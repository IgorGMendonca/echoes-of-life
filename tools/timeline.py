"""Lay the voice lines on a timeline, build the voice track, word timings and the ASS captions.

Usage: python3 timeline.py <project_dir>
Writes timeline.json, audio/voice.wav, captions.ass
"""
import json, os, re, subprocess, sys

proj = sys.argv[1]
script = json.load(open(os.path.join(proj, "script.json")))
al = json.load(open(os.path.join(proj, "audio", "alignment.json")))

LEAD = 0.5
TAIL_HOLD = 1.2        # last scene keeps playing after the final word
ENDCARD = 2.8
W, H = 1080, 1920


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).decode())


def gap_after(text, i, n):
    if i == n - 1:
        return 0
    if i == 0:
        return 1.0                      # let the hook land
    if text.rstrip().endswith((".", "?", "!")) and len(text) < 60:
        return 0.95
    return 0.75


# 1. place lines
t = LEAD
lines = []
for a in al:
    a["file"] = os.path.join(proj, "audio", os.path.basename(a["file"]))
for i, a in enumerate(al):
    d = dur(a["file"])
    lines.append({"index": i, "text": a["text"], "file": a["file"], "start": round(t, 3), "dur": round(d, 3)})
    t += d + gap_after(a["text"], i, len(al))
speech_end = lines[-1]["start"] + lines[-1]["dur"]
total = round(speech_end + TAIL_HOLD + ENDCARD, 3)

# 2. scene cuts: each scene starts a little before its line
CUT_LEAD = 0.3
cuts = [0.0] + [round(l["start"] - CUT_LEAD, 3) for l in lines[1:]] + [round(speech_end + TAIL_HOLD, 3)]

# 3. words with absolute times, from the character alignment
words = []
for l, a in zip(lines, al):
    chars = a["alignment"]["characters"]
    st = a["alignment"]["character_start_times_seconds"]
    en = a["alignment"]["character_end_times_seconds"]
    cur, ws, we = "", None, None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur:
                words.append({"line": l["index"], "w": cur, "s": l["start"] + ws, "e": l["start"] + we})
            cur, ws = "", None
            continue
        if ws is None:
            ws = s
        cur += c
        we = e
    if cur:
        words.append({"line": l["index"], "w": cur, "s": l["start"] + ws, "e": l["start"] + we})

# 4. chunk words into caption groups: phrases end at punctuation; long phrases are split
#    into balanced pieces of about MAXC characters, so no word is left alone on screen
MAXC = 21
phrases, cur = [], []
for k, w in enumerate(words):
    cur.append(w)
    nxt = words[k + 1] if k + 1 < len(words) else None
    if re.search(r"[.,!?;:…]$", w["w"]) or nxt is None or nxt["line"] != w["line"]:
        phrases.append(cur)
        cur = []


def clen(ws):
    return len(" ".join(x["w"] for x in ws))


