# -*- coding: utf-8 -*-
"""Декорации ролика «В чём встречать Новый год 2027», часть 4 (планы 104-144).

Шестой и седьмой мужские наряды, глава мелочей, памятка из пяти бирок и финал
с Огненной Козой. Все сцены нарисованы заново (R-0019).
"""
import math, random
from baza import *
from lok_obshchee import *
import anim as A


def _flakony(x, y, t, n=5, seed=9):
    """Флаконы на трюмо — сквозная мелочь главы о мелочах."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        fx = x + i * 78
        h_ = rnd.uniform(44, 86)
        c = rnd.choice((LAVANDA, PUDRA, MOLOKO, KORALL, ZOLOTO, KREM2))
        s += (f'<rect x="{fx-18:.0f}" y="{y-h_:.0f}" width="36" height="{h_:.0f}"'
              f' rx="7" fill="{c}" {o(3)}/>'
              f'<rect x="{fx-8:.0f}" y="{y-h_-14:.0f}" width="16" height="16" rx="4"'
              f' fill="{SEREBRO}" {o(2)}/>'
              f'<rect x="{fx-13:.0f}" y="{y-h_*.7:.0f}" width="8" height="{h_*.4:.0f}"'
              f' fill="#ffffff" opacity="{.18+.14*abs(A.w(t, 2.6, i*.3)):.2f}"/>')
    return s


def _medalon(cx, cy, r, t, p, risunok):
    """Круглая картинка-медальон: рамка, свет и то, что внутри."""
    s = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#2b2430" opacity="{.35+.55*p:.2f}"'
         f' stroke="{ZOLOTO}" stroke-width="{6+4*p:.0f}"/>')
    s += f'<g opacity="{p:.2f}">{risunok}</g>'
    return s


def temnyy_pidzhak_i_vinnyy_galstuk(t):
    """Муж снимает тёмный пиджак и прикладывает к нему винный галстук; жена в
    дверях показывает «хорошо»."""
    rnd = random.Random(4104)
    s = f'<rect width="{W}" height="{H}" fill="#1f1b1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 401))
    s += SL(Z_DAL, stena("oboi", t, 101))
    s += SL(Z_DAL, shkaf(520, 1050, 1120, 1000, t, 1.0, False))
    s += SL(Z_SRED, perekladina(1080, 270, 920))
    s += SL(Z_SRED, polovicy(1050))
    snyat = A.out(A.seg(t, .3, 1.4))
    s += SL(Z_SRED, naryad_plechiki(760, 300, 480, t, MOLOKO, 1.2, .2, False, KREM2, .05, 402))
    px = 1280 - 360 * snyat
    s += SL(0, naryad_plechiki(px, 300 + 80 * snyat, 470, t, GRAFIT, 1.25, .1,
                               False, MOLOKO, .04, 403, 1.6))
    gal = A.out(A.seg(t, 1.0, 1.2))
    s += SL(0, f'<path d="M{px-14:.0f},{330+80*snyat:.0f} l28,0 l-8,120 l30,130 h-72'
               f' l30,-130 Z" fill="{VINO}" opacity="{gal:.2f}" {o(4)}/>')
    q = A.out(A.seg(t, 1.9, .5))
    s += SL(0, f'<path d="M700,420 l34,42 l66,-88" fill="none" stroke="#3fae62"'
               f' stroke-width="18" stroke-linecap="round" opacity="{q:.2f}"/>')
    s += SL(0, figura(280, 1050, 540, t, "#4a4440", TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", False, MOLOKO, True))
    ruk, _ = rukav(370, 740, 250, -34 + 16 * snyat, t, "#4a4440", TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(210, 780, 190, -8, t, "#4a4440", TEPLO_SVET, .5, 5.0)
    s += SL(0, ruk2)
    # жена-силуэт в дверях показывает «хорошо»
    s += SL(Z_DAL, f'<rect x="1720" y="200" width="200" height="850" rx="10"'
                   f' fill="#161218" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1820" cy="760" rx="54" ry="150" fill="#14111a"'
                    f' opacity=".9"/><circle cx="1820" cy="596" r="42" fill="#14111a"'
                    f' opacity=".9"/>')
    mah = 14 * A.w(t, 1.6, .3)
    s += SL(Z_SRED, f'<g transform="rotate({mah:.1f} 1780 700)">'
                    f'<path d="M1780,700 l-70,-80" stroke="#14111a" stroke-width="26"'
                    f' stroke-linecap="round"/>'
                    f'<circle cx="1700" cy="606" r="26" fill="none" stroke="{ZOLOTO}"'
                    f' stroke-width="7"/></g>')
    s += SL(Z_SRED, "".join(f'<path d="M{860+i*170},1040 q14,-60 72,-62 q58,2 72,62 Z"'
                            f' fill="#2b2420" {o(4)}/>' for i in range(2)))
    s += SL(Z_SRED, zerkalo(60, 320, 180, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(400, 130, 1300, t, 10, 404, 46))
    s += SL(0, lampa_stolika(1640, 940, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def kostyum_iz_chehla_raz_v_godu(t):
    """С антресоли снимают костюм в чехле: внутри тёмно-синий костюм, с лацкана
    слетает прошлогодняя еловая иголка."""
    rnd = random.Random(4105)
    s = f'<rect width="{W}" height="{H}" fill="#221c1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 405))
    s += SL(Z_DAL, stena("kraska", t, 102))
    s += SL(Z_DAL, f'<rect x="820" y="60" width="1000" height="320" rx="10"'
                   f' fill="#2a2420" {o(6)}/>')
    s += SL(Z_DAL, korobka(1500, 360, 280, t, 110, False, "#b8a289", MOLOKO))
    s += SL(Z_DAL, f'<path d="M1300,360 q90,-70 180,0 q-50,30 -90,30 q-40,0 -90,-30 Z"'
                   f' fill="#4a3f38" {o(4)}/>')
    s += SL(Z_SRED, polovicy(1050))
    # стремянка
    s += SL(Z_SRED, f'<path d="M400,1050 l120,-520 M760,1050 l-120,-520"'
                    f' stroke="{DEREVO}" stroke-width="22"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{430+i*14}" y="{620+i*140}" width="{300-i*28}"'
                        f' height="24" rx="6" fill="{DEREVO2}" {o(4)}/>')
    # мужчина на стремянке с чехлом
    snyat = A.out(A.seg(t, .25, 1.3))
    s += SL(0, figura(580, 760, 480, t, "#7a6a58", TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#eec9a6", False, None, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(580 + sgn * 80, 480, 180, -76 - sgn * 12, t, "#7a6a58",
                       TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    kx, ky = 620 + 220 * snyat, 300 + 140 * snyat
    rasst = A.out(A.seg(t, 1.2, 1.2))
    s += SL(0, f'<path d="M{kx-130:.0f},{ky:.0f} h260 l20,440 h-300 Z"'
               f' fill="{KREM2}" opacity="{1-rasst*.55:.2f}" {o(6)}/>')
    if rasst > .1:
        s += SL(0, f'<path d="M{kx-100:.0f},{ky+30:.0f} h200 l16,380 h-232 Z"'
                   f' fill="{TSINIY}" opacity="{rasst:.2f}" {o(5)}/>')
        s += SL(0, f'<path d="M{kx:.0f},{ky+30:.0f} l0,380" stroke="{SEREBRO}"'
                   f' stroke-width="5" opacity="{rasst:.2f}"/>')
    # еловая иголка слетает
    ig = A.seg(t, 1.6, 1.6)
    if ig > 0:
        s += SL(0, f'<path d="M{kx+60:.0f},{ky+120+520*ig:.0f} l26,{6+10*ig:.0f}"'
                   f' stroke="{HVOYA}" stroke-width="6" stroke-linecap="round"'
                   f' opacity="{1-ig*.4:.2f}"/>')
    s += SL(Z_SRED, kot(880, 1046, t, 1.4, "#6b5a46"))
    s += SL(Z_SRED, korobka(1100, 1046, 300, t, 120, True, "#a8926f", MOLOKO))
    sh = ""
    for i in range(5):
        sh += (f'<circle cx="{1160+i*54}" cy="950" r="26"'
               f' fill="{(KORALL, ZOLOTO, IZUMRUD, SEREBRO, VINO)[i]}"'
               f' opacity="{.7+.3*abs(A.w(t,1.9,i*.3)):.2f}" {o(2)}/>')
    s += SL(Z_SRED, sh)
    s += SL(Z_SRED, girlyanda(900, 420, 900, t, 9, 406, 44))
    s += SL(0, lampa_stolika(1700, 820, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def kostyum_s_vodolazkoy_na_manekene(t):
    """Торс в тёмно-синем костюме: рубашка с галстуком сменяется тонкой
    водолазкой, галстук улетает на вешалку."""
    rnd = random.Random(4106)
    s = f'<rect width="{W}" height="{H}" fill="#1e1c23"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 407))
    s += SL(Z_DAL, stena("paneli", t, 103))
    s += SL(Z_DAL, elka(1820, 1050, 400, t, 1.0, True, 408))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, manekken(880, 1000, 660, t, KREM2, "m", TSINIY, .2, None, .04, 409))
    faza = A.seg(t, .3, 3.0)
    rub = max(0.0, 1 - faza * 2.4)
    vod = max(0.0, min(1.0, (faza - .35) * 2.4))
    s += SL(0, f'<path d="M800,480 h160 l10,160 h-180 Z" fill="{MOLOKO}"'
               f' opacity="{rub:.2f}" {o(4)}/>')
    s += SL(0, f'<path d="M866,480 l28,0 l-8,110 l26,110 h-64 l26,-110 Z"'
               f' fill="{TSINIY}" opacity="{rub:.2f}" {o(3)}/>')
    vodc = MOLOKO if (t % 3.0) < 1.5 else VINO
    s += SL(0, f'<path d="M790,470 h180 l14,180 h-208 Z" fill="{vodc}"'
               f' opacity="{vod:.2f}" {o(5)}/>')
    s += SL(0, f'<path d="M846,440 q34,-20 68,0 l0,40 q-34,18 -68,0 Z" fill="{vodc}"'
               f' opacity="{vod:.2f}" {o(3)}/>')
    # галстук улетает на вешалку
    let = A.out(A.seg(t, 1.1, 1.4))
    gx = 880 + 620 * let
    gy = 560 - 220 * let
    s += SL(0, f'<g opacity="{let:.2f}" transform="rotate({40*let:.0f} {gx:.0f} {gy:.0f})">'
               f'<path d="M{gx-14:.0f},{gy:.0f} l28,0 l-8,110 l26,110 h-64 l26,-110 Z"'
               f' fill="{TSINIY}" {o(3)}/></g>')
    # НАСТОЯЩАЯ ткань костюма в отражении (его слово 17.11) — метка перед
    # рамой (опора 14.11); зеркало расширено до нормы проёма R-0024
    s += SL(Z_SRED, mesto_stoka(94, 334, 760, 492, "pryam"))
    s += SL(Z_SRED, zerkalo(80, 320, 788, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1420" y="300" width="300" height="18" rx="8"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    s += SL(Z_SRED, naryad_plechiki(1560, 320, 380, t, GRAFIT, 1.0, .4, False, None, .04, 410))
    s += SL(Z_SRED, "".join(f'<path d="M{480+i*170},1040 q14,-60 72,-62 q58,2 72,62 Z"'
                            f' fill="#2b2420" {o(4)}/>' for i in range(2)))
    s += SL(Z_SRED, f'<rect x="300" y="880" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="310" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="442" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, girlyanda(400, 130, 1200, t, 10, 411, 46))
    s += SL(0, lampa_stolika(1300, 820, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def salyut_s_balkona_v_vodolazke(t):
    """Балкон новогодней ночью: в водолазке тепло, соседу в рубашке с галстуком
    холодно. В проёме балконной двери — настоящий морозный узор."""
    rnd = random.Random(4107)
    s = f'<rect width="{W}" height="{H}" fill="#0d1420"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 412))
    s += SL(Z_DAL, panelka(1180, 760, 740, t, 6, True, 413))
    s += SL(Z_DAL, ulica_dal(40, 740, 900, t, True, 414))
    # салют над крышами
    for i in range(3):
        p = ((t * .5 + i * .33) % 1.0)
        cx, cy = 420 + i * 520, 240 + (i % 2) * 90
        for j in range(16):
            a = j * 22.5
            r = 40 + 170 * p
            s += SL(Z_DAL, f'<circle cx="{cx+r*math.cos(math.radians(a)):.0f}"'
                           f' cy="{cy+r*math.sin(math.radians(a)):.0f}" r="{7*(1-p):.1f}"'
                           f' fill="{(KORALL, ZOLOTO, SEREBRO)[i]}"'
                           f' opacity="{(1-p)*.9:.2f}"/>')
    s += SL(Z_DAL, sneg_letit(t, 30, 415, .5, .8))
    # балконная дверь: проём с настоящим кадром
    px, py, pw, ph = 120, 240, 760, 420
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#16202c"/>'
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-16}" y="{py-16}" width="{pw+32}" height="{ph+32}"'
              f' fill="none" stroke="{MOLOKO}" stroke-width="24"/>')
    s += SL(Z_DAL, elka(300, 640, 300, t, 1.0, True, 416))
    # перила в снегу
    s += SL(Z_SRED, f'<rect x="0" y="820" width="{W}" height="40" rx="10"'
                    f' fill="{CHUGUN}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="0" y="806" width="{W}" height="20" rx="8"'
                    f' fill="{SNEG}" opacity=".9"/>')
    for i in range(16):
        s += SL(Z_SRED, f'<rect x="{40+i*120}" y="860" width="14" height="220"'
                        f' fill="{CHUGUN}" {o(3)}/>')
    # мужчина в костюме с винной водолазкой держит бенгальский огонь
    s += SL(0, figura(760, 1060, 520, t, TSINIY, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", False, VINO, True))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(760 + sgn * 80, 780, 170, -56 - sgn * 10, t, TSINIY,
                              TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
    bx, by = 760, 600
    s += SL(0, f'<path d="M{bx},{by+90} l0,-130" stroke="{SEREBRO}" stroke-width="5"/>')
    s += SL(0, ogon(bx, by - 40, t, .55, .1, 7))
    for i in range(10):
        a = rnd.uniform(0, 360)
        r = 40 + 50 * abs(A.w(t, .9, i * .2))
        s += SL(0, f'<circle cx="{bx+r*math.cos(math.radians(a)):.0f}"'
                   f' cy="{by-40+r*math.sin(math.radians(a)):.0f}" r="4"'
                   f' fill="{ZOLOTO}" opacity="{.4+.6*abs(A.w(t,1.3,i*.3)):.2f}"/>')
    s += SL(0, teplo(bx, by, 420, 380, .28 + .10 * abs(A.w(t, 1.5))))
    # сосед на соседнем балконе ёжится
    s += SL(0, figura(1540, 1060, 470, t, GRAFIT, HOLOD_KANT, .6, False, False, 1.0,
                      3.5, True, True, "#eec9a6", False, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(1540 + sgn * 76, 780, 130, -150 + sgn * 30, t, GRAFIT,
                       HOLOD_KANT, .5 + (0 if sgn < 0 else .3), 7.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M1526,700 l28,0 l-8,100 l24,100 h-60 l24,-100 Z"'
               f' fill="{VINO}" {o(3)}/>')
    s += SL(0, para_izo_rta(1580, 700, t, .3, 1.2, .55))
    s += SL(Z_SRED, "".join(f'<path d="M{1000+i*150},1060 q14,-60 72,-62 q58,2 72,62 Z"'
                            f' fill="#2b2420" {o(4)}/>' for i in range(2)))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def sous_letit_na_rubashku(t):
    """За столом: на белой рубашке капля соуса расплывается пятном, на винной
    водолазке её не видно."""
    rnd = random.Random(4108)
    s = f'<rect width="{W}" height="{H}" fill="#241c20"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 417))
    s += SL(Z_DAL, stena("kraska", t, 105))
    s += SL(Z_DAL, elka(1830, 1050, 400, t, 1.0, True, 418))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, stol(80, 860, 1500, 46))
    s += SL(Z_SRED, f'<path d="M70,820 h1520 l-24,200 q-740,40 -1470,0 Z"'
                    f' fill="{MOLOKO}" {o(5)}/>')
    s += SL(Z_SRED, "".join(f'<ellipse cx="{220+i*210}" cy="828" rx="60" ry="19"'
                            f' fill="{KREM2}" {o(3)}/>' for i in range(6)))
    s += SL(Z_SRED, svecha(760, 824, t, .2, 1.3) + svecha(1240, 824, t, .6, 1.2))
    s += SL(Z_SRED, f'<path d="M980,820 q-30,-90 40,-96 q70,6 40,96 Z"'
                    f' fill="url(#glina)" {o(4)}/>')
    # левый в белой рубашке: капля летит и расплывается
    s += SL(0, figura(520, 880, 470, t, GRAFIT, TEPLO_SVET, .2, False, False, 1.0,
                      1.5, True, True, "#f0cfae", False, MOLOKO, False))
    s += SL(0, f'<path d="M440,640 h160 l0,160 h-160 Z" fill="{MOLOKO}" {o(5)}/>')
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(520 + sgn * 74, 700, 140, 20 - sgn * 10, t, GRAFIT,
                              TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 3.0)
        s += SL(0, ruk)
    p = A.seg(t, .3, 1.2)
    kx, ky = 600 - 80 * p, 620 + 110 * p
    if p < .95:
        s += SL(0, f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="13" fill="#7a3a1a" {o(2)}/>')
    else:
        q = A.out(A.seg(t, 1.5, 1.0))
        s += SL(0, f'<ellipse cx="520" cy="730" rx="{20+40*q:.0f}" ry="{14+28*q:.0f}"'
                   f' fill="#7a3a1a" opacity="{.85:.2f}"/>')
    # правый в винной водолазке: капля не видна
    s += SL(0, figura(1180, 880, 470, t, GRAFIT, TEPLO_SVET, .5, False, False, 1.0,
                      1.5, True, True, "#eec9a6", False, VINO, False))
    s += SL(0, f'<path d="M1100,640 h160 l0,160 h-160 Z" fill="{VINO}" {o(5)}/>')
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(1180 + sgn * 74, 700, 140, 24 - sgn * 10, t, GRAFIT,
                              TEPLO_SVET, .5 + (0 if sgn < 0 else .3), 3.0)
        s += SL(0, ruk)
    if p >= .95:
        s += SL(0, f'<ellipse cx="1180" cy="730" rx="34" ry="24" fill="#5c0f22"'
                   f' opacity=".55"/>')
    s += SL(Z_SRED, f'<path d="M1420,820 q70,-40 130,-10 l-20,60 q-70,24 -120,-6 Z"'
                    f' fill="{MOLOKO}" {o(4)}/>')
    s += SL(Z_SRED, girlyanda(140, 120, 1500, t, 11, 419, 46))
    s += SL(0, lampa_stolika(1660, 760, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tonkaya_i_tolstaya_vodolazka(t):
    """Два торса в одинаковых пиджаках: под левым толстая вязка топорщится,
    под правым тонкая лежит ровно."""
    rnd = random.Random(4109)
    s = f'<rect width="{W}" height="{H}" fill="#201d22"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 420))
    s += SL(Z_DAL, stena("kraska", t, 106))
    s += SL(Z_DAL, elka(1840, 1050, 320, t, 1.0, True, 421))
    s += SL(Z_SRED, polovicy(1050))
    for i, x in enumerate((560, 1260)):
        s += SL(0, manekken(x, 1000, 620, t, KREM2, "m", GRAFIT, i * .3, None, .04, 422 + i))
    # левый: толстая вязка, пиджак топорщится
    top = abs(A.w(t, 1.4))
    s += SL(0, f'<path d="M{480-16*top:.0f},480 h160 l{20+16*top:.0f},180 h-200 Z"'
               f' fill="{BEZH}" {o(5)}/>')
    vz = ""
    for i in range(9):
        vz += (f'<path d="M{486+i*18},490 q10,24 0,48 q-10,24 0,48" fill="none"'
               f' stroke="#a08b6a" stroke-width="4" opacity=".6"/>')
    s += SL(0, vz)
    s += SL(0, f'<circle cx="560" cy="700" r="{16+5*top:.0f}" fill="{ZOLOTO}" {o(3)}/>')
    s += SL(0, f'<path d="M470,420 l180,0" stroke="#d13a3a" stroke-width="14"'
               f' opacity=".9"/>')
    # правый: тонкая водолазка, пиджак ровный
    s += SL(0, f'<path d="M1180,470 h160 l14,180 h-188 Z" fill="{MOLOKO}" {o(5)}/>')
    s += SL(0, f'<path d="M1232,440 q30,-18 60,0 l0,36 q-30,16 -60,0 Z" fill="{MOLOKO}"'
               f' {o(3)}/>')
    q = A.out(A.seg(t, .6, .6))
    s += SL(0, f'<path d="M1180,420 l34,42 l66,-88" fill="none" stroke="#3fae62"'
               f' stroke-width="18" stroke-linecap="round" opacity="{q:.2f}"/>')
    sv = 9 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<rect x="820" y="880" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="830" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="962" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M900,880 q{20+sv:.0f},110 {-12+sv:.0f},210"'
                    f' fill="none" stroke="{MOLOKO}" stroke-width="11"/>')
    s += SL(Z_SRED, zerkalo(80, 320, 180, 540, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(400, 130, 1200, t, 10, 424, 46))
    s += SL(0, lampa_stolika(1660, 880, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def kostyum_na_tri_torzhestva(t):
    """Тёмно-синий костюм в центре и три медальона вокруг: юбилей, свадьба,
    выпускной — костюм оказывается в каждом."""
    rnd = random.Random(4110)
    s = f'<rect width="{W}" height="{H}" fill="#1e1c24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 425))
    s += SL(Z_DAL, stena("paneli", t, 107))
    s += SL(Z_DAL, shkaf(1480, 1050, 400, 900, t, .7, True))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, naryad_plechiki(960, 320, 540, t, TSINIY, 1.5, .1, False, MOLOKO, .05, 426, 1.4))
    hod = A.seg(t, .3, 3.3)
    akt = min(2, int(hod * 3))
    MED_ = (("торт", 420, 420), ("букет", 1500, 420), ("лента", 960, 940))
    for i, (kind, cx, cy) in enumerate(MED_):
        p = 1.0 if i == akt else .35
        if kind == "торт":
            ris = (f'<path d="M{cx-70},{cy+40} h140 l-10,-80 h-120 Z" fill="{MOLOKO}"/>'
                   f'<path d="M{cx-50},{cy-40} l0,-30 M{cx},{cy-40} l0,-30'
                   f' M{cx+50},{cy-40} l0,-30" stroke="{ZOLOTO}" stroke-width="7"/>')
        elif kind == "букет":
            ris = "".join(f'<circle cx="{cx-50+j*26}" cy="{cy-30+(j%2)*20}" r="18"'
                          f' fill="{(KORALL, MOLOKO, PUDRA, KORALL, MOLOKO)[j]}"/>'
                          for j in range(5)) + \
                  f'<path d="M{cx},{cy} l0,70" stroke="{HVOYA}" stroke-width="8"/>'
        else:
            ris = (f'<path d="M{cx-80},{cy-20} q80,50 160,0 l10,40 q-90,54 -180,0 Z"'
                   f' fill="{ALYY}"/>')
        s += SL(Z_SRED, _medalon(cx, cy, 150, t, p, ris))
        if i == akt:
            s += SL(Z_SRED, teplo(cx, cy, 320, 300, .22))
            s += SL(0, f'<path d="M{cx-50},{cy-60} h100 l12,150 h-124 Z" fill="{TSINIY}"'
                       f' opacity=".9" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="120" y="760" width="200" height="250" rx="10"'
                    f' fill="{MOLOKO}" {o(5)}/>'
                    f'<rect x="120" y="760" width="200" height="54" rx="10"'
                    f' fill="{KORALL}" {o(3)}/>')
    lst = A.seg(t, .4, 2.8)
    s += SL(Z_SRED, f'<path d="M130,{820+60*lst:.0f} h180 l0,{120-60*lst:.0f} h-180 Z"'
                    f' fill="{KREM2}" opacity=".85"/>')
    s += SL(Z_SRED, "".join(f'<path d="M{1640+i*120},1040 q14,-60 72,-62 q58,2 72,62 Z"'
                            f' fill="#2b2420" {o(4)}/>' for i in range(1)))
    s += SL(Z_SRED, zerkalo(1760, 300, 140, 480, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(260, 120, 1400, t, 11, 427, 44))
    s += SL(0, lampa_stolika(260, 1000, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def odna_krasnaya_vesch_na_muzhchine(t):
    """На мужчине в тёмном костюме вспыхивает одна красная вещь: сначала винный
    галстук, потом винный джемпер. Коза рядом одобрительно кивает."""
    rnd = random.Random(4111)
    s = f'<rect width="{W}" height="{H}" fill="#201b22"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 428))
    s += SL(Z_DAL, stena("doski", t, 108))
    s += SL(Z_DAL, elka(190, 1050, 460, t, 1.0, True, 429))
    s += SL(Z_SRED, f'<rect x="420" y="980" width="1200" height="70" rx="14"'
                    f' fill="#5a3a3a" {o(5)}/>')
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, figura(920, 1000, 620, t, GRAFIT, TEPLO_SVET, .2, False, False, 1.0,
                      1.5, True, True, "#f0cfae", False, MOLOKO, True))
    faza = (t % 3.4)
    if faza < 1.7:
        s += SL(0, f'<path d="M906,640 l28,0 l-8,130 l30,140 h-72 l30,-140 Z"'
                   f' fill="{VINO}" {o(4)}/>')
    else:
        s += SL(0, f'<path d="M830,630 h180 l16,210 h-212 Z" fill="{VINO}" {o(5)}/>')
    s += SL(0, koza(1480, 1000, 330, t, .3, True))
    kiv = 7 * A.w(t, 1.5, .2)
    s += SL(0, f'<g transform="rotate({kiv:.2f} 1600 760)"><circle cx="1600" cy="760"'
               f' r="4" fill="none"/></g>')
    s += SL(0, teplo(1500, 800, 380, 340, .24 + .08 * abs(A.w(t, 1.7))))
    s += SL(Z_SRED, f'<path d="M560,1046 q-30,-200 90,-206 l0,206 Z" fill="#4a3a52" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1700" y="620" width="14" height="420" fill="{CHUGUN}" {o(3)}/>'
                    f'<path d="M1640,620 h134 l-20,-86 h-94 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, lampa_stolika(1707, 600, t, 1.4))
    s += SL(Z_SRED, zerkalo(60, 300, 160, 500, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(400, 120, 1200, t, 10, 430, 44))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tualetnyy_stolik_s_melochami(t):
    """Трюмо с трёхстворчатым зеркалом: по очереди подсвечиваются коробочка с
    украшениями, туфли на пуфике и тёмное платье в отражении."""
    rnd = random.Random(4112)
    s = f'<rect width="{W}" height="{H}" fill="#221e26"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 431))
    s += SL(Z_DAL, stena("oboi", t, 109))
    s += SL(Z_SRED, trumo(320, 1050, 1200, 460, t))
    # ТРИ СТВОРКИ ТРЮМО НЕ ДОЛЖНЫ БЫТЬ ПУСТЫМИ (осмотр 16.11): в боковых
    # отражаются флаконы и край наряда, в средней — тёмное платье целиком.
    for i, (zx, zw, zh) in enumerate(((420, 300, 480), (760, 420, 560), (1220, 300, 480))):
        s += SL(Z_SRED, f'<rect x="{zx+12}" y="{680-zh+12}" width="{zw-24}"'
                        f' height="{zh-24}" fill="{STEKLO}" opacity=".24"/>')
        s += SL(Z_SRED, f'<g opacity=".5">'
                        + naryad_plechiki(zx + zw // 2, 700 - zh + 40, zh - 150, t,
                                          (LAVANDA, TSINIY, PUDRA)[i], .9, i * .3,
                                          True, None, .0, 460 + i) + "</g>")
        s += SL(Z_SRED, zerkalo(zx, 680 - zh, zw, zh, t, "pryam", ZOLOTO, True))
    hod = A.seg(t, .3, 4.4)
    akt = min(2, int(hod * 3))
    # коробочка с украшениями
    s += SL(0, korobka(420, 880, 260, t, 100, True, DEREVO2, MOLOKO))
    for i in range(8):
        s += SL(0, f'<circle cx="{450+i*26}" cy="820" r="12"'
                   f' fill="{(ZOLOTO, SEREBRO, KORALL, MOLOKO)[i%4]}"'
                   f' opacity="{(1.0 if akt == 0 else .5)*(.7+.3*abs(A.w(t,1.8,i*.2))):.2f}"/>')
    if akt == 0:
        s += SL(0, teplo(520, 840, 300, 220, .26))
    # туфли на пуфике
    s += SL(Z_SRED, f'<path d="M980,1046 q-40,-190 130,-196 q170,6 130,196 Z"'
                    f' fill="#45384f" {o(6)}/>')
    s += SL(0, tufli(1020, 870, 1.2, GRAFIT, t))
    if akt == 1:
        s += SL(0, teplo(1110, 880, 320, 230, .26))
    # тёмное платье на плечиках, отражается в центральной створке
    s += SL(0, naryad_plechiki(1620, 240, 520, t, TSINIY, 1.4, .2, True, None, .05, 432))
    if akt == 2:
        s += SL(Z_SRED, f'<g opacity=".55">'
                        + naryad_plechiki(900, 240, 380, t, TSINIY, 1.0, .4, True, None, .0, 433)
                        + "</g>")
        s += SL(Z_SRED, teplo(960, 420, 360, 320, .24))
    s += SL(Z_SRED, _flakony(560, 920, t, 5, 434))
    s += SL(Z_SRED, f'<path d="M820,930 h150 l0,22 h-150 Z" fill="{DEREVO2}" {o(3)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{828+i*12},952 l0,26" stroke="{DEREVO2}"'
                            f' stroke-width="3"/>' for i in range(12)))
    s += SL(Z_SRED, f'<ellipse cx="1360" cy="930" rx="56" ry="20" fill="{KREM2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1480,930 q-26,-90 36,-96 q62,6 36,96 Z"'
                    f' fill="url(#glina)" {o(4)}/>')
    for i in range(5):
        a = -80 + i * 32 + 4 * A.w(t, 2.4, i * .3)
        s += SL(Z_SRED, f'<path d="M1516,840 l{60*math.cos(math.radians(a)):.0f},'
                        f'{60*math.sin(math.radians(a)):.0f}" stroke="{HVOYA}"'
                        f' stroke-width="7"/>')
    s += SL(0, lampa_stolika(300, 640, t, 1.4))
    s += SL(0, lampa_stolika(1240, 640, t, 1.4))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tri_ukrasheniya_na_vybor(t):
    """Три бархатные подушечки: серьги, брошь, колье. Луч-прожектор ходит по
    ним и останавливается на одном — два других гаснут."""
    rnd = random.Random(4113)
    s = f'<rect width="{W}" height="{H}" fill="#1f1a22"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 435))
    s += SL(Z_DAL, stena("kraska", t, 110))
    s += SL(Z_DAL, elka(1850, 1050, 300, t, 1.0, True, 436))
    s += SL(Z_SRED, stol(120, 980, 1600, 48))
    hod = A.seg(t, .2, 3.6)
    akt = min(2, int(hod * 3))
    for i, x in enumerate((420, 940, 1460)):
        yar = 1.0 if i == akt else .30
        s += SL(Z_SRED, f'<path d="M{x-190},880 q190,-80 380,0 q-50,110 -190,116'
                        f' q-140,-6 -190,-116 Z" fill="{VINO}" opacity="{.5+.5*yar:.2f}" {o(6)}/>')
        s += SL(Z_SRED, skladki(x - 170, 840, 340, 130, VINO, 5, 437 + i, t, 2.0))
        if i == 0:
            for sgn in (-1, 1):
                sx = x + sgn * 70
                s += SL(0, f'<g opacity="{yar:.2f}">'
                           f'<path d="M{sx},830 l0,-60" stroke="{ZOLOTO}" stroke-width="8"/>'
                           f'<circle cx="{sx}" cy="760" r="26" fill="none" stroke="{ZOLOTO}"'
                           f' stroke-width="8"/>'
                           f'<path d="M{sx-28},840 l28,96 l28,-96 Z" fill="{ZOLOTO}" {o(3)}/></g>')
        elif i == 1:
            s += SL(0, f'<g opacity="{yar:.2f}"><circle cx="{x}" cy="860" r="52"'
                       f' fill="{ZOLOTO}" {o(4)}/>')
            for j in range(10):
                a = j * 36
                s += SL(0, f'<circle cx="{x+66*math.cos(math.radians(a)):.0f}"'
                           f' cy="{860+66*math.sin(math.radians(a)):.0f}" r="13"'
                           f' fill="{SEREBRO}" {o(2)}/>')
            s += SL(0, "</g>")
        else:
            s += SL(0, f'<g opacity="{yar:.2f}">' + "".join(
                f'<circle cx="{x-130+j*26}" cy="{870+int(26*math.sin(j*.6))}" r="14"'
                f' fill="{SEREBRO}" {o(2)}/>' for j in range(11)) + "</g>")
        if i == akt:
            lx = x
            s += SL(Z_SRED, f'<path d="M{lx},120 l-200,760 h400 Z" fill="{ZOLOTO}"'
                            f' opacity=".12"/>')
            s += SL(Z_SRED, teplo(x, 860, 420, 300, .28))
    s += SL(Z_SRED, zerkalo(120, 200, 300, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, _flakony(1560, 1000, t, 4, 441))
    s += SL(Z_SRED, svecha(1300, 980, t, .3, 1.4))
    s += SL(Z_SRED, f'<path d="M700,1000 q60,-30 110,-6 l-10,52 q-54,22 -104,-6 Z"'
                    f' fill="{MOLOKO}" {o(4)}/>')
    s += SL(Z_SRED, girlyanda(200, 120, 1500, t, 11, 442, 44))
    s += SL(0, lampa_stolika(960, 240, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def brosh_na_lackane(t):
    """Два манекена: к яркому алому платью — спокойные серьги, к простому
    бежевому жакету — крупная золотая брошь, которую рукав переносит выше."""
    rnd = random.Random(4114)
    s = f'<rect width="{W}" height="{H}" fill="#221d22"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 443))
    s += SL(Z_DAL, stena("paneli", t, 111))
    s += SL(Z_DAL, elka(1850, 1050, 300, t, 1.0, True, 444))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, manekken(520, 1010, 680, t, KREM2, "zh", ALYY, .1, None, .05, 445))
    s += SL(Z_SRED, f'<ellipse cx="520" cy="880" rx="70" ry="42" fill="{VINO}" {o(4)}/>')
    for sgn in (-1, 1):
        s += SL(Z_SRED, f'<circle cx="{520+sgn*26}" cy="{844-5*abs(A.w(t,1.8,sgn*.3)):.0f}"'
                        f' r="13" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(0, manekken(1280, 1010, 680, t, KREM2, "zh", BEZH, .5, None, .03, 446))
    per = A.out(A.seg(t, .8, 1.4))
    bx, by = 1200, 620 - 120 * per
    s += SL(0, f'<circle cx="{bx}" cy="{by:.0f}" r="42" fill="{ZOLOTO}" {o(4)}/>')
    for j in range(8):
        a = j * 45
        s += SL(0, f'<circle cx="{bx+56*math.cos(math.radians(a)):.0f}"'
                   f' cy="{by+56*math.sin(math.radians(a)):.0f}" r="12"'
                   f' fill="{ZOLOTO}" {o(2)}/>')
    ruk, _ = rukav(1620, 400, 260, 150 - 18 * per, t, VINO, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    # круглое зеркальце на ножке (кадр отсюда снят — остаётся рисованная брошь)
    s += SL(Z_SRED, f'<path d="{kontur_proema(820, 560, 380, 380, "ellips")}"'
                    f' fill="#2b2430" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="1010" cy="750" r="58" fill="{ZOLOTO}" opacity=".85"/>')
    s += SL(Z_SRED, zerkalo(820, 560, 380, 380, t, "ellips", ZOLOTO, True))
    s += SL(Z_SRED, f'<path d="M990,940 h40 l16,110 h-72 Z" fill="{DEREVO2}" {o(4)}/>')
    s += SL(Z_SRED, korobka(620, 1046, 220, t, 90, True, DEREVO2, MOLOKO))
    s += SL(Z_SRED, "".join(f'<path d="M{1480+i*22},1000 l6,-40" stroke="{SEREBRO}"'
                            f' stroke-width="3"/>' for i in range(6)))
    s += SL(Z_SRED, f'<path d="M1540,1010 q{20:.0f},90 {-10:.0f},36" fill="none"'
                    f' stroke="{MOLOKO}" stroke-width="10"/>')
    s += SL(Z_SRED, girlyanda(300, 120, 1300, t, 10, 447, 44))
    s += SL(0, lampa_stolika(1700, 900, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def mama_i_brosh(t):
    """Трюмо в спальне: мама прикалывает брошь-веточку у плеча, дочка смотрит
    с кровати не отрываясь."""
    rnd = random.Random(4115)
    s = f'<rect width="{W}" height="{H}" fill="#241f26"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 448))
    s += SL(Z_DAL, stena("paneli", t, 112))
    s += SL(Z_DAL, elka(1840, 1050, 340, t, 1.0, True, 449))
    s += SL(Z_SRED, trumo(120, 1050, 700, 420, t))
    s += SL(Z_SRED, zerkalo(240, 240, 460, 480, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="254" y="254" width="432" height="452" fill="{STEKLO}"'
                    f' opacity=".26"/>')
    s += SL(0, figura(760, 1050, 540, t, IZUMRUD, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    p = A.out(A.seg(t, .3, 1.3))
    for sgn in (-1, 1):
        ruk, _ = rukav(760 + sgn * 84, 760, 140, -70 - sgn * 20, t, IZUMRUD,
                       TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
    bx, by = 690, 700
    s += SL(0, f'<g opacity="{p:.2f}">'
               f'<path d="M{bx},{by+40} q20,-70 0,-120" fill="none" stroke="{ZOLOTO}"'
               f' stroke-width="7"/>')
    for j in range(5):
        s += SL(0, f'<ellipse cx="{bx+14-j*4}" cy="{by+10-j*24}" rx="16" ry="9"'
                   f' fill="{ZOLOTO}" transform="rotate({-30+j*14} {bx},{by})" {o(2)}/>')
    s += SL(0, "</g>")
    # дочка на кровати, руки подпирают щёки
    s += SL(Z_SRED, f'<rect x="1180" y="760" width="700" height="290" rx="18"'
                    f' fill="#4a3f4a" {o(6)}/>'
                    f'<rect x="1200" y="780" width="660" height="40" rx="14"'
                    f' fill="#5a4b5a" opacity=".7"/>')
    s += SL(0, figura(1400, 760, 330, t, KORALL, TEPLO_SVET, .6, False, False, 1.0,
                      1.5, True, True, "#f3d3b2", True, MOLOKO, False))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(1400 + sgn * 56, 620, 110, -96 - sgn * 18, t, KORALL,
                              TEPLO_SVET, .6, 3.0)
        s += SL(0, ruk)
    s += SL(Z_SRED, korobka(360, 940, 200, t, 80, True, DEREVO2, MOLOKO))
    s += SL(Z_SRED, _flakony(560, 940, t, 4, 450))
    s += SL(Z_SRED, f'<rect x="900" y="300" width="200" height="250" rx="8"'
                    f' fill="{MOLOKO}" {o(5)}/>'
                    f'<rect x="900" y="300" width="200" height="52" rx="8"'
                    f' fill="{KORALL}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1000" cy="450" r="{34+5*abs(A.w(t,1.6)):.0f}"'
                    f' fill="{ALYY}" opacity=".9"/>')
    s += SL(Z_SRED, girlyanda(1150, 140, 700, t, 8, 451, 44))
    s += SL(0, lampa_stolika(180, 940, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def klipsy_i_cheshskoe_steklo(t):
    """Коробочка на трюмо во весь кадр: клипсы, бусы из чешского стекла; от
    бус по стене бегут радужные зайчики."""
    rnd = random.Random(4116)
    s = f'<rect width="{W}" height="{H}" fill="#241f23"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 452))
    s += SL(Z_DAL, stena("paneli", t, 113))
    # радужные зайчики по стене
    for i in range(12):
        p = ((t * .6 + i * .18) % 1.0)
        zx = 120 + 1700 * p
        zy = 180 + 140 * math.sin(i * 1.3 + t)
        c = ("#ff6b6b", "#ffd36b", "#9bf0a8", "#8fd6ff", "#c79bff")[i % 5]
        s += SL(Z_DAL, f'<ellipse cx="{zx:.0f}" cy="{zy:.0f}" rx="40" ry="26"'
                       f' fill="{c}" opacity="{.25+.25*math.sin(p*math.pi):.2f}"/>')
    # НАСТОЯЩЕЕ стекло/бисер на стене (его слово 17.11) — метка перед рамой
    # (опора 14.11), окно в свободной верхней зоне, проём от нормы R-0024
    s += SL(Z_DAL, mesto_stoka(594, 154, 760, 392, "pryam"))
    s += SL(Z_DAL, zerkalo(580, 140, 788, 420, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="120" y="640" width="1680" height="420" rx="20"'
                    f' fill="{DEREVO}" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="150" y="670" width="1620" height="360" rx="14"'
                    f' fill="{VINO}" {o(5)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{200+i*540}" y="700" width="480" height="300" rx="10"'
                        f' fill="#4a0f20" {o(4)}/>')
    # клипсы
    for sgn in (-1, 1):
        cx = 440 + sgn * 90
        s += SL(0, f'<circle cx="{cx}" cy="850" r="46" fill="{ZOLOTO}"'
                   f' opacity="{.75+.25*abs(A.w(t,1.7,sgn*.3)):.2f}" {o(4)}/>'
                   f'<circle cx="{cx}" cy="850" r="20" fill="{MOLOKO}" {o(2)}/>')
    # бусы из гранёного стекла поднимаются к лампе и поворачиваются
    pod = A.out(A.seg(t, .3, 1.4))
    bx, by = 1000, 860 - 160 * pod
    ug = 40 * A.w(t, 1.6, .2)
    s += SL(0, f'<g transform="rotate({ug:.1f} {bx} {by:.0f})">')
    for i in range(14):
        a = i * 26
        s += SL(0, f'<path d="M{bx-150+i*22},{by+int(26*math.sin(i*.6))} l16,10 l-6,18'
                   f' l-18,2 l-8,-16 Z" fill="{STEKLO}"'
                   f' opacity="{.6+.4*abs(A.w(t,1.4,i*.2)):.2f}" {o(2)}/>')
    s += SL(0, "</g>")
    # колечко
    s += SL(0, f'<circle cx="1560" cy="850" r="38" fill="none" stroke="{ZOLOTO}"'
               f' stroke-width="12"/>')
    ruk, _ = rukav(1000, 320, 230, 86 - 24 * pod, t, LAVANDA, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    s += SL(Z_SRED, _flakony(260, 640, t, 4, 453))
    s += SL(Z_SRED, f'<path d="M1640,640 h150 l0,22 h-150 Z" fill="{DEREVO2}" {o(3)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{1648+i*12},662 l0,26" stroke="{DEREVO2}"'
                            f' stroke-width="3"/>' for i in range(12)))
    s += SL(0, lampa_stolika(1000, 240, t, 1.6))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tri_sharfa_na_spinke_stula(t):
    """Венский стул с тремя шарфами: шёлковый соскальзывает на сиденье,
    шерстяной лежит складкой, золотистый пускает блик. В овальном зеркале —
    настоящая шёлковая ткань."""
    rnd = random.Random(4117)
    s = f'<rect width="{W}" height="{H}" fill="#231e24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 454))
    s += SL(Z_DAL, stena("kraska", t, 114))
    px, py, pw, ph = 1360, 180, 420, 380
    put = kontur_proema(px, py, pw, ph, "ellips")
    s += SL(Z_DAL, f'<path d="{put}" fill="#2b2430"/>'
            + otrez(px + 50, py + 70, pw - 100, ph - 160, KORALL, t, 455, .4, .2)
            + mesto_stoka(px, py, pw, ph, "ellips")
            + zerkalo(px, py, pw, ph, t, "ellips", ZOLOTO, True))
    s += SL(Z_SRED, polovicy(1050))
    # венский стул
    s += SL(Z_SRED, f'<path d="M420,560 q220,-70 440,0 l0,40 q-220,-60 -440,0 Z"'
                    f' fill="{DEREVO}" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M440,600 q200,120 400,0 l0,60 q-200,120 -400,0 Z"'
                    f' fill="{DEREVO2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="400" y="760" width="480" height="34" rx="10"'
                    f' fill="{DEREVO}" {o(6)}/>')
    for sx in (430, 840):
        s += SL(Z_SRED, f'<rect x="{sx}" y="794" width="24" height="256"'
                        f' fill="{DEREVO}" {o(4)}/>')
    # три шарфа
    sol = A.out(A.seg(t, .4, 1.6))
    s += SL(0, f'<path d="M470,580 q60,{160+200*sol:.0f} {40+120*sol:.0f},{260+120*sol:.0f}'
               f' l80,20 q{-20-100*sol:.0f},{-120-120*sol:.0f} -40,-300 Z"'
               f' fill="{ALYY}" {o(5)}/>')
    s += SL(0, f'<path d="M620,580 q50,180 20,300 l84,16 q30,-140 -24,-316 Z"'
               f' fill="{VINO}" {o(5)}/>')
    s += SL(0, skladki(620, 600, 100, 280, VINO, 4, 456, t, 3.0))
    s += SL(0, f'<path d="M770,580 q46,170 16,290 l82,16 q28,-130 -22,-306 Z"'
               f' fill="{ZOLOTO}" {o(5)}/>')
    s += SL(0, tkan_blesk(760, 580, 120, 300, t, "#ffffff", .5, .3))
    s += SL(Z_SRED, naryad_plechiki(1120, 260, 460, t, TSINIY, 1.2, .3, True, None, .04, 457))
    s += SL(Z_SRED, kot(300, 1046, t, 1.4, "#6b5a46"))
    s += SL(Z_SRED, tufli(1000, 1046, 1.0, GRAFIT, t))
    s += SL(Z_SRED, f'<path d="M1640,1046 q-20,-130 58,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_DAL, elka(120, 1050, 320, t, 1.0, True, 458))
    s += SL(Z_SRED, girlyanda(380, 120, 1200, t, 10, 459, 44))
    s += SL(0, lampa_stolika(1180, 860, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def sharf_u_shei_i_poverh_zhaketa(t):
    """Женщина у зеркала: сначала завязывает винный шарф узлом у шеи, потом
    накидывает его поверх жакета и расправляет конец."""
    rnd = random.Random(4118)
    s = f'<rect width="{W}" height="{H}" fill="#221e23"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 460))
    s += SL(Z_DAL, stena("paneli", t, 115))
    s += SL(Z_DAL, elka(1840, 1050, 320, t, 1.0, True, 461))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, zerkalo(180, 160, 620, 800, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="196" y="176" width="588" height="768" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    faza = A.seg(t, .3, 2.6)
    u_shei = faza < .55
    s += SL(Z_SRED, f'<g opacity=".45">'
                    + figura(480, 920, 430, t, KREM2, TEPLO_SVET, .2, False, False, .6,
                             1.5, True, False, "#f0cfae", True, None, False) + "</g>")
    s += SL(0, figura(1180, 1050, 560, t, KREM2, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, None, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(1180 + sgn * 100, 780, 150, -78 - sgn * 16, t, KREM2,
                       TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    if u_shei:
        s += SL(0, f'<path d="M1120,700 q60,30 120,0 l-10,60 l-100,0 Z" fill="{VINO}" {o(4)}/>'
                   f'<path d="M1160,760 l20,120 M1200,760 l-10,120" stroke="{VINO}"'
                   f' stroke-width="22" stroke-linecap="round"/>')
    else:
        rasp = A.out(A.seg(t, 1.5, 1.0))
        s += SL(0, f'<path d="M1060,700 q120,40 240,0 l14,80 q-134,44 -268,0 Z"'
                   f' fill="{VINO}" {o(5)}/>')
        s += SL(0, f'<path d="M1300,760 q30,{80+60*rasp:.0f} -10,{160+80*rasp:.0f}"'
                   f' fill="none" stroke="{VINO}" stroke-width="30" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M900,1046 q-24,-150 66,-154 l0,154 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1520" y="260" width="320" height="18" rx="8"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    s += SL(Z_SRED, naryad_plechiki(1640, 280, 400, t, TSINIY, 1.0, .4, True, None, .04, 462))
    s += SL(Z_SRED, f'<path d="M820,900 q40,-14 62,16 l12,86 h-92 Z" fill="{GRAFIT}" {o(4)}/>')
    s += SL(Z_SRED, girlyanda(200, 120, 1500, t, 10, 463, 44))
    s += SL(0, lampa_stolika(960, 820, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def obuvnaya_polka_k_prazdniku(t):
    """Обувная полка: лодочки и туфли с блеском в центре, стоптанные тапки и
    резиновые сапоги отъезжают в тень."""
    rnd = random.Random(4119)
    s = f'<rect width="{W}" height="{H}" fill="#201b19"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 464))
    s += SL(Z_DAL, stena("doski", t, 116))
    s += SL(Z_SRED, f'<rect x="120" y="360" width="1680" height="620" rx="14"'
                    f' fill="#2a2420" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="140" y="{420+i*200}" width="1640" height="26" rx="8"'
                        f' fill="{DEREVO}" {o(4)}/>')
    s += SL(0, tufli(700, 420, 1.5, GRAFIT, t))
    s += SL(0, tufli(1060, 420, 1.5, SEREBRO, t))
    s += SL(0, tkan_blesk(1040, 340, 220, 90, t, "#ffffff", .55, .2))
    kach = 5 * A.w(t, 2.0, .2)
    s += SL(0, f'<g transform="rotate({kach:.2f} 1420 400)">'
               f'<path d="M1340,400 q80,-44 160,0 l20,120 q-100,34 -200,0 Z"'
               f' fill="{GRAFIT}" {o(5)}/>'
               f'<path d="M1370,392 q70,-120 140,-4" fill="none" stroke="{SEREBRO}"'
               f' stroke-width="7"/></g>')
    ot = A.out(A.seg(t, .4, 1.5))
    s += SL(Z_SRED, f'<g opacity="{1-.65*ot:.2f}" transform="translate({-240*ot:.0f},0)">'
                    f'<path d="M300,620 q34,-38 70,0 q-34,22 -70,0 Z" fill="{KORALL}" {o(3)}/>'
                    f'<path d="M400,620 q34,-38 70,0 q-34,22 -70,0 Z" fill="{KORALL}" {o(3)}/>'
                    f'</g>')
    s += SL(Z_SRED, f'<g opacity="{1-.65*ot:.2f}" transform="translate({260*ot:.0f},0)">'
                    f'<path d="M1560,820 q20,-190 70,-192 q50,2 70,192 Z" fill="#2a3a2a" {o(5)}/>'
                    f'<path d="M1690,820 q20,-190 70,-192 q50,2 70,192 Z" fill="#2a3a2a" {o(5)}/>'
                    f'</g>')
    s += SL(Z_SRED, f'<path d="M560,820 l120,-16 l6,26 l-120,16 Z" fill="{DEREVO2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M820,830 q70,-36 130,-6 l-12,52 q-62,26 -118,-6 Z"'
                    f' fill="{DEREVO2}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="1000" width="420" height="50" rx="10"'
                    f' fill="#5a4038" {o(4)}/>')
    # В ЗЕРКАЛЕ ОБУВНОЙ ПРИХОЖЕЙ ОТРАЖАЕТСЯ РЯД ОБУВИ, А НЕ ПУСТОТА.
    s += SL(Z_SRED, f'<rect x="1492" y="452" width="256" height="436" fill="{STEKLO}"'
                    f' opacity=".22"/>')
    s += SL(Z_SRED, f'<g opacity=".55">' + tufli(1540, 740, 1.1, GRAFIT, t)
                    + tufli(1540, 860, 1.1, SEREBRO, t) + "</g>")
    s += SL(Z_SRED, zerkalo(1480, 440, 280, 460, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(160, 240, 1600, t, 11, 465, 44))
    s += SL(0, lampa_stolika(960, 300, t, 1.4))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def novye_tufli_poverh_noskov(t):
    """Женщина разнашивает новые блестящие туфли поверх толстых шерстяных
    носков: три вечера до праздника отмечены на календаре."""
    rnd = random.Random(4120)
    s = f'<rect width="{W}" height="{H}" fill="#241f22"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 466))
    s += SL(Z_DAL, stena("oboi", t, 117))
    s += SL(Z_DAL, elka(1820, 1050, 420, t, 1.0, True, 467))
    s += SL(Z_SRED, polovicy(1050))
    hod = A.seg(t, .2, 3.2)
    fx = 420 + 760 * hod
    s += SL(0, figura(fx, 1040, 540, t, "#7a6a58", TEPLO_SVET, .2, False, False, 1.0,
                      2.5, True, True, "#f0cfae", True, MOLOKO, False))
    for sgn in (-1, 1):
        s += SL(0, f'<path d="M{fx+sgn*40-30:.0f},980 h60 l6,40 h-72 Z"'
                   f' fill="{BEZH}" {o(4)}/>')
    s += SL(0, tufli(fx - 70, 1040, 1.0, SEREBRO, t))
    ruk, (hx, hy) = rukav(fx + 80, 770, 150, -38, t, "#7a6a58", TEPLO_SVET, .2, 4.0)
    s += SL(0, ruk)
    s += SL(0, f'<path d="M{hx-36:.0f},{hy-10:.0f} q-10,-56 36,-58 q46,2 36,58 Z"'
               f' fill="{KREM2}" {o(4)}/>')
    s += SL(0, par(hx, hy - 70, t, 3, .45, 110, .4, .8))
    ruk2, _ = rukav(fx - 80, 790, 160, 36, t, "#7a6a58", TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    # календарь: три вечера отмечены
    s += SL(Z_SRED, f'<rect x="1360" y="200" width="380" height="420" rx="12"'
                    f' fill="{MOLOKO}" {o(6)}/>'
                    f'<rect x="1360" y="200" width="380" height="70" rx="12"'
                    f' fill="{KORALL}" {o(3)}/>')
    for i in range(12):
        cx = 1400 + (i % 4) * 96
        cy = 320 + (i // 4) * 96
        s += SL(Z_SRED, f'<rect x="{cx}" y="{cy}" width="70" height="70" rx="8"'
                        f' fill="{KREM2}" {o(2)}/>')
        if i >= 9:
            q = A.out(A.seg(t, .5 + (i - 9) * .5, .5))
            s += SL(Z_SRED, f'<path d="M{cx+12},{cy+34} l20,24 l34,-44" fill="none"'
                            f' stroke="{ALYY}" stroke-width="10" opacity="{q:.2f}"'
                            f' stroke-linecap="round"/>')
    s += SL(Z_SRED, korobka(260, 1046, 300, t, 120, True, "#b8a289", MOLOKO))
    s += SL(Z_SRED, f'<rect x="760" y="700" width="420" height="300" rx="14"'
                    f' fill="#1b1b22" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="790" y="730" width="360" height="230" rx="8"'
                    f' fill="#2b3a4a" opacity="{.5+.3*abs(A.w(t,1.5)):.2f}"/>')
    s += SL(Z_SRED, f'<path d="M1240,1046 q-30,-200 90,-206 l0,206 Z" fill="#4a3a52" {o(5)}/>')
    kx = fx - 180
    s += SL(Z_SRED, kot(kx, 1046, t, 1.3, "#3b3430"))
    s += SL(Z_SRED, girlyanda(200, 120, 1100, t, 9, 468, 44))
    s += SL(0, lampa_stolika(1640, 820, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tufli_v_korobke_s_bumagoy(t):
    """С верхней полки снимают обувную коробку: в папиросной бумаге лаковые
    туфли, в каждую вложен комок газеты, чтобы держали форму."""
    rnd = random.Random(4121)
    s = f'<rect width="{W}" height="{H}" fill="#221d1b"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 469))
    s += SL(Z_DAL, stena("kraska", t, 118))
    s += SL(Z_DAL, shkaf(760, 1050, 1060, 980, t, 1.0, False))
    s += SL(Z_SRED, polka(840, 420, 900))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, korobka(1480, 420, 260, t, 110, False, "#b8a289", MOLOKO))
    s += SL(Z_SRED, f'<path d="M1240,420 q80,-30 160,0 l0,-90 q-80,-26 -160,0 Z"'
                    f' fill="{LAVANDA}" {o(4)}/>')
    snyat = A.out(A.seg(t, .3, 1.4))
    kx, ky = 1000, 440 + 300 * snyat
    kr = A.out(A.seg(t, 1.2, 1.0))
    s += SL(0, f'<rect x="{kx-200:.0f}" y="{ky:.0f}" width="400" height="190" rx="12"'
               f' fill="#b8a289" {o(6)}/>')
    s += SL(0, f'<g transform="rotate({-24*kr:.0f} {kx-200:.0f} {ky:.0f})">'
               f'<rect x="{kx-200:.0f}" y="{ky-44:.0f}" width="400" height="44" rx="10"'
               f' fill="#a8926f" {o(4)}/></g>')
    if kr > .2:
        s += SL(0, f'<path d="M{kx-170:.0f},{ky+40:.0f} q90,-50 180,-10 q80,40 160,-6"'
                   f' fill="none" stroke="{MOLOKO}" stroke-width="26" opacity="{kr:.2f}"/>')
        for i in range(2):
            tx = kx - 120 + i * 190
            s += SL(0, f'<g opacity="{kr:.2f}">'
                       f'<path d="M{tx},{ky+150:.0f} q16,-86 92,-88 q76,2 92,88 Z"'
                       f' fill="#1f1a18" {o(5)}/>'
                       f'<path d="M{tx+30},{ky+86:.0f} q46,-30 90,-6" fill="none"'
                       f' stroke="#ffffff" stroke-width="7" opacity=".55"/>'
                       f'<ellipse cx="{tx+80}" cy="{ky+96:.0f}" rx="34" ry="20"'
                       f' fill="{KREM2}" opacity=".8"/></g>')
    s += SL(0, figura(400, 1050, 520, t, "#7a6a58", TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#eec9a6", True, MOLOKO, False))
    for sgn in (-1, 1):
        ruk, _ = rukav(400 + sgn * 84, 740, 230, -36 - sgn * 10, t, "#7a6a58",
                       TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    s += SL(Z_SRED, f'<rect x="300" y="1000" width="220" height="50" rx="8"'
                    f' fill="{DEREVO}" {o(5)}/>')
    sh = ""
    for i, c in enumerate((KORALL, IZUMRUD, ZOLOTO)):
        sh += (f'<path d="M{1320+i*120},860 q{14+6*A.w(t,2.4,i*.3):.0f},-80 34,-110"'
               f' fill="none" stroke="{c}" stroke-width="20" stroke-linecap="round"/>')
    s += SL(Z_SRED, sh)
    s += SL(Z_SRED, girlyanda(840, 130, 1000, t, 9, 470, 44))
    s += SL(0, lampa_stolika(1700, 900, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def semeynaya_fotografiya_v_polnyy_ros(t):
    """Семья выстроилась у ёлки для снимка: камера идёт вниз к ногам, клетчатые
    тапочки зятя подсвечиваются красным, он убегает и возвращается в ботинках."""
    rnd = random.Random(4122)
    s = f'<rect width="{W}" height="{H}" fill="#241c20"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 471))
    s += SL(Z_DAL, stena("oboi", t, 119))
    s += SL(Z_DAL, elka(1700, 1050, 560, t, 1.0, True, 472))
    s += SL(Z_SRED, f'<rect x="120" y="980" width="1500" height="70" rx="14"'
                    f' fill="#5a3a3a" {o(5)}/>')
    s += SL(Z_SRED, polovicy(1050))
    ubeg = A.seg(t, .5, 2.2)
    LYUDI = ((420, TSINIY, True, "#f0cfae"), (640, GRAFIT, False, "#eec9a6"),
             (860, VINO, True, "#f0cfae"), (1120, MOLOKO, False, "#f3d3b2"))
    for i, (fx, c, zhen, koja) in enumerate(LYUDI):
        dx = 0
        if i == 3:
            dx = 900 * math.sin(min(1.0, ubeg) * math.pi)
        s += SL(0, figura(fx + dx, 1040, 520 - i * 12, t, c, TEPLO_SVET, i * .2, False,
                          False, 1.0, 1.5, True, True, koja, zhen, MOLOKO, True))
    # бабушка держит деда под руку
    ruk, _ = rukav(470, 790, 150, -6, t, TSINIY, TEPLO_SVET, .2, 3.0)
    s += SL(0, ruk)
    # тапочки зятя подсвечиваются красным
    if ubeg < .25 or ubeg > .9:
        tx = 1120 + (900 * math.sin(min(1.0, ubeg) * math.pi))
        if ubeg < .25:
            s += SL(0, f'<path d="M{tx-60:.0f},1040 q30,-34 62,0 q-30,20 -62,0 Z"'
                       f' fill="{KORALL}" {o(3)}/>'
                       f'<path d="M{tx+10:.0f},1040 q30,-34 62,0 q-30,20 -62,0 Z"'
                       f' fill="{KORALL}" {o(3)}/>')
            s += SL(0, teplo(tx, 1030, 220, 90, .30 + .14 * abs(A.w(t, 1.2))))
        else:
            s += SL(0, f'<path d="M{tx-60:.0f},1040 q16,-56 62,-58 q46,2 62,58 Z"'
                       f' fill="#2b2420" {o(4)}/>')
    # фотоаппарат на штативе, автоспуск мигает, вспышка
    s += SL(Z_SRED, f'<path d="M1500,1050 l80,-300 M1660,1050 l-80,-300"'
                    f' stroke="{CHUGUN}" stroke-width="14"/>')
    s += SL(Z_SRED, f'<rect x="1500" y="640" width="170" height="110" rx="12"'
                    f' fill="#2a2a30" {o(5)}/>'
                    f'<circle cx="1585" cy="695" r="36" fill="#1b1b22" {o(3)}/>'
                    f'<circle cx="1585" cy="695" r="18" fill="{STEKLO}" opacity=".6"/>')
    mig = 1.0 if (t % .8) < .4 else .25
    s += SL(Z_SRED, f'<circle cx="1640" cy="660" r="12" fill="{ALYY}" opacity="{mig:.2f}"/>')
    vsp = 1.0 if (t % 3.4) > 3.2 else .0
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"'
                    f' opacity="{vsp*.3:.2f}"/>')
    s += SL(Z_SRED, girlyanda(140, 120, 1300, t, 10, 473, 44))
    s += SL(0, lampa_stolika(200, 900, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def babushka_na_pleche_i_koshelek_na_n(t):
    """Два голоса на плечах: маленькая бабушка грозит чёрному платью, кошелёк
    на ножках мотает застёжкой. Женщина сводит руки — оба кивают."""
    rnd = random.Random(4124)
    s = f'<rect width="{W}" height="{H}" fill="#221d24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 474))
    s += SL(Z_DAL, stena("oboi", t, 120))
    s += SL(Z_DAL, shkaf(1360, 1050, 520, 900, t, .8, True))
    s += SL(Z_DAL, elka(160, 1050, 400, t, 1.0, True, 475))
    s += SL(Z_SRED, polovicy(1050))
    svod = A.out(A.seg(t, .8, 1.4))
    s += SL(0, figura(900, 1050, 600, t, GRAFIT, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(900 + sgn * 110, 770, 220, (30 - 54 * svod) * sgn, t, GRAFIT,
                       TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    # бабушка на левом плече
    bx, by = 760, 700
    kiv = 8 * A.w(t, 1.6, .1) * (1 if svod < .7 else .4)
    s += SL(0, f'<g transform="rotate({kiv:.2f} {bx} {by})">'
               f'<path d="M{bx-50},{by} q50,-100 100,0 Z" fill="{TSINIY}" {o(4)}/>'
               f'<circle cx="{bx}" cy="{by-110}" r="46" fill="#f0cfae" {o(3)}/>'
               f'<path d="M{bx-50},{by-120} q50,-70 100,0 q-16,-40 -50,-42'
               f' q-34,2 -50,42 Z" fill="{KORALL}" {o(3)}/>')
    groz = 20 * A.w(t, 1.1, .2)
    s += SL(0, f'<path d="M{bx+40},{by-60} l{60+groz:.0f},-50" stroke="{TSINIY}"'
               f' stroke-width="20" stroke-linecap="round"/></g>')
    # кошелёк на ножках на правом плече
    kx, ky = 1040, 700
    mot = 16 * A.w(t, 1.3, .4)
    s += SL(0, f'<g transform="rotate({mot*.3:.2f} {kx} {ky})">'
               f'<rect x="{kx-70}" y="{ky-110}" width="140" height="110" rx="16"'
               f' fill="{DEREVO2}" {o(5)}/>'
               f'<path d="M{kx-70},{ky-70} h140" stroke="{ZOLOTO}" stroke-width="9"/>'
               f'<path d="M{kx-30},{ky-110} q30,{-30-mot:.0f} 60,0" fill="none"'
               f' stroke="{ZOLOTO}" stroke-width="8"/>'
               f'<path d="M{kx-40},{ky} l-10,60 M{kx+40},{ky} l10,60" stroke="{DEREVO2}"'
               f' stroke-width="12" stroke-linecap="round"/></g>')
    # чёрное платье в шкафу, на которое грозят
    s += SL(Z_SRED, naryad_plechiki(1600, 300, 440, t, GRAFIT, 1.1, .3, True, None, .04, 476))
    s += SL(Z_SRED, zerkalo(80, 300, 190, 540, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<path d="M560,1046 q-24,-150 66,-154 l0,154 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(340, 120, 1300, t, 10, 477, 44))
    s += SL(0, lampa_stolika(1700, 880, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def chernoe_plate_i_krasnaya_detal(t):
    """Чёрное платье на манекене оживает: золотые украшения и одна красная
    вещь, которая сменяет сама себя — пояс, туфли, шарф, помада."""
    rnd = random.Random(4125)
    s = f'<rect width="{W}" height="{H}" fill="#1e1a20"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 478))
    s += SL(Z_DAL, stena("oboi", t, 121))
    s += SL(Z_DAL, elka(1840, 1050, 330, t, 1.0, True, 479))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, manekken(880, 1010, 760, t, KREM2, "zh", "#1b1820", .2, None, .03, 480))
    zol = A.out(A.seg(t, .3, .8))
    s += SL(0, f'<g opacity="{zol:.2f}">'
               f'<circle cx="810" cy="520" r="18" fill="{ZOLOTO}" {o(2)}/>'
               f'<circle cx="950" cy="520" r="18" fill="{ZOLOTO}" {o(2)}/>'
               f'<circle cx="980" cy="600" r="30" fill="{ZOLOTO}" {o(3)}/></g>')
    etap = int(A.seg(t, .6, 4.0) * 4) % 4
    if etap == 0:
        s += SL(0, f'<path d="M740,700 q140,40 280,0 l0,40 q-140,44 -280,0 Z"'
                   f' fill="{ALYY}" {o(4)}/>')
    elif etap == 1:
        s += SL(0, tufli(1140, 1046, 1.3, ALYY, t))
    elif etap == 2:
        s += SL(0, f'<path d="M740,470 q140,50 280,0 l14,70 q-154,54 -308,0 Z"'
                   f' fill="{ALYY}" {o(4)}/>')
    else:
        s += SL(0, f'<rect x="1320" y="880" width="40" height="120" rx="10"'
                   f' fill="{ALYY}" {o(3)}/>'
                   f'<rect x="1326" y="846" width="28" height="40" rx="8"'
                   f' fill="{SEREBRO}" {o(2)}/>')
    s += SL(Z_SRED, trumo(1180, 1046, 420, 300, t))
    s += SL(Z_SRED, svecha(1480, 900, t, .3, 1.4))
    s += SL(Z_SRED, f'<path d="M520,1046 q-24,-150 66,-154 l0,154 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(60, 300, 190, 540, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(300, 120, 1300, t, 10, 481, 44))
    s += SL(0, lampa_stolika(1620, 820, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def chernoe_plate_i_krasnye_tufli(t):
    """Паркет у зеркала: подол чёрного платья и красные туфли берутся за
    ленточки-руки и кружатся парой."""
    rnd = random.Random(4126)
    s = f'<rect width="{W}" height="{H}" fill="#201b1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 482))
    s += SL(Z_DAL, doski(0, 0, W, 620, 86))
    s += SL(Z_SRED, polovicy(700))
    par_ = "".join(f'<path d="M{60+i*118},700 l0,380" stroke="#5a3d26"'
                   f' stroke-width="3" opacity=".5"/>' for i in range(16))
    s += SL(Z_SRED, par_)
    s += SL(Z_SRED, f'<rect x="120" y="140" width="560" height="700" rx="10"'
                    f' fill="#2a2420" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="136" y="156" width="528" height="668" fill="{STEKLO}"'
                    f' opacity=".22"/>')
    # НАСТОЯЩИЙ КАДР ОТСЮДА СНЯТ: рисуем отражение сами, иначе остаётся дыра.
    s += SL(Z_SRED, f'<g opacity=".7">'
                    + f'<path d="M200,170 q180,46 360,0 l0,300 q-180,50 -360,0 Z"'
                      f' fill="#1b1820" {o(4)}/>'
                    + tufli(260, 760, 1.9, ALYY, t) + "</g>")
    s += SL(Z_SRED, zerkalo(120, 140, 560, 700, t, "pryam", ZOLOTO, True))
    # подол платья и ноги манекена
    s += SL(0, f'<path d="M980,140 q180,{40+12*A.w(t,2.0):.0f} 360,0 l40,520'
               f' q-220,{50+14*A.w(t,2.0,.3):.0f} -440,0 Z" fill="#1b1820" {o(6)}/>')
    s += SL(0, f'<path d="M1120,660 q40,-14 80,0 l10,200 h-100 Z" fill="#d8b89c" {o(4)}/>')
    s += SL(0, f'<ellipse cx="1160" cy="880" rx="120" ry="26" fill="{SEREBRO}" {o(4)}/>')
    # пара кружится: платье и туфли на ленточках
    kr = A.seg(t, .3, 3.0)
    a = 360 * kr
    cx2, cy2 = 1560, 820
    s += SL(0, f'<g transform="rotate({a:.1f} {cx2} {cy2})">'
               f'<path d="M{cx2-120},{cy2} q60,-120 120,-10 l10,120 h-140 Z"'
               f' fill="#1b1820" {o(5)}/>'
               f'<path d="M{cx2+60},{cy2-20} q16,-70 80,-72 q64,2 80,72 Z"'
               f' fill="{ALYY}" {o(5)}/>'
               f'<path d="M{cx2-40},{cy2-40} q80,-30 150,-10" fill="none" stroke="{KORALL}"'
               f' stroke-width="9"/></g>')
    s += SL(Z_SRED, korobka(800, 1046, 260, t, 110, True, BEZH, MOLOKO))
    s += SL(Z_SRED, f'<path d="M1800,1046 q-20,-130 58,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="1000" width="320" height="46" rx="8"'
                    f' fill="#5a4038" {o(4)}/>')
    blik_hod = (A.w(t, 4.2, .2) + 1) / 2
    s += SL(Z_SRED, f'<path d="M{200+1300*blik_hod:.0f},700 l140,380 l-90,0 l-140,-380 Z"'
                    f' fill="#ffffff" opacity=".10"/>')
    s += SL(Z_SRED, girlyanda(700, 120, 1100, t, 9, 483, 44))
    s += SL(0, lampa_stolika(900, 560, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def seryy_zhaket_i_tri_sputnika(t):
    """Серый жакет и три его спутника: винная блузка, розовый шарф, золотая
    брошь — каждый приходит по словам."""
    rnd = random.Random(4127)
    s = f'<rect width="{W}" height="{H}" fill="#201e22"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 484))
    s += SL(Z_DAL, stena("paneli", t, 123))
    s += SL(Z_DAL, elka(1840, 1050, 320, t, 1.0, True, 485))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, manekken(880, 1010, 760, t, KREM2, "zh", SERYY, .2, None, .04, 486))
    p1 = A.out(A.seg(t, .4, .7))
    s += SL(0, f'<path d="M800,480 h160 l10,170 h-180 Z" fill="{VINO}"'
               f' opacity="{p1:.2f}" {o(4)}/>')
    p2 = A.out(A.seg(t, 1.3, .9))
    s += SL(0, f'<path d="M740,460 q140,{40*p2:.0f} 280,0 l14,{60*p2:.0f}'
               f' q-154,{44*p2:.0f} -308,0 Z" fill="{PUDRA}" opacity="{p2:.2f}" {o(4)}/>')
    p3 = A.out(A.seg(t, 2.2, .7))
    s += SL(0, f'<circle cx="790" cy="560" r="{30*p3:.0f}" fill="{ZOLOTO}"'
               f' opacity="{p3:.2f}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="880" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="310" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="442" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M1420,1046 q-30,-150 70,-154 q100,4 70,154 Z"'
                    f' fill="url(#solom)" {o(5)}/>')
    sh = ""
    for i, c in enumerate((KORALL, PUDRA, ZOLOTO)):
        sh += (f'<path d="M{1450+i*40},900 q{14+6*A.w(t,2.4,i*.3):.0f},-80 32,-108"'
               f' fill="none" stroke="{c}" stroke-width="18" stroke-linecap="round"/>')
    s += SL(Z_SRED, sh)
    kx = 500 + 300 * A.seg(t, .4, 3.0)
    s += SL(Z_SRED, kot(kx, 1046, t, 1.3, SERYY))
    s += SL(Z_SRED, zerkalo(80, 300, 190, 540, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(320, 120, 1300, t, 10, 487, 44))
    s += SL(0, lampa_stolika(1700, 820, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def temno_sinee_s_izumrudom_i_zolotom(t):
    """Два манекена: на тёмно-синее платье ложится изумрудный шарф, к тёмно-
    синему жакету рукав пришивает золотистые пуговицы."""
    rnd = random.Random(4128)
    s = f'<rect width="{W}" height="{H}" fill="#1d1c24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 488))
    s += SL(Z_DAL, stena("doski", t, 124))
    s += SL(Z_DAL, elka(1850, 1050, 300, t, 1.0, True, 489))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, manekken(520, 1010, 680, t, KREM2, "zh", TSINIY, .1, None, .04, 490))
    p = A.out(A.seg(t, .3, 1.2))
    s += SL(0, f'<path d="M390,{470-60*(1-p):.0f} q130,40 260,0 l12,66'
               f' q-142,46 -284,0 Z" fill="{IZUMRUD}" opacity="{p:.2f}" {o(5)}/>')
    s += SL(0, manekken(1280, 1010, 680, t, KREM2, "m", TSINIY, .5, None, .04, 491))
    hod = A.seg(t, .6, 2.6)
    for i in range(4):
        q = max(0.0, min(1.0, hod * 4 - i))
        s += SL(0, f'<circle cx="1280" cy="{540+i*70}" r="18" fill="{ZOLOTO}"'
                   f' opacity="{q:.2f}" {o(3)}/>')
    igla = 1280 + 60 * A.w(t, 1.2, .2)
    s += SL(0, f'<path d="M{igla:.0f},{520+70*min(3,int(hod*4)):.0f} l50,-34"'
               f' stroke="{SEREBRO}" stroke-width="6" stroke-linecap="round"/>')
    ruk, _ = rukav(1620, 420, 240, 150, t, VINO, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    s += SL(Z_SRED, korobka(820, 1046, 240, t, 100, True, DEREVO2, MOLOKO))
    s += SL(Z_SRED, "".join(f'<circle cx="{850+i*34}" cy="990" r="13" fill="{ZOLOTO}"'
                            f' opacity="{.6+.4*abs(A.w(t,1.8,i*.2)):.2f}" {o(2)}/>'
                            for i in range(5)))
    s += SL(Z_SRED, f'<ellipse cx="1080" cy="1000" rx="60" ry="46" fill="{KORALL}" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{1040+i*20},978 l6,-30" stroke="{SEREBRO}"'
                            f' stroke-width="3"/>' for i in range(5)))
    s += SL(Z_SRED, zerkalo(80, 300, 180, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(320, 120, 1300, t, 10, 492, 44))
    s += SL(0, lampa_stolika(1700, 860, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def primeta_pro_obnovku(t):
    """Обновку вешают в шкаф, и рядом сами собой появляются прозрачные наряды
    будущего года. В проёме шкафа — настоящая вешалка с одеждой."""
    rnd = random.Random(4129)
    s = f'<rect width="{W}" height="{H}" fill="#201c22"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 493))
    s += SL(Z_DAL, stena("oboi", t, 125))
    px, py, pw, ph = 120, 320, 780, 320
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#241f22"/>'
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-16}" y="{py-16}" width="{pw+32}" height="{ph+32}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="24"/>')
    s += SL(Z_DAL, shkaf(980, 1050, 820, 900, t, .9, False))
    s += SL(Z_SRED, perekladina(1380, 300, 700))
    s += SL(Z_SRED, polovicy(1050))
    ves = A.out(A.seg(t, .3, 1.3))
    s += SL(0, naryad_plechiki(1120, 320 + 60 * (1 - ves), 420, t, KORALL, 1.15, .1,
                               True, None, .05, 494))
    s += SL(0, birka(1180, 420, 1.1, t, MOLOKO, .2))
    for i in range(3):
        q = A.out(A.seg(t, .9 + i * .5, .7))
        s += SL(Z_SRED, f'<g opacity="{q*.5:.2f}">'
                        + naryad_plechiki(1380 + i * 160, 320, 400, t,
                                          (LAVANDA, MOLOKO, IZUMRUD)[i], 1.0,
                                          i * .3, True, None, .0, 495 + i) + "</g>")
    s += SL(0, figura(660, 1050, 540, t, GRAFIT, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, _ = rukav(760, 740, 270, -34 + 14 * ves, t, GRAFIT, TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(580, 780, 180, 170, t, GRAFIT, TEPLO_SVET, .5, 5.0)
    s += SL(0, ruk2)
    s += SL(0, koza(1740, 1020, 300, t, .4, True))
    s += SL(0, teplo(1740, 840, 340, 300, .22 + .08 * abs(A.w(t, 1.7))))
    s += SL(Z_SRED, f'<path d="M880,1046 q-24,-150 66,-154 l0,154 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_DAL, elka(60, 1050, 300, t, 1.0, True, 498))
    s += SL(Z_SRED, girlyanda(940, 130, 900, t, 9, 499, 44))
    s += SL(0, lampa_stolika(960, 900, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def novaya_meloch_vmesto_platya(t):
    """Большая коробка с платьем и длинный чек отодвигаются, а из маленького
    свёртка появляются новый шарф и брошь на картонке."""
    rnd = random.Random(4130)
    s = f'<rect width="{W}" height="{H}" fill="#241f1c"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 500))
    s += SL(Z_DAL, doski(0, 0, W, 520, 84))
    # НАСТОЯЩИЙ шёлковый шарф на стене (его слово 17.11) — метка перед
    # рамой (опора 14.11), окно в свободной верхней зоне, проём от нормы R-0024
    s += SL(Z_DAL, mesto_stoka(664, 154, 760, 352, "pryam"))
    s += SL(Z_DAL, zerkalo(650, 140, 788, 380, t, "pryam", ZOLOTO, True))
    s += SL(Z_DAL, elka(1840, 1050, 300, t, 1.0, True, 501))
    s += SL(Z_SRED, stol(80, 1010, 1760, 48))
    ot = A.out(A.seg(t, .3, 1.4))
    s += SL(0, f'<g transform="translate({-360*ot:.0f},0)" opacity="{1-.5*ot:.2f}">'
               + korobka(260, 940, 420, t, 180, False, "#b8a289", MOLOKO)
               + f'<path d="M300,760 h120 l0,-300 h-120 Z" fill="{MOLOKO}" {o(4)}/>')
    for i in range(9):
        s += SL(0, f'<path d="M312,{480+i*30} h96" stroke="{K}" stroke-width="3"'
                   f' opacity=".45"/>')
    s += SL(0, "</g>")
    # маленький свёрток: шарф и брошь
    p1 = A.out(A.seg(t, .8, 1.0))
    p2 = A.out(A.seg(t, 1.6, 1.0))
    s += SL(0, f'<path d="M1120,960 q120,-60 240,0 l20,60 q-140,50 -280,0 Z"'
               f' fill="{KREM2}" {o(5)}/>')
    s += SL(0, f'<path d="M1180,{940-200*p1:.0f} q70,{80*p1:.0f} 40,{200*p1:.0f}'
               f' l70,16 q40,{-150*p1:.0f} -30,{-220*p1:.0f} Z" fill="{IZUMRUD}"'
               f' opacity="{p1:.2f}" {o(5)}/>')
    s += SL(0, f'<g opacity="{p2:.2f}">'
               f'<rect x="1420" y="860" width="170" height="120" rx="10"'
               f' fill="{MOLOKO}" {o(4)}/>'
               f'<circle cx="1505" cy="920" r="34" fill="{ZOLOTO}" {o(3)}/>')
    for j in range(8):
        a = j * 45
        s += SL(0, f'<circle cx="{1505+46*math.cos(math.radians(a)):.0f}"'
                   f' cy="{920+46*math.sin(math.radians(a)):.0f}" r="9"'
                   f' fill="{ZOLOTO}" {o(2)}/>')
    s += SL(0, "</g>")
    q = A.out(A.seg(t, 2.3, .5))
    s += SL(0, f'<path d="M1260,700 l34,42 l66,-88" fill="none" stroke="#3fae62"'
               f' stroke-width="18" stroke-linecap="round" opacity="{q:.2f}"/>')
    ruk, _ = rukav(760, 600, 260, 40 - 16 * ot, t, VINO, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    s += SL(Z_SRED, f'<path d="M880,1046 l90,-66 l18,22 l-90,66 Z" fill="{SEREBRO}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1700,1000 q50,-30 96,-4 l-8,54 q-46,20 -92,-6 Z"'
                    f' fill="{MOLOKO}" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="1640" cy="960" r="20" fill="none" stroke="{SEREBRO}"'
                    f' stroke-width="5"/><circle cx="1690" cy="960" r="20" fill="none"'
                    f' stroke="{SEREBRO}" stroke-width="5"/>')
    s += SL(Z_SRED, girlyanda(200, 120, 1500, t, 11, 502, 44))
    s += SL(0, lampa_stolika(500, 820, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def dve_kartochki_na_veshalke(t):
    """Две карточки-обложки висят на плечиках, как наряды; коза качает их
    носом. Тёмно-красный фон с еловыми ветками."""
    rnd = random.Random(4131)
    s = f'<rect width="{W}" height="{H}" fill="#2a1016"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 503))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#3a131c" opacity=".8"/>')
    vet = ""
    for i in range(10):
        vx = 80 + i * 200
        vy = 90 + (i % 3) * 60
        for j in range(9):
            vet += (f'<ellipse cx="{vx+j*18}" cy="{vy+int(16*math.sin(j*.8))}" rx="22"'
                    f' ry="11" fill="{HVOYA}" opacity=".9"'
                    f' transform="rotate({-20+j*5} {vx+j*18},{vy})"/>')
    s += SL(Z_DAL, vet)
    s += SL(Z_SRED, f'<rect x="240" y="300" width="1440" height="18" rx="8"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    for i, (cx, kind) in enumerate(((640, "chasy"), (1280, "podarok"))):
        kach = 4.5 * A.w(t, 2.0, i * .4)
        s += SL(0, f'<g transform="rotate({kach:.2f} {cx} 310)">'
                   + plechiki(cx, 330, 1.5, "#7a5a3a", 0.0)
                   + f'<rect x="{cx-260}" y="380" width="520" height="340" rx="16"'
                     f' fill="#1d1218" {o(6)}/>')
        if kind == "chasy":
            s += SL(0, f'<circle cx="{cx-70}" cy="550" r="100" fill="{MOLOKO}" {o(4)}/>'
                       f'<path d="M{cx-70},550 l0,-70 M{cx-70},550 l44,22"'
                       f' stroke="{K}" stroke-width="9" stroke-linecap="round"/>'
                       f'<path d="M{cx+110},490 q60,60 0,120 q-60,-60 0,-120 Z"'
                       f' fill="{SEREBRO}" {o(3)}/>'
                       f'<path d="M{cx+60},480 l120,120 M{cx+180},480 l-120,120"'
                       f' stroke="{ALYY}" stroke-width="12"/>')
        else:
            s += SL(0, f'<rect x="{cx-170}" y="470" width="200" height="170" rx="10"'
                       f' fill="{KORALL}" {o(4)}/>'
                       f'<path d="M{cx-70},470 l0,170 M{cx-170},540 h200"'
                       f' stroke="{ZOLOTO}" stroke-width="14"/>'
                       f'<circle cx="{cx+130}" cy="550" r="70" fill="{MOLOKO}" {o(3)}/>'
                       f'<path d="M{cx+80},500 l100,100 M{cx+180},500 l-100,100"'
                       f' stroke="{ALYY}" stroke-width="12"/>')
        s += SL(0, "</g>")
    s += SL(0, koza(960, 1010, 360, t, .2, True))
    s += SL(0, teplo(960, 820, 420, 360, .24 + .08 * abs(A.w(t, 1.6))))
    sh = ""
    for i in range(6):
        sx = 200 + i * 300
        sh += (f'<circle cx="{sx}" cy="{940+int(20*math.sin(i))}" r="40"'
               f' fill="{(ZOLOTO, SEREBRO, KORALL, IZUMRUD, MOLOKO, VINO)[i]}"'
               f' opacity="{.7+.3*abs(A.w(t,1.9,i*.3)):.2f}" {o(3)}/>')
    s += SL(Z_SRED, sh)
    s += SL(Z_SRED, svecha(300, 1046, t, .2, 1.5) + svecha(1660, 1046, t, .6, 1.4))
    s += SL(Z_SRED, "".join(f'<circle cx="{700+i*120}" cy="1020" r="30" fill="{MED}"'
                            f' {o(3)}/>' for i in range(4)))
    s += SL(Z_SRED, girlyanda(140, 220, 1600, t, 12, 504, 46))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def fotografiya_u_elki(t):
    """Рамка фотографии во весь кадр: снимок оживает — женщина в винном
    бархатном платье у ёлки. В окне за ёлкой — настоящие золотистые огни."""
    rnd = random.Random(4133)
    s = f'<rect width="{W}" height="{H}" fill="#201a1c"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 505))
    s += SL(Z_DAL, stena("oboi", t, 128))
    s += SL(Z_SRED, f'<rect x="120" y="90" width="1680" height="900" rx="20"'
                    f' fill="{DEREVO2}" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="180" y="150" width="1560" height="780" rx="10"'
                    f' fill="#2b2229" {o(5)}/>')
    px, py, pw, ph = 1000, 220, 760, 300
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#16202c"/>'
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-14}" y="{py-14}" width="{pw+28}" height="{ph+28}"'
              f' fill="none" stroke="{MOLOKO}" stroke-width="20"/>'
            + f'<path d="M{px+pw/2:.0f},{py-14} l0,{ph+28}" stroke="{MOLOKO}"'
              f' stroke-width="12"/>')
    s += SL(Z_DAL, elka(760, 930, 620, t, 1.0, True, 506))
    ozh = A.out(A.seg(t, .3, 1.4))
    s += SL(0, f'<g opacity="{.55+.45*ozh:.2f}">'
               + figura(1260, 930, 520, t, VINO, TEPLO_SVET, .2, False, False, 1.0,
                        2.0, True, True, "#f0cfae", True, MOLOKO, True) + "</g>")
    ruk, (hx, hy) = rukav(1180, 680, 150, 40, t, VINO, TEPLO_SVET, .2, 4.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(1340, 690, 140, 24, t, VINO, TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M{h2x-20:.0f},{h2y:.0f} q20,54 40,0 Z" fill="{STEKLO}"'
               f' opacity=".75"/>')
    s += SL(0, f'<circle cx="1190" cy="620" r="24" fill="{ZOLOTO}"'
               f' opacity="{.6+.4*abs(A.w(t,1.5)):.2f}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1420,930 q-28,-180 72,-186 l0,186 Z" fill="#4a3a52" {o(5)}/>')
    # красный фонарик с козой в углу рамки
    mig = .6 + .4 * abs(A.w(t, 1.3, .2))
    s += SL(0, f'<path d="M280,760 q70,-40 140,0 l16,120 q-86,40 -172,0 Z"'
               f' fill="{ALYY}" opacity="{mig:.2f}" {o(5)}/>')
    s += SL(0, f'<path d="M330,820 q20,-26 40,0 q-6,26 -20,28 q-14,-2 -20,-28 Z"'
               f' fill="{ZOLOTO}" opacity="{mig:.2f}"/>')
    s += SL(Z_SRED, svecha(560, 930, t, .2, 1.3) + svecha(640, 930, t, .6, 1.2))
    s += SL(Z_SRED, "".join(f'<circle cx="{420+i*70}" cy="920" r="28" fill="{MED}"'
                            f' {o(3)}/>' for i in range(3)))
    s += SL(Z_SRED, girlyanda(220, 170, 1480, t, 11, 507, 46))
    s += SL(0, lampa_stolika(1620, 880, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def pyat_birok_na_plechikah(t):
    """ГЛАВНЫЙ КАДР РОЛИКА: перекладина шкафа во весь кадр, пять плечиков с
    пустыми бирками. Задняя стенка ровная — на неё лягут карточки памятки."""
    rnd = random.Random(4134)
    s = f'<rect width="{W}" height="{H}" fill="#1b1619"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 508))
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{H}" fill="#241d20"/>')
    s += SL(Z_DAL, doski(0, 760, W, 320, 86))
    s += SL(Z_SRED, perekladina(960, 240, 1700))
    for i in range(5):
        px = 360 + i * 300
        s += SL(0, plechiki(px, 290, 1.5, "#7a5a3a", t, i * .22, 3.0))
        s += SL(0, birka(px, 330, 1.35, t, MOLOKO, i * .3))
    s += SL(Z_SRED, f'<path d="M120,900 q60,-60 120,-2 l14,120 q-74,40 -148,0 Z"'
                    f' fill="{LAVANDA}" {o(5)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{150+i*16},880 l-6,-40" stroke="#6f7a52"'
                        f' stroke-width="4"/>')
    s += SL(Z_SRED, korobka(1480, 1020, 320, t, 130, False, "#b8a289", MOLOKO))
    s += SL(0, f'<path d="M1000,780 q140,{30+10*A.w(t,2.2):.0f} 280,0 l20,300'
               f' q-160,40 -320,0 Z" fill="{VINO}" {o(5)}/>')
    sh = 6 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<g transform="rotate({sh:.2f} 1820 300)">'
                    f'<path d="M1820,300 l0,40" stroke="{SEREBRO}" stroke-width="5"/>'
                    f'<circle cx="1820" cy="390" r="54" fill="{KORALL}"'
                    f' opacity="{.8+.2*abs(A.w(t,1.6)):.2f}" {o(4)}/>'
                    f'<ellipse cx="1800" cy="372" rx="16" ry="10" fill="#ffffff"'
                    f' opacity=".5"/></g>')
    # НИЗ КАДРА БЫЛ ПУСТ (осмотр листа 16.11): на главном кадре ролика под
    # бирками оставалась голая полка. Добавлена нижняя полка шкафа с обувью,
    # коробками и стопкой белья — пустых мест в кадре быть не должно (R-0045).
    s += SL(Z_SRED, f'<rect x="60" y="860" width="1800" height="26" rx="8"'
                    f' fill="{DEREVO}" {o(5)}/>')
    for i in range(4):
        bx = 240 + i * 380
        s += SL(Z_SRED, f'<path d="M{bx},1000 q16,-74 82,-76 q66,2 82,76 Z"'
                        f' fill="#2b2420" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="{620+i*8}" y="{980-i*26}" width="300" height="24"'
                        f' rx="6" fill="{(MOLOKO, KREM2, BEZH, MOLOKO, KREM2)[i]}"'
                        f' {o(3)}/>')
    s += SL(Z_SRED, korobka(1180, 1000, 300, t, 120, False, "#b8a289", MOLOKO))
    s += SL(Z_SRED, girlyanda(100, 120, 1720, t, 12, 509, 44))
    s += SL(0, lampa_stolika(200, 1020, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def tri_naryada_iz_pamyati(t):
    """Старый альбом на коленях: девочка в платье-снежинке, мама в кофточке с
    люрексом, отец в костюме с галстуком на резинке."""
    rnd = random.Random(4141)
    s = f'<rect width="{W}" height="{H}" fill="#241f22"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 510))
    s += SL(Z_DAL, stena("paneli", t, 130))
    s += SL(Z_DAL, elka(1800, 1050, 440, t, 1.0, True, 511))
    s += SL(Z_SRED, f'<path d="M180,1050 q-40,-360 200,-370 h520 q240,10 200,370 Z"'
                    f' fill="#4a3a52" {o(7)}/>')
    s += SL(0, figura(620, 920, 460, t, "#6b5a6b", TEPLO_SVET, .2, False, False, 1.0,
                      1.5, True, True, "#eec9a6", True, MOLOKO, False))
    s += SL(0, f'<path d="M560,560 q60,-40 120,-8 q-16,42 -60,46 q-44,-4 -60,-38 Z"'
               f' fill="#d8d8de" {o(3)}/>')
    # альбом на коленях
    ax, ay = 900, 820
    s += SL(0, f'<path d="M{ax-340},{ay} q340,-70 680,0 l0,220 q-340,70 -680,0 Z"'
               f' fill="#5a3a2a" {o(6)}/>')
    s += SL(0, f'<path d="M{ax-310},{ay+16} q310,-60 620,0 l0,180 q-310,60 -620,0 Z"'
               f' fill="{KREM2}" {o(4)}/>')
    KART = ((ax - 200, MOLOKO, "снежинка"), (ax, "#6a5b73", "люрекс"),
            (ax + 200, GRAFIT, "костюм"))
    for i, (kx, c, kind) in enumerate(KART):
        s += SL(0, f'<rect x="{kx-82}" y="{ay+40}" width="164" height="150" rx="8"'
                   f' fill="#9aa6b0" {o(3)}/>')
        s += SL(0, f'<path d="M{kx-44},{ay+96} q44,-26 88,0 l16,86 h-120 Z"'
                   f' fill="{c}" {o(3)}/>')
        if kind == "снежинка":
            for j in range(6):
                a = j * 60
                s += SL(0, f'<path d="M{kx},{ay+76} l{22*math.cos(math.radians(a)):.0f},'
                           f'{22*math.sin(math.radians(a)):.0f}" stroke="{MOLOKO}"'
                           f' stroke-width="4"/>')
        elif kind == "люрекс":
            for j in range(8):
                s += SL(0, f'<circle cx="{kx-34+j*10}" cy="{ay+120+int(10*math.sin(j))}"'
                           f' r="4" fill="#ffffff"'
                           f' opacity="{.3+.6*abs(A.w(t,1.6,j*.2)):.2f}"/>')
        else:
            s += SL(0, f'<path d="M{kx-6},{ay+96} l12,0 l-4,60 h-4 Z" fill="{VINO}" {o(2)}/>')
    glad = A.seg(t, .4, 2.4)
    ruk, (hx, hy) = rukav(1180, 640, 230, 128 - 10 * glad, t, "#6b5a6b", TEPLO_SVET,
                          .2, 4.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(520, 700, 200, 56, t, "#6b5a6b", TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    s += SL(Z_SRED, f'<path d="M200,900 q140,-50 280,0 l0,150 q-140,50 -280,0 Z"'
                    f' fill="{KORALL}" opacity=".75"/>')
    s += SL(Z_SRED, kot(1400, 1046, t, 1.4, "#6b5a46"))
    s += SL(Z_SRED, f'<path d="M1500,940 q-10,-56 36,-58 q46,2 36,58 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, par(1536, 880, t, 3, .4, 110, .4, .8))
    s += SL(Z_SRED, f'<rect x="1660" y="620" width="14" height="420" fill="{CHUGUN}" {o(3)}/>'
                    f'<path d="M1600,620 h134 l-20,-86 h-94 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, lampa_stolika(1667, 600, t, 1.4))
    s += SL(Z_SRED, girlyanda(200, 120, 1300, t, 10, 512, 44))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tanec_v_polnoch(t):
    """Комната в огоньках: женщина в винном бархате танцует на паркете, подол
    отлетает по повороту. В циферблате часов — настоящие стрелки у полуночи."""
    rnd = random.Random(4142)
    s = f'<rect width="{W}" height="{H}" fill="#201a20"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 513))
    s += SL(Z_DAL, stena("oboi", t, 131))
    px, py, pw, ph = 180, 120, 420, 420
    put = kontur_proema(px, py, pw, ph, "ellips")
    s += SL(Z_DAL, f'<path d="{put}" fill="#2b2430"/>'
            + mesto_stoka(px, py, pw, ph, "ellips")
            + f'<circle cx="{px+pw/2:.0f}" cy="{py+ph/2:.0f}" r="{pw/2+20:.0f}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="30"/>'
            + f'<circle cx="{px+pw/2:.0f}" cy="{py+ph/2:.0f}" r="{pw/2+44:.0f}"'
              f' fill="none" stroke="{ZOLOTO}" stroke-width="10" opacity=".7"/>')
    s += SL(Z_DAL, elka(1760, 1050, 520, t, 1.0, True, 514))
    s += SL(Z_SRED, polovicy(820))
    par_ = "".join(f'<path d="M{60+i*118},820 l0,260" stroke="#5a3d26"'
                   f' stroke-width="3" opacity=".5"/>' for i in range(16))
    s += SL(Z_SRED, par_)
    # танец
    kruzh = A.seg(t, .15, 3.4)
    fx = 960 + 120 * math.sin(kruzh * 2 * math.pi)
    s += SL(0, figura(fx, 1040, 620, t, VINO, TEPLO_SVET, .2, False, False, 1.0,
                      3.0, True, True, "#f0cfae", True, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(fx + sgn * 110, 760, 200, -30 * sgn - 14, t, VINO, TEPLO_SVET,
                       .2 + (0 if sgn < 0 else .3), 7.0)
        s += SL(0, ruk)
    veer = abs(math.sin(kruzh * 2 * math.pi))
    for i in range(14):
        a = -84 + i * 13
        dl = 220 + 110 * veer
        ex = fx + dl * math.cos(math.radians(a))
        ey = 1040 - 260 + dl * math.sin(math.radians(a)) * .45
        s += SL(0, f'<path d="M{fx:.0f},{1040-340} L{ex:.0f},{ey:.0f} l24,18 Z"'
                   f' fill="{VINO}" opacity="{.8+.15*((i+int(kruzh*7))%2):.2f}" {o(3)}/>')
    s += SL(0, f'<circle cx="{fx-40:.0f}" cy="640" r="22" fill="{ZOLOTO}"'
               f' opacity="{.6+.4*abs(A.w(t,1.4)):.2f}" {o(3)}/>')
    s += SL(0, tufli(fx - 70, 1046, 1.0, GRAFIT, t))
    # стол со свечами и бокалами
    s += SL(Z_SRED, stol(1240, 900, 520, 40))
    s += SL(Z_SRED, svecha(1340, 866, t, .1, 1.4) + svecha(1460, 866, t, .5, 1.3))
    for i in range(3):
        bx = 1580 + i * 60
        s += SL(Z_SRED, f'<path d="M{bx-20},820 q20,54 40,0 Z" fill="{STEKLO}"'
                        f' opacity=".75"/>'
                        f'<path d="M{bx},820 l0,40 M{bx-18},864 h36" stroke="{STEKLO}"'
                        f' stroke-width="5"/>')
    # конфетти
    for i in range(26):
        p = ((t * .5 + i * .13) % 1.0)
        cx = 80 + (i * 73) % 1760
        cy = -40 + 1140 * p
        c = (KORALL, ZOLOTO, MOLOKO, IZUMRUD, SEREBRO)[i % 5]
        s += SL(Z_SRED, f'<rect x="{cx:.0f}" y="{cy:.0f}" width="14" height="22" rx="4"'
                        f' fill="{c}" opacity=".85"'
                        f' transform="rotate({i*37+t*90:.0f} {cx:.0f},{cy:.0f})"/>')
    s += SL(Z_SRED, f'<path d="M700,1046 q-30,-200 90,-206 l0,206 Z" fill="#4a3a52" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(120, 160, 1700, t, 13, 515, 50))
    s += SL(0, lampa_stolika(1200, 820, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s
