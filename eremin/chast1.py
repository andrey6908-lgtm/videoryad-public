# -*- coding: utf-8 -*-
"""Декорации 1-34 ролика «17 ноября — Ерёмин день»."""
import math, random
from baza import *
import anim as A
from lok_obshchee import *


def izba_v_noyabrskih_sumerkah(t):
    """Изба на две трети кадра: резные наличники, труба с дымом, тёплое окно.
    Внука втягивают в приоткрытую дверь, дверь захлопывается.

    Этот же кадр закрывает ролик плашкой «Оставайтесь у своего огня», поэтому
    ЖИВОЙ ОГОНЬ в кадре обязателен: фонарь у крыльца с пляшущим пламенем,
    густой дым столбом из трубы и дышащий свет в окне (осмотр 14.11)."""
    rnd = random.Random(117)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 17)
    s += oblaka(t, 150, 4, 19, .28, "#c3cedd", 12.0)
    s += ulica_dal(20, 806, 780, t, False, 21)
    s += SL(Z_DAL, gryaz_polosa(858, 120, "#43392f"))
    bx, bw, base = 470, 1070, 918
    izb = brevna(bx, base - 420, bw, 420, 84)
    izb += (f'<path d="M{bx-98},{base-418} L{bx+bw/2:.0f},{base-704}'
            f' L{bx+bw+98},{base-418} Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<path d="M{bx-98},{base-412} L{bx+bw/2:.0f},{base-698}'
            f' L{bx+bw+98},{base-412} l-54,-36 L{bx+bw/2:.0f},{base-650}'
            f' L{bx-44},{base-448} Z" fill="url(#sneg)" {o(5)}/>')
    for i in range(7):
        izb += (f'<path d="M{bx-64+i*48:.0f},{base-438+i*36:.0f} l26,19 l-26,19 Z"'
                f' fill="{MED}" opacity=".82" {o(3)}/>')
        izb += (f'<path d="M{bx+bw+64-i*48:.0f},{base-438+i*36:.0f} l-26,19 l26,19 Z"'
                f' fill="{MED}" opacity=".82" {o(3)}/>')
    izb += (f'<rect x="{bx+bw*.58:.0f}" y="{base-742}" width="86" height="150"'
            f' fill="url(#kamen)" {o(6)}/>'
            f'<rect x="{bx+bw*.56:.0f}" y="{base-756}" width="118" height="26" rx="6"'
            f' fill="{KAMEN2}" {o(5)}/>')
    s += SL(Z_DAL, izb)
    # ДЫМ СТОЛБОМ: густой, в три слоя, до самого верха кадра
    trx = bx + bw * .62
    s += SL(Z_DAL, dym(trx, base - 762, t, 7, .22, 560, .52, "#dde4ec", 1.5))
    s += SL(Z_DAL, dym(trx + 16, base - 766, t, 5, .16, 640, .34, "#eef3f8", 2.1))
    for j in range(9):                        # ровный столб над трубой
        yy = base - 770 - j * 56
        rr = 40 - j * 1.6 + 5 * A.w(t, 6.0, j * .09)
        s += SL(Z_DAL, f'<ellipse cx="{trx+5*A.w(t,7.0,j*.12):.0f}" cy="{yy:.0f}"'
                       f' rx="{max(9, rr):.0f}" ry="{max(11, rr*1.15):.0f}"'
                       f' fill="#d6dde6" opacity="{.5-j*.045:.2f}"/>')
    okx, oky = bx + 76, base - 346
    okn = okno_izby(okx, oky, 268, 206, t, svet=True, moroz=.32)
    for sgn in (-1, 1):
        okn += (f'<path d="M{okx+134+sgn*162:.0f},{oky-30}'
                f' l{-sgn*22},0 l0,266 l{sgn*22},0 Z" fill="url(#derev)" {o(5)}/>')
        okn += (f'<path d="M{okx+134+sgn*150:.0f},{oky+40} q{-sgn*34},34 0,68"'
                f' fill="none" stroke="{MED}" stroke-width="7"/>')
    okn += (f'<path d="M{okx-44},{oky-34} h356 l-30,-40 h-296 Z" fill="url(#derev)" {o(6)}/>')
    for i in range(6):
        okn += (f'<circle cx="{okx-14+i*62:.0f}" cy="{oky-54}" r="9" fill="{MED}"'
                f' opacity=".85" {o(2)}/>')
    s += SL(Z_SRED, okn)
    # СВЕТ В ОКНЕ ЖИВОЙ: дышит, и за стеклом видно пламя
    dysh = .72 + .22 * abs(A.w(t, 1.5, .1))
    s += SL(Z_SRED, f'<rect x="{okx:.0f}" y="{oky:.0f}" width="268" height="206"'
                    f' fill="{SVET}" opacity="{.42*dysh:.2f}"/>')
    s += SL(Z_SRED, ogon(okx + 134, oky + 170, t, .52, .3, 4))
    s += SL(Z_SRED, teplo(okx + 134, oky + 104, 420, 340, .46 * dysh))
    kr = (f'<path d="M{bx+bw*.62:.0f},{base} h420 l-44,-126 h-376 Z"'
          f' fill="url(#dosk)" {o(7)}/>')
    kr += (f'<path d="M{bx+bw*.66:.0f},{base-126} h340 l0,-24 h-340 Z" fill="{DOSKA2}" {o(5)}/>')
    for i in range(3):
        kr += (f'<rect x="{bx+bw*.64+i*18:.0f}" y="{base-96+i*34:.0f}"'
               f' width="{366-i*34:.0f}" height="26" rx="5" fill="url(#dosk)" {o(4)}/>')
    kr += (f'<rect x="{bx+bw*.98:.0f}" y="{base-470}" width="24" height="346"'
           f' fill="url(#derev)" {o(5)}/>')
    kr += (f'<path d="M{bx+bw*.60:.0f},{base-470} h430 l-28,-56 h-374 Z"'
           f' fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_SRED, kr)
    zahl = A.ease(A.seg(t, 1.2, 1.3))
    dx_, dy_, dw, dh = bx + bw * .70, base - 452, 230, 330
    s += SL(Z_SRED, dver(dx_, dy_, dw, dh, (1 - zahl) * .62, kruchok=True))
    s += SL(Z_SRED, grozd_ryabiny(dx_ + dw * .5, dy_ + 92, t, .72, 13, 8, .2))
    s += SL(Z_SRED, podkova(dx_ + dw * .5, dy_ - 42, .72, t))
    # ФОНАРЬ НА СТОЛБЕ У ВОРОТ: главное тёплое пятно финала. Стоит у самого
    # правого края нарочно — в плане 130 середину кадра занимает памятка из
    # пяти карточек, и огонь в центре зритель бы просто не увидел.
    fx_, fy_ = 1742, base - 250
    s += SL(Z_SRED, f'<rect x="{fx_-13:.0f}" y="{fy_+16:.0f}" width="26" height="320"'
                    f' rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_-9:.0f},{fy_-200:.0f} h18 l0,92 h-18 Z"'
                    f' fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_-48:.0f},{fy_-110:.0f} h96 l-14,-40 h-68 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_-40:.0f},{fy_-110:.0f} h80 l-9,120 h-62 Z"'
                    f' fill="url(#stekl)" opacity=".7" {o(6)}/>')
    s += SL(Z_SRED, ogon(fx_, fy_ - 10, t, .66, .1, 6))
    s += SL(Z_SRED, teplo(fx_, fy_ - 50, 460, 400, .52 + .14 * abs(A.w(t, 1.3))))
    s += SL(Z_SRED, iskra_let(t, fx_, fy_ - 60, 6, 23, 260, .4))
    tyan = A.out(A.seg(t, .4, 1.1))
    gx = dx_ + dw * 1.26 - tyan * 150
    s += SL(Z_SRED, figura(gx, base + 6, 300, t, "#33293c", "#ffd98a", False, .4, True))
    s += SL(Z_SRED, para_izo_rta(gx + 34, base - 262, t, .1, .9, .5))
    s += SL(Z_SRED, figura(dx_ + dw * .40, base + 4, 400, t, "#3a2c3c", "#ffe2a8", True, .0))
    ruk, (rx2, ry2) = rukav(dx_ + dw * .56, base - 290, 150, 12 - 24 * tyan, t, "#8f353c", "#ffd98a", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{rx2:.0f}" cy="{ry2:.0f}" rx="26" ry="19" fill="#8f353c" {o(4)}/>')
    pl = (f'<path d="M{bx-280},{base+8} q180,-30 360,-6 l10,164 h-380 Z"'
          f' fill="#2c2a2d" opacity=".9"/>')
    for i in range(5):
        pl += (f'<rect x="{bx-258+i*70:.0f}" y="{base+22}" width="16" height="150"'
               f' rx="6" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_PERED, pl)
    s += SL(Z_PERED, goloe_derevo(220, base + 40, 520, t, 9, 7, "#2a2b33"))
    s += SL(Z_LETIT, mokryy_sneg(t, 30, 13, .62, 1.0))
    s += vinetka(.44)
    return s


def erema_na_lavke_u_pechi(t):
    """Ерёма на широкой лавке у печи тянется к шапке на крючке, но перед ним
    ставят миску с пирогами. Кот трётся о лапоть."""
    rnd = random.Random(205)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 5)
    s += SL(Z_DAL, brevna(0, 60, W, 740, 92))
    s += SL(Z_DAL, okno_izby(1500, 230, 300, 210, t, svet=False, moroz=.5))
    s += utvar_izby(1180, 400, 540, t, 7)
    s += SL(Z_SRED, polovicy(856))
    s += SL(Z_SRED, pech(40, 236, 520, 620, t, True, True, False))
    s += SL(Z_SRED, teplo(300, 620, 520, 430, .44 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, iskra_let(t, 300, 560, 8, 31, 300, .42))
    s += SL(Z_SRED, lavka(600, 742, 900))
    ex, ey = 980, 742
    er = (f'<path d="M{ex-168},{ey} q14,-230 150,-242 q136,12 150,242 Z"'
          f' fill="#44506b" {o(7)}/>')
    er += (f'<path d="M{ex-150},{ey-150} q150,36 300,0" fill="none"'
           f' stroke="#8f2f33" stroke-width="22" stroke-linecap="round"/>')
    er += (f'<path d="M{ex-150},{ey-150} q150,36 300,0" fill="none"'
           f' stroke="{ZOL}" stroke-width="6" opacity=".6"/>')
    nak = 13 * A.w(t, 1.6, .1)
    er += (f'<g transform="rotate({nak:.2f} {ex:.0f} {ey-250:.0f})">'
           f'<ellipse cx="{ex}" cy="{ey-318}" rx="74" ry="80" fill="#e0b08a" {o(6)}/>'
           f'<path d="M{ex-78},{ey-372} q78,-54 156,0 q-10,-72 -78,-74 q-68,2 -78,74 Z"'
           f' fill="#4a3a2c" {o(5)}/>'
           f'<path d="M{ex-66},{ey-298} q66,118 132,0 q-8,96 -66,104 q-58,-8 -66,-104 Z"'
           f' fill="#6b5340" {o(5)}/>'
           f'<circle cx="{ex-30}" cy="{ey-330}" r="{3.0 if A.blink(t, 3.4) else 7.0}" fill="{K}"/>'
           f'<circle cx="{ex+32}" cy="{ey-330}" r="{3.0 if A.blink(t, 3.4) else 7.0}" fill="{K}"/>'
           f'<ellipse cx="{ex-52}" cy="{ey-306}" rx="18" ry="11" fill="#d1685a" opacity=".55"/>'
           f'<ellipse cx="{ex+54}" cy="{ey-306}" rx="18" ry="11" fill="#d1685a" opacity=".55"/></g>')
    for i, sgn in enumerate((-1, 1)):
        er += (f'<path d="M{ex+sgn*74},{ey-70} l{sgn*96},34 l0,52 l{-sgn*96},-20 Z"'
               f' fill="#4a506b" {o(5)}/>')
        er += (f'<path d="M{ex+sgn*150},{ey+4} q{sgn*62},6 {sgn*72},50'
               f' q{-sgn*66},18 {-sgn*96},-12 Z" fill="url(#solom)" {o(5)}/>')
        for j in range(4):
            er += (f'<path d="M{ex+sgn*152+j*sgn*18:.0f},{ey+12} l0,34"'
                   f' stroke="#a07c2e" stroke-width="5"/>')
    s += SL(Z_SRED, er)
    tyan = A.w(t, 1.9, .05)
    ruk, (hx, hy) = rukav(ex + 120, ey - 240, 150, -56 + 22 * tyan, t, "#3c4760", "#ffd98a", .2, 9.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="24" ry="17" fill="#3c4760" {o(4)}/>')
    shx, shy = ex + 286, ey - 404
    sh = (f'<path d="M{shx-8},{shy} h46" stroke="url(#zhel)" stroke-width="12"'
          f' stroke-linecap="round"/>')
    kach = 4.0 * A.w(t, 2.4, .3)
    sh += (f'<g transform="rotate({kach:.2f} {shx+34:.0f} {shy:.0f})">'
           f'<path d="M{shx-18},{shy+72} q52,-96 104,0 q-52,22 -104,0 Z" fill="#53402e" {o(5)}/>'
           f'<path d="M{shx-26},{shy+70} q58,30 118,0 l-6,30 q-54,24 -106,0 Z"'
           f' fill="#7a6246" {o(5)}/></g>')
    s += SL(Z_SRED, sh)
    s += SL(Z_SRED, stol(560, 700, 330, 30))
    put = A.out(A.seg(t, .5, 1.0))
    mx, my = 700, 668 - 0 + (1 - put) * -120
    mis = (f'<path d="M{mx-96},{my} q96,96 192,0 q-96,30 -192,0 Z" fill="url(#glina)" {o(6)}/>')
    for i in range(3):
        mis += (f'<ellipse cx="{mx-54+i*54:.0f}" cy="{my-20-((i%2)*16):.0f}" rx="46" ry="26"'
                f' fill="url(#med)" {o(5)}/>')
        mis += (f'<path d="M{mx-84+i*54:.0f},{my-30-((i%2)*16):.0f} q30,-14 60,0"'
                f' fill="none" stroke="#f2cf8c" stroke-width="6" opacity=".7"/>')
    s += SL(Z_SRED, mis)
    s += SL(Z_SRED, par(mx, my - 54, t, 5, .5, 190, .52, .9))
    s += SL(Z_SRED, kot(760, 884, t, .78, "#3b3430"))
    s += SL(Z_PERED, ramka_pp("levo", "#0d0b0a", .5))
    s += SL(Z_PERED, krynka(1690, 940, 1.35))
    s += vinetka(.42)
    return s


def izba_vse_pri_dele(t):
    """Изба в разрезе, как кукольный дом: веретено крутится, шило ходит,
    стружка летит, горошины катятся по столу."""
    rnd = random.Random(309)
    s = f'<rect width="{W}" height="{H}" fill="#2b2119"/>'
    s += nebo("sumer", t, True, 23)
    s += SL(Z_DAL, brevna(70, 70, 1780, 900, 96))
    s += SL(Z_DAL, f'<rect x="70" y="70" width="1780" height="900" fill="none" {o(10)}/>')
    s += SL(Z_DAL, f'<line x1="960" y1="70" x2="960" y2="970" stroke="#4e3220" stroke-width="22"/>'
                   f'<line x1="70" y1="520" x2="1850" y2="520" stroke="#4e3220" stroke-width="22"/>')
    s += SL(Z_SRED, pech(830, 300, 270, 400, t, True, True, False))
    s += SL(Z_SRED, teplo(964, 620, 430, 330, .40 + .12 * abs(A.w(t, 1.7))))
    s += SL(Z_SRED, dym(964, 300, t, 4, .3, 230, .3, "#d3dae2", .8))
    s += SL(Z_SRED, figura(330, 480, 330, t, "#2b2435", "#ffd98a", True, .1))
    vx, vy = 470, 352
    vr = 360 * t
    ver = (f'<g transform="rotate({vr:.1f} {vx:.0f} {vy:.0f})">'
           f'<path d="M{vx},{vy-96} l14,96 l-14,96 l-14,-96 Z" fill="url(#derev)" {o(4)}/>'
           f'<ellipse cx="{vx}" cy="{vy+28}" rx="40" ry="20" fill="url(#solom)" {o(4)}/></g>')
    ver += (f'<path d="M{vx},{vy-96} q-40,-90 -92,-150" fill="none" stroke="{KREM}"'
            f' stroke-width="6"/>')
    ver += (f'<ellipse cx="{vx-110:.0f}" cy="{vy-266:.0f}" rx="62" ry="78"'
            f' fill="url(#solom)" opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, ver)
    s += SL(Z_SRED, figura(1330, 492, 320, t, "#28222c", "#ffd98a", False, .4, True))
    val = (f'<path d="M1480,490 q16,-150 86,-154 q70,6 84,154 Z" fill="#8d8575" {o(6)}/>'
           f'<path d="M1480,490 q86,36 170,0 l10,40 q-90,30 -190,0 Z" fill="#6f6859" {o(5)}/>')
    sh_y = 24 * A.w(t, .7, .1)
    val += (f'<line x1="1528" y1="{372+sh_y:.0f}" x2="1596" y2="{300+sh_y:.0f}"'
            f' stroke="{ZHELEZ}" stroke-width="9"/>'
            f'<rect x="1590" y="{272+sh_y:.0f}" width="26" height="46" rx="8"'
            f' fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, val)
    s += SL(Z_SRED, lavka(1180, 496, 480))
    s += SL(Z_SRED, figura(380, 926, 330, t, "#272030", "#ffd98a", False, .7, True, 1.0, True))
    lx, ly = 560, 836
    s += SL(Z_SRED, f'<path d="M{lx-120},{ly} q120,-80 250,-16 l-12,46 q-120,-50 -238,10 Z"'
                    f' fill="url(#krem)" {o(5)}/>')
    nozh_a = -28 + 18 * A.w(t, .8, .2)
    s += SL(Z_SRED, f'<g transform="rotate({nozh_a:.1f} {lx+70:.0f} {ly-40:.0f})">'
                    f'<path d="M{lx+30},{ly-30} h150 l0,18 h-150 Z" fill="url(#zhel)" {o(4)}/>'
                    f'<rect x="{lx+170}" y="{ly-40}" width="60" height="38" rx="10"'
                    f' fill="url(#derev)" {o(4)}/></g>')
    struzh = ""
    for i in range(7):
        p = ((t * .62) + i / 7.0) % 1.0
        struzh += (f'<path d="M{lx+120+p*210:.0f},{ly-30+p*160:.0f} q22,-20 42,2 q-22,18 -42,-2 Z"'
                   f' fill="{KREM}" opacity="{(1-p)*.85:.2f}"/>')
    s += SL(Z_SRED, struzh)
    s += SL(Z_SRED, stol(1130, 820, 560, 28))
    for i in range(2):
        s += SL(Z_SRED, figura(1210 + i * 290, 960, 230, t, "#2a2432", "#ffd98a", i == 1, .3 * i))
    gor = ""
    for i in range(14):
        p = ((t * .74) + i / 14.0) % 1.0
        gor += (f'<circle cx="{1160+p*520:.0f}" cy="{808 - 10*abs(A.w(t,.6,i*.14)):.0f}"'
                f' r="{10+(i%3)*2}" fill="{["#7f9a4a","#93a85a","#6d8a40"][i%3]}" {o(2)}/>')
    s += SL(Z_SRED, gor)
    s += SL(Z_SRED, krynka(1700, 806, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0c0a09", .72))
    s += vinetka(.46)
    return s


def pleten_i_temnye_gosti(t):
    """Высокий плетень через весь кадр, на кольях горшки; из-за него по очереди
    высовываются лохматые любопытные тени с жёлтыми глазами."""
    rnd = random.Random(411)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 29)
    s += oblaka(t, 140, 3, 31, .24, "#b9c5d6", 9.0)
    s += SL(Z_DAL, izba_snaruzhi(80, 744, 400, t, True, True, 33))
    s += SL(Z_DAL, goloe_derevo(1740, 760, 440, t, 37, 6, "#2a2b33"))
    s += SL(Z_DAL, gryaz_polosa(790, 150, "#3d342c"))
    teni = ""
    for i in range(5):
        px = 230 + i * 350
        vyh = A.ease(A.seg(t, .2 + i * .42, .6)) - A.ease(A.seg(t, 4.6 + i * .5, .6))
        hh = 120 + 210 * vyh
        if vyh < .04:
            continue
        kol = ["#2b2736", "#332b3b", "#262232"][i % 3]
        teni += (f'<path d="M{px-96:.0f},{830} q0,{-hh:.0f} {96:.0f},{-hh:.0f}'
                 f' q{96:.0f},0 {96:.0f},{hh:.0f} Z" fill="{kol}" {o(6)}/>')
        for j in range(9):
            a = math.pi * (j / 8.0)
            teni += (f'<path d="M{px-92*math.cos(a):.0f},{830-hh*.96-6:.0f}'
                     f' l{(-10+j*2.4):.0f},{-34-14*abs(A.w(t,1.6,j*.1+i*.2)):.0f}"'
                     f' stroke="{kol}" stroke-width="13" stroke-linecap="round"/>')
        for sgn in (-1, 1):
            teni += (f'<path d="M{px+sgn*58:.0f},{830-hh*.86:.0f} l{sgn*30},-72 l{-sgn*44},16 Z"'
                     f' fill="{kol}" {o(4)}/>')
        gl = 16 if not A.blink(t, 2.2 + i * .4, i * .17) else 4
        for sgn in (-1, 1):
            teni += (f'<circle cx="{px+sgn*34:.0f}" cy="{830-hh*.66:.0f}" r="{gl}"'
                     f' fill="{SVET}"/>')
            teni += (f'<circle cx="{px+sgn*34:.0f}" cy="{830-hh*.66:.0f}" r="{gl*.4:.1f}"'
                     f' fill="{K}"/>')
        teni += teplo(px, 830 - hh * .66, 130, 100, .34)
        teni += (f'<path d="M{px:.0f},{830-hh*.60:.0f} q38,26 6,62 q-26,-18 -6,-62 Z"'
                 f' fill="{kol}" {o(4)}/>')
    s += SL(Z_DAL, teni)
    s += SL(Z_SRED, pleten(40, 886, 1840, 430, 13))
    gorshki = ""
    for i in range(6):
        gx = 120 + i * 300
        pad = A.out(A.seg(t, 3.2, .9)) if i == 2 else 0.0
        gy = 452 + pad * 320
        gorshki += krynka(gx, gy, 1.05 + (i % 3) * .12)
        gorshki += (f'<ellipse cx="{gx:.0f}" cy="{gy+12:.0f}" rx="30" ry="9"'
                    f' fill="#2a221c" opacity=".4"/>')
    s += SL(Z_SRED, gorshki)
    s += SL(Z_SRED, luchina(1560, 690, t, 1.0, .2))
    s += SL(Z_SRED, figura(1500, 892, 290, t, "#211d28", "#ffd98a", False, .2, True, 1.0, True))
    s += SL(Z_SRED, para_izo_rta(1534, 700, t, .3, .9, .5))
    s += tuman(t, 902, .46, "#d7e2ee")
    s += SL(Z_PERED, pleten(-40, 1060, 760, 230, 7))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 43, .5, .9))
    s += vinetka(.48)
    return s


def pech_s_zhivym_ognem(t):
    """Белёная печь во весь кадр, полукруглое устье на пол-экрана с живым
    огнём; из окна к огню тянутся длинные лапы теней."""
    rnd = random.Random(503)
    s = f'<rect width="{W}" height="{H}" fill="#241d18"/>'
    s += nebo("noch", t, True, 41)
    s += SL(Z_DAL, brevna(0, 0, W, 420, 98))
    s += SL(Z_DAL, okno_izby(60, 120, 250, 200, t, svet=False, moroz=.6))
    s += utvar_izby(1420, 180, 460, t, 11)
    s += SL(Z_SRED, polovicy(930))
    pechmass = (f'<rect x="200" y="210" width="1560" height="730" rx="26"'
                f' fill="url(#pech)" {o(10)}/>')
    pechmass += (f'<rect x="250" y="176" width="1460" height="46" rx="12"'
                 f' fill="{PECH2}" {o(7)}/>')
    for i in range(4):
        pechmass += (f'<line x1="216" y1="{280+i*170}" x2="1744" y2="{280+i*170}"'
                     f' stroke="{PECH2}" stroke-width="6" opacity=".55"/>')
    pechmass += (f'<rect x="1360" y="470" width="360" height="300" rx="16"'
                 f' fill="{PECH2}" {o(7)}/>')
    for i in range(3):
        pechmass += (f'<path d="M1390,{520+i*86} q170,30 300,0" fill="none"'
                     f' stroke="#c9bc9f" stroke-width="6"/>')
    s += SL(Z_SRED, pechmass)
    ux, uy, uw, uh = 430, 380, 1020, 560
    s += SL(Z_SRED, kirpich_ustya(ux, uy, uw, uh, t, False))
    put = kontur_proema(ux, uy, uw, uh, "ustie")
    vnutri = f'<path d="{put}" fill="#120c08"/>'
    vnutri += ugli(ux + 90, uy + uh - 70, uw - 180, t, 11, 53)
    for i in range(4):
        vnutri += (f'<rect x="{ux+170+i*190:.0f}" y="{uy+uh-150}" width="170" height="40"'
                   f' rx="14" fill="#5a3a22" {o(5)}/>')
    vnutri += ogon(ux + uw * .32, uy + uh - 80, t, 2.0, .0, 9)
    vnutri += ogon(ux + uw * .66, uy + uh - 70, t, 1.7, .4, 7)
    vnutri += mesto_stoka(ux, uy, uw, uh, "ustie")
    vnutri += (f'<path d="{kontur_proema(ux-18, uy-18, uw+36, uh+36, "ustie")}" fill="none"'
               f' stroke="{CHUGUN}" stroke-width="34"/>')
    vnutri += (f'<path d="{put}" fill="none" {o(10)}/>')
    for i in range(4):
        vnutri += (f'<rect x="{ux-60:.0f}" y="{uy+120+i*120:.0f}" width="54" height="96" rx="10"'
                   f' fill="url(#chug)" {o(5)}/>'
                   f'<rect x="{ux+uw+6:.0f}" y="{uy+120+i*120:.0f}" width="54" height="96" rx="10"'
                   f' fill="url(#chug)" {o(5)}/>')
    vnutri += (f'<ellipse cx="{ux+uw/2:.0f}" cy="{uy+uh:.0f}" rx="{uw*.56:.0f}"'
               f' ry="{30+10*A.w(t,1.7):.0f}" fill="{ORA}" opacity=".3"/>')
    vnutri += teplo(ux + uw / 2, uy + uh * .74, uw * .92, uh * .9, .5)
    s += SL(Z_SRED, vnutri)
    s += SL(Z_SRED, iskra_let(t, ux + uw * .5, uy + 120, 14, 59, 360, .5))
    # ЛАПЫ ТЕНЕЙ: тянутся от окна к устью. Должны читаться именно лапой —
    # толстая у окна, сужается к кисти, на конце ладонь с тремя когтями
    # (ровные палки с чёрточками читались как брак, поймано 14.11).
    lapy = ""
    for i in range(4):
        ly = 250 + i * 128
        rast = A.ease(A.seg(t, .25 + i * .22, 1.4))
        dl = 200 + rast * 520
        ky = ly + 40 + i * 16 + 10 * A.w(t, 2.1, i * .3)
        tol = 40 - i * 5
        lapy += (f'<path d="M-30,{ly-tol/2:.0f} Q{dl*.55:.0f},{ly-30+i*22:.0f}'
                 f' {dl:.0f},{ky-tol*.32:.0f} L{dl:.0f},{ky+tol*.32:.0f}'
                 f' Q{dl*.55:.0f},{ly+30+i*22:.0f} -30,{ly+tol/2:.0f} Z"'
                 f' fill="#1b1724" opacity=".88"/>')
        lapy += (f'<ellipse cx="{dl+10:.0f}" cy="{ky:.0f}" rx="{tol*.62:.0f}"'
                 f' ry="{tol*.50:.0f}" fill="#1b1724" opacity=".92"/>')
        for j in range(3):
            ug = -34 + j * 34 + 6 * A.w(t, 1.7, i * .2 + j * .3)
            dx_ = 62 * math.cos(math.radians(ug))
            dy_ = 62 * math.sin(math.radians(ug))
            lapy += (f'<path d="M{dl+10:.0f},{ky:.0f} q{dx_*.6:.0f},{dy_*.6:.0f}'
                     f' {dx_:.0f},{dy_:.0f}" fill="none" stroke="#1b1724"'
                     f' stroke-width="{13-j*2}" stroke-linecap="round" opacity=".92"/>')
            lapy += (f'<circle cx="{dl+10+dx_:.0f}" cy="{ky+dy_:.0f}" r="4.5"'
                     f' fill="#3a3348" opacity=".9"/>')
    s += SL(Z_SRED, lapy)
    s += SL(Z_SRED, lavka(120, 820, 420))
    s += SL(Z_SRED, figura(300, 820, 210, t, "#221c2a", "#ffd98a", False, .5, True, 1.0, True))
    hrap = ""
    for i in range(3):
        p = ((t * .42) + i / 3.0) % 1.0
        hrap += (f'<ellipse cx="{360+p*120:.0f}" cy="{690-p*90:.0f}" rx="{14+28*p:.0f}"'
                 f' ry="{10+20*p:.0f}" fill="#e6eef8" opacity="{(1-p)*.42:.2f}"/>')
    s += SL(Z_SRED, hrap)
    s += SL(Z_SRED, kura(1700, 924, t, .9, .3))
    s += SL(Z_PERED, ramka_pp("pravo", "#0a0807", .6))
    s += SL(Z_PERED, f'<path d="M-20,1080 q300,-90 620,-30 l0,130 h-640 Z"'
                     f' fill="#120d0a" opacity=".85"/>')
    s += vinetka(.5)
    return s


def izba_krepost(t):
    """Изба обрастает крепостными зубцами и башенками, ставни захлопываются,
    поперёк двери ложится дубовый брус, в горшке сияют угли."""
    rnd = random.Random(607)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 61)
    s += oblaka(t, 130, 3, 67, .22, "#aebbcd", 8.0)
    s += SL(Z_DAL, ulica_dal(1420, 800, 500, t, False, 71))
    s += SL(Z_DAL, gryaz_polosa(852, 140, "#3f362e"))
    bx, bw, base = 300, 1180, 900
    kor = brevna(bx, base - 440, bw, 440, 88)
    kor += (f'<path d="M{bx-80},{base-440} L{bx+bw/2:.0f},{base-690}'
            f' L{bx+bw+80},{base-440} Z" fill="{DOSKA2}" {o(9)}/>')
    s += SL(Z_DAL, kor)
    rost = A.out(A.seg(t, .4, 1.7))
    zub = ""
    for i in range(9):
        zx = bx + 30 + i * (bw - 60) / 8.0
        zh = 86 * rost * (.8 + .2 * math.sin(i))
        zub += (f'<rect x="{zx:.0f}" y="{base-446-zh:.0f}" width="86" height="{zh+16:.0f}"'
                f' rx="6" fill="url(#kamen)" {o(6)}/>')
        zub += (f'<rect x="{zx+20:.0f}" y="{base-440-zh*.6:.0f}" width="46" height="{zh*.4+6:.0f}"'
                f' rx="4" fill="{KAMEN2}" opacity=".7"/>')
    for sgn, tx in ((-1, bx - 30), (1, bx + bw - 130)):
        th = 300 * rost
        zub += (f'<rect x="{tx:.0f}" y="{base-440-th:.0f}" width="160" height="{th+40:.0f}"'
                f' rx="10" fill="url(#kamen)" {o(7)}/>')
        zub += (f'<path d="M{tx-20:.0f},{base-440-th:.0f} h200 l-100,{-90*rost:.0f} Z"'
                f' fill="{KAMEN2}" {o(6)}/>')
        zub += (f'<rect x="{tx+54:.0f}" y="{base-380-th*.5:.0f}" width="52" height="92"'
                f' rx="8" fill="#241c16" {o(5)}/>')
        zub += teplo(tx + 80, base - 334 - th * .5, 110, 90, .4)
    s += SL(Z_DAL, zub)
    s += SL(Z_DAL, dym(bx + bw * .5, base - 700, t, 5, .26, 380, .4, "#d1d8e0", 1.1))
    stav = A.ease(A.seg(t, 1.1, .9))
    okx, oky = bx + 150, base - 330
    okn = okno_izby(okx, oky, 250, 190, t, svet=True, moroz=.3)
    for sgn in (-1, 1):
        ww = 130 * stav
        okn += (f'<rect x="{okx+125+(sgn*125 - (sgn+1)/2*ww*1):.0f}" y="{oky-8}"'
                f' width="{ww:.0f}" height="206" rx="6" fill="url(#dosk)" {o(6)}/>')
        okn += (f'<path d="M{okx+125+sgn*62:.0f},{oky+40} l0,120" stroke="{DOSKA2}"'
                f' stroke-width="7" opacity="{stav:.2f}"/>')
    s += SL(Z_SRED, okn)
    dx_, dy_, dw, dh = bx + bw * .56, base - 440, 300, 440
    s += SL(Z_SRED, f'<path d="M{dx_:.0f},{dy_+dh:.0f} l0,{-dh*.72:.0f}'
                    f' q{dw*.5:.0f},{-dh*.34:.0f} {dw:.0f},0 l0,{dh*.72:.0f} Z"'
                    f' fill="#140f0c" {o(8)}/>')
    s += SL(Z_SRED, doski(dx_ + 14, dy_ + 90, dw - 28, dh - 100, 68, True, "derev"))
    s += SL(Z_SRED, podkova(dx_ + dw * .5, dy_ + 46, .9, t))
    lozh = A.out(A.seg(t, 1.4, 1.1))
    brx = dx_ - 190 + lozh * 190
    brus = (f'<rect x="{brx:.0f}" y="{dy_+dh*.46:.0f}" width="{dw+150:.0f}" height="74"'
            f' rx="16" fill="url(#derev)" {o(8)}/>')
    for i in range(5):
        brus += (f'<path d="M{brx+30+i*74:.0f},{dy_+dh*.46+16:.0f} q18,22 0,44"'
                 f' fill="none" stroke="#5a3a22" stroke-width="6"/>')
    for sx in (dx_ - 26, dx_ + dw - 12):
        brus += (f'<rect x="{sx:.0f}" y="{dy_+dh*.44:.0f}" width="44" height="96" rx="10"'
                 f' fill="url(#zhel)" {o(6)}/>')
    s += SL(Z_SRED, brus)
    ded_x = dx_ + dw * .5
    pl = A.ease(A.seg(t, 2.4, 1.0))
    s += SL(Z_SRED, figura(ded_x, dy_ + dh - 10, 300 + 26 * pl, t, "#241e2b", "#ffd98a", False, .3, True, 1.0, True))
    gx, gy = ded_x + 150, dy_ + dh - 40
    s += SL(Z_SRED, krynka(gx, gy, 1.2, "url(#chug)"))
    s += SL(Z_SRED, ugli(gx - 52, gy - 86, 104, t, 7, 73))
    s += SL(Z_SRED, teplo(gx, gy - 90, 250, 200, .52 + .14 * abs(A.w(t, 1.3))))
    s += SL(Z_SRED, iskra_let(t, gx, gy - 100, 8, 79, 220, .45))
    s += SL(Z_PERED, pleten(-60, 1020, 700, 200, 7))
    s += SL(Z_PERED, goloe_derevo(1800, 1010, 520, t, 83, 6, "#262730"))
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 89, .5, .9))
    s += vinetka(.46)
    return s


def krylco_i_skripuchaya_kalitka(t):
    """Крыльцо избы и двор до калитки: хозяин в тулупе пятится с крыльца,
    калитка качается на петле, куры жмутся под ступенями."""
    rnd = random.Random(709)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 97)
    s += oblaka(t, 160, 4, 101, .26, "#bcc8d8", 10.0)
    s += SL(Z_DAL, ulica_dal(1180, 760, 740, t, False, 103))
    s += SL(Z_DAL, gryaz_polosa(820, 170, "#423830"))
    s += SL(Z_DAL, brevna(0, 60, 900, 760, 92))
    okn = okno_izby(120, 250, 290, 210, t, svet=True, moroz=.3)
    okn += (f'<path d="M96,216 h340 l-28,-42 h-284 Z" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_DAL, okn)
    s += SL(Z_DAL, teplo(266, 356, 350, 290, .42 + .12 * abs(A.w(t, 2.1))))
    s += SL(Z_DAL, dym(690, 140, t, 5, .24, 300, .4, "#d1d8e0", 1.0))
    kr = (f'<path d="M420,1010 h700 l-70,-230 h-560 Z" fill="url(#dosk)" {o(8)}/>')
    for i in range(4):
        kr += (f'<rect x="{440+i*22:.0f}" y="{790+i*58:.0f}" width="{640-i*44:.0f}"'
               f' height="44" rx="6" fill="url(#dosk)" {o(5)}/>')
    kr += (f'<rect x="430" y="470" width="34" height="330" fill="url(#derev)" {o(6)}/>'
           f'<rect x="1060" y="470" width="34" height="330" fill="url(#derev)" {o(6)}/>')
    kr += (f'<path d="M380,470 h760 l-60,-96 h-640 Z" fill="{DOSKA2}" {o(7)}/>')
    kr += (f'<path d="M398,462 h724 l-50,-80 h-624 Z" fill="url(#sneg)" opacity=".8" {o(4)}/>')
    for i in range(6):
        kr += (f'<path d="M{470+i*118:.0f},470 q16,34 0,68" fill="none" stroke="{MED}"'
               f' stroke-width="8"/>')
    s += SL(Z_SRED, kr)
    s += SL(Z_SRED, dver(640, 500, 260, 310, .12, kruchok=True))
    s += SL(Z_SRED, podkova(770, 480, .7, t))
    nazad = A.out(A.seg(t, .4, 1.6))
    hx = 820 - nazad * 180
    s += SL(Z_SRED, figura(hx, 800 + nazad * 70, 330, t, "#221d28", "#ffd98a", False, .2, True, 1.0, True, 1.4))
    s += SL(Z_SRED, para_izo_rta(hx + 34, 800 + nazad * 70 - 268, t, .2, 1.0, .52))
    kur = ""
    for i in range(3):
        kur += kura(520 + i * 150, 1000, t, .62, i * .3, ["#e2d6c2", "#cdbba0", "#e8dcc8"][i])
    s += SL(Z_SRED, kur)
    kal_a = 15 * A.w(t, 1.9, .1)
    kal = (f'<rect x="1430" y="560" width="30" height="400" fill="url(#derev)" {o(6)}/>'
           f'<rect x="1880" y="560" width="30" height="400" fill="url(#derev)" {o(6)}/>')
    kal += (f'<g transform="rotate({kal_a:.2f} 1446 600)">')
    for i in range(5):
        kal += (f'<rect x="{1452+i*84:.0f}" y="600" width="66" height="350" rx="8"'
                f' fill="url(#dosk)" {o(5)}/>')
    kal += (f'<path d="M1452,700 l420,120" stroke="{DOSKA2}" stroke-width="22"/>'
            f'<path d="M1452,620 h420" stroke="{DOSKA2}" stroke-width="18"/></g>')
    s += SL(Z_SRED, kal)
    s += SL(Z_SRED, pleten(1140, 960, 300, 180, 5))
    s += tuman(t, 940, .44, "#d8e3ef")
    s += SL(Z_PERED, goloe_derevo(1700, 1070, 560, t, 107, 7, "#282932"))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 109, .48, .9))
    s += vinetka(.46)
    return s


