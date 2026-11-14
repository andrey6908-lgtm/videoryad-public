# -*- coding: utf-8 -*-
"""Сборка кадра плана ролика «17 ноября — Ерёмин день».

ГЛАВНОЕ ОТЛИЧИЕ ОТ ПРОШЛЫХ РОЛИКОВ (его правило 14.11): настоящее видео и
фото стоят НЕ в окне в углу, а ВНУТРИ рисованной сцены — в устье печи, за
стеклом окна, в проёме арки, на экране сельского клуба, в витрине. Место
размечает сама декорация меткой `baza.mesto_stoka`, здесь метка подменяется
настоящим кадром, и камера везёт его вместе со слоем сцены.

Весь ролик рисованный: кадр принадлежит сцене, а не рамке в углу, поэтому
надписи работают на всю ширину — свободного угла больше нет.
"""
import json, os, re, math
import anim as A
import baza, lok, over, kamera, klipy
from baza import W, H
from karta import DEK

HERE = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(HERE, "foto")
KLIPY = {}          # {номер плана: папка с кадрами клипа} — ставит render.py
_ST = {}
if os.path.exists(os.path.join(HERE, "stock.json")):
    _ST = json.load(open(os.path.join(HERE, "stock.json"), encoding="utf-8"))

_STOK_METKA = re.compile(r'<g data-stok="([^"]*)"></g>')
_RE = re.compile(r"«([^»]*)»")


def kadr_stoka(pl, t=0.0):
    """Что стоит в проёме в этот миг: кадр КЛИПА, если он есть, иначе
    фотография из foto/. Один материал — один план, повторов в ролике нет."""
    k = klipy.kadr_klipa(KLIPY, pl["n"], t)
    if k:
        return k, True
    r = _ST.get(str(pl["n"]))
    if not r:
        return None, False
    p = os.path.join(FOTO, r["file"] if isinstance(r, dict) else r)
    return (p, False) if os.path.exists(p) else (None, False)


def plany(path=None):
    p = path or os.path.join(HERE, "plany.json")
    return json.load(open(p, encoding="utf-8"))


def nado_stok(pl):
    """В колонке «Сток внутри сцены» стоит место — значит кадр в сцену идёт."""
    s = (pl.get("stok") or "").strip().lower()
    return bool(s) and s not in ("нет", "не нужно", "-", "убрано")


def nadpisi(pl):
    """Колонка «Титр» → список (тип, текст)."""
    out = []
    raw = (pl.get("titr") or "").strip()
    if not raw or raw.lower() == "нет":
        return out
    for kus in re.split(r"\s*\|\s*|\n", raw):
        kus = kus.strip()
        if not kus:
            continue
        m = _RE.findall(kus)
        if ":" in kus:
            tip, hvost = kus.split(":", 1)
            tip, hvost = tip.strip(), hvost.strip()
        else:
            tip, hvost = (out[-1][0] if out else "Плашка"), kus
        # «Плашка главы: ИСТОРИЯ ДНЯ» → на экран идёт только ИСТОРИЯ ДНЯ
        for s in (m or [hvost]):
            out.append((tip, s))
    return out


def poyasneniya(pl):
    """Колонка «Надпись-пояснение» → [(совет?, текст)]. Это его правило 14.11:
    красивые поясняющие надписи и советы крупно по центру свободного места."""
    out = []
    raw = (pl.get("poyas") or "").strip()
    if not raw or raw.lower() in ("нет", "-"):
        return out
    for kus in re.split(r"\s*\|\s*|\n", raw):
        kus = kus.strip()
        if not kus:
            continue
        sovet = kus.lower().startswith("совет")
        for s in (_RE.findall(kus) or [kus.split(":", 1)[-1].strip()]):
            out.append((sovet, s))
    return out


SREDSTVA_IMENA = {
    "наезд": "C9 наезд", "наезд_быстро": "C9 push-наезд", "отъезд": "C2 отъезд",
    "панорама_лп": "C6 панорама", "панорама_пл": "C6 панорама", "кран": "C7 кран",
    "наклон_вверх": "C11 наклон вверх", "наклон_вниз": "C11 наклон вниз",
    "снижение": "C13 снижение", "проводка": "C10 проводка", "дуга": "C12 дуга 32°",
    "долли_зум": "C15 долли-зум", "наклон_горизонта": "C14 наклон горизонта",
    "push": "C9 три удара", "дыхание": "C9 дыхание кадра",
}


