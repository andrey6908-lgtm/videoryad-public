# -*- coding: utf-8 -*-
"""СБОРКА РАСКАДРОВКИ ИЗ СЛОВ. Его правило 07.11: «оно должно попадать в слова,
мы должны иллюстрировать речь». Поэтому планы и элементы не выставляются руками,
а считаются из words.json — слова чистой озвучки с таймингами.

    python3 build_scenes.py words.json scenes.json
"""
import json, sys, re

W = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "words.json", encoding="utf-8"))
OUT = sys.argv[2] if len(sys.argv) > 2 else "scenes.json"
TOTAL = 927.1


def when(*keys, after=0.0, before=1e9):
    for t, w in W:
        if after <= t < before and any(k in w for k in keys):
            return t
    return None


def every(*keys, after=0.0, before=1e9):
    return [t for t, w in W if after <= t < before and any(k in w for k in keys)]


# ── 1 · где про какую ёлку говорят: окно с генерацией живёт только здесь
T_VIN = when("винная", "винную", "винный")
T_EKO = when("природная", "природную", after=T_VIN + 30)
T_MET = when("металлик", after=T_EKO + 30)
T_VNT = when("винтаж", after=T_MET + 30)
T_ERR = when("пятая", after=T_VNT + 30) or when("ошибка", after=T_VNT + 30)
T_FIN = when("итак", "маршрут", after=T_ERR + 60) or 871.9
TEMY = [("vin", "foto/винная.jpg", T_VIN, T_EKO),
        ("eko", "foto/эко.jpg", T_EKO, T_MET),
        ("met", "foto/металик.jpg", T_MET, T_VNT),
        ("vnt", "foto/Винтажная_ёлка.jpg", T_VNT, T_ERR),
        ("err", "foto/ёлка_ошибка.jpg", T_ERR, T_FIN)]
PAL = {"vin": ["#7d1f2e", "#9c2740", "#c9922f"], "eko": ["#8a6b45", "#c9b58a", "#6d8a4a"],
       "met": ["#c9922f", "#d9cdb0", "#ffd36e"], "vnt": ["#9c2740", "#b9743f", "#e4d4b6"],
       "err": ["#d6202f", "#c9922f", "#7fd0ff", "#9ee07f", "#7d1f2e"],
       "none": ["#7d1f2e", "#c9922f", "#3f8a4a"]}
STOCK_NEUTRAL = ["svecha", "girlyanda", "igrushki", "stol", "sneg", "salut"]


def tema_at(t):
    for nm, foto, a, b in TEMY:
        if a is not None and a <= t < (b or TOTAL):
            return nm, foto
    return "none", None


# ── 2 · события: слово → что показать ровно в эту секунду
EV = []


def ev(t, kind, **kw):
    if t is not None:
        EV.append(dict(t=round(t, 2), kind=kind, **kw))


ev(0.6, "zagolovok")                                     # заголовок ролика справа
ev(when("пять", "пяти"), "cards5")                      # «покажу вам пять ёлок»
# хозяйка года появляется там, где о ней говорят, и только там
for t_ in every("хозяйк", "гостья", "гостью")[:6]:
    ev(t_, "goat")
for nm, foto, a, b in TEMY:
    if a is None:
        continue
    ev(a, "plate", tema=nm)
    b = b or TOTAL
    # палитра — на первом названии цвета внутри темы
    c0 = when("бордо", "хвойн", "золот", "гранат", "олив", "латун", after=a, before=b)
    ev(c0, "palitra", tema=nm)
    for key, pod, box in (("гирлянд", "гирлянда — первой", [1117, 750, 190, 90]),
                          ("шар", "крупный шар", [1082, 436, 84, 84]),
                          ("бант", "бархатный бант", [1143, 262, 96, 74]),
                          ("апельсин", "сушёный апельсин", [1210, 700, 66, 66]),
                          ("шишк", "шишка", [1090, 470, 84, 84]),
                          ("звезд", "звезда", [1130, 230, 92, 92]),
                          ("мишур", "мишура кольцами", [1180, 790, 230, 110])):
        t = when(key, after=a, before=b)
        if t:
            ev(t, "obvodka", tema=nm, pod=pod, box=box)
ev(when("ритуал", "обряд"), "ritual")
ev(when("мишура", after=760), "reveal")
ev(when("ошибк", after=700), "errors")
ev(when("комментар"), "cards4")
ev(when("подпис", "подписаться", "канал", after=TOTAL - 90), "final")
EV.sort(key=lambda e: e["t"])

# ── 3 · планы: 7-11 секунд, ракурс меняется
CAMS = [("push", 1.0, 1.14, .50, .52), ("pan", 1.08, 1.08, .34, .52),
        ("crane", 1.16, 1.0, .46, .70), ("arc", 1.06, 1.12, .62, .46),
        ("wide", 1.12, 1.0, .50, .50), ("tilt", 1.1, 1.02, .50, .66)]
S, t, i, k = [], 0.0, 0, 0
while t < TOTAL - 1:
    nxt_ev = next((e["t"] for e in EV if e["t"] > t + 3.5), None)
    dur = 9.0
    if nxt_ev and nxt_ev - t < 12.5:
        dur = max(5.5, nxt_ev - t)
    b = min(TOTAL, t + dur)
    tema, foto = tema_at(t + .1)
    cam = CAMS[k % len(CAMS)]
    sc = {"n": i + 1, "a": round(t, 2), "b": round(b, 2), "kind": "scene",
          "tema": tema, "cam": cam[0], "z0": cam[1], "z1": cam[2], "cx": cam[3], "cy": cam[4],
          "pal": PAL[tema], "events": [e for e in EV if t <= e["t"] < b]}
    if foto:
        sc["foto"] = foto
    else:
        sc["stock"] = STOCK_NEUTRAL[k % len(STOCK_NEUTRAL)]
    S.append(sc)
    t = b
    i += 1
    k += 1
json.dump(S, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("планов:", len(S), "· средний %.1f с" % (TOTAL / len(S)), "· событий:", len(EV))
print("темы: вин %.0f · эко %.0f · мет %.0f · винт %.0f · ошибка %.0f · финал %.0f"
      % (T_VIN, T_EKO, T_MET, T_VNT, T_ERR, T_FIN))
