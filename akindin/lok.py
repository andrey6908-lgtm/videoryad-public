# -*- coding: utf-8 -*-
"""107 декораций ролика «15 ноября — Акиндин и Пигасий».

Каждая — функция времени f(t) -> svg. Все нарисованы ЗАНОВО под этот текст
(R-0019): ни один кадр не взят у «13 ноября» и «14 ноября».
Где в плане стоит окно вставки, главное живёт в ЛЕВОЙ полосе 0-830 (R-0007).
В каждой декорации минимум три живых элемента (R-0006).
"""
import math, random
from baza import *
from baza import (_nebo, _oblaka, _tuman, _ulica_dal, _panelka, _sneg_lezhit,
                  _sneg_letit, _utvar_izby, _utvar_pekarni, _kvartira_veschi,
                  _mebel_hlam, _ramka_pp, _vinetka)
import anim as A

OKNO = (860, 300, 980, 551)          # неподвижный контейнер вставки
DEN, MESYAC = "15", "НОЯБРЯ"


# ═══════════════ СКВОЗНЫЕ ОБРАЗЫ ЭТОГО РОЛИКА ═══════════════
# Нить шёпота — главный образ дня: чужое слово, вынесенное за порог. Тянется
# из кадра в кадр (планы 3, 4, 15, 23), поэтому вынесена кирпичиком.
def nit_shepota(pts, t, op=.9, col="#ffe9a8", sh=5.0, faza=0.0):
    """Светящаяся нить по точкам, с бегущим по ней блеском."""
    d = "M%.0f,%.0f" % pts[0]
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        mx = (x0 + x1) / 2 + 26 * A.w(t, .55, i * .4 + faza)
        my = (y0 + y1) / 2 - 22 * A.w(t, .7, i * .6 + faza)
        d += " Q%.0f,%.0f %.0f,%.0f" % (mx, my, x1, y1)
    s = (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sh*2.6:.1f}"'
         f' opacity="{op*.18:.2f}" stroke-linecap="round"/>'
         f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sh:.1f}"'
         f' opacity="{op:.2f}" stroke-linecap="round"/>')
    # блеск бежит по нити
    k = A.seg(t, 0, 2.6)
    i = min(len(pts) - 2, int(k * (len(pts) - 1)))
    f = k * (len(pts) - 1) - i
    bx = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f
    by = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
    s += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{sh*2.2:.0f}" fill="#fff6d8" opacity=".5"/>'
    return s


def ogonek_grudi(x, y, t, s_=1.0, ph=0.0, rost=0.0):
    """Тёплый огонёк в груди силуэта: дышит, при rost>0 разгорается."""
    r = (16 + 10 * rost) * s_ * (1 + .12 * A.w(t, 1.3, ph))
    return (f'<circle cx="{x}" cy="{y}" r="{r*3.4:.0f}" fill="url(#teplo)" opacity="{.5+.3*rost:.2f}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r:.0f}" fill="{SVET}" opacity=".95"/>'
            f'<circle cx="{x}" cy="{y-r*.3:.0f}" r="{r*.45:.0f}" fill="#fffdf2" opacity=".9"/>')


def figura(x, y, h_, t, col="#1b1822", kant="#ffd08a", platok=False, ph=.0,
           profil=False, op=1.0, platok_op=.5):
    """Человек со спины или в профиль. Всегда с КАНТОМ: тёмная фигура без
    канта сливается с тёмным фоном — поймано на первом же листе 12.11."""
    dy = 3.0 * A.w(t, .55, ph)
    s = f'<g transform="translate(0,{dy:.1f})" opacity="{op:.2f}">'
    s += siluet(x, y, h_, col, 1.0, False, kant)
    if platok:                     # платок приглушён: ярко-красный бьёт в глаза
        hh = h_ * .145
        cy = y - h_ * .84
        s += (f'<path d="M{x-hh*1.12:.0f},{cy-hh*.06:.0f} a{hh*1.12:.0f},{hh*1.12:.0f} 0 0 1 {hh*2.24:.0f},0'
              f' q{-hh*.2:.0f},{hh*2.1:.0f} {-hh*1.12:.0f},{hh*2.3:.0f}'
              f' q{-hh*.9:.0f},{-hh*.2:.0f} {-hh*1.12:.0f},{-hh*2.3:.0f} Z"'
              f' fill="#8f3a38" opacity="{platok_op:.2f}"/>')
    if profil:                     # нос, подбородок и бровь — профиль читается
        hh = h_ * .145
        cy = y - h_ * .84
        s += (f'<path d="M{x+hh*.86:.0f},{cy-hh*.1:.0f} q{hh*.5:.0f},{hh*.28:.0f} {hh*.06:.0f},{hh*.5:.0f}'
              f' q{-hh*.2:.0f},{hh*.16:.0f} {hh*.16:.0f},{hh*.3:.0f}" fill="none"'
              f' stroke="{kant}" stroke-width="5" opacity=".8" stroke-linecap="round"/>')
    return s + "</g>"


def barhany(t, n=4, y0=640, col1="#2d3657", col2="#1d2440"):
    """Дюны: округлый гребень, освещённый бок и теневой склон."""
    s = ""
    for i in range(n):
        y = y0 + i * 96
        rnd = random.Random(140 + i)
        d = f"M-60,{y+120}"
        x = -60
        while x < W + 120:
            w_ = rnd.randint(380, 620)
            h = rnd.randint(60, 130) - i * 8
            d += f" q{w_*.35:.0f},{-h} {w_*.6:.0f},{-h*.5:.0f} q{w_*.3:.0f},{h*.5:.0f} {w_*.4:.0f},{h*.5:.0f}"
            x += w_
        d += f" L{W+120},{H+40} H-60 Z"
        c = col1 if i % 2 else col2
        s += SL(Z_DAL - i * 70, f'<path d="{d}" fill="{c}" {o(5)}/>')
        # освещённый гребень и теневой склон
        s += SL(Z_DAL - i * 70, f'<path d="{d}" fill="#9fb6d8" opacity="{.16-.03*i:.2f}"'
                                f' transform="translate(-16,-10)"/>')
        s += SL(Z_DAL - i * 70, f'<path d="{d}" fill="#0b1022" opacity="{.20-.03*i:.2f}"'
                                f' transform="translate(26,14)"/>')
    for i in range(14):
        rnd = random.Random(90 + i)
        x = rnd.randint(0, W)
        ph = rnd.random()
        k = A.seg(t, ph * 2.4, 2.4)
        s += (f'<ellipse cx="{x+80*k:.0f}" cy="{y0-20+rnd.randint(-30,40)}" rx="30" ry="3"'
              f' fill="#cdd8ea" opacity="{.22*(1-k):.2f}"/>')
    return s


def dvorec_stena(x, y, w_, h_, t, arok=4, svet=True):
    """Белая дворцовая стена с арками: песчаник, тёплые проёмы."""
    s = (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="8"'
         f' fill="#e2d2b4" {o(8)}/>'
         f'<rect x="{x}" y="{y}" width="{w_}" height="{h_*.18:.0f}" fill="#f0e3c8" opacity=".6"/>')
    sh = w_ / arok
    for i in range(arok):
        ax = x + sh * i + sh * .18
        aw = sh * .64
        ah = h_ * .62
        ay = y + h_ - ah
        s += (f'<path d="M{ax:.0f},{ay+ah:.0f} V{ay+aw/2:.0f} a{aw/2:.0f},{aw/2:.0f} 0 0 1 {aw:.0f},0'
              f' V{ay+ah:.0f} Z" fill="#2a2a3c" {o(6)}/>')
        if svet:
            s += (f'<path d="M{ax+10:.0f},{ay+ah:.0f} V{ay+aw/2:.0f} a{aw/2-10:.0f},{aw/2-10:.0f} 0 0 1'
                  f' {aw-20:.0f},0 V{ay+ah:.0f} Z" fill="{SVET}"'
                  f' opacity="{.16+.05*A.w(t,.5,i*.7):.2f}"/>')
    s += f'<rect x="{x-8}" y="{y-16}" width="{w_+16}" height="22" rx="6" fill="#efe2c6" {o(7)}/>'
    return s


def palma(x, base, t, s_=1.0, ph=0.0, col="#2f4a33"):
    """Пальма: ствол кольцами, веер листьев качается."""
    h = 260 * s_
    s = ten(x, base + 8, 60 * s_, 12 * s_, .45)
    s += (f'<path d="M{x-14*s_:.0f},{base} q{8*s_:.0f},{-h/2:.0f} {2*s_:.0f},{-h:.0f}'
          f' l{24*s_:.0f},0 q{6*s_:.0f},{h/2:.0f} {12*s_:.0f},{h:.0f} Z"'
          f' fill="url(#derev)" {o(6)}/>')
    for i in range(6):
        kach = 6 * A.w(t, .5, ph + i * .35)
        a = -150 + i * 40 + kach
        s += (f'<path d="M{x:.0f},{base-h:.0f} q{90*s_*math.cos(math.radians(a)):.0f},'
              f'{70*s_*math.sin(math.radians(a))-30*s_:.0f}'
              f' {170*s_*math.cos(math.radians(a)):.0f},{120*s_*math.sin(math.radians(a)):.0f}'
              f' q{-60*s_*math.cos(math.radians(a)):.0f},{-20*s_:.0f}'
              f' {-170*s_*math.cos(math.radians(a)):.0f},{-120*s_*math.sin(math.radians(a))+18*s_:.0f} Z"'
              f' fill="{col}" {o(5)}/>')
    return s


def ten_korony(x, y, t, s_=1.0, naklon=0.0):
    """Огромная тень трона с короной: ложится на стену ОТ ПОЛА и кверху
    расширяется, как настоящая тень от низкого огня."""
    nk = naklon * 3.0 * A.ease(A.seg(t, .6, 2.2))
    low = H + 40                                   # тень стоит на полу
    top = y + 40 * s_
    wb, wt = 150 * s_, 250 * s_                    # у пола уже, вверху шире
    s = f'<g transform="rotate({nk:.2f} {x} {low})" opacity=".8">'
    s += (f'<path d="M{x-wb:.0f},{low} L{x-wt:.0f},{top+120*s_:.0f}'
          f' q{wt:.0f},{-80*s_:.0f} {wt*2:.0f},0 L{x+wb:.0f},{low} Z" fill="#0b0a12"/>')
    for i in range(5):                             # зубцы короны
        zx = x - wt * .78 + i * wt * .39
        s += (f'<path d="M{zx:.0f},{top+124*s_:.0f} l{26*s_:.0f},{-86*s_:.0f}'
              f' l{26*s_:.0f},{86*s_:.0f} Z" fill="#0b0a12"/>')
    s += (f'<path d="M{x-wb:.0f},{low} L{x-wt:.0f},{top+120*s_:.0f}'
          f' q{wt:.0f},{-80*s_:.0f} {wt*2:.0f},0 L{x+wb:.0f},{low} Z"'
          f' fill="#000" opacity=".45" transform="scale(1.04) translate({-x*.04:.0f},{-low*.04:.0f})"/>')
    s += "</g>"
    return s


def tolpa_siluety(y, t, n=9, seed=5, h=240, col="#13151d", ogonki=0.0):
    """Ряд силуэтов со спины: плечи разной высоты, лёгкое покачивание."""
    s = ""
    rnd = random.Random(seed)
    for i in range(n):
        x = 60 + i * (W - 120) / max(1, n - 1) + rnd.randint(-24, 24)
        hh = h * rnd.uniform(.82, 1.12)
        dx = 4 * A.w(t, .45, i * .5)
        s += f'<g transform="translate({dx:.1f},0)">{siluet(x, y, hh, col, .96, platok=(i % 3 == 0))}</g>'
        if ogonki > 0 and i / n <= ogonki:
            s += ogonek_grudi(x, y - hh * .62, t, .7, i * .4, .3)
    return s


# ═══════════════════ 1. ОТКРЫТИЕ ═══════════════════
def sumerechnoe_nebo_nad_kryshami(t):
    """Синее раннее небо, внизу тёмная линия крыш. Титр встаёт слева."""
    s = nebo("sumer", t, True, 15)
    s += SL(Z_DAL, oblaka(t, 150, 4, 21, .4, "#cfd8e6", 9.0))
    # линия крыш силуэтом
    d = "M-20,860"
    rnd = random.Random(7)
    x = -20
    while x < W + 40:
        w_ = rnd.randint(120, 230)
        hh = rnd.randint(70, 180)
        d += f" V{860-hh} h{w_} V860"
        x += w_
    d += f" L{W+40},{H} H-20 Z"
    s += SL(Z_SRED, f'<path d="{d}" fill="#141a2a" {o(0)}/>')
    # дымки из труб
    for i, tx in enumerate((210, 520, 980, 1430, 1720)):
        s += SL(Z_SRED, f'<rect x="{tx}" y="{700+i%3*40}" width="34" height="80" fill="#0f1420"/>')
        s += SL(Z_SRED, dym(tx + 17, 690 + i % 3 * 40, t, 4, .20, 260, .26 + .04 * (i % 2), wide=1.3))
    # первые звёзды мигают
    for i in range(16):
        rnd = random.Random(300 + i)
        zx, zy = rnd.randint(40, W - 40), rnd.randint(60, 480)
        mg = .35 + .55 * abs(A.w(t, .5 + rnd.random(), rnd.random()))
        s += f'<circle cx="{zx}" cy="{zy}" r="{rnd.uniform(1.8,3.4):.1f}" fill="#fff6e2" opacity="{mg:.2f}"/>'
    s += sneg_letit(t, 30, 11, .5, .7)
    s += SL(Z_PERED, f'<path d="M-20,{H} V960 q300,-40 640,-10 V{H} Z" fill="#0b0e18" {o(0)}/>')
    s += vinetka(.44)
    return s


def shkatulka_s_klyuchikom(t):
    """Записка ложится в шкатулку, ключик поворачивается и прячется."""
    s = f'<rect width="{W}" height="{H}" fill="#241a12"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 760, 92))
    s += f'<rect width="{W}" height="{H}" fill="#1a120c" opacity=".45"/>'
    s += teplo(560, 560, 760, 520, .92)
    s += SL(Z_SRED, f'<rect y="700" width="{W}" height="380" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M-20,690 q500,-40 1000,-12 q500,28 960,-10 V800 H-20 Z" fill="url(#rush)" {o(6)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="{-20+i*230}" y="690" width="10" height="390" fill="#c8a877" opacity=".35"/>')
    s += SL(Z_SRED, f'<rect y="690" width="{W}" height="12" fill="#fff3d8" opacity=".3"/>')
    s += lampa(1480, 700, t, 1.7)
    # шкатулка
    s += ten(520, 880, 250, 26, .55)
    s += (f'<rect x="210" y="640" width="640" height="250" rx="14" fill="url(#derev)" {o(8)}/>'
          f'<rect x="210" y="626" width="640" height="54" rx="12" fill="#a9754a" {o(7)}/>'
          f'<rect x="234" y="666" width="592" height="22" fill="#000" opacity=".22"/>'
          f'<rect x="234" y="700" width="592" height="160" rx="8" fill="#5e3f26" opacity=".5"/>')
    # записка опускается внутрь
    k = A.ease(A.seg(t, .2, 1.3))
    zy = 440 + 220 * k
    s += (f'<g transform="translate(0,{zy-520:.0f}) rotate({-6+10*k:.1f} 500 540)" opacity="{1-.15*k:.2f}">'
          f'<path d="M430,500 h150 l12,86 h-174 Z" fill="url(#list)" {o(5)}/>'
          f'<path d="M444,524 h120 M444,548 h96" stroke="#9a8a6c" stroke-width="5" opacity=".7"/></g>')
    # замочек и ключик
    kk = A.out(A.seg(t, 1.9, 1.1))
    s += (f'<rect x="470" y="740" width="120" height="96" rx="12" fill="url(#zol)" {o(6)}/>'
          f'<circle cx="530" cy="786" r="17" fill="#2a2018"/>'
          f'<g transform="rotate({90*kk:.0f} 530 786)" opacity="{1-kk*.5:.2f}">'
          f'<rect x="521" y="786" width="18" height="74" rx="5" fill="url(#zol)" {o(4)}/>'
          f'<circle cx="530" cy="874" r="24" fill="none" stroke="url(#zol)" stroke-width="13"/></g>')
    # руки не рисуем (правило 05.11): предмет работает сам
    s += f'<g opacity=".5">{par(560, 660, t, 3, .4, 150, .3)}</g>'
    s += SL(Z_PERED, _mebel_hlam(1620, 1040, 300, t, 41))
    s += ramka_pp("levo", "#120c08", .5)
    s += vinetka(.5)
    return s


def dva_silueta_v_arke(t):
    """Каменная арка, два силуэта со спины, из-за колонны выползает нить."""
    s = f'<rect width="{W}" height="{H}" fill="#191622"/>'
    s += SL(Z_DAL, kladka(-20, -20, W + 40, H + 40, 96, "url(#kamen)"))
    s += f'<rect width="{W}" height="{H}" fill="#120f18" opacity=".55"/>'
    s += SL(Z_DAL, svody(t, "#4a4336", 3))
    s += teplo(980, 420, 700, 520, .55)
    # арка в глубине
    s += SL(Z_SRED, f'<path d="M700,1000 V500 q260,-220 520,0 V1000 Z" fill="#2a2636" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M760,1000 V520 q200,-170 400,0 V1000 Z" fill="#39304a" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M820,1000 V540 q140,-120 280,0 V1000 Z" fill="#36405e" {o(0)}/>')
    s += SL(Z_SRED, f'<path d="M820,1000 V540 q140,-120 280,0 V1000 Z" fill="url(#teplo)" opacity=".5"/>')
    # колонны переднего плана
    for cx in (210, 1700):
        s += SL(Z_PERED, f'<rect x="{cx-90}" y="-20" width="180" height="{H+40}" fill="#241f2c" {o(0)}/>'
                         f'<rect x="{cx-100}" y="860" width="200" height="56" rx="10" fill="#2d2735" {o(5)}/>')
    # факелы: пламя и колышущаяся тень
    for i, (fx, fy) in enumerate(((430, 380), (1480, 360))):
        s += f'<rect x="{fx-8}" y="{fy}" width="16" height="120" fill="url(#derev)" {o(4)}/>'
        s += ogon(fx, fy - 10, t, 1.1, i * .6, 5)
        s += f'<ellipse cx="{fx}" cy="{fy+170}" rx="{90+16*A.w(t,.9,i):.0f}" ry="30" fill="#000" opacity=".3"/>'
    # двое со спины в арке
    s += figura(900, 1000, 350, t, "#0e1018", "#ffd08a", False, .0, True)
    s += figura(1032, 1000, 336, t, "#0e1018", "#ffd08a", True, .5, True)
    # нить шёпота выползает из-за колонны
    if t > .8:
        s += nit_shepota([(300, 760), (520, 700), (700, 690), (880, 700)], t - .8, .85)
    # песок с карниза
    for i in range(10):
        rnd = random.Random(60 + i)
        sx = rnd.randint(300, 1600)
        ph = rnd.random() * 2.2
        s += (f'<rect x="{sx}" y="{120+240*A.seg(t, ph, 2.2):.0f}" width="3" height="16"'
              f' fill="#cdbfa6" opacity="{.3*(1-A.seg(t, ph, 2.2)):.2f}"/>')
    s += vinetka(.52)
    return s


def koster_pod_tuchey(t):
    """Нить уходит к тени короны, внизу вспыхивает костёр и дважды гаснет."""
    s = f'<rect width="{W}" height="{H}" fill="#15121c"/>'
    s += SL(Z_DAL, kladka(-20, -20, W + 40, H + 40, 92, "url(#kamen)"))
    s += f'<rect width="{W}" height="{H}" fill="#100d16" opacity=".55"/>'
    s += ten_korony(430, 40, t, .95, naklon=1.0)
    # костёр слева внизу: вспыхивает, два раза схлопывается в дымок
    gas1, gas2 = A.seg(t, 2.0, .5), A.seg(t, 3.4, .5)
    zhiv = 1.0 - .85 * (gas1 if gas1 < 1 else 0) - .85 * (gas2 if gas2 < 1 else 0)
    zhiv = max(.08, min(1.0, zhiv))
    s += ten(400, 1010, 240, 26, .55)
    for i, (dx, dy, w_) in enumerate(((-110, 0, 220), (-20, -16, 200), (70, 6, 190))):
        s += (f'<rect x="{400+dx:.0f}" y="{960+dy:.0f}" width="{w_}" height="26" rx="10"'
              f' fill="url(#derev)" {o(5)} transform="rotate({-12+i*12} {400+dx+w_/2:.0f} {972+dy:.0f})"/>')
    s += teplo(400, 880, 520 * zhiv + 90, 420 * zhiv + 70, .95 * zhiv + .1)
    if zhiv > .2:
        s += ugli(270, 950, 260, t, 9, 3)
        s += ogon(400, 930, t, 2.6 * zhiv, .1, int(9 * zhiv) + 1)
        s += iskra_let(t, 400, 900, 12, 7, 420, .6)
    s += dym(400, 900, t, 6, .24, 420, .30 + .2 * (1 - zhiv), wide=1.4)
    s += dym(470, 920, t, 4, .20, 380, .22 + .2 * (1 - zhiv), wide=1.1)
    # нить шёпота идёт вверх к короне
    s += nit_shepota([(360, 880), (420, 640), (470, 420), (440, 230)], t, .8, faza=.3)
    s += ramka_pp("levo", "#0c0a10", .45)
    s += vinetka(.5)
    return s


def ovin_i_solnce_na_zakate(t):
    """Слева овин, под ним загорается огонь; справа солнце меркнет."""
    s = nebo("zakat", t, False, 23)
    s += SL(Z_NEBO, oblaka(t, 220, 5, 29, .45, "#e8c9a4", 12.0))
    # солнце меркнет на слове «гасит»
    mer = A.ease(A.seg(t, 3.6, 2.2))
    sx, sy = 1480, 430
    s += SL(Z_NEBO, f'<circle cx="{sx}" cy="{sy}" r="{260-40*mer:.0f}" fill="url(#teplo)"'
                    f' opacity="{.75-.5*mer:.2f}"/>')
    s += SL(Z_NEBO, f'<circle cx="{sx}" cy="{sy}" r="{96-14*mer:.0f}" fill="#ffd98a"'
                    f' opacity="{.95-.55*mer:.2f}"/>')
    s += SL(Z_DAL, f'<path d="M-20,760 q480,-90 980,-30 q500,60 960,-20 V{H} H-20 Z"'
                   f' fill="#8a7a62" {o(7)}/>')
    s += SL(Z_DAL, _sneg_lezhit(790, 22, "url(#sneg)"))
    s += SL(Z_SRED, _ulica_dal(1180, 790, 740, t, True, 31))
    # овин слева: сруб с высокой крышей, под ним дверца
    s += ten(430, 900, 330, 30, .5)
    s += SL(Z_SRED, brevna(230, 530, 400, 330, 66))
    s += SL(Z_SRED, f'<path d="M190,540 L430,360 L670,540 Z" fill="#6d4b2c" {o(8)}/>')
    s += SL(Z_SRED, f'<path d="M190,540 L430,360 L670,540 Z" fill="url(#sneg)" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="366" y="690" width="130" height="170" rx="8" fill="#241a12" {o(6)}/>')
    # огонь под овином разгорается на «разжигает»
    raz = A.ease(A.seg(t, .6, 1.8))
    if raz > .05:
        s += teplo(430, 840, 300 * raz, 240 * raz, .85 * raz)
        s += ogon(430, 830, t, 1.3 * raz, .2, int(7 * raz) + 1)
        s += iskra_let(t, 430, 790, 10, 9, 380, .55)
        s += dym(430, 740, t, 5, .22, 340, .26, wide=1.2)
    # длинные тени по снегу
    for i, tx in enumerate((300, 520, 760)):
        dl = 220 + 160 * mer
        s += SL(Z_SRED, f'<path d="M{tx},880 l{dl},26 l24,16 l-{dl},-20 Z" fill="#2b2a3a" opacity=".3"/>')
    s += sneg_letit(t, 22, 17, .4, .6)
    s += vinetka(.46)
    return s


def vecher_u_pechki(t):
    """Открытая дверца печки, семья полукругом, дед поднимает ладонь."""
    s = f'<rect width="{W}" height="{H}" fill="#2a1f16"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 820, 94))
    s += f'<rect width="{W}" height="{H}" fill="#1b1309" opacity=".42"/>'
    s += SL(Z_SRED, polovicy(900, "url(#pol)"))
    s += teplo(560, 660, 700, 520, .95)
    # печь с открытой дверцей
    s += SL(Z_SRED, pech(240, 300, 640, 620, t, True, True, False))
    s += SL(Z_SRED, f'<rect x="240" y="300" width="640" height="620" rx="10" fill="{ORA}" opacity=".10"/>')
    s += SL(Z_SRED, f'<ellipse cx="545" cy="760" rx="{330+30*A.w(t,.7):.0f}" ry="260"'
                    f' fill="url(#teplo)" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="430" y="640" width="230" height="200" rx="10" fill="#140d08" {o(0)}/>')
    s += ogon(545, 800, t, 1.6, .1, 7)
    s += ugli(460, 826, 170, t, 7, 5)
    # семья полукругом: дед на скамейке, дети на полу
    s += lavka(1080, 860, 300)
    ruka = A.out(A.seg(t, 1.4, .9))
    s += (f'<g transform="translate(0,{-6*A.w(t,.5):.1f})">'
          f'{figura(1180, 860, 330, t, "#1c1a22", "#ffb866", False, .2, True)}'
          f'<path d="M1232,{690-46*ruka:.0f} q34,{-34*ruka:.0f} 62,{-12*ruka:.0f}"'
          f' stroke="#1c1a22" stroke-width="28" fill="none" opacity=".95"/>'
          f'<path d="M1232,{690-46*ruka:.0f} q34,{-34*ruka:.0f} 62,{-12*ruka:.0f}"'
          f' stroke="#ffb866" stroke-width="5" fill="none" opacity=".6"/></g>')
    for i, (cx, hh) in enumerate(((880, 180), (1000, 165), (1370, 175), (1480, 160))):
        naklon = 5 * ruka
        s += (f'<g transform="rotate({naklon*(1 if cx<1200 else -1):.1f} {cx} 1010)">'
              f'{figura(cx, 1010, hh * 1.25, t, "#231f28", "#ffb062", (i % 2 == 0), i * .4, True)}</g>')
    # кот тянется
    s += kot(770, 1012, t, 1.05, "#3b3430", spit=False)
    # отсветы огня на стене и тень деда
    s += (f'<ellipse cx="1180" cy="430" rx="{150+26*A.w(t,.8):.0f}" ry="240"'
          f' fill="#000" opacity=".26"/>')
    s += f'<g opacity=".4">{par(545, 700, t, 4, .35, 200, .3)}</g>'
    s += SL(Z_PERED, _ramka_pp("oba", "#120b06", .4))
    s += vinetka(.5)
    return s


