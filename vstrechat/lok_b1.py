# -*- coding: utf-8 -*-
"""Декорации планов 1-20 ролика «Как встречать год хозяйки года 2027»."""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob
OKNO = (860, 300, 980, 551)


# ═══════════════════ СВОИ КИРПИЧИКИ БЛОКА ═══════════════════
# Градиентов defs() базы на праздничную гамму не хватает (ткань платья,
# эмаль ведра, бумага календаря), поэтому свои кладём рядом с предметом —
# так же, как это делают vinetka() и vozduh() в baza.

def _g(idn, c1, c2, vert=True):
    x2, y2 = ("0", "1") if vert else ("1", "0")
    return (f'<linearGradient id="{idn}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def _rad(idn, col, op=.55):
    return (f'<radialGradient id="{idn}" cx=".5" cy=".5" r=".5">'
            f'<stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')


def _stena(t, pol_y=900, c1="#4d5f78", c2="#1c2534", polosy=True):
    """Стена комнаты и дощатый пол. Синева — холод, тёплое пятно даёт огонь."""
    s = _g("b1st", c1, c2)
    s += f'<rect width="{W}" height="{H}" fill="url(#b1st)"/>'
    if polosy:
        for i in range(14):
            s += (f'<rect x="{i*W/13.0:.0f}" y="0" width="26" height="{pol_y:.0f}"'
                  f' fill="#ffffff" opacity=".04"/>')
    s += polovicy(pol_y)
    return s


def _okno_noch(x, y, w_, h_, t, moroz=.5, seed=7):
    """Окно, за которым идёт снег: живой дальний план для комнатных сцен."""
    r = random.Random(seed)
    vid = f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="#16203a"/>'
    for i in range(20):
        px = x + r.uniform(0, w_); p0 = r.uniform(0, 1)
        py = y + ((p0 + t * r.uniform(.07, .22)) % 1.0) * h_
        vid += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(2.0,4.4):.1f}"'
                f' fill="#dce9f7" opacity=".75"/>')
    return okno_izby(x, y, w_, h_, t, vid=vid, moroz=moroz)


def _hlopya(t, n=22, seed=12, sp=1.0):
    """Крупные хлопья ближнего плана — мельче снег уже сыплет baza."""
    r = random.Random(seed)
    s = ""
    for i in range(n):
        x0 = r.uniform(-40, W + 40); p0 = r.uniform(0, 1)
        v = r.uniform(7, 15) * sp; rr = r.uniform(7, 15); ph = r.uniform(0, 1)
        p = (p0 + t * v / H) % 1.0
        x = x0 + 70 * A.w(t, 6.5, ph)
        s += (f'<circle cx="{x:.0f}" cy="{p*(H+140)-70:.0f}" r="{rr:.1f}" fill="#ffffff"'
              f' opacity="{.35+.35*abs(A.w(t,4.0,ph)):.2f}"/>')
    return s


def _sugrob(y, amp=40, col="url(#sneg)", op=1.0):
    return (f'<path d="M-40,{y+amp} q300,{-amp*2:.0f} 620,{-14} q300,{amp:.0f} 640,{-22}'
            f' q260,{-amp*1.6:.0f} 740,{-6} L1960,{H+40} L-40,{H+40} Z"'
            f' fill="{col}" opacity="{op:.2f}" {o(5)}/>')


def _krylco(x, base, w_, t, lenta=0.0, zerkalo=1):
    """Крыльцо избы: три ступени со снегом, столбы, перила и козырёк.
    `lenta` 0..1 — доля вспыхнувшей на перилах красной ленты."""
    sg = 1 if zerkalo >= 0 else -1
    s = _g("b1kry", "#b4854f", "#66401f")
    s += ten(x + w_ * .5, base + 12, w_ * .62, 24, .55)
    for i in range(3):
        sw = w_ * (.60 + i * .14)
        sx = x + (w_ - sw) / 2
        sy = base - 38 * (3 - i)
        s += (f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="38" rx="7"'
              f' fill="url(#b1kry)" {o(5)}/>')
        s += (f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="12" rx="5"'
              f' fill="url(#sneg)" opacity=".92"/>')
    pl_y = base - 150
    s += (f'<rect x="{x:.0f}" y="{pl_y:.0f}" width="{w_:.0f}" height="38" rx="8"'
          f' fill="url(#b1kry)" {o(6)}/>')
    s += (f'<rect x="{x+8:.0f}" y="{pl_y:.0f}" width="{w_-16:.0f}" height="11" rx="5"'
          f' fill="url(#sneg)" opacity=".8"/>')
    # столбы и козырёк
    for sx in (x + 16, x + w_ - 50):
        s += (f'<rect x="{sx:.0f}" y="{pl_y-330:.0f}" width="34" height="330" rx="8"'
              f' fill="url(#derev)" {o(5)}/>')
    vys = 120 + w_ * .30                      # козырёк круче: скат читается крышей
    s += (f'<path d="M{x-40:.0f},{pl_y-330:.0f} L{x+w_*.5:.0f},{pl_y-330-vys:.0f}'
          f' L{x+w_+40:.0f},{pl_y-330:.0f} Z" fill="{DOSKA2}" {o(6)}/>')
    s += (f'<path d="M{x-48:.0f},{pl_y-330:.0f} L{x+w_*.5:.0f},{pl_y-336-vys:.0f}'
          f' L{x+w_+48:.0f},{pl_y-330:.0f} l-46,0 L{x+w_*.5:.0f},{pl_y-300-vys:.0f}'
          f' L{x-2:.0f},{pl_y-330:.0f} Z" fill="url(#sneg)" {o(4)}/>')
    # перила
    pe_y = pl_y - 118
    s += (f'<rect x="{x+10:.0f}" y="{pe_y:.0f}" width="{w_-20:.0f}" height="20" rx="8"'
          f' fill="url(#derev)" {o(5)}/>')
    for i in range(6):
        bx = x + 40 + i * (w_ - 90) / 5
        s += (f'<rect x="{bx:.0f}" y="{pe_y+20:.0f}" width="15" height="98"'
              f' fill="url(#derev)" {o(4)}/>')
    if lenta > .01:
        kol = 9 * A.w(t, 2.2)
        gor = .55 + .45 * abs(A.w(t, 1.1))
        d = f'M{x+14:.0f},{pe_y+4:.0f}'
        for i in range(6):
            x1 = x + 14 + (w_ - 28) * (i + 1) / 6.0
            d += f' q{-(w_-28)/12:.0f},{(26 if i % 2 == 0 else -22)+kol:.0f} {(w_-28)/6:.0f},0'
        s += (f'<path d="{d}" fill="none" stroke="{ob.ALYJ}" stroke-width="26"'
              f' stroke-linecap="round" opacity="{min(1.0, lenta)*gor:.2f}"/>')
        s += (f'<path d="{d}" fill="none" stroke="#ff8d72" stroke-width="8"'
              f' stroke-linecap="round" opacity="{min(1.0, lenta)*.5:.2f}"/>')
        s += teplo(x + w_ * .5, pe_y + 10, w_ * .6, 90, .4 * lenta)
    return s


def _stul(x, base, t, s_=1.0, dx=0.0, ph=0.0):
    """Венский стул: гнутая спинка, сиденье, четыре ножки."""
    s = _g("b1stu", "#b07b45", "#5c3819")
    g = f'<g transform="translate({x+dx:.1f},{base:.1f}) scale({s_:.3f})">'
    g += ten(0, 10, 130, 24, .5)
    for lx, sk in ((-96, -26), (-54, -6), (54, 6), (96, 26)):
        g += (f'<path d="M{lx},-58 q{sk*.3:.0f},36 {sk:.0f},58" fill="none"'
              f' stroke="#6d4421" stroke-width="18" stroke-linecap="round"/>')
    g += (f'<path d="M-112,-66 h224 q14,34 -10,40 h-204 q-24,-6 -10,-40 z"'
          f' fill="url(#b1stu)" {o(6)}/>')
    g += (f'<path d="M-100,-62 h200" fill="none" stroke="#f0d49a" stroke-width="6"'
          f' opacity=".35"/>')
    for ux in (-92, 86):
        g += (f'<path d="M{ux},-66 q{-ux*.12:.0f},-130 {-ux*.06:.0f},-212" fill="none"'
              f' stroke="url(#b1stu)" stroke-width="20" stroke-linecap="round"/>')
    g += (f'<path d="M-98,-278 q98,-44 196,0" fill="none" stroke="url(#b1stu)"'
          f' stroke-width="24" stroke-linecap="round"/>')
    g += (f'<path d="M-72,-236 q72,-36 144,0" fill="none" stroke="#8a5a2c"'
          f' stroke-width="14" stroke-linecap="round"/>')
    g += '</g>'
    return s + g


