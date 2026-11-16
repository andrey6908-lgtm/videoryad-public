# -*- coding: utf-8 -*-
"""СКВОЗНЫЕ ОБРАЗЫ РОЛИКА «18 ноября — День Ионы».

День поздней осени: земля голая, первый мокрый снег, сизые сумерки, рано
темнеет. Холод снаружи — тепло внутри, тёплое пятно в кадре всегда одно.
Эти кирпичики общие для всех 102 декораций ролика и живут отдельно от
`baza.py`, чтобы сцены не повторяли друг друга кодом.
"""
import math, random
from baza import *
import anim as A


# --- АНАТОМИЯ (R-0051, 15.11.2026) ----------------------------------------
# Его слово 15.11: «какие-то три руки… должны соответствовать механике, физике,
# откуда у человека что растёт». Третья рука рождалась так: сцена рисовала
# фигуру (у неё два рукава) и СВЕРХУ свою тянущуюся руку через rukav().
# Лечение: кадр собирается в два прохода. Первый проход запоминает, куда
# крепятся внешние руки, второй — фигура не рисует свой рукав на том плече,
# откуда уже растёт внешняя рука. Гейт: anatomiya.py.
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


# ═══════════════════════════════════════════════════════════════════
# ОБЩИЕ КИРПИЧИКИ РОЛИКА «18 ноября — День Ионы» (перенесены из chast1
# 15.11, чтобы порции 2 и 3 рисовали ТЕМИ ЖЕ руками и вещами, а не
# изобретали заново — на первой порции именно самодельные руки дали
# бруски сквозь тело и лицо).
#   _ruka / _ruka_ekr / _ruka_so_sgibom — рука ТОЛЬКО от плеча, угол в
#     наружном коридоре −58°…+88°, с оплечьем: в голову и грудь своей
#     фигуры не попадает ни при каких числах;
#   _venik_v_ruke — веник держится ЗА ЧЕРЕНОК, а не висит рядом;
#   остальное — обжитые мелочи двора, улицы, горницы и города.
# ═══════════════════════════════════════════════════════════════════

def _zemlya(y0, h_=480, col="#4a4038", op=1.0):
    """Широкая полоса земли/пола/воды внизу кадра: крупный предмет (R-0047)
    и опора под ногами одним движением."""
    return f'<rect x="0" y="{y0:.0f}" width="{W}" height="{h_:.0f}" fill="{col}" opacity="{op:.2f}"/>'


def _plecho(x, y, h_, storona):
    """Точка плеча figura(x,y,h_,...) для rukav(): -1 левое плечо, 1 правое."""
    w_ = h_ * .42
    return x + storona * w_ * .40, y - h_ * .66 + h_ * .02


def _trava(rnd, n, y0, y1, col=ZEL2):
    s = ""
    for _ in range(n):
        gx = rnd.uniform(30, W - 30); gy = rnd.uniform(y0, y1)
        h2 = rnd.uniform(26, 56)
        s += (f'<path d="M{gx:.0f},{gy:.0f} q{rnd.uniform(-14,14):.0f},{-h2:.0f}'
              f' {rnd.uniform(-8,8):.0f},{-h2*1.3:.0f}" fill="none" stroke="{col}"'
              f' stroke-width="5" opacity=".6"/>')
    return s