def babushka_u_okna_s_zanaveskoy(t):
    """Бабушка у окна, соседка машет с улицы, занавеска задёргивается."""
    s = f'<rect width="{W}" height="{H}" fill="#6d5b45"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 900, 90))
    s += f'<rect width="{W}" height="{H}" fill="#3b2c1c" opacity=".3"/>'
    s += SL(Z_SRED, polovicy(930, "url(#pol)"))
    s += teplo(760, 420, 620, 460, .6)
    # окно с видом на улицу и соседкой
    vid = (f'<rect width="400" height="330" fill="#6f87a6"/>'
           f'{_sneg_lezhit(250, 14, "#dfe9f6")}'
           f'<g transform="translate(250,250) scale(.5)">{siluet(0, 0, 300, "#2c3444", .9, platok=True)}</g>'
           f'<path d="M262,{150+8*A.w(t,1.6):.0f} q26,-26 40,-6" stroke="#2c3444"'
           f' stroke-width="13" fill="none"/>')
    s += SL(Z_SRED, okno_izby(560, 230, 400, 330, t, vid, .18, False, True))
    # занавеска едет по струне
    k = A.ease(A.seg(t, 3.4, 1.4))
    s += SL(Z_SRED, f'<rect x="540" y="214" width="440" height="10" rx="5" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, zanaveska(548, 224, 350, 120 + 230 * k, "url(#rush)", t, 1))
    s += SL(Z_SRED, zanaveska(972 - 120 - 230 * k, 224, 350, 120 + 230 * k, "url(#rush)", t, -1))
    # столетник в горшке на подоконнике
    s += SL(Z_SRED, f'<rect x="590" y="560" width="340" height="26" rx="6" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M640,560 h90 l-10,-54 h-70 Z" fill="url(#glina)" {o(5)}/>')
    for i in range(5):
        kach = 4 * A.w(t, .6, i * .4)
        s += SL(Z_SRED, f'<path d="M685,506 q{-40+i*20+kach:.0f},-40 {-24+i*12+kach:.0f},-96'
                        f' q{10},26 {16},96 Z" fill="{ZEL2}" {o(4)}/>')
    # бабушка у окна: качает головой
    nak = 4 * A.w(t, .9) * (1 if t > 3.0 else .3)
    s += (f'<g transform="rotate({nak:.1f} 300 1070)">'
          f'{figura(300, 1070, 620, t, "#2f2a30", "#ffd9a0", True, .1, True)}</g>')
    # пар от чашки
    s += SL(Z_SRED, f'<rect x="1210" y="700" width="300" height="24" rx="6" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, krynka(1330, 700, .8))
    s += par(1348, 640, t, 4, .5, 180, .4)
    s += SL(Z_PERED, _mebel_hlam(1700, 1050, 300, t, 63))
    s += ramka_pp("levo", "#1a1208", .42)
    s += vinetka(.48)
    return s


def dom_pod_tuchey_iz_slov(t):
    """Из форточки вылетают слова-пёрышки и собираются в тучу над домом."""
    s = nebo("sumer", t, True, 33)
    s += SL(Z_DAL, _ulica_dal(60, 820, 1800, t, True, 19))
    s += SL(Z_SRED, izba_snaruzhi(560, 900, 760, t, True, True, 5))
    s += SL(Z_SRED, _sneg_lezhit(900, 20, "url(#sneg)"))
    # пёрышки-слова из форточки
    sb = A.ease(A.seg(t, 1.2, 1.4))
    for i in range(14):
        rnd = random.Random(400 + i)
        ph = rnd.random()
        k = A.seg(t, ph * 1.2, 2.0)
        x0, y0 = 700, 560
        tx = 760 + (i - 7) * 95 * (1 - sb) + (i - 7) * 26 * sb
        ty = 300 - 120 * k - 60 * sb
        x = x0 + (tx - x0) * k
        y = y0 + (ty - y0) * k
        rot = -30 + 60 * rnd.random() + 20 * A.w(t, .8, ph)
        s += (f'<g transform="rotate({rot:.0f} {x:.0f} {y:.0f})" opacity="{.25+.6*(1-abs(.5-k)*1.2):.2f}">'
              f'<path d="M{x:.0f},{y:.0f} q22,-16 44,-2 q-20,16 -44,2 Z" fill="#e9e2d2"/></g>')
    # туча собирается над этим же домом
    if sb > .05:
        s += SL(Z_SRED, f'<g opacity="{.7*sb:.2f}">{_oblaka(t, 250, 3, 77, .9, "#5d6472", 4.0)}</g>')
        s += SL(Z_SRED, f'<ellipse cx="860" cy="270" rx="{300*sb:.0f}" ry="{90*sb:.0f}"'
                        f' fill="#4e545f" opacity="{.8*sb:.2f}"/>')
    # снег валит только на этот дом
    for i in range(26):
        rnd = random.Random(500 + i)
        sx = 600 + rnd.randint(0, 520)
        ph = rnd.random() * 2.4
        k = A.seg(t, ph, 2.4)
        s += (f'<circle cx="{sx+20*A.w(t,.5,ph):.0f}" cy="{330+620*k:.0f}" r="{rnd.uniform(2.4,4.6):.1f}"'
              f' fill="#f2f7ff" opacity="{.7*sb*(1-k*.4):.2f}"/>')
    s += vinetka(.46)
    return s


def ulica_s_nizkim_solncem(t):
    """Сельская улица, низкое солнце как стрелка часов, двое идут навстречу."""
    s = nebo("zakat", t, False, 43)
    s += SL(Z_NEBO, oblaka(t, 230, 4, 47, .4, "#e6c8a6", 11.0))
    sol = A.ease(A.seg(t, .4, 4.0))
    s += SL(Z_NEBO, f'<circle cx="1180" cy="{400+90*sol:.0f}" r="240" fill="url(#teplo)" opacity=".7"/>')
    s += SL(Z_NEBO, f'<circle cx="1180" cy="{400+90*sol:.0f}" r="88" fill="#ffd27a" opacity=".92"/>')
    s += SL(Z_DAL, f'<path d="M-20,790 q500,-60 1000,-20 q500,40 960,-14 V{H} H-20 Z"'
                   f' fill="#7e7360" {o(7)}/>')
    s += SL(Z_DAL, _sneg_lezhit(810, 20, "url(#sneg)"))
    # изб�� по обе стороны улицы
    for i, (x, b, w_, sd) in enumerate(((120, 880, 330, 3), (1540, 900, 360, 9))):
        s += SL(Z_SRED, izba_snaruzhi(x, b, w_, t, True, True, sd))
    s += SL(Z_DAL, _ulica_dal(520, 800, 900, t, True, 51))
    # дым из труб
    for i, tx in enumerate((190, 1600)):
        s += SL(Z_SRED, dym(tx, 690, t, 4, .22, 280, .3, wide=1.2))
    # двое идут навстречу
    ka = A.seg(t, 0, 6.5)
    s += SL(Z_SRED, siluet(260 + 420 * ka, 960, 250, "#241f28", .95))
    s += SL(Z_SRED, siluet(1660 - 430 * ka, 965, 258, "#241f28", .95, platok=True))
    # тени удлиняются
    for cx, dl in ((260 + 420 * ka, 180 + 150 * sol), (1660 - 430 * ka, -180 - 150 * sol)):
        s += SL(Z_SRED, f'<path d="M{cx:.0f},968 l{dl:.0f},22 l20,14 l{-dl:.0f},-18 Z"'
                        f' fill="#2e2b3a" opacity=".32"/>')
    s += sneg_letit(t, 18, 23, .35, .5)
    s += vinetka(.46)
    return s


def topor_v_kolode_pod_navesom(t):
    """Навес: топор в колоде, рукавицы на гвозде, тачка под снегом."""
    s = nebo("sumer", t, True, 57)
    s += SL(Z_DAL, _ulica_dal(40, 760, 1840, t, True, 61))
    s += f'<rect width="{W}" height="{H}" fill="#12131d" opacity=".32"/>'
    # навес: стойки и скат
    s += SL(Z_SRED, f'<path d="M80,300 L1180,240 L1180,300 L80,360 Z" fill="#5a3f26" {o(8)}/>')
    s += SL(Z_SRED, f'<path d="M80,300 L1180,240 L1180,268 L80,328 Z" fill="url(#sneg)" opacity=".55"/>')
    for sx in (140, 1080):
        s += SL(Z_SRED, f'<rect x="{sx}" y="320" width="40" height="700" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, polovicy(1010, "#6b5338"))
    s += teplo(1520, 620, 420, 420, .55)
    # дверь дома справа со светом
    s += SL(Z_SRED, f'<rect x="1380" y="420" width="300" height="600" rx="8" fill="#241a12" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="1410" y="450" width="240" height="560" rx="6" fill="{SVET}"'
                    f' opacity="{.55+.08*A.w(t,.7):.2f}"/>')
    s += SL(Z_SRED, luch(1410, 450, 240, 560, t, .22))
    # колода и топор
    s += ten(540, 1010, 190, 24, .5)
    s += SL(Z_SRED, f'<ellipse cx="540" cy="820" rx="130" ry="34" fill="#8a6039" {o(6)}/>'
                    f'<path d="M410,820 v170 q130,34 260,0 V820 Z" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<g transform="rotate(-24 540 800)">'
                    f'<rect x="528" y="640" width="26" height="180" rx="6" fill="url(#derev)" {o(5)}/>'
                    f'<path d="M506,620 q46,-30 86,-8 l-10,52 q-40,-16 -76,6 Z" fill="url(#zhel)" {o(6)}/></g>')
    # рукавицы на гвозде: качаются и уносятся
    uh = A.ease(A.seg(t, 4.6, 2.0))
    if uh < .96:
        for i in range(2):
            kach = 7 * A.w(t, 1.0, i * .5)
            rx = 880 + i * 60 + 420 * uh
            ry = 460 + 30 * uh
            s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {rx} {ry})" opacity="{1-uh:.2f}">'
                            f'<path d="M{rx-26},{ry} q26,-26 52,0 v86 q-26,20 -52,0 Z" fill="{TKAN}" {o(5)}/>'
                            f'<path d="M{rx+26},{ry+20} q26,6 20,40 q-14,10 -20,-10 Z" fill="{TKAN}" {o(4)}/></g>')
    s += SL(Z_SRED, f'<circle cx="900" cy="446" r="7" fill="{ZHELEZ}"/>')
    # тачка под снежной шапкой
    s += ten(1180, 1010, 150, 20, .45)
    s += SL(Z_SRED, f'<path d="M1080,900 h220 l-26,96 h-168 Z" fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M1074,896 q106,-34 232,0 q-106,24 -232,0 Z" fill="url(#sneg)" {o(5)}/>'
                    f'<circle cx="1112" cy="1008" r="30" fill="{CHUGUN}" {o(5)}/>')
    s += sneg_letit(t, 34, 29, .6, .8)
    s += SL(Z_PERED, f'<path d="M-20,{H} V940 q260,-30 520,-6 V{H} Z" fill="#0d0e16" {o(0)}/>')
    s += vinetka(.46)
    return s


# ═══════════════════ 2. ИСТОРИЯ ДНЯ ═══════════════════
def nochnaya_pustynya_so_zvezdami(t):
    """Глубокая синяя ночь, барханы, по тропе идут два огонька."""
    s = nebo("noch", t, True, 71)
    s += SL(Z_NEBO, f'<circle cx="1560" cy="200" r="70" fill="#f6efd8" opacity=".9"/>'
                    f'<circle cx="1560" cy="200" r="190" fill="url(#teplo)" opacity=".4"/>')
    s += barhany(t, 5, 560)
    # караванная тропа
    s += SL(Z_SRED, f'<path d="M-20,1020 q500,-120 940,-180 q420,-54 1020,-120"'
                    f' fill="none" stroke="#3a4466" stroke-width="26" opacity=".5"/>')
    # два огонька идут по тропе
    k = A.seg(t, 0, 5.0)
    for i in range(2):
        x = 120 + 1300 * k + i * 70
        y = 1000 - 240 * k
        s += ogonek_grudi(x, y, t, 1.25, i * .5, .35)
    s += f'<g opacity=".4">{_tuman(t, 900, .3, "#48567a")}</g>'
    s += vinetka(.5)
    return s


def dvorec_s_palmami(t):
    """Белый дворец с арками и пальмами, двое несут свиток и кувшин."""
    s = nebo("rassv", t, False, 83)
    s += SL(Z_NEBO, oblaka(t, 180, 4, 89, .35, "#f0dcc0", 10.0))
    s += SL(Z_DAL, f'<path d="M-20,820 q400,-40 820,-16 V{H} H-20 Z" fill="#c8ad84" {o(7)}/>')
    # дворец в левой полосе (справа окно вставки)
    s += SL(Z_SRED, dvorec_stena(60, 360, 720, 460, t, 4, True))
    s += SL(Z_SRED, f'<path d="M40,360 L420,210 L800,360 Z" fill="#d9c49c" {o(8)}/>')
    s += SL(Z_SRED, f'<circle cx="420" cy="196" r="26" fill="url(#zol)" {o(4)}/>')
    # галерея и бассейн
    s += SL(Z_SRED, f'<rect x="60" y="820" width="740" height="40" rx="8" fill="#d6bd95" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="120" y="900" width="620" height="120" rx="16" fill="url(#voda)" {o(6)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{150+i*120},{940+10*A.w(t,.8,i*.4):.0f} q30,-10 60,0"'
                        f' stroke="#9fd4dc" stroke-width="5" fill="none" opacity=".5"/>')
    # пальмы
    s += SL(Z_SRED, palma(150, 880, t, .9, .1))
    s += SL(Z_PERED, palma(760, 1010, t, 1.25, .6))
    # факелы у входа
    for i, fx in enumerate((330, 520)):
        s += SL(Z_SRED, f'<rect x="{fx-7}" y="700" width="14" height="110" fill="url(#derev)" {o(4)}/>')
        s += SL(Z_SRED, ogon(fx, 692, t, .9, i * .5, 4))
    # двое придворных со спины: свиток и кувшин
    ka = A.seg(t, 0, 5.2)
    x1 = 240 + 300 * ka
    s += SL(Z_SRED, siluet(x1, 880, 230, "#4a3c34", .95))
    s += SL(Z_SRED, f'<rect x="{x1+40:.0f}" y="760" width="70" height="20" rx="8" fill="url(#list)" {o(4)}/>')
    s += SL(Z_SRED, siluet(x1 + 110, 884, 224, "#4a3c34", .95))
    s += SL(Z_SRED, krynka(x1 + 160, 790, .5))
    s += vinetka(.42)
    return s


def nisha_za_zanavesom(t):
    """Тёмная ниша, двое прикрывают ладонями по огоньку, мимо идёт тень."""
    s = f'<rect width="{W}" height="{H}" fill="#120f16"/>'
    s += SL(Z_DAL, kladka(-20, -20, W + 40, H + 40, 88, "url(#kamen)"))
    s += f'<rect width="{W}" height="{H}" fill="#0c0a10" opacity=".62"/>'
    s += teplo(960, 640, 520, 420, .5)
    # занавес
    for i in range(7):
        kach = 10 * A.w(t, .45, i * .5)
        s += SL(Z_PERED, f'<path d="M{1480+i*70+kach:.0f},-20 q30,540 {-16+kach*.6:.0f},1120 h78 '
                         f'q16,-580 -14,-1120 Z" fill="#3a2430" {o(6)}/>')
    # двое со спины, у каждого огонёк в ладонях
    for i, (cx, hh) in enumerate(((620, 420), (900, 405))):
        s += siluet(cx, 1020, hh, "#191620", .98, platok=(i == 1))
        s += ogonek_grudi(cx + 30, 1020 - hh * .55, t, .8, i * .6, .0)
        # ладонь прикрывает, когда проходит тень
        pr = A.seg(t, 1.2, 2.2)
        pri = 1.0 if .35 < pr < .62 else 0.0
        if pri:
            s += (f'<path d="M{cx+6},{1020-hh*.55-34:.0f} q40,-26 76,2 q-38,22 -76,-2 Z"'
                  f' fill="#1d1a24" opacity=".92"/>')
    # тень стражника проходит по полу
    pr = A.seg(t, 1.2, 2.2)
    tx = -200 + 2200 * pr
    s += (f'<ellipse cx="{tx:.0f}" cy="1030" rx="180" ry="44" fill="#000" opacity=".45"/>'
          f'<path d="M{tx-70:.0f},1030 V640 q70,-40 140,0 V1030 Z" fill="#000" opacity=".3"/>')
    s += vinetka(.56)
    return s


def ten_trona(t):
    """Тень трона с короной, к ней ползёт нить, у подножия вспыхивает красным."""
    s = f'<rect width="{W}" height="{H}" fill="#1a1520"/>'
    s += SL(Z_DAL, kladka(-20, -20, W + 40, H + 40, 94, "url(#kamen)"))
    s += f'<rect width="{W}" height="{H}" fill="#120e16" opacity=".5"/>'
    s += teplo(1620, 300, 420, 420, .45)
    s += SL(Z_SRED, polovicy(1000, "#6a5c4a"))
    s += ten_korony(900, 60, t, 1.0, naklon=1.0)
    # факел чадит справа
    s += SL(Z_SRED, f'<rect x="1700" y="300" width="18" height="140" fill="url(#derev)" {o(4)}/>')
    s += ogon(1709, 290, t, 1.2, .3, 6)
    s += dym(1709, 250, t, 5, .3, 300, .34, wide=1.3)
    # нить ползёт по полу к подножию и вспыхивает
    k = A.seg(t, .2, 2.4)
    pts = [(120, 1010), (420, 980), (700, 960), (880, 940)]
    s += nit_shepota(pts[:max(2, int(2 + 2 * k))], t, .9)
    if k > .9:
        s += (f'<circle cx="880" cy="930" r="{80*(k-.9)*10:.0f}" fill="{UGOL}"'
              f' opacity="{.6*(1-(k-.9)*6):.2f}"/>')
    s += vinetka(.56)
    return s


def lestnica_k_tronu(t):
    """Широкая лестница, двое наверху, внизу в тени загораются глаза."""
    s = f'<rect width="{W}" height="{H}" fill="#171320"/>'
    s += SL(Z_DAL, kladka(-20, -20, W + 40, 620, 90, "url(#kamen)"))
    s += f'<rect width="{W}" height="{H}" fill="#100d16" opacity=".5"/>'
    s += teplo(960, 240, 620, 420, .5)
    # ступени
    for i in range(9):
        y = 520 + i * 64
        ins = i * 70
        s += SL(Z_SRED - i * 10, f'<rect x="{ins}" y="{y}" width="{W-ins*2}" height="64"'
                                 f' fill="{"#514637" if i%2 else "#463c2f"}" {o(5)}/>')
        s += SL(Z_SRED - i * 10, f'<rect x="{ins}" y="{y}" width="{W-ins*2}" height="10"'
                                 f' fill="#6b5e49" opacity=".5"/>')
    # двое на верхних ступенях
    s += SL(Z_SRED, siluet(840, 530, 300, "#20202c", .97))
    s += SL(Z_SRED, siluet(1040, 532, 292, "#20202c", .97, platok=True))
    # придворные в тени, глаза загораются по одному
    for i, (cx, ph) in enumerate(((240, .4), (470, 1.2), (1450, 2.0), (1700, 2.8))):
        s += SL(Z_PERED, siluet(cx, 1050, 270, "#0c0b12", .95))
        if t > ph:
            op = min(1.0, (t - ph) * 1.4) * (.6 + .4 * abs(A.w(t, 1.1, i)))
            for dx in (-16, 16):
                s += (f'<ellipse cx="{cx+dx}" cy="{1050-270*.78:.0f}" rx="9" ry="6"'
                      f' fill="#8ef0a8" opacity="{op:.2f}"/>')
    # пыль в луче
    s += luch(700, 0, 520, 620, t, .16)
    s += vinetka(.56)
    return s


def sud_pered_tenyu(t):
    """Двое перед тенью трона, их огоньки разгораются и освещают пол."""
    s = f'<rect width="{W}" height="{H}" fill="#191420"/>'
    s += SL(Z_DAL, kladka(-20, -20, W + 40, H + 40, 92, "url(#kamen)"))
    s += f'<rect width="{W}" height="{H}" fill="#110d15" opacity=".55"/>'
    s += SL(Z_SRED, polovicy(1010, "#60543f"))
    rost = A.ease(A.seg(t, .8, 1.6))
    s += ten_korony(960, 40, t, 1.05, naklon=-.6)
    # свет от огоньков на полу
    s += teplo(860, 940, 420 * (.5 + rost), 160 * (.5 + rost), .35 + .4 * rost)
    for i, cx in enumerate((800, 960)):
        s += siluet(cx, 1020, 420, "#1b1823", .98, platok=(i == 1))
        s += ogonek_grudi(cx + 24, 1020 - 420 * .56, t, .9 + .5 * rost, i * .5, rost)
    # копья стражи блестят
    for i, cx in enumerate((300, 420, 1520, 1660)):
        s += SL(Z_PERED, f'<rect x="{cx}" y="300" width="12" height="760" fill="#2b2a33" {o(4)}/>'
                         f'<path d="M{cx-10},300 l18,-56 l18,56 Z" fill="url(#zhel)" {o(4)}/>'
                         f'<rect x="{cx-2}" y="{320+30*A.w(t,.5,i*.6):.0f}" width="6" height="40"'
                         f' fill="#fff" opacity=".35"/>')
    s += vinetka(.58)
    return s


def ploschad_s_kostrom(t):
    """Площадь перед дворцом, дрова ещё не горят, толпа сходится, свиток."""
    s = nebo("sumer", t, True, 97)
    s += SL(Z_NEBO, oblaka(t, 200, 4, 101, .4, "#c9b49a", 9.0))
    s += SL(Z_DAL, dvorec_stena(-40, 300, 1200, 420, t, 6, True))
    s += SL(Z_DAL, f'<path d="M-20,720 H{W+20} V{H} H-20 Z" fill="#7c6c52" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M-20,760 H{W+20} V{H} H-20 Z" fill="#6b5c45" {o(6)}/>')
    # факелы у стен мерцают
    for i, fx in enumerate((160, 560, 1360, 1760)):
        s += SL(Z_DAL, f'<rect x="{fx-7}" y="560" width="14" height="110" fill="url(#derev)" {o(3)}/>')
        s += SL(Z_DAL, ogon(fx, 552, t, .8, i * .4, 4))
    # сложенные дрова в центре
    s += ten(940, 1000, 230, 26, .5)
    for i, a in enumerate((-34, -18, 0, 17, 33)):
        s += SL(Z_SRED, f'<rect x="922" y="760" width="42" height="250" rx="12" fill="url(#derev)" {o(7)}'
                        f' transform="rotate({a} 943 1004)"/>')
    for i, (yy, ww) in enumerate(((930, 300), (880, 240))):
        s += SL(Z_SRED, f'<rect x="{943-ww//2}" y="{yy}" width="{ww}" height="30" rx="12"'
                        f' fill="#7a5433" {o(6)} transform="rotate({-6+i*12} 943 {yy})"/>')
    s += SL(Z_SRED, f'<ellipse cx="943" cy="1004" rx="150" ry="26" fill="#4a3522" {o(5)}/>')
    # толпа сходится к дровам
    k = A.ease(A.seg(t, .4, 4.2))
    for i in range(10):
        rnd = random.Random(700 + i)
        x0 = rnd.choice([-60, W + 60]) + rnd.randint(-80, 80)
        x1 = 640 + i * 70
        x = x0 + (x1 - x0) * k
        s += SL(Z_SRED, siluet(x, 1020 + rnd.randint(-10, 20), 250 * rnd.uniform(.85, 1.1),
                               "#1b1a24", .95, platok=(i % 3 == 0)))
    # край свитка разворачивается в кадре
    sv = A.out(A.seg(t, 1.6, 1.6))
    s += SL(Z_PERED, f'<path d="M-20,{H} V{H-260*sv:.0f} q220,{-40*sv:.0f} 440,{-6*sv:.0f}'
                     f' V{H} Z" fill="url(#list)" opacity="{.9*sv:.2f}" {o(5)}/>')
    s += SL(Z_PERED, f'<rect x="-20" y="{H-270*sv:.0f}" width="470" height="26" rx="12"'
                     f' fill="url(#med)" opacity="{sv:.2f}" {o(5)}/>')
    s += vinetka(.5)
    return s


def liven_nad_ploschadyu(t):
    """Площадь сверху: пламя разгорелось, из тучи бьёт ливень."""
    s = nebo("noch", t, False, 103)
    s += SL(Z_NEBO, f'<g opacity=".8">{_oblaka(t, 180, 4, 107, .9, "#4c5160", 5.0)}</g>')
    s += SL(Z_DAL, f'<path d="M-20,620 H900 V{H} H-20 Z" fill="#6a5c46" {o(7)}/>')
    # костёр в левой полосе: горит, потом гаснет под струями
    liv = A.ease(A.seg(t, 1.2, 1.6))
    zhiv = max(.05, 1 - liv)
    s += ten(420, 1000, 220, 26, .5)
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="410" y="840" width="24" height="170" rx="8" fill="url(#derev)" {o(5)}'
                        f' transform="rotate({-60+i*24} 422 1000)"/>')
    s += teplo(420, 880, 360 * zhiv + 60, 300 * zhiv + 60, .9 * zhiv)
    if zhiv > .15:
        s += ogon(420, 860, t, 1.6 * zhiv, .2, int(8 * zhiv) + 1)
    # пар столбом, когда вода бьёт в огонь
    s += par(420, 820, t, 6, .4 + .4 * liv, 420, .5, wide=1.6)
    # струи дождя
    for i in range(70):
        rnd = random.Random(800 + i)
        x = rnd.randint(-40, 900)
        ph = rnd.random()
        k = A.seg(t, ph * .5, .5)
        y = -60 + (H + 120) * k
        s += (f'<rect x="{x+14*k:.0f}" y="{y:.0f}" width="4" height="{56+20*rnd.random():.0f}"'
              f' fill="#b9d6ea" opacity="{.5*liv:.2f}" transform="rotate(8 {x} {y:.0f})"/>')
    # лужи расходятся кругами
    for i in range(5):
        ph = i * .4
        k = A.seg(t, ph, 1.4)
        s += SL(Z_SRED, f'<ellipse cx="{200+i*160}" cy="{1020+i%2*20}" rx="{40+90*k:.0f}"'
                        f' ry="{12+26*k:.0f}" fill="none" stroke="#9fc8dc"'
                        f' stroke-width="4" opacity="{.5*liv*(1-k):.2f}"/>')
    s += vinetka(.5)
    return s


def tolpa_pod_dozhdem(t):
    """Силуэты под дождём: огоньки загораются цепочкой, дождь редеет."""
    s = nebo("noch", t, False, 109)
    s += SL(Z_NEBO, f'<g opacity=".7">{_oblaka(t, 200, 4, 113, .8, "#4a505e", 6.0)}</g>')
    s += SL(Z_DAL, f'<path d="M-20,780 H{W+20} V{H} H-20 Z" fill="#5f5343" {o(7)}/>')
    red = A.ease(A.seg(t, .6, 2.4))
    cep = A.seg(t, .3, 2.6)
    s += tolpa_siluety(1030, t, 11, 17, 270, "#16151e", ogonki=cep)
    s += teplo(960, 820, 700 * cep, 240 * cep, .4 * cep)
    for i in range(60):
        rnd = random.Random(900 + i)
        x = rnd.randint(-40, W + 40)
        ph = rnd.random()
        k = A.seg(t, ph * .55, .55)
        y = -60 + (H + 120) * k
        s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="3" height="52" fill="#b9d6ea"'
              f' opacity="{.45*(1-red):.2f}" transform="rotate(7 {x} {y:.0f})"/>')
    s += f'<g opacity="{.4+.2*red:.2f}">{_tuman(t, 980, .4, "#8fa6b8")}</g>'
    s += vinetka(.5)
    return s


def dva_svetilnika(t):
    """Два глиняных светильника на полке: огоньки гаснут, идут два дымка."""
    s = f'<rect width="{W}" height="{H}" fill="#0f0d14"/>'
    s += SL(Z_DAL, kladka(-20, -20, W + 40, H + 40, 96, "url(#kamen)"))
    s += f'<rect width="{W}" height="{H}" fill="#0b0a10" opacity=".66"/>'
    gas = A.ease(A.seg(t, 1.6, .8))
    zhiv = 1 - gas
    s += teplo(960, 560, 620 * zhiv + 80, 420 * zhiv + 60, .8 * zhiv + .05)
    # каменная полка
    s += SL(Z_SRED, f'<rect x="520" y="640" width="880" height="42" rx="8" fill="#6b6152" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="520" y="682" width="880" height="16" fill="#473f34" opacity=".8"/>')
    for i, cx in enumerate((760, 1160)):
        s += ten(cx, 648, 90, 14, .5)
        s += SL(Z_SRED, f'<path d="M{cx-78},640 q78,-56 156,0 q-78,26 -156,0 Z" fill="url(#glina)" {o(6)}/>')
        s += SL(Z_SRED, f'<path d="M{cx+62},600 q34,6 40,30 q-30,6 -44,-14 Z" fill="url(#glina)" {o(5)}/>')
        if zhiv > .1:
            s += ogon(cx + 70, 596, t, .8 * zhiv, i * .5, 3)
        s += dym(cx + 70, 580, t, 5, .26, 420, .20 + .34 * gas, wide=1.1)
    # капля падает с карниза
    kp = A.seg(t, .4, 1.8)
    s += (f'<ellipse cx="420" cy="{200+760*kp:.0f}" rx="6" ry="12" fill="#bcd8ea"'
          f' opacity="{.7*(1-kp*.4):.2f}"/>')
    # звезда в проёме
    s += SL(Z_DAL, f'<rect x="1560" y="180" width="180" height="300" rx="10" fill="#131a2c" {o(6)}/>')
    s += SL(Z_DAL, f'<circle cx="1650" cy="300" r="{3.4+1.4*abs(A.w(t,.6)):.1f}" fill="#fff4de" opacity=".9"/>')
    s += vinetka(.6)
    return s


def porog_i_nit(t):
    """Порог крупно: нить выползает наружу, вдали два дымка."""
    s = nebo("sumer", t, True, 127)
    s += SL(Z_DAL, _ulica_dal(60, 560, 1800, t, True, 131))
    # два дымка вдали — от них остался только след
    for i, tx in enumerate((760, 1120)):
        s += SL(Z_DAL, dym(tx, 520, t, 4, .18, 300, .24, wide=1.2))
    s += f'<rect width="{W}" height="{H}" fill="#14131e" opacity=".3"/>'
    # сени: дверь покачивается
    s += SL(Z_SRED, brevna(-20, -20, 560, 900, 88))
    kach = 3.0 * A.w(t, .5)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.2f} 560 300)">{dver(380, 140, 300, 740, .25, "url(#derev)", True)}</g>')
    s += SL(Z_SRED, teplo(300, 600, 360, 420, .5))
    # порог крупным планом
    s += SL(Z_PERED, f'<path d="M-40,1080 V880 q960,-40 2000,0 V1080 Z" fill="url(#derev)" {o(8)}/>')
    s += SL(Z_PERED, f'<path d="M-40,900 q960,-40 2000,0 v26 q-1040,-40 -2000,0 Z" fill="#c0894f" opacity=".75"/>')
    for i in range(7):
        s += SL(Z_PERED, f'<path d="M{-40+i*300},{906+i%2*8} q140,-14 280,-4" stroke="#6d4a2a"'
                         f' stroke-width="4" fill="none" opacity=".5"/>')
    s += SL(Z_PERED, _sneg_lezhit(946, 12, "#dfe9f6"))
    # нить переползает порог и уходит вдаль
    s += nit_shepota([(260, 880), (640, 860), (1020, 780), (1360, 660), (1620, 580)], t, .95, sh=6.0)
    # снежинки влетают в сени
    for i in range(16):
        rnd = random.Random(1000 + i)
        ph = rnd.random() * 1.6
        k = A.seg(t, ph, 1.6)
        s += (f'<circle cx="{700-520*k:.0f}" cy="{420+260*k:.0f}" r="{rnd.uniform(2.2,4):.1f}"'
              f' fill="#f4f9ff" opacity="{.7*(1-k):.2f}"/>')
    s += vinetka(.48)
    return s


# ═══════════════════ 3. ЧЕТЫРЕ ЗАПРЕТА ═══════════════════
def platok_s_chetyrmya_uzelkami(t):
    """Клетчатый платок на столе, на углах затягиваются четыре узелка."""
    s = f'<rect width="{W}" height="{H}" fill="#8d7250"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 420, 86))
    s += SL(Z_SRED, f'<rect y="360" width="{W}" height="{H-360}" fill="url(#derev)" {o(8)}/>')
    s += SL(Z_SRED, doski(-20, 360, W + 40, H - 340, 150, False))
    s += teplo(760, 560, 820, 520, .75)
    # луч солнца ползёт по столу
    lx = 300 + 420 * A.ease(A.seg(t, 0, 6.0))
    s += SL(Z_SRED, f'<path d="M{lx:.0f},360 l260,0 l-150,720 l-300,0 Z" fill="{SVET}" opacity=".16"/>')
    # платок
    s += ten(880, 980, 520, 40, .4)
    s += SL(Z_SRED, f'<path d="M300,520 q580,-60 1180,0 q60,330 -20,460 q-560,70 -1140,0 q-70,-200 -20,-460 Z"'
                    f' fill="#d9cdb0" {o(7)}/>')
    for i in range(9):            # клетка
        s += SL(Z_SRED, f'<rect x="{320+i*130}" y="500" width="14" height="500" fill="#a4553f" opacity=".45"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="300" y="{540+i*100}" width="1180" height="14" fill="#a4553f" opacity=".45"/>')
    # четыре узелка затягиваются по очереди
    for i, (ux, uy) in enumerate(((330, 540), (1430, 540), (330, 960), (1430, 960))):
        k = A.out(A.seg(t, 1.4 + i * .55, .7))
        r = 54 - 24 * k
        s += SL(Z_SRED, f'<circle cx="{ux}" cy="{uy}" r="{r:.0f}" fill="#cbbd9c" {o(6)}/>'
                        f'<circle cx="{ux}" cy="{uy}" r="{r*.45:.0f}" fill="#9a8a68" opacity=".7"/>')
    # бахрома шевелится
    for i in range(16):
        kach = 6 * A.w(t, .7, i * .3)
        s += SL(Z_SRED, f'<path d="M{320+i*74},1000 q{kach:.0f},26 {kach*1.4:.0f},48"'
                        f' stroke="#cbbd9c" stroke-width="7" fill="none" opacity=".8"/>')
    s += vinetka(.44)
    return s


def dve_chashki_na_kuhonnom_stole(t):
    """Две чашки: пар-шёпот от одной к другой, блюдце обрывает его."""
    s = f'<rect width="{W}" height="{H}" fill="#9fa79e"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="620" fill="#b8bfb2" {o(7)}/>')
    for i in range(14):           # кафель на стене
        for j in range(4):
            s += SL(Z_DAL, f'<rect x="{i*140+6}" y="{j*150+6}" width="128" height="138" rx="6"'
                           f' fill="#c9cfc0" opacity="{.5 if (i+j)%2 else .3}"/>')
    s += SL(Z_SRED, f'<rect y="620" width="{W}" height="{H-620}" fill="url(#derev)" {o(8)}/>')
    s += teplo(820, 700, 760, 420, .6)
    nak = A.ease(A.seg(t, 2.6, 1.0))
    for i, cx in enumerate((620, 1080)):
        s += ten(cx, 880, 150, 24, .45)
        s += SL(Z_SRED, f'<path d="M{cx-120},700 q120,-26 240,0 l-34,190 q-86,30 -172,0 Z"'
                        f' fill="{KREM}" {o(7)}/>')
        s += SL(Z_SRED, f'<ellipse cx="{cx}" cy="700" rx="122" ry="30" fill="#6b4a32" {o(4)}/>')
        s += SL(Z_SRED, f'<path d="M{cx+118},740 q70,30 -6,96" stroke="{KREM}" stroke-width="26"'
                        f' fill="none" stroke-linecap="round"/>')
    # пар-шёпот от первой ко второй
    if nak < .5:
        s += nit_shepota([(620, 660), (760, 560), (900, 560), (1080, 650)], t, .55, "#e8f1f6", 4.0)
    s += par(1080, 650, t, 4, .45, 200, .4)
    # блюдце накрывает первую чашку
    s += SL(Z_SRED, f'<g transform="translate(0,{-300*(1-nak):.0f})" opacity="{nak:.2f}">'
                    f'<ellipse cx="620" cy="690" rx="140" ry="34" fill="{KREM}" {o(6)}/></g>')
    # ложечка ходит по кругу во второй
    a = (t * 70) % 360
    s += SL(Z_SRED, f'<g transform="rotate({a:.0f} 1080 700)">'
                    f'<rect x="1072" y="610" width="14" height="110" rx="6" fill="url(#zhel)" {o(4)}/></g>')
    s += SL(Z_PERED, _kvartira_veschi(1700, 1070, 420, t, 23))
    s += vinetka(.46)
    return s


