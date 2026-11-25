"""Render a "Cinematic One Shot" (5–12 s): one real shot held still, the whole line on screen from
the first frame, one word per line, so the viewer reads it in one breath and the loop does the rest.

Usage: python3 oneshot.py videos/<slug>
Reads footage/scenes.json with one entry:
  {"pixabay_id", "file", "src_start", "dur", "fx", optional "fx_to" (slow follow), "eq", "shake" (0 = tripod)}
and script.json:
  "stack": {"words": ["do.", "your.", ...], "x": 0.5, "y": 0.62, "size": 58, "color": "F2E7C4",
            "align": "left"|"center", "from": 0.0}
  "shade": {"top": 0.5, "strength": 0.45}  optional: darkens the frame from "top" down, for text contrast
  "music_free": true  (always: the song is added on TikTok)
  optional "grade", "sharpen", "crf", "preset" (as in render.py); the scene may set "blend_fps": true
  to blend a 24/25 fps clip into 30 fps instead of repeating frames
Writes captions.ass and render/<slug>.mp4 (silent track) for finish.py.
"""
import json, os, subprocess, sys

proj = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "library", "fonts")
script = json.load(open(os.path.join(proj, "script.json")))
sc = json.load(open(os.path.join(proj, "footage", "scenes.json")))[0]
st = script["stack"]
T = sc["dur"]
W, H, FPS = 1080, 1920, 30
CW, CH = 1120, 1992                    # a little larger than the frame when the shot has a sway

GRADE = ("eq=contrast=1.06:saturation=0.86:brightness=-0.02:gamma=0.98,"
         "colorbalance=rs=0.04:bs=-0.03:rm=0.02:bm=-0.02,vignette=angle=PI/4.6")
SHARPEN = "unsharp=5:5:0.45:5:5:0"
# a script may set its own look and encoder quality (as in render.py): "grade", "sharpen", "crf", "preset"
GRADE = script.get("grade", GRADE)
SHARPEN = f"unsharp=5:5:{script.get('sharpen', 0.45)}:5:5:0"


def ts(x):
    x = max(0, x)
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


# text: one word per line, a slim sans in warm cream, a soft shadow instead of an outline
color = st.get("color", "F2E7C4")
bgr = color[4:6] + color[2:4] + color[0:2]
size = st.get("size", 58)
align = {"left": 7, "center": 8}[st.get("align", "left")]
x, y = int(W * st.get("x", 0.5)), int(H * st.get("y", 0.6))
ass = [
    "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2",
    "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
    "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    f"Style: Stack,Inter SemiBold,{size},&H00{bgr},&H00{bgr},&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,2,{align},0,0,0,1",
    "Style: Brand,Inter Medium,30,&H99FFFFFF,&H99FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,9,0,1,0,0,8,0,0,250,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    f"Dialogue: 2,{ts(st.get('from', 0))},{ts(T)},Stack,,0,0,0,,{{\\pos({x},{y})\\fsp1\\blur0.6}}"
    + "\\N".join(st["words"]),
    f"Dialogue: 0,{ts(0)},{ts(T)},Brand,,0,0,0,,ECHOES OF LIFE",
]
ass_path = os.path.abspath(os.path.join(proj, "captions.ass"))
open(ass_path, "w").write("\n".join(ass) + "\n")

# optional shade: a soft vertical gradient that darkens the lower part of the frame behind the text
shade = script.get("shade")
shade_png = None
if shade:
    from PIL import Image
    top, k = shade.get("top", 0.5), shade.get("strength", 0.45)
    g = Image.new("RGBA", (W, H))
    px = g.load()
    for yy in range(H):
        u = min(max((yy / H - top) / max(1e-6, 1 - top), 0), 1)
        a = int(255 * k * (u * u * (3 - 2 * u)))
        for xx in range(W):
            px[xx, yy] = (0, 0, 0, a)
    shade_png = os.path.abspath(os.path.join(proj, "footage", "shade.png"))
    g.save(shade_png)

fx = sc.get("fx", 0.5)
cx = (f"'(iw-ow)*({fx}+({sc['fx_to']}-{fx})*min(t/{T},1))'" if sc.get("fx_to") is not None
      else f"(iw-ow)*{fx}")
eq = ("," + sc["eq"]) if sc.get("eq") else ""
sh = sc.get("shake", 0)
if sh:
    sx = f"({sh}*sin(2*PI*0.47*t)+{sh*0.55}*sin(2*PI*1.19*t+1.1))"
    sy = f"({sh*0.8}*sin(2*PI*0.63*t+0.5)+{sh*0.5}*sin(2*PI*1.53*t+2.3))"
    hold = (f"scale={CW}:{CH}:flags=lanczos,crop=w={W}:h={H}:"
            f"x='{(CW-W)//2}+{sx}':y='{(CH-H)//2}+{sy}'")
else:
    hold = f"scale={W}:{H}:flags=lanczos"
base = (f"[0:v]trim=duration={T},setpts=PTS-STARTPTS,{'framerate=fps=' if sc.get('blend_fps') else 'fps='}{FPS},"
        f"crop=w=trunc(ih*9/16/2)*2:h=ih:x={cx}:y=0,{hold},setsar=1{eq},{SHARPEN},{GRADE}")
subs = f"subtitles=filename='{ass_path}':fontsdir='{FONTS}',format=yuv420p[vout]"
fc = ";".join([
    (f"{base}[bg];[bg][1:v]overlay=0:0:shortest=1,{subs}" if shade_png else f"{base},{subs}"),
    f"anullsrc=r=48000:cl=stereo,atrim=0:{T}[aout]",
])
out = os.path.join(proj, "render", f"{os.path.basename(os.path.abspath(proj))}.mp4")
os.makedirs(os.path.dirname(out), exist_ok=True)
tmp = out.replace(".mp4", ".part.mp4")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-nostats",
                "-ss", str(sc["src_start"]), "-t", str(T + 0.3), "-i", sc["file"],
                *(["-loop", "1", "-t", str(T + 0.3), "-i", shade_png] if shade_png else []),
                "-filter_complex", fc, "-map", "[vout]", "-map", "[aout]", "-r", str(FPS),
                "-c:v", "libx264", "-preset", script.get("preset", "medium"), "-crf", str(script.get("crf", 16)), "-pix_fmt", "yuv420p", "-profile:v", "high",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp], check=True)
os.replace(tmp, out)
print(out)
