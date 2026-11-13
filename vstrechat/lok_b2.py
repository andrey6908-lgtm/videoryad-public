# -*- coding: utf-8 -*-
"""Декорации планов 21-42 ролика «Как встречать год хозяйки года 2027»."""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob
OKNO = (860, 300, 980, 551)


# ═══════════════ СЛУЖЕБНЫЕ КИРПИЧИКИ ЭТОГО БЛОКА ═══════════════

def _medal(cx, cy, r, vnutri="", pole="#1b2740", sv=0.0, obod="url(#zol)"):
    """Медальон знака: золотой обод, тёмное поле, блик. `sv` — подсветка."""
    s = ten(cx + 5, cy + r * .94, r * .88, r * .24, .45)
    s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{obod}" {o(5)}/>'
    s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.83:.0f}" fill="{pole}" {o(4)}/>'
    if sv > .01:
        s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.83:.0f}" fill="{KRAS}"'
              f' opacity="{.8*sv:.2f}"/>')
        s += teplo(cx, cy, r * 2.6, r * 2.6, .6 * sv)
    s += vnutri
    s += (f'<path d="M{cx-r*.58:.0f},{cy-r*.52:.0f} a{r*.82:.0f},{r*.82:.0f} 0 0 1'
          f' {r*.86:.0f},{-r*.2:.0f}" fill="none" stroke="#fff6d2" stroke-width="5"'
          f' opacity=".32"/>')
    return s


def _zver(cx, cy, s_, i, t, col="#e2e9f4"):
    """Силуэт знака восточного круга. Условный, но все двенадцать разные:
    одинаковые кружки в круге читаются как орнамент, а не как знаки."""
    hv = 8 * A.w(t, 2.4 + (i % 5) * .35, i * .13)
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s_:.3f})" fill="{col}">'
    if i == 5:                                   # змея
        g += (f'<path d="M-46,28 q34,-26 2,-44 q-32,-20 4,-42 q26,-14 48,4" fill="none"'
              f' stroke="{col}" stroke-width="15" stroke-linecap="round"/>'
              f'<circle cx="18" cy="-58" r="12"/>'
              f'<path d="M28,-58 l18,4 l-18,6 z"/>')
    elif i == 9:                                 # петух
        g += ('<ellipse cx="-6" cy="10" rx="36" ry="29"/>'
              '<circle cx="26" cy="-24" r="18"/>'
              '<path d="M26,-46 q7,-15 15,-2 q9,-13 13,3 z"/>'
              '<path d="M44,-22 l19,7 l-19,7 z"/>'
              f'<path d="M-36,0 q-30,-24 -44,10 q28,14 44,-10 z"'
              f' transform="rotate({hv:.1f},-36,0)"/>'
              '<rect x="-14" y="36" width="8" height="20" rx="4"/>'
              '<rect x="8" y="36" width="8" height="20" rx="4"/>')
    else:                                        # четвероногие
        P = {0:  (30, 19, 14, "krug",   0, "tonkiy"),
             1:  (46, 31, 18, "malo",   2, "kist"),
             2:  (44, 26, 20, "malo",   0, "vverh"),
             3:  (32, 22, 16, "dlin",   0, "pushok"),
             4:  (42, 23, 34, "greben", 1, "vverh"),
             6:  (46, 28, 32, "griva",  0, "kist"),
             8:  (34, 31, 14, "krug",   0, "zavit"),
             10: (41, 24, 22, "ostro",  0, "vverh"),
             11: (44, 31, 10, "malo",   0, "zavit")}
        bw, bh, nl, ush, rog, hvt = P.get(i, (42, 26, 20, "malo", 0, "vverh"))
        g += f'<ellipse cx="-8" cy="6" rx="{bw}" ry="{bh}"/>'
        for lx in (-bw * .62, -bw * .2, bw * .28, bw * .62):
            g += (f'<rect x="{lx:.0f}" y="{bh+1:.0f}" width="10" height="24" rx="5"/>')
        hx, hy = bw * .76, 6 - nl
        g += (f'<path d="M{bw*.3:.0f},{-bh*.6:.0f} L{hx-10:.0f},{hy+6:.0f}'
              f' l22,10 l{-bw*.32:.0f},{bh*.8:.0f} z"/>')
        g += f'<ellipse cx="{hx+8:.0f}" cy="{hy:.0f}" rx="20" ry="15"/>'
        g += f'<path d="M{hx+24:.0f},{hy-4:.0f} l20,8 l-20,9 z"/>'
        if ush == "dlin":
            for dx in (-2, 12):
                g += (f'<ellipse cx="{hx+dx:.0f}" cy="{hy-34:.0f}" rx="8" ry="27"'
                      f' transform="rotate({-14+dx*.6+hv*.3:.1f},{hx+dx:.0f},{hy-34:.0f})"/>')
        elif ush == "krug":
            for dx in (-10, 16):
                g += f'<circle cx="{hx+dx:.0f}" cy="{hy-20:.0f}" r="13"/>'
        elif ush == "ostro":
            for dx in (-6, 14):
                g += f'<path d="M{hx+dx:.0f},{hy-10:.0f} l-3,-26 l19,10 z"/>'
        elif ush == "greben":
            for k in range(4):
                g += (f'<path d="M{hx-18+k*11:.0f},{hy-16:.0f} l5,-20 l7,18 z"/>')
        elif ush == "griva":
            for k in range(5):
                g += (f'<path d="M{bw*.34+k*9:.0f},{-bh*.6-k*5:.0f} q-14,-16 -8,-32"'
                      f' fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/>')
        else:
            g += f'<path d="M{hx-4:.0f},{hy-12:.0f} l0,-18 l16,9 z"/>'
        if rog == 2:
            for sg in (-1, 1):
                g += (f'<path d="M{hx+4:.0f},{hy-14:.0f} q{sg*30:.0f},-16 {sg*34:.0f},-34"'
                      f' fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/>')
        elif rog == 1:
            g += (f'<path d="M{hx:.0f},{hy-16:.0f} q10,-34 -14,-46" fill="none"'
                  f' stroke="{col}" stroke-width="8" stroke-linecap="round"/>')
        if hvt == "tonkiy":
            g += (f'<path d="M{-bw:.0f},0 q-34,{10+hv:.0f} -40,{40+hv:.0f}" fill="none"'
                  f' stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
        elif hvt == "zavit":
            g += (f'<path d="M{-bw:.0f},-4 q-26,{-6+hv:.0f} -16,{-24:.0f} q8,-12 18,-2"'
                  f' fill="none" stroke="{col}" stroke-width="8" stroke-linecap="round"/>')
        elif hvt == "vverh":
            g += (f'<path d="M{-bw:.0f},-6 q-30,{-20+hv:.0f} -24,{-54+hv:.0f}" fill="none"'
                  f' stroke="{col}" stroke-width="11" stroke-linecap="round"/>')
        elif hvt == "pushok":
            g += f'<circle cx="{-bw-12:.0f}" cy="{hv*.4:.0f}" r="13"/>'
        else:
            g += (f'<path d="M{-bw:.0f},-8 q-28,{14+hv:.0f} -26,{46+hv:.0f}" fill="none"'
                  f' stroke="{col}" stroke-width="10" stroke-linecap="round"/>')
    return g + '</g>'


def _ovca(x, base, t, s_=1.0, ph=0.0, vlevo=True, sher="#f2ece0"):
    """Кудрявая овца: руно кружками, тёмная морда, глаз моргает."""
    sgn = -1 if vlevo else 1
    kach = 2.2 * A.w(t, 2.2, ph)
    g = (f'<g transform="translate({x:.1f},{base:.1f}) scale({sgn*s_:.3f},{s_:.3f})">')
    g += ten(0, 6, 128, 24, .5)
    for nx in (-70, -30, 36, 74):
        g += (f'<rect x="{nx-11:.0f}" y="-86" width="22" height="92" rx="10"'
              f' fill="#6b5f52" {o(4)}/>')
        g += f'<rect x="{nx-13:.0f}" y="-12" width="26" height="18" rx="6" fill="{CHUGUN}" {o(3)}/>'
    g += f'<g transform="translate(0,{kach:.1f})">'
    g += (f'<ellipse cx="-4" cy="-158" rx="122" ry="84" fill="{sher}" {o(8)}/>')
    r = random.Random(7)
    for k in range(22):
        a = k * 2 * math.pi / 22
        g += (f'<circle cx="{-4+120*math.cos(a):.0f}" cy="{-158+82*math.sin(a):.0f}"'
              f' r="{r.uniform(24,34):.0f}" fill="{sher}" {o(5)}/>')
    for k in range(7):
        g += (f'<circle cx="{-70+k*24:.0f}" cy="{-186+((k*37)%40):.0f}" r="16"'
              f' fill="#ddd4c4" opacity=".7"/>')
    hx, hy = 112, -208
    g += f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="46" ry="40" fill="#5f5349" {o(6)}/>'
    g += f'<path d="M{hx+22:.0f},{hy-6:.0f} q36,10 34,34 q-28,14 -44,-6 z" fill="#4c4138" {o(5)}/>'
    uh = 9 * A.w(t, 1.6, ph + .4)
    g += (f'<ellipse cx="{hx-18:.0f}" cy="{hy-18:.0f}" rx="30" ry="14" fill="#4c4138" {o(5)}'
          f' transform="rotate({-26+uh:.1f},{hx-18:.0f},{hy-18:.0f})"/>')
    g += f'<circle cx="{hx-6:.0f}" cy="{hy-40:.0f}" r="26" fill="{sher}" {o(5)}/>'
    if A.blink(t, 3.4, ph, .3):
        g += f'<path d="M{hx+18:.0f},{hy-4:.0f} q11,8 22,0" fill="none" {o(6)}/>'
    else:
        g += f'<ellipse cx="{hx+28:.0f}" cy="{hy-6:.0f}" rx="11" ry="12" fill="#17120f"/>'
        g += f'<circle cx="{hx+32:.0f}" cy="{hy-10:.0f}" r="4" fill="#fff" opacity=".85"/>'
    g += f'<circle cx="{hx+56:.0f}" cy="{hy+22:.0f}" r="5" fill="#2a2420"/>'
    g += '</g></g>'
    return g


def _baran(x, base, t, s_=1.0, ph=0.0, vlevo=False):
    """Баран: то же руно темнее и крученый рог — третий силуэт знака 羊."""
    g = _ovca(x, base, t, s_, ph, vlevo, "#d9cdb4")
    sgn = -1 if vlevo else 1
    kach = 2.2 * A.w(t, 2.2, ph)
    g += (f'<g transform="translate({x:.1f},{base+kach:.1f}) scale({sgn*s_:.3f},{s_:.3f})">')
    for k in range(3):
        rr = 44 - k * 12
        a0 = -.4 + k * 1.9
        g += (f'<path d="M{100+rr*math.cos(a0):.0f},{-222+rr*math.sin(a0):.0f}'
              f' a{rr:.0f},{rr:.0f} 0 1 1 {-rr*.3:.0f},{rr*1.5:.0f}" fill="none"'
              f' stroke="url(#med)" stroke-width="{19-k*4}" stroke-linecap="round"/>')
    g += '</g>'
    return g


def _vorona(x, y, t, s_=1.0, ph=0.0):
    """Ворона в полёте: крылья машут, голова поворачивается."""
    kr = 30 * A.w(t, .52, ph)
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += f'<path d="M-6,-6 q26,{-34-kr:.0f} 60,{-20-kr*.6:.0f} q-28,28 -50,26 z" fill="#2b303c"/>'
    g += '<ellipse cx="0" cy="0" rx="36" ry="21" fill="#20242e"/>'
    g += '<path d="M-32,-2 l-40,18 l34,8 z" fill="#20242e"/>'
    g += f'<circle cx="30" cy="-13" r="15" fill="#20242e"/>'
    g += '<path d="M43,-13 l22,6 l-22,7 z" fill="#4a3c28"/>'
    g += '<circle cx="35" cy="-18" r="3.4" fill="#d8cfb8"/>'
    g += f'<path d="M-6,-6 q-26,{-34+kr:.0f} -60,{-20+kr*.6:.0f} q28,28 50,26 z" fill="#161a21"/>'
    return g + '</g>'


def _fonar(cx, cy, sc, t, gor=1.0, ph=0.0):
    """Китайский фонарь: красный бочонок, золотые обручи, кисть качается."""
    kist = 8 * A.w(t, 2.3, ph)
    col = KRAS if gor > .45 else "#5a2a25"
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) scale({sc:.3f})">'
    g += '<path d="M0,-76 v26" fill="none" stroke="#5a4a33" stroke-width="5"/>'
    g += f'<rect x="-26" y="-54" width="52" height="15" rx="5" fill="url(#zol)" {o(4)}/>'
    g += f'<ellipse cx="0" cy="0" rx="58" ry="50" fill="{col}" {o(6)}/>'
    for k in (-36, -17, 2, 21, 40):
        g += (f'<path d="M{k},-42 q{-k*.22:.0f},42 0,84" fill="none" stroke="{UGOL}"'
              f' stroke-width="4" opacity=".5"/>')
    g += f'<rect x="-26" y="40" width="52" height="15" rx="5" fill="url(#zol)" {o(4)}/>'
    g += (f'<g transform="rotate({kist:.1f} 0 55)">'
          f'<path d="M0,55 v34" fill="none" stroke="{ZOL}" stroke-width="6"/>'
          f'<path d="M-15,89 h30 l-6,42 h-18 z" fill="{ZOL}" {o(4)}/></g>')
    if gor > .02:
        g += f'<ellipse cx="-19" cy="-12" rx="14" ry="21" fill="#ff9d87" opacity="{.55*gor:.2f}"/>'
        g += teplo(0, 0, 168, 158, .6 * gor)
    return g + '</g>'


