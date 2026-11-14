# -*- coding: utf-8 -*-
"""102 декорации ролика «17 ноября — Ерёмин день».

Каждая — функция времени f(t) -> svg. Все нарисованы ЗАНОВО под этот текст
(R-0019): ни один кадр не взят у «13», «14», «15» и «16 ноября».
Его правила 14.11: настоящий кадр лежит ВНУТРИ сцены (метка mesto_stoka),
сцены не пустые, предметы узнаваемые, в каждой сцене живой огонёк.

СОБИРАЕТСЯ sobrat_lok.py из частей — руками этот файл не правят.
"""
import math, random
from baza import *
import anim as A

# ═══ из lok_obshchee.py ═══
def figura(x, y, h_, t, col="#1b1822", kant="#cfe4f5", platok=False, ph=.0,
           profil=False, op=1.0, tulup=False, naklon=0.0, boroda=False,
           shapka=False, lico=True, koja="#f0cfae"):
    """ЧЕЛОВЕК, А НЕ СИЛУЭТ. Его правило R-0047: человек должен опознаваться с
    первого взгляда. Поэтому у фигуры есть лицо (глаза с бликом, брови, нос,
    румянец), одежда с поясом и оторочкой, рукава и обувь, а у головы —
    платок, шапка или волосы с бородой.

    x, y — середина и уровень пола, h_ — полный рост. Кант обязателен: тёмная
    фигура без канта сливается с тёмным фоном избы.
    """
    w_ = h_ * .42
    hh = h_ * .145                      # радиус головы
    gy = y - h_ * .845                  # центр головы
    dy = 3.0 * A.w(t, .62, ph)          # дыхание
    ug = naklon * A.w(t, 1.4, ph)
    sgn = 1 if not profil else 1
    s = (f'<g transform="translate(0,{dy:.1f}) rotate({ug:.2f} {x:.0f} {y:.0f})"'
         f' opacity="{op:.2f}">')
    s += ten(x, y + h_ * .012, w_ * .62, h_ * .022, .45)
    # обувь: два валенка
    for i in (-1, 1):
        s += (f'<path d="M{x+i*w_*.22-w_*.11:.0f},{y-h_*.085:.0f} h{w_*.22:.0f}'
              f' v{h_*.062:.0f} q0,{h_*.025:.0f} {-w_*.07:.0f},{h_*.025:.0f}'
              f' h{-w_*.09:.0f} q{-w_*.06:.0f},0 {-w_*.06:.0f},{-h_*.025:.0f} Z"'
              f' fill="#3b2f26" stroke="{K}" stroke-width="{max(2, h_*.011):.1f}"/>')
    # одежда: трапеция от плеч до подола
    plech = y - h_ * .66
    pod = y - h_ * .07
    s += (f'<path d="M{x-w_*.33:.0f},{plech:.0f} q{w_*.33:.0f},{-h_*.055:.0f} {w_*.66:.0f},0'
          f' L{x+w_*.56:.0f},{pod:.0f} q{-w_*.56:.0f},{h_*.045:.0f} {-w_*1.12:.0f},0 Z"'
          f' fill="{col}" stroke="{K}" stroke-width="{max(2, h_*.012):.1f}"/>')
    # пояс и оторочка подола — без них одежда читается мешком
    s += (f'<path d="M{x-w_*.46:.0f},{y-h_*.40:.0f} q{w_*.46:.0f},{h_*.03:.0f} {w_*.92:.0f},0"'
          f' fill="none" stroke="{MED}" stroke-width="{max(3, h_*.022):.1f}" opacity=".9"/>')
    s += (f'<path d="M{x-w_*.56:.0f},{pod-h_*.03:.0f} q{w_*.56:.0f},{h_*.045:.0f} {w_*1.12:.0f},0"'
          f' fill="none" stroke="{kant}" stroke-width="{max(2, h_*.012):.1f}" opacity=".45"/>')
    if tulup:                           # тулуп: опушка по вороту и запах
        s += (f'<ellipse cx="{x:.0f}" cy="{plech+h_*.01:.0f}" rx="{w_*.40:.0f}"'
              f' ry="{h_*.035:.0f}" fill="{kant}" opacity=".55"/>')
        s += (f'<path d="M{x:.0f},{plech+h_*.03:.0f} L{x+w_*.10:.0f},{pod-h_*.02:.0f}"'
              f' stroke="{K}" stroke-width="{max(2, h_*.009):.1f}" opacity=".6" fill="none"/>')
    # рукава вдоль тела, живые
    for i in (-1, 1):
        a = i * (12 + 5 * A.w(t, 1.9, ph + (0 if i < 0 else .4)))
        rx = x + i * w_ * .40
        s += (f'<g transform="rotate({a:.1f} {rx:.0f} {plech+h_*.02:.0f})">'
              f'<rect x="{rx-w_*.11:.0f}" y="{plech+h_*.01:.0f}" width="{w_*.22:.0f}"'
              f' height="{h_*.40:.0f}" rx="{w_*.11:.0f}" fill="{col}" stroke="{K}"'
              f' stroke-width="{max(2, h_*.011):.1f}"/>'
              f'<rect x="{rx-w_*.10:.0f}" y="{plech+h_*.34:.0f}" width="{w_*.20:.0f}"'
              f' height="{h_*.045:.0f}" rx="{w_*.02:.0f}" fill="{kant}" opacity=".5"/></g>')
    # ПОДЛОЖКА УБОРА — до головы, иначе платок и шапка закрывают лицо
    if platok:
        s += (f'<path d="M{x-hh*1.22:.0f},{gy-hh*.04:.0f} a{hh*1.22:.0f},{hh*1.26:.0f} 0 0 1'
              f' {hh*2.44:.0f},0 q{-hh*.10:.0f},{hh*1.40:.0f} {-hh*1.22:.0f},{hh*1.62:.0f}'
              f' q{-hh*1.12:.0f},{-hh*.22:.0f} {-hh*1.22:.0f},{-hh*1.62:.0f} Z"'
              f' fill="{TKAN}" stroke="{K}" stroke-width="{max(2, h_*.011):.1f}"/>')
    # шея и голова
    s += (f'<rect x="{x-hh*.34:.0f}" y="{gy+hh*.72:.0f}" width="{hh*.68:.0f}"'
          f' height="{hh*.55:.0f}" fill="{koja}" stroke="{K}" stroke-width="{max(2, h_*.01):.1f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{gy:.0f}" rx="{hh:.0f}" ry="{hh*1.06:.0f}"'
          f' fill="{koja}" stroke="{K}" stroke-width="{max(2, h_*.012):.1f}"/>')
    if lico and hh > 9:
        gl = hh * .30 if not profil else hh * .40
        mig = 1 if not A.blink(t, 4.1 + (ph * 3 % 2), ph) else 0
        for i in ((1,) if profil else (-1, 1)):
            ex = x + (gl if profil else i * gl)
            if mig:
                s += (f'<ellipse cx="{ex:.0f}" cy="{gy-hh*.08:.0f}" rx="{hh*.13:.0f}"'
                      f' ry="{hh*.16:.0f}" fill="#2b2118"/>')
                s += (f'<circle cx="{ex+hh*.05:.0f}" cy="{gy-hh*.14:.0f}" r="{hh*.05:.0f}"'
                      f' fill="#ffffff" opacity=".9"/>')
            else:
                s += (f'<path d="M{ex-hh*.14:.0f},{gy-hh*.08:.0f} q{hh*.14:.0f},{hh*.10:.0f}'
                      f' {hh*.28:.0f},0" fill="none" stroke="#2b2118"'
                      f' stroke-width="{max(2, hh*.10):.1f}" stroke-linecap="round"/>')
            s += (f'<path d="M{ex-hh*.18:.0f},{gy-hh*.33:.0f} q{hh*.18:.0f},{-hh*.12:.0f}'
                  f' {hh*.36:.0f},0" fill="none" stroke="#4a3526"'
                  f' stroke-width="{max(2, hh*.08):.1f}" stroke-linecap="round"/>')
        # нос и рот
        if profil:
            s += (f'<path d="M{x+hh*.72:.0f},{gy+hh*.02:.0f} l{hh*.22:.0f},{hh*.16:.0f}'
                  f' l{-hh*.22:.0f},{hh*.06:.0f}" fill="{koja}" stroke="{K}"'
                  f' stroke-width="{max(2, hh*.08):.1f}" stroke-linejoin="round"/>')
        else:
            s += (f'<path d="M{x:.0f},{gy-hh*.02:.0f} l{-hh*.08:.0f},{hh*.26:.0f}'
                  f' q{hh*.08:.0f},{hh*.06:.0f} {hh*.16:.0f},0" fill="none" stroke="#b08763"'
                  f' stroke-width="{max(2, hh*.08):.1f}" stroke-linecap="round"/>')
        s += (f'<path d="M{x-hh*.20:.0f},{gy+hh*.46:.0f} q{hh*.20:.0f},{hh*.20:.0f}'
              f' {hh*.40:.0f},0" fill="none" stroke="#9c4a3c"'
              f' stroke-width="{max(2, hh*.10):.1f}" stroke-linecap="round"/>')
        for i in (-1, 1):               # румянец
            s += (f'<ellipse cx="{x+i*hh*.56:.0f}" cy="{gy+hh*.28:.0f}" rx="{hh*.20:.0f}"'
                  f' ry="{hh*.13:.0f}" fill="#e08a74" opacity=".35"/>')
    if boroda:
        # Борода начинается НИЖЕ РТА и расчёсана прядями: сплошное светлое
        # пятно от подбородка читалось как повязка на пол-лица (осмотр 14.11).
        s += (f'<path d="M{x-hh*.80:.0f},{gy+hh*.62:.0f} q{hh*.14:.0f},{hh*1.10:.0f}'
              f' {hh*.80:.0f},{hh*1.26:.0f} q{hh*.66:.0f},{-hh*.16:.0f} {hh*.80:.0f},{-hh*1.26:.0f}'
              f' q{-hh*.80:.0f},{hh*.34:.0f} {-hh*1.60:.0f},0 Z" fill="#ded3c4"'
              f' stroke="{K}" stroke-width="{max(2, h_*.009):.1f}"/>')
        for i in (-1, 0, 1):            # пряди
            s += (f'<path d="M{x+i*hh*.36:.0f},{gy+hh*.76:.0f} q{i*hh*.10:.0f},{hh*.52:.0f}'
                  f' {i*hh*.06:.0f},{hh*.92:.0f}" fill="none" stroke="#b9ab99"'
                  f' stroke-width="{max(2, hh*.07):.1f}" opacity=".75"/>')
        # усы — две дуги по сторонам от рта, рот остаётся виден
        for i in (-1, 1):
            s += (f'<path d="M{x:.0f},{gy+hh*.40:.0f} q{i*hh*.30:.0f},{-hh*.04:.0f}'
                  f' {i*hh*.52:.0f},{hh*.18:.0f}" fill="none" stroke="#ded3c4"'
                  f' stroke-width="{max(2, hh*.14):.1f}" stroke-linecap="round"/>')
    if not platok and not shapka and not tulup:      # волосы шапкой поверх головы
        s += (f'<path d="M{x-hh*1.02:.0f},{gy-hh*.02:.0f} a{hh*1.02:.0f},{hh*1.08:.0f} 0 0 1'
              f' {hh*2.04:.0f},0 q{-hh*.26:.0f},{-hh*.30:.0f} {-hh*.72:.0f},{-hh*.18:.0f}'
              f' q{-hh*.40:.0f},{hh*.10:.0f} {-hh*1.32:.0f},{hh*.18:.0f} Z"'
              f' fill="#4a3526" stroke="{K}" stroke-width="{max(2, h_*.009):.1f}"/>')
    if platok:                          # передние края платка и узелок
        for i in (-1, 1):
            s += (f'<path d="M{x+i*hh*1.18:.0f},{gy-hh*.10:.0f} q{-i*hh*.16:.0f},{hh*1.10:.0f}'
                  f' {i*hh*.04:.0f},{hh*1.62:.0f} q{-i*hh*.34:.0f},{-hh*.10:.0f}'
                  f' {-i*hh*.30:.0f},{-hh*1.58:.0f} Z" fill="{TKAN}" stroke="{K}"'
                  f' stroke-width="{max(2, h_*.009):.1f}"/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{gy+hh*1.46:.0f}" rx="{hh*.34:.0f}"'
              f' ry="{hh*.24:.0f}" fill="{TKAN}" stroke="{K}"'
              f' stroke-width="{max(2, h_*.009):.1f}"/>')
        s += (f'<path d="M{x-hh*.86:.0f},{gy-hh*.42:.0f} q{hh*.86:.0f},{-hh*.34:.0f}'
              f' {hh*1.72:.0f},0" fill="none" stroke="#f2e2c8"'
              f' stroke-width="{max(2, hh*.11):.1f}" opacity=".55"/>')
    elif shapka or tulup:               # тулья, околыш и меховые уши поверх головы
        s += (f'<path d="M{x-hh*1.14:.0f},{gy-hh*.42:.0f} a{hh*1.14:.0f},{hh*1.20:.0f} 0 0 1'
              f' {hh*2.28:.0f},0 Z" fill="#4a3a2c" stroke="{K}"'
              f' stroke-width="{max(2, h_*.011):.1f}"/>')
        for i in (-1, 1):
            s += (f'<ellipse cx="{x+i*hh*1.10:.0f}" cy="{gy+hh*.10:.0f}" rx="{hh*.24:.0f}"'
                  f' ry="{hh*.44:.0f}" fill="#8a6a4a" stroke="{K}"'
                  f' stroke-width="{max(2, h_*.009):.1f}"/>')
        # околыш идёт ПО ЛБУ, выше глаз: прежде он садился ровно на линию
        # глаз и лицо оставалось без мимики (осмотр 14.11, 20 планов)
        s += (f'<rect x="{x-hh*1.16:.0f}" y="{gy-hh*.62:.0f}" width="{hh*2.32:.0f}"'
              f' height="{hh*.32:.0f}" rx="{hh*.14:.0f}" fill="#8a6a4a" stroke="{K}"'
              f' stroke-width="{max(2, h_*.009):.1f}"/>')
    # светлый кант по плечам: отделяет фигуру от тёмного фона
    s += (f'<path d="M{x-w_*.33:.0f},{plech:.0f} q{w_*.33:.0f},{-h_*.055:.0f} {w_*.66:.0f},0"'
          f' fill="none" stroke="{kant}" stroke-width="{max(2, h_*.014):.1f}" opacity=".75"'
          f' stroke-linecap="round"/>')
    return s + '</g>'


def rukav(x, y, dl, ug, t, col="#2a2430", kant="#cfe4f5", ph=.0, amp=7.0):
    """Рукав без кисти: правило проекта — рук в кадре не рисуем, работает
    сам предмет. Рукав ходит, предмет на его конце двигают отдельно."""
    a = math.radians(ug + amp * A.w(t, .9, ph))
    x2, y2 = x + dl * math.cos(a), y + dl * math.sin(a)
    return (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"'
            f' stroke="{col}" stroke-width="{max(14, dl*.19):.0f}" stroke-linecap="round"/>'
            f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"'
            f' stroke="{kant}" stroke-width="3" opacity=".30"/>'), (x2, y2)


def mokryy_sneg(t, n=34, seed=5, op=.7, sp=1.0):
    """Первый мокрый снег: падает тяжело, почти без вихря, кое-где каплей."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        x0 = rnd.random() * W
        k = ((t * .19 * sp) + rnd.random()) % 1.0
        y = -60 + k * (H + 120)
        r = 3.4 + rnd.random() * 4.6
        dx = 16 * A.w(t, 2.6 + rnd.random(), rnd.random())
        if i % 5 == 0:                  # капля-ляпка
            s += (f'<ellipse cx="{x0+dx:.0f}" cy="{y:.0f}" rx="{r*.7:.1f}" ry="{r*1.5:.1f}"'
                  f' fill="#e7f1fb" opacity="{op*.8:.2f}"/>')
        else:
            s += (f'<circle cx="{x0+dx:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#f2f8ff"'
                  f' opacity="{op:.2f}"/>')
    return s


def goloe_derevo(x, base, h_, t, seed=3, vetok=7, kant="#2a2b33", inej_=False):
    """Голое дерево поздней осени: ствол и ветки качаются целиком."""
    rnd = random.Random(seed)
    sway = 2.6 * A.w(t, 3.4, seed * .11)
    s = f'<g transform="rotate({sway:.2f} {x:.0f} {base:.0f})">'
    s += (f'<path d="M{x-h_*.045:.0f},{base:.0f} L{x-h_*.018:.0f},{base-h_:.0f}'
          f' L{x+h_*.018:.0f},{base-h_:.0f} L{x+h_*.045:.0f},{base:.0f} Z"'
          f' fill="url(#derev)" {o(5)}/>')
    for i in range(vetok):
        p = .35 + .6 * (i / max(1, vetok - 1))
        yy = base - h_ * p
        sgn = -1 if i % 2 else 1
        dl = h_ * (.30 - .16 * p) * (.8 + rnd.random() * .5)
        s += (f'<path d="M{x:.0f},{yy:.0f} q{sgn*dl*.6:.0f},{-dl*.28:.0f}'
              f' {sgn*dl:.0f},{-dl*.52:.0f}" fill="none" stroke="{kant}"'
              f' stroke-width="{max(3, 9-i):.0f}" stroke-linecap="round"/>')
        if inej_:
            s += (f'<path d="M{x:.0f},{yy:.0f} q{sgn*dl*.6:.0f},{-dl*.28:.0f}'
                  f' {sgn*dl:.0f},{-dl*.52:.0f}" fill="none" stroke="#e9f4ff"'
                  f' stroke-width="3" opacity=".55"/>')
    return s + '</g>'


def gryaz_polosa(y, h_=70, col="#4a4038", op=1.0):
    """Голая мокрая земля: ноябрь без снега, блестящая колея."""
    s = (f'<rect x="0" y="{y:.0f}" width="{W}" height="{h_+40:.0f}" fill="{col}"'
         f' opacity="{op:.2f}"/>')
    for i in range(7):
        s += (f'<ellipse cx="{120+i*280}" cy="{y+h_*.5+((i%3)-1)*14:.0f}"'
              f' rx="{90+i*9}" ry="{10+(i%3)*4}" fill="#6a7a84" opacity=".34"/>')
    return s


def luchina(x, y, t, s_=1.0, ph=.0):
    """Лучина — тонкая щепка, горит вместо лампы. Огонёк мелкий и живой."""
    s = (f'<path d="M{x:.0f},{y:.0f} l{-6*s_:.0f},{-70*s_:.0f} l{9*s_:.0f},{2*s_:.0f}'
         f' l{5*s_:.0f},{68*s_:.0f} Z" fill="url(#derev)" {o(3)}/>')
    s += ogon(x - 2 * s_, y - 74 * s_, t, .34 * s_, ph, 3)
    s += teplo(x, y - 70 * s_, 150 * s_, 130 * s_, .5)
    return s


def podkova(x, y, s_=1.0, t=0.0, col="url(#zhel)"):
    """Подкова-оберег над дверью: железо, четыре гвоздя, слабый отблеск."""
    r = 44 * s_
    s = (f'<path d="M{x-r:.0f},{y+r*.5:.0f} A{r:.0f},{r:.0f} 0 1 1 {x+r:.0f},{y+r*.5:.0f}"'
         f' fill="none" stroke="{col}" stroke-width="{20*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x-r:.0f},{y+r*.5:.0f} A{r:.0f},{r:.0f} 0 1 1 {x+r:.0f},{y+r*.5:.0f}"'
          f' fill="none" {o(4)}/>')
    for i in range(4):
        a = math.radians(210 + i * 40)
        s += (f'<circle cx="{x+r*.98*math.cos(a):.0f}" cy="{y+r*.5-r*.98*math.sin(a)*-1:.0f}"'
              f' r="{3.4*s_:.1f}" fill="{K}"/>')
    bl = .3 + .25 * (0.5 + 0.5 * A.w(t, 3.6))
    s += (f'<circle cx="{x-r*.5:.0f}" cy="{y-r*.3:.0f}" r="{6*s_:.0f}" fill="#eaf4ff"'
          f' opacity="{bl:.2f}"/>')
    return s


def grozd_ryabiny(x, y, t, s_=1.0, n=14, seed=4, ph=.0):
    """Гроздь рябины: ягоды качаются кистью, пара ягод тёмная, иней искрой."""
    rnd = random.Random(seed)
    sway = 3.0 * A.w(t, 2.6, ph)
    s = f'<g transform="translate({sway:.1f},0)">'
    s += (f'<path d="M{x:.0f},{y-70*s_:.0f} q{6*s_:.0f},{34*s_:.0f} {2*s_:.0f},{54*s_:.0f}"'
          f' fill="none" stroke="{ZEL}" stroke-width="{5*s_:.0f}"/>')
    for i in range(n):
        a = rnd.uniform(0, 6.28)
        rr = rnd.uniform(.2, 1.0) * 46 * s_
        cx, cy = x + math.cos(a) * rr, y + math.sin(a) * rr * .8
        col = "#8e2a1c" if i % 6 == 0 else KRAS
        s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{(8.5+rnd.random()*3)*s_:.1f}"'
              f' fill="{col}" {o(2)}/>')
        s += (f'<circle cx="{cx-3*s_:.0f}" cy="{cy-3*s_:.0f}" r="{2.4*s_:.1f}"'
              f' fill="#ffd0b0" opacity=".55"/>')
    return s + '</g>'


def tusklaya_lampochka(x, y, t, s_=1.0, abazhur=True):
    """Современная лампочка под потолком: мигает на вводе, тёплое пятно."""
    mig = 1.0 if ((t * 1.7) % 1.0) > .06 else .55
    s = (f'<line x1="{x:.0f}" y1="{y-150*s_:.0f}" x2="{x:.0f}" y2="{y-34*s_:.0f}"'
         f' stroke="#30343a" stroke-width="{5*s_:.0f}"/>')
    if abazhur:
        s += (f'<path d="M{x-62*s_:.0f},{y:.0f} L{x-30*s_:.0f},{y-44*s_:.0f}'
              f' L{x+30*s_:.0f},{y-44*s_:.0f} L{x+62*s_:.0f},{y:.0f} Z"'
              f' fill="url(#krem)" {o(5)}/>')
    s += (f'<circle cx="{x:.0f}" cy="{y+14*s_:.0f}" r="{17*s_:.0f}" fill="{SVET}"'
          f' opacity="{mig:.2f}"/>')
    s += teplo(x, y + 30 * s_, 400 * s_, 330 * s_, .46 * mig)
    return s


def para_izo_rta(x, y, t, ph=0.0, s_=1.0, op=.5):
    """Пар изо рта: три облачка рождаются и тают. Без него холод не читается."""
    s = ""
    for i in range(3):
        k = ((t * .5 + ph + i * .33) % 1.0)
        r = (14 + 44 * k) * s_
        s += (f'<ellipse cx="{x + 48*k*s_:.0f}" cy="{y - 26*k*s_:.0f}"'
              f' rx="{r:.0f}" ry="{r*.64:.0f}" fill="#eaf4ff"'
              f' opacity="{op*(1-k)*(1-k):.2f}"/>')
    return s


def kirpich_ustya(x, y, w_, h_, t, zharko=True):
    """Кирпичная ОБВЯЗКА устья печи: кладка идёт рамкой ВОКРУГ проёма, а сам
    проём остаётся пустым — туда ложится нарисованный огонь и настоящий кадр.
    Прежняя сплошная кладка закрашивала проём целиком (поймано 14.11)."""
    p_ = 44
    s = kladka(x - p_, y - p_, w_ + 2 * p_, p_ + 8, 54, "url(#pech)")          # верх
    s += kladka(x - p_, y + h_ - 8, w_ + 2 * p_, p_ + 36, 54, "url(#pech)")    # низ
    s += kladka(x - p_, y, p_ + 6, h_, 54, "url(#pech)")                        # слева
    s += kladka(x + w_ - 6, y, p_ + 6, h_, 54, "url(#pech)")                    # справа
    s += (f'<rect x="{x-p_:.0f}" y="{y-p_:.0f}" width="{w_+2*p_:.0f}"'
          f' height="{h_+2*p_+28:.0f}" fill="none" {o(6)}/>')
    if zharko:
        s += teplo(x + w_ / 2, y + h_ * .72, w_ * .95, h_ * .9, .50)
        s += (f'<ellipse cx="{x+w_/2:.0f}" cy="{y+h_:.0f}" rx="{w_*.6:.0f}"'
              f' ry="{26+8*A.w(t,1.7):.0f}" fill="{ORA}" opacity=".28"/>')
    return s


def sumerki_fon(t, pozdnie=True):
    """Фон ноябрьских сумерек: небо, дальняя мокрая земля, тонкий туман."""
    s = f'<rect width="{W}" height="{H}" fill="url(#{"nsumer" if pozdnie else "nden"})"/>'
    # ВНИМАНИЕ: nebo и oblaka в baza.py уже обёрнуты в свой слой (_sloy),
    # второй SL поверх запрещён — поймано на части 1.
    s += nebo("sumer" if pozdnie else "den", t, pozdnie, 11)
    s += oblaka(t, 150, 4, 5, .34, "#cdd7e4", 13.0)
    return s


# ═══ из chast1.py ═══
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


# ═══ из chast2.py ═══
def _vedro(x, y, s_=1.0, t=0.0, polnoe=True, col="url(#zhel)"):
    """Ведро: конус кверху шире, обруч, дуга ручки, блик по боку."""
    w1, w2, hh = 62 * s_, 46 * s_, 84 * s_
    kach = 2.6 * A.w(t, 1.9, x * .001)
    s = ten(x, y + 8 * s_, w1 * .9, 10 * s_, .4)
    s += f'<g transform="rotate({kach:.2f} {x:.0f} {y-hh*1.9:.0f})">'
    s += (f'<path d="M{x-w1:.0f},{y-hh:.0f} L{x+w1:.0f},{y-hh:.0f}'
          f' L{x+w2:.0f},{y:.0f} L{x-w2:.0f},{y:.0f} Z" fill="{col}" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w1:.0f}" ry="{10*s_:.0f}"'
          f' fill="{ZHELEZ}" {o(4)}/>')
    if polnoe:
        s += (f'<ellipse cx="{x:.0f}" cy="{y-hh+2*s_:.0f}" rx="{w1*.86:.0f}"'
              f' ry="{8*s_:.0f}" fill="url(#voda)" opacity=".9"/>')
        s += (f'<ellipse cx="{x-w1*.3:.0f}" cy="{y-hh:.0f}" rx="{w1*.3:.0f}"'
              f' ry="{4*s_:.0f}" fill="#bfe6f2"'
              f' opacity="{.4+.4*abs(A.w(t,1.4,x*.002)):.2f}"/>')
    s += (f'<path d="M{x-w1:.0f},{y-hh*.96:.0f} q{w1:.0f},{-hh*.8:.0f} {w1*2:.0f},0"'
          f' fill="none" stroke="{ZHELEZ}" stroke-width="{7*s_:.0f}"/>')
    s += (f'<path d="M{x-w1*.72:.0f},{y-hh*.74:.0f} L{x-w2*.66:.0f},{y-hh*.12:.0f}"'
          f' stroke="#e6f1f8" stroke-width="{8*s_:.0f}"'
          f' opacity="{.3+.35*abs(A.w(t,2.2,x*.003)):.2f}"/>')
    s += (f'<path d="M{x-w1*.9:.0f},{y-hh*.5:.0f} q{w1*.9:.0f},{10*s_:.0f} {w1*1.76:.0f},0"'
          f' fill="none" stroke="{ZHELEZ}" stroke-width="{5*s_:.0f}" opacity=".8"/>')
    return s + '</g>'


def _korzina(x, y, w_, h_, t, seed=7, pustaya=True):
    """Плетёная корзина: лоза в два хода, дужка, тёмное дно."""
    rnd = random.Random(seed)
    s = ten(x, y + 10, w_ * .52, 16, .45)
    s += (f'<path d="M{x-w_/2:.0f},{y-h_:.0f} L{x+w_/2:.0f},{y-h_:.0f}'
          f' L{x+w_*.36:.0f},{y:.0f} L{x-w_*.36:.0f},{y:.0f} Z"'
          f' fill="url(#solom)" {o(6)}/>')
    for i in range(6):
        yy = y - h_ + 14 + i * (h_ - 20) / 5
        kk = (w_ / 2) * (1 - .28 * (i / 5))
        d = f'M{x-kk:.0f},{yy:.0f}'
        for j in range(6):
            xx = x - kk + j * (kk * 2 / 6)
            d += f' Q{xx+kk/6:.0f},{yy+(11 if j % 2 == 0 else -11):.0f} {xx+kk*2/6:.0f},{yy:.0f}'
        s += f'<path d="{d}" fill="none" stroke="#b78a46" stroke-width="9"/>'
    for i in range(7):
        xx = x - w_ / 2 + 10 + i * (w_ - 20) / 6
        s += (f'<line x1="{xx:.0f}" y1="{y-h_+6:.0f}" x2="{xx*.94+x*.06:.0f}" y2="{y-4:.0f}"'
              f' stroke="#8a6534" stroke-width="6" opacity=".7"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_:.0f}" rx="{w_/2:.0f}" ry="{h_*.13:.0f}"'
          f' fill="{"#3a2c1c" if pustaya else "url(#solom)"}" {o(5)}/>')
    duga = 3.0 * A.w(t, 3.1, seed * .07)
    s += (f'<g transform="rotate({duga:.2f} {x:.0f} {y-h_:.0f})">'
          f'<path d="M{x-w_*.42:.0f},{y-h_*.98:.0f} q{w_*.42:.0f},{-h_*.78:.0f}'
          f' {w_*.84:.0f},0" fill="none" stroke="#9a7238" stroke-width="13"/></g>')
    return s


def _glaza(x, y, r_, t, ph=.0, col="#f6e39a"):
    """Пара испуганных глаз: моргают и косятся. Утварь ими и оживает."""
    kos = r_ * .3 * A.w(t, 1.7, ph)
    s = ""
    for i in (-1, 1):
        s += (f'<ellipse cx="{x+i*r_*1.25:.0f}" cy="{y:.0f}" rx="{r_:.0f}"'
              f' ry="{(r_*.34 if A.blink(t, 3.6, ph) else r_*1.02):.1f}" fill="{col}" {o(3)}/>')
        if not A.blink(t, 3.6, ph):
            s += (f'<circle cx="{x+i*r_*1.25+kos:.0f}" cy="{y+r_*.1:.0f}" r="{r_*.42:.0f}"'
                  f' fill="{K}"/>')
            s += (f'<circle cx="{x+i*r_*1.25+kos-r_*.2:.0f}" cy="{y-r_*.22:.0f}"'
                  f' r="{r_*.16:.0f}" fill="#ffffff" opacity=".85"/>')
    return s


def _nozhki(x, y, w_, t, ph=.0, col="#4a3a28", dl=40):
    """Тонкие ножки припаса: шагают, пятки отрываются от земли."""
    s = ""
    for i in (-1, 1):
        sh = 16 * A.w(t, .8, ph + (0 if i < 0 else .5))
        s += (f'<path d="M{x+i*w_*.3:.0f},{y:.0f} q{sh*.4:.0f},{dl*.6:.0f} {sh:.0f},{dl:.0f}"'
              f' fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/>')
        s += (f'<ellipse cx="{x+i*w_*.3+sh*1.2:.0f}" cy="{y+dl+6:.0f}" rx="18" ry="8"'
              f' fill="{col}" {o(3)}/>')
    return s


def _gazeta(x, y, w_, h_, ang=0.0, seed=3, col="url(#list)"):
    """Газетный лист: без букв — волнистые строки и серая полоса-фото."""
    rnd = random.Random(seed)
    s = (f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
         f'<rect x="{x-w_/2:.0f}" y="{y-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="4" fill="{col}" {o(4)}/>')
    s += (f'<rect x="{x-w_*.42:.0f}" y="{y-h_*.40:.0f}" width="{w_*.38:.0f}"'
          f' height="{h_*.26:.0f}" fill="#9aa3a8" opacity=".75" {o(2)}/>')
    for i in range(9):
        yy = y - h_ * .36 + i * h_ * .09
        if i < 3:
            s += (f'<path d="M{x+w_*.02:.0f},{yy:.0f} q{w_*.12:.0f},{-4+rnd.uniform(-2,2):.1f}'
                  f' {w_*.44:.0f},0" fill="none" stroke="#6b645c" stroke-width="4"/>')
        else:
            s += (f'<path d="M{x-w_*.42:.0f},{yy:.0f} q{w_*.22:.0f},{rnd.uniform(-3,3):.1f}'
                  f' {w_*.86:.0f},0" fill="none" stroke="#6b645c" stroke-width="4"'
                  f' opacity=".85"/>')
    s += (f'<line x1="{x:.0f}" y1="{y-h_/2:.0f}" x2="{x:.0f}" y2="{y+h_/2:.0f}"'
          f' stroke="#b8ae9a" stroke-width="3" opacity=".8"/>')
    return s + '</g>'


def _banka(x, y, s_=1.0, zerno="url(#solom)", t=0.0):
    """Банка с крупой: стекло, крышка, уровень зерна, блик."""
    w_, hh = 54 * s_, 128 * s_
    s = ten(x, y + 6 * s_, w_ * .9, 9 * s_, .35)
    s += (f'<path d="M{x-w_:.0f},{y-hh:.0f} h{w_*2:.0f} l{-6*s_:.0f},{hh:.0f}'
          f' h{-w_*2+12*s_:.0f} Z" fill="url(#stekl)" opacity=".8" {o(5)}/>')
    s += (f'<path d="M{x-w_*.9:.0f},{y-hh*.56:.0f} h{w_*1.8:.0f} l{-5*s_:.0f},{hh*.54:.0f}'
          f' h{-w_*1.8+10*s_:.0f} Z" fill="{zerno}" {o(3)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh*.56:.0f}" rx="{w_*.9:.0f}" ry="{9*s_:.0f}"'
          f' fill="#d8b96a" opacity=".9"/>')
    s += (f'<rect x="{x-w_*1.08:.0f}" y="{y-hh-16*s_:.0f}" width="{w_*2.16:.0f}"'
          f' height="{20*s_:.0f}" rx="{6*s_:.0f}" fill="url(#zhel)" {o(4)}/>')
    s += (f'<path d="M{x-w_*.6:.0f},{y-hh*.9:.0f} l0,{hh*.7:.0f}" stroke="#ffffff"'
          f' stroke-width="{9*s_:.0f}" opacity="{.25+.2*abs(A.w(t,3.0,x*.002)):.2f}"/>')
    return s


def _listok(x, y, w_, h_, t, krest=False, kolco=False, otryv=0.0):
    """Листок численника: только бумага и пометки — крест или кольцо.
    Букв и цифр на нём нет (правило ролика), строки идут волной."""
    ug = -14 * otryv
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y-h_/2:.0f}) translate(0,{otryv*60:.0f})">'
         f'<rect x="{x-w_/2:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="6" fill="url(#list)" {o(5)}/>')
    for i in range(4):
        s += (f'<path d="M{x-w_*.34:.0f},{y-h_*.62+i*h_*.14:.0f} q{w_*.17:.0f},5'
              f' {w_*.68:.0f},0" fill="none" stroke="#7d756a" stroke-width="5"'
              f' opacity=".8"/>')
    if krest:
        bl = .6 + .4 * abs(A.w(t, 1.5))
        for d in (1, -1):
            s += (f'<line x1="{x-w_*.36*d:.0f}" y1="{y-h_*.82:.0f}"'
                  f' x2="{x+w_*.36*d:.0f}" y2="{y-h_*.16:.0f}" stroke="{KRAS}"'
                  f' stroke-width="14" stroke-linecap="round" opacity="{bl:.2f}"/>')
    if kolco:
        s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.48:.0f}" rx="{w_*.38:.0f}"'
              f' ry="{h_*.33:.0f}" fill="none" stroke="{ZEL2}" stroke-width="12"'
              f' opacity="{.55+.4*abs(A.w(t,1.2,.3)):.2f}"/>')
    s += (f'<path d="M{x-w_/2:.0f},{y-h_:.0f} h{w_:.0f}" stroke="{ZHELEZ}"'
          f' stroke-width="8"/>')
    return s + '</g>'


# ── 35 ─────────────────────────────────────────────────────────────────────
def okno_so_svetom_v_nochi(t):
    """Окно деревенского дома снаружи на пол-кадра: за кружевной занавеской
    горит лампа и вяжет бабушка, а по тёмной улице к огоньку идёт путник."""
    rnd = random.Random(3511)
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 353)
    s += ulica_dal(-60, 700, 820, t, False, 359)
    s += SL(Z_DAL, gryaz_polosa(792, 150, "#2c2822"))
    st = brevna(300, 60, 1500, 900, 116)
    st += (f'<path d="M260,120 L1060,-130 L1860,120 Z" fill="#43372c" opacity=".95" {o(8)}/>')
    s += SL(Z_DAL, st)
    s += SL(Z_DAL, f'<rect x="1380" y="-60" width="104" height="210"'
                   f' fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, dym(1432, -40, t, 5, .22, 320, .32, "#c8d0da", 1.1))
    ox, oy, ow, oh = 540, 230, 880, 560
    gas = A.ease(A.seg(t, 4.0, 1.0))
    yarko = (1 - gas) * (.84 + .16 * abs(A.w(t, 1.6)))
    vn = f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#2a1d12"/>'
    vn += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="{SVET}"'
           f' opacity="{.30*yarko:.2f}"/>')
    vn += teplo(ox + ow * .30, oy + oh * .52, 420, 360, .62 * yarko)
    vn += (f'<rect x="{ox+ow*.08:.0f}" y="{oy+oh*.66:.0f}" width="{ow*.5:.0f}"'
           f' height="26" rx="8" fill="#5a4026" opacity=".9"/>')
    vn += lampa(ox + ow * .22, oy + oh * .64, t, .72)
    bx = ox + ow * .66
    vn += figura(bx, oy + oh * .98, 430, t, "#4a3140", "#ffd98a", True, .2,
                 True, 1.0 * yarko + .02, False, .8)
    sp = 26 * A.w(t, .55, .1)
    for i in range(2):
        vn += (f'<line x1="{bx-130+i*18:.0f}" y1="{oy+oh*.46+sp*.5:.0f}"'
               f' x2="{bx-30+i*22:.0f}" y2="{oy+oh*.62-sp:.0f}" stroke="{KREM}"'
               f' stroke-width="7" stroke-linecap="round"'
               f' opacity="{.9*yarko+.05:.2f}"/>')
    vn += (f'<ellipse cx="{bx-156:.0f}" cy="{oy+oh*.74:.0f}" rx="52" ry="44"'
           f' fill="{TKAN2}" opacity="{.95*yarko+.05:.2f}" {o(4)}/>')
    vn += (f'<path d="M{bx-150:.0f},{oy+oh*.70:.0f} q-40,-40 -90,-8" fill="none"'
           f' stroke="{TKAN2}" stroke-width="6" opacity="{yarko:.2f}"/>')
    kr = ""
    for i in range(11):
        kx = ox + 20 + i * (ow - 40) / 10
        kr += (f'<path d="M{kx:.0f},{oy+10} q{(ow-40)/20:.0f},86 {(ow-40)/10:.0f},0"'
               f' fill="none" stroke="#f4efe2" stroke-width="7" opacity=".72"/>')
        kr += (f'<circle cx="{kx+(ow-40)/20:.0f}" cy="{oy+54}" r="9" fill="none"'
               f' stroke="#f4efe2" stroke-width="5" opacity=".6"/>')
    kr += (f'<rect x="{ox+6}" y="{oy+6}" width="{ow-12}" height="30" fill="#f4efe2"'
           f' opacity=".5"/>')
    s += SL(Z_SRED, vn + kr)
    s += SL(Z_SRED, zanaveska(ox + 24, oy + 30, 480, 190, "#efe8d6", t, 1))
    s += SL(Z_SRED, zanaveska(ox + ow - 24, oy + 30, 480, 190, "#efe8d6", t, -1))
    ob = (f'<rect x="{ox-54}" y="{oy-54}" width="{ow+108}" height="{oh+108}" rx="10"'
          f' fill="none" stroke="url(#derev)" stroke-width="96"/>')
    ob += (f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}" y2="{oy+oh}"'
           f' stroke="url(#derev)" stroke-width="30"/>'
           f'<line x1="{ox}" y1="{oy+oh*.45:.0f}" x2="{ox+ow}" y2="{oy+oh*.45:.0f}"'
           f' stroke="url(#derev)" stroke-width="30"/>')
    ob += (f'<path d="M{ox-120},{oy-64} h{ow+240} l-72,-74 h{-ow-96} Z"'
           f' fill="{DOSKA2}" {o(8)}/>')
    for i in range(9):
        nx = ox - 90 + i * (ow + 180) / 8
        ob += (f'<path d="M{nx:.0f},{oy-70} l30,-22 l30,22 Z" fill="{MED}"'
               f' opacity=".9" {o(3)}/>')
    for sgn in (-1, 1):
        sx = ox + ow / 2 + sgn * (ow / 2 + 120)
        kach = 2.2 * sgn * A.w(t, 4.6, .2)
        ob += (f'<g transform="rotate({kach:.2f} {sx:.0f} {oy-20:.0f})">'
               f'<rect x="{sx-70 if sgn < 0 else sx-10:.0f}" y="{oy-30}" width="80"'
               f' height="{oh+60}" rx="8" fill="url(#dosk)" {o(7)}/>'
               f'<path d="M{sx-50 if sgn < 0 else sx+10:.0f},{oy+90} q34,70 0,140"'
               f' fill="none" stroke="#5a3a22" stroke-width="9" opacity=".7"/></g>')
    ob += (f'<rect x="{ox-130}" y="{oy+oh+54}" width="{ow+260}" height="46" rx="10"'
           f' fill="url(#dosk)" {o(8)}/>')
    s += SL(Z_SRED, ob)
    s += SL(Z_SRED, teplo(ox + ow / 2, oy + oh + 120, 640, 260, .34 * yarko))
    hod = A.ease(A.seg(t, .3, 2.6))
    px = 1790 - hod * 300
    s += SL(Z_SRED, figura(px, 1060, 470, t, "#1d1a24", "#cfe4f5", False, .6,
                           True, 1.0, True, 1.2, True, True))
    s += SL(Z_SRED, para_izo_rta(px + 54, 672, t, .3, 1.2, .6))
    ruk, (fx, fy) = rukav(px - 100, 780, 140, 76, t, "#1d1a24", "#cfe4f5", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, teplo(fx, fy + 86, 300, 260, .5 + .12 * abs(A.w(t, 1.5))))
    fon = (f'<path d="M{fx-40:.0f},{fy:.0f} q40,-54 80,0" fill="none"'
           f' stroke="{ZHELEZ}" stroke-width="9"/>'
           f'<path d="M{fx-78:.0f},{fy+44:.0f} h156 l-18,-34 h-120 Z" fill="{ZHELEZ}" {o(6)}/>'
           f'<path d="M{fx-66:.0f},{fy+44:.0f} h132 l-14,170 h-104 Z"'
           f' fill="url(#stekl)" opacity=".78" {o(7)}/>')
    fon += ogon(fx, fy + 196, t, .72, .4, 5)
    fon += (f'<path d="M{fx-72:.0f},{fy+214:.0f} h144 l14,40 h-172 Z"'
            f' fill="{ZHELEZ}" {o(6)}/>')
    fon += (f'<line x1="{fx-54:.0f}" y1="{fy+56:.0f}" x2="{fx-44:.0f}"'
            f' y2="{fy+200:.0f}" stroke="#ffffff" stroke-width="9" opacity=".3"/>')
    s += SL(Z_SRED, fon)
    kal = A.out(A.seg(t, 2.0, 1.2))
    kal_g = (f'<rect x="130" y="600" width="34" height="470" rx="10"'
             f' fill="url(#derev)" {o(7)}/>'
             f'<rect x="420" y="600" width="34" height="470" rx="10"'
             f' fill="url(#derev)" {o(7)}/>')
    kal_g += f'<g transform="rotate({-38*kal:.1f} 150 1040)">'
    kal_g += (f'<rect x="150" y="660" width="280" height="400" rx="8"'
              f' fill="url(#dosk)" {o(7)}/>')
    for i in range(4):
        kal_g += (f'<rect x="{162+i*68:.0f}" y="666" width="56" height="388" rx="6"'
                  f' fill="url(#dosk)" {o(5)}/>')
    kal_g += (f'<line x1="150" y1="700" x2="430" y2="800" stroke="#5a3a22"'
              f' stroke-width="14"/>'
              f'<line x1="150" y1="1010" x2="430" y2="910" stroke="#5a3a22"'
              f' stroke-width="14"/>'
              f'<circle cx="400" cy="860" r="14" fill="url(#zhel)" {o(4)}/></g>')
    s += SL(Z_PERED, kal_g)
    s += SL(Z_PERED, pleten(440, 1070, 300, 180, 6))
    s += SL(Z_PERED, goloe_derevo(1810, 1080, 560, t, 37, 7, "#232630"))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 361, .5, .9))
    s += vinetka(.5)
    return s


# ── 36 ─────────────────────────────────────────────────────────────────────
def drova_vedra_i_seno_do_temnoty(t):
    """Закатное крыльцо: хозяин тащит охапку берёзовых дров, хозяйка два
    полных ведра, сын несёт сено на вилах, из хлева тянется морда коровы."""
    rnd = random.Random(3617)
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += nebo("zakat", t, False, 367)
    s += oblaka(t, 210, 5, 373, .4, "#e4b58a", 9.0)
    s += ulica_dal(1180, 690, 760, t, False, 379)
    s += SL(Z_DAL, goloe_derevo(1300, 760, 420, t, 41, 6, "#4a3b2c"))
    s += SL(Z_DAL, gryaz_polosa(780, 190, "#4a3b2c"))
    izb = brevna(60, 180, 1020, 640, 108)
    izb += (f'<path d="M20,190 L570,-80 L1120,190 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<path d="M20,196 L570,-74 L1120,196 L1066,160 L570,-32 L74,160 Z"'
            f' fill="url(#sneg)" opacity=".8" {o(4)}/>')
    izb += (f'<rect x="760" y="-150" width="96" height="200" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(808, -140, t, 5, .2, 300, .34, "#d8cbbd", 1.0))
    ok = okno_izby(170, 330, 250, 190, t, svet=True, moroz=.2)
    ok += (f'<path d="M130,312 h330 l-28,-44 h-274 Z" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, ok)
    s += SL(Z_SRED, teplo(295, 440, 330, 280, .40 + .12 * abs(A.w(t, 1.8))))
    hl = doski(1180, 420, 700, 420, 74, True, "dosk")
    hl += (f'<path d="M1150,430 L1530,250 L1910,430 Z" fill="#6b5436" {o(8)}/>')
    s += SL(Z_SRED, hl)
    okh = (f'<path d="M1290,760 L1290,580 Q1440,500 1590,580 L1590,760 Z"'
           f' fill="#1d1711" {o(9)}/>')
    okh += (f'<path d="M1270,774 h340 l0,-26 h-340 Z" fill="url(#dosk)" {o(6)}/>')
    s += SL(Z_SRED, okh)
    mu = A.ease(A.seg(t, 1.0, 1.4))
    mx = 1420 - mu * 90
    kor = (f'<ellipse cx="{mx:.0f}" cy="640" rx="118" ry="112" fill="#d6c0a2" {o(7)}/>')
    kor += (f'<ellipse cx="{mx-46:.0f}" cy="712" rx="86" ry="58" fill="#f0dcc0" {o(6)}/>')
    for i in (-1, 1):
        kor += (f'<ellipse cx="{mx-70:.0f}" cy="{712+i*22:.0f}" rx="15" ry="20"'
                f' fill="#6b5240" {o(2)}/>')
    kor += (f'<path d="M{mx-96:.0f},712 q50,26 100,0" fill="none" stroke="#b08763"'
            f' stroke-width="7"/>')
    for i, sgn in ((0, -1), (1, 1)):
        kor += (f'<ellipse cx="{mx+sgn*48:.0f}" cy="{586:.0f}" rx="24"'
                f' ry="{8 if A.blink(t, 3.2, .1) else 22}" fill="#f2e8da" {o(4)}/>')
        if not A.blink(t, 3.2, .1):
            kor += (f'<circle cx="{mx+sgn*48:.0f}" cy="588" r="12" fill="#2b2118"/>')
    for sgn in (-1, 1):                 # рога и уши
        kor += (f'<path d="M{mx+sgn*96:.0f},572 q{sgn*52:.0f},-40 {sgn*44:.0f},-96'
                f' q{-sgn*34:.0f},34 {-sgn*52:.0f},70 Z" fill="#e8dcc6" {o(5)}/>')
        kor += (f'<ellipse cx="{mx+sgn*126:.0f}" cy="640" rx="40" ry="24"'
                f' fill="#c3a888" {o(5)}/>')
    kor += (f'<path d="M{mx-30:.0f},532 q30,-30 62,-6" fill="none" stroke="#b09876"'
            f' stroke-width="12" stroke-linecap="round"/>')
    s += SL(Z_SRED, kor)
    s += SL(Z_SRED, par(mx - 86, 726, t, 4, .55, 170, .5, 1.0))
    s += SL(Z_SRED, lavka(1660, 790, 240))
    hx = 560 + A.ease(A.seg(t, .2, 3.4)) * -120
    s += SL(Z_SRED, figura(hx, 1040, 470, t, "#3a3040", "#ffd0a0", False, .2,
                           True, 1.0, True, 1.4, True))
    kach = 4.0 * A.w(t, 1.3, .1)
    for i, sgn in enumerate((-1, 1)):   # руки держат охапку снизу
        ruk, _ = rukav(hx + sgn * 86, 800, 120, -sgn * 150 + sgn * 14, t,
                       "#3a3040", "#ffd0a0", .2 + i * .3, 4.0)
        s += SL(Z_SRED, ruk)
    oh_ = f'<g transform="rotate({kach:.2f} {hx:.0f} 820)">'
    for i in range(12):                 # берёзовые поленья лежат поперёк
        row, col = i // 4, i % 4
        lx = hx - 150 + col * 94 + row * 22
        ly = 770 - row * 68
        oh_ += (f'<rect x="{lx-54:.0f}" y="{ly-30:.0f}" width="108" height="60"'
                f' rx="26" fill="#efe8dc" {o(5)}/>')
        for j in range(3):              # чёрные чёрточки бересты
            oh_ += (f'<path d="M{lx-34+j*32:.0f},{ly-24:.0f} l0,18" stroke="#2f2a26"'
                    f' stroke-width="7" stroke-linecap="round" opacity=".85"/>')
            oh_ += (f'<path d="M{lx-22+j*32:.0f},{ly+8:.0f} l0,12" stroke="#2f2a26"'
                    f' stroke-width="6" stroke-linecap="round" opacity=".7"/>')
        oh_ += (f'<ellipse cx="{lx+54:.0f}" cy="{ly:.0f}" rx="16" ry="30"'
                f' fill="#d8b98a" {o(4)}/>')
        oh_ += (f'<ellipse cx="{lx+54:.0f}" cy="{ly:.0f}" rx="8" ry="16"'
                f' fill="#a9823f" opacity=".8"/>')
    oh_ += '</g>'
    s += SL(Z_SRED, oh_)
    s += SL(Z_SRED, para_izo_rta(hx + 50, 700, t, .1, 1.1, .5))
    zx = 900 + A.ease(A.seg(t, .4, 3.2)) * -130
    s += SL(Z_SRED, figura(zx, 1056, 440, t, "#5b2f3a", "#ffd0a0", True, .5))
    for i, sgn in enumerate((-1, 1)):
        s += SL(Z_SRED, _vedro(zx + sgn * 150, 1050 - i * 8, 1.55, t, True))
        s += SL(Z_SRED, f'<line x1="{zx+sgn*96:.0f}" y1="912" x2="{zx+sgn*128:.0f}"'
                        f' y2="958" stroke="#5b2f3a" stroke-width="22"'
                        f' stroke-linecap="round"/>')
    sy = 1180
    s += SL(Z_SRED, figura(sy, 1010, 390, t, "#2e3a46", "#ffd0a0", False, .7,
                           True, 1.0, False, 1.0, False, True))
    vil_a = -46 + 22 * A.w(t, 1.0, .2)
    ruk, _ = rukav(sy + 60, 790, 130, -24, t, "#2e3a46", "#ffd0a0", .3, 5.0)
    s += SL(Z_SRED, ruk)
    vil = f'<g transform="rotate({vil_a:.1f} {sy+50:.0f} 810)">'
    vil += (f'<line x1="{sy-60:.0f}" y1="810" x2="{sy+330:.0f}" y2="810"'
            f' stroke="url(#derev)" stroke-width="24" stroke-linecap="round"/>')
    for i in range(3):
        vil += (f'<path d="M{sy+320:.0f},810 q50,{-14+i*14:.0f} 120,{-50+i*50:.0f}"'
                f' fill="none" stroke="{ZHELEZ}" stroke-width="13"'
                f' stroke-linecap="round"/>')
    for i in range(16):                 # охапка сена на зубьях
        a = rnd.uniform(-.9, .5)
        ln = rnd.uniform(60, 130)
        vil += (f'<line x1="{sy+360+rnd.uniform(-26,26):.0f}"'
                f' y1="{800+rnd.uniform(-40,30):.0f}"'
                f' x2="{sy+360+math.cos(a)*ln:.0f}" y2="{790+math.sin(a)*ln:.0f}"'
                f' stroke="#d8b96a" stroke-width="7" stroke-linecap="round"/>')
    vil += '</g>'
    s += SL(Z_SRED, vil)
    for i in range(14):                 # сено летит с вил
        p = ((t * .7) + i * .07) % 1.0
        s += SL(Z_SRED, f'<line x1="{sy+380+p*170+rnd.uniform(-20,20):.0f}"'
                        f' y1="{740+p*p*260+rnd.uniform(-20,20):.0f}"'
                        f' x2="{sy+416+p*180:.0f}" y2="{764+p*p*270:.0f}"'
                        f' stroke="#e3c272" stroke-width="6" opacity="{1-p:.2f}"/>')
    stp = (f'<rect x="420" y="1040" width="520" height="40" rx="8" fill="url(#dosk)" {o(7)}/>')
    stp += (f'<rect x="286" y="640" width="70" height="440" rx="10"'
            f' fill="url(#derev)" {o(8)}/>')
    stp += (f'<rect x="292" y="700" width="58" height="250" rx="6" fill="#6b4a2a"'
            f' opacity=".45"/>')
    for i in range(3):                  # меловые зарубки: сделанное за день
        pok = A.ease(A.seg(t, .8 + i * .35, .4))
        if pok > .02:
            stp += (f'<path d="M{302+i*18:.0f},{740:.0f} l{6:.0f},{180*pok:.0f}"'
                    f' stroke="#efe6d2" stroke-width="11" stroke-linecap="round"'
                    f' opacity="{.9*pok:.2f}"/>')
            stp += (f'<path d="M{300+i*18:.0f},{742:.0f} l{4:.0f},{30*pok:.0f}"'
                    f' stroke="#fffaf0" stroke-width="5" stroke-linecap="round"'
                    f' opacity="{.6*pok:.2f}"/>')
    s += SL(Z_SRED, stp)
    s += SL(Z_SRED, kura(690, 1070, t, .8, .3))
    s += SL(Z_SRED, kura(770, 1058, t, .7, .6))
    s += ramka_pp("pravo", "#2a1a12", .5)
    s += SL(Z_PERED, _korzina(230, 1070, 230, 170, t, 383, False))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 389, .4, .8))
    s += vinetka(.44)
    return s


# ── 37 ─────────────────────────────────────────────────────────────────────
def temnyy_podezd(t):
    """Крыльцо хрущёвки на пол-кадра, блестящее льдом: над дверью разбитый
    фонарь, жилец в пальто едет ногой и повисает на перилах.

    Человек — `figura()` с наклоном, обе руки тянутся К ПЕРИЛАМ В ОДНУ
    СТОРОНУ, нога уезжает тапком со следом. Прежние палки крест-накрест
    читались пауком (осмотр 14.11)."""
    rnd = random.Random(3719)
    s = f'<rect width="{W}" height="{H}" fill="#161d2a"/>'
    s += nebo("noch", t, True, 397)
    s += panelka(-120, 420, 760, t, 3, True, 401)
    s += panelka(1420, 430, 640, t, 3, True, 409)
    s += SL(Z_DAL, gryaz_polosa(880, 200, "#232a33"))
    st = (f'<rect x="420" y="40" width="1140" height="700" fill="url(#beton)" {o(9)}/>')
    for i in range(5):
        st += (f'<line x1="420" y1="{120+i*130:.0f}" x2="1560" y2="{120+i*130:.0f}"'
               f' stroke="{BETON2}" stroke-width="6" opacity=".7"/>')
    for i in range(4):
        st += (f'<rect x="{470+i*280:.0f}" y="70" width="150" height="150" rx="6"'
               f' fill="{"#39465a" if i % 2 else SVET}"'
               f' opacity="{.3 if i % 2 else .35+.3*abs(A.w(t,7+i,i*.2)):.2f}" {o(5)}/>')
    s += SL(Z_DAL, st)
    kz = (f'<path d="M520,420 h960 l-60,-120 h-840 Z" fill="{BETON2}" {o(9)}/>')
    kz += (f'<rect x="520" y="414" width="960" height="34" rx="8" fill="#6b747c" {o(7)}/>')
    s += SL(Z_SRED, kz)
    dx_, dy_, dw, dh = 700, 440, 400, 540
    hlop = abs(A.w(t, 2.6, .1))
    s += SL(Z_SRED, f'<rect x="{dx_-40}" y="{dy_-30}" width="{dw+80}" height="{dh+30}"'
                    f' rx="8" fill="#3d4650" {o(9)}/>')
    s += SL(Z_SRED, dver(dx_, dy_, dw, dh, .22 * hlop, "url(#zhel)", True, False))
    stek = (f'<rect x="{dx_+70}" y="{dy_+60}" width="{dw-140}" height="170" rx="8"'
            f' fill="url(#stekl)" opacity=".55" {o(6)}/>')
    s += SL(Z_SRED, stek)
    s += SL(Z_SRED, tusklaya_lampochka(dx_ + dw / 2, dy_ + 130, t, .8, False))
    f_x, f_y = dx_ + dw / 2, dy_ - 80
    fon = (f'<path d="M{f_x-80:.0f},{f_y:.0f} h160 l-26,-80 h-108 Z" fill="{ZHELEZ}" {o(7)}/>')
    for i in range(5):
        fon += (f'<path d="M{f_x-60+i*32:.0f},{f_y:.0f} l{10-i*4},34 l16,-34 Z"'
                f' fill="#8fb8ce" opacity=".5" {o(3)}/>')
    isk = 1.0 if ((t * 2.3) % 1.0) > .82 else .0
    if isk > .5:
        fon += (f'<circle cx="{f_x:.0f}" cy="{f_y+16:.0f}" r="16" fill="{SVET}"'
                f' opacity=".9"/>')
        fon += teplo(f_x, f_y + 20, 200, 160, .4)
    fon += (f'<line x1="{f_x:.0f}" y1="{f_y-80:.0f}" x2="{f_x:.0f}" y2="{f_y-120:.0f}"'
            f' stroke="{ZHELEZ}" stroke-width="9"/>')
    s += SL(Z_SRED, fon)
    sz = (f'<path d="M420,1000 h1120 l0,30 h-1120 Z" fill="#8b949c" {o(7)}/>')
    for i in range(3):
        yy = 1000 + i * 28
        sz += (f'<rect x="{440+i*22:.0f}" y="{yy:.0f}" width="{1080-i*44:.0f}"'
               f' height="30" rx="4" fill="url(#beton)" {o(6)}/>')
        for j in range(8):
            bl = .25 + .55 * abs(A.w(t, 1.4 + j * .2, i * .3 + j * .11))
            sz += (f'<ellipse cx="{500+j*130+i*18:.0f}" cy="{yy+12:.0f}" rx="46"'
                   f' ry="8" fill="url(#led)" opacity="{bl:.2f}"/>')
            sz += (f'<circle cx="{512+j*130+i*18:.0f}" cy="{yy+8:.0f}" r="6"'
                   f' fill="#ffffff" opacity="{bl*.9:.2f}"/>')
    s += SL(Z_SRED, sz)
    # ПЕРИЛА: слева для вида, справа — те, за которые он держится
    for sgn, px, hv in ((-1, 560, False), (1, 1180, True)):
        ax, ay = px, 820
        bx_, by_ = px + sgn * 400, 1050
        per = (f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{bx_:.0f}" y2="{by_:.0f}"'
               f' stroke="url(#zhel)" stroke-width="28" stroke-linecap="round"/>')
        per += (f'<line x1="{ax:.0f}" y1="{ay+16:.0f}" x2="{bx_:.0f}" y2="{by_+16:.0f}"'
                f' stroke="#dfe8f2" stroke-width="6" opacity=".45"/>')
        per += (f'<line x1="{ax:.0f}" y1="{ay+86:.0f}" x2="{bx_:.0f}" y2="{by_+60:.0f}"'
                f' stroke="{ZHELEZ}" stroke-width="13" stroke-linecap="round"/>')
        for i in range(5):
            q = i / 4.0
            qx = ax + (bx_ - ax) * q
            qy = ay + (by_ - ay) * q
            per += (f'<rect x="{qx-9:.0f}" y="{qy:.0f}" width="18"'
                    f' height="{150 - 20*q:.0f}" fill="{ZHELEZ}" {o(4)}/>')
        per += (f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="18" fill="url(#zhel)" {o(4)}/>')
        s += SL(Z_SRED, per)
    # ЖИЛЕЦ: наклон вперёд, обе руки на перилах справа, нога уехала
    ned = A.ease(A.seg(t, 1.2, 1.6))
    zx, zy, rost = 930, 1000 + ned * 26, 560
    plech = zy - rost * .66
    s += SL(Z_SRED, figura(zx, zy, rost, t, "#2d3340", "#cfe4f5", False, .4,
                           True, 1.0, False, 2.4 + 5 * ned, False, True))
    s += SL(Z_SRED, para_izo_rta(zx + 46, zy - rost * .80, t, .2, 1.2, .6))
    for i, (sx_, sy_, tx_, ty_) in enumerate((
            (zx + 70, plech + 10, 1225, 852 + 20 * ned),
            (zx + 96, plech + 46, 1330, 912 + 24 * ned))):
        dl = math.hypot(tx_ - sx_, ty_ - sy_)
        ug = math.degrees(math.atan2(ty_ - sy_, tx_ - sx_))
        ruk, (ax2, ay2) = rukav(sx_, sy_, dl, ug, t, "#2d3340", "#cfe4f5",
                                .1 + i * .4, 2.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{ax2:.0f}" cy="{ay2:.0f}" rx="30" ry="23"'
                        f' fill="#1f242c" {o(4)}/>')
    # нога уезжает: тапок скользит вперёд, за ним след по льду
    nx_ = zx - 110 - ned * 190
    ny_ = zy + 14
    s += SL(Z_SRED, f'<path d="M{nx_-150:.0f},{ny_-6:.0f} h{150+ned*170:.0f}"'
                    f' stroke="#eaf6ff" stroke-width="12" opacity="{.25+.5*ned:.2f}"'
                    f' stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<g transform="rotate({-10-16*ned:.0f} {nx_:.0f} {ny_:.0f})">'
                    f'<rect x="{zx-170:.0f}" y="{zy-130:.0f}" width="56" height="130"'
                    f' rx="24" fill="#2d3340" {o(5)}/>'
                    f'<path d="M{nx_-62:.0f},{ny_-26:.0f} q46,-28 96,6'
                    f' q-10,30 -52,30 q-44,0 -44,-36 Z" fill="#6b4a3a" {o(5)}/>'
                    f'<path d="M{nx_-58:.0f},{ny_-22:.0f} q48,-20 90,8" fill="none"'
                    f' stroke="#a97f5e" stroke-width="7"/></g>')
    s += SL(Z_SRED, kot(520, 1072, t, .7, "#2a2622"))
    bak = (f'<rect x="200" y="760" width="230" height="300" rx="14" fill="#3f4a44" {o(8)}/>')
    bak += (f'<rect x="186" y="730" width="258" height="46" rx="12" fill="#55615a" {o(6)}/>')
    bak += (f'<line x1="240" y1="800" x2="240" y2="1050" stroke="#2c342f" stroke-width="8"/>'
            f'<line x1="390" y1="800" x2="390" y2="1050" stroke="#2c342f" stroke-width="8"/>')
    s += SL(Z_SRED, bak)
    s += SL(Z_PERED, goloe_derevo(130, 1080, 620, t, 43, 8, "#1f242c", True))
    s += ramka_pp("pravo", "#0c1016", .55)
    s += SL(Z_LETIT, mokryy_sneg(t, 30, 419, .62, 1.1))
    s += vinetka(.5)
    return s


# ── 38 ─────────────────────────────────────────────────────────────────────
def pochtovye_yaschiki_i_larek(t):
    """Ряд синих почтовых ящиков в подъезде на пол-кадра: из одного торчит
    газета, а за окном подъезда через тёмный двор догорает ларёк."""
    rnd = random.Random(3823)
    s = f'<rect width="{W}" height="{H}" fill="#4d5a5c"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="url(#beton)" opacity=".55"/>')
    sten = ""
    for i in range(7):
        sten += (f'<rect x="-20" y="{i*160:.0f}" width="1080" height="150"'
                 f' fill="{"#7d8a86" if i % 2 else "#8c9792"}" opacity=".9" {o(3)}/>')
    sten += (f'<rect x="-20" y="620" width="1080" height="30" fill="#5f6a66" {o(4)}/>')
    s += SL(Z_DAL, sten)
    s += SL(Z_DAL, f'<rect x="1040" y="0" width="880" height="1080" fill="#6e7a7c"'
                   f' opacity=".9"/>')
    s += SL(Z_SRED, tusklaya_lampochka(520, 110, t, 1.1, True))
    yx, yy, yw, yh = 150, 300, 740, 520
    ya = (f'<rect x="{yx-22}" y="{yy-26}" width="{yw+44}" height="{yh+52}" rx="12"'
          f' fill="{ZHELEZ}" {o(9)}/>')
    for r in range(4):
        for c in range(4):
            bx = yx + 10 + c * (yw - 20) / 4
            by = yy + 10 + r * (yh - 20) / 4
            ya += (f'<rect x="{bx:.0f}" y="{by:.0f}" width="{(yw-20)/4-12:.0f}"'
                   f' height="{(yh-20)/4-12:.0f}" rx="7" fill="{TKAN2}" {o(5)}/>')
            ya += (f'<rect x="{bx+10:.0f}" y="{by+16:.0f}" width="{(yw-20)/4-44:.0f}"'
                   f' height="14" rx="5" fill="#223449" {o(3)}/>')
            ya += (f'<circle cx="{bx+(yw-20)/4-32:.0f}" cy="{by+(yh-20)/4-36:.0f}"'
                   f' r="9" fill="url(#zhel)" {o(3)}/>')
            ya += (f'<path d="M{bx+6:.0f},{by+8:.0f} l{(yw-20)/4-26:.0f},0"'
                   f' stroke="#6f8ca8" stroke-width="5" opacity=".5"/>')
    s += SL(Z_SRED, ya)
    drozh = 3.0 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, _gazeta(430, 470 + drozh, 300, 220, -16 + drozh, 431))
    s += SL(Z_SRED, _gazeta(300, 1010, 280, 190, 6, 433))
    klyuch = A.ease(A.seg(t, .4, 1.3))
    s += SL(Z_SRED, figura(1120, 1070, 560, t, "#53432f", "#ffd0a0", False, .3,
                           True, 1.0, False, 1.6, True))
    ruk, (hx, hy) = rukav(1030, 700, 140, 194 + 10 * A.w(t, 1.2), t, "#53432f",
                          "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<g transform="translate({-klyuch*120:.0f},{klyuch*40:.0f})">'
                    f'<rect x="{hx-10:.0f}" y="{hy-10:.0f}" width="74" height="16"'
                    f' rx="6" fill="url(#zhel)" {o(4)}/>'
                    f'<circle cx="{hx+70:.0f}" cy="{hy-2:.0f}" r="18" fill="none"'
                    f' stroke="{MED}" stroke-width="9"/>'
                    f'<path d="M{hx-10:.0f},{hy+6:.0f} l0,16 l14,0" fill="none"'
                    f' stroke="url(#zhel)" stroke-width="8"/></g>')
    s += SL(Z_SRED, f'<ellipse cx="{hx+30:.0f}" cy="{hy:.0f}" rx="28" ry="20"'
                    f' fill="#53432f" {o(4)}/>')
    ox, oy, ow, oh = 1230, 240, 560, 500
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#121a26"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.6:.0f}" width="{ow}" height="{oh*.4:.0f}"'
           f' fill="#1b2430"/>')
    for i in range(3):
        za += (f'<rect x="{ox+30+i*190:.0f}" y="{oy+70+((i%2)*40):.0f}" width="150"'
               f' height="{oh*.52:.0f}" fill="#263040" opacity=".95"/>')
        for j in range(4):
            on = (i + j) % 3 == 0
            za += (f'<rect x="{ox+48+i*190+(j%2)*70:.0f}"'
                   f' y="{oy+100+((i%2)*40)+(j//2)*90:.0f}" width="50" height="52"'
                   f' fill="{SVET if on else "#39455a"}"'
                   f' opacity="{.3+.5*abs(A.w(t,6+j,i*.3)) if on else .25:.2f}"/>')
    gas = A.ease(A.seg(t, 3.4, 1.0))
    lx, ly = ox + ow * .50, oy + oh * .88
    lar = (f'<rect x="{lx-230:.0f}" y="{ly-330:.0f}" width="460" height="330" rx="10"'
           f' fill="#3c4a52" {o(7)}/>')
    lar += (f'<path d="M{lx-262:.0f},{ly-330:.0f} h524 l-26,-56 h-472 Z"'
            f' fill="#55646c" {o(6)}/>')
    lar += (f'<rect x="{lx-196:.0f}" y="{ly-292:.0f}" width="392" height="190" rx="8"'
            f' fill="{SVET}" opacity="{(.88-.76*gas)*(.74+.26*abs(A.w(t,.9))):.2f}" {o(5)}/>')
    for i in range(5):                  # товар на витрине силуэтами
        lar += (f'<rect x="{lx-170+i*76:.0f}" y="{ly-262+((i%2)*26):.0f}" width="52"'
                f' height="{120-((i%2)*26):.0f}" rx="6" fill="#6b5a3c"'
                f' opacity="{.8*(1-gas)+.15:.2f}" {o(3)}/>')
    lar += (f'<rect x="{lx-60:.0f}" y="{ly-92:.0f}" width="120" height="92" rx="6"'
            f' fill="#2a333a" {o(5)}/>')
    for i in range(11):
        mg = (.5 + .5 * A.w(t, .7 + i * .13, i * .2)) * (1 - gas)
        lar += (f'<circle cx="{lx-220+i*44:.0f}" cy="{ly-354:.0f}" r="14"'
                f' fill="{[SVET, KRAS, ZEL2][i%3]}" opacity="{.22+.72*mg:.2f}"/>')
    lar += teplo(lx, ly - 210, 420, 330, .55 * (1 - gas))
    za += lar
    za += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#0b1018"'
           f' opacity="{.1+.3*gas:.2f}"/>')
    s += SL(Z_SRED, f'<clipPath id="pyo38"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#pyo38)">{za}</g>')
    ram = (f'<rect x="{ox-30}" y="{oy-30}" width="{ow+60}" height="{oh+60}" rx="8"'
           f' fill="none" stroke="url(#beton)" stroke-width="62"/>')
    ram += (f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}" y2="{oy+oh}"'
            f' stroke="#cdd6d8" stroke-width="22"/>'
            f'<line x1="{ox}" y1="{oy+oh*.5:.0f}" x2="{ox+ow}" y2="{oy+oh*.5:.0f}"'
            f' stroke="#cdd6d8" stroke-width="22"/>')
    ram += (f'<rect x="{ox-46}" y="{oy+oh+30}" width="{ow+92}" height="34" rx="8"'
            f' fill="#b9c2c4" {o(6)}/>')
    ram += (f'<path d="M{ox+40},{oy+40} l200,220" stroke="#ffffff" stroke-width="12"'
            f' opacity=".2"/>')
    s += SL(Z_SRED, ram)
    s += SL(Z_SRED, teplo(ox + ow * .5, oy + oh * .62, 560, 440, .40 * (1 - gas)))
    s += SL(Z_SRED, f'<ellipse cx="{ox+ow*.4:.0f}" cy="1010" rx="420" ry="90"'
                    f' fill="{SVET}" opacity="{.20*(1-gas):.2f}"/>')
    rad = ""
    for i in range(7):
        rad += (f'<rect x="{1280+i*62:.0f}" y="800" width="42" height="190" rx="12"'
                f' fill="#cfd6d8" {o(5)}/>')
    rad += (f'<rect x="1264" y="830" width="470" height="18" fill="#b2babc" {o(4)}/>')
    s += SL(Z_SRED, rad)
    s += SL(Z_SRED, teplo(1500, 900, 300, 180, .18))
    lest = (f'<path d="M-20,1080 L420,1080 L420,860 L-20,990 Z" fill="#7d8a86"'
            f' opacity=".95" {o(6)}/>')
    for i in range(4):
        lest += (f'<path d="M{-20+i*110:.0f},{1010-i*34:.0f} h120 l0,34 h-120 Z"'
                 f' fill="#919c98" {o(5)}/>')
    s += SL(Z_PERED, lest)
    sh = A.ease(A.seg(t, 4.2, 1.4))
    for i, sgn in enumerate((-1, 1)):
        tx = 200 + sgn * 56 + sh * 180
        ty = 1000 - sh * 130 - i * 20 - abs(A.w(t, .5, i * .5)) * 18
        s += SL(Z_PERED, f'<path d="M{tx-64:.0f},{ty:.0f} q10,-40 64,-40'
                         f' q58,0 64,34 q-6,26 -64,26 q-54,0 -64,-20 Z"'
                         f' fill="#8f3a42" {o(5)}/>'
                         f'<path d="M{tx-50:.0f},{ty-28:.0f} q50,-26 96,4"'
                         f' fill="none" stroke="#d9a0a6" stroke-width="12"/>'
                         f'<ellipse cx="{tx+10:.0f}" cy="{ty+6:.0f}" rx="52" ry="12"'
                         f' fill="#5e2329" opacity=".8"/>')
    s += ramka_pp("levo", "#141a1c", .45)
    s += vinetka(.46)
    return s


# ── 39 ─────────────────────────────────────────────────────────────────────
def tri_nastoyaschie_nuzhdy(t):
    """Три картинки по словам: аптечный пакет под зелёным крестом, медсестра
    у остановки под тёплым фонарём, внучка с судками на лестнице."""
    rnd = random.Random(3929)
    s = f'<rect width="{W}" height="{H}" fill="#1b2230"/>'
    s += nebo("noch", t, True, 439)
    pw = 600
    for i in range(3):
        px = 20 + i * (pw + 20)
        s += SL(Z_DAL, f'<rect x="{px}" y="90" width="{pw}" height="900" rx="12"'
                       f' fill="#2a3340" {o(10)}/>')
    # 1: аптека
    px = 20
    ap = (f'<rect x="{px+10}" y="100" width="{pw-20}" height="880" rx="8" fill="#243043"/>')
    ap += (f'<rect x="{px+10}" y="620" width="{pw-20}" height="360" fill="#2f3b4a"/>')
    ap += (f'<rect x="{px+60}" y="300" width="{pw-120}" height="330" rx="8"'
           f' fill="{SVET}" opacity="{.26+.1*abs(A.w(t,2.4)):.2f}" {o(6)}/>')
    for j in range(3):
        ap += (f'<rect x="{px+100+j*150:.0f}" y="360" width="100" height="220" rx="6"'
               f' fill="#c9d8e2" opacity=".5" {o(4)}/>')
    mig = .35 + .65 * (1.0 if ((t * 1.1) % 1.0) > .3 else .25)
    kx, ky = px + pw / 2, 230
    ap += (f'<rect x="{kx-120:.0f}" y="{ky-86:.0f}" width="240" height="172" rx="14"'
           f' fill="#14301f" {o(7)}/>')
    for a, b, c, d in ((-34, -84, 68, 168), (-84, -34, 168, 68)):
        ap += (f'<rect x="{kx+a:.0f}" y="{ky+b:.0f}" width="{c}" height="{d}" rx="10"'
               f' fill="#3ad07a" opacity="{mig:.2f}"/>')
    ap += teplo(kx, ky, 300, 240, .3 * mig)
    ap += (f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="{30+10*abs(A.w(t,1.3)):.0f}"'
           f' fill="#9ff7c4" opacity="{.3*mig:.2f}"/>')
    pod = A.out(A.seg(t, .3, 1.2))
    bgx, bgy = px + pw * .5, 700 - pod * 50
    ruk, (hx, hy) = rukav(px + pw * .46, 1010, 190, -84, t, "#3a3f4c", "#cfe4f5", .2, 3.0)
    ap += ruk
    ap += (f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="32" ry="24" fill="#3a3f4c" {o(4)}/>')
    ap += (f'<path d="M{bgx-150:.0f},{bgy:.0f} h300 l-20,330 h-260 Z"'
           f' fill="url(#krem)" {o(8)}/>')
    ap += (f'<path d="M{bgx-150:.0f},{bgy:.0f} h300 l-16,42 h-268 Z"'
           f' fill="#e2d7bd" {o(5)}/>')
    for sgn in (-1, 1):                 # ручки пакета
        ap += (f'<path d="M{bgx+sgn*76:.0f},{bgy+6:.0f} q{sgn*10:.0f},-86'
                f' {-sgn*70:.0f},-84" fill="none" stroke="{MED}" stroke-width="13"'
                f' stroke-linecap="round"/>')
    for a, b, c, d in ((-40, -16, 80, 32), (-16, -40, 32, 80)):
        ap += (f'<rect x="{bgx+a:.0f}" y="{bgy+190+b:.0f}" width="{c}" height="{d}"'
               f' rx="8" fill="#2fae63" {o(4)}/>')
    ap += (f'<rect x="{bgx+54:.0f}" y="{bgy-96:.0f}" width="86" height="120" rx="10"'
           f' fill="url(#stekl)" opacity=".92" {o(6)}/>')
    ap += (f'<rect x="{bgx+66:.0f}" y="{bgy-128:.0f}" width="62" height="36" rx="8"'
           f' fill="{TKAN}" {o(5)}/>')
    ap += (f'<rect x="{bgx+62:.0f}" y="{bgy-52:.0f}" width="70" height="60" rx="6"'
           f' fill="#d8e8f2" opacity=".85"/>')
    ap += (f'<rect x="{bgx-130:.0f}" y="{bgy-70:.0f}" width="110" height="80" rx="10"'
           f' fill="#f2f6fa" {o(5)}/>')
    for i in range(3):
        ap += (f'<circle cx="{bgx-108+i*34:.0f}" cy="{bgy-30:.0f}" r="12"'
               f' fill="#9fb6cf" {o(3)}/>')
    s += SL(Z_SRED, ap)
    # 2: медсестра
    px = 640
    md = (f'<rect x="{px+10}" y="100" width="{pw-20}" height="880" rx="8" fill="#1f2a38"/>')
    md += (f'<rect x="{px+10}" y="800" width="{pw-20}" height="180" fill="#2b3340"/>')
    for j in range(5):
        md += (f'<rect x="{px+40+j*120:.0f}" y="{300+((j%2)*60):.0f}" width="90"'
               f' height="{480-((j%2)*60):.0f}" fill="#263141" opacity=".9"/>')
        for k_ in range(3):
            on = (j + k_) % 2 == 0
            md += (f'<rect x="{px+56+j*120:.0f}" y="{330+((j%2)*60)+k_*110:.0f}"'
                   f' width="58" height="66" fill="{SVET if on else "#39455a"}"'
                   f' opacity="{.3+.4*abs(A.w(t,5+j,k_*.3)) if on else .22:.2f}"/>')
    md += (f'<rect x="{px+60}" y="420" width="300" height="34" rx="6" fill="#4a5664" {o(5)}/>')
    md += (f'<rect x="{px+70}" y="446" width="22" height="360" fill="#4a5664" {o(4)}/>'
           f'<rect x="{px+330}" y="446" width="22" height="360" fill="#4a5664" {o(4)}/>')
    md += (f'<rect x="{px+90}" y="660" width="250" height="24" rx="8" fill="#5c6a76" {o(4)}/>')
    md += tusklaya_lampochka(px + 200, 380, t, .9, True)
    sp = A.ease(A.seg(t, .2, 2.6))
    mx = px + 480 - sp * 150
    md += figura(mx, 960, 440, t, "#3b4756", "#ffe6c8", False, .4, True, 1.0, False, 1.0)
    md += (f'<path d="M{mx-66:.0f},{960-310:.0f} q66,-26 132,0 l-12,250 h-108 Z"'
           f' fill="#f2f6fa" opacity=".92" {o(5)}/>')
    md += (f'<path d="M{mx-30:.0f},{960-300:.0f} l0,230" stroke="#cfd8e0"'
           f' stroke-width="6" opacity=".9"/>')
    md += para_izo_rta(mx + 44, 960 - 372, t, .2, 1.1, .6)
    md += (f'<ellipse cx="{mx-78:.0f}" cy="{960-180:.0f}" rx="52" ry="40"'
           f' fill="{TKAN}" {o(5)}/>')
    s += SL(Z_SRED, md)
    # 3: внучка с судками
    px = 1260
    vn = (f'<rect x="{px+10}" y="100" width="{pw-20}" height="880" rx="8" fill="#2b2a2c"/>')
    for j in range(5):
        vn += (f'<path d="M{px+10:.0f},{980-j*150:.0f} h{pw-20-j*40:.0f} l0,-60'
               f' h{-(pw-20-j*40):.0f} Z" fill="{"#6e6a66" if j % 2 else "#7a766f"}"'
               f' opacity=".95" {o(5)}/>')
    vn += (f'<path d="M{px+20},980 L{px+pw-120},300" stroke="#8d8880" stroke-width="20"'
           f' opacity=".9"/>')
    vn += tusklaya_lampochka(px + 150, 220, t, .8, False)
    pd = A.ease(A.seg(t, .4, 3.0))
    vx = px + 200 + pd * 180
    vy = 950 - pd * 250
    vn += figura(vx, vy, 400, t, "#4a2f3c", "#ffe6c8", True, .6)
    kach = 7.0 * A.w(t, 1.1, .2)
    ruk, _ = rukav(vx + 72, vy - 300, 120, 26, t, "#4a2f3c", "#ffe6c8", .3, 4.0)
    vn += ruk
    vn += f'<g transform="rotate({kach:.2f} {vx+150:.0f} {vy-290:.0f})">'
    vn += (f'<path d="M{vx+86:.0f},{vy-290:.0f} q64,-66 128,0" fill="none"'
           f' stroke="{ZHELEZ}" stroke-width="12"/>')
    for j in range(3):                  # судки: три бидона друг на друге
        cy_ = vy - 250 + j * 84
        vn += (f'<rect x="{vx+70:.0f}" y="{cy_:.0f}" width="160" height="76" rx="12"'
               f' fill="url(#zhel)" {o(6)}/>')
        vn += (f'<ellipse cx="{vx+150:.0f}" cy="{cy_:.0f}" rx="80" ry="18"'
               f' fill="#b9c2c6" {o(5)}/>')
        vn += (f'<path d="M{vx+86:.0f},{cy_+30:.0f} h128" stroke="#8a9398"'
               f' stroke-width="7" opacity=".8"/>')
        vn += (f'<path d="M{vx+94:.0f},{cy_+12:.0f} l0,42" stroke="#eef4f8"'
               f' stroke-width="9" opacity="{.3+.3*abs(A.w(t,2.0,j*.3)):.2f}"/>')
    for sgn in (-1, 1):                 # боковые дужки стяжки
        vn += (f'<line x1="{vx+150+sgn*84:.0f}" y1="{vy-282:.0f}"'
               f' x2="{vx+150+sgn*84:.0f}" y2="{vy-78:.0f}" stroke="{ZHELEZ}"'
               f' stroke-width="10"/>')
    vn += '</g>'
    vn += par(vx + 150, vy - 300, t, 4, .45, 150, .5, .8)
    buh = A.ease(A.seg(t, 2.4, 1.6))
    vn += (f'<path d="M{px+440:.0f},{620+buh*230:.0f} q70,-96 140,0 q-70,40 -140,0 Z"'
           f' fill="url(#med)" {o(6)}/>')
    vn += (f'<path d="M{px+470:.0f},{600+buh*230:.0f} q40,-20 80,0" fill="none"'
           f' stroke="#f2cf8c" stroke-width="7" opacity=".7"/>')
    vn += (f'<path d="M{px+400:.0f},{700+buh*230:.0f} h220 l-20,180 h-180 Z"'
           f' fill="{TKAN2}" opacity=".9" {o(6)}/>')
    s += SL(Z_SRED, vn)
    for i in range(2):
        s += SL(Z_PERED, f'<rect x="{620+i*620}" y="60" width="26" height="960"'
                         f' fill="#0d1118" opacity=".95"/>')
    s += ramka_pp("oba", "#0b0e14", .5)
    s += vinetka(.46)
    return s


# ── 40 ─────────────────────────────────────────────────────────────────────
def gorshok_s_uglyami_na_shestke(t):
    """Шесток печи: глиняный горшок на пол-кадра полон красных углей, жар
    дрожит, чужой рукав тянется — и крышка накрывает горшок."""
    rnd = random.Random(4001)
    s = f'<rect width="{W}" height="{H}" fill="#221711"/>'
    s += SL(Z_DAL, brevna(0, 0, 520, 1080, 104))
    s += SL(Z_DAL, f'<rect x="440" y="0" width="1480" height="1080" fill="url(#pech)"'
                   f' opacity=".96"/>')
    kl = kladka(440, 0, 1480, 420, 92, "url(#pech)")
    s += SL(Z_DAL, kl)
    s += utvar_izby(80, 300, 380, t, 443)
    ust = kirpich_ustya(1420, 300, 420, 360, t, True)
    s += SL(Z_SRED, ust)
    s += SL(Z_SRED, f'<path d="{kontur_proema(1420, 300, 420, 360, "ustie")}"'
                    f' fill="#1a0d06"/>'
                    + ugli(1460, 620, 340, t, 7, 449)
                    + ogon(1630, 630, t, 1.0, .3, 6))
    s += SL(Z_SRED, iskra_let(t, 1630, 560, 9, 457, 300, .5))
    sh = (f'<rect x="420" y="700" width="1500" height="110" rx="14"'
          f' fill="{PECH2}" {o(9)}/>')
    sh += (f'<rect x="420" y="792" width="1500" height="40" fill="#b9a98c" {o(6)}/>')
    for i in range(9):
        sh += (f'<line x1="{470+i*160:.0f}" y1="700" x2="{470+i*160:.0f}" y2="792"'
               f' stroke="#cdbb9c" stroke-width="5" opacity=".7"/>')
    s += SL(Z_SRED, sh)
    s += SL(Z_SRED, polovicy(900))
    gx, gy = 840, 700
    gor = ten(gx, gy + 4, 230, 30, .62)
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-6:.0f}" rx="196" ry="30"'
            f' fill="#7d4a23" opacity=".55"/>')
    gor += (f'<path d="M{gx-186:.0f},{gy-110:.0f} q-54,-200 46,-330'
            f' q{140:.0f},-56 {280:.0f},0 q100,130 46,330 Z"'
            f' fill="url(#glina)" {o(9)}/>')
    gor += (f'<path d="M{gx-186:.0f},{gy-110:.0f} q186,60 372,0 l-10,110'
            f' q-176,48 -352,0 Z" fill="#8e5a2c" {o(7)}/>')
    for i in range(4):
        gor += (f'<path d="M{gx-178+i*4:.0f},{gy-210-i*54:.0f} q{178-i*6:.0f},{44-i*6:.0f}'
                f' {356-i*12:.0f},0" fill="none" stroke="#a9693a" stroke-width="7"'
                f' opacity=".7"/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-440:.0f}" rx="206" ry="52"'
            f' fill="#7d4a23" {o(8)}/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-432:.0f}" rx="178" ry="40"'
            f' fill="#2c1206"/>')
    s += SL(Z_SRED, gor)
    for i in range(16):
        rr = 20 + rnd.uniform(0, 26)
        ux = gx - 150 + rnd.uniform(0, 300)
        uy = gy - 448 + rnd.uniform(-12, 18)
        pul = .45 + .55 * abs(A.w(t, 1.1 + rnd.uniform(0, 1.3), i * .14))
        s += SL(Z_SRED, f'<ellipse cx="{ux:.0f}" cy="{uy:.0f}" rx="{rr:.0f}"'
                        f' ry="{rr*.56:.0f}" fill="{UGOL}" opacity="{pul:.2f}"/>')
        s += SL(Z_SRED, f'<ellipse cx="{ux:.0f}" cy="{uy-4:.0f}" rx="{rr*.5:.0f}"'
                        f' ry="{rr*.28:.0f}" fill="{ORA}" opacity="{pul*.9:.2f}"/>')
    s += SL(Z_SRED, ugli(gx - 150, gy - 444, 300, t, 9, 461))
    s += SL(Z_SRED, ogon(gx, gy - 440, t, .9, .1, 7))
    s += SL(Z_SRED, teplo(gx, gy - 400, 520, 440, .5 + .14 * abs(A.w(t, 1.3))))
    for i in range(4):
        zh = .18 + .14 * abs(A.w(t, 1.0 + i * .3, i * .2))
        s += SL(Z_SRED, f'<ellipse cx="{gx+(i-1.5)*60:.0f}"'
                        f' cy="{gy-520-i*52-18*A.w(t,1.6,i*.3):.0f}"'
                        f' rx="{90+i*22:.0f}" ry="{26+i*8:.0f}" fill="{ORA}"'
                        f' opacity="{zh:.2f}"/>')
    s += SL(Z_SRED, iskra_let(t, gx, gy - 470, 12, 463, 420, .45))
    tyan = abs(A.w(t, 2.2, .1))
    s += SL(Z_SRED, f'<path d="M1920,180 q-60,120 -40,300 l140,0 l0,-300 Z"'
                    f' fill="#241d2c" {o(7)}/>')
    ruk, (chx, chy) = rukav(1900, 330, 420 + 40 * tyan, 172, t, "#2a2230",
                            "#9fb6cf", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{chx:.0f}" cy="{chy:.0f}" rx="44" ry="30"'
                    f' fill="#2a2230" {o(5)}/>'
                    f'<ellipse cx="{chx+16:.0f}" cy="{chy-8:.0f}" rx="22" ry="14"'
                    f' fill="#4a3f52" opacity=".8"/>')
    kry = A.ease(A.seg(t, 1.2, .7))
    ky_ = gy - 700 + kry * 200
    s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{ky_:.0f}" rx="214" ry="54"'
                    f' fill="url(#glina)" {o(8)}/>'
                    f'<ellipse cx="{gx:.0f}" cy="{ky_-26:.0f}" rx="150" ry="34"'
                    f' fill="#b07a44" {o(5)}/>'
                    f'<ellipse cx="{gx:.0f}" cy="{ky_-54:.0f}" rx="40" ry="22"'
                    f' fill="#8e5a2c" {o(6)}/>')
    s += SL(Z_SRED, krynka(400, 780, 1.5))
    s += SL(Z_SRED, f'<rect x="300" y="620" width="30" height="300" rx="10"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<path d="M250,620 q66,-90 130,0" fill="none" stroke="{ZHELEZ}"'
                    f' stroke-width="18"/>')
    s += SL(Z_SRED, f'<path d="M1240,700 q66,100 132,0 q-66,30 -132,0 Z"'
                    f' fill="url(#chug)" {o(7)}/>'
                    f'<ellipse cx="1306" cy="692" rx="70" ry="20" fill="#4a4645" {o(5)}/>')
    s += SL(Z_SRED, par(1306, 672, t, 4, .4, 150, .45, .8))
    s += ramka_pp("levo", "#160d08", .5)
    s += SL(Z_PERED, _korzina(1760, 1070, 240, 180, t, 467, False))
    s += vinetka(.46)
    return s


# ── 41 ─────────────────────────────────────────────────────────────────────
def holodnaya_pech_utrom(t):
    """Серое утро: печь с чёрным холодным устьем на пол-кадра, хозяин дует в
    остывшую золу, семья дрожит под одеялом, а у соседа труба дымит.

    Печь холодная, но кадр не остаётся без живого огонька: на шестке стоит
    огарок свечи, а в окне густо валит дым соседской трубы и светится чужое
    тёплое окно (осмотр 14.11)."""
    rnd = random.Random(4103)
    s = f'<rect width="{W}" height="{H}" fill="#6b6a66"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 110))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#9aa3a8" opacity=".22"/>')
    s += utvar_izby(1180, 300, 480, t, 419)
    s += SL(Z_SRED, polovicy(900))
    pch = pech(60, 150, 640, 790, t, False, True, False)
    s += SL(Z_SRED, pch)
    ux, uy, uw, uh = 148, 480, 300, 250
    ust = (f'<path d="{kontur_proema(ux, uy, uw, uh, "ustie")}" fill="#0f0c0a"/>')
    ust += (f'<path d="{kontur_proema(ux, uy, uw, uh, "ustie")}" fill="none" {o(9)}/>')
    for i in range(14):                 # холодная зола: ни искры
        zx = ux + 26 + rnd.uniform(0, uw - 52)
        ust += (f'<ellipse cx="{zx:.0f}" cy="{uy+uh-24+rnd.uniform(-10,10):.0f}"'
                f' rx="{rnd.uniform(14,26):.0f}" ry="{rnd.uniform(6,12):.0f}"'
                f' fill="#8d8880" opacity=".65"/>')
    s += SL(Z_SRED, ust)
    s += SL(Z_SRED, f'<rect x="80" y="752" width="600" height="46" rx="10"'
                    f' fill="#c9bda4" {o(7)}/>')
    # ОГАРОК СВЕЧИ НА ШЕСТКЕ: единственное живое тепло в холодной избе
    s += SL(Z_SRED, f'<ellipse cx="520" cy="756" rx="56" ry="16" fill="#b9ab90" {o(4)}/>')
    s += SL(Z_SRED, svecha(520, 668, t, .2, 1.2, 84))
    s += SL(Z_SRED, teplo(520, 620, 420, 360, .40 + .14 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, iskra_let(t, 520, 600, 4, 4111, 170, .25))
    duy = (t * 1.4) % 1.0
    hx, hy = 680, 930
    s += SL(Z_SRED, figura(hx, hy, 520, t, "#3e4652", "#e8eef6", False, .2,
                           True, 1.0, False, 2.4, True))
    s += SL(Z_SRED, f'<ellipse cx="{hx-86:.0f}" cy="{hy+4:.0f}" rx="56" ry="18"'
                    f' fill="#e3c6a8" {o(5)}/>'
                    f'<ellipse cx="{hx+72:.0f}" cy="{hy+6:.0f}" rx="52" ry="16"'
                    f' fill="#e3c6a8" {o(5)}/>')
    for i in range(4):                  # струя воздуха в устье
        k = (duy + i * .25) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{hx-150-k*190:.0f}" cy="{hy-330+k*24:.0f}"'
                        f' rx="{24+k*62:.0f}" ry="{12+k*26:.0f}" fill="#e8eef6"'
                        f' opacity="{.5*(1-k):.2f}"/>')
    for i in range(10):                 # поднятая зола
        k = (duy * .8 + i * .1) % 1.0
        s += SL(Z_SRED, f'<circle cx="{ux+uw*.5-k*60+rnd.uniform(-40,40):.0f}"'
                        f' cy="{uy+uh-30-k*120:.0f}" r="{3+4*(1-k):.1f}"'
                        f' fill="#b8b2a6" opacity="{.6*(1-k):.2f}"/>')
    s += SL(Z_SRED, par(hx - 100, hy - 350, t, 4, .55, 170, .45, .9))
    lx, ly, lw = 820, 700, 500
    lezh = (f'<rect x="{lx}" y="{ly}" width="{lw}" height="250" rx="14"'
            f' fill="url(#derev)" {o(8)}/>')
    lezh += (f'<rect x="{lx-20}" y="{ly-28}" width="{lw+40}" height="40" rx="12"'
             f' fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_SRED, lezh)
    droz = 5.0 * A.w(t, .33, .1)
    od = f'<g transform="translate({droz:.1f},{abs(droz)*.4:.1f})">'
    od += (f'<path d="M{lx-30:.0f},{ly-10:.0f} q{lw*.5:.0f},-150 {lw+60:.0f},-10'
           f' l0,180 q{-lw*.5:.0f},60 {-lw-60:.0f},0 Z" fill="{TKAN2}" {o(8)}/>')
    for i in range(5):
        od += (f'<path d="M{lx-20+i*(lw/4.5):.0f},{ly-110+((i%2)*26):.0f}'
               f' q30,60 0,150" fill="none" stroke="#5e7ea0" stroke-width="9"'
               f' opacity=".7"/>')
    for i, dx in enumerate((110, 280, 420)):
        gy_ = ly - 128 - (i % 2) * 22
        od += (f'<ellipse cx="{lx+dx:.0f}" cy="{gy_:.0f}" rx="46" ry="50"'
               f' fill="#f0cfae" {o(5)}/>')
        od += (f'<path d="M{lx+dx-46:.0f},{gy_-18:.0f} a46,46 0 0 1 92,0 Z"'
               f' fill="{"#8a5a30" if i else "#4a3526"}" {o(4)}/>')
        for sgn in (-1, 1):
            od += (f'<ellipse cx="{lx+dx+sgn*18:.0f}" cy="{gy_+6:.0f}" rx="7"'
                   f' ry="{3 if A.blink(t, 3.0 + i, i * .2) else 8}" fill="#2b2118"/>')
        od += (f'<ellipse cx="{lx+dx:.0f}" cy="{gy_+30:.0f}" rx="12" ry="7"'
               f' fill="#9c4a3c" opacity=".8"/>')
        od += para_izo_rta(lx + dx + 20, gy_ + 34, t, i * .3, .7, .45)
    od += '</g>'
    s += SL(Z_SRED, od)
    ox, oy, ow, oh = 1380, 220, 480, 380
    moroz = .14 + .40 * A.ease(A.seg(t, .4, 3.2))
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#b9c6cf"/>')
    za += izba_snaruzhi(ox + 40, oy + oh - 20, 400, t, True, True, 421)
    za += teplo(ox + 150, oy + oh - 140, 230, 190, .5)
    s += SL(Z_SRED, f'<clipPath id="ok41"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok41)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, moroz, False, True))
    for i in range(12):                 # иней растёт лапами по стеклу
        rr = (16 + rnd.uniform(0, 40)) * moroz
        za2 = (f'<path d="M{ox+30+rnd.uniform(0,ow-60):.0f},'
               f'{oy+30+rnd.uniform(0,oh-60):.0f} l{rr:.0f},{-rr*.6:.0f}'
               f' l{-rr*.4:.0f},{rr*1.3:.0f} Z" fill="#ffffff"'
               f' opacity="{.3*moroz:.2f}"/>')
        s += SL(Z_SRED, za2)
    # СОСЕДСКАЯ ТРУБА ДЫМИТ ГУСТО — над крышей, выше окна
    s += SL(Z_SRED, dym(ox + 290, oy - 10, t, 7, .24, 300, .5, "#e4ebf2", 1.5))
    s += SL(Z_SRED, dym(ox + 306, oy - 20, t, 5, .17, 340, .34, "#f2f6fa", 2.0))
    s += SL(Z_SRED, _vedro(1180, 1000, 1.2, t, False, "url(#chug)"))
    s += SL(Z_SRED, kot(1520, 1016, t, .85, "#55504a", True))
    s += ramka_pp("pravo", "#2b2e33", .45)
    s += SL(Z_PERED, _korzina(230, 1080, 220, 170, t, 431, True))
    s += vinetka(.42)
    return s


# ── 42 ─────────────────────────────────────────────────────────────────────
def ten_i_polennica(t):
    """Лохматая тень с жёлтыми глазами крадётся к двери с пустым горшком, но
    хозяйка распахивает дверь — и тень сдувается в пустой тулуп на заборе.

    У крыльца с первой секунды горит фонарь: прежде единственный огонь
    появлялся только в распахнутой двери на третьей секунде, и до того кадр
    стоял сине-серым (осмотр 14.11)."""
    rnd = random.Random(4217)
    s = sumerki_fon(t, True)
    s += ulica_dal(1180, 700, 740, t, False, 433)
    s += SL(Z_DAL, gryaz_polosa(790, 180, "#3a332b"))
    izb = brevna(0, 120, 1120, 700, 112)
    izb += (f'<path d="M-40,130 L560,-140 L1160,130 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="820" y="-180" width="100" height="220" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(870, -170, t, 6, .2, 320, .44, "#c8d0da", 1.3))
    raz = A.out(A.seg(t, 3.0, 1.0))
    zat = A.ease(A.seg(t, 6.4, 1.4))
    otk = raz * (1 - zat)
    dx_, dy_, dw, dh = 560, 300, 330, 560
    s += SL(Z_SRED, f'<rect x="{dx_-40}" y="{dy_-40}" width="{dw+80}"'
                    f' height="{dh+40}" rx="10" fill="{DOSKA2}" {o(9)}/>')
    s += SL(Z_SRED, f'<rect x="{dx_}" y="{dy_}" width="{dw}" height="{dh}"'
                    f' fill="#1a0f08"/>')
    s += SL(Z_SRED, teplo(dx_ + dw * .5, dy_ + dh * .6, 360 * otk + 40,
                          320 * otk + 40, .62 * otk))
    s += SL(Z_SRED, lampa(dx_ + dw * .34, dy_ + dh * .5, t, .62 * otk + .18))
    s += SL(Z_SRED, figura(dx_ + dw * .62, dy_ + dh - 6, 470 * (.3 + .7 * otk), t,
                           "#4a2f3a", "#ffd98a", True, .3, True, otk * .9 + .1))
    s += SL(Z_SRED, dver(dx_, dy_, dw, dh, otk * .9, "url(#derev)", True, False))
    s += SL(Z_SRED, podkova(dx_ + dw * .5, dy_ - 70, .95, t))
    s += SL(Z_SRED, f'<path d="M{dx_-60},{dy_+dh} h{dw+120} l-30,70 h{-dw-60} Z"'
                    f' fill="url(#dosk)" {o(8)}/>')
    # ФОНАРЬ У КРЫЛЬЦА: живой огонь с самого начала плана
    fx_, fy_ = 360, 470
    s += SL(Z_SRED, f'<path d="M{fx_:.0f},300 q-8,54 0,88" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="9"/>')
    s += SL(Z_SRED, f'<path d="M{fx_-66:.0f},{fy_-190:.0f} h132 l-18,-46 h-96 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_-56:.0f},{fy_-190:.0f} h112 l-12,180 h-88 Z"'
                    f' fill="url(#stekl)" opacity=".72" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{fx_-60:.0f}" y="{fy_-16:.0f}" width="120" height="26"'
                    f' rx="8" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, ogon(fx_, fy_ - 40, t, .8, .3, 6))
    s += SL(Z_SRED, teplo(fx_, fy_ - 80, 460, 400, .5 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, iskra_let(t, fx_, fy_ - 90, 5, 4219, 240, .35))
    pw, ph_ = 560, 460
    px, py = 1200, 980
    pol = ten(px + pw * .5, py + 14, pw * .5, 26, .45)
    pol += (f'<rect x="{px-20}" y="{py-ph_-30}" width="{pw+40}" height="30" rx="8"'
            f' fill="{DOSKA2}" {o(6)}/>')
    for r in range(6):
        for c in range(7):
            lx = px + 26 + c * 76 + (r % 2) * 12
            ly = py - 30 - r * 74
            pol += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="36" ry="33"'
                    f' fill="#d8b98a" {o(5)}/>')
            pol += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="22" ry="20"'
                    f' fill="#b08a52" opacity=".7"/>')
            for j in range(3):
                pol += (f'<path d="M{lx:.0f},{ly:.0f} l{math.cos(j*2.1+r)*34:.0f},'
                        f'{math.sin(j*2.1+r)*32:.0f}" stroke="#6b4a26"'
                        f' stroke-width="3" opacity=".7"/>')
    s += SL(Z_SRED, pol)
    schet = int(A.seg(t, 4.2, 2.4) * 6)
    for i in range(schet):
        s += SL(Z_SRED, f'<path d="M{px+40+i*86:.0f},{py-ph_-60:.0f} l16,26 l28,-48"'
                        f' fill="none" stroke="#f4efe2" stroke-width="10"'
                        f' stroke-linecap="round" opacity=".85"/>')
    sd = A.ease(A.seg(t, 3.2, 1.3))
    tx = 1020 - sd * 40
    ty = 1010
    th_ = 520 * (1 - sd * .42)
    tn = f'<g opacity="{1-sd*.55:.2f}">'
    tn += (f'<path d="M{tx-th_*.30:.0f},{ty:.0f} q{-th_*.08:.0f},{-th_*.62:.0f}'
           f' {th_*.10:.0f},{-th_*.80:.0f} q{th_*.22:.0f},{-th_*.20:.0f}'
           f' {th_*.42:.0f},0 q{th_*.18:.0f},{th_*.18:.0f} {th_*.08:.0f},{th_*.80:.0f} Z"'
           f' fill="#171521" {o(6)}/>')
    for i in range(20):                 # лохмы наружу по всему контуру
        a = -3.0 + i * .30
        lr = th_ * (.16 + .07 * abs(A.w(t, 1.2, i * .13)))
        bx_ = tx + math.cos(a) * th_ * .30
        by_ = ty - th_ * .46 + math.sin(a) * th_ * .40
        tn += (f'<path d="M{bx_:.0f},{by_:.0f}'
               f' l{math.cos(a)*lr:.0f},{math.sin(a)*lr:.0f}"'
               f' stroke="#171521" stroke-width="{20-i%4*4}" stroke-linecap="round"/>')
    tn += _glaza(tx, ty - th_ * .72, 17, t, .2, "#f6e39a")
    tn += '</g>'
    s += SL(Z_SRED, tn)
    s += SL(Z_SRED, f'<g opacity="{1-sd:.2f}">'
                    + krynka(tx + 180, ty - 330, 1.5, "#3a3142") + '</g>')
    kach = 4.4 * A.w(t, 2.3, .2)
    tul = f'<g opacity="{sd:.2f}" transform="rotate({kach:.2f} {tx:.0f} {ty-520:.0f})">'
    tul += (f'<path d="M{tx-150:.0f},{ty-520:.0f} q150,-60 300,0 l-40,420'
            f' q-110,40 -220,0 Z" fill="#7a6246" {o(8)}/>')
    tul += (f'<path d="M{tx-150:.0f},{ty-520:.0f} q150,56 300,0 l-18,60'
            f' q-134,46 -264,0 Z" fill="#cdbfa4" {o(5)}/>')
    tul += (f'<path d="M{tx:.0f},{ty-470:.0f} l-16,400" stroke="#5c4a34"'
            f' stroke-width="10" opacity=".8"/>')
    for sgn in (-1, 1):
        tul += (f'<path d="M{tx+sgn*140:.0f},{ty-490:.0f} q{sgn*70:.0f},120'
                f' {sgn*40:.0f},250" fill="none" stroke="#7a6246" stroke-width="54"'
                f' stroke-linecap="round"/>')
    tul += '</g>'
    s += SL(Z_SRED, tul)
    s += SL(Z_PERED, pleten(880, 1080, 1040, 230, 11))
    s += SL(Z_PERED, goloe_derevo(170, 1080, 640, t, 439, 8, "#232630"))
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 443, .5, .9))
    s += vinetka(.48)
    return s


# ── 43 ─────────────────────────────────────────────────────────────────────
def kerosinovaya_lampa_na_polke(t):
    """Пузатая керосиновая лампа на пол-кадра: между банкой крупы и
    будильником её снимают с полки, и в высоком стекле разгорается огонь."""
    rnd = random.Random(4327)
    s = f'<rect width="{W}" height="{H}" fill="#4a3a2c"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 108, True, "dosk"))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#2a1d14" opacity=".38"/>')
    pk = (f'<rect x="120" y="250" width="1680" height="34" rx="8"'
          f' fill="url(#derev)" {o(8)}/>')
    pk += (f'<rect x="120" y="284" width="1680" height="18" fill="{DOSKA2}" {o(5)}/>')
    for i in range(6):
        pk += (f'<path d="M{200+i*300:.0f},302 l30,54 M{420+i*300:.0f},302 l-30,54"'
               f' {o(6)} fill="none"/>')
    for i in range(9):                  # зубчатая подзорная кромка полки
        pk += (f'<path d="M{150+i*190:.0f},302 q46,42 92,0 Z" fill="{DOSKA2}"'
               f' opacity=".9" {o(3)}/>')
    s += SL(Z_DAL, pk)
    s += SL(Z_DAL, _banka(290, 250, 1.35, "url(#solom)", t))
    s += SL(Z_DAL, _banka(1700, 250, 1.1, "#c2a05c", t))
    bud_x, bud_y = 1520, 250
    bud = ten(bud_x, bud_y + 8, 70, 12, .4)
    for sgn in (-1, 1):                 # колокольчики будильника
        bud += (f'<circle cx="{bud_x+sgn*66:.0f}" cy="{bud_y-176:.0f}" r="34"'
                f' fill="url(#zhel)" {o(5)}/>')
        bud += (f'<path d="M{bud_x+sgn*22:.0f},{bud_y-28:.0f} l{sgn*16:.0f},28"'
                f' stroke="{ZHELEZ}" stroke-width="10"/>')
    bud += (f'<circle cx="{bud_x:.0f}" cy="{bud_y-110:.0f}" r="88"'
            f' fill="url(#zhel)" {o(7)}/>')
    bud += (f'<circle cx="{bud_x:.0f}" cy="{bud_y-110:.0f}" r="68"'
            f' fill="url(#krem)" {o(5)}/>')
    tik = 16 * A.w(t, 1.0)
    bud += (f'<line x1="{bud_x:.0f}" y1="{bud_y-110:.0f}"'
            f' x2="{bud_x+54*math.cos(math.radians(tik-60)):.0f}"'
            f' y2="{bud_y-110+54*math.sin(math.radians(tik-60)):.0f}"'
            f' stroke="{K}" stroke-width="7"/>')
    bud += (f'<line x1="{bud_x:.0f}" y1="{bud_y-110:.0f}"'
            f' x2="{bud_x+34*math.cos(math.radians(-tik*3+140)):.0f}"'
            f' y2="{bud_y-110+34*math.sin(math.radians(-tik*3+140)):.0f}"'
            f' stroke="{K}" stroke-width="9"/>')
    for i in range(12):
        a = math.radians(i * 30)
        bud += (f'<circle cx="{bud_x+56*math.cos(a):.0f}"'
                f' cy="{bud_y-110+56*math.sin(a):.0f}" r="4" fill="#6b645c"/>')
    bud += (f'<path d="M{bud_x-52:.0f},{bud_y-176:.0f} q52,-40 104,0" fill="none"'
            f' stroke="{ZHELEZ}" stroke-width="9"/>')
    s += SL(Z_DAL, bud)
    snyat = A.ease(A.seg(t, .6, 1.8))
    lx = 950
    ly = 820 + snyat * 180              # лампу опускают с полки на стол
    s += SL(Z_SRED, stol(600, 1004, 780, 42, False))
    s += SL(Z_SRED, f'<path d="M580,1002 h820 l-34,46 h-752 Z" fill="{RUSH}"'
                    f' opacity=".9" {o(5)}/>')
    ruk, (kx, ky) = rukav(520, 360 + snyat * 150, 230, 26 + 10 * A.w(t, 1.4), t,
                          "#4a2f3a", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="40" ry="28"'
                    f' fill="#4a2f3a" {o(5)}/>')
    lam = ten(lx, ly + 16, 230, 30, .5)
    lam += (f'<path d="M{lx-180:.0f},{ly:.0f} q-30,-110 60,-150 h240'
            f' q90,40 60,150 Z" fill="url(#med)" {o(9)}/>')
    lam += (f'<path d="M{lx-150:.0f},{ly-40:.0f} q150,40 300,0" fill="none"'
            f' stroke="#f2cf8c" stroke-width="10" opacity=".55"/>')
    lam += (f'<rect x="{lx-110:.0f}" y="{ly-212:.0f}" width="220" height="68" rx="14"'
            f' fill="url(#zhel)" {o(8)}/>')
    for i in range(7):
        lam += (f'<line x1="{lx-96+i*32:.0f}" y1="{ly-208:.0f}" x2="{lx-96+i*32:.0f}"'
                f' y2="{ly-150:.0f}" stroke="#4a4f55" stroke-width="6" opacity=".8"/>')
    lam += (f'<circle cx="{lx+150:.0f}" cy="{ly-176:.0f}" r="34" fill="url(#zhel)" {o(6)}/>')
    lam += (f'<circle cx="{lx+150:.0f}" cy="{ly-176:.0f}" r="14" fill="#8a9398" {o(3)}/>')
    s += SL(Z_SRED, lam)
    gx, gy, gw, gh = lx - 210, ly - 790, 420, 580
    put = kontur_proema(gx, gy, gw, gh, "ellips")
    razg = A.ease(A.seg(t, 2.2, 1.6))
    vid = f'<clipPath id="st43"><path d="{put}"/></clipPath>'
    vid += (f'<path d="{put}" fill="#2a1a0c"/>')
    vid += (f'<g clip-path="url(#st43)">'
            + teplo(gx + gw / 2, gy + gh * .62, 300, 320, .5 + .4 * razg)
            + ogon(gx + gw / 2, gy + gh * .86, t, 1.5 + .5 * razg, .1, 7)
            + ugli(gx + gw * .28, gy + gh * .9, gw * .44, t, 5, 449)
            + f'</g>')
    vid += mesto_stoka(gx, gy, gw, gh, "ellips")
    ob = (f'<path d="{put}" fill="url(#stekl)" opacity=".30"/>')
    ob += (f'<path d="{put}" fill="none" stroke="#e8f3ff" stroke-width="12"'
           f' opacity=".75"/>')
    ob += (f'<path d="{put}" fill="none" {o(7)}/>')
    ob += (f'<path d="M{gx+gw*.16:.0f},{gy+gh*.22:.0f} q{-gw*.06:.0f},{gh*.3:.0f}'
           f' {gw*.04:.0f},{gh*.5:.0f}" fill="none" stroke="#ffffff"'
           f' stroke-width="22" opacity="{.22+.12*abs(A.w(t,2.4)):.2f}"/>')
    ob += (f'<ellipse cx="{gx+gw/2:.0f}" cy="{gy+8:.0f}" rx="{gw*.33:.0f}" ry="26"'
           f' fill="none" stroke="#cfe4f5" stroke-width="10" opacity=".8"/>')
    ob += (f'<ellipse cx="{gx+gw/2:.0f}" cy="{gy+gh-6:.0f}" rx="{gw*.46:.0f}" ry="26"'
           f' fill="url(#zhel)" {o(6)}/>')
    s += SL(Z_SRED, vid + ob)
    s += SL(Z_SRED, teplo(lx, ly - 420, 640 * (.5 + .5 * razg),
                          560 * (.5 + .5 * razg), .42 * (.4 + .6 * razg)))
    chirk = A.seg(t, 1.6, .5)
    if chirk > .01 and chirk < .999:
        sx_, sy_ = lx + 330, ly - 330
        s += SL(Z_SRED, f'<line x1="{sx_:.0f}" y1="{sy_:.0f}" x2="{sx_+70:.0f}"'
                        f' y2="{sy_+40:.0f}" stroke="url(#derev)" stroke-width="12"'
                        f' stroke-linecap="round"/>')
        s += SL(Z_SRED, ogon(sx_, sy_ - 10, t, .42, .3, 4))
        s += SL(Z_SRED, iskra_let(t, sx_, sy_ - 20, 8, 457, 180, 1.2))
    s += SL(Z_SRED, f'<rect x="{lx+430}" y="{ly-86:.0f}" width="150" height="70"'
                    f' rx="10" fill="{TKAN}" {o(6)}/>'
                    f'<rect x="{lx+446}" y="{ly-74:.0f}" width="118" height="46"'
                    f' rx="6" fill="#e2c8a0" opacity=".9"/>')
    s += SL(Z_SRED, krynka(400, 998, 1.4))
    s += SL(Z_SRED, karavay(1600, 992, 1.05, True))
    for i, cx_ in enumerate((640, 1200, 1340)):
        s += SL(Z_DAL, f'<ellipse cx="{cx_:.0f}" cy="250" rx="78" ry="18"'
                       f' fill="url(#krem)" {o(5)}/>'
                       f'<path d="M{cx_-56:.0f},232 q8,-94 56,-98 q48,4 56,98'
                       f' q-56,22 -112,0 Z" fill="url(#krem)" {o(7)}/>'
                       f'<path d="M{cx_+56:.0f},170 q54,26 0,50" fill="none"'
                       f' stroke="url(#krem)" stroke-width="14"/>'
                       f'<path d="M{cx_-44:.0f},150 q44,16 88,0" fill="none"'
                       f' stroke="{TKAN}" stroke-width="9" opacity=".8"/>')
    ch_x = 1000
    s += SL(Z_DAL, f'<path d="M{ch_x-96:.0f},250 q-18,-130 96,-140'
                   f' q114,10 96,140 Z" fill="url(#chug)" {o(7)}/>'
                   f'<path d="M{ch_x+92:.0f},170 q60,-8 48,-60" fill="none"'
                   f' stroke="url(#chug)" stroke-width="18" stroke-linecap="round"/>'
                   f'<path d="M{ch_x-50:.0f},112 q50,-56 100,0" fill="none"'
                   f' stroke="{ZHELEZ}" stroke-width="13"/>')
    tb_x = 300
    s += SL(Z_SRED, f'<rect x="{tb_x-130:.0f}" y="880" width="260" height="40"'
                    f' rx="12" fill="url(#derev)" {o(8)}/>'
                    f'<rect x="{tb_x-110:.0f}" y="920" width="40" height="160"'
                    f' rx="12" fill="url(#derev)" {o(6)}/>'
                    f'<rect x="{tb_x+70:.0f}" y="920" width="40" height="160"'
                    f' rx="12" fill="url(#derev)" {o(6)}/>'
                    f'<rect x="{tb_x-100:.0f}" y="1000" width="200" height="20"'
                    f' rx="8" fill="{DOSKA2}" {o(4)}/>')
    puch_x = 1720
    kach2 = 2.6 * A.w(t, 4.0, .2)
    puch = f'<g transform="rotate({kach2:.2f} {puch_x:.0f} 340)">'
    puch += (f'<path d="M{puch_x-30:.0f},340 q30,-24 60,0" fill="none"'
             f' stroke="{TKAN}" stroke-width="12"/>')
    for j in range(6):
        puch += (f'<path d="M{puch_x:.0f},345 q{-22+j*9:.0f},80 {-30+j*12:.0f},150"'
                 f' fill="none" stroke="{["#6f8c4a", "#8a9a58", "#5c7a40"][j%3]}"'
                 f' stroke-width="11" stroke-linecap="round"/>')
        puch += (f'<ellipse cx="{puch_x-30+j*12:.0f}" cy="500" rx="13" ry="7"'
                 f' fill="#8a9a58" opacity=".9"/>')
    puch += '</g>'
    s += SL(Z_SRED, puch)
    s += SL(Z_PERED, zanaveska(60, 0, 520, 200, TKAN, t, 1))
    s += ramka_pp("pravo", "#160f0a", .42)
    s += vinetka(.46)
    return s


# ── 44 ─────────────────────────────────────────────────────────────────────
def svet_pogas_lampa_zazhglas(t):
    """Вечерняя кухня под абажуром: лампочка мигает и гаснет, в темноте
    остаются одни белки глаз, а потом растёт тёплый круг керосинки."""
    rnd = random.Random(4421)
    s = f'<rect width="{W}" height="{H}" fill="#3c3a42"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#6b5f58"/>')
    for i in range(16):                 # обои в полоску
        s += SL(Z_DAL, f'<rect x="{i*120}" y="0" width="56" height="760"'
                       f' fill="#7a6c62" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect x="0" y="740" width="{W}" height="36" fill="#574c45" {o(4)}/>')
    s += kvartira_veschi(1300, 760, 600, t, 463)
    s += SL(Z_SRED, polovicy(860))
    gas = A.ease(A.seg(t, .9, .3))
    mig = (1.0 if ((t * 5.0) % 1.0) > .35 else .3) * (1 - gas)
    zazh = A.ease(A.seg(t, 1.5, .9))
    st = stol(560, 740, 820, 40)
    s += SL(Z_SRED, st)
    s += SL(Z_SRED, f'<path d="M520,738 h900 l-34,46 h-832 Z" fill="{RUSH}"'
                    f' opacity=".9" {o(5)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{620+i*200:.0f},700 q66,80 132,0'
                        f' q-66,26 -132,0 Z" fill="url(#krem)" {o(6)}/>')
        s += SL(Z_SRED, f'<ellipse cx="{686+i*200:.0f}" cy="694" rx="68" ry="18"'
                        f' fill="#d8cbb0" {o(4)}/>')
    s += SL(Z_SRED, karavay(1310, 724, .95, False))
    s += SL(Z_SRED, par(900, 650, t, 4, .4 * (1 - gas) + .2, 160, .45, .8))
    ab_x, ab_y = 960, 250
    s += SL(Z_SRED, f'<line x1="{ab_x}" y1="0" x2="{ab_x}" y2="{ab_y-40}"'
                    f' stroke="#30343a" stroke-width="8"/>')
    s += SL(Z_SRED, f'<path d="M{ab_x-230},{ab_y+70} L{ab_x-96},{ab_y-40}'
                    f' L{ab_x+96},{ab_y-40} L{ab_x+230},{ab_y+70} Z"'
                    f' fill="{TKAN}" {o(8)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{ab_x-210+i*52:.0f},{ab_y+70}'
                        f' q6,40 {-4+4*A.w(t,2.6,i*.2):.1f},76" fill="none"'
                        f' stroke="{ZOL}" stroke-width="7" opacity=".85"/>')
    s += SL(Z_SRED, f'<circle cx="{ab_x}" cy="{ab_y+40}" r="40" fill="{SVET}"'
                    f' opacity="{mig:.2f}"/>')
    s += SL(Z_SRED, teplo(ab_x, ab_y + 220, 700 * mig + 40, 560 * mig + 40, .5 * mig))
    lamp_x, lamp_y = 1180, 736
    s += SL(Z_SRED, f'<g opacity="{.25+.75*zazh:.2f}">'
                    + lampa(lamp_x, lamp_y, t, .95) + '</g>')
    s += SL(Z_SRED, teplo(lamp_x, lamp_y - 160, 760 * zazh + 30,
                          640 * zazh + 30, .55 * zazh))
    ljudi = ((600, 980, 520, "#4a2f3a", True, .1), (1480, 1000, 540, "#3a4150", False, .4),
             (820, 1056, 390, "#5b4a2f", False, .7), (1300, 1060, 370, "#2f4a44", False, .9))
    for i, (fx, fy, fh, col, pl, ph) in enumerate(ljudi):
        vid_op = max(.1, min(1.0, (1 - gas) + zazh))
        s += SL(Z_SRED, figura(fx, fy, fh, t, col, "#ffd98a", pl, ph, i % 2 == 0,
                               vid_op))
        if gas > .4 and zazh < .5:      # в темноте видны только белки глаз
            for sgn in (-1, 1):
                s += SL(Z_SRED, f'<ellipse cx="{fx+sgn*fh*.045:.0f}"'
                                f' cy="{fy-fh*.855:.0f}" rx="{fh*.028:.0f}"'
                                f' ry="{fh*.018 if A.blink(t,3.4,i*.2) else fh*.030:.1f}"'
                                f' fill="#f6f2e6" opacity="{gas*(1-zazh):.2f}"/>')
    hlop = abs(A.w(t, .42, .1))
    for i, (fx, fy) in enumerate(((820, 1056), (1300, 1060))):
        for sgn in (-1, 1):
            ruk, (hx, hy) = rukav(fx + sgn * 70, fy - 250, 110,
                                  -sgn * (36 + 26 * hlop) - (0 if sgn > 0 else 180),
                                  t, "#5b4a2f" if i == 0 else "#2f4a44",
                                  "#ffd98a", i * .3, 3.0)
            s += SL(Z_SRED, ruk)
            s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="22" ry="17"'
                            f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, f'<rect width="{W}" height="{H}" fill="#0b0d14"'
                    f' opacity="{.66*gas*(1-zazh*.95):.2f}"/>')
    s += ramka_pp("levo", "#0e0c12", .5)
    s += SL(Z_PERED, kot(300, 1070, t, .9, "#49413a"))
    s += vinetka(.5)
    return s


# ── 45 ─────────────────────────────────────────────────────────────────────
def zapas_sveta_na_polke(t):
    """Полка в прихожей на пол-кадра: по одной встают свечи, коробок спичек,
    фонарик и сложенный плед, а в окнах напротив разом гаснет свет."""
    rnd = random.Random(4523)
    s = f'<rect width="{W}" height="{H}" fill="#55616b"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#6d7a84"/>')
    for i in range(13):
        s += SL(Z_DAL, f'<rect x="{i*150}" y="0" width="70" height="1080"'
                       f' fill="#7e8b95" opacity=".45"/>')
    s += SL(Z_DAL, f'<rect x="0" y="880" width="{W}" height="200" fill="#4e5a62" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="866" width="{W}" height="26" fill="#8e9aa2" {o(4)}/>')
    ves = (f'<rect x="80" y="250" width="420" height="30" rx="8" fill="url(#derev)" {o(7)}/>')
    for i in range(4):
        ves += (f'<circle cx="{150+i*110:.0f}" cy="300" r="16" fill="{ZHELEZ}" {o(4)}/>')
        ves += (f'<path d="M{150+i*110:.0f},316 q{-10+6*A.w(t,4.0,i*.2):.1f},120'
                f' {-30+10*A.w(t,4.0,i*.2):.1f},300" fill="none"'
                f' stroke="{[TKAN, TKAN2, "#5b5a4a", "#7a4a3a"][i]}" stroke-width="64"'
                f' stroke-linecap="round" opacity=".92"/>')
    s += SL(Z_DAL, ves)
    pw, px, py = 1120, 700, 620
    pk = (f'<rect x="{px}" y="{py}" width="{pw}" height="44" rx="10"'
          f' fill="url(#derev)" {o(9)}/>')
    pk += (f'<rect x="{px}" y="{py+44}" width="{pw}" height="22" fill="{DOSKA2}" {o(5)}/>')
    for i in range(3):
        pk += (f'<path d="M{px+120+i*420:.0f},{py+66} l40,70 M{px+320+i*420:.0f},'
               f'{py+66} l-40,70" {o(7)} fill="none"/>')
    pk += (f'<rect x="{px}" y="{py-430}" width="{pw}" height="30" rx="8"'
           f' fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, pk)
    for i in range(5):                  # вещи на верхней полке — не пусто
        pk2 = (f'<rect x="{px+60+i*210:.0f}" y="{py-540:.0f}" width="130"'
               f' height="110" rx="10" fill="{["#6b5a3c", TKAN2, "#4a5a4a", MED, "#5b4450"][i]}"'
               f' {o(5)}/>')
        s += SL(Z_SRED, pk2)
    stavit = [A.over(A.seg(t, .3 + i * .36, .5)) for i in range(4)]
    for i in range(3):                  # свечи
        k = stavit[0]
        cx_ = px + 120 + i * 90
        s += SL(Z_SRED, f'<g opacity="{min(1, k):.2f}" transform="translate(0,'
                        f'{(1-k)*-180:.0f})">'
                        + svecha(cx_, py - 150 - i % 2 * 20, t, i * .3, 1.5, 150)
                        + '</g>')
    s += SL(Z_SRED, teplo(px + 200, py - 240, 460, 400, .4 + .12 * abs(A.w(t, 1.4))))
    k = stavit[1]                       # коробок спичек
    kx_ = px + 440
    s += SL(Z_SRED, f'<g opacity="{min(1, k):.2f}" transform="translate(0,'
                    f'{(1-k)*-200:.0f})">'
                    f'<rect x="{kx_:.0f}" y="{py-130:.0f}" width="190" height="130"'
                    f' rx="10" fill="{TKAN}" {o(7)}/>'
                    f'<rect x="{kx_+16:.0f}" y="{py-110:.0f}" width="158" height="60"'
                    f' rx="6" fill="#e8d6b2" {o(4)}/>'
                    f'<rect x="{kx_:.0f}" y="{py-40:.0f}" width="190" height="40"'
                    f' fill="#5e4a3a" opacity=".85"/></g>')
    k = stavit[2]                       # фонарик
    fx_ = px + 700
    s += SL(Z_SRED, f'<g opacity="{min(1, k):.2f}" transform="translate(0,'
                    f'{(1-k)*-220:.0f})">'
                    f'<rect x="{fx_:.0f}" y="{py-96:.0f}" width="230" height="96"'
                    f' rx="22" fill="#2f3a44" {o(7)}/>'
                    f'<path d="M{fx_+220:.0f},{py-120:.0f} h70 l16,120 h-86 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<ellipse cx="{fx_+300:.0f}" cy="{py-60:.0f}" rx="16" ry="60"'
                    f' fill="url(#stekl)" opacity=".9" {o(4)}/>'
                    f'<rect x="{fx_+40:.0f}" y="{py-72:.0f}" width="60" height="30"'
                    f' rx="8" fill="{KRAS}" {o(4)}/></g>')
    k = stavit[3]                       # плед
    gx_ = px + 940
    spol = 26 * A.ease(A.seg(t, 3.0, 1.2))
    s += SL(Z_SRED, f'<g opacity="{min(1, k):.2f}" transform="translate(0,'
                    f'{(1-k)*-240+spol:.0f})">'
                    f'<rect x="{gx_:.0f}" y="{py-170:.0f}" width="210" height="170"'
                    f' rx="14" fill="{TKAN2}" {o(8)}/>'
                    + "".join(f'<rect x="{gx_:.0f}" y="{py-150+j*44:.0f}" width="210"'
                              f' height="18" fill="#e8d6b2" opacity=".65"/>'
                              for j in range(3))
                    + f'<path d="M{gx_:.0f},{py-170:.0f} q105,30 210,0" fill="none"'
                    f' stroke="#1d2a38" stroke-width="7"/></g>')
    ox, oy, ow, oh = 110, 420, 460, 380
    gas = A.ease(A.seg(t, 2.2, .5))
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#141b28"/>')
    for r in range(4):
        for c in range(4):
            on = ((r + c) % 2 == 0) and gas < .5
            za += (f'<rect x="{ox+40+c*100:.0f}" y="{oy+40+r*86:.0f}" width="68"'
                   f' height="58" rx="5" fill="{SVET if on else "#2b3648"}"'
                   f' opacity="{.45+.45*abs(A.w(t,6+c,r*.2)) if on else .5:.2f}"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.8:.0f}" width="{ow}" height="{oh*.2:.0f}"'
           f' fill="#1b2430"/>')
    s += SL(Z_SRED, f'<clipPath id="ok45"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok45)">{za}</g>')
    ram = (f'<rect x="{ox-26}" y="{oy-26}" width="{ow+52}" height="{oh+52}" rx="8"'
           f' fill="none" stroke="#dfe6ea" stroke-width="54"/>')
    ram += (f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}" y2="{oy+oh}"'
            f' stroke="#dfe6ea" stroke-width="20"/>')
    ram += (f'<rect x="{ox-40}" y="{oy+oh+26}" width="{ow+80}" height="30" rx="8"'
            f' fill="#cfd8dc" {o(5)}/>')
    s += SL(Z_SRED, ram)
    vz = A.ease(A.seg(t, 3.2, 1.0))
    ruk, (hx, hy) = rukav(1870, 760, 300, 196 - 14 * vz, t, "#3a4150", "#cfe4f5", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="34" ry="24"'
                    f' fill="#3a4150" {o(5)}/>')
    kov = (f'<rect x="120" y="940" width="760" height="140" rx="16"'
           f' fill="#7a3a42" {o(7)}/>')
    for i in range(6):
        kov += (f'<rect x="{150+i*120:.0f}" y="960" width="90" height="100" rx="8"'
                f' fill="#9c4a52" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, kov)
    for i, (bx_, col) in enumerate(((190, "#4a3f36"), (380, "#5b4450"),
                                    (560, "#2f3a44"), (740, "#6b5a3c"))):
        s += SL(Z_SRED, f'<path d="M{bx_-70:.0f},{980+((i%2)*26):.0f}'
                        f' q12,-56 76,-56 q70,0 76,48 q-6,30 -76,30'
                        f' q-64,0 -76,-22 Z" fill="{col}" {o(6)}/>'
                        f'<path d="M{bx_-54:.0f},{956+((i%2)*26):.0f} q58,-30 110,4"'
                        f' fill="none" stroke="#cfd6dc" stroke-width="9" opacity=".6"/>')
    zr_x, zr_y = 1700, 560
    s += SL(Z_SRED, f'<rect x="{zr_x-130:.0f}" y="{zr_y-250:.0f}" width="260"'
                    f' height="500" rx="18" fill="#cfd6dc" {o(8)}/>'
                    f'<rect x="{zr_x-104:.0f}" y="{zr_y-224:.0f}" width="208"'
                    f' height="448" rx="12" fill="#9fb6c6" {o(5)}/>'
                    f'<path d="M{zr_x-80:.0f},{zr_y-180:.0f} l120,180"'
                    f' stroke="#ffffff" stroke-width="18" opacity=".3"/>')
    s += SL(Z_SRED, f'<g opacity=".55">'
                    + svecha(zr_x - 20, zr_y + 120, t, .4, 1.1, 110) + '</g>')
    for i in range(4):                  # крючки с ключами
        s += SL(Z_SRED, f'<circle cx="{1380+i*70:.0f}" cy="330" r="12"'
                        f' fill="{ZHELEZ}" {o(4)}/>'
                        f'<path d="M{1380+i*70:.0f},342 q{-6+4*A.w(t,3.4,i*.2):.1f},36'
                        f' {2:.0f},70" fill="none" stroke="url(#zhel)"'
                        f' stroke-width="7"/>'
                        f'<circle cx="{1382+i*70:.0f}" cy="{418:.0f}" r="14"'
                        f' fill="none" stroke="{MED}" stroke-width="7"/>')
    s += SL(Z_SRED, f'<path d="M1240,360 q-16,260 -30,420" fill="none"'
                    f' stroke="#2f4a7a" stroke-width="54" stroke-linecap="round"/>'
                    f'<path d="M1240,360 q40,-60 90,-10" fill="none"'
                    f' stroke="#2f3a44" stroke-width="14" stroke-linecap="round"/>')
    s += SL(Z_SRED, kot(980, 1050, t, .85, "#3b3430"))
    s += ramka_pp("pravo", "#141a20", .42)
    s += vinetka(.44)
    return s


# ── 46 ─────────────────────────────────────────────────────────────────────
def rastopka_u_pechki(t):
    """Пол у печной дверцы: в плетёную корзину на пол-кадра ложатся смолистые
    щепки, свёрнутая береста и скрученная газета, топорик колет лучину."""
    rnd = random.Random(4639)
    s = f'<rect width="{W}" height="{H}" fill="#2f241a"/>'
    s += SL(Z_DAL, brevna(0, 0, 720, 820, 104))
    s += SL(Z_DAL, f'<rect x="700" y="0" width="1220" height="900" fill="url(#pech)"'
                   f' opacity=".97"/>')
    s += SL(Z_DAL, kladka(700, 0, 1220, 360, 90, "url(#pech)"))
    s += utvar_izby(60, 240, 420, t, 467)
    s += SL(Z_SRED, polovicy(880))
    dvx, dvy, dvw, dvh = 1360, 420, 380, 330
    dvr = (f'<rect x="{dvx-34}" y="{dvy-34}" width="{dvw+68}" height="{dvh+68}"'
           f' rx="12" fill="{CHUGUN}" {o(9)}/>')
    dvr += (f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}" rx="8"'
            f' fill="#160c06"/>')
    s += SL(Z_SRED, dvr)
    s += SL(Z_SRED, ugli(dvx + 40, dvy + dvh - 50, dvw - 80, t, 8, 479)
                    + ogon(dvx + dvw * .5, dvy + dvh - 36, t, 1.25, .2, 7))
    s += SL(Z_SRED, iskra_let(t, dvx + dvw * .5, dvy + dvh - 90, 9, 487, 280, .5))
    s += SL(Z_SRED, teplo(dvx + dvw * .5, dvy + dvh * .7, 560, 460,
                          .46 + .14 * abs(A.w(t, 1.3))))
    dvr2 = (f'<path d="M{dvx+dvw+34:.0f},{dvy+dvh*.5:.0f} h56" stroke="url(#zhel)"'
            f' stroke-width="16" stroke-linecap="round"/>')
    dvr2 += (f'<circle cx="{dvx+dvw+96:.0f}" cy="{dvy+dvh*.5:.0f}" r="22"'
             f' fill="url(#zhel)" {o(5)}/>')
    for i in range(4):
        dvr2 += (f'<circle cx="{dvx-20+i*(dvw/3):.0f}" cy="{dvy-20}" r="11"'
                 f' fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, dvr2)
    kx, ky = 820, 1000
    s += SL(Z_SRED, _korzina(kx, ky, 620, 440, t, 491, False))
    for i in range(11):                 # щепки сыплются в корзину
        p = A.ease(A.seg(t, .3 + i * .13, .7))
        sx_ = kx - 230 + i * 46
        sy_ = 300 + p * (ky - 420 - 300) + (1 - p) * -60
        ug = -40 + i * 16 + (1 - p) * 120
        s += SL(Z_SRED, f'<g transform="rotate({ug:.0f} {sx_:.0f} {sy_:.0f})">'
                        f'<rect x="{sx_-12:.0f}" y="{sy_-70:.0f}" width="24"'
                        f' height="140" rx="7" fill="url(#derev)" {o(4)}/>'
                        f'<rect x="{sx_-6:.0f}" y="{sy_-60:.0f}" width="7"'
                        f' height="118" fill="#c49a5c" opacity=".8"/></g>')
    ber = A.ease(A.seg(t, 2.2, 1.4))
    bx_, by_ = kx + 150, ky - 500
    s += SL(Z_SRED, f'<g transform="rotate({-18+28*ber:.1f} {bx_:.0f} {by_:.0f})">'
                    f'<path d="M{bx_-130:.0f},{by_:.0f} q130,{-60-60*ber:.0f} 260,0'
                    f' q-130,{70+40*ber:.0f} -260,0 Z" fill="#efe8dc" {o(6)}/>'
                    + "".join(f'<path d="M{bx_-100+j*52:.0f},{by_-30:.0f} l0,46"'
                              f' stroke="#2f2a26" stroke-width="8"'
                              f' stroke-linecap="round" opacity=".8"/>' for j in range(4))
                    + f'<path d="M{bx_-130:.0f},{by_:.0f} q130,{40+30*ber:.0f} 260,0"'
                    f' fill="none" stroke="#b9ab97" stroke-width="6"/></g>')
    s += SL(Z_SRED, _gazeta(kx - 330, ky - 560, 250, 180, -24 + 10 * A.w(t, 2.0), 499))
    skr = A.ease(A.seg(t, 3.4, 1.6))
    s += SL(Z_SRED, f'<g transform="rotate({40*skr:.0f} {kx-130:.0f} {ky-330:.0f})">'
                    f'<path d="M{kx-190:.0f},{ky-330:.0f} q60,{-40+20*skr:.0f}'
                    f' 120,0 l-14,{150-40*skr:.0f} q-46,20 -92,0 Z"'
                    f' fill="url(#list)" {o(6)}/>'
                    + "".join(f'<path d="M{kx-176+j*30:.0f},{ky-300:.0f} l-6,100"'
                              f' stroke="#9c948a" stroke-width="5"/>' for j in range(4))
                    + '</g>')
    tp_a = -62 + 58 * abs(A.w(t, .8, .1))
    tx_, ty_ = 380, 900
    s += SL(Z_SRED, f'<rect x="{tx_-180:.0f}" y="{ty_-30:.0f}" width="420"'
                    f' height="56" rx="12" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<g transform="rotate({tp_a:.0f} {tx_:.0f} {ty_-180:.0f})">'
                    f'<rect x="{tx_-20:.0f}" y="{ty_-430:.0f}" width="40" height="300"'
                    f' rx="12" fill="url(#derev)" {o(6)}/>'
                    f'<path d="M{tx_-24:.0f},{ty_-470:.0f} q120,-40 150,30'
                    f' l-34,110 q-60,-34 -116,-26 Z" fill="url(#zhel)" {o(7)}/>'
                    f'<path d="M{tx_+96:.0f},{ty_-440:.0f} q34,60 10,120"'
                    f' fill="none" stroke="#eef4f8" stroke-width="12" opacity=".6"/></g>')
    for i in range(6):                  # лучинки разлетаются
        p = ((t * .8) + i * .16) % 1.0
        s += SL(Z_SRED, f'<rect x="{tx_+60+p*180:.0f}" y="{ty_-90-p*120+p*p*180:.0f}"'
                        f' width="14" height="70" rx="5" fill="#c49a5c"'
                        f' opacity="{1-p*.7:.2f}" transform="rotate({p*160:.0f}'
                        f' {tx_+66+p*180:.0f} {ty_-60-p*120:.0f})" {o(3)}/>')
    s += SL(Z_SRED, kot(1620, 1040, t, 1.05, "#8a7a68"))
    s += SL(Z_SRED, par(1620, 980, t, 3, .3, 110, .5, .6))
    s += ramka_pp("levo", "#160e08", .46)
    s += SL(Z_PERED, krynka(1830, 1070, 1.5))
    s += vinetka(.46)
    return s


# ── 47 ─────────────────────────────────────────────────────────────────────
def fonarik_v_yaschike_komoda(t):
    """Корзина со щепками оборачивается выдвинутым ящиком комода: среди
    катушек и квитанций лежит большой фонарик, и луч вспыхивает в пыли."""
    rnd = random.Random(4703)
    s = f'<rect width="{W}" height="{H}" fill="#2a2630"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#3e3a46"/>')
    for i in range(12):
        s += SL(Z_DAL, f'<rect x="{i*170}" y="0" width="76" height="1080"'
                       f' fill="#474350" opacity=".6"/>')
    s += kvartira_veschi(60, 820, 520, t, 503)
    s += SL(Z_SRED, polovicy(900))
    km_x, km_y, km_w = 620, 940, 1120
    km = ten(km_x + km_w / 2, km_y + 16, km_w * .5, 24, .5)
    km += (f'<rect x="{km_x}" y="{km_y-700}" width="{km_w}" height="700" rx="14"'
           f' fill="url(#derev)" {o(9)}/>')
    km += (f'<rect x="{km_x-24}" y="{km_y-740}" width="{km_w+48}" height="46" rx="12"'
           f' fill="{DOSKA2}" {o(7)}/>')
    for r in range(2):
        km += (f'<rect x="{km_x+40}" y="{km_y-660+r*180:.0f}" width="{km_w-80}"'
               f' height="150" rx="10" fill="{DOSKA2}" {o(6)}/>')
        for c in (-1, 1):
            km += (f'<circle cx="{km_x+km_w/2+c*180:.0f}" cy="{km_y-585+r*180:.0f}"'
                   f' r="20" fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, km)
    prev = A.ease(A.seg(t, .2, .8))
    yx, yy, yw, yh = 560, 920, 1240, 430
    ya = (f'<path d="M{yx:.0f},{yy-yh:.0f} h{yw:.0f} l-50,{yh:.0f} h{-yw+100:.0f} Z"'
          f' fill="#6b4a2c" {o(9)}/>')
    ya += (f'<rect x="{yx-30:.0f}" y="{yy-yh-54:.0f}" width="{yw+60:.0f}" height="64"'
           f' rx="14" fill="url(#derev)" {o(9)}/>')
    ya += (f'<rect x="{yx+40:.0f}" y="{yy-yh-40:.0f}" width="{yw-80:.0f}" height="36"'
           f' rx="10" fill="{DOSKA2}" opacity=".8"/>')
    for c in (-1, 1):
        ya += (f'<circle cx="{yx+yw/2+c*260:.0f}" cy="{yy-yh-22:.0f}" r="22"'
               f' fill="url(#zhel)" {o(5)}/>')
    ya += (f'<path d="M{yx+30:.0f},{yy-yh+20:.0f} h{yw-60:.0f} l-40,{yh-50:.0f}'
           f' h{-yw+140:.0f} Z" fill="#3a2a1c" {o(5)}/>')
    s += SL(Z_SRED, ya)
    kor_op = 1 - prev
    if kor_op > .02:
        s += SL(Z_SRED, f'<g opacity="{kor_op:.2f}">'
                        + _korzina(yx + yw / 2, yy, 860, 420, t, 509, False) + '</g>')
    for i in range(9):                  # катушки ниток в ящике
        cx_ = yx + 110 + i * 86
        cy_ = yy - 110 - (i % 3) * 36
        col = ["#8f3a42", "#3a5a8f", "#4a7a4a", "#8a6a2a", "#6b4a6a"][i % 5]
        s += SL(Z_SRED, f'<g opacity="{prev:.2f}">'
                        f'<rect x="{cx_-24:.0f}" y="{cy_-44:.0f}" width="48"'
                        f' height="88" rx="8" fill="{col}" {o(4)}/>'
                        f'<ellipse cx="{cx_:.0f}" cy="{cy_-44:.0f}" rx="30" ry="10"'
                        f' fill="url(#derev)" {o(3)}/>'
                        f'<ellipse cx="{cx_:.0f}" cy="{cy_+44:.0f}" rx="30" ry="10"'
                        f' fill="url(#derev)" {o(3)}/></g>')
    for i in range(4):                  # квитанции
        s += SL(Z_SRED, f'<g opacity="{prev:.2f}">'
                        + _gazeta(yx + 190 + i * 150, yy - 250 - (i % 2) * 40, 190, 120,
                                  -22 + i * 13, 521) + '</g>')
    fx_, fy_ = yx + 820, yy - 180
    vsp = 1.0 if ((t * 1.3) % 1.0) > .42 else .25
    fon = (f'<g opacity="{prev:.2f}">'
           f'<rect x="{fx_-200:.0f}" y="{fy_-74:.0f}" width="400" height="148"'
           f' rx="34" fill="#2f3a44" {o(9)}/>')
    for i in range(7):
        fon += (f'<rect x="{fx_-170+i*46:.0f}" y="{fy_-70:.0f}" width="20"'
                f' height="140" rx="8" fill="#243038" opacity=".9"/>')
    fon += (f'<path d="M{fx_+190:.0f},{fy_-108:.0f} h96 l26,216 h-122 Z"'
            f' fill="{ZHELEZ}" {o(8)}/>')
    fon += (f'<ellipse cx="{fx_+312:.0f}" cy="{fy_+2:.0f}" rx="26" ry="108"'
            f' fill="url(#stekl)" opacity=".92" {o(6)}/>')
    fon += (f'<ellipse cx="{fx_+312:.0f}" cy="{fy_+2:.0f}" rx="18" ry="86"'
            f' fill="{SVET}" opacity="{vsp:.2f}"/>')
    fon += (f'<rect x="{fx_-120:.0f}" y="{fy_-100:.0f}" width="90" height="40"'
            f' rx="10" fill="{KRAS}" {o(5)}/>')
    fon += '</g>'
    s += SL(Z_SRED, fon)
    s += SL(Z_SRED, f'<g opacity="{prev*vsp:.2f}">'
                    + luch(fx_ + 330, fy_ - 120, 300, 560, t, .30) + '</g>')
    s += SL(Z_SRED, teplo(fx_ + 380, fy_ + 60, 420 * vsp, 340 * vsp, .4 * prev * vsp))
    for i in range(18):                 # пылинки пляшут в луче
        p = ((t * .22) + i * .055) % 1.0
        s += SL(Z_SRED, f'<circle cx="{fx_+340+p*420+40*A.w(t,3.4+i*.2,i*.1):.0f}"'
                        f' cy="{fy_-80+p*420+30*A.w(t,2.6,i*.13):.0f}"'
                        f' r="{2.4+2.6*(1-p):.1f}" fill="#fff6dd"'
                        f' opacity="{prev*vsp*(1-p)*.9:.2f}"/>')
    vz = A.ease(A.seg(t, 1.4, 1.1))
    ruk, (hx, hy) = rukav(fx_ - 260, 300 + vz * 120, 190, 74, t, "#3a4150",
                          "#cfe4f5", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="38" ry="26"'
                    f' fill="#3a4150" {o(5)}/>')
    s += SL(Z_SRED, svecha(1780, 180, t, .2, 1.7, 150))
    s += SL(Z_SRED, teplo(1800, 150, 460, 420, .4 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, hodiki(300, 300, t, 1.15))
    for i in range(3):                  # тени отпрыгивают в углы
        s += SL(Z_SRED, f'<ellipse cx="{200+i*760:.0f}" cy="{1000:.0f}"'
                        f' rx="{200+80*vsp:.0f}" ry="{70+20*vsp:.0f}" fill="#13111a"'
                        f' opacity="{.5-.22*vsp:.2f}"/>')
    s += ramka_pp("oba", "#120f16", .5)
    s += vinetka(.5)
    return s


# ── 48 ─────────────────────────────────────────────────────────────────────
def odeyalo_i_noski_nagotove(t):
    """Стул у кровати на пол-кадра: на него ложится толстое стёганое одеяло,
    сверху падают шерстяные носки с узором, запрыгивает кот."""
    rnd = random.Random(4801)
    s = f'<rect width="{W}" height="{H}" fill="#3a3640"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#55505e"/>')
    for i in range(10):
        s += SL(Z_DAL, f'<path d="M{80+i*200},0 q30,540 0,1080" fill="none"'
                       f' stroke="#5f5a6c" stroke-width="40" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect x="0" y="930" width="{W}" height="150" fill="#4a4550" {o(5)}/>')
    krv = (f'<rect x="1180" y="430" width="760" height="70" rx="16"'
           f' fill="url(#derev)" {o(9)}/>')
    krv += (f'<rect x="1180" y="500" width="40" height="440" rx="12"'
            f' fill="url(#derev)" {o(7)}/>')
    krv += (f'<rect x="1230" y="660" width="720" height="250" rx="18"'
            f' fill="{TKAN2}" {o(8)}/>')
    krv += (f'<path d="M1250,680 q180,-120 400,-40 l0,60 q-200,-60 -400,40 Z"'
            f' fill="#eef2f6" {o(6)}/>')
    for i in range(5):
        krv += (f'<path d="M{1280+i*140:.0f},760 q60,40 0,120" fill="none"'
                f' stroke="#5e7ea0" stroke-width="10" opacity=".7"/>')
    for i in range(4):
        krv += (f'<rect x="{1230+i*230:.0f}" y="900" width="36" height="140" rx="10"'
                f' fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, krv)
    tb = (f'<rect x="940" y="700" width="230" height="300" rx="12"'
          f' fill="url(#derev)" {o(8)}/>')
    tb += (f'<rect x="920" y="676" width="270" height="36" rx="10" fill="{DOSKA2}" {o(6)}/>')
    tb += (f'<rect x="962" y="760" width="186" height="80" rx="8" fill="{DOSKA2}" {o(5)}/>')
    tb += (f'<circle cx="1055" cy="800" r="14" fill="url(#zhel)" {o(4)}/>')
    s += SL(Z_SRED, tb)
    s += SL(Z_SRED, svecha(1000, 540, t, .1, 1.5, 140))
    s += SL(Z_SRED, teplo(1010, 520, 540, 480, .44 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, f'<path d="M1110,676 q40,-96 76,0 q-38,22 -76,0 Z"'
                    f' fill="url(#stekl)" opacity=".9" {o(5)}/>')
    sx, sy = 540, 980
    st = ten(sx, sy + 14, 180, 24, .5)
    st += (f'<rect x="{sx-170:.0f}" y="{sy-560:.0f}" width="54" height="560" rx="12"'
           f' fill="url(#derev)" {o(8)}/>')
    st += (f'<rect x="{sx+116:.0f}" y="{sy-560:.0f}" width="54" height="560" rx="12"'
           f' fill="url(#derev)" {o(8)}/>')
    for i in range(3):
        st += (f'<rect x="{sx-170:.0f}" y="{sy-540+i*86:.0f}" width="340" height="40"'
               f' rx="12" fill="{DOSKA2}" {o(6)}/>')
    st += (f'<rect x="{sx-200:.0f}" y="{sy-300:.0f}" width="400" height="60" rx="14"'
           f' fill="url(#derev)" {o(9)}/>')
    for dx in (-180, 160):
        st += (f'<rect x="{sx+dx:.0f}" y="{sy-240:.0f}" width="40" height="240"'
               f' rx="10" fill="url(#derev)" {o(7)}/>')
    st += (f'<rect x="{sx-160:.0f}" y="{sy-130:.0f}" width="320" height="26"'
           f' rx="8" fill="{DOSKA2}" {o(5)}/>')
    s += SL(Z_SRED, st)
    lozh = A.out(A.seg(t, .3, 1.2))
    oy_ = sy - 300 - (1 - lozh) * 420
    od = f'<g transform="translate(0,{oy_-(sy-300):.0f})">'
    od += (f'<path d="M{sx-230:.0f},{sy-300:.0f} q{230:.0f},-110 {460:.0f},0'
           f' q{-20:.0f},160 {-40:.0f},260 q{-200:.0f},70 {-400:.0f},0 Z"'
           f' fill="{TKAN}" {o(9)}/>')
    for r in range(3):
        for c in range(5):
            od += (f'<rect x="{sx-200+c*84:.0f}" y="{sy-310+r*76:.0f}" width="70"'
                   f' height="62" rx="14" fill="#c2574e" opacity=".85"'
                   f' stroke="#7a1c22" stroke-width="5"/>')
    od += (f'<path d="M{sx-230:.0f},{sy-40:.0f} q230,60 460,0" fill="none"'
           f' stroke="#efe3c8" stroke-width="12" opacity=".7"/>')
    od += '</g>'
    s += SL(Z_SRED, od)
    for i in range(2):                  # носки падают сверху
        pd = A.out(A.seg(t, 1.5 + i * .3, .9))
        nx = sx - 70 + i * 150
        ny = -160 + pd * (sy - 400)
        ug = -30 + 70 * pd + 10 * A.w(t, 1.2, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({ug:.0f} {nx:.0f} {ny:.0f})">'
                        f'<path d="M{nx-50:.0f},{ny-110:.0f} h100 l0,120'
                        f' q0,60 -60,70 q-80,10 -90,-40 q-6,-40 50,-50 Z"'
                        f' fill="#e8dcc0" {o(7)}/>'
                        + "".join(f'<path d="M{nx-50:.0f},{ny-80+j*34:.0f} h100"'
                                  f' stroke="{[TKAN, ZEL2, TKAN2][j%3]}"'
                                  f' stroke-width="11" opacity=".9"/>' for j in range(3))
                        + f'<path d="M{nx-50:.0f},{ny-110:.0f} h100" stroke="#b9a884"'
                        f' stroke-width="10"/></g>')
    pryg = A.out(A.seg(t, 3.0, .9))
    s += SL(Z_SRED, kot(sx + 230, sy - pryg * 300, t, 1.0 - .15 * pryg, "#3b3430"))
    lucha = -26 + 52 * A.w(t, 2.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({lucha:.0f} 120 980)" opacity=".5">'
                    + luch(120, 420, 240, 560, t, .26) + '</g>')
    s += SL(Z_SRED, f'<rect x="60" y="900" width="260" height="110" rx="26"'
                    f' fill="#2f3a44" {o(7)}/>'
                    f'<ellipse cx="330" cy="950" rx="24" ry="56" fill="{SVET}"'
                    f' opacity="{.5+.4*abs(A.w(t,1.8)):.2f}" {o(4)}/>')
    s += SL(Z_SRED, _vedro(1740, 1060, .9, t, False, "#6b5a4a"))
    kov = (f'<rect x="300" y="1000" width="760" height="80" rx="14"'
           f' fill="#5b3a44" {o(7)}/>')
    for i in range(7):
        kov += (f'<rect x="{330+i*104:.0f}" y="1014" width="76" height="60" rx="8"'
                f' fill="#7a4a56" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, kov)
    for i, sgn in enumerate((-1, 1)):   # валенки под стулом
        vx_ = sx + sgn * 90
        s += SL(Z_SRED, f'<path d="M{vx_-46:.0f},{sy+70:.0f} l0,-150'
                        f' q46,-24 92,0 l0,150 q-46,22 -92,0 Z" fill="#9c9282" {o(6)}/>'
                        f'<path d="M{vx_-46:.0f},{sy+40:.0f} q46,26 92,0"'
                        f' fill="none" stroke="#7a7266" stroke-width="8"/>')
    km = (f'<rect x="60" y="560" width="420" height="440" rx="14"'
          f' fill="url(#derev)" {o(9)}/>')
    km += (f'<rect x="44" y="530" width="452" height="40" rx="12" fill="{DOSKA2}" {o(6)}/>')
    for r in range(3):
        km += (f'<rect x="90" y="{600+r*140:.0f}" width="360" height="118" rx="10"'
               f' fill="{DOSKA2}" {o(5)}/>')
        for c in (-1, 1):
            km += (f'<circle cx="{270+c*110:.0f}" cy="{659+r*140:.0f}" r="16"'
                   f' fill="url(#zhel)" {o(4)}/>')
    s += SL(Z_SRED, km)
    s += SL(Z_SRED, hodiki(270, 380, t, 1.0))
    s += ramka_pp("levo", "#141019", .45)
    s += vinetka(.48)
    return s


# ── 49 ─────────────────────────────────────────────────────────────────────
def porog_svoe_i_chuzhoe(t):
    """Порог избы сбоку: решето и платок замирают над светящейся чертой
    порога — хозяйка забирает решето, гостья прижимает платок к груди."""
    rnd = random.Random(4903)
    s = f'<rect width="{W}" height="{H}" fill="#241a12"/>'
    s += nebo("sumer", t, False, 541)
    s += SL(Z_DAL, f'<rect x="0" y="0" width="900" height="1080" fill="#2a1f16"/>')
    s += SL(Z_DAL, brevna(0, 0, 900, 1080, 108))
    s += ulica_dal(980, 700, 900, t, False, 547)
    s += SL(Z_DAL, gryaz_polosa(760, 170, "#3c332a"))
    kos = (f'<rect x="860" y="0" width="120" height="900" rx="14"'
           f' fill="url(#derev)" {o(10)}/>')
    kos += (f'<rect x="860" y="0" width="1060" height="130" rx="14"'
            f' fill="{DOSKA2}" {o(10)}/>')
    for i in range(7):
        kos += (f'<path d="M{1000+i*120:.0f},20 q28,40 0,84" fill="none"'
                f' stroke="#5a3a22" stroke-width="8" opacity=".7"/>')
    s += SL(Z_SRED, kos)
    por = (f'<path d="M820,800 h1100 l0,120 h-1100 Z" fill="url(#dosk)" {o(10)}/>')
    por += (f'<path d="M820,780 h1100 l0,30 h-1100 Z" fill="{DOSKA2}" {o(7)}/>')
    por += (f'<path d="M820,920 h1100 l0,60 h-1100 Z" fill="#5a3a22" {o(8)}/>')
    for i in range(8):
        por += (f'<path d="M{880+i*130:.0f},812 q24,54 0,100" fill="none"'
                f' stroke="#6b4a2a" stroke-width="9" opacity=".6"/>')
    s += SL(Z_SRED, por)
    s += SL(Z_SRED, polovicy(980))
    sv = .5 + .4 * abs(A.w(t, 1.3))
    cher = (f'<path d="M840,790 q270,-16 540,-4 q270,12 540,-6" fill="none"'
            f' stroke="{SVET}" stroke-width="54" opacity="{sv*.4:.2f}"/>')
    cher += (f'<path d="M840,790 q270,-16 540,-4 q270,12 540,-6" fill="none"'
             f' stroke="#ffffff" stroke-width="22" opacity="{sv:.2f}"'
             f' stroke-linecap="round"/>')
    for i in range(12):
        cher += (f'<circle cx="{880+i*92:.0f}" cy="{786+((i%3)-1)*5}"'
                 f' r="{6+5*abs(A.w(t,1.5,i*.12)):.1f}" fill="#fff6dd"'
                 f' opacity="{.45+.45*abs(A.w(t,1.2,i*.1)):.2f}"/>')
    s += SL(Z_SRED, cher)
    s += SL(Z_SRED, teplo(1380, 790, 620, 180, .32 * sv))
    svetec = (f'<rect x="946" y="640" width="36" height="300" rx="10"'
              f' fill="url(#derev)" {o(6)}/>'
              f'<path d="M906,660 q58,-40 116,0 l-14,46 q-44,-24 -88,0 Z"'
              f' fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, svetec)
    s += SL(Z_SRED, luchina(964, 640, t, 1.9, .2))
    s += SL(Z_SRED, teplo(950, 500, 520, 460, .42 + .12 * abs(A.w(t, 1.4))))
    zab = A.ease(A.seg(t, 1.6, 1.1))
    hx = 700
    s += SL(Z_SRED, figura(hx, 980, 620, t, "#5b2f3a", "#ffd98a", True, .2, True))
    ruk, (rx2, ry2) = rukav(hx + 150, 640, 230 - 40 * zab, 16 - 26 * zab, t,
                            "#5b2f3a", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    sit_x, sit_y = rx2 + 70, ry2 + 20
    sit = (f'<path d="M{sit_x-132:.0f},{sit_y-40:.0f} q132,-70 264,0 l-14,96'
           f' q-118,66 -236,0 Z" fill="url(#solom)" {o(8)}/>')
    sit += (f'<ellipse cx="{sit_x:.0f}" cy="{sit_y-40:.0f}" rx="132" ry="56"'
            f' fill="#c9a877" {o(6)}/>')
    sit += (f'<ellipse cx="{sit_x:.0f}" cy="{sit_y-40:.0f}" rx="112" ry="44"'
            f' fill="#9c7a42" opacity=".7"/>')
    for i in range(9):                  # сетка решета по эллипсу
        kx_ = -112 + i * 28
        hr = (1 - (kx_ / 118.0) ** 2) ** .5 * 44
        sit += (f'<line x1="{sit_x+kx_:.0f}" y1="{sit_y-40-hr:.0f}"'
                f' x2="{sit_x+kx_:.0f}" y2="{sit_y-40+hr:.0f}" stroke="#8a6534"'
                f' stroke-width="5" opacity=".85"/>')
        sit += (f'<path d="M{sit_x-112:.0f},{sit_y-62+i*11:.0f}'
                f' q112,{22-i*4:.0f} 224,0" fill="none" stroke="#8a6534"'
                f' stroke-width="4" opacity=".75"/>')
    s += SL(Z_SRED, sit)
    prizh = A.ease(A.seg(t, 2.0, 1.2))
    gx = 1600
    s += SL(Z_SRED, figura(gx, 990, 580, t, "#36415a", "#cfe4f5", True, .6, True,
                           1.0, True))
    s += SL(Z_SRED, para_izo_rta(gx - 40, 520, t, .3, 1.1, .5))
    ruk2, (px2, py2) = rukav(gx - 140, 660, 200 - 70 * prizh, 196 + 24 * prizh, t,
                             "#36415a", "#cfe4f5", .4, 4.0)
    s += SL(Z_SRED, ruk2)
    kach = 7 * A.w(t, 1.7, .1) * (1 - prizh)
    pl = f'<g transform="rotate({kach:.1f} {px2:.0f} {py2:.0f})">'
    pl += (f'<path d="M{px2-140:.0f},{py2-40:.0f} q140,-60 280,0'
           f' q-20,120 -60,180 q-80,70 -160,0 q-40,-60 -60,-180 Z"'
           f' fill="{TKAN}" {o(8)}/>')
    pl += (f'<path d="M{px2-140:.0f},{py2-40:.0f} q140,56 280,0" fill="none"'
           f' stroke="#f2e2c8" stroke-width="12" opacity=".7"/>')
    for i in range(4):
        pl += (f'<path d="M{px2-100+i*62:.0f},{py2-10:.0f} q20,110 -10,210"'
               f' fill="none" stroke="#f2e2c8" stroke-width="7" opacity=".6"/>')
    for i in range(7):
        pl += (f'<path d="M{px2-110+i*38:.0f},{py2+218:.0f} l{-6+i*2},46"'
               f' stroke="{TKAN}" stroke-width="7" stroke-linecap="round"/>')
    pl += '</g>'
    s += SL(Z_SRED, pl)
    s += SL(Z_SRED, krynka(1030, 1060, 1.3))
    s += SL(Z_SRED, kura(1820, 940, t, .9, .4))
    s += ramka_pp("levo", "#160f0a", .5)
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 557, .38, .8))
    s += vinetka(.46)
    return s


# ── 50 ─────────────────────────────────────────────────────────────────────
def hozyain_zaslonyaet_svoe_dobro(t):
    """Широкоплечий хозяин в дверях сарая раскинул руки, а за его спиной
    жмётся друг к другу утварь с испуганными глазками."""
    rnd = random.Random(5003)
    s = sumerki_fon(t, True)
    s += ulica_dal(40, 720, 700, t, False, 563)
    s += SL(Z_DAL, gryaz_polosa(800, 180, "#443a30"))
    sar = doski(420, 120, 1180, 780, 84, True, "dosk")
    sar += (f'<path d="M380,130 L1010,-150 L1640,130 Z" fill="#6b5436" {o(9)}/>')
    sar += (f'<path d="M380,136 L1010,-144 L1640,136 L1580,106 L1010,-100 L440,106 Z"'
            f' fill="url(#sneg)" opacity=".7" {o(4)}/>')
    s += SL(Z_DAL, sar)
    s += SL(Z_DAL, dym(300, 320, t, 4, .2, 260, .3, "#c8d0da", .9))
    dvx, dvy, dvw, dvh = 700, 300, 640, 640
    s += SL(Z_SRED, f'<rect x="{dvx-40}" y="{dvy-40}" width="{dvw+80}"'
                    f' height="{dvh+40}" rx="12" fill="{DOSKA2}" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="#1b140d"/>')
    s += SL(Z_SRED, teplo(dvx + dvw * .5, dvy + dvh * .62, 520, 460, .55))
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="{ORA}" opacity=".16"/>')
    utv = []
    # ухват
    ux_ = dvx + 110
    utv.append(f'<rect x="{ux_-14:.0f}" y="{dvy+180}" width="28" height="430" rx="10"'
               f' fill="url(#derev)" {o(6)}/>'
               f'<path d="M{ux_-60:.0f},{dvy+200} q60,-90 120,0" fill="none"'
               f' stroke="{ZHELEZ}" stroke-width="22"/>' + _glaza(ux_, dvy + 300, 15, t, .1))
    # коромысло
    kx_ = dvx + 250
    utv.append(f'<path d="M{kx_-120:.0f},{dvy+260} q120,-90 240,0" fill="none"'
               f' stroke="url(#derev)" stroke-width="34" stroke-linecap="round"/>'
               + _glaza(kx_, dvy + 236, 14, t, .4))
    # кадушка
    kdx = dvx + 430
    utv.append(f'<path d="M{kdx-110:.0f},{dvy+620} l14,-260 q96,-34 192,0 l14,260 Z"'
               f' fill="url(#derev)" {o(7)}/>'
               f'<path d="M{kdx-104:.0f},{dvy+440} q104,26 208,0" fill="none"'
               f' stroke="{ZHELEZ}" stroke-width="13"/>'
               + _glaza(kdx, dvy + 420, 18, t, .7))
    # топор прячется за кадушку
    pryat = A.ease(A.seg(t, 1.4, 1.0))
    tpx = dvx + 560 - pryat * 120
    utv.append(f'<g opacity="{1-pryat*.55:.2f}">'
               f'<rect x="{tpx-12:.0f}" y="{dvy+330}" width="26" height="280" rx="9"'
               f' fill="url(#derev)" {o(5)}/>'
               f'<path d="M{tpx-16:.0f},{dvy+310} q86,-30 108,22 l-24,78'
               f' q-44,-26 -84,-20 Z" fill="url(#zhel)" {o(6)}/>'
               + _glaza(tpx + 30, dvy + 300, 13, t, .2) + '</g>')
    # корыто
    krx = dvx + 160
    utv.append(f'<path d="M{krx-150:.0f},{dvy+600} q150,80 300,0 q-20,80 -150,88'
               f' q-130,-8 -150,-88 Z" fill="url(#derev)" {o(7)}/>'
               + _glaza(krx, dvy + 620, 16, t, .9))
    for u in utv:
        s += SL(Z_SRED, u)
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="none" {o(10)}/>')
    mot = 5.0 * A.w(t, 1.5, .1)
    hx, hy = dvx + dvw * .5, 1010
    s += SL(Z_SRED, f'<g transform="rotate({mot:.1f} {hx:.0f} {hy-300:.0f})">'
                    + figura(hx, hy, 660, t, "#4a3a2c", "#ffd98a", False, .2, False,
                             1.0, True, 0.0, True) + '</g>')
    for sgn in (-1, 1):
        ruk, (ax, ay) = rukav(hx + sgn * 120, hy - 460, 280,
                              (0 if sgn > 0 else 180) + sgn * (6 + 5 * A.w(t, 1.3, .2)),
                              t, "#4a3a2c", "#ffd98a", .2 + (0 if sgn > 0 else .4), 3.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="34" ry="26"'
                        f' fill="#4a3a2c" {o(5)}/>')
    s += SL(Z_SRED, para_izo_rta(hx + 60, hy - 540, t, .1, 1.2, .5))
    fnx, fny = dvx - 120, 420
    s += SL(Z_SRED, f'<rect x="{fnx-16:.0f}" y="120" width="32" height="760"'
                    f' fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M{fnx-70:.0f},{fny:.0f} h140 l-16,-36 h-108 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-58:.0f},{fny:.0f} h116 l-12,130 h-92 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 116, t, .62, .3, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 80, 340, 300, .44 + .12 * abs(A.w(t, 1.6))))
    sos_x = 1700
    s += SL(Z_SRED, figura(sos_x, 1040, 470, t, "#3c4656", "#cfe4f5", False, .7,
                           True, 1.0, True, 1.4, False, True))
    ches = -70 + 16 * A.w(t, 1.1, .3)
    ruk3, (cx3, cy3) = rukav(sos_x - 60, 700, 150, ches, t, "#3c4656", "#cfe4f5", .3, 6.0)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, f'<ellipse cx="{cx3:.0f}" cy="{cy3:.0f}" rx="26" ry="20"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_PERED, pleten(-60, 1080, 420, 200, 6))
    s += SL(Z_PERED, _korzina(1860, 1080, 240, 190, t, 569, False))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 571, .44, .9))
    s += vinetka(.46)
    return s


# ── 51 ─────────────────────────────────────────────────────────────────────
def dostatok_uhodit_verenicey(t):
    """Ворота амбара: сосед уносит отданное решето, а следом на тонких ножках
    уходят мешок муки, окорок, кадка с капустой и крынка масла.

    Каждый припас опознаётся силуэтом: у мешка завязанное горло, обсыпка
    мукой и мерка, у окорока торчит кость и подвязка, у кадки клёпки, обручи
    и кочан поверх, у крынки узкое горло под тряпицей и брусок масла. Прежде
    в ряд шли четыре безымянных пятна (осмотр 14.11)."""
    rnd = random.Random(5101)
    s = sumerki_fon(t, True)
    s += ulica_dal(1240, 700, 700, t, False, 577)
    s += SL(Z_DAL, gryaz_polosa(790, 190, "#473c30"))
    amb = doski(120, 60, 1180, 820, 92, True, "dosk")
    amb += (f'<path d="M80,70 L710,-180 L1340,70 Z" fill="#6b5436" {o(9)}/>')
    amb += (f'<rect x="640" y="-120" width="140" height="120" rx="8"'
            f' fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_DAL, amb)
    vx, vy, vw, vh = 330, 240, 760, 620
    s += SL(Z_SRED, f'<rect x="{vx-40}" y="{vy-40}" width="{vw+80}" height="{vh+40}"'
                    f' rx="12" fill="{DOSKA2}" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}"'
                    f' fill="#140e09"/>')
    pust = A.ease(A.seg(t, .6, 2.4))
    for i in range(5):                  # опустевшие полки амбара
        s += SL(Z_SRED, f'<rect x="{vx+40}" y="{vy+90+i*106:.0f}" width="{vw-80}"'
                        f' height="18" rx="6" fill="#3a2a1c" {o(4)}/>')
        if i % 2 == 0:
            s += SL(Z_SRED, f'<g opacity="{1-pust:.2f}">'
                            + krynka(vx + 150 + i * 90, vy + 86 + i * 106, .8) + '</g>')
    s += SL(Z_SRED, teplo(vx + vw * .5, vy + vh * .7, 380, 320, .24))
    for sgn, px in ((-1, vx), (1, vx + vw)):
        s += SL(Z_SRED, f'<g transform="rotate({sgn*18:.0f} {px:.0f} {vy:.0f})">'
                        f'<rect x="{px-(170 if sgn<0 else 0):.0f}" y="{vy}" width="170"'
                        f' height="{vh}" fill="url(#dosk)" {o(8)}/>'
                        f'<path d="M{px-(160 if sgn<0 else -10):.0f},{vy+60}'
                        f' l150,{vh-160:.0f}" stroke="#5a3a22" stroke-width="14"/></g>')
    # ЧЕТЫРЕ ПРИПАСА, каждый со своими приметами
    for i in range(4):
        hod = A.ease(A.seg(t, .2 + i * .26, 2.8))
        gx = vx + 110 + i * 250 + hod * 470
        gy = 1010 - i * 24
        sh = 8 * A.w(t, .8, i * .3)
        g = f'<g transform="translate({sh:.1f},{-abs(sh)*.6:.1f})">'
        if i == 0:                      # МЕШОК МУКИ: горло перевязано, мука сыплется
            g += ten(gx, gy - 46, 120, 20, .4)
            g += (f'<path d="M{gx-120:.0f},{gy-60:.0f} q-26,-250 118,-282'
                  f' q144,32 118,282 q-118,54 -236,0 Z" fill="#d8c8a4" {o(8)}/>')
            for j in range(4):          # складки холста
                g += (f'<path d="M{gx-80+j*52:.0f},{gy-96:.0f} q10,-110 2,-178"'
                      f' fill="none" stroke="#b9a87e" stroke-width="7" opacity=".7"/>')
            g += (f'<path d="M{gx-54:.0f},{gy-348:.0f} q54,-34 108,0 l-14,54'
                  f' q-40,16 -80,0 Z" fill="#c2b08a" {o(5)}/>')
            g += (f'<path d="M{gx-58:.0f},{gy-344:.0f} q58,-26 116,0" fill="none"'
                  f' stroke="{TKAN}" stroke-width="18"/>')
            g += (f'<path d="M{gx-40:.0f},{gy-396:.0f} q40,-40 80,0 q-40,16 -80,0 Z"'
                  f' fill="#e8dcc6" {o(4)}/>')
            mah = 16 * A.w(t, .9, .2)   # уголок мешка машет
            g += (f'<path d="M{gx+108:.0f},{gy-250:.0f} q{60+mah:.0f},-44 94,8'
                  f' q-62,34 -94,22 Z" fill="#d8c8a4" {o(5)}/>')
            for j in range(7):          # мука сыплется из-под завязки
                q = ((t * .6) + j * .14) % 1.0
                g += (f'<circle cx="{gx-60+j*18+10*A.w(t,2.0,j*.2):.0f}"'
                      f' cy="{gy-330+q*120:.0f}" r="{5-2*q:.1f}" fill="#f2ead6"'
                      f' opacity="{(1-q)*.8:.2f}"/>')
            g += (f'<ellipse cx="{gx-20:.0f}" cy="{gy-186:.0f}" rx="64" ry="34"'
                  f' fill="#f2ead6" opacity=".22"/>')
            g += _glaza(gx, gy - 230, 17, t, .1, "#2b2118")
            g += _nozhki(gx, gy - 56, 150, t, i * .3, "#4a3a28", 62)
        elif i == 1:                    # ОКОРОК: кость наружу, подвязка, шкурка
            g += ten(gx, gy - 56, 110, 18, .4)
            g += (f'<path d="M{gx-126:.0f},{gy-120:.0f} q-40,-170 120,-194'
                  f' q160,-10 118,200 q-118,66 -238,-6 Z" fill="#b06a4a" {o(8)}/>')
            g += (f'<path d="M{gx-126:.0f},{gy-176:.0f} q120,52 238,-16 l-6,56'
                  f' q-116,62 -226,8 Z" fill="#e8dcc6" opacity=".9" {o(4)}/>')
            for j in range(4):          # сетка шпагата
                g += (f'<path d="M{gx-110+j*66:.0f},{gy-300:.0f} q14,110 2,196"'
                      f' fill="none" stroke="#6b4a2a" stroke-width="6" opacity=".7"/>')
            g += (f'<path d="M{gx-116:.0f},{gy-246:.0f} q118,44 234,-10" fill="none"'
                  f' stroke="#6b4a2a" stroke-width="7" opacity=".7"/>')
            kost = 6 * A.w(t, 1.4, .3)
            g += (f'<path d="M{gx+70:.0f},{gy-300:.0f} l{58+kost:.0f},-80"'
                  f' stroke="#efe8d8" stroke-width="26" stroke-linecap="round"/>')
            g += (f'<circle cx="{gx+134+kost:.0f}" cy="{gy-384:.0f}" r="24"'
                  f' fill="#f6f1e2" {o(5)}/>')
            g += (f'<circle cx="{gx+112+kost:.0f}" cy="{gy-364:.0f}" r="18"'
                  f' fill="#f6f1e2" {o(4)}/>')
            g += (f'<path d="M{gx+120+kost:.0f},{gy-398:.0f} q34,-30 10,-62"'
                  f' fill="none" stroke="#8a7a5a" stroke-width="9"/>')
            g += _glaza(gx - 10, gy - 230, 15, t, .5, "#f0e4cc")
            g += _nozhki(gx, gy - 110, 140, t, i * .3, "#4a3a28", 62)
        elif i == 2:                    # КАДКА: клёпки, два обруча, кочан поверх
            g += ten(gx, gy - 52, 112, 18, .4)
            g += (f'<path d="M{gx-112:.0f},{gy-60:.0f} l18,-250 q94,-40 188,0'
                  f' l18,250 Z" fill="url(#derev)" {o(8)}/>')
            for j in range(5):          # клёпки
                g += (f'<path d="M{gx-80+j*40:.0f},{gy-300:.0f} l{-4+j*2:.0f},244"'
                      f' fill="none" stroke="#6b4a26" stroke-width="5" opacity=".8"/>')
            for j in range(2):
                g += (f'<path d="M{gx-106+j*8:.0f},{gy-110-j*130:.0f}'
                      f' q{106-j*8:.0f},30 {212-j*16:.0f},0" fill="none"'
                      f' stroke="{ZHELEZ}" stroke-width="16"/>')
            g += (f'<ellipse cx="{gx:.0f}" cy="{gy-306:.0f}" rx="100" ry="28"'
                  f' fill="#8a6a44" {o(5)}/>')
            g += (f'<ellipse cx="{gx:.0f}" cy="{gy-316:.0f}" rx="86" ry="22"'
                  f' fill="#b9c98a" {o(4)}/>')
            for j in range(3):          # кочан капусты поверх кадки
                g += (f'<ellipse cx="{gx-34+j*34:.0f}" cy="{gy-356+((j%2)*14):.0f}"'
                      f' rx="{52-j*4:.0f}" ry="{44-j*4:.0f}" fill="#cfe0a0" {o(5)}/>')
                g += (f'<path d="M{gx-60+j*34:.0f},{gy-366+((j%2)*14):.0f}'
                      f' q26,{-26:.0f} 52,0" fill="none" stroke="#8aa45a"'
                      f' stroke-width="6" opacity=".9"/>')
            g += _glaza(gx, gy - 200, 16, t, .8)
            g += _nozhki(gx, gy - 56, 150, t, i * .3, "#4a3a28", 62)
        else:                           # КРЫНКА МАСЛА: узкое горло, тряпица, брусок
            g += ten(gx, gy - 46, 92, 16, .4)
            g += (f'<path d="M{gx-92:.0f},{gy-60:.0f} q-30,-150 10,-196'
                  f' q18,-40 14,-86 l{136:.0f},0 q-4,46 14,86 q40,46 10,196 Z"'
                  f' fill="url(#krem)" {o(8)}/>')
            g += (f'<path d="M{gx-78:.0f},{gy-180:.0f} q78,28 156,0" fill="none"'
                  f' stroke="#cfbf9c" stroke-width="8" opacity=".8"/>')
            g += (f'<path d="M{gx-72:.0f},{gy-342:.0f} q72,-40 144,0 l-10,40'
                  f' q-62,28 -124,0 Z" fill="{TKAN2}" {o(5)}/>')
            g += (f'<path d="M{gx-74:.0f},{gy-338:.0f} q74,-24 148,0" fill="none"'
                  f' stroke="{TKAN}" stroke-width="12"/>')
            g += (f'<ellipse cx="{gx:.0f}" cy="{gy-352:.0f}" rx="56" ry="18"'
                  f' fill="#f4ecd0" {o(4)}/>')
            mas = 6 * A.w(t, 1.6, .4)   # брусок масла на донце рядом
            g += (f'<path d="M{gx+96:.0f},{gy-96+mas*.4:.0f} h92 l-10,56 h-76 Z"'
                  f' fill="#f2d98a" {o(5)}/>')
            g += (f'<path d="M{gx+96:.0f},{gy-96+mas*.4:.0f} h92 l-14,-18 h-66 Z"'
                  f' fill="#fbeec0" {o(4)}/>')
            g += _glaza(gx, gy - 250, 14, t, .3, "#2b2118")
            g += _nozhki(gx, gy - 56, 130, t, i * .3, "#4a3a28", 62)
        g += '</g>'
        s += SL(Z_SRED, g)
    sos = A.ease(A.seg(t, .2, 2.4))
    sx = 1180 + sos * 480
    s += SL(Z_SRED, figura(sx, 1020, 520, t, "#3c4656", "#cfe4f5", False, .5,
                           True, 1.0, True, 1.2, True, True))
    ruk, (rx2, ry2) = rukav(sx - 110, 700, 180, 176, t, "#3c4656", "#cfe4f5", .3, 4.0)
    s += SL(Z_SRED, ruk)
    sit = (f'<ellipse cx="{rx2-60:.0f}" cy="{ry2+20:.0f}" rx="120" ry="104"'
           f' fill="url(#solom)" {o(8)}/>')
    sit += (f'<ellipse cx="{rx2-60:.0f}" cy="{ry2+20:.0f}" rx="94" ry="80"'
            f' fill="#c9a877" {o(5)}/>')
    for i in range(7):
        sit += (f'<line x1="{rx2-150+i*26:.0f}" y1="{ry2-56:.0f}"'
                f' x2="{rx2-150+i*26:.0f}" y2="{ry2+96:.0f}" stroke="#8a6534"'
                f' stroke-width="5" opacity=".75"/>')
    s += SL(Z_SRED, sit)
    s += SL(Z_SRED, para_izo_rta(sx + 46, 640, t, .2, 1.1, .5))
    fnx, fny = 1340, 360
    s += SL(Z_SRED, f'<rect x="{fnx-16:.0f}" y="100" width="32" height="700"'
                    f' fill="url(#derev)" {o(7)}/>'
                    f'<path d="M{fnx-64:.0f},{fny:.0f} h128 l-14,-34 h-100 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-54:.0f},{fny:.0f} h108 l-12,124 h-84 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 112, t, .58, .2, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 70, 330, 290, .42 + .12 * abs(A.w(t, 1.5))))
    gor_p = ((t * .35) % 1.0)           # горошина катится по земле
    s += SL(Z_SRED, f'<circle cx="{vx+vw*.5+gor_p*900:.0f}"'
                    f' cy="{1062-abs(math.sin(gor_p*14))*22:.0f}" r="17"'
                    f' fill="{ZEL2}" {o(4)}/>')
    s += SL(Z_PERED, pleten(1300, 1080, 620, 210, 7))
    s += SL(Z_PERED, goloe_derevo(140, 1080, 560, t, 587, 7, "#2a2b33"))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 593, .44, .9))
    s += vinetka(.46)
    return s


# ── 52 ─────────────────────────────────────────────────────────────────────
def chuzhoy_gorshok_s_neudachami(t):
    """Чужой расписной горшок на пол-кадра: крышка приподнимается, и из него
    выбираются три взъерошенных бесёнка-неудачи."""
    rnd = random.Random(5209)
    s = f'<rect width="{W}" height="{H}" fill="#2b2118"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 760, 104))
    s += utvar_izby(1340, 260, 520, t, 599)
    s += SL(Z_SRED, polovicy(900))
    s += SL(Z_SRED, pech(-140, 160, 480, 700, t, True, True, False))
    s += SL(Z_SRED, teplo(120, 620, 520, 420, .34 + .1 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, iskra_let(t, 120, 560, 7, 601, 280, .4))
    s += SL(Z_SRED, stol(520, 760, 960, 44))
    s += SL(Z_SRED, f'<path d="M500,758 h1000 l-40,54 h-920 Z" fill="{RUSH}"'
                    f' opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, svecha(1420, 620, t, .2, 1.6, 140))
    s += SL(Z_SRED, teplo(1430, 590, 520, 460, .42 + .12 * abs(A.w(t, 1.3))))
    gx, gy = 880, 756
    gor = ten(gx, gy + 10, 210, 26, .5)
    gor += (f'<path d="M{gx-190:.0f},{gy-110:.0f} q-60,-210 50,-330'
            f' q140,-56 280,0 q110,120 50,330 Z" fill="url(#glina)" {o(9)}/>')
    gor += (f'<path d="M{gx-190:.0f},{gy-110:.0f} q190,56 380,0 l-8,110'
            f' q-182,46 -364,0 Z" fill="#b06a3c" {o(7)}/>')
    for i in range(3):                  # роспись: пояски и ягоды
        yy = gy - 200 - i * 86
        gor += (f'<path d="M{gx-184+i*6:.0f},{yy:.0f} q{184-i*6:.0f},40'
                f' {368-i*12:.0f},0" fill="none" stroke="{KREM}" stroke-width="12"'
                f' opacity=".9"/>')
        for j in range(6):
            gor += (f'<circle cx="{gx-150+j*60:.0f}" cy="{yy-30:.0f}" r="13"'
                    f' fill="{[KRAS, ZEL2, ZOL][j%3]}" {o(3)}/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-452:.0f}" rx="200" ry="50"'
            f' fill="#8e5a2c" {o(8)}/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-452:.0f}" rx="172" ry="38"'
            f' fill="#1d0f06"/>')
    s += SL(Z_SRED, gor)
    pod = A.out(A.seg(t, .3, .8))
    kry_y = gy - 470 - pod * 150
    kach = 9 * A.w(t, 1.6, .2) * pod
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {gx:.0f} {kry_y:.0f})">'
                    f'<ellipse cx="{gx:.0f}" cy="{kry_y:.0f}" rx="206" ry="50"'
                    f' fill="url(#glina)" {o(8)}/>'
                    f'<ellipse cx="{gx:.0f}" cy="{kry_y-28:.0f}" rx="140" ry="34"'
                    f' fill="#b06a3c" {o(5)}/>'
                    f'<ellipse cx="{gx:.0f}" cy="{kry_y-58:.0f}" rx="40" ry="24"'
                    f' fill="#8e5a2c" {o(6)}/></g>')
    for i in range(3):                  # бесенята вылезают
        lez = A.out(A.seg(t, .8 + i * .34, 1.1))
        bx = gx - 130 + i * 130
        by = gy - 420 - lez * (60 + i * 16)
        bh = 120
        b = f'<g transform="translate({10*A.w(t,.9,i*.3):.1f},0)">'
        b += (f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{bh*.44:.0f}"'
              f' ry="{bh*.50:.0f}" fill="#2f2436" {o(6)}/>')
        for j in range(9):              # взъерошенная шерсть
            a = -3.0 + j * .38
            b += (f'<path d="M{bx+math.cos(a)*bh*.40:.0f},'
                  f'{by+math.sin(a)*bh*.44:.0f} l{math.cos(a)*22:.0f},'
                  f'{math.sin(a)*22:.0f}" stroke="#2f2436" stroke-width="12"'
                  f' stroke-linecap="round"/>')
        for sgn in (-1, 1):             # рожки
            b += (f'<path d="M{bx+sgn*30:.0f},{by-bh*.44:.0f} l{sgn*14:.0f},-38'
                  f' l{-sgn*26:.0f},12 Z" fill="#6b4a2a" {o(4)}/>')
        b += _glaza(bx, by - 10, 14, t, i * .3, "#f6e39a")
        b += (f'<path d="M{bx-20:.0f},{by+34:.0f} q20,22 40,0" fill="none"'
              f' stroke="#f6e39a" stroke-width="7" stroke-linecap="round"/>')
        b += (f'<path d="M{bx+bh*.42:.0f},{by+20:.0f} q50,20 30,70" fill="none"'
              f' stroke="#2f2436" stroke-width="12" stroke-linecap="round"/>')
        b += '</g>'
        s += SL(Z_SRED, b)
    let = A.ease(A.seg(t, 1.6, 1.0))
    chx = 1300 + let * 240
    chy = 700 + let * 320 - math.sin(let * 3.14) * 200
    s += SL(Z_SRED, f'<g transform="rotate({let*300:.0f} {chx:.0f} {chy:.0f})">'
                    f'<path d="M{chx-60:.0f},{chy-50:.0f} q60,90 120,0'
                    f' q-60,26 -120,0 Z" fill="url(#krem)" {o(6)}/>'
                    f'<ellipse cx="{chx:.0f}" cy="{chy-54:.0f}" rx="62" ry="18"'
                    f' fill="#d8cbb0" {o(4)}/>'
                    f'<path d="M{chx+58:.0f},{chy-44:.0f} q40,20 0,46" fill="none"'
                    f' stroke="url(#krem)" stroke-width="11"/></g>')
    for i in range(6):                  # брызги из чашки
        p = ((t * .9) + i * .16) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{chx-60+p*120:.0f}" cy="{chy+p*p*160:.0f}"'
                        f' rx="{10*(1-p)+3:.1f}" ry="{16*(1-p)+4:.1f}"'
                        f' fill="#c9b78a" opacity="{1-p:.2f}"/>')
    rv = A.ease(A.seg(t, 2.2, .7))
    s += SL(Z_SRED, f'<path d="M300,420 q120,{60+40*rv:.0f} {200-80*rv:.0f},'
                    f'{120+60*rv:.0f}" fill="none" stroke="{KREM}" stroke-width="7"/>'
                    f'<path d="M{560+60*rv:.0f},{600+40*rv:.0f} q60,40 120,20"'
                    f' fill="none" stroke="{KREM}" stroke-width="7"/>')
    nes = A.ease(A.seg(t, 2.6, 1.2))
    hx = 420 + nes * -260
    s += SL(Z_SRED, figura(hx, 1070, 560, t, "#5b2f3a", "#ffd98a", True, .4, True))
    s += SL(Z_SRED, kot(1700, 1060, t, .9, "#3b3430", True))
    s += ramka_pp("pravo", "#160f0a", .46)
    s += SL(Z_PERED, krynka(220, 1070, 1.4))
    s += vinetka(.46)
    return s


# ── 53 ─────────────────────────────────────────────────────────────────────
def stena_s_instrumentom(t):
    """Стена сарая во весь кадр: на гвоздях пила, топор, коса, грабли и хомут,
    под каждым обведён углём контур — пилу снимают, контур пустеет."""
    rnd = random.Random(5303)
    s = f'<rect width="{W}" height="{H}" fill="#5c452c"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 96, True, "dosk"))
    for i in range(21):                 # гвозди и сучки по доскам
        s += SL(Z_DAL, f'<ellipse cx="{40+i*92:.0f}" cy="{120+(i%5)*190:.0f}"'
                       f' rx="11" ry="8" fill="#6b4a2a" opacity=".7"/>')
    s += SL(Z_DAL, f'<rect x="0" y="940" width="{W}" height="140" fill="#4a3a26" {o(6)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="928" width="{W}" height="24" fill="#6b5436" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="0" y="40" width="{W}" height="40" fill="#4a3a26" {o(5)}/>')
    snyat = A.ease(A.seg(t, 2.6, 1.6))
    # контуры углём: что где висит
    kont = ""
    konturi = ((300, 420, 330, 150), (720, 360, 150, 330), (1130, 330, 420, 420),
               (1600, 380, 230, 420), (430, 820, 300, 180))
    for (cx_, cy_, cw, ch) in konturi:
        kont += (f'<rect x="{cx_-cw/2:.0f}" y="{cy_-ch/2:.0f}" width="{cw}"'
                 f' height="{ch}" rx="24" fill="none" stroke="#2f2418"'
                 f' stroke-width="9" stroke-dasharray="22 16" opacity=".75"/>')
    s += SL(Z_SRED, kont)
    # пила — её снимают
    px_, py_ = 300, 420
    pila = f'<g opacity="{1-snyat:.2f}" transform="translate({snyat*-260:.0f},{snyat*-80:.0f})">'
    pila += (f'<path d="M{px_-160:.0f},{py_-40:.0f} h300 l-20,70 h-280 Z"'
             f' fill="url(#zhel)" {o(7)}/>')
    for i in range(14):
        pila += (f'<path d="M{px_-156+i*22:.0f},{py_+30:.0f} l11,26 l11,-26 Z"'
                 f' fill="url(#zhel)" {o(3)}/>')
    pila += (f'<path d="M{px_+142:.0f},{py_-50:.0f} q60,-10 60,40 q0,46 -56,40'
             f' l-10,-80 Z" fill="url(#derev)" {o(6)}/>')
    pila += (f'<path d="M{px_-150:.0f},{py_-30:.0f} h280" stroke="#eef4f8"'
             f' stroke-width="8" opacity="{.3+.3*abs(A.w(t,2.2)):.2f}"/>')
    pila += '</g>'
    s += SL(Z_SRED, pila)
    s += SL(Z_SRED, f'<circle cx="{px_-150:.0f}" cy="{py_-62:.0f}" r="13"'
                    f' fill="{ZHELEZ}" {o(4)}/>')
    # топор
    tx_, ty_ = 720, 360
    s += SL(Z_SRED, f'<rect x="{tx_-18:.0f}" y="{ty_-120:.0f}" width="36" height="300"'
                    f' rx="12" fill="url(#derev)" {o(7)}/>'
                    f'<path d="M{tx_-24:.0f},{ty_-150:.0f} q120,-44 150,30 l-32,104'
                    f' q-58,-32 -116,-24 Z" fill="url(#zhel)" {o(8)}/>'
                    f'<path d="M{tx_+96:.0f},{ty_-120:.0f} q30,56 10,116" fill="none"'
                    f' stroke="#eef4f8" stroke-width="12" opacity=".55"/>')
    # коса
    kx_, ky_ = 1130, 330
    s += SL(Z_SRED, f'<path d="M{kx_-160:.0f},{ky_-180:.0f} q40,240 160,380"'
                    f' fill="none" stroke="url(#derev)" stroke-width="34"'
                    f' stroke-linecap="round"/>'
                    f'<path d="M{kx_-150:.0f},{ky_-170:.0f} q230,30 310,250'
                    f' q-170,-150 -320,-190 Z" fill="url(#zhel)" {o(8)}/>'
                    f'<path d="M{kx_-140:.0f},{ky_-150:.0f} q210,40 280,230"'
                    f' fill="none" stroke="#eef4f8" stroke-width="9"'
                    f' opacity="{.35+.3*abs(A.w(t,2.6,.2)):.2f}"/>'
                    f'<rect x="{kx_-40:.0f}" y="{ky_+110:.0f}" width="60"'
                    f' height="30" rx="10" fill="{ZHELEZ}" {o(4)}/>')
    # грабли
    gx_, gy_ = 1600, 380
    grab = (f'<rect x="{gx_-16:.0f}" y="{gy_-170:.0f}" width="32" height="400"'
            f' rx="11" fill="url(#derev)" {o(7)}/>')
    grab += (f'<rect x="{gx_-130:.0f}" y="{gy_-220:.0f}" width="260" height="34"'
             f' rx="12" fill="url(#derev)" {o(6)}/>')
    for i in range(7):
        grab += (f'<rect x="{gx_-120+i*38:.0f}" y="{gy_-186:.0f}" width="16"'
                 f' height="74" rx="7" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, grab)
    # хомут
    hx_, hy_ = 430, 820
    hom = (f'<path d="M{hx_-140:.0f},{hy_:.0f} q-30,-150 140,-160 q170,10 140,160'
           f' q-30,110 -140,110 q-110,0 -140,-110 Z" fill="#6b4a2a" {o(9)}/>')
    hom += (f'<path d="M{hx_-80:.0f},{hy_-10:.0f} q-16,-100 80,-104 q96,4 80,104'
            f' q-16,70 -80,70 q-64,0 -80,-70 Z" fill="#2f2418" {o(6)}/>')
    for i in range(6):
        hom += (f'<circle cx="{hx_-120+i*48:.0f}" cy="{hy_-120+((i%2)*16):.0f}"'
                f' r="10" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, hom)
    ox, oy, ow, oh = 1180, 740, 420, 300
    vesna = A.ease(A.seg(t, 4.4, 2.0))
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}"'
          f' fill="{"#b9d0e2" if vesna < .5 else "#9ec8a0"}"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.62:.0f}" width="{ow}" height="{oh*.38:.0f}"'
           f' fill="{"#e8f1fa" if vesna < .5 else "#6f8c4a"}"/>')
    for i in range(4):
        za += (f'<path d="M{ox+50+i*100:.0f},{oy+oh*.64:.0f} l-30,0 l30,-80 l30,80 Z"'
               f' fill="{"#8aa0b4" if vesna < .5 else "#4a6a34"}"/>')
        if vesna > .5:
            za += (f'<circle cx="{ox+50+i*100:.0f}" cy="{oy+oh*.42:.0f}" r="34"'
                   f' fill="#7a9a46" opacity=".9"/>')
    s += SL(Z_SRED, f'<clipPath id="ok53"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok53)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .1, False, True))
    fnx, fny = 240, 180
    s += SL(Z_SRED, f'<path d="M{fnx-20:.0f},{fny-100:.0f} q20,-40 40,0" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="9"/>'
                    f'<path d="M{fnx-78:.0f},{fny:.0f} h156 l-18,-38 h-120 Z"'
                    f' fill="{ZHELEZ}" {o(7)}/>'
                    f'<path d="M{fnx-66:.0f},{fny:.0f} h132 l-14,170 h-104 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(7)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 196, t, .72, .2, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 150, 440, 400, .44 + .12 * abs(A.w(t, 1.5))))
    ruk, (rx2, ry2) = rukav(-80, 470, 170 + snyat * 90, -16 - snyat * 14, t,
                            "#4a3a2c", "#ffd98a", .2, 3.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{rx2:.0f}" cy="{ry2:.0f}" rx="40" ry="28"'
                    f' fill="#4a3a2c" {o(5)}/>')
    ches = A.ease(A.seg(t, 4.0, 1.4))
    sx_ = 1820
    s += SL(Z_SRED, figura(sx_, 1060, 470, t, "#3c4656", "#ffd98a", False, .6,
                           True, 1.0, False, 1.2, True))
    ruk3, (cx3, cy3) = rukav(sx_ - 60, 760, 140, -64 - 20 * ches, t, "#3c4656",
                             "#ffd98a", .3, 6.0)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, f'<ellipse cx="{cx3:.0f}" cy="{cy3:.0f}" rx="26" ry="20"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, _korzina(960, 1070, 260, 190, t, 5309, False))
    s += ramka_pp("levo", "#1a120a", .4)
    s += vinetka(.44)
    return s


# ── 54 ─────────────────────────────────────────────────────────────────────
def babushka_zaslonyaet_dver(t):
    """Сени, за окошком ночь: внук с полным помойным ведром идёт к двери, а
    бабушка встаёт к двери и забирает ведро из рук."""
    rnd = random.Random(5407)
    s = f'<rect width="{W}" height="{H}" fill="#352a1e"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 108))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#1d1710" opacity=".35"/>')
    s += mebel_hlam(60, 980, 520, t, 5413)
    s += SL(Z_SRED, polovicy(920))
    dvx, dvy, dvw, dvh = 820, 160, 440, 760
    s += SL(Z_SRED, f'<rect x="{dvx-46}" y="{dvy-46}" width="{dvw+92}"'
                    f' height="{dvh+46}" rx="12" fill="{DOSKA2}" {o(10)}/>')
    s += SL(Z_SRED, dver(dvx, dvy, dvw, dvh, .0, "url(#derev)", True, True))
    s += SL(Z_SRED, podkova(dvx + dvw * .5, dvy - 86, 1.0, t))
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{dvx-46}" y="{dvy+i*200:.0f}" width="{dvw+92}"'
                        f' height="18" rx="6" fill="#5a3a22" opacity=".8"/>')
    ox, oy, ow, oh = 1460, 260, 380, 300
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#141d33"/>')
    for i in range(22):
        za += (f'<circle cx="{ox+rnd.uniform(10,ow-10):.0f}"'
               f' cy="{oy+rnd.uniform(10,oh*.7):.0f}"'
               f' r="{rnd.uniform(1.4,3.0):.1f}" fill="#fdf6e0"'
               f' opacity="{.3+.6*abs(A.w(t,2.4+rnd.uniform(0,2),i*.11)):.2f}"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.72:.0f}" width="{ow}" height="{oh*.28:.0f}"'
           f' fill="#232c3e"/>')
    za += izba_snaruzhi(ox + 40, oy + oh - 6, 220, t, True, True, 5417)
    s += SL(Z_SRED, f'<clipPath id="ok54"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok54)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .3, False, True))
    s += SL(Z_SRED, tusklaya_lampochka(640, 120, t, 1.1, True))
    s += SL(Z_SRED, svecha(1700, 820, t, .3, 1.4, 130))
    s += SL(Z_SRED, teplo(1700, 790, 420, 380, .34 + .1 * abs(A.w(t, 1.4))))
    pered = A.ease(A.seg(t, 1.4, 1.3))
    vx = 1420 - pered * 180
    s += SL(Z_SRED, figura(vx, 1020, 500, t, "#3a4656", "#ffd98a", False, .5,
                           True, 1.0, False, 1.2))
    ruk, (hx, hy) = rukav(vx - 90, 700, 150, 150, t, "#3a4656", "#ffd98a", .3, 4.0)
    s += SL(Z_SRED, ruk)
    vedx = hx + 110 - pered * 80
    vedy = hy + 80 + pered * 26
    s += SL(Z_SRED, _vedro(vedx, vedy, 1.5, t, True, "url(#chug)"))
    for i in range(5):                  # вонючий парок над ведром
        k = ((t * .5) + i * .2) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{vedx-20+30*A.w(t,2.2,i*.2):.0f}"'
                        f' cy="{vedy-150-k*90:.0f}" rx="{16+30*k:.0f}"'
                        f' ry="{10+20*k:.0f}" fill="#9aa37a"'
                        f' opacity="{.34*(1-k):.2f}"/>')
    bx = 900
    s += SL(Z_SRED, figura(bx, 1050, 640, t, "#5b2f3a", "#ffd98a", True, .2))
    lad = A.ease(A.seg(t, .4, .9))
    ruk2, (lx2, ly2) = rukav(bx + 130, 700, 170, -70 - 34 * lad, t, "#5b2f3a",
                             "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{lx2:.0f}" cy="{ly2:.0f}" rx="40" ry="52"'
                    f' fill="#e3c6a8" {o(6)}/>')
    ruk3, (bx3, by3) = rukav(bx + 110, 780, 180, 10 + 16 * pered, t, "#5b2f3a",
                             "#ffd98a", .5, 4.0)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, f'<ellipse cx="{bx3:.0f}" cy="{by3:.0f}" rx="30" ry="22"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, kot(500, 1060, t, .9, "#3b3430"))
    s += SL(Z_SRED, _korzina(280, 1040, 240, 180, t, 5419, False))
    s += ramka_pp("pravo", "#160f0a", .46)
    s += SL(Z_PERED, krynka(120, 1070, 1.4))
    s += vinetka(.48)
    return s


# ── 55 ─────────────────────────────────────────────────────────────────────
def stremyanka_kniga_i_forma_dlya_piro(t):
    """Прихожая квартиры: в открытой двери очередь из трёх соседей, а хозяйка
    выносит и тут же уносит обратно стремянку, толстую книгу и форму."""
    rnd = random.Random(5501)
    s = f'<rect width="{W}" height="{H}" fill="#4a4650"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#6b6472"/>')
    for i in range(14):
        s += SL(Z_DAL, f'<rect x="{i*145}" y="0" width="64" height="1080"'
                       f' fill="#766e7e" opacity=".5"/>')
    s += SL(Z_DAL, f'<rect x="0" y="900" width="{W}" height="180" fill="#54505c" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="886" width="{W}" height="26" fill="#8a8292" {o(4)}/>')
    s += SL(Z_SRED, tusklaya_lampochka(420, 120, t, 1.2, True))
    dvx, dvy, dvw, dvh = 1120, 170, 620, 760
    s += SL(Z_SRED, f'<rect x="{dvx-44}" y="{dvy-44}" width="{dvw+88}"'
                    f' height="{dvh+44}" rx="10" fill="#8f8898" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="#2a2b36"/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="{SVET}" opacity=".12"/>')
    for i in range(4):                  # лестничная клетка за дверью
        s += SL(Z_SRED, f'<path d="M{dvx:.0f},{dvy+dvh-i*120:.0f} h{dvw:.0f}'
                        f' l0,-26 h{-dvw:.0f} Z" fill="#3c3d4a" opacity=".9"/>')
    sos = ((dvx + 130, 900, 500, "#3c4656", False, True), (dvx + 310, 880, 470, "#5b4450", True, False),
           (dvx + 480, 860, 440, "#3f5c4a", False, False))
    for i, (fx, fy, fh, col, pl, sh) in enumerate(sos):
        pere = 4.0 * A.w(t, 1.6, i * .35)
        s += SL(Z_SRED, f'<g transform="rotate({pere:.1f} {fx:.0f} {fy:.0f})">'
                        + figura(fx, fy, fh, t, col, "#e8eef6", pl, i * .3, True,
                                 1.0, False, 0.0, False, sh) + '</g>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="none" {o(10)}/>')
    s += SL(Z_SRED, dver(dvx - 560, dvy, 520, dvh, .25, "#c9c2cc", False, True))
    hod = A.w(t, 3.4, .1)               # вещь едет к двери и обратно
    sx_ = 560 + hod * 180
    s += SL(Z_SRED, figura(sx_, 1020, 560, t, "#8f3a42", "#ffd98a", True, .2, True))
    strem_x = sx_ + 170 + hod * 90
    strem = (f'<g transform="rotate({-6+4*hod:.1f} {strem_x:.0f} 980)">')
    for sgn in (-1, 1):
        strem += (f'<rect x="{strem_x+sgn*90-16:.0f}" y="330" width="32" height="650"'
                  f' rx="10" fill="#b9bec6" {o(7)}/>')
    for i in range(6):
        strem += (f'<rect x="{strem_x-96:.0f}" y="{400+i*110:.0f}" width="192"'
                  f' height="26" rx="8" fill="#9aa3ab" {o(5)}/>')
    strem += (f'<rect x="{strem_x-110:.0f}" y="320" width="220" height="40" rx="12"'
              f' fill="#8a929a" {o(6)}/>')
    strem += '</g>'
    s += SL(Z_SRED, strem)
    ruk, (hx, hy) = rukav(sx_ + 90, 690, 130, -16, t, "#8f3a42", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    kn_y = 790 + 34 * A.w(t, 2.2, .3)
    kni = (f'<g transform="rotate({-8+6*A.w(t,2.2,.3):.1f} 620 {kn_y:.0f})">'
           f'<rect x="470" y="{kn_y-170:.0f}" width="300" height="340" rx="10"'
           f' fill="{TKAN}" {o(8)}/>'
           f'<rect x="470" y="{kn_y-170:.0f}" width="54" height="340" rx="8"'
           f' fill="#7a1c22" {o(6)}/>')
    for i in range(9):
        kni += (f'<rect x="{534:.0f}" y="{kn_y-150+i*34:.0f}" width="220"'
                f' height="22" fill="#efe8d6" opacity=".9"/>')
    kni += (f'<path d="M510,{kn_y-130:.0f} q0,160 0,250" fill="none" stroke="{ZOL}"'
            f' stroke-width="10" opacity=".8"/></g>')
    s += SL(Z_SRED, kni)
    fm_x, fm_y = 250, 930
    fm = (f'<ellipse cx="{fm_x:.0f}" cy="{fm_y:.0f}" rx="190" ry="76"'
          f' fill="#b9bec6" {o(8)}/>')
    fm += (f'<ellipse cx="{fm_x:.0f}" cy="{fm_y-20:.0f}" rx="160" ry="60"'
           f' fill="#cfd6dc" {o(5)}/>')
    for i in range(14):                 # волнистый край формы
        a = i * (6.28 / 14)
        fm += (f'<ellipse cx="{fm_x+math.cos(a)*175:.0f}"'
               f' cy="{fm_y+math.sin(a)*68:.0f}" rx="26" ry="16" fill="#b9bec6"'
               f' {o(4)}/>')
    fm += (f'<path d="M{fm_x-110:.0f},{fm_y-34:.0f} q110,-30 220,0" fill="none"'
           f' stroke="#eef4f8" stroke-width="12"'
           f' opacity="{.4+.4*abs(A.w(t,2.0,.2)):.2f}"/>')
    s += SL(Z_SRED, fm)
    s += SL(Z_SRED, svecha(880, 560, t, .2, 1.4, 130))
    s += SL(Z_SRED, teplo(890, 530, 460, 420, .38 + .12 * abs(A.w(t, 1.5))))
    tmb = (f'<rect x="700" y="760" width="320" height="180" rx="14"'
           f' fill="url(#derev)" {o(8)}/>')
    tmb += (f'<rect x="684" y="736" width="352" height="34" rx="10" fill="{DOSKA2}" {o(6)}/>')
    for i in range(3):
        tmb += (f'<rect x="{724+i*100:.0f}" y="800" width="76" height="100" rx="8"'
                f' fill="#8f8898" opacity=".9" {o(4)}/>')
    s += SL(Z_SRED, tmb)
    s += ramka_pp("levo", "#1a1620", .42)
    s += vinetka(.44)
    return s


# ── 56 ─────────────────────────────────────────────────────────────────────
def chuzhaya_shal_i_chuzhaya_drel(t):
    """Соседка через порог протягивает нарядную шаль с кистями, сосед из-за её
    плеча — дрель, а хозяйка прячет обе руки за спину."""
    rnd = random.Random(5603)
    s = f'<rect width="{W}" height="{H}" fill="#423c48"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#5e5766"/>')
    for i in range(12):
        s += SL(Z_DAL, f'<path d="M{70+i*170},0 q26,540 0,1080" fill="none"'
                       f' stroke="#6b6474" stroke-width="44" opacity=".5"/>')
    s += kvartira_veschi(40, 900, 520, t, 5609)
    s += SL(Z_SRED, polovicy(930))
    dvx, dvy, dvw, dvh = 980, 150, 700, 800
    s += SL(Z_SRED, f'<rect x="{dvx-48}" y="{dvy-48}" width="{dvw+96}"'
                    f' height="{dvh+48}" rx="12" fill="#8a8292" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="#2b2c38"/>')
    s += SL(Z_SRED, teplo(dvx + dvw * .5, dvy + dvh * .4, 420, 420, .22))
    s += SL(Z_SRED, tusklaya_lampochka(dvx + dvw * .5, dvy + 60, t, .9, False))
    s += SL(Z_SRED, f'<rect x="{dvx-20}" y="{dvy+dvh}" width="{dvw+40}" height="46"'
                    f' rx="10" fill="url(#derev)" {o(8)}/>')
    sx_ = dvx + 230
    s += SL(Z_SRED, figura(sx_, dvy + dvh - 6, 620, t, "#5b4450", "#ffd98a", True,
                           .3, True))
    sos_x = dvx + 520
    s += SL(Z_SRED, figura(sos_x, dvy + dvh - 30, 560, t, "#3c4656", "#cfe4f5",
                           False, .7, True, 1.0, False, 1.0, True))
    poj = A.ease(A.seg(t, 3.0, 1.2))
    s += SL(Z_SRED, f'<path d="M{sos_x-70:.0f},{dvy+dvh-430:.0f}'
                    f' q70,{-30-24*poj:.0f} 140,0" fill="none" stroke="#3c4656"'
                    f' stroke-width="44" stroke-linecap="round"/>')
    uezd = A.ease(A.seg(t, 2.6, 1.4))
    ruk_d, (dx2, dy2) = rukav(sos_x - 80, dvy + dvh - 380, 220 - 90 * uezd,
                              170 + 10 * A.w(t, 1.6), t, "#3c4656", "#cfe4f5", .4, 4.0)
    s += SL(Z_SRED, ruk_d)
    drl = (f'<g transform="rotate({-14+6*A.w(t,1.4,.2):.1f} {dx2:.0f} {dy2:.0f})">'
           f'<path d="M{dx2-96:.0f},{dy2-54:.0f} h150 q40,0 40,54 q0,54 -40,54'
           f' h-150 Z" fill="{KRAS}" {o(8)}/>'
           f'<rect x="{dx2-130:.0f}" y="{dy2-28:.0f}" width="46" height="56" rx="10"'
           f' fill="{ZHELEZ}" {o(5)}/>'
           f'<rect x="{dx2-180:.0f}" y="{dy2-14:.0f}" width="60" height="28" rx="8"'
           f' fill="#8a9398" {o(4)}/>'
           f'<path d="M{dx2-40:.0f},{dy2+54:.0f} h90 l10,110 h-110 Z"'
           f' fill="#2f3a44" {o(6)}/>'
           f'<circle cx="{dx2+34:.0f}" cy="{dy2:.0f}" r="16" fill="#cfd6dc"'
           f' opacity="{.5+.4*abs(A.w(t,.6)):.2f}"/></g>')
    s += SL(Z_SRED, drl)
    ruk_sh, (shx, shy) = rukav(sx_ - 110, dvy + dvh - 400, 230,
                               186 + 8 * A.w(t, 1.3), t, "#5b4450", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk_sh)
    kach = 6.0 * A.w(t, 1.5, .1)
    sh = f'<g transform="rotate({kach:.1f} {shx:.0f} {shy-40:.0f})">'
    sh += (f'<path d="M{shx-210:.0f},{shy-70:.0f} q210,-60 420,0'
           f' L{shx+30:.0f},{shy+250:.0f} q-30,30 -60,0 Z"'
           f' fill="{TKAN}" {o(9)}/>')
    for i in range(5):                  # складки сходятся к углу косынки
        sh += (f'<path d="M{shx-170+i*86:.0f},{shy-50:.0f}'
               f' Q{shx-40+i*20:.0f},{shy+120:.0f} {shx:.0f},{shy+240:.0f}"'
               f' fill="none" stroke="{ZOL}" stroke-width="8" opacity=".7"/>')
    sh += (f'<path d="M{shx-180:.0f},{shy-50:.0f} q180,70 360,0" fill="none"'
           f' stroke="#f2e2c8" stroke-width="13" opacity=".7"/>')
    for i in range(12):                 # кисти по обоим косым краям
        k = i / 11.0
        kx_ = shx - 210 + k * 210
        ky2 = shy - 70 + k * 316
        for sgn in (-1, 1):
            tx2 = shx + sgn * (210 - k * 210)
            sh += (f'<path d="M{tx2:.0f},{ky2:.0f}'
                   f' l{-4+3*A.w(t,1.8,i*.2):.1f},54" stroke="{TKAN}"'
                   f' stroke-width="9" stroke-linecap="round"/>')
            sh += (f'<circle cx="{tx2:.0f}" cy="{ky2:.0f}" r="8" fill="{ZOL}"/>')
    sh += '</g>'
    s += SL(Z_SRED, sh)
    hx = 560
    s += SL(Z_SRED, figura(hx, 1030, 660, t, "#4a2f3c", "#ffd98a", True, .5))
    pr = A.ease(A.seg(t, 1.6, 1.2))
    for i, sgn in enumerate((-1, 1)):
        ug = (16 + 40 * pr) * sgn + (180 if sgn < 0 else 0)
        ruk, (ax, ay) = rukav(hx + sgn * 120, 640, 170 - 50 * pr, ug, t,
                              "#4a2f3c", "#ffd98a", .2 + i * .3, 4.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="28" ry="22"'
                        f' fill="#e3c6a8" opacity="{1-pr*.75:.2f}" {o(4)}/>')
    s += SL(Z_SRED, svecha(260, 640, t, .2, 1.5, 140))
    s += SL(Z_SRED, teplo(270, 610, 480, 440, .4 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, kot(880, 1060, t, .85, "#3b3430"))
    s += ramka_pp("levo", "#181220", .44)
    s += vinetka(.46)
    return s


# ── 57 ─────────────────────────────────────────────────────────────────────
def sosed_u_dveri_zaglyanite_zavtra(t):
    """Хозяйка в дверях показывает соседу листки численника: сегодняшний
    перечёркнут, завтрашний обведён — сосед кивает и уходит со стремянкой."""
    rnd = random.Random(5701)
    s = f'<rect width="{W}" height="{H}" fill="#464050"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#67606e"/>')
    for i in range(12):
        s += SL(Z_DAL, f'<rect x="{i*165}" y="0" width="70" height="1080"'
                       f' fill="#746c7c" opacity=".45"/>')
    s += SL(Z_DAL, f'<rect x="0" y="910" width="{W}" height="170" fill="#514b5a" {o(5)}/>')
    dvx, dvy, dvw, dvh = 240, 150, 620, 800
    s += SL(Z_SRED, f'<rect x="{dvx-44}" y="{dvy-44}" width="{dvw+88}"'
                    f' height="{dvh+44}" rx="12" fill="#8a8292" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="#2f2a26"/>')
    s += SL(Z_SRED, teplo(dvx + dvw * .5, dvy + dvh * .5, 460, 440, .4))
    s += SL(Z_SRED, tusklaya_lampochka(dvx + dvw * .5, dvy + 70, t, 1.0, True))
    s += SL(Z_SRED, dver(dvx + dvw, dvy, 440, dvh, .35, "#c9c2cc", False, True))
    hx = dvx + dvw * .52
    s += SL(Z_SRED, figura(hx, dvy + dvh - 10, 640, t, "#8f3a42", "#ffd98a", True, .2))
    ruk, (px2, py2) = rukav(hx + 150, dvy + 330, 210, -10 + 12 * A.w(t, 1.4), t,
                            "#8f3a42", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{px2:.0f}" cy="{py2:.0f}" rx="32" ry="24"'
                    f' fill="#e3c6a8" {o(5)}/>')
    chx, chy = 1180, 520
    chis = (f'<rect x="{chx-200:.0f}" y="{chy-330:.0f}" width="400" height="120"'
            f' rx="12" fill="#8a929a" {o(8)}/>')
    chis += (f'<circle cx="{chx:.0f}" cy="{chy-270:.0f}" r="26" fill="#cfd6dc" {o(5)}/>')
    s += SL(Z_SRED, chis)
    otr = A.ease(A.seg(t, 2.6, .9))
    s += SL(Z_SRED, _listok(chx, chy + 230, 360, 440, t, True, False, otr))
    if otr > .4:                        # под оторванным — завтрашний, обведён
        s += SL(Z_SRED, _listok(chx, chy + 210, 344, 424, t, False, True, 0.0))
    s += SL(Z_SRED, f'<rect x="{chx-176:.0f}" y="{chy-216:.0f}" width="352"'
                    f' height="40" rx="10" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, teplo(chx, chy, 420, 400, .26 + .08 * abs(A.w(t, 1.6))))
    paletz = A.ease(A.seg(t, .4, .8))
    ruk2, (fx2, fy2) = rukav(hx + 190, dvy + 430, 240 + 60 * paletz,
                             -6 + 6 * A.w(t, 1.1), t, "#8f3a42", "#ffd98a", .5, 3.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{fx2:.0f}" cy="{fy2:.0f}" rx="40" ry="26"'
                    f' fill="#e3c6a8" {o(5)}/>')
    kiv = 7.0 * A.w(t, 1.1, .2)
    sx_ = 1620
    s += SL(Z_SRED, f'<g transform="rotate({kiv:.1f} {sx_:.0f} 820)">'
                    + figura(sx_, 1040, 560, t, "#3c4656", "#e8eef6", False, .6,
                             True, 1.0, False, 0.0, True) + '</g>')
    uhod = A.ease(A.seg(t, 1.8, 1.6))
    strx = 1700 + uhod * 90
    strem = f'<g transform="rotate({12+6*A.w(t,2.4,.3):.1f} {strx:.0f} 1000)">'
    for sgn in (-1, 1):
        strem += (f'<rect x="{strx+sgn*80-14:.0f}" y="380" width="28" height="620"'
                  f' rx="10" fill="#b9bec6" {o(7)}/>')
    for i in range(5):
        strem += (f'<rect x="{strx-86:.0f}" y="{450+i*120:.0f}" width="172"'
                  f' height="24" rx="8" fill="#9aa3ab" {o(5)}/>')
    strem += '</g>'
    s += SL(Z_SRED, strem)
    s += SL(Z_SRED, svecha(1000, 980, t, .3, 1.3, 120))
    s += SL(Z_SRED, teplo(1010, 950, 400, 360, .34 + .1 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, f'<rect x="900" y="860" width="260" height="180" rx="12"'
                    f' fill="url(#derev)" {o(8)}/>'
                    f'<rect x="884" y="838" width="292" height="32" rx="10"'
                    f' fill="{DOSKA2}" {o(6)}/>')
    ves = (f'<rect x="1300" y="300" width="460" height="28" rx="8"'
           f' fill="url(#derev)" {o(7)}/>')
    for i in range(4):
        ves += (f'<circle cx="{1360+i*110:.0f}" cy="344" r="15" fill="{ZHELEZ}" {o(4)}/>')
        ves += (f'<path d="M{1360+i*110:.0f},358 q{-12+8*A.w(t,4.2,i*.2):.1f},140'
                f' {-34+12*A.w(t,4.2,i*.2):.1f},330" fill="none"'
                f' stroke="{[TKAN2, "#5b5a4a", "#7a4a3a", "#3f5c4a"][i]}"'
                f' stroke-width="70" stroke-linecap="round" opacity=".95"/>')
    s += SL(Z_SRED, ves)
    pol = (f'<rect x="1300" y="860" width="440" height="24" rx="8"'
           f' fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        pol += (f'<path d="M{1360+i*140:.0f},858 q10,-54 66,-54 q60,0 64,46'
                f' q-6,26 -64,26 q-56,0 -66,-18 Z"'
                f' fill="{["#4a3f36", "#5b4450", "#2f3a44"][i]}" {o(5)}/>')
    s += SL(Z_SRED, pol)
    kov = (f'<rect x="760" y="1000" width="620" height="80" rx="14"'
           f' fill="#5b4450" {o(7)}/>')
    for i in range(6):
        kov += (f'<rect x="{790+i*100:.0f}" y="1014" width="70" height="60" rx="8"'
                f' fill="#7a5a66" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, kov)
    s += SL(Z_SRED, hodiki(180, 300, t, 1.05))
    s += ramka_pp("pravo", "#1a1620", .42)
    s += vinetka(.44)
    return s


# ── 58 ─────────────────────────────────────────────────────────────────────
def telega_s_uzlami_u_vorot(t):
    """Телега на пол-кадра, нагруженная горой: узлы, перины, самовар, лавка
    вверх ногами и кот в корзине на самом верху."""
    rnd = random.Random(5801)
    s = sumerki_fon(t, True)
    s += ulica_dal(60, 700, 860, t, False, 5807)
    s += SL(Z_DAL, izba_snaruzhi(1320, 790, 560, t, True, True, 5813))
    s += SL(Z_DAL, gryaz_polosa(800, 200, "#473b2e"))
    for sgn, vx in ((-1, 170), (1, 1180)):
        s += SL(Z_DAL, f'<rect x="{vx:.0f}" y="340" width="54" height="520" rx="12"'
                       f' fill="url(#derev)" {o(8)}/>')
    s += SL(Z_DAL, f'<path d="M170,360 q490,-120 1060,0 l0,-50 q-570,-120 -1060,0 Z"'
                   f' fill="{DOSKA2}" {o(8)}/>')
    tx, ty = 820, 930
    kol = ""
    for i, (cx_, r_) in enumerate(((tx - 300, 130), (tx + 290, 150))):
        ang = (t * 30) % 360
        kol += (f'<g transform="rotate({ang:.1f} {cx_:.0f} {ty:.0f})">'
                f'<circle cx="{cx_:.0f}" cy="{ty:.0f}" r="{r_}" fill="none"'
                f' stroke="url(#derev)" stroke-width="26"/>')
        for j in range(8):
            a = j * .785
            kol += (f'<line x1="{cx_:.0f}" y1="{ty:.0f}"'
                    f' x2="{cx_+math.cos(a)*r_:.0f}" y2="{ty+math.sin(a)*r_:.0f}"'
                    f' stroke="url(#derev)" stroke-width="12"/>')
        kol += (f'<circle cx="{cx_:.0f}" cy="{ty:.0f}" r="26" fill="{ZHELEZ}" {o(5)}/></g>')
    s += SL(Z_SRED, kol)
    tel = (f'<rect x="{tx-400:.0f}" y="{ty-170:.0f}" width="800" height="120" rx="12"'
           f' fill="url(#dosk)" {o(9)}/>')
    for i in range(9):
        tel += (f'<rect x="{tx-390+i*88:.0f}" y="{ty-166:.0f}" width="70"'
                f' height="112" rx="8" fill="url(#dosk)" {o(5)}/>')
    tel += (f'<path d="M{tx-430:.0f},{ty-190:.0f} h860 l-20,30 h-820 Z"'
            f' fill="{DOSKA2}" {o(6)}/>')
    tel += (f'<path d="M{tx-420:.0f},{ty-120:.0f} l-260,-80" stroke="url(#derev)"'
            f' stroke-width="24" stroke-linecap="round"/>')
    s += SL(Z_SRED, tel)
    kach = 2.6 * A.w(t, 1.9, .1)
    gora = f'<g transform="rotate({kach:.2f} {tx:.0f} {ty-180:.0f})">'
    for i in range(6):                  # узлы
        ux = tx - 330 + (i % 3) * 230 + (i // 3) * 90
        uy = ty - 240 - (i // 3) * 190
        col = [TKAN, TKAN2, "#6b8a4a", "#8a6a3a", "#7a4a5a", "#4a6a7a"][i]
        gora += (f'<path d="M{ux-120:.0f},{uy+40:.0f} q-20,-130 120,-150'
                 f' q140,20 120,150 q-120,50 -240,0 Z" fill="{col}" {o(7)}/>')
        for sgn in (-1, 1):             # завязанные углы узла
            gora += (f'<path d="M{ux+sgn*70:.0f},{uy-110:.0f}'
                     f' q{sgn*60:.0f},-50 {sgn*86:.0f},-14'
                     f' q{-sgn*40:.0f},40 {-sgn*76:.0f},44 Z" fill="{col}" {o(5)}/>')
        gora += (f'<ellipse cx="{ux:.0f}" cy="{uy-110:.0f}" rx="46" ry="26"'
                 f' fill="{col}" {o(5)}/>')
        gora += (f'<path d="M{ux-100:.0f},{uy-20:.0f} q100,46 200,0" fill="none"'
                 f' stroke="#efe3c8" stroke-width="12" opacity=".75"/>')
        gora += (f'<path d="M{ux-96:.0f},{uy+28:.0f} q96,40 192,0" fill="none"'
                 f' stroke="#efe3c8" stroke-width="9" opacity=".5"/>')
    for i in range(2):                  # перины
        gora += (f'<path d="M{tx-320+i*300:.0f},{ty-540:.0f} q200,-80 400,0'
                 f' q-20,90 -200,96 q-180,-6 -200,-96 Z" fill="#eef2f6" {o(7)}/>')
        gora += (f'<path d="M{tx-300+i*300:.0f},{ty-520:.0f} q180,40 360,0"'
                 f' fill="none" stroke="#b9c6cf" stroke-width="9" opacity=".8"/>')
    lav = (f'<g transform="rotate(188 {tx+330:.0f} {ty-440:.0f})">'
           f'<rect x="{tx+180:.0f}" y="{ty-470:.0f}" width="300" height="30" rx="10"'
           f' fill="url(#derev)" {o(6)}/>'
           f'<rect x="{tx+200:.0f}" y="{ty-440:.0f}" width="26" height="120"'
           f' fill="url(#derev)" {o(5)}/>'
           f'<rect x="{tx+430:.0f}" y="{ty-440:.0f}" width="26" height="120"'
           f' fill="url(#derev)" {o(5)}/></g>')
    gora += lav
    gora += '</g>'
    s += SL(Z_SRED, gora)
    sx_, sy_ = tx - 150, ty - 660
    sam = (f'<path d="M{sx_-150:.0f},{sy_:.0f} q-54,-200 80,-256 q66,-26 134,0'
           f' q134,56 80,256 Z" fill="url(#zol)" {o(9)}/>')
    sam += (f'<path d="M{sx_-130:.0f},{sy_-120:.0f} q130,54 260,0" fill="none"'
            f' stroke="#fff3cc" stroke-width="10" opacity=".6"/>')
    sam += (f'<rect x="{sx_-70:.0f}" y="{sy_-250:.0f}" width="140" height="64" rx="10"'
            f' fill="url(#zol)" {o(6)}/>')
    sam += (f'<rect x="{sx_-40:.0f}" y="{sy_-330:.0f}" width="80" height="90" rx="8"'
            f' fill="url(#med)" {o(6)}/>')
    sam += (f'<path d="M{sx_+100:.0f},{sy_-90:.0f} q60,10 50,70" fill="none"'
            f' stroke="url(#zol)" stroke-width="18" stroke-linecap="round"/>')
    for sgn in (-1, 1):
        sam += (f'<path d="M{sx_+sgn*110:.0f},{sy_-130:.0f} q{sgn*60:.0f},10'
                f' {sgn*10:.0f},70" fill="none" stroke="url(#med)" stroke-width="16"/>')
    sam += (f'<ellipse cx="{sx_:.0f}" cy="{sy_+6:.0f}" rx="120" ry="24"'
            f' fill="url(#med)" {o(6)}/>')
    sam += (f'<path d="M{sx_-60:.0f},{sy_-150:.0f} q20,70 10,120" fill="none"'
            f' stroke="#fff3cc" stroke-width="16"'
            f' opacity="{.35+.35*abs(A.w(t,2.2,.1)):.2f}"/>')
    s += SL(Z_SRED, sam)
    s += SL(Z_SRED, dym(sx_, sy_ - 340, t, 5, .26, 300, .4, "#d8d2c6", .9))
    s += SL(Z_SRED, teplo(sx_, sy_ - 90, 360, 320, .3 + .1 * abs(A.w(t, 1.6))))
    kx_, ky_ = tx + 180, ty - 700
    s += SL(Z_SRED, _korzina(kx_, ky_, 300, 220, t, 5821, False))
    vygl = 24 * abs(A.w(t, 2.2, .2))
    s += SL(Z_SRED, f'<g transform="translate(0,{-vygl:.0f})">'
                    + kot(kx_, ky_ - 160, t, .8, "#4a4038") + '</g>')
    mah = 26 * A.w(t, 1.2, .1)
    zx_ = 1560
    s += SL(Z_SRED, figura(zx_, 980, 500, t, "#5b2f3a", "#ffd98a", True, .3, True))
    ruk, (ax, ay) = rukav(zx_ - 90, 700, 190, 236 + mah, t, "#5b2f3a", "#ffd98a", .2, 8.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="28" ry="22"'
                    f' fill="#e3c6a8" {o(4)}/>')
    fnx, fny = 230, 420
    s += SL(Z_SRED, f'<path d="M{fnx-62:.0f},{fny:.0f} h124 l-14,-34 h-96 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-52:.0f},{fny:.0f} h104 l-12,124 h-80 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 112, t, .56, .3, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 70, 330, 300, .42 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_PERED, pleten(1480, 1080, 440, 210, 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 5827, .46, .9))
    s += vinetka(.46)
    return s


# ── 59 ─────────────────────────────────────────────────────────────────────
def novaya_izba_bez_lada(t):
    """Новая изба из свежих брёвен в разрезе: гости с караваем на пороге, а
    внутри всё вкривь — лавку тянут врозь, ухват падает, каша лезет."""
    rnd = random.Random(5903)
    s = sumerki_fon(t, False)
    s += ulica_dal(1300, 660, 620, t, False, 5923)
    s += SL(Z_DAL, gryaz_polosa(820, 180, "#5a4c3a"))
    izb = (f'<rect x="70" y="180" width="1300" height="760" fill="#c49a62" {o(10)}/>')
    for i in range(9):                  # свежие светлые брёвна
        izb += (f'<rect x="70" y="{180+i*86:.0f}" width="1300" height="82" rx="38"'
                f' fill="#d8b07a" {o(5)}/>')
        izb += (f'<rect x="84" y="{232+i*86:.0f}" width="1272" height="14" rx="7"'
                f' fill="#b08a52" opacity=".5"/>')
    izb += (f'<path d="M20,190 L720,-120 L1420,190 Z" fill="#b98f5a" {o(9)}/>')
    izb += (f'<rect x="1060" y="-170" width="110" height="230" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(1116, -160, t, 5, .22, 320, .34, "#d8d2c6", 1.0))
    s += SL(Z_SRED, f'<rect x="130" y="260" width="1180" height="620" fill="#4a3826"'
                    f' opacity=".92" {o(8)}/>')
    s += SL(Z_SRED, f'<line x1="130" y1="580" x2="1310" y2="580" stroke="#6b4a2a"'
                    f' stroke-width="20"/>')
    s += SL(Z_SRED, polovicy(880))
    s += SL(Z_SRED, pech(880, 300, 400, 560, t, True, True, False))
    s += SL(Z_SRED, teplo(1060, 640, 460, 380, .4 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, iskra_let(t, 1000, 580, 8, 5927, 280, .45))
    chx, chy = 1180, 360
    s += SL(Z_SRED, f'<path d="M{chx-90:.0f},{chy:.0f} q90,150 180,0'
                    f' q-90,40 -180,0 Z" fill="url(#chug)" {o(7)}/>'
                    f'<ellipse cx="{chx:.0f}" cy="{chy-6:.0f}" rx="94" ry="26"'
                    f' fill="#4a4645" {o(5)}/>')
    for i in range(6):                  # каша лезет из чугунка
        k = ((t * .6) + i * .17) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{chx-70+i*28:.0f}" cy="{chy-18+k*110:.0f}"'
                        f' rx="{26-6*k:.0f}" ry="{20-5*k:.0f}" fill="#efe3c8"'
                        f' opacity="{.95-.4*k:.2f}" {o(3)}/>')
    s += SL(Z_SRED, par(chx, chy - 40, t, 4, .5, 170, .5, .9))
    lx_, ly_ = 540, 790
    tyan = A.w(t, 1.6, .1)
    s += SL(Z_SRED, f'<g transform="rotate({3*tyan:.1f} {lx_:.0f} {ly_:.0f})">'
                    + lavka(lx_ - 230 + tyan * 24, ly_, 460) + '</g>')
    for i, sgn in enumerate((-1, 1)):
        fx = lx_ + sgn * (330 + tyan * sgn * 26)
        s += SL(Z_SRED, figura(fx, 880, 520, t, "#5b2f3a" if sgn > 0 else "#3c4656",
                               "#ffd98a", sgn > 0, i * .4, True))
        ruk, (ax, ay) = rukav(fx - sgn * 90, 660, 170, 180 if sgn > 0 else 0, t,
                              "#5b2f3a" if sgn > 0 else "#3c4656", "#ffd98a", i * .3, 5.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="26" ry="20"'
                        f' fill="#e3c6a8" {o(4)}/>')
    pad = A.out(A.seg(t, 1.4, .9))
    uhx, uhy = 760, 500
    s += SL(Z_SRED, f'<g transform="rotate({-10+96*pad:.0f} {uhx:.0f} {uhy+260:.0f})">'
                    f'<rect x="{uhx-14:.0f}" y="{uhy:.0f}" width="28" height="300"'
                    f' rx="10" fill="url(#derev)" {o(6)}/>'
                    f'<path d="M{uhx-64:.0f},{uhy+10:.0f} q64,-92 128,0" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="22"/></g>')
    for i in range(3):
        s += SL(Z_SRED, krynka(690 + i * 86, 870 + (i % 2) * 10,
                               1.0 + .2 * (i % 2)))
    for i in range(5):                  # черепки и брызги от падения
        if pad > .5:
            s += SL(Z_SRED, f'<path d="M{700+i*60:.0f},{866:.0f} l26,-20 l10,24 Z"'
                            f' fill="#9c6a3c" opacity="{(pad-.5)*2:.2f}" {o(3)}/>')
    s += SL(Z_SRED, kot(330, 860, t, .95, "#3b3430", True))
    sob_x = 200
    s += SL(Z_SRED, f'<ellipse cx="{sob_x:.0f}" cy="840" rx="78" ry="48"'
                    f' fill="#7a6246" {o(6)}/>'
                    f'<circle cx="{sob_x-56:.0f}" cy="800" r="40" fill="#7a6246" {o(6)}/>'
                    f'<path d="M{sob_x-96:.0f},770 l-16,-44 l40,16 Z" fill="#6b5436" {o(4)}/>'
                    f'<path d="M{sob_x-96:.0f},812 q-30,8 -40,-6" fill="none"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<circle cx="{sob_x-72:.0f}" cy="792" r="6" fill="{K}"/>'
                    f'<path d="M{sob_x+70:.0f},824 q50,-20 40,-70" fill="none"'
                    f' stroke="#7a6246" stroke-width="18" stroke-linecap="round"/>')
    gx_ = 1560
    s += SL(Z_SRED, f'<rect x="1380" y="880" width="520" height="40" rx="10"'
                    f' fill="url(#dosk)" {o(7)}/>')
    s += SL(Z_SRED, figura(gx_, 880, 500, t, "#4a5a6b", "#ffd0a0", False, .3, True,
                           1.0, True, 1.0, True, True))
    s += SL(Z_SRED, figura(gx_ + 190, 884, 470, t, "#6b4450", "#ffd0a0", True, .7, True))
    s += SL(Z_SRED, karavay(gx_ + 90, 640, 1.3, True))
    s += SL(Z_SRED, para_izo_rta(gx_ + 46, 500, t, .2, 1.0, .5))
    s += ramka_pp("levo", "#1d150c", .42)
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 5939, .36, .8))
    s += vinetka(.44)
    return s


# ── 60 ─────────────────────────────────────────────────────────────────────
def gruzovik_u_podezda(t):
    """Фургон без надписей у подъезда на пол-кадра: двое грузчиков вертят в
    дверях диван, на балконе шарики, а женщина показывает им календарь."""
    rnd = random.Random(6007)
    s = f'<rect width="{W}" height="{H}" fill="#1c2430"/>'
    s += nebo("sumer", t, True, 6011)
    s += panelka(-200, 620, 1000, t, 4, True, 6029)
    s += panelka(1500, 600, 560, t, 4, True, 6037)
    s += SL(Z_DAL, gryaz_polosa(900, 190, "#2b3038"))
    pd = (f'<rect x="700" y="180" width="700" height="740" fill="url(#beton)" {o(9)}/>')
    pd += (f'<path d="M640,420 h820 l-50,-110 h-720 Z" fill="{BETON2}" {o(8)}/>')
    pd += (f'<rect x="900" y="440" width="320" height="480" rx="8" fill="#3d4650" {o(8)}/>')
    pd += (f'<rect x="950" y="490" width="220" height="200" rx="8"'
           f' fill="url(#stekl)" opacity=".5" {o(5)}/>')
    s += SL(Z_SRED, pd)
    s += SL(Z_SRED, tusklaya_lampochka(1060, 400, t, .9, False))
    bal = (f'<rect x="720" y="120" width="420" height="40" rx="8" fill="{BETON2}" {o(6)}/>')
    for i in range(9):
        bal += (f'<rect x="{736+i*46:.0f}" y="20" width="14" height="100" rx="5"'
                f' fill="#8a929a" {o(3)}/>')
    s += SL(Z_SRED, bal)
    for i in range(5):                  # шарики к новоселью
        kx_ = 760 + i * 84
        kach = 16 * A.w(t, 2.2 + i * .3, i * .2)
        bal_c = [KRAS, "#3a7ad0", ZEL2, ZOL, "#b05aa0"][i]
        s += SL(Z_SRED, f'<g transform="translate({kach:.1f},0)">'
                        f'<ellipse cx="{kx_:.0f}" cy="{210+((i%2)*26):.0f}" rx="40"'
                        f' ry="50" fill="{bal_c}" {o(5)}/>'
                        f'<path d="M{kx_:.0f},{260+((i%2)*26):.0f} q14,60 -10,120"'
                        f' fill="none" stroke="#e8eef6" stroke-width="4"/>'
                        f'<ellipse cx="{kx_-14:.0f}" cy="{194+((i%2)*26):.0f}" rx="12"'
                        f' ry="16" fill="#ffffff" opacity=".45"/></g>')
    fx_, fy_ = 400, 900
    fur = ten(fx_ + 60, fy_ + 16, 460, 26, .5)
    fur += (f'<rect x="{fx_-360:.0f}" y="{fy_-480:.0f}" width="760" height="420"'
            f' rx="16" fill="#cfd6dc" {o(10)}/>')
    fur += (f'<path d="M{fx_+400:.0f},{fy_-60:.0f} l0,-300 l120,-20 l90,140 l0,180 Z"'
            f' fill="#b9c2c8" {o(9)}/>')
    fur += (f'<path d="M{fx_+430:.0f},{fy_-340:.0f} l90,-14 l64,118 h-154 Z"'
            f' fill="url(#stekl)" opacity=".75" {o(5)}/>')
    fur += (f'<circle cx="{fx_+586:.0f}" cy="{fy_-120:.0f}" r="26" fill="{SVET}"'
            f' opacity="{.5+.4*abs(A.w(t,1.8)):.2f}" {o(4)}/>')
    fur += teplo(fx_ + 600, fy_ - 120, 260, 200, .34)
    zakr = A.ease(A.seg(t, 4.0, 1.6))
    fur += (f'<g transform="rotate({-20+18*zakr:.0f} {fx_-360:.0f} {fy_-60:.0f})">'
            f'<rect x="{fx_-540:.0f}" y="{fy_-470:.0f}" width="190" height="410"'
            f' rx="10" fill="#dfe6ea" {o(8)}/>'
            f'<rect x="{fx_-522:.0f}" y="{fy_-450:.0f}" width="154" height="370"'
            f' rx="8" fill="none" stroke="#9aa3ab" stroke-width="8"/>'
            f'<circle cx="{fx_-376:.0f}" cy="{fy_-266:.0f}" r="14" fill="#8a929a"/></g>')
    for cx_ in (fx_ - 230, fx_ + 310):
        ang = (t * 40) % 360
        fur += (f'<g transform="rotate({ang:.0f} {cx_:.0f} {fy_-30:.0f})">'
                f'<circle cx="{cx_:.0f}" cy="{fy_-30:.0f}" r="92" fill="#2b2f34" {o(6)}/>'
                f'<circle cx="{cx_:.0f}" cy="{fy_-30:.0f}" r="44" fill="#8a929a" {o(5)}/>'
                f'<line x1="{cx_-40:.0f}" y1="{fy_-30:.0f}" x2="{cx_+40:.0f}"'
                f' y2="{fy_-30:.0f}" stroke="#5e666c" stroke-width="10"/></g>')
    s += SL(Z_SRED, fur)
    div_a = -16 + 44 * abs(A.w(t, 1.1, .1))
    dvx_, dvy_ = 1030, 820
    div = f'<g transform="rotate({div_a:.0f} {dvx_:.0f} {dvy_:.0f})">'
    div += (f'<rect x="{dvx_-240:.0f}" y="{dvy_-120:.0f}" width="480" height="150"'
            f' rx="24" fill="#6b5a7a" {o(8)}/>')
    div += (f'<rect x="{dvx_-240:.0f}" y="{dvy_-250:.0f}" width="480" height="150"'
            f' rx="24" fill="#7a6a8a" {o(8)}/>')
    for i in range(3):
        div += (f'<rect x="{dvx_-220+i*156:.0f}" y="{dvy_-110:.0f}" width="140"'
                f' height="120" rx="18" fill="#8a7a9a" opacity=".9" {o(4)}/>')
    for sgn in (-1, 1):
        div += (f'<rect x="{dvx_+sgn*240-40:.0f}" y="{dvy_-250:.0f}" width="80"'
                f' height="280" rx="20" fill="#6b5a7a" {o(6)}/>')
    div += '</g>'
    s += SL(Z_SRED, div)
    for i, gx in enumerate((850, 1240)):
        s += SL(Z_SRED, figura(gx, 1040, 520, t, "#3a4a3a", "#cfe4f5", False,
                               i * .4, True, 1.0, False, 1.2, False, True))
        ruk, (ax, ay) = rukav(gx + (90 if i else -90), 740, 160,
                              (0 if i else 180) + (12 if i else -12), t, "#3a4a3a",
                              "#cfe4f5", i * .3, 4.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, para_izo_rta(gx + 44, 660, t, i * .4, 1.0, .5))
    zx_ = 1760
    s += SL(Z_SRED, figura(zx_, 980, 540, t, "#8f3a42", "#ffd0a0", False, .5, True))
    ruk2, (kx2, ky2) = rukav(zx_ - 110, 700, 150, 192, t, "#8f3a42", "#ffd0a0", .3, 4.0)
    s += SL(Z_SRED, ruk2)
    kal_x, kal_y = kx2 - 110, ky2 + 10
    kal = (f'<rect x="{kal_x-150:.0f}" y="{kal_y-190:.0f}" width="300" height="380"'
           f' rx="12" fill="url(#list)" {o(8)}/>')
    kal += (f'<rect x="{kal_x-150:.0f}" y="{kal_y-190:.0f}" width="300" height="80"'
            f' rx="12" fill="{TKAN2}" {o(5)}/>')
    for r in range(4):
        for c in range(5):
            kal += (f'<rect x="{kal_x-126+c*52:.0f}" y="{kal_y-86+r*62:.0f}"'
                    f' width="40" height="44" rx="6" fill="#dfd7c2" {o(2)}/>')
    kal += (f'<g opacity="{.6+.4*abs(A.w(t,1.3)):.2f}">'
            f'<line x1="{kal_x-100:.0f}" y1="{kal_y-70:.0f}" x2="{kal_x-40:.0f}"'
            f' y2="{kal_y-14:.0f}" stroke="{KRAS}" stroke-width="12"/>'
            f'<line x1="{kal_x-40:.0f}" y1="{kal_y-70:.0f}" x2="{kal_x-100:.0f}"'
            f' y2="{kal_y-14:.0f}" stroke="{KRAS}" stroke-width="12"/></g>')
    kal += (f'<ellipse cx="{kal_x+64:.0f}" cy="{kal_y+14:.0f}" rx="44" ry="38"'
            f' fill="none" stroke="{ZEL2}" stroke-width="11"'
            f' opacity="{.6+.4*abs(A.w(t,1.1,.3)):.2f}"/>')
    s += SL(Z_SRED, kal)
    s += SL(Z_SRED, f'<rect x="{zx_+40:.0f}" y="640" width="46" height="86" rx="10"'
                    f' fill="#2b2f34" {o(5)}/>'
                    f'<rect x="{zx_+46:.0f}" y="650" width="34" height="64" rx="4"'
                    f' fill="{SVET}" opacity="{.5+.4*abs(A.w(t,1.5,.2)):.2f}"/>')
    s += ramka_pp("pravo", "#0e131a", .44)
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 6043, .46, 1.0))
    s += vinetka(.48)
    return s


# ── 61 ─────────────────────────────────────────────────────────────────────
def kosa_do_poyasa(t):
    """Девушка у окна вполоборота расчёсывает костяным гребнем русую косу до
    пояса, а выпавший волосок прячет в щель между брёвнами."""
    rnd = random.Random(6101)
    s = f'<rect width="{W}" height="{H}" fill="#4a3728"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 112))
    s += utvar_izby(1420, 300, 420, t, 6113)
    s += SL(Z_SRED, polovicy(940))
    ox, oy, ow, oh = 1060, 180, 560, 470
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#b9c6cf"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.66:.0f}" width="{ow}" height="{oh*.34:.0f}"'
           f' fill="#8a9a74"/>')
    za += izba_snaruzhi(ox + 40, oy + oh - 10, 240, t, True, True, 6121)
    za += (f'<circle cx="{ox+ow*.78:.0f}" cy="{oy+oh*.22:.0f}" r="64" fill="#fff3cc"'
           f' opacity=".9"/>')
    s += SL(Z_SRED, f'<clipPath id="ok61"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok61)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .08, False, True))
    s += SL(Z_SRED, luch(ox - 40, oy + oh, 420, 480, t, .26))
    s += SL(Z_SRED, teplo(ox + 100, oy + oh + 160, 620, 520, .34))
    s += SL(Z_SRED, lavka(760, 980, 520))
    dx_, dy_ = 700, 980
    s += SL(Z_SRED, figura(dx_, dy_, 700, t, "#8f3a42", "#ffd98a", False, .2, True))
    s += SL(Z_SRED, f'<path d="M{dx_-90:.0f},{dy_-430:.0f} q90,-30 180,0'
                    f' l30,410 q-120,46 -240,0 Z" fill="#b8323a" opacity=".92" {o(7)}/>')
    for i in range(4):                  # поясок и оборки сарафана
        s += SL(Z_SRED, f'<path d="M{dx_-150:.0f},{dy_-120+i*30:.0f}'
                        f' q150,40 300,0" fill="none" stroke="{ZOL}"'
                        f' stroke-width="7" opacity=".6"/>')
    kx_, ky_ = dx_ - 190, dy_ - 500
    sway = 7 * A.w(t, 1.8, .1)
    kosa = f'<g transform="rotate({sway:.1f} {kx_:.0f} {ky_:.0f})">'
    kosa += (f'<path d="M{kx_+120:.0f},{ky_-80:.0f} q-110,-20 -130,80'
             f' q-16,130 6,260 q16,110 34,220" fill="none" stroke="#c49a4e"'
             f' stroke-width="84" stroke-linecap="round"/>')
    for i in range(7):                  # перевивы косы
        yy = ky_ + 50 + i * 76
        kosa += (f'<path d="M{kx_-52+i*5:.0f},{yy:.0f} q46,26 92,0"'
                 f' fill="none" stroke="#a87c38" stroke-width="10" opacity=".85"/>')
        kosa += (f'<path d="M{kx_-42+i*5:.0f},{yy-18:.0f} q40,22 80,-4"'
                 f' fill="none" stroke="#e8c57c" stroke-width="8"'
                 f' opacity="{.4+.4*abs(A.w(t,2.2,i*.15)):.2f}"/>')
    kosa += (f'<path d="M{kx_+30:.0f},{ky_+570:.0f} q20,40 -20,70" fill="none"'
             f' stroke="{TKAN}" stroke-width="22" stroke-linecap="round"/>')
    kosa += '</g>'
    s += SL(Z_SRED, kosa)
    greb = A.seg(t, .3, 1.8)
    gy_ = ky_ + 90 + greb * 420
    s += SL(Z_SRED, f'<g transform="rotate({8+8*A.w(t,1.4):.0f} {kx_-60:.0f} {gy_:.0f})">'
                    f'<rect x="{kx_-150:.0f}" y="{gy_-24:.0f}" width="180" height="48"'
                    f' rx="12" fill="#efe3c8" {o(6)}/>'
                    + "".join(f'<rect x="{kx_-140+j*24:.0f}" y="{gy_+22:.0f}"'
                              f' width="10" height="48" rx="4" fill="#efe3c8"'
                              f' {o(2)}/>' for j in range(7)) + '</g>')
    ruk, (hx, hy) = rukav(dx_ - 110, dy_ - 430, 150, 200 + 16 * A.w(t, 1.4, .2), t,
                          "#8f3a42", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    smot = A.ease(A.seg(t, 1.4, 1.0))
    vx_ = 330 + smot * 60
    s += SL(Z_SRED, f'<path d="M{vx_:.0f},{700-smot*60:.0f} q30,{60+40*smot:.0f}'
                    f' {-10-20*smot:.0f},{120+60*smot:.0f}" fill="none"'
                    f' stroke="#e8c57c" stroke-width="7" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="{vx_-20:.0f}" cy="{830+smot*40:.0f}"'
                    f' rx="{16+8*smot:.0f}" ry="{10+6*smot:.0f}" fill="none"'
                    f' stroke="#e8c57c" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="270" y="600" width="260" height="16" rx="6"'
                    f' fill="#2b1f14" opacity=".9"/>')
    s += SL(Z_SRED, svecha(260, 760, t, .2, 1.6, 150))
    s += SL(Z_SRED, teplo(270, 720, 520, 470, .4 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, krynka(1700, 1020, 1.4))
    s += SL(Z_PERED, zanaveska(1020, 140, 460, 190, TKAN, t, 1))
    s += ramka_pp("levo", "#1a1208", .42)
    s += vinetka(.44)
    return s


# ── 62 ─────────────────────────────────────────────────────────────────────
def strizhenyy_na_holode(t):
    """Парень со свежей стрижкой вышел на крыльцо без шапки, уши на глазах
    краснеют — и он чихает так, что с соседского пугала слетает шапка.

    Пугало сделано ПУГАЛОМ НАРОЧНО: крестовина на шесте видна насквозь,
    голова — горшок с нарисованной рожицей, из рукавов и подола торчит солома,
    на плече сидит ворона, рядно залатано. Прежде оно читалось вторым
    человеком (осмотр 14.11)."""
    rnd = random.Random(6203)
    s = sumerki_fon(t, True)
    s += ulica_dal(1180, 700, 740, t, False, 6211)
    s += SL(Z_DAL, gryaz_polosa(790, 200, "#473c30"))
    izb = brevna(0, 160, 1000, 700, 110)
    izb += (f'<path d="M-40,170 L500,-110 L1040,170 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="700" y="-160" width="100" height="220" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(750, -150, t, 5, .22, 300, .34, "#c8d0da", 1.0))
    ok = okno_izby(130, 340, 280, 210, t, None, .25, True, True)
    s += SL(Z_SRED, ok)
    s += SL(Z_SRED, teplo(270, 450, 340, 300, .36 + .1 * abs(A.w(t, 1.7))))
    kr = (f'<path d="M420,900 h620 l-40,-120 h-540 Z" fill="url(#dosk)" {o(9)}/>')
    kr += (f'<rect x="440" y="900" width="580" height="46" rx="10" fill="{DOSKA2}" {o(7)}/>')
    for i in range(3):
        kr += (f'<rect x="{460+i*16:.0f}" y="{946+i*40:.0f}" width="{560-i*32:.0f}"'
               f' height="34" rx="8" fill="url(#dosk)" {o(5)}/>')
    kr += (f'<rect x="980" y="400" width="34" height="500" fill="url(#derev)" {o(7)}/>')
    kr += (f'<path d="M400,400 h640 l-30,-54 h-580 Z" fill="{DOSKA2}" {o(7)}/>')
    s += SL(Z_SRED, kr)
    chih = A.seg(t, 2.4, .35)
    nak = -26 * math.sin(min(1.0, chih) * 3.14)
    px_ = 680
    s += SL(Z_SRED, f'<g transform="rotate({nak:.1f} {px_:.0f} 880)">'
                    + figura(px_, 880, 680, t, "#3c4656", "#ffd0a0", False, .2,
                             False, 1.0, False, 1.0) + '</g>')
    kras = A.ease(A.seg(t, .6, 1.8))
    gy_ = 880 - 680 * .845
    for sgn in (-1, 1):                 # уши торчат и краснеют
        s += SL(Z_SRED, f'<g transform="rotate({nak:.1f} {px_:.0f} 880)">'
                        f'<ellipse cx="{px_+sgn*100:.0f}" cy="{gy_+10:.0f}" rx="30"'
                        f' ry="42" fill="#f0cfae" {o(5)}/>'
                        f'<ellipse cx="{px_+sgn*100:.0f}" cy="{gy_+10:.0f}" rx="26"'
                        f' ry="38" fill="{KRAS}" opacity="{.72*kras:.2f}"/></g>')
    s += SL(Z_SRED, f'<g transform="rotate({nak:.1f} {px_:.0f} 880)">'
                    f'<ellipse cx="{px_:.0f}" cy="{gy_+36:.0f}" rx="20" ry="16"'
                    f' fill="{KRAS}" opacity="{.6*kras:.2f}"/>'
                    f'<path d="M{px_-86:.0f},{gy_-72:.0f} q86,-30 172,0" fill="none"'
                    f' stroke="#5a4a36" stroke-width="16" opacity=".9"/></g>')
    ruk, (hx, hy) = rukav(px_ + 110, 560, 150, -96 + 20 * A.w(t, 1.6), t,
                          "#3c4656", "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="34" ry="24"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, para_izo_rta(px_ + 60, gy_ + 40, t, .1,
                                 1.0 + 1.6 * math.sin(min(1.0, chih) * 3.14), .62))
    s += SL(Z_SRED, _vedro(470, 1040, .9, t, False, "url(#chug)"))
    kr_x, kr_y = 1060, 950
    s += SL(Z_SRED, f'<path d="M{kr_x-60:.0f},{kr_y-110:.0f} q60,120 120,0'
                    f' q-60,34 -120,0 Z" fill="url(#krem)" {o(7)}/>'
                    f'<path d="M{kr_x+58:.0f},{kr_y-96:.0f} q46,26 0,58" fill="none"'
                    f' stroke="url(#krem)" stroke-width="12"/>')
    s += SL(Z_SRED, par(kr_x, kr_y - 120, t, 5, .5, 190, .55, .9))
    # ПУГАЛО: шест, крестовина, горшок вместо головы, солома, ворона
    pg_x, pg_y = 1520, 980
    pug = (f'<rect x="{pg_x-15:.0f}" y="{pg_y-520:.0f}" width="30" height="520"'
           f' fill="url(#derev)" {o(6)}/>')
    pug += (f'<path d="M{pg_x-70:.0f},{pg_y:.0f} h140 l-16,-40 h-108 Z"'
            f' fill="#4a4038" opacity=".8"/>')
    pug += (f'<rect x="{pg_x-210:.0f}" y="{pg_y-420:.0f}" width="420" height="26"'
            f' rx="12" fill="url(#derev)" {o(6)}/>')     # крестовина НАСКВОЗЬ видна
    pug += (f'<path d="M{pg_x-26:.0f},{pg_y-430:.0f} q26,-16 52,0 l0,20'
            f' q-26,-12 -52,0 Z" fill="#5a3a22" {o(3)}/>')
    kach_p = 3.0 * A.w(t, 2.9, .2)
    pug += f'<g transform="rotate({kach_p:.1f} {pg_x:.0f} {pg_y-420:.0f})">'
    pug += (f'<path d="M{pg_x-116:.0f},{pg_y-400:.0f} q116,-44 232,0 l-36,236'
            f' q-80,36 -160,0 Z" fill="#6b5a3c" {o(7)}/>')
    for j in range(4):                  # заплаты на рядне
        pug += (f'<rect x="{pg_x-92+j*54:.0f}" y="{pg_y-330+((j%2)*60):.0f}"'
                f' width="46" height="42" rx="6"'
                f' fill="{"#8a6a46" if j % 2 else "#55452e"}" {o(3)}/>')
    for sgn in (-1, 1):                 # рукава на крестовине, из них солома
        pug += (f'<path d="M{pg_x+sgn*116:.0f},{pg_y-412:.0f}'
                f' q{sgn*70:.0f},-6 {sgn*96:.0f},10 l-6,56'
                f' q{-sgn*46:.0f},12 {-sgn*96:.0f},0 Z" fill="#55452e" {o(5)}/>')
        for j in range(6):
            pug += (f'<path d="M{pg_x+sgn*206:.0f},{pg_y-400:.0f}'
                    f' l{sgn*(26+j*10):.0f},{-26+j*16:.0f}" stroke="#d8b96a"'
                    f' stroke-width="7" stroke-linecap="round"/>')
    for j in range(9):                  # солома из-под подола
        pug += (f'<path d="M{pg_x-80+j*20:.0f},{pg_y-164:.0f} l{-8+j*2},62"'
                f' stroke="#d8b96a" stroke-width="7" stroke-linecap="round"/>')
    # голова — глиняный горшок с нарисованной рожицей
    pug += (f'<path d="M{pg_x-62:.0f},{pg_y-430:.0f} q-16,-80 10,-116'
            f' q52,-22 104,0 q26,36 10,116 Z" fill="url(#glina)" {o(7)}/>')
    pug += (f'<ellipse cx="{pg_x:.0f}" cy="{pg_y-546:.0f}" rx="66" ry="18"'
            f' fill="#a06c3c" {o(5)}/>')
    for i in (-1, 1):
        pug += (f'<path d="M{pg_x+i*26-14:.0f},{pg_y-512:.0f} l28,28 m0,-28 l-28,28"'
                f' stroke="{K}" stroke-width="7" stroke-linecap="round"/>')
    pug += (f'<path d="M{pg_x-28:.0f},{pg_y-466:.0f} q28,-22 56,0" fill="none"'
            f' stroke="{K}" stroke-width="7"/>')
    for j in range(7):                  # солома из-под горшка
        pug += (f'<path d="M{pg_x-54+j*18:.0f},{pg_y-436:.0f} l{-8+j*3},34"'
                f' stroke="#d8b96a" stroke-width="6" stroke-linecap="round"/>')
    pug += '</g>'
    s += SL(Z_SRED, pug)
    vor_k = 7 * A.w(t, 1.7, .4)         # ворона на крестовине
    s += SL(Z_SRED, f'<g transform="translate({pg_x+180:.0f},{pg_y-430+vor_k*.4:.0f})">'
                    f'<ellipse cx="0" cy="0" rx="46" ry="30" fill="#1f2228" {o(5)}/>'
                    f'<circle cx="30" cy="-28" r="22" fill="#1f2228" {o(4)}/>'
                    f'<path d="M48,-30 l34,8 l-34,12 Z" fill="#4a4038" {o(3)}/>'
                    f'<path d="M-40,-10 q-34,-30 -8,-50" fill="none" stroke="#1f2228"'
                    f' stroke-width="12"/>'
                    f'<circle cx="34" cy="-32" r="4" fill="{SVET}"/></g>')
    sle = A.out(A.seg(t, 2.5, 1.2))
    shx = pg_x + sle * 240
    shy = pg_y - 570 - math.sin(sle * 3.14) * 180 + sle * 40
    s += SL(Z_SRED, f'<g transform="rotate({sle*260:.0f} {shx:.0f} {shy:.0f})">'
                    f'<path d="M{shx-70:.0f},{shy:.0f} q70,-96 140,0 q-70,30 -140,0 Z"'
                    f' fill="#53402e" {o(6)}/>'
                    f'<path d="M{shx-80:.0f},{shy-4:.0f} q80,40 160,0 l-8,34'
                    f' q-72,32 -144,0 Z" fill="#7a6246" {o(5)}/></g>')
    s += SL(Z_PERED, pleten(1180, 1080, 740, 220, 8))
    s += SL(Z_PERED, goloe_derevo(170, 1080, 560, t, 6229, 7, "#2a2b33"))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 6247, .46, .9))
    s += vinetka(.46)
    return s


# ── 63 ─────────────────────────────────────────────────────────────────────
def strizhka_posredi_kuhni(t):
    """Кухня, посреди неё на газетах табурет: мальчик, закутанный в простыню
    до ушей, вертит головой, пряди падают, чайник на плите пускает пар.

    Герой посажен НИЖЕ 420 px по вертикали: верхнюю треть кадра занимает
    плашка «Не вертись!», и прежде она ложилась мальчику на голову
    (осмотр 14.11)."""
    rnd = random.Random(6301)
    s = f'<rect width="{W}" height="{H}" fill="#6b6256"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#8a8072"/>')
    for r in range(8):                  # кафель по стене
        for c in range(14):
            s += SL(Z_DAL, f'<rect x="{c*140+6:.0f}" y="{r*86+6:.0f}" width="128"'
                           f' height="74" rx="6" fill="#9c9282" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect x="0" y="700" width="{W}" height="30" fill="#6b6256" {o(4)}/>')
    s += SL(Z_SRED, polovicy(930))
    s += SL(Z_SRED, tusklaya_lampochka(300, 90, t, 1.2, True))
    pl_x, pl_y = 1580, 940
    plt = (f'<rect x="{pl_x-280:.0f}" y="{pl_y-320:.0f}" width="560" height="320"'
           f' rx="14" fill="#cfd6dc" {o(9)}/>')
    plt += (f'<rect x="{pl_x-260:.0f}" y="{pl_y-360:.0f}" width="520" height="54"'
            f' rx="12" fill="#b9c2c8" {o(6)}/>')
    for i in range(4):
        plt += (f'<circle cx="{pl_x-170+i*110:.0f}" cy="{pl_y-150:.0f}" r="22"'
                f' fill="#8a929a" {o(4)}/>')
    for r in range(2):
        for c in range(2):
            plt += (f'<circle cx="{pl_x-150+c*280:.0f}" cy="{pl_y-250+r*70:.0f}"'
                    f' r="46" fill="#9aa3ab" {o(5)}/>')
    s += SL(Z_SRED, plt)
    s += SL(Z_SRED, ogon(pl_x - 150, pl_y - 330, t, .42, .2, 4))
    ch_x, ch_y = pl_x - 150, pl_y - 420
    s += SL(Z_SRED, f'<path d="M{ch_x-110:.0f},{ch_y:.0f} q-16,-120 110,-130'
                    f' q126,10 110,130 Z" fill="url(#zhel)" {o(8)}/>'
                    f'<path d="M{ch_x+100:.0f},{ch_y-80:.0f} q70,-10 56,-70"'
                    f' fill="none" stroke="url(#zhel)" stroke-width="20"'
                    f' stroke-linecap="round"/>'
                    f'<path d="M{ch_x-60:.0f},{ch_y-130:.0f} q60,-70 120,0"'
                    f' fill="none" stroke="{ZHELEZ}" stroke-width="14"/>'
                    f'<rect x="{ch_x-26:.0f}" y="{ch_y-156:.0f}" width="52"'
                    f' height="26" rx="8" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, par(ch_x + 150, ch_y - 150, t, 6, .6, 240, .6, 1.1))
    s += SL(Z_SRED, teplo(pl_x - 150, pl_y - 330, 420, 360, .34 + .1 * abs(A.w(t, 1.4))))
    for i in range(4):                  # газеты на полу
        s += SL(Z_SRED, _gazeta(740 + (i % 2) * 300, 1004 + (i // 2) * 48, 360, 250,
                                -12 + i * 9, 6311 + i))
    tx_, ty_ = 880, 1046
    tab = ten(tx_, ty_ + 14, 160, 22, .45)
    tab += (f'<rect x="{tx_-160:.0f}" y="{ty_-150:.0f}" width="320" height="50"'
            f' rx="14" fill="url(#derev)" {o(8)}/>')
    for dx in (-140, 96):
        tab += (f'<rect x="{tx_+dx:.0f}" y="{ty_-102:.0f}" width="44" height="106"'
                f' rx="12" fill="url(#derev)" {o(6)}/>')
    tab += (f'<rect x="{tx_-130:.0f}" y="{ty_-54:.0f}" width="260" height="20"'
            f' rx="8" fill="{DOSKA2}" {o(4)}/>')
    s += SL(Z_SRED, tab)
    sid = ty_ - 150                      # уровень сиденья табурета
    rost = 480
    vert = 16 * A.w(t, 1.3, .1)
    s += SL(Z_SRED, f'<g transform="rotate({vert:.1f} {tx_:.0f} {sid:.0f})">'
                    + figura(tx_, sid, rost, t, "#eef2f6", "#b9c2c8", False,
                             .2, False, 1.0) + '</g>')
    s += SL(Z_SRED, f'<g transform="rotate({vert:.1f} {tx_:.0f} {sid:.0f})">'
                    f'<path d="M{tx_-190:.0f},{sid:.0f} q190,-130 380,0'
                    f' q-42,42 -190,42 q-148,0 -190,-42 Z" fill="#eef2f6" {o(7)}/>'
                    f'<path d="M{tx_-158:.0f},{sid-32:.0f} q158,64 316,0"'
                    f' fill="none" stroke="#b9c2c8" stroke-width="9"/></g>')
    gy_ = sid - rost * .845
    for i in range(9):                  # пряди падают на газету
        p = ((t * .55) + i * .11) % 1.0
        s += SL(Z_SRED, f'<path d="M{tx_-120+i*32:.0f},'
                        f'{gy_+40+p*420:.0f} q14,{30+20*p:.0f} -8,{60+30*p:.0f}"'
                        f' fill="none" stroke="#6b4a2a" stroke-width="7"'
                        f' stroke-linecap="round" opacity="{1-p*.5:.2f}"/>')
    nozh_a = -30 + 24 * abs(A.w(t, .7, .2))
    nx_, ny_ = tx_ + 220, gy_ + 10
    s += SL(Z_SRED, f'<g transform="rotate({nozh_a:.0f} {nx_:.0f} {ny_:.0f})">'
                    f'<path d="M{nx_:.0f},{ny_:.0f} l-150,-40 l0,18 l150,36 Z"'
                    f' fill="url(#zhel)" {o(5)}/>'
                    f'<path d="M{nx_:.0f},{ny_+10:.0f} l-150,30 l0,18 l150,-28 Z"'
                    f' fill="url(#zhel)" {o(5)}/>'
                    f'<circle cx="{nx_+20:.0f}" cy="{ny_+8:.0f}" r="12"'
                    f' fill="{ZHELEZ}" {o(3)}/>'
                    f'<path d="M{nx_+30:.0f},{ny_-10:.0f} q60,-30 70,20" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="12"/>'
                    f'<path d="M{nx_+30:.0f},{ny_+26:.0f} q60,30 70,-16" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="12"/></g>')
    ruk, _ = rukav(tx_ + 350, gy_ + 70, 170, 190, t, "#5b2f3a", "#ffd98a", .3, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, figura(tx_ + 450, ty_ + 34, 620, t, "#5b2f3a", "#ffd98a", True, .4))
    for i, mx in enumerate((300, 480)):
        hih = 10 * abs(A.w(t, .9, i * .4))
        s += SL(Z_SRED, f'<g transform="translate(0,{-hih:.1f})">'
                        + figura(mx, 1046, 360 + i * 40, t,
                                 "#4a6a5a" if i else "#6b5a3c", "#ffd98a", False,
                                 i * .5, False, 1.0) + '</g>')
    s += ramka_pp("levo", "#1c1812", .4)
    s += SL(Z_PERED, _vedro(1830, 1070, 1.1, t, False, "#8a929a"))
    s += vinetka(.44)
    return s


# ── 64 ─────────────────────────────────────────────────────────────────────
def chelka_pered_zerkalom(t):
    """Зеркало в ванной на пол-кадра: женщина со спины и её отражение держит
    чёлку, в другой руке ножницы, на стекле листок с записью к мастеру."""
    rnd = random.Random(6421)
    s = f'<rect width="{W}" height="{H}" fill="#56606b"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#6e7a84"/>')
    for r in range(9):
        for c in range(16):
            s += SL(Z_DAL, f'<rect x="{c*122+5:.0f}" y="{r*122+5:.0f}" width="112"'
                           f' height="112" rx="8" fill="#7e8a94" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="0" y="880" width="{W}" height="200" fill="#5d6770" {o(6)}/>')
    rak = (f'<path d="M620,880 q340,-70 680,0 l-30,170 q-310,56 -620,0 Z"'
           f' fill="#eef2f6" {o(9)}/>')
    rak += (f'<ellipse cx="960" cy="900" rx="250" ry="60" fill="#dfe6ea" {o(6)}/>')
    rak += (f'<path d="M940,760 q0,-70 60,-70 q50,0 50,60" fill="none"'
            f' stroke="#b9c2c8" stroke-width="24" stroke-linecap="round"/>')
    rak += (f'<rect x="1030" y="740" width="60" height="26" rx="8" fill="#cfd6dc" {o(4)}/>')
    s += SL(Z_SRED, rak)
    zx, zy, zw, zh = 520, 120, 880, 660
    s += SL(Z_SRED, f'<rect x="{zx-34}" y="{zy-34}" width="{zw+68}" height="{zh+68}"'
                    f' rx="16" fill="#cfd6dc" {o(9)}/>')
    otr = (f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="#9fb6c6"/>')
    otr += (f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="#c9dbe6"'
            f' opacity=".5"/>')
    for r in range(6):                  # отражение кафеля
        otr += (f'<rect x="{zx}" y="{zy+r*110:.0f}" width="{zw}" height="100"'
                f' fill="#aec4d2" opacity=".45"/>')
    fx_ = zx + zw * .60
    otr += figura(fx_, zy + zh + 120, 660, t, "#4a3550", "#ffe6c8", False, .3, False, 1.0)
    chel = 30 * A.w(t, 1.6, .2)
    otr += (f'<path d="M{fx_-96:.0f},{zy+zh-540:.0f} q96,-70 192,0'
            f' q-20,80 -96,{90+chel*.4:.0f} q-76,{-10+chel*.3:.0f} -96,-90 Z"'
            f' fill="#6b4a2a" {o(6)}/>')
    for i in range(7):                  # пряди чёлки
        otr += (f'<path d="M{fx_-80+i*26:.0f},{zy+zh-580:.0f}'
                f' q{6+chel*.2:.1f},70 {-6:.0f},{110+chel*.3:.0f}" fill="none"'
                f' stroke="#8a6534" stroke-width="9" opacity=".9"/>')
    s += SL(Z_SRED, f'<clipPath id="zr64"><rect x="{zx}" y="{zy}" width="{zw}"'
                    f' height="{zh}"/></clipPath><g clip-path="url(#zr64)">{otr}</g>')
    nozh_y = zy + zh - 600 + 40 * A.w(t, 1.3, .1)
    pad = A.out(A.seg(t, 4.6, 1.0))
    nx_ = fx_ + 170
    ny_ = nozh_y + pad * 520
    s += SL(Z_SRED, f'<g transform="rotate({-16+pad*120:.0f} {nx_:.0f} {ny_:.0f})">'
                    f'<path d="M{nx_:.0f},{ny_:.0f} l-10,-120 l20,0 Z"'
                    f' fill="#cfd6dc" {o(4)}/>'
                    f'<path d="M{nx_+22:.0f},{ny_:.0f} l10,-120 l-20,0 Z"'
                    f' fill="#cfd6dc" {o(4)}/>'
                    f'<circle cx="{nx_-10:.0f}" cy="{ny_+30:.0f}" r="24" fill="none"'
                    f' stroke="{KRAS}" stroke-width="11"/>'
                    f'<circle cx="{nx_+34:.0f}" cy="{ny_+30:.0f}" r="24" fill="none"'
                    f' stroke="{KRAS}" stroke-width="11"/></g>')
    s += SL(Z_SRED, f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="none"'
                    f' {o(9)}/>')
    s += SL(Z_SRED, f'<path d="M{zx+60},{zy+50} l240,300" stroke="#ffffff"'
                    f' stroke-width="16" opacity=".22"/>')
    lx_, ly_ = zx + zw - 150, zy + 180
    zach = A.ease(A.seg(t, 2.0, 1.2))
    lst = (f'<g transform="rotate(-7 {lx_:.0f} {ly_:.0f})">'
           f'<rect x="{lx_-120:.0f}" y="{ly_-150:.0f}" width="240" height="300"'
           f' rx="10" fill="url(#list)" {o(6)}/>')
    for i in range(5):
        lst += (f'<path d="M{lx_-90:.0f},{ly_-100+i*50:.0f} q90,8 180,0"'
                f' fill="none" stroke="#7d756a" stroke-width="6" opacity=".8"/>')
    lst += (f'<line x1="{lx_-100:.0f}" y1="{ly_-70:.0f}" x2="{lx_+100*zach-20:.0f}"'
            f' y2="{ly_-40:.0f}" stroke="{KRAS}" stroke-width="11"'
            f' opacity="{zach:.2f}"/>')
    lst += (f'<path d="M{lx_-80:.0f},{ly_+70:.0f} q50,{-30*zach:.0f} 110,{10*zach:.0f}"'
            f' fill="none" stroke="#2f4a7a" stroke-width="8" opacity="{zach:.2f}"/>')
    lst += '</g>'
    s += SL(Z_SRED, lst)
    s += SL(Z_SRED, tusklaya_lampochka(zx + zw * .5, zy - 120, t, 1.0, True))
    s += SL(Z_SRED, teplo(zx + zw * .5, zy - 40, 640, 420, .3 + .1 * abs(A.w(t, 1.6))))
    s += SL(Z_PERED, figura(830, 1320, 780, t, "#2e2238", "#ffd98a", False, .3,
                            False, 1.0))
    pol = (f'<rect x="1500" y="520" width="360" height="26" rx="8"'
           f' fill="#cfd6dc" {o(6)}/>')
    s += SL(Z_SRED, pol)
    s += SL(Z_SRED, svecha(1600, 390, t, .3, 1.3, 120))
    s += SL(Z_SRED, teplo(1610, 360, 420, 380, .36 + .1 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, f'<path d="M1720,520 q-16,-120 36,-124 q54,4 38,124 Z"'
                    f' fill="url(#stekl)" opacity=".9" {o(5)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{1736+i*8:.0f}" y="{400-i*10:.0f}" width="10"'
                        f' height="90" rx="4" fill="#cfd6dc" {o(2)}/>')
    zak = A.ease(A.seg(t, 5.6, .9))
    s += SL(Z_SRED, f'<g transform="translate(0,{zak*40:.0f})">'
                    f'<path d="M200,700 q80,-40 160,0 q-80,30 -160,0 Z"'
                    f' fill="{KRAS}" {o(5)}/>'
                    f'<rect x="196" y="{698-10*(1-zak):.0f}" width="170" height="16"'
                    f' rx="7" fill="#8f2f33" {o(3)}/></g>')
    s += ramka_pp("levo", "#1a2028", .4)
    s += vinetka(.44)
    return s


# ── 65 ─────────────────────────────────────────────────────────────────────
def hozyain_obhodit_izbu_s_molotkom(t):
    """Белый дневной свет: хозяин в переднике с молотком и ящиком гвоздей
    обходит избу снаружи, подбивает ставню, в щель уходит пакля."""
    rnd = random.Random(6521)
    s = f'<rect width="{W}" height="{H}" fill="#b9c6cf"/>'
    s += nebo("den", t, False, 6529)
    s += oblaka(t, 190, 5, 6547, .5, "#f2f6fa", 11.0)
    s += ulica_dal(1300, 680, 620, t, False, 6551)
    s += SL(Z_DAL, gryaz_polosa(840, 200, "#6b5a46"))
    izb = brevna(60, 180, 1500, 700, 112)
    izb += (f'<path d="M20,190 L810,-110 L1600,190 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="1180" y="-150" width="110" height="220" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(1236, -140, t, 5, .2, 300, .3, "#dfe6ec", 1.0))
    for i, ox in enumerate((220, 1120)):
        s += SL(Z_SRED, okno_izby(ox, 420, 300, 230, t, None, .0, i == 1, True))
        s += SL(Z_SRED, f'<path d="M{ox-40:.0f},402 h380 l-30,-48 h-320 Z"'
                        f' fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, teplo(1270, 530, 320, 280, .3 + .1 * abs(A.w(t, 1.8))))
    stv_x, stv_y = 980, 410
    bit = abs(A.w(t, .9, .1))
    s += SL(Z_SRED, f'<g transform="rotate({-4+3*bit:.1f} {stv_x:.0f} {stv_y:.0f})">'
                    f'<rect x="{stv_x:.0f}" y="{stv_y:.0f}" width="190" height="300"'
                    f' rx="8" fill="url(#dosk)" {o(8)}/>'
                    + "".join(f'<rect x="{stv_x+10+j*60:.0f}" y="{stv_y+8:.0f}"'
                              f' width="50" height="284" rx="6" fill="url(#dosk)"'
                              f' {o(4)}/>' for j in range(3))
                    + f'<path d="M{stv_x+30:.0f},{stv_y+80:.0f} q65,-40 130,0"'
                    f' fill="none" stroke="{MED}" stroke-width="10"/></g>')
    mx_, my_ = stv_x + 250, stv_y + 110
    mol_a = -50 + 60 * bit
    s += SL(Z_SRED, f'<g transform="rotate({mol_a:.0f} {mx_:.0f} {my_+150:.0f})">'
                    f'<rect x="{mx_-12:.0f}" y="{my_:.0f}" width="26" height="190"'
                    f' rx="9" fill="url(#derev)" {o(5)}/>'
                    f'<rect x="{mx_-56:.0f}" y="{my_-54:.0f}" width="112" height="58"'
                    f' rx="10" fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{mx_+56:.0f},{my_-44:.0f} q40,20 0,40 Z"'
                    f' fill="{ZHELEZ}" {o(4)}/></g>')
    hx = 760
    s += SL(Z_SRED, figura(hx, 980, 600, t, "#4a3a2c", "#ffd0a0", False, .2, True,
                           1.0, False, 1.2, True, True))
    s += SL(Z_SRED, f'<path d="M{hx-96:.0f},{980-330:.0f} q96,-30 192,0 l-16,300'
                    f' q-80,26 -160,0 Z" fill="#c9bda4" opacity=".95" {o(6)}/>')
    ruk, _ = rukav(hx + 80, 640, 170, -22, t, "#4a3a2c", "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    yx_ = hx + 150
    s += SL(Z_SRED, f'<rect x="{yx_:.0f}" y="880" width="220" height="140" rx="10"'
                    f' fill="url(#derev)" {o(7)}/>'
                    f'<path d="M{yx_+20:.0f},880 q90,-60 180,0" fill="none"'
                    f' stroke="url(#derev)" stroke-width="14"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{yx_+30+i*26:.0f},890 l0,40 l6,16 l6,-16 l0,-40 Z"'
                        f' fill="{ZHELEZ}" {o(3)}/>')
    pak_x = 560
    for i in range(7):
        p = A.ease(A.seg(t, .4 + i * .18, .8))
        s += SL(Z_SRED, f'<path d="M{pak_x+i*8:.0f},{520-p*40:.0f}'
                        f' q{20-10*p:.0f},40 {-6:.0f},{70-20*p:.0f}" fill="none"'
                        f' stroke="#d8c8a4" stroke-width="{14-6*p:.0f}"'
                        f' stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M540,560 h120 l0,16 h-120 Z" fill="#3a2a1c"'
                    f' opacity=".9"/>')
    zx_ = 1620
    s += SL(Z_SRED, figura(zx_, 1030, 520, t, "#8f3a42", "#ffd0a0", True, .5, True))
    mel_y = 700 - abs(A.w(t, .8, .2)) * 90
    ruk2, (ax, ay) = rukav(zx_ - 90, 740, 140, 200, t, "#8f3a42", "#ffd0a0", .3, 5.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="30" ry="22"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{ax-24:.0f}" y="{mel_y:.0f}" width="48" height="60"'
                    f' rx="10" fill="#f6f2e6" {o(5)}/>')
    for i in range(4):
        s += SL(Z_SRED, kura(420 + i * 150, 1040 - (i % 2) * 20, t,
                             .85 + .1 * (i % 2), i * .25))
    s += SL(Z_PERED, pleten(-40, 1080, 420, 200, 6))
    s += SL(Z_PERED, _korzina(1850, 1080, 250, 190, t, 6553, False))
    s += vinetka(.4)
    return s


# ── 66 ─────────────────────────────────────────────────────────────────────
def mel_nad_oknom(t):
    """Хозяйка встаёт на лавку у окна и тянется куском мела к бревну над
    наличником: двумя взмахами ставит метку и сдувает крошки."""
    rnd = random.Random(6607)
    s = sumerki_fon(t, False)
    s += ulica_dal(1340, 700, 580, t, False, 6619)
    s += SL(Z_DAL, gryaz_polosa(830, 190, "#5a4c3a"))
    izb = brevna(0, 60, 1400, 820, 116)
    izb += (f'<path d="M-40,70 L680,-190 L1400,70 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="1000" y="-220" width="110" height="240" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(1056, -210, t, 5, .22, 320, .32, "#cdd7e4", 1.0))
    ox, oy, ow, oh = 420, 420, 520, 400
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#2a1d12"/>')
    za += teplo(ox + ow * .5, oy + oh * .6, 360, 300, .62)
    za += lampa(ox + ow * .34, oy + oh * .74, t, .62)
    za += figura(ox + ow * .74, oy + oh + 10, 330, t, "#4a3140", "#ffd98a", True, .4, True)
    s += SL(Z_SRED, f'<clipPath id="ok66"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok66)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .12, False, True))
    nal = (f'<path d="M{ox-80:.0f},{oy-40:.0f} h{ow+160:.0f} l-50,-72'
           f' h{-ow-60:.0f} Z" fill="url(#derev)" {o(8)}/>')
    for i in range(7):
        nal += (f'<path d="M{ox-50+i*96:.0f},{oy-46:.0f} l32,-24 l32,24 Z"'
                f' fill="{MED}" opacity=".9" {o(3)}/>')
    for sgn in (-1, 1):
        nal += (f'<rect x="{ox+(0 if sgn<0 else ow)-(54 if sgn<0 else 0):.0f}"'
                f' y="{oy-30:.0f}" width="54" height="{oh+60:.0f}" rx="8"'
                f' fill="url(#dosk)" {o(6)}/>')
    s += SL(Z_SRED, nal)
    s += SL(Z_SRED, teplo(ox + ow * .5, oy + oh * .5, 460, 400, .3 + .1 * abs(A.w(t, 1.7))))
    lv_x, lv_y = 640, 1010
    s += SL(Z_SRED, lavka(lv_x - 230, lv_y, 480))
    skrip = 1.4 * A.w(t, 1.1, .2)
    hx = lv_x
    s += SL(Z_SRED, f'<g transform="rotate({skrip:.2f} {hx:.0f} {lv_y:.0f})">'
                    + figura(hx, lv_y, 560, t, "#8f3a42", "#ffd98a", True, .2, True)
                    + '</g>')
    vzm = abs(A.w(t, .8, .1))
    ruk, (mx, my) = rukav(hx + 160, lv_y - 400, 230, -78 - 14 * vzm, t,
                          "#8f3a42", "#ffd98a", .2, 7.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="30" ry="24"'
                    f' fill="#e3c6a8" {o(4)}/>'
                    f'<rect x="{mx-18:.0f}" y="{my-56:.0f}" width="36" height="56"'
                    f' rx="10" fill="#f6f2e6" {o(5)}/>')
    metka = A.ease(A.seg(t, .5, 1.2))
    s += SL(Z_SRED, f'<g opacity="{metka:.2f}">'
                    f'<path d="M{ox+140:.0f},{oy-130:.0f} l70,90" stroke="#f6f2e6"'
                    f' stroke-width="16" stroke-linecap="round"/>'
                    f'<path d="M{ox+230:.0f},{oy-134:.0f} l-66,94" stroke="#f6f2e6"'
                    f' stroke-width="16" stroke-linecap="round"/></g>')
    s += SL(Z_SRED, teplo(ox + 190, oy - 90, 260, 200, .22 * metka))
    for i in range(10):                 # крошки мела сыплются
        p = ((t * .6) + i * .1) % 1.0
        s += SL(Z_SRED, f'<circle cx="{ox+150+i*12+16*A.w(t,2.4,i*.2):.0f}"'
                        f' cy="{oy-100+p*260:.0f}" r="{4+3*(1-p):.1f}"'
                        f' fill="#f6f2e6" opacity="{(1-p)*.8:.2f}"/>')
    sdu = A.seg(t, 1.8, .6)
    if sdu > .02 and sdu < .98:
        s += SL(Z_SRED, par(ox + 230, oy - 120, t, 4, .5, 150, 1.2, .8))
    dvx, dvy, dvw, dvh = 1120, 480, 260, 400
    s += SL(Z_SRED, dver(dvx, dvy, dvw, dvh, .0, "url(#derev)", True, False))
    s += SL(Z_SRED, podkova(dvx + dvw * .5, dvy - 60, .8, t))
    s += SL(Z_SRED, f'<path d="M{dvx-60:.0f},{dvy+dvh:.0f} h{dvw+120:.0f}'
                    f' l-30,60 h{-dvw-60:.0f} Z" fill="url(#dosk)" {o(7)}/>')
    s += SL(Z_SRED, kura(1500, 1000, t, .9, .2))
    s += SL(Z_SRED, kura(1640, 1030, t, .8, .6))
    s += SL(Z_PERED, goloe_derevo(1800, 1080, 620, t, 6637, 8, "#2a2b33"))
    s += ramka_pp("levo", "#1a140c", .4)
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 6653, .36, .8))
    s += vinetka(.44)
    return s


# ── 67 ─────────────────────────────────────────────────────────────────────
def serp_na_stavne(t):
    """Расписная ставня на пол-кадра: хозяин вешает на гвоздь большой
    блестящий серп, а на соседнюю ставню — кованую железку."""
    rnd = random.Random(6701)
    s = sumerki_fon(t, True)
    s += ulica_dal(1300, 720, 620, t, False, 6703)
    s += SL(Z_DAL, gryaz_polosa(850, 190, "#473c30"))
    s += SL(Z_DAL, brevna(0, 0, W, 900, 116))
    ox, oy, ow, oh = 620, 250, 440, 400
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#2a1d12"/>')
    sv_on = A.ease(A.seg(t, 2.6, 1.0))
    za += teplo(ox + ow * .5, oy + oh * .6, 340, 300, .7 * sv_on + .1)
    za += lampa(ox + ow * .4, oy + oh * .8, t, .56 * sv_on + .2)
    s += SL(Z_SRED, f'<clipPath id="ok67"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok67)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .15, False, True))
    for i, sgn in enumerate((-1, 1)):
        kach = 2.6 * sgn * A.w(t, 2.8, .2 + i * .3)
        sx_ = ox + (0 if sgn < 0 else ow)
        stv = f'<g transform="rotate({kach:.2f} {sx_:.0f} {oy-20:.0f})">'
        stv += (f'<rect x="{sx_-(300 if sgn<0 else 0):.0f}" y="{oy-30:.0f}"'
                f' width="300" height="{oh+60:.0f}" rx="10" fill="url(#dosk)" {o(9)}/>')
        for j in range(3):
            stv += (f'<rect x="{sx_-(290 if sgn<0 else -10)+j*94:.0f}"'
                    f' y="{oy-20:.0f}" width="84" height="{oh+40:.0f}" rx="8"'
                    f' fill="url(#dosk)" {o(5)}/>')
        bx_ = sx_ - (150 if sgn < 0 else -150)
        for j in range(3):              # роспись по ставне
            stv += (f'<circle cx="{bx_:.0f}" cy="{oy+80+j*140:.0f}" r="34"'
                    f' fill="{[KRAS, ZOL, ZEL2][j]}" opacity=".45" {o(3)}/>')
            stv += (f'<path d="M{bx_-70:.0f},{oy+80+j*140:.0f} q70,-50 140,0'
                    f' q-70,50 -140,0 Z" fill="none" stroke="{KREM}"'
                    f' stroke-width="8" opacity=".8"/>')
        stv += '</g>'
        s += SL(Z_SRED, stv)
    nx_, ny_ = 330, 360
    s += SL(Z_SRED, f'<circle cx="{nx_:.0f}" cy="{ny_:.0f}" r="16" fill="{ZHELEZ}" {o(5)}/>')
    ves = A.out(A.seg(t, .4, 1.2))
    kach2 = (1 - ves) * 0 + 7 * A.w(t, 1.9, .1) * ves
    serp = f'<g transform="rotate({kach2:.1f} {nx_:.0f} {ny_:.0f}) translate(0,{(1-ves)*-180:.0f})">'
    serp += (f'<path d="M{nx_:.0f},{ny_:.0f} q300,70 330,430 q-100,-300 -354,-350 Z"'
             f' fill="#dfe8ee" {o(9)}/>')
    serp += (f'<path d="M{nx_+20:.0f},{ny_+16:.0f} q270,80 300,380" fill="none"'
             f' stroke="#8a929a" stroke-width="8" opacity=".8"/>')
    serp += (f'<path d="M{nx_+10:.0f},{ny_+20:.0f} q200,70 230,300" fill="none"'
             f' stroke="#eef4f8" stroke-width="12"'
             f' opacity="{.4+.4*abs(A.w(t,2.2,.1)):.2f}"/>')
    for i in range(9):                  # зубцы серпа
        k = i / 8.0
        serp += (f'<path d="M{nx_+40+k*190:.0f},{ny_+40+k*230:.0f} l18,-14 l4,22 Z"'
                 f' fill="#eef4f8" opacity=".75"/>')
    serp += (f'<g transform="rotate(-24 {nx_:.0f} {ny_:.0f})">'
             f'<rect x="{nx_-170:.0f}" y="{ny_-34:.0f}" width="180" height="66"'
             f' rx="22" fill="url(#derev)" {o(8)}/>'
             f'<rect x="{nx_-178:.0f}" y="{ny_-40:.0f}" width="34" height="78"'
             f' rx="12" fill="{DOSKA2}" {o(6)}/></g>')
    serp += '</g>'
    s += SL(Z_SRED, serp)
    s += SL(Z_SRED, teplo(nx_ + 120, ny_ + 180, 360, 320, .22 + .1 * abs(A.w(t, 1.8))))
    zay = ((t * .4) % 1.0)              # зайчик от серпа бежит по двору
    s += SL(Z_SRED, f'<ellipse cx="{200+zay*1500:.0f}" cy="{960-abs(math.sin(zay*6))*60:.0f}"'
                    f' rx="60" ry="26" fill="{SVET}" opacity="{.5-.2*zay:.2f}"/>')
    pod = A.ease(A.seg(t, 1.6, 1.2))
    sx_ = 1520
    s += SL(Z_SRED, figura(sx_, 1040, 470, t, "#3c4656", "#cfe4f5", False, .6, True,
                           1.0, False, 1.2, False, True))
    ruk, (ax, ay) = rukav(sx_ - 90, 740, 190 - 40 * pod, 196 - 20 * pod, t,
                          "#3c4656", "#cfe4f5", .3, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<path d="M{ax-80:.0f},{ay-20:.0f} q40,-40 90,-10'
                    f' q50,30 10,80 q-50,30 -100,-70 Z" fill="{ZHELEZ}" {o(6)}/>')
    hx_ = 1140
    s += SL(Z_SRED, figura(hx_, 1020, 580, t, "#4a3a2c", "#ffd98a", False, .2, True,
                           1.0, True, 1.0, True, True))
    ruk2, _ = rukav(hx_ - 110, 660, 190, 184, t, "#4a3a2c", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, para_izo_rta(hx_ + 50, 560, t, .2, 1.1, .5))
    fnx, fny = 150, 180
    s += SL(Z_SRED, f'<path d="M{fnx-60:.0f},{fny:.0f} h120 l-14,-32 h-92 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-50:.0f},{fny:.0f} h100 l-12,118 h-76 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 108, t, .54, .3, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 70, 320, 290, .4 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_PERED, pleten(1240, 1080, 680, 220, 8))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 6709, .44, .9))
    s += vinetka(.46)
    return s


# ── 68 ─────────────────────────────────────────────────────────────────────
def ryabina_u_vhoda(t):
    """Крыльцо и распахнутая дверь сеней на пол-кадра: в дверном проёме
    рябина в гроздьях, девочка несёт кисти, на перилах сидит синица."""
    rnd = random.Random(6803)
    s = sumerki_fon(t, True)
    s += ulica_dal(1420, 740, 500, t, False, 6823)
    s += SL(Z_DAL, gryaz_polosa(860, 190, "#4a3e30"))
    izb = brevna(80, 60, 1500, 860, 116)
    izb += (f'<path d="M40,70 L820,-200 L1600,70 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="1220" y="-230" width="110" height="250" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(1276, -220, t, 5, .22, 320, .32, "#cdd7e4", 1.0))
    px, py, pw, ph_ = 500, 220, 800, 760
    put = kontur_proema(px, py, pw, ph_, "arka")
    vid = f'<clipPath id="st68"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#2a2016"/>'
    za = (f'<rect x="{px}" y="{py}" width="{pw}" height="{ph_}" fill="#3a4a3a"/>')
    za += (f'<rect x="{px}" y="{py+ph_*.62:.0f}" width="{pw}" height="{ph_*.38:.0f}"'
           f' fill="#4a4030"/>')
    za += goloe_derevo(px + pw * .5, py + ph_, 620, t, 6827, 9, "#4a3a2a")
    for i in range(9):                  # нарисованная рябина в проёме
        a = -2.4 + i * .5
        gx_ = px + pw * .5 + math.cos(a) * pw * .28
        gy_ = py + ph_ * .42 + math.sin(a) * ph_ * .22
        za += grozd_ryabiny(gx_, gy_, t, .95, 13, 6829 + i, i * .13)
        for j in range(4):              # листья
            za += (f'<ellipse cx="{gx_-60+j*34:.0f}" cy="{gy_+60+((j%2)*18):.0f}"'
                   f' rx="24" ry="11" fill="#7a6a2a"'
                   f' transform="rotate({-20+j*14} {gx_-60+j*34:.0f}'
                   f' {gy_+60+((j%2)*18):.0f})" {o(3)}/>')
    vid += f'<g clip-path="url(#st68)">{za}</g>'
    vid += mesto_stoka(px, py, pw, ph_, "arka")
    ob = (f'<path d="{put}" fill="none" stroke="url(#derev)" stroke-width="86"/>')
    ob += (f'<path d="{put}" fill="none" {o(9)}/>')
    ob += (f'<path d="M{px-120:.0f},{py+ph_*.38:.0f} h{pw+240:.0f}" stroke="url(#dosk)"'
           f' stroke-width="0" fill="none"/>')
    for sgn in (-1, 1):                 # наличники по бокам проёма
        bx_ = px + (0 if sgn < 0 else pw)
        ob += (f'<rect x="{bx_-(96 if sgn<0 else 0):.0f}" y="{py+pw*.5-40:.0f}"'
               f' width="96" height="{ph_-pw*.5+40:.0f}" rx="10" fill="url(#dosk)"'
               f' {o(8)}/>')
        for j in range(4):
            ob += (f'<path d="M{bx_-(76 if sgn<0 else -20):.0f},'
                   f'{py+pw*.5+40+j*130:.0f} q28,46 0,92" fill="none"'
                   f' stroke="#5a3a22" stroke-width="9" opacity=".7"/>')
    ob += (f'<path d="M{px-150:.0f},{py-30:.0f} q{pw*.5+150:.0f},-180'
           f' {pw+300:.0f},0 l-60,-70 q{-pw*.5-120:.0f},-150 {-pw-180:.0f},0 Z"'
           f' fill="{DOSKA2}" {o(8)}/>')
    for i in range(9):
        ob += (f'<path d="M{px-110+i*(pw+220)/8:.0f},{py-70:.0f} l30,-26 l30,26 Z"'
               f' fill="{MED}" opacity=".9" {o(3)}/>')
    vid += ob
    s += SL(Z_SRED, vid)
    s += SL(Z_SRED, teplo(px + pw * .5, py + ph_ + 80, 560, 240, .26))
    kr = (f'<path d="M{px-180:.0f},{py+ph_:.0f} h{pw+360:.0f} l60,70'
          f' h{-pw-480:.0f} Z" fill="url(#dosk)" {o(9)}/>')
    for i in range(3):
        kr += (f'<rect x="{px-160+i*20:.0f}" y="{py+ph_+70+i*42:.0f}"'
               f' width="{pw+320-i*40:.0f}" height="38" rx="8" fill="url(#dosk)" {o(5)}/>')
    s += SL(Z_SRED, kr)
    stx = px + pw + 190
    s += SL(Z_SRED, f'<rect x="{stx-28:.0f}" y="{py-130:.0f}" width="56"'
                    f' height="{ph_+280:.0f}" rx="12" fill="url(#derev)" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="{stx-130:.0f}" y="{py+ph_-120:.0f}" width="260"'
                    f' height="26" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, ptica(stx + 90, py + ph_ - 130, t, 1.2, KRAS, .2, "#5b6a78"))
    for i in range(3):                  # гроздья на столбе, качаются на лыке
        kach = 4.0 * A.w(t, 2.4, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {stx:.0f} {py-60+i*40:.0f})">'
                        f'<path d="M{stx:.0f},{py-60+i*40:.0f} q20,70 6,130"'
                        f' fill="none" stroke="#b9a884" stroke-width="9"/>'
                        + grozd_ryabiny(stx + 14, py + 120 + i * 60, t, .9, 12,
                                        6841 + i, i * .2) + '</g>')
    lyk = A.ease(A.seg(t, 1.2, 1.2))
    s += SL(Z_SRED, f'<path d="M{stx-50:.0f},{py-40:.0f} q50,{-30+20*lyk:.0f}'
                    f' 100,0 q{-40*lyk:.0f},30 {-100*lyk:.0f},10" fill="none"'
                    f' stroke="#d8c8a4" stroke-width="11" stroke-linecap="round"/>')
    dx_ = 300
    s += SL(Z_SRED, figura(dx_, 1050, 430, t, "#5b2f3a", "#ffd98a", True, .4, True))
    ruk, (ax, ay) = rukav(dx_ + 90, 800, 150, -34 + 14 * A.w(t, 1.3), t,
                          "#5b2f3a", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, grozd_ryabiny(ax + 30, ay + 40, t, 1.1, 15, 6857, .1))
    s += SL(Z_SRED, para_izo_rta(dx_ + 40, 720, t, .3, 1.0, .5))
    fnx, fny = 1700, 330
    s += SL(Z_SRED, f'<rect x="{fnx-16:.0f}" y="60" width="32" height="600"'
                    f' fill="url(#derev)" {o(7)}/>'
                    f'<path d="M{fnx-62:.0f},{fny:.0f} h124 l-14,-34 h-96 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-52:.0f},{fny:.0f} h104 l-12,124 h-80 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 112, t, .58, .2, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 70, 340, 300, .42 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_PERED, _korzina(160, 1080, 240, 190, t, 6863, False))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 6869, .4, .85))
    s += vinetka(.46)
    return s


# ═══ из chast3.py ═══
def _rozhica(x, y, r_, t, ph=.0, hitraya=True, col="#2b1708"):
    """Рожица рисованного героя (огонёк, Ветер, Вихрь): глаза с бликом,
    брови домиком и косая ухмылка. Букв нет — только мимика."""
    kos = r_ * .22 * A.w(t, 1.3, ph)
    mig = A.blink(t, 3.4, ph)
    s = ""
    for i in (-1, 1):
        ex = x + i * r_ * .42
        s += (f'<ellipse cx="{ex:.0f}" cy="{y:.0f}" rx="{r_*.26:.0f}"'
              f' ry="{(r_*.07 if mig else r_*.30):.1f}" fill="#fff6e2"'
              f' stroke="{col}" stroke-width="{max(2, r_*.05):.1f}"/>')
        if not mig:
            s += (f'<circle cx="{ex+kos:.0f}" cy="{y+r_*.04:.0f}" r="{r_*.12:.0f}"'
                  f' fill="{col}"/>')
            s += (f'<circle cx="{ex+kos-r_*.05:.0f}" cy="{y-r_*.07:.0f}"'
                  f' r="{r_*.045:.0f}" fill="#ffffff" opacity=".9"/>')
        s += (f'<path d="M{ex-r_*.30:.0f},{y-r_*.44+(0 if hitraya else r_*.1)*i:.0f}'
              f' q{r_*.30:.0f},{-r_*.22 if hitraya else -r_*.05:.0f} {r_*.60:.0f},'
              f'{r_*.06 if hitraya else 0:.0f}" fill="none" stroke="{col}"'
              f' stroke-width="{max(3, r_*.08):.1f}" stroke-linecap="round"/>')
    if hitraya:
        s += (f'<path d="M{x-r_*.34:.0f},{y+r_*.44:.0f} q{r_*.40:.0f},{r_*.34:.0f}'
              f' {r_*.74:.0f},{-r_*.12:.0f}" fill="none" stroke="{col}"'
              f' stroke-width="{max(3, r_*.09):.1f}" stroke-linecap="round"/>')
    else:
        s += (f'<ellipse cx="{x:.0f}" cy="{y+r_*.50:.0f}" rx="{r_*.24:.0f}"'
              f' ry="{r_*.16+r_*.06*A.w(t,.9,ph):.1f}" fill="{col}"/>')
    return s


def _valenok(x, y, s_=1.0, t=0.0, ph=.0, galosha=True, col="#c4b091", naklon=0.0):
    """Валенок ПРОСТОЙ И УЗНАВАЕМОЙ геометрией: толстое прямое голенище и
    отдельная ступня с тупым носком, выступающая вперёд. Сложный контур
    читался корзиной — поправлено по осмотру."""
    hh, w_ = 200 * s_, 92 * s_
    ug = naklon + 1.2 * A.w(t, 2.8, ph)
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    s += ten(x + w_ * .3, y + 8 * s_, w_ * .9, 12 * s_, .42)
    # ступня: длинный блок с круглым носком
    s += (f'<path d="M{x-w_*.42:.0f},{y-hh*.40:.0f} h{w_*.70:.0f}'
          f' q{w_*.56:.0f},{hh*.04:.0f} {w_*.60:.0f},{hh*.22:.0f}'
          f' q{w_*.04:.0f},{hh*.16:.0f} {-w_*.22:.0f},{hh*.17:.0f}'
          f' h{-w_*1.08:.0f} Z" fill="{col}" {o(max(4, 7*s_))}/>')
    # голенище: прямой толстый рукав с валиком сверху
    s += (f'<rect x="{x-w_*.46:.0f}" y="{y-hh:.0f}" width="{w_*.92:.0f}"'
          f' height="{hh*.64:.0f}" rx="{w_*.14:.0f}" fill="{col}"'
          f' {o(max(4, 7*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*.46:.0f}"'
          f' ry="{14*s_:.0f}" fill="#9c8c72" {o(max(3, 5*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh+6*s_:.0f}" rx="{w_*.34:.0f}"'
          f' ry="{8*s_:.0f}" fill="#7d7160" opacity=".8"/>')
    for i in range(4):                   # войлок: короткие вертикальные штрихи
        s += (f'<path d="M{x-w_*.28+i*w_*.19:.0f},{y-hh*.88:.0f}'
              f' q{4*s_:.0f},{hh*.14:.0f} {1*s_:.0f},{hh*.28:.0f}" fill="none"'
              f' stroke="#ded0b4" stroke-width="{max(3, 7*s_):.0f}"'
              f' opacity=".55"/>')
    s += (f'<path d="M{x-w_*.44:.0f},{y-hh*.44:.0f} h{w_*.88:.0f}"'
          f' stroke="#9c8c72" stroke-width="{max(3, 7*s_):.0f}" opacity=".7"/>')
    if galosha:                          # галоша: тёмная глянцевая опушка
        s += (f'<path d="M{x-w_*.50:.0f},{y-hh*.26:.0f}'
              f' q{-w_*.04:.0f},{hh*.30:.0f} {w_*.34:.0f},{hh*.30:.0f}'
              f' h{w_*.62:.0f} q{w_*.30:.0f},{-hh*.02:.0f}'
              f' {w_*.12:.0f},{-hh*.20:.0f} q{-w_*.28:.0f},{-hh*.14:.0f}'
              f' {-w_*1.08:.0f},{-hh*.08:.0f} Z" fill="#26282b"'
              f' {o(max(3, 5*s_))}/>')
        s += (f'<path d="M{x-w_*.50:.0f},{y-hh*.26:.0f} q{w_*.50:.0f},{hh*.06:.0f}'
              f' {w_*1.10:.0f},{hh*.02:.0f}" fill="none" stroke="#dfe8ef"'
              f' stroke-width="{max(3, 7*s_):.0f}" opacity=".85"/>')
        s += (f'<path d="M{x-w_*.36:.0f},{y-hh*.16:.0f} q{w_*.46:.0f},{hh*.10:.0f}'
              f' {w_*.96:.0f},{hh*.01:.0f}" fill="none" stroke="#9fb4c2"'
              f' stroke-width="{max(3, 6*s_):.0f}"'
              f' opacity="{.4+.3*abs(A.w(t,2.4,ph)):.2f}"/>')
    return s + '</g>'


def _varezhka(x, y, s_=1.0, t=0.0, ph=.0, col=TKAN, visit=True):
    """Рукавица: ладонь овалом, отставленный большой палец, манжет полосками."""
    w_, hh = 70 * s_, 112 * s_
    ug = (9 if visit else 0) * A.w(t, 2.2, ph)
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x-w_*.44:.0f},{y:.0f} q{-w_*.14:.0f},{hh*.52:.0f} {w_*.10:.0f},{hh*.70:.0f}'
          f' q{w_*.38:.0f},{hh*.16:.0f} {w_*.72:.0f},0 q{w_*.22:.0f},{-hh*.22:.0f}'
          f' {w_*.04:.0f},{-hh*.70:.0f} Z" fill="{col}" {o(max(3, 5*s_))}/>')
    s += (f'<path d="M{x-w_*.40:.0f},{y+hh*.22:.0f} q{-w_*.40:.0f},{hh*.06:.0f}'
          f' {-w_*.30:.0f},{hh*.34:.0f} q{w_*.20:.0f},{hh*.10:.0f} {w_*.36:.0f},{-hh*.14:.0f} Z"'
          f' fill="{col}" {o(max(3, 5*s_))}/>')
    s += (f'<rect x="{x-w_*.46:.0f}" y="{y-hh*.16:.0f}" width="{w_*.92:.0f}"'
          f' height="{hh*.20:.0f}" rx="{8*s_:.0f}" fill="{KREM}" {o(max(2, 4*s_))}/>')
    for i in range(3):
        s += (f'<line x1="{x-w_*.42:.0f}" y1="{y-hh*.10+i*hh*.055:.0f}"'
              f' x2="{x+w_*.42:.0f}" y2="{y-hh*.10+i*hh*.055:.0f}" stroke="#c2ab86"'
              f' stroke-width="{max(2, 4*s_):.0f}" opacity=".8"/>')
    s += (f'<path d="M{x-w_*.20:.0f},{y+hh*.30:.0f} q{w_*.20:.0f},{hh*.14:.0f}'
          f' {w_*.40:.0f},0" fill="none" stroke="#f3e0c4"'
          f' stroke-width="{max(2, 5*s_):.0f}" opacity=".5"/>')
    return s + '</g>'


def _shapka_meh(x, y, s_=1.0, t=0.0, ph=.0, razdvinut=0.0):
    """Шапка-ушанка: меховой купол, толстый светлый околыш и два широких уха,
    прижатых к бокам (не палки в стороны — поправлено по осмотру)."""
    w_, hh = 150 * s_, 86 * s_
    s = ten(x, y + 16 * s_, w_ * .62, 14 * s_, .42)
    for i in (-1, 1):                    # уши-лопасти прижаты к бокам купола
        ug = i * (4 + 3 * A.w(t, 2.6, ph + (0 if i < 0 else .3)))
        s += (f'<g transform="rotate({ug:.1f} {x+i*w_*.40:.0f} {y-hh*.30:.0f})">'
              f'<path d="M{x+i*w_*.30:.0f},{y-hh*.56:.0f}'
              f' q{i*w_*.30:.0f},{hh*.06:.0f} {i*w_*.32:.0f},{hh*.52:.0f}'
              f' q{i*w_*.01:.0f},{hh*.52:.0f} {-i*w_*.14:.0f},{hh*.54:.0f}'
              f' q{-i*w_*.18:.0f},{-hh*.14:.0f} {-i*w_*.18:.0f},{-hh*1.06:.0f} Z"'
              f' fill="#c2a078" {o(max(3, 5*s_))}/>')
        for j in range(4):
            s += (f'<path d="M{x+i*w_*(.26+j*.015):.0f},{y-hh*.16+j*hh*.26:.0f}'
                  f' l{i*16*s_:.0f},{4*s_:.0f}" stroke="#e0c49a"'
                  f' stroke-width="{max(3, 7*s_):.0f}" stroke-linecap="round"'
                  f' opacity=".85"/>')
        s += '</g>'
    s += (f'<path d="M{x-w_*.52:.0f},{y-hh*.20:.0f}'
          f' q{w_*.02:.0f},{-hh*1.16:.0f} {w_*.52:.0f},{-hh*1.16:.0f}'
          f' q{w_*.50:.0f},0 {w_*.52:.0f},{hh*1.16:.0f} Z" fill="#6b5236"'
          f' {o(max(4, 6*s_))}/>')
    for i in range(11):                  # мех на куполе
        a = -3.0 + i * .30
        s += (f'<path d="M{x+math.cos(a)*w_*.47:.0f},'
              f'{y-hh*.20+math.sin(a)*hh*1.02:.0f}'
              f' l{math.cos(a)*18*s_:.0f},{math.sin(a)*18*s_:.0f}"'
              f' stroke="#8f6f48" stroke-width="{max(3, 9*s_):.0f}"'
              f' stroke-linecap="round" opacity=".9"/>')
    if razdvinut > .02:                  # мех раздвинут пробором на просвет
        s += (f'<path d="M{x-w_*.07:.0f},{y-hh*.26:.0f}'
              f' q{w_*.04:.0f},{-hh*.54:.0f} {w_*.01:.0f},{-hh*1.02:.0f}'
              f' l{w_*.18*razdvinut:.0f},0 q{w_*.03:.0f},{hh*.48:.0f}'
              f' {w_*.04:.0f},{hh*1.02:.0f} Z" fill="#fff0cc"'
              f' opacity="{.92*razdvinut:.2f}" {o(max(2, 3*s_))}/>')
    s += (f'<path d="M{x-w_*.58:.0f},{y-hh*.26:.0f}'
          f' q{w_*.58:.0f},{hh*.24:.0f} {w_*1.16:.0f},0'
          f' l0,{hh*.48:.0f} q{-w_*.58:.0f},{hh*.28:.0f} {-w_*1.16:.0f},0 Z"'
          f' fill="#d8b98a" {o(max(4, 6*s_))}/>')
    for i in range(9):
        xx = x - w_ * .50 + i * w_ * .125
        s += (f'<path d="M{xx:.0f},{y-hh*.20:.0f} q{6*s_:.0f},{hh*.28:.0f}'
              f' {-2*s_:.0f},{hh*.48:.0f}" fill="none" stroke="#f0d9b4"'
              f' stroke-width="{max(3, 8*s_):.0f}" opacity=".75"/>')
    s += (f'<ellipse cx="{x-w_*.20:.0f}" cy="{y-hh*.94:.0f}" rx="{w_*.16:.0f}"'
          f' ry="{hh*.14:.0f}" fill="#b08f62" opacity=".45"/>')
    return s


def _tulup_vis(x, y, w_, h_, t, ph=.0, udar=0.0):
    """Овчинный тулуп на гвозде или верёвке: ШИРОКИЙ меховой воротник, светлая
    опушка по борту, обшлагам и подолу, рукава висят по бокам. Без опушки он
    читался мешком — поправлено по осмотру."""
    ug = 2.4 * A.w(t, 2.2, ph) + 7 * udar
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    for i in (-1, 1):                    # рукава СНАЧАЛА — они за полой
        ru = i * (3.0 + 2.4 * A.w(t, 1.8, ph + .2)) + 9 * udar * i
        s += (f'<g transform="rotate({ru:.2f} {x+i*w_*.46:.0f} {y+h_*.16:.0f})">'
              f'<path d="M{x+i*w_*.40:.0f},{y+h_*.12:.0f}'
              f' q{i*w_*.30:.0f},{h_*.06:.0f} {i*w_*.30:.0f},{h_*.50:.0f}'
              f' q{-i*w_*.14:.0f},{h_*.10:.0f} {-i*w_*.30:.0f},{-h_*.04:.0f} Z"'
              f' fill="#b4915f" {o(7)}/>'
              f'<path d="M{x+i*w_*.42:.0f},{y+h_*.60:.0f}'
              f' q{i*w_*.14:.0f},{h_*.08:.0f} {i*w_*.26:.0f},{-h_*.02:.0f}'
              f' l0,{-h_*.08:.0f} q{-i*w_*.12:.0f},{h_*.06:.0f}'
              f' {-i*w_*.26:.0f},{-h_*.01:.0f} Z" fill="#f2ead6" {o(4)}/></g>')
    # пола тулупа
    s += (f'<path d="M{x-w_*.5:.0f},{y+h_*.14:.0f} q{w_*.16:.0f},{-h_*.16:.0f}'
          f' {w_*.5:.0f},{-h_*.14:.0f} q{w_*.34:.0f},{-h_*.02:.0f} {w_*.5:.0f},{h_*.14:.0f}'
          f' L{x+w_*.62:.0f},{y+h_:.0f} q{-w_*.62:.0f},{h_*.07:.0f} {-w_*1.24:.0f},0 Z"'
          f' fill="#b4915f" {o(9)}/>')
    # борт с опушкой наискось — главный признак тулупа
    s += (f'<path d="M{x+w_*.04:.0f},{y+h_*.10:.0f} L{x+w_*.18:.0f},{y+h_*.98:.0f}'
          f' l{-w_*.16:.0f},0 L{x-w_*.10:.0f},{y+h_*.12:.0f} Z" fill="#f2ead6"'
          f' {o(5)}/>')
    for i in range(4):                   # деревянные пуговицы по борту
        s += (f'<circle cx="{x+w_*(.07+i*.03):.0f}" cy="{y+h_*(.26+i*.19):.0f}"'
              f' r="{h_*.022:.0f}" fill="#5e4428" {o(3)}/>')
    # меховой воротник шалькой
    s += (f'<path d="M{x-w_*.34:.0f},{y+h_*.04:.0f} q{w_*.34:.0f},{-h_*.14:.0f}'
          f' {w_*.68:.0f},0 q{-w_*.06:.0f},{h_*.20:.0f} {-w_*.22:.0f},{h_*.22:.0f}'
          f' q{-w_*.14:.0f},{-h_*.12:.0f} {-w_*.24:.0f},{-h_*.02:.0f}'
          f' q{-w_*.12:.0f},{-h_*.10:.0f} {-w_*.22:.0f},{-h_*.20:.0f} Z"'
          f' fill="#f6efdd" {o(6)}/>')
    for i in range(7):                   # клочья меха по воротнику
        s += (f'<path d="M{x-w_*.28+i*w_*.09:.0f},{y+h_*.02:.0f}'
              f' l{4:.0f},{h_*.05:.0f}" stroke="#d8cbb0" stroke-width="7"'
              f' opacity=".8"/>')
    # опушка подола
    s += (f'<path d="M{x-w_*.58:.0f},{y+h_*.90:.0f} q{w_*.58:.0f},{h_*.12:.0f}'
          f' {w_*1.18:.0f},0 l0,{h_*.08:.0f} q{-w_*.60:.0f},{h_*.08:.0f}'
          f' {-w_*1.18:.0f},0 Z" fill="#f2ead6" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.02:.0f}" rx="{w_*.05:.0f}"'
          f' ry="{h_*.016:.0f}" fill="#8d949b" {o(3)}/>')
    return s + '</g>'


def _batareya(x, y, w_, h_, t, n=9):
    """Чугунная батарея: гармошка секций, подводка с вентилем, тёплый воздух."""
    s = (f'<rect x="{x-16:.0f}" y="{y:.0f}" width="{w_+32:.0f}" height="{h_:.0f}"'
         f' rx="14" fill="#b9bdc2" opacity=".35"/>')
    for i in range(n):
        sx = x + i * (w_ / n)
        s += (f'<rect x="{sx:.0f}" y="{y:.0f}" width="{w_/n*.72:.0f}" height="{h_:.0f}"'
              f' rx="{w_/n*.34:.0f}" fill="url(#zhel)" {o(5)}/>')
        s += (f'<rect x="{sx+w_/n*.16:.0f}" y="{y+10:.0f}" width="{w_/n*.16:.0f}"'
              f' height="{h_-20:.0f}" rx="8" fill="#cfd6dc" opacity=".45"/>')
    s += (f'<rect x="{x-20:.0f}" y="{y+h_*.16:.0f}" width="{w_+40:.0f}" height="16"'
          f' rx="8" fill="#8d949b" {o(4)}/>')
    s += (f'<rect x="{x-20:.0f}" y="{y+h_*.74:.0f}" width="{w_+40:.0f}" height="16"'
          f' rx="8" fill="#8d949b" {o(4)}/>')
    s += (f'<rect x="{x+w_+20:.0f}" y="{y-40:.0f}" width="20" height="{h_+80:.0f}"'
          f' rx="10" fill="#9aa1a8" {o(4)}/>')
    s += (f'<circle cx="{x+w_+30:.0f}" cy="{y-46:.0f}" r="26" fill="url(#zhel)" {o(5)}/>')
    s += (f'<circle cx="{x+w_+30:.0f}" cy="{y-46:.0f}" r="10" fill="#6e757c"/>')
    for i in range(4):                   # тёплый воздух дрожит над секциями
        k = ((t * .4) + i * .25) % 1.0
        s += (f'<path d="M{x+w_*(.12+i*.24):.0f},{y-10-k*110:.0f} q22,-26 0,-52"'
              f' fill="none" stroke="#ffd9a0" stroke-width="7"'
              f' opacity="{.34*(1-k):.2f}"/>')
    return s


def _chaynik(x, y, s_=1.0, t=0.0, svistok=True, col="url(#zhel)"):
    """Пузатый чайник: округлый бок, гнутый носик, дуга ручки, шишечка."""
    w_, hh = 150 * s_, 130 * s_
    s = ten(x, y + 10 * s_, w_ * .72, 14 * s_, .45)
    s += (f'<path d="M{x-w_*.46:.0f},{y:.0f} q{-w_*.22:.0f},{-hh*.52:.0f} {w_*.06:.0f},{-hh*.84:.0f}'
          f' q{w_*.40:.0f},{-hh*.22:.0f} {w_*.80:.0f},0 q{w_*.28:.0f},{hh*.32:.0f}'
          f' {w_*.06:.0f},{hh*.84:.0f} Z" fill="{col}" {o(max(4, 7*s_))}/>')
    s += (f'<path d="M{x-w_*.30:.0f},{y-hh*.60:.0f} q{w_*.10:.0f},{hh*.30:.0f}'
          f' {-w_*.02:.0f},{hh*.52:.0f}" fill="none" stroke="#e8f1f8"'
          f' stroke-width="{max(4, 12*s_):.0f}"'
          f' opacity="{.22+.2*abs(A.w(t,2.8)):.2f}"/>')
    s += (f'<path d="M{x+w_*.40:.0f},{y-hh*.56:.0f} q{w_*.44:.0f},{-hh*.06:.0f}'
          f' {w_*.46:.0f},{-hh*.40:.0f} l{w_*.14:.0f},{hh*.10:.0f}'
          f' q{-w_*.08:.0f},{hh*.44:.0f} {-w_*.52:.0f},{hh*.44:.0f} Z"'
          f' fill="{col}" {o(max(3, 6*s_))}/>')
    s += (f'<path d="M{x-w_*.22:.0f},{y-hh*.88:.0f} q{w_*.22:.0f},{-hh*.56:.0f}'
          f' {w_*.44:.0f},0" fill="none" stroke="#4a4f55"'
          f' stroke-width="{max(5, 16*s_):.0f}" stroke-linecap="round"/>')
    s += (f'<ellipse cx="{x+w_*.04:.0f}" cy="{y-hh*.86:.0f}" rx="{w_*.30:.0f}"'
          f' ry="{hh*.10:.0f}" fill="#8d949b" {o(max(3, 5*s_))}/>')
    if svistok:
        s += (f'<ellipse cx="{x+w_*.86:.0f}" cy="{y-hh*.96:.0f}" rx="{15*s_:.0f}"'
              f' ry="{18*s_:.0f}" fill="{KRAS}" {o(max(2, 4*s_))}/>')
    s += (f'<circle cx="{x+w_*.04:.0f}" cy="{y-hh*.98:.0f}" r="{13*s_:.0f}"'
          f' fill="#2f3337" {o(max(2, 4*s_))}/>')
    return s


def _chashka(x, y, s_=1.0, t=0.0, ph=.0, col=KREM, blyudce=True):
    """Чашка с блюдцем: бочок, ушко, чай внутри, пар над краем."""
    w_, hh = 62 * s_, 58 * s_
    s = ""
    if blyudce:
        s += (f'<ellipse cx="{x:.0f}" cy="{y+6*s_:.0f}" rx="{w_*.96:.0f}"'
              f' ry="{13*s_:.0f}" fill="{col}" {o(max(2, 4*s_))}/>')
    s += (f'<path d="M{x-w_*.5:.0f},{y-hh:.0f} h{w_:.0f} l{-w_*.09:.0f},{hh:.0f}'
          f' q{-w_*.32:.0f},{12*s_:.0f} {-w_*.82:.0f},0 Z" fill="{col}"'
          f' {o(max(2, 5*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*.5:.0f}" ry="{10*s_:.0f}"'
          f' fill="#6b4a2a" {o(max(2, 3*s_))}/>')
    s += (f'<ellipse cx="{x-w_*.14:.0f}" cy="{y-hh:.0f}" rx="{w_*.16:.0f}"'
          f' ry="{4*s_:.0f}" fill="#d8b98a"'
          f' opacity="{.35+.3*abs(A.w(t,1.7,ph)):.2f}"/>')
    s += (f'<path d="M{x+w_*.44:.0f},{y-hh*.78:.0f} q{w_*.40:.0f},{hh*.22:.0f}'
          f' {-w_*.06:.0f},{hh*.52:.0f}" fill="none" stroke="{col}"'
          f' stroke-width="{max(3, 9*s_):.0f}"/>')
    s += (f'<path d="M{x+w_*.44:.0f},{y-hh*.78:.0f} q{w_*.40:.0f},{hh*.22:.0f}'
          f' {-w_*.06:.0f},{hh*.52:.0f}" fill="none" stroke="{K}" stroke-width="3"/>')
    return s


def _vaza(x, y, s_=1.0, t=0.0, voda=True):
    """Стеклянная ваза: ровное цилиндрическое тулово с лёгкой талией и широким
    устьем, видно насквозь. Пузатая колба с синей заливкой читалась ретортой."""
    w_, hh = 118 * s_, 300 * s_
    s = ten(x, y + 8 * s_, w_ * .58, 13 * s_, .45)
    s += (f'<path d="M{x-w_*.44:.0f},{y-hh:.0f}'
          f' q{-w_*.04:.0f},{hh*.34:.0f} {w_*.02:.0f},{hh*.52:.0f}'
          f' q{w_*.04:.0f},{hh*.36:.0f} {w_*.40:.0f},{hh*.48:.0f}'
          f' q{w_*.40:.0f},{-hh*.12:.0f} {w_*.44:.0f},{-hh*.48:.0f}'
          f' q{w_*.06:.0f},{-hh*.18:.0f} {w_*.02:.0f},{-hh*.52:.0f} Z"'
          f' fill="url(#stekl)" opacity=".62" {o(max(4, 6*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*.44:.0f}"'
          f' ry="{13*s_:.0f}" fill="#dff0fa" {o(max(3, 5*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh+5*s_:.0f}" rx="{w_*.34:.0f}"'
          f' ry="{9*s_:.0f}" fill="#8fb8ce" opacity=".55"/>')
    if voda:
        s += (f'<path d="M{x-w_*.42:.0f},{y-hh*.42:.0f}'
              f' q{w_*.42:.0f},{hh*.05:.0f} {w_*.84:.0f},0'
              f' q{-w_*.02:.0f},{hh*.30:.0f} {-w_*.42:.0f},{hh*.34:.0f}'
              f' q{-w_*.40:.0f},{-hh*.04:.0f} {-w_*.42:.0f},{-hh*.34:.0f} Z"'
              f' fill="#8fc4d2" opacity=".40"/>')
        s += (f'<path d="M{x-w_*.41:.0f},{y-hh*.42+4*A.w(t,1.9):.0f}'
              f' q{w_*.41:.0f},{hh*.04:.0f} {w_*.82:.0f},0" fill="none"'
              f' stroke="#cfeaf6" stroke-width="{max(4, 8*s_):.0f}" opacity=".8"/>')
    s += (f'<path d="M{x-w_*.30:.0f},{y-hh*.84:.0f} q{-w_*.05:.0f},{hh*.30:.0f}'
          f' {w_*.01:.0f},{hh*.56:.0f}" fill="none" stroke="#ffffff"'
          f' stroke-width="{max(5, 12*s_):.0f}"'
          f' opacity="{.30+.14*abs(A.w(t,2.6)):.2f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-2*s_:.0f}" rx="{w_*.40:.0f}"'
          f' ry="{11*s_:.0f}" fill="#b9d6e8" opacity=".55" {o(max(3, 4*s_))}/>')
    return s


def _svetec(x, y, h_, t, s_=1.0, koryto=True):
    """Светец: КОВАНАЯ стойка — тренога внизу, витой стержень с кольцами, на
    макушке железная развилка-зажим, в неё косо вставлена длинная щепка-лучина.
    Корытце с водой МАЛЕНЬКОЕ и висит на стержне под лучиной. Прежняя версия
    читалась деревцем с тазом — поправлено по осмотру."""
    s = ten(x, y + 10, 100 * s_, 18 * s_, .5)
    # тренога: три кованые лапы с завитками
    for i, sg in ((0, -1), (1, 0), (2, 1)):
        s += (f'<path d="M{x+sg*8*s_:.0f},{y-70*s_:.0f}'
              f' q{sg*40*s_:.0f},{40*s_:.0f} {sg*92*s_:.0f},{66*s_:.0f}'
              f' q{sg*22*s_:.0f},{6*s_:.0f} {sg*8*s_:.0f},{10*s_:.0f}"'
              f' fill="none" stroke="#6b7278" stroke-width="{17*s_:.0f}"'
              f' stroke-linecap="round"/>')
        s += (f'<circle cx="{x+sg*100*s_:.0f}" cy="{y-2*s_:.0f}" r="{11*s_:.0f}"'
              f' fill="#8d949b" {o(max(2, 3*s_))}/>')
    # витой стержень: чередование утолщений даёт ковку, а не ствол
    s += (f'<rect x="{x-11*s_:.0f}" y="{y-h_:.0f}" width="{22*s_:.0f}"'
          f' height="{h_-60*s_:.0f}" rx="{10*s_:.0f}" fill="#7d848c"'
          f' {o(max(3, 5*s_))}/>')
    n = max(4, int((h_ - 120 * s_) / (54 * s_)))
    for i in range(n):
        yy = y - 80 * s_ - i * (h_ - 150 * s_) / n
        s += (f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{20*s_:.0f}"'
              f' ry="{9*s_:.0f}" fill="#9aa1a8" {o(max(2, 3*s_))}/>')
        bl = .25 + .45 * (0.5 + 0.5 * A.w(t, 1.9, i * .14))
        s += (f'<path d="M{x-14*s_:.0f},{yy-4*s_:.0f} q{14*s_:.0f},{-10*s_:.0f}'
              f' {28*s_:.0f},0" fill="none" stroke="#eaf2f8"'
              f' stroke-width="{5*s_:.0f}" opacity="{bl:.2f}"/>')
    # развилка-зажим на макушке: два кованых рога и поперечина
    sj = 3 * s_ * A.ease(A.seg(t, 1.4, .6))
    s += (f'<rect x="{x-30*s_:.0f}" y="{y-h_-18*s_:.0f}" width="{60*s_:.0f}"'
          f' height="{20*s_:.0f}" rx="{8*s_:.0f}" fill="#6b7278"'
          f' {o(max(2, 4*s_))}/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*(24*s_-sj):.0f},{y-h_-14*s_:.0f}'
              f' q{i*10*s_:.0f},{-34*s_:.0f} {i*2*s_:.0f},{-62*s_:.0f}"'
              f' fill="none" stroke="#7d848c" stroke-width="{13*s_:.0f}"'
              f' stroke-linecap="round"/>')
        s += (f'<circle cx="{x+i*(26*s_-sj):.0f}" cy="{y-h_-76*s_:.0f}"'
              f' r="{8*s_:.0f}" fill="#9aa1a8"/>')
    if koryto:                           # корытце висит на стержне, небольшое
        ky_ = y - 150 * s_
        s += (f'<path d="M{x-26*s_:.0f},{ky_-34*s_:.0f} h{52*s_:.0f}"'
              f' stroke="#6b7278" stroke-width="{7*s_:.0f}"/>')
        s += (f'<path d="M{x-62*s_:.0f},{ky_:.0f} h{124*s_:.0f}'
              f' l{-16*s_:.0f},{34*s_:.0f} h{-92*s_:.0f} Z" fill="url(#chug)"'
              f' {o(max(3, 5*s_))}/>')
        s += (f'<path d="M{x-50*s_:.0f},{ky_+8*s_:.0f} h{100*s_:.0f}'
              f' l{-10*s_:.0f},{18*s_:.0f} h{-80*s_:.0f} Z" fill="url(#voda)"'
              f' opacity=".9"/>')
        s += (f'<ellipse cx="{x-14*s_:.0f}" cy="{ky_+14*s_:.0f}" rx="{20*s_:.0f}"'
              f' ry="{5*s_:.0f}" fill="#bfe6f2"'
              f' opacity="{.3+.4*abs(A.w(t,1.6,.2)):.2f}"/>')
    return s


def _luchina_v_razvilke(x, y, t, s_=1.0, gorit=1.0, ph=.0):
    """Длинная щепка-лучина, косо вставленная в развилку: сама щепка с волокном,
    на верхнем конце огонёк, под ней уголёк. Рисуется поверх `_svetec`."""
    dl = 230 * s_
    ax, ay = x + dl * .42, y - dl * .86
    s = (f'<path d="M{x-10*s_:.0f},{y+34*s_:.0f} L{ax:.0f},{ay:.0f}'
         f' l{14*s_:.0f},{10*s_:.0f} L{x+6*s_:.0f},{y+40*s_:.0f} Z"'
         f' fill="url(#derev)" {o(max(3, 5*s_))}/>')
    s += (f'<path d="M{x-4*s_:.0f},{y+28*s_:.0f} L{ax+4*s_:.0f},{ay+6*s_:.0f}"'
          f' stroke="#c9a771" stroke-width="{4*s_:.0f}" opacity=".6"/>')
    if gorit > .02:
        s += ogon(ax + 8 * s_, ay - 6 * s_, t, .62 * s_ * gorit + .1, ph, 6)
        s += teplo(ax, ay, 320 * s_ * gorit + 90, 280 * s_ * gorit + 80,
                   .5 * gorit + .1)
    return s


def _mysh(x, y, s_=1.0, t=0.0, ph=.0, platok=True, hvost=1):
    """Мышь в платочке: капля тела, круглые уши, бусина глаза, длинный хвост."""
    w_ = 54 * s_
    sh = 3 * s_ * A.w(t, .9, ph)
    s = f'<g transform="translate({sh:.1f},0)">'
    s += ten(x, y + 5 * s_, w_ * .7, 7 * s_, .4)
    s += (f'<path d="M{x-w_*.9:.0f},{y:.0f} q{-w_*.12:.0f},{-w_*.56:.0f} {w_*.44:.0f},{-w_*.70:.0f}'
          f' q{w_*.78:.0f},{-w_*.12:.0f} {w_*1.24:.0f},{w_*.30:.0f}'
          f' q{w_*.24:.0f},{w_*.26:.0f} {-w_*.06:.0f},{w_*.40:.0f} Z"'
          f' fill="#8f8880" {o(max(2, 4*s_))}/>')
    s += (f'<ellipse cx="{x-w_*.56:.0f}" cy="{y-w_*.60:.0f}" rx="{w_*.28:.0f}"'
          f' ry="{w_*.30:.0f}" fill="#a39b92" {o(max(2, 3*s_))}/>')
    s += (f'<ellipse cx="{x+w_*.56:.0f}" cy="{y-w_*.34:.0f}" rx="{w_*.26:.0f}"'
          f' ry="{w_*.22:.0f}" fill="#f0cfae" opacity=".5"/>')
    if not A.blink(t, 3.2, ph):
        s += (f'<circle cx="{x+w_*.62:.0f}" cy="{y-w_*.40:.0f}" r="{w_*.09:.0f}"'
              f' fill="{K}"/>')
    s += (f'<circle cx="{x+w_*.94:.0f}" cy="{y-w_*.22:.0f}" r="{w_*.07:.0f}"'
          f' fill="#c97f72"/>')
    if platok:
        s += (f'<path d="M{x+w_*.22:.0f},{y-w_*.62:.0f} q{w_*.34:.0f},{-w_*.34:.0f}'
              f' {w_*.66:.0f},{-w_*.06:.0f} q{-w_*.20:.0f},{w_*.22:.0f}'
              f' {-w_*.66:.0f},{w_*.06:.0f} Z" fill="{TKAN}" {o(max(2, 3*s_))}/>')
    hv = 16 * s_ * A.w(t, 1.1, ph + .3)
    s += (f'<path d="M{x-w_*.86:.0f},{y-w_*.10:.0f} q{-w_*.70:.0f},{hvost*w_*.20:.0f}'
          f' {-w_*1.10:.0f},{hv:.0f}" fill="none" stroke="#7d766e"'
          f' stroke-width="{max(2, 6*s_):.0f}" stroke-linecap="round"/>')
    for i in (-1, 1):                    # лапки переступают
        st = 7 * s_ * A.w(t, .7, ph + (0 if i < 0 else .45))
        s += (f'<path d="M{x+i*w_*.34:.0f},{y-w_*.04:.0f} l{st:.0f},{w_*.18:.0f}"'
              f' stroke="#7d766e" stroke-width="{max(2, 5*s_):.0f}"'
              f' stroke-linecap="round"/>')
    return s + '</g>'


def _golub(x, y, s_=1.0, t=0.0, ph=.0, letit=0.0):
    """Голубь: сизое тело, белая оторочка крыла, лапки. В полёте крылья бьют."""
    w_ = 62 * s_
    vz = letit * 160
    s = f'<g transform="translate({letit*110:.0f},{-vz:.0f})">'
    if letit < .05:
        s += ten(x, y + 6 * s_, w_ * .6, 7 * s_, .35)
    s += (f'<ellipse cx="{x:.0f}" cy="{y-w_*.42:.0f}" rx="{w_*.64:.0f}"'
          f' ry="{w_*.40:.0f}" fill="#6a7684" {o(max(2, 4*s_))}/>')
    s += (f'<circle cx="{x+w_*.56:.0f}" cy="{y-w_*.76:.0f}" r="{w_*.25:.0f}"'
          f' fill="#7c889a" {o(max(2, 3*s_))}/>')
    s += (f'<path d="M{x+w_*.78:.0f},{y-w_*.78:.0f} l{w_*.26:.0f},{w_*.06:.0f}'
          f' l{-w_*.24:.0f},{w_*.10:.0f} Z" fill="#2f3337"/>')
    if not A.blink(t, 3.0, ph):
        s += (f'<circle cx="{x+w_*.62:.0f}" cy="{y-w_*.82:.0f}" r="{w_*.06:.0f}"'
              f' fill="#f2b03c"/>')
    kr = (-28 if letit > .05 else -4) * (1 + .9 * A.w(t, .36 if letit > .05 else 2.4, ph))
    s += (f'<g transform="rotate({kr:.1f} {x:.0f} {y-w_*.52:.0f})">'
          f'<path d="M{x-w_*.20:.0f},{y-w_*.60:.0f} q{w_*.30:.0f},{-w_*.30:.0f}'
          f' {w_*.74:.0f},{-w_*.08:.0f} q{-w_*.24:.0f},{w_*.34:.0f} {-w_*.74:.0f},{w_*.26:.0f} Z"'
          f' fill="#8b97a6" {o(max(2, 3*s_))}/>'
          f'<path d="M{x-w_*.10:.0f},{y-w_*.56:.0f} q{w_*.28:.0f},{-w_*.10:.0f}'
          f' {w_*.52:.0f},{-w_*.04:.0f}" fill="none" stroke="#e8eef6"'
          f' stroke-width="{max(2, 5*s_):.0f}" opacity=".8"/></g>')
    s += (f'<path d="M{x-w_*.56:.0f},{y-w_*.40:.0f} l{-w_*.46:.0f},{-w_*.14:.0f}'
          f' l{w_*.08:.0f},{w_*.26:.0f} Z" fill="#59636f" {o(max(2, 3*s_))}/>')
    if letit < .05:
        for i in (-1, 1):
            s += (f'<path d="M{x+i*w_*.12:.0f},{y-w_*.06:.0f} l0,{w_*.10:.0f}"'
                  f' stroke="#c97f52" stroke-width="{max(2, 5*s_):.0f}"/>')
    return s + '</g>'


def _pes(x, y, s_=1.0, t=0.0, ph=.0, col="#6b5a46"):
    """Пёс: вытянутое тело, висячее ухо, нос у земли, хвост метёт."""
    w_ = 110 * s_
    nos = 8 * s_ * A.w(t, 1.2, ph)
    s = ten(x, y + 8 * s_, w_ * .66, 12 * s_, .42)
    s += (f'<ellipse cx="{x:.0f}" cy="{y-w_*.40:.0f}" rx="{w_*.58:.0f}"'
          f' ry="{w_*.30:.0f}" fill="{col}" {o(max(3, 5*s_))}/>')
    s += (f'<ellipse cx="{x+w_*.62:.0f}" cy="{y-w_*.42+nos:.0f}" rx="{w_*.26:.0f}"'
          f' ry="{w_*.24:.0f}" fill="{col}" {o(max(3, 4*s_))}/>')
    s += (f'<path d="M{x+w_*.80:.0f},{y-w_*.40+nos:.0f} q{w_*.26:.0f},{w_*.04:.0f}'
          f' {w_*.24:.0f},{w_*.16:.0f} q{-w_*.14:.0f},{w_*.06:.0f} {-w_*.26:.0f},{-w_*.02:.0f} Z"'
          f' fill="{col}" {o(max(2, 3*s_))}/>')
    s += (f'<circle cx="{x+w_*1.04:.0f}" cy="{y-w_*.26+nos:.0f}" r="{w_*.07:.0f}"'
          f' fill="#23201c"/>')
    if not A.blink(t, 3.6, ph):
        s += (f'<circle cx="{x+w_*.68:.0f}" cy="{y-w_*.50+nos:.0f}" r="{w_*.05:.0f}"'
              f' fill="#1c1813"/>')
    s += (f'<path d="M{x+w_*.48:.0f},{y-w_*.60+nos:.0f} q{w_*.16:.0f},{w_*.30:.0f}'
          f' {-w_*.06:.0f},{w_*.40:.0f} q{-w_*.18:.0f},{-w_*.18:.0f} {-w_*.10:.0f},{-w_*.40:.0f} Z"'
          f' fill="#54463a" {o(max(2, 3*s_))}/>')
    hv = 34 * A.w(t, .55, ph)
    s += (f'<path d="M{x-w_*.56:.0f},{y-w_*.52:.0f} q{-w_*.30:.0f},{-w_*.20:.0f}'
          f' {-w_*.24:.0f},{-w_*.52+hv*.01:.0f}" fill="none" stroke="{col}"'
          f' stroke-width="{max(4, 13*s_):.0f}" stroke-linecap="round"'
          f' transform="rotate({hv*.5:.1f} {x-w_*.56:.0f} {y-w_*.52:.0f})"/>')
    for i, sgn in ((0, -1), (1, 1)):
        st = 6 * s_ * A.w(t, .8, ph + i * .4)
        s += (f'<rect x="{x+sgn*w_*.34:.0f}" y="{y-w_*.20:.0f}" width="{w_*.14:.0f}"'
              f' height="{w_*.22:.0f}" rx="{w_*.06:.0f}" fill="{col}"'
              f' transform="rotate({st:.1f} {x+sgn*w_*.34:.0f} {y-w_*.20:.0f})"'
              f' {o(max(2, 3*s_))}/>')
    return s


def _afisha(x, y, w_, h_, t, vid="traktor", seed=5, ug=0.0, otgib=0.0):
    """Афиша: бумага и ОДИН крупный предмет. Букв нет — название даёт
    волнистая полоса под предметом (правило: текст в декорации не рисуем)."""
    rnd = random.Random(seed)
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' rx="6" fill="url(#list)" {o(6)}/>')
    s += (f'<rect x="{x-w_/2+14:.0f}" y="{y-h_/2+14:.0f}" width="{w_-28:.0f}"'
          f' height="{h_-28:.0f}" rx="4" fill="none" stroke="{KRAS}"'
          f' stroke-width="8" opacity=".7"/>')
    cx, cy = x, y - h_ * .10
    if vid == "traktor":
        s += (f'<rect x="{cx-w_*.30:.0f}" y="{cy-h_*.10:.0f}" width="{w_*.46:.0f}"'
              f' height="{h_*.20:.0f}" rx="10" fill="{KRAS}" {o(6)}/>')
        s += (f'<rect x="{cx-w_*.06:.0f}" y="{cy-h_*.26:.0f}" width="{w_*.22:.0f}"'
              f' height="{h_*.18:.0f}" rx="8" fill="#b43a22" {o(5)}/>')
        s += (f'<rect x="{cx-w_*.26:.0f}" y="{cy-h_*.26:.0f}" width="{w_*.10:.0f}"'
              f' height="{h_*.14:.0f}" rx="5" fill="#4a4f55" {o(4)}/>')
        kol = (t * 120) % 360
        s += (f'<circle cx="{cx+w_*.14:.0f}" cy="{cy+h_*.14:.0f}" r="{h_*.16:.0f}"'
              f' fill="#2f3337" {o(6)}/>')
        s += (f'<g transform="rotate({kol:.0f} {cx+w_*.14:.0f} {cy+h_*.14:.0f})">')
        for i in range(6):
            a = i * 1.047
            s += (f'<line x1="{cx+w_*.14:.0f}" y1="{cy+h_*.14:.0f}"'
                  f' x2="{cx+w_*.14+math.cos(a)*h_*.14:.0f}"'
                  f' y2="{cy+h_*.14+math.sin(a)*h_*.14:.0f}" stroke="#8d949b"'
                  f' stroke-width="6"/>')
        s += '</g>'
        s += (f'<circle cx="{cx-w_*.22:.0f}" cy="{cy+h_*.18:.0f}" r="{h_*.10:.0f}"'
              f' fill="#2f3337" {o(5)}/>')
        for i in range(5):               # борозда поля
            s += (f'<path d="M{cx-w_*.40+i*w_*.18:.0f},{cy+h_*.30:.0f}'
                  f' q{w_*.06:.0f},{h_*.06:.0f} 0,{h_*.12:.0f}" fill="none"'
                  f' stroke="#7d5636" stroke-width="7" opacity=".8"/>')
    elif vid == "rozhok":
        # длинный изогнутый рог: от узкого мундштука слева к небольшому
        # раструбу справа вверху, лента повязана посередине
        s += (f'<path d="M{cx-w_*.40:.0f},{cy+h_*.16:.0f}'
              f' q{w_*.30:.0f},{h_*.04:.0f} {w_*.56:.0f},{-h_*.18:.0f}'
              f' q{w_*.18:.0f},{-h_*.12:.0f} {w_*.26:.0f},{-h_*.26:.0f}'
              f' l{w_*.05:.0f},{h_*.15:.0f}'
              f' q{-w_*.08:.0f},{h_*.12:.0f} {-w_*.24:.0f},{h_*.24:.0f}'
              f' q{-w_*.26:.0f},{h_*.18:.0f} {-w_*.58:.0f},{h_*.14:.0f} Z"'
              f' fill="#c9a06a" {o(7)}/>')
        s += (f'<path d="M{cx+w_*.40:.0f},{cy-h_*.28:.0f}'
              f' q{w_*.11:.0f},{-h_*.09:.0f} {w_*.16:.0f},{h_*.01:.0f}'
              f' q{w_*.02:.0f},{h_*.11:.0f} {-w_*.11:.0f},{h_*.14:.0f}'
              f' q{-w_*.07:.0f},{-h_*.05:.0f} {-w_*.05:.0f},{-h_*.15:.0f} Z"'
              f' fill="url(#zol)" {o(6)}/>')
        s += (f'<ellipse cx="{cx+w_*.50:.0f}" cy="{cy-h_*.24:.0f}"'
              f' rx="{w_*.045:.0f}" ry="{h_*.055:.0f}" fill="#5e3a16"'
              f' opacity=".9"/>')
        s += (f'<ellipse cx="{cx-w_*.40:.0f}" cy="{cy+h_*.19:.0f}"'
              f' rx="{w_*.035:.0f}" ry="{h_*.035:.0f}" fill="#8d949b"'
              f' {o(4)}/>')
        for i in range(4):               # берестяные обручи по рогу
            s += (f'<path d="M{cx-w_*.24+i*w_*.17:.0f},'
                  f'{cy+h_*.14-i*h_*.055:.0f} l{w_*.02:.0f},{h_*.085:.0f}"'
                  f' stroke="#7d5220" stroke-width="10" opacity=".9"/>')
        lent = 12 * A.w(t, 2.2, seed * .1)
        s += (f'<path d="M{cx-w_*.02:.0f},{cy+h_*.02:.0f}'
              f' q{-w_*.07:.0f},{h_*.05:.0f} {w_*.01:.0f},{h_*.11:.0f}'
              f' q{w_*.08:.0f},{-h_*.04:.0f} {w_*.03:.0f},{-h_*.12:.0f} Z"'
              f' fill="{KRAS}" {o(3)}/>')
        for j in (0, 1):                 # два хвоста ленты
            s += (f'<path d="M{cx:.0f},{cy+h_*.08:.0f}'
                  f' q{-w_*.08+lent*.2:.0f},{h_*.14+j*h_*.05:.0f}'
                  f' {-w_*.16-j*w_*.07:.0f},{h_*.24+j*h_*.07:.0f}'
                  f' l{w_*.08:.0f},{h_*.04:.0f}'
                  f' q{w_*.09:.0f},{-h_*.12:.0f} {w_*.14:.0f},{-h_*.28:.0f} Z"'
                  f' fill="{KRAS}" {o(4)}/>')
        lent = 10 * A.w(t, 2.2, seed * .1)
        s += (f'<path d="M{cx-w_*.24:.0f},{cy+h_*.16:.0f} q{-w_*.18:.0f},{h_*.16+lent:.0f}'
              f' {-w_*.06:.0f},{h_*.34:.0f} q{w_*.14:.0f},{-h_*.12:.0f}'
              f' {w_*.18:.0f},{-h_*.30:.0f} Z" fill="{KRAS}" {o(4)}/>')
    elif vid == "snop":
        # сноп: низ раскинут веером, перевясло посередине, вверху колосья
        for i in range(15):
            a = -1.15 + i * .164
            bx_ = cx + math.sin(a) * w_ * .34
            s += (f'<path d="M{cx+math.sin(a)*w_*.22:.0f},{cy+h_*.30:.0f}'
                  f' Q{cx+math.sin(a)*w_*.06:.0f},{cy+h_*.02:.0f}'
                  f' {bx_:.0f},{cy-h_*.26:.0f}" fill="none"'
                  f' stroke="url(#solom)" stroke-width="{8+(i%3)*3}"'
                  f' stroke-linecap="round"/>')
            for j in (-1, 1):            # зёрна парами по колосу
                s += (f'<ellipse cx="{bx_+j*h_*.022:.0f}"'
                      f' cy="{cy-h_*.30+4*A.w(t,2.4,i*.1):.0f}"'
                      f' rx="{h_*.022:.0f}" ry="{h_*.045:.0f}" fill="#e3c272"'
                      f' {o(2)}/>')
                s += (f'<ellipse cx="{bx_+j*h_*.020:.0f}"'
                      f' cy="{cy-h_*.38+4*A.w(t,2.4,i*.1+.2):.0f}"'
                      f' rx="{h_*.020:.0f}" ry="{h_*.040:.0f}" fill="#d8b96a"'
                      f' {o(2)}/>')
        s += (f'<path d="M{cx-w_*.20:.0f},{cy+h_*.02:.0f} q{w_*.20:.0f},{h_*.10:.0f}'
              f' {w_*.40:.0f},0 l0,{h_*.07:.0f} q{-w_*.20:.0f},{h_*.10:.0f}'
              f' {-w_*.40:.0f},0 Z" fill="{KRAS}" {o(4)}/>')
    elif vid == "parovoz":
        s += (f'<rect x="{cx-w_*.30:.0f}" y="{cy-h_*.04:.0f}" width="{w_*.56:.0f}"'
              f' height="{h_*.20:.0f}" rx="{h_*.09:.0f}" fill="#2f3337" {o(6)}/>')
        s += (f'<rect x="{cx-w_*.34:.0f}" y="{cy-h_*.22:.0f}" width="{w_*.16:.0f}"'
              f' height="{h_*.20:.0f}" rx="6" fill="#3f454a" {o(5)}/>')
        s += (f'<rect x="{cx+w_*.04:.0f}" y="{cy-h_*.24:.0f}" width="{w_*.10:.0f}"'
              f' height="{h_*.22:.0f}" rx="4" fill="#4a4f55" {o(4)}/>')
        for i in range(2):
            s += (f'<circle cx="{cx-w_*.18+i*w_*.34:.0f}" cy="{cy+h_*.20:.0f}"'
                  f' r="{h_*.09:.0f}" fill="#23262a" {o(5)}/>')
        for i in range(5):               # клубы пара на афише живут
            k = ((t * .34) + i * .2) % 1.0
            s += (f'<circle cx="{cx+w_*.10+k*w_*.26:.0f}" cy="{cy-h_*.28-k*h_*.22:.0f}"'
                  f' r="{h_*(.05+.08*k):.0f}" fill="#e8eef6"'
                  f' opacity="{.7*(1-k):.2f}"/>')
        s += (f'<path d="M{cx-w_*.34:.0f},{cy+h_*.30:.0f} h{w_*.68:.0f}"'
              f' stroke="#6b645c" stroke-width="8"/>')
    elif vid == "shlyapka":
        s += (f'<ellipse cx="{cx:.0f}" cy="{cy+h_*.02:.0f}" rx="{w_*.30:.0f}"'
              f' ry="{h_*.07:.0f}" fill="#2b2a30" {o(6)}/>')
        s += (f'<path d="M{cx-w_*.17:.0f},{cy:.0f} q{w_*.17:.0f},{-h_*.26:.0f}'
              f' {w_*.34:.0f},0 Z" fill="#3a3842" {o(5)}/>')
        s += (f'<path d="M{cx-w_*.16:.0f},{cy-h_*.10:.0f} q{w_*.18:.0f},{-h_*.10:.0f}'
              f' {w_*.34:.0f},{h_*.02:.0f}" fill="none" stroke="{TKAN}"'
              f' stroke-width="10"/>')
        for i in range(7):               # вуаль сеточкой
            vv = 4 * A.w(t, 2.6, i * .12)
            s += (f'<path d="M{cx-w_*.26+i*w_*.09:.0f},{cy+h_*.02:.0f}'
                  f' q{vv:.0f},{h_*.10:.0f} {vv*.4:.0f},{h_*.22:.0f}" fill="none"'
                  f' stroke="#2b2a30" stroke-width="4" opacity=".65"/>')
        s += (f'<path d="M{cx-w_*.26:.0f},{cy+h_*.14:.0f} q{w_*.26:.0f},{h_*.08:.0f}'
              f' {w_*.52:.0f},0" fill="none" stroke="#2b2a30" stroke-width="4"'
              f' opacity=".6"/>')
    else:                                # меч в зелёном холме
        s += (f'<path d="M{cx-w_*.42:.0f},{cy+h_*.30:.0f} q{w_*.42:.0f},{-h_*.26:.0f}'
              f' {w_*.84:.0f},0 Z" fill="{ZEL2}" {o(6)}/>')
        s += f'<g transform="rotate(18 {cx:.0f} {cy+h_*.16:.0f})">'
        s += (f'<rect x="{cx-w_*.105:.0f}" y="{cy-h_*.30:.0f}"'
              f' width="{w_*.21:.0f}" height="{h_*.46:.0f}" fill="#dfe8ef"'
              f' {o(7)}/>')
        s += (f'<line x1="{cx:.0f}" y1="{cy-h_*.28:.0f}" x2="{cx:.0f}"'
              f' y2="{cy+h_*.12:.0f}" stroke="#aebfc9" stroke-width="7"/>')
        s += (f'<path d="M{cx-w_*.105:.0f},{cy-h_*.30:.0f} l{w_*.105:.0f},'
              f'{-h_*.14:.0f} l{w_*.105:.0f},{h_*.14:.0f} Z" fill="#f2f8fc"'
              f' {o(6)}/>')
        s += (f'<path d="M{cx-w_*.30:.0f},{cy-h_*.34:.0f}'
              f' q{w_*.30:.0f},{-h_*.09:.0f} {w_*.60:.0f},0'
              f' l{-w_*.05:.0f},{h_*.09:.0f} q{-w_*.25:.0f},{h_*.06:.0f}'
              f' {-w_*.50:.0f},0 Z" fill="url(#zol)" {o(6)}/>')
        s += (f'<rect x="{cx-w_*.075:.0f}" y="{cy-h_*.52:.0f}"'
              f' width="{w_*.15:.0f}" height="{h_*.18:.0f}" rx="7"'
              f' fill="#6b4a2a" {o(6)}/>')
        for i in range(3):               # обмотка рукояти
            s += (f'<line x1="{cx-w_*.075:.0f}" y1="{cy-h_*.48+i*h_*.05:.0f}"'
                  f' x2="{cx+w_*.075:.0f}" y2="{cy-h_*.46+i*h_*.05:.0f}"'
                  f' stroke="#4a3018" stroke-width="5"/>')
        s += (f'<circle cx="{cx:.0f}" cy="{cy-h_*.57:.0f}" r="{w_*.065:.0f}"'
              f' fill="url(#zol)" {o(5)}/>')
        s += '</g>'
        bl = .3 + .5 * (0.5 + 0.5 * A.w(t, 2.0, seed * .2))
        s += (f'<line x1="{cx:.0f}" y1="{cy-h_*.26:.0f}" x2="{cx:.0f}"'
              f' y2="{cy+h_*.10:.0f}" stroke="#ffffff" stroke-width="7"'
              f' opacity="{bl:.2f}"/>')
    for i in range(3):                   # «название» — волна, не буквы
        s += (f'<path d="M{x-w_*.34:.0f},{y+h_*.30+i*h_*.07:.0f}'
              f' q{w_*.17:.0f},{rnd.uniform(-6,6):.0f} {w_*.68:.0f},0" fill="none"'
              f' stroke="#6b645c" stroke-width="{12-i*3}" opacity=".85"/>')
    if otgib > .02:                      # уголок отгибается
        s += (f'<path d="M{x+w_/2:.0f},{y-h_/2:.0f} l{-w_*.16*otgib:.0f},0'
              f' l0,{h_*.16*otgib:.0f} Z" fill="#d3c7a8" {o(3)}/>')
    return s + '</g>'


def _lampochki(x, y, w_, n, t, r=12, col=SVET):
    """Бегущие лампочки по фасаду: волна бежит, часть перегорела."""
    s = ""
    for i in range(n):
        xx = x + i * (w_ / max(1, n - 1))
        f = ((t * .9) + i / n) % 1.0
        yar = .22 + .78 * max(0.0, 1 - abs(f - .5) * 3.2)
        if i % 7 == 5:
            yar *= .25
        s += (f'<circle cx="{xx:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{col}"'
              f' opacity="{yar:.2f}"/>')
        s += (f'<circle cx="{xx:.0f}" cy="{y:.0f}" r="{r*.42:.0f}" fill="#fffaf0"'
              f' opacity="{yar:.2f}"/>')
        s += (f'<circle cx="{xx:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="none" {o(3)}/>')
        if yar > .6:
            s += teplo(xx, y, r * 5, r * 5, .22 * yar)
    return s


def _botinok(x, y, s_=1.0, t=0.0, ph=.0, col="#4a3526", blesk=0.0):
    """Зимний ботинок: толстая подошва, язычок, шнуровка крест-накрест."""
    w_, hh = 150 * s_, 110 * s_
    s = ten(x, y + 6 * s_, w_ * .56, 11 * s_, .42)
    s += (f'<path d="M{x-w_*.42:.0f},{y:.0f} q{-w_*.06:.0f},{-hh*.62:.0f} {w_*.14:.0f},{-hh*.74:.0f}'
          f' q{w_*.26:.0f},{-hh*.08:.0f} {w_*.34:.0f},{hh*.22:.0f}'
          f' q{w_*.10:.0f},{hh*.30:.0f} {w_*.46:.0f},{hh*.40:.0f}'
          f' q{w_*.16:.0f},{hh*.06:.0f} {w_*.08:.0f},{hh*.14:.0f} Z"'
          f' fill="{col}" {o(max(3, 6*s_))}/>')
    s += (f'<path d="M{x-w_*.44:.0f},{y-hh*.02:.0f} q{w_*.46:.0f},{hh*.16:.0f}'
          f' {w_*1.04:.0f},{hh*.02:.0f} q{w_*.06:.0f},{hh*.14:.0f} {-w_*.06:.0f},{hh*.16:.0f}'
          f' q{-w_*.56:.0f},{hh*.08:.0f} {-w_*1.00:.0f},{-hh*.04:.0f} Z"'
          f' fill="#23211e" {o(max(3, 5*s_))}/>')
    for i in range(6):                   # рубчик подошвы
        s += (f'<line x1="{x-w_*.36+i*w_*.17:.0f}" y1="{y+hh*.04:.0f}"'
              f' x2="{x-w_*.36+i*w_*.17:.0f}" y2="{y+hh*.16:.0f}" stroke="#3b3835"'
              f' stroke-width="{max(2, 5*s_):.0f}"/>')
    s += (f'<path d="M{x-w_*.22:.0f},{y-hh*.70:.0f} q{w_*.14:.0f},{hh*.22:.0f}'
          f' {w_*.06:.0f},{hh*.44:.0f} l{-w_*.22:.0f},{-hh*.04:.0f} Z"'
          f' fill="#6b5234" {o(max(2, 4*s_))}/>')
    for i in range(4):                   # шнуровка крест-накрест
        yy = y - hh * .60 + i * hh * .13
        s += (f'<line x1="{x-w_*.26:.0f}" y1="{yy:.0f}" x2="{x-w_*.04:.0f}"'
              f' y2="{yy+hh*.09:.0f}" stroke="#d8cbb0"'
              f' stroke-width="{max(2, 5*s_):.0f}"/>')
        s += (f'<line x1="{x-w_*.04:.0f}" y1="{yy:.0f}" x2="{x-w_*.26:.0f}"'
              f' y2="{yy+hh*.09:.0f}" stroke="#d8cbb0"'
              f' stroke-width="{max(2, 5*s_):.0f}"/>')
    if blesk > .01:                      # наведённый блеск на носке
        s += (f'<ellipse cx="{x+w_*.52:.0f}" cy="{y-hh*.20:.0f}" rx="{w_*.16:.0f}"'
              f' ry="{hh*.10:.0f}" fill="#ffffff"'
              f' opacity="{(.18+.3*abs(A.w(t,1.8,ph)))*blesk:.2f}"/>')
    return s


def _ochki(x, y, s_=1.0, t=0.0, verevka=True):
    """Очки на верёвочке: два ободка, переносица, шнурок за ушами."""
    r = 34 * s_
    bl = .3 + .4 * abs(A.w(t, 2.2))
    s = ""
    for i in (-1, 1):
        s += (f'<circle cx="{x+i*r*1.25:.0f}" cy="{y:.0f}" r="{r:.0f}"'
              f' fill="url(#stekl)" opacity=".55" {o(max(2, 5*s_))}/>')
        s += (f'<path d="M{x+i*r*1.25-r*.5:.0f},{y-r*.4:.0f} q{r*.4:.0f},{-r*.3:.0f}'
              f' {r*.8:.0f},{r*.1:.0f}" fill="none" stroke="#ffffff"'
              f' stroke-width="{max(2, 6*s_):.0f}" opacity="{bl:.2f}"/>')
    s += (f'<path d="M{x-r*.3:.0f},{y-r*.1:.0f} q{r*.3:.0f},{-r*.3:.0f} {r*.6:.0f},0"'
          f' fill="none" stroke="#4a4f55" stroke-width="{max(3, 7*s_):.0f}"/>')
    if verevka:
        for i in (-1, 1):
            s += (f'<path d="M{x+i*r*2.3:.0f},{y:.0f} q{i*r*.9:.0f},{r*.4:.0f}'
                  f' {i*r*1.1:.0f},{r*1.9+6*A.w(t,2.0,i*.2):.0f}" fill="none"'
                  f' stroke="#8d7a5a" stroke-width="{max(2, 5*s_):.0f}"/>')
    return s


def _kinokamera(x, y, s_=1.0, t=0.0, krutit=True, trenoga=True):
    """Деревянная кинокамера на треноге: корпус-ящик, две бобины сверху,
    объектив гармошкой, ручка сбоку крутится."""
    w_, hh = 240 * s_, 170 * s_
    s = ten(x, y + 10 * s_, w_ * .7, 18 * s_, .5)
    if trenoga:
        for i, sgn in ((0, -1), (1, 0), (2, 1)):  # ноги треноги
            s += (f'<path d="M{x+sgn*18*s_:.0f},{y-200*s_:.0f}'
                  f' L{x+sgn*150*s_+(0 if sgn else 20*s_):.0f},{y:.0f}"'
                  f' stroke="url(#derev)" stroke-width="{18*s_:.0f}"'
                  f' stroke-linecap="round"/>')
    s += (f'<rect x="{x-50*s_:.0f}" y="{y-250*s_:.0f}" width="{100*s_:.0f}"'
          f' height="{54*s_:.0f}" rx="{10*s_:.0f}" fill="#4a4f55" {o(5)}/>')
    s += (f'<rect x="{x-w_*.5:.0f}" y="{y-250*s_-hh:.0f}" width="{w_:.0f}"'
          f' height="{hh:.0f}" rx="{12*s_:.0f}" fill="url(#derev)" {o(8)}/>')
    s += (f'<rect x="{x-w_*.42:.0f}" y="{y-250*s_-hh*.86:.0f}" width="{w_*.84:.0f}"'
          f' height="{hh*.64:.0f}" rx="{8*s_:.0f}" fill="none" stroke="#6d4423"'
          f' stroke-width="{7*s_:.0f}"/>')
    # кожаная ручка на крышке: по ней камеру и узнают
    s += (f'<path d="M{x-w_*.14:.0f},{y-250*s_-hh:.0f} q{w_*.14:.0f},{-46*s_:.0f}'
          f' {w_*.28:.0f},0" fill="none" stroke="#4a3526"'
          f' stroke-width="{14*s_:.0f}" stroke-linecap="round"/>')
    for i, sgn in ((0, -1), (1, 1)):     # бобины
        rot = (t * (150 if krutit else 0) + i * 40) % 360
        bx, by = x + sgn * w_ * .26, y - 250 * s_ - hh - 6 * s_
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{56*s_:.0f}" fill="#3f454a" {o(6)}/>')
        s += (f'<g transform="rotate({rot:.0f} {bx:.0f} {by:.0f})">')
        for j in range(4):
            a = j * 1.5708
            s += (f'<line x1="{bx:.0f}" y1="{by:.0f}"'
                  f' x2="{bx+math.cos(a)*50*s_:.0f}" y2="{by+math.sin(a)*50*s_:.0f}"'
                  f' stroke="#8d949b" stroke-width="{8*s_:.0f}"/>')
        s += '</g>'
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{14*s_:.0f}" fill="url(#zhel)"'
              f' {o(3)}/>')
        s += (f'<rect x="{bx-16*s_:.0f}" y="{by+30*s_:.0f}" width="{32*s_:.0f}"'
              f' height="{40*s_:.0f}" rx="{6*s_:.0f}" fill="#2f3337"'
              f' {o(max(2, 3*s_))}/>')
    ox = x + w_ * .5
    s += (f'<rect x="{ox:.0f}" y="{y-250*s_-hh*.66:.0f}" width="{46*s_:.0f}"'
          f' height="{44*s_:.0f}" rx="6" fill="#4a4f55" {o(5)}/>')
    for i in range(5):                   # гармошка объектива, рёбрами
        s += (f'<rect x="{ox+40*s_+i*22*s_:.0f}" y="{y-250*s_-hh*.74+i*4*s_:.0f}"'
              f' width="{18*s_:.0f}" height="{66*s_-i*6*s_:.0f}" rx="5"'
              f' fill="#4a5056" {o(max(2, 4*s_))}/>')
        s += (f'<rect x="{ox+40*s_+i*22*s_:.0f}" y="{y-250*s_-hh*.74+i*4*s_:.0f}"'
              f' width="{18*s_:.0f}" height="{10*s_:.0f}" rx="4" fill="#737b82"'
              f' opacity=".8"/>')
    s += (f'<circle cx="{ox+118*s_:.0f}" cy="{y-250*s_-hh*.46:.0f}" r="{26*s_:.0f}"'
          f' fill="#1d2024" {o(5)}/>')
    s += (f'<circle cx="{ox+112*s_:.0f}" cy="{y-250*s_-hh*.52:.0f}" r="{9*s_:.0f}"'
          f' fill="#cfe4f5" opacity="{.4+.4*abs(A.w(t,2.2)):.2f}"/>')
    rh = (t * 300) % 360 if krutit else 0
    hx_, hy_ = x - w_ * .5 - 30 * s_, y - 250 * s_ - hh * .40
    s += (f'<circle cx="{hx_:.0f}" cy="{hy_:.0f}" r="{20*s_:.0f}" fill="#5d6168"'
          f' {o(max(2, 4*s_))}/>')
    s += (f'<g transform="rotate({rh:.0f} {hx_:.0f} {hy_:.0f})">'
          f'<line x1="{hx_:.0f}" y1="{hy_:.0f}" x2="{hx_:.0f}"'
          f' y2="{hy_+74*s_:.0f}" stroke="#8d949b"'
          f' stroke-width="{14*s_:.0f}" stroke-linecap="round"/>'
          f'<rect x="{hx_-9*s_:.0f}" y="{hy_+66*s_:.0f}" width="{18*s_:.0f}"'
          f' height="{40*s_:.0f}" rx="{9*s_:.0f}" fill="url(#derev)"'
          f' {o(max(2, 3*s_))}/></g>')
    s += (f'<rect x="{x-w_*.5-22*s_:.0f}" y="{y-250*s_-hh*.46:.0f}" width="{18*s_:.0f}"'
          f' height="{18*s_:.0f}" rx="4" fill="#2f3337"/>')
    return s


def _hlopushka(x, y, s_=1.0, t=0.0, shchel=0.0, ug=-12.0):
    """Хлопушка: доска с косыми полосами и откидная планка, которая хлопает."""
    w_, hh = 200 * s_, 130 * s_
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-hh/2:.0f}" width="{w_:.0f}" height="{hh:.0f}"'
          f' rx="{8*s_:.0f}" fill="#2b2a2e" {o(max(3, 6*s_))}/>')
    for i in range(4):                   # поля под запись — пустые полосы
        s += (f'<rect x="{x-w_*.44:.0f}" y="{y-hh*.34+i*hh*.18:.0f}"'
              f' width="{w_*.88:.0f}" height="{hh*.12:.0f}" rx="3" fill="#4b4a50"'
              f' opacity=".75"/>')
    otk = -46 * (1 - shchel)
    s += f'<g transform="rotate({otk:.1f} {x-w_/2:.0f} {y-hh/2:.0f})">'
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-hh/2-34*s_:.0f}" width="{w_:.0f}"'
          f' height="{34*s_:.0f}" rx="{6*s_:.0f}" fill="#1f1e22" {o(max(3, 5*s_))}/>')
    for i in range(7):                   # косые полосы — узнаваемый знак
        xx = x - w_ / 2 + i * (w_ / 7)
        s += (f'<path d="M{xx:.0f},{y-hh/2:.0f} l{w_/14:.0f},{-34*s_:.0f}'
              f' l{w_/14:.0f},0 l{-w_/14:.0f},{34*s_:.0f} Z" fill="#f2efe6"/>')
    s += '</g>'
    if shchel > .9:
        for i in range(5):               # пыль от хлопка
            a = -2.4 + i * .5
            s += (f'<circle cx="{x-w_/2+math.cos(a)*44*s_:.0f}"'
                  f' cy="{y-hh/2+math.sin(a)*44*s_:.0f}" r="{(7+i)*s_:.0f}"'
                  f' fill="#e8eef6" opacity=".4"/>')
    return s + '</g>'


def _loshadka(x, y, s_=1.0, t=0.0, op=1.0):
    """Рисованная лошадка-мечта: ВЫСОКИЕ ноги, глубокая грудь, длинная шея
    дугой вверх и голова с вытянутой мордой. Прежние короткие ножки при
    длинном низком корпусе давали собаку (осмотр 14.11)."""
    w_ = 150 * s_                        # масштабная единица
    kiv = 3.0 * A.w(t, 1.5)
    bx, by = x - w_ * .20, y - w_ * 1.36  # центр корпуса — высоко над землёй
    s = f'<g opacity="{op:.2f}">'
    s += ten(bx, y + w_ * .04, w_ * .60, w_ * .08, .32 * op)
    for i, (lx_, ph_, zad) in enumerate(((-.62, .0, True), (-.44, .3, True),
                                         (.22, .5, False), (.40, .8, False))):
        sh = w_ * .08 * A.w(t, .9, ph_)
        # бедро/плечо
        s += (f'<ellipse cx="{bx+w_*lx_+w_*.07:.0f}" cy="{by+w_*.34:.0f}"'
              f' rx="{w_*.17:.0f}" ry="{w_*.24:.0f}" fill="#7d5f40" {o(5)}/>')
        # голень: длинная, до самой земли
        s += (f'<g transform="rotate({sh*.3:.1f} {bx+w_*lx_+w_*.07:.0f}'
              f' {by+w_*.40:.0f})">'
              f'<rect x="{bx+w_*lx_:.0f}" y="{by+w_*.40:.0f}"'
              f' width="{w_*.14:.0f}" height="{w_*.92:.0f}" rx="{w_*.06:.0f}"'
              f' fill="#7d5f40" {o(5)}/>'
              f'<rect x="{bx+w_*lx_-w_*.02:.0f}" y="{by+w_*1.22:.0f}"'
              f' width="{w_*.18:.0f}" height="{w_*.14:.0f}" rx="{w_*.04:.0f}"'
              f' fill="#4a3526" {o(4)}/></g>')
    hv = 9 * A.w(t, 1.1, .2)             # хвост от крупа
    s += (f'<path d="M{bx-w_*.80:.0f},{by-w_*.22:.0f}'
          f' q{-w_*.34:.0f},{w_*.30:.0f} {-w_*.26:.0f},{w_*.76:.0f}'
          f' l{w_*.18:.0f},{w_*.04:.0f} q{w_*.02:.0f},{-w_*.46:.0f}'
          f' {w_*.26:.0f},{-w_*.70:.0f} Z" fill="#5e4428"'
          f' transform="rotate({hv:.1f} {bx-w_*.80:.0f} {by-w_*.22:.0f})"'
          f' {o(5)}/>')
    # корпус: глубокая грудь спереди, круп сзади, спина с провисанием
    s += (f'<path d="M{bx-w_*.84:.0f},{by-w_*.26:.0f}'
          f' q{w_*.40:.0f},{-w_*.22:.0f} {w_*.84:.0f},{-w_*.10:.0f}'
          f' q{w_*.44:.0f},{w_*.02:.0f} {w_*.78:.0f},{w_*.18:.0f}'
          f' q{w_*.14:.0f},{w_*.40:.0f} {-w_*.10:.0f},{w_*.60:.0f}'
          f' q{-w_*.60:.0f},{w_*.18:.0f} {-w_*1.46:.0f},{w_*.02:.0f}'
          f' q{-w_*.24:.0f},{-w_*.26:.0f} {-w_*.06:.0f},{-w_*.70:.0f} Z"'
          f' fill="#8a6a4a" {o(7)}/>')
    s += (f'<ellipse cx="{bx-w_*.16:.0f}" cy="{by+w_*.18:.0f}" rx="{w_*.50:.0f}"'
          f' ry="{w_*.22:.0f}" fill="#9a7a56" opacity=".5"/>')
    # шея дугой ВВЕРХ и голова с длинной мордой — кивают как одно целое
    s += f'<g transform="rotate({kiv:.1f} {bx+w_*.62:.0f} {by-w_*.24:.0f})">'
    s += (f'<path d="M{bx+w_*.46:.0f},{by-w_*.34:.0f}'
          f' q{w_*.26:.0f},{-w_*.42:.0f} {w_*.56:.0f},{-w_*.70:.0f}'
          f' l{w_*.34:.0f},{w_*.22:.0f}'
          f' q{-w_*.22:.0f},{w_*.46:.0f} {-w_*.40:.0f},{w_*.68:.0f} Z"'
          f' fill="#8a6a4a" {o(6)}/>')
    hx_, hy_ = bx + w_ * 1.10, by - w_ * 1.04
    s += (f'<path d="M{hx_-w_*.22:.0f},{hy_-w_*.06:.0f}'
          f' q{w_*.16:.0f},{-w_*.26:.0f} {w_*.40:.0f},{-w_*.16:.0f}'
          f' q{w_*.22:.0f},{w_*.10:.0f} {w_*.26:.0f},{w_*.36:.0f}'
          f' q{w_*.02:.0f},{w_*.16:.0f} {-w_*.16:.0f},{w_*.18:.0f}'
          f' q{-w_*.30:.0f},{w_*.02:.0f} {-w_*.50:.0f},{-w_*.14:.0f} Z"'
          f' fill="#8a6a4a" {o(6)}/>')
    s += (f'<ellipse cx="{hx_+w_*.36:.0f}" cy="{hy_+w_*.30:.0f}"'
          f' rx="{w_*.15:.0f}" ry="{w_*.13:.0f}" fill="#9a7a56" {o(5)}/>')
    s += (f'<ellipse cx="{hx_+w_*.40:.0f}" cy="{hy_+w_*.30:.0f}"'
          f' rx="{w_*.05:.0f}" ry="{w_*.04:.0f}" fill="#4a3526"/>')
    for i in (-1, 1):                    # уши торчком
        s += (f'<path d="M{hx_-w_*.06+i*w_*.08:.0f},{hy_-w_*.20:.0f}'
              f' l{w_*.03:.0f},{-w_*.22:.0f} l{w_*.11:.0f},{w_*.17:.0f} Z"'
              f' fill="#8a6a4a" {o(4)}/>')
    if not A.blink(t, 3.4, .2):
        s += (f'<circle cx="{hx_+w_*.08:.0f}" cy="{hy_-w_*.02:.0f}"'
              f' r="{w_*.055:.0f}" fill="{K}"/>')
    for i in range(7):                   # грива по гребню шеи
        gr = 9 * A.w(t, .8, i * .12)
        s += (f'<path d="M{bx+w_*(.58+i*.08):.0f},{by-w_*(.42+i*.11):.0f}'
              f' q{-w_*.15+gr*.01:.0f},{w_*.16:.0f}'
              f' {-w_*.28+gr*.02:.0f},{w_*.26:.0f}" fill="none"'
              f' stroke="#5e4428" stroke-width="{13*s_:.0f}"'
              f' stroke-linecap="round"/>')
    s += (f'<path d="M{hx_-w_*.08:.0f},{hy_+w_*.14:.0f} q{w_*.20:.0f},'
          f'{w_*.08:.0f} {w_*.38:.0f},{w_*.06:.0f}" fill="none" stroke="{MED}"'
          f' stroke-width="{10*s_:.0f}"/>')
    s += (f'<circle cx="{hx_-w_*.06:.0f}" cy="{hy_+w_*.16:.0f}"'
          f' r="{w_*.08:.0f}" fill="none" stroke="{MED}"'
          f' stroke-width="{8*s_:.0f}"/>')
    s += '</g>'
    return s + '</g>'


def _podkova_rzh(x, y, s_=1.0, t=0.0, kach=0.0):
    """Ржавая подкова: кольцо с ВЫРЕЗАННОЙ серединой и широким разрывом внизу
    (evenodd), пятки с шипами, гнёзда под гвозди, наклон. Дуга обводкой всё
    ещё читалась радугой — теперь это настоящее кольцо с дыркой."""
    rnd = random.Random(int(x) + 7)
    R, w_ = 118 * s_, 50 * s_
    ro, ri = R + w_ / 2, R - w_ / 2
    ug = kach - 22 + 3.0 * A.w(t, 1.8, x * .001)
    oy_ = y + R * .42                    # уровень, где подкова разомкнута
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    d = (f'M{x-ro:.0f},{oy_:.0f} A{ro:.0f},{ro:.0f} 0 1 1 {x+ro:.0f},{oy_:.0f}'
         f' L{x+ri:.0f},{oy_:.0f} A{ri:.0f},{ri:.0f} 0 1 0 {x-ri:.0f},{oy_:.0f} Z')
    s += f'<path d="{d}" fill="#9c5a24" fill-rule="evenodd" {o(max(4, 7*s_))}/>'
    s += (f'<path d="M{x-R:.0f},{oy_:.0f} A{R:.0f},{R:.0f} 0 1 1 {x+R:.0f},{oy_:.0f}"'
          f' fill="none" stroke="#c07a3a" stroke-width="{w_*.30:.0f}"'
          f' opacity=".7"/>')
    for i in range(7):                   # гнёзда под гвозди
        a = math.radians(196 + i * 24.6)
        s += (f'<ellipse cx="{x+R*math.cos(a):.0f}" cy="{y-R*math.sin(a):.0f}"'
              f' rx="{7*s_:.0f}" ry="{10*s_:.0f}" fill="#3a2110"'
              f' {o(max(2, 3*s_))}/>')
    for i in (-1, 1):                    # пятки с шипами ниже разрыва
        s += (f'<path d="M{x+i*ri:.0f},{oy_-4*s_:.0f} h{i*w_:.0f}'
              f' l{-i*w_*.18:.0f},{w_*.76:.0f} h{-i*w_*.64:.0f} Z"'
              f' fill="#7a4418" {o(max(3, 5*s_))}/>')
    for i in range(18):                  # рыжие потёки
        a = rnd.uniform(3.3, 6.1)
        rr = R + rnd.uniform(-w_ * .32, w_ * .32)
        s += (f'<circle cx="{x+math.cos(a)*rr:.0f}" cy="{y-math.sin(a)*rr:.0f}"'
              f' r="{rnd.uniform(5,12)*s_:.0f}" fill="#b5651d" opacity=".55"/>')
    bl = .25 + .3 * (0.5 + 0.5 * A.w(t, 2.4))
    s += (f'<path d="M{x-R*.70:.0f},{y-R*.62:.0f} a{R*.95:.0f},{R*.95:.0f} 0 0 1'
          f' {R*.56:.0f},{-R*.26:.0f}" fill="none" stroke="#f0c088"'
          f' stroke-width="{9*s_:.0f}" opacity="{bl:.2f}"/>')
    s += '</g>'
    for i in (-1, 1):
        s += (f'<circle cx="{x+i*R*.52:.0f}" cy="{y-R*.80:.0f}" r="{13*s_:.0f}"'
              f' fill="#8d949b" {o(max(3, 4*s_))}/>')
        s += (f'<circle cx="{x+i*R*.52-4*s_:.0f}" cy="{y-R*.84:.0f}"'
              f' r="{5*s_:.0f}" fill="#e8eef6" opacity=".7"/>')
    return s


def _vihr(x, y, s_=1.0, t=0.0, lico=True):
    """Вихрь с хитрой рожицей: воронка из витков, листья и сор кружатся."""
    rot = (t * 110) % 360
    s = f'<g transform="rotate({rot*.06:.1f} {x:.0f} {y:.0f})">'
    for i in range(7):                   # витки воронки
        rr = (40 + i * 46) * s_
        fz = i * .18 + t * .5
        s += (f'<ellipse cx="{x+14*s_*A.w(t,1.6,i*.2):.0f}" cy="{y-i*52*s_:.0f}"'
              f' rx="{rr:.0f}" ry="{rr*.30:.0f}" fill="none" stroke="#cfd6de"'
              f' stroke-width="{(16-i):.0f}" opacity="{.75-i*.07:.2f}"'
              f' stroke-dasharray="{60+i*20:.0f} {30+i*8:.0f}"'
              f' stroke-dashoffset="{fz*120:.0f}"/>')
    for i in range(12):                  # сор и листья летят по спирали
        a = t * 2.4 + i * .52
        rr = (60 + (i % 4) * 60) * s_
        s += (f'<path d="M{x+math.cos(a)*rr:.0f},{y-((i*41)%320)*s_:.0f}'
              f' l{10*s_:.0f},{-14*s_:.0f} l{8*s_:.0f},{12*s_:.0f} Z"'
              f' fill="{"#a8641e" if i % 3 else "#6b5a3a"}" opacity=".85"/>')
    if lico:                             # голова-облако под рожицей
        s += (f'<ellipse cx="{x:.0f}" cy="{y-190*s_:.0f}" rx="{104*s_:.0f}"'
              f' ry="{84*s_:.0f}" fill="#e6edf5" opacity=".9" {o(5)}/>')
        s += _rozhica(x, y - 190 * s_, 78 * s_, t, .1, True, "#3a3f48")
    return s + '</g>'


def _mol(x, y, s_=1.0, t=0.0, ph=.0):
    """Наглая моль с салфеткой на шее: пыльные крылья, усики, глазки."""
    w_ = 56 * s_
    fl = A.w(t, .22, ph)
    s = f'<g transform="translate(0,{6*A.w(t,.5,ph):.1f})">'
    for i in (-1, 1):                    # крылья машут
        s += (f'<g transform="rotate({i*fl*26:.1f} {x:.0f} {y:.0f})">'
              f'<ellipse cx="{x+i*w_*.52:.0f}" cy="{y-w_*.10:.0f}" rx="{w_*.56:.0f}"'
              f' ry="{w_*.30:.0f}" fill="#cdbfa2" opacity=".9" {o(max(2, 3*s_))}/>'
              f'<ellipse cx="{x+i*w_*.62:.0f}" cy="{y-w_*.06:.0f}" rx="{w_*.22:.0f}"'
              f' ry="{w_*.12:.0f}" fill="#a79a80" opacity=".7"/></g>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_*.22:.0f}" ry="{w_*.42:.0f}"'
          f' fill="#8d8371" {o(max(2, 3*s_))}/>')
    s += (f'<circle cx="{x:.0f}" cy="{y-w_*.46:.0f}" r="{w_*.21:.0f}" fill="#a3998a"'
          f' {o(max(2, 3*s_))}/>')
    for i in (-1, 1):
        if not A.blink(t, 2.8, ph):
            s += (f'<circle cx="{x+i*w_*.09:.0f}" cy="{y-w_*.48:.0f}"'
                  f' r="{w_*.055:.0f}" fill="{K}"/>')
        s += (f'<path d="M{x+i*w_*.10:.0f},{y-w_*.60:.0f} q{i*w_*.22:.0f},{-w_*.26:.0f}'
              f' {i*w_*.34:.0f},{-w_*.14+3*A.w(t,1.3,ph+i*.2):.0f}" fill="none"'
              f' stroke="#6b645c" stroke-width="{max(2, 4*s_):.0f}"/>')
    s += (f'<path d="M{x-w_*.20:.0f},{y-w_*.30:.0f} q{w_*.20:.0f},{w_*.16:.0f}'
          f' {w_*.40:.0f},0 l{-w_*.14:.0f},{w_*.30:.0f} q{-w_*.12:.0f},{w_*.06:.0f}'
          f' {-w_*.14:.0f},0 Z" fill="#f2efe6" {o(max(2, 3*s_))}/>')
    return s + '</g>'


def _komar(x, y, s_=1.0, t=0.0, ph=.0, chemodan=True):
    """Комар-путешественник: длинный хоботок, дрожащие крылья, шесть ног,
    ПОЛОСАТЫЙ ШАРФ с развевающимся концом и саквояж с дужкой."""
    w_ = 60 * s_
    sh = 5 * s_ * A.w(t, .7, ph)
    s = f'<g transform="translate({sh:.1f},{2*A.w(t,.9,ph):.1f})">'
    for i in range(6):                   # шесть ног, переступают
        sgn = -1 if i < 3 else 1
        st = 12 * s_ * A.w(t, .62, ph + i * .17)
        s += (f'<path d="M{x+sgn*w_*.2:.0f},{y-w_*.3:.0f}'
              f' q{sgn*w_*.5:.0f},{-w_*.2:.0f} {sgn*w_*.74+st:.0f},{w_*.46:.0f}"'
              f' fill="none" stroke="#3f4650" stroke-width="{max(3, 7*s_):.0f}"'
              f' stroke-linecap="round"/>')
    for i in (-1, 1):                    # крылья дрожат
        s += (f'<ellipse cx="{x+i*w_*.34:.0f}" cy="{y-w_*.78:.0f}"'
              f' rx="{w_*.50:.0f}"'
              f' ry="{w_*(.12+.07*abs(A.w(t,.12,ph))):.1f}" fill="#dfeaf2"'
              f' opacity=".6" {o(3)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-w_*.40:.0f}" rx="{w_*.46:.0f}"'
          f' ry="{w_*.26:.0f}" fill="#4a5260" {o(max(3, 5*s_))}/>')
    for i in range(4):                   # сегменты брюшка
        s += (f'<path d="M{x-w_*.30+i*w_*.18:.0f},{y-w_*.60:.0f}'
              f' q{w_*.03:.0f},{w_*.20:.0f} 0,{w_*.38:.0f}" fill="none"'
              f' stroke="#394150" stroke-width="{max(2, 5*s_):.0f}"'
              f' opacity=".7"/>')
    s += (f'<circle cx="{x+w_*.50:.0f}" cy="{y-w_*.58:.0f}" r="{w_*.22:.0f}"'
          f' fill="#5a6272" {o(max(2, 4*s_))}/>')
    s += (f'<path d="M{x+w_*.66:.0f},{y-w_*.50:.0f} l{w_*.50:.0f},{w_*.18:.0f}"'
          f' stroke="#2f3337" stroke-width="{max(3, 6*s_):.0f}"'
          f' stroke-linecap="round"/>')
    if not A.blink(t, 3.0, ph):
        s += (f'<circle cx="{x+w_*.54:.0f}" cy="{y-w_*.64:.0f}"'
              f' r="{w_*.08:.0f}" fill="#f2efe6"/>')
        s += (f'<circle cx="{x+w_*.56:.0f}" cy="{y-w_*.64:.0f}"'
              f' r="{w_*.04:.0f}" fill="{K}"/>')
    # ШАРФ: обмотка вокруг шеи и длинный конец, полосами
    s += (f'<path d="M{x+w_*.20:.0f},{y-w_*.40:.0f} q{w_*.20:.0f},{w_*.16:.0f}'
          f' {w_*.42:.0f},{w_*.04:.0f} l{w_*.02:.0f},{w_*.18:.0f}'
          f' q{-w_*.26:.0f},{w_*.12:.0f} {-w_*.48:.0f},{-w_*.04:.0f} Z"'
          f' fill="{TKAN}" {o(max(2, 4*s_))}/>')
    vey = w_ * .12 * A.w(t, .8, ph)
    s += (f'<path d="M{x+w_*.22:.0f},{y-w_*.26:.0f}'
          f' q{-w_*.30:.0f},{w_*.30+vey:.0f} {-w_*.76:.0f},{w_*.40:.0f}'
          f' l{-w_*.04:.0f},{-w_*.22:.0f} q{w_*.40:.0f},{-w_*.10:.0f}'
          f' {w_*.66:.0f},{-w_*.34:.0f} Z" fill="{TKAN}" {o(max(2, 4*s_))}/>')
    for i in range(3):                   # полоски на шарфе
        s += (f'<line x1="{x-w_*.10-i*w_*.18:.0f}" y1="{y-w_*.06+i*w_*.05:.0f}"'
              f' x2="{x-w_*.06-i*w_*.18:.0f}" y2="{y+w_*.14+i*w_*.04:.0f}"'
              f' stroke="#f2efe6" stroke-width="{max(2, 5*s_):.0f}"'
              f' opacity=".9"/>')
    if chemodan:                         # саквояж с дужкой и замком
        bx_, by_ = x - w_ * .92, y - w_ * .04
        s += (f'<path d="M{bx_-w_*.30:.0f},{by_:.0f} h{w_*.60:.0f}'
              f' q{w_*.06:.0f},{w_*.30:.0f} {-w_*.03:.0f},{w_*.42:.0f}'
              f' h{-w_*.54:.0f} q{-w_*.09:.0f},{-w_*.12:.0f}'
              f' {-w_*.03:.0f},{-w_*.42:.0f} Z" fill="#8a5a2a"'
              f' {o(max(3, 5*s_))}/>')
        s += (f'<path d="M{bx_-w_*.18:.0f},{by_-w_*.02:.0f}'
              f' q{w_*.18:.0f},{-w_*.26:.0f} {w_*.36:.0f},0" fill="none"'
              f' stroke="#5e3a16" stroke-width="{max(3, 6*s_):.0f}"/>')
        s += (f'<rect x="{bx_-w_*.32:.0f}" y="{by_+w_*.12:.0f}"'
              f' width="{w_*.64:.0f}" height="{w_*.08:.0f}" fill="{ZOL}"'
              f' opacity=".9"/>')
        s += (f'<rect x="{bx_-w_*.05:.0f}" y="{by_-w_*.04:.0f}"'
              f' width="{w_*.10:.0f}" height="{w_*.12:.0f}" rx="{w_*.02:.0f}"'
              f' fill="{ZOL}" {o(2)}/>')
    return s + '</g>'


def _sekator(x, y, s_=1.0, t=0.0, szhat=0.0, ug=0.0):
    """Садовые ножницы-секатор: два лезвия сходятся в точке x,y, за шарниром
    две КРАСНЫЕ ПЕТЛИ-рукоятки. Петли — главный признак, по ним ножницы и
    узнают (прежние прямые бруски читались палками)."""
    raz = 13 * (1 - szhat)
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    for i, sgn in ((0, -1), (1, 1)):
        a = sgn * raz
        s += f'<g transform="rotate({a:.1f} {x:.0f} {y:.0f})">'
        s += (f'<path d="M{x:.0f},{y:.0f} q{-46*s_:.0f},{sgn*6*s_:.0f}'
              f' {-92*s_:.0f},{sgn*18*s_:.0f} l{-6*s_:.0f},{-sgn*18*s_:.0f}'
              f' q{46*s_:.0f},{-sgn*10*s_:.0f} {96*s_:.0f},{-sgn*4*s_:.0f} Z"'
              f' fill="#e8eef4" {o(max(3, 4*s_))}/>')
        s += (f'<rect x="{x-152*s_:.0f}" y="{y+sgn*22*s_-11*s_:.0f}"'
              f' width="{64*s_:.0f}" height="{22*s_:.0f}" rx="{11*s_:.0f}"'
              f' fill="{KRAS}" {o(max(2, 4*s_))}/>')
        s += (f'<ellipse cx="{x-192*s_:.0f}" cy="{y+sgn*34*s_:.0f}"'
              f' rx="{44*s_:.0f}" ry="{32*s_:.0f}" fill="none" stroke="{KRAS}"'
              f' stroke-width="{20*s_:.0f}"/>')
        s += (f'<ellipse cx="{x-192*s_:.0f}" cy="{y+sgn*34*s_:.0f}"'
              f' rx="{44*s_:.0f}" ry="{32*s_:.0f}" fill="none" stroke="{K}"'
              f' stroke-width="{4*s_:.0f}"/>')
        s += '</g>'
    s += (f'<circle cx="{x-96*s_:.0f}" cy="{y+10*s_:.0f}" r="{14*s_:.0f}"'
          f' fill="#8d949b" {o(max(2, 3*s_))}/>')
    s += (f'<circle cx="{x-96*s_:.0f}" cy="{y+10*s_:.0f}" r="{5*s_:.0f}"'
          f' fill="#3f454a"/>')
    bl = .3 + .4 * abs(A.w(t, 2.0))
    s += (f'<line x1="{x-12*s_:.0f}" y1="{y-6*s_:.0f}" x2="{x-64*s_:.0f}"'
          f' y2="{y-16*s_:.0f}" stroke="#ffffff" stroke-width="{5*s_:.0f}"'
          f' opacity="{bl:.2f}"/>')
    return s + '</g>'


def _busy(x, y, n, t, s_=1.0, ph=.0, dl=1.0):
    """Бусы из рябины на суровой нитке: провисают дугой, ягоды качаются."""
    s = ""
    w_ = 300 * s_ * dl
    for i in range(n):
        p = i / max(1, n - 1)
        bx = x - w_ / 2 + p * w_
        by = y + math.sin(p * 3.14159) * 90 * s_ * dl + 4 * A.w(t, 1.8, ph + p)
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{11*s_:.0f}"'
              f' fill="{"#8e2a1c" if i % 5 == 0 else KRAS}" {o(max(2, 3*s_))}/>')
        s += (f'<circle cx="{bx-3*s_:.0f}" cy="{by-4*s_:.0f}" r="{3.4*s_:.1f}"'
              f' fill="#ffd0b0" opacity=".6"/>')
    s += (f'<path d="M{x-w_/2:.0f},{y:.0f} q{w_/2:.0f},{120*s_*dl:.0f} {w_:.0f},0"'
          f' fill="none" stroke="#d8cbb0" stroke-width="{max(2, 4*s_):.0f}"'
          f' opacity=".8"/>')
    return s


def _shkaf(x, y, w_, h_, t, open_=0.0, zerkalo=False):
    """Платяной шкаф: две дверцы, одна приоткрыта, ручки, карниз."""
    s = ten(x + w_ / 2, y + h_ + 12, w_ * .5, 18, .5)
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8"'
          f' fill="#3a2b1d" {o(8)}/>')
    s += (f'<rect x="{x-14:.0f}" y="{y-34:.0f}" width="{w_+28:.0f}" height="38" rx="8"'
          f' fill="url(#derev)" {o(7)}/>')
    s += (f'<rect x="{x+w_*.02:.0f}" y="{y+6:.0f}" width="{w_*.47:.0f}"'
          f' height="{h_-12:.0f}" rx="6" fill="url(#derev)" {o(6)}/>')
    pv = x + w_ * .51                   # створка открывается от своей кромки
    s += (f'<g transform="translate({pv:.0f},0) scale({1-open_*.62:.3f},1)'
          f' translate({-pv:.0f},0)">'
          f'<rect x="{pv:.0f}" y="{y+6:.0f}" width="{w_*.47:.0f}"'
          f' height="{h_-12:.0f}" rx="6" fill="url(#derev)" {o(6)}/></g>')
    if zerkalo:
        s += (f'<rect x="{x+w_*.08:.0f}" y="{y+h_*.08:.0f}" width="{w_*.35:.0f}"'
              f' height="{h_*.56:.0f}" rx="6" fill="url(#stekl)" opacity=".6" {o(4)}/>')
        s += (f'<path d="M{x+w_*.12:.0f},{y+h_*.52:.0f} l{w_*.22:.0f},{-h_*.36:.0f}"'
              f' stroke="#ffffff" stroke-width="16"'
              f' opacity="{.16+.1*abs(A.w(t,3.0)):.2f}"/>')
    for i, px in ((0, x + w_ * .44),
                  (1, x + w_ * .51 + w_ * .47 * (1 - open_ * .62) - w_ * .03)):
        s += (f'<ellipse cx="{px:.0f}" cy="{y+h_*.5:.0f}" rx="9" ry="22"'
              f' fill="url(#zhel)" {o(3)}/>')
    return s


def _veshalka(x, y, w_, t, kryuchkov=5, odezhda=True):
    """Вешалка в прихожей: планка, крючки, на них пальто и шарф."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="34" rx="8"'
         f' fill="url(#derev)" {o(7)}/>')
    for i in range(kryuchkov):
        hx = x + 40 + i * (w_ - 80) / max(1, kryuchkov - 1)
        s += (f'<path d="M{hx:.0f},{y+34:.0f} l0,26 q0,16 16,16" fill="none"'
              f' stroke="#8d949b" stroke-width="11" stroke-linecap="round"/>')
        s += (f'<circle cx="{hx:.0f}" cy="{y+17:.0f}" r="7" fill="#5d6168"/>')
    if odezhda:
        for i, (ox_, col, ww) in enumerate(((.22, "#3f4a5e", 150),
                                            (.56, "#5b2f3a", 130))):
            hx = x + w_ * ox_
            kach = 1.8 * A.w(t, 2.6, i * .3)
            s += (f'<g transform="rotate({kach:.2f} {hx:.0f} {y+60:.0f})">'
                  f'<path d="M{hx-ww*.5:.0f},{y+104:.0f} q{ww*.16:.0f},{-44:.0f}'
                  f' {ww*.5:.0f},{-44:.0f} q{ww*.34:.0f},0 {ww*.5:.0f},{44:.0f}'
                  f' l{ww*.08:.0f},{250:.0f} q{-ww*.58:.0f},{26:.0f} {-ww*1.16:.0f},0 Z"'
                  f' fill="{col}" {o(6)}/>'
                  f'<path d="M{hx:.0f},{y+66:.0f} l0,{250:.0f}" stroke="{K}"'
                  f' stroke-width="4" opacity=".5"/></g>')
        sh = x + w_ * .82
        s += (f'<path d="M{sh:.0f},{y+54:.0f} q{-34:.0f},{90+6*A.w(t,2.2):.0f}'
              f' {-16:.0f},{200:.0f} l{44:.0f},{10:.0f} q{-10:.0f},{-110:.0f}'
              f' {10:.0f},{-196:.0f} Z" fill="{TKAN}" {o(5)}/>')
    return s


# ── 69 ─────────────────────────────────────────────────────────────────────
def rzhavaya_podkova_na_dachnoy_dveri(t):
    """Дверь дачного домика с облупленной голубой краской, над ней ОГРОМНАЯ
    ржавая подкова на двух гвоздях. Дед держит внука у себя на плечах, тот
    трогает подкову и смотрит на рыжий от ржавчины палец."""
    rnd = random.Random(6911)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 691)
    s += oblaka(t, 150, 4, 701, .3, "#c6d2e0", 14.0)
    s += SL(Z_DAL, goloe_derevo(180, 840, 480, t, 709, 7, "#363844"))
    s += SL(Z_DAL, pleten(1560, 880, 360, 190, 7))
    s += SL(Z_DAL, gryaz_polosa(820, 170, "#4f4a40"))
    # стена дачи во всю ширину: голубые доски с проплешинами краски
    st = doski(60, 60, 1800, 1020, 96, True, "dosk")
    st += f'<rect x="60" y="60" width="1800" height="1020" fill="#7ea2b6" opacity=".8"/>'
    for i in range(34):
        px, py = 80 + rnd.random() * 1760, 100 + rnd.random() * 940
        st += (f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{rnd.uniform(20,62):.0f}"'
               f' ry="{rnd.uniform(12,40):.0f}" fill="#ad7f4f" opacity=".88"/>')
    st += f'<path d="M20,120 L960,-170 L1900,120 Z" fill="#55493c" opacity=".96" {o(9)}/>'
    s += SL(Z_DAL, st)
    # ДВЕРЬ в центре и ПОДКОВА над ней — крупно
    dx, dy, dw, dh = 660, 430, 620, 650
    dv = (f'<rect x="{dx-30}" y="{dy-30}" width="{dw+60}" height="{dh+30}" rx="10"'
          f' fill="url(#derev)" {o(9)}/>')
    dv += dver(dx, dy, dw, dh, 0.0, "#5f88a0", True, False)
    for i in range(26):                  # шелушинки краски на двери
        px, py = dx + 30 + rnd.random() * (dw - 60), dy + 40 + rnd.random() * (dh - 80)
        dv += (f'<path d="M{px:.0f},{py:.0f} q{rnd.uniform(10,28):.0f},-10'
               f' {rnd.uniform(22,50):.0f},{rnd.uniform(5,18):.0f}'
               f' q{-rnd.uniform(12,24):.0f},13 {-rnd.uniform(24,52):.0f},0 Z"'
               f' fill="#a67a4e" opacity=".92"/>')
    dv += (f'<rect x="{dx+dw*.12:.0f}" y="{dy+dh*.10:.0f}" width="{dw*.76:.0f}"'
           f' height="{dh*.30:.0f}" rx="8" fill="none" stroke="#3f5e70"'
           f' stroke-width="14" opacity=".85"/>')
    dv += (f'<ellipse cx="{dx+dw-70:.0f}" cy="{dy+dh*.52:.0f}" rx="24" ry="34"'
           f' fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, dv)
    s += SL(Z_SRED, f'<path d="M{dx-130},{dy-44} h{dw+260} l-70,-70 h{-dw-120} Z"'
                    f' fill="{DOSKA2}" {o(9)}/>')
    px_, py_ = dx + dw / 2, dy - 210
    s += SL(Z_SRED, _podkova_rzh(px_, py_, 1.3, t,
                                 7 * A.ease(A.seg(t, 2.6, .6)) * A.w(t, .8)))
    # лампочка над крыльцом: тёплое пятно на двери и подкове
    flx, fly = dx + dw + 190, dy - 90
    s += SL(Z_SRED, f'<rect x="{flx-12:.0f}" y="{fly-170:.0f}" width="24"'
                    f' height="80" rx="8" fill="#3a3f46" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{flx-80:.0f},{fly-90:.0f} h160 l-22,-52 h-116 Z"'
                    f' fill="#2f3337" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{flx-66:.0f},{fly-90:.0f} h132 l-14,170 h-104 Z"'
                    f' fill="url(#stekl)" opacity=".7" {o(6)}/>')
    s += SL(Z_SRED, ogon(flx, fly + 40, t, .95, .2, 5))
    s += SL(Z_SRED, f'<path d="M{flx-76:.0f},{fly+82:.0f} h152 l16,38 h-184 Z"'
                    f' fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, teplo(flx - 60, fly + 60, 1000, 840,
                          .5 + .12 * abs(A.w(t, 1.6))))
    # дед держит внука на плечах, внук тянется к подкове
    pod = A.ease(A.seg(t, .4, 1.6))
    gx = px_ - 40
    s += SL(Z_SRED, figura(gx, 1076, 540, t, "#3a3a46", "#ffd0a0", False, .2,
                           False, 1.0, True, 1.0, True))
    s += SL(Z_SRED, para_izo_rta(gx + 70, 700, t, .2, 1.2, .55))
    # дед поднимает внука НА РУКАХ, сбоку от себя — так читаются оба
    ruk0, (hx0, hy0) = rukav(gx + 120, 790, 180, -52, t, "#3a3a46", "#ffd0a0",
                             .1, 3.0)
    s += SL(Z_SRED, ruk0)
    vy = 790 - pod * 150
    s += SL(Z_SRED, figura(gx + 250, vy, 330, t, "#6b3a44", "#ffd0a0", False, .55,
                           False, 1.0, False, 1.4, False, True))
    ruk, (kx, ky) = rukav(gx + 290, vy - 260, 130, -68 + 8 * A.w(t, 1.2), t,
                          "#6b3a44", "#ffd0a0", .4, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="30" ry="23"'
                    f' fill="#6b3a44" {o(5)}/>')
    if pod > .85:                        # палец рыжий от ржавчины
        s += SL(Z_SRED, f'<ellipse cx="{kx+6:.0f}" cy="{ky-14:.0f}" rx="18"'
                        f' ry="14" fill="#a86a3a"'
                        f' opacity="{.5+.45*abs(A.w(t,1.4)):.2f}"/>')
    for i in range(10):                  # чешуйки краски сыплются вниз
        k = ((t * .5) + i * .1) % 1.0
        s += SL(Z_LETIT, f'<path d="M{dx+60+i*62:.0f},{dy+140+k*560:.0f}'
                         f' l18,-8 l7,14 Z" fill="#a9c6d6"'
                         f' opacity="{.9*(1-k):.2f}"/>')
    s += SL(Z_SRED, _valenok(400, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_SRED, _valenok(510, 1012, .86, t, .6, True, "#6e6358"))
    s += SL(Z_SRED, _vedro_dach(1620, 1012, 1.2, t))
    s += SL(Z_PERED, f'<rect x="120" y="340" width="100" height="740" rx="10"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_PERED, f'<path d="M80,350 h190 l-26,-64 h-140 Z" fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_PERED, grozd_ryabiny(1790, 460, t, 1.7, 16, 733, .2))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 739, .45, .9))
    s += vinetka(.44)
    return s


# ── 70 ─────────────────────────────────────────────────────────────────────
def ryabinovye_busy_na_nitke(t):
    """Осеннее крыльцо: посреди него большая миска рябины, две девочки нижут
    ягоды толстой иглой на суровую нитку, готовые бусы висят дугой."""
    rnd = random.Random(7013)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 743)
    s += oblaka(t, 180, 4, 751, .3, "#cbd6e2", 15.0)
    s += ulica_dal(1300, 690, 640, t, False, 757)
    s += SL(Z_DAL, goloe_derevo(140, 840, 470, t, 761, 7, "#363844"))
    s += SL(Z_DAL, gryaz_polosa(820, 180, "#4f4a40"))
    st = brevna(200, 0, 1540, 870, 112)
    st += f'<rect x="200" y="0" width="1540" height="870" fill="#9c7049" opacity=".3"/>'
    st += f'<path d="M160,40 L970,-220 L1780,40 Z" fill="#55493c" opacity=".95" {o(9)}/>'
    s += SL(Z_DAL, st)
    # окно сеней с лампой за стеклом — тёплое пятно
    s += SL(Z_DAL, okno_izby(1330, 160, 330, 260, t, svet=True, moroz=.15))
    s += SL(Z_DAL, lampa(1490, 400, t, .7))
    s += SL(Z_DAL, teplo(1490, 300, 560, 470, .46 + .1 * abs(A.w(t, 1.8))))
    s += SL(Z_SRED, dver(300, 270, 420, 610, 0.0, "url(#derev)", True, False))
    s += SL(Z_SRED, f'<rect x="170" y="880" width="1620" height="56" rx="10"'
                    f' fill="url(#dosk)" {o(9)}/>')
    s += SL(Z_SRED, polovicy(936, "url(#pol)"))
    s += SL(Z_SRED, lavka(700, 880, 480))
    # МИСКА РЯБИНЫ в центре, крупно
    mx, my = 940, 900
    ms = (f'<path d="M{mx-270:.0f},{my-190:.0f} q0,200 {270:.0f},202'
          f' q{270:.0f},-2 {270:.0f},-202 Z" fill="url(#glina)" {o(10)}/>')
    ms += (f'<ellipse cx="{mx:.0f}" cy="{my-190:.0f}" rx="270" ry="50"'
           f' fill="#9c6a3c" {o(7)}/>')
    ms += (f'<path d="M{mx-230:.0f},{my-140:.0f} q50,70 150,92" fill="none"'
           f' stroke="#e0b183" stroke-width="14" opacity=".5"/>')
    for i in range(60):                  # ягоды горкой, часть уже тёмная
        a = rnd.uniform(0, 6.283)
        rr = rnd.uniform(0, 1) ** .5 * 246
        bx, by = mx + math.cos(a) * rr, my - 196 + math.sin(a) * rr * .24
        tem = A.ease(A.seg(t, 1.6 + (i % 7) * .22, 1.2))
        col = "#8e2a1c" if (i % 5 == 0 or tem > .7) else KRAS
        ms += (f'<circle cx="{bx:.0f}" cy="{by+4*A.w(t,2.0,i*.07):.0f}"'
               f' r="{16-2.5*tem:.1f}" fill="{col}" {o(2)}/>')
        if i % 3 == 0:
            ms += (f'<circle cx="{bx-5:.0f}" cy="{by-6:.0f}" r="5"'
                   f' fill="#ffd0b0" opacity="{.6-.3*tem:.2f}"/>')
    s += SL(Z_SRED, ms)
    # девочки по сторонам миски
    s += SL(Z_SRED, figura(470, 1020, 470, t, "#5b2f3a", "#ffd0a0", False, .3,
                           False, 1.0, False, 1.4, False, False))
    s += SL(Z_SRED, figura(1480, 1024, 460, t, "#2e4a5a", "#ffd0a0", True, .65,
                           False, 1.0, False, 1.2))
    s += SL(Z_SRED, para_izo_rta(516, 740, t, .3, 1.0, .5))
    s += SL(Z_SRED, para_izo_rta(1520, 748, t, .7, 1.0, .5))
    # рукав девочки заканчивается НАД миской, в нём игла с нитью
    sh = A.w(t, .9, .1)
    ruk, (ix, iy) = rukav(560, 740, 150, 34 + 14 * sh, t, "#5b2f3a", "#ffd0a0",
                          .1, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{ix:.0f}" cy="{iy:.0f}" rx="32" ry="24"'
                    f' fill="#5b2f3a" {o(5)}/>')
    igl = (f'<line x1="{ix+18:.0f}" y1="{iy+6:.0f}" x2="{ix+190:.0f}"'
           f' y2="{iy+54+16*sh:.0f}" stroke="#cfd6dc" stroke-width="13"'
           f' stroke-linecap="round"/>')
    igl += (f'<ellipse cx="{ix+26:.0f}" cy="{iy+8:.0f}" rx="16" ry="11"'
            f' fill="none" stroke="#8d949b" stroke-width="7"/>')
    igl += (f'<circle cx="{ix+150:.0f}" cy="{iy+44+13*sh:.0f}" r="9"'
            f' fill="#ffffff" opacity="{.4+.5*abs(A.w(t,1.6)):.2f}"/>')
    igl += (f'<circle cx="{ix+192:.0f}" cy="{iy+56+16*sh:.0f}" r="20"'
            f' fill="{KRAS}" {o(4)}/>')
    igl += (f'<path d="M{ix+26:.0f},{iy+10:.0f} q-70,90 -170,130" fill="none"'
            f' stroke="#e2d6bc" stroke-width="6" opacity=".9"/>')
    s += SL(Z_SRED, igl)
    # бусы растут и девочки ими меряются
    rost = A.ease(A.seg(t, .3, 3.2))
    s += SL(Z_SRED, _busy(700, 700, int(8 + 16 * rost), t, 1.7, .2, .5 + .7 * rost))
    s += SL(Z_SRED, _busy(1450, 690, int(6 + 10 * rost), t, 1.35, .5,
                          .4 + .5 * rost))
    ruk2, (jx, jy) = rukav(1400, 760, 150, 182 - 18 * A.w(t, 1.1, .4), t,
                           "#2e4a5a", "#ffd0a0", .4, 5.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{jx:.0f}" cy="{jy:.0f}" rx="30" ry="22"'
                    f' fill="#2e4a5a" {o(5)}/>')
    s += SL(Z_SRED, _korzina_ryab(1740, 1012, 240, 170, t, 769))
    s += SL(Z_SRED, kura(1660, 1012, t, .9, .4))
    s += SL(Z_PERED, grozd_ryabiny(150, 320, t, 1.9, 17, 773, .1))
    s += SL(Z_PERED, f'<rect x="1810" y="150" width="110" height="930" rx="12"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 787, .4, .85))
    s += vinetka(.42)
    return s


def _korzina_ryab(x, y, w_, h_, t, seed=7):
    """Корзинка с рябиновыми кистями: лоза, дужка, ягоды горкой."""
    rnd = random.Random(seed)
    s = ten(x, y + 10, w_ * .52, 15, .45)
    s += (f'<path d="M{x-w_/2:.0f},{y-h_:.0f} L{x+w_/2:.0f},{y-h_:.0f}'
          f' L{x+w_*.36:.0f},{y:.0f} L{x-w_*.36:.0f},{y:.0f} Z" fill="url(#solom)" {o(6)}/>')
    for i in range(5):
        yy = y - h_ + 16 + i * (h_ - 24) / 4
        kk = (w_ / 2) * (1 - .26 * (i / 4))
        d = f'M{x-kk:.0f},{yy:.0f}'
        for j in range(5):
            xx = x - kk + j * (kk * 2 / 5)
            d += (f' Q{xx+kk/5:.0f},{yy+(10 if j % 2 == 0 else -10):.0f}'
                  f' {xx+kk*2/5:.0f},{yy:.0f}')
        s += f'<path d="{d}" fill="none" stroke="#b78a46" stroke-width="8"/>'
    for i in range(16):
        bx = x + rnd.uniform(-w_ * .42, w_ * .42)
        by = y - h_ - rnd.uniform(-6, 26)
        s += (f'<circle cx="{bx:.0f}" cy="{by+3*A.w(t,2.2,i*.09):.0f}" r="11"'
              f' fill="{KRAS if i % 4 else "#8e2a1c"}" {o(2)}/>')
    duga = 2.6 * A.w(t, 3.0, seed * .05)
    s += (f'<g transform="rotate({duga:.2f} {x:.0f} {y-h_+2:.0f})">'
          f'<path d="M{x-w_*.40:.0f},{y-h_*.98:.0f} q{w_*.40:.0f},{-h_*.76:.0f}'
          f' {w_*.80:.0f},{-h_*.01:.0f}" fill="none" stroke="#9a7238"'
          f' stroke-width="13"/></g>')
    return s


# ── 71 ─────────────────────────────────────────────────────────────────────
def grozd_ryabiny_u_svoego_krylca(t):
    """Крыльцо дачного дома с горящим фонарём: женщина в куртке срезает
    секатором тяжёлую гроздь рябины у забора и вешает её на гвоздь у двери,
    пёс нюхает упавшие ягоды."""
    rnd = random.Random(7121)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 797)
    s += oblaka(t, 150, 5, 809, .28, "#c2cfdd", 16.0)
    s += SL(Z_DAL, ulica_dal(40, 640, 760, t, False, 811))
    s += SL(Z_DAL, gryaz_polosa(790, 200, "#4a463c"))
    s += SL(Z_DAL, pleten(60, 790, 560, 200, 9))
    # стена дачного дома во всю ширину, крыльцо под навесом
    dom = doski(0, 60, 1920, 1020, 92, True, "dosk")
    dom += f'<rect x="0" y="60" width="1920" height="1020" fill="#8a9aa2" opacity=".5"/>'
    dom += f'<path d="M-40,130 L960,-150 L1960,130 Z" fill="#50483e" opacity=".96" {o(9)}/>'
    s += SL(Z_DAL, dom)
    dx, dy, dw, dh = 1320, 390, 470, 690
    s += SL(Z_SRED, dver(dx, dy, dw, dh, 0.0, "#4a5a46", True, False))
    s += SL(Z_SRED, f'<rect x="{dx+dw*.16:.0f}" y="{dy+dh*.10:.0f}"'
                    f' width="{dw*.68:.0f}" height="{dh*.28:.0f}" rx="8"'
                    f' fill="url(#stekl)" opacity=".5" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{dx-30}" y="{dy-34}" width="{dw+60}" height="34" rx="8"'
                    f' fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="1140" y="1000" width="780" height="50" rx="10"'
                    f' fill="url(#dosk)" {o(9)}/>')
    # фонарь на крыльце: качается и горит
    fk = 3.4 * A.w(t, 2.4, .1)
    fx_, fy_ = dx - 190, dy - 60
    fon = f'<g transform="rotate({fk:.2f} {fx_:.0f} {fy_:.0f})">'
    fon += (f'<line x1="{fx_:.0f}" y1="{fy_:.0f}" x2="{fx_:.0f}" y2="{fy_+90:.0f}"'
            f' stroke="#3a3f46" stroke-width="12"/>')
    fon += (f'<path d="M{fx_-86:.0f},{fy_+100:.0f} h172 l-20,-48 h-132 Z"'
            f' fill="#2f3337" {o(6)}/>')
    fon += (f'<path d="M{fx_-72:.0f},{fy_+100:.0f} h144 l-12,190 h-120 Z"'
            f' fill="url(#stekl)" opacity=".68" {o(6)}/>')
    fon += ogon(fx_, fy_ + 250, t, .85, .2, 5)
    fon += (f'<path d="M{fx_-80:.0f},{fy_+290:.0f} h160 l16,40 h-192 Z"'
            f' fill="#2f3337" {o(6)}/>')
    fon += '</g>'
    s += SL(Z_SRED, fon)
    s += SL(Z_SRED, teplo(fx_, fy_ + 230, 820, 700, .46 + .1 * abs(A.w(t, 1.6))))
    # РЯБИНА У ЗАБОРА и ТЯЖЁЛАЯ ГРОЗДЬ — главный предмет
    s += SL(Z_SRED, goloe_derevo(520, 1010, 720, t, 823, 8, "#443a2c"))
    for i in range(3):
        s += SL(Z_SRED, grozd_ryabiny(300 + i * 70, 400 + (i % 2) * 120, t,
                                      1.1, 13, 827 + i, i * .2))
    srez = A.ease(A.seg(t, .6, 1.0))
    gx, gy = 620, 560
    if srez < .98:
        s += SL(Z_SRED, grozd_ryabiny(gx, gy, t, 4.0, 30, 829, .1))
    s += SL(Z_SRED, f'<path d="M520,860 q{(gx-520)*.5:.0f},{-180:.0f}'
                    f' {gx-500:.0f},{gy-830:.0f}" fill="none" stroke="#5e4428"'
                    f' stroke-width="16"/>')
    s += SL(Z_SRED, _sekator(gx + 300, gy - 110, 1.9, t, srez, -16))
    # женщина рядом с гроздью, рукав короткий и к секатору
    zx = 880
    s += SL(Z_SRED, figura(zx, 1060, 540, t, "#2e4a5a", "#ffd0a0", False, .3,
                           True, 1.0, True, 1.2, False, True))
    ruk, _ = rukav(zx - 120, 730, 190, 206, t, "#2e4a5a", "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, para_izo_rta(zx + 56, 700, t, .2, 1.2, .5))
    # гроздь переезжает на гвоздь у двери
    pere = A.ease(A.seg(t, 2.2, 1.6))
    hx = gx + (dx - 80 - gx) * pere
    hy = gy + (dy + 210 - gy) * pere - math.sin(pere * 3.14159) * 130
    if srez > .5:
        s += SL(Z_SRED, grozd_ryabiny(hx, hy, t, 2.6, 22, 839, .3))
    s += SL(Z_SRED, f'<circle cx="{dx-80:.0f}" cy="{dy+160:.0f}" r="13"'
                    f' fill="#8d949b" {o(4)}/>')
    # пёс нюхает упавшие ягоды
    s += SL(Z_SRED, _pes(1200, 1004, 1.9, t, .4, "#6b5a46"))
    for i in range(9):
        s += SL(Z_SRED, f'<circle cx="{1230+i*26+6*A.w(t,2.2,i*.2):.0f}"'
                        f' cy="{1062+(i%3)*8:.0f}" r="11"'
                        f' fill="{KRAS if i % 3 else "#8e2a1c"}" {o(2)}/>')
    s += SL(Z_SRED, _vedro_dach(1010, 1012, 1.2, t))
    s += SL(Z_SRED, _valenok(1760, 1012, .86, t, .2, True, "#5f6a72"))
    s += SL(Z_PERED, f'<rect x="1176" y="360" width="80" height="720" rx="10"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_PERED, f'<rect x="1856" y="360" width="80" height="720" rx="10"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_PERED, goloe_derevo(80, 1080, 640, t, 853, 7, "#2a2c34"))
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 857, .45, .95))
    s += vinetka(.44)
    return s


def _vedro_dach(x, y, s_=1.0, t=0.0):
    """Садовое ведро: пластиковый конус, ободок, дуга ручки, пара ягод внутри."""
    w1, w2, hh = 70 * s_, 52 * s_, 94 * s_
    kach = 2.2 * A.w(t, 2.0, x * .001)
    s = ten(x, y + 8 * s_, w1 * .9, 11 * s_, .4)
    s += f'<g transform="rotate({kach:.2f} {x:.0f} {y-hh*1.8:.0f})">'
    s += (f'<path d="M{x-w1:.0f},{y-hh:.0f} h{w1*2:.0f}'
          f' L{x+w2:.0f},{y:.0f} h{-w2*2:.0f} Z" fill="#4a6a52" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w1:.0f}" ry="{12*s_:.0f}"'
          f' fill="#3a5742" {o(4)}/>')
    for i in range(7):
        s += (f'<circle cx="{x-w1*.6+i*w1*.2:.0f}" cy="{y-hh+4*s_:.0f}"'
              f' r="{10*s_:.0f}" fill="{KRAS if i % 3 else "#8e2a1c"}"'
              f' opacity=".95"/>')
    s += (f'<path d="M{x-w1:.0f},{y-hh*.96:.0f} q{w1:.0f},{-hh*.72:.0f} {w1*2:.0f},0"'
          f' fill="none" stroke="#2f3337" stroke-width="{7*s_:.0f}"/>')
    s += (f'<path d="M{x-w1*.7:.0f},{y-hh*.7:.0f} L{x-w2*.66:.0f},{y-hh*.1:.0f}"'
          f' stroke="#cfe4d8" stroke-width="{8*s_:.0f}"'
          f' opacity="{.25+.25*abs(A.w(t,2.4)):.2f}"/>')
    return s + '</g>'


# ── 72 ─────────────────────────────────────────────────────────────────────
def vetka_ryabiny_v_vaze(t):
    """Прихожая у входной двери: высокая стеклянная ваза с большой веткой
    рябины стоит на тумбочке и занимает пол-кадра, рядом горит лампа под
    абажуром, хозяйка поправляет гроздья и переставляет вазу на подоконник."""
    rnd = random.Random(7219)
    s = f'<rect width="{W}" height="{H}" fill="#3a3028"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 120, True, "dosk"))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#8a7a6a" opacity=".42"/>')
    for i in range(9):
        s += SL(Z_DAL, f'<path d="M{70+i*220:.0f},40 q20,300 0,1000" fill="none"'
                       f' stroke="#9c8a78" stroke-width="14" opacity=".45"/>')
    s += SL(Z_DAL, polovicy(900, "url(#pol)"))
    s += SL(Z_DAL, hodiki(150, 280, t, 1.2))
    # входная дверь справа, обведённая красноватым светом
    dx, dy, dw, dh = 1450, 120, 450, 790
    obv = .4 + .5 * A.ease(A.seg(t, 2.6, 1.2)) * (.6 + .4 * abs(A.w(t, 1.5)))
    dv = dver(dx, dy, dw, dh, 0.0, "#6b5440", True, True)
    dv += (f'<rect x="{dx+dw*.14:.0f}" y="{dy+dh*.08:.0f}" width="{dw*.72:.0f}"'
           f' height="{dh*.34:.0f}" rx="8" fill="none" stroke="#4a382a"'
           f' stroke-width="14"/>')
    dv += (f'<rect x="{dx-16:.0f}" y="{dy-16:.0f}" width="{dw+32:.0f}"'
           f' height="{dh+32:.0f}" rx="10" fill="none" stroke="#c4502e"'
           f' stroke-width="18" opacity="{obv:.2f}"/>')
    dv += (f'<rect x="{dx-36:.0f}" y="{dy-36:.0f}" width="{dw+72:.0f}"'
           f' height="{dh+72:.0f}" rx="12" fill="none" stroke="#e8743c"'
           f' stroke-width="7" opacity="{obv*.6:.2f}"/>')
    mel = A.ease(A.seg(t, 3.4, .8))
    if mel > .02:
        for i in range(3):
            dv += (f'<path d="M{dx+dw*.28+i*58:.0f},{dy-62:.0f} l20,{-48*mel:.0f}'
                   f' l18,{48*mel:.0f}" fill="none" stroke="#f2ecd8"'
                   f' stroke-width="12" opacity="{.9*mel:.2f}"/>')
    s += SL(Z_SRED, dv)
    s += SL(Z_SRED, _podkova_rzh(dx + dw / 2, dy - 120, 1.0, t))
    # тумбочка, ЛАМПА С АБАЖУРОМ и ВАЗА С ВЕТКОЙ — главное
    perevoz = A.ease(A.seg(t, 2.0, 1.6))
    tx, ty = 700, 900
    tum = (f'<rect x="{tx-250:.0f}" y="{ty-300:.0f}" width="500" height="300" rx="10"'
           f' fill="url(#derev)" {o(9)}/>')
    tum += (f'<rect x="{tx-272:.0f}" y="{ty-320:.0f}" width="544" height="28" rx="8"'
            f' fill="{DOSKA}" {o(6)}/>')
    for i in range(2):
        tum += (f'<rect x="{tx-220:.0f}" y="{ty-266+i*132:.0f}" width="440"'
                f' height="116" rx="8" fill="#7d5636" {o(5)}/>')
        tum += (f'<rect x="{tx-40:.0f}" y="{ty-218+i*132:.0f}" width="80" height="18"'
                f' rx="9" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, tum)
    s += SL(Z_SRED, _lampa_abazhur(tx - 190, ty - 318, t, 1.9, 1.0))
    s += SL(Z_SRED, teplo(tx - 190, ty - 520, 820, 700,
                          .52 + .1 * abs(A.w(t, 1.7))))
    vx = tx + 110 + (560 * perevoz)
    vy = ty - 320 - (120 * math.sin(perevoz * 3.14159))
    s += SL(Z_SRED, _vaza(vx, vy, 1.15, t, True))
    # ВЕТКА РЯБИНЫ из вазы — на пол-кадра
    vet = f'<g transform="rotate({1.6*A.w(t,3.2):.2f} {vx:.0f} {vy-340:.0f})">'
    vet += (f'<path d="M{vx:.0f},{vy-340:.0f} q{-30:.0f},{-80:.0f} {-14:.0f},{-200:.0f}"'
            f' fill="none" stroke="#5e4428" stroke-width="22"/>')
    for i in range(6):
        p = i / 5
        bx = vx - 6 - p * 16
        by = vy - 370 - p * 160
        sgn = -1 if i % 2 else 1
        vet += (f'<path d="M{bx:.0f},{by:.0f} q{sgn*80:.0f},{-26:.0f}'
                f' {sgn*160:.0f},{-46:.0f}" fill="none" stroke="#6b5234"'
                f' stroke-width="{13-i}"/>')
        vet += (f'<ellipse cx="{bx+sgn*110:.0f}"'
                f' cy="{by-34+6*A.w(t,2.6,p):.0f}" rx="42" ry="16"'
                f' fill="#7d5a2e" opacity=".92" {o(3)}/>')
    vet += '</g>'
    s += SL(Z_SRED, vet)
    for i in range(5):
        if i > 3:
            continue
        s += SL(Z_SRED, grozd_ryabiny(vx + (-1 if i % 2 else 1) * (120 + i * 12),
                                      vy - 330 - i * 52, t, 1.7, 18, 863 + i,
                                      i * .18))
    # хозяйка справа от вазы, рукав короткий, к гроздьям
    hx = 1230 - perevoz * 60
    s += SL(Z_SRED, figura(hx, 1046, 540, t, "#4a3140", "#ffd98a", True, .3,
                           True, 1.0, False, 1.0))
    ruk, (kx, ky) = rukav(hx - 120, 700, 150, 198 + 14 * A.w(t, 1.2), t,
                          "#4a3140", "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="32" ry="24"'
                    f' fill="#4a3140" {o(5)}/>')
    # тень уходит по лестнице за дверью
    ten_ = A.ease(A.seg(t, 3.0, 1.4))
    s += SL(Z_SRED, f'<path d="M{dx+40:.0f},{dy+dh-40:.0f} l{150:.0f},{-200*ten_:.0f}'
                    f' l{70:.0f},{40:.0f} l{-160:.0f},{210*ten_:.0f} Z"'
                    f' fill="#1a1620" opacity="{.45*(1-ten_*.4):.2f}"/>')
    s += SL(Z_SRED, _veshalka(1060, 200, 330, t, 3, True))
    s += SL(Z_SRED, kot(330, 1012, t, 1.35, "#3b3430", False))
    s += SL(Z_SRED, _valenok(200, 1012, .86, t, .3, False, "#6e6358"))
    s += SL(Z_SRED, _valenok(300, 1012, .82, t, .6, False, "#6e6358"))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="60" height="1080" fill="#241f1a"'
                     f' opacity=".9"/>')
    s += SL(Z_PERED, _chashka(1760, 1012, 1.4, t, .2, KREM, True))
    s += SL(Z_PERED, par(1870, 960, t, 3, .4, 150, .4, .8))
    s += vinetka(.44)
    return s


# ── 73 ─────────────────────────────────────────────────────────────────────
def hozyayka_ugovarivaet_ogon(t):
    """Хозяйка на коленях перед открытой печной дверцей: лицо освещено снизу,
    из устья выглядывает рисованный огонёк с озорной рожицей и косится на трубу."""
    rnd = random.Random(7307)
    s = f'<rect width="{W}" height="{H}" fill="#241a14"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 760, 118))
    s += SL(Z_DAL, f'<rect width="{W}" height="760" fill="#2e2118" opacity=".45"/>')
    s += SL(Z_DAL, polovicy(760, "url(#pol)"))
    s += SL(Z_DAL, utvar_izby(1560, 180, 340, t, 877))
    s += SL(Z_DAL, mebel_hlam(60, 740, 300, t, 881))
    # ПЕЧЬ НА ПОЛ-КАДРА: побелённый массив, шесток, заслонка у стены
    px, py, pw, ph_ = 420, 120, 1120, 740
    pch = (f'<rect x="{px}" y="{py+110}" width="{pw}" height="{ph_-110}" rx="22"'
           f' fill="url(#pech)" {o(10)}/>')
    # свод: русскую печь узнают по горбу над устьём, без него это камин
    pch += (f'<path d="M{px:.0f},{py+130:.0f} q{pw*.5:.0f},{-220:.0f}'
            f' {pw:.0f},0 Z" fill="url(#pech)" {o(10)}/>')
    pch += (f'<path d="M{px+50:.0f},{py+130:.0f} q{pw*.44:.0f},{-170:.0f}'
            f' {pw-100:.0f},0" fill="none" stroke="{PECH2}" stroke-width="12"'
            f' opacity=".8"/>')
    pch += (f'<rect x="{px+40}" y="{py+96}" width="{pw-80}" height="44" rx="12"'
            f' fill="{PECH2}" {o(7)}/>')
    pch += kladka(px + 10, py + 150, pw - 20, ph_ - 170, 92, "url(#pech)")
    pch += (f'<rect x="{px+pw*.60:.0f}" y="{py-130:.0f}" width="{pw*.16:.0f}"'
            f' height="260" rx="8" fill="url(#kamen)" {o(8)}/>')
    pch += (f'<rect x="{px+pw*.57:.0f}" y="{py-150:.0f}" width="{pw*.22:.0f}"'
            f' height="36" rx="8" fill="{KAMEN2}" {o(6)}/>')
    for i in range(5):                   # швы побелки
        pch += (f'<line x1="{px+16}" y1="{py+90+i*132:.0f}" x2="{px+pw-16:.0f}"'
                f' y2="{py+90+i*132:.0f}" stroke="{PECH2}" stroke-width="6"'
                f' opacity=".55"/>')
    pch += (f'<rect x="{px+pw*.62:.0f}" y="{py+ph_*.50:.0f}" width="{pw*.34:.0f}"'
            f' height="{ph_*.34:.0f}" rx="12" fill="{PECH2}" {o(7)}/>')
    s += SL(Z_SRED, pch)
    # устье с дверцей: дверца откинута, за ней угли и огонь
    ux, uy, uw, uh = px + 130, py + 300, 440, 330
    s += SL(Z_SRED, kirpich_ustya(ux, uy, uw, uh, t, True))
    put = kontur_proema(ux, uy, uw, uh, "ustie")
    vn = f'<path d="{put}" fill="#190b05"/>'
    vn += ugli(ux + 40, uy + uh - 36, uw - 80, t, 9, 883)
    vn += ogon(ux + uw * .5, uy + uh - 26, t, 1.45, .1, 7)
    vn += ogon(ux + uw * .24, uy + uh - 20, t, .8, .5, 4)
    for i in range(7):                   # полешки в устье
        vn += (f'<rect x="{ux+36+i*52:.0f}" y="{uy+uh-82+(i%3)*14:.0f}" width="48"'
               f' height="26" rx="12" fill="#4a2f1c" {o(4)}/>')
    s += SL(Z_SRED, vn)
    # ОГОНЁК С РОЖИЦЕЙ выглядывает из устья и косится на трубу
    vyh = A.ease(A.seg(t, .3, .8))
    ustroilsya = A.ease(A.seg(t, 1.7, .7))
    ox_ = ux + uw * .5 + 30 * vyh
    oy_ = uy + uh - 120 - 140 * vyh + 90 * ustroilsya
    kos = 26 * A.ease(A.seg(t, .9, .6)) * (1 - ustroilsya)
    ogl = f'<g transform="translate({kos:.0f},{-kos*.7:.0f})" opacity="{vyh:.2f}">'
    for i in range(3):                   # тельце огонька язычками
        hh = (120 - i * 22) * (1 + .18 * A.w(t, .8, i * .3))
        ogl += (f'<path d="M{ox_-56+i*34:.0f},{oy_+70:.0f}'
                f' q{-30:.0f},{-hh*.5:.0f} {16:.0f},{-hh:.0f}'
                f' q{34:.0f},{hh*.44:.0f} {24:.0f},{hh:.0f} Z"'
                f' fill="{ORA if i != 1 else SVET}" opacity=".92"/>')
    ogl += (f'<ellipse cx="{ox_:.0f}" cy="{oy_:.0f}" rx="86" ry="78" fill="{SVET}"'
            f' {o(5)}/>')
    ogl += (f'<ellipse cx="{ox_:.0f}" cy="{oy_+16:.0f}" rx="62" ry="52" fill="#ffeab8"'
            f' opacity=".85"/>')
    ogl += _rozhica(ox_, oy_ - 6, 64, t, .2, True, "#7d2f10")
    ogl += '</g>'
    s += SL(Z_SRED, ogl)
    s += SL(Z_SRED, teplo(ux + uw * .5, uy + uh * .6, 760, 640,
                          .52 + .14 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, iskra_let(t, ux + uw * .5, uy + uh - 40, 10, 887, 340, .7))
    # заслонка откинута на шестке
    s += SL(Z_SRED, f'<g transform="rotate({-18+6*A.w(t,2.6):.1f} {ux-60:.0f}'
                    f' {uy+uh+40:.0f})">'
                    f'<rect x="{ux-130:.0f}" y="{uy+uh-250:.0f}" width="90"'
                    f' height="290" rx="10" fill="url(#chug)" {o(7)}/>'
                    f'<circle cx="{ux-86:.0f}" cy="{uy+uh-110:.0f}" r="20"'
                    f' fill="url(#zhel)" {o(5)}/></g>')
    # хозяйка на коленях, лицо освещено снизу
    s += SL(Z_SRED, figura(1300, 1030, 470, t, "#4a2f3a", "#ffd98a", True, .25,
                           True, 1.0, False, 2.2))
    s += SL(Z_SRED, teplo(1240, 700, 420, 360, .40 + .1 * abs(A.w(t, 1.4))))
    # щепка подкладывается в устье
    pod = A.ease(A.seg(t, 1.0, .9))
    ruk, (kx, ky) = rukav(1190, 830, 150, 196 + 10 * A.w(t, 1.1), t,
                          "#4a2f3a", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    sx_ = kx - pod * 80
    s += SL(Z_SRED, f'<path d="M{sx_:.0f},{ky:.0f} l-150,-18 l6,22 l150,14 Z"'
                    f' fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="30" ry="22"'
                    f' fill="#4a2f3a" {o(4)}/>')
    # шёпот: три дужки у лица
    for i in range(3):
        k = ((t * .8) + i * .33) % 1.0
        s += SL(Z_SRED, f'<path d="M{1200-k*110:.0f},{690-k*40:.0f} q-26,-20 -8,-46"'
                        f' fill="none" stroke="#ffe6b8" stroke-width="6"'
                        f' opacity="{.5*(1-k):.2f}"/>')
    s += SL(Z_SRED, krynka(1620, 1012, 1.5))
    s += SL(Z_SRED, _chugunok(1700, 1012, 1.1, t))
    s += SL(Z_SRED, kot(300, 1012, t, 1.2, "#3b3430", True))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="150" height="1080" fill="#140f0c"'
                     f' opacity=".92"/>')
    s += SL(Z_LETIT, iskra_let(t, ux + uw * .5, uy + 40, 7, 907, 420, .5))
    s += vinetka(.5)
    return s


def _chugunok(x, y, s_=1.0, t=0.0, par_=False):
    """Чугунок: пузатое чугунное тулово, узкое горло, дуга ушка, блик."""
    w_, hh = 84 * s_, 100 * s_
    s = ten(x, y + 6 * s_, w_ * .8, 11 * s_, .45)
    s += (f'<path d="M{x-w_*.34:.0f},{y-hh:.0f} q{-w_*.56:.0f},{hh*.30:.0f}'
          f' {-w_*.30:.0f},{hh*.68:.0f} q{w_*.22:.0f},{hh*.34:.0f} {w_*.64:.0f},{hh*.32:.0f}'
          f' q{w_*.64:.0f},{hh*.02:.0f} {w_*.64:.0f},{-hh*.32:.0f}'
          f' q{w_*.26:.0f},{-hh*.38:.0f} {-w_*.30:.0f},{-hh*.68:.0f} Z"'
          f' fill="url(#chug)" {o(max(3, 6*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*.34:.0f}" ry="{10*s_:.0f}"'
          f' fill="#1d1b1a" {o(max(2, 4*s_))}/>')
    s += (f'<path d="M{x-w_*.72:.0f},{y-hh*.56:.0f} q{w_*.10:.0f},{-hh*.22:.0f}'
          f' {w_*.26:.0f},{-hh*.06:.0f}" fill="none" stroke="#6b6a68"'
          f' stroke-width="{max(3, 7*s_):.0f}"/>')
    s += (f'<path d="M{x-w_*.56:.0f},{y-hh*.46:.0f} q{w_*.08:.0f},{hh*.26:.0f}'
          f' {w_*.02:.0f},{hh*.42:.0f}" fill="none" stroke="#9aa0a6"'
          f' stroke-width="{max(3, 9*s_):.0f}"'
          f' opacity="{.22+.2*abs(A.w(t,2.6,x*.002)):.2f}"/>')
    if par_:
        s += par(x, y - hh - 10 * s_, t, 4, .5, 150 * s_, .4, .9)
    return s


def _ohvat(x, y, s_=1.0, t=0.0):
    """Ухват: длинная рукоять и железная дуга-рога. Стоит у печи, подрагивает."""
    ug = 4.0 + 2.0 * A.w(t, 3.4, x * .001)
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-12*s_:.0f}" y="{y-620*s_:.0f}" width="{24*s_:.0f}"'
          f' height="{620*s_:.0f}" rx="{10*s_:.0f}" fill="url(#derev)" {o(6)}/>')
    s += (f'<path d="M{x-66*s_:.0f},{y-660*s_:.0f} q{66*s_:.0f},{70*s_:.0f}'
          f' {132*s_:.0f},0" fill="none" stroke="#5d6168"'
          f' stroke-width="{18*s_:.0f}" stroke-linecap="round"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*66*s_:.0f},{y-660*s_:.0f} q{i*18*s_:.0f},{-56*s_:.0f}'
              f' {i*4*s_:.0f},{-96*s_:.0f}" fill="none" stroke="#5d6168"'
              f' stroke-width="{15*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<circle cx="{x-30*s_:.0f}" cy="{y-640*s_:.0f}" r="{8*s_:.0f}"'
          f' fill="#e8f1f8" opacity="{.3+.3*abs(A.w(t,2.2)):.2f}"/>')
    return s + '</g>'


# ── 74 ─────────────────────────────────────────────────────────────────────
def luchina_v_svetce(t):
    """Тёмная изба: посреди неё высокая кованая стойка-светец на пол-кадра,
    в её развилке горит лучина, под ней корытце с водой. Рядом полено, от
    которого ножом откалывают длинную тонкую щепку."""
    rnd = random.Random(7411)
    s = f'<rect width="{W}" height="{H}" fill="#241a18"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 820, 122))
    s += SL(Z_DAL, f'<rect width="{W}" height="820" fill="#3f2d20" opacity=".4"/>')
    s += SL(Z_DAL, polovicy(820, "#6b4a2a"))
    s += SL(Z_DAL, utvar_izby(70, 200, 380, t, 911))
    s += SL(Z_DAL, okno_izby(1540, 190, 330, 270, t, moroz=.5))
    # печь справа с углями — заполняет пустое поле и греет кадр
    s += SL(Z_SRED, pech(1440, 440, 480, 480, t, True, True, False))
    s += SL(Z_SRED, kirpich_ustya(1520, 640, 240, 180, t, True))
    put2 = kontur_proema(1520, 640, 240, 180, "ustie")
    s += SL(Z_SRED, f'<path d="{put2}" fill="#190b05"/>'
                    + ugli(1544, 790, 200, t, 7, 913)
                    + ogon(1640, 798, t, .8, .3, 5))
    s += SL(Z_SRED, teplo(1640, 740, 520, 440, .34 + .1 * abs(A.w(t, 1.7))))
    # СВЕТЕЦ НА ПОЛ-КАДРА в центре
    sx, sy = 900, 1030
    s += SL(Z_SRED, _svetec(sx, sy, 470, t, 2.1, True))
    razg = A.ease(A.seg(t, 1.0, 1.1))
    lx, ly = sx, sy - 470
    s += SL(Z_SRED, _luchina_v_razvilke(lx, ly - 76, t, 1.45, razg, .1))
    s += SL(Z_SRED, teplo(lx + 160, ly - 290, 880 * razg + 200,
                          760 * razg + 180, .54 * razg + .12))
    s += SL(Z_SRED, iskra_let(t, lx + 170, ly - 300, 10, 919, 400, .9))
    kr = 300 + 520 * razg
    s += SL(Z_SRED, f'<ellipse cx="{sx:.0f}" cy="1016" rx="{kr:.0f}"'
                    f' ry="{kr*.26:.0f}" fill="url(#teplo)"'
                    f' opacity="{.34*razg+.12:.2f}"/>')
    for i in range(3):                   # уголёк падает с лучины в корытце
        k = ((t * .55) + i * .34) % 1.0
        s += SL(Z_SRED, f'<circle cx="{lx+168-150*k+8*A.w(t,1.6,i*.3):.0f}"'
                        f' cy="{ly-290+k*(sy-320-(ly-290)):.0f}"'
                        f' r="{9-3*k:.1f}" fill="{ORA}"'
                        f' opacity="{.95*(1-k*.5):.2f}"/>')
    # ПОЛЕНО И НОЖ крупно на переднем плане
    pol_x, pol_y = 420, 1010
    pln = (f'<rect x="{pol_x-230:.0f}" y="{pol_y-190:.0f}" width="460"'
           f' height="196" rx="90" fill="#f2ece0" {o(9)}/>')
    for i in range(5):
        pln += (f'<path d="M{pol_x-170+i*96:.0f},{pol_y-168:.0f} l0,52"'
                f' stroke="#2f2a26" stroke-width="13" stroke-linecap="round"'
                f' opacity=".88"/>')
        pln += (f'<path d="M{pol_x-150+i*96:.0f},{pol_y-86:.0f} l0,34"'
                f' stroke="#2f2a26" stroke-width="11" stroke-linecap="round"'
                f' opacity=".7"/>')
    pln += (f'<ellipse cx="{pol_x+230:.0f}" cy="{pol_y-92:.0f}" rx="40" ry="98"'
            f' fill="#d8b98a" {o(6)}/>')
    pln += (f'<ellipse cx="{pol_x+230:.0f}" cy="{pol_y-92:.0f}" rx="19" ry="52"'
            f' fill="#a9823f" opacity=".85"/>')
    s += SL(Z_SRED, pln)
    nozh = A.ease(A.seg(t, .2, .9))
    nx = pol_x - 180 + nozh * 340
    s += SL(Z_SRED, f'<g transform="rotate({-10+5*A.w(t,1.4):.1f} {nx:.0f}'
                    f' {pol_y-240:.0f})">'
                    f'<rect x="{nx-20:.0f}" y="{pol_y-370:.0f}" width="40"'
                    f' height="176" rx="8" fill="#cfd6dc" {o(5)}/>'
                    f'<rect x="{nx-28:.0f}" y="{pol_y-400:.0f}" width="56"'
                    f' height="44" rx="10" fill="#6b4a2a" {o(5)}/>'
                    f'<line x1="{nx+12:.0f}" y1="{pol_y-362:.0f}" x2="{nx+12:.0f}"'
                    f' y2="{pol_y-206:.0f}" stroke="#ffffff" stroke-width="8"'
                    f' opacity="{.3+.3*abs(A.w(t,2.0)):.2f}"/></g>')
    s += SL(Z_SRED, f'<path d="M{pol_x-210:.0f},{pol_y-196:.0f}'
                    f' l{300*nozh:.0f},{-22*nozh:.0f} l0,24 l{-300*nozh:.0f},'
                    f'{16*nozh:.0f} Z" fill="#f8f0dc" opacity=".96" {o(4)}/>')
    for i in range(12):                  # стружка летит
        k = ((t * .8) + i * .085) % 1.0
        s += SL(Z_LETIT, f'<path d="M{pol_x-120+i*40+k*70:.0f},'
                         f'{pol_y-200+k*150:.0f} q16,-14 30,2" fill="none"'
                         f' stroke="#f2e8d4" stroke-width="6"'
                         f' opacity="{.85*(1-k):.2f}"/>')
    s += SL(Z_SRED, figura(250, 1070, 520, t, "#453a4a", "#ffd98a", False, .4,
                           True, 1.0, False, 1.4, True))
    ruk, _ = rukav(330, 740, 170, 42, t, "#453a4a", "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, lavka(1180, 920, 300))
    s += SL(Z_SRED, figura(1300, 920, 320, t, "#4a4450", "#ffd98a", True, .7,
                           True, .95))
    s += SL(Z_SRED, krynka(1760, 1012, 1.7))
    s += SL(Z_SRED, _chugunok(1120, 1012, 1.3, t, True))
    s += SL(Z_PERED, f'<rect x="1840" y="0" width="100" height="1080"'
                     f' fill="url(#brev)" {o(9)}/>')
    s += SL(Z_PERED, ramka_pp("levo", "#1a120e", .78))
    s += vinetka(.48)
    return s


# ── 75 ─────────────────────────────────────────────────────────────────────
def semya_prosit_svetec(t):
    """Семья полукругом перед светцом: дед впереди кланяется ему в пояс и
    грозит пальцем, а в светлое окно просовывается тонкая чёрная лапа тени и
    тянется к огоньку лучины."""
    rnd = random.Random(7517)
    s = f'<rect width="{W}" height="{H}" fill="#241c20"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 800, 120))
    s += SL(Z_DAL, f'<rect width="{W}" height="800" fill="#3a2b24" opacity=".42"/>')
    s += SL(Z_DAL, polovicy(800, "#6b4a2a"))
    s += SL(Z_DAL, utvar_izby(70, 190, 300, t, 929))
    # окно СВЕТЛОЕ, чтобы чёрная лапа тени читалась
    okx, oky, okw, okh = 1240, 170, 460, 380
    vid = (f'<rect x="{okx}" y="{oky}" width="{okw}" height="{okh}"'
           f' fill="#8fa8c4"/>')
    vid += (f'<rect x="{okx}" y="{oky+okh*.56:.0f}" width="{okw}"'
            f' height="{okh*.44:.0f}" fill="#7892ad"/>')
    for i in range(3):
        bx = okx + 40 + i * 150
        vid += (f'<rect x="{bx:.0f}" y="{oky+okh*.48:.0f}" width="110"'
                f' height="{okh*.3:.0f}" fill="#64809c" opacity=".9"/>')
        vid += (f'<path d="M{bx-16:.0f},{oky+okh*.48:.0f} l71,-54 l71,54 Z"'
                f' fill="#5a768f" opacity=".92"/>')
    vid += (f'<circle cx="{okx+okw*.78:.0f}" cy="{oky+okh*.22:.0f}" r="46"'
            f' fill="#eef5fb" opacity=".9"/>')
    for i in range(14):
        vid += (f'<circle cx="{okx+rnd.random()*okw:.0f}"'
                f' cy="{oky+rnd.random()*okh:.0f}" r="{rnd.uniform(3,7):.1f}"'
                f' fill="#f2f8ff"'
                f' opacity="{.5+.4*abs(A.w(t,2.6+i*.2,i*.1)):.2f}"/>')
    s += SL(Z_SRED, okno_izby(okx, oky, okw, okh, t, vid, .12, False, True))
    # ЛАПА ТЕНИ: чёрная, толстая, тянется из окна к огоньку
    lapa = A.ease(A.seg(t, 1.0, 1.8))
    lp = ""
    if lapa > .03:
        lp += (f'<path d="M{okx+okw*.42:.0f},{oky+okh*.46:.0f}'
               f' q{-160*lapa:.0f},{110*lapa:.0f} {-400*lapa:.0f},{190*lapa:.0f}"'
               f' fill="none" stroke="#0d0a10" stroke-width="{44*lapa+8:.0f}"'
               f' stroke-linecap="round" opacity=".95"/>')
        ex = okx + okw * .42 - 400 * lapa
        ey = oky + okh * .46 + 190 * lapa
        for i in range(4):               # когти лапы
            a = -.75 + i * .42
            lp += (f'<path d="M{ex:.0f},{ey:.0f} q{-70*lapa:.0f},'
                   f'{math.sin(a)*70*lapa:.0f} {-130*lapa:.0f},'
                   f'{math.sin(a)*112*lapa:.0f}" fill="none" stroke="#0d0a10"'
                   f' stroke-width="{24-i*3:.0f}" stroke-linecap="round"'
                   f' opacity=".95"/>')
        lp += (f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{54*lapa:.0f}"'
               f' ry="{40*lapa:.0f}" fill="#0d0a10" opacity=".95"/>')
    s += SL(Z_SRED, lp)
    # СВЕТЕЦ большой в центре, лучина вспыхивает
    sx, sy = 820, 1020
    s += SL(Z_SRED, _svetec(sx, sy, 450, t, 1.9, True))
    vsp = .6 + .4 * A.ease(A.seg(t, 2.6, .5)) + .18 * abs(A.w(t, 1.1))
    lx, ly = sx, sy - 450
    s += SL(Z_SRED, _luchina_v_razvilke(lx, ly - 72, t, 1.4, vsp, .2))
    s += SL(Z_SRED, teplo(lx + 150, ly - 280, 900 * vsp, 780 * vsp, .52 * vsp))
    s += SL(Z_SRED, iskra_let(t, lx + 160, ly - 290, 10, 937, 420, .9))
    s += SL(Z_SRED, f'<ellipse cx="{sx:.0f}" cy="1006" rx="{600*vsp:.0f}"'
                    f' ry="{160*vsp:.0f}" fill="url(#teplo)"'
                    f' opacity="{.3*vsp:.2f}"/>')
    # дед кланяется в пояс и грозит пальцем — крупно, слева
    pokl = A.ease(A.seg(t, .4, 1.2)) * (1 - A.ease(A.seg(t, 2.4, .9)))
    gx = 420
    s += SL(Z_SRED, figura(gx, 1066, 600, t, "#2f2a36", "#ffd98a", False, .2,
                           True, 1.0, False, 2.0 + 20 * pokl, True))
    ruk, (kx, ky) = rukav(gx + 120, 720 + pokl * 150, 200,
                          -54 - 20 * A.w(t, .9), t, "#2f2a36", "#ffd98a", .3, 8.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{ky:.0f} l{10:.0f},{-80:.0f}"'
                    f' stroke="#2f2a36" stroke-width="28" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx+12:.0f}" cy="{ky-92:.0f}" rx="18" ry="26"'
                    f' fill="#f0cfae" {o(4)}/>')
    # три фигуры семьи справа, с интервалом
    for i, (fx_, h_, col, pl, bo) in enumerate((
            (1200, 480, "#4a2f3a", True, False),
            (1480, 430, "#2e4a5a", True, False),
            (1740, 360, "#5b3f2a", False, False))):
        s += SL(Z_SRED, figura(fx_, 1058 + i * 8, h_, t, col, "#ffd98a", pl,
                               .2 * i, True, 1.0, False, 1.0, bo))
    s += SL(Z_SRED, lavka(1180, 940, 440))
    s += SL(Z_SRED, _lampa_abazhur(170, 700, t, 1.5, 1.0))
    s += SL(Z_SRED, teplo(170, 540, 640, 540, .42 + .1 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, kot(330, 1012, t, 1.3, "#3b3430", False))
    s += SL(Z_SRED, krynka(170, 1012, 1.5))
    s += SL(Z_SRED, _chugunok(600, 1012, 1.2, t, True))
    s += SL(Z_PERED, ramka_pp("pravo", "#16111a", .8))
    s += vinetka(.48)
    return s


# ── 76 ─────────────────────────────────────────────────────────────────────
def vecher_pochinki_zimnego(t):
    """Изба в свете открытой печи, всё зимнее вытащено наружу: мать выбивает
    тулуп прутом на верёвке, рукавицы сушатся на шестке, отец пришивает к
    валенку кожаную заплату, малыш сидит в огромной шапке, съехавшей на нос."""
    rnd = random.Random(7619)
    s = f'<rect width="{W}" height="{H}" fill="#2a2018"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 800, 116))
    s += SL(Z_DAL, f'<rect width="{W}" height="800" fill="#45321f" opacity=".4"/>')
    s += SL(Z_DAL, polovicy(800, "url(#pol)"))
    s += SL(Z_DAL, utvar_izby(1680, 170, 230, t, 941))
    # ПЕЧЬ слева с ОТКРЫТЫМ устьём — тёплое пятно сцены
    s += SL(Z_SRED, pech(10, 250, 440, 560, t, True, True, False))
    ux, uy, uw, uh = 60, 470, 250, 210
    s += SL(Z_SRED, kirpich_ustya(ux, uy, uw, uh, t, True))
    put = kontur_proema(ux, uy, uw, uh, "ustie")
    s += SL(Z_SRED, f'<path d="{put}" fill="#190b05"/>'
                    + ugli(ux + 28, uy + uh - 28, uw - 56, t, 8, 943)
                    + ogon(ux + uw * .5, uy + uh - 22, t, 1.15, .1, 6))
    s += SL(Z_SRED, teplo(ux + uw * .5, uy + uh * .6, 700, 600,
                          .52 + .12 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, iskra_let(t, ux + uw * .5, uy + uh - 40, 9, 953, 340, .7))
    # рукавицы сушатся на шестке над устьём
    s += SL(Z_SRED, f'<rect x="{ux-40:.0f}" y="{uy-70:.0f}" width="{uw+90:.0f}"'
                    f' height="26" rx="8" fill="url(#chug)" {o(5)}/>')
    for i, px in ((0, ux + 60), (1, ux + 220)):
        s += SL(Z_SRED, _varezhka(px, uy - 46, 1.15, t, .2 + i * .4, TKAN, True))
        s += SL(Z_SRED, par(px, uy - 150, t, 3, .45, 160, .5, .7))
    # ТУЛУП НА ВЕРЁВКЕ в центре, его выбивают прутом
    s += SL(Z_SRED, f'<path d="M900,230 q380,60 760,-10" fill="none"'
                    f' stroke="#c2ab86" stroke-width="9"/>')
    udar = max(0.0, A.w(t, 1.1, .1))
    s += SL(Z_SRED, _tulup_vis(1200, 250, 470, 600, t, .2, udar))
    for i in range(12):                  # пыль вылетает от удара
        k = ((t * 1.0) + i * .085) % 1.0
        s += SL(Z_SRED, f'<circle cx="{1200+rnd.uniform(-200,200)+k*140:.0f}"'
                        f' cy="{520+rnd.uniform(-140,140)-k*100:.0f}"'
                        f' r="{7+12*k:.0f}" fill="#e4d6bc"'
                        f' opacity="{.5*(1-k)*udar:.2f}"/>')
    prut = -36 + 56 * udar
    s += SL(Z_SRED, f'<g transform="rotate({prut:.1f} 1620 620)">'
                    f'<path d="M1620,620 q100,-96 230,-152" fill="none"'
                    f' stroke="url(#derev)" stroke-width="20"'
                    f' stroke-linecap="round"/>'
                    f'<path d="M1842,470 q34,-18 60,-4" fill="none"'
                    f' stroke="#8a6238" stroke-width="12"'
                    f' stroke-linecap="round"/></g>')
    if udar > .85:
        for i in range(5):
            a = -2.4 + i * .5
            s += SL(Z_SRED, f'<line x1="1420" y1="520"'
                            f' x2="{1420+math.cos(a)*70:.0f}"'
                            f' y2="{520+math.sin(a)*70:.0f}" stroke="#ffe6b8"'
                            f' stroke-width="7" opacity=".6"/>')
    s += SL(Z_SRED, figura(1700, 1046, 520, t, "#4a2f3a", "#ffd98a", True, .3,
                           True, 1.0, False, 1.6))
    ruk, _ = rukav(1660, 710, 150, -40 + 30 * udar, t, "#4a2f3a", "#ffd98a",
                   .1, 6.0)
    s += SL(Z_SRED, ruk)
    # отец и БОЛЬШОЙ ВАЛЕНОК С ЗАПЛАТОЙ справа внизу
    s += SL(Z_SRED, lavka(460, 930, 360))
    s += SL(Z_SRED, figura(540, 930, 400, t, "#3a3346", "#ffd98a", False, .5,
                           True, 1.0, False, 1.0, True))
    vx_, vy_ = 800, 1046
    s += SL(Z_SRED, _valenok(vx_, vy_, 2.6, t, .3, False, "#bda98a", -10))
    zap = (f'M{vx_-60:.0f},{vy_-400:.0f} q100,-40 184,22'
           f' q-16,110 -172,86 Z')
    s += SL(Z_SRED, f'<path d="{zap}" fill="#b5803a" {o(8)}/>')
    s += SL(Z_SRED, f'<path d="{zap}" fill="none" stroke="#f2e8d4"'
                    f' stroke-width="7" stroke-dasharray="16 14"/>')
    dra = A.w(t, .7, .2)
    ruk2, (dx_, dy_) = rukav(620, 790, 150, 26 + 24 * dra, t, "#3a3346",
                             "#ffd98a", .3, 6.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<line x1="{dx_:.0f}" y1="{dy_:.0f}" x2="{vx_+40:.0f}"'
                    f' y2="{vy_-300:.0f}" stroke="#e2d6bc" stroke-width="6"'
                    f' opacity=".9"/>')
    for i in range(5):                   # стежки по заплате
        st = A.ease(A.seg(t, .6 + i * .3, .3))
        if st > .02:
            s += SL(Z_SRED, f'<line x1="{vx_+48+i*28:.0f}" y1="{vy_-322+i*12:.0f}"'
                            f' x2="{vx_+64+i*28:.0f}" y2="{vy_-280+i*12:.0f}"'
                            f' stroke="#f8f0dc" stroke-width="8"'
                            f' opacity="{.9*st:.2f}"/>')
    # малыш в огромной шапке, съехавшей на нос
    mx, my = 1640, 1046
    s += SL(Z_SRED, figura(mx, my, 300, t, "#6b3a44", "#ffd98a", False, .8,
                           False, 1.0, False, 1.2, False, False))
    sdv = 30 * A.ease(A.seg(t, 1.4, .8))
    s += SL(Z_SRED, _shapka_meh(mx, my - 244 + sdv, 1.7, t, .4, 0.0))
    s += SL(Z_SRED, para_izo_rta(mx + 48, my - 224 + sdv, t, .5, .9, .45))
    s += SL(Z_SRED, _valenok(420, 1012, 1.0, t, .1, True, "#6e6358"))
    s += SL(Z_SRED, _chugunok(300, 1012, 1.2, t, True))
    s += SL(Z_PERED, ramka_pp("pravo", "#1a120c", .76))
    s += SL(Z_PERED, _shapka_meh(170, 1012, 1.5, t, .2, 0.0))
    s += vinetka(.46)
    return s


def _lampa_abazhur(x, y, t, s_=1.0, zazh=1.0):
    """Настольная лампа под абажуром: кремово-зелёный конус абажура с бахромой,
    точёная ножка, круглое основание и тёплый шар света под абажуром.
    `baza.lampa(abazhur=True)` даёт красную трапецию и читалась шторой."""
    w_, hh = 140 * s_, 230 * s_
    s = ten(x, y + 8 * s_, w_ * .46, 12 * s_, .42)
    s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_*.40:.0f}" ry="{14*s_:.0f}"'
          f' fill="url(#med)" {o(max(3, 5*s_))}/>')
    s += (f'<path d="M{x-12*s_:.0f},{y-6*s_:.0f} q{-8*s_:.0f},{-hh*.30:.0f}'
          f' {4*s_:.0f},{-hh*.46:.0f} l{16*s_:.0f},0'
          f' q{12*s_:.0f},{hh*.16:.0f} {4*s_:.0f},{hh*.46:.0f} Z"'
          f' fill="url(#med)" {o(max(3, 4*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh*.48:.0f}" rx="{22*s_:.0f}"'
          f' ry="{10*s_:.0f}" fill="#b5803a" {o(max(2, 3*s_))}/>')
    if zazh > .02:                       # шар света под абажуром
        s += teplo(x, y - hh * .58, 230 * s_ * zazh, 190 * s_ * zazh, .62 * zazh)
        s += (f'<circle cx="{x:.0f}" cy="{y-hh*.60:.0f}" r="{26*s_:.0f}"'
              f' fill="{SVET}" opacity="{(.6+.3*abs(A.w(t,1.6)))*zazh:.2f}"/>')
    s += (f'<path d="M{x-w_*.5:.0f},{y-hh*.56:.0f} L{x-w_*.24:.0f},{y-hh*.98:.0f}'
          f' L{x+w_*.24:.0f},{y-hh*.98:.0f} L{x+w_*.5:.0f},{y-hh*.56:.0f} Z"'
          f' fill="#e8dfae" {o(max(4, 6*s_))}/>')
    s += (f'<path d="M{x-w_*.44:.0f},{y-hh*.63:.0f} L{x-w_*.22:.0f},{y-hh*.94:.0f}'
          f' L{x+w_*.22:.0f},{y-hh*.94:.0f} L{x+w_*.44:.0f},{y-hh*.63:.0f} Z"'
          f' fill="#f4ecc8" opacity=".75"/>')
    for i in range(9):                   # бахрома по краю абажура
        xx = x - w_ * .48 + i * w_ * .12
        s += (f'<path d="M{xx:.0f},{y-hh*.56:.0f} q{3*s_:.0f},{18*s_:.0f}'
              f' {-2*s_+2*A.w(t,2.4,i*.2):.0f},{30*s_:.0f}" fill="none"'
              f' stroke="#d8cb92" stroke-width="{max(3, 6*s_):.0f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh*.98:.0f}" rx="{w_*.24:.0f}"'
          f' ry="{9*s_:.0f}" fill="#d8cb92" {o(max(2, 4*s_))}/>')
    return s


def _gruzovichok(x, y, s_=1.0, t=0.0):
    """Пузатый фургончик: капот, кабина с окном, высокий кузов, два колеса со
    спицами, бампер и круглая фара. Прежнее одно пятно читалось диваном."""
    w_, hh = 420 * s_, 200 * s_
    rot = (t * 40) % 360
    s = ten(x, y + 10 * s_, w_ * .52, 18 * s_, .5)
    # кузов-фургон
    s += (f'<rect x="{x-w_*.52:.0f}" y="{y-hh*1.45:.0f}" width="{w_*.62:.0f}"'
          f' height="{hh*1.25:.0f}" rx="{14*s_:.0f}" fill="#3f5c7a" {o(max(4, 8*s_))}/>')
    for i in range(4):                   # доски борта
        s += (f'<line x1="{x-w_*.48+i*w_*.15:.0f}" y1="{y-hh*1.40:.0f}"'
              f' x2="{x-w_*.48+i*w_*.15:.0f}" y2="{y-hh*.26:.0f}"'
              f' stroke="#324c66" stroke-width="{max(3, 8*s_):.0f}"/>')
    # кабина
    s += (f'<path d="M{x+w_*.10:.0f},{y-hh*1.45:.0f} h{w_*.30:.0f}'
          f' q{w_*.10:.0f},{hh*.10:.0f} {w_*.12:.0f},{hh*.52:.0f}'
          f' l0,{hh*.57:.0f} h{-w_*.52:.0f} Z" fill="#4a6a8a" {o(max(4, 7*s_))}/>')
    s += (f'<path d="M{x+w_*.16:.0f},{y-hh*1.34:.0f} h{w_*.22:.0f}'
          f' q{w_*.08:.0f},{hh*.06:.0f} {w_*.09:.0f},{hh*.38:.0f}'
          f' h{-w_*.31:.0f} Z" fill="url(#stekl)" opacity=".8" {o(max(3, 5*s_))}/>')
    # капот
    s += (f'<path d="M{x+w_*.40:.0f},{y-hh*.84:.0f} q{w_*.16:.0f},{hh*.04:.0f}'
          f' {w_*.17:.0f},{hh*.30:.0f} l0,{hh*.26:.0f} h{-w_*.17:.0f} Z"'
          f' fill="#3f5c7a" {o(max(4, 6*s_))}/>')
    s += (f'<rect x="{x+w_*.40:.0f}" y="{y-hh*.56:.0f}" width="{w_*.17:.0f}"'
          f' height="{hh*.18:.0f}" rx="{5*s_:.0f}" fill="#2a3c50" {o(max(2, 4*s_))}/>')
    s += (f'<circle cx="{x+w_*.52:.0f}" cy="{y-hh*.66:.0f}" r="{22*s_:.0f}"'
          f' fill="url(#zhel)" {o(max(3, 5*s_))}/>')
    s += (f'<circle cx="{x+w_*.52:.0f}" cy="{y-hh*.66:.0f}" r="{12*s_:.0f}"'
          f' fill="{SVET}" opacity="{.55+.35*abs(A.w(t,1.9)):.2f}"/>')
    s += (f'<rect x="{x-w_*.56:.0f}" y="{y-hh*.26:.0f}" width="{w_*1.16:.0f}"'
          f' height="{hh*.12:.0f}" rx="{7*s_:.0f}" fill="#2a3c50" {o(max(3, 5*s_))}/>')
    for sgn in (-1, 1):                  # два колеса со спицами
        wx = x + sgn * w_ * .33
        s += (f'<circle cx="{wx:.0f}" cy="{y-hh*.10:.0f}" r="{58*s_:.0f}"'
              f' fill="#23262a" {o(max(4, 7*s_))}/>')
        s += (f'<circle cx="{wx:.0f}" cy="{y-hh*.10:.0f}" r="{28*s_:.0f}"'
              f' fill="#9aa1a8" {o(max(3, 4*s_))}/>')
        s += f'<g transform="rotate({rot:.0f} {wx:.0f} {y-hh*.10:.0f})">'
        for j in range(4):
            a = j * .7854
            s += (f'<line x1="{wx-math.cos(a)*24*s_:.0f}"'
                  f' y1="{y-hh*.10-math.sin(a)*24*s_:.0f}"'
                  f' x2="{wx+math.cos(a)*24*s_:.0f}"'
                  f' y2="{y-hh*.10+math.sin(a)*24*s_:.0f}" stroke="#5d6168"'
                  f' stroke-width="{max(3, 6*s_):.0f}"/>')
        s += '</g>'
    return s


def _gazeta_list(x, y, w_, h_, t, ug=0.0, seed=3, komok=0.0):
    """Газетный лист: серая полоса фотографии и волнистые строки, без букв.
    `komok` сминает лист в комок — им набивают ботинок."""
    rnd = random.Random(seed)
    k = komok
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    if k < .55:
        s += (f'<rect x="{x-w_/2:.0f}" y="{y-h_/2:.0f}" width="{w_:.0f}"'
              f' height="{h_:.0f}" rx="3" fill="url(#list)" opacity="{1-k*1.4:.2f}"'
              f' {o(4)}/>')
        s += (f'<rect x="{x-w_*.44:.0f}" y="{y-h_*.38:.0f}" width="{w_*.34:.0f}"'
              f' height="{h_*.30:.0f}" fill="#8f979c" opacity="{.8*(1-k*1.4):.2f}"/>')
        for i in range(8):
            yy = y - h_ * .32 + i * h_ * .09
            s += (f'<path d="M{x-w_*.06:.0f},{yy:.0f} q{w_*.12:.0f},'
                  f'{rnd.uniform(-4,4):.1f} {w_*.46:.0f},0" fill="none"'
                  f' stroke="#6b645c" stroke-width="4"'
                  f' opacity="{.85*(1-k*1.4):.2f}"/>')
        for i in range(5):
            yy = y + h_ * .08 + i * h_ * .08
            s += (f'<path d="M{x-w_*.44:.0f},{yy:.0f} q{w_*.22:.0f},'
                  f'{rnd.uniform(-3,3):.1f} {w_*.88:.0f},0" fill="none"'
                  f' stroke="#6b645c" stroke-width="4"'
                  f' opacity="{.8*(1-k*1.4):.2f}"/>')
        s += (f'<line x1="{x:.0f}" y1="{y-h_/2:.0f}" x2="{x:.0f}" y2="{y+h_/2:.0f}"'
              f' stroke="#b8ae9a" stroke-width="3" opacity="{.8*(1-k*1.4):.2f}"/>')
    if k > .1:                           # комок: мятые дольки
        rr = (w_ * .22) * min(1.0, k * 1.5)
        s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="url(#list)"'
              f' opacity="{min(1.0, k*1.6):.2f}" {o(4)}/>')
        for i in range(9):
            a = i * .7
            s += (f'<path d="M{x+math.cos(a)*rr*.3:.0f},{y+math.sin(a)*rr*.3:.0f}'
                  f' q{math.cos(a)*rr*.5:.0f},{math.sin(a)*rr*.3:.0f}'
                  f' {math.cos(a)*rr*.95:.0f},{math.sin(a)*rr*.9:.0f}" fill="none"'
                  f' stroke="#c3b89c" stroke-width="5"'
                  f' opacity="{min(1.0, k*1.4):.2f}"/>')
    return s + '</g>'


def _shchetka(x, y, s_=1.0, t=0.0, ug=0.0):
    """Сапожная щётка: деревянная колодка и густая щетина."""
    w_, hh = 150 * s_, 40 * s_
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-hh:.0f}" width="{w_:.0f}" height="{hh:.0f}"'
          f' rx="{hh*.4:.0f}" fill="url(#derev)" {o(max(3, 5*s_))}/>')
    for i in range(16):
        xx = x - w_ * .46 + i * (w_ * .92 / 15)
        s += (f'<line x1="{xx:.0f}" y1="{y:.0f}" x2="{xx+2*A.w(t,1.4,i*.1):.0f}"'
              f' y2="{y+hh*.62:.0f}" stroke="#4a3a28"'
              f' stroke-width="{max(2, 5*s_):.0f}"/>')
    s += (f'<path d="M{x-w_*.3:.0f},{y-hh*.64:.0f} q{w_*.3:.0f},{-hh*.2:.0f}'
          f' {w_*.6:.0f},0" fill="none" stroke="#c9a771"'
          f' stroke-width="{max(2, 5*s_):.0f}" opacity=".6"/>')
    return s + '</g>'


# ── 77 ─────────────────────────────────────────────────────────────────────
def ded_pletet_vozhzhi(t):
    """Дед на лавке плетёт из трёх толстых кожаных полос косу: один конец
    зажат в зубах, другой на крюке в стене. Внук держит готовый конец и
    правит понарошку — над лавкой стоит рисованная лошадка и ждёт вожжей."""
    rnd = random.Random(7723)
    s = f'<rect width="{W}" height="{H}" fill="#2e2318"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 840, 118))
    s += SL(Z_DAL, f'<rect width="{W}" height="840" fill="#4a3620" opacity=".38"/>')
    s += SL(Z_DAL, polovicy(840, "url(#pol)"))
    s += SL(Z_DAL, utvar_izby(80, 180, 300, t, 971))
    s += SL(Z_SRED, svecha(1830, 700, t, .3, 1.6, 110))
    s += SL(Z_SRED, teplo(1830, 660, 420, 360, .3 + .1 * abs(A.w(t, 1.7))))
    s += SL(Z_SRED, lampa(560, 250, t, 1.3, False))
    s += SL(Z_SRED, teplo(560, 290, 860, 720, .46 + .1 * abs(A.w(t, 1.4))))
    # крюк в стене — от него идёт коса
    kx_, ky_ = 500, 620
    s += SL(Z_SRED, f'<rect x="{kx_-52:.0f}" y="{ky_-60:.0f}" width="104"'
                    f' height="112" rx="12" fill="#6b7278" {o(6)}/>')
    for i in (-1, 1):                    # шляпки гвоздей на пластине крюка
        s += SL(Z_SRED, f'<circle cx="{kx_+i*32:.0f}" cy="{ky_-32:.0f}" r="10"'
                        f' fill="#cfd6dc" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{kx_:.0f},{ky_+50:.0f} q70,60 6,122" fill="none"'
                    f' stroke="#9aa1a8" stroke-width="30" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M{kx_:.0f},{ky_+50:.0f} q70,60 6,122" fill="none"'
                    f' stroke="#e8eef6" stroke-width="7" opacity=".4"/>')
    s += SL(Z_SRED, lavka(700, 930, 620))
    # ДЕД крупно на лавке
    gx = 980
    s += SL(Z_SRED, figura(gx, 930, 520, t, "#3a3040", "#ffd98a", False, .2,
                           True, 1.0, False, 1.2, True))
    # КОСА ИЗ ТРЁХ ПОЛОС: короткий пролёт, явный перехлёст
    kos = ""
    for i in range(3):
        col = ("#7d5428", "#a07340", "#59391c")[i]
        d = f'M{kx_+16:.0f},{ky_+100:.0f}'
        for j in range(14):
            p = j / 13
            xx = kx_ + 30 + p * (gx - kx_ - 120)
            fz = p * 7.4 + i * 2.1 + t * 2.0
            yy = ky_ + 120 + p * 60 + math.sin(fz) * 54
            d += f' L{xx:.0f},{yy:.0f}'
        kos += (f'<path d="{d}" fill="none" stroke="{K}" stroke-width="44"'
                f' stroke-linecap="round" opacity=".9"/>')
        kos += (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="34"'
                f' stroke-linecap="round"/>')
        kos += (f'<path d="{d}" fill="none" stroke="#e4c79a" stroke-width="5"'
                f' opacity=".3"/>')
    s += SL(Z_SRED, kos)
    s += SL(Z_SRED, f'<path d="M{gx-70:.0f},{930-520*.80:.0f} l-110,52"'
                    f' stroke="#7d5428" stroke-width="22" stroke-linecap="round"/>')
    # готовая коса уходит к внуку одной толстой плетёнкой
    rost = A.ease(A.seg(t, .6, 2.2))
    vx = 1300
    s += SL(Z_SRED, figura(vx, 1050, 360, t, "#6b3a44", "#ffd98a", False, .6,
                           True, 1.0, False, 1.4, False, False))
    ruk, (rx_, ry_) = rukav(vx - 80, 850, 150, -40 + 16 * A.w(t, 1.0), t,
                            "#6b3a44", "#ffd98a", .3, 7.0)
    s += SL(Z_SRED, ruk)
    gotov = (f'<path d="M{gx+70:.0f},{790:.0f} q{(rx_-gx)*.5:.0f},{40:.0f}'
             f' {rx_-gx-20:.0f},{ry_-790:.0f}" fill="none" stroke="#59391c"'
             f' stroke-width="{26+14*rost:.0f}" stroke-linecap="round"/>')
    for i in range(8):                   # перехлёсты готовой косы
        p = i / 7
        gotov += (f'<ellipse cx="{gx+70+(rx_-gx-20)*p:.0f}"'
                  f' cy="{790+(ry_-790)*p+8*A.w(t,1.6,p):.0f}" rx="22" ry="15"'
                  f' fill="#a07340" {o(3)}/>')
    s += SL(Z_SRED, gotov)
    # ЛОШАДКА-МЕЧТА целиком, в открытом воздухе над лавкой
    pr = A.ease(A.seg(t, 1.2, 1.2))
    lgx, lgy = 1300, 660
    s += SL(Z_SRED, teplo(lgx - 70, lgy - 140, 620, 520, .2 * pr))
    s += SL(Z_SRED, _loshadka(lgx, lgy, 1.35, t, .70 + .28 * pr))
    for i in range(14):                  # пунктир мечты вокруг лошадки
        a = i * .449
        s += SL(Z_SRED, f'<circle cx="{lgx-100+math.cos(a)*280:.0f}"'
                        f' cy="{lgy-200+math.sin(a)*200:.0f}" r="6"'
                        f' fill="#ffe6b8" opacity="{.45*pr:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M{rx_:.0f},{ry_:.0f} q{(lgx-rx_)*.5:.0f},{-90:.0f}'
                    f' {lgx+100-rx_:.0f},{lgy-180-ry_:.0f}" fill="none"'
                    f' stroke="#a07340" stroke-width="13"'
                    f' opacity="{.4+.5*pr:.2f}"/>')
    # обрезки кожи и шило на лавке
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M{760+i*74:.0f},{916:.0f} q24,{-14-i*2:.0f} 52,2'
                        f' l-7,16 q-24,{-11:.0f} -48,2 Z" fill="#5f4126"'
                        f' opacity=".95" {o(3)}/>')
    s += SL(Z_SRED, f'<line x1="700" y1="912" x2="766" y2="872" stroke="#cfd6dc"'
                    f' stroke-width="8" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<rect x="672" y="902" width="44" height="24" rx="8"'
                    f' fill="#6b4a2a" {o(4)}/>')
    s += SL(Z_SRED, _chugunok(1760, 1012, 1.2, t, True))
    s += SL(Z_SRED, kot(300, 1012, t, 1.3, "#3b3430", False))
    s += SL(Z_SRED, _valenok(170, 1012, .9, t, .4, False, "#7d6f5e"))
    s += SL(Z_PERED, ramka_pp("levo", "#1c140d", .76))
    s += SL(Z_LETIT, iskra_let(t, 560, 310, 6, 977, 300, .4))
    s += vinetka(.46)
    return s


# ── 78 ─────────────────────────────────────────────────────────────────────
def valenki_shkaf_i_varezhki_na_rezink(t):
    """Городская прихожая: пара детских валенок с галошами сушится на чугунной
    батарее, из приоткрытого шкафа выплывает нафталиновое облачко, девочка
    морщит нос, варежки качаются на резинке из рукавов."""
    rnd = random.Random(7829)
    s = f'<rect width="{W}" height="{H}" fill="#2b2622"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#6f655c"/>')
    for i in range(11):                  # обои в полоску
        s += SL(Z_DAL, f'<rect x="{i*176:.0f}" y="0" width="86" height="840"'
                       f' fill="#7d7266" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect y="820" width="{W}" height="36" fill="#8d7f6e" {o(5)}/>')
    s += SL(Z_DAL, polovicy(856, "#6b4a2a"))
    s += SL(Z_DAL, kvartira_veschi(1480, 240, 420, t, 983))
    s += SL(Z_SRED, tusklaya_lampochka(960, 130, t, 1.5, True))
    # ШКАФ слева, дверца приоткрыта, из него плывёт облачко нафталина
    otk = A.ease(A.seg(t, .6, 1.3))
    s += SL(Z_SRED, _shkaf(90, 180, 520, 680, t, .5 * otk, True))
    for i in range(6):                   # нафталиновое облачко
        k = ((t * .34) + i * .17) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{470+k*320:.0f}" cy="{520-k*200:.0f}"'
                        f' rx="{54+86*k:.0f}" ry="{40*0+36+56*k:.0f}"'
                        f' fill="#e2f0f8" opacity="{.62*(1-k)*otk:.2f}"/>')
    s += SL(Z_SRED, _veshalka(640, 230, 420, t, 4, True))
    # БАТАРЕЯ и ВАЛЕНКИ на ней — главный предмет кадра
    bx, by, bw, bh = 900, 620, 660, 300
    s += SL(Z_SRED, _batareya(bx, by, bw, bh, t, 10))
    s += SL(Z_SRED, f'<rect x="{bx-40:.0f}" y="{by+bh:.0f}" width="{bw+80:.0f}"'
                    f' height="24" rx="8" fill="#8d949b" {o(5)}/>')
    for i, px in ((0, bx + 170), (1, bx + 420)):
        s += SL(Z_SRED, _valenok(px, by - 56, 2.05, t, .2 + i * .45, True,
                                 "#bda98a", -6 + i * 12))
        s += SL(Z_SRED, par(px, by - 430, t, 4, .5, 210, .42, 1.0))
    s += SL(Z_SRED, teplo(bx + bw / 2, by + bh * .4, 620, 420, .26))
    # варежки на резинке, продетой через рукава
    rez_y = 400
    s += SL(Z_SRED, f'<path d="M640,{rez_y:.0f} q{130:.0f},'
                    f'{80+10*A.w(t,2.0):.0f} {280:.0f},{-14:.0f}" fill="none"'
                    f' stroke="#c2ab86" stroke-width="8"/>')
    s += SL(Z_SRED, _varezhka(700, rez_y + 110, 1.6, t, .1, TKAN, True))
    s += SL(Z_SRED, _varezhka(880, rez_y + 76, 1.6, t, .55, TKAN2, True))
    # девочка морщит нос
    dx_ = 1730
    s += SL(Z_SRED, figura(dx_, 1050, 480, t, "#5b2f3a", "#ffd0a0", False, .35,
                           True, 1.0, False, 1.4, False, False))
    mor = A.ease(A.seg(t, 1.6, .5))
    s += SL(Z_SRED, f'<path d="M{dx_+36:.0f},{1050-480*.84:.0f}'
                    f' q{14:.0f},{-10-8*mor:.0f} {26:.0f},{2:.0f}" fill="none"'
                    f' stroke="#b08763" stroke-width="7" opacity="{.4+.6*mor:.2f}"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{dx_-10+i*14:.0f},{1050-480*.90:.0f}'
                        f' q6,{-14*mor:.0f} 12,0" fill="none" stroke="#9c7a5a"'
                        f' stroke-width="5" opacity="{.7*mor:.2f}"/>')
    ruk, (kx, ky) = rukav(dx_ - 90, 760, 170, 212 - 20 * mor, t, "#5b2f3a",
                          "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="26" ry="20"'
                    f' fill="#5b2f3a" {o(4)}/>')
    # коврик, галоши и ведро у двери
    s += SL(Z_SRED, f'<rect x="700" y="990" width="520" height="70" rx="12"'
                    f' fill="{TKAN2}" {o(6)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<line x1="{720+i*58:.0f}" y1="992" x2="{720+i*58:.0f}"'
                        f' y2="1058" stroke="#2f4a62" stroke-width="7" opacity=".7"/>')
    s += SL(Z_SRED, _botinok(1340, 1012, .86, t, .3, "#3a3630", .2))
    s += SL(Z_SRED, _botinok(1470, 1012, .82, t, .7, "#3a3630", .2))
    s += SL(Z_SRED, hodiki(250, 940, t, 1.2))
    s += SL(Z_SRED, kot(560, 1012, t, 1.15, "#4a4440", True))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="70" height="1080" fill="#1d1a16"'
                     f' opacity=".9"/>')
    s += vinetka(.44)
    return s


# ── 79 ─────────────────────────────────────────────────────────────────────
def tulup_s_gvozdya_i_chemodan_s_zimni(t):
    """Кадр надвое: слева сени — хозяин снимает с гвоздя овчинный тулуп и
    встряхивает его, валенки встают к печной дверце; справа городская комната,
    где щёлкают замки чемодана и шапки выскакивают пружиной."""
    rnd = random.Random(7919)
    s = f'<rect width="{W}" height="{H}" fill="#1e1812"/>'
    # ── левая половина: сени
    s += SL(Z_DAL, brevna(0, 0, 960, 840, 114))
    s += SL(Z_DAL, f'<rect width="960" height="840" fill="#271d14" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(840, "url(#pol)"))
    s += SL(Z_DAL, f'<rect y="840" width="960" height="240" fill="#3a2a1c"'
                   f' opacity=".55"/>')
    s += SL(Z_DAL, mebel_hlam(40, 820, 260, t, 991))
    # печь с дверцей, к ней ставят валенки
    s += SL(Z_SRED, pech(640, 300, 330, 540, t, True, True, False))
    px_, py_, pw_, ph2 = 686, 520, 240, 200
    s += SL(Z_SRED, kirpich_ustya(px_, py_, pw_, ph2, t, True))
    put = kontur_proema(px_, py_, pw_, ph2, "ustie")
    s += SL(Z_SRED, f'<path d="{put}" fill="#190b05"/>'
                    + ugli(px_ + 24, py_ + ph2 - 24, pw_ - 48, t, 7, 997)
                    + ogon(px_ + pw_ / 2, py_ + ph2 - 20, t, .95, .2, 6))
    s += SL(Z_SRED, teplo(px_ + pw_ / 2, py_ + ph2 * .7, 520, 440,
                          .46 + .12 * abs(A.w(t, 1.6))))
    vst = A.ease(A.seg(t, 1.8, 1.2))
    for i, sg in ((0, -1), (1, 1)):
        vxx = 300 + (px_ - 240 - 300) * vst + sg * 70
        s += SL(Z_SRED, _valenok(vxx, 850 - math.sin(vst * 3.14159) * 70, 1.25, t,
                                 .2 + i * .4, False, "#7d6f5e", sg * 8))
    # гвоздь и тулуп, который встряхивают
    s += SL(Z_SRED, f'<circle cx="250" cy="300" r="22" fill="#9aa1a8" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="244" cy="294" r="8" fill="#e8eef6" opacity=".7"/>')
    snyat = A.ease(A.seg(t, .3, 1.1))
    tx_ = 250 + snyat * 120
    ty_ = 220 + snyat * 110
    tryas = max(0.0, A.w(t, .8, .1)) * snyat
    s += SL(Z_SRED, _tulup_vis(tx_ + 80, ty_, 440, 580, t, .2, tryas))
    for i in range(9):                   # пыль и шерстинки при встряхивании
        k = ((t * 1.1) + i * .11) % 1.0
        s += SL(Z_SRED, f'<circle cx="{tx_+rnd.uniform(-170,170):.0f}"'
                        f' cy="{ty_+260+rnd.uniform(-120,120)-k*80:.0f}"'
                        f' r="{5+9*k:.0f}" fill="#e4d6bc"'
                        f' opacity="{.5*(1-k)*tryas:.2f}"/>')
    s += SL(Z_SRED, figura(300, 1046, 580, t, "#3a3346", "#ffd98a", False, .2,
                           True, 1.0, False, 1.2, True))
    ruk, _ = rukav(370, 690, 150, -46 + 30 * tryas, t, "#3a3346", "#ffd98a",
                   .1, 7.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, para_izo_rta(222, 690, t, .3, 1.0, .45))
    # ── правая половина: городская комната
    s += SL(Z_DAL, f'<rect x="960" width="960" height="1080" fill="#6a6056"/>')
    for i in range(6):
        s += SL(Z_DAL, f'<rect x="{980+i*160:.0f}" y="0" width="76" height="880"'
                       f' fill="#786d61" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(880, "#6b4a2a"))
    s += SL(Z_DAL, kvartira_veschi(1560, 230, 360, t, 1009))
    s += SL(Z_SRED, tusklaya_lampochka(1440, 150, t, 1.35, True))
    # чемодан на пол-кадра, замки щёлкают, крышка откидывается
    chx, chy, chw, chh = 1100, 690, 680, 300
    shchel = A.ease(A.seg(t, 1.0, .6))
    otk = A.out(A.seg(t, 1.7, 1.0))
    ch = ten(chx + chw / 2, chy + chh + 18, chw * .45, 22, .5)
    ch += (f'<rect x="{chx}" y="{chy}" width="{chw}" height="{chh}" rx="18"'
           f' fill="#6b4a2a" {o(9)}/>')
    ch += (f'<rect x="{chx+20}" y="{chy+30}" width="{chw-40}" height="{chh-60}"'
           f' rx="10" fill="none" stroke="#4f351c" stroke-width="10"/>')
    for i in (0, 1):
        ch += (f'<rect x="{chx+chw*(.22+i*.42):.0f}" y="{chy-16:.0f}" width="90"'
               f' height="{34+10*shchel:.0f}" rx="8" fill="url(#zhel)" {o(5)}/>')
        ch += (f'<circle cx="{chx+chw*(.22+i*.42)+45:.0f}" cy="{chy+2:.0f}" r="12"'
               f' fill="{ZOL}" opacity="{.5+.5*shchel:.2f}"/>')
    ch += (f'<g transform="rotate({-34*otk:.1f} {chx:.0f} {chy:.0f})">'
           f'<rect x="{chx}" y="{chy-170}" width="{chw}" height="170" rx="14"'
           f' fill="#7d5636" {o(8)}/>'
           f'<rect x="{chx+26}" y="{chy-148}" width="{chw-52}" height="124" rx="10"'
           f' fill="none" stroke="#4f351c" stroke-width="9"/>'
           f'<rect x="{chx+chw*.42:.0f}" y="{chy-186}" width="{chw*.16:.0f}"'
           f' height="24" rx="8" fill="url(#zhel)" {o(4)}/></g>')
    ch += (f'<path d="M{chx+chw*.44:.0f},{chy+chh:.0f} h{chw*.12:.0f} l0,34'
           f' h{-chw*.12:.0f} Z" fill="#4f351c" {o(4)}/>')
    s += SL(Z_SRED, ch)
    # шапки выскакивают из чемодана пружиной
    for i in range(3):
        vy_ = A.over(A.seg(t, 1.9 + i * .34, .7)) * (1.0 + i * .45)
        s += SL(Z_SRED, _shapka_meh(chx + 140 + i * 210,
                                    chy + 30 - vy_ * (230 + i * 30), 1.45, t,
                                    .2 + i * .3, 0.0))
        s += SL(Z_SRED, f'<path d="M{chx+150+i*200:.0f},{chy+60:.0f}'
                        f' q{14:.0f},{-60*vy_:.0f} 0,{-120*vy_:.0f}" fill="none"'
                        f' stroke="#9aa1a8" stroke-width="7" opacity="{.6*vy_:.2f}"'
                        f' stroke-dasharray="14 10"/>')
    s += SL(Z_SRED, _varezhka(1760, 760, 1.1, t, .3, TKAN, True))
    s += SL(Z_SRED, f'<rect x="950" y="0" width="22" height="1080" fill="#15110d"'
                    f' opacity=".85"/>')
    s += SL(Z_SRED, kot(1760, 1012, t, 1.1, "#4a4440", False))
    s += SL(Z_PERED, ramka_pp("levo", "#100c09", .8))
    s += SL(Z_PERED, _valenok(1020, 1012, 1.0, t, .5, True, "#6e6358"))
    s += SL(Z_LETIT, iskra_let(t, px_ + pw_ / 2, py_ + 30, 6, 1013, 260, .4))
    s += vinetka(.46)
    return s


# ── 80 ─────────────────────────────────────────────────────────────────────
def shapka_na_prosvet(t):
    """Меховую шапку поднимают к лампе и раздвигают мех на просвет: из меха
    вылетает одна наглая моль с салфеткой на шее, ладони хлопают мимо,
    а на столе уже ждут мешочки лаванды."""
    rnd = random.Random(8011)
    s = f'<rect width="{W}" height="{H}" fill="#241c18"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 110, True, "dosk"))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#3a2c22" opacity=".55"/>')
    s += SL(Z_DAL, polovicy(900, "url(#pol)"))
    s += SL(Z_DAL, kvartira_veschi(60, 260, 380, t, 1019))
    # ЛАМПА — источник просвета
    lx, ly = 980, 300
    s += SL(Z_SRED, lampa(lx, ly, t, 1.7, True))
    s += SL(Z_SRED, teplo(lx, ly + 40, 900, 760, .5 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, luch(lx - 170, ly + 60, 340, 620, t, .17))
    # ШАПКА НА ПРОСВЕТ, крупно: мех раздвигается
    razd = A.ease(A.seg(t, .4, 1.0))
    shx, shy = lx, ly + 420
    s += SL(Z_SRED, _shapka_meh(shx, shy, 2.1, t, .1, razd))
    s += SL(Z_SRED, f'<ellipse cx="{shx:.0f}" cy="{shy-150:.0f}" rx="{90*razd:.0f}"'
                    f' ry="{150*razd:.0f}" fill="{SVET}" opacity="{.26*razd:.2f}"/>')
    # рукава держат шапку с двух сторон, без кистей
    for i, sg in ((0, -1), (1, 1)):
        ruk, (kx, ky) = rukav(shx + sg * 420, shy + 190, 140,
                              (-160 if sg > 0 else -20) + sg * 10 * A.w(t, 1.1, i * .3),
                              t, "#43394a", "#ffd98a", .2 + i * .3, 5.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="34" ry="26"'
                        f' fill="#43394a" {o(5)}/>')
    # МОЛЬ вылетает из меха и нагло кружит
    vyl = A.ease(A.seg(t, 1.2, 1.4))
    mx = shx + 60 + vyl * 420
    my = shy - 170 - vyl * 230 + 40 * A.w(t, .9)
    s += SL(Z_SRED, _mol(mx, my, 2.3, t, .2))
    for i in range(7):                   # пыльца с крыльев
        k = ((t * .7) + i * .14) % 1.0
        s += SL(Z_SRED, f'<circle cx="{mx-40-k*90:.0f}" cy="{my+30+k*70:.0f}"'
                        f' r="{4+4*k:.0f}" fill="#e8dcc0" opacity="{.6*(1-k)*vyl:.2f}"/>')
    # ладони хлопают мимо — два рукава сходятся
    hlop = max(0.0, A.w(t, 1.3, .4)) * A.ease(A.seg(t, 2.0, .5))
    for sg in (-1, 1):
        hx = mx + sg * (210 - 170 * hlop)
        s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{my+40:.0f}" rx="52" ry="34"'
                        f' fill="#3f3546" transform="rotate({sg*-24:.0f} {hx:.0f}'
                        f' {my+40:.0f})" {o(5)}/>')
        s += SL(Z_SRED, f'<line x1="{hx+sg*44:.0f}" y1="{my+56:.0f}"'
                        f' x2="{hx+sg*180:.0f}" y2="{my+150:.0f}" stroke="#3f3546"'
                        f' stroke-width="34" stroke-linecap="round"/>')
    if hlop > .8:
        for i in range(6):
            a = -2.6 + i * .5
            s += SL(Z_SRED, f'<line x1="{mx+math.cos(a)*70:.0f}"'
                            f' y1="{my+40+math.sin(a)*70:.0f}"'
                            f' x2="{mx+math.cos(a)*130:.0f}"'
                            f' y2="{my+40+math.sin(a)*130:.0f}" stroke="#ffe6b8"'
                            f' stroke-width="8" opacity=".6"/>')
    # стол: мешочки лаванды ложатся в шапки
    s += SL(Z_SRED, stol(1380, 880, 520, 40, True))
    for i in range(3):
        lv = A.ease(A.seg(t, 2.2 + i * .3, .7))
        mxx = 1440 + i * 170
        s += SL(Z_SRED, f'<path d="M{mxx-66:.0f},{880-lv*40:.0f}'
                        f' q{-26:.0f},{-86:.0f} {18:.0f},{-120:.0f}'
                        f' q{48:.0f},{-18:.0f} {96:.0f},0 q{44:.0f},{34:.0f}'
                        f' {18:.0f},{120:.0f} Z" fill="#cbbb93" opacity=".97"'
                        f' {o(6)}/>')
        for j in range(4):               # складки холста
            s += SL(Z_SRED, f'<path d="M{mxx-44+j*30:.0f},{870-lv*40:.0f}'
                            f' q{4:.0f},{-46:.0f} {0:.0f},{-88:.0f}"'
                            f' fill="none" stroke="#b0a07c" stroke-width="6"'
                            f' opacity=".7"/>')
        s += SL(Z_SRED, f'<path d="M{mxx-52:.0f},{766-lv*40:.0f} q{52:.0f},{-26:.0f}'
                        f' {104:.0f},0" fill="none" stroke="#8a6238"'
                        f' stroke-width="14"/>')
        for j in range(4):               # веточки лаванды торчат
            s += SL(Z_SRED, f'<line x1="{mxx-20+j*14:.0f}" y1="{790-lv*40:.0f}"'
                            f' x2="{mxx-26+j*16+3*A.w(t,2.0,j*.2):.0f}"'
                            f' y2="{748-lv*40:.0f}" stroke="#7a6a9a"'
                            f' stroke-width="6"/>')
    s += SL(Z_SRED, _chugunok(1700, 880, 1.2, t, False))
    s += SL(Z_SRED, figura(560, 1070, 520, t, "#43394a", "#ffd98a", False, .25,
                           True, 1.0, False, 1.0, True))
    s += SL(Z_SRED, _varezhka(300, 820, 1.2, t, .3, TKAN, True))
    s += SL(Z_SRED, _valenok(240, 1012, .9, t, .5, False, "#7d6f5e"))
    s += SL(Z_PERED, ramka_pp("pravo", "#120e0b", .82))
    s += SL(Z_PERED, _shkaf(1760, 120, 220, 760, t, .18, False))
    s += SL(Z_LETIT, iskra_let(t, lx, ly + 60, 6, 1021, 240, .35))
    s += vinetka(.48)
    return s


# ── 81 ─────────────────────────────────────────────────────────────────────
def botinki_s_gazetoy_i_kremom(t):
    """Пара зимних ботинок на расстеленной газете: от них идёт пар, газета
    комкается и уходит внутрь, щётка с кремом наводит блеск на носок,
    а за окном падает первая снежинка."""
    rnd = random.Random(8111)
    s = f'<rect width="{W}" height="{H}" fill="#2a241e"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#726758"/>')
    for i in range(8):                   # кафельный поясок прихожей
        s += SL(Z_DAL, f'<rect x="{i*244:.0f}" y="520" width="226" height="190"'
                       f' rx="6" fill="#8d8172" opacity=".55" {o(3)}/>')
    s += SL(Z_DAL, f'<rect y="700" width="{W}" height="30" fill="#8d7f6e" {o(5)}/>')
    s += SL(Z_DAL, polovicy(730, "#6b4a2a"))
    s += SL(Z_DAL, kvartira_veschi(70, 180, 340, t, 1031))
    # окно справа: за ним падает снежинка
    okx, oky, okw, okh = 1420, 120, 420, 440
    vid = (f'<rect x="{okx}" y="{oky}" width="{okw}" height="{okh}"'
           f' fill="url(#nsumer)"/>')
    for i in range(4):
        vid += (f'<rect x="{okx+40+i*96:.0f}" y="{oky+okh*.5:.0f}" width="70"'
                f' height="{okh*.5:.0f}" fill="#3a4254" opacity=".9"/>')
        if i % 2:
            vid += (f'<rect x="{okx+58+i*96:.0f}" y="{oky+okh*.58:.0f}" width="30"'
                    f' height="30" fill="{SVET}" opacity=".5"/>')
    sn = ((t * .3) % 1.0)
    vid += (f'<circle cx="{okx+okw*.5+30*A.w(t,2.4):.0f}" cy="{oky+sn*okh:.0f}"'
            f' r="11" fill="#f2f8ff" opacity=".95"/>')
    for i in range(5):
        a = i * 1.25
        vid += (f'<line x1="{okx+okw*.5+30*A.w(t,2.4):.0f}" y1="{oky+sn*okh:.0f}"'
                f' x2="{okx+okw*.5+30*A.w(t,2.4)+math.cos(a)*20:.0f}"'
                f' y2="{oky+sn*okh+math.sin(a)*20:.0f}" stroke="#f2f8ff"'
                f' stroke-width="4" opacity=".8"/>')
    s += SL(Z_SRED, okno_izby(okx, oky, okw, okh, t, vid, .25, False, True))
    s += SL(Z_SRED, tusklaya_lampochka(700, 120, t, 1.4, True))
    # батарея, к которой ставят ботинки
    s += SL(Z_SRED, _batareya(1180, 560, 420, 230, t, 7))
    # ГАЗЕТА и ПАРА БОТИНОК на ней — крупно
    s += SL(Z_SRED, _gazeta_list(760, 930, 820, 320, t, -3, 1033, 0.0))
    s += SL(Z_SRED, _gazeta_list(1120, 960, 600, 260, t, 5, 1039, 0.0))
    pere = A.ease(A.seg(t, .4, 1.0))
    bl = A.ease(A.seg(t, 2.4, 1.2))
    for i, sg in ((0, -1), (1, 1)):
        bxx = 760 + sg * 145 + pere * 150
        s += SL(Z_SRED, _botinok(bxx, 900 + i * 14, 2.0, t, .2 + i * .4,
                                 "#4a3526", bl))
        s += SL(Z_SRED, par(bxx, 760, t, 4, .55, 220, .44, 1.0))
    s += SL(Z_SRED, teplo(1300, 700, 560, 420, .28))
    # комок газеты летит в ботинок
    kom = A.ease(A.seg(t, 1.3, 1.0))
    s += SL(Z_SRED, _gazeta_list(520 + kom * 380, 700 - math.sin(kom * 3.14159) * 160,
                                 300, 220, t, 14 + kom * 90, 1049, kom))
    # щётка ходит по носку
    hod = A.w(t, .8, .1)
    s += SL(Z_SRED, _shchetka(1360 + hod * 90, 880, 1.5, t, -12 + 8 * hod))
    s += SL(Z_SRED, f'<rect x="1660" y="960" width="130" height="80" rx="14"'
                    f' fill="#3f3a36" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1725" cy="960" rx="65" ry="18" fill="#6b645c"'
                    f' {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1725" cy="958" rx="48" ry="12" fill="#23211e"'
                    f' opacity=".9"/>')
    # рукава работают: один держит ботинок, другой ведёт щётку
    ruk, (kx, ky) = rukav(1140, 600, 170, 66 + 14 * hod, t, "#3f4a5e",
                          "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="32" ry="24"'
                    f' fill="#3f4a5e" {o(5)}/>')
    s += SL(Z_SRED, figura(250, 1070, 520, t, "#3f4a5e", "#ffd98a", False, .3,
                           True, 1.0, False, 1.0, False, False))
    s += SL(Z_SRED, _valenok(1760, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_SRED, kot(1540, 1012, t, 1.15, "#3b3430", True))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="80" height="1080" fill="#1a1612"'
                     f' opacity=".9"/>')
    s += SL(Z_PERED, _chashka(170, 1012, 1.5, t, .2, KREM, True))
    s += SL(Z_PERED, par(130, 960, t, 3, .4, 160, .4, .8))
    s += vinetka(.46)
    return s


# ── 82 ─────────────────────────────────────────────────────────────────────
def zhena_derzhit_muzha_za_kushak(t):
    """Ворота двора: муж в шапке набекрень уже взялся за кольцо калитки и
    подмигивает приятелям за забором, а жена держит его за кушак, упёршись
    лаптями в землю. Справа у избы накрытый стол и численник на стене."""
    rnd = random.Random(8221)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 1051)
    s += oblaka(t, 170, 5, 1061, .32, "#c8d4e2", 15.0)
    s += SL(Z_DAL, ulica_dal(60, 660, 820, t, False, 1063))
    s += SL(Z_DAL, izba_snaruzhi(1500, 720, 420, t, True, True, 1069))
    s += SL(Z_DAL, goloe_derevo(760, 700, 400, t, 1087, 6, "#303240"))
    s += SL(Z_DAL, gryaz_polosa(740, 220, "#443f36"))
    s += SL(Z_DAL, sneg_lezhit(900, 22, "url(#sneg)"))
    # ВОРОТА ДВОРА на пол-кадра: столбы, тёс, кольцо калитки
    vx, vy, vw, vh = 150, 260, 540, 820
    vor = (f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="8"'
           f' fill="url(#dosk)" {o(10)}/>')
    for i in range(9):
        vor += (f'<rect x="{vx+14+i*(vw-28)/9:.0f}" y="{vy+10}"'
                f' width="{(vw-28)/9-10:.0f}" height="{vh-20}" rx="6"'
                f' fill="url(#dosk)" {o(5)}/>')
    vor += (f'<path d="M{vx-50},{vy+10} h{vw+100} l-60,-90 h{-vw+20} Z"'
            f' fill="{DOSKA2}" {o(9)}/>')
    vor += (f'<rect x="{vx-70}" y="{vy-20}" width="80" height="{vh+20}" rx="10"'
            f' fill="url(#derev)" {o(9)}/>')
    vor += (f'<rect x="{vx+vw-10:.0f}" y="{vy-20}" width="80" height="{vh+20}" rx="10"'
            f' fill="url(#derev)" {o(9)}/>')
    vor += (f'<line x1="{vx+40}" y1="{vy+vh*.34:.0f}" x2="{vx+vw-40:.0f}"'
            f' y2="{vy+vh*.22:.0f}" stroke="#6b4a2a" stroke-width="22"/>')
    s += SL(Z_SRED, vor)
    s += SL(Z_SRED, podkova(vx + vw / 2, vy - 110, 2.3, t, "url(#zhel)"))
    kol = 3.0 * A.w(t, 1.2, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kol:.2f} {vx+vw-120:.0f} {vy+vh*.52:.0f})">'
                    f'<circle cx="{vx+vw-120:.0f}" cy="{vy+vh*.58:.0f}" r="42"'
                    f' fill="none" stroke="url(#zhel)" stroke-width="16"/>'
                    f'<rect x="{vx+vw-134:.0f}" y="{vy+vh*.48:.0f}" width="28"'
                    f' height="30" rx="8" fill="#5d6168" {o(4)}/></g>')
    # приятели машут из-за забора
    s += SL(Z_DAL, pleten(1380, 700, 480, 210, 9))
    for i, fx_ in ((0, 1450), (1, 1600), (2, 1740)):
        s += SL(Z_DAL, figura(fx_, 700, 230 + i * 20, t, "#2e3a46", "#cfe4f5", False,
                              .2 * i, True, 1.0, False, 1.0, i == 2, i != 2))
        mah = -40 - 36 * A.w(t, .8, i * .3)
        ruk, _ = rukav(fx_ + 40, 560, 130, mah, t, "#2e3a46", "#cfe4f5", i * .3, 10.0)
        s += SL(Z_DAL, ruk)
    # муж у кольца калитки, жена держит за кушак
    mx = 830 - 40 * A.ease(A.seg(t, .4, 1.6))
    s += SL(Z_SRED, figura(mx, 1060, 540, t, "#3a3346", "#ffd0a0", False, .1,
                           True, 1.0, True, -3.0, True, True))
    s += SL(Z_SRED, para_izo_rta(mx + 64, 690, t, .2, 1.3, .55))
    ruk, (kx, ky) = rukav(mx + 70, 760, 230, -22 + 8 * A.w(t, 1.1), t,
                          "#3a3346", "#ffd0a0", .1, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="34" ry="26"'
                    f' fill="#3a3346" {o(5)}/>')
    zx = 1180
    s += SL(Z_SRED, figura(zx, 1066, 500, t, "#5b2f3a", "#ffd0a0", True, .4,
                           True, 1.0, False, 4.0))
    s += SL(Z_SRED, para_izo_rta(zx - 60, 700, t, .6, 1.2, .5))
    # КУШАК НАТЯНУТ СТРУНОЙ между ними
    nat = .4 + .6 * abs(A.w(t, .7, .1))
    kus = (f'<path d="M{mx+30:.0f},{830:.0f} q{(zx-mx)*.5:.0f},{60-40*nat:.0f}'
           f' {zx-mx-110:.0f},{10:.0f}" fill="none" stroke="{TKAN}"'
           f' stroke-width="{30+8*nat:.0f}" stroke-linecap="round"/>')
    kus += (f'<path d="M{mx+30:.0f},{830:.0f} q{(zx-mx)*.5:.0f},{60-40*nat:.0f}'
            f' {zx-mx-110:.0f},{10:.0f}" fill="none" stroke="#f0d3a8"'
            f' stroke-width="6" opacity=".5"/>')
    for i in range(5):                   # кисти кушака трясутся
        kus += (f'<path d="M{zx-80+i*12:.0f},{842:.0f} q{6:.0f},{40:.0f}'
                f' {-4+8*A.w(t,1.1,i*.2):.0f},{72:.0f}" fill="none" stroke="{TKAN}"'
                f' stroke-width="9" stroke-linecap="round"/>')
    s += SL(Z_SRED, kus)
    ruk2, _ = rukav(zx - 70, 820, 180, 188 + 10 * A.w(t, .9, .3), t,
                    "#5b2f3a", "#ffd0a0", .4, 4.0)
    s += SL(Z_SRED, ruk2)
    for i in (-1, 1):                    # лапти жены упёрлись в землю
        s += SL(Z_SRED, f'<path d="M{zx+i*60-40:.0f},{1058:.0f} h80 q16,0 10,20'
                        f' h-96 q-10,-20 6,-20 Z" fill="#b78a46" {o(4)}/>')
        for j in range(4):
            s += SL(Z_SRED, f'<line x1="{zx+i*60-34+j*18:.0f}" y1="1060"'
                            f' x2="{zx+i*60-30+j*18:.0f}" y2="1076"'
                            f' stroke="#8a6534" stroke-width="5"/>')
    # стол у избы справа и численник: листки летят
    s += SL(Z_SRED, stol(1560, 900, 320, 36, True))
    s += SL(Z_SRED, karavay(1660, 896, .9, True))
    s += SL(Z_SRED, _chugunok(1760, 872, 1.0, t, True))
    s += SL(Z_SRED, svecha(1570, 790, t, .2, 1.8, 120))
    s += SL(Z_SRED, teplo(1570, 750, 560, 470, .44 + .1 * abs(A.w(t, 1.5))))
    for i in range(5):                   # листки численника летят по ветру
        k = ((t * .45) + i * .2) % 1.0
        s += SL(Z_LETIT, f'<g transform="rotate({k*160+i*30:.0f}'
                         f' {1540+k*300:.0f} {520-k*260:.0f})">'
                         f'<rect x="{1540+k*300:.0f}" y="{520-k*260:.0f}" width="54"'
                         f' height="72" rx="5" fill="url(#list)" opacity="{1-k*.6:.2f}"'
                         f' {o(3)}/>'
                         f'<path d="M{1550+k*300:.0f},{556-k*260:.0f} q16,4 34,0"'
                         f' fill="none" stroke="#7d756a" stroke-width="4"/></g>')
    s += SL(Z_SRED, kura(640, 1012, t, .9, .3))
    s += SL(Z_SRED, kura(720, 1012, t, .8, .7))
    s += SL(Z_PERED, ramka_pp("levo", "#141019", .8))
    s += SL(Z_PERED, goloe_derevo(1900, 1080, 640, t, 1091, 7, "#22242c"))
    s += SL(Z_LETIT, mokryy_sneg(t, 28, 1093, .5, 1.0))
    s += vinetka(.46)
    return s


# ── 83 ─────────────────────────────────────────────────────────────────────
def bolshoe_okno_s_lavkoy(t):
    """Широкое окно избы с частым переплётом на две трети кадра, под ним лавка
    и горшок с луком на подоконнике: дед усаживается смотреть небо, кот
    запрыгивает рядом. За стеклом идёт НАСТОЯЩЕЕ небо."""
    rnd = random.Random(8311)
    s = f'<rect width="{W}" height="{H}" fill="#3a2c20"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 120))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#2f2318" opacity=".42"/>')
    s += SL(Z_DAL, utvar_izby(1600, 220, 300, t, 1097))
    s += SL(Z_DAL, polovicy(900, "url(#pol)"))
    # печь краем кадра — единственное тёплое пятно в ровном дневном свете
    pch = (f'<rect x="-60" y="60" width="330" height="840" rx="18"'
           f' fill="url(#pech)" {o(9)}/>')
    pch += (f'<rect x="-40" y="20" width="290" height="44" rx="10" fill="{PECH2}"'
            f' {o(6)}/>')
    s += SL(Z_SRED, pch)
    s += SL(Z_SRED, kirpich_ustya(20, 450, 240, 230, t, True))
    s += SL(Z_SRED, f'<path d="{kontur_proema(20, 450, 240, 230, "ustie")}"'
                    f' fill="#190b05"/>'
                    + ugli(40, 660, 200, t, 8, 1103)
                    + ogon(140, 666, t, 1.15, .2, 6))
    s += SL(Z_SRED, teplo(140, 610, 560, 470, .46 + .12 * abs(A.w(t, 1.6))))
    # ОКНО: сначала нарисованный вид по форме проёма, потом метка, потом переплёт
    ox, oy, ow, oh = 400, 120, 1140, 620
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="bo83"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="url(#nden)"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#nden)"/>')
    for i in range(6):                   # облака за стеклом плывут
        k = ((t * .035) + i * .17) % 1.2 - .1
        cx_ = ox - 200 + k * (ow + 400)
        cy_ = oy + 90 + (i % 3) * 86
        za += (f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="{150+i*22:.0f}"'
               f' ry="{44+i*7:.0f}" fill="#eef3f8" opacity=".72"/>')
        za += (f'<ellipse cx="{cx_+90:.0f}" cy="{cy_+16:.0f}" rx="{110+i*14:.0f}"'
               f' ry="{34+i*5:.0f}" fill="#e2eaf2" opacity=".66"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.70:.0f}" width="{ow}" height="{oh*.30:.0f}"'
           f' fill="#8a9aa2" opacity=".55"/>')
    # кольцо вокруг солнца: иначе верх кадра — ровная заливка
    sx0, sy0 = ox + ow * .68, oy + oh * .26
    za += (f'<circle cx="{sx0:.0f}" cy="{sy0:.0f}" r="{150+6*A.w(t,2.6):.0f}"'
           f' fill="none" stroke="#fff3cf" stroke-width="22" opacity=".65"/>')
    za += (f'<circle cx="{sx0:.0f}" cy="{sy0:.0f}" r="{196+8*A.w(t,2.2):.0f}"'
           f' fill="none" stroke="#ffeeb8" stroke-width="9" opacity=".45"/>')
    za += (f'<circle cx="{sx0:.0f}" cy="{sy0:.0f}" r="56" fill="#fffaf0"'
           f' opacity=".9"/>')
    for i in range(6):               # птицы за стеклом тянутся клином
        k = ((t * .05) + i * .09) % 1.1
        bx_ = ox + 80 + k * (ow - 160)
        by_ = oy + 120 + i * 26 + 10 * A.w(t, 1.6, i * .2)
        za += (f'<path d="M{bx_:.0f},{by_:.0f} q14,-12 28,0 q14,-12 28,0"'
               f' fill="none" stroke="#4a5560" stroke-width="5" opacity=".7"/>')
    for i in range(5):                   # дальние избы и деревья за стеклом
        bx = ox + 60 + i * 230
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.64:.0f}" width="130"'
               f' height="{oh*.22:.0f}" fill="#7d8690" opacity=".8"/>')
        za += (f'<path d="M{bx-18:.0f},{oy+oh*.64:.0f} l83,-62 l83,62 Z"'
               f' fill="#6f7a85" opacity=".85"/>')
        za += (f'<path d="M{bx+180:.0f},{oy+oh*.66:.0f} l-26,0 l26,-72 l26,72 Z"'
               f' fill="#5e6a72" opacity=".8"/>')
    vid += f'<g clip-path="url(#bo83)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    # обвязка: частый переплёт, наличники, откосы
    ob = (f'<rect x="{ox-46}" y="{oy-46}" width="{ow+92}" height="{oh+92}" rx="10"'
          f' fill="none" stroke="url(#derev)" stroke-width="92"/>')
    for i in range(1, 6):                # частый переплёт по вертикали
        ob += (f'<rect x="{ox+i*ow/6-17:.0f}" y="{oy}" width="34"'
               f' height="{oh}" fill="url(#derev)"/>')
        ob += (f'<line x1="{ox+i*ow/6:.0f}" y1="{oy}" x2="{ox+i*ow/6:.0f}"'
               f' y2="{oy+oh}" stroke="{K}" stroke-width="4" opacity=".5"/>')
    for i in range(1, 4):
        ob += (f'<line x1="{ox}" y1="{oy+i*oh/4:.0f}" x2="{ox+ow}"'
               f' y2="{oy+i*oh/4:.0f}" stroke="url(#derev)" stroke-width="34"/>')
        ob += (f'<line x1="{ox}" y1="{oy+i*oh/4:.0f}" x2="{ox+ow}"'
               f' y2="{oy+i*oh/4:.0f}" stroke="{K}" stroke-width="4"'
               f' opacity=".5"/>')
    ob += (f'<path d="M{ox+30},{oy+40} l{ow*.36:.0f},{oh*.5:.0f}" stroke="#ffffff"'
           f' stroke-width="16" opacity=".16"/>')
    ob += f'<path d="{put}" fill="none" {o(10)}/>'
    ob += (f'<path d="M{ox-120},{oy-56} h{ow+240} l-66,-78 h{-ow-108} Z"'
           f' fill="{DOSKA2}" {o(9)}/>')
    for i in range(11):                  # резные зубцы наличника
        ob += (f'<path d="M{ox-96+i*(ow+192)/10:.0f},{oy-62} l32,-26 l32,26 Z"'
               f' fill="{MED}" opacity=".9" {o(3)}/>')
    ob += (f'<rect x="{ox-130}" y="{oy+oh+50}" width="{ow+260}" height="54" rx="10"'
           f' fill="url(#dosk)" {o(9)}/>')
    vid += ob
    s += SL(Z_SRED, vid)
    # подоконник с горшком лука
    s += SL(Z_SRED, f'<rect x="{ox-80}" y="{oy+oh+104}" width="{ow+160}" height="34"'
                    f' rx="8" fill="{DOSKA}" {o(6)}/>')
    gx, gy = ox + 190, oy + oh + 104
    s += SL(Z_SRED, f'<path d="M{gx-80:.0f},{gy-130:.0f} h160 l-20,130 h-120 Z"'
                    f' fill="url(#glina)" {o(7)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy-130:.0f}" rx="80" ry="20"'
                    f' fill="#9c6a3c" {o(5)}/>')
    for i in range(7):                   # перья лука покачиваются
        a = -1.1 + i * .34
        kach = 9 * A.w(t, 2.2, i * .17)
        s += SL(Z_SRED, f'<path d="M{gx+math.cos(a)*30:.0f},{gy-134:.0f}'
                        f' q{math.cos(a)*40+kach:.0f},{-80:.0f}'
                        f' {math.cos(a)*62+kach*1.6:.0f},{-168:.0f}" fill="none"'
                        f' stroke="{ZEL2}" stroke-width="{15-i}"'
                        f' stroke-linecap="round"/>')
        s += SL(Z_SRED, f'<ellipse cx="{gx+math.cos(a)*22:.0f}" cy="{gy-146:.0f}"'
                        f' rx="26" ry="20" fill="#c9a771" {o(3)}/>')
    # лавка под окном, дед усаживается, кот запрыгивает
    s += SL(Z_SRED, lavka(540, 880, 880))
    sad = A.ease(A.seg(t, .5, 1.4))
    s += SL(Z_SRED, figura(1300, 900 + 26 * sad, 520 - 70 * sad, t, "#3a3346",
                           "#ffd98a", False, .2, True, 1.0, True, 1.0, True))
    pr = A.ease(A.seg(t, 2.0, .9))
    s += SL(Z_SRED, kot(700, 880 + 180 * (1 - pr), t, 1.35, "#3b3430", False))
    s += SL(Z_SRED, f'<ellipse cx="700" cy="{886:.0f}" rx="70" ry="14"'
                    f' fill="#000000" opacity="{.3*pr:.2f}"/>')
    s += SL(Z_SRED, krynka(1620, 1012, 1.6))
    s += SL(Z_SRED, _valenok(300, 1012, .9, t, .4, False, "#7d6f5e"))
    s += SL(Z_SRED, _chashka(1480, 1012, 1.4, t, .3, KREM, True))
    s += SL(Z_SRED, par(1480, 968, t, 3, .4, 160, .4, .8))
    s += SL(Z_PERED, zanaveska(360, 60, 460, 200, RUSH, t, 1))
    s += SL(Z_PERED, zanaveska(1580, 60, 460, 200, RUSH, t, -1))
    s += vinetka(.42)
    return s


# ── 84 ─────────────────────────────────────────────────────────────────────
def ded_chitaet_nebo(t):
    """Дед на лавке вполоборота, очки на верёвочке, палец поднят: он читает
    небо, как газету, — по нему справа налево бегут рисованные строчки из
    облаков, а бабка рядом мелькает спицами."""
    rnd = random.Random(8419)
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, False, 1109)
    s += oblaka(t, 140, 5, 1117, .3, "#e4ebf2", 20.0)
    # облачные строчки бегут справа налево
    for r in range(5):                   # пять строк «слов» из облаков
        yy = 120 + r * 96
        for i in range(10):
            k = ((t * .07) + i * .105 + r * .04) % 1.25 - .12
            xx = W + 200 - k * (W + 500)
            ln = 56 + ((i * 37 + r * 19) % 110)
            s += SL(Z_NEBO, f'<path d="M{xx:.0f},{yy:.0f}'
                            f' q{ln*.16:.0f},-22 {ln*.33:.0f},0'
                            f' q{ln*.16:.0f},22 {ln*.33:.0f},0'
                            f' q{ln*.16:.0f},-22 {ln*.34:.0f},0"'
                            f' fill="none" stroke="#fbfdff" stroke-width="20"'
                            f' stroke-linecap="round"'
                            f' opacity="{.80+.16*((i+r) % 3)/2:.2f}"/>')
    s += SL(Z_DAL, ulica_dal(40, 720, 900, t, False, 1123))
    s += SL(Z_DAL, izba_snaruzhi(1560, 760, 380, t, True, True, 1129))
    s += SL(Z_DAL, pleten(1180, 800, 420, 190, 8))
    s += SL(Z_DAL, gryaz_polosa(790, 210, "#4a443a"))
    # изба за спиной: тёплое окно и дымок из трубы
    izb = brevna(60, 300, 900, 600, 112)
    izb += (f'<path d="M20,310 L510,60 L1000,310 Z" fill="#4a3b2c" opacity=".96" {o(9)}/>')
    izb += (f'<rect x="700" y="20" width="96" height="190" fill="url(#kamen)" {o(7)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(748, 30, t, 6, .24, 340, .4, "#d8cbbd", 1.2))
    s += SL(Z_DAL, okno_izby(150, 420, 400, 300, t, svet=True, moroz=.1))
    s += SL(Z_DAL, lampa(350, 700, t, 1.1, False))
    s += SL(Z_DAL, teplo(350, 580, 680, 560, .46 + .12 * abs(A.w(t, 1.7))))
    s += SL(Z_SRED, lavka(560, 1000, 760))
    # ДЕД на пол-кадра: вполоборота, очки, палец вверх
    dx = 820
    s += SL(Z_SRED, figura(dx, 1000, 680, t, "#3a3346", "#ffd98a", False, .15,
                           True, 1.0, True, 1.4, True))
    s += SL(Z_SRED, _ochki(dx + 56, 1000 - 680 * .845, 1.7, t, True))
    vedet = A.w(t, 1.6, .1)
    ruk, (kx, ky) = rukav(dx + 100, 700, 210, -78 + 16 * vedet, t, "#3a3346",
                          "#ffd98a", .1, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{ky:.0f} l{8:.0f},{-70:.0f}"'
                    f' stroke="#3a3346" stroke-width="26" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx+10:.0f}" cy="{ky-82:.0f}" rx="16" ry="22"'
                    f' fill="#f0cfae" {o(4)}/>')
    # губы шевелятся: дужки у лица
    for i in range(3):
        k = ((t * .9) + i * .33) % 1.0
        s += SL(Z_SRED, f'<path d="M{dx+120+k*60:.0f},{1000-680*.80:.0f}'
                        f' q24,-18 10,-44" fill="none" stroke="#f2e2c8"'
                        f' stroke-width="6" opacity="{.6*(1-k):.2f}"/>')
    s += SL(Z_SRED, para_izo_rta(dx + 110, 1000 - 680 * .80, t, .2, 1.3, .45))
    # бабка со спицами
    bx = 420
    s += SL(Z_SRED, figura(bx, 1010, 500, t, "#5b2f3a", "#ffd98a", True, .5,
                           False, 1.0, True, 1.0))
    sp = 24 * A.w(t, .5, .2)
    for i in range(2):
        s += SL(Z_SRED, f'<line x1="{bx-110+i*20:.0f}" y1="{780+sp*.5:.0f}"'
                        f' x2="{bx-10+i*24:.0f}" y2="{830-sp:.0f}" stroke="{KREM}"'
                        f' stroke-width="8" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="{bx-140:.0f}" cy="{856:.0f}" rx="56" ry="46"'
                    f' fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{bx-130:.0f},{826:.0f} q-44,-40 -96,-6" fill="none"'
                    f' stroke="{TKAN2}" stroke-width="7"/>')
    s += SL(Z_SRED, _chashka(1280, 940, 1.5, t, .2, KREM, True))
    s += SL(Z_SRED, par(1280, 850, t, 4, .45, 180, .42, .9))
    s += SL(Z_SRED, kura(1400, 1012, t, 1.0, .3))
    s += SL(Z_SRED, kot(1600, 1012, t, 1.2, "#4a4440", True))
    s += SL(Z_SRED, _korzina_ryab(1760, 1012, 220, 160, t, 1153))
    s += SL(Z_PERED, ramka_pp("pravo", "#17140f", .76))
    s += SL(Z_PERED, grozd_ryabiny(120, 220, t, 1.8, 17, 1163, .2))
    s += vinetka(.42)
    return s


# ── 85 ─────────────────────────────────────────────────────────────────────
def vihr_za_porogom(t):
    """Распахнутая дверь избы: за порогом рисованный Вихрь с хитрой рожицей
    срывает с мужика шапку, вертит её, кружит самого мужика волчком, а жена
    возвращает его за ворот."""
    rnd = random.Random(8521)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 1171)
    s += SL(Z_DAL, ulica_dal(900, 640, 1020, t, False, 1181))
    s += SL(Z_DAL, gryaz_polosa(720, 230, "#3f3a32"))
    s += SL(Z_DAL, goloe_derevo(1640, 760, 520, t, 1187, 7, "#2a2c34"))
    # стена избы с распахнутой дверью: изнутри тёплый свет
    st = brevna(0, 0, 860, 1080, 118)
    s += SL(Z_SRED, st)
    dx, dy, dw, dh = 230, 180, 540, 820
    s += SL(Z_SRED, f'<rect x="{dx-40}" y="{dy-40}" width="{dw+80}" height="{dh+40}"'
                    f' rx="10" fill="url(#derev)" {o(9)}/>')
    vn = (f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#2a1a10"/>')
    vn += teplo(dx + dw * .5, dy + dh * .6, 420, 500, .62)
    vn += (f'<rect x="{dx+60}" y="{dy+dh*.52:.0f}" width="{dw-120}" height="30"'
           f' rx="8" fill="#5a4026" opacity=".9"/>')
    vn += ogon(dx + dw * .36, dy + dh * .70, t, 1.0, .1, 6)
    vn += ugli(dx + dw * .22, dy + dh * .74, dw * .36, t, 7, 1193)
    vn += (f'<rect x="{dx+dw*.62:.0f}" y="{dy+dh*.30:.0f}" width="{dw*.3:.0f}"'
           f' height="{dh*.44:.0f}" rx="10" fill="url(#pech)" opacity=".92" {o(5)}/>')
    s += SL(Z_SRED, vn)
    stv = (f'<path d="M{dx+dw:.0f},{dy:.0f} L{dx+dw+250:.0f},{dy+110:.0f}'
           f' L{dx+dw+250:.0f},{dy+dh-60:.0f} L{dx+dw:.0f},{dy+dh:.0f} Z"'
           f' fill="url(#derev)" {o(8)}/>')
    for i in range(4):                   # доски створки в перспективе
        stv += (f'<line x1="{dx+dw+30+i*55:.0f}" y1="{dy+20+i*24:.0f}"'
                f' x2="{dx+dw+30+i*55:.0f}" y2="{dy+dh-14-i*12:.0f}"'
                f' stroke="#6b4a2a" stroke-width="9" opacity=".8"/>')
    stv += (f'<circle cx="{dx+dw+60:.0f}" cy="{dy+dh*.56:.0f}" r="20"'
            f' fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, stv)
    s += SL(Z_SRED, f'<rect x="{dx-20}" y="{dy+dh-20}" width="{dw+40}" height="46"'
                    f' rx="10" fill="{DOSKA2}" {o(7)}/>')
    s += SL(Z_SRED, podkova(dx + dw / 2, dy - 120, 2.1, t, "url(#zhel)"))
    # ВИХРЬ за порогом, крупно
    s += SL(Z_SRED, _vihr(1520, 1010, 2.1, t, True))
    # шапка вертится в вихре
    ug = (t * 420) % 360
    shx = 1520 + 150 * math.cos(t * 2.2)
    shy = 330 + 50 * math.sin(t * 2.6)
    s += SL(Z_SRED, f'<g transform="rotate({ug:.0f} {shx:.0f} {shy:.0f})">'
                    + _shapka_meh(shx, shy, 1.15, t, .3, 0.0) + '</g>')
    # мужика кружит волчком, он шагает не туда
    kruzh = A.ease(A.seg(t, 1.0, 1.6))
    mx = 1060 + kruzh * 90
    naklon = 16 * math.sin(t * 3.2)
    s += SL(Z_SRED, f'<g transform="rotate({kruzh*34:.1f} {mx:.0f} 1060)">'
                    + figura(mx, 1060, 500, t, "#2e3a46", "#cfe4f5", False, .2,
                             True, 1.0, True, naklon, True, False) + '</g>')
    s += SL(Z_SRED, para_izo_rta(mx + 60, 700, t, .2, 1.2, .55))
    for i in range(3):                   # круговые штрихи: его закрутило
        rr = 150 + i * 60
        s += SL(Z_SRED, f'<path d="M{mx-rr:.0f},{900:.0f} a{rr:.0f},{rr*.3:.0f} 0 1 0'
                        f' {rr*2:.0f},0" fill="none" stroke="#dfe8f2"'
                        f' stroke-width="{8-i*2}" opacity="{.5*kruzh:.2f}"'
                        f' stroke-dasharray="{50+i*20} {26+i*8}"'
                        f' stroke-dashoffset="{t*160:.0f}"/>')
    # жена возвращает его за ворот
    vozv = A.ease(A.seg(t, 2.6, 1.2))
    zx = 860 + 40 * vozv
    s += SL(Z_SRED, figura(zx, 1056, 470, t, "#5b2f3a", "#ffd98a", True, .5,
                           False, 1.0, False, -4.0 * vozv))
    ruk, (kx, ky) = rukav(zx + 80, 760, 260 * (.5 + .5 * vozv), -12, t,
                          "#5b2f3a", "#ffd98a", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="30" ry="22"'
                    f' fill="#5b2f3a" {o(4)}/>')
    s += SL(Z_SRED, kura(1760, 1012, t, .9, .4))
    s += SL(Z_SRED, _vedro_dach(960, 1012, 1.0, t))
    s += SL(Z_PERED, ramka_pp("levo", "#120f14", .8))
    s += SL(Z_PERED, f'<rect x="1850" y="0" width="90" height="1080"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_LETIT, mokryy_sneg(t, 30, 1201, .55, 1.3))
    s += vinetka(.48)
    return s


# ── 86 ─────────────────────────────────────────────────────────────────────
def mokryy_sneg_na_stekle(t):
    """Окошко сеней во весь кадр: в большом стекле НАСТОЯЩИЙ мокрый снег, а
    внук рисует пальцем солнце на СОСЕДНЕЙ, запотевшей створке.

    Внутри проёма под настоящий кадр не лежит ничего нашего: ни рисунка, ни
    запотевания, ни потёков — только нарисованная подложка под меткой. Солнце
    с лицом сидело посреди проёма и перекрывало живое видео (осмотр 14.11)."""
    rnd = random.Random(8623)
    s = f'<rect width="{W}" height="{H}" fill="#241c16"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 124))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#2a1f16" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(930))
    s += SL(Z_DAL, mebel_hlam(1700, 940, 300, t, 1213))
    s += SL(Z_SRED, tusklaya_lampochka(170, 120, t, 1.15, False))
    # БОЛЬШАЯ СТВОРКА — под настоящий кадр; рядом УЗКАЯ — наша, запотевшая
    ox, oy, ow, oh = 250, 120, 940, 700
    fx, fy, fw, fh = 1270, 120, 360, 700          # форточка-створка рядом
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="mo86"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#3f4a5a"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#41506a"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.62:.0f}" width="{ow}" height="{oh*.38:.0f}"'
           f' fill="#3a4454" opacity=".9"/>')
    for i in range(4):                   # дальние избы и забор сквозь снег
        bx = ox + 40 + i * 240
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.56:.0f}" width="150"'
               f' height="{oh*.24:.0f}" fill="#4a5466" opacity=".9"/>')
        za += (f'<path d="M{bx-20:.0f},{oy+oh*.56:.0f} l95,-70 l95,70 Z"'
               f' fill="#3f4858" opacity=".95"/>')
        if i % 2 == 0:
            za += (f'<rect x="{bx+50:.0f}" y="{oy+oh*.62:.0f}" width="46"'
                   f' height="46" fill="{SVET}" opacity=".45"/>')
    for i in range(34):                  # мокрые хлопья сползают по стеклу
        x0 = ox + rnd.random() * ow
        k = ((t * .22) + rnd.random()) % 1.0
        yy = oy + k * oh
        rr = 6 + rnd.random() * 11
        za += (f'<ellipse cx="{x0:.0f}" cy="{yy:.0f}" rx="{rr*.8:.1f}"'
               f' ry="{rr*1.5:.1f}" fill="#eef5ff" opacity=".82"/>')
        za += (f'<path d="M{x0:.0f},{yy-rr:.0f} q4,{rr*2:.0f} 0,{rr*3.4:.0f}"'
               f' fill="none" stroke="#dce9f6" stroke-width="4" opacity=".5"/>')
    vid += f'<g clip-path="url(#mo86)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    # ОБВЯЗКА: короб рамы, импост между створками, наличник и подоконник
    ob = (f'<rect x="{ox-44}" y="{oy-44}" width="{fx+fw-ox+88}" height="{oh+88}"'
          f' rx="10" fill="none" stroke="url(#derev)" stroke-width="88"/>')
    ob += (f'<rect x="{ox+ow:.0f}" y="{oy}" width="{fx-ox-ow:.0f}" height="{oh}"'
           f' fill="url(#derev)" {o(6)}/>')
    ob += f'<path d="{put}" fill="none" {o(10)}/>'
    ob += (f'<path d="M{ox-110},{oy-54} h{fx+fw-ox+220} l-58,-74'
           f' h{-(fx+fw-ox)-104} Z" fill="{DOSKA2}" {o(9)}/>')
    for i in range(10):
        ob += (f'<circle cx="{ox-70+i*(fx+fw-ox+140)/9:.0f}" cy="{oy-74}" r="14"'
               f' fill="{MED}" opacity=".9" {o(2)}/>')
    ob += (f'<rect x="{ox-120}" y="{oy+oh+46}" width="{fx+fw-ox+240}" height="58"'
           f' rx="10" fill="url(#dosk)" {o(9)}/>')
    s += SL(Z_SRED, vid + ob)
    # НАША СТВОРКА: запотевшее стекло и рисунок пальцем — ВНЕ проёма со стоком
    stv = f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#44536b"/>'
    for i in range(3):                   # за нашей створкой тоже двор
        stv += (f'<path d="M{fx+30+i*110:.0f},{fy+fh*.62:.0f} l70,-60 l70,60 Z"'
                f' fill="#3f4858"/>')
        stv += (f'<rect x="{fx+34+i*110:.0f}" y="{fy+fh*.62:.0f}" width="120"'
                f' height="{fh*.22:.0f}" fill="#4a5466"/>')
    dyh = max(0.0, A.w(t, 2.2, .1))
    stv += (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#dfe9f2"'
            f' opacity="{.40+.28*dyh:.2f}"/>')
    ris = A.ease(A.seg(t, .5, 1.6))
    sx_, sy_ = fx + fw * .5, fy + fh * .42
    if ris > .02:
        stv += (f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="88" fill="none"'
                f' stroke="#f6fbff" stroke-width="15" opacity="{.95*ris:.2f}"'
                f' stroke-dasharray="{556*ris:.0f} 999"/>')
        for i in range(10):              # лучи солнышка
            a = i * .628
            lk = max(0.0, min(1.0, ris * 10 - i))
            stv += (f'<line x1="{sx_+math.cos(a)*102:.0f}"'
                    f' y1="{sy_+math.sin(a)*102:.0f}"'
                    f' x2="{sx_+math.cos(a)*(102+46*lk):.0f}"'
                    f' y2="{sy_+math.sin(a)*(102+46*lk):.0f}" stroke="#f6fbff"'
                    f' stroke-width="12" opacity="{.9*lk:.2f}"/>')
        if ris > .7:                     # улыбка и глаза
            stv += (f'<path d="M{sx_-42:.0f},{sy_+18:.0f} q42,44 84,0" fill="none"'
                    f' stroke="#f6fbff" stroke-width="13" opacity=".95"/>')
            for i in (-1, 1):
                stv += (f'<circle cx="{sx_+i*30:.0f}" cy="{sy_-24:.0f}" r="11"'
                        f' fill="#f6fbff" opacity=".95"/>')
    for i in range(5):                   # потёки по нашей створке
        stv += (f'<path d="M{fx+40+i*70:.0f},{fy+fh*.58:.0f} q6,90 -2,{fh*.38:.0f}"'
                f' fill="none" stroke="#eaf4ff" stroke-width="6" opacity=".45"/>')
    stv += (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" {o(9)}/>')
    stv += (f'<line x1="{fx}" y1="{fy+fh*.48:.0f}" x2="{fx+fw}"'
            f' y2="{fy+fh*.48:.0f}" stroke="url(#derev)" stroke-width="28"/>')
    s += SL(Z_SRED, stv)
    # ВНУК у нашей створки: дышит на стекло и ведёт пальцем
    vx = fx + fw * .5
    s += SL(Z_SRED, figura(vx, 1070, 400, t, "#6b3a44", "#ffd98a", False, .4,
                           False, 1.0, False, 1.4, False, False))
    ruk, (kx, ky) = rukav(vx - 40, 820, 230, -74 + 16 * A.w(t, 1.1), t,
                          "#6b3a44", "#ffd98a", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="26" ry="20"'
                    f' fill="#6b3a44" {o(4)}/>')
    s += SL(Z_SRED, para_izo_rta(vx + 54, 1070 - 400 * .80, t, .1, 1.3, .55))
    # тулуп возвращается на гвоздь справа, за окном
    vozv = A.ease(A.seg(t, 1.6, 1.4))
    s += SL(Z_SRED, f'<circle cx="1790" cy="300" r="14" fill="#8d949b" {o(4)}/>')
    s += SL(Z_SRED, _tulup_vis(1790 - 70 * (1 - vozv), 320 + 160 * (1 - vozv),
                               270, 400, t, .2, 0.0))
    s += SL(Z_SRED, _valenok(1760, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_SRED, _vedro_dach(130, 1012, 1.1, t))
    s += SL(Z_PERED, ramka_pp("levo", "#140f0c", .74))
    s += vinetka(.46)
    return s


# ── 87 ─────────────────────────────────────────────────────────────────────
def dym_stolbom_i_karavay(t):
    """Деревня в тихий день: из каждой трубы дым стоит ровным столбом до неба,
    бельё на верёвке не шелохнётся, флюгер-петушок замер. Самый высокий столб
    дыма на глазах превращается в пышный румяный каравай на рушнике.

    Превращение заканчивается К СЕРЕДИНЕ плана, а не тянется до конца: прежде
    в кадре весь план стоял полупрозрачный серый эллипс, и ни дымом, ни
    караваем он не читался. Бельё перенесено влево, чтобы верёвка не резала
    каравай пополам (осмотр 14.11)."""
    rnd = random.Random(8713)
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, False, 1217)
    s += SL(Z_DAL, tuman(t, 700, .34, "#dfe7ee"))
    s += SL(Z_DAL, gryaz_polosa(880, 200, "#4a443a"))
    s += SL(Z_DAL, sneg_lezhit(900, 24, "url(#sneg)"))
    # три избы: у каждой труба и свой ровный густой столб дыма
    for i, (bx, bw, hh) in enumerate(((40, 440, 300), (1440, 460, 330),
                                      (720, 280, 210))):
        iz = brevna(bx, 900 - hh, bw, hh + 60, 92)
        iz += (f'<path d="M{bx-40:.0f},{900-hh:.0f} L{bx+bw*.5:.0f},{900-hh-150:.0f}'
               f' L{bx+bw+40:.0f},{900-hh:.0f} Z" fill="#4a3b2c" {o(8)}/>')
        iz += (f'<path d="M{bx-36:.0f},{900-hh-6:.0f} L{bx+bw*.5:.0f},{900-hh-146:.0f}'
               f' L{bx+bw+36:.0f},{900-hh-6:.0f} l-46,-26 L{bx+bw*.5:.0f},'
               f'{900-hh-112:.0f} l{-bw*.5+46:.0f},{86:.0f} Z"'
               f' fill="url(#sneg)" opacity=".85"/>')
        iz += (f'<rect x="{bx+bw*.62:.0f}" y="{900-hh-250:.0f}" width="80"'
               f' height="110" fill="url(#kamen)" {o(7)}/>')
        iz += okno_izby(bx + bw * .16, 900 - hh * .62, bw * .3, hh * .34, t,
                        svet=True, moroz=.2)
        s += SL(Z_DAL, iz)
        s += SL(Z_DAL, teplo(bx + bw * .3, 900 - hh * .45, 260, 220, .3))
        # ровный столб дыма: густой, почти без вихря
        cx_ = bx + bw * .62 + 40
        stolb = ""
        for j in range(16):
            yy = 900 - hh - 250 - j * 62
            rr = 40 - j * .9 + 4 * A.w(t, 7.0, j * .06)
            stolb += (f'<ellipse cx="{cx_+3*A.w(t,8.0,j*.1):.0f}" cy="{yy:.0f}"'
                      f' rx="{max(10, rr):.0f}" ry="{max(12, rr*1.2):.0f}"'
                      f' fill="#dfe5ec" opacity="{.80-j*.030:.2f}"/>')
        s += SL(Z_DAL, stolb)
        s += SL(Z_DAL, dym(cx_, 900 - hh - 250, t, 6, .12, 300, .46, "#d8dee6", .8))
    # бельё на верёвке СЛЕВА — не шелохнётся и каравай не режет
    s += SL(Z_SRED, f'<path d="M60,700 q220,26 440,6" fill="none" stroke="#c2ab86"'
                    f' stroke-width="6"/>')
    for i, (col, ww, hh2) in enumerate(((KREM, 130, 165), (TKAN2, 115, 140),
                                        (RUSH, 140, 180))):
        bx = 130 + i * 140
        dr = .4 * A.w(t, 9.0, i * .2)
        s += SL(Z_SRED, f'<g transform="rotate({dr:.2f} {bx:.0f} {706:.0f})">'
                        f'<path d="M{bx-ww/2:.0f},{706:.0f} h{ww:.0f}'
                        f' l{-8:.0f},{hh2:.0f} q{-ww*.4:.0f},{14:.0f}'
                        f' {-ww+16:.0f},0 Z" fill="{col}" {o(5)}/>'
                        f'<rect x="{bx-ww/2-6:.0f}" y="{700:.0f}" width="{ww+12:.0f}"'
                        f' height="14" rx="6" fill="#8d949b" {o(3)}/></g>')
    # флюгер-петушок замер
    fx_, fy_ = 1760, 300
    s += SL(Z_SRED, f'<rect x="{fx_-7:.0f}" y="{fy_:.0f}" width="14" height="170"'
                    f' rx="6" fill="#5d6168" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_-70:.0f},{fy_-40:.0f} q40,-54 92,-34'
                    f' q44,18 44,56 q-4,36 -50,40 l-16,34 l-18,-34'
                    f' q-46,-8 -52,-62 Z" fill="#2f3337" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_+66:.0f},{fy_-30:.0f} l40,-16 l-6,26 l34,8'
                    f' l-62,16 Z" fill="#8a3a22" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_-74:.0f},{fy_-66:.0f} q24,-30 44,-8'
                    f' q-18,18 -44,8 Z" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{fx_-48:.0f}" cy="{fy_-42:.0f}" r="6"'
                    f' fill="#f2efe6"/>')
    for i in range(4):                   # лучи-указатели флюгера
        a = i * 1.5708
        s += SL(Z_SRED, f'<line x1="{fx_:.0f}" y1="{fy_+30:.0f}"'
                        f' x2="{fx_+math.cos(a)*54:.0f}" y2="{fy_+30+math.sin(a)*54:.0f}"'
                        f' stroke="#5d6168" stroke-width="7"/>')
    # СТОЛБ ДЫМА ПРЕВРАЩАЕТСЯ В КАРАВАЙ — главный предмет, крупно и непрозрачно
    prev = A.ease(A.seg(t, .25, .9))
    kx_, ky_ = 960, 420
    for j in range(8):                   # столб дыма входит прямо в каравай
        s += SL(Z_SRED, f'<ellipse cx="{kx_+4*A.w(t,7.0,j*.1):.0f}"'
                        f' cy="{760-j*44:.0f}" rx="{44-j*2:.0f}"'
                        f' ry="{48-j*2:.0f}" fill="#dfe5ec"'
                        f' opacity="{.78-j*.055:.2f}"/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx_:.0f}" cy="{ky_+40:.0f}"'
                    f' rx="{46+60*(1-prev):.0f}" ry="{320*(1-prev)+60:.0f}"'
                    f' fill="#dfe5ec" opacity="{.7*(1-prev):.2f}"/>')
    kar = f'<g opacity="{prev:.2f}" transform="translate(0,{(1-prev)*-60:.0f})">'
    kar += ten(kx_, ky_ + 300, 330, 34, .45)
    kar += (f'<path d="M{kx_-350:.0f},{ky_+150:.0f} h700 l-22,156 h-656 Z"'
            f' fill="url(#rush)" {o(8)}/>')
    for i in (-1, 1):                    # концы рушника свисают
        kar += (f'<path d="M{kx_+i*340:.0f},{ky_+160:.0f} l{i*42:.0f},{44:.0f}'
                f' l{-i*20:.0f},{140:.0f} l{-i*32:.0f},{-22:.0f} Z"'
                f' fill="url(#rush)" {o(6)}/>')
    kar += (f'<path d="M{kx_-350:.0f},{ky_+198:.0f} h700" stroke="{KRAS}"'
            f' stroke-width="16" opacity=".9"/>')
    kar += (f'<path d="M{kx_-350:.0f},{ky_+270:.0f} h656" stroke="{KRAS}"'
            f' stroke-width="11" opacity=".75"/>')
    for i in range(6):                   # вышивка по рушнику — узор, не буквы
        kar += (f'<path d="M{kx_-290+i*110:.0f},{ky_+210:.0f} l28,-28 l28,28 l-28,28 Z"'
                f' fill="{KRAS}" opacity=".9"/>')
    kar += (f'<ellipse cx="{kx_:.0f}" cy="{ky_+40:.0f}" rx="320" ry="196"'
            f' fill="#a8641e" {o(9)}/>')
    kar += (f'<ellipse cx="{kx_:.0f}" cy="{ky_+16:.0f}" rx="306" ry="180"'
            f' fill="#c98c55"/>')
    kar += (f'<ellipse cx="{kx_:.0f}" cy="{ky_-2:.0f}" rx="282" ry="160"'
            f' fill="#d9a263"/>')
    kar += (f'<ellipse cx="{kx_-90:.0f}" cy="{ky_-62:.0f}" rx="140" ry="66"'
            f' fill="#e8bd84" opacity=".8"/>')
    for i in range(7):                   # насечки на румяной корке
        kar += (f'<path d="M{kx_-236+i*78:.0f},{ky_-86:.0f} q22,42 4,90"'
                f' fill="none" stroke="#a8641e" stroke-width="11" opacity=".85"/>')
    kar += (f'<path d="M{kx_-260:.0f},{ky_+72:.0f} q260,54 520,0" fill="none"'
            f' stroke="#a8641e" stroke-width="9" opacity=".6"/>')
    for i in range(5):                   # верхушка-завиток из теста
        a = -2.0 + i * .5
        kar += (f'<ellipse cx="{kx_+math.cos(a)*110:.0f}"'
                f' cy="{ky_-120+math.sin(a)*26:.0f}" rx="44" ry="24"'
                f' fill="#e8bd84" {o(5)}/>')
    kar += '</g>'
    s += SL(Z_SRED, kar)
    s += SL(Z_SRED, par(kx_, ky_ - 190, t, 6, .5 * prev + .05, 280, .45, 1.5))
    s += SL(Z_SRED, teplo(kx_, ky_ + 20, 660 * prev, 470 * prev, .32 * prev))
    s += SL(Z_SRED, figura(360, 1060, 460, t, "#3a3346", "#ffd0a0", False, .3,
                           True, 1.0, True, 1.0, True))
    s += SL(Z_SRED, para_izo_rta(410, 700, t, .2, 1.2, .5))
    s += SL(Z_SRED, figura(210, 1066, 330, t, "#5b2f3a", "#ffd0a0", True, .6,
                           True, 1.0, False, 1.2))
    # фонарь у ближней избы: без живого огня кадр оставался сине-серым
    s += SL(Z_SRED, f'<rect x="1696" y="640" width="18" height="250" rx="8"'
                    f' fill="#3a3f46" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1652,640 h106 l-16,-42 h-74 Z" fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1662,640 h86 l-10,112 h-66 Z" fill="url(#stekl)"'
                    f' opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, ogon(1705, 716, t, .95, .3, 5))
    s += SL(Z_SRED, teplo(1705, 690, 620, 540, .46 + .12 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, kura(1300, 1012, t, 1.0, .2))
    s += SL(Z_SRED, kura(1400, 1012, t, .9, .6))
    s += SL(Z_SRED, pleten(540, 1046, 420, 170, 8))
    s += SL(Z_PERED, goloe_derevo(110, 1080, 680, t, 1223, 7, "#2e3038"))
    s += SL(Z_PERED, ramka_pp("pravo", "#191510", .72))
    s += vinetka(.42)
    return s


# ── 88 ─────────────────────────────────────────────────────────────────────
def seyatel_i_risovannyy_veter(t):
    """Окно сарая: за стеклом НАСТОЯЩИЕ деревья гнутся под ветром. Слева от
    окна мужик с лукошком зерна уже замахнулся сеять, но рисованный Ветер над
    крышей качает головой — зерно сыплется обратно в мешок.

    Проём чистый: сеятель и лукошко стоят СЛЕВА ОТ окна, Ветер — НАД ним, и
    жердей поверх стекла больше нет. Прежде мужик закрывал нижнюю половину
    настоящего кадра, а Ветер — его правый край (осмотр 14.11)."""
    rnd = random.Random(8819)
    s = f'<rect width="{W}" height="{H}" fill="#2b2118"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 104, True, "dosk"))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#372a1c" opacity=".5"/>')
    s += SL(Z_DAL, svody(t, "#4b3f31", 3))
    s += SL(Z_DAL, polovicy(900))
    s += SL(Z_DAL, utvar_pekarni(120, 300, 300, t, 1229))
    # ОКНО САРАЯ справа: рисованный вид, метка, рама поверх
    ox, oy, ow, oh = 900, 300, 900, 560
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="sa88"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="url(#nsumer)"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#9fb0c2"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.64:.0f}" width="{ow}" height="{oh*.36:.0f}"'
           f' fill="#7d8a6a" opacity=".92"/>')
    for i in range(4):                   # деревья за стеклом гнутся
        gib = 11 * A.w(t, 1.1, i * .22)
        tx_ = ox + 110 + i * 230
        za += (f'<g transform="rotate({gib:.1f} {tx_:.0f} {oy+oh*.70:.0f})">'
               f'<path d="M{tx_-18:.0f},{oy+oh*.70:.0f} l9,{-oh*.44:.0f}'
               f' l18,0 l9,{oh*.44:.0f} Z" fill="#6b5a46" {o(5)}/>')
        for j in range(5):
            a = -2.4 + j * .5
            za += (f'<path d="M{tx_:.0f},{oy+oh*(.40+j*.04):.0f}'
                   f' q{math.cos(a)*60:.0f},{math.sin(a)*40:.0f}'
                   f' {math.cos(a)*120:.0f},{math.sin(a)*58:.0f}" fill="none"'
                   f' stroke="#4f4335" stroke-width="{10-j}"/>')
        za += '</g>'
    for i in range(20):                  # сор летит по ветру
        k = ((t * .7) + i * .05) % 1.0
        za += (f'<path d="M{ox+k*ow:.0f},{oy+oh*(.3+(i%6)*.09)+20*A.w(t,2.0,i*.1):.0f}'
               f' l22,-8 l-6,14 Z" fill="#8a7a5a" opacity=".8"/>')
    vid += f'<g clip-path="url(#sa88)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    ob = (f'<rect x="{ox-44}" y="{oy-44}" width="{ow+88}" height="{oh+88}" rx="8"'
          f' fill="none" stroke="url(#derev)" stroke-width="88"/>')
    ob += (f'<rect x="{ox+ow/2-15:.0f}" y="{oy}" width="30" height="{oh}"'
           f' fill="url(#derev)"/>')
    ob += (f'<line x1="{ox}" y1="{oy+oh*.5:.0f}" x2="{ox+ow}" y2="{oy+oh*.5:.0f}"'
           f' stroke="url(#derev)" stroke-width="30"/>')
    ob += f'<path d="{put}" fill="none" {o(10)}/>'
    ob += (f'<path d="M{ox-100},{oy-54} h{ow+200} l-56,-70 h{-ow-88} Z"'
           f' fill="{DOSKA2}" {o(9)}/>')
    ob += (f'<rect x="{ox-110}" y="{oy+oh+48}" width="{ow+220}" height="50" rx="10"'
           f' fill="url(#dosk)" {o(9)}/>')
    s += SL(Z_SRED, vid + ob)
    for i in range(4):                   # косые жерди сарая — ПО СТЕНЕ, не по стеклу
        s += SL(Z_SRED, f'<line x1="20" y1="{120+i*210:.0f}" x2="{ox-150:.0f}"'
                        f' y2="{90+i*210:.0f}" stroke="#6b5234" stroke-width="14"'
                        f' opacity=".7"/>')
    s += SL(Z_SRED, lampa(1860, 230, t, 1.0, False))
    s += SL(Z_SRED, teplo(1860, 270, 560, 480, .4 + .1 * abs(A.w(t, 1.5))))
    # РИСОВАННЫЙ ВЕТЕР — НАД ОКНОМ, у самого верха кадра
    vx, vy = 650, 190
    kach = 26 * A.w(t, 1.2, .1)
    vet = f'<g transform="rotate({kach*.3:.1f} {vx:.0f} {vy:.0f})">'
    for i in range(5):                   # щёки-облака
        rr = 128 - i * 14
        vet += (f'<ellipse cx="{vx+i*20-38+kach*.6:.0f}" cy="{vy+i*9-16:.0f}"'
                f' rx="{rr:.0f}" ry="{rr*.74:.0f}" fill="#cdd9e6"'
                f' opacity="{.5-i*.06:.2f}"/>')
    vet += (f'<ellipse cx="{vx+kach*.6:.0f}" cy="{vy:.0f}" rx="178" ry="142"'
            f' fill="#dde7f2" opacity=".94" {o(6)}/>')
    vet += _rozhica(vx + kach * .6, vy - 12, 118, t, .2, False, "#3f4a58")
    for i in range(6):                   # струи ветра изо рта
        k = ((t * .9) + i * .17) % 1.0
        vet += (f'<path d="M{vx+150+kach*.6+k*240:.0f},{vy+70+i*16-k*26:.0f}'
                f' q70,{-18+i*7:.0f} 150,{6:.0f}" fill="none" stroke="#e8f1f8"'
                f' stroke-width="{9-i:.0f}" opacity="{.6*(1-k):.2f}"/>')
    vet += '</g>'
    s += SL(Z_SRED, vet)
    # СЕЯТЕЛЬ СЛЕВА ОТ ОКНА: лукошко у него перед грудью, проёма не касается
    mx = 450
    s += SL(Z_SRED, figura(mx, 1066, 620, t, "#4a3a2c", "#ffd98a", False, .2,
                           True, 1.0, False, 2.0, True))
    zam = A.w(t, 1.4, .1)
    ruk, (kx, ky) = rukav(mx + 120, 720, 160, 22 + 16 * zam, t, "#4a3a2c",
                          "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    luk_x, luk_y = mx + 180, 880
    luk = (f'<path d="M{luk_x-170:.0f},{luk_y-220:.0f} h340 l-46,220 h-248 Z"'
           f' fill="url(#solom)" {o(9)}/>')
    for i in range(6):               # лоза лукошка
        luk += (f'<path d="M{luk_x-162+i*8:.0f},{luk_y-198+i*36:.0f}'
                f' q{160-i*8:.0f},{20:.0f} {322-i*16:.0f},0" fill="none"'
                f' stroke="#b78a46" stroke-width="11"/>')
    luk += (f'<ellipse cx="{luk_x:.0f}" cy="{luk_y-220:.0f}" rx="170" ry="38"'
            f' fill="#d8b96a" {o(7)}/>')
    for i in range(30):              # зерно горкой с верхом
        a = rnd.uniform(0, 6.283); rr = rnd.uniform(0, 1) ** .5 * 152
        luk += (f'<ellipse cx="{luk_x+math.cos(a)*rr:.0f}"'
                f' cy="{luk_y-244+math.sin(a)*rr*.20+3*A.w(t,2.2,i*.1):.0f}"'
                f' rx="13" ry="9" fill="#e3c272" {o(3)}/>')
    luk += (f'<path d="M{luk_x-170:.0f},{luk_y-214:.0f} q{170:.0f},{-116:.0f}'
            f' {340:.0f},0" fill="none" stroke="#9a7238" stroke-width="16"/>')
    s += SL(Z_SRED, luk)
    syp = A.ease(A.seg(t, .6, 1.8))
    msx, msy = 150, 1030
    for i in range(20):                  # зерно сыплется ОБРАТНО в мешок
        p = ((t * .9) + i * .05) % 1.0
        xx = luk_x + (msx - luk_x) * p
        yy = luk_y - 150 + (msy - 260 - (luk_y - 150)) * p + 170 * p * p
        s += SL(Z_SRED, f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="7" ry="5"'
                        f' fill="#e3c272" opacity="{.95*syp*(1-p*.3):.2f}"/>')
    # мешок завязывается
    zav = A.ease(A.seg(t, 2.2, 1.0))
    mesh = (f'<path d="M{msx-140:.0f},{msy:.0f} q{-36:.0f},{-190:.0f} {10:.0f},{-282:.0f}'
            f' q{130:.0f},{-38:.0f} {260:.0f},0 q{46:.0f},{94:.0f} {10:.0f},{282:.0f} Z"'
            f' fill="url(#solom)" {o(9)}/>')
    mesh += (f'<path d="M{msx-130:.0f},{msy-170:.0f} q{140:.0f},{28:.0f} {270:.0f},0"'
             f' fill="none" stroke="#a07c2e" stroke-width="11" opacity=".7"/>')
    gor = 130 - 84 * zav
    mesh += (f'<path d="M{msx-gor:.0f},{msy-282:.0f} q{gor:.0f},{-66:.0f}'
             f' {gor*2:.0f},0 q{-gor*.5:.0f},{-38:.0f} {-gor*2:.0f},0 Z"'
             f' fill="#d8b96a" {o(6)}/>')
    mesh += (f'<path d="M{msx-gor:.0f},{msy-298:.0f} q{gor:.0f},{38:.0f} {gor*2:.0f},0"'
             f' fill="none" stroke="#6b4a2a" stroke-width="{10+8*zav:.0f}"/>')
    if zav > .5:
        mesh += (f'<path d="M{msx-20:.0f},{msy-310:.0f} q{-40:.0f},{-40:.0f}'
                 f' {-70:.0f},{-14:.0f}" fill="none" stroke="#6b4a2a"'
                 f' stroke-width="8"/>')
        mesh += (f'<path d="M{msx+20:.0f},{msy-310:.0f} q{40:.0f},{-40:.0f}'
                 f' {70:.0f},{-14:.0f}" fill="none" stroke="#6b4a2a"'
                 f' stroke-width="8"/>')
    s += SL(Z_SRED, mesh)
    s += SL(Z_SRED, kura(840, 1000, t, 1.2, .4))
    s += SL(Z_PERED, ramka_pp("levo", "#150f0a", .72))
    s += SL(Z_LETIT, iskra_let(t, 1860, 280, 6, 1237, 240, .3))
    s += vinetka(.46)
    return s


# ── 89 ─────────────────────────────────────────────────────────────────────
def myshi_gotovyatsya_k_zime(t):
    """Разрез пола и стены избы: в подполе кипит мышиный переезд — мыши в
    платочках катят орехи, тащат колоски, одна несёт на спине перину из пуха,
    другая заколачивает дощечкой вход в норку. Хозяйка сверху прислушивается."""
    rnd = random.Random(8923)
    s = f'<rect width="{W}" height="{H}" fill="#1d1712"/>'
    # верх: изба в разрезе
    s += SL(Z_DAL, brevna(0, 0, W, 470, 108))
    s += SL(Z_DAL, f'<rect width="{W}" height="470" fill="#2a2018" opacity=".48"/>')
    s += SL(Z_DAL, utvar_izby(1480, 60, 400, t, 1249))
    s += SL(Z_SRED, f'<rect y="470" width="{W}" height="60" fill="url(#pol)" {o(7)}/>')
    for i in range(11):
        s += SL(Z_SRED, f'<line x1="{i*176:.0f}" y1="470" x2="{i*176:.0f}" y2="530"'
                        f' stroke="#4e3220" stroke-width="5" opacity=".7"/>')
    s += SL(Z_SRED, f'<rect y="530" width="{W}" height="26" fill="#3f2a18" {o(5)}/>')
    # хозяйка прислушивается, со свечой
    hx = 1180
    s += SL(Z_SRED, figura(hx, 470, 420, t, "#4a2f3a", "#ffd98a", True, .3,
                           True, 1.0, False, 3.0))
    s += SL(Z_SRED, svecha(hx - 150, 300, t, .2, 1.5, 100))
    s += SL(Z_SRED, teplo(hx - 150, 250, 560, 460, .46 + .12 * abs(A.w(t, 1.5))))
    for i in range(3):                   # дужки «слышно»
        k = ((t * .8) + i * .33) % 1.0
        s += SL(Z_SRED, f'<path d="M{hx+90:.0f},{300-k*60:.0f} q40,{-26:.0f}'
                        f' {30-k*20:.0f},{-60:.0f}" fill="none" stroke="#ffe6b8"'
                        f' stroke-width="6" opacity="{.6*(1-k):.2f}"/>')
    s += SL(Z_SRED, lavka(180, 380, 420))
    s += SL(Z_SRED, krynka(300, 376, 1.3))
    s += SL(Z_SRED, karavay(520, 374, .8, True))
    # ПОДПОЛ: земляной разрез, норки, мышиный переезд
    s += SL(Z_SRED, f'<rect y="556" width="{W}" height="524" fill="#6b5240"/>')
    for i in range(70):                  # земля комками
        s += SL(Z_SRED, f'<circle cx="{rnd.random()*W:.0f}"'
                        f' cy="{570+rnd.random()*500:.0f}"'
                        f' r="{rnd.uniform(5,20):.0f}" fill="#8a6c52"'
                        f' opacity="{rnd.uniform(.3,.7):.2f}"/>')
    s += SL(Z_SRED, f'<rect y="556" width="{W}" height="22" fill="#5a4530" {o(4)}/>')
    for i, (nx, nr) in enumerate(((240, 110), (1020, 92), (1700, 120))):
        s += SL(Z_SRED, f'<path d="M{nx-nr:.0f},1080 q0,{-nr*1.5:.0f} {nr:.0f},'
                        f'{-nr*1.5:.0f} q{nr:.0f},0 {nr:.0f},{nr*1.5:.0f} Z"'
                        f' fill="#1a120c" {o(6)}/>')
    s += SL(Z_SRED, teplo(1020, 900, 420, 300, .14))
    # мыши катят орехи
    for i in range(3):
        p = ((t * .22) + i * .3) % 1.0
        mxx = 200 + p * 900
        s += SL(Z_SRED, f'<circle cx="{mxx+130:.0f}" cy="{886+i*58:.0f}"'
                        f' r="{56-i*6:.0f}" fill="#9c6a3c" {o(5)}/>')
        s += SL(Z_SRED, f'<path d="M{mxx+96:.0f},{880+i*58:.0f} q34,{-30:.0f}'
                        f' {68:.0f},0" fill="none" stroke="#6b4a2a" stroke-width="8"/>')
        s += SL(Z_SRED, _mysh(mxx, 898 + i * 58, 2.3 - i * .25, t, i * .3, True))
    # мышь тащит колосок
    kp = ((t * .18) + .4) % 1.0
    kxx = 1500 - kp * 700
    s += SL(Z_SRED, _mysh(kxx, 760, 2.4, t, .5, True))
    s += SL(Z_SRED, f'<path d="M{kxx+70:.0f},{752:.0f} q140,-40 300,-72"'
                    f' fill="none" stroke="#a07c2e" stroke-width="11"/>')
    for i in range(11):                  # зёрна колоска парами, с усиками
        gxx = kxx + 160 + i * 20
        gyy = 726 - i * 5 + 4 * A.w(t, 2.2, i * .1)
        for sg in (-1, 1):
            s += SL(Z_SRED, f'<ellipse cx="{gxx:.0f}" cy="{gyy+sg*13:.0f}"'
                            f' rx="16" ry="11" fill="#e3c272" {o(3)}/>')
            s += SL(Z_SRED, f'<line x1="{gxx+10:.0f}" y1="{gyy+sg*13:.0f}"'
                            f' x2="{gxx+40:.0f}" y2="{gyy+sg*30:.0f}"'
                            f' stroke="#c9a04a" stroke-width="4"/>')
    # мышь с периной из пуха на спине
    pp = ((t * .16) + .7) % 1.0
    pxx = 300 + pp * 1200
    s += SL(Z_SRED, _mysh(pxx, 1010, 2.5, t, .2, True))
    s += SL(Z_SRED, f'<ellipse cx="{pxx-10:.0f}" cy="{906+6*A.w(t,1.2,.2):.0f}"'
                    f' rx="130" ry="68" fill="#f2efe6" {o(6)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{pxx-70+i*22:.0f},{920:.0f} q8,{-16:.0f} 16,{-2:.0f}"'
                        f' fill="none" stroke="#dfe3e8" stroke-width="6"/>')
    for i in range(6):                   # пушинки летят
        k = ((t * .5) + i * .17) % 1.0
        s += SL(Z_LETIT, f'<circle cx="{pxx+60+k*120:.0f}" cy="{910-k*90:.0f}"'
                         f' r="{6+5*k:.0f}" fill="#f6f6f2"'
                         f' opacity="{.6*(1-k):.2f}"/>')
    # мышь заколачивает дощечкой вход в норку
    zx_, zy_ = 1700, 1000
    s += SL(Z_SRED, _mysh(zx_ - 150, zy_ + 20, 2.3, t, .7, True))
    s += SL(Z_SRED, f'<rect x="{zx_-70:.0f}" y="{zy_-80:.0f}" width="200" height="34"'
                    f' rx="6" fill="url(#dosk)" {o(5)}/>')
    stuk = max(0.0, A.w(t, .9, .1))
    s += SL(Z_SRED, f'<g transform="rotate({-30+34*stuk:.1f} {zx_-60:.0f} {zy_-100:.0f})">'
                    f'<rect x="{zx_-70:.0f}" y="{zy_-170:.0f}" width="22" height="80"'
                    f' rx="6" fill="url(#derev)" {o(4)}/>'
                    f'<rect x="{zx_-96:.0f}" y="{zy_-196:.0f}" width="74" height="34"'
                    f' rx="8" fill="#5d6168" {o(4)}/></g>')
    if stuk > .85:
        for i in range(5):
            a = -2.4 + i * .5
            s += SL(Z_SRED, f'<line x1="{zx_-56:.0f}" y1="{zy_-96:.0f}"'
                            f' x2="{zx_-56+math.cos(a)*42:.0f}"'
                            f' y2="{zy_-96+math.sin(a)*42:.0f}" stroke="#ffe6b8"'
                            f' stroke-width="6" opacity=".7"/>')
    for i in range(2):                   # припасы в подполе
        s += SL(Z_SRED, _banka_krupy(560 + i * 150, 1000, 1.5, t))
    s += SL(Z_SRED, kartoshka(430, 1040, t, 11, 1259, 1.3))
    s += SL(Z_PERED, f'<rect x="0" y="470" width="90" height="610"'
                     f' fill="url(#brev)" {o(9)}/>')
    s += SL(Z_PERED, ramka_pp("pravo", "#120d0a", .7))
    s += SL(Z_PERED, kot(170, 540, t, 1.3, "#3b3430", False))
    s += vinetka(.5)
    return s


def _banka_krupy(x, y, s_=1.0, t=0.0, zerno="url(#solom)"):
    """Банка крупы в подполе: стекло, крышка-кружок, уровень зерна, блик."""
    w_, hh = 46 * s_, 110 * s_
    s = ten(x, y + 5 * s_, w_ * .9, 8 * s_, .35)
    s += (f'<path d="M{x-w_:.0f},{y-hh:.0f} h{w_*2:.0f} l{-5*s_:.0f},{hh:.0f}'
          f' h{-w_*2+10*s_:.0f} Z" fill="url(#stekl)" opacity=".75" {o(4)}/>')
    s += (f'<path d="M{x-w_*.9:.0f},{y-hh*.6:.0f} h{w_*1.8:.0f} l{-4*s_:.0f},'
          f'{hh*.58:.0f} h{-w_*1.8+8*s_:.0f} Z" fill="{zerno}" {o(3)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh*.6:.0f}" rx="{w_*.9:.0f}" ry="{7*s_:.0f}"'
          f' fill="#d8b96a" opacity=".9"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*1.1:.0f}" ry="{9*s_:.0f}"'
          f' fill="url(#zhel)" {o(3)}/>')
    s += (f'<line x1="{x-w_*.5:.0f}" y1="{y-hh*.9:.0f}" x2="{x-w_*.5:.0f}"'
          f' y2="{y-hh*.2:.0f}" stroke="#ffffff" stroke-width="{7*s_:.0f}"'
          f' opacity="{.2+.2*abs(A.w(t,2.8,x*.002)):.2f}"/>')
    return s


# ── 90 ─────────────────────────────────────────────────────────────────────
def komar_na_noyabrskom_okne(t):
    """Оконное стекло с первым инеем по краям: по нему, как по катку, деловито
    идёт большой рисованный комар в шарфе и с саквояжем. Газета замахивается
    и опускается, дед улыбается, комар раскланивается."""
    rnd = random.Random(9029)
    s = f'<rect width="{W}" height="{H}" fill="#2a2420"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 122))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#30241a" opacity=".45"/>')
    s += SL(Z_DAL, polovicy(950, "url(#pol)"))
    s += SL(Z_DAL, utvar_izby(60, 240, 300, t, 1277))
    # окно крупно: за стеклом сумерки, по краям иней
    ox, oy, ow, oh = 420, 110, 1120, 700
    s += SL(Z_SRED, f'<rect x="{ox-54}" y="{oy-54}" width="{ow+108}"'
                    f' height="{oh+108}" rx="10" fill="url(#derev)" {o(10)}/>')
    st_ = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#3e4a60"/>')
    st_ += (f'<rect x="{ox}" y="{oy+oh*.60:.0f}" width="{ow}" height="{oh*.40:.0f}"'
            f' fill="#333c4e" opacity=".92"/>')
    for i in range(5):                   # дальние дома и огоньки за стеклом
        bx = ox + 30 + i * 226
        st_ += (f'<rect x="{bx:.0f}" y="{oy+oh*.52:.0f}" width="140"'
                f' height="{oh*.26:.0f}" fill="#3a4354" opacity=".9"/>')
        st_ += (f'<path d="M{bx-18:.0f},{oy+oh*.52:.0f} l88,-66 l88,66 Z"'
                f' fill="#333b4a" opacity=".95"/>')
        if i % 2:
            st_ += (f'<rect x="{bx+48:.0f}" y="{oy+oh*.58:.0f}" width="44"'
                    f' height="44" fill="{SVET}"'
                    f' opacity="{.4+.25*abs(A.w(t,2.2,i*.3)):.2f}"/>')
    st_ += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#stekl)"'
            f' opacity=".30"/>')
    for i in range(16):                  # иней по краям стекла
        side = i % 4
        if side == 0:
            cx_, cy_ = ox + rnd.random() * ow, oy + rnd.random() * 90
        elif side == 1:
            cx_, cy_ = ox + rnd.random() * ow, oy + oh - rnd.random() * 90
        elif side == 2:
            cx_, cy_ = ox + rnd.random() * 110, oy + rnd.random() * oh
        else:
            cx_, cy_ = ox + ow - rnd.random() * 110, oy + rnd.random() * oh
        rr = (12 + rnd.random() * 22) * (.7 + .3 * abs(A.w(t, 8 + i * .3, i * .1)))
        st_ += (f'<circle cx="{cx_:.0f}" cy="{cy_:.0f}" r="{rr:.0f}" fill="#e8f4ff"'
                f' opacity=".24"/>')
        for j in range(5):
            a = j * 1.25
            st_ += (f'<line x1="{cx_:.0f}" y1="{cy_:.0f}"'
                    f' x2="{cx_+math.cos(a)*rr:.0f}" y2="{cy_+math.sin(a)*rr:.0f}"'
                    f' stroke="#f2faff" stroke-width="3" opacity=".4"/>')
    s += SL(Z_SRED, st_)
    s += SL(Z_SRED, f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}"'
                    f' y2="{oy+oh}" stroke="url(#derev)" stroke-width="32"/>'
                    f'<line x1="{ox}" y1="{oy+oh*.5:.0f}" x2="{ox+ow}"'
                    f' y2="{oy+oh*.5:.0f}" stroke="url(#derev)" stroke-width="32"/>')
    s += SL(Z_SRED, f'<rect x="{ox-100}" y="{oy+oh+54}" width="{ow+200}" height="56"'
                    f' rx="10" fill="url(#dosk)" {o(9)}/>')
    # КОМАР идёт по стеклу, крупно
    hod = A.ease(A.seg(t, .2, 2.2))
    kx_ = ox + 180 + hod * 560
    ky_ = oy + oh * .48 + 26 * A.w(t, 1.5)
    s += SL(Z_SRED, _komar(kx_, ky_, 4.6, t, .1, True))
    for i in range(7):                   # следы-царапины на стекле
        p = i / 6
        s += SL(Z_SRED, f'<path d="M{ox+180+p*hod*560:.0f},{ky_+70:.0f} l24,8"'
                        f' stroke="#eaf4ff" stroke-width="5" opacity=".4"/>')
    # газета замахивается и опускается
    zam = A.ease(A.seg(t, 1.6, .5)) - A.ease(A.seg(t, 2.3, .7))
    gx_, gy_ = kx_ + 480, ky_ - 90 - zam * 120
    ruk, (rx_, ry_) = rukav(gx_ + 170, gy_ + 230, 130, -118 + 40 * zam, t,
                            "#3a3346", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, _gazeta_list(gx_, gy_, 480, 350, t, -20 + 36 * zam, 1279, 0.0))
    # дед улыбается, лампа рядом
    dx_ = 1700
    s += SL(Z_SRED, figura(dx_, 1070, 520, t, "#3a3346", "#ffd98a", False, .2,
                           True, 1.0, True, 1.4, True))
    s += SL(Z_SRED, _lampa_abazhur(250, 700, t, 1.9, 1.0))
    s += SL(Z_SRED, teplo(250, 520, 820, 700, .48 + .1 * abs(A.w(t, 1.6))))
    # комар раскланивается: шляпу долой
    rask = A.ease(A.seg(t, 2.6, .8))
    if rask > .02:
        s += SL(Z_SRED, f'<g transform="rotate({-26*rask:.1f} {kx_:.0f} {ky_:.0f})">'
                        f'<ellipse cx="{kx_+150:.0f}" cy="{ky_-110:.0f}" rx="56"'
                        f' ry="18" fill="#2b2a30" {o(4)}/>'
                        f'<path d="M{kx_+118:.0f},{ky_-112:.0f} q32,-52 64,0 Z"'
                        f' fill="#3a3842" {o(4)}/></g>')
    s += SL(Z_SRED, _chashka(1280, 940, 1.4, t, .3, KREM, True))
    s += SL(Z_SRED, par(1280, 866, t, 3, .4, 160, .4, .8))
    s += SL(Z_SRED, hodiki(1760, 300, t, 1.1))
    s += SL(Z_SRED, kot(620, 1012, t, 1.2, "#3b3430", True))
    s += SL(Z_PERED, zanaveska(380, 60, 440, 190, TKAN, t, 1))
    s += SL(Z_PERED, zanaveska(1580, 60, 440, 190, TKAN, t, -1))
    s += SL(Z_PERED, _chugunok(170, 1012, 1.2, t, True))
    s += vinetka(.46)
    return s


# ── 91 ─────────────────────────────────────────────────────────────────────
def gorodskoe_okno_s_chashkoy(t):
    """Широкое окно городской квартиры: за стеклом НАСТОЯЩЕЕ небо с солнцем,
    на подоконнике по краям — чашка чая и очки, человек в халате со спины.

    Из проёма убрано всё наше: чашка, цветок, ящик, ползунок ручки и три
    зелёные галочки. Вещи стоят на подоконнике ЗА пределами стекла, галочки
    отмечены на настенном листке сбоку. Прежде проём со стоком был завален
    нашими предметами целиком (осмотр 14.11)."""
    rnd = random.Random(9137)
    s = f'<rect width="{W}" height="{H}" fill="#2e2a26"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#6e6558"/>')
    for i in range(10):                  # обои тонкой полоской
        s += SL(Z_DAL, f'<rect x="{i*196:.0f}" y="0" width="70" height="1080"'
                       f' fill="#7a7164" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(930, "#6b4a2a"))
    s += SL(Z_SRED, tusklaya_lampochka(960, 70, t, 1.1, True))
    # ОКНО: проём по центру, но УЖЕ подоконника — вещи встают по его краям
    ox, oy, ow, oh = 540, 110, 900, 510
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="go91"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="url(#nden)"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#nden)"/>')
    sx_, sy_ = ox + ow * .72, oy + oh * .26
    za += (f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="{80+5*A.w(t,2.4):.0f}"'
           f' fill="#fff3cf" opacity=".95"/>')
    for i in range(14):                  # лучи солнца за стеклом
        a = i * .449 + t * .1
        za += (f'<line x1="{sx_:.0f}" y1="{sy_:.0f}"'
               f' x2="{sx_+math.cos(a)*(140+28*abs(A.w(t,2.0,i*.1))):.0f}"'
               f' y2="{sy_+math.sin(a)*(140+28*abs(A.w(t,2.0,i*.1))):.0f}"'
               f' stroke="#ffeeb8" stroke-width="8" opacity=".55"/>')
    for i in range(6):                   # облака плывут
        k = ((t * .03) + i * .18) % 1.2 - .1
        cx_ = ox - 180 + k * (ow + 360)
        cy_ = oy + 110 + (i % 3) * 86
        za += (f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="{130+i*18:.0f}"'
               f' ry="{38+i*6:.0f}" fill="#f4f8fc" opacity=".7"/>')
        za += (f'<ellipse cx="{cx_+80:.0f}" cy="{cy_+14:.0f}" rx="{94+i*11:.0f}"'
               f' ry="{28+i*5:.0f}" fill="#e8f0f8" opacity=".6"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.68:.0f}" width="{ow}" height="{oh*.32:.0f}"'
           f' fill="#8a949c" opacity=".6"/>')
    for i in range(5):                   # панельки города за стеклом
        bx = ox + 20 + i * 184
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.54:.0f}" width="150"'
               f' height="{oh*.32:.0f}" fill="#79838c" opacity=".85"/>')
        for j in range(8):
            za += (f'<rect x="{bx+14+(j % 4)*34:.0f}"'
                   f' y="{oy+oh*.58+(j//4)*48:.0f}" width="22" height="30"'
                   f' fill="#9fa9b0" opacity=".8"/>')
    vid += f'<g clip-path="url(#go91)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    # обвязка: пластиковый короб рамы, импост, откосы, широкий подоконник
    ob = (f'<rect x="{ox-50}" y="{oy-50}" width="{ow+100}" height="{oh+100}" rx="8"'
          f' fill="none" stroke="#e8e4da" stroke-width="100"/>')
    ob += (f'<line x1="{ox+ow*.46:.0f}" y1="{oy}" x2="{ox+ow*.46:.0f}"'
           f' y2="{oy+oh}" stroke="#e8e4da" stroke-width="36"/>')
    ob += f'<path d="{put}" fill="none" {o(8)}/>'
    ob += (f'<path d="M{ox+40},{oy+60} l{ow*.26:.0f},{oh*.40:.0f}" stroke="#ffffff"'
           f' stroke-width="18" opacity=".2"/>')
    ob += (f'<rect x="{ox-310}" y="{oy+oh+54}" width="{ow+620}" height="70" rx="12"'
           f' fill="#efebe2" {o(8)}/>')
    ob += (f'<rect x="{ox-310}" y="{oy+oh+54}" width="{ow+620}" height="18" rx="9"'
           f' fill="#ffffff" opacity=".55"/>')
    s += SL(Z_SRED, vid + ob)
    pw_y = oy + oh + 54                  # уровень подоконника
    # ПОДОКОННИК СЛЕВА: чашка чая с паром и очки — левее стекла
    s += SL(Z_SRED, _chashka(ox - 130, pw_y, 2.6, t, .2, KREM, True))
    s += SL(Z_SRED, par(ox - 130, pw_y - 170, t, 6, .6, 280, .42, 1.2))
    s += SL(Z_SRED, _ochki(ox - 270, pw_y - 24, 1.3, t, False))
    # ПОДОКОННИК СПРАВА: горшок с цветком — правее стекла
    s += SL(Z_SRED, f'<path d="M{ox+ow+150:.0f},{pw_y-140:.0f} h150 l-18,140 h-114 Z"'
                    f' fill="url(#glina)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{ox+ow+142:.0f}" y="{pw_y-154:.0f}" width="166"'
                    f' height="26" rx="8" fill="#b07a46" {o(5)}/>')
    for i in range(5):                   # домашний цветок
        a = -1.2 + i * .5
        s += SL(Z_SRED, f'<path d="M{ox+ow+225:.0f},{pw_y-150:.0f}'
                        f' q{math.cos(a)*44:.0f},{-66:.0f}'
                        f' {math.cos(a)*78+6*A.w(t,2.4,i*.2):.0f},{-120:.0f}"'
                        f' fill="none" stroke="{ZEL2}" stroke-width="{12-i}"'
                        f' stroke-linecap="round"/>')
        s += SL(Z_SRED, f'<ellipse cx="{ox+ow+225+math.cos(a)*80:.0f}"'
                        f' cy="{pw_y-272:.0f}" rx="30" ry="16" fill="#56763f"'
                        f' {o(3)}/>')
    # ЛИСТОК НА СТЕНЕ СПРАВА: три галочки встают на нём по словам
    lx_, ly_ = 1700, 250
    s += SL(Z_SRED, f'<rect x="{lx_-110:.0f}" y="{ly_-130:.0f}" width="220"'
                    f' height="300" rx="10" fill="url(#list)" {o(7)}/>')
    s += SL(Z_SRED, f'<circle cx="{lx_:.0f}" cy="{ly_-144:.0f}" r="12"'
                    f' fill="{ZHELEZ}" {o(3)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<line x1="{lx_-66:.0f}" y1="{ly_-30+i*76:.0f}"'
                        f' x2="{lx_+76:.0f}" y2="{ly_-30+i*76:.0f}"'
                        f' stroke="#d6cbae" stroke-width="6"/>')
        gk = A.out(A.seg(t, 1.2 + i * .4, .5))
        if gk > .02:
            gx_ = lx_ - 74
            gy_ = ly_ - 44 + i * 76
            s += SL(Z_SRED, f'<path d="M{gx_:.0f},{gy_:.0f} l{24*gk:.0f},{24*gk:.0f}'
                            f' l{46*gk:.0f},{-60*gk:.0f}" fill="none" stroke="#5ec07a"'
                            f' stroke-width="16" stroke-linecap="round"'
                            f' opacity="{.95*gk:.2f}"/>')
    # ЧЕЛОВЕК В ХАЛАТЕ СО СПИНЫ — слева, крупно, пальцы загибаются рукавом
    hx = 190
    s += SL(Z_PERED, figura(hx, 1080, 680, t, "#5b4a62", "#e8dcc0", False, .2,
                            False, 1.0, False, 1.0, False, False))
    s += SL(Z_PERED, f'<path d="M{hx-134:.0f},{1080-680*.64:.0f}'
                     f' q{134:.0f},{48:.0f} {268:.0f},0 l{-18:.0f},{400:.0f}'
                     f' q{-116:.0f},{30:.0f} {-232:.0f},0 Z" fill="#6b5a72"'
                     f' opacity=".55"/>')
    zag = A.ease(A.seg(t, 1.2, 1.4))
    ruk, (kx_, ky_) = rukav(hx + 110, 764, 180, -40 + 16 * zag, t, "#5b4a62",
                            "#e8dcc0", .2, 4.0)
    s += SL(Z_PERED, ruk)
    for i in range(3):                   # загнутые пальцы — овалами, без кистей
        zz = A.ease(A.seg(t, 1.2 + i * .4, .4))
        s += SL(Z_PERED, f'<ellipse cx="{kx_-20+i*26:.0f}"'
                         f' cy="{ky_-30+22*zz:.0f}" rx="13"'
                         f' ry="{28-15*zz:.0f}" fill="#f0cfae" {o(3)}/>')
    s += SL(Z_SRED, _batareya(640, 760 + 180, 700, 150, t, 9))
    s += SL(Z_SRED, kot(1620, 1012, t, 1.2, "#4a4440", False))
    s += SL(Z_SRED, hodiki(1870, 560, t, 1.1))
    s += SL(Z_PERED, zanaveska(420, 40, 480, 200, TKAN2, t, 1))
    s += SL(Z_PERED, zanaveska(1540, 40, 480, 200, TKAN2, t, -1))
    s += vinetka(.42)
    return s


# ── 92 ─────────────────────────────────────────────────────────────────────
def kinokamera_i_hlopushka(t):
    """Тёплый луч прожектора в темноте: старая деревянная кинокамера на
    треноге занимает пол-кадра, рядом складной режиссёрский стул и хлопушка.
    Ручка камеры крутится, в луче пляшут пылинки, луч рисует силуэты."""
    rnd = random.Random(9221)
    s = f'<rect width="{W}" height="{H}" fill="#120f14"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#1b1720"/>')
    for i in range(7):                   # дощатый задник в полутьме
        s += SL(Z_DAL, f'<rect x="{i*280:.0f}" y="0" width="246" height="880"'
                       f' fill="#241f2a" opacity=".7" {o(3)}/>')
    s += SL(Z_DAL, f'<rect y="880" width="{W}" height="200" fill="#1d1a22"/>')
    s += SL(Z_DAL, polovicy(900, "#3a3038"))
    # прожектор слева: тёплый конус через кадр
    px_, py_ = 150, 260
    pr = (f'<rect x="{px_-70:.0f}" y="{py_-90:.0f}" width="190" height="180"'
          f' rx="20" fill="#3a3f46" {o(7)}/>')
    pr += (f'<ellipse cx="{px_+124:.0f}" cy="{py_:.0f}" rx="26" ry="92"'
           f' fill="url(#zol)" {o(5)}/>')
    pr += (f'<rect x="{px_-20:.0f}" y="{py_+90:.0f}" width="46" height="150"'
           f' fill="#2f3337" {o(5)}/>')
    pr += (f'<path d="M{px_-80:.0f},{py_+240:.0f} h166 l24,34 h-214 Z"'
           f' fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, pr)
    s += SL(Z_SRED, lampa(px_ + 40, py_ + 60, t, .8, False))
    s += SL(Z_SRED, f'<path d="M{px_+140:.0f},{py_-80:.0f} L1920,80 L1920,900'
                    f' L{px_+140:.0f},{py_+80:.0f} Z" fill="{SVET}"'
                    f' opacity="{.13+.03*abs(A.w(t,2.2)):.2f}"/>')
    s += SL(Z_SRED, luch(px_ + 150, py_ - 60, 300, 780, t, .14))
    s += SL(Z_SRED, teplo(px_ + 200, py_ + 60, 900, 760, .3))
    for i in range(26):                  # пылинки пляшут в луче
        k = ((t * .22) + rnd.random()) % 1.0
        xx = px_ + 200 + k * 1500
        yy = py_ + rnd.uniform(-60, 420) + 40 * A.w(t, 2.4 + rnd.random(), k)
        s += SL(Z_SRED, f'<circle cx="{xx:.0f}" cy="{yy:.0f}"'
                        f' r="{rnd.uniform(2,6):.1f}" fill="#fff3d0"'
                        f' opacity="{.3+.5*abs(A.w(t,1.8,k)):.2f}"/>')
    # луч рисует силуэты на заднике
    for i, (sx_, h_) in enumerate(((1430, 470),)):
        s += SL(Z_DAL, f'<g opacity="{.42+.18*abs(A.w(t,2.6,i*.3)):.2f}">'
                       + figura(sx_, 880, h_, t, "#0d0b10", "#2a2430", False,
                                .2 * i, True, 1.0, False, 1.0, True, False,
                                False)
                       + '</g>')
    # КИНОКАМЕРА НА ТРЕНОГЕ — главный предмет в центре
    s += SL(Z_SRED, _kinokamera(860, 1010, 1.85, t, True))
    s += SL(Z_SRED, teplo(860, 560, 620, 520, .22))
    # складной режиссёрский стул
    stx, sty = 1350, 1010
    st_ = ten(stx, sty + 8, 120, 16, .5)
    for i in (-1, 1):
        st_ += (f'<line x1="{stx+i*110:.0f}" y1="{sty:.0f}" x2="{stx-i*30:.0f}"'
                f' y2="{sty-290:.0f}" stroke="url(#derev)" stroke-width="20"'
                f' stroke-linecap="round"/>')
        st_ += (f'<line x1="{stx+i*110:.0f}" y1="{sty:.0f}" x2="{stx+i*86:.0f}"'
                f' y2="{sty-180:.0f}" stroke="url(#derev)" stroke-width="16"/>')
    st_ += (f'<path d="M{stx-116:.0f},{sty-290:.0f} h232 q-10,36 -116,38'
            f' q-106,-2 -116,-38 Z" fill="{TKAN}" {o(6)}/>')
    st_ += (f'<rect x="{stx-116:.0f}" y="{sty-430:.0f}" width="232" height="76"'
            f' rx="10" fill="{TKAN}" {o(6)}/>')
    for i in (-1, 1):
        st_ += (f'<rect x="{stx+i*116-10:.0f}" y="{sty-440:.0f}" width="20"'
                f' height="170" rx="8" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, st_)
    # ХЛОПУШКА щёлкает в правой нижней четверти
    shch = A.out(A.seg(t, .6, .35)) * (1 - A.ease(A.seg(t, 1.4, .5)))
    s += SL(Z_SRED, _hlopushka(1540, 820, 1.45, t, shch, -14 + 10 * shch))
    ruk, _ = rukav(1760, 1010, 150, -116, t, "#2a2430", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, _chashka(560, 1012, 1.3, t, .2, "#9aa1a8", True))
    s += SL(Z_SRED, par(560, 950, t, 3, .35, 150, .4, .8))
    for i in range(5):                   # бобины с плёнкой у ног камеры
        s += SL(Z_SRED, f'<circle cx="{660+i*58:.0f}" cy="{1058-(i%2)*18:.0f}"'
                        f' r="{34-(i%3)*4:.0f}" fill="#2f3337" {o(5)}/>')
        s += SL(Z_SRED, f'<circle cx="{660+i*58:.0f}" cy="{1058-(i%2)*18:.0f}"'
                        f' r="10" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#0a0810", .8))
    s += SL(Z_LETIT, iskra_let(t, px_ + 120, py_, 6, 9227, 260, .3))
    s += vinetka(.54)
    return s


# ── 93 ─────────────────────────────────────────────────────────────────────
def ekran_selskogo_kluba(t):
    """Сельский клуб: простыня-экран на стене, перед ней ряды лавок со
    зрителями в тулупах, киномеханик крутит ручку передвижки.

    Экран заполнен нарисованным кадром кинохроники ЦЕЛИКОМ — деревня, обоз,
    двое бегут навстречу друг другу, зерно плёнки и царапины, — а не схемным
    домиком посреди пустого поля. Зал тоже наполнен: три ряда лавок, зрители
    со спины, луч проектора с пылью (осмотр 14.11)."""
    rnd = random.Random(9323)
    s = f'<rect width="{W}" height="{H}" fill="#15121a"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 126))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#241d22" opacity=".62"/>')
    s += SL(Z_DAL, polovicy(960, "#4a3a34"))
    # простыня-экран: углы на гвоздях, лёгкие волны по полотну
    shx, shy, shw, shh = 460, 30, 1000, 900
    pol_ = (f'<rect x="{shx}" y="{shy}" width="{shw}" height="{shh}" rx="6"'
            f' fill="#efeadf" {o(8)}/>')
    for i in range(7):                   # складки простыни
        pol_ += (f'<path d="M{shx+40+i*136:.0f},{shy+10}'
                 f' q{14+6*A.w(t,4.0,i*.2):.0f},{shh*.5:.0f} 0,{shh-20:.0f}"'
                 f' fill="none" stroke="#d8d2c4" stroke-width="10" opacity=".7"/>')
    s += SL(Z_SRED, pol_)
    # ПРОЁМ ПОД НАСТОЯЩИЙ КАДР — он же поле нарисованной кинохроники
    ox, oy, ow, oh = 540, 70, 840, 820
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="ek93"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#cfc8ba"/>'
    za = ""
    # НАРИСОВАННЫЙ КАДР КИНОХРОНИКИ ВО ВЕСЬ ЭКРАН: небо, поле, деревня, обоз
    za += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh*.46:.0f}"'
           f' fill="#e6e0d2"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.46:.0f}" width="{ow}" height="{oh*.54:.0f}"'
           f' fill="#8d8778"/>')
    for i in range(5):                   # облака кинохроники
        k = ((t * .04) + i * .22) % 1.2 - .1
        za += (f'<ellipse cx="{ox-120+k*(ow+240):.0f}" cy="{oy+oh*(.10+(i%3)*.07):.0f}"'
               f' rx="{120+i*16:.0f}" ry="{34+i*5:.0f}" fill="#f2eee2" opacity=".8"/>')
    for i in range(4):                   # дальняя гряда изб
        bx = ox + 20 + i * 220
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.40:.0f}" width="150"'
               f' height="{oh*.14:.0f}" fill="#5f5a4e"/>')
        za += (f'<path d="M{bx-24:.0f},{oy+oh*.40:.0f} l87,-56 l87,56 Z"'
               f' fill="#454138"/>')
        za += (f'<rect x="{bx+108:.0f}" y="{oy+oh*.30:.0f}" width="26"'
               f' height="{oh*.08:.0f}" fill="#55503f"/>')
        for j in range(5):               # дым над каждой избой живёт
            k = ((t * .22) + j * .2 + i * .1) % 1.0
            za += (f'<circle cx="{ox+133+i*220+16*A.w(t,2.2,j*.2):.0f}"'
                   f' cy="{oy+oh*.30-k*oh*.12:.0f}" r="{10+18*k:.0f}"'
                   f' fill="#efe9db" opacity="{.6*(1-k):.2f}"/>')
    for i in range(8):                   # пашня полосами к горизонту
        yy = oy + oh * (.56 + i * .055)
        za += (f'<path d="M{ox:.0f},{yy:.0f} q{ow*.5:.0f},{14+i*3:.0f} {ow:.0f},0"'
               f' fill="none" stroke="#a79f8e" stroke-width="{5+i}" opacity=".7"/>')
    # обоз уходит вдоль поля
    for i in range(3):
        wx = ox + 90 + i * 150 + ((t * 26) % 120)
        wy = oy + oh * .52 + i * 10
        za += (f'<rect x="{wx:.0f}" y="{wy-28:.0f}" width="88" height="34" rx="6"'
               f' fill="#6f6a5c"/>')
        for j in (0, 1):
            za += (f'<circle cx="{wx+14+j*60:.0f}" cy="{wy+10:.0f}" r="16"'
                   f' fill="none" stroke="#5e594d" stroke-width="7"/>')
        za += (f'<ellipse cx="{wx-34:.0f}" cy="{wy-14:.0f}" rx="32" ry="18"'
               f' fill="#6f6a5c"/>')
    # ДВОЕ НА ЭКРАНЕ БЕГУТ НАВСТРЕЧУ И ОБНИМАЮТСЯ
    vst = A.ease(A.seg(t, .6, 2.6))
    ax_ = ox + ow * .28 + vst * ow * .16
    bx_ = ox + ow * .72 - vst * ow * .16
    for px_, h_, pl_ in ((ax_, oh * .30, False), (bx_, oh * .27, True)):
        za += figura(px_, oy + oh * .88, h_, t, "#2f2c26", "#efe9db", pl_, .2,
                     False, .95, False, 2.0 * (1 - vst), False, True)
    za += (f'<ellipse cx="{(ax_+bx_)/2:.0f}" cy="{oy+oh*.70:.0f}"'
           f' rx="{90*vst:.0f}" ry="{60*vst:.0f}" fill="#f2eee2"'
           f' opacity="{.25*vst:.2f}"/>')
    for i in range(10):                  # зерно плёнки
        za += (f'<circle cx="{ox+rnd.uniform(0,ow):.0f}" cy="{oy+rnd.uniform(0,oh):.0f}"'
               f' r="{rnd.uniform(2,5):.1f}" fill="#fffaf0" opacity=".3"/>')
    for i in range(4):                   # плёночные царапины бегут
        xx = ox + ((t * 220 + i * 230) % ow)
        za += (f'<line x1="{xx:.0f}" y1="{oy}" x2="{xx-14:.0f}" y2="{oy+oh}"'
               f' stroke="#fffaf0" stroke-width="3" opacity=".35"/>')
    za += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#vig)"'
           f' opacity=".5"/>')
    vid += f'<g clip-path="url(#ek93)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    # обвязка: только короб экрана и гвозди по углам простыни
    ob = (f'<rect x="{ox-40}" y="{oy-40}" width="{ow+80}" height="{oh+80}" rx="8"'
          f' fill="none" stroke="#efeadf" stroke-width="80"/>')
    ob += (f'<path d="{put}" fill="none" stroke="#b9b2a2" stroke-width="7"/>')
    for gx_, gy_ in ((shx + 20, shy + 20), (shx + shw - 20, shy + 20),
                     (shx + 20, shy + shh - 20), (shx + shw - 20, shy + shh - 20)):
        ob += (f'<circle cx="{gx_:.0f}" cy="{gy_:.0f}" r="14" fill="#8d949b"'
               f' {o(3)}/>')
    s += SL(Z_SRED, vid + ob)
    # ЛУЧ ПРОЕКТОРА С ПЫЛЬЮ — от передвижки к экрану, мимо проёма
    kmx, kmy = 1740, 900
    drozh = 14 * A.w(t, 1.7, .1)
    s += SL(Z_SRED, f'<path d="M{kmx:.0f},{kmy-190:.0f} L{ox+ow+44:.0f},'
                    f'{oy+drozh-40:.0f} L{ox+ow+44:.0f},{oy+oh+drozh+40:.0f} Z"'
                    f' fill="{SVET}" opacity="{.17+.05*abs(A.w(t,1.3)):.2f}"/>')
    for i in range(22):                  # пыль пляшет в луче
        q = rnd.random()
        px_ = kmx - q * (kmx - ox - ow - 40)
        py_ = kmy - 190 + q * ((oy + oh * .5) - (kmy - 190)) + \
            (q * 180) * math.sin(i * 1.7 + t * 1.3)
        s += SL(Z_SRED, f'<circle cx="{px_:.0f}" cy="{py_:.0f}"'
                        f' r="{1.8+2.6*q:.1f}" fill="#fff6dd"'
                        f' opacity="{.25+.45*abs(A.w(t,2.0,i*.13)):.2f}"/>')
    s += SL(Z_SRED, teplo(kmx - 120, kmy - 200, 620, 520, .3))
    # передвижка и киномеханик
    pd = (f'<rect x="{kmx-110:.0f}" y="{kmy-270:.0f}" width="220" height="150"'
          f' rx="16" fill="#3a3f46" {o(7)}/>')
    for i, sgn in ((0, -1), (1, 1)):
        rot = (t * 120 + i * 50) % 360
        bx2, by2 = kmx + sgn * 70, kmy - 320
        pd += (f'<circle cx="{bx2:.0f}" cy="{by2:.0f}" r="52" fill="#2f3337" {o(6)}/>')
        pd += f'<g transform="rotate({rot:.0f} {bx2:.0f} {by2:.0f})">'
        for j in range(4):
            a = j * 1.5708
            pd += (f'<line x1="{bx2:.0f}" y1="{by2:.0f}"'
                   f' x2="{bx2+math.cos(a)*46:.0f}" y2="{by2+math.sin(a)*46:.0f}"'
                   f' stroke="#8d949b" stroke-width="8"/>')
        pd += '</g>'
    pd += (f'<rect x="{kmx-130:.0f}" y="{kmy-120:.0f}" width="260" height="30"'
           f' rx="10" fill="#2f3337" {o(5)}/>')
    for i in (-1, 1):
        pd += (f'<line x1="{kmx+i*90:.0f}" y1="{kmy-90:.0f}" x2="{kmx+i*110:.0f}"'
               f' y2="{kmy:.0f}" stroke="url(#derev)" stroke-width="18"/>')
    rh = (t * 300) % 360
    pd += (f'<g transform="rotate({rh:.0f} {kmx-120:.0f} {kmy-200:.0f})">'
           f'<line x1="{kmx-120:.0f}" y1="{kmy-200:.0f}" x2="{kmx-120:.0f}"'
           f' y2="{kmy-150:.0f}" stroke="#5d6168" stroke-width="12"/>'
           f'<circle cx="{kmx-120:.0f}" cy="{kmy-144:.0f}" r="14"'
           f' fill="url(#derev)" {o(3)}/></g>')
    s += SL(Z_SRED, pd)
    s += SL(Z_SRED, figura(kmx + 130, 1060, 450, t, "#3a3346", "#ffd98a", False,
                           .2, True, 1.0, False, 1.2, False, True))
    ruk, _ = rukav(kmx + 70, 820, 150, 188, t, "#3a3346", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    # ЗАЛ: три ряда лавок со зрителями со спины, ближний ряд крупнее
    for r, (ry_, h0, n_, x0, step, op_) in enumerate((
            (952, 230, 9, 150, 160, .85),
            (1012, 290, 8, 110, 190, .92),
            (1080, 360, 7, 90, 230, 1.0))):
        s += SL(Z_SRED if r < 2 else Z_PERED,
                f'<rect x="{x0-70:.0f}" y="{ry_-26:.0f}" width="{n_*step+60:.0f}"'
                f' height="26" rx="8" fill="url(#derev)" {o(6)}/>')
        for i in range(n_):
            zx_ = x0 + i * step + ((r % 2) * 40)
            s += SL(Z_SRED if r < 2 else Z_PERED,
                    figura(zx_, ry_, h0, t, "#241e2a", "#5a6a7a", i % 2 == 0,
                           .13 * i + r * .2, False, op_, i % 3 == 0, 1.0, False,
                           False, False))
    s += SL(Z_PERED, _shapka_meh(1820, 1046, 1.2, t, .3, 0.0))
    s += SL(Z_LETIT, iskra_let(t, kmx - 60, kmy - 320, 5, 9329, 220, .3))
    s += vinetka(.5)
    return s


# ── 94 ─────────────────────────────────────────────────────────────────────
def tri_afishi_na_stene_kluba(t):
    """Бревенчатая стена клуба: завклубом в кепке мажет кистью клей и клеит
    одну за другой три большие афиши — трактор в поле, пастуший рожок с
    лентой, золотой сноп. Мальчишки сбегаются смотреть."""
    rnd = random.Random(9421)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 9431)
    s += SL(Z_DAL, oblaka(t, 120, 4, 9433, .28, "#c8d4e2", 16.0))
    s += SL(Z_DAL, gryaz_polosa(900, 180, "#4a443a"))
    st = brevna(0, 60, W, 880, 120)
    st += f'<rect y="60" width="{W}" height="880" fill="#9c7049" opacity=".26"/>'
    st += f'<path d="M-40,130 L960,-140 L1960,130 Z" fill="#524638" opacity=".96" {o(9)}/>'
    s += SL(Z_DAL, st)
    s += SL(Z_DAL, f'<rect x="760" y="-90" width="110" height="220"'
                   f' fill="url(#kamen)" {o(7)}/>')
    s += SL(Z_DAL, dym(812, -80, t, 6, .24, 340, .38, "#d8cbbd", 1.2))
    s += SL(Z_SRED, tusklaya_lampochka(1760, 200, t, 1.6, True))
    s += SL(Z_SRED, teplo(1760, 330, 760, 640, .36 + .1 * abs(A.w(t, 1.6))))
    # ТРИ АФИШИ ложатся на стену по одной
    for i, (ax, vid_) in enumerate(((440, "traktor"), (960, "rozhok"),
                                    (1470, "snop"))):
        k = A.out(A.seg(t, .3 + i * .40, .55))
        if k < .03:
            continue
        s += SL(Z_SRED, f'<g opacity="{k:.2f}" transform="translate(0,'
                        f'{(1-k)*-120:.0f})">'
                        + _afisha(ax, 480, 430, 600, t, vid_, 9437 + i,
                                  (1 - k) * 12 - 2,
                                  A.ease(A.seg(t, 2.6 + i * .2, .6)) if i == 2 else 0.0)
                        + '</g>')
        for j in range(4):               # мазки клея под афишей
            s += SL(Z_SRED, f'<path d="M{ax-190+j*110:.0f},{760:.0f}'
                            f' q50,{-16+j*6:.0f} 96,2" fill="none"'
                            f' stroke="#e8e0cc" stroke-width="12"'
                            f' opacity="{.4*k:.2f}"/>')
    # завклубом с кистью и ведром клея
    zx = 1760
    maz = A.w(t, .8, .1)
    s += SL(Z_SRED, figura(zx, 1040, 520, t, "#3f4a3a", "#ffd98a", False, .2,
                           True, 1.0, False, 1.2, False, True))
    s += SL(Z_SRED, f'<path d="M{zx-70:.0f},{1040-520*.86:.0f} q70,-40 140,-6'
                    f' l6,22 q-74,-26 -146,10 Z" fill="#2e3a46" {o(5)}/>')
    ruk, (kx, ky) = rukav(zx - 100, 700, 180, 186 + 22 * maz, t, "#3f4a3a",
                          "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<rect x="{kx-24:.0f}" y="{ky-10:.0f}" width="48" height="90"'
                    f' rx="10" fill="url(#derev)"'
                    f' transform="rotate({-24+16*maz:.0f} {kx:.0f} {ky:.0f})"'
                    f' {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{kx-32:.0f}" y="{ky+76:.0f}" width="64" height="46"'
                    f' rx="8" fill="#d8cbb0"'
                    f' transform="rotate({-24+16*maz:.0f} {kx:.0f} {ky:.0f})"'
                    f' {o(4)}/>')
    s += SL(Z_SRED, _vedro_dach(1620, 1012, 1.2, t))
    # мальчишки сбегаются
    for i in range(4):
        beg = A.ease(A.seg(t, .8 + i * .22, 1.4))
        mxx = 120 + beg * (260 + i * 120)
        s += SL(Z_SRED, figura(mxx, 1056 + (i % 2) * 8, 300 + i * 18, t,
                               ("#5b2f3a", "#2e4a5a", "#4a3a2c", "#3f3a46")[i],
                               "#ffd0a0", False, .2 * i, True, 1.0, False, 1.6,
                               False, i % 2 == 0))
        s += SL(Z_SRED, para_izo_rta(mxx + 40, 1056 - (300 + i * 18) * .80, t,
                                     i * .3, .9, .45))
    s += SL(Z_SRED, kura(1180, 1012, t, 1.0, .4))
    s += SL(Z_SRED, _korzina_ryab(1340, 1012, 200, 150, t, 9439))
    s += SL(Z_PERED, f'<rect x="0" y="100" width="90" height="980" rx="10"'
                     f' fill="url(#brev)" {o(9)}/>')
    s += SL(Z_PERED, goloe_derevo(1890, 1080, 620, t, 9443, 7, "#2c2e36"))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 9449, .42, .9))
    s += vinetka(.44)
    return s


# ── 95 ─────────────────────────────────────────────────────────────────────
def semochnaya_ploschadka_sorok_chetve(t):
    """Съёмочный павильон: режиссёр в кепке с рупором стоит со спины у большой
    кинокамеры на тележке, перед ним декорация — городские часы на башне,
    стрелки встают на шесть. Осветитель поворачивает прожектор."""
    rnd = random.Random(9521)
    s = f'<rect width="{W}" height="{H}" fill="#161320"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#1f1b28"/>')
    s += SL(Z_DAL, svody(t, "#2e2838", 3))
    for i in range(9):                   # фермы и тросы павильона
        s += SL(Z_DAL, f'<line x1="{i*240:.0f}" y1="0" x2="{i*240+90:.0f}"'
                       f' y2="260" stroke="#3a3346" stroke-width="9"'
                       f' opacity=".7"/>')
    s += SL(Z_DAL, polovicy(930, "#423848"))
    # ДЕКОРАЦИЯ: городские часы на башне — главный предмет
    bx, by, bw = 1100, 930, 420
    bash = (f'<rect x="{bx-bw/2:.0f}" y="{by-700:.0f}" width="{bw:.0f}"'
            f' height="700" rx="10" fill="url(#kamen)" {o(9)}/>')
    bash += kladka(bx - bw / 2 + 8, by - 690, bw - 16, 680, 76, "url(#kamen)")
    bash += (f'<path d="M{bx-bw/2-40:.0f},{by-700:.0f} h{bw+80:.0f} l-60,-90'
             f' h{-bw+40:.0f} Z" fill="#5e564c" {o(8)}/>')
    bash += (f'<path d="M{bx-80:.0f},{by-790:.0f} h160 l-80,-150 Z"'
             f' fill="#4a443c" {o(7)}/>')
    for i in range(3):                   # арочные окна башни
        bash += (f'<path d="M{bx-50:.0f},{by-180-i*180:.0f} v-90'
                 f' q50,-54 100,0 v90 Z" fill="#241f2a" {o(5)}/>')
    s += SL(Z_SRED, bash)
    chx, chy, chr_ = bx, by - 560, 160
    ch = (f'<circle cx="{chx:.0f}" cy="{chy:.0f}" r="{chr_+22:.0f}"'
          f' fill="#5e564c" {o(8)}/>')
    ch += (f'<circle cx="{chx:.0f}" cy="{chy:.0f}" r="{chr_:.0f}"'
           f' fill="url(#krem)" {o(6)}/>')
    for i in range(12):                  # часовые деления — не цифры
        a = i * .5236
        r1 = chr_ * (.82 if i % 3 else .74)
        ch += (f'<line x1="{chx+math.cos(a)*r1:.0f}"'
               f' y1="{chy+math.sin(a)*r1:.0f}"'
               f' x2="{chx+math.cos(a)*chr_*.94:.0f}"'
               f' y2="{chy+math.sin(a)*chr_*.94:.0f}" stroke="#4a443c"'
               f' stroke-width="{10 if i % 3 == 0 else 6}"/>')
    vst = A.ease(A.seg(t, .8, 1.6))
    ach = math.radians(-90 + vst * 180 + (1 - vst) * 40)   # часовая встаёт вниз
    amn = math.radians(-90 + (1 - vst) * 300)              # минутная — вверх
    ch += (f'<line x1="{chx:.0f}" y1="{chy:.0f}"'
           f' x2="{chx+math.cos(ach)*chr_*.56:.0f}"'
           f' y2="{chy+math.sin(ach)*chr_*.56:.0f}" stroke="#2b2a2e"'
           f' stroke-width="20" stroke-linecap="round"/>')
    ch += (f'<line x1="{chx:.0f}" y1="{chy:.0f}"'
           f' x2="{chx+math.cos(amn)*chr_*.82:.0f}"'
           f' y2="{chy+math.sin(amn)*chr_*.82:.0f}" stroke="#2b2a2e"'
           f' stroke-width="13" stroke-linecap="round"/>')
    ch += (f'<circle cx="{chx:.0f}" cy="{chy:.0f}" r="16" fill="#2b2a2e"/>')
    s += SL(Z_SRED, ch)
    s += SL(Z_SRED, teplo(chx, chy, 620, 540, .26 + .08 * abs(A.w(t, 1.6))))
    # прожектор осветителя: поворачивается
    pov = 22 * A.ease(A.seg(t, 1.6, 1.4)) - 10
    plx, ply = 1740, 520
    s += SL(Z_SRED, f'<g transform="rotate({pov:.1f} {plx:.0f} {ply:.0f})">'
                    f'<rect x="{plx-90:.0f}" y="{ply-80:.0f}" width="180"'
                    f' height="160" rx="18" fill="#3a3f46" {o(7)}/>'
                    f'<ellipse cx="{plx-96:.0f}" cy="{ply:.0f}" rx="24" ry="80"'
                    f' fill="url(#zol)" {o(5)}/>'
                    f'<path d="M{plx-110:.0f},{ply-80:.0f} L{chx+200:.0f},'
                    f'{chy-120:.0f} L{chx+200:.0f},{chy+260:.0f} Z" fill="{SVET}"'
                    f' opacity="{.12+.03*abs(A.w(t,2.0)):.2f}"/></g>')
    s += SL(Z_SRED, lampa(plx - 40, ply + 40, t, .75, False))
    s += SL(Z_SRED, f'<rect x="{plx-16:.0f}" y="{ply+80:.0f}" width="34"'
                    f' height="330" fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, figura(1850, 1030, 460, t, "#2e3a46", "#ffd98a", False, .4,
                           True, 1.0, False, 1.2, False, True))
    # кинокамера на тележке едет
    ezd = A.ease(A.seg(t, .4, 2.4))
    kcx = 520 + ezd * 150
    s += SL(Z_SRED, f'<rect x="{kcx-230:.0f}" y="1010" width="460" height="40"'
                    f' rx="12" fill="#3a3f46" {o(7)}/>')
    for i in (-1, 1):
        rot = (ezd * 600 + (0 if i < 0 else 40)) % 360
        s += SL(Z_SRED, f'<circle cx="{kcx+i*160:.0f}" cy="1058" r="40"'
                        f' fill="#23262a" {o(6)}/>')
        s += SL(Z_SRED, f'<g transform="rotate({rot:.0f} {kcx+i*160:.0f} 1058)">'
                        f'<line x1="{kcx+i*160-34:.0f}" y1="1058"'
                        f' x2="{kcx+i*160+34:.0f}" y2="1058" stroke="#8d949b"'
                        f' stroke-width="8"/></g>')
    for i in range(13):                  # шпалы под рельсами
        s += SL(Z_SRED, f'<rect x="{i*150:.0f}" y="1024" width="56" height="64"'
                        f' rx="6" fill="#6b5a46" {o(3)}/>')
    for yy in (1030, 1072):              # две светлые нитки рельсов
        s += SL(Z_SRED, f'<rect x="0" y="{yy}" width="{W}" height="16" rx="8"'
                        f' fill="#c7ced4" {o(3)}/>')
        s += SL(Z_SRED, f'<rect x="0" y="{yy+2}" width="{W}" height="5"'
                        f' fill="#f0f5f8" opacity=".8"/>')
    s += SL(Z_SRED, f'<rect x="{kcx-210:.0f}" y="908" width="420" height="54"'
                    f' rx="10" fill="#7d6a52" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="{kcx-180:.0f}" y="962" width="360" height="30"'
                    f' rx="8" fill="#56483c" {o(5)}/>')
    s += SL(Z_SRED, _kinokamera(kcx, 908, 1.05, t, True, False))
    # режиссёр со спины с рупором
    rx_ = 280
    vzmah = A.ease(A.seg(t, 1.0, .5)) - A.ease(A.seg(t, 2.0, .6))
    s += SL(Z_SRED, figura(rx_, 1060, 560, t, "#3a3346", "#ffd98a", False, .1,
                           False, 1.0, True, 1.0, False, True, False))
    ruk, (kx, ky) = rukav(rx_ + 110, 740, 220, -70 - 40 * vzmah, t, "#3a3346",
                          "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<g transform="rotate({-30-30*vzmah:.0f} {kx:.0f} {ky:.0f})">'
                    f'<rect x="{kx-30:.0f}" y="{ky-18:.0f}" width="54" height="36"'
                    f' rx="10" fill="#5d6168" {o(5)}/>'
                    f'<path d="M{kx+24:.0f},{ky-30:.0f} l150,-86 l0,232'
                    f' l-150,-80 Z" fill="url(#zhel)" {o(7)}/>'
                    f'<ellipse cx="{kx+174:.0f}" cy="{ky+16:.0f}" rx="22"'
                    f' ry="116" fill="#cfd6dc" {o(5)}/>'
                    f'<ellipse cx="{kx+174:.0f}" cy="{ky+16:.0f}" rx="12"'
                    f' ry="100" fill="#3f454a" opacity=".8"/></g>')
    s += SL(Z_SRED, _hlopushka(780, 940, .9, t, 0.0, -18))
    s += SL(Z_SRED, _chashka(940, 1012, 1.2, t, .3, "#9aa1a8", True))
    s += SL(Z_SRED, par(940, 990, t, 3, .35, 140, .4, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0d0b12", .8))
    s += SL(Z_LETIT, iskra_let(t, plx - 80, ply, 6, 9529, 240, .3))
    s += vinetka(.5)
    return s


# ── 96 ─────────────────────────────────────────────────────────────────────
def parizhskaya_ulica_s_gruzovichkom(t):
    """Улочка парижского пригорода: серые дома со ставнями, у тротуара стоит
    пузатый грузовичок, шофёр в берете выскакивает из кабины с букетом,
    продавщица выбегает из булочной, голуби взлетают с мостовой.
    В витрине магазина идёт НАСТОЯЩИЙ кадр."""
    rnd = random.Random(9623)
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, False, 9629)
    s += oblaka(t, 130, 5, 9631, .3, "#dfe6ee", 18.0)
    # дома со ставнями во всю ширину
    dom = (f'<rect x="0" y="170" width="{W}" height="690" fill="#9aa0a0" {o(8)}/>')
    dom += kladka(0, 170, W, 690, 80, "#a8aeae")
    dom += (f'<path d="M-40,230 h2000 l-80,-86 h-1840 Z" fill="#6f7472" {o(7)}/>')
    for i in range(8):                   # мансардные окошки под крышей
        dom += (f'<rect x="{60+i*240:.0f}" y="178" width="92" height="44" rx="6"'
                f' fill="#3f4a52" {o(4)}/>')
    for i in range(7):                   # окна со ставнями
        wx = 40 + i * 268
        dom += (f'<rect x="{wx:.0f}" y="300" width="130" height="190" rx="6"'
                f' fill="#3f4a52" {o(5)}/>')
        for sgn in (-1, 1):
            otk = A.ease(A.seg(t, 1.2 + i * .18, .6))
            ug = sgn * (10 + 62 * otk)
            dom += (f'<g transform="rotate({ug:.0f} {wx+(0 if sgn<0 else 130):.0f} 370)">'
                    f'<rect x="{wx+(0 if sgn<0 else 92):.0f}" y="298" width="40"'
                    f' height="194" rx="5" fill="#5b7a62" {o(4)}/>'
                    f'<line x1="{wx+(20 if sgn<0 else 112):.0f}" y1="310"'
                    f' x2="{wx+(20 if sgn<0 else 112):.0f}" y2="480"'
                    f' stroke="#3f5a46" stroke-width="7"/></g>')
        dom += (f'<rect x="{wx-14:.0f}" y="494" width="158" height="18" rx="6"'
                f' fill="#7d8286" {o(3)}/>')
    s += SL(Z_DAL, dom)
    s += SL(Z_DAL, f'<rect y="860" width="{W}" height="220" fill="#6b6f72" {o(6)}/>')
    for r in range(3):                   # брусчатка уходит в перспективу
        for i in range(14 - r * 2):
            s += SL(Z_DAL, f'<rect x="{-40+i*(150+r*22):.0f}"'
                           f' y="{906+r*62:.0f}" width="{120+r*20:.0f}"'
                           f' height="{44+r*10:.0f}" rx="8" fill="#7a7e82"'
                           f' opacity="{.5+r*.12:.2f}"/>')
    s += SL(Z_DAL, f'<rect y="846" width="{W}" height="34" fill="#8d9296" {o(4)}/>')
    for i in range(7):                   # линии тротуара в точку схода
        s += SL(Z_DAL, f'<line x1="{i*280:.0f}" y1="1080" x2="{700+i*80:.0f}"'
                       f' y2="880" stroke="#5e6266" stroke-width="5"'
                       f' opacity=".45"/>')
    # фонарь улицы — тёплое пятно
    s += SL(Z_SRED, f'<rect x="196" y="300" width="30" height="580" rx="10"'
                    f' fill="#3a3f46" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M136,300 h150 l-24,-60 h-102 Z" fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M148,300 h126 l-14,140 h-98 Z" fill="url(#stekl)"'
                    f' opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, ogon(211, 400, t, .85, .2, 5))
    s += SL(Z_SRED, teplo(211, 370, 700, 600, .44 + .1 * abs(A.w(t, 1.6))))
    # БУЛОЧНАЯ С ВИТРИНОЙ: нарисованный вид, метка, рама поверх
    s += SL(Z_SRED, f'<rect x="1050" y="196" width="840" height="884" rx="8"'
                    f' fill="#8a6a52" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="1030" y="182" width="880" height="52" rx="10"'
                    f' fill="#5b3f2a" {o(7)}/>')
    # проём витрины ВЫСОКИЙ: в него ложится портрет
    ox, oy, ow, oh = 1080, 240, 780, 800
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="pa96"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#2e2a26"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#3a332c"/>')
    za += teplo(ox + ow * .5, oy + oh * .4, 520, 480, .5)
    for i in range(4):                   # полки с хлебами внутри витрины
        yy = oy + oh * (.30 + i * .17)
        za += (f'<rect x="{ox+40:.0f}" y="{yy:.0f}" width="{ow-80:.0f}"'
               f' height="22" rx="8" fill="#6b4a2a" {o(4)}/>')
        for j in range(4):
            za += (f'<ellipse cx="{ox+110+j*180:.0f}" cy="{yy-26:.0f}" rx="74"'
                   f' ry="30" fill="#c98c55" {o(4)}/>')
            za += (f'<ellipse cx="{ox+110+j*180:.0f}" cy="{yy-34:.0f}" rx="58"'
                   f' ry="20" fill="#e8bd84" opacity=".7"/>')
    za += (f'<ellipse cx="{ox+ow*.5:.0f}" cy="{oy+oh*.14:.0f}" rx="150" ry="60"'
           f' fill="{SVET}" opacity="{.3+.1*abs(A.w(t,1.7)):.2f}"/>')
    vid += f'<g clip-path="url(#pa96)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    ob = (f'<rect x="{ox-40}" y="{oy-40}" width="{ow+80}" height="{oh+80}" rx="8"'
          f' fill="none" stroke="#5b3f2a" stroke-width="80"/>')
    ob += (f'<rect x="{ox+ow/2-13:.0f}" y="{oy}" width="26" height="{oh}"'
           f' fill="#5b3f2a"/>')
    ob += (f'<path d="M{ox+40},{oy+70} l{ow*.3:.0f},{oh*.4:.0f}" stroke="#ffffff"'
           f' stroke-width="20" opacity=".16"/>')
    ob += f'<path d="{put}" fill="none" {o(9)}/>'
    ob += (f'<path d="M{ox-60},{oy-56} h{ow+120} l-40,-50 h{-ow-40} Z"'
           f' fill="#4a3220" {o(7)}/>')
    for i in range(9):                   # полосатый маркизный козырёк
        ob += (f'<path d="M{ox-40+i*(ow+80)/9:.0f},{oy-96:.0f}'
               f' l{(ow+80)/9:.0f},0 l{-16:.0f},{-64:.0f} l{-(ow+80)/9:.0f},0 Z"'
               f' fill="{KRAS if i % 2 else KREM}" {o(3)}/>')
    s += SL(Z_SRED, vid + ob)
    # пузатый грузовичок у тротуара
    gx, gy = 700, 1010
    s += SL(Z_SRED, _gruzovichok(gx, gy, 1.25, t))
    s += SL(Z_SRED, par(gx - 300, gy - 30, t, 4, .45, 170, .4, 1.0))
    # шофёр в берете выскакивает с букетом
    vysk = A.ease(A.seg(t, .5, 1.3))
    shx = gx - 120 + vysk * 240
    s += SL(Z_SRED, figura(shx + 300, 1066 + 20 * (1 - vysk), 500, t, "#2e3a46",
                           "#ffd0a0", False, .2, True, 1.0, False, 1.4, False,
                           True))
    s += SL(Z_SRED, f'<ellipse cx="{shx+300:.0f}" cy="{1066-500*.86:.0f}" rx="60"'
                    f' ry="26" fill="#2b3a4a" {o(4)}/>')
    ruk, (kx, ky) = rukav(shx + 360, 810, 150, -62, t, "#2e3a46", "#ffd0a0",
                          .2, 5.0)
    s += SL(Z_SRED, ruk)
    for i in range(9):                   # букет
        a = -1.2 + i * .3
        s += SL(Z_SRED, f'<line x1="{kx:.0f}" y1="{ky:.0f}"'
                        f' x2="{kx+math.cos(a)*70:.0f}"'
                        f' y2="{ky+math.sin(a)*70-30:.0f}" stroke="{ZEL2}"'
                        f' stroke-width="7"/>')
        s += SL(Z_SRED, f'<circle cx="{kx+math.cos(a)*76:.0f}"'
                        f' cy="{ky+math.sin(a)*76-36+4*A.w(t,2.2,i*.2):.0f}"'
                        f' r="16" fill="{(KRAS, "#e8743c", "#f2c14e")[i%3]}"'
                        f' {o(3)}/>')
    # продавщица выбегает из булочной
    vyb = A.ease(A.seg(t, 1.6, 1.2))
    s += SL(Z_SRED, figura(1000 - vyb * 110, 1060, 500, t, "#8a4a52", "#ffd0a0",
                           True, .5, True, 1.0, False, -2.0))
    s += SL(Z_SRED, f'<path d="M{940-vyb*110:.0f},{890:.0f} h120 l-10,130 h-100 Z"'
                    f' fill="#f2efe6" opacity=".9" {o(4)}/>')
    # голуби взлетают с мостовой
    for i in range(5):
        let = A.ease(A.seg(t, .9 + i * .14, .9))
        s += SL(Z_SRED, _golub(170 + i * 76, 1012, 1.4, t, i * .2, let))

    s += SL(Z_PERED, ramka_pp("levo", "#1a1a1e", .72))
    s += SL(Z_LETIT, iskra_let(t, 213, 520, 5, 9637, 220, .3))
    s += vinetka(.44)
    return s


# ── 97 ─────────────────────────────────────────────────────────────────────
def dve_podrugi_na_kinoprobah(t):
    """Коридор киностудии: длинная очередь девочек со спины, две подруги с
    косичками и школьными сумками стоят в хвосте — одна волнуется и поправляет
    бант, вторая зевает и ест булку. Дверь открывается, рука с хлопушкой зовёт."""
    rnd = random.Random(9721)
    s = f'<rect width="{W}" height="{H}" fill="#2b2a28"/>'
    # коридор с перспективой: стены и пол сходятся
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#7d7a70"/>')
    s += SL(Z_DAL, f'<path d="M0,0 L560,300 L560,800 L0,1080 Z" fill="#6b6860"/>')
    s += SL(Z_DAL, f'<path d="M{W},0 L1360,300 L1360,800 L{W},1080 Z"'
                   f' fill="#6b6860"/>')
    s += SL(Z_DAL, f'<rect x="560" y="300" width="800" height="500"'
                   f' fill="#8a8780" {o(7)}/>')
    s += SL(Z_DAL, f'<path d="M0,1080 L560,800 L1360,800 L{W},1080 Z"'
                   f' fill="#5e5a52"/>')
    for i in range(9):                   # половицы коридора в точку схода
        s += SL(Z_DAL, f'<line x1="{-60+i*250:.0f}" y1="1080"'
                       f' x2="{600+i*90:.0f}" y2="802" stroke="#4a463f"'
                       f' stroke-width="6" opacity=".55"/>')
    for i in range(4):
        s += SL(Z_DAL, f'<line x1="{120-i*30:.0f}" y1="{1060-i*80:.0f}"'
                       f' x2="{1800+i*30:.0f}" y2="{1060-i*80:.0f}"'
                       f' stroke="#4a463f" stroke-width="4" opacity=".3"/>')
    for i in range(7):                   # панель-поясок по стенам
        s += SL(Z_DAL, f'<path d="M{i*90:.0f},{640+i*18:.0f} L560,{700:.0f}"'
                       f' stroke="#56534c" stroke-width="10" opacity=".6"/>')
    s += SL(Z_DAL, f'<rect x="560" y="690" width="800" height="26"'
                   f' fill="#56534c" {o(3)}/>')
    s += SL(Z_SRED, tusklaya_lampochka(960, 120, t, 1.5, True))
    s += SL(Z_SRED, tusklaya_lampochka(700, 230, t, .9, True))
    s += SL(Z_SRED, teplo(960, 260, 900, 700, .34 + .1 * abs(A.w(t, 1.6))))
    # дверь в конце коридора открывается, из неё бьёт свет
    otk = A.ease(A.seg(t, 1.0, 1.0))
    dx, dy, dw, dh = 820, 360, 300, 440
    s += SL(Z_SRED, f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="6"'
                    f' fill="#2a2620" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}"'
                    f' fill="{SVET}" opacity="{.5*otk:.2f}"/>')
    s += SL(Z_SRED, dver(dx, dy, dw * (1 - otk * .62) + 6, dh, 0.0,
                         "url(#derev)", True, False))
    s += SL(Z_SRED, teplo(dx + dw * .5, dy + dh * .5, 520 * otk + 60,
                          440 * otk + 60, .4 * otk))
    # рука с хлопушкой указывает из двери
    if otk > .4:
        ruk, (kx, ky) = rukav(dx + dw - 20, dy + 210, 150, 12, t, "#3a3346",
                              "#ffd98a", .2, 5.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, _hlopushka(kx + 44, ky + 6, .45, t,
                                   A.out(A.seg(t, 2.0, .3)), -16))
    # ОЧЕРЕДЬ ДЕВОЧЕК со спины: от двери к нам, растут по размеру
    step = A.w(t, 1.6, .1)
    for i in range(7):
        p = i / 6
        zx_ = 1180 - p * 220 + (i % 2) * 34
        zy_ = 790 + p * 130
        h_ = 210 + p * 150
        s += SL(Z_SRED, figura(zx_, zy_ + 6 * step * ((i % 2) * 2 - 1), h_, t,
                               ("#5b2f3a", "#2e4a5a", "#4a3a5a", "#3f4a3a",
                                "#6b3a44", "#2e3a46", "#5a4a3a")[i],
                               "#ffd0a0", i % 3 == 0, .14 * i, False, 1.0,
                               False, 1.0, False, False, False))
        for sgn in (-1, 1):             # косички
            s += SL(Z_SRED, f'<path d="M{zx_+sgn*h_*.06:.0f},{zy_-h_*.78:.0f}'
                            f' q{sgn*h_*.05:.0f},{h_*.14:.0f}'
                            f' {sgn*h_*.02+2*step:.0f},{h_*.26:.0f}" fill="none"'
                            f' stroke="#5e4428" stroke-width="{max(4, h_*.028):.0f}"'
                            f' stroke-linecap="round"/>')
    # ДВЕ ПОДРУГИ крупно в хвосте очереди
    ax, bx_ = 330, 700
    s += SL(Z_SRED, figura(ax, 1076, 680, t, "#8a4a52", "#ffd0a0", False, .3,
                           False, 1.0, False, 1.2, False, True))
    s += SL(Z_SRED, figura(bx_, 1080, 650, t, "#2e4a5a", "#ffd0a0", False, .7,
                           False, 1.0, False, -1.2, False, True))
    for sgn in (-1, 1):                 # косички подруг
        for cx_, h_ in ((ax, 680), (bx_, 650)):
            s += SL(Z_SRED, f'<path d="M{cx_+sgn*h_*.07:.0f},{1076-h_*.78:.0f}'
                            f' q{sgn*h_*.06:.0f},{h_*.16:.0f}'
                            f' {sgn*h_*.02+4*step:.0f},{h_*.30:.0f}" fill="none"'
                            f' stroke="#5e4428" stroke-width="{h_*.03:.0f}"'
                            f' stroke-linecap="round"/>')
    # бант: её поправляют
    pop = A.w(t, 1.1, .2)
    bny = 1076 - 680 * .96
    s += SL(Z_SRED, f'<g transform="rotate({6*pop:.1f} {ax:.0f} {bny:.0f})">'
                    f'<path d="M{ax-90:.0f},{bny:.0f} q52,-56 86,-6'
                    f' q34,-52 86,6 q-38,52 -86,12 q-46,38 -86,-12 Z"'
                    f' fill="{TKAN}" {o(6)}/>'
                    f'<circle cx="{ax-4:.0f}" cy="{bny+6:.0f}" r="18"'
                    f' fill="#8a1c24" {o(4)}/></g>')
    ruk, (kx, ky) = rukav(ax + 90, 740, 150, -78 + 14 * pop, t, "#8a4a52",
                          "#ffd0a0", .2, 6.0)
    s += SL(Z_SRED, ruk)
    # вторая зевает и ест булку, булка падает
    zev = max(0.0, A.w(t, 2.4, .3))
    s += SL(Z_SRED, f'<ellipse cx="{bx_+30:.0f}" cy="{1080-650*.80:.0f}" rx="26"'
                    f' ry="{10+22*zev:.0f}" fill="#7d2f28" {o(3)}/>')
    pad = A.ease(A.seg(t, 2.2, .8))
    bulx = bx_ + 150
    buly = 860 + pad * 200
    s += SL(Z_SRED, f'<g transform="rotate({pad*140:.0f} {bulx:.0f} {buly:.0f})">'
                    f'<ellipse cx="{bulx:.0f}" cy="{buly:.0f}" rx="66" ry="44"'
                    f' fill="#c98c55" {o(6)}/>'
                    f'<ellipse cx="{bulx-14:.0f}" cy="{buly-12:.0f}" rx="40"'
                    f' ry="22" fill="#e8bd84" opacity=".8"/>'
                    f'<path d="M{bulx-40:.0f},{buly-16:.0f} q40,-18 80,0"'
                    f' fill="none" stroke="#a8641e" stroke-width="7"/></g>')
    ruk2, _ = rukav(bx_ + 80, 800, 130, -24, t, "#2e4a5a", "#ffd0a0", .4, 6.0)
    s += SL(Z_SRED, ruk2)
    for i, cx_ in ((0, ax - 150), (1, bx_ + 190)):   # школьные сумки
        s += SL(Z_SRED, f'<rect x="{cx_-70:.0f}" y="{950-i*10:.0f}" width="140"'
                        f' height="110" rx="14" fill="{("#5a3a22", "#3a4a5a")[i]}"'
                        f' {o(6)}/>')
        s += SL(Z_SRED, f'<path d="M{cx_-70:.0f},{966-i*10:.0f} h140" stroke="#2f2a22"'
                        f' stroke-width="8"/>')
        s += SL(Z_SRED, f'<path d="M{cx_-40:.0f},{950-i*10:.0f} q40,-80 80,0"'
                        f' fill="none" stroke="{("#5a3a22", "#3a4a5a")[i]}"'
                        f' stroke-width="12"/>')
    s += SL(Z_SRED, lavka(1420, 920, 380))
    s += SL(Z_SRED, _chashka(1620, 916, 1.2, t, .2, KREM, True))
    s += SL(Z_SRED, par(1620, 850, t, 3, .4, 150, .4, .8))
    s += SL(Z_PERED, ramka_pp("pravo", "#1d1b16", .7))
    s += vinetka(.44)
    return s


# ── 98 ─────────────────────────────────────────────────────────────────────
def dve_afishi_parizhskogo_kinoteatra(t):
    """Фасад кинотеатра с бегущими лампочками: в двух световых коробах две
    афиши — паровоз в клубах пара и женская шляпка с вуалью, меч, воткнутый в
    зелёный холм. Прохожие останавливаются, огни отражаются в мокрой мостовой."""
    rnd = random.Random(9829)
    s = f'<rect width="{W}" height="{H}" fill="#161822"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#1f2230"/>')
    fas = (f'<rect x="0" y="40" width="{W}" height="860" fill="#3a3a48" {o(8)}/>')
    fas += kladka(0, 40, W, 860, 82, "#44445a")
    fas += (f'<path d="M-40,120 h2000 l-90,-90 h-1820 Z" fill="#2e2e3c" {o(7)}/>')
    s += SL(Z_DAL, fas)
    s += SL(Z_DAL, f'<rect y="880" width="{W}" height="200" fill="#2a2c36" {o(5)}/>')
    # бегущие лампочки по фасаду и вокруг коробов
    s += SL(Z_SRED, _lampochki(60, 140, 1800, 26, t, 15, SVET))
    s += SL(Z_SRED, _lampochki(60, 862, 1800, 26, t, 13, "#ffd0a0"))
    s += SL(Z_SRED, teplo(960, 480, 1500, 900, .22 + .05 * abs(A.w(t, 1.4))))
    # ДВА СВЕТОВЫХ КОРОБА С АФИШАМИ
    for i, (cx_, vid_) in enumerate(((520, "parovoz"), (1420, "mech"))):
        kor = (f'<rect x="{cx_-310:.0f}" y="190" width="620" height="700" rx="14"'
               f' fill="#2b2b36" {o(8)}/>')
        kor += (f'<rect x="{cx_-280:.0f}" y="220" width="560" height="640" rx="8"'
                f' fill="#efe7d2" opacity=".2"/>')
        s += SL(Z_SRED, kor)
        s += SL(Z_SRED, _afisha(cx_, 540, 530, 610, t, vid_, 9833 + i, 0.0, 0.0))
        if vid_ == "parovoz":            # шляпка с вуалью — на той же афише
            s += SL(Z_SRED, _afisha(cx_ + 140, 700, 180, 190, t, "shlyapka",
                                    9839, -4, 0.0))
        s += SL(Z_SRED, _lampochki(cx_ - 300, 196, 600, 13, t, 12, SVET))
        s += SL(Z_SRED, _lampochki(cx_ - 300, 884, 600, 13, t, 12, SVET))
        s += SL(Z_SRED, teplo(cx_, 540, 700, 700, .20))
    s += SL(Z_SRED, par(640, 520, t, 5, .4, 230, .42, 1.2))
    # козырёк над входом и фонари
    s += SL(Z_SRED, f'<path d="M820,900 h280 l40,-70 h-360 Z" fill="#3a3a48" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="860" y="900" width="200" height="180" rx="8"'
                    f' fill="#241f28" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="880" y="920" width="160" height="160"'
                    f' fill="{SVET}" opacity="{.28+.1*abs(A.w(t,1.8)):.2f}"/>')
    for i, fx_ in ((0, 790), (1, 1130)):
        s += SL(Z_SRED, f'<rect x="{fx_-10:.0f}" y="620" width="20" height="280"'
                        f' rx="8" fill="#2f3337" {o(5)}/>')
        s += SL(Z_SRED, f'<path d="M{fx_-54:.0f},620 h108 l-14,-40 h-80 Z"'
                        f' fill="#2f3337" {o(4)}/>')
        s += SL(Z_SRED, ogon(fx_, 580, t, .55, .2 + i * .3, 4))
        s += SL(Z_SRED, teplo(fx_, 580, 420, 360, .34))
    # прохожие останавливаются
    for i, (zx_, h_, col, pl) in enumerate(((240, 430, "#2b3040", False),
                                            (1020, 470, "#3f2f3a", True),
                                            (1700, 440, "#2e3a46", False))):
        stop = A.ease(A.seg(t, .6 + i * .5, 1.0))
        s += SL(Z_SRED, figura(zx_ + (1 - stop) * (60 - i * 50), 1010, h_, t,
                               col, "#cfe4f5", pl, .2 * i, True, 1.0, True,
                               1.0, i == 2, i != 2))
        s += SL(Z_SRED, para_izo_rta(zx_ + 54, 1010 - h_ * .80, t, i * .3, 1.1,
                                     .5))
    # мокрая мостовая: огни отражаются полосами
    s += SL(Z_SRED, f'<rect y="1000" width="{W}" height="80" fill="#30333e"'
                    f' opacity=".9"/>')
    for i in range(14):
        xx = 60 + i * 136
        yar = .18 + .24 * max(0.0, 1 - abs(((t * .9 + i / 14) % 1.0) - .5) * 3.2)
        s += SL(Z_SRED, f'<rect x="{xx:.0f}" y="1000" width="26" height="80"'
                        f' fill="{SVET}" opacity="{yar:.2f}"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{160+i*260:.0f}" cy="{1046+(i%3)*10:.0f}"'
                        f' rx="{90+i*8:.0f}" ry="14" fill="#6a7a84"'
                        f' opacity=".32"/>')
    s += SL(Z_SRED, _golub(1760, 1012, 1.1, t, .3, 0.0))
    s += SL(Z_PERED, ramka_pp("oba", "#101218", .76))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 9851, .4, .9))
    s += vinetka(.46)
    return s


# ── 99 ─────────────────────────────────────────────────────────────────────
def devochka_vybegaet_za_dver(t):
    """Дверь с пятью подковами над притолокой, рядом на лавке Ерёма грозит
    пальцем. Девочка с косичками весело проскальзывает у него под рукой и
    распахивает дверь: за ней красная дорожка и вспышки."""
    rnd = random.Random(9931)
    s = f'<rect width="{W}" height="{H}" fill="#2a2018"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 900, 118))
    s += SL(Z_DAL, f'<rect width="{W}" height="900" fill="#49351f" opacity=".4"/>')
    s += SL(Z_DAL, polovicy(900, "url(#pol)"))
    s += SL(Z_DAL, pech(40, 300, 300, 560, t, True, True, False))
    s += SL(Z_SRED, svecha(1330, 760, t, .2, 2.4, 150))
    s += SL(Z_SRED, teplo(1330, 690, 720, 600, .48 + .12 * abs(A.w(t, 1.5))))
    # ДВЕРЬ распахивается: за ней красная дорожка и вспышки
    otk = A.out(A.seg(t, 1.0, 1.2))
    dx, dy, dw, dh = 560, 230, 640, 850
    s += SL(Z_SRED, f'<rect x="{dx-40}" y="{dy-40}" width="{dw+80}"'
                    f' height="{dh+40}" rx="10" fill="url(#derev)" {o(9)}/>')
    za = (f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#1a1824"/>')
    za += (f'<path d="M{dx+60:.0f},{dy+dh:.0f} L{dx+dw*.34:.0f},{dy+dh*.46:.0f}'
           f' L{dx+dw*.66:.0f},{dy+dh*.46:.0f} L{dx+dw-60:.0f},{dy+dh:.0f} Z"'
           f' fill="{KRAS}" {o(6)}/>')
    for i in range(6):                   # ступени дорожки
        za += (f'<path d="M{dx+70+i*18:.0f},{dy+dh-40-i*58:.0f}'
               f' h{dw-140-i*36:.0f}" stroke="#8a1c24" stroke-width="8"'
               f' opacity=".7"/>')
    for i in range(7):                   # вспышки сверкают
        yar = max(0.0, A.w(t, .5 + i * .13, i * .21))
        za += (f'<circle cx="{dx+70+i*78:.0f}" cy="{dy+dh*.30+(i%3)*50:.0f}"'
               f' r="{24+40*yar:.0f}" fill="#ffffff"'
               f' opacity="{.85*yar*otk:.2f}"/>')
        if yar > .6:
            for j in range(6):
                a = j * 1.047
                za += (f'<line x1="{dx+70+i*78:.0f}"'
                       f' y1="{dy+dh*.30+(i%3)*50:.0f}"'
                       f' x2="{dx+70+i*78+math.cos(a)*90*yar:.0f}"'
                       f' y2="{dy+dh*.30+(i%3)*50+math.sin(a)*90*yar:.0f}"'
                       f' stroke="#ffffff" stroke-width="7"'
                       f' opacity="{.6*yar*otk:.2f}"/>')
    za += (f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#fff6dc"'
           f' opacity="{.12*otk:.2f}"/>')
    s += SL(Z_SRED, za)
    s += SL(Z_SRED, f'<g transform="translate({dx:.0f},0)'
                    f' scale({1-otk*.72:.3f},1) translate({-dx:.0f},0)">'
                    + dver(dx, dy, dw, dh, 0.0, "url(#derev)", True, False)
                    + '</g>')
    s += SL(Z_SRED, teplo(dx + dw * .5, dy + dh * .4, 700 * otk + 80,
                          600 * otk + 80, .34 * otk))
    # ПЯТЬ ПОДКОВ над притолокой
    for i in range(5):
        s += SL(Z_SRED, _podkova_rzh(dx + 70 + i * 130, dy - 100, .62, t,
                                     2.0 * (i - 2)))
    s += SL(Z_SRED, f'<path d="M{dx-120},{dy-180} h{dw+240} l-64,-70 h{-dw-112} Z"'
                    f' fill="{DOSKA2}" {o(9)}/>')
    # Ерёма на лавке грозит пальцем и хохочет в бороду
    s += SL(Z_SRED, lavka(1380, 960, 440))
    ex = 1560
    hoh = 8 * A.w(t, 1.0, .2)
    s += SL(Z_SRED, f'<g transform="rotate({hoh*.3:.1f} {ex:.0f} 960)">'
                    + figura(ex, 960, 640, t, "#4a3a2c", "#ffd98a", False, .2,
                             False, 1.0, True, 1.0 + hoh * .2, True)
                    + '</g>')
    ruk, (kx, ky) = rukav(ex - 150, 660, 120, 196 - 16 * A.w(t, .9), t,
                          "#4a3a2c", "#ffd98a", .2, 7.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky+6:.0f}" rx="52" ry="46"'
                    f' fill="#f0cfae" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{kx-10:.0f},{ky-24:.0f} l{-6:.0f},{-86:.0f}"'
                    f' fill="none" stroke="#f0cfae" stroke-width="34"'
                    f' stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M{kx-10:.0f},{ky-24:.0f} l{-6:.0f},{-86:.0f}"'
                    f' fill="none" stroke="{K}" stroke-width="4" opacity=".6"/>')
    for i in range(3):                   # согнутые пальцы кулака
        s += SL(Z_SRED, f'<ellipse cx="{kx+16+i*6:.0f}" cy="{ky-10+i*26:.0f}"'
                        f' rx="20" ry="13" fill="#e2bb98" {o(3)}/>')
    # девочка проскальзывает под рукой к двери
    skol = A.ease(A.seg(t, .3, 1.6))
    gx = 1300 - skol * 420
    s += SL(Z_SRED, f'<g transform="rotate({-10-8*skol:.1f} {gx:.0f} 1070)">'
                    + figura(gx, 1070, 430, t, "#8a4a52", "#ffd98a", False, .6,
                             True, 1.0, False, 1.0, False, True)
                    + '</g>')
    for sgn in (-1, 1):                 # косички на бегу
        s += SL(Z_SRED, f'<path d="M{gx+sgn*30:.0f},{1070-430*.78:.0f}'
                        f' q{40+sgn*10:.0f},{30:.0f} {70:.0f},{70+10*A.w(t,1.2,sgn*.2):.0f}"'
                        f' fill="none" stroke="#5e4428" stroke-width="13"'
                        f' stroke-linecap="round"/>')
    s += SL(Z_SRED, kot(1180, 1000, t, 1.2, "#3b3430", False))
    s += SL(Z_PERED, ramka_pp("levo", "#1a120c", .78))
    s += SL(Z_PERED, _valenok(1760, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_LETIT, iskra_let(t, 1500, 720, 6, 9941, 260, .35))
    s += vinetka(.46)
    return s


# ── 100 ────────────────────────────────────────────────────────────────────
def babushkina_dver_s_sekretami(t):
    """Старая дверь бабушкиного дома изнутри на пол-кадра: обита дерматином в
    клетку, цепкий крючок, половик у порога. По очереди подсвечиваются три
    места — ржавая подкова над притолокой, пучок сухой рябины за наличником и
    английская булавка, воткнутая в косяк. Внучка встаёт на цыпочки."""
    rnd = random.Random(10007)
    s = f'<rect width="{W}" height="{H}" fill="#2e2620"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#7a6a58"/>')
    for i in range(10):                  # обои прихожей
        s += SL(Z_DAL, f'<rect x="{i*196:.0f}" y="0" width="74" height="1080"'
                       f' fill="#8a7a66" opacity=".45"/>')
    s += SL(Z_DAL, polovicy(930, "#6b4a2a"))
    s += SL(Z_DAL, _veshalka(60, 230, 300, t, 3, True))
    s += SL(Z_SRED, tusklaya_lampochka(300, 110, t, 1.4, True))
    s += SL(Z_SRED, teplo(300, 250, 820, 700, .38 + .1 * abs(A.w(t, 1.6))))
    # ДВЕРЬ, обитая дерматином — главный предмет
    dx, dy, dw, dh = 620, 180, 720, 890
    dv = (f'<rect x="{dx-44}" y="{dy-44}" width="{dw+88}" height="{dh+44}" rx="10"'
          f' fill="url(#derev)" {o(10)}/>')
    dv += (f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="8"'
           f' fill="#5a3f3a" {o(9)}/>')
    for i in range(5):                   # дерматин в клетку на гвоздиках
        for j in range(6):
            cx_ = dx + 70 + i * (dw - 140) / 4
            cy_ = dy + 80 + j * (dh - 160) / 5
            dv += (f'<circle cx="{cx_:.0f}" cy="{cy_:.0f}" r="11"'
                   f' fill="url(#zhel)" {o(3)}/>')
            dv += (f'<circle cx="{cx_-3:.0f}" cy="{cy_-3:.0f}" r="4"'
                   f' fill="#e8eef6" opacity=".5"/>')
    for i in range(5):                  # прошивка дерматина — ромбы наискось
        for j in range(6):
            cx_ = dx + 70 + i * (dw - 140) / 4
            cy_ = dy + 80 + j * (dh - 160) / 5
            dv += (f'<path d="M{cx_:.0f},{cy_:.0f} l{(dw-140)/8:.0f},'
                   f'{(dh-160)/10:.0f}" stroke="#3f2b26" stroke-width="12"'
                   f' opacity=".85"/>')
            dv += (f'<path d="M{cx_:.0f},{cy_:.0f} l{(dw-140)/8:.0f},'
                   f'{-(dh-160)/10:.0f}" stroke="#3f2b26" stroke-width="12"'
                   f' opacity=".85"/>')
            dv += (f'<path d="M{cx_+6:.0f},{cy_+6:.0f} l{(dw-140)/8:.0f},'
                   f'{(dh-160)/10:.0f}" stroke="#7a5a52" stroke-width="5"'
                   f' opacity=".5"/>')
    dv += (f'<ellipse cx="{dx+dw-80:.0f}" cy="{dy+dh*.50:.0f}" rx="26" ry="38"'
           f' fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, dv)
    # цепкий крючок с цепочкой
    s += SL(Z_SRED, f'<rect x="{dx-30:.0f}" y="{dy+dh*.40:.0f}" width="54"'
                    f' height="26" rx="8" fill="#5d6168" {o(5)}/>')
    kch = 7 * A.w(t, 2.2, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {dx+24:.0f} {dy+dh*.42:.0f})">'
                    f'<path d="M{dx+24:.0f},{dy+dh*.42:.0f} q80,16 120,-10'
                    f' q16,-12 4,-28" fill="none" stroke="#8d949b"'
                    f' stroke-width="14" stroke-linecap="round"/></g>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{dx+40+i*22:.0f}"'
                        f' cy="{dy+dh*.44+5*A.w(t,2.0,i*.2):.0f}" r="9"'
                        f' fill="none" stroke="#8d949b" stroke-width="5"/>')
    # три секрета подсвечиваются по очереди
    pod1 = A.ease(A.seg(t, .5, .6)) * (1 - A.ease(A.seg(t, 2.6, .6)))
    pod2 = A.ease(A.seg(t, 1.6, .6)) * (1 - A.ease(A.seg(t, 3.6, .6)))
    pod3 = A.ease(A.seg(t, 2.8, .6))
    px_, py_ = dx + dw / 2, dy - 120
    s += SL(Z_SRED, teplo(px_, py_ + 110, 560 * pod1 + 80, 460 * pod1 + 80,
                          .54 * pod1 + .08))
    s += SL(Z_SRED, _podkova_rzh(px_, py_ + 110, 1.05, t))
    s += SL(Z_SRED, f'<path d="M{dx-130},{dy-184} h{dw+260} l-62,-66 h{-dw-136} Z"'
                    f' fill="{DOSKA2}" {o(9)}/>')
    # пучок сухой рябины за наличником
    rx_, ry_ = dx - 70, dy + 250
    s += SL(Z_SRED, teplo(rx_, ry_, 420 * pod2 + 50, 360 * pod2 + 50, .46 * pod2))
    for i in range(5):                  # пучок стянут в кисть, не враскид
        a = -.5 + i * .25
        s += SL(Z_SRED, f'<line x1="{rx_:.0f}" y1="{ry_+118:.0f}"'
                        f' x2="{rx_+math.cos(a)*34:.0f}"'
                        f' y2="{ry_+118-abs(math.sin(a))*20-86:.0f}"'
                        f' stroke="#6b5234" stroke-width="{11-i}"'
                        f' stroke-linecap="round"/>')
    s += SL(Z_SRED, grozd_ryabiny(rx_ + 20, ry_ + 30, t, 1.5, 16, 10009, .2))
    s += SL(Z_SRED, f'<path d="M{rx_-30:.0f},{ry_+120:.0f} q34,16 68,0"'
                    f' fill="none" stroke="#c2ab86" stroke-width="10"/>')
    # английская булавка в косяке поблёскивает
    bx_, by_ = dx + dw + 60, dy + 480
    s += SL(Z_SRED, teplo(bx_, by_, 320 * pod3 + 40, 280 * pod3 + 40, .42 * pod3))
    bl = .35 + .55 * (0.5 + 0.5 * A.w(t, 1.6, .2))
    s += SL(Z_SRED, f'<path d="M{bx_-16:.0f},{by_-120:.0f} q-54,118 4,232'
                    f' q48,-16 22,-90" fill="none" stroke="#e2e9ef"'
                    f' stroke-width="18" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<circle cx="{bx_-12:.0f}" cy="{by_+118:.0f}" r="24"'
                    f' fill="none" stroke="#e2e9ef" stroke-width="13"/>')
    s += SL(Z_SRED, f'<circle cx="{bx_-6:.0f}" cy="{by_-66:.0f}" r="15"'
                    f' fill="#ffffff" opacity="{bl:.2f}"/>')
    # половик у порога сминается
    sm = A.w(t, 1.3, .1)
    s += SL(Z_SRED, f'<rect x="{dx+60:.0f}" y="{dy+dh-54:.0f}" width="{dw-120:.0f}"'
                    f' height="72" rx="14" fill="{TKAN2}" {o(7)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{dx+90+i*62:.0f},{dy+dh-46:.0f}'
                        f' q{6+5*sm:.0f},32 0,60" fill="none" stroke="#2f4a62"'
                        f' stroke-width="9" opacity=".8"/>')
    # внучка встаёт на цыпочки к подкове
    cyp = A.ease(A.seg(t, .8, 1.2))
    vx = dx + dw * .32
    s += SL(Z_SRED, figura(vx, 1058 - 26 * cyp, 480, t, "#8a4a52", "#ffd98a",
                           False, .4, False, 1.0, False, 1.2, False, True))
    ruk, (kx, ky) = rukav(vx + 80, 760 - 26 * cyp, 190, -78, t, "#8a4a52",
                          "#ffd98a", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="28" ry="21"'
                    f' fill="#8a4a52" {o(5)}/>')
    s += SL(Z_SRED, _valenok(400, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_SRED, _valenok(510, 1012, .86, t, .6, True, "#6e6358"))
    s += SL(Z_SRED, kot(1700, 1012, t, 1.3, "#4a4440", True))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="70" height="1080" fill="#241d16"'
                     f' opacity=".9"/>')
    s += SL(Z_PERED, _varezhka(1800, 440, 1.5, t, .3, TKAN, True))
    s += vinetka(.44)
    return s


# ── 101 ────────────────────────────────────────────────────────────────────
def vecherniy_dom_okno_ryabina_valenki(t):
    """Уютная прихожая и комната вечером одним кадром: на окне загорается
    настольная лампа под абажуром, у входной двери вспыхивает красным ветка
    рябины в вазе, под вешалкой встают рядком три пары валенок — большие,
    средние и крошечные. Кот проходит вдоль валенок."""
    rnd = random.Random(10111)
    s = f'<rect width="{W}" height="{H}" fill="#2b2420"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#6f6052"/>')
    for i in range(10):                  # обои в мелкий цветок — пятнами
        for j in range(7):
            s += SL(Z_DAL, f'<circle cx="{70+i*196:.0f}" cy="{80+j*140:.0f}"'
                           f' r="13" fill="#8a7a64" opacity=".45"/>')
    s += SL(Z_DAL, f'<rect y="860" width="{W}" height="34" fill="#8d7f6e" {o(5)}/>')
    s += SL(Z_DAL, polovicy(894, "#6b4a2a"))
    s += SL(Z_DAL, kvartira_veschi(1520, 300, 380, t, 10113))
    # окно слева с настольной лампой: лампа загорается
    okx, oky, okw, okh = 160, 150, 540, 460
    vid = (f'<rect x="{okx}" y="{oky}" width="{okw}" height="{okh}"'
           f' fill="url(#nnoch)"/>')
    for i in range(18):
        vid += (f'<circle cx="{okx+rnd.random()*okw:.0f}"'
                f' cy="{oky+rnd.random()*okh*.62:.0f}"'
                f' r="{rnd.uniform(1.5,3):.1f}" fill="#cfe4f5"'
                f' opacity="{.4+.5*abs(A.w(t,2.6+i*.2,i*.1)):.2f}"/>')
    for i in range(4):
        bx = okx + 40 + i * 130
        vid += (f'<rect x="{bx:.0f}" y="{oky+okh*.56:.0f}" width="90"'
                f' height="{okh*.44:.0f}" fill="#242c3c" opacity=".92"/>')
        if i % 2 == 0:
            vid += (f'<rect x="{bx+24:.0f}" y="{oky+okh*.62:.0f}" width="36"'
                    f' height="36" fill="{SVET}" opacity=".5"/>')
    s += SL(Z_SRED, okno_izby(okx, oky, okw, okh, t, vid, .18, False, True))
    s += SL(Z_SRED, f'<rect x="{okx-60}" y="{okh+oky+20}" width="{okw+120}"'
                    f' height="36" rx="10" fill="{DOSKA}" {o(6)}/>')
    zazh = A.ease(A.seg(t, .4, .9))
    s += SL(Z_SRED, _lampa_abazhur(okx + 160, okh + oky + 16, t, 2.0, zazh))
    s += SL(Z_SRED, teplo(okx + 160, okh + oky - 190, 940 * zazh + 160,
                          800 * zazh + 160, .56 * zazh + .08))
    s += SL(Z_SRED, _chashka(okx + 400, okh + oky + 18, 1.3, t, .2, KREM, True))
    s += SL(Z_SRED, par(okx + 400, okh + oky - 60, t, 3, .4 * zazh + .1, 160,
                        .4, .8))
    # входная дверь справа и ваза с рябиной у неё
    dx, dy, dw, dh = 1300, 130, 440, 760
    s += SL(Z_SRED, dver(dx, dy, dw, dh, 0.0, "#6b5440", True, True))
    s += SL(Z_SRED, f'<rect x="{dx+dw*.16:.0f}" y="{dy+dh*.08:.0f}"'
                    f' width="{dw*.68:.0f}" height="{dh*.32:.0f}" rx="8"'
                    f' fill="none" stroke="#4a382a" stroke-width="14"/>')
    s += SL(Z_SRED, _podkova_rzh(dx + dw / 2, dy - 110, .95, t))
    vsp = A.ease(A.seg(t, 1.4, 1.0))
    vx_, vy_ = 1250, 890
    s += SL(Z_SRED, f'<rect x="{vx_-130:.0f}" y="{vy_-230:.0f}" width="260"'
                    f' height="230" rx="10" fill="url(#derev)" {o(8)}/>')
    s += SL(Z_SRED, _vaza(vx_, vy_ - 240, 1.15, t, False))
    s += SL(Z_SRED, f'<path d="M{vx_:.0f},{vy_-630:.0f} q-18,-120 -8,-250"'
                    f' fill="none" stroke="#5e4428" stroke-width="16"/>')
    for i in range(4):
        s += SL(Z_SRED, grozd_ryabiny(vx_ + (-1 if i % 2 else 1) * (70 + i * 10),
                                      vy_ - 660 - i * 60, t, 1.5 + .3 * vsp, 18,
                                      10117 + i, i * .2))
    s += SL(Z_SRED, teplo(vx_, vy_ - 700, 520 * vsp, 440 * vsp, .3 * vsp))
    # вешалка и ТРИ ПАРЫ ВАЛЕНОК рядком
    s += SL(Z_SRED, _veshalka(420, 210, 440, t, 4, True))
    for i, (sc, px_) in enumerate(((2.9, 500), (1.7, 830), (.85, 1040))):
        vst = A.out(A.seg(t, 1.0 + i * .34, .6))
        for j, sgn in ((0, -1), (1, 1)):
            s += SL(Z_SRED, _valenok(px_ + sgn * 40 * sc,
                                     1056 + 80 * (1 - vst) + j * 10, sc, t,
                                     .2 + i * .3 + j * .2, True,
                                     ("#c4b091", "#a89878", "#d8c7a6")[i],
                                     sgn * 4))
    s += SL(Z_SRED, f'<rect x="300" y="1050" width="880" height="28" rx="10"'
                    f' fill="{TKAN2}" opacity=".75" {o(4)}/>')
    # кот проходит вдоль валенок
    hod = A.ease(A.seg(t, 1.8, 2.2))
    s += SL(Z_SRED, kot(640 + hod * 620, 1066, t, 1.35, "#3b3430", False))
    s += SL(Z_PERED, zanaveska(120, 90, 300, 150, TKAN, t, 1))
    s += SL(Z_PERED, zanaveska(760, 90, 300, 150, TKAN, t, -1))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="60" height="1080" fill="#241d18"'
                     f' opacity=".88"/>')
    s += vinetka(.42)
    return s


# ── 102 ────────────────────────────────────────────────────────────────────
def chaynik_na_svoem_ogne(t):
    """Кухонная плита: под пузатым чайником на пол-кадра горит синий венчик
    газа, чайник пускает пар. Вокруг плиты за столом собирается семья с
    чашками, хозяйка возвращается к столу."""
    rnd = random.Random(10213)
    s = f'<rect width="{W}" height="{H}" fill="#2a2622"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#79706a"/>')
    for i in range(9):                   # кафель над плитой
        for j in range(4):
            s += SL(Z_DAL, f'<rect x="{30+i*212:.0f}" y="{60+j*150:.0f}"'
                           f' width="190" height="128" rx="6" fill="#8d8780"'
                           f' opacity=".55" {o(3)}/>')
    s += SL(Z_DAL, polovicy(900, "#6b5a4a"))
    s += SL(Z_DAL, kvartira_veschi(1600, 200, 320, t, 10219))
    s += SL(Z_SRED, tusklaya_lampochka(1180, 100, t, 1.4, True))
    # ПЛИТА и ЧАЙНИК — главный предмет слева-центре
    plx, ply, plw = 540, 900, 700
    pl = (f'<rect x="{plx-plw/2:.0f}" y="{ply-320:.0f}" width="{plw:.0f}"'
          f' height="320" rx="14" fill="#cfd2d4" {o(9)}/>')
    pl += (f'<rect x="{plx-plw/2+14:.0f}" y="{ply-300:.0f}" width="{plw-28:.0f}"'
           f' height="120" rx="10" fill="#9aa1a8" opacity=".6"/>')
    pl += (f'<rect x="{plx-plw/2:.0f}" y="{ply-360:.0f}" width="{plw:.0f}"'
           f' height="54" rx="12" fill="#5d6168" {o(7)}/>')
    for i in range(4):                   # ручки-краны плиты
        pl += (f'<circle cx="{plx-plw/2+90+i*(plw-180)/3:.0f}" cy="{ply-200:.0f}"'
               f' r="26" fill="#3f454a" {o(5)}/>')
        ang = -40 + i * 26 + 8 * A.w(t, 2.4, i * .2)
        pl += (f'<line x1="{plx-plw/2+90+i*(plw-180)/3:.0f}" y1="{ply-200:.0f}"'
               f' x2="{plx-plw/2+90+i*(plw-180)/3+math.cos(math.radians(ang))*22:.0f}"'
               f' y2="{ply-200+math.sin(math.radians(ang))*22:.0f}"'
               f' stroke="#e8eef6" stroke-width="7"/>')
    pl += (f'<rect x="{plx-plw/2+40:.0f}" y="{ply-160:.0f}" width="{plw-80:.0f}"'
           f' height="130" rx="10" fill="#3a3f46" {o(6)}/>')
    pl += (f'<rect x="{plx-plw/2+60:.0f}" y="{ply-140:.0f}" width="{plw-120:.0f}"'
           f' height="90" rx="8" fill="#8a5a2a" opacity=".45"/>')
    s += SL(Z_SRED, pl)
    # синий венчик огня под чайником
    gx_, gy_ = plx - 120, ply - 362
    s += SL(Z_SRED, f'<circle cx="{gx_:.0f}" cy="{gy_:.0f}" r="92" fill="#3a3f46"'
                    f' {o(6)}/>')
    s += SL(Z_SRED, f'<circle cx="{gx_:.0f}" cy="{gy_:.0f}" r="56" fill="#23262a"'
                    f' {o(4)}/>')
    for i in range(16):                  # венчик: синие язычки по кругу
        a = i * .3927
        hh = 34 + 14 * abs(A.w(t, .5, i * .11))
        s += SL(Z_SRED, f'<path d="M{gx_+math.cos(a)*58:.0f},'
                        f'{gy_+math.sin(a)*58*.4:.0f}'
                        f' q{math.cos(a)*10:.0f},{-hh*.5:.0f}'
                        f' {math.cos(a)*4:.0f},{-hh:.0f}'
                        f' q{-math.cos(a)*14:.0f},{hh*.5:.0f}'
                        f' {-math.cos(a)*14:.0f},{hh:.0f} Z" fill="#4aa3e0"'
                        f' opacity=".85"/>')
        s += SL(Z_SRED, f'<path d="M{gx_+math.cos(a)*58:.0f},'
                        f'{gy_+math.sin(a)*58*.4:.0f}'
                        f' q{math.cos(a)*6:.0f},{-hh*.3:.0f}'
                        f' {math.cos(a)*2:.0f},{-hh*.52:.0f}" fill="none"'
                        f' stroke="#d8f0ff" stroke-width="6" opacity=".7"/>')
    s += SL(Z_SRED, ogon(gx_, gy_ + 6, t, .5, .2, 4, "#5aa0e0"))
    s += SL(Z_SRED, f'<ellipse cx="{gx_:.0f}" cy="{gy_:.0f}" rx="150" ry="70"'
                    f' fill="#4aa3e0" opacity="{.16+.07*abs(A.w(t,1.4)):.2f}"/>')
    s += SL(Z_SRED, teplo(gx_, gy_ - 60, 640, 520, .34 + .1 * abs(A.w(t, 1.5))))
    for i in range(6):                   # решётка горелки: чайник стоит ВЫШЕ огня
        a = i * 1.047
        s += SL(Z_SRED, f'<line x1="{gx_+math.cos(a)*30:.0f}"'
                        f' y1="{gy_+math.sin(a)*12-66:.0f}"'
                        f' x2="{gx_+math.cos(a)*104:.0f}"'
                        f' y2="{gy_+math.sin(a)*40-66:.0f}" stroke="#4a4f55"'
                        f' stroke-width="13" stroke-linecap="round"/>')
    s += SL(Z_SRED, _chaynik(gx_, gy_ - 76, 2.3, t, True, "url(#zhel)"))
    s += SL(Z_SRED, par(gx_ + 170, gy_ - 380, t, 6, .6, 320, .45, 1.4))
    s += SL(Z_SRED, par(gx_ - 20, gy_ - 400, t, 4, .45, 260, .4, 1.1))
    # стол справа, семья собирается с чашками
    s += SL(Z_SRED, stol(1240, 820, 660, 44, True))
    for i, (cx_, ph_) in enumerate(((1330, .1), (1480, .4), (1630, .7),
                                    (1770, .95))):
        pri = A.out(A.seg(t, .6 + i * .34, .7))
        s += SL(Z_SRED, _chashka(cx_, 820 - 50 * pri + 50, 1.35, t, ph_, KREM,
                                 True))
        s += SL(Z_SRED, par(cx_, 760, t, 3, .4 * pri, 160, .4, .8))
    s += SL(Z_SRED, karavay(1200, 816, 1.0, True))
    for i, (fx_, h_, col, pl_, bo) in enumerate((
            (1340, 480, "#3a3346", False, True),
            (1560, 440, "#2e4a5a", True, False),
            (1780, 350, "#6b3a44", False, False))):
        sbor = A.ease(A.seg(t, .4 + i * .4, 1.2))
        s += SL(Z_SRED, figura(fx_ + (1 - sbor) * (120 - i * 40), 1060, h_, t,
                               col, "#ffd98a", pl_, .2 * i, True, 1.0, False,
                               1.0, bo))
    # хозяйка возвращается к столу от плиты
    vozv = A.ease(A.seg(t, 1.2, 1.6))
    hx = 820 + vozv * 260
    s += SL(Z_SRED, figura(hx, 1070, 540, t, "#4a2f3a", "#ffd98a", True, .3,
                           True, 1.0, False, 1.4))
    ruk, (kx, ky) = rukav(hx + 90, 760, 160, -34, t, "#4a2f3a", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, _chashka(kx + 30, ky + 20, 1.1, t, .5, KREM, False))
    s += SL(Z_SRED, kot(300, 1012, t, 1.3, "#4a4440", False))
    s += SL(Z_SRED, _chugunok(260, 560, 1.1, t, False))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="70" height="1080" fill="#201c18"'
                     f' opacity=".88"/>')
    s += SL(Z_PERED, _banka_krupy(1760, 1012, 1.5, t))
    s += vinetka(.42)
    return s


# источники света сцен: сюда ставится блик в объектив (C16/K17)
BLIKI = {
    "babushka_i_shapka_na_kryuchke": (960, 150),
    "babushka_zaslonyaet_dver": (640, 120),
    "babushkina_dver_s_sekretami": (300, 110),
    "bolshoe_okno_s_lavkoy": (40, 660),
    "botinki_s_gazetoy_i_kremom": (700, 120),
    "chaynik_na_svoem_ogne": (1180, 100),
    "chelka_pered_zerkalom": (1600, 390),
    "chuzhaya_shal_i_chuzhaya_drel": (260, 640),
    "chuzhoy_gorshok_s_neudachami": (1420, 620),
    "ded_chitaet_nebo": (350, 700),
    "ded_pletet_vozhzhi": (1830, 700),
    "devochka_vybegaet_za_dver": (1330, 760),
    "dve_podrugi_na_kinoprobah": (960, 120),
    "dvoe_na_ulice_primorskogo_goroda": (1760, 780),
    "dym_stolbom_i_karavay": (1705, 716),
    "fonarik_v_yaschike_komoda": (1780, 180),
    "gorodskoe_okno_s_chashkoy": (960, 70),
    "gorshok_s_uglyami_na_shestke": (1460, 620),
    "gruzovik_u_podezda": (1060, 400),
    "hodiki_i_rannyaya_temnota": (900, 700),
    "holodnaya_pech_utrom": (520, 668),
    "imya_letit_v_russkuyu_izbu": (1300, 700),
    "kosa_do_poyasa": (260, 760),
    "luchina_v_svetce": (1544, 790),
    "mokryy_sneg_na_stekle": (170, 120),
    "odeyalo_i_noski_nagotove": (1000, 540),
    "okolica_v_noyabrskih_sumerkah": (420, 1010),
    "ovechi_nozhnicy_na_gvozde": (1660, 760),
    "parizhskaya_ulica_s_gruzovichkom": (211, 400),
    "pleten_i_temnye_gosti": (1560, 690),
    "pochtovye_yaschiki_i_larek": (520, 110),
    "porog_cherta": (430, 700),
    "porog_svoe_i_chuzhoe": (964, 640),
    "pyat_podkov_nad_dveryu": (330, 760),
    "ryabinovye_busy_na_nitke": (1490, 400),
    "rynochnaya_ploschad_slushaet": (1480, 700),
    "seyatel_i_risovannyy_veter": (1860, 230),
    "silach_posle_strizhki": (1660, 790),
    "sosed_s_pustym_gorshkom": (640, 560),
    "sosed_u_dveri_zaglyanite_zavtra": (1000, 980),
    "stremyanka_kniga_i_forma_dlya_piro": (420, 120),
    "strizhka_posredi_kuhni": (300, 90),
    "tri_afishi_na_stene_kluba": (1760, 200),
    "tulup_s_gvozdya_i_chemodan_s_zimni": (1440, 150),
    "uchitel_i_dva_uchenika_pod_kolonna": (300, 980),
    "ugovory_i_ugrozy": (260, 740),
    "valenki_shkaf_i_varezhki_na_rezink": (960, 130),
    "valenok_nad_porogom": (560, 420),
    "zhena_derzhit_muzha_za_kushak": (1570, 790),
}
