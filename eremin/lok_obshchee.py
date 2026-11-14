# -*- coding: utf-8 -*-
"""СКВОЗНЫЕ ОБРАЗЫ РОЛИКА «17 ноября — Ерёмин день».

День поздней осени: земля голая, первый мокрый снег, сизые сумерки, рано
темнеет. Холод снаружи — тепло внутри, тёплое пятно в кадре всегда одно.
Эти кирпичики общие для всех 102 декораций ролика и живут отдельно от
`baza.py`, чтобы сцены не повторяли друг друга кодом.
"""
import math, random
from baza import *
import anim as A


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
