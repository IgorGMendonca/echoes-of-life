"""Render an ambient "tilt-up reveal": the phone starts pointed at the ground, then the person
lifts it quickly (motion blur) to the view and holds it there by hand.

Usage: python3 reveal.py videos/<slug>
Reads footage/scenes.json with two entries:
  {"role": "ground", "pixabay_id", "file", "src_start", "fx"}       the first ~1 s, looking down
  {"role": "view",   "pixabay_id", "file", "src_start", "fx", "dur", "shake"}   the scene
and script.json "reveal": {"at": seconds, "dur": seconds} (the lift). Also needs captions.ass
and audio/music.wav (run ambient.py and music.py first; with "music_free": true in script.json the
export gets a silent track instead, for a sound added on TikTok). Writes render/<slug>.mp4 for finish.py.
"""
import json, os, subprocess, sys

proj = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "library", "fonts")
script = json.load(open(os.path.join(proj, "script.json")))
scenes = json.load(open(os.path.join(proj, "footage", "scenes.json")))
ground = next(s for s in scenes if s.get("role") == "ground")
view = next(s for s in scenes if s.get("role") == "view")
rv = script.get("reveal", {"at": 0.6, "dur": 0.65})
T = view["dur"]
W, H, FPS = 1080, 1920, 30
CW, CH = 1152, 2048                     # each layer a bit larger than the frame, room for the sway
ass = os.path.abspath(os.path.join(proj, "captions.ass"))

GRADE = ("eq=contrast=1.06:saturation=0.86:brightness=-0.02:gamma=0.98,"
         "colorbalance=rs=0.04:bs=-0.03:rm=0.02:bm=-0.02,vignette=angle=PI/4.6")
SHARPEN = "unsharp=5:5:0.45:5:5:0"


def layer(sc):
    fx = sc.get("fx", 0.5)
    eq = ("," + sc["eq"]) if sc.get("eq") else ""
    return (f"trim=duration={T},setpts=PTS-STARTPTS,fps={FPS},"
            f"crop=w=trunc(ih*9/16/2)*2:h=ih:x=(iw-ow)*{fx}:y=0,"
            f"scale={CW}:{CH}:flags=lanczos,setsar=1{eq}")


a, d = rv["at"], rv["dur"]
u = f"clip((t-{a})/{d},0,1)"
ease = f"({u}*{u}*{u}*({u}*(6*{u}-15)+10))"          # smootherstep: slow start, fast middle, soft landing
sh = view.get("shake", 8)
sx = f"({sh}*sin(2*PI*0.47*t)+{sh*0.55}*sin(2*PI*1.19*t+1.1))"
sy = f"({sh*0.8}*sin(2*PI*0.63*t+0.5)+{sh*0.5}*sin(2*PI*1.53*t+2.3))"
y_top = (CH - H) // 2
x_mid = (CW - W) // 2
# canvas: the view on top, the ground below it; the window travels from the ground up to the view
y_expr = f"max(0,min({2*CH-H},{CH}*(1-{ease})+{y_top}+{sy}))"
x_expr = f"max(0,min({CW-W},{x_mid}+{sx}))"
# vertical motion blur only while the phone is moving fast
blur = f"gblur=sigma=0.01:sigmaV=28:steps=2:enable='between(t,{a+d*0.15},{a+d*0.85})'"

fc = ";".join([
    f"[0:v]{layer(ground)}[g]",
    f"[1:v]{layer(view)}[v]",
    "[v][g]vstack=inputs=2[tall]",
    f"[tall]crop=w={W}:h={H}:x='{x_expr}':y='{y_expr}',{blur},{SHARPEN},{GRADE},"
    f"subtitles=filename='{ass}':fontsdir='{FONTS}',format=yuv420p[vout]",
    # music-free export (Igor adds a TikTok sound): a silent track; otherwise the generated bed
    (f"anullsrc=r=48000:cl=stereo,atrim=0:{T}[aout]" if script.get("music_free")
     else f"[2:a]loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,atrim=0:{T}[aout]"),
])
out = os.path.join(proj, "render", f"{os.path.basename(os.path.abspath(proj))}.mp4")
os.makedirs(os.path.dirname(out), exist_ok=True)
tmp = out.replace(".mp4", ".part.mp4")
cmd = ["ffmpeg", "-y", "-v", "error", "-nostats",
       "-ss", str(ground["src_start"]), "-t", str(T + 0.3), "-i", ground["file"],
       "-ss", str(view["src_start"]), "-t", str(T + 0.3), "-i", view["file"],
       "-i", os.path.join(proj, "audio", "music.wav"),
       "-filter_complex", fc, "-map", "[vout]", "-map", "[aout]", "-r", str(FPS),
       "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-profile:v", "high",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp]
subprocess.run(cmd, check=True)
os.replace(tmp, out)
print(out)
