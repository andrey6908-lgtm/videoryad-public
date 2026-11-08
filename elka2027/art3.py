# -*- coding: utf-8 -*-
"""Кадр версии 3 (после его разбора 07.11).

Что изменено по его замечаниям:
  · декорации меняются — кадр берёт локацию из lok.LOK, а не одну комнату;
  · окно вставки ЗАФИКСИРОВАНО на экране и не ездит с камерой; содержимое
    обрезается по окну (cover), пустых полей внутри рамки нет;
  · окно исчезает, когда на экране наш блок (карточки, ошибки, обряд);
  · хозяйка года крупная и огненная, живёт в сцене;
  · всё появляется в секунду, когда звучит слово.
"""
import io, math, os
import cairosvg
from PIL import Image
import anim as A
import over as O
import lok as L
from ng import *

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
from okna import OKNO, OKNO_LOK      # позиции окна лежат отдельно
_foto = {}
TITLE = {"vin": ("ВИННАЯ", "бордо, гранат, вишня, золото"),
         "eko": ("ПРИРОДНАЯ", "хвоя, олива, молочный, дерево"),
         "met": ("МЕТАЛЛИК", "золото, латунь, бронза, серебро"),
         "vnt": ("СЕМЕЙНАЯ", "игрушки, которым по полвека"),
         "err": ("ЁЛКА-ОШИБКА", "всё сразу и ничего не вместе")}
PALS = {"vin": (["#7d1f2e", "#9c2740", "#8e1b2e", "#c9922f", "#2d6236"],
                ["бордо", "гранат", "вишня", "золото", "хвоя"]),
        "eko": (["#24512e", "#6d8a4a", "#efe6d2", "#d9c9a8", "#8a6b45"],
                ["хвоя", "олива", "молочный", "бежевый", "дерево"]),
        "met": (["#c9922f", "#b8860b", "#8c6239", "#c0c0c0", "#2d6236"],
                ["золото", "латунь", "бронза", "серебро", "зелень"]),
        "vnt": (["#9c2740", "#b9743f", "#e4d4b6", "#c9922f", "#2d6236"],
                ["красный", "медь", "молочный", "золото", "хвоя"]),
        "err": (["#d6202f", "#7fd0ff", "#9ee07f", "#c9922f", "#b06ad6"],
                ["красный", "синий", "зелёный", "золото", "фиолет"])}


def foto(path):
    if path not in _foto:
        im = Image.open(os.path.join(HERE, path)).convert("RGB")
        _foto[path] = im
    return _foto[path]


def svg2img(body, vb=None):
    vx, vy, vw, vh = vb or (0, 0, W, H)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"'
         f' viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}">'
         f'<defs>{O.defs_all()}</defs>{body}</svg>')
    png = cairosvg.svg2png(bytestring=s.encode("utf-8"), output_width=W, output_height=H,
                           background_color="transparent")
    return Image.open(io.BytesIO(png)).convert("RGBA")


def kamera(sc, p):
    z = sc.get("z0", 1.0) + (sc.get("z1", 1.1) - sc.get("z0", 1.0)) * A.ease(p)
    cx, cy = .5, .52
    cam = sc.get("cam")
    if cam == "pan":
        cx += .2 * (p - .5)
    elif cam == "crane":
        cy = .66 - .22 * A.ease(p)
    elif cam == "arc":
        cx = .58 - .16 * A.ease(p); cy = .48 + .06 * A.ease(p)
    elif cam == "tilt":
        cy = .68 - .2 * A.ease(p)
    vw, vh = W / z, H / z
    vx = min(max(0.0, cx * W - vw / 2), W - vw)
    vy = min(max(0.0, cy * H - vh / 2), H - vh)
    return vx, vy, vw, vh


def cover(im, w, h, p=0.0):
    """Заполнить окно целиком: масштаб по большей стороне + обрез. Пустых
    полей внутри рамки не остаётся (его правка 9). Плюс лёгкий наезд."""
    z = 1.0 + .10 * A.ease(p)
    sw, sh = im.size
    k = max(w / sw, h / sh) * z
    nw, nh = int(sw * k) + 1, int(sh * k) + 1
    im2 = im.resize((nw, nh), Image.BILINEAR)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return im2.crop((x, y, x + w, y + h))