def sredstva(pl):
    """Что применено к плану — из общей библиотеки эффектов."""
    imya = DEK[pl["lok"]]
    h = hod_plana(pl)
    out = [SREDSTVA_IMENA.get(x, x) for x in (h if isinstance(h, tuple) else (h,))]
    sl = {z for z, _ in kamera.sloi(getattr(lok, imya)(2.0))}
    if len([z for z in sl if z != "fix"]) > 1:
        out.append("C1/K9 планы по глубине")
    if any(isinstance(z, int) and z >= 500 for z in sl):
        out.append("C17 воздушная перспектива")
    if imya in BLIK:
        out += ["C16/K17 блик в объектив", "K5 бегущий блик"]
    out += ["K15 тёплое пятно и тёмный бок", "K16 виньетка", "K18 градиенты", "C4 тени"]
    if nado_stok(pl):
        out.append("K30 настоящий кадр ВНУТРИ рисованной сцены")
    if poyasneniya(pl):
        out.append("K20 надпись-пояснение по центру")
    if nadpisi(pl):
        out.append("K19/K20 титры и плашки")
    out.append("K31 кроссфейд на стыке")
    return out


def hod_plana(pl):
    """Ход камеры этого плана — из колонки «Камера» раскадровки."""
    return kamera.razobrat(pl.get("kam", ""))


# где в кадре горит источник: блик в объектив ставим только туда.
# Список заполняется по декорациям этого ролика (см. lok.BLIKI).
BLIK = getattr(lok, "BLIKI", {})


def gabarit_stoka(pl, t=0.0):
    """Где в кадре стоит проём с настоящим кадром: (x, y, w, h) или None.
    Нужно надписям — они не должны ложиться поверх него (его слово 14.11:
    «не должны перекрывать наши мультяшные кадры»)."""
    if not nado_stok(pl):
        return None
    m = _STOK_METKA.search(getattr(lok, DEK[pl["lok"]])(t))
    if not m:
        return None
    ch = m.group(1).split(",")
    return tuple(float(v) for v in ch[:4])


def _vstavit_stok(syr, pl, t, zaglushki):
    """Метку проёма подменяем настоящим кадром. Делается ДО камеры, поэтому
    кадр едет вместе со своим слоем сцены и не отстаёт от неё."""
    m = _STOK_METKA.search(syr)
    if not m:
        return syr
    if not nado_stok(pl):
        return syr[:m.start()] + syr[m.end():]
    ch = m.group(1).split(",")
    x, y, w_, h_ = (float(v) for v in ch[:4])
    forma = ch[4] if len(ch) > 4 else "pryam"
    f, zhivoj = kadr_stoka(pl, t)
    if f:
        zam = over.stok_v_scene(x, y, w_, h_, forma, f, 0 if zhivoj else t,
                                pl["sek"], pl["n"], zhivoj)
    elif zaglushki:
        zam = over.stok_zaglushka(x, y, w_, h_, forma, pl["stok"], pl.get("najti", ""))
    else:
        # кадра нет — проём остаётся нарисованным: пустой рамки в кадре не будет
        zam = ""
    return syr[:m.start()] + zam + syr[m.end():]


def body(pl, t, p=.5, zaglushki=True):
    """SVG кадра. t — локальное время плана, p — доля плана (для камеры)."""
    imya = DEK[pl["lok"]]
    fn = getattr(lok, imya)
    syr = fn(t)
    syr = _vstavit_stok(syr, pl, t, zaglushki)
    if '<g data-z="-' not in syr:
        # интерьеру без переднего плана добавляем край кадра: без ближнего
        # слоя параллакса не видно, сцена остаётся плоской
        syr += baza.ramka_pp("levo", "#14110c", .30)
    scena = kamera.kadr(syr, hod_plana(pl), p)
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
           f'<defs>{baza.defs()}</defs>{scena}')
    # свет поверх сцены: блик в объектив и бегущий блик (C16/K17, K5)
    if imya in BLIK:
        bx, by = BLIK[imya]
        out += baza.blik(bx, by, t, .9, op=.5)
        out += baza.begushchiy_blik(t, 16.0, (pl["n"] * .17) % 1.0, .05)
    out += nalozheniya(pl, t, gabarit_stoka(pl, t))
    return out + "</svg>"


def _polosa(proem, vys, hochu):
    """Где положить ленту высотой `vys`, чтобы не лечь на проём со стоком.
    Его слово 14.11: настоящий кадр не перекрывается нашими плашками."""
    if not proem:
        return hochu
    px, py, pw, ph = proem
    if hochu + vys <= py + 8 or hochu >= py + ph - 8:
        return hochu                      # и так мимо
    sverhu, snizu = py - vys - 16, py + ph + 16
    if snizu + vys <= 1064:
        return snizu
    if sverhu >= 16:
        return sverhu
    return 1064 - vys                     # проём занял кадр — жмёмся к низу


