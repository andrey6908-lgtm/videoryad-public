# -*- coding: utf-8 -*-
"""Восемь эффектов появления текста, КАЖДЫЙ — функция времени.
Рисуются внутри кадра, а не кладутся сверху готовой картинкой: именно
поэтому они живут. Ширина и высота МЕРЯЮТСЯ ШРИФТОМ (правило №3 «Козы»).
Обводка — отдельным слоем: cairosvg не понимает paint-order."""
import anim as A
from PIL import ImageFont

K = "#17130f"
SVET, ZOL, ORA = "#ffd36e", "#c9922f", "#e07f23"
KRAS, KREM, SER = "#d6202f", "#e4d4b6", "#eef2f7"

DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = DIR + "DejaVuSerif-Bold.ttf"
SANS = DIR + "DejaVuSans.ttf"
SANSB = DIR + "DejaVuSans-Bold.ttf"
FAM = {SERIF: "DejaVu Serif, Georgia, serif",
       SANS: "DejaVu Sans, Segoe UI, sans-serif",
       SANSB: "DejaVu Sans, Segoe UI, sans-serif"}

_fc = {}
_uid = [0]


def _font(path, size):
    key = (path, int(size))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(path, int(size))
    return _fc[key]


def wid(text, path, size, ls=0.0):
    """Ширина строки шрифтом, с учётом межбуквенного. Не прикидка."""
    return _font(path, size).getlength(text) + ls * max(0, len(text))


def uid(tag):
    _uid[0] += 1
    return "%s%d" % (tag, _uid[0])


def txt(x, y, t, size, fill="#ffffff", path=SERIF, ls=2, anchor="start",
        stroke=None, op=1.0, extra=""):
    """Текст с обводкой отдельным слоем. Толщина обводки — ДОЛЯ КЕГЛЯ:
    постоянные 11 px съедали букву на титре 44 px (титр выходил серым)."""
    if stroke is None:
        stroke = max(3.0, size * 0.085)
    base = (f'font-family="{FAM[path]}" font-size="{size:.1f}"'
            f' font-weight="{"bold" if path != SANS else "600"}" letter-spacing="{ls}"'
            f' text-anchor="{anchor}" x="{x:.1f}" y="{y:.1f}" {extra}')
    s = ""
    if stroke:
        s += (f'<text {base} fill="none" stroke="{K}" stroke-width="{stroke}"'
              f' stroke-linejoin="round" opacity="{0.85*op:.2f}">{t}</text>')
    return s + f'<text {base} fill="{fill}" opacity="{op:.2f}">{t}</text>'