def _stolb(x, base, h_, t, sv=0.0, sc=1.0):
    """Верстовой столб: полосы, табличка (текст кладёт over), шапка снега."""
    w_ = 30 * sc
    g = ten(x + 8 * sc, base + 6, 58 * sc, 15 * sc, .5)
    g += f'<rect x="{x-w_/2:.0f}" y="{base-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8" fill="url(#krem)" {o(5)}/>'
    n = max(3, int(h_ / (56 * sc)))
    for k in range(n):
        if k % 2 == 0:
            g += (f'<rect x="{x-w_/2:.0f}" y="{base-h_+k*h_/n:.0f}" width="{w_:.0f}"'
                  f' height="{h_/n:.0f}" fill="{KRAS}" opacity=".88"/>')
    tw, th = 150 * sc, 86 * sc
    ty = base - h_ - th * .2
    g += ten(x + 10 * sc, ty + th + 10, tw * .5, 12 * sc, .4)
    g += (f'<rect x="{x-tw/2:.0f}" y="{ty:.0f}" width="{tw:.0f}" height="{th:.0f}" rx="9"'
          f' fill="url(#dosk)" {o(5)}/>')
    g += (f'<rect x="{x-tw/2+9*sc:.0f}" y="{ty+9*sc:.0f}" width="{tw-18*sc:.0f}"'
          f' height="{th-18*sc:.0f}" rx="6" fill="#f3e7cb" opacity=".92" {o(3)}/>')
    if sv > .01:
        g += (f'<rect x="{x-tw/2:.0f}" y="{ty:.0f}" width="{tw:.0f}" height="{th:.0f}" rx="9"'
              f' fill="{SVET}" opacity="{.5*sv:.2f}"/>')
        g += teplo(x, ty + th / 2, tw * 1.5, th * 2.0, .55 * sv)
    g += (f'<path d="M{x-tw/2-6:.0f},{ty+2:.0f} q{tw/2:.0f},{-26*sc:.0f} {tw+12:.0f},0'
          f' q{-tw/2:.0f},{14*sc:.0f} {-tw-12:.0f},0 z" fill="url(#sneg)" {o(4)}/>')
    return g


