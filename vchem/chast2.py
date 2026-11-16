# -*- coding: utf-8 -*-
"""Декорации ролика «В чём встречать Новый год 2027», часть 2 (планы 35-70).

Ткани и блеск, память о семидесятых, первые два наряда. Все сцены нарисованы
заново под этот текст (R-0019).
"""
import math, random
from baza import *
from lok_obshchee import *
import anim as A


def _polka_melochey(x, y, w_, t, seed, n=7):
    """Полка с мелочью ателье: катушки, напёрстки, флаконы, баночки.

    Этим добирается плотность кадра до нормы (от 60 предметов): своих крупных
    предметов в сцене пять-семь, остальное — обжитой второй план.
    """
    rnd = random.Random(seed)
    s = polka(x, y, w_)
    for i in range(n):
        px = x + w_ * (i + .5) / n + rnd.uniform(-8, 8)
        h_ = rnd.uniform(26, 54)
        c = rnd.choice((KORALL, IZUMRUD, ZOLOTO, MOLOKO, VINO, LAVANDA, BEZH))
        kach = 1.6 * A.w(t, 2.4 + .2 * i, i * .3)
        s += (f'<g transform="rotate({kach:.2f} {px:.0f} {y:.0f})">'
              f'<rect x="{px-11:.0f}" y="{y-h_:.0f}" width="22" height="{h_:.0f}"'
              f' rx="5" fill="{c}" {o(3)}/>'
              f'<rect x="{px-14:.0f}" y="{y-h_-5:.0f}" width="28" height="7"'
              f' rx="3" fill="{SEREBRO}" {o(2)}/></g>')
        s += (f'<path d="M{px:.0f},{y-h_*.5:.0f} q{rnd.uniform(-9,9):.0f},10'
              f' {rnd.uniform(-14,14):.0f},22" fill="none" stroke="{c}"'
              f' stroke-width="2" opacity=".7"/>')
    return s


