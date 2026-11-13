# -*- coding: utf-8 -*-
"""Декорации планов 57-76 ролика «Как встречать год хозяйки года 2027»."""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob
OKNO = (860, 300, 980, 551)


# ═══════════════════ СВОИ КИРПИЧИКИ БЛОКА ═══════════════════
# Блок «В чём встречать» — это шкафы, ткани, зеркала и рукоделие. Общие для
# семнадцати планов детали собраны здесь, чтобы каждая декорация занималась
# только своим действием.

def _komnata(pol_y=842, stena="#c6b093", t=0.0, polosa=True, tepl=.0):
    """Жилая комната: стена с обойной полосой, плинтус, половицы."""
    s = f'<rect width="{W}" height="{pol_y+6:.0f}" fill="{stena}"/>'
    if polosa:
        for i in range(int(W / 118) + 1):
            s += (f'<rect x="{i*118:.0f}" y="0" width="54" height="{pol_y:.0f}"'
                  f' fill="#ffffff" opacity=".07"/>')
    s += (f'<rect y="{pol_y-300:.0f}" width="{W}" height="300" fill="#2a1d12"'
          f' opacity=".10"/>')
    s += baza.polovicy(pol_y)
    s += (f'<rect y="{pol_y-34:.0f}" width="{W}" height="36" rx="8"'
          f' fill="url(#derev)" {o(5)}/>')
    if tepl:
        s += teplo(W * .28, pol_y - 420, 760, 560, tepl)
    return s


def _plate(x, y, t, col, ph=.0, w_=138, h_=262, kach=1.0, vyshivka=None,
           grad=None):
    """Платье на плечиках: лиф, расклешённый подол, качание от t."""
    a = kach * 2.4 * A.w(t, 3.1 + ph, ph)
    wv = 9 * kach * A.w(t, 2.3, ph + .25)
    fill = f'url(#{grad})' if grad else col
    g = f'<g transform="rotate({a:.2f} {x:.0f} {y-44:.0f})">'
    g += (f'<path d="M{x-6:.0f},{y-42:.0f} q0,-30 14,-30 q16,0 13,22"'
          f' fill="none" stroke="url(#zhel)" stroke-width="7" stroke-linecap="round"/>')
    g += (f'<path d="M{x-w_*.46:.0f},{y+4:.0f} L{x:.0f},{y-34:.0f}'
          f' L{x+w_*.46:.0f},{y+4:.0f}" fill="none" stroke="url(#derev)"'
          f' stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
    g += (f'<path d="M{x-w_*.44:.0f},{y+6:.0f} q{w_*.44:.0f},-20 {w_*.88:.0f},0'
          f' L{x+w_*.30:.0f},{y+h_*.34:.0f} L{x+w_*.64:.0f},{y+h_:.0f}'
          f' q{-w_*.32:.0f},{20+wv:.0f} {-w_*.64:.0f},0'
          f' q{-w_*.32:.0f},{20-wv:.0f} {-w_*.64:.0f},0'
          f' L{x-w_*.30:.0f},{y+h_*.34:.0f} Z" fill="{fill}" {o(6)}/>')
    g += (f'<path d="M{x-w_*.26:.0f},{y+16:.0f} L{x-w_*.22:.0f},{y+h_*.36:.0f}'
          f' L{x-w_*.50:.0f},{y+h_-16:.0f}" fill="none" stroke="#ffffff"'
          f' stroke-width="9" opacity=".20" stroke-linecap="round"/>')
    g += (f'<path d="M{x+w_*.14:.0f},{y+h_*.40:.0f} L{x+w_*.44:.0f},{y+h_-18:.0f}"'
          f' fill="none" stroke="#1a1008" stroke-width="12" opacity=".18"'
          f' stroke-linecap="round"/>')
    if vyshivka:
        for i in range(5):
            g += (f'<circle cx="{x-w_*.20+i*w_*.10:.0f}" cy="{y+40+ (i%2)*16:.0f}"'
                  f' r="6" fill="{vyshivka}" opacity=".9"/>')
    return g + "</g>"


def _plate_lezhit(x, y, t, s_=1.0, grad="tkan", col=None, rukava=True):
    """Платье, разложенное на столе: плечи, рукава, расклешённая юбка.
    Первый заход рисовал «подушку» — форма переделана по контактному листу."""
    f = col or f'url(#{grad})'
    g = ten(x + 14 * s_, y + 250 * s_, 300 * s_, 32 * s_, .42)
    g += f'<g transform="translate({x:.0f},{y:.0f}) scale({s_:.3f})">'
    if rukava:
        for sg in (-1, 1):
            kol = 5 * A.w(t, 3.4, .2 if sg > 0 else .6)
            g += (f'<path d="M{sg*96:.0f},-150 q{sg*150:.0f},{-10+kol:.0f}'
                  f' {sg*248:.0f},{74+kol:.0f} q{sg*16:.0f},40 {-sg*30:.0f},52'
                  f' q{-sg*110:.0f},-54 {-sg*214:.0f},-66 z"'
                  f' fill="{f}" {o(7)}/>')
    g += (f'<path d="M-104,-182 q104,-40 208,0 l18,86 l172,330'
          f' q-298,58 -596,0 l172,-330 z" fill="{f}" {o(8)}/>')
    g += (f'<path d="M-104,-182 q104,38 208,0" fill="none" stroke="#000000"'
          f' stroke-width="11" opacity=".22"/>')
    g += (f'<path d="M-66,-150 L-178,208" fill="none" stroke="#ffffff"'
          f' stroke-width="16" opacity=".20" stroke-linecap="round"/>')
    g += (f'<path d="M60,-140 L172,200" fill="none" stroke="#1a0c0c"'
          f' stroke-width="18" opacity=".20" stroke-linecap="round"/>')
    return g + "</g>"


def _shkaf(x, base, w_, h_, t, raskryt=1.0, nutro="#4a3524"):
    """Корпус двустворчатого шкафа с распахнутыми дверцами (без содержимого)."""
    top = base - h_
    s = ten(x + w_ / 2, base + 14, w_ * .54, 24, .5)
    s += (f'<rect x="{x-20:.0f}" y="{top-26:.0f}" width="{w_+40:.0f}" height="34"'
          f' rx="10" fill="url(#derev)" {o(7)}/>')
    s += (f'<rect x="{x:.0f}" y="{top:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' rx="10" fill="url(#derev)" {o(8)}/>')
    s += (f'<rect x="{x+22:.0f}" y="{top+22:.0f}" width="{w_-44:.0f}"'
          f' height="{h_-44:.0f}" rx="8" fill="{nutro}" {o(6)}/>')
    s += (f'<rect x="{x+22:.0f}" y="{top+22:.0f}" width="{w_-44:.0f}" height="90"'
          f' fill="#000000" opacity=".30"/>')
    dw = w_ * .46 * raskryt
    for sgn, dx0 in ((-1, x + 10), (1, x + w_ - 10)):
        s += (f'<path d="M{dx0:.0f},{top+10:.0f} l{sgn*dw:.0f},{-26*raskryt:.0f}'
              f' l0,{h_-20+52*raskryt:.0f} l{-sgn*dw:.0f},{-26*raskryt:.0f} Z"'
              f' fill="url(#dosk)" {o(7)}/>')
        s += (f'<path d="M{dx0+sgn*dw*.18:.0f},{top+54:.0f}'
              f' l{sgn*dw*.64:.0f},-18 l0,{h_-110:.0f}'
              f' l{-sgn*dw*.64:.0f},18 Z" fill="none" stroke="{DOSKA2}"'
              f' stroke-width="7"/>')
        s += (f'<circle cx="{dx0+sgn*dw*.86:.0f}" cy="{top+h_*.52:.0f}" r="12"'
              f' fill="url(#zol)" {o(4)}/>')
    return s


def _zerkalo(x, y, rx, ry, t, vid="", ramka="url(#zol)", ph=.0):
    """Зеркало в раме: стекло, отражение, бегущий по стеклу блик."""
    s = ten(x + 10, y + ry + 22, rx * .8, 16, .4)
    s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx+22:.0f}" ry="{ry+22:.0f}"'
          f' fill="{ramka}" {o(8)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}"'
          f' fill="url(#stekl)" opacity=".92" {o(5)}/>')
    cid = f"zrk{int(x)}_{int(y)}"
    s = (f'<clipPath id="{cid}"><ellipse cx="{x:.0f}" cy="{y:.0f}"'
         f' rx="{rx:.0f}" ry="{ry:.0f}"/></clipPath>') + s
    if vid:
        s += f'<g clip-path="url(#{cid})" opacity=".72">{vid}</g>'
    u = ((t / 3.4) + ph) % 1.0
    bx = x - rx * 1.3 + u * rx * 2.6
    s += (f'<g clip-path="url(#{cid})"><path d="M{bx:.0f},{y-ry-20:.0f}'
          f' l90,0 l-150,{ry*2+40:.0f} l-90,0 Z" fill="#ffffff" opacity=".30"/></g>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}"'
          f' fill="none" {o(5)}/>')
    return s


def _tkan_volna(y0, h_, t, grad, ph=.0, amp=46, per=3.2, op=1.0, temn=.0):
    """Полоса ткани, идущая волной. Контура нет: обводка превращала полотно
    в стёганое одеяло — поймано на первом контактном листе."""
    d = f'M-60,{y0:.0f}'
    n = 5
    for i in range(n):
        x1 = -60 + (W + 120) * (i + .5) / n
        x2 = -60 + (W + 120) * (i + 1.0) / n
        dy = amp * math.sin(2 * math.pi * (t / per + i * .38 + ph))
        d += f' Q{x1:.0f},{y0+dy:.0f} {x2:.0f},{y0:.0f}'
    d += f' L{W+60},{y0+h_:.0f} L-60,{y0+h_:.0f} Z'
    s = f'<path d="{d}" fill="url(#{grad})" opacity="{op:.2f}"/>'
    s += (f'<path d="{d}" fill="none" stroke="#ff9d86" stroke-width="9"'
          f' opacity="{.30*op:.2f}"/>')
    if temn > .01:
        s += f'<path d="{d}" fill="#3d0c11" opacity="{temn:.2f}"/>'
    return s


def _busina(x, y, r_, col, bl=.8):
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_:.1f}" fill="{col}" {o(3)}/>'
            f'<circle cx="{x-r_*.32:.0f}" cy="{y-r_*.34:.0f}" r="{r_*.30:.1f}"'
            f' fill="#ffffff" opacity="{bl:.2f}"/>')