def koza_ognennaya(cx, cy, t, s=1.0):
    """Хозяйка года, версия 2 (прежняя отклонена: «вся красная, бестолковая»).

    Теперь: светлая кремово-золотая шерсть, ОГОНЬ только как грива, хвост и
    кончики копыт, тёплое свечение вокруг, добрый взгляд с моргающим глазом,
    изогнутые рога. Красный ушёл в акценты — попона и бубенец.
    """
    SHERST, TEN_SH = "#f0e2c6", "#d9c49c"
    g = f'<g transform="translate({cx:.0f},{cy:.0f}) scale({s:.3f})">'
    g += f'<ellipse cx="0" cy="170" rx="250" ry="42" fill="url(#ten)" opacity=".55"/>'
    g += f'<ellipse cx="10" cy="-20" rx="330" ry="260" fill="url(#teplo)" opacity=".55"/>'
    # хвост-огонёк
    for i in range(3):
        hh = 90 + 30 * abs(A.w(t, 1.1, i * .2))
        g += (f'<path d="M-180,-20 C{-210-10*i},{-40-hh*.4:.0f} {-200+14*A.w(t,1.3,i*.2):.0f},'
              f'{-50-hh*.7:.0f} {-186:.0f},{-30-hh:.0f} C{-170:.0f},{-50-hh*.6:.0f}'
              f' {-166-6*i},{-40-hh*.3:.0f} -180,-20 Z" fill="{[ORA, SVET, KRAS][i]}"'
              f' opacity="{.6+.3*abs(A.w(t,.9,i*.2)):.2f}"/>')
    # грива: пламя по хребту и шее
    for i in range(12):
        bx = -130 + i * 26
        hh = (90 + 70 * abs(math.sin(i * .9))) * (1 + .25 * A.w(t, .85, i * .11))
        dx = 16 * A.w(t, 1.4, i * .18)
        col = [ORA, SVET, KRAS, "#ffb347"][i % 4]
        g += (f'<path d="M{bx},-70 C{bx-22},{-70-hh*.4:.0f} {bx-6+dx:.0f},{-70-hh*.72:.0f}'
              f' {bx+dx:.0f},{-70-hh:.0f} C{bx+18+dx:.0f},{-70-hh*.66:.0f}'
              f' {bx+24},{-70-hh*.34:.0f} {bx},-70 Z" fill="{col}"'
              f' opacity="{.55+.35*abs(A.w(t,1.0,i*.15)):.2f}"/>')
    # тело
    g += f'<ellipse cx="-20" cy="30" rx="168" ry="112" fill="{SHERST}" {o(8)}/>'
    g += f'<ellipse cx="-20" cy="62" rx="150" ry="74" fill="{TEN_SH}" opacity=".55"/>'
    # попона с узором — единственное красное пятно
    g += (f'<path d="M-96,-40 q82,-26 162,6 l-14,76 q-72,-26 -140,-4 Z" fill="{GRAN}" {o(6)}/>')
    for dy in (-18, 6):
        g += f'<path d="M-84,{dy} q76,22 142,-2" fill="none" stroke="{ZOL}" stroke-width="7"/>'
    # ноги с копытами
    for x0, x1 in ((-112, -120), (-46, -52), (40, 46), (104, 112)):
        g += f'<path d="M{x0},112 L{x1},216" {o(34, SHERST)}/>'
        g += f'<path d="M{x0},112 L{x1},216" {o(10, TEN_SH)}/>'
        g += f'<path d="M{x1-16},218 h32" {o(18, "#6b4634")}/>'
    # шея и голова
    g += f'<path d="M104,-14 L162,-104" {o(74, SHERST)}/>'
    g += f'<path d="M110,-6 L150,-70" {o(26, TEN_SH)}/>'
    g += f'<ellipse cx="180" cy="-128" rx="92" ry="74" fill="{SHERST}" {o(8)} transform="rotate(-14 180 -128)"/>'
    g += f'<ellipse cx="172" cy="-106" rx="76" ry="48" fill="{TEN_SH}" opacity=".4" transform="rotate(-14 172 -106)"/>'
    # морда, нос, борода
    g += f'<path d="M246,-140 q54,12 56,44 q-44,20 -78,0 Z" fill="#fff6e6" {o(6)}/>'
    g += f'<ellipse cx="292" cy="-104" rx="13" ry="9" fill="#8a6a52"/>'
    g += f'<path d="M268,-86 q14,10 26,2" fill="none" {o(4, "#9a7a62")}/>'
    g += f'<path d="M232,-70 q26,46 2,76 q-30,-28 -26,-74 Z" fill="#efe0c2" {o(5)}/>'
    # глаз: горизонтальный зрачок, блик, моргание
    shut = A.blink(t, 4.3, .15, .14)
    if shut:
        g += f'<path d="M184,-152 q18,14 36,0" fill="none" {o(6)}/>'
    else:
        g += (f'<ellipse cx="202" cy="-154" rx="20" ry="16" fill="#fff6e6" {o(5)}/>'
              f'<ellipse cx="202" cy="-154" rx="13" ry="7" fill="{K}"/>'
              f'<circle cx="196" cy="-160" r="4.5" fill="#ffffff"/>')
    # ухо и рога
    g += f'<ellipse cx="146" cy="-176" rx="44" ry="22" fill="{TEN_SH}" {o(6)} transform="rotate(-34 146 -176)"/>'
    g += f'<path d="M168,-186 C140,-230 96,-240 56,-214" fill="none" {o(19, "#e8d8b6")}/>'
    g += f'<path d="M196,-188 C176,-236 130,-250 92,-230" fill="none" {o(17, "#e0cfa8")}/>'
    # бубенец на шее
    g += (f'<path d="M118,-56 q58,20 110,2" fill="none" stroke="{KRAS}" stroke-width="14"/>'
          f'<circle cx="170" cy="-34" r="20" fill="url(#plg)" {o(5)}/>'
          f'<path d="M160,-30 h20" {o(4)}/>')
    return g + "</g>"