def _flazhok(x, base, h_, t, ph=0.0, col=None, sgn=1):
    """Флажок на шесте: полотнище треплется, древко с золотым навершием."""
    c = col or ob.ALYJ
    g = ten(x + 6, base + 5, 40, 11, .45)
    g += f'<rect x="{x-7:.0f}" y="{base-h_:.0f}" width="14" height="{h_:.0f}" rx="6" fill="url(#derev)" {o(5)}/>'
    g += f'<circle cx="{x:.0f}" cy="{base-h_-14:.0f}" r="15" fill="url(#zol)" {o(5)}/>'
    v1 = 20 * A.w(t, 1.1, ph)
    v2 = 26 * A.w(t, 1.1, ph + .32)
    y0 = base - h_ + 20
    g += (f'<path d="M{x:.0f},{y0:.0f} q{sgn*78:.0f},{v1:.0f} {sgn*158:.0f},{v2*.5:.0f}'
          f' l0,106 q{-sgn*80:.0f},{-v2*.5+14:.0f} {-sgn*158:.0f},{-v1*.6+8:.0f} z"'
          f' fill="{c}" {o(6)}/>')
    g += (f'<path d="M{x+sgn*22:.0f},{y0+22:.0f} q{sgn*60:.0f},{v1*.6+10:.0f} {sgn*120:.0f},{v2*.4+6:.0f}"'
          f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="7" opacity=".75"/>')
    return g


def _koleso(cx, cy, R, zub, ang, t, col="url(#derev)"):
    """Деревянное зубчатое колесо: обод, зубья, спицы, ступица, блик."""
    g = ten(cx + 10, cy + R * .96, R * .82, R * .2, .45)
    g += f'<g transform="rotate({ang:.2f} {cx:.1f} {cy:.1f})">'
    for k in range(zub):
        a = k * 2 * math.pi / zub
        zx, zy = cx + R * math.cos(a), cy + R * math.sin(a)
        g += (f'<rect x="{zx-R*.1:.0f}" y="{zy-R*.08:.0f}" width="{R*.2:.0f}" height="{R*.16:.0f}"'
              f' rx="{R*.04:.0f}" fill="{col}" {o(5)}'
              f' transform="rotate({math.degrees(a):.1f} {zx:.0f} {zy:.0f})"/>')
    g += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R:.0f}" fill="{col}" {o(7)}/>'
    g += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R*.74:.0f}" fill="#2a1f16" opacity=".35"/>'
    g += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R*.7:.0f}" fill="{col}" {o(5)}/>'
    for k in range(6):
        a = k * math.pi / 3
        g += (f'<rect x="{cx-R*.055:.0f}" y="{cy-R*.7:.0f}" width="{R*.11:.0f}" height="{R*1.4:.0f}"'
              f' rx="{R*.05:.0f}" fill="{col}" {o(4)}'
              f' transform="rotate({math.degrees(a):.1f} {cx:.0f} {cy:.0f})"/>')
    g += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R*.19:.0f}" fill="url(#med)" {o(6)}/>'
    g += '</g>'
    g += (f'<path d="M{cx-R*.62:.0f},{cy-R*.56:.0f} a{R*.86:.0f},{R*.86:.0f} 0 0 1'
          f' {R*.9:.0f},{-R*.2:.0f}" fill="none" stroke="#ffe9bb" stroke-width="7"'
          f' opacity="{.2+.18*abs(A.w(t,3.4)):.2f}"/>')
    return g


def _vorota(cx, base, h_, t, sc=1.0, ph=0.0, op=1.0):
    """Огненные ворота: два столба в пламени и горящая перемычка."""
    w_ = h_ * .54
    g = f'<g opacity="{op:.2f}">'
    for sgn in (-1, 1):
        px = cx + sgn * w_ * .5
        g += (f'<rect x="{px-15*sc:.0f}" y="{base-h_:.0f}" width="{30*sc:.0f}"'
              f' height="{h_:.0f}" rx="12" fill="{UGOL}" {o(5)}/>')
        for k in range(4):
            g += baza.ogon(px, base - h_ * (.1 + k * .27), t, .46 * sc, ph + k * .23, 3)
    g += (f'<path d="M{cx-w_*.5:.0f},{base-h_:.0f} q{w_*.5:.0f},{-h_*.44:.0f} {w_:.0f},0"'
          f' fill="none" stroke="{ORA}" stroke-width="{22*sc:.0f}" stroke-linecap="round"'
          f' opacity="{.6+.4*abs(A.w(t,1.15,ph)):.2f}"/>')
    g += (f'<path d="M{cx-w_*.44:.0f},{base-h_-6:.0f} q{w_*.44:.0f},{-h_*.4:.0f} {w_*.88:.0f},0"'
          f' fill="none" stroke="{SVET}" stroke-width="{9*sc:.0f}" stroke-linecap="round"'
          f' opacity="{.5+.45*abs(A.w(t,.82,ph+.4)):.2f}"/>')
    g += baza.ogon(cx, base - h_ * 1.14, t, .62 * sc, ph + .5, 5)
    g += teplo(cx, base - h_ * .62, w_ * 1.5, h_ * .95, .5)
    return g + '</g>'


def _gazeta(x, y, w_, h_, t, ph=0.0, podsvet=0.0, naklon=0.0):
    """Газетная полоса: кремовая бумага, шапка, колонки линейками, шуршащий край."""
    g = f'<g transform="rotate({naklon:.2f} {x+w_/2:.0f} {y+h_/2:.0f})">'
    g += ten(x + w_ / 2 + 14, y + h_ + 22, w_ * .5, 26, .5)
    sh = 16 * A.w(t, 1.7, ph)
    sh2 = 13 * A.w(t, 1.7, ph + .35)
    g += (f'<path d="M{x:.0f},{y:.0f} h{w_:.0f} q{sh:.0f},{h_*.34:.0f} 0,{h_*.66:.0f}'
          f' q{sh2:.0f},{h_*.2:.0f} {-6:.0f},{h_*.34:.0f} L{x:.0f},{y+h_:.0f} z"'
          f' fill="url(#list)" {o(6)}/>')
    g += (f'<rect x="{x+26:.0f}" y="{y+26:.0f}" width="{w_-56:.0f}" height="{h_*.17:.0f}"'
          f' rx="8" fill="#e6dcc0" {o(4)}/>')
    if podsvet > .01:
        g += (f'<rect x="{x+26:.0f}" y="{y+26:.0f}" width="{w_-56:.0f}" height="{h_*.17:.0f}"'
              f' rx="8" fill="{SVET}" opacity="{.62*podsvet:.2f}"/>')
        g += teplo(x + w_ / 2, y + 26 + h_ * .085, w_ * .74, h_ * .3, .55 * podsvet)
    g += (f'<line x1="{x+26:.0f}" y1="{y+h_*.215:.0f}" x2="{x+w_-30:.0f}"'
          f' y2="{y+h_*.215:.0f}" stroke="#8a7c5e" stroke-width="5"/>')
    r = random.Random(int(x) + 3)
    for c in range(3):
        cx0 = x + 34 + c * (w_ - 60) / 3
        cw = (w_ - 60) / 3 - 22
        for k in range(14):
            ln = cw * r.uniform(.55, 1.0)
            g += (f'<rect x="{cx0:.0f}" y="{y+h_*.26+k*h_*.049:.0f}" width="{ln:.0f}"'
                  f' height="7" rx="3" fill="#9a8d72" opacity=".6"/>')
        if c == 1:
            g += (f'<rect x="{cx0-4:.0f}" y="{y+h_*.52:.0f}" width="{cw+8:.0f}"'
                  f' height="{h_*.2:.0f}" rx="6" fill="#cdc0a2" {o(3)}/>')
    return g + '</g>'


# ═══════════════ ДЕКОРАЦИИ ═══════════════

def hozyayka_goda_na_snezhnom_holme(t):
    """Коза-хозяйка во весь рост на снежном холме, розовый рассвет.
    Живое: шерсть светится на рассвете, бубенчик качается, пар от дыхания."""
    zar = .55 + .45 * A.ease(A.seg(t, 0.0, 3.2))
    puls = .78 + .22 * abs(A.w(t, 3.6))
    s = SL(Z_NEBO, baza.nebo("rassv", t, zvezdy=False)
           + f'<rect y="320" width="{W}" height="460" fill="#e8a898" opacity="{.34*zar:.2f}"/>'
           + f'<rect y="520" width="{W}" height="260" fill="#f2c4a4" opacity="{.4*zar:.2f}"/>'
           + f'<ellipse cx="1430" cy="520" rx="760" ry="420" fill="url(#teplo)" opacity="{.5*zar:.2f}"/>'
           + f'<circle cx="1440" cy="512" r="118" fill="#ffe3cc" opacity="{.75*zar:.2f}"/>'
           + f'<circle cx="1440" cy="512" r="196" fill="#ffd0b2" opacity="{.3*zar:.2f}"/>'
           + baza.oblaka(t, 300, 5, 7, .34, "#f7cfc4", 6.0))
    d = (f'<path d="M-20,768 q300,-124 640,-58 q360,66 700,-92 q340,-150 640,-38'
         f' L1940,1080 L-20,1080 z" fill="#b6c7e0" opacity=".9" {o(5)}/>')
    for i in range(14):
        ex = -40 + i * 150 + 30 * math.sin(i * 2.1)
        eh = 72 + 34 * math.sin(i * 1.7)
        ey = 748 + 16 * math.sin(i * .9)
        d += (f'<path d="M{ex:.0f},{ey:.0f} l{-eh*.34:.0f},0 l{eh*.34:.0f},{-eh:.0f}'
              f' l{eh*.34:.0f},{eh:.0f} z" fill="#6d80a2" opacity=".82"/>')
    d += (f'<path d="M1372,752 l-18,0 l18,-56 l18,56 z" fill="#5a6c8e" opacity=".9"/>')
    s += SL(Z_DAL, d)
    m = (f'<path d="M-40,1080 C240,972 540,820 900,792 C1270,814 1600,948 1960,1080 z"'
         f' fill="url(#sneg)" {o(7)}/>')
    m += (f'<path d="M160,1012 C420,916 650,846 900,826 C1180,848 1470,930 1760,1020"'
          f' fill="none" stroke="#c3d6ea" stroke-width="7" opacity=".7"/>')
    r = random.Random(4)
    for i in range(26):
        sx, sy = r.uniform(80, 1840), r.uniform(840, 1060)
        s_op = .25 + .7 * abs(A.w(t, 2.0 + r.uniform(0, 2.4), i * .12))
        m += f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{r.uniform(2.4,4.6):.1f}" fill="#fff" opacity="{s_op:.2f}"/>'
    m += teplo(900, 560, 430, 380, (.28 + .24 * zar) * puls)
    m += ob.koza(880, 800, t, 1.44, 0.0, True, .1)
    m += baza.par(1276, 326, t, 6, .6, 200, .46, 1.5)
    # куст и жердь под снегом: правая половина кадра не должна стоять пустой
    for bx, bs in ((1510, 1.05), (1676, .8), (1792, .6)):
        for k in range(9):
            a = -2.6 + k * .33
            m += (f'<path d="M{bx:.0f},1004 q{math.cos(a)*46*bs:.0f},{-54*bs:.0f}'
                  f' {math.cos(a)*74*bs+6*A.w(t,5.0,k*.2):.0f},{-120*bs:.0f}" fill="none"'
                  f' stroke="#6b5a48" stroke-width="{8*bs:.0f}" stroke-linecap="round"/>')
        m += (f'<path d="M{bx-72*bs:.0f},1000 q{72*bs:.0f},{-34*bs:.0f} {144*bs:.0f},0'
              f' q{-72*bs:.0f},{22*bs:.0f} {-144*bs:.0f},0 z" fill="url(#sneg)" {o(4)}/>')
    m += (f'<rect x="1368" y="846" width="22" height="168" rx="8" fill="url(#derev)" {o(5)}/>'
          f'<path d="M1354,848 q25,-26 50,0 q-25,16 -50,0 z" fill="url(#sneg)" {o(4)}/>'
          f'<path d="M1379,880 q84,-16 140,8" fill="none" stroke="#6b5a48" stroke-width="7"'
          f' stroke-linecap="round"/>')
    s += SL(Z_SRED, m)
    p = (f'<path d="M-40,1080 q380,-96 760,-40 q400,60 780,-28 q220,-50 440,6 L1960,1080 z"'
         f' fill="#f4f8ff" {o(6)}/>')
    s += SL(Z_PERED, p)
    s += SL(Z_LETIT, baza.sneg_letit(t, 44, 5, .7, .8))
    s += baza.vinetka(.36)
    return s


def svitok_vostochnogo_kalendarya(t):
    """Бумажный свиток разворачивается сверху вниз, на нём двенадцать знаков;
    живое: разворот, обводка кистью восьмого знака, покачивание бумаги."""
    razv = A.out(A.seg(t, 0.15, 2.4))
    L = 140 + 800 * razv
    kach = 1.0 * A.w(t, 4.4)
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#2a1f18"/>'
           + baza.doski(-20, -20, W + 40, H + 40, 118, False, "derev")
           + f'<rect width="{W}" height="{H}" fill="#1a1109" opacity=".42"/>'
           + teplo(760, 420, 940, 880, .5))
    s += SL(Z_DAL, baza.polka(1150, 900, 620)
            + ten(760, 1010, 420, 40, .55))
    x0, w_ = 430, 660
    g = f'<g transform="rotate({kach:.2f} 760 128)">'
    g += ten(x0 + w_ / 2 + 20, 128 + L + 26, w_ * .46, 24, .45)
    g += (f'<rect x="{x0:.0f}" y="128" width="{w_}" height="{L:.0f}" fill="url(#list)" {o(6)}/>')
    g += (f'<path d="M760,24 v84" fill="none" stroke="#5a4a33" stroke-width="6"/>')
    g += (f'<rect x="{x0-46:.0f}" y="84" width="{w_+92}" height="48" rx="24"'
          f' fill="url(#derev)" {o(7)}/>')
    g += (f'<circle cx="{x0-40:.0f}" cy="108" r="22" fill="url(#med)" {o(5)}/>'
          f'<circle cx="{x0+w_+40:.0f}" cy="108" r="22" fill="url(#med)" {o(5)}/>')
    g += (f'<rect x="{x0-46:.0f}" y="{128+L-14:.0f}" width="{w_+92}" height="48" rx="24"'
          f' fill="url(#derev)" {o(7)}/>')
    g += (f'<circle cx="{x0-40:.0f}" cy="{128+L+10:.0f}" r="22" fill="url(#med)" {o(5)}/>'
          f'<circle cx="{x0+w_+40:.0f}" cy="{128+L+10:.0f}" r="22" fill="url(#med)" {o(5)}/>')
    g += (f'<rect x="{x0+18:.0f}" y="146" width="{w_-36}" height="{max(10,L-36):.0f}"'
          f' fill="none" stroke="{ob.ALYJ2}" stroke-width="5" opacity=".65"/>')
    for i in range(12):
        row, col = i // 2, i % 2
        mx = x0 + 176 + col * 310
        my = 232 + row * 140
        if my - 64 > 128 + L:
            continue
        sv = A.out(A.seg(t, 2.1, .8)) if i == 7 else 0.0
        vn = (ob.koza_malaya(mx - 16, my + 30, t, .20, .2) if i == 7
              else _zver(mx, my, .62, i, t, "#2c2318"))
        g += _medal(mx, my, 58, vn, "#efe3c6", sv, "url(#med)")
    # кисть обводит восьмой знак
    kx, ky = x0 + 176 + 310, 232 + 3 * 140
    pr = A.ease(A.seg(t, 1.5, 1.4))
    dl = 2 * math.pi * 76
    g += (f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="76" fill="none" stroke="{ob.ALYJ}"'
          f' stroke-width="11" stroke-linecap="round" stroke-dasharray="{dl:.0f}"'
          f' stroke-dashoffset="{dl*(1-pr):.0f}" transform="rotate(-90 {kx:.0f} {ky:.0f})"/>')
    g += '</g>'
    ang = -90 + 360 * pr
    bx = 760 + (kx - 760) + 76 * math.cos(math.radians(ang))
    by = 128 + (ky - 128) + 76 * math.sin(math.radians(ang))
    kist = (f'<g transform="translate({bx:.0f},{by:.0f}) rotate(28)">'
            f'<path d="M0,0 q-11,-26 -4,-54 q4,-10 8,0 q7,28 -4,54 z" fill="#1c1410"/>'
            f'<rect x="-9" y="-72" width="18" height="24" rx="5" fill="url(#med)" {o(3)}/>'
            f'<rect x="-8" y="-230" width="16" height="160" rx="7" fill="url(#solom)" {o(4)}/>'
            f'<rect x="-9" y="-248" width="18" height="22" rx="6" fill="{ob.ALYJ}" {o(3)}/></g>')
    s += SL(Z_SRED, g)
    tu = (ten(1460, 924, 172, 32, .5)
          + f'<ellipse cx="1460" cy="864" rx="182" ry="100" fill="url(#kamen)" {o(8)}/>'
          + f'<ellipse cx="1460" cy="850" rx="140" ry="72" fill="#14100e" {o(5)}/>'
          + f'<ellipse cx="{1430+12*A.w(t,3.2):.0f}" cy="838" rx="52" ry="20" fill="#5a5a66"'
          f' opacity="{.3+.4*abs(A.w(t,2.6)):.2f}"/>'
          + f'<path d="M1300,900 q160,46 320,0" fill="none" stroke="#8c8275" stroke-width="9" opacity=".8"/>')
    s += SL(Z_PERED, tu + kist + baza.begushchiy_blik(t, 11.0, .2, .1, 380))
    s += baza.vinetka(.44)
    return s