def _pugovica(x, y, r_, col, t, ph=.0, dyr=4):
    """Пуговица: кружок с дырками и бликом, чуть подрагивает в куче."""
    dx = 3.0 * A.w(t, 1.7, ph)
    dy = 2.2 * A.w(t, 2.1, ph + .3)
    g = (f'<g transform="translate({x+dx:.1f},{y+dy:.1f})">'
         f'<ellipse cx="2" cy="{r_*.5:.0f}" rx="{r_:.0f}" ry="{r_*.42:.0f}"'
         f' fill="#000" opacity=".22"/>'
         f'<circle r="{r_:.1f}" fill="{col}" {o(3)}/>'
         f'<circle r="{r_*.72:.1f}" fill="none" stroke="#000000" stroke-width="2"'
         f' opacity=".25"/>'
         f'<circle cx="{-r_*.34:.1f}" cy="{-r_*.36:.1f}" r="{r_*.26:.1f}"'
         f' fill="#ffffff" opacity=".55"/>')
    for i in range(dyr):
        a = math.pi / 4 + i * 2 * math.pi / dyr
        g += (f'<circle cx="{r_*.30*math.cos(a):.1f}" cy="{r_*.30*math.sin(a):.1f}"'
              f' r="{r_*.13:.1f}" fill="#1a1410" opacity=".8"/>')
    return g + "</g>"


def _katushka(x, y, s_, col, t, ph=.0):
    """Катушка ниток: деревянный торец и намотка."""
    k = 1 + .04 * A.w(t, 2.6, ph)
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({s_*k:.3f})">'
            f'<ellipse cx="3" cy="8" rx="46" ry="20" fill="#000" opacity=".25"/>'
            f'<ellipse rx="46" ry="30" fill="url(#derev)" {o(5)}/>'
            f'<ellipse rx="34" ry="21" fill="{col}" {o(4)}/>'
            f'<ellipse rx="12" ry="8" fill="url(#derev)" {o(3)}/>'
            f'<path d="M34,-4 q26,14 46,2" fill="none" stroke="{col}"'
            f' stroke-width="5" stroke-linecap="round"/></g>')


def _lenta(x, y, w_, t, col, ph=.0, raspr=.0):
    """Моток ленты: чем больше `raspr`, тем прямее она лежит."""
    a = 56 * (1 - raspr) * (1 + .3 * A.w(t, 3.0, ph))
    d = f'M{x:.0f},{y:.0f}'
    for i in range(4):
        x1 = x + w_ * (i + .5) / 4
        x2 = x + w_ * (i + 1.0) / 4
        d += f' Q{x1:.0f},{y + (a if i % 2 == 0 else -a):.0f} {x2:.0f},{y:.0f}'
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="30"'
            f' stroke-linecap="round" opacity=".97"/>'
            f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="7"'
            f' opacity=".28"/>')


def _igla(x, y, a, t, dlina=96):
    """Игла с ниткой: блестящий стержень и тянущийся хвост нити."""
    return (f'<g transform="rotate({a:.1f} {x:.0f} {y:.0f})">'
            f'<path d="M{x:.0f},{y:.0f} l{dlina:.0f},-14" stroke="#e8eef6"'
            f' stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M{x:.0f},{y:.0f} l{dlina*.4:.0f},-6" stroke="#ffffff"'
            f' stroke-width="3" opacity=".8"/>'
            f'<circle cx="{x+dlina:.0f}" cy="{y-14:.0f}" r="7" fill="none"'
            f' stroke="#cfd8e4" stroke-width="4"/>'
            f'<path d="M{x+dlina:.0f},{y-14:.0f} q{40+8*A.w(t,1.4):.0f},-26 86,-8"'
            f' fill="none" stroke="#f3ead6" stroke-width="4"/></g>')


def _nozhnicy(x, y, a, razvod, t, s_=1.0):
    """Ножницы: лезвия сходятся и расходятся, кольца золотые."""
    r_ = 13 + 15 * razvod
    g = f'<g transform="translate({x:.0f},{y:.0f}) rotate({a:.1f}) scale({s_:.2f})">'
    for sgn in (-1, 1):
        g += (f'<path d="M0,0 L150,{sgn*r_:.0f}" stroke="url(#zhel)"'
              f' stroke-width="15" stroke-linecap="round"/>')
        g += (f'<path d="M0,0 L150,{sgn*r_:.0f}" stroke="#ffffff"'
              f' stroke-width="4" opacity=".35"/>')
        g += (f'<path d="M0,0 L-80,{sgn*24:.0f}" stroke="{CHUGUN}"'
              f' stroke-width="13" stroke-linecap="round"/>')
        g += (f'<ellipse cx="-104" cy="{sgn*34:.0f}" rx="26" ry="20"'
              f' fill="none" stroke="url(#zol)" stroke-width="10"/>')
    g += f'<circle r="9" fill="{CHUGUN}" {o(3)}/>'
    return g + "</g>"


def _babochka(x, y, t, s_, ph=.0, col=None):
    """Бабочка: крылья машут, сама плывёт по дуге."""
    c = col or "#f2d16a"
    k = abs(A.w(t, .42, ph))
    dx = 70 * A.w(t, 6.0, ph)
    dy = 26 * A.w(t, 4.1, ph + .2)
    return (f'<g transform="translate({x+dx:.0f},{y+dy:.0f}) scale({s_:.2f})">'
            f'<ellipse cx="{-16-14*k:.0f}" cy="-6" rx="{10+16*k:.0f}" ry="18"'
            f' fill="{c}" {o(3)}/>'
            f'<ellipse cx="{16+14*k:.0f}" cy="-6" rx="{10+16*k:.0f}" ry="18"'
            f' fill="{c}" {o(3)}/>'
            f'<ellipse cx="0" cy="2" rx="5" ry="16" fill="#3a2a18"/></g>')


def _maneken(x, base, h_, t, col, ph=.0):
    """Манекен витрины: безликая форма на стойке, наряд целиком красный."""
    w_ = h_ * .34
    kol = 1.2 * A.w(t, 5.0, ph)
    s = ten(x, base + 10, w_ * .7, 16, .45)
    s += (f'<rect x="{x-8:.0f}" y="{base-h_*.30:.0f}" width="16"'
          f' height="{h_*.30:.0f}" fill="url(#zhel)" {o(4)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{base-4:.0f}" rx="{w_*.46:.0f}"'
          f' ry="{w_*.17:.0f}" fill="url(#zhel)" {o(4)}/>')
    s += f'<g transform="rotate({kol:.2f} {x:.0f} {base-h_*.30:.0f})">'
    s += (f'<path d="M{x-w_*.50:.0f},{base-h_*.84:.0f}'
          f' q{w_*.50:.0f},{-h_*.13:.0f} {w_*1.0:.0f},0'
          f' q{w_*.16:.0f},{h_*.20:.0f} {-w_*.06:.0f},{h_*.30:.0f}'
          f' l{w_*.42:.0f},{h_*.32:.0f}'
          f' q{-w_*.44:.0f},{h_*.06:.0f} {-w_*1.72:.0f},0'
          f' l{w_*.42:.0f},{-h_*.32:.0f}'
          f' q{-w_*.22:.0f},{-h_*.10:.0f} {-w_*.06:.0f},{-h_*.30:.0f} z"'
          f' fill="{col}" {o(7)}/>')
    s += (f'<path d="M{x-w_*.24:.0f},{base-h_*.78:.0f}'
          f' L{x-w_*.46:.0f},{base-h_*.14:.0f}" fill="none" stroke="#ffffff"'
          f' stroke-width="11" opacity=".20" stroke-linecap="round"/>')
    s += (f'<path d="M{x+w_*.20:.0f},{base-h_*.70:.0f}'
          f' L{x+w_*.40:.0f},{base-h_*.16:.0f}" fill="none" stroke="#6b1512"'
          f' stroke-width="13" opacity=".30" stroke-linecap="round"/>')
    s += (f'<rect x="{x-9:.0f}" y="{base-h_*.90:.0f}" width="18"'
          f' height="{h_*.09:.0f}" fill="{col}" {o(4)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{base-h_*.97:.0f}" rx="{w_*.19:.0f}"'
          f' ry="{w_*.24:.0f}" fill="{col}" {o(5)}/>')
    return s + "</g>"


# ═══════════════════ ПЛАН 57 ═══════════════════

def raskrytyy_shkaf_s_naryadami(t):
    """Распахнутый шкаф при дневном свете. Живые: плечики едут по перекладине,
    платья качаются, солнечный зайчик ползёт по дверце."""
    s = SL(Z_NEBO, _komnata(858, "#cdbda0", t, True))
    dal = baza.okno_izby(96, 150, 300, 380, t,
                         vid='<rect x="96" y="150" width="300" height="380" fill="#cfe2f2"/>'
                             '<rect x="96" y="400" width="300" height="130" fill="#e8f1f8"/>',
                         svet=True, moroz=.2)
    dal += baza.luch(300, 190, 230, 700, t, .26)
    dal += teplo(420, 430, 560, 480, .35)
    s += SL(Z_DAL, dal)

    sr = _shkaf(470, 900, 760, 690, t, 1.0)
    hod = (t * 26.0) % 128.0
    for i, (col, gr, hh) in enumerate((
            (TKAN, "tkan", 268), ("#2f5f78", None, 250), (ZOL, "zol", 262),
            ("#6d8a4e", None, 244), ("#b06a9a", None, 256), (KREM, "krem", 266))):
        sr += _plate(548 + i * 122 - hod * .30, 400, t, col, ph=i * .19,
                     w_=132, h_=hh, grad=gr)
    sr += (f'<rect x="505" y="352" width="690" height="17" rx="8"'
           f' fill="url(#zhel)" {o(5)}/>')
    sr += ('<rect x="505" y="352" width="690" height="6" rx="3" fill="#ffffff"'
           ' opacity=".45"/>')
    s += SL(Z_SRED, sr)

    zx = 1300 + 120 * A.w(t, 7.0)
    pp = teplo(zx, 500 + 50 * A.w(t, 5.0, .3), 190, 230, .75)
    pp += (f'<ellipse cx="{zx-16:.0f}" cy="470" rx="56" ry="70"'
           f' fill="#fff6dd" opacity=".30"/>')
    pp += ob.figura(1690, 1020, 720, t, col="#3a2c33", kant="#f3cf92")
    pp += baza.begushchiy_blik(t, 8.0, .1, .10)
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.30)
    return s


# ═══════════════════ ПЛАН 58 ═══════════════════

def krasnaya_tkan_vo_ves_kadr(t):
    """Красная ткань разворачивается во весь кадр. Живые: ткань идёт волной,
    складки расправляются, блики бегут по полотну."""
    skl = 1.0 - A.ease(A.seg(t, .5, 1.6))
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#5c1317"/>'
           + _tkan_volna(-260, 760, t, "tkan", .0, 86, 5.0, .9, .26)
           + teplo(W * .42, H * .40, 1150, 860, .32))
    s += SL(Z_DAL, _tkan_volna(60, 760, t, "tkan", .30, 76, 4.2, 1.0, .14))
    sr = _tkan_volna(420, 760, t, "tkan", .58, 66, 3.4, 1.0, .0)
    for i in range(9):
        fx = -60 + i * 250
        sw = 120 * skl * (1 + .35 * A.w(t, 3.4, i * .15))
        sr += (f'<path d="M{fx:.0f},140 q{sw:.0f},420 {-sw*.5:.0f},900"'
               f' fill="none" stroke="#56121a" stroke-width="{34*skl+6:.0f}"'
               f' opacity="{.40*skl+.06:.2f}" stroke-linecap="round"/>')
        sr += (f'<path d="M{fx+52:.0f},140 q{sw:.0f},420 {-sw*.5:.0f},900"'
               f' fill="none" stroke="#ff9d86" stroke-width="{18*skl+4:.0f}"'
               f' opacity="{.28*skl+.05:.2f}" stroke-linecap="round"/>')
    s += SL(Z_SRED, sr)
    pp = _tkan_volna(800, 620, t, "tkan", .86, 54, 2.8, 1.0, .0)
    for i in range(3):
        u = ((t / 2.6) + i * .34) % 1.0
        bx = -500 + u * (W + 1000)
        pp += (f'<path d="M{bx:.0f},-60 l230,0 l-170,{H+120:.0f} l-230,0 Z"'
               f' fill="#ffc2ad" opacity="{.16*(1-abs(u-.5)*1.3):.2f}"/>')
    pp += baza.begushchiy_blik(t, 4.6, .0, .14, 420)
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.42)
    return s


