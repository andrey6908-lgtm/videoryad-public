# -*- coding: utf-8 -*-
"""Покадровый рендер «Год козы 2027». Каждый кадр рисуется вектором заново:
зум идёт окном просмотра (без ступенек), внутри кадра всё живёт.
Звука здесь нет и не будет — озвучка в облако не уезжает."""
import os, sys, io, subprocess, argparse, time
import cairosvg
from PIL import Image
import art, plan

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--shard", default="1/1")
a = ap.parse_args()
si, sn = (int(x) for x in a.shard.split("/"))
os.makedirs(a.out, exist_ok=True)
TMP = os.path.join(a.out, "f%02d" % si)
os.makedirs(TMP, exist_ok=True)

N = plan.NFRAMES
lo = (N * (si - 1)) // sn
hi = (N * si) // sn
print("часть %d/%d: кадры %d..%d (всего %d)" % (si, sn, lo, hi - 1, N), flush=True)

OW, OH = 1920, 1080


def png(name, t, gt, z, cx, cy):
    return cairosvg.svg2png(bytestring=art.svg(name, t, gt, z, cx, cy, (OW, OH)).encode("utf-8"),
                            output_width=OW, output_height=OH)


t0 = time.time()
for i in range(lo, hi):
    cur, nxt, mix = plan.frame_info(i)
    gt = i / plan.FPS
    nm, lt, z, cx, cy = cur
    buf = png(nm, lt, gt, z, cx, cy)
    if nxt is not None and mix > 0.001:
        nm2, lt2, z2, cx2, cy2 = nxt
        b2 = png(nm2, lt2, gt, z2, cx2, cy2)
        im = Image.blend(Image.open(io.BytesIO(buf)).convert("RGB"),
                         Image.open(io.BytesIO(b2)).convert("RGB"), mix)
        im.save("%s/f%05d.png" % (TMP, i), compress_level=1)
    else:
        with open("%s/f%05d.png" % (TMP, i), "wb") as f:
            f.write(buf)
    if (i - lo) % 60 == 0:
        done = i - lo + 1
        sp = done / max(0.001, time.time() - t0)
        print("   кадр %d/%d  %.1f кадр/с  осталось %.0f с" % (done, hi - lo, sp, (hi - lo - done) / sp), flush=True)

seg = os.path.join(a.out, "seg%02d.mp4" % si)
r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(plan.FPS),
                    "-start_number", str(lo), "-i", "%s/f%%05d.png" % TMP,
                    "-c:v", "libx264", "-crf", "15", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", "-r", str(plan.FPS), seg],
                   capture_output=True, text=True)
if r.returncode:
    print(r.stderr[-3000:]); raise SystemExit(1)
nf = len(os.listdir(TMP))
print("часть %d готова: %d кадров, %d КБ, %.0f с" % (si, nf, os.path.getsize(seg) // 1024, time.time() - t0))
for f in os.listdir(TMP):
    os.remove(os.path.join(TMP, f))
os.rmdir(TMP)
