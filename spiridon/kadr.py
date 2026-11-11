# -*- coding: utf-8 -*-
"""Сборка кадра плана: рисованная декорация + окно вставки + надписи.
Окно — НЕПОДВИЖНЫЙ контейнер в правой части (R-0014), рисованная обстановка
живёт в полосе 0-830 (R-0007). Генерация и фото — только внутрь окна (R-0003).
"""
import json, os, re, math
import anim as A
import baza, lok, over, kamera
from baza import W, H
from karta import DEK

HERE = os.path.dirname(os.path.abspath(__file__))
OKNO = (860, 300, 980, 551)


def plany(path=None):
    p = path or os.path.join(HERE, "plany.json")
    return json.load(open(p, encoding="utf-8"))


def nado_okno(pl):
    """Окно со стоком. У четырёх планов в колонке стоит ДАТА — это наша
    рисованная карточка, а не вставка; стока за ней нет."""
    o_ = (pl.get("okno") or "").strip().lower()
    if not o_ or o_ in ("убрано", "нет", "не нужно", "-"):
        return False
    return not o_.startswith("дата:")


def data_kartochka(pl):
    o_ = (pl.get("okno") or "").strip()
    if o_.lower().startswith("дата:"):
        m = _RE.findall(o_)
        return m[0] if m else o_.split(":", 1)[1].strip()
    return None


_RE = re.compile(r"«([^»]*)»")


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
        tip = kus.split(":")[0].strip() if ":" in kus else (out[-1][0] if out else "Плашка")
        for s in (m or [kus]):
            out.append((tip, s))
    return out


def hod_plana(pl):
    """Ход камеры этого плана — из колонки «Камера» раскадровки."""
    return kamera.razobrat(pl.get("kam", ""))


# где в кадре горит источник: блик в объектив ставим только туда
BLIK = {"pekarnya_noch": (400, 880), "pech_pekarni": (360, 860), "kolodec": (640, 300),
        "dvor_kolodec_noch": (300, 480), "zimnyaya_noch": (1560, 220),
        "prival": (410, 900), "svecha_okno": (500, 560), "izba_vecher": (360, 560),
        "parizh_yarmarka": (880, 450), "dvor_bulochnaya": (849, 300),
        "tri_okna": (175, 550), "okno_snaruzhi": (580, 580),
        "led_rassvet": (1350, 520), "krylco_rassvet": (1500, 300),
        "zaslonka": (430, 740), "kuhnya_duhovka": (410, 700),
        "dom_vecherom": (300, 600), "pod_maticey": (420, 660)}


def body(pl, t, p=.5, zaglushki=True):
    """SVG кадра. t — локальное время плана, p — доля плана (для камеры)."""
    imya = DEK[pl["lok"]]
    fn = getattr(lok, imya)
    # слои декорации разъезжаются по глубине под ход камеры (C1/K9)
    scena = kamera.kadr(fn(t), hod_plana(pl), p)
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
           f'<defs>{baza.defs()}</defs>{scena}')
    # свет поверх сцены: блик в объектив и бегущий блик (C16/K17, K5)
    if imya in BLIK:
        bx, by = BLIK[imya]
        out += baza.blik(bx, by, t, .9, op=.5)
    # бегущий блик — только там, где в кадре есть свой источник света,
    # иначе полоса поперёк кадра читается как брак
    if imya in BLIK:
        out += baza.begushchiy_blik(t, 16.0, (pl["n"] * .17) % 1.0, .05)
    dk = data_kartochka(pl)
    if dk:
        x, y, w_, h_ = OKNO
        out += over.kartochka_daty(x, y + 90, w_, h_ - 180, dk, t)
    if nado_okno(pl):
        x, y, w_, h_ = OKNO
        if zaglushki:
            out += over.okno_zaglushka(x, y, w_, h_, pl["okno"], pl.get("najti", ""))
        else:
            out += over.okno_ramka(x, y, w_, h_)
    out += nalozheniya(pl, t)
    return out + "</svg>"


def nalozheniya(pl, t):
    """Надписи плана. Под окно вставки не лезут (мина 3 и 5 «Ёлки»)."""
    out = ""
    est_okno = nado_okno(pl) or bool(data_kartochka(pl))
    shir = 830 if est_okno else W      # окно вставки занимает 860-1840
    maxw = 740 if est_okno else 1560
    lx = 70
    yy = 150
    kart = 0
    tri = [n for n in nadpisi(pl) if n[0].startswith("Титр-обещание")]
    if tri:
        return over.titr_obeshchanie([(s, 64) for _, s in tri], t, .5, 1010, 300)
    for tip, s in nadpisi(pl):
        tl = tip.lower()
        if tl.startswith("плашка главы"):
            out += over.plashka_glavy(s, t, .3, 780, .9, shir)
            yy = 640
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
        elif tl.startswith("шапка"):
            out += over.plashka((W - over.wid(s, 58, "SERIF", 1) - 68) / 2, 80, s, t, .2, 58, maxw=1500)
        elif tl.startswith("плашка-вопрос") or tl.startswith("плашка под списком"):
            out += over.vopros_plashka(s, t, .8, 820)
        elif tl.startswith("финальная плашка"):
            out += over.vopros_plashka(s, t, 1.0, 760)
        elif tl.startswith("в окне"):
            if data_kartochka(pl):
                continue           # дата уже нарисована карточкой
            x, y, w_, h_ = OKNO
            out += over.nadpis(x + w_ / 2, y + h_ - 34, s, t, .8, 40)
        elif tl.startswith("на экране телефона"):
            out += over.nadpis(430, 1000, s, t, .9, 40)
        elif (tl.startswith("на лопат") or tl.startswith("на лист")
              or tl.startswith("на обложке") or tl.startswith("вывеска")
              or tl.startswith("на визитке")):
            out += over.nadpis(300 + kart * 330, 270, s, t, .7, 36)
            kart += 1
        else:                      # обычная плашка, пословица, поговорка
            kg = over.kegl_pod(s, maxw - 68, "SERIF", 52, 26)
            if kg < 38:            # длинную поговорку — лентой внизу, не мелочью в углу
                out += over.plashka_vniz(s, t, .9, 900)
            else:
                x = lx if est_okno else (W - over.wid(s, kg, "SERIF", 1) - 68) / 2
                out += over.plashka(x, yy, s, t, .9, kg, maxw=maxw)
                yy += 120
    return out