def dve_gazetnye_polosy(t):
    """Две газетные полосы на столе, из-за каждой выглядывает хозяйка года.
    Живое: шуршат края, козы выглядывают и подмигивают, шапки подсвечиваются."""
    faza = int(t / 1.2) % 2
    p1 = A.out(A.seg(t, faza * 1.2, .45)) if faza == 0 else 1 - A.ease(A.seg(t, 1.2, .3))
    p1 = 1.0 if faza == 0 else .12
    p2 = .12 if faza == 0 else 1.0
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#241a15"/>'
           + teplo(960, 240, 1000, 700, .5))
    d = baza.doski(-20, 620, W + 40, 520, 128, False, "pol")
    d += f'<rect y="620" width="{W}" height="22" fill="{POL2}" {o(4)}/>'
    d += baza.lampa(960, 300, t, 1.05, True)
    s += SL(Z_DAL, d)
    g = ""
    vyh1 = A.over(A.seg(t, .35, .9))
    vyh2 = A.over(A.seg(t, .75, .9))
    # 13.11: козы сидели так высоко, что верхний край кадра резал рожки, а
    # из-за газеты торчала только макушка — фигуры опущены и уменьшены,
    # газеты сдвинуты ниже, чтобы голова читалась целиком
    g += ob.koza(430, 560 + 54 * (1 - vyh1), t, .52, 0.0, True, .0)
    g += _gazeta(140, 330, 700, 700, t, .0, p1, -1.4)
    g += ob.koza(1350, 560 + 54 * (1 - vyh2), t, .52, 0.0, True, .55)
    g += _gazeta(1080, 330, 700, 700, t, .4, p2, 1.6)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, baza.ramka_pp("oba", "#120d0a", .7)
            + baza.begushchiy_blik(t, 10.0, .35, .09, 420))
    s += baza.vinetka(.46)
    return s


def lenta_goda_s_dvumya_flazhkami(t):
    """Красная лента-дорожка через кадр, флажок в начале и в конце,
    хозяйка года идёт по ленте. Живое: ход козы, трепет флажков, волна ленты."""
    def ly(x):
        return 806 + 26 * math.sin(x / 330.0 + t * .55)
    s = SL(Z_NEBO, baza.nebo("sumer", t) + baza.oblaka(t, 210, 4, 9, .34, "#c8d4e8", 5.0))
    d = ""
    for i in range(16):
        ex = -30 + i * 132 + 26 * math.sin(i * 2.3)
        eh = 120 + 54 * math.sin(i * 1.3)
        d += (f'<path d="M{ex:.0f},700 l{-eh*.32:.0f},0 l{eh*.32:.0f},{-eh:.0f}'
              f' l{eh*.32:.0f},{eh:.0f} z" fill="#27324c" opacity=".9"/>')
    d += baza.sneg_lezhit(716, 24)
    s += SL(Z_DAL, d)
    pts_v, pts_n = [], []
    for k in range(25):
        x = -40 + k * 82
        pts_v.append(f'{x:.0f},{ly(x):.0f}')
        pts_n.append(f'{x:.0f},{ly(x)+104:.0f}')
    lenta = (f'<polygon points="{" ".join(pts_v)} {" ".join(reversed(pts_n))}"'
             f' fill="{ob.ALYJ}" {o(7)}/>')
    lenta += (f'<polyline points="{" ".join(pts_v)}" fill="none" stroke="#f0796c"'
              f' stroke-width="9" opacity=".6"/>')
    lenta += (f'<polyline points="{" ".join(pts_n)}" fill="none" stroke="{ob.ALYJ2}"'
              f' stroke-width="11" opacity=".75"/>')
    for k in range(13):
        x = 20 + k * 155
        lenta += (f'<path d="M{x:.0f},{ly(x)+12:.0f} q24,40 0,80" fill="none"'
                  f' stroke="{ob.ZOLOTO}" stroke-width="5" opacity=".45"/>')
    g = lenta
    g += _flazhok(220, ly(220) + 36, 420, t, .0, ob.ALYJ, 1)
    g += _flazhok(1706, ly(1706) + 36, 420, t, .45, ob.ZOLOTO, -1)
    hod = A.ease(A.seg(t, .45, 6.2))
    kx = 330 + 1200 * hod
    g += ob.koza(kx, ly(kx) + 72, t, .88, .45, False, .25)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, f'<path d="M-40,1080 q420,-80 860,-24 q440,56 1140,-22 L1960,1080 z"'
            f' fill="url(#sneg)" {o(6)}/>')
    s += SL(Z_LETIT, baza.sneg_letit(t, 52, 6, .72, .9))
    s += baza.vinetka(.4)
    return s


def ulica_s_krasnymi_fonaryami(t):
    """Восточная улица ночью: пятнадцать рядов фонарей зажигаются ряд за рядом.
    Живое: ряды загораются, кисти качаются, огоньки дрожат в окнах."""
    s = SL(Z_NEBO, baza.nebo("noch", t)
           + f'<ellipse cx="430" cy="640" rx="760" ry="420" fill="url(#teplo)" opacity=".22"/>')
    VX, VY = 420, 470
    # фасады и мостовая сходятся в одну точку схода: без неё пятнадцать рядов
    # фонарей читаются люстрой, а не улицей
    d = f'<rect x="-20" y="{VY-30}" width="1960" height="{H-VY+50}" fill="#161d2e"/>'
    d += (f'<path d="M-260,1100 L{VX-56},{VY+4} L{VX+56},{VY+4} L1160,1100 z"'
          f' fill="#283350"/>')
    for k in range(9):
        u = (k + 1) / 10.0
        yy = VY + (1100 - VY) * u * u
        ww = 60 + 1180 * u * u
        d += (f'<rect x="{VX+40-ww*.5:.0f}" y="{yy:.0f}" width="{ww:.0f}"'
              f' height="{7+26*u:.0f}" rx="6" fill="#3b476a" opacity=".4"/>')
    r = random.Random(3)
    for storona in (-1, 1):
        for i in range(7):
            u0, u1 = i / 7.0, (i + 1) / 7.0
            x0_ = VX + storona * (66 + 1460 * u0 * u0)
            x1_ = VX + storona * (66 + 1460 * u1 * u1)
            yt0 = VY - 46 - 640 * u0 * u0
            yt1 = VY - 46 - 640 * u1 * u1
            d += (f'<path d="M{x0_:.0f},{yt0:.0f} L{x1_:.0f},{yt1:.0f}'
                  f' L{x1_:.0f},{VY+24:.0f} L{x0_:.0f},{VY+24:.0f} z"'
                  f' fill="{"#121a2b" if i % 2 == 0 else "#0d1524"}" {o(4)}/>')
            d += (f'<path d="M{x0_:.0f},{yt0:.0f} q{(x1_-x0_)*.5:.0f},{-70-70*u0:.0f}'
                  f' {x1_-x0_:.0f},{yt1-yt0:.0f}" fill="none" stroke="{UGOL}"'
                  f' stroke-width="{4+9*u0:.0f}" opacity=".6"/>')
            nn = 2 if i > 2 else 1
            for k in range(nn):
                ww = abs(x1_ - x0_) * .3
                ox = x0_ + (x1_ - x0_) * (k + .5) / nn
                oy = yt0 + (VY - yt0) * .4
                on = r.random() < .72
                op = (.4 + .5 * abs(A.w(t, 2.4 + r.uniform(0, 2), i * .2 + k * .3))) if on else .16
                d += (f'<rect x="{ox-ww*.5:.0f}" y="{oy:.0f}" width="{max(8,ww):.0f}"'
                      f' height="{max(10,ww*1.25):.0f}" rx="6"'
                      f' fill="{"#ff8a5c" if on else "#2b3450"}" opacity="{op:.2f}"'
                      f' stroke="{K}" stroke-width="4"/>')
                if on:
                    d += (f'<circle cx="{ox:.0f}" cy="{oy+ww*.62:.0f}" r="{max(4,ww*.22):.0f}"'
                          f' fill="{KRAS}" opacity="{op*.9:.2f}"/>')
    s += SL(Z_DAL, d)
    g = ""
    for i in range(14, -1, -1):
        u = i / 14.0
        yy = 150 + 292 * u
        sc = 1.12 - .95 * u
        gor = A.ease(A.seg(t, .1 + (14 - i) * .13, .55))
        g += (f'<path d="M{-60+500*u:.0f},{yy-70*sc:.0f} Q420,{yy-112*sc:.0f}'
              f' {920-500*u:.0f},{yy-70*sc:.0f}" fill="none" stroke="#2f2620"'
              f' stroke-width="{6*sc+1:.1f}"/>')
        for k in range(-2, 3):
            fx = 412 + k * 178 * sc
            if gor > .05:
                g += ten(fx, VY + 30 + 520 * (1 - u) ** 2, 86 * sc, 24 * sc, .5 * gor)
                g += teplo(fx, VY + 26 + 520 * (1 - u) ** 2, 150 * sc, 46 * sc, .3 * gor)
            g += _fonar(fx, yy, .64 * sc, t, gor, i * .17 + k * .11)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, baza.ramka_pp("levo", "#090d16", .9)
            + _fonar(118, 236, 1.08, t, A.ease(A.seg(t, 1.9, .5)), .6))
    s += baza.vinetka(.48)
    return s