def frame(sc, t, gt):
    dur = sc["b"] - sc["a"]
    p = A.seg(t, 0, dur)
    pal = sc.get("pal", ["#7d1f2e", "#c9922f", "#3f8a4a"])
    bg = svg2img(L.LOK[sc.get("lok", "komnata")](gt, pal), kamera(sc, p)).convert("RGB")

    ox, oy, ow, oh = OKNO_LOK.get(sc.get("lok", "komnata"), OKNO)
    b = ""
    if sc.get("foto"):
        q = A.out(A.seg(t, .25, .5))
        if q > 0:
            path = sc["foto"]
            if sc.get("foto2") and t > dur * .55:
                path = sc["foto2"]
            iw, ih = int(ow * q), int(oh * q)
            if iw > 10 and ih > 10:
                bg.paste(cover(foto(path), iw, ih, p),
                         (int(ox + (ow - iw) / 2), int(oy + (oh - ih) / 2)))
            b += f'<g opacity="{q:.2f}">' + O.okno_ramka(ox, oy, ow, oh) + '</g>' 
    elif sc.get("stock"):
        # рамка проявляется ровно тогда, когда ffmpeg вводит клип: старт +0.8 с,
        # fade 0.3 с. Раньше рамка висела пустой (его правка 19).
        q = A.seg(t, .8, .3)
        if q > 0:
            b += f'<g opacity="{q:.2f}">' + O.okno_ramka(ox, oy, ow, oh) + '</g>'


    BIG = {"cards4", "cards5", "errors", "reveal", "glaz"}
    if sc.get("koza") and not any(e["kind"] in BIG for e in sc.get("events", [])):
        # хозяйка года держится весь смысловой отрезок, без мигания (правки 27-28);
        # но на крупный блок (карточки, ошибки, разгадка, глаз) она не лезет — правка 08.11
        gx = 330 + 50 * A.w(gt, 16.0)
        gy = 790 - 14 * A.w(gt, 3.0)
        b += koza_ognennaya(gx, gy, gt, .78)
    for e in sc.get("events", []):
        # отрезок: появление играется один раз, на стыке планов не повторяется
        t0 = e["a"] - sc["a"]
        k = e["kind"]
        if k == "zagolovok":
            b += O.nalив(120, 300, "КАК УКРАСИТЬ", t, t0, 64)
            b += O.nalив(120, 404, "ЁЛКУ 2027", t, t0 + .5, 92)
            q = A.out(A.seg(t, t0 + 1.4, .5))
            if q > 0:
                b += f'<rect x="116" y="440" width="{610*q:.0f}" height="11" rx="5" fill="{KRAS}"/>'
            b += O.pechat(120, 520, "чтобы год был счастливым", t, t0 + 2.0, 40)
        elif k == "plate":
            head, sub = TITLE.get(e.get("tema"), ("", ""))
            if head:
                b += O.plate(90, 900, head, sub, t, t0, 700)
        elif k == "palitra":
            cols, pod = PALS.get(e.get("tema"), PALS["vin"])
            b += O.palitra(140, 206, cols, pod, t, t0, .22, 38, 126)
        elif k == "obvodka" and sc.get("foto"):
            cx0, cy0, rx0, ry0 = e["box"]
            ex = ox + (cx0 / 1920) * ow
            ey = oy + (cy0 / 1080) * oh
            side = -1 if ex > ox + ow * .5 else 1
            b += O.obvodka(ex, ey, max(14, rx0 * ow / 1920), max(14, ry0 * oh / 1080),
                           e["pod"], t, t0, SVET, side, 20, size=24)

        elif k == "glaz":
            b += glaz(t, t0, gt)
        elif k == "cards5":
            b += cards5(t, t0)
        elif k == "ritual":
            b += O.card(620, 240, 700, 480, t, t0, "#1d1310", .93, SVET)
            b += O.txt(680, 340, "ОБРЯД", 50, SVET)
            b += O.spisok(680, 440, ["здоровье", "достаток", "ваше желание"], t, t0 + .4,
                          1.2, 40, 86, num=True)
        elif k == "reveal":
            b += O.zatemn(min(.7, .25 + max(0, t - t0) * .3))
            b += O.nalив(380, 540, "МИШУРА", t, t0, 200)
            if t > t0 + 2.2:
                b += O.txt(960, 690, "ВОТ ОНА", 90, "#ff6b6b", "middle")
        elif k == "errors":
            b += O.card(560, 240, 800, 480, t, t0, "#2e1618", .94, "#ff6b6b")
            b += O.txt(620, 340, "ОШИБКИ", 48, "#ff9d9d")
            b += O.spisok(620, 440, ["десять цветов", "холодный свет", "мишура поверх всего"],
                          t, t0 + .4, 1.4, 38, 84, strike=(0, 1, 2))
        elif k == "cards4":
            b += cards4(t, t0)
        elif k == "final":
            q = A.over(A.seg(t, t0, .5), 1.8)
            if q > 0:
                b += (f'<g transform="translate(960,900) scale({q:.2f}) translate(-960,-900)">'
                      f'<rect x="700" y="848" width="520" height="104" rx="52" fill="{KRAS}" {o(8)}/>'
                      + O.txt(960, 920, "ПОДПИСАТЬСЯ", 46, "#ffffff", "middle", O.SANS, 3, "bold")
                      + '</g>')
    b += O.vign()
    ov = svg2img(b)
    bg = bg.convert("RGBA")
    bg.alpha_composite(ov)
    return bg.convert("RGB")


