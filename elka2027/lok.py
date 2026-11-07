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
    s += f'<rect x="{cx-26}" y="{base-40}" width="52" height="60" rx="8" fill="{TERRA}" {o(6)}/>'
    for i in range(5):
        u = i / 5
        yy = base - h * u
        ww = w * (1 - u) * .5 + w * .12
        hh = h / 5 * 1.5
        s += (f'<path d="M{cx},{yy-hh:.0f} L{cx-ww:.0f},{yy:.0f} Q{cx},{yy+22:.0f} {cx+ww:.0f},{yy:.0f} Z"'
              f' fill="{HVOYA if i%2 else ZEL2}" {o(6)}/>')
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
    return (f'<rect x="{x-16}" y="{y}" width="32" height="90" rx="6" fill="{KREM}" {o(6)}/>'
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
        for i in range(18):
            u = i / 17
            x = -40 + u * 1960
            y = yy + (70 + k * 20) * math.sin(math.pi * u) * .5
            s += (f'<path d="M{x:.0f},{y:.0f} l{-18-10*(i%3)},{-26-8*(i%2)}"'
                  f' stroke="{ZEL2}" stroke-width="7" stroke-linecap="round"/>')
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
    s += f'<path d="M0,760 q300,-70 620,-30 q420,50 760,-40 q320,-80 540,10 L{W},{H} L0,{H} Z" fill="#dfe8f5"/>'
    s += f'<path d="M0,880 q420,-60 900,10 q480,70 1020,-30 L{W},{H} L0,{H} Z" fill="#ffffff"/>'
    # дом справа
    s += f'<rect x="1280" y="420" width="520" height="360" fill="#3a2a30" {o(8)}/>'
    s += f'<path d="M1240,420 L1540,250 L1840,420 Z" fill="{TERRA}" {o(8)}/>'
    for i, (x, y) in enumerate(((1360, 500), (1560, 500), (1360, 650), (1560, 650))):
        op = .55 + .45 * abs(A.w(t, 3.2, i * .3))
        s += f'<rect x="{x}" y="{y}" width="110" height="100" rx="8" fill="{SVET}" opacity="{op:.2f}" {o(5)}/>'
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
    sw = 2.4 * A.w(t, 4.2)
    g = f'<g transform="rotate({sw:.2f} {cx} {base})">'
    g += f'<ellipse cx="{cx}" cy="{base-70*s:.0f}" rx="{110*s:.0f}" ry="{96*s:.0f}" fill="#ffffff" {o(7)}/>'
    g += f'<ellipse cx="{cx}" cy="{base-210*s:.0f}" rx="{82*s:.0f}" ry="{74*s:.0f}" fill="#ffffff" {o(7)}/>'
    g += f'<circle cx="{cx}" cy="{base-320*s:.0f}" r="{60*s:.0f}" fill="#ffffff" {o(7)}/>'
    g += (f'<path d="M{cx-66*s:.0f},{base-250*s:.0f} q66,34 132,0 l6,30 q-72,34 -144,0 Z"'
          f' fill="{sharf}" {o(6)}/>'
          f'<path d="M{cx+50*s:.0f},{base-240*s:.0f} q30,60 10,110" fill="none" stroke="{sharf}"'
          f' stroke-width="{22*s:.0f}" stroke-linecap="round"/>')
    g += (f'<rect x="{cx-56*s:.0f}" y="{base-396*s:.0f}" width="{112*s:.0f}" height="{22*s:.0f}"'
          f' rx="6" fill="{K}"/>'
          f'<rect x="{cx-38*s:.0f}" y="{base-470*s:.0f}" width="{76*s:.0f}" height="{80*s:.0f}"'
          f' rx="6" fill="{K}"/>')
    for dx in (-22, 22):
        g += f'<circle cx="{cx+dx*s:.0f}" cy="{base-334*s:.0f}" r="{8*s:.1f}" fill="{K}"/>'
    g += f'<path d="M{cx:.0f},{base-316*s:.0f} l{44*s:.0f},{10*s:.0f} l{-44*s:.0f},{14*s:.0f} Z" fill="{ORA}" {o(4)}/>'
    for i, dx in enumerate((-30, 0, 30)):
        g += f'<circle cx="{cx+dx*s:.0f}" cy="{base-290*s+i*4:.0f}" r="{5*s:.1f}" fill="{K}"/>'
    for sgn in (-1, 1):
        g += (f'<path d="M{cx+sgn*86*s:.0f},{base-220*s:.0f} l{sgn*90*s:.0f},{-70*s:.0f}"'
              f' stroke="{TERRA}" stroke-width="{13*s:.0f}" stroke-linecap="round"/>')
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
    s += (f'<ellipse cx="420" cy="520" rx="110" ry="130" fill="{ZOL}" {o(8)}/>'
          f'<rect x="380" y="330" width="80" height="70" rx="10" fill="{ZOL}" {o(7)}/>'
          f'<circle cx="420" cy="320" r="26" fill="{ORA}" {o(6)}/>'
          f'<path d="M530,500 q50,-10 44,-60" fill="none" stroke="{ZOL}" stroke-width="16"/>')
    for i in range(3):
        p = ((t * .3) + i * .33) % 1.0
        s += (f'<path d="M420,{300-p*180:.0f} q{18*A.w(t,2.2,i*.3):.0f},-40 0,-70" fill="none"'
              f' stroke="#cfd8ea" stroke-width="9" opacity="{(1-p)*.5:.2f}" stroke-linecap="round"/>')
    # мандарины
    for i, (x, y) in enumerate(((760, 560), (830, 590), (700, 600), (790, 630))):
        s += (f'<circle cx="{x}" cy="{y}" r="44" fill="{ORA}" {o(6)}/>'
              f'<path d="M{x},{y-44} q10,-18 26,-20" fill="none" stroke="{ZEL2}" stroke-width="8"/>')
    # бокалы
    for i, x in enumerate((1180, 1320, 1460)):
        # бокал: чаша полукругом, ножка, основание — иначе читается конусом
        s += (f'<path d="M{x-52},430 a52,86 0 0 0 104,0 Z" fill="{VIN}" opacity=".9"/>'
              f'<path d="M{x-52},430 a52,86 0 0 0 104,0" fill="none" {o(5, "#dfe8f5")}/>'
              f'<path d="M{x-52},430 h104" stroke="#dfe8f5" stroke-width="5"/>'
              f'<rect x="{x-5}" y="514" width="10" height="84" fill="#dfe8f5"/>'
              f'<ellipse cx="{x}" cy="606" rx="46" ry="12" fill="#dfe8f5" {o(4)}/>')
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
    """Ночное небо над крышами + салют."""
    s = f'<rect width="{W}" height="{H}" fill="#101a33"/>'
    import random as _r
    r = _r.Random(7)
    for i in range(90):
        s += (f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,700):.0f}" r="{r.uniform(1,2.6):.1f}"'
              f' fill="#ffffff" opacity="{.25+.6*abs(A.w(t,2.8,i*.07)):.2f}"/>')
    for k in range(3):
        ph = k * .33
        p = ((t * .35) + ph) % 1.0
        cx = 420 + k * 520
        cy = 300 + 60 * k
        R = 40 + p * 260
        for i in range(16):
            a = i * 22.5 * math.pi / 180
            s += (f'<circle cx="{cx+R*math.cos(a):.0f}" cy="{cy+R*math.sin(a)*.8:.0f}" r="{6*(1-p)+2:.1f}"'
                  f' fill="{[SVET, KRAS, "#9ee07f"][k%3]}" opacity="{max(0,.9-p):.2f}"/>')
    s += f'<path d="M0,760 L220,640 L420,760 L640,620 L880,760 L1120,640 L1360,760 L1620,620 L1920,760 L1920,1080 L0,1080 Z" fill="#141d33"/>'
    for i, x in enumerate((180, 520, 980, 1480)):
        op = .5 + .5 * abs(A.w(t, 3.4, i * .25))
        s += f'<rect x="{x}" y="820" width="90" height="80" rx="8" fill="{SVET}" opacity="{op:.2f}"/>'
    s += f'<rect x="700" y="600" width="70" height="120" rx="6" fill="#2a2a33"/>'
    for i in range(3):
        p = ((t * .25) + i * .33) % 1.0
        s += (f'<circle cx="{735 + 30*A.w(t,2.4,i*.3):.0f}" cy="{590-p*200:.0f}" r="{18*(1-p)+6:.0f}"'
              f' fill="#cfd8ea" opacity="{(1-p)*.35:.2f}"/>')
    return s + sneg_sloy(t, 34, 4, .7)


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