# ═══════════════════ ПЛАН 59 ═══════════════════

def chetyre_krasnyh_fonarika(t):
    """Четыре красных фонарика на нитке. Живые: загораются по одному,
    кисти качаются, нитка провисает и натягивается."""
    s = SL(Z_NEBO, baza.nebo("noch", t) + teplo(W * .5, 420, 980, 640, .30))
    s += SL(Z_DAL, baza.ulica_dal(-80, 880, 2100, t, True, 9)
            + baza.tuman(t, 806, .12))

    prov = 108 + 40 * A.w(t, 3.6)
    x0, x1, y0 = 150, 1790, 270
    nit = f'M{x0},{y0}'
    for i in range(4):
        u1, u2 = (i + .5) / 4, (i + 1.0) / 4
        nit += (f' Q{x0+(x1-x0)*u1:.0f},{y0+prov*4*u1*(1-u1)*1.35:.0f}'
                f' {x0+(x1-x0)*u2:.0f},{y0+prov*4*u2*(1-u2):.0f}')
    sr = (f'<path d="{nit}" fill="none" stroke="#4b3a2c" stroke-width="7"'
          f' stroke-linecap="round"/>')

    for i in range(4):
        u = (i + .5) / 4
        fx = x0 + (x1 - x0) * u
        fy = y0 + prov * 4 * u * (1 - u)
        gor = A.out(A.seg(t, .5 + i * 1.25, .55))
        kach = 4.2 * A.w(t, 2.7 + i * .3, i * .21)
        sr += f'<g transform="rotate({kach:.2f} {fx:.0f} {fy:.0f})">'
        sr += f'<path d="M{fx:.0f},{fy:.0f} v34" stroke="#4b3a2c" stroke-width="6"/>'
        sr += teplo(fx, fy + 170, 280 * (.5 + gor), 280 * (.5 + gor), .55 * gor)
        sr += (f'<path d="M{fx-112:.0f},{fy+170:.0f} q0,-96 112,-96 q112,0 112,96'
               f' q0,96 -112,96 q-112,0 -112,-96 Z" fill="#8d1b1c" {o(7)}/>')
        sr += (f'<path d="M{fx-112:.0f},{fy+170:.0f} q0,-96 112,-96 q112,0 112,96'
               f' q0,96 -112,96 q-112,0 -112,-96 Z" fill="url(#tkan)"'
               f' opacity="{.42+.58*gor:.2f}"/>')
        for sg in (-1, 1):
            sr += (f'<path d="M{fx+sg*62:.0f},{fy+88:.0f} q{sg*26:.0f},84 0,166"'
                   f' fill="none" stroke="#6d1413" stroke-width="5" opacity=".5"/>')
        for yy in (fy + 80, fy + 250):
            sr += (f'<rect x="{fx-76:.0f}" y="{yy:.0f}" width="152" height="24"'
                   f' rx="9" fill="url(#zol)" {o(5)}/>')
        sr += (f'<ellipse cx="{fx-48:.0f}" cy="{fy+140:.0f}" rx="24" ry="46"'
               f' fill="#ffffff" opacity=".20"/>')
        gx, gy = fx, fy + 176
        if i == 0:
            sr += f'<g opacity="{gor:.2f}">{baza.ogon(gx, gy+48, t, .34, .1, 4)}</g>'
        elif i == 1:
            sr += (f'<g opacity="{gor:.2f}" fill="none" stroke="{SVET}"'
                   f' stroke-width="12" stroke-linecap="round">'
                   f'<path d="M{gx-48:.0f},{gy+6:.0f} q48,60 96,0"/></g>')
            for dx in (-32, 32):
                sr += (f'<circle cx="{gx+dx:.0f}" cy="{gy-40:.0f}" r="9"'
                       f' fill="{SVET}" opacity="{gor:.2f}"/>')
        elif i == 2:
            sr += (f'<path d="M{gx-46:.0f},{gy+48:.0f} a50,56 0 1 1 92,0"'
                   f' fill="none" stroke="url(#zol)" stroke-width="18"'
                   f' stroke-linecap="round" opacity="{gor:.2f}"/>')
            for dx in (-46, 46):
                sr += (f'<circle cx="{gx+dx:.0f}" cy="{gy+48:.0f}" r="8"'
                       f' fill="{SVET}" opacity="{gor:.2f}"/>')
        else:
            sr += (f'<g opacity="{gor:.2f}"><circle cx="{gx:.0f}" cy="{gy:.0f}"'
                   f' r="48" fill="url(#zol)" {o(5)}/>'
                   f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="30" fill="none"'
                   f' stroke="#8a6318" stroke-width="8"/>'
                   f'<circle cx="{gx-16:.0f}" cy="{gy-18:.0f}" r="10" fill="#fff6d2"'
                   f' opacity=".7"/></g>')
        kis = 7 * A.w(t, 2.1, i * .27)
        sr += f'<g transform="rotate({kis:.2f} {fx:.0f} {fy+274:.0f})">'
        sr += (f'<rect x="{fx-22:.0f}" y="{fy+274:.0f}" width="44" height="28"'
               f' rx="9" fill="url(#zol)" {o(4)}/>')
        for kk in range(7):
            sr += (f'<path d="M{fx-20+kk*7:.0f},{fy+302:.0f} q{(kk-3)*3:.0f},44'
                   f' {(kk-3)*5:.0f},84" fill="none" stroke="#c4302a"'
                   f' stroke-width="7" stroke-linecap="round"/>')
        sr += "</g></g>"
    s += SL(Z_SRED, sr)
    s += SL(Z_PERED, baza.ramka_pp("oba", "#0c1020", .55))
    s += SL(Z_LETIT, baza.sneg_letit(t, 34, 6, .5, .7))
    s += baza.vinetka(.40)
    return s


# ═══════════════════ ПЛАН 60 ═══════════════════

def babushka_povyazyvaet_krasnuyu_kosy(t):
    """Бабушка в профиль у зеркальца повязывает красную косынку в горох.
    Живые: концы косынки завязываются, бабушка кивает, зеркало ловит блик."""
    s = SL(Z_NEBO, _komnata(880, "#bfae92", t, True, .0))
    dal = baza.okno_izby(1540, 230, 300, 320, t, svet=True, moroz=.35)
    dal += baza.luch(1560, 270, 190, 640, t, .18)
    dal += baza.polka(130, 430, 330)
    dal += baza.krynka(210, 422, .62)
    dal += baza.krynka(296, 422, .5)
    dal += teplo(700, 470, 640, 540, .34)
    s += SL(Z_DAL, dal)

    otr = ob.figura(1040, 700, 400, t, col="#4a3a3e", kant="#f0c070", profil=True)
    otr += (f'<ellipse cx="1040" cy="{700-232*400/300:.0f}" rx="86" ry="96"'
            f' fill="url(#tkan)" opacity=".9"/>')
    s += SL(Z_SRED, _zerkalo(1040, 400, 130, 170, t, otr, "url(#med)"))

    cx, cbase = 640, 1130
    pp = ob.figura(cx, cbase, 760, t, col="#43343a", kant="#f3cf92", profil=True)
    gy = cbase - 232 * (760 / 300.0)
    kiv = 4.2 * A.w(t, 1.5)
    uzel = A.out(A.seg(t, .35, 1.3))
    pp += f'<g transform="rotate({kiv:.2f} {cx:.0f} {gy+130:.0f})">'
    pp += (f'<circle cx="{cx+36:.0f}" cy="{gy:.0f}" r="106"'
           f' fill="#43343a" stroke="#f3cf92" stroke-width="8" stroke-opacity=".7"/>')
    pp += (f'<path d="M{cx-112:.0f},{gy-22:.0f} q104,-132 196,-16'
           f' q16,128 -96,180 q-114,-50 -100,-164 z" fill="url(#tkan)" {o(8)}/>')
    r = random.Random(4)
    for i in range(11):
        a = r.uniform(0, 2 * math.pi)
        rad = math.sqrt(r.random())
        px = cx - 18 + 74 * rad * math.cos(a)
        py = gy + 2 + 78 * rad * math.sin(a)
        pp += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="#f7efe2" opacity=".93"/>'
    for i, sg in enumerate((1, .45)):
        dl = 40 + 96 * uzel
        kol = 12 * A.w(t, 2.2, i * .4)
        pp += (f'<path d="M{cx-48:.0f},{gy+128:.0f}'
               f' q{-30*sg+kol:.0f},{dl*.6:.0f} {-52*sg+kol:.0f},{dl:.0f}"'
               f' fill="none" stroke="{TKAN}" stroke-width="26"'
               f' stroke-linecap="round"/>')
    pp += (f'<ellipse cx="{cx-44:.0f}" cy="{gy+128:.0f}" rx="{20+22*uzel:.0f}"'
           f' ry="{16+16*uzel:.0f}" fill="{UGOL}" {o(5)}/>')
    pp += "</g>"
    s += SL(Z_PERED, pp + baza.begushchiy_blik(t, 7.5, .2, .09))
    s += baza.vinetka(.34)
    return s


# ═══════════════════ ПЛАНЫ 61-62 ═══════════════════

