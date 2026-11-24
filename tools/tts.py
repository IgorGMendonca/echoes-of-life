"""Generate one ElevenLabs voice clip per script line, with character timestamps.

Usage: python3 tts.py <project_dir>
Writes <project_dir>/audio/line_XX.mp3 and <project_dir>/audio/alignment.json
"""
import base64, json, os, sys, urllib.error, urllib.request

proj = sys.argv[1]
script = json.load(open(os.path.join(proj, "script.json")))
voice = script["voice"]
key = os.environ["ELEVEN_KEY"]
os.makedirs(os.path.join(proj, "audio"), exist_ok=True)

lines = [l["text"] for l in script["lines"]]
out = []
for i, text in enumerate(lines):
    body = {
        "text": text,
        "model_id": voice["model_id"],
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.8, "style": 0.25,
                           "use_speaker_boost": True, "speed": 0.9},
        "previous_text": " ".join(lines[:i])[-400:] or None,
        "next_text": " ".join(lines[i + 1:])[:400] or None,
    }
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice['voice_id']}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            cost = r.headers.get("character-cost") or r.headers.get("x-character-count")
            d = json.load(r)
    except urllib.error.HTTPError as e:
        # quota_exceeded / missing_permissions etc.: print the reason and stop
        print("ElevenLabs error", e.code, e.read().decode()[:500], file=sys.stderr)
        sys.exit(2)
    path = os.path.join(proj, "audio", f"line_{i:02d}.mp3")
    open(path, "wb").write(base64.b64decode(d["audio_base64"]))
    out.append({"index": i, "text": text, "file": os.path.basename(path), "alignment": d["alignment"], "cost": cost})
    print(i, "cost", cost, "end", d["alignment"]["character_end_times_seconds"][-1])

json.dump(out, open(os.path.join(proj, "audio", "alignment.json"), "w"))
