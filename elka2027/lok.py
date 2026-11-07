# -*- coding: utf-8 -*-
"""БИБЛИОТЕКА ДЕКОРАЦИЙ. Его слово 07.11: «всё должно строиться на смене сцен,
одна комната на весь ролик — это херня». Поэтому тут не одна комната, а места:
двор со снеговиком, стол, прихожая, камин крупно, ветка крупно, ночное небо,
мастерская, лес, витрина. Камера ходит ВНУТРИ локации, локации сменяются.
"""
import math, random
import anim as A
from ng import *

W, H = 1920, 1080
NOCH = "#16203a"


def sneg_sloy(t, n=40, seed=5, op=.75):
    r = random.Random(seed)
    s = f'<g fill="#ffffff" opacity="{op}">'
    for i in range(n):
        x0 = r.uniform(0, W); p0 = r.uniform(0, 1)
        sp = r.uniform(16, 44); rr = r.uniform(2.4, 5.4); ph = r.uniform(0, 1)
        p = (p0 + t * sp / H) % 1.0
        s += (f'<circle cx="{x0 + 36*A.w(t,5.2,ph):.0f}" cy="{p*H:.0f}" r="{rr:.1f}"'
              f' opacity="{.3+.55*abs(A.w(t,3.1,ph)):.2f}"/>')
    return s + "</g>"


def ogon(cx, cy, t, s=1.0, ph=0.0):
    out = f'<ellipse cx="{cx:.0f}" cy="{cy-20*s:.0f}" rx="{90*s:.0f}" ry="{70*s:.0f}" fill="url(#teplo)"/>'
    for i in range(3):
        f = i * .33 + ph
        hh = (110 if i == 1 else 78) * s * (1 + .2 * A.w(t, .9, f))
        bx = cx + (i - 1) * 40 * s
        dx = 16 * s * A.w(t, 1.6, f)
        out += (f'<path d="M{bx:.0f},{cy:.0f} C{bx-30*s:.0f},{cy-hh*.45:.0f}'
                f' {bx-12*s+dx:.0f},{cy-hh*.75:.0f} {bx+dx:.0f},{cy-hh:.0f}'
                f' C{bx+18*s+dx:.0f},{cy-hh*.7:.0f} {bx+30*s:.0f},{cy-hh*.4:.0f} {bx:.0f},{cy:.0f} Z"'
                f' fill="{SVET if i == 1 else ORA}" opacity="{.8+.18*abs(A.w(t,1.1,f)):.2f}"/>')
    for i in range(6):
        p = ((t * .45) + i * .17) % 1.0
        out += (f'<circle cx="{cx + 50*s*A.w(t,2.2,i*.2):.0f}" cy="{cy-30*s-p*200*s:.0f}"'
                f' r="{(2.6+1.6*(1-p))*s:.1f}" fill="{SVET}" opacity="{(1-p)*.8:.2f}"/>')
    return out


def shar_zhivoy(x, y, r, col, t, i=0):
    sw = 6 * A.w(t, 2.6 + (i % 5) * .4, i * .17)
    op = .78 + .22 * abs(A.w(t, 1.8 + (i % 4) * .5, i * .23))
    return (f'<g transform="rotate({sw:.1f} {x:.0f} {y-r:.0f})" opacity="{op:.2f}">'
            + ball(x, y, r, col) + '</g>')


