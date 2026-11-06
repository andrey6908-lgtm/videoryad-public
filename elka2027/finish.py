# -*- coding: utf-8 -*-
"""Склейка частей и живые вставки: настоящее видео в окне внутри рисунка.
Клипы качает сам раннер по прямым публичным ссылкам."""
import os, sys, json, subprocess, urllib.request
import plan

SEG, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
segs = sorted(os.path.join(SEG, f) for f in os.listdir(SEG)
              if f.startswith("seg") and f.endswith(".mp4"))
print("частей:", len(segs))
assert segs, "нет ни одной части"
with open("/tmp/list.txt", "w") as f:
    for p in segs:
        f.write("file '%s'\n" % os.path.abspath(p))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd[:10]), "\n", r.stderr[-2500:]); raise SystemExit(1)


run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "/tmp/list.txt",
     "-c", "copy", "/tmp/base.mp4"])

files = {}
for aa, bb, url, box in plan.STOCK:
    if url in files:
        continue
    dst = "/tmp/sv%d.mp4" % len(files)
    for att in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(dst, "wb") as f:
                f.write(r.read())
            break
        except Exception as e:
            print("   вставка не скачалась, попытка %d: %s" % (att + 1, e))
    if not os.path.exists(dst) or os.path.getsize(dst) < 80000:
        raise SystemExit("вставка не скачалась: " + url)
    files[url] = dst
    print("   вставка %s → %d КБ" % (url[-26:], os.path.getsize(dst) // 1024))

CUR = "/tmp/base.mp4"
FINAL = os.path.join(OUT, "elka2027_nemoe.mp4")
if plan.STOCK:
    inputs = ["-i", CUR]
    fc, cur, n = [], "0:v", 1
    for i, (aa, bb, url, box) in enumerate(plan.STOCK):
        x, y, w, h = box
        d = bb - aa
        inputs += ["-itsoffset", "%.3f" % aa, "-stream_loop", "-1", "-t", "%.3f" % d,
                   "-i", files[url]]
        fc.append("[%d:v]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
                  "setsar=1,fps=%d,format=rgba,fade=in:st=%.3f:d=0.3:alpha=1,"
                  "fade=out:st=%.3f:d=0.4:alpha=1[sv%d]"
                  % (n, w, h, w, h, plan.FPS, aa, max(aa, bb - .4), i))
        fc.append("[%s][sv%d]overlay=%d:%d:eof_action=pass:enable='between(t,%.3f,%.3f)'[v%d]"
                  % (cur, i, x, y, aa, bb, i))
        cur = "v%d" % i
        n += 1
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(fc),
        "-map", "[%s]" % cur, "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-r", str(plan.FPS), "-movflags", "+faststart", FINAL])
else:
    run(["ffmpeg", "-v", "error", "-y", "-i", CUR, "-c", "copy", FINAL])

dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", FINAL], capture_output=True, text=True).stdout.strip()
print("ГОТОВО:", FINAL, os.path.getsize(FINAL) // 1024, "КБ,", dur, "с")
json.dump({"file": os.path.basename(FINAL), "seconds": float(dur), "frames": plan.NFRAMES,
           "scenes": len(plan.SCENES), "stock": len(plan.STOCK)},
          open(os.path.join(OUT, "report.json"), "w"), ensure_ascii=False, indent=1)
