# -*- coding: utf-8 -*-
"""100 декораций ролика «Что дарить на Новый год 2027».

Каждая — функция времени f(t) -> svg. Все нарисованы ЗАНОВО под этот текст
(R-0019): ни один кадр не взят у прошлых роликов проекта 2027.
Его правила 15.11 (вечерняя редакция): настоящий кадр лежит ВНУТРИ сцены (метка mesto_stoka),
сцены не пустые, предметы узнаваемые, в каждой сцене живой огонёк.

СОБИРАЕТСЯ sobrat_lok.py из частей — руками этот файл не правят.
"""
import math, random
from baza import *
import anim as A

# ═══ из lok_obshchee.py ═══
_RUKI = []        # точки крепления внешних рук, набираются первым проходом
_SOBRANO = None   # готовый список для второго прохода (None = проход первый)
_NICH = []        # руки, объявленные ничьими (крупный план кистей)
_FIGURY = []      # (x, плечо, погашено, ширина, рост) — для гейта
_PRIKLEENO = []   # какие внешние руки сели на плечо фигуры — для гейта


def ruki_sbros():
    """Начать первый проход: забыть прежние руки."""
    global _RUKI, _SOBRANO
    _RUKI, _SOBRANO = [], None
    del _FIGURY[:], _PRIKLEENO[:], _NICH[:]


def ruki_gotovo():
    """Закрыть первый проход: со следующего вызова figura прячет рукава."""
    global _SOBRANO
    _SOBRANO = list(_RUKI)
    del _FIGURY[:], _PRIKLEENO[:]     # фигуры первого прохода не считаем


def ruki_spisok():
    """Что собрано первым проходом (для гейта anatomiya.py)."""
    return list(_RUKI)


def anatomiya_svodka():
    """Для гейта: фигуры, внешние руки и руки, не севшие ни на одно плечо.

    Сирота ДЕЛИТСЯ НАДВОЕ, и это важно:
    · «на фигуре» — рука растёт из туловища мимо плеча. Это и есть третья
      рука (R-0051), сборка с такой рукой не идёт;
    · «вне фигур» — крупный план кистей там, где человека в кадре нет
      (руки держат шапку, тянут ухват). Это норма, только отчёт.
    """
    siroty = [r for r in _RUKI if r not in _PRIKLEENO]
    na_figure = []
    for hx, hy in siroty:
        for fx, fpl, _p, w_, h_ in _FIGURY:
            if abs(hx - fx) <= w_ * .70 and -h_ * .10 <= hy - fpl <= h_ * .62:
                na_figure.append((hx, hy, fx, fpl))
                break
    return {"figur": len(_FIGURY), "ruk": len(_RUKI), "nichih": len(_NICH),
            "pogasheno": sum(f[2] for f in _FIGURY), "siroty": siroty,
            "na_figure": na_figure,
            "bez_svoih": [f for f in _FIGURY if f[2] >= 2]}


def scena(fn, t):
    """Собрать сцену в два прохода — иначе у фигуры вырастает третья рука."""
    ruki_sbros()
    fn(t)
    ruki_gotovo()
    out = fn(t)
    global _SOBRANO
    _SOBRANO = None
    return out


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
    # рукава вдоль тела, живые. Рукав НЕ рисуется на том плече, откуда сцена
    # уже вывела свою руку через rukav(): иначе у человека три руки (R-0051).
    _pog = 0
    for i in (-1, 1):
        rx = x + i * w_ * .40
        sel = [(hx, hy) for hx, hy in (_SOBRANO or ())
               if abs(hx - rx) <= w_ * .80 and abs(hy - (plech + h_ * .02)) <= h_ * .30]
        if sel:
            _pog += 1
            for r in sel:
                if r not in _PRIKLEENO:
                    _PRIKLEENO.append(r)
            continue
        a = i * (12 + 5 * A.w(t, 1.9, ph + (0 if i < 0 else .4)))
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
    _FIGURY.append((round(x, 1), round(plech, 1), _pog, round(w_, 1), round(h_, 1)))
    return s + '</g>'


def rukav(x, y, dl, ug, t, col="#2a2430", kant="#cfe4f5", ph=.0, amp=7.0,
          nichya=False):
    """Рукав без кисти: правило проекта — рук в кадре не рисуем, работает
    сам предмет. Рукав ходит, предмет на его конце двигают отдельно.

    nichya=True — рука НИЧЬЯ: крупный план кистей, человека в кадре нет
    (руки держат шапку, хлопают в ладоши мимо моли). Такая рука не гасит
    рукав соседней фигуры и не считается третьей рукой в гейте anatomiya.py.
    """
    a = math.radians(ug + amp * A.w(t, .9, ph))
    x2, y2 = x + dl * math.cos(a), y + dl * math.sin(a)
    if _SOBRANO is None:                # первый проход: запомнили плечо
        (_NICH if nichya else _RUKI).append((x, y))
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
IMP = "#5c2a4a"


# ───────────────────────── МЕСТНЫЕ КИРПИЧИКИ ПОРЦИИ ─────────────────────────
def _korobka(x, y, w_, h_, t, col=None, lenta=None, bant=True, otkryta=0.0, ph=0.0):
    """Подарочная коробка: крышка приоткрывается на otkryta (0..1)."""
    col = col or TKAN2
    lenta = lenta or ZOL
    kach = 2.0 * A.w(t, 2.4, ph)
    kr = h_ * (0.22 + 0.5 * otkryta)
    s = ten(x + w_ * .5, y + h_ + 10, w_ * .5, 12, .4)
    s += (f'<rect x="{x:.0f}" y="{y+kr:.0f}" width="{w_:.0f}" height="{h_-kr:.0f}" rx="8"'
          f' fill="{col}" {o(6)}/>')
    s += (f'<rect x="{x-4:.0f}" y="{y+kr:.0f}" width="{w_+8:.0f}" height="{(h_-kr)*.46:.0f}"'
          f' fill="{lenta}" opacity=".85"/>')
    s += (f'<rect x="{x+w_*.42:.0f}" y="{y+kr:.0f}" width="{w_*.16:.0f}" height="{h_-kr:.0f}"'
          f' fill="{lenta}" opacity=".85"/>')
    s += f'<g transform="rotate({-16*otkryta:.1f} {x:.0f} {y+kr:.0f})">'
    s += f'<rect x="{x-8:.0f}" y="{y:.0f}" width="{w_+16:.0f}" height="{kr+6:.0f}" rx="8" fill="{col}" {o(6)}/>'
    s += (f'<rect x="{x+w_*.42:.0f}" y="{y:.0f}" width="{w_*.16:.0f}" height="{kr+6:.0f}"'
          f' fill="{lenta}" opacity=".85"/>')
    if bant:
        bx, by = x + w_ * .5, y + kr * .3 + kach
        s += (f'<path d="M{bx:.0f},{by:.0f} q{-w_*.22:.0f},{-h_*.14:.0f} {-w_*.03:.0f},{-h_*.26:.0f}'
              f' q{w_*.12:.0f},{-h_*.02:.0f} {w_*.03:.0f},{h_*.1:.0f} q{w_*.02:.0f},{-h_*.1:.0f}'
              f' {w_*.24:.0f},{h_*.18:.0f} Z" fill="{lenta}" {o(4)}/>')
        s += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{w_*.07:.0f}" fill="{lenta}" {o(3)}/>'
    return s + '</g>'


def _svertok(x, y, s_, t, col=None, lenta=None, ph=0.0):
    """Мелкий свёрток-кулёк: ткнутый сверху узел, маленький бант."""
    col = col or RUSH
    lenta = lenta or TKAN
    bob = 3 * A.w(t, 1.8, ph)
    s = ten(x, y + 14 * s_, 38 * s_, 9 * s_, .35)
    s += (f'<path d="M{x-40*s_:.0f},{y+bob:.0f} q-4,{-56*s_:.0f} 40,{-60*s_:.0f}'
          f' q44,4 40,{60*s_:.0f} q-40,{14*s_:.0f} -80,0 Z" fill="{col}" {o(5)}/>')
    s += (f'<path d="M{x-28*s_:.0f},{y-20*s_+bob:.0f} q28,{-34*s_:.0f} 56,0" fill="none"'
          f' stroke="{lenta}" stroke-width="{7*s_:.0f}"/>')
    s += f'<circle cx="{x:.0f}" cy="{y-46*s_+bob:.0f}" r="{9*s_:.0f}" fill="{lenta}" {o(3)}/>'
    return s


def _varezhka(x, y, s_, ang, col=None, uzor=None):
    col = col or TKAN
    uzor = uzor or SVET
    s = f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x-24*s_:.0f},{y:.0f} q-6,{-56*s_:.0f} 26,{-62*s_:.0f}'
          f' q30,6 26,{62*s_:.0f} q-26,{14*s_:.0f} -52,0 Z" fill="{col}" {o(5)}/>')
    s += (f'<path d="M{x-24*s_:.0f},{y-10*s_:.0f} q-22,{-4*s_:.0f} -22,{-26*s_:.0f}'
          f' q0,{-14*s_:.0f} 20,{-14*s_:.0f} q6,{20*s_:.0f} 2,{40*s_:.0f} Z" fill="{col}" {o(4)}/>')
    s += (f'<path d="M{x-20*s_:.0f},{y-58*s_:.0f} q20,{-10*s_:.0f} 40,0" fill="none"'
          f' stroke="{uzor}" stroke-width="{4*s_:.0f}" opacity=".7"/>')
    return s + '</g>'


def _banka(x, y, s_, col=MED, tkan=None):
    tkan = tkan or TKAN
    s = ten(x, y + 6 * s_, 36 * s_, 9 * s_, .4)
    s += (f'<path d="M{x-34*s_:.0f},{y:.0f} v{-78*s_:.0f} q0,-10 10,-10 h{48*s_:.0f}'
          f' q10,0 10,10 v{78*s_:.0f} Z" fill="url(#{"med" if col==MED else "glina"})" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-92*s_:.0f}" rx="{30*s_:.0f}" ry="{10*s_:.0f}"'
          f' fill="{tkan}" {o(4)}/>')
    s += (f'<path d="M{x-28*s_:.0f},{y-92*s_:.0f} q28,{14*s_:.0f} 56,0" fill="none"'
          f' stroke="{tkan}" stroke-width="{5*s_:.0f}" opacity=".7"/>')
    return s


def _svistulka(x, y, s_, ang=0.0, col=None):
    """Глиняная свистулька-птичка: тело, хвост веером, клюв, дырочка."""
    col = col or KRAS
    s = f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{44*s_:.0f}" ry="{30*s_:.0f}" fill="{col}" {o(4)}/>'
    s += (f'<path d="M{x+34*s_:.0f},{y-4*s_:.0f} l{24*s_:.0f},{-14*s_:.0f} l{-2*s_:.0f},{18*s_:.0f}'
          f' l{-2*s_:.0f},{18*s_:.0f} Z" fill="{col}" {o(3)}/>')
    s += f'<path d="M{x-40*s_:.0f},{y:.0f} l{-18*s_:.0f},{-8*s_:.0f} l2,{16*s_:.0f} Z" fill="{ZOL}" {o(2)}/>'
    s += f'<circle cx="{x-6*s_:.0f}" cy="{y-8*s_:.0f}" r="{3*s_:.0f}" fill="{K}"/>'
    s += f'<circle cx="{x+10*s_:.0f}" cy="{y+8*s_:.0f}" r="{4*s_:.0f}" fill="#1a1410"/>'
    return s + '</g>'


def _oblachko(x, y, s_, t, ph, kind):
    rise = 10 * A.ease(A.seg(t, ph, 1.0)) % 10
    bob = 6 * A.w(t, 1.6, ph)
    s = (f'<ellipse cx="{x:.0f}" cy="{y+bob:.0f}" rx="{70*s_:.0f}" ry="{46*s_:.0f}"'
         f' fill="#ffffff" opacity=".92" {o(4)}/>')
    s += (f'<ellipse cx="{x-40*s_:.0f}" cy="{y+16*s_+bob:.0f}" rx="{26*s_:.0f}" ry="{18*s_:.0f}"'
          f' fill="#ffffff" opacity=".92" {o(3)}/>')
    s += (f'<circle cx="{x-54*s_:.0f}" cy="{y+40*s_+bob:.0f}" r="{9*s_:.0f}"'
          f' fill="#ffffff" opacity=".9" {o(2)}/>')
    cy_ = y + bob
    if kind == "serdce":
        s += (f'<path d="M{x:.0f},{cy_+16*s_:.0f} q-30,-30 -30,-50 q0,-18 16,-18 q14,0 14,14'
              f' q0,-14 14,-14 q16,0 16,18 q0,20 -30,50 Z" fill="{KRAS}"/>')
    elif kind == "moneta":
        s += f'<circle cx="{x:.0f}" cy="{cy_:.0f}" r="{22*s_:.0f}" fill="url(#med)" {o(3)}/>'
    elif kind == "ruki":
        s += (f'<ellipse cx="{x-16*s_:.0f}" cy="{cy_:.0f}" rx="{16*s_:.0f}" ry="{10*s_:.0f}"'
              f' fill="#e0b08a" {o(2)}/>')
        s += (f'<ellipse cx="{x+16*s_:.0f}" cy="{cy_:.0f}" rx="{16*s_:.0f}" ry="{10*s_:.0f}"'
              f' fill="#e0b08a" {o(2)}/>')
    elif kind == "doroga":
        s += (f'<path d="M{x-24*s_:.0f},{cy_+16*s_:.0f} L{x:.0f},{cy_-16*s_:.0f}'
              f' L{x+24*s_:.0f},{cy_+16*s_:.0f}" fill="none" stroke="#6f7f8c"'
              f' stroke-width="{8*s_:.0f}" stroke-dasharray="6 6"/>')
    elif kind == "ravno":
        s += (f'<line x1="{x-22*s_:.0f}" y1="{cy_-8*s_:.0f}" x2="{x+22*s_:.0f}" y2="{cy_-8*s_:.0f}"'
              f' stroke="{K}" stroke-width="{6*s_:.0f}"/>')
        s += (f'<line x1="{x-22*s_:.0f}" y1="{cy_+8*s_:.0f}" x2="{x+22*s_:.0f}" y2="{cy_+8*s_:.0f}"'
              f' stroke="{K}" stroke-width="{6*s_:.0f}"/>')
    elif kind == "chasy":
        s += f'<circle cx="{x:.0f}" cy="{cy_:.0f}" r="{22*s_:.0f}" fill="#efe3c8" {o(3)}/>'
        s += (f'<line x1="{x:.0f}" y1="{cy_:.0f}" x2="{x:.0f}" y2="{cy_-14*s_:.0f}" stroke="{K}" stroke-width="3"/>'
              f'<line x1="{x:.0f}" y1="{cy_:.0f}" x2="{x+10*s_:.0f}" y2="{cy_:.0f}" stroke="{K}" stroke-width="3"/>')
    return s


def _chasy_sten(x, y, s_, t, col=None):
    """Настенные/настольные часы: циферблат, две стрелки, деления без цифр."""
    col = col or KREM
    a_min = (t * 11) % 360
    a_hr = (t * .9) % 360
    s = ten(x, y + 60 * s_, 46 * s_, 10 * s_, .4)
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{52*s_:.0f}" fill="url(#derev)" {o(6)}/>'
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{40*s_:.0f}" fill="{col}" {o(4)}/>'
    for i in range(12):
        a = math.radians(i * 30)
        x1, y1 = x + math.sin(a) * 34 * s_, y - math.cos(a) * 34 * s_
        x2, y2 = x + math.sin(a) * 40 * s_, y - math.cos(a) * 40 * s_
        s += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{K}" stroke-width="2.4"/>'
    s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.sin(math.radians(a_hr))*20*s_:.0f}"'
          f' y2="{y-math.cos(math.radians(a_hr))*20*s_:.0f}" stroke="{K}" stroke-width="4" stroke-linecap="round"/>')
    s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.sin(math.radians(a_min))*30*s_:.0f}"'
          f' y2="{y-math.cos(math.radians(a_min))*30*s_:.0f}" stroke="{K}" stroke-width="3" stroke-linecap="round"/>')
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{4*s_:.0f}" fill="{K}"/>'
    return s


def _chasy_karman(x, y, s_, t, otkryt=1.0):
    a_min = (t * 24) % 360
    s = f'<g transform="rotate({6*A.w(t,2.1):.1f} {x:.0f} {y:.0f})">'
    s += f'<path d="M{x:.0f},{y-56*s_:.0f} q22,-14 22,{14*s_:.0f}" fill="none" stroke="url(#zhel)" stroke-width="{5*s_:.0f}"/>'
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{48*s_:.0f}" fill="url(#zol)" {o(6)}/>'
    if otkryt > .2:
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{36*s_:.0f}" fill="{KREM}" {o(4)}/>'
        for i in range(12):
            a = math.radians(i * 60)
            s += (f'<line x1="{x+math.sin(a)*30*s_:.0f}" y1="{y-math.cos(a)*30*s_:.0f}"'
                  f' x2="{x+math.sin(a)*34*s_:.0f}" y2="{y-math.cos(a)*34*s_:.0f}" stroke="{K}" stroke-width="2"/>')
        s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.sin(math.radians(a_min))*24*s_:.0f}"'
              f' y2="{y-math.cos(math.radians(a_min))*24*s_:.0f}" stroke="{K}" stroke-width="3"/>')
    return s + '</g>'


def _servant(x, y, w_, h_, t, col=None):
    """Полированный сервант с хрусталём за стеклом — крупный объект от 600 px."""
    col = col or "#6b4428"
    s = ten(x + w_ * .5, y + h_ + 14, w_ * .5, 18, .5)
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="url(#derev)" {o(7)}/>'
    s += (f'<rect x="{x+w_*.08:.0f}" y="{y+h_*.06:.0f}" width="{w_*.84:.0f}" height="{h_*.42:.0f}"'
          f' rx="8" fill="url(#stekl)" opacity=".7" {o(5)}/>')
    rnd = random.Random(int(x) + int(y))
    for i in range(7):
        hx = x + w_ * .14 + rnd.random() * w_ * .7
        hy = y + h_ * .12 + rnd.random() * h_ * .3
        bl = .4 + .6 * abs(A.w(t, 1.7 + i * .2, i * .15))
        s += (f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="{10+rnd.random()*7:.0f}"'
              f' ry="{14+rnd.random()*8:.0f}" fill="#eaf4ff" opacity="{bl:.2f}"/>')
    s += (f'<rect x="{x+w_*.08:.0f}" y="{y+h_*.54:.0f}" width="{w_*.84:.0f}" height="{h_*.36:.0f}"'
          f' rx="6" fill="{col}" {o(5)}/>')
    for i in range(3):
        s += (f'<circle cx="{x+w_*.2+i*w_*.3:.0f}" cy="{y+h_*.72:.0f}" r="7" fill="url(#zol)" {o(2)}/>')
    return s


def _shkaf_proem(x, y, w_, h_, t, pw, ph_, vid):
    """Шкаф/полка с проёмом под настоящий кадр — объём от 600 px."""
    s = ten(x + w_ * .5, y + h_ + 14, w_ * .5, 16, .5)
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8" fill="url(#derev)" {o(7)}/>'
    px, py = x + (w_ - pw) / 2, y + (h_ - ph_) / 2
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += f'<path d="{put}" fill="#1a140e"/>' + vid
    s += mesto_stoka(px, py, pw, ph_, "pryam")
    s += f'<path d="{put}" fill="none" {o(8)}/>'
    return s, (px, py, pw, ph_)


def _zapret(x, y, r_, t, ph=0.0):
    puls = .8 + .2 * abs(A.w(t, 1.4, ph))
    s = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_:.0f}" fill="none" stroke="{KRAS}" stroke-width="{14*puls:.0f}" opacity=".9"/>'
    a = math.radians(40)
    s += (f'<line x1="{x-r_*.8*math.cos(a):.0f}" y1="{y-r_*.8*math.sin(a):.0f}"'
          f' x2="{x+r_*.8*math.cos(a):.0f}" y2="{y+r_*.8*math.sin(a):.0f}"'
          f' stroke="{KRAS}" stroke-width="{14*puls:.0f}" opacity=".9" stroke-linecap="round"/>')
    return s


def _galochka(x, y, s_, t, ph=0.0):
    puls = .7 + .3 * abs(A.w(t, 1.8, ph))
    s = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{30*s_:.0f}" fill="{ZEL2}" opacity="{puls:.2f}" {o(3)}/>'
    s += (f'<path d="M{x-14*s_:.0f},{y:.0f} l{8*s_:.0f},{10*s_:.0f} l{18*s_:.0f},{-20*s_:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{6*s_:.0f}" stroke-linecap="round" stroke-linejoin="round"/>')
    return s


def _koshelek(x, y, s_, otkryt=True, n_monet=0, moly=False, t=0.0):
    s = ten(x, y + 20 * s_, 56 * s_, 10 * s_, .35)
    s += (f'<path d="M{x-54*s_:.0f},{y:.0f} q-6,{-50*s_:.0f} 54,{-50*s_:.0f}'
          f' q60,0 54,{50*s_:.0f} q-54,{16*s_:.0f} -108,0 Z" fill="#5a3a26" {o(5)}/>')
    if otkryt:
        s += (f'<path d="M{x-48*s_:.0f},{y-6*s_:.0f} q48,{-38*s_:.0f} 96,0" fill="none"'
              f' stroke="#2e1d12" stroke-width="{6*s_:.0f}"/>')
        for i in range(n_monet):
            s += (f'<circle cx="{x-20*s_+i*18*s_:.0f}" cy="{y-20*s_:.0f}" r="{11*s_:.0f}"'
                  f' fill="url(#med)" {o(2)}/>')
        if moly:
            fl = 8 * A.w(t, 2.3)
            s += (f'<ellipse cx="{x+30*s_+fl:.0f}" cy="{y-40*s_-abs(fl):.0f}" rx="{10*s_:.0f}" ry="{6*s_:.0f}"'
                  f' fill="#9a8a78" opacity=".7"/>')
    return s


def _elka(x, y, h_, t, seed=3, ogonki=True):
    """Ёлка с гирляндой — один путь силуэта держит крупный габарит."""
    rnd = random.Random(seed)
    sway = 1.6 * A.w(t, 3.2, seed * .1)
    s = f'<g transform="rotate({sway:.2f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x:.0f},{y-h_:.0f} l{h_*.34:.0f},{h_*.46:.0f} l{-h_*.12:.0f},0'
          f' l{h_*.3:.0f},{h_*.4:.0f} l{-h_*.14:.0f},0 l{h_*.26:.0f},{h_*.3:.0f}'
          f' l{-h_*.76:.0f},0 l{h_*.26:.0f},{-h_*.3:.0f} l{-h_*.14:.0f},0'
          f' l{h_*.3:.0f},{-h_*.4:.0f} l{-h_*.12:.0f},0 Z" fill="{ZEL}" {o(6)}/>')
    s += f'<rect x="{x-10:.0f}" y="{y:.0f}" width="20" height="30" fill="#6b4428" {o(4)}/>'
    for i in range(14):
        yy = y - h_ * (.12 + rnd.random() * .82)
        xx = x + rnd.uniform(-1, 1) * h_ * .28
        col = (KRAS, ZOL, "#4a7fb0")[i % 3]
        s += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="9" fill="{col}" {o(2)}/>'
    if ogonki:
        for i in range(10):
            yy = y - h_ * (.08 + i * .085)
            xx = x + math.sin(i * 1.3) * h_ * .22
            mig = 1.0 if ((t * 1.6 + i * .3) % 1.0) > .18 else .4
            s += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="6" fill="{SVET}" opacity="{mig:.2f}"/>'
    return s + '</g>'


def _napolnenie(x0, y0, w_, h_, t, seed, n=22):
    """Утварь у ОДНОЙ линии опоры (низ полосы x0..x0+w_, y0+h_): книга,
    банка, скрутка холста, рамка, яблоко, пряник — не висят в воздухе и не
    читаются пятном (R-0045, его слово 15.11: вещи узнаются по силуэту)."""
    rnd = random.Random(seed)
    vidy = ("kniga", "jar", "cloth", "frame", "yabloko", "bulka")
    s, posl = "", None
    baza_y = y0 + h_
    for i in range(n):
        v = rnd.choice([x for x in vidy if x != posl])
        posl = v
        cx = x0 + (i + rnd.uniform(.25, .75)) / n * w_
        sc = rnd.uniform(.75, 1.25)
        if v == "kniga":
            ww, hh = rnd.uniform(60, 86) * sc, rnd.uniform(90, 130) * sc
            cy = baza_y - hh
            col = rnd.choice((TKAN, TKAN2, MED, ZEL2, "#6b4428"))
            s += (f'<rect x="{cx-ww/2:.0f}" y="{cy:.0f}" width="{ww:.0f}" height="{hh:.0f}" rx="4"'
                  f' fill="{col}" {o(3)}/>'
                  f'<rect x="{cx-ww/2+6:.0f}" y="{cy+8:.0f}" width="{ww-12:.0f}" height="5"'
                  f' fill="#efe3c8" opacity=".6"/>')
        elif v == "jar":
            s += _banka(cx, baza_y - 6, sc * .82, rnd.choice((MED, "#8c8275")))
        elif v == "cloth":
            ww = rnd.uniform(80, 130) * sc
            col = rnd.choice((RUSH, KREM, TKAN))
            s += (f'<path d="M{cx-ww/2:.0f},{baza_y-36:.0f} q{ww*.5:.0f},{14*sc:.0f} {ww:.0f},0'
                  f' l0,{28*sc:.0f} q{-ww*.5:.0f},{10*sc:.0f} {-ww:.0f},0 Z" fill="{col}" {o(3)}/>')
        elif v == "frame":
            ww, hh = rnd.uniform(70, 96) * sc, rnd.uniform(90, 120) * sc
            cy = baza_y - hh
            s += (f'<rect x="{cx-ww/2:.0f}" y="{cy:.0f}" width="{ww:.0f}" height="{hh:.0f}" rx="4"'
                  f' fill="url(#derev)" {o(4)}/>'
                  f'<rect x="{cx-ww*.36+ww/2:.0f}" y="{cy+hh*.14:.0f}" width="{ww*.72:.0f}" height="{hh*.62:.0f}"'
                  f' fill="#cfd6de" opacity=".55"/>')
        elif v == "yabloko":
            r_ = rnd.uniform(20, 28) * sc
            cy = baza_y - r_
            s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r_:.0f}" fill="{rnd.choice((KRAS,ZOL))}" {o(2)}/>'
                  f'<path d="M{cx:.0f},{cy-r_:.0f} q6,-10 14,-6" fill="none" stroke="{ZEL}" stroke-width="3"/>')
        else:
            rx_, ry_ = rnd.uniform(30, 42) * sc, rnd.uniform(16, 22) * sc
            cy = baza_y - ry_
            s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx_:.0f}" ry="{ry_:.0f}" fill="{KREM}" {o(3)}/>'
                  f'<path d="M{cx-rx_*.4:.0f},{cy:.0f} q{rx_*.4:.0f},-7 {rx_*.8:.0f},0"'
                  f' fill="none" stroke="#c8a876" stroke-width="2" opacity=".6"/>')
    return s


def _sloi_fona(x0, y0, w_, h_, t, seed, n=5):
    """Несколько крупных перекрывающихся плоскостей (панели, драпировка,
    коврик) — поднимает число слоёв в центре кадра без раздувания объёма
    текста мелкими деталями."""
    # ВРЕМЕННО ОТКЛЮЧЕНО вкладкой 15.11: пять случайных полупрозрачных
    # прямоугольников поверх сцены накручивали метрику «слоёв», а в кадре
    # давали мутные цветные плашки поверх предметов. Насыщенность даём
    # настоящими вещами, а не подложками.
    return ""
    rnd = random.Random(seed + 900)
    cols = (TKAN2, "#4a3a2c", ZEL2, MED, "#2e3a4a", KAMEN2, DOSKA2, "#5a3a4a")
    s = ""
    for i in range(n):
        ww = w_ * rnd.uniform(.46, .82)
        hh = h_ * rnd.uniform(.4, .78)
        xx = x0 + rnd.uniform(0, max(1, w_ - ww))
        yy = y0 + rnd.uniform(0, max(1, h_ - hh))
        s += (f'<rect x="{xx:.0f}" y="{yy:.0f}" width="{ww:.0f}" height="{hh:.0f}" rx="14"'
              f' fill="{cols[(seed+i)%len(cols)]}" opacity=".5" {o(2)}/>')
    return s


def _chertenok(x, y, s_, t, ph=0.0):
    """Мелкий чертёнок: тянется к острому, хвост закручен, рожки и уши."""
    tyan = 10 * A.ease(A.seg((t + ph) % 2.4, .1, .6))
    s = f'<g transform="translate({tyan:.0f},0)">'
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{20*s_:.0f}" ry="{26*s_:.0f}" fill="{IMP}" {o(4)}/>'
    s += (f'<path d="M{x-14*s_:.0f},{y+20*s_:.0f} q{-10*s_:.0f},{20*s_:.0f} {2*s_:.0f},{30*s_:.0f}'
          f' q{10*s_:.0f},{-6*s_:.0f} {4*s_:.0f},{-26*s_:.0f} Z" fill="{IMP}" {o(3)}/>')
    for sgn in (-1, 1):
        s += (f'<path d="M{x+sgn*8*s_:.0f},{y-20*s_:.0f} l{sgn*10*s_:.0f},{-16*s_:.0f}'
              f' l{-sgn*4*s_:.0f},{18*s_:.0f} Z" fill="#2e1520" {o(3)}/>')
    s += f'<circle cx="{x-6*s_:.0f}" cy="{y-2*s_:.0f}" r="{3*s_:.0f}" fill="{SVET}"/>'
    s += f'<circle cx="{x+8*s_:.0f}" cy="{y-2*s_:.0f}" r="{3*s_:.0f}" fill="{SVET}"/>'
    return s + '</g>'


def _vesy(x, y, s_, t, nak=0.0, seed=1):
    """Чашечные весы: держат равновесие, но слегка качаются."""
    kach = 3 * A.w(t, 1.6, seed * .2) + nak
    s = f'<rect x="{x-8*s_:.0f}" y="{y-220*s_:.0f}" width="{16*s_:.0f}" height="{220*s_:.0f}" rx="6" fill="url(#zhel)" {o(5)}/>'
    s += f'<ellipse cx="{x:.0f}" cy="{y-220*s_:.0f}" rx="{30*s_:.0f}" ry="{10*s_:.0f}" fill="{ZHELEZ}" {o(4)}/>'
    s += f'<g transform="rotate({kach:.2f} {x:.0f} {y-220*s_:.0f})">'
    s += (f'<line x1="{x-150*s_:.0f}" y1="{y-220*s_:.0f}" x2="{x+150*s_:.0f}" y2="{y-220*s_:.0f}"'
          f' stroke="url(#zhel)" stroke-width="{8*s_:.0f}"/>')
    for sgn in (-1, 1):
        cx_ = x + sgn * 150 * s_
        s += (f'<line x1="{cx_:.0f}" y1="{y-220*s_:.0f}" x2="{cx_-26*s_:.0f}" y2="{y-120*s_:.0f}"'
              f' stroke="{K}" stroke-width="3"/>')
        s += (f'<line x1="{cx_:.0f}" y1="{y-220*s_:.0f}" x2="{cx_+26*s_:.0f}" y2="{y-120*s_:.0f}"'
              f' stroke="{K}" stroke-width="3"/>')
        s += (f'<ellipse cx="{cx_:.0f}" cy="{y-110*s_:.0f}" rx="{46*s_:.0f}" ry="{16*s_:.0f}"'
              f' fill="url(#zhel)" {o(5)}/>')
    s += '</g>'
    return s


def _kovrik_pol(x, y, w_, h_, col1=None, col2=None, seed=1):
    """Половик на полу: бордюр и ряд узорных кружков — настоящая вещь."""
    rnd = random.Random(seed)
    col1 = col1 or TKAN
    col2 = col2 or KREM
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="{col1}" {o(5)}/>'
    s += (f'<rect x="{x+16:.0f}" y="{y+16:.0f}" width="{w_-32:.0f}" height="{h_-32:.0f}"'
          f' fill="none" stroke="{col2}" stroke-width="6" opacity=".7"/>')
    n = max(2, int(w_ / 90))
    for i in range(n):
        s += (f'<circle cx="{x+50+i*(w_-100)/max(1,n-1):.0f}" cy="{y+h_*.5:.0f}" r="12"'
              f' fill="{col2}" opacity=".6"/>')
    return s


def _kartiny_ryad(x, y, n=3, seed=1, w_=110, h_=150):
    """Ряд рамок на стене: рама, паспарту и пятно рисунка — не пустая стена."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        fx = x + i * (w_ + 50)
        s += f'<rect x="{fx:.0f}" y="{y:.0f}" width="{w_}" height="{h_}" rx="4" fill="url(#derev)" {o(4)}/>'
        s += (f'<rect x="{fx+14:.0f}" y="{y+14:.0f}" width="{w_-28}" height="{h_-28}"'
              f' fill="{rnd.choice((KREM,"#cfd6de",TKAN2))}" opacity=".85"/>')
    return s


def _oboi_fon(col1=None, col2=None, n=14):
    """Оклеенная стена городской комнаты — отличает её от сруба избы."""
    col1 = col1 or "#5a4a5a"
    col2 = col2 or "#4a3a4a"
    s = f'<rect width="{W}" height="780" fill="{col1}"/>'
    for i in range(n):
        xx = i * (W / n)
        s += f'<rect x="{xx:.0f}" y="0" width="{W/n*.5:.0f}" height="780" fill="{col2}" opacity=".4"/>'
    s += f'<rect y="760" width="{W}" height="26" fill="#2a2420" {o(4)}/>'
    return s


def _nozh_bolshoy(x, y, h_, t, ang=0.0, col=None):
    """Большой нож: лезвие и рукоять ОДНИМ силуэтом (острие сверху, у
    острия чуть колышется), заклёпки на рукояти, блик по лезвию."""
    col = col or ZHELEZ
    w_ = h_ * .24
    sway = 2 * A.w(t, 1.6) + ang
    s = f'<g transform="rotate({sway:.1f} {x:.0f} {y:.0f})">'
    s += ten(x, y + h_ * .04, w_ * 1.6, 14, .4)
    s += (f'<path d="M{x:.0f},{y-h_:.0f} L{x+w_*.9:.0f},{y-h_*.42:.0f}'
          f' L{x+w_*.5:.0f},{y-h_*.2:.0f} L{x+w_*.5:.0f},{y:.0f}'
          f' L{x-w_*.5:.0f},{y:.0f} L{x-w_*.5:.0f},{y-h_*.2:.0f}'
          f' L{x-w_*.9:.0f},{y-h_*.4:.0f} Z" fill="{col}" {o(6)}/>')
    s += (f'<rect x="{x-w_*.42:.0f}" y="{y-h_*.2:.0f}" width="{w_*.84:.0f}" height="{h_*.2:.0f}"'
          f' rx="8" fill="#5a3a26" {o(5)}/>')
    for i in range(3):
        s += f'<circle cx="{x:.0f}" cy="{y-h_*.16+i*h_*.06:.0f}" r="{w_*.08:.0f}" fill="{K}"/>'
    s += (f'<path d="M{x-w_*.28:.0f},{y-h_*.9:.0f} L{x-w_*.06:.0f},{y-h_*.28:.0f}"'
          f' stroke="#eef4fa" stroke-width="{max(3,w_*.05):.0f}" opacity=".55" stroke-linecap="round"/>')
    return s + '</g>'


def _nozhnicy_bolshie(x, y, h_, t, ang=0.0):
    """Большие портновские ножницы: два лезвия и колечки одним крестом,
    заклёпка-винт в середине."""
    sway = 3 * A.w(t, 1.4) + ang
    s = f'<g transform="rotate({sway:.1f} {x:.0f} {y:.0f})">'
    s += ten(x, y + h_ * .42, h_ * .32, 16, .4)
    for sgn in (-1, 1):
        s += (f'<path d="M{x:.0f},{y-h_:.0f} L{x+sgn*h_*.16:.0f},{y-h_*.08:.0f}'
              f' L{x+sgn*h_*.3:.0f},{y+h_*.3:.0f} Q{x+sgn*h_*.3:.0f},{y+h_*.42:.0f}'
              f' {x+sgn*h_*.18:.0f},{y+h_*.42:.0f} Q{x+sgn*h_*.08:.0f},{y+h_*.42:.0f}'
              f' {x+sgn*h_*.08:.0f},{y+h_*.3:.0f} Z" fill="{ZHELEZ}" {o(5)}/>')
    s += f'<circle cx="{x:.0f}" cy="{y-h_*.08:.0f}" r="{h_*.05:.0f}" fill="{K}"/>'
    s += f'<circle cx="{x:.0f}" cy="{y-h_*.08:.0f}" r="{h_*.02:.0f}" fill="{SVET}" opacity=".7"/>'
    return s + '</g>'


def _veshalka_seni(x, y, w_, t, seed=1, kant=None):
    """Вешалка в сенях: крюки, тулуп на плечиках, ведро, корзина."""
    rnd = random.Random(seed)
    s = f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+w_:.0f}" y2="{y:.0f}" stroke="url(#derev)" stroke-width="16"/>'
    for i in range(3):
        hx = x + w_ * .18 + i * w_ * .32
        s += (f'<path d="M{hx-10:.0f},{y:.0f} q0,{30:.0f} 20,30 q20,0 20,-30"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="6"/>')
    cx = x + w_ * .22
    kach = 2 * A.w(t, 1.6, seed * .1)
    s += (f'<g transform="rotate({kach:.1f} {cx:.0f} {y+30:.0f})">'
          f'<path d="M{cx-66:.0f},{y+16:.0f} q-14,160 10,318 q56,30 112,0 q24,-158 10,-318'
          f' q-66,-28 -132,0 Z" fill="{TKAN2}" {o(6)}/>'
          f'<ellipse cx="{cx:.0f}" cy="{y+24:.0f}" rx="48" ry="16" fill="{TKAN2}" {o(4)}/>'
          f'<path d="M{cx-40:.0f},{y+40:.0f} q40,20 80,0" fill="none" stroke="{kant or SVET}"'
          f' stroke-width="4" opacity=".5"/></g>')
    bx = x + w_ * .58
    s += (f'<path d="M{bx-42:.0f},{y+300:.0f} l10,-130 h64 l10,130 Z" fill="{ZHELEZ}" {o(5)}/>'
          f'<ellipse cx="{bx:.0f}" cy="{y+170:.0f}" rx="42" ry="10" fill="{ZHELEZ}" {o(3)}/>'
          f'<path d="M{bx-30:.0f},{y+160:.0f} q30,-26 60,0" fill="none" stroke="{ZHELEZ}" stroke-width="5"/>')
    kx_ = x + w_ * .86
    s += (f'<path d="M{kx_-54:.0f},{y+300:.0f} q10,-64 54,-64 q44,0 54,64 Z" fill="url(#solom)" {o(5)}/>')
    for i in range(4):
        s += (f'<line x1="{kx_-42+i*28:.0f}" y1="{y+246:.0f}" x2="{kx_-42+i*28:.0f}" y2="{y+298:.0f}"'
              f' stroke="#a07c2e" stroke-width="4"/>')
    s += f'<rect x="{x+w_*.4:.0f}" y="{y+300:.0f}" width="80" height="60" rx="8" fill="#4a3a2a" {o(4)}/>'
    s += f'<rect x="{x+w_*.4+6:.0f}" y="{y+300:.0f}" width="34" height="56" rx="6" fill="#2a1f14" {o(3)}/>'
    return s


def _koza_hozyayka(x, y, h_, t, vlevo=False):
    """Огненная Коза — хозяйка года: тело на четырёх ногах, шея, морда с
    ушами, рога дугой назад, пламя отдельно в гриве и хвосте (R-0013).
    Собрана из простых примитивов (эллипс/прямоугольник), не из рукописных
    безье — так силуэт не разваливается при любом масштабе.
    `vlevo` — развернуть мордой влево (по умолчанию смотрит вправо)."""
    sgn = -1 if vlevo else 1
    w_ = h_ * .62
    dy = 3 * A.w(t, .9)
    kach = 3 * A.w(t, 1.6)
    KOL, KOL2, ROG = "#c23c2e", "#8a2e22", "#7a5a34"
    s = f'<g transform="translate(0,{dy:.1f})">'
    s += ten(x, y + 6, w_ * .62, 16, .5)
    # тело: один эллипс-барабан — надёжный силуэт на любом масштабе
    bx, by_, brx, bry = x - sgn * w_ * .04, y - h_ * .40, w_ * .50, h_ * .20
    # ноги: пара передних (со стороны морды) и пара задних, раздвоенное копыто
    leg_top = by_ + bry * .55
    for fx in (bx + sgn * brx * .62, bx + sgn * brx * .22,
               bx - sgn * brx * .22, bx - sgn * brx * .62):
        lw = w_ * .085
        s += f'<rect x="{fx-lw/2:.0f}" y="{leg_top:.0f}" width="{lw:.0f}" height="{y-10-leg_top:.0f}" rx="{lw*.4:.0f}" fill="{KOL2}" {o(5)}/>'
        s += f'<rect x="{fx-lw*.55:.0f}" y="{y-10:.0f}" width="{lw*.55:.0f}" height="10" fill="#2a1a14" {o(2)}/>'
        s += f'<rect x="{fx:.0f}" y="{y-10:.0f}" width="{lw*.55:.0f}" height="10" fill="#1a100c" {o(2)}/>'
    s += f'<ellipse cx="{bx:.0f}" cy="{by_:.0f}" rx="{brx:.0f}" ry="{bry:.0f}" fill="{KOL}" {o(7)}/>'
    # шея: толстый мазок от груди к голове
    nx0, ny0 = bx + sgn * brx * .78, by_ - bry * .35
    hx, hy = x + sgn * w_ * .70, y - h_ * .84
    s += (f'<path d="M{nx0:.0f},{ny0:.0f} L{hx-sgn*h_*.02:.0f},{hy+h_*.14:.0f}"'
          f' fill="none" stroke="{KOL}" stroke-width="{h_*.30:.0f}" stroke-linecap="round"/>')
    # голова: череп (эллипс) + морда (эллипс поменьше, вынесена вперёд-вниз)
    skr = h_ * .155
    s += f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="{skr:.0f}" ry="{skr*.92:.0f}" fill="{KOL}" {o(6)}/>'
    snx, sny = hx + sgn * h_ * .14, hy + h_ * .07
    s += f'<ellipse cx="{snx:.0f}" cy="{sny:.0f}" rx="{h_*.095:.0f}" ry="{h_*.07:.0f}" fill="{KOL}" {o(5)}/>'
    # уши: два лепестка по бокам черепа
    for sgn2 in (-1, 1):
        ex, ey = hx - sgn * h_ * .02, hy - h_ * .1
        s += (f'<g transform="translate({ex:.0f},{ey:.0f}) rotate({sgn2*38:.0f})">'
              f'<ellipse cx="0" cy="0" rx="{h_*.045:.0f}" ry="{h_*.12:.0f}" fill="{KOL2}" {o(4)}/></g>')
    # рога: две параллельные дуги назад-вверх (ближняя чуть ниже и короче
    # дальней) — одна и та же форма со смещением, чтобы не пересекались
    b1x, b1y = hx - sgn * h_ * .08, hy - h_ * .12
    for off, scl in ((0.0, 1.0), (h_ * .055, .82)):
        bx2, by2 = b1x, b1y + off
        cx2, cy2 = bx2 - sgn * h_ * .16 * scl, by2 - h_ * .22 * scl
        ex2, ey2 = cx2 - sgn * h_ * .09 * scl, cy2 + h_ * .06 * scl
        put = f'M{bx2:.0f},{by2:.0f} Q{cx2:.0f},{cy2:.0f} {ex2:.0f},{ey2:.0f}'
        s += f'<path d="{put}" fill="none" stroke="{ROG}" stroke-width="{h_*.038*scl:.0f}" stroke-linecap="round"/>'
        for k in (.3, .55, .78):
            kx = bx2 + (cx2 - bx2) * k
            ky = by2 + (cy2 - by2) * k
            s += f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="{h_*.009:.0f}" fill="#4a3620" opacity=".6"/>'
    # глаз с бликом
    ex_, ey_ = hx + sgn * h_ * .03, hy - h_ * .01
    bl = 1 if not A.blink(t, 3.6) else 0
    s += f'<ellipse cx="{ex_:.0f}" cy="{ey_:.0f}" rx="{h_*.04:.0f}" ry="{(h_*.045) if bl else 1.6:.1f}" fill="#1a1008"/>'
    if bl:
        s += f'<circle cx="{ex_+sgn*h_*.013:.0f}" cy="{ey_-h_*.013:.0f}" r="{h_*.014:.0f}" fill="#fff"/>'
    # ноздря и рот на морде
    s += f'<ellipse cx="{snx+sgn*h_*.06:.0f}" cy="{sny:.0f}" rx="{h_*.018:.0f}" ry="{h_*.012:.0f}" fill="#1a1008"/>'
    s += (f'<path d="M{snx-sgn*h_*.02:.0f},{sny+h_*.065:.0f} q{sgn*h_*.06:.0f},{h_*.025:.0f} {sgn*h_*.1:.0f},0"'
          f' fill="none" stroke="#5a1a12" stroke-width="{max(2,h_*.01):.1f}"/>')
    # грива: три небольших язычка СТРОГО вдоль гребня шеи, не шире неё
    for k in range(3):
        p = .15 + .3 * k
        gx = nx0 + (hx - nx0) * p
        gy = (ny0 + (hy - ny0) * p) - h_ * .16
        s += ogon(gx, gy, t, h_ / 2000, p * .4, 3, (SVET, ORA)[k % 2])
    s += teplo(nx0 - sgn * h_ * .06, ny0 - h_ * .1, h_ * .30, h_ * .26, .28 + .06 * abs(A.w(t, 1.3)))
    # хвост: короткий толстый мазок от крупа, видимый, с огоньком на конце
    tx0, ty0 = bx - sgn * brx * .85, by_ - bry * .1
    tx1, ty1 = tx0 - sgn * w_ * .08, ty0 + h_ * .16 + kach
    s += (f'<path d="M{tx0:.0f},{ty0:.0f} L{tx1:.0f},{ty1:.0f}"'
          f' fill="none" stroke="{KOL2}" stroke-width="{h_*.055:.0f}" stroke-linecap="round"/>')
    s += ogon(tx1, ty1, t, h_ / 1800, .8, 3, ORA)
    return s + '</g>'


# ═══════════════════════════ ДЕКОРАЦИИ 1-10 ═══════════════════════════════
def ognennaya_koza_u_elki_s_podarkami(t):
    """Коза-хозяйка носом подталкивает гору свёртков к зрителю, ёлка в
    огоньках слева. Единственное тёплое пятно — пламя в её гриве и хвосте."""
    rnd = random.Random(401)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, _oboi_fon("#3a2c38", "#2e2230"))
    s += SL(Z_DAL, okno_izby(1540, 160, 260, 320, t, svet=False, moroz=.5))
    s += SL(Z_DAL, _kartiny_ryad(1020, 150, 2, 6, 100, 130))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _kovrik_pol(560, 940, 700, 130, TKAN, KREM, 2))
    s += SL(Z_SRED, _servant(1300, 240, 520, 600, t))
    s += SL(Z_SRED, _elka(300, 900, 660, t, 7, True))
    rnd2 = random.Random(2)
    svertki = []
    for i in range(6):
        svertki.append((760 + i * 86 + rnd2.uniform(-10, 10), 920 - (i % 3) * 20))
    push = 14 * A.ease(A.seg(t % 2.4, .2, .9))
    sv = ""
    for i, (sx, sy) in enumerate(svertki):
        if i % 3 == 0:
            sv += _korobka(sx + push - 30, sy - 60, 90, 70, t, (TKAN2, ZEL2, MED)[i % 3], ZOL, True, .0, i * .2)
        else:
            sv += _svertok(sx + push, sy, 1.3 + (i % 2) * .3, t, (RUSH, KREM, TKAN2)[i % 3],
                            (TKAN, ZOL, MED)[i % 3], i * .3)
        if i % 2 == 0:
            sv += (f'<circle cx="{sx+push-10:.0f}" cy="{sy-50:.0f}" r="10" fill="url(#med)"'
                   f' opacity="{.5+.4*abs(A.w(t,2.1,i*.2)):.2f}" {o(2)}/>')
    s += SL(Z_SRED, sv)
    s += SL(Z_SRED, _koza_hozyayka(1140, 980, 580, t, vlevo=True))
    s += SL(Z_SRED, f'<path d="M700,1010 q380,40 760,0 l20,70 h-800 Z" fill="#6b4a3c" opacity=".85"/>')
    s += SL(Z_SRED, hodiki(1700, 420, t, 1.0))
    s += SL(Z_SRED, lampa(220, 420, t, .9, True))
    s += SL(Z_SRED, f'<rect x="360" y="700" width="260" height="50" rx="10" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, krynka(430, 700, 1.3))
    s += SL(Z_PERED, ramka_pp("pravo", "#120e10", .5))
    s += SL(Z_PERED, goloe_derevo(60, 1040, 260, t, 4, 5, "#241820"))
    s += vinetka(.44)
    return s


def tri_pravilnyh_podarka(t):
    """Три подарка на столе под ёлкой подпрыгивают по очереди и получают
    бирки."""
    rnd = random.Random(402)
    s = sumerki_fon(t)
    s += SL(Z_DAL, ulica_dal(0, 760, W, t, True, 12))
    s += SL(Z_DAL, okno_izby(1560, 120, 260, 300, t, svet=True, moroz=.4))
    s += SL(Z_SRED, teplo(1690, 270, 260, 220, .4))
    s += SL(Z_SRED, _kartiny_ryad(620, 260, 3, 6, 110, 150))
    s += SL(Z_SRED, f'<rect x="470" y="420" width="420" height="18" rx="5" fill="url(#derev)" {o(4)}/>')
    s += mebel_hlam(410, 760, 260, t, 4)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, _kovrik_pol(460, 900, 760, 120, TKAN2, KREM, 4))
    s += SL(Z_SRED, _elka(1400, 940, 640, t, 14, True))
    s += SL(Z_SRED, stol(560, 760, 820, 36))
    jump = lambda ph: 20 * A.out(A.seg((t + ph) % 2.6, .05, .4)) * (1 if (t + ph) % 2.6 < .5 else 0)
    items = [(740, "varezhka"), (1000, "banka"), (1260, "svistulka")]
    for i, (ix, kind) in enumerate(items):
        iy = 740 - jump(i * .5)
        if kind == "varezhka":
            s += SL(Z_SRED, _varezhka(ix, iy, 2.6, 8 * A.w(t, 2.0, i * .3)))
            s += SL(Z_SRED, _varezhka(ix + 70, iy + 4, 2.3, -6))
        elif kind == "banka":
            s += SL(Z_SRED, _banka(ix, iy, 2.3))
        else:
            s += SL(Z_SRED, _svistulka(ix, iy, 1.8, 6 * A.w(t, 2.2, .4)))
        birka = 1 if (t + i * .5) % 2.6 > 1.2 else 0
        if birka:
            s += SL(Z_SRED, f'<rect x="{ix-16:.0f}" y="{iy-96:.0f}" width="40" height="26" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M560,738 l820,0 l-4,-6 l-812,0 Z" fill="{DOSKA2}" opacity=".7"/>')
    s += SL(Z_SRED, lampa(1660, 360, t, 1.0, True))
    s += SL(Z_SRED, _napolnenie(460, 300, 900, 560, t, 16, 8))
    s += SL(Z_SRED, _napolnenie(900, 260, 500, 480, t, 17, 5))
    s += SL(Z_PERED, goloe_derevo(1900, 1040, 220, t, 6, 4, "#2a2b33"))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 7, .5, .8))
    s += vinetka(.4)
    return s


def tri_podarka_u_zakrytoy_dveri(t):
    """У входной двери три коробки, рукав бабушки в проёме отодвигает их от
    порога."""
    rnd = random.Random(403)
    s = sumerki_fon(t)
    s += SL(Z_DAL, ulica_dal(0, 700, W, t, True, 4))
    s += SL(Z_DAL, panelka(60, 1020, 560, t, 5, True, 6))
    dx_, dy_, dw, dh = 760, 300, 380, 700
    s += SL(Z_SRED, dver(dx_, dy_, dw, dh, .22, kruchok=True))
    s += SL(Z_SRED, f'<path d="M{dx_-20:.0f},{dy_-40:.0f} q{dw*.5:.0f},-30 {dw+40:.0f},0 l0,30 l{-dw-40:.0f},0 Z" fill="{ZEL}" {o(5)}/>')
    for i in range(8):
        a = i / 8 * 6.28
        s += (f'<circle cx="{dx_+dw*.5+math.cos(a)*(dw*.5+8):.0f}" cy="{dy_-18+math.sin(a)*22:.0f}"'
              f' r="8" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{dx_-40:.0f}" y="{dy_+dh:.0f}" width="{dw+80:.0f}" height="30" rx="8" fill="#5a4a3a" {o(4)}/>')
    box1 = _korobka(dx_ + 20, dy_ + dh - 160, 160, 150, t, TKAN, ZOL, True, .0, .1)
    box1 += (f'<ellipse cx="{dx_+100:.0f}" cy="{dy_+dh-200:.0f}" rx="40" ry="14" fill="url(#zol)" {o(3)}/>')
    box2 = _korobka(dx_ + 190, dy_ + dh - 140, 150, 130, t, TKAN2, SVET, True, .0, .4)
    box2 += (f'<rect x="{dx_+230:.0f}" y="{dy_+dh-180:.0f}" width="12" height="60" rx="4" fill="#5a4a3a" {o(3)}/>')
    box3 = _korobka(dx_ + 20, dy_ + dh - 100, 320, 90, t, KREM, TKAN, True, .4, .7)
    box3 += (f'<path d="M{dx_+160:.0f},{dy_+dh-140:.0f} q30,-10 50,20 q-30,10 -50,-20 Z" fill="none" stroke="#9aa0a4" stroke-width="2" opacity=".6"/>')
    push = -40 * A.ease(A.seg(t, .4, 1.2))
    s += SL(Z_SRED, f'<g transform="translate({push:.0f},0)">{box1}{box2}{box3}</g>')
    open_ = A.ease(A.seg(t, .2, .5)) - A.ease(A.seg(t, 1.6, .5))
    rx = dx_ + dw * .5
    s += SL(Z_SRED, f'<rect x="{rx-20:.0f}" y="{dy_+dh*.35:.0f}" width="40" height="{140*max(.1,open_):.0f}"'
                    f' rx="16" fill="#8f353c" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{dy_+dh*.35+140*max(.1,open_):.0f}" rx="26" ry="19" fill="#8f353c" {o(4)}/>')
    s += SL(Z_SRED, teplo(rx, dy_ + dh * .5, 260, 220, .3))
    s += SL(Z_SRED, lampa(dx_ + dw + 220, dy_ + 160, t, .85, False))
    s += SL(Z_DAL, gryaz_polosa(1024, 90, "#2a2e38"))
    # санки у стены — две полозья и дощатый настил
    skx, sky = 500, 980
    s += SL(Z_SRED, f'<path d="M{skx-70:.0f},{sky:.0f} q-10,-20 20,-30 l0,-90 q-10,-16 10,-20"'
                    f' fill="none" stroke="url(#derev)" stroke-width="10"/>')
    s += SL(Z_SRED, f'<path d="M{skx+10:.0f},{sky:.0f} q-10,-20 20,-30 l0,-90 q-10,-16 10,-20"'
                    f' fill="none" stroke="url(#derev)" stroke-width="10"/>')
    s += SL(Z_SRED, f'<rect x="{skx-66:.0f}" y="{sky-110:.0f}" width="130" height="70" rx="6" fill="url(#dosk)" {o(5)}/>')
    # лыжи у крыльца
    lx = 1360
    for sgn in (-1, 1):
        s += SL(Z_SRED, f'<path d="M{lx+sgn*16:.0f},{dy_+dh:.0f} l0,-440 q0,-16 {sgn*14:.0f},-16"'
                        f' fill="none" stroke="#8a5a30" stroke-width="12" stroke-linecap="round"/>')
    # почтовый ящик на столбе
    pyx, pyy = 1460, 760
    s += SL(Z_SRED, f'<rect x="{pyx-12:.0f}" y="{pyy:.0f}" width="24" height="120" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{pyx-34:.0f}" y="{pyy-50:.0f}" width="68" height="54" rx="10" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{pyx-10:.0f}" y="{pyy-30:.0f}" width="20" height="8" fill="{KREM}" opacity=".8"/>')
    # веник у крыльца
    vx = 1240
    s += SL(Z_SRED, f'<line x1="{vx:.0f}" y1="{dy_+dh:.0f}" x2="{vx:.0f}" y2="{dy_+dh-160:.0f}" stroke="#6b4428" stroke-width="10"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{vx-18+i*9:.0f}" y1="{dy_+dh:.0f}" x2="{vx+i*2-10:.0f}" y2="{dy_+dh-60:.0f}" stroke="#a07c2e" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="60" y="860" width="30" height="220" rx="10" fill="#6b4a2e" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="100" y="880" width="30" height="200" rx="10" fill="#6b4a2e" {o(4)}/>')
    s += SL(Z_SRED, _napolnenie(900, 700, 300, 220, t, 17, 3))
    s += SL(Z_PERED, ramka_pp("levo", "#100c0e", .55))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 9, .6, 1.0))
    s += vinetka(.42)
    return s


def podarok_govorit(t):
    """Коробка приподнимает крышку и выпускает облачко-слово; бабушка за
    столом слушает и кивает."""
    rnd = random.Random(404)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 8)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 90))
    s += SL(Z_DAL, okno_izby(1500, 160, 260, 220, t, svet=False, moroz=.4))
    s += SL(Z_DAL, _kartiny_ryad(560, 160, 2, 8, 100, 130))
    s += utvar_izby(100, 400, 280, t, 8)
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _kovrik_pol(420, 940, 680, 110, TKAN, KREM, 8))
    s += SL(Z_SRED, stol(360, 780, 820, 34))
    s += SL(Z_SRED, krynka(1080, 780, 1.0))
    s += SL(Z_SRED, karavay(680, 760, .8, True))
    otkr = .3 + .25 * abs(A.w(t, 1.2, .1))
    s += SL(Z_SRED, _korobka(560, 640, 220, 180, t, TKAN, ZOL, True, otkr, .2))
    rost = A.out(A.seg(t % 3.2, .3, 1.0))
    s += SL(Z_SRED, _oblachko(760, 560 - 60 * rost, .7 + .5 * rost, t, .2, "serdce"))
    s += SL(Z_SRED, svecha(900, 700, t, .1, 1.1))
    s += SL(Z_SRED, f'<rect x="300" y="660" width="90" height="20" rx="6" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="420" cy="700" rx="40" ry="16" fill="#efe3c8" {o(3)}/>')
    s += SL(Z_SRED, par(420, 684, t, 3, .4, 120, .5))
    s += SL(Z_SRED, f'<ellipse cx="1000" cy="680" rx="60" ry="30" fill="{KREM}" {o(4)}/>')
    kiv = 5 * A.w(t, 1.4, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kiv:.1f} 1150 940)">'
                    + figura(1150, 1060, 520, t, "#3a2c3c", "#ffe2a8", True, .2) + '</g>')
    s += SL(Z_SRED, f'<rect x="1030" y="1010" width="300" height="20" rx="6" fill="{TKAN}" opacity=".7"/>')
    s += SL(Z_SRED, pech(1140, 300, 460, 640, t, True, True, False))
    s += SL(Z_SRED, _napolnenie(420, 600, 600, 260, t, 19, 6))
    s += SL(Z_SRED, f'<rect x="420" y="320" width="320" height="420" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="350" width="280" height="160" rx="6" fill="url(#stekl)" opacity=".6" {o(4)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0c", .45))
    s += SL(Z_LETIT, mokryy_sneg(t, 14, 6, .4, .7))
    s += vinetka(.42)
    return s


def babushka_i_cennik(t):
    """Продавщица показывает на ценник, бабушка отводит его рукавом и
    слушает платок у уха."""
    rnd = random.Random(405)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("den", t, False, 2)
    s += SL(Z_DAL, brevna(0, 40, W, 700, 86))
    s += SL(Z_DAL, okno_izby(1560, 120, 240, 220, t, svet=False, moroz=.2))
    s += utvar_pekarni(1180, 720, 420, t, 2)
    s += SL(Z_SRED, polovicy(760))
    s += SL(Z_SRED, lampa(960, 160, t, 1.0, True))
    pril = f'<rect x="200" y="640" width="1200" height="140" rx="10" fill="url(#derev)" {o(7)}/>'
    pril += f'<rect x="200" y="780" width="1200" height="220" fill="#4a3528" {o(6)}/>'
    s += SL(Z_SRED, pril)
    s += SL(Z_SRED, f'<rect x="280" y="560" width="220" height="100" rx="8" fill="{ZHELEZ}" {o(5)}/>')
    kach = 2 * A.w(t, 1.6, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 390 600)"><line x1="330" y1="600" x2="450" y2="600"'
                    f' stroke="url(#zhel)" stroke-width="6"/>'
                    f'<circle cx="330" cy="600" r="26" fill="{TKAN}" opacity=".7"/>'
                    f'<circle cx="450" cy="600" r="26" fill="{TKAN}" opacity=".7"/></g>')
    s += SL(Z_SRED, f'<rect x="560" y="560" width="200" height="50" rx="10" fill="#6b4a2e" {o(4)}/>')
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{570+i*30}" y="580" width="24" height="60" rx="3" fill="{(KRAS,SVET)[i%2]}" opacity=".7"/>')
    cen_off = 46 * A.ease(A.seg(t, .3, .9))
    s += SL(Z_SRED, f'<rect x="{820+cen_off:.0f}" y="600" width="160" height="40" rx="6" fill="{TKAN}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{830+cen_off:.0f}" y="608" width="60" height="24" rx="3" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, figura(430, 780, 480, t, "#8a6a4a", "#efe3c8", False, .0))
    ruk1, (r1x, r1y) = rukav(560, 600, 150, -4 + 6 * A.w(t, 1.9, .1), t, "#8a6a4a", "#efe3c8", .1)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="24" ry="17" fill="#8a6a4a" {o(4)}/>')
    s += SL(Z_SRED, figura(1000, 940, 520, t, "#2a2c3c", "#cfe4f5", False, .3))
    plat_ear = 6 * A.w(t, 1.5, .4)
    ruk2, (r2x, r2y) = rukav(1120, 760, 170, -70 + plat_ear, t, "#2a2c3c", "#cfe4f5", .4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="24" ry="17" fill="#2a2c3c" {o(4)}/>')
    s += SL(Z_SRED, _varezhka(r2x, r2y - 10, 1.4, 0, TKAN))
    s += SL(Z_SRED, f'<rect x="{900-cen_off*.3:.0f}" y="620" width="140" height="130" rx="10" fill="{TKAN}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="260" width="420" height="340" rx="10" fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="720" y="{280+i*108:.0f}" width="380" height="90" rx="6" fill="none" {o(3)}/>')
    rnd3 = random.Random(9)
    for i in range(7):
        jx = 740 + i * 52
        jy = 280 + (i % 3) * 108 + 70
        s += SL(Z_SRED, _banka(jx, jy, .7, rnd3.choice((MED, "#8c8275"))))
    s += SL(Z_SRED, _napolnenie(420, 600, 300, 200, t, 19, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, luch(1560, 160, 160, 500, t, .18))
    s += vinetka(.4)
    return s


def tri_govoryaschie_veschi(t):
    """На подоконнике три вещи по словам всплывают облачками; рядом коробка
    с проёмом под настоящий кадр."""
    rnd = random.Random(406)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 14)
    s += SL(Z_DAL, oblaka(t, 150, 3, 9, .3, "#c3cedd", 11.0))
    s += SL(Z_DAL, okno_izby(120, 140, 900, 420, t, svet=False, moroz=.55))
    s += SL(Z_SRED, f'<rect x="60" y="560" width="1020" height="80" rx="10" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, _kovrik_pol(460, 900, 600, 110, TKAN2, KREM, 9))
    seg = A.seg(t % 6.8, 0, 6.8)
    stage = 0 if seg < .34 else (1 if seg < .67 else 2)
    items = (("koshelek", 460), ("banka", 680), ("varezhka", 900))
    for i, (kind, ix) in enumerate(items):
        rise = 30 * A.out(A.seg(t % 6.8, i * .2, .5))
        iy = 560 - rise
        if kind == "koshelek":
            s += SL(Z_SRED, _koshelek(ix, iy, 1.2, True, 1))
            kinds = "moneta"
        elif kind == "banka":
            s += SL(Z_SRED, _banka(ix, iy, 1.3))
            kinds = "serdce"
        else:
            s += SL(Z_SRED, _varezhka(ix, iy, 1.9, 6 * A.w(t, 1.6, i * .2)))
            kinds = "ruki"
        if i <= stage:
            s += SL(Z_SRED, _oblachko(ix, iy - 110, .8, t, i * .3, kinds))
    s += SL(Z_SRED, f'<rect x="1140" y="540" width="40" height="200" rx="14" fill="{ZEL}" {o(4)}/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M1160,{560+i*30} l-22,10 M1160,{560+i*30} l22,10" stroke="{ZEL}" stroke-width="5"/>')
    pw, ph_ = 760, 320
    px, py = 1180, 480
    # план 6: настоящий кадр (вязаные варежки) ставится в проём стенки;
    # план 7 той же декорации сток не требует, но метка должна быть всегда.
    put = kontur_proema(px, py, pw, ph_, "pryam")
    korob = f'<path d="{put}" fill="#1a140e"/>'
    korob += mesto_stoka(px, py, pw, ph_, "pryam")
    korob += f'<path d="{put}" fill="none" {o(6)}/>'
    korob += f'<rect x="{px-30:.0f}" y="{py-30:.0f}" width="{pw+60}" height="40" fill="{TKAN2}" {o(6)}/>'
    korob += f'<rect x="{px-30:.0f}" y="{py+ph_:.0f}" width="{pw+60}" height="180" fill="{TKAN2}" {o(6)}/>'
    s += SL(Z_SRED, korob)
    s += SL(Z_SRED, svecha(1120, 760, t, .2, 1.0))
    s += SL(Z_SRED, f'<path d="M160,780 l-16,-120 l40,20 l16,100 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="1000" cy="720" r="30" fill="url(#glina)" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="280" width="340" height="300" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _dvertsy_shkafa(420, 280, 340, 300, 150))
    s += SL(Z_SRED, _napolnenie(420, 600, 900, 200, t, 20, 6))
    s += SL(Z_PERED, ramka_pp("levo", "#120e10", .42))
    s += SL(Z_LETIT, sneg_letit(t, 20, 11, .5, .9))
    s += vinetka(.4)
    return s


def _dvertsy_shkafa(x, y, w_, h_, glass_h, col="#3a2416"):
    """Дверцы шкафа/буфета: за стеклом сверху посуда, на глухой нижней части
    филёнка и ручки, шов между створками по всей высоте. Довод четырёх сцен,
    где мебель стояла серой плашкой без деталей (хвост 15.11)."""
    mid = x + w_ * .5
    gx, gy, gw, gh = x + w_ * .07, y + 16, w_ * .86, glass_h - 30
    s = (f'<ellipse cx="{gx+gw*.28:.0f}" cy="{gy+gh*.74:.0f}" rx="{gw*.16:.0f}" ry="8"'
         f' fill="{KREM}" opacity=".85"/>')
    s += (f'<ellipse cx="{gx+gw*.28:.0f}" cy="{gy+gh*.58:.0f}" rx="{gw*.16:.0f}" ry="8"'
          f' fill="{KREM}" opacity=".85"/>')
    s += (f'<path d="M{gx+gw*.6:.0f},{gy+gh*.82:.0f} v{-gh*.46:.0f} q0,-10 10,-10'
          f' h{gw*.2:.0f} q10,0 10,10 v{gh*.46:.0f} Z" fill="url(#glina)" opacity=".85" {o(2)}/>')
    s += (f'<rect x="{gx:.0f}" y="{gy:.0f}" width="{gw:.0f}" height="{gh:.0f}" rx="4"'
          f' fill="url(#stekl)" opacity=".4" {o(3)}/>')
    s += f'<line x1="{mid:.0f}" y1="{y:.0f}" x2="{mid:.0f}" y2="{y+h_:.0f}" stroke="{col}" stroke-width="4" opacity=".6"/>'
    pan_y, pan_h = y + glass_h + 16, h_ - glass_h - 32
    if pan_h > 24:
        for lx in (x + w_ * .08, mid + w_ * .08):
            s += (f'<rect x="{lx:.0f}" y="{pan_y:.0f}" width="{w_*.34:.0f}" height="{pan_h:.0f}" rx="8"'
                  f' fill="none" stroke="{col}" stroke-width="5" opacity=".55"/>')
    hy = y + h_ * .52
    for hx in (mid - w_ * .07, mid + w_ * .07):
        s += f'<rect x="{hx:.0f}" y="{hy:.0f}" width="10" height="46" rx="5" fill="{ZHELEZ}" {o(2)}/>'
    return s


def kalendar_s_novym_godom(t):
    """Отрывной календарь: бабушка со стремянки отрывает последний листок
    декабря, под ним новогодняя обложка."""
    rnd = random.Random(407)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 5)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += utvar_izby(1200, 420, 360, t, 5)
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _kovrik_pol(500, 900, 560, 110, TKAN, KREM, 21))
    s += SL(Z_SRED, f'<rect x="1200" y="300" width="300" height="600" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _dvertsy_shkafa(1200, 300, 300, 600, 280))
    s += SL(Z_SRED, f'<rect x="420" y="420" width="260" height="480" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="440" width="220" height="18" rx="5" fill="url(#derev)" {o(4)}/>')
    kx, ky = 760, 320
    s += SL(Z_SRED, f'<rect x="{kx-130:.0f}" y="{ky-200:.0f}" width="260" height="360" rx="10" fill="{KREM}" {o(6)}/>')
    otr = A.ease(A.seg(t, .5, 1.0))
    s += SL(Z_SRED, f'<g transform="rotate({otr*60:.1f} {kx-110:.0f} {ky-80:.0f})">'
                    f'<rect x="{kx-110:.0f}" y="{ky-170:.0f}" width="220" height="160" fill="#fff" {o(4)}/></g>')
    s += SL(Z_SRED, f'<rect x="{kx-110:.0f}" y="{ky:.0f}" width="220" height="130" fill="{KRAS}" {o(5)}/>')
    s += SL(Z_SRED, _koza_hozyayka(kx, ky + 100, 160, t))
    s += SL(Z_SRED, hodiki(1400, 300, t, 1.1))
    s += SL(Z_SRED, f'<rect x="300" y="500" width="180" height="24" rx="6" fill="url(#derev)" {o(5)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="{320+i*50}" y="420" width="40" height="80" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M560,560 l-30,-60 l60,0 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="530" cy="500" r="16" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="80" y="520" width="12" height="440" fill="#6b4a2e" {o(4)}/>')
    stoy = figura(120, 980, 540, t, "#3a2c3c", "#ffd98a", True, .0)
    s += SL(Z_SRED, stoy)
    ruk, (rx, ry) = rukav(190, 640, 150, -70, t, "#3a2c3c", "#ffd98a", .0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="24" ry="17" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, lampa(1660, 420, t, .95, True))
    s += SL(Z_SRED, f'<rect x="760" y="500" width="380" height="400" rx="10" fill="#3a3028" opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 1080, 200, t, 21, 7))
    s += SL(Z_PERED, ramka_pp("pravo", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 8, .5, .7))
    s += vinetka(.42)
    return s


def monetka_za_podarok(t):
    """Две руки над столом: коробка с ножницами переходит, монетка ложится
    на ладонь, запрещающая черта гаснет и зажигается галочка."""
    rnd = random.Random(408)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 9)
    s += SL(Z_DAL, okno_izby(1560, 120, 260, 260, t, svet=True, moroz=.3))
    s += SL(Z_SRED, teplo(1690, 260, 260, 220, .38))
    s += utvar_izby(80, 440, 480, t, 11)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="320" width="300" height="500" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="340" width="260" height="220" rx="6" fill="url(#stekl)" opacity=".55" {o(4)}/>')
    s += SL(Z_SRED, hodiki(1420, 360, t, 1.0))
    s += SL(Z_SRED, f'<rect x="900" y="260" width="340" height="260" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, _kartiny_ryad(940, 290, 2, 12, 110, 150))
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN, KREM, 24))
    s += SL(Z_SRED, stol(460, 760, 900, 36))
    s += SL(Z_SRED, svecha(560, 700, t, .0, 1.1))
    s += SL(Z_SRED, svecha(1260, 700, t, .4, 1.1))
    s += SL(Z_SRED, f'<ellipse cx="800" cy="720" rx="80" ry="30" fill="{KREM}" {o(4)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{760+i*20}" cy="710" r="10" fill="{ZEL2}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1050" cy="700" rx="40" ry="16" fill="url(#derev)" {o(3)}/>')
    seg = A.seg(t, .2, .8)
    box = _korobka(640, 580, 140, 110, t, TKAN2, SVET, True, .2, .1)
    offx = -40 * (1 - seg)
    s += SL(Z_SRED, f'<g transform="translate({offx:.0f},0)">{box}</g>')
    moneta_fall = A.out(A.seg(t, 1.0, .6))
    mx, my = 1100, 560 - 30 + 30 * moneta_fall
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="22" ry="15" fill="url(#med)" {o(3)}/>')
    zapr_on = 1 - A.ease(A.seg(t, 1.0, .5))
    if zapr_on > .05:
        s += SL(Z_SRED, _zapret(760, 440, 60, t))
    else:
        s += SL(Z_SRED, _galochka(760, 440, 1.2, t))
    r1, (r1x, r1y) = rukav(760, 620, 160, -150 + 10 * A.w(t, 1.6), t, "#5a3a26", "#ffd98a", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="26" ry="18" fill="#5a3a26" {o(4)}/>')
    r2, (r2x, r2y) = rukav(1160, 620, 160, -30 + 10 * A.w(t, 1.6, .2), t, "#2a3450", "#cfe4f5", .3)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="26" ry="18" fill="#2a3450" {o(4)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 1000, 180, t, 24, 7))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .42))
    s += SL(Z_LETIT, mokryy_sneg(t, 12, 5, .35, .6))
    s += vinetka(.42)
    return s


def chasy_i_dvoe_na_perrone(t):
    """Вокзальные часы на столбе, их циферблат — проём под настоящий кадр;
    на перроне он и она, между ними растёт трещина."""
    rnd = random.Random(409)
    s = sumerki_fon(t)
    s += SL(Z_DAL, ulica_dal(0, 760, W, t, True, 3))
    s += SL(Z_DAL, f'<rect x="0" y="760" width="{W}" height="100" fill="#4a4e58" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="60" y="860" width="{W-120}" height="200" fill="#5a5e68" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{80+i*380}" y1="880" x2="{80+i*380}" y2="1050" stroke="#3a3e48" stroke-width="3" opacity=".5"/>')
    vid = f'<circle cx="960" cy="400" r="190" fill="{KREM}"/>'
    pw, ph_ = 400, 400
    px, py = 760, 200
    vid2 = ""
    for i in range(6):
        a = math.radians(i * 30)
        vid2 += (f'<line x1="{960+math.sin(a)*160:.0f}" y1="{400-math.cos(a)*160:.0f}"'
                 f' x2="{960+math.sin(a)*180:.0f}" y2="{400-math.cos(a)*180:.0f}" stroke="#333" stroke-width="4"/>')
    a_sec = (t * 70) % 360
    vid2 += (f'<line x1="960" y1="400" x2="{960+math.sin(math.radians(a_sec))*150:.0f}"'
             f' y2="{400-math.cos(math.radians(a_sec))*150:.0f}" stroke="{KRAS}" stroke-width="3"/>')
    stolb = f'<rect x="920" y="400" width="80" height="420" rx="10" fill="{ZHELEZ}" {o(5)}/>'
    put = kontur_proema(px, py, pw, ph_, "ellips")
    sten = f'<path d="{put}" fill="#1a140e"/>' + vid + vid2 + mesto_stoka(px, py, pw, ph_, "ellips")
    sten += f'<path d="{put}" fill="none" {o(10)}/>'
    s += SL(Z_SRED, stolb + sten)
    s += SL(Z_SRED, f'<rect x="300" y="900" width="220" height="30" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="320" y="840" width="24" height="60" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="480" y="840" width="24" height="60" fill="url(#derev)" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M160,900 h140 v30 l-10,40 h-120 l-10,-40 Z" fill="{ZHELEZ}" {o(4)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<ellipse cx="{200+i*40}" cy="900" rx="28" ry="24" fill="#8a7a5a" opacity=".8" {o(2)}/>')
    # станционный киоск слева от столба — крытая будка
    kx_ = 500
    s += SL(Z_SRED, f'<rect x="{kx_:.0f}" y="350" width="260" height="620" rx="8" fill="#5a3a2a" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{kx_-20:.0f},480 h300 l-20,-40 h-260 Z" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kx_+30:.0f}" y="540" width="200" height="140" rx="4" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1500" y="700" width="50" height="320" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, ogon(1525, 660, t, .5, .3, 5))
    s += SL(Z_SRED, teplo(1525, 700, 260, 210, .32))
    s += SL(Z_SRED, dym(300, 1040, t, 4, .3, 200, .3, "#cfd6de"))
    s += SL(Z_SRED, f'<rect x="1620" y="980" width="90" height="20" rx="6" fill="{ZHELEZ}" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="600" width="140" height="90" rx="6" fill="{ZHELEZ}" opacity=".6" {o(3)}/>')
    trech = 160 * A.ease(A.seg(t, .3, 2.0))
    s += SL(Z_SRED, f'<path d="M960,1040 l{trech*.3:.0f},-10 l{-trech*.4:.0f},-14 l{trech*.5:.0f},-10'
                    f' l{-trech*.2:.0f},-10" fill="none" stroke="#1a1c22" stroke-width="4" opacity="{min(1,trech/150):.2f}"/>')
    s += SL(Z_SRED, figura(840, 1030, 540, t, "#2a2e3c", "#cfe4f5", False, .0))
    s += SL(Z_SRED, f'<rect x="770" y="920" width="60" height="100" rx="10" fill="#4a3c2e" {o(4)}/>')
    s += SL(Z_SRED, figura(1080, 1020, 500, t, "#3a2c3c", "#ffd98a", True, .2))
    s += SL(Z_SRED, para_izo_rta(850, 780, t, .1, .9, .4))
    s += SL(Z_SRED, para_izo_rta(1090, 790, t, .4, .8, .35))
    s += SL(Z_SRED, _napolnenie(420, 850, 1000, 100, t, 22, 5))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c10", .5))
    s += SL(Z_LETIT, sneg_letit(t, 30, 15, .5, .9))
    s += vinetka(.44)
    return s


def nozh_rezhet_lentu_druzhby(t):
    """Нож в коробке сам приподнимается и перерезает ленту, которую держат
    две подруги за столом."""
    rnd = random.Random(410)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 6)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_DAL, okno_izby(140, 140, 280, 240, t, svet=True, moroz=.4))
    s += SL(Z_SRED, teplo(280, 260, 260, 220, .36))
    s += utvar_izby(1200, 420, 300, t, 13)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="320" width="280" height="440" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _dvertsy_shkafa(420, 320, 280, 440, 210))
    s += SL(Z_SRED, hodiki(1420, 360, t, 1.0))
    s += SL(Z_SRED, f'<rect x="760" y="260" width="340" height="300" rx="8" fill="{KAMEN2}" {o(5)}/>')
    s += SL(Z_SRED, _kartiny_ryad(800, 300, 2, 14, 110, 150))
    s += SL(Z_SRED, _kovrik_pol(500, 900, 700, 110, TKAN2, KREM, 23))
    s += SL(Z_SRED, stol(560, 760, 820, 34))
    podn = A.out(A.seg(t % 3.0, .2, .4)) * (1 if (t % 3.0) < 1.4 else 1 - A.ease(A.seg(t % 3.0, 1.4, .4)))
    s += SL(Z_SRED, f'<rect x="700" y="{700-podn*40:.0f}" width="220" height="60" rx="8" fill="#5a3a26" {o(5)}/>')
    nx, ny = 810, 700 - podn * 70
    s += SL(Z_SRED, f'<g transform="rotate({podn*20:.0f} {nx:.0f} {ny:.0f})">'
                    f'<path d="M{nx-70:.0f},{ny:.0f} l140,-10 l-20,20 l-120,6 Z" fill="{ZHELEZ}" {o(4)}/>'
                    f'<rect x="{nx+60:.0f}" y="{ny-10:.0f}" width="50" height="20" rx="6" fill="#5a3a26" {o(3)}/></g>')
    rezka = A.ease(A.seg(t, 1.6, .4))
    lenta_y = 640
    if rezka < .98:
        s += SL(Z_SRED, f'<path d="M560,{lenta_y} h{360*(1-rezka):.0f}" stroke="{KRAS}" stroke-width="14"/>')
        s += SL(Z_SRED, f'<path d="M{560+360*(1-rezka)+440*rezka:.0f},{lenta_y} h{360*(1-rezka):.0f}" stroke="{KRAS}" stroke-width="14"/>')
    else:
        lx1 = 560 - 60 * (rezka - .98) * 20
        lx2 = 1300 + 60 * (rezka - .98) * 20
        s += SL(Z_SRED, f'<path d="M{lx1:.0f},{lenta_y} h300" stroke="{KRAS}" stroke-width="14"/>')
        s += SL(Z_SRED, f'<path d="M{lx2-300:.0f},{lenta_y} h300" stroke="{KRAS}" stroke-width="14"/>')
    for bx in (560, 1340):
        s += SL(Z_SRED, f'<circle cx="{bx:.0f}" cy="{lenta_y:.0f}" r="26" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="640" cy="720" rx="60" ry="26" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1240" cy="720" rx="100" ry="30" fill="#caa86a" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="860" y="700" width="60" height="50" rx="8" fill="{KAMEN}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1000" cy="720" rx="36" ry="14" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, figura(600, 940, 480, t, "#6b2a38", "#ffd98a", False, .0))
    s += SL(Z_SRED, figura(1300, 940, 480, t, "#2a4a3a", "#ffd98a", False, .2))
    s += SL(Z_SRED, svecha(1000, 680, t, .3, 1.0))
    s += SL(Z_SRED, _napolnenie(900, 550, 400, 160, t, 23, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 14, 9, .4, .7))
    s += vinetka(.42)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 11-18 ══════════════════════════════
def pustoy_koshelek_i_pustoy_god(t):
    """Пустой кошелёк на комоде, из него вылетает моль; за ним ряд из
    двенадцати листков календаря с пустыми тарелками."""
    rnd = random.Random(411)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 10)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += kvartira_veschi(1480, 680, 380, t, 14)
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="230" width="300" height="610" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _dvertsy_shkafa(420, 230, 300, 610, 250))
    s += SL(Z_SRED, _kovrik_pol(480, 840, 760, 160, TKAN2, KREM, 25))
    s += SL(Z_SRED, f'<rect x="160" y="560" width="1200" height="40" rx="10" fill="url(#derev)" {o(6)}/>')
    for i in range(12):
        lx = 200 + i * 88
        rot = 3 * A.w(t, 1.4, i * .15)
        s += SL(Z_SRED, f'<g transform="rotate({rot:.1f} {lx+30:.0f} {520:.0f})">'
                        f'<rect x="{lx:.0f}" y="420" width="60" height="100" rx="4" fill="{KREM}" {o(3)}/>'
                        f'<ellipse cx="{lx+30:.0f}" cy="470" rx="18" ry="14" fill="none" stroke="#9aa0a4" stroke-width="2"/></g>')
    moly = 20 * A.w(t, 2.4)
    s += SL(Z_SRED, _koshelek(640, 760, 3.2, True, 0, True, t))
    s += SL(Z_SRED, f'<ellipse cx="{700+moly:.0f}" cy="{660-abs(moly):.0f}" rx="12" ry="7" fill="#9a8a78" opacity=".7"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="600" width="260" height="220" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1360" cy="660" rx="40" ry="40" fill="#cfd6de" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1430" y="640" width="14" height="60" rx="5" fill="{K}" {o(2)}/>')
    kach = 4 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 1500 700)"><circle cx="1490" cy="700" r="10" fill="{ZHELEZ}"/>'
                    f'<circle cx="1510" cy="700" r="10" fill="{ZHELEZ}"/>'
                    f'<line x1="1480" y1="700" x2="1480" y2="650" stroke="{ZHELEZ}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="800" rx="30" ry="18" fill="#cfd6de" opacity=".85" {o(2)}/>')
    s += SL(Z_SRED, svecha(1000, 740, t, .2, 1.0))
    s += SL(Z_SRED, f'<rect x="760" y="800" width="160" height="22" rx="6" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="900" y="230" width="320" height="370" rx="8" fill="{KAMEN2}" {o(5)}/>')
    s += SL(Z_SRED, _kartiny_ryad(940, 310, 2, 26, 110, 150))
    s += SL(Z_SRED, _napolnenie(900, 600, 500, 150, t, 25, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .42))
    s += SL(Z_LETIT, mokryy_sneg(t, 10, 6, .3, .6))
    s += vinetka(.42)
    return s


def derevo_s_tremya_kornyami(t):
    """Яблоня в разрезе земли: над землёй свёртки на ветках, под землёй три
    корня с загорающимися номерами. Холодный дневной свет, смена главы."""
    rnd = random.Random(412)
    s = f'<rect width="{W}" height="{H}" fill="{DEN}"/>'
    s += nebo("den", t, False, 1)
    s += SL(Z_DAL, oblaka(t, 140, 4, 13, .4, "#e8eef6", 9.0))
    zemlya_y = 700
    s += SL(Z_DAL, f'<rect x="0" y="{zemlya_y}" width="{W}" height="{H-zemlya_y}" fill="#4a3a2c" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="{zemlya_y-14}" width="{W}" height="20" fill="url(#sneg)" {o(4)}/>')
    sway = 2 * A.w(t, 2.8)
    stvol = (f'<g transform="rotate({sway:.1f} 960 {zemlya_y})">'
             f'<path d="M900,{zemlya_y} L930,{zemlya_y-440} L1010,{zemlya_y-440} L1040,{zemlya_y} Z"'
             f' fill="url(#derev)" {o(7)}/>')
    for i, (dx, dy, dl) in enumerate(((-260, -360, 220), (240, -380, 240), (-140, -460, 200), (180, -480, 210))):
        stvol += (f'<path d="M970,{zemlya_y-400+i*20} q{dx*.5:.0f},{dy*.25:.0f} {dx:.0f},{dy:.0f}"'
                  f' fill="none" stroke="{DOSKA2}" stroke-width="14" stroke-linecap="round"/>')
    stvol += '</g>'
    s += SL(Z_SRED, stvol)
    rnd2 = random.Random(5)
    for i, (dx, dy) in enumerate(((-250, -380), (220, -400), (-120, -480), (160, -500), (0, -560))):
        qx, qy = 970 + dx, zemlya_y + dy
        bob = 6 * A.w(t, 1.6, i * .2)
        s += SL(Z_SRED, _svertok(qx, qy + bob, 1.4, t, (RUSH, KREM, TKAN2)[i % 3], (TKAN, ZOL)[i % 2], i * .2))
    s += SL(Z_SRED, f'<path d="M300,{zemlya_y} h1320" stroke="url(#derev)" stroke-width="10"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="{320+i*140}" y="{zemlya_y-70}" width="18" height="70" fill="url(#derev)" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1500,{zemlya_y-220} q20,-40 60,-40 q0,40 -40,60 Z" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="1520" cy="{zemlya_y-260}" r="16" fill="#2a2420" {o(2)}/>')
    s += SL(Z_DAL, izba_snaruzhi(420, zemlya_y + 20, 480, t, True, True, 9))
    s += SL(Z_DAL, dym(260, zemlya_y - 480, t, 4, .22, 260, .4, "#dde4ec"))
    sugrob = f'<path d="M1600,{zemlya_y} q80,-60 220,-10 l0,30 h-220 Z" fill="url(#sneg)" {o(5)}/>'
    s += SL(Z_SRED, sugrob)
    fly = (t * 90) % 1920
    s += SL(Z_SRED, f'<g transform="translate({fly-200:.0f},{280+30*A.w(t,2.2):.0f})">'
                    f'<ellipse cx="0" cy="0" rx="30" ry="16" fill="#1a1c22" {o(3)}/>'
                    f'<ellipse cx="34" cy="-4" rx="16" ry="20" fill="#fff" {o(2)}/></g>')
    korni = []
    for dx, dy, lb in ((-220, 220, 1), (0, 280, 2), (220, 220, 3)):
        korni.append((960 + dx, zemlya_y + dy))
    korn_svg = f'<g transform="rotate({sway*.3:.1f} 960 {zemlya_y})">'
    for i, (kx, ky) in enumerate(korni):
        korn_svg += (f'<path d="M960,{zemlya_y} Q{(960+kx)/2:.0f},{zemlya_y+40}'
                     f' {kx:.0f},{ky:.0f}" fill="none" stroke="url(#derev)" stroke-width="{36-i*4}"/>')
        on = ((t * 1.2 + i * .4) % 3.0) < 1.5
        s_op = .9 if on else .25
        korn_svg += f'<circle cx="{kx:.0f}" cy="{ky+20:.0f}" r="22" fill="{ZOL}" opacity="{s_op:.2f}" {o(3)}/>'
    korn_svg += '</g>'
    s += SL(Z_SRED, korn_svg)
    s += SL(Z_SRED, f'<rect x="700" y="{zemlya_y-120}" width="26" height="120" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="686" y="{zemlya_y-150}" width="54" height="36" rx="8" fill="#6b4428" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="710" cy="{zemlya_y-132}" r="10" fill="#2a2420"/>')
    # колодец у забора — сруб, два столба и двускатная крыша, своя высота
    kolx = 1320
    s += SL(Z_SRED, f'<rect x="{kolx-60:.0f}" y="{zemlya_y-70:.0f}" width="120" height="70" rx="6" fill="url(#brev)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kolx-70:.0f}" y="{zemlya_y-320:.0f}" width="16" height="250" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{kolx+54:.0f}" y="{zemlya_y-320:.0f}" width="16" height="250" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{kolx-90:.0f},{zemlya_y-310:.0f} h180 l-20,-50 h-140 Z" fill="{DOSKA2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kolx-6:.0f}" y="{zemlya_y-280:.0f}" width="12" height="200" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, pleten(1180, zemlya_y + 60, 340, 170, 5))
    s += SL(Z_SRED, _napolnenie(420, 330, 460, 180, t, 26, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#1a1c22", .3))
    s += vinetka(.3)
    return s


def platki_u_vorot(t):
    """У ворот стол с платками и полотенцами: платок переходит из рук
    хозяйки к старику и соседке; лица опущены, сцена тихая."""
    rnd = random.Random(413)
    s = f'<rect width="{W}" height="{H}" fill="{SERO}"/>'
    s += nebo("den", t, False, 4)
    s += SL(Z_DAL, pleten(60, 760, 1200, 170, 7))
    s += SL(Z_DAL, f'<rect x="760" y="300" width="340" height="480" fill="#8a7a6a" opacity=".6" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="1300" y="640" width="60" height="320" fill="url(#kamen)" {o(5)}/>')
    s += SL(Z_DAL, f'<path d="M1260,640 h140 l-20,-50 h-100 Z" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="850" y="600" width="220" height="160" rx="30" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, goloe_derevo(1440, 940, 300, t, 10, 6, "#3a3a44"))
    # поленница у плетня — настоящие дрова со срезами
    for row in range(3):
        for col in range(5):
            s += SL(Z_SRED, f'<circle cx="{430+col*42:.0f}" cy="{880-row*40:.0f}" r="20" fill="url(#derev)" {o(3)}/>')
            s += SL(Z_SRED, f'<circle cx="{430+col*42:.0f}" cy="{880-row*40:.0f}" r="12" fill="{KREM}" opacity=".5"/>')
    s += SL(Z_SRED, sneg_lezhit(900))
    s += SL(Z_SRED, stol(560, 820, 760, 36))
    s += SL(Z_SRED, f'<rect x="540" y="800" width="800" height="30" rx="6" fill="#fff" opacity=".9" {o(4)}/>')
    stopka = 5
    seg = A.seg(t, 1.0, 7.0)
    stopka_now = max(2, round(stopka - seg * 3))
    for i in range(stopka_now):
        s += SL(Z_SRED, f'<rect x="{620+i*4:.0f}" y="{790-i*16:.0f}" width="180" height="20" rx="4" fill="{KREM}" {o(3)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="{900+i*4:.0f}" y="{784-i*16:.0f}" width="150" height="18" rx="4" fill="{RUSH}" {o(3)}/>')
    peredacha = A.ease(A.seg(t % 3.0, .2, 1.0))
    px_ = 980 + 220 * peredacha
    s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="760" width="100" height="16" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, figura(700, 1000, 480, t, "#3a3a44", "#9aa0a4", True, .0, naklon=6))
    r1, (r1x, r1y) = rukav(800, 700, 150, -20, t, "#3a3a44", "#9aa0a4", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="24" ry="17" fill="#3a3a44" {o(4)}/>')
    s += SL(Z_SRED, figura(1220, 1010, 500, t, "#3a3028", "#8a8a8a", False, .2, boroda=True, naklon=8))
    r2a, (r2ax, r2ay) = rukav(1130, 740, 130, -150, t, "#3a3028", "#8a8a8a", .3)
    r2b, (r2bx, r2by) = rukav(1310, 740, 130, -30, t, "#3a3028", "#8a8a8a", .5)
    s += SL(Z_SRED, r2a + r2b)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="24" ry="17" fill="#3a3028" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2bx:.0f}" cy="{r2by:.0f}" rx="24" ry="17" fill="#3a3028" {o(4)}/>')
    s += SL(Z_SRED, figura(1420, 1010, 480, t, "#44403a", "#9aa0a4", True, .4, naklon=6))
    s += SL(Z_SRED, f'<rect x="1370" y="900" width="100" height="70" rx="8" fill="{RUSH}" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 27, 4))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 27, 4))
    s += SL(Z_SRED, lampa(240, 540, t, .8, False))
    s += SL(Z_PERED, goloe_derevo(1800, 1040, 240, t, 9, 5, "#3a3a44"))
    s += SL(Z_LETIT, sneg_letit(t, 10, 7, .3, .5))
    s += vinetka(.3)
    return s


def platok_polotence_i_tapochki(t):
    """Раскрытый шкаф, на средней полке платок, полотенце и тапочки; над
    ними капли-слёзы. Средняя полка — проём под настоящий кадр."""
    rnd = random.Random(414)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 2)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(800))
    shx, shy, shw, shh = 560, 160, 900, 800
    kach = 2 * A.w(t, 1.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {shx:.0f} {shy:.0f})">'
                    f'<rect x="{shx:.0f}" y="{shy:.0f}" width="{shw}" height="{shh}" rx="10" fill="url(#derev)" {o(7)}/></g>')
    s += SL(Z_SRED, f'<rect x="{shx+20:.0f}" y="{shy+20:.0f}" width="{shw-40}" height="{shh*.32:.0f}" rx="6" fill="{KREM}" {o(4)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{shx+40+i*60:.0f}" y="{shy+40:.0f}" width="50" height="{shh*.26:.0f}" rx="4" fill="{(RUSH,TKAN,KREM,TKAN2)[i]}" {o(3)}/>')
    pw, ph_ = 760, 300
    px, py = shx + 60, shy + shh * .42
    vid = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw}" height="{ph_}" fill="{RUSH}"/>'
           f'<rect x="{px+40:.0f}" y="{py+40:.0f}" width="{pw-80}" height="80" fill="{KRAS}" opacity=".7"/>'
           f'<rect x="{px+40:.0f}" y="{py+150:.0f}" width="{pw-80}" height="80" fill="{KRAS}" opacity=".5"/>')
    put = kontur_proema(px, py, pw, ph_, "pryam")
    polka_s = f'<path d="{put}" fill="#1a140e"/>' + vid + mesto_stoka(px, py, pw, ph_, "pryam")
    polka_s += f'<path d="{put}" fill="none" {o(8)}/>'
    s += SL(Z_SRED, polka_s)
    s += SL(Z_SRED, f'<rect x="{shx+20:.0f}" y="{shy+shh*.74:.0f}" width="{shw-40}" height="{shh*.22:.0f}" rx="6" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{shx+40:.0f}" y="{shy+shh*.76:.0f}" width="140" height="50" rx="6" fill="#efe3c8" {o(3)}/>')
    tapn = A.out(A.seg(t, .3, .8))
    s += SL(Z_SRED, f'<ellipse cx="{shx+260:.0f}" cy="{shy+shh*.86-tapn*20:.0f}" rx="40" ry="18" fill="{TKAN}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{shx+330:.0f}" cy="{shy+shh*.86-tapn*20:.0f}" rx="40" ry="18" fill="{TKAN}" {o(3)}/>')
    for i, dx in enumerate((-30, 20, 60)):
        drop = ((t * .6 + i * .3) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{shx+120+dx:.0f}" cy="{shy+shh*.36+drop*40:.0f}" rx="6" ry="10" fill="#aee0ff" opacity="{1-drop:.2f}"/>')
    s += SL(Z_SRED, f'<rect x="{shx+20:.0f}" y="{shy+10:.0f}" width="140" height="70" rx="8" fill="{TKAN2}" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="{shx+90:.0f}" cy="{shy+44:.0f}" r="16" fill="{KREM}" opacity=".8"/>')
    s += SL(Z_SRED, lampa(260, 300, t, .8, True))
    s += SL(Z_SRED, _napolnenie(1460, 700, 380, 140, t, 28, 8))
    s += SL(Z_SRED, mebel_hlam(1440, 980, 300, t, 28))
    s += SL(Z_PERED, ramka_pp("levo", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 8, 5, .3, .5))
    s += vinetka(.4)
    return s


def polotence_na_vorotah_i_na_svadbe(t):
    """Кадр надвое: слева тесовые ворота с полотенцем в сумерках, справа
    светлая горница — жених и невеста держат каравай на том же узоре."""
    rnd = random.Random(415)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="960" height="{H}" fill="url(#nsumer)"/>')
    s += SL(Z_DAL, f'<rect x="960" y="0" width="960" height="{H}" fill="{KREM}"/>')
    s += SL(Z_DAL, pleten(0, 820, 900, 170, 7))
    vorx, vory = 300, 500
    s += SL(Z_SRED, dver(vorx, vory, 280, 480, .0, kruchok=False))
    kol = 3 * A.w(t, 1.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kol:.1f} {vorx+140:.0f} {vory+60:.0f})">'
                    f'<rect x="{vorx+100:.0f}" y="{vory+60:.0f}" width="80" height="220" rx="8" fill="{RUSH}" {o(4)}/>'
                    f'<rect x="{vorx+116:.0f}" y="{vory+90:.0f}" width="48" height="10" fill="{KRAS}"/></g>')
    s += SL(Z_SRED, f'<path d="M{vorx-60},{vory+420} q10,-130 -30,-160" fill="none" stroke="#5a4a3a" stroke-width="12" opacity=".7"/>')
    s += SL(Z_SRED, lavka(100, 920, 260))
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{620+i*20}" y="{700+i*10}" width="14" height="80" fill="#2a2e38" {o(2)}/>')
    s += SL(Z_SRED, okno_izby(1300, 300, 240, 220, t, svet=True, moroz=0, krest=True))
    s += SL(Z_SRED, teplo(1420, 420, 260, 220, .36))
    s += SL(Z_SRED, svecha(1500, 700, t, .2, .9))
    s += SL(Z_SRED, stol(1160, 760, 540, 34))
    s += SL(Z_SRED, f'<ellipse cx="1430" cy="780" rx="60" ry="30" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1410" y="740" width="40" height="60" fill="{ZHELEZ}" {o(3)}/>')
    karav_y = 740
    tow = f'<rect x="1150" y="{karav_y+10}" width="260" height="30" rx="6" fill="{RUSH}" {o(3)}/>'
    s += SL(Z_SRED, tow)
    s += SL(Z_SRED, karavay(1280, karav_y, 1.1, False))
    fata = 4 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, figura(1180, 980, 460, t, "#2a3a4a", "#efe3c8", False, .0))
    s += SL(Z_SRED, figura(1380, 980, 480, t, "#efe3c8", "#cfe4f5", True, .2))
    s += SL(Z_SRED, f'<g transform="rotate({fata:.1f} 1380 760)"><path d="M1340,740 q40,-60 80,0 l-10,120 h-60 Z"'
                    f' fill="#fff" opacity=".7" {o(3)}/></g>')
    kolyb = 6 * A.w(t, 1.4, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kolyb:.1f} 1700 920)">'
                    f'<path d="M1650,920 q50,-60 100,0 l0,60 h-100 Z" fill="url(#derev)" {o(4)}/>'
                    f'<ellipse cx="1700" cy="930" rx="30" ry="14" fill="#efe3c8" {o(3)}/></g>')
    s += SL(Z_SRED, siluet(700, 980, 300, "#2a2420", .5))
    s += SL(Z_SRED, siluet(780, 990, 280, "#2a2420", .5))
    s += SL(Z_SRED, f'<rect x="920" y="260" width="200" height="640" fill="{KAMEN2}" opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M920,260 h200 l-30,-60 h-140 Z" fill="{DOSKA2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="700" width="260" height="220" rx="8" fill="#5a3a2a" opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 1080, 100, t, 29, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .34))
    s += SL(Z_LETIT, mokryy_sneg(t, 8, 9, .3, .5))
    s += vinetka(.36)
    return s


def polotence_na_vesah(t):
    """На столе чашечные весы, на обеих чашах одинаковое вышитое полотенце;
    тучка под левой, солнышко под правой; весы ровно."""
    rnd = random.Random(416)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 11)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_DAL, okno_izby(1480, 160, 260, 220, t, svet=True, moroz=.3))
    s += SL(Z_SRED, teplo(1600, 280, 260, 220, .34))
    s += utvar_izby(80, 420, 360, t, 17)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="520" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="220" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, stol(660, 780, 680, 34))
    s += SL(Z_SRED, _vesy(960, 780, 1.9, t, 0, 3))
    for sgn in (-1, 1):
        cx_ = 960 + sgn * 195
        s += SL(Z_SRED, f'<rect x="{cx_-50:.0f}" y="595" width="100" height="18" rx="5" fill="{RUSH}" {o(3)}/>')
    mig = .5 + .4 * abs(A.w(t, 1.2))
    s += SL(Z_SRED, f'<ellipse cx="820" cy="540" rx="34" ry="18" fill="#9aa8b8" opacity="{mig:.2f}"/>')
    s += SL(Z_SRED, f'<circle cx="1100" cy="540" r="26" fill="{ZOL}" opacity="{1-mig*.5:.2f}"/>')
    s += SL(Z_SRED, svecha(760, 700, t, .1, 1.0))
    s += SL(Z_SRED, karavay(1200, 720, .8, True))
    s += SL(Z_SRED, f'<path d="M700,700 l20,-10 l20,30 l-30,10 Z" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1300,700 q-40,20 -20,60 q50,-10 50,-40 Z" fill="#efe3c8" opacity=".8" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="900" y="700" width="40" height="46" rx="6" fill="{CHUGUN}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="280" height="500" rx="10" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1170, 310, 1, 30, 130, 170))
    s += SL(Z_SRED, _napolnenie(420, 620, 1000, 140, t, 30, 8))
    s += SL(Z_SRED, mebel_hlam(760, 950, 260, t, 30))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 8, 4, .3, .5))
    s += vinetka(.4)
    return s


def ostroe_zhelezo_i_nechistaya_sila(t):
    """Стена сарая с острым инструментом на гвоздях; чертенята тянутся к
    остриям; дед снимает нож и заворачивает его в тряпицу."""
    rnd = random.Random(417)
    s = f'<rect width="{W}" height="{H}" fill="#2a2420"/>'
    s += nebo("sumer", t, False, 12)
    s += SL(Z_DAL, doski(0, 0, W, 800, 90, True, "dosk"))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="700" y="160" width="700" height="40" rx="8" fill="url(#derev)" {o(5)}/>')
    kosa_s = (f'<line x1="760" y1="200" x2="760" y2="420" stroke="url(#derev)" stroke-width="12"/>'
              f'<path d="M760,420 q100,20 140,-60 q-80,0 -140,60 Z" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, kosa_s)
    s += SL(Z_SRED, f'<line x1="900" y1="200" x2="900" y2="360" stroke="url(#zhel)" stroke-width="8"/>')
    s += SL(Z_SRED, f'<path d="M870,360 q30,40 60,0 q-30,-16 -60,0 Z" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M930,360 q30,40 60,0 q-30,-16 -60,0 Z" fill="{ZHELEZ}" {o(3)}/>')
    nozh_on = 1 - A.ease(A.seg(t, .6, .8))
    if nozh_on > .05:
        s += SL(Z_SRED, f'<line x1="1040" y1="200" x2="1040" y2="340" stroke="{ZHELEZ}" stroke-width="6" opacity="{nozh_on:.2f}"/>')
        s += SL(Z_SRED, f'<path d="M1010,340 h60 l-10,40 h-40 Z" fill="{ZHELEZ}" opacity="{nozh_on:.2f}" {o(3)}/>')
    s += SL(Z_SRED, f'<line x1="1140" y1="200" x2="1140" y2="320" stroke="url(#zhel)" stroke-width="6"/>')
    vily = f'<line x1="1240" y1="200" x2="1240" y2="440" stroke="url(#derev)" stroke-width="10"/>'
    for sgn in (-1, 0, 1):
        vily += f'<line x1="1240" y1="200" x2="{1240+sgn*20}" y2="140" stroke="{ZHELEZ}" stroke-width="7"/>'
    s += SL(Z_SRED, vily)
    for i in range(3):
        ph = i * .4
        s += SL(Z_SRED, _chertenok(560 - i * 60, 420 + i * 60, .9, t, ph))
    s += SL(Z_SRED, f'<rect x="60" y="640" width="420" height="140" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="620" cy="760" rx="60" ry="80" fill="#5a4a3a" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1500" y="700" width="140" height="180" rx="12" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M1500,780 h140" stroke="{ZHELEZ}" stroke-width="10"/>')
    s += SL(Z_SRED, lampa(1760, 480, t, .9, False))
    s += SL(Z_SRED, kot(300, 900, t, .9, "#2a2420"))
    s += SL(Z_SRED, figura(950, 1000, 520, t, "#3a2c3c", "#ffd98a", True, .0, tulup=True, boroda=True))
    zavyaz = A.ease(A.seg(t, .8, .6))
    r, (rx, ry) = rukav(1030, 760, 160, -70 + 40 * zavyaz, t, "#3a2c3c", "#ffd98a", .1)
    s += SL(Z_SRED, r)
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="24" ry="17" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 31, 3))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 31, 3))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += SL(Z_LETIT, dym(300, 900, t, 3, .2, 180, .3, "#cfd6de"))
    s += vinetka(.44)
    return s


def pustaya_krinka(t):
    """Пустая кринка лежит на боку на полке, паук в горлышке; полные соседи
    отодвигаются от неё."""
    rnd = random.Random(418)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 13)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="260" width="280" height="440" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN2, KREM, 32))
    s += SL(Z_SRED, f'<rect x="300" y="620" width="1320" height="40" rx="8" fill="url(#derev)" {o(6)}/>')
    otpolz = 10 * A.ease(A.seg(t, .6, 1.2))
    s += SL(Z_SRED, f'<g transform="translate({otpolz:.0f},0)"><path d="M700,620 q-10,-70 50,-76 q50,4 50,76 h-100 Z"'
                    f' fill="url(#glina)" {o(5)}/></g>')
    s += SL(Z_SRED, f'<g transform="translate({-otpolz:.0f},0)">')
    s += SL(Z_SRED, f'<ellipse cx="500" cy="590" rx="40" ry="34" fill="url(#med)" {o(4)}/>')
    s += SL(Z_SRED, karavay(420, 610, .7, True))
    s += SL(Z_SRED, f'</g>')
    s += SL(Z_SRED, f'<g transform="translate({otpolz:.0f},0)">')
    s += SL(Z_SRED, _banka(1000, 600, 1.1))
    s += SL(Z_SRED, f'<path d="M1100,600 l-10,-60 l50,10 l20,50 Z" fill="{ZOL}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1200" y="560" width="70" height="60" rx="8" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, '</g>')
    pauk_y = 4 * A.w(t, 2.2)
    s += SL(Z_SRED, f'<circle cx="{750+otpolz:.0f}" cy="{560+pauk_y:.0f}" r="10" fill="#1a1410"/>')
    for sgn in (-1, 1):
        s += SL(Z_SRED, f'<line x1="{750+otpolz:.0f}" y1="{560+pauk_y:.0f}" x2="{750+otpolz+sgn*16:.0f}" y2="{580+pauk_y:.0f}" stroke="#1a1410" stroke-width="2"/>')
    s += SL(Z_SRED, lampa(1700, 380, t, .85, True))
    s += SL(Z_SRED, utvar_izby(60, 420, 420, t, 21))
    s += utvar_pekarni(620, 900, 760, t, 9)
    s += SL(Z_SRED, f'<rect x="1140" y="260" width="260" height="420" rx="10" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(900, 600, 500, 150, t, 32, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 8, 5, .3, .5))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 19-26 ══════════════════════════════
def chasy_na_zapyaste(t):
    """Рукав пиджака с манжетой на пол-кадра: второй рукав застёгивает
    наручные часы на запястье. Видны только рукав и плечо."""
    rnd = random.Random(419)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 15)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += kvartira_veschi(1260, 700, 420, t, 16)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="480" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="200" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, _kovrik_pol(460, 900, 700, 110, TKAN, KREM, 33))
    s += SL(Z_SRED, stol(360, 780, 820, 34))
    s += SL(Z_SRED, lampa(1660, 420, t, .95, True))
    zastyog = A.ease(A.seg(t % 4.0, .4, 1.4))
    mx, my = 860, 660
    s += SL(Z_SRED, f'<path d="M{mx-120:.0f},{my+40:.0f} l240,-10 l-20,-150 l-220,10 Z" fill="#2a2e3c" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{mx-100:.0f},{my+20:.0f} l200,-6 l-8,-40 l-190,6 Z" fill="#fff" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{mx+40:.0f}" cy="{my-10:.0f}" rx="34" ry="20" fill="url(#zol)" {o(3)}/>')
    strap = (f'<path d="M{mx+70:.0f},{my-20:.0f} q{40*zastyog:.0f},{-10*zastyog:.0f} {70*zastyog:.0f},{-4*zastyog:.0f}"'
             f' fill="none" stroke="#5a3a26" stroke-width="16" stroke-linecap="round"/>')
    s += SL(Z_SRED, strap)
    r2, (r2x, r2y) = rukav(mx + 160, my - 60, 150, -160 + 20 * A.w(t, 1.6), t, "#2a2e3c", "#cfe4f5", .2, nichya=True)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="24" ry="17" fill="#2a2e3c" {o(4)}/>')
    s += SL(Z_SRED, _chasy_karman(500, 700, 1.0, t, 1.0))
    s += SL(Z_SRED, f'<rect x="300" y="700" width="60" height="70" rx="8" fill="#1a1c22" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1000" y="730" width="140" height="18" rx="4" fill="{KREM}" {o(3)}/>')
    gaz = 3 * A.w(t, 1.7, .2)
    s += SL(Z_SRED, f'<g transform="rotate({gaz:.1f} 1120 720)"><rect x="1050" y="690" width="140" height="90" fill="#e8e2d0" {o(3)}/></g>')
    s += SL(Z_SRED, f'<ellipse cx="1280" cy="760" rx="32" ry="20" fill="#cfe4f5" opacity=".6" {o(3)}/>')
    s += SL(Z_SRED, par(1280, 740, t, 3, .4, 120, .5))
    s += SL(Z_SRED, _napolnenie(900, 580, 450, 150, t, 33, 6))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1170, 310, 2, 34, 100, 130))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def hodiki_i_budilnik(t):
    """Стенные часы с кукушкой и гирями-шишками, под ними будильник на
    тумбочке; над обоими загорается галочка."""
    rnd = random.Random(420)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 16)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += kvartira_veschi(80, 720, 420, t, 18)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, _kovrik_pol(460, 900, 700, 110, TKAN, KREM, 20))
    cx, cy = 900, 420
    kuk_on = ((t * 1.4) % 3.0) < .8
    s += SL(Z_SRED, f'<rect x="{cx-100:.0f}" y="{cy-280:.0f}" width="200" height="500" rx="14" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="{cx-50:.0f}" y="{cy-80:.0f}" width="100" height="{40 if kuk_on else 6:.0f}" rx="6" fill="{KREM}" {o(3)}/>')
    if kuk_on:
        s += SL(Z_SRED, f'<ellipse cx="{cx:.0f}" cy="{cy-60:.0f}" rx="18" ry="14" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, _chasy_sten(cx, cy + 40, 1.1, t))
    for sgn, ph in ((-1, 0), (1, .5)):
        gy = cy + 180 + 30 * A.w(t, .6, ph) * .3
        s += SL(Z_SRED, f'<line x1="{cx+sgn*30:.0f}" y1="{cy+90:.0f}" x2="{cx+sgn*30:.0f}" y2="{gy:.0f}" stroke="#5a3a26" stroke-width="4"/>')
        s += SL(Z_SRED, f'<ellipse cx="{cx+sgn*30:.0f}" cy="{gy:.0f}" rx="18" ry="24" fill="#6b4428" {o(4)}/>')
    tumba_x, tumba_y = 820, 700
    s += SL(Z_SRED, f'<rect x="{tumba_x:.0f}" y="{tumba_y:.0f}" width="220" height="200" rx="10" fill="url(#derev)" {o(6)}/>')
    bud_bounce = 6 * A.ease(A.seg(t % 1.0, .0, .2))
    s += SL(Z_SRED, f'<g transform="translate(0,{-bud_bounce:.0f})">'
                    f'<circle cx="{tumba_x+110:.0f}" cy="{tumba_y-20:.0f}" r="60" fill="url(#zhel)" {o(5)}/>'
                    f'<circle cx="{tumba_x+40:.0f}" cy="{tumba_y-70:.0f}" r="20" fill="{ZHELEZ}" {o(3)}/>'
                    f'<circle cx="{tumba_x+180:.0f}" cy="{tumba_y-70:.0f}" r="20" fill="{ZHELEZ}" {o(3)}/></g>')
    s += SL(Z_SRED, _galochka(cx + 140, cy - 160, 1.1, t, .0))
    s += SL(Z_SRED, _galochka(tumba_x + 110, tumba_y - 140, 1.0, t, .4))
    s += SL(Z_SRED, lampa(1660, 420, t, .9, True))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="280" height="500" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1170, 310, 2, 34, 100, 130))
    s += SL(Z_SRED, f'<path d="M1500,900 q-20,-200 0,-260 q20,60 0,260 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1180" y="860" width="320" height="30" rx="8" fill="{RUSH}" {o(4)}/>')
    s += SL(Z_SRED, _napolnenie(1140, 600, 350, 150, t, 34, 6))
    s += mebel_hlam(500, 850, 300, t, 34)
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 6, .25, .5))
    s += vinetka(.4)
    return s


def sem_podarkov_na_servante(t):
    """Сервант с семью коробками: бабушка ставит седьмую, номера загораются
    по очереди; над сервантом по ходу времени встают карточки главы."""
    rnd = random.Random(421)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 17)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _servant(360, 300, 1300, 480, t))
    boxcols = ((TKAN, ZOL), (TKAN2, SVET), (ZEL2, KREM), (MED, ZOL), (KAMEN2, SVET), ("#5a3a4a", ZOL), ("#2e3a4a", SVET))
    postav = A.ease(A.seg(t, .2, 1.0))
    for i in range(7):
        bx = 420 + i * 150
        by = 700 - (30 if i == 6 else 0) * (1 - postav)
        col, lenta = boxcols[i]
        s += SL(Z_SRED, _korobka(bx, by, 120, 100, t, col, lenta, True, .0, i * .3))
        on = (t % 9.0) > i * 1.1
        if on:
            s += SL(Z_SRED, f'<circle cx="{bx+60:.0f}" cy="{by-20:.0f}" r="14" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="300" cy="420" rx="40" ry="90" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, hodiki(1500, 380, t, 1.0))
    s += SL(Z_SRED, svecha(1300, 700, t, .2, 1.0))
    s += SL(Z_SRED, f'<rect x="1300" y="520" width="140" height="22" rx="5" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1600,700 l-16,-120 l40,20 l16,100 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1680" cy="720" rx="60" ry="24" fill="url(#med)" {o(4)}/>')
    kart = (t % 9.0) > 4.0
    if kart:
        kpop = A.out(A.seg((t % 9.0) % 4.0, .0, .6))
        s += SL(Z_SRED, f'<g transform="translate(0,{(1-kpop)*40:.0f})">'
                        f'<rect x="760" y="140" width="240" height="140" rx="10" fill="#fff" opacity=".92" {o(4)}/></g>')
    s += SL(Z_SRED, figura(1140, 940, 540, t, "#3a2c3c", "#ffd98a", True, .0))
    r, (rx, ry) = rukav(1260, 650, 150, -60 + 10 * A.w(t, 1.8), t, "#3a2c3c", "#ffd98a", .1)
    s += SL(Z_SRED, r)
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="24" ry="17" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 35, 3))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 35, 3))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def chasy_v_krasnoy_korobke(t):
    """Красная лаковая коробка с настольными часами на шёлке; старик обеими
    руками отодвигает её; два облачка сходятся знаком равенства."""
    rnd = random.Random(422)
    s = f'<rect width="{W}" height="{H}" fill="#4a2e26"/>'
    s += nebo("sumer", t, False, 18)
    s += SL(Z_DAL, f'<rect x="0" y="40" width="{W}" height="760" fill="#5a3630" {o(5)}/>')
    s += SL(Z_SRED, lampa(960, 180, t, 1.1, True))
    s += SL(Z_SRED, teplo(960, 420, 260, 220, .4))
    s += SL(Z_SRED, f'<rect x="420" y="300" width="280" height="420" rx="10" fill="#6b4428" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="320" width="240" height="180" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 120, "#8a2a2a", ZOL, 22))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="500" y="680" width="900" height="40" rx="8" fill="url(#derev)" {o(6)}/>')
    otodv = -40 * A.ease(A.seg(t, .3, 1.0))
    box = f'<rect x="700" y="580" width="260" height="100" rx="10" fill="{KRAS}" {o(6)}/>'
    box += f'<ellipse cx="830" cy="610" rx="20" ry="30" fill="url(#zol)" {o(3)}/>'
    box += _chasy_sten(830, 610, .6, t)
    s += SL(Z_SRED, f'<g transform="translate({otodv:.0f},0)">{box}</g>')
    stage = A.seg(t, 1.2, 1.5)
    s += SL(Z_SRED, _oblachko(660, 420 - 60 * stage, .8, t, .1, "chasy"))
    s += SL(Z_SRED, _oblachko(1080, 420 - 60 * stage, .8, t, .3, "doroga"))
    if stage > .9:
        s += SL(Z_SRED, _oblachko(870, 400, .6, t, .0, "ravno"))
    s += SL(Z_SRED, f'<rect x="1300" y="620" width="160" height="90" rx="14" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1380" cy="600" rx="70" ry="16" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1380" cy="640" rx="36" ry="24" fill="url(#med)" {o(3)}/>')
    fen_sw = 5 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<g transform="rotate({fen_sw:.1f} 300 500)">'
                    f'<ellipse cx="300" cy="500" rx="60" ry="100" fill="{KRAS}" opacity=".85" {o(4)}/></g>')
    s += SL(Z_SRED, dym(430, 660, t, 3, .3, 160, .4, "#dde4ec"))
    s += SL(Z_SRED, f'<path d="M1550,700 l-10,-90 l30,10 l12,80 Z" fill="#8a2a2a" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M1500,560 q60,-30 110,0 q-20,30 -110,0 Z" fill="none" stroke="{ZOL}" stroke-width="3" opacity=".7"/>')
    s += SL(Z_SRED, figura(930, 980, 480, t, "#3a2420", "#d6a63f", False, .0, tulup=True, naklon=4))
    push1 = A.ease(A.seg(t, .3, 1.0))
    r1, (r1x, r1y) = rukav(830, 760, 140, -170 - 20 * push1, t, "#3a2420", "#d6a63f", .1)
    r2, (r2x, r2y) = rukav(1030, 760, 140, -10 + 20 * push1, t, "#3a2420", "#d6a63f", .3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="22" ry="9" fill="#d6a63f" opacity=".5"/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="22" ry="9" fill="#d6a63f" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="300" width="260" height="380" rx="10" fill="#6b4428" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(420, 620, 1080, 140, t, 36, 7))
    s += SL(Z_PERED, ramka_pp("oba", "#120a0a", .44))
    s += vinetka(.42)
    return s


def muzh_zhena_i_korobochka_s_chasami(t):
    """Муж держит коробочку с часами на ладони, жена закрывает щёки и
    качает головой у круглого стола."""
    rnd = random.Random(423)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 19)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _elka(1400, 940, 640, t, 11, True))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="500" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="210" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN2, KREM, 23))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="820" rx="340" ry="60" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="772" width="400" height="30" rx="8" fill="#fff" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, _korobka(900, 740, 120, 80, t, KREM, TKAN, True, .2, .1))
    for i in range(3):
        s += SL(Z_SRED, f'<circle cx="{480+i*110}" cy="820" r="26" fill="{KREM}" opacity=".7"/>')
    s += SL(Z_SRED, hodiki(1700, 420, t, .9))
    s += SL(Z_SRED, svecha(1500, 740, t, .2, .9))
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="700" rx="60" ry="26" fill="{KAMEN2}" {o(4)}/>')
    s += SL(Z_SRED, figura(760, 1000, 500, t, "#3a3028", "#efe3c8", False, .0))
    podn = A.out(A.seg(t % 3.0, .2, .6))
    r1, (r1x, r1y) = rukav(840, 780, 150, -40 + 10 * podn, t, "#3a3028", "#efe3c8", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="26" ry="18" fill="#3a3028" {o(4)}/>')
    s += SL(Z_SRED, _korobka(r1x - 10, r1y - 30, 70, 50, t, KREM, ZOL, True, .3, .2))
    s += SL(Z_SRED, figura(1160, 1000, 500, t, "#7a2a44", "#ffe2a8", False, .3))
    kiv = 6 * A.w(t, 1.6, .3)
    r2a, (r2ax, r2ay) = rukav(1110, 820, 130, -150 + kiv, t, "#7a2a44", "#ffe2a8", .2)
    r2b, (r2bx, r2by) = rukav(1210, 820, 130, -30 - kiv, t, "#7a2a44", "#ffe2a8", .4)
    s += SL(Z_SRED, r2a + r2b)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="24" ry="17" fill="#7a2a44" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2bx:.0f}" cy="{r2by:.0f}" rx="24" ry="17" fill="#7a2a44" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(900, 580, 450, 170, t, 37, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def monetka_za_chasy(t):
    """Тот же стол: часы уже на запястье жены, она кладёт монетку мужу на
    ладонь и слушает ход у самого уха."""
    rnd = random.Random(424)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 20)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="460" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="200" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, hodiki(1420, 360, t, .95))
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN2, KREM, 24))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="820" rx="340" ry="60" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="772" width="400" height="30" rx="8" fill="#fff" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, _korobka(1060, 750, 110, 80, t, KREM, TKAN, True, .4, .1))
    s += SL(Z_SRED, f'<ellipse cx="880" cy="800" rx="70" ry="30" fill="url(#med)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="780" width="60" height="50" rx="8" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1300" cy="800" rx="30" ry="16" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, svecha(1400, 740, t, .2, 1.0))
    s += SL(Z_SRED, f'<circle cx="1200" cy="800" r="20" fill="{ORA}" {o(3)}/>')
    s += SL(Z_SRED, figura(760, 1000, 500, t, "#3a3028", "#efe3c8", False, .0))
    s += SL(Z_SRED, figura(1160, 1000, 500, t, "#7a2a44", "#ffe2a8", False, .3))
    moneta = A.out(A.seg(t % 3.0, .2, .5))
    r1, (r1x, r1y) = rukav(840, 780, 150, -40, t, "#3a3028", "#efe3c8", .1)
    s += SL(Z_SRED, r1)
    # кисть не рисуем — работает сама монетка, лежащая на обшлаге рукава
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="20" ry="8" fill="#efe3c8" opacity=".5"/>')
    s += SL(Z_SRED, f'<circle cx="{r1x:.0f}" cy="{r1y-10-10*moneta:.0f}" r="14" fill="url(#med)" {o(2)}/>')
    r2a, (r2ax, r2ay) = rukav(1090, 800, 140, -150, t, "#7a2a44", "#ffe2a8", .2)
    r2b, (r2bx, r2by) = rukav(1230, 740, 120, -90, t, "#7a2a44", "#ffe2a8", .4)
    s += SL(Z_SRED, r2a + r2b)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="18" ry="7" fill="#ffe2a8" opacity=".5"/>')
    s += SL(Z_SRED, _chasy_karman(r2bx, r2by, .42, t, 1.0))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(900, 580, 450, 150, t, 38, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def podarki_vnuku_i_dedu(t):
    """Диван под ёлкой: внук с детскими часами, дед застёгивает свои часы,
    бабушка между ними держит блюдце с двумя монетками."""
    rnd = random.Random(425)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 21)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, _elka(240, 940, 560, t, 13, True))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="460" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(450, 310, 2, 25, 90, 120))
    s += SL(Z_SRED, f'<rect x="560" y="760" width="1240" height="220" rx="30" fill="{TKAN2}" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="620" cy="780" rx="60" ry="30" fill="{KREM}" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, figura(640, 980, 400, t, "#3a5a7a", "#ffe2a8", False, .0))
    ekr = .6 + .4 * abs(A.w(t, 2.2))
    s += SL(Z_SRED, f'<rect x="580" y="900" width="60" height="40" rx="6" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="590" y="908" width="40" height="24" rx="3" fill="{SVET}" opacity="{ekr:.2f}"/>')
    s += SL(Z_SRED, lampa(1760, 420, t, .85, True))
    s += SL(Z_SRED, figura(1300, 1000, 540, t, "#2c3a2c", "#ffd98a", False, .4, boroda=True))
    zastyog = A.ease(A.seg(t % 3.0, .3, 1.0))
    r1, (r1x, r1y) = rukav(1388, 700, 170, -150 + 20 * zastyog, t, "#2c3a2c", "#ffd98a", .2)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="24" ry="17" fill="#2c3a2c" {o(4)}/>')
    s += SL(Z_SRED, figura(970, 1010, 480, t, "#3a2c3c", "#ffd98a", True, .2))
    r2, (r2x, r2y) = rukav(1040, 750, 120, -30, t, "#3a2c3c", "#ffd98a", .3)
    r3, (r3x, r3y) = rukav(895, 720, 90, -80, t, "#3a2c3c", "#ffd98a", .5)
    s += SL(Z_SRED, r2 + r3)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="24" ry="17" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y-6:.0f}" rx="40" ry="16" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{r2x-14:.0f}" cy="{r2y-10:.0f}" r="9" fill="url(#med)" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r3x:.0f}" cy="{r3y:.0f}" rx="20" ry="14" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, kot(1620, 920, t, .9, "#3b3430"))
    s += SL(Z_SRED, _napolnenie(900, 580, 450, 170, t, 39, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def nagradnye_chasy(t):
    """Заводской красный уголок: директор обеими руками подаёт футляр с
    карманными часами, рабочий принимает и прижимает кепку к груди."""
    rnd = random.Random(426)
    s = f'<rect width="{W}" height="{H}" fill="#5a3a2e"/>'
    s += nebo("sumer", t, False, 22)
    s += SL(Z_DAL, f'<rect x="0" y="40" width="{W}" height="760" fill="#6a4536" {o(5)}/>')
    s += SL(Z_SRED, teplo(960, 420, 260, 220, .4))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="440" rx="10" fill="#5a3a2a" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(450, 310, 2, 26, 100, 140))
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 120, KRAS, ZOL, 26))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="700" y="640" width="900" height="40" rx="8" fill="{KRAS}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="600" width="200" height="60" rx="8" fill="{KAMEN2}" {o(4)}/>')
    stopka = 4
    for i in range(stopka):
        s += SL(Z_SRED, f'<rect x="{1020+i*4:.0f}" y="{620-i*12:.0f}" width="160" height="16" rx="3" fill="{KREM}" {o(3)}/>')
    znam_sw = 5 * A.w(t, 1.4)
    s += SL(Z_SRED, f'<line x1="200" y1="160" x2="200" y2="700" stroke="url(#derev)" stroke-width="12"/>')
    s += SL(Z_SRED, f'<g transform="rotate({znam_sw:.1f} 200 200)"><path d="M200,180 h260 l-30,220 h-230 Z" fill="{KRAS}" opacity=".9" {o(5)}/></g>')
    s += SL(Z_SRED, f'<rect x="1400" y="260" width="320" height="220" rx="10" fill="{KAMEN2}" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<ellipse cx="{1460+i*100:.0f}" cy="360" rx="36" ry="46" fill="#2a2420" opacity=".7" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M900,700 l-20,-150 l50,20 l20,130 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, lampa(1700, 420, t, .85, False))
    peredacha = A.ease(A.seg(t, .3, 1.5))
    futl_x = 860 + 160 * peredacha
    futl = f'<rect x="{futl_x:.0f}" y="560" width="140" height="80" rx="10" fill="{KAMEN2}" {o(6)}/>'
    glow = .5 + .5 * abs(A.w(t, 1.4))
    futl += f'<circle cx="{futl_x+70:.0f}" cy="600" r="30" fill="{ZOL}" opacity="{glow:.2f}" {o(3)}/>'
    s += SL(Z_SRED, futl)
    s += SL(Z_SRED, figura(700, 1000, 520, t, "#2a2a3a", "#d6d0c0", False, .0))
    r1a, (r1ax, r1ay) = rukav(790, 780, 140, -10, t, "#2a2a3a", "#d6d0c0", .1)
    r1b, (r1bx, r1by) = rukav(950, 780, 110, -60, t, "#2a2a3a", "#d6d0c0", .3)
    s += SL(Z_SRED, r1a + r1b)
    s += SL(Z_SRED, f'<ellipse cx="{r1ax:.0f}" cy="{r1ay:.0f}" rx="24" ry="17" fill="#2a2a3a" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r1bx:.0f}" cy="{r1by:.0f}" rx="22" ry="15" fill="#2a2a3a" {o(4)}/>')
    s += SL(Z_SRED, figura(1260, 1000, 520, t, "#3a3a2c", "#d6a63f", False, .2, boroda=True))
    r2a, (r2ax, r2ay) = rukav(1180, 780, 130, -170, t, "#3a3a2c", "#d6a63f", .2)
    s += SL(Z_SRED, r2a)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="24" ry="17" fill="#3a3a2c" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1310" cy="880" rx="60" ry="30" fill="#4a3a2c" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 40, 4))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 40, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120a0a", .44))
    s += vinetka(.42)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 27-34 ══════════════════════════════
def otcovskie_chasy_na_tumbochke(t):
    """Мостик в память. Тумбочка у кровати: часы, очки, газета, стакан с
    ложкой; над тумбочкой увеличительное стекло — проём под часовой
    механизм. Отец крутит заводную головку своих часов."""
    rnd = random.Random(427)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 23)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += kvartira_veschi(1300, 700, 400, t, 20)
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="580" rx="14" fill="{TKAN2}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="60" y="860" width="640" height="160" rx="14" fill="{TKAN2}" {o(6)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<ellipse cx="{160+i*140:.0f}" cy="880" rx="70" ry="30" fill="{KREM}" opacity=".85" {o(3)}/>')
    tx, ty = 820, 680
    s += SL(Z_SRED, f'<rect x="{tx:.0f}" y="{ty:.0f}" width="260" height="280" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{tx+20:.0f}" y="{ty+20:.0f}" width="220" height="16" rx="4" fill="#efe3c8" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{tx+20:.0f}" y="{ty+56:.0f}" width="80" height="60" fill="#1a1c22" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{tx+160:.0f}" cy="{ty+90:.0f}" rx="30" ry="34" fill="#cfe4f5" opacity=".6" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{tx+150:.0f}" y="{ty+70:.0f}" width="12" height="40" rx="4" fill="{K}" {o(2)}/>')
    gaz = A.ease(A.seg(t, .5, 2.0)) * 20
    s += SL(Z_SRED, f'<rect x="{tx+20:.0f}" y="{ty+80+gaz:.0f}" width="150" height="100" fill="#e8e2d0" {o(3)}/>')
    s += SL(Z_SRED, lampa(tx + 230, ty - 40, t, .85, False))
    px, py, pr = tx + 40, ty - 220, 190
    vid = (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr:.0f}" fill="#cfd6de"/>'
           f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr*.6:.0f}" fill="none" stroke="{K}" stroke-width="2"/>')
    mech_a = (t * 160) % 360
    vid += f'<circle cx="{px-20:.0f}" cy="{py:.0f}" r="40" fill="url(#zol)" {o(2)}/>'
    vid += f'<g transform="rotate({mech_a:.1f} {px-20:.0f} {py:.0f})"><line x1="{px-20:.0f}" y1="{py:.0f}" x2="{px-20:.0f}" y2="{py-30:.0f}" stroke="{K}" stroke-width="3"/></g>'
    vid += f'<circle cx="{px+40:.0f}" cy="{py+10:.0f}" r="26" fill="{ZHELEZ}" {o(2)}/>'
    lupa = f'<rect x="{px-10:.0f}" y="{py+pr-10:.0f}" width="20" height="90" fill="url(#zhel)" {o(5)}/>'
    put = kontur_proema(px - pr, py - pr, pr * 2, pr * 2, "ellips")
    sten = lupa + f'<path d="{put}" fill="#1a140e"/>' + vid + mesto_stoka(px - pr, py - pr, pr * 2, pr * 2, "ellips")
    sten += f'<path d="{put}" fill="none" {o(10)}/>'
    s += SL(Z_SRED, sten)
    s += SL(Z_SRED, figura(600, 1010, 480, t, "#efe3c8", "#cfe4f5", False, .0))
    krut = (t * 300) % 360
    r, (rx, ry) = rukav(680, 820, 130, -20, t, "#efe3c8", "#cfe4f5", .1)
    s += SL(Z_SRED, r)
    s += SL(Z_SRED, f'<g transform="rotate({krut:.1f} {rx:.0f} {ry:.0f})"><ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="22" ry="16" fill="#efe3c8" {o(4)}/></g>')
    s += SL(Z_SRED, f'<ellipse cx="500" cy="920" rx="80" ry="30" fill="#5a3a26" opacity=".5" {o(2)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 41, 5))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 41, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def chasy_iz_vitriny_dlya_sebya(t):
    """Витрина часового отдела: покупательница прикладывает часы к
    запястью и смотрит в зеркало, довольная; продавец за прилавком."""
    rnd = random.Random(428)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 24)
    s += SL(Z_DAL, f'<rect x="0" y="40" width="{W}" height="760" fill="{KAMEN2}" opacity=".6" {o(5)}/>')
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="300" y="620" width="1300" height="160" rx="10" fill="url(#stekl)" opacity=".5" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="760" width="1300" height="200" fill="#3a3028" {o(6)}/>')
    rnd2 = random.Random(7)
    for i in range(9):
        wx = 340 + i * 140
        kind = i % 3
        if kind == 0:
            s += SL(Z_SRED, _chasy_karman(wx, 700, .55, t, 1.0))
        elif kind == 1:
            s += SL(Z_SRED, f'<circle cx="{wx:.0f}" cy="700" r="30" fill="url(#med)" {o(3)}/>')
        else:
            s += SL(Z_SRED, f'<ellipse cx="{wx:.0f}" cy="700" rx="34" ry="14" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="900" y="260" width="300" height="360" rx="8" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _chasy_sten(1050, 420, 1.0, t))
    s += SL(Z_SRED, f'<rect x="1400" y="250" width="280" height="370" rx="8" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1430, 280, 2, 24, 100, 140))
    s += SL(Z_SRED, f'<rect x="1500" y="700" width="200" height="30" rx="6" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="340" rx="8" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="220" height="140" rx="4" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    galka_on = ((t * .8) % 3.0) > 1.6
    if galka_on:
        s += SL(Z_SRED, _galochka(900, 480, 1.2, t))
    s += SL(Z_SRED, figura(560, 1000, 520, t, "#2a2e3c", "#cfe4f5", False, .0))
    s += SL(Z_SRED, f'<rect x="490" y="840" width="140" height="60" rx="8" fill="{KREM}" opacity=".7" {o(3)}/>')
    s += SL(Z_SRED, figura(1140, 1010, 500, t, "#3a3028", "#9aa0a4", False, .2, shapka=False))
    prikl = A.ease(A.seg(t % 4.0, .3, 1.0))
    r, (rx, ry) = rukav(1220, 840, 140, -100 - 30 * prikl, t, "#3a3028", "#9aa0a4", .1)
    s += SL(Z_SRED, r)
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="24" ry="17" fill="#3a3028" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="{rx:.0f}" cy="{ry-6:.0f}" r="16" fill="url(#med)" {o(2)}/>')
    s += SL(Z_SRED, svecha(260, 680, t, .2, .8))
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 42, 4))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 42, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.4)
    return s


def ostroe_na_barhate(t):
    """Футляр на бархате: нож, ножницы, вилка, булавка вспыхивают по
    словам; запрещающая черта нависает над ним. Людей нет."""
    rnd = random.Random(429)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 25)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += utvar_izby(1240, 420, 380, t, 23)
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="420" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(450, 310, 1, 29, 110, 150))
    s += SL(Z_SRED, f'<rect x="500" y="680" width="900" height="40" rx="8" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="560" y="600" width="780" height="90" rx="12" fill="#2a1414" {o(6)}/>')
    items = (("nozh", 640), ("nozhnicy", 840), ("vilka", 1040), ("bulavka", 1240))
    for i, (kind, ix) in enumerate(items):
        on = (t % 4.0) > i * .9
        op = .3 + .7 * (1 if on else 0)
        if kind == "nozh":
            s += SL(Z_SRED, f'<g opacity="{op:.2f}"><path d="M{ix-50:.0f},630 l100,-6 l-14,16 l-86,4 Z" fill="{ZHELEZ}" {o(3)}/>'
                            f'<rect x="{ix+40:.0f}" y="624" width="40" height="16" rx="4" fill="#5a3a26" {o(2)}/></g>')
        elif kind == "nozhnicy":
            s += SL(Z_SRED, f'<g opacity="{op:.2f}"><path d="M{ix-30:.0f},610 l50,40 M{ix+20:.0f},610 l-50,40" stroke="{ZHELEZ}" stroke-width="8"/>'
                            f'<circle cx="{ix-5:.0f}" cy="630" r="7" fill="{ZHELEZ}"/></g>')
        elif kind == "vilka":
            s += SL(Z_SRED, f'<g opacity="{op:.2f}">')
            for j in range(3):
                s += SL(Z_SRED, f'<line x1="{ix-16+j*16:.0f}" y1="610" x2="{ix-16+j*16:.0f}" y2="650" stroke="{ZHELEZ}" stroke-width="6"/>')
            s += SL(Z_SRED, '</g>')
        else:
            s += SL(Z_SRED, f'<g opacity="{op:.2f}"><line x1="{ix:.0f}" y1="610" x2="{ix:.0f}" y2="650" stroke="{ZHELEZ}" stroke-width="4"/>'
                            f'<circle cx="{ix:.0f}" cy="608" r="8" fill="{KRAS}"/></g>')
    cherta_y = 480 + 140 * A.ease(A.seg(t, .6, 1.4))
    s += SL(Z_SRED, _zapret(950, cherta_y, 220, t))
    s += SL(Z_SRED, f'<rect x="300" y="700" width="160" height="30" rx="6" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1400" y="700" width="120" height="110" rx="10" fill="{TKAN}" opacity=".8" {o(4)}/>')
    bant_sw = 3 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<g transform="rotate({bant_sw:.1f} 1460 740)"><circle cx="1460" cy="740" r="18" fill="{ZOL}" {o(3)}/></g>')
    s += SL(Z_SRED, f'<path d="M600,720 l-16,-110 l40,20 l16,90 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, svecha(1600, 680, t, .3, 1.0))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN2, KREM, 43))
    s += SL(Z_SRED, _napolnenie(420, 600, 1080, 100, t, 43, 7))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .42))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.44)
    return s


def nozh_na_razdelochnoy_doske(t):
    """Кухонный стол: нож на доске, мать поднимает его выше, мальчик
    прячет руки за спину."""
    rnd = random.Random(430)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("den", t, False, 26)
    s += SL(Z_DAL, doski(0, 0, W, 760, 70, False, "dosk"))
    s += kvartira_veschi(1260, 700, 380, t, 25)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, stol(460, 780, 900, 36))
    s += SL(Z_SRED, f'<rect x="700" y="740" width="320" height="24" rx="6" fill="url(#dosk)" {o(5)}/>')
    s += SL(Z_SRED, karavay(640, 740, .7, False))
    podn = A.out(A.seg(t % 3.0, .3, .6))
    s += SL(Z_SRED, f'<ellipse cx="560" cy="760" rx="34" ry="30" fill="#b5803a" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1100" cy="760" rx="36" ry="30" fill="{KRAS}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1180" y="760" width="90" height="20" rx="5" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1280" cy="790" r="26" fill="#efe3c8" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="800" rx="46" ry="40" fill="{CHUGUN}" {o(4)}/>')
    укроп_sw = 4 * A.w(t, 2.2)
    s += SL(Z_SRED, f'<g transform="rotate({укроп_sw:.1f} 1000 790)"><path d="M1000,790 l0,-50" stroke="{ZEL}" stroke-width="5"/>'
                    f'<path d="M1000,750 q-14,-10 -24,-4 M1000,750 q14,-10 24,-4" fill="none" stroke="{ZEL}" stroke-width="3"/></g>')
    s += SL(Z_SRED, figura(560, 1010, 500, t, "#efe3c8", "#9c7049", False, .0))
    # кисть не рисуем: рукав оканчивается обшлагом прямо на рукояти ножа —
    # нож рисуется ПОСЛЕ рукава, на его же конце (R-0051, его слово 15.11)
    r1, (r1x, r1y) = rukav(640, 700, 150, -70 + 10 * podn, t, "#efe3c8", "#9c7049", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="18" ry="7" fill="#9c7049" opacity=".6"/>')
    s += SL(Z_SRED, _nozh_bolshoy(r1x, r1y, 280, t, 0))
    r2, (r2x, r2y) = rukav(480, 780, 120, -150, t, "#efe3c8", "#9c7049", .3)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="18" ry="7" fill="#9c7049" opacity=".6"/>')
    s += SL(Z_SRED, figura(1420, 1030, 320, t, "#2a4a6a", "#efe3c8", False, .3, naklon=-4))
    s += SL(Z_SRED, lampa(1700, 420, t, .9, True))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="420" rx="8" fill="{KAMEN2}" {o(5)}/>')
    s += SL(Z_SRED, _kovrik_pol(500, 900, 760, 110, TKAN2, KREM, 44))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="240" height="420" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1156" y="300" width="208" height="180" rx="5" fill="url(#stekl)" opacity=".5" {o(3)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 760, 150, t, 44, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.36)
    return s


def nozhnicy_za_kopeyku(t):
    """Швейный столик: новые ножницы с бантом придвигаются подруге;
    портниха кладёт на стол монетку. Ярлык «продано» загорается."""
    rnd = random.Random(431)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 27)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_DAL, okno_izby(1500, 160, 260, 220, t, svet=True, moroz=.3))
    s += SL(Z_SRED, teplo(1620, 280, 260, 220, .34))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="460" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="200" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN, KREM, 31))
    s += SL(Z_SRED, stol(560, 780, 800, 34))
    s += SL(Z_SRED, f'<rect x="620" y="740" width="200" height="90" rx="10" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="680" cy="800" r="26" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="770" rx="40" ry="22" fill="{TKAN}" {o(4)}/>')
    rnd2 = random.Random(3)
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{880+ (i%3)*22-22:.0f}" cy="{760+(i//3)*16:.0f}" r="3" fill="{ZHELEZ}"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<ellipse cx="{1050+i*40:.0f}" cy="770" rx="24" ry="30" fill="{(TKAN2,ZEL2,KREM)[i]}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1200" y="750" width="120" height="70" rx="6" fill="{RUSH}" opacity=".85" {o(3)}/>')
    pridv = A.ease(A.seg(t, .3, .9))
    nx = 780 + 140 * pridv
    s += SL(Z_SRED, f'<path d="M{nx-30:.0f},740 l50,40 M{nx+20:.0f},740 l-50,40" stroke="{ZHELEZ}" stroke-width="7"/>')
    s += SL(Z_SRED, f'<circle cx="{nx-5:.0f}" cy="760" r="20" fill="{KRAS}" {o(3)}/>')
    sant = 6 * A.w(t, 1.5)
    s += SL(Z_SRED, f'<path d="M700,740 q{sant:.0f},40 0,90" fill="none" stroke="{KREM}" stroke-width="8"/>')
    moneta = A.out(A.seg(t, 1.2, .6))
    s += SL(Z_SRED, f'<circle cx="1180" cy="{800-10*moneta:.0f}" r="16" fill="url(#med)" {o(2)}/>')
    yarl_on = (t % 4.0) > 2.2
    if yarl_on:
        s += SL(Z_SRED, f'<rect x="1300" y="680" width="70" height="40" rx="6" fill="{ZOL}" {o(3)}/>')
    s += SL(Z_SRED, figura(720, 1000, 440, t, "#3a3028", "#9aa0a4", False, .0))
    s += SL(Z_SRED, figura(1240, 1000, 440, t, "#7a2a44", "#ffe2a8", False, .2))
    r2, (r2x, r2y) = rukav(1160, 820, 110, -170, t, "#7a2a44", "#ffe2a8", .3)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="22" ry="15" fill="#7a2a44" {o(4)}/>')
    s += SL(Z_SRED, svecha(960, 700, t, .2, .9))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 1080, 100, t, 45, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.4)
    return s


def nabor_nozhey_dlya_docheri(t):
    """Современная кухня: коробка ножей, подставка едет к дочери за
    монетку; в проёме открытой дверцы шкафчика — настоящая нарезка."""
    rnd = random.Random(432)
    s = f'<rect width="{W}" height="{H}" fill="#e8eef0"/>'
    s += nebo("den", t, False, 28)
    s += SL(Z_DAL, f'<rect x="0" y="40" width="{W}" height="760" fill="{BETON}" opacity=".5" {o(5)}/>')
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="300" width="280" height="420" rx="8" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _kovrik_pol(460, 900, 700, 110, KAMEN, KREM, 32))
    s += SL(Z_SRED, f'<rect x="300" y="700" width="1200" height="40" rx="8" fill="{KAMEN}" {o(6)}/>')
    px, py, pw, ph_ = 1020, 300, 760, 300
    vid = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw}" height="{ph_}" fill="{KREM}"/>'
           f'<rect x="{px+60:.0f}" y="{py+100:.0f}" width="200" height="30" fill="#efe3c8"/>'
           f'<ellipse cx="{px+300:.0f}" cy="{py+140:.0f}" rx="40" ry="26" fill="{KRAS}" opacity=".7"/>')
    put = kontur_proema(px, py, pw, ph_, "pryam")
    shkf = f'<rect x="{px-30:.0f}" y="{py-40:.0f}" width="{pw+60}" height="60" fill="url(#derev)" {o(6)}/>'
    shkf += f'<path d="{put}" fill="#1a140e"/>' + vid + mesto_stoka(px, py, pw, ph_, "pryam")
    shkf += f'<path d="{put}" fill="none" {o(8)}/>'
    s += SL(Z_SRED, shkf)
    tyan = A.ease(A.seg(t, .4, 1.0))
    podx = 620 - 100 * tyan
    box_x = 640 - 60 * (1 - tyan)
    s += SL(Z_SRED, f'<rect x="{box_x:.0f}" y="640" width="260" height="90" rx="10" fill="{KAMEN2}" opacity=".3" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{podx:.0f}" y="650" width="220" height="60" rx="10" fill="url(#derev)" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="{podx+20+i*40:.0f}" y="590" width="10" height="70" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="960" y="600" width="140" height="70" rx="8" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1240" cy="640" rx="50" ry="40" fill="{KAMEN2}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1420" cy="660" rx="40" ry="30" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1500" y="640" width="60" height="50" rx="6" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1600,700 l-16,-100 l40,18 l16,82 Z" fill="{ZEL}" {o(4)}/>')
    kach = 4 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 1660 600)"><path d="M1660,600 h40 v16 h-40 Z" fill="{TKAN}" {o(3)}/></g>')
    s += SL(Z_SRED, figura(480, 1000, 500, t, "#efe3c8", "#9c7049", False, .0))
    r1a, (r1ax, r1ay) = rukav(560, 800, 140, -30, t, "#efe3c8", "#9c7049", .1)
    r1b, (r1bx, r1by) = rukav(400, 800, 140, -150, t, "#efe3c8", "#9c7049", .3)
    s += SL(Z_SRED, r1a + r1b)
    s += SL(Z_SRED, f'<ellipse cx="{r1ax:.0f}" cy="{r1ay:.0f}" rx="24" ry="17" fill="#efe3c8" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r1bx:.0f}" cy="{r1by:.0f}" rx="24" ry="17" fill="#efe3c8" {o(4)}/>')
    s += SL(Z_SRED, figura(800, 1010, 480, t, "#2a4a6a", "#efe3c8", False, .2))
    r2, (r2x, r2y) = rukav(870, 820, 110, -70, t, "#2a4a6a", "#efe3c8", .2)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="22" ry="15" fill="#2a4a6a" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="{r2x:.0f}" cy="{r2y-6:.0f}" r="14" fill="url(#med)" {o(2)}/>')
    s += SL(Z_SRED, lampa(240, 420, t, .9, True))
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 46, 6))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 46, 5))
    s += SL(Z_PERED, ramka_pp("oba", "#1a1e20", .3))
    s += vinetka(.3)
    return s


def perochinnyy_nozhik_ot_deda(t):
    """Мостик в память. Летнее крыльцо: дед на раскрытой ладони держит
    складной ножик, внук тянется обеими руками принять его."""
    rnd = random.Random(433)
    s = f'<rect width="{W}" height="{H}" fill="#cfe4c8"/>'
    s += nebo("den", t, False, 29)
    s += SL(Z_DAL, oblaka(t, 140, 4, 31, .4, "#f4f8ee", 9.0))
    s += SL(Z_DAL, pleten(0, 820, 500, 170, 5))
    s += SL(Z_DAL, izba_snaruzhi(420, 820, 540, t, False, True, 29))
    s += SL(Z_DAL, f'<path d="M1240,820 l-16,-320 l32,0 Z" fill="{ZEL}" {o(4)}/>')
    for i in range(5):
        a = i * .9
        s += SL(Z_DAL, f'<circle cx="{1240+math.cos(a)*90:.0f}" cy="{620+math.sin(a)*40:.0f}" r="34" fill="{ZOL}" {o(3)}/>')
        s += SL(Z_DAL, f'<circle cx="{1240+math.cos(a)*90:.0f}" cy="{620+math.sin(a)*40:.0f}" r="14" fill="#5a3a26" {o(2)}/>')
    # поленница у крыльца и колодец — двор не пустой
    for row in range(3):
        for col in range(5):
            s += SL(Z_SRED, f'<circle cx="{1340+col*38:.0f}" cy="{880-row*36:.0f}" r="18" fill="url(#derev)" {o(3)}/>')
            s += SL(Z_SRED, f'<circle cx="{1340+col*38:.0f}" cy="{880-row*36:.0f}" r="10" fill="{KREM}" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="300" y="780" width="1300" height="60" rx="10" fill="url(#dosk)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="700" width="20" height="90" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1560" y="700" width="20" height="90" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<line x1="300" y1="700" x2="1580" y2="700" stroke="url(#derev)" stroke-width="12"/>')
    s += SL(Z_SRED, f'<ellipse cx="1480" cy="840" rx="50" ry="40" fill="{ZHELEZ}" opacity=".85" {o(4)}/>')
    s += SL(Z_SRED, f'<line x1="400" y1="780" x2="440" y2="560" stroke="url(#derev)" stroke-width="8"/>')
    s += SL(Z_SRED, f'<line x1="440" y1="780" x2="480" y2="560" stroke="url(#derev)" stroke-width="8"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="800" width="60" height="50" rx="6" fill="#8a7a5a" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, svecha(1200, 760, t, .2, .7))
    s += SL(Z_SRED, figura(700, 940, 460, t, "#4a3a2a", "#f4e8c8", False, .0, shapka=True))
    kiv = 4 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kiv:.1f} 700 700)">')
    nozh_x, nozh_y = 800, 780
    s += SL(Z_SRED, f'<ellipse cx="{nozh_x:.0f}" cy="{nozh_y:.0f}" rx="40" ry="20" fill="#4a3a2a" opacity=".3"/>')
    s += SL(Z_SRED, f'<rect x="{nozh_x-22:.0f}" y="{nozh_y-8:.0f}" width="44" height="14" rx="5" fill="#6b4428" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{nozh_x+20:.0f},{nozh_y:.0f} l34,-4 l-6,8 l-28,4 Z" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, '</g>')
    tyan = A.ease(A.seg(t, .6, 1.4))
    s += SL(Z_SRED, figura(1000, 920, 320, t, "#cfe4c8", "#f4e8c8", False, .3, naklon=-4 * tyan))
    r2a, (r2ax, r2ay) = rukav(940, 795, 100, -20, t, "#cfe4c8", "#f4e8c8", .2)
    r2b, (r2bx, r2by) = rukav(1060, 795, 100, -160, t, "#cfe4c8", "#f4e8c8", .4)
    s += SL(Z_SRED, r2a + r2b)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="20" ry="14" fill="#cfe4c8" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2bx:.0f}" cy="{r2by:.0f}" rx="20" ry="14" fill="#cfe4c8" {o(4)}/>')
    s += SL(Z_SRED, kot(300, 860, t, .8, "#3b3430", True))
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 47, 4))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 47, 4))
    s += SL(Z_PERED, f'<rect x="0" y="980" width="{W}" height="100" fill="{TRAVA}" opacity=".6"/>')
    return s


def struzhka_i_svistulka(t):
    """Мостик в память. Тот же мальчик на бревне у реки режет ивовый прут
    ножиком, стружка летит; откладывает прут, берёт свистульку и свистит."""
    rnd = random.Random(434)
    s = f'<rect width="{W}" height="{H}" fill="#cfe4e8"/>'
    s += nebo("den", t, False, 30)
    s += SL(Z_DAL, oblaka(t, 140, 4, 33, .4, "#f4f8ee", 9.0))
    s += SL(Z_DAL, f'<rect x="0" y="760" width="{W}" height="320" fill="{VODA}" opacity=".7" {o(5)}/>')
    for i in range(6):
        bl = .3 + .4 * abs(A.w(t, 1.6 + i * .2, i * .3))
        s += SL(Z_DAL, f'<ellipse cx="{200+i*300:.0f}" cy="{820+i%2*60:.0f}" rx="120" ry="14" fill="#eaf4ff" opacity="{bl:.2f}"/>')
    s += SL(Z_DAL, f'<path d="M1500,900 q80,-160 220,-160 l0,340 h-220 Z" fill="{ZEL}" {o(5)}/>')
    s += SL(Z_DAL, goloe_derevo(560, 780, 420, t, 12, 8, "#3c5a3a", inej_=False))
    s += SL(Z_DAL, f'<path d="M420,780 q0,-90 60,-100 q60,10 60,100 Z" fill="{ZEL2}" {o(4)}/>')
    s += SL(Z_DAL, f'<path d="M1140,780 q0,-80 50,-90 q50,10 50,90 Z" fill="{ZEL2}" {o(4)}/>')
    s += SL(Z_DAL, izba_snaruzhi(1240, 800, 360, t, False, True, 34))
    s += SL(Z_DAL, f'<path d="M780,780 q0,-120 70,-130 q70,10 70,130 Z" fill="{ZEL}" {o(5)}/>')
    s += SL(Z_DAL, f'<path d="M950,780 q0,-100 60,-110 q60,10 60,110 Z" fill="{ZEL2}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="920" rx="340" ry="62" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="896" rx="300" ry="30" fill="#6b4428" {o(4)}/>')
    stryazhka_sp = A.w(t, 1.4) * 10
    s += SL(Z_SRED, f'<g transform="rotate({3*A.w(t,1.2):.1f} 820 820)">'
                    f'<path d="M820,820 l-6,-200 l10,2 l4,198 Z" fill="#d8c8a4" {o(4)}/></g>')
    letit = (t * 1.6) % 1.0
    for i in range(5):
        p = (letit + i * .2) % 1.0
        s += SL(Z_SRED, f'<path d="M{880-40*p+stryazhka_sp:.0f},{780-60*p:.0f} q10,-6 16,2 q-4,8 -14,8 Z" fill="#e8d8b4" opacity="{1-p:.2f}"/>')
    svist_on = (t % 4.0) > 2.4
    s += SL(Z_SRED, figura(700, 1000, 380, t, "#3a5a3a", "#f4e8c8", False, .0, profil=False))
    ang = -110 if not svist_on else -40
    r1, (r1x, r1y) = rukav(760, 850, 130, ang, t, "#3a5a3a", "#f4e8c8", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="20" ry="14" fill="#3a5a3a" {o(4)}/>')
    if svist_on:
        s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y:.0f} l20,6 l-4,10 l-18,-8 Z" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1050" cy="900" rx="44" ry="18" fill="#8a7a5a" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, f'<line x1="1100" y1="900" x2="1300" y2="760" stroke="#6b4428" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="1140" y="900" width="60" height="50" rx="6" fill="#8a7a5a" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="500" cy="900" rx="60" ry="24" fill="{ZOL}" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M580,900 h100 l-10,30 h-80 Z" fill="#c8a06a" {o(3)}/>')
    skok = abs(A.w(t, 2.4)) * 10
    s += SL(Z_SRED, f'<ellipse cx="{420+skok:.0f}" cy="920" rx="16" ry="10" fill="{ZEL2}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1400, 820, t, .2, .6))
    s += SL(Z_SRED, f'<rect x="420" y="600" width="220" height="160" rx="10" fill="#6b4428" opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, _napolnenie(420, 620, 1080, 100, t, 48, 6))
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 48, 7))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 48, 6))
    s += SL(Z_PERED, f'<rect x="0" y="980" width="{W}" height="100" fill="{TRAVA}" opacity=".5"/>')
    return s


# ═══ из chast2.py ═══
IMP2 = "#3a2a4a"


# ───────────────────────── МЕСТНЫЕ КИРПИЧИКИ ПОРЦИИ ─────────────────────────
def _samovar(x, y, s_, t, par_on=True):
    s = ten(x, y + 90 * s_, 60 * s_, 14 * s_, .4)
    s += f'<ellipse cx="{x:.0f}" cy="{y+70*s_:.0f}" rx="56*{s_:.0f}" ry="14" fill="url(#zol)" {o(4)}/>'.replace("56*", "")
    s += (f'<path d="M{x-54*s_:.0f},{y+70*s_:.0f} q{-6*s_:.0f},{-120*s_:.0f} 54*{s_:.0f},{-126*s_:.0f}'
          .replace("54*", "") + f' q{60*s_:.0f},6 {54*s_:.0f},{126*s_:.0f} Z" fill="url(#zol)" {o(5)}/>')
    s += f'<rect x="{x-14*s_:.0f}" y="{y-86*s_:.0f}" width="{28*s_:.0f}" height="{18*s_:.0f}" rx="4" fill="url(#zol)" {o(3)}/>'
    s += f'<circle cx="{x-50*s_:.0f}" cy="{y:.0f}" r="{10*s_:.0f}" fill="{ZHELEZ}" {o(2)}/>'
    s += f'<circle cx="{x+50*s_:.0f}" cy="{y:.0f}" r="{10*s_:.0f}" fill="{ZHELEZ}" {o(2)}/>'
    s += f'<rect x="{x-6*s_:.0f}" y="{y+30*s_:.0f}" width="{12*s_:.0f}" height="{10*s_:.0f}" fill="{ZHELEZ}" {o(2)}/>'
    if par_on:
        s += par(x, y - 92 * s_, t, 3, .45, 90 * s_, .5)
    return s


def _tryumo_otrazhenie(x, y, s_, t, vid):
    """Мини-фигура внутри створки трюмо: `vid` — young|staraya|babka."""
    if vid == "babka":
        fig = figura(x, y, 210 * s_, t, "#5a5560", "#cfd6de", True, .0, False, 1.0, False, 0, True, True)
        ruk, _ = rukav(x - 28 * s_, y - 150 * s_, 70 * s_, -120 + 20 * A.w(t, 1.2), t, "#5a5560", "#cfd6de", .0, 12)
        return fig + ruk
    col = "#6b2a44" if vid == "young" else "#4a3a4a"
    return figura(x, y, 210 * s_, t, col, "#ffd98a", False, .3 if vid == "young" else .0)


def _pryalka_stan(x, y, w_, h_, t):
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6" fill="url(#derev)" {o(5)}/>'
    for i in range(6):
        lx = x + w_ * .12 + i * w_ * .76 / 5
        sh = 3 * A.w(t, 1.1, i * .1)
        s += f'<line x1="{lx+sh:.0f}" y1="{y:.0f}" x2="{lx-sh:.0f}" y2="{y+h_:.0f}" stroke="{KREM}" stroke-width="3" opacity=".8"/>'
    return s


def _schyoty(x, y, s_, t):
    s = f'<rect x="{x-60*s_:.0f}" y="{y-50*s_:.0f}" width="{120*s_:.0f}" height="{100*s_:.0f}" rx="6" fill="url(#derev)" {o(5)}/>'
    for row in range(4):
        ry = y - 30 * s_ + row * 20 * s_
        sh = 18 * s_ * A.w(t, 1.6, row * .2)
        for i in range(4):
            s += f'<circle cx="{x-40*s_+i*26*s_+sh*((i%2)*2-1)*.3:.0f}" cy="{ry:.0f}" r="{8*s_:.0f}" fill="{ZOL}" {o(2)}/>'
    return s


def _pochta_yashchiki(x, y, w_, h_, n=6):
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="4" fill="{ZHELEZ}" {o(5)}/>'
    for i in range(n):
        cx_ = x + (i % 3 + .5) * w_ / 3
        cy_ = y + (i // 3 + .5) * h_ / 2
        s += f'<rect x="{cx_-w_/7:.0f}" y="{cy_-h_/6:.0f}" width="{w_/3.5:.0f}" height="{h_/3.5:.0f}" rx="3" fill="#3a3e44" {o(2)}/>'
    return s


def _rusalka(x, y, h_, t):
    """Русалка сидит на камне: хвост свёрнут у бедра, торс и плечи,
    обеими руками закрывает лицо, волосы падают по спине. `y` — уровень
    камня под бёдрами, `h_` — рост от бедра до макушки."""
    plach = A.seg(t % 3.0, 0, 2.0)
    kach = 2 * A.w(t, 1.1)
    hip = (x, y)
    s = ten(x - h_ * .1, y + h_ * .04, h_ * .55, 14, .45)
    # хвост: плавная дуга-«колбаска» от бедра влево, веер-плавник на конце
    s += (f'<path d="M{x-h_*.04:.0f},{y+h_*.02:.0f}'
          f' Q{x-h_*.42:.0f},{y+h_*.1:.0f} {x-h_*.68:.0f},{y-h_*.1+kach:.0f}'
          f' Q{x-h_*.42:.0f},{y-h_*.22:.0f} {x-h_*.08:.0f},{y-h_*.14:.0f} Z"'
          f' fill="url(#led)" {o(5)}/>')
    fx, fy = x - h_ * .7, y - h_ * .1 + kach
    s += (f'<path d="M{fx:.0f},{fy:.0f} l{-h_*.16:.0f},{-h_*.14:.0f} l{h_*.05:.0f},{h_*.13:.0f}'
          f' l{-h_*.18:.0f},{h_*.01:.0f} l{h_*.18:.0f},{h_*.11:.0f} l{-h_*.05:.0f},{h_*.12:.0f} Z"'
          f' fill="#9fc4d8" {o(3)}/>')
    # торс: от бедра вверх к плечам, тот же силуэт одним плавным телом
    tcx, tcy = x + h_ * .02, y - h_ * .34
    s += f'<ellipse cx="{tcx:.0f}" cy="{tcy:.0f}" rx="{h_*.17:.0f}" ry="{h_*.24:.0f}" fill="#e0b08a" {o(5)}/>'
    shx, shy = tcx, y - h_ * .54
    # волосы: прядь от затылка вдоль спины
    s += (f'<path d="M{shx+h_*.1:.0f},{shy-h_*.06:.0f} q{h_*.14:.0f},{h_*.2:.0f} {h_*.04:.0f},{h_*.42:.0f}'
          f' q{-h_*.04:.0f},{h_*.14:.0f} {-h_*.16:.0f},{h_*.14:.0f}'
          f' q{h_*.1:.0f},{-h_*.18:.0f} {h_*.02:.0f},{-h_*.5:.0f} Z" fill="#caa64a" {o(4)}/>')
    # голова — вплотную к плечам, без зазора
    hcx, hcy = shx, shy - h_ * .13
    s += f'<ellipse cx="{hcx:.0f}" cy="{hcy:.0f}" rx="{h_*.12:.0f}" ry="{h_*.13:.0f}" fill="#e0b08a" {o(5)}/>'
    s += (f'<path d="M{hcx-h_*.1:.0f},{hcy-h_*.05:.0f} q{-h_*.02:.0f},{-h_*.14:.0f} {h_*.1:.0f},{-h_*.17:.0f}'
          f' q{h_*.1:.0f},{-h_*.01:.0f} {h_*.1:.0f},{h_*.1:.0f} Z" fill="#caa64a" {o(3)}/>')
    # руки закрывают лицо: от плеч к подбородку, кисти сходятся перед лицом
    for sgn in (-1, 1):
        ruka_d = (f'M{shx+sgn*h_*.12:.0f},{shy:.0f}'
                  f' Q{shx+sgn*h_*.1:.0f},{hcy+h_*.02:.0f} {hcx+sgn*h_*.03:.0f},{hcy+h_*.03:.0f}')
        s += f'<path d="{ruka_d}" fill="none" stroke="{K}" stroke-width="{h_*.08:.0f}" stroke-linecap="round"/>'
        s += f'<path d="{ruka_d}" fill="none" stroke="#e0b08a" stroke-width="{h_*.062:.0f}" stroke-linecap="round"/>'
    if plach < .7:
        dy = plach * h_ * .5
        s += f'<circle cx="{hcx:.0f}" cy="{hcy+h_*.1+dy:.0f}" r="{h_*.017:.0f}" fill="#cfe8ff" opacity="{1-plach:.2f}"/>'
    else:
        s += f'<circle cx="{hcx:.0f}" cy="{y-h_*.1:.0f}" r="{h_*.024:.0f}" fill="{SNEG}" {o(2)}/>'
    return s


def _primeta_vorona(x, y, s_, t, uhodit=0.0):
    off = uhodit * 260 * s_
    s = f'<g transform="translate({off:.0f},0)">'
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{36*s_:.0f}" ry="{48*s_:.0f}" fill="#2a2a32" {o(4)}/>'
    s += f'<path d="M{x:.0f},{y-30*s_:.0f} l{14*s_:.0f},{-10*s_:.0f} l{-4*s_:.0f},{10*s_:.0f} Z" fill="{K}"/>'
    ug = -40 * (1 - uhodit)
    s += (f'<path d="M{x-10*s_:.0f},{y-10*s_:.0f} l{70*s_:.0f},{ug*s_:.0f}" stroke="{ZHELEZ}"'
          f' stroke-width="{4*s_:.0f}"/>')
    pleso = (1 - uhodit) * 20 * A.w(t, 1.6)
    s += f'<path d="M{x-30*s_:.0f},{y:.0f} q{-20*s_:.0f},{pleso:.0f} {-10*s_:.0f},{30*s_:.0f}" fill="none" stroke="#2a2a32" stroke-width="{8*s_:.0f}"/>'
    if uhodit > .5:
        s += f'<ellipse cx="{x-50*s_:.0f}" cy="{y+20*s_:.0f}" rx="{14*s_:.0f}" ry="{10*s_:.0f}" fill="{ZHELEZ}" {o(2)}/>'
    s += f'<rect x="{x-20*s_:.0f}" y="{y+40*s_:.0f}" width="{40*s_:.0f}" height="{18*s_:.0f}" fill="{TKAN2}" {o(2)}/>'
    return s + '</g>'


# ═══════════════════════════ ДЕКОРАЦИИ 36-38 ══════════════════════════════
# план 35 «struzhka_i_svistulka» уже написан в chast1.py — не дублируется.
def babushkin_nozh_poloska(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("den", t, False, 8)
    s += SL(Z_DAL, okno_izby(1500, 140, 260, 260, t, svet=False, moroz=.2))
    s += utvar_izby(80, 420, 420, t, 17)
    s += SL(Z_SRED, polovicy(780))
    s += SL(Z_SRED, stol(520, 700, 900, 34))
    s += SL(Z_SRED, kartoshka(900, 700, t, 7, 9))
    s += SL(Z_SRED, f'<circle cx="760" cy="696" r="46" fill="{TKAN}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1080" cy="690" rx="90" ry="34" fill="{MED}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="600" y="650" width="80" height="28" rx="6" fill="{KAMEN}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1240,660 v60" stroke="{STEKLO}" stroke-width="30" opacity=".7"/>')
    s += SL(Z_SRED, f'<path d="M560,640 q40,-10 80,0 l0,30 q-40,10 -80,0 Z" fill="{RUSH}" {o(3)}/>')
    nx, ny = 700, 650
    s += SL(Z_SRED, f'<g transform="rotate({2*A.w(t,1.1):.1f} {nx:.0f} {ny:.0f})">'
                    f'<rect x="{nx-110:.0f}" y="{ny-10:.0f}" width="80" height="22" rx="8" fill="#2a1d14" {o(4)}/>'
                    f'<path d="M{nx-10:.0f},{ny-2:.0f} L{nx+150:.0f},{ny:.0f} L{nx-10:.0f},{ny+2:.0f} Z"'
                    f' fill="{ZHELEZ}" {o(2)}/><line x1="{nx-80:.0f}" y1="{ny:.0f}" x2="{nx-40:.0f}" y2="{ny:.0f}"'
                    f' stroke="#eef4fa" stroke-width="2" opacity=".5"/></g>')
    s += SL(Z_SRED, figura(560, 960, 480, t, "#6b4a3a", KREM, True, .2))
    ruk1, (r1x, r1y) = rukav(640, 700, 150, -40, t, "#6b4a3a", KREM, .2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(560, 690, 170, -10, t, "#6b4a3a", KREM, .5)
    s += SL(Z_SRED, ruk2)
    kozhura = A.seg(t % 4.0, 0, 3.6)
    ln = kozhura * 260
    s += SL(Z_SRED, f'<path d="M{r2x:.0f},{r2y:.0f} q{40:.0f},{20:.0f} {30:.0f},{60:.0f}'
                    f' q{-10:.0f},{40:.0f} {30:.0f},{50:.0f}" fill="none" stroke="{POL}"'
                    f' stroke-width="5" stroke-dasharray="{ln:.0f} 400"/>')
    s += SL(Z_SRED, _napolnenie(1200, 540, 500, 200, t, 36, 6))
    s += SL(Z_SRED, svecha(120, 760, t, 0.0, .8))
    s += SL(Z_PERED, ramka_pp("levo", "#120e0e", .4))
    s += vinetka(.4)
    return s


def nabor_nosovyh_platkov(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 12)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(420, 720, 1100, 34))
    bx, by, bw, bh = 700, 560, 520, 160
    s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw}" height="{bh}" rx="12" fill="{KREM}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{bx+16:.0f}" y="{by+16:.0f}" width="{bw-32}" height="{bh-32}" rx="8" fill="url(#stekl)" opacity=".4" {o(3)}/>')
    for i in range(3):
        rot = -14 + i * 14
        s += SL(Z_SRED, f'<g transform="rotate({rot} {bx+140+i*110:.0f} {by+bh*.6:.0f})">'
                        f'<rect x="{bx+70+i*110:.0f}" y="{by+40:.0f}" width="120" height="100" fill="{TKAN}" {o(3)}/>'
                        f'<rect x="{bx+70+i*110+16:.0f}" y="{by+56:.0f}" width="88" height="68" fill="none"'
                        f' stroke="{KREM}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<rect x="{bx+bw-120:.0f}" y="{by+bh*.3:.0f}" width="110" height="70" rx="6" fill="{RUSH}" {o(3)}/>')
    lenta_sh = 6 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<line x1="{bx+bw-80:.0f}" y1="{by+bh*.3+10:.0f}" x2="{bx+bw-30+lenta_sh:.0f}" y2="{by+bh*.3+70:.0f}" stroke="{KRAS}" stroke-width="10"/>')
    drop_y = by - 40 + 16 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<path d="M{bx+bw*.5:.0f},{drop_y-30:.0f} q-18,22 0,40 q18,-18 0,-40 Z" fill="{STEKLO}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{bx-180:.0f}" y="{by+40:.0f}" width="140" height="190" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{bx+bw+40:.0f}" y="{by+60:.0f}" width="90" height="130" rx="6" fill="#efe3c8" {o(3)}/>')
    shisha_x = bx + 80 + 200 * ((t * 40) % 300) / 300
    s += SL(Z_SRED, f'<circle cx="{shisha_x:.0f}" cy="{by+bh+40:.0f}" r="18" fill="#6b4428" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{bx-60:.0f}" cy="{by+bh+30:.0f}" r="28" fill="{ZOL}" {o(3)}/>')
    s += SL(Z_SRED, begushchiy_blik(t, 6.0, .2, .18, 300))
    s += SL(Z_SRED, svecha(444, 796, t, 1.64, .8))
    s += SL(Z_SRED, _napolnenie(60, 560, 260, 120, t, 206, 2))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def yarmarochnyy_larek_s_platkami(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("den", t, True, 19)
    s += SL(Z_DAL, oblaka(t, 160, 3, 12, .4))
    s += SL(Z_DAL, _elka(260, 940, 440, t, 6))
    s += SL(Z_DAL, _elka(1760, 920, 400, t, 7))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="980" rx="900" ry="60" fill="{SNEG}" {o(4)}/>')
    lx, ly, lw, lh = 660, 320, 600, 520
    s += SL(Z_SRED, f'<path d="M{lx-40:.0f},{ly:.0f} L{lx+lw+40:.0f},{ly:.0f} L{lx+lw:.0f},{ly+80:.0f}'
                    f' L{lx:.0f},{ly+80:.0f} Z" fill="{TKAN}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{lx:.0f}" y="{ly+80:.0f}" width="{lw}" height="{lh-80}" fill="url(#derev)" {o(6)}/>')
    pw, ph_ = 800, 320
    px, py = lx + (lw - pw) / 2, ly + 140
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="{lx+40:.0f}" y="{ly+lh-40:.0f}" width="{lw-80}" height="60" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, _samovar(lx + 90, ly + lh - 10, .7, t))
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{lx+lw-180+i*34:.0f}" cy="{ly+lh-30:.0f}" r="14" fill="{MED}" {o(2)}/>')
    s += SL(Z_DAL, f'<path d="M1260,900 l60,-140 l60,140 Z" fill="{SNEG}" {o(3)}/>')
    s += SL(Z_DAL, f'<circle cx="1440" cy="860" r="40" fill="{SNEG}" {o(3)}/><circle cx="1440" cy="800" r="28" fill="{SNEG}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="120" y="780" width="200" height="130" rx="20" fill="{KREM}" {o(5)}/>')
    povorot = A.ease(A.seg(t % 6.0, 2.0, 1.4))
    razv = A.ease(A.seg(t % 6.0, .2, 1.4))
    stoy1 = figura(lx + 120, ly + lh + 60, 460, t, "#6b2a38", KREM, True, .0, True)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(lx + 197, ly + lh + 60 - 460 * .64, 130, -30, t, "#6b2a38", KREM, .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y:.0f} h{150*razv:.0f} v40 h{-150*razv:.0f} Z" fill="{KRAS}" {o(3)}/>')
    stoy2 = figura(1240 + povorot * 10, ly + lh + 80, 470, t, "#3a2a4a", KREM, False, .3, True)
    s += SL(Z_SRED, f'<g transform="rotate({povorot*18:.1f} 1240 {ly+lh+40:.0f})">{stoy2}</g>')
    bahroma = povorot * 40
    s += SL(Z_SRED, f'<path d="M1150,{ly+lh-80:.0f} q90,-20 180,0" fill="none" stroke="{KRAS}" stroke-width="40" opacity=".92"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<line x1="{1150+i*30:.0f}" y1="{ly+lh-60:.0f}" x2="{1150+i*30+bahroma:.0f}" y2="{ly+lh-20:.0f}" stroke="{KRAS}" stroke-width="4"/>')
    s += SL(Z_SRED, svecha(728, 812, t, 1.28, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#1a1a1a", .3))
    s += SL(Z_LETIT, sneg_letit(t, 26, 13, .5, .9))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 39-44 ══════════════════════════════
def platok_dlya_slez_i_shal_dlya_tepla(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W//2}" height="{H}" fill="{SUMER}"/>')
    s += SL(Z_SRED, f'<rect x="{W//2}" y="0" width="{W//2}" height="{H}" fill="{POL2}"/>')
    s += SL(Z_DAL, okno_izby(80, 120, 280, 300, t, svet=False, moroz=.2))
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{100+i*50}" y1="150" x2="{80+i*50}" y2="380" stroke="{STEKLO}" stroke-width="3" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="420" y="780" width="420" height="40" rx="10" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="460" y="700" width="340" height="90" rx="20" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="560" y="660" width="80" height="50" fill="#fff" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="860" cy="760" rx="34" ry="16" fill="#6b4428" {o(3)}/>')
    figl = figura(560, 1040, 480, t, "#2a3a55", "#cfd6de", False, .0)
    s += SL(Z_SRED, figl)
    ruk1, (rlx, rly) = rukav(620, 780, 150, -150, t, "#2a3a55", "#cfd6de", .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<rect x="{rlx-30:.0f}" y="{rly-16:.0f}" width="60" height="40" rx="10" fill="#fff" {o(3)}/>')
    s += SL(Z_DAL, okno_izby(W - 360, 120, 280, 300, t, svet=True, moroz=0))
    s += SL(Z_SRED, teplo(W - 220, 280, 240, 220, .4))
    s += SL(Z_SRED, kirpich_ustya(W - 360, 700, 220, 220, t))
    s += SL(Z_SRED, svecha(W - 760, 900, t, .3, 1.0))
    s += SL(Z_SRED, kot(W - 900, 980, t, 1.0, "#3b3430", False))
    figr = figura(W - 540, 1040, 480, t, "#6b2a38", SVET, True, .2, True)
    s += SL(Z_SRED, figr)
    shawl = .3 + .15 * A.w(t, 2.0)
    ruk2, (rrx, rry) = rukav(W - 470, 760, 160, -60 - shawl * 30, t, "#6b2a38", SVET, .2)
    s += SL(Z_SRED, ruk2)
    ruk3, (rr2x, rr2y) = rukav(W - 610, 760, 160, -120 + shawl * 30, t, "#6b2a38", SVET, .5)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, f'<rect x="{W-620:.0f}" y="800" width="60" height="60" rx="12" fill="{KAMEN}" {o(3)}/>')
    s += SL(Z_SRED, par(W - 620, 790, t, 3, .4, 90))
    s += SL(Z_PERED, f'<rect x="{W//2-4}" y="0" width="8" height="{H}" fill="{K}"/>')
    s += vinetka(.4)
    return s


def chto_v_podarochnyy_paket(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 15)
    s += SL(Z_DAL, _oboi_fon())
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, _veshalka_seni(1280, 300, 420, t, 4))
    s += SL(Z_SRED, f'<rect x="420" y="320" width="220" height="420" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="530" cy="460" rx="90" ry="140" fill="#cfd6de" opacity=".6" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="700" width="420" height="40" rx="10" fill="url(#derev)" {o(5)}/>')
    kx = 900
    s += SL(Z_SRED, f'<path d="M{kx-80:.0f},680 l20,-170 h120 l20,170 Z" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="510" rx="80" ry="20" fill="{TKAN2}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+140:.0f}" y="600" width="160" height="120" rx="10" fill="{KREM}" {o(4)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<circle cx="{kx+170+i*50:.0f}" cy="630" r="16" fill="{(KRAS,ZOL,ZEL2)[i]}" {o(2)}/>')
    s += SL(Z_SRED, figura(900, 1020, 480, t, "#7a5a6a", KREM, False, .0))
    plat_move = A.seg(t, .2, 1.0)
    ruk1, (r1x, r1y) = rukav(840, 760, 150, -170 + 20 * plat_move, t, "#7a5a6a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<rect x="{r1x-10:.0f}" y="{r1y-40*(1-plat_move):.0f}" width="80" height="60" rx="8" fill="{RUSH}" opacity="{1-plat_move:.2f}"/>')
    shal_in = A.ease(A.seg(t, 1.2, 1.0))
    ruk2, (r2x, r2y) = rukav(960, 760, 150, -10 - 20 * shal_in, t, "#7a5a6a", KREM, .4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<rect x="{r2x-40:.0f}" y="{r2y-30+shal_in*60:.0f}" width="90" height="36" rx="8" fill="{TKAN}" opacity=".9" {o(2)}/>')
    kach = 3 * A.w(t, 1.3)
    s += SL(Z_SRED, f'<circle cx="{700+kach:.0f}" cy="560" r="8" fill="{ZHELEZ}"/>')
    s += SL(Z_SRED, svecha(279, 871, t, 1.11, .8))
    s += SL(Z_PERED, ramka_pp("levo", "#120e14", .4))
    s += vinetka(.4)
    return s


def polotence_ot_sestry(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 17)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_DAL, okno_izby(120, 140, 280, 260, t, svet=True, moroz=.3))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _pryalka_stan(1500, 280, 220, 420, t))
    s += SL(Z_SRED, f'<path d="M1600,760 q-70,0 -70,60 q0,40 70,40 q70,0 70,-40 q0,-60 -70,-60 Z" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, kot(1700, 500, t, .9, "#3b3430", True))
    s += SL(Z_SRED, stol(300, 760, 700, 34))
    s += SL(Z_SRED, _samovar(500, 740, .8, t))
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{880+i*20:.0f},680 q{10*A.w(t,1.2,i*.2):.0f},-16 {20+i*20:.0f},0" fill="none" stroke="{ZEL2}" stroke-width="5"/>')
    s += SL(Z_SRED, _kovrik_pol(500, 900, 700, 120, TKAN, KREM, 31))
    pol_w = 360
    razv = A.ease(A.seg(t, .2, 1.4))
    cx, cy = 900, 680
    s += SL(Z_SRED, f'<rect x="{cx-pol_w*razv/2:.0f}" y="{cy:.0f}" width="{pol_w*razv:.0f}" height="90" fill="{KREM}" {o(4)}/>')
    petuh_on = .5 + .5 * abs(A.w(t, 1.0))
    if razv > .5:
        for i in range(3):
            s += SL(Z_SRED, f'<circle cx="{cx-pol_w*.3+i*pol_w*.3:.0f}" cy="{cy+45:.0f}" r="18" fill="{KRAS}" opacity="{petuh_on:.2f}"/>')
    s += SL(Z_SRED, figura(cx - pol_w * .5 - 40, 1020, 480, t, "#8c3a3a", KREM, True, .0))
    ruk1, _ = rukav(cx - pol_w * .4, 720, 130, -20, t, "#8c3a3a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    obnyat = A.ease(A.seg(t, 1.6, 1.0))
    ruk2, _ = rukav(cx - pol_w * .4 - 60, 740, 120 + obnyat * 60, 40 + obnyat * 30, t, "#8c3a3a", KREM, .4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, figura(cx + pol_w * .5 + 40, 1020, 470, t, "#3a5a4a", KREM, False, .3))
    ruk3, _ = rukav(cx + pol_w * .4, 720, 130, -160, t, "#3a5a4a", KREM, .3)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, par(500, 650, t, 3, .4, 80))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.4)
    return s


def polotence_ot_chuzhoy(t):
    s = f'<rect width="{W}" height="{H}" fill="{SUMER}"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 23))
    s += SL(Z_DAL, goloe_derevo(240, 880, 420, t, 8, 6, inej_=True))
    s += SL(Z_DAL, grozd_ryabiny(300, 700, t, 1.2, 16))
    s += SL(Z_DAL, f'<circle cx="1600" cy="760" r="60" fill="{KAMEN}" {o(5)}/><path d="M1540,760 a60,40 0 0 1 120,0" fill="none" stroke="{KAMEN}" stroke-width="10"/>')
    s += SL(Z_SRED, sneg_lezhit(840))
    s += SL(Z_SRED, pleten(680, 760, 560, 160))
    kx = 960
    s += SL(Z_SRED, f'<rect x="{kx-50:.0f}" y="640" width="100" height="220" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{kx:.0f},640 L{kx-60:.0f},600 L{kx+60:.0f},600 Z" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, figura(kx - 220, 940, 420, t, "#2a2a30", "#5a5560", True, .0))
    ruk1, (r1x, r1y) = rukav(kx - 160, 720, 160, -10, t, "#2a2a30", "#5a5560", .0)
    s += SL(Z_SRED, ruk1)
    polo_x = kx - 160 + (260) * A.ease(A.seg(t, 0, 1.0))
    s += SL(Z_SRED, f'<path d="M{polo_x-50:.0f},740 q50,-20 100,0 l0,30 q-50,20 -100,0 Z" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, _chertenok(polo_x, 750, .7, t, .3))
    s += SL(Z_SRED, figura(kx + 220, 940, 420, t, "#3a3a2a", "#cfe4f5", True, .3, True))
    ruk2, (r2x, r2y) = rukav(kx + 160, 720, 160, -170, t, "#3a3a2a", "#cfe4f5", .3)
    s += SL(Z_SRED, ruk2)
    moneta = A.ease(A.seg(t, 1.6, .6))
    s += SL(Z_SRED, f'<circle cx="{r1x+10:.0f}" cy="{r1y-40*moneta:.0f}" r="14" fill="url(#med)" {o(2)}/>')
    beg = A.ease(A.seg(t, 1.0, 1.4))
    s += SL(Z_SRED, _chertenok(polo_x - beg * 200, 770 + beg * 40, .55, t, 0) if beg > .05 else "")
    s += SL(Z_DAL, siluet(1640, 940, 260, "#1a1c22", .8))
    s += SL(Z_SRED, svecha(968, 872, t, 1.92, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c10", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 14, 17, .4, .6))
    s += vinetka(.44)
    return s


def babushkina_shal(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 25)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, pech(1340, 320, 420, 540, t))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _kovrik_pol(460, 900, 700, 120, TKAN, KREM, 33))
    s += SL(Z_SRED, hodiki(1760, 320, t, 1.0))
    s += SL(Z_SRED, f'<rect x="300" y="880" width="420" height="34" rx="10" fill="url(#derev)" {o(5)}/>')
    kach = 4 * A.w(t, 1.2)
    s += SL(Z_SRED, f'<ellipse cx="{480+kach:.0f}" cy="860" rx="110" ry="34" fill="{KREM}" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{430+kach+i*36:.0f}" cy="850" r="16" fill="{(KRAS,ZOL)[i%2]}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M680,860 l-30,40 l20,-100" stroke="{ZHELEZ}" stroke-width="8" fill="none"/>')
    s += SL(Z_SRED, kot(760, 920, t, .9, "#3b3430", False))
    s += SL(Z_SRED, f'<rect x="860" y="860" width="60" height="40" rx="6" fill="{TKAN2}" {o(3)}/>')
    sway = 2 * A.w(t, .9)
    stoy = figura(900, 1020, 500, t, "#5a5560", KREM, True, .0, False, naklon=sway)
    s += SL(Z_SRED, stoy)
    ruk1, (r1x, r1y) = rukav(840, 880, 100, 60 - sway * 5, t, "#5a5560", KREM, .0, 4)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(960, 880, 100, 120 + sway * 5, t, "#5a5560", KREM, .3, 4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, figura(900, 1060, 220, t, "#efe3c8", SVET, False, .2))
    shawl = .4 + .1 * A.w(t, 1.4)
    s += SL(Z_SRED, f'<path d="M740,900 q160,{-120-shawl*40:.0f} 320,0" fill="none" stroke="#6f7f8c" stroke-width="60" opacity=".92"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{740+i*20}" y1="900" x2="{730+i*20}" y2="960" stroke="#6f7f8c" stroke-width="5"/>')
        s += SL(Z_SRED, f'<line x1="{1060-i*20}" y1="900" x2="{1070-i*20}" y2="960" stroke="#6f7f8c" stroke-width="5"/>')
    zav_y = 760 - 60 * ((t * .5) % 1.0)
    s += SL(Z_SRED, f'<path d="M900,780 q20,{-40+zav_y*.1:.0f} 0,{-80:.0f}" fill="none" stroke="#cfd6de" stroke-width="5" opacity="{1-((t*.5)%1.0):.2f}"/>')
    s += SL(Z_SRED, f'<circle cx="940" cy="700" r="10" fill="{KRAS}" opacity=".7"/><rect x="860" y="690" width="24" height="20" fill="{POBEL}" {o(2)}/>')
    s += SL(Z_SRED, svecha(173, 797, t, 0.37, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def tapochki_v_podarochnoy_korobke(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 27)
    s += SL(Z_DAL, _elka(1500, 960, 560, t, 9))
    s += SL(Z_SRED, polovicy(840))
    bx, by = 760, 660
    s += SL(Z_SRED, _korobka(bx, by, 420, 240, t, TKAN2, ZOL, True, .55, .1))
    s += SL(Z_SRED, f'<ellipse cx="{bx+120:.0f}" cy="{by+150:.0f}" rx="130" ry="16" fill="#fdf8ec" opacity=".8"/>')
    pomp = 8 * A.w(t, 1.6)
    for i, sgn in enumerate((-1, 1)):
        tx = bx + 150 + sgn * 70
        s += SL(Z_SRED, f'<path d="M{tx-50:.0f},{by+160:.0f} q0,-40 50,-40 q50,0 50,40 q-10,20 -50,20 q-40,0 -50,-20 Z" fill="#b8323a" {o(4)}/>')
        s += SL(Z_SRED, f'<circle cx="{tx:.0f}" cy="{by+108+pomp*.3*(1 if sgn>0 else -1):.0f}" r="16" fill="#efe3c8" {o(2)}/>')
    kor_t = A.ease(A.seg(t, .4, 1.4))
    s += SL(Z_SRED, f'<path d="M{bx+420:.0f},{by+200:.0f} q{-120*kor_t:.0f},{-20*kor_t:.0f} {-220*kor_t:.0f},{-10*kor_t:.0f}"'
                    f' fill="none" stroke="{MED}" stroke-width="10" opacity="{kor_t:.2f}"/>')
    s += SL(Z_SRED, f'<rect x="{bx+180:.0f}" y="{by+210:.0f}" width="380" height="40" rx="6" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{bx+180:.0f},{by+230:.0f} h-40" stroke="{POL2}" stroke-width="4" stroke-dasharray="4 6"/>')
    for i, sgn in enumerate((-1, 1, -1)):
        s += SL(Z_SRED, _svertok(bx - 160 + i * 60, by + 210 + sgn * 10, .9, t, (KRAS, TKAN2, ZEL2)[i], ZOL, i * .2))
    for i in range(3):
        s += SL(Z_LETIT, f'<line x1="{bx+500+i*10}" y1="{by-40-i*20}" x2="{bx+500+i*10+10*A.w(t,1.2,i*.3):.0f}" y2="{by+200}" stroke="#d8d0a8" stroke-width="2" opacity=".7"/>')
    s += SL(Z_SRED, f'<circle cx="{bx+440:.0f}" cy="{by+60:.0f}" r="26" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, kot(bx + 460, by + 230, t, .85, "#3b3430", False))
    shar_x = bx - 240 + 60 * ((t * 60) % 200) / 200
    s += SL(Z_SRED, f'<circle cx="{shar_x:.0f}" cy="{by+220:.0f}" r="22" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1339, 771, t, 0.51, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 45-51 ══════════════════════════════
def vnuk_prines_tapochki(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 29)
    s += SL(Z_DAL, _oboi_fon("#4a3a4a", "#3a2e3a"))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<circle cx="300" cy="500" r="80" fill="{STEKLO}" opacity=".55" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M500,500 v360" stroke="{ZHELEZ}" stroke-width="6"/><path d="M460,540 q40,-10 80,0" fill="none" stroke="{ZHELEZ}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="1500" y="720" width="160" height="140" rx="20" fill="{TKAN}" {o(4)}/>')
    s += SL(Z_SRED, kot(1400, 940, t, .9, "#3b3430", False))
    s += SL(Z_SRED, _kovrik_pol(760, 900, 500, 110, TKAN2, KREM, 37))
    pasyol = A.ease(A.seg(t, .2, 1.2))
    bx = 900 - pasyol * 120
    s += SL(Z_SRED, figura(700, 1020, 460, t, "#2a4a3a", "#cfd6de", False, .0, True, shapka=True))
    ruk1, (r1x, r1y) = rukav(760, 760, 140, -50, t, "#2a4a3a", "#cfd6de", .0, 4)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(700, 760, 140, -130, t, "#2a4a3a", "#cfd6de", .3, 4)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<rect x="{bx-80:.0f}" y="700" width="160" height="120" rx="10" fill="{TKAN2}" {o(4)}/>')
    s += SL(Z_SRED, figura(1100, 1020, 460, t, "#8c3a3a", KREM, True, .2))
    ruk2, (r2x, r2y) = rukav(1030, 760, 140, -140, t, "#8c3a3a", KREM, .2, 4)
    s += SL(Z_SRED, ruk2)
    ruk2b, (r2bx, r2by) = rukav(1100, 760, 140, -50, t, "#8c3a3a", KREM, .5, 4)
    s += SL(Z_SRED, ruk2b)
    s += SL(Z_SRED, figura(1420, 1080, 160, t, "#6b4428", KREM, False, .4))
    nadet = A.ease(A.seg(t, 1.6, 1.0))
    s += SL(Z_SRED, f'<g transform="rotate({-20*nadet:.1f} 1440 1060)">'
                    f'<path d="M1400,1060 q10,-20 60,-16 q20,2 20,16 q0,14 -40,16 q-40,2 -40,-16 Z" fill="#b8323a" {o(3)}/></g>')
    s += SL(Z_SRED, svecha(1392, 808, t, 0.88, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e14", .36))
    s += vinetka(.4)
    return s


def gostevye_tapochki_u_vhoda(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 31)
    s += SL(Z_DAL, _oboi_fon("#5a4a4a", "#4a3a3a"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _veshalka_seni(1420, 260, 420, t, 7))
    s += SL(Z_SRED, _kovrik_pol(700, 920, 500, 120, TKAN, KREM, 41))
    shx, shy, shw = 420, 760, 560
    s += SL(Z_SRED, f'<rect x="{shx:.0f}" y="{shy:.0f}" width="{shw}" height="40" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<ellipse cx="{shx+70+i*160:.0f}" cy="{shy-16:.0f}" rx="60" ry="22" fill="#8c3a3a" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{shx+shw-80:.0f}" cy="{shy-18:.0f}" rx="86" ry="28" fill="{ZEL2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{shx+shw-150:.0f}" y="{shy-40:.0f}" width="140" height="18" fill="none" stroke="{K}" stroke-width="3" opacity=".5"/>')
    diskx, disky = 1180, 700
    s += SL(Z_SRED, f'<rect x="{diskx-60:.0f}" y="{disky:.0f}" width="120" height="90" rx="10" fill="{POBEL}" {o(4)}/>')
    blikf = .5 + .5 * abs(A.w(t, 1.4))
    s += SL(Z_SRED, f'<circle cx="{diskx:.0f}" cy="{disky-10:.0f}" r="44" fill="#2a2a30" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{diskx:.0f}" cy="{disky-10:.0f}" r="34" fill="#fff" opacity="{.3+.4*blikf:.2f}"/>')
    sn = A.ease(A.seg(t, .3, 1.5))
    stoy = figura(760, 1040, 480, t, "#3a3a4a", "#cfd6de", False, .0, False)
    s += SL(Z_SRED, stoy)
    ruk1, (r1x, r1y) = rukav(820, 820, 140, -30, t, "#3a3a4a", "#cfd6de", .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(700, 820, 140, -170, t, "#3a3a4a", "#cfd6de", .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<path d="M820,1060 l0,{-60*sn:.0f} l40,{20*sn:.0f} Z" fill="#2a2420" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="700" cy="{1100-10*sn:.0f}" rx="56" ry="24" fill="#8c3a3a" {o(3)}/>')
    s += SL(Z_SRED, svecha(438, 862, t, 0.22, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def tri_pustyh_podarka(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 33)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(220, 760, 1480, 34))
    gifts = (("koshelek", 420), ("sumka", 900), ("vaza", 1380))
    for i, (kind, gx) in enumerate(gifts):
        app = A.ease(A.seg(t, i * 1.4, .6))
        if kind == "koshelek":
            s += SL(Z_SRED, _koshelek(gx, 740, 1.6))
        elif kind == "sumka":
            s += SL(Z_SRED, f'<path d="M{gx-70:.0f},740 q-10,-90 70,-90 q80,0 70,90 Z" fill="#5a3a26" {o(5)}/>')
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="700" rx="40" ry="14" fill="#1a1410"/>')
        else:
            s += SL(Z_SRED, f'<path d="M{gx-60:.0f},740 L{gx-40:.0f},600 L{gx+40:.0f},600 L{gx+60:.0f},740 Z" fill="{STEKLO}" opacity=".5" {o(4)}/>')
            dr = (t * 30) % 40
            s += SL(Z_SRED, f'<path d="M{gx:.0f},{620+dr:.0f} q10,20 0,40" fill="none" stroke="#cfe8ee" stroke-width="3" opacity=".5"/>')
        if app > .05:
            s += SL(Z_SRED, _zapret(gx, 560, 80, t, i * .3) if app > .98 else
                    f'<g opacity="{app:.2f}">' + _zapret(gx, 560, 80, t, i * .3) + '</g>')
    for i in range(3):
        kach = 3 * A.w(t, 1.1, i * .3)
        s += SL(Z_SRED, svecha(200 + i * 1500 // 2, 700, t, i * .2, .9))
    s += SL(Z_SRED, f'<path d="M700,620 l-30,-80 l60,0 Z" fill="{ZEL}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1140" cy="650" r="34" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1600" y="680" width="80" height="60" rx="6" fill="{KREM}" {o(3)}/>')
    razv = A.ease(A.seg(t, 1.8, 1.0))
    s += SL(Z_SRED, f'<path d="M{420+80*razv:.0f},700 q20,10 30,30" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def koshelek_s_monetoy_na_donyshke(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 35)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(220, 760, 1480, 34))
    s += SL(Z_SRED, _koshelek(420, 740, 1.6, True, 0))
    s += SL(Z_SRED, f'<path d="M900,740 q-10,-90 70,-90 q80,0 70,90 Z" fill="#5a3a26" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1320,740 L1340,600 L1420,600 L1440,740 Z" fill="{STEKLO}" opacity=".5" {o(4)}/>')
    pad = A.ease(A.seg(t % 3.0, .3, .8))
    mx, my = 420 + 10, 650 - (1 - pad) * 160
    s += SL(Z_SRED, f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="18" fill="url(#zol)" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1380" cy="700" rx="40" ry="20" fill="{KRAS}" {o(3)}/>')
    for i in range(4):
        fall = A.ease(A.seg(t % 3.0, 1.3 + i * .3, .5))
        s += SL(Z_SRED, f'<circle cx="{1380-30+i*18:.0f}" cy="{700-(1-fall)*120:.0f}" r="9" fill="{(KRAS,ZOL)[i%2]}" opacity="{.3+.7*fall:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M1280,700 q-30,-50 0,-90" fill="none" stroke="{KREM}" stroke-width="20" opacity=".9"/>')
    gone = A.ease(A.seg(t % 3.0, 2.3, .6))
    if gone < .95:
        s += SL(Z_SRED, f'<g opacity="{1-gone:.2f}">' + _zapret(420, 560, 80, t, .0) + _zapret(900, 560, 80, t, .3) + '</g>')
    for i in range(3):
        s += SL(Z_SRED, svecha(1650, 700, t, i * .3, .9))
    s += SL(Z_SRED, f'<path d="M620,650 q10,-30 30,0" fill="none" stroke="{ZOL}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(650, 1060, 460, t, "#6b3a4a", KREM, True, .0))
    s += SL(Z_SRED, f'<circle cx="760" cy="1000" r="18" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def gostincy_iz_svoego_sada(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    sneg_vid = nebo("den", t, True, 39) + SL(Z_LETIT, sneg_letit(t, 12, 20, .5, .6))
    s += SL(Z_DAL, okno_izby(1420, 140, 400, 340, t, vid=sneg_vid, moroz=.15, svet=True))
    s += SL(Z_SRED, f'<ellipse cx="1760" cy="260" rx="46" ry="60" fill="{POBEL}" {o(4)}/>')
    s += SL(Z_DAL, doski(0, 40, W, 720, 70))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, stol(160, 700, 980, 34))
    s += SL(Z_SRED, krynka(360, 690, 1.3, "url(#med)"))
    s += SL(Z_SRED, f'<path d="M560,700 q-10,-40 30,-50 q40,-10 50,20 q-20,30 -50,30 q-20,0 -30,0 Z" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="696" rx="80" ry="24" fill="{KREM}" {o(3)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<ellipse cx="{710+i*20:.0f}" cy="690" rx="16" ry="8" fill="#d8b878" opacity=".85"/>')
    bx, by, bw_, bh_ = 960, 360, 840, 440
    s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw_}" height="{bh_}" rx="10" fill="url(#derev)" {o(7)}/>')
    pw, ph_ = 760, 300
    px, py = bx + 40, by + 90
    put = kontur_proema(px, py, pw, ph_, "pryam")
    stok_content = krynka(px + pw * .3, py + ph_ * .8, .6, "url(#med)") + _napolnenie(px, py + ph_ * .5, pw, ph_ * .5, t, 44, 4)
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>' + stok_content)
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M{bx+bw_:.0f},{by+10:.0f} q40,{bh_*.5:.0f} 0,{bh_-20:.0f}" fill="none" stroke="#2a1d14" stroke-width="6"/>')
    s += SL(Z_SRED, figura(600, 1020, 480, t, "#5a4a3a", KREM, False, .0))
    zav = A.ease(A.seg(t, .3, 1.2))
    ruk1, (r1x, r1y) = rukav(540, 720, 140, -90, t, "#5a4a3a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(620, 720, 150, -10 - zav * 20, t, "#5a4a3a", KREM, .3, 4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<path d="M{r2x:.0f},{r2y:.0f} q{30*zav:.0f},{-10*zav:.0f} {50*zav:.0f},{10*zav:.0f}" fill="none" stroke="{MED}" stroke-width="4"/>')
    s += SL(Z_SRED, _napolnenie(900, 560, 260, 160, t, 40, 5))
    s += SL(Z_SRED, svecha(231, 809, t, 0.41, .8))
    s += SL(Z_PERED, ramka_pp("levo", "#120e0e", .32))
    s += vinetka(.4)
    return s


def podokonnik_s_konfetami(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    city = _oboi_fon("#2a3550", "#1e2638")
    for i in range(10):
        wx, wy = 60 + i * 190 % 1800, 80 + (i * 97) % 380
        on = ((t * 1.2 + i) % 4) > .6
        city += f'<rect x="{wx}" y="{wy}" width="26" height="36" fill="{SVET if on else "#3a4258"}" opacity="{.9 if on else .4}"/>'
    s += SL(Z_DAL, okno_izby(1360, 140, 420, 360, t, vid=city, moroz=0, svet=False))
    s += SL(Z_DAL, _oboi_fon("#5a4a5a", "#4a3a4a"))
    s += SL(Z_SRED, polovicy(800))
    px, py, pw = 1340, 500, 460
    s += SL(Z_SRED, f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw}" height="200" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{px+70:.0f}" cy="{py+40:.0f}" rx="50" ry="60" fill="{ZEL2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{px+180:.0f},{py+100:.0f} L{px+150:.0f},{py+20:.0f} L{px+210:.0f},{py+20:.0f} Z" fill="{ZEL2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{px+280:.0f}" y="{py+40:.0f}" width="60" height="80" rx="20" fill="url(#stekl)" opacity=".5" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<line x1="{px+300:.0f}" y1="{py+100-i*18:.0f}" x2="{px+320:.0f}" y2="{py+100-i*18:.0f}" stroke="{ZEL}" stroke-width="3"/>')
    bowl_x, bowl_y = 900, 760
    s += SL(Z_SRED, f'<ellipse cx="{bowl_x:.0f}" cy="{bowl_y:.0f}" rx="120" ry="34" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{bowl_x-120:.0f},{bowl_y:.0f} q0,70 120,70 q120,0 120,-70" fill="{KREM}" {o(4)}/>')
    nasyp = A.ease(A.seg(t, .3, 1.6))
    for i in range(int(10 * nasyp)):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<circle cx="{bowl_x-80+rnd.random()*160:.0f}" cy="{bowl_y-10-rnd.random()*40*nasyp:.0f}" r="14" fill="{(KRAS,ZOL,TKAN2)[i%3]}" {o(2)}/>')
    stoy = figura(900, 1060, 470, t, "#8c6a7a", KREM, False, .0)
    s += SL(Z_SRED, stoy)
    ruk1, (r1x, r1y) = rukav(840, 820, 140, -70, t, "#8c6a7a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(960, 820, 140, -150, t, "#8c6a7a", KREM, .3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, svecha(862, 798, t, 1.18, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e18", .36))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 52-59 ══════════════════════════════
def banka_s_konfetami_i_tarelka_s_yabl(t):
    s = f'<rect width="{W}" height="{H}" fill="{KAMEN2}"/>'
    s += SL(Z_DAL, kladka(0, 0, W, 900))
    s += SL(Z_SRED, polovicy(900, "url(#beton)"))
    dx = 960
    s += SL(Z_SRED, f'<rect x="{dx-220:.0f}" y="240" width="440" height="660" fill="#5a4a3a" {o(7)}/>')
    for yy in range(280, 860, 60):
        s += SL(Z_SRED, f'<line x1="{dx-220:.0f}" y1="{yy}" x2="{dx+220:.0f}" y2="{yy}" stroke="#3a2e22" stroke-width="3" opacity=".5"/>')
    s += SL(Z_SRED, f'<circle cx="{dx+140:.0f}" cy="560" r="16" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<circle cx="{dx-260:.0f}" cy="540" r="22" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{dx+260:.0f}" y="700" width="120" height="100" rx="10" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, _pochta_yashchiki(140, 400, 300, 240, 6))
    s += SL(Z_SRED, f'<path d="M700,860 l-40,-160 l80,0 Z" fill="#6b4428" {o(3)}/><ellipse cx="700" cy="860" rx="40" ry="10" fill="#9aa0a4" {o(2)}/>')
    s += SL(Z_SRED, _kovrik_pol(dx - 160, 850, 320, 60, TKAN, KREM, 45))
    perehod = A.ease(A.seg(t, .3, 1.6))
    tx = dx - 200 + perehod * 200
    s += SL(Z_SRED, figura(dx - 260, 1060, 460, t, "#5a5560", KREM, True, .0))
    ruk1, (r1x, r1y) = rukav(dx - 200, 800, 160, -50, t, "#5a5560", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(dx - 240, 800, 160, -130, t, "#5a5560", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<ellipse cx="{tx:.0f}" cy="760" rx="100" ry="24" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{tx-40:.0f}" cy="750" r="26" fill="{KRAS}" {o(2)}/><circle cx="{tx+40:.0f}" cy="750" r="26" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M{tx:.0f},700 v-180 q0,-20 40,-20 q40,0 40,20 v180 Z" fill="{STEKLO}" opacity=".55" {o(4)}/>')
    for i in range(5):
        jig = 4 * A.w(t, 1.3, i * .2)
        s += SL(Z_SRED, f'<circle cx="{tx+20+jig:.0f}" cy="{660-i*22:.0f}" r="10" fill="{(KRAS,ZOL)[i%2]}"/>')
    s += SL(Z_SRED, figura(dx + 240, 1060, 460, t, "#3a5a4a", KREM, False, .4, True))
    ruk2, (r2x, r2y) = rukav(dx + 180, 800, 160, -130, t, "#3a5a4a", KREM, .4, 3)
    s += SL(Z_SRED, ruk2)
    ruk2b, (r2bx, r2by) = rukav(dx + 220, 800, 160, -50, t, "#3a5a4a", KREM, .7, 3)
    s += SL(Z_SRED, ruk2b)
    s += SL(Z_SRED, svecha(226, 834, t, 0.74, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0c", .42))
    s += vinetka(.42)
    return s


def moneta_iz_otcovskogo_yaschika(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 47)
    s += SL(Z_DAL, _oboi_fon("#3a3a4a", "#2e2e3e"))
    s += SL(Z_SRED, polovicy(820))
    dx, dy, dw = 640, 640, 760
    s += SL(Z_SRED, f'<rect x="{dx:.0f}" y="{dy:.0f}" width="{dw}" height="200" rx="8" fill="url(#derev)" {o(6)}/>')
    yasch = A.ease(A.seg(t, 0, .4))
    s += SL(Z_SRED, f'<g transform="translate(0,{-20*yasch:.0f})">'
                    f'<rect x="{dx+30:.0f}" y="{dy+60:.0f}" width="{dw-60}" height="100" rx="6" fill="#4a3a28" {o(5)}/>')
    s += f'<rect x="{dx+60:.0f}" y="{dy+80:.0f}" width="100" height="60" rx="8" fill="{KREM}" {o(3)}/>'
    for i in range(3):
        s += f'<circle cx="{dx+85+i*24:.0f}" cy="{dy+110:.0f}" r="10" fill="url(#zol)" {o(2)}/>'
    s += f'<rect x="{dx+200:.0f}" y="{dy+90:.0f}" width="70" height="30" rx="4" fill="{ZHELEZ}" {o(2)}/>'
    for i in range(3):
        s += f'<circle cx="{dx+220+i*20:.0f}" cy="{dy+105:.0f}" r="6" fill="{ZOL}" {o(1)}/>'
    s += f'<rect x="{dx+310:.0f}" y="{dy+95:.0f}" width="26" height="40" rx="6" fill="{ZHELEZ}" {o(2)}/><rect x="{dx+344:.0f}" y="{dy+95:.0f}" width="26" height="40" rx="6" fill="{ZHELEZ}" {o(2)}/>'
    s += f'<path d="M{dx+410:.0f},{dy+130:.0f} L{dx+470:.0f},{dy+90:.0f} L{dx+478:.0f},{dy+100:.0f} L{dx+420:.0f},{dy+136:.0f} Z" fill="{ZHELEZ}" {o(2)}/>'
    for i in range(4):
        s += f'<line x1="{dx+500+i*10:.0f}" y1="{dy+90:.0f}" x2="{dx+500+i*10:.0f}" y2="{dy+140:.0f}" stroke="#2a1f14" stroke-width="3"/>'
    lupa_blik = .5 + .5 * abs(A.w(t, 1.6))
    s += f'<circle cx="{dx+600:.0f}" cy="{dy+100:.0f}" r="36" fill="none" stroke="{ZHELEZ}" stroke-width="6"/>'
    s += f'<circle cx="{dx+600:.0f}" cy="{dy+100:.0f}" r="30" fill="#cfe8ee" opacity="{.3+.5*lupa_blik:.2f}"/>'
    s += f'<rect x="{dx+36:.0f}" y="{dy+160:.0f}" width="90" height="26" fill="#efe3c8" opacity=".6" {o(2)}/>'
    s += '</g>'
    s += SL(Z_SRED, figura(dx + 60, 1060, 480, t, "#4a3a2c", KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(dx + 140, 820, 150, -40, t, "#4a3a2c", KREM, .0)
    s += SL(Z_SRED, ruk1)
    beret = A.ease(A.seg(t, .8, .8))
    s += SL(Z_SRED, f'<circle cx="{dx+120+beret*20:.0f}" cy="{820-beret*60:.0f}" r="20" fill="url(#zol)" {o(2)}/>')
    s += SL(Z_SRED, figura(dx + 460, 1040, 480, t, "#6b2a44", KREM, False, .3, True))
    ruk2a, (r2ax, r2ay) = rukav(dx + 380, 780, 150, 160, t, "#6b2a44", KREM, .3)
    s += SL(Z_SRED, ruk2a)
    ruk2b, (r2bx, r2by) = rukav(dx + 420, 780, 150, -140, t, "#6b2a44", KREM, .6)
    s += SL(Z_SRED, ruk2b)
    kopeek = A.ease(A.seg(t, 1.8, .5))
    s += SL(Z_SRED, f'<rect x="{(r2ax+r2bx)/2-50:.0f}" y="{(r2ay+r2by)/2-20:.0f}" width="100" height="40" rx="6" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    if kopeek > .05:
        s += SL(Z_SRED, f'<circle cx="{(r2ax+r2bx)/2+beret*20*0:.0f}" cy="{(r2ay+r2by)/2+kopeek*10:.0f}" r="18" fill="url(#zol)" opacity="{min(1,kopeek*2):.2f}"/>')
    s += SL(Z_SRED, svecha(756, 844, t, 0.44, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def zerkalo_dver(t):
    s = f'<rect width="{W}" height="{H}" fill="{NOCH}"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="{K}" opacity=".3"/>')
    mx, my, mw, mh = 960, 480, 480, 600
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{mw*.52:.0f}" ry="{mh*.52:.0f}" fill="url(#zol)" {o(8)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{mw*.44:.0f}" ry="{mh*.44:.0f}" fill="#0a1420" {o(3)}/>')
    otkr = A.ease(A.seg(t, .4, 1.6))
    s += SL(Z_SRED, f'<path d="M{mx-20:.0f},{my-mh*.42:.0f} l{-40-80*otkr:.0f},10 l0,{mh*.8:.0f} l{40+80*otkr:.0f},10 Z" fill="#0a1420" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{mx-60-80*otkr:.0f},{my-mh*.3:.0f} v{mh*.6:.0f}" stroke="#3a7fb0" stroke-width="{10+30*otkr:.0f}" opacity="{.3+.5*otkr:.2f}"/>')
    s += SL(Z_SRED, f'<rect x="{mx-160:.0f}" y="{my+mh*.48:.0f}" width="320" height="60" rx="10" fill="url(#derev)" {o(5)}/>')
    for i, sgn in enumerate((-1, 1)):
        tyan = 10 * A.ease(A.seg(t, otkr + .1, .6))
        s += SL(Z_SRED, svecha(mx + sgn * 120, my + mh * .48, t, i * .3, 1.0 + .2 * otkr))
    s += SL(Z_SRED, f'<circle cx="{mx-40:.0f}" cy="{my+mh*.48:.0f}" r="20" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{mx+60:.0f}" cy="{my+mh*.5:.0f}" rx="30" ry="10" fill="{KREM}" {o(2)}/><circle cx="{mx+60:.0f}" cy="{my+mh*.5:.0f}" r="8" fill="{ZOL}" {o(1)}/>')
    s += SL(Z_SRED, f'<path d="M{mx+100:.0f},{my+mh*.48:.0f} q30,10 20,40" fill="none" stroke="{SVET}" stroke-width="4"/>')
    naklon = 3 * A.ease(A.seg(t, 1.2, 1.0))
    stoy = figura(mx, my + mh * .9, 420, t, "#8c6a9a", KREM, False, .0, naklon=naklon)
    s += SL(Z_SRED, stoy)
    s += SL(Z_SRED, f'<path d="M{mx-20:.0f},{my+mh*.6:.0f} q30,20 0,80" fill="none" stroke="{K}" stroke-width="8"/>')
    s += SL(Z_SRED, _napolnenie(1400, 700, 440, 180, t, 207, 8))
    s += SL(Z_PERED, ramka_pp("oba", "#060608", .48))
    s += vinetka(.5)
    return s


def devushka_u_tryumo(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 51)
    s += SL(Z_DAL, _oboi_fon())
    s += SL(Z_SRED, polovicy(840))
    tx, ty, tw = 960, 320, 760
    for i, sgn in enumerate((-1, 0, 1)):
        px = tx + sgn * tw * .34
        s += SL(Z_SRED, f'<rect x="{px-tw*.16:.0f}" y="{ty:.0f}" width="{tw*.32:.0f}" height="500" rx="8" fill="url(#zol)" {o(6)}/>')
        s += SL(Z_SRED, f'<rect x="{px-tw*.13:.0f}" y="{ty+16:.0f}" width="{tw*.26:.0f}" height="468" fill="#0a1420" {o(3)}/>')
        vid = ("young", "mid", "babka")[i]
        s += SL(Z_SRED, _tryumo_otrazhenie(px, ty + 430, .72, t, vid))
    s += SL(Z_SRED, f'<rect x="{tx-200:.0f}" y="{ty+500:.0f}" width="400" height="60" rx="10" fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{tx-120+i*110:.0f},{ty+480:.0f} q0,-40 16,-40 q16,0 16,40 Z" fill="{STEKLO}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{tx+180:.0f}" cy="{ty+470:.0f}" rx="40" ry="20" fill="#efe3c8" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M{tx-150:.0f},{ty+460:.0f} q20,-16 40,0" fill="none" stroke="{ZOL}" stroke-width="3"/>')
    for i in range(5):
        kach = 3 * A.w(t, 1.2, i * .2)
        s += SL(Z_SRED, f'<circle cx="{tx-180+i*20+kach:.0f}" cy="{ty+440:.0f}" r="10" fill="#fdf8ec" {o(2)}/>')
    s += SL(Z_SRED, figura(tx, ty + 1000, 420, t, "#efe3c8", KRAS, False, .0))
    lokon = A.ease(A.seg(t % 3.0, 0, .5))
    ruk1, (r1x, r1y) = rukav(tx - 60, ty + 820, 140, -90 + lokon * 10, t, "#efe3c8", KRAS, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(tx + 60, ty + 820, 140, -170, t, "#efe3c8", KRAS, .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<circle cx="{r2x:.0f}" cy="{r2y:.0f}" r="18" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, svecha(332, 788, t, 1.48, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def pudrenica_s_zerkalcem(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 53)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 700, 1100, 34))
    kx, ky = 1240, 760
    s += SL(Z_SRED, f'<rect x="{kx-260:.0f}" y="{ky:.0f}" width="520" height="130" rx="18" fill="{TKAN}" {o(5)}/>')
    px, py, pw, ph_ = kx - 190, ky - 330, 380, 330
    put = kontur_proema(px, py, pw, ph_, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(6)}/>')
    s += SL(Z_SRED, f'<circle cx="{kx:.0f}" cy="{ky+30:.0f}" r="110" fill="#8c3a3a" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+200:.0f}" y="{ky-10:.0f}" width="30" height="100" rx="10" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+260:.0f}" y="{ky+20:.0f}" width="80" height="26" rx="8" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M{kx-280:.0f},{ky+10:.0f} q40,-10 80,0 l0,30 q-40,10 -80,0 Z" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+320:.0f}" y="{ky-40:.0f}" width="120" height="80" rx="6" fill="{KREM}" {o(3)}/>')
    bant_sh = 6 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<path d="M{kx+380+bant_sh:.0f},{ky-50:.0f} q-30,10 -10,30 q20,-6 10,-30 Z" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx+540:.0f}" cy="{ky+40:.0f}" rx="60" ry="22" fill="{POL}" {o(3)}/>')
    s += SL(Z_SRED, par(kx + 540, ky + 20, t, 3, .4, 70))
    fx = kx - 300
    s += SL(Z_SRED, figura(fx, 1060, 480, t, "#5a6a4a", KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(fx + 80, 753, 160, -28, t, "#5a6a4a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    puh = 10 * A.w(t, 2.0)
    ruk2, (r2x, r2y) = rukav(fx - 70, 780, 140, -30 + puh * .2, t, "#5a6a4a", KREM, .4, 3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<circle cx="{r2x:.0f}" cy="{r2y:.0f}" r="22" fill="#fdf8ec" opacity=".85"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.4)
    return s


def slezy_rusalki(t):
    s = f'<rect width="{W}" height="{H}" fill="{NOCH}"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 55))
    s += SL(Z_DAL, f'<circle cx="1620" cy="220" r="90" fill="{KREM}" opacity=".9" {o(2)}/><circle cx="1620" cy="220" r="130" fill="{KREM}" opacity=".18"/>')
    s += SL(Z_SRED, f'<path d="M0,760 q960,-40 1920,0 l0,80 q-960,40 -1920,0 Z" fill="url(#voda)" {o(4)}/>')
    kach = 2 * A.w(t, 2.4)
    for i in range(6):
        s += SL(Z_SRED, f'<line x1="{200+i*60+kach}" y1="900" x2="{196+i*60}" y2="700" stroke="{ZEL}" stroke-width="7"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<ellipse cx="{1400+i*90}" cy="{800+10*math.sin(t+i)}" rx="36" ry="12" fill="{ZEL2}" {o(2)}/>')
    s += SL(Z_DAL, f'<path d="M1600,900 q0,-200 -60,-260" stroke="#2a2a2a" stroke-width="16" fill="none"/>')
    s += SL(Z_DAL, goloe_derevo(1700, 900, 380, t, 5, 6, inej_=True))
    s += SL(Z_SRED, f'<path d="M1500,820 q60,-30 140,-10 l0,30 q-70,20 -140,0 Z" fill="#6b4428" {o(4)}/>')
    kx, ky = 760, 820
    rkx, rky = 880, 600
    s += SL(Z_SRED, f'<ellipse cx="{rkx:.0f}" cy="{rky:.0f}" rx="230" ry="50" fill="{KAMEN}" opacity=".9" {o(4)}/>')
    s += SL(Z_SRED, _rusalka(rkx, rky - 6, 300, t))
    s += SL(Z_SRED, f'<rect x="{kx-100:.0f}" y="{ky:.0f}" width="200" height="110" rx="16" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kx-70:.0f}" y="{ky-10:.0f}" width="140" height="18" fill="#0a1420" {o(2)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{kx-50+i*24:.0f}" cy="{ky+40:.0f}" r="10" fill="#f4f0e2" {o(2)}/>')
    s += SL(Z_SRED, svecha(1180, 780, t, 1.4, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#040608", .5))
    s += vinetka(.52)
    return s


def mamina_shkatulka_s_zhemchugom(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 59)
    s += SL(Z_DAL, _oboi_fon("#4a3a3a", "#3a2e2e"))
    s += SL(Z_SRED, polovicy(820))
    dx, dy, dw = 740, 700, 700
    s += SL(Z_SRED, f'<rect x="{dx:.0f}" y="{dy:.0f}" width="{dw}" height="160" rx="10" fill="url(#derev)" {o(6)}/>')
    skx, sky = dx + 350, dy - 220
    s += SL(Z_SRED, f'<rect x="{skx-230:.0f}" y="{sky-10:.0f}" width="460" height="400" rx="16" fill="#6b3a4a" {o(6)}/>')
    px, py, pw, ph_ = skx - 200, sky + 10, 400, 360
    put = kontur_proema(px, py, pw, ph_, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(6)}/>')
    sping = (t * 180) % 360
    s += SL(Z_SRED, f'<g transform="translate({dx+100:.0f},{dy-40:.0f}) rotate({sping:.1f})">'
                    f'<ellipse cx="0" cy="0" rx="10" ry="30" fill="#efe3c8" {o(2)}/></g>')
    s += SL(Z_SRED, f'<path d="M{dx+200:.0f},{dy-60:.0f} q40,-10 40,-60" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<circle cx="{dx-180:.0f}" cy="{dy+20:.0f}" r="26" fill="url(#stekl)" opacity=".7" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{dx-80:.0f},{dy+10:.0f} l40,-20 l-6,30 Z" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{dx+dw+30:.0f}" y="{dy+30:.0f}" width="90" height="70" rx="4" fill="{KREM}" opacity=".9" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{dx+dw+140:.0f}" y="{dy+10:.0f}" width="70" height="90" rx="4" fill="url(#derev)" {o(3)}/>')
    s += SL(Z_SRED, _elka(dx + dw + 250, dy + 200, 220, t, 11))
    s += SL(Z_SRED, figura(dx - 60, 1040, 480, t, "#6b2a38", KREM, False, .0))
    zastyog = A.ease(A.seg(t, .5, 1.2))
    ruk1, (r1x, r1y) = rukav(dx + 10, 820, 140, -140 + zastyog * 10, t, "#6b2a38", KREM, .0)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(dx - 130, 820, 140, -40 - zastyog * 10, t, "#6b2a38", KREM, .3)
    s += SL(Z_SRED, ruk2)
    cypo = 8 * A.ease(A.seg(t, 1.0, 1.0)) % 8
    s += SL(Z_SRED, figura(dx - 380, 1080 - cypo, 260, t, "#cfe4f5", SVET, False, .4))
    s += SL(Z_SRED, f'<path d="M{dx-320:.0f},1040 h40" stroke="{K}" stroke-width="4" opacity=".4"/>')
    s += SL(Z_SRED, svecha(373, 867, t, 1.23, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 60-68 ══════════════════════════════
def spornye_podarki_na_vesah(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 61)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(560, 760, 800, 34))
    nak = 30 * math.sin(t * .7)
    s += SL(Z_SRED, _vesy(960, 760, 1.5, t, nak, 5))
    cycle = (t * .4) % 3.0
    stage = int(cycle)
    item_svg = (
        f'<rect x="-40" y="-14" width="80" height="28" rx="10" fill="{KRAS}" {o(3)}/><rect x="-40" y="4" width="80" height="4" fill="{KREM}"/>',
        f'<path d="M-50,10 q0,-40 50,-40 q50,0 50,40 l0,10 l-100,0 Z" fill="#6b4428" {o(3)}/>',
        f'<rect x="-10" y="-50" width="20" height="60" rx="6" fill="{KREM}" {o(2)}/><circle cx="0" cy="-54" r="8" fill="{SVET}"/>')[stage]
    nak_r = math.radians(nak)
    for sgn in (-1, 1):
        ipx = 960 + sgn * 150 * math.cos(nak_r) * 1.5 - nak * 0
        ipy = 760 - 220 * 1.5 + sgn * 150 * math.sin(nak_r) * 1.5 - 120 * 1.5
    s += SL(Z_SRED, f'<g transform="translate({960-150*1.5*math.cos(nak_r):.0f},{760-220*1.5+150*1.5*math.sin(nak_r)-100*1.5:.0f})">{item_svg}</g>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="700" rx="40" ry="16" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1160" cy="700" r="30" fill="{KRAS}" {o(2)}/>')
    stoy1 = figura(600, 1020, 460, t, "#6b4a3a", KREM, True, .0)
    s += SL(Z_SRED, stoy1)
    da = 10 * A.w(t, 1.1)
    ruk1, _ = rukav(680, 780, 130, -60 + da, t, "#6b4a3a", KREM, .0, 5)
    s += SL(Z_SRED, ruk1)
    stoy2 = figura(1320, 1020, 460, t, "#4a5a6b", KREM, False, .3, True)
    s += SL(Z_SRED, stoy2)
    net = 10 * A.w(t, 1.3, .4)
    ruk2, _ = rukav(1240, 780, 130, -120 - net, t, "#4a5a6b", KREM, .3, 5)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, par(760, 680, t, 3, .4, 70))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def monetka_na_krasnoy_varezhke(t):
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += SL(Z_NEBO, teplo(960, 300, 900, 500, .5))
    s += SL(Z_DAL, _elka(260, 940, 460, t, 13))
    s += SL(Z_DAL, _elka(1700, 920, 440, t, 14))
    s += SL(Z_DAL, okno_izby(1560, 140, 220, 220, t, svet=True, moroz=.2))
    for i in range(3):
        s += SL(Z_SRED, svecha(1200 + i * 60, 820, t, i * .3, .9))
    gifts = (("chasy", 320), ("nozhnicy", 500), ("platok", 660), ("tapochki", 820),
             ("koshelek", 980), ("zerkalo", 1120), ("zhemchug", 1260))
    for i, (kind, gx) in enumerate(gifts):
        jit = 2 * A.w(t, .35, i * .1)
        if kind == "chasy":
            s += SL(Z_SRED, _chasy_sten(gx, 700, .55, t))
        elif kind == "nozhnicy":
            s += SL(Z_SRED, _nozhnicy_bolshie(gx, 760, 90, t))
        elif kind == "platok":
            s += SL(Z_SRED, f'<rect x="{gx-30:.0f}" y="720" width="60" height="60" fill="{TKAN}" {o(2)}/>')
        elif kind == "tapochki":
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="750" rx="40" ry="18" fill="#8c3a3a" {o(2)}/>')
        elif kind == "koshelek":
            s += SL(Z_SRED, _koshelek(gx, 760, .8))
        elif kind == "zerkalo":
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="740" rx="36" ry="48" fill="url(#zol)" {o(3)}/><ellipse cx="{gx:.0f}" cy="740" rx="26" ry="38" fill="#0a1420"/>')
        else:
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="750" rx="40" ry="14" fill="#f4f0e2" {o(2)}/>')
        s += SL(Z_SRED, f'<g transform="translate({jit:.0f},0)">' + _zapret(gx, 700, 50, t, i * .2) + '</g>')
    vx, vy = 640, 960
    s += SL(Z_SRED, _varezhka(vx, vy, 3.0, 6 * A.w(t, 1.4)))
    s += SL(Z_SRED, f'<circle cx="{vx-30:.0f}" cy="{vy-70:.0f}" r="26" fill="url(#med)" {o(3)}/>')
    luch_x = vx + 20 + ((t * 200) % 900)
    s += SL(Z_SRED, f'<line x1="{vx:.0f}" y1="{vy-80:.0f}" x2="{luch_x:.0f}" y2="700" stroke="{SVET}" stroke-width="5" opacity=".7"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#1a0e08", .3))
    s += SL(Z_LETIT, sneg_letit(t, 16, 63, .4, .6))
    s += vinetka(.36)
    return s


def podarok_s_yarlykom(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 65)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(260, 740, 1400, 40))
    s += SL(Z_SRED, _schyoty(680, 680, .9, t))
    s += SL(Z_SRED, f'<rect x="860" y="680" width="200" height="30" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1120" y="640" width="160" height="110" rx="8" fill="{TKAN}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1140" y="660" width="120" height="70" fill="#2a1f14" {o(2)}/>')
    bx = 1500
    s += SL(Z_SRED, _korobka(bx, 620, 220, 150, t, TKAN2, ZOL, True, .0, .1))
    ярlyk_y = 600 + 20 * A.ease(A.seg(t, .4, .8)) % 20
    s += SL(Z_SRED, f'<line x1="{bx+40:.0f}" y1="{560:.0f}" x2="{bx+40:.0f}" y2="{ярlyk_y:.0f}" stroke="{K}" stroke-width="2"/>')
    s += SL(Z_SRED, f'<rect x="{bx+10:.0f}" y="{ярlyk_y:.0f}" width="60" height="36" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1000" cy="700" rx="70" ry="24" fill="#6b4428" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M940,690 h120" stroke="{KREM}" stroke-width="4" opacity=".6"/>')
    s += SL(Z_SRED, f'<circle cx="400" cy="700" r="28" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1760, 720, t, .4, .9))
    stoy = figura(500, 1040, 480, t, "#4a3a2c", KREM, True, .0)
    s += SL(Z_SRED, stoy)
    ruk1, (r1x, r1y) = rukav(560, 800, 140, -40, t, "#4a3a2c", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    mig = A.ease(A.seg(t % 4.0, 2.0, .3)) * (1 - A.ease(A.seg(t % 4.0, 2.3, .3)))
    ruk2, (r2x, r2y) = rukav(bx - 60, 800, 150, -140, t, "#4a3a2c", KREM, .3, 3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{500-40:.0f}" cy="{960-60*mig:.0f}" rx="14" ry="{10*(1-mig*.6):.0f}" fill="{K}"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def primeta_uhodit(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 67)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="200" y="700" width="1520" height="60" rx="10" fill="{KREM}" {o(5)}/>')
    bx = 900
    s += SL(Z_SRED, _korobka(bx, 580, 220, 150, t, TKAN2, SVET, True, .3, .1))
    uhodit = A.ease(A.seg(t, .4, 1.6))
    s += SL(Z_SRED, _primeta_vorona(bx + 20, 560, .9, t, uhodit))
    zvon = 1 - A.ease(A.seg(t, 0, .3))
    s += SL(Z_SRED, f'<circle cx="{bx+40:.0f}" cy="640" r="16" fill="url(#zol)" opacity="{max(0,zvon):.2f}" {o(2)}/>')
    cross = A.ease(A.seg(t, .2, .5))
    if cross < .95:
        s += SL(Z_SRED, f'<g opacity="{1-cross:.2f}">' + _zapret(bx, 700, 50, t, 0) + '</g>')
    if cross > .1:
        s += SL(Z_SRED, f'<g opacity="{cross:.2f}">' + _galochka(bx, 700, 1.0, t, 0) + '</g>')
    s += SL(Z_SRED, svecha(400, 700, t, .2, .9))
    s += SL(Z_SRED, svecha(1500, 700, t, .5, .9))
    s += SL(Z_SRED, f'<circle cx="640" cy="700" r="26" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1200" y="690" width="90" height="60" rx="6" fill="{KREM}" {o(3)}/>')
    lenta = 5 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<path d="M1350,700 q{20+lenta:.0f},10 10,30" fill="none" stroke="{KRAS}" stroke-width="6"/>')
    s += SL(Z_SRED, f'<ellipse cx="1660" cy="700" rx="60" ry="22" fill="{KREM}" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def tri_vykuplennyh_podarka(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 69)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="260" y="700" width="1400" height="70" rx="12" fill="{KREM}" {o(5)}/>')
    items = (("nozh", 500), ("chasy", 960), ("platok", 1420))
    for i, (kind, gx) in enumerate(items):
        if kind == "nozh":
            s += SL(Z_SRED, f'<path d="M{gx-80:.0f},700 h160 l-20,-24 h-120 Z" fill="{ZHELEZ}" {o(3)}/><rect x="{gx-30:.0f}" y="674" width="60" height="18" rx="4" fill="#5a3a26" {o(2)}/>')
        elif kind == "chasy":
            s += SL(Z_SRED, _chasy_karman(gx, 660, 1.0, t))
        else:
            s += SL(Z_SRED, f'<path d="M{gx-60:.0f},700 l120,0 l-20,-40 l-80,0 Z" fill="{TKAN}" {o(3)}/>')
        app = A.ease(A.seg(t, i * 1.0, .5))
        moneta_y = 650 - (1 - app) * 150
        s += SL(Z_SRED, f'<circle cx="{gx:.0f}" cy="{moneta_y:.0f}" r="16" fill="url(#zol)" {o(2)}/>')
        if app > .98:
            s += SL(Z_SRED, _galochka(gx, 600, .9, t, i * .2))
    s += SL(Z_SRED, f'<path d="M700,690 h40" stroke="{KREM}" stroke-width="4" opacity=".5"/>')
    s += SL(Z_SRED, svecha(300, 700, t, .3, .9))
    s += SL(Z_SRED, f'<path d="M1180,620 l-30,-70 l60,0 Z" fill="{ZEL}" {o(3)}/>')
    mand_x = 1650 + 20 * math.sin(t * 1.2)
    s += SL(Z_SRED, f'<circle cx="{mand_x:.0f}" cy="700" r="24" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1750" cy="690" rx="70" ry="24" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="150" cy="660" r="20" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def s_tebya_kopeyka(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 71)
    s += SL(Z_DAL, _oboi_fon("#5a3a4a", "#4a2e3a"))
    s += SL(Z_DAL, _elka(1600, 960, 520, t, 17))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, f'<rect x="120" y="760" width="320" height="140" rx="20" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="80" y="620" width="40" height="280" fill="{ZHELEZ}" {o(4)}/><ellipse cx="100" cy="610" rx="60" ry="20" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="500" cy="840" rx="70" ry="24" fill="{KREM}" {o(3)}/><path d="M460,830 l-40,-80 l40,20 l30,60 Z" fill="#6b4428" {o(3)}/>')
    s += SL(Z_SRED, kot(600, 900, t, .85, "#3b3430", False))
    for i in range(3):
        s += SL(Z_SRED, _svertok(1500 + i * 60, 900, .9, t, (KRAS, TKAN2, ZEL2)[i], ZOL, i * .2))
    s += SL(Z_SRED, hodiki(1760, 420, t, .9))
    topnуt = 10 * abs(math.sin(t * 3))
    stoy1 = figura(820, 1040 - topnуt * .3, 460, t, "#8c3a6a", KREM, False, .0)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(900, 800, 150, -40, t, "#8c3a6a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, _korobka(r1x + 40, r1y - 30, 140, 100, t, TKAN2, ZOL, True, .0, .2))
    ruk1b, (r1bx, r1by) = rukav(780, 820, 140, -160, t, "#8c3a6a", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, _oblachko(820, 680, .7, t, .2, "moneta"))
    stoy2 = figura(1200, 1040, 470, t, "#3a5a6b", KREM, False, .3, True)
    s += SL(Z_SRED, stoy2)
    hlopok = abs(A.w(t, .6)) > .8
    ruk2, (r2x, r2y) = rukav(1140, 800, 140, -110 + (10 if hlopok else 0), t, "#3a5a6b", KREM, .3)
    s += SL(Z_SRED, ruk2)
    ruk2b, (r2bx, r2by) = rukav(1260, 800, 150, -70, t, "#3a5a6b", KREM, .6)
    s += SL(Z_SRED, ruk2b)
    s += SL(Z_SRED, svecha(1021, 789, t, 0.29, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e18", .36))
    s += vinetka(.4)
    return s


def pokupayu(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("noch", t, True, 73)
    s += SL(Z_DAL, _oboi_fon("#3a3a4a", "#2e2e3e"))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _veshalka_seni(1380, 260, 420, t, 9))
    s += SL(Z_SRED, f'<rect x="420" y="640" width="200" height="220" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="520" cy="720" rx="80" ry="40" fill="url(#zol)" {o(3)}/>')
    kach = 4 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 900 600)"><circle cx="900" cy="600" r="80" fill="{ZEL}" {o(4)}/>'
                    f'<circle cx="870" cy="590" r="10" fill="{KRAS}"/><circle cx="930" cy="610" r="10" fill="{KRAS}"/>'
                    f'<path d="M900,520 q30,30 0,80" fill="none" stroke="{KRAS}" stroke-width="6"/></g>')
    s += SL(Z_SRED, _kovrik_pol(760, 900, 500, 110, TKAN, KREM, 77))
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{500+i*20:.0f}" cy="728" r="8" fill="{ZOL}" opacity="{.6+.4*abs(A.w(t,1.2,i*.2)):.2f}"/>')
    s += SL(Z_SRED, figura(900, 1060, 480, t, "#5a6a4a", KREM, False, .0, False, shapka=False))
    ruk1, (r1x, r1y) = rukav(840, 800, 150, -70, t, "#5a6a4a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, _korobka(r1x + 30, r1y - 20, 160, 130, t, TKAN2, SVET, True, .0, .2))
    s += SL(Z_SRED, f'<rect x="{r1x+60:.0f}" y="{r1y-10:.0f}" width="100" height="90" rx="6" fill="url(#zol)" {o(3)}/>')
    s += SL(Z_SRED, figura(1220, 1060, 470, t, "#8c3a6a", SVET, False, .3, True))
    moneta = A.ease(A.seg(t, .5, 1.0))
    ruk2, (r2x, r2y) = rukav(1150, 800, 140, -150 + moneta * 20, t, "#8c3a6a", SVET, .3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<circle cx="{r2x+20*moneta:.0f}" cy="{r2y-10*moneta:.0f}" r="14" fill="url(#zol)" {o(2)}/>')
    ruk3, (r3x, r3y) = rukav(1290, 800, 140, -30 - moneta * 10, t, "#8c3a6a", SVET, .6)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, svecha(915, 835, t, 1.55, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c10", .4))
    s += vinetka(.42)
    return s


# ═══ из chast3.py ═══
def _oblako_rechi(x, y, s_, t, ph, nastroenie):
    """Облачко-реакция над подарком: grust/pusto/radost."""
    rise = 8 * A.w(t, 1.6, ph)
    s = (f'<ellipse cx="{x:.0f}" cy="{y+rise:.0f}" rx="{64*s_:.0f}" ry="{42*s_:.0f}"'
         f' fill="#ffffff" opacity=".92" {o(4)}/>')
    s += (f'<circle cx="{x-50*s_:.0f}" cy="{y+28*s_+rise:.0f}" r="{10*s_:.0f}" fill="#ffffff" opacity=".9" {o(2)}/>')
    cy_ = y + rise
    if nastroenie == "grust":
        s += f'<ellipse cx="{x:.0f}" cy="{cy_-4*s_:.0f}" rx="{14*s_:.0f}" ry="{18*s_:.0f}" fill="#6f7f8c" opacity=".8"/>'
        s += f'<path d="M{x-10*s_:.0f},{cy_+16*s_:.0f} q4,{10*s_:.0f} 0,{18*s_:.0f}" fill="none" stroke="{STEKLO}" stroke-width="3"/>'
    elif nastroenie == "pusto":
        s += f'<line x1="{x-16*s_:.0f}" y1="{cy_:.0f}" x2="{x+16*s_:.0f}" y2="{cy_:.0f}" stroke="{K}" stroke-width="3" stroke-dasharray="4 5" opacity=".5"/>'
    else:
        s += f'<circle cx="{x:.0f}" cy="{cy_-2*s_:.0f}" r="{14*s_:.0f}" fill="{SVET}" {o(2)}/>'
        s += f'<path d="M{x-16*s_:.0f},{cy_+16*s_:.0f} l{32*s_:.0f},0 l{-16*s_:.0f},{16*s_:.0f} Z" fill="#6b4428" {o(2)}/>'
        s += f'<path d="M{x-6*s_:.0f},{cy_-2*s_:.0f} q6,8 12,0" fill="none" stroke={K!r}/>'.replace("={K!r}", f'="{K}" stroke-width="2"')
    return s


def _olenok(x, y, h_, t):
    """Молодой олень (детская игрушка/силуэт) — не используется, резерв."""
    return ""


# ═══════════════════════════ 69-73 ══════════════════════════════
def pustoe_napolnyayut(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 73)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 740, 1200, 34))
    s += SL(Z_SRED, f'<ellipse cx="760" cy="720" rx="110" ry="30" fill="{CHUGUN}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M650,720 q110,-50 220,0" fill="none" stroke={K!r}'.replace("={K!r}", f'="{K}"') + ' stroke-width="4" opacity=".4"/>')
    s += SL(Z_SRED, _korobka(760, 660, 40, 24, t, KRAS, ZOL, True, .2))
    s += SL(Z_SRED, _koshelek(1140, 740, 1.4, True, 0))
    bounce = abs(math.sin(t * 2.6))
    mx, my = 940, 700 - bounce * 80
    s += SL(Z_SRED, f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="16" fill="url(#zol)" {o(2)}/>')
    sypet = A.ease(A.seg(t % 4.0, 2.0, 1.6))
    for i in range(int(6 * sypet)):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<circle cx="{700+rnd.random()*120:.0f}" cy="{700-rnd.random()*20:.0f}" r="18" fill="{ZOL}" {o(2)}/>')
    if sypet > .3:
        s += SL(Z_SRED, f'<rect x="1090" y="700" width="90" height="36" rx="4" fill="{ZEL2}" opacity="{sypet:.2f}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M500,690 q30,-20 60,0" fill="none" stroke="{MED}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="400" y="700" width="120" height="30" rx="6" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1400,690 q-10,-60 30,-70 q40,10 30,70 Z" fill="url(#zol)" {o(3)}/>')
    s += SL(Z_SRED, par(1340, 660, t, 3, .4, 70))
    ruk1, (r1x, r1y) = rukav(820, 560, 180, 100, t, "#5a4a3a", KREM, .0, 4)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def meloch_na_prazdnichnyy_vecher(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 74)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(260, 760, 1400, 36))
    s += SL(Z_SRED, f'<rect x="700" y="640" width="280" height="40" rx="8" fill="{TKAN}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M900,700 l-30,70 l50,0 Z" fill="{KREM}" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, svecha(400 + i * 60, 700, t, i * .2, .9))
    s += SL(Z_SRED, f'<ellipse cx="620" cy="700" rx="80" ry="24" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1200,660 v60" stroke="{STEKLO}" stroke-width="40" opacity=".7"/>')
    bx, by = 1500, 760
    s += SL(Z_SRED, f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="230" ry="60" fill="{POBEL}" {o(4)}/>')
    put = kontur_proema(bx - 190, by - 160, 380, 320, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(bx - 190, by - 160, 380, 320, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(5)}/>')
    s += SL(Z_SRED, figura(900, 1040, 480, t, "#6b4a3a", KREM, False, .0))
    sypet = A.seg(t % 3.0, 0, 2.2)
    ruk1, (r1x, r1y) = rukav(960, 760, 150, -40, t, "#6b4a3a", KREM, .0, 4)
    s += SL(Z_SRED, ruk1)
    for i in range(5):
        fall = A.ease(A.seg(t % 3.0, i * .3, .5))
        s += SL(Z_SRED, f'<circle cx="{r1x-10+i*8:.0f}" cy="{r1y+20+(1-fall)*(-60):.0f}" r="7" fill="{(ZOL,MED)[i%2]}" opacity="{.4+.6*fall:.2f}"/>')
    ruk2, (r2x, r2y) = rukav(840, 760, 150, -140, t, "#6b4a3a", KREM, .3, 3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<rect x="{r2x-20:.0f}" y="{r2y-10:.0f}" width="60" height="50" fill="{DOSKA}" opacity=".9" {o(2)}/>')
    carm = 4 * A.w(t, 1.1)
    s += SL(Z_SRED, f'<path d="M{r1x+carm:.0f},{r1y+30:.0f} q16,30 -6,{40+carm:.0f}" fill="none" stroke="{DOSKA}" stroke-width="6" opacity=".6"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def kopeechka_chtoby_ne_possoritsya(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 75)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    okvid = _primeta_vorona(0, 0, .6, t, min(1.0, A.ease(A.seg(t, 1.6, 1.0))))
    s += SL(Z_DAL, okno_izby(1500, 160, 280, 240, t, vid=f'<g transform="translate(160,170)">{okvid}</g>', svet=False, moroz=.2))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 760, 900, 34))
    s += SL(Z_SRED, _samovar(500, 740, .8, t))
    s += SL(Z_SRED, f'<ellipse cx="800" cy="720" rx="90" ry="28" fill="{MED}" {o(3)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{700+i*22}" cy="700" r="12" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1040" cy="712" rx="60" ry="20" fill="{STEKLO}" opacity=".6" {o(2)}/>')
    s += SL(Z_SRED, hodiki(1650, 320, t, 1.0))
    s += SL(Z_SRED, figura(560, 1020, 460, t, "#5a5560", KREM, True, .0))
    ruk1, (r1x, r1y) = rukav(640, 780, 140, -40, t, "#5a5560", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, _varezhka(r1x + 10, r1y + 10, 1.3, 0, KRAS))
    s += SL(Z_SRED, _nozhnicy_bolshie(r1x + 10, r1y - 20, 70, t))
    s += SL(Z_SRED, figura(900, 1020, 460, t, "#8c6a3a", KREM, False, .3))
    hohot = abs(A.w(t, .7)) > .6
    ruk2, (r2x, r2y) = rukav(840, 780, 140, -150 - (10 if hohot else 0), t, "#8c6a3a", KREM, .3, 4)
    s += SL(Z_SRED, ruk2)
    moneta_t = A.ease(A.seg(t, 1.2, .6))
    s += SL(Z_SRED, f'<circle cx="{r2x-10*moneta_t:.0f}" cy="{r2y+10*moneta_t:.0f}" r="14" fill="url(#med)" opacity="{moneta_t:.2f}" {o(2)}/>')
    s += SL(Z_SRED, svecha(597, 853, t, 1.33, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def ognennaya_koza_s_meshkom_podarkov(t):
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += SL(Z_NEBO, teplo(960, 300, 900, 500, .5))
    s += SL(Z_DAL, izba_snaruzhi(260, 940, 460, t, True, True, 17))
    s += SL(Z_DAL, _elka(1680, 960, 480, t, 19))
    s += SL(Z_SRED, sneg_lezhit(880))
    s += SL(Z_SRED, f'<path d="M1500,900 l60,-150 l60,150 Z" fill="{SNEG}" {o(3)}/><ellipse cx="1560" cy="900" rx="40" ry="14" fill="{SNEG}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1300" y="820" width="140" height="80" rx="10" fill="{ZHELEZ}" {o(3)}/><circle cx="1370" cy="800" r="40" fill="{SVET}" opacity=".8"/>')
    kx, ky = 900, 880
    s += SL(Z_SRED, _koza_hozyayka(kx, ky, 460, t))
    mesh_sw = 6 * A.w(t, 1.1)
    mx = kx + 160 + mesh_sw
    s += SL(Z_SRED, f'<path d="M{mx:.0f},{ky-220:.0f} q60,10 50,110 q-10,70 -60,70 q-50,0 -56,-70 q-6,-100 66,-110 Z" fill="#6b3a26" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{mx+30:.0f},{ky-230:.0f} l40,-30" stroke="{ZHELEZ}" stroke-width="5"/>')
    for i, (dx, col) in enumerate([(-10, TKAN2), (20, MED), (-25, ZEL2), (10, KRAS)]):
        s += SL(Z_SRED, f'<rect x="{mx+dx:.0f}" y="{ky-240-i*6:.0f}" width="26" height="18" rx="4" fill="{col}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M{mx-30:.0f},{ky-250:.0f} l10,-20 l10,20 Z" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#1a0e08", .3))
    s += SL(Z_LETIT, sneg_letit(t, 18, 29, .5, .8))
    s += vinetka(.38)
    return s


# ═══════════════════════════ 74-81 ══════════════════════════════
def krasnyy_konvert(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a1618"/>'
    s += SL(Z_DAL, teplo(960, 460, 1100, 760, .55))
    s += SL(Z_DAL, lampa(960, 220, t, 1.2, True))
    s += SL(Z_SRED, f'<path d="M1500,900 q-80,-200 -160,-260" stroke="#2a1a16" stroke-width="16" fill="none"/>')
    s += SL(Z_SRED, f'<rect x="1500" y="640" width="200" height="130" rx="30" fill="{KRAS}" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1600" cy="700" rx="30" ry="40" fill="{ZOL}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="300" cy="760" rx="120" ry="34" fill="{KREM}" {o(3)}/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{220+i*28}" cy="750" r="12" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1150" y="700" width="60" height="90" rx="8" fill="{KAMEN}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1180,690 q20,-10 30,-30" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    s += SL(Z_SRED, par(1180, 680, t, 3, .4, 70))
    kx, ky, kw, kh = 760, 640, 400, 240
    glow = .4 + .3 * abs(A.w(t, 1.3))
    s += SL(Z_SRED, f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw}" height="{kh}" rx="14" fill="{KRAS}" opacity="{.9+.1*glow:.2f}" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{ky:.0f} L{kx+kw/2:.0f},{ky+kh*.6:.0f} L{kx+kw:.0f},{ky:.0f}" fill="none" stroke="{ZOL}" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw}" height="{kh}" rx="14" fill="none" stroke="{ZOL}" stroke-width="6"/>')
    klap = A.ease(A.seg(t, .4, 1.0))
    s += SL(Z_SRED, f'<rect x="{kx+kw*.1:.0f}" y="{ky+kh*.5+klap*20:.0f}" width="{kw*.8:.0f}" height="30" fill="{KREM}" opacity=".9" {o(2)}/>')
    oblk = _oblachko(kx + kw * .5, ky - 60 - klap * 20, .7 + .3 * klap, t, .2, "serdce")
    s += SL(Z_SRED, f'<g opacity="{klap:.2f}">{oblk}</g>')
    s += SL(Z_SRED, _napolnenie(60, 560, 1000, 160, t, 204, 20))
    s += SL(Z_PERED, ramka_pp("oba", "#0c0608", .4))
    s += vinetka(.42)
    return s


def konvert_dvumya_rukami(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a1420"/>'
    s += SL(Z_DAL, teplo(500, 400, 600, 440, .4))
    s += SL(Z_DAL, teplo(1500, 400, 600, 440, .4))
    for fx in (300, 1700):
        s += SL(Z_SRED, f'<path d="M{fx-50:.0f},700 l50,-90 l50,90 Z" fill="{KRAS}" {o(4)}/><ellipse cx="{fx:.0f}" cy="700" rx="30" ry="12" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, stol(760, 860, 400, 30))
    s += SL(Z_SRED, f'<ellipse cx="900" cy="850" rx="80" ry="22" fill="{MED}" {o(3)}/>')
    naklon = 8 * A.ease(A.seg(t, .3, .6))
    stoy1 = figura(600, 1020, 460, t, "#3a2a40", KREM, False, .0, naklon=naklon)
    s += SL(Z_SRED, stoy1)
    konv_x = 600 + (320) * A.ease(A.seg(t, .6, 1.0))
    ruk1, (r1x, r1y) = rukav(680, 820, 150, -40, t, "#3a2a40", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(620, 820, 150, -140, t, "#3a2a40", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    klanyat = A.ease(A.seg(t, 1.6, .6))
    stoy2 = figura(1200, 1040 - 4 * klanyat, 420, t, "#8c3a3a", KREM, False, .3, naklon=10 * klanyat)
    s += SL(Z_SRED, stoy2)
    ruk2, (r2x, r2y) = rukav(1130, 820, 150, -150, t, "#8c3a3a", KREM, .3, 3)
    s += SL(Z_SRED, ruk2)
    ruk2b, (r2bx, r2by) = rukav(1270, 820, 150, -40, t, "#8c3a3a", KREM, .6, 3)
    s += SL(Z_SRED, ruk2b)
    s += SL(Z_SRED, f'<rect x="{konv_x-50:.0f}" y="760" width="100" height="70" rx="6" fill="{KRAS}" {o(4)}/>')
    vtoraya = A.ease(A.seg(t, 2.4, 1.0))
    if vtoraya > .1:
        s += SL(Z_SRED, f'<g opacity="{vtoraya:.2f}"><rect x="1400" y="860" width="260" height="140" rx="30" fill="#efe3c8" {o(4)}/>'
                        f'<circle cx="1480" cy="900" r="40" fill="#e0b08a" {o(2)}/>'
                        f'<rect x="1560" y="940" width="60" height="40" rx="6" fill="{KRAS}" opacity=".9"/></g>')
    s += SL(Z_SRED, svecha(544, 816, t, 0.96, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0810", .4))
    s += vinetka(.42)
    return s


def chay_i_frukty_v_podarok(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a1420"/>'
    s += SL(Z_DAL, teplo(960, 400, 700, 500, .35))
    s += SL(Z_SRED, stol(300, 780, 1340, 32))
    s += SL(Z_SRED, f'<path d="M400,780 q0,-50 80,-50 q80,0 80,50 Z" fill="url(#derev)" {o(4)}/>')
    for i in range(4):
        jig = 4 * A.w(t, 1.3, i * .2)
        s += SL(Z_SRED, f'<circle cx="{420+i*36+jig:.0f}" cy="730" r="18" fill="{(ZOL,ZEL2)[i%2]}" {o(2)}/>')
    lenta = 6 * A.w(t, 1.4)
    s += SL(Z_SRED, f'<path d="M{420+lenta:.0f},730 q80,-20 160,0" fill="none" stroke="{KRAS}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="700" y="740" width="260" height="40" rx="8" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="730" rx="50" ry="40" fill="{CHUGUN}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="736" rx="30" ry="14" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, par(760, 690, t, 3, .4, 70))
    s += SL(Z_SRED, svecha(1020, 770, t, .3, .9))
    kx, ky = 1540, 680
    s += SL(Z_SRED, f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="210" fill="url(#derev)" {o(6)}/>')
    px, py, pw, ph_ = kx - 190, ky - 190, 380, 380
    put = kontur_proema(px, py, pw, ph_, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M1180,700 l40,-70 l40,70 Z" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1130" cy="760" rx="40" ry="16" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1060, 220, 2, 7, 90, 120))
    s += SL(Z_SRED, f'<rect x="200" y="600" width="90" height="160" rx="8" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M160,780 l-16,-140 l40,20 l16,120 Z" fill="{ZEL}" {o(3)}/>')
    blik_i = 4 * A.w(t, 2.0)
    s += SL(Z_SRED, f'<ellipse cx="{kx+blik_i:.0f}" cy="{ky-120:.0f}" rx="40" ry="14" fill="#fff" opacity=".4"/>')
    s += SL(Z_SRED, _napolnenie(1600, 560, 260, 160, t, 201, 14))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0810", .38))
    s += vinetka(.4)
    return s


def babushka_pishet_zapisku_v_konvert(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("noch", t, True, 77)
    s += SL(Z_DAL, okno_izby(1480, 160, 300, 300, t, svet=False, moroz=.3))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(420, 760, 980, 34))
    s += SL(Z_SRED, lampa(1200, 700, t, 1.0, True))
    s += SL(Z_SRED, f'<rect x="540" y="700" width="140" height="90" rx="4" fill="{POBEL}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="560" y="680" width="110" height="70" rx="4" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M700,700 v60" stroke="{ZHELEZ}" stroke-width="3"/><path d="M680,700 q20,10 40,0" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<circle cx="840" cy="730" r="30" fill="{STEKLO}" opacity=".6" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="920" y="700" width="90" height="30" rx="4" fill="{MED}" opacity=".8"/>')
    s += SL(Z_SRED, f'<rect x="1040" y="700" width="60" height="50" rx="4" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, figura(680, 1040, 480, t, "#6b2a44", KREM, True, .2))
    ruk1, (r1x, r1y) = rukav(640, 780, 140, -30, t, "#6b2a44", KREM, .2, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(720, 780, 150, -20, t, "#6b2a44", KREM, .5, 2)
    s += SL(Z_SRED, ruk2)
    pish = A.seg(t % 3.0, .2, 2.4)
    s += SL(Z_SRED, f'<path d="M{r2x:.0f},{r2y+10:.0f} h{80*pish:.0f}" stroke="#2a1d14" stroke-width="3" stroke-dasharray="6 4"/>')
    ochki_sv = 4 * A.ease(A.seg(t % 5.0, 2.0, 1.0))
    s += SL(Z_SRED, f'<rect x="{676+ochki_sv:.0f}" y="{940+ochki_sv:.0f}" width="40" height="14" rx="6" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, par(840, 700, t, 3, .4, 60))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def koza_v_sharfe_plede_i_varezhkah(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 79)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, pech(1500, 320, 380, 500, t))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _kovrik_pol(500, 900, 700, 120, TKAN, KREM, 81))
    kx, ky = 820, 900
    s += SL(Z_SRED, _koza_hozyayka(kx, ky, 420, t))
    sharf_sw = 4 * A.w(t, 1.2)
    s += SL(Z_SRED, f'<path d="M{kx-60+sharf_sw:.0f},{ky-280:.0f} q60,30 0,60 q-60,-10 0,-60 Z" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{kx+30:.0f},{ky-220:.0f} q20,60 -10,120" fill="none" stroke="{TKAN2}" stroke-width="22" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M{kx-120:.0f},{ky-60:.0f} q120,-40 240,0 l0,60 q-120,40 -240,0 Z" fill="{KAMEN}" opacity=".85" {o(3)}/>')
    for i in range(2):
        s += SL(Z_SRED, _varezhka(kx - 40 + i * 110, ky - 320 + 8 * A.w(t, 1.6, i * .3), 1.0, 20 - i * 40, KRAS))
    s += SL(Z_SRED, kot(kx + 200, ky + 20, t, .9, "#3b3430", False))
    s += SL(Z_SRED, f'<path d="M{kx+220:.0f},{ky-20:.0f} q20,{-20*A.w(t,2.0):.0f} 10,-40" fill="none" stroke="{TKAN}" stroke-width="6"/>')
    uzel = A.ease(A.seg(t, .4, 1.4))
    s += SL(Z_SRED, figura(kx - 220, 1040, 460, t, "#5a6a4a", KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(kx - 160, 820, 140, -20 + uzel * 30, t, "#5a6a4a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(kx - 100, 820, 140, -60 - uzel * 30, t, "#5a6a4a", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<rect x="300" y="860" width="100" height="90" rx="30" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M340,860 v-30" stroke="{DOSKA}" stroke-width="6"/><path d="M360,860 v-30" stroke="{DOSKA}" stroke-width="6"/>')
    s += SL(Z_SRED, svecha(703, 807, t, 0.07, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def suvenir_v_shkafu(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 83)
    s += SL(Z_DAL, _oboi_fon("#4a3a4a", "#3a2e3a"))
    s += SL(Z_SRED, polovicy(840))
    sx, sy, sw, sh = 660, 380, 600, 500
    s += SL(Z_SRED, f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw}" height="{sh}" rx="10" fill="url(#derev)" {o(7)}/>')
    for row in range(2):
        gy = sy + 40 + row * 220
        s += SL(Z_SRED, f'<rect x="{sx+30:.0f}" y="{gy:.0f}" width="{sw-60}" height="180" rx="6" fill="url(#stekl)" opacity=".4" {o(3)}/>')
    suveniry = [(0, "slon", KREM), (1, "palma", ZEL), (2, "shar", STEKLO), (3, "figurka", MED), (4, "rakushka", "#e8d8c8")]
    for idx, kind, col in suveniry:
        gx = sx + 70 + idx * (sw - 140) / 4
        gy = sy + 180
        if kind == "slon":
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="22" ry="18" fill="{col}" {o(2)}/>')
        elif kind == "palma":
            s += SL(Z_SRED, f'<path d="M{gx:.0f},{gy+16:.0f} v-30 M{gx-14:.0f},{gy-14:.0f} l14,0 l10,-10" stroke="{col}" stroke-width="4" fill="none"/>')
        elif kind == "shar":
            s += SL(Z_SRED, f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="20" fill="{col}" opacity=".7" {o(2)}/>')
        elif kind == "figurka":
            s += SL(Z_SRED, f'<rect x="{gx-10:.0f}" y="{gy-20:.0f}" width="20" height="34" rx="6" fill="{col}" {o(2)}/>')
        else:
            s += SL(Z_SRED, f'<path d="M{gx-16:.0f},{gy+10:.0f} q16,-26 32,0 Z" fill="{col}" {o(2)}/>')
    nova = A.ease(A.seg(t, .4, 1.0))
    nx, ny = sx + sw + 60 - nova * 170, sy + 180
    s += SL(Z_SRED, f'<rect x="{nx-14:.0f}" y="{ny-20:.0f}" width="28" height="34" rx="6" fill="{ZOL}" {o(2)}/>')
    pautinka = A.ease(A.seg(t, 1.4, 1.2))
    if pautinka > .1:
        s += SL(Z_SRED, f'<path d="M{nx:.0f},{ny-20:.0f} q10,{-10*pautinka:.0f} 20,0 q-6,{10*pautinka:.0f} -20,0" fill="none" stroke="#cfd6de" stroke-width="2" opacity="{pautinka:.2f}"/>')
    zakr = A.ease(A.seg(t, 2.0, .6))
    s += SL(Z_SRED, f'<rect x="{sx+sw-20*zakr:.0f}" y="{sy:.0f}" width="20" height="{sh}" fill="url(#derev)" opacity="{zakr:.2f}" {o(2)}/>')
    ruk1, (r1x, r1y) = rukav(sx + sw + 140, 900, 160, -140, t, "#3a3a4a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    povorot = A.ease(A.seg(t, 2.4, .8))
    s += SL(Z_SRED, f'<g transform="rotate({povorot*20:.1f} {sx+150:.0f} {sy+100:.0f})">' + _koza_hozyayka(sx + 150, sy + 320, 180, t) + '</g>')
    s += SL(Z_SRED, svecha(1286, 854, t, 0.14, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e14", .38))
    s += vinetka(.4)
    return s


# ═══════════════════════════ 82-91 ══════════════════════════════
def vechera_nad_vyazanem(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    luna_x = 1500 + 300 * math.sin(t * .6)
    oknovid = nebo("noch", t, True, 85) + f'<circle cx="{luna_x-1300:.0f}" cy="200" r="34" fill="{KREM}" opacity=".9"/>'
    s += SL(Z_DAL, okno_izby(1300, 160, 360, 340, t, vid=oknovid, moroz=.1, svet=False))
    s += SL(Z_DAL, _oboi_fon("#4a3a3a", "#3a2e2e"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, f'<rect x="960" y="700" width="260" height="280" rx="20" fill="#6b4428" {o(6)}/>')
    s += SL(Z_SRED, lampa(1180, 620, t, 1.1, True))
    mx, my, mw, mh = 1080, 500, 460, 400
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{mw*.52:.0f}" ry="{mh*.52:.0f}" fill="url(#zol)" {o(5)}/>')
    put = kontur_proema(mx - mw * .42, my - mh * .42, mw * .84, mh * .84, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(mx - mw * .42, my - mh * .42, mw * .84, mh * .84, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(4)}/>')
    stopka_h = min(140, 10 + t * 12)
    s += SL(Z_SRED, f'<rect x="1340" y="{860-stopka_h:.0f}" width="140" height="{stopka_h:.0f}" rx="6" fill="{TKAN}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M100,760 q80,-40 160,0 l0,60 q-80,40 -160,0 Z" fill="#6b4428" {o(4)}/>')
    for i in range(3):
        s += SL(Z_SRED, _banka(140 + i * 50, 790, .6, (TKAN, TKAN2, MED)[i]))
    s += SL(Z_SRED, kot(420, 940, t, .9, "#3b3430", True))
    s += SL(Z_SRED, f'<circle cx="640" cy="760" r="60" fill="url(#derev)" {o(4)}/><circle cx="640" cy="760" r="46" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, figura(1060, 1040, 440, t, "#6b2a38", KREM, False, .0))
    sp1 = 6 * A.w(t, 4.0)
    sp2 = 6 * A.w(t, 4.0, .5)
    ruk1, (r1x, r1y) = rukav(1000, 840, 130, -20 + sp1, t, "#6b2a38", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(1120, 840, 130, -160 + sp2, t, "#6b2a38", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<circle cx="1060" cy="900" r="40" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def vyazanye_noski_idut_mimo_primety(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 87)
    s += SL(Z_DAL, _oboi_fon("#5a4a5a", "#4a3a4a"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _kovrik_pol(500, 880, 900, 140, TKAN, KREM, 89))
    idut = (t * 120) % 760
    for i, col in enumerate((KRAS, TKAN2)):
        nx = 560 + idut - i * 60
        tilt = 10 * math.sin(t * 6 + i)
        s += SL(Z_SRED, f'<g transform="rotate({tilt:.1f} {nx:.0f} 900)">'
                        f'<path d="M{nx-30:.0f},900 q0,-50 30,-50 q30,0 30,50 q-10,20 -30,20 q-20,0 -30,-20 Z"'
                        f' fill="{col}" {o(3)}/></g>')
    s += SL(Z_SRED, _varezhka(560 + idut - 140, 880, 1.0, 10 * math.sin(t * 5)))
    s += SL(Z_SRED, f'<path d="M{560+idut-220:.0f},860 q40,-10 80,0" fill="none" stroke="{TKAN2}" stroke-width="18"/>')
    px = 1500
    s += SL(Z_SRED, f'<path d="M{px:.0f},900 v-260" stroke="{ZHELEZ}" stroke-width="6"/>')
    zhezl = -20 * A.ease(A.seg(t % 3.0, .6, .5))
    s += SL(Z_SRED, f'<g transform="rotate({zhezl:.1f} {px:.0f} 760)">'
                    f'<line x1="{px:.0f}" y1="760" x2="{px+100:.0f}" y2="700" stroke="{ZHELEZ}" stroke-width="5"/></g>')
    s += SL(Z_SRED, _primeta_vorona(px, 660, 1.0, t, 0))
    s += SL(Z_SRED, _veshalka_seni(1600, 300, 300, t, 11))
    s += SL(Z_SRED, kot(1300, 900, t, .8, "#3b3430", False))
    s += SL(Z_SRED, f'<ellipse cx="1340" cy="700" rx="60" ry="90" fill="{STEKLO}" opacity=".5" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="400" y="820" width="100" height="40" rx="8" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M300,780 q10,-60 40,-70" fill="none" stroke="{ZOL}" stroke-width="6"/>')
    s += SL(Z_SRED, svecha(1498, 762, t, 1.62, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .38))
    s += vinetka(.4)
    return s


def stopka_noskov_s_birkami(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 91)
    s += SL(Z_DAL, _oboi_fon("#4a3a4a", "#3a2e3a"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, f'<rect x="260" y="700" width="700" height="200" rx="30" fill="{TKAN2}" {o(5)}/>')
    tvx, tvy = 1500, 540
    s += SL(Z_SRED, f'<rect x="{tvx-130:.0f}" y="{tvy-80:.0f}" width="260" height="190" rx="10" fill="{ZHELEZ}" {o(5)}/>')
    mig = ((t * 1.4) % 1.0) > .5
    s += SL(Z_SRED, f'<rect x="{tvx-100:.0f}" y="{tvy-60:.0f}" width="200" height="150" fill="{SVET if mig else "#4a5a68"}" opacity="{.7 if mig else .4}"/>')
    s += SL(Z_SRED, f'<rect x="{tvx-140:.0f}" y="{tvy+110:.0f}" width="280" height="30" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="900" y="700" width="260" height="40" rx="8" fill="url(#derev)" {o(5)}/>')
    stopka = min(170, 10 + t * 22)
    cols = (KRAS, TKAN2, ZEL2, TKAN)
    for i in range(4):
        hh = stopka / 4
        s += SL(Z_SRED, f'<rect x="920" y="{700-hh*(i+1):.0f}" width="220" height="{hh-4:.0f}" rx="8" fill="{cols[i]}" {o(2)}/>')
        if stopka > hh * (i + .6) * 4 / 4:
            s += SL(Z_SRED, f'<rect x="1000" y="{700-hh*(i+1)+6:.0f}" width="50" height="20" fill="{KREM}" {o(1)}/>')
    s += SL(Z_SRED, f'<circle cx="430" cy="690" r="60" fill="{TKAN}" {o(3)}/>')
    s += SL(Z_SRED, kot(300, 900, t, .9, "#3b3430", False))
    s += SL(Z_SRED, figura(700, 1040, 460, t, "#5a6a4a", KREM, True, .0))
    sp1 = 5 * A.w(t, 4.2)
    sp2 = 5 * A.w(t, 4.2, .5)
    ruk1, (r1x, r1y) = rukav(640, 820, 140, -30 + sp1, t, "#5a6a4a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(760, 820, 140, -150 + sp2, t, "#5a6a4a", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    ochki_dr = 3 * A.w(t, 1.0)
    s += SL(Z_SRED, f'<rect x="{676+ochki_dr:.0f}" y="950" width="40" height="14" rx="6" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, svecha(1233, 817, t, 1.77, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def banka_v_sitcevoy_shapochke(t):
    s = f'<rect width="{W}" height="{H}" fill="{KAMEN2}"/>'
    s += SL(Z_DAL, kladka(0, 0, W, 900))
    s += SL(Z_SRED, polovicy(900, "url(#beton)"))
    sx, sy, sw = 1060, 320, 820
    s += SL(Z_SRED, f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw}" height="80" fill="url(#derev)" {o(4)}/>')
    px, py, pw, ph_ = sx + 30, sy + 90, 760, 300
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{sx:.0f}" y="{py+ph_+10:.0f}" width="{sw}" height="80" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, stol(260, 760, 800, 34))
    s += SL(Z_SRED, _banka(460, 740, 1.5, RUSH))
    s += SL(Z_SRED, f'<ellipse cx="700" cy="720" rx="60" ry="40" fill="url(#med)" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{660+i*16:.0f},720 q8,-20 0,-40" fill="none" stroke="#6b4a2e" stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M880,730 q10,-60 30,-70" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<circle cx="340" cy="700" r="26" fill="{ZHELEZ}" {o(2)}/>')
    birka_i = int((t * .6) % 3)
    labels = (("Варенье",), ("Мёд",), ("Грибы",))[birka_i]
    s += SL(Z_SRED, f'<rect x="420" y="640" width="80" height="30" rx="4" fill="{KREM}" opacity="{.6+.4*abs(A.w(t,1.5)):.2f}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1000, 760, t, .3, .9))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0c", .4))
    s += vinetka(.4)
    return s


def banka_mezhdu_chaynikom_i_hlebnicey(t):
    s = f'<rect width="{W}" height="{H}" fill="#3a3e44"/>'
    s += SL(Z_DAL, _oboi_fon("#4a5258", "#3a4248"))
    s += SL(Z_DAL, f'<rect x="300" y="160" width="340" height="420" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_DAL, f'<rect x="320" y="180" width="300" height="160" rx="6" fill="url(#stekl)" opacity=".4" {o(3)}/>')
    s += SL(Z_DAL, f'<rect x="1260" y="200" width="300" height="260" rx="8" fill="#2a2e34" {o(5)}/>')
    s += SL(Z_DAL, _chasy_sten(1600, 300, 1.0, t))
    s += SL(Z_SRED, f'<rect x="200" y="700" width="1520" height="300" fill="{BETON}" {o(5)}/>')
    s += SL(Z_SRED, _samovar(460, 740, .7, t, True))
    s += SL(Z_SRED, f'<rect x="1300" y="700" width="220" height="110" rx="10" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1320" y="660" width="180" height="50" rx="6" fill="{KREM}" opacity=".8" {o(3)}/>')
    kladovka = max(0, 1 - A.ease(A.seg(t % 4.0, .3, 1.6)))
    if kladovka > .02:
        s += SL(Z_SRED, f'<g opacity="{kladovka*.5:.2f}">' + brevna(700, 300, 500, 440, 60) + '</g>')
    s += SL(Z_SRED, _banka(900, 760, 1.5, RUSH))
    bant_sh = 4 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<path d="M{900+bant_sh:.0f},700 q-20,10 0,20" fill="none" stroke="{KRAS}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="1080" y="750" width="40" height="20" fill="url(#zhel)" {o(2)}/>')
    s += SL(Z_SRED, svecha(160, 780, t, 0.0, .8))
    s += SL(Z_SRED, _napolnenie(60, 760, 220, 180, t, 208, 3))
    s += SL(Z_SRED, _napolnenie(700, 760, 540, 160, t, 211, 7))
    s += SL(Z_SRED, kot(1700, 920, t, .85, "#3b3430", False))
    s += SL(Z_PERED, ramka_pp("oba", "#1a1e22", .34))
    s += vinetka(.36)
    return s


def koshelek_s_monetoy_i_vaza_s_gostin(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 93)
    s += SL(Z_DAL, _elka(1500, 960, 520, t, 23))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, stol(360, 760, 1000, 34))
    s += SL(Z_SRED, _koshelek(600, 740, 1.3, True, 1))
    blesk = .5 + .5 * abs(A.w(t, 1.6))
    s += SL(Z_SRED, f'<circle cx="590" cy="708" r="10" fill="{SVET}" opacity="{blesk:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M900,700 v-80 q0,-20 40,-20 q40,0 40,20 v80 Z" fill="{STEKLO}" opacity=".5" {o(4)}/>')
    podn = 4 * A.w(t, 1.2)
    s += SL(Z_SRED, f'<path d="M{900+podn:.0f},690 q40,-6 80,0" fill="none" stroke="{KREM}" stroke-width="4" opacity=".7"/>')
    if abs(math.sin(t * .8)) > .5:
        s += SL(Z_SRED, _galochka(600, 650, .7, t, 0))
    if abs(math.sin(t * .8 + 1)) > .5:
        s += SL(Z_SRED, _galochka(940, 620, .7, t, .3))
    s += SL(Z_SRED, f'<path d="M1100,740 q10,-50 40,-60" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_SRED, svecha(1250, 740, t, .4, .9))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.4)
    return s


def kniga_s_nadpisyu(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 95)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 760, 1200, 34))
    s += SL(Z_SRED, lampa(600, 680, t, 1.1, True))
    s += SL(Z_SRED, f'<path d="M900,780 L900,700 Q900,680 940,680 L1180,680 Q1220,680 1220,700 L1220,780 Z" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<line x1="1060" y1="680" x2="1060" y2="780" stroke="{POL}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<rect x="1280" y="700" width="60" height="30" rx="6" fill="#1a1a2a" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1380,710 l30,-16 l6,6 l-26,18 Z" fill="{DOSKA}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1440" y="720" width="40" height="14" rx="6" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<ellipse cx="1550" cy="730" rx="40" ry="18" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, figura(900, 1060, 480, t, "#5a4a3a", KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(840, 800, 140, -40, t, "#5a4a3a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(1030, 800, 150, -140, t, "#5a4a3a", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    pero = A.seg(t % 3.0, .3, 2.2)
    s += SL(Z_SRED, f'<path d="M{r2x:.0f},{r2y+6:.0f} h{90*pero:.0f}" stroke="#1a1a2a" stroke-width="3" stroke-dasharray="4 5"/>')
    s += SL(Z_SRED, f'<path d="M{950+90*pero:.0f},{r2y:.0f} l10,0 l-4,-6" fill="none" stroke="#1a1a2a" stroke-width="2"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def kniga_na_polke_cherez_gody(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 97)
    s += SL(Z_DAL, _oboi_fon("#4a3a4a", "#3a2e3a"))
    s += SL(Z_SRED, polovicy(840))
    px, py = 760, 440
    s += SL(Z_SRED, f'<rect x="{px:.0f}" y="{py:.0f}" width="500" height="340" rx="8" fill="url(#derev)" {o(6)}/>')
    for i in range(10):
        bx = px + 30 + i * 44
        s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{py+40:.0f}" width="34" height="240" rx="3" fill="{(TKAN,TKAN2,MED,ZEL2)[i%4]}" {o(2)}/>')
    snyali = A.ease(A.seg(t, .3, .8))
    s += SL(Z_SRED, f'<rect x="{px+200+snyali*60:.0f}" y="{py+40-snyali*140:.0f}" width="34" height="240" rx="3" fill="{MED}" {o(3)}/>')
    oblk = A.ease(A.seg(t, 1.2, 1.4))
    if oblk > .05:
        s += SL(Z_SRED, f'<g opacity="{oblk:.2f}"><ellipse cx="{px+260:.0f}" cy="{py-30-oblk*40:.0f}" rx="70" ry="46" fill="#ffffff" opacity=".9" {o(3)}/>'
                        f'<circle cx="{px+230:.0f}" cy="{py-10-oblk*40:.0f}" r="22" fill="#e0b08a" {o(2)}/>'
                        f'<rect x="{px+200:.0f}" y="{py+6-oblk*40:.0f}" width="60" height="30" fill="#2a3a4a" {o(2)}/></g>')
    s += SL(Z_SRED, kot(1400, 920, t, .9, "#3b3430", False))
    s += SL(Z_SRED, f'<rect x="200" y="760" width="220" height="200" rx="16" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, figura(px + 150, 1040, 460, t, "#3a3a4a", KREM, False, .3))
    ruk1, (r1x, r1y) = rukav(px + 210, 820, 130, -50, t, "#3a3a4a", KREM, .3, 2)
    s += SL(Z_SRED, ruk1)
    prizh = A.ease(A.seg(t, 2.6, 1.0))
    s += SL(Z_SRED, f'<rect x="{px+150-20*prizh:.0f}" y="{960-prizh*60:.0f}" width="40" height="60" rx="4" fill="{MED}" opacity="{.5+.5*prizh:.2f}" {o(2)}/>')
    s += SL(Z_SRED, svecha(491, 779, t, 0.59, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def vnuki_s_konvertami(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 99)
    s += SL(Z_DAL, _elka(1500, 960, 520, t, 29))
    s += SL(Z_SRED, _kovrik_pol(500, 880, 900, 160, TKAN, KREM, 31))
    s += SL(Z_SRED, hodiki(1700, 300, t, .9))
    s += SL(Z_SRED, f'<path d="M1300,900 l60,-30 l-20,40 Z" fill="{ZEL2}" {o(2)}/>')
    s += SL(Z_SRED, figura(700, 1000, 300, t, "#3a5a6b", KREM, False, .0))
    svet = A.seg(t % 3.0, .3, 2.0)
    ruk1, (r1x, r1y) = rukav(750, 810, 90, -40, t, "#3a5a6b", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(650, 810, 90, -150, t, "#3a5a6b", KREM, .3, 2)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<g transform="rotate({8*math.sin(t*1.4):.1f} {(r1x+r1bx)/2:.0f} {(r1y+r1by)/2:.0f})">'
                    f'<rect x="{(r1x+r1bx)/2-40:.0f}" y="{(r1y+r1by)/2-28:.0f}" width="80" height="56" rx="4" fill="{KRAS}" {o(3)}/></g>')
    s += SL(Z_SRED, figura(1040, 1020, 280, t, "#8c3a4a", KREM, False, .3))
    ubyvaet = int(6 - (t * 1.5) % 6)
    ruk2, (r2x, r2y) = rukav(1100, 920, 90, -30, t, "#8c3a4a", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<path d="M{r2x-10:.0f},{r2y:.0f} l20,0 l-10,16 Z" fill="{MED}" {o(2)}/>')
    for i in range(max(0, 8 - ubyvaet)):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<circle cx="{980+rnd.random()*80:.0f}" cy="{1080+rnd.random()*30:.0f}" r="10" fill="{(ZOL,KRAS)[i%2]}" opacity=".6" {o(1)}/>')
    s += SL(Z_SRED, f'<path d="M1200,860 l-60,-30 l60,-10 Z" fill="{DOSKA}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1445, 845, t, 1.25, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .38))
    s += vinetka(.4)
    return s


def korzinka_dlya_vzroslyh_detey(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 101)
    s += SL(Z_DAL, _oboi_fon())
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, stol(460, 780, 1000, 34))
    kx = 900
    perehod = A.ease(A.seg(t, .3, 1.4))
    kkx = 700 + perehod * 260
    s += SL(Z_SRED, f'<path d="M{kkx-90:.0f},780 q90,-50 180,0 Z" fill="none" stroke="{MED}" stroke-width="8"/>'
                    f'<path d="M{kkx-100:.0f},780 q100,40 200,0 l0,40 q-100,40 -200,0 Z" fill="{MED}" {o(4)}/>')
    s += SL(Z_SRED, _banka(kkx - 40, 760, .6, RUSH))
    s += SL(Z_SRED, f'<rect x="{kkx+10:.0f}" y="750" width="50" height="30" rx="8" fill="{TKAN2}" {o(2)}/>')
    s += SL(Z_SRED, f'<circle cx="{kkx+60:.0f}" cy="770" r="14" fill="{ZOL}" {o(1)}/><circle cx="{kkx+80:.0f}" cy="770" r="14" fill="{ZOL}" {o(1)}/>')
    s += SL(Z_SRED, f'<path d="M1200,750 q10,-50 40,-60" fill="none" stroke="{KRAS}" stroke-width="5"/>')
    s += SL(Z_SRED, svecha(1350, 780, t, .3, .9))
    stoy1 = figura(600, 1060, 470, t, "#5a3a4a", KREM, False, .0)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(670, 820, 150, -30, t, "#5a3a4a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(540, 820, 150, -150, t, "#5a3a4a", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    stoy2 = figura(1260, 1060, 460, t, "#8c3a6a", KREM, False, .3, True)
    s += SL(Z_SRED, stoy2)
    poceluy = A.ease(A.seg(t, 2.0, .6))
    s += SL(Z_SRED, f'<g transform="translate({-20*poceluy:.0f},0)">'
                    f'<ellipse cx="640" cy="1000" rx="20" ry="14" fill="#e0b08a" {o(2)}/></g>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .38))
    s += vinetka(.4)
    return s


# ═══════════════════════════ 92-99 ══════════════════════════════
def chay_s_sosedkoy(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 103)
    s += SL(Z_DAL, _oboi_fon("#5a4a4a", "#4a3a3a"))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(420, 760, 1080, 34))
    s += SL(Z_SRED, _banka(560, 720, 1.0, RUSH))
    s += SL(Z_SRED, f'<path d="M520,700 q20,-20 20,-40" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<ellipse cx="720" cy="740" rx="40" ry="16" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="880" cy="740" rx="40" ry="16" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, _samovar(1100, 740, .55, t))
    s += SL(Z_SRED, f'<ellipse cx="1300" cy="750" rx="60" ry="22" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1480" cy="730" r="16" fill="{CHUGUN}" {o(2)}/>')
    s += SL(Z_SRED, figura(680, 1040, 460, t, "#6b4a3a", KREM, True, .0))
    nal_t = A.seg(t % 3.0, .2, 2.4)
    ruk1, (r1x, r1y) = rukav(760, 800, 140, -50, t, "#6b4a3a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y:.0f} q10,{30*nal_t:.0f} 0,{60*nal_t:.0f}" fill="none" stroke="{STEKLO}" stroke-width="3" opacity="{nal_t:.2f}"/>')
    ruk1b, (r1bx, r1by) = rukav(600, 800, 140, -150, t, "#6b4a3a", KREM, .3, 2)
    s += SL(Z_SRED, ruk1b)
    stoy2 = figura(1140, 1040, 460, t, "#3a5a6b", KREM, False, .4)
    s += SL(Z_SRED, stoy2)
    ruk2, (r2x, r2y) = rukav(1060, 800, 140, -30, t, "#3a5a6b", KREM, .4, 2)
    s += SL(Z_SRED, ruk2)
    zhmur = abs(A.w(t, 1.1)) > .7
    s += SL(Z_SRED, f'<ellipse cx="1050" cy="990" rx="14" ry="{3 if zhmur else 8}" fill="{K}"/>')
    s += SL(Z_SRED, par(560, 700, t, 3, .4, 60))
    s += SL(Z_SRED, par(1100, 660, t, 3, .4, 60, .5))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def sharf_dlya_muzha(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 105)
    s += SL(Z_DAL, okno_izby(1480, 160, 280, 280, t, svet=False, moroz=.6))
    s += SL(Z_DAL, _oboi_fon("#3a3a4a", "#2e2e3e"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _veshalka_seni(1200, 260, 400, t, 15))
    s += SL(Z_SRED, f'<path d="M160,900 l0,-260 l20,-10 l0,270 Z" fill="{DOSKA}" {o(3)}/><path d="M160,640 l120,30" stroke="{DOSKA}" stroke-width="10"/>')
    s += SL(Z_SRED, f'<path d="M320,900 l-30,-130 l60,0 Z" fill="#8c3a3a" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="760" width="90" height="60" rx="6" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, _kovrik_pol(700, 900, 500, 110, TKAN, KREM, 37))
    stoy1 = figura(900, 1040, 480, t, "#6b4a6b", KREM, False, .0)
    s += SL(Z_SRED, stoy1)
    stoy2 = figura(900, 1060, 500, t, "#2a3a4a", "#cfd6de", True, .3)
    s += SL(Z_SRED, stoy2)
    obmot = A.ease(A.seg(t % 3.0, .3, 2.0)) % 1.0
    wrap = min(obmot * 3, 3)
    for i in range(3):
        if wrap > i:
            rot = -30 + i * 35
            s += SL(Z_SRED, f'<g transform="rotate({rot:.1f} 900 840)"><rect x="840" y="800" width="120" height="40" rx="10" fill="{TKAN}" {o(2)}/></g>')
    s += SL(Z_SRED, f'<rect x="870" y="860" width="60" height="140" rx="20" fill="{TKAN}" {o(2)}/>')
    us_sh = 2 * A.w(t, 1.2)
    s += SL(Z_SRED, f'<path d="M{880+us_sh:.0f},880 q-20,4 -30,0 M{920-us_sh:.0f},880 q20,4 30,0" stroke="#2a1d14" stroke-width="4" fill="none"/>')
    s += SL(Z_SRED, f'<circle cx="300" cy="700" r="20" fill="none" stroke="{STEKLO}" stroke-width="3" opacity=".6"/>')
    s += SL(Z_SRED, svecha(1074, 826, t, 0.66, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e14", .36))
    s += vinetka(.4)
    return s


def sad_i_devyatyy_etazh(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W//2}" height="{H}" fill="{DEN}"/>')
    s += SL(Z_SRED, f'<rect x="{W//2}" y="0" width="{W//2}" height="{H}" fill="{SUMER}"/>')
    s += SL(Z_DAL, izba_snaruzhi(260, 880, 400, t, False, True, 7))
    s += SL(Z_SRED, sneg_lezhit(840))
    s += SL(Z_SRED, f'<rect x="600" y="640" width="200" height="200" rx="10" fill="{STEKLO}" opacity=".3" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M560,900 l-30,-200 l200,-20 l0,220 Z" fill="{ZEL}" opacity=".5" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="700" cy="920" rx="70" ry="24" fill="#6b4428" {o(3)}/>')
    stoy1 = figura(400, 1040, 480, t, "#3a4a3a", KREM, True, .0)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(480, 800, 140, -70, t, "#3a4a3a", KREM, .0, 4)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(400, 800, 140, -110, t, "#3a4a3a", KREM, .3, 4)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<rect x="{(r1x+r1bx)/2-60:.0f}" y="{(r1y+r1by)/2-30:.0f}" width="120" height="70" rx="8" fill="{DOSKA}" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{(r1x+r1bx)/2-40+i*26:.0f}" cy="{(r1y+r1by)/2-10:.0f}" r="14" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_DAL, panelka(W - 420, 900, 400, t, 6, True, 11))
    s += SL(Z_SRED, okno_izby(W - 360, 680, 280, 260, t, svet=True, moroz=0, krest=True))
    s += SL(Z_SRED, teplo(W - 220, 800, 260, 200, .4))
    ovx, ovy, ovw, ovh = W - 900, 760, 820, 340
    s += SL(Z_SRED, f'<rect x="{ovx:.0f}" y="{ovy:.0f}" width="{ovw}" height="{ovh}" rx="10" fill="{PECH}" {o(5)}/>')
    px, py, pw, ph_ = ovx + 30, ovy + 30, 760, 300
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(7)}/>')
    otkr = A.ease(A.seg(t, .4, .8))
    stoy2 = figura(W - 540, 1060, 480, t, "#8c3a4a", KREM, False, .3, True)
    s += SL(Z_SRED, stoy2)
    ruk2, (r2x, r2y) = rukav(ovx + ovw - 60, ovy + ovh - 60, 150, -140, t, "#8c3a4a", KREM, .3, 3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<rect x="{r2x-30:.0f}" y="{r2y-20:.0f}" width="60" height="40" rx="6" fill="{TKAN}" {o(2)}/>')
    s += SL(Z_SRED, par(ovx + ovw - 40, ovy + ovh - 40, t, 3, .4, 60) if otkr > .5 else "")
    s += SL(Z_PERED, f'<rect x="{W//2-4}" y="0" width="8" height="{H}" fill="{K}"/>')
    s += vinetka(.4)
    return s


def vecher_protiv_pensii(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 107)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(560, 760, 800, 34))
    nak = 22
    s += SL(Z_SRED, _vesy(960, 760, 1.4, t, nak, 9))
    s += SL(Z_SRED, f'<g transform="translate({960-150*1.4-50:.0f},{760-220*1.4-60:.0f})">'
                    f'<rect width="100" height="70" rx="6" fill="{TKAN2}" {o(3)}/>'
                    f'<rect x="10" y="50" width="30" height="20" fill="{KREM}" {o(2)}/></g>')
    s += SL(Z_SRED, f'<path d="M{960-150*1.4-20:.0f},{760-220*1.4+80:.0f} q-10,-90 60,-100" fill="none" stroke="{KREM}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<g transform="translate({960+150*1.4-50:.0f},{760-220*1.4+30:.0f})">'
                    + _varezhka(50, 40, 1.1, 0) + f'<path d="M80,20 l0,-50" stroke="{SVET}" stroke-width="6" opacity=".7"/></g>')
    s += SL(Z_SRED, figura(900, 1060, 480, t, "#6b4a3a", KREM, True, .0))
    s += SL(Z_SRED, f'<circle cx="840" cy="990" r="18" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<ellipse cx="700" cy="720" rx="40" ry="14" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, f'<circle cx="1200" cy="700" r="24" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, hodiki(1500, 320, t, .9))
    s += SL(Z_SRED, svecha(657, 783, t, 0.87, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def kartochka_drugogo_rolika(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a0e14"/>'
    s += SL(Z_DAL, teplo(960, 400, 800, 500, .4))
    for i in range(6):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<path d="M{200+rnd.random()*1500:.0f},{200+rnd.random()*700:.0f} l-10,-60 l20,0 Z" fill="{ZEL}" opacity=".5" {o(2)}/>')
    otskok = A.over(A.seg(t, .3, 1.0))
    cx, cy, cw, ch = 960, 580, 500, 320
    s += SL(Z_SRED, f'<g transform="translate(0,{(1-otskok)*300:.0f})"><rect x="{cx-cw/2:.0f}" y="{cy-ch/2:.0f}" width="{cw}" height="{ch}" rx="16" fill="{KREM}" {o(6)}/>'
                    f'<path d="M{cx-120:.0f},{cy+60:.0f} l40,-110 l80,0 l40,110 Z" fill="{KRAS}" {o(3)}/>'
                    f'<circle cx="{cx+120:.0f}" cy="{cy:.0f}" r="70" fill="url(#zol)" {o(3)}/>'
                    f'<line x1="{cx+120:.0f}" y1="{cy:.0f}" x2="{cx+120:.0f}" y2="{cy-40:.0f}" stroke="{K}" stroke-width="4"/>'
                    f'<line x1="{cx+120:.0f}" y1="{cy:.0f}" x2="{cx+150:.0f}" y2="{cy:.0f}" stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, _koza_hozyayka(400, 920, 340, t))
    s += SL(Z_SRED, f'<path d="M580,860 q30,-10 60,0" fill="none" stroke="{SVET}" stroke-width="4" opacity=".6"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<circle cx="{1500+i*60}" cy="{400+60*math.sin(t+i)}" r="20" fill="{(KRAS,ZOL,TKAN2)[i]}" opacity=".8" {o(2)}/>')
    s += SL(Z_SRED, svecha(1600, 800, t, .3, 1.0))
    s += SL(Z_SRED, _napolnenie(120, 700, 420, 160, t, 202, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#0c0608", .42))
    s += vinetka(.44)
    return s


def shkolnyy_zal_s_elkoy(t):
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += SL(Z_NEBO, teplo(960, 300, 900, 500, .4))
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="700" fill="{KAMEN2}"/>')
    for i in range(6):
        s += SL(Z_DAL, f'<rect x="{80+i*300}" y="200" width="160" height="320" rx="80" fill="{KAMEN}" opacity=".4" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M0,700 L1920,700 L1920,760 L0,760 Z" fill="{DOSKA}" {o(4)}/>')
    s += SL(Z_SRED, _elka(1500, 940, 560, t, 41))
    for i in range(10):
        s += SL(Z_SRED, f'<path d="M{1360+i*30:.0f},700 l-6,-40 l12,0 Z" fill="{KRAS}" opacity=".7"/>')
    s += SL(Z_SRED, f'<rect x="60" y="480" width="500" height="220" rx="10" fill="#3a2e2e" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="80" y="500" width="460" height="180" fill="#1a1414" opacity=".8"/>')
    s += SL(Z_SRED, f'<rect x="760" y="520" width="140" height="180" rx="8" fill="#2a1a10" {o(4)}/><rect x="770" y="530" width="120" height="60" fill="{KREM}" {o(2)}/>')
    for row in range(2):
        for col in range(6):
            s += SL(Z_SRED, f'<ellipse cx="{300+col*220}" cy="{820+row*110}" rx="40" ry="24" fill="{SUMER}" opacity=".7" {o(2)}/>')
    stoy = figura(900, 940, 300, t, KRAS, KREM, False, .0)
    s += SL(Z_SRED, stoy)
    s += SL(Z_SRED, f'<path d="M870,700 q30,-30 60,0" fill="none" stroke="{KREM}" stroke-width="10"/>')
    ushi = 8 * A.w(t, 1.4)
    s += SL(Z_SRED, f'<path d="M870,{700+ushi:.0f} l-10,-30 M930,{700+ushi:.0f} l10,-30" stroke="{KREM}" stroke-width="6" fill="none"/>')
    chitaet = A.seg(t % 2.0, 0, 1.6)
    s += SL(Z_SRED, f'<ellipse cx="900" cy="{880+6*chitaet:.0f}" rx="12" ry="{6+4*chitaet:.0f}" fill="#2a1d14"/>')
    ded = figura(1100, 980, 400, t, KRAS, "#efe3c8", False, .3, True, boroda=True)
    s += SL(Z_SRED, ded)
    kivok = 4 * A.w(t, 1.0)
    s += SL(Z_SRED, f'<path d="M1030,{900+kivok:.0f} v120" stroke="url(#derev)" stroke-width="10"/>')
    s += SL(Z_SRED, svecha(1127, 863, t, 1.03, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#1a0e08", .36))
    s += vinetka(.38)
    return s


# ═══════════════════════════ 99-106 ══════════════════════════════
def paket_s_detskogo_prazdnika(t):
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += SL(Z_DAL, teplo(960, 400, 800, 500, .36))
    s += SL(Z_DAL, _elka(1600, 940, 480, t, 43))
    s += SL(Z_SRED, f'<path d="M1300,900 q80,-60 180,0 l-20,40 q-70,30 -140,0 Z" fill="#6b3a26" {o(4)}/>')
    px, py, pw, ph_ = 640, 460, 820, 480
    s += SL(Z_SRED, f'<path d="M{px:.0f},{py+ph_:.0f} L{px-20:.0f},{py+60:.0f} L{px+pw+20:.0f},{py+60:.0f} L{px+pw:.0f},{py+ph_:.0f} Z"'
                    f' fill="{KREM}" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{px+60:.0f},{py+100:.0f} q30,-60 60,0" fill="none" stroke="{ZEL}" stroke-width="6"/>')
    put = kontur_proema(px + 20, py + 60, pw - 40, ph_ - 120, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px + 20, py + 60, pw - 40, ph_ - 120, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(5)}/>')
    ded = figura(500, 1020, 420, t, KRAS, "#efe3c8", False, .0, True, boroda=True)
    s += SL(Z_SRED, ded)
    ruk1, (r1x, r1y) = rukav(560, 860, 150, -40, t, KRAS, "#efe3c8", .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(440, 860, 150, -140, t, KRAS, "#efe3c8", .3, 2)
    s += SL(Z_SRED, ruk1b)
    stoy = figura(960, 1060, 320, t, "#4a5a6b", "#cfe4f5", False, .3)
    s += SL(Z_SRED, stoy)
    tyanet = A.ease(A.seg(t % 3.0, .3, 2.0))
    ruk2, (r2x, r2y) = rukav(900, 940, 140, -50 - tyanet * 20, t, "#4a5a6b", "#cfe4f5", .3, 2)
    s += SL(Z_SRED, ruk2)
    ushi2 = 6 * A.w(t, 1.3)
    s += SL(Z_SRED, f'<path d="M930,{860+ushi2:.0f} l-8,-24 M990,{860+ushi2:.0f} l8,-24" stroke="{KREM}" stroke-width="5" fill="none"/>')
    mesh_sw = 4 * A.w(t, 1.1)
    s += SL(Z_SRED, f'<path d="M{1700+mesh_sw:.0f},860 q60,10 50,100" fill="none" stroke="#6b3a26" stroke-width="30" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<rect x="1700" y="880" width="180" height="140" rx="20" fill="#6b3a26" {o(4)}/>')
    s += SL(Z_SRED, svecha(586, 854, t, 0.46, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#1a0e08", .32))
    s += vinetka(.34)
    return s


def paket_v_shkolnom_koridore(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a2a30"/>'
    s += SL(Z_DAL, kladka(0, 0, W, 900, 80, "url(#kamen)"))
    for i in range(5):
        s += SL(Z_DAL, f'<rect x="{200+i*340}" y="200" width="30" height="620" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1400" y="200" width="420" height="700" fill="#1a1410" opacity=".85" {o(5)}/>')
    for h in range(6):
        s += SL(Z_SRED, f'<path d="M1420,{250+h*100:.0f} h380" stroke="{DOSKA}" stroke-width="10"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1440+i*110}" y="560" width="90" height="180" rx="8" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="500" width="200" height="320" rx="6" fill="{ZHELEZ}" {o(4)}/>')
    stup = (t * 60) % 400
    stoy_y = 760 + stup * .5
    boy = figura(900, stoy_y, 440, t, KREM, "#2a4a3a", False, .2)
    s += SL(Z_SRED, boy)
    ruk1, (r1x, r1y) = rukav(900, stoy_y - 320, 120, -40, t, KREM, "#2a4a3a", .2, 2)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<path d="M820,{stoy_y-100:.0f} v{-stup*.4:.0f}" stroke="{ZHELEZ}" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="{r1x-40:.0f}" y="{r1y-20:.0f}" width="80" height="60" fill="#6b3a26" {o(2)}/>')
    struyka_y = r1y - 60 - ((t * 40) % 300)
    s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y-30:.0f} q20,{-(r1y-30-struyka_y)*.3:.0f} 10,{struyka_y-r1y+30:.0f}"'
                    f' fill="none" stroke="#e8812a" stroke-width="6" opacity="{max(0,1-((t*40)%300)/300):.2f}"/>')
    s += SL(Z_SRED, f'<circle cx="{r1x+10:.0f}" cy="{struyka_y:.0f}" r="10" fill="{ZOL}" opacity="{max(0,1-((t*40)%300)/300):.2f}"/>')
    pov = 6 * A.w(t, 1.6)
    s += SL(Z_SRED, siluet(1600, 300, 220, "#0e0c10", .8))
    s += SL(Z_SRED, f'<g transform="rotate({pov:.1f} 1600 280)"><circle cx="1600" cy="280" r="4" fill="none"/></g>')
    s += SL(Z_SRED, f'<circle cx="960" cy="260" r="40" fill="{SVET}" opacity=".3"/>')
    s += SL(Z_SRED, svecha(809, 761, t, 0.81, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0c0c10", .4))
    s += vinetka(.42)
    return s


def paket_nesut_domoy(t):
    s = f'<rect width="{W}" height="{H}" fill="{NOCH}"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 45))
    s += SL(Z_DAL, izba_snaruzhi(1500, 900, 460, t, True, True, 7))
    s += SL(Z_DAL, f'<rect x="300" y="700" width="30" height="240" fill="{ZHELEZ}" {o(3)}/><ellipse cx="315" cy="690" rx="40" ry="16" fill="{SVET}" opacity=".8"/>')
    s += SL(Z_SRED, sneg_lezhit(880))
    s += SL(Z_SRED, pleten(1100, 800, 420, 140))
    s += SL(Z_SRED, f'<path d="M700,900 q200,-10 400,0" fill="none" stroke="{SNEG}" stroke-width="40" opacity=".6"/>')
    put = (t * 60) % 600
    boy = figura(300 + put, 1000, 460, t, "#2a4a5a", "#cfd6de", True, .0)
    s += SL(Z_SRED, boy)
    ruk1, (r1x, r1y) = rukav(380 + put, 706, 150, -40, t, "#2a4a5a", "#cfd6de", .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(220 + put, 706, 150, -140, t, "#2a4a5a", "#cfd6de", .3, 2)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<rect x="{(r1x+r1bx)/2-60:.0f}" y="{(r1y+r1by)/2+60:.0f}" width="120" height="70" rx="8" fill="#6b3a26" {o(3)}/>')
    girl = figura(1100, 1000, 300, t, "#8c3a3a", "#cfe4f5", True, .3)
    s += SL(Z_SRED, girl)
    tyanet = A.ease(A.seg(t % 4.0, 1.0, 1.0))
    ruk2, (r2x, r2y) = rukav(1180, 810, 110, -40 - tyanet * 10, t, "#8c3a3a", "#cfe4f5", .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, _varezhka(r2x, r2y, 1.1, 0, KRAS))
    if tyanet > .8:
        s += SL(Z_SRED, f'<rect x="{r2x-20:.0f}" y="{r2y-30:.0f}" width="40" height="18" rx="4" fill="{KREM}" {o(2)}/>')
    sobaka_x = 1300 + 20 * math.sin(t * 2)
    s += SL(Z_SRED, f'<ellipse cx="{sobaka_x:.0f}" cy="960" rx="60" ry="30" fill="#6b4a3a" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#040608", .42))
    s += SL(Z_LETIT, mokryy_sneg(t, 10, 47, .3, .5))
    s += vinetka(.46)
    return s


def konfety_po_poryadku(t):
    s = f'<rect width="{W}" height="{H}" fill="{DOSKA2}"/>'
    s += SL(Z_DAL, teplo(960, 300, 1200, 700, .3))
    s += SL(Z_SRED, f'<rect x="0" y="500" width="{W}" height="{H-500}" fill="{DOSKA}" {o(4)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{300+i*70}" cy="700" r="20" fill="{(KRAS,ZOL)[i%2]}" {o(2)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1100+i*80}" y="680" width="60" height="40" rx="6" fill="#6b4a2e" {o(2)}/>')
    otodv = A.ease(A.seg(t, .3, 1.4)) * 80
    s += SL(Z_SRED, f'<g transform="translate({otodv:.0f},0)">'
                    + ''.join(f'<rect x="{1060+i*80}" y="680" width="60" height="40" rx="6" fill="{TKAN}" opacity=".9" {o(2)}/>' for i in range(3))
                    + '</g>')
    s += SL(Z_SRED, f'<circle cx="760" cy="700" r="30" fill="{ZOL}" {o(2)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{900+i*18:.0f},700 q8,-16 0,-32" fill="none" stroke="#6b4a2e" stroke-width="4"/>')
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="700" rx="60" ry="30" fill="#efe3c8" opacity=".8" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1600" y="680" width="80" height="40" rx="6" fill="{KREM}" opacity=".5" {o(2)}/>')
    drozh = 3 * A.w(t, 2.4)
    s += SL(Z_SRED, f'<ellipse cx="{200+drozh:.0f}" cy="700" rx="60" ry="24" fill="{STEKLO}" opacity=".6" {o(2)}/>')
    rukx = 500
    ruk1, (r1x, r1y) = rukav(rukx, 500, 140, 70, t, KREM, KRAS, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(1140, 500, 140, 110, t, KREM, KRAS, .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, svecha(302, 838, t, 0.82, .8))
    s += SL(Z_SRED, _napolnenie(60, 560, 1800, 100, t, 203, 16))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .34))
    s += vinetka(.38)
    return s


def otkrytki_na_servante(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 49)
    s += SL(Z_DAL, okno_izby(1500, 160, 300, 300, t, svet=False, moroz=.2))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _servant(1120, 480, 420, 500, t))
    rnd = random.Random(104)
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{1150+i*54}" y="{860-i%2*10}" width="46" height="60" rx="3" fill="{(KRAS,KREM)[i%2]}" {o(2)}/>')
    s += SL(Z_SRED, stol(420, 760, 640, 34))
    s += SL(Z_SRED, lampa(500, 680, t, 1.0, True))
    s += SL(Z_SRED, f'<rect x="640" y="700" width="200" height="30" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="680" width="80" height="24" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, figura(560, 1040, 480, t, "#6b2a44", KREM, True, .2))
    ruk1, (r1x, r1y) = rukav(620, 780, 140, -30, t, "#6b2a44", KREM, .2, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(500, 780, 140, -150, t, "#6b2a44", KREM, .5, 2)
    s += SL(Z_SRED, ruk2)
    pero = A.seg(t % 3.0, .3, 2.4)
    s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y:.0f} h{-80*pero:.0f}" stroke="#2a1d14" stroke-width="3" stroke-dasharray="5 4"/>')
    marka = A.ease(A.seg(t, 2.6, .6))
    s += SL(Z_SRED, f'<rect x="{800-10*marka:.0f}" y="{690:.0f}" width="26" height="30" fill="{ZOL}" opacity="{marka:.2f}" {o(1)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.4)
    return s


def odekolon_v_korobochke(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 105)
    s += SL(Z_DAL, _oboi_fon("#4a4a4a", "#3a3a3a"))
    s += SL(Z_SRED, polovicy(840))
    zx, zy = 960, 500
    s += SL(Z_SRED, f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="220" fill="url(#zol)" {o(5)}/>')
    put = kontur_proema(zx - 190, zy - 190, 380, 380, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(zx - 190, zy - 190, 380, 380, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="680" width="400" height="60" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M740,680 q30,-30 60,0" fill="none" stroke="{SVET}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="820" y="630" width="30" height="50" rx="4" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M880,650 q30,10 30,40" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    kx, ky = 1200, 640
    s += SL(Z_SRED, _korobka(kx, ky, 220, 150, t, TKAN2, ZOL, True, .55, .1))
    flak = A.ease(A.seg(t, .3, .8))
    s += SL(Z_SRED, f'<rect x="{kx+80+flak*120:.0f}" y="{ky-60-flak*40:.0f}" width="36" height="70" rx="8" fill="{STEKLO}" opacity=".8" {o(3)}/>')
    zakr = A.ease(A.seg(t, 1.4, .8))
    s += SL(Z_SRED, f'<rect x="{kx-30:.0f}" y="{ky-40*(1-zakr):.0f}" width="150" height="20" fill="{KREM}" opacity="{zakr:.2f}"/>')
    polka_y = 320
    s += SL(Z_SRED, f'<rect x="1150" y="{polka_y:.0f}" width="260" height="30" rx="4" fill="url(#derev)" {o(4)}/>')
    vstal = A.ease(A.seg(t, 2.2, .8))
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1170+i*70}" y="{polka_y-40-vstal*10*0:.0f}" width="50" height="40" rx="4" fill="{(TKAN2,MED,ZEL2)[i]}" opacity=".9" {o(2)}/>')
    s += SL(Z_SRED, figura(600, 1060, 480, t, KREM, KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(660, 820, 140, -30, t, KREM, KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, svecha(515, 825, t, 0.05, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def dva_flakona_na_vidnom_meste(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 106)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _servant(760, 420, 420, 440, t))
    s += SL(Z_SRED, f'<rect x="760" y="860" width="420" height="30" rx="10" fill="{KREM}" {o(3)}/>')
    bx1, bx2 = 820, 1020
    otkr = A.ease(A.seg(t, .3, .8))
    s += SL(Z_SRED, f'<rect x="{bx1:.0f}" y="860" width="140" height="100" rx="10" fill="{TKAN2}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{bx1+20:.0f}" y="{860-otkr*30:.0f}" width="100" height="30" fill="{TKAN2}" opacity="{1-otkr:.2f}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{bx2:.0f}" y="860" width="110" height="80" rx="10" fill="{KRAS}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{bx2+55:.0f},860 q20,-20 0,-40" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<ellipse cx="1300" cy="700" rx="60" ry="30" fill="url(#zol)" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1420" cy="760" rx="50" ry="60" fill="{POBEL}" {o(3)}/><rect x="1400" y="700" width="40" height="30" rx="4" fill="#efe3c8" {o(2)}/>')
    stoy1 = figura(600, 1040, 470, t, "#8c3a6a", KREM, False, .0)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(680, 860, 140, -40, t, "#8c3a6a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    stoy2 = figura(1180, 1060, 480, t, "#3a3a5a", "#cfd6de", False, .3, True, shapka=True)
    s += SL(Z_SRED, f'<g transform="translate(0,{-10*(1-otkr):.0f})">{stoy2}</g>')
    nyuh = A.ease(A.seg(t, 1.6, 1.0))
    s += SL(Z_SRED, f'<g transform="rotate({-10*nyuh:.1f} 1100 900)">'
                    f'<ellipse cx="1100" cy="900" rx="20" ry="14" fill="#e0b08a" {o(2)}/></g>')
    s += SL(Z_SRED, svecha(385, 825, t, 1.85, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


# ═══════════════════════════ 109-121 ══════════════════════════════
def chto_govoryat_podarki(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 111)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="160" y="700" width="1600" height="60" rx="10" fill="url(#derev)" {o(5)}/>')
    items = [("chasy", 280, "grust"), ("nozh", 560, "grust"), ("platok", 840, "grust"),
             ("koshelek", 1120, "pusto"), ("banka", 1500, "radost")]
    for kind, gx, mood in items:
        if kind == "chasy":
            s += SL(Z_SRED, _chasy_sten(gx, 660, .6, t))
        elif kind == "nozh":
            s += SL(Z_SRED, _nozh_bolshoy(gx, 700, 90, t))
        elif kind == "platok":
            s += SL(Z_SRED, f'<rect x="{gx-30:.0f}" y="660" width="60" height="60" fill="{TKAN}" {o(2)}/>')
        elif kind == "koshelek":
            s += SL(Z_SRED, _koshelek(gx, 700, .9))
        else:
            s += SL(Z_SRED, _banka(gx, 700, .9, RUSH))
        app = A.ease(A.seg(t, items.index((kind, gx, mood)) * .9, .6))
        if app > .1:
            s += SL(Z_SRED, f'<g opacity="{app:.2f}">' + _oblako_rechi(gx, 560, .8 if mood != "radost" else 1.1, t, items.index((kind, gx, mood)) * .2, mood) + '</g>')
    s += SL(Z_SRED, svecha(200, 700, t, .3, .9))
    s += SL(Z_SRED, svecha(1780, 700, t, .5, .9))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def monetka_i_gorst_konfet(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 119)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 760, 1200, 34))
    s += SL(Z_SRED, _korobka(560, 660, 200, 140, t, TKAN2, ZOL, True, .0, .1))
    s += SL(Z_SRED, f'<path d="M1200,700 v-80 q0,-20 40,-20 q40,0 40,20 v80 Z" fill="{STEKLO}" opacity=".5" {o(4)}/>')
    app1 = A.ease(A.seg(t, .3, .6))
    s += SL(Z_SRED, f'<circle cx="640" cy="{650-(1-app1)*100:.0f}" r="16" fill="url(#zol)" {o(2)}/>')
    if app1 > .95:
        s += SL(Z_SRED, _galochka(560, 600, .8, t, 0))
    app2 = A.ease(A.seg(t, 1.3, .8))
    for i in range(int(6 * app2)):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<circle cx="{1240+rnd.random()*40:.0f}" cy="{620+rnd.random()*40:.0f}" r="10" fill="{(KRAS,ZOL)[i%2]}"/>')
    if app2 > .95:
        s += SL(Z_SRED, _galochka(1240, 560, .8, t, .3))
    s += SL(Z_SRED, f'<path d="M900,660 l-30,-70 l60,0 Z" fill="{ZEL}" {o(3)}/>')
    s += SL(Z_SRED, svecha(1000, 700, t, .4, .9))
    ruk1, (r1x, r1y) = rukav(640, 500, 160, 100, t, "#5a4a3a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(1280, 500, 160, 80, t, "#5a4a3a", KREM, .4, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, _napolnenie(60, 560, 260, 120, t, 205, 2))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def korobka_detskih_sokrovisch(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 121)
    s += SL(Z_DAL, _elka(1600, 960, 480, t, 53))
    s += SL(Z_SRED, f'<rect x="700" y="860" width="500" height="200" rx="16" fill="#efe3c8" opacity=".3" {o(2)}/>')
    kx, ky = 940, 820
    s += SL(Z_SRED, f'<rect x="{kx-180:.0f}" y="{ky:.0f}" width="360" height="200" rx="10" fill="#9c7049" opacity=".9" {o(5)}/>')
    dostal = A.ease(A.seg(t, .3, 1.0))
    mx, my = kx - 40, ky - dostal * 160
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="50" ry="40" fill="#8c6a4a" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{mx-20:.0f}" cy="{my-10:.0f}" r="20" fill="#8c6a4a" {o(2)}/>')
    s += SL(Z_SRED, f'<circle cx="{mx+26:.0f}" cy="{my-18:.0f}" r="10" fill="#8c6a4a" {o(1)}/>')
    s += SL(Z_SRED, f'<circle cx="{kx+60:.0f}" cy="{ky+40:.0f}" r="34" fill="{STEKLO}" opacity=".6" {o(2)}/>')
    blik_k = (t * 90) % 360
    s += SL(Z_SRED, f'<line x1="{kx+60:.0f}" y1="{ky+40:.0f}" x2="{kx+60+30*math.cos(math.radians(blik_k)):.0f}"'
                    f' y2="{ky+40+30*math.sin(math.radians(blik_k)):.0f}" stroke="{SVET}" stroke-width="3" opacity=".7"/>')
    s += SL(Z_SRED, f'<circle cx="{kx+130:.0f}" cy="{ky+20:.0f}" r="20" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+150:.0f}" y="{ky+60:.0f}" width="50" height="40" rx="4" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, figura(900, 1080, 440, t, "#8c8a94", KREM, False, .0, False, False, 0, False, False))
    ruk1, (r1x, r1y) = rukav(840, 860, 130, -60, t, "#8c8a94", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(960, 860, 130, -120, t, "#8c8a94", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    prizh = A.ease(A.seg(t, 1.6, 1.0))
    s += SL(Z_SRED, f'<ellipse cx="{(r1x+r2x)/2:.0f}" cy="{(r1y+r2y)/2-prizh*60:.0f}" rx="30" ry="24" fill="#8c6a4a" opacity="{.4+.6*prizh:.2f}" {o(2)}/>')
    kot(300, 940, t, .9, "#3b3430", False)
    s += SL(Z_SRED, kot(300, 940, t, .9, "#3b3430", False))
    vopros = A.ease(A.seg(t, 2.4, .6))
    if vopros > .1:
        s += SL(Z_SRED, f'<g opacity="{vopros:.2f}"><ellipse cx="1500" cy="320" rx="140" ry="80" fill="#ffffff" opacity=".9" {o(3)}/>'
                        f'<text x="1500" y="340" font-size="60" text-anchor="middle" fill="{K}">?</text></g>')
    s += SL(Z_SRED, svecha(650, 770, t, 1.7, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def chetyre_podarka_na_podokonnike(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, _oboi_fon("#4a3a3a", "#3a2e2e"))
    px, py, pw, ph_ = 560, 260, 800, 340
    s += SL(Z_DAL, f'<rect x="{px-30:.0f}" y="{py-30:.0f}" width="{pw+60}" height="{ph_+60}" rx="10" fill="url(#derev)" {o(7)}/>')
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_DAL, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_DAL, f'<path d="{put}" fill="none" {o(8)}/>')
    s += SL(Z_DAL, f'<line x1="{px+pw/2:.0f}" y1="{py:.0f}" x2="{px+pw/2:.0f}" y2="{py+ph_:.0f}" stroke="#2a1d14" stroke-width="6"/>')
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="{px-20:.0f}" y="{py+ph_:.0f}" width="{pw+40}" height="60" rx="8" fill="url(#derev)" {o(5)}/>')
    items = [("konvert", px + 60), ("varezhki", px + 280), ("banka", px + 500), ("blyudce", px + 700)]
    for i, (kind, ix) in enumerate(items):
        glow = .4 + .6 * max(0, 1 - abs(((t * .3) % 4) - i))
        if kind == "konvert":
            s += SL(Z_SRED, f'<rect x="{ix-40:.0f}" y="{py+ph_-10:.0f}" width="80" height="55" rx="4" fill="{KRAS}" opacity="{.7+.3*glow:.2f}" {o(3)}/>')
        elif kind == "varezhki":
            s += SL(Z_SRED, _varezhka(ix, py + ph_ + 20, .9, -8, KRAS))
            s += SL(Z_SRED, _varezhka(ix + 50, py + ph_ + 24, .9, 8, KRAS))
        elif kind == "banka":
            s += SL(Z_SRED, _banka(ix, py + ph_ + 36, .7, RUSH))
        else:
            s += SL(Z_SRED, f'<ellipse cx="{ix:.0f}" cy="{py+ph_+40:.0f}" rx="40" ry="14" fill="{KREM}" opacity="{.7+.3*glow:.2f}" {o(2)}/>'
                            f'<circle cx="{ix:.0f}" cy="{py+ph_+32:.0f}" r="10" fill="url(#zol)"/>')
        s += SL(Z_SRED, f'<ellipse cx="{ix:.0f}" cy="{py+ph_+40:.0f}" rx="60" ry="20" fill="{SVET}" opacity="{glow*.3:.2f}"/>')
    s += SL(Z_SRED, zanaveska(px - 60, py - 20, ph_ + 80, 100, TKAN, t, -1))
    s += SL(Z_SRED, zanaveska(px + pw + 60, py - 20, ph_ + 80, 100, TKAN, t, 1))
    s += SL(Z_SRED, kot(1500, 900, t, .9, "#3b3430", False))
    s += SL(Z_SRED, svecha(1600, 800, t, .4, 1.0))
    s += SL(Z_SRED, f'<path d="M1700,760 l-30,-70 l60,0 Z" fill="{ZEL}" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#040608", .38))
    s += vinetka(.42)
    return s


# источники света сцен: сюда ставится блик в объектив (C16/K17)
BLIKI = {
    "babushka_i_cennik": (960, 160),
    "babushka_pishet_zapisku_v_konvert": (1200, 700),
    "babushkin_nozh_poloska": (120, 760),
    "babushkina_shal": (173, 797),
    "banka_mezhdu_chaynikom_i_hlebnicey": (160, 780),
    "banka_s_konfetami_i_tarelka_s_yabl": (226, 834),
    "banka_v_sitcevoy_shapochke": (1000, 760),
    "chasy_i_dvoe_na_perrone": (1525, 660),
    "chasy_iz_vitriny_dlya_sebya": (260, 680),
    "chasy_na_zapyaste": (1660, 420),
    "chasy_v_krasnoy_korobke": (960, 180),
    "chay_i_frukty_v_podarok": (1020, 770),
    "chetyre_podarka_na_podokonnike": (1600, 800),
    "chto_govoryat_podarki": (200, 700),
    "chto_v_podarochnyy_paket": (279, 871),
    "devushka_u_tryumo": (332, 788),
    "dva_flakona_na_vidnom_meste": (385, 825),
    "gostevye_tapochki_u_vhoda": (438, 862),
    "gostincy_iz_svoego_sada": (231, 809),
    "hodiki_i_budilnik": (1660, 420),
    "kalendar_s_novym_godom": (1660, 420),
    "kartochka_drugogo_rolika": (1600, 800),
    "kniga_na_polke_cherez_gody": (491, 779),
    "kniga_s_nadpisyu": (600, 680),
    "konfety_po_poryadku": (302, 838),
    "konvert_dvumya_rukami": (544, 816),
    "kopeechka_chtoby_ne_possoritsya": (597, 853),
    "korobka_detskih_sokrovisch": (650, 770),
    "korzinka_dlya_vzroslyh_detey": (1350, 780),
    "koshelek_s_monetoy_i_vaza_s_gostin": (1250, 740),
    "koshelek_s_monetoy_na_donyshke": (1650, 700),
    "koza_v_sharfe_plede_i_varezhkah": (703, 807),
    "krasnyy_konvert": (960, 220),
    "mamina_shkatulka_s_zhemchugom": (373, 867),
    "moneta_iz_otcovskogo_yaschika": (756, 844),
    "monetka_i_gorst_konfet": (1000, 700),
    "monetka_za_chasy": (1400, 740),
    "monetka_za_podarok": (560, 700),
    "muzh_zhena_i_korobochka_s_chasami": (1500, 740),
    "nabor_nosovyh_platkov": (444, 796),
    "nabor_nozhey_dlya_docheri": (240, 420),
    "nagradnye_chasy": (1700, 420),
    "nozh_na_razdelochnoy_doske": (1700, 420),
    "nozh_rezhet_lentu_druzhby": (1000, 680),
    "nozhnicy_za_kopeyku": (960, 700),
    "odekolon_v_korobochke": (515, 825),
    "ognennaya_koza_u_elki_s_podarkami": (220, 420),
    "ostroe_na_barhate": (1600, 680),
    "ostroe_zhelezo_i_nechistaya_sila": (1760, 480),
    "otkrytki_na_servante": (500, 680),
    "paket_s_detskogo_prazdnika": (586, 854),
    "paket_v_shkolnom_koridore": (809, 761),
    "perochinnyy_nozhik_ot_deda": (1200, 760),
    "platki_u_vorot": (240, 540),
    "platok_polotence_i_tapochki": (260, 300),
    "podarki_vnuku_i_dedu": (1760, 420),
    "podarok_govorit": (900, 700),
    "podarok_s_yarlykom": (1760, 720),
    "podokonnik_s_konfetami": (862, 798),
    "pokupayu": (915, 835),
    "polotence_na_vesah": (760, 700),
    "polotence_na_vorotah_i_na_svadbe": (1500, 700),
    "polotence_ot_chuzhoy": (968, 872),
    "primeta_uhodit": (400, 700),
    "pustaya_krinka": (1700, 380),
    "pustoy_koshelek_i_pustoy_god": (1000, 740),
    "s_tebya_kopeyka": (1021, 789),
    "sem_podarkov_na_servante": (1300, 700),
    "sharf_dlya_muzha": (1074, 826),
    "shkolnyy_zal_s_elkoy": (1127, 863),
    "slezy_rusalki": (1180, 780),
    "stopka_noskov_s_birkami": (1233, 817),
    "struzhka_i_svistulka": (1400, 820),
    "suvenir_v_shkafu": (1286, 854),
    "tapochki_v_podarochnoy_korobke": (1339, 771),
    "tri_govoryaschie_veschi": (1120, 760),
    "tri_pravilnyh_podarka": (1660, 360),
    "tri_vykuplennyh_podarka": (300, 700),
    "vecher_protiv_pensii": (657, 783),
    "vechera_nad_vyazanem": (1180, 620),
    "vnuk_prines_tapochki": (1392, 808),
    "vnuki_s_konvertami": (1445, 845),
    "vyazanye_noski_idut_mimo_primety": (1498, 762),
    "yarmarochnyy_larek_s_platkami": (728, 812),
}