def krasnaya_devica_na_lugu(t):
    """Летний луг, девушка в красном сарафане с венком. Живые: сарафан
    колышется, красное солнце поднимается, бабочки ходят над травой."""
    sun = 660 - 330 * A.ease(A.seg(t, .0, 4.4))
    s = SL(Z_NEBO, baza.nebo("zakat", t, False)
           + teplo(1430, sun, 820, 640, .55)
           + f'<circle cx="1430" cy="{sun:.0f}" r="248" fill="#e8553a" opacity=".45"/>'
             f'<circle cx="1430" cy="{sun:.0f}" r="178" fill="#f2724a" {o(7)}/>'
             f'<circle cx="1364" cy="{sun-56:.0f}" r="62" fill="#ffd9a6" opacity=".45"/>'
           + baza.oblaka(t, 190, 4, 12, .30, "#f6dcc0", 7.0))
    dal = ""
    for i in range(9):
        tx = 60 + i * 230
        th = 120 + (i % 3) * 56
        dal += (f'<ellipse cx="{tx:.0f}" cy="{742-th*.5:.0f}" rx="{th*.6:.0f}"'
                f' ry="{th*.52:.0f}" fill="#4a6b3d" opacity=".85"/>')
        dal += (f'<rect x="{tx-9:.0f}" y="{742-th*.5:.0f}" width="18"'
                f' height="{th*.5:.0f}" fill="#4b3826" opacity=".8"/>')
    dal += (f'<path d="M-20,740 q480,-34 960,-8 q480,24 980,-16 L{W+20},{H} L-20,{H} Z"'
            f' fill="#6f8c4a"/>')
    dal += (f'<path d="M-20,820 q520,26 1000,-6 q470,-30 960,10 L{W+20},{H} L-20,{H} Z"'
            f' fill="#5d7b3e"/>')
    dal += (f'<path d="M-20,900 q520,30 1000,-4 q470,-26 960,14 L{W+20},{H} L-20,{H} Z"'
            f' fill="url(#solom)" opacity=".22"/>')
    s += SL(Z_DAL, dal)

    sr = ""
    r = random.Random(8)
    for i in range(110):
        gx = r.uniform(-20, W + 20)
        gy = r.uniform(790, 1060)
        gh = r.uniform(50, 130) * (gy - 740) / 320
        sw = 18 * A.w(t, 2.4 + r.uniform(0, 1.6), i * .07)
        sr += (f'<path d="M{gx:.0f},{gy:.0f} q{sw*.4:.0f},{-gh*.5:.0f} {sw:.0f},{-gh:.0f}"'
               f' fill="none" stroke="{["#6f8c4a","#86a257","#55733a"][i%3]}"'
               f' stroke-width="8" stroke-linecap="round"/>')
    s += SL(Z_SRED, sr)

    gx = 540 + 24 * A.w(t, 6.0)
    pp = ob.figura(gx, 1000, 600, t, col="#7a2622", kant="#ffd79a", krasnoe=True)
    gs = 600 / 300.0
    kol = 24 * A.w(t, 2.2)
    pp += (f'<path d="M{gx-74:.0f},{1000-140*gs:.0f} q74,-22 148,0'
           f' L{gx+206+kol*.5:.0f},996'
           f' q{-104-kol*.3:.0f},36 {-412-kol*.2:.0f},0 z"'
           f' fill="{ob.ALYJ}" {o(7)}/>')
    pp += (f'<path d="M{gx-74:.0f},{1000-140*gs:.0f} q74,-22 148,0'
           f' L{gx+206+kol*.5:.0f},996'
           f' q{-104-kol*.3:.0f},36 {-412-kol*.2:.0f},0 z"'
           f' fill="url(#tkan)" opacity=".5"/>')
    pp += (f'<path d="M{gx-40:.0f},{1000-128*gs:.0f} L{gx-150:.0f},988"'
           f' fill="none" stroke="#ffffff" stroke-width="13" opacity=".22"'
           f' stroke-linecap="round"/>')
    pp += (f'<path d="M{gx+44:.0f},{1000-122*gs:.0f} L{gx+150:.0f},986"'
           f' fill="none" stroke="#6b1512" stroke-width="15" opacity=".24"'
           f' stroke-linecap="round"/>')
    vy = 1000 - 232 * gs
    pp += (f'<ellipse cx="{gx:.0f}" cy="{vy-70:.0f}" rx="106" ry="36"'
           f' fill="none" stroke="#6f8c4a" stroke-width="20"/>')
    for i in range(9):
        a = i * 2 * math.pi / 9
        pp += (f'<circle cx="{gx+106*math.cos(a):.0f}"'
               f' cy="{vy-70+36*math.sin(a):.0f}" r="17"'
               f' fill="{["url(#zol)", "#f3f0e6", "url(#tkan)"][i%3]}" {o(4)}/>')
    s += SL(Z_PERED, pp)
    s += SL(Z_LETIT, _babochka(1060, 700, t, 2.1, .0)
            + _babochka(1560, 800, t, 1.7, .4, "#f0f0e2")
            + _babochka(250, 760, t, 1.9, .7, "#e8a85c"))
    s += baza.vinetka(.30)
    return s


# ═══════════════════ ПЛАН 63 ═══════════════════

def chetyre_otreza_tkani(t):
    """Четыре отреза веером на столе. Живые: отрезы приподнимаются по одному,
    сантиметровая лента сползает со стола, свет скользит по тканям."""
    s = SL(Z_NEBO, _komnata(930, "#b9a98f", t, True, .0))
    dal = baza.okno_izby(1440, 150, 360, 320, t, svet=True, moroz=.25)
    dal += baza.luch(1500, 190, 200, 620, t, .20)
    dal += baza.polka(90, 260, 380)
    dal += _katushka(150, 246, .8, TKAN, t, .1)
    dal += _katushka(240, 248, .7, "#3f5c7a", t, .4)
    dal += _katushka(330, 246, .75, ZOL, t, .7)
    dal += teplo(700, 500, 680, 520, .32)
    s += SL(Z_DAL, dal)

    sr = baza.stol(60, 700, 1800, 40, True)
    for i, (col, grad, ugol) in enumerate(((TKAN, "tkan", -21), (ORA, "med", -7),
                                           ("#e8a98c", "glina", 7),
                                           (ZOL, "solom", 21))):
        cx, cy = 440 + i * 345, 666
        pod = (A.out(A.seg(t, .7 + i * 1.5, .7))
               - A.out(A.seg(t, 1.6 + i * 1.5, .7)))
        drozh = 4 * pod * A.w(t, 1.1, i * .3)
        sr += (f'<g transform="rotate({ugol+drozh:.1f} {cx:.0f} {cy:.0f})">'
               f'<g transform="translate(0,{-150*pod:.0f})">')
        sr += ten(cx, cy + 180, 190, 24, .42 * (1 - pod * .6))
        sr += (f'<path d="M{cx-182:.0f},{cy-150:.0f} h364 q16,0 14,20'
               f' l-22,296 q-182,30 -348,0 l-22,-296 q-2,-20 14,-20 z"'
               f' fill="url(#{grad})" {o(7)}/>')
        for kk in range(3):
            sr += (f'<path d="M{cx-120+kk*120:.0f},{cy-134:.0f} q14,150 -6,288"'
                   f' fill="none" stroke="#000000" stroke-width="10" opacity=".13"/>')
        sr += (f'<path d="M{cx-150:.0f},{cy-130:.0f} q12,140 -4,282" fill="none"'
               f' stroke="#ffffff" stroke-width="14" opacity=".22"/>')
        sr += (f'<path d="M{cx-182:.0f},{cy-150:.0f} h364" fill="none"'
               f' stroke="#ffffff" stroke-width="8" opacity=".32"/>')
        sr += "</g></g>"
    s += SL(Z_SRED, sr)

    sp = A.ease(A.seg(t, 1.6, 4.4))
    d = (f'M330,692 q-70,{40+60*sp:.0f} -118,{150+150*sp:.0f}'
         f' q-26,{70+90*sp:.0f} 34,{130+170*sp:.0f}')
    pp = (f'<path d="{d}" fill="none" stroke="url(#solom)" stroke-width="46"'
          f' stroke-linecap="round"/>')
    pp += (f'<path d="{d}" fill="none" stroke="#5d4a1c" stroke-width="46"'
           f' stroke-dasharray="4 34" opacity=".55"/>')
    pp += (f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="10"'
           f' opacity=".25"/>')
    pp += baza.begushchiy_blik(t, 5.2, .0, .14, 380)
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.34)
    return s


# ═══════════════════ ПЛАН 64 ═══════════════════

def blyudce_s_ukrasheniyami(t):
    """Блюдце с серьгами и кольцом у зеркала, рядом пояс с пряжкой.
    Живые: серьги поблёскивают, кольцо катится по блюдцу, пряжка ловит свет.
    Окно вставки справа — всё главное в полосе 0-830."""
    s = SL(Z_NEBO, _komnata(940, "#b6a68d", t, True, .0))
    dal = _zerkalo(290, 290, 208, 254, t, "", "url(#med)")
    dal += baza.polka(620, 240, 210)
    dal += baza.krynka(700, 232, .56)
    dal += teplo(360, 540, 680, 560, .38)
    s += SL(Z_DAL, dal)

    sr = baza.stol(-60, 660, 940, 48, True)
    for kk in range(3):
        sr += (f'<path d="M{830+kk*4:.0f},{612+kk*6:.0f} q-170,{-26+kk*4:.0f}'
               f' -330,{40+kk*3:.0f}" fill="none" stroke="#6b3f26"'
               f' stroke-width="{48-kk*12}" stroke-linecap="round"'
               f' opacity="{.92-kk*.22:.2f}"/>')
    bl = .4 + .6 * abs(A.w(t, 1.9))
    sr += (f'<rect x="596" y="560" width="152" height="124" rx="16"'
           f' fill="url(#zol)" {o(8)}/>')
    sr += ('<rect x="628" y="592" width="86" height="60" rx="10" fill="none"'
           ' stroke="#8a6318" stroke-width="12"/>')
    sr += (f'<path d="M606,570 l128,104" stroke="#ffffff" stroke-width="20"'
           f' opacity="{bl*.6:.2f}"/>')
    sr += teplo(672, 622, 230, 190, .40 * bl)
    s += SL(Z_SRED, sr)

    bx, by = 380, 626
    pp = ten(bx + 10, by + 46, 250, 32, .5)
    pp += (f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="340" ry="126"'
           f' fill="url(#krem)" {o(9)}/>')
    pp += (f'<ellipse cx="{bx:.0f}" cy="{by-18:.0f}" rx="276" ry="100"'
           f' fill="#f8f2e4" {o(6)}/>')
    pp += (f'<ellipse cx="{bx:.0f}" cy="{by-18:.0f}" rx="214" ry="74"'
           f' fill="none" stroke="{TKAN}" stroke-width="7" opacity=".55"/>')
    a = 2 * math.pi * ((t / 2.6) % 1.0)
    kx = bx + 206 * math.cos(a)
    ky = by - 18 + 66 * math.sin(a)
    pp += (f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="48"'
           f' ry="{18+28*abs(math.cos(a)):.0f}" fill="none"'
           f' stroke="url(#zol)" stroke-width="16"/>')
    pp += (f'<circle cx="{kx-12:.0f}" cy="{ky-22:.0f}" r="11" fill="#fff6d2"'
           f' opacity="{.4+.6*abs(A.w(t,1.3)):.2f}"/>')
    pod = A.out(A.seg(t, 1.5, 1.2))
    for i, (sx, ph) in enumerate(((bx - 150, .0), (bx + 140, .5))):
        ly = -240 * pod if i == 1 else 0
        bls = .35 + .65 * abs(A.w(t, 1.6, ph))
        kol = 8 * A.w(t, 2.4, ph) * (1 if i == 1 else .3)
        pp += f'<g transform="translate({sx+kol:.0f},{by-66+ly:.0f})">'
        pp += f'<path d="M0,0 q-36,46 0,82 q36,-36 0,-82" fill="url(#zol)" {o(6)}/>'
        pp += f'<circle cx="0" cy="102" r="36" fill="{TKAN}" {o(6)}/>'
        pp += f'<circle cx="-12" cy="88" r="13" fill="#ffd9c6" opacity="{bls:.2f}"/>'
        pp += teplo(0, 72, 170, 170, .45 * bls)
        pp += "</g>"
    pp += baza.begushchiy_blik(t, 6.4, .3, .10)
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.34)
    return s