def elka(cx, base, h, t, pal, zv=True):
    w = h * .80
    s = f'<ellipse cx="{cx}" cy="{base-h*.5:.0f}" rx="{w*.9:.0f}" ry="{h*.62:.0f}" fill="url(#teplo)" opacity=".4"/>'
    s += ten(cx + 10, base + 16, w * .72, 34, .55)
    s += f'<rect x="{cx-26}" y="{base-40}" width="52" height="60" rx="8" fill="url(#derevo)" {o(6)}/>'
    for i in range(5):
        u = i / 5
        yy = base - h * u
        ww = w * (1 - u) * .5 + w * .12
        hh = h / 5 * 1.5
        s += (f'<path d="M{cx},{yy-hh:.0f} L{cx-ww:.0f},{yy:.0f} Q{cx},{yy+22:.0f} {cx+ww:.0f},{yy:.0f} Z"'
              f' fill="url(#hvoya)" {o(6)}/>')
    k = 0
    for i in range(5):
        u = i / 5
        yy = base - h * u - h * .06
        ww = w * (1 - u) * .5
        for j in range(max(2, 5 - i)):
            px = cx - ww * .8 + (ww * 1.6) * (j / max(1, 4 - i))
            s += shar_zhivoy(px, yy - 10, max(8, h * .055 - i * h * .008),
                             pal[k % len(pal)], t, k)
            k += 1
    s += lights(cx - w * .46, base - h * .30, w * .92, 7, max(5, h * .016))
    s += lights(cx - w * .30, base - h * .58, w * .60, 5, max(4, h * .014))
    if zv:
        zp = 1 + .12 * A.w(t, 2.2)
        s += (f'<g transform="translate({cx},{base-h-18}) scale({zp:.3f})'
              f' translate({-cx},{-(base-h-18)})">' + zvezda(cx, base - h - 18, 38, SVET) + '</g>')
    return s


# ─────────────────────────── ЛОКАЦИИ ───────────────────────────
def komnata(t, pal):
    s = room(W, H, .80)
    s += f'<path d="M0,120 q480,120 960,0 q480,-120 960,0" fill="none" stroke="{ZEL2}" stroke-width="10"/>'
    for i in range(16):
        u = i / 15; x = u * W
        y = 120 + 120 * math.sin(math.pi * u * 2) * (1 if u < .5 else -1) * .5
        col = [SVET, KRAS, "#9ee07f", "#7fd0ff"][i % 4]
        op = .45 + .55 * abs(A.w(t, 1.6 + (i % 5) * .3, i * .2))
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{col}" opacity="{op:.2f}" {o(3)}/>'
    s += (f'<rect x="1380" y="150" width="320" height="330" rx="10" fill="#14203a" {o(9)}/>'
          f'<path d="M1540,150 v330 M1380,315 h320" stroke="{KREM}" stroke-width="10"/>')
    s += f'<rect x="60" y="520" width="430" height="330" rx="10" fill="#5c3d33" {o(7)}/>'
    s += f'<rect x="34" y="484" width="482" height="38" rx="8" fill="{TERRA}" {o(7)}/>'
    s += f'<rect x="116" y="586" width="318" height="264" rx="12" fill="#1a0f0c" {o(7)}/>'
    s += ogon(275, 806, t, .9)
    s += elka(900, 940, 600, t, pal)
    for x, y, w_, h_, c1, c2 in ((700, 950, 150, 104, VIN, ZOL), (860, 968, 160, 88, ZEL2, SVET),
                                 (1030, 958, 140, 98, KRAS, ZOL)):
        s += gift(x, y, w_, h_, c1, c2)
    return s + sneg_sloy(t, 18, 6, .35)


def kamin_krupno(t, pal):
    s = f'<rect width="{W}" height="{H}" fill="#3a2420"/>'
    s += f'<rect y="900" width="{W}" height="180" fill="{POL}"/>'
    s += f'<rect x="240" y="180" width="1440" height="760" rx="14" fill="#5c3d33" {o(9)}/>'
    s += f'<rect x="190" y="120" width="1540" height="60" rx="10" fill="{TERRA}" {o(8)}/>'
    s += f'<rect x="420" y="330" width="1080" height="610" rx="16" fill="#1a0f0c" {o(8)}/>'
    s += ogon(960, 880, t, 2.4)
    for i, x in enumerate((520, 760, 1160, 1400)):
        sw = 5 * A.w(t, 3.6, i * .3)
        s += (f'<g transform="rotate({sw:.1f} {x} 180)">'
              f'<path d="M{x-40},186 v120 q0,44 44,44 h44 v-164 Z" fill="{[KRAS, ZEL2, GRAN, KRAS][i]}" {o(7)}/>'
              f'<rect x="{x-46}" y="166" width="100" height="32" rx="10" fill="{KREM}" {o(6)}/></g>')
    for i, x in enumerate((300, 1620)):
        s += svecha_bol(x, 60, t, i * .4)
    return s