def cards5(t, t0):
    s, pal = "", [["#7d1f2e", "#9c2740", "#c9922f"], ["#8a6b45", "#c9b58a", "#6d8a4a"],
                  ["#c9922f", "#d9cdb0", "#ffd36e"], ["#9c2740", "#b9743f", "#e4d4b6"],
                  ["#d6202f", "#7fd0ff", "#9ee07f"]]
    nm = ["винная", "природная", "металлик", "семейная", "?"]
    for i in range(5):
        q = A.over(A.seg(t, t0 + i * .42, .4), 1.5)
        if q <= 0:
            continue
        x = 90 + i * 360
        s += (f'<g transform="translate({x+160},560) scale({q:.2f}) translate({-(x+160)},-560)">'
              f'<rect x="{x}" y="340" width="320" height="440" rx="20" fill="#1d1310"'
              f' opacity=".94" stroke="{"#ff6b6b" if i == 4 else ZOL}" stroke-width="5"/>')
        if i < 4:
            s += tree(x + 160, 700, 250, pal[i], bows_on=False)
            s += O.txt(x + 160, 750, nm[i], 28, KREM, "middle", O.SANS, 1, "600")
        else:
            s += O.txt(x + 160, 620, "?", 170, SVET, "middle")
        s += "</g>"
    return s


