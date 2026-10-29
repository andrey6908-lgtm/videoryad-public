# -*- coding: utf-8 -*-
"""Кирпичики движения: всё считается от времени, поэтому кадр живой,
а зум идёт вектором и не дёргается."""
import math, random

def w(t, period, phase=0.0):
    """Колебание -1..1."""
    return math.sin(2 * math.pi * (t / period + phase))


def blink(t, period=4.3, phase=0.0, dur=0.14):
    """True, пока глаз закрыт. Вразнобой задаётся фазой."""
    return ((t / period) + phase) % 1.0 < dur / period


def sway(t, period=5.1, phase=0.0, amp=0.7):
    """Мелкое покачивание тела, градусы."""
    return amp * w(t, period, phase)


def flame(x, y, t, s=1.0, glow=52, phase=0.0):
    """Пламя свечи: колышется, меняет высоту и ширину, ореол дышит."""
    dx = 3.2 * s * w(t, 1.7, phase) + 1.5 * s * w(t, 0.41, phase + .3)
    h = 40 * s * (1 + .10 * w(t, 0.63, phase + .2))
    half = 16 * s * (1 + .12 * w(t, 0.37, phase + .7))
    g = glow * (1 + .07 * w(t, 0.83, phase))
    return (f'<ellipse cx="{x+dx*.4:.1f}" cy="{y-h*.45:.1f}" rx="{g*.85:.1f}" ry="{g:.1f}" fill="url(#candle)"/>'
            f'<path d="M{x+dx:.1f} {y-h:.1f} C{x+half+dx*.3:.1f} {y-h*.45:.1f} {x+half*.9:.1f} {y-h*.1:.1f} {x:.1f} {y:.1f}'
            f' C{x-half*.9:.1f} {y-h*.1:.1f} {x-half+dx*.3:.1f} {y-h*.45:.1f} {x+dx:.1f} {y-h:.1f} Z" fill="#f9bb3e"/>'
            f'<path d="M{x+dx*.7:.1f} {y-h*.62:.1f} C{x+half*.42:.1f} {y-h*.3:.1f} {x+half*.4:.1f} {y-h*.06:.1f} {x:.1f} {y-2:.1f}'
            f' C{x-half*.4:.1f} {y-h*.06:.1f} {x-half*.42:.1f} {y-h*.3:.1f} {x+dx*.7:.1f} {y-h*.62:.1f} Z" fill="#fff0bb" opacity=".8"/>')


def candle(x, y, t, hgt=78, glow=52, phase=0.0, s=1.0):
    return (f'<rect x="{x-10*s:.0f}" y="{y}" width="{20*s:.0f}" height="{hgt}" rx="4"'
            f' fill="#ecdfc2" stroke="#1b1309" stroke-width="7"/>' + flame(x, y, t, s, glow, phase))


def smoke(x, y, t, n=3, h=120, s=1.0, op=.3):
    """Дымок: волнистые струйки ползут вверх и расходятся."""
    out = f'<g stroke="#f3d6b2" stroke-width="{8*s:.1f}" fill="none" opacity="{op}" stroke-linecap="round">'
    for i in range(n):
        ph = i * .37
        p = ((t * .22) + ph) % 1.0
        yy = y - p * h
        fade = min(1.0, p * 3.6) * max(0.0, 1 - (p - .55) / .45) if p > .55 else min(1.0, p * 3.6)
        if fade <= 0.02:
            continue
        a = 22 * s * w(t, 2.6, ph)
        out += (f'<path d="M{x+(i-1)*34*s:.0f} {yy:.0f} C{x+(i-1)*34*s+a:.0f} {yy-h*.22:.0f}'
                f' {x+(i-1)*34*s-a:.0f} {yy-h*.4:.0f} {x+(i-1)*34*s+a*.6:.0f} {yy-h*.62:.0f}"'
                f' opacity="{fade:.2f}"/>')
    return out + '</g>'


_CONF = None
def confetti(t, n=34, seed=7, W=960, H=540, top=0, bot=540):
    """Конфетти: падает, качается, крутится. Детерминировано по seed."""
    global _CONF
    if _CONF is None or len(_CONF) != n:
        r = random.Random(seed)
        _CONF = [(r.uniform(0, W), r.uniform(0, 1), r.uniform(14, 30), r.uniform(0, 1),
                  r.choice(["#d6202f", "#e07f23", "#c9922f", "#efb07a", "#6abf4b", "#f4efe3"]),
                  r.uniform(5, 9), r.uniform(2.4, 4.4)) for _ in range(n)]
    out = '<g>'
    span = bot - top
    for x0, p0, spd, ph, col, sz, per in _CONF:
        p = (p0 + t * spd / span) % 1.0
        y = top + p * span
        x = x0 + 26 * w(t, per, ph)
        rot = (t * 120 * (0.5 + ph)) % 360
        sq = abs(math.cos(math.radians(rot)))
        out += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{sz:.1f}" height="{sz*0.5*(0.35+sq):.1f}"'
                f' rx="1.5" fill="{col}" opacity=".85" transform="rotate({rot*.3:.0f} {x:.0f} {y:.0f})"/>')
    return out + '</g>'


def glare(t, period=13.0, dur=1.6, W=960, H=540, phase=0.0):
    """Блик: мягкая диагональная полоса пробегает по кадру."""
    p = ((t / period) + phase) % 1.0
    k = p * period
    if k > dur:
        return ""
    f = k / dur
    cx = -300 + f * (W + 600)
    return (f'<g opacity="{(math.sin(math.pi*f)*0.16):.3f}">'
            f'<path d="M{cx:.0f} -60 L{cx+150:.0f} -60 L{cx+150-220:.0f} {H+60} L{cx-220:.0f} {H+60} Z"'
            ' fill="#ffe9bb"/></g>')


def lights(items, t):
    """Огоньки гирлянды мигают вразнобой."""
    out = '<g>'
    for i, (x, y, col) in enumerate(items):
        o = .55 + .45 * w(t, 1.9 + (i % 5) * .31, i * .17)
        out += (f'<circle cx="{x}" cy="{y}" r="7" fill="{col}" opacity="{o:.2f}"/>'
                f'<circle cx="{x}" cy="{y}" r="17" fill="{col}" opacity="{o*0.3:.2f}"/>')
    return out + '</g>'


def snowfall(t, n=16, seed=3, W=960, H=540):
    r = random.Random(seed)
    pts = [(r.uniform(0, W), r.uniform(0, 1), r.uniform(8, 18), r.uniform(0, 1), r.uniform(2.6, 5))
           for _ in range(n)]
    out = '<g fill="#eef6ff" opacity=".45">'
    for x0, p0, spd, ph, rr in pts:
        p = (p0 + t * spd / H) % 1.0
        out += f'<circle cx="{x0 + 20*w(t, 4.2, ph):.0f}" cy="{p*H:.0f}" r="{rr:.1f}"/>'
    return out + '</g>'
