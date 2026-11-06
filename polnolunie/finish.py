# -*- coding: utf-8 -*-
"""Склейка частей пробника. Наложений отдельным проходом НЕТ — весь текст
уже нарисован в кадрах, поэтому склейка идёт копией, без перекодирования."""
import os, sys, json, subprocess
import plan

SEG, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
segs = sorted(os.path.join(SEG, f) for f in os.listdir(SEG)
              if f.startswith("seg") and f.endswith(".mp4"))
print("частей найдено:", len(segs))
assert segs, "нет ни одной части"

with open("/tmp/list.txt", "w") as f:
    for p in segs:
        f.write("file '%s'\n" % os.path.abspath(p))

FINAL = os.path.join(OUT, "polnolunie_%s_nemoe.mp4" % plan.TAG)
r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", "/tmp/list.txt", "-c:v", "libx264", "-crf", "19",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(plan.FPS),
                    "-movflags", "+faststart", FINAL], capture_output=True, text=True)
if r.returncode:
    print(r.stderr[-3000:]); raise SystemExit(1)

dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", FINAL], capture_output=True, text=True).stdout.strip()
print("ГОТОВО:", FINAL, os.path.getsize(FINAL) // 1024, "КБ,", dur, "с")
json.dump({"file": os.path.basename(FINAL), "seconds": float(dur),
           "frames": plan.NFRAMES, "fps": plan.FPS, "shots": len(plan.SHOTS),
           "scenes": sorted(set(s[2] for s in plan.SHOTS)), "effects": plan.EFFECTS},
          open(os.path.join(OUT, "report.json"), "w"), ensure_ascii=False, indent=1)
