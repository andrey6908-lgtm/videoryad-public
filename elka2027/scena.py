# -*- coding: utf-8 -*-
"""Богатая новогодняя комната, которая ЖИВЁТ: камин слева с огнём, ёлка в центре
с качающимися шарами и мигающей гирляндой, окно вставки справа, гирлянда по
стене, венок, свечи, подарки, снег за окном. Камера ходит по сцене (viewBox)."""
import math
import anim as A
from ng import *

W, H = 1920, 1080
OKNO = (1150, 560, 700, 394)        # вставка: правый низ, под окном в сад


def kamin_zhivoy(x, y, t, w=430, h=330):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#5c3d33" {o(7)}/>'
         f'<rect x="{x-26}" y="{y-36}" width="{w+52}" height="38" rx="8" fill="{TERRA}" {o(7)}/>'
         f'<rect x="{x+w*.13:.0f}" y="{y+h*.2:.0f}" width="{w*.74:.0f}" height="{h*.8:.0f}"'
         f' rx="12" fill="#1a0f0c" {o(7)}/>')
    cx, cy = x + w * .5, y + h * .86
    s += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{w*.3:.0f}" ry="{h*.22:.0f}" fill="url(#teplo)"/>'
    for i, dx in enumerate((-56, 6, 58)):
        s += f'<rect x="{cx+dx:.0f}" y="{cy-8:.0f}" width="62" height="18" rx="9" fill="{TERRA}" {o(5)}/>'
    for i in range(3):
        ph = i * .33
        hh = (96 if i == 1 else 70) * (1 + .18 * A.w(t, .9, ph))
        bx = cx + (i - 1) * 40
        dx = 14 * A.w(t, 1.6, ph)
        s += (f'<path d="M{bx:.0f},{cy-6:.0f}'
              f' C{bx-26:.0f},{cy-hh*.45:.0f} {bx-10+dx:.0f},{cy-hh*.75:.0f} {bx+dx:.0f},{cy-hh:.0f}'
              f' C{bx+16+dx:.0f},{cy-hh*.7:.0f} {bx+26:.0f},{cy-hh*.4:.0f} {bx:.0f},{cy-6:.0f} Z"'
              f' fill="{SVET if i == 1 else ORA}" opacity="{.8+.18*abs(A.w(t,1.1,ph)):.2f}"/>')
    for i in range(2):
        ph = i * .5
        hh = 44 * (1 + .2 * A.w(t, .7, ph))
        bx = cx + (i * 2 - 1) * 18
        s += (f'<path d="M{bx:.0f},{cy-6:.0f} C{bx-12:.0f},{cy-hh*.5:.0f}'
              f' {bx+8:.0f},{cy-hh*.8:.0f} {bx:.0f},{cy-hh:.0f}'
              f' C{bx-6:.0f},{cy-hh*.6:.0f} {bx+12:.0f},{cy-hh*.4:.0f} {bx:.0f},{cy-6:.0f} Z"'
              f' fill="#fff3c9" opacity=".85"/>')
    for i in range(5):
        p = ((t * .5) + i * .2) % 1.0
        s += (f'<circle cx="{cx + 40*A.w(t,2.2,i*.2):.0f}" cy="{cy-30-p*170:.0f}"'
              f' r="{2.5+1.5*(1-p):.1f}" fill="{SVET}" opacity="{(1-p)*.8:.2f}"/>')
    # носки
    for i, dx in enumerate((-120, 0, 120)):
        sw = 4 * A.w(t, 3.6, i * .3)
        s += (f'<g transform="rotate({sw:.1f} {x+w*.5+dx:.0f} {y-30})">'
              f'<path d="M{x+w*.5+dx-22:.0f},{y-26} v70 q0,26 26,26 h26 v-96 Z"'
              f' fill="{[KRAS, ZEL2, GRAN][i]}" {o(6)}/>'
              f'<rect x="{x+w*.5+dx-26:.0f}" y="{y-36}" width="60" height="20" rx="8"'
              f' fill="{KREM}" {o(5)}/></g>')
    return s


def svecha(x, y, t, ph=0.0, s=1.0):
    hh = 30 * s * (1 + .12 * A.w(t, .7, ph))
    dx = 3 * s * A.w(t, 1.4, ph)
    return (f'<ellipse cx="{x:.0f}" cy="{y-hh*.5:.0f}" rx="{34*s:.0f}" ry="{44*s:.0f}" fill="url(#teplo)"/>'
            f'<rect x="{x-9*s:.0f}" y="{y}" width="{18*s:.0f}" height="{52*s:.0f}" rx="4"'
            f' fill="{KREM}" {o(5)}/>'
            f'<path d="M{x+dx:.1f},{y-hh:.1f} c10,{hh*.5:.1f} 8,{hh*.8:.1f} -1,{hh:.1f}'
            f' c-9,{-hh*.2:.1f} -11,{-hh*.5:.1f} 1,{-hh:.1f} Z" fill="{SVET}"/>')


def venok(x, y, t, r=86):
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{ZEL2}" stroke-width="34"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{HVOYA}" stroke-width="18" opacity=".7"/>'
    for i in range(10):
        a = i * 36 * math.pi / 180
        bx, by = x + r * math.cos(a), y + r * math.sin(a)
        op = .55 + .45 * abs(A.w(t, 2.4, i * .13))
        s += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="9" fill="{[KRAS, ZOL][i%2]}" opacity="{op:.2f}"/>'
    s += bow(x, y + r - 6, .5, VIN)
    return s


def okno_v_sad(x, y, t, w=300, h=360):
    """Нарисованное окно комнаты: ночь, снег — глубина кадра."""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#14203a" {o(9)}/>')
    import random
    r = random.Random(3)
    for i in range(18):
        x0 = r.uniform(x + 8, x + w - 8); p0 = r.uniform(0, 1)
        p = (p0 + t * .06) % 1.0
        s += (f'<circle cx="{x0 + 10*A.w(t,4.2,p0):.0f}" cy="{y + p*h:.0f}" r="2.6"'
              f' fill="#ffffff" opacity=".7"/>')
    s += (f'<path d="M{x+w/2},{y} v{h} M{x},{y+h/2} h{w}" stroke="{KREM}" stroke-width="10"/>'
          f'<rect x="{x-10}" y="{y-10}" width="{w+20}" height="{h+20}" rx="12" fill="none"'
          f' stroke="{KREM}" stroke-width="12"/>')
    return s


def girlyanda_steny(y, t, n=16):
    s = f'<path d="M0,{y} q480,120 960,0 q480,-120 960,0" fill="none" stroke="{ZEL2}" stroke-width="10"/>'
    for i in range(n):
        u = i / (n - 1)
        x = u * W
        yy = y + 120 * math.sin(math.pi * u * 2) * (1 if u < .5 else -1) * .5
        col = [SVET, KRAS, "#9ee07f", "#7fd0ff"][i % 4]
        op = .45 + .55 * abs(A.w(t, 1.6 + (i % 5) * .3, i * .2))
        s += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="22" fill="{col}" opacity="{op*.25:.2f}"/>'
        s += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="9" fill="{col}" opacity="{op:.2f}" {o(3)}/>'
    return s


def elka_zhivaya(cx, base, h, t, palette, zvezda_puls=True):
    """Ёлка, у которой шары качаются, часть подсвечивается, звезда дышит."""
    w = h * .80
    s = f'<ellipse cx="{cx}" cy="{base-h*.5:.0f}" rx="{w*.9:.0f}" ry="{h*.62:.0f}" fill="url(#teplo)" opacity=".45"/>'
    s += f'<rect x="{cx-26}" y="{base-40}" width="52" height="60" rx="8" fill="{TERRA}" {o(6)}/>'
    tiers = 5
    for i in range(tiers):
        u = i / tiers
        yy = base - h * u
        ww = w * (1 - u) * .5 + w * .12
        hh = h / tiers * 1.5
        s += (f'<path d="M{cx},{yy-hh:.0f} L{cx-ww:.0f},{yy:.0f} Q{cx},{yy+22:.0f} {cx+ww:.0f},{yy:.0f} Z"'
              f' fill="{HVOYA if i%2 else ZEL2}" {o(6)}/>')
    k = 0
    for i in range(tiers):
        u = i / tiers
        yy = base - h * u - h * .06
        ww = w * (1 - u) * .5
        n = max(2, 5 - i)
        for j in range(n):
            px = cx - ww * .8 + (ww * 1.6) * (j / max(1, n - 1))
            r = max(8, h * .055 - i * h * .008)
            sw = 5 * A.w(t, 2.6 + (k % 5) * .4, k * .17)          # покачивание
            op = .75 + .25 * abs(A.w(t, 1.8 + (k % 4) * .5, k * .23))  # подсветка
            col = palette[k % len(palette)]
            s += (f'<g transform="rotate({sw:.1f} {px:.0f} {yy-10-r:.0f})" opacity="{op:.2f}">'
                  + ball(px, yy - 10, r, col) + '</g>')
            k += 1
    s += lights(cx - w * .46, base - h * .30, w * .92, 7, max(5, h * .016))
    s += lights(cx - w * .30, base - h * .58, w * .60, 5, max(4, h * .014))
    for i in range(7):
        u = i / 6
        x = cx - w * .4 + w * .8 * u
        y = base - h * (.18 + .5 * abs(math.sin(u * 3)))
        op = .3 + .7 * abs(A.w(t, 1.3 + i * .21, i * .3))
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{SVET}" opacity="{op:.2f}"/>'
    zp = 1 + (.12 * A.w(t, 2.2) if zvezda_puls else 0)
    s += (f'<g transform="translate({cx},{base-h-18}) scale({zp:.3f}) translate({-cx},{-(base-h-18)})">'
          + zvezda(cx, base - h - 18, 38, SVET) + '</g>')
    s += bow(cx - w * .26, base - h * .42, .5, VIN)
    s += bow(cx + w * .2, base - h * .66, .42, VIN)
    return s


def komnata(t, pal, zvezda_puls=True):
    """Весь фон: камин СЛЕВА, ёлка в центре, окно в сад справа — не внахлёст."""
    s = room(W, H, .80)
    s += girlyanda_steny(120, t)
    s += okno_v_sad(1430, 110, t, 300, 300)
    s += venok(1000, 210, t, 78)
    s += kamin_zhivoy(90, 520, t)
    s += f'<rect x="60" y="474" width="490" height="26" rx="8" fill="{TERRA}" {o(6)}/>'
    for i, x in enumerate((140, 250, 360, 470)):
        s += svecha(x, 440, t, i * .27, .9)
    s += elka_zhivaya(800, 940, 600, t, pal, zvezda_puls)
    for i, (x, y, w_, h_, c1, c2) in enumerate(((600, 950, 150, 104, VIN, ZOL),
                                                (760, 968, 160, 88, ZEL2, SVET),
                                                (930, 958, 140, 98, KRAS, ZOL))):
        s += gift(x, y, w_, h_, c1, c2)
    return s
