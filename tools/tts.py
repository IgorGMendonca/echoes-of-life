"""Generate the ElevenLabs narration with character timestamps.

Usage:
  python3 tts.py <project_dir>                       # one continuous take of the whole script (default)
  python3 tts.py <project_dir> --per-line [i ...]    # old mode: one clip per line (only lines i ... if given)

One take (since 2026-11-24): the whole script is read in a single request, so the voice carries its
own breaths and natural pauses from sentence to sentence. Separate clips ended in a falling
intonation and were joined by holes of digital silence, which Igor heard as the audio stalling
after every sentence (v008). Writes audio/take.mp3 and audio/alignment.json: one entry per line
with "take": true, "offset" (where the line starts in the take) and its character times relative
to that offset, so timeline.py can place lines, captions and cuts.
"""
import base64, difflib, json, os, sys, urllib.error, urllib.request

proj = sys.argv[1]
args = sys.argv[2:]
script = json.load(open(os.path.join(proj, "script.json")))
voice = script["voice"]
key = os.environ["ELEVEN_KEY"]
os.makedirs(os.path.join(proj, "audio"), exist_ok=True)
lines = [l["text"] for l in script["lines"]]
SETTINGS = {"stability": 0.55, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True, "speed": 0.9}


def speak(text, previous=None, following=None):
    body = {"text": text, "model_id": voice["model_id"], "voice_settings": SETTINGS,
            "previous_text": previous or None, "next_text": following or None}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice['voice_id']}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            cost = r.headers.get("character-cost") or r.headers.get("x-character-count")
            return json.load(r), cost
    except urllib.error.HTTPError as e:
        # quota_exceeded / missing_permissions etc.: print the reason and stop
        print("ElevenLabs error", e.code, e.read().decode()[:500], file=sys.stderr)
        sys.exit(2)


if args and args[0] == "--per-line":
    only = {int(a) for a in args[1:]}
    out = []
    if only:
        old = {a["index"]: a for a in json.load(open(os.path.join(proj, "audio", "alignment.json")))}
    for i, text in enumerate(lines):
        if only and i not in only:
            out.append(old[i])
            continue
        d, cost = speak(text, " ".join(lines[:i])[-400:], " ".join(lines[i + 1:])[:400])
        path = os.path.join(proj, "audio", f"line_{i:02d}.mp3")
        open(path, "wb").write(base64.b64decode(d["audio_base64"]))
        out.append({"index": i, "text": text, "file": os.path.basename(path), "alignment": d["alignment"], "cost": cost})
        print(i, "cost", cost, "end", d["alignment"]["character_end_times_seconds"][-1])
    json.dump(out, open(os.path.join(proj, "audio", "alignment.json"), "w"))
    sys.exit(0)

# one take
full = " ".join(lines)
d, cost = speak(full)
open(os.path.join(proj, "audio", "take.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
al = d["alignment"]
chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
spoken = "".join(chars)

# map each position of our text to a position in the returned characters (usually identical)
if spoken == full:
    pos = list(range(len(full)))
else:
    pos = [None] * len(full)
    for a, b, n in difflib.SequenceMatcher(None, full, spoken, autojunk=False).get_matching_blocks():
        for k in range(n):
            pos[a + k] = b + k

out, p = [], 0
for i, text in enumerate(lines):
    idx = [pos[k] for k in range(p, p + len(text)) if pos[k] is not None]
    a, b = idx[0], idx[-1]
    off = st[a]
    out.append({"index": i, "text": text, "file": "take.mp3", "take": True, "offset": round(off, 3),
                "alignment": {"characters": chars[a:b + 1],
                              "character_start_times_seconds": [round(x - off, 3) for x in st[a:b + 1]],
                              "character_end_times_seconds": [round(x - off, 3) for x in en[a:b + 1]]},
                "cost": cost if i == 0 else "0"})
    p += len(text) + 1
json.dump(out, open(os.path.join(proj, "audio", "alignment.json"), "w"))
print("one take:", len(full), "characters, cost", cost, "speech", round(en[-1], 2), "s")
for o in out:
    e = o["alignment"]["character_end_times_seconds"][-1]
    print(o["index"], "at", o["offset"], "for", e, "s,", round(len(o["text"]) / max(e, 0.01), 1), "chars/s")
