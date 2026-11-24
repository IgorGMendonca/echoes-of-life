"""Download the clips chosen in footage/scenes.json (by pixabay_id) and fill in their file paths.

Usage: python3 fetch_clips.py videos/<slug>
Each scenes.json entry needs "pixabay_id"; "file" is set to videos/<slug>/footage/clips/scene_N.mp4.
Prefers the 4K/large rendition, falls back to medium.
"""
import json, os, sys, urllib.request

proj = sys.argv[1]
key = os.environ["PIXABAY_KEY"]
path = os.path.join(proj, "footage", "scenes.json")
scenes = json.load(open(path))
os.makedirs(os.path.join(proj, "footage", "clips"), exist_ok=True)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0"}), timeout=120)


for i, sc in enumerate(scenes):
    out = os.path.join(proj, "footage", "clips", f"scene_{i}.mp4")
    sc["file"] = out
    if os.path.exists(out) and os.path.getsize(out) > 100_000:
        continue
    hit = json.load(get(f"https://pixabay.com/api/videos/?key={key}&id={sc['pixabay_id']}"))["hits"][0]
    v = hit["videos"]
    url = v["large"]["url"] or v["medium"]["url"]
    sc["width"], sc["height"] = (v["large"]["width"], v["large"]["height"]) if v["large"]["url"] else \
        (v["medium"]["width"], v["medium"]["height"])
    sc.setdefault("vertical", sc["height"] > sc["width"])
    tmp = out + ".part"
    with get(url) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    os.replace(tmp, out)
    print(i, sc["pixabay_id"], f"{sc['width']}x{sc['height']}", os.path.getsize(out) // 1_000_000, "MB")

json.dump(scenes, open(path, "w"), indent=1)