def _zabor_dosok(x, y, w_, h_, seed=5, step=58, col="url(#derev)"):
    """Дощатый забор: каждая доска отдельная, с зазором и прожилиной, две
    поперечины. Забор держит средний план там, где иначе пустое небо."""
    rnd = random.Random(seed)
    s = ""
    n = max(3, int(w_ // step))
    for i in range(n):
        bx = x + i * step
        dh = h_ * rnd.uniform(.90, 1.0)
        ty = y + (h_ - dh)
        s += (f'<rect x="{bx:.0f}" y="{ty:.0f}" width="{step-14:.0f}" height="{dh:.0f}"'
              f' rx="6" fill="{col}" {o(4)}/>'
              f'<line x1="{bx+9:.0f}" y1="{ty+22:.0f}" x2="{bx+9:.0f}" y2="{y+h_-20:.0f}"'
              f' stroke="#2c1f14" stroke-width="3" opacity=".45"/>')
    for k in (.28, .76):
        s += (f'<rect x="{x-10:.0f}" y="{y+h_*k:.0f}" width="{w_+20:.0f}" height="18"'
              f' rx="6" fill="#3f2d1c" {o(4)}/>')
    return s


def _polenica(x, y, w_, h_, seed=7, r=27):
    """Поленница под навесом: колотые поленья торцами, разного калибра и
    тона, в рядах вперевязку; у части виден клин раскола."""
    rnd = random.Random(seed)
    tona = ["url(#derev)", "#6b4e30", "#7b5c38", "#5a4228", "#8a6a44"]
    s = (f'<rect x="{x-10:.0f}" y="{y+h_:.0f}" width="{w_+20:.0f}" height="20" rx="6"'
         f' fill="#33261a" {o(4)}/>')
    ry = max(1, int(h_ // (r * 1.78)))
    rx = max(1, int(w_ // (r * 1.86)))
    for j in range(ry):
        for i in range(rx):
            rr = r * rnd.uniform(.76, 1.12)
            cx = x + r + i * r * 1.86 + (r * .52 if j % 2 else 0) + rnd.uniform(-4, 4)
            cy = y + h_ - r - j * r * 1.78 + rnd.uniform(-5, 5)
            if cx > x + w_ - r * .4:
                continue
            s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}"'
                  f' fill="{tona[rnd.randrange(len(tona))]}" {o(4)}/>')
            if rnd.random() < .45:
                s += (f'<path d="M{cx-rr*.72:.0f},{cy-rr*.30:.0f}'
                      f' Q{cx:.0f},{cy+rr*.16:.0f} {cx+rr*.66:.0f},{cy-rr*.40:.0f}"'
                      f' fill="none" stroke="#5e442a" stroke-width="4" opacity=".7"/>')
            else:
                s += (f'<path d="M{cx-rr*.86:.0f},{cy-rr*.20:.0f}'
                      f' L{cx+rr*.20:.0f},{cy+rr*.14:.0f}'
                      f' L{cx+rr*.10:.0f},{cy-rr*.80:.0f} Z" fill="#8f7048"'
                      f' opacity=".55"/>')
            if rnd.random() < .28:
                s += (f'<line x1="{cx:.0f}" y1="{cy-rr*.76:.0f}" x2="{cx+rr*.18:.0f}"'
                      f' y2="{cy+rr*.76:.0f}" stroke="#432f1c" stroke-width="4"'
                      f' opacity=".65"/>')
    s += (f'<rect x="{x-24:.0f}" y="{y-26:.0f}" width="{w_+48:.0f}" height="26" rx="8"'
          f' fill="#4a3826" {o(5)}/>')
    return s


def _dvorovaya_utvar(x, y, w_, t, seed=9, nabor=None):
    """Дворовая утварь в рост полметра: кадка, вёдра, корзина, мешок, короб.
    Ставится НА землю у стены — та самая «сопутствующая вещь»."""
    rnd = random.Random(seed)
    veschi = nabor or ["kadka", "vedro", "korzina", "meshok", "korob", "vedro"]
    s = ""
    step = w_ / max(1, len(veschi))
    for i, v in enumerate(veschi):
        vx = x + step * (i + .5) + rnd.uniform(-14, 14)
        k = rnd.uniform(.86, 1.12)
        if v == "kadka":
            h2, w2 = 150 * k, 124 * k
            s += (f'<path d="M{vx-w2/2:.0f},{y-h2:.0f} L{vx+w2/2:.0f},{y-h2:.0f}'
                  f' L{vx+w2*.42:.0f},{y:.0f} L{vx-w2*.42:.0f},{y:.0f} Z"'
                  f' fill="url(#derev)" {o(5)}/>'
                  f'<rect x="{vx-w2/2-4:.0f}" y="{y-h2*.86:.0f}" width="{w2+8:.0f}" height="14"'
                  f' rx="5" fill="{ZHELEZ}" {o(3)}/>'
                  f'<rect x="{vx-w2*.46:.0f}" y="{y-h2*.26:.0f}" width="{w2*.92:.0f}"'
                  f' height="14" rx="5" fill="{ZHELEZ}" {o(3)}/>'
                  f'<ellipse cx="{vx:.0f}" cy="{y-h2:.0f}" rx="{w2/2:.0f}" ry="{w2*.15:.0f}"'
                  f' fill="#2a1d12" {o(4)}/>')
        elif v == "vedro":
            h2, w2 = 112 * k, 96 * k
            s += (f'<path d="M{vx-w2/2:.0f},{y-h2:.0f} L{vx+w2/2:.0f},{y-h2:.0f}'
                  f' L{vx+w2*.36:.0f},{y:.0f} L{vx-w2*.36:.0f},{y:.0f} Z"'
                  f' fill="url(#zhel)" {o(5)}/>'
                  f'<path d="M{vx-w2/2:.0f},{y-h2:.0f} Q{vx:.0f},{y-h2-w2*.6:.0f}'
                  f' {vx+w2/2:.0f},{y-h2:.0f}" fill="none" stroke="{ZHELEZ}" stroke-width="7"/>'
                  f'<ellipse cx="{vx:.0f}" cy="{y-h2:.0f}" rx="{w2/2:.0f}" ry="{w2*.16:.0f}"'
                  f' fill="#2f3337" {o(4)}/>')
        elif v == "korzina":
            h2, w2 = 108 * k, 136 * k
            s += (f'<path d="M{vx-w2/2:.0f},{y-h2:.0f} L{vx+w2/2:.0f},{y-h2:.0f}'
                  f' L{vx+w2*.34:.0f},{y:.0f} L{vx-w2*.34:.0f},{y:.0f} Z"'
                  f' fill="url(#solom)" {o(5)}/>')
            for q in range(3):
                yy = y - h2 * .74 + q * h2 * .26
                s += (f'<path d="M{vx-w2*.44:.0f},{yy:.0f} Q{vx:.0f},{yy+16:.0f}'
                      f' {vx+w2*.44:.0f},{yy:.0f}" fill="none" stroke="#8a6a3c"'
                      f' stroke-width="5" opacity=".8"/>')
            s += (f'<path d="M{vx-w2*.4:.0f},{y-h2:.0f} Q{vx:.0f},{y-h2-w2*.5:.0f}'
                  f' {vx+w2*.4:.0f},{y-h2:.0f}" fill="none" stroke="#8a6a3c" stroke-width="8"/>')
        elif v == "meshok":
            h2, w2 = 134 * k, 108 * k
            s += (f'<path d="M{vx-w2/2:.0f},{y:.0f} Q{vx-w2*.56:.0f},{y-h2*.62:.0f}'
                  f' {vx-w2*.2:.0f},{y-h2:.0f} Q{vx:.0f},{y-h2-16:.0f}'
                  f' {vx+w2*.2:.0f},{y-h2:.0f} Q{vx+w2*.56:.0f},{y-h2*.62:.0f}'
                  f' {vx+w2/2:.0f},{y:.0f} Z" fill="url(#krem)" {o(5)}/>'
                  f'<path d="M{vx-w2*.2:.0f},{y-h2:.0f} Q{vx:.0f},{y-h2-18:.0f}'
                  f' {vx+w2*.2:.0f},{y-h2:.0f}" fill="none" stroke="#8a7a58" stroke-width="6"/>')
        elif v == "korob":
            h2, w2 = 102 * k, 150 * k
            s += (f'<rect x="{vx-w2/2:.0f}" y="{y-h2:.0f}" width="{w2:.0f}" height="{h2:.0f}"'
                  f' rx="8" fill="url(#derev)" {o(5)}/>'
                  f'<rect x="{vx-w2/2:.0f}" y="{y-h2:.0f}" width="{w2:.0f}" height="20" rx="6"'
                  f' fill="#5b4328" {o(4)}/>'
                  f'<line x1="{vx-w2*.3:.0f}" y1="{y-h2+22:.0f}" x2="{vx-w2*.3:.0f}"'
                  f' y2="{y-6:.0f}" stroke="#3a2a1a" stroke-width="4" opacity=".6"/>')
        else:
            h2, w2 = 96 * k, 118 * k
            s += (f'<ellipse cx="{vx:.0f}" cy="{y-h2*.5:.0f}" rx="{w2*.46:.0f}"'
                  f' ry="{h2*.5:.0f}" fill="url(#glina)" {o(5)}/>')
        s += ten(vx, y + 6, w2 * .56, 13, .45)
    return s


def _polka_s_utvaryu(x, y, w_, t, seed=11, n=5):
    """Полка на стене и посуда НА ней: горшки, крынки, миски, короб, связка
    трав. Мелочь кладётся на предмет, а не рассыпается по полу."""
    rnd = random.Random(seed)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="20" rx="6"'
         f' fill="url(#derev)" {o(5)}/>'
         f'<rect x="{x+22:.0f}" y="{y+20:.0f}" width="22" height="34" fill="#4a3522" {o(4)}/>'
         f'<rect x="{x+w_-44:.0f}" y="{y+20:.0f}" width="22" height="34" fill="#4a3522" {o(4)}/>')
    step = (w_ - 60) / max(1, n)
    for i in range(n):
        px = x + 40 + step * i + step * .5
        vid = rnd.randrange(4)
        h2 = rnd.uniform(78, 124)
        if vid == 0:
            s += (f'<path d="M{px-34:.0f},{y:.0f} Q{px-48:.0f},{y-h2*.5:.0f}'
                  f' {px-30:.0f},{y-h2:.0f} L{px+30:.0f},{y-h2:.0f}'
                  f' Q{px+48:.0f},{y-h2*.5:.0f} {px+34:.0f},{y:.0f} Z"'
                  f' fill="url(#glina)" {o(5)}/>'
                  f'<ellipse cx="{px:.0f}" cy="{y-h2:.0f}" rx="34" ry="11" fill="#6d4e32" {o(4)}/>')
        elif vid == 1:
            s += (f'<path d="M{px-30:.0f},{y:.0f} L{px-24:.0f},{y-h2*.62:.0f}'
                  f' Q{px:.0f},{y-h2*.86:.0f} {px+24:.0f},{y-h2*.62:.0f}'
                  f' L{px+30:.0f},{y:.0f} Z" fill="url(#krem)" {o(5)}/>'
                  f'<rect x="{px-22:.0f}" y="{y-h2:.0f}" width="44" height="18" rx="7"'
                  f' fill="#9a8a68" {o(4)}/>')
        elif vid == 2:
            s += (f'<path d="M{px-44:.0f},{y-h2*.42:.0f} Q{px:.0f},{y+14:.0f}'
                  f' {px+44:.0f},{y-h2*.42:.0f} L{px+36:.0f},{y-h2*.6:.0f}'
                  f' Q{px:.0f},{y-h2*.2:.0f} {px-36:.0f},{y-h2*.6:.0f} Z"'
                  f' fill="url(#zhel)" {o(5)}/>')
        else:
            s += (f'<rect x="{px-38:.0f}" y="{y-h2:.0f}" width="76" height="{h2:.0f}" rx="7"'
                  f' fill="url(#derev)" {o(5)}/>'
                  f'<line x1="{px-38:.0f}" y1="{y-h2*.5:.0f}" x2="{px+38:.0f}"'
                  f' y2="{y-h2*.5:.0f}" stroke="#3a2a1a" stroke-width="4" opacity=".6"/>')
    kach = 3.0 * A.w(t, 3.4, .2)
    tx = x + w_ - 36
    s += (f'<g transform="rotate({kach:.1f} {tx:.0f} {y:.0f})">'
          f'<path d="M{tx-10:.0f},{y:.0f} L{tx+2:.0f},{y+74:.0f} L{tx+18:.0f},{y:.0f} Z"'
          f' fill="#6f7a44" {o(4)}/>'
          f'<line x1="{tx+0:.0f}" y1="{y+26:.0f}" x2="{tx-20:.0f}" y2="{y+48:.0f}"'
          f' stroke="#6f7a44" stroke-width="5"/>'
          f'<line x1="{tx+8:.0f}" y1="{y+46:.0f}" x2="{tx+28:.0f}" y2="{y+66:.0f}"'
          f' stroke="#6f7a44" stroke-width="5"/></g>')
    return s


def _derevnya_ryad(base, t, seed=7, mesta=((300, 440), (880, 380), (1560, 500))):
    """Ряд изб разной величины по дальнему плану — улица, а не пустое поле."""
    s = ""
    for i, (mx, mw) in enumerate(mesta):
        s += izba_snaruzhi(mx, base + (i % 2) * 16, mw, t, svet=True, truba=True,
                           seed=seed + i * 3)
    return s


def _bulyzhnik(y0, y1, seed=13, n=90, col="#5a5248"):
    """Булыжная мостовая: камни рядами, ближе к низу крупнее."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        p = rnd.random()
        cy = y0 + (y1 - y0) * (p ** .7)
        r = 20 + 44 * ((cy - y0) / max(1, y1 - y0))
        cx = rnd.uniform(-30, W + 30)
        tn = rnd.uniform(-.08, .08)
        s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r*1.22:.0f}" ry="{r*.72:.0f}"'
              f' fill="{col}" opacity="{.85+tn:.2f}" {o(3)}/>'
              f'<ellipse cx="{cx-r*.22:.0f}" cy="{cy-r*.2:.0f}" rx="{r*.56:.0f}"'
              f' ry="{r*.3:.0f}" fill="#6e665b" opacity=".45"/>')
    return s


def _listya(seed, n, y0, y1, cols=("#9a5a28", "#b4762f", "#7d4a24", "#c08a3a")):
    """Палая листва поздней осени — лежит НА земле, пятном не висит."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        lx, ly = rnd.uniform(0, W), rnd.uniform(y0, y1)
        r = rnd.uniform(17, 31)
        ug = rnd.uniform(0, 360)
        s += (f'<g transform="rotate({ug:.0f} {lx:.0f} {ly:.0f})">'
              f'<path d="M{lx-r:.0f},{ly:.0f} Q{lx:.0f},{ly-r*.86:.0f} {lx+r:.0f},{ly:.0f}'
              f' Q{lx:.0f},{ly+r*.86:.0f} {lx-r:.0f},{ly:.0f} Z"'
              f' fill="{cols[i%len(cols)]}" opacity=".9" {o(2)}/>'
              f'<line x1="{lx-r:.0f}" y1="{ly:.0f}" x2="{lx+r:.0f}" y2="{ly:.0f}"'
              f' stroke="#6a4120" stroke-width="2" opacity=".7"/></g>')
    return s


def _vetka_pered(x, y, dl, ug, t, seed=3, col="#241c16", vetok=6):
    """Ветка у самого объектива: держит ближний план и качается целиком."""
    rnd = random.Random(seed)
    kach = 1.6 * A.w(t, 4.2, .3)
    r = math.radians(ug)
    x2, y2 = x + dl * math.cos(r), y + dl * math.sin(r)
    s = (f'<g transform="rotate({kach:.2f} {x:.0f} {y:.0f})">'
         f'<path d="M{x:.0f},{y:.0f} Q{(x+x2)/2:.0f},{(y+y2)/2-40:.0f} {x2:.0f},{y2:.0f}"'
         f' fill="none" stroke="{col}" stroke-width="22" stroke-linecap="round"/>')
    for i in range(vetok):
        p = .18 + .76 * i / max(1, vetok - 1)
        bx = x + (x2 - x) * p
        by = y + (y2 - y) * p - 40 * math.sin(math.pi * p)
        dl2 = rnd.uniform(70, 140)
        a2 = r + rnd.uniform(-1.1, 1.1)
        s += (f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx+dl2*math.cos(a2):.0f}"'
              f' y2="{by+dl2*math.sin(a2):.0f}" stroke="{col}" stroke-width="10"'
              f' stroke-linecap="round"/>')
    s += "</g>"
    return s


def _stolb_pered(x, w_, col="#1d1611", ot=0, do=H):
    """Столб/косяк у самого края кадра — ближний план, ради объёма."""
    return (f'<rect x="{x:.0f}" y="{ot:.0f}" width="{w_:.0f}" height="{do-ot:.0f}"'
            f' fill="{col}" {o(6)}/>'
            f'<rect x="{x+w_*.18:.0f}" y="{ot:.0f}" width="{w_*.2:.0f}" height="{do-ot:.0f}"'
            f' fill="#2e2219" opacity=".7"/>')


def _kryl_co(x, y, w_, h_, t, stup=3, peril=True, naves=False):
    """Крыльцо: настил, ступени, столбы, перила с балясинами, при нужде навес."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="34" rx="6"'
         f' fill="url(#derev)" {o(5)}/>'
         f'<rect x="{x+10:.0f}" y="{y+34:.0f}" width="{w_-20:.0f}" height="{h_:.0f}"'
         f' fill="#3a2b1c" {o(4)}/>')
    for i in range(stup):
        sw = w_ * (.62 - .1 * i)
        sx = x + w_ * .5 - sw * .5
        s += (f'<rect x="{sx:.0f}" y="{y+34+h_*(i+1)/(stup+1):.0f}" width="{sw:.0f}"'
              f' height="26" rx="5" fill="url(#derev)" {o(4)}/>')
    if peril:
        for px in (x + 14, x + w_ - 40):
            s += (f'<rect x="{px:.0f}" y="{y-130:.0f}" width="26" height="140" rx="6"'
                  f' fill="#4e3a24" {o(4)}/>')
        s += (f'<rect x="{x+8:.0f}" y="{y-134:.0f}" width="{w_-14:.0f}" height="20" rx="7"'
              f' fill="#5b4428" {o(5)}/>')
        for i in range(5):
            bx = x + 54 + i * (w_ - 118) / 4.0
            s += (f'<path d="M{bx:.0f},{y-114:.0f} Q{bx+16:.0f},{y-92:.0f}'
                  f' {bx:.0f},{y-70:.0f} Q{bx-16:.0f},{y-48:.0f} {bx:.0f},{y-24:.0f}'
                  f' L{bx+16:.0f},{y-24:.0f} Q{bx:.0f},{y-48:.0f} {bx+16:.0f},{y-70:.0f}'
                  f' Q{bx+32:.0f},{y-92:.0f} {bx+16:.0f},{y-114:.0f} Z"'
                  f' fill="#6a5030" {o(3)}/>')
    if naves:
        s += (f'<path d="M{x-34:.0f},{y-250:.0f} L{x+w_/2:.0f},{y-320:.0f}'
              f' L{x+w_+34:.0f},{y-250:.0f} Z" fill="#4a3a28" {o(5)}/>'
              f'<rect x="{x-40:.0f}" y="{y-256:.0f}" width="{w_+80:.0f}" height="22" rx="7"'
              f' fill="#5c4830" {o(4)}/>')
    return s


def _koleya(y, seed=21, n=2):
    """След тележного колеса на мёрзлой земле: две колеи и ледок в них."""
    s = ""
    for i in range(n):
        yy = y + i * 62
        s += (f'<path d="M-40,{yy:.0f} Q480,{yy-30-i*8:.0f} 1000,{yy-10:.0f}'
              f' Q1500,{yy+6:.0f} 1960,{yy-14:.0f}" fill="none" stroke="#3a3028"'
              f' stroke-width="{26-i*5}" opacity=".8"/>'
              f'<path d="M-40,{yy-8:.0f} Q480,{yy-38-i*8:.0f} 1000,{yy-18:.0f}'
              f' Q1500,{yy-2:.0f} 1960,{yy-22:.0f}" fill="none" stroke="#7d8f9c"'
              f' stroke-width="5" opacity=".45"/>')
    return s


def _stena_gornicy(t, seed=5, venec=True, pol_y=760, bok=True):
    """Задник горницы: бревенчатая стена во весь кадр, матица, венцы по углам,
    половицы и плинтус. Это фон — плотность на нём набирается предметами."""
    s = brevna(0, 0, W, pol_y + 40, 96)
    if venec:
        s += (f'<rect x="0" y="{pol_y-10:.0f}" width="{W}" height="26" fill="#3b2a1a"'
              f' opacity=".9"/>'
              f'<rect x="0" y="86" width="{W}" height="28" fill="#4a3522" opacity=".55"/>')
    s += polovicy(pol_y + 30)
    if bok:
        s += (f'<rect x="0" y="0" width="86" height="{pol_y+40:.0f}" fill="#241a11"'
              f' opacity=".55"/>'
              f'<rect x="{W-86}" y="0" width="86" height="{pol_y+40:.0f}" fill="#241a11"'
              f' opacity=".55"/>')
    return s


def _zemlya_faktura(y0, y1, seed=3, n=16, kom="#3f3326"):
    """Мёрзлая земля вблизи: комья, камни, проплешины, лужицы с ледком —
    чтобы полоса земли не читалась крашеной доской."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        gx, gy = rnd.uniform(-40, W + 40), rnd.uniform(y0, y1)
        rx_ = rnd.uniform(70, 190)
        s += (f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="{rx_:.0f}" ry="{rx_*.26:.0f}"'
              f' fill="{kom}" opacity="{rnd.uniform(.30,.5):.2f}"/>')
        if rnd.random() < .4:
            s += (f'<ellipse cx="{gx+rnd.uniform(-40,40):.0f}" cy="{gy+18:.0f}"'
                  f' rx="{rx_*.44:.0f}" ry="{rx_*.13:.0f}" fill="#6d7f8c"'
                  f' opacity=".45"/>')
        if rnd.random() < .34:
            r2 = rnd.uniform(16, 34)
            s += (f'<ellipse cx="{gx+rnd.uniform(-70,70):.0f}" cy="{gy-6:.0f}"'
                  f' rx="{r2:.0f}" ry="{r2*.72:.0f}" fill="#6a6256" {o(2)}/>')
    return s


def _venik(vx, vy, h2, t, col, tryap, birka=False, rastr=.0, ph=.0, s_=1.0,
           seed=None):
    """Веник, который видно со стоп-кадра (R-0047): прутья веером, перевязь,
    ручка, обмахрённый низ. Качается целиком."""
    rr = random.Random(seed if seed is not None else int(vx))
    kach = 3.4 * A.w(t, 2.2, ph)
    g = f'<g transform="rotate({kach:.1f} {vx:.0f} {vy:.0f})">'
    n = 23
    for i in range(n):
        p = (i / (n - 1.0)) - .5
        raz = (1.0 + rastr * rr.uniform(0, 1.6))
        ex = vx + p * 180 * s_ * raz
        ey = vy - h2 + rr.uniform(-30, 20) * raz
        g += (f'<path d="M{vx+p*34*s_:.0f},{vy-h2*.40:.0f}'
              f' Q{vx+p*118*s_:.0f},{vy-h2*.76:.0f} {ex:.0f},{ey:.0f}"'
              f' fill="none" stroke="{col}" stroke-width="{9*s_:.0f}"'
              f' stroke-linecap="round" opacity=".92"/>')
    g += (f'<rect x="{vx-28*s_:.0f}" y="{vy-h2*.42:.0f}" width="{56*s_:.0f}"'
          f' height="{h2*.46:.0f}" rx="18" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{vx-44*s_:.0f}" y="{vy-h2*.50:.0f}" width="{88*s_:.0f}"'
          f' height="{34*s_:.0f}" rx="12" fill="{tryap}" {o(4)}/>'
          f'<rect x="{vx-40*s_:.0f}" y="{vy-h2*.28:.0f}" width="{80*s_:.0f}"'
          f' height="{24*s_:.0f}" rx="10" fill="#8a6a3c" {o(3)}/>')
    if tryap == "#b8352c":
        tr = 8 * A.w(t, 1.7, ph + .5)
        g += (f'<path d="M{vx+40*s_:.0f},{vy-h2*.48:.0f}'
              f' Q{vx+86*s_+tr:.0f},{vy-h2*.42:.0f} {vx+70*s_:.0f},{vy-h2*.30:.0f} Z"'
              f' fill="#b8352c" {o(3)}/>')
    if birka:
        bk = 4 * A.w(t, 1.8, ph + .3)
        g += (f'<g transform="rotate({bk:.1f} {vx+34*s_:.0f} {vy-h2*.28:.0f})">'
              f'<line x1="{vx+34*s_:.0f}" y1="{vy-h2*.28:.0f}" x2="{vx+52*s_:.0f}"'
              f' y2="{vy-h2*.14:.0f}" stroke="#cbbb98" stroke-width="4"/>'
              f'<rect x="{vx+34*s_:.0f}" y="{vy-h2*.14:.0f}" width="{52*s_:.0f}"'
              f' height="{68*s_:.0f}" rx="8" fill="#efe4c8" {o(4)}/>'
              f'<path d="M{vx+44*s_:.0f},{vy-h2*.14+30*s_:.0f}'
              f' Q{vx+58*s_:.0f},{vy-h2*.14+20*s_:.0f}'
              f' {vx+74*s_:.0f},{vy-h2*.14+30*s_:.0f}" fill="none" stroke="#9a8a68"'
              f' stroke-width="4"/></g>')
    g += "</g>"
    return g


def _venik_v_ruke(ex, ey, h2, t, col="#4b3f28", tryap="#5a4a2e", ug=96.0, s_=.9,
                  seed=None, rastr=.25, ph=.0):
    """ВЕНИК В РУКЕ ДЕРЖИТСЯ ЗА ЧЕРЕНОК. Осмотр 15.11: «веник висит в воздухе
    без руки» и «черенок веника лежит поперёк лица» — сцены ставили веник
    смещённым на 180-330 px ниже кисти, то есть ни одним концом её не
    касались, да ещё прутьями к хозяйке.

    `_venik()` рисует прутья СВЕРХУ (от vy-h2 до vy-h2*.42), а черенок снизу,
    и его нижний конец приходится ровно на vy. Значит кисть — это vy, и
    остаётся только повернуть: `ug` — куда смотрят ПРУТЬЯ в экранных
    градусах (96 — вниз и чуть вперёд, -40 — вверх-вправо, 196 — влево).
    Прутья всегда уводятся ОТ фигуры, а не на неё.
    """
    return (f'<g transform="rotate({ug + 90:.1f} {ex:.0f} {ey:.0f})">'
            + _venik(ex, ey, h2, t, col, tryap, False, rastr, ph, s_, seed)
            + "</g>")


def _gorodskoy_hlam(x, y, w_, t, seed=7, nabor=None):
    """Двор у подъезда: столбик-ограждение, ящик, картонная коробка, пакет,
    куст в кадке, велосипед у стены. Городская «сопутствующая вещь»."""
    rnd = random.Random(seed)
    veschi = nabor or ["stolbik", "yaschik", "korobka", "kust", "velik", "stolbik"]
    s = ""
    step = w_ / max(1, len(veschi))
    for i, v in enumerate(veschi):
        vx = x + step * (i + .5) + rnd.uniform(-12, 12)
        if v == "stolbik":
            s += (f'<rect x="{vx-20:.0f}" y="{y-180:.0f}" width="40" height="180" rx="14"'
                  f' fill="#4a5055" {o(5)}/>'
                  f'<rect x="{vx-26:.0f}" y="{y-192:.0f}" width="52" height="20" rx="9"'
                  f' fill="#6a7278" {o(3)}/>'
                  f'<rect x="{vx-20:.0f}" y="{y-120:.0f}" width="40" height="18"'
                  f' fill="#c0c6ca" opacity=".8"/>')
        elif v == "yaschik":
            s += (f'<rect x="{vx-86:.0f}" y="{y-140:.0f}" width="172" height="140"'
                  f' rx="8" fill="#6b5a3c" {o(5)}/>')
            for k in range(3):
                s += (f'<rect x="{vx-80:.0f}" y="{y-132+k*46:.0f}" width="160"'
                      f' height="30" rx="5" fill="#7d6a44" {o(3)}/>')
        elif v == "korobka":
            s += (f'<rect x="{vx-78:.0f}" y="{y-128:.0f}" width="156" height="128"'
                  f' rx="6" fill="#a98a5e" {o(5)}/>'
                  f'<path d="M{vx-78:.0f},{y-128:.0f} L{vx:.0f},{y-156:.0f}'
                  f' L{vx+78:.0f},{y-128:.0f}" fill="none" stroke="#8a6c44"'
                  f' stroke-width="7"/>'
                  f'<line x1="{vx:.0f}" y1="{y-128:.0f}" x2="{vx:.0f}" y2="{y-6:.0f}"'
                  f' stroke="#8a6c44" stroke-width="5" opacity=".8"/>')
        elif v == "kust":
            s += (f'<path d="M{vx-70:.0f},{y:.0f} L{vx-56:.0f},{y-110:.0f}'
                  f' L{vx+56:.0f},{y-110:.0f} L{vx+70:.0f},{y:.0f} Z" fill="#5a5c60"'
                  f' {o(5)}/>')
            for k in range(7):
                a = math.radians(-160 + k * 26)
                dl = 120 + (k % 3) * 34
                kach = 2.0 * A.w(t, 3.2 + k * .2, k * .3)
                s += (f'<line x1="{vx:.0f}" y1="{y-110:.0f}"'
                      f' x2="{vx+dl*math.cos(a)+kach:.0f}"'
                      f' y2="{y-110+dl*math.sin(a):.0f}" stroke="#4e4436"'
                      f' stroke-width="7" stroke-linecap="round"/>')
        elif v == "velik":
            s += (f'<circle cx="{vx-76:.0f}" cy="{y-70:.0f}" r="70" fill="none"'
                  f' stroke="#2f3338" stroke-width="12"/>'
                  f'<circle cx="{vx+76:.0f}" cy="{y-70:.0f}" r="70" fill="none"'
                  f' stroke="#2f3338" stroke-width="12"/>'
                  f'<path d="M{vx-76:.0f},{y-70:.0f} L{vx-10:.0f},{y-70:.0f}'
                  f' L{vx+20:.0f},{y-170:.0f} L{vx-50:.0f},{y-170:.0f} Z" fill="none"'
                  f' stroke="#8a4a4a" stroke-width="11"/>'
                  f'<path d="M{vx+76:.0f},{y-70:.0f} L{vx+20:.0f},{y-170:.0f}"'
                  f' stroke="#8a4a4a" stroke-width="11" fill="none"/>'
                  f'<path d="M{vx-50:.0f},{y-170:.0f} L{vx-66:.0f},{y-196:.0f}'
                  f' L{vx-26:.0f},{y-196:.0f}" fill="none" stroke="#2f3338"'
                  f' stroke-width="9"/>'
                  f'<rect x="{vx+2:.0f}" y="{y-198:.0f}" width="44" height="18" rx="8"'
                  f' fill="#2f3338" {o(2)}/>')
        else:
            s += (f'<ellipse cx="{vx:.0f}" cy="{y-50:.0f}" rx="60" ry="50"'
                  f' fill="#8a8c90" opacity=".8" {o(3)}/>')
        s += ten(vx, y + 6, 70, 14, .4)
    return s


def _tryumo(x, y, w_, h_, t, seed=3):
    """Старое трюмо: три зеркала в резных рамах, подзеркальник на точёных
    ножках, отражение тёплой лампы в каждом стекле."""
    s = ""
    # подзеркальник
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="46" rx="10"'
          f' fill="url(#derev)" {o(6)}/>'
          f'<rect x="{x+16:.0f}" y="{y+46:.0f}" width="{w_-32:.0f}" height="26"'
          f' fill="#3a2a1a" opacity=".8"/>')
    for px in (x + 40, x + w_ - 76):
        s += (f'<rect x="{px:.0f}" y="{y+72:.0f}" width="36" height="200" rx="12"'
              f' fill="#4a3522" {o(4)}/>'
              f'<ellipse cx="{px+18:.0f}" cy="{y+136:.0f}" rx="28" ry="18"'
              f' fill="#5e442a" {o(3)}/>')
    s += (f'<rect x="{x+90:.0f}" y="{y+120:.0f}" width="{w_-180:.0f}" height="110"'
          f' rx="8" fill="url(#dosk)" {o(4)}/>'
          f'<rect x="{x+90:.0f}" y="{y+166:.0f}" width="{w_-180:.0f}" height="12"'
          f' fill="#3a2a1a" opacity=".7"/>'
          f'<circle cx="{x+w_*.34:.0f}" cy="{y+196:.0f}" r="14" fill="{ZHELEZ}" {o(2)}/>'
          f'<circle cx="{x+w_*.66:.0f}" cy="{y+196:.0f}" r="14" fill="{ZHELEZ}" {o(2)}/>')
    # три зеркала
    for i, (mx, mw, mh) in enumerate((
            (x + 40, w_ * .26, h_ * .72), (x + w_ * .34, w_ * .32, h_),
            (x + w_ * .70, w_ * .26, h_ * .72))):
        ug = (-9, 0, 9)[i]
        s += (f'<g transform="rotate({ug} {mx+mw/2:.0f} {y:.0f})">'
              f'<path d="M{mx-14:.0f},{y:.0f} L{mx-14:.0f},{y-mh+60:.0f}'
              f' Q{mx+mw/2:.0f},{y-mh-50:.0f} {mx+mw+14:.0f},{y-mh+60:.0f}'
              f' L{mx+mw+14:.0f},{y:.0f} Z" fill="#5b4428" {o(6)}/>'
              f'<path d="M{mx:.0f},{y-8:.0f} L{mx:.0f},{y-mh+66:.0f}'
              f' Q{mx+mw/2:.0f},{y-mh-30:.0f} {mx+mw:.0f},{y-mh+66:.0f}'
              f' L{mx+mw:.0f},{y-8:.0f} Z" fill="#30404a" {o(3)}/>'
              f'<path d="M{mx+12:.0f},{y-20:.0f} L{mx+mw*.46:.0f},{y-mh+40:.0f}'
              f' L{mx+mw*.70:.0f},{y-mh+40:.0f} L{mx+mw*.30:.0f},{y-20:.0f} Z"'
              f' fill="#8fb0c4" opacity=".28"/>'
              f'<ellipse cx="{mx+mw*.5:.0f}" cy="{y-mh*.42:.0f}" rx="{mw*.22:.0f}"'
              f' ry="{mh*.14:.0f}" fill="#ffd98a"'
              f' opacity="{.22+.08*abs(A.w(t,2.4,i*.3)):.2f}"/></g>')
    return s


def _asfalt(y0, y1, seed=3, listvy=26):
    """Городской тротуар: плитка швами, бордюр, лужица, палая листва."""
    rnd = random.Random(seed)
    s = (f'<rect x="0" y="{y0:.0f}" width="{W}" height="{y1-y0:.0f}" fill="#4e4f52"/>'
         f'<rect x="0" y="{y0:.0f}" width="{W}" height="30" fill="#62646a"'
         f' opacity=".85"/>')
    ry = 0
    yy = y0 + 40
    while yy < y1:
        sh = 120 + (yy - y0) * .34
        s += (f'<line x1="0" y1="{yy:.0f}" x2="{W}" y2="{yy:.0f}" stroke="#3c3d40"'
              f' stroke-width="4" opacity=".8"/>')
        xx = -((ry % 2) * sh / 2)
        while xx < W:
            s += (f'<line x1="{xx:.0f}" y1="{yy:.0f}" x2="{xx:.0f}" y2="{yy+sh:.0f}"'
                  f' stroke="#3c3d40" stroke-width="4" opacity=".7"/>')
            xx += sh
        yy += sh
        ry += 1
    s += (f'<ellipse cx="{rnd.uniform(300,1600):.0f}" cy="{(y0+y1)/2+90:.0f}" rx="210"'
          f' ry="46" fill="#6d7f8c" opacity=".45"/>')
    s += _listya(seed + 7, listvy, y0 + 30, y1)
    return s


def _stennoe_hozyaystvo(x, y, t, seed=3):
    """Что всегда висит на стене амбара или сарая: грабли, коса, хомут,
    серп, верёвочный моток, скоба и пила. Узнаваемые силуэты в рост человека."""
    rnd = random.Random(seed)
    s = ""
    # грабли
    gx = x + 40
    kach = 1.4 * A.w(t, 4.6, .1)
    s += (f'<g transform="rotate({kach:.2f} {gx:.0f} {y+430:.0f})">'
          f'<rect x="{gx-9:.0f}" y="{y:.0f}" width="18" height="430" rx="8"'
          f' fill="url(#derev)" {o(4)}/>'
          f'<rect x="{gx-86:.0f}" y="{y:.0f}" width="172" height="22" rx="8"'
          f' fill="#5b4428" {o(4)}/>')
    for i in range(7):
        s += (f'<line x1="{gx-76+i*25:.0f}" y1="{y+20:.0f}" x2="{gx-76+i*25:.0f}"'
              f' y2="{y+66:.0f}" stroke="#4a3522" stroke-width="8"/>')
    s += "</g>"
    # коса
    kx = x + 240
    s += (f'<line x1="{kx:.0f}" y1="{y+30:.0f}" x2="{kx+40:.0f}" y2="{y+450:.0f}"'
          f' stroke="url(#derev)" stroke-width="18" stroke-linecap="round"/>'
          f'<path d="M{kx:.0f},{y+34:.0f} Q{kx-130:.0f},{y+90:.0f}'
          f' {kx-186:.0f},{y+196:.0f} Q{kx-110:.0f},{y+112:.0f} {kx-4:.0f},{y+62:.0f} Z"'
          f' fill="url(#zhel)" {o(5)}/>'
          f'<rect x="{kx+18:.0f}" y="{y+210:.0f}" width="40" height="18" rx="7"'
          f' fill="#5b4428" {o(3)}/>')
    # хомут
    hx, hy = x + 420, y + 150
    s += (f'<path d="M{hx:.0f},{hy-110:.0f} Q{hx+116:.0f},{hy-70:.0f}'
          f' {hx+106:.0f},{hy+70:.0f} Q{hx+56:.0f},{hy+170:.0f}'
          f' {hx-6:.0f},{hy+170:.0f} Q{hx-68:.0f},{hy+170:.0f}'
          f' {hx-118:.0f},{hy+70:.0f} Q{hx-128:.0f},{hy-70:.0f} {hx:.0f},{hy-110:.0f} Z"'
          f' fill="#5e442a" {o(6)}/>'
          f'<path d="M{hx:.0f},{hy-62:.0f} Q{hx+72:.0f},{hy-32:.0f}'
          f' {hx+64:.0f},{hy+62:.0f} Q{hx+32:.0f},{hy+120:.0f}'
          f' {hx-6:.0f},{hy+120:.0f} Q{hx-44:.0f},{hy+120:.0f}'
          f' {hx-76:.0f},{hy+62:.0f} Q{hx-84:.0f},{hy-32:.0f} {hx:.0f},{hy-62:.0f} Z"'
          f' fill="#2e2118" {o(4)}/>'
          f'<rect x="{hx-18:.0f}" y="{hy-128:.0f}" width="36" height="26" rx="9"'
          f' fill="{ZHELEZ}" {o(3)}/>')
    # моток верёвки
    vx, vy = x + 600, y + 120
    for i in range(4):
        s += (f'<circle cx="{vx:.0f}" cy="{vy:.0f}" r="{74-i*16:.0f}" fill="none"'
              f' stroke="#9a8a68" stroke-width="13" opacity=".9"/>')
    # серп
    sx_, sy_ = x + 760, y + 110
    s += (f'<path d="M{sx_:.0f},{sy_:.0f} Q{sx_+110:.0f},{sy_+20:.0f}'
          f' {sx_+120:.0f},{sy_+140:.0f} Q{sx_+86:.0f},{sy_+48:.0f} {sx_:.0f},{sy_+30:.0f} Z"'
          f' fill="url(#zhel)" {o(5)}/>'
          f'<rect x="{sx_-56:.0f}" y="{sy_-10:.0f}" width="60" height="26" rx="11"'
          f' fill="url(#derev)" {o(4)}/>')
    # пила
    px_, py_ = x + 880, y + 320
    s += (f'<path d="M{px_:.0f},{py_:.0f} L{px_+280:.0f},{py_+40:.0f}'
          f' L{px_+280:.0f},{py_+88:.0f} L{px_:.0f},{py_+48:.0f} Z" fill="url(#zhel)"'
          f' {o(5)}/>')
    for i in range(11):
        s += (f'<path d="M{px_+10+i*25:.0f},{py_+50+i*3.6:.0f}'
              f' L{px_+22+i*25:.0f},{py_+72+i*3.6:.0f}'
              f' L{px_+34+i*25:.0f},{py_+52+i*3.6:.0f} Z" fill="#cfd8e0" opacity=".9"/>')
    s += (f'<rect x="{px_-46:.0f}" y="{py_-10:.0f}" width="50" height="70" rx="12"'
          f' fill="url(#derev)" {o(4)}/>')
    return s


def _kadushki_i_grabli(x, y, t, seed=5):
    """Угол двора: кадушка с водой и ледком, пара вёдер, корзина с репой,
    охапка хвороста и воткнутая лопата. Ставится у ног, держит низ кадра."""
    rnd = random.Random(seed)
    s = _dvorovaya_utvar(x, y, 420, t, seed, ["kadka", "vedro", "korzina"])
    # ЛЕДОК В КАДУШКЕ — ВОДА И КОЛОТЫЕ ПЛАСТИНЫ, А НЕ БЕЛАЯ ТРУБКА. Осмотр
    # 15.11: бледный овал #9fc4da с жёсткой чертой #e4f1fa во всю ширину
    # лежал на тёмном устье кадки и читался костью, лампой-трубкой или
    # скалкой. Теперь сначала тёмная вода, потом льдины с трещиной и
    # притопленным краем, а блик разбит на короткие искры.
    s += (f'<ellipse cx="{x+54:.0f}" cy="{y-150:.0f}" rx="58" ry="18"'
          f' fill="#2b4450" {o(0)}/>'
          f'<ellipse cx="{x+54:.0f}" cy="{y-151:.0f}" rx="50" ry="14"'
          f' fill="#3d5f6b" opacity=".9"/>'
          f'<path d="M{x+10:.0f},{y-152:.0f} Q{x+32:.0f},{y-164:.0f}'
          f' {x+56:.0f},{y-157:.0f} Q{x+76:.0f},{y-150:.0f} {x+60:.0f},{y-142:.0f}'
          f' Q{x+30:.0f},{y-140:.0f} {x+10:.0f},{y-152:.0f} Z" fill="#8fb6cc"'
          f' stroke="#5c7f90" stroke-width="3"/>'
          f'<path d="M{x+62:.0f},{y-160:.0f} Q{x+84:.0f},{y-156:.0f}'
          f' {x+96:.0f},{y-148:.0f} Q{x+80:.0f},{y-142:.0f} {x+62:.0f},{y-148:.0f} Z"'
          f' fill="#a2c6d8" stroke="#5c7f90" stroke-width="3"/>'
          f'<path d="M{x+34:.0f},{y-160:.0f} L{x+46:.0f},{y-146:.0f}'
          f' L{x+40:.0f},{y-141:.0f}" fill="none" stroke="#5c7f90"'
          f' stroke-width="3" opacity=".9"/>'
          f'<path d="M{x+22:.0f},{y-156:.0f} l10,-2 M{x+68:.0f},{y-153:.0f} l9,-2'
          f' M{x+48:.0f},{y-162:.0f} l8,-1" stroke="#e8f4fb" stroke-width="4"'
          f' opacity=".75" stroke-linecap="round"/>')
    # репа в корзине
    for i in range(5):
        rx_ = x + 300 + rnd.uniform(-44, 44)
        ry_ = y - 112 + rnd.uniform(-14, 10)
        s += (f'<circle cx="{rx_:.0f}" cy="{ry_:.0f}" r="{22+rnd.uniform(0,8):.0f}"'
              f' fill="#c9b07a" {o(3)}/>'
              f'<path d="M{rx_:.0f},{ry_-24:.0f} L{rx_+8:.0f},{ry_-48:.0f}"'
              f' stroke="#6f7a44" stroke-width="5"/>')
    # охапка хвороста
    hx = x + 400
    for i in range(9):
        a = math.radians(-66 + i * 9)
        s += (f'<line x1="{hx:.0f}" y1="{y-6:.0f}" x2="{hx+170*math.cos(a):.0f}"'
              f' y2="{y-6+170*math.sin(a):.0f}" stroke="#5e472e" stroke-width="7"'
              f' stroke-linecap="round" opacity=".9"/>')
    # лопата воткнута
    lx = x - 40
    s += (f'<line x1="{lx:.0f}" y1="{y-320:.0f}" x2="{lx+16:.0f}" y2="{y-70:.0f}"'
          f' stroke="url(#derev)" stroke-width="17" stroke-linecap="round"/>'
          f'<path d="M{lx+2:.0f},{y-74:.0f} L{lx+56:.0f},{y-58:.0f}'
          f' L{lx+42:.0f},{y+8:.0f} L{lx-18:.0f},{y-4:.0f} Z" fill="url(#zhel)" {o(5)}/>'
          f'<path d="M{lx-6:.0f},{y-320:.0f} L{lx+6:.0f},{y-350:.0f}'
          f' L{lx+26:.0f},{y-320:.0f} Z" fill="#5b4428" {o(3)}/>')
    return s


def _lavka_krupno(x, y, w_, t, h_=120, spinka=False):
    """Лавка вдоль стены: толстая доска, точёные ножки, подзор, тень под ней."""
    s = (f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="38" rx="8"'
         f' fill="url(#dosk)" {o(6)}/>'
         f'<rect x="{x:.0f}" y="{y-h_+38:.0f}" width="{w_:.0f}" height="16"'
         f' fill="#3a2a1a" opacity=".75"/>')
    for i in range(2):
        px = x + 24 + i * (w_ - 86)
        s += (f'<rect x="{px:.0f}" y="{y-h_+54:.0f}" width="52" height="{h_-54:.0f}"'
              f' rx="9" fill="#4a3522" {o(4)}/>'
              f'<ellipse cx="{px+26:.0f}" cy="{y-h_+90:.0f}" rx="32" ry="16"'
              f' fill="#5e442a" {o(3)}/>')
    s += (f'<rect x="{x+70:.0f}" y="{y-h_+58:.0f}" width="{w_-140:.0f}" height="22"'
          f' rx="8" fill="#4a3522" {o(3)}/>')
    if spinka:
        s += (f'<rect x="{x+10:.0f}" y="{y-h_-150:.0f}" width="{w_-20:.0f}" height="26"'
              f' rx="9" fill="#5b4428" {o(5)}/>')
        for i in range(5):
            bx = x + 50 + i * (w_ - 120) / 4.0
            s += (f'<rect x="{bx:.0f}" y="{y-h_-150:.0f}" width="20" height="152"'
                  f' rx="7" fill="#6a5030" {o(3)}/>')
    s += ten(x + w_ / 2, y + 6, w_ * .48, 16, .45)
    return s


def _stena_ambara(x, y, w_, h_, t, vorota=True, seed=3):
    """Бревенчатая стена амбара: венцы, затёсы, скоба, ворота на полозе."""
    s = brevna(x, y, w_, h_, 94)
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="none" {o(9)}/>'
    for bx in (x - 18, x + w_ - 36):
        s += (f'<rect x="{bx:.0f}" y="{y-10:.0f}" width="54" height="{h_+20:.0f}" rx="8"'
              f' fill="#3b2a1a" {o(5)}/>')
    if vorota:
        vx, vw = x + w_ * .54, w_ * .34
        s += (f'<rect x="{vx:.0f}" y="{y+h_*.22:.0f}" width="{vw:.0f}"'
              f' height="{h_*.78:.0f}" rx="8" fill="url(#derev)" {o(6)}/>')
        for i in range(5):
            s += (f'<rect x="{vx+12+i*(vw-32)/5:.0f}" y="{y+h_*.24:.0f}"'
                  f' width="{(vw-32)/6:.0f}" height="{h_*.74:.0f}" rx="6"'
                  f' fill="#6a5030" {o(3)}/>')
        s += (f'<path d="M{vx:.0f},{y+h_*.36:.0f} L{vx+vw:.0f},{y+h_*.70:.0f}'
              f' M{vx+vw:.0f},{y+h_*.36:.0f} L{vx:.0f},{y+h_*.70:.0f}" fill="none"'
              f' stroke="#4a3522" stroke-width="16"/>'
              f'<rect x="{vx-20:.0f}" y="{y+h_*.18:.0f}" width="{vw+40:.0f}" height="26"'
              f' rx="9" fill="{ZHELEZ}" {o(4)}/>'
              f'<circle cx="{vx+vw*.5:.0f}" cy="{y+h_*.56:.0f}" r="26" fill="{ZHELEZ}"'
              f' {o(4)}/>')
    return s


def _vid_za_proemom(put, t, kind="reka", seed=5, cx0=960):
    """Нарисованный вид ЗА проёмом — чтобы без стока сцена была целой, а за
    стеклом не чернела дыра (грабли №8). Клипуется контуром самого проёма."""
    rnd = random.Random(seed)
    cid = "vid%d" % seed
    s = (f'<clipPath id="{cid}"><path d="{put}"/></clipPath>'
         f'<g clip-path="url(#{cid})">')
    if kind == "reka":
        s += (f'<rect x="0" y="0" width="{W}" height="{H}" fill="#8a97a2"/>'
              f'<rect x="0" y="0" width="{W}" height="520" fill="#9fb0bc"/>'
              f'<path d="M0,520 L{W},520 L{W},{H} L0,{H} Z" fill="url(#voda)"/>')
        for i in range(7):                                     # лесистый берег
            bx = i * 300 + rnd.uniform(-60, 60)
            s += (f'<path d="M{bx-200:.0f},522 Q{bx-60:.0f},{470-rnd.uniform(0,40):.0f}'
                  f' {bx+40:.0f},{486:.0f} Q{bx+150:.0f},{452:.0f} {bx+280:.0f},522 Z"'
                  f' fill="#4e5a4a" opacity=".9"/>')
        for i in range(14):                                    # блики на воде
            wy = 540 + i * 34
            dl = 120 + (i % 4) * 90
            wx = rnd.uniform(0, W) + 26 * A.w(t, 5.0 + i * .3, i * .2)
            s += (f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{dl:.0f}" height="7" rx="3"'
                  f' fill="#d7e6ef" opacity="{.18+.14*abs(A.w(t,3.0,i*.3)):.2f}"/>')
    elif kind == "zarya":
        s += (f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#zakat)"/>'
              f'<rect x="0" y="560" width="{W}" height="{H-560}" fill="#6e5f46"/>')
        sol = 1.0 + .08 * abs(A.w(t, 3.2, .1))
        s += (f'<circle cx="{cx0:.0f}" cy="548" r="{150*sol:.0f}" fill="#ffd79a"'
              f' opacity=".85"/>'
              f'<circle cx="{cx0:.0f}" cy="548" r="{250*sol:.0f}" fill="#ffc07a"'
              f' opacity=".3"/>')
        for i in range(9):
            fy = 570 + i * 46
            s += (f'<path d="M-40,{fy:.0f} Q480,{fy-18:.0f} 960,{fy+8:.0f}'
                  f' Q1440,{fy+26:.0f} 1960,{fy-6:.0f}" fill="none" stroke="#7d6b4c"'
                  f' stroke-width="{7+i}" opacity=".45"/>')
        for i in range(5):                                     # полосы тумана
            my = 520 + i * 58
            s += (f'<rect x="{-200+((t*8+i*280)%2400):.0f}" y="{my:.0f}" width="620"'
                  f' height="26" rx="13" fill="#e8dcc8" opacity=".38"/>')
    elif kind == "les":
        s += (f'<rect x="0" y="0" width="{W}" height="{H}" fill="#8e9a96"/>'
              f'<rect x="0" y="700" width="{W}" height="{H-700}" fill="#5c5744"/>')
        for sl, col, hh in ((0, "#6b7a6c", 300), (1, "#4e5c50", 420), (2, "#3a4740", 540)):
            for i in range(9):
                ex = i * 230 - 60 + sl * 70 + 10 * A.w(t, 6.0 + sl, i * .2)
                eb = 700 + sl * 20
                s += (f'<path d="M{ex:.0f},{eb:.0f} L{ex+70:.0f},{eb-hh:.0f}'
                      f' L{ex+140:.0f},{eb:.0f} Z" fill="{col}" opacity=".95"/>')
        for i in range(4):
            my = 560 + i * 70
            s += (f'<rect x="{-200+((t*10+i*320)%2500):.0f}" y="{my:.0f}" width="760"'
                  f' height="34" rx="17" fill="#dce4e2" opacity=".32"/>')
    elif kind == "ulica":
        s += (f'<rect x="0" y="0" width="{W}" height="{H}" fill="#1b2232"/>'
              f'<rect x="0" y="720" width="{W}" height="{H-720}" fill="#2b3240"/>')
        for i in range(10):
            dx_ = i * 210 - 40
            s += (f'<rect x="{dx_:.0f}" y="{260+(i%3)*60:.0f}" width="150"'
                  f' height="{460-(i%3)*60:.0f}" fill="#2a3champ"/>'.replace("champ", "140"))
            for k in range(5):
                if (i + k) % 2:
                    s += (f'<rect x="{dx_+18+(k%2)*70:.0f}" y="{300+(i%3)*60+k*74:.0f}"'
                          f' width="52" height="50" rx="5" fill="#ffd98a"'
                          f' opacity="{.5+.3*abs(A.w(t,4.0,i*.2+k*.1)):.2f}"/>')
        for i in range(7):
            fx_ = 110 + i * 280
            s += (f'<circle cx="{fx_:.0f}" cy="{660:.0f}" r="{40+14*abs(A.w(t,3.0,i*.3)):.0f}"'
                  f' fill="#ffe0a0" opacity=".55"/>'
                  f'<rect x="{fx_-6:.0f}" y="660" width="12" height="180" fill="#20252e"/>')
    s += "</g>"
    return s


def _moneta_krupno(cx, cy, r, t, ph=.0, med=True, profil=True, plosko=.0):
    """Монета, которую видно со стоп-кадра (R-0047): поле, гурт насечкой,
    внутренний ободок, рельефный профиль головы, венок, бегущий блик и тень.
    plosko 0..1 — насколько монета ЛЕЖИТ: кружок сплющивается в эллипс."""
    bl = .5 + .5 * A.w(t, 1.9, ph)
    col = "url(#med)" if med else "url(#zhel)"
    szh = 1.0 - .58 * plosko
    g0 = (f'<g transform="translate({cx:.0f} {cy:.0f}) scale(1 {szh:.3f})'
          f' translate({-cx:.0f} {-cy:.0f})">')
    s = ten(cx, cy + r * .72 * szh + 10, r * 1.1, r * .20, .5)
    s += g0
    s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{col}" {o(7)}/>'
          f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.88:.0f}" fill="none"'
          f' stroke="#8a5a22" stroke-width="7" opacity=".8"/>'
          f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.76:.0f}" fill="none"'
          f' stroke="#d6a358" stroke-width="5" opacity=".65"/>')
    for i in range(34):
        a = math.radians(i * 360 / 34.0)
        s += (f'<line x1="{cx+r*.9*math.cos(a):.0f}" y1="{cy+r*.9*math.sin(a):.0f}"'
              f' x2="{cx+r*1.0*math.cos(a):.0f}" y2="{cy+r*1.0*math.sin(a):.0f}"'
              f' stroke="#7a4d1c" stroke-width="5" opacity=".75"/>')
    if profil and r >= 48:
        for i in range(11):
            a = math.radians(118 + i * 124 / 10.0)
            lx, ly = cx + r * .82 * math.cos(a), cy + r * .82 * math.sin(a)
            s += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{r*.09:.0f}"'
                  f' ry="{r*.045:.0f}" transform="rotate({math.degrees(a)+90:.0f}'
                  f' {lx:.0f} {ly:.0f})" fill="#b57c33" opacity=".85"/>')
        s += (f'<path d="M{cx-r*.30:.0f},{cy+r*.56:.0f}'
              f' L{cx-r*.26:.0f},{cy+r*.08:.0f}'
              f' Q{cx-r*.30:.0f},{cy-r*.34:.0f} {cx-r*.02:.0f},{cy-r*.46:.0f}'
              f' Q{cx+r*.22:.0f},{cy-r*.52:.0f} {cx+r*.26:.0f},{cy-r*.26:.0f}'
              f' L{cx+r*.38:.0f},{cy-r*.02:.0f} L{cx+r*.24:.0f},{cy+r*.04:.0f}'
              f' L{cx+r*.26:.0f},{cy+r*.14:.0f} L{cx+r*.14:.0f},{cy+r*.18:.0f}'
              f' Q{cx+r*.20:.0f},{cy+r*.34:.0f} {cx+r*.02:.0f},{cy+r*.38:.0f}'
              f' L{cx+r*.06:.0f},{cy+r*.56:.0f} Z" fill="#a86a28" {o(4)}/>'
              f'<path d="M{cx-r*.24:.0f},{cy-r*.30:.0f}'
              f' Q{cx-r*.02:.0f},{cy-r*.46:.0f} {cx+r*.22:.0f},{cy-r*.28:.0f}"'
              f' fill="none" stroke="#d8a357" stroke-width="{max(3,r*.05):.0f}"'
              f' opacity=".85"/>'
              f'<circle cx="{cx+r*.10:.0f}" cy="{cy-r*.20:.0f}" r="{max(2,r*.045):.0f}"'
              f' fill="#6d4116"/>'
              f'<path d="M{cx+r*.10:.0f},{cy+r*.08:.0f} L{cx+r*.22:.0f},{cy+r*.08:.0f}"'
              f' stroke="#6d4116" stroke-width="{max(2,r*.035):.0f}"/>')
    elif profil:
        s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.40:.0f}" fill="#a86a28" {o(3)}/>')
    s += (f'<path d="M{cx-r*.72:.0f},{cy-r*.40:.0f} Q{cx-r*.16:.0f},{cy-r*.90:.0f}'
          f' {cx+r*.50:.0f},{cy-r*.58:.0f}" fill="none" stroke="#fff3cf"'
          f' stroke-width="{r*.15:.0f}" stroke-linecap="round" opacity="{.30+bl*.42:.2f}"/>')
    s += "</g>"
    for i in range(4):
        a = math.radians(42 + i * 76 + 40 * A.w(t, 2.6, ph + i * .2))
        rr = r * (1.16 + .16 * i)
        s += (f'<circle cx="{cx+rr*math.cos(a):.0f}"'
              f' cy="{cy+rr*math.sin(a)*szh:.0f}" r="{6+i*2}" fill="#fff0c4"'
              f' opacity="{.25+bl*.45:.2f}"/>')
    return s


