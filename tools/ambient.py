"""Timeline for an ambient video: a few scenic shots, no narration, optional one-line text.

Usage: python3 ambient.py videos/<slug>
Reads script.json ("format": "ambient", optional "text") and footage/scenes.json (each scene
has "dur" in seconds). Writes timeline.json (no end card), captions.ass and a silent
audio/voice.wav, so render.py and finish.py work unchanged. Music comes from music.py; Igor
can replace it with a song from the TikTok library when posting.
"""
import json, os, subprocess, sys

proj = sys.argv[1]
script = json.load(open(os.path.join(proj, "script.json")))
scenes = json.load(open(os.path.join(proj, "footage", "scenes.json")))
W, H = 1080, 1920
XF = script.get("xfade", 0.45)

cuts, t = [], 0.0
for sc in scenes:
    cuts.append(round(t, 3))
    t += sc["dur"]
total = round(t, 3)


def ts(x):
    x = max(0, x)
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


ass = [
    "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0",
    "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
    "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Line,Playfair Display,80,&H00FFFFFF,&H00FFFFFF,&H8C000000,&H00000000,0,1,0,0,100,100,0,0,1,3,0,5,90,90,0,1",
    "Style: Brand,Inter Medium,30,&H99FFFFFF,&H99FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,9,0,1,0,0,8,0,0,250,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
# one line ("text") or several in sequence ("texts", e.g. a setup early and its payoff on the last
# shot); each may set "x" (0-1, centre of the line) to sit beside the subject instead of over it
texts = script.get("texts") or ([script["text"]] if script.get("text") else [])
for text in texts:
    if not text.get("line"):
        continue
    a = text.get("from", 0.5)
    b = text.get("to", total - 0.3)
    x = int(W * text.get("x", 0.5))
    ass.append(f"Dialogue: 2,{ts(a)},{ts(b)},Line,,0,0,0,,{{\\pos({x},{int(H*text.get('y', 0.34))})\\fad(500,400)\\blur9}}"
               + text["line"].replace("\n", "\\N"))
ass.append(f"Dialogue: 0,{ts(0.2)},{ts(total)},Brand,,0,0,0,,{{\\fad(400,300)}}ECHOES OF LIFE")
open(os.path.join(proj, "captions.ass"), "w").write("\n".join(ass) + "\n")

os.makedirs(os.path.join(proj, "audio"), exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                "-t", str(total), os.path.join(proj, "audio", "voice.wav")], check=True)
json.dump({"lines": [], "words": [], "cuts": cuts, "total": total, "speech_end": 0,
           "endcard": False, "xfade": XF, "grain": script.get("grain", 0)}, open(os.path.join(proj, "timeline.json"), "w"), indent=1)
print("total", total, "cuts", cuts)