def selo_sverhu_zimoy(t):
    """Село с высоты: улица, колодец, тропинка, дома связаны ниткой следов."""
    s = f'<rect width="{W}" height="{H}" fill="#dfe8f4"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="url(#sneg)" {o(0)}/>')
    s += f'<rect width="{W}" height="{H}" fill="#9fb4ce" opacity=".25"/>'
    # улица наискось
    s += SL(Z_SRED, f'<path d="M-40,760 q520,-150 1000,-220 q500,-70 1000,-180 l0,120'
                    f' q-520,110 -1000,180 q-480,70 -1000,220 Z" fill="#c2cfdf" {o(4)}/>')
    # дома сверху: крыши прямоугольниками с коньком
    rnd = random.Random(31)
    doma = []
    for i in range(11):
        x = 90 + i * 170 + rnd.randint(-30, 30)
        y = 300 + (i % 3) * 60 + (-140 if i % 2 else 210) + rnd.randint(-20, 20)
        doma.append((x, y))
        w_, h_ = 130, 96
        s += SL(Z_SRED, ten(x + 16, y + h_ + 14, w_ * .6, 16, .3))
        s += SL(Z_SRED, f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="6" fill="#8e5f3a" {o(6)}/>')
        s += SL(Z_SRED, f'<path d="M{x},{y+h_/2:.0f} h{w_}" stroke="#c9a173" stroke-width="8"/>')
        s += SL(Z_SRED, f'<rect x="{x}" y="{y}" width="{w_}" height="{h_*.42:.0f}" fill="url(#sneg)" opacity=".8"/>')
        s += SL(Z_SRED, f'<rect x="{x+w_*.7:.0f}" y="{y+h_*.2:.0f}" width="20" height="24" fill="#4b3827"/>')
        s += SL(Z_SRED, dym(x + w_ * .74, y + h_ * .2, t, 3, .18, 160, .22, wide=.8))
    # колодец точкой на улице
    kk = A.ease(A.seg(t, 1.2, 1.0))
    s += SL(Z_SRED, f'<circle cx="960" cy="560" r="{46*kk:.0f}" fill="#6d5842" {o(6)}/>'
                    f'<circle cx="960" cy="560" r="{26*kk:.0f}" fill="#20262e" opacity=".9"/>')
    # нитка следов связывает дома
    sl = A.seg(t, .4, 4.0)
    pts = doma[:max(2, int(len(doma) * sl))]
    if len(pts) > 1:
        d = "M%d,%d" % (pts[0][0] + 60, pts[0][1] + 110)
        for x, y in pts[1:]:
            d += " Q%d,%d %d,%d" % (x - 40, y + 190, x + 60, y + 110)
        s += SL(Z_SRED, f'<path d="{d}" fill="none" stroke="#8ba0bb" stroke-width="7"'
                        f' stroke-dasharray="16 20" opacity=".8"/>')
    # человечки идут к колодцу
    for i in range(3):
        k = A.seg(t, i * .7, 5.0)
        s += SL(Z_SRED, f'<circle cx="{300+660*k+i*40:.0f}" cy="{700-150*k:.0f}" r="13"'
                        f' fill="#36404f" opacity=".9"/>')
    s += sneg_letit(t, 30, 37, .55, .6)
    s += vinetka(.4)
    return s


def krylco_hozyaina(t):
    """Снежный ком-слово в человеческий рост подкатывается к крыльцу."""
    s = nebo("den", t, False, 41)
    s += SL(Z_DAL, _ulica_dal(60, 700, 1840, t, True, 43))
    s += SL(Z_SRED, izba_snaruzhi(1420, 1010, 900, t, True, True, 7))
    s += SL(Z_SRED, _sneg_lezhit(960, 24, "url(#sneg)"))
    # крыльцо
    s += SL(Z_SRED, f'<path d="M1180,1012 h480 v-44 h-480 Z" fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1210+i*26}" y="{968-i*50}" width="{420-i*52}" height="50"'
                        f' rx="6" fill="#8a6440" {o(5)}/>')
    # хозяин на пороге: чешет затылок, шапка сползает
    sh = A.ease(A.seg(t, 1.4, 1.4))
    s += SL(Z_SRED, figura(1420, 826, 420, t, "#2f2a2e", "#ffe3b0", False, .2, True))
    s += SL(Z_SRED, f'<rect x="{1376-12*sh:.0f}" y="{450+30*sh:.0f}" width="92" height="50" rx="16"'
                    f' fill="#6a3a34" {o(5)} transform="rotate({-9*sh:.0f} 1422 474)"/>')
    # ком-слово в рост человека
    k = A.ease(A.seg(t, .2, 2.4))
    kx = -200 + 1040 * k
    s += ten(kx, 1000, 180, 26, .45)
    s += SL(Z_SRED, f'<g transform="rotate({k*280:.0f} {kx:.0f} 830)">'
                    f'<circle cx="{kx:.0f}" cy="830" r="170" fill="#eef5ff" {o(7)}/>'
                    f'<circle cx="{kx-60:.0f}" cy="790" r="44" fill="#d8e4f2" opacity=".8"/>'
                    f'<circle cx="{kx+50:.0f}" cy="880" r="30" fill="#d8e4f2" opacity=".7"/>'
                    f'<path d="M{kx+120:.0f},780 l70,-40 M{kx+140:.0f},860 l80,20 M{kx-150:.0f},760 l-60,-40"'
                    f' stroke="#6d5236" stroke-width="10" stroke-linecap="round"/></g>')
    # ком осыпается
    for i in range(10):
        rnd = random.Random(50 + i)
        ph = rnd.random() * 1.2
        kk = A.seg(t, ph, 1.2)
        s += (f'<circle cx="{kx+rnd.randint(-160,160):.0f}" cy="{960+120*kk:.0f}"'
              f' r="{rnd.uniform(4,9):.0f}" fill="#f2f8ff" opacity="{.7*(1-kk):.2f}"/>')
    # собака пятится
    dx = -70 * A.ease(A.seg(t, 1.0, 1.6))
    s += SL(Z_SRED, f'<g transform="translate({dx:.0f},0)">'
                    f'<ellipse cx="820" cy="980" rx="70" ry="40" fill="#6b4c33" {o(5)}/>'
                    f'<circle cx="884" cy="944" r="34" fill="#6b4c33" {o(5)}/>'
                    f'<path d="M760,960 q-40,-20 -50,10 q30,20 50,6 Z" fill="#6b4c33" {o(4)}/></g>')
    s += sneg_letit(t, 22, 53, .4, .6)
    s += vinetka(.42)
    return s


def deti_v_ryad_na_brevne(t):
    """Шестеро детей на бревне шепчут по цепочке: кот превращается в самолёт."""
    s = nebo("den", t, False, 59)
    s += SL(Z_DAL, _ulica_dal(40, 720, 1840, t, False, 61))
    s += SL(Z_DAL, f'<path d="M-20,820 q500,-40 1000,-20 q500,20 960,-10 V{H} H-20 Z"'
                   f' fill="{TRAVA}" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="60" y="900" width="1800" height="70" rx="34" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<ellipse cx="60" cy="935" rx="26" ry="35" fill="#7d5636" {o(5)}/>')
    for i in range(6):
        cx = 260 + i * 290
        nak = 5 * A.w(t, .6, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({nak:.1f} {cx} 900)">'
                        f'{figura(cx, 900, 260, t, "#2a2733", "#ffe6bc", (i % 2 == 0), i * .3, True)}</g>')
        # ноги болтаются
        for lx in (-26, 26):
            s += SL(Z_SRED, f'<rect x="{cx+lx-10:.0f}" y="900" width="20" height="90" rx="9"'
                            f' fill="#2a2733" transform="rotate({12*A.w(t,1.2,i*.4+lx):.1f} {cx+lx} 900)"/>')
        # облачко над первым и последним
        if i in (0, 5):
            kk = A.seg(t, 0, 3.0)
            s += SL(Z_SRED, f'<ellipse cx="{cx}" cy="560" rx="120" ry="76" fill="#f4f7fb" {o(5)}/>')
            if i == 0:
                s += SL(Z_SRED, f'<g transform="translate({cx-50},520) scale(.7)">{kot(0, 60, t, 1.0, "#4a4038")}</g>')
            else:
                s += SL(Z_SRED, f'<path d="M{cx-70},560 l140,-30 l-30,34 l50,10 l-56,24 l-20,-26 Z"'
                                f' fill="#54607a" {o(4)}/>')
    # воробей скачет
    sx = 1500 + 120 * A.seg(t, 0, 2.2)
    s += SL(Z_SRED, ptica(sx, 880 - 30 * abs(A.w(t, 3.0)), t, .8, "#7d6b55"))
    s += vinetka(.42)
    return s


def dve_devochki_s_bantami(t):
    """Школьный двор: одна шепчет на ухо, у второй округляются глаза."""
    s = nebo("den", t, False, 67)
    s += SL(Z_DAL, _panelka(60, 700, 700, t, 5, True, 71))
    s += SL(Z_DAL, _panelka(1240, 680, 640, t, 5, True, 73))
    s += SL(Z_DAL, f'<rect y="820" width="{W}" height="{H-820}" fill="#9ba195" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M-20,900 q600,-30 1200,-10 q400,14 760,-6 V{H} H-20 Z" fill="#8d937f" {o(5)}/>')
    s += teplo(900, 500, 900, 520, .5)
    # две девочки
    s += figura(700, 1030, 520, t, "#33303c", "#ffe2b0", False, .0, True)
    s += figura(1120, 1030, 520, t, "#33303c", "#ffe2b0", False, .4, True)
    # банты подпрыгивают
    for cx, ph in ((700, .0), (1120, .4)):
        by = 1030 - 520 * .965 + 7 * A.w(t, 1.6, ph)
        for sgn in (-1, 1):
            bx = cx + sgn * 62
            s += (f'<path d="M{bx:.0f},{by:.0f} q{sgn*34:.0f},-30 {sgn*54:.0f},0'
                  f' q{-sgn*20:.0f},24 {-sgn*54:.0f},0 Z" fill="#b8323a" {o(5)}/>')
    # ладонь у уха: шепчет
    s += (f'<path d="M832,{1030-520*.78:.0f} q56,-30 92,8 q-50,32 -92,-8 Z" fill="#33303c"/>'
          f'<path d="M832,{1030-520*.78:.0f} q56,-30 92,8" stroke="#ffe2b0" stroke-width="5"'
          f' fill="none" opacity=".8"/>')
    # округлённые глаза второй
    gl = .5 + .5 * A.ease(A.seg(t, 1.6, .8))
    for dx in (34, 56):          # глаза в профиль: обе с правого края лица
        s += (f'<ellipse cx="{1120+dx}" cy="{1030-520*.855:.0f}" rx="{8+5*gl:.0f}" ry="{9+6*gl:.0f}"'
              f' fill="#f5efe2" opacity=".95"/>'
              f'<circle cx="{1120+dx+3}" cy="{1030-520*.855:.0f}" r="{4+2*gl:.0f}" fill="#20202a"/>')
    # листья летят, портфель падает
    for i in range(9):
        rnd = random.Random(80 + i)
        ph = rnd.random() * 2.6
        k = A.seg(t, ph, 2.6)
        s += (f'<path d="M{1700-1500*k:.0f},{300+420*k+60*A.w(t,.8,ph):.0f} q22,-16 40,2 q-20,18 -40,-2 Z"'
              f' fill="#c47a35" opacity="{.8*(1-k*.5):.2f}"/>')
    pf = A.seg(t, 2.2, .9)
    s += (f'<rect x="1300" y="{700+300*pf:.0f}" width="150" height="110" rx="12" fill="#6b4a2c" {o(6)}'
          f' transform="rotate({40*pf:.0f} 1375 {755+300*pf:.0f})"/>')
    s += vinetka(.44)
    return s


def myach_globus(t):
    """Мяч-глобус крутится на асфальте, лента шёпота облетает его."""
    s = nebo("den", t, False, 79)
    s += SL(Z_DAL, _panelka(1180, 700, 760, t, 5, True, 83))
    s += SL(Z_SRED, f'<rect y="700" width="{W}" height="{H-700}" fill="#8e928c" {o(6)}/>')
    s += SL(Z_SRED, f'<rect y="700" width="{W}" height="26" fill="#a4a89f" opacity=".6"/>')
    # мел на асфальте стирается
    st = 1 - A.ease(A.seg(t, 1.6, 2.4))
    s += SL(Z_SRED, f'<g opacity="{.5*st:.2f}"><path d="M300,980 h260 v-120 h-260 Z M560,980 h240 v-120 h-240 Z"'
                    f' fill="none" stroke="#e8e6dc" stroke-width="8"/></g>')
    # мяч-глобус
    a = (t * 150) % 360
    s += ten(760, 1000, 180, 26, .45)
    s += SL(Z_SRED, f'<circle cx="760" cy="840" r="170" fill="#4e86a8" {o(8)}/>')
    s += SL(Z_SRED, f'<g transform="rotate({a:.0f} 760 840)" opacity=".92">'
                    f'<path d="M660,760 q90,-40 170,10 q-50,70 -140,60 Z" fill="{ZEL2}"/>'
                    f'<path d="M700,900 q110,-20 180,40 q-120,50 -200,-10 Z" fill="{ZEL2}"/>'
                    f'<path d="M760,670 v340" stroke="#e8f2f8" stroke-width="5" opacity=".5"/>'
                    f'<ellipse cx="760" cy="840" rx="170" ry="60" fill="none" stroke="#e8f2f8"'
                    f' stroke-width="5" opacity=".5"/></g>')
    s += SL(Z_SRED, f'<circle cx="700" cy="780" r="60" fill="#ffffff" opacity=".18"/>')
    # лента шёпота облетает мяч, потом обматывает девочку
    ob = A.ease(A.seg(t, 2.6, 1.6))
    if ob < .5:
        s += nit_shepota([(560, 900), (700, 700), (920, 760), (980, 900), (760, 1000)], t, .8, sh=6)
    else:
        s += nit_shepota([(1320, 1000), (1420, 860), (1320, 740), (1240, 860), (1330, 980)], t, .85, sh=6)
    s += figura(1330, 1020, 460, t, "#33303c", "#ffe2b0", False, .2, True)
    for sgn in (-1, 1):
        bx = 1330 + sgn * 56
        by = 1020 - 460 * .965
        s += (f'<path d="M{bx:.0f},{by:.0f} q{sgn*30:.0f},-28 {sgn*48:.0f},0'
              f' q{-sgn*18:.0f},22 {-sgn*48:.0f},0 Z" fill="#b8323a" {o(5)}/>')
    s += vinetka(.44)
    return s


def lavochka_u_podezda(t):
    """Подъезд, лавочка с тремя бабушками, конвертики слетаются из окон."""
    s = nebo("den", t, False, 89)
    # всё главное в левой полосе: справа окно вставки
    s += SL(Z_DAL, _panelka(-40, 1010, 900, t, 5, True, 97))
    s += SL(Z_SRED, f'<rect y="1010" width="{W}" height="{H-1010}" fill="#8d918a" {o(5)}/>')
    s += teplo(380, 760, 520, 360, .45)
    # козырёк подъезда и дверь
    s += SL(Z_SRED, f'<rect x="140" y="640" width="420" height="30" rx="8" fill="#6d7079" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="220" y="670" width="260" height="350" rx="8" fill="#4a5a52" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="250" y="700" width="90" height="280" rx="6" fill="#9fc0cc" opacity=".55"/>')
    # мелом почтовый рожок
    s += SL(Z_SRED, f'<g opacity=".55" transform="translate(600,700) scale(.9)">'
                    f'<path d="M0,40 q60,-70 140,-20 q-20,60 -80,70 q-50,8 -60,-50 Z" fill="none"'
                    f' stroke="#eceade" stroke-width="7"/>'
                    f'<path d="M120,20 q40,-30 70,-6" stroke="#eceade" stroke-width="7" fill="none"/></g>')
    # лавочка и три бабушки
    s += SL(Z_SRED, f'<rect x="120" y="930" width="520" height="26" rx="10" fill="url(#derev)" {o(6)}/>')
    for i, cx in enumerate((220, 380, 540)):
        s += SL(Z_SRED, figura(cx, 930, 300, t, "#2f2c36", "#ffe0ae", True, i * .4, True))
    # конвертики слетаются из окон к лавочке
    for i in range(7):
        rnd = random.Random(300 + i)
        ph = rnd.random() * 2.2
        k = A.seg(t, ph, 2.2)
        x0, y0 = rnd.randint(60, 820), rnd.randint(120, 560)
        x1, y1 = 380 + rnd.randint(-120, 120), 900
        x = x0 + (x1 - x0) * k
        y = y0 + (y1 - y0) * k
        s += (f'<g transform="rotate({-20+40*k:.0f} {x:.0f} {y:.0f})" opacity="{.9*(1-k*.4):.2f}">'
              f'<rect x="{x-26:.0f}" y="{y-18:.0f}" width="52" height="36" rx="4" fill="#f2ecdc"/>'
              f'<path d="M{x-26:.0f},{y-18:.0f} l26,22 l26,-22" fill="none" stroke="#b9ab90" stroke-width="4"/></g>')
    # голуби клюют, бельё качается
    for i, gx in enumerate((700, 780)):
        s += SL(Z_SRED, f'<ellipse cx="{gx}" cy="{1030+4*A.w(t,2.0,i):.0f}" rx="30" ry="20"'
                        f' fill="#6f7a86" {o(4)}/><circle cx="{gx+26}" cy="{1014:.0f}" r="13" fill="#6f7a86"/>')
    for i in range(4):
        s += SL(Z_DAL, f'<path d="M{120+i*70},300 q20,{30+8*A.w(t,.6,i):.0f} 44,0 v70 q-24,26 -44,0 Z"'
                       f' fill="{"#d8dce4" if i%2 else "#cfa8a0"}" opacity=".8"/>')
    s += vinetka(.44)
    return s


def dvor_i_dvorec_v_odnoy_teni(t):
    """Тень подъезда вытягивается и становится тенью дворцовых арок."""
    s = f'<rect width="{W}" height="{H}" fill="#9ba097"/>'
    s += SL(Z_DAL, _panelka(-60, 760, 820, t, 4, False, 101))
    s += SL(Z_SRED, f'<rect y="760" width="{W}" height="{H-760}" fill="#8d918a" {o(6)}/>')
    k = A.ease(A.seg(t, .4, 2.6))
    # тень растёт вправо и превращается в арки
    s += SL(Z_SRED, f'<rect x="100" y="430" width="420" height="340" rx="10" fill="#6b7079" {o(6)}/>'
                    f'<rect x="190" y="500" width="230" height="270" rx="8" fill="#3e4d46" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M100,800 l{520+1000*k:.0f},0 l{-220-260*k:.0f},280 H40 Z"'
                    f' fill="#3f444d" opacity=".72"/>')
    for i in range(4):
        ax = 620 + i * 270 * k
        aw = 150 * k
        if k > .2:
            s += SL(Z_SRED, f'<path d="M{ax:.0f},1080 V{950-120*k:.0f} a{aw/2:.0f},{aw/2:.0f} 0 0 1 {aw:.0f},0'
                            f' V1080 Z" fill="#3b3f48" opacity="{.5*k:.2f}"/>')
    # два огонька загораются и гаснут в тени
    og = A.seg(t, 1.6, 1.4)
    if .2 < og < .8:
        for dx in (-40, 40):
            s += ogonek_grudi(900 + dx, 980, t, .9, dx * .01, .2)
    # лист катится по асфальту
    lx = -100 + 2100 * A.seg(t, .2, 3.4)
    s += (f'<g transform="rotate({lx*.6:.0f} {lx:.0f} 1030)">'
          f'<path d="M{lx-24:.0f},1030 q24,-24 48,2 q-24,22 -48,-2 Z" fill="#c07a34" {o(4)}/></g>')
    s += vinetka(.46)
    return s


def doschatyy_zabor_s_dyrkoy_ot_suchka(t):
    """Хозяйка с ведром идёт вдоль забора и затыкает дырку варежкой."""
    s = nebo("den", t, False, 103)
    s += SL(Z_DAL, _ulica_dal(60, 640, 1840, t, True, 107))
    # забор во весь кадр
    s += SL(Z_SRED, f'<rect y="440" width="{W}" height="520" fill="url(#dosk)" {o(8)}/>')
    for i in range(22):
        s += SL(Z_SRED, f'<rect x="{i*90}" y="440" width="82" height="520" fill="#8a6239"'
                        f' opacity="{.25 if i%2 else .1}"/>')
    s += SL(Z_SRED, f'<rect y="520" width="{W}" height="26" fill="#6d4a2a" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect y="840" width="{W}" height="26" fill="#6d4a2a" opacity=".5"/>')
    s += SL(Z_SRED, f'<path d="M-20,452 q240,-26 480,-6 q240,20 480,-8 q240,-24 480,4 q240,24 500,-8'
                    f' v26 q-260,28 -500,4 q-240,-24 -480,8 q-240,24 -480,-4 q-240,-26 -480,0 Z"'
                    f' fill="url(#sneg)" {o(4)}/>')
    s += SL(Z_PERED, f'<path d="M-20,1080 V980 q480,-40 960,-16 q480,24 980,-10 V1080 Z"'
                     f' fill="#eef4fc" {o(4)}/>')
    # дырка от сучка и луч из неё
    zat = A.ease(A.seg(t, 2.8, 1.0))
    if zat < .9:
        s += SL(Z_SRED, f'<ellipse cx="1180" cy="700" rx="26" ry="30" fill="#2a2016" opacity="{1-zat:.2f}"/>')
        s += SL(Z_SRED, f'<path d="M1180,700 l340,-120 l0,260 Z" fill="{SVET}" opacity="{.3*(1-zat):.2f}"/>')
    else:
        s += SL(Z_SRED, f'<path d="M1150,668 q30,-26 62,0 q10,40 -2,66 q-32,16 -60,-4 Z" fill="{TKAN}" {o(5)}/>')
    # хозяйка с ведром идёт вдоль забора
    k = A.seg(t, 0, 5.2)
    hx = 200 + 1100 * k
    s += figura(hx, 1010, 420, t, "#38333c", "#ffe2b0", True, .1, True)
    s += (f'<path d="M{hx+70:.0f},880 q36,10 30,46 l-8,70 q-30,14 -58,0 l-8,-70 q-6,-36 30,-46 Z"'
          f' fill="{ZHELEZ}" {o(5)}/>')
    s += par(hx + 10, 1010 - 420 * .86, t, 3, .4, 120, .35)
    # пёс зевает у будки
    s += SL(Z_SRED, f'<path d="M100,960 h230 l-30,-120 h-170 Z" fill="#6d4a2a" {o(6)}/>'
                    f'<circle cx="215" cy="900" r="46" fill="#2a2016" opacity=".9"/>')
    zev = A.seg(t, 1.2, 2.0)
    s += SL(Z_SRED, f'<ellipse cx="300" cy="946" rx="54" ry="32" fill="#5c4530" {o(4)}/>'
                    f'<ellipse cx="348" cy="{936+10*zev:.0f}" rx="26" ry="{16+14*zev:.0f}" fill="#4a3728" {o(4)}/>')
    # снег с забора осыпается
    for i in range(12):
        rnd = random.Random(400 + i)
        ph = rnd.random() * 1.8
        kk = A.seg(t, ph, 1.8)
        s += (f'<circle cx="{rnd.randint(60,1860)}" cy="{460+500*kk:.0f}" r="{rnd.uniform(3,6):.0f}"'
              f' fill="#f4f9ff" opacity="{.8*(1-kk):.2f}"/>')
    s += vinetka(.42)
    return s


def komnata_s_tremya_zaborami(t):
    """Городская комната: над тремя вещами по очереди вырастает штакетник."""
    s = f'<rect width="{W}" height="{H}" fill="#b6a68e"/>'
    for i in range(16):
        s += SL(Z_DAL, f'<rect x="{i*120}" width="112" height="{H}" fill="#c2b296"'
                       f' opacity="{.35 if i%2 else .15}"/>')
    s += SL(Z_SRED, f'<rect y="880" width="{W}" height="200" fill="url(#pol)" {o(7)}/>')
    s += SL(Z_SRED, polovicy(880, "url(#pol)"))
    s += teplo(960, 560, 900, 520, .5)
    # книжная полка с дисковым телефоном
    s += SL(Z_SRED, polka(120, 520, 420))
    s += SL(Z_SRED, f'<rect x="200" y="432" width="180" height="86" rx="12" fill="#2f3a44" {o(6)}/>'
                    f'<circle cx="290" cy="470" r="30" fill="#8fa6b4" {o(4)}/>')
    # окно с видом на лавочку
    vid = (f'<rect width="420" height="330" fill="#93a8bd"/>'
           f'<rect y="250" width="420" height="80" fill="#8d918a"/>'
           f'<rect x="140" y="212" width="160" height="12" rx="5" fill="#7a5636"/>'
           f'{siluet(190, 212, 90, "#3a3640", .9, platok=True)}')
    s += SL(Z_SRED, okno_izby(760, 300, 420, 330, t, vid, 0, False, True))
    # тюль
    s += SL(Z_SRED, zanaveska(748, 288, 330, 120, "#f0f2f4", t, 1))
    s += SL(Z_SRED, zanaveska(1072, 288, 330, 120, "#f0f2f4", t, -1))
    # диван с мобильным
    s += SL(Z_SRED, f'<rect x="1380" y="700" width="480" height="200" rx="24" fill="#5c6b5e" {o(7)}/>'
                    f'<rect x="1400" y="640" width="440" height="110" rx="20" fill="#6b7a6c" {o(6)}/>')
    ek = .55 + .45 * abs(A.w(t, 1.4))
    s += SL(Z_SRED, f'<rect x="1560" y="690" width="110" height="60" rx="10" fill="#1d232a" {o(5)}/>'
                    f'<rect x="1570" y="698" width="90" height="44" rx="6" fill="#9fd4e8" opacity="{ek:.2f}"/>')
    # штакетники вырастают по очереди
    for i, (zx, zy, zw) in enumerate(((180, 432, 240), (780, 290, 380), (1540, 660, 180))):
        k = A.out(A.seg(t, .6 + i * 1.6, .8))
        if k <= 0:
            continue
        for j in range(int(zw / 46) + 1):
            hh = (70 + 10 * (j % 2)) * k
            s += (f'<rect x="{zx+j*46}" y="{zy-hh:.0f}" width="26" height="{hh:.0f}" rx="5"'
                  f' fill="url(#derev)" {o(4)}/>')
        s += (f'<rect x="{zx-6}" y="{zy-46*k:.0f}" width="{zw+20}" height="12" rx="5"'
              f' fill="#7d5636" opacity="{k:.2f}"/>')
    s += SL(Z_PERED, _kvartira_veschi(1780, 1070, 300, t, 29))
    s += vinetka(.44)
    return s


def karman_fartuka(t):
    """Карман клетчатого фартука крупно: три бумажки падают внутрь."""
    s = f'<rect width="{W}" height="{H}" fill="#6f5b44"/>'
    s += teplo(960, 520, 900, 560, .6)
    # фартук во весь кадр
    s += SL(Z_SRED, f'<rect width="{W}" height="{H}" fill="#d6c9ab" {o(0)}/>')
    for i in range(13):
        dyh = 4 * A.w(t, .5, i * .2)
        s += SL(Z_SRED, f'<rect x="{i*150+dyh:.0f}" width="22" height="{H}" fill="#9c6f50" opacity=".4"/>')
    for i in range(8):
        s += SL(Z_SRED, f'<rect y="{i*140}" width="{W}" height="22" fill="#9c6f50" opacity=".4"/>')
    # карман
    s += SL(Z_PERED, f'<path d="M420,620 h1080 q30,300 -40,420 q-500,60 -1000,0 q-70,-120 -40,-420 Z"'
                     f' fill="#c6b795" {o(8)}/>')
    s += SL(Z_PERED, f'<path d="M420,620 h1080 l6,-26 h-1092 Z" fill="#a89573" {o(5)}/>')
    # три бумажки падают в карман
    znaki = ("градусник", "кольца", "монета")
    for i in range(3):
        k = A.ease(A.seg(t, .4 + i * .9, 1.1))
        bx = 620 + i * 340
        by = 120 + 520 * k
        rot = -16 + 26 * k + 10 * A.w(t, 1.2, i)
        s += (f'<g transform="rotate({rot:.0f} {bx} {by:.0f})" opacity="{1-.3*max(0,k-.85)*6:.2f}">'
              f'<rect x="{bx-80}" y="{by-56:.0f}" width="160" height="112" rx="10" fill="url(#list)" {o(6)}/>')
        if i == 0:
            s += (f'<rect x="{bx-8}" y="{by-36:.0f}" width="16" height="72" rx="8" fill="#b8323a" opacity=".8"/>'
                  f'<circle cx="{bx}" cy="{by+36:.0f}" r="16" fill="#b8323a" opacity=".8"/>')
        elif i == 1:
            s += (f'<circle cx="{bx-30}" cy="{by:.0f}" r="26" fill="none" stroke="url(#zol)" stroke-width="9"/>'
                  f'<circle cx="{bx+34}" cy="{by:.0f}" r="26" fill="none" stroke="url(#zol)" stroke-width="9"/>')
        else:
            s += f'<circle cx="{bx}" cy="{by:.0f}" r="34" fill="url(#med)" {o(4)}/>'
        s += "</g>"
    # пуговица застёгивается и блестит
    pg = A.out(A.seg(t, 3.6, .8))
    s += SL(Z_PERED, f'<circle cx="960" cy="{600+20*pg:.0f}" r="34" fill="url(#krem)" {o(6)}/>'
                     f'<circle cx="952" cy="{592+20*pg:.0f}" r="9" fill="#fff" opacity="{.4+.5*abs(A.w(t,1.6)):.2f}"/>')
    s += vinetka(.46)
    return s


def u_pochtovyh_yaschikov(t):
    """Ряд почтовых ящиков: вопрос-крючок распрямляется о ладонь."""
    s = f'<rect width="{W}" height="{H}" fill="#8e9790"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="620" fill="#9aa39b" {o(6)}/>')
    s += SL(Z_SRED, f'<rect y="900" width="{W}" height="{H-900}" fill="#6e756d" {o(6)}/>')
    s += teplo(1180, 420, 520, 420, .4)
    # стена ящиков
    for r in range(3):
        for c in range(6):
            x, y = 180 + c * 150, 330 + r * 130
            s += SL(Z_SRED, f'<rect x="{x}" y="{y}" width="130" height="110" rx="8" fill="#2f5a7a" {o(6)}/>'
                            f'<rect x="{x+10}" y="{y+16}" width="110" height="16" rx="6" fill="#16303f" opacity=".8"/>'
                            f'<circle cx="{x+108}" cy="{y+80}" r="8" fill="url(#zhel)" {o(3)}/>')
    # газета торчит
    s += SL(Z_SRED, f'<path d="M560,{356+8*A.w(t,.7):.0f} l120,-26 l10,40 l-120,26 Z" fill="#e6e2d6" {o(4)}/>')
    # лампочка мигает
    mg = .4 + .6 * (1 if abs(A.w(t, 2.2)) > .25 else .2)
    s += SL(Z_DAL, f'<circle cx="960" cy="140" r="34" fill="{SVET}" opacity="{mg:.2f}"/>'
                   f'<circle cx="960" cy="140" r="160" fill="url(#teplo)" opacity="{mg*.5:.2f}"/>')
    # две женщины: соседка с вопросом-крючком
    s += figura(1380, 1010, 520, t, "#333039", "#ffdfae", True, .2, True)
    s += figura(1620, 1015, 505, t, "#333039", "#ffdfae", False, .5, True)
    kr = A.ease(A.seg(t, .8, 1.2))
    if kr < 1:
        s += (f'<path d="M1380,{1010-520*.96:.0f} q{40-40*kr:.0f},{-60+30*kr:.0f} {70-20*kr:.0f},{-10:.0f}'
              f' q{20*(1-kr):.0f},{36*(1-kr):.0f} {-8*(1-kr):.0f},{40*(1-kr):.0f}"'
              f' fill="none" stroke="{SVET}" stroke-width="10" stroke-linecap="round" opacity=".9"/>')
    # ладонь мягко выставлена
    s += (f'<path d="M1520,{1015-505*.56:.0f} q50,-40 84,6 q-44,42 -84,-6 Z" fill="#333039"/>'
          f'<path d="M1520,{1015-505*.56:.0f} q50,-40 84,6" stroke="#ffdfae" stroke-width="5"'
          f' fill="none" opacity=".85"/>')
    # кот на батарее
    s += SL(Z_SRED, f'<rect x="120" y="760" width="300" height="140" rx="10" fill="#c9cdc6" {o(5)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{134+i*40}" y="770" width="22" height="120" rx="8" fill="#b4b9b1" {o(3)}/>')
    s += SL(Z_SRED, kot(270, 760, t, 1.2, "#4a4038", spit=True))
    s += vinetka(.46)
    return s


def iskra_v_ladonyah(t):
    """Слово-искра влетает в фонарь и становится ровным тёплым огоньком.
    Рук в кадре нет (правило 05.11): предмет работает сам."""
    s = f'<rect width="{W}" height="{H}" fill="#16131c"/>'
    s += SL(Z_DAL, kladka(-20, -20, W + 40, H + 40, 96, "url(#kamen)"))
    s += f'<rect width="{W}" height="{H}" fill="#120f18" opacity=".66"/>'
    k = A.ease(A.seg(t, .3, 1.8))
    cx, cy = 900, 600
    s += teplo(cx, cy, 380 + 260 * k, 340 + 200 * k, .4 + .45 * k)
    # стол и фонарь
    s += SL(Z_SRED, f'<rect y="900" width="{W}" height="{H-900}" fill="url(#derev)" {o(7)}/>')
    s += ten(cx, 910, 190, 24, .5)
    s += SL(Z_SRED, f'<path d="M{cx-120},900 h240 l-26,-50 h-188 Z" fill="url(#zhel)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{cx-110}" y="430" width="220" height="420" rx="14"'
                    f' fill="#bcd8e8" opacity=".30" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{cx-130},430 h260 l-40,-70 h-180 Z" fill="url(#zhel)" {o(6)}/>'
                    f'<rect x="{cx-14}" y="300" width="28" height="64" rx="10" fill="url(#zhel)" {o(4)}/>'
                    f'<path d="M{cx-14},300 q14,-40 28,0" fill="none" stroke="url(#zhel)" stroke-width="12"/>')
    # искра: мечется снаружи, потом ровно горит внутри
    if k < .92:
        jx = cx + (1 - k) * 520 * A.w(t, 2.6)
        jy = cy - 240 * (1 - k) + (1 - k) * 200 * A.w(t, 3.3, .3)
        s += ogonek_grudi(jx, jy, t, .9, .0, .1)
        s += nit_shepota([(jx - 180, jy + 90), (jx - 60, jy + 20), (jx, jy)], t, .5, sh=3.5)
    else:
        s += ogon(cx, 790, t, 1.15, .0, 4)
        s += ogonek_grudi(cx, 700, t, 1.5, .0, 1.0)
    # свет ложится на кладку и на стол
    s += SL(Z_SRED, f'<ellipse cx="{cx}" cy="930" rx="{300*k+90:.0f}" ry="60"'
                    f' fill="url(#teplo)" opacity="{.5*k+.1:.2f}"/>')
    s += f'<g opacity=".4">{par(cx, 420, t, 3, .35, 200, .3)}</g>'
    s += vinetka(.56)
    return s


def dva_doma_naprotiv_na_zakate(t):
    """Два дома через улицу, между ними ложится длинная тень, садится солнце."""
    s = nebo("zakat", t, False, 109)
    k = A.ease(A.seg(t, 0, 5.0))
    s += SL(Z_NEBO, f'<circle cx="960" cy="{520+120*k:.0f}" r="260" fill="url(#teplo)" opacity=".7"/>')
    s += SL(Z_NEBO, f'<circle cx="960" cy="{520+120*k:.0f}" r="92" fill="#ffcf84" opacity=".95"/>')
    s += SL(Z_DAL, f'<path d="M-20,860 H{W+20} V{H} H-20 Z" fill="#7a6e5c" {o(6)}/>')
    s += SL(Z_SRED, izba_snaruzhi(120, 1010, 700, t, True, True, 11))
    s += SL(Z_SRED, izba_snaruzhi(1800, 1010, 740, t, True, True, 13))
    # длинная тень между домами
    s += SL(Z_SRED, f'<path d="M520,1080 q440,{-120-80*k:.0f} 880,0 Z" fill="#2e2b3a"'
                    f' opacity="{.35+.3*k:.2f}"/>')
    # по силуэту в окнах
    for cx, cy in ((300, 760), (1620, 740)):
        s += SL(Z_SRED, f'<g opacity=".8">{siluet(cx, cy, 120, "#2a2430", .9)}</g>')
    s += sneg_letit(t, 16, 59, .3, .5)
    s += vinetka(.46)
    return s