def _inej(seed, n, y0, y1, col="#cfe4f5"):
    """Иней на мёрзлой земле: искры-крестики, вспыхивают по сетке."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        ix, iy = rnd.uniform(0, W), rnd.uniform(y0, y1)
        r = rnd.uniform(7, 15)
        s += (f'<line x1="{ix-r:.0f}" y1="{iy:.0f}" x2="{ix+r:.0f}" y2="{iy:.0f}"'
              f' stroke="{col}" stroke-width="3" opacity=".55"/>'
              f'<line x1="{ix:.0f}" y1="{iy-r:.0f}" x2="{ix:.0f}" y2="{iy+r:.0f}"'
              f' stroke="{col}" stroke-width="3" opacity=".55"/>')
    return s


def _podorozhnik(x, y, s_=1.0, t=0.0, ph=.0, n=5, col="#6f7a44"):
    """Куст подорожника: широкие листья розеткой и стрелка-колос."""
    s = ""
    for i in range(n):
        a = math.radians(-168 + i * (336.0 / max(1, n - 1)) + 6 * A.w(t, 3.2, ph + i * .2))
        dl = 86 * s_ * (.8 + .2 * (i % 2))
        ex, ey = x + dl * math.cos(a), y + dl * math.sin(a) * .5
        s += (f'<path d="M{x:.0f},{y:.0f} Q{(x+ex)/2:.0f},{(y+ey)/2-34*s_:.0f}'
              f' {ex:.0f},{ey:.0f} Q{(x+ex)/2:.0f},{(y+ey)/2+22*s_:.0f} {x:.0f},{y:.0f} Z"'
              f' fill="{col}" {o(3)}/>')
    s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+8*s_:.0f}" y2="{y-130*s_:.0f}"'
          f' stroke="#7f8a52" stroke-width="{5*s_:.0f}"/>'
          f'<ellipse cx="{x+8*s_:.0f}" cy="{y-142*s_:.0f}" rx="{9*s_:.0f}" ry="{26*s_:.0f}"'
          f' fill="#8a7a46" {o(2)}/>')
    return s


def _ruka(fx, fy, fh, storona, dl, ug, t, col="#2a2430", kant="#cfe4f5",
          ph=.0, amp=6.0):
    """РУКА ОТ ПЛЕЧА И ТОЛЬКО НАРУЖУ. Осмотр 15.11 глазами: рукав рисовался
    прямой палкой, рос из корпуса мимо плеча и шёл через грудь, подбородок и
    лицо («позу распятие» и «брусок через глаза» видно в кадре, числами не
    ловится). Лечение держит КОД, а не памятка:

    · точка начала берётся у `_plecho()` этой же фигуры — из корпуса рука
      вырасти не может;
    · угол задаётся в НАРУЖНОЙ системе: 0 — прямо в сторону от тела,
      +90 — вниз, -90 — вверх. Внутрь, к оси тела, повернуть нельзя: знак
      подставляет сторона плеча;
    · коридор -58°..+88°: выше рука задирается к своему лицу, ниже она
      заваливается внутрь, к подолу, и ложится на грудь.

    Отсюда и свойство, которое проверяется по координатам: конец рукава
    всегда дальше от оси тела, чем плечо, значит в прямоугольник головы и
    груди он не попадает НИ ПРИ КАКИХ числах.

    Возвращает (svg, (конец рукава), (плечо)).
    """
    px, py = _plecho(fx, fy, fh, storona)
    ug = max(-58.0, min(88.0, float(ug)))
    a = ug if storona > 0 else 180.0 - ug
    ruk, (ex, ey) = rukav(px, py, dl, a, t, col, kant, ph, amp)
    # ОПЛЕЧЬЕ. Осмотр 15.11, второй заход: `_plecho` держит точку на w*.40, а
    # верхний край одежды кончается на w*.33 — между ними 17 px пустоты, и
    # рукав толщиной 33 px висел РЯДОМ с фигурой отдельной палкой с
    # набалдашником-скруглением на конце («ни за что не держится»). Зазор
    # закрывается накладкой у плеча: она принадлежит ПЛЕЧУ, поэтому обещание
    # «конец рукава не попадает в голову и грудь» остаётся в силе.
    w_ = fh * .42
    plech = fy - fh * .66
    tol = max(14.0, dl * .19)
    opl = (f'<ellipse cx="{fx + storona * w_ * .345:.0f}"'
           f' cy="{plech + fh * .018:.0f}" rx="{w_ * .135:.0f}"'
           f' ry="{tol * .62:.0f}" fill="{col}" stroke="{K}"'
           f' stroke-width="{max(2, fh * .011):.1f}"/>'
           f'<path d="M{fx + storona * w_ * .22:.0f},{plech - fh * .004:.0f}'
           f' Q{fx + storona * w_ * .34:.0f},{plech - fh * .030:.0f}'
           f' {fx + storona * w_ * .46:.0f},{plech + fh * .010:.0f}"'
           f' fill="none" stroke="{kant}" stroke-width="{max(2, fh * .012):.1f}"'
           f' opacity=".7" stroke-linecap="round"/>')
    return opl + ruk, (ex, ey), (px, py)


def _ruka_ekr(fx, fy, fh, storona, dl, ug_ekran, t, col="#2a2430", kant="#cfe4f5",
              ph=.0, amp=6.0):
    """Тот же `_ruka`, но угол задан в ЭКРАННЫХ градусах, как у `rukav()`.

    Нужен, чтобы перевести на безопасную руку все сцены разом, не переписывая
    каждую позу числами: экранный угол сводится к наружному (для левого плеча
    это 180 - угол), а дальше работает коридор `_ruka`. Где поза и так была
    наружу, кадр не меняется ни на пиксель; где рукав шёл поперёк тела, он
    прижимается к ближайшей честной позе.
    """
    u = float(ug_ekran) if storona > 0 else 180.0 - float(ug_ekran)
    u = (u + 180.0) % 360.0 - 180.0
    return _ruka(fx, fy, fh, storona, dl, u, t, col, kant, ph, amp)


def _ruka_so_sgibom(fx, fy, fh, storona, dl1, ug1, dl2, ug2, t, col="#2a2430",
                    kant="#cfe4f5", ph=.0, amp=6.0):
    """РУКА СО СГИБОМ В ЛОКТЕ. Прямой рукав в полроста читается БРУСКОМ, даже
    когда он честно идёт от плеча и никого не пересекает (осмотр 15.11:
    «длинная прямая рука-брусок по диагонали»). Лечение — два звена: плечевая
    часть от плеча, предплечье от локтя под своим углом.

    Углы оба в НАРУЖНОЙ системе `_ruka` и оба зажаты тем же коридором, поэтому
    предплечье уходит ещё дальше от оси тела, чем локоть: в голову и грудь
    кисть не попадает так же надёжно, как у прямой руки.
    """
    ruk, (ex, ey), (px, py) = _ruka(fx, fy, fh, storona, dl1, ug1, t, col, kant,
                                    ph, amp)
    u2 = max(-58.0, min(88.0, float(ug2)))
    a2 = u2 if storona > 0 else 180.0 - u2
    pre, (kx, ky) = rukav(ex, ey, dl2, a2, t, col, kant, ph + .3, amp * .7, True)
    lok = (f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{max(9, dl1 * .11):.0f}"'
           f' fill="{col}" stroke="{K}" stroke-width="{max(2, fh * .010):.1f}"/>')
    return ruk + lok + pre, (kx, ky), (px, py)


def _predmet_naruzhu(fx, fh, ex, w_pred):
    """Сдвиг предмета, чтобы его габарит не налез на свою же фигуру.

    Предмет начинается от конца рукава; если его половина достаёт до оси
    тела — отодвигаем наружу ровно настолько, насколько не хватает.
    """
    st = 1 if ex >= fx else -1
    nado = fh * .42 * .52 + w_pred * .5
    est = abs(ex - fx)
    return st * max(.0, nado - est)


def _sledy(x0, y0, x1, y1, n=7, seed=3, col="#33281d", s_=1.0):
    """Цепочка следов валенок, уходящая в глубину: НАСТОЯЩАЯ вещь в нижней
    трети, а не полупрозрачное пятно (за пятна работу уже отклоняли).
    Каждый след — вдавленный овал с бортиком и рубчиком подошвы."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        p = i / max(1, n - 1.0)
        sx = x0 + (x1 - x0) * p + rnd.uniform(-10, 10)
        sy = y0 + (y1 - y0) * p
        k = s_ * (1.0 - .52 * p)
        bok = 34 * k * (1 if i % 2 else -1)
        rx_, ry_ = 40 * k, 20 * k
        s += (f'<ellipse cx="{sx+bok:.0f}" cy="{sy:.0f}" rx="{rx_:.0f}" ry="{ry_:.0f}"'
              f' fill="{col}" opacity=".92"/>'
              f'<ellipse cx="{sx+bok:.0f}" cy="{sy-ry_*.26:.0f}" rx="{rx_*.86:.0f}"'
              f' ry="{ry_*.72:.0f}" fill="#241b12" opacity=".85"/>')
        for j in range(3):
            s += (f'<line x1="{sx+bok-rx_*.6:.0f}" y1="{sy-ry_*.4+j*ry_*.5:.0f}"'
                  f' x2="{sx+bok+rx_*.6:.0f}" y2="{sy-ry_*.4+j*ry_*.5:.0f}"'
                  f' stroke="#6b5a44" stroke-width="{max(2,3*k):.0f}" opacity=".5"/>')
        s += (f'<path d="M{sx+bok-rx_:.0f},{sy+ry_*.2:.0f} a{rx_:.0f},{ry_:.0f} 0 0 0'
              f' {rx_*2:.0f},0" fill="none" stroke="#cfe4f5" stroke-width="{max(2,3*k):.0f}"'
              f' opacity=".45"/>')
    return s