def svecha_bol(x, y, t, ph=0.0):
    hh = 44 * (1 + .14 * A.w(t, .8, ph))
    dx = 5 * A.w(t, 1.5, ph)
    return (ten(x + 4, y + 92, 34, 9, .45)
            + f'<rect x="{x-16}" y="{y}" width="32" height="90" rx="6" fill="url(#vosk)" {o(6)}/>'
            f'<ellipse cx="{x}" cy="{y-hh*.4:.0f}" rx="54" ry="64" fill="url(#teplo)"/>'
            f'<path d="M{x+dx:.0f},{y-hh:.0f} c16,{hh*.5:.0f} 12,{hh*.8:.0f} -2,{hh:.0f}'
            f' c-14,{-hh*.2:.0f} -16,{-hh*.5:.0f} 2,{-hh:.0f} Z" fill="{SVET}"/>')


def vetka_krupno(t, pal):
    """Крупный план ветки с игрушками — фактура и блеск."""
    s = f'<rect width="{W}" height="{H}" fill="#1d2a1c"/>'
    s += sneg_sloy(t, 22, 3, .25)
    for k in range(3):
        yy = 240 + k * 300
        s += (f'<path d="M-40,{yy} q480,{70+k*20} 1000,{10-k*30} q520,{-60} 1000,{30}"'
              f' fill="none" stroke="{HVOYA}" stroke-width="{34-k*4}" stroke-linecap="round"/>')
        for i in range(52):
            u = i / 51
            x = -40 + u * 1960
            y = yy + (70 + k * 20) * math.sin(math.pi * u) * .5
            for sgn in (-1, 1):
                ln = 34 + 16 * ((i + k) % 3)
                s += (f'<path d="M{x:.0f},{y:.0f} l{sgn*(10+6*(i%2)):.0f},{-ln:.0f}"'
                      f' stroke="{ZEL2 if i % 2 else HVOYA}" stroke-width="6"'
                      f' stroke-linecap="round"/>')
            if i % 6 == 0:
                s += (f'<path d="M{x-26:.0f},{y-10:.0f} q26,-16 52,0 q-26,12 -52,0 Z"'
                      f' fill="#e8eef9" opacity=".8"/>')
        for i in range(4):
            u = (i + .5) / 4
            x = -40 + u * 1960
            y = yy + (70 + k * 20) * math.sin(math.pi * u) * .5 + 90
            s += (f'<path d="M{x:.0f},{y-90:.0f} v60" stroke="{ZOL}" stroke-width="5"/>')
            s += shar_zhivoy(x, y, 56 - k * 8, pal[(i + k) % len(pal)], t, i + k * 3)
    for i in range(10):
        u = i / 9
        x = u * W
        y = 300 + 420 * abs(math.sin(u * 4))
        op = .3 + .7 * abs(A.w(t, 1.3 + i * .21, i * .3))
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="{SVET}" opacity="{op:.2f}"/>'
    return s


