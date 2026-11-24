"""Render the vertical video: graded footage with crossfades, captions, end card, mixed audio.

Usage:
  python3 render.py <project_dir> frames 1.5 6 21 ...   # full-size stills at those times, for review
  python3 render.py <project_dir> full                  # the final mp4
Reads script.json, timeline.json, footage/scenes.json, captions.ass, audio/voice.wav, audio/music.wav
"""
import json, os, subprocess, sys

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
GRAIN = "noise=alls=5:allf=t"


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


def scene_chain(i, length, t_out0=None):
    """Filter chain for film scene i (input already trimmed by -ss/-t)."""
    sc = scenes[i]
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
    return f"fps={FPS},{base},{zp},setsar=1,format=yuv420p"


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
            chain = scene_chain(i, 1.0)
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

vi = n
inputs += ["-i", os.path.join(proj, "audio", "voice.wav"), "-i", os.path.join(proj, "audio", "music.wav")]
parts.append(f"[{vi}:a]asplit=2[voice][key]")
parts.append(f"[{vi+1}:a]volume=0.45[mus]")
parts.append("[mus][key]sidechaincompress=threshold=0.025:ratio=4:attack=60:release=700:makeup=1[duck]")
parts.append(f"[voice][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,"
             f"aresample=48000,atrim=0:{total}[aout]")

out = os.path.join(proj, "render", f"{os.path.basename(os.path.abspath(proj))}.mp4")
os.makedirs(os.path.dirname(out), exist_ok=True)
tmp = out.replace(".mp4", ".part.mp4")
cmd = ["ffmpeg", "-y", "-v", "error", "-nostats", *inputs, "-filter_complex", ";".join(parts),
       "-map", "[vout]", "-map", "[aout]", "-r", str(FPS),
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp]
subprocess.run(cmd, check=True)
os.replace(tmp, out)
print(out)