def hodiki_s_nebom(t):
    """Ходики: вместо цифр полоска неба, стрелка пробегает светлую дольку."""
    s = f'<rect width="{W}" height="{H}" fill="#7d6a52"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 92))
    s += f'<rect width="{W}" height="{H}" fill="#2b2016" opacity=".3"/>'
    s += teplo(460, 480, 560, 460, .55)
    # корпус ходиков в левой полосе (справа окно вставки)
    cx, cy, R = 430, 470, 260
    s += ten(cx, 980, 230, 26, .4)
    s += SL(Z_SRED, f'<rect x="{cx-280}" y="{cy-300}" width="560" height="640" rx="28" fill="url(#derev)" {o(8)}/>')
    s += SL(Z_SRED, f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#f2ead6" {o(7)}/>')
    # на циферблате — небо: светлая долька и синяя часть
    s += SL(Z_SRED, f'<path d="M{cx},{cy} L{cx+R},{cy} A{R},{R} 0 0 1 {cx+R*0.5:.0f},{cy+R*0.87:.0f} Z"'
                    f' fill="#f6d79a" opacity=".9"/>')
    s += SL(Z_SRED, f'<path d="M{cx},{cy} L{cx+R*0.5:.0f},{cy+R*0.87:.0f} A{R},{R} 0 1 1 {cx+R},{cy} Z"'
                    f' fill="#4a6690" opacity=".85"/>')
    for i in range(12):
        a = math.radians(i * 30)
        s += SL(Z_SRED, f'<circle cx="{cx+math.cos(a)*R*0.86:.0f}" cy="{cy+math.sin(a)*R*0.86:.0f}"'
                        f' r="6" fill="#f6efdc" opacity=".7"/>')
    # стрелка бежит
    a = -90 + (t * 46) % 360
    s += SL(Z_SRED, f'<g transform="rotate({a:.0f} {cx} {cy})">'
                    f'<rect x="{cx-8}" y="{cy-R*0.8:.0f}" width="16" height="{R*0.8:.0f}" rx="7"'
                    f' fill="#2e2a24" {o(4)}/></g>')
    s += SL(Z_SRED, f'<circle cx="{cx}" cy="{cy}" r="16" fill="#2e2a24"/>')
    # маятник и гирька
    mk = 12 * A.w(t, .9)
    s += SL(Z_SRED, f'<g transform="rotate({mk:.1f} {cx} {cy+300})">'
                    f'<rect x="{cx-6}" y="{cy+300}" width="12" height="300" fill="url(#zhel)" {o(3)}/>'
                    f'<circle cx="{cx}" cy="{cy+620}" r="46" fill="url(#zol)" {o(5)}/></g>')
    gk = A.seg(t, 0, 8.0)
    s += SL(Z_SRED, f'<rect x="{cx+200}" y="{cy+300+80*gk:.0f}" width="36" height="120" rx="12"'
                    f' fill="url(#chug)" {o(4)}/>')
    # кукушка выглядывает
    ku = A.out(A.seg(t, 2.4, .9))
    if ku > .05:
        s += SL(Z_SRED, f'<g transform="translate({40*ku:.0f},0)" opacity="{ku:.2f}">'
                        f'<ellipse cx="{cx+10}" cy="{cy-260}" rx="34" ry="26" fill="#9a6b3e" {o(4)}/>'
                        f'<path d="M{cx+44},{cy-262} l34,10 l-34,10 Z" fill="url(#zol)"/></g>')
    s += vinetka(.46)
    return s


def kreslo_u_torshera(t):
    """Человек с газетой поглядывает на дверь, синяя тень накрывает кресло."""
    s = f'<rect width="{W}" height="{H}" fill="#8e7f6a"/>'
    for i in range(15):
        s += SL(Z_DAL, f'<rect x="{i*130}" width="118" height="{H}" fill="#9c8d75"'
                       f' opacity="{.3 if i%2 else .12}"/>')
    s += SL(Z_SRED, polovicy(900, "url(#pol)"))
    s += teplo(1320, 520, 460, 420, .6)
    # торшер загорается сам
    tr = A.ease(A.seg(t, 1.8, .8))
    s += SL(Z_SRED, f'<rect x="1412" y="560" width="16" height="420" fill="url(#zhel)" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M1320,560 h200 l-40,-130 h-120 Z" fill="#c9a06a" {o(6)}/>')
    s += SL(Z_SRED, f'<circle cx="1420" cy="560" r="{200*tr:.0f}" fill="url(#teplo)" opacity="{.7*tr:.2f}"/>')
    # кресло
    s += ten(900, 1000, 300, 28, .45)
    s += SL(Z_SRED, f'<rect x="640" y="640" width="520" height="340" rx="36" fill="#5f4a52" {o(8)}/>'
                    f'<rect x="600" y="700" width="90" height="280" rx="26" fill="#6d5660" {o(6)}/>'
                    f'<rect x="1110" y="700" width="90" height="280" rx="26" fill="#6d5660" {o(6)}/>')
    s += figura(900, 940, 400, t, "#312b33", "#ffd9a0", False, .1, True)
    # газета шуршит, человек поглядывает на дверь
    gl = A.seg(t, .6, 2.6)
    down = 1.0 if gl < .45 else .45
    s += (f'<g transform="rotate({-6+10*down:.0f} 900 760)">'
          f'<rect x="740" y="{700+40*(1-down):.0f}" width="320" height="230" rx="10"'
          f' fill="#e8e2d2" {o(6)}/>'
          f'<path d="M760,{740+40*(1-down):.0f} h280 M760,{780+40*(1-down):.0f} h240"'
          f' stroke="#9a9280" stroke-width="6"/></g>')
    # дверь
    s += SL(Z_SRED, dver(180, 300, 300, 680, 0, "url(#derev)", cepochka=True))
    # синяя тень ползёт по полу и накрывает кресло
    pk = A.ease(A.seg(t, .4, 4.4))
    s += SL(Z_SRED, f'<path d="M-20,1080 V{980-120*pk:.0f} q{700*pk:.0f},-60 {1500*pk:.0f},40 V1080 Z"'
                    f' fill="#2c3a58" opacity="{.25+.25*pk:.2f}"/>')
    s += vinetka(.46)
    return s


def pesochnica_dva_mizinca(t):
    """Двор, песочница: двое детей стоят рядом и качают сцепленными руками
    на слова присказки. Анатомии рук нет — только линия жеста."""
    s = nebo("den", t, False, 113)
    s += SL(Z_DAL, _panelka(-20, 620, 820, t, 5, False, 127))
    s += SL(Z_SRED, f'<rect y="620" width="{W}" height="{H-620}" fill="#9aa08f" {o(5)}/>')
    # песочница
    s += SL(Z_SRED, f'<rect x="60" y="860" width="640" height="150" rx="14" fill="#c9a96f" {o(7)}/>'
                    f'<rect x="40" y="836" width="680" height="40" rx="12" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="380" y="{862+8*A.w(t,.5):.0f}" width="24" height="120" rx="8"'
                    f' fill="#b8323a" {o(4)} transform="rotate(24 392 920)"/>'
                    f'<path d="M406,982 q56,-28 90,10 q-38,42 -90,-10 Z" fill="#b8323a" {o(4)}/>')
    # качели скрипят
    sk = 9 * A.w(t, .7)
    s += SL(Z_DAL, f'<g transform="rotate({sk:.1f} 1700 400)">'
                   f'<rect x="1620" y="400" width="12" height="330" fill="url(#zhel)" {o(3)}/>'
                   f'<rect x="1770" y="400" width="12" height="330" fill="url(#zhel)" {o(3)}/>'
                   f'<rect x="1600" y="730" width="200" height="26" rx="8" fill="url(#derev)" {o(5)}/></g>')
    # двое детей рядом, сцепленные руки качаются на присказку
    kach = 16 * A.w(t, 1.25)
    ub = A.ease(A.seg(t, 6.0, 1.8))
    sdv = 700 * ub
    for i, cx in enumerate((900, 1180)):
        s += figura(cx + sdv * (1 if i else .8), 1020, 470, t, "#33303c", "#ffe2b0",
                    (i == 1), i * .3, True, 1 - .35 * ub)
    if ub < .35:
        x1, x2 = 900 + 86, 1180 - 86
        ym = 1020 - 470 * .56
        s += (f'<path d="M{x1},{ym:.0f} q{(x2-x1)/2:.0f},{60+kach:.0f} {x2-x1},0"'
              f' fill="none" stroke="#33303c" stroke-width="26" stroke-linecap="round"/>')
        s += (f'<path d="M{x1},{ym:.0f} q{(x2-x1)/2:.0f},{60+kach:.0f} {x2-x1},0"'
              f' fill="none" stroke="#ffe2b0" stroke-width="6" opacity=".6"'
              f' stroke-linecap="round"/>')
    # песок сыплется
    for i in range(14):
        rnd = random.Random(500 + i)
        ph = rnd.random() * 1.4
        k = A.seg(t, ph, 1.4)
        s += (f'<rect x="{rnd.randint(120,680)}" y="{700+240*k:.0f}" width="4" height="12"'
              f' fill="#d8b87a" opacity="{.7*(1-k):.2f}"/>')
    s += vinetka(.44)
    return s


def avtobusnaya_ostanovka_dvoe(t):
    """Остановка: двое смотрят в разные стороны, на плечах надутые индюки."""
    s = nebo("sumer", t, False, 131)
    s += SL(Z_DAL, _ulica_dal(60, 700, 1840, t, True, 137))
    s += SL(Z_SRED, f'<rect y="900" width="{W}" height="{H-900}" fill="#767c74" {o(5)}/>')
    # навес остановки
    s += SL(Z_SRED, f'<rect x="240" y="300" width="1440" height="40" rx="10" fill="#4e5a62" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="260" y="340" width="40" height="600" fill="#4e5a62" {o(6)}/>'
                    f'<rect x="1620" y="340" width="40" height="600" fill="#4e5a62" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="340" width="1320" height="560" fill="#9fc2d2" opacity=".2"/>')
    # расписание хлопает
    hl = 7 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<g transform="rotate({hl:.1f} 1660 480)">'
                    f'<rect x="1640" y="420" width="130" height="180" rx="8" fill="#e6e2d4" {o(5)}/>'
                    f'<path d="M1656,460 h90 M1656,492 h90 M1656,524 h70" stroke="#9a9280" stroke-width="6"/></g>')
    # двое спиной к спине... нет: рядом, смотрят в разные стороны
    s += figura(760, 1010, 540, t, "#2f2c36", "#e8cf9a", False, .0, True)
    s += figura(1120, 1012, 530, t, "#2f2c36", "#e8cf9a", True, .4, True)
    # индюки на плечах надуваются
    for i, (cx, ph) in enumerate(((760, .0), (1120, .5))):
        nad = .7 + .5 * abs(A.w(t, .8, ph))
        oy = 1010 - 540 * .70
        s += (f'<g transform="translate({cx+70*(1 if i else -1):.0f},{oy:.0f}) scale({nad:.2f})">'
              f'<ellipse cx="0" cy="0" rx="58" ry="46" fill="#6a4458" {o(6)}/>'
              f'<circle cx="34" cy="-30" r="22" fill="#6a4458" {o(5)}/>'
              f'<path d="M50,-30 l28,6 l-28,10 Z" fill="url(#zol)"/>'
              f'<path d="M44,-16 q14,22 -4,30" stroke="#b8323a" stroke-width="7" fill="none"/>'
              f'<path d="M-50,-10 q-40,-40 -70,0 q36,16 70,14 Z" fill="#8a5a70" opacity=".9"/></g>')
    # ветер треплет шарфы
    for i, cx in enumerate((760, 1120)):
        sh = 40 * A.w(t, 1.1, i * .4)
        s += (f'<path d="M{cx-30},{1010-540*.66:.0f} q{60+sh:.0f},40 {20+sh:.0f},150'
              f' q-40,10 -50,-20 Z" fill="#b8323a" opacity=".85"/>')
    s += sneg_letit(t, 20, 139, .35, .6)
    s += vinetka(.46)
    return s


def podokonnik_s_telefonom_i_fialkami(t):
    """Дисковый телефон у фиалок, за окном сужается полоска заката."""
    s = f'<rect width="{W}" height="{H}" fill="#7f6b54"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#8d7a60" {o(0)}/>')
    # окно во всю стену
    zk = 1 - A.ease(A.seg(t, .6, 4.2))
    vid = (f'<rect width="1180" height="560" fill="#2e3a58"/>'
           f'<rect y="{430-120*zk:.0f}" width="1180" height="{140*zk+20:.0f}" fill="#e8945a" opacity=".9"/>'
           f'<rect y="{560-80*zk:.0f}" width="1180" height="90" fill="#8a5a3a" opacity=".7"/>')
    s += SL(Z_SRED, okno_izby(360, 140, 1180, 560, t, vid, 0, False, True))
    # подоконник
    s += SL(Z_SRED, f'<rect x="300" y="700" width="1300" height="46" rx="10" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="746" width="1300" height="20" fill="#6d4a2a" opacity=".6"/>')
    s += teplo(900, 700, 700, 420, .5)
    # фиалки
    for i, fx in enumerate((440, 600)):
        s += SL(Z_SRED, f'<path d="M{fx-50},700 h100 l-14,-76 h-72 Z" fill="url(#glina)" {o(5)}/>')
        for j in range(5):
            a = -150 + j * 44 + 5 * A.w(t, .5, i + j * .3)
            s += SL(Z_SRED, f'<ellipse cx="{fx+math.cos(math.radians(a))*44:.0f}"'
                            f' cy="{600+math.sin(math.radians(a))*30:.0f}" rx="26" ry="20"'
                            f' fill="{"#7a4a86" if j%2 else "#9a5fa6"}" {o(3)}/>')
        s += SL(Z_SRED, f'<circle cx="{fx}" cy="600" r="14" fill="url(#zol)" {o(2)}/>')
    # дисковый телефон
    s += ten(1120, 720, 160, 18, .4)
    s += SL(Z_SRED, f'<path d="M940,700 h360 q24,-96 -36,-120 h-288 q-60,24 -36,120 Z" fill="#2f3a44" {o(8)}/>')
    a = (t * 90) % 360 if t < 3.4 else 0
    s += SL(Z_SRED, f'<g transform="rotate({a:.0f} 1120 630)">'
                    f'<circle cx="1120" cy="630" r="72" fill="#8fa6b4" {o(5)}/>')
    for i in range(10):
        ang = math.radians(i * 36)
        s += SL(Z_SRED, f'<circle cx="{1120+math.cos(ang)*52:.0f}" cy="{630+math.sin(ang)*52:.0f}"'
                        f' r="12" fill="#2f3a44" opacity=".9"/>')
    s += SL(Z_SRED, "</g>")
    # трубка снята, шнур качается
    s += SL(Z_SRED, f'<rect x="980" y="548" width="280" height="44" rx="20" fill="#1f272e" {o(5)}'
                    f' transform="rotate(-8 1120 570)"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{960+i*34}" cy="{780+26*A.w(t,.8,i*.3):.0f}" r="16" fill="none"'
                        f' stroke="#1f272e" stroke-width="9" opacity=".8"/>')
    s += SL(Z_PERED, _kvartira_veschi(120, 1070, 420, t, 41))
    s += vinetka(.46)
    return s


def provod_mezhdu_dvumya_oknami(t):
    """Вечерняя улица: по проводу от окна к окну бегут два огонька-слова."""
    s = nebo("sumer", t, True, 149)
    s += SL(Z_DAL, _panelka(-60, 1010, 760, t, 5, True, 151))
    s += SL(Z_DAL, _panelka(1240, 1010, 800, t, 5, True, 157))
    s += SL(Z_SRED, f'<rect y="1010" width="{W}" height="{H-1010}" fill="#6e756d" {o(5)}/>')
    # провод качается
    sag = 120 + 18 * A.w(t, .5)
    d = f"M240,420 q720,{sag:.0f} 1440,0"
    s += SL(Z_SRED, f'<path d="{d}" fill="none" stroke="#2a2d33" stroke-width="7"/>')
    # дальнее окно загорается, в нём силуэт с трубкой
    zg = A.ease(A.seg(t, 2.2, 1.0))
    s += SL(Z_DAL, f'<rect x="1430" y="430" width="230" height="200" rx="8" fill="{SVET}"'
                   f' opacity="{.25+.6*zg:.2f}" {o(5)}/>')
    s += SL(Z_DAL, f'<g opacity="{.5+.5*zg:.2f}">{siluet(1545, 630, 180, "#3a3038", .95)}</g>')
    s += SL(Z_DAL, f'<path d="M1590,540 q34,-16 30,22" stroke="#3a3038" stroke-width="18"'
                   f' fill="none" opacity="{.5+.5*zg:.2f}"/>')
    # ближнее окно
    s += SL(Z_DAL, f'<rect x="260" y="470" width="220" height="190" rx="8" fill="{SVET}"'
                   f' opacity=".55" {o(5)}/>')
    s += SL(Z_DAL, f'<g opacity=".85">{siluet(370, 660, 170, "#3a3038", .95, platok=True)}</g>')
    # два огонька бегут по проводу
    for i in range(2):
        k = A.seg(t, i * .5, 2.6)
        x = 240 + 1440 * k
        y = 420 + sag * math.sin(math.pi * k) * .55
        s += ogonek_grudi(x, y, t, .55, i * .4, .25)
    # воробьи взлетают
    for i in range(4):
        vz = A.seg(t, 1.4 + i * .2, 1.6)
        s += SL(Z_SRED, ptica(620 + i * 170, 420 - 260 * vz + 30 * A.w(t, 2.0, i), t, .6, "#6b6356"))
    s += sneg_letit(t, 16, 163, .3, .5)
    s += vinetka(.46)
    return s


def ruki_s_mobilnym_pod_pledom(t):
    """Плед, под ним светится экран; строчка улетает бумажной птичкой."""
    s = f'<rect width="{W}" height="{H}" fill="#2a2029"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#352a33" {o(0)}/>')
    s += teplo(780, 760, 620, 420, .6)
    # диван и плед
    s += SL(Z_SRED, f'<rect y="700" width="{W}" height="{H-700}" fill="#4e3f4a" {o(7)}/>')
    dyh = 10 * A.w(t, .45)
    s += SL(Z_SRED, f'<ellipse cx="340" cy="800" rx="230" ry="110" fill="#e8dcc8" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M160,{880+dyh:.0f} q300,-180 760,-70 q360,52 1000,20 V1080 H160 Z"'
                    f' fill="#9a5a4a" {o(8)}/>')
    for i in range(10):
        s += SL(Z_SRED, f'<rect x="{180+i*180}" y="{820+dyh:.0f}" width="22" height="260"'
                        f' fill="#6d3a32" opacity=".5"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="160" y="{900+i*70+dyh:.0f}" width="1760" height="20"'
                        f' fill="#6d3a32" opacity=".5"/>')
    # экран виден сбоку из-под пледа
    ek = .6 + .4 * abs(A.w(t, 1.6))
    s += SL(Z_SRED, f'<g transform="rotate(-12 820 820)">'
                    f'<rect x="700" y="760" width="240" height="130" rx="16" fill="#1d232a" {o(6)}/>'
                    f'<rect x="716" y="774" width="208" height="100" rx="8" fill="#a8dcf0"'
                    f' opacity="{ek:.2f}"/></g>')
    s += SL(Z_SRED, f'<ellipse cx="820" cy="790" rx="260" ry="180" fill="url(#teplo)" opacity=".4"/>')
    # строчка отрывается и складывается в птичку
    k = A.ease(A.seg(t, .5, 2.0))
    bx = 820 + 900 * k
    by = 790 - 520 * k
    if k < .35:
        s += (f'<rect x="{bx-70:.0f}" y="{by:.0f}" width="140" height="18" rx="8"'
              f' fill="#dff0fa" opacity="{.9-k:.2f}"/>')
    else:
        rot = -18 + 30 * A.w(t, 1.4)
        s += (f'<g transform="rotate({rot:.0f} {bx:.0f} {by:.0f})">'
              f'<path d="M{bx-60:.0f},{by:.0f} l120,-34 l-30,40 l40,14 l-130,26 Z"'
              f' fill="#eef6fc" {o(4)}/></g>')
    # форточка и пар от чашки
    s += SL(Z_DAL, f'<rect x="1480" y="120" width="330" height="420" rx="10" fill="#1e2a40" {o(7)}/>'
                   f'<rect x="1500" y="140" width="290" height="180" rx="6" fill="#2d3c58" opacity=".9"/>')
    s += SL(Z_SRED, krynka(360, 780, .9))
    s += par(378, 710, t, 4, .5, 200, .45)
    s += vinetka(.5)
    return s


def lopata_v_sugrobe(t):
    """Лопата в сугробе, недочищенная дорожка, на черенке растёт шапочка."""
    s = nebo("sumer", t, True, 167)
    s += SL(Z_DAL, _ulica_dal(60, 720, 1840, t, True, 173))
    # фонарь загорается
    fz = A.ease(A.seg(t, 1.0, .9))
    s += SL(Z_SRED, f'<rect x="1540" y="300" width="18" height="700" fill="#3a4049" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1480,300 h140 l-28,-60 h-84 Z" fill="#4a525c" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="1550" cy="300" r="{220*fz:.0f}" fill="url(#teplo)" opacity="{.6*fz:.2f}"/>')
    # снег и дорожка
    s += SL(Z_SRED, f'<path d="M-20,1080 V900 q520,-70 980,-40 q500,30 960,-30 V1080 Z"'
                    f' fill="#eaf2fc" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M160,1080 q300,-150 520,-170 q180,-16 300,-10 l0,40'
                    f' q-200,10 -320,30 q-240,40 -420,110 Z" fill="#c3d2e4" {o(4)}/>')
    # сугроб и лопата
    s += SL(Z_SRED, f'<path d="M700,960 q180,-120 360,-10 q-180,70 -360,10 Z" fill="#f2f8ff" {o(6)}/>')
    s += SL(Z_SRED, f'<g transform="rotate(-18 880 940)">'
                    f'<rect x="866" y="520" width="30" height="420" rx="10" fill="url(#derev)" {o(5)}/>'
                    f'<path d="M820,930 h120 l-14,110 h-92 Z" fill="{ZHELEZ}" {o(6)}/></g>')
    # снежная шапочка на черенке растёт
    sh = A.ease(A.seg(t, .4, 3.0))
    s += SL(Z_SRED, f'<ellipse cx="{824:.0f}" cy="{520:.0f}" rx="{20+26*sh:.0f}" ry="{12+18*sh:.0f}"'
                    f' fill="#ffffff" {o(4)}/>')
    s += sneg_letit(t, 44, 179, .75, .9)
    s += SL(Z_PERED, f'<path d="M-20,1080 V1020 q300,-40 640,-10 V1080 Z" fill="#dce8f6" {o(4)}/>')
    s += vinetka(.46)
    return s


def tropinka_s_meshkom(t):
    """Человек с мешком на обледенелой тропинке, над поясницей зигзаг."""
    s = nebo("noch", t, True, 181)
    s += SL(Z_DAL, _ulica_dal(40, 700, 1860, t, True, 191))
    # фонарь мигает
    mg = .35 + .65 * (1 if abs(A.w(t, 2.4)) > .3 else .25)
    s += SL(Z_SRED, f'<rect x="300" y="260" width="16" height="660" fill="#3a4049" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="308" cy="250" r="{200*mg:.0f}" fill="url(#teplo)" opacity="{.55*mg:.2f}"/>')
    # тропинка с ледком
    s += SL(Z_SRED, f'<path d="M-20,1080 V920 q520,-60 980,-30 q500,26 960,-26 V1080 Z"'
                    f' fill="#e4eefa" {o(5)}/>')
    for i in range(7):
        bl = .25 + .35 * abs(A.w(t, 1.2, i * .4))
        s += SL(Z_SRED, f'<ellipse cx="{260+i*220}" cy="{990+i%3*22}" rx="90" ry="18"'
                        f' fill="#9fc8dc" opacity="{bl:.2f}"/>')
    # человек с мешком, нога скользит
    sk = A.seg(t, 1.6, 1.4)
    nak = -8 * math.sin(math.pi * sk)
    s += (f'<g transform="rotate({nak:.1f} 980 1000)">'
          f'{figura(980, 1000, 520, t, "#2f2b33", "#cfe2f2", False, .1, True)}'
          f'<path d="M1050,760 q130,-40 150,90 q10,80 -60,110 q-80,20 -110,-60 Z"'
          f' fill="#8a7352" {o(7)}/></g>')
    # красный зигзаг над поясницей
    zg = A.seg(t, 2.6, 1.2)
    if zg > .02:
        s += (f'<path d="M940,760 l34,-54 l-14,54 l40,-60 l-20,66" fill="none" stroke="#e03a2a"'
              f' stroke-width="12" opacity="{.9*math.sin(math.pi*zg):.2f}" stroke-linecap="round"/>')
    s += par(960, 740, t, 3, .5, 160, .4)
    s += sneg_letit(t, 26, 193, .5, .7)
    s += vinetka(.48)
    return s


def divan_s_grelkoy(t):
    """Человек на диване, на пояснице платок и грелка, стрелки часов летят."""
    s = f'<rect width="{W}" height="{H}" fill="#8a7b66"/>'
    for i in range(14):
        s += SL(Z_DAL, f'<rect x="{i*140}" width="128" height="{H}" fill="#96866e"'
                       f' opacity="{.3 if i%2 else .12}"/>')
    s += SL(Z_SRED, polovicy(930, "url(#pol)"))
    s += teplo(900, 700, 700, 420, .55)
    # диван
    s += SL(Z_SRED, f'<rect x="240" y="700" width="1240" height="240" rx="28" fill="#55606a" {o(8)}/>'
                    f'<rect x="200" y="620" width="1320" height="120" rx="26" fill="#63707a" {o(6)}/>')
    # лежит
    s += SL(Z_SRED, f'<path d="M420,700 q400,-90 800,-10 q60,40 -20,60 q-420,40 -760,10 Z"'
                    f' fill="#2f2b33" {o(7)}/>')
    s += SL(Z_SRED, f'<circle cx="420" cy="660" r="58" fill="#2f2b33" {o(6)}/>')
    # платок и грелка булькает
    bl = 6 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<rect x="820" y="{620+bl:.0f}" width="260" height="90" rx="30"'
                    f' fill="#c0523c" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="648" width="380" height="60" rx="20" fill="#9a5a4a" opacity=".8"/>')
    # кот ложится на спину хозяину
    kp = A.ease(A.seg(t, 1.2, 1.4))
    s += SL(Z_SRED, kot(1180, 700 - 10 * kp, t, 1.1 * kp + .2, "#3b3430", spit=True))
    # часы быстро крутят стрелки
    s += SL(Z_DAL, f'<circle cx="1660" cy="330" r="130" fill="#f2ead6" {o(7)}/>')
    for i in range(12):
        a = math.radians(i * 30)
        s += SL(Z_DAL, f'<circle cx="{1660+math.cos(a)*104:.0f}" cy="{330+math.sin(a)*104:.0f}"'
                       f' r="5" fill="#6b6150"/>')
    for sp, L in ((360, 90), (1400, 60)):
        a = -90 + (t * sp) % 360
        s += SL(Z_DAL, f'<g transform="rotate({a:.0f} 1660 330)">'
                       f'<rect x="1654" y="{330-L}" width="12" height="{L}" rx="6" fill="#2e2a24"/></g>')
    # мешок в углу маленький и невинный
    s += SL(Z_SRED, f'<path d="M1560,1000 q70,-120 150,0 q-70,40 -150,0 Z" fill="#8a7352" {o(6)}/>')
    s += vinetka(.46)
    return s


def seni_masterskaya(t):
    """Тёплые сени: лук в косах, корзина с лозой, нож на бруске."""
    s = f'<rect width="{W}" height="{H}" fill="#54402c"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 90))
    s += f'<rect width="{W}" height="{H}" fill="#2e2113" opacity=".35"/>'
    s += SL(Z_SRED, polovicy(930, "url(#pol)"))
    s += teplo(960, 560, 900, 520, .6)
    # дверь со двора закрывается
    zk = A.ease(A.seg(t, 0, 1.2))
    s += SL(Z_SRED, dver(60, 240, 330, 700, .55 * (1 - zk), "url(#derev)", True))
    s += SL(Z_SRED, f'<path d="M390,300 l{200*(1-zk):.0f},-40 l0,700 l{-200*(1-zk):.0f},-20 Z"'
                    f' fill="#cfe0f0" opacity="{.35*(1-zk):.2f}"/>')
    # лук в косах качается
    for i, lx in enumerate((640, 760)):
        kach = 5 * A.w(t, .6, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {lx} 240)">'
                        f'<rect x="{lx-8}" y="240" width="16" height="120" fill="#b8a271" {o(3)}/>')
        for j in range(5):
            s += SL(Z_SRED, f'<ellipse cx="{lx+(-1)**j*26}" cy="{380+j*74}" rx="42" ry="48"'
                            f' fill="#d2a85c" {o(5)}/>')
        s += SL(Z_SRED, "</g>")
    # корзина и лоза гнётся
    s += SL(Z_SRED, f'<path d="M1020,940 q140,-40 280,0 l-30,-190 q-110,-30 -220,0 Z" fill="#b08a52" {o(7)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M1040,{790+i*34} q120,{18+6*A.w(t,.8,i):.0f} 240,0"'
                        f' fill="none" stroke="#8a6a3c" stroke-width="8" opacity=".8"/>')
    gn = 20 * A.w(t, .9)
    s += SL(Z_SRED, f'<path d="M1300,760 q{90+gn:.0f},-90 160,-10" fill="none" stroke="#c9a76a"'
                    f' stroke-width="10" stroke-linecap="round"/>')
    # нож ходит по бруску
    hx = 1620 + 60 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<rect x="1500" y="900" width="320" height="40" rx="10" fill="#7d7265" {o(6)}/>')
    s += SL(Z_SRED, f'<g transform="rotate(-10 {hx:.0f} 880)">'
                    f'<rect x="{hx-110:.0f}" y="860" width="200" height="26" rx="8" fill="url(#zhel)" {o(5)}/>'
                    f'<rect x="{hx+90:.0f}" y="854" width="80" height="38" rx="10" fill="url(#derev)" {o(5)}/></g>')
    s += SL(Z_SRED, _utvar_izby(340, 1000, 260, t, 19))
    s += vinetka(.46)
    return s


def ogorod_pod_ineem(t):
    """Огород в инее: грядки, бочка; у двери машут рукой, грабли к стене."""
    s = nebo("rassv", t, False, 197)
    s += SL(Z_DAL, _ulica_dal(60, 640, 1200, t, True, 199))
    s += SL(Z_SRED, izba_snaruzhi(1560, 1000, 740, t, True, True, 23))
    s += SL(Z_SRED, f'<path d="M-20,760 q520,-40 1020,-10 q480,26 940,-20 V{H} H-20 Z"'
                    f' fill="#8a8470" {o(6)}/>')
    # грядки в инее
    for i in range(5):
        y = 820 + i * 56
        s += SL(Z_SRED, f'<path d="M{60-i*20},{y} q400,{-24-i*4:.0f} 860,0 q-420,34 -860,0 Z"'
                        f' fill="#6f6a56" {o(4)}/>')
        s += SL(Z_SRED, f'<path d="M{60-i*20},{y-6} q400,{-24-i*4:.0f} 860,0"'
                        f' fill="none" stroke="#dfe9f2" stroke-width="9" opacity=".75"/>')
    # иней искрится
    for i in range(22):
        rnd = random.Random(600 + i)
        bl = .2 + .7 * abs(A.w(t, 1.4 + rnd.random(), rnd.random()))
        s += (f'<circle cx="{rnd.randint(60,1000)}" cy="{rnd.randint(800,1040)}" r="3.4"'
              f' fill="#ffffff" opacity="{bl:.2f}"/>')
    # перевёрнутая бочка
    s += SL(Z_SRED, f'<ellipse cx="1120" cy="880" rx="110" ry="36" fill="#7d5636" {o(6)}/>'
                    f'<path d="M1010,880 v110 q110,40 220,0 V880 Z" fill="url(#derev)" {o(7)}/>')
    # грабли к стене
    gr = A.ease(A.seg(t, 1.6, 1.2))
    s += SL(Z_SRED, f'<g transform="rotate({-28+10*gr:.0f} 1430 1000)">'
                    f'<rect x="1420" y="620" width="22" height="380" fill="url(#derev)" {o(4)}/>'
                    f'<rect x="1370" y="600" width="120" height="20" rx="6" fill="#6d5636" {o(4)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="{1378+i*26}" y="618" width="10" height="34" fill="#6d5636"/>')
    s += SL(Z_SRED, "</g>")
    # бабушка в дверях машет
    s += SL(Z_SRED, figura(1660, 1000, 400, t, "#332e33", "#ffe0ae", True, .2, True))
    mh = 26 * A.w(t, 2.0)
    s += SL(Z_SRED, f'<path d="M1706,800 q50,{-50+mh:.0f} 84,{-10+mh*.4:.0f}" fill="none"'
                    f' stroke="#332e33" stroke-width="24" stroke-linecap="round"/>')
    # калитка покачивается, дым из трубы
    kk = 5 * A.w(t, .5)
    s += SL(Z_SRED, f'<g transform="rotate({kk:.1f} 1220 700)">'
                    f'<rect x="1220" y="700" width="180" height="300" rx="8" fill="url(#derev)"'
                    f' opacity=".9" {o(5)}/></g>')
    s += vinetka(.44)
    return s


def dorozhka_ot_magazina_k_podezdu(t):
    """Огород перелистывается страницей, на его месте — городской двор."""
    k = A.ease(A.seg(t, .2, 1.8))
    s = nebo("den", t, False, 211)
    # новый кадр: двор
    s += SL(Z_DAL, _panelka(1180, 1010, 820, t, 5, True, 223))
    s += SL(Z_SRED, f'<rect y="1010" width="{W}" height="{H-1010}" fill="#8d918a" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M-20,1080 V940 q520,-50 980,-26 q500,24 960,-26 V1080 Z"'
                    f' fill="#eaf2fc" {o(5)}/>')
    # дорожка от магазина к подъезду
    s += SL(Z_SRED, f'<path d="M200,1080 q320,-120 700,-150 q300,-24 560,-10 l0,40'
                    f' q-280,-10 -540,14 q-340,32 -640,146 Z" fill="#c3d2e4" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="120" y="640" width="420" height="380" rx="10" fill="#8a6b58" {o(7)}/>'
                    f'<rect x="160" y="700" width="340" height="160" rx="8" fill="#9fc0cc" opacity=".6"/>'
                    f'<rect x="120" y="600" width="420" height="50" rx="10" fill="#b8323a" {o(5)}/>')
    # фонарь загорается
    fz = A.ease(A.seg(t, 1.4, 1.0))
    s += SL(Z_SRED, f'<rect x="980" y="420" width="16" height="560" fill="#3a4049" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="988" cy="416" r="{190*fz:.0f}" fill="url(#teplo)" opacity="{.55*fz:.2f}"/>')
    # урна и санки под снежными шапками
    s += SL(Z_SRED, f'<path d="M1300,1000 h150 l-20,-170 h-110 Z" fill="#5c6b5e" {o(6)}/>'
                    f'<ellipse cx="1375" cy="828" rx="80" ry="26" fill="#f2f8ff" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1560" y="940" width="240" height="26" rx="10" fill="#b8323a" {o(5)}/>'
                    f'<ellipse cx="1680" cy="932" rx="120" ry="24" fill="#f2f8ff" {o(4)}/>')
    # страница-огород перелистывается
    if k < .98:
        s += (f'<g transform="translate({-1920*k:.0f},0)">'
              f'<rect width="{W}" height="{H}" fill="#9aa08a" {o(0)}/>')
        for i in range(5):
            s += (f'<path d="M{60},{820+i*56} q400,{-24-i*4:.0f} 860,0 q-420,34 -860,0 Z"'
                  f' fill="#6f6a56" {o(4)}/>')
        s += (f'<path d="M{W-40},0 q60,540 0,1080" fill="none" stroke="#5c5544"'
              f' stroke-width="14" opacity=".6"/></g>')
        s += (f'<path d="M{W-1920*k:.0f},0 q90,540 0,1080 l40,0 V0 Z" fill="#c9cfbe" opacity=".5"/>')
    s += sneg_letit(t, 22, 227, .4, .6)
    s += vinetka(.44)
    return s


