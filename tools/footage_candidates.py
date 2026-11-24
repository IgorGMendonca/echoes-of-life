"""Search Pixabay videos for each script line and build contact sheets to pick from.

Usage: python3 footage_candidates.py <project_dir> [per_query]
Writes <project_dir>/footage/candidates.json and sheet_XX.jpg (one per line).
"""
import io, json, os, sys, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont

proj = sys.argv[1]
per = int(sys.argv[2]) if len(sys.argv) > 2 else 6
key = os.environ["PIXABAY_KEY"]
script = json.load(open(os.path.join(proj, "script.json")))
os.makedirs(os.path.join(proj, "footage"), exist_ok=True)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)


def search(q):
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
        {"key": key, "q": q, "per_page": 20, "safesearch": "true", "order": "popular"})
    return json.load(get(url))["hits"]


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0"}))


def fetch(url):
    return Image.open(io.BytesIO(get(url).read())).convert("RGB")


allc = {}
for i, line in enumerate(script["lines"]):
    hits, seen = [], set()
    for q in (line["query"], line.get("alt")):
        if not q:
            continue
        for h in search(q):
            if h["id"] in seen or h["duration"] < 4:
                continue
            seen.add(h["id"]); hits.append(h)
            if len([x for x in hits if x.get("_q") is None]) >= per * 2:
                break
    hits = hits[: per * 2]
    allc[i] = [{"id": h["id"], "duration": h["duration"], "tags": h["tags"],
                "large": h["videos"]["large"], "medium": h["videos"]["medium"]} for h in hits]
    tw, th = 384, 216
    cols = 4
    rows = max(1, (len(hits) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * tw, rows * (th + 30)), "black")
    d = ImageDraw.Draw(sheet)
    for k, h in enumerate(hits):
        try:
            im = fetch(h["videos"]["small"]["thumbnail"] or h["videos"]["tiny"]["thumbnail"]).resize((tw, th))
        except Exception:
            continue
        x, y = (k % cols) * tw, (k // cols) * (th + 30)
        sheet.paste(im, (x, y))
        d.text((x + 6, y + th + 3), f"{h['id']}  {h['duration']}s  {h['videos']['large']['width']}w", fill="white", font=font)
    sheet.save(os.path.join(proj, "footage", f"sheet_{i:02d}.jpg"), quality=80)
    print(i, line["query"], len(hits))

json.dump(allc, open(os.path.join(proj, "footage", "candidates.json"), "w"))