def split_balanced(ws):
    if clen(ws) <= MAXC + 3 or len(ws) < 2:
        return [ws]
    n = -(-clen(ws) // MAXC)
    best, best_cost = None, None
    # try every way to cut into n parts, keep the one with the most even lengths
    import itertools
    for cut in itertools.combinations(range(1, len(ws)), n - 1):
        parts = [ws[a:b] for a, b in zip((0,) + cut, cut + (len(ws),))]
        weak = {"a", "an", "the", "your", "to", "of", "my", "and", "is", "this", "you'd"}
        cost = max(clen(p) for p in parts) + (100 if any(len(p) == 1 and clen(p) < 8 for p in parts) else 0) \
            + 6 * sum(p[-1]["w"].lower().strip(",.") in weak for p in parts[:-1])
        if best_cost is None or cost < best_cost:
            best, best_cost = parts, cost
    return best


chunks = [part for ph in phrases for part in split_balanced(ph)]
# glue a very short phrase (one short word) onto the previous chunk of the same line
merged = []
for ch in chunks:
    if merged and len(ch) == 1 and clen(ch) <= 5 and merged[-1][0]["line"] == ch[0]["line"] \
            and clen(merged[-1]) + clen(ch) <= MAXC + 4:
        merged[-1] = merged[-1] + ch
    else:
        merged.append(ch)
chunks = merged

# 5. ASS captions (karaoke fill per word); the hook line is shown as a serif title instead
def ts(x):
    x = max(0, x)
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"


hook_line = 0
ass = [
    "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0",
    "ScaledBorderAndShadow: yes", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
    "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    # captions: white fill, unsung words 55% transparent
    "Style: Cap,Inter SemiBold,82,&H00FFFFFF,&H00BEBEBE,&H8C000000,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,80,80,0,1",
    "Style: Hook,Playfair Display,116,&H00FFFFFF,&H00FFFFFF,&H8C000000,&H00000000,0,1,0,0,100,100,0,0,1,3,0,5,90,90,0,1",
    "Style: Brand,Inter Medium,30,&H99FFFFFF,&H99FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,9,0,1,0,0,8,0,0,250,1",
    "Style: End,Playfair Display,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1",
    "Style: EndSub,Inter Light,40,&H33FFFFFF,&H33FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,4,0,1,0,0,5,0,0,0,1",
    "", "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
CAP_Y = int(H * 0.64)
for ch in chunks:
    if ch[0]["line"] == hook_line:
        continue
    s = ch[0]["s"] - 0.08
    nxt_chunks = [c for c in chunks if c[0]["s"] > ch[0]["s"]]
    e = min(ch[-1]["e"] + 0.35, nxt_chunks[0][0]["s"] - 0.1) if nxt_chunks else ch[-1]["e"] + 0.6
    parts, prev = [], s
    for w in ch:
        lead_cs = max(0, int(round((w["s"] - prev) * 100)))
        fill_cs = max(1, int(round((w["e"] - w["s"]) * 100)))
        parts.append(f"{{\\k{lead_cs}}}{{\\kf{fill_cs}}}{w['w']}")
        prev = w["e"]
    text = " ".join(parts)
    ass.append(f"Dialogue: 1,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\pos({W//2},{CAP_Y})\\fad(120,100)\\blur7}}{text}")

# hook title: big serif, two lines, held through the first scene
hook = lines[hook_line]
hw = [w for w in words if w["line"] == hook_line]
split = len(hw) // 2 + (1 if len(hw) % 2 else 0)
hook_text = " ".join(w["w"] for w in hw[:split]) + "\\N" + " ".join(w["w"] for w in hw[split:])
ass.append(f"Dialogue: 2,{ts(0.25)},{ts(cuts[1] + 0.2)},Hook,,0,0,0,,{{\\pos({W//2},{int(H*0.34)})\\fad(450,350)\\blur9}}{hook_text}")

# small wordmark during the film part
ass.append(f"Dialogue: 0,{ts(0.4)},{ts(cuts[-1])},Brand,,0,0,0,,{{\\fad(600,400)}}ECHOES OF LIFE")
# end card text
ec = cuts[-1]
ass.append(f"Dialogue: 3,{ts(ec + 0.35)},{ts(total)},End,,0,0,0,,{{\\pos({W//2},{int(H*0.57)})\\fad(600,0)}}Echoes of Life")
ass.append(f"Dialogue: 3,{ts(ec + 0.9)},{ts(total)},EndSub,,0,0,0,,{{\\pos({W//2},{int(H*0.63)})\\fad(600,0)}}{script.get('endcard', 'follow for more')}")
open(os.path.join(proj, "captions.ass"), "w").write("\n".join(ass) + "\n")

# 6. voice track: place each line at its start
inputs, filt = [], []
for k, l in enumerate(lines):
    inputs += ["-i", l["file"]]
    ms = int(round(l["start"] * 1000))
    filt.append(f"[{k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]")
mix = "".join(f"[a{k}]" for k in range(len(lines)))
filt.append(f"{mix}amix=inputs={len(lines)}:normalize=0,apad,atrim=0:{total}[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[v]",
                "-ac", "2", "-ar", "48000", os.path.join(proj, "audio", "voice.wav")], check=True)

json.dump({"lines": lines, "cuts": cuts, "total": total, "speech_end": speech_end, "words": words},
          open(os.path.join(proj, "timeline.json"), "w"), indent=1)
print("total", total, "speech_end", round(speech_end, 2))
print("cuts", cuts)
print("chunks", [" ".join(w["w"] for w in c) for c in chunks])