def balkon_s_lyzhami_i_bankami(t):
    """Балкон снаружи, забитый лыжами, банками и санками; вдали гаражи."""
    s = nebo("den", t, False, 229)
    s += SL(Z_DAL, f'<rect y="700" width="{W}" height="{H-700}" fill="#9aa09a" {o(5)}/>')
    for i in range(6):            # гаражи вдали
        x = 90 + i * 310
        s += SL(Z_DAL, f'<rect x="{x}" y="730" width="250" height="150" rx="8" fill="#7a6a58" {o(6)}/>'
                       f'<rect x="{x+22}" y="772" width="206" height="108" rx="6" fill="#5c5247" {o(4)}/>'
                       f'<rect x="{x+108}" y="820" width="36" height="20" rx="6" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M-20,880 H{W+20} V{H} H-20 Z" fill="#dfe8f2" {o(4)}/>')
    # стена дома с балконом крупно слева
    s += SL(Z_PERED, f'<rect x="-40" y="-20" width="1120" height="{H+40}" fill="#b4b8ae" {o(7)}/>')
    for i in range(9):
        s += SL(Z_PERED, f'<rect x="-40" y="{i*130}" width="1120" height="8" fill="#9aa096" opacity=".45"/>')
    # проём балкона
    s += SL(Z_PERED, f'<rect x="80" y="180" width="880" height="700" rx="10" fill="#6d7a72" {o(8)}/>')
    s += SL(Z_PERED, f'<rect x="110" y="210" width="820" height="640" rx="8" fill="#2f3a36" {o(5)}/>')
    # внутри: банки рядами, лыжи у стенки, санки
    for r in range(3):
        for c in range(6):
            bx, by = 420 + c * 84, 420 + r * 130
            s += SL(Z_PERED, f'<rect x="{bx}" y="{by}" width="62" height="96" rx="10"'
                             f' fill="#9fc8a8" opacity=".9" {o(4)}/>'
                             f'<rect x="{bx+5}" y="{by-16}" width="52" height="22" rx="7"'
                             f' fill="#c9a86a" {o(3)}/>')
    sl = A.ease(A.seg(t, 1.8, 1.2))
    for i in range(2):
        s += SL(Z_PERED, f'<g transform="rotate({-12+4*sl+i*5:.0f} {210+i*48} 840)">'
                         f'<rect x="{194+i*48}" y="{300+26*sl:.0f}" width="40" height="540" rx="18"'
                         f' fill="#b8323a" {o(6)}/></g>')
    s += SL(Z_PERED, f'<rect x="150" y="800" width="250" height="28" rx="12" fill="#8a5a3a" {o(5)}/>')
    s += SL(Z_PERED, ptica(260, 770 - 16 * abs(A.w(t, 2.2)), t, .8, "#e8c24a", seryj="#4a6a8a"))
    # перила и снег на них
    s += SL(Z_PERED, f'<rect x="80" y="840" width="880" height="56" rx="10" fill="#8f958c" {o(6)}/>')
    s += SL(Z_PERED, f'<path d="M80,842 q440,-26 880,0 v20 q-440,-20 -880,0 Z" fill="#ffffff" {o(3)}/>')
    # дверь балкона закрывается изнутри
    zk = A.ease(A.seg(t, .6, 1.4))
    s += SL(Z_PERED, f'<rect x="120" y="220" width="300" height="620" rx="8" fill="#5c6b62" {o(7)}/>')
    s += SL(Z_PERED, f'<rect x="{140+250*zk:.0f}" y="246" width="260" height="580" rx="6"'
                     f' fill="#bcd8e8" opacity="{.35+.35*zk:.2f}"/>')
    s += sneg_letit(t, 20, 233, .4, .6)
    s += vinetka(.44)
    return s


def banka_s_tugoy_kryshkoy(t):
    """Банка солёных огурцов с тугой крышкой: тянется в сторону и возвращается."""
    s = f'<rect width="{W}" height="{H}" fill="#9fa79e"/>'
    for i in range(13):
        for j in range(4):
            s += SL(Z_DAL, f'<rect x="{i*150+6}" y="{j*150+6}" width="138" height="138" rx="6"'
                           f' fill="#c2c8ba" opacity="{.5 if (i+j)%2 else .3}"/>')
    s += SL(Z_SRED, f'<rect y="700" width="{W}" height="{H-700}" fill="url(#derev)" {o(8)}/>')
    s += teplo(900, 560, 760, 480, .55)
    # банка: уезжает вбок и возвращается
    k = A.seg(t, 1.0, 2.4)
    dx = 300 * math.sin(math.pi * min(1.0, k)) if k < 1 else 0
    s += ten(900 + dx, 710, 170, 22, .45)
    s += (f'<g transform="translate({dx:.0f},0)">'
          f'<rect x="700" y="190" width="400" height="520" rx="34" fill="#9fc8b0" opacity=".55" {o(8)}/>'
          f'<rect x="690" y="150" width="420" height="72" rx="18" fill="#c9a86a" {o(7)}/>'
          f'<rect x="700" y="222" width="400" height="18" fill="#8a6a3c" opacity=".5"/>')
    # огурцы всплывают, рассол качается
    for i in range(5):
        oy = 640 - i * 66 - 10 * A.w(t, .7, i * .5)
        s += (f'<ellipse cx="{780+(i%3)*104}" cy="{oy:.0f}" rx="74" ry="34"'
              f' fill="#5f7a3c" {o(5)} transform="rotate({-18+i*14} {780+(i%3)*104} {oy:.0f})"/>')
    ry = 270 + 10 * A.w(t, .9)
    s += (f'<path d="M704,{ry:.0f} q200,18 392,0 V706 H704 Z" fill="#8aa86a" opacity=".35"/>')
    s += "</g>"
    # полотенце на плече сползает (без фигуры: висит на крючке и съезжает)
    sp = A.ease(A.seg(t, 2.0, 1.6))
    s += SL(Z_SRED, f'<path d="M1480,{260+120*sp:.0f} q60,-40 120,0 l-20,320 q-50,26 -84,0 Z"'
                    f' fill="#e2d6b4" {o(6)}/>')
    s += vinetka(.46)
    return s


def starik_na_zavalinke(t):
    """Старик на завалинке; просьба-бумеранг возвращается и сбивает шапку."""
    s = nebo("den", t, False, 239)
    s += SL(Z_DAL, _ulica_dal(60, 700, 1840, t, True, 241))
    s += SL(Z_SRED, brevna(-40, 300, 1100, 680, 92))
    s += SL(Z_SRED, f'<path d="M-60,300 L500,120 L1120,300 Z" fill="#6d4b2c" {o(8)}/>')
    s += SL(Z_SRED, f'<rect y="960" width="{W}" height="{H-960}" fill="#e8f0fa" {o(4)}/>')
    # завалинка
    s += SL(Z_SRED, f'<rect x="60" y="880" width="900" height="90" rx="12" fill="#8a6a44" {o(7)}/>')
    s += SL(Z_SRED, figura(420, 880, 420, t, "#332e33", "#ffe0ae", False, .1, True))
    # палец вверх — линией, не анатомией
    pl = A.out(A.seg(t, .4, .8))
    s += (f'<path d="M482,{740-60*pl:.0f} q40,{-50*pl:.0f} 54,{-6*pl:.0f}" fill="none"'
          f' stroke="#332e33" stroke-width="22" stroke-linecap="round"/>')
    # бумеранг: круг и возврат
    k = A.seg(t, .8, 2.6)
    a = 2 * math.pi * k
    bx = 900 + 620 * math.sin(a)
    by = 620 - 180 * math.cos(a)
    s += (f'<g transform="rotate({k*720:.0f} {bx:.0f} {by:.0f})">'
          f'<path d="M{bx-60:.0f},{by:.0f} q30,-70 90,-30 q-40,20 -40,70 q-40,10 -50,-40 Z"'
          f' fill="#c9a86a" {o(5)}/></g>')
    # шапка падает в конце
    sh = A.ease(A.seg(t, 3.0, .8))
    s += SL(Z_SRED, f'<rect x="{1380}" y="{520+360*sh:.0f}" width="96" height="52" rx="18"'
                    f' fill="#6a3a34" {o(5)} transform="rotate({40*sh:.0f} 1428 {546+360*sh:.0f})"/>')
    s += SL(Z_SRED, figura(1430, 1000, 440, t, "#2f2a2e", "#ffe3b0", False, .4, True))
    # собака лает
    lay = abs(A.w(t, 3.0))
    s += SL(Z_SRED, f'<ellipse cx="1700" cy="980" rx="74" ry="44" fill="#6b4c33" {o(5)}/>'
                    f'<circle cx="1766" cy="{940-6*lay:.0f}" r="36" fill="#6b4c33" {o(5)}/>'
                    f'<ellipse cx="1800" cy="{952+8*lay:.0f}" rx="22" ry="{10+10*lay:.0f}" fill="#4a3728"/>')
    s += sneg_letit(t, 16, 251, .3, .5)
    s += vinetka(.44)
    return s


def hozyayka_s_otvertkoy(t):
    """Дверца кухонного шкафа подкручивается сама и перестаёт висеть."""
    s = f'<rect width="{W}" height="{H}" fill="#a8a194"/>'
    for i in range(13):
        for j in range(4):
            s += SL(Z_DAL, f'<rect x="{i*150+6}" y="{j*150+6}" width="138" height="138" rx="6"'
                           f' fill="#bcb6a6" opacity="{.5 if (i+j)%2 else .28}"/>')
    s += SL(Z_SRED, f'<rect y="880" width="{W}" height="200" fill="url(#derev)" {o(7)}/>')
    s += teplo(820, 480, 700, 460, .5)
    # шкаф
    s += SL(Z_SRED, f'<rect x="340" y="200" width="900" height="520" rx="12" fill="#8a6a4a" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="220" width="520" height="480" rx="10" fill="#9c7a56" {o(6)}/>')
    s += SL(Z_SRED, f'<circle cx="730" cy="460" r="16" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="340" y="700" width="900" height="30" rx="8" fill="#6d4a2a" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1280" y="420" width="420" height="300" rx="10" fill="#8a6a4a" {o(7)}/>'
                    f'<rect x="1300" y="450" width="380" height="36" rx="8" fill="#b4916a" {o(4)}/>'
                    f'<rect x="1300" y="520" width="380" height="36" rx="8" fill="#b4916a" {o(4)}/>')
    for i, kx in enumerate((1340, 1440, 1540)):
        s += SL(Z_SRED, krynka(kx, 450, .55))
    # дверца перестаёт висеть
    fix = A.ease(A.seg(t, 1.2, 1.6))
    nak = (12 - 12 * fix) + 1.4 * A.w(t, 1.1) * (1 - fix)
    s += SL(Z_SRED, f'<g transform="rotate({nak:.1f} 380 240)">'
                    f'<rect x="360" y="220" width="330" height="480" rx="10" fill="#9c7a56" {o(6)}/>'
                    f'<circle cx="650" cy="460" r="16" fill="url(#zhel)" {o(3)}/></g>')
    # отвёртка крутится у верхней петли
    a = (t * 240) % 360
    s += SL(Z_SRED, f'<g transform="rotate({a:.0f} 392 250)">'
                    f'<rect x="384" y="250" width="18" height="150" rx="6" fill="{ZHELEZ}" {o(4)}/>'
                    f'<rect x="372" y="380" width="42" height="120" rx="14" fill="#b8323a" {o(5)}/></g>')
    # винтик блестит
    s += SL(Z_SRED, f'<circle cx="392" cy="250" r="{10+5*abs(A.w(t,2.2)):.0f}" fill="#fff" opacity=".8"/>')
    # табуретка и кот смотрит снизу
    s += SL(Z_SRED, f'<rect x="300" y="880" width="260" height="30" rx="10" fill="url(#derev)" {o(6)}/>'
                    f'<rect x="320" y="910" width="26" height="150" fill="#7d5636" {o(4)}/>'
                    f'<rect x="514" y="910" width="26" height="150" fill="#7d5636" {o(4)}/>')
    s += SL(Z_SRED, kot(760, 1060, t, 1.25, "#3b3430"))
    s += vinetka(.46)
    return s


def zapiska_na_holodilnike(t):
    """Листок «спросить завтра» прижимается магнитом; за окном луна."""
    s = f'<rect width="{W}" height="{H}" fill="#8e958c"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#99a098" {o(0)}/>')
    # окно с луной
    lu = A.ease(A.seg(t, 1.0, 2.0))
    vid = (f'<rect width="420" height="330" fill="#1e2a44"/>'
           f'<circle cx="{150+40*lu:.0f}" cy="120" r="56" fill="#f6efd8" opacity=".95"/>'
           f'<ellipse cx="{90-60*lu:.0f}" cy="140" rx="150" ry="54" fill="#39415c" opacity=".9"/>')
    s += SL(Z_DAL, okno_izby(1400, 220, 420, 330, t, vid, 0, False, True))
    # холодильник
    s += SL(Z_SRED, f'<rect x="200" y="120" width="860" height="940" rx="26" fill="#eef1ee" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="200" y="420" width="860" height="16" fill="#c9cec7" opacity=".9"/>')
    s += SL(Z_SRED, f'<rect x="980" y="240" width="26" height="150" rx="12" fill="#b4bab2" {o(4)}/>'
                    f'<rect x="980" y="500" width="26" height="180" rx="12" fill="#b4bab2" {o(4)}/>')
    # листок прижимается магнитом
    k = A.out(A.seg(t, .3, 1.0))
    ly = 300 - 160 * (1 - k)
    kach = 4 * A.w(t, 1.2) * (1 - k * .7)
    s += SL(Z_SRED, f'<g transform="rotate({-5+kach:.1f} 600 {ly+110:.0f})">'
                    f'<rect x="420" y="{ly:.0f}" width="360" height="260" rx="8" fill="url(#list)" {o(6)}/>'
                    f'<path d="M460,{ly+90:.0f} h280 M460,{ly+150:.0f} h200" stroke="#8a7a5c"'
                    f' stroke-width="9" opacity=".8"/></g>')
    s += SL(Z_SRED, f'<circle cx="600" cy="{ly+10:.0f}" r="{26+8*(1-k):.0f}" fill="#b8323a" {o(5)}/>')
    s += vinetka(.46)
    return s


# ═══════════════════ 4. ЗАБОТЫ ДНЯ: ОГОНЬ ═══════════════════
def ogon_v_temnote(t):
    """Чёрный фон; в центре разгорается пламя и освещает брёвна стены."""
    k = A.ease(A.seg(t, 1.2, 2.2))
    s = f'<rect width="{W}" height="{H}" fill="#0b0a0c"/>'
    s += SL(Z_DAL, f'<g opacity="{.9*k:.2f}">{brevna(-20, -20, W + 40, H + 40, 94)}</g>')
    s += f'<rect width="{W}" height="{H}" fill="#0b0a0c" opacity="{.72-.35*k:.2f}"/>'
    s += teplo(960, 720, 420 + 420 * k, 360 + 300 * k, .35 + .5 * k)
    if k > .04:
        s += ten(960, 1010, 260 * k, 26, .5)
        for i, (dx, a) in enumerate(((-120, -16), (-10, 2), (110, 18))):
            s += SL(Z_SRED, f'<rect x="{930+dx}" y="950" width="30" height="190" rx="10"'
                            f' fill="url(#derev)" {o(6)} transform="rotate({a} {945+dx} 1010)"/>')
        s += ugli(860, 1000, 200, t, 8, 3)
        s += ogon(960, 980, t, 2.4 * k, .0, int(9 * k) + 1)
        s += iskra_let(t, 960, 920, 14, 7, 520, .62)
        s += dym(960, 880, t, 5, .22, 420, .22, wide=1.3)
    s += vinetka(.56)
    return s


def slovo_iz_solomy(t):
    """Соломинки слетаются и складываются в слово ОВИН; сверху знак вопроса.
    Буквы собраны из ШТРИХОВ-соломин, иначе слово не читается."""
    s = f'<rect width="{W}" height="{H}" fill="#120f0c"/>'
    s += teplo(960, 560, 860, 470, .45)
    k = A.ease(A.seg(t, .2, 1.8))
    # штрихи букв: (x, y, длина, угол)
    BUKVY = {
        "O": [(0, 0, 210, 90), (150, 0, 210, 90), (0, 0, 150, 0), (0, 210, 150, 0)],
        "B": [(0, 0, 210, 90), (0, 0, 130, 0), (0, 105, 130, 0), (0, 210, 130, 0),
              (130, 0, 105, 90), (130, 105, 105, 90)],
        "I": [(0, 0, 210, 90), (160, 0, 210, 90), (6, 200, 250, -52)],
        "H": [(0, 0, 210, 90), (160, 0, 210, 90), (0, 100, 160, 0)],
    }
    slovo = (("O", 300), ("B", 680), ("I", 1030), ("H", 1380))
    rnd = random.Random(777)
    n = 0
    for bi, (b_, bx) in enumerate(slovo):
        for (sx, sy, dl, ug) in BUKVY[b_]:
            n += 1
            kk = min(1.0, max(0.0, k * 1.35 - bi * .09))
            a0 = rnd.uniform(0, 360)
            r0 = 800 + rnd.uniform(0, 500)
            x1, y1 = bx + sx, 450 + sy
            x0 = x1 + math.cos(math.radians(a0)) * r0
            y0 = y1 + math.sin(math.radians(a0)) * r0
            x = x0 + (x1 - x0) * kk
            y = y0 + (y1 - y0) * kk
            rot = rnd.uniform(0, 180) * (1 - kk) + ug * kk
            s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{dl}" height="30" rx="13"'
                  f' fill="url(#solom)" opacity="{.55+.45*kk:.2f}" {o(5)}'
                  f' transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>')
    # знак вопроса качается над словом
    if k > .6:
        kach = 6 * A.w(t, .7)
        s += (f'<g transform="rotate({kach:.1f} 960 230)" opacity="{min(1.0,(k-.6)*2.5):.2f}">'
              f'<path d="M880,190 q70,-96 150,-26 q58,52 -24,100 q-46,28 -46,76" fill="none"'
              f' stroke="url(#solom)" stroke-width="30" stroke-linecap="round"/>'
              f'<circle cx="960" cy="382" r="19" fill="url(#solom)"/></g>')
    # пыль золотится
    for i in range(26):
        rnd2 = random.Random(800 + i)
        ph = rnd2.random()
        s += (f'<circle cx="{rnd2.randint(200,1700)}" cy="{300+600*((t*.12+ph)%1):.0f}" r="3"'
              f' fill="#e8c86a" opacity="{.25+.3*abs(A.w(t,1.1,ph)):.2f}"/>')
    s += vinetka(.54)
    return s


def ovin_bez_steny(t):
    """Овин в разрезе: наверху снопы на жердях, внизу в яме огонь."""
    s = nebo("noch", t, True, 257)
    s += SL(Z_DAL, _ulica_dal(1160, 760, 760, t, True, 263))
    # сруб без передней стены — в левой полосе (справа окно вставки)
    s += SL(Z_SRED, f'<path d="M40,980 V420 L430,230 L820,420 V980 Z" fill="#2a1f16" {o(8)}/>')
    s += SL(Z_SRED, brevna(40, 420, 60, 560, 70))
    s += SL(Z_SRED, brevna(760, 420, 60, 560, 70))
    s += SL(Z_SRED, f'<path d="M20,430 L430,210 L840,430 L430,330 Z" fill="#6d4b2c" {o(8)}/>')
    s += teplo(430, 880, 420, 320, .8)
    # жерди и снопы наверху
    for i in range(3):
        y = 500 + i * 90
        s += SL(Z_SRED, f'<rect x="100" y="{y}" width="660" height="14" rx="6" fill="url(#derev)" {o(4)}/>')
        for j in range(4):
            kk = A.out(A.seg(t, .4 + (i * 4 + j) * .14, .6))
            sx = 150 + j * 160
            s += SL(Z_SRED, f'<g transform="translate(0,{-120*(1-kk):.0f}) rotate({-10+j*7} {sx} {y})"'
                            f' opacity="{kk:.2f}">'
                            f'<path d="M{sx-40},{y} q40,-110 80,0 q-40,30 -80,0 Z" fill="url(#solom)" {o(5)}/>'
                            f'<rect x="{sx-44}" y="{y-54}" width="88" height="12" rx="5"'
                            f' fill="#a07c2e" opacity=".8"/></g>')
    # яма с огнём
    s += SL(Z_SRED, f'<path d="M190,980 h480 l-40,96 h-400 Z" fill="#1a120c" {o(6)}/>')
    s += ugli(260, 1010, 340, t, 9, 4)
    s += ogon(430, 1000, t, 2.0, .1, 7)
    # стрелки тепла идут вверх
    for i in range(5):
        kk = A.seg(t, i * .3, 1.8)
        y = 960 - 420 * kk
        s += (f'<g opacity="{.5*(1-kk):.2f}"><path d="M{240+i*110},{y:.0f} v-70 m-22,22 l22,-28 l22,28"'
              f' fill="none" stroke="#ffd08a" stroke-width="8" stroke-linecap="round"/></g>')
    # зерно сыплется со снопов
    for i in range(12):
        rnd = random.Random(900 + i)
        ph = rnd.random() * 1.4
        kk = A.seg(t, ph, 1.4)
        s += (f'<circle cx="{rnd.randint(120,760)}" cy="{620+340*kk:.0f}" r="4"'
              f' fill="#e8c86a" opacity="{.8*(1-kk):.2f}"/>')
    s += vinetka(.5)
    return s


def usadba_izdali(t):
    """Усадьба с пригорка: дом, двор, поодаль овин и площадка с цепами."""
    s = nebo("sumer", t, False, 269)
    s += SL(Z_NEBO, oblaka(t, 220, 4, 271, .4, "#c0b2a0", 10.0))
    s += SL(Z_DAL, f'<path d="M-20,700 q500,-80 1000,-30 q500,50 960,-20 V{H} H-20 Z"'
                   f' fill="#7a7260" {o(7)}/>')
    s += SL(Z_DAL, _sneg_lezhit(740, 22, "url(#sneg)"))
    # дом и двор слева
    s += SL(Z_SRED, izba_snaruzhi(360, 900, 560, t, True, True, 29))
    s += SL(Z_SRED, pleten(60, 830, 700, 120, 9))
    # овин поодаль справа
    s += SL(Z_DAL, brevna(1320, 640, 300, 240, 60))
    s += SL(Z_DAL, f'<path d="M1290,650 L1470,520 L1650,650 Z" fill="#6d4b2c" {o(7)}/>')
    s += SL(Z_DAL, dym(1470, 520, t, 4, .2, 260, .3, wide=1.1))
    # площадка с двумя человечками, цепы взлетают
    for i, cx in enumerate((1180, 1280)):
        ud = A.w(t, 1.1, i * .5)
        s += SL(Z_DAL, siluet(cx, 880, 150, "#2a2630", .95))
        s += SL(Z_DAL, f'<g transform="rotate({-40+50*ud:.0f} {cx} 810)">'
                       f'<rect x="{cx-6}" y="740" width="12" height="90" fill="url(#derev)" {o(3)}/>'
                       f'<rect x="{cx-4}" y="690" width="10" height="60" fill="#6d4a2a" {o(3)}/></g>')
    # вороны на жердях
    for i, (vx, vy) in enumerate(((1560, 600), (1620, 596), (980, 700))):
        s += SL(Z_DAL, f'<ellipse cx="{vx}" cy="{vy+3*A.w(t,1.4,i):.0f}" rx="22" ry="14" fill="#1d1f26"/>'
                       f'<circle cx="{vx+18}" cy="{vy-8:.0f}" r="10" fill="#1d1f26"/>')
    s += sneg_letit(t, 18, 277, .35, .5)
    s += vinetka(.46)
    return s


def iskra_i_solominka(t):
    """Крупно: искра тянется к соломинке, край тлеет, его прихлопывают."""
    s = f'<rect width="{W}" height="{H}" fill="#140f0b"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 96))
    s += f'<rect width="{W}" height="{H}" fill="#0f0a07" opacity=".6"/>'
    s += teplo(820, 900, 620, 420, .8)
    # свисающая соломинка крупно
    otd = A.ease(A.seg(t, 1.2, .5))
    tle = A.seg(t, 3.0, 1.6)
    hlo = A.ease(A.seg(t, 4.6, .8))
    kach = 14 * A.w(t, 1.6) * (1 + otd)
    s += (f'<g transform="rotate({-6+kach:.1f} 900 180)">'
          f'<rect x="880" y="180" width="26" height="560" rx="10" fill="url(#solom)" {o(6)}/>'
          f'<rect x="846" y="180" width="18" height="420" rx="8" fill="#c8a850" opacity=".9" {o(4)}/>')
    if tle > .02 and hlo < .4:
        s += (f'<ellipse cx="893" cy="{740:.0f}" rx="{20+16*tle:.0f}" ry="{14+10*tle:.0f}"'
              f' fill="{UGOL}" opacity="{.9*(1-hlo*2):.2f}"/>')
        s += dym(893, 720, t, 4, .3, 260, .3 * (1 - hlo), wide=.9)
    s += "</g>"
    # искры из ямы
    s += SL(Z_SRED, f'<path d="M300,1000 h700 l-40,80 h-620 Z" fill="#1a120c" {o(6)}/>')
    s += ugli(420, 1020, 300, t, 8, 5)
    s += ogon(620, 1010, t, 1.4, .2, 6)
    for i in range(3):
        k = A.seg(t, .3 + i * .9, 1.4)
        ix = 620 + (893 - 620) * k
        iy = 1000 - 300 * k
        s += f'<circle cx="{ix:.0f}" cy="{iy:.0f}" r="{9-4*k:.0f}" fill="#ffd27a" opacity="{1-k*.5:.2f}"/>'
    # рукавица прихлопывает (предмет, не рука)
    if hlo > .02:
        s += (f'<g transform="translate(0,{-300*(1-hlo):.0f})">'
              f'<path d="M800,640 q60,-60 140,-10 q30,70 -10,130 q-80,30 -130,-40 Z"'
              f' fill="{TKAN}" {o(7)}/></g>')
    s += vinetka(.54)
    return s


def temnyy_ugol_s_glazami(t):
    """Тёмный угол овина: лохматая тень с глазами-угольками, перед ней миска."""
    s = f'<rect width="{W}" height="{H}" fill="#0d0b0a"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 92))
    s += f'<rect width="{W}" height="{H}" fill="#0a0807" opacity=".74"/>'
    s += teplo(620, 880, 460, 300, .5)
    # лохматая тень
    rnd = random.Random(321)
    d = "M560,1010"
    for i in range(16):
        d += f" q{rnd.randint(-40,60)},{-rnd.randint(50,120)} {rnd.randint(30,70)},{-rnd.randint(10,40)}"
    s += f'<path d="{d} L1180,1010 Z" fill="#16130f" opacity=".96"/>'
    # шерсть шевелится
    for i in range(22):
        rnd2 = random.Random(400 + i)
        bx = 540 + i * 32
        hh = rnd2.randint(50, 150)
        kach = 10 * A.w(t, .8, i * .3)
        yb = 1020 - (260 if 3 < i < 18 else 60)
        s += (f'<path d="M{bx},{yb} q{kach:.0f},{-hh} {kach*1.7:.0f},{-hh*1.35:.0f}"'
              f' fill="none" stroke="#1f1a14" stroke-width="14" stroke-linecap="round"/>')
    # глаза-угольки моргают и добреют
    dob = A.ease(A.seg(t, 2.4, 1.6))
    bl = A.blink(t, 2.6) if hasattr(A, "blink") else 1.0
    for dx in (-86, 86):
        ry = (34 - 12 * dob) * bl
        s += (f'<ellipse cx="{880+dx}" cy="640" rx="44" ry="{max(4,ry):.0f}"'
              f' fill="{SVET if dob>.5 else UGOL}" opacity=".95"/>'
              f'<ellipse cx="{880+dx}" cy="640" rx="96" ry="{max(8,ry*2.2):.0f}"'
              f' fill="url(#teplo)" opacity=".55"/>')
    # миска каши и кусок пирога
    s += ten(540, 1012, 120, 18, .5)
    s += SL(Z_SRED, f'<path d="M430,960 q110,-40 220,0 q-30,70 -110,70 q-80,0 -110,-70 Z"'
                    f' fill="url(#glina)" {o(6)}/>')
    s += par(540, 950, t, 4, .5, 180, .45)
    s += SL(Z_SRED, f'<path d="M680,1010 l120,-40 l40,60 l-120,36 Z" fill="url(#krem)" {o(5)}/>')
    s += vinetka(.6)
    return s


def zhitnica_s_laryami(t):
    """Житница: лари с зерном, струйка зерна, кот следит за норкой."""
    s = f'<rect width="{W}" height="{H}" fill="#2a2119"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 94))
    s += f'<rect width="{W}" height="{H}" fill="#1c1510" opacity=".45"/>'
    s += SL(Z_SRED, polovicy(940, "url(#pol)"))
    # луч из окошка с пылью
    s += SL(Z_DAL, f'<rect x="120" y="140" width="200" height="200" rx="8" fill="#9fc0d8" opacity=".5" {o(6)}/>')
    s += luch(140, 160, 200, 760, t, .22)
    s += teplo(420, 560, 520, 420, .45)
    # лари вдоль стены (в левой полосе: справа окно вставки)
    for i, lx in enumerate((80, 420)):
        s += SL(Z_SRED, f'<rect x="{lx}" y="600" width="300" height="340" rx="10" fill="url(#derev)" {o(8)}/>'
                        f'<rect x="{lx-14}" y="570" width="328" height="46" rx="10" fill="#8a6440" {o(6)}/>')
        s += SL(Z_SRED, f'<path d="M{lx+20},600 q130,-40 260,0 q-130,36 -260,0 Z" fill="url(#solom)" {o(4)}/>')
    # струйка зерна из верхнего ларя
    for i in range(16):
        rnd = random.Random(500 + i)
        ph = rnd.random()
        k = (t * .9 + ph) % 1.0
        s += (f'<circle cx="{560+rnd.randint(-16,16)}" cy="{600+340*k:.0f}" r="4.5"'
              f' fill="#e8c86a" opacity="{.9*(1-k*.4):.2f}"/>')
    s += SL(Z_SRED, f'<path d="M470,940 q90,-50 180,0 q-90,34 -180,0 Z" fill="url(#solom)" {o(5)}/>')
    # кот и норка
    s += SL(Z_SRED, kot(840, 940, t, 1.2, "#3b3430"))
    s += SL(Z_SRED, f'<path d="M980,940 q40,-60 80,0 Z" fill="#120d09"/>')
    gl = .3 + .5 * abs(A.w(t, 1.6))
    s += SL(Z_SRED, f'<circle cx="1012" cy="922" r="5" fill="#ffd27a" opacity="{gl:.2f}"/>'
                    f'<circle cx="1030" cy="922" r="5" fill="#ffd27a" opacity="{gl:.2f}"/>')
    s += vinetka(.5)
    return s


def deti_u_yamy_s_ognem(t):
    """Трое детей у ямы ворошат картошку; тени складываются в овинника."""
    s = f'<rect width="{W}" height="{H}" fill="#120e0a"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 92))
    s += f'<rect width="{W}" height="{H}" fill="#0d0907" opacity=".55"/>'
    s += teplo(960, 880, 560, 360, .85)
    # тень на стене складывается в лохматого овинника
    k = A.ease(A.seg(t, 1.0, 2.6))
    rnd = random.Random(55)
    d = "M620,900"
    for i in range(14):
        d += f" q{rnd.randint(-30,50)},{-rnd.randint(60,160)*k-20:.0f} {rnd.randint(30,70)},{-rnd.randint(10,40)*k-6:.0f}"
    s += f'<path d="{d} L1300,900 Z" fill="#000" opacity="{.25+.3*k:.2f}"/>'
    # яма с углями
    s += SL(Z_SRED, f'<path d="M620,1000 h680 l-50,80 h-580 Z" fill="#1a120c" {o(6)}/>')
    s += ugli(680, 1016, 560, t, 12, 7)
    s += ogon(960, 1004, t, 1.1, .0, 4)
    # картофелина перекатывается
    px = 820 + 240 * A.seg(t, .6, 2.4)
    s += (f'<ellipse cx="{px:.0f}" cy="1004" rx="40" ry="30" fill="#8a6a44" {o(5)}'
          f' transform="rotate({px:.0f} {px:.0f} 1004)"/>')
    # трое детей кружком, палочки
    for i, (cx, hh, ph) in enumerate(((620, 420, .0), (980, 400, .4), (1320, 430, .8))):
        ogl = 8 * A.w(t, .7, ph) if i == 0 else 0
        s += (f'<g transform="rotate({ogl:.1f} {cx} 1010)">'
              f'{figura(cx, 1010, hh, t, "#1f1a18", "#ffb866", (i == 1), ph, True)}</g>')
        s += (f'<path d="M{cx+(60 if i<2 else -60)},{1010-hh*.5:.0f} L{960+(i-1)*60},990"'
              f' stroke="#6d4a2a" stroke-width="12" stroke-linecap="round"/>')
    s += iskra_let(t, 960, 960, 10, 9, 420, .5)
    s += vinetka(.54)
    return s


# ═══════════════════ 5. КАРТОШКА И ВЕЧЕР ═══════════════════
def koster_za_ogorodami(t):
    """Костёр за огородами, дети на корточках; вдали палатка и флажок."""
    s = nebo("sumer", t, True, 281)
    s += SL(Z_DAL, _ulica_dal(1100, 700, 820, t, False, 283))
    s += SL(Z_DAL, f'<path d="M-20,780 q520,-50 1000,-20 q500,30 960,-24 V{H} H-20 Z"'
                   f' fill="#5e6a4a" {o(6)}/>')
    # палатка и флажок проступают
    pr = A.ease(A.seg(t, 2.6, 1.6))
    s += SL(Z_DAL, f'<g opacity="{pr:.2f}">'
                   f'<path d="M1180,820 L1340,620 L1500,820 Z" fill="#6b7a5c" {o(6)}/>'
                   f'<path d="M1340,620 V820" stroke="#4a5640" stroke-width="8"/>'
                   f'<rect x="1600" y="520" width="10" height="300" fill="#8a8470" {o(3)}/>'
                   f'<path d="M1610,520 l{90+16*A.w(t,1.6):.0f},26 l-{90:.0f},26 Z" fill="#b8323a" {o(4)}/></g>')
    # костёр в левой полосе (справа окно вставки)
    s += ten(470, 1000, 250, 28, .5)
    for i, a in enumerate((-36, -12, 14, 36)):
        s += SL(Z_SRED, f'<rect x="452" y="810" width="34" height="210" rx="12" fill="url(#derev)" {o(6)}'
                        f' transform="rotate({a} 470 1010)"/>')
    s += teplo(470, 870, 520, 400, .9)
    s += ugli(380, 1004, 190, t, 8, 3)
    s += ogon(470, 960, t, 2.2, .0, 8)
    s += iskra_let(t, 470, 880, 16, 5, 600, .7)
    s += dym(470, 840, t, 5, .2, 420, .26, wide=1.5)
    # дети на корточках
    for i, (cx, hh) in enumerate(((230, 300), (700, 290))):
        s += SL(Z_SRED, figura(cx, 1020, hh, t, "#231f26", "#ffb866", (i == 1), i * .4, True))
    s += vinetka(.48)
    return s


