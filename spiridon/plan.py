# -*- coding: utf-8 -*-
"""Раскадровка для рендера: планы из plany.json, тайминги — по озвучке.
SPIRIDON_PLANY="1-10" или "1,13,23" собирает пробник из выбранных планов."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 25
TRANS = 0.4                       # кроссфейд между планами (K31)
TAG = "spiridon"

_P = json.load(open(os.path.join(HERE, "plany.json"), encoding="utf-8"))


def _vybor():
    s = (os.environ.get("SPIRIDON_PLANY") or "").strip()
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
    """Кадр → (план, локальное время, доля плана), следующий план и смесь."""
    gt = i / FPS
    k = len(PLANY) - 1
    for j, p in enumerate(PLANY):
        if p["tab"] <= gt < p["tab"] + p["sek"]:
            k = j
            break
    p = PLANY[k]
    lt = gt - p["tab"]
    cur = (k, lt, min(1.0, lt / max(.001, p["sek"])))
    nxt, mix = None, 0.0
    kon = p["tab"] + p["sek"]
    if k + 1 < len(PLANY) and gt > kon - TRANS:
        mix = (gt - (kon - TRANS)) / TRANS
        p2 = PLANY[k + 1]
        lt2 = gt - (p2["tab"] - TRANS)
        nxt = (k + 1, lt2, min(1.0, max(0.0, lt2 / max(.001, p2["sek"]))))
    return cur, nxt, mix