def vedma_i_koldun_na_perekrestke_doro(t):
    """Развилка дорог у кривой берёзы: колдун и носатая ведьма варят зелье в
    котле на огне, за путником семенят костыль и градусник."""
    rnd = random.Random(811)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 113)
    s += oblaka(t, 150, 3, 127, .24, "#b4c0d2", 9.0)
    s += SL(Z_DAL, ulica_dal(60, 700, 620, t, False, 131))
    s += SL(Z_DAL, gryaz_polosa(760, 200, "#3b332b"))
    road = (f'<path d="M900,780 L420,1080 h620 Z" fill="#5a4e42" opacity=".9"/>'
            f'<path d="M940,780 L1560,1080 h-520 Z" fill="#544840" opacity=".9"/>')
    for i in range(6):
        road += (f'<ellipse cx="{700+i*90:.0f}" cy="{900+i*26:.0f}" rx="{70-i*6}" ry="12"'
                 f' fill="#76848c" opacity=".3"/>')
    s += SL(Z_DAL, road)
    s += SL(Z_DAL, goloe_derevo(1520, 800, 620, t, 137, 8, "#e6edf4"))
    s += SL(Z_DAL, f'<path d="M1500,800 q-70,-220 40,-420 q60,-150 -10,-200"'
                   f' fill="none" stroke="#e8eff6" stroke-width="40" opacity=".55"/>')
    s += SL(Z_DAL, ptica(1420, 330, t, 1.1, "#2b2b33", .2, "#1f2029"))
    kx, ky = 900, 830
    kot_ = (f'<path d="M{kx-190},{ky-220} q0,230 190,236 q190,-6 190,-236 Z"'
            f' fill="url(#chug)" {o(9)}/>')
    kot_ += (f'<ellipse cx="{kx}" cy="{ky-222}" rx="196" ry="52" fill="#1f2a22" {o(7)}/>')
    bul = ""
    for i in range(8):
        p = ((t * .72) + i / 8.0) % 1.0
        bul += (f'<circle cx="{kx-130+i*38:.0f}" cy="{ky-240-p*80:.0f}"'
                f' r="{(10+16*(1-p)):.1f}" fill="#8fc14f" opacity="{(1-p)*.8:.2f}"/>')
    kot_ += (f'<ellipse cx="{kx}" cy="{ky-226}" rx="178" ry="42" fill="#5f8c35"'
             f' opacity="{.8+.15*abs(A.w(t,1.1)):.2f}"/>') + bul
    for sgn in (-1, 1):
        kot_ += (f'<path d="M{kx+sgn*196:.0f},{ky-250} q{sgn*60},40 {sgn*10},96"'
                 f' fill="none" stroke="{ZHELEZ}" stroke-width="16"/>')
    s += SL(Z_SRED, kot_)
    s += SL(Z_SRED, ugli(kx - 160, ky + 24, 320, t, 9, 139))
    s += SL(Z_SRED, ogon(kx - 70, ky + 18, t, 1.25, .1, 7))
    s += SL(Z_SRED, ogon(kx + 90, ky + 20, t, 1.0, .5, 6))
    s += SL(Z_SRED, teplo(kx, ky - 60, 440, 340, .46 + .12 * abs(A.w(t, 1.5))))
    kold_x = 470
    s += SL(Z_SRED, figura(kold_x, 900, 400, t, "#2a2338", "#cfe4f5", False, .1, True, 1.0, False, .8))
    bor = (f'<path d="M{kold_x-54},{900-330} q54,320 108,0 q-18,330 -54,336 q-36,-6 -54,-336 Z"'
           f' fill="#d9e2ea" opacity=".93" {o(5)}/>')
    for i in range(4):
        bor += (f'<path d="M{kold_x-36+i*24:.0f},{900-300} q{6-i*3},160 {-4+i*2},300"'
                f' fill="none" stroke="#aebbc6" stroke-width="5"/>')
    bor += (f'<path d="M{kold_x-74},{900-368} q74,-70 148,0 q-20,-74 -74,-76 q-54,2 -74,76 Z"'
            f' fill="#3d3b4a" {o(5)}/>')
    s += SL(Z_SRED, bor)
    ved_x = 1250
    s += SL(Z_SRED, figura(ved_x, 906, 380, t, "#2d2238", "#cfe4f5", True, .5, True, 1.0))
    nos = (f'<path d="M{ved_x-28},{906-316} q-96,24 -8,54 q22,-12 10,-54 Z"'
           f' fill="#c79a84" {o(5)}/>')
    nos += (f'<circle cx="{ved_x-96}" cy="{906-268}" r="9" fill="#8d5f4a"/>')
    s += SL(Z_SRED, nos)
    duet = ""
    for i in range(4):
        p = ((t * .66) + i / 4.0) % 1.0
        duet += (f'<ellipse cx="{ved_x-120-p*220:.0f}" cy="{906-280+p*40:.0f}"'
                 f' rx="{16+40*p:.0f}" ry="{12+26*p:.0f}" fill="#cfe4f5"'
                 f' opacity="{(1-p)*.42:.2f}"/>')
    s += SL(Z_SRED, duet)
    pom = (f'<line x1="{ved_x+120}" y1="930" x2="{ved_x+176}" y2="560"'
           f' stroke="url(#derev)" stroke-width="18"/>')
    for i in range(11):
        pom += (f'<path d="M{ved_x+120:.0f},930 l{-50+i*10},{76+8*abs(A.w(t,2.2,i*.09)):.0f}"'
                f' stroke="#a07c2e" stroke-width="7" stroke-linecap="round"/>')
    s += SL(Z_SRED, pom)
    hod = A.seg(t, .5, 6.0)
    px = 1700 - hod * 560
    for i, (dx, col) in enumerate(((0, "#cfd6de"), (70, "#d7b4a4"))):
        st = 22 * abs(A.w(t, .5, i * .5))
        s += SL(Z_PERED, f'<g transform="translate({px+dx:.0f},{1010-st:.0f})">'
                         f'<rect x="-12" y="-170" width="24" height="170" rx="10" fill="{col}" {o(5)}/>'
                         f'<path d="M-34,-170 q34,-34 68,0 q-34,22 -68,0 Z" fill="{col}" {o(4)}/>'
                         f'<line x1="-10" y1="4" x2="-30" y2="44" stroke="{K}" stroke-width="8"/>'
                         f'<line x1="10" y1="4" x2="32" y2="44" stroke="{K}" stroke-width="8"/></g>')
    s += tuman(t, 960, .4, "#d6e1ed")
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 149, .5, .9))
    s += vinetka(.48)
    return s


def sosed_s_pustym_gorshkom(t):
    """Порог избы: сосед протягивает глиняный горшок для углей, а хозяйка по
    очереди прячет за спину уголёк, щепку и свечку. Горшок НЕ во весь кадр и
    не обрезан краем: пузатое тулово, узкая шейка, развал венчика и две ушки —
    прежний «гигантский обрезанный горшок» не опознавался (осмотр 14.11)."""
    rnd = random.Random(907)
    s = f'<rect width="{W}" height="{H}" fill="#241c16"/>'
    s += nebo("noch", t, True, 151)
    s += SL(Z_DAL, brevna(0, 0, W, 500, 96))
    s += utvar_izby(90, 300, 520, t, 13)
    s += SL(Z_SRED, polovicy(900))
    pr = (f'<path d="M980,0 l0,900 h820 l0,-900 Z" fill="#12100e" opacity=".95"/>')
    pr += (f'<rect x="950" y="0" width="60" height="912" fill="url(#derev)" {o(7)}/>'
           f'<rect x="1790" y="0" width="60" height="912" fill="url(#derev)" {o(7)}/>')
    pr += (f'<rect x="950" y="880" width="900" height="80" rx="10" fill="url(#dosk)" {o(8)}/>')
    s += SL(Z_SRED, pr)
    s += SL(Z_SRED, pech(30, 330, 400, 560, t, True, True, False))
    s += SL(Z_SRED, teplo(230, 660, 430, 350, .44 + .12 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, figura(1270, 890, 520, t, "#231c2b", "#ffd98a", True, .1))
    s += SL(Z_SRED, figura(1660, 886, 440, t, "#1a1824", "#cfe4f5", False, .4, True, 1.0, True))
    s += SL(Z_SRED, para_izo_rta(1700, 886 - 374, t, .3, 1.1, .5))
    # ГОРШОК ДЛЯ УГЛЕЙ: ростом в треть кадра, целиком в кадре, на уровне груди
    put = A.out(A.seg(t, .4, 1.2))
    gx, gy = 1580 - put * 110, 788          # gy — донце
    gw, gh = 150, 300                       # полуширина тулова и высота
    gor = ten(gx, gy + 12, gw * .9, 22, .45)
    gor += (f'<path d="M{gx-gw*.52:.0f},{gy:.0f}'
            f' q{-gw*.62:.0f},{-gh*.30:.0f} {-gw*.40:.0f},{-gh*.60:.0f}'
            f' q{gw*.16:.0f},{-gh*.22:.0f} {gw*.48:.0f},{-gh*.26:.0f}'
            f' l{gw*.88:.0f},0'
            f' q{gw*.34:.0f},{gh*.04:.0f} {gw*.46:.0f},{gh*.26:.0f}'
            f' q{gw*.22:.0f},{gh*.30:.0f} {-gw*.38:.0f},{gh*.60:.0f} Z"'
            f' fill="url(#glina)" {o(9)}/>')
    for sgn in (-1, 1):                     # ушки по бокам шейки
        gor += (f'<path d="M{gx+sgn*gw*.84:.0f},{gy-gh*.78:.0f}'
                f' q{sgn*gw*.44:.0f},{gh*.06:.0f} {sgn*gw*.30:.0f},{gh*.26:.0f}'
                f' q{-sgn*gw*.10:.0f},{gh*.06:.0f} {-sgn*gw*.22:.0f},{-gh*.04:.0f}'
                f' q{sgn*gw*.14:.0f},{-gh*.12:.0f} {-sgn*gw*.08:.0f},{-gh*.18:.0f} Z"'
                f' fill="#b07a46" {o(5)}/>')
    gor += (f'<path d="M{gx-gw*.92:.0f},{gy-gh*.90:.0f} h{gw*1.84:.0f}'
            f' l{-gw*.14:.0f},{gh*.10:.0f} h{-gw*1.56:.0f} Z" fill="#b07a46" {o(6)}/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-gh*.90:.0f}" rx="{gw*.92:.0f}"'
            f' ry="{gh*.095:.0f}" fill="#a06c3c" {o(6)}/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-gh*.88:.0f}" rx="{gw*.72:.0f}"'
            f' ry="{gh*.070:.0f}" fill="#1d1510"/>')
    for i in range(3):                      # поясок по тулову
        gor += (f'<path d="M{gx-gw*.78+i*6:.0f},{gy-gh*.22-i*gh*.18:.0f}'
                f' q{gw*.78-i*6:.0f},{gh*.08:.0f} {gw*1.56-i*12:.0f},0"'
                f' fill="none" stroke="#9c6a3c" stroke-width="8" opacity=".75"/>')
    gor += (f'<path d="M{gx-gw*.52:.0f},{gy-gh*.52:.0f}'
            f' q{-gw*.14:.0f},{-gh*.18:.0f} {gw*.04:.0f},{-gh*.30:.0f}"'
            f' fill="none" stroke="#f0cfa0"'
            f' stroke-width="{12+3*abs(A.w(t,2.2)):.0f}" opacity=".35"/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-6:.0f}" rx="{gw*.62:.0f}" ry="20"'
            f' fill="#201a14" opacity=".4"/>')
    s += SL(Z_SRED, gor)
    ruk1, (r1x, r1y) = rukav(1690, 600, 190, 176, t, "#232028", "#cfe4f5", .2, 6.0)
    s += SL(Z_SRED, ruk1)
    faza = int((t * .9) % 3)
    pryach = abs(A.w(t, 1.5, .25))
    hx, hy = 1130 - pryach * 90, 640 + pryach * 30
    pred = ""
    if faza == 0:
        pred += (f'<path d="M{hx-130},{hy} h170 l0,-22 h-170 Z" fill="url(#zhel)" {o(5)}/>'
                 f'<path d="M{hx+40},{hy-26} q70,-10 130,6 l0,24 q-66,-14 -130,-4 Z"'
                 f' fill="{ZHELEZ}" {o(5)}/>')
        pred += ugli(hx - 120, hy - 14, 130, t, 5, 157)
        pred += teplo(hx - 60, hy - 24, 220, 180, .56)
    elif faza == 1:
        pred += (f'<path d="M{hx-60},{hy+40} l30,-200 l24,6 l-26,200 Z" fill="url(#derev)" {o(4)}/>')
        pred += ogon(hx - 36, hy - 170, t, .5, .1, 5)
        pred += teplo(hx - 36, hy - 180, 200, 170, .52)
    else:
        pred += (f'<path d="M{hx-110},{hy+30} q110,70 220,0 q-110,26 -220,0 Z"'
                 f' fill="url(#glina)" {o(6)}/>')
        pred += svecha(hx, hy - 60, t, .2, 1.1, 90)
    s += SL(Z_SRED, pred)
    ruk2, (r2x, r2y) = rukav(1230, 560, 160, 178 + 14 * pryach, t, "#5b2b32", "#ffd98a", .4, 7.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="26" ry="19" fill="#5b2b32" {o(4)}/>')
    s += SL(Z_SRED, kot(760, 952, t, .7, "#332c28"))
    s += SL(Z_SRED, luchina(640, 560, t, 1.1, .3))
    s += SL(Z_PERED, ramka_pp("levo", "#0c0a08", .52))
    s += SL(Z_PERED, krynka(240, 1010, 1.4))
    s += vinetka(.48)
    return s


def schaste_uhodit_za_ugolkom(t):
    """Сосед уносит по тёмной улице светящийся горшок с углём, а следом из
    двери топает круглая фигурка Счастья с котомкой на палке.

    Счастье — МАЛЕНЬКИЙ ЧЕЛОВЕК, а не голова с ногами: рубаха с пояском вдвое
    выше головы, короткая шея, лапти, рукава. Прежняя версия читалась уродцем
    (голова в две трети туловища) — поправлено по осмотру 14.11."""
    rnd = random.Random(1009)
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 163)
    s += SL(Z_DAL, ulica_dal(40, 720, 1840, t, False, 167))
    s += SL(Z_DAL, gryaz_polosa(790, 300, "#261f1a"))
    s += SL(Z_DAL, goloe_derevo(300, 820, 480, t, 173, 6, "#1f2029"))
    s += SL(Z_DAL, goloe_derevo(1760, 840, 540, t, 179, 7, "#1f2029"))
    ib = brevna(1180, 560, 700, 320, 78)
    ib += (f'<path d="M1120,560 L1530,330 L1940,560 Z" fill="{DOSKA2}" {o(8)}/>')
    ib += (f'<path d="M1120,556 L1530,326 L1940,556 l-50,-30 L1530,296 L1170,526 Z"'
           f' fill="url(#sneg)" {o(5)}/>')
    ib += (f'<rect x="1700" y="300" width="74" height="130" fill="url(#kamen)" {o(6)}/>')
    ib += (f'<rect x="1160" y="870" width="740" height="40" rx="10" fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_SRED, ib)
    s += SL(Z_SRED, dym(1737, 288, t, 5, .24, 340, .4, "#cdd4dc", 1.0))
    s += SL(Z_SRED, okno_izby(1390, 620, 190, 156, t, svet=False, moroz=.3))
    tusk = .62 - .30 * A.ease(A.seg(t, .6, 1.8))
    s += SL(Z_SRED, f'<rect x="1390" y="620" width="190" height="156" fill="{SVET}"'
                    f' opacity="{tusk:.2f}"/>')
    s += SL(Z_SRED, teplo(1484, 700, 300, 240, tusk * .7))
    s += SL(Z_SRED, dver(1230, 600, 210, 270, .5, kruchok=True))
    hod = A.ease(A.seg(t, .3, 2.4))
    sx = 1180 - hod * 820
    s += SL(Z_SRED, figura(sx, 962, 420, t, "#2b2738", "#cfe4f5", False, .1, True, 1.0, True))
    gx, gy = sx - 150, 820
    gor = krynka(gx, gy, 1.9, "url(#glina)")
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-92}" rx="40" ry="14" fill="{ORA}"'
            f' opacity="{.72+.22*abs(A.w(t,1.2)):.2f}"/>')
    gor += ugli(gx - 34, gy - 92, 68, t, 5, 191)
    gor += teplo(gx, gy - 70, 320, 260, .62)
    gor += iskra_let(t, gx, gy - 100, 7, 193, 230, .46)
    s += SL(Z_SRED, gor)
    s += SL(Z_SRED, para_izo_rta(sx + 30, 962 - 300, t, .2, 1.0, .46))
    # СЧАСТЬЕ: рост 330, голова 1/4 роста, тело с поясом, лапти, котомка
    hx = 1240 - hod * 700
    stup = 14 * abs(A.w(t, .46, .2))
    pod = 1010                               # уровень земли под лаптями
    sch = f'<g transform="translate({hx:.0f},{-stup:.0f})">'
    sch += ten(0, pod + 6, 112, 18, .45)
    for sgn in (-1, 1):                      # лапти, по очереди отрываются
        sh = 16 * A.w(t, .46, .2 + (0 if sgn < 0 else .5))
        sch += (f'<path d="M{sgn*48-44:.0f},{pod-26+min(0,sh):.0f} h88'
                f' q18,0 14,20 q-4,16 -26,16 h-66 q-20,0 -22,-18 Z"'
                f' fill="url(#solom)" {o(5)}/>')
        for j in range(3):
            sch += (f'<path d="M{sgn*48-32+j*22:.0f},{pod-24+min(0,sh):.0f} l0,32"'
                    f' stroke="#a07c2e" stroke-width="5" opacity=".8"/>')
    sch += (f'<path d="M-92,{pod-30:.0f} q-16,-150 20,-212 q72,-26 144,0'
            f' q36,62 20,212 Z" fill="#8f2f33" {o(8)}/>')
    sch += (f'<path d="M-86,{pod-150:.0f} q86,22 172,0" fill="none" stroke="{MED}"'
            f' stroke-width="16" opacity=".9"/>')
    sch += (f'<path d="M-90,{pod-48:.0f} q90,24 180,0" fill="none" stroke="#e8c9a0"'
            f' stroke-width="7" opacity=".5"/>')
    for sgn in (-1, 1):                      # рукава вдоль тела
        a = sgn * (14 + 6 * A.w(t, 1.6, .3 if sgn > 0 else 0))
        sch += (f'<g transform="rotate({a:.1f} {sgn*62:.0f} {pod-220:.0f})">'
                f'<rect x="{sgn*62-22:.0f}" y="{pod-226:.0f}" width="44" height="130"'
                f' rx="22" fill="#8f2f33" {o(5)}/></g>')
    sch += (f'<rect x="-26" y="{pod-258:.0f}" width="52" height="40" fill="#e6b188" {o(4)}/>')
    sch += (f'<ellipse cx="0" cy="{pod-300:.0f}" rx="76" ry="78" fill="#e6b188" {o(7)}/>')
    sch += (f'<path d="M-78,{pod-318:.0f} q78,-72 156,0 q-20,-84 -78,-84'
            f' q-58,0 -78,84 Z" fill="#6b4a30" {o(5)}/>')
    sch += (f'<ellipse cx="-36" cy="{pod-282:.0f}" rx="22" ry="15" fill="#d9705f" opacity=".7"/>'
            f'<ellipse cx="38" cy="{pod-282:.0f}" rx="22" ry="15" fill="#d9705f" opacity=".7"/>')
    bl = 4 if A.blink(t, 3.2, .1) else 9
    sch += (f'<circle cx="-26" cy="{pod-308:.0f}" r="{bl}" fill="{K}"/>'
            f'<circle cx="28" cy="{pod-308:.0f}" r="{bl}" fill="{K}"/>')
    sch += (f'<path d="M-30,{pod-262:.0f} q30,28 60,0" fill="none" stroke="{K}"'
            f' stroke-width="6"/>')
    sch += (f'<line x1="70" y1="{pod-176:.0f}" x2="152" y2="{pod-420:.0f}"'
            f' stroke="url(#derev)" stroke-width="14"/>')
    sch += (f'<path d="M136,{pod-420:.0f} q78,-26 112,52 q-70,40 -122,-18 Z"'
            f' fill="url(#rush)" {o(6)}/>'
            f'<path d="M146,{pod-398:.0f} q60,-12 90,34" fill="none" stroke="{TKAN}"'
            f' stroke-width="7"/>')
    sch += '</g>'
    s += SL(Z_SRED, sch)
    s += SL(Z_SRED, teplo(hx, 760, 260, 220, .22))
    pes = (f'<g transform="translate(560,{980-10*abs(A.w(t,.8,.3)):.0f})">'
           f'<ellipse cx="0" cy="0" rx="78" ry="46" fill="#4a4038" {o(5)}/>'
           f'<circle cx="62" cy="-42" r="34" fill="#4a4038" {o(5)}/>'
           f'<path d="M86,-60 l24,-34 l-40,8 Z" fill="#4a4038" {o(4)}/>'
           f'<path d="M-70,-10 q-54,-56 -24,-96" fill="none" stroke="#4a4038" stroke-width="16"/>'
           f'<circle cx="76" cy="-46" r="5" fill="{SVET}"/></g>')
    s += SL(Z_SRED, pes)
    s += SL(Z_PERED, pleten(-80, 1070, 760, 190, 7))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 197, .46, .9))
    s += vinetka(.52)
    return s