def dvor(t, pal):
    """Двор: снеговик, фонарь, сугробы, дом с тёплыми окнами."""
    s = f'<rect width="{W}" height="{H}" fill="{NOCH}"/>'
    import random as _r
    r = _r.Random(11)
    for i in range(70):
        s += (f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,620):.0f}" r="{r.uniform(1.2,2.6):.1f}"'
              f' fill="#cfe0ff" opacity="{.3+.5*abs(A.w(t,2.4,i*.11)):.2f}"/>')
    s += f'<path d="M0,760 q300,-70 620,-30 q420,50 760,-40 q320,-80 540,10 L{W},{H} L0,{H} Z" fill="url(#snegg)"/>'
    s += f'<path d="M0,880 q420,-60 900,10 q480,70 1020,-30 L{W},{H} L0,{H} Z" fill="#ffffff"/>'
    # дом справа
    s += f'<rect x="1280" y="420" width="520" height="360" fill="#3a2a30" {o(8)}/>'
    s += f'<path d="M1240,420 L1540,250 L1840,420 Z" fill="{TERRA}" {o(8)}/>'
    for i, (x, y) in enumerate(((1360, 500), (1560, 500), (1360, 650), (1560, 650))):
        # окна живут: одни горят ровно, другие гаснут и зажигаются
        phase = A.w(t / (3.0 + i * 1.7), 1.0, i * .27)
        op = .22 if (i % 2 and phase < -.3) else .5 + .5 * abs(A.w(t, 3.2 + i * .6, i * .3))
        s += (f'<rect x="{x}" y="{y}" width="110" height="100" rx="8" fill="{SVET}"'
              f' opacity="{op:.2f}" {o(5)}/>')
        s += (f'<ellipse cx="{x+55}" cy="{y+50}" rx="150" ry="120" fill="url(#teplo)"'
              f' opacity="{op*.5:.2f}"/>')
    # фонарь
    s += f'<rect x="950" y="300" width="22" height="470" fill="#2a2a33" {o(6)}/>'
    s += (f'<path d="M905,300 h112 l-18,-52 h-76 Z" fill="#2a2a33" {o(6)}/>'
          f'<rect x="920" y="196" width="82" height="60" rx="8" fill="{SVET}" opacity=".9" {o(6)}/>')
    s += f'<ellipse cx="961" cy="240" rx="200" ry="170" fill="url(#teplo)"/>'
    # снеговик
    s += snegovik(420, 860, t, 1.0)
    s += elka(1120, 800, 300, t, pal, zv=False)
    return s + sneg_sloy(t, 46, 2, .9)


