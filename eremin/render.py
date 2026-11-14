# -*- coding: utf-8 -*-
"""Покадровый рендер. Каждый кадр — рисованная сцена со слоями по глубине под
ход камеры, поверх надписи. Звука здесь нет, он подмешивается на его машине."""
import os, sys, io, json, subprocess, argparse, time
import cairosvg
from PIL import Image
import kadr, baza, plan, klipy

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--shard", default="1/1")
ap.add_argument("--shir", type=int, default=1920)
a = ap.parse_args()
si, sn = (int(x) for x in a.shard.split("/"))
os.makedirs(a.out, exist_ok=True)
TMP = os.path.join(a.out, "f%02d" % si)
os.makedirs(TMP, exist_ok=True)
H = int(a.shir * baza.H / baza.W)


def risuy(j, t, p):
    svg = kadr.body(plan.PLANY[j], t, p, zaglushki=False)
    buf = io.BytesIO()
    # unsafe=True нужен, чтобы в окно встал настоящий кадр: без него
    # cairosvg молча рисует пустое окно (поймано на сведении 11.11)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf,
                     output_width=a.shir, output_height=H, unsafe=True)
    return Image.open(buf).convert("RGB")


N = plan.NFRAMES
lo, hi = (N * (si - 1)) // sn, (N * si) // sn
print("часть %d/%d: кадры %d..%d из %d" % (si, sn, lo, hi - 1, N), flush=True)

# клипы в окна: качаем и разворачиваем ТОЛЬКО те планы, что попали в эту часть
SV = {}
_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_video.json")
if os.path.exists(_f):
    SV = json.load(open(_f, encoding="utf-8"))
if SV:
    nado = set()
    for i in range(lo, hi):
        (k, _, _), nxt, _ = plan.frame_info(i)
        nado.add(plan.PLANY[k]["n"])
        if nxt:
            nado.add(plan.PLANY[nxt[0]]["n"])
    t0k = time.time()
    kadr.KLIPY = klipy.razvernut(SV, nado, os.path.join(a.out, "klipy%02d" % si), plan.FPS)
    print("клипов развёрнуто: %d за %.0f с" % (len(kadr.KLIPY), time.time() - t0k), flush=True)
t0 = time.time()
for i in range(lo, hi):
    cur, nxt, mix = plan.frame_info(i)
    im = risuy(*cur)
    if nxt is not None and mix > 0.001:
        im = Image.blend(im, risuy(*nxt), min(1.0, mix))
    im.save("%s/f%06d.png" % (TMP, i), compress_level=1)
    if (i - lo) % 100 == 0 and i > lo:
        done = i - lo
        sp = done / max(.001, time.time() - t0)
        print("   %d/%d  %.1f кадр/с  осталось %.0f с"
              % (done, hi - lo, sp, (hi - lo - done) / sp), flush=True)

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
