# -*- coding: utf-8 -*-
"""Кадр ролика «Ёлка 2027»: фотоподложка с движением камеры + наши наложения,
или целиком рисованная сцена. Всё считается от времени, кадр собирается заново."""
import io, math, os
import cairosvg
from PIL import Image
import anim as A
import over as O
from ng import *

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
_foto = {}


def foto(path):
    if path not in _foto:
        im = Image.open(os.path.join(HERE, path)).convert("RGB")
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        _foto[path] = im
    return _foto[path]


def kb(im, z0, z1, ax, ay, p, box=False):
    """Движение камеры по фото: окно едет и наезжает — покадрово, без ступенек.
    box=True отдаёт ещё и окно: по нему координаты обводок переводятся в экранные,
    иначе указатель уезжает с деталью (поймано на первом прогоне)."""
    z = z0 + (z1 - z0) * A.ease(p)
    cw, ch = W / z, H / z
    x = min(max(0.0, ax * W - cw / 2), W - cw)
    y = min(max(0.0, ay * H - ch / 2), H - ch)
    out = im.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch))
    return (out, (x, y, cw, ch)) if box else out


def svg2img(body, defs=True):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"'
         f' viewBox="0 0 {W} {H}">'
         + (f'<defs>{O.defs_all()}</defs>' if defs else "") + body + '</svg>')
    png = cairosvg.svg2png(bytestring=s.encode("utf-8"), output_width=W, output_height=H,
                           background_color="transparent")
    return Image.open(io.BytesIO(png)).convert("RGBA")


def room_bg(t, pol=.78):
    return room(W, H, pol) + kamin(120, 430) + O.sneg(t, 28, 9)