# ═══════════════════ ПЛАН 65 ═══════════════════

def babushka_vybiraet_svetloe(t):
    """Бабушка у своего шкафа: чёрное платье уезжает в угол, светлая блузка
    снимается с плечиков, на стене кухни шевелится листок численника."""
    s = SL(Z_NEBO, _komnata(890, "#c3b396", t, True, .0))
    dal = baza.okno_izby(1560, 560, 280, 240, t, svet=True, moroz=.3)
    dal += baza.luch(1580, 590, 180, 400, t, .16)
    dal += teplo(500, 470, 700, 540, .34)
    cx, cy = 1320, 300
    dal += ten(cx + 8, cy + 232, 90, 16, .4)
    dal += (f'<rect x="{cx-96:.0f}" y="{cy-56:.0f}" width="192" height="60" rx="10"'
            f' fill="url(#derev)" {o(6)}/>')
    kol = 3.4 * A.w(t, 2.0)
    dal += (f'<g transform="rotate({kol:.2f} {cx:.0f} {cy-20:.0f})">'
            f'<rect x="{cx-92:.0f}" y="{cy-20:.0f}" width="184" height="214" rx="8"'
            f' fill="url(#list)" {o(6)}/>'
            f'<rect x="{cx-92:.0f}" y="{cy-20:.0f}" width="184" height="36"'
            f' fill="{TKAN}" opacity=".85"/>'
            f'<text x="{cx:.0f}" y="{cy+150:.0f}" text-anchor="middle"'
            f' font-family="DejaVu Serif" font-size="128" font-weight="bold"'
            f' fill="#2a2018">1</text></g>')
    otr = 7 * A.w(t, 1.6, .4)
    dal += (f'<path d="M{cx-88:.0f},{cy+186:.0f} q{44+otr:.0f},28 176,-6'
            f' l0,30 q-88,34 -176,4 z" fill="#efe7d4" {o(5)}/>')
    s += SL(Z_DAL, dal)

    sr = _shkaf(90, 900, 700, 660, t, .9)
    sr += (f'<rect x="128" y="372" width="624" height="16" rx="8"'
           f' fill="url(#zhel)" {o(5)}/>')
    ugol = A.ease(A.seg(t, .6, 2.0))
    sr += _plate(650 + 88 * ugol, 416, t, "#1d1a1c", ph=.1, w_=118, h_=232,
                 kach=.5)
    sr += (f'<rect x="{650+88*ugol-70:.0f}" y="416" width="140" height="250"'
           f' fill="#000000" opacity="{.42*ugol:.2f}"/>')
    for i, col in enumerate(("#6d8a4e", TKAN2, "#9a6f8c")):
        sr += _plate(224 + i * 112, 416, t, col, ph=i * .3, w_=116, h_=226,
                     kach=.6)
    s += SL(Z_SRED, sr)

    sn = A.out(A.seg(t, 2.6, 1.8))
    bx, by = 546 - 34 * sn, 414 + 120 * sn
    pp = f'<g transform="rotate({-8*sn:.1f} {bx:.0f} {by:.0f})">'
    pp += _plate(bx, by, t, KREM, ph=.6, w_=152 + 40 * sn, h_=250, kach=1.4,
                 vyshivka=TKAN, grad="krem")
    pp += "</g>"
    pp += teplo(bx, by + 110, 300, 260, .35 * sn)
    pp += ob.figura(960, 1070, 720, t, col="#3d3036", kant="#f3cf92", platok=True)
    s += SL(Z_PERED, pp + baza.begushchiy_blik(t, 8.5, .5, .08))
    s += baza.vinetka(.32)
    return s


# ═══════════════════ ПЛАН 66 ═══════════════════