def _luzha(cx, cy, rx, t, ph=.0, ry=None, otraz="#7e97ad"):
    """Лужа с ОТРАЖЕНИЕМ: вода, перевёрнутое небо в ней, кромка грязи и
    дрожь по поверхности. Настоящая вещь нижней трети."""
    ry = ry if ry is not None else rx * .34
    dr = 1.0 + .04 * A.w(t, 1.1, ph)
    s = (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx*1.06:.0f}" ry="{ry*1.16:.0f}"'
         f' fill="#2e2317" opacity=".9"/>'
         f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}"'
         f' fill="{otraz}" opacity=".88"/>'
         f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx*.92:.0f}" ry="{ry*.84:.0f}"'
         f' fill="#4a5f72" opacity=".55"/>')
    for i in range(3):
        yy = cy - ry * .40 + i * ry * .42
        s += (f'<ellipse cx="{cx+rx*.10*(1 if i%2 else -1):.0f}" cy="{yy:.0f}"'
              f' rx="{rx*(.72-i*.16)*dr:.0f}" ry="{ry*.13:.0f}" fill="#cfe4f5"'
              f' opacity="{.50-i*.12:.2f}"/>')
    s += (f'<ellipse cx="{cx-rx*.34:.0f}" cy="{cy-ry*.18:.0f}" rx="{rx*.20:.0f}"'
          f' ry="{ry*.26:.0f}" fill="#eaf3fb" opacity=".45"/>')
    for i in range(5):
        a = math.radians(i * 72 + 14)
        s += (f'<ellipse cx="{cx+rx*1.02*math.cos(a):.0f}" cy="{cy+ry*1.08*math.sin(a):.0f}"'
              f' rx="{rx*.13:.0f}" ry="{ry*.22:.0f}" fill="#3f3122" opacity=".8"/>')
    return s