def ovechi_nozhnicy_na_gvozde(t):
    """Кованые овечьи ножницы на гвозде в бревенчатой стене на пол-кадра:
    паук деловито тянет от них паутину, ниже жуёт овца."""
    rnd = random.Random(1103)
    s = f'<rect width="{W}" height="{H}" fill="{BREVNO2}"/>'
    s += nebo("sumer", t, False, 199)
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 104))
    s += SL(Z_DAL, okno_izby(60, 120, 260, 200, t, svet=False, moroz=.55))
    s += utvar_izby(1420, 260, 440, t, 17)
    s += SL(Z_SRED, polovicy(930))
    nx, ny = 830, 220
    s += SL(Z_SRED, f'<rect x="{nx-18}" y="{ny-26}" width="40" height="40" rx="8"'
                    f' fill="url(#zhel)" {o(5)}/>')
    kach = 3.2 * A.w(t, 2.8, .1)
    nozh = f'<g transform="rotate({kach:.2f} {nx:.0f} {ny:.0f})">'
    nozh += (f'<path d="M{nx-10},{ny} q-60,210 -24,330 q34,96 20,170" fill="none"'
             f' stroke="{ZHELEZ}" stroke-width="28" stroke-linecap="round"/>')
    nozh += (f'<path d="M{nx+10},{ny} q60,210 24,330 q-34,96 -20,170" fill="none"'
             f' stroke="{ZHELEZ}" stroke-width="28" stroke-linecap="round"/>')
    for sgn in (-1, 1):
        nozh += (f'<path d="M{nx+sgn*4:.0f},{ny+500} l{sgn*96},186 l{sgn*34},-10'
                 f' l{-sgn*96},-196 Z" fill="url(#zhel)" {o(6)}/>')
        nozh += (f'<path d="M{nx+sgn*20:.0f},{ny+520} l{sgn*80},160" stroke="#dfe8f2"'
                 f' stroke-width="7" opacity=".6"/>')
    nozh += (f'<circle cx="{nx}" cy="{ny+486}" r="26" fill="{CHUGUN}" {o(5)}/>')
    nozh += (f'<ellipse cx="{nx-10}" cy="{ny+170}" rx="54" ry="22" fill="none"'
             f' stroke="{ZHELEZ}" stroke-width="20"/>')
    nozh += '</g>'
    s += SL(Z_SRED, nozh)
    s += SL(Z_SRED, blik(nx + 60, ny + 540, t, .5, "#bcd8ff", SVET, .5))
    pau = A.ease(A.seg(t, .4, 2.6))
    pax, pay = nx + 180 + pau * 300, ny + 300 + pau * 120
    pat = ""
    for i in range(7):
        pat += (f'<path d="M{nx+30},{ny+240+i*44} Q{(nx+pax)/2+30:.0f},'
                f'{ny+230+i*60+18*A.w(t,3.0,i*.12):.0f} {pax:.0f},{pay:.0f}"'
                f' fill="none" stroke="#e4eef6" stroke-width="3" opacity="{.3+.07*i:.2f}"/>')
    for i in range(4):
        pat += (f'<path d="M{nx+70+i*70:.0f},{ny+250} q{40:.0f},{120+i*40} -10,{280}"'
                f' fill="none" stroke="#e4eef6" stroke-width="2.4" opacity=".32"/>')
    s += SL(Z_SRED, pat)
    pk = (f'<g transform="translate({pax:.0f},{pay:.0f})">'
          f'<ellipse cx="0" cy="0" rx="26" ry="22" fill="#2a2420" {o(4)}/>'
          f'<circle cx="18" cy="-10" r="12" fill="#2a2420" {o(3)}/>')
    for j in range(8):
        a = -2.4 + j * .62
        pk += (f'<path d="M0,0 q{34*math.cos(a):.0f},{26*math.sin(a):.0f}'
               f' {56*math.cos(a):.0f},{20*math.sin(a)+16*A.w(t,1.2,j*.12):.0f}"'
               f' fill="none" stroke="#2a2420" stroke-width="5"/>')
    pk += '</g>'
    s += SL(Z_SRED, pk)
    ov = (f'<g transform="translate(390,{900+6*A.w(t,1.9,.2):.0f})">')
    ov += (f'<ellipse cx="0" cy="-130" rx="230" ry="150" fill="#ece4d4" {o(8)}/>')
    for i in range(16):
        a = rnd.uniform(0, 6.28); rr = rnd.uniform(.3, 1.0)
        ov += (f'<circle cx="{math.cos(a)*220*rr:.0f}" cy="{-130+math.sin(a)*140*rr:.0f}"'
               f' r="{30+rnd.random()*16:.0f}" fill="#f7f1e4" opacity=".7"/>')
    zhuy = 8 * A.w(t, .7, .1)
    ov += (f'<g transform="rotate({zhuy:.1f} 200 -180)">'
           f'<ellipse cx="238" cy="-200" rx="92" ry="74" fill="#d8cdb8" {o(6)}/>'
           f'<path d="M300,-176 q46,14 10,46 q-34,6 -46,-30 Z" fill="#c3b49b" {o(5)}/>'
           f'<circle cx="286" cy="-216" r="8" fill="{K}"/>'
           f'<path d="M190,-258 q-54,-54 -74,-14 q24,34 74,14 Z" fill="#d8cdb8" {o(5)}/></g>')
    for i, dx in enumerate((-150, -40, 70, 180)):
        ov += (f'<rect x="{dx}" y="-20" width="38" height="{110+8*abs(A.w(t,1.4,i*.2)):.0f}"'
               f' rx="12" fill="#cfc4ad" {o(5)}/>')
    ov += '</g>'
    s += SL(Z_SRED, ov)
    s += SL(Z_SRED, figura(1300, 930, 420, t, "#241f2a", "#ffd98a", False, .3, True, 1.0, True))
    cheh = 10 * A.w(t, 1.1, .3)
    s += SL(Z_SRED, f'<g transform="rotate({cheh:.1f} 1300 700)">'
                    f'<path d="M1252,690 q48,190 96,0 q-16,196 -48,200 q-32,-4 -48,-200 Z"'
                    f' fill="#b2a894" {o(5)}/></g>')
    s += SL(Z_SRED, luchina(1660, 760, t, 1.2, .1))
    s += SL(Z_PERED, ramka_pp("levo", "#0b0908", .5))
    s += vinetka(.44)
    return s


def silach_posle_strizhki(t):
    """Деревенский силач играючи держит бревно над головой; ножницы щёлкают,
    кудри падают, он сдувается и бревно опускается ему на плечи.

    Человек — `figura()` в сжимающемся слое, а не самодельное тело: руки
    поднимаются рукавами к бревну, кудри идут сплошной шапкой с фестонами,
    срезанные пряди падают запятыми. Прежние цепочки кружков читались не
    руками и не кудрями (осмотр 14.11)."""
    rnd = random.Random(1201)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 211)
    s += SL(Z_DAL, brevna(0, 0, W, 980, 100))
    s += SL(Z_DAL, okno_izby(1540, 180, 300, 220, t, svet=True, moroz=.3))
    s += SL(Z_DAL, teplo(1690, 290, 330, 270, .36))
    s += utvar_izby(80, 220, 420, t, 19)
    s += SL(Z_SRED, polovicy(900))
    sdul = A.ease(A.seg(t, 1.6, 1.8))
    cx, cy, rost = 900, 940, 620
    kx_, ky_ = 1.0 - .30 * sdul, 1.0 - .14 * sdul
    plech = cy - rost * .66 * ky_
    bry = 146 + sdul * 330                   # бревно опускается на плечи
    # ТЕЛО: обычная фигура ролика, сжатая группой
    tel = (f'<g transform="translate({cx:.0f},{cy:.0f}) scale({kx_:.3f},{ky_:.3f})'
           f' translate({-cx:.0f},{-cy:.0f})">')
    tel += figura(cx, cy, rost, t, "#6d7f99", "#ffd98a", False, .1, False, 1.0,
                  False, .8, True)
    tel += '</g>'
    s += SL(Z_SRED, tel)
    # КУДРИ: сплошная шапка с фестонами, тает вместе с силой
    kud = 1.0 - sdul
    gy_ = cy - rost * .845 * ky_
    hh_ = rost * .145 * ky_
    if kud > .02:
        d = f'M{cx-hh_*1.26:.0f},{gy_+hh_*.10:.0f}'
        for i in range(7):
            a = -3.14 + i * .524
            rr = hh_ * (1.30 + .16 * kud)
            d += (f' Q{cx+math.cos(a-.26)*rr*1.12:.0f},'
                  f'{gy_+math.sin(a-.26)*rr*1.06:.0f}'
                  f' {cx+math.cos(a)*rr:.0f},{gy_+math.sin(a)*rr*.96:.0f}')
        d += ' Z'
        s += SL(Z_SRED, f'<path d="{d}" fill="#7a5436" opacity="{.45+.55*kud:.2f}" {o(6)}/>')
        for i in range(6):                   # завитки по кромке
            a = -2.75 + i * .42
            s += SL(Z_SRED, f'<path d="M{cx+math.cos(a)*hh_*1.20:.0f},'
                            f'{gy_+math.sin(a)*hh_*1.16:.0f}'
                            f' q{math.cos(a)*hh_*.42:.0f},{-hh_*.30*kud:.0f}'
                            f' {math.cos(a)*hh_*.30:.0f},{hh_*(.30+.22*kud):.0f}"'
                            f' fill="none" stroke="#5e4028"'
                            f' stroke-width="{10+8*kud:.0f}" stroke-linecap="round"'
                            f' opacity="{.5+.4*kud:.2f}"/>')
    # РУКИ: два рукава от плеч к бревну, кисти не рисуем
    for sgn in (-1, 1):
        px_ = cx + sgn * rost * .17 * kx_
        tx_ = cx + sgn * 230 * kx_
        ty_ = bry + 86
        dl = math.hypot(tx_ - px_, ty_ - plech)
        ug = math.degrees(math.atan2(ty_ - plech, tx_ - px_))
        ruk, _ = rukav(px_, plech, dl, ug, t, "#5c6c86", "#ffd98a",
                       .2 if sgn < 0 else .6, 3.0)
        s += SL(Z_SRED, ruk)
    brv = (f'<rect x="440" y="{bry:.0f}" width="1000" height="124" rx="56"'
           f' fill="url(#brev)" {o(9)}/>')
    brv += (f'<ellipse cx="440" cy="{bry+62:.0f}" rx="36" ry="64" fill="#5a3721" {o(6)}/>'
            f'<ellipse cx="1440" cy="{bry+62:.0f}" rx="36" ry="64" fill="#5a3721" {o(6)}/>')
    for i in range(6):
        brv += (f'<path d="M{540+i*160:.0f},{bry+28:.0f} q40,62 0,74" fill="none"'
                f' stroke="#5a3721" stroke-width="7" opacity=".6"/>')
    brv += (f'<ellipse cx="440" cy="{bry+62:.0f}" rx="20" ry="36" fill="#7a5436"'
            f' opacity=".7"/>')
    s += SL(Z_SRED, brv)
    shchel = abs(A.w(t, .9, .05))
    nx, ny = 1430, gy_ - 60
    nozh = (f'<circle cx="{nx}" cy="{ny:.0f}" r="18" fill="{CHUGUN}" {o(4)}/>')
    for sgn in (-1, 1):
        ang = sgn * (8 + 22 * shchel)
        nozh += (f'<g transform="rotate({ang:.1f} {nx} {ny:.0f})">'
                 f'<path d="M{nx},{ny:.0f} l-230,-26 l-6,34 l236,20 Z" fill="url(#zhel)" {o(5)}/>'
                 f'<path d="M{nx},{ny:.0f} l-210,-18" stroke="#dfe8f2" stroke-width="6" opacity=".6"/></g>')
    nozh += (f'<path d="M{nx+10},{ny-20:.0f} q90,-40 110,10 q-80,40 -110,-10 Z"'
             f' fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, nozh)
    pad = ""                                  # срезанные пряди падают запятыми
    for i in range(11):
        p = ((t * .56) + i / 11.0) % 1.0
        px2 = 1180 + i * 30 + 24 * A.w(t, 1.9, i * .14)
        py2 = gy_ + 30 + p * 480
        kr = 26 + 10 * (1 - p)
        pad += (f'<path d="M{px2:.0f},{py2:.0f} q{kr*.9:.0f},{kr*.5:.0f}'
                f' {kr*.5:.0f},{kr*1.3:.0f} q{-kr*.7:.0f},{-kr*.2:.0f}'
                f' {-kr*.5:.0f},{-kr*1.3:.0f} Z" fill="#7a5436"'
                f' opacity="{(1-p)*.95:.2f}" {o(3)}/>')
    s += SL(Z_SRED, pad)
    for i in range(5):                        # кудри на полу уже лежат
        s += SL(Z_SRED, f'<ellipse cx="{1120+i*110:.0f}" cy="{972+((i%2)*10)}"'
                        f' rx="{34+i*3:.0f}" ry="14" fill="#6b4a2e"'
                        f' opacity="{.5+.4*sdul:.2f}" {o(3)}/>')
    s += SL(Z_SRED, svecha(1660, 790, t, .1, 1.5, 110))
    s += SL(Z_SRED, teplo(1670, 740, 300, 250, .44))
    s += SL(Z_SRED, kot(300, 950, t, .72, "#3b3430"))
    s += SL(Z_PERED, ramka_pp("oba", "#0b0908", .6))
    s += vinetka(.44)
    return s


def primorskiy_gorod_pervogo_veka(t):
    """Белый каменный город на склоне над бухтой: черепичные крыши, кипарисы,
    на переднем плане каменная арка на пол-кадра, в проёме живое море."""
    rnd = random.Random(1301)
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, False, 223)
    s += oblaka(t, 150, 4, 227, .5, "#ffffff", 7.0)
    s += SL(Z_DAL, teplo(1620, 160, 460, 400, .54 + .1 * abs(A.w(t, 3.0))))
    s += SL(Z_DAL, f'<circle cx="1620" cy="150" r="96" fill="{SVET}" opacity=".9"/>')
    gor = (f'<path d="M-20,760 q380,-260 760,-220 q560,28 1200,240 Z" fill="#b9ab94" {o(6)}/>')
    for i in range(14):
        hx = 120 + i * 130 + rnd.uniform(-30, 30)
        hy = 700 - rnd.uniform(0, 200)
        hw = rnd.uniform(90, 160); hh = rnd.uniform(80, 150)
        gor += (f'<rect x="{hx:.0f}" y="{hy-hh:.0f}" width="{hw:.0f}" height="{hh:.0f}"'
                f' rx="6" fill="#f0ead9" {o(5)}/>')
        gor += (f'<path d="M{hx-14:.0f},{hy-hh:.0f} h{hw+28:.0f} l-18,-34 h{-hw+8:.0f} Z"'
                f' fill="#b4603c" {o(4)}/>')
        gor += (f'<rect x="{hx+hw*.3:.0f}" y="{hy-hh*.6:.0f}" width="{hw*.26:.0f}"'
                f' height="{hh*.34:.0f}" fill="#54504a" opacity=".8"/>')
        if i % 4 == 0:
            gor += dym(hx + hw * .6, hy - hh - 30, t, 3, .22, 160, .3, "#e2e6ea", .6)
    s += SL(Z_DAL, gor)
    kip = ""
    for i in range(7):
        kx = 90 + i * 250
        kh = 240 + rnd.uniform(-60, 90)
        sway = 2.4 * A.w(t, 3.6, i * .17)
        kip += (f'<g transform="rotate({sway:.2f} {kx:.0f} 770)">'
                f'<path d="M{kx:.0f},770 q-54,{-kh*.5:.0f} 0,{-kh:.0f}'
                f' q54,{kh*.5:.0f} 0,{kh:.0f} Z" fill="#2f4a33" {o(5)}/>'
                f'<rect x="{kx-10:.0f}" y="760" width="20" height="40" fill="#53422c"/></g>')
    s += SL(Z_DAL, kip)
    for i in range(5):
        s += SL(Z_DAL, ptica(360 + i * 300, 260 + i * 46, t, .7, "#f2f5f8", i * .2, "#dfe6ec"))
    ax, ay, aw, ah = 520, 250, 880, 700
    put = kontur_proema(ax, ay, aw, ah, "arka")
    vid = f'<clipPath id="arka13"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#2f6b78"/>'
    more = f'<rect x="{ax}" y="{ay}" width="{aw}" height="{ah*.44:.0f}" fill="url(#nden)"/>'
    more += (f'<rect x="{ax}" y="{ay+ah*.42:.0f}" width="{aw}" height="{ah*.6:.0f}"'
             f' fill="url(#voda)"/>')
    for i in range(9):
        yy = ay + ah * .46 + i * 46
        dxw = 34 * A.w(t, 2.4 + i * .3, i * .2)
        more += (f'<path d="M{ax-20},{yy:.0f} q{aw*.25:.0f},{-18+dxw:.0f} {aw*.5:.0f},0'
                 f' q{aw*.25:.0f},{18-dxw:.0f} {aw*.5+40:.0f},0" fill="none"'
                 f' stroke="#8ec4cf" stroke-width="{7-i*.4:.1f}" opacity="{.5-i*.03:.2f}"/>')
    more += (f'<ellipse cx="{ax+aw*.5:.0f}" cy="{ay+ah*.42:.0f}" rx="{aw*.4:.0f}" ry="26"'
             f' fill="{SVET}" opacity=".32"/>')
    vid += f'<g clip-path="url(#arka13)">{more}</g>'
    vid += mesto_stoka(ax, ay, aw, ah, "arka")
    ob = kladka(ax - 150, ay + 120, 150, ah - 120 + 130, 76, "url(#kamen)")
    ob += kladka(ax + aw, ay + 120, 150, ah - 120 + 130, 76, "url(#kamen)")
    for i in range(11):
        a = math.pi * (i / 10.0)
        bx_ = ax + aw * .5 - aw * .5 * math.cos(a)
        by_ = ay + aw * .5 - aw * .5 * math.sin(a)
        ob += (f'<g transform="rotate({-90+i*18:.0f} {bx_:.0f} {by_:.0f})">'
               f'<rect x="{bx_-56:.0f}" y="{by_-14:.0f}" width="112" height="86" rx="8"'
               f' fill="url(#kamen)" stroke="#4b443b" stroke-width="4"/></g>')
    ob += (f'<path d="{put}" fill="none" {o(9)}/>')
    vid += ob
    s += SL(Z_SRED, vid)
    s += SL(Z_SRED, blik(ax + aw * .5, ay + ah * .36, t, .7, "#cfe8ff", SVET, .42))
    hod = A.ease(A.seg(t, .4, 3.4))
    for i, (dx, hh) in enumerate(((0, 360), (150, 300))):
        s += SL(Z_PERED, figura(300 + dx + hod * 180, 1010, hh, t,
                                "#3a3242", "#fff0cf", False, i * .4, True))
    s += SL(Z_PERED, f'<line x1="{300+hod*180:.0f}" y1="1000" x2="{280+hod*180:.0f}"'
                     f' y2="640" stroke="url(#derev)" stroke-width="16"/>')
    s += SL(Z_PERED, f'<path d="M-20,1020 q400,-60 900,-20 l0,110 h-920 Z"'
                     f' fill="#8f8270" opacity=".9"/>')
    s += vinetka(.4)
    return s


def svitok_i_glinyanyy_svetilnik(t):
    """На каменном столе разворачивается папирусный свиток на пол-кадра, рядом
    горит глиняный светильник, тростниковое перо ведёт по папирусу."""
    rnd = random.Random(1409)
    s = f'<rect width="{W}" height="{H}" fill="#2a2420"/>'
    s += nebo("noch", t, False, 229)
    s += SL(Z_DAL, kladka(0, 0, W, 620, 86, "url(#kamen)"))
    s += SL(Z_DAL, svody(t, "#4b443b", 3))
    s += SL(Z_DAL, f'<path d="M1480,160 q120,-60 240,0 l0,300 h-240 Z" fill="#1d1a16" {o(6)}/>')
    s += SL(Z_DAL, mebel_hlam(60, 980, 420, t, 23))
    s += SL(Z_SRED, kladka(-40, 700, 2000, 400, 92, "url(#kamen)"))
    s += SL(Z_SRED, f'<rect x="-40" y="690" width="2000" height="34" rx="8"'
                    f' fill="{KAMEN2}" {o(7)}/>')
    raz = A.out(A.seg(t, .3, 1.5))
    sw = 340 + raz * 940
    sx, sy = 960 - sw / 2, 430
    sv = (f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="430" rx="10"'
          f' fill="url(#list)" {o(7)}/>')
    for i in range(9):
        sv += (f'<path d="M{sx+30:.0f},{sy+40+i*44:.0f} q{sw*.25:.0f},10 {sw*.5:.0f},0'
               f' q{sw*.25:.0f},-10 {sw*.5-60:.0f},0" fill="none" stroke="#cfc29a"'
               f' stroke-width="3" opacity=".6"/>')
    for sgn, px in ((-1, sx), (1, sx + sw)):
        sv += (f'<rect x="{px-34:.0f}" y="{sy-30}" width="68" height="490" rx="34"'
               f' fill="url(#derev)" {o(7)}/>')
        sv += (f'<ellipse cx="{px:.0f}" cy="{sy-30}" rx="34" ry="14" fill="{MED}" {o(5)}/>'
               f'<ellipse cx="{px:.0f}" cy="{sy+460}" rx="34" ry="14" fill="{MED}" {o(5)}/>')
    s += SL(Z_SRED, sv)
    pish = A.seg(t, 1.0, 1.1)
    pex, pey = 960 - 260 + pish * 520, sy + 250
    shtr = ""
    for r in range(3):
        d = f'M{960-260:.0f},{sy+150+r*70:.0f}'
        nn = max(1, int(9 * pish))
        for i in range(nn):
            d += (f' q{30:.0f},{-26 if i % 2 == 0 else 26} {60:.0f},0')
        shtr += (f'<path d="{d}" fill="none" stroke="#2b2118" stroke-width="{10-r*2}"'
                 f' stroke-linecap="round" opacity="{.9-r*.2:.2f}"/>')
    s += SL(Z_SRED, shtr)
    per_a = -52 + 9 * A.w(t, .7, .1)
    s += SL(Z_SRED, f'<g transform="rotate({per_a:.1f} {pex:.0f} {pey:.0f})">'
                    f'<path d="M{pex:.0f},{pey:.0f} l18,-300 l22,8 l-22,296 Z"'
                    f' fill="url(#solom)" {o(5)}/>'
                    f'<path d="M{pex:.0f},{pey:.0f} l20,-34 l14,30 Z" fill="#2b2118" {o(3)}/></g>')
    s += SL(Z_SRED, f'<ellipse cx="{pex+70:.0f}" cy="{pey+30:.0f}" rx="130" ry="24"'
                    f' fill="#2b2118" opacity=".26"/>')
    lx, ly = 1620, 650
    sve = (f'<path d="M{lx-130},{ly} q-30,-96 40,-116 q90,-24 180,0 q70,20 40,116 Z"'
           f' fill="url(#glina)" {o(8)}/>')
    sve += (f'<ellipse cx="{lx+10:.0f}" cy="{ly-118}" rx="128" ry="36" fill="#9c6a3c" {o(6)}/>')
    sve += (f'<path d="M{lx-158},{ly-104} q-70,10 -40,44 q40,16 56,-18 Z" fill="url(#glina)" {o(5)}/>')
    sve += ogon(lx - 150, ly - 112, t, .62, .2, 5)
    sve += ogon(lx + 30, ly - 128, t, .8, .5, 6)
    sve += teplo(lx, ly - 150, 420, 340, .56 + .12 * abs(A.w(t, 1.3)))
    s += SL(Z_SRED, sve)
    s += SL(Z_SRED, iskra_let(t, lx, ly - 170, 7, 233, 240, .4))
    s += SL(Z_SRED, krynka(360, 700, 1.3))
    s += SL(Z_SRED, monety(300, 640, t, 6, 239, 1.2))
    s += SL(Z_PERED, ramka_pp("levo", "#0b0908", .5))
    s += SL(Z_PERED, f'<path d="M-20,1060 q420,-70 940,-26 l0,120 h-960 Z"'
                     f' fill="#1a1612" opacity=".9"/>')
    s += vinetka(.44)
    return s


