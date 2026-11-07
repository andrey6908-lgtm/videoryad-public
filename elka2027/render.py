# -*- coding: utf-8 -*-
"""Покадровый рендер «Ёлки 2027». Каждый кадр собирается заново: фото с
движением камеры или рисованная сцена, поверх — наложения. Звука здесь нет."""
import os, sys, subprocess, argparse, time
from PIL import Image
import art2 as art, plan

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--shard", default="1/1")
a = ap.parse_args()
si, sn = (int(x) for x in a.shard.split("/"))
os.makedirs(a.out, exist_ok=True)
TMP = os.path.join(a.out, "f%02d" % si)
os.makedirs(TMP, exist_ok=True)

N = plan.NFRAMES
lo, hi = (N * (si - 1)) // sn, (N * si) // sn
print("часть %d/%d: кадры %d..%d из %d" % (si, sn, lo, hi - 1, N), flush=True)

t0 = time.time()
for i in range(lo, hi):
    cur, nxt, mix = plan.frame_info(i)
    gt = i / plan.FPS
    k, lt = cur
    im = art.frame(plan.SCENES[k], lt, gt)
    if nxt is not None and mix > 0.001:
        k2, lt2 = nxt
        im = Image.blend(im, art.frame(plan.SCENES[k2], lt2, gt), min(1.0, mix))
    im.save("%s/f%06d.png" % (TMP, i), compress_level=1)
    if (i - lo) % 100 == 0:
        done = i - lo + 1
        sp = done / max(.001, time.time() - t0)
        print("   %d/%d  %.1f кадр/с  осталось %.0f с" % (done, hi - lo, sp, (hi - lo - done) / sp),
              flush=True)

seg = os.path.join(a.out, "seg%02d.mp4" % si)
r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(plan.FPS),
                    "-start_number", str(lo), "-i", "%s/f%%06d.png" % TMP,
                    "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", "-r", str(plan.FPS), seg],
                   capture_output=True, text=True)
if r.returncode:
    print(r.stderr[-3000:]); raise SystemExit(1)
print("часть %d готова: %d КБ, %.0f с" % (si, os.path.getsize(seg) // 1024, time.time() - t0))
for f in os.listdir(TMP):
    os.remove(os.path.join(TMP, f))
os.rmdir(TMP)