# ─────────────────── рисованные сцены ───────────────────
def sc_five(sc, t, dur, gt):
    """Пять ёлок подряд: каждая по 2,6 с, на пятой стоп и знак вопроса."""
    fs = sc["foto"]
    step = 2.6
    i = min(int(t / step), len(fs) - 1)
    local = t - i * step
    im = kb(foto(fs[i]), 1.06, 1.0, .5, .5, min(1.0, local / step))
    b = ""
    if i == len(fs) - 1 and local > .6:
        b += O.zatemn(min(.55, (local - .6) * .5))
        b += O.vopros(W // 2, 700, t, i * step + 1.4, 320)
    if t < 1.0:
        b += O.zatemn(max(0.0, 1 - t))
    b += O.vign()
    return im, b


def sc_title(sc, t, dur, gt):
    bg = svg2img(f'<rect width="{W}" height="{H}" fill="{TEMN}"/>' + O.sneg(t, 50, 4)).convert("RGB")
    b = O.nalив(140, 300, "ЁЛКА 2027", t, .4, 150)
    b += O.pechat(140, 390, "наряжаем — удачу и счастье привлекаем", t, 2.2, 42)
    pal = [[VIN, GRAN, ZOL], ["#8a6b45", "#c9b58a", "#6d8a4a"], [ZOL, "#d9cdb0", SVET],
           [GRAN, "#b9743f", KREM]]
    nm = ["винная", "природная", "металлик", "семейная"]
    for i in range(4):
        x = 150 + i * 330
        b += O.card(x, 520, 280, 290, t, 4.0 + i * .5)
        if A.seg(t, 4.0 + i * .5, .4) > .9:
            b += tree(x + 140, 770, 200, pal[i], bows_on=False)
            b += O.txt(x + 140, 860, nm[i], 30, KREM, "middle", O.SANS, 1, "600")
    b += O.card(1520, 520, 280, 290, t, 6.2, "#140d0b", .95, "#ff6b6b")
    b += O.vopros(1660, 740, t, 6.6, 150)
    return bg, b


def sc_goat_card(sc, t, dur, gt):
    bg = svg2img(f'<rect width="{W}" height="{H}" fill="{TEMN}"/>' + O.sneg(t, 30, 7)).convert("RGB")
    rip = A.out(A.seg(t, dur * .55, 1.2))
    b = ""
    for side in (-1, 1):
        dx = side * rip * 230
        rot = side * rip * 7
        b += (f'<g transform="translate({dx:.0f},{rip*40:.0f}) rotate({rot:.1f} 960 560)">'
              f'<clipPath id="half{1 if side>0 else 0}">'
              f'<rect x="{960 if side>0 else 300}" y="150" width="660" height="800"/></clipPath>'
              f'<g clip-path="url(#half{1 if side>0 else 0})">')
        b += f'<rect x="360" y="170" width="1200" height="760" rx="14" fill="#efe6d2" stroke="{TERRA}" stroke-width="8"/>'
        b += f'<rect x="420" y="620" width="1080" height="250" rx="12" fill="#cfe0b8"/>'
        b += koza(820, 640, 1.5)
        b += O.txt(960, 300, "«мягкая, любит травку»", 54, "#5a4632", "middle", O.SANS, 1, "600", stroke=0)
        b += "</g></g>"
    if rip > .05:
        b += (f'<path d="M960,120 l-40,160 l54,120 l-44,150 l50,140 l-36,190" fill="none"'
              f' stroke="{TEMN}" stroke-width="{10+18*rip:.0f}" stroke-linejoin="round"/>')
    b += O.vign()
    return bg, b


def sc_live(sc, t, dur, gt):
    bg = svg2img(f'<rect width="{W}" height="{H}" fill="{TEMN}"/>' + O.sneg(t, 40, 2)).convert("RGB")
    b = O.okno_ramka(260, 180, 1400, 790)
    b += O.plate(260, 960, sc["pod"][0], sc["pod"][1], t, .6, 760)
    return bg, b


def sc_eye(sc, t, dur, gt):
    bg = svg2img(f'<rect width="{W}" height="{H}" fill="{TEMN}"/>').convert("RGB")
    p = A.ease(A.seg(t, .5, 1.6))
    b = (f'<path d="M960,540 m-620,0 a620,620 0 0 1 1240,0 l-80,0 a540,540 0 0 0 -1080,0 Z"'
         f' fill="{SVET}" opacity="{.2*p:.2f}"/>')
    b += f'<ellipse cx="960" cy="540" rx="300" ry="190" fill="#f3ead5" {o(8)}/>'
    wob = 1 + .06 * A.w(t, 3.4)
    b += f'<ellipse cx="960" cy="540" rx="{150*wob:.0f}" ry="46" fill="{K}"/>'
    b += f'<circle cx="890" cy="505" r="22" fill="#ffffff" opacity=".85"/>'
    b += O.nalив(960 - 460, 240, "ГОРИЗОНТАЛЬНЫЙ ЗРАЧОК", t, .8, 56)
    b += O.pechat(560, 900, "видит почти триста сорок градусов", t, 3.0, 44)
    b += O.iskry(t, 960, 540, 10, 6, 420)
    return bg, b


def sc_room_walk(sc, t, dur, gt):
    p = A.ease(A.seg(t, .5, dur * .6))
    bg = svg2img(room_bg(t) + tree(1480, 920, 560, [VIN, ZOL, KRAS])
                 + gift(1250, 940, 150, 110, VIN) + gift(1420, 960, 170, 92, ZEL2, SVET)).convert("RGB")
    gx = 260 + p * 980
    b = koza(gx, 820, 1.0)
    if p > .05:
        b += (f'<path d="M260,900 L{gx:.0f},900" stroke="{SVET}" stroke-width="7"'
              f' stroke-dasharray="22 18" opacity=".8"/>')
    if p > .9:
        b += O.plate(120, 120, "ОНА ИДЁТ К ЁЛКЕ", "мимо стола и подарков", t, dur * .62, 620)
    b += O.vign()
    return bg, b


def sc_split(sc, t, dur, gt):
    bg = svg2img(f'<rect width="{W}" height="{H}" fill="{TEMN}"/>' + O.sneg(t, 26, 11)).convert("RGB")
    (ln, lp, lok), (rn, rp, rok) = sc["left"], sc["right"]
    b = O.card(80, 180, 840, 780, t, .3, "#2a1416", .9, "#ff6b6b")
    b += O.card(1000, 180, 840, 780, t, .8, "#15220f", .9, "#7ed07e")
    if A.seg(t, .3, .4) > .9:
        b += O.txt(500, 300, ln, 44, "#ff9d9d", "middle", O.SANS, 1, "600")
        b += tree(500, 880, 440, lp, bows_on=False)
    if A.seg(t, .8, .4) > .9:
        b += O.txt(1420, 300, rn, 44, "#b7f0b7", "middle", O.SANS, 1, "600")
        b += tree(1420, 880, 440, rp, bows_on=False)
    b += O.galka(500, 380, t, 2.2, 48, lok)
    b += O.galka(1420, 380, t, 2.8, 48, rok)
    return bg, b


def sc_box(sc, t, dur, gt):
    bg = svg2img(room_bg(t, .82)).convert("RGB")
    op = A.ease(A.seg(t, .4, 1.0))
    b = (f'<g opacity="{op:.2f}"><rect x="620" y="520" width="680" height="330" rx="14"'
         f' fill="{TERRA}" {o(8)}/>'
         f'<rect x="600" y="470" width="720" height="80" rx="10" fill="#8a5a3c" {o(8)}/>')
    for i, (dx, col) in enumerate(((120, KRAS), (260, GRAN), (400, VIN), (540, KRAS))):
        bob = 10 * A.w(t, 2.6, i * .2)
        b += ball(620 + dx, 600 + bob, 48, col)
    b += "</g>"
    b += bow(1420, 640, 1.5, VIN)
    b += O.plate(120, 140, sc["pod"][0], sc["pod"][1], t, 1.2, 760)
    b += O.vign()
    return bg, b


def sc_shishki(sc, t, dur, gt):
    bg = svg2img(room_bg(t)).convert("RGB")
    b = tree(960, 940, 600, ["#8a6b45", "#c9b58a", "#6d8a4a"], bows_on=False)
    n = 1 if t < dur * .45 else 10
    import random
    r = random.Random(4)
    for i in range(n):
        p = A.over(A.seg(t, (0 if i == 0 else dur * .45) + i * .08, .4), 1.5)
        if p <= 0:
            continue
        x = 960 + r.uniform(-200, 200)
        y = 560 + r.uniform(-180, 240)
        b += (f'<g transform="translate({x:.0f},{y:.0f}) scale({p:.2f})">'
              f'<ellipse cx="0" cy="0" rx="26" ry="38" fill="#8a5a3c" {o(5)}/>'
              f'<path d="M-18,-18 q18,10 36,0 M-20,2 q20,10 40,0 M-16,20 q16,8 32,0"'
              f' fill="none" stroke="#5e3a22" stroke-width="5"/></g>')
    b += O.plate(120, 130, "ОДНА — СЛУЧАЙНОСТЬ", "десять — замысел", t, dur * .5, 700)
    b += O.vign()
    return bg, b


def sc_shkaf(sc, t, dur, gt):
    bg = svg2img(f'<rect width="{W}" height="{H}" fill="#2a1a18"/>'
                 f'<rect x="420" y="60" width="1080" height="960" rx="12" fill="{TERRA}" {o(9)}/>'
                 f'<rect x="460" y="110" width="1000" height="300" rx="8" fill="#3a2420" {o(6)}/>'
                 f'<rect x="460" y="450" width="1000" height="300" rx="8" fill="#3a2420" {o(6)}/>').convert("RGB")
    p = A.ease(A.seg(t, .6, 2.2))
    y = 180 + p * 420
    b = (f'<g transform="translate(0,{y-180:.0f})">'
         f'<rect x="700" y="180" width="520" height="230" rx="12" fill="#8a5a3c" {o(8)}/>'
         f'<rect x="690" y="160" width="540" height="60" rx="8" fill="{TERRA}" {o(7)}/></g>')
    if p > .8:
        q = A.seg(t, 3.0, 1.2)
        for i in range(5):
            bob = 12 * A.w(t, 2.2, i * .25)
            b += ball(760 + i * 110, y + 40 + bob, 42, [KRAS, ZOL, GRAN, KREM, VIN][i])
        b += O.pechat(560, 940, "в ней то, что уже ничего не стоит и дороже всего", t, 3.4, 42)
    b += O.vign()
    return bg, b


def sc_sloi(sc, t, dur, gt):
    bg = svg2img(room_bg(t)).convert("RGB")
    st = dur / 4
    b = tree(960, 950, 620, [], bows_on=False, bare=True)
    if t > st * .4:
        b += lights(640, 640, 640, 9, 10)
    if t > st * 1.4:
        for i in range(6):
            p = A.over(A.seg(t, st * 1.4 + i * .3, .4), 1.4)
            if p > 0:
                b += ball(780 + (i % 3) * 170, 520 + (i // 3) * 170, 44 * p, [KREM, ZOL][i % 2])
    if t > st * 2.6:
        for i in range(5):
            p = A.over(A.seg(t, st * 2.6 + i * .35, .4), 1.5)
            if p > 0:
                b += ball(820 + i * 90, 760, 34 * p, [GRAN, "#b9743f", KREM, ZOL, VIN][i])
    b += O.spisok(120, 300, ["сначала свет", "потом крупные", "потом старые"], t, 1.0,
                  st / 1.6, 40, 80, num=True)
    b += O.vign()
    return bg, b


def sc_perebor(sc, t, dur, gt):
    bg = svg2img(room_bg(t)).convert("RGB")
    import random
    r = random.Random(9)
    fall = A.seg(t, .8, 1.6)
    back = A.seg(t, dur * .55, 1.6)
    b = tree(960, 950, 600, [KRAS, ZOL, VIN, "#7fd0ff", "#9ee07f"], bows_on=False)
    for i in range(40):
        x = 960 + r.uniform(-300, 300)
        y0 = -100 - r.uniform(0, 400)
        y1 = 420 + r.uniform(0, 420)
        y = y0 + (y1 - y0) * A.ease(min(1.0, fall + i * .005))
        if back > 0:
            y = y + (1100 - y) * A.ease(back)
        b += ball(x, y, 26, [KRAS, ZOL, VIN, "#7fd0ff", "#9ee07f", KREM][i % 6])
    if t > dur * .6:
        b += O.plate(120, 140, "НЕ ВСЁ СРАЗУ", "пять-семь любимых, остальное в коробку", t,
                     dur * .62, 820)
    b += O.vign()
    return bg, b


def sc_grid4(sc, t, dur, gt):
    bg = svg2img(f'<rect width="{W}" height="{H}" fill="{TEMN}"/>' + O.sneg(t, 40, 8)).convert("RGB")
    pal = [[VIN, GRAN, ZOL], ["#8a6b45", "#c9b58a", "#6d8a4a"], [ZOL, "#d9cdb0", SVET],
           [GRAN, "#b9743f", KREM]]
    nm = ["винная", "природная", "металлик", "семейная"]
    b = ""
    for i in range(4):
        x = 150 + (i % 2) * 470
        y = 150 + (i // 2) * 430
        b += O.card(x, y, 410, 390, t, .2 + i * .3)
        if A.seg(t, .2 + i * .3, .4) > .9:
            b += tree(x + 205, y + 340, 260, pal[i], bows_on=False)
            b += O.txt(x + 205, y + 375, nm[i], 28, KREM, "middle", O.SANS, 1, "600")
            if sc.get("goats"):
                b += koza(x + 320, y + 95, .32)
            else:
                b += O.galka(x + 350, y + 60, t, 1.6 + i * .3, 30, True)
    if sc.get("q5"):
        b += O.card(1120, 330, 640, 420, t, 1.8, "#140d0b", .95, "#ff6b6b")
        b += O.vopros(1440, 600, t, 2.2, 200)
    return bg, b


def sc_mishura(sc, t, dur, gt):
    im = kb(foto("foto/ёлка_ошибка.jpg"), 1.3, 1.42, .58, .62, A.seg(t, 0, dur))
    b = O.zatemn(min(.78, .3 + t * .3))
    b += O.nalив(430, 500, "МИШУРА", t, .4, 200)
    if t > 2.6:
        b += O.txt(960, 650, "ВОТ ОНА", 92, "#ff6b6b", "middle")
    if t > 4.0:
        b += O.pechat(560, 790, "та самая вещь, которую вешают последней", t, 4.0, 42)
    return im, b


def sc_check(sc, t, dur, gt):
    bg = svg2img(room_bg(t) + tree(1540, 940, 480, [VIN, ZOL, KRAS])).convert("RGB")
    b = O.card(110, 180, 1180, 700, t, .2)
    b += O.txt(170, 300, "СЕГОДНЯ ВЕЧЕРОМ", 54, SVET)
    items = ["снять мишуру", "поменять свет на тёплый", "убрать лишние цвета"]
    b += O.spisok(180, 430, items, t, 1.2, 2.2, 46, 130, num=True)
    for i in range(3):
        b += O.galka(1120, 420 + i * 130, t, 2.6 + i * 2.2, 40, True)
    if t > dur * .75:
        b += O.pechat(180, 840, "один вечер — и ёлка работает весь год", t, dur * .75, 40)
    b += O.vign()
    return bg, b


def sc_cards4(sc, t, dur, gt):
    bg = svg2img(f'<rect width="{W}" height="{H}" fill="{TEMN}"/>' + O.sneg(t, 36, 3)).convert("RGB")
    nm = ["винная", "природная", "металлик", "семейная"]
    pal = [[VIN, GRAN, ZOL], ["#8a6b45", "#c9b58a", "#6d8a4a"], [ZOL, "#d9cdb0", SVET],
           [GRAN, "#b9743f", KREM]]
    b = O.txt(960, 170, "КАКАЯ ВАША?", 72, "#ffffff", "middle")
    for i in range(4):
        x = 110 + i * 440
        b += O.card(x, 280, 400, 420, t, .3 + i * .25)
        if A.seg(t, .3 + i * .25, .4) > .9:
            b += tree(x + 200, 640, 250, pal[i], bows_on=False)
            b += (f'<circle cx="{x+200}" cy="340" r="46" fill="{ZOL}" {o(6)}/>'
                  f'<text x="{x+200}" y="358" text-anchor="middle" font-family="{O.SERIF}"'
                  f' font-size="52" font-weight="bold" fill="#17130f">{i+1}</text>')
            b += O.txt(x + 200, 690, nm[i], 30, KREM, "middle", O.SANS, 1, "600")
    b += O.card(560, 790, 800, 170, t, 2.4, "#1d1310", .95, SVET)
    if A.seg(t, 2.4, .4) > .9:
        cur = "|" if (t * 2) % 1 < .5 else " "
        b += O.txt(610, 890, "пишите цифру в комментариях " + cur, 40, KREM,
                   font=O.SANS, ls=1, weight="600")
    return bg, b


def sc_final(sc, t, dur, gt):
    bg = svg2img(room_bg(t) + tree(600, 950, 620, [VIN, ZOL, KRAS])).convert("RGB")
    b = koza(650, 250, .8)
    wave = 12 * A.w(t, 1.6)
    b += (f'<path d="M710,180 q40,{-30+wave:.0f} 74,{-10+wave:.0f}" fill="none"'
          f' stroke="{KREM}" stroke-width="10" stroke-linecap="round"/>')
    p = A.over(A.seg(t, .6, .5), 1.8)
    if p > 0:
        b += (f'<g transform="translate(1180,760) scale({p:.2f}) translate(-1180,-760)">'
              f'<rect x="920" y="708" width="520" height="104" rx="52" fill="{KRAS}" {o(8)}/>'
              + O.txt(1180, 780, "ПОДПИСАТЬСЯ", 46, "#ffffff", "middle", O.SANS, 3, "bold") + "</g>")
    b += O.pechat(900, 900, "дальше: когда ставить и когда снимать ёлку", t, 3.0, 36)
    b += O.iskry(t, 1180, 760, 12, 2, 300)
    b += O.vign()
    return bg, b


# ─────────────────── фотосцена с наложениями ───────────────────
def sc_photo(sc, t, dur, gt):
    p = A.seg(t, 0, dur)
    im, win = kb(foto(sc["foto"]), sc.get("z0", 1.0), sc.get("z1", 1.08),
                 sc.get("ax", .5), sc.get("ay", .5), p, box=True)
    wx, wy, cw, ch = win
    kx, ky = W / cw, H / ch

    def ekran(px, py):
        return (px - wx) * kx, (py - wy) * ky
    b = ""
    if sc.get("dark"):
        b += O.zatemn(sc["dark"])
    if sc.get("dark_end"):
        b += O.zatemn(.55 * A.ease(A.seg(t, dur * .45, dur * .5)))
    if sc.get("q"):
        b += O.vopros(330, 640, t, 1.0, 240)
    if sc.get("live_win"):
        wb = sc.get("win_box", [1180, 150, 640, 360])
        b += O.okno_ramka(*wb)
    if sc.get("plate"):
        b += O.plate(110, 110, sc["plate"][0], sc["plate"][1], t, .5, 700)
    if sc.get("pal"):
        cols, pod = sc["pal"]
        b += O.palitra(200, sc.get("pal_y", 330), cols, pod, t, 1.6)
    for ob in sc.get("obv", []):
        cx, cy, rx, ry, pod, side, dx, t0 = ob
        sx, sy = ekran(cx, cy)
        b += O.obvodka(sx, sy, rx * kx, ry * ky, pod, t, t0,
                       "#ff6b6b" if sc.get("red") else SVET, side, dx)
    if sc.get("card3"):
        b += O.card(1180, 300, 640, 540, t, 1.0, "#1b2416", .9, "#6d8a4a")
        b += O.txt(1230, 400, "ТРИ ШАГА", 46, "#b7f0b7")
        b += O.spisok(1230, 500, sc["card3"], t, 2.0, 1.6, 38, 90, num=True)
    if sc.get("card2"):
        b += O.card(120, 820, 760, 180, t, 1.4, "#1d1310", .92, "#7ed07e")
        b += O.txt(170, 900, sc["card2"][0], 40, "#b7f0b7", font=O.SANS, ls=1, weight="600")
        b += O.txt(170, 960, sc["card2"][1], 36, "#ff9d9d", font=O.SANS, ls=1, weight="600")
    if sc.get("dots"):
        for i, (c, nm, ok) in enumerate(sc["dots"]):
            y = 300 + i * 150
            q = A.over(A.seg(t, 2.0 + i * .8, .4), 1.5)
            if q <= 0:
                continue
            b += f'<circle cx="220" cy="{y}" r="{54*q:.0f}" fill="{c}" {o(6)}/>'
            b += O.galka(330, y, t, 2.4 + i * .8, 34, ok)
            b += O.txt(410, y + 14, nm, 38, KREM, font=O.SANS, ls=1, weight="600")
    if sc.get("formula"):
        b += O.card(1120, 280, 700, 560, t, .6)
        b += O.txt(1170, 380, "ФОРМУЛА", 46, SVET)
        for i, (cx, r, col) in enumerate(((1240, 78, ZOL), (1430, 52, "#3f8a4a"),
                                          (1580, 26, KREM), (1650, 26, KREM), (1720, 26, KREM))):
            q = A.over(A.seg(t, 1.6 + i * .4, .4), 1.6)
            if q > 0:
                b += f'<circle cx="{cx}" cy="520" r="{r*q:.0f}" fill="{col}" {o(6)}/>'
        b += O.pechat(1170, 700, "один большой, один средний, три мелких", t, 4.0, 32)
    if sc.get("goat"):
        p2 = A.ease(A.seg(t, .8, dur * .7))
        gy = 980 - p2 * 520
        b += koza(1420, gy, .9 + .1 * p2)
        if sc.get("sector"):
            b += (f'<path d="M1420,{gy-60:.0f} L700,300 L700,900 Z" fill="{SVET}" opacity=".16"/>')
    if sc.get("goat_top"):
        b += koza(1180, 300, .9)
        b += O.iskry(t, 1180, 300, 10, 5, 220)
    if sc.get("goat_leave"):
        p2 = A.ease(A.seg(t, 1.2, dur * .6))
        b += koza(1380 - p2 * 1500, 880 + 40 * math.sin(p2 * 6), 1.0)
    if sc.get("glow_mishura"):
        for i in range(5):
            y = 420 + i * 120
            op = .35 + .35 * abs(A.w(t, 2.4, i * .2))
            b += (f'<path d="M820,{y} q320,70 620,-30" fill="none" stroke="{SVET}"'
                  f' stroke-width="16" opacity="{op:.2f}"/>')
    if sc.get("strip"):
        q = A.ease(A.seg(t, .8, dur * .7))
        for i in range(6):
            y = 900 - i * 120
            if q > i / 6:
                b += (f'<path d="M800,{y} q340,80 660,-30" fill="none" stroke="#1d3a1d"'
                      f' stroke-width="26" opacity=".85"/>')
        b += O.pechat(140, 980, "мишура снимается кольцо за кольцом", t, 1.2, 40)
    if sc.get("flare"):
        b += O.iskry(t, 1360, 300, 16, 1, 320)
    b += O.vign()
    if not sc.get("dark"):
        b += O.sneg(gt, 22, 6)
    return im, b


KINDS = {"five": sc_five, "title": sc_title, "goat_card": sc_goat_card, "live": sc_live,
         "eye": sc_eye, "room_walk": sc_room_walk, "photo": sc_photo, "split": sc_split,
         "box": sc_box, "shishki": sc_shishki, "shkaf": sc_shkaf, "sloi": sc_sloi,
         "perebor": sc_perebor, "grid4": sc_grid4, "mishura": sc_mishura,
         "check": sc_check, "cards4": sc_cards4, "final": sc_final}


def frame(sc, t, gt):
    dur = sc["b"] - sc["a"]
    bg, body = KINDS[sc["kind"]](sc, t, dur, gt)
    if body:
        ov = svg2img(body)
        bg = bg.convert("RGBA")
        bg.alpha_composite(ov)
        bg = bg.convert("RGB")
    return bg