def vitrina_s_krasnymi_naryadami(t):
    """Зимняя улица, витрина с тремя красными манекенами. Живые: женщина
    проходит мимо, лампочки витрины мигают, снег падает."""
    s = SL(Z_NEBO, baza.nebo("noch", t) + teplo(900, 540, 900, 620, .22))
    s += SL(Z_DAL, baza.ulica_dal(-120, 820, 2200, t, True, 11)
            + baza.sneg_lezhit(900, 22))

    sr = (f'<rect x="120" y="70" width="1680" height="820" rx="10"'
          f' fill="#3a3326" {o(8)}/>')
    sr += (f'<rect x="120" y="70" width="1680" height="74" rx="8"'
           f' fill="url(#derev)" {o(7)}/>')
    sr += (f'<rect x="186" y="156" width="1548" height="690" rx="6"'
           f' fill="#2b2f3c" {o(6)}/>')
    sr += teplo(960, 540, 980, 520, .55)
    for i, mx in enumerate((520, 960, 1400)):
        sr += _maneken(mx, 840, 600, t, ("#d13a2c", "#b32a26", "#d13a2c")[i], i * .33)
    sr += ('<rect x="186" y="156" width="1548" height="690"'
           ' fill="url(#stekl)" opacity=".14"/>')
    sr += ('<path d="M280,180 l440,620" stroke="#ffffff" stroke-width="44"'
           ' opacity=".09"/>')
    sr += ('<path d="M470,170 l400,580" stroke="#ffffff" stroke-width="20"'
           ' opacity=".09"/>')
    for xx in (186, 1734):
        sr += (f'<rect x="{xx-10:.0f}" y="156" width="20" height="690"'
               f' fill="url(#derev)" {o(5)}/>')
    for i in range(24):
        lx = 150 + (i / 23.0) * 1620
        gor = .3 + .7 * (0.5 + 0.5 * math.sin(2 * math.pi * (t / 1.5 + i * .19)))
        sr += (f'<circle cx="{lx:.0f}" cy="108" r="15"'
               f' fill="{SVET if i%2==0 else ob.ZOLOTO}" opacity="{gor:.2f}"/>')
        sr += (f'<circle cx="{lx:.0f}" cy="108" r="38" fill="{SVET}"'
               f' opacity="{gor*.20:.2f}"/>')
    sr += (f'<rect x="120" y="862" width="1680" height="40" rx="8"'
           f' fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_SRED, sr)

    pp = ob.figura(230 + 168 * t, 1055, 720, t, col="#1b1f2c", kant="#8fc0e8")
    pp += baza.ramka_pp("pravo", "#0b0f1a", .7)
    s += SL(Z_PERED, pp)
    s += SL(Z_LETIT, baza.sneg_letit(t, 70, 3, .88, 1.1))
    s += baza.vinetka(.42)
    return s


# ═══════════════════ ПЛАН 67 ═══════════════════

def odna_krasnaya_vesch_na_svetlom_pla(t):
    """Плечи женщины в светлом платье крупно. Живые: красные вещи сменяют
    друг друга, бусы покачиваются, лента вьётся в волосах."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#4d4255"/>'
           + teplo(900, 460, 1150, 880, .34))
    dal = ob.girlyanda(-40, 150, 1960, 190, t, 14, 120, .1)
    dal += ob.elka(1720, 1070, 540, t, True, False, 6)
    dal += baza.tuman(t, 860, .16, "#cdbcd0")
    s += SL(Z_DAL, dal)

    cx = 880
    dy = 8 * A.w(t, .7)
    sr = f'<g transform="translate(0,{dy:.1f})">'
    sr += ten(cx, 1070, 520, 40, .5)
    sr += (f'<path d="M{cx-560:.0f},1100 q20,-300 170,-392 q130,-80 390,-80'
           f' q260,0 390,80 q150,92 170,392 z" fill="url(#krem)"'
           f' stroke="#c9a46a" stroke-width="8"/>')
    sr += (f'<path d="M{cx-300:.0f},760 q300,-90 600,0" fill="none"'
           f' stroke="#d9c79f" stroke-width="18" opacity=".7"/>')
    sr += (f'<path d="M{cx-420:.0f},960 q60,-180 170,-250" fill="none"'
           f' stroke="#ffffff" stroke-width="30" opacity=".22"/>')
    sr += (f'<path d="M{cx+330:.0f},1000 q-40,-200 -130,-272" fill="none"'
           f' stroke="#a98f63" stroke-width="34" opacity=".28"/>')
    sr += f'<rect x="{cx-82:.0f}" y="560" width="164" height="190" fill="#efe3c8"/>'
    sr += (f'<path d="M{cx-186:.0f},520 q0,-250 186,-250 q186,0 186,250'
           f' q-20,180 -186,196 q-166,-16 -186,-196 z" fill="#4a3426" {o(8)}/>')
    sr += f'<ellipse cx="{cx:.0f}" cy="640" rx="112" ry="78" fill="#3c2a1e" {o(6)}/>'
    sr += (f'<path d="M{cx-120:.0f},360 q120,-70 240,0" fill="none"'
           f' stroke="#6b4d36" stroke-width="22" opacity=".6"/>')
    sr += "</g>"
    s += SL(Z_SRED, sr)

    per = 1.55
    faza = int(t / per) % 4
    k = A.out(A.seg(t - faza * per, .0, .45))
    pp = ""
    if faza == 0:
        pp += (f'<g opacity="{k:.2f}"><path d="M{cx-540:.0f},900'
               f' q230,-190 540,-196 q310,6 540,196'
               f' q-180,40 -300,120 L{cx:.0f},1100'
               f' q-120,-140 -300,-180 z" fill="url(#tkan)" {o(9)}/>')
        pp += (f'<path d="M{cx-540:.0f},900 q230,-190 540,-196 q310,6 540,196"'
               f' fill="none" stroke="#ff9d86" stroke-width="14" opacity=".35"/>')
        for i, sg in enumerate((-1, 1)):
            pp += (f'<path d="M{cx+sg*390:.0f},{992+10*A.w(t,2.4,i*.3):.0f}'
                   f' l{sg*28:.0f},70" stroke="{UGOL}" stroke-width="13"'
                   f' stroke-linecap="round"/>')
        pp += (f'<path d="M{cx-46:.0f},{1062+14*A.w(t,2.4,.4):.0f} v48"'
               f' stroke="{UGOL}" stroke-width="13" stroke-linecap="round"/>')
        pp += "</g>"
    elif faza == 1:
        kach = 26 * A.w(t, 1.8)
        pp += f'<g opacity="{k:.2f}">'
        for i in range(19):
            u = (i + .5) / 19
            bx = cx - 300 + u * 600
            by = 790 + (250 + kach) * math.sin(math.pi * u)
            pp += _busina(bx, by, 30, ob.ALYJ)
        pp += "</g>"
    elif faza == 2:
        pul = .92 + .08 * A.w(t, 1.6)
        pp += (f'<g opacity="{k:.2f}" transform="translate({cx-330:.0f},870)'
               f' scale({pul*1.5:.3f})">')
        for i in range(8):
            a = i * math.pi / 4
            pp += (f'<ellipse cx="{74*math.cos(a):.0f}" cy="{74*math.sin(a):.0f}"'
                   f' rx="42" ry="25" fill="{ob.ALYJ}" {o(5)}'
                   f' transform="rotate({math.degrees(a):.0f},{74*math.cos(a):.0f},{74*math.sin(a):.0f})"/>')
        pp += f'<circle r="48" fill="url(#zol)" {o(6)}/>'
        pp += '<circle cx="-15" cy="-17" r="16" fill="#fff6d2" opacity=".75"/>'
        pp += teplo(0, 0, 230, 210, .4)
        pp += "</g>"
    else:
        pp += f'<g opacity="{k:.2f}">'
        d = f'M{cx-260:.0f},400'
        for i in range(5):
            u1, u2 = (i + .5) / 5, (i + 1.0) / 5
            wv = 76 * math.sin(2 * math.pi * (t / 2.2 + i * .3))
            d += (f' Q{cx-260+520*u1:.0f},{400+wv:.0f}'
                  f' {cx-260+520*u2:.0f},400')
        pp += (f'<path d="{d}" fill="none" stroke="{ob.ALYJ}" stroke-width="40"'
               f' stroke-linecap="round"/>')
        pp += (f'<path d="{d}" fill="none" stroke="#ff9d86" stroke-width="11"'
               f' opacity=".35"/>')
        for sg in (-1, 1):
            hv = 46 * A.w(t, 1.9, sg * .3)
            pp += (f'<path d="M{cx+sg*250:.0f},420'
                   f' q{sg*70:.0f},{140+hv:.0f} {sg*24:.0f},290"'
                   f' fill="none" stroke="{ob.ALYJ}" stroke-width="32"'
                   f' stroke-linecap="round"/>')
        pp += "</g>"
    s += SL(Z_PERED, pp + baza.begushchiy_blik(t, 6.0, .4, .10))
    s += baza.vinetka(.40)
    return s


# ═══════════════════ ПЛАН 68 ═══════════════════

def ded_i_vnuchka_u_zerkala(t):
    """Дед и внучка у трюмо. Живые: уголок красного платка расправляется в
    кармане, бант завязывается, внучка вертится перед зеркалом."""
    s = SL(Z_NEBO, _komnata(900, "#b8a58d", t, True, .0))
    dal = ob.girlyanda(60, 130, 1860, 150, t, 13, 96, .3)
    dal += baza.polka(1520, 400, 330)
    dal += baza.krynka(1600, 392, .55)
    dal += teplo(900, 500, 820, 560, .34)
    s += SL(Z_DAL, dal)

    otr = ob.figura(880, 740, 470, t, col="#3a3240", kant="#f0c070")
    sr = _zerkalo(880, 420, 300, 330, t, otr, "url(#derev)")
    sr += (f'<rect x="520" y="760" width="720" height="40" rx="10"'
           f' fill="url(#derev)" {o(7)}/>')
    sr += (f'<rect x="560" y="800" width="640" height="120" rx="10"'
           f' fill="url(#dosk)" {o(6)}/>')
    for i in range(3):
        sr += f'<circle cx="{660+i*230:.0f}" cy="860" r="13" fill="url(#zol)" {o(4)}/>'
    s += SL(Z_SRED, sr)

    dx, dbase, dh = 400, 1070, 780
    pp = ob.figura(dx, dbase, dh, t, col="#2b3040", kant="#f0c070")
    ds = dh / 300.0
    for sg in (-1, 1):
        pp += (f'<path d="M{dx+sg*34*ds:.0f},{dbase-198*ds:.0f}'
               f' L{dx+sg*8*ds:.0f},{dbase-112*ds:.0f}'
               f' L{dx+sg*40*ds:.0f},{dbase-96*ds:.0f} Z"'
               f' fill="#1c2130" {o(4)}/>')
    pkx, pky = dx + 42 * ds, dbase - 158 * ds
    pp += (f'<rect x="{pkx-34:.0f}" y="{pky:.0f}" width="68" height="11" rx="5"'
           f' fill="#1c2130" {o(3)}/>')
    rsp = A.out(A.seg(t, .5, 1.6))
    for sg in (-1, 0, 1):
        hh = (20 + 44 * rsp) * (1 - abs(sg) * .3)
        pp += (f'<path d="M{pkx+sg*22:.0f},{pky+2:.0f}'
               f' l{sg*10:.0f},{-hh:.0f} l17,{hh*.7:.0f} z"'
               f' fill="{ob.ALYJ}" {o(3)}/>')
    pp += teplo(pkx, pky, 120 * rsp, 100 * rsp, .40 * rsp)

    vert = 7.0 * A.w(t, 2.4)
    vx, vbase, vh = 1330, 1070, 500
    pp += f'<g transform="rotate({vert:.2f} {vx:.0f} {vbase:.0f})">'
    pp += ob.figura(vx, vbase, vh, t, col="#6b4a64", kant="#ffd79a", ph=.3)
    vs = vh / 300.0
    bgy = vbase - 262 * vs
    ban = A.over(A.seg(t, 1.2, 1.4))
    for sg in (-1, 1):
        pp += (f'<ellipse cx="{vx+sg*54*vs*ban:.0f}" cy="{bgy:.0f}"'
               f' rx="{48*vs*ban:.0f}" ry="{34*vs*ban:.0f}" fill="{ob.ALYJ}" {o(5)}'
               f' transform="rotate({sg*22:.0f},{vx+sg*54*vs*ban:.0f},{bgy:.0f})"/>')
        pp += (f'<path d="M{vx+sg*16*vs:.0f},{bgy+18*vs:.0f}'
               f' q{sg*30*vs:.0f},{54*vs*ban:.0f} {sg*12*vs:.0f},{96*vs*ban:.0f}"'
               f' fill="none" stroke="{ob.ALYJ2}" stroke-width="{13*vs:.0f}"'
               f' stroke-linecap="round"/>')
    pp += (f'<circle cx="{vx:.0f}" cy="{bgy:.0f}" r="{20*vs*ban:.0f}"'
           f' fill="{ob.ALYJ2}" {o(4)}/>')
    pp += "</g>"
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.34)
    return s


# ═══════════════════ ПЛАН 69 ═══════════════════

def krasnaya_salfetka_u_tarelki(t):
    """Крупно белая тарелка на скатерти. Живые: салфетка сама складывается
    веером, вилка ложится рядом, блик скользит по фарфору."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#6a4f3a"/>'
           + teplo(860, 420, 1100, 800, .38))
    dal = (f'<path d="M-20,150 q480,-40 960,-6 q480,34 980,-22 L{W+20},{H} L-20,{H} Z"'
           f' fill="url(#rush)" {o(7)}/>')
    for i in range(9):
        dal += (f'<path d="M{-40+i*240:.0f},170 q30,420 -10,{H+20}" fill="none"'
                f' stroke="{TKAN}" stroke-width="7" opacity=".28"/>')
    for i in range(5):
        dal += (f'<path d="M-20,{300+i*170:.0f} q480,26 960,0 q480,-26 980,14"'
                f' fill="none" stroke="{TKAN}" stroke-width="7" opacity=".22"/>')
    dal += ob.bokal(1700, 420, t, 1.3, .2, .55, True)
    dal += ob.mandarin(130, 940, 1.5, .4, t)
    s += SL(Z_DAL, dal)

    px, py = 760, 650
    sr = (f'<clipPath id="tar"><ellipse cx="{px:.0f}" cy="{py-14:.0f}"'
          f' rx="342" ry="230"/></clipPath>')
    sr += ten(px + 16, py + 130, 340, 46, .55)
    sr += (f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="382" ry="262"'
           f' fill="url(#krem)" {o(9)}/>')
    sr += (f'<ellipse cx="{px:.0f}" cy="{py-14:.0f}" rx="342" ry="230"'
           f' fill="#fbf6ec" {o(5)}/>')
    sr += (f'<ellipse cx="{px:.0f}" cy="{py-14:.0f}" rx="244" ry="158"'
           f' fill="none" stroke="#d8cdb8" stroke-width="7"/>')
    bu = (t / 3.0) % 1.0
    sr += (f'<g clip-path="url(#tar)"><path d="M{px-342+bu*660:.0f},{py-250:.0f}'
           f' l130,0 l-220,490 l-130,0 Z" fill="#ffffff" opacity=".38"/></g>')
    s += SL(Z_SRED, sr)

    vx, vy = 1430, 600
    pp = ten(vx + 10, vy + 236, 160, 24, .45)
    for i in range(7):
        k = A.out(A.seg(t, .35 + i * .22, .5))
        a = -74 + i * 24 * k
        pp += (f'<g transform="rotate({a:.1f} {vx:.0f} {vy+230:.0f})">'
               f'<path d="M{vx-40:.0f},{vy+230:.0f} l40,-300 l40,300 z"'
               f' fill="url(#tkan)" {o(5)}/>'
               f'<path d="M{vx:.0f},{vy-62:.0f} L{vx-24:.0f},{vy+220:.0f}"'
               f' fill="none" stroke="#ffffff" stroke-width="7" opacity=".22"/></g>')
    pp += (f'<ellipse cx="{vx:.0f}" cy="{vy+238:.0f}" rx="80" ry="28"'
           f' fill="{UGOL}" {o(5)}/>')
    vil = A.out(A.seg(t, 1.0, .9))
    fx, fy = 230, 500 - 180 * (1 - vil)
    pp += (f'<g transform="rotate({6-4*vil:.1f} {fx:.0f} {fy:.0f})"'
           f' opacity="{.2+.8*vil:.2f}">')
    pp += (f'<rect x="{fx-16:.0f}" y="{fy:.0f}" width="32" height="290" rx="14"'
           f' fill="url(#zhel)" {o(5)}/>')
    for kk in range(4):
        pp += (f'<rect x="{fx-30+kk*18:.0f}" y="{fy-130:.0f}" width="11"'
               f' height="138" rx="5" fill="url(#zhel)" {o(3)}/>')
    pp += (f'<rect x="{fx-34:.0f}" y="{fy-18:.0f}" width="68" height="30" rx="12"'
           f' fill="url(#zhel)" {o(4)}/>')
    pp += (f'<rect x="{fx-9:.0f}" y="{fy+18:.0f}" width="8" height="250"'
           f' fill="#ffffff" opacity=".3"/>')
    pp += "</g>"
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.40)
    return s


# ═══════════════════ ПЛАН 71 ═══════════════════

