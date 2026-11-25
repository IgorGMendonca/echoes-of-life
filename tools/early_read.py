"""Turn a Windsor.ai TikTok video pull into comparable numbers, match videos to log.json and keep
a dated snapshot in metrics.json (the brief asks for readings at about 24 h, 72 h and 7 days).

Usage: python3 early_read.py <rows.json> [focus_slug ...]
<rows.json> is the get_data result saved as it came (a {"data": [...]} object or a bare list), pulled
with these fields: video_id, video_caption, video_create_datetime, video_duration,
video_views_count, video_reach, video_likes, video_comments, video_shares, video_favorites,
video_average_time_watched, video_full_watched_rate, video_new_followers, video_profile_views.

Prints a table (one row per video, oldest first) with hours since posting, views per hour, the
average watch as a share of the video's length, the full-watch rate, and likes, comments,
shares, saves and new followers per 100 views. Videos are matched to log.json by "tiktok_id",
then by the start of the caption, then by duration; the match is written back to log.json.
Early numbers on a new account are noisy: read them as hints, never as rules.
"""
import datetime as dt, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = json.load(open(sys.argv[1]))
rows = raw.get("data", raw) if isinstance(raw, dict) else raw
focus = set(sys.argv[2:])
log_path = os.path.join(ROOT, "log.json")
log = json.load(open(log_path))
now = dt.datetime.now(dt.timezone.utc)


def num(x):
    return float(x) if x not in (None, "") else 0.0


def exact(r):
    for e in log:
        if e.get("tiktok_id") == r["video_id"]:
            return e
    cap = (r.get("video_caption") or "").strip().lower()
    for e in log:
        c = (e.get("caption") or "").strip().lower()
        if c and cap.startswith(c[:40]):
            return e
    return None


# exact matches first (id, then caption); then duration, only when one video and one log entry
# point at each other and nothing else (Igor sometimes rewrites a caption or posts two versions)
found = {r["video_id"]: exact(r) for r in rows}
for r in rows:
    if found[r["video_id"]] is not None:
        found[r["video_id"]].setdefault("tiktok_id", r["video_id"])
free = [e for e in log if not e.get("tiktok_id") and e.get("duration")]
close = lambda e, r: abs(float(e["duration"]) - num(r.get("video_duration"))) <= 0.12
left = [r for r in rows if found[r["video_id"]] is None]
for r in left:
    cands = [e for e in free if close(e, r)]
    if len(cands) == 1 and sum(close(cands[0], q) for q in left) == 1:
        found[r["video_id"]] = cands[0]
        cands[0]["tiktok_id"] = r["video_id"]


table = []
for r in rows:
    created = dt.datetime.fromisoformat(r["video_create_datetime"]).replace(tzinfo=dt.timezone.utc)
    hours = max((now - created).total_seconds() / 3600, 0.01)
    v, d = num(r.get("video_views_count")), num(r.get("video_duration"))
    e = found[r["video_id"]]
    per100 = (lambda k: round(100 * num(r.get(k)) / v, 1) if v else 0.0)
    table.append({
        "slug": e["slug"] if e else "?", "video_id": r["video_id"],
        "format": (e.get("kind") or e.get("format")) if e else "?",
        "posted_utc": created.isoformat(timespec="minutes"), "hours": round(hours, 1),
        "views": int(v), "views_per_hour": round(v / hours, 1),
        "watch_share": round(num(r.get("video_average_time_watched")) / d, 3) if d else 0.0,
        "avg_watch_s": num(r.get("video_average_time_watched")), "duration_s": d,
        "full_watch": round(num(r.get("video_full_watched_rate")), 4),
        "likes_100": per100("video_likes"), "comments_100": per100("video_comments"),
        "shares_100": per100("video_shares"), "saves_100": per100("video_favorites"),
        "follows_100": per100("video_new_followers"),
        "caption": (r.get("video_caption") or "")[:60],
    })
table.sort(key=lambda t: t["posted_utc"])
json.dump(log, open(log_path, "w"), indent=1, ensure_ascii=False)

m_path = os.path.join(ROOT, "metrics.json")
metrics = json.load(open(m_path)) if os.path.exists(m_path) else []
metrics.append({"taken_utc": now.isoformat(timespec="minutes"), "videos": table})
json.dump(metrics, open(m_path, "w"), indent=1, ensure_ascii=False)

print("| slug | kind | hours | views | views/h | avg watch | full watch | likes/100 | comments/100 | shares/100 | saves/100 | follows/100 |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for t in table:
    mark = " ←" if t["slug"] in focus else ""
    print(f"| {t['slug']}{mark} | {t['format']} | {t['hours']} | {t['views']} | {t['views_per_hour']} | "
          f"{t['avg_watch_s']:.1f} s of {t['duration_s']:.0f} s ({100 * t['watch_share']:.0f}%) | "
          f"{100 * t['full_watch']:.1f}% | {t['likes_100']} | {t['comments_100']} | {t['shares_100']} | "
          f"{t['saves_100']} | {t['follows_100']} |")
missing = [e["slug"] for e in log if e.get("post_date") and not e.get("tiktok_id")]
if missing:
    print("\nIn log.json with a post date but not found on TikTok in this pull:", ", ".join(missing))
