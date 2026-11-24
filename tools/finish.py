"""Make the upload copy, write post.txt and check the result.

Usage: python3 finish.py videos/<slug> <upload_name>
Writes videos/<slug>/render/<upload_name>.mp4 and post.txt; prints a report and exits 1 if a check fails.
"""
import json, os, re, subprocess, sys
import numpy as np

proj, name = sys.argv[1], sys.argv[2]
slug = os.path.basename(os.path.abspath(proj))
master = os.path.join(proj, "render", f"{slug}.mp4")
out = os.path.join(proj, "render", f"{name}.mp4")
script = json.load(open(os.path.join(proj, "script.json")))

tmp = out.replace(".mp4", ".part.mp4")
# high bitrate on purpose: TikTok re-encodes everything, and a clean source survives that much better
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", master, "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-maxrate", "20M", "-bufsize", "40M", "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "copy",
                "-movflags", "+faststart", tmp], check=True)
os.replace(tmp, out)

post = script["post"]
text = post["caption"] + "\n\n" + " ".join(post["hashtags"]) + "\n"
if post.get("pinned_comment"):
    text += "\nPinned comment:\n" + post["pinned_comment"] + "\n"
open(os.path.join(proj, "render", "post.txt"), "w").write(text)

probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                            "stream=codec_type,width,height,r_frame_rate,sample_rate:format=duration,size",
                                            "-of", "json", out]))
v = [s for s in probe["streams"] if s["codec_type"] == "video"][0]
a = [s for s in probe["streams"] if s["codec_type"] == "audio"][0]
dur = float(probe["format"]["duration"])
log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
summ = log[log.rfind("Summary"):]
lufs = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1))
peak = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1))


def rms_db(path, s, e):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(s), "-t", str(e - s), "-i", path,
                                   "-ac", "1", "-f", "f32le", "-ar", "16000", "-"])
    x = np.frombuffer(raw, dtype=np.float32)
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


fmt = script.get("format", "short")
checks = {
    "size 1080x1920": (v["width"], v["height"]) == (1080, 1920),
    "30 fps": v["r_frame_rate"] == "30/1",
    "audio 48 kHz": a["sample_rate"] == "48000",
    "loudness -15..-13 LUFS": -15 <= lufs <= -13,
    "true peak <= -0.9 dBFS": peak <= -0.9,
    "duration fits format": {"long": 61.5 <= dur <= 80, "short": 30 <= dur <= 50,
                             "ambient": 6 <= dur <= 15}[fmt],
}
report = {"file": out, "duration": round(dur, 2), "lufs": lufs, "peak": peak,
          "size_mb": round(int(probe["format"]["size"]) / 1e6, 1), "checks": checks}
print(json.dumps(report, indent=1))
sys.exit(0 if all(checks.values()) else 1)
