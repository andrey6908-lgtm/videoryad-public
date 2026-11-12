# -*- coding: utf-8 -*-
"""Раскадровка версии 4 — после его разбора 12.11.2026.

Что чинит (правила режиссёра R-0021, R-0023, R-0038..R-0043):
  · окно вставки больше НЕ МИГАЕТ: появилось один раз и держится, пока не
    сменится другим клипом (в каждом плане отрезка — okno_cont);
  · один клип — один раз, и живёт он подотрезком ~22 с, а не одним планом;
  · пустая половина кадра заполняется вторым персонажем (Дед Мороз, снеговик);
  · ключевые слова речи выскакивают надписями-акцентами со значком;
  · перечисление «первое, второе, третье» идёт нашими плашками-пунктами;
  · «космонавт, птица, часы» — рисованные игрушки крупно;
  · на «она пройдёт» коза идёт передним планом у рамки.
"""
import json, sys

W = json.load(open("words.json", encoding="utf-8"))
SRT = json.load(open("srt.json", encoding="utf-8"))
TOTAL = 927.1
OUT = sys.argv[1] if len(sys.argv) > 1 else "scenes.json"


def when(*keys, after=0.0, before=1e9):
    for t, w in W:
        if after <= t < before and any(k in w for k in keys):
            return t
    return None


def when_srt(sub, after=0.0, before=1e9):
    """Точное время реплики по куску текста — надёжнее пословной карты."""
    for a, b, t in SRT:
        if after <= a < before and sub.lower() in t.lower():
            return a
    return None


# ── 1 · смысловые отрезки
T_VIN = when("винная", "винную")
T_EKO = when("природная", "природную", after=T_VIN + 30)
T_MET = when("металлик", after=T_EKO + 30)
T_VNT = when("винтаж", after=T_MET + 30)
T_ERR = when("пятая", after=T_VNT + 30)
T_FIN = when("итак", "маршрут", after=T_ERR + 60) or 871.9

SEG = []


def seg(a, b, lok, okno=None, tema="none", koza=False, sprava=None):
    if a is None or b is None or b <= a:
        return
    SEG.append({"a": round(a, 2), "b": round(b, 2), "lok": lok, "okno": okno,
                "tema": tema, "koza": koza, "sprava": sprava})


t_pyat = when("пять", "пяти")
seg(0, 26, "komnata", "clip:igrushki|naryazhaet")
seg(26, t_pyat - 1, "vetka", "clip:elka|ogni_elka")
seg(t_pyat - 1, 57, "komnata", None)                      # карточки пяти ёлок
t_zagon = when("загоне", "жуёт", "жует", after=57) or 70
t_skaly = when("скал", "отвесн", after=t_zagon) or 80
t_ustup = when("уступ", "уступах", after=t_skaly) or (t_skaly + 14)
t_derevo = when("марокко", "деревь", after=t_ustup) or (t_ustup + 12)
t_glaz = when("глаз", "видит", after=t_derevo) or (t_derevo + 14)
# 0:57-1:10 — открытка и «забудьте картинку»: окна нет, правая половина
# заполняется Дедом Морозом (его правка 12.11 по 1:01)
seg(57, t_zagon, "komnata", None, koza=True, sprava="moroz")
seg(t_zagon, t_skaly, "les", "clip:koza_zagon|koza_kormushka", koza=True)
seg(t_skaly, t_derevo, "nebo", "clip:koza_skaly|koza_ustup")
seg(t_derevo, t_glaz, "dvor", "foto:foto/kozy_derevo1_br.jpg|foto/kozy_derevo2_br.jpg")
seg(t_glaz, t_glaz + 22, "komnata", None)                 # крупный глаз
t_dver = when("дверь", "порог", "входит", after=t_glaz + 20)
t_elka = when("ёлке", "елке", "ёлку", "елку", after=(t_dver or t_glaz) + 4)
seg(t_glaz + 22, t_dver or (T_VIN - 20), "prihozhaya", "clip:svecha", koza=True)
seg(t_dver, t_elka, "stol", "clip:stol|dom_ogni", koza=True)
seg(t_elka, T_VIN, "komnata", "clip:girlyanda|vetka_girlyanda", koza=True)
for tema, a, b in (("vin", T_VIN, T_EKO), ("eko", T_EKO, T_MET), ("met", T_MET, T_VNT),
                   ("vnt", T_VNT, T_ERR), ("err", T_ERR, T_FIN)):
    foto = {"vin": "foto/винная_br.jpg", "eko": "foto/эко_br.jpg",
            "met": "foto/металик_br.jpg", "vnt": "foto/Винтажная_ёлка_br.jpg",
            "err": "foto/ёлка_ошибка_br.jpg"}[tema]
    lok = {"vin": "komnata", "eko": "les", "met": "kamin", "vnt": "masterskaya",
           "err": "komnata"}[tema]
    klip = {"vin": "elka_shary", "eko": "vetka_girlyanda", "met": "ogni_elka",
            "vnt": "naryad_ruka", "err": "naryazhaet"}[tema]
    seg(a, b, lok, "foto:" + foto + "|clip:" + klip, tema)
