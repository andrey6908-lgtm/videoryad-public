# -*- coding: utf-8 -*-
"""Раскадровка для рендера: планы из plany.json, тайминги — по озвучке.
KUZMINKI_PLANY="1-10" или "1,13,23" собирает пробник из выбранных планов."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 25
TRANS = 0.4                       # кроссфейд между планами (K31)
TAG = "kuzminki"

_P = json.load(open(os.path.join(HERE, "plany.json"), encoding="utf-8"))


def _vybor():
    s = (os.environ.get("KUZMINKI_PLANY") or "").strip()
    if not s:
        return _P
    nado = set()
    for k in s.split(","):
        k = k.strip()
        if "-" in k:
            a, b = k.split("-")
            nado |= set(range(int(a), int(b) + 1))
        elif k:
            nado.add(int(k))
    vyb = [p for p in _P if p["n"] in nado]
    t = 0.0
    out = []
    for p in vyb:                 # пробник идёт подряд, без дыр
        q = dict(p); q["tab"] = t; t += p["sek"]
        out.append(q)
    return out


PLANY = _vybor()
TOTAL = PLANY[-1]["tab"] + PLANY[-1]["sek"]
NFRAMES = int(round(TOTAL * FPS))


def frame_info(i):
    """Кадр → (план, локальное время, доля плана), партнёр по смеси и вес.

    R-0027: граница планов стоит В ЦЕНТРЕ паузы, поэтому и переход кладём
    СИММЕТРИЧНО вокруг границы — половина до неё, половина после. Иначе вся
    смена картинки успевает пройти до того, как пауза началась, и пауза
    остаётся «внутри плана», на что он и показал 11.11.
    """
    gt = i / FPS
    k = len(PLANY) - 1
    for j, p in enumerate(PLANY):
        if p["tab"] <= gt < p["tab"] + p["sek"]:
            k = j
            break
    p = PLANY[k]
    lt = gt - p["tab"]
    cur = (k, lt, min(1.0, lt / max(.001, p["sek"])))
    kon = p["tab"] + p["sek"]
    pol = TRANS / 2.0
    nxt, mix = None, 0.0
    if k + 1 < len(PLANY) and gt > kon - pol:          # уходим в следующий
        mix = (gt - (kon - pol)) / TRANS
        p2 = PLANY[k + 1]
        lt2 = max(0.0, gt - p2["tab"])
        nxt = (k + 1, lt2, min(1.0, lt2 / max(.001, p2["sek"])))
    elif k > 0 and lt < pol:                           # досматриваем предыдущий
        p0 = PLANY[k - 1]
        lt0 = gt - p0["tab"]
        nxt = (k - 1, lt0, min(1.0, lt0 / max(.001, p0["sek"])))
        mix = .5 - lt / TRANS                          # 0.5 на стыке → 0 через TRANS/2
    return cur, nxt, max(0.0, min(1.0, mix))