def kartoshka_v_ladonyah(t):
    """Печёная картофелина крупно на газете: корка лопается, идёт пар."""
    s = f'<rect width="{W}" height="{H}" fill="#140f0b"/>'
    s += teplo(960, 640, 700, 460, .75)
    s += SL(Z_SRED, f'<rect y="820" width="{W}" height="{H-820}" fill="#2a2119" {o(0)}/>')
    # газета
    s += SL(Z_SRED, f'<path d="M420,900 q540,-60 1080,0 q-20,170 -540,170 q-520,0 -540,-170 Z"'
                    f' fill="#d8d2c0" {o(6)}/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M520,{930+i*26} h880" stroke="#9a9484" stroke-width="5" opacity=".6"/>')
    # картофелина
    tr = A.ease(A.seg(t, 1.2, 1.0))
    s += ten(960, 870, 230, 26, .5)
    s += (f'<ellipse cx="960" cy="700" rx="300" ry="210" fill="#8a6a44" {o(9)}/>'
          f'<ellipse cx="880" cy="640" rx="90" ry="60" fill="#a07f52" opacity=".5"/>')
    # зола на корке
    for i in range(14):
        rnd = random.Random(900 + i)
        s += (f'<ellipse cx="{rnd.randint(720,1200)}" cy="{rnd.randint(570,840)}" rx="{rnd.randint(10,26)}"'
              f' ry="{rnd.randint(6,16)}" fill="#3b332c" opacity=".45"/>')
    # разлом и пар
    if tr > .02:
        s += (f'<path d="M760,700 q200,{-60*tr:.0f} 400,0 q-200,{90*tr:.0f} -400,0 Z"'
              f' fill="#f2e6c2" {o(6)}/>')
        s += (f'<path d="M800,700 q160,{-40*tr:.0f} 320,0" fill="none" stroke="#fff6dc"'
              f' stroke-width="8" opacity=".8"/>')
        s += par(960, 660, t, 6, .55 * tr, 320, .5 * tr, wide=1.4)
    # крошки золы осыпаются
    for i in range(10):
        rnd = random.Random(950 + i)
        ph = rnd.random() * 1.2
        k = A.seg(t, ph, 1.2)
        s += (f'<circle cx="{rnd.randint(700,1220)}" cy="{860+180*k:.0f}" r="{rnd.uniform(3,7):.0f}"'
              f' fill="#4a4038" opacity="{.7*(1-k):.2f}"/>')
    s += vinetka(.52)
    return s


def korobok_s_solyu_po_krugu(t):
    """Спичечный коробок идёт по кругу над костром, соль сыплется на разлом."""
    s = f'<rect width="{W}" height="{H}" fill="#150f0b"/>'
    s += teplo(820, 760, 640, 420, .7)
    s += SL(Z_SRED, f'<rect y="860" width="{W}" height="{H-860}" fill="#2a2119" {o(0)}/>')
    # круг «мест»: пять картофелин на газетках по дуге (в левой полосе)
    for i in range(5):
        a = math.radians(-160 + i * 40)
        cx = 420 + math.cos(a) * 340
        cy = 820 + math.sin(a) * 150
        s += SL(Z_SRED, f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="86" ry="60" fill="#8a6a44" {o(6)}/>')
        s += SL(Z_SRED, f'<path d="M{cx-60:.0f},{cy:.0f} q60,-20 120,0 q-60,26 -120,0 Z"'
                        f' fill="#f2e6c2" {o(4)}/>')
    # коробок переходит по кругу
    k = A.seg(t, 0, 3.2)
    a = math.radians(-170 + 180 * k)
    bx = 420 + math.cos(a) * 420
    by = 700 + math.sin(a) * 190
    s += (f'<g transform="rotate({k*90:.0f} {bx:.0f} {by:.0f})">'
          f'<rect x="{bx-70:.0f}" y="{by-44:.0f}" width="140" height="88" rx="10" fill="#c9a86a" {o(6)}/>'
          f'<rect x="{bx-50:.0f}" y="{by-26:.0f}" width="100" height="52" rx="6" fill="#8a6a3c" opacity=".7"/></g>')
    # крупинки соли падают на разлом
    for i in range(16):
        rnd = random.Random(1000 + i)
        ph = rnd.random()
        kk = (t * 1.1 + ph) % 1.0
        s += (f'<rect x="{bx+rnd.randint(-40,40):.0f}" y="{by+40+200*kk:.0f}" width="5" height="5"'
              f' fill="#f4f6fa" opacity="{.9*(1-kk):.2f}"/>')
    s += par(420, 760, t, 4, .45, 240, .4)
    s += vinetka(.52)
    return s


def kosterok_u_saraya(t):
    """Дед и внук у маленького костра за сараем, рядом ведро воды."""
    s = nebo("sumer", t, True, 293)
    s += SL(Z_DAL, _ulica_dal(1200, 720, 720, t, True, 307))
    # сарай слева
    s += SL(Z_SRED, f'<rect x="-40" y="360" width="620" height="620" rx="8" fill="#6d5636" {o(8)}/>')
    s += SL(Z_SRED, doski(-40, 360, 620, 620, 90, True))
    s += SL(Z_SRED, f'<path d="M-60,370 L280,220 L620,370 Z" fill="#5c4028" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M-60,370 L280,220 L620,370 Z" fill="url(#sneg)" opacity=".45"/>')
    s += SL(Z_SRED, f'<path d="M-20,980 q520,-40 1000,-16 q500,22 960,-20 V{H} H-20 Z"'
                    f' fill="#eaf2fc" {o(5)}/>')
    # костерок
    s += teplo(1060, 900, 420, 300, .85)
    s += ten(1060, 1010, 180, 22, .5)
    s += ugli(990, 1000, 150, t, 7, 3)
    s += ogon(1060, 980, t, 1.5, .0, 6)
    s += iskra_let(t, 1060, 930, 10, 11, 380, .55)
    # дед и внук
    s += figura(820, 1020, 460, t, "#2f2b33", "#ffb866", False, .1, True)
    pr = 10 * abs(A.w(t, 2.2))
    s += (f'<g transform="translate(0,{-pr:.0f})">'
          f'{figura(1320, 1020, 300, t, "#2f2b33", "#ffb866", False, .5, True)}</g>')
    # прутик закатывает картошку
    s += (f'<path d="M880,860 q120,60 200,96" fill="none" stroke="#6d4a2a" stroke-width="10"'
          f' stroke-linecap="round"/>')
    # ведро воды
    s += SL(Z_SRED, f'<path d="M1460,1000 q80,16 160,0 l-20,-150 q-60,-16 -120,0 Z" fill="{ZHELEZ}" {o(6)}/>'
                    f'<ellipse cx="1540" cy="852" rx="62" ry="18" fill="#9fc8dc" {o(4)}/>')
    s += par(820, 840, t, 3, .4, 150, .35)
    s += par(1320, 900, t, 3, .4, 130, .3)
    s += sneg_letit(t, 18, 311, .35, .5)
    s += vinetka(.46)
    return s


def protiven_za_steklom_duhovki(t):
    """Крупно стекло духовки: противень с картошкой, отражение носа."""
    s = f'<rect width="{W}" height="{H}" fill="#2a2a2c"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#3a3a3e" {o(0)}/>')
    # корпус духовки во весь кадр
    s += SL(Z_SRED, f'<rect x="60" y="80" width="1800" height="920" rx="26" fill="#6b6e72" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="130" y="150" width="1660" height="700" rx="18" fill="#1d1f22" {o(7)}/>')
    # свет духовки
    sv = .75 + .2 * abs(A.w(t, .8))
    s += SL(Z_SRED, f'<rect x="150" y="170" width="1620" height="660" rx="14" fill="#e8a24a"'
                    f' opacity="{.55*sv:.2f}"/>')
    # противень с картошкой
    s += SL(Z_SRED, f'<rect x="300" y="620" width="1320" height="60" rx="10" fill="#4a4a4e" {o(6)}/>')
    for i in range(7):
        kx = 380 + i * 180
        lop = A.ease(A.seg(t, 1.6 + i * .2, .8))
        s += SL(Z_SRED, f'<ellipse cx="{kx}" cy="580" rx="86" ry="62" fill="#b58a52" {o(6)}/>')
        if lop > .05:
            s += SL(Z_SRED, f'<path d="M{kx-50},580 q50,{-26*lop:.0f} 100,0 q-50,{34*lop:.0f} -100,0 Z"'
                            f' fill="#f2e6c2" opacity="{lop:.2f}" {o(4)}/>')
    # отражение лица с прижатым носом
    s += SL(Z_SRED, f'<g opacity=".22">'
                    f'<path d="M1020,840 V520 q160,-150 330,0 V840 Z" fill="#cfe2f2"/>'
                    f'<ellipse cx="1185" cy="470" rx="110" ry="120" fill="#cfe2f2"/>'
                    f'<ellipse cx="1290" cy="500" rx="40" ry="30" fill="#eaf4ff"/></g>')
    # пар из-под дверцы
    s += par(600, 980, t, 5, .5, 260, .4, wide=1.6)
    s += par(1300, 980, t, 4, .45, 240, .35, wide=1.4)
    s += vinetka(.5)
    return s


def miska_kartoshki_i_mnogo_ruk(t):
    """Вид сверху: клеёнка, миска картошки, блюдце соли; картошка разбирается."""
    s = f'<rect width="{W}" height="{H}" fill="#7a6b58"/>'
    # клеёнка в клетку
    s += SL(Z_SRED, f'<rect width="{W}" height="{H}" fill="#cfd6c2" {o(0)}/>')
    for i in range(13):
        s += SL(Z_SRED, f'<rect x="{i*150}" width="26" height="{H}" fill="#9fb08a" opacity=".55"/>')
    for i in range(8):
        s += SL(Z_SRED, f'<rect y="{i*150}" width="{W}" height="26" fill="#9fb08a" opacity=".55"/>')
    s += teplo(960, 540, 700, 480, .5)
    # миска сверху
    s += ten(960, 620, 330, 180, .35)
    s += SL(Z_SRED, f'<circle cx="960" cy="540" r="300" fill="url(#glina)" {o(8)}/>'
                    f'<circle cx="960" cy="540" r="250" fill="#8a5f3a" opacity=".5"/>')
    # картофелины разбираются по одной
    for i in range(9):
        a = math.radians(i * 40)
        kx = 960 + math.cos(a) * 150
        ky = 540 + math.sin(a) * 120
        ushla = A.ease(A.seg(t, 1.0 + i * .35, .7))
        dx = math.cos(a) * 700 * ushla
        dy = math.sin(a) * 500 * ushla
        s += (f'<ellipse cx="{kx+dx:.0f}" cy="{ky+dy:.0f}" rx="70" ry="52" fill="#b58a52"'
              f' opacity="{1-ushla*.8:.2f}" {o(5)}'
              f' transform="rotate({i*33+ushla*80:.0f} {kx+dx:.0f} {ky+dy:.0f})"/>')
    # блюдце с солью, соль рассыпается
    s += SL(Z_SRED, f'<circle cx="1560" cy="760" r="130" fill="{KREM}" {o(6)}/>'
                    f'<circle cx="1560" cy="760" r="84" fill="#f4f6fa" {o(3)}/>')
    for i in range(12):
        rnd = random.Random(1100 + i)
        s += (f'<rect x="{1560+rnd.randint(-240,240)}" y="{760+rnd.randint(-160,160)}" width="6" height="6"'
              f' fill="#f4f6fa" opacity=".8"/>')
    s += par(960, 480, t, 6, .5, 300, .45, wide=1.5)
    s += vinetka(.44)
    return s


def solnce_s_fitilem_nad_selom(t):
    """Солнце — керосиновая лампа: фитиль садится, небо синеет."""
    k = A.ease(A.seg(t, .4, 3.0))
    s = nebo("zakat" if k < .5 else "sumer", t, k > .6, 313)
    s += f'<rect width="{W}" height="{H}" fill="#2b3550" opacity="{.5*k:.2f}"/>'
    # солнце-лампа
    cx, cy = 1180, 380
    s += SL(Z_NEBO, f'<circle cx="{cx}" cy="{cy}" r="{300-120*k:.0f}" fill="url(#teplo)"'
                    f' opacity="{.8-.5*k:.2f}"/>')
    s += SL(Z_NEBO, f'<path d="M{cx-120},{cy+150} q120,{-420+200*k:.0f} 240,0 q-120,120 -240,0 Z"'
                    f' fill="#bcd8e8" opacity="{.30-.12*k:.2f}" {o(5)}/>')
    s += SL(Z_NEBO, f'<ellipse cx="{cx}" cy="{cy+60}" rx="{70-30*k:.0f}" ry="{110-60*k:.0f}"'
                    f' fill="#ffd27a" opacity="{.95-.35*k:.2f}"/>')
    s += SL(Z_NEBO, f'<rect x="{cx-150}" y="{cy+150}" width="300" height="60" rx="18"'
                    f' fill="url(#med)" {o(6)}/>')
    # колёсико прикручивается
    s += SL(Z_NEBO, f'<g transform="rotate({-120*k:.0f} {cx+170} {cy+180})">'
                    f'<circle cx="{cx+170}" cy="{cy+180}" r="34" fill="url(#zhel)" {o(5)}/>'
                    f'<rect x="{cx+166}" y="{cy+150}" width="8" height="60" fill="#3a3a40"/></g>')
    # крыши села и окна зажигаются
    s += SL(Z_DAL, _ulica_dal(60, 820, 1840, t, True, 317))
    for i, (ox, oy) in enumerate(((240, 760), (620, 780), (980, 770), (1420, 775), (1700, 768))):
        zg = A.ease(A.seg(t, 1.6 + i * .3, .6))
        s += SL(Z_SRED, f'<rect x="{ox}" y="{oy}" width="60" height="50" rx="6" fill="{SVET}"'
                        f' opacity="{.2+.7*zg*k:.2f}" {o(3)}/>')
    # тени растут
    s += SL(Z_SRED, f'<path d="M-20,1080 V{1000-60*k:.0f} q520,-40 1000,-10 q500,24 960,-24 V1080 Z"'
                    f' fill="#2b3148" opacity="{.25+.3*k:.2f}"/>')
    s += vinetka(.46)
    return s


def griby_na_nitke_pri_sveche(t):
    """Стол при свече: игла с ниткой нанизывает грибы, связка на гвозде."""
    s = f'<rect width="{W}" height="{H}" fill="#241b12"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 760, 92))
    s += f'<rect width="{W}" height="{H}" fill="#191109" opacity=".45"/>'
    s += SL(Z_SRED, f'<rect y="760" width="{W}" height="{H-760}" fill="url(#derev)" {o(7)}/>')
    s += teplo(620, 620, 620, 460, .85)
    s += svecha(620, 700, t, .0, 2.0)
    # готовая связка на гвозде
    for i in range(6):
        kach = 6 * A.w(t, .5, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 1480 240)">'
                        f'<path d="M{1440+(-1)**i*26},{300+i*90} q60,-50 120,0 q-60,34 -120,0 Z"'
                        f' fill="#9a6b3e" {o(5)}/>'
                        f'<rect x="{1494+(-1)**i*26}" y="{300+i*90}" width="14" height="40"'
                        f' fill="#c9a86a" {o(3)}/></g>')
    s += SL(Z_SRED, f'<path d="M1480,240 v60" stroke="#c9b48a" stroke-width="6"/>'
                    f'<circle cx="1480" cy="236" r="9" fill="{ZHELEZ}"/>')
    # игла с ниткой ходит
    k = A.seg(t, 0, 2.0)
    ix = 780 + 300 * math.sin(math.pi * k)
    s += (f'<g transform="rotate(-24 {ix:.0f} 840)">'
          f'<rect x="{ix:.0f}" y="836" width="190" height="9" rx="4" fill="#cfd6de" {o(3)}/></g>')
    s += (f'<path d="M{ix-180:.0f},880 q180,-40 360,-10" fill="none" stroke="#e2d6b4"'
          f' stroke-width="5" opacity=".9"/>')
    # грибы на столе
    for i in range(4):
        gx = 700 + i * 150
        s += SL(Z_SRED, f'<path d="M{gx-60},900 q60,-54 120,0 q-60,34 -120,0 Z" fill="#9a6b3e" {o(5)}/>'
                        f'<rect x="{gx-10}" y="900" width="22" height="46" rx="8" fill="#c9a86a" {o(4)}/>')
    s += vinetka(.5)
    return s


def rasskazchik_v_ramke(t):
    """На комоде пустая рамка: в ней по очереди появляются рассказчики."""
    s = f'<rect width="{W}" height="{H}" fill="#7d6a52"/>'
    for i in range(14):
        s += SL(Z_DAL, f'<rect x="{i*140}" width="128" height="{H}" fill="#8a7458"'
                       f' opacity="{.3 if i%2 else .12}"/>')
    s += SL(Z_SRED, polovicy(940, "url(#pol)"))
    s += teplo(900, 560, 700, 460, .55)
    # комод с кружевной дорожкой
    s += SL(Z_SRED, f'<rect x="420" y="700" width="1080" height="300" rx="14" fill="url(#derev)" {o(8)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="460" y="{740+i*110}" width="1000" height="90" rx="10"'
                        f' fill="#8a6440" {o(5)}/><circle cx="960" cy="{785+i*110}" r="14"'
                        f' fill="url(#zhel)" {o(3)}/>')
    kach = 4 * A.w(t, .6)
    s += SL(Z_SRED, f'<path d="M440,700 q520,{-30+kach:.0f} 1040,0 q-520,26 -1040,0 Z"'
                    f' fill="#f2ead6" {o(4)}/>')
    for i in range(10):
        s += SL(Z_SRED, f'<circle cx="{470+i*110}" cy="{706+kach*.5:.0f}" r="14" fill="none"'
                        f' stroke="#f2ead6" stroke-width="5"/>')
    # рамка и рассказчики по очереди
    s += SL(Z_SRED, f'<rect x="700" y="260" width="520" height="440" rx="12" fill="url(#derev)" {o(8)}/>'
                    f'<rect x="740" y="300" width="440" height="360" rx="8" fill="#2d2a30" {o(5)}/>')
    kto = int(A.seg(t, 0, 7.8) * 3) % 3
    poyav = A.out(A.seg(t, kto * 2.6, .6))
    s += SL(Z_SRED, f'<g opacity="{poyav:.2f}">'
                    f'{figura(960, 660, 330, t, "#3a3340", "#ffd9a0", kto == 1, kto * .4, True)}</g>')
    if kto == 2:      # сосед с шапкой в руках: шапка перед фигурой
        s += SL(Z_SRED, f'<ellipse cx="960" cy="590" rx="70" ry="34" fill="#6a3a34"'
                        f' opacity="{poyav:.2f}" {o(5)}/>')
    # слушатели кивают
    for i, cx in enumerate((230, 1700)):
        kiv = 6 * A.w(t, .8, i * .5)
        s += SL(Z_PERED, f'<g transform="rotate({kiv:.1f} {cx} 1070)">'
                         f'{figura(cx, 1070, 360, t, "#241f28", "#ffd9a0", (i == 1), i * .3, True)}</g>')
    s += vinetka(.46)
    return s


def komnata_s_pogasshey_lyustroy(t):
    """Люстра гаснет со щелчком: в темноте видны глаза детей и синее окно."""
    gas = 1.0 if t < 1.2 else max(0.0, 1.0 - (t - 1.2) * 4)
    s = f'<rect width="{W}" height="{H}" fill="#6d5c48"/>'
    for i in range(14):
        s += SL(Z_DAL, f'<rect x="{i*140}" width="128" height="{H}" fill="#7a6750"'
                       f' opacity="{(.3 if i%2 else .12)*(.3+.7*gas):.2f}"/>')
    s += f'<rect width="{W}" height="{H}" fill="#0e1220" opacity="{.72*(1-gas):.2f}"/>'
    s += SL(Z_SRED, polovicy(940, "url(#pol)"))
    # ковёр на стене
    s += SL(Z_SRED, f'<rect x="1120" y="240" width="700" height="500" rx="10" fill="#7a3a3c"'
                    f' opacity="{.35+.55*gas:.2f}" {o(6)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{1160+i*170}" y="280" width="120" height="420" rx="40"'
                        f' fill="#a85a4a" opacity="{.3+.4*gas:.2f}"/>')
    # люстра
    s += SL(Z_SRED, f'<rect x="596" y="40" width="10" height="130" fill="#6b6150" {o(3)}/>')
    for i, dx in enumerate((-110, 0, 110)):
        s += SL(Z_SRED, f'<path d="M{600+dx},170 q{dx*.3:.0f},60 {dx*.5:.0f},110" fill="none"'
                        f' stroke="#6b6150" stroke-width="8"/>')
        s += SL(Z_SRED, f'<path d="M{600+dx*1.5-40:.0f},280 h80 l-14,70 h-52 Z" fill="#f2ead6"'
                        f' opacity="{.5+.5*gas:.2f}" {o(4)}/>')
        if gas > .1:
            s += SL(Z_SRED, f'<circle cx="{600+dx*1.5:.0f}" cy="300" r="{150*gas:.0f}"'
                            f' fill="url(#teplo)" opacity="{.6*gas:.2f}"/>')
    # синее окно
    s += SL(Z_SRED, f'<rect x="180" y="300" width="330" height="420" rx="8" fill="#2a3c60"'
                    f' opacity="{.6+.4*(1-gas):.2f}" {o(6)}/>')
    s += SL(Z_SRED, zanaveska(170, 290, 400, 120, "#dfe4ea", t, 1))
    s += SL(Z_SRED, f'<path d="M180,300 L510,300 L900,1080 L60,1080 Z" fill="#8fb4e0"'
                    f' opacity="{.10+.12*(1-gas):.2f}"/>')
    s += SL(Z_SRED, f'<ellipse cx="880" cy="900" rx="520" ry="150" fill="#8fb4e0"'
                    f' opacity="{.08+.10*(1-gas):.2f}"/>')
    # глаза детей в темноте
    if gas < .5:
        for i, (cx, cy) in enumerate(((760, 820), (900, 830), (1030, 824))):
            for dx in (-22, 22):
                bl = .5 + .5 * abs(A.w(t, 1.6 + i * .3, i * .4))
                s += (f'<ellipse cx="{cx+dx}" cy="{cy}" rx="14" ry="{8*bl:.0f}" fill="#f2efe4"'
                      f' opacity="{(1-gas*2)*.95:.2f}"/>'
                      f'<circle cx="{cx+dx}" cy="{cy}" r="{5*bl:.0f}" fill="#20202a"'
                      f' opacity="{(1-gas*2):.2f}"/>')
    s += vinetka(.5)
    return s


def krug_sveta_na_stole(t):
    """Круг света от свечи; в дыму проступают рисунки из рассказов."""
    s = f'<rect width="{W}" height="{H}" fill="#0e0b09"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 700, 92))
    s += f'<rect width="{W}" height="{H}" fill="#0b0907" opacity=".7"/>'
    s += SL(Z_SRED, f'<rect y="820" width="{W}" height="{H-820}" fill="url(#derev)" {o(7)}/>')
    s += teplo(960, 760, 620, 360, .9)
    s += SL(Z_SRED, f'<ellipse cx="960" cy="860" rx="520" ry="150" fill="url(#teplo)" opacity=".5"/>')
    s += svecha(960, 820, t, .0, 2.2)
    # рисунки в дыму по очереди
    ris = int(A.seg(t, .6, 8.4) * 3) % 3
    poy = A.out(A.seg(t, .6 + ris * 2.8, .8))
    gx, gy = 960, 420
    s += f'<g opacity="{.55*poy:.2f}" fill="none" stroke="#cfd6de" stroke-width="10">'
    if ris == 0:            # пилотка
        s += (f'<path d="M{gx-150},{gy+40} q150,-120 300,0 q-150,50 -300,0 Z"/>'
              f'<path d="M{gx-60},{gy-20} l60,-50 l60,50"/>')
    elif ris == 1:          # дед с косой
        s += (f'<circle cx="{gx}" cy="{gy-70}" r="44"/>'
              f'<path d="M{gx},{gy-26} v140 M{gx-60},{gy+40} h120"/>'
              f'<path d="M{gx+70},{gy-80} l120,180 q-90,-40 -120,-180 Z"/>')
    else:                   # дом под соломой
        s += (f'<path d="M{gx-170},{gy+90} v-110 h340 v110 Z"/>'
              f'<path d="M{gx-210},{gy-20} l210,-130 l210,130 Z"/>')
    s += "</g>"
    s += dym(960, 740, t, 6, .24, 520, .26, wide=1.6)
    # лица в полутьме
    for i, cx in enumerate((320, 1600)):
        s += SL(Z_PERED, figura(cx, 1080, 420, t, "#171419", "#ffb866", (i == 1), i * .4, True, .95))
    s += vinetka(.6)
    return s


def shalash_iz_odeyala(t):
    """Под одеялом двое детей с фонариком; снаружи крадётся тень руки."""
    s = f'<rect width="{W}" height="{H}" fill="#120f16"/>'
    s += teplo(900, 700, 560, 380, .6)
    # одеяло шалашом
    dyh = 10 * A.w(t, .5)
    s += (f'<path d="M-40,1080 L540,{330+dyh:.0f} q420,-120 840,0 L1960,1080 Z"'
          f' fill="#6b4a6a" {o(10)}/>')
    s += (f'<path d="M540,{330+dyh:.0f} q420,-120 840,0" fill="none" stroke="#8a6488"'
          f' stroke-width="18" opacity=".8"/>')
    for i in range(7):
        s += (f'<path d="M{200+i*240},1080 L{620+i*120},{420+dyh:.0f}" stroke="#53395a"'
              f' stroke-width="14" opacity=".6"/>')
    # внутри: фонарик и круглые глаза
    fl = .7 + .3 * abs(A.w(t, 3.0))
    s += (f'<ellipse cx="960" cy="800" rx="340" ry="230" fill="#1d1a22" opacity=".96"/>')
    s += (f'<ellipse cx="960" cy="790" rx="{220*fl:.0f}" ry="{150*fl:.0f}" fill="url(#teplo)"'
          f' opacity="{.75*fl:.2f}"/>')
    s += (f'<rect x="920" y="840" width="80" height="150" rx="16" fill="#c9a86a" {o(5)}/>')
    for i, cx in enumerate((830, 1090)):
        for dx in (-26, 26):
            s += (f'<ellipse cx="{cx+dx}" cy="760" rx="22" ry="{20+4*A.w(t,1.3,i*.4):.0f}"'
                  f' fill="#f4efe2"/>'
                  f'<circle cx="{cx+dx}" cy="760" r="10" fill="#1d1a22"/>')
    # тень руки крадётся по одеялу снаружи
    k = A.seg(t, 1.0, 3.0)
    tx = 200 + 1400 * k
    s += (f'<g opacity=".5" transform="translate({tx:.0f},0)">'
          f'<path d="M0,560 q60,-120 140,-40 q50,-90 110,10 q60,-60 100,30 q40,70 -40,150'
          f' q-150,60 -230,-30 Z" fill="#0d0b10"/></g>')
    s += vinetka(.56)
    return s


def pechnaya_dverca_i_zvezda(t):
    """Печная дверца крупно: искра уходит в трубу и становится звездой."""
    k = A.seg(t, .8, 3.0)
    s = f'<rect width="{W}" height="{H}" fill="#140f0b"/>'
    # внизу — печь, вверху — ночное небо над трубой
    s += SL(Z_NEBO, f'<rect width="{W}" height="520" fill="url(#nnoch)"/>')
    for i in range(20):
        rnd = random.Random(1200 + i)
        s += SL(Z_NEBO, f'<circle cx="{rnd.randint(40,1880)}" cy="{rnd.randint(40,420)}"'
                        f' r="{rnd.uniform(1.6,3):.1f}" fill="#fff6e2" opacity="{.4+.4*abs(A.w(t,.6,rnd.random())):.2f}"/>')
    s += SL(Z_DAL, f'<path d="M-20,520 q500,-40 1000,-10 q500,24 960,-20 V720 H-20 Z" fill="#2a2a38" {o(0)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="300" width="200" height="260" rx="10" fill="#6d5636" {o(7)}/>')
    s += SL(Z_SRED, dym(860, 300, t, 5, .22, 320, .3, wide=1.2))
    # печь крупно внизу
    s += SL(Z_PERED, f'<rect y="560" width="{W}" height="{H-560}" fill="{PECH}" {o(8)}/>')
    s += SL(Z_PERED, f'<rect x="560" y="700" width="700" height="380" rx="16" fill="#2a2018" {o(7)}/>')
    s += SL(Z_PERED, f'<rect x="600" y="740" width="620" height="300" rx="10" fill="#140d08" {o(4)}/>')
    s += ogon(900, 1000, t, 2.2, .0, 7)
    s += ugli(660, 1030, 480, t, 11, 5)
    s += teplo(900, 900, 620, 360, .9)
    # искра уходит вверх и становится звездой
    ix = 900 + 40 * A.w(t, 1.2)
    iy = 960 - 900 * k
    if k < .96:
        s += f'<circle cx="{ix:.0f}" cy="{iy:.0f}" r="{10-4*k:.0f}" fill="#ffd27a" opacity="{1-.3*k:.2f}"/>'
    else:
        bl = .6 + .4 * abs(A.w(t, 1.4))
        s += (f'<circle cx="860" cy="120" r="{8*bl:.0f}" fill="#fff6e2"/>'
              f'<circle cx="860" cy="120" r="{40*bl:.0f}" fill="url(#teplo)" opacity=".6"/>')
    s += vinetka(.5)
    return s


def dom_s_dymkom_dnem(t):
    """Сельский дом днём: охапка щепок к крыльцу, первый дымок, дети у калитки."""
    s = nebo("den", t, False, 331)
    s += SL(Z_DAL, _ulica_dal(60, 700, 1840, t, True, 337))
    s += SL(Z_SRED, izba_snaruzhi(900, 990, 820, t, False, True, 31))
    s += SL(Z_SRED, f'<path d="M-20,980 q520,-40 1000,-14 q500,22 960,-20 V{H} H-20 Z"'
                    f' fill="#eaf2fc" {o(5)}/>')
    # первый дымок
    s += SL(Z_SRED, dym(1130, 560, t, 5, .2, 360, .32, wide=1.2))
    # хозяйка с охапкой щепок (охапка — предмет, не руки)
    k = A.seg(t, 0, 4.0)
    hx = 420 + 320 * k
    s += SL(Z_SRED, figura(hx, 1020, 440, t, "#332e33", "#ffe0ae", True, .1, True))
    s += SL(Z_SRED, f'<g transform="rotate({-6+4*A.w(t,1.2):.1f} {hx+80:.0f} 800)">')
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{hx+30+i*12:.0f}" y="{760+i*8:.0f}" width="150" height="16" rx="7"'
                        f' fill="url(#derev)" {o(4)} transform="rotate({-14+i*6} {hx+100:.0f} {768+i*8:.0f})"/>')
    s += SL(Z_SRED, "</g>")
    # щепка падает
    sh = A.seg(t, 1.6, 1.2)
    s += (f'<rect x="{hx+120:.0f}" y="{800+240*sh:.0f}" width="120" height="14" rx="6"'
          f' fill="url(#derev)" {o(4)} transform="rotate({90*sh:.0f} {hx+180:.0f} {807+240*sh:.0f})"/>')
    # калитка, дети и собака
    s += SL(Z_SRED, pleten(60, 880, 420, 130, 7))
    for i, cx in enumerate((180, 300)):
        s += SL(Z_SRED, figura(cx, 1030, 260 + i * 30, t, "#2f2b33", "#ffe0ae", (i == 1), i * .4, True))
    s += SL(Z_SRED, f'<ellipse cx="620" cy="1010" rx="72" ry="42" fill="#6b4c33" {o(5)}/>'
                    f'<circle cx="684" cy="{972-8*abs(A.w(t,2.4)):.0f}" r="34" fill="#6b4c33" {o(5)}/>')
    s += vinetka(.44)
    return s


def panelnyy_dom_v_sinih_oknah(t):
    """Фасад девятиэтажки вечером: все окна мерцают синим."""
    s = nebo("noch", t, True, 347)
    s += SL(Z_DAL, f'<rect y="900" width="{W}" height="{H-900}" fill="#2a2f36" {o(0)}/>')
    s += SL(Z_SRED, f'<rect x="120" y="120" width="1680" height="880" rx="10" fill="#6b7076" {o(8)}/>')
    for r in range(9):
        for c in range(12):
            x, y = 180 + c * 136, 160 + r * 92
            mg = .35 + .55 * abs(A.w(t, 1.2 + (r * 12 + c) % 7 * .2, (r * 3 + c) * .37))
            s += SL(Z_SRED, f'<rect x="{x}" y="{y}" width="104" height="66" rx="6"'
                            f' fill="#7fc8f0" opacity="{mg:.2f}" {o(3)}/>')
    # антенны качаются
    for i, ax in enumerate((400, 900, 1500)):
        kach = 5 * A.w(t, .7, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {ax} 120)">'
                        f'<rect x="{ax-4}" y="0" width="8" height="130" fill="#3a4049" {o(2)}/>'
                        f'<rect x="{ax-50}" y="20" width="100" height="7" fill="#3a4049" {o(2)}/>'
                        f'<rect x="{ax-36}" y="50" width="72" height="7" fill="#3a4049" {o(2)}/></g>')
    s += sneg_letit(t, 44, 349, .7, .9)
    s += vinetka(.48)
    return s