def nalozheniya(pl, t, proem=None):
    """Надписи плана. Весь кадр рисованный, свободного угла нет — титры идут
    по центру и по краям, пояснения крупно по центру (R-0030)."""
    out = ""
    maxw = 1560
    lx = 100
    yy = 160
    kart = 0
    niz_zanyat = False
    tri = [n for n in nadpisi(pl) if n[0].startswith("Титр-обещание")]
    if not tri and pl["n"] == 1 and nadpisi(pl):
        tri = nadpisi(pl)                      # первый план — всегда титр-обещание
    if tri:
        stroki = []
        for _, s_ in tri:
            for kus in re.split(r"\s*·\s*", s_):
                kus = kus.strip()
                if kus:
                    stroki.append((kus, 86 if len(kus) < 18 else 56))
        return over.titr_obeshchanie(stroki, t, .5, 1120, 300)
    for tip, s in nadpisi(pl):
        tl = tip.lower()
        if tl.startswith("плашка главы"):
            out += over.plashka_glavy(s, t, .3, _polosa(proem, 150, 760), .9, W)
            yy = 620
        elif tl.startswith("плашка запрета"):
            m = re.match(r"ЗАПРЕТ\s*(\d+)\s*[—-]\s*(.+)", s)
            if m:
                out += over.plashka_zapreta(m.group(1), m.group(2), t, 1.1, lx, yy)
            else:
                out += over.plashka(lx, yy, s, t, 1.1, 52, .6, maxw=maxw)
            yy += 170
        elif tl.startswith("карточка"):
            m = re.match(r"(\d+)\.\s*(.+)", s)
            n_, txt_ = (m.group(1), m.group(2)) if m else ("", s)
            col = kart % 2
            out += over.kartochka(170 + col * 880, 300 + (kart // 2) * 190, 680, 150,
                                  n_, txt_, t, .6 + kart * .4)
            kart += 1
        elif tl.startswith("шапка") or tl.startswith("название"):
            out += over.plashka((W - over.wid(s, 58, "SERIF", 1) - 68) / 2, 80, s, t, .2, 58, maxw=1500)
        elif tl.startswith("плашка-вопрос") or tl.startswith("плашка под списком"):
            out += over.vopros_plashka(s, t, .8, _polosa(proem, 120, 820))
            niz_zanyat = True
        elif tl.startswith("финальная плашка"):
            out += over.vopros_plashka(s, t, 1.0, _polosa(proem, 120, 760))
            niz_zanyat = True
        elif (tl.startswith("подпись") or tl.startswith("на афиш")
              or tl.startswith("надпись на свитк") or tl.startswith("надпис")
              or tl.startswith("на лопат") or tl.startswith("на лист")
              or tl.startswith("на обложке") or tl.startswith("вывеска")):
            out += over.nadpis(560 + kart * 800, 250, s, t, .7, 42)
            kart += 1
        else:                      # обычная плашка, пословица, присказка
            kg = over.kegl_pod(s, maxw - 68, "SERIF", 56, 26)
            if kg < 40:            # длинную поговорку — лентой внизу, не мелочью в углу
                out += over.plashka_vniz(s, t, .9, _polosa(proem, 110, 880))
                niz_zanyat = True
            else:
                x = (W - over.wid(s, kg, "SERIF", 1) - 68) / 2
                out += over.plashka(x, yy, s, t, .9, kg, maxw=maxw)
                yy += 130
    # пояснения и советы — по центру свободного места, ниже титров
    poy = poyasneniya(pl)
    if poy:
        y0 = 620 if (yy > 600 or niz_zanyat) else 820
        if proem:                  # под проём не лезем: сток не перекрываем
            px, py, pw, ph = proem
            vysota = 130 * len(poy[:2])
            if py + ph + 24 + vysota <= 1040:
                y0 = py + ph + 24
            elif py - 24 - vysota >= 110:
                y0 = py - 24 - vysota
            else:                  # проём занял кадр — ставим лентой у самого низа
                y0 = 1040 - vysota
        if len(poy) > 1:
            y0 = min(y0, 660)
        for i, (sovet, s_) in enumerate(poy[:2]):
            out += over.poyasnenie(s_, t, .7 + i * .45, y0 + i * 130, sovet)
    return out