def novoe_plate_pered_podrugami(t):
    """Мостик в память: девушка в новом платье кружится перед подругами.
    Живые: юбка кружится, подруги качаются и тянутся к подолу, коса летит."""
    s = SL(Z_NEBO, _komnata(910, "#a89a86", t, True, .0))
    dal = baza.okno_izby(1450, 150, 330, 310, t, svet=True, moroz=.25)
    dal += baza.luch(1500, 190, 190, 640, t, .20)
    dal += baza.polka(120, 300, 320)
    dal += baza.krynka(200, 292, .55)
    dal += baza.hodiki(330, 270, t, .7)
    dal += teplo(860, 480, 760, 560, .34)
    s += SL(Z_DAL, dal)

    sr = (f'<rect x="1160" y="700" width="700" height="34" rx="10"'
          f' fill="url(#derev)" {o(6)}/>')
    sr += (f'<rect x="1190" y="734" width="640" height="176" rx="10"'
           f' fill="url(#tkan)" opacity=".75" {o(5)}/>')
    s += SL(Z_SRED, sr)

    gx, gbase = 620, 1010
    sp = 2 * math.pi * (t / 2.1)
    shir = 1.0 + .30 * math.sin(sp)
    pp = ""
    for i, (px, ph, hh) in enumerate(((1290, .0, 560), (1580, .45, 540))):
        nak = 4.6 * A.w(t, 2.3, ph)
        pp += f'<g transform="rotate({nak:.2f} {px:.0f} 1010)">'
        pp += ob.figura(px, 1010, hh, t, col="#4b3a46", kant="#f0c070",
                        platok=(i == 0), ph=ph)
        pp += "</g>"
    pp += ob.figura(gx, gbase, 640, t, col="#2f5f78", kant="#ffd79a")
    gs = 640 / 300.0
    hem = gbase - 6
    pp += (f'<g transform="translate({gx:.0f},{hem:.0f}) scale({shir:.3f},1)'
           f' translate({-gx:.0f},{-hem:.0f})">')
    d = f'M{gx-62:.0f},{gbase-150*gs:.0f} q62,-16 124,0 L{gx+210:.0f},{hem:.0f}'
    for i in range(4):
        u1, u2 = (i + .5) / 4, (i + 1.0) / 4
        wv = 30 * math.sin(2 * math.pi * (t / 1.05 + i * .3))
        d += (f' Q{gx+210-420*u1:.0f},{hem+26+wv:.0f}'
              f' {gx+210-420*u2:.0f},{hem+10:.0f}')
    d += " Z"
    pp += f'<path d="{d}" fill="#3a7692" {o(7)}/>'
    pp += (f'<path d="M{gx-34:.0f},{gbase-140*gs:.0f} L{gx-150:.0f},{hem:.0f}"'
           f' fill="none" stroke="#ffffff" stroke-width="14" opacity=".22"'
           f' stroke-linecap="round"/>')
    pp += (f'<path d="M{gx+44:.0f},{gbase-124*gs:.0f} L{gx+154:.0f},{hem-8:.0f}"'
           f' fill="none" stroke="#1b3c4c" stroke-width="16" opacity=".25"'
           f' stroke-linecap="round"/>')
    pp += "</g>"
    kosa = 56 * math.sin(sp + .9)
    kx0, ky0 = gx - 54, gbase - 212 * gs
    pp += (f'<path d="M{kx0:.0f},{ky0:.0f}'
           f' q{-60+kosa:.0f},90 {-34+kosa*1.4:.0f},206" fill="none"'
           f' stroke="#5a3c22" stroke-width="32" stroke-linecap="round"/>')
    pp += (f'<circle cx="{kx0-34+kosa*1.4:.0f}" cy="{ky0+212:.0f}" r="21"'
           f' fill="{ob.ALYJ}" {o(4)}/>')
    s += SL(Z_PERED, pp + baza.begushchiy_blik(t, 7.0, .2, .10))
    s += baza.vinetka(.34)
    return s


# ═══════════════════ ПЛАН 72 ═══════════════════

def shite_platya_po_vecheram(t):
    """Мостик в память: вечернее шитьё в три приёма — журнал с выкройкой,
    ручная машинка под лампой, платье на живую нитку. Живые: колесо машинки
    крутится, ткань ползёт под лапкой, булавки поблёскивают.
    Окно вставки справа — работа идёт в полосе 0-830."""
    s = SL(Z_NEBO, _komnata(900, "#8f7f6b", t, True, .0))
    dal = baza.lampa(410, 250, t, 1.45, False)
    dal += teplo(410, 420, 820, 660, .55)
    dal += baza.polka(40, 190, 250)
    dal += _katushka(110, 176, .66, TKAN, t, .2)
    dal += _katushka(190, 178, .6, KREM, t, .6)
    s += SL(Z_DAL, dal)

    s += SL(Z_SRED, baza.stol(-60, 700, 960, 48, True))

    a1 = 1.0 - A.ease(A.seg(t, 2.0, .35))
    a2 = A.ease(A.seg(t, 2.35, .35)) - A.ease(A.seg(t, 5.0, .35))
    a3 = A.ease(A.seg(t, 5.35, .35))
    pp = ""
    if a1 > .01:
        lx, ly = 400, 630
        pp += f'<g opacity="{a1:.2f}">'
        pp += ten(lx + 16, ly + 92, 310, 28, .45)
        pp += (f'<path d="M{lx-330:.0f},{ly+74:.0f} q330,-46 660,0 l0,-36'
               f' q-330,-46 -660,0 z" fill="url(#list)" {o(6)}/>')
        pp += (f'<path d="M{lx-320:.0f},{ly+32:.0f} q320,-46 640,0 l-22,-240'
               f' q-298,-42 -596,0 z" fill="#f4eedd" {o(5)}/>')
        kol = 6 * A.w(t, 2.6)
        pp += (f'<g transform="rotate({kol*.3:.2f} {lx:.0f} {ly:.0f})">'
               f'<path d="M{lx-266:.0f},{ly-10+kol:.0f} q266,-42 532,0'
               f' l-18,-196 q-250,-38 -498,0 z" fill="#eae3cf" {o(4)}/>')
        for ax, ay, bw in ((-160, -78, 120), (10, -96, 130), (172, -70, 100)):
            pp += (f'<path d="M{lx+ax:.0f},{ly+ay+kol:.0f} l{bw*.4:.0f},-86'
                   f' l{bw*.5:.0f},12 l{-bw*.2:.0f},94 z" fill="none"'
                   f' stroke="#9b8a6a" stroke-width="6" stroke-dasharray="15 11"/>')
        pp += "</g></g>"
    if a2 > .01:
        mx, my = 420, 660
        pp += f'<g opacity="{a2:.2f}">'
        pp += ten(mx + 16, my + 50, 330, 34, .5)
        pp += (f'<path d="M{mx-330:.0f},{my+22:.0f} h660 l-28,50 h-604 z"'
               f' fill="url(#derev)" {o(7)}/>')
        pp += (f'<path d="M{mx-280:.0f},{my+22:.0f} l48,-186 q28,-48 94,-48'
               f' h250 q48,0 48,54 v180 z" fill="url(#chug)" {o(8)}/>')
        pp += (f'<path d="M{mx-250:.0f},{my-28:.0f} l40,-150 q22,-38 76,-38'
               f' h200 q32,0 32,40 v148 z" fill="{ZHELEZ}" opacity=".45"/>')
        pp += (f'<path d="M{mx-236:.0f},{my-142:.0f} q106,-40 296,-26"'
               f' fill="none" stroke="url(#zol)" stroke-width="10" opacity=".75"/>')
        pp += (f'<rect x="{mx-200:.0f}" y="{my-128:.0f}" width="150" height="54"'
               f' rx="10" fill="url(#zol)" opacity=".35" {o(4)}/>')
        pp += (f'<path d="M{mx-150:.0f},{my-70:.0f} q90,-20 190,-8" fill="none"'
               f' stroke="url(#zol)" stroke-width="6" opacity=".45"/>')
        kx, ky = mx + 214, my - 120
        ang = (t * 270) % 360
        pp += f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="104" fill="url(#chug)" {o(8)}/>'
        pp += (f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="76" fill="none"'
               f' stroke="{ZHELEZ}" stroke-width="10"/>')
        pp += f'<g transform="rotate({ang:.0f} {kx:.0f} {ky:.0f})">'
        for i in range(6):
            a = i * math.pi / 3
            pp += (f'<line x1="{kx:.0f}" y1="{ky:.0f}"'
                   f' x2="{kx+86*math.cos(a):.0f}" y2="{ky+86*math.sin(a):.0f}"'
                   f' stroke="url(#zhel)" stroke-width="10"/>')
        pp += f'<circle cx="{kx+66:.0f}" cy="{ky:.0f}" r="18" fill="url(#zol)" {o(4)}/>'
        pp += "</g>"
        pp += f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="24" fill="url(#zhel)" {o(4)}/>'
        pp += (f'<rect x="{mx-214:.0f}" y="{my-56:.0f}" width="26" height="58"'
               f' rx="7" fill="url(#zhel)" {o(4)}/>')
        tk = (t * 90) % 64
        pp += (f'<path d="M{mx-350:.0f},{my+2:.0f} h290 l-22,46 h-290 z"'
               f' fill="url(#tkan)" {o(6)}/>')
        for i in range(8):
            pp += (f'<line x1="{mx-340+i*46-tk:.0f}" y1="{my+6:.0f}"'
                   f' x2="{mx-348+i*46-tk:.0f}" y2="{my+46:.0f}"'
                   f' stroke="#ffe7d8" stroke-width="6" opacity=".55"/>')
        pp += "</g>"
    if a3 > .01:
        pp += f'<g opacity="{a3:.2f}">'
        pp += _zerkalo(170, 420, 140, 240, t, "", "url(#derev)")
        pp += _plate(560, 280, t, KREM, ph=.3, w_=280, h_=450, kach=.8,
                     grad="krem")
        for i in range(9):
            sx = 440 + (i % 3) * 120
            sy = 420 + (i // 3) * 130
            pp += (f'<path d="M{sx:.0f},{sy:.0f} l44,20" stroke="#c7b48a"'
                   f' stroke-width="6" stroke-dasharray="13 10"/>')
        pp += "</g>"
    r = random.Random(12)
    for i in range(11):
        bx = 70 + r.uniform(0, 700)
        by = 730 + r.uniform(0, 80)
        bl = .25 + .75 * abs(A.w(t, 1.2 + r.uniform(0, 1.2), i * .17))
        pp += (f'<path d="M{bx:.0f},{by:.0f} l60,-16" stroke="#e8eef6"'
               f' stroke-width="6" stroke-linecap="round" opacity="{.5+.5*bl:.2f}"/>')
        pp += (f'<circle cx="{bx+64:.0f}" cy="{by-17:.0f}" r="9"'
               f' fill="{[TKAN, ZOL, "#3f5c7a"][i%3]}" {o(2)}/>')
        pp += (f'<circle cx="{bx+10:.0f}" cy="{by-3:.0f}" r="{6*bl:.1f}"'
               f' fill="#ffffff" opacity="{bl:.2f}"/>')
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.36)
    return s


# ═══════════════════ ПЛАН 73 ═══════════════════