def snegovik(cx, base, t, s=1.0, sharf=KRAS):
    """Снеговик с лицом: улыбка дугой, глаза с бликом и морганием, румянец,
    варежки, объём на шарах и падающая тень (его правка 22)."""
    sw = 2.2 * A.w(t, 4.2)
    g = ten(cx, base + 10 * s, 150 * s, 32 * s, .5)
    g += f'<g transform="rotate({sw:.2f} {cx} {base})">'
    for cy, rr in ((base - 70 * s, 110 * s), (base - 210 * s, 82 * s), (base - 318 * s, 60 * s)):
        g += (f'<ellipse cx="{cx}" cy="{cy:.0f}" rx="{rr:.0f}" ry="{rr*.92:.0f}"'
              f' fill="url(#snegg)" {o(7)}/>')
        g += (f'<ellipse cx="{cx-rr*.3:.0f}" cy="{cy-rr*.3:.0f}" rx="{rr*.3:.0f}"'
              f' ry="{rr*.2:.0f}" fill="#ffffff" opacity=".8"/>')
        g += (f'<path d="M{cx-rr*.75:.0f},{cy+rr*.4:.0f} a{rr*.75:.0f},{rr*.75:.0f} 0 0 0'
              f' {rr*1.5:.0f},0" fill="none" stroke="#9fb0c8" stroke-width="{rr*.1:.1f}"'
              f' opacity=".45"/>')
    # шарф
    g += (f'<path d="M{cx-66*s:.0f},{base-252*s:.0f} q66,36 132,0 l8,34 q-74,36 -148,0 Z"'
          f' fill="{sharf}" {o(6)}/>')
    g += (f'<path d="M{cx+52*s:.0f},{base-240*s:.0f} q34,64 {10+6*A.w(t,3.4):.0f},116"'
          f' fill="none" stroke="{sharf}" stroke-width="{24*s:.0f}" stroke-linecap="round"/>')
    # шляпа
    g += (f'<rect x="{cx-58*s:.0f}" y="{base-394*s:.0f}" width="{116*s:.0f}" height="{22*s:.0f}"'
          f' rx="7" fill="#20202a" {o(5)}/>'
          f'<rect x="{cx-38*s:.0f}" y="{base-472*s:.0f}" width="{76*s:.0f}" height="{84*s:.0f}"'
          f' rx="7" fill="#20202a" {o(5)}/>'
          f'<rect x="{cx-39*s:.0f}" y="{base-410*s:.0f}" width="{78*s:.0f}" height="{18*s:.0f}"'
          f' fill="{sharf}"/>')
    # глаза с бликом и морганием
    shut = A.blink(t, 4.1, .2, .16)
    for dx in (-24, 24):
        ex, ey = cx + dx * s, base - 336 * s
        if shut:
            g += f'<path d="M{ex-13*s:.0f},{ey:.0f} q13,11 26,0" fill="none" {o(5)}/>'
        else:
            g += (f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{11*s:.1f}" fill="#20202a"/>'
                  f'<circle cx="{ex-3.5*s:.0f}" cy="{ey-3.5*s:.0f}" r="{3.6*s:.1f}" fill="#ffffff"/>')
    # нос-морковка с объёмом
    g += (f'<path d="M{cx:.0f},{base-318*s:.0f} l{46*s:.0f},{11*s:.0f} l{-46*s:.0f},{15*s:.0f} Z"'
          f' fill="{ORA}" {o(4)}/>'
          f'<path d="M{cx+6*s:.0f},{base-316*s:.0f} l{30*s:.0f},{8*s:.0f}" stroke="#f6b26b"'
          f' stroke-width="{3*s:.1f}" opacity=".8"/>')
    # румянец и улыбка дугой
    for dx in (-44, 44):
        g += (f'<ellipse cx="{cx+dx*s:.0f}" cy="{base-304*s:.0f}" rx="{15*s:.0f}" ry="{9*s:.0f}"'
              f' fill="{PERS}" opacity=".55"/>')
    g += (f'<path d="M{cx-30*s:.0f},{base-290*s:.0f} q{30*s:.0f},{26*s:.0f} {60*s:.0f},0"'
          f' fill="none" {o(max(3, 5*s))}/>')
    # пуговицы и руки-ветки с варежками
    for i, dy in enumerate((-160, -120, -80)):
        g += f'<circle cx="{cx:.0f}" cy="{base+dy*s:.0f}" r="{8*s:.1f}" fill="#20202a"/>'
    for sgn in (-1, 1):
        hx, hy = cx + sgn * 86 * s, base - 220 * s
        ex, ey = hx + sgn * 92 * s, hy - 74 * s
        g += f'<path d="M{hx:.0f},{hy:.0f} L{ex:.0f},{ey:.0f}" {o(13, "#8a5a3c")}/>'
        g += (f'<path d="M{ex+sgn*10*s:.0f},{ey-6*s:.0f} l{sgn*26*s:.0f},{-20*s:.0f}'
              f' M{ex+sgn*6*s:.0f},{ey+4*s:.0f} l{sgn*28*s:.0f},{4*s:.0f}" {o(8, "#8a5a3c")}/>')
        g += (f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{22*s:.0f}" ry="{18*s:.0f}"'
              f' fill="{sharf}" {o(5)}/>')
    return g + "</g>"