def dvoe_na_ulice_primorskogo_goroda(t):
    """Узкая улица с лавками под навесами: амфоры, корзины с рыбой и оливками,
    посреди улицы со спины идут высокий старший с посохом и младший с сумой.

    Двое стоят ПО ЦЕНТРУ и КРУПНО, ногами на мостовой у нижней трети, чтобы
    подписи имён ложились рядом с людьми, а не висели в пустом небе
    (осмотр 14.11)."""
    rnd = random.Random(1511)
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, False, 241)
    s += oblaka(t, 120, 3, 251, .4, "#ffffff", 6.0)
    s += SL(Z_DAL, teplo(960, 60, 520, 380, .4))
    st = (f'<rect x="-20" y="80" width="520" height="900" fill="#efe7d4" {o(7)}/>'
          f'<rect x="1420" y="80" width="520" height="900" fill="#e6ddc8" {o(7)}/>')
    for i in range(6):
        st += (f'<rect x="{40+i*70:.0f}" y="{200+((i%2)*40)}" width="48" height="120"'
               f' rx="6" fill="#55504a" opacity=".75"/>')
        st += (f'<rect x="{1470+i*70:.0f}" y="{180+((i%2)*44)}" width="48" height="120"'
               f' rx="6" fill="#55504a" opacity=".75"/>')
    st += (f'<path d="M-20,900 q960,-110 1960,0 l0,200 h-1960 Z" fill="#c2b49b" {o(6)}/>')
    for i in range(10):
        st += (f'<path d="M{-20+i*200:.0f},{960+((i%2)*26)} h180" stroke="#9c8f78"'
               f' stroke-width="8" opacity=".7"/>')
    s += SL(Z_DAL, st)
    nav = ""
    for i, (bx, col) in enumerate(((60, "#b8323a"), (1500, "#3f5c7a"), (300, "#8a6a30"))):
        kol = 16 * A.w(t, 2.6, i * .3)
        nav += (f'<path d="M{bx:.0f},300 h360 q-20,{90+kol*.4:.0f} -180,{120+kol:.0f}'
                f' q-160,{-30-kol*.6:.0f} -180,{-120-kol*.3:.0f} Z" fill="{col}"'
                f' opacity=".92" {o(6)}/>')
        nav += (f'<rect x="{bx-10:.0f}" y="290" width="26" height="420" fill="url(#derev)" {o(5)}/>'
                f'<rect x="{bx+350:.0f}" y="290" width="26" height="420" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, nav)
    lav = ""
    for i, bx in enumerate((80, 1560)):
        lav += stol(bx, 700, 290, 30)
        for j in range(3):
            lav += (f'<ellipse cx="{bx+56+j*86:.0f}" cy="{680-((j%2)*10)}" rx="44" ry="25"'
                    f' fill="{["#8a4d3a","#5f7a3a","#a0763c"][j]}" {o(4)}/>')
        lav += (f'<path d="M{bx+10:.0f},860 l10,-120 q130,-34 260,0 l10,120 Z"'
                f' fill="url(#solom)" {o(6)}/>')
        for j in range(5):
            lav += (f'<ellipse cx="{bx+50+j*54:.0f}" cy="{750+((j%2)*14)}" rx="34" ry="16"'
                    f' fill="#9fb6cc" {o(3)}/>')
    for i, ax in enumerate((420, 1500)):
        lav += (f'<path d="M{ax-60:.0f},880 q-34,-220 60,-260 q94,40 60,260 Z"'
                f' fill="url(#glina)" {o(7)}/>'
                f'<ellipse cx="{ax:.0f}" cy="{620}" rx="56" ry="18" fill="#8a5a30" {o(5)}/>')
        for sgn in (-1, 1):
            lav += (f'<path d="M{ax+sgn*52:.0f},640 q{sgn*46},30 {sgn*6},76" fill="none"'
                    f' stroke="#9c6a3c" stroke-width="13"/>')
    s += SL(Z_SRED, lav)
    s += SL(Z_SRED, ogon(1760, 780, t, .9, .2, 6))
    s += SL(Z_SRED, dym(1760, 720, t, 4, .3, 260, .34, "#dde3e8", .8))
    s += SL(Z_SRED, teplo(1760, 740, 300, 250, .4))
    # ДВОЕ: середина кадра, рост в половину экрана, подписи лягут у плеч
    hod = A.ease(A.seg(t, .3, 4.2))
    base_y = 1016 + hod * 20
    sx1 = 820 + hod * 40
    sx2_ = 1130 + hod * 34
    s += SL(Z_SRED, figura(sx1, base_y, 660 + hod * 30, t, "#3d3345", "#fff0cf", False, .1, True))
    s += SL(Z_SRED, f'<line x1="{sx1+180:.0f}" y1="{base_y+6:.0f}"'
                    f' x2="{sx1+152:.0f}" y2="{base_y-700:.0f}"'
                    f' stroke="url(#derev)" stroke-width="22"/>')
    s += SL(Z_SRED, f'<circle cx="{sx1+152:.0f}" cy="{base_y-700:.0f}" r="22"'
                    f' fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, figura(sx2_, base_y + 10, 540 + hod * 26, t, "#42384c", "#fff0cf", False, .5, True))
    s += SL(Z_SRED, f'<path d="M{sx2_+70:.0f},{base_y-300:.0f} q110,46 80,164'
                    f' q-94,36 -130,-70 Z" fill="url(#rush)" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{sx2_+40:.0f},{base_y-350:.0f} q80,30 108,74"'
                    f' fill="none" stroke="#8a7a5a" stroke-width="12"/>')
    for i, (bx, ph) in enumerate(((260, .1), (1680, .5))):
        pok = 16 * abs(A.w(t, 1.9, ph))
        s += SL(Z_SRED, figura(bx, 940, 300, t, "#4a4050", "#ffeec8", i == 1, ph, True, 1.0, False, 2.2 + pok * .1))
    mal_x = 1870 - A.ease(A.seg(t, .6, 3.0)) * 520
    s += SL(Z_PERED, figura(mal_x, 1070, 260, t, "#4a3f52", "#fff0cf", False, .2, True))
    s += SL(Z_PERED, f'<ellipse cx="{mal_x+72:.0f}" cy="{890}" rx="46" ry="27"'
                     f' fill="url(#med)" {o(5)}/>')
    s += SL(Z_PERED, ramka_pp("levo", "#2a231c", .45))
    s += vinetka(.42)
    return s


def uchitel_i_dva_uchenika_pod_kolonna(t):
    """Тень колоннады и каменная скамья: седой учитель со спины держит
    раскрытый свиток, двое учеников пишут стилем по восковым дощечкам."""
    rnd = random.Random(1607)
    s = f'<rect width="{W}" height="{H}" fill="#3b352c"/>'
    s += nebo("den", t, False, 257)
    s += SL(Z_DAL, kladka(0, 0, W, 360, 84, "url(#kamen)"))
    s += SL(Z_DAL, svody(t, "#554c40", 4))
    kol = ""
    for i in range(5):
        kx = 90 + i * 430
        kol += (f'<rect x="{kx:.0f}" y="300" width="120" height="700" rx="10"'
                f' fill="#e3dbc6" {o(7)}/>')
        for j in range(7):
            kol += (f'<line x1="{kx+16+j*14:.0f}" y1="310" x2="{kx+16+j*14:.0f}" y2="990"'
                    f' stroke="#c8bfa6" stroke-width="5" opacity=".8"/>')
        kol += (f'<rect x="{kx-24:.0f}" y="250" width="168" height="58" rx="8"'
                f' fill="#efe7d2" {o(6)}/>')
        kol += (f'<rect x="{kx-18:.0f}" y="980" width="156" height="46" rx="8"'
                f' fill="#d8cfb8" {o(6)}/>')
    s += SL(Z_DAL, kol)
    s += SL(Z_DAL, ptica(220, 240, t, .9, "#cfd8e2", .3, "#aab6c2"))
    pol = ""
    polz = (t * .06) % 1.0
    for i in range(5):
        px = 40 + i * 430 + polz * 120
        pol += (f'<path d="M{px:.0f},1000 l170,0 l{250:.0f},-240 l-170,0 Z"'
                f' fill="{SVET}" opacity=".20"/>')
    s += SL(Z_SRED, pol)
    s += SL(Z_SRED, luch(500, 300, 240, 620, t, .17))
    s += SL(Z_SRED, f'<rect x="-20" y="990" width="1960" height="120" fill="#b7ac93" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="860" width="1180" height="60" rx="12"'
                    f' fill="#cdc2a8" {o(7)}/>'
                    f'<rect x="470" y="920" width="56" height="110" fill="#bdb299" {o(5)}/>'
                    f'<rect x="1490" y="920" width="56" height="110" fill="#bdb299" {o(5)}/>')
    ux, uy = 760, 880
    s += SL(Z_SRED, figura(ux, uy, 520, t, "#4b4255", "#fff2d4", False, .1, True))
    s += SL(Z_SRED, f'<path d="M{ux-60},{uy-470} q60,66 120,0 q-18,120 -60,124'
                    f' q-42,-4 -60,-124 Z" fill="#e4ebf2" opacity=".9" {o(5)}/>')
    svx, svy = ux + 230, uy - 330
    sv = (f'<rect x="{svx-180:.0f}" y="{svy-30:.0f}" width="360" height="250" rx="8"'
          f' fill="url(#list)" {o(6)}/>')
    for i in range(6):
        sv += (f'<path d="M{svx-150:.0f},{svy+10+i*38:.0f} q150,10 300,0" fill="none"'
               f' stroke="#cfc29a" stroke-width="4" opacity=".65"/>')
    for sgn in (-1, 1):
        sv += (f'<rect x="{svx+sgn*190-20:.0f}" y="{svy-50:.0f}" width="40" height="290" rx="20"'
               f' fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, sv)
    vedet = A.seg(t, .4, 4.0)
    ruk, (fx, fy) = rukav(ux + 110, uy - 280, 150, -14 + 26 * vedet, t, "#4b4255", "#fff2d4", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{fx:.0f}" cy="{fy:.0f}" rx="22" ry="16" fill="#4b4255" {o(4)}/>')
    for i, (bx, ph) in enumerate(((1180, .0), (1430, .4))):
        s += SL(Z_SRED, figura(bx, 900, 330, t, "#453b50", "#fff2d4", False, ph, True))
        dx_, dy_ = bx + 70, 760
        s += SL(Z_SRED, f'<rect x="{dx_-80:.0f}" y="{dy_:.0f}" width="190" height="130" rx="8"'
                        f' fill="url(#derev)" {o(6)}/>'
                        f'<rect x="{dx_-62:.0f}" y="{dy_+16:.0f}" width="154" height="98" rx="5"'
                        f' fill="#d9c48f" {o(4)}/>')
        car = 24 * A.w(t, .8, ph)
        s += SL(Z_SRED, f'<line x1="{dx_+car:.0f}" y1="{dy_+70:.0f}" x2="{dx_+car-30:.0f}"'
                        f' y2="{dy_-90:.0f}" stroke="{ZHELEZ}" stroke-width="10"/>')
        for j in range(3):
            s += SL(Z_SRED, f'<path d="M{dx_-50+j*18:.0f},{dy_+40+j*20:.0f} h{80-j*14}"'
                            f' stroke="#9c8a5e" stroke-width="5" opacity=".8"/>')
    s += SL(Z_SRED, svecha(300, 980, t, .2, 1.6, 120))
    s += SL(Z_SRED, teplo(310, 920, 320, 270, .42))
    s += SL(Z_PERED, ramka_pp("pravo", "#211c16", .55))
    s += vinetka(.44)
    return s


def rynochnaya_ploschad_slushaet(t):
    """Рыночная площадь у фонтана: на каменном возвышении двое со спины,
    старший поднял руку; толпа прибывает, рыбак бросает сеть, весы качаются."""
    rnd = random.Random(1709)
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, False, 263)
    s += oblaka(t, 130, 4, 269, .42, "#ffffff", 6.5)
    s += SL(Z_DAL, teplo(400, 100, 440, 360, .38))
    dom = ""
    for i in range(6):
        dx_ = -40 + i * 330
        dh = 320 + rnd.uniform(-60, 120)
        dom += (f'<rect x="{dx_:.0f}" y="{620-dh:.0f}" width="290" height="{dh:.0f}"'
                f' rx="6" fill="#ece3cf" {o(6)}/>')
        dom += (f'<path d="M{dx_-20:.0f},{620-dh:.0f} h330 l-26,-46 h-278 Z"'
                f' fill="#b4603c" {o(5)}/>')
        for j in range(3):
            dom += (f'<rect x="{dx_+40+j*80:.0f}" y="{660-dh:.0f}" width="54" height="86"'
                    f' rx="6" fill="#55504a" opacity=".75"/>')
        if i % 3 == 1:
            dom += dym(dx_ + 200, 620 - dh - 40, t, 3, .24, 180, .28, "#e2e6ea", .7)
    s += SL(Z_DAL, dom)
    s += SL(Z_DAL, f'<path d="M-20,620 q980,-30 1960,0 l0,120 h-1960 Z" fill="#c9bca3" {o(5)}/>')
    fon = (f'<ellipse cx="300" cy="860" rx="280" ry="90" fill="url(#voda)" {o(7)}/>'
           f'<ellipse cx="300" cy="836" rx="280" ry="86" fill="#cdc2a8" {o(7)}/>'
           f'<ellipse cx="300" cy="840" rx="222" ry="62" fill="url(#voda)"/>'
           f'<rect x="276" y="640" width="48" height="200" fill="#d8cfb8" {o(5)}/>'
           f'<ellipse cx="300" cy="630" rx="80" ry="26" fill="#d8cfb8" {o(5)}/>')
    for i in range(8):
        p = ((t * .8) + i / 8.0) % 1.0
        fon += (f'<circle cx="{300+(i-4)*34:.0f}" cy="{620+p*210:.0f}"'
                f' r="{6+6*(1-p):.1f}" fill="#bfe0e8" opacity="{(1-p)*.8:.2f}"/>')
    s += SL(Z_SRED, fon)
    vx, vy, vw = 900, 880, 700
    voz = kladka(vx, vy - 150, vw, 200, 70, "url(#kamen)")
    voz += (f'<rect x="{vx-20}" y="{vy-170}" width="{vw+40}" height="40" rx="8"'
            f' fill="#d8cfb8" {o(7)}/>')
    s += SL(Z_SRED, voz)
    s += SL(Z_SRED, figura(vx + 230, vy - 170, 470, t, "#44394e", "#fff2d4", False, .1, True))
    ruk, (hx, hy) = rukav(vx + 300, vy - 480, 190, -74 + 7 * A.w(t, 2.2), t, "#44394e", "#fff2d4", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="24" ry="18" fill="#44394e" {o(4)}/>')
    s += SL(Z_SRED, figura(vx + 450, vy - 166, 380, t, "#4b4055", "#fff2d4", False, .5, True))
    tol = ""
    pri = A.ease(A.seg(t, .3, 3.6))
    for i in range(11):
        tx = 120 + i * 168 + (1 - pri) * (i - 5) * 80
        hh = 250 + ((i * 37) % 70)
        tol += figura(tx, 1070 - ((i % 3) * 14), hh, t, "#3b3345", "#fff2d4",
                      i % 3 == 0, ph=i * .19, op=.95, shapka=i % 3 == 1)
    s += SL(Z_PERED, tol)
    set_ = A.seg(t, .8, 1.6)
    rx_, ry_ = 1700, 860
    seti = (f'<path d="M{rx_:.0f},{ry_:.0f} q{-120*set_:.0f},{-200*set_:.0f}'
            f' {-280*set_:.0f},{-80*set_:.0f}" fill="none" stroke="#cfd6de" stroke-width="5"/>')
    for i in range(7):
        seti += (f'<path d="M{rx_-40*i*set_:.0f},{ry_-40-30*i*set_:.0f} l{-60*set_:.0f},{70*set_:.0f}"'
                 f' stroke="#cfd6de" stroke-width="3" opacity=".7"/>')
    s += SL(Z_SRED, seti)
    s += SL(Z_SRED, figura(1760, 1000, 350, t, "#473c50", "#fff2d4", False, .3, True))
    boch = (f'<path d="M160,1060 l12,-200 q90,-26 180,0 l12,200 Z" fill="url(#derev)" {o(7)}/>')
    for yy in (960, 1010):
        boch += (f'<path d="M156,{yy} q104,20 216,0" fill="none" stroke="{ZHELEZ}"'
                 f' stroke-width="12"/>')
    s += SL(Z_PERED, boch)
    for i in range(2):
        s += SL(Z_PERED, figura(200 + i * 110, 858 - i * 10, 210, t, "#3f3648", "#fff2d4", False, i * .4, True))
    ves_a = 11 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<g transform="rotate({ves_a:.1f} 700 560)">'
                    f'<line x1="540" y1="560" x2="860" y2="560" stroke="{ZHELEZ}" stroke-width="10"/>'
                    f'<path d="M560,560 l-30,70 h60 Z" fill="url(#med)" {o(4)}/>'
                    f'<path d="M840,560 l-30,70 h60 Z" fill="url(#med)" {o(4)}/></g>'
                    f'<line x1="700" y1="420" x2="700" y2="560" stroke="{ZHELEZ}" stroke-width="8"/>')
    s += SL(Z_SRED, ogon(1480, 700, t, .8, .3, 5))
    s += SL(Z_SRED, dym(1480, 650, t, 4, .3, 240, .3, "#dde3e8", .8))
    s += vinetka(.42)
    return s


def gradonachalnik_na_balkone(t):
    """Каменный балкон дворца над площадью: толстый градоначальник в тоге с
    пурпурной каймой резко указывает перстом вниз, ниже выходят стражники.

    Голова ЦЕЛИКОМ в кадре (прежде макушка уходила за верхний край), балюстрада
    сделана точёными балясинами с поручнем и пурпурным полотнищем — ряд белых
    полос балконом не читался (осмотр 14.11)."""
    rnd = random.Random(1801)
    s = f'<rect width="{W}" height="{H}" fill="#3a332b"/>'
    s += nebo("sumer", t, False, 271)
    s += SL(Z_DAL, kladka(0, 0, W, 560, 88, "url(#kamen)"))
    s += SL(Z_DAL, svody(t, "#4e463a", 3))
    s += SL(Z_DAL, f'<path d="M620,560 q340,-140 680,0 l0,120 h-680 Z" fill="#1d1a16" {o(6)}/>')
    fak = ""
    for i, fx in enumerate((250, 1670)):
        fak += (f'<rect x="{fx-16:.0f}" y="360" width="32" height="190" rx="10"'
                f' fill="url(#derev)" {o(5)}/>')
        fak += (f'<path d="M{fx-44:.0f},360 q44,-36 88,0 q-44,26 -88,0 Z" fill="{ZHELEZ}" {o(5)}/>')
        fak += ogon(fx, 356, t, 1.0, i * .4, 7)
        fak += teplo(fx, 310, 330, 280, .5)
    s += SL(Z_DAL, fak)
    # БАЛКОН: карниз, точёные балясины, поручень, пурпурное полотнище
    bx, by, bw = 400, 830, 1120
    bal = (f'<path d="M{bx-70},{by+150} h{bw+140} l-54,120 h{-bw-32} Z"'
           f' fill="#9c907a" {o(8)}/>')
    bal += kladka(bx, by + 56, bw, 120, 60, "url(#kamen)")
    bal += (f'<rect x="{bx-50}" y="{by+34}" width="{bw+100}" height="40" rx="10"'
            f' fill="#b4a98f" {o(7)}/>')
    for i in range(11):                      # балясины: ваза с перехватом
        px = bx + 44 + i * (bw - 88) / 10.0
        bal += (f'<path d="M{px-30:.0f},{by+34} q10,-22 2,-40 q-22,-14 -2,-30'
                f' q24,-12 2,-34 l56,0 q-22,22 2,34 q20,16 -2,30 q-8,18 2,40 Z"'
                f' fill="#e4dcc4" {o(5)}/>')
        bal += (f'<ellipse cx="{px:.0f}" cy="{by-34}" rx="21" ry="9"'
                f' fill="#cfc5a8" {o(3)}/>')
    bal += (f'<rect x="{bx-62}" y="{by-72}" width="{bw+124}" height="42" rx="12"'
            f' fill="#d8cfb8" {o(8)}/>')
    bal += (f'<rect x="{bx-62}" y="{by-72}" width="{bw+124}" height="14" rx="7"'
            f' fill="#f2ead6" opacity=".7"/>')
    kol_p = 10 * A.w(t, 1.9, .2)
    bal += (f'<path d="M{bx+170},{by-36} h420 l{-16-kol_p*.4:.0f},230'
            f' q-200,{30+kol_p:.0f} -390,0 Z" fill="#6b2a52" {o(7)}/>')
    for i in range(4):
        bal += (f'<path d="M{bx+200+i*100:.0f},{by+10} l-6,170" stroke="#90407a"'
                f' stroke-width="9" opacity=".75"/>')
    bal += (f'<path d="M{bx+170},{by-36} q210,36 420,0" fill="none" stroke="{ZOL}"'
            f' stroke-width="12" opacity=".8"/>')
    s += SL(Z_SRED, bal)
    # ГРАДОНАЧАЛЬНИК: голова у отметки 300, макушка в кадре
    gx, gy = 960, by - 60                    # gy — линия, где тога уходит за поручень
    gr = (f'<path d="M{gx-250},{gy} q-30,-300 250,-320 q280,20 250,320 Z"'
          f' fill="#f2ead6" {o(9)}/>')
    kol = 18 * A.w(t, 1.5, .1)
    gr += (f'<path d="M{gx-244},{gy-60} q{244+kol:.0f},58 488,-18 l0,46'
           f' q{-244-kol:.0f},76 -488,-14 Z" fill="#6b2a52" {o(5)}/>')
    gr += (f'<path d="M{gx-190},{gy-250} q190,66 380,-10" fill="none" stroke="#6b2a52"'
           f' stroke-width="24"/>')
    gr += (f'<rect x="{gx-44}" y="{gy-364}" width="88" height="70" fill="#dba884" {o(6)}/>')
    gr += (f'<ellipse cx="{gx}" cy="{gy-430}" rx="104" ry="100" fill="#dba884" {o(7)}/>')
    gr += (f'<path d="M{gx-94},{gy-488} q94,-46 188,0 q-18,-64 -94,-64 q-76,0 -94,64 Z"'
           f' fill="#5c5042" {o(5)}/>')
    for i in range(9):                       # венок
        a = -2.9 + i * .36
        gr += (f'<ellipse cx="{gx+math.cos(a)*108:.0f}" cy="{gy-492+math.sin(a)*54:.0f}"'
               f' rx="25" ry="15" fill="#4e6b34" {o(3)}/>')
    hmur = 16 * abs(A.w(t, 1.1, .2))
    gr += (f'<path d="M{gx-68},{gy-452+hmur*.4:.0f} l54,{-14-hmur*.3:.0f}"'
           f' stroke="{K}" stroke-width="11"/>'
           f'<path d="M{gx+68},{gy-452+hmur*.4:.0f} l-54,{-14-hmur*.3:.0f}"'
           f' stroke="{K}" stroke-width="11"/>')
    gr += (f'<circle cx="{gx-34}" cy="{gy-428}" r="{4 if A.blink(t,3.0,.1) else 10}" fill="{K}"/>'
           f'<circle cx="{gx+36}" cy="{gy-428}" r="{4 if A.blink(t,3.0,.1) else 10}" fill="{K}"/>')
    gr += (f'<path d="M{gx-10},{gy-424} l-14,40 q14,10 28,0" fill="none"'
           f' stroke="#b08763" stroke-width="8"/>')
    gr += (f'<path d="M{gx-52},{gy-368} q52,{-20-hmur:.0f} 104,0" fill="none"'
           f' stroke="{K}" stroke-width="9"/>')
    for i in (-1, 1):
        gr += (f'<ellipse cx="{gx+i*70:.0f}" cy="{gy-392}" rx="24" ry="15"'
               f' fill="#c07a62" opacity=".35"/>')
    s += SL(Z_SRED, gr)
    ukaz = A.over(A.seg(t, .4, .9))
    ruk, (px, py) = rukav(gx + 210, gy - 268, 230, 10 + 70 * ukaz, t, "#f2ead6", "#8a7a60", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="28" ry="20" fill="#dba884" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{px:.0f},{py+14:.0f} l10,70" stroke="#dba884"'
                    f' stroke-width="20" stroke-linecap="round"/>')
    str_ = A.ease(A.seg(t, 1.0, 1.9))
    strazh = ""
    for i in range(5):
        sx = 220 + i * 200 - (1 - str_) * 320
        strazh += figura(sx, 1076, 280, t, "#2f2a36", "#ffd98a", False,
                         ph=i * .23, op=.96)
        strazh += (f'<ellipse cx="{sx:.0f}" cy="{1076-280*.84:.0f}" rx="46" ry="38"'
                   f' fill="{ZHELEZ}" {o(4)}/>')
        strazh += (f'<path d="M{sx-48:.0f},{1076-280*.9:.0f} q48,-38 96,0 l0,16'
                   f' q-48,-28 -96,0 Z" fill="#8d9298" {o(3)}/>')
        kop = 7 * A.w(t, 2.0, i * .19)
        strazh += (f'<line x1="{sx+70+kop:.0f}" y1="1080" x2="{sx+56+kop:.0f}" y2="700"'
                   f' stroke="url(#derev)" stroke-width="13"/>')
        strazh += (f'<path d="M{sx+56+kop:.0f},700 l20,-70 l18,70 Z" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_PERED, strazh)
    s += vinetka(.46)
    return s


def ugovory_i_ugrozy(t):
    """Каменный зал, длинный стол на пол-кадра: перед двумя стоящими ставят
    блюдо с виноградом, кубок и мешочек монет, потом на стол падают цепи."""
    rnd = random.Random(1901)
    s = f'<rect width="{W}" height="{H}" fill="#2f2a22"/>'
    s += nebo("noch", t, False, 277)
    s += SL(Z_DAL, kladka(0, 0, W, 700, 90, "url(#kamen)"))
    s += SL(Z_DAL, svody(t, "#4b4238", 4))
    s += SL(Z_DAL, mebel_hlam(1560, 980, 360, t, 29))
    fak = ""
    for i, fx in enumerate((180, 1740)):
        fak += (f'<rect x="{fx-14:.0f}" y="260" width="28" height="170" rx="9"'
                f' fill="url(#derev)" {o(5)}/>')
        fak += ogon(fx, 258, t, 1.1, i * .5, 8)
        fak += teplo(fx, 210, 360, 300, .52)
    s += SL(Z_DAL, fak)
    teni = ""
    rost = A.ease(A.seg(t, 1.8, 1.6))
    for i in range(6):
        tx = 420 + i * 200
        th = 120 + rost * 520
        teni += (f'<path d="M{tx:.0f},700 l{-18-i*3},{-th:.0f} l36,0 Z"'
                 f' fill="#15110e" opacity="{.4+.3*rost:.2f}"/>')
        teni += (f'<path d="M{tx-20-i*3:.0f},{700-th:.0f} l20,-56 l20,56 Z"'
                 f' fill="#15110e" opacity="{.4+.3*rost:.2f}"/>')
    s += SL(Z_DAL, teni)
    s += SL(Z_SRED, f'<rect x="-20" y="880" width="1960" height="220" fill="#6a6252" {o(6)}/>')
    sx, sy, sw = 120, 740, 1700
    st = (f'<rect x="{sx}" y="{sy}" width="{sw}" height="70" rx="10"'
          f' fill="url(#derev)" {o(9)}/>')
    st += (f'<rect x="{sx+30}" y="{sy+70}" width="{sw-60}" height="26" rx="8"'
           f' fill="{DOSKA2}" {o(5)}/>')
    for px in (sx + 90, sx + sw - 170):
        st += (f'<path d="M{px:.0f},{sy+96} l-26,220 h130 l-26,-220 Z"'
               f' fill="url(#derev)" {o(7)}/>')
    for i in range(7):
        st += (f'<path d="M{sx+60+i*230:.0f},{sy+20} q60,18 120,0" fill="none"'
               f' stroke="#5a3a22" stroke-width="6" opacity=".6"/>')
    s += SL(Z_SRED, st)
    put = A.out(A.seg(t, .3, .9))
    dy_ = (1 - put) * -260
    bl = (f'<g transform="translate(0,{dy_:.0f})">'
          f'<ellipse cx="620" cy="{sy-6}" rx="180" ry="46" fill="url(#med)" {o(7)}/>'
          f'<ellipse cx="620" cy="{sy-18}" rx="166" ry="38" fill="#c8a35c"/>')
    for i in range(14):
        a = rnd.uniform(0, 6.28); rr = rnd.uniform(.1, 1.0)
        bl += (f'<circle cx="{620+math.cos(a)*140*rr:.0f}" cy="{sy-34+math.sin(a)*28*rr:.0f}"'
               f' r="{16+rnd.random()*7:.0f}" fill="{["#5b3a66","#6d4a78","#47304f"][i%3]}" {o(2)}/>')
    bl += (f'<path d="M560,{sy-80} q60,-40 120,0" fill="none" stroke="{ZEL}" stroke-width="8"/>')
    bl += '</g>'
    s += SL(Z_SRED, bl)
    kub = (f'<g transform="translate(0,{dy_*.8:.0f})">'
           f'<path d="M900,{sy-10} l-56,-150 q56,-26 112,0 l-56,150 Z" fill="url(#zol)" {o(7)}/>'
           f'<ellipse cx="900" cy="{sy-160}" rx="58" ry="18" fill="#8f6a1e" {o(5)}/>'
           f'<rect x="866" y="{sy-20}" width="68" height="22" rx="8" fill="url(#zol)" {o(5)}/>'
           f'<ellipse cx="880" cy="{sy-130}" rx="12" ry="22" fill="#fff0bb" opacity=".6"/></g>')
    s += SL(Z_SRED, kub)
    mes = (f'<g transform="translate(0,{dy_*.6:.0f})">'
           f'<path d="M1160,{sy-10} q-70,-120 10,-166 q80,-36 150,10 q66,46 -10,156 Z"'
           f' fill="url(#tkan)" {o(7)}/>'
           f'<path d="M1180,{sy-174} q60,-30 110,6" fill="none" stroke="{ZOL}" stroke-width="10"/></g>')
    s += SL(Z_SRED, mes)
    s += SL(Z_SRED, monety(1260, sy - 30, t, 7, 281, 1.3))
    smet = A.ease(A.seg(t, 1.5, .8))
    ruk, (hx, hy) = rukav(1420, sy - 230, 260, 160 - 26 * smet, t, "#3f3550", "#fff2d4", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="30" ry="20" fill="#3f3550" {o(4)}/>')
    cep_y = sy - 60 + A.out(A.seg(t, 2.1, .7)) * 60
    cep = ""
    for i in range(16):
        cep += (f'<ellipse cx="{320+i*62:.0f}" cy="{cep_y+16*A.w(t,1.2,i*.1):.0f}" rx="28" ry="18"'
                f' fill="none" stroke="{ZHELEZ}" stroke-width="12"/>')
    s += SL(Z_SRED, cep)
    for i, (bx, ph) in enumerate(((1560, .0), (1720, .45))):
        s += SL(Z_PERED, figura(bx, 1060, 500 - i * 50, t, "#3a3148", "#fff2d4", False, ph, True))
    s += SL(Z_PERED, svecha(260, 740, t, .3, 1.7, 120))
    s += SL(Z_PERED, teplo(270, 680, 340, 290, .48))
    s += vinetka(.5)
    return s


def dva_svetilnika_v_temnote(t):
    """Двое стоят плечом к плечу, со спины, и не оборачиваются: зал темнеет,
    два светильника разгораются, тени копий отступают."""
    rnd = random.Random(2003)
    s = f'<rect width="{W}" height="{H}" fill="#191511"/>'
    s += nebo("noch", t, False, 283)
    temn = A.ease(A.seg(t, .4, 2.6))
    s += SL(Z_DAL, kladka(0, 0, W, 760, 92, "url(#kamen)"))
    s += SL(Z_DAL, svody(t, "#3f382f", 3))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#0c0a08" opacity="{.30+.42*temn:.2f}"/>')
    s += SL(Z_DAL, mebel_hlam(90, 1000, 380, t, 31))
    otst = A.ease(A.seg(t, .8, 2.0))
    kop = ""
    for i in range(7):
        kx = 180 + i * 250 - otst * 260
        kh = 620 * (1 - .5 * otst)
        kop += (f'<path d="M{kx:.0f},900 l{-14-i*2},{-kh:.0f} l30,0 Z"'
                f' fill="#0f0d0b" opacity="{(.6-.36*otst):.2f}"/>')
        kop += (f'<path d="M{kx-16-i*2:.0f},{900-kh:.0f} l18,-64 l20,64 Z"'
                f' fill="#0f0d0b" opacity="{(.6-.36*otst):.2f}"/>')
    s += SL(Z_DAL, kop)
    kolon = ""
    for i, kx in enumerate((180, 1700)):
        kolon += (f'<rect x="{kx-80:.0f}" y="120" width="160" height="790" rx="10"'
                  f' fill="#3f392f" {o(6)}/>')
        kolon += (f'<rect x="{kx-110:.0f}" y="80" width="220" height="56" rx="10"'
                  f' fill="#4a4238" {o(5)}/>')
        for j in range(8):
            kolon += (f'<line x1="{kx-56+j*16:.0f}" y1="140" x2="{kx-56+j*16:.0f}" y2="900"'
                      f' stroke="#332e26" stroke-width="6"/>')
    s += SL(Z_SRED, kolon)
    s += SL(Z_SRED, f'<rect x="-20" y="900" width="1960" height="200" fill="#4d463a" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="770" width="560" height="44" rx="12"'
                    f' fill="#5e5648" {o(6)}/>'
                    f'<rect x="740" y="814" width="54" height="96" fill="#4e4739" {o(5)}/>'
                    f'<rect x="1166" y="814" width="54" height="96" fill="#4e4739" {o(5)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{-20+i*290:.0f},900 h260" stroke="#3a342b"'
                        f' stroke-width="8" opacity=".8"/>')
    s += SL(Z_SRED, figura(860, 920, 560, t, "#2a2436", "#ffe2a8", False, .1, False))
    s += SL(Z_SRED, figura(1080, 924, 530, t, "#2b2537", "#ffe2a8", False, .5, False))
    s += SL(Z_SRED, ten(970, 930, 260, 36, .55))
    for i, (lx, ph) in enumerate(((560, .0), (1400, .5))):
        gor = .35 + .65 * A.ease(A.seg(t, .6 + i * .5, 2.2))
        sve = (f'<path d="M{lx-120},{880} q-30,-90 36,-110 q84,-24 168,0'
               f' q66,20 36,110 Z" fill="url(#glina)" {o(8)}/>')
        sve += (f'<ellipse cx="{lx+10:.0f}" cy="{770}" rx="120" ry="34" fill="#8a5a30" {o(6)}/>')
        sve += (f'<path d="M{lx-140},{782} q-64,10 -36,42 q36,16 52,-18 Z"'
                f' fill="url(#glina)" {o(5)}/>')
        sve += (f'<rect x="{lx-34:.0f}" y="{880}" width="90" height="46" rx="10"'
                f' fill="#9c6a3c" {o(5)}/>')
        sve += ogon(lx - 132, 772, t, .5 * gor + .2, ph, 4)
        sve += ogon(lx + 20, 756, t, .9 * gor + .2, ph + .3, 7)
        sve += teplo(lx, 720, 420 * gor, 360 * gor, .6 * gor)
        sve += iskra_let(t, lx, 720, 8, 293 + i, 280, .45)
        s += SL(Z_SRED, sve)
    s += SL(Z_SRED, blik(560, 750, t, .55, "#cfe0ff", SVET, .34 + .3 * temn))
    s += SL(Z_SRED, blik(1400, 740, t, .55, "#cfe0ff", SVET, .34 + .3 * temn))
    s += SL(Z_PERED, ramka_pp("oba", "#070605", .55 + .3 * temn))
    s += SL(Z_PERED, f'<path d="M-20,1070 q460,-60 1000,-20 l0,110 h-1020 Z"'
                     f' fill="#0b0908" opacity=".92"/>')
    s += vinetka(.54)
    return s


def imya_letit_v_russkuyu_izbu(t):
    """Каменная ПЛИТА-СТЕЛА с выбитым именем: знаки снимаются с камня
    светящимися клиньями и летят к листку численника в избе.

    Плита сделана стелой: полукруглый верх, карниз, цоколь со ступенями,
    сколы и мох, а знаки сидят в УГЛУБЛЕНИИ. Прежний серый прямоугольник в
    линейку ни плитой, ни камнем не читался (осмотр 14.11)."""
    rnd = random.Random(2101)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 307)
    s += oblaka(t, 150, 4, 311, .3, "#c2cedd", 10.0)
    s += SL(Z_DAL, f'<rect x="-20" y="620" width="1000" height="200" fill="url(#voda)"/>')
    for i in range(7):
        s += SL(Z_DAL, f'<path d="M-20,{640+i*26} q240,{-16+10*A.w(t,2.2,i*.2):.0f} 500,0'
                       f' q240,{16-10*A.w(t,2.2,i*.2):.0f} 520,0" fill="none"'
                       f' stroke="#8ec4cf" stroke-width="5" opacity="{.42-i*.04:.2f}"/>')
    s += SL(Z_DAL, sneg_lezhit(790, 30))
    s += SL(Z_DAL, ulica_dal(980, 800, 900, t, True, 313))
    plx, ply = 360, 960
    pl = ten(plx, ply + 10, 300, 30, .5)
    pl += (f'<path d="M{plx-250},{ply-80} h500 l16,70 h-532 Z" fill="#6e6558" {o(8)}/>')
    pl += (f'<path d="M{plx-214},{ply-150} h428 l14,70 h-456 Z" fill="#7d7466" {o(7)}/>')
    pl += (f'<path d="M{plx-190},{ply-150} l10,-330 a190,190 0 0 1 360,0'
           f' l10,330 Z" fill="url(#kamen)" {o(9)}/>')
    pl += (f'<path d="M{plx-196},{ply-430} a196,196 0 0 1 392,0 l-16,44'
           f' a178,178 0 0 0 -360,0 Z" fill="#9c9183" {o(6)}/>')
    pl += (f'<path d="M{plx-164},{ply-172} h328 l6,34 h-340 Z" fill="#9c9183" {o(5)}/>')
    pl += (f'<path d="M{plx-150},{ply-396} a150,150 0 0 1 300,0 l8,210 h-316 Z"'
           f' fill="#5e564c" opacity=".55"/>')
    snyat = A.seg(t, .3, 2.0)
    for i in range(10):                      # знаки в углублении снимаются
        gl = max(0.0, 1.0 - max(0.0, snyat * 10 - i))
        gx = plx - 104 + (i % 5) * 52
        gy = ply - 330 + (i // 5) * 104
        pl += (f'<path d="M{gx:.0f},{gy:.0f} l34,-12 l8,58 l-34,12 Z" fill="#2a251e"'
               f' opacity=".92"/>')
        pl += (f'<path d="M{gx+2:.0f},{gy+2:.0f} l34,-12 l2,10 l-34,12 Z"'
               f' fill="#b9aE97" opacity=".35"/>')
        if gl > .02:
            pl += (f'<path d="M{gx:.0f},{gy:.0f} l34,-12 l8,58 l-34,12 Z" fill="{SVET}"'
                   f' opacity="{gl*.9:.2f}"/>')
    for i in range(5):                       # сколы и трещины
        cx_ = plx - 150 + rnd.uniform(0, 300)
        cy_ = ply - 420 + rnd.uniform(0, 260)
        pl += (f'<path d="M{cx_:.0f},{cy_:.0f} l{rnd.uniform(14,34):.0f},'
               f'{rnd.uniform(20,60):.0f} l{rnd.uniform(-20,-8):.0f},'
               f'{rnd.uniform(10,30):.0f}" fill="none" stroke="#4e483e"'
               f' stroke-width="5" opacity=".7"/>')
    for i in range(7):                       # мох по цоколю
        pl += (f'<ellipse cx="{plx-220+i*74:.0f}" cy="{ply-86+((i%2)*10)}" rx="36"'
               f' ry="13" fill="#5f7a40" opacity=".55"/>')
    s += SL(Z_DAL, pl)
    s += SL(Z_DAL, teplo(plx, ply - 330, 420, 360, .34 + .14 * abs(A.w(t, 1.8))))
    letit = ""
    for i in range(10):
        p = min(1.0, max(0.0, (t - .4 - i * .16) / 2.4))
        if p <= 0:
            continue
        lx = plx - 120 + A.ease(p) * 1500
        ly = ply - 350 - math.sin(math.pi * p) * 330
        rot = p * 540 + i * 36
        letit += (f'<g transform="rotate({rot:.0f} {lx:.0f} {ly:.0f})">'
                  f'<path d="M{lx:.0f},{ly:.0f} l46,-16 l12,74 l-46,16 Z" fill="{SVET}"'
                  f' opacity="{.5+.5*(1-p):.2f}"/></g>')
        letit += (f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{16+16*(1-p):.0f}" fill="{SVET}"'
                  f' opacity="{(1-p)*.35:.2f}"/>')
    s += SL(Z_SRED, letit)
    s += SL(Z_SRED, brevna(1180, 60, 760, 980, 96))
    s += SL(Z_SRED, okno_izby(1240, 160, 290, 230, t, svet=False, moroz=.5))
    chx, chy = 1700, 560
    ch = (f'<rect x="{chx-150:.0f}" y="{chy-230:.0f}" width="300" height="300" rx="10"'
          f' fill="url(#list)" {o(8)}/>')
    ch += (f'<rect x="{chx-150:.0f}" y="{chy-230:.0f}" width="300" height="76" rx="8"'
           f' fill="{TKAN}" {o(6)}/>')
    shev = 7 * A.w(t, 1.4, .2)
    ch += (f'<g transform="rotate({shev:.1f} {chx:.0f} {chy-154:.0f})">'
           f'<rect x="{chx-130:.0f}" y="{chy-150:.0f}" width="260" height="210" rx="6"'
           f' fill="#fbf7ea" {o(5)}/>')
    for i in range(4):
        ch += (f'<path d="M{chx-100:.0f},{chy-60+i*34:.0f} h200" stroke="#d6cbae"'
               f' stroke-width="5" opacity=".8"/>')
    ch += '</g>'
    ch += (f'<circle cx="{chx:.0f}" cy="{chy-212:.0f}" r="12" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, ch)
    s += SL(Z_SRED, teplo(chx, chy - 120, 340, 290, .40 + .16 * abs(A.w(t, 1.2))))
    s += SL(Z_SRED, lampa(1300, 700, t, .9, False))
    s += SL(Z_SRED, figura(1480, 1010, 420, t, "#241e2b", "#ffd98a", True, .2))
    s += SL(Z_PERED, goloe_derevo(170, 1070, 560, t, 317, 7, "#2a2b33"))
    s += SL(Z_LETIT, mokryy_sneg(t, 30, 331, .56, 1.0))
    s += vinetka(.44)
    return s


def tri_zhizni_odnogo_cheloveka(t):
    """Зелёный склон: молодой пастух с посохом и свирелью стоит среди овец и
    смотрит на дорогу, по которой в пыли идёт войско со значками.

    Свирель идёт ОТ ГУБ ВНИЗ-ВПЕРЁД и лица не пересекает: прежде палка
    проходила сквозь голову и торчала с обеих сторон (осмотр 14.11)."""
    rnd = random.Random(2203)
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, False, 337)
    s += oblaka(t, 170, 5, 347, .5, "#ffffff", 8.0)
    s += SL(Z_DAL, teplo(300, 120, 480, 400, .4))
    skl = (f'<path d="M-20,760 q500,-200 1000,-120 q520,80 960,-40 l0,500 h-1960 Z"'
           f' fill="#6f8c4a" {o(6)}/>')
    skl += (f'<path d="M-20,880 q520,-130 1040,-50 q480,70 940,-30 l0,300 h-1960 Z"'
            f' fill="#5c7a40" opacity=".85"/>')
    for i in range(22):
        gx = rnd.uniform(0, W); gy = rnd.uniform(800, 1070)
        skl += (f'<path d="M{gx:.0f},{gy:.0f} q{-6+8*A.w(t,2.8,i*.1):.0f},-30'
                f' {2:.0f},-52" fill="none" stroke="#86a456" stroke-width="6"/>')
    s += SL(Z_DAL, skl)
    doroga = (f'<path d="M980,700 q320,30 960,-20 l0,70 q-640,60 -960,10 Z"'
              f' fill="#b5a888" opacity=".9"/>')
    s += SL(Z_DAL, doroga)
    hod = A.seg(t, .2, 5.0)
    voy = ""
    for i in range(9):
        vx = 1900 - hod * 520 - i * 80
        voy += figura(vx, 740 + (i % 3) * 8, 150 + (i % 2) * 14, t, "#4e4538",
                      "#f2e6c8", False, ph=i * .27, op=.9, shapka=True)
        voy += (f'<line x1="{vx+24:.0f}" y1="736" x2="{vx+16:.0f}" y2="590"'
                f' stroke="#6b5a3c" stroke-width="7"/>')
        voy += (f'<path d="M{vx+16:.0f},590 q40,-14 54,18 q-42,16 -56,-4 Z"'
                f' fill="{["#8f2f33","#6b2a52","#8a6a30"][i%3]}" {o(3)}/>')
    for i in range(9):
        p = ((t * .5) + i / 9.0) % 1.0
        voy += (f'<ellipse cx="{1300+i*70-hod*300:.0f}" cy="{730-p*40:.0f}"'
                f' rx="{40+70*p:.0f}" ry="{18+30*p:.0f}" fill="#d8cdae"'
                f' opacity="{(1-p)*.42:.2f}"/>')
    s += SL(Z_DAL, voy)
    px, py = 620, 980
    s += SL(Z_SRED, figura(px, py, 560, t, "#4a3f2e", "#fff2d4", False, .1, True))
    s += SL(Z_SRED, f'<line x1="{px-176}" y1="{py+10}" x2="{px-150}" y2="{py-620}"'
                    f' stroke="url(#derev)" stroke-width="22"/>'
                    f'<path d="M{px-150},{py-620} q-66,-44 -46,28 q48,26 46,-28 Z"'
                    f' fill="url(#derev)" {o(5)}/>')
    # СВИРЕЛЬ: от губ вниз-вперёд, рукав подпирает её снизу
    hh_ = 560 * .145
    gy_ = py - 560 * .845
    podn = A.ease(A.seg(t, .8, 1.0))
    rx0, ry0 = px + hh_ * .62, gy_ + hh_ * .50
    ug = 34 - 8 * podn
    dl = 210
    rx1 = rx0 + dl * math.cos(math.radians(ug))
    ry1 = ry0 + dl * math.sin(math.radians(ug))
    svir = (f'<g transform="rotate({ug:.1f} {rx0:.0f} {ry0:.0f})">'
            f'<rect x="{rx0:.0f}" y="{ry0-16:.0f}" width="{dl:.0f}" height="32"'
            f' rx="15" fill="url(#derev)" {o(6)}/>')
    for i in range(4):
        svir += (f'<circle cx="{rx0+44+i*42:.0f}" cy="{ry0:.0f}" r="7" fill="{K}"/>')
    svir += (f'<rect x="{rx0-10:.0f}" y="{ry0-20:.0f}" width="26" height="40"'
             f' rx="10" fill="#8a6a44" {o(4)}/>')
    svir += '</g>'
    s += SL(Z_SRED, svir)
    ruk, _ = rukav(px + 110, py - 340, 180, -24 - 10 * podn, t, "#4a3f2e", "#fff2d4", .3, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{rx1-30:.0f}" cy="{ry1+10:.0f}" rx="26" ry="19"'
                    f' fill="#4a3f2e" {o(4)}/>')
    ovcy = ""
    for i in range(6):
        ox = 150 + i * 240 + 18 * A.w(t, 3.0 + i * .3, i * .2)
        oy = 1030 + (i % 3) * 20
        sc = .74 + (i % 3) * .1
        ovcy += (f'<ellipse cx="{ox:.0f}" cy="{oy-90*sc:.0f}" rx="{130*sc:.0f}"'
                 f' ry="{86*sc:.0f}" fill="#efe8d8" {o(6)}/>')
        for j in range(7):
            a = rnd.uniform(0, 6.28)
            ovcy += (f'<circle cx="{ox+math.cos(a)*110*sc:.0f}"'
                     f' cy="{oy-90*sc+math.sin(a)*74*sc:.0f}" r="{26*sc:.0f}"'
                     f' fill="#f8f3e6" opacity=".75"/>')
        shch = 14 * abs(A.w(t, .8, i * .23))
        ovcy += (f'<g transform="rotate({shch:.0f} {ox+110*sc:.0f} {oy-120*sc:.0f})">'
                 f'<ellipse cx="{ox+136*sc:.0f}" cy="{oy-104*sc:.0f}" rx="{52*sc:.0f}"'
                 f' ry="{42*sc:.0f}" fill="#d9cfb8" {o(5)}/>'
                 f'<circle cx="{ox+160*sc:.0f}" cy="{oy-116*sc:.0f}" r="{6*sc:.0f}" fill="{K}"/></g>')
        for j, dx in enumerate((-70, -20, 36, 86)):
            ovcy += (f'<rect x="{ox+dx*sc:.0f}" y="{oy-20*sc:.0f}" width="{22*sc:.0f}"'
                     f' height="{48*sc:.0f}" rx="8" fill="#cdc2a8" {o(4)}/>')
    s += SL(Z_SRED, ovcy)
    beg = ((t * .5) % 1.0)
    dog_x = 300 + beg * 1000
    s += SL(Z_SRED, f'<g transform="translate({dog_x:.0f},{1060-26*abs(A.w(t,.4)):.0f})">'
                    f'<ellipse cx="0" cy="0" rx="72" ry="42" fill="#5a4a38" {o(5)}/>'
                    f'<circle cx="58" cy="-38" r="32" fill="#5a4a38" {o(5)}/>'
                    f'<path d="M82,-58 l22,-32 l-38,8 Z" fill="#5a4a38" {o(4)}/>'
                    f'<path d="M-66,-8 q-52,-50 -22,-90" fill="none" stroke="#5a4a38"'
                    f' stroke-width="15"/><circle cx="72" cy="-42" r="5" fill="{SVET}"/></g>')
    kx, ky = 1180, 1010
    kos = (f'<path d="M{kx-70},{ky} l24,-90 q46,-20 92,0 l24,90 Z" fill="#5a4030" {o(6)}/>')
    s += SL(Z_PERED, kos)
    s += SL(Z_PERED, ugli(kx - 60, ky - 92, 120, t, 6, 349))
    s += SL(Z_PERED, ogon(kx, ky - 100, t, .9, .2, 7))
    s += SL(Z_PERED, dym(kx, ky - 160, t, 5, .3, 320, .36, "#dde3e8", .9))
    s += SL(Z_PERED, teplo(kx, ky - 120, 300, 250, .44))
    s += vinetka(.42)
    return s


def otshelnik_na_kamne_u_peschery(t):
    """Седой отшельник неподвижно сидит на плоском камне у входа в пещеру, а
    вокруг быстро сменяются времена: снег ложится и тает, трава желтеет."""
    rnd = random.Random(2309)
    s = f'<rect width="{W}" height="{H}" fill="#3a3a38"/>'
    s += nebo("sumer", t, True, 353)
    s += SL(Z_DAL, kladka(0, 0, W, 520, 96, "url(#kamen)"))
    sk = (f'<path d="M-20,540 q300,-300 620,-240 q520,60 740,-60 q400,-120 600,60'
          f' l0,780 h-1960 Z" fill="#6b645a" {o(7)}/>')
    for i in range(9):
        sk += (f'<path d="M{80+i*220:.0f},{520+((i%3)*40)} q120,{-40-((i%2)*30)} 220,10"'
               f' fill="none" stroke="#565049" stroke-width="9" opacity=".8"/>')
    s += SL(Z_DAL, sk)
    pesh = (f'<path d="M620,980 q0,-480 340,-480 q340,0 340,480 Z" fill="#18150f" {o(10)}/>')
    pesh += (f'<path d="M660,980 q0,-440 300,-440 q300,0 300,440 Z" fill="#0d0b08"/>')
    for i in range(7):
        pesh += (f'<path d="M{700+i*86:.0f},{560+((i%3)*40)} q40,60 0,120" fill="none"'
                 f' stroke="#2d2822" stroke-width="12" opacity=".8"/>')
    s += SL(Z_DAL, pesh)
    kam = (f'<path d="M520,1010 q0,-120 220,-130 q260,-10 260,130 Z" fill="#8a8275" {o(9)}/>')
    kam += (f'<path d="M540,960 q220,-50 440,0" fill="none" stroke="#6f685c" stroke-width="10"/>')
    s += SL(Z_SRED, kam)
    ox, oy = 760, 880
    ot = (f'<path d="M{ox-200},{oy} q-30,-330 200,-350 q230,20 200,350 Z"'
          f' fill="#4a4336" {o(9)}/>')
    ot += (f'<ellipse cx="{ox}" cy="{oy-404}" rx="96" ry="98" fill="#d9b291" {o(7)}/>')
    bor_k = 1.0 + .08 * A.w(t, 1.1, .1)
    ot += (f'<path d="M{ox-110},{oy-376} q110,{150*bor_k:.0f} 220,0'
           f' q-24,{330*bor_k:.0f} -110,{340*bor_k:.0f}'
           f' q-86,{-10*bor_k:.0f} -110,{-340*bor_k:.0f} Z"'
           f' fill="#e7eef4" opacity=".93" {o(5)}/>')
    for i in range(5):
        ot += (f'<path d="M{ox-70+i*34:.0f},{oy-340} q{4-i*2},180 {-2+i:.0f},300"'
               f' fill="none" stroke="#b9c6d0" stroke-width="5"/>')
    ot += (f'<path d="M{ox-96},{oy-440} q96,-54 192,0 q-22,-70 -96,-72 q-74,2 -96,72 Z"'
           f' fill="#cfd8e0" {o(5)}/>')
    ulyb = 10 * abs(A.w(t, 1.6, .2))
    ot += (f'<path d="M{ox-44},{oy-392} q44,{14+ulyb:.0f} 88,0" fill="none" stroke="{K}"'
           f' stroke-width="7"/>')
    ot += (f'<circle cx="{ox-32}" cy="{oy-418}" r="{3 if A.blink(t,4.0,.1) else 8}" fill="{K}"/>'
           f'<circle cx="{ox+34}" cy="{oy-418}" r="{3 if A.blink(t,4.0,.1) else 8}" fill="{K}"/>')
    s += SL(Z_SRED, ot)
    tay = (abs(A.w(t, 2.2)) ** 2)
    sneg = (f'<path d="M{ox-186},{oy-316} q186,-70 372,0 q-186,36 -372,0 Z" fill="url(#sneg)"'
            f' opacity="{tay:.2f}"/>')
    sneg += (f'<ellipse cx="{ox}" cy="{oy-452}" rx="86" ry="22" fill="url(#sneg)"'
             f' opacity="{tay:.2f}"/>')
    s += SL(Z_SRED, sneg)
    trav = ""
    rost = abs(A.w(t, 2.8, .4))
    for i in range(16):
        gx = 300 + i * 90 + rnd.uniform(-20, 20)
        hh = (60 + rnd.uniform(0, 110)) * rost
        col = ["#6f8c4a", "#9aa14a", "#b79a3c"][int(rost * 2.9) % 3]
        trav += (f'<path d="M{gx:.0f},1050 q{-10+10*A.w(t,2.4,i*.11):.0f},{-hh*.6:.0f}'
                 f' {4:.0f},{-hh:.0f}" fill="none" stroke="{col}" stroke-width="8"/>')
    s += SL(Z_PERED, trav)
    gn = A.ease(A.seg(t, .5, 1.2))
    s += SL(Z_PERED, f'<ellipse cx="1040" cy="1000" rx="{70*gn:.0f}" ry="{36*gn:.0f}"'
                     f' fill="#8a6a3c" opacity="{gn:.2f}" {o(5)}/>')
    for i in range(5):
        s += SL(Z_PERED, f'<path d="M{980+i*30:.0f},{1000-20*gn:.0f} q30,{-16*gn:.0f} 60,0"'
                         f' fill="none" stroke="#6b5230" stroke-width="5" opacity="{gn:.2f}"/>')
    ptx = 1040 + (1 - gn) * 240
    s += SL(Z_PERED, ptica(ptx, 960 - (1 - gn) * 260, t, 1.2, KRAS, .2, "#5b6a78"))
    kx, ky = 1420, 1020
    s += SL(Z_PERED, f'<path d="M{kx-70},{ky} l20,-80 q50,-18 100,0 l20,80 Z"'
                     f' fill="#4e3a2a" {o(6)}/>')
    s += SL(Z_PERED, ugli(kx - 56, ky - 84, 112, t, 6, 359))
    s += SL(Z_PERED, ogon(kx, ky - 90, t, .95, .3, 7))
    s += SL(Z_PERED, dym(kx, ky - 150, t, 5, .3, 340, .34, "#dde3e8", .9))
    s += SL(Z_PERED, teplo(kx, ky - 110, 320, 270, .46))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 367, .34 * tay + .1, .9))
    s += vinetka(.46)
    return s


def kniga_imen_i_ogon_v_ochage(t):
    """Слева толстая книга-календарь на подставке: страницы перелистываются,
    качаются кожаные закладки; справа у очага тесно сидит семья."""
    rnd = random.Random(2411)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("noch", t, False, 373)
    s += SL(Z_DAL, brevna(0, 0, W, 760, 98))
    s += SL(Z_DAL, okno_izby(60, 150, 260, 200, t, svet=False, moroz=.55))
    s += utvar_izby(1500, 230, 380, t, 37)
    s += SL(Z_SRED, polovicy(900))
    pdx, pdy = 480, 940
    pod = (f'<path d="M{pdx-30},{pdy} l-120,0 l150,-120 l150,120 Z" fill="url(#derev)" {o(7)}/>')
    pod += (f'<rect x="{pdx-170:.0f}" y="{pdy-130}" width="340" height="30" rx="8"'
            f' fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_SRED, pod)
    kx, ky = 480, 760
    kn = (f'<path d="M{kx-330},{ky} l0,-420 q330,-70 660,0 l0,420 q-330,64 -660,0 Z"'
          f' fill="#6b2f28" {o(9)}/>')
    kn += (f'<path d="M{kx-300},{ky-24} l0,-370 q300,-60 600,0 l0,370 q-300,56 -600,0 Z"'
           f' fill="url(#list)" {o(6)}/>')
    for i in range(9):
        kn += (f'<path d="M{kx-280},{ky-40-i*36} q280,-52 560,0" fill="none"'
               f' stroke="#e2d8bc" stroke-width="5" opacity=".75"/>')
    for i in range(12):
        kn += (f'<path d="M{kx-200+i*40:.0f},{ky-300} l0,210" stroke="#c0b394"'
               f' stroke-width="4" opacity=".6"/>')
    lis = ((t * .9) % 1.0)
    kn += (f'<path d="M{kx:.0f},{ky-390} q{330*(1-lis*2):.0f},{-40+120*lis:.0f}'
           f' {300*(1-lis*1.9):.0f},{320+40*lis:.0f} q{-150*(1-lis):.0f},{-30:.0f}'
           f' {-300*(1-lis*1.9):.0f},{-320-40*lis:.0f} Z" fill="#fbf7ea" opacity=".95" {o(5)}/>')
    kn += (f'<rect x="{kx-14:.0f}" y="{ky-410}" width="28" height="420" fill="#4a1f1a"'
           f' opacity=".9"/>')
    s += SL(Z_SRED, kn)
    zak = ""
    for i, (dx, col) in enumerate(((-230, "#b8323a"), (-60, "#3f5c7a"), (130, "#8a6a30"),
                                   (280, "#4e6b34"))):
        kach = 6.0 * A.w(t, 2.2 + i * .3, i * .21)
        zak += (f'<g transform="rotate({kach:.2f} {kx+dx:.0f} {ky-400:.0f})">'
                f'<path d="M{kx+dx:.0f},{ky-400} l44,0 l0,{200+i*26} l-22,-40 l-22,40 Z"'
                f' fill="{col}" {o(5)}/></g>')
    s += SL(Z_SRED, zak)
    s += SL(Z_SRED, teplo(kx, ky - 200, 400, 340, .32 + .1 * abs(A.w(t, 2.0))))
    ocx, ocy = 1420, 940
    och = kladka(ocx - 330, ocy - 330, 660, 340, 76, "url(#pech)")
    och += (f'<path d="M{ocx-220:.0f},{ocy} l0,-180 q220,-130 440,0 l0,180 Z"'
            f' fill="#1a120c" {o(8)}/>')
    och += (f'<rect x="{ocx-350:.0f}" y="{ocy-360}" width="700" height="46" rx="10"'
            f' fill="{PECH2}" {o(7)}/>')
    s += SL(Z_SRED, och)
    s += SL(Z_SRED, ugli(ocx - 170, ocy - 40, 340, t, 10, 379))
    s += SL(Z_SRED, ogon(ocx - 60, ocy - 50, t, 1.3, .1, 8))
    s += SL(Z_SRED, ogon(ocx + 90, ocy - 46, t, 1.0, .5, 6))
    s += SL(Z_SRED, teplo(ocx, ocy - 130, 520, 420, .56 + .14 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, iskra_let(t, ocx, ocy - 120, 12, 383, 400, .5))
    sem = ""
    for i, (dx, hh, plt) in enumerate(((-300, 400, True), (-120, 300, False),
                                       (190, 280, False), (340, 420, True))):
        sem += figura(ocx + dx, ocy + 60, hh, t, "#231d2a", "#ffd98a", plt,
                      ph=i * .31, boroda=(i == 2))
    s += SL(Z_PERED, sem)
    podn = A.over(A.seg(t, 1.4, 1.0))
    ruk, (fx, fy) = rukav(ocx + 340, ocy - 300, 170, -40 - 56 * podn, t, "#5b2b32", "#ffd98a", .2, 4.0)
    s += SL(Z_PERED, ruk)
    s += SL(Z_PERED, f'<ellipse cx="{fx:.0f}" cy="{fy:.0f}" rx="24" ry="18" fill="#dfb391" {o(4)}/>')
    s += SL(Z_PERED, f'<path d="M{fx:.0f},{fy-10:.0f} l6,-80" stroke="#dfb391"'
                     f' stroke-width="20" stroke-linecap="round"/>')
    s += SL(Z_PERED, kot(900, 1030, t, .8, "#3b3430"))
    s += vinetka(.46)
    return s


def pyat_podkov_nad_dveryu(t):
    """Тяжёлая дощатая дверь избы изнутри во весь кадр: молоток вбивает гвозди,
    пять подков повисают над притолокой и качаются в свете лучины.

    Поверх этого плана идёт памятка: пять карточек шириной 1440 px по центру,
    от 300 до 1000 px по высоте. Поэтому дверь ДОЛЖНА ЧИТАТЬСЯ ПО КРАЯМ —
    притолока с резьбой и подковами сверху, косяки, фонарь, пучок трав и кот
    слева, лавка с веником справа, порог с половиком внизу. Прежде три четверти
    кадра занимала голая доска (осмотр 14.11)."""
    rnd = random.Random(2503)
    s = f'<rect width="{W}" height="{H}" fill="#241c15"/>'
    s += nebo("noch", t, False, 389)
    s += SL(Z_DAL, brevna(0, 0, 250, 1080, 100))
    s += SL(Z_DAL, brevna(1670, 0, 250, 1080, 100))
    s += SL(Z_DAL, f'<rect x="236" y="0" width="1448" height="1080" fill="#160f0a"/>')
    # ДВЕРЬ с филёнками, коваными петлями и ручкой-скобой
    dv = doski(286, 340, 1348, 740, 142, True, "dosk")
    dv += (f'<rect x="286" y="340" width="1348" height="740" fill="none" {o(10)}/>')
    for yy in (330, 700, 1010):
        dv += (f'<rect x="306" y="{yy}" width="1308" height="52" rx="10"'
               f' fill="{DOSKA2}" {o(7)}/>')
        for i in range(10):
            dv += (f'<circle cx="{356+i*140:.0f}" cy="{yy+26}" r="13" fill="{ZHELEZ}" {o(4)}/>')
    for sgn, px in ((-1, 300), (1, 1620)):     # кованые петли по краям двери
        for yy in (410, 900):
            dv += (f'<path d="M{px:.0f},{yy} h{sgn*130:.0f} l{sgn*26:.0f},22'
                   f' l{-sgn*26:.0f},22 h{-sgn*130:.0f} Z" fill="{ZHELEZ}" {o(5)}/>')
            dv += (f'<circle cx="{px+sgn*30:.0f}" cy="{yy+22}" r="10"'
                   f' fill="#cfd6dc" {o(3)}/>')
    dv += (f'<rect x="330" y="648" width="1260" height="40" rx="14" fill="#5d6168" {o(7)}/>')
    for i in range(2):                         # скобы засова
        dv += (f'<rect x="{430+i*940:.0f}" y="628" width="54" height="82" rx="14"'
               f' fill="none" stroke="{ZHELEZ}" stroke-width="16"/>')
    dv += (f'<circle cx="960" cy="860" r="96" fill="#5d6168" {o(8)}/>')
    dv += (f'<circle cx="960" cy="860" r="62" fill="url(#derev)" {o(6)}/>')
    for i in range(8):                         # кованая розетка лучами
        a_ = i * .785
        dv += (f'<path d="M{960+math.cos(a_)*62:.0f},{860+math.sin(a_)*62:.0f}'
               f' l{math.cos(a_)*40:.0f},{math.sin(a_)*40:.0f}" stroke="#5d6168"'
               f' stroke-width="14" stroke-linecap="round"/>')
    dv += (f'<circle cx="960" cy="860" r="24" fill="{ZHELEZ}" {o(5)}/>')
    dv += (f'<rect x="1440" y="640" width="150" height="48" rx="22" fill="url(#zhel)" {o(6)}/>')
    dv += (f'<path d="M1430,560 q90,-40 170,0 l0,40 q-80,-30 -170,0 Z" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, dv)
    # КОСЯКИ и НАЛИЧНИК: резьба, зубцы, полотенца по краям
    kos = (f'<rect x="230" y="206" width="78" height="874" fill="url(#derev)" {o(9)}/>'
           f'<rect x="1612" y="206" width="78" height="874" fill="url(#derev)" {o(9)}/>')
    for i in range(9):
        for px in (236, 1618):
            kos += (f'<path d="M{px:.0f},{290+i*88:.0f} q33,22 66,0 q-33,26 -66,0 Z"'
                    f' fill="{MED}" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, kos)
    pri = kladka(220, 86, 1480, 200, 86, "url(#derev)")
    pri += (f'<rect x="188" y="60" width="1544" height="52" rx="12" fill="{DOSKA2}" {o(9)}/>')
    pri += (f'<rect x="188" y="276" width="1544" height="44" rx="10" fill="{DOSKA2}" {o(8)}/>')
    for i in range(16):                        # зубчатая резьба по наличнику
        pri += (f'<path d="M{200+i*96:.0f},320 l44,0 l-22,34 Z" fill="{DOSKA2}" {o(3)}/>')
    for i in range(12):
        pri += (f'<path d="M{250+i*122:.0f},128 q24,56 0,112" fill="none" stroke="#5a3a22"'
                f' stroke-width="7" opacity=".7"/>')
    s += SL(Z_SRED, pri)
    # ПЯТЬ ПОДКОВ: кольцо с вырезанной серединой, разрыв внизу, шипы, гвозди
    for i in range(5):
        px = 300 + i * 330
        py = 248
        vb = A.out(A.seg(t, .3 + i * .55, .45))
        if vb < .02:
            continue
        kach = 7.0 * A.w(t, 1.9 + i * .2, i * .17) * vb
        R, tol = 84.0, 46.0                    # радиус дуги и толщина железа
        pk = f'<g transform="rotate({kach:.2f} {px:.0f} {py-70:.0f})">'
        yy = py + (1 - vb) * -60
        d = (f'M{px-R-tol/2:.0f},{yy+R*.46:.0f}'
             f' A{R+tol/2:.0f},{R+tol/2:.0f} 0 1 1 {px+R+tol/2:.0f},{yy+R*.46:.0f}'
             f' l{-tol:.0f},0'
             f' A{R-tol/2:.0f},{R-tol/2:.0f} 0 1 0 {px-R+tol/2:.0f},{yy+R*.46:.0f} Z')
        pk += f'<path d="{d}" fill="#6e757e" {o(8)}/>'
        pk += (f'<path d="{d}" fill="none" stroke="#c6d2dc" stroke-width="5"'
               f' opacity=".45"/>')
        for sgn in (-1, 1):                    # шипы на концах
            pk += (f'<rect x="{px+sgn*R-tol/2-8:.0f}" y="{yy+R*.46:.0f}"'
                   f' width="{tol+16:.0f}" height="38" rx="10" fill="#4a5059" {o(5)}/>')
            pk += (f'<rect x="{px+sgn*R-10:.0f}" y="{yy+R*.46+28:.0f}"'
                   f' width="20" height="22" rx="6" fill="#30353c" {o(4)}/>')
        for j in range(6):                     # гвозди по дуге
            a = math.radians(206 + j * 26)
            pk += (f'<circle cx="{px+math.cos(a)*R:.0f}" cy="{yy+R*.46+math.sin(a)*R:.0f}"'
                   f' r="7" fill="#2b2b30"/>')
        bl = .3 + .3 * (0.5 + 0.5 * A.w(t, 3.6, i * .2))
        pk += (f'<path d="M{px-R*.72:.0f},{yy-R*.30:.0f}'
               f' a{R*.78:.0f},{R*.78:.0f} 0 0 1 {R*.70:.0f},{-R*.34:.0f}"'
               f' fill="none" stroke="#eaf4ff" stroke-width="9"'
               f' opacity="{bl:.2f}"/>')
        pk += (f'<circle cx="{px:.0f}" cy="{yy-R*.52:.0f}" r="9" fill="{K}"/>')
        pk += '</g>'
        s += SL(Z_SRED, pk)
        s += SL(Z_SRED, teplo(px, 286, 190, 150, .18 + .1 * vb))
    mol_i = min(4, int(t / .55))
    mx = 300 + mol_i * 330
    udar = abs(A.w(t, .55, .0))
    mol = (f'<g transform="rotate({-50+34*udar:.0f} {mx+120:.0f} {330:.0f})">'
           f'<rect x="{mx+100:.0f}" y="330" width="34" height="230" rx="12"'
           f' fill="url(#derev)" {o(6)}/>'
           f'<rect x="{mx+60:.0f}" y="296" width="120" height="60" rx="12"'
           f' fill="url(#zhel)" {o(7)}/>'
           f'<path d="M{mx+60:.0f},306 l120,0" stroke="#dfe8f2" stroke-width="6" opacity=".6"/></g>')
    s += SL(Z_SRED, mol)
    ruk, (rx2, ry2) = rukav(mx + 300, 520, 200, 190 - 24 * udar, t, "#5b2b32", "#ffd98a", .1, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{rx2:.0f}" cy="{ry2:.0f}" rx="28" ry="20" fill="#5b2b32" {o(4)}/>')
    # ЛЕВЫЙ КРАЙ: фонарь с живым огнём, пучок трав, валенки, кот
    fx_, fy_ = 120, 430
    fon = (f'<path d="M{fx_:.0f},230 q-6,60 0,96" fill="none" stroke="{ZHELEZ}"'
           f' stroke-width="8"/>')
    fon += (f'<path d="M{fx_-62:.0f},{fy_-200:.0f} h124 l-18,-44 h-88 Z"'
            f' fill="{ZHELEZ}" {o(6)}/>')
    fon += (f'<path d="M{fx_-54:.0f},{fy_-200:.0f} h108 l-10,186 h-88 Z"'
            f' fill="url(#stekl)" opacity=".7" {o(6)}/>')
    fon += (f'<rect x="{fx_-58:.0f}" y="{fy_-20:.0f}" width="116" height="26" rx="8"'
            f' fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, fon)
    s += SL(Z_SRED, ogon(fx_, fy_ - 40, t, .78, .2, 5))
    s += SL(Z_SRED, teplo(fx_, fy_ - 70, 400, 360, .5 + .12 * abs(A.w(t, 1.4))))
    puch = 5 * A.w(t, 2.6, .3)                 # пучок сухих трав на гвозде
    s += SL(Z_SRED, f'<g transform="rotate({puch:.1f} 148 600)">'
                    f'<circle cx="148" cy="600" r="9" fill="{ZHELEZ}" {o(3)}/>'
                    + "".join(
                        f'<path d="M148,606 q{-30+i*12:.0f},90 {-46+i*20:.0f},196"'
                        f' fill="none" stroke="{"#8a7a46" if i % 2 else "#6f6236"}"'
                        f' stroke-width="{9-i%3*2}" stroke-linecap="round"/>'
                        for i in range(7))
                    + f'<path d="M110,642 q38,22 76,0" fill="none" stroke="{TKAN}"'
                      f' stroke-width="10"/></g>')
    s += SL(Z_SRED, kot(150, 1040, t, 1.1, "#3b3430"))
    for i, (vx_, sc) in enumerate(((96, .62), (178, .60))):
        s += SL(Z_PERED, f'<g transform="translate(0,{-4*i})">'
                         f'<rect x="{vx_-38:.0f}" y="{1070-176*sc*1.6:.0f}"'
                         f' width="{76:.0f}" height="{176*sc*1.3:.0f}" rx="22"'
                         f' fill="#c4b091" {o(6)}/>'
                         f'<path d="M{vx_-40:.0f},{1070-40:.0f} h74 q34,2 34,22'
                         f' q0,18 -26,18 h-82 Z" fill="#c4b091" {o(6)}/>'
                         f'<ellipse cx="{vx_:.0f}" cy="{1070-176*sc*1.6:.0f}" rx="38"'
                         f' ry="12" fill="#a0917a" {o(4)}/></g>')
    # ПРАВЫЙ КРАЙ: лавка с веником и крынкой
    s += SL(Z_PERED, lavka(1700, 900, 210))
    s += SL(Z_PERED, f'<rect x="1790" y="700" width="20" height="200" rx="8"'
                     f' fill="url(#derev)" {o(5)}/>')
    ven = 4 * A.w(t, 3.0, .1)
    s += SL(Z_PERED, f'<g transform="rotate({ven:.1f} 1800 700)">'
                     + "".join(
                        f'<path d="M1800,700 q{-40+i*16:.0f},-70 {-62+i*26:.0f},-136"'
                        f' fill="none" stroke="#9a8450" stroke-width="7"'
                        f' stroke-linecap="round"/>' for i in range(6))
                     + '</g>')
    s += SL(Z_PERED, krynka(1760, 898, 1.0))
    # НИЗ: порог и половик
    s += SL(Z_PERED, f'<rect x="236" y="1016" width="1448" height="64" rx="10"'
                     f' fill="{DOSKA2}" {o(8)}/>')
    s += SL(Z_PERED, f'<path d="M520,1070 q440,-44 880,-6 l0,20 h-880 Z"'
                     f' fill="{TKAN}" opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, luchina(330, 760, t, 1.5, .2))
    s += SL(Z_SRED, teplo(330, 650, 460, 400, .38 + .12 * abs(A.w(t, 1.3))))
    tenb = ""
    hod = 70 * A.w(t, 4.6, .1)
    tenb += (f'<path d="M{430+hod:.0f},1080 q-40,-380 70,-480 q90,-86 170,8'
             f' q70,116 36,472 Z" fill="#120d0a" opacity=".20"/>')
    s += SL(Z_SRED, tenb)
    s += SL(Z_PERED, ramka_pp("levo", "#0a0806", .4))
    s += vinetka(.5)
    return s


def valenok_nad_porogom(t):
    """Высокий деревянный порог на пол-кадра, над ним занесён валенок с
    галошей. Валенок собран ДВУМЯ ТЕЛАМИ: прямое толстое голенище с валиком
    сверху и отдельная ступня с тупым носком вперёд. Прежний сплошной конус
    читался мешком и колоколом (осмотр 14.11)."""
    rnd = random.Random(2609)
    s = f'<rect width="{W}" height="{H}" fill="#1f1912"/>'
    s += nebo("sumer", t, False, 397)
    s += SL(Z_DAL, brevna(0, 0, 420, 1080, 98))
    s += SL(Z_DAL, brevna(1500, 0, 420, 1080, 98))
    s += SL(Z_DAL, f'<rect x="400" y="0" width="1120" height="1080" fill="url(#nsumer)"'
                   f' opacity=".9"/>')
    s += SL(Z_DAL, ulica_dal(420, 700, 1100, t, False, 401))
    s += SL(Z_DAL, gryaz_polosa(740, 160, "#3a322a"))
    pr = (f'<rect x="380" y="730" width="1160" height="210" rx="20" fill="url(#dosk)" {o(10)}/>')
    pr += (f'<rect x="380" y="700" width="1160" height="46" rx="14" fill="{DOSKA2}" {o(8)}/>')
    for i in range(9):
        pr += (f'<path d="M{430+i*130:.0f},760 q22,80 0,160" fill="none" stroke="#5a3a22"'
               f' stroke-width="8" opacity=".65"/>')
    pr += (f'<rect x="380" y="930" width="1160" height="40" rx="12" fill="#5a3a22" {o(7)}/>')
    s += SL(Z_SRED, pr)
    s += SL(Z_SRED, f'<rect x="360" y="0" width="80" height="760" rx="10"'
                    f' fill="url(#derev)" {o(8)}/>'
                    f'<rect x="1480" y="0" width="80" height="760" rx="10"'
                    f' fill="url(#derev)" {o(8)}/>')
    sm = A.ease(A.seg(t, 1.4, .8))
    pol = (f'<path d="M420,1010 q{280-60*sm:.0f},-50 {560-40*sm:.0f},-6'
           f' q{280:.0f},44 {520+60*sm:.0f},10 l0,76 h-1100 Z" fill="{TKAN}"'
           f' opacity=".88" {o(6)}/>')
    for i in range(7):
        pol += (f'<path d="M{450+i*160:.0f},1016 q40,{20-8*sm:.0f} 80,0" fill="none"'
                f' stroke="{RUSH}" stroke-width="7" opacity=".7"/>')
    s += SL(Z_SRED, pol)
    # ВАЛЕНОК: прямое голенище + ОТДЕЛЬНАЯ ступня с тупым носком вперёд
    vis = A.ease(A.seg(t, .3, .7)) - A.ease(A.seg(t, 1.5, .8))
    vx, vy = 840 - vis * 40, 744 - vis * 120   # vy — низ подошвы
    vw, vh = 96, 286                           # полуширина голенища, высота
    fl, fh = 268, 152                          # длина ступни и её высота
    val = f'<g transform="rotate({-7+7*vis:.1f} {vx:.0f} {vy:.0f})">'
    val += ten(vx + 70, 968 + vis * 14, 190 - vis * 48, 26, .5)
    # ступня: пятка под голенищем, тупой круглый носок вперёд
    val += (f'<path d="M{vx-vw:.0f},{vy-fh:.0f} h{fl*.52:.0f}'
            f' q{fl*.42:.0f},10 {fl*.46:.0f},{fh*.52:.0f}'
            f' q{fl*.02:.0f},{fh*.40:.0f} {-fl*.26:.0f},{fh*.46:.0f}'
            f' h{-fl*.72:.0f} q{-fl*.12:.0f},{-fh*.20:.0f} {-fl*.02:.0f},{-fh*.98:.0f} Z"'
            f' fill="#c4b091" {o(10)}/>')
    # голенище: прямой толстый рукав, валик сверху
    val += (f'<rect x="{vx-vw:.0f}" y="{vy-fh-vh+30:.0f}" width="{vw*2:.0f}"'
            f' height="{vh:.0f}" rx="{vw*.24:.0f}" fill="#c4b091" {o(10)}/>')
    val += (f'<ellipse cx="{vx:.0f}" cy="{vy-fh-vh+30:.0f}" rx="{vw*1.06:.0f}" ry="30"'
            f' fill="#a0917a" {o(7)}/>')
    val += (f'<ellipse cx="{vx:.0f}" cy="{vy-fh-vh+38:.0f}" rx="{vw*.76:.0f}" ry="19"'
            f' fill="#7d7160" opacity=".85"/>')
    for i in range(4):                         # войлок: короткие штрихи
        val += (f'<path d="M{vx-vw*.62+i*vw*.42:.0f},{vy-fh-vh+104:.0f}'
                f' q8,{vh*.16:.0f} 2,{vh*.32:.0f}" fill="none" stroke="#ded0b4"'
                f' stroke-width="9" opacity=".55"/>')
    val += (f'<path d="M{vx-vw:.0f},{vy-fh-6:.0f} h{vw*2:.0f}" stroke="#9c8c72"'
            f' stroke-width="10" opacity=".75"/>')
    # ГАЛОША: тёмная, обнимает ступню целиком и заходит на носок
    val += (f'<path d="M{vx-vw*1.14:.0f},{vy-fh*.74:.0f}'
            f' q-14,{fh*.62:.0f} {vw*.52:.0f},{fh*.74:.0f}'
            f' h{fl*.50:.0f} q{fl*.34:.0f},-6 {fl*.22:.0f},{-fh*.56:.0f}'
            f' q{-fl*.10:.0f},{-fh*.30:.0f} {-fl*.52:.0f},{-fh*.26:.0f}'
            f' q{-fl*.30:.0f},{fh*.04:.0f} {-fl*.36:.0f},{fh*.08:.0f} Z"'
            f' fill="#26282b" {o(8)}/>')
    val += (f'<path d="M{vx-vw*1.12:.0f},{vy-fh*.70:.0f} q{fl*.30:.0f},{-fh*.14:.0f}'
            f' {fl*.92:.0f},{-fh*.04:.0f}" fill="none" stroke="#dfe8ef"'
            f' stroke-width="10" opacity=".85"/>')
    val += (f'<path d="M{vx-vw*.78:.0f},{vy-fh*.30:.0f} q{fl*.34:.0f},26'
            f' {fl*.80:.0f},0" fill="none" stroke="#9fb4c2" stroke-width="7"'
            f' opacity="{.35+.3*abs(A.w(t,2.4)):.2f}"/>')
    val += (f'<ellipse cx="{vx+fl*.72:.0f}" cy="{vy-fh*.34:.0f}" rx="26" ry="16"'
            f' fill="#4a4f55" opacity=".7"/>')
    val += '</g>'
    s += SL(Z_SRED, val)
    s += SL(Z_SRED, figura(1240, 1070, 540, t, "#231d2b", "#ffd98a", True, .2))
    ruk, (hx, hy) = rukav(1150, 640, 190, 208, t, "#5b2b32", "#ffd98a", .3, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="30" ry="22" fill="#5b2b32" {o(4)}/>')
    s += SL(Z_SRED, lampa(560, 420, t, .9, False))
    s += SL(Z_SRED, teplo(560, 340, 460, 400, .42 + .12 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, podkova(960, 180, 1.0, t))
    s += tuman(t, 980, .5, "#d9e4f0")
    s += SL(Z_PERED, f'<path d="M-20,1080 q380,-70 820,-24 l0,120 h-840 Z"'
                     f' fill="#110d0a" opacity=".9"/>')
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 409, .4, .8))
    s += vinetka(.48)
    return s


def hodiki_i_rannyaya_temnota(t):
    """Окно избы с переплётом на пол-кадра: на подоконнике ходики-кукушка и
    недоеденный обед, а за стеклом ноябрьские сумерки гаснут до темноты."""
    rnd = random.Random(2707)
    s = f'<rect width="{W}" height="{H}" fill="{BREVNO2}"/>'
    s += nebo("sumer", t, False, 419)
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 104))
    s += utvar_izby(60, 240, 400, t, 41)
    ox, oy, ow, oh = 500, 150, 920, 600
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    gas = A.ease(A.seg(t, .4, 2.4))
    vid = f'<clipPath id="okn27"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="url(#nsumer)"/>'
    za = f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#nsumer)"/>'
    za += (f'<path d="M{ox},{oy+oh*.62:.0f} q{ow*.25:.0f},-80 {ow*.5:.0f},-20'
           f' q{ow*.25:.0f},60 {ow*.5:.0f},-30 l0,{oh*.5:.0f} h{-ow:.0f} Z"'
           f' fill="#3b4254" opacity=".95"/>')
    for i in range(4):
        bx = ox + 90 + i * 220
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.56:.0f}" width="120" height="120"'
               f' fill="#2f3646" opacity=".95"/>')
        za += (f'<path d="M{bx-16:.0f},{oy+oh*.56:.0f} l76,-60 l76,60 Z"'
               f' fill="#262c3a" opacity=".95"/>')
        if i % 2 == 0:
            za += (f'<rect x="{bx+36:.0f}" y="{oy+oh*.62:.0f}" width="44" height="44"'
                   f' fill="{SVET}" opacity="{.35+.6*gas:.2f}"/>')
            za += teplo(bx + 58, oy + oh * .64, 140, 120, .3 + .4 * gas)
    for i in range(5):
        za += (f'<path d="M{ox+40+i*190:.0f},{oy+oh*.42:.0f} l-34,0 l34,-90 l34,90 Z"'
               f' fill="#2a3348" opacity=".9"/>')
    za += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#0d1018"'
           f' opacity="{.06+.38*gas:.2f}"/>')
    vid += f'<g clip-path="url(#okn27)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    ob = (f'<rect x="{ox-40}" y="{oy-40}" width="{ow+80}" height="{oh+80}" rx="10"'
          f' fill="none" stroke="url(#derev)" stroke-width="80"/>')
    ob += (f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}" y2="{oy+oh}"'
           f' stroke="url(#derev)" stroke-width="34"/>'
           f'<line x1="{ox}" y1="{oy+oh/2:.0f}" x2="{ox+ow}" y2="{oy+oh/2:.0f}"'
           f' stroke="url(#derev)" stroke-width="34"/>')
    for i in range(4):
        ob += (f'<line x1="{ox+ow*.25+i*ow*.166:.0f}" y1="{oy}"'
               f' x2="{ox+ow*.25+i*ow*.166:.0f}" y2="{oy+oh}" stroke="url(#derev)"'
               f' stroke-width="12" opacity=".8"/>')
    ob += (f'<path d="M{ox+20},{oy+40} l{ow*.42:.0f},{oh*.5:.0f}" stroke="#ffffff"'
           f' stroke-width="14" opacity="{.22-.14*gas:.2f}"/>')
    ob += (f'<path d="M{put}" fill="none" {o(10)}/>')
    ob += (f'<path d="M{ox-90},{oy-50} h{ow+180:.0f} l-50,-56 h{-ow-80:.0f} Z"'
           f' fill="url(#derev)" {o(7)}/>')
    for i in range(8):
        ob += (f'<circle cx="{ox-40+i*(ow+80)/7:.0f}" cy="{oy-74}" r="12" fill="{MED}"'
               f' opacity=".85" {o(2)}/>')
    vid += ob
    s += SL(Z_SRED, vid)
    s += SL(Z_SRED, f'<rect x="420" y="770" width="1080" height="66" rx="12"'
                    f' fill="url(#dosk)" {o(9)}/>')
    s += SL(Z_SRED, hodiki(680, 650, t, 1.5))
    s += SL(Z_SRED, f'<path d="M620,560 q60,-54 120,0 q-60,-16 -120,0 Z" fill="#6b2f28" {o(5)}/>')
    s += SL(Z_SRED, ptica(690, 568, t, .7, "#a8641e", .2, "#7a4a18"))
    ob_ = (f'<path d="M1060,770 q110,86 220,0 q-110,30 -220,0 Z" fill="url(#glina)" {o(7)}/>')
    ob_ += (f'<ellipse cx="1170" cy="760" rx="104" ry="26" fill="#9c6a3c" {o(5)}/>')
    ob_ += kartoshka(1170, 744, t, 6, 421, .9)
    ob_ += (f'<rect x="1290" y="736" width="140" height="18" rx="8" fill="url(#zhel)" {o(4)}/>')
    ob_ += karavay(1390, 770, .7, True)
    s += SL(Z_SRED, ob_)
    s += SL(Z_SRED, par(1170, 720, t, 4, .40 - .2 * gas, 160, .4, .8))
    sv_on = A.ease(A.seg(t, 1.8, .8))
    if sv_on > .02:
        s += SL(Z_SRED, svecha(900, 700, t, .2, 1.5 * sv_on + .2, 110))
        s += SL(Z_SRED, teplo(900, 640, 460 * sv_on, 400 * sv_on, .54 * sv_on))
    s += SL(Z_SRED, figura(1640, 1060, 520, t, "#241e2b", "#ffd98a", True, .3))
    s += SL(Z_PERED, zanaveska(460, 90, 480, 180, TKAN, t, 1))
    s += SL(Z_PERED, zanaveska(1460, 90, 480, 180, TKAN, t, -1))
    s += SL(Z_PERED, krynka(240, 1030, 1.4))
    s += vinetka(.46)
    return s


def chernaya_derevenskaya_ulica(t):
    """Чёрная ноябрьская улица без снега: мужик с горящей лучиной идёт вдоль
    заборов, крошечный круг света дрожит, он натыкается на бочку и свинью."""
    rnd = random.Random(2803)
    s = f'<rect width="{W}" height="{H}" fill="#0b0d14"/>'
    s += nebo("noch", t, True, 431)
    s += SL(Z_DAL, f'<rect y="420" width="{W}" height="{H-420}" fill="#0a0b0f"/>')
    s += SL(Z_DAL, ulica_dal(40, 560, 1840, t, False, 433))
    s += SL(Z_DAL, f'<rect y="540" width="{W}" height="560" fill="#07080c" opacity=".88"/>')
    zab = ""
    for i in range(22):
        zx = -40 + i * 92
        zh = 230 + ((i * 53) % 60)
        zab += (f'<rect x="{zx:.0f}" y="{700-zh:.0f}" width="62" height="{zh+40:.0f}"'
                f' rx="8" fill="#15161d" {o(4)}/>')
    zab += (f'<path d="M-40,620 h1960" stroke="#1d1f28" stroke-width="18"/>')
    s += SL(Z_DAL, zab)
    s += SL(Z_DAL, goloe_derevo(1700, 740, 520, t, 439, 7, "#191b22"))
    hod = A.ease(A.seg(t, .3, 5.4))
    mx = 420 + hod * 900
    drozh = 26 * A.w(t, .33, .1) + 12 * A.w(t, 1.7, .4)
    s += SL(Z_SRED, gryaz_polosa(700, 380, "#0e0f14"))
    krug = (f'<ellipse cx="{mx+120+drozh:.0f}" cy="{880}" rx="300" ry="150"'
            f' fill="url(#teplo)" opacity="{.42+.1*abs(A.w(t,1.2)):.2f}"/>')
    krug += (f'<ellipse cx="{mx+120+drozh:.0f}" cy="{880}" rx="170" ry="86"'
             f' fill="{SVET}" opacity=".18"/>')
    s += SL(Z_SRED, krug)
    boch_x = 1180
    toln = A.ease(A.seg(t, 2.6, .5))
    boch = (f'<g transform="rotate({-14*toln:.1f} {boch_x:.0f} 940)">'
            f'<path d="M{boch_x-130:.0f},940 l16,-280 q114,-34 228,0 l16,280 Z"'
            f' fill="#2a2320" {o(7)}/>')
    for yy in (720, 820, 900):
        boch += (f'<path d="M{boch_x-128:.0f},{yy} q128,26 262,0" fill="none"'
                 f' stroke="#3d3a38" stroke-width="13"/>')
    boch += (f'<ellipse cx="{boch_x+4:.0f}" cy="662" rx="116" ry="30" fill="#332b26" {o(5)}/></g>')
    s += SL(Z_SRED, boch)
    s += SL(Z_SRED, figura(mx, 1000, 520, t, "#12121a", "#ffd98a", False, .2, True, 1.0, True, 2.0))
    s += SL(Z_SRED, para_izo_rta(mx + 40, 1000 - 440, t, .2, 1.2, .4))
    ruk, (lx, ly) = rukav(mx + 110, 1000 - 320, 190, -22 + 14 * A.w(t, 1.1), t, "#1a1a24", "#ffd98a", .1, 8.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, luchina(lx, ly + 30, t, 1.5, .1))
    s += SL(Z_SRED, teplo(lx, ly - 70, 420, 360, .52 + .14 * abs(A.w(t, 1.1))))
    s += SL(Z_SRED, blik(lx, ly - 60, t, .45, "#a8c8ff", SVET, .34))
    vsk = A.out(A.seg(t, 3.4, .5))
    svx, svy = 700, 1010 - vsk * 70
    svin = (f'<g transform="rotate({-10*vsk:.1f} {svx:.0f} {svy:.0f})">'
            f'<ellipse cx="{svx:.0f}" cy="{svy:.0f}" rx="200" ry="118" fill="#3a2b2a" {o(7)}/>'
            f'<circle cx="{svx+180:.0f}" cy="{svy-60:.0f}" r="76" fill="#3a2b2a" {o(6)}/>'
            f'<ellipse cx="{svx+250:.0f}" cy="{svy-46:.0f}" rx="40" ry="30" fill="#4e3b39" {o(5)}/>'
            f'<circle cx="{svx+238:.0f}" cy="{svy-50:.0f}" r="7" fill="{K}"/>'
            f'<circle cx="{svx+262:.0f}" cy="{svy-50:.0f}" r="7" fill="{K}"/>'
            f'<path d="M{svx+160:.0f},{svy-124:.0f} l-10,-56 l56,26 Z" fill="#3a2b2a" {o(4)}/>'
            f'<circle cx="{svx+198:.0f}" cy="{svy-96:.0f}" r="{4 if A.blink(t,2.4) else 10}" fill="{K}"/>')
    for i, dx in enumerate((-130, -40, 70, 150)):
        svin += (f'<rect x="{svx+dx:.0f}" y="{svy+94:.0f}" width="40"'
                 f' height="{70+16*vsk:.0f}" rx="12" fill="#322524" {o(4)}/>')
    svin += (f'<path d="M{svx-200:.0f},{svy-20:.0f} q-60,-30 -30,-70" fill="none"'
             f' stroke="#3a2b2a" stroke-width="14"/></g>')
    s += SL(Z_SRED, svin)
    s += SL(Z_PERED, f'<path d="M-20,1080 q440,-110 960,-40 l0,150 h-980 Z"'
                     f' fill="#07080c" opacity=".95"/>')
    s += SL(Z_PERED, pleten(1320, 1070, 640, 220, 7))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 443, .3, .8))
    s += vinetka(.56)
    return s


def ledyanaya_koleya_u_vorot(t):
    """Ворота и глубокая тележная колея: грязь затягивается блестящим льдом,
    нога едет, лучина летит дугой, мужик садится в колею.

    Колея — ДВЕ борозды в перспективе с продольным ледяным блеском и
    трещинами, а не ряд белых блинов поперёк дороги; летящая лучина — щепка с
    огоньком и хвостом искр, а не светлое пятно в небе (осмотр 14.11)."""
    rnd = random.Random(2909)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 449)
    s += oblaka(t, 140, 3, 457, .24, "#b2bfd0", 8.0)
    s += SL(Z_DAL, ulica_dal(1180, 640, 760, t, False, 461))
    s += SL(Z_DAL, gryaz_polosa(660, 420, "#352d26"))
    vor = ""
    for xx in (120, 820):
        vor += (f'<rect x="{xx:.0f}" y="200" width="80" height="560" rx="10"'
                f' fill="url(#derev)" {o(8)}/>')
        for i in range(5):
            vor += (f'<path d="M{xx+14:.0f},{260+i*100} q52,24 52,0" fill="none"'
                    f' stroke="#5a3a22" stroke-width="7" opacity=".7"/>')
    vor += (f'<path d="M80,200 h820 l-40,-70 h-740 Z" fill="{DOSKA2}" {o(8)}/>')
    vor += (f'<path d="M100,192 h780 l-30,-56 h-720 Z" fill="url(#sneg)" opacity=".75" {o(4)}/>')
    stv = 11 * A.w(t, 3.2, .1)
    vor += (f'<g transform="rotate({stv:.2f} 200 240)">')
    for i in range(6):
        vor += (f'<rect x="{212+i*98:.0f}" y="250" width="80" height="480" rx="8"'
                f' fill="url(#dosk)" {o(6)}/>')
    vor += (f'<path d="M212,330 l580,140" stroke="{DOSKA2}" stroke-width="24"/>'
            f'<path d="M212,620 l580,-140" stroke="{DOSKA2}" stroke-width="24"/></g>')
    s += SL(Z_SRED, vor)
    s += SL(Z_SRED, podkova(500, 170, .9, t))
    kol = (f'<path d="M-20,1080 q500,-300 1960,-330 l0,120 q-1420,40 -1900,290 Z"'
           f' fill="#2e2822" {o(6)}/>')
    kol += (f'<path d="M-20,1010 q520,-280 1960,-310 l0,60 q-1420,40 -1900,290 Z"'
            f' fill="#241f1a"/>')
    s += SL(Z_SRED, kol)
    # ДВЕ БОРОЗДЫ: уходят вдаль к воротам, лёд блестит ВДОЛЬ колеи
    led = A.ease(A.seg(t, .3, 2.0))
    ld = ""
    for b, (y0, y1) in enumerate(((1060, 836), (946, 806))):
        ld += (f'<path d="M-40,{y0:.0f} q620,{-(y0-y1)*.72:.0f} 1960,{-(y0-y1):.0f}'
               f' l0,66 q-1340,{(y0-y1)*.86:.0f} -1960,{(y0-y1)*.16+64:.0f} Z"'
               f' fill="#1d1915" {o(5)}/>')
        ld += (f'<path d="M-40,{y0+14:.0f} q620,{-(y0-y1)*.72:.0f} 1960,{-(y0-y1):.0f}"'
               f' fill="none" stroke="url(#led)" stroke-width="{26*led:.0f}"'
               f' opacity="{.8*led:.2f}"/>')
        ld += (f'<path d="M-40,{y0+42:.0f} q620,{-(y0-y1)*.72:.0f} 1960,{-(y0-y1):.0f}"'
               f' fill="none" stroke="#eaf6ff" stroke-width="{7*led:.0f}"'
               f' opacity="{(.4+.4*abs(A.w(t,1.8,b*.3)))*led:.2f}"/>')
        for i in range(9):                   # продольные блики-штрихи по льду
            p = i / 8.0
            bx = -40 + p * 1960
            by = y0 + 20 - (y0 - y1) * p * .92
            ld += (f'<path d="M{bx:.0f},{by:.0f} l{130*led:.0f},{-12*led:.0f}"'
                   f' stroke="#ffffff" stroke-width="{5+3*abs(A.w(t,2.2,i*.17)):.0f}"'
                   f' opacity="{(.25+.35*abs(A.w(t,1.6,i*.13)))*led:.2f}"'
                   f' stroke-linecap="round"/>')
        for i in range(6):                   # трещины во льду
            bx = 120 + i * 300
            by = y0 + 30 - (y0 - y1) * ((bx + 40) / 1960.0) * .92
            ld += (f'<path d="M{bx:.0f},{by:.0f} l24,{-14:.0f} l30,10 l26,-12"'
                   f' fill="none" stroke="#9fc2d8" stroke-width="3"'
                   f' opacity="{.5*led:.2f}"/>')
    s += SL(Z_SRED, ld)
    pad = A.ease(A.seg(t, 1.6, .9))
    mx, my = 1120, 960
    s += SL(Z_SRED, figura(mx + pad * 70, my + pad * 110, 520 - pad * 130, t,
                           "#241d2b", "#ffd98a", False, .2, True, 1.0, True, 3.0 + pad * 6))
    s += SL(Z_SRED, para_izo_rta(mx + 40, my - 430 + pad * 120, t, .1, 1.1, .5))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(mx + sgn * 110, my - 300 + pad * 90, 180,
                              (-60 if sgn < 0 else -120) - 70 * pad * sgn, t,
                              "#2a2430", "#ffd98a", .2 + sgn * .1, 10.0)
        s += SL(Z_SRED, ruk)
    # ЛУЧИНА ЛЕТИТ ДУГОЙ: щепка с огоньком на конце и хвостом искр
    pl = A.seg(t, 1.7, 1.4)
    lx = mx + 180 + pl * 420
    ly = my - 360 - math.sin(math.pi * pl) * 420
    ugl = -40 + pl * 170
    luch_ = (f'<g transform="rotate({ugl:.0f} {lx:.0f} {ly:.0f})">'
             f'<path d="M{lx-96:.0f},{ly+6:.0f} l180,-14 l6,18 l-184,14 Z"'
             f' fill="url(#derev)" {o(4)}/>'
             f'<path d="M{lx-96:.0f},{ly+6:.0f} l180,-14" fill="none"'
             f' stroke="#d8b98a" stroke-width="3" opacity=".6"/></g>')
    s += SL(Z_SRED, luch_)
    s += SL(Z_SRED, ogon(lx + 86 * math.cos(math.radians(ugl)),
                         ly + 86 * math.sin(math.radians(ugl)), t, .52, .2, 4))
    for i in range(8):                       # хвост искр за лучиной
        q = i / 8.0
        s += SL(Z_SRED, f'<circle cx="{lx-q*150-10*A.w(t,1.4,i*.2):.0f}"'
                        f' cy="{ly+q*54+8*A.w(t,1.9,i*.1):.0f}"'
                        f' r="{6-q*4:.1f}" fill="{SVET}" opacity="{(1-q)*.7:.2f}"/>')
    s += SL(Z_SRED, teplo(lx, ly - 20, 230, 190, .40))
    kach = 8 * A.w(t, 2.2, .3)
    s += SL(Z_PERED, f'<g transform="rotate({kach:.1f} 420 700)">'
                     + figura(420, 1040, 440, t, "#231e2a", "#ffd98a", True, .5) + '</g>')
    s += SL(Z_PERED, para_izo_rta(452, 1040 - 376, t, .4, 1.0, .46))
    s += SL(Z_PERED, pleten(1480, 1070, 480, 200, 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 467, .5, 1.0))
    s += vinetka(.46)
    return s


