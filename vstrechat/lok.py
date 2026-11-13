# -*- coding: utf-8 -*-
"""ДЕКОРАЦИИ ролика «Как встречать год хозяйки года 2027» (185 планов).

Каждая — функция времени f(t) -> svg. Все нарисованы ЗАНОВО под этот текст
(R-0019): ни один кадр не взят у «13 ноября Спиридон», «14 ноября Кузьминки»,
«15 ноября Акиндин и Пигасий» и «16 ноября Анна Холодная».
Где в плане стоит окно вставки, главное живёт в ЛЕВОЙ полосе 0-830 (R-0007).
В каждой декорации минимум три живых элемента (R-0006).

Гамма праздника: синий вечер и снег, одно тёплое пятно в кадре — ёлка, окно,
свеча, циферблат. Красный и золото — акценты. Хозяйка года (красная коза) и
огненная лошадь живут в obrazy.py, общие кирпичики — в baza.py.

Собран sborka_lok.py из восьми файлов блоков, руками не правится.
"""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob

OKNO = (860, 300, 980, 551)          # неподвижный контейнер вставки


# ═══════════════ lok_b1.py ═══════════════

OKNO = (860, 300, 980, 551)


def b1_g(idn, c1, c2, vert=True):
    x2, y2 = ("0", "1") if vert else ("1", "0")
    return (f'<linearGradient id="{idn}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def b1_rad(idn, col, op=.55):
    return (f'<radialGradient id="{idn}" cx=".5" cy=".5" r=".5">'
            f'<stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')


def b1_stena(t, pol_y=900, c1="#4d5f78", c2="#1c2534", polosy=True):
    """Стена комнаты и дощатый пол. Синева — холод, тёплое пятно даёт огонь."""
    s = b1_g("b1st", c1, c2)
    s += f'<rect width="{W}" height="{H}" fill="url(#b1st)"/>'
    if polosy:
        for i in range(14):
            s += (f'<rect x="{i*W/13.0:.0f}" y="0" width="26" height="{pol_y:.0f}"'
                  f' fill="#ffffff" opacity=".04"/>')
    s += polovicy(pol_y)
    return s


def b1_okno_noch(x, y, w_, h_, t, moroz=.5, seed=7):
    """Окно, за которым идёт снег: живой дальний план для комнатных сцен."""
    r = random.Random(seed)
    vid = f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="#16203a"/>'
    for i in range(20):
        px = x + r.uniform(0, w_); p0 = r.uniform(0, 1)
        py = y + ((p0 + t * r.uniform(.07, .22)) % 1.0) * h_
        vid += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(2.0,4.4):.1f}"'
                f' fill="#dce9f7" opacity=".75"/>')
    return okno_izby(x, y, w_, h_, t, vid=vid, moroz=moroz)


def b1_hlopya(t, n=22, seed=12, sp=1.0):
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


def b1_sugrob(y, amp=40, col="url(#sneg)", op=1.0):
    return (f'<path d="M-40,{y+amp} q300,{-amp*2:.0f} 620,{-14} q300,{amp:.0f} 640,{-22}'
            f' q260,{-amp*1.6:.0f} 740,{-6} L1960,{H+40} L-40,{H+40} Z"'
            f' fill="{col}" opacity="{op:.2f}" {o(5)}/>')


def b1_krylco(x, base, w_, t, lenta=0.0, zerkalo=1):
    """Крыльцо избы: три ступени со снегом, столбы, перила и козырёк.
    `lenta` 0..1 — доля вспыхнувшей на перилах красной ленты."""
    sg = 1 if zerkalo >= 0 else -1
    s = b1_g("b1kry", "#b4854f", "#66401f")
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


def b1_stul(x, base, t, s_=1.0, dx=0.0, ph=0.0):
    """Венский стул: гнутая спинка, сиденье, четыре ножки."""
    s = b1_g("b1stu", "#b07b45", "#5c3819")
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


def b1_plate(idn, x, ytop, h_, t, c1="#f7efdc", c2="#c9b991", kach=0.0,
           kruzhevo=False, karman=0.0, ph=0.0, plechiki=True):
    """Платье на плечиках: крючок, плечики, лиф с талией и юбка колоколом.
    `kach` — угол качания, `karman` 0..1 — насколько отогнут кармашек."""
    sh = h_ / 520.0
    pl, ta, yu = 122 * sh, 76 * sh, 196 * sh          # плечо, талия, подол
    yt, yta, yh = ytop + 30 * sh, ytop + 215 * sh, ytop + h_ - 18 * sh
    s = b1_g(idn, c1, c2)
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


def b1_pidzhak(x, ytop, h_, t, karman_vyv=0.0, ph=0.0):
    """Пола пиджака с нагрудным карманом; `karman_vyv` 0..1 — вывернут."""
    sh = h_ / 420.0
    s = b1_g("b1pid", "#3a4150", "#171c26")
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


def b1_ochki(x, y, t, s_=1.0, ph=0.0):
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


def b1_ryumka(x, base, t, s_=1.0, ph=0.0):
    """Праздничная рюмка: стекло с бликом, блик дышит."""
    bl = .3 + .7 * abs(A.w(t, 2.6, ph))
    g = f'<g transform="translate({x:.1f},{base:.1f}) scale({s_:.3f})">'
    g += ten(0, 6, 26, 7, .4)
    g += f'<path d="M-24,-78 h48 q-4,46 -24,60 q-20,-14 -24,-60 z" fill="{STEKLO}" opacity=".55" {o(4)}/>'
    g += f'<path d="M0,-18 v14" fill="none" {o(5)}/><path d="M-20,0 h40" fill="none" {o(5)}/>'
    g += f'<path d="M-18,-70 q6,38 10,46" fill="none" stroke="#ffffff" stroke-width="7" opacity="{bl:.2f}"/>'
    g += '</g>'
    return g


def b1_tarelka(x, y, s_=1.0, kant=True):
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(2, 14, 74, 12, .4)
    g += f'<ellipse rx="76" ry="26" fill="url(#krem)" {o(5)}/>'
    g += f'<ellipse rx="48" ry="15" fill="#fbf4e4" {o(3)}/>'
    if kant:
        g += f'<ellipse rx="64" ry="21" fill="none" stroke="{ob.ALYJ}" stroke-width="5" opacity=".75"/>'
    g += f'<path d="M-52,-10 q22,-12 44,-6" fill="none" stroke="#ffffff" stroke-width="6" opacity=".6"/>'
    g += '</g>'
    return g


def b1_blyudo(x, y, t, s_=1.0, par_on=True):
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


def b1_moneta(x, y, s_=1.0, fase=0.0):
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


def b1_bant(x, y, s_=1.0, p=1.0, col=None):
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


def b1_karandash(x, y, ang=0.0, s_=1.0, col=None):
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


def b1_banka(x, base, t, s_=1.0, op=1.0, col="#cf9a4a", ph=0.0):
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


def b1_lozhka(x, y, t, s_=1.0, zvon=0.0):
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


def b1_vedro(x, base, t, s_=1.0, vid="emal", voda=True, duzhka=0.0, op=1.0):
    """Ведро: эмалированное или пластиковое. `duzhka` 0..1 — поднята дужка."""
    if op <= .02:
        return ""
    if vid == "emal":
        s = b1_g("b1ved", "#f4f7fa", "#9fb6c6")
        korp, kant = "url(#b1ved)", "#2f5d86"
    else:
        s = b1_g("b1vedp", "#6f8ea8", "#2d4055")
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


def b1_paket(x, base, t, s_=1.0, uzel=0.0, op=1.0):
    """Завязанный мусорный пакет: мятый бок, узел затягивается сам."""
    if op <= .02:
        return ""
    u = A.out(max(0.0, min(1.0, uzel)))
    s = b1_g("b1pak", "#5a6a74", "#222c33")
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


def b1_tuchka(x, y, t, s_=1.0, ph=0.0, szhatie=1.0):
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


def b1_listok(x, y, w_, h_, flip=0.0, col="#f6efdc", col2="#d6c9a8"):
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


def b1_shkaf(x, base, w_, h_, t, dverca=0.0, zerkalo=False, ph=0.0, nutro="#2a2f3a"):
    """Шкаф: корпус, нутро, дверца на петле слева (0 закрыта, 1 раскрыта)."""
    s = b1_g("b1shk", "#a2743f", "#58361a")
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


def ognennaya_hozyayka_u_krylca(t):
    """Зимняя ночь, изба с тёплыми окнами и крыльцом, на дорожке — хозяйка
    года, красная коза. Живое: дышит огненное свечение шерсти, коза поводит
    ухом и бубенчиком, крупные хлопья снега падают."""
    s = baza.nebo("noch", t)
    s += baza.oblaka(t, 170, 3, 7, .2, "#9db0c8", 5.0)
    s += ulica_dal(1130, 742, 760, t)
    s += SL(Z_DAL, b1_sugrob(772, 34, "#dbe6f2", .95))
    s += SL(Z_SRED, izba_snaruzhi(30, 846, 700, t)
            + b1_okno_noch(214, 560, 176, 148, t, .45, 3)
            + b1_krylco(470, 946, 330, t, A.ease(A.seg(t, 1.5, .6)))
            + b1_sugrob(912, 46))
    # хозяйка года на дорожке: свечение шерсти дышит
    puls = .78 + .22 * abs(A.w(t, 2.3))
    s += SL(0, b1_rad("b1zar", "#ff7a28", .72) + b1_rad("b1zar2", "#ffd08a", .6)
            + f'<ellipse cx="946" cy="808" rx="{420*puls:.0f}" ry="{350*puls:.0f}"'
              f' fill="url(#b1zar)" opacity="{.9*puls:.2f}"/>'
            + f'<ellipse cx="946" cy="820" rx="{250*puls:.0f}" ry="{210*puls:.0f}"'
              f' fill="url(#b1zar2)" opacity="{.85*puls:.2f}"/>'
            + teplo(946, 800, 300 * puls, 260 * puls, .7)
            + ob.koza(946, 952, t, .82, 0.0, True, .1)
            + iskra_let(t, 946, 880, 14, 4, 340, .5)
            + f'<ellipse cx="946" cy="962" rx="230" ry="42" fill="#ffb060"'
              f' opacity="{.18*puls:.2f}"/>')
    s += SL(Z_PERED, b1_sugrob(1012, 54, "#f2f7ff", 1.0)
            + f'<ellipse cx="946" cy="982" rx="190" ry="34" fill="#9fc0dd" opacity=".35"/>')
    s += ramka_pp("levo", "#0a0f1a", .72)
    s += SL(Z_LETIT, b1_hlopya(t, 24, 12, .9))
    s += sneg_letit(t, 46, 5, .7, .9)
    s += vinetka(.44)
    return s


def dva_stula_u_prazdnichnogo_stola(t):
    """Праздничный стол и два стула: на спинке одного чёрное платье, на другом
    пиджак с вывернутым пустым карманом. Живое: стулья отъезжают от стола,
    карман болтается, огоньки свечей качаются."""
    ot = A.ease(A.seg(t, .5, 2.1))
    s = SL(Z_NEBO, b1_stena(t, 940, "#4a5d78", "#1b2433"))
    s += SL(Z_DAL, b1_okno_noch(1470, 170, 340, 310, t, .4, 9)
            + ob.girlyanda(100, 150, 1860, 190, t, 14, 110)
            + ob.elka(210, 940, 460, t, True, True, 4))
    # стол: столешница, скатерть, приборы
    g = ten(960, 962, 560, 30, .5)
    g += f'<rect x="600" y="690" width="740" height="44" rx="12" fill="url(#derev)" {o(7)}/>'
    g += (f'<path d="M580,690 h780 v48 q-390,40 -780,0 z" fill="url(#rush)" {o(6)}/>')
    g += (f'<path d="M580,738 q390,40 780,0 l-26,186 q-364,30 -728,0 z" fill="url(#rush)" {o(6)}/>')
    g += (f'<path d="M592,754 q384,38 756,0" fill="none" stroke="{ob.ALYJ}"'
          f' stroke-width="8" opacity=".65"/>')
    g += (b1_tarelka(760, 700, .78) + b1_tarelka(1170, 700, .78) + b1_blyudo(960, 694, t, .8)
          + svecha(700, 578, t, .1, 1.0) + svecha(1230, 578, t, .55, 1.0)
          + ob.bokal(850, 700, t, .56, .2) + ob.bokal(1080, 700, t, .56, .7)
          + teplo(960, 630, 600, 360, .5))
    s += SL(Z_SRED, g)
    # левый стул: чёрное платье переброшено через спинку
    lx = 410 - ot * 200
    s += SL(0, b1_stul(410, 946, t, 1.25, -ot * 200)
            + b1_plate("b1chp", lx + 10, 686, 250, t, "#3b3442", "#141219",
                     2.4 * A.w(t, 3.1), True, -1, .2, False)
            + f'<path d="M{lx-130:.0f},692 q130,-34 260,0 q-130,26 -260,0 z"'
              f' fill="#2a2531" {o(5)}/>')
    # правый стул: пиджак с вывернутым карманом
    rx = 1500 + ot * 200
    s += SL(0, b1_stul(1500, 946, t, 1.25, ot * 200)
            + b1_pidzhak(rx, 650, 270, t, A.ease(A.seg(t, .9, 1.0)), .4)
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
    s = SL(Z_NEBO, b1_stena(t, 930, "#43566f", "#1a2230"))
    s += SL(Z_DAL, b1_okno_noch(130, 210, 280, 260, t, .5, 11)
            + lampa(1700, 380, t, .95, True) + teplo(1700, 500, 560, 440, .5)
            + polka(1430, 560, 380) + krynka(1500, 554, .7) + b1_ryumka(1620, 554, t, 1.0, .3)
            + ob.elka(240, 936, 300, t, True, False, 7)
            + ob.girlyanda(60, 120, 1880, 160, t, 13, 90))
    kach = 1.8 * A.w(t, 2.6)
    x0, y0, w_, h_ = 900, 150, 680, 680
    g = f'<g transform="rotate({kach:.2f} {x0} {y0-40})">'
    g += ten(x0 + 26, y0 + h_ + 46, w_ * .5, 28, .5)
    g += (f'<rect x="{x0-w_/2-20:.0f}" y="{y0-58:.0f}" width="{w_+40:.0f}" height="{h_+100:.0f}"'
          f' rx="16" fill="url(#derev)" {o(7)}/>')
    g += b1_g("b1bum", "#fbf5e4", "#cdbf9c")
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
        s += SL(0, b1_karandash(x0 - w_ / 2 + 90 + 150 * zp, y0 + h_ * .36 + 150 * zp,
                              10, 1.3, "#2f3944"))
    if .02 < ob_p < .995:
        a = -math.pi * .5 + 2 * math.pi * ob_p
        s += SL(0, b1_karandash(cx6 + 64 * math.cos(a), cy6 + 50 * math.sin(a), 16, 1.3, ob.ALYJ))
    s += SL(Z_PERED, f'<rect y="986" width="{W}" height="106" fill="#121a26" {o(6)}/>'
            + f'<rect y="986" width="{W}" height="16" fill="#2b3644"/>'
            + b1_mandarin_kuchka(t))
    s += vinetka(.42)
    return s


def b1_mandarin_kuchka(t):
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
    s += SL(Z_DAL, b1_sugrob(798, 32, "#dbe6f2", .95))
    s += SL(Z_SRED, izba_snaruzhi(1230, 900, 660, t)
            + b1_okno_noch(1406, 620, 166, 140, t, .45, 5)
            + b1_krylco(900, 1010, 440, t, 0.0)
            + b1_sugrob(968, 44))
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
    s += SL(Z_PERED, b1_sugrob(1042, 52, "#f2f7ff", 1.0))
    s += ramka_pp("pravo", "#0a0f1a", .62)
    s += SL(Z_LETIT, b1_hlopya(t, 20, 15, .8))
    s += sneg_letit(t, 42, 8, .65, .85)
    s += vinetka(.44)
    return s


def chasy_nad_prazdnichnym_stolom(t):
    """Комната, накрытый стол, над ним круглые часы без пяти двенадцать.
    Живое: стрелка вздрагивает, маятник качается, свечи горят."""
    s = SL(Z_NEBO, b1_stena(t, 940, "#44566f", "#19212f"))
    s += SL(Z_DAL, b1_okno_noch(140, 230, 300, 280, t, .45, 4)
            + ob.girlyanda(70, 150, 1850, 190, t, 13, 120)
            + ob.elka(1660, 940, 420, t, True, True, 6))
    # часы с маятником над столом
    cx, cy = 790, 250
    vzd = .004 * (1 if (t * 2) % 1 < .5 else 0)
    g = b1_g("b1kor", "#8f6134", "#4d2d14")
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
    tg += (b1_tarelka(560, 782, .8) + b1_tarelka(1360, 782, .8)
           + b1_blyudo(1130, 776, t, .9)
           + svecha(430, 650, t, .1, 1.1) + svecha(1500, 650, t, .6, 1.1)
           + ob.bokal(690, 782, t, .66, .2) + ob.bokal(1270, 782, t, .66, .7)
           + ob.mandarin(960, 766, .76, .4, t)
           + teplo(960, 760, 720, 380, .5))
    s += SL(0, tg)
    s += SL(Z_PERED, f'<rect y="1026" width="{W}" height="66" fill="#101823" opacity=".85"/>'
            + b1_stul(300, 1140, t, 1.3))
    s += vinetka(.42)
    return s


def babushka_razglazhivaet_skatert(t):
    """Бабушка со спины у стола: по белой скатерти сама бежит разглаживающая
    волна, тарелка встаёт на место, очки на шнурке качаются."""
    s = SL(Z_NEBO, b1_stena(t, 940, "#4b5d76", "#1d2735"))
    s += SL(Z_DAL, kvartira_veschi(1200, 940, 680, t, 11)
            + b1_okno_noch(120, 210, 270, 260, t, .4, 6)
            + ob.girlyanda(60, 120, 1880, 150, t, 12, 80))
    # стол с белой скатертью: не на весь кадр, подол короткий
    g = b1_g("b1ska", "#fdfaf0", "#cbd4de")
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
    s += SL(0, b1_tarelka(1150 - 160 * (1 - dv), 806 + 10 * (1 - dv), .84)
            + b1_tarelka(1400, 806, .84) + b1_tarelka(560, 806, .84)
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
            + b1_ochki(742, 790, t, 1.1, .3))
    s += SL(Z_PERED, b1_stul(1640, 1120, t, 1.3)
            + f'<rect y="1042" width="{W}" height="50" fill="#111a26" opacity=".8"/>')
    s += vinetka(.4)
    return s


def karman_naryad_i_blyudo(t):
    """Три крупные детали подряд: монета опускается в карман, красный бант
    сам завязывается на платье, горячее блюдо встаёт на стол."""
    s = SL(Z_NEBO, b1_stena(t, 1000, "#3e4f68", "#161e2b", False)
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
    g1 += b1_pidzhak(300, 330, 600, t, 0.0, .1)
    if mp < .99:
        g1 += teplo(404, 180 + 356 * mp, 170, 170, .5 * (1 - mp * .7))
        g1 += b1_moneta(404, 180 + 356 * mp, 1.5, t * 7.0)
    # 2. платье и красный бант, который завязывается сам
    g2 = b1_plate("b1nar", 960, 250, 620, t, "#f8f1df", "#cbbd98",
                1.6 * A.w(t, 3.4), False, -1, .4)
    g2 += b1_bant(960, 352, .92, A.seg(t, 1.7, 1.2))
    # 3. горячее блюдо встаёт на стол
    bp = A.out(A.seg(t, 3.0, 1.0))
    # блюдо встаёт НА СТОЛ, а не зависает: опора и тень под ним
    g3 = (f'<rect x="1380" y="946" width="440" height="30" rx="10"'
          f' fill="url(#derev)" {o(6)}/>'
          + ten(1600, 952, 180, 22, .55))
    g3 += b1_blyudo(1600, 932 - 230 * (1 - bp), t, 1.5)
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
    g = b1_g("b1len", "#6a7b96", "#2a3447")
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
               + b1_listok(lx, ly, 132, 244, fl, sez[0], sez[1]) + '</g>')
    s += SL(Z_SRED, lg)
    # монета катится, следом бант и блюдо, рядом шагает фигурка
    pr = A.ease(A.seg(t, .15, 2.2))
    mx = 430 + 1270 * pr
    sh = abs(math.sin(2 * math.pi * (t / .62)))
    s += SL(0, teplo(mx, 720, 300, 200, .5)
            + b1_moneta(mx, 700 - 22 * abs(math.sin(2 * math.pi * pr * 3)), 1.9, mx * .018)
            + b1_bant(mx - 200, 706, .78, 1.0)
            + b1_blyudo(mx - 370, 724, t, .66)
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
    s = SL(Z_NEBO, b1_stena(t, 950, "#46586f", "#1b2432"))
    s += SL(Z_DAL, b1_shkaf(1500, 950, 380, 680, t, .08, True, .2)
            + b1_okno_noch(130, 240, 260, 250, t, .45, 8)
            + ob.girlyanda(60, 110, 1880, 150, t, 12, 80)
            + polka(380, 620, 300) + krynka(450, 614, .66))
    kach = 4.2 * A.w(t, 3.0)
    fx, fy = 820, 60
    g = b1_g("b1fon", "#e2493a", "#8d1b1c")
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
    s += SL(0, b1_plate("b1sve", 820, 440, 560, t, "#f9f3e2", "#cdc0a0",
                      1.5 * A.w(t, 4.0), False, -1, .3)
            + b1_rad("b1kra", "#ff4a35", .55)
            + f'<ellipse cx="820" cy="{py:.0f}" rx="280" ry="130" fill="url(#b1kra)"'
              f' opacity=".7"/>'
            + f'<path d="M700,{py-28:.0f} q120,34 240,0 q-120,46 -240,0 z"'
              f' fill="{ob.ALYJ}" opacity=".26"/>')
    s += SL(Z_PERED, f'<rect y="1004" width="{W}" height="88" fill="#101925" opacity=".85"/>'
            + b1_mandarin_kuchka(t))
    s += vinetka(.42)
    return s


def babushka_shepchet_vnuchke(t):
    """Кухня: бабушка в профиль наклоняется к внучке и говорит ей на ухо,
    внучка серьёзно кивает, на подоконнике поблёскивают рюмки."""
    s = SL(Z_NEBO, b1_stena(t, 1000, "#4a6072", "#1b2630"))
    s += SL(Z_DAL, b1_okno_noch(1240, 200, 440, 350, t, .5, 13)
            + f'<rect x="1200" y="566" width="520" height="28" rx="8" fill="url(#derev)" {o(5)}/>'
            + "".join(b1_ryumka(1270 + i * 110, 592, t, 1.5, i * .27) for i in range(4))
            + dver(170, 250, 260, 680, .0, "url(#derev)", True)
            + ob.girlyanda(60, 120, 1180, 170, t, 9, 70))
    s += SL(Z_SRED, f'<rect x="120" y="856" width="1700" height="40" rx="12" fill="url(#derev)" {o(6)}/>'
            + f'<rect x="160" y="896" width="1620" height="190" rx="12" fill="{DOSKA2}" {o(5)}/>'
            + krynka(300, 850, 1.0) + karavay(1560, 854, .66, True)
            + b1_tarelka(1360, 852, .7)
            + lampa(880, 230, t, .95, True) + teplo(880, 430, 680, 500, .5))
    nak = 10.5 * A.ease(A.seg(t, .25, 1.0))
    s += SL(0, f'<g transform="rotate({nak:.2f} 700 866)">'
            + ob.figura(700, 866, 700, t, "#3c2b3c", "#f0c070", True, .2, True, 1.0, False)
            + '</g>'
            + b1_ochki(818, 616, t, 1.2, .4))
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
    s = SL(Z_NEBO, b1_stena(t, 1000, "#465874", "#1a2432", False)
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
    g += b1_pidzhak(960, 230, 660, t, vyv, .1)
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
    s = SL(Z_NEBO, b1_stena(t, 950, "#4a5f70", "#1a242e"))
    s += SL(Z_DAL, "".join(
        f'<rect x="{60+c*96:.0f}" y="{120+r_*96:.0f}" width="88" height="88" rx="8"'
        f' fill="#ffffff" opacity=".05"/>' for c in range(19) for r_ in range(9)))
    x0, y0, w_, h_ = 540, 150, 840, 760
    g = b1_g("b1kuh", "#9c7b52", "#4f3a21")
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
                g += b1_banka(x0 + 120 + j * 190, sy, t, .78, op,
                            ("#cf9a4a", "#b8323a", "#6f8c4a", "#d6a63f")[j], j * .2)
        else:
            g += b1_lozhka(x0 + 160, sy - 10, t, 1.0, A.seg(t, 3.3, .4))
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
    s = SL(Z_NEBO, b1_stena(t, 944, "#4b5a74", "#1c2432"))
    s += SL(Z_DAL, b1_okno_noch(1480, 250, 330, 300, t, .5, 17)
            + f'<rect x="60" y="690" width="620" height="40" rx="14" fill="url(#tkan)" {o(6)}/>'
            + f'<rect x="60" y="730" width="620" height="210" rx="12" fill="#43506b" {o(6)}/>'
            + f'<path d="M90,700 q150,-60 300,-6" fill="none" stroke="#f1e7cf" stroke-width="22"/>')
    s += SL(Z_SRED, b1_shkaf(830, 944, 520, 800, t, .0, True, .1)
            + lampa(340, 300, t, .8, True) + teplo(340, 470, 520, 400, .45))
    otg = .35 + .65 * (.5 + .5 * A.w(t, 2.6))
    # 13.11: платье стояло ровно на середине дверцы и читалось как бежевый
    # блок поверх шкафа — сдвинуто к краю створки и ужато по высоте
    s += SL(0, b1_plate("b1prz", 1176, 250, 520, t, "#faf4e3", "#cfc1a0",
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
    s = SL(Z_NEBO, b1_stena(t, 952, "#43536d", "#191f2c"))
    s += SL(Z_DAL, b1_okno_noch(130, 240, 260, 250, t, .5, 21)
            + lampa(1640, 300, t, .8, True) + teplo(1640, 470, 500, 400, .4))
    g = b1_shkaf(620, 952, 760, 820, t, .95, False, .0)
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
    s += SL(0, b1_plate("b1chrn", px, 250 - 10 * stuk, 620, t, "#3b3442", "#141219",
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
    s = SL(Z_NEBO, b1_stena(t, 958, "#46566e", "#1a2230"))
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
    s += SL(Z_SRED, b1_tuchka(kray + shir * .42, 430, t, 1.15, .0, szh)
            + b1_tuchka(kray + shir * .62, 620, t, .9, .4, szh * .9))
    # дверь закрывается
    s += SL(0, f'<g transform="translate({dx0},0) scale({stvor:.3f},1)'
            f' translate({-dx0},0)">'
            + dver(dx0, 150, dw, 810, .0, "url(#derev)", True, True) + '</g>')
    # коврик сдвигается
    k = A.ease(A.seg(t, 1.0, 1.4))
    sdv = 54 * k
    s += SL(0, b1_g("b1kov", "#8d4a3c", "#4a2119")
            + f'<g transform="rotate({-2.2*k:.2f} 1100 990)">'
              f'<rect x="{860-sdv:.0f}" y="952" width="520" height="86" rx="12"'
              f' fill="url(#b1kov)" {o(6)}/>'
              f'<rect x="{890-sdv:.0f}" y="974" width="460" height="42" rx="8" fill="none"'
              f' stroke="{ob.ZOLOTO}" stroke-width="6" opacity=".6"/></g>')
    # чёрный подол платья на переднем плане
    s += SL(Z_PERED, b1_g("b1pod2", "#241e2b", "#0e0b12")
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
            + b1_sugrob(960, 30, "#cfdcea", .9))
    x0, y0, cw, ch = 420, 180, 360, 380
    g = b1_g("b1dom", "#9aa3a8", "#636c74")
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
            g += b1_shkaf(sx, sy + shh, sw, shh, t, dv, False, i * .1)
            # чёрное платье внутри
            # платья разной длины и оттенка: шесть одинаковых читались как
            # повтор одной картинки (контактный лист 13.11)
            dl = (150, 168, 138, 160, 144, 172)[i]
            tn = ("#35303c", "#2c2833", "#3a3442", "#292530", "#372f3b", "#2f2a36")[i]
            g += b1_plate(f'b1d{i}', sx + sw * .5, sy + 34 + (168 - dl) * .3, dl, t, tn, "#121018",
                        3.0 * A.w(t, 2.4 + i * .3, i * .2) * dv, True, -1, i * .13)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, b1_sugrob(1030, 40, "#eaf2fb", 1.0))
    s += SL(Z_LETIT, b1_hlopya(t, 16, 19, .8))
    s += sneg_letit(t, 40, 6, .6, .8)
    s += vinetka(.44)
    return s


def vedro_u_poroga_nochyu(t):
    """Ночная прихожая, за приоткрытой дверью метёт снег, у порога полное
    эмалированное ведро. Живое: дужка ведра падает, снег метёт за дверью,
    лампочка в прихожей качается."""
    s = SL(Z_NEBO, b1_stena(t, 940, "#3f4f66", "#161d29"))
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
    s += SL(0, b1_vedro(820, 952, t, 1.15, "emal", True, duzh)
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
    s = SL(Z_NEBO, b1_stena(t, 1000, "#3b4a60", "#141b26", False))
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
    s += SL(0, b1_vedro(960, 940, t, 1.5, "emal", True, .9, a)
            + b1_vedro(960, 940, t, 1.5, "plastik", True, .9, b)
            + b1_paket(960, 940, t, 1.5, uz, c)
            + teplo(960, 760, 420, 360, .3))
    s += SL(Z_PERED, f'<rect y="1016" width="{W}" height="76" fill="#0e1520" opacity=".88"/>')
    s += vinetka(.46)
    return s


# ═══════════════ lok_b2.py ═══════════════

OKNO = (860, 300, 980, 551)


def b2_medal(cx, cy, r, vnutri="", pole="#1b2740", sv=0.0, obod="url(#zol)"):
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


def b2_zver(cx, cy, s_, i, t, col="#e2e9f4"):
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


def b2_ovca(x, base, t, s_=1.0, ph=0.0, vlevo=True, sher="#f2ece0"):
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


def b2_baran(x, base, t, s_=1.0, ph=0.0, vlevo=False):
    """Баран: то же руно темнее и крученый рог — третий силуэт знака 羊."""
    g = b2_ovca(x, base, t, s_, ph, vlevo, "#d9cdb4")
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


def b2_vorona(x, y, t, s_=1.0, ph=0.0):
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


def b2_fonar(cx, cy, sc, t, gor=1.0, ph=0.0):
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


def b2_stolb(x, base, h_, t, sv=0.0, sc=1.0):
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


def b2_flazhok(x, base, h_, t, ph=0.0, col=None, sgn=1):
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


def b2_koleso(cx, cy, R, zub, ang, t, col="url(#derev)"):
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


def b2_vorota(cx, base, h_, t, sc=1.0, ph=0.0, op=1.0):
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


def b2_gazeta(x, y, w_, h_, t, ph=0.0, podsvet=0.0, naklon=0.0):
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
              else b2_zver(mx, my, .62, i, t, "#2c2318"))
        g += b2_medal(mx, my, 58, vn, "#efe3c6", sv, "url(#med)")
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
    g += b2_gazeta(140, 330, 700, 700, t, .0, p1, -1.4)
    g += ob.koza(1350, 560 + 54 * (1 - vyh2), t, .52, 0.0, True, .55)
    g += b2_gazeta(1080, 330, 700, 700, t, .4, p2, 1.6)
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
    g += b2_flazhok(220, ly(220) + 36, 420, t, .0, ob.ALYJ, 1)
    g += b2_flazhok(1706, ly(1706) + 36, 420, t, .45, ob.ZOLOTO, -1)
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
            g += b2_fonar(fx, yy, .64 * sc, t, gor, i * .17 + k * .11)
    s += SL(Z_SRED, g)
    s += SL(Z_PERED, baza.ramka_pp("levo", "#090d16", .9)
            + b2_fonar(118, 236, 1.08, t, A.ease(A.seg(t, 1.9, .5)), .6))
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
            g += b2_medal(mx, my, 92, vn, "#241026", sv)
        else:
            g += b2_medal(mx, my, 80, b2_zver(mx, my, .84, i, t), "#1b2740", 0.0)
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
            g += b2_ovca(kx + 72, ky + 262, t, .50, .3, True)
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
                   + b2_ovca(xx + 44, 1022, t, .56, .3, True) + '</g>')
        else:
            p3 += (f'<g transform="translate({dx:.0f},0)" opacity="{pv:.2f}">'
                   + b2_baran(xx + 54, 1022, t, .58, .6, True) + '</g>')
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
        g += b2_zver(bx, yt, .52, i, t, "#edd9a8")
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
    g = b2_koleso(bc[0], bc[1], bc[2], 12, ab, t)
    g += b2_koleso(sc_[0], sc_[1], sc_[2], 5, as_, t, "url(#dosk)")
    mb = math.radians(ab - 14)
    mx = bc[0] + bc[2] * .72 * math.cos(mb)
    my = bc[1] + bc[2] * .72 * math.sin(mb)
    g += b2_medal(mx, my, 74, ob.koza_malaya(mx - 20, my + 32, t, .21, .1), "#2a1a14", .25 + .6 * p)
    ms = math.radians(as_ - 16)
    sx = sc_[0] + sc_[2] * .72 * math.cos(ms)
    sy = sc_[1] + sc_[2] * .72 * math.sin(ms)
    g += b2_medal(sx, sy, 58, baza.ogon(sx, sy + 28, t, .34, .3, 0), "#2a1a14", .25 + .6 * p)
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
    d += b2_stolb(1092, 724, 92, t, sv[2], .34)
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
    g += b2_stolb(700, 842, 212, t, sv[1], .72)
    s += SL(Z_SRED, g)
    pp = b2_stolb(368, 1046, 420, t, sv[0], 1.32)
    vp = ((t * .36) % 1.0)
    vx = 460 + (1020 - 460) * A.ease(vp)
    vy = 596 - 182 * math.sin(math.pi * vp)
    pp += b2_vorona(vx, vy, t, 2.3 - .7 * vp, .1)
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
    d += b2_vorota(1256, 676, 112, t, .5, .35, .95)
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
    g += b2_vorota(vx, vy, vh, t, 1.0, .0, 1.0)
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


# ═══════════════ lok_b3.py ═══════════════

OKNO = (860, 300, 980, 551)


ASFALT  = "#4f555c"


ASFALT2 = "#373d43"


TRAV67  = "#5d7a42"


TRAV68  = "#3f5730"


SHTUK   = "#e3d6b6"


SHTUK2  = "#bfae86"


BORDO   = "#6e1f26"


BORDO2  = "#43131a"


BUMAGA  = "#f0e4c3"


BUMAGA2 = "#cdbb8e"


SINKA   = "#2f4c70"


SEPIA   = "#b49c76"


SEPIA2 = "#6d5c45"


PLENKA  = "#2a2724"


SERIF   = 'font-family="DejaVu Serif"'


def b3_lampochki(x, y, w_, h_, t, n=24, col=SVET, r_=11, sp=.7):
    """Цепочка лампочек по периметру афиши: огонёк бежит по кругу."""
    s = ""
    per = 2.0 * (w_ + h_)
    for i in range(n):
        u = per * i / n
        if u < w_:
            px, py = x + u, y
        elif u < w_ + h_:
            px, py = x + w_, y + (u - w_)
        elif u < 2 * w_ + h_:
            px, py = x + w_ - (u - w_ - h_), y + h_
        else:
            px, py = x, y + h_ - (u - 2 * w_ - h_)
        gor = .26 + .74 * (.5 + .5 * math.sin(2 * math.pi * (t * sp - 2.2 * i / n)))
        s += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r_*2.6:.0f}" fill="{col}"'
              f' opacity="{gor*.18:.2f}"/>')
        s += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r_*(.62+.38*gor):.1f}" fill="{col}"'
              f' opacity="{.35+.65*gor:.2f}" stroke="{K}" stroke-width="3"/>')
    return s


def b3_stroka(x, y, shir, s_, kegl, col="#2a1d12"):
    """Строка названия на афише. Единственный текст, который блок разрешает:
    фильмы показываем БЕЗ кадров и лиц — только буквами."""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" {SERIF}'
            f' font-size="{kegl:.0f}" font-weight="bold" letter-spacing="2"'
            f' fill="{col}">{s_}</text>')


def b3_gory(x, y, w_, h_, seed=3, noch=False):
    """Рисунок афиши: горы и светило. Ни кадра из фильма, ни лица."""
    r = random.Random(seed)
    sx = x + w_ * (.70 if seed % 2 else .26)
    if noch:
        s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
             f' fill="#334058" opacity=".55"/>')
        s += (f'<circle cx="{sx:.0f}" cy="{y+h_*.30:.0f}" r="{h_*.20:.0f}" fill="{KREM}"/>'
              f'<circle cx="{sx+h_*.11:.0f}" cy="{y+h_*.23:.0f}" r="{h_*.19:.0f}" fill="#3b4761"/>')
        gory = ((.16, .86, "#3f4c66"), (.42, 1.0, "#2d3a50"), (.72, .74, "#1f2838"))
    else:
        s = (f'<circle cx="{sx:.0f}" cy="{y+h_*.34:.0f}" r="{h_*.20:.0f}"'
             f' fill="{ORA}" opacity=".85"/>')
        gory = ((.16, .86, "#6d7f8c"), (.42, 1.0, "#55697a"), (.72, .74, "#3f5466"))
    for i, (u, hh, col) in enumerate(gory):
        px = x + w_ * u
        ph_ = h_ * hh * .78
        s += (f'<path d="M{px-w_*.30:.0f},{y+h_:.0f} L{px:.0f},{y+h_-ph_:.0f}'
              f' L{px+w_*.30:.0f},{y+h_:.0f} Z" fill="{col}" {o(5)}/>')
        s += (f'<path d="M{px-w_*.055:.0f},{y+h_-ph_*.78:.0f} L{px:.0f},{y+h_-ph_:.0f}'
              f' L{px+w_*.055:.0f},{y+h_-ph_*.78:.0f} q{-w_*.04:.0f},{h_*.05:.0f}'
              f' {-w_*.085:.0f},0 q{-w_*.04:.0f},{-h_*.05:.0f} {-w_*.085:.0f},0 Z"'
              f' fill="{KREM}" opacity=".85"/>')
    return s


def b3_afisha(x, y, w_, h_, naz, t=0.0, kegl=54, otgib=0.0, seed=3, lampy=False,
            noch=False):
    """Рисованная киноафиша: рама, выгоревшая бумага, горы, название буквами.
    `otgib` 0..1 — отстающий уголок внизу справа."""
    s = ten(x + w_ / 2 + 14, y + h_ + 18, w_ * .48, 16, .45)
    s += (f'<rect x="{x-14:.0f}" y="{y-14:.0f}" width="{w_+28:.0f}" height="{h_+28:.0f}"'
          f' rx="8" fill="url(#derev)" {o(7)}/>')
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' fill="url(#list)" {o(5)}/>')
    stroki = [naz]
    if len(naz) > 13:
        m = naz.rfind(" ", 0, len(naz) // 2 + 4)
        if m > 0:
            stroki = [naz[:m], naz[m + 1:]]
    nl = len(stroki)
    kg = max(30, min(kegl, (w_ - 44) * 1.70 / max(1, max(len(u) for u in stroki)),
                     h_ * .30 / nl))
    tband = min(.66, .10 + kg * 1.20 * nl / h_)
    s += b3_gory(x + 10, y + h_ * tband, w_ - 20, h_ * (1 - tband) - 12, seed, noch)
    for i, u in enumerate(stroki):
        s += b3_stroka(x + w_ / 2, y + h_ * .06 + kg * .82 + i * kg * 1.18, w_, u.upper(), kg)
    pw = min(w_ * .70, kg * .60 * max(len(u) for u in stroki))
    s += (f'<path d="M{x+w_/2-pw/2:.0f},{y+h_*tband-10:.0f} h{pw:.0f}" {o(4, "#a4381f")}/>')
    if otgib > .01:
        a = 26 * otgib
        s += (f'<g transform="rotate({a:.1f} {x+w_:.0f} {y+h_:.0f})">'
              f'<path d="M{x+w_-110*otgib:.0f},{y+h_:.0f} L{x+w_:.0f},{y+h_:.0f}'
              f' L{x+w_:.0f},{y+h_-110*otgib:.0f} Z" fill="{BUMAGA2}" {o(4)}/></g>')
    s += (f'<path d="M{x+16:.0f},{y+h_*.06:.0f} l{w_*.36:.0f},{h_*.5:.0f}"'
          f' stroke="#ffffff" stroke-width="12" opacity=".16"/>')
    if lampy:
        s += b3_lampochki(x - 26, y - 26, w_ + 52, h_ + 52, t, 26)
    return s


def b3_golova(x, y, r_, t, col="#1d2029", kant="#f0c070", ph=0.0, tryas=0.0, plechi=1.0):
    """Затылок и плечи зрителя. Тряска от смеха — живой элемент зала."""
    dy = tryas * (2.6 * A.w(t, .33, ph) + 1.6 * A.w(t, .19, ph * 1.7))
    return (f'<g transform="translate({x:.0f},{y+dy:.1f})">'
            f'<path d="M{-r_*2.6*plechi:.0f},{r_*3.0:.0f} q{r_*2.6*plechi:.0f},{-r_*2.3:.0f}'
            f' {r_*5.2*plechi:.0f},0 Z" fill="{col}"/>'
            f'<circle cx="0" cy="0" r="{r_:.0f}" fill="{col}"/>'
            f'<circle cx="0" cy="0" r="{r_:.0f}" fill="none" stroke="#0d1119"'
            f' stroke-width="{max(2,r_*.10):.1f}" opacity=".8"/>'
            f'<path d="M{-r_*.52:.0f},{-r_*.78:.0f} a{r_:.0f},{r_:.0f} 0 0 1 {r_*1.04:.0f},0"'
            f' fill="none" stroke="{kant}" stroke-width="{max(2,r_*.17):.1f}" opacity=".65"/></g>')


def b3_katushka(x, y, r_, t, sp=1.0, col="#6a6f76", lenta=True):
    """Катушка киноплёнки: обод, три окна, плёнка намотана. Вращается."""
    a = (t * sp * 150.0) % 360
    s = f'<g transform="translate({x:.0f},{y:.0f})">'
    s += f'<circle r="{r_:.0f}" fill="url(#zhel)" {o(6)}/>'
    if lenta:
        s += f'<circle r="{r_*.78:.0f}" fill="{PLENKA}" {o(4)}/>'
        s += f'<circle r="{r_*.44:.0f}" fill="{col}" {o(4)}/>'
    s += f'<g transform="rotate({a:.1f})">'
    for i in range(3):
        aa = i * 120
        s += (f'<g transform="rotate({aa})"><ellipse cx="0" cy="{-r_*.60:.0f}"'
              f' rx="{r_*.20:.0f}" ry="{r_*.26:.0f}" fill="#1b1d20" opacity=".8"/></g>')
    s += (f'<line x1="{-r_*.9:.0f}" y1="0" x2="{r_*.9:.0f}" y2="0" stroke="#d7dde4"'
          f' stroke-width="4" opacity=".55"/>')
    s += '</g>'
    s += f'<circle r="{r_*.14:.0f}" fill="{CHUGUN}" {o(3)}/>'
    s += f'<circle cx="{-r_*.34:.0f}" cy="{-r_*.42:.0f}" r="{r_*.16:.0f}" fill="#ffffff" opacity=".2"/>'
    return s + '</g>'


def b3_kreslo(x, y, w_, h_, col=BORDO, col2=BORDO2):
    """Кресло зала фронтально: спинка валиком, подлокотники, тень под сиденьем."""
    return (ten(x + w_ / 2, y + h_ + 10, w_ * .52, 14, .45)
            + f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
              f' rx="{w_*.22:.0f}" fill="{col}" {o(6)}/>'
            + f'<rect x="{x+w_*.12:.0f}" y="{y+h_*.12:.0f}" width="{w_*.76:.0f}"'
              f' height="{h_*.6:.0f}" rx="{w_*.16:.0f}" fill="{col2}" opacity=".55"/>'
            + f'<rect x="{x-w_*.12:.0f}" y="{y+h_*.52:.0f}" width="{w_*.18:.0f}"'
              f' height="{h_*.5:.0f}" rx="10" fill="url(#derev)" {o(5)}/>'
            + f'<rect x="{x+w_*.94:.0f}" y="{y+h_*.52:.0f}" width="{w_*.18:.0f}"'
              f' height="{h_*.5:.0f}" rx="10" fill="url(#derev)" {o(5)}/>'
            + f'<path d="M{x+w_*.2:.0f},{y+h_*.1:.0f} q{w_*.3:.0f},{-h_*.06:.0f} {w_*.6:.0f},0"'
              f' stroke="#ffffff" stroke-width="7" opacity=".16" fill="none"/>')


def b3_svechka(x, y, h_, t, gorit=1.0, ph=0.0, w_=12):
    """Свечка на пироге: воск, фитиль, огонёк, который загорается в свой срок."""
    s = (f'<rect x="{x-w_/2:.1f}" y="{y-h_:.1f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="4" fill="{ob.ALYJ}" {o(3)}/>')
    s += (f'<rect x="{x-w_/2:.1f}" y="{y-h_*.60:.1f}" width="{w_:.0f}"'
          f' height="{h_*.26:.1f}" fill="#fbf3e4"/>')
    s += f'<path d="M{x:.1f},{y-h_:.1f} v-8" fill="none" {o(3)}/>'
    if gorit > .02:
        hh = (21 + 5 * A.w(t, .72, ph)) * gorit
        dx = 1.6 * A.w(t, 1.25, ph)
        s += teplo(x, y - h_ - hh * .5, 26 * gorit, 30 * gorit, .42 * gorit)
        s += (f'<path d="M{x+dx:.1f},{y-h_-8-hh:.1f} c7,{hh*.5:.1f} 5,{hh*.8:.1f} -1,{hh:.1f}'
              f' c-6,{-hh*.2:.1f} -7,{-hh*.5:.1f} 1,{-hh:.1f} Z" fill="{SVET}"'
              f' opacity="{min(1.0,gorit):.2f}"/>')
    return s


def b3_tochki_60(cx, cy, r_):
    """Точки по контуру цифр «60» — на них встают свечки пирога.

    Цифры стоят почти фронтально (сжатие .76), кольца РАЗНОЙ высоты и свечек
    мало: при плоской раскладке по ободу и частой расстановке ряды свечек
    сливаются и число читается частоколом (поймано на трёх осмотрах)."""
    p = []
    szh = .45

    def tochka(u, v):
        p.append((cx + u * r_, cy + v * r_ * szh))

    for i in range(7):                        # кольцо шестёрки — внизу и мельче
        a_ = 2 * math.pi * i / 7
        tochka(-.78 + .42 * math.cos(a_), .36 + .56 * math.sin(a_))
    for i in range(4):                        # хвост шестёрки вверх-вправо
        u = (i + 1) / 4.0
        tochka(-1.20 + .68 * u * u, -.22 - .74 * u)
    for i in range(12):                       # кольцо нуля — во всю высоту
        a_ = 2 * math.pi * i / 12
        tochka(.82 + .44 * math.cos(a_), .96 * math.sin(a_))
    return p


def b3_dom67(x, base, w_, t, seed=1, svet=True):
    """Частный дом летнего вечера: обшивка, шиферная крыша с трубой, окно со
    ставнями, палисадник. Снега на крыше нет — это июнь, а не ноябрь."""
    r = random.Random(seed)
    h_ = w_ * .74
    s = ten(x + w_ / 2, base + 14, w_ * .52, 20, .5)
    s += baza.doski(x, base - h_, w_, h_, max(34, int(w_ * .13)), True,
                    r.choice(("dosk", "derev")))
    kh_ = w_ * r.uniform(.19, .25)
    s += (f'<path d="M{x-w_*.10:.0f},{base-h_:.0f} L{x+w_/2:.0f},{base-h_-kh_:.0f}'
          f' L{x+w_*1.10:.0f},{base-h_:.0f} Z" fill="#4d535c" {o(7)}/>')
    for i in range(4):
        s += (f'<path d="M{x-w_*.10+w_*.07:.0f},{base-h_-kh_*(.16+i*.2):.0f}'
              f' L{x+w_*1.10-w_*.07:.0f},{base-h_-kh_*(.16+i*.2):.0f}" fill="none"'
              f' stroke="#5e656f" stroke-width="4" opacity=".45"/>')
    s += (f'<path d="M{x-w_*.10:.0f},{base-h_:.0f} L{x+w_/2:.0f},{base-h_-kh_:.0f}"'
          f' fill="none" stroke="#7d848e" stroke-width="7" opacity=".75"/>')
    tx = x + w_ * r.choice((.30, .66))
    s += (f'<rect x="{tx:.0f}" y="{base-h_-kh_*.92:.0f}" width="{w_*.10:.0f}"'
          f' height="{kh_*.62:.0f}" fill="url(#kamen)" {o(5)}/>'
          f'<rect x="{tx-w_*.015:.0f}" y="{base-h_-kh_*.96:.0f}" width="{w_*.13:.0f}"'
          f' height="{kh_*.10:.0f}" rx="4" fill="{KAMEN2}" {o(4)}/>')
    s += (f'<rect x="{x-w_*.12:.0f}" y="{base-h_-10:.0f}" width="{w_*1.24:.0f}" height="20"'
          f' rx="7" fill="{DOSKA2}" {o(5)}/>')
    ox, oy = x + w_ * .30, base - h_ * .80
    ow, oh = w_ * .28, w_ * .22
    s += baza.okno_izby(ox, oy, ow, oh, t, None, 0.0, svet, True)
    for sgn, sx in ((-1, ox - 16), (1, ox + ow + 16)):
        s += (f'<rect x="{sx-(ow*.22 if sgn<0 else 0):.0f}" y="{oy-14:.0f}"'
              f' width="{ow*.22:.0f}" height="{oh+28:.0f}" rx="5" fill="#2c4a52" {o(5)}/>')
        s += (f'<path d="M{sx-(ow*.16 if sgn<0 else -ow*.06):.0f},{oy+oh*.3:.0f}'
              f' h{ow*.12:.0f}" stroke="#4f727a" stroke-width="5"/>')
    s += (f'<rect x="{x+w_*.70:.0f}" y="{base-h_*.40:.0f}" width="{w_*.17:.0f}"'
          f' height="{h_*.40:.0f}" rx="6" fill="{DOSKA2}" {o(6)}/>')
    for i in range(3):
        bx = x + w_ * (.10 + i * .36)
        s += (f'<ellipse cx="{bx:.0f}" cy="{base-18:.0f}" rx="{w_*.12:.0f}"'
              f' ry="{w_*.10:.0f}" fill="{TRAV68}" opacity=".92" {o(4)}/>')
    return s


def b3_belyo(x, y, w_, h_, col, t, ph=0.0):
    """Бельё на верёвке: прищепки сверху, подол чуть дышит на вечернем воздухе."""
    k = 5 * A.w(t, 4.6, ph)
    return (f'<path d="M{x:.0f},{y:.0f} h{w_:.0f} q{6+k:.0f},{h_*.55:.0f} {k*.4:.0f},{h_:.0f}'
            f' h{-w_:.0f} q{-6-k:.0f},{-h_*.45:.0f} {-k*.4:.0f},{-h_:.0f} Z"'
            f' fill="{col}" opacity=".93" {o(4)}/>'
            f'<rect x="{x+4:.0f}" y="{y-14:.0f}" width="12" height="26" rx="4" fill="url(#derev)" {o(3)}/>'
            f'<rect x="{x+w_-16:.0f}" y="{y-14:.0f}" width="12" height="26" rx="4" fill="url(#derev)" {o(3)}/>')


def b3_kartochka_bw(x, y, w_, h_, vid, t, otkl=0.0, ph=0.0):
    """Чёрно-белая рисованная карточка в альбомных уголках. Чуть отходит
    от уголка — это её живой элемент."""
    a = 2.6 * otkl * (1 + .4 * A.w(t, 3.0, ph))
    s = f'<g transform="rotate({a:.2f} {x:.0f} {y+h_:.0f})">'
    s += ten(x + w_ / 2 + 8, y + h_ + 12, w_ * .46, 12, .5)
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="#efe8da" {o(4)}/>'
    s += (f'<rect x="{x+10:.0f}" y="{y+10:.0f}" width="{w_-20:.0f}" height="{h_-28:.0f}"'
          f' fill="{SEPIA}" opacity=".55"/>')
    ix, iy, iw, ih = x + 10, y + 10, w_ - 20, h_ - 28
    if vid == "dom":
        s += (f'<path d="M{ix+iw*.18:.0f},{iy+ih*.86:.0f} v{-ih*.4:.0f} h{iw*.5:.0f}'
              f' v{ih*.4:.0f} Z" fill="{SEPIA2}"/>'
              f'<path d="M{ix+iw*.12:.0f},{iy+ih*.46:.0f} L{ix+iw*.43:.0f},{iy+ih*.2:.0f}'
              f' L{ix+iw*.74:.0f},{iy+ih*.46:.0f} Z" fill="#4e4234"/>')
    elif vid == "para":
        s += ob.figura(ix + iw * .36, iy + ih * .9, ih * .72, t, "#4e4234", "#d9cdb4", False, ph)
        s += ob.figura(ix + iw * .64, iy + ih * .9, ih * .66, t, "#5d503f", "#d9cdb4", False, ph + .4)
    elif vid == "elka":
        s += ob.elka(ix + iw * .5, iy + ih * .92, ih * .8, t, False, True, 6, False)
    else:
        s += ob.koza_malaya(ix + iw * .34, iy + ih * .88, t, ih * .0013, ph)
    s += (f'<rect x="{x+10:.0f}" y="{y+10:.0f}" width="{w_-20:.0f}" height="{h_-28:.0f}"'
          f' fill="#cdc1a6" opacity=".52"/>')
    for sx, sy, d in ((x, y, "l34,0 l-34,34"), (x + w_, y, "l-34,0 l34,34"),
                      (x, y + h_, "l34,0 l-34,-34"), (x + w_, y + h_, "l-34,0 l34,-34")):
        s += f'<path d="M{sx:.0f},{sy:.0f} {d} Z" fill="#2d2721" opacity=".85"/>'
    return s + '</g>'


def dvor_shestdesyat_sedmogo(t):
    """Двор между пятиэтажками на закате: бельевые столбы, стол для домино,
    дети с мячом, радиола в открытом окне. Живое: мяч прыгает, костяшка
    домино стучит по столу, занавески в окне колышутся."""
    s = baza.nebo("zakat", t, False)
    s += baza.oblaka(t, 170, 5, 21, .42, "#f7ddba", 6.0)
    s += baza.panelka(-120, 700, 700, t, 5, True, 12)
    s += baza.panelka(1260, 700, 760, t, 5, True, 19)
    # дальний план: тополя и торец дальнего дома между корпусами
    d = f'<rect x="580" y="500" width="700" height="210" fill="#4a5262" opacity=".9" {o(5)}/>'
    for i in range(6):
        tx = 620 + i * 118
        d += (f'<ellipse cx="{tx:.0f}" cy="{640 - (i % 3) * 26:.0f}" rx="44"'
              f' ry="{104 + (i % 3) * 18:.0f}" fill="#33442f" opacity=".92" {o(4)}/>'
              f'<rect x="{tx-7:.0f}" y="{700 - (i % 3) * 26:.0f}" width="14" height="40" fill="#3a2a1c"/>')
    d += f'<rect y="700" width="{W}" height="36" fill="{TRAV68}" opacity=".9"/>'
    s += SL(Z_DAL, d)
    # ── средний план: двор
    m = f'<rect y="736" width="{W}" height="{H-736}" fill="{ASFALT}"/>'
    m += (f'<path d="M0,736 q480,22 960,8 q480,-16 960,10 L1920,860 L0,860 Z"'
          f' fill="{TRAV67}" opacity=".9"/>')
    for i in range(7):
        m += (f'<path d="M{-60+i*300:.0f},{880+i*22:.0f} q300,{18-i*4:.0f} 620,{-10:.0f}"'
              f' fill="none" stroke="{ASFALT2}" stroke-width="5" opacity=".45"/>')
    # бельевые столбы с верёвками
    for i, (bx, bh) in enumerate(((580, 250), (1030, 250))):
        m += ten(bx, 846, 44, 13, .5)
        m += (f'<rect x="{bx-13:.0f}" y="{846-bh:.0f}" width="26" height="{bh:.0f}"'
              f' rx="8" fill="url(#derev)" {o(6)}/>'
              f'<rect x="{bx-74:.0f}" y="{846-bh-16:.0f}" width="148" height="20" rx="8"'
              f' fill="url(#derev)" {o(5)}/>')
    for k, (y0, col) in enumerate(((618, "#eef1f3"), (660, "#dfe6ec"))):
        m += (f'<path d="M{516:.0f},{y0:.0f} Q815,{y0+46:.0f} 1094,{y0:.0f}" fill="none"'
              f' stroke="#cfd6dd" stroke-width="4"/>')
        for j in range(3):
            u = .22 + j * .28
            bx = 516 + 578 * u
            by = y0 + 46 * (4 * u * (1 - u)) * .92
            m += b3_belyo(bx, by, 86 - j * 8, 118 - k * 26,
                        ("#eef1f3", "#e7d9c2", "#cfd9e4", "#e9c7bd")[(j + k) % 4], t, j * .3 + k * .17)
    # стол для домино, два силуэта по сторонам, костяшка стучит
    m += baza.stol(560, 920, 300, 30)
    m += ob.figura(518, 1002, 236, t, "#242a33", "#f0c070", False, .2, True)
    m += ob.figura(902, 1002, 230, t, "#2a2420", "#f0c070", False, .7, True)
    r = random.Random(4)
    for i in range(7):
        dx = 576 + (i % 4) * 66 + (i // 4) * 30
        dy = 906 + (i // 4) * 16
        m += (f'<g transform="rotate({r.uniform(-14,14):.0f} {dx:.0f} {dy:.0f})">'
              f'<rect x="{dx-13:.0f}" y="{dy-22:.0f}" width="26" height="44" rx="5"'
              f' fill="#f3ecdc" {o(3)}/>'
              f'<line x1="{dx-11:.0f}" y1="{dy:.0f}" x2="{dx+11:.0f}" y2="{dy:.0f}" {o(2)}/>'
              f'<circle cx="{dx-4:.0f}" cy="{dy-11:.0f}" r="3" fill="{K}"/>'
              f'<circle cx="{dx+4:.0f}" cy="{dy+11:.0f}" r="3" fill="{K}"/></g>')
    stuk = max(0.0, math.sin(2 * math.pi * (t / .92))) ** 5
    m += (f'<g transform="translate(802,{900-44*stuk:.1f}) rotate({-16*stuk:.1f})">'
          f'<rect x="-14" y="-24" width="28" height="48" rx="6" fill="#fbf5e8" {o(4)}/>'
          f'<line x1="-12" y1="0" x2="12" y2="0" {o(3)}/>'
          f'<circle cx="-5" cy="-12" r="3.4" fill="{K}"/><circle cx="5" cy="-12" r="3.4" fill="{K}"/>'
          f'<circle cx="0" cy="13" r="3.4" fill="{K}"/></g>')
    m += (f'<ellipse cx="802" cy="916" rx="{26+16*stuk:.0f}" ry="7" fill="#000"'
          f' opacity="{.18+.2*stuk:.2f}"/>')
    # дети с мячом
    m += ob.figura(1216, 1000, 196, t, "#2b2733", "#f6cf8c", False, .1, False, 1.0, True)
    m += ob.figura(1452, 1004, 182, t, "#242d33", "#f6cf8c", False, .55)
    bu = abs(math.sin(math.pi * t / .64))
    by = 1012 - 250 * (bu ** .78)
    sq = 1.0 + .20 * (1 - bu) ** 2
    m += ten(1334, 1018, 46 * (1 + .35 * (1 - bu)), 13, .75 - .25 * bu)
    m += (f'<g transform="translate(1334,{by:.0f}) scale({sq:.2f},{2-sq:.2f})">'
          f'<circle r="38" fill="#e8e2d4" {o(6)}/>'
          f'<path d="M-38,-4 q38,22 76,0" fill="none" stroke="{ob.ALYJ}" stroke-width="11"/>'
          f'<path d="M-30,-22 q30,16 60,0" fill="none" stroke="{SINKA}" stroke-width="9"/>'
          f'<circle cx="-13" cy="-15" r="9" fill="#ffffff" opacity=".5"/></g>')
    s += SL(Z_SRED, m)
    # ── ближний угол дома с открытым окном: занавески и радиола
    p = f'<rect x="-40" y="150" width="420" height="{H-150}" fill="url(#beton)" {o(7)}/>'
    p += (f'<rect x="-40" y="150" width="420" height="{H-150}" fill="#1a2330" opacity=".22"/>')
    for i in range(4):
        p += (f'<line x1="-40" y1="{280+i*210:.0f}" x2="380" y2="{280+i*210:.0f}"'
              f' stroke="{BETON2}" stroke-width="5" opacity=".55"/>')
    ox, oy, ow, oh = 72, 420, 256, 240
    p += baza.okno_izby(ox, oy, ow, oh, t, None, 0.0, False, False)
    p += f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}" fill="#26303c" opacity=".88"/>'
    p += teplo(ox + ow * .62, oy + oh * .72, 150, 120, .75)
    p += (f'<rect x="{ox-6:.0f}" y="{oy-4:.0f}" width="{ow+12:.0f}" height="14" rx="6"'
          f' fill="{DOSKA2}" {o(4)}/>')
    p += baza.zanaveska(ox + 8, oy + 8, oh - 16, 68, "#ddd0b4", t, 1)
    p += baza.zanaveska(ox + ow - 8, oy + 8, oh - 16, 68, "#ddd0b4", t, -1)
    rx, ry = ox + ow * .50, oy + oh * .92
    p += (f'{ten(rx+8, ry+10, 100, 14, .45)}'
          f'<rect x="{rx-104:.0f}" y="{ry-104:.0f}" width="208" height="112" rx="12"'
          f' fill="url(#derev)" {o(6)}/>'
          f'<rect x="{rx-86:.0f}" y="{ry-88:.0f}" width="112" height="46" rx="8"'
          f' fill="{SVET}" opacity="{.66+.28*abs(A.w(t,2.6)):.2f}" {o(4)}/>')
    for i in range(5):
        p += (f'<line x1="{rx-78+i*22:.0f}" y1="{ry-86:.0f}" x2="{rx-78+i*22:.0f}"'
              f' y2="{ry-50:.0f}" stroke="#8c6b32" stroke-width="3" opacity=".7"/>')
    p += (f'<line x1="{rx-54:.0f}" y1="{ry-90:.0f}" x2="{rx-54:.0f}" y2="{ry-40:.0f}"'
          f' stroke="{KRAS}" stroke-width="5"/>'
          f'<circle cx="{rx+62:.0f}" cy="{ry-62:.0f}" r="22" fill="url(#zhel)" {o(5)}/>'
          f'<circle cx="{rx+62:.0f}" cy="{ry-62:.0f}" r="7" fill="{SVET}"/>'
          f'<rect x="{rx-86:.0f}" y="{ry-34:.0f}" width="170" height="16" rx="7"'
          f' fill="{DOSKA2}" opacity=".8"/>')
    p += teplo(rx, ry - 70, 210, 170, .7)
    p += (f'<rect x="{ox-14:.0f}" y="{oy+oh:.0f}" width="{ow+28:.0f}" height="22" rx="6"'
          f' fill="url(#beton)" {o(5)}/>')
    p += (f'<path d="M1790,1080 q-30,-220 60,-330 q90,120 70,330 Z" fill="{TRAV68}" {o(6)}/>'
          f'<path d="M1690,1080 q-18,-150 48,-230 q66,86 54,230 Z" fill="#35492a" {o(5)}/>')
    s += SL(Z_PERED, p)
    s += baza.vinetka(.40)
    return s


def kinoteatr_s_afishey(t):
    """Фасад кинотеатра с колоннами, над входом рисованная афиша (только
    название буквами и горы). Живое: лампочки вокруг афиши бегут, двери
    открываются, голуби ходят по карнизу. Окно вставки занимает 860-1840."""
    s = baza.nebo("den", t, False)
    s += baza.oblaka(t, 150, 5, 15, .5, "#eef3f8", 7.0)
    d = ""
    for i in range(7):
        bx = 760 + i * 190
        bh = 190 + (i % 3) * 70
        d += (f'<rect x="{bx:.0f}" y="{790-bh:.0f}" width="168" height="{bh:.0f}"'
              f' fill="#6a7788" opacity=".8" {o(4)}/>')
        for j in range(3):
            d += (f'<rect x="{bx+18+j*48:.0f}" y="{810-bh:.0f}" width="30" height="40" rx="4"'
                  f' fill="{SVET}" opacity="{.2+.25*abs(A.w(t,8+i,j*.3)):.2f}"/>')
    for i in range(9):
        d += (f'<ellipse cx="{60+i*230:.0f}" cy="{700+(i%2)*26:.0f}" rx="86" ry="110"'
              f' fill="#3c5235" opacity=".8"/>'
              f'<rect x="{52+i*230:.0f}" y="{790+(i%2)*26:.0f}" width="18" height="46" fill="#3a2a1c"/>')
    d += f'<rect y="836" width="{W}" height="36" fill="#7b8794" opacity=".75"/>'
    s += SL(Z_DAL, d)
    # ── фасад
    m = ten(420, 960, 460, 26, .5)
    m += (f'<rect x="-40" y="96" width="880" height="800" fill="url(#krem)" {o(8)}/>')
    m += (f'<rect x="-40" y="96" width="880" height="800" fill="{SHTUK2}" opacity=".30"/>')
    m += (f'<path d="M-60,120 L400,34 L860,120 Z" fill="{SHTUK}" {o(8)}/>'
          f'<path d="M-60,120 L400,34 L860,120 Z" fill="#8f8160" opacity=".22"/>')
    m += (f'<rect x="-50" y="118" width="900" height="34" rx="8" fill="{SHTUK2}" {o(6)}/>')
    # афиша над входом
    m += b3_afisha(84, 146, 640, 228, "Кавказская пленница", t, 54, 0.0, 5, True)
    # карниз с голубями
    m += (f'<rect x="-40" y="420" width="880" height="32" rx="8" fill="{SHTUK2}" {o(6)}/>'
          f'<rect x="-40" y="420" width="880" height="10" fill="#ffffff" opacity=".18"/>')
    for i, (gx, ph) in enumerate(((150, .0), (438, .4), (712, .75))):
        m += baza.ptica(gx, 416, t, .58, "#c3ccd6", ph, "#7d8894")
    # колонны
    for i, cx in enumerate((22, 196, 592, 766)):
        m += ten(cx + 38, 902, 56, 14, .45)
        m += (f'<rect x="{cx:.0f}" y="{444:.0f}" width="76" height="430" rx="10"'
              f' fill="url(#krem)" {o(6)}/>')
        for j in range(5):
            m += (f'<line x1="{cx+14+j*12:.0f}" y1="462" x2="{cx+14+j*12:.0f}" y2="862"'
                  f' stroke="{SHTUK2}" stroke-width="5" opacity=".75"/>')
        m += (f'<rect x="{cx-12:.0f}" y="{424:.0f}" width="100" height="26" rx="6" fill="{SHTUK}" {o(5)}/>'
              f'<rect x="{cx-12:.0f}" y="{868:.0f}" width="100" height="26" rx="6" fill="{SHTUK}" {o(5)}/>')
    # вход: тёмный портал и две створки, которые открываются
    m += f'<rect x="288" y="500" width="266" height="378" rx="10" fill="#1b1f27" {o(7)}/>'
    m += teplo(421, 700, 170, 200, .5)
    otk = .18 + .82 * (.5 + .5 * math.sin(2 * math.pi * (t / 3.4)))
    for sgn, bx in ((1, 288), (-1, 554)):
        m += (f'<g transform="translate({bx:.0f},500) scale({sgn*(1-otk*.72):.3f},1)">'
              f'<rect x="0" y="0" width="133" height="378" fill="url(#derev)" {o(6)}/>'
              f'<rect x="18" y="26" width="97" height="150" rx="6" fill="url(#stekl)" opacity=".7" {o(4)}/>'
              f'<circle cx="112" cy="220" r="9" fill="url(#zhel)" {o(3)}/></g>')
    # площадь и ступени
    m += f'<rect y="896" width="{W}" height="{H-896}" fill="#6e6f6c"/>'
    m += (f'<path d="M-20,916 q480,-22 960,-8 q480,14 980,16 L1940,1080 L-20,1080 Z"'
          f' fill="#7b7c78" opacity=".8"/>')
    for i in range(6):
        m += (f'<path d="M{-40+i*340:.0f},{990+i*16:.0f} q200,14 420,-8" fill="none"'
              f' stroke="#5f605d" stroke-width="5" opacity=".4"/>')
    for i in range(3):
        m += (f'<rect x="{196-i*34:.0f}" y="{878+i*22:.0f}" width="{452+i*68:.0f}" height="24"'
              f' rx="5" fill="{SHTUK2}" {o(5)}/>')
    s += SL(Z_SRED, m)
    # ── народ у входа
    p = ""
    for i, (fx, hh, kr, pl, ph) in enumerate(((118, 272, False, True, .1),
                                              (236, 286, True, False, .5),
                                              (640, 278, False, False, .8),
                                              (760, 292, False, True, .3))):
        p += ob.figura(fx, 1000, hh, t, "#272231", "#f3d2a0", pl, ph, False, 1.0, kr)
    p += baza.ramka_pp("levo", "#141008", .34)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.42)
    return s


def polnyy_zritelnyy_zal(t):
    """Зрительный зал со спины: все места заняты, над головами луч проектора,
    над залом наливается счётчик, над экраном встаёт пьедестал первого места.
    Живое: плечи трясутся от смеха, пылинки в луче, счётчик бежит."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#0e1118"/>'
           + f'<rect width="{W}" height="{H}" fill="#1a2030" opacity=".6"/>')
    # ── экран и занавес
    d = ""
    mig = .78 + .22 * (.5 + .5 * math.sin(2 * math.pi * (t * .9)) * math.sin(2 * math.pi * (t * .37)))
    d += f'<rect x="300" y="150" width="1320" height="470" rx="8" fill="#2a2b31" {o(8)}/>'
    d += (f'<rect x="336" y="182" width="1248" height="406" fill="#d2dbe6"'
          f' opacity="{.82*mig:.2f}"/>')
    d += (f'<rect x="336" y="182" width="1248" height="406" fill="{SVET}" opacity="{.26*mig:.2f}"/>')
    d += (f'<ellipse cx="960" cy="385" rx="560" ry="200" fill="#ffffff" opacity="{.22*mig:.2f}"/>')
    d += (f'<rect x="336" y="500" width="1248" height="88" fill="#6b7686" opacity=".30"/>')
    d += teplo(960, 390, 760, 330, .4 * mig)
    for i, bx in enumerate((150, 1620)):
        d += (f'<path d="M{bx:.0f},120 q60,260 0,540 l{-150 if i else 150:.0f},0'
              f' q-50,-280 0,-540 Z" fill="{BORDO}" {o(6)}/>')
        for j in range(5):
            d += (f'<path d="M{bx+(j*26-60 if i==0 else -j*26+60):.0f},130'
                  f' q{40 if i==0 else -40:.0f},260 0,520" fill="none" stroke="{BORDO2}"'
                  f' stroke-width="9" opacity=".7"/>')
    # пьедестал первого места встаёт над экраном
    vst = A.out(A.seg(t, 1.5, 1.1))
    if vst > .01:
        py = 232 - 136 * vst
        d += (f'<g opacity="{vst:.2f}"><g transform="translate(960,{py:.0f})">'
              f'{ten(0, 112, 150, 18, .5)}'
              f'<rect x="-168" y="54" width="110" height="60" rx="6" fill="url(#med)" {o(5)}/>'
              f'<rect x="58" y="76" width="110" height="38" rx="6" fill="url(#med)" {o(5)}/>'
              f'<rect x="-58" y="-6" width="116" height="120" rx="8" fill="url(#zol)" {o(6)}/>'
              f'<path d="M-44,-6 h88" stroke="#fff6cf" stroke-width="7" opacity=".55"/>'
              f'</g></g>')
        d += teplo(960, 170, 300, 180, .35 * vst)
    s += SL(Z_DAL, d)
    # ── счётчик над залом
    f_ = ""
    cx0, cw = 300, 1320
    nap = A.ease(min(1.0, t / 3.0))
    f_ += (f'<rect x="{cx0:.0f}" y="48" width="{cw:.0f}" height="46" rx="23"'
           f' fill="#1d222c" {o(5)}/>')
    f_ += (f'<rect x="{cx0+6:.0f}" y="54" width="{(cw-12)*nap:.0f}" height="34" rx="17"'
           f' fill="url(#zol)"/>')
    for i in range(22):
        u = i / 21.0
        gor = .25 + .75 * (1.0 if u <= nap else .0) * (.6 + .4 * abs(A.w(t, .6, i * .12)))
        f_ += (f'<rect x="{cx0+16+u*(cw-44):.0f}" y="{62:.0f}" width="6" height="18" rx="3"'
               f' fill="{SVET if u <= nap else "#555c68"}" opacity="{gor:.2f}"/>')
    f_ += (f'<circle cx="{cx0+6+(cw-12)*nap:.0f}" cy="71" r="18" fill="{SVET}"'
           f' opacity="{.55+.45*abs(A.w(t,.9)):.2f}" {o(4)}/>')
    s += SL(Z_SRED, f_)
    # ── луч проектора над головами
    b = ""
    b += (f'<path d="M2010,1150 L600,196 L1420,196 Z" fill="#cfe4ff" opacity=".16"/>'
          f'<path d="M2010,1150 L760,210 L1300,210 Z" fill="#eaf4ff" opacity=".16"/>'
          f'<path d="M2010,1150 L900,226 L1160,226 Z" fill="#ffffff" opacity=".13"/>')
    r = random.Random(17)
    for i in range(44):
        u = r.uniform(.04, 1.0)
        px = 2010 - u * (2010 - r.uniform(640, 1380))
        py = 1150 - u * (1150 - 200)
        b += (f'<circle cx="{px+22*A.w(t,6+i*.3,i*.11):.0f}" cy="{py+((t*9+i*17)%40)-20:.0f}"'
              f' r="{r.uniform(1.8,4.2):.1f}" fill="#fff6dd" opacity="{r.uniform(.3,.85):.2f}"/>')
    s += SL(Z_SRED, b)
    # ── ряды голов: дальние мелкие, ближние крупные
    z = ""
    for row, (yy, rr, n, col) in enumerate(((654, 26, 13, "#4b5478"),
                                            (726, 33, 11, "#404868"),
                                            (814, 41, 9, "#353c5a"))):
        rnd = random.Random(30 + row)
        for i in range(n):
            x = 120 + (W - 240) * (i + .5) / n + rnd.uniform(-16, 16)
            z += b3_golova(x, yy, rr, t, col, "#8fb4d8", i * .23 + row * .4, .9, 1.05)
    s += SL(Z_SRED, z)
    p = ""
    for row, (yy, rr, n, col) in enumerate(((926, 52, 7, "#2b3250"),
                                            (1068, 68, 6, "#222841"))):
        rnd = random.Random(60 + row)
        for i in range(n):
            x = 90 + (W - 180) * (i + .5) / n + rnd.uniform(-22, 22)
            p += b3_golova(x, yy, rr, t, col, "#9ec2e6", i * .31 + row * .6, 1.25, 1.1)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.5)
    return s


def dve_afishi_na_zabore(t):
    """Дощатый забор с двумя свежими афишами: только названия крупными
    буквами. Живое: кисть разглаживает вторую афишу, уголок первой
    отгибается, кот идёт по верхней планке забора."""
    s = baza.nebo("den", t, False)
    s += baza.oblaka(t, 196, 5, 31, .46, "#f1f5f9", 6.0)
    d = ""
    for i in range(5):
        bx = -60 + i * 430
        d += (f'<rect x="{bx:.0f}" y="300" width="300" height="180" fill="#5a6475" opacity=".75"/>'
              f'<path d="M{bx-24:.0f},300 L{bx+150:.0f},214 L{bx+324:.0f},300 Z"'
              f' fill="#49536a" opacity=".8"/>')
    for i in range(7):
        d += (f'<ellipse cx="{40+i*300:.0f}" cy="{360+(i%3)*22:.0f}" rx="96" ry="128"'
              f' fill="#3b5333" opacity=".8"/>')
    s += SL(Z_DAL, d)
    # ── забор
    m = ten(960, 1006, 900, 26, .45)
    m += baza.doski(-30, 400, 1990, 580, 78, True, "dosk")
    m += (f'<rect x="-30" y="368" width="1990" height="40" rx="8" fill="url(#derev)" {o(6)}/>')
    for yy in (560, 848):
        m += (f'<rect x="-30" y="{yy:.0f}" width="1990" height="30" fill="{DOSKA2}"'
              f' opacity=".8" {o(4)}/>')
    for bx in (120, 700, 1300, 1820):
        m += (f'<rect x="{bx-22:.0f}" y="352" width="44" height="640" rx="8"'
              f' fill="{DOSKA2}" {o(6)}/>')
    m += f'<rect y="968" width="{W}" height="24" fill="#4b4237" opacity=".8"/>'
    # афиша первая — с отгибающимся уголком
    otg = .35 + .65 * (.5 + .5 * math.sin(2 * math.pi * (t / 2.3)))
    m += b3_afisha(190, 470, 500, 330, "Свадьба в Малиновке", t, 60, otg, 7)
    # афиша вторая — её разглаживает кисть
    m += b3_afisha(1020, 456, 450, 348, "Вий", t, 128, 0.0, 12, False, True)
    # мокрый блик свежего клея под кистью
    ku = .5 + .5 * math.sin(2 * math.pi * (t / 1.9))
    kx = 1060 + 380 * ku
    ky = 640 + 110 * (.5 + .5 * math.sin(2 * math.pi * (t / 3.8)))
    m += (f'<ellipse cx="{kx:.0f}" cy="{ky+40:.0f}" rx="96" ry="54" fill="#ffffff"'
          f' opacity=".16"/>')
    m += (f'<g transform="translate({kx:.0f},{ky:.0f}) rotate({-24+16*ku:.1f})">'
          f'{ten(10, 36, 46, 11, .4)}'
          f'<rect x="-26" y="-6" width="52" height="56" rx="7" fill="#c9a86a" {o(5)}/>'
          f'<path d="M-30,46 h60 l-8,54 h-44 Z" fill="#8b7a5f" {o(5)}/>'
          f'<rect x="-15" y="-150" width="30" height="150" rx="10" fill="url(#derev)" {o(5)}/>'
          f'<path d="M-24,92 q24,18 48,0" fill="none" stroke="#e8eef4" stroke-width="7" opacity=".7"/></g>')
    # кот идёт по верхней планке
    kx2 = -40 + ((t * 78) % 2060)
    m += baza.kot(kx2, 372, t, .56, "#3a342f")
    s += SL(Z_SRED, m)
    # ── трава и лопухи переднего плана
    p = (f'<path d="M-20,1080 q180,-120 400,-96 q240,26 480,-40 q300,-80 560,-16'
         f' q300,74 520,-30 L1940,1080 Z" fill="{TRAV68}" {o(6)}/>')
    r = random.Random(23)
    for i in range(14):
        lx = r.uniform(-20, W + 20)
        ly = r.uniform(980, 1072)
        p += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{r.uniform(44,86):.0f}"'
              f' ry="{r.uniform(26,46):.0f}" fill="{TRAV67}" opacity=".85" {o(4)}/>')
    p += baza.ramka_pp("pravo", "#15190f", .30)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.4)
    return s


def ryad_kresel_smeh_i_strah(t):
    """Один ряд кресел лицом к зрителю, свет экрана на силуэтах. Слева
    взрослые хохочут и раскачиваются, справа трое детей закрылись
    программками, у одного программка отходит — он подглядывает в щель.
    Живое: взрослые хохочут, щель программки раздвигается, свет мигает."""
    mig = .70 + .30 * (.5 + .5 * math.sin(2 * math.pi * (t * 1.15))
                       * math.sin(2 * math.pi * (t * .43 + .2)))
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#0c0f16"/>')
    d = (f'<rect y="0" width="{W}" height="560" fill="#161c28"/>')
    for i in range(9):
        d += (f'<rect x="{-40+i*230:.0f}" y="0" width="140" height="560" rx="12"'
              f' fill="{BORDO2}" opacity=".5"/>')
    d += teplo(960, 240, 1100, 420, .26 * mig)
    for i, bx in enumerate((250, 700, 1200, 1660)):
        gor = .55 + .45 * abs(A.w(t, 5.4 + i, i * .2))
        d += (f'<path d="M{bx-44:.0f},300 q44,-54 88,0 q-44,34 -88,0 Z" fill="url(#zol)" {o(5)}/>'
              f'<rect x="{bx-9:.0f}" y="300" width="18" height="46" rx="6" fill="{MED}" {o(4)}/>')
        d += teplo(bx, 290, 150, 130, .5 * gor)
    for i, dx in enumerate((160, 560, 960, 1360, 1760)):
        gor = .5 + .5 * abs(A.w(t, 6.2 + i, i * .17))
        d += (f'<path d="M{dx:.0f},0 v54" stroke="{CHUGUN}" stroke-width="7"/>'
              f'<ellipse cx="{dx:.0f}" cy="76" rx="56" ry="26" fill="{KREM}"'
              f' opacity="{.45+.35*gor:.2f}" {o(5)}/>')
        d += teplo(dx, 86, 140, 110, .34 * gor)
    d += (f'<rect x="1700" y="150" width="190" height="400" rx="10" fill="#101620" {o(6)}/>'
          f'<rect x="1716" y="166" width="158" height="368" rx="8" fill="{BORDO2}" {o(4)}/>'
          f'<rect x="60" y="170" width="170" height="380" rx="10" fill="#101620" {o(6)}/>'
          f'<rect x="74" y="186" width="142" height="348" rx="8" fill="{BORDO2}" {o(4)}/>')
    d += (f'<rect y="540" width="{W}" height="40" fill="#1d2430" {o(4)}/>')
    s += SL(Z_DAL, d)
    # ── зрители сидят В креслах: сперва фигуры, кресла ложатся поверх
    m = ""
    # взрослые слева: корпус раскачивается от хохота
    for i, (fx, hh, kr, pl, ph) in enumerate(((160, 364, False, False, .0),
                                              (398, 348, False, True, .42),
                                              (636, 370, True, False, .8),
                                              (874, 354, False, False, .25))):  # noqa
        kach = 7.5 * A.w(t, .66, ph) + 3.2 * A.w(t, .33, ph * 1.4)
        col = "#2c3348" if i % 2 == 0 else "#434a66"
        m += (f'<g transform="rotate({kach:.2f} {fx:.0f} 782)">'
              + ob.figura(fx, 782, hh, t, col, "#dceeff", pl, ph, False, 1.0, kr)
              + f'</g>')
    # дети справа: вместо рук работает предмет — программка кинотеатра
    for i, (fx, hh, ph, otk) in enumerate(((1174, 300, .1, .0), (1412, 312, .5, .0),
                                           (1650, 294, .8, 1.0))):
        m += ob.figura(fx, 782, hh, t, "#4a5476", "#dceeff", False, ph)
        gy = 782 - hh * .74
        if otk < .5:
            kch = 2.4 * A.w(t, 2.4, ph)
            m += (f'<g transform="rotate({kch:.2f} {fx:.0f} {gy+70:.0f})">'
                  f'<rect x="{fx-62:.0f}" y="{gy+16:.0f}" width="124" height="120" rx="8"'
                  f' fill="{BUMAGA}" {o(5)}/>'
                  f'<path d="M{fx-44:.0f},{gy+46:.0f} h88 M{fx-44:.0f},{gy+74:.0f} h70"'
                  f' stroke="{SEPIA2}" stroke-width="6" opacity=".7"/></g>')
        else:
            # щель раздвигается: программка отходит, в зазор бьёт свет экрана
            sch = .18 + .82 * (.5 + .5 * math.sin(2 * math.pi * (t / 1.45)))
            a = -34 * sch
            m += (f'<g transform="rotate({a:.1f} {fx-60:.0f} {gy+72:.0f})">'
                  f'<rect x="{fx-62:.0f}" y="{gy+16:.0f}" width="124" height="120" rx="8"'
                  f' fill="{BUMAGA}" {o(5)}/>'
                  f'<path d="M{fx-44:.0f},{gy+46:.0f} h88 M{fx-44:.0f},{gy+74:.0f} h70"'
                  f' stroke="{SEPIA2}" stroke-width="6" opacity=".7"/></g>')
            # свет экрана бьёт В ЩЕЛЬ поверх программки — иначе приём не виден
            shch = 5 + 15 * sch
            for k in range(3):
                m += (f'<path d="M{fx-50:.0f},{gy+18-k*5:.0f} l{100:.0f},{-shch*.7:.0f}'
                      f' l0,{shch*(1-k*.3):.1f} l{-100:.0f},{shch*.7:.0f} Z"'
                      f' fill="#fff8e2" opacity="{(.75-k*.22)*(.3+.7*sch)*mig:.2f}"/>')
            m += teplo(fx, gy + 14, 70 + 40 * sch, 44, .5 * sch * mig)
            m += (f'<circle cx="{fx+16:.0f}" cy="{gy+12:.0f}" r="{4+3*sch:.1f}"'
                  f' fill="#fff6dd" opacity="{.5+.5*sch:.2f}"/>')
    # глухой низ ряда: без него тела просвечивают в щелях между креслами
    m += f'<rect y="668" width="{W}" height="{H-668}" fill="#131727"/>'
    # кресла ложатся поверх: из-за спинок видны головы и плечи — ряд сидит
    for i in range(8):
        m += b3_kreslo(32 + i * 238, 622, 222, 330)
    s += SL(Z_SRED, m)
    # ── спинки переднего ряда и мигающий свет экрана
    p = (f'<rect y="840" width="{W}" height="{H-840}" fill="#0a0d13"/>')
    for i in range(5):                        # спинки переднего ряда крупно
        p += (f'<rect x="{-120+i*430:.0f}" y="876" width="330" height="240" rx="64"'
              f' fill="#2a2030" {o(6)}/>'
              f'<rect x="{-80+i*430:.0f}" y="912" width="250" height="150" rx="48"'
              f' fill="{BORDO}" opacity=".45"/>'
              f'<path d="M{-70+i*430:.0f},904 q{120:.0f},-26 {240:.0f},0" fill="none"'
              f' stroke="#cfe4ff" stroke-width="5" opacity=".2"/>')
    for i in range(7):
        p += (f'<path d="M{-80+i*300:.0f},1080 q130,-180 260,0 Z" fill="#101520" {o(5)}/>')
    p += (f'<rect width="{W}" height="{H}" fill="#cfe4ff" opacity="{.09+.14*mig:.2f}"/>')
    p += teplo(960, 1080, 1200, 560, .3 * mig)
    p += baza.ramka_pp("oba", "#07090e", .5)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.52)
    return s


def budka_kinomehanika(t):
    """Будка киномеханика: проектор с двумя катушками, окошко в зал, на стене
    маленький календарь с красной рогатой хозяйкой. Живое: катушки
    вращаются, луч бьёт в окошко, календарь покачивается."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#161a22"/>')
    # ── стена будки с окошком в зал
    d = (f'<rect width="{W}" height="{H}" fill="#2c3240"/>')
    d += baza.kladka(-40, 60, 2000, 700, 86, "#3a4150")
    d += (f'<rect y="0" width="{W}" height="60" fill="#232936" {o(5)}/>')
    okx, oky, okw, okh = 980, 300, 230, 196
    d += (f'<rect x="{okx-34:.0f}" y="{oky-34:.0f}" width="{okw+68:.0f}" height="{okh+68:.0f}"'
          f' rx="10" fill="{CHUGUN}" {o(8)}/>')
    d += (f'<rect x="{okx-20:.0f}" y="{oky-20:.0f}" width="{okw+40:.0f}" height="{okh+40:.0f}"'
          f' rx="8" fill="url(#zhel)" {o(5)}/>')
    d += (f'<rect x="{okx-44:.0f}" y="{oky+okh+34:.0f}" width="{okw+88:.0f}" height="22"'
          f' rx="8" fill="url(#zhel)" {o(5)}/>')
    d += (f'<rect x="{okx:.0f}" y="{oky:.0f}" width="{okw:.0f}" height="{okh:.0f}"'
          f' fill="#8a6a2e" {o(5)}/>')
    puls = .72 + .28 * (.5 + .5 * math.sin(2 * math.pi * (t * 1.05)))
    d += (f'<rect x="{okx:.0f}" y="{oky:.0f}" width="{okw:.0f}" height="{okh:.0f}"'
          f' fill="{SVET}" opacity="{.58*puls:.2f}"/>')
    d += (f'<rect x="{okx+16:.0f}" y="{oky+14:.0f}" width="{okw-32:.0f}" height="{okh-28:.0f}"'
          f' fill="#fff6dd" opacity="{.45*puls:.2f}"/>')
    d += teplo(okx + okw / 2, oky + okh / 2, 280, 240, .6 * puls)
    # календарь на стене: красная рогатая хозяйка года, качается на гвозде
    kach = 2.6 * A.w(t, 3.6)
    kx, ky = 1450, 300
    d += (f'<g transform="rotate({kach:.2f} {kx:.0f} {ky:.0f})">'
          f'{ten(kx+10, ky+350, 110, 16, .45)}'
          f'<rect x="{kx-120:.0f}" y="{ky:.0f}" width="240" height="330" rx="10"'
          f' fill="{BUMAGA}" {o(6)}/>'
          f'<rect x="{kx-120:.0f}" y="{ky:.0f}" width="240" height="74" rx="10"'
          f' fill="{ob.ALYJ}" {o(5)}/>'
          f'<text x="{kx:.0f}" y="{ky+54:.0f}" text-anchor="middle" {SERIF} font-size="44"'
          f' font-weight="bold" fill="#fdf0d2">1967</text>')
    d += ob.koza_malaya(kx - 54, ky + 248, t, .30, .3)
    for i in range(4):
        d += (f'<path d="M{kx-96:.0f},{ky+272+i*16:.0f} h{192:.0f}" stroke="{SEPIA2}"'
              f' stroke-width="4" opacity=".45"/>')
    d += (f'<path d="M{kx:.0f},{ky-10:.0f} v-26" stroke="{ZHELEZ}" stroke-width="7"/>')
    d += f'<circle cx="{kx:.0f}" cy="{ky-10:.0f}" r="9" fill="url(#zhel)" {o(4)}/></g>'
    d += (f'<rect x="96" y="500" width="400" height="24" rx="8" fill="url(#derev)" {o(6)}/>'
          f'<path d="M140,524 l26,40 M444,524 l-26,40" {o(5)} fill="none"/>')
    for i in range(4):
        jx = 150 + i * 94
        d += (f'<ellipse cx="{jx:.0f}" cy="{470:.0f}" rx="42" ry="34" fill="url(#zhel)" {o(5)}/>'
              f'<ellipse cx="{jx:.0f}" cy="{462:.0f}" rx="24" ry="19" fill="{ZHELEZ}" opacity=".7"/>')
    d += (f'<rect x="120" y="640" width="340" height="22" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        jx = 180 + i * 104
        d += (f'<rect x="{jx-40:.0f}" y="{564:.0f}" width="80" height="76" rx="7"'
              f' fill="{CHUGUN}" {o(5)}/>'
              f'<path d="M{jx-30:.0f},{600:.0f} h60" stroke="{ZHELEZ}" stroke-width="6"/>')
    d += baza.hodiki(1740, 250, t, .9)
    d += (f'<rect x="1540" y="690" width="330" height="22" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        jx = 1600 + i * 104
        d += (f'<ellipse cx="{jx:.0f}" cy="{668:.0f}" rx="40" ry="32" fill="url(#zhel)" {o(5)}/>'
              f'<ellipse cx="{jx:.0f}" cy="{660:.0f}" rx="22" ry="17" fill="{ZHELEZ}" opacity=".7"/>')
    s += SL(Z_DAL, d)
    # ── луч от проектора в окошко
    b = (f'<path d="M806,700 L{okx:.0f},{oky+10:.0f} L{okx:.0f},{oky+okh-10:.0f} Z"'
         f' fill="{SVET}" opacity="{.26*puls:.2f}"/>'
         f'<path d="M806,700 L{okx:.0f},{oky+54:.0f} L{okx:.0f},{oky+okh-54:.0f} Z"'
         f' fill="#fff6dd" opacity="{.20*puls:.2f}"/>')
    r = random.Random(29)
    for i in range(26):
        u = r.uniform(.05, .98)
        bx = 806 + u * (okx - 806)
        by = 700 + u * ((oky + okh / 2) - 700) + r.uniform(-.5, .5) * u * okh * .8
        b += (f'<circle cx="{bx:.0f}" cy="{by+((t*11+i*23)%30)-15:.0f}"'
              f' r="{r.uniform(1.6,3.6):.1f}" fill="#fff6dd" opacity="{r.uniform(.3,.8):.2f}"/>')
    s += SL(Z_SRED, b)
    # ── проектор
    m = ten(420, 1006, 330, 28, .55)
    m += (f'<rect x="150" y="860" width="560" height="34" rx="8" fill="url(#chug)" {o(6)}/>'
          f'<rect x="206" y="894" width="46" height="130" rx="10" fill="url(#zhel)" {o(5)}/>'
          f'<rect x="600" y="894" width="46" height="130" rx="10" fill="url(#zhel)" {o(5)}/>'
          f'<rect x="170" y="1016" width="520" height="24" rx="8" fill="{CHUGUN}" {o(5)}/>')
    m += (f'<rect x="250" y="600" width="400" height="270" rx="22" fill="url(#chug)" {o(8)}/>'
          f'<rect x="286" y="636" width="140" height="106" rx="10" fill="{ZHELEZ}" opacity=".7" {o(4)}/>')
    m += (f'<rect x="628" y="660" width="112" height="86" rx="12" fill="url(#zhel)" {o(6)}/>'
          f'<circle cx="760" cy="703" r="48" fill="#1b1e24" {o(7)}/>'
          f'<circle cx="760" cy="703" r="30" fill="{SVET}" opacity="{.6+.4*puls:.2f}"/>'
          f'<circle cx="748" cy="692" r="10" fill="#ffffff" opacity=".7"/>')
    m += teplo(760, 703, 230, 190, .55 * puls)
    m += b3_katushka(330, 520, 118, t, 1.0)
    m += b3_katushka(560, 544, 96, t, -1.2)
    m += (f'<path d="M330,402 q118,-46 230,38" fill="none" stroke="{PLENKA}" stroke-width="13"/>'
          f'<path d="M330,402 q118,-46 230,38" fill="none" stroke="#54504a"'
          f' stroke-width="4" stroke-dasharray="7 11"/>')
    m += (f'<path d="M420,636 q60,-20 134,30" fill="none" stroke="{PLENKA}" stroke-width="11"/>')
    s += SL(Z_SRED, m)
    # ── ближний край стола с бобинами
    p = (f'<rect y="996" width="{W}" height="{H-996}" fill="#201f1e" {o(6)}/>')
    p += f'<rect y="988" width="{W}" height="18" fill="#35312c" {o(4)}/>'
    p += b3_katushka(1430, 1056, 118, t, .55, "#5a5f66")
    for i in range(3):                        # стопка жестянок рядом с бобиной
        p += (f'<ellipse cx="1760" cy="{1050-i*34:.0f}" rx="118" ry="40" fill="url(#zhel)" {o(6)}/>'
              f'<ellipse cx="1760" cy="{1042-i*34:.0f}" rx="74" ry="24" fill="{ZHELEZ}"'
              f' opacity=".65"/>')
    p += baza.ramka_pp("levo", "#0c0b0a", .4)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.48)
    return s


def kassa_i_lishniy_biletik(t):
    """Окошко кассы кинотеатра, очередь со спины в летних платьях, у входа над
    головой трепещет лишний билетик; во дворе за спиной мальчишки показывают
    сценку из кино, соседи смеются. Живое: очередь переступает, билетик
    трепещет, мальчишки размахивают. Окно вставки занимает 860-1840."""
    s = baza.nebo("zakat", t, False)
    s += baza.oblaka(t, 150, 4, 41, .4, "#f8e0bd", 5.0)
    # ── двор за кассой: сценка из кино и соседи-зрители
    d = ""
    for i in range(7):
        bx = 350 + i * 250
        bh = 240 + (i % 3) * 70
        d += (f'<rect x="{bx:.0f}" y="{748-bh:.0f}" width="214" height="{bh:.0f}"'
              f' fill="#5b6575" opacity=".82" {o(4)}/>')
        for j in range(2):
            d += (f'<rect x="{bx+28+j*104:.0f}" y="{774-bh:.0f}" width="72" height="62" rx="5"'
                  f' fill="{SVET}" opacity="{.24+.3*abs(A.w(t,7+i,j*.3)):.2f}" {o(3)}/>')
    for i in range(6):
        d += (f'<ellipse cx="{380+i*290:.0f}" cy="{660+(i%2)*22:.0f}" rx="68" ry="94"'
              f' fill="#3b5333" opacity=".8"/>')
    d += f'<rect y="744" width="{W}" height="152" fill="#6e7886" opacity=".8"/>'
    d += (f'<path d="M-20,792 q480,22 960,8 q480,-14 980,14 L1940,896 L-20,896 Z"'
          f' fill="#5f6a52" opacity=".75"/>')
    for i, (mx, ph) in enumerate(((432, .0), (524, .45), (614, .8))):
        rot = 15 * A.w(t, .8, ph)
        d += (f'<g transform="rotate({rot:.1f} {mx:.0f} 778)">'
              + ob.figura(mx, 778, 164, t, "#2a2535", "#f5d6a4", False, ph, False, .95)
              + f'<path d="M{mx-50:.0f},{692:.0f} q50,-44 100,0" fill="none"'
                f' stroke="#2a2535" stroke-width="13" stroke-linecap="round"/></g>')
    for i, (sx, pl) in enumerate(((706, True), (772, False), (830, True))):
        d += ob.figura(sx, 782, 150, t, "#262430", "#f5d6a4", pl, i * .3, False, .9)
    s += SL(Z_DAL, d)
    # ── стена кинотеатра с окошком кассы
    m = (f'<rect x="-40" y="100" width="380" height="980" fill="url(#krem)" {o(7)}/>')
    m += (f'<rect x="-40" y="100" width="380" height="980" fill="{SHTUK2}" opacity=".32"/>')
    m += (f'<rect x="-40" y="100" width="380" height="44" rx="8" fill="{SHTUK}" {o(5)}/>')
    m += (f'<path d="M-30,140 l150,300" stroke="#ffffff" stroke-width="22" opacity=".10"/>')
    kx, ky, kw, kh = 48, 544, 236, 198
    m += (f'<rect x="{kx-26:.0f}" y="{ky-26:.0f}" width="{kw+52:.0f}" height="{kh+52:.0f}"'
          f' rx="10" fill="url(#derev)" {o(7)}/>')
    m += f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw:.0f}" height="{kh:.0f}" fill="#1a1f28" {o(5)}/>'
    m += (f'<rect x="{kx:.0f}" y="{ky+kh*.50:.0f}" width="{kw:.0f}" height="{kh*.50:.0f}"'
          f' fill="{SVET}" opacity="{.5+.18*abs(A.w(t,4.0)):.2f}"/>')
    m += teplo(kx + kw * .5, ky + kh * .72, 210, 170, .7)
    for i in range(4):
        m += (f'<rect x="{kx+16+i*58:.0f}" y="{ky-6:.0f}" width="13" height="{kh*.46:.0f}"'
              f' rx="6" fill="url(#zhel)" {o(3)}/>')
    m += (f'<rect x="{kx-36:.0f}" y="{ky+kh:.0f}" width="{kw+72:.0f}" height="28" rx="7"'
          f' fill="url(#derev)" {o(6)}/>')
    for i in range(4):                       # синие билетики на полочке кассы
        m += (f'<rect x="{kx+18+i*54:.0f}" y="{ky+kh+4:.0f}" width="48" height="23" rx="4"'
              f' fill="{SINKA}" {o(3)}'
              f' transform="rotate({-8+i*5},{kx+42+i*54:.0f},{ky+kh+15:.0f})"/>')
    # ── тротуар на всю ширину: под окном вставки не должно быть пусто
    m += f'<rect y="868" width="{W}" height="{H-868}" fill="#6f6c64"/>'
    m += f'<rect y="856" width="{W}" height="20" fill="#86826f" {o(4)}/>'
    m += (f'<path d="M-20,906 q480,-20 960,-8 q480,12 980,14 L1940,1080 L-20,1080 Z"'
          f' fill="#7d7a70" opacity=".82"/>')
    for i in range(7):
        m += (f'<path d="M{-40+i*300:.0f},{972+i*12:.0f} q160,12 330,-8" fill="none"'
              f' stroke="#5e5b53" stroke-width="5" opacity=".4"/>')
    # ── очередь со спины: переступает с ноги на ногу
    for i, (fx, hh, pl, kr, ph) in enumerate(((352, 282, True, False, .0),
                                              (474, 294, False, True, .33),
                                              (596, 306, True, False, .66),
                                              (716, 318, False, False, .18))):
        per = 7 * A.w(t, 1.35, ph)
        col = "#241f30" if i % 2 == 0 else "#6a5f82"
        m += (f'<g transform="translate({per:.1f},{-abs(per)*.35:.1f})">'
              + ob.figura(fx, 1014, hh, t, col, "#ffe4b4", pl, ph, False, 1.0, kr)
              + '</g>')
    # парень у входа: лишний билетик над головой трепещет
    m += ob.figura(788, 1020, 344, t, "#242c36", "#f6d6a0", False, .5)
    bx, by = 788, 1020 - 344 * .96
    trep = 12 * A.w(t, .42) + 5 * A.w(t, .19, .3)
    m += (f'<g transform="rotate({trep:.1f} {bx:.0f} {by+40:.0f})">'
          f'<path d="M{bx:.0f},{by-18:.0f} v46" stroke="{SINKA}" stroke-width="8"/>'
          f'<rect x="{bx-42:.0f}" y="{by-78:.0f}" width="84" height="54" rx="6"'
          f' fill="{SINKA}" {o(5)}/>'
          f'<path d="M{bx-28:.0f},{by-62:.0f} h56 M{bx-28:.0f},{by-44:.0f} h38"'
          f' stroke="#cfe0f2" stroke-width="6" opacity=".85"/>'
          f'<circle cx="{bx+26:.0f}" cy="{by-42:.0f}" r="7" fill="{SVET}" opacity=".8"/></g>')
    s += SL(Z_SRED, m)
    p = (f'<path d="M-20,1080 q150,-104 340,-70 L320,1080 Z" fill="#43502f" {o(5)}/>'
         f'<path d="M1740,1080 q-36,-190 60,-266 q96,98 76,266 Z" fill="#3d4d2d" {o(5)}/>')
    p += baza.ramka_pp("levo", "#150f0a", .3)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.42)
    return s


def ulica_idet_v_kino(t):
    """Вечерняя улица частных домов: из калиток выходят нарядные люди и
    собираются в одну весёлую колонну, бабушки под руку, дети впереди. Живое:
    калитки хлопают, дети бегут впереди, подолы платьев колышутся на ходу."""
    s = baza.nebo("zakat", t, False)
    s += baza.oblaka(t, 170, 5, 51, .44, "#f9ddb6", 5.0)
    d = ""
    for i in range(6):
        bx = -60 + i * 360
        d += (f'<rect x="{bx:.0f}" y="440" width="250" height="180" fill="#4c566a"'
              f' opacity=".7"/>'
              f'<path d="M{bx-20:.0f},440 L{bx+125:.0f},364 L{bx+270:.0f},440 Z"'
              f' fill="#404a60" opacity=".75"/>')
    for i in range(8):
        tx = -20 + i * 270
        d += (f'<ellipse cx="{tx:.0f}" cy="{450+(i%3)*26:.0f}" rx="76"'
              f' ry="{114+(i%3)*18:.0f}" fill="#2f4630" opacity=".88"/>'
              f'<rect x="{tx-9:.0f}" y="{548+(i%3)*26:.0f}" width="18" height="70"'
              f' fill="#33261a"/>')
    s += SL(Z_DAL, d)
    # ── дома и штакетник с калитками
    # глухая зелень за штакетником: без неё в просветы между усадьбами
    # светит небо и дома читаются навесами на пустом каркасе
    m = f'<rect y="560" width="{W}" height="260" fill="#2c3f2d"/>'
    r0 = random.Random(31)
    for i in range(22):
        m += (f'<ellipse cx="{-40+i*92:.0f}" cy="{r0.uniform(596,700):.0f}"'
              f' rx="{r0.uniform(62,96):.0f}" ry="{r0.uniform(48,74):.0f}"'
              f' fill="{"#36502f" if i % 2 else "#2a4228"}" opacity=".95"/>')
    for i, (hx, hw, seed, dy) in enumerate(((-150, 490, 2, 0), (330, 440, 5, 22),
                                            (750, 460, 8, -12), (1160, 440, 11, 18),
                                            (1560, 500, 14, -6))):
        m += b3_dom67(hx, 792 + dy, hw * .80, t, seed, i % 2 == 0)
    m += (f'<rect x="-30" y="748" width="1990" height="22" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(44):
        sx = -30 + i * 46
        m += (f'<rect x="{sx:.0f}" y="664" width="22" height="100" rx="6"'
              f' fill="url(#dosk)" {o(4)}/>')
    m += (f'<rect x="-30" y="690" width="1990" height="14" fill="{DOSKA2}" opacity=".75"/>')
    for i in range(5):                        # калитки хлопают
        gx = 150 + i * 430
        hlop = max(0.0, math.sin(2 * math.pi * (t / 2.6 + i * .19))) ** 2
        m += f'<rect x="{gx-6:.0f}" y="650" width="152" height="124" fill="#4a4336" opacity=".5"/>'
        m += (f'<g transform="translate({gx:.0f},650) scale({1-hlop*.74:.3f},1)">'
              f'<rect x="0" y="0" width="140" height="124" rx="8" fill="url(#derev)" {o(6)}/>'
              f'<path d="M8,22 h124 M8,62 h124 M8,102 h124" stroke="{DOSKA2}" stroke-width="8"/>'
              f'<circle cx="122" cy="68" r="9" fill="url(#zhel)" {o(3)}/></g>')
    m += (f'<rect y="764" width="{W}" height="{H-764}" fill="#6a6256"/>')
    m += (f'<path d="M-20,800 q480,32 960,10 q480,-22 980,16 L1940,1080 L-20,1080 Z"'
          f' fill="#787063" opacity=".85"/>')
    for i in range(8):
        m += (f'<path d="M{-60+i*260:.0f},{916+i*14:.0f} q180,16 360,-8" fill="none"'
              f' stroke="#5d5549" stroke-width="5" opacity=".45"/>')
    s += SL(Z_SRED, m)
    # ── колонна: бабушки под руку, нарядные, дети впереди
    p = ""
    hod = (t * 30.0) % 220
    for i, (fx, hh, pl, kr, ph) in enumerate(((228, 322, True, False, .0),
                                              (316, 316, True, True, .3),
                                              (486, 336, False, False, .55),
                                              (578, 330, False, True, .15),
                                              (742, 326, True, False, .75),
                                              (938, 340, False, False, .4))):
        x = fx + hod * .5
        p += ob.figura(x, 1024, hh, t, "#2a2334" if i % 2 == 0 else "#473c58",
                       "#ffe0ab", pl, ph, False, 1.0, kr)
        pod = 8 * A.w(t, .7, ph)                 # подол колышется на ходу
        hip = 1024 - hh * .40
        p += (f'<path d="M{x-hh*.145:.0f},{hip:.0f} q{hh*.145:.0f},{12+pod:.0f}'
              f' {hh*.29:.0f},0 l{hh*.025:.0f},{hh*.40:.0f}'
              f' q{-hh*.17:.0f},{16-pod:.0f} {-hh*.34:.0f},0 Z"'
              f' fill="{ob.ALYJ2 if kr else "#352e46"}" {o(4)}/>')
        p += (f'<path d="M{x-hh*.17:.0f},{1024:.0f} q{hh*.17:.0f},{16-pod:.0f} {hh*.34:.0f},0"'
              f' fill="none" stroke="#f8d8a2" stroke-width="4" opacity=".45"/>')
    for i, (bx, hh, ph) in enumerate(((1272, 206, .0), (1420, 192, .5))):
        beg = 96 * ((t * .42 + i * .2) % 1.0)
        pr = abs(math.sin(math.pi * (t * 2.4 + i * .5))) * 20
        p += ob.figura(bx + beg, 1030 - pr, hh, t, "#2d2838", "#ffd79a", False, ph,
                       False, 1.0, i == 0)
        p += ten(bx + beg, 1032, 42, 11, .45)
    s += SL(Z_PERED, p)
    s += SL(Z_PERED, baza._ramka_pp("pravo", "#160f0a", .32))
    s += baza.vinetka(.42)
    return s


def tetradka_pesennik(t):
    """Тетрадка-песенник в клеёнчатой обложке крупно: ручка выводит строчки
    волнистыми линиями, на поля ложится вырезанный цветок. За ней — стол,
    над тарелками плывёт вторая тетрадка, которую передают из рук в руки."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1b2130"/>'
           + f'<rect width="{W}" height="{H}" fill="#2b2436" opacity=".6"/>')
    # ── комната и праздничный стол на дальнем плане
    d = f'<rect x="860" y="0" width="{W-860}" height="760" fill="#3a2f44"/>'
    for i in range(9):
        d += (f'<rect x="{880+i*120:.0f}" y="0" width="52" height="760" fill="#48384f"'
              f' opacity=".7"/>')
    d += f'<rect x="860" y="744" width="{W-860}" height="26" fill="#2b2434" {o(5)}/>'
    d += baza.lampa(1360, 300, t, 1.0, True)
    d += teplo(1360, 420, 620, 460, .55)
    # люди за столом: сперва фигуры, столешница ложится поверх — они СИДЯТ
    for i, (fx, hh, pl, ph) in enumerate(((1010, 320, True, .1), (1290, 330, False, .5),
                                          (1620, 324, True, .8))):
        d += ob.figura(fx, 582, hh, t, "#2a2436", "#f0c070", pl, ph, False, .95)
    d += ob.stol_prazdnik(900, 540, 1020, t)
    for i, (px, r_) in enumerate(((1020, 60), (1176, 54), (1332, 58), (1492, 52), (1646, 56))):
        d += (f'<ellipse cx="{px:.0f}" cy="538" rx="{r_:.0f}" ry="{r_*.34:.0f}"'
              f' fill="#f2ead8" {o(4)}/>'
              f'<ellipse cx="{px:.0f}" cy="534" rx="{r_*.62:.0f}" ry="{r_*.2:.0f}"'
              f' fill="{MED}" opacity=".55"/>'
              f'<ellipse cx="{px-r_*.20:.0f}" cy="530" rx="{r_*.26:.0f}"'
              f' ry="{r_*.13:.0f}" fill="{ob.ALYJ2}" opacity=".85"/>'
              f'<ellipse cx="{px+r_*.22:.0f}" cy="532" rx="{r_*.22:.0f}"'
              f' ry="{r_*.11:.0f}" fill="{ZEL2}" opacity=".85"/>')
    d += baza.svecha(1790, 430, t, .2, 1.0, 92)
    d += ob.bokal(1716, 544, t, .66, .3)
    s += SL(Z_DAL, d)
    # ── тетрадка плывёт над столом из рук в руки
    u = (t * .26) % 1.0
    tx = 980 + 760 * A.ease(u)
    ty = 470 - 60 * math.sin(math.pi * u)
    m = (f'<g transform="translate({tx:.0f},{ty:.0f}) rotate({-8+16*u:.1f})">'
         f'{ten(10, 54, 86, 14, .5)}'
         f'<rect x="-84" y="-58" width="168" height="112" rx="8" fill="{SINKA}" {o(5)}/>'
         f'<rect x="-70" y="-46" width="140" height="88" rx="5" fill="#eae3cf" opacity=".9"/>'
         f'<path d="M-56,-24 h112 M-56,0 h96 M-56,22 h112" stroke="#8d9bb0" stroke-width="5"/>'
         f'</g>')
    s += SL(Z_SRED, m)
    # ── тетрадка крупно, на столе
    p = (f'<path d="M-40,1080 q60,-150 300,-168 q420,-28 740,8 L1000,1080 Z"'
         f' fill="url(#derev)" {o(7)}/>')
    p += (f'<path d="M-40,938 q320,-40 700,-16" fill="none" stroke="#b78a52"'
          f' stroke-width="9" opacity=".5"/>')
    p += ten(470, 1006, 420, 34, .55)
    p += (f'<g transform="rotate(-3 470 700)">'
          f'<rect x="60" y="300" width="840" height="680" rx="18" fill="{SINKA}" {o(8)}/>'
          f'<rect x="60" y="300" width="840" height="680" rx="18" fill="#101a2a" opacity=".25"/>'
          f'<path d="M96,340 l240,420" stroke="#ffffff" stroke-width="22" opacity=".10"/>'
          f'<rect x="92" y="330" width="776" height="620" rx="10" fill="#f3eddb" {o(5)}/>')
    # клетка
    for i in range(13):
        p += (f'<line x1="{120+i*58:.0f}" y1="340" x2="{120+i*58:.0f}" y2="940"'
              f' stroke="#b9c8d6" stroke-width="2.5" opacity=".7"/>')
    for i in range(11):
        p += (f'<line x1="104" y1="{368+i*58:.0f}" x2="856" y2="{368+i*58:.0f}"'
              f' stroke="#b9c8d6" stroke-width="2.5" opacity=".7"/>')
    p += f'<line x1="186" y1="330" x2="186" y2="950" stroke="{KRAS}" stroke-width="4" opacity=".7"/>'
    # строчки появляются одна за другой, ручка идёт по последней
    nstrok = 6
    r = random.Random(7)
    volny = []
    for i in range(nstrok):
        y0 = 410 + i * 86
        volny.append((y0, r.uniform(.8, 1.3)))
    put = min(1.0, t / 2.4) * nstrok
    for i, (y0, am) in enumerate(volny):
        dolya = max(0.0, min(1.0, put - i))
        if dolya <= 0:
            continue
        shir = (600 if i % 2 == 0 else 520) * dolya
        d_ = f'M210,{y0:.0f}'
        n = 9
        for j in range(n):
            xx = 210 + shir * (j + 1) / n
            d_ += f' q{shir/n/2:.0f},{(-17 if j % 2 == 0 else 17)*am:.0f} {shir/n:.0f},0'
        p += f'<path d="{d_}" fill="none" stroke="#1f2a44" stroke-width="7" stroke-linecap="round"/>'
    # ручка над концом последней строки
    ai = min(nstrok - 1, int(put))
    ay = volny[ai][0]
    ax = 210 + (600 if ai % 2 == 0 else 520) * max(0.0, min(1.0, put - ai))
    p += (f'<g transform="translate({ax:.0f},{ay:.0f}) rotate({34+3*A.w(t,.5):.1f})">'
          f'<path d="M0,0 l14,-34 l-28,0 Z" fill="{CHUGUN}" {o(3)}/>'
          f'<rect x="-15" y="-250" width="30" height="218" rx="12" fill="{ob.ALYJ2}" {o(5)}/>'
          f'<rect x="-15" y="-250" width="12" height="218" rx="6" fill="#ffffff" opacity=".18"/>'
          f'<rect x="-18" y="-66" width="36" height="34" rx="6" fill="url(#zol)" {o(4)}/></g>')
    # вырезанный цветок приклеивается на поля
    pk = A.over(A.seg(t, 1.1, .9))
    fx, fy = 134, 690
    p += (f'<g transform="translate({fx:.0f},{fy:.0f}) scale({pk:.3f}) rotate({18*(1-pk)+4*A.w(t,5.0):.1f})"'
          f' opacity="{min(1.0, pk*1.3):.2f}">')
    for i in range(6):
        a = i * 60
        p += (f'<ellipse cx="0" cy="-34" rx="17" ry="30" fill="{ob.ALYJ}" {o(3)}'
              f' transform="rotate({a})"/>')
    p += f'<circle r="15" fill="url(#zol)" {o(3)}/></g>'
    pk2 = A.over(A.seg(t, 2.4, .9))
    if pk2 > .01:
        p += (f'<g transform="translate(140,838) scale({pk2*.78:.3f})"'
              f' opacity="{min(1.0, pk2*1.3):.2f}">')
        for i in range(6):
            p += (f'<ellipse cx="0" cy="-34" rx="17" ry="30" fill="{ZOL}" {o(3)}'
                  f' transform="rotate({i*60})"/>')
        p += f'<circle r="15" fill="{ob.ALYJ}" {o(3)}/></g>'
    p += '</g>'
    s += SL(Z_PERED, p)
    s += SL(Z_PERED, baza._ramka_pp("pravo", "#120e14", .26))
    s += baza.vinetka(.46)
    return s


def malchik_s_samokatom_i_devushka_s_k(t):
    """У стены кинотеатра рядом стоят мальчик с самодельным самокатом и
    девушка в платье в горошек. Живое: самокат катается туда-сюда, подол в
    горошек колышется, над обоими всплывают золотые кружки под цифры."""
    s = baza.nebo("den", t, False)
    s += baza.oblaka(t, 140, 4, 61, .4, "#eef4f9", 6.0)
    # ── дальний план: афишная тумба и тополя
    d = (f'<rect x="1430" y="300" width="500" height="630" fill="#60697a" opacity=".75" {o(4)}/>')
    for e in range(3):
        for c in range(3):
            d += (f'<rect x="{1466+c*150:.0f}" y="{340+e*150:.0f}" width="92" height="94" rx="5"'
                  f' fill="{SVET}" opacity="{.18+.26*abs(A.w(t,8+e,c*.3)):.2f}" {o(3)}/>')
    d += (f'<rect x="1410" y="276" width="540" height="34" rx="8" fill="#4e5666" {o(4)}/>')
    d += ten(1300, 834, 110, 20, .45)
    d += (f'<rect x="1222" y="470" width="156" height="364" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<ellipse cx="1300" cy="470" rx="92" ry="26" fill="{DOSKA2}" {o(5)}/>'
          f'<rect x="1238" y="512" width="124" height="190" rx="6" fill="{BUMAGA}" {o(4)}/>'
          f'<path d="M1252,560 h96 M1252,600 h78 M1252,640 h96" stroke="{SEPIA2}"'
          f' stroke-width="7" opacity=".6"/>')
    for i in range(4):
        d += (f'<ellipse cx="{1520+i*150:.0f}" cy="{380+(i%2)*26:.0f}" rx="74" ry="104"'
              f' fill="#3b5333" opacity=".75"/>')
    s += SL(Z_DAL, d)
    # ── стена кинотеатра
    m = (f'<rect x="-40" y="120" width="1300" height="780" fill="url(#krem)" {o(7)}/>'
         f'<rect x="-40" y="120" width="1300" height="780" fill="{SHTUK2}" opacity=".28"/>'
         f'<rect x="-40" y="120" width="1300" height="38" rx="8" fill="{SHTUK}" {o(5)}/>')
    for i in range(4):
        m += (f'<rect x="{40+i*300:.0f}" y="240" width="190" height="300" rx="8"'
              f' fill="#2d3a46" opacity=".5" {o(5)}/>'
              f'<path d="M{48+i*300:.0f},252 l60,120" stroke="#ffffff" stroke-width="12" opacity=".16"/>')
    m += (f'<rect x="-40" y="866" width="1300" height="58" rx="8" fill="{SHTUK2}" {o(6)}/>')
    m += f'<rect y="918" width="{W}" height="{H-918}" fill="#73695d"/>'
    m += (f'<path d="M-20,940 q960,-30 1940,0 L1920,1080 L0,1080 Z" fill="#80766a" opacity=".8"/>')
    m += (f'<path d="M-20,962 q480,-14 960,-6 q480,8 980,10" fill="none" stroke="#5f574c"'
          f' stroke-width="5" opacity=".45"/>')
    s += SL(Z_SRED, m)
    # ── мальчик с самодельным самокатом: катается туда-сюда
    p = ""
    kat = 150 * math.sin(2 * math.pi * (t / 2.9))
    mx = 430 + kat
    p += ob.figura(mx - 46, 1012, 310, t, "#2b3242", "#f3d79f", False, .2, True)
    p += ten(mx + 40, 1024, 134, 16, .5)
    p += (f'<g transform="translate({mx:.0f},1016)">'
          f'<rect x="-104" y="-26" width="288" height="26" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="-104" y="-26" width="288" height="9" fill="#ffffff" opacity=".16"/>'
          f'<rect x="142" y="-230" width="24" height="208" rx="9" fill="url(#derev)" {o(5)}/>'
          f'<rect x="86" y="-244" width="136" height="22" rx="10" fill="url(#derev)" {o(5)}/>'
          f'<path d="M92,-236 q62,-14 124,0" fill="none" stroke="{ob.ALYJ}" stroke-width="10"/>'
          f'<path d="M154,-222 L-66,-26" fill="none" stroke="{DOSKA2}" stroke-width="12"/>'
          f'<circle cx="-82" cy="8" r="28" fill="{CHUGUN}" {o(5)}/>'
          f'<circle cx="-82" cy="8" r="9" fill="{ZHELEZ}"/>'
          f'<circle cx="162" cy="8" r="28" fill="{CHUGUN}" {o(5)}/>'
          f'<circle cx="162" cy="8" r="9" fill="{ZHELEZ}"/></g>')
    # ── девушка лет двадцати в платье в горошек, коса через плечо
    gx, gh, gb = 1110, 392, 1018
    p += ob.figura(gx, gb, gh, t, "#b04a52", "#ffe0ae", False, .6)
    pod = 11 * A.w(t, 1.9)
    hip = gb - gh * .44
    p += (f'<path d="M{gx-gh*.15:.0f},{hip:.0f} q{gh*.15:.0f},{14+pod:.0f} {gh*.30:.0f},0'
          f' l{gh*.04:.0f},{gh*.44:.0f} q{-gh*.19:.0f},{18-pod:.0f} {-gh*.38:.0f},0 Z"'
          f' fill="#c75f68" {o(5)}/>')
    r = random.Random(3)
    for i in range(20):                      # горошек по подолу
        u = r.uniform(0, 1); v = r.uniform(0, 1)
        dx = (gh * .15 + gh * .04 * v) * r.uniform(-1, 1)
        dy = hip + gh * .44 * v
        p += (f'<circle cx="{gx+dx+pod*.12*v:.1f}" cy="{dy:.0f}" r="7" fill="#f8ece0"'
              f' opacity=".92"/>')
    p += (f'<path d="M{gx-gh*.14:.0f},{hip+18:.0f} q{gh*.14:.0f},{16-pod:.0f} {gh*.28:.0f},0"'
          f' fill="none" stroke="#ffe0ae" stroke-width="5" opacity=".5"/>')
    # коса: от ВИСКА вниз по плечу, к концу тоньше, на конце бант
    for k, (wd, t0, t1) in enumerate(((22, .00, .34), (17, .30, .60), (12, .56, .82))):
        p += (f'<path d="M{gx-gh*(.12+.015*k):.0f},{gb-gh*(.80-.22*t0):.0f}'
              f' q{-gh*.05:.0f},{gh*.12:.0f} {gh*.012:.0f},{gh*(.22*(t1-t0)+.04):.0f}"'
              f' fill="none" stroke="{"#7a5733" if k % 2 == 0 else "#64462a"}"'
              f' stroke-width="{wd}" stroke-linecap="round"/>')
    bx_ = gx - gh * .13
    by_ = gb - gh * .80 + gh * .26
    p += (f'<path d="M{bx_-16:.0f},{by_:.0f} q16,-16 32,0 q-16,16 -32,0 Z" fill="{ob.ALYJ}" {o(4)}/>'
          f'<circle cx="{bx_:.0f}" cy="{by_:.0f}" r="6" fill="{ob.ALYJ2}"/>')
    # ── золотые кружки под цифры возраста всплывают над обоими
    for i, (cx, t0) in enumerate(((mx + 20, .4), (gx, 1.0))):
        vs = A.out(A.seg(t, t0, .8))
        if vs <= .01:
            continue
        cy = 640 - 110 * vs - 16 * A.w(t, 2.6, i * .4)
        p += (f'<g opacity="{vs:.2f}">{teplo(cx, cy, 160, 160, .5)}'
              f'<path d="M{cx:.0f},{cy+66:.0f} v{(1 if i else 1)*96:.0f}" stroke="url(#zol)"'
              f' stroke-width="5" stroke-dasharray="10 9" opacity=".8"/>'
              f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{70*vs:.0f}" fill="url(#zol)" {o(6)}/>'
              f'<circle cx="{cx-22:.0f}" cy="{cy-24:.0f}" r="{17*vs:.0f}" fill="#fff6cf"'
              f' opacity=".6"/></g>')
    s += SL(Z_PERED, p)
    s += SL(Z_PERED, baza._ramka_pp("levo", "#141009", .28))
    s += baza.vinetka(.4)
    return s


def kolyaska_i_yubileynyy_pirog(t):
    """Низкая коляска шестидесятых у подъезда с торчащей погремушкой на глазах
    становится столом с именинным пирогом, на пироге шестьдесят из свечек.
    Живое: погремушка качается, коляска превращается в стол, свечки загораются."""
    s = baza.nebo("zakat", t, False)
    s += baza.oblaka(t, 190, 4, 71, .4, "#f6dcba", 5.0)
    # ── подъезд
    d = (f'<rect x="-60" y="60" width="2040" height="760" fill="url(#beton)" {o(7)}/>')
    for i in range(5):
        d += (f'<line x1="-60" y1="{170+i*150:.0f}" x2="1980" y2="{170+i*150:.0f}"'
              f' stroke="{BETON2}" stroke-width="6" opacity=".5"/>')
    for e, oy in enumerate((160, 420, 640)):
        for i in range(6):
            ox_ = 120 + i * 300
            if oy > 380 and 640 < ox_ < 1180:
                continue                      # над козырьком подъезда окон нет
            on = (i + e) % 2 == 0
            d += (f'<rect x="{ox_:.0f}" y="{oy:.0f}" width="152" height="122" rx="6"'
                  f' fill="{SVET if on else "#49596a"}"'
                  f' opacity="{(.4+.35*abs(A.w(t,8+i+e,i*.2))) if on else .3:.2f}" {o(4)}/>'
                  f'<line x1="{ox_+76:.0f}" y1="{oy:.0f}" x2="{ox_+76:.0f}" y2="{oy+122:.0f}"'
                  f' stroke="{BETON2}" stroke-width="7"/>')
    d += (f'<rect x="700" y="420" width="470" height="420" rx="10" fill="#1d2430" {o(7)}/>'
          f'<rect x="676" y="376" width="518" height="56" rx="10" fill="{BETON2}" {o(6)}/>')
    for bx in (420, 1120):                   # балконы по сторонам подъезда
        for i in range(3):
            by = 302 + i * 260
            d += (f'<rect x="{bx:.0f}" y="{by:.0f}" width="230" height="26" rx="7"'
                  f' fill="{BETON2}" {o(5)}/>')
            for k in range(7):
                d += (f'<line x1="{bx+14+k*34:.0f}" y1="{by:.0f}" x2="{bx+14+k*34:.0f}"'
                      f' y2="{by-70:.0f}" stroke="{BETON2}" stroke-width="6"/>')
            d += (f'<rect x="{bx-4:.0f}" y="{by-78:.0f}" width="238" height="12" rx="5"'
                  f' fill="{BETON2}" {o(4)}/>')
    d += (f'{ten(1620, 824, 120, 16, .5)}'
          f'<rect x="1546" y="744" width="20" height="78" fill="{DOSKA2}" {o(4)}/>'
          f'<rect x="1672" y="744" width="20" height="78" fill="{DOSKA2}" {o(4)}/>'
          f'<rect x="1530" y="722" width="180" height="24" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        d += (f'<ellipse cx="{520+i*180:.0f}" cy="{824:.0f}" rx="74" ry="56"'
              f' fill="{TRAV68}" opacity=".9" {o(5)}/>')
    d += teplo(935, 640, 260, 230, .45)
    d += (f'<rect x="724" y="452" width="200" height="388" rx="8" fill="url(#derev)" {o(5)}/>'
          f'<rect x="944" y="452" width="200" height="388" rx="8" fill="url(#derev)" {o(5)}/>')
    d += (f'<rect y="820" width="{W}" height="{H-820}" fill="#6f6a60"/>')
    d += (f'<path d="M-20,846 q960,-26 1940,0 L1920,1080 L0,1080 Z" fill="#7d786d" opacity=".8"/>')
    s += SL(Z_DAL, d)
    # ── превращение: коляска → стол с пирогом
    uhod = A.ease(A.seg(t, .9, .8))           # коляска уходит
    per = A.ease(A.seg(t, 1.5, .9))           # стол с пирогом приходит
    m = ""
    cx, cy = 935, 964
    if uhod < .99:
        op = 1 - uhod
        m += (f'<g opacity="{op:.2f}" transform="translate({cx:.0f},{cy:.0f}) scale({1-uhod*.18:.3f})">'
              f'{ten(0, 44, 230, 26, .55)}'
              f'<path d="M-210,-40 q0,-150 210,-150 q210,0 210,150 q0,54 -60,54 l-300,0 q-60,0 -60,-54 Z"'
              f' fill="{SINKA}" {o(8)}/>'
              f'<path d="M-186,-70 q40,-120 190,-120 q150,0 190,120 Z" fill="#3e6490" opacity=".8"/>'
              f'<path d="M-150,-140 q150,-70 300,0" fill="none" stroke="#dfe7ef" stroke-width="10" opacity=".55"/>'
              f'<rect x="-230" y="10" width="460" height="22" rx="10" fill="url(#zhel)" {o(5)}/>'
              f'<circle cx="-150" cy="44" r="42" fill="{CHUGUN}" {o(6)}/>'
              f'<circle cx="-150" cy="44" r="14" fill="{ZHELEZ}"/>'
              f'<circle cx="150" cy="44" r="42" fill="{CHUGUN}" {o(6)}/>'
              f'<circle cx="150" cy="44" r="14" fill="{ZHELEZ}"/>'
              f'<path d="M190,-150 q80,-40 120,-120" fill="none" stroke="url(#zhel)" stroke-width="14"/>')
        # погремушка качается на ручке
        kach = 22 * A.w(t, 1.25)
        m += (f'<g transform="translate(300,-282) rotate({kach:.1f})">'
              f'<path d="M0,0 v64" stroke="{ob.ALYJ2}" stroke-width="8"/>'
              f'<circle cx="0" cy="88" r="30" fill="{ob.ALYJ}" {o(5)}/>'
              f'<circle cx="-10" cy="78" r="9" fill="#ffd9cf" opacity=".7"/>'
              f'<circle cx="0" cy="88" r="46" fill="{ob.ALYJ}" opacity="{.12+.16*abs(A.w(t,1.25)):.2f}"/></g>')
        m += '</g>'
    if per > .01:
        m += (f'<g opacity="{per:.2f}" transform="translate({cx:.0f},{cy:.0f}) scale({.86+.14*per:.3f})">')
        for lx in (-310, 250):
            m += (f'<rect x="{lx:.0f}" y="-26" width="46" height="150" rx="8"'
                  f' fill="url(#derev)" {o(6)}/>')
        m += (f'<rect x="-300" y="86" width="606" height="22" rx="8" fill="{DOSKA2}" {o(5)}/>')
        m += ob.stol_prazdnik(-390, -30, 780, t)
        m += '</g>'
        # пирог со свечками
        px, py = cx, cy - 98
        m += (f'<g opacity="{per:.2f}">')
        m += ten(px + 16, py + 82, 250, 22, .55)
        m += (f'<path d="M{px-270:.0f},{py:.0f} q0,84 270,84 q270,0 270,-84 l0,-104'
              f' q0,-84 -270,-84 q-270,0 -270,84 Z" fill="url(#med)" {o(7)}/>')
        m += (f'<ellipse cx="{px:.0f}" cy="{py-104:.0f}" rx="270" ry="84" fill="url(#krem)" {o(6)}/>')
        m += (f'<ellipse cx="{px:.0f}" cy="{py-104:.0f}" rx="222" ry="64" fill="#f8ead0" opacity=".92"/>')
        for i in range(14):
            a = 2 * math.pi * i / 14
            m += (f'<circle cx="{px+248*math.cos(a):.0f}" cy="{py-6+76*math.sin(a):.0f}" r="12"'
                  f' fill="{ob.ALYJ}" opacity=".9"/>')
        # точки лежат НА верхней плоскости пирога (эллипс rx 270, ry 84)
        tochki = sorted(b3_tochki_60(px, py - 108, 120), key=lambda q: q[1])
        for i, (sx, sy) in enumerate(tochki):
            gor = A.out(A.seg(t, 2.1 + i * .05, .3))
            m += b3_svechka(sx, sy, 15, t, gor * per, i * .13, 9)
        m += teplo(px, py - 200, 480, 340, .55 * per)
        m += '</g>'
    s += SL(Z_SRED, m)
    p = (f'<path d="M1640,1080 q-40,-230 70,-330 q110,120 86,330 Z" fill="#3f5330" {o(6)}/>'
         f'<path d="M-20,1080 q80,-170 10,-250 q150,70 170,250 Z" fill="#3a4c2d" {o(5)}/>')
    p += baza.ramka_pp("pravo", "#130f0a", .3)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.44)
    return s


def barhatnyy_albom_s_ugolkami(t):
    """Бархатный альбом с уголками на коленях: открыта страница с подписью
    года, на ней четыре чёрно-белые рисованные карточки. Живое: страница
    переворачивается, карточки чуть отходят от уголков, закладка-тесьма
    ведёт по подписи."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#191520"/>')
    # ── комната за альбомом: тёплое окно и ёлка пятном
    d = f'<rect width="{W}" height="{H}" fill="#241d2c" opacity=".9"/>'
    d += (f'<rect x="1388" y="118" width="444" height="384" rx="10" fill="#1d1724" {o(8)}/>')
    d += baza.okno_izby(1420, 150, 380, 320, t, None, 0.0, False, True)
    d += (f'<rect x="1420" y="150" width="380" height="320" fill="{SVET}" opacity=".40"/>')
    d += (f'<rect x="1386" y="128" width="448" height="18" rx="8" fill="url(#derev)" {o(5)}/>'
          f'<circle cx="1392" cy="137" r="14" fill="{MED}" {o(4)}/>'
          f'<circle cx="1828" cy="137" r="14" fill="{MED}" {o(4)}/>')
    d += baza.zanaveska(1434, 146, 300, 84, "#e2d4b6", t, 1)
    d += baza.zanaveska(1786, 146, 300, 84, "#e2d4b6", t, -1)
    d += (f'<rect x="1396" y="470" width="428" height="26" rx="8" fill="url(#derev)" {o(5)}/>')
    d += baza.krynka(1470, 468, .7)
    d += teplo(1610, 310, 520, 440, .5)
    d += ob.elka(300, 620, 480, t, True, True, 9)
    d += (f'<rect y="620" width="{W}" height="24" fill="#2e2535" opacity=".9"/>')
    s += SL(Z_DAL, d)
    # ── альбом
    m = ten(950, 1010, 620, 40, .6)
    m += (f'<g transform="rotate(-2 940 700)">'
          f'<rect x="250" y="300" width="1400" height="690" rx="22" fill="#5c1f2c" {o(9)}/>'
          f'<rect x="250" y="300" width="1400" height="690" rx="22" fill="#2c0c14" opacity=".32"/>')
    for i in range(16):                     # ворс бархата
        m += (f'<path d="M{274+i*88:.0f},316 q22,330 0,660" fill="none" stroke="#7b2c3a"'
              f' stroke-width="7" opacity=".28"/>')
    m += (f'<rect x="286" y="332" width="1328" height="626" rx="14" fill="#efe6d2" {o(6)}/>'
          f'<rect x="286" y="332" width="1328" height="626" rx="14" fill="{SEPIA}" opacity=".34"/>')
    m += (f'<rect x="930" y="332" width="30" height="626" fill="#c9b690" opacity=".8"/>')
    # подпись года — волной чернил, цифры кладёт over
    m += (f'<rect x="384" y="812" width="474" height="76" rx="12" fill="#e4d8bc"'
          f' opacity=".85" {o(4)}/>')
    m += (f'<path d="M420,856 q52,-40 104,0 q52,40 104,0 q52,-40 104,0 q30,22 56,6"'
          f' fill="none" stroke="#24335a" stroke-width="11" stroke-linecap="round"/>')
    # закладка-тесьма ведёт по подписи
    vu = (t * .33) % 1.0
    vx = 420 + 368 * A.ease(vu)
    m += (f'<path d="M{vx:.0f},600 q{18*A.w(t,2.4):.0f},132 {-6:.0f},238" fill="none"'
          f' stroke="{ob.ALYJ}" stroke-width="22" stroke-linecap="round"/>'
          f'<path d="M{vx-10:.0f},838 l12,32 l12,-32 Z" fill="{ob.ALYJ2}" {o(3)}/>')
    # четыре карточки
    for i, (kx, ky, vid, otk, ph) in enumerate(((344, 364, "dom", .9, .0),
                                                (1004, 364, "para", .5, .3),
                                                (1004, 586, "elka", .3, .6),
                                                (344, 586, "koza", 1.0, .85))):
        m += b3_kartochka_bw(kx, ky, 540, 214, vid, t, otk, ph)
    m += '</g>'
    # страница переворачивается
    pu = ((t * .24) + .62) % 1.0
    if pu < .26:
        k = A.ease(pu / .26)
        shir = 660 * abs(math.cos(math.pi * k))
        m += (f'<g transform="translate(945,330)">'
              f'<path d="M0,0 l{shir:.0f},{18 if k < .5 else -18} l0,626 l{-shir:.0f},18 Z"'
              f' fill="#f3ebd8" {o(5)} opacity=".97"/>'
              f'<path d="M0,0 l{shir*.3:.0f},6 l0,626 l{-shir*.3:.0f},10 Z"'
              f' fill="#000000" opacity="{.22*(1-abs(.5-k)*2):.2f}"/></g>')
    s += SL(Z_SRED, m)
    # ── колени
    p = (f'<path d="M-40,1080 q120,-230 420,-236 q300,-6 420,236 Z" fill="#3b3348" {o(7)}/>'
         f'<path d="M1060,1080 q120,-242 420,-236 q300,6 420,236 Z" fill="#453a52" {o(7)}/>')
    p += (f'<path d="M160,980 q220,-120 420,-30" fill="none" stroke="#574c68"'
          f' stroke-width="10" opacity=".7"/>'
          f'<path d="M1260,984 q220,-120 420,-26" fill="none" stroke="#5f5372"'
          f' stroke-width="10" opacity=".7"/>')
    s += SL(Z_PERED, p)
    s += baza.vinetka(.5)
    return s


# ═══════════════ lok_b4.py ═══════════════

OKNO = (860, 300, 980, 551)


def b4_komnata(pol_y=842, stena="#c6b093", t=0.0, polosa=True, tepl=.0):
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


def b4_plate(x, y, t, col, ph=.0, w_=138, h_=262, kach=1.0, vyshivka=None,
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


def b4_plate_lezhit(x, y, t, s_=1.0, grad="tkan", col=None, rukava=True):
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


def b4_shkaf(x, base, w_, h_, t, raskryt=1.0, nutro="#4a3524"):
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


def b4_zerkalo(x, y, rx, ry, t, vid="", ramka="url(#zol)", ph=.0):
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


def b4_tkan_volna(y0, h_, t, grad, ph=.0, amp=46, per=3.2, op=1.0, temn=.0):
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


def b4_busina(x, y, r_, col, bl=.8):
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_:.1f}" fill="{col}" {o(3)}/>'
            f'<circle cx="{x-r_*.32:.0f}" cy="{y-r_*.34:.0f}" r="{r_*.30:.1f}"'
            f' fill="#ffffff" opacity="{bl:.2f}"/>')


def b4_pugovica(x, y, r_, col, t, ph=.0, dyr=4):
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


def b4_katushka(x, y, s_, col, t, ph=.0):
    """Катушка ниток: деревянный торец и намотка."""
    k = 1 + .04 * A.w(t, 2.6, ph)
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({s_*k:.3f})">'
            f'<ellipse cx="3" cy="8" rx="46" ry="20" fill="#000" opacity=".25"/>'
            f'<ellipse rx="46" ry="30" fill="url(#derev)" {o(5)}/>'
            f'<ellipse rx="34" ry="21" fill="{col}" {o(4)}/>'
            f'<ellipse rx="12" ry="8" fill="url(#derev)" {o(3)}/>'
            f'<path d="M34,-4 q26,14 46,2" fill="none" stroke="{col}"'
            f' stroke-width="5" stroke-linecap="round"/></g>')


def b4_lenta(x, y, w_, t, col, ph=.0, raspr=.0):
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


def b4_igla(x, y, a, t, dlina=96):
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


def b4_nozhnicy(x, y, a, razvod, t, s_=1.0):
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


def b4_babochka(x, y, t, s_, ph=.0, col=None):
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


def b4_maneken(x, base, h_, t, col, ph=.0):
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


def raskrytyy_shkaf_s_naryadami(t):
    """Распахнутый шкаф при дневном свете. Живые: плечики едут по перекладине,
    платья качаются, солнечный зайчик ползёт по дверце."""
    s = SL(Z_NEBO, b4_komnata(858, "#cdbda0", t, True))
    dal = baza.okno_izby(96, 150, 300, 380, t,
                         vid='<rect x="96" y="150" width="300" height="380" fill="#cfe2f2"/>'
                             '<rect x="96" y="400" width="300" height="130" fill="#e8f1f8"/>',
                         svet=True, moroz=.2)
    dal += baza.luch(300, 190, 230, 700, t, .26)
    dal += teplo(420, 430, 560, 480, .35)
    s += SL(Z_DAL, dal)

    sr = b4_shkaf(470, 900, 760, 690, t, 1.0)
    hod = (t * 26.0) % 128.0
    for i, (col, gr, hh) in enumerate((
            (TKAN, "tkan", 268), ("#2f5f78", None, 250), (ZOL, "zol", 262),
            ("#6d8a4e", None, 244), ("#b06a9a", None, 256), (KREM, "krem", 266))):
        sr += b4_plate(548 + i * 122 - hod * .30, 400, t, col, ph=i * .19,
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


def krasnaya_tkan_vo_ves_kadr(t):
    """Красная ткань разворачивается во весь кадр. Живые: ткань идёт волной,
    складки расправляются, блики бегут по полотну."""
    skl = 1.0 - A.ease(A.seg(t, .5, 1.6))
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#5c1317"/>'
           + b4_tkan_volna(-260, 760, t, "tkan", .0, 86, 5.0, .9, .26)
           + teplo(W * .42, H * .40, 1150, 860, .32))
    s += SL(Z_DAL, b4_tkan_volna(60, 760, t, "tkan", .30, 76, 4.2, 1.0, .14))
    sr = b4_tkan_volna(420, 760, t, "tkan", .58, 66, 3.4, 1.0, .0)
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
    pp = b4_tkan_volna(800, 620, t, "tkan", .86, 54, 2.8, 1.0, .0)
    for i in range(3):
        u = ((t / 2.6) + i * .34) % 1.0
        bx = -500 + u * (W + 1000)
        pp += (f'<path d="M{bx:.0f},-60 l230,0 l-170,{H+120:.0f} l-230,0 Z"'
               f' fill="#ffc2ad" opacity="{.16*(1-abs(u-.5)*1.3):.2f}"/>')
    pp += baza.begushchiy_blik(t, 4.6, .0, .14, 420)
    s += SL(Z_PERED, pp)
    s += baza.vinetka(.42)
    return s


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


def babushka_povyazyvaet_krasnuyu_kosy(t):
    """Бабушка в профиль у зеркальца повязывает красную косынку в горох.
    Живые: концы косынки завязываются, бабушка кивает, зеркало ловит блик."""
    s = SL(Z_NEBO, b4_komnata(880, "#bfae92", t, True, .0))
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
    s += SL(Z_SRED, b4_zerkalo(1040, 400, 130, 170, t, otr, "url(#med)"))

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
    s += SL(Z_LETIT, b4_babochka(1060, 700, t, 2.1, .0)
            + b4_babochka(1560, 800, t, 1.7, .4, "#f0f0e2")
            + b4_babochka(250, 760, t, 1.9, .7, "#e8a85c"))
    s += baza.vinetka(.30)
    return s


def chetyre_otreza_tkani(t):
    """Четыре отреза веером на столе. Живые: отрезы приподнимаются по одному,
    сантиметровая лента сползает со стола, свет скользит по тканям."""
    s = SL(Z_NEBO, b4_komnata(930, "#b9a98f", t, True, .0))
    dal = baza.okno_izby(1440, 150, 360, 320, t, svet=True, moroz=.25)
    dal += baza.luch(1500, 190, 200, 620, t, .20)
    dal += baza.polka(90, 260, 380)
    dal += b4_katushka(150, 246, .8, TKAN, t, .1)
    dal += b4_katushka(240, 248, .7, "#3f5c7a", t, .4)
    dal += b4_katushka(330, 246, .75, ZOL, t, .7)
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


def blyudce_s_ukrasheniyami(t):
    """Блюдце с серьгами и кольцом у зеркала, рядом пояс с пряжкой.
    Живые: серьги поблёскивают, кольцо катится по блюдцу, пряжка ловит свет.
    Окно вставки справа — всё главное в полосе 0-830."""
    s = SL(Z_NEBO, b4_komnata(940, "#b6a68d", t, True, .0))
    dal = b4_zerkalo(290, 290, 208, 254, t, "", "url(#med)")
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


def babushka_vybiraet_svetloe(t):
    """Бабушка у своего шкафа: чёрное платье уезжает в угол, светлая блузка
    снимается с плечиков, на стене кухни шевелится листок численника."""
    s = SL(Z_NEBO, b4_komnata(890, "#c3b396", t, True, .0))
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

    sr = b4_shkaf(90, 900, 700, 660, t, .9)
    sr += (f'<rect x="128" y="372" width="624" height="16" rx="8"'
           f' fill="url(#zhel)" {o(5)}/>')
    ugol = A.ease(A.seg(t, .6, 2.0))
    sr += b4_plate(650 + 88 * ugol, 416, t, "#1d1a1c", ph=.1, w_=118, h_=232,
                 kach=.5)
    sr += (f'<rect x="{650+88*ugol-70:.0f}" y="416" width="140" height="250"'
           f' fill="#000000" opacity="{.42*ugol:.2f}"/>')
    for i, col in enumerate(("#6d8a4e", TKAN2, "#9a6f8c")):
        sr += b4_plate(224 + i * 112, 416, t, col, ph=i * .3, w_=116, h_=226,
                     kach=.6)
    s += SL(Z_SRED, sr)

    sn = A.out(A.seg(t, 2.6, 1.8))
    bx, by = 546 - 34 * sn, 414 + 120 * sn
    pp = f'<g transform="rotate({-8*sn:.1f} {bx:.0f} {by:.0f})">'
    pp += b4_plate(bx, by, t, KREM, ph=.6, w_=152 + 40 * sn, h_=250, kach=1.4,
                 vyshivka=TKAN, grad="krem")
    pp += "</g>"
    pp += teplo(bx, by + 110, 300, 260, .35 * sn)
    pp += ob.figura(960, 1070, 720, t, col="#3d3036", kant="#f3cf92", platok=True)
    s += SL(Z_PERED, pp + baza.begushchiy_blik(t, 8.5, .5, .08))
    s += baza.vinetka(.32)
    return s


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
        sr += b4_maneken(mx, 840, 600, t, ("#d13a2c", "#b32a26", "#d13a2c")[i], i * .33)
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
            pp += b4_busina(bx, by, 30, ob.ALYJ)
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


def ded_i_vnuchka_u_zerkala(t):
    """Дед и внучка у трюмо. Живые: уголок красного платка расправляется в
    кармане, бант завязывается, внучка вертится перед зеркалом."""
    s = SL(Z_NEBO, b4_komnata(900, "#b8a58d", t, True, .0))
    dal = ob.girlyanda(60, 130, 1860, 150, t, 13, 96, .3)
    dal += baza.polka(1520, 400, 330)
    dal += baza.krynka(1600, 392, .55)
    dal += teplo(900, 500, 820, 560, .34)
    s += SL(Z_DAL, dal)

    otr = ob.figura(880, 740, 470, t, col="#3a3240", kant="#f0c070")
    sr = b4_zerkalo(880, 420, 300, 330, t, otr, "url(#derev)")
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


def novoe_plate_pered_podrugami(t):
    """Мостик в память: девушка в новом платье кружится перед подругами.
    Живые: юбка кружится, подруги качаются и тянутся к подолу, коса летит."""
    s = SL(Z_NEBO, b4_komnata(910, "#a89a86", t, True, .0))
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


def shite_platya_po_vecheram(t):
    """Мостик в память: вечернее шитьё в три приёма — журнал с выкройкой,
    ручная машинка под лампой, платье на живую нитку. Живые: колесо машинки
    крутится, ткань ползёт под лапкой, булавки поблёскивают.
    Окно вставки справа — работа идёт в полосе 0-830."""
    s = SL(Z_NEBO, b4_komnata(900, "#8f7f6b", t, True, .0))
    dal = baza.lampa(410, 250, t, 1.45, False)
    dal += teplo(410, 420, 820, 660, .55)
    dal += baza.polka(40, 190, 250)
    dal += b4_katushka(110, 176, .66, TKAN, t, .2)
    dal += b4_katushka(190, 178, .6, KREM, t, .6)
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
        pp += b4_zerkalo(170, 420, 140, 240, t, "", "url(#derev)")
        pp += b4_plate(560, 280, t, KREM, ph=.3, w_=280, h_=450, kach=.8,
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


def mamino_plate_stanovitsya_dochkinym(t):
    """Мамино платье на столе становится дочкиным. Живые: ножницы идут по
    ткани, платье уменьшается, девочка идёт, придерживая подол."""
    s = SL(Z_NEBO, b4_komnata(900, "#bfa98b", t, True, .0))
    dal = baza.okno_izby(1400, 140, 350, 300, t, svet=True, moroz=.3)
    dal += baza.luch(1450, 180, 200, 620, t, .20)
    dal += baza.polka(80, 260, 300)
    dal += b4_katushka(150, 246, .7, KREM, t, .3)
    dal += b4_katushka(240, 248, .65, TKAN, t, .8)
    dal += teplo(560, 480, 700, 540, .32)
    s += SL(Z_DAL, dal)

    sr = baza.stol(40, 700, 960, 44, True)
    um = A.ease(A.seg(t, .5, 1.7))
    k = 1.0 - .40 * um
    ax, ay = 520, 470
    sr += (f'<g transform="translate({ax:.0f},{ay:.0f}) scale({k:.3f})'
           f' translate({-ax:.0f},{-ay:.0f})">')
    sr += b4_plate_lezhit(ax, ay, t, 1.0, "tkan")
    sr += "</g>"
    u = A.ease(A.seg(t, .4, 1.9))
    nx = ax - 300 + 600 * u
    ny = ay + 196 - 40 * math.sin(math.pi * u)
    sr += (f'<path d="M{ax-300:.0f},{ay+196:.0f} q300,-40 600,0" fill="none"'
           f' stroke="#f4efe2" stroke-width="8" stroke-dasharray="22 15"'
           f' opacity=".85"/>')
    sr += b4_nozhnicy(nx, ny, -14 + 10 * math.sin(2 * math.pi * t),
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


def vorotnichok_i_busy_iz_ryabiny(t):
    """Стол у окна: к простому платью пришивается кружевной воротничок, рядом
    нанизываются рябиновые бусы. Живые: игла ходит, ягоды нанизываются,
    воротничок ложится на платье."""
    s = SL(Z_NEBO, b4_komnata(920, "#b5a388", t, True, .0))
    dal = baza.okno_izby(700, 90, 460, 380, t, svet=True, moroz=.28)
    dal += baza.luch(780, 150, 280, 700, t, .24)
    dal += baza.ryabina(1620, 500, t, 1.1, 5)
    dal += teplo(860, 440, 760, 580, .36)
    s += SL(Z_DAL, dal)

    sr = baza.stol(20, 700, 1880, 48, True)
    sr += b4_plate_lezhit(500, 540, t, .86, None, "#8ea8bc")
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
    pp += b4_igla(ix, iy, -26 + 40 * math.sin(2 * math.pi * u), t, 100)
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
            pp += b4_busina(bx, by, 24, KRAS)
        elif i == nag:
            dp = 1.0 - A.seg(t, .3 + i * (4.6 / 15), 4.6 / 15)
            pp += b4_busina(bx, by - 140 * dp, 24, KRAS)
    pp += teplo(nx, ny + 40, 340, 220, .22)
    s += SL(Z_PERED, pp + baza.begushchiy_blik(t, 8.2, .6, .09))
    s += baza.vinetka(.34)
    return s


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
    dal += b4_katushka(1500, 236, .8, TKAN, t, .1)
    dal += b4_katushka(1600, 238, .75, "#3f5c7a", t, .5)
    dal += b4_katushka(1700, 236, .7, ZOL, t, .9)
    s += SL(Z_DAL, dal)

    cx, cy = 420, 670
    rsp = A.ease(A.seg(t, 1.4, 2.4))
    sr = b4_lenta(90, 950, 560, t, ob.ALYJ, .0, rsp)
    sr += b4_lenta(170, 1014, 600, t, ob.ZOLOTO, .4, rsp * .85)
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
        sr += b4_pugovica(cx + 300 * rad * math.cos(a), cy + 212 * rad * math.sin(a),
                        r.uniform(16, 34), col, t, i * .13, r.choice((2, 4)))
    for i, (kx, ky, kc, ks) in enumerate(((cx - 190, cy + 96, TKAN, .9),
                                          (cx + 76, cy + 136, "#3f5c7a", .8),
                                          (cx + 196, cy - 56, KREM, .75))):
        sr += b4_katushka(kx, ky, ks, kc, t, i * .3)
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


# ═══════════════ lok_b5.py ═══════════════

OKNO = (860, 300, 980, 551)


BAND = 830


MUKA = "#f3ecdc"


TESTO = "#ead9b4"


FARSH = "#9c4a3a"


HOLOD = "#1a2440"


STENA = "#2b3449"


STENA2 = "#1a2130"


CHAY = "#c9892f"


def b5_gladko(pts, zamknut=False):
    """Ломаную — в мягкую кривую: через середины отрезков."""
    d = "M%.0f,%.0f" % (pts[0][0], pts[0][1])
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        d += " Q%.0f,%.0f %.0f,%.0f" % (x0, y0, (x0 + x1) / 2, (y0 + y1) / 2)
    d += " L%.0f,%.0f" % (pts[-1][0], pts[-1][1])
    return d + (" Z" if zamknut else "")


def b5_tochka_lomanoy(pts, u):
    """Точка на ломаной по доле пути: по ней едут запах, чек, мандарин."""
    dl = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
          for i in range(len(pts) - 1)]
    L = sum(dl) or 1.0
    s = max(0.0, min(.999, u)) * L
    for i, d in enumerate(dl):
        if s <= d:
            k = s / (d or 1.0)
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k,
                    pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k)
        s -= d
    return pts[-1]


def b5_stena(t, teplo_x=520, teplo_y=520, col=STENA, col2=STENA2, R=820):
    """Холодная стена комнаты и ОДНО тёплое пятно — гамма праздника."""
    s = f'<rect width="{W}" height="{H}" fill="{col2}"/>'
    s += f'<rect y="{H*.08:.0f}" width="{W}" height="{H*.92:.0f}" fill="{col}" opacity=".9"/>'
    for i in range(7):
        s += (f'<rect x="{i*W/7:.0f}" y="{H*.08:.0f}" width="4" height="{H*.92:.0f}"'
              f' fill="#0e131d" opacity=".25"/>')
    s += teplo(teplo_x, teplo_y, R, R * .82, .62)
    return s


def b5_za_oknom(x, y, w_, h_, t, col=HOLOD, seed=21, n=15):
    """Что видно за стеклом: синяя ночь и падающий снег."""
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="{col}"/>'
    r = random.Random(seed)
    for i in range(n):
        x0 = r.uniform(x, x + w_)
        per = r.uniform(4.0, 9.0)
        ph = r.random()
        u = ((t / per) + ph) % 1.0
        s += (f'<circle cx="{x0 + 24*A.w(t,5.2,ph):.0f}" cy="{y + u*h_:.0f}"'
              f' r="{r.uniform(2.2,4.8):.1f}" fill="{SNEG}" opacity=".8"/>')
    return s


def b5_skatert(x, y, w_, t, svis=104, col="url(#rush)", kant=None, amp=9.0,
             ph=0.0, n=6, polosa=True, gl=130):
    """Скатерть на столе: ПЛОСКОСТЬ столешницы в перспективе, передняя кромка,
    свисающий край волной, красная полоса. Без плоскости стол читается доской."""
    kant = kant or ob.ALYJ
    bot = y + 26 + svis
    pts = []
    for i in range(n + 1):
        u = 1 - i / n
        pts.append((x - 12 + (w_ + 24) * u,
                    bot + amp * A.w(t, 2.4 + i * .32, ph + i * .17)))
    s = ten(x + w_ / 2, bot + 44, w_ * .52, 30, .5)
    # ПЛОСКОСТЬ столешницы в перспективе: дальняя кромка уже передней
    dd = min(w_ * .17, 190.0)
    s += (f'<path d="M{x+dd:.0f},{y-gl:.0f} L{x+w_-dd:.0f},{y-gl:.0f}'
          f' L{x+w_+20:.0f},{y:.0f} L{x-20:.0f},{y:.0f} Z" fill="{col}" {o(6)}/>')
    s += (f'<path d="M{x+dd:.0f},{y-gl:.0f} L{x+w_-dd:.0f},{y-gl:.0f}" fill="none"'
          f' stroke="#ffffff" stroke-width="8" opacity=".3"/>')
    for i in range(1, 5):
        u = i / 5.0
        s += (f'<path d="M{x + dd + (w_ - 2*dd)*u:.0f},{y-gl:.0f}'
              f' L{x - 20 + (w_ + 40)*u:.0f},{y:.0f}" stroke="#d9c8a4"'
              f' stroke-width="3" opacity=".35"/>')
    d = ("M%.0f,%.0f h%.0f v26 L%.0f,%.0f " % (x - 20, y, w_ + 40, pts[0][0], pts[0][1])
         + b5_gladko(pts)[1:] + " L%.0f,%.0f Z" % (x - 20, y + 26))
    s += f'<path d="{d}" fill="{col}" {o(6)}/>'
    if polosa:
        up = [(px, py - 34) for px, py in pts]
        s += (f'<path d="{b5_gladko(up)}" fill="none" stroke="{kant}"'
              f' stroke-width="9" opacity=".75" stroke-linecap="round"/>')
    for i in range(1, n):
        px = pts[i][0]
        s += (f'<path d="M{px:.0f},{y+28:.0f} q{6*A.w(t,3.4,i*.2):.0f},{svis*.5:.0f}'
              f' {2:.0f},{svis*.9:.0f}" fill="none" stroke="#cdb98d"'
              f' stroke-width="4" opacity=".55"/>')
    s += (f'<rect x="{x-20:.0f}" y="{y:.0f}" width="{w_+40:.0f}" height="12" rx="6"'
          f' fill="#ffffff" opacity=".35"/>')
    return s


def b5_blyudo(cx, cy, r_, t=0.0, col="url(#krem)", obod=None, ph=0.0):
    """Блюдо силуэтом: овал, золотой ободок, блик. Без кухонной мелочи."""
    obod = obod or ob.ZOLOTO
    s = ten(cx, cy + r_ * .30, r_ * .92, r_ * .22, .5)
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r_:.0f}" ry="{r_*.34:.0f}"'
          f' fill="{col}" {o(6)}/>')
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy-2:.0f}" rx="{r_*.74:.0f}" ry="{r_*.24:.0f}"'
          f' fill="none" stroke="{obod}" stroke-width="5" opacity=".8"/>')
    bl = .3 + .3 * abs(A.w(t, 3.6, ph))
    s += (f'<ellipse cx="{cx-r_*.36:.0f}" cy="{cy-r_*.13:.0f}" rx="{r_*.24:.0f}"'
          f' ry="{r_*.07:.0f}" fill="#ffffff" opacity="{.25+bl:.2f}"/>')
    return s


def b5_pelmen(cx, cy, s_=1.0, a=0.0, iney=0.0, vyh=1.0):
    """Пельмень силуэтом: тело, защип дугой, блик. Иней — белая вуаль."""
    if vyh <= .02:
        return ""
    w_ = 42 * s_ * vyh
    h_ = 27 * s_ * vyh
    s = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({a:.1f})">'
    s += ten(0, h_ * 1.05, w_ * .9, h_ * .36, .4)
    s += f'<ellipse rx="{w_:.1f}" ry="{h_:.1f}" fill="url(#krem)" {o(max(3, 4*s_)):s}/>'
    s += (f'<path d="M{-w_*.8:.1f},{h_*.1:.1f} q{w_*.8:.1f},{h_*.95:.1f} {w_*1.6:.1f},0"'
          f' fill="none" stroke="#d6c097" stroke-width="{max(2.4, 4*s_):.1f}"/>')
    for i in range(4):
        u = -.6 + i * .4
        s += (f'<path d="M{w_*u:.1f},{h_*.5:.1f} q{w_*.1:.1f},{h_*.36:.1f} {w_*.2:.1f},0"'
              f' fill="none" stroke="#c3ab7e" stroke-width="{max(1.8, 2.8*s_):.1f}"/>')
    s += (f'<ellipse cx="{-w_*.3:.1f}" cy="{-h_*.36:.1f}" rx="{w_*.25:.1f}"'
          f' ry="{h_*.22:.1f}" fill="#ffffff" opacity=".5"/>')
    if iney > .01:
        s += f'<ellipse rx="{w_:.1f}" ry="{h_:.1f}" fill="{INEY}" opacity="{min(.8, iney*.8):.2f}"/>'
        for i in range(5):
            s += (f'<circle cx="{-w_*.6 + i*w_*.3:.1f}" cy="{h_*(-.3 + (i%2)*.5):.1f}"'
                  f' r="{2.4*s_:.1f}" fill="#ffffff" opacity="{min(.9, iney):.2f}"/>')
    return s + "</g>"


def b5_banka(x, y, w_, h_, t, soderzh="#b63b27", ph=0.0, kryshka=True, zontik=False):
    """Банка припасов: стекло, содержимое ПЯТНОМ, крышка, бегущий блик."""
    s = ten(x, y + 10, w_ * .62, w_ * .17, .45)
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' rx="{w_*.18:.0f}" fill="url(#stekl)" opacity=".88" {o(5)}/>')
    s += (f'<rect x="{x-w_/2+7:.0f}" y="{y-h_*.8:.0f}" width="{w_-14:.0f}"'
          f' height="{h_*.74:.0f}" rx="{w_*.14:.0f}" fill="{soderzh}" opacity=".92"/>')
    for i in range(3):
        s += (f'<circle cx="{x - w_*.2 + i*w_*.2:.0f}" cy="{y - h_*(.24 + .2*(i % 2)):.0f}"'
              f' r="{w_*.13:.0f}" fill="#ffffff" opacity=".16"/>')
    if zontik:
        for i in range(5):
            a = -1.5 + i * .55
            s += (f'<path d="M{x:.0f},{y-h_*.52:.0f} l{math.cos(a)*w_*.3:.0f},'
                  f'{-abs(math.sin(a))*h_*.2 - h_*.1:.0f}" fill="none" stroke="#8fae5a"'
                  f' stroke-width="4" opacity=".85"/>')
    if kryshka:
        s += (f'<rect x="{x-w_*.57:.0f}" y="{y-h_-22:.0f}" width="{w_*1.14:.0f}"'
              f' height="28" rx="9" fill="url(#zhel)" {o(5)}/>')
    bl = ((t * .5 + ph) % 1.0)
    s += (f'<rect x="{x - w_*.42 + bl*w_*.6:.0f}" y="{y-h_*.88:.0f}" width="{w_*.1:.0f}"'
          f' height="{h_*.7:.0f}" rx="{w_*.05:.0f}" fill="#ffffff"'
          f' opacity="{.18 + .3*math.sin(math.pi*bl):.2f}"/>')
    return s


def b5_muka(x, y, w_, t, n=20, seed=3, R=180, sp=.55, op=.6):
    """Мучная пыль: поднимается и оседает — живой элемент всех кухонных планов."""
    r = random.Random(seed)
    s = ""
    for i in range(n):
        ph = r.random()
        per = r.uniform(1.7, 3.4) / sp
        u = ((t / per) + ph) % 1.0
        xx = x + r.uniform(0, w_) + 46 * A.w(t, 3.0 + i * .19, ph)
        yy = y - R * math.sin(math.pi * u) * r.uniform(.45, 1.0)
        s += (f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{r.uniform(2.6,6.8):.1f}"'
              f' fill="{MUKA}" opacity="{op*(1-abs(2*u-1)):.2f}"/>')
    return s


def b5_drozh(x, y, w_, t, n=5, R=160, op=.32, col="#ffd49a"):
    """Дрожь тёплого воздуха — над батареей и над горячим блюдом."""
    s = ""
    for i in range(n):
        xx = x + (i + .5) * w_ / n
        d = "M%.0f,%.0f" % (xx, y)
        for k in range(1, 5):
            dy = -R * k / 4.0
            dx = 15 * A.w(t, 1.5 + i * .27, k * .26)
            d += " Q%.0f,%.0f %.0f,%.0f" % (xx + dx * 1.7, y + dy + R / 8.0, xx + dx, y + dy)
        s += (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5"'
              f' opacity="{op:.2f}" stroke-linecap="round"/>')
    return s


def b5_vilka(cx, cy, a, s_=1.0, dl=1.0):
    """Вилка силуэтом: черенок и три зубца. Тянется к блюду сама, без рukи."""
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({a:.1f}) scale({s_:.3f})">'
    g += f'<rect x="10" y="-11" width="{150*dl:.0f}" height="22" rx="11" fill="#c9d2da" {o(5)}/>'
    g += f'<path d="M-52,-34 q54,-14 62,34 q-8,48 -62,34 z" fill="#dde5ec" {o(5)}/>'
    for i in (-1, 0, 1):
        g += (f'<rect x="-116" y="{i*24-7:.0f}" width="70" height="14" rx="7"'
              f' fill="#dde5ec" {o(4)}/>')
    g += '<rect x="-40" y="-24" width="10" height="48" rx="5" fill="#ffffff" opacity=".6"/>'
    return g + "</g>"


def b5_stul(x, y, t, s_=1.0, spinka=True, otodvinut=0.0):
    """Табурет или стул со спинкой — сиденье и ножки, с тенью и бликом."""
    g = f'<g transform="translate({x + otodvinut:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 14, 108, 22, .5)
    if spinka:
        g += f'<rect x="-82" y="-430" width="164" height="30" rx="12" fill="url(#derev)" {o(6)}/>'
        g += f'<rect x="-74" y="-400" width="22" height="180" rx="8" fill="url(#derev)" {o(5)}/>'
        g += f'<rect x="52" y="-400" width="22" height="180" rx="8" fill="url(#derev)" {o(5)}/>'
    g += f'<rect x="-104" y="-232" width="208" height="34" rx="12" fill="url(#derev)" {o(6)}/>'
    g += f'<rect x="-96" y="-226" width="190" height="10" rx="5" fill="#ffffff" opacity=".28"/>'
    for xx in (-88, 66):
        g += f'<rect x="{xx}" y="-198" width="24" height="198" rx="8" fill="url(#derev)" {o(5)}/>'
    g += '<rect x="-80" y="-120" width="160" height="14" rx="6" fill="#6d4423" opacity=".8"/>'
    return g + "</g>"


def b5_kuvshin(x, y, s_=1.0, col="#eef3f8"):
    """Кувшин молока: тулово, горло, носик, блик."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 10, 66, 15, .45)
    g += (f'<path d="M-60,0 q-16,-108 14,-146 l0,-40 q46,-14 92,0 l0,40'
          f' q30,38 14,146 z" fill="{col}" {o(6)}/>')
    g += '<path d="M46,-186 q44,10 30,54" fill="none" stroke="#dfe6ee" stroke-width="16"/>'
    g += '<ellipse cx="-22" cy="-104" rx="16" ry="54" fill="#ffffff" opacity=".55"/>'
    g += f'<path d="M-56,-56 q56,20 112,0" fill="none" stroke="#c6d2dd" stroke-width="7"/>'
    return g + "</g>"


def b5_zelen(x, y, t, s_=1.0, n=9, ph=0.0, col=None, vyh=1.0):
    """Пучок зелени: перья качаются вразнобой — живой элемент стола."""
    if vyh <= .02:
        return ""
    col = col or "#5f8a3e"
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_*vyh:.3f})">'
    g += ten(0, 8, 70, 14, .4)
    for i in range(n):
        u = (i / (n - 1.0)) - .5
        kch = 13 * A.w(t, 2.2 + i * .21, ph + i * .13)
        c = (col, "#79a44f", "#486f31")[i % 3]
        g += (f'<path d="M{u*54:.0f},6 q{u*40 + kch*.5:.0f},-70 {u*66 + kch:.0f},-136"'
              f' fill="none" stroke="{c}" stroke-width="13" stroke-linecap="round"/>')
        g += (f'<circle cx="{u*66 + kch:.0f}" cy="-138" r="15" fill="{c}" opacity=".9"/>')
    g += f'<path d="M-30,6 q30,16 60,0" fill="none" stroke="{ob.ALYJ}" stroke-width="10"/>'
    return g + "</g>"


def b5_syr(x, y, s_=1.0, vyh=1.0):
    """Тарелка с сыром: три клина жёлтым пятном, дырки — три точки."""
    if vyh <= .02:
        return ""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_*vyh:.3f})">'
    g += b5_blyudo(0, 0, 96, 0.0, "url(#krem)")
    for i, dx in enumerate((-48, 0, 48)):
        g += (f'<path d="M{dx:.0f},-12 l62,-10 l-16,-46 z" fill="url(#zol)" {o(5)}'
              f' transform="rotate({-14 + i*14},{dx},-12)"/>')
        g += f'<circle cx="{dx+28:.0f}" cy="-32" r="6" fill="#b58a28" opacity=".8"/>'
    return g + "</g>"


def b5_ogurcy(x, y, s_=1.0, vyh=1.0):
    """Огурцы и редиска силуэтом: зелёные веретёна и красные шарики."""
    if vyh <= .02:
        return ""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_*vyh:.3f})">'
    g += b5_blyudo(0, 0, 102, 0.0, "url(#krem)")
    for i, (dx, a) in enumerate(((-54, -14), (-6, 6), (42, -8))):
        g += (f'<ellipse cx="{dx:.0f}" cy="-22" rx="44" ry="17" fill="#4f7a37" {o(5)}'
              f' transform="rotate({a},{dx},-22)"/>')
        g += (f'<ellipse cx="{dx-12:.0f}" cy="-28" rx="18" ry="5" fill="#8fb866" opacity=".7"/>')
    for i, dx in enumerate((-30, 16, 58)):
        g += f'<circle cx="{dx:.0f}" cy="-50" r="20" fill="{ob.ALYJ}" {o(4)}/>'
        g += f'<circle cx="{dx-6:.0f}" cy="-56" r="6" fill="#ffffff" opacity=".45"/>'
        g += f'<path d="M{dx:.0f},-68 q8,-18 22,-16" fill="none" stroke="#6f9a46" stroke-width="6"/>'
    return g + "</g>"


def b5_rukavichka(x, y, s_=1.0, col=None, t=0.0, ph=0.0):
    """Вязаная рukавичка: ладонь не рисуем — варежка работает сама."""
    col = col or ob.ALYJ
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 16, 92, 18, .45)
    g += (f'<path d="M-78,10 q-20,-104 24,-140 q54,-32 112,-4 q44,26 26,144 z"'
          f' fill="{col}" {o(6)}/>')
    g += (f'<path d="M66,-86 q54,-14 52,34 q-2,40 -50,28" fill="{col}" {o(5)}/>')
    g += f'<rect x="-82" y="-4" width="168" height="40" rx="18" fill="{ob.ALYJ2}" {o(5)}/>'
    for i in range(6):
        g += (f'<path d="M{-70 + i*28:.0f},-2 v34" fill="none" stroke="#6d1316"'
              f' stroke-width="6" opacity=".6"/>')
    for i in range(4):
        g += (f'<path d="M{-58 + i*32:.0f},-116 q10,30 0,60" fill="none"'
              f' stroke="#ffffff" stroke-width="5" opacity=".2"/>')
    return g + "</g>"


def b5_kozhura(x, y, a=0.0, s_=1.0, zagib=0.0):
    """Кусочек кожуры: подсыхая, загибается — живой элемент батареи."""
    k = 1.0 + zagib
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({a:.1f}) scale({s_:.3f})">'
            f'{ten(0, 16, 46, 10, .4)}'
            f'<path d="M-54,10 q{26*k:.0f},{-58*k:.0f} 54,{-18*k:.0f}'
            f' q{30*k:.0f},{14*k:.0f} 54,{18*k:.0f} q-54,{26:.0f} -108,0 z"'
            f' fill="{ob.MANDA}" {o(5)}/>'
            f'<path d="M-44,2 q52,{-40*k:.0f} 98,{-4*k:.0f}" fill="none"'
            f' stroke="#fff0dc" stroke-width="7" opacity=".6"/></g>')


def b5_kartochka_video(x, y, w_, h_, t, vyh=1.0, ph=0.0, tema=0):
    """Карточка-обложка другого видео: рамка, рисованный стол и хозяйка года.
    Текста НЕ рисуем — заголовок кладёт over.py."""
    if vyh <= .02:
        return ""
    g = (f'<g transform="translate({x + w_/2:.1f},{y + h_:.1f}) scale({vyh:.3f})'
         f' translate({-w_/2:.1f},{-h_:.1f})">')
    g += ten(w_ / 2, h_ + 20, w_ * .48, 24, .55)
    fon = (ob.HVOYA, ob.ALYJ2, "#243a52")[tema % 3]
    g += f'<rect width="{w_:.0f}" height="{h_:.0f}" rx="22" fill="{fon}" {o(7)}/>'
    g += (f'<rect x="10" y="10" width="{w_-20:.0f}" height="{h_-20:.0f}" rx="16"'
          f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="6" opacity=".85"/>')
    g += teplo(w_ * .5, h_ * .42, w_ * .5, h_ * .36, .45)
    # рисованный стол внутри обложки
    ty = h_ * .70
    g += (f'<rect x="{w_*.12:.0f}" y="{ty:.0f}" width="{w_*.76:.0f}" height="{h_*.05:.0f}"'
          f' rx="8" fill="url(#rush)" {o(4)}/>')
    for i, dx in enumerate((.24, .42, .62)):
        g += (f'<ellipse cx="{w_*dx:.0f}" cy="{ty-6:.0f}" rx="{w_*.08:.0f}"'
              f' ry="{w_*.03:.0f}" fill="{(KREM, ob.MANDA, "#7f9f55")[i]}" {o(3)}/>')
    g += baza.svecha(w_ * .80, ty - 46, t, ph, .34, 70)
    g += ob.koza_malaya(w_ * .34, ty - 10, t, w_ / 2100.0 * 1.5, ph)
    # бегущий блик по глянцу обложки
    bl = ((t * .34 + ph) % 1.0)
    g += (f'<path d="M{w_*bl - w_*.5:.0f},0 l{w_*.2:.0f},0 l{-w_*.3:.0f},{h_:.0f}'
          f' l{-w_*.2:.0f},0 z" fill="#ffffff" opacity=".10"/>')
    return g + "</g>"


def b5_tetrad(x, y, w_, h_, t, ph=0.0):
    """Тетрадка в клетку, исписанная: страница переворачивается сама."""
    g = f'<g transform="translate({x:.1f},{y:.1f})">'
    g += ten(w_ / 2, h_ + 14, w_ * .5, 18, .5)
    g += f'<rect width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="#f3f0e2" {o(6)}/>'
    for i in range(int(w_ / 26)):
        g += (f'<line x1="{i*26:.0f}" y1="0" x2="{i*26:.0f}" y2="{h_:.0f}"'
              f' stroke="#9db7cf" stroke-width="2" opacity=".55"/>')
    for i in range(int(h_ / 26)):
        g += (f'<line x1="0" y1="{i*26:.0f}" x2="{w_:.0f}" y2="{i*26:.0f}"'
              f' stroke="#9db7cf" stroke-width="2" opacity=".55"/>')
    r = random.Random(17)
    for i in range(9):
        yy = 34 + i * (h_ - 56) / 8.0
        ww = r.uniform(.4, .86) * w_
        g += (f'<path d="M{w_*.08:.0f},{yy:.0f} h{ww:.0f}" stroke="#2f4256"'
              f' stroke-width="5" opacity=".7" stroke-linecap="round"/>')
    # страница переворачивается: ширина листа идёт от полной к нулю и обратно
    u = ((t / 3.4) + ph) % 1.0
    k = abs(math.cos(math.pi * u))
    g += (f'<g transform="translate({w_/2:.0f},0) scale({k:.3f},1) translate({-w_/2:.0f},0)">'
          f'<rect width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="#fbf8ec" {o(5)}/>'
          f'<path d="M{w_*.1:.0f},{h_*.3:.0f} h{w_*.7:.0f} M{w_*.1:.0f},{h_*.52:.0f}'
          f' h{w_*.5:.0f} M{w_*.1:.0f},{h_*.74:.0f} h{w_*.64:.0f}" stroke="#2f4256"'
          f' stroke-width="5" opacity=".6" stroke-linecap="round"/></g>')
    g += f'<rect x="{w_*.46:.0f}" y="0" width="10" height="{h_:.0f}" fill="#b9a884" opacity=".7"/>'
    return g + "</g>"


def b5_vetka_eli(x, y, dl, t, s_=1.0, ph=0.0, vniz=1.0):
    """Еловая лапа: ось и иглы двумя тонами, лёгкое дыхание от t."""
    kach = 2.2 * A.w(t, 4.6, ph)
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({kach:.2f}) scale({s_:.3f})">'
    g += f'<path d="M0,0 q{dl*.5:.0f},{26*vniz:.0f} {dl:.0f},{54*vniz:.0f}" fill="none" stroke="#3a2a1c" stroke-width="18"/>'
    n = 30
    for i in range(n):
        u = (i + .5) / n
        bx = dl * u
        by = 26 * vniz * u + 28 * vniz * u * u
        ln = ((210 - 96 * u) * (.72 + .5 * ((i * 7) % 5) / 4.0)
              * (1 + .1 * A.w(t, 3.2, ph + i * .11)))
        for sgn in (-1, 1):
            c = ob.HVOYA if (i + (sgn > 0)) % 2 == 0 else ob.HVOYA2
            # игла уходит НАЗАД и вбок, иначе лапа читается гребёнкой
            g += (f'<path d="M{bx:.0f},{by:.0f} q{-ln*.4:.0f},{sgn*ln*.18:.0f}'
                  f' {-ln*.78:.0f},{sgn*ln*.54:.0f}" fill="none" stroke="{c}"'
                  f' stroke-width="14" stroke-linecap="round"/>')
    g += (f'<path d="M0,0 q{dl*.5:.0f},{26*vniz:.0f} {dl:.0f},{54*vniz:.0f}" fill="none"'
          f' stroke="#4a3626" stroke-width="10"/>')
    return g + "</g>"


def skatert_lozhitsya_na_stol(t):
    """Комната под абажуром, белая скатерть парусом садится на раздвинутый стол.
    Живое: скатерть летит и садится, складки расправляются, абажур покачивается."""
    p = A.out(A.seg(t, .20, 1.80))
    s = SL(Z_NEBO, b5_stena(t, 820, 430, "#2c3650", "#171d2b", 900)
           + ob.girlyanda(-60, 150, 1980, 196, t, 16, 120))
    dal = okno_izby(1430, 250, 330, 290, t, vid=b5_za_oknom(1430, 250, 330, 290, t),
                    moroz=.45, krest=True)
    dal += ob.elka(300, 1010, 470, t, seed=6)
    dal += b5_stul(540, 1010, t, .62) + b5_stul(1380, 1010, t, .62)
    s += SL(Z_DAL, dal)
    # стол раздвинут: видно вставную доску посередине
    sred = ten(960, 1066, 800, 46, .55)
    sred += (f'<path d="M420,640 L1500,640 L1760,790 L160,790 Z" fill="url(#derev)" {o(7)}/>')
    sred += (f'<rect x="160" y="780" width="1600" height="46" rx="14" fill="url(#derev)" {o(7)}/>')
    sred += '<path d="M930,642 L1010,642 L1016,788 L924,788 Z" fill="#6d4423" opacity=".5"/>'
    for xx in (268, 1584):
        sred += f'<rect x="{xx}" y="826" width="46" height="240" fill="url(#derev)" {o(6)}/>'

    s += SL(Z_SRED, sred)
    # ПАРУС: верх держится, низ полощет; к p=1 скатерть ложится на столешницу
    x0, w0 = 150, 1620
    y0 = 250 + (660 - 250) * p
    amp = 150 * (1 - p) + 11
    verh, niz = [], []
    for i in range(8):
        u = i / 7.0
        verh.append((x0 + w0 * u, y0 + 38 * math.sin(math.pi * u) * (1 - p)))
        niz.append((x0 + w0 * (1 - u),
                    y0 + 130 + 190 * (1 - p) + amp * A.w(t, 1.0 + .8 * p, (1 - u) * 1.7)))
    d = b5_gladko(verh) + " " + b5_gladko(niz)[1:] + " Z"
    per = ten(960, 1032, 700 * (.4 + .6 * p), 30, .4 * p)
    per += f'<path d="{d}" fill="url(#rush)" {o(6)} opacity=".98"/>'
    for i in range(1, 7):
        u = i / 7.0
        vx, vy = verh[i]
        per += (f'<path d="M{vx:.0f},{vy:.0f} q{26*(1-p)*A.w(t,1.6,u):.0f},'
                f'{(130 + 190*(1-p))*.5:.0f} {10*(1-p)*A.w(t,1.2,u):.0f},'
                f'{130 + 190*(1-p):.0f}" fill="none" stroke="#d8c7a2"'
                f' stroke-width="{4 + 5*(1-p):.0f}" opacity="{.35 + .4*(1-p):.2f}"/>')
    per += (f'<path d="{b5_gladko([(px, py - 30) for px, py in niz])}" fill="none"'
            f' stroke="{ob.ALYJ}" stroke-width="9" opacity=".7" stroke-linecap="round"/>')
    per += baza.lampa(820, 430, t, 1.35, True)
    s += SL(Z_PERED, per)
    s += vinetka(.4)
    return s


def dva_blyuda_mandariny_i_pelmeni(t):
    """Два блюда на скатерти: горка мандаринов и дымящиеся пельмени.
    Живое: пар от пельменей, листик качается, вилки тянутся к блюду."""
    s = SL(Z_NEBO, b5_stena(t, 960, 420, "#2e3850", "#191f2d", 980)
           + ob.girlyanda(-60, 130, 1980, 170, t, 18, 100))
    s += SL(Z_DAL, ob.elka(1700, 1030, 540, t, seed=9)
            + okno_izby(90, 200, 300, 270, t, vid=b5_za_oknom(90, 200, 300, 270, t), moroz=.4))
    s += SL(Z_SRED, b5_skatert(60, 700, 1800, t, 150))
    # ГОРКА МАНДАРИНОВ слева — пятна цвета, никаких долек
    gor = ""
    for i, (dx, dy, sc) in enumerate(((-150, 10, 1.5), (-40, 18, 1.6), (72, 8, 1.5),
                                      (-96, -58, 1.5), (14, -52, 1.6), (-42, -116, 1.5))):
        gor += ob.mandarin(430 + dx, 672 + dy, sc, 0.0, t)
    # листик на верхнем мандарине качается
    kch = 11 * A.w(t, 2.0)
    gor += (f'<g transform="translate(388,560) rotate({kch:.1f})">'
            f'<path d="M0,0 q46,-34 96,-10 q-40,40 -96,10 z" fill="#5f8a3e" {o(5)}/>'
            f'<path d="M4,-2 q44,-20 86,-6" fill="none" stroke="#8fb866" stroke-width="5"/></g>')
    # БЛЮДО ПЕЛЬМЕНЕЙ справа
    pel = b5_blyudo(1360, 690, 250, t, "url(#krem)")
    r = random.Random(4)
    for i in range(11):
        a = i * 2.39996
        rr = 160 * math.sqrt((i + .6) / 11.0)
        pel += b5_pelmen(1360 + math.cos(a) * rr, 668 + math.sin(a) * rr * .36,
                       1.25, r.uniform(-26, 26))
    pel += baza.par(1300, 600, t, 5, .72, 280, .38, 1.5)
    pel += baza.par(1420, 610, t, 4, .66, 250, .32, 1.3)
    pel += b5_drozh(1240, 590, 240, t, 4, 170, .3)
    s += SL(Z_PERED, gor + pel)
    # ЧЕТЫРЕ ВИЛКИ тянутся к блюду с четырёх сторон (рukи не рисуем)
    vil = ""
    for i, (vx, vy, a, t0) in enumerate(((1910, 686, 180, .5), (820, 700, 0, 1.0),
                                         (1120, 1000, -36, 1.5), (1620, 404, 148, 2.0))):
        k = A.ease(A.seg(t, t0, 1.5))
        dxp = (1360 - vx) * .46 * k
        dyp = (690 - vy) * .46 * k
        vil += b5_vilka(vx + dxp, vy + dyp, a, 1.5, .8 + .2 * k)
    s += SL(Z_LETIT, vil)
    s += vinetka(.38)
    return s


def mandarin_v_detskih_rukah(t):
    """Крупно мандарин над вязаными рukавами: кожура сходит одной спиралью.
    Живое: спираль кожуры растёт, капли сока летят, дольки раскрываются."""
    p = A.ease(A.seg(t, .35, 2.6))
    s = SL(Z_NEBO, b5_stena(t, 400, 520, "#2a3348", "#171d29", 780))
    # тёплое боке гирлянды на фоне
    bok = ""
    r = random.Random(13)
    for i in range(14):
        bx, by = r.uniform(20, BAND), r.uniform(80, 560)
        gor = .25 + .5 * abs(A.w(t, 2.6 + r.uniform(0, 2), i * .17))
        col = (SVET, ob.ALYJ, ob.ZOLOTO, "#8fd6ff")[i % 4]
        bok += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r.uniform(22,54):.0f}"'
                f' fill="{col}" opacity="{gor*.3:.2f}"/>')
    s += SL(Z_DAL, bok + f'<rect y="900" width="{BAND}" height="180" fill="#3a2b22" opacity=".8"/>')
    # вязаные рukава: манжеты, без ладоней
    muf = ""
    for i, (mx, col) in enumerate(((190, ob.ALYJ), (640, "#2f5a78"))):
        kch = 3.4 * A.w(t, 3.0, i * .4)
        muf += (f'<g transform="translate({mx:.0f},{896 + kch:.0f})">'
                f'{ten(0, 150, 230, 38, .55)}'
                f'<rect x="-210" y="-10" width="420" height="200" rx="46" fill="{col}" {o(8)}/>')
        for k in range(13):
            muf += (f'<path d="M{-186 + k*31:.0f},-4 q14,70 0,146" fill="none"'
                    f' stroke="#ffffff" stroke-width="9" opacity=".2"/>')
        muf += (f'<rect x="-218" y="-44" width="436" height="56" rx="28" fill="{col}"'
                f' {o(7)} opacity=".96"/>'
                f'<rect x="-200" y="-34" width="400" height="14" rx="7" fill="#ffffff"'
                f' opacity=".18"/></g>')
    s += SL(Z_SRED, muf)
    # МАНДАРИН: шар, спираль кожуры, раскрытые дольки
    cx, cy, R = 408, 630, 168
    man = ten(cx, cy + R + 34, R * .9, 30, .55)
    man += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{ob.MANDA}" {o(9)}/>'
    man += f'<circle cx="{cx - R*.34:.0f}" cy="{cy - R*.36:.0f}" r="{R*.3:.0f}" fill="#ffc98a" opacity=".6"/>'
    # ОТКРЫТАЯ МЯКОТЬ: светлее кожуры, дольки расходятся лучами
    man += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R*.80:.0f}" fill="#fbb962"'
            f' opacity="{min(1.0, p*1.4):.2f}"/>')
    for i in range(9):
        a = -math.pi / 2 + i * (2 * math.pi / 9)
        man += (f'<path d="M{cx:.0f},{cy:.0f} L{cx + math.cos(a)*R*.78:.0f},'
                f'{cy + math.sin(a)*R*.78:.0f}" stroke="#f6e2bd" stroke-width="9"'
                f' stroke-linecap="round" opacity="{min(1.0, p*1.4)*.9:.2f}"/>')
    man += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R*.16:.0f}" fill="#f6e2bd"'
            f' opacity="{min(1.0, p*1.4)*.9:.2f}"/>')
    # две дольки отходят в сторону — «дольки раскрываются»
    for i, (dax, day) in enumerate(((-1.42, .72), (-1.05, 1.18))):
        raz = p * 200
        man += (f'<g transform="translate({cx + dax*raz:.0f},{cy + day*raz:.0f})'
                f' rotate({16 + i*26:.0f})" opacity="{min(1.0, p*1.5):.2f}">'
                f'<path d="M0,0 q{R*.5:.0f},{-R*.3:.0f} {R*.74:.0f},{R*.06:.0f}'
                f' q{-R*.3:.0f},{R*.4:.0f} {-R*.74:.0f},{-R*.06:.0f} z" fill="#fbb962" {o(5)}/>'
                f'<path d="M{R*.08:.0f},{R*.02:.0f} q{R*.38:.0f},{-R*.2:.0f} {R*.6:.0f},{R*.03:.0f}"'
                f' fill="none" stroke="#f6e2bd" stroke-width="7"/></g>')
    man += (f'<path d="M{cx:.0f},{cy-R:.0f} q16,-26 44,-22" fill="none"'
            f' stroke="{ZEL}" stroke-width="12" stroke-linecap="round"/>')
    # СПИРАЛЬ КОЖУРЫ — одной лентой свисает справа, длина растёт от t
    sp = []
    N = 52
    sx, sy = cx + R * 1.05, cy - R * .34
    for i in range(N + 1):
        u = (i / N) * p
        a = -1.4 + u * 8.4
        rr = 30 + u * 72
        sp.append((sx + math.cos(a) * rr, sy + math.sin(a) * rr * .52 + u * 300))
    if p > .03:
        man += (f'<path d="{b5_gladko(sp)}" fill="none" stroke="{ob.MANDA}"'
                f' stroke-width="40" stroke-linecap="round"/>')
        man += (f'<path d="{b5_gladko(sp)}" fill="none" stroke="#fff0dc"'
                f' stroke-width="14" stroke-linecap="round" opacity=".5"/>')
        man += (f'<circle cx="{sp[-1][0]:.0f}" cy="{sp[-1][1]:.0f}" r="22"'
                f' fill="{ob.MANDA}" {o(5)}/>')
    s += SL(Z_PERED, man)
    # КАПЛИ СОКА
    kap = ""
    rr = random.Random(5)
    for i in range(16):
        ph = rr.random()
        u = ((t * .9 + ph) % 1.0)
        a = rr.uniform(-2.6, .4)
        d = 60 + u * 300
        kap += (f'<ellipse cx="{cx + math.cos(a)*d:.0f}" cy="{cy + math.sin(a)*d + u*u*160:.0f}"'
                f' rx="{7*(1-u*.5):.1f}" ry="{11*(1-u*.5):.1f}" fill="#ffd089"'
                f' opacity="{(1-u)*.85:.2f}"/>')
    s += SL(Z_LETIT, kap)
    s += vinetka(.44)
    return s


def zapah_idet_po_komnatam(t):
    """Дом в разрезе, четыре комнаты: оранжевая струйка запаха идёт из кухни.
    Живое: струйка плывёт, дед поднимает нос и кот просыпается, малыш бежит."""
    s = SL(Z_NEBO, nebo("noch", t) + sneg_letit(t, 44))
    x0, y0, x1, y1 = 150, 220, 1770, 985
    cw, ch = (x1 - x0) / 2.0, (y1 - y0) / 2.0
    dal = (f'<path d="M{x0-70:.0f},{y0:.0f} L{(x0+x1)/2:.0f},{y0-220:.0f}'
           f' L{x1+70:.0f},{y0:.0f} Z" fill="{DOSKA2}" {o(7)}/>')
    dal += (f'<path d="M{x0-80:.0f},{y0+8:.0f} L{(x0+x1)/2:.0f},{y0-228:.0f}'
            f' L{x1+80:.0f},{y0+8:.0f} l-34,-26 L{(x0+x1)/2:.0f},{y0-196:.0f}'
            f' l{-(x1-x0)/2-46:.0f},0 Z" fill="url(#sneg)" {o(5)}/>')
    dal += f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1-x0:.0f}" height="{y1-y0:.0f}" fill="#2a2a38" {o(8)}/>'
    s += SL(Z_DAL, dal)
    # четыре комнаты
    kom = ""
    for r_ in range(2):
        for c in range(2):
            kx, ky = x0 + c * cw, y0 + r_ * ch
            tep = (r_ == 1 and c == 0)
            kom += (f'<rect x="{kx+10:.0f}" y="{ky+10:.0f}" width="{cw-20:.0f}"'
                    f' height="{ch-20:.0f}" rx="10" fill="{"#4a3a2c" if tep else "#38404f"}"/>')
            kom += (f'<rect x="{kx+10:.0f}" y="{ky+ch-70:.0f}" width="{cw-20:.0f}"'
                    f' height="60" fill="url(#pol)" opacity=".9"/>')
            kom += f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{cw:.0f}" height="{ch:.0f}" fill="none" {o(8)}/>'
    # КУХНЯ (низ слева): плита, кастрюля, пар
    kx, ky = x0, y0 + ch
    kom += teplo(kx + cw * .5, ky + ch * .55, 420, 340, .75)
    kom += (f'<rect x="{kx+120:.0f}" y="{ky+ch-230:.0f}" width="300" height="170" rx="12"'
            f' fill="url(#zhel)" {o(6)}/>')
    kom += (f'<ellipse cx="{kx+270:.0f}" cy="{ky+ch-238:.0f}" rx="94" ry="34"'
            f' fill="url(#chug)" {o(6)}/>')
    kom += baza.par(kx + 270, ky + ch - 266, t, 5, .55, 210, .4, 1.3)
    kom += (f'<rect x="{kx+470:.0f}" y="{ky+ch-300:.0f}" width="200" height="22" rx="8"'
            f' fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        kom += b5_banka(kx + 510 + i * 66, ky + ch - 300, 52, 78, t, (ob.ALYJ2, "#6f8c4a", CHAY)[i], i * .3)
    # ДЕД с газетой (верх слева) — поднимает нос
    nos = -9 * A.ease(A.seg(t, .5, .9))
    dx, dy = x0 + cw * .54, y0 + ch - 70
    kom += (f'<g transform="rotate({nos:.1f} {dx:.0f} {dy:.0f})">'
            + ob.figura(dx, dy, 330, t, "#2a2430", "#f0c070", False, .1, True) + '</g>')
    kom += (f'<rect x="{dx-240:.0f}" y="{dy-186:.0f}" width="206" height="150" rx="8"'
            f' fill="#e7e2d4" {o(5)} transform="rotate(-14 {dx-140:.0f} {dy-110:.0f})"/>')
    kom += (f'<path d="M{dx-224:.0f},{dy-152:.0f} h164 M{dx-226:.0f},{dy-124:.0f} h136'
            f' M{dx-228:.0f},{dy-96:.0f} h158" stroke="#8c8778" stroke-width="7" opacity=".6"/>')
    kom += b5_stul(dx + 100, dy, t, .54)
    # КОТ (верх справа) — просыпается
    kom += baza.kot(x0 + cw * 1.5, y0 + ch - 80, t, 1.0, "#3b3430", spit=(t < 1.1))
    kom += (f'<rect x="{x0+cw*1.18:.0f}" y="{y0+ch-150:.0f}" width="360" height="70"'
            f' rx="22" fill="{TKAN2}" {o(6)}/>')
    # МАЛЫШ (низ справа) — бежит на кухню
    beg = A.ease(A.seg(t, .55, 1.6))
    mx = x0 + cw * 1.78 - 430 * beg
    kom += ob.figura(mx, y1 - 60 + 8 * A.w(t, .32), 310, t, "#2b2436", "#ffd79a",
                     False, .3, True, 1.0, True)
    s += SL(Z_SRED, kom)
    # СТРУЙКА ЗАПАХА — из кухни через все комнаты
    put = [(x0 + 270, y0 + ch + ch - 300), (x0 + 300, y0 + ch - 60),
           (x0 + 420, y0 + ch * .5), (x0 + cw * .9, y0 + 150),
           (x0 + cw * 1.3, y0 + 180), (x0 + cw * 1.62, y0 + ch * .8),
           (x0 + cw * 1.5, y0 + ch + 140), (x0 + cw * 1.62, y1 - 160)]
    zap = (f'<path d="{b5_gladko(put)}" fill="none" stroke="{ob.MANDA}" stroke-width="22"'
           f' stroke-linecap="round" opacity=".5" stroke-dasharray="58 42"'
           f' stroke-dashoffset="{-t*190:.0f}"/>')
    zap += (f'<path d="{b5_gladko(put)}" fill="none" stroke="{SVET}" stroke-width="9"'
            f' stroke-linecap="round" opacity=".55" stroke-dasharray="30 70"'
            f' stroke-dashoffset="{-t*190:.0f}"/>')
    for i in range(7):
        u = ((t * .34 + i / 7.0) % 1.0)
        px, py = b5_tochka_lomanoy(put, u)
        zap += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{16 + 12*math.sin(math.pi*u):.0f}"'
                f' fill="{ob.MANDA}" opacity="{.5*(1-abs(2*u-1))+.15:.2f}"/>')
    s += SL(Z_PERED, zap + ramka_pp("oba", "#0b0d14", .55).replace("<g data-z=\"-230\">", "").replace("</g><!--/z-->", ""))
    s += vinetka(.42)
    return s


def kozhura_na_bataree(t):
    """Мандарины ложатся в варежки, камера уходит к батарее с сохнущей кожурой.
    Живое: мандарины падают в варежки, кожура загибается, над батареей дрожит воздух."""
    s = SL(Z_NEBO, b5_stena(t, 1380, 560, "#2d3750", "#181e2c", 900))
    dal = okno_izby(1130, 150, 520, 420, t, vid=b5_za_oknom(1130, 150, 520, 420, t),
                    moroz=.55)
    dal += ob.girlyanda(1050, 96, 1760, 112, t, 11, 64)
    s += SL(Z_DAL, dal)
    # ЧУГУННАЯ БАТАРЕЯ под окном
    bat = ten(1390, 960, 300, 28, .5)
    for i in range(9):
        bx = 1130 + i * 58
        bat += (f'<rect x="{bx:.0f}" y="640" width="44" height="282" rx="20"'
                f' fill="url(#chug)" {o(6)}/>')
        bat += f'<rect x="{bx+8:.0f}" y="660" width="10" height="240" rx="5" fill="#8f949a" opacity=".3"/>'
    bat += f'<rect x="1120" y="690" width="546" height="22" rx="10" fill="url(#zhel)" {o(5)}/>'
    bat += f'<rect x="1120" y="846" width="546" height="22" rx="10" fill="url(#zhel)" {o(5)}/>'
    bat += teplo(1390, 700, 420, 300, .5)
    # кожура на батарее — подсыхает и загибается
    zag = A.ease(A.seg(t, .4, 3.4))
    for i, bx in enumerate((1180, 1286, 1392, 1498, 1604)):
        bat += b5_kozhura(bx, 630, -14 + i * 7, .82, zag * (.5 + .12 * i))
    bat += b5_drozh(1140, 606, 520, t, 6, 230, .34)
    s += SL(Z_SRED, bat)
    # ДВЕ ВАРЕЖКИ на табурете, в них падают по два мандарина
    per = ten(470, 1000, 440, 34, .5)
    per += (f'<path d="M140,790 L800,790 L880,900 L60,900 Z" fill="url(#derev)" {o(7)}/>'
            f'<rect x="60" y="890" width="820" height="40" rx="14" fill="url(#derev)" {o(7)}/>'
            f'<rect x="80" y="898" width="780" height="12" rx="6" fill="#ffffff" opacity=".25"/>')
    for xx in (180, 700):
        per += f'<rect x="{xx}" y="930" width="40" height="150" fill="url(#derev)" {o(6)}/>'
    per += b5_rukavichka(260, 836, 1.35, ob.ALYJ, t, 0.0)
    per += b5_rukavichka(680, 842, 1.35, "#2f5a78", t, .3)
    for i, (mx, my, t0) in enumerate(((208, 756, .25), (310, 770, .75),
                                      (628, 760, 1.25), (734, 776, 1.75))):
        k = A.out(A.seg(t, t0, .85))
        if k <= .01:
            continue
        y = -220 + (my + 220) * k
        per += ob.mandarin(mx, y, 1.7, 0.0, t)
    per += b5_muka(220, 790, 560, t, 8, 9, 90, .4, .16)
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def vaza_s_mandarinami(t):
    """Дверца холодильника закрывается, мандарины катятся в стеклянную вазу.
    Живое: мандарины катятся, дверца закрывается, ваза встаёт на скатерть."""
    zak = A.ease(A.seg(t, .15, 1.2))
    s = SL(Z_NEBO, b5_stena(t, 480, 520, "#2b3449", "#171d2a", 820))
    # ХОЛОДИЛЬНИК слева, дверца закрывается
    hol = ten(180, 980, 150, 26, .5)
    hol += f'<rect x="40" y="200" width="300" height="760" rx="22" fill="#2b3340" {o(7)}/>'
    hol += (f'<rect x="64" y="226" width="252" height="296" rx="12" fill="#3a4654" {o(4)}/>'
            f'<rect x="64" y="542" width="252" height="392" rx="12" fill="#3a4654" {o(4)}/>')
    for i in range(3):
        hol += b5_banka(132 + i * 62, 500, 48, 74, t, (ob.ALYJ2, "#6f8c4a", CHAY)[i], i * .3, True)
    hol += teplo(190, 560, 230, 330, .55 * (1 - zak))
    hol += (f'<g transform="translate(40,200) scale({1-zak*.78:.3f},1)">'
            f'<rect width="300" height="760" rx="22" fill="url(#beton)" {o(7)}/>'
            f'<rect x="24" y="24" width="252" height="300" rx="14" fill="#b5bec4" opacity=".6"/>'
            f'<rect x="252" y="330" width="22" height="200" rx="11" fill="url(#zhel)" {o(4)}/>'
            f'<rect x="30" y="30" width="20" height="690" rx="10" fill="#ffffff" opacity=".3"/></g>')
    s += SL(Z_DAL, hol + ob.girlyanda(-40, 120, 860, 150, t, 9, 70))
    s += SL(Z_SRED, b5_skatert(50, 740, 760, t, 160, gl=112))
    # ВАЗА НА НОЖКЕ встаёт в середину стола
    vst = A.over(A.seg(t, 1.0, 1.1))
    vx, vy = 560, 730
    vaz = (f'<g transform="translate({vx:.0f},{vy - 300*(1-vst):.0f})'
           f' scale({1.12 + .14*vst:.3f})">')
    vaz += ten(0, 36, 150, 26, .5)
    vaz += '<path d="M-150,-170 q22,118 150,142 q128,-24 150,-142 z" fill="url(#stekl)" opacity=".62" stroke="#d6e8f2" stroke-width="6"/>'
    vaz += '<path d="M0,-28 v54" fill="none" stroke="#cfe3ef" stroke-width="22"/>'
    vaz += '<path d="M-96,30 q96,26 192,0 q-96,16 -192,0 z" fill="#cfe3ef" stroke="#b7d2e2" stroke-width="5"/>'
    # мандарины, уже лежащие в вазе
    for i, (dx, dy) in enumerate(((-78, -122), (-6, -112), (66, -124), (-40, -186), (36, -192))):
        kk = A.out(A.seg(t, 1.5 + i * .33, .55))
        if kk > .02:
            vaz += (f'<g opacity="{kk:.2f}" transform="translate({dx},{dy - 70*(1-kk):.0f})">'
                    + ob.mandarin(0, 0, 1.25, 0.0, t) + '</g>')
    vaz += '<path d="M-130,-150 q16,96 76,126" fill="none" stroke="#ffffff" stroke-width="12" opacity=".4"/>'
    vaz += '</g>'
    # мандарины КАТЯТСЯ по столу от холодильника к вазе
    kat = ""
    for i, t0 in enumerate((.3, .62, .94)):
        k = A.ease(A.seg(t, t0, 1.25))
        if k <= .01 or k >= .999:
            continue
        mx = 120 + (vx - 150 - 120) * k
        my = 706 - 26 * math.sin(math.pi * k)
        kat += (f'<g transform="rotate({k*420:.0f} {mx:.0f} {my:.0f})">'
                + ob.mandarin(mx, my, 1.3, 0.0, t) + '</g>')
    s += SL(Z_PERED, vaz + kat + baza.svecha(760, 640, t, .2, 1.0, 96))
    s += vinetka(.42)
    return s


def semya_lepit_pelmeni(t):
    """Большой кухонный стол в мukе, вокруг вся семья: дед, мать, отец и двое детей.
    Живое: мukа летит, пельмени ложатся на доску, фигуры покачиваются."""
    s = SL(Z_NEBO, b5_stena(t, 960, 380, "#2f3950", "#1a202e", 1000)
           + baza.lampa(960, 330, t, 1.1, True))
    dal = ob.figura(430, 740, 620, t, "#2a2432", "#f3c884", False, .0, False)
    dal += ob.figura(760, 730, 600, t, "#31273a", "#ffd79a", True, .3, False)
    dal += ob.figura(1240, 742, 630, t, "#262031", "#f0c070", False, .6, False)
    dal += b5_muka(420, 640, 900, t, 14, 21, 140, .5, .35)
    s += SL(Z_DAL, dal)
    # СТОЛ в мukе
    sred = ten(960, 1030, 820, 46, .55)
    sred += (f'<path d="M330,580 L1590,580 L1810,700 L110,700 Z" fill="url(#derev)" {o(7)}/>')
    sred += (f'<path d="M330,580 L1590,580 L1810,700 L110,700 Z" fill="{MUKA}" opacity=".42"/>')
    sred += f'<rect x="110" y="700" width="1700" height="46" rx="14" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="110" y="700" width="1700" height="18" rx="9" fill="{MUKA}" opacity=".75"/>'
    for xx in (210, 1640):
        sred += f'<rect x="{xx}" y="746" width="44" height="290" fill="url(#derev)" {o(6)}/>'
    r = random.Random(7)
    for i in range(16):
        sred += (f'<ellipse cx="{r.uniform(150, 1760):.0f}" cy="{r.uniform(690, 712):.0f}"'
                 f' rx="{r.uniform(24, 70):.0f}" ry="{r.uniform(5, 11):.0f}" fill="{MUKA}"'
                 f' opacity="{r.uniform(.35, .8):.2f}"/>')
    # кружочки теста
    for i, dx in enumerate((300, 420, 1420, 1540)):
        sred += (f'<ellipse cx="{dx}" cy="686" rx="54" ry="19" fill="{TESTO}" {o(5)}/>'
                 f'<ellipse cx="{dx-16}" cy="680" rx="22" ry="7" fill="#f6e9c8" opacity=".6"/>')
    # скалка
    sred += (f'<rect x="1560" y="664" width="230" height="30" rx="15" fill="url(#derev)" {o(5)}/>'
             f'<rect x="1532" y="672" width="40" height="14" rx="7" fill="url(#derev)" {o(4)}/>'
             f'<rect x="1778" y="672" width="40" height="14" rx="7" fill="url(#derev)" {o(4)}/>')
    # ДОСКА с пельменями — ложатся по одному
    sred += f'<rect x="700" y="640" width="520" height="68" rx="14" fill="url(#dosk)" {o(6)}/>'
    for i in range(14):
        k = A.over(A.seg(t, .18 + i * .11, .42))
        if k <= .02:
            continue
        px = 740 + (i % 7) * 68
        py = 660 + (i // 7) * 32
        sred += (f'<g transform="translate(0,{-90*(1-k):.0f})" opacity="{min(1.0,k):.2f}">'
                 + b5_pelmen(px, py, .78, -18 + (i * 29) % 36) + '</g>')
    s += SL(Z_SRED, sred)
    # ПЕРЕДНИЙ ПЛАН: отец и двое детей спиной, срезаны нижним краем
    per = ob.figura(250, 1480, 1020, t, "#191520", "#f6cf8a", False, .15, False)
    per += ob.figura(1700, 1460, 990, t, "#1c1724", "#ffd79a", False, .45, False)
    per += ob.figura(1000, 1520, 760, t, "#20192a", "#ffd79a", False, .7, False, 1.0, True)
    per += b5_muka(260, 760, 1400, t, 22, 5, 240, .6, .55)
    s += SL(Z_PERED, per)
    s += vinetka(.44)
    return s


def doska_s_pelmenyami_na_moroze(t):
    """Кадр надвое: балкон многоэтажки и крыльцо дома, на обоих — доска пельменей.
    Живое: доски ставят разом, пельмени белеют инеем, пар изо рта."""
    stav = A.out(A.seg(t, .2, 1.0))
    iney = A.ease(A.seg(t, 1.3, 2.6))
    s = SL(Z_NEBO, nebo("noch", t) + sneg_letit(t, 52))
    dal = panelka(-120, 1080, 900, t, 6, True, 4).replace('<g data-z="520">', '').replace('</g><!--/z-->', '')
    dal += ulica_dal(990, 880, 900, t, True, 11).replace('<g data-z="520">', '').replace('</g><!--/z-->', '')
    dal += baza.izba_snaruzhi(1180, 900, 520, t, True, True, 3)
    s += SL(Z_DAL, dal)
    # ЛЕВО — балкон многоэтажки
    lev = f'<rect x="0" y="300" width="950" height="780" fill="url(#beton)" opacity=".92" {o(6)}/>'
    lev += f'<rect x="0" y="300" width="950" height="40" fill="{BETON2}"/>'
    lev += okno_izby(90, 380, 300, 300, t, svet=True, moroz=.5, krest=True)
    lev += f'<rect x="0" y="880" width="950" height="40" rx="12" fill="url(#zhel)" {o(6)}/>'
    for i in range(9):
        lev += f'<rect x="{30 + i*104:.0f}" y="900" width="18" height="180" rx="8" fill="url(#zhel)" {o(4)}/>'
    lev += sneg_lezhit(1004, 18).replace('<g data-z="520">', '').replace('</g><!--/z-->', '')
    lev += teplo(240, 530, 420, 340, .5)
    lev += b5_stul(560, 1010, t, .74, False)
    lev += (f'<path d="M402,784 q88,-22 176,0 q-88,16 -176,0 z" fill="url(#sneg)" {o(4)}/>')
    for i in range(9):
        lev += (f'<ellipse cx="{36 + i*104:.0f}" cy="898" rx="22" ry="9"'
                f' fill="url(#sneg)" {o(3)}/>')
    # ПРАВО — крыльцо дома
    pra = f'<rect x="970" y="240" width="950" height="840" fill="url(#brev)" opacity=".2"/>'
    pra += brevna(970, 240, 950, 560, 92)
    pra += okno_izby(1560, 330, 290, 270, t, vid=b5_za_oknom(1560, 330, 290, 270, t, "#3c2a16"),
                     svet=True, moroz=.4)
    pra += baza.dver(1040, 380, 240, 420, .0, "url(#derev)", True)
    pra += f'<rect x="970" y="800" width="950" height="40" rx="10" fill="url(#dosk)" {o(6)}/>'
    pra += doski(970, 840, 950, 240, 72, True, "dosk")
    pra += f'<rect x="980" y="700" width="930" height="34" rx="16" fill="url(#derev)" {o(6)}/>'
    for i in range(6):
        pra += f'<rect x="{1040 + i*160:.0f}" y="734" width="20" height="108" rx="8" fill="url(#derev)" {o(4)}/>'
    s += SL(Z_SRED, lev + pra)
    # ДОСКИ с пельменями ставят разом
    per = ""
    for j, (bx, by) in enumerate(((330, 830), (1230, 672))):
        yy = by - 260 * (1 - stav)
        per += f'<g transform="translate(0,{yy - by:.0f})">'
        per += ten(bx + 190, by + 48, 210, 20, .5)
        per += f'<rect x="{bx:.0f}" y="{by:.0f}" width="400" height="56" rx="12" fill="url(#dosk)" {o(6)}/>'
        for i in range(12):
            px = bx + 44 + (i % 6) * 62
            py = by + 14 + (i // 6) * 26
            per += b5_pelmen(px, py, .72, -20 + (i * 37) % 40, iney)
        per += '</g>'
    # пар изо рта — у края каждой половины
    per += baza.par(690, 760, t, 4, .45, 190, .35, 1.2)
    per += baza.par(1030, 640, t, 4, .4, 180, .32, 1.1)
    per += f'<rect x="952" y="0" width="16" height="{H}" fill="#0b0f18" opacity=".85"/>'
    s += SL(Z_PERED, per)
    s += vinetka(.46)
    return s


def svobodnyy_stul_u_testa(t):
    """За столом в мukе свободный стул: он отодвигается, с сиденья взлетает мukа.
    Живое: стул отодвигается, мучное облачко от хлопка, кружочек теста ложится."""
    ot = A.out(A.seg(t, .25, 1.05))
    hlop = max(0.0, math.sin(math.pi * A.seg(t, 1.35, .55)))
    klad = A.over(A.seg(t, 1.9, .95))
    s = SL(Z_NEBO, b5_stena(t, 820, 430, "#2c3650", "#181e2c", 900)
           + baza.lampa(820, 300, t, 1.0, True))
    # дальняя сторона стола: тесто, скалка, миска
    dal = ""
    for i, dx in enumerate((420, 540, 1300, 1430, 1540)):
        dal += (f'<ellipse cx="{dx}" cy="596" rx="46" ry="16" fill="{TESTO}" {o(5)}/>'
                f'<ellipse cx="{dx-14}" cy="591" rx="19" ry="6" fill="#f6e9c8" opacity=".6"/>')
    dal += (f'<rect x="1480" y="562" width="210" height="28" rx="14" fill="url(#derev)" {o(5)}/>')
    dal += baza.krynka(380, 594, 1.05)
    dal += b5_muka(380, 580, 1200, t, 14, 31, 130, .45, .3)
    s += SL(Z_DAL, dal)
    # СТОЛ
    sred = ten(960, 1040, 800, 44, .55)
    sred += (f'<path d="M330,600 L1600,600 L1820,700 L120,700 Z" fill="url(#derev)" {o(7)}/>')
    sred += (f'<path d="M330,600 L1600,600 L1820,700 L120,700 Z" fill="{MUKA}" opacity=".42"/>')
    sred += f'<rect x="120" y="700" width="1700" height="46" rx="14" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="120" y="700" width="1700" height="18" rx="9" fill="{MUKA}" opacity=".8"/>'
    for xx in (220, 1650):
        sred += f'<rect x="{xx}" y="746" width="44" height="294" fill="url(#derev)" {o(6)}/>'
    r = random.Random(23)
    for i in range(14):
        sred += (f'<ellipse cx="{r.uniform(160, 1770):.0f}" cy="{r.uniform(690, 712):.0f}"'
                 f' rx="{r.uniform(26, 76):.0f}" ry="{r.uniform(5, 12):.0f}" fill="{MUKA}"'
                 f' opacity="{r.uniform(.3, .8):.2f}"/>')
    s += SL(Z_SRED, sred)
    # СВОБОДНЫЙ СТУЛ отодвигается, с сиденья бьёт мучное облачко
    per = b5_stul(860, 1046, t, .96, True, 180 * ot)
    cx = 860 + 180 * ot
    per += (f'<ellipse cx="{cx:.0f}" cy="{1046-222:.0f}" rx="{104 + 26*hlop:.0f}"'
            f' ry="{16 + 6*hlop:.0f}" fill="{MUKA}" opacity="{.35 + .45*hlop:.2f}"/>')
    per += b5_muka(cx - 120, 1046 - 226, 240, t, 16, 13, 230, 1.0, .55 * (.3 + .7 * hlop))
    # кружочек теста и ложка фарша перед стулом
    if klad > .02:
        ky = 672 - 150 * (1 - klad)
        per += (f'<g opacity="{min(1.0,klad):.2f}">'
                f'<ellipse cx="{cx:.0f}" cy="{ky:.0f}" rx="{72*klad:.0f}" ry="{26*klad:.0f}"'
                f' fill="{TESTO}" {o(6)}/>'
                f'<ellipse cx="{cx-20:.0f}" cy="{ky-7:.0f}" rx="{28*klad:.0f}"'
                f' ry="{9*klad:.0f}" fill="#f6e9c8" opacity=".6"/></g>')
        per += (f'<g transform="translate({cx+150:.0f},{672:.0f}) rotate(-14)">'
                f'{ten(0, 18, 60, 12, .45)}'
                f'<rect x="34" y="-10" width="190" height="20" rx="10" fill="url(#zhel)" {o(4)}/>'
                f'<ellipse rx="52" ry="26" fill="url(#zhel)" {o(5)}/>'
                f'<ellipse cx="0" cy="-4" rx="38" ry="17" fill="{FARSH}" {o(3)}/>'
                f'<ellipse cx="-14" cy="-10" rx="12" ry="5" fill="#c06a54" opacity=".7"/></g>')
    s += SL(Z_PERED, per)
    s += vinetka(.44)
    return s


def babushka_i_vnuki_v_muke(t):
    """Сегодняшняя кухня: бабушка и двое внukов, на доске три ровных ряда по десять.
    Живое: ряды пельменей растут, внuk сдувает мukу, бабушка поправляет пельмень."""
    s = SL(Z_NEBO, b5_stena(t, 400, 420, "#2e3850", "#1a202e", 860))
    # кухонный гарнитур слева, в полосе 0-830
    dal = f'<rect x="0" y="180" width="{BAND}" height="250" rx="14" fill="#5a4026" {o(6)}/>'
    for i in range(4):
        dal += (f'<rect x="{20 + i*200:.0f}" y="196" width="180" height="218" rx="10"'
                f' fill="url(#derev)" {o(5)}/>'
                f'<rect x="{34 + i*200:.0f}" y="210" width="152" height="60" rx="8"'
                f' fill="#ffffff" opacity=".12"/>'
                f'<rect x="{90 + i*200:.0f}" y="384" width="42" height="12" rx="6" fill="url(#zhel)"/>')
    dal += ob.girlyanda(-30, 110, 850, 140, t, 10, 60)
    s += SL(Z_DAL, dal)
    # БАБУШКА и ДВОЕ ВНУКОВ
    sred = ob.figura(210, 818, 470, t, "#2a2432", "#f3c884", True, .1, False)
    sred += ob.figura(470, 820, 300, t, "#272134", "#ffd79a", False, .45, True)
    sred += ob.figura(650, 822, 286, t, "#231e2e", "#ffd79a", False, .8, True, 1.0, True)
    # внuk сдувает мukу — облачко от его лица к доске
    sdu = max(0.0, math.sin(math.pi * ((t / 2.6) % 1.0))) ** 2
    sred += b5_muka(430, 700, 300, t, 14, 29, 200, .9, .5 * (.25 + .75 * sdu))
    sred += (f'<ellipse cx="520" cy="712" rx="{90*sdu + 20:.0f}" ry="{26*sdu + 8:.0f}"'
             f' fill="{MUKA}" opacity="{.5*sdu:.2f}"/>')
    s += SL(Z_SRED, sred)
    # ДОСКА: три ряда по десять
    per = ten(430, 1046, 390, 28, .55)
    per += (f'<path d="M50,812 L810,812 L860,1012 L0,1012 Z" fill="url(#dosk)" {o(7)}/>')
    per += (f'<path d="M52,818 L806,818" fill="none" stroke="{MUKA}" stroke-width="10" opacity=".55"/>')
    per += b5_muka(40, 1000, 820, t, 14, 3, 120, .5, .35)
    rost = A.seg(t, .15, 2.6)
    for row in range(3):
        for i in range(10):
            idx = row * 10 + i
            k = A.over(A.seg(t, .1 + idx * .055, .35))
            if k <= .02:
                continue
            sc = .62 + row * .07
            px = 86 + i * 72 + row * 10
            py = 856 + row * 62
            popr = 0.0
            if idx == 24:                       # бабушка поправляет один пельмень
                popr = 9 * A.w(t, 1.5)
            per += (f'<g transform="translate({popr:.1f},{-70*(1-k) + popr*.3:.1f})"'
                    f' opacity="{min(1.0,k):.2f}">'
                    + b5_pelmen(px, py, sc, -16 + (idx * 31) % 34) + '</g>')
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def stopka_zhurnalov(t):
    """Журнальный столик, стопка глянцевых журналов без названий; верхний раскрывается.
    Живое: журнал раскрывается, страницы идут веером, закладка выпадает."""
    otk = A.ease(A.seg(t, .35, 1.5))
    ver = A.seg(t, 1.3, 1.8)
    s = SL(Z_NEBO, b5_stena(t, 1500, 420, "#2a3348", "#171d2a", 880))
    dal = ob.elka(1640, 1020, 560, t, seed=12)
    dal += (f'<path d="M-60,1080 L-60,700 q30,-80 150,-80 h520 q70,0 70,80 v380 z"'
            f' fill="#3c4a63" {o(7)}/>')
    dal += (f'<rect x="-40" y="800" width="700" height="150" rx="34" fill="#4a5a76" {o(6)}/>')
    dal += (f'<rect x="-20" y="690" width="300" height="120" rx="26" fill="#55668a" {o(5)}/>'
            f'<rect x="300" y="690" width="300" height="120" rx="26" fill="#55668a" {o(5)}/>')
    dal += (f'<rect x="40" y="712" width="200" height="22" rx="11" fill="#ffffff" opacity=".14"/>')
    s += SL(Z_DAL, dal)
    # столик + стопка
    sred = ten(960, 1040, 460, 32, .55)
    sred += f'<rect x="500" y="790" width="920" height="34" rx="12" fill="url(#derev)" {o(7)}/>'
    for xx in (570, 1300):
        sred += f'<rect x="{xx}" y="824" width="36" height="216" fill="url(#derev)" {o(6)}/>'
    for i in range(5):
        sred += (f'<rect x="{540 + (i % 2)*16:.0f}" y="{770 - i*22:.0f}" width="760"'
                 f' height="24" rx="6" fill="{("#c2402c", "#2f5a78", "#d8a63a", "#3f6b4a", "#8d3a5e")[i]}"'
                 f' {o(5)}/>')
        sred += (f'<rect x="{546 + (i % 2)*16:.0f}" y="{772 - i*22:.0f}" width="748"'
                 f' height="7" rx="4" fill="#ffffff" opacity=".28"/>')
    s += SL(Z_SRED, sred)
    # ВЕРХНИЙ ЖУРНАЛ раскрывается сам
    bx, by = 920, 660
    per = ten(bx, by + 44, 420, 26, .5)
    per += (f'<rect x="{bx:.0f}" y="{by-14:.0f}" width="380" height="26" rx="6"'
            f' fill="#f3eee0" {o(5)}/>')
    # ОБЛОЖКА откидывается влево, под ней разворот двух страниц
    kr = max(.04, math.cos(math.pi * .92 * otk))
    per += (f'<g transform="translate({bx:.0f},{by:.0f}) scale({kr:.3f},1)">'
            f'<path d="M0,10 L-376,-14 L-376,-44 L0,-20 Z" fill="{ob.ALYJ}" {o(5)}/>'
            f'<path d="M-30,-18 L-352,-40" stroke="#ffffff" stroke-width="9" opacity=".3"/></g>')
    # РАЗВОРОТ: две страницы под углом, обе с полосами текста (без букв)
    for sgn in (-1, 1):
        per += (f'<path d="M0,0 L{sgn*372:.0f},{-34:.0f} L{sgn*366:.0f},{14:.0f} L0,{34:.0f} Z"'
                f' fill="#faf6ea" {o(5)} transform="translate({bx:.0f},{by-14:.0f})"/>')
        for i in range(5):
            per += (f'<path d="M{bx + sgn*60:.0f},{by - 26 + i*11:.0f}'
                    f' L{bx + sgn*(300 - i*34):.0f},{by - 46 + i*11:.0f}" stroke="#93a2b2"'
                    f' stroke-width="6" opacity=".7" stroke-linecap="round"/>')
    per += (f'<rect x="{bx-7:.0f}" y="{by-54:.0f}" width="14" height="92" rx="7"'
            f' fill="#e2dbc8" {o(4)}/>')
    # СТРАНИЦЫ ВЕЕРОМ: три листа в перевороте, выгнутые дугой
    for i in range(2):
        k = A.ease(A.seg(t, 1.1 + i * .7, 1.1))
        if k <= .02 or k >= .99:
            continue
        u = 1 - 2 * k
        per += (f'<path d="M{bx:.0f},{by-14:.0f} q{u*220:.0f},{-108 - 26*abs(u):.0f}'
                f' {u*372:.0f},{-34:.0f} q{-u*170:.0f},{40:.0f} {-u*372:.0f},{26:.0f} z"'
                f' fill="#fdfaf0" stroke="#cdc2a6" stroke-width="4" opacity=".9"/>')
    s += SL(Z_PERED, per)
    # ЗАКЛАДКА выпадает
    if ver > .01:
        zx = bx - 120 + 230 * ver
        zy = by + 20 + 420 * ver * ver
        s += SL(Z_LETIT, f'<g transform="translate({zx:.0f},{zy:.0f}) rotate({ver*300:.0f})">'
                f'<rect x="-14" y="-70" width="28" height="140" rx="8" fill="{ob.ZOLOTO}" {o(4)}/>'
                f'<path d="M-14,70 l14,-22 l14,22 z" fill="{ob.ZOLOTO2}"/></g>')
    s += vinetka(.44)
    return s


def hozyayka_goda_za_stolom(t):
    """Хозяйка года с салфеткой на шее: на столе по одному встают зелень,
    огурцы с редиской, сыр и молоко. Живое: она жуёт, угощения появляются, бубенчик качается."""
    s = SL(Z_NEBO, b5_stena(t, 380, 460, "#2c3650", "#181e2c", 860)
           + ob.girlyanda(-40, 120, 870, 150, t, 10, 70))
    dal = (f'<rect x="20" y="300" width="250" height="430" rx="12" fill="url(#derev)" {o(6)}/>'
           f'<rect x="40" y="326" width="210" height="180" rx="8" fill="url(#stekl)" opacity=".6" {o(4)}/>')
    for i in range(4):
        dal += b5_banka(72 + i * 52, 500, 44, 72, t, (ob.ALYJ2, "#6f8c4a", CHAY, "#7a4a2a")[i], i * .3, True)
    dal += baza.hodiki(170, 230, t, .7)
    s += SL(Z_DAL, dal)
    # ХОЗЯЙКА ГОДА за столом: ноги скрывает скатерть
    koz = ob.koza(286, 930, t, .80, 0.0, True, .0)
    # салфетка на шее — белый треугольник на груди
    koz += (f'<g transform="translate(404,734) rotate({2.4*A.w(t,2.4,.3):.1f})">'
            f'<path d="M-52,-26 q52,-22 104,0 l-24,112 q-28,14 -56,0 z" fill="#f6f2e4" {o(6)}/>'
            f'<path d="M-42,-12 q42,-16 84,0" fill="none" stroke="{ob.ALYJ}" stroke-width="7"/></g>')
    # петрушка во рту: жуёт
    zh = 6 * A.w(t, .72)
    koz += (f'<g transform="translate({516 + zh*.4:.0f},{618 + zh:.0f})">'
            + b5_zelen(0, 0, t, .5, 5, .6) + '</g>')
    s += SL(Z_SRED, koz)
    # СТОЛ ПЕРЕД НЕЙ + угощения по одному
    per = b5_skatert(-60, 826, 900, t, 180, gl=78)
    for i, (f, fx, t0) in enumerate(((0, 450, 1.1), (1, 580, 2.2), (2, 700, 3.4), (3, 806, 4.6))):
        k = A.over(A.seg(t, t0, .9))
        if k <= .02:
            continue
        if f == 0:
            per += b5_zelen(fx, 818, t, .88, 9, i * .2, None, k)
        elif f == 1:
            per += b5_ogurcy(fx, 818, .82, k)
        elif f == 2:
            per += b5_syr(fx, 818, .82, k)
        else:
            per += (f'<g opacity="{min(1.0,k):.2f}" transform="translate(0,{-120*(1-k):.0f})">'
                    + b5_kuvshin(fx, 818, .72) + '</g>')
    per += baza.svecha(110, 766, t, .4, 1.0, 100)
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def blyudo_pod_kryshkoy_unosyat(t):
    """Блюдо под блестящей крышкой уплывает на кухню, хозяйка года выдыхает.
    Живое: блюдо уплывает, из-под крышки идёт пар, хозяйка выдыхает."""
    p = A.ease(A.seg(t, .30, 2.40))
    s = SL(Z_NEBO, b5_stena(t, 1620, 520, "#2b3449", "#171d2a", 820))
    # дверь кухни справа, свет оттуда
    dal = f'<rect x="1430" y="210" width="360" height="760" rx="10" fill="#1b2029" {o(7)}/>'
    dal += (f'<rect x="1468" y="230" width="300" height="720" rx="8" fill="{SVET}"'
            f' opacity="{.42 + .1*abs(A.w(t, 4.0)):.2f}"/>')
    dal += baza.luch(1420, 210, 380, 870, t, .18)
    dal += baza.dver(1150, 240, 290, 720, .65, "url(#derev)", True)
    dal += teplo(1620, 560, 460, 480, .6)
    s += SL(Z_DAL, dal)
    # хозяйка года за столом слева, выдыхает
    sred = ob.koza(420, 946, t, .86, 0.0, True, .2)
    vyd = max(0.0, math.sin(math.pi * A.seg(t, 1.9, 1.0)))
    for i in range(4):
        u = ((t * .6 + i * .25) % 1.0)
        sred += (f'<ellipse cx="{792 + 150*u:.0f}" cy="{598 - 56*u:.0f}"'
                 f' rx="{20 + 64*u:.0f}" ry="{(20 + 64*u)*.6:.0f}" fill="#fbf4e4"'
                 f' opacity="{.7*vyd*(1-u)*(1-u):.2f}"/>')
    s += SL(Z_SRED, sred + b5_skatert(-40, 836, 940, t, 170, gl=78))
    # БЛЮДО ПОД КРЫШКОЙ уплывает к двери (прихватки — не рukи)
    bx = 700 + 700 * p
    by = 690 - 70 * math.sin(math.pi * p)
    per = f'<g transform="translate({bx:.0f},{by:.0f}) scale({1 - .22*p:.3f})">'
    per += ten(0, 96, 190, 28, .5)
    per += b5_blyudo(0, 60, 196, t, "url(#krem)")
    per += (f'<path d="M-178,56 q14,-146 178,-150 q164,4 178,150 q-178,44 -356,0 z"'
            f' fill="url(#zhel)" {o(7)}/>')
    per += '<path d="M-130,10 q80,-96 190,-70" fill="none" stroke="#ffffff" stroke-width="22" opacity=".45"/>'
    per += f'<circle cx="0" cy="-104" r="26" fill="url(#zol)" {o(5)}/>'
    for sgn in (-1, 1):
        per += (f'<path d="M{sgn*174:.0f},54 q{sgn*62:.0f},-6 {sgn*70:.0f},50'
                f' q{-sgn*10:.0f},44 {-sgn*66:.0f},36 z" fill="{ob.ALYJ}" {o(6)}/>')
        for k in range(3):
            per += (f'<path d="M{sgn*(182 + k*18):.0f},58 v70" fill="none"'
                    f' stroke="#ffffff" stroke-width="5" opacity=".22"/>')
    per += '</g>'
    per += baza.par(bx - 110, by - 54, t, 5, .5, 240, .4, 1.3)
    per += baza.par(bx + 110, by - 48, t, 4, .45, 220, .34, 1.2)
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def babushkin_nakrytyy_stol(t):
    """Раздвинутый стол под ковром на стене, заставлен посудой без просвета;
    бабушка со спины ставит последнюю вазочку. Живое: вазочка встаёт, графин
    поблёскивает, от миски идёт пар."""
    vst = A.over(A.seg(t, .7, 1.1))
    s = SL(Z_NEBO, b5_stena(t, 1100, 380, "#2b3449", "#171d2a", 980))
    s += kvartira_veschi(1180, 980, 700, t, 11)
    # ковёр на стене слева
    dal = f'<rect x="90" y="190" width="820" height="540" rx="14" fill="{ob.ALYJ2}" {o(7)}/>'
    dal += f'<rect x="124" y="222" width="752" height="476" rx="10" fill="none" stroke="{ob.ZOLOTO}" stroke-width="9" opacity=".8"/>'
    for i in range(5):
        dal += (f'<path d="M150,{266 + i*96:.0f} q350,52 700,0" fill="none"'
                f' stroke="{ob.ZOLOTO}" stroke-width="7" opacity=".6"/>')
    for i in range(4):
        dal += (f'<path d="M{260 + i*170:.0f},300 l60,120 l-60,120 l-60,-120 z"'
                f' fill="{ob.ZOLOTO2}" opacity=".5"/>')
    dal += teplo(500, 420, 520, 380, .35)
    s += SL(Z_DAL, dal)
    # СТОЛ без просвета
    sred = ten(960, 1046, 840, 44, .55)
    sred += f'<rect x="90" y="760" width="1740" height="46" rx="14" fill="url(#derev)" {o(7)}/>'
    sred += b5_skatert(90, 760, 1740, t, 170, "url(#rush)", ob.ALYJ, 8.0, .2, 7)
    r = random.Random(33)
    poz = []
    for i in range(11):
        poz.append((180 + i * 156, 748 - (i % 3) * 10))
    for i, (px, py) in enumerate(poz):
        k = i % 5
        if k == 0:
            sred += b5_blyudo(px, py, 92, t, "url(#krem)", ob.ZOLOTO, i * .2)
            sred += (f'<ellipse cx="{px:.0f}" cy="{py-12:.0f}" rx="60" ry="19"'
                     f' fill="{("#9c4a3a", "#6f8c4a", CHAY, "#8d3a5e")[i % 4]}" opacity=".9"/>')
        elif k == 1:
            sred += b5_banka(px, py + 8, 92, 148, t, (ob.ALYJ2, "#6f8c4a", CHAY)[i % 3], i * .17, False)
        elif k == 2:
            sred += baza.krynka(px, py + 6, 1.25)
        elif k == 3:
            # графин поблёскивает
            bl = .3 + .55 * abs(A.w(t, 2.4, i * .2))
            sred += (f'<g transform="translate({px:.0f},{py+8:.0f})">{ten(0, 10, 54, 12, .45)}'
                     f'<path d="M-46,0 q-12,-92 10,-124 l0,-56 q22,-10 44,0 l0,56'
                     f' q22,32 10,124 z" fill="url(#stekl)" opacity=".8" {o(5)}/>'
                     f'<rect x="-14" y="-200" width="28" height="26" rx="8" fill="url(#zhel)" {o(4)}/>'
                     f'<path d="M-30,-70 q30,16 60,0" fill="none" stroke="{ob.ALYJ}" stroke-width="22" opacity=".55"/>'
                     f'<rect x="-32" y="-116" width="14" height="92" rx="7" fill="#ffffff"'
                     f' opacity="{bl:.2f}"/></g>')
        else:
            sred += b5_syr(px, py, .8, 1.0)
    # пар от миски
    sred += baza.par(620, 706, t, 5, .5, 230, .38, 1.3)
    sred += baza.par(1250, 700, t, 4, .45, 200, .32, 1.2)
    s += SL(Z_SRED, sred)
    # БАБУШКА со спины ставит последнюю вазочку
    per = ob.figura(1480, 1080, 680, t, "#221c2c", "#f3c884", True, .1, False)
    vx, vy = 1230, 742
    per += (f'<g transform="translate(0,{-280*(1-vst):.0f})" opacity="{min(1.0,vst+.2):.2f}">'
            f'{ten(vx, vy+18, 58, 14, .45)}'
            f'<path d="M{vx-62:.0f},{vy-92:.0f} q62,66 124,0 q-20,88 -62,96'
            f' q-42,-8 -62,-96 z" fill="url(#stekl)" opacity=".82" {o(5)}/>'
            f'<ellipse cx="{vx:.0f}" cy="{vy-86:.0f}" rx="62" ry="18" fill="#f0c86a" {o(4)}/>'
            f'<rect x="{vx-26:.0f}" y="{vy-2:.0f}" width="52" height="18" rx="8" fill="#cfe3ef" {o(4)}/>'
            f'<path d="M{vx-44:.0f},{vy-70:.0f} q10,56 30,70" fill="none" stroke="#ffffff"'
            f' stroke-width="9" opacity=".45"/></g>')
    per += b5_stul(330, 1080, t, .76)
    s += SL(Z_PERED, per)
    s += vinetka(.44)
    return s


def verhnyaya_polka_s_pripasami(t):
    """Верхняя полка шкафа снизу, как смотрит ребёнок: банка, плоская банка,
    коробка с бантом. Живое: ребёнок тянется на цыпочках, бант качается, банки поблёскивают."""
    tyan = abs(math.sin(math.pi * ((t / 2.2) % 1.0)))
    s = SL(Z_NEBO, b5_stena(t, 960, 300, "#29324a", "#161b28", 980))
    # корпус шкафа, вид снизу: верх далеко, низ уходит на зрителя
    dal = (f'<path d="M150,120 L1770,120 L1700,760 L220,760 Z" fill="#3a3024" {o(8)}/>')
    dal += (f'<path d="M200,180 L1720,180 L1664,560 L256,560 Z" fill="#2b2419" opacity=".9"/>')
    dal += teplo(960, 460, 760, 420, .4)
    s += SL(Z_DAL, dal)
    # ПРИПАСЫ на полке: низ предметов скрыт передней кромкой доски
    sred = ""
    sred += b5_banka(520, 560, 190, 280, t, "#6f8c4a", .1, True)
    for i in range(6):                       # «нарисованный горошек» — зелёные точки
        sred += (f'<circle cx="{470 + (i % 3)*48:.0f}" cy="{430 + (i//3)*54:.0f}" r="22"'
                 f' fill="#9ec266" opacity=".85" stroke="#4f6b31" stroke-width="4"/>')
    # плоская банка со шпротами
    sred += ten(900, 574, 150, 20, .45)
    sred += (f'<rect x="770" y="470" width="270" height="96" rx="16" fill="url(#zhel)" {o(6)}/>')
    sred += (f'<rect x="790" y="484" width="230" height="30" rx="12" fill="#cfd6dd" opacity=".55"/>')
    bl = .3 + .5 * abs(A.w(t, 2.8, .4))
    sred += f'<rect x="800" y="488" width="60" height="18" rx="9" fill="#ffffff" opacity="{bl:.2f}"/>'
    sred += f'<circle cx="1010" cy="480" r="16" fill="#9aa4ad" {o(4)}/>'
    # коробка конфет с бантом
    sred += ten(1340, 578, 190, 22, .5)
    sred += f'<rect x="1150" y="402" width="390" height="170" rx="14" fill="{ob.ALYJ}" {o(7)}/>'
    sred += f'<rect x="1150" y="402" width="390" height="22" rx="10" fill="#ffffff" opacity=".28"/>'
    sred += f'<rect x="1320" y="402" width="50" height="170" fill="{ob.ZOLOTO}" opacity=".9"/>'
    sred += f'<rect x="1150" y="470" width="390" height="40" fill="{ob.ZOLOTO}" opacity=".9"/>'
    ban = 9 * A.w(t, 2.3)
    sred += (f'<g transform="translate(1345,420) rotate({ban:.1f})">'
             f'<path d="M0,0 q-96,-64 -104,-6 q-8,54 104,6 z" fill="{ob.ZOLOTO}" {o(5)}/>'
             f'<path d="M0,0 q96,-64 104,-6 q8,54 -104,6 z" fill="{ob.ZOLOTO}" {o(5)}/>'
             f'<circle r="20" fill="{ob.ZOLOTO2}" {o(4)}/>'
             f'<path d="M-24,10 q-30,60 -70,76 M24,10 q30,60 70,76" fill="none"'
             f' stroke="{ob.ZOLOTO}" stroke-width="12" stroke-linecap="round"/></g>')
    s += SL(Z_SRED, sred)
    # ПЕРЕДНЯЯ КРОМКА доски и ребёнок на цыпочках
    per = (f'<path d="M228,556 L1692,556 L1720,660 L200,660 Z" fill="url(#derev)" {o(7)}/>')
    per += f'<path d="M232,562 L1688,562" fill="none" stroke="#ffffff" stroke-width="7" opacity=".25"/>'
    bx, bby = 1160, 1080
    per += (f'<g transform="translate(0,{-44*tyan:.1f})">'
            + ob.figura(bx, bby, 560, t, "#1d1826", "#ffd79a", False, .2, True)
            + f'<ellipse cx="{bx-34:.0f}" cy="{bby-6 + 44*tyan:.0f}" rx="38" ry="13"'
            f' fill="#1a1522" opacity=".85"/>'
            f'<ellipse cx="{bx+40:.0f}" cy="{bby-6 + 44*tyan:.0f}" rx="38" ry="13"'
            f' fill="#1a1522" opacity=".85"/></g>')
    s += SL(Z_PERED, per)
    s += vinetka(.5)
    return s


def pogreb_s_letnimi_bankami(t):
    """Погреб со светом фонарика: луч идёт по банкам, самая красивая поднимается
    к люку. Живое: луч идёт по полкам, банка поднимается, паутинка качается."""
    pod = A.ease(A.seg(t, 4.0, 2.6))
    a = -58 + 30 * A.w(t, 6.0)
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1a1510"/>'
           + kladka(-60, -40, W + 120, H + 80, 86, "#3a2f23"))
    # ПОЛКИ С БАНКАМИ
    dal = ""
    for row, py in enumerate((420, 650, 880)):
        dal += (f'<rect x="60" y="{py:.0f}" width="1300" height="26" rx="8"'
                f' fill="url(#derev)" {o(6)}/>')
        dal += (f'<path d="M140,{py+26:.0f} l26,46 M1240,{py+26:.0f} l-26,46" {o(5)} fill="none"/>')
        for i in range(8):
            bx = 130 + i * 156
            col = ("#b63b27", "#6f8c4a", CHAY, "#7a4a2a", "#8d3a5e")[(i + row) % 5]
            dal += b5_banka(bx, py, 104, 150 - (row % 2) * 16, t, col, (i + row) * .13, True)
    dal += teplo(300, 940, 520, 300, .22)
    s += SL(Z_DAL, dal)
    # ЛУЧ ФОНАРИКА
    fx, fy = 180, 1040
    ar = math.radians(a)
    L = 1500
    sred = (f'<path d="M{fx:.0f},{fy:.0f} L{fx + math.cos(ar-.22)*L:.0f},'
            f'{fy + math.sin(ar-.22)*L:.0f} L{fx + math.cos(ar+.22)*L:.0f},'
            f'{fy + math.sin(ar+.22)*L:.0f} Z" fill="{SVET}" opacity=".16"/>')
    sred += (f'<path d="M{fx:.0f},{fy:.0f} L{fx + math.cos(ar-.09)*L:.0f},'
             f'{fy + math.sin(ar-.09)*L:.0f} L{fx + math.cos(ar+.09)*L:.0f},'
             f'{fy + math.sin(ar+.09)*L:.0f} Z" fill="{SVET}" opacity=".2"/>')
    sred += teplo(fx + math.cos(ar) * 760, fy + math.sin(ar) * 760, 300, 260, .45)
    sred += (f'<rect x="{fx-60:.0f}" y="{fy-40:.0f}" width="150" height="56" rx="20"'
             f' fill="url(#zhel)" {o(6)} transform="rotate({a:.0f} {fx:.0f} {fy:.0f})"/>')
    # ВЫБРАННАЯ БАНКА поднимается к люку
    byx = 598
    byy = 650 - (650 - 220) * pod
    sred += (f'<g transform="translate({28*pod:.0f},0)">'
             + b5_banka(byx, byy, 128, 190, t, "#b63b27", .0, True, True)
             + f'<rect x="{byx-72:.0f}" y="{byy-196:.0f}" width="144" height="202" rx="26"'
               f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="7"'
               f' opacity="{.45 + .45*abs(A.w(t, 1.8)):.2f}"/>' + '</g>')
    sred += teplo(byx, byy - 90, 230, 230, .4 * pod)
    s += SL(Z_SRED, sred)
    # ЛЮК сверху и ПАУТИНКА в углу
    per = (f'<path d="M520,-20 L1180,-20 L1120,210 L580,210 Z" fill="#101722"/>'
           f'<path d="M560,0 L1140,0 L1096,180 L604,180 Z" fill="#93b6cf"'
           f' opacity="{.35 + .1*abs(A.w(t, 5.0)):.2f}"/>')
    per += baza.luch(600, 180, 480, 760, t, .13)
    per += (f'<path d="M500,-20 L560,0 L604,180 L540,200 Z" fill="url(#dosk)" {o(6)}/>')
    kch = 2.6 * A.w(t, 4.4)
    per += f'<g transform="rotate({kch:.2f} 1880 40)">'
    for i in range(5):
        rr = 70 + i * 62
        per += (f'<path d="M1880,{40:.0f} m{-rr:.0f},0 q{rr*.5:.0f},{rr*.55:.0f} {rr:.0f},{rr:.0f}"'
                f' fill="none" stroke="#c9d6e2" stroke-width="3" opacity=".35"/>')
    for i in range(6):
        aa = math.pi * (.5 + i * .09)
        per += (f'<path d="M1880,40 L{1880 + math.cos(aa)*400:.0f},{40 + abs(math.sin(aa))*400:.0f}"'
                f' stroke="#c9d6e2" stroke-width="3" opacity=".3"/>')
    per += '</g>'
    per += ramka_pp("levo", "#070a0e", .8).replace('<g data-z="-230">', '').replace('</g><!--/z-->', '')
    s += SL(Z_PERED, per)
    s += vinetka(.56)
    return s


def polka_kuhonnogo_shkafa(t):
    """Люк погреба стал дверцей кухонного шкафа: она открывается, на полке те же
    припасы, только поменьше. Живое: дверца открывается, банки поблёскивают,
    свет кухни ложится на полку."""
    otk = A.ease(A.seg(t, .35, 1.5))
    plit = f'<rect width="{W}" height="{H}" fill="#2b3a4e"/>'
    for r_ in range(3):
        for c in range(int(W / 120) + 1):
            plit += (f'<rect x="{c*120 + (0 if r_ % 2 == 0 else 60):.0f}" y="{r_*100:.0f}"'
                     f' width="112" height="92" rx="8" fill="#5f7183" opacity=".8"'
                     f' stroke="#3d4e60" stroke-width="4"/>')
    plit += f'<rect y="300" width="{W}" height="{H-300}" fill="#2b3a4e"/>'
    s = SL(Z_NEBO, plit)
    # корпус шкафа и полка с припасами
    dal = ten(960, 1024, 640, 30, .5)
    dal += f'<rect x="300" y="160" width="1320" height="780" rx="16" fill="#3d3225" {o(8)}/>'
    dal += f'<rect x="340" y="200" width="1240" height="700" rx="10" fill="#2c2419"/>'
    dal += teplo(960, 560, 640, 400, .45 * otk)
    for row, py in enumerate((520, 830)):
        dal += (f'<rect x="340" y="{py:.0f}" width="1240" height="22" rx="8"'
                f' fill="url(#derev)" {o(5)}/>')
        for i in range(7):
            bx = 420 + i * 190
            col = ("#b63b27", "#6f8c4a", CHAY, "#7a4a2a", "#8d3a5e")[(i + row) % 5]
            dal += b5_banka(bx, py, 86, 118 - (row % 2) * 12, t, col, (i + row) * .15, True)
    # коробка с бантом на верхней полке — та же, что была на шкафу
    dal += f'<rect x="1300" y="412" width="250" height="106" rx="10" fill="{ob.ALYJ}" {o(6)}/>'
    dal += f'<rect x="1300" y="450" width="250" height="26" fill="{ob.ZOLOTO}" opacity=".9"/>'
    dal += f'<rect x="1402" y="412" width="32" height="106" fill="{ob.ZOLOTO}" opacity=".9"/>'
    s += SL(Z_DAL, dal)
    # свет кухни падает на полку
    s += SL(Z_SRED, baza.luch(240, 60, 520, 900, t, .2 * otk)
            + f'<rect x="340" y="200" width="1240" height="700" fill="{SVET}" opacity="{.1*otk:.2f}"/>')
    # ДВЕРЦА открывается
    per = (f'<g transform="translate(300,160) scale({1 - otk*.78:.3f},1)">'
           f'<rect width="1320" height="780" rx="16" fill="url(#derev)" {o(8)}/>'
           f'<rect x="60" y="60" width="1200" height="660" rx="12" fill="none"'
           f' stroke="{DOSKA2}" stroke-width="12"/>'
           f'<rect x="90" y="90" width="60" height="600" rx="30" fill="#ffffff" opacity=".2"/>'
           f'<rect x="1200" y="360" width="34" height="120" rx="17" fill="url(#zhel)" {o(5)}/></g>')
    per += f'<rect x="120" y="940" width="1680" height="44" rx="14" fill="url(#beton)" {o(7)}/>'
    per += f'<rect x="120" y="940" width="1680" height="14" rx="7" fill="#ffffff" opacity=".22"/>'
    per += b5_banka(400, 940, 92, 126, t, "#6f8c4a", .5, True)
    per += baza.krynka(1600, 936, 1.1)
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def otkrytaya_korobka_konfet(t):
    """Коробка конфет на праздничной скатерти, крышка снимается сама; на миг
    коробка становится хрустальной салатницей. Живое: крышка снимается,
    золотые бумажки блестят, коробка превращается и возвращается."""
    kr = A.out(A.seg(t, .35, 1.1))
    mor = max(0.0, math.sin(math.pi * A.seg(t, 1.45, .95)))
    s = SL(Z_NEBO, b5_stena(t, 1460, 420, "#2b3449", "#171d2a", 900)
           + ob.girlyanda(-60, 130, 1980, 170, t, 16, 110))
    s += SL(Z_DAL, ob.elka(1680, 1020, 560, t, seed=15)
            + okno_izby(120, 210, 310, 280, t, vid=b5_za_oknom(120, 210, 310, 280, t), moroz=.45))
    s += SL(Z_SRED, b5_skatert(120, 720, 1680, t, 170))
    cx, cy = 880, 690
    # коробка
    kor = f'<g opacity="{1 - mor:.2f}">'
    kor += ten(cx, cy + 86, 300, 30, .55)
    kor += f'<rect x="{cx-290:.0f}" y="{cy-40:.0f}" width="580" height="130" rx="16" fill="{ob.ALYJ}" {o(7)}/>'
    kor += f'<rect x="{cx-290:.0f}" y="{cy-40:.0f}" width="580" height="20" rx="10" fill="#ffffff" opacity=".25"/>'
    kor += (f'<path d="M{cx-290:.0f},{cy-40:.0f} q290,-54 580,0 q-290,56 -580,0 z"'
            f' fill="{ob.ALYJ2}" {o(5)}/>')
    # конфеты в золотых бумажках
    for i in range(12):
        bx = cx - 232 + (i % 6) * 93
        by = cy - 48 + (i // 6) * 42
        gor = .45 + .55 * abs(A.w(t, 1.8 + (i % 4) * .4, i * .19))
        kor += (f'<g transform="translate({bx:.0f},{by:.0f}) rotate({-14 + (i*23) % 28})">'
                f'<ellipse rx="38" ry="23" fill="url(#zol)" {o(4)}/>'
                f'<path d="M-38,0 l-24,-16 l0,32 z" fill="{ob.ZOLOTO2}" {o(3)}/>'
                f'<path d="M38,0 l24,-16 l0,32 z" fill="{ob.ZOLOTO2}" {o(3)}/>'
                f'<ellipse cx="-10" cy="-8" rx="13" ry="7" fill="#fff8dc" opacity="{gor:.2f}"/></g>')
    kor += '</g>'
    # хрустальная салатница — на миг вместо коробки
    hru = f'<g opacity="{mor:.2f}">'
    hru += ten(cx, cy + 90, 250, 28, .5)
    hru += (f'<path d="M{cx-250:.0f},{cy-60:.0f} q40,164 250,176 q210,-12 250,-176 z"'
            f' fill="#cfe7f5" opacity=".92" stroke="#ffffff" stroke-width="8"/>')
    for i in range(9):
        hx = cx - 210 + i * 52
        hru += (f'<path d="M{hx:.0f},{cy-56:.0f} l{(i-4)*7:.0f},150" fill="none"'
                f' stroke="#ffffff" stroke-width="7" opacity=".4"/>')
    hru += (f'<ellipse cx="{cx:.0f}" cy="{cy-60:.0f}" rx="250" ry="34" fill="#dff0fa"'
            f' opacity=".6" {o(5)}/>')
    hru += f'<rect x="{cx-70:.0f}" y="{cy+110:.0f}" width="140" height="22" rx="10" fill="#cfe3ef" {o(4)}/>'
    hru += '</g>'
    s += SL(Z_PERED, kor + hru + baza.svecha(1500, 700, t, .3, 1.1, 110))
    # КРЫШКА снимается и уходит вверх
    ly = cy - 40 - 300 * kr
    s += SL(Z_LETIT, f'<g transform="translate({cx + 36*kr:.0f},{ly:.0f}) rotate({-7*kr:.1f})"'
            f' opacity="{1 - .25*kr:.2f}">'
            f'<rect x="-300" y="-46" width="600" height="92" rx="16" fill="{ob.ALYJ2}" {o(7)}/>'
            f'<rect x="-300" y="-46" width="600" height="18" rx="9" fill="#ffffff" opacity=".22"/>'
            f'<rect x="-120" y="-30" width="240" height="60" rx="12" fill="none"'
            f' stroke="{ob.ZOLOTO}" stroke-width="7" opacity=".9"/></g>')
    s += vinetka(.42)
    return s


def dlinnyy_chek_uletaet(t):
    """Над столом вьётся длинная лента чека; она сминается в комок, и под ней
    открывается простой красивый стол. Живое: лента вьётся, комок летит прочь,
    свечи горят."""
    sm = A.ease(A.seg(t, 2.2, 1.2))
    let = A.ease(A.seg(t, 3.2, 1.6))
    s = SL(Z_NEBO, b5_stena(t, 860, 560, "#2a3348", "#161c29", 880))
    s += SL(Z_DAL, okno_izby(1420, 200, 360, 320, t,
                             vid=b5_za_oknom(1420, 200, 360, 320, t), moroz=.5)
            + ob.girlyanda(-40, 130, 1980, 170, t, 16, 110))
    # ПРОСТОЙ КРАСИВЫЙ СТОЛ — открывается по мере ухода чека
    otk = min(1.0, sm * 1.1)
    sred = b5_skatert(300, 740, 1320, t, 170)
    sred += (f'<g opacity="{.25 + .75*otk:.2f}">'
             + b5_blyudo(960, 726, 190, t, "url(#krem)")
             + b5_zelen(960, 700, t, .7, 9, .2)
             + b5_ogurcy(680, 726, .78, 1.0)
             + b5_syr(1250, 726, .8, 1.0)
             + ob.mandarin(560, 700, 1.3, 0.0, t)
             + ob.mandarin(1420, 702, 1.25, 0.0, t) + '</g>')
    sred += baza.svecha(430, 660, t, .0, 1.25, 120)
    sred += baza.svecha(1510, 664, t, .45, 1.2, 116)
    sred += ob.bokal(820, 726, t, .72, .1, .6, True)
    sred += ob.bokal(1110, 726, t, .72, .5, .55, True)
    s += SL(Z_SRED, sred)
    # ЛЕНТА ЧЕКА — вьётся над столом, без цифр и названий
    per = ""
    if sm < .98:
        pts = []
        for i in range(26):
            u = i / 25.0
            x = 120 + u * 1700
            y = 300 + 130 * math.sin(2 * math.pi * (u * 1.7 + t * .22)) \
                + 60 * math.sin(2 * math.pi * (u * 3.4 - t * .15))
            pts.append((x, y))
        d = b5_gladko(pts)
        per += (f'<g opacity="{1 - sm:.2f}">'
                f'<path d="{d}" fill="none" stroke="#f4f1e6" stroke-width="{86*(1-sm*.5):.0f}"'
                f' stroke-linecap="round" {""}/>'
                f'<path d="{d}" fill="none" stroke="#d6cfbd" stroke-width="{86*(1-sm*.5):.0f}"'
                f' stroke-linecap="round" opacity=".25"/>')
        for i in range(1, 25):
            px, py = pts[i]
            per += (f'<path d="M{px-26:.0f},{py-8:.0f} h52" stroke="#b7b0a0"'
                    f' stroke-width="5" opacity=".65"/>')
            per += (f'<path d="M{px-20:.0f},{py+10:.0f} h34" stroke="#c6bfae"'
                    f' stroke-width="5" opacity=".5"/>')
        per += '</g>'
    # КОМОК летит прочь
    if sm > .05:
        kx = 980 + 900 * let
        ky = 360 - 300 * let - 160 * math.sin(math.pi * let)
        rr = 90 * sm * (1 - .3 * let)
        per += (f'<g transform="translate({kx:.0f},{ky:.0f}) rotate({let*520:.0f})"'
                f' opacity="{1 - let*.6:.2f}">'
                f'<circle r="{rr:.0f}" fill="#f4f1e6" {o(6)}/>')
        rnd = random.Random(19)
        for i in range(9):
            a1 = rnd.uniform(0, 6.28)
            per += (f'<path d="M{math.cos(a1)*rr*.2:.0f},{math.sin(a1)*rr*.2:.0f}'
                    f' L{math.cos(a1)*rr*.9:.0f},{math.sin(a1)*rr*.9:.0f}" stroke="#c0b9a7"'
                    f' stroke-width="6" opacity=".7"/>')
        per += '</g>'
    s += SL(Z_LETIT, per)
    s += vinetka(.44)
    return s


def novogodniy_stol_sverhu(t):
    """Круглый стол строго сверху: блюда встают по одному, в середине блюдо под
    вышитым полотенцем. Живое: блюда встают, полотенце приподнимается, свечи горят."""
    vr = t * 2.1
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1b2231"/>'
           + polovicy(0, "url(#pol)")
           + f'<rect width="{W}" height="{H}" fill="#121a28" opacity=".55"/>'
           + teplo(960, 540, 1000, 820, .5))
    # четыре стула вокруг — видны спинками сверху
    dal = ""
    for i in range(6):
        a = vr + i * 60
        ar = math.radians(a)
        sx, sy = 960 + math.cos(ar) * 560, 540 + math.sin(ar) * 470
        dal += (f'<g transform="translate({sx:.0f},{sy:.0f}) rotate({a + 90:.0f})">'
                f'{ten(0, 22, 86, 30, .5)}'
                f'<rect x="-84" y="-56" width="168" height="112" rx="16" fill="url(#derev)" {o(6)}/>'
                f'<rect x="-76" y="-50" width="152" height="24" rx="10" fill="#ffffff" opacity=".2"/></g>')
    s += SL(Z_DAL, dal)
    # КРУГЛЫЙ СТОЛ
    sred = ten(960, 600, 440, 420, .6)
    sred += f'<ellipse cx="960" cy="540" rx="432" ry="420" fill="url(#derev)" {o(8)}/>'
    sred += f'<ellipse cx="960" cy="540" rx="404" ry="392" fill="url(#rush)" {o(6)}/>'
    sred += (f'<ellipse cx="960" cy="540" rx="364" ry="352" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="10" opacity=".65"/>')
    sred += f'<ellipse cx="820" cy="400" rx="150" ry="110" fill="#ffffff" opacity=".2"/>'
    s += SL(Z_SRED, sred)
    # ВРАЩЕНИЕ + блюда по одному
    per = f'<g transform="rotate({vr:.2f} 960 540)">'
    bl = ((0, 196, .5, "zelen"), (120, 196, 1.6, "syr"), (240, 196, 2.7, "manda"))
    for a0, rr, t0, kind in bl:
        k = A.over(A.seg(t, t0, .95))
        if k <= .02:
            continue
        ar = math.radians(a0 - 90)
        px, py = 960 + math.cos(ar) * rr, 540 + math.sin(ar) * rr * .95
        per += (f'<g transform="translate({px:.0f},{py:.0f})'
                f' scale({k*1.45:.3f}) rotate({-vr:.2f})">')
        if kind == "zelen":
            per += (f'<ellipse rx="112" ry="108" fill="url(#krem)" {o(6)}/>'
                    f'<ellipse rx="86" ry="82" fill="none" stroke="{ob.ZOLOTO}" stroke-width="5" opacity=".8"/>')
            rr2 = random.Random(5)
            for i in range(12):
                aa = rr2.uniform(0, 6.28)
                dd = rr2.uniform(0, 70)
                per += (f'<ellipse cx="{math.cos(aa)*dd:.0f}" cy="{math.sin(aa)*dd:.0f}"'
                        f' rx="34" ry="13" fill="{("#5f8a3e","#79a44f","#486f31")[i%3]}"'
                        f' transform="rotate({aa*57:.0f},{math.cos(aa)*dd:.0f},{math.sin(aa)*dd:.0f})"/>')
        elif kind == "syr":
            per += (f'<ellipse rx="112" ry="108" fill="url(#krem)" {o(6)}/>')
            for i in range(5):
                aa = i * 1.256
                per += (f'<path d="M0,0 l{math.cos(aa)*86:.0f},{math.sin(aa)*86:.0f}'
                        f' A86,86 0 0 1 {math.cos(aa+1.1)*86:.0f},{math.sin(aa+1.1)*86:.0f} z"'
                        f' fill="url(#zol)" {o(4)}/>')
        else:
            per += (f'<ellipse rx="120" ry="116" fill="url(#stekl)" opacity=".6" {o(6)}/>')
            for i in range(7):
                aa = i * .9
                dd = 0 if i == 0 else 56
                per += (f'<circle cx="{math.cos(aa)*dd:.0f}" cy="{math.sin(aa)*dd:.0f}" r="38"'
                        f' fill="{ob.MANDA}" {o(5)}/>'
                        f'<circle cx="{math.cos(aa)*dd-12:.0f}" cy="{math.sin(aa)*dd-12:.0f}"'
                        f' r="12" fill="#ffc98a" opacity=".6"/>')
        per += '</g>'
    # СВЕЧИ сверху: пламя как горящая точка с ореолом
    for i in range(3):
        ar = math.radians(60 + i * 120)
        px, py = 960 + math.cos(ar) * 340, 540 + math.sin(ar) * 330
        gor = .72 + .28 * abs(A.w(t, .9, i * .3))
        per += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="26" fill="url(#vosk)" {o(5)}/>'
                f'{teplo(px, py, 120*gor, 120*gor, .75)}'
                f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{13*gor:.0f}" fill="{SVET}"/>')
    # БЛЮДО ПОД ВЫШИТЫМ ПОЛОТЕНЦЕМ в середине
    pr = A.over(A.seg(t, 3.8, 1.0))
    lift = 26 * max(0.0, math.sin(math.pi * ((t / 2.8) % 1.0)))
    if pr > .02:
        per += f'<g transform="translate(960,540) scale({pr:.3f})">'
        per += ten(0, 40, 200, 180, .5)
        per += f'<ellipse rx="196" ry="188" fill="url(#krem)" {o(7)}/>'
        per += (f'<path d="M-196,{-10 - lift:.0f} q196,{-150 - lift:.0f} 392,0'
                f' q-30,196 -196,206 q-166,-10 -196,-206 z" fill="url(#rush)" {o(6)}/>')
        for i in range(3):
            per += (f'<path d="M-168,{34 + i*58 - lift*.4:.0f} q168,46 336,0" fill="none"'
                    f' stroke="{ob.ALYJ}" stroke-width="9" opacity=".75"/>')
        for i in range(7):
            px = -150 + i * 50
            per += (f'<path d="M{px:.0f},{-26-lift:.0f} l18,26 l-18,26 l-18,-26 z"'
                    f' fill="{ob.ALYJ2}" opacity=".8"/>')
        per += baza.par(0, -40 - lift, t, 4, .45, 150, .3, 1.0)
        per += '</g>'
    per += '</g>'
    s += SL(Z_PERED, per)
    s += vinetka(.46)
    return s


def tri_okna_tri_blyuda(t):
    """Три светящихся окна в зимней стене: холодец, слоёный салат в хрустале,
    пирог и раскрытая тетрадка. Живое: окна загораются по одному, холодец
    дрожит, страница тетрадки переворачивается."""
    s = SL(Z_NEBO, nebo("noch", t) + sneg_letit(t, 46))
    s += SL(Z_DAL, brevna(-20, 120, BAND + 40, 960, 104)
            + f'<rect x="-20" y="120" width="{BAND+40}" height="30" rx="10" fill="url(#sneg)" {o(5)}/>')
    sred = ""
    for i, ox in enumerate((40, 300, 560)):
        gor = A.ease(A.seg(t, .35 + i * .75, .7))
        oy, ow, oh = 380, 230, 300
        vid = (f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
               f' fill="{"#3a2a16" if gor > .05 else "#1a1e2c"}"/>')
        vid += (f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
                f' fill="{SVET}" opacity="{.42*gor:.2f}"/>')
        # стол внутри окна и блюдо силуэтом
        ty = oy + oh - 76
        vid += (f'<rect x="{ox+16:.0f}" y="{ty:.0f}" width="{ow-32:.0f}" height="16"'
                f' rx="7" fill="url(#rush)" opacity="{.3 + .7*gor:.2f}"/>')
        cx = ox + ow / 2
        if i == 0:
            # ХОЛОДЕЦ дрожит
            dr = 7 * A.w(t, .55) * gor
            vid += (f'<g transform="translate({cx:.0f},{ty:.0f}) scale({1 + dr*.012:.3f},'
                    f'{1 - dr*.012:.3f})" opacity="{gor:.2f}">'
                    f'<rect x="-82" y="-62" width="164" height="62" rx="14" fill="#cfd8c0" {o(5)}/>'
                    f'<rect x="-82" y="-62" width="164" height="16" rx="8" fill="#e6ecd8" opacity=".8"/>'
                    f'<ellipse cx="-26" cy="-28" rx="20" ry="11" fill="#9a6b4a" opacity=".8"/>'
                    f'<ellipse cx="28" cy="-34" rx="18" ry="10" fill="#9a6b4a" opacity=".8"/>'
                    f'<ellipse cx="2" cy="-16" rx="16" ry="8" fill="#6f8c4a" opacity=".8"/></g>')
        elif i == 1:
            # СЛОЁНЫЙ САЛАТ в хрустале
            vid += (f'<g transform="translate({cx:.0f},{ty:.0f})" opacity="{gor:.2f}">'
                    f'<path d="M-84,-8 q14,-104 84,-110 q70,6 84,110 z" fill="url(#stekl)"'
                    f' opacity=".55" {o(5)}/>')
            for k, c in enumerate(("#b63b27", "#f0d79a", "#6f8c4a", "#e8c15a")):
                vid += (f'<path d="M{-78 + k*7:.0f},{-20 - k*22:.0f} q{78 - k*7:.0f},-22'
                        f' {156 - k*14:.0f},0 l0,22 q{-78 + k*7:.0f},20 {-156 + k*14:.0f},0 z"'
                        f' fill="{c}" opacity=".95"/>')
            vid += '</g>'
        else:
            # ПИРОГ
            vid += (f'<g transform="translate({cx:.0f},{ty:.0f})" opacity="{gor:.2f}">'
                    f'<ellipse cx="0" cy="-12" rx="86" ry="34" fill="url(#med)" {o(5)}/>'
                    f'<ellipse cx="0" cy="-26" rx="86" ry="34" fill="url(#med)" {o(5)}/>'
                    f'<path d="M-62,-36 q62,-22 124,0" fill="none" stroke="#f2cf8c" stroke-width="8" opacity=".8"/>'
                    f'<path d="M-40,-50 l80,24 M40,-50 l-80,24" stroke="#c48f3c" stroke-width="7"/></g>')
            vid += baza.par(cx, ty - 70, t, 4, .35 * gor, 140, .4, 1.0)
        vid += teplo(cx, oy + oh * .5, 180 * gor, 170 * gor, .55)
        sred += okno_izby(ox, oy, ow, oh, t, vid=vid, moroz=.3, krest=True)
        sred += teplo(cx, oy + oh * .5, 260 * gor, 240 * gor, .4)
    s += SL(Z_SRED, sred)
    # ТЕТРАДКА В КЛЕТКУ на снежном приступке
    per = sneg_lezhit(934, 20).replace('<g data-z="520">', '').replace('</g><!--/z-->', '')
    per += b5_tetrad(250, 786, 430, 270, t, .1)
    per += (f'<g transform="translate(738,866) rotate(-18)">'
            f'{ten(0, 16, 20, 8, .4)}'
            f'<rect x="-9" y="-130" width="18" height="150" rx="8" fill="#2f5a78" {o(4)}/>'
            f'<path d="M-9,20 l9,22 l9,-22 z" fill="#1d1a16"/></g>')
    s += SL(Z_PERED, per)
    s += vinetka(.44)
    return s


def tri_kartochki_drugih_video(t):
    """Тёмно-красный фон, слева встаёт первая карточка-обложка, хозяйка года
    показывает на неё копытцем. Живое: карточка встаёт с отскоком, копытце
    показывает, фон мерцает."""
    mer = .82 + .18 * abs(A.w(t, 3.4))
    vst = A.over(A.seg(t, .25, 1.0))
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#3a0f14"/>'
           + f'<rect width="{W}" height="{H}" fill="{ob.ALYJ2}" opacity="{.5*mer:.2f}"/>'
           + teplo(620, 560, 980, 820, .5 * mer))
    # круги-ореолы вокруг места карточки
    dal = ""
    for i in range(4):
        u = ((t * .3 + i * .25) % 1.0)
        dal += (f'<circle cx="620" cy="560" r="{180 + u*520:.0f}" fill="none"'
                f' stroke="{ob.ZOLOTO}" stroke-width="5" opacity="{(1-u)*.2:.2f}"/>')
    dal += ob.konfetti(t, 18, 9, .35, .6)
    s += SL(Z_DAL, dal)
    # кремовое паспарту под карточкой: красное на красном не читалось
    s += SL(Z_SRED,
            f'<g opacity="{vst:.2f}">'
            + teplo(620, 650, 460, 540, .55)
            + f'<rect x="324" y="274" width="592" height="752" rx="18"'
              f' fill="#f1e4c6" opacity=".92" {o(7)}/>'
            + '</g>'
            + b5_kartochka_video(350, 300, 540, 700, t, vst, .0, 0))
    # ХОЗЯЙКА ГОДА справа, развёрнута к карточке
    XC = 1420
    per = (f'<g transform="matrix(-1,0,0,1,{2*XC:.0f},0)">'
           + ob.koza(XC, 1010, t, .92, 0.0, True, .1) + '</g>')
    # копытце показывает на карточку
    uk = 14 * A.w(t, 1.5)
    per += (f'<g transform="translate({1330 + uk*.5:.0f},{842 + uk:.0f})">'
            f'<path d="M0,0 q-70,-44 -150,-52" fill="none" stroke="{ob.ALYJ}"'
            f' stroke-width="36" stroke-linecap="round"/>'
            f'<path d="M0,0 q-70,-44 -150,-52" fill="none" stroke="{ob.ALYJ2}"'
            f' stroke-width="13" stroke-linecap="round" opacity=".5"/>'
            f'<rect x="-186" y="-72" width="44" height="34" rx="10" fill="{CHUGUN}" {o(5)}/></g>')
    s += SL(Z_PERED, per)
    s += vinetka(.5)
    return s


def elochnaya_vetka_s_krasnym_sharom(t):
    """Крупно еловая ветка с красным шаром, в шаре отражается карточка-обложка;
    на второй фразе под веткой встают все три. Живое: шар покачивается,
    отражение блестит, карточки встают в ряд."""
    kch = 4.4 * A.w(t, 2.6)
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#121b26"/>'
           + f'<rect width="{W}" height="{H}" fill="{ob.HVOYA2}" opacity=".5"/>'
           + teplo(640, 420, 820, 700, .45))
    # боке огней
    bok = ""
    r = random.Random(27)
    for i in range(18):
        bx, by = r.uniform(40, W - 40), r.uniform(60, H - 60)
        gor = .25 + .55 * abs(A.w(t, 2.4 + r.uniform(0, 2.4), i * .13))
        col = (SVET, ob.ALYJ, ob.ZOLOTO, "#8fd6ff")[i % 4]
        bok += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r.uniform(20,60):.0f}"'
                f' fill="{col}" opacity="{gor*.26:.2f}"/>')
    s += SL(Z_NEBO, bok)
    # ТРИ КАРТОЧКИ встают в ряд под веткой
    dal = ""
    for i, cx in enumerate((190, 790, 1390)):
        k = A.over(A.seg(t, 2.6 + i * .32, .95))
        dal += b5_kartochka_video(cx, 700, 340, 330, t, k, i * .3, i)
    s += SL(Z_DAL, dal)
    # ШАР с отражением карточки
    bx, by, R = 640, 470, 168
    sred = f'<g transform="rotate({kch:.2f} {bx:.0f} {by-250:.0f})">'
    sred += f'<path d="M{bx:.0f},{by-250:.0f} v{250-R:.0f}" stroke="{ob.ZOLOTO2}" stroke-width="7"/>'
    sred += f'<rect x="{bx-26:.0f}" y="{by-R-42:.0f}" width="52" height="46" rx="10" fill="url(#zol)" {o(5)}/>'
    sred += ten(bx + 16, by + R + 34, R * .8, 26, .5)
    sred += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{R:.0f}" fill="{ob.ALYJ}" {o(9)}/>'
    sred += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{R:.0f}" fill="{ob.ALYJ2}" opacity=".35"/>'
    # отражение третьей обложки внутри шара
    sred += (f'<clipPath id="shar5"><circle cx="{bx:.0f}" cy="{by:.0f}" r="{R-10:.0f}"/></clipPath>'
             f'<g clip-path="url(#shar5)" opacity=".8">'
             f'<g transform="translate({bx-92:.0f},{by-96:.0f}) scale(.52)">'
             + b5_kartochka_video(0, 0, 340, 330, t, 1.0, .5, 2) + '</g></g>')
    # блик по отражению бежит
    bl = ((t * .4) % 1.0)
    sred += (f'<g clip-path="url(#shar5)"><path d="M{bx - R + bl*2*R:.0f},{by-R:.0f}'
             f' l60,0 l-96,{2*R:.0f} l-60,0 z" fill="#ffffff" opacity=".28"/></g>')
    sred += (f'<ellipse cx="{bx-R*.4:.0f}" cy="{by-R*.42:.0f}" rx="{R*.26:.0f}"'
             f' ry="{R*.18:.0f}" fill="#ffffff" opacity="{.4 + .3*abs(A.w(t,2.0)):.2f}"/>')
    sred += teplo(bx, by, 330, 330, .4)
    sred += '</g>'
    s += SL(Z_SRED, sred)
    # ВЕТКА поверх, с краю кадра
    per = b5_vetka_eli(-60, 150, 1180, t, 1.0, .0, 1.0)
    per += b5_vetka_eli(1980, 120, 900, t, 1.0, .4, 1.0).replace(
        'translate(1980.0,120.0)', 'translate(1980.0,120.0) scale(-1,1)')

    s += SL(Z_PERED, per)
    s += vinetka(.48)
    return s


# ═══════════════ lok_b6.py ═══════════════

OKNO = (860, 300, 980, 551)


def b6_g(nid, c1, c2, vert=True):
    """Свой градиент: у каждого предмета должен быть объём (правило 5)."""
    return (f'<linearGradient id="{nid}" x1="0" y1="0" x2="{0 if vert else 1}"'
            f' y2="{1 if vert else 0}"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def b6_mix(c1, c2, k):
    """Перетекание цвета: им бледнеют яблоки и гаснет лампа."""
    k = max(0.0, min(1.0, k))
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def b6_stena(c1, c2, y_pol=None, pol="url(#pol)"):
    """Стена комнаты одним куском плюс пол: дешёвая глубина для крупных планов."""
    s = b6_g("stnb", c1, c2) + f'<rect width="{W}" height="{H}" fill="url(#stnb)"/>'
    if y_pol:
        s += baza.polovicy(y_pol, pol)
    return s


def b6_moneta(cx, cy, rx, ry, t, ph=0.0, op=1.0, ten_=True):
    """Монета: золотой градиент, ободок, бегающий блик."""
    bl = .3 + .7 * abs(A.w(t, 2.3, ph))
    s = f'<g opacity="{op:.2f}">'
    if ten_:
        s += ten(cx + 3, cy + ry * 1.2, rx * 1.05, ry * .75, .45)
    s += (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"'
          f' fill="url(#zol)" {o(max(2.0, rx * .13))}/>')
    s += (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx * .62:.1f}" ry="{ry * .62:.1f}"'
          f' fill="none" stroke="{ob.ZOLOTO2}" stroke-width="{max(1.6, rx * .09):.1f}" opacity=".6"/>')
    s += (f'<ellipse cx="{cx - rx * .3:.1f}" cy="{cy - ry * .34:.1f}" rx="{rx * .3:.1f}"'
          f' ry="{ry * .28:.1f}" fill="#fff8de" opacity="{bl:.2f}"/>')
    return s + "</g>"


def b6_kupyura(cx, cy, w_, h_, ang=0.0, op=1.0, slozh=False):
    """Купюра БЕЗ цифр и названий: рамка, розетка и волна — узор, не текст."""
    s = (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.2f})" opacity="{op:.2f}">'
         + ten(4, h_ * .62, w_ * .52, h_ * .22, .4))
    s += (f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6"'
          f' fill="url(#list)" {o(max(3, w_ * .018))}/>')
    s += (f'<rect x="{-w_/2 + w_*.06:.0f}" y="{-h_/2 + h_*.12:.0f}" width="{w_*.88:.0f}"'
          f' height="{h_*.76:.0f}" rx="4" fill="none" stroke="{ob.ZOLOTO2}"'
          f' stroke-width="{max(2, w_*.012):.0f}" opacity=".55"/>')
    s += (f'<circle cx="{-w_*.26:.0f}" cy="0" r="{h_*.26:.0f}" fill="none"'
          f' stroke="{MED}" stroke-width="{max(2, w_*.01):.0f}" opacity=".5"/>')
    s += (f'<path d="M{-w_*.06:.0f},{-h_*.16:.0f} q{w_*.12:.0f},{h_*.22:.0f} {w_*.24:.0f},0'
          f' q{w_*.12:.0f},{-h_*.22:.0f} {w_*.24:.0f},0" fill="none" stroke="{MED}"'
          f' stroke-width="{max(2, w_*.011):.0f}" opacity=".45"/>')
    if slozh:
        s += (f'<line x1="0" y1="{-h_/2:.0f}" x2="0" y2="{h_/2:.0f}" stroke="#b9a87e"'
              f' stroke-width="{max(2, w_*.014):.0f}" opacity=".7"/>')
        s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} h{w_/2:.0f} v{h_:.0f} h{-w_/2:.0f} z"'
              f' fill="#ffffff" opacity=".12"/>')
    return s + "</g>"


def b6_tarelka(cx, cy, rx, t, podem=0.0, s_=1.0):
    """Тарелка. `podem` 0..1 — левый край приподнят, правый лежит на столе."""
    ry = rx * .36
    ang = -13 * podem
    lift = -18 * podem
    s = (f'<g transform="translate({cx:.1f},{cy + lift:.1f}) rotate({ang:.2f})">'
         + ten(0, ry * 1.5 + 12 * podem, rx * 1.02, ry * .7, .5))
    s += f'<ellipse rx="{rx:.0f}" ry="{ry:.0f}" fill="url(#krem)" {o(6)}/>'
    s += (f'<ellipse rx="{rx*.72:.0f}" ry="{ry*.72:.0f}" fill="none" stroke="{ob.ALYJ}"'
          f' stroke-width="5" opacity=".55"/>')
    s += (f'<ellipse rx="{rx*.58:.0f}" ry="{ry*.58:.0f}" fill="#fbf4e3" opacity=".8" {o(3)}/>')
    s += (f'<path d="M{-rx*.72:.0f},{-ry*.26:.0f} q{rx*.4:.0f},{-ry*.6:.0f} {rx*.82:.0f},{-ry*.1:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="8" opacity=".5"/>')
    return s + "</g>"


def b6_varezhka(x, y, s_, t, szhat=0.0, ph=0.0, zerk=False, dr=1.6):
    """ВАРЕЖКА вместо ладони (правило 6). `szhat` 0..1 — верх ладони
    загибается вниз и накрывает то, что лежит на ней."""
    drog = dr * A.w(t, 3.1, ph)
    sx = -s_ if zerk else s_
    g = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({drog:.2f})'
         f' scale({sx:.3f},{s_:.3f})">')
    g += ten(6, 120, 104, 24, .5)
    # рукав кофты уходит за нижний край
    g += f'<path d="M-84,96 h168 l22,150 q-102,30 -206,0 z" fill="url(#tkan)" {o(7)}/>'
    for yy in (132, 176, 220):
        g += f'<path d="M-80,{yy} q84,22 168,0" fill="none" stroke="{ob.ALYJ2}" stroke-width="9" opacity=".6"/>'
    # ладонь: от запястья до кончиков пальцев
    g += (f'<path d="M-88,100 q-32,-204 12,-266 q68,-46 152,-8 q46,42 22,274 z"'
          f' fill="url(#rush)" {o(7)}/>')
    # большой палец сбоку
    g += (f'<path d="M-84,-18 q-62,-24 -70,-84 q8,-36 44,-24 q36,14 42,68 z"'
          f' fill="url(#rush)" {o(6)}/>')
    # РЕЗИНКА МАНЖЕТЫ: вертикальные рубчики у запястья
    g += (f'<path d="M-90,36 q90,30 180,0 l-4,66 q-86,28 -172,-2 z"'
          f' fill="#e3d2a8" {o(6)}/>')
    for i in range(11):
        g += (f'<path d="M{-78+i*16},44 v62" fill="none" stroke="#b9a87e"'
              f' stroke-width="7" opacity=".55"/>')
    # ВЯЗКА: ёлочка по всему полю, не просто линии
    for i in range(5):
        yy = -128 + i * 50
        g += (f'<path d="M-72,{yy} q74,22 148,0" fill="none" stroke="#c2ae82"'
              f' stroke-width="7" opacity=".6"/>')
        for k in range(6):
            xx = -66 + k * 28
            g += (f'<path d="M{xx},{yy+20} l13,-17 l13,17" fill="none" stroke="#cdb98d"'
                  f' stroke-width="5" opacity=".5"/>')
    # ЖАККАРДОВАЯ ПОЛОСА — красный акцент, по ней варежка и опознаётся
    g += (f'<path d="M-82,-54 q82,26 164,0 l-3,46 q-80,26 -158,-2 z"'
          f' fill="{ob.ALYJ}" opacity=".8" {o(4)}/>')
    # ромбики, а не зигзаг: острая «ёлочка» на красной полосе читалась зубами
    for k in range(7):
        cx_ = -62 + k * 24
        g += (f'<path d="M{cx_},-46 l11,13 l-11,13 l-11,-13 z" fill="#f6e2c2"'
              f' opacity=".85"/>')
    # ШОВ большого пальца
    g += (f'<path d="M-84,-18 q-40,-26 -50,-78" fill="none" stroke="#b9a87e"'
          f' stroke-width="7" opacity=".7"/>')
    g += f'<ellipse cx="-24" cy="-110" rx="40" ry="26" fill="#ffffff" opacity=".22"/>'
    # верх ладони загибается вниз — «кулак»
    if szhat > .01:
        g += (f'<g transform="rotate({-88*szhat:.1f} -82 -24)">'
              f'<path d="M-88,-24 q34,-176 92,-212 q62,-22 86,46 q20,72 -4,172 q-82,28 -174,-6 z"'
              f' fill="url(#rush)" {o(7)}/>'
              f'<path d="M-62,-150 q66,24 130,2 M-70,-84 q72,24 142,0" fill="none"'
              f' stroke="#cdb98d" stroke-width="7" opacity=".55"/></g>')
    return g + "</g>"


def b6_listok(x, y, w_, h_, t, ph=0.0, ang=0.0, op=1.0, col="url(#list)"):
    """Чистый листок календаря/квитанция: текст на него кладёт over.py."""
    kach = 2.6 * A.w(t, 3.6, ph)
    s = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang + kach:.2f})" opacity="{op:.2f}">'
         + ten(6, h_ * .56, w_ * .5, h_ * .14, .4))
    s += (f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="7"'
          f' fill="{col}" {o(5)}/>')
    s += (f'<path d="M{w_/2 - w_*.2:.0f},{h_/2:.0f} l{w_*.2:.0f},{-h_*.2:.0f} l0,{h_*.2:.0f} z"'
          f' fill="#cdbf9f" opacity=".8"/>')
    s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} h{w_*.5:.0f} l{-w_*.5:.0f},{h_*.4:.0f} z"'
          f' fill="#ffffff" opacity=".2"/>')
    return s + "</g>"


def b6_kvitancia(x, y, w_, h_, ang, t, ph=0.0, op=1.0):
    """Квитанция без названий и цифр: строки только намёком."""
    s = b6_listok(x, y, w_, h_, t, ph, ang, op)
    s += f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f})" opacity="{op*.75:.2f}">'
    for i in range(4):
        s += (f'<line x1="{-w_*.34:.0f}" y1="{-h_*.26 + i*h_*.17:.0f}"'
              f' x2="{w_*(.3 - .07*i):.0f}" y2="{-h_*.26 + i*h_*.17:.0f}"'
              f' stroke="#9d8f74" stroke-width="5" opacity=".6"/>')
    return s + "</g>"


def b6_konvert(cx, cy, w_, h_, ang=0.0, op=1.0):
    s = (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.2f})" opacity="{op:.2f}">'
         + ten(5, h_ * .66, w_ * .5, h_ * .18, .42))
    s += (f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6"'
          f' fill="url(#krem)" {o(6)}/>')
    s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} L0,{h_*.12:.0f} L{w_/2:.0f},{-h_/2:.0f} z"'
          f' fill="url(#rush)" {o(5)}/>')
    s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} L0,{h_*.12:.0f} L{w_/2:.0f},{-h_/2:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="5" opacity=".35"/>')
    return s + "</g>"


def b6_kniga(x, y, w_, h_, t, ang=0.0):
    s = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f})">'
         + ten(6, h_ * .9, w_ * .52, h_ * .3, .5))
    s += f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="7" fill="url(#tkan)" {o(7)}/>'
    s += (f'<rect x="{-w_/2 + 10:.0f}" y="{-h_/2 + 7:.0f}" width="{w_ - 26:.0f}"'
          f' height="{h_ - 14:.0f}" rx="4" fill="url(#list)" {o(3)}/>')
    for i in range(4):
        s += (f'<line x1="{-w_/2 + 14:.0f}" y1="{-h_/2 + 14 + i*(h_-28)/4:.0f}"'
              f' x2="{w_/2 - 18:.0f}" y2="{-h_/2 + 14 + i*(h_-28)/4:.0f}"'
              f' stroke="#cdbf9f" stroke-width="3" opacity=".8"/>')
    zak = 7 * A.w(t, 2.6)
    s += (f'<path d="M{w_*.18:.0f},{-h_/2:.0f} v{h_*1.5:.0f} l{zak:.0f},18 l{-18 + zak:.0f},-18 z"'
          f' fill="{ob.ALYJ}" {o(3)}/>')
    return s + "</g>"


def b6_banka(x, y, s_, t, ph=0.0):
    """Чистая трёхлитровая банка: стекло с бликом и тенью."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(4, 12, 66, 14, .45)
    g += (f'<path d="M-58,0 q-10,-120 2,-168 l112,0 q12,48 2,168 z" fill="url(#stekl)"'
          f' opacity=".95" {o(6)}/>')
    g += f'<rect x="-44" y="-194" width="88" height="30" rx="8" fill="url(#stekl)" opacity=".98" {o(5)}/>'
    g += f'<ellipse cx="0" cy="-194" rx="44" ry="13" fill="#e8f3fa" opacity=".85" {o(4)}/>'
    g += f'<path d="M-38,-158 q-6,78 -2,132" fill="none" stroke="#ffffff" stroke-width="10" opacity=".5"/>'
    return g + "</g>"


def b6_stakan(x, y, s_, t, par_op=.5):
    """Стакан чая в подстаканнике: пар слабеет — чай остывает."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(4, 10, 46, 11, .4)
    g += f'<path d="M-40,0 l6,-118 h68 l6,118 z" fill="url(#stekl)" opacity=".7" {o(5)}/>'
    g += f'<path d="M-33,-16 l5,-86 h56 l5,86 z" fill="url(#med)" opacity=".85"/>'
    g += f'<path d="M-26,-96 q26,12 52,0" fill="none" stroke="#f2cf8c" stroke-width="6" opacity=".6"/>'
    g += f'<path d="M40,-92 q38,26 2,58" fill="none" {o(8, ZHELEZ)}/>'
    g += "</g>"
    g += baza.par(x, y - 120 * s_, t, 4, par_op, 150 * s_, .42, s_)
    return g


def b6_ochki(x, y, s_, t):
    bl = .3 + .7 * abs(A.w(t, 3.4))
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(4, 22, 110, 12, .4)
    for dx in (-62, 62):
        g += (f'<ellipse cx="{dx}" cy="0" rx="54" ry="38" fill="url(#stekl)" opacity=".55"'
              f' stroke="{MED}" stroke-width="8"/>')
        g += (f'<path d="M{dx-34},-16 q30,-22 60,-6" fill="none" stroke="#ffffff"'
              f' stroke-width="9" opacity="{bl:.2f}"/>')
    g += f'<path d="M-10,-4 q10,-16 20,0" fill="none" stroke="{MED}" stroke-width="8"/>'
    g += f'<path d="M-114,-10 q-46,8 -58,38" fill="none" stroke="{MED}" stroke-width="8"/>'
    return g + "</g>"


def b6_vedro(x, y, s_, t, kach=0.0):
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({kach:.2f}) scale({s_:.3f})">'
    g += ten(0, 12, 78, 17, .5)
    g += f'<path d="M-72,-152 h144 l-18,152 h-108 z" fill="url(#zhel)" {o(7)}/>'
    g += f'<ellipse cx="0" cy="-152" rx="72" ry="19" fill="url(#zhel)" {o(6)}/>'
    g += f'<ellipse cx="0" cy="-152" rx="57" ry="13" fill="#262c33" opacity=".6"/>'
    g += f'<path d="M-72,-170 q72,-90 144,0" fill="none" {o(9, ZHELEZ)}/>'
    g += f'<path d="M-52,-122 l10,120" fill="none" stroke="#e3ebf2" stroke-width="8" opacity=".4"/>'
    return g + "</g>"


def b6_korobka(x, y, w_, h_, t, ang=0.0, op=1.0):
    s = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f})" opacity="{op:.2f}">'
         + ten(6, h_ * .56, w_ * .5, h_ * .16, .45))
    s += (f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6"'
          f' fill="url(#solom)" {o(6)}/>')
    s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} h{w_:.0f} l{-w_*.16:.0f},{-h_*.3:.0f}'
          f' h{-w_*.68:.0f} z" fill="#d4b267" {o(5)}/>')
    s += (f'<line x1="0" y1="{-h_/2:.0f}" x2="0" y2="{h_/2:.0f}" stroke="#a07c2e"'
          f' stroke-width="7" opacity=".7"/>')
    return s + "</g>"


def b6_ochistka(x, y, ang, s_, op=1.0):
    """Картофельная кожурка: витая лента."""
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.0f}) scale({s_:.3f})"'
            f' opacity="{op:.2f}"><path d="M-44,0 q22,-30 50,-10 q28,20 48,-6"'
            f' fill="none" stroke="#b07c42" stroke-width="18" stroke-linecap="round"/>'
            f'<path d="M-44,0 q22,-30 50,-10 q28,20 48,-6" fill="none" stroke="#e4c48d"'
            f' stroke-width="7" stroke-linecap="round" opacity=".7"/></g>')


def b6_prischepka(x, y, ang, s_=1.0):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f}) scale({s_:.3f})">'
            f'<rect x="-13" y="-6" width="26" height="62" rx="7" fill="url(#derev)" {o(4)}/>'
            f'<rect x="-13" y="-6" width="11" height="62" rx="5" fill="#8d6440" opacity=".7"/>'
            f'<path d="M-11,10 h22" stroke="{ZHELEZ}" stroke-width="5"/></g>')


def b6_pyos(x, y, t, s_=1.0, col="#6b5a46"):
    hv = 28 * A.w(t, .72)
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 8, 90, 16, .45)
    g += (f'<g transform="rotate({hv:.1f} -66 -74)"><path d="M-66,-74 q-46,-26 -42,-78"'
          f' fill="none" stroke="{col}" stroke-width="18" stroke-linecap="round"/></g>')
    g += f'<ellipse cx="0" cy="-68" rx="82" ry="45" fill="{col}" {o(6)}/>'
    for nx in (-48, -16, 28, 60):
        g += f'<rect x="{nx}" y="-36" width="19" height="42" rx="9" fill="{col}" {o(4)}/>'
    g += f'<circle cx="76" cy="-114" r="37" fill="{col}" {o(6)}/>'
    g += f'<path d="M102,-106 l30,7 l-28,15 z" fill="{col}" {o(4)}/>'
    g += f'<path d="M54,-142 l-8,-36 l32,17 z" fill="{col}" {o(4)}/>'
    g += f'<circle cx="88" cy="-122" r="4.6" fill="{K}"/>'
    return g + "</g>"


def b6_venik(x, y, t, s_=1.0, ang=0.0):
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f}) scale({s_:.3f})">'
    g += f'<rect x="-13" y="-320" width="26" height="210" rx="12" fill="url(#derev)" {o(5)}/>'
    g += f'<path d="M-46,-120 h92 l34,138 q-80,26 -160,0 z" fill="url(#solom)" {o(6)}/>'
    r = random.Random(21)
    for i in range(13):
        dx = -52 + i * 9
        g += (f'<path d="M{dx},-116 q{r.uniform(-12,12):.0f},70 {dx*.34 + r.uniform(-16,16):.0f},142"'
              f' fill="none" stroke="#c2982f" stroke-width="5" opacity=".75"/>')
    g += f'<path d="M-48,-96 q50,16 100,0" fill="none" stroke="{ob.ALYJ2}" stroke-width="11"/>'
    return g + "</g>"


def b6_taz(x, y, w_, t, pena=1.0):
    """Таз с мокрым бельём: вода, бельё комками, пена оседает."""
    h_ = w_ * .34
    s = ten(x, y + h_ * .5, w_ * .55, h_ * .3, .5)
    s += (f'<path d="M{x-w_/2:.0f},{y-h_*.5:.0f} h{w_:.0f} l{-w_*.1:.0f},{h_:.0f}'
          f' h{-w_*.8:.0f} z" fill="url(#zhel)" {o(7)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.5:.0f}" rx="{w_/2:.0f}" ry="{h_*.2:.0f}"'
          f' fill="url(#zhel)" {o(6)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.48:.0f}" rx="{w_*.43:.0f}" ry="{h_*.16:.0f}"'
          f' fill="url(#voda)" opacity=".92"/>')
    for i, dx in enumerate((-.22, .04, .26)):
        s += (f'<ellipse cx="{x + dx*w_:.0f}" cy="{y-h_*.52 + 8*A.w(t,4.0,i*.3):.0f}"'
              f' rx="{w_*.15:.0f}" ry="{h_*.11:.0f}" fill="url(#krem)" opacity=".92" {o(4)}/>')
    r = random.Random(33)
    for i in range(26):
        u = (i / 26.0 + .04)
        rr = (12 + 24 * r.random()) * (.25 + .75 * pena)
        s += (f'<circle cx="{x + (u-.5)*w_*.8:.0f}"'
              f' cy="{y - h_*.5 - 10 + 14*A.w(t, 3.0, i*.14):.0f}" r="{rr:.1f}"'
              f' fill="#ffffff" opacity="{.2 + .55*pena*abs(A.w(t, 2.4, i*.11)):.2f}"/>')
    s += (f'<path d="M{x-w_*.42:.0f},{y-h_*.3:.0f} l{w_*.06:.0f},{h_*.72:.0f}"'
          f' fill="none" stroke="#e3ebf2" stroke-width="9" opacity=".4"/>')
    return s


def b6_boke(t, tochki, seed=5, r_=34):
    """Огоньки ёлки/гирлянды расфокусом — тёплое пятно для дальнего плана."""
    rr = random.Random(seed)
    s = ""
    for i, (bx, by) in enumerate(tochki):
        col = (SVET, ob.ALYJ, ob.ZOLOTO, "#8fd6ff")[i % 4]
        gor = .28 + .62 * (.5 + .5 * math.sin(2 * math.pi * (t / (1.8 + (i % 5) * .35) + i * .21)))
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r_ * rr.uniform(.7, 1.35):.0f}"'
              f' fill="{col}" opacity="{gor * .32:.2f}"/>')
        s += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r_*.3:.0f}" fill="{col}" opacity="{gor:.2f}"/>'
    return s


def girlyanda_iz_semi_flazhkov(t):
    """Смена главы: вдоль стены избы натянута гирлянда из семи флажков,
    бабушка и внучка стоят под ней со спины.
    Живое: номера загораются на флажках по очереди; гирлянда провисает и
    снова натягивается; огоньки за окном мигают."""
    x0, shir, y0 = 120, 1500, 210
    # провисла — потянули: вся гирлянда идёт вниз и возвращается
    dy = 54 - 54 * A.out(A.seg(t, .7, 1.5)) + 7 * A.w(t, 2.6)

    nebo_v = (f'<rect x="110" y="470" width="420" height="300" fill="{NOCH}"/>'
              + b6_boke(t, [(180, 690), (258, 650), (338, 712), (420, 664), (496, 718)], 3, 26)
              + baza.sneg_letit(t, 16, 9, .55))

    s = SL(Z_NEBO, b6_stena("#20283f", "#131a2c"))
    dal = baza.brevna(-20, 60, W + 40, 880, hh=96)
    dal += baza.okno_izby(110, 470, 420, 300, t, vid=nebo_v, moroz=.35)
    dal += baza.polovicy(905)
    s += SL(Z_DAL, dal)

    sred = baza.mebel_hlam(640, 900, 480, t, 13)
    sred += ob.elka(1700, 1015, 540, t, seed=6)
    sred += f'<g transform="translate(0,{dy:.1f})">' + ob.flazhki(x0, y0, shir, 7, t) + "</g>"
    # номера на флажках — подпись ВНУТРИ предмета, задание просит её прямо
    cx_, cy_ = x0 + shir / 2, y0 + 60
    for i in range(7):
        u = (i + .5) / 7
        fx = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx_ + u * u * (x0 + shir)
        fy = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy_ + u * u * y0 + dy
        gl = A.out(A.seg(t, 1.3 + i * .52, .42))
        if gl > .01:
            sred += (f'<circle cx="{fx:.0f}" cy="{fy + 44:.0f}" r="34" fill="{SVET}"'
                     f' opacity="{gl * .45:.2f}"/>')
            sred += (f'<text x="{fx:.0f}" y="{fy + 62:.0f}" text-anchor="middle"'
                     f' font-family="DejaVu Serif" font-size="46" font-weight="bold"'
                     f' fill="#2a1d12" opacity="{gl:.2f}">{i + 1}</text>')
    s += SL(Z_SRED, sred)

    per = ob.figura(1180, 1090, 560, t, kant="#f0c070", platok=True)
    per += ob.figura(1370, 1094, 410, t, col="#2b2030", kant="#f0c070", ph=.4)
    per += baza.ramka_pp("levo", "#0d0b14", .55)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1720, 700, 620, 520, .3) + baza.vinetka(.4))
    return s


def pustoy_karman_pidzhaka(t):
    """Крупно боковой карман праздничного пиджака на спинке стула.
    Живое: карман просвечивает и внутри пусто; нитка качается; пиджак
    покачивается на спинке."""
    kach = 1.3 * A.w(t, 4.6)
    skvoz = .10 + .20 * abs(A.w(t, 2.7))
    nit = 9 * A.w(t, 2.1)

    s = SL(Z_NEBO, b6_stena("#1c2439", "#101728"))
    dal = baza.okno_izby(1430, 190, 380, 300, t,
                         vid=f'<rect x="1430" y="190" width="380" height="300" fill="{NOCH}"/>'
                             + b6_boke(t, [(1490, 400), (1580, 350), (1680, 410), (1760, 360)], 7, 24),
                         moroz=.4)
    dal += b6_boke(t, [(170, 420), (250, 330), (330, 440), (120, 560), (300, 600)], 4, 54)
    dal += baza.polovicy(930)
    s += SL(Z_DAL, dal)

    sred = b6_g("pidzh", "#46557a", "#1a2133") + b6_g("podkl", "#f3e4c2", "#c3a878")
    # стул
    sred += ten(820, 1010, 420, 40, .55)
    for sx in (430, 1210):
        sred += f'<rect x="{sx}" y="190" width="40" height="740" rx="14" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="430" y="200" width="820" height="46" rx="16" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="430" y="470" width="820" height="34" rx="12" fill="url(#derev)" {o(6)}/>'
    # пиджак
    sred += f'<g transform="rotate({kach:.2f} 840 230)">'
    sred += ten(850, 955, 350, 34, .5)
    # корпус пиджака: плечи уже, пола шире
    sred += ('<path d="M560,250 q140,-70 280,-62 q150,-8 290,66 q36,330 18,650'
             ' q-156,54 -318,48 q-166,4 -300,-54 q-14,-320 30,-648 z"'
             f' fill="url(#pidzh)" {o(8)}/>')
    # воротник и лацканы клином
    sred += ('<path d="M840,188 l-120,70 l70,290 l54,-186 z" fill="#2b3450" {}/>'.format(o(6)))
    sred += ('<path d="M840,188 l122,72 l-62,288 l-56,-184 z" fill="#2b3450" {}/>'.format(o(6)))
    sred += ('<path d="M840,188 l-120,70 l34,-96 q86,-28 172,2 l36,96 z"'
             f' fill="#36426a" {o(6)}/>')
    # рукав свисает вправо
    sred += ('<path d="M1118,286 q104,56 112,196 q10,170 -34,330 q-72,24 -112,-16'
             ' q34,-250 14,-492 z" fill="#38456b" {}/>'.format(o(7)))
    # КАРМАН: ткань просвечивает, внутри пусто
    sred += f'<rect x="648" y="572" width="340" height="212" rx="18" fill="#394668" {o(7)}/>'
    sred += (f'<rect x="668" y="596" width="300" height="168" rx="12" fill="url(#podkl)"'
             f' opacity="{skvoz:.2f}"/>')
    sred += ('<path d="M668,596 h300 v168 h-300 z" fill="none" stroke="#f3e4c2"'
             f' stroke-width="4" opacity="{skvoz + .24:.2f}" stroke-dasharray="14 12"/>')
    # клапан кармана
    sred += (f'<path d="M640,534 h356 q10,34 -4,52 q-176,22 -348,0 q-14,-20 -4,-52 z"'
             f' fill="#2f3b5c" {o(6)}/>')
    sred += ('<path d="M652,546 q174,-20 334,-4" fill="none" stroke="#8ea0c6"'
             ' stroke-width="7" opacity=".45"/>')
    # нитка внутри кармана — просвечивает
    sred += (f'<path d="M712,610 q{36 + nit:.0f},78 {14 + nit*1.6:.0f},152" fill="none"'
             f' stroke="#efe0bd" stroke-width="5" opacity="{skvoz + .36:.2f}"/>')
    sred += "</g>"
    s += SL(Z_SRED, sred)

    # нитка, свисающая из угла кармана
    per = (f'<g transform="rotate({kach:.2f} 840 230)">'
           f'<path d="M972,778 q{14 + nit:.0f},80 {-10 + nit*2.1:.0f},156" fill="none"'
           f' stroke="#efe0bd" stroke-width="6" stroke-linecap="round"/>'
           f'<circle cx="{962 + nit*2.1:.0f}" cy="936" r="8" fill="#efe0bd"/></g>')
    per += baza.ramka_pp("oba", "#0b0a12", .6)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(250, 470, 440, 400, .3) + baza.vinetka(.44))
    return s


def moneta_pod_tarelkoy(t):
    """Праздничный стол крупно: край тарелки приподнят, под неё сама ложится
    сложенная купюра и три монеты (рук не рисуем — правило 6).
    Живое: тарелка приподнимается; монеты ложатся; свеча рядом горит."""
    pod = A.ease(A.seg(t, .35, .95)) * (1 - .3 * A.ease(A.seg(t, 2.8, .8)))
    kx = 430 + 250 * A.ease(A.seg(t, .7, .8))

    s = SL(Z_NEBO, b6_stena("#1e2740", "#121a2c"))
    dal = baza.brevna(-20, 60, W + 40, 560, hh=92)
    dal += ob.girlyanda(-60, 210, W + 60, 230, t, 14, 120)
    dal += b6_boke(t, [(180, 390), (330, 330), (1600, 360), (1780, 300)], 8, 46)
    s += SL(Z_DAL, dal)

    sred = ob.stol_prazdnik(-80, 620, W + 160, t)
    sred += (f'<rect y="654" width="{W}" height="{H - 654}" fill="url(#rush)"/>')
    sred += (f'<path d="M0,690 q480,46 960,10 q480,-36 960,28" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".4"/>')
    sred += baza.svecha(1560, 480, t, .2, 1.7, 100)
    sred += ob.bokal(1760, 660, t, .9, .3)
    sred += ob.mandarin(190, 640, 1.2, .4, t)
    s += SL(Z_SRED, sred)

    per = ""
    # купюра въезжает под приподнятый край тарелки
    per += b6_kupyura(kx, 760, 290, 132, -7, min(1.0, A.seg(t, .7, .4)), slozh=True)
    # три монеты ложатся одна за другой
    for i in range(3):
        k = A.out(A.seg(t, 1.05 + i * .32, .5))
        if k > .01:
            per += b6_moneta(500 + i * 128, 836 - 210 * (1 - k), 56, 34, t, i * .3, min(1.0, k * 1.6))
            per += baza.teplo(500 + i * 128, 836 - 210 * (1 - k), 120, 100, .30)
    per += b6_tarelka(1080, 724, 340, t, pod)
    per += baza.ramka_pp("levo", "#0c0a10", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1500, 520, 520, 450, .34) + baza.vinetka(.4))
    return s


def moneta_katitsya_cherez_god(t):
    """От тарелки монета катится по дорожке из двенадцати плиток-месяцев.
    Живое: монета катится; на пройденных плитках остаются монетки; плитки
    подсвечиваются одна за другой."""
    p = A.ease(A.seg(t, .3, 6.0))
    cur = p * 12.0
    bx0, shag = 196, 134

    s = SL(Z_NEBO, b6_stena("#232b44", "#121a2c"))
    dal = baza.brevna(-20, 40, W + 40, 560, hh=94)
    dal += ob.elka(1700, 640, 430, t, seed=9)
    dal += ob.girlyanda(-60, 130, W + 60, 150, t, 15, 110)
    dal += b6_boke(t, [(210, 330), (350, 270), (120, 440)], 8, 48)
    s += SL(Z_DAL, dal)

    sred = b6_g("plit", "#9a8d78", "#52483a")
    sred += (f'<rect y="640" width="{W}" height="{H - 640}" fill="url(#rush)"/>')
    sred += (f'<rect y="640" width="{W}" height="20" fill="#cdb98d"/>')
    sred += (f'<path d="M0,742 q480,44 960,8 q480,-34 960,26" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".3"/>')
    for i in range(12):
        x = bx0 + i * shag
        y = 862 - i * 4
        w_ = 132 - i * 1.6
        gor = 1.0 if cur > i + .35 else (.24 + .5 * A.seg(t, .3 + i * .45, .3))
        nak = (-4.5, 3.0, -2.0, 5.0, -3.5, 1.5)[i % 6]
        sred += ten(x + 6, y + 34, w_ * .55, 16, .45)
        sred += f'<g transform="rotate({nak} {x} {y})">'
        sred += (f'<rect x="{x - w_/2:.0f}" y="{y - 26:.0f}" width="{w_:.0f}" height="52"'
                 f' rx="10" fill="url(#plit)" {o(5)}/>')
        # щербины и шов: камень, а не чёрточка схемы
        sred += (f'<path d="M{x - w_/2 + 6:.0f},{y + 20:.0f} h{w_ - 12:.0f}" fill="none"'
                 f' stroke="#43392c" stroke-width="6" opacity=".55"/>')
        sred += (f'<circle cx="{x - w_*.28:.0f}" cy="{y + 6:.0f}" r="5" fill="#43392c"'
                 f' opacity=".4"/>'
                 f'<circle cx="{x + w_*.22:.0f}" cy="{y - 4:.0f}" r="4" fill="#43392c"'
                 f' opacity=".35"/>')
        sred += (f'<rect x="{x - w_/2 + 8:.0f}" y="{y - 19:.0f}" width="{w_ - 16:.0f}"'
                 f' height="38" rx="7" fill="{ob.ZOLOTO}" opacity="{.18 + .55*gor:.2f}"/>')
        sred += (f'<path d="M{x - w_/2 + 11:.0f},{y - 14:.0f} h{w_*.5:.0f}" fill="none"'
                 f' stroke="#ffffff" stroke-width="5" opacity="{.22 + .4*gor:.2f}"/>')
        if gor > .9:
            sred += baza.teplo(x, y, w_ * .9, 70, .3)
        sred += '</g>'
        if cur > i + .6:
            pop = A.out(min(1.0, (cur - i - .6) * 3.2))
            sred += b6_moneta(x, y - 36, 22 * pop, 14 * pop, t, i * .17, 1.0, False)
    s += SL(Z_SRED, sred)

    per = b6_tarelka(120, 838, 250, t, .2)
    mx = bx0 + 46 + cur * shag
    my = 808 - cur * 4
    rx = 11 + 41 * abs(math.cos(cur * 2.3))
    per += ten(mx + 4, my + 60, 44, 15, .5)
    per += (f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{rx:.1f}" ry="46" fill="url(#zol)" {o(6)}/>')
    per += (f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{rx*.55:.1f}" ry="27" fill="none"'
            f' stroke="{ob.ZOLOTO2}" stroke-width="5" opacity=".65"/>')
    per += (f'<ellipse cx="{mx - rx*.25:.0f}" cy="{my - 16:.0f}" rx="{rx*.3:.1f}" ry="12"'
            f' fill="#fff8de" opacity="{.4 + .6*abs(A.w(t, 1.2)):.2f}"/>')
    per += baza.teplo(mx, my, 180, 160, .45)
    per += baza.ramka_pp("levo", "#0c0b12", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.42))
    return s


def tri_monetki_na_ladoni(t):
    """Крупно раскрытая вязаная варежка (ладонь играет предмет — правило 6),
    на ней три мелкие монетки.
    Живое: монетки пересчитываются по одной; ладонь закрывается; рукав
    кофты подрагивает."""
    szhat = A.ease(A.seg(t, 2.45, .85))
    schet = (t * 1.15) % 3.3

    s = SL(Z_NEBO, b6_stena("#232b42", "#141a2b"))
    dal = baza.brevna(-20, 40, W + 40, 700, hh=98)
    dal += baza.lampa(1560, 560, t, 1.25, abazhur=True)
    dal += b6_boke(t, [(250, 300), (360, 240), (170, 400)], 6, 48)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 830, W + 120, 46, False)
    sred += (f'<path d="M-60,876 h{W+120} v140 q-520,50 -1040,8 q-460,-38 -1040,16 z"'
             f' fill="url(#rush)" {o(6)}/>')
    sred += b6_varezhka(800, 820, 2.2, t, szhat, .0, False, 2.2)
    s += SL(Z_SRED, sred)

    per = ""
    for i in range(3):
        aktiv = 1.0 if (i <= schet < i + 1) else 0.0
        podn = 20 * aktiv * abs(A.w(t, .9, i * .2))
        op = max(0.0, 1.0 - A.seg(t, 2.55 + i * .06, .3))
        per += b6_moneta(680 + i * 120, 560 - podn, 48, 30, t, i * .33, op)
        if aktiv and op > .3:
            per += baza.teplo(680 + i * 120, 560 - podn, 130, 110, .45)
    per += baza.ramka_pp("oba", "#0c0b13", .55)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1540, 620, 640, 520, .3) + baza.vinetka(.46))
    return s


def rebenok_zaglyadyvaet_pod_tarelku(t):
    """МОСТИК В ПАМЯТЬ: край стола на уровне детских глаз, тарелка сама
    приподнимается и под ней блестит монета.
    Живое: тарелка приподнимается; монета блестит; ребёнок подаётся вперёд."""
    pod = A.ease(A.seg(t, .5, 1.0))
    vper = A.ease(A.seg(t, .9, 1.3))
    bl = .35 + .65 * abs(A.w(t, 1.5))

    s = SL(Z_NEBO, b6_stena("#4a3524", "#1d1510"))
    dal = baza.brevna(-20, 30, W + 40, 560, hh=96)
    dal += ob.elka(1680, 690, 430, t, seed=12)
    dal += ob.figura(1330, 700, 470, t, col="#2a2018", kant="#f2c47c", platok=True, ph=.3)
    dal += b6_boke(t, [(210, 250), (340, 200), (120, 330)], 2, 52)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 600, W + 120, 54, False)
    sred += (f'<rect y="654" width="{W}" height="{H - 654}" fill="url(#rush)"/>')
    sred += (f'<path d="M0,712 q480,44 960,8 q480,-34 960,26" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".35"/>')
    sred += b6_moneta(760, 640, 52, 30, t, .1)
    sred += baza.teplo(760, 636, 210, 150, .34 + .3 * bl)
    sred += ten(1090, 660, 300, 34, .55)      # контакт со столом
    sred += b6_tarelka(1090, 616, 310, t, pod)
    s += SL(Z_SRED, sred)

    # ребёнок со спины снизу слева: тёмная масса, лиц не рисуем
    rx = 330 + 54 * vper
    ry = 1010 - 36 * vper
    per = ten(rx, 1070, 250, 30, .6)
    per += (f'<path d="M{rx-250:.0f},{H + 20} q10,-230 70,-300 q120,-96 300,-30'
            f' q90,54 96,330 z" fill="#1a1410" stroke="#f2c47c" stroke-width="5"'
            f' stroke-opacity=".55"/>')
    per += (f'<circle cx="{rx + 6:.0f}" cy="{ry - 368:.0f}" r="118" fill="#1a1410"'
            f' stroke="#f2c47c" stroke-width="6" stroke-opacity=".8"/>')
    per += (f'<path d="M{rx-104:.0f},{ry-274:.0f} q110,-54 220,0" fill="none"'
            f' stroke="#f2c47c" stroke-width="6" stroke-opacity=".7"/>')
    per += baza.ramka_pp("pravo", "#120d09", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(900, 560, 900, 700, .3) + baza.vinetka(.52))
    return s


def moneta_v_karmashek_vnuka(t):
    """Монеты сами падают в нагрудные кармашки двоих внуков, клапаны
    прихлопываются, а дальше вглубь уходит цепь маленьких фигурок с монетками.
    Живое: монеты падают в кармашки; клапаны прихлопывают; фигурки бегут вдаль."""
    deti = ((540, 1020, 540, .0), (880, 1026, 490, .45))

    s = SL(Z_NEBO, b6_stena("#2a3049", "#161c2e"))
    dal = baza.brevna(-20, 40, W + 40, 820, hh=96)
    dal += baza.dver(1540, 190, 330, 760, .35, kruchok=True)
    dal += baza.teplo(1700, 560, 360, 440, .5)
    # цепь фигурок уходит вдаль
    for j in range(7):
        u = ((t * .2 + j / 7.0) % 1.0)
        fx = 1120 + u * 700
        fb = 980 - u * 320
        fh = 270 * (1 - u * .74)
        op = max(.1, 1 - u * .72)
        dal += ob.figura(fx, fb, fh, t, col="#232a3e", kant="#e7b96e", ph=j * .21, op=op)
        dal += b6_moneta(fx + fh * .12, fb - fh * .5, fh * .07, fh * .045, t, j * .2, op, False)
    dal += baza.polovicy(950)
    s += SL(Z_DAL, dal)

    sred = ""
    for i, (x, b, h_, ph) in enumerate(deti):
        sred += ob.figura(x, b, h_, t, col="#2d2335", kant="#f0c070", ph=ph)
    s += SL(Z_SRED, sred)

    per = ""
    for i, (x, b, h_, ph) in enumerate(deti):
        px, py = x + h_ * .12, b - h_ * .54
        pw, phh = h_ * .2, h_ * .15
        # кармашек
        per += (f'<rect x="{px - pw/2:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{phh:.0f}"'
                f' rx="7" fill="url(#rush)" {o(5)}/>')
        per += (f'<path d="M{px - pw/2 + 8:.0f},{py + phh*.55:.0f} h{pw - 16:.0f}" fill="none"'
                f' stroke="#cdb98d" stroke-width="5" opacity=".7"/>')
        k = A.out(A.seg(t, .9 + i * 1.2, .7))
        if k < 1.0:
            per += b6_moneta(px, py + phh * .4 - 360 * (1 - k), 26, 26, t, i * .4, 1.0, False)
        klap = A.ease(A.seg(t, 1.65 + i * 1.2, .45))
        per += (f'<g transform="rotate({-78 + 78*klap:.1f} {px - pw/2:.0f} {py:.0f})">'
                f'<rect x="{px - pw/2:.0f}" y="{py - 5:.0f}" width="{pw:.0f}" height="{phh*.46:.0f}"'
                f' rx="6" fill="#bda47a" {o(5)}/></g>')
    per += baza.ramka_pp("levo", "#0c0b13", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.42))
    return s


def protyanutaya_i_zakrytaya_ladon(t):
    """Плашка второго запрета: над столом раскрытая варежка-ладонь тянется
    вперёд, вторая сжимается в кулак над купюрой и покачивает отказом.
    Позади на прищепках два чистых листка — текст на них кладёт over.py.
    Живое: ладонь протягивается; кулак закрывается; листки покачиваются."""
    dx = 120 * A.ease(A.seg(t, .4, 1.0))
    szhat = A.ease(A.seg(t, 1.35, .9))
    otkaz = 8 * A.w(t, 1.05) * A.seg(t, 2.2, .7)

    s = SL(Z_NEBO, b6_stena("#222a42", "#131a2b"))
    dal = baza.brevna(-20, 30, W + 40, 620, hh=96)
    dal += (f'<path d="M820,186 q320,44 980,-6" fill="none" stroke="#5a4c38" stroke-width="6"/>')
    for i, lx in enumerate((1040, 1480)):
        dal += b6_prischepka(lx, 196 + i * 10, -4 + 3 * A.w(t, 4.2, i * .3), 1.1)
        dal += b6_listok(lx, 372 + i * 8, 310, 250, t, i * .35, -3 + 4 * A.w(t, 4.0, i * .3))
    dal += baza.lampa(420, 440, t, 1.1, abazhur=True)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 780, W + 120, 44, False)
    sred += (f'<rect y="824" width="{W}" height="{H - 824}" fill="url(#rush)"/>')
    sred += (f'<path d="M0,878 q480,42 960,8 q480,-32 960,24" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="6" opacity=".35"/>')
    s += SL(Z_SRED, sred)

    per = b6_varezhka(400 + dx, 902, 1.35, t, .0, .2, False, 2.4)
    per += b6_kupyura(1090, 790, 310, 142, -9)
    per += (f'<g transform="rotate({otkaz:.2f} 1260 900)">'
            + b6_varezhka(1260, 876, 1.35, t, szhat, .55, True, 1.4) + "</g>")
    per += baza.ramka_pp("oba", "#0b0a12", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(430, 520, 560, 460, .3) + baza.vinetka(.44))
    return s


def blagopoluchie_uhodit_za_kupyuroy(t):
    """Купюра уходит за дверь, и за ней на золотой нити тянется из дома
    каравай, свет лампы и румянец яблок.
    Живое: золотая нить тянется за дверь; свет лампы тускнеет; яблоки бледнеют."""
    uh = A.ease(A.seg(t, .1, 1.9))
    kx = 880 + 700 * uh
    ky = 540 - 60 * uh
    gasnet = A.ease(A.seg(t, .35, 1.6))
    yabl = b6_mix(ob.ALYJ, "#98918a", A.ease(A.seg(t, .55, 1.5)))

    s = SL(Z_NEBO, b6_stena("#232b42", "#141b2c"))
    dal = baza.brevna(-20, 30, W + 40, 900, hh=96)
    dal += baza.dver(1480, 160, 380, 800, .55, kruchok=True)
    dal += (f'<rect x="1480" y="160" width="190" height="800" fill="#9ec8e8" opacity=".3"/>')
    dal += baza.polovicy(958)
    s += SL(Z_DAL, dal)

    sred = baza.lampa(620, 420, t, 1.2, abazhur=True)
    sred += (f'<ellipse cx="620" cy="620" rx="420" ry="330" fill="url(#teplo)"'
             f' opacity="{.75 * (1 - .7*gasnet):.2f}"/>')
    sred += baza.stol(120, 700, 900, 40)
    sred += baza.karavay(430, 690, 1.5)
    for i, ax in enumerate((700, 800, 756)):
        ay = 686 - (26 if i == 2 else 0)
        sred += ten(ax + 3, ay + 30, 42, 11, .4)
        sred += f'<circle cx="{ax}" cy="{ay}" r="40" fill="{yabl}" {o(5)}/>'
        sred += (f'<circle cx="{ax-13}" cy="{ay-14}" r="12" fill="#ffffff" opacity=".35"/>')
        sred += (f'<path d="M{ax},{ay-40} q8,-16 22,-14" fill="none" stroke="{ZEL}"'
                 f' stroke-width="6" stroke-linecap="round"/>')
    s += SL(Z_SRED, sred)

    per = ""
    for i, (sx, sy) in enumerate(((430, 650), (620, 500), (756, 660))):
        per += (f'<path d="M{sx},{sy} Q{(sx + kx)/2:.0f},{sy - 160 - i*50:.0f} {kx:.0f},{ky:.0f}"'
                f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="{7 - i}"'
                f' stroke-linecap="round" opacity="{.45 + .45*uh:.2f}"/>')
        # блик, бегущий по нити: живое без пунктира
        per += (f'<path d="M{sx},{sy} Q{(sx + kx)/2:.0f},{sy - 160 - i*50:.0f} {kx:.0f},{ky:.0f}"'
                f' fill="none" stroke="#fff3c8" stroke-width="{4 - i*.6:.1f}"'
                f' stroke-linecap="round" stroke-dasharray="40 320"'
                f' stroke-dashoffset="{-t * 150:.0f}" opacity=".8"/>')
    per += b6_kupyura(kx, ky, 300, 138, -11 + 16 * uh, max(0.0, 1.0 - A.seg(t, 2.9, .7)))
    per += baza.ramka_pp("levo", "#0b0a12", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.46))
    return s


def sosed_vozvraschaet_dolg_u_zabora(t):
    """Зимний день у плетня: три монеты сами перелетают через забор к хозяйке,
    на столбе стоит пустая кринка, оба кланяются.
    Живое: монеты переходят из рук в руки; пар изо рта; пёс виляет хвостом."""
    poklon_a = -7 * A.ease(A.seg(t, 2.4, .5)) * (1 - A.ease(A.seg(t, 3.1, .5)))
    poklon_b = 7 * A.ease(A.seg(t, 2.5, .5)) * (1 - A.ease(A.seg(t, 3.2, .5)))

    s = SL(Z_NEBO, baza.nebo("den", t) + baza.oblaka(t, 180, 5, 7, .55))
    dal = baza.ulica_dal(60, 640, 1800, t)
    dal += baza.izba_snaruzhi(1320, 690, 520, t)
    dal += baza.sneg_lezhit(690, 30)
    s += SL(Z_DAL, dal)

    sred = baza.pleten(230, 880, 1460, 210, 11)
    sred += baza.krynka(900, 700, 1.25)
    sred += (f'<g transform="rotate({poklon_a:.2f} 520 920)">'
             + ob.figura(520, 920, 580, t, col="#3b3026", kant="#ffe2a8") + "</g>")
    sred += (f'<g transform="rotate({poklon_b:.2f} 1250 920)">'
             + ob.figura(1250, 920, 556, t, col="#33283a", kant="#ffe2a8", platok=True, ph=.4) + "</g>")
    sred += baza.par(560, 690, t, 4, .5, 150, .4, .9)
    sred += baza.par(1210, 700, t, 4, .45, 140, .38, .85)
    s += SL(Z_SRED, sred)

    per = ""
    for i in range(3):
        u = A.ease(A.seg(t, .6 + i * .45, .95))
        if u > .01:
            mx = 660 + 450 * u
            my = 740 - 190 * math.sin(math.pi * u)
            per += b6_moneta(mx, my, 30, 30, t, i * .3, 1.0, False)
    per += b6_pyos(1640, 960, t, 1.05)
    per += baza.sneg_lezhit(1010, 22)
    per += baza.ramka_pp("levo", "#1b2434", .45)
    s += SL(Z_PERED, per)
    s += baza.sneg_letit(t, 34, 5, .55, .7)
    s += SL(Z_FIX, baza.vinetka(.34))
    return s


def svetyaschiysya_porog_novogo_goda(t):
    """Дверной проём, за ним свет. Человек со спины подходит к порогу, мешок
    с биркой сам сползает с плеч (бирку надписывает over.py).
    Живое: мешок сползает с плеч; свет из проёма льётся; человек распрямляется."""
    idet = A.ease(A.seg(t, .2, 2.5))
    fx = 700 + 250 * idet
    rovno = A.ease(A.seg(t, 1.5, 1.1))
    sk = A.ease(A.seg(t, .95, 1.15))
    puls = .8 + .2 * abs(A.w(t, 2.4))

    s = SL(Z_NEBO, b6_stena("#f6e6bf", "#e0b878"))
    dal = b6_g("proem", "#fff6dc", "#f0c878")
    dal += f'<rect width="{W}" height="{H}" fill="#19202f"/>'
    dal += (f'<path d="M790,1080 V380 q270,-230 540,0 V1080 z" fill="url(#proem)"'
            f' opacity="{puls:.2f}"/>')
    dal += baza.teplo(1060, 640, 620, 620, .8 * puls)
    dal += baza.brevna(-20, 0, 800, 1080, hh=100)
    dal += baza.brevna(1330, 0, 620, 1080, hh=100)
    dal += (f'<path d="M790,1080 V380 q270,-230 540,0 V1080" fill="none" stroke="{K}"'
            f' stroke-width="14"/>')
    s += SL(Z_DAL, dal)

    sred = baza.luch(820, 380, 460, 700, t, .26 * puls)
    sred += (f'<rect x="790" y="986" width="540" height="42" rx="10" fill="url(#derev)" {o(7)}/>')
    sred += ob.figura(fx, 1010, 640 + 60 * rovno, t, col="#201a26", kant="#ffd79a")
    s += SL(Z_SRED, sred)

    # мешок сползает с плеч и остаётся у порога
    mx = fx - 150 + 24 * sk
    my = 1010 - 470 + 430 * sk
    rot = 26 * sk
    per = (f'<g transform="translate({mx:.1f},{my:.1f}) rotate({rot:.1f})">'
           + ten(0, 96, 100, 22, .55)
           + f'<path d="M-96,88 q-24,-150 16,-196 q70,-34 148,2 q34,52 10,194 z"'
             f' fill="url(#solom)" {o(7)}/>'
           + f'<path d="M-80,-104 q78,-36 156,-2" fill="none" stroke="{ob.ALYJ2}" stroke-width="12"/>'
           + f'<path d="M-40,-116 q40,-28 84,-4" fill="none" stroke="#8a6a3a" stroke-width="9"/>'
           + f'<path d="M62,-96 q46,26 44,70" fill="none" stroke="#6b4428" stroke-width="6"/>'
           + b6_listok(118, 2, 104, 76, t, .2, 9) + "</g>")
    per += baza.ramka_pp("oba", "#0b0a10", .72)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.4))
    return s


def zanyatoe_nesut_sosedke(t):
    """Лестничная площадка: стопка — книга с закладкой, чистая трёхлитровая
    банка и конверт — плывёт к открывающейся двери, соседка в дверях всплёскивает.
    Живое: банка покачивается на книге; дверь открывается; соседка всплёскивает."""
    otkr = A.ease(A.seg(t, .8, 1.5))
    kach = 4.2 * A.w(t, 2.2)
    vspl = A.ease(A.seg(t, 2.1, .6))
    dyf = -26 * vspl * (1 - .4 * A.ease(A.seg(t, 3.4, .8)))

    s = SL(Z_NEBO, b6_stena("#39414a", "#20262e"))
    dal = f'<rect y="0" width="{W}" height="980" fill="url(#beton)"/>'
    dal += (f'<rect y="560" width="{W}" height="22" fill="{BETON2}" opacity=".8"/>')
    for i in range(5):
        dal += (f'<rect x="-40" y="{980 + i*26:.0f}" width="{W+80}" height="26"'
                f' fill="{BETON2 if i % 2 else BETON}" opacity=".9" stroke="{K}" stroke-width="3"/>')
    dal += (f'<path d="M60,700 q0,-150 140,-150 h300" fill="none" stroke="{ZHELEZ}"'
            f' stroke-width="18" stroke-linecap="round"/>')
    for i in range(5):
        dal += (f'<path d="M{110 + i*74},700 v-120" fill="none" stroke="{ZHELEZ}"'
                f' stroke-width="10" stroke-linecap="round"/>')
    dal += (f'<circle cx="1000" cy="130" r="42" fill="{SVET}"'
            f' opacity="{.6 + .35*abs(A.w(t, 5.2)):.2f}"/>')
    dal += baza.teplo(1000, 150, 420, 340, .45)
    s += SL(Z_DAL, dal)

    sred = (f'<rect x="1180" y="170" width="430" height="810" fill="{SVET}"'
            f' opacity="{.34*otkr:.2f}"/>')
    sred += baza.dver(1180, 170, 430, 810, otkr * .62, kruchok=True)
    sred += (f'<g transform="translate(0,{dyf:.1f}) rotate({5*vspl*A.w(t,1.1):.2f} 1370 1000)">'
             + ob.figura(1370, 1000, 610, t, col="#2e2436", kant="#f0c070", platok=True) + "</g>")
    s += SL(Z_SRED, sred)

    bx, by = 580, 880
    per = b6_kniga(bx, by, 430, 104, t, 1.4 * A.w(t, 3.0))
    per += f'<g transform="rotate({kach:.2f} {bx:.0f} {by - 52:.0f})">'
    per += b6_banka(bx + 12, by - 56, 1.75, t)
    per += b6_konvert(bx + 18, by - 420, 264, 176, -6 + .6 * kach)
    per += "</g>"
    per += baza.ramka_pp("levo", "#14181e", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.44))
    return s


def stopka_kvitanciy(t):
    """Кухонный стол: веер чистых квитанций под магнитом-мандарином, они сами
    перелетают по одной в стопку «готово».
    Живое: квитанции перекладываются; блик бежит по очкам; чай в стакане остывает."""
    s = SL(Z_NEBO, b6_stena("#2b3348", "#171e2e"))
    dal = baza.doski(-20, 40, W + 40, 640, 150, True, "dosk")
    dal += baza.okno_izby(1380, 150, 440, 350, t,
                          vid=f'<rect x="1380" y="150" width="440" height="350" fill="{NOCH}"/>'
                              + b6_boke(t, [(1450, 400), (1560, 350), (1680, 420), (1770, 340)], 5, 26)
                              + baza.sneg_letit(t, 14, 4, .5),
                          moroz=.45)
    dal += baza.polka(180, 330, 520)
    for i in range(3):
        dal += baza.krynka(280 + i * 170, 324, .72)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 720, W + 120, 46, False)
    sred += (f'<path d="M-60,766 h{W+120} v120 q-520,52 -1040,10 q-460,-40 -1040,16 z"'
             f' fill="url(#rush)" {o(6)}/>')
    sred += b6_stakan(1180, 712, 1.25, t, .52 * (1 - .62 * A.seg(t, 0, 4.2)))
    sred += b6_ochki(820, 790, 1.15, t)
    s += SL(Z_SRED, sred)

    per = ""
    gotovo = 0
    for i in range(6):
        k = A.ease(A.seg(t, .55 + i * .6, .55))
        ang0 = -30 + i * 11
        x0, y0 = 450, 700
        x1, y1 = 1480, 706 - i * 9
        x = x0 + (x1 - x0) * k
        y = y0 + (y1 - y0) * k - 160 * math.sin(math.pi * k)
        ang = ang0 + (4 - ang0) * k
        per += b6_kvitancia(x, y, 260, 200, ang, t, i * .2)
        if k > .98:
            gotovo += 1
    per += ob.mandarin(452, 648, 1.0, .0, t)
    per += (f'<rect x="1340" y="{728 - gotovo*9:.0f}" width="280" height="14" rx="6"'
            f' fill="{MED}" opacity=".45"/>')
    per += baza.ramka_pp("levo", "#0d0c14", .48)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1600, 360, 520, 420, .26) + baza.vinetka(.44))
    return s


def zapiska_na_vtoroe_yanvarya(t):
    """Прихожая: на зеркало сама прикрепляется чистая записка (текст кладёт
    over.py), листки календаря отлетают, и конверт уходит в приоткрытую дверь.
    Живое: записка прикрепляется; листки отлетают; конверт уходит к соседу."""
    pri = A.over(A.seg(t, .3, .65))
    snyat = A.seg(t, 4.0, .4)
    kon = A.ease(A.seg(t, 4.3, 2.0))

    s = SL(Z_NEBO, b6_stena("#2a3148", "#161c2c"))
    dal = baza.doski(-20, 20, W + 40, 700, 160, True, "dosk")
    dal += (f'<path d="M1180,200 h620" fill="none" stroke="{ZHELEZ}" stroke-width="14"/>')
    for i, hx in enumerate((1270, 1400, 1530)):
        dal += (f'<path d="M{hx},200 v44" fill="none" stroke="{ZHELEZ}" stroke-width="8"/>')
        dal += (f'<path d="M{hx-56},250 q56,-30 112,0 l26,270 q-82,30 -164,0 z"'
                f' fill="{[TKAN2, ZEL, TKAN][i]}" opacity=".9" {o(6)}/>')
    dal += (f'<rect x="1600" y="150" width="310" height="830" fill="{SVET}" opacity=".2"/>')
    dal += baza.dver(1600, 150, 310, 830, .35 + .25 * A.ease(A.seg(t, 4.0, 1.2)), kruchok=True)
    dal += ob.figura(1790, 962, 520, t, col="#2a2234", kant="#f0c070", op=.9)
    dal += baza.polovicy(975)
    s += SL(Z_DAL, dal)

    sred = ten(650, 790, 260, 28, .5)
    sred += (f'<rect x="398" y="178" width="504" height="604" rx="18" fill="url(#med)" {o(8)}/>')
    sred += (f'<rect x="428" y="208" width="444" height="544" rx="10" fill="url(#stekl)"'
             f' opacity=".9" {o(5)}/>')
    sred += (f'<g clip-path="url(#zerk)"><clipPath id="zerk"><rect x="428" y="208"'
             f' width="444" height="544" rx="10"/></clipPath>'
             + b6_boke(t, [(520, 560), (640, 470), (760, 580), (700, 330), (540, 350)], 9, 44)
             + f'<path d="M428,640 h444 v112 h-444 z" fill="{SVET}" opacity=".12"/></g>')
    sred += (f'<path d="M444,230 l180,300" fill="none" stroke="#ffffff" stroke-width="16"'
             f' opacity=".22"/>')
    # календарь
    sred += ten(1060, 640, 130, 20, .45)
    sred += f'<rect x="950" y="270" width="230" height="330" rx="12" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="968" y="306" width="194" height="280" rx="8" fill="url(#list)" {o(5)}/>'
    for i in range(3):
        k = A.ease(A.seg(t, 1.5 + i * .5, .85))
        if k < .99:
            sred += b6_listok(1065 + 420 * k, 446 - 230 * k, 190, 272, t, i * .3,
                            -6 + 230 * k, max(0.0, 1 - k * 1.15))
    s += SL(Z_SRED, sred)

    per = ""
    if pri > .02 and snyat < 1.0:
        per += (f'<g transform="translate(652,392) scale({pri:.3f}) translate(-652,{-392 - 54*snyat:.0f})">'
                + b6_listok(652, 392, 282, 240, t, .1, -5, 1 - snyat, "#f6e6a8") + "</g>")
    per += b6_konvert(900 + 760 * kon, 760 - 200 * math.sin(math.pi * kon), 250, 162,
                    -8 + 20 * kon, 1.0 if kon > .02 else 0.0)
    per += baza.ramka_pp("levo", "#0c0b13", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1790, 540, 420, 520, .26) + baza.vinetka(.44))
    return s


def paket_v_ruke_u_nochnoy_dveri(t):
    """Плашка третьего запрета: ночь, дверь квартиры приоткрыта, человек в
    тапочках замер на пороге, пакет висит у него сбоку, часы на двенадцати.
    Живое: пакет покачивается; дверь поскрипывает; стрелки часов на двенадцати."""
    skrip = .42 + .05 * A.w(t, 2.3) + .03 * A.w(t, 5.7, .3)
    kach = 7.5 * A.w(t, 2.15)

    s = SL(Z_NEBO, b6_stena("#1a2033", "#0d1220"))
    dal = baza.doski(-20, 10, W + 40, 740, 162, True, "dosk")
    dal += ob.kuranty(1430, 400, t, .92, 1.0, True)
    dal += (f'<path d="M1700,220 v420" fill="none" stroke="{ZHELEZ}" stroke-width="10"/>')
    dal += (f'<path d="M1644,266 q56,-30 112,0 l24,250 q-80,28 -160,0 z" fill="{TKAN2}"'
            f' opacity=".85" {o(6)}/>')
    dal += baza.polovicy(958)
    s += SL(Z_DAL, dal)

    sred = (f'<rect x="150" y="150" width="440" height="830" fill="#8fb6cf" opacity=".32"/>')
    sred += baza.dver(150, 150, 440, 830, skrip, kruchok=True, cepochka=True)
    sred += (f'<path d="M590,150 l150,-30 v890 l-150,-40 z" fill="#9ec8e8" opacity=".2"/>')
    sred += baza.teplo(640, 560, 420, 520, .22)
    s += SL(Z_SRED, sred)

    per = ob.figura(870, 1050, 760, t, col="#1b1726", kant="#9ec8e8")
    for dx in (-78, 30):
        per += ten(870 + dx + 30, 1056, 70, 16, .55)
        per += (f'<path d="M{870+dx:.0f},1046 q58,-34 116,-4 q6,28 -40,34 q-66,6 -76,-30 z"'
                f' fill="#3c3140" stroke="#9ec8e8" stroke-width="4" stroke-opacity=".6"/>')
    per += b6_g("paket", "#dbe3ec", "#8d99a7")
    per += (f'<g transform="rotate({kach:.2f} 1104 640)">'
            f'<path d="M1104,640 l-34,42 M1104,640 l34,42" fill="none" stroke="#b7c2cd" stroke-width="9"/>'
            f'{ten(1108, 952, 96, 20, .5)}'
            f'<path d="M1034,676 h140 l30,250 q-100,34 -200,0 z" fill="url(#paket)" opacity=".92" {o(6)}/>'
            f'<path d="M1052,712 q52,22 104,0 M1046,800 q58,24 116,0" fill="none"'
            f' stroke="#ffffff" stroke-width="7" opacity=".45"/>'
            f'<path d="M1080,700 q22,110 10,208" fill="none" stroke="#6f7b88"'
            f' stroke-width="6" opacity=".5"/></g>')
    per += baza.ramka_pp("pravo", "#0a0912", .6)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.52))
    return s


def venik_metet_ot_poroga(t):
    """Деревенская горница: веник метёт сор не к двери, а ОТ порога в угол к
    печи; порог остаётся чистым и закрытым.
    Живое: веник метёт; сор собирается в кучку; кот прыгает за веником."""
    hod = .5 + .5 * A.w(t, 2.6)
    vx = 540 + 460 * hod
    kucha = min(1.0, t / 4.4)
    pryg = max(0.0, math.sin(2 * math.pi * (t / 2.2))) ** 3

    s = SL(Z_NEBO, b6_stena("#232b40", "#141a2a"))
    dal = baza.brevna(-20, 20, W + 40, 820, hh=96)
    dal += baza.okno_izby(240, 210, 390, 310, t,
                          vid=f'<rect x="240" y="210" width="390" height="310" fill="{NOCH}"/>'
                              + baza.sneg_letit(t, 16, 6, .5),
                          moroz=.8)
    dal += baza.utvar_izby(700, 340, 520, t, 4)
    s += SL(Z_DAL, dal)

    sred = baza.pech(1260, 330, 580, 650, t)
    sred += baza.dver(60, 250, 320, 720, 0.0, kruchok=True)
    sred += baza.polovicy(910)
    # чистый порог
    sred += (f'<rect x="60" y="930" width="330" height="40" rx="10" fill="url(#derev)" {o(6)}/>')
    sred += (f'<rect x="72" y="938" width="306" height="14" rx="6" fill="#ffffff" opacity=".3"/>')
    s += SL(Z_SRED, sred)

    per = b6_venik(vx, 1000, t, 1.15, -20 + 28 * hod)
    # сор летит в кучку у печи
    r = random.Random(17)
    for i in range(11):
        u = min(1.0, max(0.0, (t - .4 - i * .3) / 1.6))
        sx = vx - 60 + r.uniform(-60, 60) + (1340 - vx + 60) * u
        sy = 1000 + r.uniform(-8, 8) - 26 * math.sin(math.pi * u)
        per += (f'<ellipse cx="{sx:.0f}" cy="{sy:.0f}" rx="{r.uniform(7,14):.0f}"'
                f' ry="{r.uniform(4,8):.0f}" fill="#8b6f3f" opacity=".85"/>')
    per += ten(1360, 1004, 140 * kucha + 30, 20, .5)
    per += (f'<path d="M{1360 - 150*kucha - 30:.0f},1004 q{75*kucha + 15:.0f},{-70*kucha - 16:.0f}'
            f' {150*kucha + 30:.0f},0 z" fill="#8b6f3f" {o(5)}/>')
    per += f'<g transform="translate(0,{-110*pryg:.0f})">' + baza.kot(vx + 250, 980, t, .92) + "</g>"
    per += baza.ramka_pp("levo", "#0c0b12", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1540, 700, 620, 520, .36) + baza.vinetka(.42))
    return s


def dvor_s_kalitkoy_dnem(t):
    """РАЗВИЛКА, свой двор: ясный зимний день, низкое солнце, хозяин в валенках
    идёт с ведром по расчищенной дорожке к калитке.
    Живое: ведро покачивается; калитка открывается; солнце блестит на снегу."""
    idet = A.ease(A.seg(t, .3, 4.3))
    hx = 420 + 430 * idet
    hb = 900 + 70 * idet
    hh = 540 + 70 * idet
    kach = 9 * A.w(t, 1.45)
    otkr = A.ease(A.seg(t, 2.9, 1.7))

    s = SL(Z_NEBO, baza.nebo("den", t, False) + baza.oblaka(t, 200, 5, 3, .55))
    nebo_add = (f'<circle cx="1620" cy="250" r="92" fill="#fff6d6" opacity=".97"/>'
                + baza.teplo(1620, 250, 520, 470, .75))
    s += SL(Z_NEBO, nebo_add)
    dal = baza.ulica_dal(40, 600, 1840, t, True, 9)
    dal += baza.izba_snaruzhi(60, 680, 450, t)
    dal += baza.sneg_lezhit(680, 30)
    s += SL(Z_DAL, dal)

    # расчищенная дорожка: от переднего края к калитке
    sred = (f'<path d="M420,1090 L1040,836 h240 L1700,1090 z" fill="#c2b391"'
            f' opacity=".85" {o(5)}/>')
    sred += (f'<path d="M520,1090 L1070,850 h180 L1600,1090 z" fill="#d8caa6" opacity=".6"/>')
    sred += baza.pleten(900, 880, 1020, 200, 9)
    # калитка в створе плетня
    sred += f'<rect x="1046" y="688" width="24" height="230" rx="8" fill="url(#derev)" {o(5)}/>'
    sred += f'<rect x="1330" y="688" width="24" height="230" rx="8" fill="url(#derev)" {o(5)}/>'
    sred += (f'<g transform="translate(1070,900) scale({math.cos(math.radians(74*otkr)):.3f},1)'
             f' translate(-1070,-900)">'
             f'<rect x="1070" y="716" width="258" height="196" rx="10" fill="url(#derev)" {o(6)}/>'
             f'<path d="M1080,770 h238 M1080,856 h238 M1080,726 l238,176" fill="none"'
             f' stroke="#a97f4e" stroke-width="13"/></g>')
    s += SL(Z_SRED, sred)

    per = ob.figura(hx, hb, hh, t, col="#2e2a22", kant="#ffe9bd")
    for dx in (-52, 22):
        per += ten(hx + dx + 22, hb + 6, 50, 13, .5)
        per += (f'<path d="M{hx+dx:.0f},{hb - 2:.0f} q46,-28 92,-4 q4,24 -32,28'
                f' q-54,4 -60,-24 z" fill="#4a3a26" {o(4)}/>')
    per += b6_vedro(hx + 128, hb - 190, .62, t, kach)
    per += baza.sneg_lezhit(1030, 26)
    r = random.Random(23)
    for i in range(26):
        sx, sy = r.uniform(0, W), r.uniform(880, 1070)
        per += (f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{r.uniform(2.4,5.2):.1f}"'
                f' fill="#ffffff" opacity="{.25 + .7*abs(A.w(t, 1.4 + r.uniform(0,1.6), i*.13)):.2f}"/>')
    per += baza.ramka_pp("levo", "#5a6d85", .35)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.blik(1560, 300, t, .8, "#cfe6ff", None, .5)
            + baza.begushchiy_blik(t, 9.0, .2, .12) + baza.vinetka(.3))
    return s


def paket_u_dveri_kvartiry(t):
    """РАЗВИЛКА, квартира: калитка растворяется и становится дверью лифта,
    створки сходятся без пассажира, а пакет сам затягивается на два узла и
    встаёт у входной двери на коврик.
    Живое: двери лифта закрываются; узел затягивается; пакет встаёт на коврик."""
    kalit = max(0.0, 1.0 - A.ease(A.seg(t, .15, 1.1)))
    zakr = A.ease(A.seg(t, .55, 1.55))
    uzel = A.ease(A.seg(t, 1.9, 1.1))
    stav = A.out(A.seg(t, 3.0, 1.1))
    sed = 1.0 - .12 * math.sin(math.pi * min(1.0, A.seg(t, 3.8, .45)))

    s = SL(Z_NEBO, b6_stena("#39414c", "#1f252e"))
    dal = f'<rect y="0" width="{W}" height="906" fill="url(#beton)"/>'
    dal += (f'<rect y="520" width="{W}" height="20" fill="{BETON2}" opacity=".75"/>')
    if kalit > .01:
        dal += f'<g opacity="{kalit:.2f}">' + baza.pleten(240, 880, 700, 200, 7) + "</g>"
    dal += baza.polovicy(906, "url(#kamen)")
    dal += (f'<rect y="878" width="{W}" height="32" fill="{BETON2}" {o(4)}/>')
    s += SL(Z_DAL, dal)

    sred = ten(760, 1004, 280, 26, .5)
    sred += (f'<rect x="488" y="190" width="546" height="814" rx="10" fill="url(#chug)" {o(8)}/>')
    sred += (f'<rect x="516" y="218" width="490" height="770" fill="#10151c"/>')
    for sgn, x0 in ((1, 516), (-1, 1006)):
        w_ = 245 * zakr
        xx = x0 if sgn > 0 else x0 - w_
        sred += (f'<rect x="{xx:.0f}" y="218" width="{w_:.0f}" height="770"'
                 f' fill="url(#zhel)" {o(6)}/>')
        sred += (f'<rect x="{xx + (w_*.2 if sgn>0 else w_*.6):.0f}" y="260" width="{max(2, w_*.2):.0f}"'
                 f' height="690" fill="#ffffff" opacity=".16"/>')
    sred += (f'<rect x="628" y="120" width="266" height="58" rx="10" fill="url(#chug)" {o(6)}/>')
    for i in range(3):
        sred += (f'<circle cx="{688 + i*84}" cy="149" r="15" fill="{ob.ALYJ if i == 1 else "#3a4049"}"'
                 f' opacity="{.45 + .5*abs(A.w(t, 1.8, i*.3)):.2f}"/>')
    s += SL(Z_SRED, sred)

    # дверь квартиры, коврик и пакет
    per = b6_g("kovr", "#7a5440", "#3c2a20")
    per += (f'<rect x="1340" y="140" width="520" height="880" rx="8" fill="url(#derev)" {o(8)}/>')
    per += (f'<rect x="1384" y="190" width="432" height="340" rx="8" fill="none"'
            f' stroke="{DOSKA2}" stroke-width="10"/>')
    per += f'<circle cx="1800" cy="600" r="18" fill="url(#zhel)" {o(5)}/>'
    per += ten(1560, 1020, 250, 28, .5)
    per += (f'<rect x="1330" y="986" width="470" height="70" rx="10" fill="url(#kovr)" {o(6)}/>')
    for i in range(7):
        per += (f'<line x1="{1360 + i*64}" y1="992" x2="{1360 + i*64}" y2="1050"'
                f' stroke="#2c1f18" stroke-width="5" opacity=".6"/>')
    py = 672 + 128 * stav
    per += b6_g("paket2", "#dde5ee", "#8e9aa7")
    per += (f'<g transform="translate(1540,{py:.1f}) scale({1.18:.2f},{1.18*sed:.3f})">'
            + ten(6, 196, 128, 26, .5)
            + f'<path d="M-132,-46 h264 l34,232 q-166,46 -332,0 z" fill="url(#paket2)"'
              f' opacity=".94" {o(7)}/>'
            + f'<path d="M-104,16 q104,34 208,0 M-96,116 q96,34 192,0" fill="none"'
              f' stroke="#ffffff" stroke-width="9" opacity=".45"/>')
    for i, ux in enumerate((-40, 42)):
        r_ = 40 - 24 * uzel
        per += (f'<path d="M{ux - r_:.0f},-52 q{r_:.0f},-58 {r_*2:.0f},0" fill="none"'
                f' stroke="#c3cdd8" stroke-width="{13 + 7*uzel:.0f}" stroke-linecap="round"/>')
        per += (f'<ellipse cx="{ux:.0f}" cy="-48" rx="{r_*.66:.0f}" ry="{14 - 5*uzel:.0f}"'
                f' fill="none" stroke="#aab6c2" stroke-width="{9 + 4*uzel:.0f}"/>')
    per += "</g>"
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.44))
    return s


def ochistki_i_korobki_na_kuhne(t):
    """Кухня днём в разгар готовки: гора картофельных очистков на газете и
    стопка пустых коробок сами сгребаются в ведро, за окном ещё светло.
    Живое: очистки сгребаются; коробки складываются; солнце за окном низко."""
    s = SL(Z_NEBO, b6_stena("#b7c7d2", "#7e93a4"))
    dal = baza.doski(-20, 0, W + 40, 900, 160, True, "dosk")
    okno_vid = (f'<rect x="1300" y="130" width="500" height="390" fill="#cfe0ec"/>'
                f'<circle cx="1420" cy="440" r="70" fill="#ffe7ad" opacity=".95"/>'
                + baza.teplo(1420, 440, 300, 260, .8)
                + f'<path d="M1300,470 q120,-34 250,-10 q130,24 250,-14 v74 h-500 z"'
                  f' fill="#e9f2f8"/>')
    dal += baza.okno_izby(1300, 130, 500, 390, t, vid=okno_vid, moroz=.12)
    dal += baza.luch(1240, 520, 320, 520, t, .2)
    dal += baza.polka(140, 300, 520)
    for i in range(3):
        dal += baza.krynka(240 + i * 180, 294, .74)
    dal += baza.dver(1832, 180, 240, 790, .3)
    dal += baza.polovicy(900)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 690, 1260, 58)
    sred += (f'<rect x="-60" y="748" width="1260" height="36" rx="8" fill="{DOSKA2}" {o(5)}/>')
    # газета под очистками
    sred += ten(620, 752, 350, 22, .4)
    sred += (f'<path d="M250,672 h740 l-54,76 h-632 z" fill="url(#list)" {o(5)}/>')
    for i in range(6):
        sred += (f'<line x1="{282 + i*8}" y1="{686 + i*10}" x2="{962 - i*9}" y2="{686 + i*10}"'
                 f' stroke="#a9a08c" stroke-width="3" opacity=".6"/>')
    # сама гора очистков на газете
    gora = max(0.0, 1.0 - A.seg(t, 1.6, 4.0))
    if gora > .02:
        sred += (f'<path d="M{620 - 210*gora:.0f},720 q{105*gora:.0f},{-130*gora:.0f}'
                 f' {210*gora:.0f},0 z" fill="#b07c42" opacity="{.9*gora:.2f}" {o(5)}/>')
        rr = random.Random(41)
        for i in range(9):
            sred += b6_ochistka(620 + rr.uniform(-180, 180) * gora,
                              706 - rr.uniform(0, 80) * gora,
                              rr.uniform(-50, 50), 1.1 + .5 * rr.random(), gora)
    # коробки складываются стопкой
    for i in range(4):
        k = A.out(A.seg(t, .9 + i * .45, .7))
        sred += b6_korobka(1090, 646 - i * 86 + 210 * (1 - k), 300, 92, t,
                         -4 + i * 3, min(1.0, k * 1.4))
    s += SL(Z_SRED, sred)

    r = random.Random(29)
    per = ""
    # гора очистков: то, что ещё не улетело, лежит кучей на газете
    for i in range(18):
        u = A.ease(A.seg(t, 1.6 + i * .22, .55))
        ox = 600 + r.uniform(-170, 150)
        oy = 686 + r.uniform(-56, 10)
        tx, ty = 1560, 850
        x = ox + (tx - ox) * u
        y = oy + (ty - oy) * u - 200 * math.sin(math.pi * u)
        per += b6_ochistka(x, y, r.uniform(-60, 60) + 240 * u, 1.1 + .6 * r.random(),
                         1.0 if u < .97 else 0.0)
    per += b6_vedro(1570, 1060, 1.5, t, 2.2 * A.w(t, 3.4))
    per += baza.ramka_pp("levo", "#5d6a76", .4)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.begushchiy_blik(t, 10.0, .3, .1) + baza.vinetka(.32))
    return s


def taz_i_prischepki(t):
    """Плашка четвёртого запрета: таз с мокрым бельём, над ним пустая верёвка
    с прищепками; наволочка сама тянется к верёвке и опускается обратно в таз.
    Живое: прищепки покачиваются; пена в тазу оседает; наволочка опускается в таз."""
    vverh = A.out(A.seg(t, .35, 1.15))
    vniz = A.ease(A.seg(t, 1.85, 1.2))
    ny = 720 - 420 * vverh + 430 * vniz
    nang = -6 + 10 * A.w(t, 2.4) * (1 - vniz)
    pena = 1.0 - .72 * A.seg(t, .2, 3.4)

    s = SL(Z_NEBO, b6_stena("#3d5668", "#1d2c38"))
    dal = b6_g("kafel", "#cfe0e6", "#92acb8")
    for r_ in range(7):
        for c in range(13):
            dal += (f'<rect x="{-20 + c*152:.0f}" y="{-10 + r_*120:.0f}" width="146"'
                    f' height="114" rx="6" fill="url(#kafel)" opacity=".92"'
                    f' stroke="#7e95a2" stroke-width="3"/>')
    dal += baza.okno_izby(1420, 140, 400, 300, t,
                          vid=f'<rect x="1420" y="140" width="400" height="300" fill="{SUMER}"/>'
                              + baza.sneg_letit(t, 14, 7, .5),
                          moroz=.5)
    dal += (f'<rect y="840" width="{W}" height="{H-840}" fill="#6f8290"/>')
    dal += (f'<rect y="832" width="{W}" height="18" fill="#54646f"/>')
    # единственное тёплое пятно: лампочка под потолком
    dal += (f'<path d="M300,0 v96" fill="none" stroke="{K}" stroke-width="6"/>')
    dal += (f'<circle cx="300" cy="130" r="38" fill="{SVET}"'
            f' opacity="{.72 + .22*abs(A.w(t, 5.4)):.2f}" {o(5)}/>')
    dal += baza.teplo(300, 160, 480, 420, .5)
    s += SL(Z_DAL, dal)

    prov = 56 + 8 * A.w(t, 4.0)
    sred = (f'<path d="M80,252 Q960,{252 + prov:.0f} 1860,252" fill="none"'
            f' stroke="#9b8a6e" stroke-width="8"/>')
    for i in range(7):
        u = (i + .5) / 7
        px = (1 - u) ** 2 * 80 + 2 * (1 - u) * u * 970 + u * u * 1860
        py = (1 - u) ** 2 * 252 + 2 * (1 - u) * u * (252 + prov) + u * u * 252
        sred += b6_prischepka(px, py - 6, 6 * A.w(t, 2.5, i * .19), 1.35)
    sred += baza.polka(130, 430, 430)
    sred += baza.krynka(230, 424, .72)
    sred += baza.krynka(380, 424, .6)
    sred += baza.krynka(500, 424, .52)
    # стопка сухого белья на табурете
    sred += ten(290, 1010, 150, 22, .45)
    for i in range(4):
        sred += (f'<rect x="178" y="{896 - i*34:.0f}" width="228" height="34" rx="9"'
                 f' fill="url(#krem)" {o(5)}/>')
    sred += f'<rect x="196" y="930" width="192" height="130" rx="8" fill="url(#derev)" {o(6)}/>'
    s += SL(Z_SRED, sred)

    per = b6_taz(900, 960, 820, t, max(0.0, pena))
    per += (f'<g transform="translate(900,{ny:.1f}) rotate({nang:.2f})">'
            + ten(6, 150, 140, 26, .45)
            + f'<path d="M-160,-130 h320 q24,140 -8,266 q-156,42 -310,0 q-28,-130 -2,-266 z"'
              f' fill="url(#krem)" {o(7)}/>'
            + f'<path d="M-130,-96 q130,34 260,0 M-136,10 q136,38 272,0 M-128,112 q128,34 256,0"'
              f' fill="none" stroke="#cfbf9c" stroke-width="8" opacity=".75"/>'
            + f'<path d="M-150,-120 q150,-26 300,0" fill="none" stroke="#ffffff"'
              f' stroke-width="10" opacity=".35"/></g>')
    per += baza.ramka_pp("oba", "#16222b", .45)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.4))
    return s


# ═══════════════ lok_b7.py ═══════════════

OKNO = (860, 300, 980, 551)


def b7_grad(idd, c1, c2, vert=True):
    x2, y2 = (0, 1) if vert else (1, 0)
    return (f'<linearGradient id="{idd}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def b7_fon(idd, c1, c2):
    """Полнокадровая заливка с запасом под оверскан камеры."""
    return (b7_grad(idd, c1, c2)
            + f'<rect x="-440" y="-340" width="{W+880}" height="{H+680}" fill="url(#{idd})"/>')


def b7_oboi(y0, h_, col, shag=124, op=.14):
    """Обои полосой: без них стена читается пустой заливкой."""
    s = ""
    for i in range(int((W + 880) / shag) + 1):
        x = -440 + i * shag
        s += (f'<rect x="{x:.0f}" y="{y0}" width="{shag*.40:.0f}" height="{h_}"'
              f' fill="{col}" opacity="{op:.2f}"/>')
    return s


def b7_pol(y, idd="b7pol", c1="#8d6440", c2="#432a18"):
    s = b7_grad(idd, c1, c2)
    s += f'<rect x="-440" y="{y}" width="{W+880}" height="{H+680-y}" fill="url(#{idd})"/>'
    for i in range(9):
        yy = y + 22 + i * (H + 240 - y) / 8.0
        s += (f'<line x1="-440" y1="{yy:.0f}" x2="{W+440}" y2="{yy:.0f}"'
              f' stroke="#36210f" stroke-width="3" opacity=".42"/>')
    return s


def b7_plintus(y, h_=36, col="#d9cdb8"):
    return (f'<rect x="-440" y="{y-h_}" width="{W+880}" height="{h_}" rx="6"'
            f' fill="{col}" {o(5)}/>')


def b7_plitka(x, y, w_, h_, step, idd, c1="#e2edf4", c2="#b4cad9"):
    """Кафель: ряды со сдвигом, шов холодный."""
    s = b7_grad(idd, c1, c2)
    for r in range(int(h_ / step) + 1):
        for c in range(int(w_ / step) + 2):
            xx = x + c * step - (step * .5 if r % 2 else 0)
            s += (f'<rect x="{xx:.0f}" y="{y+r*step:.0f}" width="{step-7}" height="{step-7}"'
                  f' rx="7" fill="url(#{idd})" stroke="#9db5c6" stroke-width="3"/>')
    return s


def b7_tuchka(x, y, s_, t, ph=0.0, hmuraya=True, op=.95, col="#8e98a6"):
    """Серая тучка-обида: дышит, губы поджаты. ЛЮДЯМ лиц не рисуем — складка
    рта есть только у тучки, это знак настроения, а не лицо."""
    dy = 8 * s_ * A.w(t, 2.6, ph)
    g = f'<g transform="translate({x:.0f},{y+dy:.1f}) scale({s_:.3f})" opacity="{op:.2f}">'
    g += ten(0, 104, 126, 22, .40)
    g += (f'<path d="M-146,44 q-44,-70 20,-96 q2,-74 80,-68 q52,-46 108,8'
          f' q70,-12 76,64 q10,58 -50,58 z" fill="{col}" {o(7)}/>')
    g += ('<path d="M-112,6 q62,-32 124,-6" fill="none" stroke="#b7c1cd"'
          ' stroke-width="13" stroke-linecap="round" opacity=".65"/>')
    if hmuraya:
        g += f'<path d="M-62,2 q28,-24 56,-4" fill="none" {o(8)} opacity=".85"/>'
        g += f'<path d="M14,0 q26,-22 52,0" fill="none" {o(8)} opacity=".85"/>'
        g += f'<path d="M-34,62 q34,-20 68,0" fill="none" {o(9)}/>'
    g += '</g>'
    return g


def b7_shkaf_stvorka(x, y, w_, h_, idd, otkr=0.0):
    """Дверца шкафа: при otkr=0 стоит на месте, при 1 — закрыта до конца."""
    s = b7_grad(idd, "#8a6039", "#4a2e18")
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10"'
          f' fill="url(#{idd})" {o(8)}/>')
    s += (f'<rect x="{x+34:.0f}" y="{y+44:.0f}" width="{w_-68:.0f}" height="{h_-88:.0f}"'
          f' rx="8" fill="none" stroke="#3a2210" stroke-width="7" opacity=".7"/>')
    s += (f'<ellipse cx="{x+30:.0f}" cy="{y+h_*.52:.0f}" rx="15" ry="26"'
          f' fill="url(#zol)" {o(4)}/>')
    s += (f'<rect x="{x-90:.0f}" y="{y:.0f}" width="92" height="{h_:.0f}"'
          f' fill="#120d09" opacity="{.42*otkr:.2f}"/>')
    return s


def b7_vesh(x, y, w_, h_, col, t, ph=0.0, cvetochek=False, amp=6.0):
    """Платье на плечиках: крючок, плечики, подол качается."""
    kach = amp * A.w(t, 3.1, ph)
    g = f'<g transform="rotate({kach*.5:.2f} {x:.0f} {y:.0f})">'
    g += (f'<path d="M{x:.0f},{y:.0f} q-16,-22 0,-34 q16,12 0,34" fill="none"'
          f' stroke="#9aa3ab" stroke-width="7"/>')
    g += (f'<path d="M{x-w_*.46:.0f},{y+34:.0f} L{x:.0f},{y+4:.0f} L{x+w_*.46:.0f},{y+34:.0f}"'
          f' fill="none" stroke="#6f5436" stroke-width="12" stroke-linecap="round"/>')
    sl_, sr_ = x - w_ * .30, x + w_ * .30
    sy_ = y + 42
    wl_, wr_ = x - w_ * .21, x + w_ * .21
    wy_ = y + 42 + h_ * .34
    hl_, hr_ = x - w_ * .56 - kach * .3, x + w_ * .56 + kach * .3
    hy_ = y + 42 + h_
    for sgn in (-1, 1):
        # РУКАВ: выходит за линию плеча и свисает — иначе платье без плеч
        g += (f'<path d="M{x + sgn*w_*.22:.0f},{sy_+4:.0f}'
              f' q{sgn*w_*.26:.0f},{-h_*.02:.0f} {sgn*w_*.34:.0f},{h_*.10:.0f}'
              f' q{sgn*w_*.03:.0f},{h_*.16:.0f} {-sgn*w_*.07:.0f},{h_*.19:.0f}'
              f' q{-sgn*w_*.13:.0f},{-h_*.08:.0f} {-sgn*w_*.27:.0f},{-h_*.19:.0f} z"'
              f' fill="{col}" {o(6)}/>')
        g += (f'<path d="M{x + sgn*w_*.27:.0f},{sy_+h_*.27:.0f}'
              f' q{sgn*w_*.05:.0f},{h_*.02:.0f} {sgn*w_*.10:.0f},{-h_*.01:.0f}"'
              f' fill="none" stroke="#ffffff" stroke-width="6" opacity=".30"/>')
    g += (f'<path d="M{sl_:.0f},{sy_:.0f} Q{x:.0f},{y+16:.0f} {sr_:.0f},{sy_:.0f}'
          f' L{wr_:.0f},{wy_:.0f} Q{x+w_*.40:.0f},{y+42+h_*.72:.0f} {hr_:.1f},{hy_:.0f}'
          f' Q{x:.0f},{hy_+38:.0f} {hl_:.1f},{hy_:.0f}'
          f' Q{x-w_*.40:.0f},{y+42+h_*.72:.0f} {wl_:.0f},{wy_:.0f} Z"'
          f' fill="{col}" {o(7)}/>')
    g += (f'<path d="M{wl_:.0f},{wy_:.0f} Q{x:.0f},{wy_+20:.0f} {wr_:.0f},{wy_:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="9" opacity=".38"/>')
    g += (f'<path d="M{x-w_*.14:.0f},{sy_+16:.0f} Q{x:.0f},{wy_-10:.0f} {x+w_*.14:.0f},{sy_+16:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="7" opacity=".26"/>')
    if cvetochek:
        r = random.Random(int(x) % 97)
        for i in range(11):
            cx = x + r.uniform(-w_ * .40, w_ * .40)
            cy = y + 120 + r.uniform(0, h_ * .76)
            g += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r.uniform(7,11):.0f}"'
                  f' fill="{ob.ALYJ}" opacity=".55"/>')
    g += '</g>'
    return g


def b7_nozhnicy(x, y, t, s_=1.0, ug=0.0, razvod=1.0, bl=True):
    """Ножницы предметом: лезвия и кольца. Рук нет — они работают сами."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ug:.2f}) scale({s_:.3f})">'
    g += ten(10, 230, 70, 14, .35)
    for sgn in (-1, 1):
        a = sgn * 11 * razvod
        g += (f'<g transform="rotate({a:.2f} 0 60)">'
              f'<path d="M{sgn*13},50 L{sgn*31},-168 q{sgn*13},-20 {sgn*21},2'
              f' L{sgn*32},56 z" fill="url(#zhel)" {o(5)}/>'
              f'<path d="M{sgn*17},40 L{sgn*31},-150" fill="none" stroke="#eef5fb"'
              f' stroke-width="5" opacity="{.75 if bl else .3:.2f}"/>'
              f'<path d="M{sgn*16},70 q{sgn*44},70 {sgn*10},128" fill="none"'
              f' stroke="#4b5159" stroke-width="13"/>'
              f'<ellipse cx="{sgn*30}" cy="226" rx="50" ry="42" fill="none"'
              f' stroke="#4b5159" stroke-width="18"/></g>')
    g += f'<circle cx="0" cy="60" r="13" fill="url(#zol)" {o(4)}/>'
    g += '</g>'
    return g


def b7_konvert(x, y, s_, znak, t, ph=0.0):
    """Конверт со значком: монета, сердечко с градусником, домик с ключом."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(8, 86, 118, 18, .38)
    g += f'<rect x="-130" y="-78" width="260" height="160" rx="10" fill="url(#list)" {o(7)}/>'
    g += (f'<path d="M-130,-78 L0,20 L130,-78" fill="none" stroke="#b6a784"'
          f' stroke-width="7"/>')
    if znak == "moneta":
        g += f'<circle cx="0" cy="34" r="36" fill="url(#zol)" {o(5)}/>'
        g += '<circle cx="-11" cy="24" r="11" fill="#fff0bc" opacity=".7"/>'
    elif znak == "serdce":
        g += (f'<path d="M0,66 q-62,-42 -62,-82 q0,-34 32,-34 q22,0 30,26'
              f' q8,-26 30,-26 q32,0 32,34 q0,40 -62,82 z" fill="{ob.ALYJ}" {o(5)}/>')
        g += ('<path d="M44,6 v-56 q0,-16 16,-16 q16,0 16,16 v56" fill="#eef5fb"'
              f' {o(4)}/><circle cx="60" cy="18" r="17" fill="{ob.ALYJ}" {o(4)}/>')
    else:
        g += (f'<path d="M-60,66 v-58 L0,-40 L60,8 v58 z" fill="{MED}" {o(5)}/>')
        g += f'<path d="M-72,10 L0,-52 L72,10" fill="none" stroke="{UGOL}" stroke-width="12" stroke-linecap="round"/>'
        g += (f'<circle cx="56" cy="44" r="15" fill="none" stroke="url(#zol)" stroke-width="8"/>'
              f'<path d="M56,58 v26 M56,74 h16" fill="none" stroke="url(#zol)" stroke-width="8"/>')
    g += '</g>'
    return g


def b7_svecha_stola(x, y, t, s_=1.0, ph=0.0):
    return baza.svecha(x, y, t, ph, s_, 96)


def shvabra_otdyhaet_v_uglu(t):
    """Вечерний угол с сухой шваброй и ведром, справа двумя листками назад —
    день с распахнутым окном. Живое: мишура на швабре блестит, два листка
    отлетают вправо, дневная швабра ходит по полу."""
    POL = 792
    s = SL(Z_NEBO, b7_fon("b7a_f", "#36465f", "#1b2434"))

    d = b7_oboi(60, POL - 60, "#4c5e78", 130, .20)
    d += (f'<rect x="-440" y="-340" width="{1320}" height="{POL+340}"'
          f' fill="#0d1523" opacity=".32"/>')
    d += f'<line x1="880" y1="-40" x2="880" y2="{POL}" stroke="#0e1725" stroke-width="8" opacity=".55"/>'
    # ДЕНЬ справа — единственное тёплое пятно кадра
    d += ('<linearGradient id="b7a_den" x1="0" y1="0" x2="1" y2="0">'
          '<stop offset="0" stop-color="#e8f1ff" stop-opacity="0"/>'
          '<stop offset=".40" stop-color="#eef4ff" stop-opacity=".55"/>'
          '<stop offset="1" stop-color="#fff0cf" stop-opacity=".92"/></linearGradient>'
          f'<rect x="880" y="-340" width="{W+440-880}" height="{H+680}" fill="url(#b7a_den)"/>')
    # распахнутое окно дневной половины
    ox, oy, ow, oh = 1210, 190, 420, 400
    d += f'<rect x="{ox-22}" y="{oy-22}" width="{ow+44}" height="{oh+44}" rx="8" fill="url(#derev)" {o(7)}/>'
    d += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#dceeff"/>'
    d += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#fff6dd" opacity=".55"/>'
    for sgn, bx in ((-1, ox), (1, ox + ow)):
        d += (f'<g transform="translate({bx},{oy}) skewY({sgn*8})">'
              f'<rect x="{-100 if sgn<0 else 0}" y="0" width="100" height="{oh}"'
              f' fill="url(#stekl)" opacity=".8" {o(6)}/></g>')
    d += baza.luch(ox + 80, oy + oh, 260, POL - oy - oh + 180, t, .26)
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    m = b7_pol(POL, "b7a_p")
    m += (f'<rect x="880" y="{POL}" width="{W+440-880}" height="{H+680-POL}"'
          f' fill="#ffe9bd" opacity=".30"/>')
    # ВЕДРО — сухое, дужка вверх
    bx, by = 492, POL
    m += ten(bx, by + 8, 104, 20, .5)
    m += (f'<path d="M{bx-92},{by-176} h184 l-26,176 h-132 z" fill="url(#zhel)" {o(8)}/>')
    m += (f'<ellipse cx="{bx}" cy="{by-176}" rx="92" ry="26" fill="#2b323a" {o(6)}/>'
          f'<ellipse cx="{bx}" cy="{by-176}" rx="74" ry="18" fill="#1a1f25"/>')
    m += (f'<path d="M{bx-86},{by-186} q86,-150 172,0" fill="none" stroke="#565e68"'
          f' stroke-width="12" stroke-linecap="round"/>')
    m += f'<path d="M{bx-62},{by-150} l-18,140" fill="none" stroke="#eef5fb" stroke-width="10" opacity=".35"/>'
    # ШВАБРА отдыхает: ручка в угол, насадка сухая
    hx1, hy1, hx2, hy2 = 300, POL - 6, 196, 150
    m += ten(hx1, POL + 8, 112, 18, .45)
    m += (f'<path d="M{hx1},{hy1} L{hx2},{hy2}" fill="none" stroke="url(#derev)"'
          f' stroke-width="24" stroke-linecap="round"/>')
    m += (f'<path d="M{hx1-4},{hy1-6} L{hx2-4},{hy2+8}" fill="none" stroke="#c9a173"'
          f' stroke-width="7" opacity=".5"/>')
    m += (f'<g transform="rotate(-7 {hx1} {hy1})">'
          f'<rect x="{hx1-150}" y="{hy1-64}" width="300" height="62" rx="16"'
          f' fill="url(#dosk)" {o(7)}/>'
          f'<path d="M{hx1-134},{hy1-44} h268" stroke="#c9a173" stroke-width="9" opacity=".6"/>')
    for i in range(14):
        lx = hx1 - 136 + i * 21
        m += (f'<path d="M{lx},{hy1-6} q{4*A.w(t,6.0,i*.11):.1f},20 1,34" fill="none"'
              f' stroke="#d8cdb2" stroke-width="15" stroke-linecap="round"/>')
    m += '</g>'
    # БАНТИК ИЗ МИШУРЫ — блестит
    mx, my = int(hx2 + (hx1 - hx2) * .34), int(hy2 + (hy1 - hy2) * .34)
    for sgn in (-1, 1):
        m += (f'<path d="M{mx},{my} q{sgn*96},-86 {sgn*122},10 q{-sgn*46},62 {-sgn*122},-10 z"'
              f' fill="url(#zol)" {o(6)}/>')
        m += (f'<path d="M{mx},{my+8} q{sgn*40},54 {sgn*76},92" fill="none"'
              f' stroke="{ob.ZOLOTO2}" stroke-width="13" stroke-linecap="round"/>')
    m += f'<circle cx="{mx}" cy="{my}" r="26" fill="{ob.ZOLOTO}" {o(6)}/>'
    for i in range(13):
        a = i * .62
        gx = mx + math.cos(a) * (36 + 54 * (i % 3))
        gy = my + math.sin(a) * (28 + 38 * (i % 2))
        bl = .20 + .80 * abs(A.w(t, 1.1 + i * .17, i * .21))
        m += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="{7.5 + 2.5*(i%2):.1f}"'
              f' fill="#fff3c4" opacity="{bl:.2f}"/>')
    # ДНЕВНАЯ ШВАБРА — ходит по полу под окном
    sx = 1340 + 250 * A.w(t, 3.4)
    nak = -6 + 7 * A.w(t, 3.4)
    m += f'<g transform="translate({sx:.0f},0) rotate({nak:.1f} 0 {POL})">'
    m += (f'<path d="M0,{POL} L52,{POL-470}" fill="none" stroke="url(#derev)"'
          f' stroke-width="20" stroke-linecap="round"/>')
    m += (f'<rect x="-120" y="{POL-52}" width="240" height="52" rx="14" fill="url(#dosk)" {o(6)}/>')
    for i in range(11):
        m += (f'<path d="M{-108+i*21},{POL} v26" stroke="#d8cdb2" stroke-width="13"'
              f' stroke-linecap="round" opacity=".9"/>')
    m += (f'<ellipse cx="0" cy="{POL+16}" rx="150" ry="22" fill="#bfe0f2" opacity=".55"/>')
    m += '</g>'
    for i in range(4):
        gx = 1180 + i * 170 + 40 * A.w(t, 4.0, i * .3)
        m += (f'<ellipse cx="{gx:.0f}" cy="{POL+54+i*22}" rx="{70-i*8}" ry="12"'
              f' fill="#ffffff" opacity="{.18+.22*abs(A.w(t,2.4,i*.2)):.2f}"/>')
    s += SL(Z_SRED, m)

    # ДВА ЛИСТКА — отлетают назад, в день
    f = f'<rect x="620" y="268" width="210" height="36" rx="8" fill="url(#zhel)" {o(5)}/>'
    f += f'<rect x="636" y="304" width="178" height="214" rx="8" fill="url(#list)" {o(6)}/>'
    f += '<path d="M652,330 h146 M652,372 h146" stroke="#c3b694" stroke-width="5"/>'
    for i, t0 in enumerate((.45, 1.25)):
        p = A.out(A.seg(t, t0, 1.55))
        if p <= 0:
            continue
        lx = 726 + 560 * p
        ly = 400 - 150 * p + 240 * p * p
        f += (f'<g transform="translate({lx:.0f},{ly:.0f}) rotate({-16-54*p:.1f})"'
              f' opacity="{1-.45*p:.2f}">'
              f'<rect x="-88" y="-108" width="176" height="212" rx="8" fill="url(#list)" {o(6)}/>'
              f'<path d="M-66,-62 h132 M-66,-18 h132" stroke="#c7baa0" stroke-width="5"/></g>')
    s += SL(Z_LETIT, f)

    p = baza._ramka_pp("levo", "#0b0f18", .78)
    s += SL(Z_PERED, p)
    s += SL(Z_FIX, baza._vinetka(.40))
    return s


def merzluyu_prostynyu_vnosyat_v_dom(t):
    """Мостик в память: дверь из сеней в клубах пара, простыня стоит листом
    у стены, девочка прижалась к ней. Живое: пар клубится в дверях, простыня
    медленно обмякает, девочка дышит в неё и жмурится плечами."""
    POL = 836
    s = SL(Z_NEBO, b7_fon("b7b_f", "#3a3a50", "#201d2a"))

    d = b7_oboi(40, POL - 40, "#4e4a63", 118, .18)
    d += baza.brevna(960, 60, 980, POL - 60, 96)
    # дверь из сеней: распахнута, оттуда холодный синий свет
    dx, dy, dw, dh = 110, 180, 330, POL - 180
    d += f'<rect x="{dx-26}" y="{dy-26}" width="{dw+52}" height="{dh+26}" rx="8" fill="url(#derev)" {o(8)}/>'
    d += f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#16233c"/>'
    d += ('<linearGradient id="b7b_seni" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#93bedd" stop-opacity=".85"/>'
          '<stop offset="1" stop-color="#2c3f5e" stop-opacity=".9"/></linearGradient>'
          f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="url(#b7b_seni)"/>')
    d += baza.dver(dx + dw - 40, dy, dw, dh, .72, "url(#derev)", True)
    d += (f'<path d="M{dx},{POL} l{dw},0 l180,220 l-{dw+360},0 z" fill="#bcd6ea"'
          f' opacity=".22"/>')
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    m = b7_pol(POL, "b7b_p", "#8a6038", "#3f2715")
    # ПРОСТЫНЯ стоит листом и медленно обмякает
    ob_ = A.ease(A.seg(t, .9, 3.4))
    px, py = 1240, POL
    volna = 26 * ob_
    m += ten(px, py + 10, 190, 26, .5)
    m += (f'<g transform="rotate({-6 + 9*ob_:.2f} {px} {py})">'
          f'<path d="M{px-150},{py} L{px-134+volna*.4:.0f},{py-620}'
          f' q150,{-34-volna:.0f} 290,{6:.0f} L{px+156},{py} z"'
          f' fill="url(#list)" {o(7)}/>')
    for i in range(4):
        wx = px - 112 + i * 76
        m += (f'<path d="M{wx},{py-584} q{10+volna*.6:.1f},200 {-6:.0f},576"'
              f' fill="none" stroke="#cfd8e4" stroke-width="7" opacity=".7"/>')
    m += (f'<path d="M{px-130},{py-560} q140,{-26-volna:.0f} 280,0" fill="none"'
          f' stroke="{TKAN2}" stroke-width="12" opacity=".75"/>')
    m += (f'<path d="M{px-122},{py-520} l60,300" fill="none" stroke="#ffffff"'
          f' stroke-width="18" opacity=".28"/></g>')
    # иней с простыни — холодное облачко
    for i in range(5):
        k = ((t * .4 + i * .2) % 1.0)
        m += (f'<ellipse cx="{px-200-60*k:.0f}" cy="{py-430-120*k:.0f}"'
              f' rx="{26+54*k:.0f}" ry="{(26+54*k)*.7:.0f}" fill="#d7e8f6"'
              f' opacity="{.34*(1-k):.2f}"/>')
    # МАТЬ: вошла из сеней, идёт к стене
    hod = A.ease(A.seg(t, .2, 2.4))
    m += ob.figura(430 + 320 * hod, POL + 10, 470, t, "#2c2436", "#f0c070", True, ph=.1)
    # ДЕВОЧКА нюхает простыню: вдох поднимает плечи, жмурится всем телом
    vdoh = .5 + .5 * A.w(t, 1.9, .2)
    m += (f'<g transform="translate(0,{-9*vdoh:.1f})">'
          + ob.figura(px - 196, POL + 10, 340 + 10 * vdoh, t, "#352a3e", "#f3cf90",
                      False, ph=.55, profil=True) + '</g>')
    s += SL(Z_SRED, m)

    f = baza.par(dx + dw * .5, POL - 150, t, 6, .62, 430, .34, 1.5)
    f += baza.par(dx + dw * .8, POL - 70, t, 5, .5, 330, .4, 1.2)
    f += baza._ramka_pp("levo", "#0a0d14", .62)
    s += SL(Z_PERED, f)

    fix = f'<rect width="{W}" height="{H}" fill="#c2884a" opacity=".13"/>'
    fix += baza._vinetka(.46)
    s += SL(Z_FIX, fix)
    return s


def stopka_belya_so_skatertyu(t):
    """Полка шкафа крупно: ровная стопка с синей каймой, сверху накрахмаленная
    скатерть. Живое: свет проводит по скатерти вместо ладони, уголок хрустит
    и встаёт, дверца шкафа закрывается справа."""
    s = SL(Z_NEBO, b7_fon("b7c_f", "#4a331f", "#190f07"))

    d = baza.doski(-40, -60, W + 120, 980, 108, True, "dosk")
    d += f'<rect x="-440" y="-340" width="{W+880}" height="{H+680}" fill="#17100a" opacity=".42"/>'
    d += baza.teplo(520, 120, 760, 460, .50)
    d += (f'<rect x="-440" y="-340" width="{W+880}" height="420" fill="#0b0705" opacity=".55"/>')
    # холодный свет из двери справа: иначе весь кадр — коричневое на коричневом
    for i, (rx_, op_) in enumerate(((760, .10), (560, .10), (380, .10), (230, .12))):
        d += (f'<ellipse cx="1960" cy="520" rx="{rx_}" ry="{rx_*1.2:.0f}"'
              f' fill="#5b86b4" opacity="{op_}"/>')
    d += baza.luch(1650, -180, 320, 1180, t, .13)
    s += SL(Z_DAL, d)

    m = ""
    # ПОЛКА
    m += f'<rect x="-40" y="828" width="{W+200}" height="46" rx="10" fill="url(#derev)" {o(8)}/>'
    m += f'<rect x="-40" y="874" width="{W+200}" height="26" fill="#3f2713" opacity=".8"/>'
    m += ten(760, 836, 620, 30, .55)
    # РУШНИКИ стопкой на правом краю полки — красно-золотой акцент и опора
    m += ten(1560, 834, 210, 24, .5)
    for i in range(3):
        yy = 824 - i * 44
        col = (ob.ALYJ, RUSH, ob.ALYJ)[i]
        m += (f'<rect x="{1398+i*8}" y="{yy-42:.0f}" width="340" height="44" rx="12"'
              f' fill="{col}" {o(6)}/>')
        m += (f'<path d="M{1412+i*8},{yy-28:.0f} h312" stroke="{ob.ZOLOTO}"'
              f' stroke-width="7" opacity=".8"/>')
    # свешенный конец рушника — полка читается как полка, а не как линия
    m += (f'<path d="M1420,824 q-12,78 10,150 q34,16 56,-6 q-16,-72 -4,-144 z"'
          f' fill="{ob.ALYJ}" {o(6)}/>'
          f'<path d="M1428,948 h54" stroke="{ob.ZOLOTO}" stroke-width="9" opacity=".85"/>')
    # СТОПКА БЕЛЬЯ с синей каймой
    r = random.Random(4)
    for i in range(7):
        yy = 824 - i * 56
        dx = r.uniform(-14, 14)
        m += (f'<rect x="{250+dx:.0f}" y="{yy-54:.0f}" width="1000" height="56" rx="14"'
              f' fill="url(#list)" {o(6)}/>')
        m += (f'<rect x="{250+dx:.0f}" y="{yy-22:.0f}" width="1000" height="22" rx="8"'
              f' fill="{TKAN2}" opacity=".95"/>')
        m += (f'<rect x="{250+dx:.0f}" y="{yy-30:.0f}" width="1000" height="7"'
              f' fill="#2c4260" opacity=".7"/>')
        m += (f'<path d="M{262+dx:.0f},{yy-42:.0f} h976" stroke="#ffffff"'
              f' stroke-width="7" opacity=".30"/>')
    # СКАТЕРТЬ сверху — накрахмаленная, уголок встаёт
    ug = A.over(A.seg(t, .8, 1.4)) * 52
    m += (f'<path d="M258,352 h988 q16,56 0,110 h-988 q-16,-54 0,-110 z"'
          f' fill="#f7efdc" {o(7)}/>')
    m += (f'<path d="M258,430 h988 q16,80 0,156 h-988 q-16,-78 0,-156 z"'
          f' fill="url(#krem)" {o(7)}/>')
    m += '<path d="M268,436 h968" stroke="#ffffff" stroke-width="9" opacity=".45"/>'
    m += ('<path d="M300,470 q460,-26 900,0" fill="none" stroke="#d7c49c" stroke-width="7"/>'
          '<path d="M300,548 q460,26 900,0" fill="none" stroke="#d7c49c" stroke-width="7"/>')
    for i in range(9):
        cx = 330 + i * 112
        m += (f'<path d="M{cx},500 q16,-22 32,0 q-16,22 -32,0 z" fill="{TKAN2}" opacity=".55"/>')
    m += ten(1180, 586, 150, 22, .45)      # тень под встающим уголком: он не висит
    m += (f'<g transform="rotate({-ug:.1f} 1246 586)">'
          f'<path d="M1246,586 l-176,-30 q-10,-66 6,-126 l170,0 z" fill="url(#krem)" {o(6)}/>'
          f'<path d="M1246,470 l-160,8" stroke="#ffffff" stroke-width="9" opacity=".4"/></g>')
    # СВЕТ ВМЕСТО ЛАДОНИ: полоса проходит по скатерти
    bx = 180 + ((t * 340) % 1500)
    m += (f'<g opacity=".55"><path d="M{bx:.0f},412 l150,0 l-104,180 l-150,0 z"'
          f' fill="#fff8e4" opacity=".55"/>'
          f'<path d="M{bx+54:.0f},412 l44,0 l-104,180 l-44,0 z" fill="#ffffff" opacity=".6"/></g>')
    s += SL(Z_SRED, m)

    zakr = A.ease(A.seg(t, 2.6, 2.6))
    f = b7_shkaf_stvorka(1920 - 760 * zakr, -200, 820, H + 420, "b7c_dv", zakr)
    f += baza._ramka_pp("levo", "#090705", .70)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.44))
    return s


def utyug_i_gotovyy_naryad(t):
    """Гладильная доска в полосе 0-830: утюг делает последний проход по
    скатерти и встаёт на подставку, рядом наряд на спинке стула. Живое:
    утюг идёт, пар валит, наряд покачивается."""
    POL = 940
    s = SL(Z_NEBO, b7_fon("b7d_f", "#3c4a60", "#232a38"))

    d = b7_oboi(30, POL - 30, "#4d5d76", 116, .16)
    d += baza.teplo(400, 240, 620, 420, .40)
    d += f'<rect x="60" y="150" width="300" height="22" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(3):
        d += (f'<rect x="{96+i*92}" y="60" width="72" height="90" rx="10"'
              f' fill="url(#list)" {o(5)}/>')
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    m = b7_pol(POL, "b7d_p", "#8f6744", "#412918")
    # ДОСКА
    bx0, bx1, by = 40, 700, 612
    m += ten(380, POL - 6, 290, 26, .5)
    m += (f'<path d="M{bx0},{by+8} q40,-54 120,-54 h{bx1-bx0-180} q90,0 90,56'
          f' q0,52 -90,52 h{-(bx1-bx0-180)} q-80,0 -120,-54 z" fill="url(#krem)" {o(8)}/>')
    m += (f'<path d="M{bx0+30},{by-14} h{bx1-bx0-120}" stroke="#ffffff" stroke-width="10" opacity=".35"/>')
    for sgn, nx in ((1, 170), (-1, 560)):
        m += (f'<path d="M{nx},{by+54} l{sgn*150},{POL-by-56}" fill="none"'
              f' stroke="#6d757e" stroke-width="18" stroke-linecap="round"/>')
        m += (f'<path d="M{nx+sgn*150},{by+54} l{-sgn*150},{POL-by-56}" fill="none"'
              f' stroke="#565d66" stroke-width="18" stroke-linecap="round"/>')
    # СКАТЕРТЬ на доске
    m += (f'<path d="M{bx0+20},{by-16} h{bx1-bx0-90} q24,96 -40,180 h-{bx1-bx0-240}'
          f' q-60,-80 -40,-180 z" fill="url(#list)" {o(6)}/>')
    m += (f'<path d="M{bx0+60},{by+36} q250,22 500,0" fill="none" stroke="{TKAN2}"'
          f' stroke-width="9" opacity=".7"/>')
    # УТЮГ: проход и посадка на подставку
    hod = A.ease(A.seg(t, .15, 3.0))
    stav = A.out(A.seg(t, 3.3, 1.3))
    ux = 130 + 360 * hod + 80 * stav
    uy = by - 42 - 30 * stav
    m += (f'<g transform="translate({ux:.0f},{uy:.0f})">'
          f'{ten(6, 60, 104, 16, .45)}'
          f'<path d="M-150,22 q86,-26 180,-14 q50,8 54,24 q4,16 -36,18 l-186,0 z"'
          f' fill="#cfd8e2" {o(7)}/>'
          f'<path d="M-146,16 q-10,-66 60,-84 q88,-20 150,22 q22,16 10,42 q-16,26 -220,20 z"'
          f' fill="url(#zhel)" {o(8)}/>'
          f'<path d="M-128,-14 q94,-54 190,-22" fill="none" stroke="#eef5fb" stroke-width="10" opacity=".6"/>'
          f'<path d="M-78,-88 q70,-26 132,8 q22,14 14,40 l-168,0 q-14,-28 22,-48 z"'
          f' fill="{CHUGUN}" {o(6)}/>'
          f'<path d="M-64,-98 q66,-24 124,10" fill="none" stroke="#9aa1a9" stroke-width="11"/>'
          f'<circle cx="80" cy="-18" r="15" fill="url(#zol)" {o(4)}/></g>')
    # ПОДСТАВКА
    m += (f'<rect x="488" y="{by-22}" width="160" height="26" rx="10" fill="#4a5159" {o(5)}/>')
    s += SL(Z_SRED, m)

    f = baza.par(ux - 60, uy - 20, t, 6, .52, 340, .42, 1.1)
    # СТУЛ с нарядом
    sx, sb = 700, POL + 10
    f += ten(sx, sb, 140, 24, .5)
    f += (f'<rect x="{sx-96}" y="{sb-320}" width="192" height="30" rx="10" fill="url(#derev)" {o(7)}/>')
    f += (f'<rect x="{sx-86}" y="{sb-700}" width="26" height="382" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="{sx+62}" y="{sb-700}" width="26" height="382" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="{sx-86}" y="{sb-700}" width="174" height="28" rx="10" fill="url(#derev)" {o(6)}/>')
    f += (f'<rect x="{sx-86}" y="{sb-290}" width="24" height="290" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{sx+62}" y="{sb-290}" width="24" height="290" fill="url(#derev)" {o(5)}/>')
    f += b7_vesh(sx, sb - 712, 250, 400, ob.ALYJ, t, .2, False, 9.0)
    f += baza._ramka_pp("levo", "#0a0e16", .62)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


def tihaya_vannaya(t):
    """Ванная по трём предметам: пустой неподвижный барабан с табличкой-
    мандарином, сложенная сушилка у стены, тряпка на краю ведра. Живое:
    блик ползёт по стеклу, сушилка складывается, тряпка качается."""
    POL = 880
    s = SL(Z_NEBO, b7_fon("b7e_f", "#30465a", "#1a2733"))

    d = b7_plitka(-440, -120, W + 880, POL + 140, 128, "b7e_pl")
    d += f'<rect x="-440" y="-340" width="{W+880}" height="{H+680}" fill="#16222e" opacity=".34"/>'
    d += baza.teplo(980, 60, 820, 420, .34)
    d += baza.teplo(1790, 330, 460, 420, .52)   # свет лампы у двери
    d += f'<rect x="700" y="150" width="520" height="22" rx="8" fill="#c7d6e2" {o(5)}/>'
    for i in range(4):
        d += (f'<rect x="{740+i*110}" y="74" width="54" height="76" rx="10"'
              f' fill="{["#9fc4d8","#e2d2b0","#c0d8c2","#dcc0c6"][i]}" {o(5)}/>')
    s += SL(Z_DAL, d)

    m = b7_plitka(-440, POL, W + 880, 360, 150, "b7e_pol", "#c9d8e4", "#8fa6b6")
    # СТИРАЛЬНАЯ МАШИНА — барабан пуст и неподвижен
    mx, my = 120, POL
    m += ten(mx + 230, my + 10, 250, 26, .5)
    m += (f'<rect x="{mx}" y="{my-520}" width="460" height="520" rx="22"'
          f' fill="url(#krem)" {o(8)}/>')
    m += (f'<rect x="{mx+24}" y="{my-492}" width="412" height="64" rx="12" fill="#cfd9e2" {o(5)}/>')
    for i in range(3):
        m += f'<circle cx="{mx+70+i*58}" cy="{my-460}" r="15" fill="#8d9aa6" {o(4)}/>'
    m += f'<circle cx="{mx+340}" cy="{my-460}" r="30" fill="url(#zhel)" {o(5)}/>'
    m += f'<circle cx="{mx+230}" cy="{my-250}" r="178" fill="#aab8c4" {o(8)}/>'
    m += f'<circle cx="{mx+230}" cy="{my-250}" r="146" fill="url(#stekl)" opacity=".92" {o(6)}/>'
    m += f'<circle cx="{mx+230}" cy="{my-250}" r="112" fill="#263241" opacity=".82"/>'
    for i in range(8):
        a = i * math.pi / 4
        m += (f'<circle cx="{mx+230+math.cos(a)*74:.0f}" cy="{my-250+math.sin(a)*74:.0f}"'
              f' r="13" fill="#15202c" opacity=".7"/>')
    bl = ((t * .28) % 1.0)
    m += (f'<g opacity=".8"><path d="M{mx+110+230*bl:.0f},{my-396} l76,0 l-120,292 l-76,0 z"'
          f' fill="#ffffff" opacity=".35"/></g>')
    m += (f'<path d="M{mx+120},{my-330} q70,-62 150,-48" fill="none" stroke="#ffffff"'
          f' stroke-width="13" opacity=".45"/>')
    # ТАБЛИЧКА-МАНДАРИН на дверце
    kach = 4 * A.w(t, 3.6)
    m += (f'<g transform="rotate({kach:.2f} {mx+398} {my-390})">'
          f'<path d="M{mx+398},{my-390} l-10,96" stroke="#b9452c" stroke-width="7"/>'
          + ob.mandarin(mx + 388, my - 258, .9, .0, t) + '</g>')
    # СУШИЛКА складывается
    sl = A.ease(A.seg(t, .8, 2.6))
    sx, sy = 880, POL
    ug = 17 - 13 * sl
    m += ten(sx + 60, sy + 8, 200, 22, .45)
    for sgn in (-1, 1):
        m += f'<g transform="rotate({sgn*ug:.1f} {sx+60} {sy-430})">'
        for rx0 in (sx - 56, sx + 176):
            m += (f'<rect x="{rx0}" y="{sy-430}" width="26" height="430" rx="10"'
                  f' fill="#aeb9c4" {o(6)}/>')
        for i in range(6):
            yy = sy - 400 + i * 66
            m += (f'<line x1="{sx-46}" y1="{yy}" x2="{sx+190}" y2="{yy}"'
                  f' stroke="#cdd8e0" stroke-width="11" stroke-linecap="round"/>')
        m += '</g>'
    # ПОЛОТЕНЦЕ на сушилке — единственное тёплое пятно кадра (правило гаммы)
    pk = 7 * A.w(t, 4.2, .2)
    m += (f'<g transform="rotate({pk:.2f} {sx+68} {sy-334})">'
          f'<path d="M{sx-34},{sy-346} h204 q10,8 0,18 h-204 q-10,-10 0,-18 z"'
          f' fill="{ob.ZOLOTO2}" {o(5)}/>'
          f'<path d="M{sx-28},{sy-330} h192 q14,122 -4,214 q-92,24 -184,0'
          f' q-18,-92 -4,-214 z" fill="{ob.ALYJ}" {o(6)}/>'
          f'<path d="M{sx-20},{sy-250} h176 M{sx-20},{sy-206} h176"'
          f' stroke="{ob.ZOLOTO}" stroke-width="9" opacity=".85"/>'
          f'<path d="M{sx-14},{sy-316} q88,22 172,0" fill="none" stroke="#f4b9a6"'
          f' stroke-width="7" opacity=".5"/></g>')
    m += baza.teplo(sx + 68, sy - 230, 330, 300, .40)
    # ВЕДРО с тряпкой
    vx, vy = 1480, POL
    m += ten(vx, vy + 8, 120, 22, .5)
    m += f'<path d="M{vx-108},{vy-250} h216 l-30,250 h-156 z" fill="url(#zhel)" {o(8)}/>'
    m += (f'<ellipse cx="{vx}" cy="{vy-250}" rx="108" ry="30" fill="#2c343c" {o(6)}/>'
          f'<ellipse cx="{vx}" cy="{vy-250}" rx="86" ry="21" fill="#18202a"/>')
    m += f'<path d="M{vx-78},{vy-200} l-16,186" stroke="#eef5fb" stroke-width="10" opacity=".3"/>'
    tr = 9 * A.w(t, 3.0, .3)
    m += (f'<g transform="rotate({tr:.2f} {vx+60} {vy-256})">'
          f'<path d="M{vx-50},{vy-278} q130,-44 200,-6 q10,70 -34,180'
          f' q-70,22 -128,-14 q-54,-78 -38,-160 z" fill="#d7e3ec" {o(6)}/>'
          f'<path d="M{vx-20},{vy-240} q80,30 150,8" fill="none" stroke="#9fb6c6" stroke-width="8"/></g>')
    s += SL(Z_SRED, m)

    f = baza.lampa(1778, 300, t, .66, True)
    f += baza._ramka_pp("levo", "#0b1118", .55)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.40))
    return s


def kuhnya_v_razgar_gotovki(t):
    """Кухня: все конфорки заняты, на столе миски, противень и скалка,
    хозяйка со спины пробует с ложки. Живое: крышки подпрыгивают, пар стоит
    столбом, ложка идёт ко рту. Рук нет — ложка едет сама."""
    POL = 930
    s = SL(Z_NEBO, b7_fon("b7f_f", "#2f3f55", "#1a2330"))

    d = b7_plitka(600, 120, 900, 480, 120, "b7f_pl", "#dfe9ef", "#b2c6d2")
    d += b7_oboi(30, POL - 30, "#45566d", 120, .14)
    d += baza.okno_izby(120, 180, 330, 300, t, None, .55, False, True)
    d += f'<rect x="620" y="150" width="560" height="22" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(5):
        d += baza.krynka(680 + i * 110, 146, .52)
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    m = b7_pol(POL, "b7f_p", "#8b6341", "#3e2614")
    # ПЛИТА с четырьмя занятыми конфорками
    px, py, pw = 560, POL, 700
    m += ten(px + pw / 2, py + 8, pw * .5, 26, .5)
    m += f'<rect x="{px}" y="{py-430}" width="{pw}" height="430" rx="16" fill="url(#chug)" {o(8)}/>'
    m += f'<rect x="{px+18}" y="{py-250}" width="{pw-36}" height="200" rx="12" fill="#1b1917" {o(5)}/>'
    m += (f'<rect x="{px+40}" y="{py-230}" width="{pw-80}" height="150" rx="10"'
          f' fill="{ORA}" opacity="{.28+.16*abs(A.w(t,1.4)):.2f}"/>')
    m += f'<rect x="{px-12}" y="{py-452}" width="{pw+24}" height="34" rx="10" fill="url(#zhel)" {o(6)}/>'
    for i in range(4):
        cx = px + 110 + (i % 2) * 300
        cy = py - 400 + (i // 2) * 86
        m += baza.ogon(cx, cy + 26, t, .36, i * .23, 3)
        # кастрюля, крышка подпрыгивает
        pod = max(0.0, A.w(t, .9 + i * .17, i * .3)) ** 2 * 22
        m += (f'<path d="M{cx-104},{cy-130} h208 l-18,128 h-172 z" fill="url(#zhel)" {o(7)}/>')
        m += (f'<path d="M{cx-118},{cy-134} h236" stroke="#3e444c" stroke-width="12" stroke-linecap="round"/>')
        m += (f'<g transform="translate(0,{-pod:.1f})">'
              f'<ellipse cx="{cx}" cy="{cy-142}" rx="112" ry="26" fill="#c2cad2" {o(6)}/>'
              f'<circle cx="{cx}" cy="{cy-162}" r="17" fill="#4e555d" {o(4)}/></g>')
        m += baza.par(cx, cy - 170, t, 4, .46, 240, .4 + i * .05, .9)
    s += SL(Z_SRED, m)

    # СТОЛ с мисками, противнем и скалкой
    f = ""
    sx, sy = -40, 700
    f += ten(260, POL - 4, 330, 26, .5)
    f += f'<rect x="{sx}" y="{sy}" width="560" height="38" rx="10" fill="url(#derev)" {o(8)}/>'
    f += f'<rect x="{sx+360}" y="{sy+38}" width="34" height="{POL-sy-38}" fill="url(#derev)" {o(6)}/>'
    for i, (bx, rx_) in enumerate(((110, 100), (320, 72))):
        f += (f'<path d="M{bx-rx_},{sy-16} q{rx_*.1:.0f},{rx_*1.25:.0f} {rx_:.0f},{rx_*1.3:.0f}'
              f' q{rx_*.9:.0f},{-rx_*.05:.0f} {rx_:.0f},{-rx_*1.3:.0f} z"'
              f' fill="url(#glina)" {o(7)}/>')
        f += (f'<ellipse cx="{bx}" cy="{sy-16}" rx="{rx_}" ry="{rx_*.34:.0f}"'
              f' fill="#efe3c8" {o(6)}/>')
        f += (f'<ellipse cx="{bx}" cy="{sy-16}" rx="{rx_*.76:.0f}" ry="{rx_*.24:.0f}"'
              f' fill="#d9c8a4"/>')
    f += (f'<rect x="{sx+400}" y="{sy-24}" width="170" height="30" rx="8" fill="url(#zhel)" {o(6)}/>')
    f += (f'<rect x="{sx+120}" y="{sy-54}" width="300" height="22" rx="11" fill="url(#derev)" {o(5)}/>'
          f'<circle cx="{sx+112}" cy="{sy-43}" r="18" fill="url(#derev)" {o(4)}/>'
          f'<circle cx="{sx+428}" cy="{sy-43}" r="18" fill="url(#derev)" {o(4)}/>')
    # ХОЗЯЙКА со спины + ЛОЖКА идёт ко рту
    hx, hb = 1480, POL + 150
    # тёплая подложка за спиной: без неё тёмная фигура сливалась с плитой
    f += baza.teplo(hx, hb - 420, 330, 450, .40)
    f += ob.figura(hx, hb, 640, t, "#241d2b", "#ffd089", True, ph=.3)
    f += (f'<path d="M{hx-116},{hb-470} q110,-34 220,6 l-6,170 q-110,30 -212,-4 z"'
          f' fill="url(#krem)" opacity=".85" {o(5)}/>')
    lo = A.ease(A.seg(t, .5, 1.6))
    lx = hx - 430 + 150 * lo
    ly = hb - 300 - 150 * lo
    f += (f'<g transform="translate({lx:.0f},{ly:.0f}) rotate({-28+22*lo:.1f})">'
          f'<rect x="-13" y="0" width="26" height="230" rx="13" fill="url(#zhel)" {o(6)}/>'
          f'<ellipse cx="0" cy="-22" rx="62" ry="44" fill="url(#zhel)" {o(7)}/>'
          f'<ellipse cx="0" cy="-26" rx="46" ry="30" fill="#f2f7fb" opacity=".8"/>'
          f'<ellipse cx="-14" cy="-34" rx="20" ry="12" fill="#ffffff" opacity=".7"/></g>')
    f += baza.par(lx, ly - 46, t, 3, .4, 130, .5, .6)
    f += baza._ramka_pp("levo", "#090d14", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


def nozhnicy_nad_pryadyu(t):
    """Крупно затылок под накинутой простынёй, ножницы зависли над прядью и
    опускаются, не щёлкнув. Живое: ножницы висят и уходят вниз, прядь
    качается, простыня на плечах подрагивает. Лица нет — только затылок."""
    s = SL(Z_NEBO, b7_fon("b7g_f", "#303b52", "#171d2a"))

    d = b7_oboi(-40, 1100, "#44506b", 132, .16)
    d += baza.teplo(1600, 240, 560, 480, .46)
    # ЗЕРКАЛО в раме, а не голый прямоугольник
    d += (f'<rect x="1472" y="152" width="356" height="476" rx="24" fill="url(#med)" {o(8)}/>'
          f'<rect x="1500" y="180" width="300" height="420" rx="14" fill="url(#stekl)"'
          f' opacity=".55" {o(6)}/>'
          f'<path d="M1530,560 l210,-330" stroke="#ffffff" stroke-width="30" opacity=".16"/>'
          f'<path d="M1588,578 l180,-300" stroke="#ffffff" stroke-width="14" opacity=".12"/>')
    d += (f'<rect x="1452" y="628" width="396" height="24" rx="8" fill="url(#derev)" {o(6)}/>'
          f'<path d="M1500,652 l18,30 M1800,652 l-18,30" {o(5)} fill="none"/>')
    # на полочке под зеркалом — гребень и две заколки, ножницы «из дома»
    d += (f'<path d="M1520,628 h150 v-26 h-150 z" fill="url(#zhel)" {o(5)}/>')
    for i in range(9):
        d += (f'<line x1="{1528+i*17}" y1="628" x2="{1528+i*17}" y2="650"'
              f' stroke="#4b5159" stroke-width="6" stroke-linecap="round"/>')
    for i in range(2):
        d += (f'<ellipse cx="{1720+i*54}" cy="618" rx="24" ry="9" fill="{ob.ZOLOTO}" {o(4)}/>')
    d += f'<rect x="120" y="190" width="320" height="24" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(4):
        d += baza.krynka(180 + i * 86, 186, .4, "url(#krem)")
    s += SL(Z_DAL, d)

    # ЗАТЫЛОК и ПРОСТЫНЯ
    drozh = 4 * A.w(t, 2.3, .2)
    m = ten(760, 1050, 520, 44, .5)
    m += (f'<g transform="translate(0,{drozh:.1f})">'
          f'<path d="M210,1120 q20,-224 150,-286 q120,-58 380,-58 q260,0 380,58'
          f' q130,62 150,286 z" fill="url(#list)" {o(8)}/>')
    m += ('<path d="M300,1100 q40,-212 170,-272" fill="none" stroke="#ffffff"'
          ' stroke-width="18" opacity=".30"/>')
    m += (f'<path d="M360,834 q380,-96 760,0" fill="none" stroke="{TKAN2}"'
          f' stroke-width="14" opacity=".55"/>')
    m += (f'<path d="M560,790 q180,-44 360,0 q-30,54 -180,54 q-150,0 -180,-54 z"'
          f' fill="#dfe6ef" {o(6)}/>'
          f'<circle cx="740" cy="828" r="22" fill="url(#zol)" {o(4)}/></g>')
    # голова со спины
    m += (f'<g transform="translate(0,{drozh*.5:.1f})">'
          f'<circle cx="740" cy="520" r="266" fill="#2a2029" {o(9)}/>')
    r = random.Random(7)
    for i in range(16):
        a = -2.5 + i * .19
        x0 = 740 + math.cos(a) * 250
        y0 = 520 + math.sin(a) * 250
        m += (f'<path d="M{x0:.0f},{y0:.0f} q{r.uniform(-40,40):.0f},120'
              f' {r.uniform(-26,26):.0f},230" fill="none" stroke="#3a2d36"'
              f' stroke-width="18" stroke-linecap="round"/>')
    m += ('<path d="M600,330 q140,-70 280,10" fill="none" stroke="#5a4650"'
          ' stroke-width="22" opacity=".65"/>')
    m += (f'<path d="M520,620 q-30,180 20,330" fill="none" stroke="#2a2029"'
          f' stroke-width="56" stroke-linecap="round"/></g>')
    # ПРЯДЬ качается
    pr = 20 * A.w(t, 2.0, .1)
    m += (f'<path d="M966,380 q{104+pr:.1f},180 {56+pr*1.7:.1f},392" fill="none"'
          f' stroke="#4a3a44" stroke-width="62" stroke-linecap="round"/>')
    m += (f'<path d="M974,402 q{92+pr:.1f},168 {50+pr*1.6:.1f},356" fill="none"'
          f' stroke="#7d6672" stroke-width="18" stroke-linecap="round" opacity=".8"/>')
    m += (f'<path d="M1010,430 q{86+pr:.1f},158 {44+pr*1.5:.1f},330" fill="none"'
          f' stroke="#5b4953" stroke-width="22" stroke-linecap="round" opacity=".9"/>')
    s += SL(Z_SRED, m)

    # НОЖНИЦЫ: зависли и опустились, не щёлкнув
    vis = A.ease(A.seg(t, .4, 1.5))
    niz = A.out(A.seg(t, 2.6, 2.0))
    ny = 230 + 130 * vis + 210 * niz + 14 * A.w(t, 2.4)
    f = baza.teplo(1046, ny + 120, 300, 260, .40)
    f += b7_nozhnicy(1046, ny, t, 1.34, 10 + 5 * A.w(t, 3.2) - 12 * niz, 1.0 - .15 * niz)
    f += baza._ramka_pp("levo", "#080c13", .6)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.46))
    return s


def mama_v_bigudi(t):
    """Мостик в память: вечер у трюмо, мама со спины докручивает последние
    бигуди и повязывает косынку, в зеркале дочка повторяет на кукле. Живое:
    бигуди появляются одна за другой, косынка опускается, прядь куклы
    наматывается."""
    POL = 960
    s = SL(Z_NEBO, b7_fon("b7h_f", "#4a4463", "#262337"))

    d = b7_oboi(-20, POL + 20, "#5b5579", 112, .20)
    r = random.Random(12)
    for i in range(26):
        cx, cy = r.uniform(-60, W + 60), r.uniform(0, POL - 60)
        d += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="{ob.ALYJ}" opacity=".22"/>'
              f'<circle cx="{cx+22:.0f}" cy="{cy+16:.0f}" r="7" fill="{ob.ZOLOTO}" opacity=".18"/>')
    d += baza.zanaveska(1880, -20, 980, 260, TKAN, t, -1)
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    # ТРЮМО с зеркалом
    m = b7_pol(POL, "b7h_p", "#86603e", "#3b2414")
    tx, ty = 170, 770
    m += ten(tx + 330, POL - 4, 340, 26, .5)
    m += f'<rect x="{tx}" y="{ty}" width="660" height="34" rx="10" fill="url(#derev)" {o(8)}/>'
    m += (f'<rect x="{tx+30}" y="{ty+34}" width="250" height="{POL-ty-34}" rx="8"'
          f' fill="url(#derev)" {o(6)}/>')
    for i in range(2):
        m += (f'<rect x="{tx+52}" y="{ty+66+i*76}" width="206" height="56" rx="8"'
              f' fill="#6d492a" {o(5)}/>'
              f'<circle cx="{tx+155}" cy="{ty+94+i*76}" r="12" fill="url(#zol)" {o(3)}/>')
    m += (f'<rect x="{tx+420}" y="{ty+34}" width="200" height="{POL-ty-34}" rx="8"'
          f' fill="url(#derev)" {o(6)}/>')
    # зеркало
    mx, my, mrx, mry = tx + 330, 430, 265, 320
    m += (f'<ellipse cx="{mx}" cy="{my}" rx="{mrx+28}" ry="{mry+28}" fill="url(#med)" {o(8)}/>')
    m += (f'<ellipse cx="{mx}" cy="{my}" rx="{mrx}" ry="{mry}" fill="#243049" {o(5)}/>')
    m += (f'<clipPath id="b7h_zerk"><ellipse cx="{mx}" cy="{my}" rx="{mrx}" ry="{mry}"/></clipPath>'
          f'<g clip-path="url(#b7h_zerk)">')
    m += (f'<rect x="{mx-mrx}" y="{my-mry}" width="{mrx*2}" height="{mry*2}" fill="#3b4663"/>')
    m += baza.teplo(mx - 60, my + 60, 300, 280, .5)
    # отражение: дочка с куклой
    m += ob.figura(mx - 92, my + 320, 380, t, "#2b2436", "#ffd79a", False, ph=.4, profil=True)
    kx, ky = mx + 96, my + 150
    m += (f'<ellipse cx="{kx}" cy="{ky}" rx="56" ry="74" fill="{KREM}" {o(5)}/>'
          f'<circle cx="{kx}" cy="{ky-96}" r="60" fill="{KREM}" {o(5)}/>')
    vit = (t * 150) % 360
    m += (f'<g transform="rotate({vit:.0f} {kx+34} {ky-96})">'
          f'<path d="M{kx+34},{ky-96} q46,-24 52,26 q-40,36 -62,-6" fill="none"'
          f' stroke="{MED}" stroke-width="14" stroke-linecap="round"/></g>')
    m += (f'<path d="M{kx-46},{ky-110} q46,-44 92,0" fill="none" stroke="{MED}"'
          f' stroke-width="16"/>')
    m += '</g>'
    m += (f'<path d="M{mx-mrx*.7:.0f},{my-mry*.6:.0f} l{mrx*.8:.0f},{mry*1.1:.0f}"'
          f' stroke="#ffffff" stroke-width="26" opacity=".14"/>')
    # лампа трюмо — тёплое пятно
    m += baza.lampa(tx + 616, 700, t, .72, True)
    for i in range(3):
        m += baza.krynka(tx + 470 + i * 56, ty - 6, .34, "url(#stekl)")
    s += SL(Z_SRED, m)

    # МАМА со спины: бигуди и косынка
    f = baza.teplo(1420, 540, 420, 520, .40)
    hx, hb = 1420, POL + 130
    f += (f'<ellipse cx="{hx}" cy="{hb-300}" rx="330" ry="470" fill="#1c1828"'
          f' opacity=".52"/>')          # тёмная подложка разводит фигуру и обои
    f += ob.figura(hx, hb, 690, t, "#2a2338", "#ffd79a", False, ph=.15)
    gy = hb - 690 * .80
    for i in range(8):
        p = A.out(A.seg(t, .3 + i * .22, .6))
        if p <= 0:
            continue
        ryad = i // 4
        a = -2.35 + (i % 4) * .62
        rr = 96 - ryad * 44
        bx = hx + math.cos(a) * rr
        by = gy + math.sin(a) * rr + ryad * 26
        f += (f'<g transform="translate({bx:.0f},{by:.0f}) rotate({a*57.3+90:.0f}) scale({p:.2f})">'
              f'<rect x="-44" y="-26" width="88" height="52" rx="24" fill="{ob.ALYJ}" {o(6)}/>'
              f'<path d="M-30,-26 v52 M0,-26 v52 M30,-26 v52" stroke="#8d1b1c" stroke-width="6"/>'
              f'<ellipse cx="-14" cy="-12" rx="16" ry="7" fill="#f4a89c" opacity=".7"/></g>')
    kos = A.out(A.seg(t, 3.9, 1.9))
    if kos > 0:
        ky2 = gy - 320 + 320 * kos
        f += (f'<g transform="translate({hx:.0f},{ky2:.0f})" opacity="{min(1,kos*1.6):.2f}">'
              f'<path d="M-120,-10 q120,-128 240,0 q10,140 -120,196 q-130,-56 -120,-196 z"'
              f' fill="{ob.ZOLOTO}" {o(6)}/>')
        for i in range(7):
            f += (f'<circle cx="{-92+i*30}" cy="{30+((i*37)%52)}" r="9" fill="{ob.ALYJ}"'
                  f' opacity=".6"/>')
        f += (f'<path d="M-24,182 q{26*kos:.0f},34 {62*kos:.0f},10" fill="none"'
              f' stroke="{ob.ZOLOTO}" stroke-width="18" stroke-linecap="round"/></g>')
    f += baza._ramka_pp("levo", "#0a0a12", .52)
    s += SL(Z_PERED, f)

    fix = f'<rect width="{W}" height="{H}" fill="#c08a4a" opacity=".12"/>' + baza._vinetka(.44)
    s += SL(Z_FIX, fix)
    return s


def parikmaherskaya_pered_prazdnikom(t):
    """Зал в полосе 0-830: три занятых кресла, дамы под колпаками-сушуарами с
    журналами, у двери очередь, на зеркале мишура. Живое: ножницы мастера
    мелькают, колпаки гудят светом, очередь листает журналы."""
    POL = 900
    s = SL(Z_NEBO, b7_fon("b7i_f", "#45506a", "#232a3a"))

    d = b7_oboi(20, POL - 20, "#525f7c", 110, .16)
    # зеркальная стена
    for i in range(3):
        zx = 40 + i * 268
        d += (f'<rect x="{zx}" y="110" width="226" height="286" rx="12" fill="url(#med)" {o(6)}/>'
              f'<rect x="{zx+16}" y="126" width="194" height="254" rx="8" fill="#5a6c88"'
              f' opacity=".9" {o(4)}/>'
              f'<path d="M{zx+36},{352} l120,-196" stroke="#ffffff" stroke-width="20" opacity=".17"/>')
    # мишура по верху зеркал
    for i in range(16):
        gx = 50 + i * 50
        gy = 98 + 16 * math.sin(i * .9)
        bl = .35 + .65 * abs(A.w(t, 1.4 + (i % 4) * .3, i * .13))
        d += (f'<circle cx="{gx}" cy="{gy:.0f}" r="17" fill="{[ob.ZOLOTO, ob.ALYJ][i%2]}"'
              f' opacity="{bl:.2f}"/>')
        d += (f'<circle cx="{gx}" cy="{gy:.0f}" r="30" fill="{ob.ZOLOTO}"'
              f' opacity="{bl*.2:.2f}"/>')
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    m = b7_pol(POL, "b7i_p", "#7e7367", "#3b352d")
    # ТРИ КРЕСЛА с колпаками-сушуарами
    for i, (cx, sc, ph) in enumerate(((150, 1.0, 0.0), (420, .88, .3), (660, .76, .6))):
        base = POL - 30 + 30 * (1 - sc)
        m += f'<g transform="translate({cx},{base}) scale({sc:.2f})">'
        m += ten(0, 10, 130, 22, .5)
        m += f'<rect x="-26" y="-180" width="52" height="180" rx="12" fill="#4b525b" {o(6)}/>'
        m += f'<ellipse cx="0" cy="0" rx="124" ry="26" fill="#3d444c" {o(5)}/>'
        m += f'<rect x="-116" y="-300" width="232" height="130" rx="22" fill="{TKAN}" {o(7)}/>'
        m += f'<rect x="-104" y="-560" width="208" height="270" rx="26" fill="{TKAN}" {o(7)}/>'
        m += (f'<path d="M-86,-540 q86,-30 172,0" fill="none" stroke="#e0756c"'
              f' stroke-width="12" opacity=".5"/>')
        # дама силуэтом со спины
        m += (f'<path d="M-82,-300 q-6,-180 82,-214 q88,34 82,214 z" fill="#4c4059"'
              f' stroke="#f0c070" stroke-width="4" stroke-opacity=".6"/>')
        m += (f'<circle cx="0" cy="-566" r="82" fill="#5e5073" stroke="#ffd79a"'
              f' stroke-width="5" stroke-opacity=".75"/>')
        # колпак-сушуар накрывает голову
        gor = .45 + .55 * abs(A.w(t, 1.7 + i * .4, i * .2))
        m += baza.teplo(0, -570, 210, 160, gor * .8)
        m += (f'<path d="M-98,-648 q98,-182 196,0 q-22,36 -98,36 q-76,0 -98,-36 z"'
              f' fill="#cfd8e2" {o(7)}/>')
        m += (f'<path d="M-80,-656 q80,-146 160,0 q-18,26 -80,26 q-62,0 -80,-26 z"'
              f' fill="{SVET}" opacity="{gor*.6:.2f}"/>')
        m += (f'<path d="M-70,-682 q70,-104 140,0" fill="none" stroke="#ffffff"'
              f' stroke-width="10" opacity="{gor*.5:.2f}"/>')
        m += f'<rect x="-15" y="-900" width="30" height="258" rx="10" fill="#8f98a3" {o(5)}/>'
        # журнал в руках не рисуем — журнал сам лежит на коленях и листается
        lst = ((t * .8 + i * .33) % 1.0)
        m += (f'<g transform="translate(60,-300)">'
              f'<rect x="-70" y="-30" width="140" height="100" rx="8" fill="url(#list)" {o(5)}/>'
              f'<g transform="translate(0,-30) scale({max(.05,1-2*abs(lst-.5)):.2f},1)">'
              f'<rect x="-66" y="0" width="132" height="96" rx="8" fill="#efe9d8" {o(4)}/></g></g>')
        m += '</g>'
    # НОЖНИЦЫ мастера мелькают у первого кресла
    mel = .55 + .45 * abs(A.w(t, .55))
    m += (f'<g opacity="{mel:.2f}">'
          + b7_nozhnicy(310, 330 + 26 * A.w(t, 1.1), t, .72, -48 + 30 * A.w(t, .55), .8)
          + '</g>')
    s += SL(Z_SRED, m)

    # ОЧЕРЕДЬ у двери — передний план
    f = ""
    for i, (qx, sc) in enumerate(((640, 1.0), (776, .94))):
        qb = POL + 110 - 20 * i
        f += f'<g transform="translate({qx},{qb}) scale({sc:.2f})">'
        f += ten(0, 8, 96, 18, .45)
        f += f'<rect x="-84" y="-40" width="168" height="34" rx="10" fill="url(#derev)" {o(6)}/>'
        f += (f'<rect x="-74" y="-6" width="22" height="90" fill="url(#derev)" {o(4)}/>'
              f'<rect x="52" y="-6" width="22" height="90" fill="url(#derev)" {o(4)}/>')
        f += (f'<path d="M-78,-44 q-8,-220 78,-252 q86,32 78,252 z" fill="#3a3148"'
              f' stroke="#e8b06a" stroke-width="4" stroke-opacity=".55"/>')
        f += (f'<circle cx="0" cy="-330" r="74" fill="#3a3148" stroke="#e8b06a"'
              f' stroke-width="4" stroke-opacity=".55"/>')
        lst = ((t * .7 + i * .5) % 1.0)
        f += (f'<g transform="translate(0,-170)">'
              f'<rect x="-82" y="-40" width="164" height="118" rx="8" fill="url(#list)" {o(5)}/>'
              f'<g transform="translate(0,-40) scale({max(.05,1-2*abs(lst-.5)):.2f},1)">'
              f'<rect x="-78" y="0" width="156" height="114" rx="8" fill="#f2ecdb" {o(4)}/></g></g>')
        f += '</g>'
    f += baza._ramka_pp("levo", "#090c14", .55)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.36))
    return s


def vnuk_s_dlinnoy_chelkoy(t):
    """Мальчик на стуле сдувает чёлку, бабушка убирает ножницы в карман
    фартука и закалывает чёлку заколкой. Живое: чёлка взлетает от выдоха,
    ножницы уходят в карман, заколка защёлкивается. Лиц нет — профиль."""
    POL = 940
    s = SL(Z_NEBO, b7_fon("b7j_f", "#3a4259", "#1f2531"))

    d = b7_oboi(10, POL - 10, "#4a556f", 122, .16)
    # КОВЁР НА СТЕНЕ: кайма, медальон и бахрома — было голое красное поле
    d += (f'<rect x="1100" y="150" width="620" height="420" rx="8" fill="{TKAN}" {o(7)}/>')
    d += (f'<rect x="1132" y="182" width="556" height="356" rx="4" fill="none"'
          f' stroke="{ob.ZOLOTO}" stroke-width="9" opacity=".8"/>')
    d += (f'<rect x="1160" y="210" width="500" height="300" rx="4" fill="#8d1b1c"'
          f' opacity=".55"/>')
    d += (f'<ellipse cx="1410" cy="360" rx="150" ry="112" fill="none"'
          f' stroke="{ob.ZOLOTO}" stroke-width="11" opacity=".85"/>')
    d += (f'<ellipse cx="1410" cy="360" rx="86" ry="62" fill="{ob.ZOLOTO2}" opacity=".5"/>')
    for i in range(4):
        a_ = i * math.pi / 2 + math.pi / 4
        d += (f'<path d="M{1410+math.cos(a_)*150:.0f},{360+math.sin(a_)*112:.0f}'
              f' l{math.cos(a_)*52:.0f},{math.sin(a_)*40:.0f}" stroke="{ob.ZOLOTO}"'
              f' stroke-width="8" opacity=".7" stroke-linecap="round"/>')
    for i in range(22):
        d += (f'<path d="M{1106+i*28},570 v26" stroke="{RUSH}" stroke-width="6"'
              f' opacity=".8" stroke-linecap="round"/>')
    d += baza.okno_izby(170, 170, 330, 290, t, None, .4, True, True)
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    # СТУЛ и МАЛЬЧИК в профиль
    m = b7_pol(POL, "b7j_p", "#8a6340", "#3d2616")
    sx, sb = 700, POL + 20
    m += ten(sx, sb, 140, 24, .5)
    m += f'<rect x="{sx-100}" y="{sb-270}" width="200" height="32" rx="10" fill="url(#derev)" {o(7)}/>'
    m += (f'<rect x="{sx-92}" y="{sb-240}" width="24" height="240" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{sx+68}" y="{sb-240}" width="24" height="240" fill="url(#derev)" {o(5)}/>')
    m += (f'<rect x="{sx+72}" y="{sb-620}" width="26" height="370" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="{sx-20}" y="{sb-636}" width="120" height="26" rx="10" fill="url(#derev)" {o(5)}/>')
    # тело и голова в профиль
    m += (f'<path d="M{sx-96},{sb-272} q-10,-200 96,-228 q104,28 94,228 z"'
          f' fill="#2b2434" stroke="#f0c070" stroke-width="4" stroke-opacity=".7"/>')
    hy = sb - 580
    m += (f'<circle cx="{sx+16}" cy="{hy}" r="92" fill="#2b2434" stroke="#f0c070"'
          f' stroke-width="4" stroke-opacity=".7"/>')
    m += (f'<path d="M{sx-66},{hy-24} q70,-96 164,-30" fill="none" stroke="#3b3042"'
          f' stroke-width="34" stroke-linecap="round"/>')
    # ЧЁЛКА: мальчик её сдувает
    sdv = max(0.0, A.w(t, 1.5)) ** 3
    for i in range(6):
        cx0 = sx + 22 + i * 17       # чёлка только надо лбом, череп не закрыт
        m += (f'<path d="M{cx0},{hy-84} q{30+66*sdv:.0f},{104-56*sdv:.0f}'
              f' {16+96*sdv:.0f},{192-92*sdv:.0f}" fill="none" stroke="#453750"'
              f' stroke-width="19" stroke-linecap="round"/>')
        m += (f'<path d="M{cx0+8},{hy-78} q{28+62*sdv:.0f},{96-52*sdv:.0f}'
              f' {14+90*sdv:.0f},{178-86*sdv:.0f}" fill="none" stroke="#7a6684"'
              f' stroke-width="7" stroke-linecap="round" opacity=".55"/>')
    for i in range(3):
        k = ((t * 1.1 + i * .33) % 1.0)
        m += (f'<ellipse cx="{sx+112+70*k:.0f}" cy="{hy+28-22*k:.0f}" rx="{10+30*k:.0f}"'
              f' ry="{(10+30*k)*.5:.0f}" fill="#dbe7f2" opacity="{.3*(1-k)*sdv:.2f}"/>')
    # ЗАКОЛКА защёлкивается
    zp = A.over(A.seg(t, 2.5, 1.0))
    if zp > .02:
        m += (f'<g transform="translate({sx-18},{hy-84}) rotate({-18+10*zp:.1f}) scale({zp:.2f})">'
              f'<rect x="-52" y="-13" width="104" height="26" rx="13" fill="url(#zol)" {o(5)}/>'
              f'<path d="M-40,0 h80" stroke="#8a6414" stroke-width="7"/>'
              f'<circle cx="46" cy="0" r="12" fill="#fff3c4" opacity=".8"/></g>')
    s += SL(Z_SRED, m)

    # БАБУШКА с фартуком, ножницы уходят в карман
    f = ""
    bx, bb = 1500, POL + 170
    f += ob.figura(bx, bb, 700, t, "#2a2231", "#f2c477", True, ph=.4)
    f += (f'<path d="M{bx-130},{bb-500} q130,-40 258,6 l-10,266 q-124,34 -240,-6 z"'
          f' fill="url(#krem)" opacity=".9" {o(6)}/>')
    f += (f'<rect x="{bx-74}" y="{bb-370}" width="152" height="112" rx="12"'
          f' fill="#ded0b2" {o(6)}/>')
    f += (f'<path d="M{bx-66},{bb-342} h136" stroke="#b8a681" stroke-width="5"'
          f' opacity=".9" stroke-dasharray="12 9"/>')
    kar = A.ease(A.seg(t, 1.0, 1.5))
    nx = bx - 240 + 244 * kar
    ny = bb - 560 + 142 * kar
    f += (f'<g opacity="{1-.15*kar:.2f}">'
          + b7_nozhnicy(nx, ny, t, .62 - .1 * kar, -24 + 30 * kar, .5) + '</g>')
    f += (f'<rect x="{bx-74}" y="{bb-370}" width="152" height="60" rx="12"'
          f' fill="#cfbf9c" {o(5)}/>')
    f += baza._ramka_pp("levo", "#090c13", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


def sleza_nad_prazdnichnoy_tarelkoy(t):
    """Крупно пустая праздничная тарелка, на её край падает одна слеза, рядом
    хлеб, разломленный пополам. Живое: слеза падает и расходится кругом,
    огонёк свечи вздрагивает, половинки хлеба расходятся. Без лиц."""
    s = SL(Z_NEBO, b7_fon("b7k_f", "#2b3146", "#14161f"))

    d = f'<rect x="-440" y="-340" width="{W+880}" height="620" fill="#10131c" opacity=".7"/>'
    d += baza.teplo(1560, 340, 540, 430, .42)
    rg = random.Random(31)
    d += (f'<path d="M1300,470 q190,-130 420,-90 q-150,70 -420,90 z" fill="{ob.HVOYA2}"'
          f' opacity=".85" {o(5)}/>')
    for i in range(14):
        gx = 1310 + rg.uniform(0, 420)
        gy = 300 + rg.uniform(0, 170)
        gor = .3 + .7 * abs(A.w(t, 1.6 + rg.uniform(0, 1.4), i * .17))
        d += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="13" fill="{[SVET, ob.ALYJ, ob.ZOLOTO][i%3]}"'
              f' opacity="{gor:.2f}"/>')
        d += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="30" fill="{SVET}"'
              f' opacity="{gor*.16:.2f}"/>')
    d += (f'<path d="M-440,470 q560,-46 1160,-10 q520,30 1200,-16 L{W+440},620 L-440,620 z"'
          f' fill="url(#rush)" {o(7)}/>')
    d += (f'<path d="M-440,540 q600,40 1200,6 q500,-30 1160,8" fill="none"'
          f' stroke="{ob.ALYJ}" stroke-width="9" opacity=".6"/>')
    d += b7_svecha_stola(1700, 300, t, 1.5, .2)
    s += SL(Z_DAL, d)

    m = (f'<rect x="-440" y="560" width="{W+880}" height="{H+340}" fill="url(#rush)"/>')
    for i in range(5):
        m += (f'<path d="M-440,{640+i*120} q620,34 1240,0 q480,-26 1120,14" fill="none"'
              f' stroke="#d9c79f" stroke-width="5" opacity=".5"/>')
    # ТАРЕЛКА крупно
    px, py = 720, 790
    m += ten(px, py + 130, 460, 54, .55)
    m += f'<ellipse cx="{px}" cy="{py}" rx="470" ry="186" fill="url(#krem)" {o(9)}/>'
    m += f'<ellipse cx="{px}" cy="{py+12}" rx="470" ry="186" fill="#c8b894" opacity=".45"/>'
    m += f'<ellipse cx="{px}" cy="{py-10}" rx="468" ry="184" fill="url(#krem)" {o(8)}/>'
    m += (f'<ellipse cx="{px}" cy="{py-10}" rx="368" ry="140" fill="none"'
          f' stroke="url(#zol)" stroke-width="12"/>')
    m += (f'<ellipse cx="{px}" cy="{py-10}" rx="250" ry="92" fill="#efe6cd" {o(5)}/>')
    m += (f'<path d="M{px-370},{py-60} q130,-78 300,-72" fill="none" stroke="#ffffff"'
          f' stroke-width="22" opacity=".45"/>')
    # ХЛЕБ разломлен пополам — половинки расходятся
    razh = 34 * A.ease(A.seg(t, .25, 1.6))
    for sgn in (-1, 1):
        hx = 1480 + sgn * (70 + razh)
        m += ten(hx, 965, 130, 24, .45)
        m += (f'<g transform="translate({hx:.0f},880) rotate({sgn*5:.0f})">'
              f'<path d="M{-sgn*6},78 q-110,-10 -118,-86 q-6,-80 110,-92 l{sgn*14},0'
              f' q10,94 0,178 z" fill="url(#med)" {o(7)}/>'
              f'<path d="M{-sgn*10},-96 q-80,10 -96,76" fill="none" stroke="#f0cf90"'
              f' stroke-width="12" opacity=".6"/>'
              f'<path d="M{-sgn*2},-98 q{sgn*16},92 0,178" fill="none" stroke="{KREM}"'
              f' stroke-width="16"/>'
              # мякиш на изломе: половинки читались двумя бурыми пятнами
              f'<path d="M{-sgn*12},-86 q{sgn*26},88 {-sgn*2},164'
              f' q{-sgn*30},-80 {sgn*14},-164 z" fill="#f3e6c6" {o(4)}/>'
              f'<circle cx="{-sgn*6}" cy="-20" r="9" fill="#e2cfa4" opacity=".9"/>'
              f'<circle cx="{-sgn*2}" cy="46" r="7" fill="#e2cfa4" opacity=".9"/>'
              f'<path d="M{-sgn*64},-74 q-18,74 6,142" fill="none" stroke="#8d6230"'
              f' stroke-width="7" opacity=".6"/></g>')
    s += SL(Z_SRED, m)

    # СЛЕЗА падает на край тарелки
    k = ((t + .2) % 1.9) / 1.9
    f = ""
    if k < .62:
        u = k / .62
        ty = -110 + (py - 150 + 110) * (u * u)   # падает из-за верхнего края
        f += (f'<g transform="translate(400,{ty:.0f})">'
              f'{baza.teplo(0, 50, 110, 110, .3)}'
              f'<path d="M0,-78 q56,66 56,116 q0,56 -56,56 q-56,0 -56,-56 q0,-50 56,-116 z"'
              f' fill="#cfe6f6" opacity=".92" {o(5)}/>'
              f'<ellipse cx="-18" cy="76" rx="15" ry="24" fill="#ffffff" opacity=".85"/></g>')
    else:
        u = (k - .62) / .38
        f += (f'<ellipse cx="400" cy="{py-84}" rx="{50+190*u:.0f}" ry="{16+58*u:.0f}"'
              f' fill="none" stroke="#dcefff" stroke-width="{14*(1-u):.1f}"'
              f' opacity="{(1-u)*.9:.2f}"/>')
        f += (f'<ellipse cx="400" cy="{py-84}" rx="{18+70*u:.0f}" ry="{6+22*u:.0f}"'
              f' fill="#dcefff" opacity="{(1-u)*.35:.2f}"/>')
    f += baza._ramka_pp("levo", "#070910", .5)
    s += SL(Z_LETIT, f)
    s += SL(Z_FIX, baza._vinetka(.50))
    return s


def ssora_tyanetsya_cherez_god(t):
    """От тарелки со слезой ползёт серая дорожка: за ней ковыляют градусник с
    грелкой и унылая тучка, а трещина от разломленного хлеба бежит через
    двенадцать плиток-месяцев. Живое: дорожка ползёт, предметы ковыляют,
    трещина бежит."""
    s = SL(Z_NEBO, b7_fon("b7l_f", "#333d54", "#171c27"))

    # ДВЕНАДЦАТЬ ПЛИТОК-МЕСЯЦЕВ
    d = ""
    rk = random.Random(19)
    for i in range(12):
        px = 44 + i * 153
        nak = rk.uniform(-3.4, 3.4)
        d += ten(px + 66, 848, 78, 17, .45)
        d += f'<g transform="rotate({nak:.1f} {px+66} 760)">'
        # ЛИСТОК ОТРЫВНОГО КАЛЕНДАРЯ: шапка месяца, дырки под скрепку, отгиб
        d += (f'<rect x="{px}" y="650" width="134" height="190" rx="10"'
              f' fill="url(#krem)" {o(6)}/>')
        d += (f'<rect x="{px}" y="650" width="134" height="46" rx="10"'
              f' fill="{ob.ALYJ if i in (0, 11) else MED}" {o(5)}/>')
        d += (f'<path d="M{px},692 h134" stroke="{K}" stroke-width="4" opacity=".55"/>')
        for hx_ in (px + 34, px + 100):
            d += (f'<circle cx="{hx_}" cy="672" r="8" fill="#6b5a3c" opacity=".85"/>')
        # крупная цифра месяца — блок, а не пустое поле
        d += (f'<rect x="{px+30}" y="712" width="74" height="60" rx="8"'
              f' fill="{"#d8c7a0" if i not in (0, 11) else "#eac9b4"}" {o(4)}/>')
        for r_ in range(2):
            d += (f'<path d="M{px+24},{794+r_*24} h86" stroke="#c6b794"'
                  f' stroke-width="7" opacity=".8" stroke-linecap="round"/>')
        # отогнутый уголок — лист, а не плитка
        d += (f'<path d="M{px+134},840 l-34,0 l34,-34 z" fill="#cbb995" {o(4)}/>')
        d += '</g>'
    # тусклая гирлянда под потолком: верх кадра был пустым полем
    d += ob.girlyanda(-60, 170, 1180, 130, t, 11, 110)
    d += f'<rect x="-440" y="0" width="{W+880}" height="420" fill="#1b2230" opacity=".45"/>'
    d += baza.teplo(140, 330, 420, 360, .34)
    s += SL(Z_DAL, d)

    # ТАРЕЛКА СО СЛЕЗОЙ и СЕРАЯ ДОРОЖКА
    m = ""
    m += ten(210, 520, 190, 28, .5)
    m += f'<ellipse cx="200" cy="470" rx="196" ry="74" fill="url(#krem)" {o(7)}/>'
    m += (f'<ellipse cx="200" cy="462" rx="146" ry="54" fill="none" stroke="url(#zol)"'
          f' stroke-width="9"/>')
    kap = ((t * .7) % 1.0)
    m += (f'<ellipse cx="268" cy="{400+70*kap:.0f}" rx="13" ry="19" fill="#cfe6f6"'
          f' opacity="{1-kap:.2f}"/>')
    hod = (t * 46) % 72
    m += (f'<path d="M300,492 q320,70 640,22 q360,-52 700,40 q180,54 300,10"'
          f' fill="none" stroke="#7c8694" stroke-width="56" stroke-linecap="round"'
          f' opacity=".75"/>')
    # кайма дорожки и витая нить: пунктир читался технической схемой
    for sgn in (-1, 1):
        m += (f'<path d="M300,{492+sgn*22} q320,70 640,22 q360,-52 700,40 q180,54 300,10"'
              f' fill="none" stroke="{MED}" stroke-width="8" stroke-linecap="round"'
              f' opacity=".55"/>')
    for j in range(2):
        m += (f'<path d="M300,{486+j*12} q320,70 640,22 q360,-52 700,40 q180,54 300,10"'
              f' fill="none" stroke="#b3bcc8" stroke-width="5" stroke-linecap="round"'
              f' opacity=".55" transform="translate(0,{-hod*.06+j*3:.1f})"/>')
    for i in range(14):
        vx_ = 320 + i * 128 - hod * .4
        m += (f'<path d="M{vx_:.0f},468 q22,24 0,48" fill="none" stroke="#6b7480"'
              f' stroke-width="6" opacity=".45" stroke-linecap="round"/>')
    # ГРАДУСНИК и ГРЕЛКА ковыляют по дорожке
    sh = (t * 78) % 1560
    gx = 600 + sh
    kov = 18 * abs(A.w(t, .62))
    m += (f'<g transform="translate({gx:.0f},{470-kov:.1f}) rotate({9*A.w(t,.62):.1f})">'
          f'{ten(0, 112, 54, 13, .4)}'
          f'<rect x="-22" y="-150" width="44" height="236" rx="22" fill="url(#stekl)" {o(6)}/>'
          f'<rect x="-9" y="-120" width="18" height="186" rx="9" fill="{ob.ALYJ}"/>'
          f'<circle cx="0" cy="96" r="34" fill="{ob.ALYJ}" {o(5)}/>'
          f'<path d="M-22,-110 h14 M-22,-74 h14 M-22,-38 h14" stroke="{K}" stroke-width="5"/></g>')
    gx2 = 470 + sh
    kov2 = 16 * abs(A.w(t, .62, .35))
    m += (f'<g transform="translate({gx2:.0f},{486-kov2:.1f}) rotate({-8*A.w(t,.62,.35):.1f})">'
          f'{ten(0, 104, 76, 15, .4)}'
          f'<path d="M-82,80 q-26,-130 20,-168 q-30,-44 18,-56 q62,-12 70,40'
          f' q56,46 32,184 q-70,26 -140,0 z" fill="#b8564c" {o(7)}/>'
          f'<path d="M-40,-96 q34,-18 66,0" fill="none" stroke="#e08b80" stroke-width="12"/>'
          f'<path d="M-50,20 q56,22 112,-6" fill="none" stroke="#8d2f28" stroke-width="9"/></g>')
    s += SL(Z_SRED, m)

    # УНЫЛАЯ ТУЧКА позади них и ТРЕЩИНА по плиткам
    f = b7_tuchka(370 + sh * .92, 290, .86, t, .2)
    for i in range(4):
        dq = ((t * .6 + i * .25) % 1.0)
        f += (f'<line x1="{370+sh*.92-60+i*42:.0f}" y1="{366+120*dq:.0f}"'
              f' x2="{370+sh*.92-74+i*42:.0f}" y2="{400+120*dq:.0f}"'
              f' stroke="#9fc0d8" stroke-width="7" stroke-linecap="round"'
              f' opacity="{(1-dq)*.75:.2f}"/>')
    tre = A.ease(A.seg(t, 3.4, 4.2))
    pts = []
    for i in range(25):
        u = i / 24.0
        pts.append((44 + u * 1836, 744 + 34 * math.sin(u * 13.0) + (18 if i % 2 else -18)))
    dd = "M%.0f,%.0f " % pts[0] + " ".join("L%.0f,%.0f" % p for p in pts[1:])
    f += (f'<path d="{dd}" fill="none" stroke="#2a1f1a" stroke-width="13"'
          f' stroke-linecap="round" stroke-dasharray="2000"'
          f' stroke-dashoffset="{2000*(1-tre):.0f}" opacity=".9"/>')
    f += (f'<path d="{dd}" fill="none" stroke="#6d5b4a" stroke-width="5"'
          f' stroke-dasharray="2000" stroke-dashoffset="{2000*(1-tre):.0f}" opacity=".8"/>')
    f += baza._ramka_pp("levo", "#090c13", .45)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.42))
    return s


def obida_saditsya_za_stol(t):
    """Праздничный стол: на свободный стул рядом с хмурым человеком взбирается
    надутая серая тучка, придвигает тарелку и заправляет салфетку. Живое:
    тучка взбирается, тарелка едет, салфетка встаёт. Человек — силуэт со
    спины, лица нет."""
    POL = 1000
    s = SL(Z_NEBO, b7_fon("b7m_f", "#36405c", "#1d2330"))

    d = b7_oboi(0, POL, "#47536f", 126, .15)
    d += ob.elka(1620, 880, 520, t)
    d += ob.girlyanda(-40, 180, 1180, 150, t, 12, 120)
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    m = b7_pol(POL, "b7m_p", "#89613d", "#3b2414")
    STY = 690
    m += ob.stol_prazdnik(60, STY, 1480, t)
    for i, px in enumerate((340, 760, 1180)):
        m += (f'<ellipse cx="{px}" cy="{STY-14}" rx="112" ry="40" fill="url(#krem)" {o(6)}/>'
              f'<ellipse cx="{px}" cy="{STY-18}" rx="78" ry="26" fill="#efe6cd" {o(4)}/>')
    m += ob.bokal(560, STY - 10, t, .8, .2)
    m += ob.bokal(980, STY - 10, t, .76, .5)
    m += b7_svecha_stola(1340, STY - 110, t, 1.0, .1)
    m += ob.mandarin(200, STY - 46, .9, .0, t)
    # ХМУРЫЙ ЧЕЛОВЕК на своём стуле — со спины
    cx, cb = 420, POL + 40
    m += ten(cx, cb, 130, 22, .5)
    m += f'<rect x="{cx-100}" y="{cb-640}" width="200" height="300" rx="16" fill="url(#derev)" {o(7)}/>'
    m += (f'<rect x="{cx-92}" y="{cb-250}" width="22" height="250" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{cx+70}" y="{cb-250}" width="22" height="250" fill="url(#derev)" {o(5)}/>')
    m += ob.figura(cx, cb - 150, 470, t, "#272034", "#e8b06a", False, ph=.7)
    s += SL(Z_SRED, m)

    # СВОБОДНЫЙ СТУЛ и ТУЧКА, которая на него взбирается
    f = ""
    sx, sb = 860, POL + 60
    f += ten(sx, sb, 140, 24, .5)
    f += f'<rect x="{sx-106}" y="{sb-680}" width="212" height="320" rx="16" fill="url(#derev)" {o(7)}/>'
    f += f'<rect x="{sx-110}" y="{sb-300}" width="220" height="34" rx="10" fill="url(#derev)" {o(7)}/>'
    f += (f'<rect x="{sx-98}" y="{sb-268}" width="24" height="268" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{sx+74}" y="{sb-268}" width="24" height="268" fill="url(#derev)" {o(5)}/>')
    vz = A.out(A.seg(t, .25, 1.7))
    tx = sx - 150 + 150 * vz
    ty = sb - 110 - 286 * vz - 70 * math.sin(math.pi * vz)   # садится НА сиденье
    f += b7_tuchka(tx, ty, 1.02, t, .1)
    # ТАРЕЛКА придвигается к тучке
    pr = A.ease(A.seg(t, 1.9, 1.2))
    ppx = sx + 150 - 110 * pr
    f += (f'<ellipse cx="{ppx:.0f}" cy="{STY-14}" rx="110" ry="40" fill="url(#krem)" {o(6)}/>'
          f'<ellipse cx="{ppx:.0f}" cy="{STY-18}" rx="76" ry="26" fill="#e7dcc0" {o(4)}/>')
    # САЛФЕТКА заправляется
    sl = A.over(A.seg(t, 2.6, 1.1))
    if sl > .02:
        f += (f'<g transform="translate({tx:.0f},{ty+124:.0f}) rotate({-14*sl:.1f}) scale({sl:.2f})">'
              f'<path d="M-62,0 l124,0 l-40,150 l-44,0 z" fill="url(#list)" {o(6)}/>'
              f'<path d="M-40,40 h92" stroke="{ob.ALYJ}" stroke-width="9" opacity=".7"/></g>')
    f += baza._ramka_pp("levo", "#090c14", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


def mir_na_kuhne(t):
    """Кухня перед праздником: в комнате за дверью накрывают, у окна одна
    стоит отвернувшись, вторая подходит — и они обнимаются, тучка-обида
    улетает за окно. Живое: фигура подходит, двое сходятся в одно пятно,
    тучка уплывает. Без лиц, только силуэты."""
    POL = 960
    s = SL(Z_NEBO, b7_fon("b7n_f", "#333f58", "#1b2330"))

    d = b7_plitka(60, 140, 780, 420, 118, "b7n_pl", "#dde8ef", "#b0c5d2")
    d += b7_oboi(0, POL, "#46526c", 128, .14)
    # дверь в комнату — тёплое пятно кадра
    dx, dy, dw, dh = 1330, 180, 470, POL - 180
    d += f'<rect x="{dx-28}" y="{dy-28}" width="{dw+56}" height="{dh+28}" rx="10" fill="url(#derev)" {o(8)}/>'
    d += f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#2a2236"/>'
    d += baza.teplo(dx + dw / 2, dy + dh * .45, 330, 330, .9)
    d += (f'<rect x="{dx+40}" y="{dy+330}" width="{dw-80}" height="30" rx="8"'
          f' fill="url(#derev)" {o(6)}/>')
    d += (f'<path d="M{dx+30},{dy+330} h{dw-60} v34 q{-(dw-60)/2:.0f},34 {-(dw-60):.0f},0 z"'
          f' fill="url(#rush)" {o(5)}/>')
    for i in range(3):
        d += (f'<ellipse cx="{dx+110+i*120}" cy="{dy+324}" rx="44" ry="15"'
              f' fill="url(#krem)" {o(4)}/>')
    d += ob.figura(dx + 120, dy + 318, 230, t, "#2b2436", "#f2c477", True, ph=.3)
    d += ob.figura(dx + 340, dy + 322, 220, t, "#2b2436", "#f2c477", False, ph=.75)
    for i in range(7):
        gx = dx + 40 + i * 64
        gor = .3 + .7 * abs(A.w(t, 2.0 + (i % 3) * .4, i * .2))
        d += f'<circle cx="{gx}" cy="{dy+60}" r="13" fill="{[SVET, ob.ALYJ][i%2]}" opacity="{gor:.2f}"/>'
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    m = b7_pol(POL, "b7n_p", "#8a6240", "#3c2515")
    # ОКНО кухни, за ним улетает тучка
    ox, oy, ow, oh = 120, 190, 470, 400
    uley = A.ease(A.seg(t, 2.6, 3.6))
    vid = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#24344e"/>'
           + baza._sneg_letit(t, 26, 5, .55, .7)
           + b7_tuchka(ox + 150 + 330 * uley, oy + 240 - 170 * uley,
                     .52 - .22 * uley, t, .4, True, .9 - .8 * uley))
    m += baza.okno_izby(ox, oy, ow, oh, t, vid, .35, False, True)
    m += (f'<rect x="40" y="{POL-250}" width="560" height="34" rx="10" fill="url(#derev)" {o(7)}/>')
    m += (f'<rect x="66" y="{POL-216}" width="510" height="216" rx="10" fill="#6d4a2b" {o(6)}/>')
    for i in range(2):
        m += baza.krynka(170 + i * 190, POL - 262, .72)
    s += SL(Z_SRED, m)

    # ДВОЕ У ОКНА: подходит и обнимает
    f = ""
    pod = A.ease(A.seg(t, .6, 2.2))
    obn = A.ease(A.seg(t, 2.8, 1.6))
    ax = 680
    bx = 1240 - 370 * pod
    f += ob.figura(ax, POL + 60, 640, t, "#2a2235", "#f0bf78", False, ph=.2, profil=obn > .3)
    f += ob.figura(bx, POL + 60, 640, t, "#312839", "#f2c477", True, ph=.6, profil=True)
    if obn > .02:
        f += baza.teplo((ax + bx) / 2, POL - 320, 300 * obn, 260 * obn, .55 * obn)
        f += (f'<path d="M{ax-10:.0f},{POL-330:.0f} q{(bx-ax)/2:.0f},{-70*obn:.0f}'
              f' {bx-ax:.0f},0" fill="none" stroke="#f0c070" stroke-width="{10*obn:.1f}"'
              f' stroke-linecap="round" opacity="{.8*obn:.2f}"/>')
        f += (f'<ellipse cx="{(ax+bx)/2:.0f}" cy="{POL-300:.0f}" rx="{150*obn:.0f}"'
              f' ry="{210*obn:.0f}" fill="none" stroke="#f0c070" stroke-width="7"'
              f' opacity="{.35*obn:.2f}"/>')
    f += baza._ramka_pp("levo", "#090c14", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


def tri_konverta_v_yaschik_komoda(t):
    """Три конверта со значками — монета, сердечко с градусником, домик с
    ключом — сами ложатся в ящик комода, ящик задвигается, листок на нём
    покачивается. Живое: конверты падают, ящик едет, листок качается."""
    POL = 980
    s = SL(Z_NEBO, b7_fon("b7o_f", "#3a3d55", "#1e2029"))

    d = b7_oboi(-10, POL + 10, "#4b4e6a", 118, .16)
    d += (f'<rect x="660" y="90" width="620" height="300" rx="14" fill="url(#med)" {o(7)}/>'
          f'<rect x="686" y="116" width="568" height="248" rx="10" fill="#54607e" {o(5)}/>'
          f'<path d="M716,352 l200,-210" stroke="#ffffff" stroke-width="26" opacity=".15"/>')
    d += baza.lampa(1620, 460, t, .78, True)
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    # КОМОД
    m = b7_pol(POL, "b7o_p", "#87603d", "#3a2313")
    kx, ky, kw = 420, 560, 1040
    m += ten(kx + kw / 2, POL + 6, kw * .5, 28, .55)
    m += f'<rect x="{kx}" y="{ky}" width="{kw}" height="{POL-ky}" rx="12" fill="url(#derev)" {o(9)}/>'
    m += f'<rect x="{kx-24}" y="{ky-34}" width="{kw+48}" height="40" rx="12" fill="url(#med)" {o(7)}/>'
    for i in range(2):
        yy = ky + 190 + i * 150
        m += (f'<rect x="{kx+30}" y="{yy}" width="{kw-60}" height="130" rx="10"'
              f' fill="#70492a" {o(6)}/>')
        for xx in (kx + 300, kx + kw - 300):
            m += f'<ellipse cx="{xx}" cy="{yy+66}" rx="30" ry="15" fill="url(#zol)" {o(4)}/>'
    # ВЕРХНИЙ ЯЩИК выдвинут и задвигается
    zad = A.ease(A.seg(t, 2.9, 1.7))
    vy = ky + 30 + 36 * (1 - zad)
    vh = 150
    m += (f'<path d="M{kx+40},{vy} h{kw-80} l-64,{vh*.5:.0f} h{-(kw-208):.0f} z"'
          f' fill="#2b1b0e" opacity="{.9-.3*zad:.2f}"/>')
    m += (f'<g transform="translate(0,{90*(1-zad):.0f})">'
          f'<rect x="{kx+20}" y="{vy+60}" width="{kw-40}" height="{vh}" rx="10"'
          f' fill="url(#dosk)" {o(8)}/>'
          f'<rect x="{kx+54}" y="{vy+88}" width="{kw-108}" height="{vh-56}" rx="8"'
          f' fill="none" stroke="#6d4a2a" stroke-width="7" opacity=".8"/>'
          f'<ellipse cx="{kx+kw/2:.0f}" cy="{vy+134}" rx="42" ry="18" fill="url(#zol)" {o(5)}/>')
    # ЛИСТОК на ящике — текст кладёт over
    kach = 5 * A.w(t, 3.2)
    m += (f'<g transform="rotate({kach:.2f} {kx+180} {vy+74})">'
          f'<rect x="{kx+118}" y="{vy+74}" width="150" height="178" rx="8"'
          f' fill="url(#list)" {o(6)}/>'
          f'<rect x="{kx+118}" y="{vy+74}" width="150" height="34" rx="8"'
          f' fill="{ob.ALYJ}" opacity=".85"/></g>')
    m += '</g>'
    s += SL(Z_SRED, m)

    # ТРИ КОНВЕРТА ложатся в ящик сами
    vidno = 1.0 - A.ease(A.seg(t, 2.9, .9))
    f = f'<g opacity="{vidno:.2f}">'
    for i, (zn, t0) in enumerate((("moneta", .2), ("serdce", .9), ("domik", 1.6))):
        p = A.ease(A.seg(t, t0, 1.1))
        if p <= .001:
            continue
        x0 = 560 + i * 400
        y0 = -160
        x1 = kx + 230 + i * 300
        y1 = vy + 110
        f += b7_konvert(x0 + (x1 - x0) * p, y0 + (y1 - y0) * (p * p * .6 + p * .4),
                      .92 - .18 * p, zn, t, i * .2)
    f += '</g>'
    f += baza._ramka_pp("levo", "#090b12", .48)
    s += SL(Z_LETIT, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


def prigorevshiy_pirog(t):
    """Из духовки выезжает пирог с чёрным краем, на полу две половинки
    блюдца, хозяйка со спины смеётся. Живое: дымок от пирога, половинки
    блюдца качаются, плечи трясутся от смеха. Без жести и без лиц."""
    POL = 1000
    s = SL(Z_NEBO, b7_fon("b7p_f", "#37455c", "#1d2633"))

    d = b7_plitka(560, 140, 820, 420, 122, "b7p_pl", "#e0ebf1", "#b3c7d4")
    d += b7_oboi(0, POL, "#48556e", 124, .14)
    d += f'<rect x="620" y="200" width="560" height="22" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(4):
        d += baza.krynka(690 + i * 128, 196, .56)
    d += baza.okno_izby(1400, 150, 360, 270, t, None, .45, True, True)
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    # ПЛИТА С ДУХОВКОЙ
    m = b7_pol(POL, "b7p_p", "#8b6341", "#3d2615")
    px, pw = 160, 700
    m += ten(px + pw / 2, POL + 6, pw * .5, 28, .55)
    m += f'<rect x="{px}" y="{POL-620}" width="{pw}" height="620" rx="16" fill="url(#chug)" {o(9)}/>'
    m += f'<rect x="{px-14}" y="{POL-646}" width="{pw+28}" height="36" rx="12" fill="url(#zhel)" {o(6)}/>'
    for i in range(4):
        m += (f'<circle cx="{px+130+(i%2)*300}" cy="{POL-560+(i//2)*62}" r="44"'
              f' fill="#1b1917" {o(5)}/>')
    # откинутая дверца и противень с пирогом
    m += (f'<path d="M{px+40},{POL-330} h{pw-80} l140,230 h{-(pw-80)-140:.0f} z"'
          f' fill="url(#zhel)" {o(7)}/>')
    m += (f'<rect x="{px+40}" y="{POL-350}" width="{pw-80}" height="30" rx="10"'
          f' fill="#4a5159" {o(5)}/>')
    m += (f'<rect x="{px+60}" y="{POL-560}" width="{pw-120}" height="220" rx="10"'
          f' fill="#120f0d" opacity=".9"/>')
    m += baza.teplo(px + pw / 2, POL - 430, 260, 150, .45)
    vy = A.out(A.seg(t, .2, 1.5))
    prx = px + pw / 2 + 70 * vy
    pry = POL - 430 + 110 * vy
    m += (f'<g transform="translate({prx:.0f},{pry:.0f})">'
          f'{ten(0, 54, 230, 26, .45)}'
          f'<ellipse cx="0" cy="0" rx="250" ry="76" fill="#55585e" {o(6)}/>'
          f'<ellipse cx="0" cy="-16" rx="206" ry="62" fill="url(#med)" {o(6)}/>'
          f'<path d="M-206,-16 q0,-60 206,-60 q206,0 206,60" fill="none" stroke="#1d1410"'
          f' stroke-width="28" opacity=".95"/>'
          f'<path d="M-206,-16 q0,62 206,62 q206,0 206,-62" fill="none" stroke="#2d2017"'
          f' stroke-width="18" opacity=".8"/>'
          f'<path d="M-170,-34 q82,-30 170,-24" fill="none" stroke="#f0cf90"'
          f' stroke-width="14" opacity=".6"/>'
          f'<path d="M-120,-40 q40,26 86,0 q40,26 86,-4" fill="none" stroke="#7d4a20"'
          f' stroke-width="9" opacity=".8"/></g>')
    s += SL(Z_SRED, m)

    # ДЫМОК, БЛЮДЦЕ и ХОЗЯЙКА
    f = baza.dym(prx, pry - 60, t, 6, .32, 420, .42, "#b8bfc8", 1.1)
    for sgn in (-1, 1):
        bx = 1130 + sgn * 150
        kach = 8 * A.w(t, 2.2, .25 if sgn > 0 else .0)
        f += ten(bx, POL + 18, 136, 19, .45)
        f += (f'<g transform="rotate({kach*sgn:.2f} {bx} {POL})">'
              f'<path d="M{bx-sgn*146},{POL+4} q{sgn*82},-102 {sgn*146},-6'
              f' q{-sgn*66},52 {-sgn*146},6 z" fill="url(#krem)" {o(7)}/>'
              f'<path d="M{bx-sgn*132},{POL-2} q{sgn*76},-88 {sgn*130},-6" fill="none"'
              f' stroke="#cdbb96" stroke-width="12" opacity=".9"/>'
              f'<path d="M{bx-sgn*108},{POL-12} q{sgn*64},-50 {sgn*104},-10" fill="none"'
              f' stroke="{TKAN2}" stroke-width="9" opacity=".75"/>'
              f'<path d="M{bx-sgn*18},{POL+2} l{sgn*16},-22 l{sgn*14},22 z"'
              f' fill="#b9a67f" opacity=".8"/></g>')
    tr = 5 * A.w(t, .33) + 7 * A.w(t, 7.4)
    hx, hb = 1520, POL + 36
    f += baza.teplo(hx, hb - 400, 320, 430, .38)
    f += (f'<g transform="rotate({tr*.3:.2f} {hx} {hb})" >'
          + ob.figura(hx, hb + 4 * abs(A.w(t, 7.4)), 630, t, "#2b2334", "#f2c477", True, ph=.5)
          + f'<path d="M{hx-118},{hb-452} q118,-36 236,6 l-10,240 q-114,30 -220,-6 z"'
            f' fill="url(#krem)" opacity=".88" {o(6)}/></g>')
    f += baza._ramka_pp("levo", "#090c13", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.40))
    return s


def svetlye_platya_vyhodyat_iz_shkafa(t):
    """Из шкафа одно за другим выплывают платья — белое в цветочек, голубое,
    жёлтое, красное — и кружатся по комнате. Живое: платья выплывают, подолы
    кружатся, свет в комнате теплеет."""
    POL = 980
    s = SL(Z_NEBO, b7_fon("b7q_f", "#3b4258", "#20242f"))

    teplee = A.ease(A.seg(t, .2, 2.4))
    d = b7_oboi(-10, POL + 10, "#4c5572", 120, .16)
    d += baza.teplo(1180, 420, 900, 700, .22 + .40 * teplee)
    d += (f'<rect x="-440" y="-340" width="{W+880}" height="{H+680}" fill="#ffd79a"'
          f' opacity="{.05+.13*teplee:.2f}"/>')
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    # ШКАФ слева, дверца открыта
    m = b7_pol(POL, "b7q_p", "#8b6340", "#3c2515")
    sx, sy, sw = 60, 140, 520
    m += ten(sx + sw / 2, POL + 6, sw * .5, 26, .55)
    m += f'<rect x="{sx}" y="{sy}" width="{sw}" height="{POL-sy}" rx="12" fill="url(#derev)" {o(9)}/>'
    m += f'<rect x="{sx+28}" y="{sy+30}" width="{sw-56}" height="{POL-sy-80}" rx="10" fill="#241508" {o(6)}/>'
    m += (f'<line x1="{sx+50}" y1="{sy+110}" x2="{sx+sw-50}" y2="{sy+110}"'
          f' stroke="#9aa3ab" stroke-width="12"/>')
    for i in range(4):
        m += (f'<path d="M{sx+90+i*80},{sy+110} q-26,70 -16,210" fill="none"'
              f' stroke="#4b3a47" stroke-width="30" opacity=".6"/>')
    m += b7_shkaf_stvorka(sx + sw - 20, sy, 300, POL - sy, "b7q_dv", .0)
    m += (f'<g transform="translate({sx+sw+300},{sy}) skewY(-6)">'
          f'<rect x="0" y="0" width="30" height="{POL-sy}" fill="#3d2615" opacity=".5"/></g>')
    # ПЛАТЬЯ выплывают и кружатся
    plat = (("#f4efe4", True), ("#9fc9e4", False), ("#efcf72", False), (ob.ALYJ, False))
    for i, (col, cvet) in enumerate(plat):
        p = A.out(A.seg(t, .15 + i * .42, 1.5))
        if p <= 0:
            continue
        a = -1.9 + i * 1.15 + t * .9
        cx = sx + sw + 70 + (390 + i * 205) * p
        cy = 300 + 190 * math.sin(a) - 60 * p + i * 34
        m += (f'<g transform="rotate({22*math.sin(a+i):.1f} {cx:.0f} {cy:.0f})">'
              + b7_vesh(cx, cy, 300 - i * 12, 430 - i * 18, col, t, i * .27, cvet, 20.0)
              + '</g>')
    s += SL(Z_SRED, m)

    f = b7_vesh(1700, 300, 330, 470, ob.ALYJ, t, .5, False, 22.0)
    f += baza._ramka_pp("levo", "#0a0d14", .45)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.34))
    return s


def globus_s_dvumya_ogonkami(t):
    """Школьный глобус на подставке: на двух сторонах горят огоньки, от них
    тянутся красные нитки, глобус поворачивается, нитки встречаются и
    завязываются в бант. Живое: глобус вращается, нитки тянутся, бант
    затягивается."""
    POL = 1010
    s = SL(Z_NEBO, b7_fon("b7r_f", "#32405c", "#181f2b"))

    d = b7_oboi(0, POL, "#45526e", 126, .15)
    d += baza.okno_izby(120, 190, 380, 330, t, None, .45, False, True)
    d += f'<rect x="1340" y="250" width="500" height="24" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(7):
        d += (f'<rect x="{1370+i*64}" y="{140+(i%3)*14}" width="48" height="{110-(i%3)*14}"'
              f' rx="6" fill="{[TKAN, ZEL2, MED, TKAN2, "#6b4428", ob.ALYJ, "#51607a"][i]}" {o(4)}/>')
    d += baza.teplo(960, 520, 640, 560, .34)
    d += b7_plintus(POL)
    s += SL(Z_DAL, d)

    # СТОЛ и ГЛОБУС
    m = b7_pol(POL, "b7r_p", "#8a6240", "#3b2414")
    STY = 860
    m += ten(960, STY + 110, 520, 34, .5)
    m += f'<rect x="300" y="{STY}" width="1340" height="40" rx="12" fill="url(#derev)" {o(8)}/>'
    m += f'<rect x="400" y="{STY+40}" width="40" height="{POL-STY-40}" fill="url(#derev)" {o(6)}/>'
    m += f'<rect x="1500" y="{STY+40}" width="40" height="{POL-STY-40}" fill="url(#derev)" {o(6)}/>'
    # подставка
    gx, gy, gr = 940, 520, 290
    m += f'<ellipse cx="{gx}" cy="{STY-6}" rx="150" ry="34" fill="url(#med)" {o(7)}/>'
    m += f'<rect x="{gx-22}" y="{gy+gr-40}" width="44" height="{STY-gy-gr+40}" fill="url(#med)" {o(6)}/>'
    m += (f'<path d="M{gx-gr-40},{gy-60} q{gr+40},{gr*1.5:.0f} {gr*2+80:.0f},0"'
          f' fill="none" stroke="url(#med)" stroke-width="26"/>')
    # шар
    m += f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="url(#voda)" {o(9)}/>'
    faza = t * .55
    m += f'<clipPath id="b7r_sh"><circle cx="{gx}" cy="{gy}" r="{gr-6}"/></clipPath>'
    m += f'<g clip-path="url(#b7r_sh)">'
    r = random.Random(21)
    for i in range(7):
        u = (i / 7.0 + faza * .5) % 1.0
        cx0 = gx - gr + u * gr * 2
        sc = max(.12, math.sin(math.pi * u))
        cy0 = gy + r.uniform(-160, 160)
        ww = r.uniform(70, 140) * sc
        hh = r.uniform(50, 100)
        m += (f'<path d="M{cx0-ww:.0f},{cy0:.0f}'
              f' q{ww*.3:.0f},{-hh*1.1:.0f} {ww*.9:.0f},{-hh*.7:.0f}'
              f' q{ww*.5:.0f},{hh*.2:.0f} {ww*1.1:.0f},{hh*.5:.0f}'
              f' q{-ww*.2:.0f},{hh*.9:.0f} {-ww*.8:.0f},{hh*.6:.0f}'
              f' q{-ww*.7:.0f},{-hh*.1:.0f} {-ww*1.2:.0f},{-hh*.4:.0f} z"'
              f' fill="{[ZEL2, TRAVA, "#6f8c4a", ZEL][i%4]}" opacity=".95" {o(4)}/>')
    for i in range(7):
        u = (i / 7.0 + faza) % 1.0
        rx_ = abs(math.cos(math.pi * u)) * gr
        m += (f'<ellipse cx="{gx}" cy="{gy}" rx="{rx_:.0f}" ry="{gr:.0f}" fill="none"'
              f' stroke="#cfe6f2" stroke-width="3" opacity=".30"/>')
    for yy in (-170, -60, 60, 170):
        m += (f'<ellipse cx="{gx}" cy="{gy+yy}" rx="{math.sqrt(max(1,gr*gr-yy*yy)):.0f}"'
              f' ry="18" fill="none" stroke="#cfe6f2" stroke-width="3" opacity=".25"/>')
    m += '</g>'
    m += (f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="none" {o(9)}/>')
    m += (f'<path d="M{gx-gr*.72:.0f},{gy-gr*.6:.0f} q{gr*.5:.0f},{-gr*.3:.0f} {gr*.86:.0f},{gr*.1:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="26" opacity=".18"/>')
    s += SL(Z_SRED, m)

    # ДВА ОГОНЬКА и НИТКИ, которые завязываются бантом
    f = ""
    ax, ay = gx - 196, gy - 40
    bx2, by2 = gx + 196, gy + 10
    for i, (ox_, oy_) in enumerate(((ax, ay), (bx2, by2))):
        pul = .6 + .4 * abs(A.w(t, 1.3, i * .4))
        f += baza.teplo(ox_, oy_, 120 * pul, 110 * pul, .8)
        f += f'<circle cx="{ox_}" cy="{oy_}" r="{16*pul:.0f}" fill="{SVET}" {o(3)}/>'
        f += f'<circle cx="{ox_}" cy="{oy_}" r="{34*pul:.0f}" fill="{SVET}" opacity=".35"/>'
    tyan = A.ease(A.seg(t, .25, 1.6))
    mxp, myp = gx, gy - 330
    for sgn, (ox_, oy_) in ((-1, (ax, ay)), (1, (bx2, by2))):
        ex = ox_ + (mxp - ox_) * tyan
        ey = oy_ + (myp - oy_) * tyan
        f += (f'<path d="M{ox_},{oy_} Q{ox_ + sgn*120:.0f},{(oy_+myp)/2 - 120:.0f} {ex:.0f},{ey:.0f}"'
              f' fill="none" stroke="{ob.ALYJ}" stroke-width="11" stroke-linecap="round"/>')
    ban = A.over(A.seg(t, 1.8, 1.2))
    if ban > .02:
        f += (f'<g transform="translate({mxp},{myp}) scale({ban:.2f})">')
        for sgn in (-1, 1):
            f += (f'<path d="M0,0 q{sgn*120},-88 {sgn*138},10 q{-sgn*44},72 {-sgn*138},-10 z"'
                  f' fill="{ob.ALYJ}" {o(6)}/>')
            f += (f'<path d="M0,4 q{sgn*52},62 {sgn*96},110" fill="none" stroke="{ob.ALYJ2}"'
                  f' stroke-width="12" stroke-linecap="round"/>')
        f += f'<circle cx="0" cy="0" r="24" fill="{ob.ALYJ2}" {o(5)}/>'
        f += '<circle cx="-8" cy="-8" r="8" fill="#f4a89c" opacity=".7"/>'
        f += '</g>'
    f += baza._ramka_pp("oba", "#090c13", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.40))
    return s


# ═══════════════ lok_b8.py ═══════════════

OKNO = (860, 300, 980, 551)


def b8_grad(i_, c1, c2, x2=0, y2=1):
    return (f'<linearGradient id="{i_}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def b8_komnata(y_pol=780, obo="#6f5a46", obo2="#50412f", polosy=True):
    """Стена комнаты с обоями в полоску и дощатый пол. Без неё кадр висит
    в пустоте, а наезд камеры не за что зацепить."""
    s = b8_grad("b8obo", obo, obo2)
    s += f'<rect width="{W}" height="{y_pol+20}" fill="url(#b8obo)"/>'
    if polosy:
        for i in range(17):
            x = i * (W / 16.0)
            s += (f'<rect x="{x:.0f}" y="0" width="22" height="{y_pol:.0f}"'
                  f' fill="#ffffff" opacity=".05"/>')
            s += (f'<rect x="{x+44:.0f}" y="0" width="7" height="{y_pol:.0f}"'
                  f' fill="#2b2016" opacity=".10"/>')
    s += baza.polovicy(y_pol)
    return s


def b8_kalendar(x, y, t, w_=1420, zapiski=3, goryat=(), n=7, h_=300):
    """Полотняный календарь: n кармашков-дней, последний красный.
    Записки выглядывают из кармашков и дышат — живой элемент главы."""
    kach = 3.4 * A.w(t, 5.2)
    s = ten(x + w_ / 2, y + h_ + 34, w_ * .45, 24, .34)
    s += (f'<rect x="{x-34:.0f}" y="{y-40:.0f}" width="{w_+68:.0f}" height="24" rx="11"'
          f' fill="url(#derev)" {o(6)}/>')
    for k in (0.08, 0.5, 0.92):
        kol = ob.ALYJ2 if k == 0.5 else "#4a3c2c"
        s += (f'<path d="M{x+w_*k:.0f},{y-28:.0f} v24" fill="none" stroke="{kol}"'
              f' stroke-width="6"/>')
    s += (f'<path d="M{x:.0f},{y:.0f} h{w_:.0f} v{h_:.0f}'
          f' q{-w_/2:.0f},{20+kach:.0f} {-w_:.0f},0 z" fill="url(#rush)" {o(7)}/>')
    s += (f'<path d="M{x+14:.0f},{y+20:.0f} h{w_-28:.0f}" fill="none" stroke="{ob.ALYJ}"'
          f' stroke-width="6" opacity=".55"/>')
    pw = w_ / n * .80
    for i in range(n):
        cx = x + w_ * (i + .5) / n
        posl = (i == n - 1)
        col = ob.ALYJ if posl else "#e4d4ad"
        gor = (.74 + .26 * abs(A.w(t, 1.7))) if posl else 1.0
        puls = .55 + .45 * abs(A.w(t, 1.9, i * .3))
        if i in goryat:
            s += teplo(cx, y + h_ * .60, pw * 1.6, h_ * 1.0, .60 * puls)
        # записка выглядывает ИЗ-ЗА кармашка — рисуется раньше него
        if i < zapiski:
            vy = -104 - 17 * A.w(t, 3.3 + i * .55, i * .2)
            kr = 3.4 * A.w(t, 4.1, i * .3)
            s += (f'<g transform="rotate({kr:.2f} {cx:.0f} {y+h_*.34:.0f})">'
                  f'<rect x="{cx-pw*.40:.0f}" y="{y+h_*.34+vy:.0f}" width="{pw*.80:.0f}"'
                  f' height="{-vy+36:.0f}" rx="7" fill="url(#list)" {o(5)}/>')
            for k in range(3):
                s += (f'<path d="M{cx-pw*.28:.0f},{y+h_*.34+vy+30+k*28:.0f} h{pw*.56:.0f}"'
                      f' fill="none" stroke="#6d6258" stroke-width="5" opacity=".75"/>')
            s += '</g>'
        s += (f'<rect x="{cx-pw/2:.0f}" y="{y+h_*.34:.0f}" width="{pw:.0f}"'
              f' height="{h_*.52:.0f}" rx="12" fill="{col}" opacity="{gor:.2f}" {o(6)}/>')
        s += (f'<rect x="{cx-pw/2+6:.0f}" y="{y+h_*.34:.0f}" width="{pw-12:.0f}"'
              f' height="{h_*.10:.0f}" rx="7" fill="#000000" opacity=".22"/>')
        s += (f'<path d="M{cx-pw/2+10:.0f},{y+h_*.48:.0f} h{pw-20:.0f}" fill="none"'
              f' stroke="#ffffff" stroke-width="5" opacity=".32"/>')
        # ПРОШИВКА по краю кармана и ярлык дня — иначе это просто прямоугольник
        s += (f'<rect x="{cx-pw/2+9:.0f}" y="{y+h_*.34+9:.0f}" width="{pw-18:.0f}"'
              f' height="{h_*.52-18:.0f}" rx="9" fill="none" stroke="{"#f6e6c0" if posl else "#9c8a63"}"'
              f' stroke-width="4" stroke-dasharray="11 8" opacity=".85"/>')
        s += (f'<rect x="{cx-pw*.30:.0f}" y="{y+h_*.38:.0f}" width="{pw*.60:.0f}"'
              f' height="{h_*.11:.0f}" rx="6" fill="{"#f3dcc6" if posl else "#cdb98d"}"'
              f' opacity=".9" {o(3)}/>')
        s += (f'<path d="M{cx-pw*.22:.0f},{y+h_*.62:.0f} h{pw*.44:.0f}" fill="none"'
              f' stroke="{"#8d1b1c" if posl else "#b2a075"}" stroke-width="6"'
              f' opacity=".8" stroke-linecap="round"/>')
        if i in goryat:
            s += (f'<rect x="{cx-pw/2:.0f}" y="{y+h_*.34:.0f}" width="{pw:.0f}"'
                  f' height="{h_*.52:.0f}" rx="12" fill="{SVET}" opacity="{.62*puls:.2f}"/>')
            s += (f'<rect x="{cx-pw/2:.0f}" y="{y+h_*.34:.0f}" width="{pw:.0f}"'
                  f' height="{h_*.52:.0f}" rx="12" fill="none" stroke="#fff6d2"'
                  f' stroke-width="8" opacity="{.85*puls:.2f}"/>')
    return s


def b8_listok(x, y, w_, h_, t, rost=(1.0, 1.0, 1.0), zacherk=(0.0, 0.0, 0.0),
            galka=0.0, ang=-3.0, svet=0.0):
    """Тетрадный листок в линейку: строчки пишутся, зачёркиваются, галочка."""
    s = f'<g transform="rotate({ang:.2f} {x+w_/2:.0f} {y+h_/2:.0f})">'
    s += ten(x + w_ / 2 + 12, y + h_ + 16, w_ * .46, 15, .45)
    if svet > 0:
        s += teplo(x + w_ / 2, y + h_ / 2, w_ * 1.15, h_ * 1.1, svet)
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="7"'
          f' fill="url(#list)" {o(5)}/>')
    for i in range(7):
        yy = y + h_ * (.16 + i * .115)
        s += (f'<line x1="{x+w_*.08:.0f}" y1="{yy:.0f}" x2="{x+w_*.92:.0f}" y2="{yy:.0f}"'
              f' stroke="#8fb6cf" stroke-width="3" opacity=".65"/>')
    s += (f'<line x1="{x+w_*.15:.0f}" y1="{y+6:.0f}" x2="{x+w_*.15:.0f}" y2="{y+h_-6:.0f}"'
          f' stroke="#d9918e" stroke-width="3" opacity=".6"/>')
    wmax = w_ * .60
    for i in range(3):
        yy = y + h_ * (.275 + i * .23)
        u = max(0.0, min(1.0, rost[i]))
        if u <= .01:
            continue
        d = f'M{x+w_*.21:.0f},{yy:.0f}'
        for k in range(1, 11):
            uu = k / 10.0
            if uu > u:
                break
            d += f' L{x+w_*.21+wmax*uu:.0f},{yy + (4 if k % 2 else -4):.0f}'
        s += f'<path d="{d}" fill="none" stroke="#39322e" stroke-width="{max(4,h_*.018):.0f}" stroke-linecap="round"/>'
        z = max(0.0, min(1.0, zacherk[i]))
        if z > .01:
            s += (f'<line x1="{x+w_*.18:.0f}" y1="{yy+3:.0f}"'
                  f' x2="{x+w_*.21+wmax*z:.0f}" y2="{yy-6:.0f}" stroke="{ob.ALYJ}"'
                  f' stroke-width="{max(4,h_*.018):.0f}" stroke-linecap="round"/>')
    if galka > .01:
        gx, gy = x + w_ * .56, y + h_ * .84
        r_ = h_ * .10
        p1 = min(1.0, galka * 2.0); p2 = max(0.0, galka * 2.0 - 1.0)
        s += (f'<path d="M{gx-r_*1.5:.0f},{gy-r_*.2:.0f} l{r_*p1:.0f},{r_*p1:.0f}"'
              f' fill="none" stroke="{ob.ALYJ}" stroke-width="{r_*.42:.0f}" stroke-linecap="round"/>')
        if p2 > .01:
            s += (f'<path d="M{gx-r_*.5:.0f},{gy+r_*.8:.0f} l{r_*2.1*p2:.0f},{-r_*2.5*p2:.0f}"'
                  f' fill="none" stroke="{ob.ALYJ}" stroke-width="{r_*.42:.0f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x+10:.0f},{y+h_*.06:.0f} l{w_*.34:.0f},{h_*.38:.0f}"'
          f' stroke="#ffffff" stroke-width="{max(6,w_*.03):.0f}" opacity=".20"/>')
    return s + '</g>'


def b8_karandash(tx, ty, ang=-28, L=330, col1="#e6b345", col2="#a3701b"):
    """Карандаш, который пишет сам: рук в этом ролике не рисуем."""
    s = b8_grad("b8kar", col1, col2)
    s += f'<g transform="translate({tx:.0f},{ty:.0f}) rotate({ang:.1f})">'
    s += ten(L * .5, 54, L * .42, 15, .35)
    s += f'<path d="M0,0 L44,-21 L44,21 Z" fill="#edd6a8" {o(4)}/>'
    s += f'<path d="M0,0 L16,-8 L16,8 Z" fill="#2a2320"/>'
    s += (f'<rect x="42" y="-21" width="{L-96:.0f}" height="42" fill="url(#b8kar)" {o(5)}/>')
    s += (f'<rect x="42" y="-16" width="{L-96:.0f}" height="9" fill="#ffffff" opacity=".22"/>')
    s += f'<rect x="{L-54:.0f}" y="-21" width="28" height="42" fill="url(#zhel)" {o(4)}/>'
    s += f'<rect x="{L-26:.0f}" y="-19" width="26" height="38" rx="9" fill="#cf8e86" {o(4)}/>'
    return s + '</g>'


def b8_ruchka(tx, ty, ang=-32, L=250):
    """Шариковая ручка — дописывает строчку сама."""
    s = b8_grad("b8ruch", "#2f5f7a", "#15303f")
    s += f'<g transform="translate({tx:.0f},{ty:.0f}) rotate({ang:.1f})">'
    s += ten(L * .5, 42, L * .4, 12, .3)
    s += f'<path d="M0,0 L34,-15 L34,15 Z" fill="url(#zhel)" {o(4)}/>'
    s += f'<rect x="32" y="-16" width="{L-70:.0f}" height="32" rx="6" fill="url(#b8ruch)" {o(5)}/>'
    s += f'<rect x="32" y="-12" width="{L-70:.0f}" height="7" fill="#ffffff" opacity=".2"/>'
    s += f'<rect x="{L-40:.0f}" y="-16" width="40" height="32" rx="10" fill="#1b2a33" {o(4)}/>'
    return s + '</g>'


def b8_kover(cid, nl, nr, ny, fl, fr, fy, t, c1="#9c4036", c2="#5a2220",
           uzor="#e3b64a", uop=.9, iznanka=False):
    """Большой узорный ковёр трапецией: ближний край шире дальнего."""
    d = (f'M{nl:.0f},{ny:.0f} L{nr:.0f},{ny:.0f} L{fr:.0f},{fy:.0f} L{fl:.0f},{fy:.0f} Z')
    s = b8_grad(cid + "g", c1, c2)
    s += f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
    s += f'<path d="{d}" fill="url(#{cid}g)" {o(7)}/>'
    s += f'<g clip-path="url(#{cid})" opacity="{uop:.2f}">'
    if iznanka:
        for i in range(34):
            v = i / 33.0
            yy = fy + (ny - fy) * v
            s += (f'<line x1="{fl+(nl-fl)*v-30:.0f}" y1="{yy:.0f}"'
                  f' x2="{fr+(nr-fr)*v+30:.0f}" y2="{yy:.0f}" stroke="#f3e8d2"'
                  f' stroke-width="{3+3*v:.1f}" opacity=".30"/>')
        for i in range(22):
            u = i / 21.0
            s += (f'<line x1="{fl+(fr-fl)*u:.0f}" y1="{fy:.0f}"'
                  f' x2="{nl+(nr-nl)*u:.0f}" y2="{ny:.0f}" stroke="#4a3a2a"'
                  f' stroke-width="4" opacity=".26"/>')
        # прошитая кайма изнанки и заплата — ковёр, а не плоскость
        cx_ = (nl + nr + fl + fr) / 4.0; cy_ = (ny + fy) / 2.0
        for k_, wd, col_ in ((.955, 16, "#6d5a42"), (.90, 7, "#efe0c4")):
            pts = " ".join("%.0f,%.0f" % (cx_ + (px - cx_) * k_, cy_ + (py - cy_) * k_)
                           for px, py in ((nl, ny), (nr, ny), (fr, fy), (fl, fy)))
            s += (f'<polygon points="{pts}" fill="none" stroke="{col_}"'
                  f' stroke-width="{wd}" opacity=".75"/>')
        s += (f'<rect x="{cx_-150:.0f}" y="{cy_-46:.0f}" width="230" height="130" rx="10"'
              f' fill="#8d7757" opacity=".55" stroke="#5c4a34" stroke-width="6"'
              f' stroke-dasharray="16 12"/>')
    else:
        cx_ = (nl + nr + fl + fr) / 4.0; cy_ = (ny + fy) / 2.0
        for k, wd in ((.92, 11), (.82, 6)):
            pts = " ".join("%.0f,%.0f" % (cx_ + (px - cx_) * k, cy_ + (py - cy_) * k)
                           for px, py in ((nl, ny), (nr, ny), (fr, fy), (fl, fy)))
            s += f'<polygon points="{pts}" fill="none" stroke="{uzor}" stroke-width="{wd}" opacity=".8"/>'
        for r_ in range(5):
            v = (r_ + .5) / 5.0
            yy = fy + (ny - fy) * v
            hl = fl + (nl - fl) * v; hr = fr + (nr - fr) * v
            for c_ in range(9):
                u = (c_ + .5) / 9.0
                xx = hl + (hr - hl) * u
                rr = 22 + 30 * v
                col = uzor if (r_ + c_) % 2 == 0 else "#f0e2c2"
                s += (f'<polygon points="{xx:.0f},{yy-rr*.62:.0f} {xx+rr*.52:.0f},{yy:.0f}'
                      f' {xx:.0f},{yy+rr*.62:.0f} {xx-rr*.52:.0f},{yy:.0f}"'
                      f' fill="{col}" opacity=".85"/>')
                s += (f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{rr*.16:.0f}" fill="#7d2420" opacity=".7"/>')
    s += '</g>'
    return s


def b8_vedro(x, y, s_, t, dnom_vverh=False, tryapka=False, ph=0.0):
    """Оцинкованное ведро. Тряпка свешивается через край и покачивается."""
    s = ten(x, y + 10 * s_, 96 * s_, 20 * s_, .5)
    if dnom_vverh:
        s += (f'<path d="M{x-78*s_:.0f},{y:.0f} l{14*s_:.0f},{-150*s_:.0f}'
              f' h{128*s_:.0f} l{14*s_:.0f},{150*s_:.0f} z" fill="url(#zhel)" {o(7)}/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{y-150*s_:.0f}" rx="{64*s_:.0f}" ry="{17*s_:.0f}"'
              f' fill="#8a9099" {o(6)}/>')
        s += (f'<path d="M{x-56*s_:.0f},{y-20*s_:.0f} q{56*s_:.0f},{18*s_:.0f} {112*s_:.0f},0"'
              f' fill="none" stroke="#c7d0d8" stroke-width="{7*s_:.0f}" opacity=".6"/>')
    else:
        s += (f'<path d="M{x-92*s_:.0f},{y-170*s_:.0f} l{20*s_:.0f},{170*s_:.0f}'
              f' h{144*s_:.0f} l{20*s_:.0f},{-170*s_:.0f} z" fill="url(#zhel)" {o(7)}/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{y-170*s_:.0f}" rx="{92*s_:.0f}" ry="{24*s_:.0f}"'
              f' fill="#5f6a74" {o(6)}/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{y-170*s_:.0f}" rx="{72*s_:.0f}" ry="{16*s_:.0f}"'
              f' fill="#2c3740" opacity=".75"/>')
        s += (f'<path d="M{x-84*s_:.0f},{y-120*s_:.0f} q{84*s_:.0f},{26*s_:.0f} {168*s_:.0f},0"'
              f' fill="none" stroke="#cdd6de" stroke-width="{8*s_:.0f}" opacity=".55"/>')
        dug = 24 * s_ * A.w(t, 4.6, ph)
        s += (f'<path d="M{x-96*s_:.0f},{y-180*s_:.0f} q{96*s_+dug:.0f},{-120*s_:.0f} {192*s_:.0f},0"'
              f' fill="none" stroke="#7d868f" stroke-width="{9*s_:.0f}"/>')
    if tryapka:
        dx = 13 * s_ * A.w(t, 3.1, ph + .2)
        s += (f'<path d="M{x+36*s_:.0f},{y-186*s_:.0f} q{44*s_:.0f},{-16*s_:.0f} {72*s_:.0f},{10*s_:.0f}'
              f' q{10*s_+dx:.0f},{86*s_:.0f} {-16*s_+dx:.0f},{140*s_:.0f}'
              f' q{-30*s_:.0f},{10*s_:.0f} {-44*s_:.0f},{-14*s_:.0f}'
              f' q{14*s_:.0f},{-66*s_:.0f} {-12*s_:.0f},{-136*s_:.0f} z"'
              f' fill="#8fb0c4" {o(6)}/>')
        s += (f'<path d="M{x+50*s_:.0f},{y-120*s_:.0f} q{26*s_:.0f},{40*s_:.0f} {10*s_+dx:.0f},{96*s_:.0f}"'
              f' fill="none" stroke="#cfe1ec" stroke-width="{7*s_:.0f}" opacity=".7"/>')
    return s


def b8_shchetka(x, y, s_, ang=0.0):
    """Щётка на длинной ручке."""
    s = f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-11*s_:.0f}" y="{y-420*s_:.0f}" width="{22*s_:.0f}" height="{420*s_:.0f}"'
          f' rx="10" fill="url(#derev)" {o(5)}/>')
    s += (f'<rect x="{x-62*s_:.0f}" y="{y-46*s_:.0f}" width="{124*s_:.0f}" height="{36*s_:.0f}"'
          f' rx="8" fill="url(#derev)" {o(6)}/>')
    for i in range(9):
        xx = x - 54 * s_ + i * 13.5 * s_
        s += (f'<line x1="{xx:.0f}" y1="{y-12*s_:.0f}" x2="{xx:.0f}" y2="{y+30*s_:.0f}"'
              f' stroke="#b98a46" stroke-width="{6*s_:.0f}" stroke-linecap="round"/>')
    return s + '</g>'


def b8_medalon(cx, cy, r, t, gor=1.0, nutro=""):
    """Медальон в золотой рамке: загорается и держит картинку."""
    s = ""
    if gor > .02:
        s += teplo(cx, cy, r * 2.1, r * 2.1, .50 * gor)
    s += ten(cx, cy + r + 20, r * .82, 18, .42)
    s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#zol)" {o(8)}/>'
    s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.88:.0f}" fill="#2a2a33"'
          f' opacity="{1-.0*gor:.2f}"/>')
    s += b8_grad(f"b8m{int(cx)}", "#8a7350", "#4a3a28")
    s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.86:.0f}" fill="url(#b8m{int(cx)})"/>')
    s += f'<clipPath id="b8mc{int(cx)}"><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.86:.0f}"/></clipPath>'
    s += f'<g clip-path="url(#b8mc{int(cx)})" opacity="{.22+.78*gor:.2f}">{nutro}</g>'
    s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.86:.0f}" fill="none"'
          f' stroke="{ob.ZOLOTO2}" stroke-width="5" opacity=".8"/>')
    s += (f'<path d="M{cx-r*.72:.0f},{cy-r*.44:.0f} a{r*.84:.0f},{r*.84:.0f} 0 0 1 {r*.72:.0f},{-r*.42:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{r*.1:.0f}" opacity="{.24*gor:.2f}"/>')
    return s


def b8_tarelka(cx, cy, r, t, podyom=0.0, moneta=False):
    """Тарелка; при подъёме её край отходит и из-под него бьёт свет."""
    s = ""
    if podyom > .02:
        s += teplo(cx - r * .55, cy + r * .05, r * 1.35, r * .55, .50 + .40 * podyom)
        s += (f'<path d="M{cx-r*1.00:.0f},{cy+r*.06:.0f}'
              f' L{cx-r*1.75:.0f},{cy-r*(.10+.26*podyom):.0f}'
              f' L{cx-r*.30:.0f},{cy-r*(.16+.30*podyom):.0f}'
              f' L{cx+r*.26:.0f},{cy+r*.08:.0f} Z"'
              f' fill="{SVET}" opacity="{.34+.34*podyom:.2f}"/>')
        s += (f'<ellipse cx="{cx-r*.62:.0f}" cy="{cy+r*.02:.0f}" rx="{r*.52:.0f}"'
              f' ry="{r*.13*(1+podyom):.0f}" fill="#fff6d2" opacity="{.45*podyom:.2f}"/>')
    if moneta:
        bl = .45 + .55 * abs(A.w(t, 2.2))
        s += (f'<ellipse cx="{cx-r*.72:.0f}" cy="{cy+r*.20:.0f}" rx="{r*.22:.0f}"'
              f' ry="{r*.09:.0f}" fill="url(#zol)" {o(4)}/>')
        s += (f'<ellipse cx="{cx-r*.76:.0f}" cy="{cy+r*.18:.0f}" rx="{r*.09:.0f}"'
              f' ry="{r*.04:.0f}" fill="#fff0bd" opacity="{bl:.2f}"/>')
    s += ten(cx + 8, cy + r * .30, r * .92, r * .18, .45)
    ang = -11 * podyom
    s += f'<g transform="rotate({ang:.2f} {cx+r:.0f} {cy:.0f}) translate(0,{-r*.10*podyom:.0f})">'
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r:.0f}" ry="{r*.30:.0f}"'
          f' fill="url(#krem)" {o(6)}/>')
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy-r*.03:.0f}" rx="{r*.70:.0f}" ry="{r*.20:.0f}"'
          f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="{r*.035:.0f}" opacity=".8"/>')
    s += (f'<path d="M{cx-r*.76:.0f},{cy-r*.10:.0f} a{r*.8:.0f},{r*.28:.0f} 0 0 1 {r*.70:.0f},{-r*.09:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{r*.07:.0f}" opacity=".35"/>')
    return s + '</g>'


def b8_gazety(x, y, s_, t, ph=0.0):
    """Стопка пожелтевших газет, перевязанная бечёвкой; уголки шевелятся."""
    s = ten(x, y + 10 * s_, 108 * s_, 18 * s_, .45)
    for i in range(7):
        yy = y - i * 20 * s_
        dx = (i % 2 * 2 - 1) * 7 * s_
        s += (f'<rect x="{x-104*s_+dx:.0f}" y="{yy-22*s_:.0f}" width="{208*s_:.0f}"'
              f' height="{22*s_:.0f}" rx="4" fill="{"#e2d4ac" if i%2 else "#d5c494"}" {o(4)}/>')
        if i >= 4:
            ug = 11 * s_ * A.w(t, 2.3 + i * .4, ph + i * .17)
            s += (f'<path d="M{x+104*s_+dx:.0f},{yy-22*s_:.0f} q{26*s_:.0f},{-6*s_+ug:.0f}'
                  f' {34*s_:.0f},{14*s_+ug:.0f} l{-34*s_:.0f},{8*s_:.0f} z"'
                  f' fill="#efe3bd" {o(4)}/>')
    for k in range(4):
        yy = y - (146 - k * 13) * s_
        wd = (150 if k else 96) * s_
        s += (f'<path d="M{x-86*s_:.0f},{yy:.0f} h{wd:.0f}" fill="none"'
              f' stroke="#9a8c62" stroke-width="{4*s_:.1f}" opacity=".7"/>')
    s += (f'<path d="M{x-30*s_:.0f},{y+6*s_:.0f} v{-150*s_:.0f}" fill="none"'
          f' stroke="#b59a63" stroke-width="{9*s_:.0f}"/>')
    s += (f'<path d="M{x-104*s_:.0f},{y-74*s_:.0f} h{208*s_:.0f}" fill="none"'
          f' stroke="#b59a63" stroke-width="{9*s_:.0f}"/>')
    s += (f'<path d="M{x-44*s_:.0f},{y-82*s_:.0f} q{14*s_:.0f},{-18*s_:.0f} {28*s_:.0f},0"'
          f' fill="none" stroke="#b59a63" stroke-width="{7*s_:.0f}"/>')
    return s


def b8_zont(x, y, s_, t, spica=True, ph=0.0):
    """Сложенный зонт; одна спица торчит вбок и дрожит."""
    s = ten(x + 10 * s_, y + 8 * s_, 44 * s_, 12 * s_, .4)
    s += (f'<path d="M{x:.0f},{y:.0f} v{-300*s_:.0f}" fill="none" stroke="{CHUGUN}"'
          f' stroke-width="{13*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x-62*s_:.0f},{y-306*s_:.0f} q{62*s_:.0f},{-150*s_:.0f} {124*s_:.0f},0'
          f' q{-16*s_:.0f},{170*s_:.0f} {-62*s_:.0f},{196*s_:.0f}'
          f' q{-46*s_:.0f},{-24*s_:.0f} {-62*s_:.0f},{-196*s_:.0f} z"'
          f' fill="{ob.HVOYA}" {o(7)}/>')
    for k in range(3):
        s += (f'<path d="M{x-34*s_+k*34*s_:.0f},{y-298*s_:.0f}'
              f' q{14*s_:.0f},{150*s_:.0f} {6*s_:.0f},{186*s_:.0f}"'
              f' fill="none" stroke="{ob.HVOYA2}" stroke-width="{7*s_:.0f}" opacity=".75"/>')
    s += (f'<path d="M{x-48*s_:.0f},{y-280*s_:.0f} q{30*s_:.0f},{-54*s_:.0f} {58*s_:.0f},{-20*s_:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{9*s_:.0f}" opacity=".22"/>')
    s += (f'<path d="M{x:.0f},{y-420*s_:.0f} v{120*s_:.0f}" fill="none" stroke="{ZHELEZ}"'
          f' stroke-width="{10*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x:.0f},{y:.0f} q{-26*s_:.0f},{20*s_:.0f} {-40*s_:.0f},{-6*s_:.0f}"'
          f' fill="none" stroke="{CHUGUN}" stroke-width="{13*s_:.0f}" stroke-linecap="round"/>')
    if spica:
        dr = 5.6 * A.w(t, .55, ph) + 2.4 * A.w(t, .17, ph * 2)
        s += (f'<g transform="rotate({dr:.2f} {x+34*s_:.0f} {y-256*s_:.0f})">'
              f'<path d="M{x+34*s_:.0f},{y-256*s_:.0f} l{186*s_:.0f},{-52*s_:.0f}"'
              f' fill="none" stroke="{K}" stroke-width="{15*s_:.0f}" stroke-linecap="round"/>'
              f'<path d="M{x+34*s_:.0f},{y-256*s_:.0f} l{186*s_:.0f},{-52*s_:.0f}"'
              f' fill="none" stroke="#c8d2dc" stroke-width="{8*s_:.0f}" stroke-linecap="round"/>'
              f'<circle cx="{x+220*s_:.0f}" cy="{y-308*s_:.0f}" r="{11*s_:.0f}" fill="#c8d2dc" {o(4)}/></g>')
    return s


def b8_chashka(x, y, s_, t, ph=0.0, ruchka_ryadom=True):
    """Чашка без ручки — ручка лежит рядом; чашка покачивается."""
    kach = 3.4 * A.w(t, 2.7, ph)
    s = ten(x + 6 * s_, y + 8 * s_, 70 * s_, 14 * s_, .45)
    s += f'<g transform="rotate({kach:.2f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x-62*s_:.0f},{y-128*s_:.0f} q{10*s_:.0f},{128*s_:.0f} {62*s_:.0f},{128*s_:.0f}'
          f' q{52*s_:.0f},0 {62*s_:.0f},{-128*s_:.0f} z" fill="url(#krem)" {o(7)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-128*s_:.0f}" rx="{62*s_:.0f}" ry="{19*s_:.0f}"'
          f' fill="#cfc0a1" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-128*s_:.0f}" rx="{48*s_:.0f}" ry="{13*s_:.0f}"'
          f' fill="#8f8572" opacity=".65"/>')
    s += (f'<path d="M{x-58*s_:.0f},{y-104*s_:.0f} q{58*s_:.0f},{18*s_:.0f} {116*s_:.0f},0"'
          f' fill="none" stroke="{ob.ALYJ}" stroke-width="{8*s_:.0f}" opacity=".75"/>')
    s += (f'<path d="M{x+36*s_:.0f},{y-116*s_:.0f} q{14*s_:.0f},{54*s_:.0f} {2*s_:.0f},{96*s_:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{9*s_:.0f}" opacity=".3"/>')
    s += (f'<path d="M{x+56*s_:.0f},{y-110*s_:.0f} q{10*s_:.0f},{4*s_:.0f} {12*s_:.0f},{14*s_:.0f}"'
          f' fill="none" stroke="#8f8572" stroke-width="{6*s_:.0f}"/>')
    s += '</g>'
    if ruchka_ryadom:
        hx, hy = x + 162 * s_, y - 12 * s_
        s += ten(hx, y + 8 * s_, 64 * s_, 12 * s_, .4)
        # ушко ручки: наружная и внутренняя дуги одним контуром
        s += (f'<path d="M{hx-56*s_:.0f},{hy+30*s_:.0f}'
              f' a{62*s_:.0f},{58*s_:.0f} 0 1 1 {112*s_:.0f},0'
              f' l{-26*s_:.0f},{4*s_:.0f}'
              f' a{38*s_:.0f},{36*s_:.0f} 0 1 0 {-60*s_:.0f},0 z"'
              f' fill="#e4d6b8" {o(max(4, 6*s_))}/>')
        s += (f'<path d="M{hx-44*s_:.0f},{hy+6*s_:.0f}'
              f' a{50*s_:.0f},{48*s_:.0f} 0 0 1 {34*s_:.0f},{-40*s_:.0f}"'
              f' fill="none" stroke="#ffffff" stroke-width="{8*s_:.0f}" opacity=".45"/>')
        s += (f'<path d="M{hx-56*s_:.0f},{hy+30*s_:.0f} l{14*s_:.0f},{10*s_:.0f}'
              f' M{hx+56*s_:.0f},{hy+30*s_:.0f} l{-14*s_:.0f},{10*s_:.0f}"'
              f' fill="none" stroke="#b5a582" stroke-width="{6*s_:.0f}"/>')
    return s


def b8_stul(x, y, s_, ang=0.0):
    s = f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
    s += ten(x, y + 8 * s_, 60 * s_, 12 * s_, .4)
    s += (f'<rect x="{x-56*s_:.0f}" y="{y-120*s_:.0f}" width="{112*s_:.0f}" height="{22*s_:.0f}"'
          f' rx="8" fill="url(#derev)" {o(5)}/>')
    s += (f'<rect x="{x-48*s_:.0f}" y="{y-300*s_:.0f}" width="{18*s_:.0f}" height="{190*s_:.0f}"'
          f' rx="7" fill="url(#derev)" {o(4)}/>')
    s += (f'<rect x="{x-48*s_:.0f}" y="{y-280*s_:.0f}" width="{96*s_:.0f}" height="{18*s_:.0f}"'
          f' rx="7" fill="url(#derev)" {o(4)}/>')
    for dx in (-46, 40):
        s += (f'<rect x="{x+dx*s_:.0f}" y="{y-100*s_:.0f}" width="{14*s_:.0f}"'
              f' height="{100*s_:.0f}" fill="url(#derev)" {o(4)}/>')
    return s + '</g>'


def b8_blyudo_pelmeni(cx, cy, s_, t, ph=0.0, par_on=True):
    """Блюдо пельменей: горка, пар, золотой ободок."""
    s = ten(cx + 6 * s_, cy + 22 * s_, 150 * s_, 26 * s_, .45)
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{156*s_:.0f}" ry="{48*s_:.0f}"'
          f' fill="url(#krem)" {o(6)}/>')
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy-4*s_:.0f}" rx="{126*s_:.0f}" ry="{36*s_:.0f}"'
          f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="{6*s_:.0f}" opacity=".8"/>')
    r = random.Random(21)
    for i in range(13):
        a = r.uniform(0, 6.28)
        rr = r.uniform(0, 1) ** .5
        px = cx + math.cos(a) * 104 * s_ * rr
        py = cy - 16 * s_ - abs(math.sin(a)) * 16 * s_ * rr - r.uniform(0, 26) * s_
        s += (f'<path d="M{px-30*s_:.0f},{py:.0f} q{30*s_:.0f},{-34*s_:.0f} {60*s_:.0f},0'
              f' q{-30*s_:.0f},{18*s_:.0f} {-60*s_:.0f},0 z" fill="#f2e6cc" {o(4)}/>')
        s += (f'<path d="M{px-18*s_:.0f},{py-10*s_:.0f} q{18*s_:.0f},{-10*s_:.0f} {36*s_:.0f},0"'
              f' fill="none" stroke="#ffffff" stroke-width="{4*s_:.0f}" opacity=".6"/>')
    if par_on:
        s += baza.par(cx - 40 * s_, cy - 54 * s_, t + ph, 4, .45, 170 * s_, .45, s_)
        s += baza.par(cx + 46 * s_, cy - 48 * s_, t + ph + .7, 4, .4, 150 * s_, .42, s_)
    return s


def b8_struyka(x, y, t, L=420, ph=0.0, col=None, op=.8):
    """Оранжевая струйка запаха — волна, которая плывёт вверх."""
    c = col or ob.MANDA
    d = f'M{x:.0f},{y:.0f}'
    for i in range(1, 13):
        u = i / 12.0
        yy = y - L * u
        xx = x + 34 * u * math.sin(2 * math.pi * (u * 1.3 - t * .32 + ph))
        d += f' L{xx:.0f},{yy:.0f}'
    s = (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="13"'
         f' stroke-linecap="round" opacity="{op*.55:.2f}"/>')
    s += (f'<path d="{d}" fill="none" stroke="{SVET}" stroke-width="5"'
          f' stroke-linecap="round" opacity="{op*.5:.2f}"/>')
    return s


def b8_proyom(x, y, w_, h_, t, sila=1.0):
    """Светящийся дверной проём: из него льётся тёплый свет на пол."""
    s = b8_grad("b8pro", "#fff6d8", "#efba55")
    s += teplo(x + w_ / 2, y + h_ * .42, w_ * 2.0, h_ * 1.05, .75 * sila)
    s += (f'<rect x="{x-22:.0f}" y="{y-24:.0f}" width="{w_+44:.0f}" height="{h_+28:.0f}"'
          f' rx="12" fill="url(#derev)" {o(8)}/>')
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="url(#b8pro)"/>'
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="{SVET}"'
          f' opacity="{.14+.10*abs(A.w(t,2.6)):.2f}"/>')
    # глубина проёма: притолока в тени, косяки темнее, светлее к полу
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_*.30:.0f}"'
          f' fill="#8a5a1e" opacity=".34"/>')
    for sgn, xx in ((1, x), (-1, x + w_)):
        s += (f'<rect x="{xx if sgn>0 else xx-54:.0f}" y="{y:.0f}" width="54"'
              f' height="{h_:.0f}" fill="#a87324" opacity=".26"/>')
    s += (f'<ellipse cx="{x+w_/2:.0f}" cy="{y+h_*.86:.0f}" rx="{w_*.44:.0f}"'
          f' ry="{h_*.20:.0f}" fill="#ffffff" opacity=".30"/>')
    # ПОРОГ: проём стоит на полу, а не висит прямоугольником
    s += (f'<rect x="{x-26:.0f}" y="{y+h_-10:.0f}" width="{w_+52:.0f}" height="30"'
          f' rx="9" fill="url(#med)" {o(7)}/>')
    s += (f'<path d="M{x:.0f},{y+h_:.0f} L{x-300:.0f},{H+40} L{x+w_+340:.0f},{H+40}'
          f' L{x+w_:.0f},{y+h_:.0f} Z" fill="{SVET}" opacity="{.22*sila:.2f}"/>')
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="none" {o(8)}/>'
    return s


def b8_meshok(x, y, s_, t, ph=0.0, szhat=0.0):
    """Огромный мешок старья: зонт и газеты торчат из горловины."""
    sx = 1.0 - .13 * szhat
    s = ten(x, y + 12 * s_, 210 * s_, 32 * s_, .5)
    s += f'<g transform="translate({x:.0f},{y:.0f}) scale({s_*sx:.3f},{s_:.3f})">'
    s += (f'<path d="M-196,0 q-34,-212 36,-318 q58,-46 136,-46 q96,0 150,56'
          f' q68,104 40,308 z" fill="url(#solom)" {o(9)}/>')
    s += (f'<path d="M-150,-54 q140,34 286,-10" fill="none" stroke="#a07c2e"'
          f' stroke-width="12" opacity=".6"/>')
    s += (f'<path d="M-120,-200 q114,38 236,-14" fill="none" stroke="#a07c2e"'
          f' stroke-width="10" opacity=".45"/>')
    s += (f'<path d="M-114,-330 q110,-44 218,6 q-30,46 -108,46 q-80,0 -110,-52 z"'
          f' fill="#c9ad72" {o(7)}/>')
    s += (f'<path d="M-100,-336 q104,-40 198,4" fill="none" stroke="#8a6d33"'
          f' stroke-width="12" stroke-dasharray="14 12"/>')
    # ВЕРЁВКА с узлом на горловине
    s += (f'<path d="M-118,-290 q112,52 224,-8" fill="none" stroke="#7d5f28"'
          f' stroke-width="19" stroke-linecap="round"/>')
    s += (f'<path d="M-118,-282 q112,52 224,-8" fill="none" stroke="#c0a055"'
          f' stroke-width="8" stroke-linecap="round" opacity=".8"/>')
    s += (f'<path d="M96,-298 q34,-14 42,16 q-26,22 -48,8 z" fill="#7d5f28" {o(5)}/>'
          f'<path d="M126,-278 q24,44 6,86" fill="none" stroke="#7d5f28"'
          f' stroke-width="11" stroke-linecap="round"/>')
    # углы содержимого распирают бок — мешок, а не гладкий купол
    for lx_, ly_, rr_ in ((-132, -176, 52), (108, -222, 44), (-52, -96, 58), (74, -84, 40)):
        s += (f'<ellipse cx="{lx_}" cy="{ly_}" rx="{rr_}" ry="{rr_*.78:.0f}"'
              f' fill="#b99a5e" opacity=".32"/>')
        s += (f'<path d="M{lx_-rr_},{ly_+rr_*.3:.0f} q{rr_},{-rr_*.9:.0f} {rr_*2},0"'
              f' fill="none" stroke="#8a6d33" stroke-width="7" opacity=".45"/>')
    s += f'<path d="M-160,-250 q50,-70 70,-110" fill="none" stroke="#ffffff" stroke-width="16" opacity=".16"/>'
    s += '</g>'
    s += b8_zont(x + 66 * s_, y - 316 * s_, s_ * .86, t, True, ph)
    s += (f'<g transform="translate({x-120*s_:.0f},{y-336*s_:.0f}) rotate(-24)">'
          + b8_gazety(0, 0, s_ * .72, t, ph + .3) + '</g>')
    return s


def b8_figury_vokrug(cx, cy, rx, ry, t, n=6, h0=250, seed=3, krasnyh=(0, 3)):
    """Родные вокруг круглого стола: дальние мельче, ближние крупнее."""
    r = random.Random(seed)
    out = []
    for i in range(n):
        a = math.pi * (.08 + .84 * (i + .5) / n) + math.pi
        x = cx + math.cos(a) * rx * 1.02
        y = cy + math.sin(a) * ry * 1.02
        k = .72 + .5 * (y - (cy - ry)) / (2 * ry + 1)
        out.append((y, x, k, i))
    out.sort()
    s = ""
    for y, x, k, i in out:
        s += ob.figura(x, y + 96 * k, h0 * k, t,
                       col=("#2e2330", "#243040", "#33262c")[i % 3],
                       kant="#f0c070", platok=(i % 3 == 1), ph=i * .19,
                       krasnoe=(i in krasnyh))
    return s


def sem_karmashkov_do_prazdnika(t):
    """Морозное утро, стена с полотняным календарём из семи кармашков-дней.
    Живое: записки выглядывают, солнечный зайчик ползёт, красный кармашек мерцает."""
    vid = (baza._nebo("den", t, zvezdy=False)
           + baza._oblaka(t, 240, 3, 9, .55, "#ffffff", 5.0)
           + baza._sneg_letit(t, 18, 8, .45, .5))
    for i, (ex, eh) in enumerate(((1430, 150), (1560, 196), (1690, 126))):
        vid += (f'<path d="M{ex:.0f},470 l{-eh*.34:.0f},0 l{eh*.34:.0f},{-eh:.0f}'
                f' l{eh*.34:.0f},{eh:.0f} z" fill="#56687d" opacity=".75"/>')
    zx = 170 + 880 * ((t * .055) % 1.0)

    s = SL(Z_DAL,
           b8_komnata(820, "#8a7158", "#63513a")
           + baza.doski(0, 0, W, 820, 118, False, "dosk")
           + f'<rect width="{W}" height="820" fill="#f2e2c4" opacity=".15"/>'
           + baza.okno_izby(1390, 150, 440, 360, t, vid=vid, moroz=.09, svet=True)
           + teplo(1610, 330, 640, 540, .62)
           + teplo(zx, 500, 260, 210, .40)
           + f'<ellipse cx="{zx:.0f}" cy="500" rx="140" ry="104" fill="{SVET}" opacity=".20"/>')

    s += SL(Z_SRED,
            b8_kalendar(130, 430, t, 1160, zapiski=3, goryat=(), n=7, h_=320)
            + baza.luch(1280, 250, 250, 740, t, .20))

    s += baza.mebel_hlam(40, 1010, 560, t, 13)

    s += SL(Z_PERED,
            baza._ramka_pp("levo", "#120e0a", .72)
            + baza.lavka(1240, 940, 520)
            + baza.krynka(1360, 930, .9)
            + ob.mandarin(1530, 900, .9, 0.0, t)
            + ob.mandarin(1620, 916, .78, 0.0, t))
    s += baza.vinetka(.40)
    return s


def listok_s_dolgami(t):
    """Стол, тетрадный листок, карандаш пишет три строчки и ставит значки.
    Живое: карандаш пишет, значки появляются, листок чуть сдвигается."""
    rost = [A.ease(A.seg(t, .25 + i * 1.05, .85)) for i in range(3)]
    sdv = 5 * A.w(t, 6.4)
    lx, ly, lw, lh = 250, 290, 620, 730

    s = SL(Z_DAL,
           b8_komnata(360, "#5c4b3c", "#3b3025")
           + baza.vozduh(520, 220, t, 940, .34)
           + baza.lampa(430, 180, t, .95, abazhur=True)
           + baza.polka(1130, 180, 690)
           + baza.krynka(1240, 176, .7) + baza.krynka(1710, 176, .62)
           + ob.mandarin(1430, 150, .66, 0.0, t))

    stol = (f'<rect y="360" width="{W}" height="{H-360}" fill="url(#derev)"/>'
            + f'<rect y="352" width="{W}" height="24" fill="{DOSKA2}" {o(6)}/>')
    for i in range(10):
        stol += (f'<line x1="0" y1="{430+i*74}" x2="{W}" y2="{430+i*74}"'
                 f' stroke="#5a3b22" stroke-width="4" opacity=".4"/>')
    s += SL(Z_SRED, stol + teplo(620, 640, 920, 520, .42))

    # значки у строчек: монета, книга, трубка
    zn = ""
    for i in range(3):
        u = A.over(A.seg(t, 1.0 + i * 1.05, .45))
        if u <= .02:
            continue
        zx, zy = lx + lw + 330, ly + lh * (.275 + i * .23) - 4
        zn += f'<g transform="translate({zx:.0f},{zy:.0f}) scale({u*1.75:.3f})">'
        zn += f'<circle r="64" fill="{SVET}" opacity=".12"/>'
        if i == 0:
            bl = .4 + .6 * abs(A.w(t, 2.3))
            zn += f'<circle r="46" fill="url(#zol)" {o(7)}/>'
            zn += f'<circle r="30" fill="none" stroke="{ob.ZOLOTO2}" stroke-width="6"/>'
            zn += f'<circle cx="-15" cy="-15" r="13" fill="#fff0bd" opacity="{bl:.2f}"/>'
        elif i == 1:
            zn += f'<rect x="-48" y="-38" width="96" height="78" rx="8" fill="{ob.ALYJ}" {o(7)}/>'
            zn += f'<rect x="-34" y="-30" width="74" height="62" rx="5" fill="url(#list)" {o(5)}/>'
            zn += f'<path d="M3,-30 v62" fill="none" {o(6)}/>'
            zn += f'<path d="M-22,-14 h22 M-22,2 h22 M8,-14 h22 M8,2 h22" stroke="#8f8572" stroke-width="4"/>'
        else:
            zn += (f'<path d="M-52,26 q-18,-38 12,-54 q20,-9 27,11 q-14,7 -9,20'
                   f' q27,27 61,18 q7,-14 23,-7 q18,11 7,32 q-45,25 -121,-20 z"'
                   f' fill="{CHUGUN}" {o(7)}/>')
            zn += f'<path d="M-34,-20 q7,-11 18,-7" fill="none" stroke="#9aa3ac" stroke-width="7"/>'
            zn += f'<path d="M34,16 q10,-9 20,-3" fill="none" stroke="#9aa3ac" stroke-width="7"/>'
        zn += '</g>'

    # карандаш: остриё стоит на конце текущей строчки
    akt = 0
    for i in range(3):
        if rost[i] > .01:
            akt = i
    px = lx + lw * .21 + lw * .60 * rost[akt]
    py = ly + lh * (.275 + akt * .23) + 6

    s += SL(Z_PERED,
            b8_listok(lx + sdv, ly, lw, lh, t, rost=rost, ang=-3.4, svet=.0)
            + zn
            + b8_karandash(px + sdv, py, -29, 360)
            + baza._ramka_pp("levo", "#140f0b", .55))
    s += baza.vinetka(.46)
    return s


def tri_nevypolnennyh_obeschaniya(t):
    """Три вещи ждут своей очереди: телефон с диском, чужая дверь с ковриком,
    открытка с недописанным рецептом. Живое: диск крутится, свет под дверью
    дышит, ручка дописывает строку."""
    s = SL(Z_DAL,
           b8_komnata(700, "#5a4a3e", "#372c24")
           + baza.vozduh(960, 300, t, 1000, .30)
           + f'<rect y="700" width="{W}" height="{H-700}" fill="url(#derev)" opacity=".9"/>')

    # тумбы под тремя вещами
    tum = ""
    for cx in (330, 1590):
        tum += ten(cx, 952, 250, 24, .45)
        tum += (f'<rect x="{cx-240:.0f}" y="770" width="480" height="180" rx="12"'
                f' fill="url(#derev)" {o(7)}/>')
        tum += (f'<rect x="{cx-220:.0f}" y="790" width="440" height="20" rx="8"'
                f' fill="#ffffff" opacity=".12"/>')
    s += SL(Z_SRED, tum)

    # ── телефон с диском
    p = (t / 1.7) % 1.0
    ang = 300 * A.ease(min(1.0, p * 2.3)) if p < .44 else 300 * (1 - A.ease((p - .44) / .56))
    tel = ten(370, 784, 240, 24, .45)
    tel += teplo(370, 650, 440, 380, .34)
    tel += f'<path d="M170,774 q0,-170 200,-170 q200,0 200,170 z" fill="url(#chug)" {o(8)}/>'
    tel += f'<path d="M206,652 q164,-76 328,0" fill="none" stroke="#5d5956" stroke-width="16"/>'
    tel += f'<circle cx="370" cy="638" r="104" fill="#ded6c6" {o(7)}/>'
    tel += f'<g transform="rotate({ang:.1f} 370 638)">'
    for i in range(10):
        a = -1.9 + i * .62
        tel += (f'<circle cx="{370+math.cos(a)*72:.0f}" cy="{638+math.sin(a)*72:.0f}"'
                f' r="17" fill="#3a3733" opacity=".85"/>')
    tel += f'<circle cx="370" cy="638" r="28" fill="#a79e92" {o(5)}/></g>'
    tel += f'<circle cx="370" cy="638" r="104" fill="none" {o(7)}/>'
    tel += (f'<path d="M288,586 a104,104 0 0 1 78,-50" fill="none" stroke="#ffffff"'
            f' stroke-width="14" opacity=".35"/>')
    # снятая трубка лежит рядом, шнур спиралью
    tel += f'<g transform="translate(252,786) rotate(-10) scale(1.3)">'
    tel += ten(60, 14, 100, 14, .4)
    tel += (f'<path d="M-52,0 q-20,-32 6,-44 q18,-8 24,10 l92,-10 q6,-18 24,-10'
            f' q26,12 6,44 q-78,24 -152,10 z" fill="{CHUGUN}" {o(6)}/>')
    tel += (f'<path d="M-30,-22 q66,16 128,-6" fill="none" stroke="#8b9199"'
            f' stroke-width="7" opacity=".6"/>')
    tel += '</g>'
    sh = f'M316,758'
    for i in range(9):
        sh += f' q16,{20 if i % 2 == 0 else -20} 32,0'
    tel += f'<path d="{sh}" fill="none" stroke="#2b2724" stroke-width="11" opacity=".9"/>'

    # ── чужая дверь с ковриком
    svs = .35 + .35 * abs(A.w(t, 2.9))
    dv = (f'<rect x="724" y="258" width="472" height="520" rx="6" fill="#4a3728" {o(7)}/>'
          + f'<rect x="748" y="282" width="424" height="496" rx="4" fill="#2a1f16" {o(5)}/>'
          + f'<rect x="760" y="296" width="400" height="482" rx="4" fill="#1d2129"/>'
          + baza.dver(770, 310, 380, 456, 0.0, "url(#derev)", True, False)
          + f'<rect x="716" y="770" width="488" height="22" rx="8" fill="{MED}" {o(6)}/>')
    dv += (f'<rect x="770" y="752" width="380" height="16" fill="{SVET}"'
           f' opacity="{svs:.2f}"/>')
    dv += teplo(960, 770, 320, 110, svs * .85)
    ug = 11 * A.w(t, 3.6)
    dv += ten(960, 828, 240, 20, .45)
    dv += (f'<path d="M760,778 h400 l{-42+ug:.0f},74 h{-316-ug*2:.0f} z"'
           f' fill="#a3875f" {o(7)}/>')
    for i in range(7):
        dv += (f'<path d="M{792+i*60:.0f},786 l-10,60" fill="none" stroke="#6d5736"'
               f' stroke-width="8" opacity=".85"/>')
    dv += f'<path d="M776,794 h368" fill="none" stroke="#d6bd8c" stroke-width="7" opacity=".7"/>'

    # ── открытка с недописанным рецептом
    rost = A.ease(A.seg(t, 1.1, 2.4))
    otk = ""
    ox, oy, ow, oh = 1380, 470, 420, 300
    otk += ten(1600, 786, 220, 18, .42)
    otk += f'<g transform="rotate(-5 {ox+ow/2:.0f} {oy+oh/2:.0f})">'
    otk += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="9" fill="url(#list)" {o(6)}/>'
    otk += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="54" rx="9" fill="{ob.ALYJ}" opacity=".85"/>')
    otk += (f'<path d="M{ox+18},{oy+30} q{ow*.2:.0f},-26 {ow*.4:.0f},0" fill="none"'
            f' stroke="{ob.ZOLOTO}" stroke-width="7" opacity=".9"/>')
    for i in range(4):
        yy = oy + 100 + i * 46
        w2 = ow * .72 if i < 3 else ow * .72 * rost
        otk += (f'<path d="M{ox+36},{yy} h{w2:.0f}" fill="none" stroke="#3b342f"'
                f' stroke-width="7" stroke-linecap="round" opacity=".85"/>')
    otk += f'<path d="M{ox+12},{oy+70} l{ow*.3:.0f},{oh*.3:.0f}" stroke="#ffffff" stroke-width="14" opacity=".2"/>'
    otk += '</g>'
    otk += b8_ruchka(ox + 36 + ow * .72 * rost + 22, oy + 244, -34, 250)

    s += SL(Z_PERED, tel + dv + otk + baza._ramka_pp("oba", "#120e0a", .6))
    s += baza.vinetka(.45)
    return s


def vedro_tryapka_i_dva_dnya(t):
    """Комната: ведро с отжатой тряпкой и щётка, на стене загораются два дня.
    Живое: числа загораются, тряпка свешивается, щётка падает и встаёт."""
    p = (t / 3.6) % 1.0
    if p < .30:
        ang = 0.0
    elif p < .52:
        ang = -74 * A.ease((p - .30) / .22)
    elif p < .66:
        ang = -74
    else:
        ang = -74 * (1 - A.ease((p - .66) / .34))

    s = SL(Z_DAL,
           b8_komnata(760, "#6b5846", "#473828")
           + baza.vozduh(760, 420, t, 980, .32)
           + b8_kalendar(170, 130, t, 1120, zapiski=0, goryat=(4, 5), n=7, h_=280))

    s += baza.mebel_hlam(1390, 1020, 520, t, 9)
    # тёплая лампа и полотенце на гвозде: кадр был пустой бурой стеной
    s += SL(Z_DAL,
            baza.lampa(1660, 420, t, .78, True)
            + f'<rect x="300" y="520" width="28" height="18" rx="6" fill="{ZHELEZ}" {o(4)}/>'
            + f'<path d="M258,534 q58,-26 114,0 q18,150 -12,250 q-54,20 -94,-4'
              f' q-28,-98 -8,-246 z" fill="{ob.ALYJ}" {o(6)}/>'
            + f'<path d="M266,660 h100 M266,706 h100" stroke="{ob.ZOLOTO}"'
              f' stroke-width="8" opacity=".85"/>'
            + baza.teplo(1660, 470, 420, 380, .46))

    s += SL(Z_SRED,
            teplo(840, 890, 780, 420, .40)
            + b8_vedro(700, 1000, 1.42, t, False, True)
            + b8_shchetka(1180, 1006, 1.30, ang))

    luzha = (f'<ellipse cx="930" cy="1026" rx="380" ry="50" fill="#9fc4d8" opacity=".30"/>'
             f'<ellipse cx="860" cy="1020" rx="210" ry="28" fill="#dff0fa" opacity=".24"/>')
    s += SL(Z_PERED,
            luzha
            + baza._ramka_pp("levo", "#120e0a", .55))
    s += baza.vinetka(.44)
    return s


def kover_na_chistom_snegu(t):
    """Двор пятиэтажки: большой узорный ковёр узором вниз на снегу, его метут
    вдвоём и поднимают. Живое: веник метёт, ковёр поднимают, остаётся серый след."""
    pod = A.ease(A.seg(t, 2.9, 1.5))            # подъём ковра
    met = A.seg(t, .1, 2.7)
    vx = 560 + 620 * (.5 + .5 * A.w(t, 1.5)) * (1 - pod)

    s = baza.nebo("den", t, zvezdy=False)
    s += baza.oblaka(t, 180, 4, 9, .5, "#f2f6fb", 7.0)
    s += SL(Z_DAL,
            baza._panelka(60, 690, 760, t, 5, True, 4)
            + baza._panelka(1180, 690, 640, t, 5, True, 9)
            + baza._ulica_dal(820, 690, 380, t, True, 5)
            + baza._sneg_lezhit(690, 30))
    s += SL(Z_SRED,
            f'<rect y="700" width="{W}" height="{H-700}" fill="url(#sneg)"/>'
            + f'<path d="M0,760 q480,-34 960,-10 q480,24 960,-14 L1920,{H} L0,{H} Z"'
              f' fill="#ffffff" opacity=".55"/>')

    # серый прямоугольник остаётся на снегу
    sled = (f'<path d="M430,1010 L1490,1010 L1300,742 L620,742 Z" fill="#8fa0b4"'
            f' opacity="{.22+.78*pod:.2f}" stroke="#6f8096" stroke-width="6"/>'
            f'<path d="M470,990 L1450,990 L1290,762 L630,762 Z" fill="#7b8da4"'
            f' opacity="{.16+.58*pod:.2f}"/>')

    # ковёр изнанкой вверх, поднимается за углы
    bahroma = ""
    for i in range(26):
        u = i / 25.0
        bx = 420 + 1080 * u
        bahroma += (f'<path d="M{bx:.0f},1012 l{-4+8*((i%2)):.0f},26" fill="none"'
                    f' stroke="#8d7f63" stroke-width="5" stroke-linecap="round"/>')
    kov = (f'<g transform="translate(0,{-290*pod:.0f}) scale(1,{1-.46*pod:.3f})'
           f' rotate({-4.5*pod:.2f})" transform-origin="960 1010">'
           + b8_kover("b8kv1", 420, 1500, 1012, 614, 1306, 740, t,
                    "#b9a687", "#85715a",
                    "#9c8a66", .9, iznanka=True)
           + bahroma
           + f'<path d="M470,990 L1450,990 L1292,762 L628,762 Z" fill="none"'
             f' stroke="#8d7f63" stroke-width="9" opacity=".7"/>'
           + '</g>')

    # веник метёт по ковру, пока его не подняли
    venik = ""
    if met > .01 and pod < .5:
        venik += f'<g transform="translate({vx:.0f},{900 - 220*pod:.0f}) rotate({-22+10*A.w(t,1.5):.1f})">'
        venik += (f'<rect x="-10" y="-330" width="21" height="330" rx="9"'
                  f' fill="url(#derev)" {o(5)}/>')
        for i in range(11):
            venik += (f'<path d="M{-2+i*2:.0f},-24 q{-46+i*9:.0f},50 {-54+i*11:.0f},96"'
                      f' fill="none" stroke="#c6a152" stroke-width="7" stroke-linecap="round"/>')
        venik += f'<rect x="-30" y="-46" width="62" height="24" rx="8" fill="{ob.ALYJ}" {o(4)}/>'
        venik += '</g>'
        venik += (f'<ellipse cx="{vx:.0f}" cy="{916-220*pod:.0f}" rx="130" ry="26"'
                  f' fill="#ffffff" opacity="{.22*(1-pod):.2f}"/>')

    # отец и сын держат ковёр за углы
    ded = ob.figura(330, 1046, 430, t, col="#2b2430", kant="#cfe0f2", ph=.0)
    syn = ob.figura(1620, 1030, 270, t, col="#32242a", kant="#cfe0f2", ph=.4, krasnoe=True)

    s += SL(Z_SRED, sled + kov + venik + ded + syn)
    s += SL(Z_PERED,
            baza._sneg_lezhit(1004, 44)
            + baza._ramka_pp("oba", "#1a2232", .5))
    s += baza.sneg_letit(t, 46, 5, .72)
    s += baza.vinetka(.40)
    return s


def pylesos_na_kovre(t):
    """Комната: пылесос идёт по узорному ковру и оставляет яркую чистую полосу.
    Живое: щётка идёт, узор яснеет полосой, шнур тянется."""
    u = (t / 3.4) % 1.0
    xb = 300 + 1200 * A.ease(u)

    s = SL(Z_DAL,
           b8_komnata(600, "#64533f", "#3f3326")
           + baza.vozduh(960, 280, t, 980, .28)
           + baza.kvartira_veschi(40, 600, 700, t, 11)
           + b8_kalendar(1060, 130, t, 760, zapiski=0, goryat=(4, 5), n=7, h_=270))

    pol = (f'<rect y="600" width="{W}" height="{H-600}" fill="url(#pol)"/>')
    for i in range(9):
        pol += (f'<line x1="0" y1="{650+i*56}" x2="{W}" y2="{650+i*56}"'
                f' stroke="#4e3220" stroke-width="4" opacity=".45"/>')

    kov_tus = b8_kover("b8kv2", 120, 1820, 1070, 410, 1540, 620, t,
                     "#6d3b35", "#3f1f1e", "#9d8552", .55)
    kov_yar = b8_kover("b8kv3", 120, 1820, 1070, 410, 1540, 620, t,
                     "#b04a3c", "#6b2724", "#f0c766", 1.0)
    polosa = (f'<clipPath id="b8pol"><rect x="80" y="580" width="{max(0,xb-80):.0f}"'
              f' height="520"/></clipPath>'
              f'<g clip-path="url(#b8pol)">{kov_yar}</g>')

    s += SL(Z_SRED, pol + kov_tus + polosa
            + f'<rect x="{xb-14:.0f}" y="600" width="16" height="470" fill="{SVET}" opacity=".24"/>'
            + teplo(xb, 880, 280, 220, .28))

    # шнур тянется от пылесоса к левому краю
    shn = f'M{xb-70:.0f},940'
    for i in range(9):
        shn += f' Q{xb-70-(i+.5)*(xb+120)/9:.0f},{958+26*A.w(t,3.0,i*.2):.0f} {xb-70-(i+1)*(xb+120)/9:.0f},944'
    pyl = f'<path d="{shn}" fill="none" stroke="#2c2a28" stroke-width="10"/>'

    # корпус, шланг, щётка
    bx = xb - 300
    pyl += ten(bx, 1020, 150, 24, .45)
    pyl += (f'<path d="M{bx-140:.0f},1012 q-16,-150 60,-176 q80,-26 160,-2'
            f' q70,26 56,178 z" fill="url(#zhel)" {o(8)}/>')
    pyl += (f'<ellipse cx="{bx-10:.0f}" cy="866" rx="92" ry="34" fill="#5f6a74" {o(5)}/>')
    pyl += (f'<path d="M{bx-120:.0f},930 q110,30 230,-6" fill="none" stroke="#ffffff"'
            f' stroke-width="12" opacity=".2"/>')
    for dx in (-110, 110):
        pyl += (f'<circle cx="{bx+dx:.0f}" cy="1012" r="34" fill="url(#chug)" {o(5)}/>'
                f'<circle cx="{bx+dx:.0f}" cy="1012" r="13" fill="#8a9099"/>')
    pyl += (f'<path d="M{bx+96:.0f},880 Q{bx+240:.0f},700 {xb-40:.0f},880"'
            f' fill="none" stroke="#3a3734" stroke-width="30" stroke-linecap="round"/>')
    pyl += (f'<path d="M{bx+96:.0f},880 Q{bx+240:.0f},700 {xb-40:.0f},880"'
            f' fill="none" stroke="#6a6560" stroke-width="12" stroke-dasharray="10 16"/>')
    pyl += (f'<rect x="{xb-56:.0f}" y="876" width="28" height="90" rx="10"'
            f' fill="url(#zhel)" {o(5)}/>')
    pyl += ten(xb - 42, 1010, 110, 16, .4)
    pyl += (f'<rect x="{xb-140:.0f}" y="952" width="200" height="46" rx="12"'
            f' fill="url(#chug)" {o(6)}/>')
    pyl += (f'<rect x="{xb-128:.0f}" y="992" width="176" height="14" rx="6"'
            f' fill="#6a6560"/>')

    s += SL(Z_PERED, pyl + baza._ramka_pp("levo", "#120e0a", .5))
    s += baza.vinetka(.44)
    return s


def stare_vynosyat_iz_treh_mest(t):
    """Из шкафа коробка, с антресоли связка, из сарая тачка — всё к порогу.
    Живое: коробка выезжает, связка спускается, тачка катится."""
    k1 = A.out(A.seg(t, .25, 1.25))
    k2 = A.ease(A.seg(t, 1.5, 1.45))
    k3 = A.ease(A.seg(t, 2.4, 1.7))

    s = SL(Z_DAL,
           b8_komnata(800, "#5f4e3c", "#3a2f23")
           + baza.vozduh(1500, 420, t, 1000, .34))

    # шкаф слева
    shk = ten(300, 992, 250, 24, .45)
    shk += f'<rect x="60" y="300" width="470" height="690" rx="10" fill="url(#derev)" {o(8)}/>'
    shk += f'<rect x="86" y="326" width="200" height="638" rx="7" fill="{DOSKA2}" {o(5)}/>'
    shk += f'<circle cx="300" cy="650" r="13" fill="url(#zhel)" {o(4)}/>'
    shk += f'<rect x="306" y="326" width="200" height="638" rx="7" fill="#2a2119" opacity=".9"/>'
    shk += teplo(400, 640, 260, 420, .22)
    # коробка выезжает
    shk += (f'<g transform="translate({330 + 230*k1:.0f},{880:.0f})">'
            + ten(0, 96, 180, 24, .45)
            + f'<rect x="-168" y="-158" width="336" height="246" rx="10" fill="#c9a970" {o(8)}/>'
            + f'<path d="M-168,-82 h336" fill="none" stroke="#8d7345" stroke-width="9"/>'
            + f'<path d="M-36,-158 v246" fill="none" stroke="#8d7345" stroke-width="9"/>'
            + f'<path d="M-158,-148 l110,52" stroke="#ffffff" stroke-width="14" opacity=".22"/>'
            + '</g>')

    # антресоль посередине: связка спускается на верёвке
    ant = f'<rect x="620" y="170" width="560" height="150" rx="8" fill="url(#derev)" {o(8)}/>'
    ant += f'<rect x="642" y="190" width="516" height="112" rx="6" fill="#3a2d20" {o(5)}/>'
    ant += teplo(900, 250, 300, 150, .26)
    for i in range(4):
        ant += (f'<rect x="{676+i*118:.0f}" y="206" width="92" height="80" rx="6"'
                f' fill="#6a563c" {o(4)} opacity=".9"/>')
    ant += f'<path d="M900,310 v{130 + 320*k2:.0f}" fill="none" stroke="#b59a63" stroke-width="10"/>'
    sv_y = 440 + 320 * k2
    ant += (f'<g transform="translate(900,{sv_y:.0f}) rotate({3.2*A.w(t,2.6):.2f})">'
            + ten(0, 140, 160, 22, .42)
            + b8_gazety(0, 126, 1.12, t, .2)
            + f'<path d="M-132,-8 h264" fill="none" stroke="#b59a63" stroke-width="11"/>'
            + '</g>')

    # сарай справа: тачка катится
    sar = f'<rect x="1230" y="330" width="560" height="660" rx="10" fill="#3a3027" {o(8)}/>'
    sar += baza.doski(1250, 350, 520, 620, 86, True, "dosk")
    sar += f'<rect x="1250" y="350" width="520" height="620" fill="#140f0c" opacity=".30"/>'
    sar += (f'<rect x="1310" y="430" width="400" height="430" rx="10" fill="#f0c168"'
            f' opacity=".30"/>')
    sar += teplo(1510, 660, 420, 420, .45)
    tx = 1510 - 420 * k3
    sar += (f'<g transform="translate({tx:.0f},910) scale(1.34)">'
            + ten(0, 96, 160, 22, .45)
            + f'<path d="M-150,0 l40,-110 h230 l-26,110 z" fill="url(#zhel)" {o(8)}/>'
            + f'<path d="M-110,-110 h230 l-14,40 h-202 z" fill="#3c454e" {o(5)}/>'
            + f'<path d="M-110,-110 h230" fill="none" stroke="#d2dae2" stroke-width="10" opacity=".65"/>'
            + f'<path d="M-124,-40 h208" fill="none" stroke="#ffffff" stroke-width="8" opacity=".18"/>'
            + f'<path d="M100,-16 l132,74" fill="none" stroke="{CHUGUN}" stroke-width="18" stroke-linecap="round"/>'
            + f'<path d="M-136,-6 l-80,80" fill="none" stroke="{CHUGUN}" stroke-width="16" stroke-linecap="round"/>'
            + f'<circle cx="232" cy="58" r="13" fill="#8a6540" {o(4)}/>'
            + f'<g transform="rotate({-tx*.55:.0f} -94 70)">'
            + f'<circle cx="-94" cy="70" r="56" fill="url(#chug)" {o(6)}/>'
            + f'<circle cx="-94" cy="70" r="18" fill="#8a9099"/>'
            + f'<path d="M-150,70 h112 M-94,14 v112" stroke="#8a9099" stroke-width="7"/></g>'
            + b8_zont(-40, -116, .5, t, True, .5)
            + '</g>')

    s += SL(Z_SRED, shk + ant + sar)

    # куча у порога
    kuch = ""
    if k3 > .55:
        kop = min(1.0, (k3 - .55) / .45)
        kuch += f'<g opacity="{kop:.2f}">'
        kuch += ten(1660, 1020, 300, 30, .5)
        kuch += b8_gazety(1616, 1010, 1.0, t, .6)
        kuch += b8_zont(1782, 1010, .70, t, True, .2)
        kuch += (f'<rect x="1470" y="866" width="260" height="154" rx="8" fill="#c9a970" {o(7)}/>'
                 f'<path d="M1470,924 h260" fill="none" stroke="#8d7345" stroke-width="8"/>')
        kuch += '</g>'
    s += SL(Z_PERED,
            kuch
            + f'<rect y="1016" width="{W}" height="64" fill="{DOSKA2}" {o(6)}/>'
            + baza._ramka_pp("pravo", "#120e0a", .55))
    s += baza.vinetka(.44)
    return s


def tri_nenuzhnye_veschi(t):
    """Крупно три вещи в ряд: чашка без ручки, зонт с торчащей спицей,
    стопка газет. Живое: чашка качается, спица дрожит, уголки шевелятся."""
    s = SL(Z_DAL,
           b8_komnata(700, "#6a5744", "#42342a")
           + baza.vozduh(960, 280, t, 1050, .30)
           + baza.polka(240, 300, 1440)
           + baza.krynka(380, 296, .72) + baza.krynka(1540, 296, .64)
           + ob.mandarin(1380, 268, .66, 0.0, t))

    stol = f'<rect y="846" width="{W}" height="{H-846}" fill="url(#derev)"/>'
    stol += f'<rect y="838" width="{W}" height="24" fill="{DOSKA2}" {o(6)}/>'
    for i in range(4):
        stol += (f'<line x1="0" y1="{900+i*54}" x2="{W}" y2="{900+i*54}"'
                 f' stroke="#5a3b22" stroke-width="4" opacity=".4"/>')
    s += SL(Z_SRED, stol + teplo(960, 830, 1080, 470, .44))

    s += SL(Z_PERED,
            b8_chashka(300, 848, 2.05, t, .0, True)
            + b8_zont(950, 858, 1.78, t, True, .3)
            + b8_gazety(1610, 848, 1.85, t, .5)
            + baza._ramka_pp("oba", "#120e0a", .55))
    s += baza.vinetka(.46)
    return s


def meshok_starya_u_poroga_goda(t):
    """Светящийся проём года: мешок старья в него не пролезает, человек
    ставит мешок и проходит налегке. Живое: мешок застревает, свет льётся."""
    k_pod = A.ease(A.seg(t, .15, 1.35))          # подошли к проёму
    zastr = A.seg(t, 1.5, .85)                   # застрял, толчки
    stavit = A.ease(A.seg(t, 2.45, .85))         # ставит мешок
    uhod = A.ease(A.seg(t, 3.35, 1.5))           # проходит налегке

    tolch = 16 * math.sin(2 * math.pi * t * 3.1) * zastr * (1 - stavit)
    mx = 700 + 340 * k_pod + tolch
    my = 980 + 24 * stavit

    s = SL(Z_DAL,
           f'<rect width="{W}" height="{H}" fill="#191520"/>'
           + b8_grad("b8pri", "#2d2432", "#120e16")
           + f'<rect width="{W}" height="840" fill="url(#b8pri)"/>'
           + baza.doski(0, 0, W, 840, 150, True, "dosk")
           + f'<rect width="{W}" height="840" fill="#0d0a12" opacity=".58"/>'
           + f'<rect y="830" width="{W}" height="{H-830}" fill="url(#pol)" opacity=".8"/>'
           + b8_proyom(1120, 230, 420, 650, t, 1.0))

    s += SL(Z_SRED,
            baza.lampa(330, 420, t, .85, abazhur=False)
            + baza._mebel_hlam(60, 980, 420, t, 5)
            + teplo(1330, 640, 760, 620, .45))

    # мешок и человек
    chel = ob.figura(mx - 310 + 700 * uhod, 1030 - 50 * uhod, 520 - 110 * uhod, t,
                     col="#231a26", kant="#ffd89a", ph=.2,
                     op=1.0 - .30 * uhod, krasnoe=False)
    mesh = b8_meshok(mx, my, 1.02 - .05 * stavit, t, .1, szhat=zastr * (1 - stavit))

    s += SL(Z_PERED,
            mesh + chel
            + f'<path d="M0,1060 h{W}" stroke="{DOSKA2}" stroke-width="22"/>'
            + baza._ramka_pp("levo", "#0c0910", .75))
    s += baza.vinetka(.50)
    return s


def etazh_i_zabor(t):
    """Развилка: слева окно высокого этажа, справа дом за дощатым забором,
    и там и там один листок. Живое: листки подсвечиваются разом, дым, занавеска."""
    gor = .30 + .55 * (0.5 + 0.5 * A.w(t, 2.4))

    vid_l = (f'<rect width="{W}" height="{H}" fill="#f6d79a"/>'
             + teplo(400, 520, 420, 400, .8)
             + baza.siluet(300, 700, 300, "#6a4a28", .55, False, "#ffe6b0")
             + f'<rect x="130" y="300" width="540" height="440" fill="{SVET}" opacity=".3"/>')

    s = baza.nebo("sumer", t)
    s += baza.oblaka(t, 210, 4, 7, .45, "#d8e0ee", 8.0)
    s += SL(Z_DAL,
            baza._panelka(-60, 1080, 1000, t, 7, True, 4)
            + baza._ulica_dal(1000, 800, 920, t, True, 11))

    # ── левая половина: окно высокого этажа
    lev = f'<rect x="0" y="0" width="930" height="{H}" fill="#3c4458" opacity=".55"/>'
    lev += baza.kladka(0, 180, 930, 900, 96, "url(#beton)")
    lev += f'<rect x="0" y="180" width="930" height="900" fill="#2c3346" opacity=".5"/>'
    lev += baza.okno_izby(130, 300, 540, 440, t, vid=vid_l, moroz=.12, svet=True)
    lev += baza.zanaveska(170, 318, 400, 150, "#c8d6e6", t, 1)
    lev += baza.zanaveska(632, 318, 400, 150, "#c8d6e6", t, -1)
    lev += teplo(400, 520, 460, 400, .50)
    lev += (f'<rect x="130" y="760" width="540" height="40" rx="8" fill="url(#beton)" {o(6)}/>'
            f'<path d="M130,760 q136,-22 270,-8 q136,14 270,-10 l0,20 h-540 z"'
            f' fill="url(#sneg)" {o(4)}/>')
    lev += b8_listok(716, 440, 180, 224, t, rost=(1, 1, 1), zacherk=(1, 1, 1),
                   galka=1.0, ang=-4.0, svet=gor)

    # ── правая половина: дом за дощатым забором
    prav = baza.izba_snaruzhi(1130, 820, 700, t, True, True, 3)
    prav += (f'<path d="M990,830 q230,-26 460,-10 q230,16 470,-12 L1920,{H} L990,{H} Z"'
             f' fill="url(#sneg)" {o(5)}/>')
    prav += baza.doski(990, 700, 930, 380, 92, True, "dosk")
    prav += f'<rect x="990" y="700" width="930" height="380" fill="#2a2016" opacity=".30"/>'
    for yy in (744, 1010):
        prav += f'<rect x="990" y="{yy}" width="930" height="24" fill="{DOSKA2}" {o(5)}/>'
    prav += (f'<path d="M990,700 q232,-20 464,-6 q232,14 466,-8 l0,18 h-930 z"'
             f' fill="url(#sneg)" {o(4)}/>')
    prav += b8_listok(1600, 788, 180, 224, t, rost=(1, 1, 1), zacherk=(1, 1, 1),
                    galka=1.0, ang=3.0, svet=gor)

    s += SL(Z_SRED, lev + prav)

    razdel = (f'<rect x="930" y="0" width="60" height="{H}" fill="#0f131c" opacity=".88"/>'
              f'<rect x="946" y="0" width="10" height="{H}" fill="{ob.ZOLOTO}" opacity=".30"/>')
    s += SL(Z_PERED,
            razdel
            + f'<path d="M-20,1052 q240,-24 480,-8 q240,16 480,-10 q240,-20 480,-4'
              f' q240,14 500,-12 L1940,{H} L-20,{H} Z" fill="url(#sneg)" {o(5)}/>'
            + baza._ramka_pp("oba", "#101624", .50))
    s += baza.sneg_letit(t, 52, 7, .78)
    s += baza.vinetka(.42)
    return s


def god_kakim_ego_hotyat_prozhit(t):
    """Вечер, золотой свет: семья за столом, вид от торца. Двое обнимаются,
    блюдо встаёт на стол, под тарелкой блестит монета, листок зачёркнут."""
    obn = .5 + .5 * A.w(t, 3.6)                       # двое обнимаются
    bl_u = A.out(A.seg(t, 1.3, 1.25))                 # блюдо опускается
    by = 330 + (700 - 330) * bl_u

    vid = baza._nebo("noch", t) + baza._sneg_letit(t, 22, 6, .6)

    s = SL(Z_DAL,
           b8_komnata(640, "#6b4f3a", "#3f2c1e")
           + baza.okno_izby(70, 190, 330, 290, t, vid=vid, moroz=.18)
           + ob.elka(1700, 650, 520, t, True, True, 4, True)
           + ob.girlyanda(120, 150, 1820, 170, t, 16, 110, .2)
           + baza.lampa(960, 330, t, 1.25, abazhur=True)
           + baza.vozduh(960, 360, t, 1050, .26))

    # стол от торца: трапеция
    stol = (f'<path d="M230,1050 L1690,1050 L1180,560 L740,560 Z" fill="url(#rush)" {o(7)}/>')
    stol += (f'<path d="M258,1030 L1662,1030 L1168,578 L752,578 Z" fill="#f6ecd2" opacity=".55"/>')
    stol += (f'<path d="M230,1050 L1690,1050 L1180,560 L740,560 Z" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".45"/>')
    stol += ten(960, 1062, 740, 30, .5)

    # блюда и свечи по столу
    pred = ""
    for i, (px, py, sc) in enumerate(((560, 950, 1.0), (1360, 950, 1.0),
                                      (780, 760, .72), (1140, 760, .72),
                                      (960, 660, .58))):
        pred += b8_tarelka(px, py, 96 * sc, t, 0.0, False)
    pred += baza.svecha(960, 820, t, .0, 1.1)
    pred += ob.bokal(700, 930, t, .9, .1)
    pred += ob.bokal(1230, 930, t, .9, .5)
    pred += baza.karavay(960, 900, .8, True)
    pred += ob.mandarin(840, 870, .78, 0.0, t)
    pred += ob.mandarin(1090, 876, .72, .3, t)

    # блюдо встаёт на стол
    pred += b8_blyudo_pelmeni(960, by, .9, t, .0, par_on=bl_u > .9)

    # семья: по левому и правому борту, в красном
    lyudi = ""
    for i, (px, py, hh, kr) in enumerate(((300, 1010, 330, True), (520, 880, 280, False),
                                          (690, 770, 236, True))):
        lyudi += ob.figura(px, py, hh, t, col="#2b2230", kant="#ffd89a",
                           platok=(i == 1), ph=i * .21, krasnoe=kr)
    for i, (px, py, hh, kr) in enumerate(((1620, 1010, 330, False), (1400, 880, 280, True),
                                          (1230, 770, 236, False))):
        lyudi += ob.figura(px, py, hh, t, col="#2a2630", kant="#ffd89a",
                           platok=(i == 2), ph=.1 + i * .23, krasnoe=kr)
    # двое у дальнего торца обнимаются
    lyudi += ob.figura(880 + 22 * obn, 650, 210, t, col="#2e2330", kant="#ffd89a",
                       platok=True, ph=.5, krasnoe=True)
    lyudi += ob.figura(1040 - 22 * obn, 650, 210, t, col="#262c38", kant="#ffd89a",
                       ph=.8, krasnoe=False)

    s += SL(Z_SRED, stol + lyudi + pred)

    # ближний край: тарелка с монетой и зачёркнутый листок
    s += SL(Z_PERED,
            b8_tarelka(540, 1000, 215, t, .26 + .08 * A.w(t, 3.0), moneta=True)
            + b8_listok(1250, 880, 220, 264, t, rost=(1, 1, 1), zacherk=(1, 1, 1),
                      galka=1.0, ang=5.0, svet=.34)
            + baza._ramka_pp("oba", "#1a1008", .50))
    s += baza.vinetka(.40)
    return s


def tarelka_i_karman_s_sekretom(t):
    """Крупно край стола: край тарелки сам приподнимается и из-под него идёт
    свет, из кармашка фартука — тоже. Живое: подъём, свет, скатерть."""
    pod = .18 + .82 * (0.5 + 0.5 * A.w(t, 4.2))
    kar = .58 + .42 * (0.5 + 0.5 * A.w(t, 3.1, .35))
    kol = 9 * A.w(t, 5.0)

    s = SL(Z_DAL,
           b8_komnata(520, "#60452f", "#35241a")
           + ob.elka(1700, 560, 380, t, True, True, 7, True)
           + ob.girlyanda(60, 120, 1860, 140, t, 14, 90, .4)
           + baza.lampa(620, 250, t, 1.0, abazhur=True)
           + baza.vozduh(760, 330, t, 1000, .32)
           + f'<rect width="{W}" height="{H}" fill="#120c08" opacity=".22"/>')

    # край стола крупно
    skat = (f'<path d="M-40,700 h2000 v{H-640} h-2000 z" fill="url(#rush)" {o(7)}/>')
    skat += (f'<path d="M-40,700 q480,{30+kol:.0f} 980,4 q480,{-26+kol:.0f} 1020,12"'
             f' fill="none" stroke="{DOSKA2}" stroke-width="11" opacity=".55"/>')
    for i in range(7):
        skat += (f'<path d="M{-40+i*300:.0f},724 q{22+kol*.6:.0f},180 {-8:.0f},380"'
                 f' fill="none" stroke="#cdb98d" stroke-width="11" opacity=".6"/>')
    skat += (f'<path d="M-40,784 q480,{34+kol:.0f} 980,6 q480,{-30+kol:.0f} 1020,14"'
             f' fill="none" stroke="{ob.ALYJ}" stroke-width="14" opacity=".65"/>')
    skat += (f'<path d="M-40,700 q480,{30+kol:.0f} 980,4 q480,{-26+kol:.0f} 1020,12 v-60 h-2000 z"'
             f' fill="#000000" opacity=".16"/>')
    s += SL(Z_SRED, skat + teplo(760, 860, 1000, 440, .32))

    # фартук с кармашком справа: складки и сноп света из кармана
    fart = f'<g transform="translate(1440,400)">'
    fart += ten(60, 660, 260, 30, .5)
    fart += (f'<path d="M-200,0 q200,-56 400,0 l46,640 q-246,54 -492,0 z"'
             f' fill="{ob.ALYJ}" {o(9)}/>')
    for i in range(5):
        fart += (f'<path d="M{-150+i*76:.0f},30 q{14+kol*.4:.0f},300 {4:.0f},604"'
                 f' fill="none" stroke="{ob.ALYJ2}" stroke-width="10" opacity=".55"/>')
    fart += (f'<path d="M-182,34 q182,-48 364,0" fill="none" stroke="{ob.ZOLOTO}"'
             f' stroke-width="11" opacity=".85"/>')
    fart += (f'<path d="M-160,60 q90,-30 160,-14" fill="none" stroke="#ffffff"'
             f' stroke-width="14" opacity=".16"/>')
    fart += teplo(0, 300, 360, 320, .40 * kar)
    fart += (f'<path d="M-150,228 h300 v150 q0,90 -150,86 q-150,4 -150,-86 z"'
             f' fill="{ob.ALYJ2}" {o(8)}/>')
    fart += (f'<path d="M-150,228 h300 v150 q0,90 -150,86 q-150,4 -150,-86 z"'
             f' fill="{SVET}" opacity="{.26*kar:.2f}"/>')
    fart += (f'<path d="M-132,250 h264 v132 q0,74 -132,70 q-132,4 -132,-70 z"'
             f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="5"'
             f' stroke-dasharray="15 11" opacity=".8"/>')
    fart += (f'<path d="M-158,214 h316 v34 q-158,18 -316,0 z" fill="{ob.ALYJ}" {o(6)}/>')
    # сноп света наружу из кармана
    fart += (f'<path d="M-110,234 L{-190-60*kar:.0f},{70-80*kar:.0f}'
             f' L{160+70*kar:.0f},{50-90*kar:.0f} L110,234 Z" fill="{SVET}"'
             f' opacity="{.17*kar:.2f}"/>')
    fart += (f'<ellipse cx="0" cy="234" rx="{168*kar:.0f}" ry="{54*kar:.0f}" fill="#fff6d2"'
             f' opacity="{.80*kar:.2f}"/>')
    fart += (f'<ellipse cx="0" cy="232" rx="{104*kar:.0f}" ry="{30*kar:.0f}" fill="#ffffff"'
             f' opacity="{.72*kar:.2f}"/>')
    fart += (f'<path d="M-138,244 h276" fill="none" stroke="{ob.ZOLOTO}" stroke-width="10"'
             f' opacity=".9"/>')
    fart += '</g>'

    s += SL(Z_PERED,
            b8_tarelka(560, 830, 360, t, pod, moneta=False)
            + fart
            + baza._ramka_pp("levo", "#140d08", .45))
    s += baza.vinetka(.46)
    return s


def svoi_za_novogodnim_stolom(t):
    """Стол под абажуром со стороны хозяйки: красная лента в волосах, карман
    вздрагивает, ваза мандаринов, внук забирается на стул."""
    lenta = 8 * A.w(t, 2.9)
    vnuk = A.over(A.seg(t, 2.1, 1.35))
    hlop = max(0.0, math.sin(2 * math.pi * (t / 2.3))) ** 6

    vid = baza._nebo("noch", t) + baza._sneg_letit(t, 20, 4, .6)

    s = SL(Z_DAL,
           b8_komnata(600, "#664a36", "#3a291c")
           + baza.okno_izby(90, 170, 320, 280, t, vid=vid, moroz=.5)
           + ob.elka(1690, 640, 480, t, True, True, 5, True)
           + ob.girlyanda(80, 130, 1840, 150, t, 15, 100, .15)
           + baza.vozduh(960, 330, t, 1020, .26))

    # круглый стол
    stol = ten(960, 952, 640, 44, .5)
    stol += (f'<ellipse cx="960" cy="760" rx="600" ry="226" fill="url(#rush)" {o(8)}/>')
    stol += (f'<ellipse cx="960" cy="748" rx="540" ry="194" fill="#f6ecd2" opacity=".5"/>')
    stol += (f'<ellipse cx="960" cy="760" rx="600" ry="226" fill="none" stroke="{ob.ALYJ}"'
             f' stroke-width="8" opacity=".5"/>')
    stol += (f'<path d="M360,760 q600,286 1200,0 v96 q-600,286 -1200,0 z"'
             f' fill="url(#rush)" {o(6)}/>')

    # ваза мандаринов в середине
    vaza = ten(960, 742, 170, 22, .45)
    vaza += (f'<path d="M842,690 q118,78 236,0 q-14,58 -118,58 q-104,0 -118,-58 z"'
             f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    vaza += f'<path d="M912,748 h96 v18 h-96 z" fill="url(#zhel)" {o(5)}/>'
    for i, (dx, dy, sc) in enumerate(((-66, 672, .82), (0, 656, .9), (62, 672, .82),
                                      (-32, 630, .74), (34, 628, .74))):
        vaza += ob.mandarin(960 + dx, dy, sc, 0.0, t)
        bl = .35 + .65 * abs(A.w(t, 2.1 + i * .4, i * .2))
        vaza += (f'<ellipse cx="{960+dx-13:.0f}" cy="{dy-14:.0f}" rx="{13*sc:.0f}"'
                 f' ry="{9*sc:.0f}" fill="#fff3d2" opacity="{bl*.8:.2f}"/>')

    # родные вокруг стола + стул внука
    lyudi = b8_figury_vokrug(960, 680, 540, 196, t, 5, 268, 3, krasnyh=(1, 3))
    stul = b8_stul(1510, 920, 1.08, -3.0)
    if vnuk > .02:
        lyudi += ob.figura(1510, 920 - 126 * vnuk, 168 + 26 * vnuk, t,
                           col="#2f2330", kant="#ffd89a", ph=.6, krasnoe=True)

    s += SL(Z_SRED, stol + stul + lyudi + vaza
            + baza.svecha(700, 736, t, .2, 1.0)
            + baza.svecha(1230, 738, t, .6, 1.0)
            + ob.bokal(820, 782, t, .85, .2)
            + ob.bokal(1110, 784, t, .85, .7)
            + baza.lampa(960, 300, t, 1.35, abazhur=True))

    # хозяйка со спины крупно, ближний план
    hgy = 1560 - 940 * .77                     # макушка силуэта хозяйки
    hoz = ob.figura(900, 1560, 940, t, col="#2a1f28", kant="#ffd89a", ph=.0)
    # красная лента в волосах: бант НА затылке, концы вниз по центру
    hoz += (f'<g transform="rotate({lenta:.2f} 900 {hgy+40:.0f})">'
            f'<path d="M784,{hgy+36:.0f} q116,-74 232,0" fill="none" stroke="{ob.ALYJ}"'
            f' stroke-width="26" stroke-linecap="round"/>'
            f'<path d="M862,{hgy+30:.0f} q38,-40 76,0 q-38,34 -76,0 z" fill="{ob.ALYJ}" {o(6)}/>'
            f'<circle cx="900" cy="{hgy+32:.0f}" r="15" fill="{ob.ZOLOTO}" {o(4)}/>'
            f'<path d="M914,{hgy+40:.0f} q34,48 16,108 q-26,-18 -30,-70 z"'
            f' fill="{ob.ALYJ}" {o(5)}/>'
            f'<path d="M886,{hgy+40:.0f} q-34,48 -16,108 q26,-18 30,-70 z"'
            f' fill="{ob.ALYJ2}" {o(5)}/></g>')
    # карман вздрагивает — руки не рисуем, работает сам карман
    ksc = 1.0 + .09 * hlop
    hoz += (f'<g transform="translate(978,1046) rotate(-5) scale({ksc:.3f})">'
            f'<rect x="-96" y="-84" width="192" height="168" rx="14" fill="{ob.ALYJ2}" {o(7)}/>'
            f'<path d="M-86,-64 h172" fill="none" stroke="{ob.ZOLOTO}" stroke-width="10" opacity=".85"/>'
            f'<path d="M-70,-40 q70,-24 140,-8" fill="none" stroke="#ffffff"'
            f' stroke-width="10" opacity=".14"/>'
            f'<ellipse cx="0" cy="-74" rx="{94*hlop:.0f}" ry="{30*hlop:.0f}" fill="{SVET}"'
            f' opacity="{.50*hlop:.2f}"/></g>')

    s += SL(Z_PERED, hoz + baza._ramka_pp("oba", "#180f08", .5))
    s += baza.vinetka(.42)
    return s


def blyudo_pelmeney_idet_po_krugu(t):
    """Блюдо пельменей идёт по кругу вокруг стола и не пустеет, над столом
    плывёт оранжевая струйка запаха. Живое: круг, пар, струйка."""
    a = -math.pi / 2 + 2 * math.pi * ((t / 6.4) % 1.0)
    bx = 960 + math.cos(a) * 380
    by = 762 + math.sin(a) * 132
    bs = .80 + .30 * (0.5 + 0.5 * math.sin(a))

    s = SL(Z_DAL,
           b8_komnata(600, "#6a4c35", "#3a281b")
           + ob.elka(190, 640, 460, t, True, True, 9, True)
           + ob.girlyanda(70, 130, 1850, 150, t, 15, 96, .55)
           + baza.lampa(960, 290, t, 1.3, abazhur=True)
           + baza.vozduh(960, 350, t, 1020, .26))

    stol = ten(960, 960, 660, 44, .5)
    stol += f'<ellipse cx="960" cy="770" rx="620" ry="236" fill="url(#rush)" {o(8)}/>'
    stol += f'<ellipse cx="960" cy="756" rx="556" ry="202" fill="#f6ecd2" opacity=".5"/>'
    stol += (f'<ellipse cx="960" cy="770" rx="620" ry="236" fill="none" stroke="{ob.ALYJ}"'
             f' stroke-width="8" opacity=".5"/>')
    stol += (f'<path d="M340,770 q620,300 1240,0 v100 q-620,300 -1240,0 z"'
             f' fill="url(#rush)" {o(6)}/>')

    # тарелки по кругу — каждый себе положил
    tar = ""
    for i in range(7):
        aa = -math.pi / 2 + 2 * math.pi * (i / 7.0) + .22
        tx = 960 + math.cos(aa) * 430
        ty = 752 + math.sin(aa) * 148
        sc = .66 + .30 * (0.5 + 0.5 * math.sin(aa))
        tar += b8_tarelka(tx, ty, 108 * sc, t, 0.0, False)
        for k in range(3):
            tar += (f'<path d="M{tx-34*sc+k*34*sc:.0f},{ty-6*sc:.0f}'
                    f' q{16*sc:.0f},{-20*sc:.0f} {32*sc:.0f},0'
                    f' q{-16*sc:.0f},{10*sc:.0f} {-32*sc:.0f},0 z"'
                    f' fill="#f2e6cc" {o(3)}/>')

    lyudi = b8_figury_vokrug(960, 700, 580, 204, t, 6, 268, 8, krasnyh=(0, 4))

    s += SL(Z_SRED, stol + lyudi + tar
            + baza.svecha(660, 716, t, .3, 1.0)
            + baza.svecha(1280, 718, t, .8, 1.0))

    s += SL(Z_PERED,
            b8_blyudo_pelmeni(bx, by, bs, t, .0, True)
            + teplo(bx, by - 40 * bs, 300 * bs, 230 * bs, .40)
            + b8_struyka(bx, by - 70 * bs, t, 240, .0, ob.MANDA, .55)
            + b8_struyka(bx + 70 * bs, by - 56 * bs, t, 180, .45, SVET, .38)
            + baza._ramka_pp("oba", "#1a1008", .5))
    s += baza.vinetka(.42)
    return s


def tri_sdelannyh_dela(t):
    """Три медальона: стопка белья со скатертью, зачёркнутый листок с галочкой,
    пустое ведро вверх дном у двери. Живое: загораются по одному, галочка, кот."""
    gor = [A.ease(A.seg(t, .25 + i * .95, .7)) for i in range(3)]
    gal = A.ease(A.seg(t, 2.1, .9))
    kot_u = A.over(A.seg(t, 3.0, .85))

    vid = (baza._nebo("rassv", t, zvezdy=False)
           + baza._oblaka(t, 230, 3, 6, .5, "#f0ead8", 6.0))

    s = SL(Z_DAL,
           b8_komnata(760, "#6d5742", "#43331f")
           + baza.polka(1150, 236, 660)
           + baza.krynka(1270, 232, .64)
           + ob.mandarin(1470, 206, .6, 0.0, t)
           + baza.krynka(1700, 232, .58)
           + teplo(1680, 260, 520, 400, .40)
           + baza.vozduh(760, 400, t, 980, .28)
           + ob.girlyanda(60, 110, 1860, 130, t, 14, 86, .3))

    # ── нутро медальонов: рисуется вокруг центра своего круга
    # 1: стопка белья со скатертью
    n1 = teplo(330, 600, 260, 220, .40)
    for i in range(5):
        yy = 700 - i * 40
        wdt = 270 - i * 12
        n1 += (f'<rect x="{330-wdt/2:.0f}" y="{yy-38:.0f}" width="{wdt:.0f}" height="38"'
               f' rx="8" fill="{"#f3ecdc" if i%2 else "#e2d8c2"}" {o(5)}/>')
        n1 += (f'<path d="M{330-wdt/2+14:.0f},{yy-20:.0f} h{wdt-28:.0f}" fill="none"'
               f' stroke="#c7b997" stroke-width="5" opacity=".8"/>')
    n1 += f'<path d="M216,504 h228 l-20,58 h-188 z" fill="url(#rush)" {o(6)}/>'
    n1 += f'<path d="M232,532 h196" fill="none" stroke="{ob.ALYJ}" stroke-width="8" opacity=".85"/>'
    n1 += ten(330, 716, 150, 18, .4)

    # 2: зачёркнутый листок с галочкой
    n2 = teplo(960, 580, 250, 230, .35)
    n2 += b8_listok(850, 420, 230, 288, t, rost=(1, 1, 1), zacherk=(1, 1, 1),
                  galka=gal, ang=-4.0, svet=.0)

    # 3: пустое ведро вверх дном у двери, за окном ещё светло
    n3 = (f'<rect x="1398" y="400" width="200" height="330" rx="8" fill="url(#derev)" {o(7)}/>')
    n3 += (f'<rect x="1420" y="420" width="158" height="290" rx="6" fill="{DOSKA2}" {o(5)}/>')
    n3 += f'<circle cx="1562" cy="586" r="12" fill="url(#zhel)" {o(4)}/>'
    n3 += (f'<rect x="1618" y="430" width="170" height="200" rx="8" fill="#d6e8f4"'
           f' opacity=".9" {o(6)}/>')
    n3 += (f'<path d="M1703,430 v200 M1618,530 h170" stroke="url(#derev)" stroke-width="12"/>')
    n3 += teplo(1703, 530, 210, 190, .50)
    n3 += b8_vedro(1672, 722, .66, t, True, False)
    if kot_u > .02:
        n3 += baza.kot(1672, 722 - 106 - 34 * kot_u, t, .54 * kot_u, "#3b3430", False)

    # Три равных круга в ряд читались схемой. Подвесы на гвоздях, разные
    # размеры и высоты — это ВИСЯЩИЕ медальоны, а не выложенные кружки.
    podves = ""
    for mx_, my_, mr_ in ((330, 572, 244), (960, 548, 258), (1590, 580, 238)):
        podves += (f'<circle cx="{mx_}" cy="{my_-mr_-96}" r="11" fill="{ZHELEZ}" {o(4)}/>')
        podves += (f'<path d="M{mx_},{my_-mr_-92} l{-26},{86} m{26},{-86} l{26},{86}"'
                   f' fill="none" stroke="{MED}" stroke-width="9" opacity=".9"/>')
    s += SL(Z_SRED,
            podves
            + b8_medalon(330, 572, 244, t, gor[0], n1)
            + b8_medalon(960, 548, 258, t, gor[1], n2)
            + b8_medalon(1590, 580, 238, t, gor[2], n3))

    s += SL(Z_PERED,
            baza.polka(150, 906, 1340)
            + ob.mandarin(300, 896, .86, 0.0, t)
            + ob.mandarin(392, 900, .72, .3, t)
            + baza.krynka(640, 898, .78)
            + baza.karavay(1060, 900, .72, True)
            + baza.krynka(1380, 898, .7)
            + ob.elka(1874, 1128, 290, t, True, False, 3, True)
            + baza._ramka_pp("levo", "#140e08", .45))
    s += baza.vinetka(.42)
    return s
