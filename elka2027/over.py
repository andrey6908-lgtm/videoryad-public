# -*- coding: utf-8 -*-
"""Наложения ролика «Ёлка 2027»: плашки, палитры, обводки, карточки, титры.
Каждое — ФУНКЦИЯ ВРЕМЕНИ: появляется, живёт, уходит. Рисуется поверх кадра."""
import anim as A
from ng import *

W, H = 1920, 1080
SANS = "DejaVu Sans, Segoe UI, sans-serif"
SERIF = "DejaVu Serif, Georgia, serif"


def defs_all():
    return defs()


def txt(x, y, t, size=64, col="#ffffff", anchor="start", font=SERIF, ls=2,
        weight="bold", stroke=None, op=1.0):
    st = stroke if stroke is not None else max(3, size * .09)
    base = (f'font-family="{font}" font-size="{size:.1f}" font-weight="{weight}"'
            f' letter-spacing="{ls}" text-anchor="{anchor}" x="{x:.1f}" y="{y:.1f}"')
    s = ""
    if st:
        s += (f'<text {base} fill="none" stroke="{K}" stroke-width="{st:.1f}"'
              f' stroke-linejoin="round" opacity="{0.9*op:.2f}">{t}</text>')
    return s + f'<text {base} fill="{col}" opacity="{op:.2f}">{t}</text>'