def _plate(idn, x, ytop, h_, t, c1="#f7efdc", c2="#c9b991", kach=0.0,
           kruzhevo=False, karman=0.0, ph=0.0, plechiki=True):
    """Платье на плечиках: крючок, плечики, лиф с талией и юбка колоколом.
    `kach` — угол качания, `karman` 0..1 — насколько отогнут кармашек."""
    sh = h_ / 520.0
    pl, ta, yu = 122 * sh, 76 * sh, 196 * sh          # плечо, талия, подол
    yt, yta, yh = ytop + 30 * sh, ytop + 215 * sh, ytop + h_ - 18 * sh
    s = _g(idn, c1, c2)
    g = f'<g transform="rotate({kach:.2f} {x:.1f} {ytop:.1f})">'
    if plechiki:
        g += (f'<path d="M{x:.0f},{ytop-30*sh:.0f} q{-16*sh:.0f},{-26*sh:.0f} 0,{-34*sh:.0f}'
              f' q{16*sh:.0f},{8*sh:.0f} 0,{34*sh:.0f}" fill="none"'
              f' stroke="#c8ccd2" stroke-width="{7*sh:.1f}"/>')
        g += (f'<path d="M{x-pl-10*sh:.0f},{yt+4*sh:.0f} L{x:.0f},{ytop-26*sh:.0f}'
              f' L{x+pl+10*sh:.0f},{yt+4*sh:.0f}" fill="none" stroke="#9aa2ab"'
              f' stroke-width="{12*sh:.1f}" stroke-linejoin="round"/>')
    g += ten(x + 10 * sh, yh + 26 * sh, yu * .85, 22 * sh, .45)
    # силуэт: плечи — талия — колокол юбки
    g += (f'<path d="M{x-pl:.0f},{yt:.0f}'
          f' q{pl*.45:.0f},{-30*sh:.0f} {pl*.9:.0f},{-6*sh:.0f}'
          f' q{pl*.45:.0f},{-24*sh:.0f} {pl*1.1:.0f},{6*sh:.0f}'
          f' q{-14*sh:.0f},{64*sh:.0f} {-(pl-ta):.0f},{yta-yt:.0f}'
          f' q{(yu-ta)*.5:.0f},{(yh-yta)*.6:.0f} {yu-ta:.0f},{yh-yta:.0f}'
          f' q{-yu:.0f},{44*sh:.0f} {-yu*2:.0f},0'
          f' q{(yu-ta)*.5:.0f},{-(yh-yta)*.4:.0f} {yu-ta:.0f},{-(yh-yta):.0f}'
          f' q{-(pl-ta)*.6:.0f},{-(yta-yt)*.55:.0f} {-(pl-ta):.0f},{-(yta-yt):.0f} z"'
          f' fill="url(#{idn})" {o(max(4, 6*sh))}/>')
    # пройма, талия, складки юбки
    for sgn in (-1, 1):
        g += (f'<path d="M{x+sgn*(pl-16*sh):.0f},{yt+10*sh:.0f}'
              f' q{sgn*10*sh:.0f},{40*sh:.0f} {-sgn*18*sh:.0f},{64*sh:.0f}" fill="none"'
              f' stroke="{c2}" stroke-width="{5*sh:.1f}" opacity=".6"/>')
    g += (f'<path d="M{x-ta-4*sh:.0f},{yta:.0f} q{ta+4*sh:.0f},{26*sh:.0f} {ta*2+8*sh:.0f},0"'
          f' fill="none" stroke="{c2}" stroke-width="{9*sh:.1f}" opacity=".75"/>')
    for i in range(5):
        fx = x - ta * .8 + i * ta * .4
        g += (f'<path d="M{fx:.0f},{yta+18*sh:.0f} q{(fx-x)*.5:.0f},{(yh-yta)*.6:.0f}'
              f' {(fx-x)*1.1:.0f},{yh-yta-10*sh:.0f}" fill="none" stroke="{c2}"'
              f' stroke-width="{5*sh:.1f}" opacity=".5"/>')
    # вырез и блик
    g += (f'<path d="M{x-44*sh:.0f},{yt-4*sh:.0f} q{44*sh:.0f},{52*sh:.0f} {88*sh:.0f},0"'
          f' fill="none" stroke="{c2}" stroke-width="{7*sh:.1f}" opacity=".7"/>')
    g += (f'<path d="M{x-pl*.5:.0f},{yt+30*sh:.0f} q{18*sh:.0f},{70*sh:.0f} {4*sh:.0f},{130*sh:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{9*sh:.1f}" opacity=".3"/>')
    if kruzhevo:
        drozh = 3.0 * A.w(t, 1.1, ph)
        for i in range(11):
            cx = x - 60 * sh + i * 12 * sh
            g += (f'<circle cx="{cx:.0f}" cy="{yt+10*sh+drozh+abs(cx-x)*.12:.1f}"'
                  f' r="{11*sh:.0f}" fill="#f4f1e8" opacity=".92" {o(max(2, 3*sh))}/>')
        g += (f'<path d="M{x-66*sh:.0f},{yt-2*sh+drozh:.1f} q{66*sh:.0f},{54*sh:.0f} {132*sh:.0f},0"'
              f' fill="none" stroke="#f4f1e8" stroke-width="{7*sh:.1f}" opacity=".85"/>')
    if karman > -.5:
        kx, ky = x + 58 * sh, yta + 86 * sh
        otg = 30 * sh * karman
        kw, kh = 62 * sh, 60 * sh
        g += (f'<path d="M{kx-kw:.0f},{ky:.0f} h{kw*2:.0f} v{kh:.0f}'
              f' q{-kw:.0f},{16*sh:.0f} {-kw*2:.0f},0 z" fill="{c2}" opacity=".85"'
              f' {o(max(3, 4*sh))}/>')
        if karman > .3:
            g += (f'<ellipse cx="{kx:.0f}" cy="{ky+6*sh:.0f}" rx="{kw*.86:.0f}"'
                  f' ry="{8*sh+otg*.5:.1f}" fill="#2a2420" opacity="{min(.6, karman):.2f}"/>')
        g += (f'<path d="M{kx-kw-3*sh:.0f},{ky:.0f} h{kw*2+6*sh:.0f} l{-8*sh:.0f},{-otg:.1f}'
              f' q{-(kw-4*sh):.0f},{-18*sh-otg*.6:.1f} {-(kw*2-8*sh):.0f},0 z"'
              f' fill="url(#{idn})" {o(max(3, 4*sh))}/>')
    g += '</g>'
    return s + g


def _pidzhak(x, ytop, h_, t, karman_vyv=0.0, ph=0.0):
    """Пола пиджака с нагрудным карманом; `karman_vyv` 0..1 — вывернут."""
    sh = h_ / 420.0
    s = _g("b1pid", "#3a4150", "#171c26")
    g = f'<g transform="translate({x:.1f},{ytop:.1f})">'
    g += ten(10 * sh, h_ + 16 * sh, 128 * sh, 20 * sh, .45)
    g += (f'<path d="M{-116*sh:.0f},{20*sh:.0f} q{116*sh:.0f},{-48*sh:.0f} {232*sh:.0f},0'
          f' l{14*sh:.0f},{h_-20*sh:.0f} q{-130*sh:.0f},{34*sh:.0f} {-260*sh:.0f},0 z"'
          f' fill="url(#b1pid)" {o(max(4, 6*sh))}/>')
    g += (f'<path d="M{-40*sh:.0f},{2*sh:.0f} L{-6*sh:.0f},{176*sh:.0f} L{-92*sh:.0f},{96*sh:.0f} z"'
          f' fill="#242a36" {o(max(3, 4*sh))}/>')
    g += (f'<path d="M{40*sh:.0f},{2*sh:.0f} L{6*sh:.0f},{176*sh:.0f} L{92*sh:.0f},{96*sh:.0f} z"'
          f' fill="#2b3240" {o(max(3, 4*sh))}/>')
    for i in range(2):
        g += (f'<circle cx="{14*sh:.0f}" cy="{(210+i*78)*sh:.0f}" r="{14*sh:.0f}"'
              f' fill="url(#zol)" {o(max(2, 3*sh))}/>')
    # карман: клапан, прорезь со строчкой и вывернутая подкладка мешочком
    kx, ky = 72 * sh, 150 * sh
    kw = 56 * sh
    if karman_vyv > .01:
        k = min(1.0, karman_vyv)
        bol = 7 * A.w(t, 1.35, ph) * k
        gl = 150 * sh * k                      # глубина вывернутого мешочка
        g += (f'<path d="M{kx-kw:.0f},{ky+16*sh:.0f}'
              f' q{-14*sh+bol:.1f},{gl*.78:.0f} {kw*.52:.0f},{gl:.0f}'
              f' q{kw*.92:.0f},{16*sh*k:.0f} {kw*1.48:.0f},{-gl:.0f}'
              f' q{-12*sh:.0f},{-gl*.78:.0f} {-kw*2:.0f},{-16*sh:.0f} z"'
              f' fill="#efe7d3" {o(max(3, 4*sh))}/>')
        g += (f'<ellipse cx="{kx:.0f}" cy="{ky+22*sh:.0f}" rx="{kw*.84:.0f}"'
              f' ry="{14*sh*k:.1f}" fill="#8e8367" opacity="{.5*k:.2f}"/>')
        g += (f'<path d="M{kx-kw*.5:.0f},{ky+gl*.66:.0f} q{kw*.5:.0f},{26*sh*k:.0f} {kw:.0f},0"'
              f' fill="none" stroke="#bfb295" stroke-width="{6*sh:.1f}" opacity=".85"/>')
    g += (f'<path d="M{kx-kw-4*sh:.0f},{ky:.0f} h{kw*2+8*sh:.0f} v{16*sh:.0f}'
          f' h{-kw*2-8*sh:.0f} z" fill="#161c26" {o(max(3, 4*sh))}/>')
    g += (f'<g transform="rotate({-10*min(1.0, karman_vyv):.1f} {kx-kw:.0f} {ky:.0f})">'
          f'<path d="M{kx-kw-4*sh:.0f},{ky:.0f} h{kw*2+8*sh:.0f} v{46*sh:.0f}'
          f' q{-kw-4*sh:.0f},{16*sh:.0f} {-kw*2-8*sh:.0f},0 z" fill="#333a49"'
          f' {o(max(3, 4*sh))}/>'
          f'<path d="M{kx-kw*.8:.0f},{ky+36*sh:.0f} q{kw*.8:.0f},{18*sh:.0f} {kw*1.6:.0f},0"'
          f' fill="none" stroke="#6d7a8d" stroke-width="{4*sh:.1f}" opacity=".6"/></g>')
    g += '</g>'
    return s + g


def _ochki(x, y, t, s_=1.0, ph=0.0):
    """Очки на шнурке: качаются сами — третий живой элемент у фигуры."""
    ang = 7 * A.w(t, 2.4, ph)
    g = f'<g transform="rotate({ang:.2f} {x:.0f} {y-60*s_:.0f})">'
    g += (f'<path d="M{x:.0f},{y-120*s_:.0f} q{-18*s_:.0f},{40*s_:.0f} {-4*s_:.0f},{60*s_:.0f}"'
          f' fill="none" stroke="{ZOL}" stroke-width="{4*s_:.1f}"/>')
    for sgn in (-1, 1):
        g += (f'<circle cx="{x+sgn*26*s_:.0f}" cy="{y:.0f}" r="{22*s_:.0f}"'
              f' fill="#cfe3f0" opacity=".45" stroke="{ZOL}" stroke-width="{5*s_:.1f}"/>')
    g += (f'<path d="M{x-6*s_:.0f},{y-4*s_:.0f} h{12*s_:.0f}" fill="none"'
          f' stroke="{ZOL}" stroke-width="{5*s_:.1f}"/>')
    g += (f'<circle cx="{x-32*s_:.0f}" cy="{y-10*s_:.0f}" r="{7*s_:.0f}" fill="#ffffff" opacity=".5"/>')
    g += '</g>'
    return g


def _ryumka(x, base, t, s_=1.0, ph=0.0):
    """Праздничная рюмка: стекло с бликом, блик дышит."""
    bl = .3 + .7 * abs(A.w(t, 2.6, ph))
    g = f'<g transform="translate({x:.1f},{base:.1f}) scale({s_:.3f})">'
    g += ten(0, 6, 26, 7, .4)
    g += f'<path d="M-24,-78 h48 q-4,46 -24,60 q-20,-14 -24,-60 z" fill="{STEKLO}" opacity=".55" {o(4)}/>'
    g += f'<path d="M0,-18 v14" fill="none" {o(5)}/><path d="M-20,0 h40" fill="none" {o(5)}/>'
    g += f'<path d="M-18,-70 q6,38 10,46" fill="none" stroke="#ffffff" stroke-width="7" opacity="{bl:.2f}"/>'
    g += '</g>'
    return g


def _tarelka(x, y, s_=1.0, kant=True):
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(2, 14, 74, 12, .4)
    g += f'<ellipse rx="76" ry="26" fill="url(#krem)" {o(5)}/>'
    g += f'<ellipse rx="48" ry="15" fill="#fbf4e4" {o(3)}/>'
    if kant:
        g += f'<ellipse rx="64" ry="21" fill="none" stroke="{ob.ALYJ}" stroke-width="5" opacity=".75"/>'
    g += f'<path d="M-52,-10 q22,-12 44,-6" fill="none" stroke="#ffffff" stroke-width="6" opacity=".6"/>'
    g += '</g>'
    return g


