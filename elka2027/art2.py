# -*- coding: utf-8 -*-
"""Кадр ролика «Ёлка 2027», версия 07.11 после его разбора.

Четыре правила, которые тут зашиты:
  1) генерация живёт ТОЛЬКО в окне и ТОЛЬКО пока о ней говорят;
  2) всё появляется в ту секунду, когда звучит слово (события из words.json);
  3) камера ходит по самой сцене — viewBox, а не только наезд по фото;
  4) кадр живой: шары качаются, гирлянда мигает, огонь в камине, снег.
"""
import io, math, os
import cairosvg
from PIL import Image
import anim as A
import over as O
import scena as SC
from ng import *

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
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
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
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
    """Окно просмотра сцены: наезд, панорама, кран — движение непрерывное."""
    z = sc.get("z0", 1.0) + (sc.get("z1", 1.1) - sc.get("z0", 1.0)) * A.ease(p)
    cx, cy = sc.get("cx", .5), sc.get("cy", .5)
    if sc.get("cam") == "pan":
        cx = cx + .22 * (p - .5)
    if sc.get("cam") == "crane":
        cy = cy - .24 * A.ease(p)
    if sc.get("cam") == "arc":
        cx = cx - .14 * A.ease(p)
        cy = cy + .05 * A.ease(p)
    if sc.get("cam") == "tilt":
        cy = cy - .18 * A.ease(p)
    vw, vh = W / z, H / z
    vx = min(max(0.0, cx * W - vw / 2), W - vw)
    vy = min(max(0.0, cy * H - vh / 2), H - vh)
    return vx, vy, vw, vh


def frame(sc, t, gt):
    dur = sc["b"] - sc["a"]
    p = A.seg(t, 0, dur)
    vb = kamera(sc, p)
    pal = sc.get("pal", ["#7d1f2e", "#c9922f", "#3f8a4a"])
    # ── фон: живая комната, камера ходит по ней
    bg = svg2img(SC.komnata(gt, pal), vb).convert("RGB")

    # ── окно вставки: фото темы или живой сток. Координаты — экранные,
    #    поэтому пересчитываем через то же окно просмотра.
    vx, vy, vw, vh = vb
    kx, ky = W / vw, H / vh
    ox, oy, ow, oh = SC.OKNO
    sx, sy = (ox - vx) * kx, (oy - vy) * ky
    sw, sh = ow * kx, oh * ky
    b = ""
    showing = sc.get("foto") or sc.get("stock")
    if showing:
        poyav = A.out(A.seg(t, .25, .5))
        if poyav > 0:
            if sc.get("foto"):
                im, box = kbf(sc["foto"], p)
                iw, ih = int(sw * poyav), int(sh * poyav)
                if iw > 8 and ih > 8:
                    mx, my = int(sx + (sw - iw) / 2), int(sy + (sh - ih) / 2)
                    if -iw < mx < W and -ih < my < H:
                        bg.paste(im.resize((iw, ih), Image.BILINEAR), (mx, my))
                sc["_box"] = box
            b += O.okno_ramka(sx, sy, sw, sh)

    # ── события: всё строго в свою секунду
    for e in sc.get("events", []):
        t0 = e["t"] - sc["a"]
        k = e["kind"]
        if k == "plate":
            head, sub = TITLE.get(e.get("tema"), ("", ""))
            if head:
                b += O.plate(90, 90, head, sub, t, t0, 700)
        elif k == "palitra":
            cols, pod = PALS.get(e.get("tema"), PALS["vin"])
            b += O.palitra(140, 300, cols, pod, t, t0, .22, 38, 126)
        elif k == "obvodka" and sc.get("foto") and sc.get("_box"):
            bx, by, bw, bh = sc["_box"]
            cx0, cy0, rx0, ry0 = e["box"]
            ex = sx + (cx0 - bx) * sw / bw
            ey = sy + (cy0 - by) * sh / bh
            if sx - 40 < ex < sx + sw + 40:
                side = -1 if ex > sx + sw * .5 else 1
                b += O.obvodka(ex, ey, max(16, rx0 * sw / bw), max(16, ry0 * sh / bh),
                               e["pod"], t, t0, SVET, side, 24, size=26)
        elif k == "zagolovok":
            b += O.nalив(1010, 330, "КАК УКРАСИТЬ", t, t0, 74)
            b += O.nalив(1010, 430, "ЁЛКУ 2027", t, t0 + .5, 96)
            q = A.out(A.seg(t, t0 + 1.4, .5))
            if q > 0:
                b += (f'<rect x="1006" y="466" width="{500*q:.0f}" height="10" rx="5"'
                      f' fill="{KRAS}"/>')
            b += O.pechat(1010, 528, "чтобы год был счастливым", t, t0 + 2.0, 36)
        elif k == "goat":
            q = A.out(A.seg(t, t0, .6))
            if q > 0:
                gy = 820 - 40 * A.w(t, 3.2)
                b += koza(300 + 40 * A.ease(A.seg(t, t0, 3.0)), gy, .85 * q)
        elif k == "cards5":
            b += lenta5(t, t0)
        elif k == "ritual":
            b += O.card(90, 560, 640, 400, t, t0, "#1d1310", .92, SVET)
            b += O.txt(140, 650, "ОБРЯД", 46, SVET)
            b += O.spisok(140, 730, ["здоровье", "достаток", "ваше желание"], t, t0 + .4,
                          1.2, 36, 76, num=True)
        elif k == "reveal":
            b += O.zatemn(min(.7, .25 + (t - t0) * .3) if t > t0 else 0)
            b += O.nalив(380, 520, "МИШУРА", t, t0, 190)
            if t > t0 + 2.2:
                b += O.txt(960, 660, "ВОТ ОНА", 86, "#ff6b6b", "middle")
        elif k == "errors":
            b += O.card(90, 520, 700, 420, t, t0, "#2e1618", .93, "#ff6b6b")
            b += O.txt(140, 610, "ОШИБКИ", 44, "#ff9d9d")
            b += O.spisok(140, 700, ["десять цветов", "холодный свет", "мишура поверх всего"],
                          t, t0 + .4, 1.4, 34, 74, strike=(0, 1, 2))
        elif k == "cards4":
            b += cards4(t, t0)
        elif k == "final":
            q = A.over(A.seg(t, t0, .5), 1.8)
            if q > 0:
                b += (f'<g transform="translate(960,980) scale({q:.2f}) translate(-960,-980)">'
                      f'<rect x="700" y="928" width="520" height="104" rx="52" fill="{KRAS}" {o(8)}/>'
                      + O.txt(960, 1000, "ПОДПИСАТЬСЯ", 46, "#ffffff", "middle", O.SANS, 3, "bold")
                      + '</g>')
    b += O.sneg(gt, 26, 6)
    b += O.vign()
    ov = svg2img(b)
    bg = bg.convert("RGBA")
    bg.alpha_composite(ov)
    return bg.convert("RGB")