# ─────────────── 1 · ЛУННЫЙ НАЛИВ ───────────────
def naliv(x, y, s, t, t0, size=132, dur=1.5, ls=2, path=SERIF):
    """Буквы стоят контуром и наливаются лунным светом снизу вверх."""
    p = A.ease(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    cid = uid("nal")
    top, bot = y - size * 0.82, y + size * 0.26
    hh = (bot - top) * p
    s_out = txt(x, y, s, size, "none", path, ls, stroke=size*0.09, op=1.0)
    glow = (f'<text font-family="{FAM[path]}" font-size="{size:.1f}" font-weight="bold"'
            f' letter-spacing="{ls}" x="{x:.1f}" y="{y:.1f}" fill="none" stroke="{SVET}"'
            f' stroke-width="{10*(1-p)+3:.1f}" opacity="{0.25+0.45*p:.2f}">{s}</text>')
    fill = (f'<clipPath id="{cid}"><rect x="{x-40:.0f}" y="{bot-hh:.1f}"'
            f' width="{wid(s, path, size, ls)+90:.0f}" height="{hh+2:.1f}"/></clipPath>'
            f'<g clip-path="url(#{cid})">'
            f'<text font-family="{FAM[path]}" font-size="{size:.1f}" font-weight="bold"'
            f' letter-spacing="{ls}" x="{x:.1f}" y="{y:.1f}" fill="#ffffff">{s}</text></g>')
    return s_out + glow + fill


# ─────────────── 2 · ПЕЧАТЬ ───────────────
def pechat(x, y, s, t, t0, size=40, cps=19, fill="#dfe6f4", path=SANS, ls=1):
    """Печатная машинка: символы набегают, курсор мигает и исчезает."""
    if t < t0:
        return ""
    n = int((t - t0) * cps)
    if n <= 0:
        return ""
    part = s[:n]
    out = txt(x, y, part, size, fill, path, ls)
    done = n >= len(s)
    if not done or (t - t0 - len(s) / cps) < 0.7:
        if ((t * 2) % 1.0) < 0.6:
            cx = x + wid(part, path, size, ls) + 6
            out += (f'<rect x="{cx:.1f}" y="{y-size*0.78:.1f}" width="{size*0.09:.1f}"'
                    f' height="{size*0.95:.1f}" fill="{SVET}" opacity=".9"/>')
    return out


# ─────────────── 3 · ПЛАШКА-МАСКА ───────────────
def plashka(x, y, head, sub, t, t0, dur=0.9):
    """Золотая плашка темы раскрывается слева направо, текст — за ней."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    hw = max(wid(head, SERIF, 38, 1) * 1.02, wid(sub, SANS, 20, 1) * 1.06 if sub else 0) + 54
    W, H = hw, (86 if sub else 62)
    cid = uid("pl")
    g = (f'<clipPath id="{cid}"><rect x="{x:.0f}" y="{y-8:.0f}" width="{W*p:.1f}"'
         f' height="{H+16:.0f}"/></clipPath><g clip-path="url(#{cid})">')
    g += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{W:.0f}" height="{H}" rx="6" fill="url(#plg)"/>'
          f'<text x="{x+26:.0f}" y="{y+45:.0f}" font-family="{FAM[SERIF]}" font-size="38"'
          f' font-weight="bold" fill="#17130f" letter-spacing="1">{head}</text>')
    if sub:
        g += (f'<text x="{x+26:.0f}" y="{y+75:.0f}" font-family="{FAM[SANS]}" font-size="20"'
              f' fill="#3a2a12" letter-spacing="1">{sub}</text>')
    g += '</g>'
    if p < 1:                       # светящийся край маски — видно, что она едет
        g += (f'<rect x="{x+W*p-5:.1f}" y="{y:.0f}" width="7" height="{H}" fill="{SVET}"'
              f' opacity=".85"/>')
    return g


# ─────────────── 4 · ПАДЕНИЕ СЛОВ ───────────────
def padenie(x, y, words, t, t0, size=96, step=0.2, fall=0.45, ls=2, fill="#ffffff",
            path=SERIF, gap=26):
    """Слова падают сверху по очереди и встают с лёгким перелётом."""
    out, cx = "", x
    for i, word in enumerate(words):
        p = A.seg(t, t0 + i * step, fall)
        if p > 0:
            k = A.over(p, 1.55)
            dy = -300 * (1 - k)
            rot = -7 * (1 - k)
            out += (f'<g transform="translate({cx:.1f},{y+dy:.1f}) rotate({rot:.2f})">'
                    + txt(0, 0, word, size, fill, path, ls) + '</g>')
        cx += wid(word, path, size, ls) + gap
    return out


def padenie_width(words, size=96, ls=2, path=SERIF, gap=26):
    return sum(wid(x, path, size, ls) for x in words) + gap * (len(words) - 1)


# ─────────────── 5 · ЗАЧЁРКИВАНИЕ ───────────────
def zacherk(x, y, width, t, t0, dur=0.5, col=KRAS, th=13):
    """Красная черта проезжает по строке — запрет закрывается на глазах."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    ln = width * p
    s = (f'<path d="M{x:.0f},{y:.0f} q{ln*0.5:.1f},{-7-4*p:.1f} {ln:.1f},{2:.0f}"'
         f' fill="none" stroke="{col}" stroke-width="{th}" stroke-linecap="round"/>')
    if p > 0.45:                    # вторая, короткая — рука не линейка
        l2 = width * (p - 0.45) / 0.55 * 0.82
        s += (f'<path d="M{x+width*0.08:.0f},{y+11:.0f} q{l2*0.5:.1f},6 {l2:.1f},-3"'
              f' fill="none" stroke="{col}" stroke-width="{th*0.55:.1f}"'
              f' stroke-linecap="round" opacity=".75"/>')
    return s


# ─────────────── 6 · РОСЧЕРК ───────────────
def roscherk(x, y, width, t, t0, dur=0.7, col=SVET, th=9):
    """Подчёркивание рисуется рукой: волна с завитком на конце."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    n = max(2, int(44 * p))
    pts = []
    for i in range(n + 1):
        u = (i / 44.0)
        px = x + width * u
        py = y + 13 * A.w(u * 1.0, 0.5) * (1 - u * 0.4)
        if u > 0.86:                # завиток
            k = (u - 0.86) / 0.14
            px += 26 * k
            py -= 34 * k * k
        pts.append("%.1f,%.1f" % (px, py))
    return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}"'
            f' stroke-width="{th}" stroke-linecap="round" stroke-linejoin="round"/>')


# ─────────────── 7 · ШТАМП ───────────────
def shtamp(cx, cy, s, t, t0, size=64, col="#9ee07f", dur=0.3):
    """Штамп прилетает с перелётом, бьёт по кадру и мелко дрожит."""
    p = A.seg(t, t0, dur)
    if p <= 0:
        return ""
    k = A.over(p, 2.2) if p < 1 else 1.0
    sc = 2.4 - 1.4 * k
    sh = 0 if p < 1 else 1.3 * A.w(t - t0 - dur, 0.22) * max(0.0, 1 - (t - t0 - dur) / 0.5)
    w = wid(s, SERIF, size, 6) + 56
    h = size * 1.62
    op = min(1.0, p * 3)
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({-6+sh:.2f})'
            f' scale({sc:.3f}) translate({-cx:.1f},{-cy:.1f})" opacity="{op:.2f}">'
            f'<rect x="{cx-w/2:.1f}" y="{cy-h*0.72:.1f}" width="{w:.1f}" height="{h:.1f}"'
            f' rx="9" fill="none" stroke="{col}" stroke-width="7"/>'
            f'<rect x="{cx-w/2+11:.1f}" y="{cy-h*0.72+11:.1f}" width="{w-22:.1f}"'
            f' height="{h-22:.1f}" rx="5" fill="none" stroke="{col}" stroke-width="3"'
            f' opacity=".7"/>'
            + txt(cx, cy + size * 0.2, s, size, col, SERIF, 6, "middle")
            + '</g>')


# ─────────────── 8 · ЛЕНТА-РАЗДЕЛИТЕЛЬ ───────────────
def lenta(y, s, t, t0, W=1920, h=96, dur=0.75, size=44):
    """Две половины ленты съезжаются к центру, титр проявляется в стыке."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    half = W / 2
    off = half * (1 - p)
    g = ""
    for sgn in (-1, 1):
        x = (0 - off) if sgn < 0 else (half + off)
        g += (f'<rect x="{x:.1f}" y="{y:.0f}" width="{half:.0f}" height="{h}" fill="#22304a"'
              f' opacity=".96"/>'
              f'<rect x="{x:.1f}" y="{y:.0f}" width="{half:.0f}" height="5" fill="{ZOL}"/>'
              f'<rect x="{x:.1f}" y="{y+h-5:.0f}" width="{half:.0f}" height="5" fill="{ZOL}"/>')
    if p >= 1:
        q = A.ease(A.seg(t, t0 + dur, 0.45))
        g += txt(W / 2, y + h * 0.66, s, size, "#ffffff", SANS,
                 2 + 10 * q, "middle", op=q)
    return g