def _iriska(cx, cy, s_=1.0, ug=0.0, col="#8a5a22", fant="#efe2c2"):
    """ИРИСКА — ПОДУШЕЧКА В ФАНТИКЕ, А НЕ МОНЕТКА. Осмотр 15.11: в окошке
    ларька и в коробке на полке конфеты были нарисованы жёлтыми кружками и
    читались мелочью. Здесь: тёмная подушечка с мягкими рёбрами, светлый
    фантик скрученными концами по сторонам и косая полоска-надрыв."""
    w_, h_ = 54 * s_, 36 * s_
    return (f'<g transform="rotate({ug:.0f} {cx:.0f} {cy:.0f})">'
            f'<path d="M{cx-w_:.0f},{cy:.0f} L{cx-w_*.56:.0f},{cy-h_*.86:.0f}'
            f' L{cx-w_*.50:.0f},{cy+h_*.10:.0f} L{cx-w_*.62:.0f},{cy+h_*.90:.0f} Z"'
            f' fill="{fant}" {o(3)}/>'
            f'<path d="M{cx+w_:.0f},{cy:.0f} L{cx+w_*.56:.0f},{cy-h_*.90:.0f}'
            f' L{cx+w_*.50:.0f},{cy+h_*.06:.0f} L{cx+w_*.62:.0f},{cy+h_*.86:.0f} Z"'
            f' fill="{fant}" {o(3)}/>'
            f'<path d="M{cx-w_*.58:.0f},{cy-h_*.72:.0f}'
            f' Q{cx:.0f},{cy-h_*.98:.0f} {cx+w_*.58:.0f},{cy-h_*.72:.0f}'
            f' Q{cx+w_*.70:.0f},{cy:.0f} {cx+w_*.58:.0f},{cy+h_*.72:.0f}'
            f' Q{cx:.0f},{cy+h_*.98:.0f} {cx-w_*.58:.0f},{cy+h_*.72:.0f}'
            f' Q{cx-w_*.70:.0f},{cy:.0f} {cx-w_*.58:.0f},{cy-h_*.72:.0f} Z"'
            f' fill="{col}" {o(4)}/>'
            f'<path d="M{cx-w_*.34:.0f},{cy-h_*.60:.0f} L{cx-w_*.06:.0f},{cy+h_*.62:.0f}"'
            f' stroke="{fant}" stroke-width="{max(3,5*s_):.0f}" opacity=".75"/>'
            f'<path d="M{cx-w_*.40:.0f},{cy-h_*.30:.0f}'
            f' Q{cx:.0f},{cy-h_*.52:.0f} {cx+w_*.40:.0f},{cy-h_*.30:.0f}" fill="none"'
            f' stroke="#c99a52" stroke-width="{max(2,4*s_):.0f}" opacity=".7"/>'
            f'<path d="M{cx-w_*.44:.0f},{cy+h_*.34:.0f}'
            f' Q{cx:.0f},{cy+h_*.56:.0f} {cx+w_*.44:.0f},{cy+h_*.34:.0f}" fill="none"'
            f' stroke="#5e3c14" stroke-width="{max(2,4*s_):.0f}" opacity=".7"/></g>')