def tetradka_pod_lampoy(t):
    """Тетрадка в клетку под лампой: из строчек вырастают рисунки."""
    s = f'<rect width="{W}" height="{H}" fill="#1c1812"/>'
    s += teplo(620, 620, 620, 440, .8)
    s += SL(Z_SRED, f'<rect y="700" width="{W}" height="{H-700}" fill="url(#derev)" {o(7)}/>')
    # лампа слева (окно вставки справа)
    s += SL(Z_SRED, f'<rect x="150" y="300" width="18" height="400" fill="{ZHELEZ}" {o(4)}/>'
                    f'<path d="M60,300 h220 l-44,-110 h-132 Z" fill="#3a6a4a" {o(7)}/>')
    s += SL(Z_SRED, f'<circle cx="170" cy="310" r="260" fill="url(#teplo)" opacity=".55"/>')
    # тетрадка
    s += ten(620, 1010, 330, 24, .4)
    s += SL(Z_SRED, f'<rect x="300" y="660" width="660" height="400" rx="10" fill="#f2f0e4" {o(7)}'
                    f' transform="rotate(-5 630 860)"/>')
    s += SL(Z_SRED, f'<g transform="rotate(-5 630 860)">')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="300" y="{690+i*42}" width="660" height="3" fill="#9fb8cf" opacity=".8"/>')
    for i in range(16):
        s += SL(Z_SRED, f'<rect x="{300+i*42}" y="660" width="3" height="400" fill="#9fb8cf" opacity=".8"/>')
    # строчки растут
    for i in range(4):
        k = A.ease(A.seg(t, .4 + i * .5, .8))
        s += SL(Z_SRED, f'<rect x="340" y="{724+i*84}" width="{560*k:.0f}" height="12" rx="6"'
                        f' fill="#2f4a6a" opacity=".85"/>')
    s += SL(Z_SRED, "</g>")
    # рисунки вырастают из строчек
    for i, (rx, ry) in enumerate(((1180, 560), (1420, 620), (1640, 540))):
        k = A.out(A.seg(t, 1.2 + i * .7, .8))
        if k <= .02:
            continue
        s += f'<g opacity="{k:.2f}" transform="translate({rx},{ry}) scale({k:.2f})" fill="none" stroke="#2f4a6a" stroke-width="9">'
        if i == 0:      # костёр
            s += '<path d="M-60,60 L60,60 M-40,60 q40,-90 80,0 Z"/>'
        elif i == 1:    # картошка
            s += '<ellipse cx="0" cy="20" rx="70" ry="50"/><path d="M-40,10 q40,-20 80,0"/>'
        else:           # мизинцы
            s += '<path d="M-70,40 q40,-60 70,0 q30,-60 70,0"/>'
        s += "</g>"
    # очки на столе блестят
    s += SL(Z_SRED, f'<g transform="translate(980,990)">'
                    f'<circle cx="0" cy="0" r="40" fill="none" stroke="url(#zhel)" stroke-width="8"/>'
                    f'<circle cx="100" cy="0" r="40" fill="none" stroke="url(#zhel)" stroke-width="8"/>'
                    f'<path d="M40,0 h20" stroke="url(#zhel)" stroke-width="8"/>'
                    f'<circle cx="-16" cy="-16" r="8" fill="#fff" opacity="{.3+.5*abs(A.w(t,1.8)):.2f}"/></g>')
    s += vinetka(.5)
    return s


def lampa_pechka(t):
    """Свет настольной лампы рисует на стене тёплый контур печки с огнём."""
    k = A.ease(A.seg(t, .6, 2.4))
    s = f'<rect width="{W}" height="{H}" fill="#15121a"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#1b1722" {o(0)}/>')
    # конус света от лампы
    s += SL(Z_SRED, f'<path d="M420,420 L1560,160 L1560,980 L420,620 Z" fill="{SVET}"'
                    f' opacity="{.10+.10*k:.2f}"/>')
    for i in range(22):
        rnd = random.Random(1300 + i)
        ph = rnd.random()
        s += (f'<circle cx="{620+rnd.randint(0,860)}" cy="{300+500*((t*.1+ph)%1):.0f}" r="3"'
              f' fill="#ffe9bc" opacity="{.2+.35*abs(A.w(t,1.1,ph)):.2f}"/>')
    # контур печки на стене
    s += (f'<g opacity="{.25+.5*k:.2f}" fill="none" stroke="#ffcf8a" stroke-width="{10+6*k:.0f}">'
          f'<path d="M1000,900 V420 h420 v480 Z"/>'
          f'<path d="M1060,880 V600 h160 v280 Z"/>'
          f'<path d="M980,420 h460"/></g>')
    if k > .4:
        s += ogon(1140, 860, t, 1.3 * (k - .4) / .6, .0, 5)
        s += teplo(1140, 760, 320 * k, 280 * k, .35 * k)
    # лампа
    s += SL(Z_PERED, f'<rect x="300" y="500" width="20" height="440" fill="{ZHELEZ}" {o(4)}/>'
                     f'<path d="M200,500 h220 l-40,-120 h-140 Z" fill="#8a3a34" {o(7)}/>'
                     f'<ellipse cx="310" cy="950" rx="120" ry="26" fill="#8a3a34" {o(6)}/>')
    s += SL(Z_PERED, f'<circle cx="310" cy="510" r="180" fill="url(#teplo)" opacity=".6"/>')
    s += vinetka(.54)
    return s


# ═══════════════════ 6. ПОКУПКИ И ПОГОДА ═══════════════════
def prilavok_univermaga(t):
    """Прилавок: дешёвый ботинок разевает подошву, добротный блестит."""
    s = f'<rect width="{W}" height="{H}" fill="#9aa0a4"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="620" fill="#aab0b2" {o(6)}/>')
    # лампа дневного света мигает
    mg = .45 + .5 * (1 if abs(A.w(t, 3.0)) > .2 else .3)
    s += SL(Z_DAL, f'<rect x="420" y="80" width="1080" height="40" rx="10" fill="#eef4f8"'
                   f' opacity="{mg:.2f}" {o(4)}/>')
    s += SL(Z_DAL, f'<rect x="420" y="120" width="1080" height="200" fill="url(#teplo)" opacity="{.2*mg:.2f}"/>')
    # прилавок
    s += SL(Z_SRED, f'<rect y="700" width="{W}" height="{H-700}" fill="#8a6a4a" {o(8)}/>')
    s += SL(Z_SRED, f'<rect y="660" width="{W}" height="60" rx="10" fill="#b49070" {o(6)}/>')
    # дешёвый ботинок: подошва хлопает
    hl = abs(A.w(t, 2.2))
    s += ten(560, 700, 150, 18, .4)
    s += (f'<path d="M380,660 q40,-130 170,-120 q120,10 150,120 Z" fill="#4a4036" {o(7)}/>')
    s += (f'<g transform="rotate({-14*hl:.1f} 400 660)">'
          f'<path d="M370,650 q170,30 330,0 l0,30 q-170,26 -330,0 Z" fill="#6b5a46" {o(6)}/></g>')
    # добротный ботинок блестит
    s += ten(1340, 700, 160, 18, .45)
    s += (f'<path d="M1160,660 q40,-150 190,-136 q140,14 170,136 Z" fill="#3a2a22" {o(8)}/>'
          f'<path d="M1150,650 q190,34 370,0 l0,34 q-190,30 -370,0 Z" fill="#241a14" {o(6)}/>')
    s += (f'<ellipse cx="1280" cy="570" rx="{50+16*abs(A.w(t,1.4)):.0f}" ry="26" fill="#fff"'
          f' opacity=".35" transform="rotate(-18 1280 570)"/>')
    # касса и чек
    s += SL(Z_SRED, f'<rect x="1600" y="420" width="280" height="240" rx="12" fill="#6b7076" {o(7)}/>'
                    f'<rect x="1640" y="460" width="200" height="80" rx="8" fill="#2f3a44" {o(4)}/>')
    ch = A.seg(t, .6, 2.6)
    s += SL(Z_SRED, f'<rect x="1700" y="400" width="90" height="{20+240*ch:.0f}" fill="#f2f0e4" {o(4)}/>')
    s += vinetka(.46)
    return s


def vitrina_vecherom(t):
    """Витрина под снегом: манекен в пальто, сапоги; в стекле отражение."""
    s = nebo("noch", t, False, 353)
    s += SL(Z_DAL, _panelka(1240, 1010, 760, t, 5, True, 359))
    s += SL(Z_SRED, f'<rect y="1010" width="{W}" height="{H}" fill="#6e756d" {o(5)}/>')
    # витрина в левой полосе
    s += SL(Z_SRED, f'<rect x="60" y="220" width="760" height="800" rx="12" fill="#3a3f46" {o(8)}/>')
    sv = .7 + .2 * abs(A.w(t, .9))
    s += SL(Z_SRED, f'<rect x="100" y="260" width="680" height="720" rx="8" fill="#f2e2bc"'
                    f' opacity="{.55*sv:.2f}"/>')
    s += SL(Z_SRED, f'<circle cx="440" cy="560" r="420" fill="url(#teplo)" opacity="{.4*sv:.2f}"/>')
    # манекен в пальто
    s += SL(Z_SRED, f'<path d="M300,980 V560 q120,-80 240,0 V980 Z" fill="#5a4a5e" {o(7)}/>'
                    f'<circle cx="420" cy="500" r="56" fill="#cfc3b2" {o(5)}/>'
                    f'<path d="M420,560 v300" stroke="#43374a" stroke-width="10" opacity=".7"/>')
    # сапоги на подставке
    for i, bx in enumerate((620, 700)):
        s += SL(Z_SRED, f'<path d="M{bx},960 v-220 q40,-30 70,0 v220 Z" fill="#3a2a22" {o(6)}/>'
                        f'<path d="M{bx-10},960 h90 v26 h-90 Z" fill="#241a14" {o(5)}/>')
    # отражение хозяйки в стекле
    otr = A.ease(A.seg(t, 1.2, 1.6))
    s += SL(Z_SRED, f'<g opacity="{.3+.2*otr:.2f}" transform="translate({60*otr:.0f},0)">'
                    f'{figura(600, 980, 520, t, "#cfe2f2", "#ffffff", True, .2, True)}</g>')
    s += sneg_letit(t, 40, 367, .7, .9)
    s += vinetka(.46)
    return s


def budka_sapozhnika(t):
    """Будка сапожника: молоточек прибивает набойку, за окошком идёт снег."""
    s = f'<rect width="{W}" height="{H}" fill="#2a2119"/>'
    s += SL(Z_DAL, doski(-20, -20, W + 40, H + 40, 110, True))
    s += f'<rect width="{W}" height="{H}" fill="#1d1510" opacity=".45"/>'
    s += teplo(620, 660, 560, 420, .7)
    s += SL(Z_SRED, f'<rect y="860" width="{W}" height="{H-860}" fill="url(#derev)" {o(7)}/>')
    # лапка с сапогом
    s += SL(Z_SRED, f'<rect x="520" y="700" width="40" height="180" fill="{ZHELEZ}" {o(5)}/>'
                    f'<ellipse cx="540" cy="880" rx="110" ry="26" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M420,700 q60,-260 190,-230 q110,26 120,230 Z" fill="#3a2a22" {o(8)}/>'
                    f'<path d="M400,690 q180,34 350,0 l0,36 q-180,30 -350,0 Z" fill="#241a14" {o(6)}/>')
    # молоточек стучит
    ud = abs(A.w(t, 3.2))
    s += SL(Z_SRED, f'<g transform="rotate({-40+36*ud:.0f} 760 560)">'
                    f'<rect x="750" y="560" width="22" height="200" rx="8" fill="url(#derev)" {o(4)}/>'
                    f'<rect x="700" y="520" width="130" height="56" rx="12" fill="{ZHELEZ}" {o(6)}/></g>')
    # гвоздики в банке
    s += SL(Z_SRED, f'<rect x="980" y="780" width="150" height="100" rx="10" fill="#9fc8b0"'
                    f' opacity=".6" {o(5)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{995+i*18}" y="{740+6*A.w(t,2.4,i*.3):.0f}" width="6" height="60"'
                        f' fill="{ZHELEZ}" {o(2)}/>')
    # окошко: мимо проходит пальто, снег гуще
    s += SL(Z_SRED, f'<rect x="1280" y="180" width="520" height="520" rx="10" fill="#2a3c58" {o(8)}/>')
    k = A.seg(t, 0, 1.3)
    gust = int(A.seg(t, 0, 4.3) * 10)
    s += SL(Z_SRED, f'<g>{siluet(1300 + 520 * k, 700, 420, "#1a1f2c", .92, platok=(gust % 2 == 0))}</g>')
    for i in range(10 + gust * 5):
        rnd = random.Random(1400 + i)
        ph = rnd.random()
        kk = (t * .6 + ph) % 1.0
        s += SL(Z_SRED, f'<circle cx="{1290+rnd.randint(0,500)}" cy="{180+520*kk:.0f}"'
                        f' r="{rnd.uniform(2.5,5):.1f}" fill="#f2f8ff" opacity=".8"/>')
    s += vinetka(.5)
    return s


def koshka_na_podushke(t):
    """Серое утро: полосатая кошка на вышитой подушке умывается."""
    s = f'<rect width="{W}" height="{H}" fill="#9aa0a2"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#a6abac" {o(0)}/>')
    # окно с серым небом
    vid = (f'<rect width="520" height="420" fill="#b4bcc2"/>'
           f'<rect y="300" width="520" height="120" fill="#9fa8ae"/>')
    s += SL(Z_DAL, okno_izby(1240, 160, 520, 420, t, vid, .1, False, True))
    s += SL(Z_SRED, f'<rect y="820" width="{W}" height="{H-820}" fill="url(#derev)" {o(7)}/>')
    s += teplo(700, 700, 620, 400, .35)
    # подушка с вышивкой
    s += ten(700, 940, 330, 30, .4)
    s += SL(Z_SRED, f'<path d="M380,900 q320,-130 640,0 q-60,120 -320,120 q-260,0 -320,-120 Z"'
                    f' fill="#e2d2b8" {o(8)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{480+i*110},880 q26,-40 52,0 q-26,36 -52,0 Z" fill="#b8323a"'
                        f' opacity=".7"/>')
    # кошка умывается: лапка ходит у мордочки
    s += SL(Z_SRED, kot(700, 880, t, 2.1, "#8a7a62"))
    um = 14 * A.w(t, 2.0)
    s += (f'<path d="M660,{690+um:.0f} q40,-40 76,-6" fill="none" stroke="#8a7a62"'
          f' stroke-width="24" stroke-linecap="round"/>')
    # полоски
    for i in range(5):
        s += (f'<path d="M{620+i*40},790 q20,30 0,60" fill="none" stroke="#6b5c46"'
              f' stroke-width="9" opacity=".8"/>')
    # усы шевелятся
    for i, sgn in ((0, -1), (1, 1)):
        for j in range(3):
            s += (f'<path d="M{700+sgn*30},{700+j*14} q{sgn*70:.0f},{-10+6*A.w(t,1.6,j*.3):.0f}'
                  f' {sgn*110:.0f},{4*j:.0f}" fill="none" stroke="#f2ead6" stroke-width="4"/>')
    s += vinetka(.44)
    return s


def gvozdik_vmesto_barometra(t):
    """Пустой гвоздик и светлое пятно; под ним кошка — хвост как стрелка."""
    s = f'<rect width="{W}" height="{H}" fill="#b4a68c"/>'
    for i in range(16):
        s += SL(Z_DAL, f'<rect x="{i*120}" width="110" height="{H}" fill="#c0b294"'
                       f' opacity="{.4 if i%2 else .16}"/>')
    s += SL(Z_SRED, f'<rect y="900" width="{W}" height="{H-900}" fill="url(#pol)" {o(7)}/>')
    s += teplo(700, 500, 620, 460, .5)
    s += luch(240, 0, 420, 900, t, .18)
    # светлое пятно и гвоздик
    s += SL(Z_SRED, f'<ellipse cx="860" cy="380" rx="190" ry="220" fill="#e2d8c0" opacity=".85"/>')
    s += SL(Z_SRED, f'<circle cx="860" cy="250" r="12" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="880" cy="268" rx="26" ry="10" fill="#000" opacity=".2"/>')
    # кошка под гвоздиком, хвост — стрелка
    s += SL(Z_SRED, kot(860, 900, t, 2.4, "#4a4038"))
    a = -30 + 40 * A.w(t, .55)
    s += (f'<g transform="rotate({a:.1f} 860 860)">'
          f'<rect x="852" y="640" width="16" height="230" rx="8" fill="#4a4038" {o(4)}/>'
          f'<path d="M846,650 l14,-40 l14,40 Z" fill="#4a4038"/></g>')
    # тень кошки на стене
    s += SL(Z_SRED, f'<ellipse cx="1140" cy="760" rx="{150+20*A.w(t,.5):.0f}" ry="200"'
                    f' fill="#000" opacity=".2"/>')
    s += vinetka(.44)
    return s


def koshka_klubkom_i_uzory(t):
    """Кошка клубком на лежанке; на окне разрастаются ледяные узоры."""
    s = f'<rect width="{W}" height="{H}" fill="#7d6a52"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 92))
    s += f'<rect width="{W}" height="{H}" fill="#2b2016" opacity=".28"/>'
    mor = A.ease(A.seg(t, .8, 2.6))
    vid = f'<rect width="520" height="440" fill="#9fb8cf"/>'
    s += SL(Z_SRED, okno_izby(1180, 180, 520, 440, t, vid, .25 + .65 * mor, False, True))
    s += teplo(560, 700, 560, 400, .55)
    # лежанка
    s += SL(Z_SRED, f'<rect x="120" y="780" width="900" height="60" rx="20" fill="url(#derev)" {o(7)}/>'
                    f'<rect x="150" y="730" width="840" height="60" rx="26" fill="#c9b48a" {o(6)}/>')
    # кошка клубком, бок дышит
    dyh = 1 + .04 * A.w(t, .55)
    s += SL(Z_SRED, f'<g transform="translate(560,700) scale({dyh:.3f})">'
                    f'<ellipse cx="0" cy="0" rx="210" ry="150" fill="#8a7a62" {o(8)}/>'
                    f'<ellipse cx="-120" cy="-40" rx="96" ry="84" fill="#8a7a62" {o(7)}/>'
                    f'<path d="M-190,-100 l30,-70 l56,56 Z" fill="#8a7a62" {o(5)}/>'
                    f'<path d="M-96,-96 l18,-62 l54,48 Z" fill="#8a7a62" {o(5)}/>'
                    f'<path d="M160,40 q110,-30 70,70 q-60,40 -90,-30 Z" fill="#8a7a62" {o(6)}/>'
                    f'<path d="M-170,-10 q60,-40 110,0 q-50,40 -110,0 Z" fill="#6b5c46" {o(5)}/></g>')
    s += par(430, 640, t, 3, .35, 140, .3)
    # ледяные узоры разрастаются
    for i in range(10):
        rnd = random.Random(1500 + i)
        k = max(0.0, min(1.0, mor * 1.3 - i * .08))
        if k <= 0:
            continue
        x0, y0 = rnd.randint(1200, 1660), rnd.randint(210, 580)
        for j in range(5):
            a = math.radians(rnd.uniform(0, 360))
            L = 80 * k
            s += (f'<path d="M{x0},{y0} l{math.cos(a)*L:.0f},{math.sin(a)*L:.0f}"'
                  f' stroke="#eaf6ff" stroke-width="5" opacity="{.7*k:.2f}" stroke-linecap="round"/>')
    s += vinetka(.46)
    return s


def okolica_v_tumane(t):
    """Околица в тумане: человек смотрит из-под ладони, с крыши капает."""
    s = nebo("rassv", t, False, 373)
    s += f'<rect width="{W}" height="{H}" fill="#cdd8e0" opacity=".35"/>'
    s += SL(Z_DAL, _ulica_dal(900, 740, 1020, t, True, 379))
    s += SL(Z_DAL, f'<g opacity=".85">{_tuman(t, 700, .5, "#e2eaf0")}</g>')
    s += SL(Z_SRED, f'<path d="M-20,880 q500,-40 1000,-14 q500,22 960,-20 V{H} H-20 Z"'
                    f' fill="#dfe8ee" {o(4)}/>')
    # сарай слева, с крыши капает
    s += SL(Z_SRED, f'<rect x="60" y="560" width="520" height="340" rx="8" fill="#6d5636" {o(8)}/>')
    s += SL(Z_SRED, f'<path d="M20,570 L320,420 L620,570 Z" fill="#5c4028" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M20,570 L320,420 L620,570 Z" fill="url(#sneg)" opacity=".6"/>')
    for i in range(2):
        kp = A.seg(t, 1.0 + i * 1.6, 1.4)
        s += (f'<ellipse cx="{200+i*220}" cy="{576+320*kp:.0f}" rx="7" ry="14" fill="#bcd8ea"'
              f' opacity="{.85*(1-kp*.3):.2f}"/>')
    # человек смотрит из-под ладони
    s += SL(Z_SRED, figura(1180, 1010, 520, t, "#3a3740", "#eaf2f8", False, .1, True))
    s += (f'<path d="M1230,{1010-520*.86:.0f} q60,-30 96,6" fill="none" stroke="#3a3740"'
          f' stroke-width="22" stroke-linecap="round"/>')
    # сорока на столбе
    s += SL(Z_SRED, f'<rect x="1640" y="520" width="26" height="420" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1653" cy="{490+4*A.w(t,1.4):.0f}" rx="40" ry="22" fill="#1d1f26" {o(4)}/>'
                    f'<circle cx="1686" cy="470" r="17" fill="#1d1f26"/>'
                    f'<path d="M1620,500 l-70,36 l66,-6 Z" fill="#1d1f26"/>'
                    f'<ellipse cx="1648" cy="492" rx="18" ry="12" fill="#eef4f8"/>')
    s += vinetka(.42)
    return s


def kuhonnoe_okno_na_rassvete(t):
    """Кухонное окно: розовеющее небо со звёздами, чайник пускает пар."""
    s = f'<rect width="{W}" height="{H}" fill="#6d6a62"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#78756c" {o(0)}/>')
    # окно (главное слева: справа окно вставки)
    vid = (f'<rect width="700" height="520" fill="#4a5a7a"/>'
           f'<rect y="300" width="700" height="220" fill="#c98a72" opacity=".85"/>'
           f'<rect y="430" width="700" height="90" fill="#e8b48a" opacity=".8"/>')
    for i in range(9):
        rnd = random.Random(1600 + i)
        vid += (f'<circle cx="{rnd.randint(40,660)}" cy="{rnd.randint(40,260)}" r="3"'
                f' fill="#fff6e2" opacity="{.4+.5*abs(A.w(t,.8,rnd.random())):.2f}"/>')
    s += SL(Z_SRED, okno_izby(80, 90, 760, 620, t, vid, .12, False, True))
    s += teplo(560, 760, 560, 380, .5)
    # плита с чайником
    s += SL(Z_SRED, f'<rect y="820" width="1100" height="260" fill="#9aa0a2" {o(7)}/>')
    s += SL(Z_SRED, f'<circle cx="420" cy="860" r="70" fill="#4a4a4e" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="420" cy="860" r="40" fill="{ORA}" opacity="{.5+.3*abs(A.w(t,2.0)):.2f}"/>')
    s += SL(Z_SRED, f'<path d="M250,830 q180,-260 360,0 Z" fill="#cfd6de" {o(8)}/>'
                    f'<path d="M596,742 q120,-40 90,-120" fill="none" stroke="#cfd6de" stroke-width="26"/>'
                    f'<rect x="392" y="596" width="86" height="42" rx="16" fill="#2f3a44" {o(5)}/>'
                    f'<ellipse cx="430" cy="836" rx="190" ry="26" fill="#9aa0a2" {o(5)}/>')
    s += par(640, 620, t, 6, .55, 460, .55, wide=1.5)
    s += vinetka(.46)
    return s


def flyuger_i_dva_neba(t):
    """Флюгер-петушок против облаков; правее небо золотое, закат."""
    s = nebo("den", t, False, 383)
    s += SL(Z_NEBO, f'<rect x="1100" width="820" height="{H}" fill="#e8a85a" opacity=".45"/>')
    s += SL(Z_NEBO, oblaka(t, 240, 5, 389, .5, "#e4e0d6", 14.0))
    s += SL(Z_NEBO, f'<circle cx="1620" cy="420" r="240" fill="url(#teplo)" opacity=".6"/>')
    # крыши
    s += SL(Z_SRED, f'<path d="M-20,900 L320,700 L660,900 Z" fill="#6d4b2c" {o(8)}/>')
    s += SL(Z_SRED, f'<path d="M600,980 L980,760 L1360,980 Z" fill="#5c4028" {o(8)}/>')
    s += SL(Z_SRED, f'<path d="M1240,1020 L1620,820 L2000,1020 Z" fill="#7a5436" {o(8)}/>')
    s += SL(Z_SRED, f'<path d="M1240,1020 L1620,820 L2000,1020 Z" fill="#f0c074" opacity=".45"/>')
    s += SL(Z_SRED, f'<rect y="980" width="{W}" height="{H-980}" fill="#5a5244" {o(0)}/>')
    # флюгер-петушок вертится
    a = 30 * A.w(t, .35)
    s += SL(Z_SRED, f'<rect x="312" y="520" width="16" height="190" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, f'<g transform="rotate({a:.1f} 320 520)">'
                    f'<path d="M250,520 q50,-70 110,-30 q60,40 20,90 q-70,30 -130,-60 Z"'
                    f' fill="#2f3a44" {o(6)}/>'
                    f'<path d="M360,490 l60,30 l-60,30 Z" fill="#b8323a" {o(4)}/></g>')
    # первые хлопья
    s += sneg_letit(t, 30, 397, .6, .7)
    s += vinetka(.44)
    return s


def staryy_topol_s_voronem(t):
    """Голый тополь с вороньём; внизу человек приставил ладонь к уху."""
    s = nebo("sumer", t, False, 401)
    s += SL(Z_DAL, _ulica_dal(1100, 780, 820, t, True, 409))
    s += SL(Z_SRED, f'<path d="M-20,960 q520,-40 1000,-14 q500,22 960,-20 V{H} H-20 Z"'
                    f' fill="#e8f0f8" {o(4)}/>')
    # тополь
    s += SL(Z_SRED, f'<path d="M380,980 q-30,-420 20,-640 q40,-60 70,0 q50,230 20,640 Z"'
                    f' fill="url(#derev)" {o(8)}/>')
    rnd = random.Random(99)
    vetki = []
    for i in range(9):
        y = 420 - i * 36
        L = 180 + rnd.randint(-60, 120)
        sgn = -1 if i % 2 else 1
        x2 = 420 + sgn * L
        kach = 6 * A.w(t, .5, i * .3)
        s += SL(Z_SRED, f'<path d="M420,{y} q{sgn*L*.6:.0f},{-30+kach:.0f} {sgn*L:.0f},{-60+kach:.0f}"'
                        f' fill="none" stroke="#6d4a2a" stroke-width="{16-i}"/>')
        vetki.append((x2, y - 60 + kach))
    # вороньё, клювы в одну сторону
    for i, (vx, vy) in enumerate(vetki):
        rot = abs(A.w(t, 1.6, i * .3))
        s += SL(Z_SRED, f'<ellipse cx="{vx:.0f}" cy="{vy-16:.0f}" rx="34" ry="22" fill="#1d1f26" {o(4)}/>'
                        f'<circle cx="{vx+26:.0f}" cy="{vy-36:.0f}" r="16" fill="#1d1f26"/>'
                        f'<path d="M{vx+40:.0f},{vy-38:.0f} l{34+10*rot:.0f},{6+8*rot:.0f}'
                        f' l{-34:.0f},{6:.0f} Z" fill="#3a3f48"/>')
    # человек слушает
    s += SL(Z_SRED, figura(1180, 1020, 520, t, "#33303a", "#e8eef4", True, .2, True))
    s += (f'<path d="M1124,{1020-520*.84:.0f} q-50,-26 -80,10" fill="none" stroke="#33303a"'
          f' stroke-width="22" stroke-linecap="round"/>')
    # подтаявший снег падает с ветки
    for i in range(3):
        k = A.seg(t, .6 + i * 1.3, 1.2)
        s += (f'<circle cx="{300+i*160}" cy="{380+620*k:.0f}" r="{10-3*k:.0f}" fill="#f2f8ff"'
              f' opacity="{.85*(1-k*.4):.2f}"/>')
    s += vinetka(.46)
    return s


def dve_koshki(t):
    """Кадр надвое: кошка на заборе в селе и кошка на подоконнике в городе."""
    s = f'<rect width="{W}" height="{H}" fill="#2b3550"/>'
    # левая половина: село
    s += SL(Z_DAL, f'<rect width="950" height="{H}" fill="url(#nsumer)"/>')
    s += SL(Z_DAL, _ulica_dal(60, 760, 860, t, True, 419))
    s += SL(Z_SRED, f'<rect y="940" width="950" height="{H-940}" fill="#e8f0f8" {o(0)}/>')
    s += SL(Z_SRED, pleten(60, 820, 820, 130, 9))
    s += SL(Z_SRED, dym(420, 640, t, 4, .2, 260, .3, wide=1.1))
    s += SL(Z_SRED, kot(520, 820, t, 1.7, "#4a4038"))
    # правая половина: город
    s += SL(Z_DAL, f'<rect x="970" width="950" height="{H}" fill="#1a2238"/>')
    for i in range(40):
        rnd = random.Random(1700 + i)
        s += SL(Z_DAL, f'<rect x="{rnd.randint(980,1900)}" y="{rnd.randint(620,1000)}" width="22"'
                       f' height="16" rx="4" fill="#f0d28a"'
                       f' opacity="{.4+.5*abs(A.w(t,.9,rnd.random())):.2f}"/>')
    s += SL(Z_SRED, f'<rect x="970" y="760" width="950" height="40" rx="8" fill="#6b7076" {o(6)}/>')
    s += SL(Z_SRED, kot(1420, 760, t, 1.7, "#6b5c46"))
    # обе зевают
    for cx in (520, 1420):
        zev = A.seg(t, 1.2, 2.8)
        if .3 < zev < .6:
            s += (f'<ellipse cx="{cx+36}" cy="{(820 if cx<900 else 760)-66}" rx="18" ry="22"'
                  f' fill="#3a2a2a"/>')
    # стык половин
    s += SL(Z_PERED, f'<rect x="946" width="28" height="{H}" fill="#0e1118" opacity=".9"/>')
    s += vinetka(.46)
    return s


def balkon_na_zakate(t):
    """Хозяйка с чашкой на балконе смотрит на закат; рядом кошка."""
    s = nebo("zakat", t, False, 421)
    k = A.ease(A.seg(t, .4, 5.0))
    s += SL(Z_NEBO, f'<circle cx="1180" cy="{480+120*k:.0f}" r="240" fill="url(#teplo)"'
                    f' opacity="{.7-.3*k:.2f}"/>')
    s += SL(Z_NEBO, f'<circle cx="1180" cy="{480+120*k:.0f}" r="{90-20*k:.0f}" fill="#ffcf84"'
                    f' opacity="{.95-.4*k:.2f}"/>')
    # дома по сторонам
    s += SL(Z_DAL, _panelka(-60, 1080, 620, t, 6, True, 431))
    s += SL(Z_DAL, _panelka(1560, 1080, 660, t, 6, True, 433))
    # балкон изнутри: перила снизу
    s += SL(Z_PERED, f'<rect y="900" width="{W}" height="{H-900}" fill="#8f958c" {o(7)}/>')
    s += SL(Z_PERED, f'<rect y="860" width="{W}" height="50" rx="10" fill="#a8aea4" {o(6)}/>')
    for i in range(16):
        s += SL(Z_PERED, f'<rect x="{40+i*120}" y="910" width="18" height="170" fill="#6b7076" {o(3)}/>')
    # хозяйка со спины и чашка
    s += SL(Z_SRED, figura(560, 980, 620, t, "#3a3340", "#ffd9a0", True, .1, False))
    s += SL(Z_SRED, krynka(700, 700, .8))
    s += par(718, 650, t, 4, .5, 200, .45)
    # кошка на табуретке, потягивается
    pt = .9 + .25 * A.ease(A.seg(t, 2.0, 1.6))
    s += SL(Z_SRED, f'<rect x="1340" y="820" width="240" height="26" rx="8" fill="url(#derev)" {o(6)}/>'
                    f'<rect x="1360" y="846" width="22" height="120" fill="#7d5636" {o(4)}/>'
                    f'<rect x="1540" y="846" width="22" height="120" fill="#7d5636" {o(4)}/>')
    s += SL(Z_SRED, f'<g transform="translate(1460,820) scale({pt:.2f},1)">'
                    f'{kot(0, 0, t, 1.4, "#6b5c46")}</g>')
    s += vinetka(.46)
    return s


# ═══════════════════ 7. РОДИЛИСЬ В ЭТОТ ДЕНЬ ═══════════════════
def dva_mikrofona_v_luchah(t):
    """Тёмная сцена: два луча прожектора падают на два микрофона."""
    s = f'<rect width="{W}" height="{H}" fill="#0e0d14"/>'
    # занавес
    for i in range(10):
        kach = 10 * A.w(t, .4, i * .4)
        s += SL(Z_DAL, f'<path d="M{i*200+kach:.0f},-20 q40,540 {-10+kach*.5:.0f},1120 h200'
                       f' q10,-580 -30,-1120 Z" fill="#4a1f2c" {o(5)}/>')
    s += f'<rect width="{W}" height="{H}" fill="#0b0a10" opacity=".55"/>'
    # лучи двигаются
    for i, (bx, ph) in enumerate(((660, .0), (1260, .5))):
        sh = 60 * A.w(t, .35, ph)
        s += (f'<path d="M{bx+sh:.0f},-40 L{bx-200:.0f},1080 L{bx+200:.0f},1080 Z"'
              f' fill="{SVET}" opacity=".14"/>')
        s += teplo(bx, 900, 300, 200, .5)
        # микрофон на стойке
        s += SL(Z_SRED, f'<rect x="{bx-7}" y="620" width="14" height="420" fill="{ZHELEZ}" {o(4)}/>'
                        f'<ellipse cx="{bx}" cy="1040" rx="90" ry="22" fill="{ZHELEZ}" {o(5)}/>'
                        f'<ellipse cx="{bx}" cy="600" rx="40" ry="52" fill="#3a3f48" {o(6)}/>'
                        f'<ellipse cx="{bx}" cy="590" rx="26" ry="32" fill="#6b7076" opacity=".8"/>')
    # пылинки в свете
    for i in range(26):
        rnd = random.Random(1800 + i)
        ph = rnd.random()
        s += (f'<circle cx="{rnd.randint(500,1450)}" cy="{200+800*((t*.09+ph)%1):.0f}" r="3"'
              f' fill="#ffe9bc" opacity="{.2+.35*abs(A.w(t,1.2,ph)):.2f}"/>')
    s += vinetka(.56)
    return s