def okolica_v_noyabrskih_sumerkah(t):
    """Край деревни: последняя жердяная ограда через весь кадр, покосившийся
    столб с вороной, дальше поле и туман, в котором что-то шевелится."""
    rnd = random.Random(3001)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 479)
    s += oblaka(t, 150, 4, 487, .26, "#b8c4d5", 9.0)
    s += SL(Z_DAL, f'<path d="M-20,620 q520,-50 1040,-16 q480,32 940,-24 l0,200 h-1960 Z"'
                   f' fill="#55514a" opacity=".9"/>')
    der = ""
    for i in range(5):
        dx_ = 40 + i * 240
        der += izba_snaruzhi(dx_, 600, 190, t, True, True, 491 + i)
    s += SL(Z_DAL, der)
    s += SL(Z_DAL, gryaz_polosa(640, 240, "#3c342c"))
    for i in range(4):
        s += SL(Z_DAL, dym(140 + i * 240, 470, t, 5, .22 + i * .02, 330, .4, "#d1d8e0", .9))
    pole = (f'<path d="M-20,700 q980,-60 1960,10 l0,400 h-1960 Z" fill="#4a443c" opacity=".9"/>')
    for i in range(14):
        pole += (f'<path d="M{60+i*140:.0f},{760+((i%3)*30)} q50,{-26-((i%2)*14)} 100,4"'
                 f' fill="none" stroke="#5d564b" stroke-width="7" opacity=".8"/>')
    s += SL(Z_DAL, pole)
    shev = ""
    sx_ = 1300 + 90 * A.w(t, 4.4, .1)
    shev += (f'<path d="M{sx_:.0f},860 q-40,-180 50,-230 q90,40 50,230 Z"'
             f' fill="#2b2f38" opacity="{.4+.3*abs(A.w(t,2.6)):.2f}"/>')
    shev += (f'<circle cx="{sx_+30:.0f}" cy="{640}" r="34" fill="#2b2f38"'
             f' opacity="{.4+.3*abs(A.w(t,2.6)):.2f}"/>')
    s += SL(Z_DAL, shev)
    ogr = ""
    for i in range(8):
        px = 60 + i * 260
        nak = -6 + (i % 3) * 5
        ogr += (f'<g transform="rotate({nak} {px:.0f} 1000)">'
                f'<rect x="{px-18:.0f}" y="700" width="36" height="320" rx="10"'
                f' fill="url(#derev)" {o(6)}/></g>')
    for r in range(3):
        yy = 760 + r * 90
        d = f'M20,{yy}'
        for i in range(8):
            d += f' Q{150+i*260:.0f},{yy+(22 if i%2==0 else -22)} {280+i*260:.0f},{yy}'
        ogr += (f'<path d="{d}" fill="none" stroke="url(#derev)" stroke-width="26"'
                f' stroke-linecap="round"/>')
    s += SL(Z_SRED, ogr)
    stx = 1600
    s += SL(Z_SRED, f'<g transform="rotate(-9 {stx} 1020)">'
                    f'<rect x="{stx-30}" y="420" width="60" height="620" rx="12"'
                    f' fill="url(#derev)" {o(8)}/>'
                    f'<rect x="{stx-54}" y="400" width="108" height="34" rx="10"'
                    f' fill="{DOSKA2}" {o(6)}/></g>')
    per = 7 * A.w(t, 1.3, .2)
    s += SL(Z_SRED, f'<g transform="translate({per:.1f},0)">'
                    + ptica(stx + 10, 380, t, 1.5, "#23262e", .1, "#1a1d24") + '</g>')
    for i, (bx, plt, ph) in enumerate(((560, False, .0), (740, True, .4))):
        s += SL(Z_PERED, figura(bx, 1070, 520 - i * 30, t, "#211c28", "#ffd98a", plt, ph, True, 1.0, True))
        s += SL(Z_PERED, para_izo_rta(bx + 36, 1070 - (520 - i * 30) * .84, t, ph, 1.1, .5))
    pok = A.ease(A.seg(t, .6, 1.3))
    ruk, (hx, hy) = rukav(640, 700, 240, -24 - 14 * pok, t, "#241f2b", "#ffd98a", .2, 4.0)
    s += SL(Z_PERED, ruk)
    s += SL(Z_PERED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="28" ry="20" fill="#241f2b" {o(4)}/>')
    s += SL(Z_PERED, luchina(420, 1010, t, 1.3, .2))
    s += SL(Z_PERED, teplo(420, 900, 420, 360, .4 + .12 * abs(A.w(t, 1.5))))
    s += tuman(t, 880, .5, "#d5e0ec")
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 499, .46, .9))
    s += vinetka(.48)
    return s