def gostyu_vstrechayut_v_prihozhey(t):
    """Прихожая: дверь распахнута, на пороге хозяйка года, навстречу плывёт
    полотенце. Живое: снег осыпается с копытец, разворот полотенца, бубенчик."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1b1410"/>'
           + teplo(620, 420, 820, 760, .55))
    d = baza.brevna(-20, -20, W + 40, 1020, 96)
    d += baza.polovicy(880)
    d += baza.polka(120, 300, 420)
    for k, c in enumerate((ob.ALYJ2, "#3c4b66", "#5b4a2e")):
        hx = 190 + k * 136
        d += f'<circle cx="{hx}" cy="300" r="12" fill="url(#zhel)" {o(4)}/>'
        d += (f'<path d="M{hx-56},318 q56,-24 112,0 l-18,280 q-38,20 -76,0 z"'
              f' fill="{c}" {o(6)} opacity=".95"/>')
    d += baza.mebel_hlam(96, 880, 420, t, 21)
    s += SL(Z_DAL, d)
    g = ""
    dx0, dy0, dw, dh = 960, 182, 520, 700
    g += f'<rect x="{dx0-34}" y="{dy0-34}" width="{dw+68}" height="{dh+34}" rx="10" fill="url(#dosk)" {o(8)}/>'
    g += f'<rect x="{dx0}" y="{dy0}" width="{dw}" height="{dh}" fill="#101a2e"/>'
    g += f'<g clip-path="url(#prh)"><clipPath id="prh"><rect x="{dx0}" y="{dy0}" width="{dw}" height="{dh}"/></clipPath>'
    g += f'<rect x="{dx0}" y="{dy0}" width="{dw}" height="{dh}" fill="url(#nnoch)"/>'
    r = random.Random(8)
    for i in range(30):
        px = dx0 + r.uniform(0, dw)
        pp = (r.random() + t * .3) % 1.0
        g += (f'<circle cx="{px+22*A.w(t,4.0,i*.1):.0f}" cy="{dy0+pp*dh:.0f}"'
              f' r="{r.uniform(2.4,5):.1f}" fill="#fff" opacity=".7"/>')
    for i in range(4):
        bx = dx0 + 40 + i * 130
        g += (f'<path d="M{bx},{dy0+440} l-34,0 l34,-120 l34,120 z" fill="#1d2742" opacity=".9"/>')
    g += f'<rect x="{dx0}" y="{dy0+500}" width="{dw}" height="{dh-500}" fill="#c9d9ec" opacity=".9"/>'
    g += '</g>'
    g += baza.dver(dx0 + dw - 40, dy0, 420, dh, .62, "url(#derev)", True)
    g += (f'<rect x="{dx0-50}" y="{dy0+dh-16}" width="{dw+100}" height="46" rx="10"'
          f' fill="url(#derev)" {o(7)}/>')
    g += ob.koza(1248, dy0 + dh + 6, t, .82, 0.0, True, .3)
    for i in range(18):
        pp = ((t * .85) + i * .056) % 1.0
        sx = 1130 + (i % 6) * 62 + 16 * A.w(t, 2.2, i * .2)
        g += (f'<circle cx="{sx:.0f}" cy="{dy0+dh-96+pp*120:.0f}"'
              f' r="{(3.6+5.0*(1-pp)):.1f}" fill="#ffffff" opacity="{(1-pp)*.95:.2f}"/>')
    g += ob.figura(462, 992, 580, t, "#2b2130", "#f0c070", True, .1)
    raz = A.out(A.seg(t, .55, 1.7))
    rl = 460 * raz
    if rl > 10:
        y0 = 660
        g += (f'<path d="M548,{y0} q{rl*.5:.0f},{66+10*A.w(t,3.0):.0f} {rl:.0f},{-14:.0f}'
              f' l0,92 q{-rl*.5:.0f},{76+10*A.w(t,3.0):.0f} {-rl:.0f},14 z"'
              f' fill="url(#rush)" {o(6)}/>')
        for k in (.14, .3, .72, .88):
            g += (f'<path d="M{548+rl*k:.0f},{y0+30+56*k*(1-k)*2:.0f} l0,86" fill="none"'
                  f' stroke="{ob.ALYJ}" stroke-width="9" opacity=".8"/>')
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, baza.ramka_pp("levo", "#0d0a08", .82))
    s += baza.vinetka(.46)
    return s


def krug_iz_dvenadcati_znakov(t):
    """Круг из двенадцати знаков на тёмно-синем; огонёк обегает круг и
    замирает на восьмом. Живое: бег огонька, вспышка знака, вращение круга."""
    rot = 4.5 * t
    cx, cy, R = 960, 536, 398
    pr = A.ease(A.seg(t, .3, 2.3)) * 7.0
    sv = A.out(A.seg(t, 2.7, .6))
    s = SL(Z_NEBO, baza.nebo("noch", t, True, 11)
           + f'<ellipse cx="{cx}" cy="{cy}" rx="860" ry="620" fill="url(#holod)" opacity=".5"/>')
    d = ""
    for k in range(36):
        a = math.radians(k * 10 + rot * .4)
        d += (f'<line x1="{cx+R*1.16*math.cos(a):.0f}" y1="{cy+R*1.16*math.sin(a):.0f}"'
              f' x2="{cx+R*1.3*math.cos(a):.0f}" y2="{cy+R*1.3*math.sin(a):.0f}"'
              f' stroke="{ob.ZOLOTO2}" stroke-width="5" opacity=".5"/>')
    d += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="url(#zol)" stroke-width="16" opacity=".85"/>'
    d += f'<circle cx="{cx}" cy="{cy}" r="{R*.72:.0f}" fill="none" stroke="{ob.ZOLOTO2}" stroke-width="6" opacity=".45"/>'
    d += f'<circle cx="{cx}" cy="{cy}" r="{R*.3:.0f}" fill="#16213a" {o(6)}/>'
    d += teplo(cx, cy, 240, 240, .3 + .18 * abs(A.w(t, 3.2)))
    s += SL(Z_DAL, d)
    g = ""
    for i in range(12):
        a = math.radians(-90 + i * 30 + rot)
        mx, my = cx + R * math.cos(a), cy + R * math.sin(a)
        if i == 7:
            vn = ob.koza_malaya(mx - 24, my + 40, t, .27, .2)
            g += _medal(mx, my, 92, vn, "#241026", sv)
        else:
            g += _medal(mx, my, 80, _zver(mx, my, .84, i, t), "#1b2740", 0.0)
    ao = math.radians(-90 + pr * 30 + rot)
    ox, oy = cx + R * math.cos(ao), cy + R * math.sin(ao)
    g += teplo(ox, oy, 150, 150, .7)
    g += baza.ogon(ox, oy + 30, t, .58, .2, 6)
    s += SL(Z_SRED, g)
    p = baza.iskra_let(t, ox, oy, 12, 4, 260, .7)
    if sv > .05:
        mx8 = cx + R * math.cos(math.radians(-90 + 7 * 30 + rot))
        my8 = cy + R * math.sin(math.radians(-90 + 7 * 30 + rot))
        p += baza.blik(mx8, my8, t, .42, "#ffd0b0", SVET, .32 * sv)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.5)
    return s


def dva_kalendarya_na_stene(t):
    """Два настенных календаря: слева рогатая хозяйка, справа кудрявая овечка.
    Живое: качание на гвоздиках, кивок хозяйки, моргание овечки."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#6b5f52"/>'
           + baza.doski(-20, -20, W + 40, H + 40, 128, True, "krem")
           + f'<rect width="{W}" height="{H}" fill="#3a2e24" opacity=".3"/>'
           + teplo(1180, 220, 960, 820, .45))
    d = ""
    for k in range(13):
        d += (f'<path d="M{70+k*150},120 q18,56 0,112 q-18,56 0,112" fill="none"'
              f' stroke="#8b7a63" stroke-width="7" opacity=".35"/>')
    d += f'<rect y="930" width="{W}" height="26" fill="#4a3a2c" {o(4)}/>'
    d += f'<rect y="956" width="{W}" height="124" fill="#2f241c"/>'
    d += baza.mebel_hlam(1180, 930, 700, t, 17)
    d += baza.lavka(140, 946, 420)
    s += SL(Z_DAL, d)
    g = ""
    for idx, (kx, ky, ph) in enumerate(((510, 196, .0), (1404, 196, .45))):
        kw, kh = 470, 620
        kach = 1.8 * A.w(t, 4.2, ph)
        g += f'<circle cx="{kx}" cy="{ky-28}" r="11" fill="url(#zhel)" {o(4)}/>'
        g += f'<g transform="rotate({kach:.2f} {kx} {ky-28})">'
        g += f'<path d="M{kx},{ky-26} l0,32" fill="none" stroke="#5d6168" stroke-width="5"/>'
        g += ten(kx + 18, ky + kh + 16, kw * .48, 20, .45)
        g += (f'<rect x="{kx-kw/2:.0f}" y="{ky}" width="{kw}" height="{kh}" rx="10"'
              f' fill="url(#krem)" {o(7)}/>')
        g += (f'<rect x="{kx-kw/2+22:.0f}" y="{ky+26}" width="{kw-44}" height="{kh*.56:.0f}"'
              f' rx="8" fill="#2b3a52" {o(5)}/>')
        if idx == 0:
            nod = 4.2 * A.w(t, 1.6, .1)
            g += (f'<g transform="rotate({nod:.2f} {kx+58:.0f} {ky+250:.0f})">'
                  + ob.koza_malaya(kx - 46, ky + 258, t, .34, .15) + '</g>')
            g += teplo(kx, ky + 180, 190, 150, .3)
        else:
            g += _ovca(kx + 72, ky + 262, t, .50, .3, True)
        g += (f'<rect x="{kx-kw/2+22:.0f}" y="{ky+kh*.6:.0f}" width="{kw-44}"'
              f' height="{kh*.34:.0f}" rx="8" fill="#f6eedb" {o(5)}/>')
        for k in range(5):
            g += (f'<rect x="{kx-kw/2+56:.0f}" y="{ky+kh*.66+k*kh*.052:.0f}"'
                  f' width="{kw-112}" height="9" rx="4" fill="#b9a988" opacity=".6"/>')
        g += (f'<rect x="{kx-kw/2+22:.0f}" y="{ky+kh*.6:.0f}" width="{kw-44}" height="14"'
              f' fill="{ob.ALYJ}" opacity=".85"/>')
        g += '</g>'
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, f'<rect y="1012" width="{W}" height="68" fill="#171009" opacity=".92"/>'
            + baza.ramka_pp("oba", "#140e09", .55))
    s += baza.vinetka(.44)
    return s