def stol(t, pal):
    """Накрытый стол: самовар, мандарины, свечи, бокалы."""
    s = f'<rect width="{W}" height="{H}" fill="#3a2a26"/>'
    s += f'<path d="M0,620 h{W} v{H-620} h-{W} Z" fill="{TERRA}"/>'
    s += f'<rect y="600" width="{W}" height="40" rx="10" fill="#8a5a3c" {o(6)}/>'
    s += f'<path d="M120,640 h1680 v300 h-1680 Z" fill="#efe6d2" opacity=".85"/>'
    for i in range(12):
        s += f'<path d="M{120+i*150},640 v300" stroke="#d8cbb0" stroke-width="4" opacity=".6"/>'
    # самовар
    s += ten(430, 648, 120, 22, .5)
    s += (f'<ellipse cx="420" cy="520" rx="110" ry="130" fill="url(#plg)" {o(8)}/>'
          f'<ellipse cx="384" cy="470" rx="34" ry="56" fill="#ffe9b8" opacity=".45"/>'
          f'<rect x="380" y="330" width="80" height="70" rx="10" fill="{ZOL}" {o(7)}/>'
          f'<circle cx="420" cy="320" r="26" fill="{ORA}" {o(6)}/>'
          f'<path d="M530,500 q50,-10 44,-60" fill="none" stroke="{ZOL}" stroke-width="16"/>')
    for i in range(3):
        p = ((t * .3) + i * .33) % 1.0
        s += (f'<path d="M420,{300-p*180:.0f} q{18*A.w(t,2.2,i*.3):.0f},-40 0,-70" fill="none"'
              f' stroke="#cfd8ea" stroke-width="9" opacity="{(1-p)*.5:.2f}" stroke-linecap="round"/>')
    # мандарины
    for i, (x, y) in enumerate(((760, 560), (830, 590), (700, 600), (790, 630))):
        s += ten(x + 6, y + 44, 48, 12, .5)
        s += (f'<circle cx="{x}" cy="{y}" r="44" fill="{ORA}" {o(6)}/>'
              f'<ellipse cx="{x-14}" cy="{y-16}" rx="15" ry="11" fill="#ffd9a0" opacity=".55"/>'
              f'<path d="M{x-26},{y+22} a26,26 0 0 0 52,0" fill="none" stroke="#a85a12" stroke-width="5" opacity=".4"/>'
              f'<path d="M{x},{y-44} q10,-18 26,-20" fill="none" stroke="{ZEL2}" stroke-width="8"/>')
    # бокалы
    for i, x in enumerate((1180, 1320, 1460)):
        # бокал: чаша полукругом, ножка, основание — иначе читается конусом
        s += (f'<path d="M{x-52},430 a52,86 0 0 0 104,0 Z" fill="url(#vino)"/>'
              f'<path d="M{x-52},430 a52,86 0 0 0 104,0" fill="none" {o(5, "#dfe8f5")}/>'
              f'<path d="M{x-52},430 h104" stroke="#dfe8f5" stroke-width="5"/>'
              f'<rect x="{x-5}" y="514" width="10" height="84" fill="#dfe8f5"/>'
              f'<ellipse cx="{x}" cy="606" rx="46" ry="12" fill="#dfe8f5" {o(4)}/>'
              f'<path d="M{x-52},430 a52,86 0 0 0 104,0 Z" fill="url(#steklo)"/>'
              f'<path d="M{x-34},446 q-10,40 6,62" fill="none" stroke="#ffffff" stroke-width="7" opacity=".5"/>')
    s += ten(980, 676, 150, 18, .45)
    s += f'<ellipse cx="980" cy="660" rx="140" ry="34" fill="#f3ead5" {o(6)}/>'
    for i, (dx, dy) in enumerate(((-70, -14), (-10, -24), (52, -12), (16, 4))):
        s += (f'<path d="M{980+dx-26},{660+dy} q26,-30 52,0 q-26,26 -52,0 Z" fill="#c98a4b" {o(5)}/>'
              f'<path d="M{980+dx-14},{660+dy-4} q14,-8 28,0" fill="none" stroke="#fff3e0" stroke-width="4"/>')
    s += (f'<path d="M300,650 q120,-40 240,-6" fill="none" stroke="{HVOYA}" stroke-width="16" stroke-linecap="round"/>')
    for i in range(10):
        xx = 300 + i * 26
        yy = 650 - 30 * math.sin(i / 9 * math.pi)
        s += f'<path d="M{xx},{yy:.0f} l-14,-22 M{xx},{yy:.0f} l14,-20" stroke="{ZEL2}" stroke-width="6" stroke-linecap="round"/>'
    s += ball(430, 624, 26, KRAS)
    for i, x in enumerate((1640, 1760)):
        s += svecha_bol(x, 420, t, i * .5)
    return s