def _kucha_listev(x, y, w_, seed=5, h_=78):
    """СГРЕБЁННАЯ куча листьев: горка с черенками, а не россыпь по всему
    кадру. Ставится у стены, у крыльца, под деревом."""
    rnd = random.Random(seed)
    cols = ("#9a5a28", "#b4762f", "#7d4a24", "#c08a3a", "#6e4420")
    s = (f'<path d="M{x-w_*.5:.0f},{y:.0f} Q{x-w_*.30:.0f},{y-h_:.0f} {x:.0f},{y-h_*.92:.0f}'
         f' Q{x+w_*.32:.0f},{y-h_*.86:.0f} {x+w_*.5:.0f},{y:.0f} Z"'
         f' fill="#6b4320" {o(5)}/>')
    for i in range(26):
        lx = x + rnd.uniform(-w_ * .50, w_ * .50)
        ly = y - rnd.uniform(0, h_ * .92) * (1 - abs(lx - x) / (w_ * .55))
        r = rnd.uniform(16, 30)
        a = rnd.uniform(-70, 70)
        s += (f'<g transform="rotate({a:.0f} {lx:.0f} {ly:.0f})">'
              f'<path d="M{lx:.0f},{ly:.0f} q{r*.8:.0f},{-r*.7:.0f} {r*1.7:.0f},0'
              f' q{-r*.8:.0f},{r*.7:.0f} {-r*1.7:.0f},0 Z"'
              f' fill="{cols[rnd.randrange(len(cols))]}" {o(3)}/>'
              f'<line x1="{lx:.0f}" y1="{ly:.0f}" x2="{lx-r*.5:.0f}" y2="{ly+r*.2:.0f}"'
              f' stroke="#4e3418" stroke-width="3"/></g>')
    return s