def ieroglif_i_tri_silueta(t):
    """Кисть пишет иероглиф, от него расходятся три силуэта: коза, овца, баран.
    Живое: письмо кистью, подсыхающий блеск туши, проступающие силуэты."""
    S = [((880, 186), (832, 278)), ((1040, 186), (1088, 278)),
         ((836, 320), (1084, 320)), ((804, 432), (1116, 432)),
         ((750, 548), (1170, 548)), ((960, 180), (960, 692))]
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#2b2017"/>'
           + teplo(960, 380, 980, 760, .5))
    d = baza.polovicy(886)
    d += ten(960, 798, 640, 34, .5)
    d += f'<rect x="318" y="76" width="1284" height="700" rx="14" fill="url(#list)" {o(7)}/>'
    r = random.Random(13)
    for i in range(70):
        d += (f'<circle cx="{r.uniform(330,1590):.0f}" cy="{r.uniform(88,764):.0f}"'
              f' r="{r.uniform(1.6,4.2):.1f}" fill="#cbbb96" opacity=".4"/>')
    d += (f'<rect x="352" y="108" width="1216" height="636" rx="8" fill="none"'
          f' stroke="#c2ab84" stroke-width="5" opacity=".7"/>')
    s += SL(Z_DAL, d)
    g = ""
    T0, DD = .10, .20
    cur = None
    for i, ((ax, ay), (bx, by)) in enumerate(S):
        p = A.out(A.seg(t, T0 + i * DD, DD))
        if p <= 0.001:
            continue
        ln = math.hypot(bx - ax, by - ay)
        wdt = 34 if i < 2 else (40 if i == 5 else 36)
        g += (f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="#15110e"'
              f' stroke-width="{wdt}" stroke-linecap="round" stroke-dasharray="{ln:.0f}"'
              f' stroke-dashoffset="{ln*(1-p):.0f}"/>')
        suh = 1 - A.ease(A.seg(t, T0 + i * DD + DD, 1.5))
        if suh > .02:
            g += (f'<line x1="{ax}" y1="{ay-6}" x2="{bx}" y2="{by-6}" stroke="#6a7a90"'
                  f' stroke-width="11" stroke-linecap="round" stroke-dasharray="{ln:.0f}"'
                  f' stroke-dashoffset="{ln*(1-p):.0f}" opacity="{.5*suh:.2f}"/>')
        if 0.001 < p < .999:
            cur = (ax + (bx - ax) * p, ay + (by - ay) * p)
    if cur:
        g += (f'<g transform="translate({cur[0]:.0f},{cur[1]:.0f}) rotate(24)">'
              f'<path d="M0,6 q-13,-30 -5,-62 q5,-12 10,0 q8,32 -5,62 z" fill="#15110e"/>'
              f'<rect x="-11" y="-86" width="22" height="28" rx="6" fill="url(#med)" {o(3)}/>'
              f'<rect x="-10" y="-268" width="20" height="186" rx="8" fill="url(#solom)" {o(4)}/>'
              f'<rect x="-11" y="-288" width="22" height="24" rx="6" fill="{ob.ALYJ}" {o(3)}/></g>')
        g += teplo(cur[0], cur[1], 180, 160, .35)
    s += SL(Z_SRED, g)
    p3 = ""
    for k, xx in enumerate((372, 958, 1546)):
        pv = A.out(A.seg(t, 1.35 + k * .35, .55))
        if pv < .01:
            continue
        dx = (xx - 960) * (1 - pv)
        if k == 0:
            p3 += (f'<g transform="translate({dx:.0f},0)" opacity="{pv:.2f}">'
                   + ob.koza(xx - 66, 1022, t, .62, 0.0, True, .1) + '</g>')
        elif k == 1:
            p3 += (f'<g transform="translate({dx:.0f},0)" opacity="{pv:.2f}">'
                   + _ovca(xx + 44, 1022, t, .56, .3, True) + '</g>')
        else:
            p3 += (f'<g transform="translate({dx:.0f},0)" opacity="{pv:.2f}">'
                   + _baran(xx + 54, 1022, t, .58, .6, True) + '</g>')
    s += SL(Z_PERED, p3 + baza.begushchiy_blik(t, 12.0, .1, .08, 400))
    s += baza.vinetka(.42)
    return s


def hozyayka_goda_u_ochaga(t):
    """Очаг с ровным огнём, у огня дремлет хозяйка года, над устьем знак пламени.
    Живое: пламя, дыхание боков козы, мерцание углей."""
    dyh = 1.0 + .022 * A.w(t, 2.6)
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1a1512"/>'
           + teplo(620, 700, 900, 700, .55))
    d = baza.kladka(-20, -20, W + 40, 900, 82)
    d += f'<rect width="{W}" height="920" fill="#191310" opacity=".48"/>'
    d += baza.svody(t, "#3d362e", 3)
    d += baza.polovicy(900)
    s += SL(Z_DAL, d)
    g = ""
    ox, oy, ow, oh = 400, 420, 620, 480
    g += ten(ox + ow / 2, oy + oh + 16, ow * .55, 26, .5)
    g += f'<rect x="{ox-40}" y="{oy-60}" width="{ow+80}" height="70" rx="12" fill="url(#kamen)" {o(7)}/>'
    g += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="14" fill="url(#kamen)" {o(8)}/>'
    g += baza.kladka(ox + 10, oy + 10, ow - 20, oh - 20, 72, "url(#kamen)")
    uw, uh = ow * .62, oh * .46
    ux, uy = ox + ow * .19, oy + oh * .5
    g += (f'<path d="M{ux:.0f},{uy+uh:.0f} v{-uh*.5:.0f} q{uw*.5:.0f},{-uh*.86:.0f}'
          f' {uw:.0f},0 v{uh*.5:.0f} z" fill="#110d0b" {o(7)}/>')
    g += baza.ugli(ux + 36, uy + uh - 26, uw - 72, t, 9, 6)
    g += baza.ogon(ux + uw * .5, uy + uh - 18, t, 1.15, .0, 7)
    g += baza.iskra_let(t, ux + uw * .5, uy + uh - 60, 9, 5, 340, .42)
    # значок пламени над устьем
    zy = oy - 110
    g += f'<circle cx="{ox+ow*.5:.0f}" cy="{zy:.0f}" r="64" fill="#2a211a" {o(6)}/>'
    g += f'<circle cx="{ox+ow*.5:.0f}" cy="{zy:.0f}" r="64" fill="none" stroke="url(#zol)" stroke-width="8"/>'
    g += baza.ogon(ox + ow * .5, zy + 36, t, .42, .35, 0)
    g += teplo(ox + ow * .5, zy, 150, 150, .3 + .2 * abs(A.w(t, 2.2)))
    # половик и спящая коза
    g += ten(1352, 1034, 356, 44, .5)
    g += f'<ellipse cx="1352" cy="1008" rx="350" ry="76" fill="url(#tkan)" {o(7)}/>'
    for k in range(2):
        g += (f'<ellipse cx="1352" cy="1008" rx="{300-k*120:.0f}" ry="{64-k*26:.0f}"'
              f' fill="none" stroke="{ob.ZOLOTO if k % 2 == 0 else ob.ALYJ2}"'
              f' stroke-width="7" opacity=".55"/>')
    # 13.11: коза лежала под клипом и читалась как фигура без ног, а тело
    # сливалось с красным половиком — ставим её целиком НА половик
    g += (f'<g transform="translate(1352,996) scale(1,{dyh:.3f}) translate(-1352,-996)">'
          + ob.koza(1352, 996, t, .82, 0.0, True, .4) + '</g>')
    g += teplo(1352, 900, 450, 330, .3)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, baza.ramka_pp("levo", "#0b0806", .85)
            + baza.dym(ox + ow * .5, oy - 170, t, 4, .2, 320, .18, "#c8c0b4", .9))
    s += baza.vinetka(.5)
    return s