# финал: окна нет — правая половина с Дедом Морозом и снеговиком
seg(T_FIN, TOTAL, "komnata", None, "none", koza=True, sprava="moroz")

# ── 2 · элементы отрезками
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

# ── 2-бис · НОВОЕ 12.11: слова-акценты, игрушки, плашки-пункты
SLOVA = [("Потом банты", "БАНТЫ", "bant"),
         ("сушёные дольки апельсина", "АПЕЛЬСИНЫ", "apelsin"),
         ("про деньги", "ДЕНЬГИ", "dengi"),
         ("Шишки. Деревянные", "ШИШКИ", "shishka"),
         ("Дольки апельсина", "АПЕЛЬСИНЫ", "apelsin"),
         ("банты. Всё", "ТРИ ЦВЕТА", "shar"),
         ("с облупившейся краской", "СТАРЫЕ ИГРУШКИ", "chasy"),
         ("Мишура. Вот она", "МИШУРА", "mishura")]
_last = -99
for sub, word, icon in SLOVA:
    t0 = when_srt(sub)
    if t0 is None or t0 - _last < 22:
        continue
    el(t0 + .15, t0 + 3.4, "slovo", text=word, icon=icon, x=430, y=268, size=62)
    _last = t0

t_vint = when_srt("чего она не видела космонавт") or 706.5
el(t_vint, t_vint + 11, "vintage")

t_shag = when_srt("по шагам") or 867.2
el(t_shag - .4, t_shag + 19, "shagi", head="ЧТО СДЕЛАТЬ СЕГОДНЯ",
   items=["снять мишуру — всю", "холодную гирлянду на тёплую",
          "оставить только то, что вписывается"])

BLOK = {"cards5", "cards4", "errors", "ritual", "reveal", "glaz", "shagi", "vintage"}

# ── 3 · планы; окно держится ПОДОТРЕЗКОМ и не перезапускается
CAMS = [("push", 1.0, 1.16), ("pan", 1.1, 1.1), ("crane", 1.18, 1.0),
        ("arc", 1.06, 1.14), ("wide", 1.14, 1.0), ("tilt", 1.12, 1.02)]
OKNO_MIN = 24.0      # меньше этого окно не открываем
KLIP_MAX = 26.0      # дольше этого один клип не крутим (пойдёт по кругу)
S, k = [], 0
t_hod = when_srt("А теперь взгляд") or 279.3

