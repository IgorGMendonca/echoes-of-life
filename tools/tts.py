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

Direction (from 2026-11-25, Igor chose the eleven_v4 test with emotion over the flat v2 read):
  "voice": {"voice_id", "name", "model_id": "eleven_v4", "settings": {"stability": 0.5, "similarity_boost": 0.75},
            "language_code": "pt", "context": "<unspoken framing sent as previous_text>", "seed": 7, "join": "\n"}
  a line may carry "say": the spoken form with English audio tags at its start ("[wistful] ...") and ellipses for
  pauses; "text" stays the caption. Tags go only at the start of a line (they would show in the captions otherwise)
  and only on the shifts. v4 ignores style and speed, and multilingual_v2 speaks tags aloud, so "say" needs v4.
  Without these keys the old v2 settings below are used.
  "tempo" in the voice block (0.95 to 1.08) slows or speeds the finished take without changing the pitch, because
  v4 ignores speed and read the first v4 script (v021) about 15% faster than v2; the raw take stays in
  audio/take_raw.mp3. `tts.py <project_dir> --tempo 0.95` applies it to the take already recorded, at no cost.
"""
import base64, difflib, json, os, sys, urllib.error, urllib.request

proj = sys.argv[1]
args = sys.argv[2:]
script = json.load(open(os.path.join(proj, "script.json")))
voice = script["voice"]
key = os.environ.get("ELEVEN_KEY")         # needed only to record (not for --tempo)
os.makedirs(os.path.join(proj, "audio"), exist_ok=True)
lines = [l["text"] for l in script["lines"]]
says = [l.get("say", l["text"]) for l in script["lines"]]
SETTINGS = voice.get("settings") or {"stability": 0.55, "similarity_boost": 0.8, "style": 0.25,
                                     "use_speaker_boost": True, "speed": 0.9}
SEP = voice.get("join", " ")


def speak(text, previous=None, following=None):
    body = {"text": text, "model_id": voice["model_id"], "voice_settings": SETTINGS,
            "previous_text": previous or None, "next_text": following or None}
    for k in ("language_code", "seed"):
        if voice.get(k) is not None:
            body[k] = voice[k]
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


def apply_tempo(t):
    """Stretch audio/take.mp3 by atempo t (pitch kept) and scale the line offsets and character times to match."""
    a_dir = os.path.join(proj, "audio")
    raw, raw_al = os.path.join(a_dir, "take_raw.mp3"), os.path.join(a_dir, "alignment_raw.json")
    if not os.path.exists(raw):
        os.replace(os.path.join(a_dir, "take.mp3"), raw)
        os.replace(os.path.join(a_dir, "alignment.json"), raw_al)
    import subprocess
    tmp = os.path.join(a_dir, "take.part.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-filter:a", f"atempo={t}", "-c:a", "libmp3lame",
                    "-b:a", "192k", tmp], check=True)
    os.replace(tmp, os.path.join(a_dir, "take.mp3"))
    al = json.load(open(raw_al))
    for o in al:
        o["offset"] = round(o["offset"] / t, 3)
        for k in ("character_start_times_seconds", "character_end_times_seconds"):
            o["alignment"][k] = [round(x / t, 3) for x in o["alignment"][k]]
        o["tempo"] = t
    json.dump(al, open(os.path.join(a_dir, "alignment.json"), "w"))
    last = al[-1]
    print("tempo", t, "speech", round(last["offset"] + last["alignment"]["character_end_times_seconds"][-1], 2), "s")


if args and args[0] == "--tempo":
    apply_tempo(float(args[1]))
    sys.exit(0)

if args and args[0] == "--per-line":
    only = {int(a) for a in args[1:]}
    out = []
    if only:
        old = {a["index"]: a for a in json.load(open(os.path.join(proj, "audio", "alignment.json")))}
    for i, text in enumerate(lines):
        if only and i not in only:
            out.append(old[i])
            continue
        d, cost = speak(says[i], " ".join(lines[:i])[-400:], " ".join(lines[i + 1:])[:400])
        path = os.path.join(proj, "audio", f"line_{i:02d}.mp3")
        open(path, "wb").write(base64.b64decode(d["audio_base64"]))
        out.append({"index": i, "text": text, "file": os.path.basename(path), "alignment": d["alignment"], "cost": cost})
        print(i, "cost", cost, "end", d["alignment"]["character_end_times_seconds"][-1])
    json.dump(out, open(os.path.join(proj, "audio", "alignment.json"), "w"))
    sys.exit(0)

# one take: the spoken form is sent, the caption text is mapped onto the returned characters
full = SEP.join(lines)
d, cost = speak(SEP.join(says), voice.get("context"))
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
print("one take:", len(SEP.join(says)), "characters, cost", cost, "speech", round(en[-1], 2), "s")
for o in out:
    e = o["alignment"]["character_end_times_seconds"][-1]
    print(o["index"], "at", o["offset"], "for", e, "s,", round(len(o["text"]) / max(e, 0.01), 1), "chars/s")
if voice.get("tempo"):
    apply_tempo(voice["tempo"])