def cards4(t, t0):
    s = O.txt(960, 150, "КАКАЯ ВАША?", 64, "#ffffff", "middle")
    pal = [["#7d1f2e", "#9c2740", "#c9922f"], ["#8a6b45", "#c9b58a", "#6d8a4a"],
           ["#c9922f", "#d9cdb0", "#ffd36e"], ["#9c2740", "#b9743f", "#e4d4b6"]]
    for i in range(4):
        q = A.over(A.seg(t, t0 + i * .4, .4), 1.5)
        if q <= 0:
            continue
        x = 110 + i * 440
        s += (f'<g transform="translate({x+200},560) scale({q:.2f}) translate({-(x+200)},-560)">'
              f'<rect x="{x}" y="300" width="400" height="420" rx="20" fill="#1d1310"'
              f' opacity=".94" stroke="{ZOL}" stroke-width="5"/>')
        s += tree(x + 200, 660, 250, pal[i], bows_on=False)
        s += (f'<circle cx="{x+200}" cy="370" r="44" fill="{ZOL}" {o(6)}/>'
              f'<text x="{x+200}" y="388" text-anchor="middle" font-family="{O.SERIF}"'
              f' font-size="50" font-weight="bold" fill="#17130f">{i+1}</text></g>')
    return s


def glaz(t, t0, gt):
    """Крупный план глаза: горизонтальный зрачок, отражение комнаты, сектор
    обзора почти на весь круг. Его правка 23 — «нужен Голливуд»."""
    p = A.out(A.seg(t, t0, .8))
    if p <= 0:
        return ""
    cx, cy = 820, 540
    rx, ry = 430 * p, 300 * p
    s = f'<rect width="{W}" height="{H}" fill="#120c0a" opacity="{.82*p:.2f}"/>'
    # сектор обзора
    q = A.out(A.seg(t, t0 + 1.2, 1.4))
    if q > 0:
        import math as _m
        a0, a1 = -_m.pi * .96 * q, _m.pi * .96 * q
        x0, y0 = cx + 900 * _m.cos(a0), cy + 760 * _m.sin(a0)
        x1, y1 = cx + 900 * _m.cos(a1), cy + 760 * _m.sin(a1)
        s += (f'<path d="M{cx},{cy} L{x0:.0f},{y0:.0f} A900,760 0 {1 if q>.5 else 0} 1'
              f' {x1:.0f},{y1:.0f} Z" fill="{SVET}" opacity="{.12*q:.2f}"/>')
    # веко и глазное яблоко
    s += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:.0f}" ry="{ry:.0f}" fill="#fff6e6" {o(12)}/>')
    # радужка
    s += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*.52:.0f}" ry="{ry*.72:.0f}"'
          f' fill="#b07a3a" {o(8)}/>')
    for i in range(26):
        import math as _m
        a = i * (2 * _m.pi / 26)
        s += (f'<path d="M{cx + rx*.14*_m.cos(a):.0f},{cy + ry*.2*_m.sin(a):.0f}'
              f' L{cx + rx*.5*_m.cos(a):.0f},{cy + ry*.7*_m.sin(a):.0f}"'
              f' stroke="#d9a35c" stroke-width="5" opacity=".6"/>')
    # горизонтальный зрачок
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*.40:.0f}" ry="{ry*.17:.0f}" fill="#120c0a"/>'
    # ОТРАЖЕНИЕ комнаты в зрачке: ёлка, огоньки, окно
    s += (f'<g opacity=".55"><rect x="{cx-rx*.34:.0f}" y="{cy-ry*.1:.0f}"'
          f' width="{rx*.68:.0f}" height="{ry*.2:.0f}" fill="#2a1a18"/>')
    s += tree(cx - rx * .12, cy + ry * .09, ry * .17, [VIN, ZOL, KRAS], bows_on=False, star=False)
    for i in range(5):
        gx = cx - rx * .3 + i * rx * .15
        op = .4 + .6 * abs(A.w(gt, 1.4, i * .2))
        s += f'<circle cx="{gx:.0f}" cy="{cy - ry*.02:.0f}" r="4" fill="{SVET}" opacity="{op:.2f}"/>'
    s += '</g>'
    # блик
    s += (f'<ellipse cx="{cx-rx*.3:.0f}" cy="{cy-ry*.42:.0f}" rx="{rx*.14:.0f}"'
          f' ry="{ry*.16:.0f}" fill="#ffffff" opacity=".85"/>')
    # веки моргают
    if A.blink(gt, 3.6, .1, .18):
        s += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx+10:.0f}" ry="{ry+10:.0f}" fill="#e8c9a0"/>'
              f'<path d="M{cx-rx:.0f},{cy} q{rx:.0f},40 {rx*2:.0f},0" fill="none" {o(10)}/>')
    if q > .8:
        s += O.txt(1480, 520, "почти", 56, SVET, "middle")
        s += O.txt(1480, 620, "340°", 120, "#ffffff", "middle")
        s += O.pechat(1300, 720, "видит вокруг себя", t, t0 + 2.6, 38)
    return s
