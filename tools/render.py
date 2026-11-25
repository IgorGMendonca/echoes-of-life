"""Render the vertical video: graded footage with crossfades, captions, end card, mixed audio.

Usage:
  python3 render.py <project_dir> frames 1.5 6 21 ...   # full-size stills at those times, for review
  python3 render.py <project_dir> full                  # the final mp4
Reads script.json, timeline.json, footage/scenes.json, captions.ass, audio/voice.wav and, unless
script.json has "bed": "none" (voice only), audio/music.wav
"""
import json, os, re, subprocess, sys

proj = sys.argv[1]
mode = sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "library", "fonts")
ENDCARD = os.path.join(ROOT, "library", "endcard.png")
W, H, FPS, XF = 1080, 1920, 30, 0.5

tl = json.load(open(os.path.join(proj, "timeline.json")))
scenes = json.load(open(os.path.join(proj, "footage", "scenes.json")))
cuts, total = tl["cuts"], tl["total"]
HAS_END = tl.get("endcard", True)      # ambient videos end on footage, no end card
XF = tl.get("xfade", XF)
ass = os.path.abspath(os.path.join(proj, "captions.ass"))

GRADE = ("eq=contrast=1.06:saturation=0.82:brightness=-0.035:gamma=0.97,"
         "colorbalance=rs=0.04:bs=-0.04:rm=0.02:bm=-0.02,vignette=angle=PI/4.6")
# a script may set its own look and encoder quality: the muted grade above suits the essays, while
# a city edit wants natural, vivid colour ("grade"), a lighter "sharpen" and a lower "crf"
SCRIPT = json.load(open(os.path.join(proj, "script.json")))
GRADE = SCRIPT.get("grade", GRADE)
# film grain looks nice locally but TikTok's re-encode turns it into mush: none by default since
# 2026-11-24 (a script can still ask for it with "grain")
GRAIN_AMOUNT = tl.get("grain", 0)
GRAIN = f"noise=alls={GRAIN_AMOUNT}:allf=t" if GRAIN_AMOUNT else "null"
SHARPEN = f"unsharp=5:5:{SCRIPT.get('sharpen', 0.45)}:5:5:0"


def xf(k):
    """Length of the transition into segment k (a scene may set its own "xf")."""
    return scenes[k].get("xf", XF) if k < len(scenes) else XF


def transition(k):
    """xfade transition into segment k: "fade" by default; a scene may ask for e.g. "zoomin"."""
    return scenes[k].get("transition", "fade") if k < len(scenes) else "fade"


def seg_bounds(i):
    """Start/end of segment i in output time, including crossfade overlap."""
    n = len(cuts)          # film scenes are 0..n-2, end card is n-1 (all film when HAS_END is false)
    start = cuts[i] - (xf(i) / 2 if i > 0 else 0)
    end = (cuts[i + 1] + xf(i + 1) / 2) if i + 1 < n else total
    return start, end


def pan_chain(sc, t_off=0.0):
    """One continuous shot "filmed by hand": the 9:16 window turns from one part of a wide 4K
    frame to another (eased like a person turning the phone) with a light handheld sway.
    sc["pan"] = {"from": 0..1, "to": 0..1, "at": seconds, "dur": seconds}, optional "shake" px."""
    p = sc["pan"]
    a, b, t0, d = p["from"], p["to"], p["at"], p["dur"]
    sh = sc.get("shake", 7)
    zoom = 1 + sc.get("zoom", 0.08)
    u = f"clip((t-{t0})/{d},0,1)"
    ease = f"({u}*{u}*(3-2*{u}))"
    sx = f"({sh}*sin(2*PI*0.53*t)+{sh*0.6}*sin(2*PI*1.27*t+1.3))"
    sy = f"({sh*0.8}*sin(2*PI*0.71*t+0.4)+{sh*0.5}*sin(2*PI*1.61*t+2.1))"
    ch = f"trunc(ih/{zoom}/2)*2"
    crop = (f"crop=w=trunc({ch}*9/16/2)*2:h={ch}:"
            f"x='max(0,min(iw-ow,(iw-ow)*({a}+({b}-{a})*{ease})+{sx}))':"
            f"y='max(0,min(ih-oh,(ih-oh)/2+{sy}))'")
    pre = f"setpts=PTS-STARTPTS+{t_off}/TB," if t_off else ""
    eq = ("," + sc["eq"]) if sc.get("eq") else ""
    return f"fps={FPS},{pre}{crop},scale={W}:{H}:flags=lanczos,setsar=1{eq},{SHARPEN},format=yuv420p"


def scene_chain(i, length, t_off=0.0):
    """Filter chain for film scene i (input already trimmed by -ss/-t)."""
    sc = scenes[i]
    if sc.get("pan"):
        return pan_chain(sc, t_off)
    zoom = sc.get("zoom", 0.05)
    frames = max(1, int(round(length * FPS)))
    if sc.get("vertical"):
        base = f"scale={W*2}:{H*2}:flags=lanczos,setsar=1"
    else:
        fx = sc.get("fx", 0.5)
        base = (f"crop=w=trunc(ih*9/16/2)*2:h=ih:x=(iw-ow)*{fx}:y=0,"
                f"scale={W*2}:{H*2}:flags=lanczos,setsar=1")
    if sc.get("eq"):
        base += "," + sc["eq"]
    zp = (f"zoompan=z='1+{zoom}*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d=1:s={W}x{H}:fps={FPS}")
    if sc.get("zoom_out"):
        zp = (f"zoompan=z='1+{zoom}*(1-on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d=1:s={W}x{H}:fps={FPS}")
    return f"fps={FPS},{base},{zp},{SHARPEN},setsar=1,format=yuv420p"