def kbf(path, p):
    """Лёгкий наезд ВНУТРИ окна — содержимое вставки тоже живёт."""
    im = foto(path)
    z = 1.0 + .10 * A.ease(p)
    cw, ch = W / z, H / z
    x = (W - cw) / 2
    y = (H - ch) / 2
    return im.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch)), (x, y, cw, ch)


def lenta5(t, t0):
    """Пять ёлок лентой внизу кадра — ровно на словах «покажу вам пять ёлок»."""
    s = ""
    pal = [["#7d1f2e", "#9c2740", "#c9922f"], ["#8a6b45", "#c9b58a", "#6d8a4a"],
           ["#c9922f", "#d9cdb0", "#ffd36e"], ["#9c2740", "#b9743f", "#e4d4b6"],
           ["#d6202f", "#7fd0ff", "#9ee07f"]]
    nm = ["винная", "природная", "металлик", "семейная", "?"]
    for i in range(5):
        q = A.over(A.seg(t, t0 + i * .45, .4), 1.5)
        if q <= 0:
            continue
        x = 120 + i * 350
        s += (f'<g transform="translate({x+150},860) scale({q:.2f}) translate({-(x+150)},-860)">'
              f'<rect x="{x}" y="700" width="300" height="320" rx="18" fill="#1d1310"'
              f' opacity=".93" stroke="{"#ff6b6b" if i == 4 else ZOL}" stroke-width="5"/>')
        if i < 4:
            s += tree(x + 150, 960, 200, pal[i], bows_on=False)
            s += O.txt(x + 150, 1000, nm[i], 26, KREM, "middle", O.SANS, 1, "600")
        else:
            s += O.txt(x + 150, 920, "?", 150, SVET, "middle")
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