def mamino_plate_stanovitsya_dochkinym(t):
    """Мамино платье на столе становится дочкиным. Живые: ножницы идут по
    ткани, платье уменьшается, девочка идёт, придерживая подол."""
    s = SL(Z_NEBO, _komnata(900, "#bfa98b", t, True, .0))
    dal = baza.okno_izby(1400, 140, 350, 300, t, svet=True, moroz=.3)
    dal += baza.luch(1450, 180, 200, 620, t, .20)
    dal += baza.polka(80, 260, 300)
    dal += _katushka(150, 246, .7, KREM, t, .3)
    dal += _katushka(240, 248, .65, TKAN, t, .8)
    dal += teplo(560, 480, 700, 540, .32)
    s += SL(Z_DAL, dal)

    sr = baza.stol(40, 700, 960, 44, True)
    um = A.ease(A.seg(t, .5, 1.7))
    k = 1.0 - .40 * um
    ax, ay = 520, 470
    sr += (f'<g transform="translate({ax:.0f},{ay:.0f}) scale({k:.3f})'
           f' translate({-ax:.0f},{-ay:.0f})">')
    sr += _plate_lezhit(ax, ay, t, 1.0, "tkan")
    sr += "</g>"
    u = A.ease(A.seg(t, .4, 1.9))
    nx = ax - 300 + 600 * u
    ny = ay + 196 - 40 * math.sin(math.pi * u)
    sr += (f'<path d="M{ax-300:.0f},{ay+196:.0f} q300,-40 600,0" fill="none"'
           f' stroke="#f4efe2" stroke-width="8" stroke-dasharray="22 15"'
           f' opacity=".85"/>')
    sr += _nozhnicy(nx, ny, -14 + 10 * math.sin(2 * math.pi * t),
                    abs(A.w(t, .62)), t, 1.25)
    s += SL(Z_SRED, sr)

    dx = 1250 + 58 * t
    dbase, dh = 1050, 440
    pp = ob.figura(dx, dbase, dh, t, col="#8d2f2c", kant="#ffd79a", krasnoe=True)
    pod = 24 * A.w(t, 1.1)
    pp += (f'<path d="M{dx-96:.0f},{dbase-124:.0f} q96,20 192,0'
           f' L{dx+150:.0f},{dbase-4:.0f} q-150,{-34-pod*.5:.0f} -300,0 z"'
           f' fill="{ob.ALYJ}" stroke="{ob.ALYJ2}" stroke-width="7"/>')
    for sg in (-1, 1):
        pp += (f'<path d="M{dx+sg*146:.0f},{dbase-10:.0f}'
               f' l{sg*12:.0f},{-54-pod*.6:.0f}" stroke="{ob.ALYJ2}"'
               f' stroke-width="18" stroke-linecap="round"/>')
    s += SL(Z_PERED, pp + baza.begushchiy_blik(t, 7.6, .1, .09))
    s += baza.vinetka(.34)
    return s


# ═══════════════════ ПЛАН 74 ═══════════════════

def vorotnichok_i_busy_iz_ryabiny(t):
    """Стол у окна: к простому платью пришивается кружевной воротничок, рядом
    нанизываются рябиновые бусы. Живые: игла ходит, ягоды нанизываются,
    воротничок ложится на платье."""
    s = SL(Z_NEBO, _komnata(920, "#b5a388", t, True, .0))
    dal = baza.okno_izby(700, 90, 460, 380, t, svet=True, moroz=.28)
    dal += baza.luch(780, 150, 280, 700, t, .24)
    dal += baza.ryabina(1620, 500, t, 1.1, 5)
    dal += teplo(860, 440, 760, 580, .36)
    s += SL(Z_DAL, dal)

    sr = baza.stol(20, 700, 1880, 48, True)
    sr += _plate_lezhit(500, 540, t, .86, None, "#8ea8bc")
    s += SL(Z_SRED, sr)

    lo = A.out(A.seg(t, .5, 1.6))
    vx, vy = 500, 306 + 46 * lo
    pp = f'<g transform="rotate({-14+14*lo:.1f} {vx:.0f} {vy:.0f})">'
    pp += ten(vx + 10, vy + 92, 150, 18, .32 * lo)
    pp += (f'<path d="M{vx-168:.0f},{vy:.0f} q168,-66 336,0'
           f' q-36,118 -168,122 q-132,-4 -168,-122 z" fill="#fbf7ee" {o(7)}/>')
    for i in range(13):
        a = math.pi * (i + .5) / 13
        pp += (f'<circle cx="{vx-168*math.cos(a):.0f}"'
               f' cy="{vy+44+80*math.sin(a):.0f}" r="17" fill="none"'
               f' stroke="#e2d6bb" stroke-width="7"/>')
    for i in range(9):
        pp += (f'<circle cx="{vx-126+i*32:.0f}" cy="{vy+28:.0f}" r="9"'
               f' fill="none" stroke="#e2d6bb" stroke-width="5"/>')
    pp += (f'<path d="M{vx-168:.0f},{vy:.0f} q168,-66 336,0" fill="none"'
           f' stroke="#ffffff" stroke-width="8" opacity=".55"/>')
    pp += "</g>"
    u = (t / 1.25) % 1.0
    ix = vx - 150 + 300 * u
    iy = vy + 36 + 30 * math.sin(2 * math.pi * u)
    pp += _igla(ix, iy, -26 + 40 * math.sin(2 * math.pi * u), t, 100)
    for i in range(8):
        if i / 8.0 < u:
            pp += (f'<path d="M{vx-150+i*38:.0f},{vy+48:.0f} l24,-14"'
                   f' stroke="#d8c9a4" stroke-width="7" stroke-linecap="round"/>')
    nx, ny = 1280, 690
    pp += (f'<path d="M{nx-280:.0f},{ny:.0f} q280,{120+14*A.w(t,3.0):.0f} 520,-18"'
           f' fill="none" stroke="#c9b48a" stroke-width="9"/>')
    nag = int(A.ease(A.seg(t, .3, 4.6)) * 15)
    for i in range(15):
        u2 = (i + .5) / 15
        bx = nx - 280 + 520 * u2
        by = ny + 4 * 120 * u2 * (1 - u2) * .92 - 18 * u2 * u2
        if i < nag:
            pp += _busina(bx, by, 24, KRAS)
        elif i == nag:
            dp = 1.0 - A.seg(t, .3 + i * (4.6 / 15), 4.6 / 15)
            pp += _busina(bx, by - 140 * dp, 24, KRAS)
    pp += teplo(nx, ny + 40, 340, 220, .22)
    s += SL(Z_PERED, pp + baza.begushchiy_blik(t, 8.2, .6, .09))
    s += baza.vinetka(.34)
    return s


# ═══════════════════ ПЛАНЫ 75-76 ═══════════════════

def korobka_iz_pod_pechenya_s_pugovica(t):
    """Мостик в память: круглая коробка из-под печенья сверху. Живые: крышка
    снимается, пуговицы пересыпаются, ленты распрямляются.
    Окно вставки справа — коробка стоит в полосе 0-830."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#6d5a44"/>'
           + teplo(430, 520, 920, 800, .40))
    dal = f'<rect y="90" width="{W}" height="{H-90}" fill="url(#rush)"/>'
    for i in range(13):
        dal += (f'<path d="M{-60+i*170:.0f},90 q24,460 -8,{H:.0f}" fill="none"'
                f' stroke="#cdb98d" stroke-width="9" opacity=".5"/>')
    dal += baza.polka(1420, 250, 380)
    dal += _katushka(1500, 236, .8, TKAN, t, .1)
    dal += _katushka(1600, 238, .75, "#3f5c7a", t, .5)
    dal += _katushka(1700, 236, .7, ZOL, t, .9)
    s += SL(Z_DAL, dal)

    cx, cy = 420, 670
    rsp = A.ease(A.seg(t, 1.4, 2.4))
    sr = _lenta(90, 950, 560, t, ob.ALYJ, .0, rsp)
    sr += _lenta(170, 1014, 600, t, ob.ZOLOTO, .4, rsp * .85)
    sr += ten(cx + 24, cy + 250, 330, 54, .55)
    sr += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="360" ry="268"'
           f' fill="url(#med)" {o(9)}/>')
    sr += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="320" ry="232"'
           f' fill="#3a2a1c" {o(6)}/>')
    sr += (f'<path d="M{cx-320:.0f},{cy:.0f} a320,232 0 0 1 640,0 l-26,0'
           f' a294,210 0 0 0 -588,0 z" fill="#000000" opacity=".4"/>')
    r = random.Random(21)
    for i in range(54):
        a = r.uniform(0, 2 * math.pi)
        rad = math.sqrt(r.random()) * .86
        col = [TKAN, "#f3ead6", "#3f5c7a", ZOL, "#6d8a4e", "#b06a9a",
               "#2a2420", MED][i % 8]
        sr += _pugovica(cx + 300 * rad * math.cos(a), cy + 212 * rad * math.sin(a),
                        r.uniform(16, 34), col, t, i * .13, r.choice((2, 4)))
    for i, (kx, ky, kc, ks) in enumerate(((cx - 190, cy + 96, TKAN, .9),
                                          (cx + 76, cy + 136, "#3f5c7a", .8),
                                          (cx + 196, cy - 56, KREM, .75))):
        sr += _katushka(kx, ky, ks, kc, t, i * .3)
    s += SL(Z_SRED, sr)

    sn = A.out(A.seg(t, .25, 1.5))
    lx, ly = cx - 170 * sn, cy - 350 * sn
    pp = (f'<g opacity="{1 - .08*sn:.2f}"'
          f' transform="rotate({-9*sn:.1f} {lx:.0f} {ly:.0f})">')
    pp += ten(lx + 20, ly + 250, 320, 44, .45 * sn)
    pp += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="374" ry="278"'
           f' fill="url(#med)" {o(9)}/>')
    pp += (f'<ellipse cx="{lx:.0f}" cy="{ly-10:.0f}" rx="340" ry="250"'
           f' fill="url(#krem)" {o(6)}/>')
    pp += (f'<ellipse cx="{lx:.0f}" cy="{ly-10:.0f}" rx="286" ry="206"'
           f' fill="none" stroke="{MED}" stroke-width="8" opacity=".7"/>')
    for i in range(7):
        a = i * 2 * math.pi / 7 + .25
        fx = lx + 190 * math.cos(a)
        fy = ly - 10 + 134 * math.sin(a)
        kol = 2.4 * A.w(t, 3.0, i * .2)
        for kk in range(6):
            b = kk * math.pi / 3 + math.radians(kol)
            pp += (f'<ellipse cx="{fx+34*math.cos(b):.0f}" cy="{fy+30*math.sin(b):.0f}"'
                   f' rx="22" ry="16" fill="{[TKAN, "#b06a9a", "#3f5c7a"][i%3]}"'
                   f' opacity=".85" {o(3)}/>')
        pp += f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="15" fill="url(#zol)" {o(3)}/>'
    pp += (f'<path d="M{lx-250:.0f},{ly-160:.0f} q120,-80 300,-40"'
           f' fill="none" stroke="#ffffff" stroke-width="22" opacity=".25"/>')
    pp += "</g>"
    pp += baza.begushchiy_blik(t, 6.8, .2, .10)
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.40)
    return s