def endcard_chain(length):
    frames = int(round(length * FPS))
    return (f"loop=loop=-1:size=1:start=0,trim=duration={length},fps={FPS},"
            f"zoompan=z='1+0.035*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
            f"setsar=1,format=yuv420p")


def subs():
    return f"subtitles=filename='{ass}':fontsdir='{FONTS}'"


if mode == "frames":
    os.makedirs(os.path.join(proj, "review"), exist_ok=True)
    for t in map(float, sys.argv[3:]):
        i = max(k for k in range(len(cuts)) if cuts[k] <= t)
        out = os.path.join(proj, "review", f"frame_{t:05.1f}.jpg")
        if HAS_END and i == len(cuts) - 1:
            inp = ["-loop", "1", "-i", ENDCARD]
            chain = f"scale={W}:{H},setsar=1,format=yuv420p"
        else:
            s0, _ = seg_bounds(i)
            sc = scenes[i]
            sp = sc.get("speed", 1.0)
            inp = ["-ss", str(sc["src_start"] + (t - s0) * sp), "-i", sc["file"]]
            chain = scene_chain(i, 1.0, t_off=t - s0)
        vf = f"{chain},setpts=PTS-STARTPTS+{t}/TB,{GRADE},{GRAIN},{subs()}"
        subprocess.run(["ffmpeg", "-y", "-v", "error", *inp, "-frames:v", "1", "-vf", vf, "-q:v", "2", out],
                       check=True)
        print(out)
    sys.exit()

# full render
inputs, parts = [], []
n = len(cuts)
for i in range(n):
    s0, s1 = seg_bounds(i)
    L = round(s1 - s0, 3)
    if HAS_END and i == n - 1:
        inputs += ["-i", ENDCARD]
        parts.append(f"[{i}:v]{endcard_chain(L)}[s{i}]")
    else:
        sc = scenes[i]
        sp = sc.get("speed", 1.0)          # >1 plays the clip faster (more motion, more punch)
        inputs += ["-ss", str(sc["src_start"]), "-t", str(L * sp + 0.3), "-i", sc["file"]]
        parts.append(f"[{i}:v]trim=duration={round(L * sp, 3)},setpts=(PTS-STARTPTS)/{sp},"
                     f"{scene_chain(i, L)}[s{i}]")
prev = "s0"
for k in range(1, n):
    off = round(cuts[k] - xf(k) / 2, 3)
    parts.append(f"[{prev}][s{k}]xfade=transition={transition(k)}:duration={xf(k)}:offset={off}[x{k}]")
    prev = f"x{k}"
# grade the film part only: the end card stays clean black
parts.append(f"[{prev}]{GRADE},{GRAIN},{subs()},trim=duration={total},format=yuv420p[vout]")

# audio is mixed first, then brought to -14 LUFS with one fixed gain and a limiter. A one-pass
# loudnorm rides the gain up in every pause, so the music surged between sentences (v008).
# The bed is compressed so the closing swell stays under the voice, and the slow release keeps it
# down through the short pauses between lines.
# "bed": "none" in script.json: voice only (Igor adds a song from the TikTok library, 2026-11-24)
def premix():
    raw = os.path.join(proj, "audio", "mix_raw.wav")
    final = os.path.join(proj, "audio", "mix.wav")
    script = json.load(open(os.path.join(proj, "script.json")))
    if script.get("bed") == "none" or not os.path.exists(os.path.join(proj, "audio", "music.wav")):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(proj, "audio", "voice.wav"),
                        "-af", f"aresample=48000,atrim=0:{total}", "-c:a", "pcm_s16le", raw], check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(proj, "audio", "voice.wav"),
                        "-i", os.path.join(proj, "audio", "music.wav"), "-filter_complex",
                        "[0:a]asplit=2[voice][key];[1:a]volume=0.34,acompressor=threshold=0.04:ratio=5:attack=30:release=500:makeup=1[mus];"
                        "[mus][key]sidechaincompress=threshold=0.025:ratio=3:attack=80:release=1100:makeup=1[duck];"
                        f"[voice][duck]amix=inputs=2:normalize=0,aresample=48000,atrim=0:{total}[a]",
                        "-map", "[a]", "-c:a", "pcm_s16le", raw], check=True)
    meas = subprocess.run(["ffmpeg", "-v", "info", "-i", raw, "-af", "ebur128=peak=true", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    integrated = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", meas)[-1])
    gain = -14.0 - integrated
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af",
                    f"volume={gain:.2f}dB,alimiter=limit=0.79:attack=3:release=60:level=false",
                    "-c:a", "pcm_s16le", "-ar", "48000", final], check=True)
    return final


vi = n
inputs += ["-i", premix()]
parts.append(f"[{vi}:a]atrim=0:{total}[aout]")

out = os.path.join(proj, "render", f"{os.path.basename(os.path.abspath(proj))}.mp4")
os.makedirs(os.path.dirname(out), exist_ok=True)
tmp = out.replace(".mp4", ".part.mp4")
cmd = ["ffmpeg", "-y", "-v", "error", "-nostats", *inputs, "-filter_complex", ";".join(parts),
       "-map", "[vout]", "-map", "[aout]", "-r", str(FPS),
       "-c:v", "libx264", "-preset", SCRIPT.get("preset", "medium"), "-crf", str(SCRIPT.get("crf", 16)), "-pix_fmt", "yuv420p", "-profile:v", "high",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp]
subprocess.run(cmd, check=True)
os.replace(tmp, out)
print(out)
