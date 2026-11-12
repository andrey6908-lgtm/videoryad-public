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
from okna import OKNO as _O, OKNO_LOK as _OL
# Вставка идёт НЕПРЕРЫВНЫМ отрезком: соседние планы с тем же клипом склеиваются
# в один показ. Раньше каждый план открывал окно заново — оно мигало каждые
# 6-8 секунд (его правка 12.11: «появилась она один раз, и держим её, пока не
# сменится другая»).
STOCK = []
for sc in SCENES:
    if not sc.get("stock"):
        continue
    x, y, w, h = _OL.get(sc.get("lok", "komnata"), _O)
    url = _ST[sc["stock"]]
    if (STOCK and sc.get("okno_cont") and STOCK[-1][2] == url
            and abs(STOCK[-1][1] - (sc["a"] - .2)) < .5):
        a0, _, u0, box = STOCK[-1]
        STOCK[-1] = (a0, sc["b"] - .2, u0, box)
    else:
        STOCK.append((sc["a"] + .8, sc["b"] - .2, url, (x, y, w, h)))

# ГЕЙТ (правило режиссёра R-0021, ужесточено 12.11.2026): один стоковый клип —
# РОВНО ОДИН раз на весь ролик. Взят однажды — второй раз ставить запрещено,
# ни подряд, ни после паузы. Сборка не идёт, пока повтор не убран.
_vzyato = {}
for _a, _b, _url, _box in STOCK:
    _vzyato.setdefault(_url, []).append(_a)
_povtor = {u: t for u, t in _vzyato.items() if len(t) > 1}
if _povtor:
    _s = "\n".join("   %s — %d раза, в секундах %s"
                    % (u.rsplit("/", 2)[1], len(t), ", ".join("%.1f" % x for x in t))
                    for u, t in _povtor.items())
    raise SystemExit("ПОВТОР СТОКА, сборка остановлена (R-0021):\n" + _s +
                     "\nКаждой сцене — СВОЙ клип. Правь scenes.json/stock.json.")


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