def _blyudo(x, y, t, s_=1.0, par_on=True):
    """Горячее блюдо на подносе: горка, подлива, пар."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(4, 20, 110, 18, .5)
    g += f'<ellipse rx="112" ry="34" fill="url(#krem)" {o(6)}/>'
    g += f'<ellipse cy="-12" rx="92" ry="26" fill="url(#med)" {o(5)}/>'
    g += f'<path d="M-62,-20 q62,-54 124,0 q-62,22 -124,0 z" fill="url(#solom)" {o(5)}/>'
    g += f'<path d="M-30,-34 q30,-16 58,-2" fill="none" stroke="#f6dfa8" stroke-width="7" opacity=".7"/>'
    g += '</g>'
    if par_on:
        g += par(x, y - 48 * s_, t, 5, .5, 190 * s_, .42, s_)
    return g


def _moneta(x, y, s_=1.0, fase=0.0):
    """Монета: `fase` — фаза вращения, ребро даёт объём при качении."""
    k = abs(math.cos(fase))
    rx = max(4.0, 30 * s_ * k)
    g = f'<g transform="translate({x:.1f},{y:.1f})">'
    g += (f'<ellipse rx="{rx:.1f}" ry="{30*s_:.1f}" fill="url(#zol)" {o(max(3, 4*s_))}/>')
    g += (f'<ellipse rx="{rx*.62:.1f}" ry="{19*s_:.1f}" fill="none" stroke="#8a6116"'
          f' stroke-width="{3*s_:.1f}" opacity=".7"/>')
    g += (f'<ellipse cx="{-rx*.3:.1f}" cy="{-9*s_:.1f}" rx="{max(2.0, rx*.3):.1f}"'
          f' ry="{8*s_:.1f}" fill="#fff3c8" opacity=".75"/>')
    g += '</g>'
    return g


def _bant(x, y, s_=1.0, p=1.0, col=None):
    """Красный бант, который завязывается сам: петли вырастают, концы падают."""
    c = col or ob.ALYJ
    pp = A.out(max(0.0, min(1.0, p)))
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += (f'<path d="M-180,0 q90,{-26*pp:.0f} 180,0 q90,{26*pp:.0f} 180,0" fill="none"'
          f' stroke="{c}" stroke-width="22" stroke-linecap="round"/>')
    for sgn in (-1, 1):
        g += (f'<g transform="translate({sgn*18},0) scale({pp:.3f},{pp:.3f})">'
              f'<path d="M0,0 q{sgn*96},-72 {sgn*112},-4 q{sgn*10},62 {-sgn*112},4 z"'
              f' fill="{c}" {o(6)}/>'
              f'<path d="M{sgn*30},-18 q{sgn*44},-20 {sgn*62},-4" fill="none"'
              f' stroke="#ff9a86" stroke-width="7" opacity=".5"/></g>')
        g += (f'<path d="M{sgn*12},6 q{sgn*34},{64*pp:.0f} {sgn*18},{128*pp:.0f}" fill="none"'
              f' stroke="{ob.ALYJ2}" stroke-width="20" stroke-linecap="round"'
              f' opacity="{pp:.2f}"/>')
    g += f'<circle r="{24*pp:.0f}" fill="{c}" {o(5)}/>'
    g += f'<circle cx="-7" cy="-8" r="{8*pp:.0f}" fill="#ff9a86" opacity=".6"/>'
    g += '</g>'
    return g


def _karandash(x, y, ang=0.0, s_=1.0, col=None):
    """Карандаш — он работает сам, рук не рисуем (правило 6)."""
    c = col or "#c23a2c"
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">'
    g += ten(14 * s_, 16 * s_, 54 * s_, 10 * s_, .35)
    g += (f'<path d="M0,0 l{22*s_:.0f},{-12*s_:.0f} l{14*s_:.0f},{8*s_:.0f} z"'
          f' fill="#e8d9b8" {o(max(2, 3*s_))}/>')
    g += (f'<path d="M{10*s_:.0f},{-5*s_:.0f} l{12*s_:.0f},{-7*s_:.0f} l{6*s_:.0f},{4*s_:.0f} z" fill="{c}"/>')
    g += (f'<rect x="{30*s_:.0f}" y="{-26*s_:.0f}" width="{210*s_:.0f}" height="{26*s_:.0f}"'
          f' rx="{5*s_:.0f}" fill="{c}" {o(max(2, 3*s_))}'
          f' transform="rotate(-29 {30*s_:.0f} {-26*s_:.0f})"/>')
    g += (f'<rect x="{36*s_:.0f}" y="{-20*s_:.0f}" width="{196*s_:.0f}" height="{6*s_:.0f}"'
          f' fill="#ffffff" opacity=".28" transform="rotate(-29 {30*s_:.0f} {-26*s_:.0f})"/>')
    g += '</g>'
    return g


def _banka(x, base, t, s_=1.0, op=1.0, col="#cf9a4a", ph=0.0):
    """Банка с крышкой: содержимое и блик. Таять будет прозрачностью."""
    if op <= .02:
        return ""
    g = f'<g transform="translate({x:.1f},{base:.1f}) scale({s_:.3f})" opacity="{op:.2f}">'
    g += ten(0, 6, 40, 9, .4)
    g += f'<path d="M-38,0 v-112 q38,-16 76,0 v112 z" fill="{STEKLO}" opacity=".5" {o(5)}/>'
    g += f'<path d="M-32,-6 v-78 q32,-12 64,0 v78 z" fill="{col}" opacity=".85"/>'
    g += f'<rect x="-42" y="-130" width="84" height="24" rx="7" fill="url(#zhel)" {o(4)}/>'
    g += f'<path d="M-24,-100 v76" fill="none" stroke="#ffffff" stroke-width="8" opacity=".35"/>'
    g += '</g>'
    return g


def _lozhka(x, y, t, s_=1.0, zvon=0.0):
    """Ложка на полке: от звона подрагивает."""
    ang = 9 * zvon * A.w(t, .42)
    g = f'<g transform="rotate({ang:.2f} {x:.0f} {y:.0f})">'
    g += ten(x + 4, y + 10, 46 * s_, 7 * s_, .35)
    g += (f'<ellipse cx="{x-42*s_:.0f}" cy="{y:.0f}" rx="{26*s_:.0f}" ry="{16*s_:.0f}"'
          f' fill="url(#zhel)" {o(max(2, 3*s_))}/>')
    g += (f'<ellipse cx="{x-46*s_:.0f}" cy="{y-4*s_:.0f}" rx="{11*s_:.0f}" ry="{6*s_:.0f}"'
          f' fill="#e8eef4" opacity=".65"/>')
    g += (f'<rect x="{x-18*s_:.0f}" y="{y-7*s_:.0f}" width="{96*s_:.0f}" height="{13*s_:.0f}"'
          f' rx="{6*s_:.0f}" fill="url(#zhel)" {o(max(2, 3*s_))}/>')
    g += '</g>'
    return g


def _vedro(x, base, t, s_=1.0, vid="emal", voda=True, duzhka=0.0, op=1.0):
    """Ведро: эмалированное или пластиковое. `duzhka` 0..1 — поднята дужка."""
    if op <= .02:
        return ""
    if vid == "emal":
        s = _g("b1ved", "#f4f7fa", "#9fb6c6")
        korp, kant = "url(#b1ved)", "#2f5d86"
    else:
        s = _g("b1vedp", "#6f8ea8", "#2d4055")
        korp, kant = "url(#b1vedp)", "#8fa9bd"
    g = f'<g transform="translate({x:.1f},{base:.1f}) scale({s_:.3f})" opacity="{op:.2f}">'
    g += ten(6, 12, 128, 24, .55)
    g += (f'<path d="M-124,-212 h248 l-30,212 q-94,22 -188,0 z" fill="{korp}" {o(7)}/>')
    g += (f'<path d="M-124,-212 q124,-30 248,0 q-124,30 -248,0 z" fill="{kant}"'
          f' opacity=".9" {o(5)}/>')
    g += (f'<path d="M-118,-196 l-18,160" fill="none" stroke="#ffffff" stroke-width="16"'
          f' opacity=".35"/>')
    g += (f'<path d="M96,-188 l22,150" fill="none" stroke="#1b2a38" stroke-width="12"'
          f' opacity=".18"/>')
    if vid == "emal":
        g += (f'<path d="M-120,-150 q120,26 240,0" fill="none" stroke="{kant}"'
              f' stroke-width="12" opacity=".8"/>')
    else:
        for i in range(3):
            g += (f'<path d="M{-118+i*4:.0f},{-170+i*52:.0f} q{118-i*3:.0f},24 {236-i*6:.0f},0"'
                  f' fill="none" stroke="#1f2e3d" stroke-width="6" opacity=".35"/>')
    if voda:
        ryab = 5 * A.w(t, 2.4)
        g += (f'<path d="M-112,-186 q112,{-26+ryab:.1f} 224,0 q-112,{30:.0f} -224,0 z"'
              f' fill="#3f7f96" opacity=".92"/>')
        g += (f'<ellipse cx="-34" cy="-186" rx="44" ry="9" fill="#bfe6f2" opacity="{.3+.4*abs(A.w(t,1.9)):.2f}"/>')
    # дужка: поднята — встаёт дугой над ведром, упала — ложится на край
    d = max(0.0, min(1.0, duzhka))
    pod = 34 + 210 * d
    tilt = 4.0 * (1 - d) * A.w(t, .55)
    for ex in (-122, 122):
        g += (f'<circle cx="{ex}" cy="-206" r="13" fill="url(#zhel)" {o(4)}/>')
    g += (f'<g transform="rotate({tilt:.2f} 0 -206)">'
          f'<path d="M-122,-206 q122,{-pod*1.5:.0f} 244,0" fill="none" stroke="url(#zhel)"'
          f' stroke-width="14" stroke-linecap="round"/>'
          f'<path d="M-104,{-206-pod*.52:.0f} q104,{-pod*.5:.0f} 208,0" fill="none"'
          f' stroke="#eef3f8" stroke-width="5" stroke-linecap="round" opacity=".45"/></g>')
    g += '</g>'
    return s + g


def _paket(x, base, t, s_=1.0, uzel=0.0, op=1.0):
    """Завязанный мусорный пакет: мятый бок, узел затягивается сам."""
    if op <= .02:
        return ""
    u = A.out(max(0.0, min(1.0, uzel)))
    s = _g("b1pak", "#5a6a74", "#222c33")
    g = f'<g transform="translate({x:.1f},{base:.1f}) scale({s_:.3f})" opacity="{op:.2f}">'
    g += ten(6, 12, 132, 24, .55)
    g += (f'<path d="M-130,0 q-26,-136 36,-186 q94,-50 188,0 q62,50 36,186 z"'
          f' fill="url(#b1pak)" {o(7)}/>')
    for i, (mx, my) in enumerate(((-66, -62), (18, -96), (62, -40))):
        g += (f'<path d="M{mx},{my} q30,{-34+i*10:.0f} 58,{-6:.0f}" fill="none"'
              f' stroke="#79888f" stroke-width="7" opacity=".45"/>')
    g += (f'<path d="M-120,-30 q120,26 240,0" fill="none" stroke="#0f161b"'
          f' stroke-width="10" opacity=".3"/>')
    # ГОРЛОВИНА И УЗЕЛ. Прежний вариант давал «два рога»: уши были длиннее
    # самого мешка и торчали тонкими усами (контактный лист 13.11). Теперь
    # горловина стянута светлой лентой, уши короткие и толстые.
    sh = 1.0 - .34 * u
    g += (f'<g transform="translate(0,-186) scale({sh:.3f},1)">'
          f'<path d="M-84,0 q-16,-62 26,-96 q58,-26 116,0 q42,34 26,96 z"'
          f' fill="url(#b1pak)" {o(7)}/></g>')
    for sgn in (-1, 1):
        g += (f'<path d="M{sgn*20},-272 q{sgn*(54-26*u):.0f},-30 {sgn*(30-12*u):.0f},-62"'
              f' fill="none" stroke="#3b4850" stroke-width="34" stroke-linecap="round"/>')
        g += (f'<path d="M{sgn*20},-272 q{sgn*(54-26*u):.0f},-30 {sgn*(30-12*u):.0f},-62"'
              f' fill="none" {o(6)} opacity=".55"/>')
    g += (f'<ellipse cy="-268" rx="{72-26*u:.0f}" ry="{26-6*u:.0f}" fill="#2b353d" {o(6)}/>')
    g += (f'<path d="M{-60+22*u:.0f},-268 q{60-22*u:.0f},16 {120-44*u:.0f},0" fill="none"'
          f' stroke="#c3ccd4" stroke-width="9" opacity=".7"/>')
    g += '</g>'
    return s + g


def _tuchka(x, y, t, s_=1.0, ph=0.0, szhatie=1.0):
    """Серая хмурая тучка: брови домиком, бока дышат, протискивается в щель."""
    dy = 9 * s_ * A.w(t, 1.6, ph)
    g = (f'<g transform="translate({x:.1f},{y+dy:.1f}) scale({s_*szhatie:.3f},{s_:.3f})">')
    g += ten(0, 56, 70, 12, .35)
    g += f'<ellipse cy="0" rx="130" ry="80" fill="#cfdae6" opacity=".18"/>'
    g += (f'<path d="M-96,20 q-30,-54 18,-72 q6,-54 66,-44 q44,-34 82,8'
          f' q52,-4 44,52 q10,46 -40,56 z" fill="#aeb9c6" {o(8)}/>')
    g += (f'<path d="M-66,-16 q44,-22 86,-6" fill="none" stroke="#c3ccd4"'
          f' stroke-width="9" opacity=".5"/>')
    for sgn, bx in ((-1, -40), (1, 34)):
        g += (f'<path d="M{bx-24:.0f},{-6+sgn*0:.0f} q22,{-18 if sgn<0 else -18:.0f} 46,{4:.0f}"'
              f' fill="none" stroke="#2f3944" stroke-width="10" stroke-linecap="round"'
              f' transform="rotate({-16*sgn:.0f} {bx:.0f} -6)"/>')
        g += f'<circle cx="{bx:.0f}" cy="{18:.0f}" r="9" fill="#2f3944"/>'
    g += f'<path d="M-18,48 q18,-14 38,0" fill="none" stroke="#2f3944" stroke-width="8" stroke-linecap="round"/>'
    g += '</g>'
    return g


def _listok(x, y, w_, h_, flip=0.0, col="#f6efdc", col2="#d6c9a8"):
    """Листок месяца: при перелистывании складывается по верхнему краю."""
    k = math.cos(math.pi * max(0.0, min(1.0, flip)))
    lico = k >= 0
    g = (f'<g transform="translate({x:.1f},{y:.1f}) scale(1,{abs(k):.3f})">')
    g += (f'<rect x="{-w_/2:.0f}" y="0" width="{w_:.0f}" height="{h_:.0f}" rx="8"'
          f' fill="{col if lico else col2}" {o(5)}/>')
    g += (f'<rect x="{-w_/2:.0f}" y="0" width="{w_:.0f}" height="{h_*.2:.0f}" rx="8"'
          f' fill="{ob.ALYJ}" opacity="{.85 if lico else .4:.2f}"/>')
    for i in range(4):
        g += (f'<path d="M{-w_/2+12:.0f},{h_*(.42+i*.14):.0f} h{w_-24:.0f}" fill="none"'
              f' stroke="{col2}" stroke-width="5" opacity=".8"/>')
    g += '</g>'
    return g


def _shkaf(x, base, w_, h_, t, dverca=0.0, zerkalo=False, ph=0.0, nutro="#2a2f3a"):
    """Шкаф: корпус, нутро, дверца на петле слева (0 закрыта, 1 раскрыта)."""
    s = _g("b1shk", "#a2743f", "#58361a")
    g = f'<g>'
    g += ten(x + w_ * .5, base + 12, w_ * .54, 22, .5)
    g += (f'<rect x="{x:.0f}" y="{base-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10"'
          f' fill="{nutro}" {o(7)}/>')
    g += (f'<rect x="{x+16:.0f}" y="{base-h_+26:.0f}" width="{w_-32:.0f}" height="16" rx="7"'
          f' fill="url(#zhel)" {o(4)}/>')
    sh = 1.0 - .86 * max(0.0, min(1.0, dverca))
    g += (f'<g transform="translate({x:.0f},0) scale({sh:.3f},1)">'
          f'<rect x="0" y="{base-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10"'
          f' fill="url(#b1shk)" {o(7)}/>'
          f'<rect x="{w_*.1:.0f}" y="{base-h_+h_*.07:.0f}" width="{w_*.8:.0f}"'
          f' height="{h_*.82:.0f}" rx="8" fill="none" stroke="#6d4421" stroke-width="7"/>')
    if zerkalo:
        bl = ((t * .34 + ph) % 1.0)
        g += (f'<rect x="{w_*.14:.0f}" y="{base-h_+h_*.1:.0f}" width="{w_*.72:.0f}"'
              f' height="{h_*.76:.0f}" rx="6" fill="url(#stekl)" opacity=".7"/>')
        g += (f'<path d="M{w_*.14+w_*.72*bl:.0f},{base-h_+h_*.1:.0f} l{w_*.2:.0f},0'
              f' l{-w_*.3:.0f},{h_*.76:.0f} l{-w_*.2:.0f},0 z" fill="#ffffff" opacity=".3"/>')
    g += (f'<circle cx="{w_*.88:.0f}" cy="{base-h_*.52:.0f}" r="12" fill="url(#zhel)" {o(4)}/>')
    g += '</g></g>'
    return s + g


# ═══════════════════ ДЕКОРАЦИИ 1-20 ═══════════════════

def ognennaya_hozyayka_u_krylca(t):
    """Зимняя ночь, изба с тёплыми окнами и крыльцом, на дорожке — хозяйка
    года, красная коза. Живое: дышит огненное свечение шерсти, коза поводит
    ухом и бубенчиком, крупные хлопья снега падают."""
    s = baza.nebo("noch", t)
    s += baza.oblaka(t, 170, 3, 7, .2, "#9db0c8", 5.0)
    s += ulica_dal(1130, 742, 760, t)
    s += SL(Z_DAL, _sugrob(772, 34, "#dbe6f2", .95))
    s += SL(Z_SRED, izba_snaruzhi(30, 846, 700, t)
            + _okno_noch(214, 560, 176, 148, t, .45, 3)
            + _krylco(470, 946, 330, t, A.ease(A.seg(t, 1.5, .6)))
            + _sugrob(912, 46))
    # хозяйка года на дорожке: свечение шерсти дышит
    puls = .78 + .22 * abs(A.w(t, 2.3))
    s += SL(0, _rad("b1zar", "#ff7a28", .72) + _rad("b1zar2", "#ffd08a", .6)
            + f'<ellipse cx="946" cy="808" rx="{420*puls:.0f}" ry="{350*puls:.0f}"'
              f' fill="url(#b1zar)" opacity="{.9*puls:.2f}"/>'
            + f'<ellipse cx="946" cy="820" rx="{250*puls:.0f}" ry="{210*puls:.0f}"'
              f' fill="url(#b1zar2)" opacity="{.85*puls:.2f}"/>'
            + teplo(946, 800, 300 * puls, 260 * puls, .7)
            + ob.koza(946, 952, t, .82, 0.0, True, .1)
            + iskra_let(t, 946, 880, 14, 4, 340, .5)
            + f'<ellipse cx="946" cy="962" rx="230" ry="42" fill="#ffb060"'
              f' opacity="{.18*puls:.2f}"/>')
    s += SL(Z_PERED, _sugrob(1012, 54, "#f2f7ff", 1.0)
            + f'<ellipse cx="946" cy="982" rx="190" ry="34" fill="#9fc0dd" opacity=".35"/>')
    s += ramka_pp("levo", "#0a0f1a", .72)
    s += SL(Z_LETIT, _hlopya(t, 24, 12, .9))
    s += sneg_letit(t, 46, 5, .7, .9)
    s += vinetka(.44)
    return s


def dva_stula_u_prazdnichnogo_stola(t):
    """Праздничный стол и два стула: на спинке одного чёрное платье, на другом
    пиджак с вывернутым пустым карманом. Живое: стулья отъезжают от стола,
    карман болтается, огоньки свечей качаются."""
    ot = A.ease(A.seg(t, .5, 2.1))
    s = SL(Z_NEBO, _stena(t, 940, "#4a5d78", "#1b2433"))
    s += SL(Z_DAL, _okno_noch(1470, 170, 340, 310, t, .4, 9)
            + ob.girlyanda(100, 150, 1860, 190, t, 14, 110)
            + ob.elka(210, 940, 460, t, True, True, 4))
    # стол: столешница, скатерть, приборы
    g = ten(960, 962, 560, 30, .5)
    g += f'<rect x="600" y="690" width="740" height="44" rx="12" fill="url(#derev)" {o(7)}/>'
    g += (f'<path d="M580,690 h780 v48 q-390,40 -780,0 z" fill="url(#rush)" {o(6)}/>')
    g += (f'<path d="M580,738 q390,40 780,0 l-26,186 q-364,30 -728,0 z" fill="url(#rush)" {o(6)}/>')
    g += (f'<path d="M592,754 q384,38 756,0" fill="none" stroke="{ob.ALYJ}"'
          f' stroke-width="8" opacity=".65"/>')
    g += (_tarelka(760, 700, .78) + _tarelka(1170, 700, .78) + _blyudo(960, 694, t, .8)
          + svecha(700, 578, t, .1, 1.0) + svecha(1230, 578, t, .55, 1.0)
          + ob.bokal(850, 700, t, .56, .2) + ob.bokal(1080, 700, t, .56, .7)
          + teplo(960, 630, 600, 360, .5))
    s += SL(Z_SRED, g)
    # левый стул: чёрное платье переброшено через спинку
    lx = 410 - ot * 200
    s += SL(0, _stul(410, 946, t, 1.25, -ot * 200)
            + _plate("b1chp", lx + 10, 686, 250, t, "#3b3442", "#141219",
                     2.4 * A.w(t, 3.1), True, -1, .2, False)
            + f'<path d="M{lx-130:.0f},692 q130,-34 260,0 q-130,26 -260,0 z"'
              f' fill="#2a2531" {o(5)}/>')
    # правый стул: пиджак с вывернутым карманом
    rx = 1500 + ot * 200
    s += SL(0, _stul(1500, 946, t, 1.25, ot * 200)
            + _pidzhak(rx, 650, 270, t, A.ease(A.seg(t, .9, 1.0)), .4)
            + f'<path d="M{rx-130:.0f},660 q130,-34 260,0 q-130,26 -260,0 z"'
              f' fill="#262c38" {o(5)}/>')
    s += SL(Z_PERED, f'<rect y="1024" width="{W}" height="68" fill="#0e1420" opacity=".85"/>'
            + f'<ellipse cx="{lx:.0f}" cy="1016" rx="220" ry="28" fill="#0a0f18" opacity=".45"/>'
            + f'<ellipse cx="{rx:.0f}" cy="1016" rx="220" ry="28" fill="#0a0f18" opacity=".45"/>')
    s += vinetka(.4)
    return s


def nastennyy_kalendar_na_pruzhine(t):
    """Перекидной календарь на пружине: карандаш зачёркивает первое число,
    страница перелистывается, красный карандаш обводит второе. Живое:
    страница переворачивается, карандаш ведёт линию, пружина покачивается."""
    s = SL(Z_NEBO, _stena(t, 930, "#43566f", "#1a2230"))
    s += SL(Z_DAL, _okno_noch(130, 210, 280, 260, t, .5, 11)
            + lampa(1700, 380, t, .95, True) + teplo(1700, 500, 560, 440, .5)
            + polka(1430, 560, 380) + krynka(1500, 554, .7) + _ryumka(1620, 554, t, 1.0, .3)
            + ob.elka(240, 936, 300, t, True, False, 7)
            + ob.girlyanda(60, 120, 1880, 160, t, 13, 90))
    kach = 1.8 * A.w(t, 2.6)
    x0, y0, w_, h_ = 900, 150, 680, 680
    g = f'<g transform="rotate({kach:.2f} {x0} {y0-40})">'
    g += ten(x0 + 26, y0 + h_ + 46, w_ * .5, 28, .5)
    g += (f'<rect x="{x0-w_/2-20:.0f}" y="{y0-58:.0f}" width="{w_+40:.0f}" height="{h_+100:.0f}"'
          f' rx="16" fill="url(#derev)" {o(7)}/>')
    g += _g("b1bum", "#fbf5e4", "#cdbf9c")
    # нижний лист — на нём обводка
    g += (f'<rect x="{x0-w_/2:.0f}" y="{y0:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10"'
          f' fill="url(#b1bum)" {o(6)}/>')
    g += (f'<rect x="{x0-w_/2:.0f}" y="{y0:.0f}" width="{w_:.0f}" height="{h_*.26:.0f}" rx="10"'
          f' fill="{ob.ALYJ}" opacity=".88"/>')
    for r_ in range(4):
        for c_ in range(6):
            g += (f'<rect x="{x0-w_/2+46+c_*96:.0f}" y="{y0+h_*.34+r_*96:.0f}" width="68"'
                  f' height="68" rx="8" fill="#ffffff" opacity=".45"'
                  f' stroke="#c9bb97" stroke-width="3"/>')
    cx6 = x0 - w_ / 2 + 46 + 2 * 96 + 34
    cy6 = y0 + h_ * .34 + 96 + 34
    ob_p = A.out(A.seg(t, 2.0, 1.5))
    if ob_p > .01:
        per = 2 * math.pi * 64
        g += (f'<ellipse cx="{cx6:.0f}" cy="{cy6:.0f}" rx="64" ry="50" fill="none"'
              f' stroke="{ob.ALYJ}" stroke-width="12" stroke-linecap="round"'
              f' stroke-dasharray="{per:.0f}" stroke-dashoffset="{per*(1-ob_p):.0f}"'
              f' transform="rotate(-8 {cx6:.0f} {cy6:.0f})"/>')
    # верхний лист: зачёркнут и перелистывается
    fl = A.ease(A.seg(t, 1.2, .75))
    zp = A.ease(A.seg(t, .15, .85))
    if fl < .999:
        k = math.cos(math.pi * fl)
        verh = "url(#b1bum)" if k >= 0 else "#d8cbab"
        g += (f'<g transform="translate({x0:.0f},{y0:.0f}) scale(1,{abs(k):.3f})'
              f' translate({-x0:.0f},{-y0:.0f})">')
        g += (f'<rect x="{x0-w_/2:.0f}" y="{y0:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10"'
              f' fill="{verh}" {o(6)}/>')
        if k >= 0:
            g += (f'<rect x="{x0-w_/2:.0f}" y="{y0:.0f}" width="{w_:.0f}" height="{h_*.26:.0f}"'
                  f' rx="10" fill="{ob.HVOYA}" opacity=".85"/>')
            for r_ in range(4):
                for c_ in range(6):
                    g += (f'<rect x="{x0-w_/2+46+c_*96:.0f}" y="{y0+h_*.34+r_*96:.0f}" width="68"'
                          f' height="68" rx="8" fill="#ffffff" opacity=".4"'
                          f' stroke="#c9bb97" stroke-width="3"/>')
            for i in range(2):
                x1 = x0 - w_ / 2 + 60 + i * 30
                g += (f'<path d="M{x1:.0f},{y0+h_*.36:.0f} l{150*zp:.0f},{150*zp:.0f}"'
                      f' fill="none" stroke="#2f3944" stroke-width="13" stroke-linecap="round"'
                      f' opacity=".85"/>')
        g += '</g>'
    # пружина
    for i in range(10):
        sx = x0 - w_ / 2 + 36 + i * (w_ - 72) / 9
        g += (f'<path d="M{sx:.0f},{y0-26:.0f} q20,-44 0,-60" fill="none" stroke="url(#zhel)"'
              f' stroke-width="12" stroke-linecap="round"/>')
    g += '</g>'
    s += SL(Z_SRED, g)
    # карандаши работают сами, рук не рисуем
    if fl < .05:
        s += SL(0, _karandash(x0 - w_ / 2 + 90 + 150 * zp, y0 + h_ * .36 + 150 * zp,
                              10, 1.3, "#2f3944"))
    if .02 < ob_p < .995:
        a = -math.pi * .5 + 2 * math.pi * ob_p
        s += SL(0, _karandash(cx6 + 64 * math.cos(a), cy6 + 50 * math.sin(a), 16, 1.3, ob.ALYJ))
    s += SL(Z_PERED, f'<rect y="986" width="{W}" height="106" fill="#121a26" {o(6)}/>'
            + f'<rect y="986" width="{W}" height="16" fill="#2b3644"/>'
            + _mandarin_kuchka(t))
    s += vinetka(.42)
    return s


def _mandarin_kuchka(t):
    """Горка мандаринов на комоде переднего плана — тёплое пятно у нижнего края."""
    return (ob.mandarin(250, 1016, .8, .35, t) + ob.mandarin(340, 1030, .72, 0.0, t)
            + ob.mandarin(300, 964, .66, 0.0, t) + teplo(300, 1000, 300, 180, .35))


def ognennaya_loshad_na_krylce(t):
    """То же крыльцо с другой стороны: на нём стоит огненная лошадь и бьёт
    копытом. Живое: грива горит и колышется, копыто бьёт по доскам,
    пар из ноздрей."""
    s = baza.nebo("noch", t)
    s += baza.oblaka(t, 190, 3, 5, .2, "#9db0c8", 5.0)
    s += ulica_dal(40, 770, 640, t)
    s += SL(Z_DAL, _sugrob(798, 32, "#dbe6f2", .95))
    s += SL(Z_SRED, izba_snaruzhi(1230, 900, 660, t)
            + _okno_noch(1406, 620, 166, 140, t, .45, 5)
            + _krylco(900, 1010, 440, t, 0.0)
            + _sugrob(968, 44))
    bit = max(0.0, math.sin(2 * math.pi * (t / 1.7))) ** 3
    # 13.11: лошадь (.58) сливалась с навесом крыльца — УКРУПНЕНА, но
    # ОСТАВЛЕНА НА КРЫЛЬЦЕ, как требует раскадровка («стоит на нём и бьёт
    # копытом»): первая правка унесла её на снег и разошлась с заданием
    bx, by = 1008, 1004
    s += SL(0, teplo(bx - 40, by - 240, 600, 460, .6)
            + ob.loshad(bx, by, t, .74, 0.0)
            + "".join(f'<circle cx="{bx+104+i*20-bit*34:.0f}" cy="{by-130-bit*44-i*9:.0f}"'
                      f' r="{(5+i*3.0)*bit:.1f}" fill="#eef5ff" opacity="{.6*bit:.2f}"/>'
                      for i in range(5)))
    s += SL(Z_PERED, _sugrob(1042, 52, "#f2f7ff", 1.0))
    s += ramka_pp("pravo", "#0a0f1a", .62)
    s += SL(Z_LETIT, _hlopya(t, 20, 15, .8))
    s += sneg_letit(t, 42, 8, .65, .85)
    s += vinetka(.44)
    return s


def chasy_nad_prazdnichnym_stolom(t):
    """Комната, накрытый стол, над ним круглые часы без пяти двенадцать.
    Живое: стрелка вздрагивает, маятник качается, свечи горят."""
    s = SL(Z_NEBO, _stena(t, 940, "#44566f", "#19212f"))
    s += SL(Z_DAL, _okno_noch(140, 230, 300, 280, t, .45, 4)
            + ob.girlyanda(70, 150, 1850, 190, t, 13, 120)
            + ob.elka(1660, 940, 420, t, True, True, 6))
    # часы с маятником над столом
    cx, cy = 790, 250
    vzd = .004 * (1 if (t * 2) % 1 < .5 else 0)
    g = _g("b1kor", "#8f6134", "#4d2d14")
    g += ten(cx + 16, 700, 130, 22, .4)
    g += (f'<rect x="{cx-86:.0f}" y="{cy+66:.0f}" width="172" height="330" rx="14"'
          f' fill="url(#b1kor)" {o(7)}/>')
    g += (f'<rect x="{cx-60:.0f}" y="{cy+92:.0f}" width="120" height="278" rx="10"'
          f' fill="url(#stekl)" opacity=".5" {o(4)}/>')
    mang = 13 * A.w(t, 1.9)
    g += (f'<g transform="rotate({mang:.2f} {cx:.0f} {cy+100:.0f})">'
          f'<line x1="{cx:.0f}" y1="{cy+100:.0f}" x2="{cx:.0f}" y2="{cy+300:.0f}"'
          f' stroke="url(#med)" stroke-width="10"/>'
          f'<circle cx="{cx:.0f}" cy="{cy+316:.0f}" r="38" fill="url(#zol)" {o(5)}/>'
          f'<circle cx="{cx-12:.0f}" cy="{cy+304:.0f}" r="11" fill="#fff6d2" opacity=".6"/></g>')
    g += (f'<path d="M{cx-86:.0f},{cy+72:.0f} h172" fill="none" stroke="#3c2410"'
          f' stroke-width="8" opacity=".7"/>')
    g += ob.kuranty(cx, cy, t, 1.1, .54 + vzd)
    g += teplo(cx, cy, 380, 340, .34)
    s += SL(Z_SRED, g)
    # накрытый стол
    tg = ten(960, 1000, 620, 32, .5)
    tg += f'<rect x="330" y="770" width="1260" height="46" rx="12" fill="url(#derev)" {o(7)}/>'
    tg += f'<path d="M310,770 h1300 v50 q-650,42 -1300,0 z" fill="url(#rush)" {o(6)}/>'
    tg += (f'<path d="M310,820 q650,42 1300,0 l-28,200 q-622,32 -1244,0 z"'
           f' fill="url(#rush)" {o(6)}/>')
    tg += (f'<path d="M322,836 q644,40 1288,0" fill="none" stroke="{ob.ALYJ}"'
           f' stroke-width="8" opacity=".65"/>')
    tg += (_tarelka(560, 782, .8) + _tarelka(1360, 782, .8)
           + _blyudo(1130, 776, t, .9)
           + svecha(430, 650, t, .1, 1.1) + svecha(1500, 650, t, .6, 1.1)
           + ob.bokal(690, 782, t, .66, .2) + ob.bokal(1270, 782, t, .66, .7)
           + ob.mandarin(960, 766, .76, .4, t)
           + teplo(960, 760, 720, 380, .5))
    s += SL(0, tg)
    s += SL(Z_PERED, f'<rect y="1026" width="{W}" height="66" fill="#101823" opacity=".85"/>'
            + _stul(300, 1140, t, 1.3))
    s += vinetka(.42)
    return s


def babushka_razglazhivaet_skatert(t):
    """Бабушка со спины у стола: по белой скатерти сама бежит разглаживающая
    волна, тарелка встаёт на место, очки на шнурке качаются."""
    s = SL(Z_NEBO, _stena(t, 940, "#4b5d76", "#1d2735"))
    s += SL(Z_DAL, kvartira_veschi(1200, 940, 680, t, 11)
            + _okno_noch(120, 210, 270, 260, t, .4, 6)
            + ob.girlyanda(60, 120, 1880, 150, t, 12, 80))
    # стол с белой скатертью: не на весь кадр, подол короткий
    g = _g("b1ska", "#fdfaf0", "#cbd4de")
    g += ten(930, 1020, 600, 30, .5)
    g += f'<rect x="330" y="760" width="1200" height="40" rx="10" fill="url(#derev)" {o(7)}/>'
    g += f'<path d="M312,760 h1236 v44 q-618,38 -1236,0 z" fill="url(#b1ska)" {o(6)}/>'
    g += (f'<path d="M312,804 q618,38 1236,0 l-26,150 q-592,28 -1184,0 z"'
          f' fill="url(#b1ska)" {o(6)}/>')
    g += (f'<path d="M324,820 q612,36 1224,0" fill="none" stroke="{ob.ALYJ}"'
          f' stroke-width="7" opacity=".6"/>')
    for i in range(6):
        amp = 1.0 - A.ease(A.seg(t, .25 + i * .28, .7))
        if amp < .02:
            continue
        fx = 440 + i * 190
        g += (f'<path d="M{fx:.0f},820 q{20*amp:.0f},70 {-12*amp:.0f},140" fill="none"'
              f' stroke="#a9b6c4" stroke-width="{11*amp:.1f}" opacity="{.8*amp:.2f}"/>')
    s += SL(Z_SRED, g)
    dv = A.out(A.seg(t, .8, 1.1))
    s += SL(0, _tarelka(1150 - 160 * (1 - dv), 806 + 10 * (1 - dv), .84)
            + _tarelka(1400, 806, .84) + _tarelka(560, 806, .84)
            + f'<rect x="1270" y="786" width="150" height="12" rx="5" fill="url(#zhel)" {o(4)}/>'
            + svecha(860, 676, t, .2, 1.0)
            + teplo(900, 760, 620, 320, .42))
    s += SL(0, ob.figura(600, 1020, 660, t, "#3b2b3a", "#f0c070", True, .2, False, 1.0, False)
            # нарядная кофта: кайма и горошек по плечам, иначе силуэт — пятно
            + f'<path d="M{600-80:.0f},{1020-430:.0f} q80,34 160,0" fill="none"'
              f' stroke="{ob.ZOLOTO}" stroke-width="8" opacity=".7"/>'
            + "".join(f'<circle cx="{600-62+i*31:.0f}" cy="{1020-392+(abs(i-2))*7:.0f}"'
                      f' r="6" fill="{ob.ZOLOTO}" opacity=".65"/>' for i in range(5))
            + f'<path d="M{600-54:.0f},{1020-300:.0f} q54,22 108,0" fill="none"'
              f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".55"/>'
            + _ochki(742, 790, t, 1.1, .3))
    s += SL(Z_PERED, _stul(1640, 1120, t, 1.3)
            + f'<rect y="1042" width="{W}" height="50" fill="#111a26" opacity=".8"/>')
    s += vinetka(.4)
    return s


def karman_naryad_i_blyudo(t):
    """Три крупные детали подряд: монета опускается в карман, красный бант
    сам завязывается на платье, горячее блюдо встаёт на стол."""
    s = SL(Z_NEBO, _stena(t, 1000, "#3e4f68", "#161e2b", False)
           + "".join(teplo(320 + i * 640, 540, 340, 460, .34) for i in range(3)))
    s += SL(Z_DAL, ob.girlyanda(40, 130, 1880, 160, t, 13, 90)
            + "".join(f'<rect x="{640+i*640:.0f}" y="0" width="8" height="{H}"'
                      f' fill="#ffffff" opacity=".07"/>' for i in range(2))
            + "".join(f'<rect x="{60+i*640:.0f}" y="930" width="520" height="26" rx="8"'
                      f' fill="url(#derev)" {o(5)}/>' for i in range(3)))
    # 1. карман пиджака и монета
    mp = A.ease(A.seg(t, .2, 1.6))
    # ПОДСВЕТКА ЗА ПИДЖАКОМ (правка 13.11 по листу): тёмная вещь на тёмной
    # стене пропадала — ставим за ней светлое пятно и перекладину вешалки
    g1 = (teplo(300, 560, 300, 420, .5)
          + f'<rect x="120" y="296" width="360" height="14" rx="7" fill="url(#derev)" {o(4)}/>'
          + f'<path d="M240,300 q60,-30 120,0" fill="none" stroke="#c8a96a"'
            f' stroke-width="9" stroke-linecap="round"/>')
    g1 += _pidzhak(300, 330, 600, t, 0.0, .1)
    if mp < .99:
        g1 += teplo(404, 180 + 356 * mp, 170, 170, .5 * (1 - mp * .7))
        g1 += _moneta(404, 180 + 356 * mp, 1.5, t * 7.0)
    # 2. платье и красный бант, который завязывается сам
    g2 = _plate("b1nar", 960, 250, 620, t, "#f8f1df", "#cbbd98",
                1.6 * A.w(t, 3.4), False, -1, .4)
    g2 += _bant(960, 352, .92, A.seg(t, 1.7, 1.2))
    # 3. горячее блюдо встаёт на стол
    bp = A.out(A.seg(t, 3.0, 1.0))
    # блюдо встаёт НА СТОЛ, а не зависает: опора и тень под ним
    g3 = (f'<rect x="1380" y="946" width="440" height="30" rx="10"'
          f' fill="url(#derev)" {o(6)}/>'
          + ten(1600, 952, 180, 22, .55))
    g3 += _blyudo(1600, 932 - 230 * (1 - bp), t, 1.5)
    s += SL(Z_SRED, g1 + g2 + g3)
    s += SL(Z_PERED, f'<rect y="1004" width="{W}" height="88" fill="#0f1621" opacity=".85"/>')
    s += vinetka(.44)
    return s


def dvenadcat_mesyacev_s_monetoy(t):
    """Лента из двенадцати листков-месяцев: по ней катятся монета, бант и
    блюдо, рядом весь путь шагает фигурка. Живое: листки переворачиваются,
    монета катится, фигурка шагает."""
    s = baza.nebo("noch", t, True, 9)
    s += SL(Z_DAL, ob.girlyanda(40, 110, 1880, 140, t, 16, 80)
            + ob.elka(130, 980, 330, t, True, False, 5)
            + ob.elka(1800, 1000, 300, t, True, False, 8))
    # дорога-лента с перспективой
    g = _g("b1len", "#6a7b96", "#2a3447")
    g += (f'<path d="M-60,720 q500,-46 1000,-12 q520,32 1040,-22 l0,210'
          f' q-520,54 -1040,22 q-500,-34 -1000,12 z" fill="url(#b1len)" {o(7)}/>')
    g += (f'<path d="M-60,760 q500,-44 1000,-10 q520,30 1040,-20" fill="none"'
          f' stroke="#9eb0c8" stroke-width="8" stroke-dasharray="46 40" opacity=".55"/>')
    s += SL(Z_SRED, g)
    # двенадцать листков над лентой
    lg = ""
    for i in range(12):
        lx = 130 + i * 146
        ly = 250 + 26 * math.sin(i * .9)
        fl = A.seg(t, .15 + i * .19, .5)
        sez = (("#eef4fb", "#bcd0e4"), ("#eef4fb", "#bcd0e4"),
               ("#eef7e8", "#bcd3a8"), ("#eef7e8", "#bcd3a8"), ("#eef7e8", "#bcd3a8"),
               ("#fdf6df", "#dcc88c"), ("#fdf6df", "#dcc88c"), ("#fdf6df", "#dcc88c"),
               ("#f8ecd2", "#cfa96a"), ("#f8ecd2", "#cfa96a"), ("#f8ecd2", "#cfa96a"),
               ("#eef4fb", "#bcd0e4"))[i]
        lg += ten(lx + 8, ly + 268, 70, 14, .45)
        lg += (f'<g transform="rotate({-6 + (i % 3) * 5:.0f} {lx:.0f} {ly:.0f})">'
               + _listok(lx, ly, 132, 244, fl, sez[0], sez[1]) + '</g>')
    s += SL(Z_SRED, lg)
    # монета катится, следом бант и блюдо, рядом шагает фигурка
    pr = A.ease(A.seg(t, .15, 2.2))
    mx = 430 + 1270 * pr
    sh = abs(math.sin(2 * math.pi * (t / .62)))
    s += SL(0, teplo(mx, 720, 300, 200, .5)
            + _moneta(mx, 700 - 22 * abs(math.sin(2 * math.pi * pr * 3)), 1.9, mx * .018)
            + _bant(mx - 200, 706, .78, 1.0)
            + _blyudo(mx - 370, 724, t, .66)
            + ob.figura(max(150.0, mx - 560), 760 - 12 * sh, 330, t, "#2c2434",
                        "#f0c070", True, .1, True, 1.0, False))
    s += SL(Z_PERED, f'<path d="M-60,900 q520,-40 1020,-8 q520,30 1020,-16 L1980,1140 L-60,1140 Z"'
            f' fill="#0f1726" {o(6)}/>'
            + f'<path d="M-60,940 q520,-38 1020,-6 q520,28 1020,-14" fill="none"'
              f' stroke="#1d2838" stroke-width="10"/>')
    s += SL(Z_LETIT, ob.konfetti(t, 22, 9, .55, .7))
    s += vinetka(.42)
    return s


def krasnyy_bumazhnyy_fonar(t):
    """Красный бумажный фонарь с кистью над светлым платьем на плечиках.
    Живое: фонарь покачивается, кисть качается следом, красный свет ползёт
    по платью сверху вниз."""
    s = SL(Z_NEBO, _stena(t, 950, "#46586f", "#1b2432"))
    s += SL(Z_DAL, _shkaf(1500, 950, 380, 680, t, .08, True, .2)
            + _okno_noch(130, 240, 260, 250, t, .45, 8)
            + ob.girlyanda(60, 110, 1880, 150, t, 12, 80)
            + polka(380, 620, 300) + krynka(450, 614, .66))
    kach = 4.2 * A.w(t, 3.0)
    fx, fy = 820, 60
    g = _g("b1fon", "#e2493a", "#8d1b1c")
    g += f'<g transform="rotate({kach:.2f} {fx} {fy-40})">'
    g += f'<line x1="{fx}" y1="{fy-80}" x2="{fx}" y2="{fy+6}" stroke="{K}" stroke-width="6"/>'
    g += f'<rect x="{fx-46}" y="{fy}" width="92" height="22" rx="7" fill="url(#zol)" {o(4)}/>'
    g += f'<ellipse cx="{fx}" cy="{fy+118}" rx="122" ry="104" fill="url(#b1fon)" {o(7)}/>'
    for i in range(5):
        g += (f'<path d="M{fx-120+i*48:.0f},{fy+44:.0f} q16,84 0,164" fill="none"'
              f' stroke="{ob.ALYJ2}" stroke-width="5" opacity=".5"/>')
    g += f'<ellipse cx="{fx-44}" cy="{fy+84}" rx="34" ry="28" fill="#ff9a86" opacity=".45"/>'
    g += f'<rect x="{fx-46}" y="{fy+212}" width="92" height="22" rx="7" fill="url(#zol)" {o(4)}/>'
    kis = 7.0 * A.w(t, 3.0, .22)
    g += (f'<g transform="rotate({kis:.2f} {fx} {fy+234})">'
          f'<path d="M{fx-6},{fy+234} h12 l6,30 h-24 z" fill="url(#zol)" {o(4)}/>')
    for i in range(7):
        g += (f'<path d="M{fx-24+i*8:.0f},{fy+264:.0f} q{-4+i*1.4:.0f},58 {-8+i*2.6:.0f},108"'
              f' fill="none" stroke="{ob.ALYJ}" stroke-width="7" stroke-linecap="round"/>')
    g += '</g></g>'
    g += teplo(fx, fy + 120, 420, 380, .5)
    s += SL(Z_SRED, g)
    # платье и красный свет, ползущий по нему полосой
    polz = .5 + .5 * A.w(t, 5.2)
    py = 470 + polz * 420
    s += SL(0, _plate("b1sve", 820, 440, 560, t, "#f9f3e2", "#cdc0a0",
                      1.5 * A.w(t, 4.0), False, -1, .3)
            + _rad("b1kra", "#ff4a35", .55)
            + f'<ellipse cx="820" cy="{py:.0f}" rx="280" ry="130" fill="url(#b1kra)"'
              f' opacity=".7"/>'
            + f'<path d="M700,{py-28:.0f} q120,34 240,0 q-120,46 -240,0 z"'
              f' fill="{ob.ALYJ}" opacity=".26"/>')
    s += SL(Z_PERED, f'<rect y="1004" width="{W}" height="88" fill="#101925" opacity=".85"/>'
            + _mandarin_kuchka(t))
    s += vinetka(.42)
    return s


def babushka_shepchet_vnuchke(t):
    """Кухня: бабушка в профиль наклоняется к внучке и говорит ей на ухо,
    внучка серьёзно кивает, на подоконнике поблёскивают рюмки."""
    s = SL(Z_NEBO, _stena(t, 1000, "#4a6072", "#1b2630"))
    s += SL(Z_DAL, _okno_noch(1240, 200, 440, 350, t, .5, 13)
            + f'<rect x="1200" y="566" width="520" height="28" rx="8" fill="url(#derev)" {o(5)}/>'
            + "".join(_ryumka(1270 + i * 110, 592, t, 1.5, i * .27) for i in range(4))
            + dver(170, 250, 260, 680, .0, "url(#derev)", True)
            + ob.girlyanda(60, 120, 1180, 170, t, 9, 70))
    s += SL(Z_SRED, f'<rect x="120" y="856" width="1700" height="40" rx="12" fill="url(#derev)" {o(6)}/>'
            + f'<rect x="160" y="896" width="1620" height="190" rx="12" fill="{DOSKA2}" {o(5)}/>'
            + krynka(300, 850, 1.0) + karavay(1560, 854, .66, True)
            + _tarelka(1360, 852, .7)
            + lampa(880, 230, t, .95, True) + teplo(880, 430, 680, 500, .5))
    nak = 10.5 * A.ease(A.seg(t, .25, 1.0))
    s += SL(0, f'<g transform="rotate({nak:.2f} 700 866)">'
            + ob.figura(700, 866, 700, t, "#3c2b3c", "#f0c070", True, .2, True, 1.0, False)
            + '</g>'
            + _ochki(818, 616, t, 1.2, .4))
    kiv = 6.0 * A.w(t, .72, .1) * A.seg(t, 1.0, .6)
    s += SL(0, f'<g transform="rotate({kiv:.2f} 1010 872)">'
            + ob.figura(1010, 872, 440, t, "#36314a", "#f0c070", False, .55, True, 1.0, False)
            + '</g>')
    s += SL(Z_PERED, f'<rect y="1064" width="{W}" height="36" fill="#101822" opacity=".85"/>')
    s += ramka_pp("levo", "#0b1119", .5)
    s += vinetka(.42)
    return s


def vyvernutyy_karman(t):
    """Праздничный пиджак на плечиках, у него сам выворачивается боковой
    карман: внутри пусто, вылетает одна крошка. Живое: карман выворачивается,
    ткань подрагивает, крошка падает.

    ПЕРЕРИСОВАНО 13.11 по контактному листу: прежний вариант показывал полу
    пиджака во весь кадр, и карман читался как бежевая миска — предмет не
    опознавался. Теперь средний план: виден весь пиджак, карман крупный, но
    в масштабе вещи.
    """
    vyv = A.over(A.seg(t, .5, 1.3))
    drozh = .7 * A.w(t, 2.2)
    s = SL(Z_NEBO, _stena(t, 1000, "#465874", "#1a2432", False)
           + teplo(960, 430, 520, 520, .34))
    s += SL(Z_DAL, ob.girlyanda(40, 120, 1880, 150, t, 13, 86)
            + f'<rect x="300" y="196" width="1320" height="16" rx="8" fill="url(#derev)" {o(5)}/>'
            + "".join(f'<rect x="{360+i*300:.0f}" y="212" width="10" height="34"'
                      f' fill="#6d5a42"/>' for i in range(5)))
    # плечики и сам пиджак
    g = f'<g transform="rotate({drozh:.2f} 960 230)">'
    g += (f'<path d="M870,214 q90,-40 180,0" fill="none" stroke="#c8a96a"'
          f' stroke-width="11" stroke-linecap="round"/>')
    g += f'<path d="M960,196 q6,-22 0,-34" fill="none" {o(6)}/>'
    g += _pidzhak(960, 230, 660, t, vyv, .1)
    g += '</g>'
    s += SL(Z_SRED, g)
    # крошка вылетает из пустого кармана и падает
    kp = A.seg(t, 1.6, 1.5)
    if .01 < kp < .999:
        cx = 1072 + 210 * kp
        cy = 640 - 180 * math.sin(math.pi * kp) + 300 * kp * kp
        s += SL(0, f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="12" fill="#e6d7b0" {o(3)}/>'
                + f'<circle cx="{cx-4:.0f}" cy="{cy-4:.0f}" r="5" fill="#fff8e4" opacity=".75"/>')
    s += SL(Z_PERED, f'<rect y="1002" width="{W}" height="90" fill="#101823" opacity=".88"/>')
    s += vinetka(.44)
    return s


def pustye_polki_na_ves_god(t):
    """Кухонный шкафчик с четырьмя полками: банки тают сверху вниз, на
    нижней остаётся одна ложка. Живое: банки исчезают, дверца покачивается,
    ложка звякает."""
    s = SL(Z_NEBO, _stena(t, 950, "#4a5f70", "#1a242e"))
    s += SL(Z_DAL, "".join(
        f'<rect x="{60+c*96:.0f}" y="{120+r_*96:.0f}" width="88" height="88" rx="8"'
        f' fill="#ffffff" opacity=".05"/>' for c in range(19) for r_ in range(9)))
    x0, y0, w_, h_ = 540, 150, 840, 760
    g = _g("b1kuh", "#9c7b52", "#4f3a21")
    g += ten(x0 + w_ * .5 + 20, y0 + h_ + 30, w_ * .5, 26, .5)
    g += f'<rect x="{x0}" y="{y0}" width="{w_}" height="{h_}" rx="12" fill="#232a33" {o(8)}/>'
    g += f'<rect x="{x0+14}" y="{y0+14}" width="{w_-28}" height="{h_-28}" rx="8" fill="#2d3540"/>'
    for i in range(4):
        sy = y0 + 170 + i * 180
        g += (f'<rect x="{x0+14}" y="{sy:.0f}" width="{w_-28}" height="20" rx="6"'
              f' fill="url(#b1kuh)" {o(5)}/>')
        if i < 3:
            for j in range(4):
                op = 1.0 - A.ease(A.seg(t, .4 + i * .9 + j * .14, .5))
                g += _banka(x0 + 120 + j * 190, sy, t, .78, op,
                            ("#cf9a4a", "#b8323a", "#6f8c4a", "#d6a63f")[j], j * .2)
        else:
            g += _lozhka(x0 + 160, sy - 10, t, 1.0, A.seg(t, 3.3, .4))
    # дверца покачивается на петле справа
    kach = 7.0 + 4.5 * A.w(t, 3.4)
    g += (f'<g transform="translate({x0+w_:.0f},0) scale({-math.cos(math.radians(kach*4)):.3f},1)'
          f' translate({-x0-w_:.0f},0)">'
          f'<rect x="{x0+w_*.52:.0f}" y="{y0}" width="{w_*.48:.0f}" height="{h_}" rx="10"'
          f' fill="url(#b1kuh)" opacity=".97" {o(7)}/>'
          f'<rect x="{x0+w_*.58:.0f}" y="{y0+40}" width="{w_*.36:.0f}" height="{h_-80}" rx="8"'
          f' fill="none" stroke="#5f4526" stroke-width="7"/>'
          f'<circle cx="{x0+w_*.57:.0f}" cy="{y0+h_*.5:.0f}" r="13" fill="url(#zhel)" {o(4)}/></g>')
    s += SL(Z_SRED, g)
    s += SL(0, teplo(960, 520, 620, 480, .35))
    s += SL(Z_PERED, f'<rect y="968" width="{W}" height="124" fill="#1a222c" {o(6)}/>'
            + f'<rect y="968" width="{W}" height="18" fill="#2f3a46"/>')
    s += vinetka(.42)
    return s


def prazdnichnoe_plate_na_dverce_shkaf(t):
    """Спальня: на дверце шкафа светлое праздничное платье с кармашком.
    Кармашек сам отгибается — внутри пусто. Живое: платье покачивается,
    кармашек оттопыривается, зеркало шкафа ловит блик."""
    s = SL(Z_NEBO, _stena(t, 944, "#4b5a74", "#1c2432"))
    s += SL(Z_DAL, _okno_noch(1480, 250, 330, 300, t, .5, 17)
            + f'<rect x="60" y="690" width="620" height="40" rx="14" fill="url(#tkan)" {o(6)}/>'
            + f'<rect x="60" y="730" width="620" height="210" rx="12" fill="#43506b" {o(6)}/>'
            + f'<path d="M90,700 q150,-60 300,-6" fill="none" stroke="#f1e7cf" stroke-width="22"/>')
    s += SL(Z_SRED, _shkaf(830, 944, 520, 800, t, .0, True, .1)
            + lampa(340, 300, t, .8, True) + teplo(340, 470, 520, 400, .45))
    otg = .35 + .65 * (.5 + .5 * A.w(t, 2.6))
    # 13.11: платье стояло ровно на середине дверцы и читалось как бежевый
    # блок поверх шкафа — сдвинуто к краю створки и ужато по высоте
    s += SL(0, _plate("b1prz", 1176, 250, 520, t, "#faf4e3", "#cfc1a0",
                      2.1 * A.w(t, 3.6), False, otg, .2)
            + teplo(1176, 500, 380, 380, .32))
    s += SL(Z_PERED, f'<rect y="1016" width="{W}" height="76" fill="#121a26" opacity=".85"/>'
            + f'<path d="M-40,1092 q300,-120 620,-96 l0,96 z" fill="#1a2232" opacity=".9"/>')
    s += vinetka(.42)
    return s


def chernoe_plate_u_shkafa(t):
    """Раскрытый шкаф: нарядное чёрное платье с кружевным воротником само
    выезжает на плечиках, держится секунду и возвращается. Живое: платье
    качается, кружево подрагивает, плечики стучат о перекладину."""
    s = SL(Z_NEBO, _stena(t, 952, "#43536d", "#191f2c"))
    s += SL(Z_DAL, _okno_noch(130, 240, 260, 250, t, .5, 21)
            + lampa(1640, 300, t, .8, True) + teplo(1640, 470, 500, 400, .4))
    g = _shkaf(620, 952, 760, 820, t, .95, False, .0)
    # ряд вешалок в глубине
    for i in range(5):
        hx = 700 + i * 110
        g += (f'<path d="M{hx},176 q-12,-20 0,-26 q12,6 0,26" fill="none"'
              f' stroke="#b7bdc6" stroke-width="6"/>')
        g += (f'<path d="M{hx-56},214 L{hx},172 L{hx+56},214" fill="none" stroke="#9aa2ab"'
              f' stroke-width="9" stroke-linejoin="round"/>')
        g += (f'<path d="M{hx-52},216 q52,-30 104,0 q-14,180 4,300 q-56,24 -112,0'
              f' q18,-120 4,-300 z" fill="{("#2f3a4b","#4a3340","#333a33","#3a3440","#2b3340")[i]}"'
              f' opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, g)
    # платье выезжает и возвращается
    vyh = A.ease(A.seg(t, .25, 1.0)) - A.ease(A.seg(t, 2.0, 1.0))
    stuk = max(0.0, 1.0 - abs(t - 2.95) * 6.0) + max(0.0, 1.0 - abs(t - 1.3) * 6.0)
    px = 1000 + 420 * vyh
    s += SL(0, _plate("b1chrn", px, 250 - 10 * stuk, 620, t, "#3b3442", "#141219",
                      3.4 * A.w(t, 2.8) * (.4 + vyh), True, -1, .25)
            + f'<path d="M{px-70:.0f},176 q70,-16 140,0" fill="none" stroke="#c9d0d8"'
              f' stroke-width="{6+5*stuk:.1f}" opacity="{.5+.5*stuk:.2f}"/>')
    s += SL(Z_PERED, f'<rect y="1012" width="{W}" height="80" fill="#111926" opacity=".85"/>')
    s += vinetka(.42)
    return s


def dve_hmurye_tuchki_u_dveri(t):
    """Прихожая: за чёрным подолом в приоткрытую дверь лезут две хмурые
    тучки, дверь закрывается перед ними. Живое: тучки протискиваются,
    дверь закрывается, коврик у двери сдвигается."""
    zakr = A.ease(A.seg(t, .7, 2.2))
    stvor = .54 + .46 * zakr                 # створка едет на проём и закрывает его
    dx0, dw = 820, 560
    kray = dx0 + dw * stvor                  # где край створки, там и щель
    s = SL(Z_NEBO, _stena(t, 958, "#46566e", "#1a2230"))
    s += SL(Z_DAL, f'<rect x="{dx0}" y="150" width="{dw}" height="810" rx="10" fill="#1a2740"/>'
            + "".join(
                f'<circle cx="{dx0+20+((i*83)%520):.0f}"'
                f' cy="{150+((i*137+t*120*(1+i%3))%800):.0f}" r="{3+i%4:.0f}"'
                f' fill="#dceaf8" opacity=".75"/>' for i in range(26))
            + f'<rect x="{dx0}" y="760" width="{dw}" height="200" fill="#cfdeee" opacity=".55"/>'
            + f'<rect x="770" y="120" width="70" height="870" rx="8" fill="url(#derev)" {o(7)}/>'
            + f'<rect x="1360" y="120" width="70" height="870" rx="8" fill="url(#derev)" {o(7)}/>')
    # тучки лезут ровно в оставшуюся щель и сплющиваются
    shir = max(60.0, 1380 - kray)
    szh = max(.26, min(1.0, shir / 330.0))
    s += SL(Z_SRED, _tuchka(kray + shir * .42, 430, t, 1.15, .0, szh)
            + _tuchka(kray + shir * .62, 620, t, .9, .4, szh * .9))
    # дверь закрывается
    s += SL(0, f'<g transform="translate({dx0},0) scale({stvor:.3f},1)'
            f' translate({-dx0},0)">'
            + dver(dx0, 150, dw, 810, .0, "url(#derev)", True, True) + '</g>')
    # коврик сдвигается
    k = A.ease(A.seg(t, 1.0, 1.4))
    sdv = 54 * k
    s += SL(0, _g("b1kov", "#8d4a3c", "#4a2119")
            + f'<g transform="rotate({-2.2*k:.2f} 1100 990)">'
              f'<rect x="{860-sdv:.0f}" y="952" width="520" height="86" rx="12"'
              f' fill="url(#b1kov)" {o(6)}/>'
              f'<rect x="{890-sdv:.0f}" y="974" width="460" height="42" rx="8" fill="none"'
              f' stroke="{ob.ZOLOTO}" stroke-width="6" opacity=".6"/></g>')
    # чёрный подол платья на переднем плане
    s += SL(Z_PERED, _g("b1pod2", "#241e2b", "#0e0b12")
            + f'<path d="M-40,1092 q20,-270 170,-396 q62,66 136,196 q74,130 100,200 z"'
              f' fill="url(#b1pod2)" {o(7)}/>'
            + f'<path d="M-30,1058 q150,-54 350,-12" fill="none" stroke="#6b5a78"'
              f' stroke-width="9" opacity=".8"/>'
            + f'<path d="M40,740 q74,80 128,222" fill="none" stroke="#6b5a78"'
              f' stroke-width="7" opacity=".6"/>')
    s += vinetka(.44)
    return s


def dom_v_razreze_shkaf_v_kazhdoy_kvar(t):
    """Многоэтажный дом в разрезе, шесть комнат: в каждой шкаф, дверцы
    открываются одна за другой, и в каждом висит чёрное платье. Живое:
    дверцы открываются, платья качаются, свет в комнатах мигает."""
    s = baza.nebo("noch", t, True, 11)
    s += SL(Z_DAL, panelka(60, 980, 300, t, 6, True, 4)
            + panelka(1580, 980, 300, t, 6, True, 9)
            + _sugrob(960, 30, "#cfdcea", .9))
    x0, y0, cw, ch = 420, 180, 360, 380
    g = _g("b1dom", "#9aa3a8", "#636c74")
    g += ten(960, 992, 560, 26, .5)
    g += (f'<rect x="{x0-30}" y="{y0-40}" width="{cw*3+60}" height="{ch*2+80}" rx="12"'
          f' fill="url(#b1dom)" {o(8)}/>')
    for r_ in range(2):
        for c_ in range(3):
            i = r_ * 3 + c_
            rx, ry = x0 + c_ * cw, y0 + r_ * ch
            mig = .55 + .45 * abs(A.w(t, 2.0 + i * .5, i * .17))
            g += (f'<rect x="{rx}" y="{ry}" width="{cw-16}" height="{ch-16}" rx="8"'
                  f' fill="{("#44536b","#4c4458","#3f4e63","#514754","#3b4a5e","#4a4250")[i]}"'
                  f' {o(5)}/>')
            g += teplo(rx + cw * .5, ry + 60, 220, 180, .45 * mig)
            g += (f'<circle cx="{rx+cw*.5:.0f}" cy="{ry+54:.0f}" r="16" fill="{SVET}"'
                  f' opacity="{mig:.2f}"/>')
            g += (f'<rect x="{rx+10}" y="{ry+ch-56}" width="{cw-36}" height="18" rx="6"'
                  f' fill="#4a3522" opacity=".9"/>')
            # шкаф
            sw, shh = 150, 230
            sx, sy = rx + 40, ry + ch - 38 - shh
            dv = A.ease(A.seg(t, .5 + i * .22, .7))
            g += _shkaf(sx, sy + shh, sw, shh, t, dv, False, i * .1)
            # чёрное платье внутри
            # платья разной длины и оттенка: шесть одинаковых читались как
            # повтор одной картинки (контактный лист 13.11)
            dl = (150, 168, 138, 160, 144, 172)[i]
            tn = ("#35303c", "#2c2833", "#3a3442", "#292530", "#372f3b", "#2f2a36")[i]
            g += _plate(f'b1d{i}', sx + sw * .5, sy + 34 + (168 - dl) * .3, dl, t, tn, "#121018",
                        3.0 * A.w(t, 2.4 + i * .3, i * .2) * dv, True, -1, i * .13)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, _sugrob(1030, 40, "#eaf2fb", 1.0))
    s += SL(Z_LETIT, _hlopya(t, 16, 19, .8))
    s += sneg_letit(t, 40, 6, .6, .8)
    s += vinetka(.44)
    return s


def vedro_u_poroga_nochyu(t):
    """Ночная прихожая, за приоткрытой дверью метёт снег, у порога полное
    эмалированное ведро. Живое: дужка ведра падает, снег метёт за дверью,
    лампочка в прихожей качается."""
    s = SL(Z_NEBO, _stena(t, 940, "#3f4f66", "#161d29"))
    r = random.Random(23)
    ulica = f'<rect x="1150" y="170" width="470" height="790" fill="#18243c"/>'
    for i in range(34):
        p0 = r.uniform(0, 1); v = r.uniform(.25, .7)
        px = 1150 + ((r.uniform(0, 470) + t * 180 * v) % 470)
        py = 170 + ((p0 + t * v * .45) % 1.0) * 790
        ulica += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(3,7):.1f}"'
                  f' fill="#e6f1fc" opacity="{.5+.4*abs(A.w(t,3.0,i*.1)):.2f}"/>')
    ulica += f'<rect x="1150" y="820" width="470" height="140" fill="#d6e4f2" opacity=".6"/>'
    s += SL(Z_DAL, ulica + teplo(1380, 560, 330, 420, .22)
            # вешалка с одеждой слева — второй план, не пустая стена
            + f'<rect x="150" y="430" width="420" height="22" rx="8" fill="url(#derev)" {o(5)}/>'
            + "".join(
                f'<path d="M{230+i*120},452 q-10,-16 0,-22 q10,6 0,22" fill="none"'
                f' stroke="#b7bdc6" stroke-width="5"/>'
                f'<path d="M{230+i*120-46},486 L{230+i*120},448 L{230+i*120+46},486"'
                f' fill="none" stroke="#9aa2ab" stroke-width="8" stroke-linejoin="round"/>'
                f'<path d="M{230+i*120-44},488 q44,-26 88,0 q-12,150 4,250 q-48,20 -96,0'
                f' q16,-100 4,-250 z" fill="{("#39425a","#4a3340","#333a33")[i]}"'
                f' opacity=".92" {o(5)}/>' for i in range(3)))
    kach = 3.4 * A.w(t, 3.8)
    lam = (f'<g transform="rotate({kach:.2f} 760 40)">'
           f'<line x1="760" y1="0" x2="760" y2="230" stroke="{K}" stroke-width="6"/>'
           f'<rect x="736" y="226" width="48" height="38" rx="8" fill="url(#zhel)" {o(4)}/>'
           f'<circle cx="760" cy="302" r="44" fill="{SVET}"'
           f' opacity="{.8+.2*abs(A.w(t,2.2)):.2f}" {o(4)}/>'
           + teplo(760, 320, 560, 470, .55) + '</g>')
    s += SL(Z_SRED, lam
            + f'<rect x="1120" y="140" width="70" height="850" rx="8" fill="url(#derev)" {o(7)}/>'
            + f'<g transform="translate(1150,0) scale(.42,1) translate(-1150,0)">'
            + dver(1150, 170, 470, 790, .0, "url(#derev)", True) + '</g>'
            + f'<rect x="1090" y="938" width="620" height="30" rx="8" fill="{DOSKA2}" {o(6)}/>')
    p = A.seg(t, .3, .7)
    pad = A.seg(t, 1.3, .55)
    duzh = A.out(p) * (1.0 - A.ease(pad))
    zv = max(0.0, 1.0 - abs(t - 1.9) * 5.0)
    s += SL(0, _vedro(820, 952, t, 1.15, "emal", True, duzh)
            + f'<ellipse cx="820" cy="960" rx="{160+44*zv:.0f}" ry="{22+9*zv:.0f}"'
              f' fill="#cfe6f2" opacity="{.25*zv:.2f}"/>'
            + teplo(820, 820, 340, 300, .3))
    s += SL(Z_PERED, f'<rect y="1010" width="{W}" height="82" fill="#0f1721" opacity=".88"/>'
            + f'<path d="M-40,1092 q140,-190 330,-240 l0,240 z" fill="#131b27" opacity=".9"/>')
    s += vinetka(.46)
    return s


def vedro_prevraschaetsya_v_paket(t):
    """Крупно: эмалированное ведро становится пластиковым, потом завязанным
    мусорным пакетом. Над ними — всё та же закрытая дверь. Живое: вид ведра
    меняется, узел пакета затягивается, за дверным глазком мигает свет."""
    s = SL(Z_NEBO, _stena(t, 1000, "#3b4a60", "#141b26", False))
    # закрытая дверь во весь верх кадра
    gl = .35 + .65 * abs(A.w(t, 1.35))
    dv = f'<rect x="250" y="-60" width="1420" height="700" rx="14" fill="url(#derev)" {o(9)}/>'
    dv += (f'<rect x="330" y="30" width="1260" height="250" rx="10" fill="none"'
           f' stroke="{DOSKA2}" stroke-width="12"/>')
    dv += (f'<rect x="330" y="320" width="1260" height="240" rx="10" fill="none"'
           f' stroke="{DOSKA2}" stroke-width="12"/>')
    dv += f'<circle cx="960" cy="300" r="40" fill="url(#zhel)" {o(6)}/>'
    dv += f'<circle cx="960" cy="300" r="22" fill="{SVET}" opacity="{gl:.2f}"/>'
    dv += teplo(960, 300, 260, 220, .34 * gl)
    dv += f'<circle cx="1520" cy="430" r="26" fill="url(#zhel)" {o(5)}/>'
    s += SL(Z_DAL, dv + f'<rect y="620" width="{W}" height="40" fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_SRED, polovicy(900) + ten(960, 936, 420, 34, .5))
    # три вида один в другом: эмаль → пластик → пакет
    a = 1.0 - A.ease(A.seg(t, .45, .55))
    b = A.ease(A.seg(t, .45, .55)) - A.ease(A.seg(t, 1.35, .55))
    c = A.ease(A.seg(t, 1.35, .55))
    uz = A.seg(t, 1.95, .75)
    s += SL(0, _vedro(960, 940, t, 1.5, "emal", True, .9, a)
            + _vedro(960, 940, t, 1.5, "plastik", True, .9, b)
            + _paket(960, 940, t, 1.5, uz, c)
            + teplo(960, 760, 420, 360, .3))
    s += SL(Z_PERED, f'<rect y="1016" width="{W}" height="76" fill="#0e1520" opacity=".88"/>')
    s += vinetka(.46)
    return s
