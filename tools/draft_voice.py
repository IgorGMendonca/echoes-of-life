"""Stand-in for tts.py when the images are reviewed before paying for a voice.

Usage: python3 draft_voice.py videos/<slug>
Writes silent audio/line_XX.wav and audio/alignment.json in the same shape tts.py writes, with
each line timed at Brian's measured pace (15.6 characters a second, from v002) and short pauses at
punctuation. timeline.py, render.py and the captions then work unchanged, so the draft shows the
real pacing; run tts.py later and the timings are replaced by the real ones (re-run timeline.py).
"""
import json, os, subprocess, sys

proj = sys.argv[1]
script = json.load(open(os.path.join(proj, "script.json")))
CPS = 15.6                     # characters per second, Brian at speed 0.9 (v002)
PAUSE = {",": 0.18, ".": 0.28, "?": 0.28, "!": 0.28, ";": 0.22, ":": 0.22, "—": 0.22}
os.makedirs(os.path.join(proj, "audio"), exist_ok=True)

out = []
for i, line in enumerate(script["lines"]):
    text = line["text"]
    chars, st, en, t = [], [], [], 0.0
    for c in text:
        d = 1 / CPS + PAUSE.get(c, 0) * 0.5
        chars.append(c); st.append(round(t, 3)); en.append(round(t + d, 3)); t += d
    name = f"line_{i:02d}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", f"{t + 0.05:.3f}", os.path.join(proj, "audio", name)], check=True)
    out.append({"index": i, "text": text, "file": name, "draft": True, "cost": "0",
                "alignment": {"characters": chars, "character_start_times_seconds": st,
                              "character_end_times_seconds": en}})
json.dump(out, open(os.path.join(proj, "audio", "alignment.json"), "w"))
print("draft voice:", len(out), "lines,", round(sum(o["alignment"]["character_end_times_seconds"][-1] for o in out), 1), "s of speech")