for sg in SEG:
    plans = []
    t = sg["a"]
    while t < sg["b"] - .4:
        zav = t < 32
        dur = min(6.0 if zav else 8.5, sg["b"] - t)
        if sg["b"] - (t + dur) < 2.5:
            dur = sg["b"] - t
        plans.append((t, t + dur))
        t += dur
    # раздача окна по планам: клипы меняются не чаще, чем раз в OKNO_MIN
    ok = sg["okno"] or ""
    vidy = []
    if ok:
        for part in ok.split("|"):
            if ":" in part:
                vidy.append(tuple(part.split(":", 1)))
            elif vidy:
                vidy.append((vidy[-1][0], part))
    if vidy and (sg["b"] - sg["a"]) < 7.0:
        vidy = []
    okno_map = {}
    if vidy:
        # один вид живёт НЕПРЕРЫВНО, но не дольше KLIP_MAX: зацикленный клип
        # длиннее получаса экрана начинает повторять сам себя.
        # Последний вид отрезка получает ровно KLIP_MAX секунд в конце.
        dlina = sg["b"] - sg["a"]
        if len(vidy) > 1 and dlina < OKNO_MIN + KLIP_MAX:
            vidy = vidy[:1]
        granica = sg["b"] - KLIP_MAX if len(vidy) > 1 else 1e9
        # переключаемся только на границе плана, и только если новому виду
        # достанется не меньше 12 секунд — иначе он мигнёт и пропадёт
        if len(vidy) > 1:
            podh = [a for a, b in plans if a >= granica and sg["b"] - a >= 12.0]
            granica = podh[0] if podh else 1e9
        gi, gstart = 0, plans[0][0] if plans else sg["a"]
        for i, (a, b) in enumerate(plans):
            if gi + 1 < len(vidy) and a >= granica:
                gi, gstart = gi + 1, a
            okno_map[i] = (vidy[gi], gstart)
    for i, (a, b) in enumerate(plans):
        evs = [e for e in EL if e["a"] < b and e["b"] > a]
        blok = any(e["kind"] in BLOK for e in evs)
        cam = CAMS[k % len(CAMS)]
        sc = {"n": len(S) + 1, "a": round(a, 2), "b": round(b, 2), "lok": sg["lok"],
              "tema": sg["tema"], "cam": cam[0], "z0": cam[1], "z1": cam[2],
              "koza": sg["koza"], "events": evs}
        if sg.get("sprava") and not blok:
            sc["sprava"] = sg["sprava"]
        if a <= t_hod < b:
            sc["koza"], sc["koza_hod"] = True, True
        if vidy and not blok:
            (rod, vid), gstart = okno_map[i]
            prev = S[-1] if S else None
            cont = bool(prev and prev.get("okno_vid") == vid
                        and abs(prev["b"] - a) < .01)
            sc["okno_vid"] = vid
            if cont:
                sc["okno_cont"] = True
            if rod == "clip":
                sc["stock"] = vid
            else:
                sc["foto"] = vid
            # наезд внутри окна считается по всему подотрезку, а не по плану,
            # иначе масштаб прыгает на стыке
            gend = gstart
            for j, (aa, bb) in enumerate(plans):
                if (okno_map.get(j, ((None, None),))[0][1] == vid
                        and okno_map[j][1] == gstart):
                    gend = bb
            sc["okno_a"], sc["okno_b"] = round(gstart, 2), round(gend, 2)
        S.append(sc)
        k += 1

# ── 4 · чистка: вставка короче 12 с мелькает. Такую группу присоединяем к
#       предыдущей (тот же вид продолжается) или снимаем окно совсем.
def gruppy(S):
    g = []
    for i, sc in enumerate(S):
        if not sc.get("okno_vid"):
            continue
        if g and g[-1][-1] == i - 1 and sc.get("okno_cont"):
            g[-1].append(i)
        else:
            g.append([i])
    return g


for _ in range(4):
    menyali = False
    for gr in gruppy(S):
        a, b = S[gr[0]]["a"], S[gr[-1]]["b"]
        if b - a >= 12.0:
            continue
        pred = gr[0] - 1
        if pred >= 0 and S[pred].get("okno_vid") and abs(S[pred]["b"] - a) < .01:
            vid, rod = S[pred]["okno_vid"], ("stock" if S[pred].get("stock") else "foto")
            for i in gr:
                S[i].pop("stock", None); S[i].pop("foto", None)
                S[i]["okno_vid"] = vid
                S[i]["okno_cont"] = True
                S[i][rod] = vid
                S[i]["okno_a"], S[i]["okno_b"] = S[pred]["okno_a"], S[gr[-1]]["b"]
            for i in range(gr[0] - 1, -1, -1):
                if S[i].get("okno_vid") != vid:
                    break
                S[i]["okno_b"] = S[gr[-1]]["b"]
        else:
            for i in gr:
                for key in ("stock", "foto", "okno_vid", "okno_cont", "okno_a", "okno_b"):
                    S[i].pop(key, None)
        menyali = True
    if not menyali:
        break

json.dump(S, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
okna = [s for s in S if s.get("okno_vid")]
vstavki = []
for s in okna:
    if not vstavki or vstavki[-1][0] != s["okno_vid"] or not s.get("okno_cont"):
        vstavki.append([s["okno_vid"], s["a"], s["b"]])
    else:
        vstavki[-1][2] = s["b"]
print("отрезков:", len(SEG), "· планов:", len(S), "· элементов:", len(EL))
print("вставок (непрерывных):", len(vstavki))
for v, a, b in vstavki:
    print("   %-18s %6.1f → %6.1f  (%.1f с)" % (v, a, b, b - a))