def prihozhaya(t, pal):
    s = f'<rect width="{W}" height="{H}" fill="#4a3129"/>'
    s += f'<rect y="880" width="{W}" height="200" fill="{POL}"/>'
    s += f'<rect x="620" y="140" width="680" height="760" rx="12" fill="#6b4634" {o(9)}/>'
    for i in range(2):
        s += f'<rect x="{680+i*300}" y="220" width="240" height="300" rx="8" fill="#5c3d33" {o(6)}/>'
    s += f'<circle cx="1240" cy="560" r="22" fill="{ZOL}" {o(6)}/>'
    # венок на двери
    cx, cy, r = 960, 420, 150
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ZEL2}" stroke-width="56"/>'
    for i in range(14):
        a = i * 26 * math.pi / 180
        op = .5 + .5 * abs(A.w(t, 2.2, i * .12))
        s += (f'<circle cx="{cx+r*math.cos(a):.0f}" cy="{cy+r*math.sin(a):.0f}" r="14"'
              f' fill="{[KRAS, ZOL][i%2]}" opacity="{op:.2f}"/>')
    s += bow(cx, cy + r - 10, .8, VIN)
    # коробки с игрушками
    s += (f'<rect x="180" y="700" width="380" height="200" rx="12" fill="#8a5a3c" {o(8)}/>'
          f'<rect x="160" y="664" width="420" height="56" rx="10" fill="{TERRA}" {o(7)}/>')
    for i, c in enumerate((KRAS, ZOL, GRAN, KREM)):
        s += shar_zhivoy(250 + i * 88, 760, 38, c, t, i)
    s += (f'<rect x="1420" y="740" width="320" height="160" rx="10" fill="{VIN}" {o(8)}/>'
          f'<rect x="1560" y="740" width="40" height="160" fill="{ZOL}"/>' + bow(1580, 744, .5, ZOL))
    return s


def nebo(t, pal):
    """Ночной город: крыши со снегом, тёплые окна, ёлка на площади, салют."""
    s = f'<rect width="{W}" height="{H}" fill="#0d1630"/>'
    import random as _r
    r = _r.Random(7)
    for i in range(110):
        s += (f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,760):.0f}" r="{r.uniform(1,2.8):.1f}"'
              f' fill="#ffffff" opacity="{.25+.6*abs(A.w(t,2.8,i*.07)):.2f}"/>')
    s += f'<circle cx="1660" cy="180" r="76" fill="#f3ead5" opacity=".95"/>'
    s += f'<circle cx="1660" cy="180" r="130" fill="url(#teplo)" opacity=".5"/>'
    # салют: вспышка, лучи, хвосты
    for k in range(3):
        ph = k * .34
        p = ((t * .32) + ph) % 1.0
        cx = 380 + k * 540
        cy = 260 + 70 * k
        R = 30 + p * 300
        col = [SVET, KRAS, "#9ee07f"][k % 3]
        if p < .12:
            s += f'<circle cx="{cx}" cy="{cy}" r="{40*(1-p/.12):.0f}" fill="#ffffff" opacity=".9"/>'
        for i in range(22):
            a_ = i * 16.4 * math.pi / 180
            x2 = cx + R * math.cos(a_)
            y2 = cy + R * math.sin(a_) * .85 + p * p * 90
            x1 = cx + R * .55 * math.cos(a_)
            y1 = cy + R * .55 * math.sin(a_) * .85
            s += (f'<path d="M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}" stroke="{col}"'
                  f' stroke-width="{5*(1-p)+1.5:.1f}" stroke-linecap="round"'
                  f' opacity="{max(0,.95-p*1.1):.2f}"/>')
    # дома: стены заметнее фона, иначе крыши висят в пустоте
    for x0, x1, top in ((0, 470, 660), (470, 960, 640), (960, 1430, 660), (1430, 1920, 650)):
        s += f'<rect x="{x0}" y="{top+10}" width="{x1-x0}" height="{1080-top}" fill="#1b2746"/>'
        s += f'<rect x="{x0}" y="{top+10}" width="{x1-x0}" height="{1080-top}" fill="none" stroke="#0d1630" stroke-width="6"/>'
    s += (f'<path d="M0,820 L240,660 L470,820 L700,640 L960,820 L1200,660 L1430,820'
          f' L1700,650 L1920,820 L1920,1080 L0,1080 Z" fill="#16203a"/>')
    s += (f'<path d="M0,820 L240,660 L470,820 M700,640 L960,820 M1200,660 L1430,820'
          f' M1700,650 L1920,820" fill="none" stroke="#e8eef9" stroke-width="14"'
          f' stroke-linejoin="round" opacity=".9"/>')
    for i, (x, y) in enumerate(((150, 880), (390, 880), (610, 900), (880, 880),
                                (1120, 900), (1360, 880), (1620, 900))):
        op = .45 + .55 * abs(A.w(t, 3.4, i * .25))
        s += (f'<rect x="{x}" y="{y}" width="96" height="86" rx="8" fill="{SVET}"'
              f' opacity="{op:.2f}" {o(5)}/>')
    # труба с дымом
    s += f'<rect x="690" y="560" width="76" height="130" rx="6" fill="#2a2a33" {o(6)}/>'
    s += f'<rect x="676" y="540" width="104" height="30" rx="8" fill="{TERRA}" {o(6)}/>'
    for i in range(4):
        p = ((t * .22) + i * .25) % 1.0
        s += (f'<circle cx="{728 + 40*A.w(t,2.4,i*.3):.0f}" cy="{520-p*230:.0f}"'
              f' r="{22*(1-p)+8:.0f}" fill="#cfd8ea" opacity="{(1-p)*.3:.2f}"/>')
    # ёлка на площади
    s += elka(1180, 1010, 330, t, pal)
    return s + sneg_sloy(t, 40, 4, .8)


