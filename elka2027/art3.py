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
    """Хозяйка года: крупная, с ОГНЕННОЙ гривой по хребту и шее, свечение.
    2027 — год Красной Огненной Козы, поэтому пламя, а не бежевые палки."""
    g = f'<g transform="translate({cx:.0f},{cy:.0f}) scale({s:.3f})">'
    g += f'<ellipse cx="10" cy="-30" rx="300" ry="230" fill="url(#teplo)" opacity=".8"/>'
    # пламя по хребту: языки вверх, разной высоты, живые
    for i in range(10):
        bx = -140 + i * 34
        hh = (120 + 60 * abs(math.sin(i * 1.1))) * (1 + .22 * A.w(t, .9, i * .13))
        dx = 18 * A.w(t, 1.5, i * .2)
        col = [ORA, SVET, KRAS][i % 3]
        g += (f'<path d="M{bx},-60 C{bx-24},{-60-hh*.4:.0f} {bx-8+dx:.0f},{-60-hh*.7:.0f}'
              f' {bx+dx:.0f},{-60-hh:.0f} C{bx+20+dx:.0f},{-60-hh*.65:.0f}'
              f' {bx+26},{-60-hh*.35:.0f} {bx},-60 Z" fill="{col}"'
              f' opacity="{.65+.3*abs(A.w(t,1.1,i*.17)):.2f}"/>')
    # тело
    g += f'<ellipse cx="-20" cy="40" rx="160" ry="108" fill="{KRAS}" {o(8)}/>'
    for dy in (0, 38, 76):
        g += f'<path d="M-118,{dy} q98,32 196,0" fill="none" stroke="{ZOL}" stroke-width="9" opacity=".9"/>'
    for x0, x1 in ((-104, -112), (-40, -46), (36, 42), (98, 106)):
        g += f'<path d="M{x0},132 L{x1},244" {o(24, TERRA)}/>'
        g += f'<path d="M{x1-12},244 h24" {o(14, K)}/>'
    # хвост
    g += f'<path d="M-176,-10 q-40,-16 -46,-54" fill="none" {o(18, KRAS)}/>'
    # шея и голова
    g += f'<path d="M96,-10 L150,-96" {o(58, KRAS)}/>'
    g += f'<ellipse cx="168" cy="-120" rx="86" ry="70" fill="{KRAS}" {o(8)} transform="rotate(-14 168 -120)"/>'
    # морда и борода
    g += f'<path d="M226,-128 q56,8 60,40 q-44,20 -76,2 Z" fill="{KREM}" {o(6)}/>'
    g += f'<circle cx="276" cy="-96" r="10" fill="{K}"/>'
    g += f'<path d="M222,-68 q18,56 -20,76 q-18,-48 -6,-76 Z" fill="{KREM}" {o(6)}/>'
    g += f'<circle cx="186" cy="-142" r="13" fill="{K}"/>'
    g += f'<circle cx="190" cy="-146" r="4.5" fill="#ffffff"/>'
    # ухо и рога назад
    g += f'<ellipse cx="132" cy="-168" rx="42" ry="22" fill="{GRAN}" {o(6)} transform="rotate(-32 132 -168)"/>'
    g += f'<path d="M150,-182 q-20,-70 -96,-104" fill="none" {o(16, KREM)}/>'
    g += f'<path d="M172,-186 q-8,-74 -74,-116" fill="none" {o(16, KREM)}/>'
    # пламя у головы
    for i in range(4):
        bx = 120 + i * 26
        hh = 70 * (1 + .3 * A.w(t, 1.0, i * .2))
        g += (f'<path d="M{bx},-186 q-10,{-hh*.6:.0f} 6,{-hh:.0f} q18,{hh*.5:.0f} -6,{hh:.0f} Z"'
              f' fill="{[SVET, ORA][i%2]}" opacity="{.55+.35*abs(A.w(t,.8,i*.2)):.2f}"/>')
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
            iw, ih = int(ow * q), int(oh * q)
            if iw > 10 and ih > 10:
                bg.paste(cover(foto(sc["foto"]), iw, ih, p),
                         (int(ox + (ow - iw) / 2), int(oy + (oh - ih) / 2)))
            b += O.okno_ramka(ox, oy, ow, oh)
    elif sc.get("stock"):
        b += O.okno_ramka(ox, oy, ow, oh)

    for e in sc.get("events", []):
        t0 = e["t"] - sc["a"]
        k = e["kind"]
        if k == "zagolovok":
            b += O.nalив(120, 300, "КАК УКРАСИТЬ", t, t0, 86)
            b += O.nalив(120, 410, "ЁЛКУ 2027", t, t0 + .5, 112)
            q = A.out(A.seg(t, t0 + 1.4, .5))
            if q > 0:
                b += f'<rect x="116" y="450" width="{560*q:.0f}" height="11" rx="5" fill="{KRAS}"/>'
            b += O.pechat(120, 520, "чтобы год был счастливым", t, t0 + 2.0, 40)
        elif k == "plate":
            head, sub = TITLE.get(e.get("tema"), ("", ""))
            if head:
                b += O.plate(90, 900, head, sub, t, t0, 700)
        elif k == "palitra":
            cols, pod = PALS.get(e.get("tema"), PALS["vin"])
            b += O.palitra(140, 260, cols, pod, t, t0, .22, 38, 126)
        elif k == "obvodka" and sc.get("foto"):
            cx0, cy0, rx0, ry0 = e["box"]
            ex = ox + (cx0 / 1920) * ow
            ey = oy + (cy0 / 1080) * oh
            side = -1 if ex > ox + ow * .5 else 1
            b += O.obvodka(ex, ey, max(14, rx0 * ow / 1920), max(14, ry0 * oh / 1080),
                           e["pod"], t, t0, SVET, side, 20, size=24)
        elif k == "goat":
            q = A.out(A.seg(t, t0, .6))
            if q > 0:
                gx = 760 + 90 * A.ease(A.seg(t, t0, 4.0))
                gy = 720 - 22 * A.w(t, 3.0)
                b += koza_ognennaya(gx, gy, gt, 1.15 * q)
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
