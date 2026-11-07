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
import art3 as _A
STOCK = []
for sc in SCENES:
    # нейтральный новогодний сток — только там, где окно есть и экран не занят
    if sc.get("stock"):
        x, y, w, h = _A.OKNO_LOK.get(sc.get("lok", "komnata"), _A.OKNO)
        STOCK.append((sc["a"] + .8, sc["b"] - .2, _ST[sc["stock"]], (x, y, w, h)))


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