def proigryvatel_s_plastinkoy(t):
    """Проигрыватель: крышка поднимается, под ней пластинка, горит индикатор."""
    s = f'<rect width="{W}" height="{H}" fill="#2a2219"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#352a20" {o(0)}/>')
    s += SL(Z_SRED, f'<rect y="840" width="{W}" height="{H-840}" fill="url(#derev)" {o(7)}/>')
    s += teplo(520, 620, 560, 400, .55)
    # корпус (слева: справа окно вставки с портретом)
    s += ten(480, 870, 320, 24, .45)
    s += SL(Z_SRED, f'<rect x="120" y="620" width="760" height="250" rx="18" fill="#6d4a2a" {o(8)}/>')
    # крышка поднимается
    k = A.out(A.seg(t, .6, 1.2))
    s += SL(Z_SRED, f'<g transform="rotate({-62*k:.0f} 130 620)">'
                    f'<rect x="120" y="580" width="760" height="40" rx="12" fill="#8a6440" {o(7)}/>'
                    f'<rect x="150" y="560" width="700" height="24" rx="10" fill="#bcd8e8"'
                    f' opacity=".4" {o(4)}/></g>')
    # пластинка с чистой этикеткой
    a = (t * 60) % 360
    s += SL(Z_SRED, f'<circle cx="480" cy="700" r="170" fill="#1d1a1c" {o(6)}/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="480" cy="700" r="{60+i*20}" fill="none" stroke="#2f2b2e"'
                        f' stroke-width="4" opacity=".8"/>')
    s += SL(Z_SRED, f'<g transform="rotate({a:.0f} 480 700)">'
                    f'<circle cx="480" cy="700" r="54" fill="#e8d6a8" {o(4)}/>'
                    f'<circle cx="480" cy="700" r="8" fill="#2a2219"/></g>')
    # тонарм и индикатор
    s += SL(Z_SRED, f'<g transform="rotate({-28+8*k:.0f} 760 640)">'
                    f'<rect x="600" y="634" width="180" height="12" rx="6" fill="#9aa0a2" {o(3)}/></g>')
    ind = A.ease(A.seg(t, 1.4, .6))
    s += SL(Z_SRED, f'<circle cx="810" cy="820" r="14" fill="#b8323a" opacity="{.3+.7*ind:.2f}" {o(3)}/>')
    s += luch(260, 120, 320, 560, t, .14)
    s += vinetka(.5)
    return s


def servant_s_radioloy(t):
    """Комната: сервант с хрусталём, радиола на ножках, семья вокруг."""
    s = f'<rect width="{W}" height="{H}" fill="#8a7458"/>'
    for i in range(14):
        s += SL(Z_DAL, f'<rect x="{i*140}" width="128" height="{H}" fill="#96806a"'
                       f' opacity="{.3 if i%2 else .12}"/>')
    s += SL(Z_SRED, polovicy(930, "url(#pol)"))
    s += SL(Z_SRED, f'<rect x="60" y="930" width="1200" height="150" rx="12" fill="#7a3a3c" opacity=".6"/>')
    s += teplo(1000, 520, 760, 460, .5)
    # сервант с хрусталём
    s += SL(Z_SRED, f'<rect x="80" y="280" width="620" height="650" rx="12" fill="#8a6440" {o(8)}/>'
                    f'<rect x="120" y="330" width="540" height="330" rx="8" fill="#bcd8e8" opacity=".35" {o(5)}/>')
    for i in range(5):
        bl = .4 + .5 * abs(A.w(t, 1.4, i * .4))
        s += SL(Z_SRED, f'<path d="M{180+i*110},520 q30,-70 60,0 q-30,40 -60,0 Z" fill="#eaf4ff"'
                        f' opacity="{bl:.2f}" {o(3)}/>'
                        f'<rect x="{204+i*110}" y="520" width="12" height="60" fill="#eaf4ff" opacity="{bl:.2f}"/>')
    # радиола на ножках
    s += SL(Z_SRED, f'<rect x="820" y="600" width="640" height="260" rx="14" fill="#6d4a2a" {o(8)}/>'
                    f'<rect x="860" y="650" width="260" height="160" rx="10" fill="#c9b48a" opacity=".7" {o(5)}/>')
    for lx in (860, 1400):
        s += SL(Z_SRED, f'<rect x="{lx}" y="860" width="24" height="120" fill="#5c4028" {o(4)}'
                        f' transform="rotate({-8 if lx<1000 else 8} {lx+12} 860)"/>')
    # пластинка опускается (предмет сам)
    k = A.ease(A.seg(t, .8, 1.4))
    s += SL(Z_SRED, f'<circle cx="1280" cy="{400+260*k:.0f}" r="110" fill="#1d1a1c" {o(5)}/>'
                    f'<circle cx="1280" cy="{400+260*k:.0f}" r="34" fill="#e8d6a8"/>')
    # семья силуэтами
    for i, cx in enumerate((1620, 1760)):
        s += SL(Z_PERED, figura(cx, 1070, 420 + i * 40, t, "#2f2a30", "#ffd9a0", (i == 1), i * .4, True))
    s += vinetka(.46)
    return s


def igla_na_plastinke(t):
    """Крупно игла в бороздке; из бороздки встаёт золотая лента-голос."""
    s = f'<rect width="{W}" height="{H}" fill="#14110f"/>'
    s += teplo(760, 760, 620, 380, .6)
    # пластинка крупно
    a = (t * 40) % 360
    s += SL(Z_SRED, f'<circle cx="700" cy="900" r="620" fill="#1d1a1c" {o(8)}/>')
    for i in range(14):
        s += SL(Z_SRED, f'<circle cx="700" cy="900" r="{200+i*30}" fill="none" stroke="#2f2b2e"'
                        f' stroke-width="5" opacity=".85"/>')
    s += SL(Z_SRED, f'<g transform="rotate({a:.0f} 700 900)">'
                    f'<circle cx="700" cy="900" r="170" fill="#e8d6a8" {o(5)}/></g>')
    # блик по пластинке
    s += SL(Z_SRED, f'<ellipse cx="{460+60*A.w(t,.5):.0f}" cy="640" rx="260" ry="60" fill="#ffffff"'
                    f' opacity=".10" transform="rotate(-24 460 640)"/>')
    # игла в бороздке
    s += SL(Z_SRED, f'<g transform="rotate(-18 1180 540)">'
                    f'<rect x="1020" y="520" width="420" height="30" rx="12" fill="#9aa0a2" {o(6)}/>'
                    f'<path d="M1020,550 l-36,60 l54,-26 Z" fill="#cfd6de" {o(4)}/></g>')
    # лента-голос поднимается
    k = A.seg(t, .4, 3.0)
    pts = [(1000, 600), (1080, 440), (980, 300), (1120, 180), (1040, 80)]
    s += nit_shepota(pts[:max(2, int(2 + 3 * k))], t, .9, "#f0cf7a", 9.0)
    # пылинка скачет
    s += (f'<circle cx="{1300+40*A.w(t,2.0):.0f}" cy="{420+30*abs(A.w(t,3.0)):.0f}" r="5"'
          f' fill="#ffe9bc" opacity=".8"/>')
    s += vinetka(.52)
    return s


def girlyanda_iz_treh_tancev(t):
    """Гирлянда через три картинки: танцплощадка, свадьба, кухня с магнитофоном."""
    s = f'<rect width="{W}" height="{H}" fill="#1a1620"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#221c2a" {o(0)}/>')
    # три картинки (третья уходит под окно вставки — ставим левее)
    ramki = ((60, 300), (660, 360), (1260, 300))
    for i, (x, y) in enumerate(ramki):
        zg = A.ease(A.seg(t, .4 + i * 1.2, .8))
        s += SL(Z_SRED, f'<rect x="{x}" y="{y}" width="540" height="400" rx="12" fill="#2f2a36"'
                        f' {o(7)}/>')
        s += SL(Z_SRED, f'<rect x="{x+16}" y="{y+16}" width="508" height="368" rx="8"'
                        f' fill="#3a3344" opacity="{.4+.6*zg:.2f}"/>')
        if i == 0:        # танцплощадка: пары кружатся
            for j in range(3):
                a = math.radians(t * 70 + j * 120)
                px = x + 270 + math.cos(a) * 140
                py = y + 230 + math.sin(a) * 70
                s += SL(Z_SRED, f'<g opacity="{zg:.2f}">{siluet(px, py + 90, 160, "#161320", .95)}'
                                f'{siluet(px + 40, py + 90, 150, "#161320", .95, platok=True)}</g>')
        elif i == 1:      # свадьба во дворе
            s += SL(Z_SRED, f'<g opacity="{zg:.2f}">{siluet(x+220, y+330, 230, "#161320", .95)}'
                            f'{siluet(x+320, y+330, 220, "#161320", .95, platok=True)}'
                            f'<path d="M{x+120},{y+340} h300" stroke="#6d4a2a" stroke-width="12"/></g>')
        else:             # кухня с магнитофоном: катушки крутятся
            s += SL(Z_SRED, f'<g opacity="{zg:.2f}">'
                            f'<rect x="{x+140}" y="{y+180}" width="260" height="150" rx="12"'
                            f' fill="#6b6150" {o(5)}/>')
            for j, kx in enumerate((x + 200, x + 330)):
                aa = (t * 180 + j * 60) % 360
                s += SL(Z_SRED, f'<g transform="rotate({aa:.0f} {kx} {y+250})">'
                                f'<circle cx="{kx}" cy="{y+250}" r="46" fill="#2f2b2e" {o(4)}/>'
                                f'<rect x="{kx-46}" y="{y+244}" width="92" height="10" fill="#8a7a62"/></g>')
            s += SL(Z_SRED, "</g>")
    # гирлянда поверх
    s += SL(Z_PERED, f'<path d="M-20,200 q480,{160+16*A.w(t,.5):.0f} 960,0'
                     f' q480,{-160-16*A.w(t,.5,.5):.0f} 980,120" fill="none" stroke="#3a3344"'
                     f' stroke-width="8"/>')
    for i in range(16):
        lx = 40 + i * 120
        ly = 200 + 150 * math.sin(math.pi * (i / 15)) * (1 if i < 8 else -1) + 60
        bl = .35 + .6 * abs(A.w(t, 1.4, i * .3))
        s += SL(Z_PERED, f'<circle cx="{lx}" cy="{ly:.0f}" r="16" fill="#ffd27a" opacity="{bl:.2f}"/>'
                         f'<circle cx="{lx}" cy="{ly:.0f}" r="40" fill="url(#teplo)" opacity="{bl*.5:.2f}"/>')
    s += vinetka(.5)
    return s


def estrada_shestidesyatyh(t):
    """Эстрада: занавес расходится, оркестр силуэтом, певица у микрофона."""
    s = f'<rect width="{W}" height="{H}" fill="#140f16"/>'
    # сцена и рампа
    s += SL(Z_DAL, f'<rect y="300" width="{W}" height="780" fill="#2a2430" {o(0)}/>')
    s += SL(Z_SRED, f'<rect y="960" width="{W}" height="40" fill="#6b5a3c" {o(5)}/>')
    for i in range(14):
        bl = .5 + .4 * abs(A.w(t, 1.2, i * .3))
        s += SL(Z_SRED, f'<circle cx="{80+i*140}" cy="1000" r="22" fill="#ffd27a" opacity="{bl:.2f}"/>')
    # занавес расходится
    k = A.ease(A.seg(t, .4, 2.0))
    for storona in (-1, 1):
        x0 = 0 if storona < 0 else W
        for i in range(6):
            w_ = 170
            x = (x0 + storona * (i * w_ - 520 * k)) - (w_ if storona > 0 else 0)
            kach = 8 * A.w(t, .45, i * .4)
            s += SL(Z_PERED, f'<path d="M{x+kach:.0f},-20 q40,540 {-10:.0f},1120 h{w_}'
                             f' q10,-580 -30,-1120 Z" fill="#5a1f2c" {o(6)}/>')
    # оркестр силуэтом
    for i in range(6):
        s += SL(Z_SRED, f'<g opacity=".85">{siluet(220 + i * 130, 980, 230, "#120f16", .95)}</g>')
    # дирижёр взмахивает
    vz = 20 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<path d="M160,780 q40,{-60+vz:.0f} 80,{-20+vz:.0f}" fill="none"'
                    f' stroke="#120f16" stroke-width="14" stroke-linecap="round"/>')
    # певица в платье колоколом у микрофона
    s += SL(Z_SRED, f'<rect x="1193" y="520" width="14" height="440" fill="{ZHELEZ}" {o(4)}/>'
                    f'<ellipse cx="1200" cy="500" rx="34" ry="44" fill="#3a3f48" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1080,960 q120,-320 240,0 Z" fill="#2a2430" {o(8)}/>')
    s += SL(Z_SRED, figura(1200, 760, 300, t, "#2a2430", "#ffd9a0", False, .2, True))
    s += vinetka(.5)
    return s


def semya_poet_za_stolom(t):
    """Стол сбоку: семья поёт, дядя с гармонью, над столом плывут ноты."""
    s = f'<rect width="{W}" height="{H}" fill="#6d5a44"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 92))
    s += f'<rect width="{W}" height="{H}" fill="#2b2016" opacity=".3"/>'
    # абажур качается
    kach = 4 * A.w(t, .5)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 960 60)">'
                    f'<rect x="952" y="0" width="16" height="200" fill="#6b6150" {o(3)}/>'
                    f'<path d="M820,200 h280 l-60,-110 h-160 Z" fill="#c9683c" {o(7)}/></g>')
    s += teplo(960, 420, 760, 460, .7)
    # стол сбоку
    s += SL(Z_SRED, f'<rect x="120" y="760" width="1680" height="40" rx="10" fill="url(#derev)" {o(7)}/>'
                    f'<rect x="200" y="800" width="36" height="260" fill="#7d5636" {o(5)}/>'
                    f'<rect x="1680" y="800" width="36" height="260" fill="#7d5636" {o(5)}/>')
    # поющие: рты открыты (овалы), головы покачиваются
    for i, cx in enumerate((300, 520, 1300, 1560)):
        kiv = 5 * A.w(t, .9, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({kiv:.1f} {cx} 760)">'
                        f'{figura(cx, 760, 420, t, "#2f2a30", "#ffd9a0", (i % 2 == 0), i * .3, True)}'
                        f'<ellipse cx="{cx+30}" cy="{760-420*.80:.0f}" rx="16"'
                        f' ry="{16+8*abs(A.w(t,1.8,i*.3)):.0f}" fill="#2a1a1a"/></g>')
    # дядя с гармонью
    gx = 880
    rast = 1 + .18 * A.w(t, 1.2)
    s += SL(Z_SRED, figura(gx, 760, 440, t, "#2f2a30", "#ffd9a0", False, .5, True))
    s += SL(Z_SRED, f'<g transform="translate({gx-10},560) scale({rast:.2f},1)">'
                    f'<rect x="-120" y="0" width="90" height="150" rx="12" fill="#8a3a34" {o(6)}/>'
                    f'<rect x="30" y="0" width="90" height="150" rx="12" fill="#8a3a34" {o(6)}/>'
                    f'<path d="M-30,10 l60,0 l0,130 l-60,0 Z" fill="#c9a86a" {o(4)}/></g>')
    # дед отбивает такт ложкой
    lo = 16 * abs(A.w(t, 2.6))
    s += SL(Z_SRED, f'<path d="M1120,{700-lo:.0f} q40,-30 70,10" fill="none" stroke="#2f2a30"'
                    f' stroke-width="18" stroke-linecap="round"/>')
    # ноты плывут
    for i in range(7):
        rnd = random.Random(1900 + i)
        ph = rnd.random()
        k = (t * .25 + ph) % 1.0
        nx = 300 + rnd.randint(0, 1300) + 60 * A.w(t, .7, ph)
        ny = 700 - 560 * k
        s += (f'<g opacity="{.75*(1-k*.6):.2f}" transform="translate({nx:.0f},{ny:.0f})">'
              f'<ellipse cx="0" cy="0" rx="18" ry="13" fill="#f2ead6" transform="rotate(-20)"/>'
              f'<rect x="14" y="-56" width="7" height="56" fill="#f2ead6"/></g>')
    s += vinetka(.46)
    return s


def zapevala(t):
    """Крупно бабушка запевает; от неё идёт нота-огонёк, вокруг ещё пять."""
    s = f'<rect width="{W}" height="{H}" fill="#1d1620"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 96))
    s += f'<rect width="{W}" height="{H}" fill="#120e14" opacity=".55"/>'
    s += teplo(760, 640, 620, 460, .75)
    # бабушка крупно
    s += figura(760, 1080, 900, t, "#2f2a30", "#ffd9a0", True, .1, True)
    # щека подперта: линия руки
    s += (f'<path d="M900,860 q70,-60 56,-150" fill="none" stroke="#2f2a30" stroke-width="30"'
          f' stroke-linecap="round"/>')
    # поёт: рот
    s += (f'<ellipse cx="820" cy="{1080-900*.80:.0f}" rx="22"'
          f' ry="{22+10*abs(A.w(t,1.6)):.0f}" fill="#2a1a1a"/>')
    # слеза блестит
    sl = A.seg(t, 2.0, 2.4)
    s += (f'<ellipse cx="832" cy="{1080-900*.84+140*sl:.0f}" rx="7" ry="11" fill="#bcd8ea"'
          f' opacity="{.9*(1-sl*.5):.2f}"/>')
    # ноты-огоньки загораются по очереди
    s += ogonek_grudi(980, 520, t, 1.1, .0, .8)
    for i in range(5):
        k = A.ease(A.seg(t, 1.4 + i * .6, .6))
        if k <= .02:
            continue
        a = math.radians(-150 + i * 42)
        ox = 980 + math.cos(a) * 420
        oy = 520 + math.sin(a) * 260
        s += ogonek_grudi(ox, oy, t, .8 * k, i * .3, .5 * k)
    s += vinetka(.52)
    return s


# ═══════════════════ 8. ФИНАЛ ═══════════════════
def slovo_i_spichka(t):
    """Слово-искра и вспыхнувшая спичка улетают, их уже не вернуть."""
    s = f'<rect width="{W}" height="{H}" fill="#100d12"/>'
    s += teplo(960, 560, 700, 420, .4)
    k = A.seg(t, .6, 3.0)
    # слово-искра слева
    ix = 520 + 520 * k
    iy = 620 - 300 * k
    s += nit_shepota([(300, 760), (420, 700), (ix - 60, iy + 40), (ix, iy)], t, .8, sh=5)
    s += ogonek_grudi(ix, iy, t, 1.0, .0, .4)
    # спичка справа
    ch = A.ease(A.seg(t, .8, .6))
    sx = 1360 + 360 * k
    sy = 700 - 260 * k
    s += (f'<g transform="rotate({-28+40*k:.0f} {sx:.0f} {sy:.0f})">'
          f'<rect x="{sx-110:.0f}" y="{sy-9:.0f}" width="220" height="18" rx="8"'
          f' fill="#c9a86a" {o(5)}/></g>')
    if ch > .05:
        s += ogon(sx + 110, sy - 30, t, 1.1 * ch, .2, 4)
        s += teplo(sx + 110, sy - 40, 220 * ch, 180 * ch, .6 * ch)
    # силуэт тянется вслед и не достаёт
    s += SL(Z_PERED, figura(960, 1080, 620, t, "#1a1720", "#ffd08a", False, .2, False, .95))
    s += (f'<path d="M1030,760 q{160*k:.0f},{-120*k:.0f} {220*k:.0f},{-150*k:.0f}" fill="none"'
          f' stroke="#1a1720" stroke-width="26" stroke-linecap="round"/>')
    s += vinetka(.56)
    return s


def babushkiny_ladoni_i_lampa(t):
    """Огонёк керосиновой лампы прикрыт от сквозняка; рядом та же шкатулка."""
    s = f'<rect width="{W}" height="{H}" fill="#241a12"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 820, 92))
    s += f'<rect width="{W}" height="{H}" fill="#1a120b" opacity=".5"/>'
    s += SL(Z_SRED, f'<rect y="760" width="{W}" height="{H-760}" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M-20,750 q500,-40 1000,-12 q500,26 960,-10 V820 H-20 Z"'
                    f' fill="url(#rush)" {o(6)}/>')
    # лампа: огонёк сперва мечется, потом выравнивается
    rov = A.ease(A.seg(t, 1.2, 1.6))
    s += teplo(760, 600, 560 + 120 * rov, 440, .8)
    s += lampa(760, 760, t, 2.0)
    s += (f'<ellipse cx="760" cy="{600-20*rov:.0f}" rx="{30-10*rov:.0f}" ry="{48+14*rov:.0f}"'
          f' fill="{SVET}" opacity=".9"'
          f' transform="rotate({12*(1-rov)*A.w(t,2.4):.1f} 760 630)"/>')
    # заслон от сквозняка — платок на ширме, не рука
    s += SL(Z_SRED, f'<path d="M430,760 q60,-300 150,-330 q40,180 30,330 Z" fill="#8f3a38"'
                    f' opacity=".85" {o(7)}/>')
    # шкатулка из плана 2 — закрытая
    s += ten(1340, 790, 220, 20, .45)
    s += SL(Z_SRED, f'<rect x="1160" y="640" width="400" height="150" rx="12" fill="url(#derev)" {o(8)}/>'
                    f'<rect x="1160" y="624" width="400" height="36" rx="10" fill="#a9754a" {o(6)}/>'
                    f'<rect x="1320" y="690" width="80" height="60" rx="10" fill="url(#zol)" {o(5)}/>')
    # тень на стене
    s += SL(Z_DAL, f'<ellipse cx="1500" cy="420" rx="{240+30*A.w(t,.6):.0f}" ry="300"'
                   f' fill="#000" opacity=".25"/>')
    s += vinetka(.5)
    return s


def platok_pamyatka_na_stole(t):
    """Клетчатый платок под лампой, вид сверху: узелки светятся."""
    s = f'<rect width="{W}" height="{H}" fill="#3a2d20"/>'
    s += SL(Z_SRED, f'<rect width="{W}" height="{H}" fill="url(#derev)" {o(0)}/>')
    s += SL(Z_SRED, doski(-20, -20, W + 40, H + 40, 170, False))
    s += f'<rect width="{W}" height="{H}" fill="#1a120b" opacity=".35"/>'
    # круг света лампы
    s += SL(Z_SRED, f'<ellipse cx="960" cy="540" rx="820" ry="520" fill="url(#teplo)" opacity=".55"/>')
    # платок
    s += SL(Z_SRED, f'<path d="M300,180 q660,-50 1320,0 q60,380 -20,700 q-640,60 -1280,0'
                    f' q-80,-320 -20,-700 Z" fill="#d9cdb0" {o(8)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="{330+i*140}" y="170" width="16" height="720"'
                        f' fill="#a4553f" opacity=".4"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="300" y="{220+i*160}" width="1320" height="16"'
                        f' fill="#a4553f" opacity=".4"/>')
    # узелки светятся по очереди
    for i, (ux, uy) in enumerate(((330, 210), (1600, 210), (330, 860), (1600, 860))):
        sv = A.ease(A.seg(t, .4 + i * .5, .8))
        s += SL(Z_SRED, f'<circle cx="{ux}" cy="{uy}" r="{200*sv:.0f}" fill="url(#teplo)"'
                        f' opacity="{.5*sv:.2f}"/>')
        s += SL(Z_SRED, f'<circle cx="{ux}" cy="{uy}" r="46" fill="#cbbd9c" {o(6)}/>'
                        f'<circle cx="{ux}" cy="{uy}" r="20" fill="#9a8a68" opacity=".7"/>')
    # бахрома
    for i in range(16):
        kach = 5 * A.w(t, .7, i * .3)
        s += SL(Z_SRED, f'<path d="M{320+i*82},890 q{kach:.0f},30 {kach*1.4:.0f},54"'
                        f' stroke="#cbbd9c" stroke-width="8" fill="none" opacity=".85"/>')
    s += vinetka(.5)
    return s


def svecha_i_pustoy_stul(t):
    """Свеча на столе, пустой стул с пиджаком; дым складывается в вопрос."""
    s = f'<rect width="{W}" height="{H}" fill="#120e10"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 760, 92))
    s += f'<rect width="{W}" height="{H}" fill="#0d0a0c" opacity=".62"/>'
    s += SL(Z_SRED, f'<rect y="820" width="{W}" height="{H-820}" fill="url(#derev)" {o(7)}/>')
    s += teplo(620, 700, 560, 400, .8)
    s += svecha(620, 820, t, .0, 2.2)
    # дым складывается в знак вопроса
    k = A.ease(A.seg(t, 1.2, 2.4))
    s += dym(620, 680, t, 5, .22, 380, .26 * (1 - k * .6), wide=1.2)
    if k > .25:
        s += (f'<g opacity="{(k-.25)*1.2:.2f}" fill="none" stroke="#cfd6de" stroke-width="16"'
              f' stroke-linecap="round">'
              f'<path d="M560,520 q60,-110 140,-40 q56,50 -24,100 q-44,28 -44,74"/>'
              f'<circle cx="634" cy="700" r="12" fill="#cfd6de" stroke="none"/></g>')
    # пустой стул с пиджаком
    s += ten(1300, 1010, 220, 22, .45)
    s += SL(Z_SRED, f'<rect x="1160" y="760" width="300" height="30" rx="10" fill="url(#derev)" {o(6)}/>'
                    f'<rect x="1170" y="790" width="26" height="230" fill="#7d5636" {o(4)}/>'
                    f'<rect x="1424" y="790" width="26" height="230" fill="#7d5636" {o(4)}/>'
                    f'<rect x="1160" y="440" width="26" height="330" fill="#7d5636" {o(4)}/>'
                    f'<rect x="1424" y="440" width="26" height="330" fill="#7d5636" {o(4)}/>'
                    f'<rect x="1160" y="470" width="290" height="30" rx="10" fill="#7d5636" {o(4)}/>')
    spol = A.ease(A.seg(t, 2.6, 2.0))
    s += SL(Z_SRED, f'<g transform="translate({-10*spol:.0f},{26*spol:.0f}) rotate({-4*spol:.1f} 1300 600)">'
                    f'<path d="M1180,470 q120,-60 240,0 l20,300 q-140,50 -280,0 Z" fill="#4a4450" {o(7)}/>'
                    f'<path d="M1300,470 v300" stroke="#3a3540" stroke-width="8"/></g>')
    s += vinetka(.56)
    return s


def dom_i_mnogoetazhka_ryadom(t):
    """Сумерки: сельский дом с дымком и многоэтажка с одним тёплым окном."""
    s = nebo("sumer", t, True, 439)
    s += SL(Z_DAL, f'<path d="M-20,940 q520,-40 1000,-14 q500,22 960,-20 V{H} H-20 Z"'
                   f' fill="#e4edf6" {o(4)}/>')
    # общая дорога
    s += SL(Z_SRED, f'<path d="M-20,1080 q500,-150 960,-170 q460,-20 980,-40 l0,60'
                    f' q-520,20 -980,40 q-460,20 -960,170 Z" fill="#c3d2e4" {o(4)}/>')
    s += SL(Z_SRED, izba_snaruzhi(420, 950, 620, t, True, True, 37))
    s += SL(Z_SRED, dym(560, 560, t, 5, .2, 320, .3, wide=1.1))
    s += SL(Z_DAL, _panelka(1500, 980, 700, t, 7, False, 443))
    # одно тёплое окно
    zg = A.ease(A.seg(t, .8, 1.4))
    s += SL(Z_DAL, f'<rect x="1560" y="640" width="90" height="64" rx="8" fill="{SVET}"'
                   f' opacity="{.25+.7*zg:.2f}" {o(4)}/>')
    s += SL(Z_DAL, f'<circle cx="1605" cy="672" r="{160*zg:.0f}" fill="url(#teplo)" opacity="{.4*zg:.2f}"/>')
    s += sneg_letit(t, 30, 449, .55, .7)
    s += vinetka(.46)
    return s


def podokonnik_s_koshkoy_i_svechoy(t):
    """На подоконнике собирается кадр: миска картошки, свеча, кошка."""
    s = f'<rect width="{W}" height="{H}" fill="#2a2219"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, 700, 90))
    s += f'<rect width="{W}" height="{H}" fill="#1c150e" opacity=".42"/>'
    # окно с ночью
    vid = (f'<rect width="900" height="420" fill="#1e2a40"/>'
           f'<circle cx="700" cy="110" r="46" fill="#f6efd8" opacity=".9"/>')
    s += SL(Z_DAL, okno_izby(520, 120, 900, 420, t, vid, .2, False, True))
    s += SL(Z_SRED, f'<rect x="300" y="640" width="1320" height="56" rx="12" fill="url(#derev)" {o(7)}/>')
    s += teplo(880, 640, 700, 380, .7)
    # миска картошки с паром
    k1 = A.out(A.seg(t, .2, .8))
    s += SL(Z_SRED, f'<g opacity="{k1:.2f}">'
                    f'<path d="M420,640 q140,-40 280,0 q-40,86 -140,86 q-100,0 -140,-86 Z"'
                    f' fill="url(#glina)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<ellipse cx="{500+i*62}" cy="614" rx="48" ry="32" fill="#b58a52" {o(4)}/>')
    s += SL(Z_SRED, "</g>")
    if k1 > .4:
        s += par(560, 580, t, 5, .5, 240, .45 * k1, wide=1.3)
    # свеча
    k2 = A.out(A.seg(t, 1.2, .8))
    if k2 > .05:
        s += f'<g opacity="{k2:.2f}">{svecha(1000, 640, t, .0, 1.8)}</g>'
    # кошка вытянулась
    k3 = A.out(A.seg(t, 2.2, 1.0))
    if k3 > .05:
        s += SL(Z_SRED, f'<g opacity="{k3:.2f}" transform="translate(1320,640) scale({.9+.3*k3:.2f},1)">'
                        f'<ellipse cx="0" cy="-40" rx="200" ry="56" fill="#8a7a62" {o(7)}/>'
                        f'<circle cx="-180" cy="-70" r="56" fill="#8a7a62" {o(6)}/>'
                        f'<path d="M-230,-110 l16,-56 l48,40 Z" fill="#8a7a62" {o(4)}/>'
                        f'<path d="M-150,-120 l10,-50 l44,36 Z" fill="#8a7a62" {o(4)}/>'
                        f'<path d="M190,-60 q90,-20 70,50 q-60,24 -78,-30 Z" fill="#8a7a62" {o(5)}/>'
                        f'<circle cx="-212" cy="-62" r="7" fill="#2a2219"/></g>')
    s += vinetka(.48)
    return s


def ulica_v_ranney_temnote(t):
    """Улица: окна зажигаются, из форточек кружат золотые искры-слова."""
    s = nebo("noch", t, True, 457)
    s += SL(Z_DAL, _ulica_dal(60, 820, 1840, t, True, 461))
    s += SL(Z_SRED, f'<path d="M-20,1000 q520,-50 1000,-20 q500,26 960,-24 V{H} H-20 Z"'
                    f' fill="#e4edf6" {o(4)}/>')
    doma = ((180, 940, 420), (720, 960, 460), (1320, 950, 440))
    for i, (x, b, w_) in enumerate(doma):
        s += SL(Z_SRED, izba_snaruzhi(x, b, w_, t, False, True, 7 + i * 6))
        zg = A.ease(A.seg(t, .4 + i * .7, .8))
        s += SL(Z_SRED, f'<rect x="{x-60}" y="{b-250}" width="110" height="80" rx="8" fill="{SVET}"'
                        f' opacity="{.2+.7*zg:.2f}" {o(4)}/>')
        s += SL(Z_SRED, f'<circle cx="{x-5}" cy="{b-210}" r="{180*zg:.0f}" fill="url(#teplo)"'
                        f' opacity="{.35*zg:.2f}"/>')
        # искры кружат над своим домом
        for j in range(3):
            a = 2 * math.pi * ((t * .22 + j / 3 + i * .2) % 1.0)
            ox = x + math.cos(a) * (120 + j * 26)
            oy = b - 420 + math.sin(a) * (50 + j * 14)
            s += ogonek_grudi(ox, oy, t, .34, j * .3, .3)
    s += sneg_letit(t, 26, 463, .5, .6)
    s += vinetka(.48)
    return s


def nebo_nad_kryshami_iskra_zvezda(t):
    """Искра поднимается над крышами и становится звездой среди других."""
    s = nebo("noch", t, True, 467)
    # крыши силуэтом
    d = "M-20,900"
    rnd = random.Random(13)
    x = -20
    while x < W + 40:
        w_ = rnd.randint(140, 260)
        hh = rnd.randint(60, 190)
        d += f" V{900-hh} h{w_} V900"
        x += w_
    d += f" L{W+40},{H} H-20 Z"
    s += SL(Z_SRED, f'<path d="{d}" fill="#12182a" {o(0)}/>')
    for i, tx in enumerate((300, 760, 1260, 1660)):
        s += SL(Z_SRED, f'<rect x="{tx}" y="{700+i%2*40}" width="36" height="90" fill="#0f1420"/>')
        s += SL(Z_SRED, dym(tx + 18, 690 + i % 2 * 40, t, 4, .18, 300, .22, wide=1.2))
    # звёзды
    for i in range(22):
        rnd2 = random.Random(1900 + i)
        zx, zy = rnd2.randint(40, W - 40), rnd2.randint(60, 520)
        mg = .4 + .5 * abs(A.w(t, .6 + rnd2.random(), rnd2.random()))
        s += f'<circle cx="{zx}" cy="{zy}" r="{rnd2.uniform(2,3.6):.1f}" fill="#fff6e2" opacity="{mg:.2f}"/>'
    # искра поднимается и становится звездой
    k = A.ease(A.seg(t, .2, 2.4))
    ix = 960 + 60 * A.w(t, .9)
    iy = 900 - 620 * k
    if k < .94:
        s += f'<circle cx="{ix:.0f}" cy="{iy:.0f}" r="{11-5*k:.0f}" fill="#ffd27a" opacity="{1-.2*k:.2f}"/>'
        s += f'<circle cx="{ix:.0f}" cy="{iy:.0f}" r="{34-12*k:.0f}" fill="url(#teplo)" opacity=".5"/>'
    else:
        bl = .6 + .4 * abs(A.w(t, 1.2))
        s += (f'<circle cx="960" cy="280" r="{9*bl:.0f}" fill="#fff6e2"/>'
              f'<circle cx="960" cy="280" r="{48*bl:.0f}" fill="url(#teplo)" opacity=".6"/>')
    s += sneg_letit(t, 14, 479, .3, .45)
    s += vinetka(.46)
    return s