def nalив(x, y, s, t, t0, size=130, dur=1.6, font=SERIF):
    """Титр наливается золотом снизу вверх."""
    p = A.ease(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    top, bot = y - size * .82, y + size * .26
    hh = (bot - top) * p
    cid = "nal%d" % int((x + y + size) % 9999)
    base = (f'font-family="{font}" font-size="{size}" font-weight="bold"'
            f' letter-spacing="2" x="{x}" y="{y}"')
    out = (f'<text {base} fill="none" stroke="{K}" stroke-width="{size*0.1:.0f}"'
           f' stroke-linejoin="round" opacity=".9">{s}</text>')
    out += (f'<text {base} fill="none" stroke="{SVET}" stroke-width="{10*(1-p)+3:.1f}"'
            f' opacity="{0.25+0.5*p:.2f}">{s}</text>')
    out += (f'<clipPath id="{cid}"><rect x="{x-60}" y="{bot-hh:.1f}" width="2400"'
            f' height="{hh+2:.1f}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><text {base} fill="{SVET}">{s}</text></g>')
    return out


def pechat(x, y, s, t, t0, size=40, cps=20, col="#f0e4d2"):
    if t < t0:
        return ""
    n = int((t - t0) * cps)
    if n <= 0:
        return ""
    return txt(x, y, s[:n], size, col, font=SANS, ls=1, weight="600")


def plate(x, y, head, sub, t, t0, w=660, dur=.7):
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    h = 86 if sub else 62
    cid = "pl%d" % int((x + y) % 9999)
    s = (f'<clipPath id="{cid}"><rect x="{x}" y="{y-8}" width="{w*p:.1f}" height="{h+16}"/>'
         f'</clipPath><g clip-path="url(#{cid})">')
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="url(#plg)"/>'
    s += (f'<text x="{x+26}" y="{y+45}" font-family="{SERIF}" font-size="38"'
          f' font-weight="bold" fill="#17130f" letter-spacing="1">{head}</text>')
    if sub:
        s += (f'<text x="{x+26}" y="{y+75}" font-family="{SANS}" font-size="20"'
              f' fill="#3a2a12" letter-spacing="1">{sub}</text>')
    s += "</g>"
    if p < 1:
        s += f'<rect x="{x+w*p-5:.1f}" y="{y}" width="7" height="{h}" fill="{SVET}" opacity=".85"/>'
    return s


def palitra(x, y, cols, pod, t, t0, step=.25, r=44, dx=148):
    # подложка: без неё подписи тонут в декорации (его правка 08.11 по камину)
    k0 = A.over(A.seg(t, t0, .45), 1.6)
    s = ""
    if k0 > 0:
        bx, by = x - r - 26, y - r - 20
        bw = (len(cols) - 1) * dx + 2 * r + 52
        bh = 2 * r + 86
        s += (f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="22" '
              f'fill="#120d0b" opacity="{.74 * min(1.0, k0):.2f}"/>')
    for i, (c, p) in enumerate(zip(cols, pod)):
        k = A.over(A.seg(t, t0 + i * step, .45), 1.6)
        if k <= 0:
            continue
        cx = x + i * dx
        s += f'<circle cx="{cx}" cy="{y}" r="{r*k:.1f}" fill="{c}" {o(6)}/>'
        if k > .9:
            _b = (f'font-family="{SANS}" font-size="30" font-weight="500"'
                  f' letter-spacing="1" text-anchor="middle" x="{cx}" y="{y+r+42}"')
            s += (f'<text {_b} fill="none" stroke="{K}" stroke-width="6"'
                  f' stroke-linejoin="round" opacity=".9">{p}</text>'
                  f'<text {_b} fill="#ffffff">{p}</text>')
    return s


def obvodka(cx, cy, rx, ry, pod, t, t0, col=SVET, side=1, dx=160, dur=.6, size=34,
            life=8.5, lim=None):
    """Обводка рисуется по кругу, затем выноска и подпись."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    fade = 1.0 - A.ease(A.seg(t, t0 + life, .6))
    if fade <= 0.01:
        return ""
    per = 2 * 3.1416 * ((rx + ry) / 2)
    s = (f'<g opacity="{fade:.2f}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none"'
         f' stroke="{col}" stroke-width="7" stroke-dasharray="{per*p:.0f} {per:.0f}"'
         f' transform="rotate(-90 {cx} {cy})"/>')
    q = A.out(A.seg(t, t0 + dur, .4))
    if q > 0:
        lx = cx + (rx + dx) * side
        anc = "start" if side > 0 else "end"
        s += (f'<path d="M{cx + rx*side},{cy} L{cx + (rx + dx*q)*side:.0f},{cy-40*q:.0f}"'
              f' stroke="{col}" stroke-width="5"/>')
        if q > .8:
            # подложка под подпись: на светлом фото светлый текст не читался
            # подложка с запасом, текст — по её центру: иначе хвост надписи
            # вылезал за фон и за край окна (его правка 12.11)
            wpx = len(pod) * size * .64 + 34
            bx = (lx + 10 * side) - (wpx if side < 0 else 0)
            if lim:
                bx = min(max(bx, lim[0] + 8), lim[1] - wpx - 8)
            s += (f'<rect x="{bx:.0f}" y="{cy-46-size*0.86:.0f}" width="{wpx:.0f}"'
                  f' height="{size*1.26:.0f}" rx="8" fill="#17130f" opacity=".80"/>')
            s += (f'<text x="{bx + wpx/2:.0f}" y="{cy-46}" text-anchor="middle"'
                  f' font-family="{SANS}" font-size="{size}" font-weight="600" fill="{col}">'
                  f'{pod}</text>')
    return s + "</g>"


def card(x, y, w, h, t, t0, fill="#1d1310", op=.9, stroke=ZOL, dur=.4):
    p = A.over(A.seg(t, t0, dur), 1.3)
    if p <= 0:
        return ""
    cy = y + h / 2
    return (f'<g transform="translate({x+w/2:.0f},{cy:.0f}) scale({p:.3f})'
            f' translate({-(x+w/2):.0f},{-cy:.0f})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}"'
            f' opacity="{op}" stroke="{stroke}" stroke-width="5"/></g>')


def spisok(x, y, items, t, t0, step=.7, size=40, dy=74, num=False, strike=(),
           col="#ffffff"):
    s = ""
    for i, it in enumerate(items):
        p = A.out(A.seg(t, t0 + i * step, .4))
        if p <= 0:
            continue
        yy = y + i * dy
        dxx = (1 - p) * -60
        if num:
            s += (f'<circle cx="{x+20+dxx:.0f}" cy="{yy-13}" r="22" fill="{ZOL}" {o(4)}'
                  f' opacity="{p:.2f}"/>'
                  f'<text x="{x+20+dxx:.0f}" y="{yy-3}" text-anchor="middle" font-family="{SERIF}"'
                  f' font-size="28" font-weight="bold" fill="#17130f" opacity="{p:.2f}">{i+1}</text>')
            tx = x + 58 + dxx
        else:
            s += f'<circle cx="{x+13+dxx:.0f}" cy="{yy-12}" r="10" fill="{SVET}" opacity="{p:.2f}"/>'
            tx = x + 42 + dxx
        _b = (f'x="{tx:.0f}" y="{yy}" font-family="{SANS}" font-size="{size}"'
              f' font-weight="600"')
        s += (f'<text {_b} fill="none" stroke="{K}" stroke-width="6"'
              f' stroke-linejoin="round" opacity="{.9*p:.2f}">{it}</text>'
              f'<text {_b} fill="{col}" opacity="{p:.2f}">{it}</text>')
        if i in strike:
            q = A.out(A.seg(t, t0 + i * step + .9, .35))
            if q > 0:
                wdt = len(it) * size * .52 * q
                s += (f'<path d="M{tx-6:.0f},{yy-11} q{wdt/2:.0f},-9 {wdt:.0f},2" fill="none"'
                      f' stroke="#ff6b6b" stroke-width="8" stroke-linecap="round"/>')
    return s


def galka(x, y, t, t0, r=52, ok=True):
    p = A.over(A.seg(t, t0, .35), 2.0)
    if p <= 0:
        return ""
    col = "#7ed07e" if ok else "#ff6b6b"
    s = (f'<g transform="translate({x},{y}) scale({p:.3f}) translate({-x},{-y})">'
         f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" {o(6)}/>')
    if ok:
        s += f'<path d="M{x-24},{y+2} l16,20 l34,-40" fill="none" {o(11, "#15300f")}/>'
    else:
        s += f'<path d="M{x-20},{y-20} l40,40 M{x+20},{y-20} l-40,40" fill="none" {o(11, "#3a0d0d")}/>'
    return s + "</g>"


def zatemn(op=.5):
    return f'<rect width="{W}" height="{H}" fill="#0b0705" opacity="{op}"/>'


def vign(hole=None):
    """Виньетка по краям кадра. Окно вставки из неё ВЫРЕЗАЕТСЯ: иначе фото в
    рамке уходит в самую тёмную зону и выглядит затемнённым (его правка 12.11)."""
    g = ('<radialGradient id="vg" cx=".5" cy=".5" r=".75">'
         '<stop offset=".55" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>')
    if hole:
        x, y, w, h = hole
        g += (f'<mask id="vgm"><rect width="{W}" height="{H}" fill="#fff"/>'
              f'<rect x="{x-9}" y="{y-9}" width="{w+18}" height="{h+18}" rx="20"'
              f' fill="#000"/></mask>')
        return g + f'<rect width="{W}" height="{H}" fill="url(#vg)" mask="url(#vgm)"/>'
    return g + f'<rect width="{W}" height="{H}" fill="url(#vg)"/>'


def sneg(t, n=60, seed=5):
    """Снежный слой поверх всего — новогодний слой «Козы»."""
    import random
    r = random.Random(seed)
    s = '<g fill="#ffffff" opacity=".8">'
    for i in range(n):
        x0 = r.uniform(0, W); p0 = r.uniform(0, 1)
        sp = r.uniform(18, 46); rr = r.uniform(2.2, 5.2); ph = r.uniform(0, 1)
        p = (p0 + t * sp / H) % 1.0
        s += (f'<circle cx="{x0 + 34*A.w(t, 5.2, ph):.0f}" cy="{p*H:.0f}" r="{rr:.1f}"'
              f' opacity="{0.25 + 0.5*abs(A.w(t, 3.1, ph)):.2f}"/>')
    return s + "</g>"


def iskry(t, cx, cy, n=14, seed=3, R=260):
    """Золотые искры вокруг точки — на акцентах."""
    import random, math
    r = random.Random(seed)
    s = ""
    for i in range(n):
        a = r.uniform(0, 6.28); d = r.uniform(.3, 1) * R; ph = r.uniform(0, 1)
        op = .25 + .55 * abs(A.w(t, 2.2, ph))
        x = cx + d * math.cos(a + t * .15)
        y = cy + d * math.sin(a + t * .15) * .7
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{2.5 + 2*abs(A.w(t,1.7,ph)):.1f}" fill="{SVET}" opacity="{op:.2f}"/>'
    return s


def okno_ramka(x, y, w, h):
    # ТЕНЬ ТОЛЬКО ПО ПЕРИМЕТРУ. Раньше здесь лежал сплошной чёрный прямоугольник
    # на 45% — он ложился ПОВЕРХ фото и гасил его (его правка 12.11:
    # «фотография в рамке затемнённая, я не хочу, чтобы она была затемнённая»).
    return (f'<rect x="{x-16}" y="{y-16}" width="{w+32}" height="{h+32}" rx="24"'
            f' fill="none" stroke="#000" stroke-width="16" opacity=".45"/>'
            f'<rect x="{x-9}" y="{y-9}" width="{w+18}" height="{h+18}" rx="20" fill="none" {o(14)}/>'
            f'<rect x="{x-9}" y="{y-9}" width="{w+18}" height="{h+18}" rx="20" fill="none"'
            f' stroke="{ZOL}" stroke-width="5"/>')


def vopros(x, y, t, t0, size=300):
    p = A.over(A.seg(t, t0, .5), 1.8)
    if p <= 0:
        return ""
    return (f'<g transform="translate({x},{y}) scale({p:.3f}) translate({-x},{-y})">'
            + txt(x, y, "?", size, SVET, "middle", SERIF, 0, "bold", stroke=size*.08) + "</g>")


def slovo(x, y, s, t, t0, size=72, col=None, icon=None, dur=.42):
    """Выскакивающее слово-акцент (его правка 12.11: «надо какие-то надписи,
    чтобы выскакивали — деньги, шары, апельсины, банты»).

    Выпрыгивает с перелётом, живёт 2,6 с, уходит вниз. Рядом — рисованный
    значок предмета, если он задан."""
    col = col or SVET
    k = A.over(A.seg(t, t0, dur), 1.7)
    if k <= 0:
        return ""
    ut = A.ease(A.seg(t, t0 + 2.6, .4))          # уход
    if ut >= 1:
        return ""
    dy = 54 * ut
    op = 1 - ut
    w = max(240, len(s) * size * .62 + (190 if icon else 92))
    g = (f'<g transform="translate({x},{y + dy:.0f}) scale({k:.3f}) rotate(-2)"'
         f' opacity="{op:.2f}">')
    g += (f'<rect x="{-w/2:.0f}" y="-{size*.86:.0f}" width="{w:.0f}"'
          f' height="{size*1.3:.0f}" rx="{size*.3:.0f}" fill="#17130f" opacity=".88"'
          f' stroke="{col}" stroke-width="4"/>')
    if icon:
        g += znachok(icon, -w / 2 + size * 1.02, -size * .22, size * .38, col)
        g += txt(size * .52, size * .22, s, size, "#ffffff", "middle", SANS, 2, "bold", stroke=0)
    else:
        g += txt(0, size * .22, s, size, "#ffffff", "middle", SANS, 2, "bold", stroke=0)
    return g + "</g>"


def znachok(kind, x, y, r, col=None):
    """Маленький рисованный значок предмета для слова-акцента."""
    col = col or SVET
    if kind == "shar":
        return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{KRAS}" {o(3)}/>'
                f'<circle cx="{x-r*.3:.0f}" cy="{y-r*.34:.0f}" r="{r*.26:.0f}" fill="#fff" opacity=".7"/>'
                f'<rect x="{x-r*.22:.0f}" y="{y-r*1.42:.0f}" width="{r*.44:.0f}"'
                f' height="{r*.44:.0f}" rx="3" fill="{ZOL}"/>')
    if kind == "bant":
        return (f'<g transform="translate({x:.0f},{y:.0f})">' + bow(0, 0, r / 26, VIN) + '</g>')
    if kind == "apelsin":
        return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#e8872a" {o(3)}/>'
                + "".join(f'<path d="M{x:.0f},{y:.0f} L{x + r*.86*math.cos(i*1.05):.0f},'
                          f'{y + r*.86*math.sin(i*1.05):.0f}" stroke="#c96a16" stroke-width="2.5"/>'
                          for i in range(6))
                + f'<path d="M{x:.0f},{y-r:.0f} q{r*.4:.0f},-{r*.3:.0f} {r*.6:.0f},-{r*.06:.0f}"'
                  f' fill="{ZEL2}"/>')
    if kind == "dengi":
        return (f'<rect x="{x-r:.0f}" y="{y-r*.62:.0f}" width="{r*2:.0f}" height="{r*1.24:.0f}"'
                f' rx="4" fill="#5b8c5a" {o(3)}/>'
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*.38:.0f}" fill="none" stroke="#e8f0d8" stroke-width="3"/>')
    if kind == "mishura":
        return (f'<path d="M{x-r:.0f},{y:.0f} q{r*.5:.0f},-{r*.7:.0f} {r:.0f},0'
                f' q{r*.5:.0f},{r*.7:.0f} {r:.0f},0" fill="none" stroke="{ZOL}"'
                f' stroke-width="{r*.34:.0f}" stroke-linecap="round"/>')
    if kind == "svecha":
        return (f'<rect x="{x-r*.3:.0f}" y="{y-r*.3:.0f}" width="{r*.6:.0f}" height="{r*1.3:.0f}"'
                f' rx="4" fill="{KREM}" {o(3)}/>'
                f'<ellipse cx="{x:.0f}" cy="{y-r*.62:.0f}" rx="{r*.22:.0f}" ry="{r*.42:.0f}" fill="{SVET}"/>')
    if kind == "shishka":
        return (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r*.62:.0f}" ry="{r:.0f}"'
                f' fill="#8a5a3c" {o(3)}/>'
                f'<path d="M{x-r*.42:.0f},{y-r*.4:.0f} q{r*.42:.0f},{r*.24:.0f} {r*.84:.0f},0'
                f' M{x-r*.44:.0f},{y:.0f} q{r*.44:.0f},{r*.24:.0f} {r*.88:.0f},0"'
                f' fill="none" stroke="#5e3a22" stroke-width="3"/>')
    if kind == "zvezda":
        return zvezda(x, y, r, SVET)
    if kind == "chasy":
        return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{KREM}" {o(4)}/>'
                f'<path d="M{x:.0f},{y:.0f} V{y-r*.6:.0f} M{x:.0f},{y:.0f} L{x+r*.46:.0f},{y+r*.2:.0f}"'
                f' stroke="{K}" stroke-width="4" stroke-linecap="round"/>')
    if kind == "ptica":
        return (f'<path d="M{x-r:.0f},{y:.0f} q{r*.6:.0f},-{r*.9:.0f} {r*1.1:.0f},-{r*.1:.0f}'
                f' q{r*.5:.0f},{r*.1:.0f} {r*.8:.0f},-{r*.4:.0f}" fill="{SVET}" {o(3)}/>'
                f'<circle cx="{x+r*.5:.0f}" cy="{y-r*.3:.0f}" r="{r*.12:.0f}" fill="{K}"/>')
    if kind == "kosmonavt":
        return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#d9dde6" {o(4)}/>'
                f'<path d="M{x-r*.62:.0f},{y-r*.1:.0f} a{r*.62:.0f},{r*.56:.0f} 0 0 1'
                f' {r*1.24:.0f},0 Z" fill="#2a3550"/>'
                f'<circle cx="{x-r*.22:.0f}" cy="{y-r*.3:.0f}" r="{r*.16:.0f}" fill="#9fd4ff" opacity=".8"/>')
    return ""
