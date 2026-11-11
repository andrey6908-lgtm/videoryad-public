# -*- coding: utf-8 -*-
"""Клип в окне вставки: качаем по прямой ссылке и разворачиваем в кадры ровно
под длительность плана. Кадр окна подставляется в SVG как картинка — так же,
как фотография, поэтому рамка, подписи и порядок слоёв не меняются.

Скачивает РАННЕР: в репозитории лежат только ссылки, видео туда не кладём.
"""
import json, os, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    " (KHTML, like Gecko) Chrome/125.0 Safari/537.36"}
OKNO_W, OKNO_H = 980, 551


def _skachat(url, path):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r, \
         open(path, "wb") as f:
        while True:
            b = r.read(1 << 18)
            if not b:
                break
            f.write(b)
    return os.path.getsize(path) > 50000


def razvernut(st, nado, out_dir, fps=25, log=print):
    """st — stock_video.json, nado — номера планов, которые нужны этому шарду."""
    os.makedirs(out_dir, exist_ok=True)
    gotovo = {}
    for n in sorted(nado):
        r = st.get(str(n))
        if not r:
            continue
        d = os.path.join(out_dir, "%03d" % n)
        if os.path.isdir(d) and os.listdir(d):
            gotovo[n] = d
            continue
        os.makedirs(d, exist_ok=True)
        mp4 = os.path.join(out_dir, "%03d.mp4" % n)
        try:
            if not os.path.exists(mp4):
                _skachat(r["url"], mp4)
        except Exception as e:
            log("клип %d не скачался: %r" % (n, e))
            continue
        # ровно под длительность плана, с запасом в полсекунды на кроссфейд
        dl = float(r.get("sek") or 8) + .6
        nach = float(r.get("start") or 0)
        vf = (f"scale={OKNO_W}:{OKNO_H}:force_original_aspect_ratio=increase,"
              f"crop={OKNO_W}:{OKNO_H},fps={fps}")
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{nach:.2f}", "-t", f"{dl:.2f}",
               "-i", mp4, "-vf", vf, "-q:v", "6", os.path.join(d, "%06d.jpg")]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode or not os.listdir(d):
            log("клип %d не развернулся: %s" % (n, p.stderr[-300:]))
            continue
        os.remove(mp4)
        gotovo[n] = d
        log("клип %d: %d кадров" % (n, len(os.listdir(d))))
    return gotovo


def kadr_klipa(dirs, n, t, fps=25):
    d = dirs.get(n)
    if not d:
        return None
    i = int(t * fps) + 1
    p = os.path.join(d, "%06d.jpg" % i)
    if os.path.exists(p) and os.path.getsize(p) > 1200:
        return p
    # клип короче плана — держим последний кадр, чёрной дыры в окне не будет
    try:
        poslednij = max(os.listdir(d))
    except Exception:
        return None
    return os.path.join(d, poslednij)
