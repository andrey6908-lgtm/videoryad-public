# -*- coding: utf-8 -*-
"""Декорации ролика «В чём встречать Новый год 2027», часть 3 (планы 71-103).

Третий и четвёртый женские наряды, затем мужская глава: шкаф, рубашки,
джемперы, костюмы, галстуки, обувь. Все сцены нарисованы заново (R-0019).
"""
import math, random
from baza import *
from lok_obshchee import *
import anim as A


def _mel_polka(x, y, w_, t, seed, n=7):
    """Полка мелочей мужской комнаты: запонки, щётки, флаконы, коробочки."""
    rnd = random.Random(seed)
    s = polka(x, y, w_)
    for i in range(n):
        px = x + w_ * (i + .5) / n
        h_ = rnd.uniform(24, 50)
        c = rnd.choice((GRAFIT, DEREVO2, SEREBRO, MOLOKO, VINO, BEZH))
        s += (f'<rect x="{px-13:.0f}" y="{y-h_:.0f}" width="26" height="{h_:.0f}"'
              f' rx="5" fill="{c}" {o(3)}/>'
              f'<rect x="{px-16:.0f}" y="{y-h_-6:.0f}" width="32" height="8" rx="3"'
              f' fill="{SEREBRO}" {o(2)}/>')
        s += (f'<circle cx="{px:.0f}" cy="{y-h_-16:.0f}" r="5" fill="{ZOLOTO}"'
              f' opacity="{.4+.5*abs(A.w(t, 2.2, i*.3)):.2f}"/>')
    return s