def _kot_zhivoy(x, y, t, s_=1.0, col="#3b3430", ph=.0, polosy=True, spit=False):
    """КОТ, КОТОРЫЙ ЧИТАЕТСЯ КОТОМ. Осмотр 15.11: тёмное пятно с двумя
    точками. Здесь — хвост трубой с кольцами, два уха с розовой изнанкой,
    четыре лапы, белая грудка и морда с усами."""
    hv = 9 * A.w(t, 2.4, ph)
    uh = 5 * A.w(t, 1.7, ph + .3)
    s = ten(x, y + 8 * s_, 86 * s_, 15 * s_, .45)
    # четыре лапы — две передние, две задние
    for dx, w2 in ((-54, 20), (-26, 18), (34, 20), (58, 18)):
        s += (f'<rect x="{x+dx*s_-w2*s_*.5:.0f}" y="{y-34*s_:.0f}" width="{w2*s_:.0f}"'
              f' height="{36*s_:.0f}" rx="{w2*s_*.45:.0f}" fill="{col}" {o(4)}/>'
              f'<ellipse cx="{x+dx*s_:.0f}" cy="{y:.0f}" rx="{w2*s_*.72:.0f}"'
              f' ry="{8*s_:.0f}" fill="#241f1c" {o(3)}/>')
    # хвост трубой
    s += (f'<g transform="rotate({hv:.1f} {x-62*s_:.0f} {y-42*s_:.0f})">'
          f'<path d="M{x-62*s_:.0f},{y-42*s_:.0f} q{-30*s_:.0f},{-46*s_:.0f}'
          f' {-6*s_:.0f},{-108*s_:.0f}" fill="none" stroke="{col}"'
          f' stroke-width="{24*s_:.0f}" stroke-linecap="round"/>')
    for i in range(3):
        s += (f'<line x1="{x-80*s_+i*4*s_:.0f}" y1="{y-78*s_-i*26*s_:.0f}"'
              f' x2="{x-56*s_+i*4*s_:.0f}" y2="{y-84*s_-i*26*s_:.0f}"'
              f' stroke="#8f857c" stroke-width="{7*s_:.0f}" opacity=".6"/>')
    s += (f'<circle cx="{x-68*s_:.0f}" cy="{y-150*s_:.0f}" r="{12*s_:.0f}"'
          f' fill="#cfc6bb" opacity=".7"/></g>')
    # корпус и белая грудка
    s += (f'<ellipse cx="{x:.0f}" cy="{y-56*s_:.0f}" rx="{82*s_:.0f}" ry="{44*s_:.0f}"'
          f' fill="{col}" {o(6)}/>')
    if polosy:
        for i in range(4):
            s += (f'<path d="M{x-46*s_+i*28*s_:.0f},{y-92*s_:.0f} q{8*s_:.0f},{30*s_:.0f}'
                  f' {2*s_:.0f},{58*s_:.0f}" fill="none" stroke="#6a6058"'
                  f' stroke-width="{9*s_:.0f}" opacity=".55"/>')
    s += (f'<ellipse cx="{x+44*s_:.0f}" cy="{y-44*s_:.0f}" rx="{26*s_:.0f}"'
          f' ry="{30*s_:.0f}" fill="#e7ded2" opacity=".85"/>')
    hx, hy = x + 62 * s_, y - 106 * s_
    for sgn in (-1, 1):                 # уши с розовой изнанкой
        s += (f'<g transform="rotate({uh*sgn:.1f} {hx:.0f} {hy:.0f})">'
              f'<path d="M{hx+sgn*26*s_:.0f},{hy-20*s_:.0f} l{sgn*8*s_:.0f},{-36*s_:.0f}'
              f' l{-sgn*34*s_:.0f},{12*s_:.0f} Z" fill="{col}" {o(4)}/>'
              f'<path d="M{hx+sgn*24*s_:.0f},{hy-24*s_:.0f} l{sgn*5*s_:.0f},{-20*s_:.0f}'
              f' l{-sgn*19*s_:.0f},{7*s_:.0f} Z" fill="#c08a8a" opacity=".8"/></g>')
    s += (f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{40*s_:.0f}" fill="{col}" {o(6)}/>'
          f'<ellipse cx="{hx+10*s_:.0f}" cy="{hy+18*s_:.0f}" rx="{24*s_:.0f}"'
          f' ry="{16*s_:.0f}" fill="#e7ded2" opacity=".8"/>')
    for dx in (-14, 16):                # глаза
        if spit or A.blink(t, 4.6, ph + .2):
            s += (f'<path d="M{hx+dx*s_-11*s_:.0f},{hy-4*s_:.0f}'
                  f' q{11*s_:.0f},{7*s_:.0f} {22*s_:.0f},0" fill="none" stroke="{K}"'
                  f' stroke-width="{max(2,4*s_):.0f}" stroke-linecap="round"/>')
        else:
            s += (f'<ellipse cx="{hx+dx*s_:.0f}" cy="{hy-4*s_:.0f}" rx="{9*s_:.0f}"'
                  f' ry="{11*s_:.0f}" fill="#d8e86a"/>'
                  f'<ellipse cx="{hx+dx*s_:.0f}" cy="{hy-4*s_:.0f}" rx="{3.2*s_:.0f}"'
                  f' ry="{10*s_:.0f}" fill="{K}"/>')
    s += (f'<path d="M{hx+6*s_:.0f},{hy+12*s_:.0f} l{8*s_:.0f},{6*s_:.0f}'
          f' l{-8*s_:.0f},{5*s_:.0f} Z" fill="#c07a74" {o(2)}/>')
    for i, dy in enumerate((-4, 4)):    # усы
        for sgn in (-1, 1):
            s += (f'<line x1="{hx+sgn*8*s_:.0f}" y1="{hy+16*s_+dy*s_:.0f}"'
                  f' x2="{hx+sgn*48*s_:.0f}" y2="{hy+10*s_+dy*2.4*s_:.0f}"'
                  f' stroke="#e7ded2" stroke-width="{3*s_:.0f}" opacity=".8"/>')
    return s