def kust_ili_chelovek(t):
    """В тумане за оградой стоит тёмная фигура на пол-кадра: голова, плечи,
    раскинутые руки. Путник с лучиной замирает и снимает шапку.

    Это КУСТ, которого принимают за человека: ствол с корой, крона из частых
    веток с инеем на концах, снеговая шапка сверху, рядно, зацепившееся за
    сук. Прежняя сплошная чёрная клякса не читалась ни тем, ни другим
    (осмотр 14.11)."""
    rnd = random.Random(3109)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 503)
    s += oblaka(t, 160, 3, 509, .2, "#aab7c8", 7.0)
    s += SL(Z_DAL, f'<path d="M-20,660 q980,-40 1960,20 l0,400 h-1960 Z"'
                   f' fill="#4b453d" opacity=".92"/>')
    s += SL(Z_DAL, ulica_dal(40, 620, 620, t, False, 521))
    s += SL(Z_DAL, gryaz_polosa(700, 260, "#362f28"))
    for i in range(3):
        s += SL(Z_DAL, dym(160 + i * 200, 480, t, 4, .22, 280, .34, "#ccd4de", .8))
    cx, cy = 1180, 1010
    rash = .92 + .08 * A.w(t, 2.4, .1)
    kus = ten(cx, cy + 14, 230, 34, .5)
    # СТВОЛ-ТУЛОВИЩЕ: от земли до «плеч», с корой
    kus += (f'<path d="M{cx-86},{cy} q22,-200 26,-430 q{32:.0f},-16 {64:.0f},0'
            f' q10,230 32,430 Z" fill="#4a3b2c" {o(7)}/>')
    for i in range(5):
        kus += (f'<path d="M{cx-56+i*28:.0f},{cy-24} q{-7+i*4:.0f},-200'
                f' {3:.0f},-392" fill="none" stroke="#33281e" stroke-width="5"'
                f' opacity=".8"/>')
    # «ПЛЕЧИ»: густой ком веток поперёк ствола
    kus += (f'<path d="M{cx-210},{cy-430} q90,-74 210,-74 q120,0 210,74'
            f' q-96,60 -210,60 q-114,0 -210,-60 Z" fill="#2f2b28"'
            f' opacity=".94" {o(6)}/>')
    # «ГОЛОВА»: круглый ком прутьев на макушке ствола
    kus += (f'<circle cx="{cx}" cy="{cy-596}" r="104" fill="#2f2b28"'
            f' opacity=".94" {o(6)}/>')
    for i in range(22):                        # прутья головы торчат во все стороны
        a = i * .2856
        dl = (54 + 44 * abs(math.sin(i * 1.3))) * rash
        kol_ = 5 * A.w(t, 2.0 + (i % 3) * .5, i * .09)
        kus += (f'<path d="M{cx+math.cos(a)*86:.0f},{cy-596+math.sin(a)*86:.0f}'
                f' l{math.cos(a)*dl+kol_:.0f},{math.sin(a)*dl:.0f}" stroke="#3b3028"'
                f' stroke-width="{9-i%4*2}" stroke-linecap="round"/>')
    for i in range(18):                        # прутья плеч — вверх и в стороны
        a = -2.86 + i * .152
        dl = (130 + 90 * abs(math.sin(i * .9))) * rash
        bx = cx + math.cos(a) * 110
        by = cy - 440 + math.sin(a) * 30
        kol_ = 7 * A.w(t, 2.3 + (i % 4) * .4, i * .11)
        ex, ey = bx + math.cos(a) * dl + kol_, by + math.sin(a) * dl * .9
        kus += (f'<path d="M{bx:.0f},{by:.0f} Q{(bx+ex)/2:.0f},{(by+ey)/2-26:.0f}'
                f' {ex:.0f},{ey:.0f}" fill="none" stroke="#3b3028"'
                f' stroke-width="{12-i%4*2}" stroke-linecap="round"/>')
        kus += (f'<path d="M{(bx+ex)/2:.0f},{(by+ey)/2-12:.0f} L{ex:.0f},{ey:.0f}"'
                f' fill="none" stroke="#cfe0f0" stroke-width="3" opacity=".5"/>')
    for sgn in (-1, 1):                        # «РУКИ»: толстые сучья в стороны
        kus += (f'<path d="M{cx+sgn*96:.0f},{cy-452}'
                f' q{sgn*200*rash:.0f},{-30*rash:.0f}'
                f' {sgn*300*rash:.0f},{-150*rash:.0f}" fill="none" stroke="#4a3b2c"'
                f' stroke-width="40" stroke-linecap="round"/>')
        kus += (f'<path d="M{cx+sgn*96:.0f},{cy-460}'
                f' q{sgn*200*rash:.0f},{-30*rash:.0f}'
                f' {sgn*300*rash:.0f},{-150*rash:.0f}" fill="none" stroke="#d2e2f2"'
                f' stroke-width="5" opacity=".45"/>')
        for j in range(3):                     # пальцы-прутья на концах «рук»
            kus += (f'<path d="M{cx+sgn*300*rash:.0f},{cy-602*rash:.0f}'
                    f' l{sgn*(44+j*24):.0f},{-50+j*34+8*A.w(t,2.0,j*.2):.0f}"'
                    f' stroke="#3b3028" stroke-width="{11-j*2}"'
                    f' stroke-linecap="round"/>')
        kus += (f'<path d="M{cx+sgn*300*rash-38:.0f},{cy-604*rash:.0f}'
                f' q38,-20 76,0 q-24,12 -38,12 q-14,0 -38,-12 Z"'
                f' fill="url(#sneg)" opacity=".7"/>')
    kus += (f'<path d="M{cx-96},{cy-672} q96,-54 192,0 q-48,30 -96,30'
            f' q-48,0 -96,-30 Z" fill="url(#sneg)" opacity=".88" {o(4)}/>')
    for i in range(5):                         # снег комками на плечах
        kus += (f'<path d="M{cx-178+i*74:.0f},{cy-466-((i%2)*18):.0f}'
                f' q28,-18 56,0 q-18,10 -28,10 q-10,0 -28,-10 Z"'
                f' fill="url(#sneg)" opacity=".5"/>')
    s += SL(Z_SRED, kus)
    ryad = 7 * A.w(t, 2.8, .2)                 # рядно, зацепившееся за сук
    s += SL(Z_SRED, f'<path d="M{cx-300:.0f},{cy-540:.0f}'
                    f' q{-40+ryad:.0f},90 {-10+ryad:.0f},200'
                    f' q{60:.0f},20 {96:.0f},-30 q{-30:.0f},-90 {-16:.0f},-166 Z"'
                    f' fill="#7a6246" opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, grozd_ryabiny(cx + 310, cy - 640, t, .8, 12, 523, .3))
    vzl = A.ease(A.seg(t, 2.2, 1.1))
    s += SL(Z_SRED, ptica(cx + 60 - vzl * 300, cy - 700 - vzl * 300, t, 1.3, "#23262e", .2, "#1a1d24"))
    ogr = ""
    for i in range(9):
        px = 60 + i * 230
        ogr += (f'<rect x="{px-16:.0f}" y="760" width="32" height="300" rx="9"'
                f' fill="url(#derev)" {o(5)}/>')
    for r in range(2):
        yy = 820 + r * 90
        d = f'M20,{yy}'
        for i in range(9):
            d += f' Q{130+i*230:.0f},{yy+(18 if i%2==0 else -18)} {250+i*230:.0f},{yy}'
        ogr += (f'<path d="{d}" fill="none" stroke="url(#derev)" stroke-width="22"'
                f' stroke-linecap="round"/>')
    s += SL(Z_SRED, ogr)
    snyal = A.ease(A.seg(t, .9, .7)) - A.ease(A.seg(t, 2.8, .6))
    px_, py_ = 460, 1060
    s += SL(Z_PERED, figura(px_, py_, 540, t, "#1d1924", "#ffd98a", False, .2, True, 1.0, True))
    s += SL(Z_PERED, para_izo_rta(px_ + 40, py_ - 460, t, .2, 1.2, .52))
    ruk, (sx2, sy2) = rukav(px_ + 50, py_ - 420, 150, -84 - 30 * snyal, t, "#20202c", "#ffd98a", .1, 5.0)
    s += SL(Z_PERED, ruk)
    s += SL(Z_PERED, f'<ellipse cx="{sx2:.0f}" cy="{sy2-40*snyal:.0f}" rx="76"'
                     f' ry="{46 - 10*snyal:.0f}" fill="#4a3a2c" {o(6)}/>'
                     f'<ellipse cx="{sx2:.0f}" cy="{sy2-14-40*snyal:.0f}" rx="58" ry="30"'
                     f' fill="#5e4a36" {o(4)}/>')
    ruk2, (lx, ly) = rukav(px_ - 60, py_ - 400, 170, 202, t, "#20202c", "#ffd98a", .4, 7.0)
    s += SL(Z_PERED, ruk2)
    s += SL(Z_PERED, luchina(lx, ly + 20, t, 1.5, .2))
    s += SL(Z_PERED, teplo(lx, ly - 60, 440, 380, .5 + .14 * abs(A.w(t, 1.2))))
    s += SL(Z_PERED, blik(lx, ly - 50, t, .5, "#a8c8ff", SVET, .3))
    s += tuman(t, 820, .62, "#dbe6f2")
    s += tuman(t, 980, .5, "#d2deea")
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 541, .44, .9))
    s += vinetka(.5)
    return s