def _zriteli_pod(x, y, n, t, seed=5, h_=120):
    """Ряд зрителей-силуэтов у подиума: тёмные головы и плечи, чуть качаются."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        zx = x + i * 92 + rnd.uniform(-8, 8)
        dy = 4 * A.w(t, 2.2, i * .25)
        s += (f'<g transform="translate(0,{dy:.1f})">'
              f'<ellipse cx="{zx:.0f}" cy="{y:.0f}" rx="46" ry="{h_*.52:.0f}"'
              f' fill="#15131a" opacity=".88"/>'
              f'<circle cx="{zx:.0f}" cy="{y-h_*.52:.0f}" r="30" fill="#15131a"'
              f' opacity=".88"/></g>')
    return s


def platya_uezzhayut_kostyum_ostaetsya(t):
    """Рукав отодвигает все платья на штанге одним движением, и на свободном
    месте остаётся брючный костюм."""
    rnd = random.Random(3071)
    s = f'<rect width="{W}" height="{H}" fill="#221f26"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 151))
    s += SL(Z_DAL, stena("oboi", t, 101))
    s += SL(Z_DAL, elka(140, 1050, 400, t, 1.0, True, 153))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, shtanga(1060, 1040, 1300, t, 520))
    ot = A.out(A.seg(t, .3, 1.5))
    for i, c in enumerate((VINO, IZUMRUD, KORALL, LAVANDA, TERRAKOT)):
        px = 640 + i * 110 - 420 * ot
        s += SL(Z_SRED, naryad_plechiki(px, 540, 400, t, c, 1.0, i * .2, True, None, .04, 160 + i))
    s += SL(0, naryad_plechiki(1320, 520, 480, t, TSINIY, 1.3, .1, False, MOLOKO, .05, 166, 1.6))
    s += SL(0, f'<path d="M1230,900 h190 l10,230 h-72 l-30,-170 l-30,170 h-72 Z"'
               f' fill="{TSINIY}" {o(5)}/>')
    s += SL(0, figura(560, 1050, 520, t, GRAFIT, HOLOD_KANT, .2, False, False, 1.0,
                      2.0, True, True, "#eec9a6", False, MOLOKO, True))
    ruk, _ = rukav(650, 740, 260, -14 + 16 * ot, t, GRAFIT, HOLOD_KANT, .2, 5.0)
    s += SL(0, ruk)
    s += SL(Z_SRED, tufli(380, 1046, 1.1, GRAFIT, t))
    s += SL(Z_SRED, f'<path d="M240,1046 q-22,-140 60,-144 l0,144 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(60, 300, 190, 560, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(300, 140, 1500, t, 11, 167, 52))
    s += SL(0, lampa_stolika(1760, 900, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def naryad_tretiy_na_manekene(t):
    """Манекен в брючном костюме: выноски показывают жакет по фигуре, одну
    пуговицу и брюки до щиколотки; оттенок идёт от молочного к тёмно-синему."""
    rnd = random.Random(3072)
    s = f'<rect width="{W}" height="{H}" fill="#201e24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 155))
    s += SL(Z_DAL, stena("kraska", t, 102))
    s += SL(Z_DAL, elka(1840, 1050, 340, t, 1.0, True, 157))
    s += SL(Z_SRED, polovicy(1050))
    perekl = (t % 3.4) < 1.7
    col = MOLOKO if perekl else TSINIY
    s += SL(0, manekken(880, 1000, 700, t, KREM2, "zh", col, .2, None, .04, 170, False))
    s += SL(0, f'<path d="M760,640 h240 l16,370 h-104 l-32,-250 l-32,250 h-104 Z"'
               f' fill="{col}" {o(6)}/>')
    s += SL(0, f'<circle cx="880" cy="600" r="16" fill="{ZOLOTO}"'
               f' opacity="{.6+.4*abs(A.w(t,1.6)):.2f}" {o(2)}/>')
    VYN = ((790, 520, -1), (880, 600, 1), (960, 980, 1))
    for i, (vx, vy, sgn) in enumerate(VYN):
        p = A.out(A.seg(t, .4 + i * .6, .6))
        if p <= .02:
            continue
        ex = vx + sgn * 250 * p
        s += SL(0, f'<path d="M{vx},{vy} L{ex:.0f},{vy-56*p:.0f}" stroke="{ZOLOTO}"'
                   f' stroke-width="6" opacity="{p:.2f}"/>'
                   f'<circle cx="{vx}" cy="{vy}" r="11" fill="{ZOLOTO}" opacity="{p:.2f}"/>'
                   f'<rect x="{min(vx,ex):.0f}" y="{vy-96*p:.0f}" width="230" height="50"'
                   f' rx="10" fill="{GRAFIT}" opacity="{p*.9:.2f}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1420,880 l240,-26 l8,58 l-240,26 Z" fill="{MOLOKO}" {o(6)}/>'
                    f'<path d="M1460,938 l0,104 M1630,920 l0,122" stroke="{SEREBRO}"'
                    f' stroke-width="8"/>')
    s += SL(Z_SRED, f'<path d="M1490,862 q54,-38 106,-4 l6,28 l-116,14 Z" fill="{CHUGUN}" {o(5)}/>')
    s += SL(Z_SRED, par(1546, 846, t, 4, .5, 150, .45, 1.0))
    s += SL(Z_SRED, tufli(1240, 1046, 1.1, GRAFIT, t))
    s += SL(Z_SRED, f'<rect x="320" y="880" width="180" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="330" y="906" width="18" height="140" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="472" y="906" width="18" height="140" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, zerkalo(80, 280, 200, 560, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(300, 140, 1400, t, 10, 171, 52))
    s += SL(0, lampa_stolika(1760, 860, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def yubka_v_skladku(t):
    """Женщина кружится перед зеркалом в длинной юбке в складку: складки
    раскрываются веером по ходу поворота."""
    rnd = random.Random(3074)
    s = f'<rect width="{W}" height="{H}" fill="#231e24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 159))
    s += SL(Z_DAL, stena("paneli", t, 103))
    s += SL(Z_DAL, elka(1830, 1050, 380, t, 1.0, True, 161))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, zerkalo(120, 180, 520, 760, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="136" y="196" width="488" height="728" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    kruzh = A.seg(t, .2, 3.2)
    ug = 360 * kruzh
    fx = 1020
    s += SL(0, figura(fx, 1040, 560, t, IZUMRUD, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", False, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(fx + sgn * 100, 760, 170, 30 * sgn, t, IZUMRUD, TEPLO_SVET,
                       .2 + (0 if sgn < 0 else .3), 6.0)
        s += SL(0, ruk)
    veer = abs(math.sin(math.radians(ug)))
    for i in range(16):
        a = -90 + i * 12
        dl = 230 + 90 * veer
        ex = fx + dl * math.cos(math.radians(a))
        ey = 1040 - 240 + dl * math.sin(math.radians(a)) * .5
        s += SL(0, f'<path d="M{fx},{1040-320} L{ex:.0f},{ey:.0f} l22,16 Z"'
                   f' fill="{VINO}" opacity="{.75+.2*((i+int(kruzh*8))%2):.2f}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1500" y="840" width="180" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="1510" y="866" width="18" height="180" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1652" y="866" width="18" height="180" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M1520,840 q40,120 10,220 h80 q30,-100 -10,-220 Z"'
                    f' fill="{GRAFIT}" {o(5)}/>')
    s += SL(Z_SRED, kot(760, 1046, t, 1.3, "#3b3430"))
    s += SL(Z_SRED, f'<rect x="700" y="620" width="14" height="420" fill="{CHUGUN}" {o(3)}/>'
                    f'<path d="M640,620 h134 l-20,-86 h-94 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, lampa_stolika(707, 600, t, 1.4))
    s += SL(Z_SRED, tufli(840, 1046, 1.0, VINO, t))
    s += SL(Z_SRED, girlyanda(700, 140, 1100, t, 9, 163, 50))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def zhaket_i_bryuki_iz_raznyh_shkafov(t):
    """Жакет и брюки выезжают из двух шкафов навстречу друг другу: оттенок
    совпал — загорается галочка."""
    rnd = random.Random(3075)
    s = f'<rect width="{W}" height="{H}" fill="#221d22"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 165))
    s += SL(Z_DAL, stena("doski", t, 104))
    s += SL(Z_DAL, shkaf(40, 1050, 700, 900, t, .9, False))
    s += SL(Z_DAL, shkaf(1180, 1050, 700, 900, t, .9, True))
    s += SL(Z_SRED, polovicy(1050))
    p = A.out(A.seg(t, .25, 1.4))
    jx = 300 + 420 * p
    bx = 1620 - 420 * p
    s += SL(0, naryad_plechiki(jx, 300, 420, t, TSINIY, 1.2, .1, False, MOLOKO, .05, 172))
    s += SL(0, f'<path d="M{bx-100:.0f},540 h200 l12,420 h-80 l-32,-300 l-32,300 h-80 Z"'
               f' fill="{TSINIY}" {o(6)}/>')
    if p > .85:
        gx, gy = 960, 560
        q = A.out(A.seg(t, 1.6, .5))
        s += SL(0, f'<path d="M{gx},{gy} l34,42 l66,-88" fill="none" stroke="#3fae62"'
                   f' stroke-width="18" stroke-linecap="round" opacity="{q:.2f}"/>')
    s += SL(Z_SRED, korobka(820, 1046, 260, t, 110, True, BEZH, MOLOKO))
    s += SL(Z_SRED, f'<path d="M1060,1046 q-20,-130 58,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(880, 180, 200, 420, t, "pryam", ZOLOTO, True))
    s += SL(Z_DAL, elka(1870, 1050, 300, t, 1.0, True, 173))
    s += SL(Z_SRED, girlyanda(120, 130, 1680, t, 12, 175, 54))
    s += SL(0, lampa_stolika(960, 960, t, 1.15))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def dve_podrugi_u_zerkala(t):
    """Две подруги у большого зеркала в прихожей: винное платье, расширенное
    книзу, и тёмно-синее с запахом. Обе довольны отражением."""
    rnd = random.Random(3076)
    s = f'<rect width="{W}" height="{H}" fill="#241f22"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 177))
    s += SL(Z_DAL, stena("oboi", t, 105))
    s += SL(Z_DAL, f'<rect x="1360" y="200" width="500" height="780" rx="12"'
                   f' fill="#2a232a" {o(6)}/>')
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, zerkalo(620, 150, 700, 820, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="636" y="166" width="668" height="788" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    # отражения: те же силуэты, тускло
    s += SL(Z_SRED, f'<g opacity=".42">'
                    + figura(820, 920, 420, t, VINO, TEPLO_SVET, .2, False, False, .6,
                             1.5, True, False, "#f0cfae", True, None, False)
                    + figura(1080, 920, 430, t, TSINIY, TEPLO_SVET, .5, False, False, .6,
                             1.5, True, False, "#f0cfae", True, None, False) + "</g>")
    # полная женщина в винном: обе руки на поясе — рукава внешние
    s += SL(0, figura(430, 1050, 520, t, VINO, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(430 + sgn * 100, 760, 120, 60 * sgn + 14, t, VINO, TEPLO_SVET,
                       .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M330,700 q100,-30 200,0 l60,350 q-160,40 -320,0 Z"'
               f' fill="{VINO}" {o(6)}/>')
    # седая в тёмно-синем с запахом: правая рука к серьге
    s += SL(0, figura(1660, 1050, 500, t, TSINIY, TEPLO_SVET, .5, False, False, 1.0,
                      2.0, True, True, "#eec9a6", True, MOLOKO, True))
    ruk, (hx, hy) = rukav(1600, 770, 150, -108, t, TSINIY, TEPLO_SVET, .4, 5.0)
    s += SL(0, ruk)
    s += SL(0, f'<circle cx="{hx:.0f}" cy="{hy+8:.0f}" r="12" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(0, f'<path d="M1560,700 l200,40 l-30,80 l-170,-50 Z" fill="{TSINIY}" {o(5)}/>')
    s += SL(0, f'<path d="M1600,580 q60,-40 120,-6 q-20,40 -60,44 q-40,-4 -60,-38 Z"'
               f' fill="#d8d8de" {o(3)}/>')
    s += SL(Z_SRED, tufli(1240, 1046, 1.0, GRAFIT, t))
    s += SL(Z_SRED, f'<path d="M180,1046 q-22,-140 62,-146 l0,146 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1320,900 q40,-14 62,16 l12,96 h-92 Z" fill="{GRAFIT}" {o(4)}/>')
    s += SL(Z_SRED, girlyanda(200, 130, 1600, t, 11, 179, 52))
    s += SL(0, lampa_stolika(1420, 760, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def dva_platya_chetvertogo_naryada(t):
    """Два манекена: платье-трапеция и платье с запахом. В высоком зеркале за
    ними — настоящая матовая ткань."""
    rnd = random.Random(3077)
    s = f'<rect width="{W}" height="{H}" fill="#211d24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 181))
    s += SL(Z_DAL, stena("kraska", t, 106))
    # зеркало-проём ровно по центру
    px, py, pw, ph = 580, 200, 760, 420
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#22202a"/>'
            + otrez(px + 30, py + 40, pw - 60, ph - 90, TSINIY, t, 183, 0, .2)
            + mesto_stoka(px, py, pw, ph, "pryam")
            + zerkalo(px, py, pw, ph, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, polovicy(1050))
    rasch = A.out(A.seg(t, .3, 1.4))
    s += SL(0, manekken(500, 1020, 660, t, KREM2, "zh", VINO, .2, None, .04, 184))
    s += SL(0, f'<path d="M{500-120-60*rasch:.0f},700 q120,-30 240,0'
               f' l{60+40*rasch:.0f},320 q-{180+60*rasch:.0f},40 -{360+120*rasch:.0f},0 Z"'
               f' fill="{VINO}" {o(6)}/>')
    s += SL(0, manekken(1420, 1020, 660, t, KREM2, "zh", IZUMRUD, .5, None, .04, 185))
    zap = A.out(A.seg(t, .7, 1.2))
    s += SL(0, f'<path d="M1300,660 L{1420+100*zap:.0f},760 l-20,300 h-120 Z"'
               f' fill="{IZUMRUD}" {o(5)}/>')
    s += SL(0, f'<path d="M1540,660 L{1420-60*zap:.0f},780 l20,280 h110 Z"'
               f' fill="#0d5c40" {o(5)}/>')
    if zap > .7:
        s += SL(0, f'<path d="M1480,800 q40,16 70,-10 l-10,60 q-40,10 -70,-14 Z"'
                   f' fill="{ZOLOTO}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M900,900 q60,120 20,146" fill="none" stroke="{MOLOKO}"'
                    f' stroke-width="12"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{896+i*3},{918+i*18} l16,0" stroke="{K}"'
                        f' stroke-width="2" opacity=".6"/>')
    s += SL(Z_SRED, f'<rect x="820" y="880" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="830" y="906" width="18" height="140" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="962" y="906" width="18" height="140" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, tufli(1000, 1046, 1.0, GRAFIT, t))
    s += SL(Z_DAL, elka(120, 1050, 380, t, 1.0, True, 187))
    s += SL(Z_SRED, girlyanda(400, 130, 1300, t, 10, 189, 50))
    s += SL(0, lampa_stolika(1760, 920, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def sergi_sumochka_i_udobnye_tufli(t):
    """Пуфик у зеркала: блестящая сумочка и серьги на подставке, внизу туфли
    на широком каблуке; коробку со шпильками закрывает рукав."""
    rnd = random.Random(3079)
    s = f'<rect width="{W}" height="{H}" fill="#241f25"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 191))
    s += SL(Z_DAL, stena("paneli", t, 107))
    s += SL(Z_DAL, elka(140, 1050, 330, t, 1.0, True, 193))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, zerkalo(1300, 160, 520, 620, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1314" y="174" width="492" height="592" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    # пуфик крупно
    s += SL(0, f'<path d="M620,1000 q-50,-230 160,-238 q210,8 160,238 Z"'
               f' fill="#45384f" {o(7)}/>')
    s += SL(0, f'<ellipse cx="780" cy="770" rx="170" ry="40" fill="#51425c" {o(4)}/>')
    bl = .6 + .4 * abs(A.w(t, 1.7))
    s += SL(0, f'<path d="M640,760 q90,-50 180,0 l20,120 q-110,30 -220,0 Z"'
               f' fill="{GRAFIT}" {o(5)}/>')
    s += SL(0, f'<path d="M640,760 q90,-50 180,0" fill="none" stroke="{SEREBRO}"'
               f' stroke-width="9" opacity="{bl:.2f}"/>')
    s += SL(0, tkan_blesk(640, 740, 200, 140, t, "#ffffff", .5, .2))
    s += SL(0, f'<path d="M900,780 q60,-26 110,0 l10,90 h-130 Z" fill="{VINO}" {o(4)}/>')
    for sgn in (-1, 1):
        sx = 955 + sgn * 30
        s += SL(0, f'<path d="M{sx},780 l0,-46" stroke="{ZOLOTO}" stroke-width="6"/>'
                   f'<circle cx="{sx}" cy="{728-5*abs(A.w(t,1.8,sgn*.3)):.0f}" r="17"'
                   f' fill="{ZOLOTO}" {o(2)}/>')
    s += SL(0, tufli(1060, 1046, 1.3, GRAFIT, t, True, False))
    # коробка со шпильками закрывается рукавом
    zak = A.out(A.seg(t, .5, 1.3))
    s += SL(0, korobka(1360, 1046, 300, t, 110, zak < .8, "#b8a289", MOLOKO))
    ruk, _ = rukav(1760, 700, 230, 134 - 30 * zak, t, VINO, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    s += SL(Z_SRED, f'<rect x="460" y="1010" width="420" height="50" rx="10"'
                    f' fill="#5a4038" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M300,1046 l110,-16 l6,24 l-110,16 Z" fill="{DEREVO2}" {o(3)}/>')
    s += SL(0, f'<path d="M380,150 q160,{40+12*A.w(t,2.2):.0f} 320,0 l0,120'
               f' q-160,{-28+10*A.w(t,2.2,.3):.0f} -320,0 Z" fill="{VINO}" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(760, 130, 1000, t, 9, 195, 48))
    s += SL(0, lampa_stolika(1180, 820, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tri_platya_tesnoe_meshok_i_v_samyy(t):
    """Три манекена: тесное платье трещит по швам, балахон висит мешком, а
    полуприталенное сидит ровно — над ним галочка."""
    rnd = random.Random(3080)
    s = f'<rect width="{W}" height="{H}" fill="#221d23"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 197))
    s += SL(Z_DAL, stena("doski", t, 108))
    s += SL(Z_DAL, _mel_polka(60, 280, 420, t, 80, 6))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, manekken(360, 1010, 640, t, KREM2, "zh", KORALL, .1, None, .04, 198))
    tresk = abs(A.w(t, 1.3))
    for i in range(5):
        s += SL(0, f'<path d="M{300+i*30},{640+i*40} l{40+20*tresk:.0f},{10:.0f}"'
                   f' stroke="{MOLOKO}" stroke-width="5" opacity="{.5+.4*tresk:.2f}"/>')
    s += SL(0, f'<path d="M250,520 l220,0" stroke="#d13a3a" stroke-width="14"'
               f' opacity=".9"/>')
    s += SL(0, manekken(960, 1010, 640, t, KREM2, "zh", IZUMRUD, .4, None, .04, 199))
    p = A.out(A.seg(t, .6, .6))
    s += SL(0, f'<path d="M880,480 l34,42 l66,-88" fill="none" stroke="#3fae62"'
               f' stroke-width="18" stroke-linecap="round" opacity="{p:.2f}"/>')
    s += SL(0, manekken(1560, 1010, 640, t, KREM2, "zh", LAVANDA, .7, None, .04, 200))
    s += SL(0, f'<path d="M1400,620 q160,-40 320,0 l60,400 q-220,50 -440,0 Z"'
               f' fill="{LAVANDA}" {o(6)}/>')
    s += SL(0, skladki(1420, 660, 280, 340, LAVANDA, 6, 201, t, 4.0))
    s += SL(0, f'<path d="M1450,520 l220,0" stroke="#d13a3a" stroke-width="14"'
               f' opacity=".9"/>')
    # портниха показывает на средний
    s += SL(0, figura(700, 1050, 460, t, HVOYA, TEPLO_SVET, .3, False, False, 1.0,
                      2.0, True, True, "#eec9a6", False, MOLOKO, True))
    ruk, _ = rukav(770, 800, 190, -16 + 8 * A.w(t, 1.7), t, HVOYA, TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    sv = 9 * A.w(t, 2.0, .3)
    s += SL(0, f'<path d="M660,710 q{20+sv:.0f},80 {-10+sv:.0f},150" fill="none"'
               f' stroke="{MOLOKO}" stroke-width="11"/>')
    s += SL(Z_SRED, stol(60, 1020, 300, 32))
    s += SL(Z_SRED, girlyanda(200, 130, 1600, t, 11, 203, 50))
    s += SL(0, lampa_stolika(240, 960, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def perebor_plechikov_matovoe(t):
    """Женщина перебирает плечики в шкафу: блестящее отодвигает, пёстрое
    отодвигает, матовое тёмно-синее снимает и прикладывает к себе."""
    rnd = random.Random(3081)
    s = f'<rect width="{W}" height="{H}" fill="#201c22"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 205))
    s += SL(Z_DAL, stena("oboi", t, 109))
    s += SL(Z_DAL, shkaf(740, 1050, 1060, 980, t, 1.0, False))
    s += SL(Z_SRED, perekladina(1270, 260, 940))
    s += SL(Z_SRED, polovicy(1050))
    hod = A.seg(t, .3, 3.0)
    for i, c in enumerate((SEREBRO, KORALL, TSINIY, LAVANDA, MOLOKO)):
        sdvig = 150 * max(0.0, min(1.0, hod * 3 - i)) if i < 2 else 0
        px = 900 + i * 180 - sdvig
        vys = 420 if i != 2 else 420 - 120 * max(0.0, min(1.0, hod * 2 - 1.2))
        s += SL(Z_SRED if i != 2 else 0,
                naryad_plechiki(px, 280, vys, t, c, 1.1, i * .2, True, None,
                                .45 if i == 0 else .04, 206 + i))
    # женщина прикладывает матовое к себе
    s += SL(0, figura(480, 1050, 540, t, GRAFIT, HOLOD_KANT, .3, False, False, 1.0,
                      2.0, True, True, "#eec9a6", True, MOLOKO, True))
    ruk, _ = rukav(570, 720, 280, -22 + 12 * A.w(t, 1.8), t, GRAFIT, HOLOD_KANT, .2, 5.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(560, 820, 160, 20, t, GRAFIT, HOLOD_KANT, .5, 4.0)
    s += SL(0, ruk2)
    prilozh = A.out(A.seg(t, 1.4, 1.2))
    if prilozh > .05:
        s += SL(0, f'<path d="M{400:.0f},{700:.0f} q80,-26 160,0 l30,300'
                   f' q-110,30 -220,0 Z" fill="{TSINIY}" opacity="{prilozh:.2f}" {o(5)}/>')
    s += SL(Z_SRED, kot(1700, 1046, t, 1.4, "#3b3430"))
    s += SL(Z_SRED, tufli(300, 1046, 1.0, GRAFIT, t))
    s += SL(Z_SRED, f'<path d="M160,1046 q-20,-130 58,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(60, 300, 170, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_DAL, elka(1860, 1050, 280, t, 1.0, True, 211))
    s += SL(Z_SRED, girlyanda(760, 120, 1080, t, 9, 213, 48))
    s += SL(0, lampa_stolika(1760, 880, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def busy_u_sosedki_tufli_u_sestry(t):
    """Лестничная площадка: соседка подаёт нитку бус, сестра машет из своей
    двери, девушка в бигуди держит коробку с туфлями."""
    rnd = random.Random(3082)
    s = f'<rect width="{W}" height="{H}" fill="#2a2520"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 215))
    s += SL(Z_DAL, kladka(0, 0, W, 1080, 78))
    s += SL(Z_DAL, dver(180, 180, 380, 800, .35, "url(#derev)", True, True))
    s += SL(Z_DAL, dver(1360, 180, 380, 800, .22, "url(#derev)", True, False))
    s += SL(Z_SRED, polovicy(1000))
    ya = ""
    for i in range(6):
        ya += (f'<rect x="{760+(i%3)*90}" y="{300+(i//3)*120}" width="78" height="104"'
               f' rx="6" fill="{CHUGUN}" {o(4)}/>'
               f'<rect x="{772+(i%3)*90}" y="{330+(i//3)*120}" width="54" height="10"'
               f' fill="#1b1b1b"/>')
    s += SL(Z_SRED, ya)
    # соседка в халате подаёт бусы обеими руками
    s += SL(0, figura(330, 1000, 470, t, KORALL, TEPLO_SVET, .2, True, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, False))
    p = A.out(A.seg(t, .3, 1.6))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(330 + sgn * 76, 740, 170, -16 + sgn * 10, t, KORALL,
                              TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
    bx = 500 + 300 * p
    bus = ""
    for i in range(18):
        bus += (f'<circle cx="{bx-90+i*11:.0f}" cy="{700+34*math.sin(i*.5):.0f}" r="10"'
                f' fill="{MOLOKO}" {o(2)}/>')
    s += SL(0, bus)
    # девушка в бигуди принимает бусы, коробка под мышкой
    s += SL(0, figura(980, 1000, 500, t, IZUMRUD, TEPLO_SVET, .5, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, (hx, hy) = rukav(900, 720, 180, -176, t, IZUMRUD, TEPLO_SVET, .4, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(1060, 760, 130, 30, t, IZUMRUD, TEPLO_SVET, .7, 4.0)
    s += SL(0, ruk2)
    s += SL(0, korobka(1070, 860, 220, t, 90, False, "#b8a289", MOLOKO))
    big = ""
    for i in range(7):
        big += (f'<circle cx="{940+i*16}" cy="{560-abs(i-3)*10}" r="16" fill="{PUDRA}"'
                f' {o(2)}/>')
    s += SL(0, big)
    # сестра машет из второй двери
    s += SL(Z_SRED, figura(1560, 980, 420, t, LAVANDA, TEPLO_SVET, .8, False, False,
                           1.0, 2.0, True, True, "#eec9a6", True, None, False))
    mah = 24 * A.w(t, 1.4, .2)
    ruk3, _ = rukav(1500, 720, 160, -96 + mah, t, LAVANDA, TEPLO_SVET, .6, 8.0)
    s += SL(Z_SRED, ruk3)
    # коврики, санки, венок
    s += SL(Z_SRED, f'<rect x="200" y="1000" width="300" height="46" rx="8"'
                    f' fill="#5a4038" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M620,1000 h220 l0,-26 h-220 Z" fill="{DEREVO2}" {o(4)}/>'
                    f'<path d="M640,1000 l-20,46 M820,1000 l20,46" stroke="{CHUGUN}"'
                    f' stroke-width="7"/>')
    ven = "".join(f'<ellipse cx="{1550+70*math.cos(math.radians(i*24)):.0f}"'
                  f' cy="{280+70*math.sin(math.radians(i*24)):.0f}" rx="19" ry="11"'
                  f' fill="{HVOYA}" {o(2)}/>' for i in range(15))
    s += SL(Z_SRED, ven)
    s += SL(Z_SRED, girlyanda(560, 150, 820, t, 8, 217, 46))
    s += SL(0, lampa_stolika(760, 220, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def sharf_ot_docheri_sumochka_ot_vnuch(t):
    """Прихожая: дочь повязывает бабушке винный шарф, внучка вешает ей на
    плечо свою блестящую сумочку."""
    rnd = random.Random(3083)
    s = f'<rect width="{W}" height="{H}" fill="#241f23"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 219))
    s += SL(Z_DAL, stena("paneli", t, 111))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, zerkalo(1480, 180, 380, 640, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1494" y="194" width="352" height="612" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    # бабушка в центре, руки разведены
    s += SL(0, figura(960, 1050, 530, t, TSINIY, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#eec9a6", True, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(960 + sgn * 100, 760, 160, 34 * sgn, t, TSINIY, TEPLO_SVET,
                       .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M900,580 q60,-40 120,-8 q-16,42 -60,46 q-44,-4 -60,-38 Z"'
               f' fill="#d8d8de" {o(3)}/>')
    # дочь слева повязывает шарф
    s += SL(0, figura(600, 1050, 500, t, HVOYA, TEPLO_SVET, .5, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    p = A.out(A.seg(t, .3, 1.5))
    for sgn in (-1, 1):
        ruk, _ = rukav(600 + sgn * 84, 720, 230, -24 + sgn * 16, t, HVOYA, TEPLO_SVET,
                       .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M870,{640-40*(1-p):.0f} q90,{30*p:.0f} 180,0 l10,80'
               f' q-100,34 -200,0 Z" fill="{VINO}" opacity="{p:.2f}" {o(5)}/>')
    # внучка справа вешает сумочку и показывает «отлично»
    s += SL(0, figura(1300, 1050, 430, t, KORALL, TEPLO_SVET, .8, False, False, 1.0,
                      2.5, True, True, "#f3d3b2", True, MOLOKO, True))
    q = A.out(A.seg(t, .9, 1.3))
    ruk, (hx, hy) = rukav(1230, 760, 190, -156, t, KORALL, TEPLO_SVET, .6, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(1370, 770, 150, -56, t, KORALL, TEPLO_SVET, .9, 5.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M{1060+60*q:.0f},{700+30*q:.0f} q40,-16 62,14 l10,80 h-90 Z"'
               f' fill="{SEREBRO}" opacity="{.5+.5*q:.2f}" {o(4)}/>')
    s += SL(0, f'<circle cx="{h2x:.0f}" cy="{h2y:.0f}" r="22" fill="none"'
               f' stroke="{ZOLOTO}" stroke-width="8"/>')
    s += SL(Z_SRED, f'<rect x="120" y="240" width="520" height="18" rx="8"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    for i, c in enumerate(("#5c4a3f", "#4a3f38")):
        s += SL(Z_SRED, naryad_plechiki(240 + i * 220, 260, 400, t, c, 1.1, i * .3,
                                        False, MOLOKO, .0, 221 + i))
    s += SL(Z_SRED, tufli(820, 1046, 1.0, GRAFIT, t))
    s += SL(Z_DAL, elka(1860, 1050, 300, t, 1.0, True, 223))
    s += SL(Z_SRED, girlyanda(200, 130, 1500, t, 10, 225, 50))
    s += SL(0, lampa_stolika(1700, 900, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def odno_plate_na_vseh_fotografiyah(t):
    """Стена с фотографиями разных лет: на каждой женщина в одном и том же
    платье в горошек, меняются только причёска и седина."""
    rnd = random.Random(3084)
    s = f'<rect width="{W}" height="{H}" fill="#241f1c"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 227))
    s += SL(Z_DAL, stena("oboi", t, 112))
    hod = A.seg(t, .3, 3.6)
    akt = min(3, int(hod * 4))
    for i in range(4):
        fx = 200 + (i % 2) * 760
        fy = 180 + (i // 2) * 420
        yar = 1.0 if i == akt else .55
        s += SL(Z_SRED, f'<rect x="{fx}" y="{fy}" width="620" height="360" rx="8"'
                        f' fill="{DEREVO2}" opacity="{yar:.2f}" {o(5)}/>')
        s += SL(Z_SRED, f'<rect x="{fx+24}" y="{fy+24}" width="572" height="312"'
                        f' fill="#8f99a6" opacity="{yar:.2f}"/>')
        # женщина в платье в горошек, без лица
        s += SL(Z_SRED, f'<g opacity="{yar:.2f}">'
                        f'<path d="M{fx+250},{fy+140} q60,-26 120,0 l40,196 h-200 Z"'
                        f' fill="{TSINIY}" {o(4)}/>')
        gor = "".join(f'<circle cx="{fx+252+rnd.randint(0,116)}"'
                      f' cy="{fy+150+rnd.randint(0,180)}" r="7" fill="{MOLOKO}"/>'
                      for _ in range(14))
        pr = ("#4a3528", "#4a3528", "#8d8a86", "#d8d8de")[i]
        s += SL(Z_SRED, gor + f'<circle cx="{fx+310}" cy="{fy+108}" r="40"'
                              f' fill="#f0cfae" {o(3)}/>'
                              f'<path d="M{fx+268},{fy+96} q42,-56 84,0 q-10,-34 -42,-36'
                              f' q-32,2 -42,36 Z" fill="{pr}" {o(3)}/></g>')
        if i == akt:
            s += SL(Z_SRED, teplo(fx + 310, fy + 180, 340, 230, .22))
    # комод, ваза, часы, салфетка
    s += SL(Z_SRED, f'<rect x="640" y="900" width="640" height="150" rx="10"'
                    f' fill="{DEREVO}" {o(6)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="{680+i*300}" y="940" width="260" height="60" rx="6"'
                        f' fill="{DEREVO2}" {o(4)}/>'
                        f'<circle cx="{810+i*300}" cy="970" r="12" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M900,900 q-30,-120 40,-126 q70,6 40,126 Z"'
                    f' fill="url(#glina)" {o(5)}/>')
    for i in range(6):
        a = -84 + i * 28 + 4 * A.w(t, 2.4, i * .3)
        s += SL(Z_SRED, f'<path d="M940,790 l{70*math.cos(math.radians(a)):.0f},'
                        f'{70*math.sin(math.radians(a)):.0f}" stroke="#6f7a52"'
                        f' stroke-width="5"/>')
    s += SL(Z_SRED, hodiki(1400, 820, t, 1.5))
    s += SL(Z_SRED, "".join(f'<path d="M{1180+i*22},900 q11,12 22,0" fill="none"'
                            f' stroke="{MOLOKO}" stroke-width="3" opacity=".6"/>'
                            for i in range(5)))
    s += SL(Z_SRED, girlyanda(100, 120, 1700, t, 11, 229, 48))
    s += SL(0, lampa_stolika(500, 880, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def spisok_naryadov_na_divane(t):
    """Диван под ёлкой: бабушка держит листок с четырьмя нарядами, дочь и
    внучка показывают на второй, бабушка — на первый и на себя."""
    rnd = random.Random(3085)
    s = f'<rect width="{W}" height="{H}" fill="#241c22"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 231))
    s += SL(Z_DAL, stena("oboi", t, 113))
    s += SL(Z_DAL, elka(1740, 1050, 520, t, 1.0, True, 233))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, f'<path d="M180,1040 q-40,-330 180,-340 h840 q220,10 180,340 Z"'
                    f' fill="#4a3a52" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="240" y="760" width="1080" height="90" rx="30"'
                    f' fill="#55435f" {o(5)}/>')
    s += SL(0, figura(480, 1000, 400, t, HVOYA, TEPLO_SVET, .4, False, False, 1.0,
                      1.5, True, True, "#f0cfae", True, MOLOKO, False))
    s += SL(0, figura(780, 1000, 420, t, TSINIY, TEPLO_SVET, .2, False, False, 1.0,
                      1.5, True, True, "#eec9a6", True, MOLOKO, False))
    s += SL(0, figura(1080, 1000, 360, t, KORALL, TEPLO_SVET, .7, False, False, 1.0,
                      2.0, True, True, "#f3d3b2", True, MOLOKO, False))
    # листок с четырьмя значками у бабушки
    lx, ly = 780, 780
    s += SL(0, f'<rect x="{lx-150}" y="{ly-110}" width="300" height="200" rx="10"'
               f' fill="{MOLOKO}" {o(5)}/>')
    for i in range(4):
        zx = lx - 110 + (i % 2) * 140
        zy = ly - 60 + (i // 2) * 90
        c = (VINO, RUBIN, TSINIY, IZUMRUD)[i]
        s += SL(0, f'<path d="M{zx-26},{zy-30} q26,-12 52,0 l12,70 h-76 Z"'
                   f' fill="{c}" {o(3)}/>')
    for sgn in (-1, 1):
        ruk, _ = rukav(780 + sgn * 70, 740, 110, 40 * sgn + 20, t, TSINIY, TEPLO_SVET,
                       .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
    # дочь и внучка тянутся ко второму значку
    ruk2, (h2x, h2y) = rukav(560, 760, 200, -18, t, HVOYA, TEPLO_SVET, .5, 5.0)
    s += SL(0, ruk2)
    ruk3, (h3x, h3y) = rukav(1000, 780, 190, -166, t, KORALL, TEPLO_SVET, .8, 5.0)
    s += SL(0, ruk3)
    s += SL(Z_SRED, kot(1320, 1000, t, 1.4, "#6b5a46"))
    s += SL(Z_SRED, f'<path d="M240,900 q120,-40 240,0 l0,120 q-120,40 -240,0 Z"'
                    f' fill="{KORALL}" opacity=".7"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<circle cx="{1400+i*70}" cy="1000" r="34" fill="{MED}" {o(3)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{200+i*60},1000 q28,-30 56,0 q-28,16 -56,0 Z"'
                        f' fill="{KREM2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1540" y="640" width="14" height="400" fill="{CHUGUN}" {o(3)}/>'
                    f'<path d="M1480,640 h134 l-20,-86 h-94 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, lampa_stolika(1547, 620, t, 1.4))
    s += SL(Z_SRED, girlyanda(200, 120, 1400, t, 10, 235, 48))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def muzhskoy_shkaf(t):
    """Строгий мужской шкаф раскрыт: три наряда с номерами, полка с рубашками,
    галстуки, ботинки. Муж чешет затылок, жена-силуэт в дверях."""
    rnd = random.Random(3086)
    s = f'<rect width="{W}" height="{H}" fill="#1e1a18"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 237))
    s += SL(Z_DAL, stena("kraska", t, 114))
    s += SL(Z_DAL, shkaf(560, 1050, 1120, 1000, t, 1.0, False))
    s += SL(Z_SRED, perekladina(1080, 260, 920))
    s += SL(Z_SRED, polovicy(1050))
    for i, (c, pl) in enumerate(((MOLOKO, False), (TERRAKOT, False), (TSINIY, False))):
        px = 760 + i * 300
        s += SL(Z_SRED, naryad_plechiki(px, 280, 460, t, c, 1.15, i * .25, pl, MOLOKO, .04, 240 + i))
        p = A.out(A.seg(t, .4 + i * .35, .5))
        s += SL(Z_SRED, f'<circle cx="{px}" cy="220" r="30" fill="{ZOLOTO}"'
                        f' opacity="{p*.95:.2f}" {o(3)}/>')
    s += SL(Z_SRED, polka(640, 880, 360))
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="660" y="{840-i*22}" width="320" height="20" rx="5"'
                        f' fill="{(MOLOKO, KREM2, MOLOKO, BEZH)[i]}" {o(3)}/>')
    gal = ""
    for i in range(5):
        gx = 1480 + i * 52
        kach = 3.6 * A.w(t, 2.3, i * .3)
        c = (VINO, TSINIY, GRAFIT, HVOYA, TERRAKOT)[i]
        gal += (f'<g transform="rotate({kach:.2f} {gx} 420)">'
                f'<path d="M{gx-11},420 l22,0 l-5,130 h-12 Z" fill="{c}" {o(3)}/></g>')
    s += SL(Z_SRED, gal)
    s += SL(Z_SRED, f'<rect x="640" y="960" width="420" height="90" rx="8"'
                    f' fill="#2a2420" {o(4)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<path d="M{680+i*180},1040 q10,-56 70,-58 q60,2 70,58 Z"'
                        f' fill="#2b2420" {o(4)}/>')
    # муж в халате чешет затылок
    s += SL(0, figura(320, 1050, 520, t, "#6a4a3a", TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", False, MOLOKO, True))
    ruk, (hx, hy) = rukav(390, 740, 150, -104 + 10 * A.w(t, 1.5), t, "#6a4a3a",
                          TEPLO_SVET, .2, 6.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(250, 790, 120, 36, t, "#6a4a3a", TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    # жена-силуэт в дверях
    s += SL(Z_DAL, f'<rect x="1760" y="220" width="160" height="830" rx="8"'
                   f' fill="#161218" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1840" cy="760" rx="52" ry="150" fill="#14111a"'
                    f' opacity=".9"/><circle cx="1840" cy="600" r="40" fill="#14111a"'
                    f' opacity=".9"/>')
    s += SL(0, lampa_stolika(240, 560, t, 1.5))
    s += SL(Z_SRED, teplo(300, 600, 420, 380, .28 + .08 * abs(A.w(t, 1.8))))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def bordovyy_galstuk(t):
    """Вешалка с галстуками: рукав откладывает ярко-красный и берёт бордовый —
    глубокий и тёмный."""
    rnd = random.Random(3087)
    s = f'<rect width="{W}" height="{H}" fill="#201b1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 239))
    s += SL(Z_DAL, stena("paneli", t, 115))
    s += SL(Z_DAL, _mel_polka(1440, 300, 420, t, 87, 7))
    s += SL(Z_SRED, f'<rect x="200" y="240" width="1100" height="20" rx="9"'
                    f' fill="{SEREBRO}" {o(5)}/>')
    CV = (SERYY, TSINIY, "#6b5347", GRAFIT, TSINIY, "#5c4a3f", VINO)
    ot = A.out(A.seg(t, .3, 1.2))
    vz = A.out(A.seg(t, 1.1, 1.2))
    for i, c in enumerate(CV):
        gx = 280 + i * 150
        kach = 4.0 * A.w(t, 2.2, i * .25)
        dy = 0
        if i == 2:                       # ярко-красный откладывается
            c = "#e03a3a"
            dy = 240 * ot
        if i == 6 and vz > .05:          # бордовый поднимается
            dy = -160 * vz
        s += SL(0, f'<g transform="rotate({kach:.2f} {gx} 260) translate(0,{dy:.0f})">'
                   f'<path d="M{gx-10},260 l20,0 l-6,120 l34,180 l-72,0 l34,-180 Z"'
                   f' fill="{c}" {o(4)}/>'
                   f'<path d="M{gx-10},260 l20,0 l-4,30 l-12,0 Z" fill="#ffffff"'
                   f' opacity=".22"/></g>')
    ruk, _ = rukav(1520, 520, 280, 176 - 26 * vz, t, GRAFIT, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    s += SL(Z_SRED, zerkalo(120, 420, 300, 560, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="134" y="434" width="272" height="532" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="920" rx="120" ry="40" fill="{MOLOKO}" {o(5)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{700+i*40}" cy="912" r="14" fill="{ZOLOTO}"'
                        f' opacity="{.6+.4*abs(A.w(t,1.9,i*.3)):.2f}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="980" y="880" width="120" height="70" rx="10"'
                    f' fill="{STEKLO}" opacity=".7" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1180,950 q70,-30 130,-4 l-10,56 q-62,22 -120,-6 Z"'
                    f' fill="{DEREVO2}" {o(4)}/>')
    s += SL(Z_SRED, naryad_plechiki(1680, 560, 400, t, MOLOKO, 1.1, .4, False, None, .05, 243))
    s += SL(Z_SRED, girlyanda(200, 140, 1500, t, 10, 245, 48))
    s += SL(0, lampa_stolika(560, 880, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def muzhskoy_podium(t):
    """Мужской подиум: четыре манекенщика-силуэта, бордовый пиджак подсвечен."""
    rnd = random.Random(3088)
    s = f'<rect width="{W}" height="{H}" fill="#14121a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 247))
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="620" fill="#1b1822"/>')
    sof = ""
    for i in range(7):
        sx = 160 + i * 270
        mig = .45 + .55 * (0.5 + 0.5 * math.cos(2 * math.pi * ((t * 1.3 + i * .2) % 1.0)))
        sof += (f'<path d="M{sx-40},60 h80 l20,70 h-120 Z" fill="{CHUGUN}" {o(3)}/>'
                f'<path d="M{sx},130 l-90,280 h180 Z" fill="{ZOLOTO}"'
                f' opacity="{.10*mig:.2f}"/>'
                f'<circle cx="{sx}" cy="132" r="16" fill="{ZOLOTO}" opacity="{mig:.2f}"/>')
    s += SL(Z_DAL, sof)
    s += SL(Z_SRED, f'<path d="M0,900 h{W} l-140,180 h-1640 Z" fill="#2a2630" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M0,900 h{W}" stroke="{ZOLOTO}" stroke-width="6" opacity=".5"/>')
    hod = A.seg(t, .1, 4.0)
    COL = ("#6b5347", BEZH, "#7a5a3a", "#5e1226")
    for i, c in enumerate(COL):
        p = (hod + i * .25) % 1.0
        mx = 180 + 1500 * p
        sh = 10 * math.sin(p * 18)
        yar = 1.0 if i == 3 else .85
        s += SL(0, f'<g opacity="{yar:.2f}">'
                   f'<path d="M{mx-56:.0f},900 q56,-40 112,0 l-16,-330 h-80 Z"'
                   f' fill="{c}" {o(5)}/>'
                   f'<circle cx="{mx:.0f}" cy="536" r="38" fill="#2a2228" {o(3)}/>'
                   f'<path d="M{mx-40+sh:.0f},900 l10,-130 M{mx+40-sh:.0f},900 l-10,-130"'
                   f' stroke="{c}" stroke-width="26" stroke-linecap="round"/></g>')
        if i == 3:
            s += SL(0, teplo(mx, 700, 300, 320, .30 + .10 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, _zriteli_pod(80, 1000, 12, t, 249, 150))
    vsp = 1.0 if (t % 1.7) < .14 else .0
    s += SL(Z_SRED, f'<rect x="0" y="600" width="{W}" height="480" fill="#ffffff"'
                    f' opacity="{vsp*.18:.2f}"/>')
    s += SL(Z_SRED, girlyanda(60, 70, 1800, t, 14, 251, 40))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.48)
    return s


def svetlaya_rubashka_na_plechikah(t):
    """Светлая выглаженная рубашка на ручке двери, за дверью — комната с ёлкой
    и накрытым столом."""
    rnd = random.Random(3089)
    s = f'<rect width="{W}" height="{H}" fill="#241f1b"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 253))
    s += SL(Z_DAL, stena("oboi", t, 117))
    # дверь приоткрыта: за ней праздничная комната
    s += SL(Z_DAL, f'<rect x="1100" y="120" width="700" height="930" rx="10"'
                   f' fill="#2d2129" {o(6)}/>')
    s += SL(Z_DAL, elka(1620, 1000, 480, t, 1.0, True, 255))
    s += SL(Z_DAL, f'<rect x="1140" y="760" width="420" height="40" rx="8"'
                   f' fill="{MOLOKO}" {o(4)}/>')
    s += SL(Z_DAL, "".join(f'<ellipse cx="{1200+i*110}" cy="756" rx="42" ry="14"'
                           f' fill="{KREM2}" {o(2)}/>' for i in range(4)))
    s += SL(Z_DAL, svecha(1320, 752, t, .2, 1.2))
    s += SL(Z_SRED, dver(760, 100, 420, 950, .0, "url(#derev)", True, False))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, naryad_plechiki(600, 300, 560, t, MOLOKO, 1.5, .1, False, KREM2, .06, 256, 2.0))
    s += SL(0, f'<path d="M520,330 h160 l0,40 h-160 Z" fill="{KREM2}" {o(3)}/>')
    # гладильная доска, утюг, стул, тапки, кот
    s += SL(Z_SRED, f'<path d="M80,860 l300,-34 l10,70 l-300,34 Z" fill="{MOLOKO}" {o(6)}/>'
                    f'<path d="M130,930 l0,120 M330,906 l0,144" stroke="{SEREBRO}"'
                    f' stroke-width="9"/>')
    s += SL(Z_SRED, f'<path d="M180,840 q60,-44 118,-6 l6,32 l-130,16 Z"'
                    f' fill="{CHUGUN}" {o(5)}/>')
    s += SL(Z_SRED, par(240, 820, t, 4, .5, 150, .45, 1.0))
    s += SL(Z_SRED, f'<rect x="420" y="880" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="430" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="562" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{300+i*80},1040 q30,-34 62,0 q-30,20 -62,0 Z"'
                            f' fill="{KORALL}" {o(3)}/>' for i in range(2)))
    kx = 300 + 420 * A.seg(t, .4, 2.6)
    s += SL(Z_SRED, kot(kx, 1046, t, 1.3, "#6b5a46"))
    s += SL(Z_SRED, girlyanda(100, 130, 900, t, 8, 257, 46))
    s += SL(0, lampa_stolika(900, 860, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def kardigan_s_shalevym_vorotnikom(t):
    """Мужской торс в светлой рубашке: винный джемпер сменяется тёмно-зелёным
    кардиганом. В застеклённой дверце шкафа — настоящая шерстяная вязка."""
    rnd = random.Random(3090)
    s = f'<rect width="{W}" height="{H}" fill="#1f1b1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 259))
    s += SL(Z_DAL, stena("kraska", t, 118))
    px, py, pw, ph = 120, 300, 760, 300
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#1b2a22"/>'
            + otrez(px + 24, py + 30, pw - 48, ph - 70, HVOYA, t, 261, 0, .2)
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-14}" y="{py-14}" width="{pw+28}" height="{ph+28}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="22"/>'
            + f'<path d="M{px+pw/2:.0f},{py-14} l0,{ph+28}" stroke="{DEREVO2}"'
              f' stroke-width="12"/>')
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, manekken(1240, 1000, 620, t, KREM2, "m", MOLOKO, .2, None, .04, 262))
    faza = A.seg(t, .3, 3.0)
    dzh = max(0.0, min(1.0, faza * 2.4))
    kard = max(0.0, min(1.0, (faza - .5) * 2.6))
    if kard < .1:
        s += SL(0, f'<path d="M1100,{520-90*(1-dzh):.0f} h280 l20,300 h-320 Z"'
                   f' fill="{VINO}" opacity="{dzh:.2f}" {o(6)}/>')
    else:
        s += SL(0, f'<path d="M1100,{520-70*(1-kard):.0f} h280 l24,310 h-328 Z"'
                   f' fill="{HVOYA}" opacity="{kard:.2f}" {o(6)}/>')
        s += SL(0, f'<path d="M1180,{520-70*(1-kard):.0f} q60,120 0,220'
                   f' M1300,{520-70*(1-kard):.0f} q-60,120 0,220" fill="none"'
                   f' stroke="#17382b" stroke-width="40" opacity="{kard:.2f}"/>')
    vyaz = ""
    for i in range(10):
        vyaz += (f'<path d="M{1120+i*28},560 q14,30 0,60 q-14,30 0,60" fill="none"'
                 f' stroke="#0f2a20" stroke-width="3" opacity=".5"/>')
    s += SL(0, vyaz)
    s += SL(Z_SRED, naryad_plechiki(1700, 420, 420, t, GRAFIT, 1.1, .4, False, None, .04, 263))
    s += SL(Z_SRED, f'<rect x="900" y="880" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="910" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1042" y="906" width="18" height="144" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{620+i*150},1040 q14,-62 76,-64 q62,2 76,64 Z"'
                            f' fill="#2b2420" {o(4)}/>' for i in range(2)))
    s += SL(Z_SRED, zerkalo(1760, 320, 140, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(200, 130, 1500, t, 10, 265, 46))
    s += SL(0, lampa_stolika(960, 760, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def bryuki_noski_i_botinki(t):
    """Стул у стены: брюки со стрелками, тёмные носки, начищенные ботинки, в
    которых отражается ёлка; белые носки отодвигает рукав."""
    rnd = random.Random(3091)
    s = f'<rect width="{W}" height="{H}" fill="#1e1b1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 267))
    s += SL(Z_DAL, stena("paneli", t, 119))
    s += SL(Z_DAL, elka(1780, 1050, 400, t, 1.0, True, 269))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, f'<rect x="560" y="520" width="420" height="40" rx="10"'
                    f' fill="{DEREVO}" {o(6)}/>'
                    f'<rect x="580" y="560" width="30" height="480" fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="930" y="560" width="30" height="480" fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="560" y="700" width="420" height="34" rx="8"'
                    f' fill="{DEREVO2}" {o(5)}/>')
    # брюки со стрелками на спинке
    s += SL(0, f'<path d="M600,540 h340 l-30,460 h-120 l-40,-300 l-40,300 h-120 Z"'
               f' fill="{GRAFIT}" {o(7)}/>')
    for sx in (700, 840):
        s += SL(0, f'<path d="M{sx},560 l-10,420" stroke="#ffffff" stroke-width="4"'
                   f' opacity="{.5+.4*abs(A.w(t, 2.2, sx*.001)):.2f}"/>')
    # носки на сиденье
    s += SL(0, f'<path d="M640,700 q60,-26 120,0 l-10,66 q-50,20 -100,0 Z"'
               f' fill="#2a2a32" {o(4)}/>')
    s += SL(0, f'<path d="M790,700 q60,-26 120,0 l-10,66 q-50,20 -100,0 Z"'
               f' fill="#2a2a32" {o(4)}/>')
    # ботинки под стулом, в них отражается ёлка
    for i in range(2):
        bx = 640 + i * 190
        s += SL(0, f'<path d="M{bx},1020 q14,-80 90,-82 q76,2 90,82 Z"'
                   f' fill="#2b2420" {o(6)}/>')
        s += SL(0, f'<path d="M{bx+40},960 q40,-30 80,-6" fill="none" stroke="{HVOYA}"'
                   f' stroke-width="9" opacity="{.4+.4*abs(A.w(t,1.8,i*.3)):.2f}"/>')
        s += SL(0, f'<circle cx="{bx+70}" cy="948" r="7" fill="{ZOLOTO}"'
                   f' opacity="{.5+.5*abs(A.w(t,1.4,i*.4)):.2f}"/>')
    # белые носки отодвигаются рукавом
    ot = A.out(A.seg(t, .4, 1.3))
    s += SL(0, f'<g transform="translate({260*ot:.0f},0)">'
               f'<path d="M1080,980 q60,-26 120,0 l-10,66 q-50,20 -100,0 Z"'
               f' fill="{MOLOKO}" {o(4)}/>'
               f'<path d="M1210,980 q60,-26 120,0 l-10,66 q-50,20 -100,0 Z"'
               f' fill="{MOLOKO}" {o(4)}/></g>')
    ruk, _ = rukav(1120, 700, 240, 70 - 20 * ot, t, GRAFIT, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    s += SL(Z_SRED, f'<path d="M1480,1010 q70,-40 130,-6 l-12,56 q-60,26 -118,-6 Z"'
                    f' fill="{DEREVO2}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1640" y="960" width="110" height="80" rx="12"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="1000" width="300" height="50" rx="10"'
                    f' fill="#5a4038" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{180+i*86},1040 q30,-34 62,0 q-30,20 -62,0 Z"'
                            f' fill="{KORALL}" {o(3)}/>' for i in range(2)))
    s += SL(Z_SRED, girlyanda(200, 130, 1400, t, 10, 271, 46))
    s += SL(0, lampa_stolika(1300, 560, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def muzh_v_vyglazhennoy_rubashke_za_st(t):
    """Праздничный стол: муж в светлой рубашке и винном джемпере, жена
    поправляет ему воротник; галстук висит на спинке стула нетронутый."""
    rnd = random.Random(3092)
    s = f'<rect width="{W}" height="{H}" fill="#241c20"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 273))
    s += SL(Z_DAL, stena("doski", t, 120))
    s += SL(Z_DAL, elka(1800, 1050, 440, t, 1.0, True, 275))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, stol(120, 900, 1400, 46))
    s += SL(Z_SRED, f'<path d="M110,860 h1420 l-26,180 q-690,40 -1370,0 Z"'
                    f' fill="{MOLOKO}" {o(5)}/>')
    s += SL(Z_SRED, "".join(f'<ellipse cx="{260+i*220}" cy="866" rx="64" ry="20"'
                            f' fill="{KREM2}" {o(3)}/>' for i in range(6)))
    s += SL(Z_SRED, svecha(640, 862, t, .1, 1.3) + svecha(1080, 862, t, .5, 1.2))
    s += SL(Z_SRED, f'<path d="M880,860 q-26,-120 40,-126 q66,6 40,126 Z"'
                    f' fill="{STEKLO}" opacity=".7" {o(3)}/>')
    s += SL(Z_SRED, "".join(f'<circle cx="{1240+i*62}" cy="856" r="30" fill="{MED}"'
                            f' {o(3)}/>' for i in range(3)))
    # муж сидит прямо, обе руки на столе
    s += SL(0, figura(640, 880, 460, t, VINO, TEPLO_SVET, .2, False, False, 1.0,
                      1.0, True, True, "#f0cfae", False, MOLOKO, False))
    s += SL(0, f'<path d="M560,640 h160 l0,120 h-160 Z" fill="{MOLOKO}" {o(4)}/>')
    for sgn in (-1, 1):
        ruk, _ = rukav(640 + sgn * 74, 700, 150, 38 - sgn * 8, t, VINO, TEPLO_SVET,
                       .2 + (0 if sgn < 0 else .3), 3.0)
        s += SL(0, ruk)
    # жена поправляет воротник
    s += SL(0, figura(980, 900, 450, t, VINO, TEPLO_SVET, .5, False, False, 1.0,
                      1.5, True, True, "#eec9a6", True, MOLOKO, False))
    ruk, (hx, hy) = rukav(900, 700, 200, -168 + 8 * A.w(t, 1.7), t, VINO, TEPLO_SVET,
                          .4, 5.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(1050, 720, 140, -140, t, VINO, TEPLO_SVET, .7, 4.0)
    s += SL(0, ruk2)
    # галстук на спинке стула, нетронутый
    s += SL(Z_SRED, f'<rect x="420" y="760" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>')
    kach = 3.4 * A.w(t, 2.4, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.2f} 500 786)">'
                    f'<path d="M488,786 l24,0 l-6,120 l28,140 h-68 l28,-140 Z"'
                    f' fill="{TSINIY}" {o(4)}/></g>')
    s += SL(Z_SRED, girlyanda(140, 120, 1500, t, 11, 277, 46))
    s += SL(0, lampa_stolika(1620, 760, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def dzhemper_s_vyrezom_ugolkom(t):
    """Полка со стопкой джемперов: муж вытягивает джемпер с вырезом уголком и
    надевает его поверх рубашки — воротник ложится в вырез ровно."""
    rnd = random.Random(3093)
    s = f'<rect width="{W}" height="{H}" fill="#201c1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 279))
    s += SL(Z_DAL, stena("oboi", t, 121))
    s += SL(Z_DAL, shkaf(820, 1050, 1000, 960, t, .95, False))
    s += SL(Z_SRED, polka(900, 620, 760))
    s += SL(Z_SRED, polovicy(1050))
    vyt = A.out(A.seg(t, .3, 1.4))
    for i in range(5):
        c = (GRAFIT, TSINIY, HVOYA, BEZH, VINO)[i]
        dy = 0 if i != 2 else -120 * vyt
        dx = 0 if i != 2 else 260 * vyt
        s += SL(Z_SRED, f'<rect x="{940+dx:.0f}" y="{580-i*34+dy:.0f}" width="520"'
                        f' height="30" rx="8" fill="{c}" {o(4)}/>')
    # джемпер на плечиках поверх рубашки
    s += SL(0, naryad_plechiki(520, 300, 520, t, MOLOKO, 1.4, .1, False, KREM2, .05, 281, 1.6))
    nad = A.out(A.seg(t, 1.1, 1.3))
    if nad > .05:
        s += SL(0, f'<path d="M400,{400-60*(1-nad):.0f} h240 l24,330 h-288 Z"'
                   f' fill="{HVOYA}" opacity="{nad:.2f}" {o(6)}/>')
        s += SL(0, f'<path d="M480,{400-60*(1-nad):.0f} l40,80 l40,-80 Z"'
                   f' fill="{MOLOKO}" opacity="{nad:.2f}" {o(3)}/>')
    # муж: правая рука тянет джемпер, левая придерживает стопку
    s += SL(0, figura(1300, 1050, 530, t, "#4a4440", TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", False, MOLOKO, True))
    ruk, _ = rukav(1220, 740, 250, -170 + 14 * vyt, t, "#4a4440", TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(1380, 760, 180, -150, t, "#4a4440", TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    # пустой пакет на стуле, в него лезет кот
    s += SL(Z_SRED, f'<rect x="1560" y="820" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="1570" y="846" width="18" height="200" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1702" y="846" width="18" height="200" fill="{DEREVO}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M1580,800 h130 l14,160 h-158 Z" fill="{KREM2}" {o(5)}/>')
    kp = A.out(A.seg(t, 1.6, 1.2))
    s += SL(Z_SRED, kot(1646, 800 + 60 * kp, t, 1.1, "#6b5a46"))
    s += SL(Z_SRED, zerkalo(80, 300, 180, 560, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(300, 130, 1300, t, 9, 283, 46))
    s += SL(0, lampa_stolika(760, 900, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def noski_pod_stolom(t):
    """Вид под праздничный стол: у левого короткие носки и белая полоска кожи,
    у правого длинные в тон брюкам — галочка."""
    rnd = random.Random(3094)
    s = f'<rect width="{W}" height="{H}" fill="#1d1a18"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 285))
    s += SL(Z_DAL, doski(0, 0, W, 460, 80))
    s += SL(Z_SRED, polovicy(900))
    kach = 6 * A.w(t, 2.0, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach*.06:.2f} 960 200)">'
                    f'<path d="M0,120 h{W} l-40,300 q-920,60 -1840,0 Z" fill="{MOLOKO}"'
                    f' {o(6)}/></g>')
    for i in range(4):
        nx = 260 + i * 460
        s += SL(Z_SRED, f'<rect x="{nx}" y="420" width="26" height="480"'
                        f' fill="{DEREVO}" {o(4)}/>')
    # левый: короткие носки, полоска кожи, красная черта
    for sgn in (-1, 1):
        lx = 600 + sgn * 90
        s += SL(0, f'<rect x="{lx-44}" y="430" width="88" height="260" rx="14"'
                   f' fill="{GRAFIT}" {o(5)}/>')
        s += SL(0, f'<rect x="{lx-40}" y="690" width="80" height="50" rx="8"'
                   f' fill="#f0cfae" {o(3)}/>')
        s += SL(0, f'<rect x="{lx-42}" y="740" width="84" height="80" rx="10"'
                   f' fill="#2a2a32" {o(4)}/>')
        s += SL(0, f'<path d="M{lx-54},900 q14,-80 54,-82 q40,2 54,82 Z"'
                   f' fill="#2b2420" {o(5)}/>')
    s += SL(0, f'<path d="M460,660 l280,0" stroke="#d13a3a" stroke-width="14"'
               f' opacity=".9"/>')
    # правый: длинные носки в тон, галочка
    for sgn in (-1, 1):
        rx = 1340 + sgn * 90
        s += SL(0, f'<rect x="{rx-44}" y="430" width="88" height="300" rx="14"'
                   f' fill="{GRAFIT}" {o(5)}/>')
        s += SL(0, f'<rect x="{rx-42}" y="700" width="84" height="120" rx="10"'
                   f' fill="{GRAFIT}" {o(4)}/>')
        s += SL(0, f'<path d="M{rx-54},900 q14,-80 54,-82 q40,2 54,82 Z"'
                   f' fill="#2b2420" {o(5)}/>')
    p = A.out(A.seg(t, .4, .5))
    s += SL(0, f'<path d="M1240,620 l34,42 l66,-88" fill="none" stroke="#3fae62"'
               f' stroke-width="18" stroke-linecap="round" opacity="{p:.2f}"/>')
    # кот катает мандарин, упавшая салфетка, тапки
    mx = 900 + 220 * A.seg(t, .3, 2.6)
    s += SL(Z_SRED, kot(760, 900, t, 1.4, "#3b3430"))
    s += SL(Z_SRED, f'<circle cx="{mx:.0f}" cy="880" r="34" fill="{MED}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1560,900 q70,-40 130,-10 l-20,60 q-70,24 -120,-6 Z"'
                    f' fill="{MOLOKO}" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{1720+i*90},900 q30,-34 62,0 q-30,20 -62,0 Z"'
                            f' fill="{KORALL}" {o(3)}/>' for i in range(2)))
    s += SL(Z_SRED, girlyanda(60, 60, 1800, t, 12, 287, 36))
    s += SL(0, lampa_stolika(200, 880, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def mat_gladit_beluyu_rubashku(t):
    """Комната, утро: мать ведёт тяжёлый утюг по рукаву белой рубашки,
    разложенной на одеяле вместо доски."""
    rnd = random.Random(3095)
    s = f'<rect width="{W}" height="{H}" fill="#2a2520"/>'
    s += SL(Z_NEBO, nebo("rassv", t, False, 289))
    s += SL(Z_DAL, stena("paneli", t, 123))
    s += SL(Z_DAL, okno_izby(1420, 160, 420, 400, t, svet=False, moroz=.55))
    s += SL(Z_DAL, elka(120, 1050, 330, t, 1.0, True, 291))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, stol(360, 980, 1000, 46))
    s += SL(Z_SRED, f'<path d="M350,900 h1020 l-20,100 q-500,30 -1000,0 Z"'
                    f' fill="#7b6a58" {o(5)}/>')
    # белая рубашка крупно
    s += SL(0, f'<path d="M520,700 h520 l40,200 h-600 Z" fill="{MOLOKO}" {o(7)}/>')
    s += SL(0, f'<path d="M520,700 l-140,70 l40,80 l120,-60 Z" fill="{MOLOKO}" {o(5)}/>')
    s += SL(0, f'<path d="M1040,700 l140,70 l-40,80 l-120,-60 Z" fill="{MOLOKO}" {o(5)}/>')
    s += SL(0, f'<path d="M740,700 q40,50 80,0" fill="none" stroke="{K}"'
               f' stroke-width="5" opacity=".5"/>')
    # утюг идёт по рукаву
    p = A.seg(t, .3, 2.2)
    ux = 420 + 620 * p
    s += SL(0, f'<path d="M{ux-70:.0f},780 q70,-50 140,-6 l8,38 l-156,18 Z"'
               f' fill="{CHUGUN}" {o(6)}/>')
    s += SL(0, f'<path d="M{ux-40:.0f},740 q40,-44 80,-4" fill="none" stroke="{DEREVO2}"'
               f' stroke-width="18" stroke-linecap="round"/>')
    s += SL(0, par(ux, 720, t, 5, .55, 180, .5, 1.1))
    # мать: правая рука ведёт утюг, левая расправляет ткань
    s += SL(0, figura(560, 1050, 540, t, "#8a6a55", TEPLO_SVET, .2, True, False, 1.0,
                      3.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, _ = rukav(650, 760, 230, 10 + 10 * p, t, "#8a6a55", TEPLO_SVET, .2, 4.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(480, 790, 190, 30, t, "#8a6a55", TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    s += SL(Z_SRED, f'<path d="M1480,900 q-24,-80 34,-84 q58,4 34,84 Z"'
                    f' fill="{STEKLO}" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1240,880 q60,-26 120,0 l-10,54 q-50,20 -100,0 Z"'
                    f' fill="{MOLOKO}" opacity=".7" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1600" y="820" width="180" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>')
    s += SL(Z_SRED, plechiki(1690, 846, 1.2, "#7a5a3a", t, .2))
    s += SL(Z_SRED, f'<rect x="1560" y="620" width="230" height="120" rx="10"'
                    f' fill="{DEREVO2}" {o(5)}/>'
                    f'<circle cx="1620" cy="680" r="32" fill="#2b2b2b" {o(3)}/>')
    s += SL(Z_SRED, girlyanda(300, 130, 1100, t, 9, 293, 46))
    s += SL(0, lampa_stolika(1200, 640, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def otec_gladit_bryuki_cherez_marlyu(t):
    """Тот же стол: отец гладит брюки через влажную марлю, из-под неё валит
    пар; стрелка выходит острая, как лезвие."""
    rnd = random.Random(3096)
    s = f'<rect width="{W}" height="{H}" fill="#2a2520"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 295))
    s += SL(Z_DAL, stena("paneli", t, 124))
    s += SL(Z_DAL, elka(1840, 1050, 300, t, 1.0, True, 297))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, stol(300, 980, 1100, 46))
    s += SL(Z_SRED, f'<path d="M290,900 h1120 l-20,100 q-550,30 -1100,0 Z"'
                    f' fill="#7b6a58" {o(5)}/>')
    # брюки на столе
    s += SL(0, f'<path d="M520,740 h420 l-40,170 h-120 l-50,-110 l-50,110 h-120 Z"'
               f' fill="{GRAFIT}" {o(7)}/>')
    # марля расстилается и снимается
    rast = A.out(A.seg(t, .25, 1.1))
    snyat = A.out(A.seg(t, 1.7, .9))
    if snyat < .1:
        s += SL(0, f'<rect x="520" y="740" width="{420*rast:.0f}" height="170"'
                   f' fill="{MOLOKO}" opacity=".55"/>')
    else:
        s += SL(0, f'<rect x="{520+420*snyat:.0f}" y="{740-90*snyat:.0f}"'
                   f' width="{420*(1-snyat):.0f}" height="170" fill="{MOLOKO}"'
                   f' opacity="{.55*(1-snyat):.2f}"/>')
        s += SL(0, f'<path d="M700,740 l-20,170" stroke="#ffffff" stroke-width="5"'
                   f' opacity="{snyat:.2f}"/>')
    s += SL(0, par(720, 730, t, 6, .6, 200, .55, 1.2))
    s += SL(0, f'<path d="M640,700 q60,-46 120,-6 l8,36 l-136,16 Z" fill="{CHUGUN}" {o(6)}/>')
    # отец в майке и трико
    s += SL(0, figura(430, 1050, 540, t, "#6b6a66", TEPLO_SVET, .2, False, False, 1.0,
                      2.5, True, True, "#eec9a6", False, None, True))
    ruk, _ = rukav(520, 760, 210, 6, t, "#6b6a66", TEPLO_SVET, .2, 4.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(500, 820, 180, 28, t, "#6b6a66", TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    # часы пробегают ночь
    s += SL(Z_SRED, hodiki(1560, 300, t, 1.8))
    beg = -90 + 720 * A.seg(t, .3, 3.0)
    s += SL(Z_SRED, f'<path d="M1560,300 l{50*math.cos(math.radians(beg)):.0f},'
                    f'{50*math.sin(math.radians(beg)):.0f}" stroke="{K}"'
                    f' stroke-width="6" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M1300,900 q-24,-80 34,-84 q58,4 34,84 Z"'
                    f' fill="{STEKLO}" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1180,1046 q-20,-130 58,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1600" y="820" width="180" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>')
    s += SL(Z_SRED, plechiki(1690, 846, 1.1, "#7a5a3a", t, .4))
    s += SL(Z_SRED, girlyanda(200, 120, 1400, t, 10, 299, 44))
    s += SL(0, lampa_stolika(1000, 620, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def kostyum_na_vyhod(t):
    """Шкаф, в нём один тёмный костюм, рядом спецовка и телогрейка; на дверце
    листки календаря, и над каждым праздником тот же костюм."""
    rnd = random.Random(3097)
    s = f'<rect width="{W}" height="{H}" fill="#201c19"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 301))
    s += SL(Z_DAL, stena("oboi", t, 125))
    s += SL(Z_DAL, shkaf(220, 1050, 1000, 980, t, 1.0, False))
    s += SL(Z_SRED, perekladina(720, 280, 860))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, naryad_plechiki(560, 300, 560, t, GRAFIT, 1.5, .1, False, MOLOKO, .05, 303, 1.4))
    s += SL(Z_SRED, naryad_plechiki(880, 310, 460, t, "#4a5a4a", 1.1, .3, False, None, .0, 304))
    s += SL(Z_SRED, naryad_plechiki(1080, 310, 440, t, "#5a4a3a", 1.1, .6, False, None, .0, 305))
    # листки календаря на дверце
    hod = A.seg(t, .3, 3.2)
    for i in range(4):
        lx = 1360 + (i % 2) * 230
        ly = 300 + (i // 2) * 300
        akt = (int(hod * 4) == i)
        s += SL(Z_SRED, f'<rect x="{lx}" y="{ly}" width="200" height="240" rx="8"'
                        f' fill="{MOLOKO}" opacity="{1.0 if akt else .6:.2f}" {o(4)}/>')
        s += SL(Z_SRED, f'<rect x="{lx}" y="{ly}" width="200" height="50" rx="8"'
                        f' fill="{KORALL}" opacity="{1.0 if akt else .6:.2f}"/>')
        s += SL(Z_SRED, f'<path d="M{lx+60},{ly+110} q40,-20 80,0 l16,100 h-112 Z"'
                        f' fill="{GRAFIT}" opacity="{1.0 if akt else .5:.2f}" {o(3)}/>')
        if akt:
            s += SL(Z_SRED, teplo(lx + 100, ly + 130, 200, 180, .24))
    s += SL(Z_SRED, polka(700, 220, 420))
    s += SL(Z_SRED, f'<path d="M820,220 q90,-60 180,0 q-50,26 -90,26 q-40,0 -90,-26 Z"'
                    f' fill="#4a3f38" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{700+i*170},1040 q14,-60 72,-62 q58,2 72,62 Z"'
                            f' fill="#2b2420" {o(4)}/>' for i in range(2)))
    s += SL(Z_SRED, f'<path d="M1120,1000 q40,-26 80,-4 l-8,46 q-38,16 -76,-4 Z"'
                    f' fill="{DEREVO2}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1240" cy="960" rx="40" ry="26" fill="{MOLOKO}"'
                    f' opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, girlyanda(260, 130, 1400, t, 10, 307, 46))
    s += SL(0, lampa_stolika(1700, 900, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def galstuk_na_rezinke_i_botinki(t):
    """Прихожая: сын натягивает галстук на резинке, отец полирует ботинок
    бархатной тряпочкой. В окошке обувного шкафчика — настоящая чистка."""
    rnd = random.Random(3098)
    s = f'<rect width="{W}" height="{H}" fill="#241e1b"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 309))
    s += SL(Z_DAL, stena("kirpich", t, 126))
    px, py, pw, ph = 1060, 700, 760, 300
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#1b1714"/>'
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-14}" y="{py-14}" width="{pw+28}" height="{ph+28}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="22"/>')
    s += SL(Z_SRED, polovicy(1050))
    # сын натягивает галстук на резинке
    s += SL(0, figura(420, 1050, 430, t, TSINIY, TEPLO_SVET, .2, False, False, 1.0,
                      2.5, True, True, "#f3d3b2", False, MOLOKO, True))
    nat = A.seg(t, .3, 1.6)
    shelk = 1.0 if (t % 1.9) > 1.75 else 0.0
    for sgn in (-1, 1):
        ruk, _ = rukav(420 + sgn * 70, 740, 150, -96 - sgn * 14 + 26 * nat, t,
                       TSINIY, TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M400,{700-70*nat+16*shelk:.0f} l40,0 l-8,130 l34,120 h-92'
               f' l34,-120 Z" fill="{VINO}" {o(4)}/>')
    # отец на табурете полирует ботинок
    s += SL(0, f'<rect x="700" y="880" width="220" height="30" rx="8"'
               f' fill="{DEREVO}" {o(5)}/>'
               f'<rect x="712" y="910" width="20" height="140" fill="{DEREVO}" {o(4)}/>'
               f'<rect x="888" y="910" width="20" height="140" fill="{DEREVO}" {o(4)}/>')
    s += SL(0, figura(810, 880, 420, t, "#4a4440", TEPLO_SVET, .5, False, False, 1.0,
                      1.5, True, True, "#eec9a6", False, MOLOKO, False))
    pol = 30 * A.w(t, 1.2, .2)
    ruk, (hx, hy) = rukav(760, 700, 170, 54, t, "#4a4440", TEPLO_SVET, .4, 4.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(880, 700, 160, 48 + pol * .3, t, "#4a4440", TEPLO_SVET, .7, 7.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M{hx-60:.0f},{hy+40:.0f} q16,-70 76,-72 q60,2 76,72 Z"'
               f' fill="#2b2420" {o(6)}/>')
    s += SL(0, f'<path d="M{h2x-30:.0f},{h2y:.0f} q30,-16 60,0 l-6,40 q-26,14 -54,0 Z"'
               f' fill="{VINO}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="560" y="960" width="110" height="80" rx="12"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    s += SL(Z_SRED, zerkalo(120, 240, 280, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="134" y="254" width="252" height="492" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    s += SL(Z_SRED, f'<rect x="520" y="240" width="420" height="18" rx="8"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    s += SL(Z_SRED, naryad_plechiki(640, 260, 380, t, "#5c4a3f", 1.0, .3, False, None, .0, 311))
    s += SL(Z_SRED, f'<rect x="980" y="1010" width="320" height="46" rx="8"'
                    f' fill="#5a4038" {o(4)}/>')
    s += SL(Z_SRED, girlyanda(140, 130, 1600, t, 10, 313, 46))
    s += SL(0, lampa_stolika(1500, 440, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def garderob_restorana(t):
    """Гардероб ресторана: гость в вельветовом пиджаке подаёт пальто, другой
    рукой поправляет винный галстук."""
    rnd = random.Random(3099)
    s = f'<rect width="{W}" height="{H}" fill="#241c1e"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 315))
    s += SL(Z_DAL, kladka(0, 0, W, 1080, 82))
    s += SL(Z_DAL, elka(1800, 1050, 460, t, 1.0, True, 317))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(Z_SRED, f'<rect x="120" y="640" width="900" height="180" rx="10"'
                    f' fill="{DEREVO}" {o(7)}/>'
                    f'<rect x="120" y="640" width="900" height="16" fill="#ffffff"'
                    f' opacity=".14"/>')
    nom = ""
    for i in range(12):
        nx = 180 + i * 68
        kach = 4.0 * A.w(t, 2.4, i * .2)
        nom += (f'<g transform="rotate({kach:.2f} {nx} 300)">'
                f'<path d="M{nx},300 l0,40" stroke="{SEREBRO}" stroke-width="4"/>'
                f'<circle cx="{nx}" cy="362" r="22" fill="{MED}" {o(3)}/></g>')
    s += SL(Z_SRED, nom)
    # гардеробщик принимает пальто
    s += SL(0, figura(420, 640, 420, t, GRAFIT, TEPLO_SVET, .2, False, False, 1.0,
                      1.5, True, True, "#eec9a6", False, MOLOKO, False))
    p = A.out(A.seg(t, .3, 1.5))
    for sgn in (-1, 1):
        ruk, _ = rukav(420 + sgn * 70, 460, 160, 20 - sgn * 10, t, GRAFIT, TEPLO_SVET,
                       .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
    px2 = 760 - 280 * p
    s += SL(0, f'<path d="M{px2-80:.0f},480 h160 l30,300 q-110,30 -220,0 Z"'
               f' fill="#5c4a3f" opacity="{.6+.4*p:.2f}" {o(5)}/>')
    # гость в вельветовом пиджаке
    s += SL(0, figura(1280, 1050, 540, t, "#6b4426", TEPLO_SVET, .5, False, False, 1.0,
                      2.0, True, True, "#f0cfae", False, MOLOKO, True))
    ruk, _ = rukav(1190, 760, 250, -34, t, "#6b4426", TEPLO_SVET, .4, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(1370, 770, 150, -112, t, "#6b4426", TEPLO_SVET, .7, 5.0)
    s += SL(0, ruk2)
    rub = ""
    for i in range(14):
        rub += (f'<path d="M{1200+i*12},700 l0,220" stroke="#50321c"'
                f' stroke-width="3" opacity=".6"/>')
    s += SL(0, rub)
    s += SL(0, f'<path d="M1268,660 l24,0 l-6,120 l28,130 h-68 l28,-130 Z"'
               f' fill="{VINO}" {o(4)}/>')
    s += SL(Z_SRED, zerkalo(1060, 220, 320, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1074" y="234" width="292" height="492" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    s += SL(Z_SRED, f'<rect x="420" y="980" width="420" height="70" rx="12"'
                    f' fill="#45384f" {o(5)}/>')
    lyus = ""
    for i in range(9):
        a = i * 40
        lyus += (f'<circle cx="{960+120*math.cos(math.radians(a)):.0f}"'
                 f' cy="{180+40*math.sin(math.radians(a)):.0f}" r="14" fill="{ZOLOTO}"'
                 f' opacity="{.5+.5*abs(A.w(t,1.8,i*.2)):.2f}"/>')
    s += SL(Z_SRED, lyus)
    s += SL(Z_SRED, teplo(960, 200, 420, 260, .26 + .08 * abs(A.w(t, 1.9))))
    s += SL(Z_SRED, girlyanda(1100, 120, 700, t, 9, 319, 44))
    s += SL(0, lampa_stolika(160, 600, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def sborka_shestogo_naryada(t):
    """На покрывале кровати наряд выкладывается, как выкройка: рубашка,
    галстук, брюки, ремень и ботинки одного оттенка; между ними знаки равенства."""
    rnd = random.Random(3101)
    s = f'<rect width="{W}" height="{H}" fill="#221d1c"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 321))
    s += SL(Z_DAL, stena("doski", t, 128))
    s += SL(Z_SRED, f'<rect x="60" y="560" width="1800" height="480" rx="20"'
                    f' fill="#4a3f4a" {o(7)}/>'
                    f'<rect x="80" y="580" width="1760" height="40" rx="14"'
                    f' fill="#5a4b5a" opacity=".7"/>')
    s += SL(Z_SRED, f'<path d="M120,620 q130,-80 260,0 l0,120 q-130,40 -260,0 Z"'
                    f' fill="{MOLOKO}" {o(5)}/>')
    hod = A.seg(t, .25, 3.2)
    VESCHI = (("rub", 520, MOLOKO), ("gal", 760, VINO), ("bryu", 1000, GRAFIT),
              ("rem", 1300, "#6b4426"), ("bot", 1560, "#6b4426"))
    for i, (kind, x, c) in enumerate(VESCHI):
        p = A.out(A.seg(t, .3 + i * .45, .5))
        if p <= .02:
            continue
        op = f'opacity="{p:.2f}"'
        if kind == "rub":
            s += SL(0, f'<path d="M{x-110},700 h220 l20,180 h-260 Z" fill="{c}" {op} {o(5)}/>'
                       f'<path d="M{x-110},700 l-60,40 l20,50 l50,-30 Z" fill="{c}" {op} {o(3)}/>')
        elif kind == "gal":
            s += SL(0, f'<path d="M{x-14},700 l28,0 l-8,110 l30,120 h-72 l30,-120 Z"'
                       f' fill="{c}" {op} {o(4)}/>')
        elif kind == "bryu":
            s += SL(0, f'<path d="M{x-110},700 h220 l-20,230 h-70 l-20,-150 l-20,150'
                       f' h-70 Z" fill="{c}" {op} {o(5)}/>')
        elif kind == "rem":
            s += SL(0, f'<rect x="{x-140}" y="760" width="280" height="30" rx="12"'
                       f' fill="{c}" {op} {o(4)}/>'
                       f'<rect x="{x+100}" y="752" width="46" height="46" rx="8"'
                       f' fill="{ZOLOTO}" {op} {o(3)}/>')
        else:
            for j in range(2):
                s += SL(0, f'<path d="M{x-120+j*140},880 q14,-72 80,-74 q66,2 80,74 Z"'
                           f' fill="{c}" {op} {o(5)}/>')
    for i, ex in enumerate((1150, 1430)):
        q = A.out(A.seg(t, 1.9 + i * .3, .5))
        s += SL(0, f'<path d="M{ex-30},790 h60 M{ex-30},830 h60" stroke="{ZOLOTO}"'
                   f' stroke-width="12" opacity="{q:.2f}" stroke-linecap="round"/>')
    kp = A.out(A.seg(t, 2.4, 1.0))
    s += SL(0, kot(1000 - 60 * kp, 940, t, 1.4, "#6b5a46", kp > .6))
    s += SL(Z_SRED, f'<rect x="60" y="760" width="240" height="280" rx="12"'
                    f' fill="{DEREVO}" {o(6)}/>')
    s += SL(Z_SRED, hodiki(220, 420, t, 1.3))
    s += SL(Z_SRED, girlyanda(400, 120, 1200, t, 9, 323, 44))
    s += SL(0, lampa_stolika(180, 740, t, 1.4))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def koza_i_velvetovyy_rukav(t):
    """Коза трётся щекой о рукав вельветового пиджака на манекене и жмурится;
    рядом раскрыт журнал с рисунком такого же пиджака."""
    rnd = random.Random(3102)
    s = f'<rect width="{W}" height="{H}" fill="#241c1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 325))
    s += SL(Z_DAL, stena("oboi", t, 129))
    s += SL(Z_DAL, elka(1820, 1050, 420, t, 1.0, True, 327))
    s += SL(Z_SRED, f'<rect x="200" y="960" width="1300" height="90" rx="14"'
                    f' fill="#5a3a3a" {o(5)}/>')
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, manekken(1280, 1000, 640, t, KREM2, "m", "#6b4426", .3, MOLOKO, .04, 329))
    rub = "".join(f'<path d="M{1180+i*16},560 l0,250" stroke="#50321c"'
                  f' stroke-width="3" opacity=".6"/>' for i in range(14))
    s += SL(0, rub)
    tr = A.w(t, 1.6)
    s += SL(0, koza(620 + 30 * tr, 1010, 380, t, .2, True))
    s += SL(0, teplo(760, 780, 420, 380, .26 + .08 * abs(A.w(t, 1.6))))
    # журнал на столике
    s += SL(Z_SRED, f'<rect x="160" y="820" width="320" height="40" rx="8"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="180" y="860" width="24" height="190" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="436" y="860" width="24" height="190" fill="{DEREVO}" {o(4)}/>')
    kol = 5 * A.w(t, 2.6, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kol:.2f} 320 800)">'
                    f'<path d="M180,800 q140,-30 280,0 l0,-180 q-140,-26 -280,0 Z"'
                    f' fill="{MOLOKO}" {o(5)}/>'
                    f'<path d="M320,620 l0,180" stroke="{K}" stroke-width="3"'
                    f' opacity=".45"/>'
                    f'<path d="M230,700 h60 l10,70 h-80 Z" fill="#6b4426" {o(3)}/>'
                    f'<path d="M360,700 h60 l10,70 h-80 Z" fill="#6b4426" {o(3)}/></g>')
    s += SL(Z_SRED, f'<path d="M1560,1046 q-30,-200 90,-206 l0,206 Z" fill="#4a3a52" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1500" y="600" width="14" height="440" fill="{CHUGUN}" {o(3)}/>'
                    f'<path d="M1440,600 h134 l-20,-86 h-94 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, lampa_stolika(1507, 580, t, 1.4))
    s += SL(Z_SRED, zerkalo(60, 300, 160, 480, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(300, 120, 1300, t, 10, 331, 44))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def pustye_plechiki(t):
    """Плечики едут по перекладине мужского шкафа: рубашки, куртка, спортивный
    костюм — и одни пустые плечики там, где мог бы висеть пиджак."""
    rnd = random.Random(3103)
    s = f'<rect width="{W}" height="{H}" fill="#1f1b1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 333))
    s += SL(Z_DAL, stena("kraska", t, 130))
    s += SL(Z_DAL, shkaf(360, 1050, 1200, 980, t, 1.0, False))
    s += SL(Z_SRED, perekladina(960, 270, 1060))
    s += SL(Z_SRED, polovicy(1050))
    hod = A.seg(t, .2, 3.0)
    for i, c in enumerate((MOLOKO, KREM2, "#4a5a6a", "#3a4a3a")):
        px = 560 + i * 200 + 120 * hod
        s += SL(Z_SRED, naryad_plechiki(px, 290, 420, t, c, 1.05, i * .25, False,
                                        None, .04, 334 + i))
    px = 1360 + 120 * hod
    s += SL(0, plechiki(px, 300, 1.6, "#7a5a3a", t, .1, 5.0))
    s += SL(0, f'<circle cx="{px:.0f}" cy="420" r="{70+16*abs(A.w(t,1.5)):.0f}"'
               f' fill="{ZOLOTO}" opacity=".10"/>')
    s += SL(0, figura(240, 1050, 540, t, "#4a4440", TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", False, MOLOKO, True))
    ruk, _ = rukav(330, 740, 230, -28 + 14 * A.w(t, 1.7), t, "#4a4440", TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(170, 780, 200, 196, t, "#4a4440", TEPLO_SVET, .5, 6.0)
    s += SL(0, ruk2)
    gal = ""
    for i in range(5):
        gx = 1640 + i * 44
        kach = 3.4 * A.w(t, 2.3, i * .3)
        gal += (f'<g transform="rotate({kach:.2f} {gx} 420)">'
                f'<path d="M{gx-10},420 l20,0 l-5,120 h-10 Z"'
                f' fill="{(VINO, TSINIY, GRAFIT, HVOYA, TERRAKOT)[i]}" {o(3)}/></g>')
    s += SL(Z_SRED, gal)
    s += SL(Z_SRED, "".join(f'<path d="M{700+i*170},1040 q14,-60 72,-62 q58,2 72,62 Z"'
                            f' fill="#2b2420" {o(4)}/>' for i in range(2)))
    s += SL(Z_SRED, kot(1540, 1046, t, 1.3, "#3b3430"))
    s += SL(Z_SRED, zerkalo(1760, 320, 140, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(400, 120, 1300, t, 10, 339, 44))
    s += SL(0, lampa_stolika(1700, 900, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s
