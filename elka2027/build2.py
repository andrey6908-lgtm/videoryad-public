# -*- coding: utf-8 -*-
"""Раскадровка ИЗ СЛОВ И СО СМЕНОЙ ДЕКОРАЦИЙ (его разбор 07.11).

Правила, зашитые здесь:
  · план 5-7 с в первые полминуты, дальше 7-10 с;
  · декорация меняется каждый план в завязке и не реже раза в 2 плана дальше;
  · окно вставки — НЕ интерьер: появляется только там, где показываем ёлку
    или нужное живое видео, и уходит, когда на экране наши карточки;
  · всё появляется в секунду, когда звучит слово.
"""
import json, sys

W = json.load(open("words.json", encoding="utf-8"))
TOTAL = 927.1
OUT = sys.argv[1] if len(sys.argv) > 1 else "scenes.json"


def when(*keys, after=0.0, before=1e9):
    for t, w in W:
        if after <= t < before and any(k in w for k in keys):
            return t
    return None


def every(*keys, after=0.0, before=1e9):
    return [t for t, w in W if after <= t < before and any(k in w for k in keys)]


T_VIN = when("винная", "винную")
T_EKO = when("природная", "природную", after=T_VIN + 30)
T_MET = when("металлик", after=T_EKO + 30)
T_VNT = when("винтаж", after=T_MET + 30)
T_ERR = when("пятая", after=T_VNT + 30)
T_FIN = when("итак", "маршрут", after=T_ERR + 60) or 871.9
TEMY = [("vin", "foto/винная.jpg", T_VIN, T_EKO), ("eko", "foto/эко.jpg", T_EKO, T_MET),
        ("met", "foto/металик.jpg", T_MET, T_VNT), ("vnt", "foto/Винтажная_ёлка.jpg", T_VNT, T_ERR),
        ("err", "foto/ёлка_ошибка.jpg", T_ERR, T_FIN)]
PAL = {"vin": ["#7d1f2e", "#9c2740", "#c9922f"], "eko": ["#8a6b45", "#c9b58a", "#6d8a4a"],
       "met": ["#c9922f", "#d9cdb0", "#ffd36e"], "vnt": ["#9c2740", "#b9743f", "#e4d4b6"],
       "err": ["#d6202f", "#7fd0ff", "#9ee07f", "#c9922f", "#b06ad6"],
       "none": ["#7d1f2e", "#c9922f", "#3f8a4a"]}

# очередь декораций: в завязке меняем каждый план
ZAVYAZKA = ["komnata", "kamin", "vetka", "dvor", "nebo", "stol", "les", "prihozhaya"]
PO_TEME = {"vin": ["komnata", "vetka", "stol", "kamin"],
           "eko": ["les", "vetka", "dvor", "masterskaya"],
           "met": ["komnata", "vetka", "kamin", "masterskaya"],
           "vnt": ["masterskaya", "prihozhaya", "komnata", "vetka"],
           "err": ["komnata", "vetka", "kamin", "nebo"],
           "none": ["komnata", "stol", "dvor", "nebo", "prihozhaya", "les"]}
NEUTRAL = ["svecha", "girlyanda", "igrushki", "stol", "sneg", "salut"]


def tema_at(t):
    for nm, foto, a, b in TEMY:
        if a is not None and a <= t < (b or TOTAL):
            return nm, foto
    return "none", None


EV = []


def ev(t, kind, **kw):
    if t is not None:
        EV.append(dict(t=round(t, 2), kind=kind, **kw))


ev(0.6, "zagolovok")
ev(when("пять", "пяти"), "cards5")
for t_ in every("хозяйк", "гостья", "гостью")[:5]:
    ev(t_, "goat")
for nm, foto, a, b in TEMY:
    if a is None:
        continue
    b = b or TOTAL
    ev(a, "plate", tema=nm)
    ev(when("бордо", "хвойн", "золот", "гранат", "олив", "латун", after=a, before=b), "palitra", tema=nm)
    for key, pod, box in (("гирлянд", "гирлянда — первой", [1117, 750, 190, 90]),
                          ("шар", "крупный шар", [1082, 436, 84, 84]),
                          ("бант", "бархатный бант", [1143, 262, 96, 74]),
                          ("апельсин", "сушёный апельсин", [1210, 700, 66, 66]),
                          ("шишк", "шишка", [1090, 470, 84, 84]),
                          ("мишур", "мишура кольцами", [1180, 790, 230, 110])):
        ev(when(key, after=a, before=b), "obvodka", tema=nm, pod=pod, box=box)
ev(when("ритуал", "обряд"), "ritual")
ev(when("мишура", after=760), "reveal")
ev(when("ошибк", after=700), "errors")
ev(when("комментар"), "cards4")
ev(when("подпис", "подписаться", after=TOTAL - 90), "final")
EV.sort(key=lambda e: e["t"])
BLOK = {"cards5", "cards4", "errors", "ritual", "reveal", "zagolovok"}

CAMS = [("push", 1.0, 1.16), ("pan", 1.1, 1.1), ("crane", 1.18, 1.0), ("arc", 1.06, 1.14),
        ("wide", 1.14, 1.0), ("tilt", 1.12, 1.02)]
S, t, i, k = [], 0.0, 0, 0
while t < TOTAL - 1:
    zav = t < 32
    dur = 5.5 if zav else (7.5 if t < 90 else 9.0)
    nxt = next((e["t"] for e in EV if e["t"] > t + 2.5), None)
    if nxt and nxt - t < dur + 3:
        dur = max(4.0, nxt - t)
    b = min(TOTAL, t + dur)
    tema, foto = tema_at(t + .1)
    lokl = ZAVYAZKA[i % len(ZAVYAZKA)] if zav else PO_TEME[tema][(i // 2) % len(PO_TEME[tema])]
    cam = CAMS[k % len(CAMS)]
    evs = [e for e in EV if t <= e["t"] < b]
    blok = any(e["kind"] in BLOK for e in evs)
    sc = {"n": i + 1, "a": round(t, 2), "b": round(b, 2), "lok": lokl, "tema": tema,
          "cam": cam[0], "z0": cam[1], "z1": cam[2], "pal": PAL[tema], "events": evs}
    # окно показываем, когда есть что показать и экран не занят нашим блоком
    if not blok:
        if foto and tema != "none":
            sc["foto"] = foto
        elif i % 3 == 0:
            sc["stock"] = NEUTRAL[k % len(NEUTRAL)]
    S.append(sc)
    t = b; i += 1; k += 1
json.dump(S, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
okna = sum(1 for s in S if s.get("foto") or s.get("stock"))
print("планов:", len(S), "· средний %.1f с" % (TOTAL / len(S)), "· с окном:", okna,
      "· декораций в ротации:", len(set(s["lok"] for s in S)))