def den_del_i_vecher_u_ognya(t):
    """Двор избы: низкое солнце быстро катится по небу, а хозяева бегом
    успевают всё — отец колет дрова, мать несёт вёдра, сын гонит корову."""
    rnd = random.Random(3203)
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += nebo("zakat", t, False, 547)
    s += oblaka(t, 170, 4, 557, .34, "#e8c9a8", 11.0)
    kat = A.seg(t, .2, 6.0)
    sx_ = 260 + kat * 1420
    sy_ = 300 - math.sin(math.pi * kat) * 170
    s += SL(Z_NEBO, f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="92" fill="{SVET}" opacity=".95"/>')
    s += SL(Z_NEBO, teplo(sx_, sy_, 520, 460, .5))
    s += SL(Z_DAL, ulica_dal(1200, 700, 740, t, False, 563))
    s += SL(Z_DAL, izba_snaruzhi(80, 820, 620, t, True, True, 569))
    s += SL(Z_DAL, dym(520, 560, t, 6, .26, 400, .44, "#d8d0c6", 1.2))
    s += SL(Z_DAL, gryaz_polosa(820, 280, "#44382c"))
    s += SL(Z_SRED, pleten(760, 880, 1140, 200, 11))
    chur = ""
    for i in range(5):
        chur += (f'<ellipse cx="{980+i*70:.0f}" cy="{1010+((i%3)*12)}" rx="46" ry="30"'
                 f' fill="url(#brev)" {o(5)}/>'
                 f'<ellipse cx="{980+i*70:.0f}" cy="{1004+((i%3)*12)}" rx="30" ry="18"'
                 f' fill="#5a3721" opacity=".6"/>')
    s += SL(Z_SRED, chur)
    kolx, koly = 760, 940
    s += SL(Z_SRED, f'<path d="M{kolx-70},{koly} l14,-120 q56,-18 112,0 l14,120 Z"'
                    f' fill="url(#brev)" {o(7)}/>')
    rasp = abs(A.w(t, .52, .0))
    chx = kolx
    s += SL(Z_SRED, f'<path d="M{chx-80:.0f},{koly-120} q80,-30 160,0 l-14,-70'
                    f' q-66,-20 -132,0 Z" fill="url(#brev)" {o(6)}/>')
    s += SL(Z_SRED, figura(600, 1030, 480, t, "#2b2436", "#ffe2a8", False, .1, True))
    ruk, (ax, ay) = rukav(680, 1030 - 380, 200, -70 + 110 * rasp, t, "#2b2436", "#ffe2a8", .0, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<g transform="rotate({-60+120*rasp:.0f} {ax:.0f} {ay:.0f})">'
                    f'<rect x="{ax-10:.0f}" y="{ay:.0f}" width="26" height="190" rx="10"'
                    f' fill="url(#derev)" {o(5)}/>'
                    f'<path d="M{ax-50:.0f},{ay:.0f} q60,-48 90,6 q-40,30 -90,-6 Z"'
                    f' fill="url(#zhel)" {o(6)}/></g>')
    shep = ""
    for i in range(8):
        p = ((t * 1.1) + i / 8.0) % 1.0
        shep += (f'<path d="M{kolx+20+p*200:.0f},{koly-160+p*150:.0f} q20,-16 38,2'
                 f' q-20,16 -38,-2 Z" fill="{KREM}" opacity="{(1-p)*.85:.2f}"/>')
    s += SL(Z_SRED, shep)
    hod = A.ease(A.seg(t, .4, 4.6))
    mx = 1700 - hod * 520
    s += SL(Z_SRED, figura(mx, 1050, 450, t, "#2d2537", "#ffe2a8", True, .4, True))
    kor = 13 * A.w(t, 1.1, .2)
    krm = (f'<g transform="rotate({kor:.1f} {mx:.0f} {1050-380:.0f})">'
           f'<path d="M{mx-180:.0f},{1050-390} q180,-46 360,0" fill="none"'
           f' stroke="url(#derev)" stroke-width="22" stroke-linecap="round"/>')
    for sgn in (-1, 1):
        krm += (f'<line x1="{mx+sgn*170:.0f}" y1="{1050-382}" x2="{mx+sgn*170:.0f}"'
                f' y2="{1050-250}" stroke="{ZHELEZ}" stroke-width="7"/>'
                f'<path d="M{mx+sgn*170-54:.0f},{1050-250} l12,130 h84 l12,-130 Z"'
                f' fill="url(#zhel)" {o(6)}/>'
                f'<ellipse cx="{mx+sgn*170:.0f}" cy="{1050-244}" rx="54" ry="14"'
                f' fill="#8fb4c4" opacity=".8"/>')
    s += SL(Z_SRED, krm + '</g>')
    kx = 1300 + (1 - hod) * 420
    krv = (f'<g transform="translate({kx:.0f},{1000+8*A.w(t,1.4,.3):.0f})">'
           f'<ellipse cx="0" cy="-120" rx="230" ry="130" fill="#a8744a" {o(8)}/>'
           f'<ellipse cx="-80" cy="-150" rx="70" ry="54" fill="#efe7d8" opacity=".9"/>'
           f'<circle cx="200" cy="-210" r="84" fill="#a8744a" {o(7)}/>'
           f'<ellipse cx="262" cy="-176" rx="44" ry="34" fill="#d9a583" {o(5)}/>'
           f'<circle cx="250" cy="-182" r="7" fill="{K}"/><circle cx="276" cy="-182" r="7" fill="{K}"/>'
           f'<path d="M166,-278 q-40,-66 20,-56 q30,20 10,56 Z" fill="#e8e0cf" {o(4)}/>'
           f'<path d="M234,-284 q40,-66 -18,-56 q-30,20 -10,56 Z" fill="#e8e0cf" {o(4)}/>'
           f'<circle cx="214" cy="-258" r="{4 if A.blink(t,3.2,.2) else 10}" fill="{K}"/>'
           f'<path d="M-230,-150 q-70,-60 -30,-120" fill="none" stroke="#a8744a" stroke-width="18"/>')
    for i, dx in enumerate((-160, -60, 60, 160)):
        krv += (f'<rect x="{dx}" y="0" width="46" height="{90+12*abs(A.w(t,1.0,i*.2)):.0f}"'
                f' rx="14" fill="#8d5f3c" {o(5)}/>')
    krv += '</g>'
    s += SL(Z_SRED, krv)
    zakr = A.ease(A.seg(t, 4.4, 1.0))
    s += SL(Z_PERED, dver(300, 600, 240, 320, (1 - zakr) * .7, kruchok=True))
    s += SL(Z_PERED, teplo(420, 740, 340, 290, .3 + .3 * zakr))
    s += SL(Z_PERED, goloe_derevo(1840, 1070, 540, t, 571, 7, "#2d2a28"))
    s += vinetka(.44)
    return s


def babushka_i_shapka_na_kryuchke(t):
    """Прихожая деревенского дома: вешалка с крючками, на крючке ушанка.
    Рука подростка тянется к ней и опускается, бабушка смотрит поверх очков.

    Ушанка — РАЗМЕРОМ С ГОЛОВУ, а не с человека (прежде была под 500 px и
    читалась тулупом), очки лежат на лице самой `figura()`, второго лица
    поверх не рисуем (осмотр 14.11)."""
    rnd = random.Random(3301)
    s = f'<rect width="{W}" height="{H}" fill="#564436"/>'
    s += nebo("noch", t, False, 577)
    s += SL(Z_DAL, doski(0, 0, W, 1080, 150, True, "dosk"))
    s += SL(Z_DAL, f'<rect y="0" width="{W}" height="1080" fill="#3b2f26" opacity=".35"/>')
    s += SL(Z_DAL, okno_izby(80, 170, 280, 230, t, svet=False, moroz=.2))
    s += SL(Z_DAL, f'<rect x="80" y="170" width="280" height="230" fill="#0d1018" opacity=".8"/>')
    s += kvartira_veschi(1420, 1040, 480, t, 43)
    s += SL(Z_SRED, polovicy(930))
    s += SL(Z_SRED, tusklaya_lampochka(960, 150, t, 1.5, True))
    vx, vy, vw = 560, 360, 800
    ves = (f'<rect x="{vx}" y="{vy}" width="{vw}" height="110" rx="14"'
           f' fill="url(#derev)" {o(9)}/>')
    ves += (f'<rect x="{vx+20}" y="{vy+22}" width="{vw-40}" height="24" rx="8"'
            f' fill="{DOSKA2}" {o(5)}/>')
    for i in range(5):
        hx_ = vx + 80 + i * 160
        ves += (f'<path d="M{hx_:.0f},{vy+110} l0,46 q0,34 -34,34 q-30,0 -30,-26"'
                f' fill="none" stroke="url(#zhel)" stroke-width="16" stroke-linecap="round"/>')
        ves += (f'<circle cx="{hx_:.0f}" cy="{vy+66}" r="14" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, ves)
    # УШАНКА: купол, светлый околыш, два уха — ширина 230, высота 180
    kach = 5.0 * A.w(t, 2.1, .1)
    ux, uy = vx + 400, vy + 230                # uy — низ околыша
    uw, uh = 118, 104                          # полуширина купола, его высота
    ush = f'<g transform="rotate({kach:.2f} {ux:.0f} {vy+150:.0f})">'
    ush += (f'<line x1="{ux:.0f}" y1="{vy+150:.0f}" x2="{ux:.0f}" y2="{uy-uh:.0f}"'
            f' stroke="#5e4a36" stroke-width="7"/>')
    for sgn in (-1, 1):                        # уши-лопасти прижаты к бокам
        ush += (f'<path d="M{ux+sgn*uw*.74:.0f},{uy-uh*.52:.0f}'
                f' q{sgn*uw*.52:.0f},{uh*.30:.0f} {sgn*uw*.40:.0f},{uh*1.10:.0f}'
                f' q{-sgn*uw*.40:.0f},{uh*.20:.0f} {-sgn*uw*.56:.0f},{-uh*.18:.0f} Z"'
                f' fill="#cbb48c" {o(6)}/>')
        for j in range(4):
            ush += (f'<path d="M{ux+sgn*(uw*.78+j*10):.0f},{uy-uh*.30+j*16:.0f}'
                    f' l{sgn*22:.0f},26" stroke="#a98f68" stroke-width="5"'
                    f' opacity=".8"/>')
    ush += (f'<path d="M{ux-uw:.0f},{uy-uh*.30:.0f} a{uw:.0f},{uh*.96:.0f} 0 0 1'
            f' {uw*2:.0f},0 Z" fill="#6b5340" {o(7)}/>')
    for i in range(5):                         # мех: короткие штрихи по куполу
        ush += (f'<path d="M{ux-uw*.66+i*uw*.33:.0f},{uy-uh*.44:.0f}'
                f' q8,{-uh*.22:.0f} 2,{-uh*.36:.0f}" fill="none" stroke="#50402f"'
                f' stroke-width="6" opacity=".7"/>')
    ush += (f'<rect x="{ux-uw*1.04:.0f}" y="{uy-uh*.34:.0f}" width="{uw*2.08:.0f}"'
            f' height="{uh*.40:.0f}" rx="{uh*.18:.0f}" fill="#cbb48c" {o(6)}/>')
    for i in range(7):
        ush += (f'<path d="M{ux-uw*.90+i*uw*.30:.0f},{uy-uh*.30:.0f} q8,{uh*.16:.0f}'
                f' -2,{uh*.30:.0f}" fill="none" stroke="#a98f68" stroke-width="6"'
                f' opacity=".8"/>')
    ush += '</g>'
    s += SL(Z_SRED, ush)
    s += SL(Z_SRED, teplo(ux, uy - 60, 330, 280, .32 + .1 * abs(A.w(t, 1.8))))
    tyan = A.ease(A.seg(t, .4, 1.1)) - A.ease(A.seg(t, 2.6, 1.0))
    ruk, (hx, hy) = rukav(1300, 1000, 420, -118 + 26 * (1 - tyan), t, "#2c4a5e", "#ffd98a", .1, 3.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="34" ry="24" fill="#2c4a5e" {o(5)}/>')
    s += SL(Z_SRED, figura(1360, 1070, 560, t, "#24313d", "#ffd98a", False, .3))
    # БАБУШКА: лицо рисует сама figura, сверху только очки и взгляд поверх них
    bx, by_ = 320, 1060
    s += SL(Z_SRED, figura(bx, by_, 600, t, "#4a2b33", "#ffd98a", True, .5))
    hh_ = 600 * .145
    gy_ = by_ - 600 * .845
    och_y = gy_ + hh_ * .30 + 10 * abs(A.w(t, 1.9, .2))
    och = ""
    for sgn in (-1, 1):
        och += (f'<circle cx="{bx+sgn*hh_*.42:.0f}" cy="{och_y:.0f}" r="{hh_*.33:.0f}"'
                f' fill="url(#stekl)" opacity=".45" stroke="{ZHELEZ}" stroke-width="7"/>')
    och += (f'<path d="M{bx-hh_*.12:.0f},{och_y:.0f} h{hh_*.24:.0f}" stroke="{ZHELEZ}"'
            f' stroke-width="6"/>')
    och += (f'<path d="M{bx-hh_*.76:.0f},{och_y-hh_*.06:.0f} q{-hh_*.30:.0f},{hh_*.10:.0f}'
            f' {-hh_*.34:.0f},{hh_*.40:.0f}" fill="none" stroke="{ZHELEZ}"'
            f' stroke-width="5"/>')
    s += SL(Z_SRED, och)
    s += SL(Z_SRED, mebel_hlam(640, 1070, 420, t, 47))
    bot = ""
    for i in range(4):
        bx_ = 760 + i * 130
        bot += (f'<path d="M{bx_:.0f},1070 q10,-110 70,-114 q66,6 50,70'
                f' q60,10 60,44 Z" fill="#2b2b30" {o(6)}/>')
        bot += (f'<path d="M{bx_:.0f},1056 q96,26 180,8" fill="none" stroke="#4e4e58"'
                f' stroke-width="8"/>')
    s += SL(Z_PERED, bot)
    s += SL(Z_PERED, ramka_pp("pravo", "#15100c", .5))
    s += vinetka(.46)
    return s


def porog_cherta(t):
    """Дверной проём и порог на пол-кадра: по порогу проведена светящаяся
    меловая черта, соседка снаружи протягивает через неё миску."""
    rnd = random.Random(3407)
    s = f'<rect width="{W}" height="{H}" fill="#1e1811"/>'
    s += nebo("sumer", t, False, 587)
    s += SL(Z_DAL, brevna(0, 0, 400, 1080, 100))
    s += SL(Z_DAL, brevna(1520, 0, 400, 1080, 100))
    s += SL(Z_DAL, f'<rect x="380" y="0" width="1160" height="1080" fill="url(#nsumer)"'
                   f' opacity=".92"/>')
    s += SL(Z_DAL, ulica_dal(400, 660, 1140, t, False, 593))
    for i in range(3):
        s += SL(Z_DAL, dym(520 + i * 330, 520, t, 4, .22, 280, .34, "#ccd4de", .8))
    s += SL(Z_DAL, gryaz_polosa(700, 180, "#39312a"))
    pr = (f'<rect x="340" y="0" width="90" height="820" rx="12" fill="url(#derev)" {o(9)}/>'
          f'<rect x="1490" y="0" width="90" height="820" rx="12" fill="url(#derev)" {o(9)}/>'
          f'<rect x="340" y="0" width="1240" height="110" rx="12" fill="{DOSKA2}" {o(9)}/>')
    for i in range(10):
        pr += (f'<path d="M{400+i*120:.0f},20 q26,34 0,68" fill="none" stroke="#5a3a22"'
               f' stroke-width="7" opacity=".7"/>')
    s += SL(Z_SRED, pr)
    s += SL(Z_SRED, podkova(960, 170, 1.1, t))
    por = (f'<rect x="330" y="840" width="1260" height="150" rx="18"'
           f' fill="url(#dosk)" {o(10)}/>')
    por += (f'<rect x="330" y="812" width="1260" height="44" rx="14" fill="{DOSKA2}" {o(8)}/>')
    for i in range(10):
        por += (f'<path d="M{380+i*130:.0f},862 q24,60 0,120" fill="none" stroke="#5a3a22"'
                f' stroke-width="8" opacity=".6"/>')
    por += (f'<rect x="330" y="982" width="1260" height="40" rx="12" fill="#5a3a22" {o(7)}/>')
    por += polovicy(1020)
    s += SL(Z_SRED, por)
    s += SL(Z_SRED, f'<rect x="340" y="820" width="90" height="260" rx="12"'
                    f' fill="url(#derev)" {o(9)}/>'
                    f'<rect x="1490" y="820" width="90" height="260" rx="12"'
                    f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_SRED, dver(120, 150, 240, 830, .0, kruchok=True, cepochka=True))
    sv = .54 + .34 * abs(A.w(t, 1.2))
    cher = (f'<path d="M370,{836} q300,{-18} 600,{-4} q300,14 600,{-2}" fill="none"'
            f' stroke="#ffffff" stroke-width="32" opacity="{sv:.2f}"'
            f' stroke-linecap="round"/>')
    cher += (f'<path d="M370,{836} q300,{-18} 600,{-4} q300,14 600,{-2}" fill="none"'
             f' stroke="{SVET}" stroke-width="46" opacity="{sv*.45:.2f}"/>')
    for i in range(11):
        cher += (f'<circle cx="{400+i*118:.0f}" cy="{832+((i%3)-1)*6}"'
                 f' r="{7+5*abs(A.w(t,1.6,i*.13)):.1f}" fill="#ffffff"'
                 f' opacity="{.5+.4*abs(A.w(t,1.3,i*.11)):.2f}"/>')
    s += SL(Z_SRED, cher)
    s += SL(Z_SRED, teplo(960, 836, 620, 170, .36 * sv))
    perest = A.ease(A.seg(t, 3.0, 1.4))
    sx_ = 1430 - perest * 150
    s += SL(Z_SRED, figura(sx_, 1010 - perest * 30, 560, t, "#1f1b26", "#cfe4f5", True, .3, True, 1.0, True))
    s += SL(Z_SRED, para_izo_rta(sx_ + 40, 1010 - 470, t, .2, 1.1, .5))
    viz = abs(A.w(t, 1.9, .1))
    ruk, (hx, hy) = rukav(sx_ - 120, 1010 - 400, 300, 176 + 10 * viz, t, "#44303a", "#cfe4f5", .2, 5.0)
    s += SL(Z_SRED, ruk)
    mis = (f'<path d="M{hx-110:.0f},{hy-10:.0f} q110,96 220,0 q-110,30 -220,0 Z"'
           f' fill="url(#glina)" {o(7)}/>')
    mis += (f'<ellipse cx="{hx:.0f}" cy="{hy-16:.0f}" rx="112" ry="28" fill="#9c6a3c" {o(5)}/>')
    mis += (f'<ellipse cx="{hx:.0f}" cy="{hy-24:.0f}" rx="92" ry="20" fill="url(#krem)"/>')
    s += SL(Z_SRED, mis)
    s += SL(Z_SRED, par(hx, hy - 50, t, 4, .5, 170, .5, .8))
    mnt = abs(A.w(t, 1.1, .3))
    bx = 520
    s += SL(Z_SRED, figura(bx, 1040, 600, t, "#4a2b33", "#ffd98a", True, .5))
    ruk2, (bx2, by2) = rukav(bx + 110, 1040 - 420, 230, -16 - 34 * mnt, t, "#5b2b32", "#ffd98a", .1, 6.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{bx2:.0f}" cy="{by2:.0f}" rx="34" ry="24"'
                    f' fill="#dfb391" {o(5)}/>')
    s += SL(Z_SRED, luchina(430, 700, t, 1.6, .2))
    s += SL(Z_SRED, teplo(440, 560, 520, 460, .46 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_PERED, f'<path d="M-20,1080 q420,-80 900,-30 l0,130 h-920 Z"'
                     f' fill="#120d0a" opacity=".92"/>')
    s += SL(Z_PERED, krynka(260, 1050, 1.5))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 599, .42, .9))
    s += vinetka(.48)
    return s
