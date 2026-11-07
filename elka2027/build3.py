# -*- coding: utf-8 -*-
"""Раскадровка версии 3: СМЫСЛОВЫЕ ОТРЕЗКИ вместо точек и механической ротации.

Что чинит (его разбор 07.11, правки 26-32):
  26 · в окне всегда то, о чём говорят прямо сейчас;
  27-28 · элементы живут ОТРЕЗКАМИ и не моргают на стыках планов;
  30 · один клип — один раз;
  31 · декорация выбирается по смыслу речи, а не по очереди;
  32 · окно большое.
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


# ── 1 · смысловые отрезки: что показываем и где происходит
T_VIN = when("винная", "винную")
T_EKO = when("природная", "природную", after=T_VIN + 30)
T_MET = when("металлик", after=T_EKO + 30)
T_VNT = when("винтаж", after=T_MET + 30)
T_ERR = when("пятая", after=T_VNT + 30)
T_FIN = when("итак", "маршрут", after=T_ERR + 60) or 871.9

SEG = []        # (начало, конец, локация, что в окне, тема, нужна ли коза)


def seg(a, b, lok, okno=None, tema="none", koza=False):
    if a is None or b is None or b <= a:
        return
    SEG.append({"a": round(a, 2), "b": round(b, 2), "lok": lok, "okno": okno,
                "tema": tema, "koza": koza})


# завязка: про вещь на ёлке и пять ёлок
t_pyat = when("пять", "пяти")
seg(0, 26, "komnata", "clip:igrushki")
seg(26, t_pyat - 1, "vetka", "clip:elka")
seg(t_pyat - 1, 57, "komnata", None)                    # карточки пяти ёлок, окно не нужно
# хозяйка года: открытка → загон → скалы → уступ → деревья Марокко → глаз
t_zagon = when("загоне", "жуёт", "жует", after=57) or 70
t_skaly = when("скал", "отвесн", after=t_zagon) or 80
t_ustup = when("уступ", "уступах", after=t_skaly) or (t_skaly + 14)
t_derevo = when("марокко", "деревь", after=t_ustup) or (t_ustup + 12)
t_glaz = when("глаз", "видит", after=t_derevo) or (t_derevo + 14)
seg(57, t_zagon, "komnata", None, koza=True)            # открытка и «забудьте картинку»
seg(t_zagon, t_skaly, "les", "clip:koza_zagon", koza=True)
seg(t_skaly, t_ustup, "nebo", "clip:koza_skaly")
seg(t_ustup, t_derevo, "nebo", "clip:koza_ustup")
seg(t_derevo, t_glaz, "dvor", "foto:foto/kozy_derevo1_br.jpg|foto/kozy_derevo2_br.jpg")
seg(t_glaz, t_glaz + 22, "komnata", None)               # крупный глаз во весь кадр
# дорога к ёлке: про дверь, стол, подарки и саму ёлку
t_dver = when("дверь", "порог", "входит", after=t_glaz + 20)
t_elka = when("ёлке", "елке", "ёлку", "елку", after=(t_dver or t_glaz) + 4)
seg(t_glaz + 22, t_dver or (T_VIN - 20), "prihozhaya", "clip:svecha", koza=True)
seg(t_dver, t_elka, "stol", "clip:stol", koza=True)
seg(t_elka, T_VIN, "komnata", "clip:girlyanda", koza=True)
# пять ёлок по очереди: своя тема, своя декорация
for tema, a, b in (("vin", T_VIN, T_EKO), ("eko", T_EKO, T_MET), ("met", T_MET, T_VNT),
                   ("vnt", T_VNT, T_ERR), ("err", T_ERR, T_FIN)):
    foto = {"vin": "foto/винная_br.jpg", "eko": "foto/эко_br.jpg",
            "met": "foto/металик_br.jpg", "vnt": "foto/Винтажная_ёлка_br.jpg",
            "err": "foto/ёлка_ошибка_br.jpg"}[tema]
    lok = {"vin": "komnata", "eko": "les", "met": "kamin", "vnt": "masterskaya",
           "err": "komnata"}[tema]
    seg(a, b, lok, "foto:" + foto, tema)
seg(T_FIN, TOTAL, "komnata", None, "none", koza=True)

# ── 2 · элементы: ОТРЕЗКАМИ, с абсолютным временем
EL = []


def el(a, b, kind, **kw):
    if a is None:
        return
    EL.append(dict(a=round(a, 2), b=round(min(b, TOTAL), 2), kind=kind, **kw))


el(0.6, 14, "zagolovok")
el(t_pyat - .4, t_pyat + 14, "cards5")
el(t_glaz, t_glaz + 20, "glaz")
for tema, a, b in (("vin", T_VIN, T_EKO), ("eko", T_EKO, T_MET), ("met", T_MET, T_VNT),
                   ("vnt", T_VNT, T_ERR), ("err", T_ERR, T_FIN)):
    el(a, a + 9, "plate", tema=tema)
    c0 = when("бордо", "хвойн", "золот", "гранат", "олив", "латун", after=a, before=b)
    el(c0, (c0 or a) + 12, "palitra", tema=tema)
    for key, pod, box in (("гирлянд", "гирлянда — первой", [1117, 750, 190, 90]),
                          ("шар", "крупный шар", [1082, 436, 84, 84]),
                          ("бант", "бархатный бант", [1143, 262, 96, 74]),
                          ("шишк", "шишка", [1090, 470, 84, 84]),
                          ("мишур", "мишура кольцами", [1180, 790, 230, 110])):
        t0 = when(key, after=a, before=b)
        el(t0, (t0 or a) + 8, "obvodka", tema=tema, pod=pod, box=box)
t_rit = when("ритуал", "обряд")
el(t_rit, (t_rit or 0) + 16, "ritual")
t_rev = when("мишура", after=760)
el(t_rev, (t_rev or 0) + 10, "reveal")
t_err = when("ошибк", after=700)
el(t_err, (t_err or 0) + 12, "errors")
t_com = when("комментар")
el(t_com, (t_com or 0) + 14, "cards4")
t_sub = when("подпис", "подписаться", after=TOTAL - 90)
el(t_sub, TOTAL, "final")
BLOK = {"cards5", "cards4", "errors", "ritual", "reveal", "glaz"}

# ── 3 · планы внутри отрезков: ракурс меняется, декорация держится
CAMS = [("push", 1.0, 1.16), ("pan", 1.1, 1.1), ("crane", 1.18, 1.0),
        ("arc", 1.06, 1.14), ("wide", 1.14, 1.0), ("tilt", 1.12, 1.02)]
S, k = [], 0
for sg in SEG:
    t = sg["a"]
    while t < sg["b"] - .4:
        zav = t < 32
        dur = min(6.0 if zav else 8.5, sg["b"] - t)
        if sg["b"] - (t + dur) < 2.5:
            dur = sg["b"] - t
        b = t + dur
        evs = [e for e in EL if e["a"] < b and e["b"] > t]
        blok = any(e["kind"] in BLOK for e in evs)
        cam = CAMS[k % len(CAMS)]
        sc = {"n": len(S) + 1, "a": round(t, 2), "b": round(b, 2), "lok": sg["lok"],
              "tema": sg["tema"], "cam": cam[0], "z0": cam[1], "z1": cam[2],
              "koza": sg["koza"], "events": evs}
        ok = sg["okno"]
        if ok and not blok:
            if ok.startswith("clip:"):
                sc["stock"] = ok[5:]
            else:
                parts = ok[5:].split("|")
                sc["foto"] = parts[0]
                if len(parts) > 1:
                    sc["foto2"] = parts[1]
        S.append(sc)
        t = b
        k += 1
json.dump(S, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("отрезков:", len(SEG), "· планов:", len(S), "· средний %.1f с" % (TOTAL / len(S)),
      "· элементов:", len(EL))
print("окно: фото", sum(1 for s in S if s.get("foto")), "· клип",
      sum(1 for s in S if s.get("stock")), "· пусто",
      sum(1 for s in S if not s.get("foto") and not s.get("stock")))