def _yaschiki(x, y, t, seed=7, n=3, s_=1.0):
    """Штабель ящиков и короб у стены: вещи в рост человека по пояс."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        w2 = (150 + rnd.uniform(-20, 28)) * s_
        h2 = (110 + rnd.uniform(-14, 22)) * s_
        bx = x + i * w2 * .96
        by = y - (h2 if i % 2 == 0 else h2 * 1.9)
        s += (f'<rect x="{bx:.0f}" y="{by:.0f}" width="{w2:.0f}" height="{h2:.0f}"'
              f' rx="7" fill="url(#derev)" {o(5)}/>')
        for j in range(3):
            s += (f'<line x1="{bx+6:.0f}" y1="{by+h2*(j+1)/4.0:.0f}"'
                  f' x2="{bx+w2-6:.0f}" y2="{by+h2*(j+1)/4.0:.0f}"'
                  f' stroke="#3c2a1a" stroke-width="4" opacity=".6"/>')
        s += (f'<rect x="{bx+w2*.18:.0f}" y="{by+h2*.22:.0f}" width="{w2*.64:.0f}"'
              f' height="{h2*.30:.0f}" rx="5" fill="#8a6a44" opacity=".5"/>')
        if i % 2 == 0:
            s += (f'<rect x="{bx:.0f}" y="{by-h2*.84:.0f}" width="{w2:.0f}"'
                  f' height="{h2*.84:.0f}" rx="7" fill="#5a4228" {o(5)}/>')
    return s