def derevyannye_schety(t):
    """Крупные счёты: на верхней спице двенадцать костяшек-знаков, на нижней
    пять цветных костяшек-стихий. Живое: перекат костяшек, блик по раме."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#241a13"/>'
           + teplo(960, 520, 980, 760, .5))
    d = baza.doski(-20, 820, W + 40, 300, 136, False, "pol")
    d += f'<rect y="820" width="{W}" height="20" fill="{POL2}" {o(4)}/>'
    d += baza.mebel_hlam(1300, 828, 560, t, 7)
    d += baza.polka(110, 262, 420)
    d += baza.krynka(190, 256, .8) + baza.krynka(300, 256, .62) + baza.karavay(420, 258, .45, False)
    s += SL(Z_DAL, d)
    x0, x1 = 236, 1690
    yt, yb = 452, 706
    g = ten(960, 884, 700, 36, .5)
    g += f'<rect x="{x0-56}" y="286" width="{x1-x0+112}" height="580" rx="20" fill="url(#derev)" {o(9)}/>'
    g += (f'<rect x="{x0-18}" y="326" width="{x1-x0+36}" height="500" rx="12"'
          f' fill="#2a1d13" opacity=".55" {o(5)}/>')
    for yy in (yt, yb):
        g += (f'<rect x="{x0-20}" y="{yy-7}" width="{x1-x0+40}" height="14" rx="7"'
              f' fill="url(#zhel)" {o(4)}/>')
    for i in range(12):
        t0 = .25 + i * .2
        sh = 78 * A.out(A.seg(t, t0, .36))
        bx = x0 + 44 + i * 112 + sh
        g += ten(bx + 5, yt + 54, 46, 12, .4)
        g += f'<ellipse cx="{bx:.0f}" cy="{yt:.0f}" rx="54" ry="44" fill="url(#med)" {o(6)}/>'
        g += f'<ellipse cx="{bx:.0f}" cy="{yt:.0f}" rx="40" ry="32" fill="#2b2016" opacity=".75"/>'
        g += _zver(bx, yt, .52, i, t, "#edd9a8")
        g += (f'<ellipse cx="{bx-18:.0f}" cy="{yt-20:.0f}" rx="13" ry="8" fill="#ffeab8"'
              f' opacity=".5"/>')
    STIH = (KRAS, "#3f7f96", "#55813f", "#8d949c", "#a9813f")
    for i in range(5):
        t0 = 2.9 + i * .26
        sh = 108 * A.out(A.seg(t, t0, .4))
        bx = x0 + 110 + i * 232 + sh
        g += ten(bx + 5, yb + 60, 56, 14, .4)
        g += f'<ellipse cx="{bx:.0f}" cy="{yb:.0f}" rx="66" ry="52" fill="{STIH[i]}" {o(7)}/>'
        g += f'<ellipse cx="{bx:.0f}" cy="{yb:.0f}" rx="48" ry="36" fill="#120d0a" opacity=".3"/>'
        g += (f'<ellipse cx="{bx-22:.0f}" cy="{yb-24:.0f}" rx="18" ry="11" fill="#fff"'
              f' opacity=".4"/>')
        if i == 0:
            g += baza.ogon(bx, yb + 26, t, .3, .2, 0)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, baza.ramka_pp("oba", "#120c08", .62)
            + baza.begushchiy_blik(t, 7.0, .0, .14, 420))
    s += baza.vinetka(.46)
    return s


def dva_kolesa_s_metkami(t):
    """Большое и малое зубчатые колёса: метка-хозяйка и метка-пламя сходятся,
    в точке встречи вспышка. Живое: вращение, сближение меток, вспышка."""
    p = A.ease(A.seg(t, .25, 2.9))
    fl = A.seg(t, 3.0, .22) * (1 - A.ease(A.seg(t, 3.22, 1.1)))
    bc, sc_ = (660, 572, 322), (1216, 600, 198)
    ab = -76 + 76 * p
    as_ = 184 - 182 * p
    s = SL(Z_NEBO, baza.nebo("noch", t, True, 5)
           + f'<ellipse cx="980" cy="600" rx="900" ry="620" fill="url(#holod)" opacity=".45"/>')
    d = ""
    for k in range(10):
        d += (f'<line x1="{-100+k*230}" y1="1080" x2="{180+k*230}" y2="0"'
              f' stroke="#273551" stroke-width="12" opacity=".35"/>')
    d += teplo(980, 600, 620, 520, .26)
    s += SL(Z_DAL, d)
    g = _koleso(bc[0], bc[1], bc[2], 12, ab, t)
    g += _koleso(sc_[0], sc_[1], sc_[2], 5, as_, t, "url(#dosk)")
    mb = math.radians(ab - 14)
    mx = bc[0] + bc[2] * .72 * math.cos(mb)
    my = bc[1] + bc[2] * .72 * math.sin(mb)
    g += _medal(mx, my, 74, ob.koza_malaya(mx - 20, my + 32, t, .21, .1), "#2a1a14", .25 + .6 * p)
    ms = math.radians(as_ - 16)
    sx = sc_[0] + sc_[2] * .72 * math.cos(ms)
    sy = sc_[1] + sc_[2] * .72 * math.sin(ms)
    g += _medal(sx, sy, 58, baza.ogon(sx, sy + 28, t, .34, .3, 0), "#2a1a14", .25 + .6 * p)
    s += SL(Z_SRED, g)
    vx, vy = (mx + sx) / 2, (my + sy) / 2
    pp = ""
    if fl > .01:
        pp += teplo(vx, vy, 520, 480, .6 * fl)
        pp += baza.blik(vx, vy, t, .9, "#ffd6a8", SVET, .72 * fl)
        pp += baza.iskra_let(t, vx, vy, 16, 7, 420, 1.1)
    pp += baza.iskra_let(t, vx, vy + 40, 8, 3, 220, .5)
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.48)
    return s


def doroga_let_s_tremya_stolbami(t):
    """Снежная дорога вдаль, три верстовых столба с пустыми табличками.
    Живое: таблички вспыхивают по очереди, снег летит, ворона перелетает."""
    faza = (t / 1.15) % 3.0
    sv = [max(0.0, 1 - abs(faza - k) * 1.7) for k in range(3)]
    s = SL(Z_NEBO, baza.nebo("sumer", t)
           + baza.oblaka(t, 200, 5, 3, .34, "#c6d2e6", 4.0)
           + f'<ellipse cx="960" cy="690" rx="820" ry="300" fill="url(#teplo)" opacity=".18"/>')
    d = ""
    for i in range(22):
        ex = -40 + i * 94 + 22 * math.sin(i * 2.7)
        eh = 92 + 50 * math.sin(i * 1.1)
        d += (f'<path d="M{ex:.0f},706 l{-eh*.3:.0f},0 l{eh*.3:.0f},{-eh:.0f}'
              f' l{eh*.3:.0f},{eh:.0f} z" fill="#333f5c" opacity=".9"/>')
    d += baza.sneg_lezhit(716, 20)
    # 13.11: кадр читался почти пустым — на горизонте появилась деревня с
    # тёплыми окнами, она же даёт единственное тёплое пятно
    for hx, hs in ((250, .52), (430, .42), (1560, .48), (1740, .38)):
        d += baza.izba_snaruzhi(hx, 712, int(300 * hs), t, True, True, int(hx) % 7)
    d += baza.tuman(t, 688, .30, "#dbe6f2")
    for bx, bs in ((1468, 1.0), (1700, .74), (1296, .58)):
        for k in range(6):
            a = -2.5 + k * .5
            d += (f'<path d="M{bx:.0f},{800+26*bs:.0f}'
                  f' q{math.cos(a)*50*bs:.0f},{-58*bs:.0f}'
                  f' {math.cos(a)*80*bs+6*A.w(t,5.0,k*.2):.0f},{-128*bs:.0f}" fill="none"'
                  f' stroke="#5b4e3e" stroke-width="{8*bs:.0f}" stroke-linecap="round"/>')
        d += (f'<path d="M{bx-80*bs:.0f},{800+22*bs:.0f} q{80*bs:.0f},{-38*bs:.0f}'
              f' {160*bs:.0f},0 q{-80*bs:.0f},{24*bs:.0f} {-160*bs:.0f},0 z"'
              f' fill="url(#sneg)" {o(4)}/>')
    d += _stolb(1092, 724, 92, t, sv[2], .34)
    s += SL(Z_DAL, d)
    g = (f'<path d="M-120,1080 L810,712 L1046,712 L1980,1080 z" fill="url(#sneg)" {o(6)}/>')
    g += (f'<path d="M-40,1080 L836,718 L900,718 L560,1080 z" fill="#d6e4f4" opacity=".7"/>')
    g += (f'<path d="M1960,1080 L1020,718 L960,718 L1400,1080 z" fill="#d6e4f4" opacity=".7"/>')
    for k in range(7):
        u = k / 6.0
        yy = 724 + u * u * 350
        ww = 20 + u * 150
        g += (f'<rect x="{930-ww/2:.0f}" y="{yy:.0f}" width="{ww:.0f}" height="{8+u*22:.0f}"'
              f' rx="6" fill="#b8ccdf" opacity=".55"/>')
    g += _stolb(700, 842, 212, t, sv[1], .72)
    s += SL(Z_SRED, g)
    pp = _stolb(368, 1046, 420, t, sv[0], 1.32)
    vp = ((t * .36) % 1.0)
    vx = 460 + (1020 - 460) * A.ease(vp)
    vy = 596 - 182 * math.sin(math.pi * vp)
    pp += _vorona(vx, vy, t, 2.3 - .7 * vp, .1)
    s += SL(Z_PERED, pp)
    s += SL(Z_LETIT, baza.sneg_letit(t, 58, 8, .72, 1.0))
    s += baza.vinetka(.42)
    return s


def prababushka_na_staroy_kartochke(t):
    """Карточка цвета сепии в овальной рамке: девушка с косой у плетня.
    Живое: качание косы, колыхание подола, загибающийся уголок карточки."""
    kach = 1.0 * A.w(t, 5.2)
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#241217"/>'
           + teplo(960, 380, 1000, 820, .42))
    d = ""
    for k in range(16):
        d += (f'<path d="M{-60+k*130},0 q40,300 0,560 q-40,300 0,520" fill="none"'
              f' stroke="#3c1d24" stroke-width="40" opacity=".5"/>')
    d += ten(960, 992, 560, 40, .6)
    s += SL(Z_DAL, d)
    g = f'<g transform="rotate({kach:.2f} 960 560)">'
    cx0, cy0, cw, ch = 560, 150, 800, 820
    g += f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="10" fill="#e9d9b6" {o(6)}/>'
    g += (f'<rect x="{cx0+26}" y="{cy0+26}" width="{cw-52}" height="{ch-52}" rx="8"'
          f' fill="none" stroke="#b79a68" stroke-width="5"/>')
    ovx, ovy, orx, ory = 960, 506, 312, 356
    g += f'<clipPath id="ovl"><ellipse cx="{ovx}" cy="{ovy}" rx="{orx}" ry="{ory}"/></clipPath>'
    g += f'<g clip-path="url(#ovl)">'
    g += f'<rect x="{ovx-orx}" y="{ovy-ory}" width="{orx*2}" height="{ory*2}" fill="#d9bd8c"/>'
    g += f'<ellipse cx="{ovx}" cy="{ovy-90}" rx="{orx}" ry="{ory*.74}" fill="#eddcb4"/>'
    g += f'<rect x="{ovx-orx}" y="{ovy+96}" width="{orx*2}" height="{ory}" fill="#ab8e60"/>'
    g += baza.pleten(636, 724, 648, 268, 11)
    g += (f'<path d="M{ovx-orx},720 q{orx*.5:.0f},-26 {orx:.0f},-6 q{orx*.5:.0f},22'
          f' {orx:.0f},2 L{ovx+orx},{ovy+ory} L{ovx-orx},{ovy+ory} z" fill="#9c8054"/>')
    podol = 16 * A.w(t, 3.2, .2)
    g += ob.figura(958, 856, 548, t, "#33230f", "#fff2cf", False, .1)
    # длинная юбка светлее корпуса — иначе фигура читается пятном
    g += (f'<path d="M{884-podol*.4:.0f},648 q{74:.0f},30 {150:.0f},0'
          f' l{30+podol:.0f},208 q{-106:.0f},40 {-212:.0f},0 z" fill="#7d6141" {o(5)}/>')
    for k in range(4):
        g += (f'<path d="M{896+k*2-podol*.3:.0f},{700+k*42:.0f} q{66-k*2:.0f},22'
              f' {132-k*4:.0f},0" fill="none" stroke="#6a5134" stroke-width="5" opacity=".7"/>')
    kos = 18 * A.w(t, 2.4, .35)
    for k in range(6):
        u = k / 5.0
        g += (f'<circle cx="{1004+kos*(.4+u)+u*26:.0f}" cy="{632+u*176:.0f}"'
              f' r="{17-u*4:.0f}" fill="#6b5231" {o(4)}/>')
    g += (f'<path d="M{1030+kos*1.4:.0f},812 l-22,36 l44,0 z" fill="{ob.ALYJ2}" {o(3)}/>')
    g += f'<ellipse cx="{ovx}" cy="{ovy}" rx="{orx}" ry="{ory}" fill="#8a6a42" opacity=".22"/>'
    g += (f'<ellipse cx="{ovx-170}" cy="{ovy-220}" rx="170" ry="130" fill="#fff3d8"'
          f' opacity=".12"/>')
    g += '</g>'
    g += (f'<ellipse cx="{ovx}" cy="{ovy}" rx="{orx}" ry="{ory}" fill="none"'
          f' stroke="#8d7246" stroke-width="12"/>')
    g += (f'<ellipse cx="{ovx}" cy="{ovy}" rx="{orx+16}" ry="{ory+16}" fill="none"'
          f' stroke="#c9b083" stroke-width="5" opacity=".8"/>')
    zag = 46 + 54 * (.5 + .5 * A.w(t, 4.6, .3))
    g += (f'<path d="M{cx0+cw},{cy0+ch} l{-zag:.0f},0 q{zag*.44:.0f},{-zag*.44:.0f}'
          f' {zag:.0f},{-zag:.0f} z" fill="#3a2a1b"/>')
    g += (f'<path d="M{cx0+cw-zag:.0f},{cy0+ch} q{zag*.5:.0f},{-zag*.2:.0f} {zag:.0f},{-zag:.0f}'
          f' q{-zag*.1:.0f},{zag*.7:.0f} {-zag:.0f},{zag:.0f} z" fill="#f3e6c6" {o(4)}/>')
    g += '</g>'
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, baza.ramka_pp("oba", "#180b0e", .62)
            + baza.begushchiy_blik(t, 8.5, .15, .13, 460))
    s += baza.vinetka(.48)
    return s


def chelovek_i_ognennye_vorota(t):
    """Дорога жизни: человек проходит сквозь ближние огненные ворота, вторые
    горят далеко впереди. Живое: шаг, мерцание ворот, ползущая тень."""
    hod = A.ease(A.seg(t, .2, 6.0))
    s = SL(Z_NEBO, baza.nebo("noch", t, True, 7)
           + f'<ellipse cx="1180" cy="700" rx="860" ry="420" fill="url(#teplo)" opacity=".18"/>')
    d = ""
    for i in range(18):
        ex = -40 + i * 116 + 24 * math.sin(i * 2.9)
        eh = 70 + 40 * math.sin(i * 1.5)
        d += (f'<path d="M{ex:.0f},664 l{-eh*.3:.0f},0 l{eh*.3:.0f},{-eh:.0f}'
              f' l{eh*.3:.0f},{eh:.0f} z" fill="#1c2438" opacity=".9"/>')
    d += f'<rect y="660" width="{W}" height="24" fill="#222c42"/>'
    d += _vorota(1256, 676, 112, t, .5, .35, .95)
    s += SL(Z_DAL, d)
    g = (f'<path d="M-160,1080 L1190,672 L1322,672 L2080,1080 z" fill="#3a4258" {o(5)}/>')
    g += (f'<path d="M-40,1080 L1210,676 L1246,676 L540,1080 z" fill="#4a5572" opacity=".6"/>')
    for k in range(9):
        u = k / 8.0
        yy = 690 + u * u * 380
        ww = 16 + u * 170
        g += (f'<rect x="{1248-ww/2-u*120:.0f}" y="{yy:.0f}" width="{ww:.0f}"'
              f' height="{7+u*20:.0f}" rx="6" fill="#59637f" opacity=".5"/>')
    vx, vy, vh = 780, 1010, 558
    # ползущая тень от ворот по дороге
    tl = 260 + 190 * (.5 + .5 * A.w(t, 3.1))
    g += (f'<path d="M{vx-vh*.3:.0f},{vy} l{-tl*.3:.0f},{tl:.0f} l{vh*1.3:.0f},0'
          f' l{-tl*.2:.0f},{-tl:.0f} z" fill="#0a0d16" opacity=".5"/>')
    g += teplo(vx, vy - vh * .5, vh * .9, vh * .8, .45)
    hx = 400 + 580 * hod
    hh = 408 - 150 * hod
    g += ob.figura(hx, vy - 10 + 46 * hod, hh, t, "#1a1620", "#ffb870", False, .0)
    g += _vorota(vx, vy, vh, t, 1.0, .0, 1.0)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, baza.ramka_pp("oba", "#07090f", .85)
            + baza.iskra_let(t, vx, vy - 60, 14, 9, 480, .36))
    s += baza.vinetka(.52)
    return s


def malchik_i_sedoy_chelovek_v_zerkale(t):
    """Зеркало в прихожей: перед ним седой человек, из зеркала — мальчик в
    ушанке с санками. Живое: варежка машет, кант теплеет, дождик качается."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1a151a"/>'
           + teplo(1300, 330, 860, 740, .4))
    d = baza.doski(-20, -20, W + 40, 1000, 142, True, "derev")
    d += f'<rect width="{W}" height="1000" fill="#160f12" opacity=".5"/>'
    d += baza.polovicy(900)
    d += baza.polka(1340, 270, 480)
    for k, c in enumerate(("#3d4c68", ob.ALYJ2)):
        hx = 1430 + k * 230
        d += f'<circle cx="{hx}" cy="270" r="11" fill="url(#zhel)" {o(4)}/>'
        d += (f'<path d="M{hx-52},288 q52,-22 104,0 l-16,250 q-36,18 -72,0 z"'
              f' fill="{c}" {o(6)} opacity=".92"/>')
    s += SL(Z_DAL, d)
    zx, zy, zw, zh = 300, 200, 620, 720
    g = ten(zx + zw / 2 + 16, zy + zh + 26, zw * .5, 24, .5)
    g += f'<rect x="{zx-38}" y="{zy-38}" width="{zw+76}" height="{zh+76}" rx="26" fill="url(#derev)" {o(9)}/>'
    g += (f'<rect x="{zx-16}" y="{zy-16}" width="{zw+32}" height="{zh+32}" rx="18"'
          f' fill="none" stroke="url(#med)" stroke-width="10"/>')
    g += f'<clipPath id="zrk"><rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="10"/></clipPath>'
    g += f'<g clip-path="url(#zrk)">'
    g += f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="#5d7ca6"/>'
    g += f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="url(#holod)" opacity=".55"/>'
    g += baza.doski(zx, zy, zw, zh * .52, 128, True, "dosk")
    g += f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh*.52:.0f}" fill="#8fb0d4" opacity=".45"/>'
    # мальчик в ушанке с санками
    bx, bbase, bh = zx + 316, zy + 668, 430
    # 13.11: мальчик был синим на синем — тело темнее, кант ярче
    g += ob.figura(bx, bbase, bh, t, "#22304a", "#ffe6a8", False, .2)
    sh_ = bh / 300.0
    hy_, hr_ = bbase - 232 * sh_, 42 * sh_
    ush = 8 * A.w(t, 2.0, .2)
    for sg in (-1, 1):
        g += (f'<ellipse cx="{bx+sg*(hr_+2):.0f}" cy="{hy_+16:.0f}" rx="22" ry="42"'
              f' fill="#6b5338" {o(5)}'
              f' transform="rotate({sg*(16+ush):.1f},{bx+sg*(hr_+2):.0f},{hy_+16:.0f})"/>')
    g += (f'<path d="M{bx-hr_-8:.0f},{hy_+2:.0f} a{hr_+8:.0f},{hr_+8:.0f} 0 0 1'
          f' {2*hr_+16:.0f},0 z" fill="#5a4530" {o(6)}/>')
    g += (f'<rect x="{bx-hr_-16:.0f}" y="{hy_-8:.0f}" width="{2*hr_+32:.0f}" height="28"'
          f' rx="13" fill="#8b6c45" {o(5)}/>')
    # варежка на резинке — машет вместо руки
    vm = 34 * A.w(t, .85, .1)
    vy2 = bbase - bh * .52
    g += (f'<path d="M{bx+58},{bbase-bh*.64:.0f} q{30+vm:.0f},{-20:.0f} {44+vm:.0f},{-52:.0f}"'
          f' fill="none" stroke="#c9a05a" stroke-width="6"/>')
    g += (f'<g transform="translate({bx+104+vm:.0f},{vy2-44:.0f}) rotate({vm*.7:.1f})">'
          f'<path d="M-24,0 q0,-40 24,-40 q24,0 24,40 q-6,30 -24,30 q-18,0 -24,-30 z"'
          f' fill="{ob.ALYJ}" {o(6)}/>'
          f'<path d="M20,-14 q22,-6 22,12 q0,14 -18,10 z" fill="{ob.ALYJ2}" {o(5)}/>'
          f'<rect x="-24" y="14" width="48" height="12" rx="6" fill="#f0e4cc" {o(4)}/></g>')
    # санки
    sx0 = bx - 320
    g += ten(sx0 + 118, bbase + 12, 142, 18, .45)
    g += (f'<rect x="{sx0}" y="{bbase-118}" width="236" height="26" rx="10"'
          f' fill="url(#derev)" {o(6)}/>')
    for k in range(4):
        g += (f'<rect x="{sx0+12+k*56}" y="{bbase-112}" width="38" height="14" rx="6"'
              f' fill="url(#dosk)" {o(3)}/>')
    for dxx in (28, 180):
        g += (f'<rect x="{sx0+dxx}" y="{bbase-94}" width="20" height="72" rx="9"'
              f' fill="url(#derev)" {o(5)}/>')
    for dy in (0, 15):
        g += (f'<path d="M{sx0-28},{bbase-24+dy} h246 q36,-6 38,-48" fill="none"'
              f' stroke="url(#zhel)" stroke-width="12" stroke-linecap="round"/>')
    g += (f'<path d="M{sx0+252},{bbase-70} q44,-16 58,-58" fill="none"'
          f' stroke="#c9a05a" stroke-width="7" stroke-linecap="round"/>')
    g += f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="#bcd8ff" opacity=".1"/>'
    g += (f'<path d="M{zx+40},{zy+zh} L{zx+300},{zy} l120,0 L{zx+160},{zy+zh} z"'
          f' fill="#ffffff" opacity=".12"/>')
    g += '</g>'
    # ёлочный дождик на раме
    for k in range(22):
        dxx = zx - 30 + k * (zw + 60) / 21
        kol = 11 * A.w(t, 2.6, k * .14)
        g += (f'<path d="M{dxx:.0f},{zy-44} q{kol:.0f},44 {kol*1.4:.0f},96" fill="none"'
              f' stroke="{(ob.ZOLOTO, "#9fe0ff", ob.ALYJ)[k%3]}" stroke-width="5"'
              f' stroke-linecap="round" opacity=".62"/>')
    s += SL(Z_SRED, g)
    ulyb = .6 + .4 * abs(A.w(t, 2.2, .3))
    p = ob.figura(1270, 1004, 640, t, "#262232", "#f0c070", False, .35)
    hy2, hr2 = 1004 - 640 * .772, 640 * .14
    p += (f'<path d="M{1270-hr2:.0f},{hy2+6:.0f} a{hr2:.0f},{hr2:.0f} 0 0 1 {hr2*2:.0f},0'
          f' q{-hr2*.48:.0f},{hr2*.46:.0f} {-hr2:.0f},{hr2*.4:.0f}'
          f' q{-hr2*.52:.0f},{hr2*.06:.0f} {-hr2:.0f},{-hr2*.46:.0f} z"'
          f' fill="#d7d2c8" opacity="{.8+.16*ulyb:.2f}" {o(4)}/>')
    p += (f'<path d="M{1270+hr2*.42:.0f},{hy2-hr2*.6:.0f} q{hr2*.5:.0f},{hr2*.32:.0f}'
          f' {hr2*.4:.0f},{hr2*.84:.0f}" fill="none" stroke="#f3eee2" stroke-width="7"'
          f' stroke-linecap="round" opacity=".7"/>')
    p += (f'<path d="M1200,{1004-640*.63:.0f} q70,-26 140,0 l-10,120 q-60,22 -120,0 z"'
          f' fill="#4a4a3c" {o(6)}/>')
    for k in range(5):
        p += (f'<path d="M1206,{1004-640*.6+k*34:.0f} q64,20 128,0" fill="none"'
              f' stroke="#5e5e4c" stroke-width="7" opacity=".75"/>')
    sh = 24 * A.w(t, .9, .5)
    p += (f'<path d="M1210,{1004-640*.66:.0f} q-40,90 {-30+sh:.0f},190" fill="none"'
          f' stroke="{ob.ALYJ2}" stroke-width="22" stroke-linecap="round"/>')
    p += teplo(1270, 520, 360, 420, .22 * ulyb)
    s += SL(Z_PERED, p + baza.ramka_pp("pravo", "#0d0a0e", .55))
    s += baza.vinetka(.5)
    return s
