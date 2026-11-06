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
    s = ""
    for i, (c, p) in enumerate(zip(cols, pod)):
        k = A.over(A.seg(t, t0 + i * step, .45), 1.6)
        if k <= 0:
            continue
        cx = x + i * dx
        s += f'<circle cx="{cx}" cy="{y}" r="{r*k:.1f}" fill="{c}" {o(6)}/>'
        if k > .9:
            s += (f'<text x="{cx}" y="{y+r+40}" text-anchor="middle" font-family="{SANS}"'
                  f' font-size="26" fill="{KREM}" stroke="{K}" stroke-width="5"'
                  f' paint-order="stroke">{p}</text>')
    return s


def obvodka(cx, cy, rx, ry, pod, t, t0, col=SVET, side=1, dx=160, dur=.6, size=34):
    """Обводка рисуется по кругу, затем выноска и подпись."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    per = 2 * 3.1416 * ((rx + ry) / 2)
    s = (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{col}"'
         f' stroke-width="7" stroke-dasharray="{per*p:.0f} {per:.0f}"'
         f' transform="rotate(-90 {cx} {cy})"/>')
    q = A.out(A.seg(t, t0 + dur, .4))
    if q > 0:
        lx = cx + (rx + dx) * side
        anc = "start" if side > 0 else "end"
        s += (f'<path d="M{cx + rx*side},{cy} L{cx + (rx + dx*q)*side:.0f},{cy-40*q:.0f}"'
              f' stroke="{col}" stroke-width="5"/>')
        if q > .8:
            s += (f'<text x="{lx + 10*side}" y="{cy-46}" text-anchor="{anc}"'
                  f' font-family="{SANS}" font-size="{size}" font-weight="600" fill="{col}"'
                  f' stroke="{K}" stroke-width="6" paint-order="stroke">{pod}</text>')
    return s


def card(x, y, w, h, t, t0, fill="#1d1310", op=.9, stroke=ZOL, dur=.4):
    p = A.over(A.seg(t, t0, dur), 1.3)
    if p <= 0:
        return ""
    cy = y + h / 2
    return (f'<g transform="translate({x+w/2:.0f},{cy:.0f}) scale({p:.3f})'
            f' translate({-(x+w/2):.0f},{-cy:.0f})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}"'
            f' opacity="{op}" stroke="{stroke}" stroke-width="5"/></g>')


def spisok(x, y, items, t, t0, step=.7, size=40, dy=74, num=False, strike=(), col=KREM):
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
        s += (f'<text x="{tx:.0f}" y="{yy}" font-family="{SANS}" font-size="{size}"'
              f' fill="{col}" opacity="{p:.2f}" stroke="{K}" stroke-width="5"'
              f' paint-order="stroke">{it}</text>')
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


def vign():
    return ('<radialGradient id="vg" cx=".5" cy=".5" r=".75">'
            '<stop offset=".55" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>'
            f'<rect width="{W}" height="{H}" fill="url(#vg)"/>')


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
    return (f'<rect x="{x-16}" y="{y-16}" width="{w+32}" height="{h+32}" rx="24" fill="#000" opacity=".45"/>'
            f'<rect x="{x-9}" y="{y-9}" width="{w+18}" height="{h+18}" rx="20" fill="none" {o(14)}/>'
            f'<rect x="{x-9}" y="{y-9}" width="{w+18}" height="{h+18}" rx="20" fill="none"'
            f' stroke="{ZOL}" stroke-width="5"/>')


def vopros(x, y, t, t0, size=300):
    p = A.over(A.seg(t, t0, .5), 1.8)
    if p <= 0:
        return ""
    return (f'<g transform="translate({x},{y}) scale({p:.3f}) translate({-x},{-y})">'
            + txt(x, y, "?", size, SVET, "middle", SERIF, 0, "bold", stroke=size*.08) + "</g>")
