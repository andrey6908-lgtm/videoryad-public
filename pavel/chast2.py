# -*- coding: utf-8 -*-
"""ПОРЦИЯ 2: декорации ролика «19 ноября — Павел Ледостав».

Блок запретов: лёд, молоко, зависть. Сцены рисуются заново под текст ЭТОГО
дня (R-0019), люди — figura() из lok_obshchee, руки — _ruka() от плеча,
кистей и пальцев не рисуем (R-0051). Задание — zadaniya/porciya2.md.
"""
import math, random
from baza import *
import anim as A
from lok_obshchee import *
from lok_obshchee import (
    _plecho, _predmet_naruzhu, _ruka, _ruka_ekr, _ruka_so_sgibom)
from chast1 import (_merzlaya_zemlya, _trava_suhaya, _petuh, _ramka_lubok,
                    _cherta_zapreta, _valenok)


def mokrye_valenki_na_pechi(t):
    """Тёплая печь с лежанкой: на приступке сохнет пара мокрых валенок, с них
    натекла лужица, рядом варежки на верёвочке. Мальчик в отцовской сорочке
    сидит на лавке с кружкой молока, мать качает головой."""
    rnd = random.Random(2001)
    s = stena_gornicy_19(t, 5, 800, True, True)
    s += SL(Z_DAL, okno_izby(1480, 220, 300, 260, t, None, .55, False, True))
    s += SL(Z_SRED, pech(120, 180, 720, 620, t, True, True, False))
    s += SL(Z_SRED, ogon(380, 640, t, 1.5, .1, 7) + teplo(380, 620, 420, 340, .55))
    # приступок с мокрыми валенками и лужицей
    s += SL(Z_SRED, f'<rect x="300" y="800" width="520" height="40" rx="8"'
                    f' fill="{PECH2}" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, _valenok(430, 806, 2.7, -7, "#c9bfa6")
            + _valenok(690, 812, 2.7, 8, "#d8cbb0"))
    for i in range(4):
        s += SL(Z_SRED, par(430 + i * 60, 680, t, 3, .45, 130, .35, .9))
    luzh = 90 + 60 * A.ease(A.seg(t, .4, 3.0))
    s += SL(Z_SRED, f'<ellipse cx="520" cy="856" rx="{luzh:.0f}" ry="{luzh*.22:.0f}"'
                    f' fill="#4a7a88" opacity=".7"/>'
                    f'<ellipse cx="500" cy="850" rx="{luzh*.4:.0f}" ry="{luzh*.1:.0f}"'
                    f' fill="#9fd0e4" opacity=".55"/>')
    # варежки на верёвочке и мокрые штаны
    s += SL(Z_SRED, f'<path d="M880,600 q{120:.0f},{40:.0f} {240:.0f},{-10:.0f}"'
                    f' fill="none" stroke="#b9a37a" stroke-width="5"/>')
    s += SL(Z_SRED, varezhka(930, 660, 1.1, -8, TKAN, t, .2)
            + varezhka(1060, 650, 1.1, 8, TKAN, t, .7))
    s += SL(Z_SRED, f'<path d="M1180,610 q{60:.0f},{120:.0f} {20:.0f},{230:.0f}'
                    f' l{-110:.0f},0 q{40:.0f},{-120:.0f} {-10:.0f},{-230:.0f} Z"'
                    f' fill="#5a6a7a" stroke="{K}" stroke-width="4.5"/>')
    # МАЛЬЧИК на лавке с кружкой
    s += SL(Z_SRED, lavka(1180, 900, 420))
    mx, my, mh = 1340, 900, 420
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#e8e2d6", kant="#ffd98a", ph=.3))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .26, 42, t, "#e8e2d6", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .26, 46, t, "#e8e2d6", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2 + kruzhka_moloka((e1x + e2x) * .5, e1y + 40, .9, t, True, .2))
    s += SL(Z_SRED, f'<ellipse cx="{mx-60:.0f}" cy="{my-20:.0f}" rx="30" ry="46"'
                    f' fill="#9a7c45" stroke="{K}" stroke-width="3.6"/>'
                    f'<ellipse cx="{mx+50:.0f}" cy="{my-16:.0f}" rx="30" ry="46"'
                    f' fill="#9a7c45" stroke="{K}" stroke-width="3.6"/>')
    # МАТЬ у печи: обе руки в бока, качает головой
    zx, zy, zh = 900, 1040, 660
    kch = 3.4 * A.w(t, 1.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {zx:.0f} {zy-zh*.6:.0f})">'
            + figura(zx, zy, zh, t, col="#8a2f22", kant="#ffd98a", platok=True, ph=.5)
            + '</g>')
    r3, (e3x, e3y), _ = _ruka(zx, zy, zh, 1, zh * .24, 64, t, "#8a2f22", "#ffd98a", .3, 3)
    r4, (e4x, e4y), _ = _ruka(zx, zy, zh, -1, zh * .24, 66, t, "#8a2f22", "#ffd98a", .8, 3)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, ten(zx, zy + 6, 130, 22, .45))
    # ухват, чугунок, кот, палка у двери
    s += SL(Z_SRED, f'<path d="M160,1060 l{30:.0f},{-420:.0f}" stroke="#8a6342"'
                    f' stroke-width="12" fill="none"/>'
                    f'<path d="M172,650 q{-40:.0f},{-50:.0f} {10:.0f},{-80:.0f}'
                    f' M212,642 q{40:.0f},{-50:.0f} {-6:.0f},{-82:.0f}" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="11"/>')
    s += SL(Z_SRED, f'<path d="M760,1040 q{-18:.0f},{-70:.0f} {56:.0f},{-74:.0f}'
                    f' q{74:.0f},{4:.0f} {56:.0f},{74:.0f} Z" fill="{CHUGUN}"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="816" cy="964" rx="58" ry="16" fill="#4a4442"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, kot(1600, 1050, t, 1.6, "#3b3430", True))
    s += SL(Z_SRED, polka_s_bankami(1180, 420, 560, t, 13, 4, False))
    s += SL(Z_SRED, utvar_izby(140, 480, 320, t, 7))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def brat_vedet_mladshih(t):
    """Развилка тропинок у пруда: прямая идёт через лёд, длинная огибает по
    берегу. Четверо детей цепочкой идут в обход — старший в отцовской шапке
    ведёт младшую за руку, один везёт санки. Короткая тропинка пустует."""
    rnd = random.Random(2002)
    s = nebo("den", t, False, 227)
    s += oblaka(t, 140, 5, 137, .40)
    s += SL(Z_DAL, ulica_dal(1180, 360, 740, t, True, 101))
    s += SL(Z_DAL, izba_snaruzhi(1560, 380, 260, t, True, True, 53)
            + dym(1586, 240, t, 6, .22, 240, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(420, 229, False))
    s += SL(Z_SRED, f'<ellipse cx="980" cy="700" rx="620" ry="220" fill="url(#led)"'
                    f' stroke="#eaf6ff" stroke-width="9"/>')
    s += SL(Z_SRED, korka_lda(980, 700, 580, 200, t, .2, .0, .8, .3))
    # короткая тропинка через лёд — пунктиром, пустая
    for i in range(9):
        s += SL(Z_SRED, f'<ellipse cx="{560+i*96:.0f}" cy="{700+((i*5)%3-1)*20:.0f}"'
                        f' rx="34" ry="12" fill="#8a98a8" opacity=".35"/>')
    # длинная тропинка по берегу
    s += SL(Z_SRED, f'<path d="M-40,980 Q400,1040 980,980 Q1500,930 1960,1000"'
                    f' fill="none" stroke="#8a7a62" stroke-width="86" opacity=".9"/>'
                    f'<path d="M-40,980 Q400,1040 980,980 Q1500,930 1960,1000"'
                    f' fill="none" stroke="#6f6256" stroke-width="44" opacity=".65"/>')
    # ЧЕТВЕРО ДЕТЕЙ цепочкой
    idt = A.ease(A.seg(t, .3, 3.0))
    deti = ((360, 1056, 520, "#6b4428", True), (560, 1066, 420, "#3f5a6a", False),
            (760, 1062, 450, "#8a2f22", False), (950, 1072, 380, "#4a6a3a", False))
    for i, (dx_, dy_, dh_, col, star) in enumerate(deti):
        px_ = dx_ + 220 * idt
        s += SL(Z_SRED, figura(px_, dy_, dh_, t, col=col, kant="#ffd9a8",
                               shapka=True, ph=i * .3))
        rk, (ex, ey), _ = _ruka(px_, dy_, dh_, -1 if i == 0 else 1, dh_ * .24,
                                40 if i else -10, t, col, "#ffd9a8", i * .2, 5)
        s += SL(Z_SRED, rk)
        if star:
            rk2, (e2x, e2y), _ = _ruka(px_, dy_, dh_, 1, dh_ * .26, 26, t,
                                       col, "#ffd9a8", .5, 4)
            s += SL(Z_SRED, rk2 + f'<path d="M{e2x:.0f},{e2y:.0f} L{px_+180:.0f},'
                                  f'{dy_-180:.0f}" stroke="{col}" stroke-width="13"'
                                  f' stroke-linecap="round"/>')
        if i == 2:
            s += SL(Z_SRED, f'<path d="M{ex:.0f},{ey:.0f} q{90:.0f},{60:.0f}'
                            f' {170:.0f},{70:.0f}" fill="none" stroke="#b9a37a"'
                            f' stroke-width="4"/>')
            s += SL(Z_SRED, sanki_derev(px_ + 230, dy_ + 20, .70, t, i * .2, False))
        s += SL(Z_SRED, para_izo_rta(px_ - 22, dy_ - dh_ * .80, t, i * .25, .8, .45))
        s += SL(Z_SRED, ten(px_, dy_ + 5, 84, 15, .35))
    # собака бежит впереди
    beg = ((t * .55) % 1.0)
    sx_ = 1300 + 300 * beg
    s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="1000" rx="70" ry="34" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{sx_+62:.0f}" cy="966" r="28" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M{sx_+78:.0f},944 l{12:.0f},{-28:.0f} l{12:.0f},{26:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{sx_-66:.0f},988 q{-36:.0f},{-28:.0f} {-52:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#6b5230" stroke-width="8"/>'
                    f'<path d="M{sx_-36:.0f},1028 l-6,30 M{sx_+14:.0f},1032 l4,28'
                    f' M{sx_+52:.0f},1026 l8,30" stroke="#54351f" stroke-width="9"/>')
    s += SL(Z_SRED, goloe_derevo_ld(220, 920, 480, t, 229, 7, True)
            + goloe_derevo_ld(1780, 960, 420, t, 233, 6, True))
    s += SL(Z_SRED, kamysh(120, 880, 200, t, 6, 239, True)
            + kamysh(1860, 900, 210, t, 6, 241, True))
    s += SL(Z_SRED, mostki(1420, 760, 380, t, True, 140))
    s += SL(Z_SRED, dvorovye_veschi(1560, 1070, 320, t, 227, ["kadka", "vedro"]))
    s += SL(Z_LETIT, sneg_letit(t, 16, 47, .34, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def listok_na_shkolnoy_doske_obyavleni(t):
    """Школьный коридор: доска объявлений на пол-кадра — расписание, стенгазета
    с нарисованной ёлкой и большой листок с прудом и восклицательным знаком.
    Учительница с указкой стучит по листку, трое школьников кивают."""
    rnd = random.Random(2003)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="520" fill="#d8cbb0"/>'
                   f'<rect x="0" y="520" width="{W}" height="60" fill="#8a7a52"'
                   f' opacity=".9"/>'
                   f'<rect x="0" y="580" width="{W}" height="500" fill="#6f7a84"'
                   f' opacity=".55"/>')
    s += SL(Z_DAL, polovicy(880, "#8a6342"))
    # окно в морозных узорах
    s += SL(Z_DAL, okno_izby(1480, 120, 380, 420, t, None, .85, False, True))
    # ДОСКА ОБЪЯВЛЕНИЙ на пол-кадра
    dx, dy, dw, dh = 200, 140, 1040, 600
    s += SL(Z_SRED, f'<rect x="{dx-16:.0f}" y="{dy-16:.0f}" width="{dw+32:.0f}"'
                    f' height="{dh+32:.0f}" rx="10" fill="#8a6342" stroke="{K}"'
                    f' stroke-width="7"/>'
                    f'<rect x="{dx:.0f}" y="{dy:.0f}" width="{dw:.0f}" height="{dh:.0f}"'
                    f' fill="#3f5a4a" stroke="{K}" stroke-width="5"/>')
    # расписание без текста
    s += SL(Z_SRED, f'<rect x="{dx+40:.0f}" y="{dy+50:.0f}" width="300" height="400"'
                    f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{dx+66:.0f},{dy+100+i*40:.0f} q{60:.0f},{-6:.0f}'
                        f' {120:.0f},0 q{40:.0f},{6:.0f} {66:.0f},{-2:.0f}" fill="none"'
                        f' stroke="#8a7a62" stroke-width="4"/>')
    # стенгазета с нарисованной ёлкой
    s += SL(Z_SRED, f'<rect x="{dx+380:.0f}" y="{dy+40:.0f}" width="280" height="240"'
                    f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{dx+520:.0f},{dy+80:.0f} l{70:.0f},{120:.0f} l{-140:.0f},0 Z"'
                    f' fill="#3c5a3a" stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M{dx+520:.0f},{dy+130:.0f} l{54:.0f},{90:.0f} l{-108:.0f},0 Z"'
                    f' fill="#49693a" stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="{dx+510:.0f}" y="{dy+218:.0f}" width="20" height="26"'
                    f' fill="#6b4428"/>')
    # БОЛЬШОЙ ЛИСТОК: пруд и восклицательный знак
    s += SL(Z_SRED, f'<rect x="{dx+380:.0f}" y="{dy+310:.0f}" width="560" height="240"'
                    f' rx="8" fill="#fff4d8" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="{dx+560:.0f}" cy="{dy+440:.0f}" rx="130" ry="60"'
                    f' fill="#9fc4d8" stroke="#6f7a84" stroke-width="5"/>'
                    f'<path d="M{dx+450:.0f},{dy+470:.0f} q{110:.0f},{-30:.0f} {220:.0f},{4:.0f}"'
                    f' fill="none" stroke="#eaf6ff" stroke-width="7"/>'
                    f'<rect x="{dx+780:.0f}" y="{dy+350:.0f}" width="40" height="110"'
                    f' rx="12" fill="#c8301f"/>'
                    f'<circle cx="{dx+800:.0f}" cy="{dy+492:.0f}" r="22" fill="#c8301f"/>')
    s += SL(Z_SRED, f'<rect x="{dx+700:.0f}" y="{dy+40:.0f}" width="220" height="240"'
                    f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{dx+726:.0f},{dy+90+i*30:.0f} q{50:.0f},{-6:.0f}'
                        f' {100:.0f},0 q{30:.0f},{6:.0f} {60:.0f},{-2:.0f}" fill="none"'
                        f' stroke="#8a7a62" stroke-width="3.6"/>')
    # УЧИТЕЛЬНИЦА с указкой, трое школьников
    ux, uy, uh = 1420, 1000, 660
    stuk = abs(A.w(t, 1.1, .0))
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#3f3a4a", kant="#ffd9a8", ph=.2))
    r1, (e1x, e1y), _ = _ruka(ux, uy, uh, -1, uh * .32, -4 - 16 * stuk, t,
                              "#3f3a4a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(ux, uy, uh, 1, uh * .22, -34, t, "#3f3a4a", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + r2
            + f'<path d="M{e1x:.0f},{e1y:.0f} L{dx+820:.0f},{dy+430+12*stuk:.0f}"'
              f' stroke="#8a6342" stroke-width="8" stroke-linecap="round"/>')
    for i, (sx_, sy_, sh_, col) in enumerate(((560, 1066, 480, "#3f5a6a"),
                                              (740, 1060, 500, "#6b3a6a"),
                                              (920, 1070, 460, "#4a6a3a"))):
        kiv = 4.0 * A.w(t, 1.5, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({kiv:.1f} {sx_:.0f} {sy_-sh_*.5:.0f})">'
                + figura(sx_, sy_, sh_, t, col=col, kant="#ffd9a8", ph=i * .3) + '</g>')
        s += SL(Z_SRED, ten(sx_, sy_ + 5, 88, 15, .35))
    s += SL(Z_SRED, ten(ux, uy + 6, 120, 20, .4))
    # батарея, фикус, вешалка с пальто, звонок
    s += SL(Z_SRED, f'<rect x="60" y="780" width="280" height="150" rx="8"'
                    f' fill="#c9ccd1" stroke="{K}" stroke-width="4.5"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{76+i*38:.0f}" y="790" width="22" height="130"'
                        f' rx="6" fill="#dde3e8" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<path d="M1700,1020 h150 l-16,-90 h-118 Z" fill="#a8743c"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(7):
        a = -1.2 + i * .4
        s += SL(Z_SRED, f'<path d="M1775,930 q{70*math.sin(a):.0f},{-60:.0f}'
                        f' {110*math.sin(a):.0f},{-150:.0f} q{30:.0f},{40:.0f}'
                        f' {-50*math.sin(a):.0f},{150:.0f} Z" fill="#56763f"'
                        f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="1380" y="150" width="20" height="300" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    for i, (px_, col) in enumerate(((1330, "#3f4a7a"), (1420, "#6b3a2a"))):
        s += SL(Z_SRED, f'<path d="M{px_:.0f},300 q{40:.0f},{-30:.0f} {80:.0f},0'
                        f' l{10:.0f},{200:.0f} q{-50:.0f},{20:.0f} {-100:.0f},0 Z"'
                        f' fill="{col}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(960, 90, t, 1.3, True) + teplo(960, 110, 300, 240, .40))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.40)
    return s


def blestyaschiy_led_i_gradusnik(t):
    """Пруд блестит на солнце и манит, а на столбе у берега большой уличный
    градусник: столбик стоит чуть ниже черты и опускается ниже, пока летят
    листки численника — и только тогда на льду встаёт галочка."""
    rnd = random.Random(2004)
    s = nebo("den", t, False, 239)
    s += oblaka(t, 150, 4, 139, .34, "#ffe9c8")
    s += SL(Z_NEBO, f'<circle cx="640" cy="200" r="104" fill="#ffe9ac" opacity=".45"/>'
                    f'<circle cx="640" cy="200" r="60" fill="#fff4d8" opacity=".9"/>')
    s += SL(Z_DAL, ulica_dal(1160, 380, 780, t, True, 103))
    s += SL(Z_DAL, izba_snaruzhi(260, 400, 280, t, True, True, 59)
            + dym(288, 256, t, 6, .22, 250, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(470, 241, False))
    s += SL(Z_SRED, f'<rect x="0" y="560" width="{W}" height="520" fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(960, 760, 820, 180, t, .2, .0, .9, .35))
    bl = (t * .35) % 1.0
    s += SL(Z_SRED, f'<ellipse cx="{-200+2300*bl:.0f}" cy="700" rx="360" ry="60"'
                    f' fill="#ffffff" opacity="{.18+.14*math.sin(bl*3.14):.2f}"/>')
    # СТОЛБ с градусником
    s += SL(Z_SRED, f'<rect x="1440" y="300" width="40" height="740" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="5"/>')
    stolb = .55 - .30 * A.ease(A.seg(t, .6, 2.6))
    s += SL(Z_SRED, gradusnik_ulichnyy(1560, 640, 1.5, t, .2, stolb))
    s += SL(Z_SRED, f'<path d="M1500,440 h130" stroke="#c8301f" stroke-width="6"'
                    f' opacity=".9"/>')
    # листки численника отлетают
    for i in range(3):
        d = ((t * .5 + i * .33) % 1.0)
        s += SL(Z_LETIT, f'<rect x="{1380-300*d:.0f}" y="{420+300*d*d:.0f}" width="90"'
                         f' height="120" rx="6" fill="#f2ead6" opacity="{(1-d)*.85:.2f}"'
                         f' transform="rotate({-d*160:.0f} {1425-300*d:.0f}'
                         f' {480+300*d*d:.0f})" stroke="{K}" stroke-width="3"/>')
    # ГАЛОЧКА на льду в конце
    gal = A.out(A.seg(t, 2.8, .8))
    if gal > .02:
        s += SL(Z_SRED, f'<path d="M620,820 l{90*gal:.0f},{80*gal:.0f}'
                        f' l{180*gal:.0f},{-200*gal:.0f}" fill="none" stroke="#3f8a4a"'
                        f' stroke-width="24" stroke-linecap="round" opacity="{gal:.2f}"/>')
    # ДЕД показывает на градусник, ВНУК тянется ко льду
    dx, dy, dh = 980, 1050, 680
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#4a4038", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, 1, dh * .34, -22, t, "#4a4038", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, -1, dh * .26, 46, t, "#4a4038", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x + 14, e1y - 6, 1.0, -20, "#6b4428", t, .2) + r2)
    vx, vy, vh = 780, 1066, 440
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#3f5a6a", kant="#ffd9a8",
                           shapka=True, ph=.6, naklon=3.0))
    s += SL(Z_SRED, f'<path d="M{e2x:.0f},{e2y:.0f} L{vx+60:.0f},{vy-vh*.54:.0f}"'
                    f' stroke="#4a4038" stroke-width="14" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(dx - 36, dy - dh * .80, t, .3, 1.0, .5)
            + para_izo_rta(vx - 24, vy - vh * .80, t, .8, .8, .45))
    s += SL(Z_SRED, ten(dx, dy + 6, 126, 21, .4) + ten(vx, vy + 6, 92, 16, .4))
    s += SL(Z_SRED, mostki(180, 600, 420, t, True, 170))
    s += SL(Z_SRED, goloe_derevo_ld(1800, 1000, 480, t, 241, 7, True))
    s += SL(Z_SRED, sanki_derev(480, 1050, .85, t, .3, True))
    s += SL(Z_SRED, kot(1300, 1046, t, 1.3, "#6b5230", False))
    s += SL(Z_SRED, kamysh(60, 1040, 200, t, 6, 251, True))
    s += SL(Z_SRED, inej_mel(239, 44, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def alleya_u_gorodskogo_pruda(t):
    """Аллея городского парка вдоль пруда: слева ограда и лёд, справа скамейки
    и липы. Бабушка переводит внука на дальнюю от воды сторону, внук
    оглядывается на пруд."""
    rnd = random.Random(2005)
    s = nebo("sumer", t, False, 251)
    s += oblaka(t, 140, 5, 149, .40)
    s += SL(Z_DAL, panelka(1500, 420, 420, t, 5, True, 29))
    s += SL(Z_DAL, goloe_derevo_ld(1180, 560, 460, t, 251, 8, True)
            + goloe_derevo_ld(1400, 580, 400, t, 257, 7, True))
    # пруд слева и ограда
    s += SL(Z_SRED, f'<rect x="0" y="420" width="760" height="660" fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(340, 700, 340, 200, t, .2, .0, .85, .3))
    s += SL(Z_SRED, f'<rect x="700" y="400" width="26" height="680" fill="{CHUGUN}"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<rect x="{620:.0f}" y="{420+i*56:.0f}" width="110" height="12"'
                        f' rx="5" fill="{CHUGUN}" opacity=".9"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{560+i*26:.0f}" y="400" width="12" height="660"'
                        f' fill="{CHUGUN}" opacity=".8"/>')
    # аллея
    s += SL(Z_SRED, f'<path d="M760,420 L1920,440 L1920,1080 L700,1080 Z"'
                    f' fill="#9a8a72"/>')
    for i in range(14):
        s += SL(Z_SRED, f'<path d="M{780+i*90:.0f},440 L{700+i*120:.0f},1080"'
                        f' stroke="#8a7a62" stroke-width="4" opacity=".4"/>')
    # фонари
    for i, (fx, fy) in enumerate(((860, 380), (1180, 330), (1560, 300))):
        s += SL(Z_SRED, f'<rect x="{fx:.0f}" y="{fy:.0f}" width="20" height="{700-fy*.5:.0f}"'
                        f' fill="{BETON2}" stroke="{K}" stroke-width="3.6"/>')
        s += SL(Z_SRED, lampa(fx + 10, fy, t, 1.0 + i * .1, True)
                + teplo(fx + 10, fy + 10, 180, 150, .32))
    # БАБУШКА переводит ВНУКА на дальнюю сторону
    per = A.ease(A.seg(t, .5, 2.6))
    bx, by, bh = 1020 + 340 * per, 1040, 650
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd9a8", ph=.3))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, -1, bh * .26, 32, t, "#4a3a52", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, 1, bh * .24, 54, t, "#4a3a52", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    kch = 7 * A.w(t, 1.2, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {e2x:.0f} {e2y:.0f})">'
                    f'<rect x="{e2x-40:.0f}" y="{e2y+8:.0f}" width="80" height="66"'
                    f' rx="8" fill="#8a2f22" stroke="{K}" stroke-width="4"/></g>')
    vx, vy, vh = bx - 190, 1056, 440
    ogl = A.ease(A.seg(t, 1.2, 1.2))
    s += SL(Z_SRED, f'<g transform="rotate({-6*ogl:.1f} {vx:.0f} {vy-vh*.5:.0f})">'
            + figura(vx, vy, vh, t, col="#c8301f", kant="#ffd9a8", shapka=True, ph=.6)
            + '</g>')
    r3, (e3x, e3y), _ = _ruka(vx, vy, vh, 1, vh * .26, 28, t, "#c8301f", "#ffd9a8", .4, 4)
    s += SL(Z_SRED, r3 + varezhka(e3x + 8, e3y + 10, .9, 14, TKAN, t, .4)
            + f'<path d="M{e3x:.0f},{e3y:.0f} L{e1x:.0f},{e1y:.0f}" stroke="#4a3a52"'
              f' stroke-width="12" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(bx - 30, by - bh * .80, t, .4, .9, .45)
            + para_izo_rta(vx - 24, vy - vh * .80, t, .9, .8, .45))
    s += SL(Z_SRED, ten(bx, by + 6, 120, 20, .4) + ten(vx, vy + 6, 92, 16, .4))
    # скамейки, урна, голуби, утки у ограды, киоск без вывески
    for i, sx_ in enumerate((880, 1240, 1640)):
        s += SL(Z_SRED, f'<rect x="{sx_:.0f}" y="{860+i*20:.0f}" width="260" height="20"'
                        f' rx="6" fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                        f'<rect x="{sx_:.0f}" y="{800+i*20:.0f}" width="260" height="18"'
                        f' rx="6" fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                        f'<rect x="{sx_+16:.0f}" y="{880+i*20:.0f}" width="20" height="90"'
                        f' fill="{BETON2}" stroke="{K}" stroke-width="3.4"/>'
                        f'<rect x="{sx_+220:.0f}" y="{880+i*20:.0f}" width="20" height="90"'
                        f' fill="{BETON2}" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="1780" y="900" width="100" height="130" rx="10"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="4.5"/>')
    for i, (gx, gy) in enumerate(((940, 1020), (1040, 1050), (1140, 1010))):
        s += SL(Z_SRED, ptica(gx, gy, t, 1.6, "#9aa3a8", i * .3, "#6f7a84"))
    for i, (ux, uy) in enumerate(((300, 1000), (420, 1030), (540, 990))):
        s += SL(Z_SRED, f'<ellipse cx="{ux:.0f}" cy="{uy:.0f}" rx="44" ry="24"'
                        f' fill="#4a4038" stroke="{K}" stroke-width="3.4"/>'
                        f'<circle cx="{ux+34:.0f}" cy="{uy-22:.0f}" r="16" fill="#4a4038"'
                        f' stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{ux+48:.0f},{uy-24:.0f} l20,5 l-20,6 Z" fill="{ZOL}"/>')
    s += SL(Z_SRED, f'<rect x="60" y="620" width="300" height="240" rx="8"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="90" y="660" width="240" height="120" rx="6"'
                    f' fill="#8aa8b4" opacity=".6" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="40" y="596" width="340" height="30" rx="6"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_LETIT, sneg_letit(t, 16, 53, .32, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def korotkiy_put_cherez_prud(t):
    """Пруд сверху, как карта: через лёд мигает красным короткий путь от дома
    до магазина, вокруг по берегу загорается зелёный. Рыбак с ящиком и
    подросток поворачивают на зелёный, бабушка говорит в трубку у окна."""
    rnd = random.Random(2006)
    s = nebo("sumer", t, True, 257)
    s += SL(Z_DAL, ulica_dal(60, 240, 900, t, True, 107))
    s += SL(Z_SRED, _merzlaya_zemlya(300, 263, False))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="680" rx="700" ry="300" fill="url(#led)"'
                    f' stroke="#eaf6ff" stroke-width="10"/>')
    s += SL(Z_SRED, korka_lda(960, 680, 660, 280, t, .2, .0, .75, .35))
    # КРАСНЫЙ ПУНКТИР через лёд — мигает
    mig = .4 + .6 * abs(A.w(t, .8, .0))
    for i in range(12):
        s += SL(Z_SRED, f'<rect x="{430+i*95:.0f}" y="{660+((i*5)%3-1)*26:.0f}"'
                        f' width="56" height="14" rx="7" fill="#d6452a"'
                        f' opacity="{mig:.2f}"/>')
    # ЗЕЛЁНЫЙ ПУНКТИР по берегу
    zel = A.ease(A.seg(t, 1.0, 1.6))
    for i in range(16):
        a = 3.14 + i * .22
        zx_ = 960 + 790 * math.cos(a)
        zy_ = 690 + 350 * math.sin(a)
        if i / 16.0 > zel:
            break
        s += SL(Z_SRED, f'<rect x="{zx_:.0f}" y="{zy_:.0f}" width="50" height="14"'
                        f' rx="7" fill="#3f8a4a" opacity=".92"'
                        f' transform="rotate({math.degrees(a)+90:.0f} {zx_:.0f} {zy_:.0f})"/>')
    # дом с окном и магазин
    s += SL(Z_SRED, izba_snaruzhi(250, 420, 340, t, True, True, 61)
            + dym(286, 240, t, 6, .22, 260, .42, "#d7dee6", 1.0))
    s += SL(Z_SRED, f'<rect x="1480" y="300" width="400" height="260" rx="8"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="1520" y="360" width="320" height="150" rx="6"'
                    f' fill="#8aa8b4" opacity=".6" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="1460" y="276" width="440" height="30" rx="6"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, lampa(1680, 300, t, 1.0, True) + teplo(1680, 310, 180, 150, .34))
    # БАБУШКА-силуэт в окне с трубкой
    s += SL(Z_SRED, f'<rect x="320" y="470" width="190" height="170" rx="6"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<g opacity=".92">'
            + figura(415, 640, 300, t, col="#4a3a52", kant="#ffd98a", platok=True, ph=.3)
            + '</g>')
    rk, (ex, ey), _ = _ruka(415, 640, 300, 1, 300 * .28, -40, t, "#4a3a52", "#ffd98a", .3, 4)
    s += SL(Z_SRED, rk + f'<rect x="{ex-14:.0f}" y="{ey-18:.0f}" width="28" height="48"'
                         f' rx="10" fill="#23242a" stroke="{K}" stroke-width="3"/>'
                         f'<path d="M{ex:.0f},{ey+30:.0f} q{30:.0f},{40:.0f} {-10:.0f},{70:.0f}"'
                         f' fill="none" stroke="#23242a" stroke-width="5"/>')
    # РЫБАК с ящиком и ПОДРОСТОК поворачивают на зелёный
    pov = A.ease(A.seg(t, 1.4, 1.6))
    rx_, ry_, rh = 760 - 140 * pov, 1046, 640
    s += SL(Z_SRED, figura(rx_, ry_, rh, t, col="#3f4a3a", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(rx_, ry_, rh, -1, rh * .24, -30, t, "#3f4a3a", "#ffd9a8", .2, 4)
    s += SL(Z_SRED, r1 + yaschik_rybaka(e1x - 40, e1y + 60, .72, t, .0, .2))
    px_, py_, ph_ = 1060 + 160 * pov, 1056, 560
    s += SL(Z_SRED, figura(px_, py_, ph_, t, col="#6b3a6a", kant="#ffd9a8",
                           shapka=True, ph=.6))
    s += SL(Z_SRED, f'<path d="M{px_-70:.0f},{py_-ph_*.60:.0f} q{70:.0f},{-20:.0f}'
                    f' {140:.0f},0 l{10:.0f},{150:.0f} q{-80:.0f},{20:.0f} {-160:.0f},0 Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, para_izo_rta(rx_ - 34, ry_ - rh * .80, t, .3, 1.0, .5)
            + para_izo_rta(px_ - 28, py_ - ph_ * .80, t, .8, .9, .45))
    s += SL(Z_SRED, ten(rx_, ry_ + 6, 124, 21, .4) + ten(px_, py_ + 6, 108, 18, .4))
    s += SL(Z_SRED, kamysh(120, 980, 220, t, 7, 263, True)
            + kamysh(1840, 1000, 230, t, 7, 269, True))
    s += SL(Z_SRED, goloe_derevo_ld(1700, 1050, 420, t, 263, 6, True))
    s += SL(Z_SRED, dvorovye_veschi(400, 1070, 300, t, 257, ["kadka", "korzina"]))
    s += SL(Z_LETIT, sneg_letit(t, 18, 59, .34, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def rybak_na_mostkah(t):
    """Мостки над полыньёй у берега на пол-кадра: рыбак в ватнике сидит на
    складном стульчике, обеими руками держит длинную удочку, поплавок стоит
    в чёрной воде у кромки. Дальше от берега лёд пуст и нетронут."""
    rnd = random.Random(2007)
    s = nebo("rassv", t, False, 269)
    s += oblaka(t, 140, 5, 151, .38)
    s += SL(Z_DAL, ulica_dal(1180, 300, 740, t, True, 109))
    s += SL(Z_DAL, goloe_derevo_ld(360, 340, 360, t, 269, 6, True))
    s += SL(Z_DAL, izba_snaruzhi(1520, 320, 260, t, True, True, 67)
            + dym(1548, 180, t, 6, .22, 240, .40, "#d7dee6", .9))
    s += SL(Z_SRED, f'<rect x="0" y="420" width="{W}" height="660" fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(1300, 620, 560, 160, t, .4, .0, .85, .3))
    # ПОЛЫНЬЯ у берега и мостки на пол-кадра
    s += SL(Z_SRED, prorub(760, 800, 230, t, .1, True))
    s += SL(Z_SRED, mostki(120, 700, 900, t, True, 320))
    # РЫБАК на складном стульчике
    rx_, ry_, rh = 560, 700, 420
    s += SL(Z_SRED, f'<path d="M{rx_-80:.0f},{ry_:.0f} l{70:.0f},{-120:.0f}'
                    f' M{rx_+80:.0f},{ry_:.0f} l{-70:.0f},{-110:.0f}" stroke="{ZHELEZ}"'
                    f' stroke-width="11" fill="none"/>'
                    f'<rect x="{rx_-90:.0f}" y="{ry_-126:.0f}" width="180" height="22"'
                    f' rx="6" fill="#3f4a3a" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(rx_, ry_ - 92, rh, t, col="#3f4a3a", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(rx_, ry_ - 92, rh, 1, rh * .30, 14, t,
                              "#3f4a3a", "#ffd9a8", .2, 3)
    r2, (e2x, e2y), _ = _ruka(rx_, ry_ - 92, rh, -1, rh * .24, 24, t,
                              "#3f4a3a", "#ffd9a8", .6, 3)
    s += SL(Z_SRED, r1 + r2)
    drozh = 6 * A.w(t, 2.6, .1)
    s += SL(Z_SRED, f'<path d="M{e2x:.0f},{e2y:.0f} L{760:.0f},{560+drozh:.0f}"'
                    f' stroke="#8a6342" stroke-width="15" stroke-linecap="round"/>'
                    f'<path d="M{760:.0f},{560+drozh:.0f} L{780:.0f},{770:.0f}"'
                    f' fill="none" stroke="#cfd6db" stroke-width="2.6"/>')
    popl = 8 * A.w(t, 1.5, .2)
    s += SL(Z_SRED, f'<ellipse cx="782" cy="{778+popl:.0f}" rx="11" ry="22"'
                    f' fill="#c8301f" stroke="{K}" stroke-width="3"/>'
                    f'<ellipse cx="782" cy="{766+popl:.0f}" rx="9" ry="10"'
                    f' fill="#f4f1e8" stroke="{K}" stroke-width="2.4"/>')
    # ноги в сапогах стоят на досках
    s += SL(Z_SRED, f'<path d="M{rx_-50:.0f},{ry_-120:.0f} l{-20:.0f},{104:.0f}'
                    f' l{70:.0f},{10:.0f} l{10:.0f},{-110:.0f} Z" fill="#3f4a3a"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{rx_-74:.0f},{ry_-26:.0f} h{90:.0f} q{18:.0f},{10:.0f}'
                    f' {4:.0f},{28:.0f} h{-100:.0f} Z" fill="#23242a" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    s += SL(Z_SRED, para_izo_rta(rx_ - 34, ry_ - 92 - rh * .80, t, .3, 1.0, .5))
    # ящик, термос с паром, банка с наживкой, сачок, кот
    s += SL(Z_SRED, yaschik_rybaka(300, 700, 1.0, t, .35, .3))
    s += SL(Z_SRED, f'<rect x="420" y="596" width="62" height="110" rx="12"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="414" y="580" width="74" height="22" rx="6"'
                    f' fill="#c9ccd1" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, par(452, 560, t, 4, .5, 150, .45, 1.0))
    s += SL(Z_SRED, banka_moloka(880, 700, .5, t, False, .5, "#6b5230"))
    s += SL(Z_SRED, f'<g transform="rotate(16 960 700)">'
                    f'<rect x="954" y="420" width="13" height="280" rx="6"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3"/>'
                    f'<ellipse cx="961" cy="400" rx="66" ry="42" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="8"/></g>')
    s += SL(Z_SRED, kot(1120, 700, t, 1.5, "#6b5230", False))
    s += SL(Z_SRED, snast_kruchki(1420, 940, t, 1.0, 6, .2))
    s += SL(Z_SRED, kamysh(80, 900, 220, t, 7, 271, True)
            + kamysh(1860, 940, 230, t, 7, 277, True))
    s += SL(Z_SRED, inej_mel(269, 40, 900, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def krynka_i_moneta(t):
    """Плашка третьего запрета: край стола в сенях, на нём запотевшая крынка
    молока под полотняной салфеткой. Через порог тянется рука соседки с
    монетой на варежке; хозяйка придвигает крынку к себе и отводит ладонь."""
    rnd = random.Random(2008)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    s += SL(Z_DAL, brevna(0, 0, W, 820, 84, 1))
    s += SL(Z_DAL, dver(1360, 180, 420, 700, .32, "url(#derev)", True, True))
    s += SL(Z_DAL, f'<rect x="1380" y="220" width="200" height="620" fill="#2b3550"'
                   f' opacity=".9"/>')
    s += SL(Z_DAL, sneg_letit(t, 14, 61, .4, .5))
    s += SL(Z_SRED, polovicy(880, "#6b4428"))
    # СТОЛ в сенях
    s += SL(Z_SRED, stol(60, 700, 900, 40, True))
    s += SL(Z_SRED, f'<rect x="60" y="700" width="900" height="16" fill="#8a6342"'
                    f' opacity=".9"/>')
    # КРЫНКА под салфеткой — главный предмет
    s += SL(Z_SRED, krynka_moloka(520, 740, 3.0, t, True, True, .2))
    for i in range(9):                 # запотевшие капли
        s += SL(Z_SRED, f'<ellipse cx="{420+i*26:.0f}" cy="{520+((i*7)%5)*30:.0f}"'
                        f' rx="5" ry="8" fill="#eef6ff" opacity=".6"/>')
    # ПОДОЙНИК, сито, лавка рядом
    s += SL(Z_SRED, podoynik(820, 700, 1.0, t, True, .4))
    s += SL(Z_SRED, f'<ellipse cx="180" cy="690" rx="90" ry="26" fill="#b9a37a"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="180" cy="678" rx="76" ry="20" fill="#d8cbb0"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M{130+i*20:.0f},664 l0,26" stroke="#8a7a52"'
                        f' stroke-width="3" opacity=".8"/>')
    s += SL(Z_SRED, lavka(1060, 980, 320))
    # ХОЗЯЙКА: левой придвигает крынку, правой отводит ладонь
    hx, hy, hh = 700, 1056, 700
    prid = A.ease(A.seg(t, .6, 1.2))
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .32, -16 + 10 * prid, t,
                              "#8a2f22", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .30, -22, t, "#8a2f22", "#ffd98a", .6, 5)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{hx-110:.0f},{hy-hh*.44:.0f} q{110:.0f},{-26:.0f}'
                    f' {220:.0f},0 l0,{hh*.30:.0f} q{-110:.0f},{26:.0f} {-220:.0f},0 Z"'
                    f' fill="{RUSH}" opacity=".9" stroke="{K}" stroke-width="4"/>')
    # РУКА СОСЕДКИ через порог с монетой на варежке (рука ничья: человека нет)
    otv = A.ease(A.seg(t, 1.4, 1.2))
    ruk, (kx_, ky_) = rukav(1760, 620, 420, 196 + 10 * otv, t, "#5a4a3a",
                            "#cfe4f5", .3, 4, True)
    s += SL(Z_SRED, ruk + varezhka(kx_, ky_ + 6, 1.3, 6, "#6b4428", t, .3))
    bl = .5 + .5 * A.w(t, 2.4, .1)
    s += SL(Z_SRED, f'<ellipse cx="{kx_:.0f}" cy="{ky_-16:.0f}" rx="34" ry="12"'
                    f' fill="url(#med)" stroke="{K}" stroke-width="3.6"/>'
                    f'<ellipse cx="{kx_-8:.0f}" cy="{ky_-20:.0f}" rx="13" ry="5"'
                    f' fill="#ffe9ac" opacity="{bl:.2f}"/>')
    # СЕНИ ОБЖИТЫ: полка над столом, травы под потолком, упряжь, кадки
    s += SL(Z_SRED, polka_s_bankami(380, 420, 560, t, 19, 5, False))
    for i, (px_, ph2) in enumerate(((560, .2), (700, .6), (840, .9))):
        s += SL(Z_SRED, puchok_trav(px_, 180, .9, t, ph2, 23 + i, "#8a7a4a"))
    s += SL(Z_SRED, f'<path d="M1100,180 q{90:.0f},{120:.0f} {10:.0f},{250:.0f}'
                    f' q{-70:.0f},{-130:.0f} {-10:.0f},{-250:.0f} Z" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1104,200 q{70:.0f},{104:.0f} {6:.0f},{216:.0f}"'
                    f' fill="none" stroke="#8a6342" stroke-width="8"/>')
    for i, (kx2, ky2) in enumerate(((1240, 880), (1340, 900))):
        s += SL(Z_SRED, f'<path d="M{kx2-46:.0f},{ky2-96:.0f} h{92:.0f} l{-8:.0f},{96:.0f}'
                        f' h{-76:.0f} Z" fill="url(#derev)" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{kx2:.0f}" cy="{ky2-96:.0f}" rx="46" ry="13"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="420" y="250" width="16" height="130" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<path d="M360,380 q{68:.0f},{-30:.0f} {136:.0f},0 l{12:.0f},{200:.0f}'
                    f' q{-80:.0f},{24:.0f} {-160:.0f},0 Z" fill="#3f4a3a" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    s += SL(Z_SRED, kot(1180, 980, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, utvar_izby(80, 300, 340, t, 11))
    s += SL(Z_SRED, polka_s_bankami(1080, 360, 500, t, 17, 4, False))
    s += SL(Z_SRED, lampa(240, 180, t, 1.3, False) + teplo(240, 190, 320, 270, .45))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .55))
    s += vinetka(.44)
    return s


def dva_puti_krynki(t):
    """Кадр надвое: слева крынка уходит за ворота в чужих руках и следом
    уплывают каравай, масло и баранки; справа крынка остаётся на столе,
    корова жуёт сено, а каждый день на столе новая полная крынка."""
    rnd = random.Random(2009)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    # ЛЕВАЯ ПОЛОВИНА: двор, ворота, уплывающие припасы
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W*.5:.0f}" height="{H}" fill="#3f4a56"/>')
    s += SL(Z_DAL, nebo("sumer", t, False, 271))
    s += SL(Z_DAL, f'<rect x="{W*.5:.0f}" y="0" width="{W*.5:.0f}" height="{H}"'
                   f' fill="#2b2419"/>')
    s += SL(Z_DAL, brevna(W // 2, 0, W // 2, 820, 84, 2))
    s += SL(Z_SRED, _merzlaya_zemlya(620, 277, False))
    s += SL(Z_SRED, f'<rect x="{W*.5:.0f}" y="820" width="{W*.5:.0f}" height="260"'
                    f' fill="#7a5436"/>' + polovicy(820, "#6b4428"))
    # ворота и уходящая крынка
    s += SL(Z_SRED, kalitka_rez(380, 380, 320, 400, t, .55, True))
    uh = A.ease(A.seg(t, .4, 2.4))
    ruk, (kx_, ky_) = rukav(240 - 160 * uh, 600, 240, -8, t, "#5a4a3a",
                            "#cfe4f5", .2, 4, True)
    s += SL(Z_SRED, ruk + krynka_moloka(kx_ + 10, ky_ + 70, 1.1, t, True, True, .3))
    for i, (px_, py_) in enumerate(((560, 760), (640, 860), (720, 940))):
        d = A.ease(A.seg(t, .6 + i * .35, 1.8))
        s += SL(Z_SRED, f'<g opacity="{1-d*.8:.2f}" transform="translate({-460*d:.0f},'
                        f'{-40*d:.0f})">'
                + (karavay(px_, py_, .8, True) if i == 0 else
                   (f'<rect x="{px_-50:.0f}" y="{py_-60:.0f}" width="100" height="60"'
                    f' rx="8" fill="#f2e2b8" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{px_-50:.0f},{py_-40:.0f} h100" stroke="#d8c7a4"'
                    f' stroke-width="5"/>' if i == 1 else
                    "".join(f'<circle cx="{px_+k*26:.0f}" cy="{py_-30:.0f}" r="26"'
                            f' fill="none" stroke="#c8a05a" stroke-width="12"/>'
                            for k in range(3))))
                + '</g>')
    hx, hy, hh = 820, 1000, 600
    s += SL(Z_SRED, f'<rect x="700" y="1000" width="320" height="26" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, ph=.4, naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .26, 70, t, "#4a3a52", "#cfe4f5", .2, 3)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .26, 72, t, "#4a3a52", "#cfe4f5", .6, 3)
    s += SL(Z_SRED, r1 + r2)
    # ПРАВАЯ ПОЛОВИНА: стол, крынка, окно в хлев с коровой, численник
    s += SL(Z_SRED, stol(1060, 760, 800, 40, True))
    s += SL(Z_SRED, krynka_moloka(1300, 760, 1.5, t, True, True, .1))
    s += SL(Z_SRED, karavay(1620, 756, .8, True))
    s += SL(Z_SRED, okno_izby(1420, 180, 420, 320, t, None, .2, True, True))
    # корова за окном
    s += SL(Z_SRED, f'<ellipse cx="1620" cy="360" rx="130" ry="70" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="1570" cy="340" rx="42" ry="30" fill="#6b4428"'
                    f' opacity=".9"/>'
                    f'<ellipse cx="1660" cy="380" rx="34" ry="24" fill="#6b4428"'
                    f' opacity=".9"/>'
                    f'<circle cx="1500" cy="320" r="44" fill="#e8e2d6" stroke="{K}"'
                    f' stroke-width="4.5"/>'
                    f'<path d="M1470,286 l{-16:.0f},{-26:.0f} M1530,286 l{16:.0f},{-26:.0f}"'
                    f' stroke="#c9bfa6" stroke-width="9"/>'
                    f'<circle cx="1488" cy="314" r="5" fill="{K}"/>')
    zhuy = 6 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<path d="M1460,{348+zhuy:.0f} q{22:.0f},{14:.0f} {44:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#8a7a62" stroke-width="5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M{1430-i*8:.0f},{360+i*6:.0f} l{-40:.0f},{-20:.0f}"'
                        f' stroke="#b9a37a" stroke-width="5" opacity=".9"/>')
    # численник: листки летят всю зиму
    for i in range(4):
        d = ((t * .6 + i * .25) % 1.0)
        s += SL(Z_LETIT, f'<rect x="{1120+200*d:.0f}" y="{300+300*d*d:.0f}" width="84"'
                         f' height="110" rx="6" fill="#f2ead6" opacity="{(1-d)*.85:.2f}"'
                         f' transform="rotate({d*150:.0f} {1162+200*d:.0f}'
                         f' {355+300*d*d:.0f})" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<rect x="1080" y="240" width="140" height="180" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1080" y="240" width="140" height="38" rx="8"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, polka_s_bankami(1060, 540, 420, t, 29, 4, False))
    s += SL(Z_SRED, dvorovye_veschi(120, 1066, 420, t, 271, ["vedro", "kadka", "korzina"]))
    s += SL(Z_SRED, lampa(1760, 560, t, 1.2, False) + teplo(1760, 570, 260, 220, .40))
    s += SL(Z_SRED, kot(1180, 1040, t, 1.4, "#3b3430", False))
    s += SL(Z_PERED, f'<rect x="{W*.5-7:.0f}" y="0" width="14" height="{H}"'
                     f' fill="#1d1611" opacity=".9"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def polnyy_podoynik(t):
    """Хлев в тёплом свете фонаря: хозяйка на скамеечке держит обеими руками
    подойник, полный до краёв с шапкой пены. В проёме приоткрытой двери —
    настоящее молоко, льющееся в ведро."""
    rnd = random.Random(2010)
    s = (f'<rect width="{W}" height="{H}" fill="#241c16"/>')
    s += SL(Z_DAL, brevna(0, 0, W, 860, 88, 3))
    s += SL(Z_DAL, svody(t, "#3f352c", 3))
    s += SL(Z_SRED, f'<rect x="0" y="860" width="{W}" height="220" fill="#6b5230"/>')
    for i in range(30):
        s += SL(Z_SRED, f'<path d="M{rnd.uniform(-20,1940):.0f},{rnd.uniform(880,1070):.0f}'
                        f' l{rnd.uniform(26,60):.0f},{rnd.uniform(-14,10):.0f}"'
                        f' stroke="#b9a37a" stroke-width="4" opacity=".7"/>')
    # ДВЕРЬ ХЛЕВА с проёмом (стоймя 760x420 — по таблице)
    px, py, pw, ph_ = 1080, 300, 800, 620
    put = kontur_proema(px, py, pw, ph_, "pryam")
    dv = (f'<path d="{put}" fill="#8aa8b4"/>')
    dv += (f'<path d="{put}" fill="#cfe4f5" opacity=".35"/>')
    dv += mesto_stoka(px + 10, py + 150, 780, 320, "pryam")
    dv += (f'<path d="{put}" fill="none" stroke="#54351f" stroke-width="22"/>')
    s += SL(Z_SRED, dv)
    s += SL(Z_SRED, f'<rect x="{px-60:.0f}" y="{py-40:.0f}" width="56" height="{ph_+80:.0f}"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="5"/>')
    # КОРОВА и хозяйка с подойником
    s += SL(Z_SRED, f'<ellipse cx="760" cy="620" rx="330" ry="190" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<ellipse cx="640" cy="580" rx="100" ry="70" fill="#6b4428"'
                    f' opacity=".9"/>'
                    f'<ellipse cx="880" cy="660" rx="80" ry="54" fill="#6b4428"'
                    f' opacity=".9"/>'
                    f'<circle cx="430" cy="540" r="104" fill="#e8e2d6" stroke="{K}"'
                    f' stroke-width="5.5"/>'
                    f'<path d="M360,452 l{-36:.0f},{-54:.0f} M500,452 l{36:.0f},{-54:.0f}"'
                    f' stroke="#c9bfa6" stroke-width="16"/>'
                    f'<circle cx="396" cy="520" r="9" fill="{K}"/>'
                    f'<ellipse cx="420" cy="600" rx="54" ry="34" fill="#d8b0a0"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="402" cy="596" r="7" fill="#8a5a4a"/>'
                    f'<circle cx="440" cy="598" r="7" fill="#8a5a4a"/>'
                    f'<path d="M560,800 l-14,120 M720,810 l-6,118 M900,800 l14,120'
                    f' M1020,780 l22,130" stroke="#c9bfa6" stroke-width="22"/>')
    zh = 7 * A.w(t, 1.5, .1)
    s += SL(Z_SRED, f'<path d="M376,{630+zh:.0f} q{44:.0f},{22:.0f} {88:.0f},{-6:.0f}"'
                    f' fill="none" stroke="#8a7a62" stroke-width="6"/>')
    hx, hy, hh = 1060, 1000, 560
    s += SL(Z_SRED, f'<rect x="{hx-90:.0f}" y="{hy-70:.0f}" width="180" height="24"'
                    f' rx="5" fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{hx-70:.0f}" y="{hy-46:.0f}" width="18" height="46"'
                    f' fill="{DOSKA2}"/>'
                    f'<rect x="{hx+54:.0f}" y="{hy-46:.0f}" width="18" height="46"'
                    f' fill="{DOSKA2}"/>')
    s += SL(Z_SRED, figura(hx, hy - 60, hh, t, col="#4a3a52", kant="#ffd98a",
                           platok=True, ph=.3, naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(hx, hy - 60, hh, 1, hh * .26, 40, t, "#4a3a52", "#ffd98a", .2, 3)
    r2, (e2x, e2y), _ = _ruka(hx, hy - 60, hh, -1, hh * .26, 44, t, "#4a3a52", "#ffd98a", .6, 3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, podoynik((e1x + e2x) * .5, e1y + 190, 2.3, t, True, .2))
    # ясли с сеном, вилы, кот у блюдца, телёнок в загородке
    s += SL(Z_SRED, f'<path d="M60,820 h380 l-40,-170 h-300 Z" fill="url(#derev)"'
                    f' stroke="{K}" stroke-width="5"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<path d="M{110+i*28:.0f},660 q{16:.0f},{-50:.0f} {44:.0f},{-74:.0f}"'
                        f' fill="none" stroke="#b9a37a" stroke-width="5"/>')
    s += SL(Z_SRED, f'<g transform="rotate(-12 300 1000)">'
                    f'<rect x="294" y="560" width="14" height="440" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{282+i*12:.0f},560 l{-6+i*6:.0f},{-80:.0f}"'
                        f' stroke="{ZHELEZ}" stroke-width="7"/>')
    s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, kot(660, 1050, t, 1.4, "#6b5230", False)
            + f'<ellipse cx="740" cy="1056" rx="46" ry="14" fill="#e8e2d6"'
              f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="1180" y="700" width="200" height="200" rx="6"'
                    f' fill="none" stroke="#6b4428" stroke-width="10"/>'
                    f'<ellipse cx="1280" cy="860" rx="86" ry="52" fill="#d8cbb0"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="1210" cy="820" r="34" fill="#d8cbb0" stroke="{K}"'
                    f' stroke-width="4"/>')
    s += SL(Z_SRED, lampa(240, 240, t, 1.5, False) + teplo(240, 250, 360, 300, .5))
    s += SL(Z_SRED, ten(hx, hy + 4, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def kruzhki_moloka_po_schetu(t):
    """Длинный стол в избе: в ряд пять кружек разного роста, мать наливает из
    крынки в каждую, пятеро детей на лавке следят, чтобы всем поровну. Над
    кружками встают рисованные мерки на одной высоте."""
    rnd = random.Random(2011)
    s = stena_gornicy_19(t, 7, 820, True, True)
    s += SL(Z_DAL, okno_izby(120, 180, 320, 280, t, None, .7, False, True))
    s += SL(Z_SRED, pech(1500, 220, 420, 560, t, True, True, False))
    s += SL(Z_SRED, ogon(1660, 640, t, 1.2, .2, 6) + teplo(1660, 620, 340, 280, .5))
    s += SL(Z_SRED, stol(260, 700, 1120, 44, True))
    s += SL(Z_SRED, lavka(300, 980, 1040))
    # ПЯТЬ КРУЖЕК разного роста
    nal = A.ease(A.seg(t, .4, 3.4))
    for i in range(5):
        kx_ = 400 + i * 200
        ks = .9 + (i % 3) * .12
        s += SL(Z_SRED, kruzhka_moloka(kx_, 700, ks, t, nal * 5 > i, i * .2))
        # мерка на одной высоте
        mer = A.out(A.seg(t, 1.2 + i * .18, .5))
        if mer > .02:
            s += SL(Z_SRED, f'<path d="M{kx_-46:.0f},{620:.0f} h{92*mer:.0f}"'
                            f' stroke="#d6a63f" stroke-width="7" opacity="{mer:.2f}"/>')
    # МАТЬ наливает из крынки
    mx, my, mh = 1180, 1040, 680
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.2, naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, -1, mh * .30, 6, t, "#8a2f22", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, 1, mh * .22, 34, t, "#8a2f22", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<g transform="rotate(38 {e1x:.0f} {e1y:.0f})">'
            + krynka_moloka(e1x - 10, e1y + 90, 1.1, t, False, True, .2) + '</g>')
    s += SL(Z_SRED, f'<path d="M{e1x-80:.0f},{e1y+40:.0f} q{-20:.0f},{70:.0f}'
                    f' {-30:.0f},{120:.0f}" fill="none" stroke="#faf6ec"'
                    f' stroke-width="9" opacity=".9"/>')
    # ПЯТЕРО ДЕТЕЙ на лавке по росту
    for i in range(5):
        dx_ = 400 + i * 190
        dh_ = 300 + i * 34
        s += SL(Z_SRED, figura(dx_, 980, dh_, t, col=["#3f5a6a", "#4a6a3a", "#6b3a6a",
                                                      "#8a6342", "#3f4a7a"][i],
                               kant="#ffd98a", ph=i * .3))
        rk, (ex, ey), _ = _ruka(dx_, 980, dh_, 1 if i % 2 else -1, dh_ * .24, 50, t,
                                "#3f4a4a", "#ffd98a", i * .2, 4)
        s += SL(Z_SRED, rk)
    s += SL(Z_SRED, karavay(300, 696, .9, True))
    for i in range(6):
        s += SL(Z_SRED, f'<ellipse cx="{1280+i*26:.0f}" cy="700" rx="13" ry="30"'
                        f' fill="#b9a37a" stroke="{K}" stroke-width="2.6"'
                        f' transform="rotate({-16+i*6} {1280+i*26:.0f} 700)"/>')
    s += SL(Z_SRED, kot(760, 1056, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, polka_s_bankami(260, 420, 520, t, 31, 5, False))
    s += SL(Z_SRED, utvar_izby(1200, 360, 300, t, 13))
    s += SL(Z_SRED, ten(mx, my + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def banka_moloka_ot_sosedki(t):
    """Развилка, деревня: соседка подаёт через калитку трёхлитровую банку
    молока под полотняной крышкой, хозяйка принимает её обеими руками и
    несёт в дом; попутчица с бидоном идёт мимо к рынку одна."""
    rnd = random.Random(2012)
    s = nebo("rassv", t, False, 281)
    s += oblaka(t, 140, 5, 157, .40)
    s += SL(Z_DAL, ulica_dal(1180, 420, 740, t, True, 113))
    s += SL(Z_DAL, izba_snaruzhi(220, 440, 330, t, True, True, 71)
            + dym(252, 280, t, 6, .22, 260, .42, "#d7dee6", 1.0))
    s += SL(Z_SRED, _merzlaya_zemlya(520, 283, False))
    s += SL(Z_SRED, zabor_shtaket(680, 420, 1240, 240, 281, 62))
    s += SL(Z_SRED, kalitka_rez(880, 420, 300, 360, t, .22, True))
    # САРАЙ с коровой и куры
    s += SL(Z_SRED, f'<rect x="1360" y="460" width="520" height="300" rx="8"'
                    f' fill="#5e4430" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1330,460 l270,-130 l280,130 Z" fill="#4a3526"'
                    f' stroke="{K}" stroke-width="5.5"/>'
                    f'<path d="M1330,460 l270,-130 l280,130" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="16" opacity=".9"/>'
                    f'<rect x="1520" y="560" width="220" height="200" rx="6"'
                    f' fill="#2b2016" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<ellipse cx="1640" cy="690" rx="100" ry="58" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="1566" cy="650" r="38" fill="#e8e2d6" stroke="{K}"'
                    f' stroke-width="4"/>'
                    f'<path d="M1540,618 l{-14:.0f},{-22:.0f} M1594,618 l{14:.0f},{-22:.0f}"'
                    f' stroke="#c9bfa6" stroke-width="8"/>')
    for i, (kx_, ky_) in enumerate(((1300, 980), (1420, 1010), (1200, 1030))):
        s += SL(Z_SRED, kura(kx_, ky_, t, 1.4, i * .3, "#e2d6c2", True))
    # СОСЕДКА подаёт банку, ХОЗЯЙКА принимает
    per = A.ease(A.seg(t, .5, 1.8))
    sx_, sy_, sh_ = 1080, 1040, 640
    s += SL(Z_SRED, figura(sx_, sy_, sh_, t, col="#3f4a3a", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(sx_, sy_, sh_, -1, sh_ * .28, -6, t, "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(sx_, sy_, sh_, 1, sh_ * .24, 26, t, "#3f4a3a", "#ffd9a8", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    hx_, hy_, hh_ = 660 - 120 * per, 1050, 650
    s += SL(Z_SRED, figura(hx_, hy_, hh_, t, col="#6b3a6a", kant="#ffd9a8", ph=.6))
    r3, (e3x, e3y), _ = _ruka(hx_, hy_, hh_, 1, hh_ * .28, -8, t, "#6b3a6a", "#ffd9a8", .3, 4)
    r4, (e4x, e4y), _ = _ruka(hx_, hy_, hh_, -1, hh_ * .26, 10, t, "#6b3a6a", "#ffd9a8", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    bx_ = e1x + (e3x - e1x) * per
    by_ = e1y + (e3y - e1y) * per
    s += SL(Z_SRED, banka_moloka(bx_, by_ + 80, 1.2, t, False, .86)
            + f'<path d="M{bx_-46:.0f},{by_-80:.0f} q{46:.0f},{-24:.0f} {92:.0f},0'
              f' l{-6:.0f},{26:.0f} q{-40:.0f},{16:.0f} {-80:.0f},0 Z" fill="{RUSH}"'
              f' stroke="{K}" stroke-width="4"/>')
    # ПОПУТЧИЦА с бидоном идёт мимо
    idt = A.ease(A.seg(t, .2, 4.0))
    px_, py_, ph_ = 300 + 240 * idt, 1066, 600
    s += SL(Z_SRED, f'<g opacity=".92">'
            + figura(px_, py_, ph_, t, col="#4a4450", kant="#cfe4f5",
                     platok=True, ph=.9) + '</g>')
    r5, (e5x, e5y), _ = _ruka(px_, py_, ph_, 1, ph_ * .26, 56, t, "#4a4450", "#cfe4f5", .4, 4)
    s += SL(Z_SRED, r5 + bidon_moloka(e5x + 10, e5y + 130, .62, t, .4))
    # кот бежит за банкой
    s += SL(Z_SRED, kot(840 - 60 * per, 1056, t, 1.4, "#6b5230", False))
    s += SL(Z_SRED, ryabina(760, 1000, t, 1.4, 6)
            + kalina_grozd(800, 930, t, 1.0, 11, 283, .3))
    s += SL(Z_SRED, para_izo_rta(sx_ - 32, sy_ - sh_ * .80, t, .3, .9, .45)
            + para_izo_rta(hx_ - 30, hy_ - hh_ * .80, t, .8, .9, .45))
    s += SL(Z_SRED, ten(sx_, sy_ + 6, 120, 20, .4) + ten(hx_, hy_ + 6, 120, 20, .4))
    s += SL(Z_SRED, dvorovye_veschi(120, 1070, 300, t, 283, ["kadka", "vedro"]))
    s += SL(Z_LETIT, sneg_letit(t, 14, 67, .32, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def molochnyy_sup_i_prostokvasha(t):
    """Развилка, город: кухня в квартире, за окном многоэтажки. Хозяйка сыплет
    вермишель в кастрюльку с молоком, в круглой врезке над плитой — настоящий
    молочный суп. На подоконнике банка под блюдцем с биркой на завтра."""
    rnd = random.Random(2013)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="700" fill="#d8cbb0"/>')
    for i in range(14):
        s += SL(Z_DAL, f'<path d="M{80+i*140:.0f},0 v700" stroke="#c9bfa6"'
                       f' stroke-width="4" opacity=".6"/>')
    s += SL(Z_DAL, okno_izby(1420, 140, 420, 420, t, None, .15, False, True))
    s += SL(Z_DAL, f'<rect x="1460" y="190" width="150" height="320" fill="#6f7a84"'
                   f' opacity=".7"/>'
                   f'<rect x="1640" y="230" width="160" height="280" fill="#7a8690"'
                   f' opacity=".7"/>')
    for i in range(10):
        s += SL(Z_DAL, f'<rect x="{1480+(i%3)*50:.0f}" y="{220+(i//3)*70:.0f}" width="32"'
                       f' height="44" fill="#ffd98a"'
                       f' opacity="{.5+.3*A.w(t,4.0,i*.3):.2f}"/>')
    # кухонный стол, плита, кастрюлька
    s += SL(Z_SRED, f'<rect x="0" y="700" width="{W}" height="40" fill="#8a7a62"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<rect x="0" y="740" width="{W}" height="340" fill="#b9a082"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{40+i*270:.0f}" y="760" width="230" height="300"'
                        f' rx="8" fill="#a8956f" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{155+i*270:.0f}" cy="800" r="12" fill="{MED}"/>')
    s += SL(Z_SRED, f'<rect x="760" y="640" width="420" height="64" rx="8"'
                    f' fill="#c9ccd1" stroke="{K}" stroke-width="5"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{830+i*110:.0f}" cy="672" r="36" fill="none"'
                        f' stroke="#8a8078" stroke-width="7"/>')
    s += SL(Z_SRED, f'<path d="M820,640 q{-10:.0f},{-110:.0f} {90:.0f},{-120:.0f}'
                    f' q{100:.0f},{10:.0f} {90:.0f},{120:.0f} Z" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="910" cy="520" rx="92" ry="22" fill="#faf6ec"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1000,560 q{54:.0f},{-10:.0f} {70:.0f},{20:.0f}"'
                    f' fill="none" stroke="{CHUGUN}" stroke-width="9"/>')
    s += SL(Z_SRED, par(910, 480, t, 5, .55, 180, .5, 1.0))
    # ВРЕЗКА-круг над кастрюлькой: вид, метка, обвязка
    ox, oy, od = 300, 160, 420
    put = kontur_proema(ox, oy, od, od, "ellips")
    vr = (f'<path d="{put}" fill="#e8e2d6"/>')
    vr += (f'<path d="{put}" fill="#faf6ec" opacity=".5"/>')
    vr += mesto_stoka(ox, oy, od, od, "ellips")
    vr += (f'<circle cx="{ox+od*.5:.0f}" cy="{oy+od*.5:.0f}" r="{od*.5:.0f}"'
           f' fill="none" stroke="#8a7a62" stroke-width="20"/>')
    vr += (f'<circle cx="{ox+od*.5:.0f}" cy="{oy+od*.5:.0f}" r="{od*.5+16:.0f}"'
           f' fill="none" stroke="#d8cbb0" stroke-width="8" opacity=".9"/>')
    s += SL(Z_SRED, vr)
    # ХОЗЯЙКА: правой сыплет вермишель, левой держит кастрюльку
    hx, hy, hh = 1180, 1060, 700
    syp = ((t * 1.2) % 1.0)
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#8a2f22", kant="#ffd98a", ph=.3))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .30, -20, t, "#8a2f22", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .22, 24, t, "#8a2f22", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    for i in range(7):
        d = ((syp + i / 7.0) % 1.0)
        s += SL(Z_SRED, f'<rect x="{e1x-60+i*8:.0f}" y="{e1y+40+160*d:.0f}" width="12"'
                        f' height="6" rx="3" fill="#e4d8bd" opacity="{1-d:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M{hx-110:.0f},{hy-hh*.46:.0f} q{110:.0f},{-24:.0f}'
                    f' {220:.0f},0 l0,{hh*.32:.0f} q{-110:.0f},{24:.0f} {-220:.0f},0 Z"'
                    f' fill="{RUSH}" opacity=".9" stroke="{K}" stroke-width="4"/>')
    # БАНКА под блюдцем с биркой на подоконнике
    s += SL(Z_SRED, banka_moloka(1560, 600, .9, t, False, .8)
            + f'<ellipse cx="1560" cy="486" rx="54" ry="14" fill="#e8e2d6"'
              f' stroke="{K}" stroke-width="3.6"/>')
    kch = 6 * A.w(t, 2.2, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} 1612 520)">'
                    f'<path d="M1604,520 l40,0 l-6,56 h-28 Z" fill="#f2ead6"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1612,540 h24" stroke="#8a7a62" stroke-width="4"/></g>')
    # бутылка молока, половник, сахарница, хлебница, полотенце, кот
    s += SL(Z_SRED, f'<path d="M420,700 h80 l-8,-130 q{-4:.0f},{-50:.0f} {-30:.0f},{-60:.0f}'
                    f' l0,{-30:.0f} h{-24:.0f} l0,{30:.0f} q{-26:.0f},{10:.0f}'
                    f' {-30:.0f},{60:.0f} Z" fill="{STEKLO}" opacity=".6" stroke="{K}"'
                    f' stroke-width="4"/>'
                    f'<path d="M424,700 h72 l-6,-120 q{-30:.0f},{10:.0f} {-60:.0f},0 Z"'
                    f' fill="#faf6ec"/>'
                    f'<rect x="446" y="470" width="30" height="16" rx="4" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<path d="M640,700 q{-6:.0f},{-40:.0f} {40:.0f},{-46:.0f}'
                    f' q{46:.0f},{6:.0f} {40:.0f},{46:.0f} Z" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M680,654 l{10:.0f},{-140:.0f}" stroke="#8a8078"'
                    f' stroke-width="9"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="620" width="110" height="80" rx="8"'
                    f' fill="#e8e2d6" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1290" y="606" width="130" height="20" rx="5"'
                    f' fill="#d8cbb0" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="60" y="700" width="200" height="30" rx="6"'
                    f' fill="#b9a082" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M100,700 q{60:.0f},{-70:.0f} {120:.0f},0 Z"'
                    f' fill="#c9a05a" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="1640" y="700" width="90" height="160" rx="6"'
                    f' fill="{TKAN2}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, kot(1400, 1050, t, 1.4, "#3b3430", False))
    s += SL(Z_SRED, lampa(960, 90, t, 1.3, True) + teplo(960, 110, 300, 250, .40))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.40)
    return s


def bidon_u_molochnoy_bochki(t):
    """Мостик в память: двор, жёлтая бочка на колёсах без надписей на пол-кадра,
    очередь с бидонами. Продавщица мерной кружкой наполняет бидон девочки,
    из окна над ними машет бабушка."""
    rnd = random.Random(2014)
    s = nebo("den", t, False, 293)
    s += oblaka(t, 140, 5, 163, .40)
    s += SL(Z_DAL, panelka(60, 620, 900, t, 5, True, 31))
    s += SL(Z_DAL, panelka(1180, 600, 740, t, 5, True, 37))
    s += SL(Z_DAL, goloe_derevo_ld(1040, 680, 460, t, 293, 8, False)
            + goloe_derevo_ld(300, 700, 420, t, 307, 7, False))
    s += SL(Z_SRED, _merzlaya_zemlya(700, 293, False))
    s += SL(Z_SRED, f'<rect x="0" y="880" width="{W}" height="200" fill="#9aa3a8"'
                    f' opacity=".85"/>')
    # БОЧКА на колёсах
    bx, by = 760, 880
    s += SL(Z_SRED, f'<rect x="{bx-380:.0f}" y="{by-420:.0f}" width="760" height="380"'
                    f' rx="120" fill="#d6a63f" stroke="{K}" stroke-width="7"/>'
                    f'<rect x="{bx-380:.0f}" y="{by-300:.0f}" width="760" height="26"'
                    f' fill="#b5803a" opacity=".9"/>'
                    f'<ellipse cx="{bx-380:.0f}" cy="{by-230:.0f}" rx="40" ry="190"'
                    f' fill="#c89a3a" stroke="{K}" stroke-width="5"/>')
    for wx in (bx - 240, bx + 180):
        s += SL(Z_SRED, f'<circle cx="{wx:.0f}" cy="{by+30:.0f}" r="68" fill="#4a4442"'
                        f' stroke="{K}" stroke-width="5"/>'
                        f'<circle cx="{wx:.0f}" cy="{by+30:.0f}" r="26" fill="#8a8078"'
                        f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="{bx-410:.0f}" y="{by-150:.0f}" width="60" height="26"'
                    f' rx="6" fill="{ZHELEZ}" stroke="{K}" stroke-width="4"/>')
    strui = ((t * 1.4) % 1.0)
    s += SL(Z_SRED, f'<path d="M{bx-404:.0f},{by-128:.0f} q{-10:.0f},{60*strui:.0f}'
                    f' {-16:.0f},{110*strui:.0f}" fill="none" stroke="#faf6ec"'
                    f' stroke-width="11" opacity=".92"/>')
    # ПРОДАВЩИЦА у крана
    px_, py_, ph_ = 300, 1040, 600
    s += SL(Z_SRED, f'<rect x="{px_-60:.0f}" y="{py_-70:.0f}" width="120" height="22"'
                    f' rx="5" fill="{DOSKA}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(px_, py_ - 60, ph_, t, col="#f2ead6", kant="#8a7a62",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(px_, py_ - 60, ph_, 1, ph_ * .30, 22, t,
                              "#f2ead6", "#8a7a62", .2, 4)
    r2, (e2x, e2y), _ = _ruka(px_, py_ - 60, ph_, -1, ph_ * .24, 44, t,
                              "#f2ead6", "#8a7a62", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{110:.0f},{-30:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="7"/>'
                    f'<path d="M{e1x+110:.0f},{e1y-40:.0f} h70 l-8,54 h-54 Z"'
                    f' fill="#c9ccd1" stroke="{K}" stroke-width="4"/>')
    # ДЕВОЧКА с бидоном
    dx_, dy_, dh_ = 1180, 1060, 480
    s += SL(Z_SRED, figura(dx_, dy_, dh_, t, col="#8a2f22", kant="#ffd9a8",
                           shapka=True, ph=.6))
    r3, (e3x, e3y), _ = _ruka(dx_, dy_, dh_, -1, dh_ * .28, 34, t, "#8a2f22", "#ffd9a8", .3, 4)
    r4, (e4x, e4y), _ = _ruka(dx_, dy_, dh_, 1, dh_ * .28, 38, t, "#8a2f22", "#ffd9a8", .8, 4)
    s += SL(Z_SRED, r3 + r4 + bidon_moloka((e3x + e4x) * .5, e3y + 130, .78, t, .3))
    # ОЧЕРЕДЬ: ещё двое с бидонами
    for i, (ox_, oy_, oh_, col) in enumerate(((1480, 1056, 620, "#4a4450"),
                                              (1700, 1066, 580, "#3f5a6a"))):
        s += SL(Z_SRED, figura(ox_, oy_, oh_, t, col=col, kant="#ffd9a8", ph=i * .4))
        rk, (ex, ey), _ = _ruka(ox_, oy_, oh_, 1, oh_ * .26, 52, t, col, "#ffd9a8", i * .3, 4)
        s += SL(Z_SRED, rk + bidon_moloka(ex + 10, ey + 120, .58, t, i * .3))
    # БАБУШКА машет из окна
    s += SL(Z_SRED, f'<rect x="1340" y="300" width="230" height="200" rx="6"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, figura(1455, 500, 320, t, col="#4a3a52", kant="#ffd98a",
                           platok=True, ph=.5))
    mah = 26 * A.w(t, 1.0, .0)
    r5, (e5x, e5y), _ = _ruka(1455, 500, 320, 1, 320 * .30, -40 + mah, t,
                              "#4a3a52", "#ffd98a", .2, 12)
    s += SL(Z_SRED, r5)
    for i, (gx, gy) in enumerate(((600, 1000), (700, 1040), (820, 1010))):
        s += SL(Z_SRED, ptica(gx, gy, t, 1.6, "#9aa3a8", i * .3, "#6f7a84"))
    s += SL(Z_SRED, f'<circle cx="1860" cy="980" r="60" fill="none" stroke="{CHUGUN}"'
                    f' stroke-width="9"/>'
                    f'<path d="M1800,980 L1860,920 L1900,980" fill="none"'
                    f' stroke="#8a2f22" stroke-width="9"/>')
    s += SL(Z_SRED, para_izo_rta(dx_ - 26, dy_ - dh_ * .80, t, .4, .8, .45))
    s += SL(Z_SRED, ten(px_, py_ + 6, 120, 20, .4) + ten(dx_, dy_ + 6, 100, 18, .4))
    s += SL(Z_SRED, inej_mel(293, 40, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def treugolnyy_paket_i_stakan(t):
    """Мостик в память: кухонный стол с клеёнкой, на нём треугольный молочный
    пакет без надписей с отрезанным уголком. Мальчик на табурете наклоняет
    пакет над гранёным стаканом, молоко течёт тонкой струйкой."""
    rnd = random.Random(2015)
    s = (f'<rect width="{W}" height="{H}" fill="#c3ab8a"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="640" fill="#d8cbb0"/>')
    for i in range(13):
        s += SL(Z_DAL, f'<path d="M{70+i*150:.0f},0 v640" stroke="#c9bfa6"'
                       f' stroke-width="4" opacity=".55"/>')
    s += SL(Z_DAL, okno_izby(1400, 120, 420, 400, t, None, .2, False, True))
    s += SL(Z_DAL, goloe_derevo_ld(1620, 500, 280, t, 311, 6, False))
    # радиоточка на стене
    s += SL(Z_SRED, f'<rect x="300" y="180" width="200" height="130" rx="10"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="400" cy="240" r="46" fill="#5e4430" stroke="{K}"'
                    f' stroke-width="4"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{366+i*11:.0f},210 v60" stroke="#8a7a62"'
                        f' stroke-width="3" opacity=".8"/>')
    # СТОЛ с клеёнкой
    s += SL(Z_SRED, f'<rect x="0" y="700" width="{W}" height="60" rx="6"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="6"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<rect x="{-20+i*90:.0f}" y="700" width="44" height="60"'
                        f' fill="#4a7a88" opacity=".7"/>')
    s += SL(Z_SRED, f'<rect x="240" y="760" width="34" height="300" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1600" y="760" width="34" height="300" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="4"/>')
    # ПАКЕТ-ПИРАМИДКА на пол-кадра и стакан
    nakl = 18 * A.ease(A.seg(t, .5, 1.2))
    s += SL(Z_SRED, paket_treugolnyy(760, 700, 2.4, -nakl, "#eef2f6"))
    s += SL(Z_SRED, f'<path d="M980,520 q{40:.0f},{90:.0f} {18:.0f},{170:.0f}"'
                    f' fill="none" stroke="#faf6ec" stroke-width="10" opacity=".95"/>')
    kap = ((t * .7) % 1.0)
    s += SL(Z_SRED, f'<ellipse cx="{900+20*kap:.0f}" cy="{560+120*kap:.0f}" rx="7"'
                    f' ry="10" fill="#faf6ec" opacity="{1-kap:.2f}"/>')
    nap = .25 + .5 * A.ease(A.seg(t, .8, 3.0))
    s += SL(Z_SRED, f'<path d="M1020,700 h150 l-16,-210 h-118 Z" fill="{STEKLO}"'
                    f' opacity=".55" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{1022+16*(1-nap):.0f},700 h{146-32*(1-nap):.0f}'
                    f' l{-8*nap:.0f},{-200*nap:.0f} q{-62:.0f},{14:.0f} {-130*nap:.0f},0 Z"'
                    f' fill="#faf6ec"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{1034+i*16:.0f},700 l{6:.0f},{-206:.0f}"'
                        f' stroke="#cfe4f5" stroke-width="3" opacity=".7"/>')
    # МАЛЬЧИК на табурете
    mx, my, mh = 1320, 900, 520
    s += SL(Z_SRED, f'<rect x="{mx-90:.0f}" y="{my:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{mx-70:.0f}" y="{my+26:.0f}" width="20" height="130"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="{mx+50:.0f}" y="{my+26:.0f}" width="20" height="130"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#e8e2d6", kant="#8a7a62", ph=.3))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, -1, mh * .36, -2, t, "#e8e2d6", "#8a7a62", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, 1, mh * .22, 46, t, "#e8e2d6", "#8a7a62", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<ellipse cx="{mx-54:.0f}" cy="{my+110:.0f}" rx="28" ry="56"'
                    f' fill="#6b3a2a" stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="{mx+42:.0f}" cy="{my+112:.0f}" rx="28" ry="56"'
                    f' fill="#6b3a2a" stroke="{K}" stroke-width="4"/>')
    # батон, сетка с бутылками у двери, кот
    s += SL(Z_SRED, f'<path d="M300,700 q{80:.0f},{-90:.0f} {180:.0f},{-10:.0f}'
                    f' q{20:.0f},{10:.0f} {0:.0f},{10:.0f} Z" fill="#c9a05a"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{330+i*34:.0f},{668+((i*3)%2)*8:.0f} l{20:.0f},{-20:.0f}"'
                        f' stroke="#a8824a" stroke-width="5"/>')
    s += SL(Z_SRED, f'<path d="M80,900 q{60:.0f},{-20:.0f} {120:.0f},0 l{-10:.0f},{160:.0f}'
                    f' h{-100:.0f} Z" fill="none" stroke="#6b5230" stroke-width="5"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{106+i*34:.0f},920 h26 l-4,120 h-18 Z"'
                        f' fill="{STEKLO}" opacity=".6" stroke="{K}" stroke-width="3.4"/>')
    # КУХНЯ ОБЖИТА: полка с посудой, часы, занавеска, банки и тарелки
    s += SL(Z_SRED, polka_s_bankami(560, 380, 620, t, 37, 5, False))
    s += SL(Z_SRED, hodiki(1280, 230, t, 1.2))
    for i, (tx_, ty_) in enumerate(((300, 560), (430, 572))):
        s += SL(Z_SRED, f'<ellipse cx="{tx_:.0f}" cy="{ty_:.0f}" rx="56" ry="18"'
                        f' fill="#e8e2d6" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{tx_:.0f}" cy="{ty_-6:.0f}" rx="40" ry="12"'
                        f' fill="#f2ead6" stroke="{K}" stroke-width="3"/>')
    kch2 = 5 * A.w(t, 2.6, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kch2:.1f} 1700 160)">'
                    f'<path d="M1560,160 q{140:.0f},{-40:.0f} {280:.0f},0 l0,{220:.0f}'
                    f' q{-140:.0f},{34:.0f} {-280:.0f},0 Z" fill="{RUSH}" opacity=".92"'
                    f' stroke="{K}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<path d="M520,680 q{-6:.0f},{-50:.0f} {44:.0f},{-54:.0f}'
                    f' q{50:.0f},{4:.0f} {44:.0f},{54:.0f} Z" fill="#b9a082"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, utvar_izby(80, 300, 300, t, 19))
    s += SL(Z_SRED, kot(1700, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, lampa(960, 90, t, 1.3, True) + teplo(960, 110, 300, 250, .42))
    s += SL(Z_SRED, ten(mx, my + 160, 120, 20, .4))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.40)
    return s


def penka_v_kruzhke(t):
    """Мостик в память: на кухонном столе две кружки горячего молока с пенкой.
    Брат зажмурился и пьёт, на губе белые усы; сестра вылавливает пенку
    ложкой и вешает её на край блюдца."""
    rnd = random.Random(2016)
    s = (f'<rect width="{W}" height="{H}" fill="#c3ab8a"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="620" fill="#d8cbb0"/>')
    for i in range(12):
        s += SL(Z_DAL, f'<path d="M{90+i*160:.0f},0 v620" stroke="#c9bfa6"'
                       f' stroke-width="4" opacity=".5"/>')
    s += SL(Z_DAL, okno_izby(1420, 120, 400, 380, t, None, .25, False, True))
    # СТОЛ в клетку
    s += SL(Z_SRED, f'<rect x="0" y="680" width="{W}" height="70" rx="6"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="6"/>')
    for i in range(24):
        s += SL(Z_SRED, f'<rect x="{-20+i*84:.0f}" y="680" width="42" height="70"'
                        f' fill="#a8432a" opacity=".65"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M0,{694+i*14:.0f} h{W}" stroke="#f2ead6"'
                        f' stroke-width="3" opacity=".35"/>')
    # ДВЕ КРУЖКИ с пенкой
    s += SL(Z_SRED, kruzhka_moloka(700, 680, 2.0, t, True, .1, "#e8e2d6"))
    s += SL(Z_SRED, kruzhka_moloka(1180, 680, 2.0, t, True, .5, "#dce4ea"))
    s += SL(Z_SRED, par(700, 540, t, 4, .45, 150, .45, .9)
            + par(1180, 540, t, 4, .45, 150, .45, .9))
    # БРАТ пьёт, зажмурившись, с белыми усами
    bx, by, bh = 420, 960, 520
    s += SL(Z_SRED, f'<rect x="{bx-80:.0f}" y="{by:.0f}" width="160" height="24"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{bx-62:.0f}" y="{by+24:.0f}" width="18" height="120"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>'
                    f'<rect x="{bx+44:.0f}" y="{by+24:.0f}" width="18" height="120"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>')
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#3f5a6a", kant="#ffd98a", ph=.2))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, 1, bh * .26, -30, t, "#3f5a6a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, -1, bh * .26, -26, t, "#3f5a6a", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2 + kruzhka_moloka((e1x + e2x) * .5, e1y + 40, .8, t, False, .3))
    s += SL(Z_SRED, f'<path d="M{bx-24:.0f},{by-bh*.80+16:.0f} q{24:.0f},{14:.0f}'
                    f' {48:.0f},0" fill="none" stroke="#faf6ec" stroke-width="9"'
                    f' stroke-linecap="round"/>')
    # СЕСТРА вылавливает пенку ложкой
    sx_, sy_, sh_ = 1520, 970, 540
    s += SL(Z_SRED, f'<rect x="{sx_-80:.0f}" y="{sy_:.0f}" width="160" height="24"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{sx_-62:.0f}" y="{sy_+24:.0f}" width="18" height="120"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>'
                    f'<rect x="{sx_+44:.0f}" y="{sy_+24:.0f}" width="18" height="120"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>')
    s += SL(Z_SRED, figura(sx_, sy_, sh_, t, col="#8a2f8a", kant="#ffd98a",
                           platok=False, ph=.6))
    lozh = A.ease(A.seg(t, .6, 1.0))
    r3, (e3x, e3y), _ = _ruka(sx_, sy_, sh_, -1, sh_ * .32, -16 - 14 * lozh, t,
                              "#8a2f8a", "#ffd98a", .3, 5)
    r4, (e4x, e4y), _ = _ruka(sx_, sy_, sh_, 1, sh_ * .24, 36, t, "#8a2f8a", "#ffd98a", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, f'<path d="M{e3x:.0f},{e3y:.0f} l{-90:.0f},{-30:.0f}"'
                    f' stroke="#c9ccd1" stroke-width="7"/>'
                    f'<ellipse cx="{e3x-104:.0f}" cy="{e3y-34:.0f}" rx="26" ry="16"'
                    f' fill="#dde3e8" stroke="{K}" stroke-width="3.4"/>'
                    f'<ellipse cx="{e3x-104:.0f}" cy="{e3y-38:.0f}" rx="18" ry="10"'
                    f' fill="#f2ead6" opacity="{lozh:.2f}"/>')
    s += SL(Z_SRED, f'<ellipse cx="1320" cy="690" rx="74" ry="20" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1282,682 q{34:.0f},{-20:.0f} {64:.0f},{-2:.0f}"'
                    f' fill="none" stroke="#f2ead6" stroke-width="10"'
                    f' opacity="{lozh:.2f}"/>')
    # батон, сахарница, кот
    s += SL(Z_SRED, f'<path d="M160,680 q{80:.0f},{-86:.0f} {176:.0f},{-10:.0f}'
                    f' q{18:.0f},{10:.0f} {0:.0f},{10:.0f} Z" fill="#c9a05a"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<path d="M900,680 q{-6:.0f},{-70:.0f} {60:.0f},{-74:.0f}'
                    f' q{66:.0f},{4:.0f} {60:.0f},{74:.0f} Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="960" cy="602" rx="54" ry="14" fill="#d8cbb0"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<circle cx="960" cy="586" r="12" fill="{MED}" stroke="{K}"'
                    f' stroke-width="3"/>')
    # КУХНЯ ОБЖИТА: полка с посудой, часы, занавеска, банки и тарелки
    s += SL(Z_SRED, polka_s_bankami(560, 380, 620, t, 37, 5, False))
    s += SL(Z_SRED, hodiki(1280, 230, t, 1.2))
    for i, (tx_, ty_) in enumerate(((300, 560), (430, 572))):
        s += SL(Z_SRED, f'<ellipse cx="{tx_:.0f}" cy="{ty_:.0f}" rx="56" ry="18"'
                        f' fill="#e8e2d6" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{tx_:.0f}" cy="{ty_-6:.0f}" rx="40" ry="12"'
                        f' fill="#f2ead6" stroke="{K}" stroke-width="3"/>')
    kch2 = 5 * A.w(t, 2.6, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kch2:.1f} 1700 160)">'
                    f'<path d="M1560,160 q{140:.0f},{-40:.0f} {280:.0f},0 l0,{220:.0f}'
                    f' q{-140:.0f},{34:.0f} {-280:.0f},0 Z" fill="{RUSH}" opacity=".92"'
                    f' stroke="{K}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<path d="M520,680 q{-6:.0f},{-50:.0f} {44:.0f},{-54:.0f}'
                    f' q{50:.0f},{4:.0f} {44:.0f},{54:.0f} Z" fill="#b9a082"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, utvar_izby(80, 300, 300, t, 19))
    s += SL(Z_SRED, kot(1020, 1040, t, 1.6, "#6b5230", False))
    s += SL(Z_SRED, lampa(960, 80, t, 1.2, True) + teplo(960, 100, 280, 230, .40))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.40)
    return s


def smetana_i_syr_na_svoem_stole(t):
    """Свой обеденный стол: горшочек сметаны с ложкой и доска с куском сыра
    на пол-кадра, рядом хлеб, блины стопкой, чайник и солонка. Хозяйка кладёт
    ложку сметаны на блин, а кружку молока отодвигает рукав."""
    rnd = random.Random(2017)
    s = stena_gornicy_19(t, 11, 780, True, True)
    s += SL(Z_DAL, okno_izby(1420, 160, 420, 380, t, None, .35, False, True))
    # за окном силуэт рыночного прилавка — остаётся в стороне
    s += SL(Z_DAL, f'<rect x="1470" y="330" width="320" height="120" rx="6"'
                   f' fill="#6f7a84" opacity=".55"/>'
                   f'<path d="M1450,330 q{170:.0f},{-46:.0f} {340:.0f},0 l{-14:.0f},{26:.0f}'
                   f' q{-156:.0f},{-34:.0f} {-312:.0f},0 Z" fill="#8a98a8" opacity=".5"/>')
    s += SL(Z_SRED, stol(80, 700, 1240, 46, True))
    # ГОРШОЧЕК СМЕТАНЫ и ДОСКА С СЫРОМ — главное
    s += SL(Z_SRED, f'<path d="M360,700 q{-26:.0f},{-120:.0f} {40:.0f},{-150:.0f}'
                    f' q{90:.0f},{-14:.0f} {110:.0f},{40:.0f} q{16:.0f},{60:.0f}'
                    f' {-6:.0f},{110:.0f} Z" fill="url(#glina)" stroke="{K}"'
                    f' stroke-width="6"/>'
                    f'<ellipse cx="455" cy="556" rx="86" ry="26" fill="#faf6ec"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M500,548 l{60:.0f},{-120:.0f}" stroke="#b9a37a"'
                    f' stroke-width="12"/>'
                    f'<ellipse cx="572" cy="414" rx="30" ry="18" fill="#dcd3c2"'
                    f' stroke="{K}" stroke-width="4"'
                    f' transform="rotate(-28 572 414)"/>')
    s += SL(Z_SRED, f'<rect x="700" y="640" width="400" height="60" rx="10"'
                    f' fill="#b9a082" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M760,640 l{70:.0f},{-150:.0f} l{180:.0f},0 l{60:.0f},{150:.0f} Z"'
                    f' fill="#f2d98a" stroke="{K}" stroke-width="5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{820+((i*37)%170):.0f}" cy="{540+((i*53)%80):.0f}"'
                        f' r="{10+((i*7)%8):.0f}" fill="#e4c46a" stroke="#c9a85a"'
                        f' stroke-width="2.6"/>')
    # блины стопкой, хлеб, чайник, солонка
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="1220" cy="{690-i*16:.0f}" rx="{104-i*2:.0f}"'
                        f' ry="{24-i*0.6:.0f}" fill="#d6a63f" stroke="{K}"'
                        f' stroke-width="3.4"/>')
    s += SL(Z_SRED, karavay(180, 696, 1.0, True))
    s += SL(Z_SRED, chaynik_s_parom(1560, 700, 1.1, t, .2, True))
    s += SL(Z_SRED, f'<path d="M980,700 h70 l-8,-56 h-54 Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="1015" cy="644" rx="27" ry="9" fill="#f4f1e8"'
                    f' stroke="{K}" stroke-width="3"/>')
    # ХОЗЯЙКА за столом
    hx, hy, hh = 780, 1040, 620
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.3))
    lozh = A.ease(A.seg(t, .7, 1.4))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .32, -28 + 20 * lozh, t,
                              "#8a2f22", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .26, -18, t, "#8a2f22", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{-70:.0f},{-30:.0f}"'
                    f' stroke="#b9a37a" stroke-width="9"/>'
                    f'<ellipse cx="{e1x-86:.0f}" cy="{e1y-36:.0f}" rx="26" ry="15"'
                    f' fill="#faf6ec" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<ellipse cx="{e2x+40:.0f}" cy="{e2y+30:.0f}" rx="86" ry="24"'
                    f' fill="#e8e2d6" stroke="{K}" stroke-width="4"/>')
    # кружку молока отодвигает рукав (рука ничья)
    otod = A.ease(A.seg(t, 1.6, 1.2))
    ruk, (kx_, ky_) = rukav(60, 560, 230, 20, t, "#4a3a52", "#ffd98a", .4, 4, True)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, kruzhka_moloka(330 - 150 * otod, 700, 1.0, t, True, .4))
    s += SL(Z_SRED, polka_s_bankami(300, 380, 560, t, 41, 5, False))
    # СЕРЕДИНА СТЕНЫ ОБЖИТА: поставец, связки лука, рушник, вторая полка
    s += SL(Z_SRED, f'<rect x="900" y="200" width="420" height="300" rx="10"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="920" y="222" width="180" height="256" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1120" y="222" width="180" height="256" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="1104" cy="350" r="10" fill="{MED}"/>'
                    f'<circle cx="1128" cy="350" r="10" fill="{MED}"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<ellipse cx="{960+i*96:.0f}" cy="{300+((i*5)%2)*120:.0f}"'
                        f' rx="44" ry="16" fill="#e8e2d6" stroke="{K}" stroke-width="3.4"/>')
    for i, (lx_, ph2) in enumerate(((1420, .2), (1520, .6))):
        s += SL(Z_SRED, f'<path d="M{lx_:.0f},120 l0,{90:.0f}" stroke="#8a7a52"'
                        f' stroke-width="5"/>')
        for k in range(5):
            s += SL(Z_SRED, f'<ellipse cx="{lx_+((k*7)%3-1)*26:.0f}"'
                            f' cy="{220+k*52:.0f}" rx="26" ry="34" fill="#c9a05a"'
                            f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, puchok_trav(640, 140, 1.0, t, .3, 43, "#8a7a4a"))
    s += SL(Z_SRED, hodiki(760, 300, t, 1.3))
    s += SL(Z_SRED, pech(1700, 300, 320, 480, t, True, True, False))
    s += SL(Z_SRED, ogon(1800, 660, t, 1.0, .3, 5) + teplo(1800, 640, 300, 250, .45))
    s += SL(Z_SRED, kot(1320, 1050, t, 1.4, "#3b3430", False))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def glaz_u_chuzhogo_zabora(t):
    """Плашка четвёртого запрета: дощатый забор на пол-кадра, в нём выпал
    сучок — и в круглую дырку смотрит прищуренный глаз. За забором чужой
    двор: новая шуба на верёвке, блестящие санки, упитанный поросёнок."""
    rnd = random.Random(2018)
    s = nebo("sumer", t, False, 311)
    s += oblaka(t, 130, 5, 167, .42)
    s += SL(Z_DAL, ulica_dal(1240, 300, 700, t, True, 127))
    s += SL(Z_DAL, izba_snaruzhi(1500, 320, 300, t, True, True, 73)
            + dym(1532, 160, t, 6, .22, 260, .42, "#d7dee6", 1.0))
    # ЧУЖОЙ ДВОР за забором
    s += SL(Z_SRED, _merzlaya_zemlya(430, 313, False))
    s += SL(Z_SRED, sneg_lezhit(560, 30, "url(#sneg)"))
    kch = 7 * A.w(t, 2.2, .2)
    s += SL(Z_SRED, f'<path d="M1180,420 q180,{40:.0f} 400,{-10:.0f}" fill="none"'
                    f' stroke="#b9a37a" stroke-width="5"/>'
                    f'<g transform="rotate({kch:.1f} 1360 430)">'
                    f'<path d="M1270,434 q90,{-28:.0f} 180,0 l{26:.0f},{200:.0f}'
                    f' q{-116:.0f},{34:.0f} {-232:.0f},0 Z" fill="#6b3a2a"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1270,434 q90,{34:.0f} 180,0" fill="none"'
                    f' stroke="#e8e2d6" stroke-width="15" opacity=".9"/></g>')
    s += SL(Z_SRED, sanki_derev(1700, 700, 1.0, t, .3, True))
    s += SL(Z_SRED, f'<ellipse cx="1180" cy="700" rx="110" ry="66" fill="#e8b4a8"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="1280" cy="660" r="44" fill="#e8b4a8" stroke="{K}"'
                    f' stroke-width="4.5"/>'
                    f'<ellipse cx="1320" cy="664" rx="22" ry="16" fill="#d89a90"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="1314" cy="662" r="4" fill="{K}"/>'
                    f'<circle cx="1328" cy="662" r="4" fill="{K}"/>'
                    f'<path d="M1264,626 l{-10:.0f},{-26:.0f} l{30:.0f},{14:.0f} Z"'
                    f' fill="#e8b4a8" stroke="{K}" stroke-width="3"/>'
                    f'<path d="M1110,756 l-8,44 M1180,764 l0,40 M1250,756 l8,44"'
                    f' stroke="#d89a90" stroke-width="13"/>')
    # ЧУЖОЙ ДВОР ВИДЕН НАД ЗАБОРОМ: дом соседки, поленница, куры, дерево
    s += SL(Z_SRED, izba_snaruzhi(760, 560, 420, t, True, True, 109)
            + dym(804, 330, t, 7, .22, 280, .44, "#d7dee6", 1.0))
    s += SL(Z_SRED, goloe_derevo_ld(1120, 580, 380, t, 311, 7, True))
    s += SL(Z_SRED, f'<rect x="300" y="420" width="260" height="170" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<circle cx="{322+(i%6)*44:.0f}" cy="{448+(i//6)*58:.0f}" r="22"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    for i, (kx2, ky2) in enumerate(((620, 600), (700, 616), (540, 612))):
        s += SL(Z_SRED, kura(kx2, ky2, t, 1.3, i * .3, "#e2d6c2", True))
    s += SL(Z_SRED, dvorovye_veschi(1300, 616, 360, t, 313, ["kadka", "vedro", "korzina"]))
    # ЗАБОР на пол-кадра с дыркой от сучка
    s += SL(Z_SRED, f'<rect x="-20" y="640" width="1960" height="440" fill="url(#derev)"'
                    f' stroke="{K}" stroke-width="6"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<rect x="{-20+i*90:.0f}" y="640" width="80" height="440"'
                        f' fill="{DOSKA if i % 2 else DOSKA2}" stroke="{K}"'
                        f' stroke-width="3.4"/>')
        if i % 3 == 0:
            s += SL(Z_SRED, f'<path d="M{10+i*90:.0f},680 q{20:.0f},{160:.0f}'
                            f' {4:.0f},{340:.0f}" fill="none" stroke="#6b4428"'
                            f' stroke-width="4" opacity=".6"/>')
    for k in (.26, .74):
        s += SL(Z_SRED, f'<rect x="-20" y="{640+440*k:.0f}" width="1960" height="26"'
                        f' fill="{DOSKA2}" stroke="{K}" stroke-width="4"/>')
    # ДЫРКА ОТ СУЧКА и прищуренный глаз
    gx, gy = 700, 850
    s += SL(Z_SRED, f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="104" fill="#2b2016"'
                    f' stroke="{K}" stroke-width="6"/>')
    pr = .5 + .5 * abs(A.w(t, 1.6, .0))
    s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="86" ry="{54*pr:.0f}"'
                    f' fill="#f0cfae"/>'
                    f'<circle cx="{gx+8:.0f}" cy="{gy:.0f}" r="{34*pr:.0f}"'
                    f' fill="#4a6a78"/>'
                    f'<circle cx="{gx+8:.0f}" cy="{gy:.0f}" r="{16*pr:.0f}" fill="{K}"/>'
                    f'<circle cx="{gx+22:.0f}" cy="{gy-14*pr:.0f}" r="{8*pr:.0f}"'
                    f' fill="#ffffff" opacity=".9"/>'
                    f'<path d="M{gx-86:.0f},{gy-54*pr:.0f} q{86:.0f},{-40*pr:.0f}'
                    f' {172:.0f},{14*pr:.0f}" fill="none" stroke="#3f3122"'
                    f' stroke-width="10"/>')
    # СОСЕДКА согнулась к дырке
    sx_, sy_, sh_ = 480, 1070, 620
    s += SL(Z_SRED, figura(sx_, sy_, sh_, t, col="#5e5a55", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.4, naklon=4.0))
    r1, (e1x, e1y), _ = _ruka(sx_, sy_, sh_, 1, sh_ * .30, 62, t, "#5e5a55", "#cfe4f5", .2, 3)
    r2, (e2x, e2y), _ = _ruka(sx_, sy_, sh_, -1, sh_ * .30, 64, t, "#5e5a55", "#cfe4f5", .7, 3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, para_izo_rta(sx_ - 34, sy_ - sh_ * .78, t, .4, 1.0, .5))
    s += SL(Z_SRED, ten(sx_, sy_ + 6, 130, 22, .45))
    # ворона на заборе, рябина, сугроб
    vor = 7 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<ellipse cx="{1000+vor:.0f}" cy="470" rx="52" ry="34"'
                    f' fill="#23242a" stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{1036+vor:.0f}" cy="436" r="24" fill="#23242a"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M{1058+vor:.0f},434 l28,6 l-28,8 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="2.6"/>'
                    f'<circle cx="{1044+vor:.0f}" cy="430" r="4" fill="#e8e2d6"/>')
    s += SL(Z_SRED, ryabina(200, 980, t, 1.5, 6)
            + kalina_grozd(240, 900, t, 1.1, 12, 313, .2))
    s += SL(Z_SRED, inej_mel(311, 46, 960, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 18, 71, .34, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def schety_u_okna(t):
    """Окно в морозных узорах, перед ним на подоконнике деревянные счёты на
    пол-кадра. Женщина в шали перекидывает деревяшку за деревяшкой и
    протирает в стекле глазок, а спицы счётов уходят за край кадра."""
    rnd = random.Random(2019)
    s = stena_gornicy_19(t, 13, 820, True, False)
    # ОКНО в морозных узорах
    s += SL(Z_SRED, f'<rect x="420" y="120" width="1080" height="560" rx="8"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="7"/>'
                    f'<rect x="450" y="150" width="1020" height="500" fill="#9fc4d8"'
                    f' opacity=".5"/>'
                    f'<path d="M960,120 v560 M420,400 h1080" stroke="#e4d8bd"'
                    f' stroke-width="16"/>'
                    f'<rect x="390" y="680" width="1140" height="36" rx="6"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="5"/>')
    for i in range(18):
        ix_ = 460 + (i % 6) * 170; iy_ = 170 + (i // 6) * 160
        s += SL(Z_SRED, f'<path d="M{ix_:.0f},{iy_:.0f} l{40:.0f},{30:.0f}'
                        f' M{ix_+40:.0f},{iy_:.0f} l{-40:.0f},{30:.0f}" stroke="#eaf6ff"'
                        f' stroke-width="4" opacity=".75"/>'
                        f'<circle cx="{ix_+20:.0f}" cy="{iy_+15:.0f}" r="12" fill="none"'
                        f' stroke="#eaf6ff" stroke-width="3" opacity=".6"/>')
    # глазок, протёртый в стекле, и чужой дом за ним
    s += SL(Z_SRED, f'<circle cx="1180" cy="330" r="110" fill="#3f4a56" opacity=".9"/>'
                    f'<rect x="1120" y="300" width="130" height="90" rx="5"'
                    f' fill="#5e6a78"/>'
                    f'<rect x="1150" y="330" width="40" height="40" fill="#ffd98a"'
                    f' opacity="{.6+.25*A.w(t,4.0,.2):.2f}"/>')
    for i in range(16):
        d = ((t * .3 + i / 16.0) % 1.0)
        s += SL(Z_SRED, f'<circle cx="{1110+((i*53)%140):.0f}" cy="{250+220*d:.0f}"'
                        f' r="4" fill="#ffffff" opacity="{(1-d)*.7:.2f}"/>')
    # СЧЁТЫ на подоконнике — главный предмет, спицы уходят за край
    s += SL(Z_SRED, schety_kostyashki(540, 530, 2.2, t, .1, 7))
    s += SL(Z_SRED, f'<rect x="1200" y="560" width="760" height="10" fill="{ZHELEZ}"'
                    f' opacity=".9"/>'
                    f'<rect x="1200" y="640" width="760" height="10" fill="{ZHELEZ}"'
                    f' opacity=".9"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{1240+i*96:.0f}" cy="565" rx="18" ry="22"'
                        f' fill="#c8a05a" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{1280+i*92:.0f}" cy="645" rx="18" ry="22"'
                        f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    # ЖЕНЩИНА в шали на табурете
    zx, zy, zh = 420, 1050, 640
    s += SL(Z_SRED, f'<rect x="{zx-80:.0f}" y="{zy-26:.0f}" width="160" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(zx, zy - 20, zh, t, col="#4a4450", kant="#ffd98a",
                           platok=True, ph=.3))
    s += SL(Z_SRED, f'<path d="M{zx-120:.0f},{zy-zh*.62:.0f} q{120:.0f},{-30:.0f}'
                    f' {240:.0f},0 l{20:.0f},{zh*.36:.0f} q{-140:.0f},{34:.0f}'
                    f' {-280:.0f},0 Z" fill="#6b3a6a" opacity=".92" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    perek = A.ease(A.seg(t, .5, 1.6))
    r1, (e1x, e1y), _ = _ruka(zx, zy - 20, zh, 1, zh * .32, -16 + 10 * perek, t,
                              "#4a4450", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(zx, zy - 20, zh, -1, zh * .28, -30, t,
                              "#4a4450", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    # остывший чай, клубок, кот, ходики
    s += SL(Z_SRED, kruzhka_moloka(240, 700, 1.0, t, False, .5, "#d8cbb0"))
    s += SL(Z_SRED, f'<circle cx="1700" cy="980" r="60" fill="#8a2f8a" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M{1650+i*8:.0f},{950+i*10:.0f} q{50:.0f},{20:.0f}'
                        f' {100:.0f},{-10:.0f}" fill="none" stroke="#6b2f6b"'
                        f' stroke-width="3"/>')
    s += SL(Z_SRED, kot(1500, 1050, t, 1.5, "#3b3430", True))
    s += SL(Z_SRED, hodiki(180, 260, t, 1.4))
    s += SL(Z_SRED, lampa(1760, 200, t, 1.2, False) + teplo(1760, 210, 280, 230, .42))
    s += SL(Z_SRED, ten(zx, zy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def bant_za_pervoy_partoy(t):
    """Класс с задних парт: затылки и косы, а за первой партой — девочка с
    огромным пышным белым бантом на пол-кадра, бант светится на солнце.
    Над одноклассницами всплывают облачка с таким же бантом."""
    rnd = random.Random(2020)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="620" fill="#d8cbb0"/>'
                   f'<rect x="0" y="620" width="{W}" height="60" fill="#8a7a52"'
                   f' opacity=".85"/>')
    s += SL(Z_DAL, klassnaya_doska(240, 120, 760, 400, t, 7))
    s += SL(Z_DAL, okno_izby(1500, 130, 380, 400, t, None, .3, False, True))
    s += SL(Z_DAL, f'<circle cx="1690" cy="300" r="90" fill="#ffe9ac" opacity=".35"/>')
    s += SL(Z_SRED, polovicy(760, "#8a6342"))
    s += SL(Z_SRED, f'<rect x="1120" y="420" width="120" height="150" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="1180" cy="380" r="62" fill="#3f6b7a" stroke="{K}"'
                    f' stroke-width="5"/>'
                    f'<path d="M1124,370 q{56:.0f},{40:.0f} {112:.0f},0" fill="none"'
                    f' stroke="#56763f" stroke-width="7"/>')
    # ПАРТЫ рядами, затылки и косы
    for r_ in range(3):
        py_ = 980 - r_ * 230
        for i in range(3):
            px_ = 300 + i * 540 - r_ * 40
            s += SL(Z_SRED, parta_shkolnaya(px_, py_, 400, t, 7 + i, i == 0))
    for i, (hx_, hy_, hh_) in enumerate(((420, 1070, 360), (960, 1066, 350),
                                         (1480, 1070, 340))):
        s += SL(Z_SRED, f'<ellipse cx="{hx_:.0f}" cy="{hy_-200:.0f}" rx="56" ry="66"'
                        f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>'
                        f'<path d="M{hx_-30:.0f},{hy_-150:.0f} q{30:.0f},{90:.0f}'
                        f' {10:.0f},{150:.0f}" fill="none" stroke="#5e4430"'
                        f' stroke-width="18"/>'
                        f'<path d="M{hx_+30:.0f},{hy_-150:.0f} q{-24:.0f},{90:.0f}'
                        f' {-6:.0f},{150:.0f}" fill="none" stroke="#5e4430"'
                        f' stroke-width="18"/>')
        for bx_ in (hx_ - 40, hx_ + 36):
            s += SL(Z_SRED, f'<path d="M{bx_-20:.0f},{hy_-60:.0f} q{20:.0f},{-20:.0f}'
                            f' {40:.0f},0 q{-20:.0f},{20:.0f} {-40:.0f},0 Z"'
                            f' fill="#c8301f" stroke="{K}" stroke-width="3"/>')
    # ДЕВОЧКА С БАНТОМ за первой партой
    dx, dy, dh = 960, 760, 420
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#3f3a4a", kant="#ffd98a", ph=.2))
    siy = .75 + .25 * A.w(t, 2.6, .0)
    bx_, by_ = dx, dy - dh * .95
    s += SL(Z_SRED, f'<ellipse cx="{bx_:.0f}" cy="{by_:.0f}" rx="300" ry="190"'
                    f' fill="#ffffff" opacity="{.20*siy:.2f}"/>')
    for i in (-1, 1):
        s += SL(Z_SRED, f'<path d="M{bx_:.0f},{by_:.0f}'
                        f' q{i*210:.0f},{-130:.0f} {i*230:.0f},{10:.0f}'
                        f' q{-i*20:.0f},{130:.0f} {-i*230:.0f},{-10:.0f} Z"'
                        f' fill="#f8fbff" stroke="#c6d4e4" stroke-width="7"/>')
        s += SL(Z_SRED, f'<path d="M{bx_+i*60:.0f},{by_+30:.0f}'
                        f' q{i*40:.0f},{120:.0f} {i*20:.0f},{210:.0f}'
                        f' l{-i*70:.0f},{-20:.0f} q{i*30:.0f},{-80:.0f}'
                        f' {-i*10:.0f},{-180:.0f} Z" fill="#eef4fb"'
                        f' stroke="#c6d4e4" stroke-width="6"/>')
    s += SL(Z_SRED, f'<ellipse cx="{bx_:.0f}" cy="{by_+10:.0f}" rx="62" ry="50"'
                    f' fill="#ffffff" stroke="#c6d4e4" stroke-width="7"/>')
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, 1, dh * .24, 56, t, "#3f3a4a", "#ffd98a", .2, 3)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, -1, dh * .24, 58, t, "#3f3a4a", "#ffd98a", .6, 3)
    s += SL(Z_SRED, r1 + r2)
    # ОБЛАЧКА с бантами над одноклассницами
    for i, (ox_, oy_) in enumerate(((420, 700), (1480, 690), (700, 560), (1240, 560))):
        vsp = A.out(A.seg(t, .6 + i * .3, .7))
        if vsp < .02:
            continue
        s += SL(Z_SRED, f'<g opacity="{vsp:.2f}">'
                        f'<ellipse cx="{ox_:.0f}" cy="{oy_:.0f}" rx="{110*vsp:.0f}"'
                        f' ry="{76*vsp:.0f}" fill="#f2ead6" stroke="{K}"'
                        f' stroke-width="4"/>'
                        f'<ellipse cx="{ox_-34:.0f}" cy="{oy_-6:.0f}" rx="{40*vsp:.0f}"'
                        f' ry="{28*vsp:.0f}" fill="#ffffff" stroke="#dde7f4"'
                        f' stroke-width="4"/>'
                        f'<ellipse cx="{ox_+34:.0f}" cy="{oy_-6:.0f}" rx="{40*vsp:.0f}"'
                        f' ry="{28*vsp:.0f}" fill="#ffffff" stroke="#dde7f4"'
                        f' stroke-width="4"/>'
                        f'<circle cx="{ox_:.0f}" cy="{oy_:.0f}" r="{16*vsp:.0f}"'
                        f' fill="#ffffff" stroke="#dde7f4" stroke-width="3"/></g>')
    s += SL(Z_SRED, lampa(960, 80, t, 1.2, True) + teplo(960, 100, 280, 230, .36))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.40)
    return s


def sugrob_pod_chuzhim_svetom(t):
    """Зимний вечер, два дома напротив: мужик стоит лицом к чужому
    освещённому окну и не оборачивается, а в его собственном окне за спиной
    жена ставит самовар и машут дети. Сугроб у его ног растёт."""
    rnd = random.Random(2021)
    s = nebo("noch", t, True, 317)
    s += SL(Z_NEBO, luna_v_gorode(1680, 160, t, .8, True))
    s += SL(Z_DAL, ulica_dal(600, 500, 760, t, True, 131))
    # ЧУЖОЙ ДОМ с освещённым окном (слева)
    s += SL(Z_SRED, izba_snaruzhi(300, 820, 520, t, True, True, 79)
            + dym(348, 540, t, 7, .22, 300, .42, "#d7dee6", 1.0))
    s += SL(Z_SRED, f'<rect x="260" y="560" width="240" height="190" rx="6"'
                    f' fill="#ffd98a" opacity="{.75+.2*A.w(t,4.0,.2):.2f}"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M380,560 v190 M260,650 h240" stroke="#6b4428"'
                    f' stroke-width="12"/>')
    s += SL(Z_SRED, teplo(380, 650, 360, 300, .45))
    # СВОЙ ДОМ справа — в окне жена с самоваром и дети
    s += SL(Z_SRED, izba_snaruzhi(1560, 840, 500, t, True, True, 83)
            + dym(1604, 570, t, 7, .22, 300, .42, "#d7dee6", 1.0))
    s += SL(Z_SRED, f'<rect x="1440" y="580" width="300" height="220" rx="6"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1452" y="592" width="276" height="196" fill="#ffd98a"'
                    f' opacity="{.8+.15*A.w(t,3.4,.4):.2f}"/>')
    s += SL(Z_SRED, f'<g opacity=".95">'
            + figura(1540, 780, 170, t, col="#8a2f22", kant="#ffd98a", platok=True, ph=.3)
            + '</g>')
    s += SL(Z_SRED, f'<path d="M1600,700 h70 l-8,66 h-54 Z" fill="{ZOL}" stroke="{K}"'
                    f' stroke-width="3.4"/>'
                    f'<ellipse cx="1635" cy="700" rx="36" ry="11" fill="{MED}"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<rect x="1626" y="664" width="18" height="38" fill="{ZOL}"'
                    f' stroke="{K}" stroke-width="2.6"/>')
    for i, dx_ in enumerate((1700, 1470)):
        mah = 18 * A.w(t, 1.2, i * .5)
        s += SL(Z_SRED, f'<g opacity=".95">'
                + figura(dx_, 788, 120, t, col="#3f5a6a", kant="#ffd98a", ph=i * .4)
                + f'<path d="M{dx_+16:.0f},{740:.0f} q{20+mah:.0f},{-26:.0f}'
                  f' {30+mah:.0f},{-44:.0f}" fill="none" stroke="#3f5a6a"'
                  f' stroke-width="9" stroke-linecap="round"/></g>')
    s += SL(Z_SRED, kot(1452, 790, t, .7, "#3b3430", False))
    s += SL(Z_SRED, teplo(1590, 690, 320, 260, .40))
    # МУЖИК спиной к своему дому
    sug = A.ease(A.seg(t, .5, 4.0))
    mx, my, mh = 940, 1010, 700
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f3a33", kant="#cfe4f5",
                           tulup=True, shapka=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .22, 60, t, "#3f3a33", "#cfe4f5", .2, 3)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .22, 62, t, "#3f3a33", "#cfe4f5", .7, 3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{mx-56:.0f},{my-mh*.90:.0f} q{56:.0f},{-18:.0f}'
                    f' {112:.0f},0 l0,{14:.0f} q{-56:.0f},{16:.0f} {-112:.0f},0 Z"'
                    f' fill="url(#sneg)" opacity=".9"/>')
    s += SL(Z_SRED, para_izo_rta(mx - 40, my - mh * .80, t, .3, 1.1, .55))
    # СУГРОБ растёт у ног
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my+10:.0f}" rx="{200+120*sug:.0f}"'
                    f' ry="{40+70*sug:.0f}" fill="url(#sneg)" opacity=".95"/>')
    s += SL(Z_SRED, inej_mel(317, 40, my - 40, my + 40, mx - 280, mx + 280))
    s += SL(Z_SRED, _merzlaya_zemlya(980, 331, False))
    s += SL(Z_SRED, sneg_lezhit(1000, 32, "url(#sneg)"))
    s += SL(Z_SRED, zabor_shtaket(-40, 880, 700, 180, 317, 60)
            + zabor_shtaket(1240, 900, 720, 170, 331, 62))
    s += SL(Z_SRED, goloe_derevo_ld(760, 1000, 440, t, 337, 7, True))
    s += SL(Z_LETIT, sneg_letit(t, 44, 73, .7, .9))
    s += ramka_pp("oba", "#0e0c0b", .55)
    s += vinetka(.46)
    return s


def sosedka_u_kotoroy_vse_luchshe(t):
    """Окно соседки на пол-кадра: по словам подсвечиваются белоснежные
    занавески, ряд банок с вареньем под одинаковыми крышками и двое детей с
    пятёрками в дневниках. Под окном на лавочке переглядываются соседки."""
    rnd = random.Random(2022)
    s = nebo("sumer", t, False, 331)
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="820" fill="#8a7a62"/>')
    s += SL(Z_DAL, brevna(0, 0, W, 820, 86, 1))
    # ОКНО на пол-кадра
    ox, oy, ow, oh = 380, 120, 1180, 620
    s += SL(Z_SRED, f'<rect x="{ox-40:.0f}" y="{oy-40:.0f}" width="{ow+80:.0f}"'
                    f' height="{oh+80:.0f}" rx="10" fill="#d8cbb0" stroke="{K}"'
                    f' stroke-width="7"/>'
                    f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
                    f' fill="#ffe9c8" opacity=".55" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{ox+ow*.5:.0f},{oy:.0f} v{oh:.0f}'
                    f' M{ox:.0f},{oy+oh*.5:.0f} h{ow:.0f}" stroke="#e4d8bd"'
                    f' stroke-width="18"/>')
    # ЗАНАВЕСКИ подсвечиваются первыми
    z1 = A.out(A.seg(t, .4, .8))
    for i in (0, 1):
        s += SL(Z_SRED, f'<path d="M{ox+20+i*(ow-280):.0f},{oy+16:.0f}'
                        f' q{70:.0f},{40:.0f} {60:.0f},{oh*.84:.0f} q{-50:.0f},{30:.0f}'
                        f' {-110:.0f},{10:.0f} Z" fill="#ffffff"'
                        f' opacity="{.55+.4*z1:.2f}" stroke="#dde7f4" stroke-width="5"/>')
    s += SL(Z_SRED, f'<path d="M{ox+10:.0f},{oy+14:.0f} h{ow-20:.0f}"'
                    f' stroke="#c9bfa6" stroke-width="8"/>')
    # БАНКИ с вареньем в ряд
    z2 = A.out(A.seg(t, 1.2, .8))
    for i in range(6):
        s += SL(Z_SRED, f'<g opacity="{.5+.5*z2:.2f}">'
                + banka_moloka(ox + 180 + i * 150, oy + oh - 30, .62, t, True, .82,
                               ["#8a2f22", "#c8301f", "#6b3a6a", "#b5803a",
                                "#8a2f22", "#c8301f"][i]) + '</g>')
    s += SL(Z_SRED, f'<rect x="{ox+10:.0f}" y="{oy+oh-26:.0f}" width="{ow-20:.0f}"'
                    f' height="26" rx="5" fill="#e4d8bd" stroke="{K}" stroke-width="4"/>')
    # ДВОЕ ДЕТЕЙ с дневниками и СОСЕДКА поправляет занавеску
    z3 = A.out(A.seg(t, 2.0, .8))
    for i, dx_ in enumerate((720, 960)):
        s += SL(Z_SRED, figura(dx_, oy + oh - 60, 300, t,
                               col=["#3f5a6a", "#6b3a6a"][i], kant="#ffd98a", ph=i * .4))
        s += SL(Z_SRED, f'<rect x="{dx_-70:.0f}" y="{oy+oh-180:.0f}" width="140"'
                        f' height="96" rx="8" fill="#f2ead6" stroke="{K}"'
                        f' stroke-width="4"/>')
        for k in range(2):
            s += SL(Z_SRED, f'<path d="M{dx_-30+k*60:.0f},{oy+oh-150:.0f}'
                            f' l{10:.0f},{26:.0f} l{20:.0f},{-44:.0f}" fill="none"'
                            f' stroke="#c8301f" stroke-width="7"'
                            f' opacity="{z3:.2f}"/>')
    sx_, sy_, sh_ = 1380, oy + oh - 40, 420
    s += SL(Z_SRED, figura(sx_, sy_, sh_, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(sx_, sy_, sh_, 1, sh_ * .30, -34, t, "#8a2f22", "#ffd98a", .2, 5)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, lampa(960, oy + 60, t, 1.3, True) + teplo(960, oy + 80, 340, 280, .45))
    # ЛАВОЧКА под окном: две женщины-силуэта переглядываются
    s += SL(Z_SRED, f'<rect x="420" y="900" width="900" height="26" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="440" y="926" width="24" height="120" fill="{DOSKA2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1260" y="926" width="24" height="120" fill="{DOSKA2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i, (zx_, naklon) in enumerate(((620, 5.0), (1060, -5.0))):
        pov = A.w(t, 1.6, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({naklon*pov:.1f} {zx_:.0f} 900)">'
                + figura(zx_, 900, 420, t, col=["#4a4450", "#5e5a55"][i],
                         kant="#cfe4f5", platok=True, tulup=True, ph=i * .4) + '</g>')
        s += SL(Z_SRED, para_izo_rta(zx_ - 26, 900 - 420 * .80, t, i * .4, .8, .45))
    s += SL(Z_SRED, _merzlaya_zemlya(1000, 337, False))
    s += SL(Z_SRED, sneg_lezhit(1010, 26, "url(#sneg)"))
    s += SL(Z_SRED, dvorovye_veschi(120, 1066, 300, t, 337, ["kadka", "metla"]))
    s += SL(Z_LETIT, sneg_letit(t, 20, 79, .36, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def chuzhoy_karavay(t):
    """Кухня: на столе свой небольшой каравай на полотенце, а в окне напротив
    сияет чужой огромный рисованный каравай. Бабушка прикрывает внучке рот
    варежкой-прихваткой и поворачивает её к своему столу и горбушке."""
    rnd = random.Random(2023)
    s = stena_gornicy_19(t, 17, 800, True, True)
    # ОКНО напротив с чужим караваем
    s += SL(Z_SRED, f'<rect x="1100" y="150" width="620" height="460" rx="8"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="7"/>'
                    f'<rect x="1130" y="180" width="560" height="400" fill="#3f4a56"'
                    f' opacity=".9"/>'
                    f'<path d="M1410,150 v460 M1100,380 h620" stroke="#e4d8bd"'
                    f' stroke-width="16"/>')
    siy = .7 + .3 * A.w(t, 2.4, .0)
    s += SL(Z_SRED, f'<ellipse cx="1410" cy="420" rx="300" ry="190" fill="#ffe9ac"'
                    f' opacity="{.3*siy:.2f}"/>')
    s += SL(Z_SRED, f'<g transform="translate(1410,400) scale(2.6)">'
            + karavay(0, 0, 1.0, True) + '</g>')
    # СВОЙ СТОЛ с небольшим караваем и горбушкой
    s += SL(Z_SRED, stol(80, 760, 900, 44, True))
    s += SL(Z_SRED, f'<path d="M180,756 q{150:.0f},{-36:.0f} {300:.0f},0 l{-10:.0f},{20:.0f}'
                    f' q{-140:.0f},{26:.0f} {-280:.0f},0 Z" fill="{RUSH}" stroke="{K}"'
                    f' stroke-width="4"/>')
    s += SL(Z_SRED, karavay(330, 740, 1.3, False))
    s += SL(Z_SRED, f'<path d="M560,756 q{40:.0f},{-80:.0f} {110:.0f},{-70:.0f}'
                    f' l{-10:.0f},{70:.0f} Z" fill="#c9a05a" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    s += SL(Z_SRED, par(610, 650, t, 3, .4, 120, .35, .8))
    s += SL(Z_SRED, f'<path d="M700,756 l{130:.0f},{-30:.0f} l{14:.0f},{20:.0f}'
                    f' l{-140:.0f},{34:.0f} Z" fill="#c9ccd1" stroke="{K}"'
                    f' stroke-width="4"/>'
                    f'<rect x="828" y="708" width="60" height="22" rx="6"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, chaynik_s_parom(900, 760, .9, t, .3, True))
    # ВНУЧКА на табурете у окна и БАБУШКА сзади
    pov = A.ease(A.seg(t, 1.0, 1.4))
    vx, vy, vh = 980, 880, 430
    s += SL(Z_SRED, f'<rect x="{vx-70:.0f}" y="{vy:.0f}" width="140" height="24"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{vx-54:.0f}" y="{vy+24:.0f}" width="18" height="120"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>'
                    f'<rect x="{vx+36:.0f}" y="{vy+24:.0f}" width="18" height="120"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>')
    s += SL(Z_SRED, f'<g transform="rotate({-14*pov:.1f} {vx:.0f} {vy-vh*.5:.0f})">'
            + figura(vx, vy, vh, t, col="#c8301f", kant="#ffd98a", ph=.4) + '</g>')
    r1, (e1x, e1y), _ = _ruka(vx, vy, vh, 1, vh * .26, 10, t, "#c8301f", "#ffd98a", .3, 4)
    r2, (e2x, e2y), _ = _ruka(vx, vy, vh, -1, vh * .26, 14, t, "#c8301f", "#ffd98a", .8, 4)
    s += SL(Z_SRED, r1 + r2)
    bx, by, bh = 700, 1056, 660
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd98a",
                           platok=True, ph=.2))
    r3, (e3x, e3y), _ = _ruka(bx, by, bh, 1, bh * .36, -28, t, "#4a3a52", "#ffd98a", .2, 4)
    r4, (e4x, e4y), _ = _ruka(bx, by, bh, -1, bh * .30, -14, t, "#4a3a52", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, varezhka(e3x + 10, e3y, 1.2, 20, "#8a2f22", t, .2)
            + f'<path d="M{e4x:.0f},{e4y:.0f} L{vx-70:.0f},{vy-vh*.56:.0f}"'
              f' stroke="#4a3a52" stroke-width="14" stroke-linecap="round"/>')
    # очки бабушки — две дуги поверх лица
    s += SL(Z_SRED, f'<g opacity=".9">'
                    f'<circle cx="{bx-26:.0f}" cy="{by-bh*.845:.0f}" r="26" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="5"/>'
                    f'<circle cx="{bx+26:.0f}" cy="{by-bh*.845:.0f}" r="26" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="5"/>'
                    f'<path d="M{bx-2:.0f},{by-bh*.845:.0f} h4" stroke="{ZHELEZ}"'
                    f' stroke-width="5"/></g>')
    s += SL(Z_SRED, kot(1180, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, polka_s_bankami(160, 420, 540, t, 43, 5, False))
    s += SL(Z_SRED, polka_s_bankami(560, 300, 480, t, 53, 4, False))
    s += SL(Z_SRED, puchok_trav(740, 120, .9, t, .4, 59, "#8a7a4a")
            + puchok_trav(880, 130, .8, t, .8, 61, "#7d7040"))
    s += SL(Z_SRED, hodiki(480, 260, t, 1.2))
    s += SL(Z_SRED, utvar_izby(900, 500, 300, t, 23))
    for i, (kx2, ky2) in enumerate(((620, 980), (760, 1000))):
        s += SL(Z_SRED, f'<path d="M{kx2-44:.0f},{ky2-92:.0f} h{88:.0f} l{-8:.0f},{92:.0f}'
                        f' h{-72:.0f} Z" fill="url(#derev)" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{kx2:.0f}" cy="{ky2-92:.0f}" rx="44" ry="13"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, pech(1760, 420, 280, 400, t, True, True, False))
    s += SL(Z_SRED, ogon(1830, 700, t, .9, .4, 5) + teplo(1830, 680, 260, 210, .42))
    s += SL(Z_SRED, ten(bx, by + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def tri_oblachka_nad_lavochkoy(t):
    """Лавочка у подъезда, три соседки: над ними по словам всплывают три
    облачка — шуба на плечиках, конверт без цифр, сын с дипломом. Средняя
    одним движением сдувает все три и достаёт вязание."""
    rnd = random.Random(2024)
    s = nebo("den", t, False, 347)
    s += oblaka(t, 140, 5, 173, .40)
    s += SL(Z_DAL, panelka(60, 700, 900, t, 5, True, 41))
    s += SL(Z_DAL, panelka(1180, 680, 740, t, 5, True, 43))
    s += SL(Z_DAL, goloe_derevo_ld(1020, 760, 420, t, 347, 7, False))
    s += SL(Z_SRED, _merzlaya_zemlya(760, 349, False))
    s += SL(Z_SRED, f'<rect x="0" y="900" width="{W}" height="40" rx="6"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="5"/>')
    # ЛАВОЧКА
    s += SL(Z_SRED, f'<rect x="420" y="880" width="1080" height="26" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="420" y="820" width="1080" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="450" y="906" width="24" height="120" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1450" y="906" width="24" height="120" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    # ТРИ СОСЕДКИ
    sdul = A.out(A.seg(t, 2.2, .8))
    for i, (zx_, col) in enumerate(((620, "#4a4450"), (960, "#6b3a6a"), (1300, "#5e5a55"))):
        s += SL(Z_SRED, figura(zx_, 880, 540, t, col=col, kant="#ffd9a8",
                               platok=True, tulup=True, ph=i * .35))
        if i == 1:
            mah = -40 + 70 * sdul
            rk, (ex, ey), _ = _ruka(zx_, 880, 540, 1, 540 * .32, mah, t,
                                    col, "#ffd9a8", .2, 6)
            s += SL(Z_SRED, rk)
            rk2, (e2x, e2y), _ = _ruka(zx_, 880, 540, -1, 540 * .26, 40, t,
                                       col, "#ffd9a8", .6, 4)
            s += SL(Z_SRED, rk2)
            if sdul > .3:
                s += SL(Z_SRED, f'<circle cx="{e2x-20:.0f}" cy="{e2y+40:.0f}" r="40"'
                                f' fill="#8a2f8a" stroke="{K}" stroke-width="4"'
                                f' opacity="{sdul:.2f}"/>'
                                f'<path d="M{e2x-50:.0f},{e2y+10:.0f} l{60:.0f},{-30:.0f}'
                                f' M{e2x-36:.0f},{e2y+6:.0f} l{64:.0f},{-26:.0f}"'
                                f' stroke="#c9ccd1" stroke-width="5"'
                                f' opacity="{sdul:.2f}"/>')
        else:
            rk, (ex, ey), _ = _ruka(zx_, 880, 540, 1 if i else -1, 540 * .26, 46, t,
                                    col, "#ffd9a8", i * .3, 4)
            s += SL(Z_SRED, rk)
            if sdul > .5:
                s += SL(Z_SRED, f'<path d="M{ex-30:.0f},{ey+20:.0f} l{56:.0f},{-26:.0f}'
                                f' M{ex-24:.0f},{ey+36:.0f} l{58:.0f},{-24:.0f}"'
                                f' stroke="#c9ccd1" stroke-width="5"'
                                f' opacity="{(sdul-.5)*2:.2f}"/>')
        s += SL(Z_SRED, para_izo_rta(zx_ - 26, 880 - 540 * .80, t, i * .3, .8, .45))
    # ТРИ ОБЛАЧКА по словам
    for i, (ox_, oy_) in enumerate(((500, 420), (960, 330), (1420, 420))):
        vsp = A.out(A.seg(t, .5 + i * .45, .7)) * (1 - sdul)
        if vsp < .02:
            continue
        s += SL(Z_SRED, f'<g opacity="{vsp:.2f}" transform="translate({60*sdul:.0f},'
                        f'{-80*sdul:.0f})">'
                        f'<ellipse cx="{ox_:.0f}" cy="{oy_:.0f}" rx="170" ry="120"'
                        f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>'
                        f'<ellipse cx="{ox_-60:.0f}" cy="{oy_+90:.0f}" rx="40" ry="28"'
                        f' fill="#f2ead6" stroke="{K}" stroke-width="4"/>')
        if i == 0:
            s += SL(Z_SRED, f'<path d="M{ox_-70:.0f},{oy_-30:.0f} q{70:.0f},{-26:.0f}'
                            f' {140:.0f},0 l{20:.0f},{130:.0f} q{-90:.0f},{26:.0f}'
                            f' {-180:.0f},0 Z" fill="#6b3a2a" stroke="{K}"'
                            f' stroke-width="4"/>'
                            f'<path d="M{ox_-70:.0f},{oy_-30:.0f} q{70:.0f},{30:.0f}'
                            f' {140:.0f},0" fill="none" stroke="#e8e2d6"'
                            f' stroke-width="13"/>'
                            f'<path d="M{ox_-20:.0f},{oy_-44:.0f} q{20:.0f},{-26:.0f}'
                            f' {40:.0f},0" fill="none" stroke="{ZHELEZ}"'
                            f' stroke-width="5"/>')
        elif i == 1:
            s += SL(Z_SRED, f'<rect x="{ox_-80:.0f}" y="{oy_-50:.0f}" width="160"'
                            f' height="100" rx="6" fill="#f8f4e8" stroke="{K}"'
                            f' stroke-width="4.5"/>'
                            f'<path d="M{ox_-80:.0f},{oy_-50:.0f} l{80:.0f},{60:.0f}'
                            f' l{80:.0f},{-60:.0f}" fill="none" stroke="#c9bfa6"'
                            f' stroke-width="5"/>')
        else:
            s += SL(Z_SRED, figura(ox_ - 30, oy_ + 80, 180, t, col="#3f4a7a",
                                   kant="#ffd98a", ph=.3)
                    + f'<rect x="{ox_+30:.0f}" y="{oy_-20:.0f}" width="90" height="64"'
                      f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="4"/>'
                      f'<ellipse cx="{ox_+60:.0f}" cy="{oy_+66:.0f}" rx="66" ry="26"'
                      f' fill="#8a98a8" stroke="{K}" stroke-width="4"/>')
        s += SL(Z_SRED, '</g>')
    # клумба в инее, голуби, коляска, кот
    s += SL(Z_SRED, f'<path d="M120,1070 q{40:.0f},{-110:.0f} {170:.0f},{-104:.0f}'
                    f' q{130:.0f},{10:.0f} {160:.0f},{104:.0f} Z" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="5"/>'
            + _trava_suhaya(rnd, 5, 940, 1000, 160, 420))
    for i, (gx, gy) in enumerate(((1620, 1000), (1720, 1040), (1820, 1000))):
        s += SL(Z_SRED, ptica(gx, gy, t, 1.6, "#9aa3a8", i * .3, "#6f7a84"))
    s += SL(Z_SRED, f'<ellipse cx="1560" cy="930" rx="120" ry="60" fill="#3f6b7a"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="1490" cy="1000" r="40" fill="none" stroke="{CHUGUN}"'
                    f' stroke-width="8"/>'
                    f'<circle cx="1630" cy="1000" r="40" fill="none" stroke="{CHUGUN}"'
                    f' stroke-width="8"/>'
                    f'<path d="M1660,900 q{70:.0f},{-30:.0f} {90:.0f},{30:.0f}"'
                    f' fill="none" stroke="{CHUGUN}" stroke-width="8"/>')
    s += SL(Z_SRED, kot(380, 1050, t, 1.4, "#6b5230", False))
    s += SL(Z_SRED, inej_mel(349, 42, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def novaya_shuba_sosedki(t):
    """Лестничная площадка: соседка в новой пушистой шубе запирает дверь, а
    женщина в старом пальто поднимается с сумкой, улыбается, показывает
    «хороша!» и идёт к своей двери, где её ждут коврик и кот."""
    rnd = random.Random(2025)
    s = (f'<rect width="{W}" height="{H}" fill="#b9b2a6"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="560" fill="#c9c2b4"/>'
                   f'<rect x="0" y="560" width="{W}" height="40" fill="#8a8078"/>')
    for i in range(12):
        s += SL(Z_DAL, f'<path d="M{80+i*160:.0f},0 v560" stroke="#b0a89a"'
                       f' stroke-width="4" opacity=".55"/>')
    s += SL(Z_DAL, okno_izby(820, 120, 300, 300, t, None, .25, False, True))
    # ЛЕСТНИЦА и перила
    s += SL(Z_SRED, f'<path d="M0,1080 L560,760 L560,1080 Z" fill="#9aa3a8"'
                    f' stroke="{K}" stroke-width="5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M{i*95:.0f},{1080-i*54:.0f} h{95:.0f} l0,{-54:.0f}"'
                        f' fill="none" stroke="#8a8078" stroke-width="7"/>')
    s += SL(Z_SRED, f'<path d="M40,980 L600,660" stroke="{CHUGUN}" stroke-width="12"'
                    f' fill="none"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{60+i*80:.0f},{1000-i*46:.0f} l{14:.0f},{-120:.0f}"'
                        f' stroke="{CHUGUN}" stroke-width="7"/>')
    # ДВЕРИ и почтовые ящики
    for i, dx_ in enumerate((700, 1500)):
        s += SL(Z_SRED, f'<rect x="{dx_:.0f}" y="300" width="300" height="640" rx="6"'
                        f' fill="{"#6b3a2a" if i else "#3f5a4a"}" stroke="{K}"'
                        f' stroke-width="6"/>'
                        f'<rect x="{dx_+30:.0f}" y="340" width="240" height="250" rx="5"'
                        f' fill="#4a2a1e" opacity=".55"/>'
                        f'<circle cx="{dx_+260:.0f}" cy="640" r="16" fill="{MED}"'
                        f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="1120" y="420" width="260" height="200" rx="6"'
                    f' fill="{ZHELEZ}" stroke="{K}" stroke-width="5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{1136+(i%3)*84:.0f}" y="{436+(i//3)*92:.0f}"'
                        f' width="72" height="80" rx="4" fill="#6f7a84" stroke="{K}"'
                        f' stroke-width="3"/>'
                        f'<path d="M{1146+(i%3)*84:.0f},{470+(i//3)*92:.0f} h52"'
                        f' stroke="#4a5664" stroke-width="5"/>')
    # СОСЕДКА В ШУБЕ на пол-кадра
    sx_, sy_, sh_ = 920, 1000, 680
    s += SL(Z_SRED, figura(sx_, sy_, sh_, t, col="#6b4428", kant="#ffd9a8", ph=.2))
    puh = 1.0 + .04 * A.w(t, 2.6, .0)
    s += SL(Z_SRED, f'<path d="M{sx_-170*puh:.0f},{sy_-sh_*.64:.0f}'
                    f' q{170*puh:.0f},{-54:.0f} {340*puh:.0f},0 l{30:.0f},{sh_*.56:.0f}'
                    f' q{-200*puh:.0f},{50:.0f} {-400*puh:.0f},0 Z" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="6"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<path d="M{sx_-160+i*16:.0f},{sy_-sh_*.60:.0f}'
                        f' q{6:.0f},{20:.0f} {-2:.0f},{40:.0f}" fill="none"'
                        f' stroke="#a37b52" stroke-width="4" opacity=".75"/>')
    s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="{sy_-sh_*.66:.0f}" rx="130" ry="44"'
                    f' fill="#b08a52" stroke="{K}" stroke-width="5"/>')
    r1, (e1x, e1y), _ = _ruka(sx_, sy_, sh_, 1, sh_ * .26, 10, t, "#8a6342", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(sx_, sy_, sh_, -1, sh_ * .22, -20, t, "#8a6342", "#ffd9a8", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    # ЖЕНЩИНА в старом пальто показывает «хороша!»
    idt = A.ease(A.seg(t, 1.2, 1.8))
    zx_, zy_, zh_ = 1420 + 160 * idt, 1056, 640
    s += SL(Z_SRED, figura(zx_, zy_, zh_, t, col="#4a4450", kant="#ffd9a8", ph=.6))
    pok = A.ease(A.seg(t, .6, .8)) - A.ease(A.seg(t, 1.6, .6))
    r3, (e3x, e3y), _ = _ruka(zx_, zy_, zh_, -1, zh_ * .28, 30 - 60 * pok, t,
                              "#4a4450", "#ffd9a8", .3, 5)
    r4, (e4x, e4y), _ = _ruka(zx_, zy_, zh_, 1, zh_ * .26, 54, t, "#4a4450", "#ffd9a8", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, f'<path d="M{e4x-42:.0f},{e4y+10:.0f} h84 l-8,78 h-68 Z"'
                    f' fill="#6b3a6a" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="1740" y="960" width="180" height="40" rx="8"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, kot(1700, 960, t, 1.4, "#3b3430", False))
    s += SL(Z_SRED, sanki_derev(300, 700, .7, t, .4, True))
    s += SL(Z_SRED, lampa(960, 80, t, 1.3, True) + teplo(960, 100, 320, 260, .42))
    s += SL(Z_SRED, ten(sx_, sy_ + 6, 150, 24, .45) + ten(zx_, zy_ + 6, 120, 20, .4))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def svoe_bogatstvo_na_polkah(t):
    """Своя кухня: открытый шкаф с полками на пол-кадра — банки варенья,
    мешочек грибов, пачка чая, мёд, крупа, стопка вязаных носков, альбом.
    Женщина считает полки рукавом, над каждой встаёт галочка."""
    rnd = random.Random(2026)
    s = stena_gornicy_19(t, 19, 820, False, True)
    s += SL(Z_DAL, okno_izby(1560, 180, 320, 300, t, None, .3, False, True))
    # ШКАФ на пол-кадра
    shx, shy, shw, shh = 180, 140, 1000, 740
    s += SL(Z_SRED, f'<rect x="{shx:.0f}" y="{shy:.0f}" width="{shw:.0f}"'
                    f' height="{shh:.0f}" rx="10" fill="url(#derev)" stroke="{K}"'
                    f' stroke-width="7"/>'
                    f'<rect x="{shx+20:.0f}" y="{shy+20:.0f}" width="{shw-40:.0f}"'
                    f' height="{shh-40:.0f}" fill="#5f3f27" opacity=".55"/>')
    for i in range(4):
        py_ = shy + 60 + i * (shh - 100) / 4.0
        s += SL(Z_SRED, f'<rect x="{shx+20:.0f}" y="{py_+140:.0f}" width="{shw-40:.0f}"'
                        f' height="18" fill="{DOSKA}" stroke="{K}" stroke-width="4"/>')
        if i == 0:
            for k in range(5):
                s += SL(Z_SRED, banka_moloka(shx + 110 + k * 180, py_ + 140, .68, t, True,
                                             .8, ["#8a2f22", "#c8301f", "#6b3a6a",
                                                  "#b5803a", "#8a2f22"][k]))
        elif i == 1:
            s += SL(Z_SRED, f'<path d="M{shx+100:.0f},{py_+140:.0f} q{40:.0f},{-110:.0f}'
                            f' {90:.0f},{-20:.0f} q{30:.0f},{70:.0f} {10:.0f},{130:.0f} Z"'
                            f' fill="#b9a37a" stroke="{K}" stroke-width="4.5"/>')
            for k in range(4):
                s += SL(Z_SRED, f'<ellipse cx="{shx+330+k*60:.0f}" cy="{py_+118:.0f}"'
                                f' rx="26" ry="18" fill="#8a6342" stroke="{K}"'
                                f' stroke-width="3.4"/>'
                                f'<rect x="{shx+322+k*60:.0f}" y="{py_+118:.0f}"'
                                f' width="16" height="24" fill="#c9bfa6" stroke="{K}"'
                                f' stroke-width="2.6"/>')
            s += SL(Z_SRED, f'<rect x="{shx+620:.0f}" y="{py_+40:.0f}" width="120"'
                            f' height="100" rx="6" fill="#3f6b7a" stroke="{K}"'
                            f' stroke-width="4"/>'
                            f'<path d="M{shx+640:.0f},{py_+80:.0f} h80" stroke="#8aa8b4"'
                            f' stroke-width="7"/>')
            s += SL(Z_SRED, banka_moloka(shx + 840, py_ + 140, .66, t, True, .72, "#d6a63f"))
        elif i == 2:
            for k in range(3):
                s += SL(Z_SRED, f'<rect x="{shx+90+k*200:.0f}" y="{py_+60:.0f}"'
                                f' width="150" height="80" rx="8" fill="#c9a05a"'
                                f' stroke="{K}" stroke-width="4"/>'
                                f'<path d="M{shx+90+k*200:.0f},{py_+90:.0f} h150"'
                                f' stroke="#a8824a" stroke-width="6"/>')
            for k in range(4):
                s += SL(Z_SRED, f'<path d="M{shx+700+k*10:.0f},{py_+140-k*22:.0f}'
                                f' q{60:.0f},{-20:.0f} {120:.0f},0 l0,{20:.0f}'
                                f' q{-60:.0f},{20:.0f} {-120:.0f},0 Z" fill="#8a2f8a"'
                                f' opacity=".9" stroke="{K}" stroke-width="3.4"/>')
        else:
            s += SL(Z_SRED, f'<rect x="{shx+110:.0f}" y="{py_+30:.0f}" width="230"'
                            f' height="110" rx="8" fill="#6b3a2a" stroke="{K}"'
                            f' stroke-width="4.5"/>'
                            f'<path d="M{shx+110:.0f},{py_+70:.0f} h230" stroke="#54351f"'
                            f' stroke-width="6"/>')
            for k in range(3):
                s += SL(Z_SRED, f'<rect x="{shx+420+k*150:.0f}" y="{py_+54:.0f}"'
                                f' width="120" height="86" rx="6" fill="#e8e2d6"'
                                f' stroke="{K}" stroke-width="4"/>')
        # ГАЛОЧКА над полкой
        gal = A.out(A.seg(t, .5 + i * .45, .5))
        if gal > .02:
            s += SL(Z_SRED, f'<path d="M{shx+shw-120:.0f},{py_+80:.0f}'
                            f' l{26*gal:.0f},{26*gal:.0f} l{54*gal:.0f},{-60*gal:.0f}"'
                            f' fill="none" stroke="#3f8a4a" stroke-width="12"'
                            f' stroke-linecap="round" opacity="{gal:.2f}"/>')
    # ЖЕНЩИНА считает полки
    zx, zy, zh = 1480, 1050, 700
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#4a4450", kant="#ffd98a",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(zx, zy, zh, -1, zh * .34, -10, t, "#4a4450", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(zx, zy, zh, 1, zh * .24, 44, t, "#4a4450", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x - 10, e1y + 10, 1.0, -16, "#8a2f22", t, .2) + r2)
    # фотографии на стене без лиц, кот на подоконнике
    for i, (fx_, fy_) in enumerate(((1300, 240), (1450, 300), (1600, 240))):
        s += SL(Z_SRED, f'<rect x="{fx_:.0f}" y="{fy_:.0f}" width="120" height="150"'
                        f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>'
                        f'<ellipse cx="{fx_+60:.0f}" cy="{fy_+70:.0f}" rx="34" ry="42"'
                        f' fill="#c9bfa6"/>')
    s += SL(Z_SRED, kot(1700, 480, t, 1.4, "#3b3430", True))
    s += SL(Z_SRED, lampa(1240, 180, t, 1.2, True) + teplo(1240, 200, 300, 250, .42))
    s += SL(Z_SRED, ten(zx, zy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def izba_s_chetyrmya_zabotami(t):
    """Смена главы: изба в разрезе, четыре угла по словам. Дед распутывает
    снасти, мальчик привязывает конёк к валенку, мать снимает пучок трав,
    бабушка перебирает калину в решете. За окном пруд белеет."""
    rnd = random.Random(2027)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 92, 2))
    # перекрестье балок — четыре угла
    s += SL(Z_SRED, f'<rect x="0" y="520" width="{W}" height="26" fill="#5e4430"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<rect x="946" y="0" width="28" height="1080" fill="#5e4430"'
                    f' stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, polovicy(440, "#6b4428"))
    s += SL(Z_SRED, polovicy(980, "#6b4428"))
    # 1-й угол: дед со снастями
    s += SL(Z_SRED, stol(60, 380, 760, 36, True))
    s += SL(Z_SRED, snast_kruchki(300, 376, t, .9, 6, .1))
    dx, dy, dh = 620, 470, 420
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#3f4a3a", kant="#ffd98a",
                           boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, -1, dh * .30, -20, t, "#3f4a3a", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, 1, dh * .30, -16, t, "#3f4a3a", "#ffd98a", .6, 5)
    s += SL(Z_SRED, r1 + r2)
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} q{-80-i*18:.0f},{40+i*16:.0f}'
                        f' {-160-i*24:.0f},{10+i*10:.0f}" fill="none" stroke="#cfd6db"'
                        f' stroke-width="2.6" opacity=".9"/>')
    # 2-й угол: мальчик и конёк
    s += SL(Z_SRED, lavka(1060, 440, 420))
    mx, my, mh = 1280, 440, 380
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f5a6a", kant="#ffd98a", ph=.5))
    r3, (e3x, e3y), _ = _ruka(mx, my, mh, 1, mh * .34, 40, t, "#3f5a6a", "#ffd98a", .3, 5)
    r4, (e4x, e4y), _ = _ruka(mx, my, mh, -1, mh * .34, 44, t, "#3f5a6a", "#ffd98a", .8, 5)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, konki_snegurki((e3x + e4x) * .5, e3y + 90, 1.0, 6, True, t, .2))
    # 3-й угол: мать у печи с травами
    s += SL(Z_SRED, pech(60, 600, 520, 440, t, True, True, False))
    s += SL(Z_SRED, ogon(220, 930, t, 1.3, .1, 6) + teplo(220, 910, 360, 300, .5))
    s += SL(Z_SRED, f'<path d="M560,640 h380" stroke="#8a6342" stroke-width="11"/>')
    for i, (px_, ph2) in enumerate(((640, .2), (760, .6), (880, .9))):
        s += SL(Z_SRED, puchok_trav(px_, 648, .8, t, ph2, 47 + i, "#8a7a4a"))
    zx, zy, zh = 760, 1010, 520
    snyat = A.ease(A.seg(t, .6, 1.4))
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.4))
    r5, (e5x, e5y), _ = _ruka(zx, zy, zh, 1, zh * .34, -34 - 16 * snyat, t,
                              "#8a2f22", "#ffd98a", .2, 4)
    r6, (e6x, e6y), _ = _ruka(zx, zy, zh, -1, zh * .24, 34, t, "#8a2f22", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r5 + r6 + chaynik_s_parom(e6x - 30, e6y + 90, .62, t, .3, True))
    # 4-й угол: бабушка с калиной в решете у окна
    s += SL(Z_SRED, okno_izby(1480, 620, 360, 300, t, None, .3, False, True))
    bel = A.ease(A.seg(t, .8, 4.0))
    s += SL(Z_SRED, f'<rect x="1510" y="650" width="300" height="240" fill="url(#led)"'
                    f' opacity="{.4+.5*bel:.2f}"/>')
    bx, by, bh = 1220, 1020, 540
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd98a",
                           platok=True, ph=.6))
    r7, (e7x, e7y), _ = _ruka(bx, by, bh, 1, bh * .30, 24, t, "#4a3a52", "#ffd98a", .3, 5)
    r8, (e8x, e8y), _ = _ruka(bx, by, bh, -1, bh * .30, 26, t, "#4a3a52", "#ffd98a", .8, 5)
    s += SL(Z_SRED, r7 + r8)
    res_x, res_y = (e7x + e8x) * .5, e7y + 70
    s += SL(Z_SRED, f'<ellipse cx="{res_x:.0f}" cy="{res_y:.0f}" rx="120" ry="40"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="{res_x:.0f}" cy="{res_y-8:.0f}" rx="104" ry="32"'
                    f' fill="#8a7a52" stroke="{K}" stroke-width="3.6"/>')
    for i in range(14):
        a = i * .45
        s += SL(Z_SRED, f'<circle cx="{res_x+70*math.cos(a)*.9:.0f}"'
                        f' cy="{res_y-10+24*math.sin(a):.0f}" r="10" fill="#c8301f"'
                        f' stroke="#7d1b11" stroke-width="2.4"/>')
    s += SL(Z_SRED, lampa(960, 480, t, 1.5, True) + teplo(960, 500, 420, 340, .5))
    s += SL(Z_SRED, kot(1700, 1040, t, 1.4, "#3b3430", True))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def snasti_na_stole_pod_lampoy(t):
    """Стол под лампой: рыбацкое хозяйство на пол-кадра — зимние удочки,
    блёсны, катушки лески, поплавки, грузила, напильник, моток проволоки.
    Дед в жилетке и очках протирает удочку тряпочкой и берёт напильник."""
    rnd = random.Random(2028)
    s = stena_gornicy_19(t, 23, 860, False, True)
    s += SL(Z_DAL, okno_izby(1520, 200, 340, 300, t, None, .45, False, True))
    s += SL(Z_SRED, f'<rect x="0" y="700" width="{W}" height="60" rx="6"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="6"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<rect x="{-20+i*90:.0f}" y="700" width="44" height="60"'
                        f' fill="#4a7a88" opacity=".65"/>')
    s += SL(Z_SRED, f'<rect x="180" y="760" width="36" height="300" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1660" y="760" width="36" height="300" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="4"/>')
    # УДОЧКИ, блёсны, катушки, поплавки, грузила
    for i, ux in enumerate((300, 380, 460)):
        s += SL(Z_SRED, f'<g transform="rotate({-6+i*5} {ux:.0f} 700)">'
                        f'<rect x="{ux:.0f}" y="420" width="16" height="280" rx="7"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3.6"/>'
                        f'<rect x="{ux-10:.0f}" y="640" width="36" height="60" rx="8"'
                        f' fill="#6b3a2a" stroke="{K}" stroke-width="3.4"/>'
                        f'<circle cx="{ux+8:.0f}" cy="470" r="14" fill="none"'
                        f' stroke="{ZHELEZ}" stroke-width="4"/></g>')
    for i in range(6):
        bx_ = 640 + i * 70
        bl = .4 + .6 * abs(A.w(t, 2.2, i * .3))
        s += SL(Z_SRED, f'<path d="M{bx_:.0f},660 l{20:.0f},{-46:.0f} l{14:.0f},{46:.0f}'
                        f' l{-20:.0f},{30:.0f} Z" fill="#c9ccd1" stroke="{K}"'
                        f' stroke-width="3.4"/>'
                        f'<ellipse cx="{bx_+14:.0f}" cy="{630:.0f}" rx="7" ry="12"'
                        f' fill="#ffffff" opacity="{bl*.8:.2f}"/>')
    for i, kx_ in enumerate((1120, 1220)):
        s += SL(Z_SRED, f'<circle cx="{kx_:.0f}" cy="660" r="46" fill="#8a6342"'
                        f' stroke="{K}" stroke-width="4.5"/>'
                        f'<circle cx="{kx_:.0f}" cy="660" r="20" fill="#5f3f27"'
                        f' stroke="{K}" stroke-width="3.4"/>')
        for k in range(5):
            s += SL(Z_SRED, f'<circle cx="{kx_:.0f}" cy="660" r="{26+k*4:.0f}"'
                            f' fill="none" stroke="#cfd6db" stroke-width="2"'
                            f' opacity=".7"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<ellipse cx="{1320+i*54:.0f}" cy="670" rx="13" ry="26"'
                        f' fill="#c8301f" stroke="{K}" stroke-width="3"/>'
                        f'<ellipse cx="{1320+i*54:.0f}" cy="648" rx="11" ry="12"'
                        f' fill="#f4f1e8" stroke="{K}" stroke-width="2.6"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<ellipse cx="{880+i*40:.0f}" cy="686" rx="16" ry="12"'
                        f' fill="{ZHELEZ}" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<rect x="1000" y="676" width="150" height="16" rx="5"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="3.4"/>')
    for i in range(10):
        s += SL(Z_SRED, f'<path d="M{1006+i*14:.0f},676 l{-6:.0f},{16:.0f}"'
                        f' stroke="#6f7a84" stroke-width="2.4"/>')
    s += SL(Z_SRED, f'<circle cx="1480" cy="668" r="40" fill="none" stroke="#9aa3a8"'
                    f' stroke-width="7"/>'
                    f'<circle cx="1480" cy="668" r="26" fill="none" stroke="#9aa3a8"'
                    f' stroke-width="6"/>')
    # ДЕД в жилетке и очках
    dx, dy, dh = 760, 1050, 660
    s += SL(Z_SRED, f'<rect x="{dx-90:.0f}" y="{dy-20:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(dx, dy - 10, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, ph=.2))
    s += SL(Z_SRED, f'<path d="M{dx-80:.0f},{dy-dh*.62:.0f} q{80:.0f},{-20:.0f}'
                    f' {160:.0f},0 l{10:.0f},{dh*.30:.0f} q{-90:.0f},{24:.0f}'
                    f' {-180:.0f},0 Z" fill="#3f4a3a" stroke="{K}" stroke-width="4.5"/>')
    tryap = A.w(t, 1.1, .0)
    r1, (e1x, e1y), _ = _ruka(dx, dy - 10, dh, -1, dh * .32, -14 + 10 * tryap, t,
                              "#4a4038", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(dx, dy - 10, dh, 1, dh * .28, -8, t, "#4a4038", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<rect x="{e1x-26:.0f}" y="{e1y-14:.0f}" width="52" height="34"'
                    f' rx="8" fill="#b9c2c8" stroke="{K}" stroke-width="3.4"'
                    f' transform="rotate({-20+14*tryap:.0f} {e1x:.0f} {e1y:.0f})"/>')
    s += SL(Z_SRED, f'<g opacity=".9">'
                    f'<circle cx="{dx-26:.0f}" cy="{dy-10-dh*.845:.0f}" r="26"'
                    f' fill="none" stroke="{ZHELEZ}" stroke-width="5"/>'
                    f'<circle cx="{dx+26:.0f}" cy="{dy-10-dh*.845:.0f}" r="26"'
                    f' fill="none" stroke="{ZHELEZ}" stroke-width="5"/>'
                    f'<path d="M{dx-2:.0f},{dy-10-dh*.845:.0f} h4" stroke="{ZHELEZ}"'
                    f' stroke-width="5"/></g>')
    s += SL(Z_SRED, chaynik_s_parom(220, 700, .8, t, .4, True))
    s += SL(Z_SRED, f'<path d="M1560,700 q{40:.0f},{-40:.0f} {90:.0f},{-10:.0f}'
                    f' q{-20:.0f},{30:.0f} {-50:.0f},{10:.0f} Z" fill="#c9a05a"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, kot(1060, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, hodiki(1760, 260, t, 1.3))
    s += SL(Z_SRED, lampa(960, 140, t, 1.6, True) + teplo(960, 170, 460, 380, .55))
    s += SL(Z_SRED, ten(dx, dy + 20, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def moneta_dlya_vodyanogo(t):
    """Мостки над тёмной полыньёй: рыбак бросает в воду монету и краюху, а
    из глубины выглядывает сказочный водяной — ловит монету рукавицей и
    довольно кивает; за ним стайка окуней поворачивает к мосткам."""
    rnd = random.Random(2029)
    s = nebo("sumer", t, True, 353)
    s += SL(Z_DAL, ulica_dal(1180, 260, 740, t, True, 137))
    s += SL(Z_DAL, izba_snaruzhi(300, 300, 280, t, True, True, 89)
            + dym(328, 160, t, 6, .22, 250, .40, "#d7dee6", .9))
    s += SL(Z_SRED, f'<rect x="0" y="380" width="{W}" height="700" fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(1480, 620, 420, 140, t, .3, .0, .8, .3))
    s += SL(Z_SRED, prorub(820, 780, 300, t, .1, True))
    s += SL(Z_SRED, mostki(100, 640, 760, t, True, 300))
    # ВОДЯНОЙ в полынье
    s += SL(Z_SRED, vodyanoy(820, 900, t, 1.25, .2))
    kiv = 10 * A.w(t, 1.4, .3)
    mon = A.ease(A.seg(t, .5, 1.0))
    s += SL(Z_SRED, f'<ellipse cx="{700+120*mon:.0f}" cy="{620+160*mon-kiv:.0f}"'
                    f' rx="26" ry="10" fill="url(#med)" stroke="{K}" stroke-width="3.4"/>')
    kray = A.ease(A.seg(t, 1.4, 1.0))
    s += SL(Z_SRED, f'<path d="M{660+150*kray:.0f},{600+200*kray:.0f}'
                    f' q{40:.0f},{-30:.0f} {80:.0f},{-4:.0f} q{-26:.0f},{36:.0f}'
                    f' {-80:.0f},{4:.0f} Z" fill="#c9a05a" stroke="{K}"'
                    f' stroke-width="3.6"/>')
    # окуни поворачивают к мосткам
    for i in range(5):
        px_ = 1180 - 180 * A.ease(A.seg(t, 1.8 + i * .12, 1.6))
        py_ = 860 + i * 36
        s += SL(Z_SRED, f'<path d="M{px_-40:.0f},{py_:.0f} q{40:.0f},{-24:.0f} {80:.0f},0'
                        f' q{-40:.0f},{24:.0f} {-80:.0f},0 Z" fill="#4a6a3a"'
                        f' stroke="{K}" stroke-width="3.2"/>'
                        f'<path d="M{px_+40:.0f},{py_:.0f} l{22:.0f},{-14:.0f} l0,{28:.0f} Z"'
                        f' fill="#3f5a30" stroke="{K}" stroke-width="2.8"/>'
                        f'<circle cx="{px_-24:.0f}" cy="{py_-4:.0f}" r="4" fill="{K}"/>')
    # РЫБАК на мостках
    rx_, ry_, rh = 420, 640, 640
    s += SL(Z_SRED, figura(rx_, ry_, rh, t, col="#3f4a3a", kant="#cfe4f5",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    br = A.ease(A.seg(t, .3, .6))
    r1, (e1x, e1y), _ = _ruka(rx_, ry_, rh, 1, rh * .32, -40 + 50 * br, t,
                              "#3f4a3a", "#cfe4f5", .2, 5)
    r2, (e2x, e2y), _ = _ruka(rx_, ry_, rh, -1, rh * .26, 36, t, "#3f4a3a", "#cfe4f5", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x + 8, e1y + 8, 1.0, 14, "#6b4428", t, .2) + r2)
    s += SL(Z_SRED, f'<path d="M{e2x-36:.0f},{e2y+10:.0f} q{36:.0f},{-26:.0f} {72:.0f},0'
                    f' q{-30:.0f},{34:.0f} {-72:.0f},{-10:.0f} Z" fill="#c9a05a"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, para_izo_rta(rx_ - 34, ry_ - rh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(rx_, ry_ + 6, 120, 20, .4))
    # камыш, вмёрзшая лодка, ива, верша
    s += SL(Z_SRED, kamysh(80, 980, 240, t, 8, 353, True)
            + kamysh(1880, 1000, 230, t, 7, 359, True))
    s += SL(Z_SRED, f'<path d="M1420,980 q{110:.0f},{60:.0f} {280:.0f},{16:.0f}'
                    f' q{-40:.0f},{-60:.0f} {-280:.0f},{-16:.0f} Z" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="1560" cy="1004" rx="150" ry="24" fill="{INEY}"'
                    f' opacity=".55"/>')
    s += SL(Z_SRED, goloe_derevo_ld(1700, 900, 460, t, 367, 7, True))
    s += SL(Z_SRED, f'<path d="M1180,1066 l10,-200" stroke="#7d5636" stroke-width="12"'
                    f' fill="none"/>'
                    f'<path d="M1160,880 q{44:.0f},{-70:.0f} {92:.0f},{-8:.0f}'
                    f' q{-34:.0f},{70:.0f} {-92:.0f},{8:.0f} Z" fill="#b9a37a"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_LETIT, sneg_letit(t, 20, 83, .36, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def kryuchki_v_probke(t):
    """Тот же стол: круглая пробка на блюдце, в неё ёжиком воткнуты крючки, а
    рядом круглое увеличительное стекло на подставке — проём с настоящими
    снастями. Рыбак пинцетом втыкает очередной крючок."""
    rnd = random.Random(2030)
    s = stena_gornicy_19(t, 29, 860, False, True)
    s += SL(Z_SRED, f'<rect x="0" y="700" width="{W}" height="60" rx="6"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="6"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<rect x="{-20+i*90:.0f}" y="700" width="44" height="60"'
                        f' fill="#4a7a88" opacity=".65"/>')
    # УВЕЛИЧИТЕЛЬНОЕ СТЕКЛО на подставке — проём
    ox, oy, od = 1160, 180, 420
    put = kontur_proema(ox, oy, od, od, "ellips")
    lin = (f'<path d="{put}" fill="#dce4ea"/>')
    lin += (f'<path d="{put}" fill="#eef6ff" opacity=".45"/>')
    lin += mesto_stoka(ox, oy, od, od, "ellips")
    lin += (f'<circle cx="{ox+od*.5:.0f}" cy="{oy+od*.5:.0f}" r="{od*.5:.0f}"'
            f' fill="none" stroke="{MED}" stroke-width="24"/>')
    lin += (f'<circle cx="{ox+od*.5:.0f}" cy="{oy+od*.5:.0f}" r="{od*.5+18:.0f}"'
            f' fill="none" stroke="#8a6342" stroke-width="8"/>')
    lin += (f'<path d="M{ox+od*.5-14:.0f},{oy+od+10:.0f} h28 l6,{160:.0f} h-40 Z"'
            f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
            f'<ellipse cx="{ox+od*.5:.0f}" cy="{oy+od+170:.0f}" rx="90" ry="24"'
            f' fill="#6b4428" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, lin)
    # ПРОБКА с крючками на блюдце
    s += SL(Z_SRED, f'<ellipse cx="520" cy="700" rx="150" ry="44" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="520" cy="690" rx="120" ry="34" fill="#f2ead6"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<ellipse cx="520" cy="640" rx="96" ry="60" fill="#c89a52"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="520" cy="620" rx="96" ry="54" fill="#d8a95a"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i in range(13):
        s += SL(Z_SRED, f'<circle cx="{450+((i*37)%140):.0f}" cy="{600+((i*23)%40):.0f}"'
                        f' r="{3+((i*7)%3):.0f}" fill="#a87c3a" opacity=".8"/>')
    n_kr = 9 + int(A.ease(A.seg(t, .6, 2.4)) * 3)
    for i in range(n_kr):
        a = -1.4 + i * .32
        kx_ = 520 + 76 * math.sin(a)
        ky_ = 600 - 26 * math.cos(a)
        s += SL(Z_SRED, f'<path d="M{kx_:.0f},{ky_:.0f} l{14*math.sin(a):.0f},{-70:.0f}"'
                        f' stroke="{ZHELEZ}" stroke-width="4" fill="none"/>'
                        f'<path d="M{kx_+14*math.sin(a):.0f},{ky_-70:.0f}'
                        f' q{-16:.0f},{-20:.0f} {-18:.0f},{-34:.0f} q{16:.0f},{-6:.0f}'
                        f' {14:.0f},{12:.0f}" fill="none" stroke="{ZHELEZ}"'
                        f' stroke-width="4"/>')
    # РЫБАК с пинцетом
    rx_, ry_, rh = 860, 1050, 640
    s += SL(Z_SRED, f'<rect x="{rx_-90:.0f}" y="{ry_-20:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(rx_, ry_ - 10, rh, t, col="#6b3a6a", kant="#ffd98a",
                           boroda=True, ph=.3))
    vtyk = A.ease(A.seg(t, .8, 1.0))
    r1, (e1x, e1y), _ = _ruka(rx_, ry_ - 10, rh, -1, rh * .34, -26 + 16 * vtyk, t,
                              "#6b3a6a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(rx_, ry_ - 10, rh, 1, rh * .26, -14, t,
                              "#6b3a6a", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{-80:.0f},{-20:.0f}'
                    f' M{e1x:.0f},{e1y+8:.0f} l{-80:.0f},{-6:.0f}" stroke="#c9ccd1"'
                    f' stroke-width="5"/>')
    s += SL(Z_SRED, f'<g opacity=".9">'
                    f'<circle cx="{rx_-26:.0f}" cy="{ry_-10-rh*.845:.0f}" r="26"'
                    f' fill="none" stroke="{ZHELEZ}" stroke-width="5"/>'
                    f'<circle cx="{rx_+26:.0f}" cy="{ry_-10-rh*.845:.0f}" r="26"'
                    f' fill="none" stroke="{ZHELEZ}" stroke-width="5"/>'
                    f'<path d="M{rx_-2:.0f},{ry_-10-rh*.845:.0f} h4" stroke="{ZHELEZ}"'
                    f' stroke-width="5"/></g>')
    # катушки, поплавки, коробочки
    for i, kx_ in enumerate((160, 280)):
        s += SL(Z_SRED, f'<circle cx="{kx_:.0f}" cy="660" r="44" fill="#8a6342"'
                        f' stroke="{K}" stroke-width="4.5"/>'
                        f'<circle cx="{kx_:.0f}" cy="660" r="18" fill="#5f3f27"'
                        f' stroke="{K}" stroke-width="3.4"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<ellipse cx="{1500+i*60:.0f}" cy="670" rx="13" ry="26"'
                        f' fill="#c8301f" stroke="{K}" stroke-width="3"/>'
                        f'<ellipse cx="{1500+i*60:.0f}" cy="648" rx="11" ry="12"'
                        f' fill="#f4f1e8" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<rect x="1700" y="640" width="180" height="60" rx="8"'
                    f' fill="#b9c2c8" stroke="{K}" stroke-width="4.5"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{1700+i*45:.0f},640 v60" stroke="#8a98a8"'
                        f' stroke-width="3"/>')
    s += SL(Z_SRED, lampa(640, 160, t, 1.5, True) + teplo(640, 190, 420, 340, .5))
    s += SL(Z_SRED, kot(1400, 1050, t, 1.4, "#3b3430", False))
    s += SL(Z_SRED, ten(rx_, ry_ + 20, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def razgovor_o_proshlyh_ulovah(t):
    """Тот же стол под лампой: дед развёл руки на ширину плеч, показывая
    рыбу, и над столом всплывает рисованная щука такого размера; сын
    усмехается, показывает размер поменьше — щука сжимается до окуня."""
    rnd = random.Random(2031)
    s = stena_gornicy_19(t, 31, 860, True, True)
    s += SL(Z_DAL, okno_izby(1540, 220, 320, 280, t, None, .4, False, True))
    s += SL(Z_SRED, stol(360, 760, 1200, 44, True))
    s += SL(Z_SRED, f'<rect x="420" y="804" width="36" height="260" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1460" y="804" width="36" height="260" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="4"/>')
    # ЩУКА всплывает и сжимается до окуня
    szh = A.ease(A.seg(t, 1.8, 1.4))
    dl = 560 - 380 * szh
    vys = 150 - 90 * szh
    vsp = A.out(A.seg(t, .6, .8))
    if vsp > .02:
        qx, qy = 960, 380
        s += SL(Z_SRED, f'<g opacity="{vsp:.2f}">'
                        f'<path d="M{qx-dl*.5:.0f},{qy:.0f} q{dl*.5:.0f},{-vys:.0f}'
                        f' {dl:.0f},0 q{-dl*.5:.0f},{vys:.0f} {-dl:.0f},0 Z"'
                        f' fill="#5f7a3a" stroke="{K}" stroke-width="6"/>'
                        f'<path d="M{qx+dl*.5:.0f},{qy:.0f} l{dl*.22:.0f},{-vys*.6:.0f}'
                        f' l0,{vys*1.2:.0f} Z" fill="#4a6a30" stroke="{K}"'
                        f' stroke-width="5"/>'
                        f'<path d="M{qx-dl*.4:.0f},{qy-vys*.42:.0f}'
                        f' q{dl*.2:.0f},{-vys*.3:.0f} {dl*.36:.0f},{-vys*.04:.0f}"'
                        f' fill="none" stroke="#3f5a30" stroke-width="9"/>'
                        f'<circle cx="{qx-dl*.34:.0f}" cy="{qy-vys*.12:.0f}" r="{10:.0f}"'
                        f' fill="#f4f1e8" stroke="{K}" stroke-width="3"/>'
                        f'<circle cx="{qx-dl*.34:.0f}" cy="{qy-vys*.12:.0f}" r="5"'
                        f' fill="{K}"/>')
        for i in range(6):
            s += SL(Z_SRED, f'<path d="M{qx-dl*.3+i*dl*.12:.0f},{qy-vys*.3:.0f}'
                            f' q{10:.0f},{vys*.3:.0f} {0:.0f},{vys*.6:.0f}" fill="none"'
                            f' stroke="#4a6a30" stroke-width="3.4" opacity=".8"/>')
        s += SL(Z_SRED, '</g>')
    # ДЕД разводит руки
    dx, dy, dh = 640, 1040, 660
    razv = A.ease(A.seg(t, .4, .8))
    s += SL(Z_SRED, f'<rect x="{dx-90:.0f}" y="{dy-20:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(dx, dy - 10, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(dx, dy - 10, dh, 1, dh * (.20 + .18 * razv), -6, t,
                              "#4a4038", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy - 10, dh, -1, dh * (.20 + .18 * razv), -4, t,
                              "#4a4038", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    # СЫН усмехается и показывает размер поменьше
    sx_, sy_, sh_ = 1300, 1046, 640
    s += SL(Z_SRED, f'<rect x="{sx_-90:.0f}" y="{sy_-20:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(sx_, sy_ - 10, sh_, t, col="#3f5a6a", kant="#ffd98a", ph=.6))
    pok = A.ease(A.seg(t, 1.6, .8))
    r3, (e3x, e3y), _ = _ruka(sx_, sy_ - 10, sh_, -1, sh_ * (.14 + .10 * pok), -10, t,
                              "#3f5a6a", "#ffd98a", .3, 4)
    r4, (e4x, e4y), _ = _ruka(sx_, sy_ - 10, sh_, 1, sh_ * .22, 30, t,
                              "#3f5a6a", "#ffd98a", .8, 4)
    s += SL(Z_SRED, r3 + varezhka(e3x - 8, e3y + 8, .9, -14, "#8a2f22", t, .3) + r4)
    # чайник, кружки, снасти, кот, ходики
    s += SL(Z_SRED, chaynik_s_parom(520, 760, .9, t, .3, True))
    s += SL(Z_SRED, kruzhka_moloka(760, 760, .9, t, False, .2, "#d8cbb0")
            + kruzhka_moloka(1160, 760, .9, t, False, .6, "#e8e2d6"))
    s += SL(Z_SRED, snast_kruchki(1420, 756, t, .8, 5, .4))
    s += SL(Z_SRED, kot(900, 1050, t, 1.4, "#3b3430", True))
    s += SL(Z_SRED, hodiki(220, 280, t, 1.3))
    s += SL(Z_SRED, lampa(960, 150, t, 1.5, True) + teplo(960, 180, 440, 360, .52))
    s += SL(Z_SRED, polka_s_bankami(120, 480, 420, t, 47, 4, False))
    s += SL(Z_SRED, ten(dx, dy + 20, 130, 22, .45) + ten(sx_, sy_ + 20, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def dedov_rybackiy_yaschik(t):
    """Чулан: фанерный рыбацкий ящик с брезентовым ремнём на пол-кадра,
    крышка-сиденье вытерта до блеска, на ней круглая коробочка из-под
    леденцов. Дед поднимает крышку, внук заглядывает внутрь."""
    rnd = random.Random(2032)
    s = (f'<rect width="{W}" height="{H}" fill="#241c16"/>')
    s += SL(Z_DAL, doski(0, 0, W, 880, 78, True, "dosk"))
    s += SL(Z_DAL, f'<rect x="0" y="880" width="{W}" height="200" fill="#5f3f27"/>'
            + polovicy(880, "#6b4428"))
    s += SL(Z_DAL, okno_izby(1560, 160, 300, 260, t, None, .55, False, True))
    # ЯЩИК на пол-кадра

    # коробочка из-под леденцов с ягодами на крышке
    s += SL(Z_SRED, f'<ellipse cx="1020" cy="700" rx="90" ry="28" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="1020" cy="684" rx="90" ry="28" fill="#dde3e8"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(7):
        a = i * .9
        s += SL(Z_SRED, f'<circle cx="{1020+54*math.cos(a):.0f}"'
                        f' cy="{684+16*math.sin(a):.0f}" r="11" fill="#c8301f"'
                        f' stroke="#7d1b11" stroke-width="2.6"/>')
    # ДЕД на корточках и ВНУК
    dx, dy, dh = 420, 1050, 480
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, ph=.2, naklon=2.0))
    pod = A.ease(A.seg(t, .6, 1.4))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, -1, dh * .40, -20 - 20 * pod, t,
                              "#4a4038", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, 1, dh * .32, 26, t, "#4a4038", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    vx, vy, vh = 1300, 1056, 450
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#3f5a6a", kant="#ffd98a",
                           shapka=True, ph=.6, naklon=4.0))
    r3, (e3x, e3y), _ = _ruka(vx, vy, vh, -1, vh * .26, 30, t, "#3f5a6a", "#ffd98a", .3, 4)
    r4, (e4x, e4y), _ = _ruka(vx, vy, vh, 1, vh * .26, 34, t, "#3f5a6a", "#ffd98a", .8, 4)
    s += SL(Z_SRED, r3 + varezhka(e3x - 8, e3y + 10, .9, -12, TKAN, t, .3)
            + r4 + varezhka(e4x + 8, e4y + 10, .9, 12, TKAN, t, .8))
    # валенки, удочки, тулуп на гвозде, сачок
    s += SL(Z_SRED, _valenok(160, 1056, 1.3, -4) + _valenok(260, 1060, 1.3, 5))
    for i, ux in enumerate((1560, 1640, 1720)):
        s += SL(Z_SRED, f'<g transform="rotate({-8+i*5} {ux:.0f} 1060)">'
                        f'<rect x="{ux:.0f}" y="420" width="15" height="640" rx="7"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3.6"/></g>')
    s += SL(Z_SRED, f'<path d="M1080,240 q{90:.0f},{-30:.0f} {180:.0f},0 l{20:.0f},{420:.0f}'
                    f' q{-110:.0f},{34:.0f} {-220:.0f},0 Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="5.5"/>'
                    f'<path d="M1080,240 q{90:.0f},{40:.0f} {180:.0f},0" fill="none"'
                    f' stroke="#9a8a62" stroke-width="16"/>'
                    f'<circle cx="1170" cy="220" r="10" fill="{ZHELEZ}" stroke="{K}"'
                    f' stroke-width="3"/>')
    s += SL(Z_SRED, f'<g transform="rotate(14 1880 1000)">'
                    f'<rect x="1874" y="620" width="14" height="380" rx="6"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.4"/>'
                    f'<ellipse cx="1881" cy="600" rx="70" ry="44" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="8"/></g>')
    s += SL(Z_SRED, polka_s_bankami(420, 420, 520, t, 59, 5, False))
    s += SL(Z_SRED, polka_s_bankami(900, 300, 420, t, 61, 4, False))
    for i, (kx2, ky2, ks2) in enumerate(((180, 900, 1.0), (1700, 920, .8), (1480, 880, .9))):
        s += SL(Z_SRED, f'<rect x="{kx2-70*ks2:.0f}" y="{ky2-90*ks2:.0f}"'
                        f' width="{140*ks2:.0f}" height="{90*ks2:.0f}" rx="8"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="{4*ks2:.1f}"/>'
                        f'<path d="M{kx2-70*ks2:.0f},{ky2-60*ks2:.0f} h{140*ks2:.0f}"'
                        f' stroke="#6b4428" stroke-width="{5*ks2:.1f}"/>')
    s += SL(Z_SRED, snast_kruchki(760, 560, t, .9, 6, .3))
    s += SL(Z_SRED, peshnya(1420, 1060, .9, -14, t, .2))
    s += SL(Z_SRED, lampa(760, 150, t, 1.4, False) + teplo(760, 170, 400, 330, .5))
    s += SL(Z_SRED, dvorovye_veschi(1420, 1066, 260, t, 367, ["korzina", "churbak"]))
    s += SL(Z_SRED, ten(dx, dy + 6, 120, 20, .45) + ten(vx, vy + 6, 100, 18, .45))
    # ЯЩИК — главный предмет: рисуется ПОВЕРХ короба и снастей, иначе теряется
    s += SL(Z_PERED, teplo(860, 880, 460, 340, .32)
            + yaschik_rybaka(860, 1010, 3.0, t, A.ease(A.seg(t, .6, 1.4)), .1))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .55))
    s += vinetka(.46)
    return s