def _katushki_tk(x, y, t, n=6, seed=11):
    """Катушки ниток россыпью — сквозная мелочь всех швейных сцен."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        cx = x + i * 46 + rnd.uniform(-7, 7)
        cy = y + rnd.uniform(-10, 10)
        c = rnd.choice((ALYY, VINO, IZUMRUD, ZOLOTO, TSINIY, MOLOKO))
        kr = 2.2 * A.w(t, 3.0, i * .4)
        s += (f'<g transform="rotate({kr:.2f} {cx:.0f} {cy:.0f})">'
              f'<rect x="{cx-13:.0f}" y="{cy-26:.0f}" width="26" height="52" rx="6"'
              f' fill="{c}" {o(3)}/>'
              f'<rect x="{cx-16:.0f}" y="{cy-30:.0f}" width="32" height="8" rx="3"'
              f' fill="{DEREVO2}" {o(2)}/>'
              f'<rect x="{cx-16:.0f}" y="{cy+22:.0f}" width="32" height="8" rx="3"'
              f' fill="{DEREVO2}" {o(2)}/></g>')
    return s


def lavandovyy_i_svetlo_seryy(t):
    """Окно, сухая лаванда в кувшине и серый кот; рядом на плечиках лавандовая
    блузка и светло-серая юбка — наряд повторяет то, что уже есть в комнате."""
    rnd = random.Random(2035)
    s = f'<rect width="{W}" height="{H}" fill="#2a2430"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 11))
    s += SL(Z_DAL, doski(0, 0, W, 820, 92))
    s += SL(Z_DAL, okno_izby(1060, 90, 700, 540, t, svet=False, moroz=.30))
    s += SL(Z_DAL, sneg_letit(t, 26, 7, .55, .7))
    s += SL(Z_DAL, zanaveska(1030, 80, 580, 150, "#e4e8f3", t, 1))
    s += SL(Z_DAL, zanaveska(1770, 80, 580, 150, "#e4e8f3", t, -1))
    s += SL(Z_SRED, _polka_melochey(70, 300, 420, t, 35, 6))
    # подоконник
    s += SL(Z_SRED, f'<rect x="1000" y="620" width="860" height="34" rx="8"'
                    f' fill="url(#derev)" {o(6)}/>')
    # кувшин с сухой лавандой: сам букет и есть «лавандовый» оттенок сцены
    kx, ky = 1180, 620
    s += SL(Z_SRED, f'<path d="M{kx-54},{ky} q-16,-96 20,-128 q-8,-26 14,-30'
                    f' q22,4 14,30 q36,32 20,128 Z" fill="url(#glina)" {o(6)}/>')
    for i in range(11):
        a = -74 + i * 9 + 3.2 * A.w(t, 2.2, i * .22)
        dl = rnd.uniform(130, 210)
        ex = kx + dl * math.cos(math.radians(a))
        ey = ky - 150 + dl * math.sin(math.radians(a))
        s += SL(Z_SRED, f'<path d="M{kx},{ky-150} Q{(kx+ex)/2+10:.0f},'
                        f'{(ky-150+ey)/2:.0f} {ex:.0f},{ey:.0f}" fill="none"'
                        f' stroke="#6f7a52" stroke-width="4"/>')
        for j in range(4):
            bx = ex + rnd.uniform(-9, 9)
            by = ey + j * 11
            s += SL(Z_SRED, f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="7" ry="11"'
                            f' fill="{LAVANDA}" opacity=".9"/>')
    # серый кот на пол-кадра: открывает один глаз
    s += SL(0, kot(1560, 620, t, 2.3, SERYY))
    # плечики с лавандовой блузкой и светло-серой юбкой
    s += SL(0, naryad_plechiki(430, 180, 440, t, LAVANDA, 1.25, .1, True, MOLOKO, .10, 21))
    s += SL(0, naryad_plechiki(760, 210, 380, t, "#b9bcc4", 1.15, .5, True, None, .06, 22))
    # стол с книгой, чашкой и салфеткой
    s += SL(Z_SRED, stol(240, 880, 620, 34))
    s += SL(Z_SRED, f'<path d="M300,870 h210 l-10,-54 h-190 Z" fill="{MOLOKO}" {o(4)}/>'
                    f'<path d="M305,845 h196" stroke="{K}" stroke-width="3" opacity=".4"/>')
    s += SL(Z_SRED, f'<path d="M560,872 q-8,-56 34,-58 q42,2 34,58 Z" fill="{KREM2}" {o(4)}/>'
                    f'<path d="M628,838 q26,6 22,26 q-6,16 -24,12" fill="none"'
                    f' stroke="{KREM2}" stroke-width="7"/>')
    s += SL(Z_SRED, par(594, 820, t, 3, .45, 120, .4, .8))
    for i in range(9):
        sx = 300 + i * 26
        s += SL(Z_SRED, f'<path d="M{sx},900 q13,14 26,0" fill="none"'
                        f' stroke="{MOLOKO}" stroke-width="3" opacity=".55"/>')
    s += SL(Z_SRED, svecha(840, 876, t, .3, 1.1))
    s += SL(Z_SRED, _katushki_tk(120, 848, t, 5, 7))
    s += SL(Z_SRED, teplo(840, 820, 420, 330, .26 + .07 * abs(A.w(t, 1.7))))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def albom_obrazcov_tkani(t):
    """Раскрытый альбом образцов: пары лоскутов приподнимаются по очереди и
    получают номер — это и есть действие сцены."""
    rnd = random.Random(2036)
    s = f'<rect width="{W}" height="{H}" fill="#241d19"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 5))
    s += SL(Z_DAL, doski(0, 0, W, 560, 84))
    s += SL(Z_DAL, _polka_melochey(1420, 300, 440, t, 36, 7))
    s += SL(Z_DAL, okno_izby(120, 90, 420, 330, t, svet=False, moroz=.42))
    s += SL(Z_SRED, stol(120, 980, 1700, 44))
    # альбом: два разворота, шесть пар лоскутов
    ax, ay = 420, 540
    s += SL(Z_SRED, f'<path d="M{ax},{ay} q540,-44 1080,0 l0,400 q-540,44 -1080,0 Z"'
                    f' fill="{KREM2}" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M{ax+540},{ay-22} l0,418" stroke="{K}"'
                    f' stroke-width="6" opacity=".55"/>')
    PARY = ((ALYY, MOLOKO), (VINO, ZOLOTO), (IZUMRUD, ZOLOTO),
            (TERRAKOT, BEZH), (TSINIY, SEREBRO), (KORALL, MOLOKO))
    for i, (c1, c2) in enumerate(PARY):
        kol, ryad = i % 3, i // 3
        px = ax + 90 + kol * 320 + ryad * 10
        py = ay + 70 + ryad * 190
        podnyat = A.out(A.seg(t, .4 + i * .35, .8)) if i < 3 else 0.0
        dy = -34 * podnyat
        for j, c in enumerate((c1, c2)):
            lx = px + j * 118
            s += SL(Z_SRED, f'<g transform="translate(0,{dy:.1f})">'
                            f'<path d="M{lx},{py} h104 l-6,132 h-92 Z" fill="{c}" {o(4)}/>'
                            f'{skladki(lx, py, 104, 132, c, 3, 40 + i * 3 + j, t, 2.0)}'
                            f'<circle cx="{lx+52}" cy="{py+8}" r="7" fill="{SEREBRO}" {o(2)}/>'
                            f'</g>')
        if i < 3 and podnyat > .25:
            s += SL(Z_SRED, f'<circle cx="{px+112:.0f}" cy="{py-52+dy:.0f}" r="26"'
                            f' fill="{ZOLOTO}" opacity="{min(1, podnyat):.2f}" {o(3)}/>')
    # мелочь портного вокруг
    s += SL(Z_SRED, _katushki_tk(190, 930, t, 6, 12))
    s += SL(Z_SRED, f'<path d="M1540,950 l120,-34 l10,22 l-120,34 Z" fill="{MOLOKO}" {o(3)}/>')
    for i in range(12):
        s += SL(Z_SRED, f'<path d="M{1546+i*10},{944-i*2.8:.0f} l0,16"'
                        f' stroke="{K}" stroke-width="2" opacity=".55"/>')
    s += SL(Z_SRED, f'<path d="M1420,978 l64,-56 l16,18 l-64,56 Z" fill="{SEREBRO}" {o(3)}/>'
                    f'<circle cx="1414" cy="984" r="15" fill="none" stroke="{SEREBRO}"'
                    f' stroke-width="6"/>')
    s += SL(0, lampa_stolika(1700, 880, t, 1.25))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def magazin_tkaney_vecherom(t):
    """Прилавок магазина тканей: рулоны стеной, продавщица разматывает винный
    отрез, покупательница трогает его рукавом."""
    rnd = random.Random(2038)
    s = f'<rect width="{W}" height="{H}" fill="#2b2119"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 7))
    s += SL(Z_DAL, doski(0, 0, W, 460, 78))
    # стена рулонов
    for i in range(14):
        rx = 70 + i * 132
        h_ = 300 + (i % 4) * 46
        c = (ALYY, VINO, IZUMRUD, TSINIY, TERRAKOT, MOLOKO, KORALL, LAVANDA,
             BEZH, HVOYA, RUBIN, KREM2, SERYY, PUDRA)[i]
        kach = 1.2 * A.w(t, 3.2, i * .2)
        s += SL(Z_DAL, f'<g transform="rotate({kach:.2f} {rx:.0f} 620)">'
                       f'<rect x="{rx-52:.0f}" y="{620-h_:.0f}" width="104" height="{h_:.0f}"'
                       f' rx="22" fill="{c}" {o(5)}/>'
                       f'<ellipse cx="{rx:.0f}" cy="{620-h_:.0f}" rx="52" ry="16"'
                       f' fill="{c}" stroke="{K}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<rect x="0" y="690" width="{W}" height="54" fill="url(#derev)" {o(6)}/>')
    # прилавок
    s += SL(Z_SRED, f'<rect x="120" y="744" width="1680" height="150" rx="10"'
                    f' fill="{DEREVO}" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="120" y="744" width="1680" height="16" fill="#ffffff"'
                    f' opacity=".14"/>')
    # винный отрез разматывается
    raz = A.out(A.seg(t, .3, 2.0))
    s += SL(0, otrez(430, 700, 300 + 620 * raz, 190, VINO, t, 14, .22, .1))
    s += SL(0, tkan_blesk(430, 700, 300 + 620 * raz, 190, t, "#ffffff", .30, .2))
    # продавщица за прилавком, обе руки на рулоне
    s += SL(Z_SRED, figura(320, 760, 420, t, IZUMRUD, TEPLO_SVET, .1, False, False,
                           1.0, 2.5, True, True, "#f0cfae", False, MOLOKO, False))
    ruk, (hx, hy) = rukav(452, 686, 118, -6 + 9 * A.w(t, 1.6), t, IZUMRUD, TEPLO_SVET, .2, 5.0)
    s += SL(Z_SRED, ruk)
    # покупательница перед прилавком, рукав трогает ткань, вторая рука с сумкой
    s += SL(0, figura(1430, 1010, 470, t, TSINIY, HOLOD_KANT, .5, False, False,
                      1.0, 2.0, True, True, "#eec9a6", True, KORALL, True))
    ruk2, (h2x, h2y) = rukav(1330, 836, 150, -170 + 7 * A.w(t, 1.9, .3), t,
                             TSINIY, HOLOD_KANT, .4, 6.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M1520,860 q34,-10 52,18 l12,92 h-96 l12,-92 Z"'
               f' fill="{GRAFIT}" {o(4)}/>')
    # касса, метр, ножницы на шнурке
    s += SL(Z_SRED, f'<rect x="1570" y="610" width="190" height="130" rx="12"'
                    f' fill="{CHUGUN}" {o(6)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<circle cx="{1596+(i%3)*58}" cy="{642+(i//3)*32}" r="11"'
                        f' fill="{KREM2}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M150,744 h260 l0,14 h-260 Z" fill="{MOLOKO}" {o(3)}/>')
    for i in range(13):
        s += SL(Z_SRED, f'<path d="M{160+i*20},744 l0,14" stroke="{K}" stroke-width="2"/>')
    kach = 7 * A.w(t, 2.1, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.2f} 1050 610)">'
                    f'<path d="M1050,610 l0,70" stroke="{BEZH}" stroke-width="4"/>'
                    f'<path d="M1030,680 l40,34 M1070,680 l-40,34" stroke="{SEREBRO}"'
                    f' stroke-width="8" stroke-linecap="round"/></g>')
    s += SL(0, lampa_stolika(1050, 470, t, 1.5))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def pyat_tkaney_na_prilavke(t):
    """Пять отрезов веером: рукав проводит по каждому, и каждый отзывается
    по-своему — бархат темнеет, шифон взлетает, кружево даёт тень, трикотаж
    тянется, атлас пускает блик."""
    rnd = random.Random(2039)
    s = f'<rect width="{W}" height="{H}" fill="#241b15"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 9))
    s += SL(Z_DAL, doski(0, 0, W, 420, 76))
    s += SL(Z_DAL, _polka_melochey(60, 300, 420, t, 39, 6))
    s += SL(Z_DAL, _polka_melochey(1440, 300, 420, t, 41, 6))
    # витрина за прилавком: сначала рисованный вид, потом метка, потом переплёт
    px, py, pw, ph = 570, 120, 780, 300
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#1d2630"/>'
            + otrez(px + 24, py + 30, pw - 48, ph - 70, TSINIY, t, 58, .25, .2)
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-14}" y="{py-14}" width="{pw+28}" height="{ph+28}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="22"/>'
            + f'<path d="M{px+pw/2:.0f},{py-14} l0,{ph+28}" stroke="{DEREVO2}"'
              f' stroke-width="12"/>')
    s += SL(Z_SRED, f'<rect x="0" y="560" width="{W}" height="520" fill="{DEREVO}" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="0" y="560" width="{W}" height="18" fill="#ffffff" opacity=".12"/>')
    TK = ((VINO, "бархат"), (MOLOKO, "шифон"), (KREM2, "кружево"),
          (TERRAKOT, "трикотаж"), (KREM2, "атлас"))
    hod = A.seg(t, .3, 4.2)
    aktiv = min(4, int(hod * 5))
    for i, (c, _) in enumerate(TK):
        x = 150 + i * 330
        ug = -16 + i * 8
        zhiv = (abs(A.w(t, 1.6, i * .3)) if i == aktiv else .18)
        s += SL(Z_SRED, f'<g transform="rotate({ug:.1f} {x+140:.0f} 700)">')
        if i == 0:        # бархат темнеет полосой
            s += SL(Z_SRED, otrez(x, 620, 280, 300, c, t, 50, 0, .1))
            s += SL(Z_SRED, f'<rect x="{x+40+90*zhiv:.0f}" y="620" width="80" height="300"'
                            f' fill="#000000" opacity="{.30*zhiv+.10:.2f}"/>')
        elif i == 1:      # шифон приподнимается
            s += SL(Z_SRED, otrez(x, 600 - 40 * zhiv, 280, 300, c, t, 51, .12, .2))
        elif i == 2:      # кружево бросает узорную тень
            s += SL(Z_SRED, otrez(x, 620, 280, 300, c, t, 52, 0, .3))
            for j in range(18):
                cx = x + 26 + (j % 6) * 44
                cy = 660 + (j // 6) * 74
                s += SL(Z_SRED, f'<circle cx="{cx}" cy="{cy}" r="15" fill="none"'
                                f' stroke="{K}" stroke-width="3" opacity=".45"/>')
                s += SL(Z_SRED, f'<circle cx="{cx+14}" cy="{cy+66}" r="9" fill="{K}"'
                                f' opacity="{.14+.12*zhiv:.2f}"/>')
        elif i == 3:      # трикотаж тянется
            s += SL(Z_SRED, otrez(x, 620, 280 + 54 * zhiv, 300, c, t, 53, 0, .4))
        else:             # атлас пускает блик
            s += SL(Z_SRED, otrez(x, 620, 280, 300, c, t, 54, .5, .5))
            s += SL(Z_SRED, tkan_blesk(x, 620, 280, 300, t, "#ffffff", .55, .5))
        s += SL(Z_SRED, "</g>")
    # рукав покупательницы идёт по тканям
    rx = 190 + 330 * aktiv + 120
    ruk, (hx, hy) = rukav(rx, 420, 190, 74, t, TSINIY, HOLOD_KANT, .2, 5.0, True)
    s += SL(0, ruk)
    s += SL(Z_SRED, _katushki_tk(120, 1010, t, 6, 21))
    s += SL(Z_SRED, f'<path d="M1500,1006 l80,-62 l18,20 l-80,62 Z" fill="{SEREBRO}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1660,1010 h180 l0,12 h-180 Z" fill="{MOLOKO}" {o(3)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{1668+i*20},1010 l0,12" stroke="{K}" stroke-width="2"/>')
    s += SL(0, lampa_stolika(960, 430, t, 1.4))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def barhatnaya_portera(t):
    """Тяжёлая рубиновая портьера с кистью; девочка обнимает её и прижимается
    щекой. В раме у окна — настоящий рубиновый бархат."""
    rnd = random.Random(2040)
    s = f'<rect width="{W}" height="{H}" fill="#1e1512"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 13))
    s += SL(Z_DAL, stena("oboi", t, 105))
    s += SL(Z_DAL, sneg_letit(t, 22, 9, .45, .6))
    # место настоящего кадра: рама портьеры у окна слева, 800x420 стоймя
    # НАСТОЯЩИЙ КАДР ОТСЮДА СНЯТ: клип бархата был почти чёрным и читался бы
    # пустой рамкой (гейт «в окне нет почти чёрного клипа»). Рисованный бархат
    # в раме остаётся — сцена от этого не беднеет.
    px, py, pw, ph = 60, 300, 780, 420
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#2a0d14"/>'
                    + otrez(px + 20, py + 16, pw - 40, ph - 40, RUBIN, t, 61, .18, .2)
                    + skladki(px + 40, py + 40, pw - 80, ph - 90, RUBIN, 7, 62, t, 4.0)
                    + zerkalo(px, py, pw, ph, t, "pryam", DEREVO2, True))
    # сама портьера справа, на пол-кадра
    for i in range(9):
        fx = 880 + i * 86
        tem = .22 + .22 * (0.5 + 0.5 * math.cos(2 * math.pi * ((t * .35 + i * .12) % 1.0)))
        s += SL(0, f'<path d="M{fx},180 q{18+8*A.w(t,2.6,i*.2):.0f},440 {-6:.0f},880'
                   f' l78,0 q{-10:.0f},-440 {-12:.0f},-880 Z" fill="{RUBIN}" {o(5)}/>')
        s += SL(0, f'<path d="M{fx},180 q{18:.0f},440 {-6:.0f},880 l78,0'
                   f' q{-10:.0f},-440 {-12:.0f},-880 Z" fill="#000000"'
                   f' opacity="{tem*.5:.2f}"/>')
    s += SL(0, f'<rect x="860" y="150" width="800" height="46" rx="12"'
               f' fill="{DEREVO2}" {o(6)}/>')
    # шнур с кистью
    kx = 1320
    kach = 6 * A.w(t, 1.9, .1)
    s += SL(0, f'<g transform="rotate({kach:.2f} {kx} 560)">'
               f'<path d="M{kx-180},560 q180,52 360,0" fill="none" stroke="{ZOLOTO}"'
               f' stroke-width="12"/>'
               f'<path d="M{kx},600 l0,56" stroke="{ZOLOTO}" stroke-width="10"/>'
               f'<path d="M{kx-44},656 h88 l-14,96 h-60 Z" fill="{ZOLOTO}" {o(4)}/>')
    for i in range(7):
        s += SL(0, f'<path d="M{kx-36+i*12},752 l{-2+i*.6:.1f},44" stroke="{ZOLOTO}"'
                   f' stroke-width="4"/>')
    s += SL(0, "</g>")
    # девочка обнимает портьеру и прижимается щекой
    s += SL(0, figura(860, 1020, 380, t, IZUMRUD, TEPLO_SVET, .3, False, True,
                      1.0, 3.5, True, True, "#f3d3b2", True, MOLOKO, True))
    ruk, _ = rukav(916, 800, 128, -24, t, IZUMRUD, TEPLO_SVET, .2, 4.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(916, 848, 120, 8, t, IZUMRUD, TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    # комната: кресло, торшер, рояль, ёлка
    s += SL(Z_SRED, f'<path d="M820,1030 q-30,-180 70,-186 l0,186 Z" fill="#4a3a52" {o(5)}/>')
    s += SL(Z_DAL, elka(1840, 1040, 420, t, 1.0, True, 17))
    s += SL(Z_DAL, f'<rect x="300" y="880" width="520" height="150" rx="10"'
                   f' fill="#1b1b22" {o(6)}/>')
    for i in range(16):
        s += SL(Z_DAL, f'<rect x="{320+i*30}" y="884" width="20" height="40"'
                       f' fill="{MOLOKO}" {o(2)}/>')
    s += SL(Z_SRED, girlyanda(140, 180, 760, t, 8, 23, 56))
    s += SL(Z_SRED, lampa_stolika(960, 900, t, 1.1))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.46)
    return s


def shifon_i_trikotazh(t):
    """Кадр надвое: слева шифоновая блузка у балкона, справа трикотажное
    платье само садится по форме манекена."""
    rnd = random.Random(2041)
    s = f'<rect width="{W}" height="{H}" fill="#262029"/>'
    s += SL(Z_NEBO, nebo("sumer", t, False, 15))
    s += SL(Z_DAL, stena("kraska", t, 106))
    s += SL(Z_DAL, f'<path d="M960,0 l0,1080" stroke="{K}" stroke-width="6" opacity=".35"/>')
    # ЛЕВО: балконная дверь, за ней вечер и снег; ветер тянет ткань
    s += SL(Z_DAL, f'<rect x="150" y="150" width="620" height="760" rx="14"'
                   f' fill="#121a24" {o(7)}/>')
    s += SL(Z_DAL, sneg_letit(t, 30, 3, .6, .9))
    s += SL(Z_DAL, f'<rect x="150" y="150" width="620" height="760" rx="14" fill="none"'
                   f' stroke="{DEREVO2}" stroke-width="18"/>')
    s += SL(Z_DAL, f'<path d="M460,150 l0,760" stroke="{DEREVO2}" stroke-width="12"/>')
    for i in range(5):
        oy = 300 + i * 120
        s += SL(Z_DAL, f'<path d="M170,{oy} q200,{-26+10*A.w(t,2.2,i*.3):.0f} 580,0"'
                       f' fill="none" stroke="{MOLOKO}" stroke-width="3" opacity=".22"/>')
    veter = A.w(t, 1.8)
    s += SL(0, naryad_plechiki(420, 250, 430, t, MOLOKO, 1.2, .2, True, None, .18, 31, 5.0))
    for i in range(6):
        ax = 300 + i * 46
        s += SL(0, f'<path d="M{ax},420 q{40+26*veter:.0f},90 {24+34*veter:.0f},190"'
                   f' fill="none" stroke="{MOLOKO}" stroke-width="5" opacity=".55"/>')
    # ПРАВО: манекен, трикотажное платье садится по форме
    sad = A.out(A.seg(t, .45, 1.5))
    s += SL(0, manekken(1420, 980, 700, t, KREM2, "zh",
                        TERRAKOT if sad > .25 else None, .3, None, .06, 33))
    s += SL(0, f'<path d="M{1420-170-60*(1-sad):.0f},{430-70*(1-sad):.0f}'
               f' q{170+60*(1-sad):.0f},-40 {340+120*(1-sad):.0f},0'
               f' l-30,{90+40*(1-sad):.0f} q-150,30 -300,0 Z"'
               f' fill="{TERRAKOT}" opacity="{.35+.6*(1-sad):.2f}" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(1680, 260, 200, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1690" y="270" width="180" height="500" fill="{STEKLO}"'
                    f' opacity=".30"/>')
    s += SL(Z_SRED, f'<path d="M1740,420 q40,-16 80,0 l-14,320 h-54 Z" fill="{KREM2}"'
                    f' opacity=".55"/>')
    # обжитый второй план: стул, корзина, цветок, коробки
    s += SL(Z_SRED, f'<rect x="1020" y="760" width="150" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="1030" y="786" width="18" height="240" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1142" y="786" width="18" height="240" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1026" y="600" width="140" height="170" rx="8"'
                    f' fill="{DEREVO2}" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M820,1030 q-26,-130 58,-134 q84,4 58,134 Z"'
                    f' fill="url(#solom)" {o(5)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{806+i*22},940 l0,90" stroke="{MED}"'
                        f' stroke-width="3" opacity=".6"/>')
    s += SL(Z_SRED, f'<path d="M1240,1030 l0,-120" stroke="#3e5a3a" stroke-width="10"/>')
    for i in range(5):
        a = -60 + i * 30 + 4 * A.w(t, 2.6, i * .3)
        s += SL(Z_SRED, f'<ellipse cx="{1240+58*math.cos(math.radians(a)):.0f}"'
                        f' cy="{900+40*math.sin(math.radians(a)):.0f}" rx="30" ry="16"'
                        f' fill="#3e5a3a" {o(3)}/>')
    s += SL(Z_SRED, girlyanda(1000, 120, 860, t, 9, 37, 50))
    s += SL(Z_SRED, lampa_stolika(1120, 700, t, 1.0))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def tkan_na_oschup(t):
    """Четыре отреза, рукав ложится на каждый: над шерстью, вискозой и шёлком
    всплывают облачка-подушки, над синтетикой — ёжик с молниями."""
    rnd = random.Random(2042)
    s = f'<rect width="{W}" height="{H}" fill="#221c17"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 17))
    s += SL(Z_DAL, doski(0, 0, W, 480, 82))
    s += SL(Z_DAL, _polka_melochey(1400, 290, 460, t, 42, 7))
    s += SL(Z_SRED, stol(80, 1000, 1760, 46))
    CV = (BEZH, LAVANDA, KREM2, "#5f6b7a")
    hod = A.seg(t, .3, 4.0)
    akt = min(3, int(hod * 4))
    for i, c in enumerate(CV):
        x = 130 + i * 430
        s += SL(Z_SRED, otrez(x, 640, 360, 330, c, t, 70 + i, .10 if i == 2 else 0, i * .2))
        if i == 3:
            top = abs(A.w(t, 1.4)) if i == akt else .25
            for j in range(16):
                jx = x + 20 + j * 21
                s += SL(Z_SRED, f'<path d="M{jx},640 l{4-8*(j%2)},{-26-20*top:.0f}"'
                                f' stroke="#5f6b7a" stroke-width="5"/>')
    # рукав ведёт по тканям
    rx = 310 + 430 * akt
    ruk, (hx, hy) = rukav(rx, 330, 250, 86, t, VINO, TEPLO_SVET, .2, 4.0, True)
    s += SL(0, ruk)
    # облачка-подушки над мягкими и ёжик с молниями над синтетикой
    for i in range(3):
        if i > akt:
            continue
        ox = 310 + i * 430
        p = A.out(A.seg(t, .5 + i * .5, .7))
        s += SL(0, f'<g opacity="{p:.2f}">'
                   f'<ellipse cx="{ox}" cy="{540-40*p:.0f}" rx="118" ry="66"'
                   f' fill="{MOLOKO}" {o(4)}/>'
                   f'<ellipse cx="{ox-64}" cy="{566-40*p:.0f}" rx="62" ry="42"'
                   f' fill="{MOLOKO}" {o(3)}/>'
                   f'<ellipse cx="{ox+68}" cy="{566-40*p:.0f}" rx="56" ry="38"'
                   f' fill="{MOLOKO}" {o(3)}/></g>')
    if akt == 3:
        ex, ey = 1600, 520
        p = abs(A.w(t, 1.2))
        s += SL(0, f'<ellipse cx="{ex}" cy="{ey}" rx="96" ry="72" fill="#6b5a46" {o(4)}/>')
        for j in range(16):
            a = -170 + j * 21
            s += SL(0, f'<path d="M{ex+86*math.cos(math.radians(a)):.0f},'
                       f'{ey+64*math.sin(math.radians(a)):.0f}'
                       f' l{(26+12*p)*math.cos(math.radians(a)):.0f},'
                       f'{(26+12*p)*math.sin(math.radians(a)):.0f}"'
                       f' stroke="#4a3b2c" stroke-width="6" stroke-linecap="round"/>')
        for j in range(4):
            zx = ex - 150 + j * 100
            s += SL(0, f'<path d="M{zx},{ey+120} l26,44 l-18,6 l30,56 l-44,-50 l20,-8 Z"'
                       f' fill="{ZOLOTO}" opacity="{.4+.5*p:.2f}"/>')
    s += SL(Z_SRED, _katushki_tk(140, 1046, t, 5, 31))
    s += SL(Z_SRED, f'<path d="M1520,1040 l90,-66 l18,22 l-90,66 Z" fill="{SEREBRO}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1300,1052 q46,-26 92,0" fill="none" stroke="{SEREBRO}"'
                    f' stroke-width="5"/>')
    s += SL(0, lampa_stolika(900, 470, t, 1.35))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def ladon_na_tkani_i_vecher(t):
    """Рукав-варежка отдыхает на винной ткани, и над ним вырастает картинка
    вечера: та же женщина за праздничным столом, стрелки бегут к полуночи."""
    rnd = random.Random(2043)
    s = f'<rect width="{W}" height="{H}" fill="#241a18"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 19))
    s += SL(Z_DAL, doski(0, 0, W, 520, 80))
    s += SL(Z_DAL, _polka_melochey(80, 300, 400, t, 43, 6))
    s += SL(Z_SRED, stol(60, 1010, 1800, 46))
    s += SL(Z_SRED, otrez(180, 700, 820, 300, VINO, t, 44, .14, .1))
    # варежка-ладонь лежит и не уходит
    mx, my = 560, 700
    dy = 6 * A.w(t, 1.1)
    s += SL(0, f'<g transform="translate(0,{dy:.1f})">'
               f'<ellipse cx="{mx}" cy="{my+30}" rx="150" ry="86" fill="{GRAFIT}" {o(6)}/>'
               f'<ellipse cx="{mx-96}" cy="{my+58}" rx="54" ry="44" fill="{GRAFIT}" {o(4)}/>'
               f'<path d="M{mx+110},{my-20} q90,-30 150,-130" fill="none"'
               f' stroke="{GRAFIT}" stroke-width="64" stroke-linecap="round"/></g>')
    # картинка вечера растёт над рукой
    p = A.out(A.seg(t, .35, 1.5))
    kx, ky, kw, kh = 1060, 220, 740, 480
    s += SL(0, f'<g opacity="{p:.2f}" transform="translate({kx+kw/2:.0f},{ky+kh/2:.0f})'
               f' scale({.6+.4*p:.2f}) translate({-kx-kw/2:.0f},{-ky-kh/2:.0f})">')
    s += SL(0, f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="22"'
               f' fill="#2d2230" {o(6)}/>')
    s += SL(0, f'<rect x="{kx+28}" y="{ky+300}" width="{kw-56}" height="30" rx="8"'
               f' fill="{MOLOKO}" {o(4)}/>')
    for i in range(6):
        s += SL(0, f'<circle cx="{kx+90+i*110}" cy="{ky+288}" r="18" fill="{KREM2}" {o(2)}/>')
    s += SL(0, figura(kx + 250, ky + 300, 250, t, VINO, TEPLO_SVET, .2, False, False,
                      1.0, 1.5, True, True, "#f0cfae", True, ZOLOTO, False))
    s += SL(0, f'<path d="{kontur_proema(kx+360, ky+150, 110, 130, "ellips")}"'
               f' fill="{STEKLO}" opacity=".6"/>')
    # часы над столом: стрелки бегут к полуночи
    cx2, cy2 = kx + 580, ky + 120
    s += SL(0, f'<circle cx="{cx2}" cy="{cy2}" r="78" fill="{MOLOKO}" {o(5)}/>')
    for i in range(12):
        a = i * 30
        s += SL(0, f'<path d="M{cx2+62*math.cos(math.radians(a)):.0f},'
                   f'{cy2+62*math.sin(math.radians(a)):.0f} l'
                   f'{10*math.cos(math.radians(a)):.0f},'
                   f'{10*math.sin(math.radians(a)):.0f}" stroke="{K}" stroke-width="4"/>')
    beg = -90 + 320 * A.seg(t, .6, 1.8)
    s += SL(0, f'<path d="M{cx2},{cy2} l{54*math.cos(math.radians(beg)):.0f},'
               f'{54*math.sin(math.radians(beg)):.0f}" stroke="{K}" stroke-width="7"'
               f' stroke-linecap="round"/>')
    s += SL(0, f'<path d="M{cx2},{cy2} l0,-38" stroke="{K}" stroke-width="9"'
               f' stroke-linecap="round"/>')
    s += SL(0, "</g>")
    s += SL(Z_SRED, _katushki_tk(1180, 1046, t, 5, 47))
    s += SL(Z_SRED, f'<path d="M1420,1046 l88,-64 l18,22 l-88,64 Z" fill="{SEREBRO}" {o(3)}/>')
    s += SL(Z_SRED, svecha(1660, 1006, t, .2, 1.3))
    s += SL(0, lampa_stolika(300, 640, t, 1.2))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.44)
    return s


def tri_muzhskie_tkani(t):
    """Три мужских торса в ряд: вельвет, шерсть, твид. Мужское ателье вокруг —
    зеркало, галстуки, колодки, утюг с паром."""
    rnd = random.Random(2044)
    s = f'<rect width="{W}" height="{H}" fill="#241e18"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 23))
    s += SL(Z_DAL, stena("oboi", t, 109))
    s += SL(Z_DAL, _polka_melochey(60, 280, 420, t, 44, 6))
    # полка с галстуками
    gal = polka(1420, 300, 440)
    for i in range(7):
        gx = 1452 + i * 60
        kach = 3.4 * A.w(t, 2.4, i * .3)
        c = (VINO, TSINIY, IZUMRUD, GRAFIT, RUBIN, HVOYA, TERRAKOT)[i]
        gal += (f'<g transform="rotate({kach:.2f} {gx} 300)">'
                f'<path d="M{gx-13},300 l26,0 l-5,150 l-16,0 Z" fill="{c}" {o(3)}/>'
                f'<path d="M{gx-10},300 l20,0 l-4,26 l-12,0 Z" fill="#ffffff" opacity=".2"/>'
                f'</g>')
    s += SL(Z_DAL, gal)
    s += SL(Z_SRED, polovicy(1010))
    TK = ((TERRAKOT, "вельвет"), (GRAFIT, "шерсть"), (BEZH, "твид"))
    for i, (c, _) in enumerate(TK):
        x = 400 + i * 440
        s += SL(0, manekken(x, 960, 620, t, KREM2, "m", c, i * .3, MOLOKO, .05, 50 + i))
        if i == 0:                      # рубчик вельвета
            rub = "".join(f'<path d="M{x-150+j*14},520 l0,230" stroke="#8c3f22"'
                          f' stroke-width="3" opacity=".55"/>' for j in range(22))
            s += SL(0, rub)
        elif i == 2:                    # мелкая клетка твида
            kl = "".join(f'<path d="M{x-150+j*26},520 l0,230" stroke="#9a8460"'
                         f' stroke-width="2" opacity=".5"/>' for j in range(12))
            kl += "".join(f'<path d="M{x-150},{530+j*26} l300,0" stroke="#9a8460"'
                          f' stroke-width="2" opacity=".5"/>' for j in range(9))
            s += SL(0, kl)
        pod = A.out(A.seg(t, .4 + i * .3, .7))
        s += SL(0, f'<rect x="{x-110:.0f}" y="{300-30*pod:.0f}" width="220" height="56"'
                   f' rx="10" fill="{GRAFIT}" opacity="{pod*.9:.2f}" {o(3)}/>')
    # утюг с паром и гладильная доска
    s += SL(Z_SRED, f'<path d="M1560,900 l250,-30 l10,70 l-250,30 Z" fill="{MOLOKO}" {o(6)}/>'
                    f'<path d="M1600,970 l0,110 M1770,952 l0,128" stroke="{SEREBRO}"'
                    f' stroke-width="9"/>')
    s += SL(Z_SRED, f'<path d="M1640,884 q60,-44 120,-6 l6,34 l-130,16 Z"'
                    f' fill="{CHUGUN}" {o(5)}/>')
    s += SL(Z_SRED, par(1700, 864, t, 4, .5, 150, .45, 1.0))
    s += SL(Z_SRED, zerkalo(120, 420, 240, 560, t, "pryam", DEREVO2, True))
    s += SL(Z_SRED, f'<rect x="130" y="430" width="220" height="540" fill="{STEKLO}"'
                    f' opacity=".25"/>')
    kol = "".join(f'<path d="M{150+i*74},1006 q40,-66 84,-6 q-42,26 -84,6 Z"'
                  f' fill="{DEREVO2}" {o(3)}/>' for i in range(4))
    s += SL(Z_SRED, kol)
    s += SL(Z_SRED, girlyanda(60, 150, 1800, t, 11, 61, 62))
    s += SL(0, lampa_stolika(1180, 420, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def atlasnaya_bluzka_pod_lampoy(t):
    """Атласная блузка под лампой: по ней идёт мягкая волна света. В овальном
    зеркале на подставке — настоящий атлас."""
    rnd = random.Random(2046)
    s = f'<rect width="{W}" height="{H}" fill="#2a2026"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 27))
    s += SL(Z_DAL, stena("kraska", t, 110))
    s += SL(Z_DAL, elka(1840, 1060, 360, t, 1.0, True, 29))
    s += SL(Z_SRED, trumo(980, 1010, 820, 420, t))
    # овальное зеркало на подставке: сначала рисованный вид, потом метка, потом рама
    px, py, pw, ph = 170, 360, 420, 380
    put = kontur_proema(px, py, pw, ph, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#2b2420"/>'
            + otrez(px + 40, py + 60, pw - 80, ph - 140, KREM2, t, 62, .45, .2)
            + mesto_stoka(px, py, pw, ph, "ellips")
            + zerkalo(px, py, pw, ph, t, "ellips", ZOLOTO, True))
    s += SL(Z_SRED, f'<path d="M{px+pw/2-24:.0f},{py+ph:.0f} h48 l20,120 h-88 Z"'
                    f' fill="{DEREVO2}" {o(4)}/>')
    # блузка на плечиках под лампой
    s += SL(0, naryad_plechiki(880, 230, 520, t, KREM2, 1.4, .1, True, MOLOKO, .5, 63, 1.6))
    volna = (A.w(t, 3.6, .1) + 1) / 2
    s += SL(0, f'<path d="M{700+520*volna:.0f},280 q40,220 -30,480" fill="none"'
               f' stroke="#ffffff" stroke-width="54" opacity=".16"/>')
    # столик: флаконы, бусы, свеча, шарф сползает
    fl = ""
    for i in range(6):
        fx = 1180 + i * 92
        h_ = 54 + (i % 3) * 26
        fl += (f'<rect x="{fx-20}" y="{760-h_}" width="40" height="{h_}" rx="8"'
               f' fill="{(LAVANDA, KORALL, MOLOKO, ZOLOTO, PUDRA, IZUMRUD)[i]}" {o(3)}/>'
               f'<rect x="{fx-9}" y="{748-h_}" width="18" height="16" rx="4"'
               f' fill="{SEREBRO}" {o(2)}/>')
    s += SL(Z_SRED, fl)
    bus = ""
    for i in range(16):
        a = i * 22
        bus += (f'<circle cx="{1120+130*math.cos(math.radians(a)):.0f}"'
                f' cy="{800+34*math.sin(math.radians(a)):.0f}" r="11"'
                f' fill="{KORALL}" {o(2)}/>')
    s += SL(Z_SRED, bus)
    s += SL(Z_SRED, svecha(1760, 756, t, .2, 1.4))
    spolz = A.out(A.seg(t, .6, 1.6))
    s += SL(0, f'<path d="M1480,770 q70,{40+120*spolz:.0f} 20,{220+160*spolz:.0f}'
               f' l64,14 q46,{-150-160*spolz:.0f} -16,{-240-120*spolz:.0f} Z"'
               f' fill="{VINO}" {o(5)}/>')
    s += SL(0, lampa_stolika(880, 190, t, 1.6))
    s += SL(Z_SRED, teplo(880, 320, 520, 420, .30 + .08 * abs(A.w(t, 1.8))))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def nit_i_payetki(t):
    """Швейный столик: игла ведёт блестящую нить по вороту, на воротник
    ложится десяток пайеток, не больше."""
    rnd = random.Random(2047)
    s = f'<rect width="{W}" height="{H}" fill="#201a16"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 31))
    s += SL(Z_DAL, doski(0, 0, W, 520, 80))
    s += SL(Z_DAL, _polka_melochey(1400, 280, 460, t, 47, 7))
    s += SL(Z_SRED, stol(80, 1000, 1760, 48))
    # платье на столе, крупно — ворот в центре
    s += SL(Z_SRED, otrez(420, 620, 900, 380, TSINIY, t, 64, .08, .1))
    s += SL(0, f'<path d="M760,640 q110,120 220,0 q-26,96 -110,104 q-84,-8 -110,-104 Z"'
               f' fill="{TSINIY}" stroke="{K}" stroke-width="6"/>')
    # катушка блестящей нити крутится
    kx, ky = 300, 840
    kr = t * 180
    s += SL(0, f'<g transform="rotate({kr:.1f} {kx} {ky})">'
               f'<ellipse cx="{kx}" cy="{ky}" rx="86" ry="86" fill="{ZOLOTO}" {o(5)}/>'
               f'<ellipse cx="{kx}" cy="{ky}" rx="34" ry="34" fill="{DEREVO2}" {o(4)}/>'
               f'<path d="M{kx-86},{ky} h172" stroke="#ffffff" stroke-width="4"'
               f' opacity=".35"/></g>')
    # игла ведёт нить
    p = A.seg(t, .3, 2.6)
    ix = 700 + 460 * p
    s += SL(0, f'<path d="M{kx+70},{ky-30} Q{(kx+ix)/2:.0f},640 {ix:.0f},700"'
               f' fill="none" stroke="{ZOLOTO}" stroke-width="4"/>')
    s += SL(0, f'<path d="M{ix:.0f},700 l54,-40" stroke="{SEREBRO}" stroke-width="7"'
               f' stroke-linecap="round"/>')
    ruk, _ = rukav(ix + 140, 480, 170, 118, t, VINO, TEPLO_SVET, .2, 4.0, True)
    s += SL(0, ruk)
    ruk2, _ = rukav(640, 500, 160, 96, t, VINO, TEPLO_SVET, .6, 4.0, True)
    s += SL(0, ruk2)
    # пайетки ложатся по одной, их ровно десять
    pay = ""
    for i in range(10):
        if p < (i + 1) / 12.0:
            continue
        a = -74 + i * 16
        pay += (f'<circle cx="{870+96*math.cos(math.radians(a)):.0f}"'
                f' cy="{700+70*math.sin(math.radians(a)):.0f}" r="13"'
                f' fill="{SEREBRO}" opacity="{.7+.3*abs(A.w(t, 1.8, i*.2)):.2f}" {o(2)}/>')
    s += SL(0, pay)
    # блюдце с пайетками, игольница, напёрсток, ножницы
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="880" rx="140" ry="54" fill="{MOLOKO}" {o(5)}/>')
    bl = "".join(f'<circle cx="{1400+rnd.randint(0,200)}" cy="{860+rnd.randint(0,40)}"'
                 f' r="10" fill="{SEREBRO}" {o(2)}/>' for _ in range(16))
    s += SL(Z_SRED, bl)
    s += SL(Z_SRED, f'<ellipse cx="1700" cy="960" rx="62" ry="48" fill="{KORALL}" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{1660+i*18},940 l6,-30" stroke="{SEREBRO}"'
                            f' stroke-width="3"/>' for i in range(5)))
    s += SL(Z_SRED, _katushki_tk(140, 1046, t, 6, 71))
    s += SL(0, lampa_stolika(1180, 420, t, 1.4))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def blestit_chto_to_odno(t):
    """Манекен в матовом тёмном наряде: блестит по очереди что-то одно, а на
    попытку включить всё сразу манекен вспыхивает ёлкой."""
    rnd = random.Random(2048)
    s = f'<rect width="{W}" height="{H}" fill="#1f1c24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 33))
    s += SL(Z_DAL, stena("doski", t, 112))
    s += SL(Z_DAL, elka(120, 1050, 460, t, 1.0, True, 35))
    s += SL(Z_SRED, polovicy(1030))
    s += SL(0, manekken(900, 1000, 720, t, KREM2, "zh", GRAFIT, .2, None, .04, 72))
    hod = A.seg(t, .3, 3.4)
    etap = min(4, int(hod * 5))
    yar = .55 + .45 * abs(A.w(t, 1.5))
    # 0 юбка · 1 жакет · 2 сумочка · 3 туфли · 4 всё сразу
    if etap in (0, 4):
        s += SL(0, f'<path d="M740,640 L690,980 q210,40 420,0 L1060,640 Z"'
                   f' fill="{SEREBRO}" opacity="{yar:.2f}" {o(4)}/>')
    if etap in (1, 4):
        s += SL(0, f'<path d="M760,420 h280 l24,250 h-328 Z" fill="{SEREBRO}"'
                   f' opacity="{yar:.2f}" {o(4)}/>')
    if etap in (2, 4):
        s += SL(0, f'<path d="M1120,560 q40,-14 62,16 l14,96 h-96 Z" fill="{ZOLOTO}"'
                   f' opacity="{yar:.2f}" {o(3)}/>')
    if etap in (3, 4):
        s += SL(0, tufli(1260, 1010, 1.3, SEREBRO, t))
    if etap == 4:
        for i in range(14):
            a = i * 26
            s += SL(0, f'<circle cx="{900+300*math.cos(math.radians(a)):.0f}"'
                       f' cy="{700+300*math.sin(math.radians(a)):.0f}" r="16"'
                       f' fill="{ZOLOTO}" opacity="{.3+.6*abs(A.w(t,1.1,i*.2)):.2f}"/>')
        s += SL(0, teplo(900, 700, 520, 480, .45))
    ruk, _ = rukav(640, 560, 180, 20, t, VINO, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    # зеркало «зажмуривается» на вспышке
    zm = 1.0 if etap < 4 else .22
    s += SL(Z_SRED, zerkalo(1480, 300, 360, 620, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1492" y="312" width="336" height="{596*zm:.0f}"'
                    f' fill="{STEKLO}" opacity=".32"/>')
    s += SL(Z_SRED, f'<path d="M1500,{312+596*zm:.0f} h320" stroke="{K}"'
                    f' stroke-width="10" opacity=".7"/>')
    s += SL(Z_SRED, f'<path d="M300,1030 q-26,-170 66,-176 l0,176 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, shtanga(420, 1030, 300, t, 380))
    s += SL(Z_SRED, girlyanda(60, 140, 1800, t, 12, 73, 64))
    s += SL(0, lampa_stolika(1700, 980, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def blestyaschee_i_matovoe_plate(t):
    """Два манекена рядом: у блестящего стрелки расходятся, у матового
    сходятся. Портниха показывает на правый."""
    rnd = random.Random(2049)
    s = f'<rect width="{W}" height="{H}" fill="#221f26"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 37))
    s += SL(Z_DAL, stena("oboi", t, 113))
    s += SL(Z_DAL, _polka_melochey(60, 270, 400, t, 49, 6))
    s += SL(Z_SRED, polovicy(1030))
    s += SL(0, manekken(470, 1000, 660, t, KREM2, "zh", SEREBRO, .1, None, .55, 74))
    s += SL(0, manekken(1410, 1000, 660, t, KREM2, "zh", TSINIY, .4, None, .03, 75))
    raz = A.out(A.seg(t, .4, 1.4))
    for sgn in (-1, 1):
        s += SL(0, f'<path d="M{470+sgn*(150+90*raz):.0f},700 l{sgn*86:.0f},0'
                   f' l{-sgn*26:.0f},-30 l{sgn*26:.0f},30 l{-sgn*26:.0f},30 Z"'
                   f' fill="{KORALL}" {o(3)}/>')
        s += SL(0, f'<path d="M{1410+sgn*(240-90*raz):.0f},700 l{-sgn*86:.0f},0'
                   f' l{sgn*26:.0f},-30 l{-sgn*26:.0f},30 l{sgn*26:.0f},30 Z"'
                   f' fill="{IZUMRUD}" {o(3)}/>')
    # серьги на подставке и сумочка у матового
    s += SL(0, f'<ellipse cx="1620" cy="760" rx="70" ry="46" fill="{VINO}" {o(4)}/>')
    for sgn in (-1, 1):
        s += SL(0, f'<path d="M{1620+sgn*26},740 l0,-44" stroke="{ZOLOTO}"'
                   f' stroke-width="5"/>'
                   f'<circle cx="{1620+sgn*26}" cy="{700-6*abs(A.w(t,1.7,sgn*.2)):.0f}"'
                   f' r="15" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(0, f'<path d="M1700,860 q42,-14 64,18 l14,100 h-100 Z" fill="{GRAFIT}" {o(4)}/>')
    # портниха между манекенами: правая рука показывает вправо
    s += SL(0, figura(940, 1020, 430, t, HVOYA, TEPLO_SVET, .3, False, False, 1.0,
                      2.0, True, True, "#eec9a6", False, MOLOKO, True))
    ruk, (hx, hy) = rukav(1020, 790, 190, -12 + 8 * A.w(t, 1.7), t, HVOYA, TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    s += SL(0, f'<path d="M900,700 q40,-10 80,0 l0,16 q-40,10 -80,0 Z" fill="{MOLOKO}"'
               f' {o(3)}/>')
    for i in range(6):
        s += SL(0, f'<path d="M{906+i*14},700 l0,16" stroke="{K}" stroke-width="2"/>')
    # очки
    s += SL(0, f'<circle cx="918" cy="628" r="20" fill="none" stroke="{SEREBRO}"'
               f' stroke-width="5"/><circle cx="966" cy="628" r="20" fill="none"'
               f' stroke="{SEREBRO}" stroke-width="5"/>'
               f'<path d="M938,628 h8" stroke="{SEREBRO}" stroke-width="4"/>')
    s += SL(Z_SRED, stol(60, 1020, 320, 34))
    s += SL(Z_SRED, _katushki_tk(90, 980, t, 5, 77))
    s += SL(Z_SRED, zerkalo(1760, 280, 150, 620, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(80, 150, 1760, t, 11, 79, 58))
    s += SL(0, lampa_stolika(240, 940, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def mamina_koftochka_s_lyureksom(t):
    """Комната семидесятых: мамина кофточка искрится люрексом, дочка трогает
    блестящий рукав. Сервант, проигрыватель, ёлка с дождиком."""
    rnd = random.Random(2050)
    s = f'<rect width="{W}" height="{H}" fill="#2b2119"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 41))
    s += SL(Z_DAL, stena("paneli", t, 114))
    # ковёр на стене — примета семидесятых
    s += SL(Z_DAL, f'<rect x="60" y="180" width="720" height="520" rx="8"'
                   f' fill="#7a3b2a" {o(6)}/>')
    uz = ""
    for i in range(5):
        for j in range(4):
            cx, cy = 150 + i * 140, 260 + j * 120
            uz += (f'<path d="M{cx},{cy-40} l34,40 l-34,40 l-34,-40 Z" fill="#c9a06a"'
                   f' opacity=".75"/>')
    s += SL(Z_DAL, uz)
    s += SL(Z_DAL, kvartira_veschi(1180, 700, 700, t, 11))
    s += SL(Z_SRED, polovicy(1020))
    s += SL(Z_DAL, elka(1740, 1040, 420, t, 1.0, True, 43))
    dozhd = ""
    for i in range(18):
        dx = 1600 + rnd.randint(0, 280)
        dy = 700 + rnd.randint(0, 300)
        dozhd += (f'<path d="M{dx},{dy} l0,54" stroke="{SEREBRO}" stroke-width="3"'
                  f' opacity="{.35+.5*abs(A.w(t,1.6,i*.2)):.2f}"/>')
    s += SL(Z_DAL, dozhd)
    # мама: обе руки поправляют причёску — обе рукава внешние
    s += SL(0, figura(760, 1010, 520, t, "#6a5b73", TEPLO_SVET, .2, False, False,
                      1.0, 2.0, True, True, "#f0cfae", False, None, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(760 + sgn * 86, 700, 150, -70 - sgn * 16, t, "#6a5b73",
                       TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    isk = ""
    for i in range(26):
        ix = 640 + rnd.randint(0, 240)
        iy = 650 + rnd.randint(0, 180)
        fase = (t * 1.5 + i * .21) % 1.0
        isk += (f'<path d="M{ix},{iy-9} l3,9 l9,3 l-9,3 l-3,9 l-3,-9 l-9,-3 l9,-3 Z"'
                f' fill="#ffffff" opacity="{.25+.65*(0.5+0.5*math.cos(2*math.pi*fase)):.2f}"/>')
    s += SL(0, isk)
    # высокая причёска
    s += SL(0, f'<path d="M690,560 q70,-120 140,0 q-20,-70 -70,-74 q-50,4 -70,74 Z"'
               f' fill="#4a3528" {o(4)}/>')
    # дочка в бантах трогает рукав мамы
    s += SL(0, figura(1010, 1020, 300, t, KORALL, TEPLO_SVET, .6, False, False,
                      1.0, 3.0, True, True, "#f3d3b2", True, MOLOKO, True))
    ruk2, _ = rukav(956, 820, 120, -168, t, KORALL, TEPLO_SVET, .4, 5.0)
    s += SL(0, ruk2)
    for sgn in (-1, 1):
        s += SL(0, f'<path d="M{1010+sgn*48},752 q{sgn*40},-30 {sgn*54},6'
                   f' q{-sgn*30},16 {-sgn*54},-6 Z" fill="{MOLOKO}" {o(3)}/>')
    # проигрыватель на серванте
    s += SL(Z_SRED, f'<rect x="1180" y="820" width="300" height="60" rx="10"'
                    f' fill="{DEREVO2}" {o(5)}/>')
    kr = t * 90
    s += SL(Z_SRED, f'<g transform="rotate({kr:.1f} 1320 820)">'
                    f'<circle cx="1320" cy="820" r="76" fill="#1b1b1b" {o(4)}/>'
                    f'<circle cx="1320" cy="820" r="22" fill="{KORALL}" {o(2)}/>'
                    f'<path d="M1320,744 l0,152" stroke="#2d2d2d" stroke-width="3"/></g>')
    s += SL(Z_SRED, f'<path d="M1420,760 l-70,56" stroke="{SEREBRO}" stroke-width="7"'
                    f' stroke-linecap="round"/>')
    s += SL(Z_SRED, lampa_stolika(260, 900, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def krimplenovoe_plate_stoit_samo(t):
    """Кримпленовое платье стоит само, как колокол: дочка обходит его кругом,
    толкает рукавом — платье качается и встаёт обратно."""
    rnd = random.Random(2051)
    s = f'<rect width="{W}" height="{H}" fill="#2b2119"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 45))
    s += SL(Z_DAL, stena("paneli", t, 115))
    s += SL(Z_DAL, kvartira_veschi(1240, 680, 660, t, 13))
    s += SL(Z_SRED, polovicy(1030))
    s += SL(Z_DAL, elka(200, 1040, 400, t, 1.0, True, 47))
    # платье-колокол: цветастое, стоит само
    kach = 9 * A.w(t, 1.5, .1) * A.seg(t, .8, 2.4)
    s += SL(0, f'<g transform="rotate({kach:.2f} 900 1020)">')
    s += SL(0, f'<path d="M790,470 q110,-40 220,0 l130,550 q-240,50 -480,0 Z"'
               f' fill="{TERRAKOT}" {o(7)}/>')
    cv = ""
    for i in range(24):
        cx = 720 + rnd.randint(0, 360)
        cy = 520 + rnd.randint(0, 460)
        c = rnd.choice((MOLOKO, ZOLOTO, IZUMRUD, KORALL))
        for j in range(5):
            a = j * 72
            cv += (f'<ellipse cx="{cx+16*math.cos(math.radians(a)):.0f}"'
                   f' cy="{cy+16*math.sin(math.radians(a)):.0f}" rx="9" ry="13"'
                   f' fill="{c}" opacity=".85"/>')
        cv += f'<circle cx="{cx}" cy="{cy}" r="7" fill="{ZOLOTO}"/>'
    s += SL(0, cv)
    s += SL(0, skladki(700, 600, 400, 420, TERRAKOT, 7, 51, t, 3.0))
    s += SL(0, f'<ellipse cx="900" cy="470" rx="112" ry="34" fill="#20190f" opacity=".55"/>')
    s += SL(0, "</g>")
    # дочка обходит кругом и толкает рукавом
    p = A.seg(t, .2, 2.2)
    dx = 1240 - 320 * p
    s += SL(0, figura(dx, 1030, 310, t, KORALL, TEPLO_SVET, .4, False, p > .5,
                      1.0, 3.0, True, True, "#f3d3b2", True, MOLOKO, True))
    ruk, _ = rukav(dx - 60, 828, 140, -176, t, KORALL, TEPLO_SVET, .3, 6.0)
    s += SL(0, ruk)
    # утюг скучает на доске
    s += SL(Z_SRED, f'<path d="M1420,880 l260,-26 l8,62 l-260,26 Z" fill="{MOLOKO}" {o(6)}/>'
                    f'<path d="M1460,942 l0,96 M1640,926 l0,112" stroke="{SEREBRO}"'
                    f' stroke-width="8"/>')
    s += SL(Z_SRED, f'<path d="M1500,862 q56,-40 110,-6 l6,30 l-120,14 Z"'
                    f' fill="{CHUGUN}" {o(5)}/>')
    s += SL(Z_SRED, par(1560, 846, t, 2, .3, 90, .3, .6))
    s += SL(Z_SRED, f'<path d="M1760,1030 q-26,-190 70,-196 l0,196 Z" fill="#4a3a52" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(120, 160, 1700, t, 10, 53, 60))
    s += SL(0, lampa_stolika(1700, 700, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def lyureks_togda_i_segodnya(t):
    """Два плечика рядом: мамина колючая кофточка и сегодняшнее платье с
    мягкой нитью; между ними идёт стрелка времени."""
    rnd = random.Random(2052)
    s = f'<rect width="{W}" height="{H}" fill="#241f27"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 49))
    s += SL(Z_DAL, stena("paneli", t, 116))
    s += SL(Z_DAL, shkaf(60, 1040, 620, 880, t, .85, True))
    s += SL(Z_DAL, elka(1800, 1040, 380, t, 1.0, True, 55))
    s += SL(Z_SRED, polovicy(1040))
    # слева мамина кофточка: колючий яркий люрекс
    s += SL(0, naryad_plechiki(560, 260, 400, t, "#6a5b73", 1.2, .1, True, None, .0, 56))
    isk = ""
    for i in range(22):
        ix = 430 + rnd.randint(0, 260)
        iy = 320 + rnd.randint(0, 300)
        fase = (t * 1.9 + i * .17) % 1.0
        isk += (f'<path d="M{ix},{iy-11} l4,11 l11,4 l-11,4 l-4,11 l-4,-11 l-11,-4 l11,-4 Z"'
                f' fill="#ffffff" opacity="{.2+.75*(0.5+0.5*math.cos(2*math.pi*fase)):.2f}"/>')
    s += SL(0, isk)
    # справа сегодняшнее платье: мягкая нить
    s += SL(0, naryad_plechiki(1320, 250, 460, t, TSINIY, 1.3, .5, True, None, .22, 57))
    myag = ""
    for i in range(14):
        mx = 1210 + i * 18
        myag += (f'<path d="M{mx},330 q10,150 -6,300" fill="none" stroke="{SEREBRO}"'
                 f' stroke-width="2" opacity="{.18+.22*abs(A.w(t,2.6,i*.2)):.2f}"/>')
    s += SL(0, myag)
    # стрелка времени идёт от кофточки к платью
    p = A.out(A.seg(t, .4, 1.8))
    sx = 720 + 380 * p
    s += SL(0, f'<path d="M700,760 h{20+380*p:.0f}" stroke="{ZOLOTO}" stroke-width="8"'
               f' opacity=".85"/>'
               f'<path d="M{sx:.0f},760 l-30,-20 l0,40 Z" fill="{ZOLOTO}" {o(3)}/>')
    # взрослая дочь держит оба плечика, правое платье прикладывает к щеке
    s += SL(0, figura(980, 1040, 470, t, GRAFIT, HOLOD_KANT, .3, False, False,
                      1.0, 2.0, True, True, "#eec9a6", True, MOLOKO, True))
    for sgn, ug in ((-1, -150), (1, -36)):
        ruk, _ = rukav(980 + sgn * 92, 790, 170, ug, t, GRAFIT, HOLOD_KANT,
                       .2 + (0 if sgn < 0 else .35), 5.0)
        s += SL(0, ruk)
    s += SL(0, f'<circle cx="940" cy="640" r="20" fill="none" stroke="{SEREBRO}"'
               f' stroke-width="5"/><circle cx="1000" cy="640" r="20" fill="none"'
               f' stroke="{SEREBRO}" stroke-width="5"/>'
               f'<path d="M960,640 h20" stroke="{SEREBRO}" stroke-width="4"/>')
    # коробка с фотографиями и пуфик
    s += SL(Z_SRED, korobka(1560, 1040, 300, t, 120, True, BEZH, MOLOKO))
    fot = ""
    for i in range(5):
        fot += (f'<g transform="rotate({-12+i*7} {1620+i*30} 930)">'
                f'<rect x="{1600+i*30}" y="900" width="86" height="64" rx="4"'
                f' fill="{MOLOKO}" {o(3)}/>'
                f'<rect x="{1608+i*30}" y="908" width="70" height="40" fill="#9aa6b0"/></g>')
    s += SL(Z_SRED, fot)
    s += SL(Z_SRED, f'<path d="M760,1040 q-26,-150 62,-156 l0,156 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(60, 150, 1800, t, 11, 59, 60))
    s += SL(0, lampa_stolika(1700, 820, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def hozyayka_stavit_salatnik(t):
    """Кухня-столовая: хозяйка в винном трикотажном платье ставит салатник.
    В окне-раздаче — настоящая сервировка праздничного стола."""
    rnd = random.Random(2054)
    s = f'<rect width="{W}" height="{H}" fill="#241c18"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 57))
    s += SL(Z_DAL, stena("kraska", t, 117))
    # окно-раздача: рисованный вид, метка, наличник поверх
    px, py, pw, ph = 980, 150, 780, 300
    put = kontur_proema(px, py, pw, ph, "pryam")
    vid = (f'<path d="{put}" fill="#2e2620"/>'
           + f'<rect x="{px+30}" y="{py+150}" width="{pw-60}" height="40" rx="8"'
             f' fill="{MOLOKO}" {o(3)}/>')
    s += SL(Z_DAL, vid + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-16}" y="{py-16}" width="{pw+32}" height="{ph+32}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="26"/>'
            + f'<path d="M{px-16},{py+ph+16} h{pw+32}" stroke="{DEREVO}"'
              f' stroke-width="18"/>')
    s += SL(Z_SRED, polovicy(1040))
    # праздничный стол наполовину накрыт
    s += SL(Z_SRED, stol(120, 940, 1180, 44))
    sk = (f'<path d="M110,900 h1200 l-20,120 q-580,34 -1160,0 Z" fill="{MOLOKO}" {o(5)}/>')
    s += SL(Z_SRED, sk)
    tar = ""
    for i in range(6):
        tx = 220 + i * 180
        tar += (f'<ellipse cx="{tx}" cy="896" rx="62" ry="20" fill="{KREM2}" {o(3)}/>'
                f'<ellipse cx="{tx}" cy="890" rx="44" ry="13" fill="{MOLOKO}" {o(2)}/>')
    s += SL(Z_SRED, tar)
    s += SL(Z_SRED, svecha(400, 892, t, .1, 1.3) + svecha(1120, 892, t, .5, 1.2))
    # хозяйка ставит салатник: обе руки внешние, несут салатник
    s += SL(0, figura(760, 1040, 470, t, VINO, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    stav = A.out(A.seg(t, .3, 1.5))
    sx, sy = 760, 700 + 150 * stav
    for sgn in (-1, 1):
        ruk, _ = rukav(760 + sgn * 90, 790, 130, -60 + 40 * stav - sgn * 12, t,
                       VINO, TEPLO_SVET, .2 + (0 if sgn < 0 else .25), 4.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M{sx-96:.0f},{sy:.0f} q96,76 192,0 q-16,56 -96,60'
               f' q-80,-4 -96,-60 Z" fill="{IZUMRUD}" {o(5)}/>')
    s += SL(0, f'<ellipse cx="{sx:.0f}" cy="{sy:.0f}" rx="96" ry="22" fill="{KREM2}" {o(3)}/>')
    # кухонная часть: духовка, хлебница, стопка тарелок, полотенце
    s += SL(Z_SRED, f'<rect x="1420" y="700" width="420" height="340" rx="12"'
                    f' fill="{CHUGUN}" {o(6)}/>'
                    f'<rect x="1452" y="740" width="356" height="170" rx="8"'
                    f' fill="#20262c" {o(4)}/>')
    s += SL(Z_SRED, teplo(1630, 830, 190, 130, .34 + .10 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, f'<path d="M1452,950 h356" stroke="{SEREBRO}" stroke-width="10"/>')
    kach = 5 * A.w(t, 2.2, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.2f} 1400 700)">'
                    f'<path d="M1360,700 h80 l-10,170 h-60 Z" fill="{KORALL}" {o(4)}/></g>')
    st = "".join(f'<ellipse cx="1300" cy="{880-i*16}" rx="56" ry="16" fill="{KREM2}"'
                 f' {o(2)}/>' for i in range(6))
    s += SL(Z_SRED, st)
    s += SL(Z_DAL, elka(90, 1040, 420, t, 1.0, True, 59))
    s += SL(Z_SRED, girlyanda(140, 170, 760, t, 9, 61, 54))
    s += SL(0, lampa_stolika(1180, 560, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def naryad_pervyy_na_manekene(t):
    """Манекен в трикотажном платье: стрелки-выноски показывают длину, рукав и
    горловину, оттенок переключается с винного на терракотовый."""
    rnd = random.Random(2055)
    s = f'<rect width="{W}" height="{H}" fill="#241d22"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 61))
    s += SL(Z_DAL, stena("kraska", t, 118))
    s += SL(Z_DAL, okno_izby(120, 140, 460, 420, t, svet=False, moroz=.32))
    s += SL(Z_DAL, sneg_letit(t, 22, 63, .5, .7))
    s += SL(Z_DAL, elka(1820, 1040, 400, t, 1.0, True, 65))
    s += SL(Z_SRED, polovicy(1040))
    perekl = (t % 3.2) < 1.6
    s += SL(0, manekken(880, 1010, 760, t, KREM2, "zh",
                        VINO if perekl else TERRAKOT, .2, MOLOKO, .05, 80))
    # три стрелки-выноски встают по очереди
    VYN = ((640, 900, "длина ниже колена"), (1110, 640, "длинный рукав"),
           (880, 380, "круглая горловина"))
    for i, (vx, vy, _) in enumerate(VYN):
        p = A.out(A.seg(t, .4 + i * .55, .6))
        if p <= 0.02:
            continue
        ex = vx + (240 if vx > 900 else -240) * p
        s += SL(0, f'<path d="M{vx},{vy} L{ex:.0f},{vy-70*p:.0f}" stroke="{ZOLOTO}"'
                   f' stroke-width="6" opacity="{p:.2f}"/>'
                   f'<circle cx="{vx}" cy="{vy}" r="12" fill="{ZOLOTO}" opacity="{p:.2f}"/>'
                   f'<rect x="{min(vx,ex)-10:.0f}" y="{vy-110*p:.0f}" width="210"'
                   f' height="54" rx="10" fill="{GRAFIT}" opacity="{p*.9:.2f}" {o(3)}/>')
    # сантиметр свисает со стула
    s += SL(Z_SRED, f'<rect x="300" y="880" width="180" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="310" y="906" width="18" height="134" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="452" y="906" width="18" height="134" fill="{DEREVO}" {o(4)}/>')
    sv = 10 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<path d="M380,880 q{20+sv:.0f},120 {-14+sv:.0f},230"'
                    f' fill="none" stroke="{MOLOKO}" stroke-width="12"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{374+i*2},{900+i*25} l14,0" stroke="{K}"'
                        f' stroke-width="2" opacity=".6"/>')
    # столик с серьгами
    s += SL(Z_SRED, trumo(1420, 1040, 420, 300, t))
    s += SL(Z_SRED, f'<ellipse cx="1620" cy="760" rx="64" ry="40" fill="{VINO}" {o(4)}/>')
    for sgn in (-1, 1):
        s += SL(Z_SRED, f'<circle cx="{1620+sgn*24}" cy="{724-5*abs(A.w(t,1.8,sgn*.3)):.0f}"'
                        f' r="14" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(Z_SRED, zerkalo(1380, 300, 260, 460, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1392" y="312" width="236" height="436" fill="{STEKLO}"'
                    f' opacity=".28"/>')
    s += SL(Z_SRED, girlyanda(60, 150, 1800, t, 12, 67, 58))
    s += SL(0, lampa_stolika(1620, 700, t, 1.15))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def naklon_k_duhovke(t):
    """Хозяйка наклоняется к духовке и вынимает противень: платье не задралось,
    ворот на месте — над ними встают две зелёные галочки."""
    rnd = random.Random(2056)
    s = f'<rect width="{W}" height="{H}" fill="#241c18"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 69))
    s += SL(Z_DAL, stena("kraska", t, 119))
    s += SL(Z_DAL, _polka_melochey(120, 300, 420, t, 56, 6))
    s += SL(Z_SRED, polovicy(1040))
    # плита с духовкой
    s += SL(Z_SRED, f'<rect x="1120" y="620" width="700" height="420" rx="14"'
                    f' fill="{CHUGUN}" {o(7)}/>'
                    f'<rect x="1160" y="680" width="620" height="230" rx="10"'
                    f' fill="#1d2228" {o(5)}/>')
    s += SL(Z_SRED, teplo(1470, 800, 300, 180, .38 + .10 * abs(A.w(t, 1.5))))
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{1200+i*180}" cy="640" r="34" fill="#2b3238" {o(3)}/>')
    # противень выезжает
    vyez = A.out(A.seg(t, .35, 1.3))
    px = 1160 - 320 * vyez
    s += SL(0, f'<rect x="{px:.0f}" y="810" width="420" height="40" rx="8"'
               f' fill="{ZHELEZ}" {o(5)}/>')
    for i in range(8):
        s += SL(0, f'<ellipse cx="{px+50+i*46:.0f}" cy="808" rx="24" ry="16"'
                   f' fill="{MED}" {o(3)}/>')
    s += SL(0, par(px + 210, 780, t, 4, .55, 170, .5, 1.0))
    # хозяйка: колени согнуты, обе руки в прихватках
    s += SL(0, figura(700, 1040, 500, t, VINO, TEPLO_SVET, .2, False, True, 1.0,
                      4.0, True, True, "#f0cfae", True, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(700 + sgn * 78, 790, 190, -8 + sgn * 14, t, VINO,
                              TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
        s += SL(0, f'<rect x="{hx-28:.0f}" y="{hy-24:.0f}" width="56" height="48"'
                   f' rx="12" fill="{KORALL}" {o(3)}/>')
    # две галочки
    for i, (gx, gy) in enumerate(((560, 560), (860, 500))):
        p = A.out(A.seg(t, .9 + i * .3, .5))
        if p <= .02:
            continue
        s += SL(0, f'<path d="M{gx},{gy} l34,40 l64,-86" fill="none" stroke="#3fae62"'
                   f' stroke-width="16" stroke-linecap="round" opacity="{p:.2f}"/>')
    # чайник, полотенце, стол с мукой, кот, часы
    s += SL(Z_SRED, f'<path d="M1880,620 q-40,-70 -110,-70 q-70,0 -110,70 Z"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    s += SL(Z_SRED, stol(120, 980, 420, 36))
    s += SL(Z_SRED, f'<ellipse cx="300" cy="944" rx="120" ry="30" fill="{MOLOKO}"'
                    f' opacity=".85"/>')
    s += SL(Z_SRED, kot(430, 1040, t, 1.5, "#6b5a46"))
    s += SL(Z_SRED, hodiki(960, 240, t, 1.3))
    s += SL(Z_SRED, girlyanda(100, 160, 820, t, 8, 71, 52))
    s += SL(0, lampa_stolika(960, 520, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def sergi_na_barhatnoy_podushechke(t):
    """Туалетный столик: пара серёг на бархатной подушечке, рукав закрывает
    крышку коробки с остальными украшениями — надето только одно."""
    rnd = random.Random(2058)
    s = f'<rect width="{W}" height="{H}" fill="#241f28"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 73))
    s += SL(Z_DAL, stena("doski", t, 120))
    s += SL(Z_DAL, elka(1840, 1050, 340, t, 1.0, True, 75))
    s += SL(Z_SRED, trumo(260, 1040, 1300, 460, t))
    # В ЗЕРКАЛЕ ДОЛЖНО ЧТО-ТО ОТРАЖАТЬСЯ (осмотр 16.11): пустая золотая рама
    # на пол-кадра читается как дыра. Ставим отражение наряда и флаконов.
    s += SL(Z_SRED, f'<rect x="634" y="184" width="592" height="492" fill="{STEKLO}"'
                    f' opacity=".26"/>')
    s += SL(Z_SRED, f'<g opacity=".5">'
                    + naryad_plechiki(930, 230, 380, t, VINO, 1.0, .3, True, None, .0, 85)
                    + f'<ellipse cx="760" cy="640" rx="90" ry="26" fill="{KREM2}"/>'
                    + f'<ellipse cx="1120" cy="640" rx="70" ry="22" fill="{LAVANDA}"/></g>')
    s += SL(Z_SRED, zerkalo(620, 170, 620, 520, t, "pryam", ZOLOTO, True))
    # подушечка с серьгами, крупно
    s += SL(0, f'<path d="M480,900 q280,-110 560,0 q-62,150 -280,156 q-218,-6 -280,-156 Z"'
               f' fill="{VINO}" {o(7)}/>')
    s += SL(0, skladki(520, 850, 480, 150, VINO, 6, 81, t, 2.0))
    for sgn in (-1, 1):
        kach = 5 * A.w(t, 1.7, .2 if sgn < 0 else .6)
        sx = 760 + sgn * 150
        s += SL(0, f'<g transform="rotate({kach:.2f} {sx} 820)">'
                   f'<path d="M{sx},820 l0,-92" stroke="{ZOLOTO}" stroke-width="11"/>'
                   f'<circle cx="{sx}" cy="722" r="34" fill="none" stroke="{ZOLOTO}"'
                   f' stroke-width="11"/>'
                   f'<path d="M{sx-44},832 l44,130 l44,-130 Z" fill="{ZOLOTO}" {o(4)}/>'
                   f'<circle cx="{sx}" cy="902" r="20" fill="{KREM2}" {o(3)}/></g>')
    # коробка с бусами, брошами, браслетами; крышка закрывается рукавом
    zak = A.out(A.seg(t, .5, 1.4))
    kx, ky, kw = 1180, 980, 460
    s += SL(0, f'<rect x="{kx}" y="{ky-130}" width="{kw}" height="130" rx="12"'
               f' fill="{DEREVO2}" {o(6)}/>')
    vn = ""
    for i in range(14):
        bx = kx + 30 + rnd.randint(0, kw - 70)
        by = ky - 110 + rnd.randint(0, 60)
        c = rnd.choice((ZOLOTO, SEREBRO, KORALL, IZUMRUD, MOLOKO))
        vn += f'<circle cx="{bx}" cy="{by}" r="{rnd.randint(8, 15)}" fill="{c}" {o(2)}/>'
    s += SL(0, vn)
    s += SL(0, f'<g transform="rotate({-70+70*zak:.1f} {kx} {ky-130})">'
               f'<rect x="{kx}" y="{ky-170}" width="{kw}" height="40" rx="8"'
               f' fill="{DEREVO}" {o(4)}/></g>')
    ruk, _ = rukav(kx + kw + 120, ky - 330, 230, 130 - 40 * zak, t, MOLOKO,
                   TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    # флаконы, гребень, свеча, ёлочная ветка
    fl = ""
    for i in range(5):
        fx = 320 + i * 86
        h_ = 52 + (i % 3) * 24
        fl += (f'<rect x="{fx-19}" y="{940-h_}" width="38" height="{h_}" rx="7"'
               f' fill="{(LAVANDA, PUDRA, KORALL, MOLOKO, ZOLOTO)[i]}" {o(3)}/>'
               f'<rect x="{fx-8}" y="{928-h_}" width="16" height="14" rx="4"'
               f' fill="{SEREBRO}" {o(2)}/>')
    s += SL(Z_SRED, fl)
    s += SL(Z_SRED, f'<path d="M980,960 h150 l0,22 h-150 Z" fill="{DEREVO2}" {o(3)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{988+i*12},982 l0,26" stroke="{DEREVO2}"'
                            f' stroke-width="3"/>' for i in range(12)))
    s += SL(Z_SRED, svecha(1700, 940, t, .3, 1.4))
    s += SL(Z_SRED, girlyanda(80, 150, 1780, t, 11, 83, 56))
    s += SL(0, lampa_stolika(1060, 880, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def hozyayka_ves_vecher(t):
    """Три картинки одного вечера — восемь, десять и полночь: платье везде без
    единой складки, хозяйка успевает всё."""
    rnd = random.Random(2059)
    s = f'<rect width="{W}" height="{H}" fill="#221b20"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 77))
    s += SL(Z_DAL, stena("oboi", t, 121))
    s += SL(Z_DAL, elka(1850, 1060, 320, t, 1.0, True, 79))
    CHASY = (8, 10, 12)
    for i in range(3):
        x0 = 60 + i * 620
        s += SL(Z_DAL, f'<rect x="{x0}" y="300" width="560" height="640" rx="18"'
                       f' fill="#2c242b" {o(6)}/>')
        s += SL(Z_DAL, f'<rect x="{x0+16}" y="316" width="528" height="608" rx="14"'
                       f' fill="#3a2f36" opacity=".55"/>')
        # часы над картинкой
        cx, cy = x0 + 280, 240
        s += SL(Z_SRED, f'<circle cx="{cx}" cy="{cy}" r="66" fill="{MOLOKO}" {o(5)}/>')
        for j in range(12):
            a = j * 30
            s += SL(Z_SRED, f'<path d="M{cx+52*math.cos(math.radians(a)):.0f},'
                            f'{cy+52*math.sin(math.radians(a)):.0f} l'
                            f'{8*math.cos(math.radians(a)):.0f},'
                            f'{8*math.sin(math.radians(a)):.0f}" stroke="{K}"'
                            f' stroke-width="4"/>')
        hod = CHASY[i] * 30 - 90 + 10 * A.seg(t, .3, 3.0)
        s += SL(Z_SRED, f'<path d="M{cx},{cy} l{44*math.cos(math.radians(hod)):.0f},'
                        f'{44*math.sin(math.radians(hod)):.0f}" stroke="{K}"'
                        f' stroke-width="7" stroke-linecap="round"/>'
                        f'<path d="M{cx},{cy} l0,-30" stroke="{K}" stroke-width="9"'
                        f' stroke-linecap="round"/>')
    # первая: идёт от плиты с блюдом в обеих руках
    idet = A.out(A.seg(t, .3, 1.8))
    fx = 180 + 160 * idet
    s += SL(0, figura(fx, 900, 380, t, VINO, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(fx + sgn * 68, 690, 110, -26 - sgn * 10, t, VINO,
                              TEPLO_SVET, .2, 4.0)
        s += SL(0, ruk)
    s += SL(0, f'<ellipse cx="{fx:.0f}" cy="620" rx="96" ry="26" fill="{KREM2}" {o(4)}/>'
               f'<ellipse cx="{fx:.0f}" cy="608" rx="70" ry="18" fill="{MED}" {o(2)}/>')
    s += SL(0, par(fx, 592, t, 3, .4, 110, .4, .8))
    # вторая: разливает компот
    s += SL(0, figura(960, 900, 380, t, VINO, TEPLO_SVET, .5, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, (hx, hy) = rukav(1026, 690, 130, -40, t, VINO, TEPLO_SVET, .3, 4.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(894, 710, 110, -8, t, VINO, TEPLO_SVET, .6, 4.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M{hx-30:.0f},{hy-40:.0f} q36,-54 72,0 l10,86 h-92 Z"'
               f' fill="url(#glina)" {o(4)}/>')
    liv = A.seg(t, .6, 1.6)
    s += SL(0, f'<path d="M{hx+34:.0f},{hy+40:.0f} l-10,{90*liv:.0f}" stroke="{KORALL}"'
               f' stroke-width="9" opacity=".85"/>')
    s += SL(0, f'<path d="M870,860 h180 l-14,70 h-152 Z" fill="{MOLOKO}" {o(3)}/>')
    # третья: сидит с бокалом среди гостей-силуэтов, фотограф щёлкает
    s += SL(0, figura(1560, 900, 360, t, VINO, TEPLO_SVET, .8, False, False, 1.0,
                      1.5, True, True, "#f0cfae", True, MOLOKO, False))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(1560 + sgn * 62, 700, 96, -62 - sgn * 8, t, VINO,
                              TEPLO_SVET, .4, 4.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M1540,600 q20,54 40,0 Z" fill="{STEKLO}" opacity=".75"/>'
               f'<path d="M1560,600 l0,40 M1540,644 h40" stroke="{STEKLO}"'
               f' stroke-width="5"/>')
    go = ""
    for i in range(3):
        gx = 1400 + i * 120
        go += (f'<ellipse cx="{gx}" cy="800" rx="46" ry="90" fill="#1b1620"'
               f' opacity=".85"/><circle cx="{gx}" cy="690" r="34" fill="#1b1620"'
               f' opacity=".85"/>')
    s += SL(Z_SRED, go)
    vsp = 1.0 if (t % 2.2) < .18 else .0
    s += SL(0, f'<rect x="1300" y="320" width="560" height="620" fill="#ffffff"'
               f' opacity="{vsp*.35:.2f}"/>')
    s += SL(Z_SRED, svecha(1260, 930, t, .2, 1.2) + svecha(640, 930, t, .6, 1.2))
    s += SL(Z_SRED, girlyanda(60, 160, 1800, t, 12, 85, 54))
    s += SL(0, lampa_stolika(1180, 1000, t, 1.0))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def seroe_plate_i_vinnyy_sharf(t):
    """Простое серое платье на плечиках: винный поясок и винный шарф делают
    его праздничным прямо в кадре."""
    rnd = random.Random(2060)
    s = f'<rect width="{W}" height="{H}" fill="#242027"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 81))
    s += SL(Z_DAL, stena("kraska", t, 122))
    s += SL(Z_DAL, shkaf(900, 1050, 900, 940, t, .9, True))
    s += SL(Z_DAL, elka(120, 1050, 380, t, 1.0, True, 83))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, naryad_plechiki(1240, 250, 620, t, "#9b9ca4", 1.5, .1, True, None, .04, 86, 1.4))
    # поясок завязывается
    p1 = A.out(A.seg(t, .35, 1.2))
    s += SL(0, f'<path d="M{1240-190*p1:.0f},600 q{190*p1:.0f},36 {380*p1:.0f},0"'
               f' fill="none" stroke="{VINO}" stroke-width="26"/>')
    if p1 > .8:
        s += SL(0, f'<path d="M1240,600 l-54,-34 l10,70 Z" fill="{VINO}" {o(3)}/>'
                   f'<path d="M1240,600 l54,-34 l-10,70 Z" fill="{VINO}" {o(3)}/>')
    # шарф ложится на плечо
    p2 = A.out(A.seg(t, 1.1, 1.3))
    s += SL(0, f'<path d="M{1090:.0f},{300-160*(1-p2):.0f} q60,120 20,300'
               f' l70,16 q50,-200 -10,-320 Z" fill="{VINO}" opacity="{p2:.2f}" {o(5)}/>')
    # женщина завязывает поясок и накидывает шарф
    s += SL(0, figura(700, 1050, 520, t, GRAFIT, HOLOD_KANT, .3, False, False, 1.0,
                      2.0, True, True, "#eec9a6", True, MOLOKO, True))
    ruk, _ = rukav(790, 760, 230, -20 + 10 * A.w(t, 1.6), t, GRAFIT, HOLOD_KANT, .2, 5.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(790, 690, 250, -44 + 12 * A.w(t, 1.9, .3), t, GRAFIT, HOLOD_KANT, .5, 5.0)
    s += SL(0, ruk2)
    # корзина с шарфами, туфли, пуфик, зеркало
    s += SL(Z_SRED, f'<path d="M300,1046 q-30,-150 70,-154 q100,4 70,154 Z"'
                    f' fill="url(#solom)" {o(5)}/>')
    sh = ""
    for i in range(5):
        c = (KORALL, IZUMRUD, TSINIY, ZOLOTO, LAVANDA)[i]
        sh += (f'<path d="M{320+i*26},900 q{14+6*A.w(t,2.4,i*.3):.0f},-70 30,-96"'
               f' fill="none" stroke="{c}" stroke-width="18" stroke-linecap="round"/>')
    s += SL(Z_SRED, sh)
    s += SL(Z_SRED, tufli(520, 1046, 1.1, GRAFIT, t))
    s += SL(Z_SRED, f'<path d="M160,1046 q-20,-130 56,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(60, 280, 220, 560, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(260, 150, 1560, t, 10, 87, 52))
    s += SL(0, lampa_stolika(1760, 960, t, 1.15))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def fartuk_poverh_naryadnogo(t):
    """Кухня шестидесятых: мама развязывает тесёмки ситцевого фартука, он
    слетает на спинку стула. В стекле окна — настоящий зимний двор."""
    rnd = random.Random(2061)
    s = f'<rect width="{W}" height="{H}" fill="#241d16"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 89))
    s += SL(Z_DAL, stena("kraska", t, 123))
    # окно кухни: рисованный вид, метка, переплёт поверх
    px, py, pw, ph = 120, 170, 800, 330
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#15202c"/>'
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-14}" y="{py-14}" width="{pw+28}" height="{ph+28}"'
              f' fill="none" stroke="{MOLOKO}" stroke-width="22"/>'
            + f'<path d="M{px+pw/2:.0f},{py-14} l0,{ph+28}" stroke="{MOLOKO}"'
              f' stroke-width="16"/>'
            + f'<path d="M{px-14},{py+ph/2:.0f} l{pw+28},0" stroke="{MOLOKO}"'
              f' stroke-width="12"/>')
    s += SL(Z_SRED, polovicy(1050))
    # плита, кастрюли, противень с пирожками
    s += SL(Z_SRED, f'<rect x="1180" y="640" width="660" height="410" rx="12"'
                    f' fill="{CHUGUN}" {o(7)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{1270+i*160}" cy="662" r="36" fill="#2b3238" {o(3)}/>')
    for i, (kx, kw) in enumerate(((1280, 180), (1530, 150))):
        s += SL(Z_SRED, f'<path d="M{kx},600 h{kw} l-14,-90 h{-kw+28} Z"'
                        f' fill="{SEREBRO}" {o(5)}/>')
        s += SL(Z_SRED, par(kx + kw / 2, 500, t, 4, .5, 160, .45, 1.0))
    s += SL(Z_SRED, f'<rect x="1230" y="760" width="420" height="34" rx="6"'
                    f' fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<ellipse cx="{1270+i*58}" cy="756" rx="26" ry="17"'
                            f' fill="{MED}" {o(3)}/>' for i in range(7)))
    # мама: обе руки заведены за спину, развязывают тесёмки
    s += SL(0, figura(760, 1050, 520, t, IZUMRUD, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    raz = A.seg(t, .3, 1.8)
    for sgn in (-1, 1):
        ruk, _ = rukav(760 + sgn * 92, 760, 140, 150 - sgn * 24 + 20 * raz, t,
                       IZUMRUD, TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    # фартук слетает на спинку стула
    let = A.out(A.seg(t, 1.0, 1.4))
    fx = 760 + 420 * let
    fy = 820 + 120 * let
    s += SL(0, f'<g transform="rotate({40*let:.1f} {fx:.0f} {fy:.0f})">'
               f'<path d="M{fx-110:.0f},{fy-230:.0f} h220 l34,300 q-134,30 -268,0 Z"'
               f' fill="{MOLOKO}" {o(5)}/>')
    cvet = ""
    for i in range(14):
        cx = fx - 96 + rnd.randint(0, 190)
        cy = fy - 210 + rnd.randint(0, 260)
        cvet += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="{KORALL}"'
                 f' opacity=".9"/>')
    s += SL(0, cvet + "</g>")
    s += SL(Z_SRED, f'<rect x="1080" y="860" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="1090" y="886" width="18" height="164" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1222" y="886" width="18" height="164" fill="{DEREVO}" {o(4)}/>')
    # радио, скалка, полотенце, часы без пяти двенадцать
    s += SL(Z_SRED, f'<rect x="300" y="620" width="230" height="130" rx="10"'
                    f' fill="{DEREVO2}" {o(5)}/>'
                    f'<circle cx="360" cy="686" r="34" fill="#2b2b2b" {o(3)}/>'
                    f'<circle cx="470" cy="686" r="18" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="620" y="716" width="200" height="22" rx="11"'
                    f' fill="{DEREVO2}" {o(3)}/>')
    s += SL(Z_SRED, hodiki(1000, 230, t, 1.4))
    s += SL(Z_SRED, girlyanda(980, 150, 880, t, 9, 91, 50))
    s += SL(0, lampa_stolika(520, 560, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def fartuk_na_kryuchke(t):
    """Сегодняшняя кухня: фартук с пятном висит на крючке, хозяйка в чистом
    винном платье гасит свет и уходит к гостям."""
    rnd = random.Random(2062)
    s = f'<rect width="{W}" height="{H}" fill="#1f1b20"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 93))
    s += SL(Z_DAL, stena("kraska", t, 124))
    s += SL(Z_SRED, polovicy(1050))
    # фартук на крючке, крупно
    kach = 4.5 * A.w(t, 2.0, .1)
    s += SL(0, f'<g transform="rotate({kach:.2f} 620 300)">'
               f'<path d="M620,300 l0,46" stroke="{SEREBRO}" stroke-width="8"/>'
               f'<path d="M500,346 h240 l40,420 q-160,34 -320,0 Z" fill="{KREM2}" {o(6)}/>'
               f'<path d="M500,420 h240" stroke="{K}" stroke-width="4" opacity=".35"/>'
               f'<ellipse cx="660" cy="620" rx="52" ry="38" fill="{VINO}" opacity=".8"/>'
               f'<ellipse cx="688" cy="652" rx="22" ry="16" fill="{VINO}" opacity=".7"/></g>')
    s += SL(Z_SRED, f'<path d="M560,290 h120 l0,16 h-120 Z" fill="{SEREBRO}" {o(3)}/>')
    # хозяйка в дверях: правая рука к серьге, левая на выключателе
    s += SL(0, figura(1280, 1050, 520, t, VINO, TEPLO_SVET, .3, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, (hx, hy) = rukav(1216, 760, 150, -104, t, VINO, TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(1352, 770, 170, -22, t, VINO, TEPLO_SVET, .5, 5.0)
    s += SL(0, ruk2)
    s += SL(0, f'<circle cx="{hx:.0f}" cy="{hy+10:.0f}" r="13" fill="{ZOLOTO}" {o(2)}/>')
    gasnet = A.seg(t, .6, 1.6)
    s += SL(Z_SRED, f'<rect x="{h2x-22:.0f}" y="{h2y-30:.0f}" width="44" height="60"'
                    f' rx="8" fill="{MOLOKO}" {o(3)}/>')
    # кухня гаснет, столовая со свечами светится
    s += SL(Z_SRED, f'<rect x="0" y="0" width="1120" height="1080" fill="#000000"'
                    f' opacity="{.45*gasnet:.2f}"/>')
    s += SL(Z_DAL, f'<rect x="1480" y="200" width="420" height="850" rx="12"'
                   f' fill="#2d2129" {o(6)}/>')
    s += SL(Z_DAL, svecha(1580, 700, t, .1, 1.5) + svecha(1700, 690, t, .5, 1.4)
            + svecha(1810, 706, t, .8, 1.3))
    s += SL(Z_DAL, teplo(1690, 680, 300, 320, .34 + .10 * abs(A.w(t, 1.7))))
    # плита, полотенце, венок, часы
    s += SL(Z_SRED, f'<rect x="120" y="700" width="420" height="350" rx="12"'
                    f' fill="{CHUGUN}" {o(6)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{190+i*110}" cy="722" r="30" fill="#2b3238" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M880,640 h120 l0,230 h-120 Z" fill="{KORALL}" {o(4)}/>')
    ven = ""
    for i in range(16):
        a = i * 22.5
        ven += (f'<ellipse cx="{980+96*math.cos(math.radians(a)):.0f}"'
                f' cy="{330+96*math.sin(math.radians(a)):.0f}" rx="22" ry="13"'
                f' fill="{HVOYA}" transform="rotate({a:.0f} '
                f'{980+96*math.cos(math.radians(a)):.0f},'
                f'{330+96*math.sin(math.radians(a)):.0f})" {o(2)}/>')
    s += SL(Z_SRED, ven)
    s += SL(Z_SRED, hodiki(300, 300, t, 1.2))
    s += SL(0, lampa_stolika(880, 980, t, 1.0))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def taksi_u_podezda_vecherom(t):
    """Зимний вечер у подъезда в огоньках: женщина в шубке спускается с
    крыльца к машине с шашечками, в руке блестящая сумочка."""
    rnd = random.Random(2063)
    s = f'<rect width="{W}" height="{H}" fill="#101722"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 97))
    s += SL(Z_DAL, panelka(60, 760, 760, t, 5, True, 99))
    s += SL(Z_DAL, ulica_dal(900, 700, 1000, t, True, 101))
    s += SL(Z_DAL, sneg_letit(t, 44, 103, .75, 1.0))
    s += SL(Z_SRED, f'<rect x="0" y="880" width="{W}" height="200" fill="{SNEG}"'
                    f' opacity=".82"/>')
    # подъезд в огоньках и крыльцо
    s += SL(Z_SRED, f'<rect x="240" y="420" width="420" height="520" rx="10"'
                    f' fill="#2a2f3a" {o(6)}/>'
                    f'<rect x="300" y="520" width="300" height="420" rx="8"'
                    f' fill="#16202c" {o(4)}/>')
    s += SL(Z_SRED, girlyanda(250, 440, 400, t, 9, 105, 44))
    stup = "".join(f'<rect x="{250+i*18}" y="{900+i*26}" width="{380-i*36}"'
                   f' height="26" fill="{SNEG}" {o(3)}/>' for i in range(3))
    s += SL(Z_SRED, stup)
    # машина-силуэт с шашечками
    s += SL(Z_SRED, f'<path d="M1120,900 q40,-120 200,-130 l240,0 q150,20 190,130 Z"'
                    f' fill="#1d222c" {o(6)}/>'
                    f'<path d="M1240,790 q120,-70 260,0 Z" fill="{STEKLO}" opacity=".45"/>')
    sh = "".join(f'<rect x="{1180+i*40}" y="856" width="40" height="22"'
                 f' fill="{"#e9eef6" if i % 2 == 0 else "#20242c"}"/>' for i in range(10))
    s += SL(Z_SRED, sh)
    for cx in (1180, 1620):
        s += SL(Z_SRED, f'<circle cx="{cx}" cy="930" r="46" fill="#15181e" {o(4)}/>'
                        f'<circle cx="{cx}" cy="930" r="18" fill="{SEREBRO}" {o(2)}/>')
    s += SL(Z_SRED, teplo(1700, 880, 160, 90, .30 + .10 * abs(A.w(t, 1.4))))
    # женщина спускается: левая рука придерживает подол, правая с сумочкой
    p = A.out(A.seg(t, .25, 1.6))
    fx, fy = 620 + 260 * p, 900 + 60 * p
    s += SL(0, figura(fx, fy, 470, t, "#6b5347", HOLOD_KANT, .2, False, False, 1.0,
                      3.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, (hx, hy) = rukav(fx - 76, fy - 300, 150, 62, t, "#6b5347", HOLOD_KANT, .2, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(fx + 76, fy - 300, 140, 50, t, "#6b5347", HOLOD_KANT, .5, 5.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M{h2x-34:.0f},{h2y:.0f} q34,-14 58,14 l10,70 h-82 Z"'
               f' fill="{SEREBRO}" opacity="{.75+.25*abs(A.w(t,1.9)):.2f}" {o(3)}/>')
    s += SL(0, f'<ellipse cx="{fx:.0f}" cy="{fy-420:.0f}" rx="66" ry="30"'
               f' fill="#8a7466" {o(4)}/>')
    s += SL(0, para_izo_rta(fx + 30, fy - 400, t, .2, 1.0, .45))
    # фонарь, ёлка у подъезда, скамейка
    s += SL(Z_SRED, f'<rect x="940" y="420" width="16" height="500" fill="{CHUGUN}" {o(4)}/>'
                    f'<path d="M900,420 q48,-56 96,0 Z" fill="{ZOLOTO}" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, teplo(948, 440, 260, 230, .30 + .08 * abs(A.w(t, 2.1))))
    s += SL(Z_DAL, elka(780, 920, 360, t, 1.0, True, 107))
    s += SL(Z_SRED, f'<rect x="1000" y="880" width="180" height="16" rx="6"'
                    f' fill="{DEREVO}" {o(3)}/>'
                    f'<rect x="1010" y="896" width="14" height="60" fill="{CHUGUN}" {o(2)}/>'
                    f'<rect x="1156" y="896" width="14" height="60" fill="{CHUGUN}" {o(2)}/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def naryad_vtoroy_na_manekene(t):
    """Манекен в бархатном платье: стрелки-выноски показывают силуэт, подол и
    рукав три четверти, оттенок переключается с рубинового на изумрудный."""
    rnd = random.Random(2064)
    s = f'<rect width="{W}" height="{H}" fill="#201d26"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 109))
    s += SL(Z_DAL, stena("kraska", t, 126))
    s += SL(Z_DAL, elka(140, 1050, 440, t, 1.0, True, 111))
    s += SL(Z_SRED, polovicy(1050))
    perekl = (t % 3.6) < 1.8
    s += SL(0, manekken(960, 1020, 780, t, KREM2, "zh",
                        RUBIN if perekl else IZUMRUD, .2, None, .14, 112))
    tem = ""
    for i in range(9):
        tx = 820 + i * 36
        tem += (f'<path d="M{tx},560 q{10+6*A.w(t,2.4,i*.2):.0f},180 -4,340"'
                f' fill="none" stroke="#000000" stroke-width="16" opacity=".22"/>')
    s += SL(0, tem)
    VYN = ((780, 640, 1), (1180, 880, -1), (1140, 560, -1))
    for i, (vx, vy, sgn) in enumerate(VYN):
        p = A.out(A.seg(t, .4 + i * .6, .6))
        if p <= .02:
            continue
        ex = vx - sgn * 230 * p
        s += SL(0, f'<path d="M{vx},{vy} L{ex:.0f},{vy-60*p:.0f}" stroke="{ZOLOTO}"'
                   f' stroke-width="6" opacity="{p:.2f}"/>'
                   f'<circle cx="{vx}" cy="{vy}" r="12" fill="{ZOLOTO}" opacity="{p:.2f}"/>'
                   f'<rect x="{min(vx,ex)-20:.0f}" y="{vy-100*p:.0f}" width="220"'
                   f' height="52" rx="10" fill="{GRAFIT}" opacity="{p*.9:.2f}" {o(3)}/>')
    s += SL(Z_SRED, tufli(1420, 1046, 1.2, GRAFIT, t))
    s += SL(Z_SRED, f'<path d="M1640,1046 q-24,-150 64,-154 l0,154 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(1700, 260, 180, 600, t, "pryam", ZOLOTO, True))
    # торшер: живой тёплый источник
    s += SL(Z_SRED, f'<rect x="420" y="620" width="14" height="430" fill="{CHUGUN}" {o(3)}/>'
                    f'<path d="M350,620 h154 l-24,-90 h-106 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, lampa_stolika(427, 600, t, 1.5))
    s += SL(Z_SRED, girlyanda(600, 150, 1200, t, 10, 113, 52))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tufli_lodochki_na_parkete(t):
    """Паркет у зеркала: подставка-нога в гладких колготках, рукав отодвигает
    упаковки с узорными и блестящими."""
    rnd = random.Random(2065)
    s = f'<rect width="{W}" height="{H}" fill="#241e1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 115))
    s += SL(Z_DAL, doski(0, 0, W, 620, 86))
    s += SL(Z_DAL, elka(1840, 1050, 320, t, 1.0, True, 117))
    s += SL(Z_SRED, polovicy(760))
    par_ = ""
    for i in range(16):
        par_ += (f'<path d="M{60+i*118},760 l0,320" stroke="#5a3d26"'
                 f' stroke-width="3" opacity=".5"/>')
    s += SL(Z_SRED, par_)
    # напольное зеркало: рисованный вид и рама (кадр отсюда снят)
    s += SL(Z_SRED, f'<rect x="150" y="150" width="620" height="720" rx="10"'
                    f' fill="#2a2420" {o(6)}/>'
            + zerkalo(150, 150, 620, 720, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="166" y="166" width="588" height="688" fill="{STEKLO}"'
                    f' opacity=".22"/>')
    # НАСТОЯЩИЙ КАДР ОТСЮДА СНЯТ (туфли сток даёт только на людях), поэтому
    # зеркало не остаётся пустым: в нём отражаются сами лодочки и край подола.
    s += SL(Z_SRED, f'<g opacity=".65">'
                    + f'<path d="M230,180 q150,40 300,0 l0,250 q-150,44 -300,0 Z"'
                      f' fill="{RUBIN}" {o(4)}/>'
                    + tufli(300, 800, 1.9, GRAFIT, t) + "</g>")
    # подставка-нога в гладких колготках
    nx = 1120
    s += SL(0, f'<path d="M{nx-56},1040 q-20,-280 56,-330 q76,50 56,330 Z"'
               f' fill="#d8b89c" {o(6)}/>')
    s += SL(0, f'<path d="M{nx-56},900 q56,-26 112,0" fill="none" stroke="#c7a68c"'
               f' stroke-width="5" opacity=".7"/>')
    s += SL(0, tufli(nx - 70, 1046, 1.3, GRAFIT, t, False))
    # упаковки колготок: рукав отодвигает две
    ot = A.out(A.seg(t, .4, 1.4))
    for i, c in enumerate((LAVANDA, SEREBRO)):
        ux = 1420 + i * 180 + 120 * ot
        s += SL(0, f'<g transform="rotate({8+14*ot:.1f} {ux} 940)">'
                   f'<rect x="{ux-80:.0f}" y="820" width="160" height="230" rx="10"'
                   f' fill="{c}" {o(5)}/>'
                   f'<rect x="{ux-60:.0f}" y="850" width="120" height="110" rx="8"'
                   f' fill="{MOLOKO}" opacity=".65"/></g>')
    ruk, _ = rukav(1380, 640, 230, 56 - 20 * ot, t, VINO, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    # край бархатного подола покачивается сверху
    s += SL(0, f'<path d="M980,150 q180,{40+14*A.w(t,2.0):.0f} 360,0 l0,120'
               f' q-180,{-30+10*A.w(t,2.0,.3):.0f} -360,0 Z" fill="{RUBIN}" {o(5)}/>')
    s += SL(Z_SRED, korobka(820, 1046, 260, t, 110, True, BEZH, MOLOKO))
    s += SL(Z_SRED, f'<path d="M1680,1046 q-20,-130 58,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1480,1046 l120,-16 l6,26 l-120,16 Z" fill="{DEREVO2}" {o(3)}/>')
    blik_hod = (A.w(t, 4.2, .2) + 1) / 2
    s += SL(Z_SRED, f'<path d="M{200+1300*blik_hod:.0f},760 l140,320 l-90,0 l-140,-320 Z"'
                    f' fill="#ffffff" opacity=".10"/>')
    s += SL(Z_SRED, girlyanda(820, 140, 1000, t, 9, 119, 48))
    s += SL(0, lampa_stolika(900, 560, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def sumochka_brosh_i_kole(t):
    """Туалетный столик: маленькая сумочка с блеском, а над брошью и колье
    качаются весы — надеть нужно что-то одно."""
    rnd = random.Random(2066)
    s = f'<rect width="{W}" height="{H}" fill="#231f27"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 121))
    s += SL(Z_DAL, stena("doski", t, 128))
    s += SL(Z_DAL, elka(120, 1050, 340, t, 1.0, True, 123))
    s += SL(Z_SRED, trumo(380, 1050, 1200, 440, t))
    s += SL(Z_SRED, zerkalo(700, 160, 560, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="714" y="174" width="532" height="492" fill="{STEKLO}"'
                    f' opacity=".26"/>')
    # сумочка на треть кадра
    sx, sy = 620, 900
    bl = .6 + .4 * abs(A.w(t, 1.6))
    s += SL(0, f'<path d="M{sx-150},{sy-170} q150,-60 300,0 l30,230 q-180,40 -360,0 Z"'
               f' fill="{GRAFIT}" {o(6)}/>')
    s += SL(0, f'<path d="M{sx-150},{sy-170} q150,-60 300,0" fill="none"'
               f' stroke="{SEREBRO}" stroke-width="10" opacity="{bl:.2f}"/>')
    s += SL(0, f'<path d="M{sx-110},{sy-180} q110,-190 230,-10" fill="none"'
               f' stroke="{SEREBRO}" stroke-width="7"/>')
    s += SL(0, tkan_blesk(sx - 150, sy - 170, 300, 230, t, "#ffffff", .5, .2))
    # две подушечки: брошь и колье, над ними весы
    for i, (px, c) in enumerate(((1180, ZOLOTO), (1480, SEREBRO))):
        s += SL(Z_SRED, f'<path d="M{px-90},{880} q90,-40 180,0 q-24,66 -90,70'
                        f' q-66,-4 -90,-70 Z" fill="{VINO}" {o(5)}/>')
        if i == 0:
            s += SL(0, f'<circle cx="{px}" cy="862" r="34" fill="{c}" {o(3)}/>')
            for j in range(8):
                a = j * 45
                s += SL(0, f'<circle cx="{px+44*math.cos(math.radians(a)):.0f}"'
                           f' cy="{862+44*math.sin(math.radians(a)):.0f}" r="10"'
                           f' fill="{c}" {o(2)}/>')
        else:
            s += SL(0, "".join(f'<circle cx="{px-70+j*20}" cy="{868+int(14*math.sin(j*.7))}"'
                               f' r="10" fill="{c}" {o(2)}/>' for j in range(8)))
    kach = 9 * A.w(t, 2.0, .2)
    s += SL(0, f'<g transform="rotate({kach:.2f} 1330 620)">'
               f'<path d="M1150,620 h360" stroke="{ZOLOTO}" stroke-width="8"/>'
               f'<path d="M1150,620 l0,60 M1510,620 l0,60" stroke="{ZOLOTO}"'
               f' stroke-width="5"/>'
               f'<path d="M1100,680 h100 l-16,46 h-68 Z" fill="{ZOLOTO}" {o(3)}/>'
               f'<path d="M1460,680 h100 l-16,46 h-68 Z" fill="{ZOLOTO}" {o(3)}/></g>')
    s += SL(0, f'<path d="M1330,620 l0,-130" stroke="{ZOLOTO}" stroke-width="7"/>')
    # рукава: правый берёт брошь, левый отодвигает колье
    ruk, _ = rukav(1120, 420, 230, 78, t, RUBIN, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    ruk2, _ = rukav(1620, 450, 220, 112, t, RUBIN, TEPLO_SVET, .5, 5.0, True)
    s += SL(0, ruk2)
    fl = ""
    for i in range(5):
        fx = 320 + i * 70
        h_ = 46 + (i % 3) * 22
        fl += (f'<rect x="{fx-16}" y="{980-h_}" width="32" height="{h_}" rx="6"'
               f' fill="{(PUDRA, LAVANDA, MOLOKO, KORALL, ZOLOTO)[i]}" {o(3)}/>')
    s += SL(Z_SRED, fl)
    s += SL(Z_SRED, f'<path d="M1700,1000 q50,-30 96,-4 l-8,54 q-46,20 -92,-6 Z"'
                    f' fill="{MOLOKO}" {o(4)}/>')
    s += SL(Z_SRED, svecha(1800, 950, t, .4, 1.3))
    s += SL(Z_SRED, girlyanda(300, 140, 1400, t, 10, 125, 50))
    s += SL(0, lampa_stolika(980, 960, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def trikotazh_i_barhatnyy_zhaket(t):
    """Рубиновое трикотажное платье на плечиках: сверху ложится бархатный
    жакет, потом его сменяет бархатный шарф."""
    rnd = random.Random(2068)
    s = f'<rect width="{W}" height="{H}" fill="#241f23"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 127))
    s += SL(Z_DAL, stena("oboi", t, 129))
    s += SL(Z_DAL, shkaf(820, 1050, 940, 960, t, .95, True))
    s += SL(Z_DAL, elka(130, 1050, 360, t, 1.0, True, 129))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, naryad_plechiki(1240, 230, 600, t, RUBIN, 1.5, .1, True, None, .05, 130, 1.5))
    # жакет ложится, потом сменяется шарфом
    faza = A.seg(t, .3, 3.2)
    zh = max(0.0, min(1.0, faza * 2.2))
    sh = max(0.0, min(1.0, (faza - .55) * 2.6))
    if sh < .1:
        s += SL(0, f'<g opacity="{zh:.2f}">'
                   f'<path d="M1090,{300-120*(1-zh):.0f} h300 l24,330 h-348 Z"'
                   f' fill="#4a1b2a" {o(6)}/>'
                   f'<path d="M1240,{300-120*(1-zh):.0f} l0,330" stroke="{K}"'
                   f' stroke-width="4" opacity=".5"/></g>')
    else:
        s += SL(0, f'<path d="M1130,{300-100*(1-sh):.0f} q60,150 24,360 l72,16'
                   f' q44,-230 -16,-380 Z" fill="#4a1b2a" opacity="{sh:.2f}" {o(5)}/>')
    # женщина обеими руками работает с плечиками
    s += SL(0, figura(660, 1050, 520, t, GRAFIT, HOLOD_KANT, .3, False, False, 1.0,
                      2.0, True, True, "#eec9a6", True, MOLOKO, True))
    for sgn, ug in ((-1, -46), (1, -26)):
        ruk, _ = rukav(660 + sgn * 92, 740, 250, ug, t, GRAFIT, HOLOD_KANT,
                       .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    s += SL(Z_SRED, f'<path d="M280,1046 q-30,-150 70,-154 q100,4 70,154 Z"'
                    f' fill="url(#solom)" {o(5)}/>')
    s += SL(Z_SRED, tufli(470, 1046, 1.1, RUBIN, t))
    s += SL(Z_SRED, zerkalo(60, 300, 200, 540, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<path d="M1760,1046 q-20,-140 60,-144 l0,144 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(300, 140, 1500, t, 11, 131, 54))
    s += SL(0, lampa_stolika(1700, 900, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tufli_v_pakete(t):
    """Заснеженная улица под фонарями: мама с дочкой идут в гости, из пакета
    торчат каблучки нарядных туфель. В витрине — настоящая зимняя улица."""
    rnd = random.Random(2069)
    s = f'<rect width="{W}" height="{H}" fill="#101824"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 133))
    s += SL(Z_DAL, panelka(1180, 720, 700, t, 5, True, 135))
    s += SL(Z_DAL, ulica_dal(60, 680, 900, t, True, 137))
    s += SL(Z_DAL, sneg_letit(t, 46, 139, .8, 1.0))
    # витрина магазина: рисованный вид, метка, переплёт поверх
    px, py, pw, ph = 1040, 300, 800, 320
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#16202c"/>'
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-16}" y="{py-16}" width="{pw+32}" height="{ph+32}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="24"/>'
            + f'<path d="M{px+pw/2:.0f},{py-16} l0,{ph+32}" stroke="{DEREVO2}"'
              f' stroke-width="14"/>')
    s += SL(Z_SRED, f'<rect x="0" y="900" width="{W}" height="180" fill="{SNEG}"'
                    f' opacity=".85"/>')
    sug = "".join(f'<ellipse cx="{120+i*260}" cy="910" rx="150" ry="40" fill="{SNEG}"'
                  f' {o(2)}/>' for i in range(8))
    s += SL(Z_SRED, sug)
    # мама и дочка идут слева направо
    p = A.seg(t, .2, 3.0)
    mx = 260 + 420 * p
    s += SL(0, figura(mx, 1000, 500, t, "#5c4a3f", HOLOD_KANT, .2, False, False, 1.0,
                      2.5, True, True, "#f0cfae", False, "#8a7466", True))
    ruk, (hx, hy) = rukav(mx + 86, 740, 180, 76, t, "#5c4a3f", HOLOD_KANT, .2, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(mx - 86, 760, 170, 104, t, "#5c4a3f", HOLOD_KANT, .5, 5.0)
    s += SL(0, ruk2)
    # пакет с каблучками
    kach = 7 * A.w(t, 1.5, .2)
    s += SL(0, f'<g transform="rotate({kach:.2f} {hx:.0f} {hy:.0f})">'
               f'<path d="M{hx-66:.0f},{hy:.0f} h132 l14,180 h-160 Z" fill="{KREM2}" {o(5)}/>'
               f'<path d="M{hx-36:.0f},{hy-14:.0f} q36,-40 72,0" fill="none"'
               f' stroke="{BEZH}" stroke-width="6"/>'
               f'<path d="M{hx-24:.0f},{hy-6:.0f} l-10,-58 l16,-2 l12,58 Z"'
               f' fill="{RUBIN}" {o(3)}/>'
               f'<path d="M{hx+22:.0f},{hy-6:.0f} l10,-54 l16,4 l-12,52 Z"'
               f' fill="{RUBIN}" {o(3)}/></g>')
    # дочка в шубке и валенках с мешочком
    dx = mx + 190
    s += SL(0, figura(dx, 1010, 330, t, "#7a5a4a", HOLOD_KANT, .6, False, False, 1.0,
                      3.0, True, True, "#f3d3b2", False, MOLOKO, False))
    s += SL(0, f'<path d="M{dx-52},1010 q20,-80 52,-80 q32,0 52,80 Z"'
               f' fill="#6b6256" {o(4)}/>')
    ruk3, (h3x, h3y) = rukav(dx + 56, 820, 120, 88, t, "#7a5a4a", HOLOD_KANT, .3, 5.0)
    s += SL(0, ruk3)
    s += SL(0, f'<path d="M{h3x-30:.0f},{h3y:.0f} q30,-16 60,0 l8,76 q-38,16 -76,0 Z"'
               f' fill="{KORALL}" {o(4)}/>')
    s += SL(0, para_izo_rta(mx + 40, 700, t, .2, 1.1, .5))
    s += SL(0, para_izo_rta(dx + 30, 810, t, .6, .8, .45))
    # фонари, троллейбус-силуэт, собака
    for i, fx2 in enumerate((160, 760)):
        s += SL(Z_SRED, f'<rect x="{fx2}" y="380" width="14" height="530"'
                        f' fill="{CHUGUN}" {o(4)}/>'
                        f'<path d="M{fx2-40},380 q47,-54 94,0 Z" fill="{ZOLOTO}"'
                        f' opacity=".9" {o(3)}/>')
        s += SL(Z_SRED, teplo(fx2 + 7, 400, 240, 220, .28 + .08 * abs(A.w(t, 2.0, i * .3))))
    s += SL(Z_DAL, f'<path d="M60,780 h420 l0,120 h-420 Z" fill="#1d2630" {o(5)}/>')
    sob = 40 * A.w(t, 2.6)
    s += SL(Z_SRED, f'<ellipse cx="{mx-220+sob:.0f}" cy="980" rx="56" ry="28"'
                    f' fill="#3a3028" {o(4)}/>'
                    f'<circle cx="{mx-170+sob:.0f}" cy="950" r="24" fill="#3a3028" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def sapogi_u_dveri(t):
    """Прихожая в гостях: гостья меняет сапоги на лодочки, рядом на коврике
    натекла снежная лужица, кот нюхает сапог."""
    rnd = random.Random(2070)
    s = f'<rect width="{W}" height="{H}" fill="#241d1c"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 141))
    s += SL(Z_DAL, stena("kirpich", t, 131))
    s += SL(Z_DAL, dver(1480, 120, 380, 820, .12, "url(#derev)", True, True))
    s += SL(Z_SRED, polovicy(1000))
    # вешалка с шубами
    s += SL(Z_SRED, f'<rect x="120" y="260" width="700" height="18" rx="8"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    for i, c in enumerate(("#6b5347", "#4a3f38", "#7a6a58")):
        sx = 240 + i * 220
        s += SL(Z_SRED, naryad_plechiki(sx, 280, 420, t, c, 1.2, i * .3, False, MOLOKO, .0, 142 + i))
    # коврик, сапоги, лужица
    s += SL(Z_SRED, f'<rect x="900" y="940" width="560" height="110" rx="12"'
                    f' fill="#5a4038" {o(5)}/>')
    for i in range(10):
        s += SL(Z_SRED, f'<path d="M{920+i*56},944 l0,102" stroke="#7a5a4a"'
                        f' stroke-width="4" opacity=".7"/>')
    for i in range(2):
        bx = 980 + i * 120
        s += SL(0, f'<path d="M{bx-40},1000 q-12,-250 48,-256 q60,6 48,256 Z"'
                   f' fill="#3a3038" {o(5)}/>'
                   f'<path d="M{bx+8},760 l0,230" stroke="{SEREBRO}" stroke-width="5"/>')
    luzh = .5 + .5 * A.seg(t, .4, 2.4)
    s += SL(Z_SRED, f'<ellipse cx="1060" cy="1046" rx="{150*luzh:.0f}" ry="{28*luzh:.0f}"'
                    f' fill="{STEKLO}" opacity=".45"/>')
    # гостья на пуфе надевает вторую лодочку
    s += SL(0, f'<path d="M520,1000 q-30,-160 80,-166 q110,6 80,166 Z"'
               f' fill="#45384f" {o(6)}/>')
    s += SL(0, figura(600, 870, 430, t, RUBIN, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, False))
    nad = A.out(A.seg(t, .4, 1.4))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(600 + sgn * 70, 690, 200, 64 + sgn * 12 + 14 * nad, t,
                              RUBIN, TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
    s += SL(0, tufli(540, 1000, 1.0, GRAFIT, t, False))
    s += SL(0, f'<g transform="translate({40*(1-nad):.0f},{-60*(1-nad):.0f})">'
               + tufli(660, 1000, 1.0, GRAFIT, t, False) + "</g>")
    # пакет, сумочка, венок, тапки, кот
    s += SL(Z_SRED, f'<path d="M820,1000 h120 l14,-150 h-148 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M760,960 q40,-16 62,14 l12,86 h-92 Z" fill="{GRAFIT}" {o(4)}/>')
    ven = ""
    for i in range(14):
        a = i * 26
        ven += (f'<ellipse cx="{1660+80*math.cos(math.radians(a)):.0f}"'
                f' cy="{300+80*math.sin(math.radians(a)):.0f}" rx="20" ry="12"'
                f' fill="{HVOYA}" {o(2)}/>')
    s += SL(Z_SRED, ven)
    s += SL(Z_SRED, "".join(f'<path d="M{1240+i*80},1020 q40,-40 80,0 q-40,24 -80,0 Z"'
                            f' fill="{KORALL}" {o(3)}/>' for i in range(2)))
    s += SL(Z_SRED, kot(1180, 1000, t, 1.4, "#6b5a46"))
    s += SL(Z_SRED, girlyanda(120, 150, 1700, t, 10, 145, 52))
    s += SL(0, lampa_stolika(1300, 420, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s
