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
STOCK = []
for sc in SCENES:
    if sc["kind"] == "live":
        STOCK.append((sc["a"] + .3, sc["b"] - .3, _ST[sc["clip"]], (260, 180, 1400, 790)))
    elif sc.get("live_win"):
        x, y, w, h = sc.get("win_box", [1180, 150, 640, 360])
        STOCK.append((sc["a"] + .5, sc["b"] - .5, _ST[sc["live_win"]], (x, y, w, h)))


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
