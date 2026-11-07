# -*- coding: utf-8 -*-
"""Раскадровка «Ёлка 2027»: сцены из scenes.json, тайминги — с ЧИСТОЙ озвучки
(служебные заголовки вырезаны montazh.py). Звук в облако не едет."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 25
TRANS = 0.4                      # перекрытие между сценами
TAG = "elka2027"

SCENES = json.load(open(os.path.join(HERE, "scenes.json"), encoding="utf-8"))
TOTAL = SCENES[-1]["b"]
NFRAMES = int(round(TOTAL * FPS))

# живые вставки: качает раннер по прямой ссылке, ключей в облаке нет
_ST = json.load(open(os.path.join(HERE, "stock.json"), encoding="utf-8"))
import scena as _SC
STOCK = []
for sc in SCENES:
    # нейтральный новогодний сток живёт в окне, пока не говорят о конкретной ёлке
    if sc.get("stock"):
        ox, oy, ow, oh = _SC.OKNO
        z0 = sc.get("z0", 1.0); z1 = sc.get("z1", 1.1)
        z = (z0 + z1) / 2
        cx, cy = sc.get("cx", .5), sc.get("cy", .5)
        vw, vh = 1920 / z, 1080 / z
        vx = min(max(0.0, cx * 1920 - vw / 2), 1920 - vw)
        vy = min(max(0.0, cy * 1080 - vh / 2), 1080 - vh)
        kx, ky = 1920 / vw, 1080 / vh
        x = int((ox - vx) * kx); y = int((oy - vy) * ky)
        w = int(ow * kx); h = int(oh * ky)
        if x > -w and y > -h and x < 1920 and y < 1080:
            STOCK.append((sc["a"] + .75, sc["b"] - .25, _ST[sc["stock"]],
                          (max(0, x), max(0, y), max(16, w), max(16, h))))


def frame_info(i):
    """Кадр → (сцена, локальное время), сцена перехода и доля смеси."""
    gt = i / FPS
    k = 0
    for j, sc in enumerate(SCENES):
        if sc["a"] <= gt < sc["b"]:
            k = j
            break
    else:
        k = len(SCENES) - 1
    sc = SCENES[k]
    cur = (k, gt - sc["a"])
    nxt, mix = None, 0.0
    if k + 1 < len(SCENES) and gt > sc["b"] - TRANS:
        mix = (gt - (sc["b"] - TRANS)) / TRANS
        nxt = (k + 1, gt - (SCENES[k + 1]["a"] - TRANS))
    return cur, nxt, mix