def les(t, pal):
    s = f'<rect width="{W}" height="{H}" fill="#16203a"/>'
    s += sneg_sloy(t, 26, 8, .4)
    for k, (y, sc, col) in enumerate(((760, 1.0, "#0f1726"), (820, 1.4, "#14203a"), (900, 1.9, "#1b2a3f"))):
        for i in range(9):
            x = -100 + i * 260 + k * 60
            hh = 220 * sc
            ww = hh * .42
            s += (f'<path d="M{x},{y-hh:.0f} L{x-ww:.0f},{y:.0f} L{x+ww:.0f},{y:.0f} Z" fill="{col}"/>'
                  f'<path d="M{x},{y-hh*1.3:.0f} L{x-ww*.7:.0f},{y-hh*.45:.0f} L{x+ww*.7:.0f},{y-hh*.45:.0f} Z"'
                  f' fill="{col}"/>')
    s += f'<path d="M0,900 q480,-50 960,0 q480,50 960,-10 L{W},{H} L0,{H} Z" fill="#dfe8f5"/>'
    s += elka(960, 900, 460, t, pal)
    return s


def masterskaya(t, pal):
    """Стол с игрушками крупно: коробка, лента, шары, шишки."""
    s = f'<rect width="{W}" height="{H}" fill="#2e211c"/>'
    s += f'<rect y="560" width="{W}" height="520" fill="{TERRA}"/>'
    s += f'<rect y="540" width="{W}" height="36" rx="8" fill="#8a5a3c" {o(6)}/>'
    s += (f'<rect x="120" y="300" width="620" height="300" rx="16" fill="#8a5a3c" {o(9)}/>'
          f'<rect x="96" y="250" width="668" height="64" rx="12" fill="{TERRA}" {o(8)}/>')
    for i, c in enumerate((KRAS, ZOL, GRAN, KREM, VIN)):
        s += shar_zhivoy(210 + i * 120, 420, 52, c, t, i)
    s += (f'<circle cx="1180" cy="520" r="120" fill="none" stroke="{VIN}" stroke-width="56"/>'
          f'<circle cx="1180" cy="520" r="34" fill="{TERRA}" {o(6)}/>'
          f'<path d="M1300,520 q120,30 220,-40" fill="none" stroke="{VIN}" stroke-width="30"/>')
    for i, (x, y) in enumerate(((1560, 640), (1680, 680), (1460, 700))):
        s += (f'<ellipse cx="{x}" cy="{y}" rx="40" ry="56" fill="#8a5a3c" {o(6)}/>'
              f'<path d="M{x-28},{y-26} q28,16 56,0 M{x-30},{y+2} q30,16 60,0 M{x-24},{y+30} q24,12 48,0"'
              f' fill="none" stroke="#5e3a22" stroke-width="6"/>')
    s += svecha_bol(900, 360, t)
    return s


LOK = {"komnata": komnata, "kamin": kamin_krupno, "vetka": vetka_krupno, "dvor": dvor,
       "stol": stol, "prihozhaya": prihozhaya, "nebo": nebo, "les": les,
       "masterskaya": masterskaya}
