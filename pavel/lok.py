# -*- coding: utf-8 -*-
"""96 декораций ролика «19 ноября — Павел Ледостав».

Каждая — функция времени f(t) -> svg. Все нарисованы ЗАНОВО под этот текст
(R-0019): ни один кадр не взят у «13»-«18 ноября».
Его правила 14-15.11: настоящий кадр лежит ВНУТРИ сцены (метка mesto_stoka),
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


def _plecho(x, y, h_, storona):
    """Точка плеча figura(x,y,h_,...) для rukav(): -1 левое плечо, 1 правое."""
    w_ = h_ * .42
    return x + storona * w_ * .40, y - h_ * .66 + h_ * .02


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
    # РУКА НЕ ТОРЧИТ ГОРИЗОНТАЛЬНО (осмотр контактных листов 16.11): угол около
    # нуля давал «позу распятия» — прямые руки в стороны у каждой второй
    # фигуры. Узкий коридор у горизонтали отводится вниз-вбок, а осмысленные
    # позы (рука поднята вверх, рука вдоль тела) остаются как заданы.
    if -34.0 < ug < 34.0:
        ug = 34.0 + (ug + 34.0) * .11
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


# ═══════════ ЛЁД И ВОДА — ГЛАВНЫЙ ОБРАЗ ДНЯ ═══════════════════════════════

def korka_lda(cx, cy, rx, ry, t, ph=.0, slom=.0, op=1.0, prozr=.0):
    """ПЕРВАЯ КОРКА: белёсый лёд с перьями-узорами, вмёрзшими пузырьками и
    травинками, по нему бежит блеск. slom 0..1 — пролом с осколками и тёмной
    водой в середине (день ледостава: корку ломают, и под ней вода).

    Узнаваемость (R-0047): не серый овал, а именно лёд — перья узора от
    краёв к середине, цепочки пузырьков, матовая кромка, мокрый блеск.
    """
    rnd = random.Random(int(abs(cx) + abs(cy)) % 977 + 11)
    s = (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}"'
         f' fill="url(#led)" opacity="{op*(1-prozr*.4):.2f}" stroke="#dcecf8"'
         f' stroke-width="{max(3, rx*.025):.1f}"/>')
    # перья узора: от кромки к середине, разной длины
    for i in range(13):
        a = rnd.uniform(0, 6.283)
        d = rnd.uniform(.45, .95)
        x1, y1 = cx + rx * d * math.cos(a), cy + ry * d * math.sin(a)
        x2, y2 = cx + rx * d * .30 * math.cos(a), cy + ry * d * .30 * math.sin(a)
        s += (f'<path d="M{x1:.0f},{y1:.0f} Q{(x1+x2)/2+rnd.uniform(-18,18):.0f},'
              f'{(y1+y2)/2+rnd.uniform(-10,10):.0f} {x2:.0f},{y2:.0f}" fill="none"'
              f' stroke="#f2fbff" stroke-width="{rnd.uniform(1.8,4.4):.1f}"'
              f' opacity="{rnd.uniform(.40,.80):.2f}"/>')
        for k in range(3):              # перо: короткие ости по сторонам
            p = (k + 1) / 4.0
            mx, my = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
            s += (f'<line x1="{mx:.0f}" y1="{my:.0f}" x2="{mx+rnd.uniform(-16,16):.0f}"'
                  f' y2="{my+rnd.uniform(-9,9):.0f}" stroke="#eaf6ff"'
                  f' stroke-width="1.6" opacity=".45"/>')
    # пузырьки воздуха цепочкой — верный признак молодого льда
    for i in range(9):
        bx = cx + rnd.uniform(-rx * .8, rx * .8)
        by = cy + rnd.uniform(-ry * .7, ry * .7)
        for k in range(rnd.randint(2, 4)):
            r = rnd.uniform(2.4, 6.0)
            s += (f'<circle cx="{bx+k*r*2.1:.0f}" cy="{by-k*r*.7:.0f}" r="{r:.1f}"'
                  f' fill="#ffffff" opacity=".55"/>')
    # вмёрзшие травинки и листик
    for i in range(4):
        gx = cx + rnd.uniform(-rx * .75, rx * .75)
        gy = cy + rnd.uniform(-ry * .5, ry * .6)
        s += (f'<path d="M{gx:.0f},{gy:.0f} q{rnd.uniform(16,40):.0f},{rnd.uniform(-14,6):.0f}'
              f' {rnd.uniform(34,78):.0f},{rnd.uniform(-6,12):.0f}" fill="none"'
              f' stroke="#8a7a52" stroke-width="2.6" opacity=".7"/>')
    s += (f'<path d="M{cx-rx*.42:.0f},{cy+ry*.30:.0f} q{rx*.12:.0f},{-ry*.26:.0f}'
          f' {rx*.30:.0f},{-ry*.06:.0f} q{-rx*.10:.0f},{ry*.22:.0f} {-rx*.30:.0f},{ry*.06:.0f} Z"'
          f' fill="#9a6a2e" opacity=".55"/>')
    # мокрый блеск бежит поперёк корки
    bl = (t * .5 + ph) % 1.0
    s += (f'<ellipse cx="{cx-rx*.6+rx*1.2*bl:.0f}" cy="{cy-ry*.18:.0f}"'
          f' rx="{rx*.26:.0f}" ry="{ry*.34:.0f}" fill="#ffffff"'
          f' opacity="{.16+.14*math.sin(bl*3.14):.2f}"/>')
    s += (f'<path d="M{cx-rx*.86:.0f},{cy-ry*.16:.0f} q{rx*.5:.0f},{-ry*.52:.0f}'
          f' {rx*1.5:.0f},{-ry*.10:.0f}" fill="none" stroke="#ffffff"'
          f' stroke-width="{max(2, rx*.018):.1f}" opacity=".40"/>')
    if slom > .01:
        # пролом: тёмная вода, зубчатая кромка, осколки поверх
        pr = rx * .30 * slom
        put = f'M{cx-pr:.0f},{cy:.0f}'
        for k in range(1, 9):
            a = k * .785
            rr = pr * (0.72 + 0.42 * ((k * 7) % 5) / 5.0)
            put += f' L{cx+rr*math.cos(a):.0f},{cy+rr*math.sin(a)*.62:.0f}'
        s += f'<path d="{put} Z" fill="{VODA2}" stroke="#cfe4f5" stroke-width="3"/>'
        s += (f'<path d="{put} Z" fill="none" stroke="#1b2b33" stroke-width="7"'
              f' opacity=".45"/>')
        for k in range(5):
            ox = cx + rnd.uniform(-pr * 2.1, pr * 2.1)
            oy = cy + rnd.uniform(-pr * .9, pr * 1.1)
            s += (f'<path d="M{ox:.0f},{oy:.0f} l{rnd.uniform(18,46):.0f},{rnd.uniform(-10,8):.0f}'
                  f' l{rnd.uniform(-10,14):.0f},{rnd.uniform(10,22):.0f} Z" fill="#dcecf8"'
                  f' stroke="#9fc4d8" stroke-width="2" opacity=".92"/>')
        s += treschina(cx, cy, rx * .9, 7, 6)
    return s


def treschina(cx, cy, r, seed=3, n=5, col="#ffffff", w_=4.0):
    """Трещина-звезда во льду: лучи с изломами и тонкие ответвления."""
    rnd = random.Random(seed * 31 + 7)
    s = ""
    for i in range(n):
        a = rnd.uniform(0, 6.283)
        x, y = cx, cy
        put = f'M{cx:.0f},{cy:.0f}'
        for k in range(4):
            d = r * rnd.uniform(.18, .34)
            a += rnd.uniform(-.42, .42)
            x += d * math.cos(a); y += d * math.sin(a) * .62
            put += f' L{x:.0f},{y:.0f}'
        s += (f'<path d="{put}" fill="none" stroke="{col}"'
              f' stroke-width="{w_*rnd.uniform(.6,1.0):.1f}" opacity=".80"/>')
        s += (f'<path d="{put}" fill="none" stroke="#5d7f93"'
              f' stroke-width="{w_*.45:.1f}" opacity=".45"/>')
    return s


def ledyanoe_pole(y, t, seed=5, berega=True, naled=True):
    """Пруд, схваченный первым льдом: полосы наледи, переметённый снег по
    кромке, вмёрзшие былинки, тонкая прозрачная дорожка у середины."""
    rnd = random.Random(seed * 17 + 3)
    s = (f'<rect x="0" y="{y:.0f}" width="{W}" height="{H-y:.0f}" fill="url(#led)"/>')
    s += (f'<path d="M0,{y:.0f} Q480,{y+26:.0f} 960,{y+8:.0f} T1920,{y+22:.0f}'
          f' L1920,{y+70:.0f} L0,{y+70:.0f} Z" fill="#b9d6e8" opacity=".75"/>')
    if naled:
        for i in range(11):
            yy = y + 40 + i * (H - y - 40) / 11.0 + rnd.uniform(-12, 12)
            s += (f'<path d="M{rnd.uniform(-60, 300):.0f},{yy:.0f}'
                  f' Q{rnd.uniform(500,900):.0f},{yy+rnd.uniform(-26,26):.0f}'
                  f' {rnd.uniform(1500,2000):.0f},{yy+rnd.uniform(-18,18):.0f}"'
                  f' fill="none" stroke="#dcecf8" stroke-width="{rnd.uniform(3,11):.1f}"'
                  f' opacity="{rnd.uniform(.25,.60):.2f}"/>')
    for i in range(7):                  # переметённый снег языками
        sx = rnd.uniform(-100, 1800); sy = y + rnd.uniform(60, H - y - 40)
        s += (f'<ellipse cx="{sx:.0f}" cy="{sy:.0f}" rx="{rnd.uniform(90,260):.0f}"'
              f' ry="{rnd.uniform(14,34):.0f}" fill="url(#sneg)"'
              f' opacity="{rnd.uniform(.45,.85):.2f}"/>')
    # прозрачное «окно» молодого льда, под ним видно тёмную воду
    ox, oy = rnd.uniform(620, 1180), y + (H - y) * .46
    s += (f'<ellipse cx="{ox:.0f}" cy="{oy:.0f}" rx="230" ry="62" fill="{VODA}"'
          f' opacity=".35"/>')
    s += treschina(ox, oy, 210, seed + 2, 4)
    bl = (t * .32) % 1.0
    s += (f'<ellipse cx="{-300+2500*bl:.0f}" cy="{y+(H-y)*.30:.0f}" rx="420" ry="46"'
          f' fill="#ffffff" opacity="{.10+.08*math.sin(bl*3.14):.2f}"/>')
    if berega:
        for i in range(5):
            bx = rnd.uniform(-40, 1880)
            s += kamysh(bx, y + rnd.uniform(6, 48), rnd.uniform(90, 190), t,
                        rnd.randint(3, 6), seed + i, True)
    return s


def kamysh(x, y, h_, t, n=5, seed=3, inej_=True):
    """Камыш в инее: стебли с метёлками, которые качаются врозь."""
    rnd = random.Random(seed * 13 + 5)
    s = ""
    for i in range(n):
        xx = x + rnd.uniform(-34, 34)
        hh = h_ * rnd.uniform(.7, 1.15)
        kach = 4.0 * A.w(t, rnd.uniform(2.4, 3.8), rnd.uniform(0, 1))
        s += (f'<path d="M{xx:.0f},{y:.0f} q{kach*.6:.0f},{-hh*.55:.0f}'
              f' {kach:.0f},{-hh:.0f}" fill="none" stroke="#8b7a4e"'
              f' stroke-width="{rnd.uniform(3,5.5):.1f}"/>')
        s += (f'<ellipse cx="{xx+kach:.0f}" cy="{y-hh-10:.0f}" rx="{rnd.uniform(6,10):.1f}"'
              f' ry="{rnd.uniform(18,30):.1f}" fill="#6f5f38" stroke="{K}"'
              f' stroke-width="1.6"/>')
        if inej_:
            s += (f'<ellipse cx="{xx+kach:.0f}" cy="{y-hh-16:.0f}" rx="{rnd.uniform(5,9):.1f}"'
                  f' ry="{rnd.uniform(10,18):.1f}" fill="{INEY}" opacity=".55"/>')
    return s


def mostki(x, y, w_, t, svai=True, h_=140):
    """Деревянные мостки на пруду: настил с зазорами, поперечины, сваи,
    отражение в воде и наледь на досках."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="26" rx="4"'
         f' fill="url(#dosk)" stroke="{K}" stroke-width="4"/>')
    n = max(4, int(w_ / 64))
    for i in range(n):
        dx = x + i * w_ / n
        s += (f'<rect x="{dx:.0f}" y="{y-10:.0f}" width="{w_/n-7:.0f}" height="34"'
              f' rx="3" fill="{DOSKA}" stroke="{K}" stroke-width="2.5"/>')
        s += (f'<rect x="{dx+4:.0f}" y="{y-10:.0f}" width="{w_/n-15:.0f}" height="7"'
              f' fill="{INEY}" opacity="{.35+.25*((i*7)%3)/3:.2f}"/>')
    if svai:
        for sx in (x + w_ * .12, x + w_ * .52, x + w_ * .88):
            s += (f'<rect x="{sx:.0f}" y="{y+22:.0f}" width="22" height="{h_:.0f}"'
                  f' fill="{DOSKA2}" stroke="{K}" stroke-width="3.5"/>')
            s += (f'<ellipse cx="{sx+11:.0f}" cy="{y+22+h_*.72:.0f}" rx="30" ry="9"'
                  f' fill="#dcecf8" opacity=".6"/>')
    s += (f'<rect x="{x:.0f}" y="{y+26:.0f}" width="{w_:.0f}" height="12"'
          f' fill="{K}" opacity=".35"/>')
    return s


def prorub(cx, cy, r, t, ph=.0, shuga=True):
    """Прорубь (лунка): бортик битого льда, тёмная вода, по ней ходит
    дрожь, рядом выброшенная шуга и мокрый след."""
    s = (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r*1.18:.0f}" ry="{r*.78:.0f}"'
         f' fill="#cfe4f5" opacity=".9" stroke="#eaf6ff" stroke-width="5"/>')
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r:.0f}" ry="{r*.62:.0f}"'
          f' fill="{VODA2}" stroke="#1b2b33" stroke-width="4"/>')
    for i in range(3):
        d = (t * .8 + ph + i * .33) % 1.0
        s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r*(.25+.7*d):.0f}"'
              f' ry="{r*(.15+.44*d):.0f}" fill="none" stroke="#9fd0e4"'
              f' stroke-width="2.6" opacity="{(1-d)*.55:.2f}"/>')
    s += (f'<ellipse cx="{cx-r*.26:.0f}" cy="{cy-r*.20:.0f}" rx="{r*.22:.0f}"'
          f' ry="{r*.10:.0f}" fill="#ffffff" opacity=".35"/>')
    if shuga:
        rnd = random.Random(int(abs(cx)) % 503 + 3)
        for i in range(7):
            sx = cx + rnd.uniform(-r * 1.9, r * 1.9)
            sy = cy + rnd.uniform(-r * .9, r * 1.0)
            s += (f'<path d="M{sx:.0f},{sy:.0f} l{rnd.uniform(12,30):.0f},{rnd.uniform(-8,6):.0f}'
                  f' l{rnd.uniform(-8,10):.0f},{rnd.uniform(8,18):.0f} Z" fill="#eaf6ff"'
                  f' stroke="#9fc4d8" stroke-width="2"/>')
    return s


# ═══════════ ДВОР, ПРИРОДА, ПОГОДА ════════════════════════════════════════

def goloe_derevo_ld(x, base, h_, t, seed=3, vetok=6, inej_=True, kant="#2a2b33"):
    """Голое дерево ноября: ствол с утолщением у земли, ветви вилками,
    на верхних — иней, качается медленно и неравномерно."""
    rnd = random.Random(seed * 23 + 9)
    kach = 1.6 * A.w(t, 4.4, seed * .13)
    s = (f'<g transform="rotate({kach:.2f} {x:.0f} {base:.0f})">')
    s += (f'<path d="M{x-h_*.055:.0f},{base:.0f} q{h_*.012:.0f},{-h_*.46:.0f}'
          f' {h_*.030:.0f},{-h_*.92:.0f} l{h_*.050:.0f},0 q{h_*.020:.0f},{h_*.46:.0f}'
          f' {h_*.036:.0f},{h_*.92:.0f} Z" fill="#3a3126" stroke="{K}" stroke-width="3.5"/>')
    for i in range(vetok):
        p = .35 + .62 * i / max(1, vetok - 1)
        sgn = 1 if i % 2 else -1
        y0 = base - h_ * p
        dl = h_ * rnd.uniform(.20, .40) * (1.15 - p * .5)
        ug = rnd.uniform(.5, 1.15) * sgn
        x1, y1 = x + dl * math.sin(ug), y0 - dl * math.cos(ug) * .55
        s += (f'<path d="M{x:.0f},{y0:.0f} Q{(x+x1)/2+sgn*14:.0f},{(y0+y1)/2:.0f}'
              f' {x1:.0f},{y1:.0f}" fill="none" stroke="#3a3126"'
              f' stroke-width="{max(3, h_*.016*(1.1-p)):.1f}" stroke-linecap="round"/>')
        for k in range(2):              # вилка на конце ветви
            ug2 = ug + rnd.uniform(-.55, .55)
            dl2 = dl * rnd.uniform(.30, .52)
            x2, y2 = x1 + dl2 * math.sin(ug2), y1 - dl2 * math.cos(ug2) * .5
            s += (f'<path d="M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}" fill="none"'
                  f' stroke="#453a2c" stroke-width="{max(2, h_*.008):.1f}"'
                  f' stroke-linecap="round"/>')
            if inej_:
                s += (f'<path d="M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}" fill="none"'
                      f' stroke="{INEY}" stroke-width="{max(2, h_*.004):.1f}" opacity=".6"/>')
    s += (f'<path d="M{x-h_*.10:.0f},{base+4:.0f} q{h_*.10:.0f},{-h_*.03:.0f}'
          f' {h_*.20:.0f},0" fill="none" stroke="{kant}" stroke-width="4" opacity=".5"/>')
    return s + '</g>'


def kalina_grozd(x, y, t, s_=1.0, n=13, seed=4, ph=.0, inej_=True):
    """Гроздь калины: алые прозрачные ягоды гнездом, черешки веером, на
    ягодах иней и блик. Качается от веса."""
    rnd = random.Random(seed * 29 + 13)
    kach = 3.2 * A.w(t, 2.6, ph)
    s = (f'<g transform="rotate({kach:.1f} {x:.0f} {y-60*s_:.0f})">')
    s += (f'<path d="M{x:.0f},{y-70*s_:.0f} q{6*s_:.0f},{26*s_:.0f} {2*s_:.0f},{44*s_:.0f}"'
          f' fill="none" stroke="#5e4a2a" stroke-width="{4*s_:.1f}"/>')
    for i in range(n):
        a = rnd.uniform(0, 6.283)
        d = rnd.uniform(.2, 1.0)
        bx = x + 42 * s_ * d * math.cos(a)
        by = y + 30 * s_ * d * math.sin(a)
        r = rnd.uniform(9, 14) * s_
        s += (f'<line x1="{x:.0f}" y1="{y-26*s_:.0f}" x2="{bx:.0f}" y2="{by:.0f}"'
              f' stroke="#6b5230" stroke-width="{2.0*s_:.1f}" opacity=".8"/>')
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r:.1f}" fill="#c8301f"'
              f' stroke="#7d1b11" stroke-width="{1.8*s_:.1f}"/>')
        s += (f'<circle cx="{bx-r*.32:.0f}" cy="{by-r*.34:.0f}" r="{r*.30:.1f}"'
              f' fill="#ffd9c8" opacity=".8"/>')
        if inej_ and i % 3 == 0:
            s += (f'<path d="M{bx-r:.0f},{by+r*.3:.0f} q{r:.0f},{r*.5:.0f} {r*2:.0f},0"'
                  f' fill="none" stroke="{INEY}" stroke-width="{2.2*s_:.1f}" opacity=".7"/>')
    return s + '</g>'


def inej_mel(seed, n, y0, y1, x0=0, x1=W, col=INEY):
    """Иней крупинками и звёздочками по земле и предметам."""
    rnd = random.Random(seed * 37 + 11)
    s = ""
    for i in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        r = rnd.uniform(1.6, 4.2)
        if i % 4:
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{col}" opacity="{rnd.uniform(.4,.9):.2f}"/>'
        else:
            s += (f'<path d="M{x-r*2:.0f},{y:.0f} h{r*4:.0f} M{x:.0f},{y-r*2:.0f} v{r*4:.0f}"'
                  f' stroke="{col}" stroke-width="1.6" opacity=".7"/>')
    return s


def sledy_valenok(x0, y0, x1, y1, n=7, seed=3, col="#2f2a22", s_=1.0, obryv=.0):
    """Цепочка следов валенок в глубину: пара вразнос, дальние мельче.
    obryv>0 — следы ОБРЫВАЮТСЯ на этой доле пути (тонкий лёд, R-записка:
    беды в кадре нет, обрывается только след)."""
    rnd = random.Random(seed * 41 + 7)
    s = ""
    for i in range(n):
        p = i / max(1, n - 1)
        if obryv > .01 and p > obryv:
            break
        x = x0 + (x1 - x0) * p + (26 if i % 2 else -26) * s_ * (1 - p * .6)
        y = y0 + (y1 - y0) * p
        w_ = 44 * s_ * (1 - p * .55)
        h_ = 24 * s_ * (1 - p * .55)
        s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_:.1f}" ry="{h_:.1f}"'
              f' fill="{col}" opacity="{.75-.3*p:.2f}"/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.5:.0f}" rx="{w_*.72:.1f}"'
              f' ry="{h_*.5:.1f}" fill="{col}" opacity="{.55-.2*p:.2f}"/>')
        s += (f'<path d="M{x-w_:.0f},{y+h_*.6:.0f} q{w_:.0f},{h_*.4:.0f} {w_*2:.0f},0"'
              f' fill="none" stroke="#f2fbff" stroke-width="2" opacity=".35"/>')
    if obryv > .01:                      # у обрыва — потревоженный снег
        px = x0 + (x1 - x0) * obryv; py = y0 + (y1 - y0) * obryv
        s += (f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{64*s_:.0f}" ry="{26*s_:.0f}"'
              f' fill="#cfe4f5" opacity=".5"/>')
        for k in range(4):
            s += (f'<path d="M{px+rnd.uniform(-50,50):.0f},{py+rnd.uniform(-16,16):.0f}'
                  f' l{rnd.uniform(14,30):.0f},{rnd.uniform(-10,8):.0f}" stroke="#ffffff"'
                  f' stroke-width="2.4" opacity=".6" fill="none"/>')
    return s


def para_izo_rta(x, y, t, ph=.0, s_=1.0, op=.5, n=4):
    """Пар изо рта — живой огонёк уличной сцены: облачка уходят вбок и тают."""
    s = ""
    for i in range(n):
        d = ((t * .55 + ph + i / n) % 1.0)
        s += (f'<ellipse cx="{x + 60*s_*d:.0f}" cy="{y - 34*s_*d - 6*i:.0f}"'
              f' rx="{(13 + 26*d)*s_:.0f}" ry="{(9 + 17*d)*s_:.0f}" fill="#e8f2fb"'
              f' opacity="{op*(1-d)*.9:.2f}"/>')
    return s


def dym_stolbom(x, y, t, h_=340, op=.5, wide=.42, n=7, col="#d7dee6"):
    """Дым СТОЛБОМ (примета дня): идёт почти вертикально, лишь чуть ведёт в
    сторону — не стелется."""
    s = ""
    for i in range(n):
        d = ((t * .22 + i / n) % 1.0)
        yy = y - h_ * d
        rx = (16 + 30 * d) * wide * 2.0
        s += (f'<ellipse cx="{x + 16*math.sin(d*2.6 + i):.0f}" cy="{yy:.0f}"'
              f' rx="{rx:.0f}" ry="{rx*.82:.0f}" fill="{col}"'
              f' opacity="{op*(1-d*.85):.2f}"/>')
    s += (f'<rect x="{x-8:.0f}" y="{y-14:.0f}" width="16" height="22" fill="{col}"'
          f' opacity="{op*.5:.2f}"/>')
    return s


def luna_v_gorode(x, y, t, s_=1.0, galo=True):
    """Луна с гало и кольцом — ночное небо ледостава."""
    s = ""
    if galo:
        for i, (r, o) in enumerate(((3.6, .10), (2.4, .14), (1.7, .20))):
            s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{52*s_*r:.0f}" fill="#cfe0f5"'
                  f' opacity="{o + .03*A.w(t, 5.0, i*.3):.2f}"/>')
    s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{52*s_:.0f}" fill="#f4f7ff"'
          f' stroke="#dde7f4" stroke-width="3"/>')
    for cx_, cy_, r in ((-16, -10, 13), (14, 8, 9), (-4, 18, 7), (20, -16, 6)):
        s += (f'<circle cx="{x+cx_*s_:.0f}" cy="{y+cy_*s_:.0f}" r="{r*s_:.0f}"'
              f' fill="#dfe6f2" opacity=".75"/>')
    return s


def zabor_shtaket(x, y, w_, h_, seed=5, step=58, col="url(#derev)", sneg=True):
    """Штакетник: планки врозь по высоте, две прожилины, снеговые шапки."""
    rnd = random.Random(seed * 43 + 5)
    s = ""
    n = max(3, int(w_ / step))
    for i in range(n):
        px = x + i * w_ / n
        hh = h_ * rnd.uniform(.88, 1.06)
        s += (f'<rect x="{px:.0f}" y="{y + h_ - hh:.0f}" width="{step*.62:.0f}"'
              f' height="{hh:.0f}" rx="4" fill="{col}" stroke="{K}" stroke-width="3"/>')
        s += (f'<path d="M{px:.0f},{y+h_-hh:.0f} l{step*.31:.0f},{-14:.0f}'
              f' l{step*.31:.0f},{14:.0f} Z" fill="{DOSKA2}" stroke="{K}" stroke-width="2.5"/>')
        if sneg:
            s += (f'<path d="M{px-2:.0f},{y+h_-hh-10:.0f} q{step*.33:.0f},{-12:.0f}'
                  f' {step*.66:.0f},0 l0,8 q{-step*.33:.0f},{8:.0f} {-step*.66:.0f},0 Z"'
                  f' fill="url(#sneg)" opacity=".9"/>')
    for k in (.28, .74):
        s += (f'<rect x="{x:.0f}" y="{y + h_*k:.0f}" width="{w_:.0f}" height="14"'
              f' fill="{DOSKA2}" stroke="{K}" stroke-width="2.5" opacity=".95"/>')
    return s


def kalitka_rez(x, y, w_, h_, t, otkr=.0, sneg=True):
    """Калитка деревенского двора: резной верх, доски, кольцо-ручка, петли.
    otkr 0..1 — приоткрыта (поворот на петлях)."""
    ug = -26 * otkr
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y+h_:.0f})">'
         f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6"'
         f' fill="url(#derev)" stroke="{K}" stroke-width="5"/>')
    n = max(3, int(w_ / 58))
    for i in range(n):
        dx = x + 8 + i * (w_ - 16) / n
        s += (f'<rect x="{dx:.0f}" y="{y+10:.0f}" width="{(w_-16)/n-8:.0f}"'
              f' height="{h_-20:.0f}" rx="4" fill="{DOSKA}" opacity=".85"'
              f' stroke="{K}" stroke-width="2"/>')
    s += (f'<path d="M{x+6:.0f},{y+h_*.30:.0f} L{x+w_-6:.0f},{y+h_*.62:.0f}"'
          f' stroke="{DOSKA2}" stroke-width="16" fill="none"/>')
    for i in range(max(3, int(w_ / 46))):   # резной гребень
        gx = x + 6 + i * (w_ - 12) / max(3, int(w_ / 46))
        s += (f'<path d="M{gx:.0f},{y:.0f} q{11:.0f},{-26:.0f} {22:.0f},0 Z"'
              f' fill="{DOSKA2}" stroke="{K}" stroke-width="2"/>')
    s += (f'<circle cx="{x+w_-34:.0f}" cy="{y+h_*.52:.0f}" r="15" fill="none"'
          f' stroke="{ZHELEZ}" stroke-width="7"/>')
    for py in (y + h_ * .18, y + h_ * .80):
        s += (f'<rect x="{x-10:.0f}" y="{py:.0f}" width="34" height="13" rx="3"'
              f' fill="{CHUGUN}" stroke="{K}" stroke-width="2"/>')
    if sneg:
        s += (f'<path d="M{x-4:.0f},{y-6:.0f} q{w_*.5:.0f},{-16:.0f} {w_+8:.0f},0'
              f' l0,9 q{-w_*.5:.0f},{10:.0f} {-w_-8:.0f},0 Z" fill="url(#sneg)"/>')
    s += '</g>'
    for bx in (x - 26, x + w_ + 6):     # столбы калитки
        s += (f'<rect x="{bx:.0f}" y="{y-28:.0f}" width="26" height="{h_+58:.0f}"'
              f' rx="4" fill="{DOSKA2}" stroke="{K}" stroke-width="4"/>')
        s += (f'<path d="M{bx-8:.0f},{y-28:.0f} l{21:.0f},{-24:.0f} l{21:.0f},{24:.0f} Z"'
              f' fill="{DOSKA}" stroke="{K}" stroke-width="3"/>')
    return s


def dvorovye_veschi(x, y, w_, t, seed=9, nabor=None):
    """Обжитой двор: ведро с наледью, кадка, корыто, грабли, метла, чурбак.
    Набор и расстановка РАЗНЫЕ по seed — одинаковый двор в шести сценах
    читается как один и тот же кадр."""
    rnd = random.Random(seed * 47 + 3)
    vse = ["vedro", "kadka", "koryto", "grabli", "metla", "churbak", "korzina"]
    nab = nabor or rnd.sample(vse, rnd.randint(3, 5))
    s = ""
    for i, v in enumerate(nab):
        px = x + (i + .5) * w_ / len(nab) + rnd.uniform(-18, 18)
        if v == "vedro":
            s += (f'<path d="M{px-30:.0f},{y-66:.0f} h60 l-7,66 h-46 Z" fill="{ZHELEZ}"'
                  f' stroke="{K}" stroke-width="3.5"/>'
                  f'<ellipse cx="{px:.0f}" cy="{y-66:.0f}" rx="30" ry="9" fill="#8f979f"'
                  f' stroke="{K}" stroke-width="3"/>'
                  f'<ellipse cx="{px:.0f}" cy="{y-62:.0f}" rx="24" ry="6" fill="{INEY}"'
                  f' opacity=".8"/>'
                  f'<path d="M{px-30:.0f},{y-70:.0f} q{30:.0f},{-34:.0f} {60:.0f},0"'
                  f' fill="none" stroke="{CHUGUN}" stroke-width="4"/>')
        elif v == "kadka":
            s += (f'<path d="M{px-38:.0f},{y-84:.0f} h76 l-6,84 h-64 Z" fill="url(#derev)"'
                  f' stroke="{K}" stroke-width="4"/>')
            for k in (.22, .70):
                s += (f'<rect x="{px-37:.0f}" y="{y-84+84*k:.0f}" width="74" height="9"'
                      f' fill="{ZHELEZ}" opacity=".9"/>')
            s += (f'<ellipse cx="{px:.0f}" cy="{y-84:.0f}" rx="38" ry="11" fill="#8a6342"'
                  f' stroke="{K}" stroke-width="3"/>')
        elif v == "koryto":
            s += (f'<path d="M{px-62:.0f},{y-40:.0f} q{62:.0f},{30:.0f} {124:.0f},0'
                  f' l-12,34 q{-50:.0f},{16:.0f} {-100:.0f},0 Z" fill="url(#derev)"'
                  f' stroke="{K}" stroke-width="4"/>'
                  f'<path d="M{px-52:.0f},{y-32:.0f} q{52:.0f},{22:.0f} {104:.0f},0"'
                  f' fill="none" stroke="{INEY}" stroke-width="7" opacity=".55"/>')
        elif v == "grabli":
            s += (f'<path d="M{px:.0f},{y:.0f} L{px+16:.0f},{y-170:.0f}" stroke="#7d5636"'
                  f' stroke-width="9" fill="none"/>'
                  f'<rect x="{px+2:.0f}" y="{y-186:.0f}" width="62" height="12"'
                  f' fill="#6b4428" stroke="{K}" stroke-width="2.5"/>')
            for k in range(5):
                s += (f'<line x1="{px+8+k*13:.0f}" y1="{y-174:.0f}" x2="{px+8+k*13:.0f}"'
                      f' y2="{y-152:.0f}" stroke="#6b4428" stroke-width="5"/>')
        elif v == "metla":
            s += (f'<path d="M{px:.0f},{y:.0f} L{px-14:.0f},{y-180:.0f}" stroke="#8a6342"'
                  f' stroke-width="10" fill="none"/>')
            for k in range(9):
                s += (f'<path d="M{px-2:.0f},{y-36:.0f} l{-22+k*5.5:.0f},{34:.0f}"'
                      f' stroke="#9a7c45" stroke-width="3.4" fill="none" opacity=".9"/>')
            s += (f'<rect x="{px-12:.0f}" y="{y-48:.0f}" width="22" height="12" rx="3"'
                  f' fill="{MED}" stroke="{K}" stroke-width="2"/>')
        elif v == "churbak":
            s += (f'<rect x="{px-34:.0f}" y="{y-56:.0f}" width="68" height="56" rx="6"'
                  f' fill="#7d5636" stroke="{K}" stroke-width="3.5"/>'
                  f'<ellipse cx="{px:.0f}" cy="{y-56:.0f}" rx="34" ry="11" fill="#a37b4e"'
                  f' stroke="{K}" stroke-width="3"/>')
            for r in (8, 16, 24):
                s += (f'<ellipse cx="{px:.0f}" cy="{y-56:.0f}" rx="{r:.0f}" ry="{r*.33:.0f}"'
                      f' fill="none" stroke="#8a6342" stroke-width="2"/>')
        else:
            s += (f'<path d="M{px-34:.0f},{y-54:.0f} q{34:.0f},{14:.0f} {68:.0f},0'
                  f' l-8,54 h-52 Z" fill="#b08a52" stroke="{K}" stroke-width="3.5"/>')
            for k in range(4):
                s += (f'<path d="M{px-30+k*3:.0f},{y-44+k*12:.0f} q{30-k*2:.0f},{9:.0f}'
                      f' {60-k*6:.0f},0" fill="none" stroke="#8a6a3a" stroke-width="2.6"/>')
        s += ten(px, y + 4, 42, 11, .4)
    return s


# ═══════════ ПРЕДМЕТЫ ДНЯ: МОЛОКО, СНАСТИ, КОНЬКИ, ЧАЙ ════════════════════

def varezhka(x, y, s_=1.0, ug=0.0, col=TKAN, t=0.0, ph=.0, uzor=True):
    """ВАРЕЖКА — вместо кисти (кистей с пальцами в ролике нет вовсе).
    Овал ладони, клин большого пальца, резинка с узором."""
    kach = 3.0 * A.w(t, 1.6, ph)
    s = (f'<g transform="rotate({ug+kach:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x-26*s_:.0f},{y-20*s_:.0f} q{26*s_:.0f},{-26*s_:.0f}'
         f' {52*s_:.0f},0 q{10*s_:.0f},{34*s_:.0f} {-6*s_:.0f},{54*s_:.0f}'
         f' q{-24*s_:.0f},{10*s_:.0f} {-46*s_:.0f},0 Z" fill="{col}"'
         f' stroke="{K}" stroke-width="{3.2*s_:.1f}"/>')
    s += (f'<path d="M{x-24*s_:.0f},{y+4*s_:.0f} q{-18*s_:.0f},{6*s_:.0f}'
          f' {-14*s_:.0f},{26*s_:.0f} q{12*s_:.0f},{6*s_:.0f} {18*s_:.0f},{-8*s_:.0f} Z"'
          f' fill="{col}" stroke="{K}" stroke-width="{3.0*s_:.1f}"/>')
    s += (f'<rect x="{x-26*s_:.0f}" y="{y+30*s_:.0f}" width="{52*s_:.0f}"'
          f' height="{16*s_:.0f}" rx="{5*s_:.0f}" fill="{RUSH}" stroke="{K}"'
          f' stroke-width="{2.4*s_:.1f}"/>')
    if uzor:
        for i in range(3):
            s += (f'<path d="M{x-18*s_+i*16*s_:.0f},{y-8*s_:.0f} l{6*s_:.0f},{8*s_:.0f}'
                  f' l{-6*s_:.0f},{8*s_:.0f}" fill="none" stroke="{RUSH}"'
                  f' stroke-width="{2.6*s_:.1f}" opacity=".85"/>')
    return s + '</g>'


def krynka_moloka(x, y, s_=1.0, t=0.0, rushnik=False, polnaya=True, ph=.0):
    """Крынка (глиняный горшок с узким горлом): пузатый бок, венчик, блик,
    молоко в горле качается, на боку потёк."""
    s = (f'<path d="M{x-46*s_:.0f},{y-96*s_:.0f} q{-16*s_:.0f},{54*s_:.0f}'
         f' {6*s_:.0f},{80*s_:.0f} q{40*s_:.0f},{22*s_:.0f} {80*s_:.0f},0'
         f' q{22*s_:.0f},{-26*s_:.0f} {6*s_:.0f},{-80*s_:.0f} Z"'
         f' fill="url(#glina)" stroke="{K}" stroke-width="{4*s_:.1f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-96*s_:.0f}" rx="{46*s_:.0f}" ry="{13*s_:.0f}"'
          f' fill="#8a5a3a" stroke="{K}" stroke-width="{3.4*s_:.1f}"/>')
    if polnaya:
        dr = 2.2 * s_ * A.w(t, 1.3, ph)
        s += (f'<ellipse cx="{x:.0f}" cy="{y-94*s_+dr:.0f}" rx="{36*s_:.0f}"'
              f' ry="{9*s_:.0f}" fill="#f6f1e6" stroke="#dcd3c2"'
              f' stroke-width="{2*s_:.1f}"/>')
        s += (f'<path d="M{x+30*s_:.0f},{y-92*s_:.0f} q{8*s_:.0f},{26*s_:.0f}'
              f' {2*s_:.0f},{42*s_:.0f}" fill="none" stroke="#f6f1e6"'
              f' stroke-width="{6*s_:.1f}" opacity=".85"/>')
    s += (f'<path d="M{x-30*s_:.0f},{y-64*s_:.0f} q{-8*s_:.0f},{30*s_:.0f}'
          f' {4*s_:.0f},{54*s_:.0f}" fill="none" stroke="#ffe9c8"'
          f' stroke-width="{7*s_:.1f}" opacity=".45"/>')
    if rushnik:
        s += (f'<path d="M{x-50*s_:.0f},{y-104*s_:.0f} q{50*s_:.0f},{-16*s_:.0f}'
              f' {100*s_:.0f},0 l{-6*s_:.0f},{26*s_:.0f} q{-44*s_:.0f},{14*s_:.0f}'
              f' {-88*s_:.0f},0 Z" fill="{RUSH}" stroke="{K}" stroke-width="{3*s_:.1f}"/>')
        for i in range(3):
            s += (f'<path d="M{x-40*s_+i*28*s_:.0f},{y-96*s_:.0f} l{7*s_:.0f},{9*s_:.0f}'
                  f' l{-7*s_:.0f},{9*s_:.0f}" fill="none" stroke="{TKAN}"'
                  f' stroke-width="{2.6*s_:.1f}"/>')
    s += ten(x, y + 6 * s_, 52 * s_, 13 * s_, .45)
    return s


def podoynik(x, y, s_=1.0, t=0.0, polnyy=True, ph=.0):
    """Подойник: расширяющееся кверху ведёрко с дужкой и носиком, молоко с
    пенкой у края, капля на носике."""
    s = (f'<path d="M{x-54*s_:.0f},{y-110*s_:.0f} h{108*s_:.0f} l{-14*s_:.0f},{110*s_:.0f}'
         f' h{-80*s_:.0f} Z" fill="#aeb6bd" stroke="{K}" stroke-width="{4*s_:.1f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-110*s_:.0f}" rx="{54*s_:.0f}" ry="{15*s_:.0f}"'
          f' fill="#c3cbd2" stroke="{K}" stroke-width="{3.6*s_:.1f}"/>')
    if polnyy:
        dr = 2.6 * s_ * A.w(t, 1.1, ph)
        s += (f'<ellipse cx="{x:.0f}" cy="{y-106*s_+dr:.0f}" rx="{45*s_:.0f}"'
              f' ry="{12*s_:.0f}" fill="#faf6ec"/>')
        for i in range(6):              # пенка пузырьками
            s += (f'<circle cx="{x-30*s_+i*12*s_:.0f}" cy="{y-108*s_+dr+((i*5)%7-3)*s_:.0f}"'
                  f' r="{(3.4+((i*3)%4))*s_:.1f}" fill="#ffffff" opacity=".8"/>')
    s += (f'<path d="M{x+46*s_:.0f},{y-108*s_:.0f} l{22*s_:.0f},{6*s_:.0f}'
          f' l{-16*s_:.0f},{14*s_:.0f} Z" fill="#c3cbd2" stroke="{K}"'
          f' stroke-width="{3*s_:.1f}"/>')
    kap = (t * .8 + ph) % 1.0
    s += (f'<ellipse cx="{x+64*s_:.0f}" cy="{y-92*s_+30*s_*kap:.0f}" rx="{5*s_:.1f}"'
          f' ry="{7*s_:.1f}" fill="#faf6ec" opacity="{1-kap:.2f}"/>')
    s += (f'<path d="M{x-54*s_:.0f},{y-114*s_:.0f} q{54*s_:.0f},{-56*s_:.0f}'
          f' {108*s_:.0f},0" fill="none" stroke="{CHUGUN}" stroke-width="{5*s_:.1f}"/>')
    s += (f'<path d="M{x-40*s_:.0f},{y-86*s_:.0f} q{-6*s_:.0f},{40*s_:.0f}'
          f' {2*s_:.0f},{74*s_:.0f}" fill="none" stroke="#eef3f8"'
          f' stroke-width="{8*s_:.1f}" opacity=".5"/>')
    s += ten(x, y + 5 * s_, 58 * s_, 14 * s_, .45)
    return s


def bidon_moloka(x, y, s_=1.0, t=0.0, ph=.0):
    """Молочный бидон: конус с хомутом, крышка с ушками, скоба-ручка."""
    s = (f'<path d="M{x-48*s_:.0f},{y:.0f} h{96*s_:.0f} l{-10*s_:.0f},{-96*s_:.0f}'
         f' q{-38*s_:.0f},{-14*s_:.0f} {-76*s_:.0f},0 Z" fill="#9aa3a8"'
         f' stroke="{K}" stroke-width="{4*s_:.1f}"/>')
    s += (f'<rect x="{x-40*s_:.0f}" y="{y-112*s_:.0f}" width="{80*s_:.0f}"'
          f' height="{22*s_:.0f}" rx="{5*s_:.0f}" fill="#b6bec4" stroke="{K}"'
          f' stroke-width="{3.4*s_:.1f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-114*s_:.0f}" rx="{40*s_:.0f}"'
          f' ry="{11*s_:.0f}" fill="#cfd6db" stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*34*s_:.0f},{y-112*s_:.0f} q{i*20*s_:.0f},{-14*s_:.0f}'
              f' {i*4*s_:.0f},{-26*s_:.0f}" fill="none" stroke="{CHUGUN}"'
              f' stroke-width="{5*s_:.1f}"/>')
    s += (f'<rect x="{x-48*s_:.0f}" y="{y-54*s_:.0f}" width="{96*s_:.0f}"'
          f' height="{10*s_:.0f}" fill="#808a90" opacity=".9"/>')
    s += (f'<path d="M{x-34*s_:.0f},{y-88*s_:.0f} q{-6*s_:.0f},{38*s_:.0f}'
          f' {2*s_:.0f},{64*s_:.0f}" fill="none" stroke="#eef3f8"'
          f' stroke-width="{9*s_:.1f}" opacity=".45"/>')
    s += (f'<ellipse cx="{x+8*s_:.0f}" cy="{y-118*s_:.0f}" rx="{10*s_:.0f}"'
          f' ry="{4*s_:.0f}" fill="{INEY}" opacity="{.4+.2*A.w(t,2.2,ph):.2f}"/>')
    s += ten(x, y + 5 * s_, 54 * s_, 14 * s_, .45)
    return s


def banka_moloka(x, y, s_=1.0, t=0.0, kryshka=True, uroven=.78, soderzh="#faf6ec"):
    """Стеклянная банка: плечики, резьба, содержимое до уровня, блик."""
    hh = 130 * s_
    s = (f'<path d="M{x-40*s_:.0f},{y-hh+26*s_:.0f} q0,{-22*s_:.0f} {14*s_:.0f},{-26*s_:.0f}'
         f' h{52*s_:.0f} q{14*s_:.0f},{4*s_:.0f} {14*s_:.0f},{26*s_:.0f}'
         f' l0,{hh-26*s_:.0f} q{-40*s_:.0f},{14*s_:.0f} {-80*s_:.0f},0 Z"'
         f' fill="{STEKLO}" opacity=".55" stroke="{K}" stroke-width="{3.6*s_:.1f}"/>')
    s += (f'<path d="M{x-38*s_:.0f},{y-hh*uroven+26*s_:.0f} l0,{hh*uroven-26*s_:.0f}'
          f' q{38*s_:.0f},{13*s_:.0f} {76*s_:.0f},0 l0,{-hh*uroven+26*s_:.0f}'
          f' q{-38*s_:.0f},{10*s_:.0f} {-76*s_:.0f},0 Z" fill="{soderzh}" opacity=".95"/>')
    if kryshka:
        s += (f'<rect x="{x-30*s_:.0f}" y="{y-hh-4*s_:.0f}" width="{60*s_:.0f}"'
              f' height="{18*s_:.0f}" rx="{4*s_:.0f}" fill="#c9ccd1" stroke="{K}"'
              f' stroke-width="{3*s_:.1f}"/>')
        for i in range(4):
            s += (f'<line x1="{x-24*s_+i*16*s_:.0f}" y1="{y-hh-2*s_:.0f}"'
                  f' x2="{x-24*s_+i*16*s_:.0f}" y2="{y-hh+12*s_:.0f}" stroke="#9aa0a6"'
                  f' stroke-width="{2.2*s_:.1f}"/>')
    s += (f'<path d="M{x-28*s_:.0f},{y-hh+44*s_:.0f} q{-6*s_:.0f},{46*s_:.0f}'
          f' {2*s_:.0f},{76*s_:.0f}" fill="none" stroke="#ffffff"'
          f' stroke-width="{8*s_:.1f}" opacity=".5"/>')
    s += ten(x, y + 5 * s_, 44 * s_, 12 * s_, .4)
    return s


def paket_treugolnyy(x, y, s_=1.0, ug=0.0, col="#eef2f6"):
    """Треугольный пакет молока (без названий и марок — его правило):
    тетраэдр со швами и синей полосой по ребру."""
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x-54*s_:.0f},{y:.0f} L{x+54*s_:.0f},{y:.0f}'
         f' L{x+6*s_:.0f},{y-96*s_:.0f} Z" fill="{col}" stroke="{K}"'
         f' stroke-width="{3.6*s_:.1f}"/>')
    s += (f'<path d="M{x-54*s_:.0f},{y:.0f} L{x+6*s_:.0f},{y-96*s_:.0f}'
          f' L{x+12*s_:.0f},{y-18*s_:.0f} Z" fill="#dde4ea" stroke="{K}"'
          f' stroke-width="{2.6*s_:.1f}"/>')
    s += (f'<path d="M{x-54*s_:.0f},{y:.0f} L{x+54*s_:.0f},{y:.0f}" stroke="#7fa3c4"'
          f' stroke-width="{7*s_:.1f}" opacity=".85"/>')
    s += (f'<path d="M{x-14*s_:.0f},{y-56*s_:.0f} q{16*s_:.0f},{-8*s_:.0f}'
          f' {26*s_:.0f},{4*s_:.0f}" fill="none" stroke="#7fa3c4"'
          f' stroke-width="{4*s_:.1f}" opacity=".7"/>')
    s += '</g>' + ten(x, y + 5 * s_, 52 * s_, 12 * s_, .4)
    return s


def kruzhka_moloka(x, y, s_=1.0, t=0.0, penka=True, ph=.0, col="#e8e2d6"):
    """Кружка с молоком: ручка-ухо, пенка кружком, пар не рисуем (холодное)."""
    s = (f'<path d="M{x-34*s_:.0f},{y-78*s_:.0f} h{68*s_:.0f} l{-6*s_:.0f},{78*s_:.0f}'
         f' h{-56*s_:.0f} Z" fill="{col}" stroke="{K}" stroke-width="{3.8*s_:.1f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-78*s_:.0f}" rx="{34*s_:.0f}" ry="{10*s_:.0f}"'
          f' fill="#d6cfc0" stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-75*s_:.0f}" rx="{27*s_:.0f}" ry="{7.5*s_:.0f}"'
          f' fill="#faf6ec"/>')
    if penka:
        for i in range(5):
            s += (f'<circle cx="{x-18*s_+i*9*s_:.0f}" cy="{y-76*s_+((i*3)%5-2)*s_:.0f}"'
                  f' r="{(2.8+((i*2)%3))*s_:.1f}" fill="#ffffff" opacity=".85"/>')
    s += (f'<path d="M{x+30*s_:.0f},{y-64*s_:.0f} q{26*s_:.0f},{10*s_:.0f}'
          f' {0:.0f},{34*s_:.0f}" fill="none" stroke="{col}"'
          f' stroke-width="{10*s_:.1f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x+30*s_:.0f},{y-64*s_:.0f} q{26*s_:.0f},{10*s_:.0f}'
          f' {0:.0f},{34*s_:.0f}" fill="none" stroke="{K}" stroke-width="{2.4*s_:.1f}"/>')
    s += ten(x, y + 4 * s_, 38 * s_, 10 * s_, .4)
    return s


def snast_kruchki(x, y, t, s_=1.0, n=6, ph=.0):
    """Пробка с крючками и мотком лески: крючок узнаётся по цевью, жалу и
    бородке, леска уходит петлёй."""
    s = (f'<rect x="{x-70*s_:.0f}" y="{y-26*s_:.0f}" width="{140*s_:.0f}"'
         f' height="{40*s_:.0f}" rx="{10*s_:.0f}" fill="#c89a52" stroke="{K}"'
         f' stroke-width="{3.4*s_:.1f}"/>')
    for i in range(10):
        s += (f'<circle cx="{x-60*s_+i*13*s_:.0f}" cy="{y-14*s_:.0f}" r="{2.4*s_:.1f}"'
              f' fill="#a87c3a" opacity=".8"/>')
    for i in range(n):
        kx = x - 52 * s_ + i * 104 * s_ / max(1, n - 1)
        dr = 2.0 * s_ * A.w(t, 1.8, ph + i * .2)
        s += (f'<path d="M{kx:.0f},{y-26*s_:.0f} l0,{-42*s_+dr:.0f}" stroke="{ZHELEZ}"'
              f' stroke-width="{3.2*s_:.1f}" fill="none"/>')
        s += (f'<path d="M{kx:.0f},{y-68*s_+dr:.0f} q{-14*s_:.0f},{-16*s_:.0f}'
              f' {-16*s_:.0f},{-30*s_:.0f} q{14*s_:.0f},{-6*s_:.0f} {12*s_:.0f},{10*s_:.0f}"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="{3.2*s_:.1f}"/>')
        s += (f'<circle cx="{kx:.0f}" cy="{y-26*s_:.0f}" r="{3.2*s_:.1f}" fill="{CHUGUN}"/>')
    s += (f'<path d="M{x+64*s_:.0f},{y-10*s_:.0f} q{40*s_:.0f},{-24*s_:.0f}'
          f' {66*s_:.0f},{8*s_:.0f} q{-26*s_:.0f},{22*s_:.0f} {-62*s_:.0f},{10*s_:.0f}"'
          f' fill="none" stroke="#cfd6db" stroke-width="{2.2*s_:.1f}" opacity=".85"/>')
    s += ten(x, y + 16 * s_, 74 * s_, 13 * s_, .4)
    return s


def peshnya(x, y, s_=1.0, ug=-18.0, t=0.0, ph=.0):
    """Пешня — пика на длинном черене, которой пробуют лёд: гранёное железо,
    обмотка, кожаная петля."""
    dr = 1.4 * A.w(t, 2.4, ph)
    s = (f'<g transform="rotate({ug+dr:.1f} {x:.0f} {y:.0f})">'
         f'<rect x="{x-9*s_:.0f}" y="{y-250*s_:.0f}" width="{18*s_:.0f}"'
         f' height="{250*s_:.0f}" rx="{6*s_:.0f}" fill="#8a6342" stroke="{K}"'
         f' stroke-width="{3*s_:.1f}"/>')
    s += (f'<path d="M{x-14*s_:.0f},{y:.0f} l{14*s_:.0f},{52*s_:.0f}'
          f' l{14*s_:.0f},{-52*s_:.0f} Z" fill="{ZHELEZ}" stroke="{K}"'
          f' stroke-width="{3.2*s_:.1f}"/>')
    s += (f'<path d="M{x:.0f},{y+14*s_:.0f} l0,{36*s_:.0f}" stroke="#cfd6db"'
          f' stroke-width="{2.4*s_:.1f}" opacity=".8"/>')
    for i in range(3):
        s += (f'<rect x="{x-11*s_:.0f}" y="{y-40*s_+i*13*s_:.0f}" width="{22*s_:.0f}"'
              f' height="{7*s_:.0f}" fill="{MED}" opacity=".9"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-250*s_:.0f}" rx="{14*s_:.0f}" ry="{8*s_:.0f}"'
          f' fill="none" stroke="#6b4428" stroke-width="{4*s_:.1f}"/>')
    return s + '</g>'


def konki_snegurki(x, y, s_=1.0, ug=0.0, na_valenke=False, t=0.0, ph=.0):
    """Коньки-«снегурки»: полоз с загнутым носом, площадка, ремешки; при
    na_valenke — привязаны к валенку верёвкой с палочкой-закруткой."""
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    if na_valenke:
        s += (f'<path d="M{x-46*s_:.0f},{y-126*s_:.0f} h{66*s_:.0f} q{12*s_:.0f},{54*s_:.0f}'
              f' {6*s_:.0f},{92*s_:.0f} l{-62*s_:.0f},0 q{-16*s_:.0f},{-44*s_:.0f}'
              f' {-10*s_:.0f},{-92*s_:.0f} Z" fill="#6f6256" stroke="{K}"'
              f' stroke-width="{3.6*s_:.1f}"/>')
        s += (f'<path d="M{x-44*s_:.0f},{y-54*s_:.0f} h{72*s_:.0f}" stroke="#55493f"'
              f' stroke-width="{6*s_:.1f}" opacity=".8"/>')
    s += (f'<rect x="{x-50*s_:.0f}" y="{y-28*s_:.0f}" width="{100*s_:.0f}"'
          f' height="{14*s_:.0f}" rx="{4*s_:.0f}" fill="#8a6342" stroke="{K}"'
          f' stroke-width="{2.8*s_:.1f}"/>')
    s += (f'<path d="M{x-52*s_:.0f},{y-6*s_:.0f} h{92*s_:.0f} q{18*s_:.0f},0'
          f' {18*s_:.0f},{-18*s_:.0f} q{-6*s_:.0f},{10*s_:.0f} {-20*s_:.0f},{10*s_:.0f}'
          f' h{-90*s_:.0f} Z" fill="#c9ccd1" stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    s += (f'<path d="M{x-52*s_:.0f},{y-2*s_:.0f} h{110*s_:.0f}" stroke="#eef3f8"'
          f' stroke-width="{2.4*s_:.1f}" opacity=".9"/>')
    for i in (-1, 1):                   # ремешки
        s += (f'<path d="M{x+i*26*s_:.0f},{y-28*s_:.0f} q{i*12*s_:.0f},{-20*s_:.0f}'
              f' {i*2*s_:.0f},{-36*s_:.0f}" fill="none" stroke="#5e4a2a"'
              f' stroke-width="{5*s_:.1f}"/>')
    s += (f'<rect x="{x-8*s_:.0f}" y="{y-74*s_:.0f}" width="{16*s_:.0f}"'
          f' height="{10*s_:.0f}" rx="{3*s_:.0f}" fill="#7d5636" stroke="{K}"'
          f' stroke-width="{2.2*s_:.1f}"/>')
    return s + '</g>'


def sanki_derev(x, y, s_=1.0, t=0.0, ph=.0, verevka=True):
    """Санки: гнутые полозья, стойки, настил из реек, верёвка петлёй."""
    s = (f'<path d="M{x-80*s_:.0f},{y:.0f} h{150*s_:.0f} q{22*s_:.0f},0'
         f' {26*s_:.0f},{-26*s_:.0f}" fill="none" stroke="#7d5636"'
         f' stroke-width="{9*s_:.1f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x-70*s_:.0f},{y-14*s_:.0f} h{150*s_:.0f} q{20*s_:.0f},0'
          f' {24*s_:.0f},{-24*s_:.0f}" fill="none" stroke="#8a6342"'
          f' stroke-width="{8*s_:.1f}" stroke-linecap="round" opacity=".9"/>')
    for i in range(4):
        px = x - 60 * s_ + i * 42 * s_
        s += (f'<rect x="{px:.0f}" y="{y-54*s_:.0f}" width="{10*s_:.0f}"'
              f' height="{46*s_:.0f}" fill="#6b4428" stroke="{K}" stroke-width="{2.4*s_:.1f}"/>')
    for i in range(5):
        s += (f'<rect x="{x-74*s_:.0f}" y="{y-70*s_+i*8*s_:.0f}" width="{166*s_:.0f}"'
              f' height="{6*s_:.0f}" rx="{2*s_:.0f}" fill="{DOSKA}" stroke="{K}"'
              f' stroke-width="{1.8*s_:.1f}"/>')
    if verevka:
        kach = 4 * s_ * A.w(t, 2.0, ph)
        s += (f'<path d="M{x+96*s_:.0f},{y-30*s_:.0f} q{50*s_:.0f},{10*s_+kach:.0f}'
              f' {86*s_:.0f},{-14*s_:.0f}" fill="none" stroke="#b9a37a"'
              f' stroke-width="{4*s_:.1f}"/>')
    s += ten(x + 10 * s_, y + 8 * s_, 96 * s_, 14 * s_, .4)
    return s


def chaynik_s_parom(x, y, s_=1.0, t=0.0, ph=.0, par_=True):
    """Чайник: пузатый корпус, носик, крышка с пуговкой, дужка; из носика
    идёт пар (живой огонёк сцены)."""
    s = (f'<path d="M{x-56*s_:.0f},{y-40*s_:.0f} q{-10*s_:.0f},{-56*s_:.0f}'
         f' {56*s_:.0f},{-58*s_:.0f} q{66*s_:.0f},{2*s_:.0f} {56*s_:.0f},{58*s_:.0f}'
         f' q{-6*s_:.0f},{34*s_:.0f} {-56*s_:.0f},{34*s_:.0f}'
         f' q{-50*s_:.0f},0 {-56*s_:.0f},{-34*s_:.0f} Z" fill="#b5803a"'
         f' stroke="{K}" stroke-width="{4*s_:.1f}"/>')
    s += (f'<path d="M{x+50*s_:.0f},{y-82*s_:.0f} q{40*s_:.0f},{-6*s_:.0f}'
          f' {44*s_:.0f},{-40*s_:.0f} l{-14*s_:.0f},{-6*s_:.0f}'
          f' q{-6*s_:.0f},{26*s_:.0f} {-34*s_:.0f},{30*s_:.0f} Z" fill="#a8742f"'
          f' stroke="{K}" stroke-width="{3.2*s_:.1f}"/>')
    s += (f'<path d="M{x-56*s_:.0f},{y-86*s_:.0f} q{-44*s_:.0f},{-20*s_:.0f}'
          f' {-28*s_:.0f},{-52*s_:.0f}" fill="none" stroke="{CHUGUN}"'
          f' stroke-width="{6*s_:.1f}"/>')
    s += (f'<ellipse cx="{x-4*s_:.0f}" cy="{y-100*s_:.0f}" rx="{30*s_:.0f}"'
          f' ry="{11*s_:.0f}" fill="#c08a3a" stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    s += (f'<circle cx="{x-4*s_:.0f}" cy="{y-112*s_:.0f}" r="{7*s_:.0f}" fill="{ZOL}"'
          f' stroke="{K}" stroke-width="{2.4*s_:.1f}"/>')
    s += (f'<path d="M{x-34*s_:.0f},{y-70*s_:.0f} q{-8*s_:.0f},{22*s_:.0f}'
          f' {4*s_:.0f},{38*s_:.0f}" fill="none" stroke="#ffe9c8"'
          f' stroke-width="{7*s_:.1f}" opacity=".5"/>')
    if par_:
        for i in range(5):
            d = ((t * .5 + ph + i / 5.0) % 1.0)
            s += (f'<ellipse cx="{x+96*s_+22*s_*d:.0f}" cy="{y-126*s_-66*s_*d:.0f}"'
                  f' rx="{(10+20*d)*s_:.0f}" ry="{(8+15*d)*s_:.0f}" fill="#eef3f8"'
                  f' opacity="{(1-d)*.5:.2f}"/>')
    s += ten(x, y + 6 * s_, 64 * s_, 15 * s_, .45)
    return s


def puchok_trav(x, y, s_=1.0, t=0.0, ph=.0, seed=3, col="#8a7a4a"):
    """Пучок сушёных трав, подвешенный вниз головками: стебли перевязаны
    бечёвкой, листочки врозь, качается."""
    rnd = random.Random(seed * 53 + 7)
    kach = 2.6 * A.w(t, 3.2, ph)
    s = f'<g transform="rotate({kach:.1f} {x:.0f} {y:.0f})">'
    for i in range(9):
        dx = rnd.uniform(-26, 26) * s_
        hh = rnd.uniform(90, 150) * s_
        s += (f'<path d="M{x:.0f},{y:.0f} q{dx*.5:.0f},{hh*.55:.0f} {dx:.0f},{hh:.0f}"'
              f' fill="none" stroke="{col}" stroke-width="{rnd.uniform(2.4,4.2)*s_:.1f}"/>')
        for k in range(3):
            p = .45 + k * .22
            lx = x + dx * p; ly = y + hh * p
            s += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rnd.uniform(5,9)*s_:.1f}"'
                  f' ry="{rnd.uniform(9,15)*s_:.1f}" fill="#7d7040"'
                  f' transform="rotate({rnd.uniform(-40,40):.0f} {lx:.0f} {ly:.0f})"'
                  f' opacity=".9"/>')
    s += (f'<rect x="{x-16*s_:.0f}" y="{y-8*s_:.0f}" width="{32*s_:.0f}"'
          f' height="{14*s_:.0f}" rx="{4*s_:.0f}" fill="#b9a37a" stroke="{K}"'
          f' stroke-width="{2.4*s_:.1f}"/>')
    return s + '</g>'


# ═══════════ ИНТЕРЬЕРЫ, ШКОЛА, СЕВЕР, СКАЗОЧНЫЕ ФИГУРЫ ════════════════════

def stena_gornicy_19(t, seed=5, pol_y=790, polotence=True, venec=True):
    """Бревенчатая стена горницы этого ролика: венцы, мох в пазах, полотенце
    с красным узором, деревянный пол с половицами и домотканый половик."""
    rnd = random.Random(seed * 59 + 3)
    s = brevna(0, 0, W, pol_y, 86, seed % 3)
    for i in range(7):                  # мох в пазах, чтобы стена не была обоями
        yy = 86 * (i + 1)
        s += (f'<path d="M0,{yy:.0f} Q{rnd.uniform(300,700):.0f},{yy+rnd.uniform(-5,5):.0f}'
              f' {W},{yy+rnd.uniform(-4,4):.0f}" fill="none" stroke="#5e6a3a"'
              f' stroke-width="{rnd.uniform(3,6):.1f}" opacity=".45"/>')
    if venec:
        s += (f'<rect x="0" y="{pol_y-28:.0f}" width="{W}" height="28" fill="{BREVNO2}"'
              f' stroke="{K}" stroke-width="4"/>')
    s += polovicy(pol_y)
    s += (f'<path d="M{rnd.uniform(200,420):.0f},{pol_y+120:.0f} h620 l-40,160 h-540 Z"'
          f' fill="{TKAN2}" opacity=".85" stroke="{K}" stroke-width="3"/>')
    for i in range(6):
        s += (f'<path d="M{rnd.uniform(230,420)+i*96:.0f},{pol_y+128:.0f}'
              f' l{-26:.0f},{150:.0f}" stroke="{RUSH}" stroke-width="7" opacity=".55"/>')
    if polotence:
        px = rnd.uniform(1280, 1600)
        s += (f'<rect x="{px:.0f}" y="{90:.0f}" width="124" height="300" rx="5"'
              f' fill="{RUSH}" stroke="{K}" stroke-width="4"/>')
        for i in range(4):
            s += (f'<path d="M{px+10:.0f},{150+i*62:.0f} h104" stroke="{TKAN}"'
                  f' stroke-width="9" opacity=".9"/>')
            s += (f'<path d="M{px+22:.0f},{168+i*62:.0f} l16,-14 l16,14 l16,-14 l16,14"'
                  f' fill="none" stroke="{TKAN}" stroke-width="4"/>')
        s += (f'<rect x="{px-8:.0f}" y="{78:.0f}" width="140" height="16" rx="4"'
              f' fill="{DOSKA2}" stroke="{K}" stroke-width="3"/>')
    return s


def polka_s_bankami(x, y, w_, t, seed=11, n=5, inej_=False):
    """Полка с банками, крынками и лукошком — обжитой средний план.
    Состав РАЗНЫЙ по seed, иначе одна и та же полка во всех сценах."""
    rnd = random.Random(seed * 61 + 5)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="18" rx="4"'
         f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>')
    s += (f'<path d="M{x+20:.0f},{y+18:.0f} l14,34 M{x+w_-34:.0f},{y+18:.0f} l-14,34"'
          f' stroke="{DOSKA2}" stroke-width="7" fill="none"/>')
    for i in range(n):
        px = x + 40 + i * (w_ - 80) / max(1, n - 1)
        vid = rnd.choice(("banka", "krynka", "lukoshko", "chugunok", "butyl"))
        if vid == "banka":
            s += banka_moloka(px, y, rnd.uniform(.44, .62), t, True,
                              rnd.uniform(.5, .9),
                              rnd.choice(("#c8301f", "#b5803a", "#7d9a3a", "#faf6ec")))
        elif vid == "krynka":
            s += krynka_moloka(px, y, rnd.uniform(.42, .58), t, False, False, i * .3)
        elif vid == "lukoshko":
            s += (f'<path d="M{px-34:.0f},{y-56:.0f} q{34:.0f},{14:.0f} {68:.0f},0'
                  f' l-8,56 h-52 Z" fill="#b08a52" stroke="{K}" stroke-width="3.4"/>'
                  f'<path d="M{px-32:.0f},{y-56:.0f} q{32:.0f},{-44:.0f} {64:.0f},0"'
                  f' fill="none" stroke="#9a7c45" stroke-width="5"/>')
        elif vid == "chugunok":
            s += (f'<path d="M{px-32:.0f},{y-30:.0f} q{-10:.0f},{-38:.0f} {32:.0f},{-40:.0f}'
                  f' q{42:.0f},{2:.0f} {32:.0f},{40:.0f} q{-6:.0f},{30:.0f} {-32:.0f},{30:.0f}'
                  f' q{-26:.0f},0 {-32:.0f},{-30:.0f} Z" fill="{CHUGUN}" stroke="{K}"'
                  f' stroke-width="3.4"/>'
                  f'<ellipse cx="{px:.0f}" cy="{y-70:.0f}" rx="26" ry="8" fill="#4a4442"'
                  f' stroke="{K}" stroke-width="2.6"/>')
        else:
            s += (f'<path d="M{px-18:.0f},{y-44:.0f} h36 l6,44 h-48 Z" fill="{STEKLO}"'
                  f' opacity=".6" stroke="{K}" stroke-width="3"/>'
                  f'<rect x="{px-7:.0f}" y="{y-82:.0f}" width="14" height="40"'
                  f' fill="{STEKLO}" opacity=".6" stroke="{K}" stroke-width="2.6"/>'
                  f'<rect x="{px-9:.0f}" y="{y-88:.0f}" width="18" height="9" rx="2"'
                  f' fill="{MED}" stroke="{K}" stroke-width="2"/>')
        if inej_:
            s += inej_mel(seed + i, 6, y - 60, y - 10, px - 30, px + 30)
    return s


def parta_shkolnaya(x, y, w_, t, seed=3, portfel=True):
    """Школьная парта: наклонная крышка с желобком, откидная скамья,
    чернильница-непроливайка, ручка, кусок мела."""
    s = (f'<path d="M{x:.0f},{y-150:.0f} l{w_:.0f},{-26:.0f} l0,{20:.0f}'
         f' l{-w_:.0f},{26:.0f} Z" fill="{DOSKA}" stroke="{K}" stroke-width="4"/>')
    s += (f'<rect x="{x:.0f}" y="{y-132:.0f}" width="{w_:.0f}" height="16" rx="3"'
          f' fill="{DOSKA2}" stroke="{K}" stroke-width="3"/>')
    for px in (x + 16, x + w_ - 34):
        s += (f'<rect x="{px:.0f}" y="{y-120:.0f}" width="20" height="120"'
              f' fill="{POL2}" stroke="{K}" stroke-width="3.4"/>')
    s += (f'<rect x="{x-14:.0f}" y="{y-60:.0f}" width="{w_+28:.0f}" height="16" rx="4"'
          f' fill="{DOSKA}" stroke="{K}" stroke-width="3.4"/>')
    s += (f'<circle cx="{x+w_*.80:.0f}" cy="{y-158:.0f}" r="14" fill="#2b3550"'
          f' stroke="{K}" stroke-width="3"/>')
    s += (f'<ellipse cx="{x+w_*.80:.0f}" cy="{y-162:.0f}" rx="9" ry="4" fill="#16203a"/>')
    s += (f'<path d="M{x+w_*.60:.0f},{y-156:.0f} l44,-10" stroke="#8a6342"'
          f' stroke-width="6" fill="none"/>'
          f'<path d="M{x+w_*.60+44:.0f},{y-166:.0f} l12,-3" stroke="{ZHELEZ}"'
          f' stroke-width="5" fill="none"/>')
    s += (f'<rect x="{x+w_*.22:.0f}" y="{y-152:.0f}" width="26" height="9" rx="3"'
          f' fill="#f4f1e8" stroke="{K}" stroke-width="2"/>')
    if portfel:
        s += (f'<rect x="{x+w_*.10:.0f}" y="{y-44:.0f}" width="104" height="72" rx="8"'
              f' fill="#6b4428" stroke="{K}" stroke-width="3.6"/>'
              f'<path d="M{x+w_*.10:.0f},{y-20:.0f} h104" stroke="#54351f"'
              f' stroke-width="5"/>'
              f'<rect x="{x+w_*.10+40:.0f}" y="{y-26:.0f}" width="24" height="16" rx="3"'
              f' fill="{MED}" stroke="{K}" stroke-width="2.4"/>')
    s += ten(x + w_ * .5, y + 6, w_ * .6, 14, .4)
    return s


def uchebnik_razvorot(x, y, w_, h_, t, proem=False, ph=.0):
    """Раскрытый учебник: две страницы с корешком, волнистые строки (букв не
    рисуем), закладка. proem=True — правая страница оставлена ПУСТОЙ под
    настоящий портрет (метку ставит сцена)."""
    s = (f'<path d="M{x:.0f},{y:.0f} q{w_*.25:.0f},{-18:.0f} {w_*.5:.0f},0'
         f' q{w_*.25:.0f},{-18:.0f} {w_*.5:.0f},0 l0,{h_:.0f}'
         f' q{-w_*.25:.0f},{16:.0f} {-w_*.5:.0f},0 q{-w_*.25:.0f},{16:.0f}'
         f' {-w_*.5:.0f},0 Z" fill="#f6f1e2" stroke="{K}" stroke-width="4.5"/>')
    s += (f'<path d="M{x+w_*.5:.0f},{y-6:.0f} l0,{h_+4:.0f}" stroke="#c9bfa6"'
          f' stroke-width="7" opacity=".9"/>')
    s += (f'<path d="M{x-10:.0f},{y+h_-6:.0f} q{w_*.5:.0f},{22:.0f} {w_+20:.0f},0'
          f' l0,16 q{-w_*.5:.0f},{20:.0f} {-w_-20:.0f},0 Z" fill="#8a2f22"'
          f' stroke="{K}" stroke-width="4"/>')
    rnd = random.Random(7)
    for i in range(9):                  # волнистые строки на левой странице
        yy = y + 46 + i * (h_ - 80) / 9.0
        s += (f'<path d="M{x+w_*.07:.0f},{yy:.0f} q{w_*.10:.0f},{rnd.uniform(-5,5):.0f}'
              f' {w_*.20:.0f},0 q{w_*.10:.0f},{rnd.uniform(-5,5):.0f} {w_*.16:.0f},0"'
              f' fill="none" stroke="#6f6354" stroke-width="3.4" opacity=".75"/>')
    if not proem:
        for i in range(7):
            yy = y + 60 + i * (h_ - 110) / 7.0
            s += (f'<path d="M{x+w_*.56:.0f},{yy:.0f} q{w_*.12:.0f},{rnd.uniform(-5,5):.0f}'
                  f' {w_*.22:.0f},0" fill="none" stroke="#6f6354" stroke-width="3.2"'
                  f' opacity=".7"/>')
    bl = .14 + .10 * A.w(t, 3.4, ph)
    s += (f'<ellipse cx="{x+w_*.30:.0f}" cy="{y+h_*.42:.0f}" rx="{w_*.22:.0f}"'
          f' ry="{h_*.30:.0f}" fill="#ffffff" opacity="{bl:.2f}"/>')
    s += (f'<rect x="{x+w_*.92:.0f}" y="{y+10:.0f}" width="14" height="{h_*.5:.0f}"'
          f' fill="{TKAN}" stroke="{K}" stroke-width="2.4"/>')
    return s


def klassnaya_doska(x, y, w_, h_, t, seed=5):
    """Классная доска: тёмное поле, рама, желобок с мелом и тряпкой, следы
    стёртого мела (строк и букв не рисуем)."""
    rnd = random.Random(seed * 67 + 3)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6"'
         f' fill="#2e3a33" stroke="{K}" stroke-width="5"/>')
    s += (f'<rect x="{x+10:.0f}" y="{y+10:.0f}" width="{w_-20:.0f}" height="{h_-20:.0f}"'
          f' rx="4" fill="#27322c" stroke="#4a564d" stroke-width="3"/>')
    for i in range(6):
        s += (f'<path d="M{x+rnd.uniform(40, w_*.5):.0f},{y+rnd.uniform(40, h_-50):.0f}'
              f' q{rnd.uniform(60,180):.0f},{rnd.uniform(-20,20):.0f}'
              f' {rnd.uniform(140,320):.0f},{rnd.uniform(-14,14):.0f}" fill="none"'
              f' stroke="#cfd6cb" stroke-width="{rnd.uniform(6,16):.1f}" opacity=".10"/>')
    s += (f'<rect x="{x-6:.0f}" y="{y+h_:.0f}" width="{w_+12:.0f}" height="20" rx="4"'
          f' fill="{DOSKA2}" stroke="{K}" stroke-width="4"/>')
    s += (f'<rect x="{x+w_*.18:.0f}" y="{y+h_-6:.0f}" width="40" height="11" rx="4"'
          f' fill="#f4f1e8" stroke="{K}" stroke-width="2.2"/>')
    s += (f'<rect x="{x+w_*.70:.0f}" y="{y+h_-10:.0f}" width="62" height="18" rx="5"'
          f' fill="{TKAN2}" stroke="{K}" stroke-width="2.6"/>')
    return s


def schety_kostyashki(x, y, s_=1.0, t=0.0, ph=.0, seed=3):
    """Счёты: рама, прутья, костяшки сдвинуты врозь, одна катится."""
    rnd = random.Random(seed * 71 + 5)
    w_, h_ = 300 * s_, 190 * s_
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8"'
         f' fill="url(#derev)" stroke="{K}" stroke-width="{4.5*s_:.1f}"/>')
    s += (f'<rect x="{x+10*s_:.0f}" y="{y+10*s_:.0f}" width="{w_-20*s_:.0f}"'
          f' height="{h_-20*s_:.0f}" rx="5" fill="#6b4428" opacity=".55"/>')
    for i in range(7):
        yy = y + 24 * s_ + i * (h_ - 48 * s_) / 6.0
        s += (f'<line x1="{x+14*s_:.0f}" y1="{yy:.0f}" x2="{x+w_-14*s_:.0f}" y2="{yy:.0f}"'
              f' stroke="{ZHELEZ}" stroke-width="{2.6*s_:.1f}"/>')
        sd = rnd.randint(2, 7)
        for k in range(9):
            cx = (x + 24 * s_ + k * 15 * s_) if k < sd else (x + w_ - 24 * s_ - (8 - k) * 15 * s_)
            if i == 2 and k == sd - 1:  # одна костяшка катится
                cx += 26 * s_ * A.ease(A.seg(t, .4, .9))
            s += (f'<ellipse cx="{cx:.0f}" cy="{yy:.0f}" rx="{7.5*s_:.1f}"'
                  f' ry="{9.5*s_:.1f}" fill="{"#8a2f22" if k in (4,5) else "#c8a05a"}"'
                  f' stroke="{K}" stroke-width="{2*s_:.1f}"/>')
    return s


def gradusnik_ulichnyy(x, y, s_=1.0, t=0.0, ph=.0, stolb=.42):
    """Уличный градусник за окном: шкала с делениями, красный столбик,
    колба внизу. Цифр не рисуем — только риски (букв и чисел не рисуем)."""
    h_ = 260 * s_
    s = (f'<rect x="{x-26*s_:.0f}" y="{y-h_:.0f}" width="{52*s_:.0f}" height="{h_:.0f}"'
         f' rx="{8*s_:.0f}" fill="#f2efe4" stroke="{K}" stroke-width="{3.6*s_:.1f}"/>')
    for i in range(13):
        yy = y - h_ + 18 * s_ + i * (h_ - 36 * s_) / 12.0
        dl = 16 * s_ if i % 3 == 0 else 9 * s_
        s += (f'<line x1="{x-20*s_:.0f}" y1="{yy:.0f}" x2="{x-20*s_+dl:.0f}" y2="{yy:.0f}"'
              f' stroke="#5f5a4e" stroke-width="{2.4*s_:.1f}"/>')
    kol = y - 26 * s_
    st = h_ * stolb * (1 + .02 * A.w(t, 4.0, ph))
    s += (f'<rect x="{x+4*s_:.0f}" y="{kol-st:.0f}" width="{9*s_:.0f}" height="{st:.0f}"'
          f' fill="#c8301f" opacity=".95"/>')
    s += (f'<circle cx="{x+8*s_:.0f}" cy="{kol:.0f}" r="{13*s_:.0f}" fill="#c8301f"'
          f' stroke="{K}" stroke-width="{2.6*s_:.1f}"/>')
    s += (f'<path d="M{x-18*s_:.0f},{y-h_+30*s_:.0f} l0,{h_*.5:.0f}" stroke="#ffffff"'
          f' stroke-width="{5*s_:.1f}" opacity=".4"/>')
    return s


def verstovoy_stolb(x, y, h_, t, s_=1.0, ph=.0):
    """Верстовой столб: косые полосы, навершие, снеговая шапка (цифр нет)."""
    s = (f'<rect x="{x-14*s_:.0f}" y="{y-h_:.0f}" width="{28*s_:.0f}" height="{h_:.0f}"'
         f' rx="{4*s_:.0f}" fill="#efe6d2" stroke="{K}" stroke-width="{3.6*s_:.1f}"/>')
    for i in range(int(h_ / (34 * s_))):
        s += (f'<path d="M{x-14*s_:.0f},{y-h_+i*34*s_:.0f} l{28*s_:.0f},{-18*s_:.0f}'
              f' l0,{16*s_:.0f} l{-28*s_:.0f},{18*s_:.0f} Z" fill="#2b3550" opacity=".85"/>')
    s += (f'<path d="M{x-20*s_:.0f},{y-h_:.0f} l{20*s_:.0f},{-24*s_:.0f}'
          f' l{20*s_:.0f},{24*s_:.0f} Z" fill="#efe6d2" stroke="{K}"'
          f' stroke-width="{3*s_:.1f}"/>')
    s += (f'<path d="M{x-22*s_:.0f},{y-h_-22*s_:.0f} q{22*s_:.0f},{-14*s_:.0f}'
          f' {44*s_:.0f},0 l0,{8*s_:.0f} q{-22*s_:.0f},{10*s_:.0f} {-44*s_:.0f},0 Z"'
          f' fill="url(#sneg)"/>')
    s += ten(x, y + 4 * s_, 26 * s_, 8 * s_, .4)
    return s


def karbas_pod_parusom(x, y, w_, t, ph=.0):
    """Поморский карбас: высокий нос и корма, мачта с надутым парусом,
    борта обшиты, на корме руль-весло, в лодке бочонок и сети."""
    h_ = w_ * .30
    s = (f'<path d="M{x-w_*.5:.0f},{y:.0f} q{w_*.1:.0f},{h_*.72:.0f} {w_*.5:.0f},{h_*.80:.0f}'
         f' q{w_*.4:.0f},{-h_*.08:.0f} {w_*.5:.0f},{-h_*.80:.0f} q{-w_*.2:.0f},{h_*.26:.0f}'
         f' {-w_*.5:.0f},{h_*.30:.0f} q{-w_*.3:.0f},{-h_*.04:.0f} {-w_*.5:.0f},{-h_*.30:.0f} Z"'
         f' fill="#6b4428" stroke="{K}" stroke-width="5"/>')
    for i in range(3):
        s += (f'<path d="M{x-w_*.46:.0f},{y+h_*(.14+i*.16):.0f}'
              f' q{w_*.46:.0f},{h_*.34:.0f} {w_*.92:.0f},0" fill="none" stroke="#54351f"'
              f' stroke-width="4" opacity=".8"/>')
    s += (f'<rect x="{x-6:.0f}" y="{y-w_*.52:.0f}" width="12" height="{w_*.52:.0f}"'
          f' fill="#8a6342" stroke="{K}" stroke-width="3.4"/>')
    puz = 26 + 12 * A.w(t, 3.0, ph)
    s += (f'<path d="M{x+2:.0f},{y-w_*.50:.0f} q{puz+w_*.26:.0f},{w_*.14:.0f}'
          f' {w_*.06:.0f},{w_*.44:.0f} Z" fill="{RUSH}" stroke="{K}" stroke-width="4"/>')
    s += (f'<path d="M{x+2:.0f},{y-w_*.34:.0f} q{puz*.8+w_*.18:.0f},{w_*.08:.0f}'
          f' {w_*.04:.0f},{w_*.16:.0f}" fill="none" stroke="#c9bfa6" stroke-width="3"/>')
    s += (f'<path d="M{x+w_*.40:.0f},{y+h_*.30:.0f} l{w_*.22:.0f},{h_*.70:.0f}"'
          f' stroke="#7d5636" stroke-width="9" fill="none"/>')
    s += (f'<path d="M{x-w_*.26:.0f},{y+h_*.34:.0f} h{w_*.16:.0f} l-4,{h_*.26:.0f}'
          f' h{-w_*.14:.0f} Z" fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    for i in range(4):
        s += (f'<path d="M{x-w_*.08+i*18:.0f},{y+h_*.46:.0f} q{14:.0f},{18:.0f}'
              f' {0:.0f},{30:.0f}" fill="none" stroke="#b9a37a" stroke-width="2.4"'
              f' opacity=".85"/>')
    return s


def sani_s_rogozhey(x, y, s_=1.0, t=0.0, ph=.0, ryba=True):
    """Сани обоза: полозья, грядки, груз под рогожей, верёвочная обвязка;
    из-под рогожи торчат мороженые рыбины."""
    s = (f'<path d="M{x-110*s_:.0f},{y:.0f} h{220*s_:.0f} q{26*s_:.0f},0'
         f' {32*s_:.0f},{-30*s_:.0f}" fill="none" stroke="#6b4428"'
         f' stroke-width="{10*s_:.1f}" stroke-linecap="round"/>')
    for i in range(4):
        s += (f'<rect x="{x-90*s_+i*52*s_:.0f}" y="{y-60*s_:.0f}" width="{11*s_:.0f}"'
              f' height="{56*s_:.0f}" fill="#54351f" stroke="{K}" stroke-width="{2.6*s_:.1f}"/>')
    s += (f'<rect x="{x-104*s_:.0f}" y="{y-74*s_:.0f}" width="{212*s_:.0f}"'
          f' height="{16*s_:.0f}" rx="{4*s_:.0f}" fill="{DOSKA}" stroke="{K}"'
          f' stroke-width="{3*s_:.1f}"/>')
    s += (f'<path d="M{x-100*s_:.0f},{y-76*s_:.0f} q{40*s_:.0f},{-66*s_:.0f}'
          f' {100*s_:.0f},{-62*s_:.0f} q{62*s_:.0f},{-4*s_:.0f} {100*s_:.0f},{62*s_:.0f} Z"'
          f' fill="#9a8a62" stroke="{K}" stroke-width="{4*s_:.1f}"/>')
    for i in range(5):
        s += (f'<path d="M{x-84*s_+i*42*s_:.0f},{y-82*s_:.0f} q{6*s_:.0f},{-30*s_:.0f}'
              f' {2*s_:.0f},{-46*s_:.0f}" fill="none" stroke="#7d7050"'
              f' stroke-width="{3*s_:.1f}" opacity=".8"/>')
    s += (f'<path d="M{x-96*s_:.0f},{y-108*s_:.0f} q{96*s_:.0f},{26*s_:.0f}'
          f' {192*s_:.0f},0" fill="none" stroke="#b9a37a" stroke-width="{4*s_:.1f}"/>')
    if ryba:
        for i, (dx, ug) in enumerate(((-66, -16), (-18, 8), (40, -8))):
            fx, fy = x + dx * s_, y - 128 * s_
            s += (f'<g transform="rotate({ug} {fx:.0f} {fy:.0f})">'
                  f'<path d="M{fx-34*s_:.0f},{fy:.0f} q{34*s_:.0f},{-20*s_:.0f}'
                  f' {68*s_:.0f},0 q{-34*s_:.0f},{20*s_:.0f} {-68*s_:.0f},0 Z"'
                  f' fill="#a8b4bc" stroke="{K}" stroke-width="{2.8*s_:.1f}"/>'
                  f'<path d="M{fx+34*s_:.0f},{fy:.0f} l{16*s_:.0f},{-10*s_:.0f}'
                  f' l0,{20*s_:.0f} Z" fill="#8f9ba3" stroke="{K}" stroke-width="{2.4*s_:.1f}"/>'
                  f'<circle cx="{fx-22*s_:.0f}" cy="{fy-3*s_:.0f}" r="{3.4*s_:.1f}"'
                  f' fill="{K}"/>'
                  f'<path d="M{fx-20*s_:.0f},{fy-8*s_:.0f} q{20*s_:.0f},{-6*s_:.0f}'
                  f' {38*s_:.0f},{2*s_:.0f}" fill="none" stroke="{INEY}"'
                  f' stroke-width="{2.6*s_:.1f}" opacity=".7"/></g>')
    s += ten(x, y + 8 * s_, 120 * s_, 16 * s_, .4)
    return s


def vodyanoy(x, y, t, s_=1.0, ph=.0):
    """ВОДЯНОЙ — сказочная фигура, НЕ страшная (его записка): добродушный
    старик из воды, борода водорослями, на голове шапка из тины, в руке
    кубышка. Полупрозрачен только фоном, лицо доброе."""
    s = (f'<ellipse cx="{x:.0f}" cy="{y-40*s_:.0f}" rx="{96*s_:.0f}" ry="{66*s_:.0f}"'
         f' fill="{VODA}" opacity=".40"/>')
    s += (f'<path d="M{x-70*s_:.0f},{y:.0f} q{10*s_:.0f},{-92*s_:.0f} {70*s_:.0f},{-96*s_:.0f}'
          f' q{60*s_:.0f},{4*s_:.0f} {70*s_:.0f},{96*s_:.0f} Z" fill="#3f7f82"'
          f' stroke="{K}" stroke-width="{4*s_:.1f}" opacity=".95"/>')
    gy = y - 128 * s_
    s += (f'<circle cx="{x:.0f}" cy="{gy:.0f}" r="{46*s_:.0f}" fill="#5aa0a0"'
          f' stroke="{K}" stroke-width="{4*s_:.1f}"/>')
    mig = 0 if A.blink(t, 3.6, ph) else 1
    for i in (-1, 1):
        if mig:
            s += (f'<circle cx="{x+i*17*s_:.0f}" cy="{gy-6*s_:.0f}" r="{7*s_:.1f}"'
                  f' fill="#f4f8f2"/>'
                  f'<circle cx="{x+i*17*s_:.0f}" cy="{gy-6*s_:.0f}" r="{3.4*s_:.1f}"'
                  f' fill="#1b2b33"/>')
        else:
            s += (f'<path d="M{x+i*24*s_:.0f},{gy-6*s_:.0f} q{-i*7*s_:.0f},{5*s_:.0f}'
                  f' {-i*14*s_:.0f},0" fill="none" stroke="#1b2b33"'
                  f' stroke-width="{3*s_:.1f}"/>')
    s += (f'<path d="M{x-16*s_:.0f},{gy+16*s_:.0f} q{16*s_:.0f},{14*s_:.0f}'
          f' {32*s_:.0f},0" fill="none" stroke="#1b4b4b" stroke-width="{3.4*s_:.1f}"'
          f' stroke-linecap="round"/>')
    for i in range(9):                  # борода водорослями
        a = -1.1 + i * .27
        kach = 6 * s_ * A.w(t, 2.2, ph + i * .17)
        s += (f'<path d="M{x+36*s_*math.sin(a):.0f},{gy+34*s_:.0f}'
              f' q{kach:.0f},{40*s_:.0f} {kach*1.4:.0f},{74*s_:.0f}" fill="none"'
              f' stroke="#2f6b5a" stroke-width="{5*s_:.1f}" opacity=".9"/>')
    s += (f'<path d="M{x-48*s_:.0f},{gy-30*s_:.0f} q{48*s_:.0f},{-34*s_:.0f}'
          f' {96*s_:.0f},0 q{-20*s_:.0f},{16*s_:.0f} {-96*s_:.0f},0 Z" fill="#3f6b3a"'
          f' stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    for i in range(4):
        d = ((t * .6 + ph + i / 4.0) % 1.0)
        s += (f'<circle cx="{x+40*s_+30*s_*math.sin(i*2.1):.0f}"'
              f' cy="{y-60*s_-110*s_*d:.0f}" r="{(4+7*d)*s_:.1f}" fill="#cfe4f5"'
              f' opacity="{(1-d)*.6:.2f}"/>')
    return s


def moroz_ded(x, y, t, s_=1.0, ph=.0):
    """МОРОЗ — сказочный дед в синей шубе с посохом-сосулькой: не страшный,
    борода сосульками, из посоха сыплются искры холода."""
    s = figura(x, y, 420 * s_, t, col="#2f5c84", kant="#dcecf8", ph=ph,
               boroda=True, tulup=True)
    px, py = _plecho(x, y, 420 * s_, 1)
    ruk, (ex, ey), _ = _ruka(x, y, 420 * s_, 1, 150 * s_, 34, t, "#2f5c84",
                             "#dcecf8", ph, 4.0)
    s += ruk
    s += (f'<path d="M{ex:.0f},{ey-190*s_:.0f} l{8*s_:.0f},{250*s_:.0f}'
          f' l{-16*s_:.0f},0 Z" fill="#9fd0e4" stroke="#eaf6ff"'
          f' stroke-width="{3*s_:.1f}" opacity=".95"/>')
    s += (f'<circle cx="{ex+4*s_:.0f}" cy="{ey-196*s_:.0f}" r="{18*s_:.0f}"'
          f' fill="#dcecf8" stroke="#ffffff" stroke-width="{3*s_:.1f}"/>')
    for i in range(6):
        d = ((t * .7 + ph + i / 6.0) % 1.0)
        s += (f'<path d="M{ex+4*s_+(i-3)*16*s_:.0f},{ey-180*s_+120*s_*d:.0f}'
              f' l{5*s_:.0f},{5*s_:.0f} l{-5*s_:.0f},{5*s_:.0f} l{-5*s_:.0f},{-5*s_:.0f} Z"'
              f' fill="#ffffff" opacity="{(1-d)*.8:.2f}"/>')
    return s


def neudacha_figurka(x, y, t, s_=1.0, ph=.0):
    """НЕУДАЧА — серая сутулая фигурка с пустым узелком на палке: идёт
    следом, сказочная, не страшная (его записка)."""
    h_ = 300 * s_
    s = figura(x, y, h_, t, col="#5e5a55", kant="#9aa3a8", ph=ph, naklon=2.0)
    ruk, (ex, ey), _ = _ruka(x, y, h_, 1, 96 * s_, 22, t, "#5e5a55", "#9aa3a8", ph, 5.0)
    s += ruk
    s += (f'<path d="M{ex-10*s_:.0f},{ey-6*s_:.0f} l{120*s_:.0f},{-54*s_:.0f}"'
          f' stroke="#6b5230" stroke-width="{6*s_:.1f}" fill="none"/>')
    kach = 5 * s_ * A.w(t, 1.7, ph)
    s += (f'<path d="M{ex+104*s_:.0f},{ey-50*s_:.0f} q{26*s_+kach:.0f},{54*s_:.0f}'
          f' {52*s_:.0f},{-4*s_:.0f} q{-24*s_:.0f},{-26*s_:.0f} {-52*s_:.0f},{4*s_:.0f} Z"'
          f' fill="#8f8a82" stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y+4*s_:.0f}" rx="{70*s_:.0f}" ry="{14*s_:.0f}"'
          f' fill="{K}" opacity=".30"/>')
    return s


def chertenok(x, y, t, s_=1.0, ph=.0, col="#4a3a52"):
    """Чертёнок — мелкая сказочная фигурка (не страшная): круглая голова,
    рожки, хвост с кисточкой, прыгает на месте."""
    pr = 16 * s_ * abs(A.w(t, 1.1, ph))
    s = f'<g transform="translate(0,{-pr:.1f})">'
    s += (f'<ellipse cx="{x:.0f}" cy="{y-44*s_:.0f}" rx="{30*s_:.0f}" ry="{36*s_:.0f}"'
          f' fill="{col}" stroke="{K}" stroke-width="{3.4*s_:.1f}"/>')
    s += (f'<circle cx="{x:.0f}" cy="{y-92*s_:.0f}" r="{27*s_:.0f}" fill="{col}"'
          f' stroke="{K}" stroke-width="{3.4*s_:.1f}"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*16*s_:.0f},{y-112*s_:.0f} q{i*6*s_:.0f},{-18*s_:.0f}'
              f' {i*14*s_:.0f},{-22*s_:.0f} q{-i*2*s_:.0f},{14*s_:.0f} {-i*8*s_:.0f},{22*s_:.0f} Z"'
              f' fill="#c8a05a" stroke="{K}" stroke-width="{2.4*s_:.1f}"/>')
        s += (f'<circle cx="{x+i*9*s_:.0f}" cy="{y-96*s_:.0f}" r="{5*s_:.1f}"'
              f' fill="#ffe9ac"/>')
    s += (f'<path d="M{x-9*s_:.0f},{y-82*s_:.0f} q{9*s_:.0f},{9*s_:.0f} {18*s_:.0f},0"'
          f' fill="none" stroke="#f4d6a0" stroke-width="{2.6*s_:.1f}"/>')
    hv = 10 * s_ * A.w(t, 1.4, ph + .3)
    s += (f'<path d="M{x+26*s_:.0f},{y-44*s_:.0f} q{34*s_:.0f},{hv:.0f}'
          f' {30*s_:.0f},{-34*s_:.0f}" fill="none" stroke="{col}"'
          f' stroke-width="{4.4*s_:.1f}"/>')
    s += (f'<path d="M{x+54*s_:.0f},{y-82*s_:.0f} l{12*s_:.0f},{-10*s_:.0f}'
          f' l{2*s_:.0f},{16*s_:.0f} Z" fill="#c8a05a" stroke="{K}"'
          f' stroke-width="{2.2*s_:.1f}"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*14*s_:.0f},{y-14*s_:.0f} l{i*6*s_:.0f},{16*s_:.0f}"'
              f' stroke="{col}" stroke-width="{7*s_:.1f}" stroke-linecap="round"/>')
    return s + '</g>'


def yaschik_rybaka(x, y, s_=1.0, t=0.0, otkryt=.0, ph=.0):
    """Дедов рыбацкий ящик: деревянный, с ремнём, крышка приоткрыта на
    otkryt 0..1, внутри мотовило, блёсны, коробочка."""
    w_, h_ = 180 * s_, 120 * s_
    s = (f'<rect x="{x-w_*.5:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="{8*s_:.0f}" fill="url(#derev)" stroke="{K}" stroke-width="{4.4*s_:.1f}"/>')
    for i in range(3):
        s += (f'<path d="M{x-w_*.5+6*s_:.0f},{y-h_+22*s_+i*32*s_:.0f} h{w_-12*s_:.0f}"'
              f' stroke="#6b4428" stroke-width="{3*s_:.1f}" opacity=".7"/>')
    ug = -52 * otkryt
    s += (f'<g transform="rotate({ug:.0f} {x-w_*.5:.0f} {y-h_:.0f})">'
          f'<rect x="{x-w_*.5:.0f}" y="{y-h_-18*s_:.0f}" width="{w_:.0f}"'
          f' height="{20*s_:.0f}" rx="{5*s_:.0f}" fill="{DOSKA}" stroke="{K}"'
          f' stroke-width="{3.6*s_:.1f}"/></g>')
    if otkryt > .3:
        s += (f'<rect x="{x-w_*.34:.0f}" y="{y-h_+8*s_:.0f}" width="{48*s_:.0f}"'
              f' height="{26*s_:.0f}" rx="{4*s_:.0f}" fill="#8a6342" stroke="{K}"'
              f' stroke-width="{2.6*s_:.1f}"/>')
        for i in range(3):
            s += (f'<path d="M{x+6*s_+i*22*s_:.0f},{y-h_+10*s_:.0f} l{6*s_:.0f},{22*s_:.0f}'
                  f' l{-12*s_:.0f},0 Z" fill="#c9ccd1" stroke="{K}" stroke-width="{2.2*s_:.1f}"/>')
    s += (f'<path d="M{x-w_*.5:.0f},{y-h_*.62:.0f} q{w_*.5:.0f},{-54*s_:.0f}'
          f' {w_:.0f},0" fill="none" stroke="#6b5230" stroke-width="{7*s_:.1f}"/>')
    s += (f'<rect x="{x+w_*.30:.0f}" y="{y-h_*.52:.0f}" width="{22*s_:.0f}"'
          f' height="{16*s_:.0f}" rx="{3*s_:.0f}" fill="{MED}" stroke="{K}"'
          f' stroke-width="{2.4*s_:.1f}"/>')
    s += ten(x, y + 5 * s_, w_ * .56, 14 * s_, .45)
    return s


def ledobur(x, y, s_=1.0, t=0.0, ph=.0):
    """Ледобур: шнек витком, ножи снизу, коленчатая ручка."""
    s = (f'<rect x="{x-7*s_:.0f}" y="{y-250*s_:.0f}" width="{14*s_:.0f}"'
         f' height="{250*s_:.0f}" fill="{ZHELEZ}" stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    for i in range(9):
        yy = y - 30 * s_ - i * 22 * s_
        s += (f'<path d="M{x-24*s_:.0f},{yy:.0f} q{24*s_:.0f},{-14*s_:.0f}'
              f' {48*s_:.0f},0 q{-24*s_:.0f},{14*s_:.0f} {-48*s_:.0f},0 Z"'
              f' fill="#8f979f" stroke="{K}" stroke-width="{2.2*s_:.1f}"/>')
    s += (f'<path d="M{x-26*s_:.0f},{y-12*s_:.0f} h{52*s_:.0f} l{-10*s_:.0f},{14*s_:.0f}'
          f' h{-32*s_:.0f} Z" fill="#c9ccd1" stroke="{K}" stroke-width="{2.8*s_:.1f}"/>')
    s += (f'<path d="M{x:.0f},{y-250*s_:.0f} h{60*s_:.0f} l0,{36*s_:.0f}"'
          f' fill="none" stroke="{ZHELEZ}" stroke-width="{9*s_:.1f}"/>')
    s += (f'<rect x="{x+52*s_:.0f}" y="{y-216*s_:.0f}" width="{17*s_:.0f}"'
          f' height="{44*s_:.0f}" rx="{6*s_:.0f}" fill="#8a2f22" stroke="{K}"'
          f' stroke-width="{2.6*s_:.1f}"/>')
    return s


# ═══ из chast1.py ═══
def _merzlaya_zemlya(y0, seed=3, luzhi=True):
    """Мёрзлая земля ноября: бурая, с комьями, схваченной колеёй и инеем."""
    rnd = random.Random(seed * 17 + 1)
    s = (f'<rect x="0" y="{y0:.0f}" width="{W}" height="{H-y0:.0f}" fill="#4a3a2a"/>')
    s += (f'<path d="M-40,{H} Q420,{y0+180:.0f} 760,{y0+40:.0f} L1240,{y0+40:.0f}'
          f' Q1520,{y0+180:.0f} 1960,{H} Z" fill="#5f4a32" opacity=".95"/>')
    for i in range(26):
        kx, ky = rnd.uniform(-40, 1960), rnd.uniform(y0 + 20, H - 10)
        s += (f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="{rnd.uniform(14,46):.0f}"'
              f' ry="{rnd.uniform(5,15):.0f}" fill="#3f3122"'
              f' opacity="{rnd.uniform(.35,.75):.2f}"/>')
    for i in range(9):
        gy = rnd.uniform(y0 + 40, H - 20)
        s += (f'<path d="M{rnd.uniform(-60,400):.0f},{gy:.0f}'
              f' Q{rnd.uniform(700,1200):.0f},{gy+rnd.uniform(-22,22):.0f}'
              f' {rnd.uniform(1500,1980):.0f},{gy+rnd.uniform(-14,14):.0f}" fill="none"'
              f' stroke="#6b5438" stroke-width="{rnd.uniform(4,12):.1f}" opacity=".5"/>')
    if luzhi:
        for i in range(3):
            lx, ly = rnd.uniform(120, 1800), rnd.uniform(y0 + 70, H - 40)
            s += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rnd.uniform(40,86):.0f}"'
                  f' ry="{rnd.uniform(12,24):.0f}" fill="#9fc4d8" opacity=".55"/>')
    s += inej_mel(seed + 4, 44, y0 + 20, H - 6)
    return s


def _trava_suhaya(rnd, n, y0, y1, x0=0, x1=W):
    """Сухой бурьян по кромке: пучки разной высоты, чуть качаются."""
    s = ""
    for i in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        for k in range(rnd.randint(3, 6)):
            hh = rnd.uniform(18, 54)
            s += (f'<path d="M{x:.0f},{y:.0f} q{rnd.uniform(-10,10):.0f},{-hh*.6:.0f}'
                  f' {rnd.uniform(-16,16):.0f},{-hh:.0f}" fill="none" stroke="#8a7a4e"'
                  f' stroke-width="{rnd.uniform(1.8,3.2):.1f}" opacity="{rnd.uniform(.5,.9):.2f}"/>')
    return s


def _petuh(x, y, t, s_=1.0, ph=.0):
    """Петух на калитке: гребень, бородка, хвост косицами, тянет шею."""
    shea = 16 * s_ * A.ease(abs(A.w(t, 2.4, ph)))
    s = (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{54*s_:.0f}" ry="{40*s_:.0f}"'
         f' fill="#8d4a2a" stroke="{K}" stroke-width="{3.4*s_:.1f}"/>')
    s += (f'<path d="M{x-46*s_:.0f},{y+6*s_:.0f} q{-54*s_:.0f},{-30*s_:.0f}'
          f' {-30*s_:.0f},{-66*s_:.0f} q{30*s_:.0f},{20*s_:.0f} {24*s_:.0f},{58*s_:.0f} Z"'
          f' fill="#5e2f1a" stroke="{K}" stroke-width="{2.8*s_:.1f}"/>')
    for i in range(3):
        s += (f'<path d="M{x-40*s_:.0f},{y+2*s_:.0f} q{-56*s_-i*10*s_:.0f},{-26*s_-i*18*s_:.0f}'
              f' {-40*s_-i*22*s_:.0f},{-72*s_-i*14*s_:.0f}" fill="none" stroke="#7d3f22"'
              f' stroke-width="{5*s_:.1f}"/>')
    s += (f'<path d="M{x+32*s_:.0f},{y-20*s_:.0f} q{18*s_+shea:.0f},{-20*s_-shea:.0f}'
          f' {20*s_+shea:.0f},{-50*s_-shea:.0f} l{-26*s_:.0f},{-2*s_:.0f}'
          f' q{-2*s_:.0f},{26*s_:.0f} {-18*s_:.0f},{44*s_:.0f} Z" fill="#9c5630"'
          f' stroke="{K}" stroke-width="{2.8*s_:.1f}"/>')
    gx, gy = x + 34 * s_ + shea, y - 66 * s_ - shea
    s += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="{21*s_:.0f}" fill="#a85c33"'
          f' stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    for i in range(3):
        s += (f'<path d="M{gx-10*s_+i*9*s_:.0f},{gy-18*s_:.0f} q{5*s_:.0f},{-16*s_:.0f}'
              f' {11*s_:.0f},{-2*s_:.0f} Z" fill="#c8301f" stroke="{K}" stroke-width="{2*s_:.1f}"/>')
    s += (f'<path d="M{gx+18*s_:.0f},{gy+2*s_:.0f} l{20*s_:.0f},{6*s_:.0f}'
          f' l{-20*s_:.0f},{7*s_:.0f} Z" fill="{ZOL}" stroke="{K}" stroke-width="{2*s_:.1f}"/>')
    s += (f'<ellipse cx="{gx+4*s_:.0f}" cy="{gy+22*s_:.0f}" rx="{7*s_:.0f}" ry="{12*s_:.0f}"'
          f' fill="#c8301f" stroke="{K}" stroke-width="{2*s_:.1f}"/>')
    s += (f'<circle cx="{gx+8*s_:.0f}" cy="{gy-4*s_:.0f}" r="{3.6*s_:.1f}" fill="{K}"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*12*s_:.0f},{y+36*s_:.0f} l{i*4*s_:.0f},{22*s_:.0f}"'
              f' stroke="{ZOL}" stroke-width="{4.4*s_:.1f}"/>')
    return s


def _ramka_lubok(x, y, w_, h_, col="#8a6342"):
    """Рамка «картинки в ряд»: тёсаная доска с уголками — внутри вид."""
    s = (f'<rect x="{x-10:.0f}" y="{y-10:.0f}" width="{w_+20:.0f}" height="{h_+20:.0f}"'
         f' rx="8" fill="{col}" stroke="{K}" stroke-width="5"/>')
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' fill="#2b3550" stroke="{K}" stroke-width="3"/>')
    for ax, ay in ((x - 6, y - 6), (x + w_ - 20, y - 6),
                   (x - 6, y + h_ - 20), (x + w_ - 20, y + h_ - 20)):
        s += (f'<rect x="{ax:.0f}" y="{ay:.0f}" width="26" height="26" rx="5"'
              f' fill="{MED}" stroke="{K}" stroke-width="2.6"/>')
    return s


def _cherta_zapreta(cx, cy, r, t, ph=.0, w_=16):
    """Красная запрещающая черта: круг и косая, встаёт рывком."""
    k = A.out(A.seg(t, .3 + ph, .5))
    if k <= .01:
        return ""
    s = (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*k:.0f}" fill="none"'
         f' stroke="#d6452a" stroke-width="{w_:.0f}" opacity=".92"/>')
    s += (f'<line x1="{cx-r*.72*k:.0f}" y1="{cy+r*.72*k:.0f}" x2="{cx+r*.72*k:.0f}"'
          f' y2="{cy-r*.72*k:.0f}" stroke="#d6452a" stroke-width="{w_:.0f}"'
          f' opacity=".92"/>')
    return s


def _valenok(x, y, s_=1.0, ug=0.0, col="#6f6256"):
    """Валенок: голенище, толстая подошва, заплата — узнаётся силуэтом."""
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x-30*s_:.0f},{y-130*s_:.0f} h{58*s_:.0f} q{14*s_:.0f},{66*s_:.0f}'
         f' {10*s_:.0f},{96*s_:.0f} q{26*s_:.0f},{6*s_:.0f} {30*s_:.0f},{26*s_:.0f}'
         f' l{-124*s_:.0f},0 q{-12*s_:.0f},{-52*s_:.0f}'
         f' {8*s_:.0f},{-104*s_:.0f} Z" fill="{col}" stroke="{K}"'
         f' stroke-width="{3.8*s_:.1f}"/>'
         f'<path d="M{x-33*s_:.0f},{y-134*s_:.0f} h{64*s_:.0f} q{6*s_:.0f},{16*s_:.0f}'
         f' {-2*s_:.0f},{26*s_:.0f} h{-60*s_:.0f} q{-6*s_:.0f},{-12*s_:.0f}'
         f' {-2*s_:.0f},{-26*s_:.0f} Z" fill="#8a8078" opacity=".55"/>')
    s += (f'<path d="M{x-40*s_:.0f},{y-26*s_:.0f} h{84*s_:.0f} q{12*s_:.0f},{10*s_:.0f}'
          f' {2*s_:.0f},{26*s_:.0f} l{-92*s_:.0f},0 Z" fill="#4a4038" stroke="{K}"'
          f' stroke-width="{3.2*s_:.1f}"/>')
    s += (f'<path d="M{x-28*s_:.0f},{y-124*s_:.0f} h{54*s_:.0f}" stroke="#55493f"'
          f' stroke-width="{5*s_:.1f}"/>')
    s += (f'<ellipse cx="{x+14*s_:.0f}" cy="{y-70*s_:.0f}" rx="{13*s_:.0f}"'
          f' ry="{17*s_:.0f}" fill="#7d7066" opacity=".8" stroke="{K}"'
          f' stroke-width="{2*s_:.1f}"/>')
    return s + '</g>'


# ── ДЕКОРАЦИИ ──────────────────────────────────────────────────────────────

def luzha_u_kalitki_pod_pervoy_korkoy(t):
    """Калитка двора морозным утром, перед ней большая лужа: её овал — проём
    с настоящим первым льдом. Мальчик занёс над лужей ногу, бабушка держит
    его за хлястик. Петух на калитке тянет шею."""
    rnd = random.Random(1901)
    gor = 430
    s = nebo("rassv", t, False, 19)
    s += oblaka(t, 150, 5, 11, .40)
    s += SL(Z_DAL, izba_snaruzhi(250, gor + 40, 330, t, True, True, 5)
            + dym(286, gor - 210, t, 6, .24, 300, .42, "#d7dee6", 1.0))
    s += SL(Z_DAL, ulica_dal(1180, gor + 30, 760, t, True, 9))
    s += SL(Z_DAL, goloe_derevo_ld(1620, gor + 46, 380, t, 7, 6, True))
    s += SL(Z_DAL, zabor_shtaket(-30, gor - 110, 760, 190, 5, 58)
            + zabor_shtaket(1190, gor - 96, 760, 176, 8, 60))
    s += SL(Z_SRED, _merzlaya_zemlya(gor + 20, 4, False))
    s += SL(Z_SRED, kalitka_rez(812, gor - 150, 300, 350, t, .10, True))
    s += SL(Z_SRED, ryabina(1468, gor + 140, t, 1.5, 6)
            + kalina_grozd(1510, gor + 60, t, 1.15, 12, 6, .3))

    # ЛУЖА: сначала рисованный вид, потом метка, потом кромка поверх
    lx, ly, lw, lh = 700, 712, 520, 360
    luzha = (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.56:.0f}"'
             f' ry="{lh*.56:.0f}" fill="#2f4a52"/>')
    luzha += korka_lda(lx + lw * .5, ly + lh * .5, lw * .50, lh * .48, t, .1, .0, .9)
    luzha += mesto_stoka(lx, ly, lw, lh, "ellips")
    luzha += (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.56:.0f}"'
              f' ry="{lh*.56:.0f}" fill="none" stroke="#6b5438" stroke-width="18"'
              f' opacity=".85"/>')
    luzha += (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.60:.0f}"'
              f' ry="{lh*.60:.0f}" fill="none" stroke="{INEY}" stroke-width="9"'
              f' opacity=".55"/>')
    luzha += _trava_suhaya(rnd, 7, ly + lh * .72, ly + lh + 30, lx - 40, lx + lw + 40)
    s += SL(Z_SRED, luzha)

    # МАЛЬЧИК: стоит на мёрзлой земле у края лужи, заносит правую ногу
    mx, my, mh = 520, 1012, 560
    noga = A.ease(A.seg(t, .4, 1.1))
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f4a6a", kant="#cfe4f5",
                           shapka=True, ph=.1))
    rk1, (e1x, e1y), _ = _ruka(mx, my, mh, -1, mh * .30, 18, t, "#3f4a6a", "#cfe4f5", .2, 7)
    rk2, (e2x, e2y), _ = _ruka(mx, my, mh, 1, mh * .30, 14, t, "#3f4a6a", "#cfe4f5", .5, 7)
    s += SL(Z_SRED, rk1 + varezhka(e1x - 10, e1y + 10, .9, -18, TKAN, t, .2)
            + rk2 + varezhka(e2x + 10, e2y + 10, .9, 16, TKAN, t, .6))
    s += SL(Z_SRED, _valenok(mx + 96 + 54 * noga, my - 36 - 74 * noga, .62, 16 + 14 * noga)
            + f'<path d="M{mx+40:.0f},{my-70:.0f} q{60*noga:.0f},{-40*noga:.0f}'
              f' {104*noga:.0f},{-54*noga:.0f}" fill="none" stroke="#3f4a6a"'
              f' stroke-width="26" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(mx + 34, my - mh * .80, t, .2, .9, .55))

    # БАБУШКА: за ним, правой держит хлястик, в левой ведро
    bx, by, bh = 356, 1046, 650
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.45))
    rk3, (e3x, e3y), _ = _ruka(bx, by, bh, 1, bh * .34, 26, t, "#4a3a52", "#cfe4f5", .3, 5)
    s += SL(Z_SRED, rk3 + f'<path d="M{e3x:.0f},{e3y:.0f} L{mx-70:.0f},{my-mh*.52:.0f}"'
                          f' stroke="#4a3a52" stroke-width="16" stroke-linecap="round"/>')
    rk4, (e4x, e4y), _ = _ruka(bx, by, bh, -1, bh * .30, 58, t, "#4a3a52", "#cfe4f5", .7, 4)
    kach = 5 * A.w(t, 1.5, .2)
    s += SL(Z_SRED, rk4
            + f'<g transform="rotate({kach:.1f} {e4x:.0f} {e4y:.0f})">'
              f'<path d="M{e4x-36:.0f},{e4y+10:.0f} h72 l-8,86 h-56 Z" fill="{ZHELEZ}"'
              f' stroke="{K}" stroke-width="4"/>'
              f'<ellipse cx="{e4x:.0f}" cy="{e4y+10:.0f}" rx="36" ry="11" fill="#8f979f"'
              f' stroke="{K}" stroke-width="3.4"/>'
              f'<path d="M{e4x-36:.0f},{e4y+6:.0f} q{36:.0f},{-34:.0f} {72:.0f},0"'
              f' fill="none" stroke="{CHUGUN}" stroke-width="5"/></g>')
    s += SL(Z_SRED, para_izo_rta(bx - 30, by - bh * .80, t, .6, 1.0, .5))
    s += SL(Z_SRED, ten(mx, my + 6, 120, 22, .45) + ten(bx, by + 6, 140, 24, .45))

    s += SL(Z_SRED, lavka(1240, 940, 300) + dvorovye_veschi(1300, 1066, 420, t, 12,
                                                            ["kadka", "churbak", "korzina"]))
    s += SL(Z_SRED, sledy_valenok(1860, 1066, 1180, 860, 6, 5, "#352a1c", 1.2))
    s += SL(Z_PERED, _petuh(900, gor - 196, t, 1.0, .2))
    s += SL(Z_PERED, goloe_derevo_ld(90, 1080, 560, t, 3, 5, True))
    s += ramka_pp("oba", "#0e0c0b", .55)
    s += vinetka(.40)
    return s


def tri_lda_prud_ozero_luzha(t):
    """Три картинки в ряд: пруд с мостками, озеро с вмёрзшей лодкой, лужа с
    кленовым листом. Над каждой встаёт красная черта, валенок заносится и
    отдёргивается. Людей нет."""
    rnd = random.Random(1902)
    s = nebo("sumer", t, True, 23)
    s += oblaka(t, 130, 6, 17, .38)
    s += SL(Z_DAL, ulica_dal(60, 470, 860, t, True, 13))
    s += SL(Z_DAL, izba_snaruzhi(1520, 500, 300, t, True, True, 8)
            + dym(1552, 300, t, 6, .22, 280, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(560, 6, True))

    # три «картинки»: вид внутри рамки
    for i, vid in enumerate(("prud", "ozero", "luzha")):
        x = 120 + i * 580
        y = 300
        w_, h_ = 500, 340
        s += SL(Z_SRED, _ramka_lubok(x, y, w_, h_))
        kus = ""
        if vid == "prud":
            kus += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_*.52:.0f}"'
                    f' fill="url(#nsumer)"/>')
            kus += (f'<rect x="{x:.0f}" y="{y+h_*.52:.0f}" width="{w_:.0f}"'
                    f' height="{h_*.48:.0f}" fill="url(#led)"/>')
            kus += korka_lda(x + w_ * .5, y + h_ * .74, w_ * .44, h_ * .20, t, .1)
            kus += mostki(x + 40, y + h_ * .62, 230, t, True, 60)
            kus += goloe_derevo_ld(x + w_ - 90, y + h_ * .56, 170, t, 9, 5, True)
            kus += kamysh(x + w_ - 44, y + h_ * .70, 70, t, 4, 3, True)
        elif vid == "ozero":
            kus += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_*.40:.0f}"'
                    f' fill="url(#nsumer)"/>')
            kus += (f'<rect x="{x:.0f}" y="{y+h_*.40:.0f}" width="{w_:.0f}"'
                    f' height="{h_*.60:.0f}" fill="#b9d6e8"/>')
            kus += treschina(x + w_ * .55, y + h_ * .70, 170, 11, 5)
            # лодка, вмёрзшая у берега
            kus += (f'<path d="M{x+90:.0f},{y+h_*.70:.0f} q{60:.0f},{44:.0f} {170:.0f},{10:.0f}'
                    f' q{-20:.0f},{-30:.0f} {-170:.0f},{-10:.0f} Z" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="4"/>')
            kus += (f'<path d="M{x+120:.0f},{y+h_*.70:.0f} l{-26:.0f},{-54:.0f}"'
                    f' stroke="#8a6342" stroke-width="7" fill="none"/>')
            kus += (f'<ellipse cx="{x+176:.0f}" cy="{y+h_*.78:.0f}" rx="96" ry="16"'
                    f' fill="{INEY}" opacity=".6"/>')
            kus += kamysh(x + 54, y + h_ * .60, 92, t, 5, 7, True)
        else:
            kus += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
                    f' fill="#5f4a32"/>')
            kus += (f'<path d="M{x:.0f},{y+h_*.66:.0f} q{w_*.5:.0f},{-30:.0f} {w_:.0f},{10:.0f}'
                    f' l0,{h_*.34:.0f} l{-w_:.0f},0 Z" fill="#4a3a2a"/>')
            kus += korka_lda(x + w_ * .5, y + h_ * .60, w_ * .36, h_ * .22, t, .4)
            # вмёрзший кленовый лист
            kus += (f'<path d="M{x+w_*.5:.0f},{y+h_*.52:.0f} l{34:.0f},{-26:.0f}'
                    f' l{-8:.0f},{26:.0f} l{34:.0f},{-6:.0f} l{-26:.0f},{24:.0f}'
                    f' l{22:.0f},{18:.0f} l{-34:.0f},{2:.0f} l{-4:.0f},{26:.0f}'
                    f' l{-22:.0f},{-20:.0f} l{-28:.0f},{14:.0f} l{10:.0f},{-28:.0f}'
                    f' l{-30:.0f},{-6:.0f} Z" fill="#9a5a28" stroke="#7d4a24"'
                    f' stroke-width="3"/>')
            kus += inej_mel(13, 16, y + h_ * .40, y + h_ * .92, x + 20, x + w_ - 20)
        s += SL(Z_SRED, kus)
        # валенок заносится над картинкой и отдёргивается
        faza = (t * .9 + i * .33) % 1.0
        pod = A.ease(min(1.0, faza * 2.2)) - A.ease(max(.0, faza * 2.2 - 1.1))
        s += SL(Z_PERED, _valenok(x + w_ * .5, y - 40 - 80 * pod, .78, -8 + 10 * pod))
        s += SL(Z_PERED, _cherta_zapreta(x + w_ * .5, y + h_ * .5, 150, t, i * .22, 15))

    s += SL(Z_SRED, kamysh(1870, 700, 180, t, 6, 19, True)
            + kamysh(40, 740, 150, t, 5, 21, True))
    # колодец с журавлём и корзина — обжитой низ кадра
    s += SL(Z_SRED, f'<rect x="760" y="880" width="260" height="120" rx="10"'
                    f' fill="{KAMEN}" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="890" cy="880" rx="130" ry="26" fill="{KAMEN2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1000,880 L1060,660" stroke="#6b4428" stroke-width="14"'
                    f' fill="none"/>'
                    f'<path d="M1060,660 L820,700" stroke="#6b4428" stroke-width="11"'
                    f' fill="none"/>'
                    f'<path d="M846,700 l6,80" stroke="#b9a37a" stroke-width="5"'
                    f' fill="none"/>'
                    f'<path d="M826,780 h52 l-6,44 h-40 Z" fill="{ZHELEZ}" stroke="{K}"'
                    f' stroke-width="3.4"/>')
    s += SL(Z_SRED, dvorovye_veschi(180, 1060, 420, t, 15, ["korzina", "vedro", "koryto"]))
    for i, (ux, uy) in enumerate(((1310, 1012), (1390, 1030), (1466, 1008))):
        s += SL(Z_SRED, ptica(ux, uy, t, 1.5, "#4a4038", i * .3, "#5b6a78"))
    s += SL(Z_LETIT, sneg_letit(t, 26, 9, .55, .7))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def slomannyy_led_i_pustoy_zakrom(t):
    """Озорник убегает от проломленной лужи, от пролома через двор к амбару
    бежит чёрная дорожка: в амбаре пустеют закрома, худеет мешок. У амбара
    стоит семья — отец со снятой шапкой, мать, дед на палке."""
    rnd = random.Random(1903)
    gor = 400
    s = nebo("den", t, False, 29)
    s += oblaka(t, 120, 5, 23, .45)
    s += SL(Z_DAL, ulica_dal(40, gor + 10, 700, t, True, 17))
    s += SL(Z_DAL, goloe_derevo_ld(680, gor + 24, 320, t, 11, 6, True))
    s += SL(Z_SRED, _merzlaya_zemlya(gor + 18, 7, False))

    # АМБАР справа: раскрытые ворота, закрома, полка с караваями, мешок
    ax, ay, aw, ah = 1120, 300, 700, 540
    amb = (f'<rect x="{ax:.0f}" y="{ay:.0f}" width="{aw:.0f}" height="{ah:.0f}"'
           f' fill="#4a3526" stroke="{K}" stroke-width="6"/>')
    amb += (f'<path d="M{ax-50:.0f},{ay:.0f} L{ax+aw*.5:.0f},{ay-170:.0f}'
            f' L{ax+aw+50:.0f},{ay:.0f} Z" fill="#5e4430" stroke="{K}" stroke-width="6"/>')
    amb += (f'<path d="M{ax-50:.0f},{ay:.0f} L{ax+aw*.5:.0f},{ay-170:.0f}'
            f' L{ax+aw+50:.0f},{ay:.0f}" fill="none" stroke="url(#sneg)" stroke-width="16"'
            f' opacity=".9"/>')
    amb += doski(ax + 40, ay + 40, aw - 80, ah - 60, 64, True)
    s += SL(Z_DAL, amb)
    # пустеющие закрома: уровень зерна падает, караваи исчезают по очереди
    uh = A.ease(A.seg(t, .5, 2.6))
    zak = ""
    for i in range(3):
        zx = ax + 70 + i * 200
        zak += (f'<rect x="{zx:.0f}" y="{ay+250:.0f}" width="160" height="190" rx="8"'
                f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
        hh = 120 * (1 - uh * (.55 + i * .15))
        zak += (f'<rect x="{zx+12:.0f}" y="{ay+430-hh:.0f}" width="136" height="{hh:.0f}"'
                f' fill="#c8a05a" opacity=".95"/>')
        zak += (f'<ellipse cx="{zx+80:.0f}" cy="{ay+430-hh:.0f}" rx="68" ry="13"'
                f' fill="#dbb771"/>')
    s += SL(Z_SRED, zak)
    pol = polka(ax + 90, ay + 170, 520)
    for i in range(4):
        if uh * 4 < 3 - i + .6:
            pol += karavay(ax + 150 + i * 140, ay + 168, .62, i % 2 == 0)
    s += SL(Z_SRED, pol)
    msh = 1 - .45 * uh
    s += SL(Z_SRED, f'<path d="M{ax+560:.0f},{ay+440:.0f} q{-30*msh:.0f},{-150*msh:.0f}'
                    f' {40*msh:.0f},{-190*msh:.0f} q{70*msh:.0f},{40*msh:.0f}'
                    f' {40*msh:.0f},{190*msh:.0f} Z" fill="#b9a37a" stroke="{K}"'
                    f' stroke-width="4.5"/>'
                    f'<path d="M{ax+590:.0f},{ay+260:.0f} q{20:.0f},{-26:.0f} {42:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#8a7a52" stroke-width="6"/>')

    # ПРОЛОМЛЕННАЯ ЛУЖА слева и чёрная дорожка от неё к амбару
    s += SL(Z_SRED, korka_lda(300, 940, 210, 96, t, .2, .95))
    beg = A.ease(A.seg(t, .3, 2.2))
    put = f'M320,960'
    for i in range(1, 9):
        p = i / 8.0
        put += f' Q{320+ (ax-320)*p - 60:.0f},{960 - 150*math.sin(p*3.14):.0f} {320 + (ax+120-320)*p:.0f},{950 - 240*p:.0f}'
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#17120d" stroke-width="22"'
                    f' opacity=".75" stroke-dasharray="{2400*beg:.0f} 4000"/>')

    # ОЗОРНИК убегает влево, обе руки машут, шарф летит
    bx, by, bh = 470, 1012, 470
    beg2 = A.ease(A.seg(t, .2, 1.8))
    bx -= 120 * beg2
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#6b3a2a", kant="#ffd9a8",
                           shapka=True, ph=.1, naklon=4.0))
    r1, (q1x, q1y), _ = _ruka(bx, by, bh, -1, bh * .32, -36, t, "#6b3a2a", "#ffd9a8", .1, 16)
    r2, (q2x, q2y), _ = _ruka(bx, by, bh, 1, bh * .32, 46, t, "#6b3a2a", "#ffd9a8", .5, 16)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{bx+30:.0f},{by-bh*.62:.0f} q{90:.0f},{10+14*A.w(t,.8,.2):.0f}'
                    f' {170:.0f},{-20:.0f} l{6:.0f},{34:.0f} q{-86:.0f},{26:.0f}'
                    f' {-176:.0f},{14:.0f} Z" fill="{TKAN}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, para_izo_rta(bx - 40, by - bh * .80, t, .3, .9, .5))

    # СЕМЬЯ у амбара: отец со снятой шапкой, мать, дед на палке, ребёнок
    ox, oy, oh = 980, 1040, 540
    s += SL(Z_SRED, figura(ox, oy, oh, t, col="#3f3a4a", kant="#ffd9a8", ph=.2, boroda=True))
    r3, (e3x, e3y), _ = _ruka(ox, oy, oh, 1, oh * .26, 54, t, "#3f3a4a", "#ffd9a8", .2, 3)
    s += SL(Z_SRED, r3 + f'<ellipse cx="{e3x+14:.0f}" cy="{e3y+18:.0f}" rx="44" ry="26"'
                         f' fill="#4a3a2c" stroke="{K}" stroke-width="4"/>'
                         f'<ellipse cx="{e3x+14:.0f}" cy="{e3y+8:.0f}" rx="44" ry="13"'
                         f' fill="#8a6a4a" stroke="{K}" stroke-width="3"/>')
    mx2, my2, mh2 = 820, 1052, 520
    s += SL(Z_SRED, figura(mx2, my2, mh2, t, col="#5a3a4a", kant="#ffd9a8",
                           platok=True, ph=.5))
    r4, _, _ = _ruka(mx2, my2, mh2, 1, mh2 * .22, 70, t, "#5a3a4a", "#ffd9a8", .4, 4)
    s += SL(Z_SRED, r4)
    dx, dy, dh = 1120, 1066, 520
    kach = 3.0 * A.w(t, 2.2, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {dx:.0f} {dy:.0f})">'
            + figura(dx, dy, dh, t, col="#4a443c", kant="#ffd9a8", boroda=True, ph=.8)
            + '</g>')
    r5, (e5x, e5y), _ = _ruka(dx, dy, dh, 1, dh * .30, 62, t, "#4a443c", "#ffd9a8", .6, 3)
    s += SL(Z_SRED, r5 + f'<path d="M{e5x:.0f},{e5y-20:.0f} l{18:.0f},{dy-e5y+16:.0f}"'
                         f' stroke="#7d5636" stroke-width="12" stroke-linecap="round"/>')
    s += SL(Z_SRED, ten(ox, oy + 6, 110, 20, .4) + ten(mx2, my2 + 6, 104, 19, .4)
            + ten(dx, dy + 6, 110, 20, .4) + ten(bx, by + 6, 96, 18, .4))

    # двор: телега, корыто, ворота, собака
    s += SL(Z_SRED, f'<rect x="580" y="820" width="300" height="34" rx="6" fill="{DOSKA}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="640" cy="900" r="54" fill="none" stroke="#6b4428"'
                    f' stroke-width="13"/>'
                    f'<circle cx="830" cy="900" r="54" fill="none" stroke="#6b4428"'
                    f' stroke-width="13"/>'
                    f'<path d="M580,838 L470,790" stroke="#7d5636" stroke-width="10"'
                    f' fill="none"/>')
    s += SL(Z_SRED, dvorovye_veschi(120, 1066, 420, t, 19, ["koryto", "grabli", "churbak"]))
    s += SL(Z_SRED, kot(700, 1044, t, 1.4, "#55493f", False))
    s += SL(Z_SRED, sledy_valenok(640, 1070, 300, 962, 6, 9, "#352a1c", 1.1))
    s += SL(Z_PERED, zabor_shtaket(-40, 880, 420, 200, 13, 56))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def prud_pod_pervym_ldom(t):
    """Пруд на рассвете под первым льдом: под прозрачным льдом спит сама
    Вода — девица с длинными волосами под ледяным одеялом, рядом дремлют
    карась и лягушка. В окне избы на берегу — настоящий замёрзший пруд."""
    rnd = random.Random(1904)
    gor = 430
    s = nebo("rassv", t, False, 31)
    s += oblaka(t, 140, 5, 29, .40)
    s += SL(Z_DAL, goloe_derevo_ld(300, gor + 30, 420, t, 13, 7, True))
    s += SL(Z_DAL, f'<path d="M120,{gor+20:.0f} q60,-180 180,-210 q-40,120 -40,210 Z"'
                   f' fill="#4a4a3a" opacity=".8"/>')
    # баня с дымом на дальнем берегу
    s += SL(Z_DAL, izba_snaruzhi(1660, gor + 16, 250, t, True, True, 11)
            + dym(1686, gor - 150, t, 6, .22, 260, .40, "#d7dee6", .9))

    # ИЗБА НА БЕРЕГУ с окном-проёмом (справа сверху)
    ix, iy, iw, ih = 1020, 150, 880, 470
    izba = (f'<rect x="{ix:.0f}" y="{iy:.0f}" width="{iw:.0f}" height="{ih:.0f}"'
            f' fill="#5e4430" stroke="{K}" stroke-width="6"/>')
    izba += brevna(ix, iy, iw, ih, 82, 1)
    izba += (f'<path d="M{ix-60:.0f},{iy:.0f} L{ix+iw*.5:.0f},{iy-160:.0f}'
             f' L{ix+iw+60:.0f},{iy:.0f} Z" fill="#4a3526" stroke="{K}" stroke-width="6"/>')
    izba += (f'<path d="M{ix-60:.0f},{iy:.0f} L{ix+iw*.5:.0f},{iy-160:.0f}'
             f' L{ix+iw+60:.0f},{iy:.0f}" fill="none" stroke="url(#sneg)"'
             f' stroke-width="18" opacity=".92"/>')
    s += SL(Z_DAL, izba)
    px, py, pw, ph_ = 1120, 230, 780, 320
    okno = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
            f' fill="#9fc4d8"/>')
    okno += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.45:.0f}"'
             f' fill="#c4d8e8"/>')
    okno += mesto_stoka(px, py, pw, ph_, "pryam")
    okno += (f'<rect x="{px-16:.0f}" y="{py-16:.0f}" width="{pw+32:.0f}"'
             f' height="{ph_+32:.0f}" rx="6" fill="none" stroke="#6b4428"'
             f' stroke-width="26"/>')
    okno += (f'<path d="M{px+pw*.5:.0f},{py:.0f} l0,{ph_:.0f} M{px:.0f},{py+ph_*.5:.0f}'
             f' l{pw:.0f},0" stroke="#6b4428" stroke-width="16"/>')
    okno += (f'<path d="M{px+20:.0f},{py+ph_-24:.0f} q{pw*.2:.0f},{-40:.0f}'
             f' {pw*.42:.0f},{-16:.0f}" fill="none" stroke="#ffffff" stroke-width="9"'
             f' opacity=".30"/>')
    okno += (f'<rect x="{px-46:.0f}" y="{py-46:.0f}" width="{pw+92:.0f}" height="34"'
             f' rx="6" fill="{DOSKA2}" stroke="{K}" stroke-width="5"/>')
    for i in range(7):
        okno += (f'<path d="M{px-30+i*(pw+60)/6:.0f},{py-12:.0f} q{12:.0f},{-22:.0f}'
                 f' {24:.0f},0 Z" fill="{DOSKA}" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_DAL, okno)

    # ПРУД: лёд, под ним спящая Вода
    led_y = 640
    s += SL(Z_SRED, ledyanoe_pole(led_y, t, 23, True, True))
    dyh = 7 * A.w(t, 5.2, .1)
    voda = (f'<ellipse cx="760" cy="{880+dyh:.0f}" rx="420" ry="150" fill="#2f6b78"'
            f' opacity=".45"/>')
    voda += (f'<path d="M420,{900+dyh:.0f} q180,{-120:.0f} 420,{-70:.0f}'
             f' q180,{24:.0f} 260,{70:.0f} q-60,{80:.0f} -340,{80:.0f}'
             f' q-280,0 -340,{-80:.0f} Z" fill="#dcecf8" opacity=".55"/>')
    # девица: голова, плечи, длинные струящиеся волосы, ледяное одеяло
    voda += (f'<ellipse cx="560" cy="{852+dyh:.0f}" rx="76" ry="84" fill="#eaf6ff"'
             f' opacity=".97" stroke="#4a7a8a" stroke-width="7"/>')
    for i in (-1, 1):
        voda += (f'<path d="M{560+i*26:.0f},{842+dyh:.0f} q{i*10:.0f},{8:.0f} {i*22:.0f},0"'
                 f' fill="none" stroke="#2f4a56" stroke-width="7"/>')
    voda += (f'<path d="M524,{886+dyh:.0f} q36,{20:.0f} 72,0" fill="none"'
             f' stroke="#2f4a56" stroke-width="7"/>')
    for i in range(9):
        vl = 8 * A.w(t, 3.4, i * .2)
        voda += (f'<path d="M{520+i*10:.0f},{812+dyh:.0f} q{-120-vl:.0f},{60:.0f}'
                 f' {-300-vl*2:.0f},{54+i*8:.0f}" fill="none" stroke="#9fd0e4"'
                 f' stroke-width="7" opacity=".7"/>')
    voda += (f'<path d="M600,{890+dyh:.0f} q180,{-40:.0f} 370,{20:.0f} l0,{70:.0f}'
             f' q-190,{-30:.0f} -370,{20:.0f} Z" fill="#eaf6ff" opacity=".65"'
             f' stroke="#cfe4f5" stroke-width="4"/>')
    # карась и лягушка
    plav = 9 * A.w(t, 2.0, .3)
    voda += (f'<path d="M1080,{930:.0f} q40,{-26:.0f} 92,0 q-44,{26:.0f} -92,0 Z"'
             f' fill="#b58a3a" stroke="{K}" stroke-width="3.4"/>'
             f'<path d="M1172,{930:.0f} l{26+plav:.0f},{-16:.0f} l0,{32:.0f} Z"'
             f' fill="#9a722c" stroke="{K}" stroke-width="3"/>'
             f'<circle cx="1098" cy="926" r="4.6" fill="{K}"/>')
    voda += (f'<ellipse cx="1300" cy="968" rx="46" ry="30" fill="#5f7a3a"'
             f' stroke="{K}" stroke-width="3.4"/>'
             f'<circle cx="1282" cy="946" r="12" fill="#6f8c4a" stroke="{K}"'
             f' stroke-width="3"/><circle cx="1318" cy="946" r="12" fill="#6f8c4a"'
             f' stroke="{K}" stroke-width="3"/>'
             f'<circle cx="1282" cy="944" r="4" fill="{K}"/>'
             f'<circle cx="1318" cy="944" r="4" fill="{K}"/>')
    s += SL(Z_SRED, voda)
    s += SL(Z_SRED, korka_lda(760, 880, 440, 160, t, .3, .0, .55, .5))

    # мостки и двое на них
    s += SL(Z_SRED, mostki(180, 700, 520, t, True, 180))
    bx, by, bh = 330, 712, 420
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.3, naklon=3.0))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, -1, bh * .26, -14, t, "#4a3a52", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, 1, bh * .22, -30, t, "#4a3a52", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    cyp = 10 * A.ease(abs(A.w(t, 2.6, .2)))
    vx, vy, vh = 540, 706 - cyp, 330
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#6b4a5a", kant="#cfe4f5",
                           platok=True, ph=.7))
    s += SL(Z_SRED, para_izo_rta(bx - 26, by - bh * .80, t, .4, .8, .5)
            + para_izo_rta(vx - 20, vy - vh * .80, t, .9, .7, .45))
    s += SL(Z_SRED, ten(bx, by + 4, 90, 16, .4) + ten(vx, vy + 4, 70, 13, .4))
    # лодка у берега, камыши, ведро
    s += SL(Z_SRED, f'<path d="M60,900 q80,{60:.0f} 300,{20:.0f} q-40,{-54:.0f}'
                    f' -300,{-20:.0f} Z" fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M120,890 l-30,-70" stroke="#8a6342" stroke-width="9"'
                    f' fill="none"/>')
    s += SL(Z_SRED, kamysh(90, 1000, 200, t, 6, 27, True)
            + kamysh(1780, 1010, 230, t, 7, 31, True))
    s += SL(Z_SRED, dvorovye_veschi(1450, 1066, 380, t, 23, ["vedro", "korzina"]))
    s += SL(Z_PERED, goloe_derevo_ld(1870, 1080, 620, t, 17, 6, True))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.40)
    return s


def palka_i_kamen_nad_ldom(t):
    """Край пруда и мостки: мальчик занёс над льдом палку, мужик взвесил
    камень. Над обоими встают красные черты — палка ложится на мостки,
    камень возвращается на берег."""
    rnd = random.Random(1905)
    s = nebo("den", t, False, 37)
    s += oblaka(t, 150, 6, 31, .42)
    s += SL(Z_DAL, ulica_dal(1180, 430, 760, t, True, 19))
    s += SL(Z_DAL, goloe_derevo_ld(250, 470, 460, t, 19, 7, True))
    s += SL(Z_DAL, izba_snaruzhi(760, 452, 240, t, True, True, 13)
            + dym(786, 300, t, 5, .22, 240, .38, "#d7dee6", .9))
    s += SL(Z_SRED, ledyanoe_pole(560, t, 29, True, True))
    s += SL(Z_SRED, korka_lda(1180, 820, 430, 150, t, .2, .0, .75, .35))
    s += SL(Z_SRED, mostki(120, 740, 780, t, True, 220))
    # вмёрзшая лодка, ведро, верша на колу, ворона
    s += SL(Z_SRED, f'<path d="M1480,880 q90,{64:.0f} 330,{16:.0f} q-44,{-58:.0f}'
                    f' -330,{-16:.0f} Z" fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="1640" cy="906" rx="180" ry="26" fill="{INEY}"'
                    f' opacity=".55"/>')
    s += SL(Z_SRED, f'<path d="M1320,1066 l14,-250" stroke="#7d5636" stroke-width="14"'
                    f' fill="none"/>'
                    f'<path d="M1300,830 q40,{-70:.0f} 86,{-6:.0f} q-30,{70:.0f} -86,{6:.0f} Z"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{1302+i*16:.0f},{824-i*4:.0f} q{30:.0f},{-30:.0f}'
                        f' {56:.0f},{6:.0f}" fill="none" stroke="#8a7a52" stroke-width="3"/>')
    vor = 7 * A.w(t, 2.2, .2)
    s += SL(Z_SRED, f'<ellipse cx="{1340+vor:.0f}" cy="790" rx="44" ry="30"'
                    f' fill="#23242a" stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="{1370+vor:.0f}" cy="764" r="20" fill="#23242a"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{1388+vor:.0f},762 l26,6 l-26,7 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="2.4"/>'
                    f'<circle cx="{1376+vor:.0f}" cy="758" r="3.6" fill="#e8e2d6"/>'
                    f'<path d="M{1300+vor:.0f},790 q{-40:.0f},{10:.0f} {-56:.0f},{-14:.0f}"'
                    f' fill="none" stroke="#17181c" stroke-width="9"/>')

    # МАЛЬЧИК с палкой: опускает её на мостки
    opusk = A.ease(A.seg(t, .6, 1.6))
    mx, my, mh = 470, 742, 480
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#4a5a6a", kant="#ffd9a8",
                           tulup=True, shapka=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -20 + 70 * opusk, t,
                              "#4a5a6a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .24, -4 + 60 * opusk, t,
                              "#4a5a6a", "#ffd9a8", .5, 5)
    s += SL(Z_SRED, r1 + r2)
    pal_ug = -34 + 54 * opusk
    s += SL(Z_SRED, f'<g transform="rotate({pal_ug:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-20:.0f}" y="{e1y-10:.0f}" width="320" height="17"'
                    f' rx="8" fill="#7d5636" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e1x+240:.0f},{e1y-10:.0f} q{26:.0f},{-16:.0f}'
                    f' {46:.0f},{6:.0f}" fill="none" stroke="#6b4428" stroke-width="7"/></g>')
    s += SL(Z_SRED, para_izo_rta(mx - 30, my - mh * .80, t, .3, .9, .5))

    # МУЖИК: взвесил камень на правой рукавице, левая на поясе
    ux, uy, uh = 900, 752, 620
    vzves = 16 * A.w(t, 1.6, .1) * (1 - A.ease(A.seg(t, 1.6, 1.4)))
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#3a3f4a", kant="#ffd9a8",
                           shapka=True, tulup=True, boroda=True, ph=.6))
    r3, (e3x, e3y), _ = _ruka(ux, uy, uh, 1, uh * .30, 30 + 26 * A.ease(A.seg(t, 1.6, 1.4)),
                              t, "#3a3f4a", "#ffd9a8", .3, 4)
    r4, (e4x, e4y), _ = _ruka(ux, uy, uh, -1, uh * .22, 60, t, "#3a3f4a", "#ffd9a8", .8, 3)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, varezhka(e3x + 8, e3y + 16, 1.1, 8, "#5a4a3a", t, .3)
            + f'<ellipse cx="{e3x+14:.0f}" cy="{e3y-4+vzves:.0f}" rx="40" ry="31"'
              f' fill="{KAMEN}" stroke="{K}" stroke-width="4"/>'
              f'<path d="M{e3x-10:.0f},{e3y-16+vzves:.0f} q{22:.0f},{-14:.0f}'
              f' {44:.0f},{4:.0f}" fill="none" stroke="{KAMEN2}" stroke-width="7"/>')
    s += SL(Z_SRED, para_izo_rta(ux - 36, uy - uh * .80, t, .7, 1.0, .5))
    s += SL(Z_SRED, ten(mx, my + 4, 90, 16, .4) + ten(ux, uy + 4, 110, 19, .4))
    s += SL(Z_SRED, dvorovye_veschi(1560, 1066, 340, t, 29, ["vedro", "kadka"]))
    s += SL(Z_PERED, _cherta_zapreta(470, 470, 180, t, .0, 17)
            + _cherta_zapreta(930, 430, 200, t, .25, 17))
    s += SL(Z_PERED, kamysh(60, 1060, 240, t, 7, 33, True))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def sled_do_serediny_reki(t):
    """Река под первым льдом: цепь следов обрывается у почерневшего пятна,
    на льду осталась одна рукавица. Мужик с жердью стоит на твёрдом берегу
    и поворачивает к мосту вдали. Беды в кадре нет."""
    rnd = random.Random(1906)
    s = nebo("sumer", t, False, 41)
    s += oblaka(t, 130, 5, 37, .40)
    s += SL(Z_DAL, ulica_dal(1240, 420, 700, t, True, 23))
    s += SL(Z_DAL, izba_snaruzhi(1480, 436, 260, t, True, True, 17)
            + dym(1506, 280, t, 6, .22, 250, .40, "#d7dee6", .9))
    # мост вдали
    most = (f'<rect x="980" y="372" width="620" height="26" fill="#6b4428"'
            f' stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        most += (f'<rect x="{1020+i*140:.0f}" y="398" width="20" height="120"'
                 f' fill="#54351f" stroke="{K}" stroke-width="3"/>')
    for i in range(9):
        most += (f'<rect x="{990+i*72:.0f}" y="330" width="12" height="46"'
                 f' fill="#7d5636" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_DAL, most)
    s += SL(Z_SRED, ledyanoe_pole(500, t, 37, True, True))
    # тёмное пятно, где лёд прогнулся
    s += SL(Z_SRED, f'<ellipse cx="1140" cy="760" rx="210" ry="74" fill="#17424c"'
                    f' opacity=".82"/>'
                    f'<ellipse cx="1140" cy="760" rx="150" ry="48" fill="#0f2a32"'
                    f' opacity=".9"/>'
            + treschina(1140, 760, 250, 43, 6))
    s += SL(Z_SRED, sledy_valenok(360, 1010, 1180, 772, 11, 47, "#3a4a52", 1.25, .72))
    # одинокая рукавица на льду
    s += SL(Z_SRED, varezhka(1012, 836, 1.0, -28, TKAN, t, .4)
            + ten(1012, 866, 44, 11, .35))
    s += SL(Z_SRED, korka_lda(620, 900, 330, 110, t, .5, .0, .6, .4))

    # МУЖИК на берегу: жердь поперёк груди обеими руками, поворачивает к мосту
    pov = A.ease(A.seg(t, 1.2, 1.8))
    ux, uy, uh = 420, 1050, 640
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#3f3a33", kant="#cfe4f5",
                           tulup=True, shapka=True, boroda=True, ph=.3,
                           naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(ux, uy, uh, 1, uh * .26, 8 - 20 * pov, t,
                              "#3f3a33", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ux, uy, uh, -1, uh * .26, 10 - 18 * pov, t,
                              "#3f3a33", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    zh_ug = -8 + 14 * pov
    s += SL(Z_SRED, f'<g transform="rotate({zh_ug:.1f} {ux:.0f} {e1y:.0f})">'
                    f'<rect x="{ux-300:.0f}" y="{e1y-9:.0f}" width="620" height="18"'
                    f' rx="9" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{ux+300:.0f},{e1y:.0f} l{34:.0f},{-12:.0f} l0,{24:.0f} Z"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, para_izo_rta(ux - 40 + 20 * pov, uy - uh * .80, t, .4, 1.0, .55))
    s += SL(Z_SRED, ten(ux, uy + 6, 120, 20, .45))
    # ивняк на берегу, сани на том берегу
    for i, (kx, kb) in enumerate(((120, 1066), (250, 1050), (1860, 1040))):
        s += SL(Z_SRED, goloe_derevo_ld(kx, kb, 300 + i * 40, t, 47 + i, 6, True))
    s += SL(Z_SRED, sani_s_rogozhey(1700, 560, .62, t, .3, True))
    s += SL(Z_SRED, _trava_suhaya(rnd, 9, 980, 1070, 60, 700))
    s += SL(Z_PERED, kamysh(1880, 1070, 280, t, 8, 53, True))
    s += SL(Z_LETIT, sneg_letit(t, 22, 11, .45, .6))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def neudacha_idet_sledom(t):
    """Баба у чужого забора смотрит на новую шубу соседки и уходит прочь, а
    за ней семенит Неудача — тощая серая кошка с рваным ухом и дырявым
    мешком. Соседка на крыльце выбивает половик."""
    rnd = random.Random(1907)
    gor = 470
    s = nebo("den", t, False, 43)
    s += oblaka(t, 140, 6, 41, .44)
    s += SL(Z_DAL, ulica_dal(60, gor - 10, 900, t, True, 29))
    s += SL(Z_DAL, izba_snaruzhi(1180, gor + 40, 460, t, True, True, 19)
            + dym(1226, gor - 206, t, 7, .24, 300, .44, "#d7dee6", 1.0))
    s += SL(Z_DAL, goloe_derevo_ld(820, gor + 40, 360, t, 23, 6, True))
    s += SL(Z_SRED, sneg_lezhit(gor + 60, 30, "url(#sneg)"))
    s += SL(Z_SRED, _merzlaya_zemlya(gor + 180, 11, False))
    s += SL(Z_SRED, f'<rect x="0" y="{gor+160:.0f}" width="{W}" height="{H-gor-160:.0f}"'
                    f' fill="url(#sneg)" opacity=".92"/>'
            + inej_mel(17, 70, gor + 170, H - 10))

    # ЗАБОР посреди кадра: по эту сторону — баба, по ту — двор соседки
    s += SL(Z_SRED, zabor_shtaket(880, gor + 60, 1040, 230, 23, 62))
    # верёвка с новой шубой во дворе соседки
    kch = 6 * A.w(t, 2.4, .2)
    s += SL(Z_SRED, f'<path d="M1180,{gor+30:.0f} q260,{30:.0f} 540,{-10:.0f}"'
                    f' fill="none" stroke="#b9a37a" stroke-width="5"/>'
                    f'<g transform="rotate({kch:.1f} 1420 {gor+40:.0f})">'
                    f'<path d="M1330,{gor+44:.0f} q90,{-28:.0f} 180,0 l{30:.0f},{250:.0f}'
                    f' q{-120:.0f},{40:.0f} {-240:.0f},0 Z" fill="#6b3a2a" stroke="{K}"'
                    f' stroke-width="5"/>'
                    f'<path d="M1330,{gor+44:.0f} q90,{34:.0f} 180,0" fill="none"'
                    f' stroke="#e8e2d6" stroke-width="16" opacity=".9"/>'
                    f'<path d="M1420,{gor+60:.0f} l0,{240:.0f}" stroke="#4a2a1e"'
                    f' stroke-width="6" opacity=".8"/>'
                    f'<path d="M1310,{gor+70:.0f} l{-34:.0f},{170:.0f}" stroke="#6b3a2a"'
                    f' stroke-width="34" stroke-linecap="round"/>'
                    f'<path d="M1530,{gor+70:.0f} l{34:.0f},{170:.0f}" stroke="#6b3a2a"'
                    f' stroke-width="34" stroke-linecap="round"/></g>')

    # СОСЕДКА на крыльце выбивает половик
    kx, ky, kh = 1700, 820, 540
    s += SL(Z_SRED, f'<rect x="1560" y="820" width="340" height="30" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1580" y="850" width="300" height="24" rx="5"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="3.5"/>')
    s += SL(Z_SRED, figura(kx, ky, kh, t, col="#5a3a4a", kant="#ffd9a8",
                           platok=True, ph=.4))
    vzmah = A.w(t, 1.0, .0)
    r1, (e1x, e1y), _ = _ruka(kx, ky, kh, -1, kh * .30, -16 + 26 * vzmah, t,
                              "#5a3a4a", "#ffd9a8", .1, 9)
    s += SL(Z_SRED, r1 + f'<g transform="rotate({-16+20*vzmah:.1f} {e1x:.0f} {e1y:.0f})">'
                         f'<rect x="{e1x-150:.0f}" y="{e1y:.0f}" width="160" height="110"'
                         f' rx="6" fill="{TKAN2}" stroke="{K}" stroke-width="4"/>'
                         f'<path d="M{e1x-144:.0f},{e1y+30:.0f} h148 M{e1x-144:.0f},'
                         f'{e1y+66:.0f} h148" stroke="{RUSH}" stroke-width="8"'
                         f' opacity=".8"/></g>')
    s += SL(Z_SRED, para_izo_rta(kx - 30, ky - kh * .80, t, .3, .9, .5))

    # БАБА: смотрит через жердь забора и уходит прочь
    uh = A.ease(A.seg(t, .8, 1.4))
    bx, by, bh = 640 - 150 * uh, 1040, 650
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#5e5a55", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.6, naklon=2.0))
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, 1, bh * .26, 16 + 30 * uh, t,
                              "#5e5a55", "#cfe4f5", .2, 4)
    r3, (e3x, e3y), _ = _ruka(bx, by, bh, -1, bh * .24, 20 + 26 * uh, t,
                              "#5e5a55", "#cfe4f5", .7, 4)
    s += SL(Z_SRED, r2 + r3)
    s += SL(Z_SRED, para_izo_rta(bx - 36, by - bh * .80, t, .5, 1.0, .5))
    s += SL(Z_SRED, ten(bx, by + 6, 120, 20, .4) + ten(kx, ky + 6, 110, 19, .4))
    # НЕУДАЧА семенит следом
    s += SL(Z_SRED, neudacha_figurka(bx + 240 - 120 * uh, 1066, t, .85, .3))
    s += SL(Z_SRED, sledy_valenok(960, 1070, 700, 1006, 5, 59, "#8aa0b4", 1.1))
    # колодец, поленница, сани, синицы
    s += SL(Z_SRED, f'<rect x="120" y="760" width="230" height="110" rx="8"'
                    f' fill="{KAMEN}" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="235" cy="760" rx="115" ry="24" fill="{KAMEN2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M150,760 l-10,-150 h190 l-10,150" fill="none"'
                    f' stroke="#6b4428" stroke-width="12"/>'
                    f'<path d="M140,616 h200" stroke="#54351f" stroke-width="14"/>'
                    f'<path d="M240,616 l6,120" stroke="#b9a37a" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="420" y="800" width="250" height="150" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<circle cx="{436+(i%6)*44:.0f}" cy="{824+(i//6)*52:.0f}" r="21"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, sanki_derev(300, 1050, .9, t, .4, True))
    for i, (px, py) in enumerate(((1020, 560), (1086, 596))):
        s += SL(Z_SRED, ptica(px, py, t, 1.3, "#4a6a78", i * .4, "#b5803a"))
    s += SL(Z_LETIT, sneg_letit(t, 20, 13, .40, .55))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def gorod_u_yuzhnogo_morya(t):
    """Смена главы: тёплый южный свет. Каменный город на холмах у моря —
    стены с башнями, черепица, колоннада, маяк, корабли в гавани. По дороге
    к воротам идёт человек со спины: в правой руке посох, левая на суме."""
    rnd = random.Random(1908)
    s = (f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>')
    s += nebo("den", t, False, 47)
    s += oblaka(t, 120, 4, 43, .30, "#ffe9c8")
    s += SL(Z_NEBO, f'<circle cx="1560" cy="250" r="110" fill="#ffe9ac" opacity=".55"/>'
                    f'<circle cx="1560" cy="250" r="64" fill="#fff4d8" opacity=".9"/>')
    # море и гавань
    s += SL(Z_DAL, f'<rect x="0" y="430" width="{W}" height="300" fill="#2f6b78"/>')
    for i in range(14):
        yy = 440 + i * 20
        s += SL(Z_DAL, f'<path d="M{rnd.uniform(-60,200):.0f},{yy:.0f}'
                       f' q{rnd.uniform(200,420):.0f},{rnd.uniform(-8,8):.0f}'
                       f' {rnd.uniform(700,1200):.0f},{rnd.uniform(-5,5):.0f}" fill="none"'
                       f' stroke="#4a8a94" stroke-width="{rnd.uniform(2,5):.1f}" opacity=".6"/>')
    for i, (kx, ky, ks) in enumerate(((330, 640, 1.0), (620, 600, .76), (170, 586, .62))):
        puz = 10 * A.w(t, 3.0, i * .3)
        s += SL(Z_DAL, f'<path d="M{kx-70*ks:.0f},{ky:.0f} q{70*ks:.0f},{40*ks:.0f}'
                       f' {140*ks:.0f},0 q{-20*ks:.0f},{-26*ks:.0f} {-140*ks:.0f},0 Z"'
                       f' fill="#6b4428" stroke="{K}" stroke-width="{3.4*ks:.1f}"/>'
                       f'<rect x="{kx-4*ks:.0f}" y="{ky-120*ks:.0f}" width="{8*ks:.0f}"'
                       f' height="{120*ks:.0f}" fill="#8a6342"/>'
                       f'<path d="M{kx:.0f},{ky-116*ks:.0f} q{(50+puz)*ks:.0f},{40*ks:.0f}'
                       f' {4*ks:.0f},{86*ks:.0f} Z" fill="{"#c8301f" if i%2 else "#d6a63f"}"'
                       f' stroke="{K}" stroke-width="{3*ks:.1f}"/>')
    # город на холмах: стены, башни, черепица, колоннада, маяк
    gor = ""
    gor += (f'<path d="M820,730 L920,470 L1500,420 L1920,520 L1920,730 Z"'
            f' fill="#b9a082" stroke="{K}" stroke-width="5"/>')
    for i in range(9):
        bx = 900 + i * 110
        bh = rnd.uniform(90, 180)
        gor += (f'<rect x="{bx:.0f}" y="{560-bh:.0f}" width="86" height="{bh+170:.0f}"'
                f' fill="#cbb492" stroke="{K}" stroke-width="4"/>')
        gor += (f'<path d="M{bx-10:.0f},{560-bh:.0f} l{53:.0f},{-44:.0f} l{53:.0f},{44:.0f} Z"'
                f' fill="#a8552f" stroke="{K}" stroke-width="3.6"/>')
        for k in range(3):
            gor += (f'<rect x="{bx+12+k*24:.0f}" y="{600-bh*.4:.0f}" width="15" height="34"'
                    f' rx="4" fill="#5e4430" opacity=".9"/>')
    for i in range(6):                 # колоннада
        cx = 1000 + i * 92
        gor += (f'<rect x="{cx:.0f}" y="600" width="30" height="150" fill="#e4d8bd"'
                f' stroke="{K}" stroke-width="3.4"/>'
                f'<rect x="{cx-8:.0f}" y="592" width="46" height="16" fill="#d8c7a4"'
                f' stroke="{K}" stroke-width="3"/>')
    gor += (f'<rect x="1000" y="576" width="520" height="22" fill="#e4d8bd"'
            f' stroke="{K}" stroke-width="3.6"/>')
    # крепостная стена с башнями и воротами
    gor += (f'<rect x="760" y="660" width="1160" height="150" fill="#c3ab8a"'
            f' stroke="{K}" stroke-width="5"/>')
    for i in range(16):
        gor += (f'<rect x="{770+i*72:.0f}" y="640" width="40" height="26"'
                f' fill="#c3ab8a" stroke="{K}" stroke-width="3"/>')
    for bx in (1080, 1600):
        gor += (f'<rect x="{bx:.0f}" y="560" width="130" height="250" fill="#cbb492"'
                f' stroke="{K}" stroke-width="5"/>'
                f'<path d="M{bx-16:.0f},560 l{73:.0f},{-56:.0f} l{73:.0f},{56:.0f} Z"'
                f' fill="#a8552f" stroke="{K}" stroke-width="4"/>')
    gor += (f'<path d="M1300,810 l0,-120 q60,{-80:.0f} 120,0 l0,120 Z" fill="#3f2d1c"'
            f' stroke="{K}" stroke-width="5"/>')
    # маяк с живым огнём
    gor += (f'<path d="M1810,660 l26,-230 h44 l26,230 Z" fill="#e4d8bd" stroke="{K}"'
            f' stroke-width="4.5"/>'
            f'<rect x="1828" y="392" width="64" height="44" rx="6" fill="#b9a082"'
            f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_DAL, gor)
    s += SL(Z_DAL, ogon(1860, 404, t, .9, .2, 5) + teplo(1860, 404, 160, 130, .5))
    s += SL(Z_SRED, f'<rect x="0" y="730" width="{W}" height="350" fill="#b08a52"/>'
            + f'<path d="M-40,1080 Q560,840 1120,790 L1920,760 L1920,1080 Z"'
              f' fill="#c89a62"/>')
    for i in range(30):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(800,1070):.0f}" rx="{rnd.uniform(10,34):.0f}"'
                        f' ry="{rnd.uniform(4,11):.0f}" fill="#a8824a" opacity=".6"/>')
    # кипарисы, виноградник, ослик
    for i, (kx, kb, kh) in enumerate(((120, 880, 420), (300, 840, 330), (1780, 900, 380))):
        kach = 2.0 * A.w(t, 3.6, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {kx:.0f} {kb:.0f})">'
                        f'<path d="M{kx-38:.0f},{kb:.0f} q{10:.0f},{-kh*.7:.0f} {38:.0f},{-kh:.0f}'
                        f' q{28:.0f},{kh*.3:.0f} {38:.0f},{kh:.0f} Z" fill="#3c5a3a"'
                        f' stroke="{K}" stroke-width="4"/></g>')
    for i in range(7):
        vx = 460 + i * 86
        s += SL(Z_SRED, f'<rect x="{vx:.0f}" y="860" width="12" height="90"'
                        f' fill="#6b4428" stroke="{K}" stroke-width="2.6"/>'
                        f'<path d="M{vx-28:.0f},864 q{34:.0f},{-22:.0f} {68:.0f},0"'
                        f' fill="none" stroke="#56763f" stroke-width="7"/>'
                        f'<circle cx="{vx+6:.0f}" cy="890" r="13" fill="#6b3a6a"'
                        f' stroke="{K}" stroke-width="2.4"/>')
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="980" rx="96" ry="56" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="1584" cy="936" r="38" fill="#8a8078" stroke="{K}"'
                    f' stroke-width="4"/>'
                    f'<path d="M1604,906 l10,-40 l16,38 Z" fill="#8a8078" stroke="{K}"'
                    f' stroke-width="3"/>'
                    f'<path d="M1430,1012 l-8,52 M1480,1024 l-4,46 M1540,1020 l6,46"'
                    f' stroke="#6f6256" stroke-width="11"/>'
                    f'<rect x="1452" y="930" width="110" height="46" rx="8"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="3.6"/>')
    # ЧЕЛОВЕК со спины: посох в правой руке, левая на суме
    px, py, ph_ = 860, 1056, 620
    idt = A.ease(A.seg(t, .4, 3.0))
    px += 120 * idt
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e4d8bd", kant="#8a7a52", ph=.3))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .30, 40, t, "#e4d8bd", "#8a7a52", .2, 4)
    r2, (e2x, e2y), _ = _ruka(px, py, ph_, -1, ph_ * .22, 56, t, "#e4d8bd", "#8a7a52", .6, 3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y-320:.0f} l{10:.0f},{py-e1y+300:.0f}"'
                    f' stroke="#7d5636" stroke-width="13" stroke-linecap="round"/>'
                    f'<path d="M{e1x-6:.0f},{e1y-320:.0f} q{22:.0f},{-30:.0f} {42:.0f},{-6:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="10"/>')
    s += SL(Z_SRED, f'<path d="M{e2x-50:.0f},{e2y:.0f} h92 l-10,86 h-72 Z" fill="#b9a37a"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e2x-50:.0f},{e2y+6:.0f} q{46:.0f},{-54:.0f} {92:.0f},0"'
                    f' fill="none" stroke="#8a7a52" stroke-width="6"/>')
    s += SL(Z_SRED, ten(px, py + 6, 130, 22, .4))
    for i in range(5):                 # чайки
        a = (t * .22 + i * .2) % 1.0
        cx_, cy_ = 300 + 1300 * a, 300 + 70 * math.sin(a * 6 + i)
        s += SL(Z_LETIT, f'<path d="M{cx_:.0f},{cy_:.0f} q{16:.0f},{-14:.0f} {32:.0f},0'
                         f' q{16:.0f},{-14:.0f} {32:.0f},0" fill="none" stroke="#f4f1e8"'
                         f' stroke-width="4" opacity=".9"/>')
    # ОБЖИТОЙ ЮЖНЫЙ НИЗ: лавки под навесами, амфоры, корзины смокв, козы,
    # придорожные камни — без них дорога к воротам шла по пустому склону
    for i, (lx, ly) in enumerate(((980, 880), (1240, 900), (1660, 920))):
        kch = 3.0 * A.w(t, 3.2, i * .4)
        s += SL(Z_SRED, f'<rect x="{lx:.0f}" y="{ly:.0f}" width="190" height="90" rx="6"'
                        f' fill="#b9a37a" stroke="{K}" stroke-width="4"/>'
                        f'<g transform="rotate({kch:.1f} {lx+95:.0f} {ly-70:.0f})">'
                        f'<path d="M{lx-20:.0f},{ly-60:.0f} q{105:.0f},{-34:.0f} {230:.0f},0'
                        f' l{-16:.0f},{26:.0f} q{-100:.0f},{-20:.0f} {-198:.0f},0 Z"'
                        f' fill="{"#c8301f" if i % 2 else "#3f6b7a"}" stroke="{K}"'
                        f' stroke-width="3.6"/></g>'
                        f'<rect x="{lx-14:.0f}" y="{ly-62:.0f}" width="12" height="62"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="2.6"/>'
                        f'<rect x="{lx+192:.0f}" y="{ly-62:.0f}" width="12" height="62"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="2.6"/>')
        for k in range(4):
            s += SL(Z_SRED, f'<circle cx="{lx+24+k*44:.0f}" cy="{ly+14:.0f}" r="17"'
                            f' fill="#6b3a6a" stroke="{K}" stroke-width="2.6"/>')
    for i, (ax_, ay_, as_) in enumerate(((690, 1000, 1.0), (760, 1016, .8), (1380, 1030, .9))):
        s += SL(Z_SRED, f'<path d="M{ax_-34*as_:.0f},{ay_-96*as_:.0f}'
                        f' q{-18*as_:.0f},{70*as_:.0f} {30*as_:.0f},{96*as_:.0f}'
                        f' q{48*as_:.0f},{-26*as_:.0f} {30*as_:.0f},{-96*as_:.0f} Z"'
                        f' fill="#a8743c" stroke="{K}" stroke-width="{4*as_:.1f}"/>'
                        f'<rect x="{ax_-16*as_:.0f}" y="{ay_-124*as_:.0f}"'
                        f' width="{32*as_:.0f}" height="{30*as_:.0f}" fill="#8a5a2e"'
                        f' stroke="{K}" stroke-width="{3*as_:.1f}"/>'
                        f'<path d="M{ax_-34*as_:.0f},{ay_-104*as_:.0f}'
                        f' q{-22*as_:.0f},{24*as_:.0f} {4*as_:.0f},{44*as_:.0f}"'
                        f' fill="none" stroke="#8a5a2e" stroke-width="{6*as_:.1f}"/>')
    for i, (kz, kzy) in enumerate(((430, 960), (560, 986))):
        hv = 8 * A.w(t, 2.2, i * .5)
        s += SL(Z_SRED, f'<ellipse cx="{kz:.0f}" cy="{kzy:.0f}" rx="62" ry="38"'
                        f' fill="#d8cbb0" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{kz+58:.0f}" cy="{kzy-30:.0f}" r="26" fill="#d8cbb0"'
                        f' stroke="{K}" stroke-width="3.4"/>'
                        f'<path d="M{kz+72:.0f},{kzy-48:.0f} q{18:.0f},{-26:.0f} {4:.0f},{-40:.0f}"'
                        f' fill="none" stroke="#8a7a52" stroke-width="7"/>'
                        f'<path d="M{kz-56:.0f},{kzy-10:.0f} q{-26+hv:.0f},{16:.0f}'
                        f' {-34:.0f},{-14:.0f}" fill="none" stroke="#d8cbb0"'
                        f' stroke-width="9"/>'
                        f'<path d="M{kz-30:.0f},{kzy+30:.0f} l-6,40 M{kz+20:.0f},'
                        f'{kzy+34:.0f} l4,38" stroke="#b9a37a" stroke-width="9"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<ellipse cx="{200+i*190:.0f}" cy="{1040+(i%3)*14:.0f}"'
                        f' rx="{26+(i%4)*9:.0f}" ry="{12+(i%3)*5:.0f}" fill="#8a7a62"'
                        f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_PERED, f'<path d="M-20,1080 q220,{-120:.0f} 420,{-40:.0f} l0,180 l-440,0 Z"'
                     f' fill="#7d5636" opacity=".9"/>')
    s += ramka_pp("oba", "#120d08", .45)
    s += vinetka(.38)
    return s


def ploschad_stolicy(t):
    """Мощёная площадь с фонтаном и колоннадой: на возвышении со спины и
    вполоборота стоит человек в длинной мантии, обе руки сложены на посохе.
    Горожане снимают шапки, мальчик выпускает голубя."""
    rnd = random.Random(1909)
    s = (f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>')
    s += nebo("den", t, False, 53)
    s += oblaka(t, 110, 5, 47, .30, "#ffe9c8")
    # колоннада и портик в глубине
    kol = (f'<rect x="0" y="250" width="{W}" height="300" fill="#cbb492" opacity=".65"/>')
    for i in range(10):
        cx = 60 + i * 200
        kol += (f'<rect x="{cx:.0f}" y="270" width="54" height="300" fill="#e4d8bd"'
                f' stroke="{K}" stroke-width="4.5"/>')
        for k in range(6):
            kol += (f'<path d="M{cx+8+k*8:.0f},274 l0,292" stroke="#cdbc9c"'
                    f' stroke-width="3" opacity=".8"/>')
        kol += (f'<rect x="{cx-12:.0f}" y="252" width="78" height="24" fill="#d8c7a4"'
                f' stroke="{K}" stroke-width="4"/>'
                f'<rect x="{cx-8:.0f}" y="566" width="70" height="20" fill="#d8c7a4"'
                f' stroke="{K}" stroke-width="3.6"/>')
    kol += (f'<rect x="-20" y="214" width="{W+40}" height="40" fill="#e4d8bd"'
            f' stroke="{K}" stroke-width="5"/>')
    s += SL(Z_DAL, kol)
    # мозаичная мостовая
    most = (f'<rect x="0" y="586" width="{W}" height="{H-586}" fill="#b9a082"/>')
    for i in range(26):
        for k in range(9):
            px = -40 + i * 78 + (39 if k % 2 else 0)
            py = 600 + k * 56
            most += (f'<rect x="{px:.0f}" y="{py:.0f}" width="70" height="48" rx="6"'
                     f' fill="{"#c7b391" if (i+k) % 3 else "#ab9573"}" opacity=".9"/>')
    s += SL(Z_SRED, most)
    # фонтан с играющей струёй
    s += SL(Z_SRED, f'<ellipse cx="520" cy="880" rx="300" ry="100" fill="#8aa8b4"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<ellipse cx="520" cy="866" rx="262" ry="80" fill="#2f6b78"/>'
                    f'<ellipse cx="520" cy="860" rx="200" ry="56" fill="#4a8a94"'
                    f' opacity=".7"/>'
                    f'<rect x="494" y="700" width="52" height="166" fill="#d8c7a4"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="520" cy="700" rx="110" ry="30" fill="#e4d8bd"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(9):
        a = (t * .8 + i / 9.0) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{520+(i-4)*34*a:.0f}" cy="{668-120*a+170*a*a:.0f}"'
                        f' rx="{7+6*a:.0f}" ry="{10+8*a:.0f}" fill="#cfe4f5"'
                        f' opacity="{.85-.5*a:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M470,676 q50,{-70:.0f} 100,0" fill="none" stroke="#9fd0e4"'
                    f' stroke-width="9" opacity=".75"/>')
    # возвышение и ГЛАВНЫЙ: со спины и вполоборота, обе руки на посохе
    s += SL(Z_SRED, f'<rect x="1140" y="880" width="520" height="52" rx="6"'
                    f' fill="#d8c7a4" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1180" y="932" width="440" height="46" rx="6"'
                    f' fill="#c7b391" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="1220" y="978" width="360" height="44" rx="6"'
                    f' fill="#b9a082" stroke="{K}" stroke-width="4"/>')
    px, py, ph_ = 1400, 880, 660
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#8a7a52",
                           ph=.2, boroda=True, profil=True))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .26, 44, t, "#e8e2d6", "#8a7a52", .2, 3)
    r2, (e2x, e2y), _ = _ruka(px, py, ph_, -1, ph_ * .24, 50, t, "#e8e2d6", "#8a7a52", .5, 3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{(e1x+e2x)/2:.0f},{e1y-210:.0f} l{6:.0f},{py-e1y+190:.0f}"'
                    f' stroke="#7d5636" stroke-width="14" stroke-linecap="round"/>'
                    f'<path d="M{(e1x+e2x)/2-6:.0f},{e1y-210:.0f} q{24:.0f},{-34:.0f}'
                    f' {46:.0f},{-6:.0f}" fill="none" stroke="#6b4428" stroke-width="11"/>')
    # мантия длинная, со складками
    s += SL(Z_SRED, f'<path d="M{px-130:.0f},{py-ph_*.60:.0f} q{130:.0f},{-40:.0f}'
                    f' {260:.0f},0 l{44:.0f},{ph_*.58:.0f} q{-174:.0f},{40:.0f}'
                    f' {-348:.0f},0 Z" fill="#efe6d2" opacity=".55" stroke="#c9bfa6"'
                    f' stroke-width="4"/>')
    s += SL(Z_SRED, ten(px, py + 8, 150, 24, .4))
    # ГОРОЖАНЕ снимают шапки
    for i, (hx, hy, hh, col) in enumerate(((760, 1046, 470, "#a8743c"),
                                           (960, 1056, 430, "#6b3a6a"),
                                           (1760, 1040, 450, "#3f6b7a"))):
        snyal = A.ease(A.seg(t, .4 + i * .2, .8))
        s += SL(Z_SRED, figura(hx, hy, hh, t, col=col, kant="#ffd9a8", ph=i * .3))
        rk, (ex, ey), _ = _ruka(hx, hy, hh, 1, hh * .26, 60 - 70 * snyal, t,
                                col, "#ffd9a8", i * .2, 4)
        s += SL(Z_SRED, rk + f'<ellipse cx="{ex+10:.0f}" cy="{ey+14:.0f}" rx="34"'
                             f' ry="20" fill="#8a6a4a" stroke="{K}" stroke-width="3.6"/>')
        s += SL(Z_SRED, ten(hx, hy + 6, 92, 16, .35))
    # торговец с корзиной смокв и женщина с кувшином
    tx, ty, th = 300, 1066, 500
    s += SL(Z_SRED, figura(tx, ty, th, t, col="#8a5a2e", kant="#ffd9a8", ph=.7))
    r3, (e3x, e3y), _ = _ruka(tx, ty, th, 1, th * .24, 62, t, "#8a5a2e", "#ffd9a8", .4, 4)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x-40:.0f},{e3y+8:.0f} q{40:.0f},{16:.0f} {80:.0f},0'
                         f' l{-10:.0f},{54:.0f} h{-60:.0f} Z" fill="#b08a52" stroke="{K}"'
                         f' stroke-width="3.6"/>')
    for k in range(5):
        s += SL(Z_SRED, f'<circle cx="{e3x-28+k*14:.0f}" cy="{e3y+18:.0f}" r="11"'
                        f' fill="#6b3a6a" stroke="{K}" stroke-width="2.4"/>')
    zx, zy, zh = 1900, 1060, 520
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#c8301f", kant="#ffd9a8",
                           platok=True, ph=.9))
    s += SL(Z_SRED, f'<path d="M{zx-120:.0f},{zy-zh*.70:.0f} q{-22:.0f},{44:.0f}'
                    f' {12:.0f},{70:.0f} q{40:.0f},{14:.0f} {54:.0f},{-20:.0f}'
                    f' q{10:.0f},{-44:.0f} {-20:.0f},{-56:.0f} Z" fill="#a8743c"'
                    f' stroke="{K}" stroke-width="4"/>')
    # МАЛЬЧИК с голубем: голубь взлетает
    mx, my, mh = 1080, 1062, 330
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#e4d8bd", kant="#8a7a52", ph=.5))
    r4, (e4x, e4y), _ = _ruka(mx, my, mh, 1, mh * .30, -24, t, "#e4d8bd", "#8a7a52", .3, 6)
    s += SL(Z_SRED, r4)
    vzl = A.ease(A.seg(t, 1.0, 1.4))
    gx, gy = e4x + 10 + 120 * vzl, e4y - 10 - 300 * vzl
    kr = 20 * A.w(t, .35, .0)
    s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="30" ry="20" fill="#e8eef6"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<circle cx="{gx+24:.0f}" cy="{gy-14:.0f}" r="13" fill="#e8eef6"'
                    f' stroke="{K}" stroke-width="2.6"/>'
                    f'<path d="M{gx+36:.0f},{gy-16:.0f} l14,4 l-14,5 Z" fill="{ORA}"/>'
                    f'<path d="M{gx-6:.0f},{gy-8:.0f} q{20:.0f},{-30-kr:.0f} {50:.0f},{-16:.0f}"'
                    f' fill="none" stroke="#cfd6de" stroke-width="12"/>'
                    f'<path d="M{gx-6:.0f},{gy+2:.0f} q{18:.0f},{26+kr:.0f} {46:.0f},{14:.0f}"'
                    f' fill="none" stroke="#cfd6de" stroke-width="11"/>')
    # навесы лавок и светильник на столбе — живой огонёк площади
    for i, (lx, ly) in enumerate(((60, 700), (1700, 690))):
        kch = 3.4 * A.w(t, 3.0, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {lx+100:.0f} {ly:.0f})">'
                        f'<path d="M{lx:.0f},{ly:.0f} q{100:.0f},{-40:.0f} {200:.0f},0'
                        f' l{-14:.0f},{30:.0f} q{-86:.0f},{-26:.0f} {-172:.0f},0 Z"'
                        f' fill="{"#c8301f" if i else "#3f6b7a"}" stroke="{K}"'
                        f' stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<rect x="1660" y="560" width="22" height="330" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, lampa(1671, 548, t, 1.3, False) + teplo(1671, 540, 190, 160, .45))
    s += SL(Z_PERED, f'<rect x="-10" y="250" width="70" height="830" fill="#1d1611"'
                     f' opacity=".85"/>')
    s += ramka_pp("oba", "#120d08", .45)
    s += vinetka(.40)
    return s


def dva_imeni_na_svitke(t):
    """Стол в каменной палате: развёрнутый свиток с двумя строчками-завитками,
    чернильница, перо, светильник. Старец в кресле указывает на свиток,
    старейшина кладёт камешек-жребий на верхнюю строчку — она загорается."""
    rnd = random.Random(1910)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    s += SL(Z_DAL, kladka(0, 0, W, 760, 86, "url(#kamen)"))
    s += SL(Z_DAL, svody(t, "#4b443b", 3))
    # окно с видом на море
    s += SL(Z_DAL, f'<path d="M1480,180 q120,{-150:.0f} 240,0 l0,330 l-240,0 Z"'
                   f' fill="#4a8a94" stroke="{K}" stroke-width="6"/>'
                   f'<path d="M1480,380 q120,{20:.0f} 240,{-10:.0f} l0,140 l-240,0 Z"'
                   f' fill="#2f6b78"/>'
                   f'<path d="M1480,300 q120,{-130:.0f} 240,0" fill="none" stroke="#e4d8bd"'
                   f' stroke-width="7" opacity=".5"/>'
                   f'<rect x="1590" y="40" width="18" height="470" fill="#6b4428"'
                   f' opacity=".9"/>')
    s += SL(Z_DAL, f'<path d="M1180,0 q40,{280:.0f} -10,{560:.0f} l-150,0 q50,{-280:.0f}'
                   f' 10,{-560:.0f} Z" fill="#8a2f22" stroke="{K}" stroke-width="5"/>')
    for i in range(5):
        s += SL(Z_DAL, f'<path d="M{1040+i*26:.0f},20 q{30:.0f},{280:.0f} {-6:.0f},{540:.0f}"'
                       f' fill="none" stroke="#6b2419" stroke-width="7" opacity=".7"/>')
    # СТОЛ во весь кадр
    s += SL(Z_SRED, f'<rect x="60" y="700" width="1800" height="60" rx="10"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="60" y="760" width="1800" height="26" fill="#54351f"'
                    f' opacity=".9"/>'
                    f'<rect x="200" y="786" width="54" height="294" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1640" y="786" width="54" height="294" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="4"/>')
    # СВИТОК с двумя строчками-завитками
    sx, sy, sw, sh_ = 560, 560, 820, 150
    svit = (f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="{sh_:.0f}"'
            f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>')
    for i in (0, 1):
        rx_ = sx - 40 if i == 0 else sx + sw
        svit += (f'<rect x="{rx_:.0f}" y="{sy-18:.0f}" width="40" height="{sh_+36:.0f}"'
                 f' rx="20" fill="#c9a05a" stroke="{K}" stroke-width="4.5"/>')
    gor_ = A.ease(A.seg(t, 1.3, 1.0))
    for i, yy in enumerate((sy + 46, sy + 104)):
        col = "#8a2f22" if i == 0 else "#6f6354"
        svit += (f'<path d="M{sx+70:.0f},{yy:.0f} q{60:.0f},{-14:.0f} {120:.0f},0'
                 f' q{60:.0f},{14:.0f} {120:.0f},0 q{60:.0f},{-14:.0f} {120:.0f},0'
                 f' q{60:.0f},{14:.0f} {120:.0f},0" fill="none" stroke="{col}"'
                 f' stroke-width="7" opacity=".9"/>')
    svit += (f'<rect x="{sx+54:.0f}" y="{sy+22:.0f}" width="{sw-110:.0f}" height="48"'
             f' rx="10" fill="#ffd98a" opacity="{.55*gor_:.2f}"/>')
    svit += (f'<rect x="{sx+54:.0f}" y="{sy+22:.0f}" width="{sw-110:.0f}" height="48"'
             f' rx="10" fill="none" stroke="#ffe9ac" stroke-width="5"'
             f' opacity="{.9*gor_:.2f}"/>')
    s += SL(Z_SRED, svit)
    # камешек-жребий ложится на верхнюю строчку
    kl = A.out(A.seg(t, .7, .9))
    s += SL(Z_SRED, f'<ellipse cx="{sx+300:.0f}" cy="{sy+46-180*(1-kl):.0f}" rx="26"'
                    f' ry="18" fill="{KAMEN}" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{sx+282:.0f},{sy+38-180*(1-kl):.0f} q{18:.0f},{-10:.0f}'
                    f' {36:.0f},{4:.0f}" fill="none" stroke="#9aa3a8" stroke-width="5"/>')
    # чернильница, перо, светильник
    s += SL(Z_SRED, f'<path d="M1430,700 h110 l-14,-66 h-82 Z" fill="#3f3a33"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="1485" cy="634" rx="42" ry="13" fill="#17120d"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1500,630 l80,-150" stroke="#e8e2d6" stroke-width="9"'
                    f' fill="none"/>'
                    f'<path d="M1572,490 q{26:.0f},{-40:.0f} {40:.0f},{-8:.0f}'
                    f' q{-18:.0f},{26:.0f} {-34:.0f},{30:.0f} Z" fill="#f4f1e8"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M300,700 h140 l-20,-40 h-100 Z" fill="#b5803a"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M330,660 q40,{-30:.0f} 80,0 l-10,-26 h-60 Z"'
                    f' fill="#c08a3a" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, ogon(370, 610, t, 1.15, .1, 6) + teplo(370, 600, 320, 260, .5))
    s += SL(Z_SRED, f'<path d="M1720,760 q-40,{-120:.0f} 10,{-190:.0f} q70,{40:.0f}'
                    f' {50:.0f},{190:.0f} Z" fill="#a8743c" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    # СТАРЕЦ в кресле: слабой правой рукой указывает на свиток
    kx, ky, kh = 1760, 1010, 560
    s += SL(Z_SRED, f'<rect x="{kx-150:.0f}" y="{ky-470:.0f}" width="300" height="470"'
                    f' rx="16" fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="{kx-130:.0f}" y="{ky-440:.0f}" width="260" height="300"'
                    f' rx="12" fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(kx, ky, kh, t, col="#e8e2d6", kant="#8a7a52",
                           boroda=True, ph=.8))
    uk = A.ease(A.seg(t, .3, 1.0))
    r1, (e1x, e1y), _ = _ruka(kx, ky, kh, -1, kh * .34, 16 - 30 * uk, t,
                              "#e8e2d6", "#8a7a52", .2, 3)
    s += SL(Z_SRED, r1)
    # ДВОЕ СТАРЕЙШИН у стола: один держит свиток обеими руками, второй — жребий
    for i, (ox, oy, oh, col) in enumerate(((420, 1066, 620, "#6f6354"),
                                           (980, 1070, 640, "#8a7a52"))):
        s += SL(Z_SRED, figura(ox, oy, oh, t, col=col, kant="#ffd9a8",
                               boroda=(i == 0), ph=.3 + i * .4))
        rk1, (ax_, ay_), _ = _ruka(ox, oy, oh, 1, oh * .26, -14 + i * 8, t,
                                   col, "#ffd9a8", .2 + i * .2, 4)
        rk2, (bx_, by_), _ = _ruka(ox, oy, oh, -1, oh * .24, -10 + i * 6, t,
                                   col, "#ffd9a8", .6 + i * .2, 4)
        s += SL(Z_SRED, rk1 + rk2)
    s += SL(Z_SRED, ten(420, 1072, 120, 20, .4) + ten(980, 1076, 124, 20, .4))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="90" height="{H}" fill="#120d08"'
                     f' opacity=".9"/>')
    s += ramka_pp("oba", "#120d08", .5)
    s += vinetka(.44)
    return s


def imperator_vozvraschaetsya(t):
    """Городские ворота: в них въезжает колесница. Император в пурпурном
    плаще резко указывает вперёд, возница с кнутом. Навстречу из города
    со спины выходит Павел с посохом и сумой, стражники провожают копьями."""
    rnd = random.Random(1911)
    s = (f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>')
    s += nebo("den", t, False, 59)
    s += oblaka(t, 120, 5, 53, .32, "#ffe9c8")
    # СТЕНА С ВОРОТАМИ во весь кадр
    st_ = (f'<rect x="0" y="200" width="{W}" height="640" fill="#c3ab8a"'
           f' stroke="{K}" stroke-width="6"/>')
    st_ += kladka(0, 200, W, 640, 88, "url(#kamen)")
    for i in range(20):
        st_ += (f'<rect x="{10+i*96:.0f}" y="168" width="54" height="36"'
                f' fill="#c3ab8a" stroke="{K}" stroke-width="3.4"/>')
    for bx in (120, 1560):
        st_ += (f'<rect x="{bx:.0f}" y="90" width="230" height="750" fill="#cbb492"'
                f' stroke="{K}" stroke-width="6"/>'
                f'<path d="M{bx-28:.0f},90 l{129:.0f},{-74:.0f} l{129:.0f},{74:.0f} Z"'
                f' fill="#a8552f" stroke="{K}" stroke-width="5"/>')
        for k in range(3):
            st_ += (f'<rect x="{bx+36+k*62:.0f}" y="280" width="34" height="72" rx="16"'
                    f' fill="#4a3526" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_DAL, st_)
    # проём ворот: тёмная арка, за ней город
    s += SL(Z_DAL, f'<path d="M700,840 l0,-330 q260,{-260:.0f} 520,0 l0,330 Z"'
                   f' fill="#3f2d1c" stroke="{K}" stroke-width="7"/>'
                   f'<path d="M740,840 l0,-310 q220,{-230:.0f} 440,0 l0,310 Z"'
                   f' fill="#6b5a44" opacity=".8"/>')
    for i in range(6):
        s += SL(Z_DAL, f'<rect x="{760+i*68:.0f}" y="{560+(i%2)*30:.0f}" width="52"'
                       f' height="{280-(i%2)*30:.0f}" fill="#8a7a62" opacity=".55"/>')
    # знамёна БЕЗ СИМВОЛОВ по сторонам ворот
    for i, zx in enumerate((640, 1270)):
        kch = 5 * A.w(t, 2.6, i * .4)
        s += SL(Z_SRED, f'<rect x="{zx:.0f}" y="300" width="14" height="360"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{zx+14:.0f},318 q{60+kch:.0f},{30:.0f} {110:.0f},{-6:.0f}'
                        f' l0,{130:.0f} q{-50:.0f},{24:.0f} {-110:.0f},{-6:.0f} Z"'
                        f' fill="{"#8a2f22" if i else "#3f4a7a"}" stroke="{K}"'
                        f' stroke-width="4"/>')
    # дорога и пыль
    s += SL(Z_SRED, f'<rect x="0" y="840" width="{W}" height="240" fill="#b08a52"/>'
            + f'<path d="M-40,1080 Q600,900 1180,860 L1920,846 L1920,1080 Z"'
              f' fill="#c89a62"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(870,1070):.0f}" rx="{rnd.uniform(12,40):.0f}"'
                        f' ry="{rnd.uniform(5,13):.0f}" fill="#a8824a" opacity=".55"/>')
    vezd = A.ease(A.seg(t, .3, 3.4))
    for i in range(7):
        d = ((t * .6 + i / 7.0) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{1500-400*vezd+90*d:.0f}" cy="{1000-60*d:.0f}"'
                        f' rx="{30+50*d:.0f}" ry="{16+26*d:.0f}" fill="#d8c7a4"'
                        f' opacity="{(1-d)*.45:.2f}"/>')
    # КОЛЕСНИЦА въезжает
    kx = 1520 - 420 * vezd
    kol = (f'<path d="M{kx-110:.0f},900 h220 q26,0 26,{-80:.0f} l{-10:.0f},{-70:.0f}'
           f' h{-252:.0f} Z" fill="#a8743c" stroke="{K}" stroke-width="5"/>')
    kol += (f'<path d="M{kx-110:.0f},760 h236" stroke="{ZOL}" stroke-width="10"/>')
    ug = (t * 260) % 360
    for wx in (kx - 90, kx + 90):
        kol += (f'<g transform="rotate({ug:.0f} {wx:.0f} 906)">'
                f'<circle cx="{wx:.0f}" cy="906" r="86" fill="none" stroke="#6b4428"'
                f' stroke-width="15"/>')
        for k in range(8):
            a = k * .785
            kol += (f'<line x1="{wx:.0f}" y1="906" x2="{wx+80*math.cos(a):.0f}"'
                    f' y2="{906+80*math.sin(a):.0f}" stroke="#7d5636" stroke-width="7"/>')
        kol += '</g>'
    kol += (f'<path d="M{kx+130:.0f},840 q{120:.0f},{-20:.0f} {210:.0f},{10:.0f}"'
            f' fill="none" stroke="#6b4428" stroke-width="9"/>')
    s += SL(Z_SRED, kol)
    # ИМПЕРАТОР: левая держит поводья, правая резко указывает вперёд
    ix, iy, ih = kx - 10, 820, 560
    ukaz = A.out(A.seg(t, .9, .7))
    s += SL(Z_SRED, figura(ix, iy, ih, t, col="#6b2a5a", kant="#ffd98a",
                           ph=.2, boroda=True))
    r1, (e1x, e1y), _ = _ruka(ix, iy, ih, -1, ih * .34, -6 - 24 * ukaz, t,
                              "#6b2a5a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ix, iy, ih, 1, ih * .26, 34, t, "#6b2a5a", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e2x:.0f},{e2y:.0f} q{90:.0f},{30:.0f} {170:.0f},{6:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="6"/>')
    # плащ отлетает назад
    pl = 40 + 26 * A.w(t, 1.4, .1)
    s += SL(Z_SRED, f'<path d="M{ix+40:.0f},{iy-ih*.64:.0f} q{-60-pl:.0f},{120:.0f}'
                    f' {-160-pl:.0f},{210:.0f} q{70:.0f},{20:.0f} {150:.0f},{-40:.0f} Z"'
                    f' fill="#7d2f66" stroke="{K}" stroke-width="4.5"/>')
    # венец
    s += SL(Z_SRED, f'<path d="M{ix-44:.0f},{iy-ih*.86:.0f} h88 l-8,-26 h-72 Z"'
                    f' fill="{ZOL}" stroke="{K}" stroke-width="3.6"/>')
    # ВОЗНИЦА с кнутом
    vx, vy, vh = kx + 86, 824, 500
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#8a7a52", kant="#ffd9a8", ph=.7))
    r3, (e3x, e3y), _ = _ruka(vx, vy, vh, 1, vh * .28, -28, t, "#8a7a52", "#ffd9a8", .4, 7)
    knut = 20 * A.w(t, .9, .2)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x:.0f},{e3y:.0f} q{70:.0f},{-60-knut:.0f}'
                         f' {150:.0f},{-20+knut:.0f}" fill="none" stroke="#5e4a2a"'
                         f' stroke-width="5"/>')
    # ПАВЕЛ со спины выходит из ворот, стражники провожают копьями
    px, py, ph_ = 860 - 60 * A.ease(A.seg(t, 1.4, 2.0)), 1000, 600
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#8a7a52", ph=.5))
    r4, (e4x, e4y), _ = _ruka(px, py, ph_, 1, ph_ * .28, 44, t, "#e8e2d6", "#8a7a52", .3, 3)
    r5, (e5x, e5y), _ = _ruka(px, py, ph_, -1, ph_ * .22, 56, t, "#e8e2d6", "#8a7a52", .8, 3)
    s += SL(Z_SRED, r4 + r5)
    s += SL(Z_SRED, f'<path d="M{e4x:.0f},{e4y-300:.0f} l{8:.0f},{py-e4y+280:.0f}"'
                    f' stroke="#7d5636" stroke-width="12" stroke-linecap="round"/>'
                    f'<path d="M{e5x-44:.0f},{e5y:.0f} h86 l-10,78 h-66 Z" fill="#b9a37a"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i, sx_ in enumerate((1010, 1150)):
        s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="980" rx="46" ry="110"'
                        f' fill="#4a4038" opacity=".92" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{sx_:.0f}" cy="844" r="38" fill="#4a4038"'
                        f' stroke="{K}" stroke-width="4"/>'
                        f'<path d="M{sx_+40:.0f},1070 l{-14:.0f},{-330:.0f}"'
                        f' stroke="#6b4428" stroke-width="8"/>'
                        f'<path d="M{sx_+24:.0f},740 l{8:.0f},{-44:.0f} l{10:.0f},{44:.0f} Z"'
                        f' fill="#c9ccd1" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, ten(px, py + 6, 130, 22, .4))
    s += SL(Z_SRED, lampa(300, 560, t, 1.2, False) + teplo(300, 560, 200, 170, .40))
    s += SL(Z_PERED, f'<path d="M-20,1080 q180,{-90:.0f} 360,{-30:.0f} l0,160 l-380,0 Z"'
                     f' fill="#7d5636" opacity=".9"/>')
    s += ramka_pp("oba", "#120d08", .45)
    s += vinetka(.40)
    return s


def vorota_otkryvayutsya_i_zakryvayuts(t):
    """Те же ворота во весь кадр: Павел со спины входит — створки
    распахиваются, выходит — захлопываются, и снова. Над воротами растёт
    рисованный счётчик, ослик у придорожного камня провожает его взглядом."""
    rnd = random.Random(1912)
    s = (f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>')
    s += nebo("den", t, False, 61)
    s += oblaka(t, 130, 4, 59, .30, "#ffe9c8")
    st_ = (f'<rect x="0" y="120" width="{W}" height="740" fill="#c3ab8a"'
           f' stroke="{K}" stroke-width="6"/>')
    st_ += kladka(0, 120, W, 740, 92, "url(#kamen)")
    for i in range(20):
        st_ += (f'<rect x="{6+i*98:.0f}" y="86" width="56" height="38"'
                f' fill="#c3ab8a" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_DAL, st_)
    s += SL(Z_DAL, f'<path d="M620,860 l0,-360 q340,{-300:.0f} 680,0 l0,360 Z"'
                   f' fill="#2b2016" stroke="{K}" stroke-width="8"/>')
    # что видно в проёме: улица города с огоньком
    s += SL(Z_DAL, f'<path d="M700,860 l0,-310 q280,{-250:.0f} 560,0 l0,310 Z"'
                   f' fill="#6b5a44" opacity=".85"/>')
    for i in range(5):
        s += SL(Z_DAL, f'<rect x="{720+i*110:.0f}" y="{600+(i%2)*34:.0f}" width="80"'
                       f' height="{260-(i%2)*34:.0f}" fill="#8a7a62" opacity=".6"/>')
    s += SL(Z_DAL, svecha(960, 700, t, .2, 1.6, 110) + teplo(960, 660, 220, 190, .40))
    # СТВОРКИ: распахиваются и захлопываются
    faza = (t * .75) % 1.0
    otkr = A.ease(min(1.0, faza * 2.6)) - A.ease(max(.0, faza * 2.6 - 1.5))
    for i in (-1, 1):
        ug = i * 52 * otkr
        cx_ = 960 + i * 340
        stv = (f'<g transform="rotate({ug:.1f} {cx_:.0f} 860)">'
               f'<rect x="{cx_-(340 if i>0 else 0):.0f}" y="500" width="340" height="360"'
               f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>')
        for k in range(5):
            stv += (f'<rect x="{cx_-(330 if i>0 else -10)+k*66:.0f}" y="510" width="52"'
                    f' height="340" rx="5" fill="{DOSKA}" opacity=".9" stroke="{K}"'
                    f' stroke-width="2.6"/>')
        stv += (f'<rect x="{cx_-(330 if i>0 else -10):.0f}" y="640" width="320"'
                f' height="26" fill="{ZHELEZ}" opacity=".9"/>')
        stv += (f'<circle cx="{cx_-i*60:.0f}" cy="700" r="24" fill="none"'
                f' stroke="{CHUGUN}" stroke-width="10"/></g>')
        s += SL(Z_SRED, stv)
    # ПАВЕЛ входит и выходит: по фазе
    hod = math.sin(faza * 6.283)
    px, py, ph_ = 960 + 260 * hod, 1020, 620
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#8a7a52", ph=.3))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .28, 42, t, "#e8e2d6", "#8a7a52", .2, 4)
    s += SL(Z_SRED, r1 + f'<path d="M{e1x:.0f},{e1y-300:.0f} l{8:.0f},{py-e1y+280:.0f}"'
                         f' stroke="#7d5636" stroke-width="13" stroke-linecap="round"/>')
    s += SL(Z_SRED, ten(px, py + 6, 130, 22, .4))
    # СЧЁТЧИК над воротами: рисованные палочки-засечки, их всё больше
    n = 1 + int((t * .9) % 4)
    for i in range(n):
        s += SL(Z_SRED, f'<rect x="{830+i*70:.0f}" y="300" width="18" height="86"'
                        f' rx="6" fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    # стражники-силуэты на стене
    for i, sx_ in enumerate((420, 1500)):
        s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="150" rx="40" ry="86"'
                        f' fill="#4a4038" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{sx_:.0f}" cy="48" r="32" fill="#4a4038"'
                        f' stroke="{K}" stroke-width="3.6"/>'
                        f'<path d="M{sx_+36:.0f},220 l{-10:.0f},{-260:.0f}"'
                        f' stroke="#6b4428" stroke-width="8"/>')
    # дорога, оливы, придорожный камень, ослик
    s += SL(Z_SRED, f'<rect x="0" y="860" width="{W}" height="220" fill="#b08a52"/>'
            + f'<path d="M-40,1080 Q620,920 1200,878 L1920,866 L1920,1080 Z"'
              f' fill="#c89a62"/>')
    for i in range(18):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(890,1070):.0f}" rx="{rnd.uniform(14,42):.0f}"'
                        f' ry="{rnd.uniform(5,14):.0f}" fill="#a8824a" opacity=".55"/>')
    for i, (ox, ob, oh) in enumerate(((120, 1010, 300), (1830, 1030, 340))):
        kch = 2.4 * A.w(t, 3.4, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {ox:.0f} {ob:.0f})">'
                        f'<path d="M{ox-16:.0f},{ob:.0f} q{6:.0f},{-oh*.6:.0f}'
                        f' {18:.0f},{-oh:.0f} l{20:.0f},0 q{10:.0f},{oh*.6:.0f}'
                        f' {14:.0f},{oh:.0f} Z" fill="#6b5230" stroke="{K}"'
                        f' stroke-width="4"/>'
                        f'<ellipse cx="{ox+14:.0f}" cy="{ob-oh-30:.0f}" rx="{oh*.38:.0f}"'
                        f' ry="{oh*.26:.0f}" fill="#56763f" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{ox-50:.0f}" cy="{ob-oh+40:.0f}" rx="{oh*.22:.0f}"'
                        f' ry="{oh*.16:.0f}" fill="#49693a" stroke="{K}" stroke-width="3.4"/></g>')
    s += SL(Z_SRED, f'<path d="M330,1066 q30,{-110:.0f} 130,{-96:.0f} q40,{60:.0f}'
                    f' {26:.0f},{96:.0f} Z" fill="#8a8078" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M360,1020 q50,{-24:.0f} 96,{-6:.0f}" fill="none"'
                    f' stroke="#6f6256" stroke-width="7"/>')
    glyad = 10 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<ellipse cx="1620" cy="990" rx="104" ry="58" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="{1716+glyad:.0f}" cy="936" r="40" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{1738+glyad:.0f},904 l10,-44 l18,40 Z" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="3.2"/>'
                    f'<circle cx="{1728+glyad:.0f}" cy="930" r="5" fill="{K}"/>'
                    f'<path d="M1540,1030 l-8,46 M1596,1042 l-4,40 M1664,1038 l6,42"'
                    f' stroke="#6f6256" stroke-width="11"/>'
                    f'<rect x="1560" y="930" width="120" height="50" rx="9"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="3.6"/>')
    s += ramka_pp("oba", "#120d08", .45)
    s += vinetka(.40)
    return s


def gornaya_doroga_v_ssylku(t):
    """Каменистая тропа над ущельем: в проёме старого каменного моста —
    настоящие заснеженные горы. Павел со спины идёт вверх, опираясь на
    посох; за ним стражник с копьём и щитом, выше кружит орёл."""
    rnd = random.Random(1913)
    s = (f'<rect width="{W}" height="{H}" fill="#6b7a88"/>')
    s += nebo("den", t, False, 67)
    s += oblaka(t, 150, 6, 61, .40)
    # дальние скалы
    for i, (sx, sb, sh_, col) in enumerate(((-100, 640, 520, "#6f7a84"),
                                            (420, 600, 460, "#5e6a74"),
                                            (1500, 660, 540, "#6f7a84"))):
        s += SL(Z_DAL, f'<path d="M{sx:.0f},{sb:.0f} l{sh_*.5:.0f},{-sh_:.0f}'
                       f' l{sh_*.35:.0f},{sh_*.42:.0f} l{sh_*.30:.0f},{-sh_*.28:.0f}'
                       f' l{sh_*.55:.0f},{sh_*.86:.0f} Z" fill="{col}" stroke="{K}"'
                       f' stroke-width="5"/>')
        s += SL(Z_DAL, f'<path d="M{sx+sh_*.5:.0f},{sb-sh_:.0f} l{sh_*.18:.0f},{sh_*.22:.0f}'
                       f' l{-sh_*.36:.0f},0 Z" fill="url(#sneg)" opacity=".9"/>')
    # КАМЕННАЯ АРКА МОСТА: сначала вид, потом метка, потом кладка поверх
    ax, ay, aw, ah = 120, 300, 780, 320
    put = kontur_proema(ax, ay, aw, ah, "arka")
    arka = (f'<path d="{put}" fill="#8aa0b4"/>')
    arka += (f'<path d="{put}" fill="#cfe4f5" opacity=".45"/>')
    arka += mesto_stoka(ax, ay, aw, ah, "arka")
    arka += (f'<path d="{put}" fill="none" stroke="#5e564c" stroke-width="26"/>')
    s += SL(Z_SRED, arka)
    most = (f'<path d="M{ax-180:.0f},{ay+ah:.0f} l0,-120 q{aw*.5+180:.0f},{-380:.0f}'
            f' {aw+360:.0f},0 l0,120 l-120,0 q{-aw*.4:.0f},{-280:.0f} {-aw-120:.0f},0 Z"'
            f' fill="#7d7265" stroke="{K}" stroke-width="6"/>')
    most += kladka(ax - 180, ay - 90, aw + 360, 150, 54, "url(#kamen)")
    most += (f'<rect x="{ax-200:.0f}" y="{ay-120:.0f}" width="{aw+400:.0f}" height="40"'
             f' rx="6" fill="#8a8078" stroke="{K}" stroke-width="5"/>')
    most += (f'<path d="M{ax-200:.0f},{ay-120:.0f} q{(aw+400)*.5:.0f},{-18:.0f}'
             f' {aw+400:.0f},0 l0,12 q{-(aw+400)*.5:.0f},{16:.0f} {-aw-400:.0f},0 Z"'
             f' fill="url(#sneg)" opacity=".9"/>')
    s += SL(Z_SRED, most)
    # ТРОПА по склону
    s += SL(Z_SRED, f'<path d="M-40,1080 Q560,900 1060,820 Q1480,756 1920,700'
                    f' L1920,1080 Z" fill="#7a6e5e" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-40,1080 Q600,940 1100,862 Q1500,800 1920,752"'
                    f' fill="none" stroke="#8d8070" stroke-width="40" opacity=".8"/>')
    for i in range(30):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(800,1070):.0f}" rx="{rnd.uniform(12,46):.0f}"'
                        f' ry="{rnd.uniform(6,18):.0f}" fill="#6b6050" opacity=".65"/>')
    s += SL(Z_SRED, inej_mel(19, 50, 820, 1070))
    # сухие кусты и каменная хижина
    for i in range(6):
        kx = rnd.uniform(60, 1860)
        s += SL(Z_SRED, _trava_suhaya(rnd, 1, 880, 1050, kx, kx + 90))
    s += SL(Z_SRED, f'<rect x="1540" y="560" width="300" height="190" rx="8"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1520,560 l170,-110 l170,110 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1520,560 l170,-110 l170,110" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="14" opacity=".9"/>'
                    f'<rect x="1640" y="640" width="80" height="110" rx="6"'
                    f' fill="#3f3a33" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, dym(1700, 440, t, 6, .22, 260, .42, "#d7dee6", 1.0))
    # ВЬЮЧНЫЙ МУЛ
    s += SL(Z_SRED, f'<ellipse cx="1320" cy="880" rx="110" ry="60" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="1420" cy="822" r="42" fill="#6f6256" stroke="{K}"'
                    f' stroke-width="4.5"/>'
                    f'<path d="M1440,786 l10,-46 l20,42 Z" fill="#6f6256" stroke="{K}"'
                    f' stroke-width="3.4"/>'
                    f'<path d="M1240,930 l-10,54 M1300,942 l-4,48 M1370,938 l8,46"'
                    f' stroke="#55493f" stroke-width="12"/>'
                    f'<rect x="1250" y="812" width="140" height="60" rx="10"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="4"/>')
    # ПАВЕЛ со спины вверх по тропе + СТРАЖНИК
    idt = A.ease(A.seg(t, .3, 3.2))
    px, py, ph_ = 760 + 150 * idt, 1000 - 60 * idt, 620
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#6f6354",
                           ph=.2, naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .30, 38, t, "#e8e2d6", "#6f6354", .2, 4)
    r2, (e2x, e2y), _ = _ruka(px, py, ph_, -1, ph_ * .22, -16, t, "#e8e2d6", "#6f6354", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y-290:.0f} l{10:.0f},{py-e1y+270:.0f}"'
                    f' stroke="#7d5636" stroke-width="13" stroke-linecap="round"/>')
    pl = 40 + 24 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<path d="M{px+30:.0f},{py-ph_*.66:.0f} q{-70-pl:.0f},{130:.0f}'
                    f' {-170-pl:.0f},{230:.0f} q{76:.0f},{22:.0f} {160:.0f},{-44:.0f} Z"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="4.5"/>')
    sx_, sy_, sh2 = px - 250, py + 34, 560
    s += SL(Z_SRED, figura(sx_, sy_, sh2, t, col="#5e564c", kant="#cfe4f5", ph=.6))
    r3, (e3x, e3y), _ = _ruka(sx_, sy_, sh2, 1, sh2 * .26, 24, t, "#5e564c", "#cfe4f5", .3, 4)
    r4, (e4x, e4y), _ = _ruka(sx_, sy_, sh2, -1, sh2 * .22, 40, t, "#5e564c", "#cfe4f5", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, f'<path d="M{e3x:.0f},{e3y-280:.0f} l{6:.0f},{sy_-e3y+250:.0f}"'
                    f' stroke="#6b4428" stroke-width="9"/>'
                    f'<path d="M{e3x-6:.0f},{e3y-280:.0f} l{10:.0f},{-54:.0f} l{14:.0f},{52:.0f} Z"'
                    f' fill="#c9ccd1" stroke="{K}" stroke-width="3.4"/>'
                    f'<ellipse cx="{e4x-16:.0f}" cy="{e4y+16:.0f}" rx="54" ry="64"'
                    f' fill="#8a7a52" stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="{e4x-16:.0f}" cy="{e4y+16:.0f}" r="16" fill="#c9a05a"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, ten(px, py + 6, 120, 20, .4) + ten(sx_, sy_ + 6, 110, 18, .4))
    # ОРЁЛ кружит
    oa = (t * .25) % 1.0
    ox_, oy_ = 400 + 900 * oa, 220 + 90 * math.sin(oa * 6.283)
    s += SL(Z_LETIT, f'<path d="M{ox_:.0f},{oy_:.0f} q{40:.0f},{-30:.0f} {80:.0f},{-6:.0f}'
                     f' q{-40:.0f},{14:.0f} {-80:.0f},{6:.0f} Z" fill="#3f3a33"/>'
                     f'<path d="M{ox_:.0f},{oy_:.0f} q{-40:.0f},{-30:.0f} {-80:.0f},{-6:.0f}'
                     f' q{40:.0f},{14:.0f} {80:.0f},{6:.0f} Z" fill="#3f3a33"/>'
                     f'<ellipse cx="{ox_:.0f}" cy="{oy_+4:.0f}" rx="16" ry="9"'
                     f' fill="#2b2419"/>')
    s += SL(Z_PERED, f'<path d="M-20,1080 q160,{-140:.0f} 300,{-80:.0f} l0,200 l-320,0 Z"'
                     f' fill="#4a4038" opacity=".92"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def posoh_u_steny_hizhiny(t):
    """Каменная хижина в горах: у стены стоит посох с дорожной сумой, на
    пороге сложен плащ. Светильник в оконце гаснет, над горами встаёт одна
    яркая звезда. Людей нет."""
    rnd = random.Random(1914)
    s = nebo("noch", t, True, 71)
    s += SL(Z_NEBO, luna_v_gorode(260, 170, t, .72, True))
    for i, (sx, sb, sh_) in enumerate(((-120, 700, 560), (1360, 720, 620))):
        s += SL(Z_DAL, f'<path d="M{sx:.0f},{sb:.0f} l{sh_*.48:.0f},{-sh_:.0f}'
                       f' l{sh_*.32:.0f},{sh_*.40:.0f} l{sh_*.30:.0f},{-sh_*.26:.0f}'
                       f' l{sh_*.52:.0f},{sh_*.86:.0f} Z" fill="#3a434e" stroke="{K}"'
                       f' stroke-width="5"/>'
                       f'<path d="M{sx+sh_*.48:.0f},{sb-sh_:.0f} l{sh_*.16:.0f},{sh_*.20:.0f}'
                       f' l{-sh_*.32:.0f},0 Z" fill="url(#sneg)" opacity=".85"/>')
    # ЗВЕЗДА встаёт над горами
    vst = A.ease(A.seg(t, 1.2, 1.6))
    zx, zy = 1180, 320 - 90 * vst
    s += SL(Z_NEBO, f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="{10+6*vst:.0f}"'
                    f' fill="#ffffff" opacity="{vst:.2f}"/>'
                    f'<path d="M{zx-70*vst:.0f},{zy:.0f} h{140*vst:.0f}'
                    f' M{zx:.0f},{zy-70*vst:.0f} v{140*vst:.0f}" stroke="#ffffff"'
                    f' stroke-width="4" opacity="{vst*.8:.2f}"/>'
                    f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="{46*vst:.0f}" fill="#cfe4f5"'
                    f' opacity="{vst*.22:.2f}"/>')
    # ХИЖИНА на пол-кадра
    hx, hy, hw, hh = 560, 320, 820, 540
    hiz = (f'<rect x="{hx:.0f}" y="{hy:.0f}" width="{hw:.0f}" height="{hh:.0f}"'
           f' fill="#6f6256" stroke="{K}" stroke-width="7"/>')
    hiz += kladka(hx, hy, hw, hh, 62, "url(#kamen)")
    hiz += (f'<path d="M{hx-70:.0f},{hy:.0f} l{hw*.5+70:.0f},{-200:.0f}'
            f' l{hw*.5+70:.0f},{200:.0f} Z" fill="#5e564c" stroke="{K}" stroke-width="6"/>')
    hiz += (f'<path d="M{hx-70:.0f},{hy:.0f} l{hw*.5+70:.0f},{-200:.0f}'
            f' l{hw*.5+70:.0f},{200:.0f}" fill="none" stroke="url(#sneg)"'
            f' stroke-width="22" opacity=".92"/>')
    hiz += (f'<path d="M{hx+300:.0f},{hy+hh:.0f} l0,-230 q{90:.0f},{-70:.0f} {180:.0f},0'
            f' l0,230 Z" fill="#3f352c" stroke="{K}" stroke-width="6"/>')
    for i in range(5):
        hiz += (f'<rect x="{hx+310+i*34:.0f}" y="{hy+hh-224:.0f}" width="26"'
                f' height="224" fill="#4a3f34" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_DAL, hiz)
    # ОКОНЦЕ: светильник догорает и гаснет
    gas = max(.0, 1 - A.ease(A.seg(t, 1.0, 1.8)))
    s += SL(Z_SRED, f'<rect x="{hx+600:.0f}" y="{hy+150:.0f}" width="140" height="130"'
                    f' rx="8" fill="#241c16" stroke="{K}" stroke-width="6"/>')
    if gas > .02:
        s += SL(Z_SRED, f'<g opacity="{gas:.2f}">' + svecha(hx + 670, hy + 268, t, .2, 1.3, 70)
                + teplo(hx + 670, hy + 230, 200, 170, .55 * gas) + '</g>')
    # ПОСОХ с сумой у стены — главный предмет
    kach = 1.6 * A.w(t, 2.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 400 1000)">'
                    f'<rect x="376" y="300" width="48" height="700" rx="20"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M370,300 q{34:.0f},{-54:.0f} {68:.0f},{-10:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="22"/>'
                    f'<path d="M400,470 q{110:.0f},{40:.0f} {160:.0f},{140:.0f}'
                    f' q{-20:.0f},{130:.0f} {-146:.0f},{134:.0f} q{-118:.0f},{-14:.0f}'
                    f' {-108:.0f},{-140:.0f} q{44:.0f},{-96:.0f} {94:.0f},{-134:.0f} Z"'
                    f' fill="#c9b78e" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M320,590 q{84:.0f},{-56:.0f} {162:.0f},{10:.0f}"'
                    f' fill="none" stroke="#8a7a52" stroke-width="12"/>'
                    f'<path d="M332,700 q{80:.0f},{26:.0f} {150:.0f},{-6:.0f}"'
                    f' fill="none" stroke="#a8956f" stroke-width="9"/></g>')
    # плащ на пороге, снег ложится
    s += SL(Z_SRED, f'<path d="M760,1010 q{140:.0f},{-56:.0f} {290:.0f},{-6:.0f}'
                    f' q{20:.0f},{60:.0f} {-10:.0f},{80:.0f} q{-150:.0f},{20:.0f}'
                    f' {-290:.0f},{-4:.0f} Z" fill="#9aa3a8" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M790,1000 q{130:.0f},{-40:.0f} {250:.0f},{-4:.0f}"'
                    f' fill="none" stroke="url(#sneg)" stroke-width="14" opacity=".9"/>')
    # вязанка хвороста, кувшин, следы только к двери
    s += SL(Z_SRED, f'<g transform="rotate(-8 1500 1000)">')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{1400+i*8:.0f},1040 q{70:.0f},{-30-i*4:.0f}'
                        f' {150:.0f},{-16:.0f}" fill="none" stroke="#6b5230"'
                        f' stroke-width="7"/>')
    s += SL(Z_SRED, f'<rect x="1470" y="1000" width="22" height="46" rx="6"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, krynka_moloka(1700, 1046, .9, t, False, False, .4))
    s += SL(Z_SRED, sledy_valenok(1880, 1070, 1000, 1000, 7, 73, "#8aa0b4", 1.1))
    s += SL(Z_SRED, sneg_lezhit(980, 26, "url(#sneg)"))
    s += SL(Z_SRED, inej_mel(23, 60, 960, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 30, 17, .55, .6))
    s += ramka_pp("oba", "#0e0c0b", .55)
    s += vinetka(.46)
    return s


def chelovek_protiv_vetra(t):
    """Навстречу человеку дует рисованный ветер-великан с надутыми щеками:
    гонит пыль и листья, срывает шапки с прохожих и поворачивает их назад.
    Человек стоит прямо, обе руки на посохе, ноги упёрты в землю."""
    rnd = random.Random(1915)
    s = nebo("sumer", t, False, 73)
    s += oblaka(t, 110, 7, 67, .50)
    s += SL(Z_DAL, ulica_dal(40, 520, 820, t, False, 31))
    s += SL(Z_DAL, izba_snaruzhi(250, 560, 260, t, True, True, 47)
            + dym(276, 420, t, 6, .24, 240, .44, "#d7dee6", .9))
    # ВЕТЕР-ВЕЛИКАН справа: лицо из туч с надутыми щеками
    dut = .5 + .5 * A.w(t, 1.2, .0)
    vx, vy = 1600, 330
    vel = (f'<ellipse cx="{vx:.0f}" cy="{vy:.0f}" rx="{300+30*dut:.0f}"'
           f' ry="{230+20*dut:.0f}" fill="#8a98a8" opacity=".55"/>')
    vel += (f'<ellipse cx="{vx:.0f}" cy="{vy:.0f}" rx="{230+20*dut:.0f}"'
            f' ry="{180+14*dut:.0f}" fill="#9fb0c0" opacity=".65"/>')
    for i in (-1, 1):
        vel += (f'<ellipse cx="{vx+i*110:.0f}" cy="{vy+30:.0f}" rx="{70+26*dut:.0f}"'
                f' ry="{58+20*dut:.0f}" fill="#b4c2d0" opacity=".75"/>')
        vel += (f'<path d="M{vx+i*96:.0f},{vy-40:.0f} q{-i*26:.0f},{18:.0f} {-i*52:.0f},{2:.0f}"'
                f' fill="none" stroke="#5e6a78" stroke-width="9"/>')
    vel += (f'<ellipse cx="{vx-60:.0f}" cy="{vy+74:.0f}" rx="{44+16*dut:.0f}"'
            f' ry="{30+10*dut:.0f}" fill="#4a5664"/>')
    for i in range(7):
        d = ((t * 1.1 + i / 7.0) % 1.0)
        vel += (f'<path d="M{vx-100-900*d:.0f},{vy+90+40*math.sin(i+d*6):.0f}'
                f' q{-120:.0f},{-26:.0f} {-240:.0f},{6:.0f}" fill="none" stroke="#cfd6de"'
                f' stroke-width="{10-6*d:.1f}" opacity="{(1-d)*.6:.2f}"/>')
    s += SL(Z_DAL, vel)
    # дорога, пыль и листья по ветру
    s += SL(Z_SRED, _merzlaya_zemlya(620, 29, True))
    for i in range(26):
        d = ((t * 1.4 + i / 26.0) % 1.0)
        lx = 1900 - 2000 * d
        ly = 700 + 300 * ((i * 7) % 10) / 10.0 + 40 * math.sin(d * 7 + i)
        s += SL(Z_LETIT, f'<path d="M{lx:.0f},{ly:.0f} l{18:.0f},{-12:.0f} l{6:.0f},{14:.0f}'
                         f' l{-16:.0f},{8:.0f} Z" fill="{"#9a5a28" if i%2 else "#b4762f"}"'
                         f' opacity="{.5+.4*(1-d):.2f}"/>')
    # ПРОХОЖИЕ-СИЛУЭТЫ, которых разворачивает; шапки летят
    for i, (hx, hy, hh) in enumerate(((320, 980, 420), (560, 1010, 450))):
        pov = A.ease(A.seg(t, .5 + i * .3, 1.0))
        s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a4450", kant="#cfe4f5",
                               ph=i * .4, naklon=5.0 + 4 * pov))
        rk, (ex, ey), _ = _ruka(hx, hy, hh, 1, hh * .26, -30 + 40 * pov, t,
                                "#4a4450", "#cfe4f5", i * .3, 8)
        s += SL(Z_SRED, rk)
        s += SL(Z_SRED, f'<ellipse cx="{hx-120-240*pov:.0f}" cy="{hy-hh-40-120*pov:.0f}"'
                        f' rx="40" ry="24" fill="#5e4a3a" stroke="{K}" stroke-width="3.6"'
                        f' transform="rotate({-40*pov:.0f} {hx-120-240*pov:.0f}'
                        f' {hy-hh-40-120*pov:.0f})"/>')
        s += SL(Z_SRED, ten(hx, hy + 6, 96, 17, .35))
    # ГЛАВНЫЙ: стоит прямо, обе руки на посохе, ноги расставлены
    px, py, ph_ = 1060, 1050, 660
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#8a7a52",
                           boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .26, 34, t, "#e8e2d6", "#8a7a52", .2, 2)
    r2, (e2x, e2y), _ = _ruka(px, py, ph_, -1, ph_ * .24, 40, t, "#e8e2d6", "#8a7a52", .5, 2)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{(e1x+e2x)/2:.0f},{e1y-240:.0f} l{4:.0f},{py-e1y+220:.0f}"'
                    f' stroke="#7d5636" stroke-width="15" stroke-linecap="round"/>')
    odzh = 30 + 18 * dut
    s += SL(Z_SRED, f'<path d="M{px-70:.0f},{py-ph_*.58:.0f} q{-60-odzh:.0f},{150:.0f}'
                    f' {-130-odzh:.0f},{250:.0f} q{70:.0f},{26:.0f} {140:.0f},{-30:.0f} Z"'
                    f' fill="#d8cbb0" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, ten(px, py + 8, 150, 24, .45))
    # согнутое дерево, сорванный навес, придорожный камень
    s += SL(Z_SRED, f'<g transform="rotate(-18 1810 1020)">'
            + goloe_derevo_ld(1810, 1020, 420, t, 29, 6, False) + '</g>')
    nav = 14 * A.w(t, 1.0, .3)
    s += SL(Z_SRED, f'<g transform="rotate({-20+nav:.1f} 200 760)">'
                    f'<path d="M80,760 q{120:.0f},{-46:.0f} {240:.0f},0 l{-18:.0f},{34:.0f}'
                    f' q{-100:.0f},{-30:.0f} {-204:.0f},0 Z" fill="#8a2f22" stroke="{K}"'
                    f' stroke-width="4.5"/></g>'
                    f'<rect x="86" y="760" width="14" height="230" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M1390,1070 q30,{-120:.0f} 140,{-100:.0f} q46,{64:.0f}'
                    f' {30:.0f},{100:.0f} Z" fill="#8a8078" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, dvorovye_veschi(560, 1070, 320, t, 31, ["korzina", "churbak"]))
    # ЦЕНТР КАДРА НЕ ПУСТОЙ: вдоль дороги камни, бурьян, рассыпанная поклажа
    for i, (kx, ky, ks) in enumerate(((760, 940, .8), (1280, 900, .6), (900, 1020, 1.0))):
        s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="{54*ks:.0f}"'
                        f' ry="{30*ks:.0f}" fill="#8a8078" stroke="{K}"'
                        f' stroke-width="{4*ks:.1f}"/>'
                        f'<path d="M{kx-40*ks:.0f},{ky-10*ks:.0f} q{40*ks:.0f},{-18*ks:.0f}'
                        f' {80*ks:.0f},{4*ks:.0f}" fill="none" stroke="#6f6256"'
                        f' stroke-width="{6*ks:.1f}"/>')
    s += SL(Z_SRED, _trava_suhaya(rnd, 11, 760, 1060, 620, 1860))
    s += SL(Z_SRED, f'<path d="M1180,1040 q{54:.0f},{18:.0f} {108:.0f},0 l{-10:.0f},{34:.0f}'
                    f' h{-88:.0f} Z" fill="#b08a52" stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<ellipse cx="{1196+i*22:.0f}" cy="{1044:.0f}" rx="13" ry="9"'
                        f' fill="#9a5a28" stroke="{K}" stroke-width="2.4"/>')
    s += SL(Z_SRED, inej_mel(37, 44, 820, 1070, 400, 1900))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="80" height="{H}" fill="#1d1611"'
                     f' opacity=".85"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def imya_nad_zamerzshey_rekoy(t):
    """Деревня над рекой: река на глазах затягивается льдом от берегов к
    середине, над ней из морозного пара складывается имя дня. Дед в тулупе
    показывает внуку на реку."""
    rnd = random.Random(1916)
    gor = 460
    s = nebo("rassv", t, False, 79)
    s += oblaka(t, 140, 5, 71, .40)
    s += SL(Z_DAL, ulica_dal(0, gor - 20, 980, t, True, 37))
    for i, (ix, iw) in enumerate(((1120, 300), (1500, 260), (1760, 240))):
        s += SL(Z_DAL, izba_snaruzhi(ix, gor + 10, iw, t, True, True, 41 + i)
                + dym(ix + iw * .1, gor - iw * .62, t, 6, .22, 270, .42, "#d7dee6", 1.0))
    s += SL(Z_DAL, goloe_derevo_ld(980, gor + 24, 300, t, 43, 6, True))
    # РЕКА: лёд идёт от берегов к середине
    led = A.ease(A.seg(t, .4, 3.2))
    s += SL(Z_SRED, f'<rect x="0" y="{gor+120:.0f}" width="{W}" height="{H-gor-120:.0f}"'
                    f' fill="{VODA}"/>')
    for i in range(16):
        yy = gor + 140 + i * 36
        s += SL(Z_SRED, f'<path d="M{rnd.uniform(-40,300):.0f},{yy:.0f}'
                        f' q{rnd.uniform(400,800):.0f},{rnd.uniform(-10,10):.0f}'
                        f' {rnd.uniform(1400,1960):.0f},{rnd.uniform(-8,8):.0f}"'
                        f' fill="none" stroke="#3f8a94" stroke-width="{rnd.uniform(2,5):.1f}"'
                        f' opacity=".55"/>')
    for i in (-1, 1):
        shir = 520 * led
        s += SL(Z_SRED, f'<path d="M{(0 if i<0 else W):.0f},{gor+120:.0f}'
                        f' q{i*shir*.5:.0f},{140:.0f} {i*shir*.2:.0f},{H-gor-120:.0f}'
                        f' l{-i*shir*.4:.0f},0 l0,{-(H-gor-120):.0f} Z"'
                        f' fill="url(#led)" opacity=".92"/>')
        s += SL(Z_SRED, f'<path d="M{(0 if i<0 else W)+i*shir*.2:.0f},{gor+140:.0f}'
                        f' q{i*60:.0f},{220:.0f} {-i*20:.0f},{430:.0f}" fill="none"'
                        f' stroke="#eaf6ff" stroke-width="8" opacity=".7"/>')
    s += SL(Z_SRED, korka_lda(960, 880, 300 * led + 60, 90, t, .2, .0, .8, .4))
    # ПАР над рекой складывается в полосы-слово (своих букв не рисуем)
    for i in range(7):
        d = A.ease(A.seg(t, 1.0 + i * .12, 1.0))
        px_ = 560 + i * 130
        s += SL(Z_SRED, f'<path d="M{px_:.0f},{gor+80:.0f} q{26:.0f},{-40*d:.0f}'
                        f' {54:.0f},{-14*d:.0f} q{-24:.0f},{30*d:.0f} {-54:.0f},{14*d:.0f} Z"'
                        f' fill="#eef6ff" opacity="{.55*d:.2f}"/>')
    s += SL(Z_SRED, tuman(t, gor + 60, .34, "#dde7f0"))
    # ДЕД показывает внуку на реку
    dx, dy, dh = 420, 1040, 660
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#4a4038", kant="#ffd9a8",
                           tulup=True, boroda=True, shapka=True, ph=.2))
    uk = A.ease(A.seg(t, .5, 1.2))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, 1, dh * .34, 20 - 36 * uk, t,
                              "#4a4038", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, -1, dh * .26, 54, t, "#4a4038", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x + 14, e1y + 6, 1.0, 10 - 30 * uk, "#6b4428", t, .2)
            + r2)
    vx, vy, vh = 250, 1060, 400
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#3f5a6a", kant="#ffd9a8",
                           shapka=True, ph=.6))
    s += SL(Z_SRED, f'<path d="M{e2x:.0f},{e2y:.0f} L{vx+70:.0f},{vy-vh*.52:.0f}"'
                    f' stroke="#4a4038" stroke-width="15" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(dx - 36, dy - dh * .80, t, .3, 1.0, .5)
            + para_izo_rta(vx - 24, vy - vh * .80, t, .8, .8, .45))
    s += SL(Z_SRED, ten(dx, dy + 6, 124, 21, .4) + ten(vx, vy + 6, 86, 15, .4))
    # лодки вверх дном, мостки, баня
    for i, (lx, ly, ls) in enumerate(((760, 1012, 1.0), (1040, 1046, .84))):
        s += SL(Z_SRED, f'<path d="M{lx-150*ls:.0f},{ly:.0f} q{150*ls:.0f},{-70*ls:.0f}'
                        f' {300*ls:.0f},0 Z" fill="#6b4428" stroke="{K}"'
                        f' stroke-width="{5*ls:.1f}"/>'
                        f'<path d="M{lx-120*ls:.0f},{ly-16*ls:.0f} q{120*ls:.0f},{-46*ls:.0f}'
                        f' {240*ls:.0f},0" fill="none" stroke="#54351f"'
                        f' stroke-width="{5*ls:.1f}"/>'
                        f'<path d="M{lx-150*ls:.0f},{ly:.0f} h{300*ls:.0f}"'
                        f' stroke="url(#sneg)" stroke-width="{10*ls:.1f}" opacity=".9"/>')
    s += SL(Z_SRED, mostki(1340, 920, 480, t, True, 150))
    s += SL(Z_SRED, kamysh(1880, 1060, 240, t, 7, 47, True)
            + kamysh(60, 1040, 200, t, 6, 53, True))
    s += SL(Z_SRED, dvorovye_veschi(1500, 1070, 360, t, 43, ["kadka", "vedro", "grabli"]))
    s += SL(Z_LETIT, sneg_letit(t, 18, 19, .40, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def posoh_i_led(t):
    """Кадр надвое: слева посох стоит прямо в камнях, на него давят
    рисованные ладони-тучи и не гнут; справа над первым льдом занесён
    валенок — и отступает на берег. Обе половины вспыхивают ровным светом."""
    rnd = random.Random(1917)
    s = nebo("sumer", t, True, 83)
    s += SL(Z_NEBO, f'<rect x="0" y="0" width="{W*.5:.0f}" height="{H}" fill="#2f3b4e"'
                    f' opacity=".45"/>')
    # ЛЕВАЯ ПОЛОВИНА: камни, посох, ладони-тучи
    for i, (sx, sb, sh_) in enumerate(((-120, 700, 520), (420, 760, 420))):
        s += SL(Z_DAL, f'<path d="M{sx:.0f},{sb:.0f} l{sh_*.5:.0f},{-sh_:.0f}'
                       f' l{sh_*.34:.0f},{sh_*.40:.0f} l{sh_*.46:.0f},{sh_*.60:.0f} Z"'
                       f' fill="#4a5664" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="0" y="880" width="{W*.5:.0f}" height="200" fill="#6f6256"/>')
    for i in range(14):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(0,950):.0f}"'
                        f' cy="{rnd.uniform(900,1070):.0f}" rx="{rnd.uniform(26,70):.0f}"'
                        f' ry="{rnd.uniform(12,30):.0f}" fill="#8a8078" stroke="{K}"'
                        f' stroke-width="4"/>')
    davl = .5 + .5 * A.w(t, 1.4, .0)
    s += SL(Z_SRED, f'<rect x="418" y="300" width="74" height="640" rx="28"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="7"/>'
                    f'<path d="M420,320 q{36:.0f},{-56:.0f} {72:.0f},{-10:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="24"/>'
                    f'<path d="M426,460 h58 M426,620 h58 M426,780 h58"'
                    f' stroke="#6b4428" stroke-width="7" opacity=".8"/>')
    for i, (lx, ly) in enumerate(((300, 330), (640, 360))):
        s += SL(Z_SRED, f'<ellipse cx="{lx:.0f}" cy="{ly+30*davl:.0f}" rx="170" ry="104"'
                        f' fill="#6a7888" opacity=".95" stroke="#48525e" stroke-width="7"/>')
        for k in range(4):
            s += SL(Z_SRED, f'<ellipse cx="{lx-54+k*36:.0f}" cy="{ly+86+30*davl:.0f}"'
                            f' rx="20" ry="46" fill="#8a98a8" opacity=".85"'
                            f' stroke="#5e6a78" stroke-width="4"/>')
    vsp = max(.0, A.w(t, 2.4, .2))
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W*.5:.0f}" height="{H}" fill="#ffe9ac"'
                    f' opacity="{.16*vsp:.2f}"/>')
    # ПРАВАЯ ПОЛОВИНА: пруд, ива, мостки, валенок отступает
    s += SL(Z_SRED, f'<rect x="{W*.5:.0f}" y="640" width="{W*.5:.0f}" height="440"'
                    f' fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(1430, 860, 360, 140, t, .3))
    s += SL(Z_SRED, f'<rect x="{W*.5:.0f}" y="560" width="{W*.5:.0f}" height="90"'
                    f' fill="#5f4a32"/>' + sneg_lezhit(600, 24, "url(#sneg)"))
    s += SL(Z_SRED, mostki(1540, 700, 380, t, True, 160))
    s += SL(Z_SRED, goloe_derevo_ld(1120, 660, 420, t, 59, 7, True))
    s += SL(Z_SRED, kamysh(1880, 900, 190, t, 6, 61, True))
    otst = A.ease(A.seg(t, .8, 1.4))
    s += SL(Z_PERED, _valenok(1420 + 180 * otst, 760 - 120 * (1 - otst) + 200 * otst,
                              .9, -10 + 16 * otst))
    s += SL(Z_SRED, f'<rect x="{W*.5:.0f}" y="0" width="{W*.5:.0f}" height="{H}"'
                    f' fill="#ffe9ac" opacity="{.16*vsp:.2f}"/>')
    # шов кадра: столб света по центру
    s += SL(Z_PERED, f'<rect x="{W*.5-7:.0f}" y="0" width="14" height="{H}"'
                     f' fill="#dcecf8" opacity=".5"/>')
    s += SL(Z_SRED, dvorovye_veschi(1640, 1066, 280, t, 59, ["vedro", "korzina"])
            + dvorovye_veschi(140, 1066, 300, t, 61, ["churbak", "metla"]))
    s += SL(Z_SRED, svecha(760, 1010, t, .1, 1.5, 90) + teplo(760, 970, 230, 200, .45))
    # ОБЕ ПОЛОВИНЫ ОБЖИТЫ: слева осыпь и сухие кусты, справа берег с вещами
    for i in range(10):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(40,900):.0f}"'
                        f' cy="{rnd.uniform(820,1060):.0f}" rx="{rnd.uniform(18,44):.0f}"'
                        f' ry="{rnd.uniform(9,20):.0f}" fill="#7a6e5e" stroke="{K}"'
                        f' stroke-width="3.4"/>')
    s += SL(Z_SRED, _trava_suhaya(rnd, 8, 860, 1050, 60, 900))
    s += SL(Z_SRED, _trava_suhaya(rnd, 7, 900, 1060, 1000, 1880))
    for i, (kx, ky) in enumerate(((1180, 980), (1300, 1016), (1640, 1004))):
        s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="{44-i*6:.0f}"'
                        f' ry="{22-i*3:.0f}" fill="#8a8078" stroke="{K}"'
                        f' stroke-width="3.6"/>')
    s += SL(Z_SRED, sanki_derev(1000, 1050, .72, t, .5, True))
    s += SL(Z_SRED, kamysh(1060, 1030, 150, t, 5, 67, True))
    s += SL(Z_SRED, sledy_valenok(1900, 1060, 1500, 940, 6, 71, "#8aa0b4", 1.0))
    s += SL(Z_SRED, inej_mel(73, 50, 840, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 24, 23, .45, .6))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def chetyre_ldinki_na_perilah(t):
    """Перила крыльца на пол-кадра: в ряд стоят на ребре четыре прозрачные
    льдинки, солнце бросает сквозь них радужные пятна на стену. Бабушка
    ставит четвёртую, внук считает. Правая треть оставлена под памятку."""
    rnd = random.Random(1918)
    s = nebo("rassv", t, False, 89)
    s += oblaka(t, 130, 4, 73, .34, "#ffe9c8")
    s += SL(Z_NEBO, f'<circle cx="300" cy="250" r="96" fill="#ffe9ac" opacity=".5"/>'
                    f'<circle cx="300" cy="250" r="58" fill="#fff4d8" opacity=".9"/>')
    s += SL(Z_DAL, ulica_dal(1180, 520, 740, t, True, 59))
    s += SL(Z_DAL, goloe_derevo_ld(1020, 560, 340, t, 67, 6, True))
    # СТЕНА ИЗБЫ с дверью — на неё ложатся радужные пятна
    s += SL(Z_SRED, brevna(0, 120, 1120, 740, 88, 2))
    s += SL(Z_SRED, dver(140, 300, 300, 520, .0, "url(#derev)", True, False))
    s += SL(Z_SRED, f'<path d="M120,286 h340 l-14,-30 h-312 Z" fill="{DOSKA2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        rx_ = 520 + i * 110
        s += SL(Z_SRED, f'<ellipse cx="{rx_:.0f}" cy="{420+((i*7)%4)*40:.0f}" rx="54"'
                        f' ry="34" fill="{["#c8301f","#d6a63f","#56763f","#3f6b7a","#8a2f8a"][i%5]}"'
                        f' opacity="{.22+.12*A.w(t,2.6,i*.3):.2f}"/>')
    # ПЕРИЛА крыльца во всю ширину
    s += SL(Z_SRED, f'<rect x="-20" y="820" width="1600" height="40" rx="10"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="-20" y="940" width="1600" height="26" rx="8"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="4.5"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="{30+i*170:.0f}" y="860" width="28" height="200"'
                        f' fill="{DOSKA}" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<rect x="-20" y="1040" width="1920" height="40" fill="{DOSKA2}"'
                    f' stroke="{K}" stroke-width="5"/>')
    # ЧЕТЫРЕ ЛЬДИНКИ на ребре; четвёртая встаёт
    stav = A.out(A.seg(t, .8, 1.1))
    for i in range(4):
        lx = 300 + i * 220
        ly = 820 - (0 if i < 3 else 150 * (1 - stav))
        op = 1.0 if i < 3 else stav
        s += SL(Z_SRED, f'<g opacity="{op:.2f}">'
                        f'<path d="M{lx-58:.0f},{ly:.0f} l{18:.0f},{-120:.0f}'
                        f' l{80:.0f},{-8:.0f} l{20:.0f},{128:.0f} Z" fill="#cfe4f5"'
                        f' opacity=".75" stroke="#eaf6ff" stroke-width="5"/>'
                        f'<path d="M{lx-40:.0f},{ly-110:.0f} l{14:.0f},{104:.0f}"'
                        f' fill="none" stroke="#ffffff" stroke-width="6" opacity=".7"/>'
                        f'<path d="M{lx+22:.0f},{ly-118:.0f} l{10:.0f},{112:.0f}"'
                        f' fill="none" stroke="#9fd0e4" stroke-width="4" opacity=".7"/>'
                        f'<ellipse cx="{lx-6:.0f}" cy="{ly-64:.0f}" rx="22" ry="34"'
                        f' fill="#ffffff" opacity="{.18+.12*A.w(t,3.0,i*.4):.2f}"/></g>')
    # БАБУШКА ставит четвёртую, ВНУК считает
    bx, by, bh = 1300, 1046, 620
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, -1, bh * .34, 6 + 16 * (1 - stav), t,
                              "#4a3a52", "#ffd9a8", .2, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x - 10, e1y + 12, 1.0, -14, TKAN, t, .3))
    vx, vy, vh = 980, 1060, 420
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#3f5a6a", kant="#ffd9a8",
                           shapka=True, ph=.7))
    r2, (e2x, e2y), _ = _ruka(vx, vy, vh, 1, vh * .28, -34, t, "#3f5a6a", "#ffd9a8", .4, 5)
    r3, (e3x, e3y), _ = _ruka(vx, vy, vh, -1, vh * .26, -30, t, "#3f5a6a", "#ffd9a8", .9, 5)
    s += SL(Z_SRED, r2 + varezhka(e2x + 6, e2y + 8, .8, 10, TKAN, t, .4)
            + r3 + varezhka(e3x - 6, e3y + 8, .8, -10, TKAN, t, .9))
    s += SL(Z_SRED, para_izo_rta(bx - 34, by - bh * .80, t, .3, 1.0, .5)
            + para_izo_rta(vx - 24, vy - vh * .80, t, .8, .8, .45))
    s += SL(Z_SRED, ten(bx, by + 6, 120, 20, .4) + ten(vx, vy + 6, 90, 16, .4))
    # веник, валенки, рябина, сугроб
    s += SL(Z_SRED, dvorovye_veschi(60, 1040, 300, t, 67, ["metla", "vedro"]))
    s += SL(Z_SRED, _valenok(560, 1040, .62, -4) + _valenok(630, 1044, .62, 6))
    s += SL(Z_SRED, ryabina(1700, 1000, t, 1.5, 6)
            + kalina_grozd(1740, 930, t, 1.0, 12, 71, .2))
    s += SL(Z_SRED, sneg_lezhit(1000, 28, "url(#sneg)"))
    s += SL(Z_SRED, dym(1240, 300, t, 6, .22, 280, .40, "#d7dee6", 1.0))
    s += SL(Z_LETIT, sneg_letit(t, 16, 29, .36, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def kabluk_nad_korkoy(t):
    """Плашка первого запрета: лужа под белой коркой с вмёрзшей травинкой,
    над ней занесён детский ботинок с каблуком на треть кадра — зависает и
    возвращается на землю. В кадре только ноги до колен."""
    rnd = random.Random(1919)
    s = nebo("den", t, False, 97)
    s += oblaka(t, 150, 5, 79, .42)
    s += SL(Z_DAL, zabor_shtaket(-40, 300, 2000, 260, 79, 64))
    s += SL(Z_DAL, goloe_derevo_ld(1600, 560, 420, t, 83, 6, True))
    s += SL(Z_DAL, izba_snaruzhi(300, 560, 260, t, True, True, 23)
            + dym(326, 420, t, 6, .22, 240, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(560, 83, False))
    # КОЛЕЯ и лужа под коркой
    for i in range(2):
        s += SL(Z_SRED, f'<path d="M-40,{900+i*90:.0f} Q700,{840+i*80:.0f}'
                        f' 1960,{880+i*86:.0f}" fill="none" stroke="#3f3122"'
                        f' stroke-width="{26-i*6:.0f}" opacity=".55"/>')
    s += SL(Z_SRED, f'<ellipse cx="780" cy="900" rx="430" ry="150" fill="#2f4a52"/>')
    s += SL(Z_SRED, korka_lda(780, 898, 400, 130, t, .1, .0, .95))
    s += SL(Z_SRED, f'<ellipse cx="780" cy="900" rx="438" ry="156" fill="none"'
                    f' stroke="#6b5438" stroke-width="20" opacity=".85"/>')
    s += SL(Z_SRED, _trava_suhaya(rnd, 6, 940, 1050, 400, 1200))
    # БОТИНОК с каблуком на треть кадра: зависает и возвращается
    viс = A.ease(A.seg(t, .4, 1.0)) - A.ease(A.seg(t, 1.8, 1.0))
    bx, by = 900, 860 - 240 * viс
    s += SL(Z_SRED, f'<g transform="rotate({-14+10*viс:.1f} {bx:.0f} {by:.0f})">'
                    f'<path d="M{bx-150:.0f},{by-40:.0f} q{40:.0f},{-120:.0f} {150:.0f},{-110:.0f}'
                    f' q{90:.0f},{10:.0f} {120:.0f},{90:.0f} l{10:.0f},{70:.0f}'
                    f' q{-130:.0f},{40:.0f} {-280:.0f},{-10:.0f} Z" fill="#8a5a38"'
                    f' stroke="{K}" stroke-width="8"/>'
                    f'<path d="M{bx-160:.0f},{by-28:.0f} h{300:.0f} q{20:.0f},{20:.0f}'
                    f' {4:.0f},{46:.0f} h{-300:.0f} Z" fill="#2b2016" stroke="{K}"'
                    f' stroke-width="6"/>'
                    f'<rect x="{bx+60:.0f}" y="{by+16:.0f}" width="70" height="56"'
                    f' rx="6" fill="#241c16" stroke="{K}" stroke-width="5"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{bx-96+i*52:.0f},{by-96:.0f} l{34:.0f},{14:.0f}"'
                        f' stroke="#f2ead6" stroke-width="9"/>')
    s += SL(Z_SRED, f'<path d="M{bx-150:.0f},{by-146:.0f} q{120:.0f},{-30:.0f}'
                    f' {250:.0f},{10:.0f} l{10:.0f},{-170:.0f} q{-140:.0f},{-30:.0f}'
                    f' {-270:.0f},{-6:.0f} Z" fill="#5a6a7a" stroke="{K}"'
                    f' stroke-width="6"/></g>')
    # вторая нога стоит на земле
    s += SL(Z_SRED, f'<path d="M420,1000 q{30:.0f},{-90:.0f} {120:.0f},{-84:.0f}'
                    f' q{70:.0f},{8:.0f} {94:.0f},{70:.0f} l{8:.0f},{54:.0f}'
                    f' q{-100:.0f},{30:.0f} {-222:.0f},{-8:.0f} Z" fill="#4a3526"'
                    f' stroke="{K}" stroke-width="7"/>'
                    f'<path d="M412,1012 h236 q{16:.0f},{16:.0f} {2:.0f},{38:.0f}'
                    f' h{-238:.0f} Z" fill="#2b2016" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M420,916 q{100:.0f},{-24:.0f} {210:.0f},{8:.0f}'
                    f' l{8:.0f},{-150:.0f} q{-120:.0f},{-26:.0f} {-226:.0f},{-4:.0f} Z"'
                    f' fill="#5a6a7a" stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, ten(520, 1050, 130, 20, .4) + ten(bx, 1046, 150, 22, .35 + .2 * (1 - viс)))
    # жёлтый лист, камешек, воробьи
    s += SL(Z_SRED, f'<path d="M1320,980 l{40:.0f},{-30:.0f} l{-8:.0f},{30:.0f}'
                    f' l{40:.0f},{-8:.0f} l{-30:.0f},{28:.0f} l{26:.0f},{20:.0f}'
                    f' l{-40:.0f},{4:.0f} l{-6:.0f},{30:.0f} l{-26:.0f},{-24:.0f}'
                    f' l{-32:.0f},{16:.0f} l{12:.0f},{-32:.0f} l{-34:.0f},{-8:.0f} Z"'
                    f' fill="#b4762f" stroke="#7d4a24" stroke-width="3.4"/>'
                    f'<ellipse cx="1480" cy="1020" rx="40" ry="24" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i, (vx, vy) in enumerate(((1560, 940), (1680, 980), (1760, 920))):
        s += SL(Z_SRED, ptica(vx, vy, t, 1.5, "#8a7a62", i * .3, "#6f6256"))
    s += SL(Z_SRED, dvorovye_veschi(100, 1066, 300, t, 71, ["vedro", "korzina"]))
    s += SL(Z_SRED, inej_mel(79, 50, 940, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 14, 31, .34, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def prud_v_razreze_ledyanaya_krysha(t):
    """Пруд в разрезе: сверху тонкая пластина льда как стеклянная крыша, под
    ней толща воды с зимними жильцами — караси, щука в корягах, рак, лягушка
    в иле. Круглый иллюминатор в толще — настоящий лёд изнутри."""
    rnd = random.Random(1920)
    s = nebo("sumer", t, False, 101)
    s += SL(Z_DAL, ulica_dal(40, 220, 820, t, True, 73))
    s += SL(Z_DAL, goloe_derevo_ld(1640, 250, 320, t, 89, 6, True))
    s += SL(Z_DAL, izba_snaruzhi(1200, 240, 240, t, True, True, 29)
            + dym(1224, 118, t, 5, .22, 220, .38, "#d7dee6", .9))
    s += SL(Z_SRED, mostki(180, 230, 420, t, True, 120))
    # ЛЕДЯНАЯ КРЫША
    s += SL(Z_SRED, f'<rect x="0" y="300" width="{W}" height="86" fill="url(#led)"'
                    f' stroke="#eaf6ff" stroke-width="6"/>')
    s += SL(Z_SRED, korka_lda(960, 344, 900, 40, t, .2, .0, .85))
    # ТОЛЩА ВОДЫ
    s += SL(Z_SRED, f'<rect x="0" y="386" width="{W}" height="{H-386}" fill="{VODA}"/>'
            + f'<rect x="0" y="386" width="{W}" height="{H-386}" fill="{VODA2}"'
              f' opacity=".45"/>')
    for i in range(13):
        yy = 420 + i * 54
        s += SL(Z_SRED, f'<path d="M{rnd.uniform(-40,200):.0f},{yy:.0f}'
                        f' q{rnd.uniform(400,900):.0f},{rnd.uniform(-14,14):.0f}'
                        f' {rnd.uniform(1500,1980):.0f},{rnd.uniform(-10,10):.0f}"'
                        f' fill="none" stroke="#3f8a94" stroke-width="{rnd.uniform(2,6):.1f}"'
                        f' opacity=".4"/>')
    # СВАИ МОСТКОВ уходят в воду, а вокруг них стоит рыба — середина кадра
    for i, px_ in enumerate((430, 560, 690)):
        s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="360" width="30" height="700"'
                        f' fill="#54351f" stroke="{K}" stroke-width="4" opacity=".92"/>')
        for k in range(5):
            s += SL(Z_SRED, f'<ellipse cx="{px_+15:.0f}" cy="{460+k*130:.0f}" rx="26"'
                            f' ry="11" fill="#3f7f6a" opacity=".7"/>')
    for i in range(11):
        kx = 760 + (i % 4) * 150 + rnd.uniform(-26, 26)
        ky = 430 + (i // 4) * 120 + rnd.uniform(-22, 22)
        pl = 9 * A.w(t, 2.2, i * .21)
        s += SL(Z_SRED, f'<path d="M{kx-40:.0f},{ky:.0f} q{40:.0f},{-26:.0f} {80:.0f},0'
                        f' q{-40:.0f},{26:.0f} {-80:.0f},0 Z" fill="#b58a3a"'
                        f' stroke="{K}" stroke-width="3.2"/>'
                        f'<path d="M{kx+40:.0f},{ky:.0f} l{22+pl:.0f},{-14:.0f} l0,{28:.0f} Z"'
                        f' fill="#9a722c" stroke="{K}" stroke-width="2.8"/>'
                        f'<circle cx="{kx-24:.0f}" cy="{ky-4:.0f}" r="4" fill="{K}"/>')
    s += SL(Z_SRED, f'<path d="M420,760 q{260:.0f},{-60:.0f} {560:.0f},{-10:.0f}'
                    f' q{180:.0f},{30:.0f} {300:.0f},{40:.0f} l0,{46:.0f}'
                    f' q{-300:.0f},{-30:.0f} {-860:.0f},{14:.0f} Z" fill="#54351f"'
                    f' stroke="{K}" stroke-width="5"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{520+i*170:.0f},760 q{30:.0f},{-70:.0f}'
                        f' {70:.0f},{-96:.0f}" fill="none" stroke="#46301c"'
                        f' stroke-width="11"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{460+i*150:.0f}" cy="{880+((i*5)%3)*40:.0f}"'
                        f' rx="{34+((i*3)%4)*10:.0f}" ry="{16+((i*7)%3)*6:.0f}"'
                        f' fill="#5e564c" stroke="{K}" stroke-width="3.4"/>')
    # ТОЛЩА НЕ ПУСТАЯ: заросли рдеста, коряги, камни на дне, цепочки пузырьков
    for i in range(14):
        wx = 60 + i * 136 + rnd.uniform(-24, 24)
        wh = rnd.uniform(200, 460)
        kach = 10 * A.w(t, rnd.uniform(3.0, 5.0), i * .2)
        s += SL(Z_SRED, f'<path d="M{wx:.0f},1070 q{kach:.0f},{-wh*.5:.0f}'
                        f' {kach*1.6:.0f},{-wh:.0f}" fill="none" stroke="#2f6b5a"'
                        f' stroke-width="{rnd.uniform(5,11):.1f}" opacity=".8"/>')
        for k in range(4):
            py_ = 1070 - wh * (.3 + k * .18)
            s += SL(Z_SRED, f'<ellipse cx="{wx+kach*(.4+k*.3):.0f}" cy="{py_:.0f}"'
                            f' rx="{rnd.uniform(8,16):.0f}" ry="{rnd.uniform(16,30):.0f}"'
                            f' fill="#3f7f6a" opacity=".75"'
                            f' transform="rotate({rnd.uniform(-40,40):.0f}'
                            f' {wx:.0f} {py_:.0f})"/>')
    for i in range(10):
        cx_ = rnd.uniform(60, 1860); cy_ = rnd.uniform(980, 1060)
        s += SL(Z_SRED, f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}"'
                        f' rx="{rnd.uniform(26,62):.0f}" ry="{rnd.uniform(12,26):.0f}"'
                        f' fill="#5e564c" stroke="{K}" stroke-width="3.4" opacity=".9"/>')
    for i in range(8):
        bx_ = 140 + i * 230
        for k in range(5):
            d = ((t * .5 + i * .13 + k * .08) % 1.0)
            s += SL(Z_SRED, f'<circle cx="{bx_+10*math.sin(k+d*6):.0f}"'
                            f' cy="{960-520*d:.0f}" r="{3+5*d:.1f}" fill="#cfe4f5"'
                            f' opacity="{(1-d)*.5:.2f}"/>')
    # ИЛЛЮМИНАТОР: вид, метка, обвязка
    ox, oy, od = 1300, 520, 420
    put = kontur_proema(ox, oy, od, od, "ellips")
    ill = (f'<path d="{put}" fill="#9fc4d8"/>')
    ill += (f'<path d="{put}" fill="#cfe4f5" opacity=".5"/>')
    ill += mesto_stoka(ox, oy, od, od, "ellips")
    ill += (f'<circle cx="{ox+od*.5:.0f}" cy="{oy+od*.5:.0f}" r="{od*.5:.0f}"'
            f' fill="none" stroke="#5e6a78" stroke-width="22"/>')
    for i in range(10):
        a = i * .628
        ill += (f'<circle cx="{ox+od*.5+(od*.5+11)*math.cos(a):.0f}"'
                f' cy="{oy+od*.5+(od*.5+11)*math.sin(a):.0f}" r="9" fill="#8a98a8"'
                f' stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, ill)
    # ЗИМНИЕ ЖИЛЬЦЫ
    for i in range(6):
        kx = 300 + (i % 3) * 120 + rnd.uniform(-20, 20)
        ky = 620 + (i // 3) * 90 + rnd.uniform(-20, 20)
        pl = 8 * A.w(t, 2.4, i * .25)
        s += SL(Z_SRED, f'<path d="M{kx-46:.0f},{ky:.0f} q{46:.0f},{-30:.0f} {92:.0f},0'
                        f' q{-46:.0f},{30:.0f} {-92:.0f},0 Z" fill="#b58a3a"'
                        f' stroke="{K}" stroke-width="3.4"/>'
                        f'<path d="M{kx+46:.0f},{ky:.0f} l{24+pl:.0f},{-16:.0f} l0,{32:.0f} Z"'
                        f' fill="#9a722c" stroke="{K}" stroke-width="3"/>'
                        f'<circle cx="{kx-28:.0f}" cy="{ky-4:.0f}" r="4.6" fill="{K}"/>')
    s += SL(Z_SRED, f'<path d="M620,860 q{150:.0f},{-40:.0f} {300:.0f},{-6:.0f}'
                    f' q{-140:.0f},{52:.0f} {-300:.0f},{6:.0f} Z" fill="#5f7a3a"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M920,854 l{50:.0f},{-26:.0f} l0,{52:.0f} Z" fill="#4a6a30"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="{664:.0f}" cy="{848:.0f}" r="6" fill="{K}"/>')
    for i in range(4):                 # коряги
        s += SL(Z_SRED, f'<path d="M{500+i*180:.0f},1070 q{40:.0f},{-120:.0f}'
                        f' {-10:.0f},{-200:.0f} q{60:.0f},{60:.0f} {90:.0f},{30:.0f}"'
                        f' fill="none" stroke="#54351f" stroke-width="13"/>')
    rak = 16 * A.ease(A.seg(t, .6, 1.6))
    s += SL(Z_SRED, f'<ellipse cx="{1700-rak:.0f}" cy="980" rx="54" ry="34"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{1650-rak:.0f},962 q{-40:.0f},{-20:.0f} {-60:.0f},{6:.0f}'
                    f' q{24:.0f},{16:.0f} {56:.0f},{10:.0f} Z" fill="#8a2f22"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{1650-rak:.0f},1000 q{-40:.0f},{20:.0f} {-62:.0f},{-2:.0f}'
                    f' q{26:.0f},{-18:.0f} {58:.0f},{-12:.0f} Z" fill="#8a2f22"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<rect x="0" y="1010" width="{W}" height="70" fill="#4a4038"/>'
                    f'<ellipse cx="1060" cy="1030" rx="70" ry="26" fill="#5f7a3a"'
                    f' opacity=".9" stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="1030" cy="1020" r="9" fill="#6f8c4a" stroke="{K}"'
                    f' stroke-width="2.6"/>'
                    f'<circle cx="1062" cy="1018" r="9" fill="#6f8c4a" stroke="{K}"'
                    f' stroke-width="2.6"/>')
    for i in range(16):
        d = ((t * .32 + i / 16.0) % 1.0)
        s += SL(Z_SRED, f'<circle cx="{120+i*118:.0f}" cy="{1000-560*d:.0f}"'
                        f' r="{4+7*d:.0f}" fill="#cfe4f5" opacity="{(1-d)*.55:.2f}"/>')
    s += SL(Z_SRED, kamysh(90, 300, 180, t, 6, 97, True)
            + kamysh(1880, 310, 200, t, 6, 101, True))
    s += SL(Z_PERED, f'<rect x="0" y="300" width="{W}" height="14" fill="#eaf6ff"'
                     f' opacity=".7"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def tropinka_v_obhod_pruda(t):
    """Пруд сверху: гладкая ледяная крыша, под ней ровно горят тёплые
    огоньки-окошки рыбьих домиков. По берегу дугой идёт натоптанная тропинка:
    баба с коромыслом и девочка с бидончиком обходят пруд. Следов на льду нет."""
    rnd = random.Random(1921)
    s = nebo("sumer", t, True, 103)
    s += SL(Z_DAL, ulica_dal(1100, 300, 820, t, True, 79))
    s += SL(Z_DAL, izba_snaruzhi(260, 320, 300, t, True, True, 31)
            + dym(290, 170, t, 6, .22, 250, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(360, 89, False))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="720" rx="760" ry="330" fill="url(#led)"'
                    f' stroke="#eaf6ff" stroke-width="10"/>')
    s += SL(Z_SRED, korka_lda(960, 720, 700, 300, t, .2, .0, .7, .3))
    # огоньки-окошки рыбьих домиков подо льдом
    for i in range(9):
        hx = 480 + (i % 5) * 220 + rnd.uniform(-30, 30)
        hy = 640 + (i // 5) * 130 + rnd.uniform(-20, 20)
        s += SL(Z_SRED, f'<path d="M{hx-50:.0f},{hy+40:.0f} l0,-56 l{50:.0f},{-40:.0f}'
                        f' l{50:.0f},{40:.0f} l0,{56:.0f} Z" fill="#3f5a6a"'
                        f' opacity=".85" stroke="#2b3f4a" stroke-width="4"/>'
                        f'<rect x="{hx-18:.0f}" y="{hy-10:.0f}" width="36" height="34"'
                        f' rx="4" fill="#ffd98a"'
                        f' opacity="{.65+.25*A.w(t,3.0,i*.3):.2f}"/>')
        s += SL(Z_SRED, teplo(hx, hy + 6, 90, 70, .25))
    # ТРОПИНКА дугой по берегу
    s += SL(Z_SRED, f'<path d="M-40,980 Q400,820 960,1060 Q1500,820 1960,960"'
                    f' fill="none" stroke="#8a7a62" stroke-width="80" opacity=".9"/>'
                    f'<path d="M-40,980 Q400,820 960,1060 Q1500,820 1960,960"'
                    f' fill="none" stroke="#6f6256" stroke-width="40" opacity=".7"/>')
    s += SL(Z_SRED, sledy_valenok(1880, 950, 1180, 1030, 8, 103, "#4a4038", 1.1))
    # БАБА с коромыслом и ДЕВОЧКА
    bx, by, bh = 1480, 1066, 640
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, 1, bh * .24, -36, t, "#4a3a52", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, -1, bh * .24, -34, t, "#4a3a52", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    kach = 6 * A.w(t, 1.3, .1)
    s += SL(Z_SRED, f'<path d="M{bx-230:.0f},{e1y-60:.0f} q{230:.0f},{-40:.0f}'
                    f' {460:.0f},0" fill="none" stroke="#8a6342" stroke-width="16"/>')
    for i, vx_ in enumerate((bx - 220, bx + 220)):
        s += SL(Z_SRED, f'<g transform="rotate({kach*(1 if i else -1):.1f} {vx_:.0f}'
                        f' {e1y-50:.0f})">'
                        f'<path d="M{vx_:.0f},{e1y-50:.0f} l0,{110:.0f}" stroke="#b9a37a"'
                        f' stroke-width="5" fill="none"/>'
                        f'<path d="M{vx_-40:.0f},{e1y+60:.0f} h80 l-8,86 h-64 Z"'
                        f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{vx_:.0f}" cy="{e1y+60:.0f}" rx="40" ry="12"'
                        f' fill="#8f979f" stroke="{K}" stroke-width="3.4"/></g>')
    dx, dy, dh = 1180, 1070, 400
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#6b4a5a", kant="#cfe4f5",
                           platok=True, ph=.8))
    r3, (e3x, e3y), _ = _ruka(dx, dy, dh, 1, dh * .26, 52, t, "#6b4a5a", "#cfe4f5", .3, 5)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x-22:.0f},{e3y+6:.0f} h44 l-5,56 h-34 Z"'
                         f' fill="#9aa3a8" stroke="{K}" stroke-width="3.6"/>'
                         f'<path d="M{e3x-22:.0f},{e3y+2:.0f} q{22:.0f},{-20:.0f}'
                         f' {44:.0f},0" fill="none" stroke="{CHUGUN}" stroke-width="4"/>')
    s += SL(Z_SRED, para_izo_rta(bx - 34, by - bh * .80, t, .3, 1.0, .5)
            + para_izo_rta(dx - 22, dy - dh * .80, t, .9, .8, .45))
    s += SL(Z_SRED, ten(bx, by + 4, 120, 20, .4) + ten(dx, dy + 4, 84, 15, .4))
    # собака бежит по тропинке
    beg = ((t * .5) % 1.0)
    sx_ = 1500 - 700 * beg
    s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="1000" rx="76" ry="38" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{sx_+66:.0f}" cy="962" r="30" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M{sx_+84:.0f},940 l{12:.0f},{-30:.0f} l{14:.0f},{28:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{sx_-70:.0f},986 q{-40:.0f},{-30:.0f} {-56:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#6b5230" stroke-width="9"/>'
                    f'<path d="M{sx_-40:.0f},1032 l-6,34 M{sx_+10:.0f},1038 l4,30'
                    f' M{sx_+54:.0f},1030 l8,34" stroke="#54351f" stroke-width="9"/>')
    # ивы, мостки, баня, поленница
    s += SL(Z_SRED, goloe_derevo_ld(180, 900, 420, t, 107, 7, True)
            + goloe_derevo_ld(1800, 930, 380, t, 109, 6, True))
    s += SL(Z_SRED, mostki(1420, 560, 380, t, True, 120))
    s += SL(Z_SRED, f'<rect x="60" y="560" width="260" height="150" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<circle cx="{78+(i%6)*46:.0f}" cy="{586+(i//6)*54:.0f}" r="22"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_LETIT, sneg_letit(t, 20, 37, .40, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def rybak_i_ledobur_u_steny(t):
    """Стена сарая: прислонён ледобур на пол-кадра, рядом удочки-коротышки,
    сачок, валенки с галошами. Рыбак берётся за ледобур и убирает руку, пока
    листки численника отлетают, а пруд за спиной белеет; потом берёт его."""
    rnd = random.Random(1922)
    s = nebo("den", t, False, 107)
    s += oblaka(t, 140, 5, 83, .42)
    # пруд за спиной белеет по ходу плана
    bel = A.ease(A.seg(t, 1.4, 4.4))
    s += SL(Z_DAL, f'<rect x="1180" y="420" width="740" height="300" fill="{VODA2}"/>')
    s += SL(Z_DAL, f'<rect x="1180" y="420" width="740" height="300" fill="url(#led)"'
                   f' opacity="{bel:.2f}"/>')
    s += SL(Z_DAL, f'<ellipse cx="1550" cy="560" rx="{320*bel:.0f}" ry="{90*bel:.0f}"'
                   f' fill="#eaf6ff" opacity="{.5*bel:.2f}"/>')
    s += SL(Z_DAL, kamysh(1240, 700, 170, t, 6, 113, True)
            + kamysh(1880, 712, 190, t, 6, 127, True))
    s += SL(Z_DAL, goloe_derevo_ld(1300, 740, 300, t, 113, 6, True))
    # СТЕНА САРАЯ
    s += SL(Z_SRED, doski(0, 180, 1180, 700, 72, True, "dosk"))
    s += SL(Z_SRED, f'<rect x="0" y="150" width="1180" height="40" fill="{DOSKA2}"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-20,150 q600,{-54:.0f} 1200,{-10:.0f} l0,20'
                    f' q-600,{-40:.0f} -1200,{10:.0f} Z" fill="url(#sneg)"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(880, 97, False))
    # ЛЕДОБУР у стены — главный предмет
    s += SL(Z_SRED, f'<g transform="rotate(-9 420 1000)">' + ledobur(420, 1000, 1.9, t, .1)
            + '</g>')
    # удочки, сачок, валенки с галошами
    for i, ux in enumerate((640, 700, 758)):
        s += SL(Z_SRED, f'<g transform="rotate({-13+i*4} {ux:.0f} 1000)">'
                        f'<rect x="{ux:.0f}" y="640" width="13" height="360" rx="6"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>'
                        f'<circle cx="{ux+6:.0f}" cy="700" r="12" fill="none"'
                        f' stroke="{ZHELEZ}" stroke-width="4"/>'
                        f'<path d="M{ux+6:.0f},640 q{30:.0f},{60:.0f} {12:.0f},{150:.0f}"'
                        f' fill="none" stroke="#cfd6db" stroke-width="2.4"/></g>')
    s += SL(Z_SRED, f'<g transform="rotate(14 900 1000)">'
                    f'<rect x="894" y="700" width="14" height="300" rx="6" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<ellipse cx="901" cy="672" rx="74" ry="48" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="8"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M{840+i*25:.0f},648 q{18:.0f},{40:.0f} {4:.0f},{66:.0f}"'
                        f' fill="none" stroke="#b9c2c8" stroke-width="2.4" opacity=".8"/>')
    s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, _valenok(1020, 1040, .9, -3) + _valenok(1100, 1044, .9, 5)
            + f'<ellipse cx="1020" cy="1046" rx="44" ry="16" fill="#23242a"'
              f' stroke="{K}" stroke-width="3.4"/>'
              f'<ellipse cx="1100" cy="1050" rx="44" ry="16" fill="#23242a"'
              f' stroke="{K}" stroke-width="3.4"/>')
    # ЧИСЛЕННИК на стене: листки отлетают (цифр не рисуем — только листки)
    s += SL(Z_SRED, f'<rect x="150" y="300" width="190" height="240" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="150" y="300" width="190" height="46" rx="8"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    for i in range(4):
        d = ((t * .5 + i * .25) % 1.0)
        s += SL(Z_LETIT, f'<rect x="{200+260*d:.0f}" y="{360+300*d*d:.0f}" width="120"'
                         f' height="150" rx="6" fill="#f2ead6" opacity="{(1-d)*.9:.2f}"'
                         f' transform="rotate({d*120:.0f} {260+260*d:.0f} {430+300*d*d:.0f})"'
                         f' stroke="{K}" stroke-width="3"/>')
    # РЫБАК: правая берётся за ледобур и убирает, левая рвёт листок
    ryx, ryy, ryh = 760, 1060, 660
    hvat = A.ease(A.seg(t, .6, .8)) - A.ease(A.seg(t, 1.8, .8)) + A.ease(A.seg(t, 5.6, .9))
    s += SL(Z_SRED, figura(ryx, ryy, ryh, t, col="#3f4a3a", kant="#ffd9a8",
                           shapka=True, tulup=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(ryx, ryy, ryh, -1, ryh * .32, 10 + 24 * hvat, t,
                              "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ryx, ryy, ryh, 1, ryh * .26, -22, t,
                              "#3f4a3a", "#ffd9a8", .7, 5)
    s += SL(Z_SRED, r1 + varezhka(e1x - 10, e1y + 10, 1.0, -16, "#5a4a3a", t, .2) + r2)
    s += SL(Z_SRED, para_izo_rta(ryx - 36, ryy - ryh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(ryx, ryy + 6, 130, 22, .45))
    s += SL(Z_SRED, dvorovye_veschi(1280, 1066, 420, t, 101, ["kadka", "vedro", "korzina"]))
    s += SL(Z_SRED, yaschik_rybaka(1500, 1040, .9, t, .25, .3))
    s += SL(Z_SRED, inej_mel(97, 46, 920, 1070))
    s += SL(Z_SRED, lampa(120, 240, t, 1.1, False) + teplo(120, 250, 190, 160, .35))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def doroga_v_shkolu_i_luzha(t):
    """Мостик в память: утренняя улица шестидесятых — забор, фонарный столб,
    тополь, почтовый ящик, вдали школа. Школьник с портфелем наступает
    каблуком на замёрзшую лужу: её овал — проём с настоящим треснувшим льдом."""
    rnd = random.Random(1923)
    s = nebo("rassv", t, False, 109)
    s += oblaka(t, 150, 5, 89, .40)
    s += SL(Z_DAL, panelka(1280, 560, 620, t, 5, True, 7))
    s += SL(Z_DAL, f'<rect x="120" y="330" width="760" height="260" rx="8"'
                   f' fill="#d8cbb0" stroke="{K}" stroke-width="6"/>')
    for i in range(10):
        s += SL(Z_DAL, f'<rect x="{160+i*70:.0f}" y="370" width="44" height="76" rx="5"'
                       f' fill="#8aa8b4" stroke="{K}" stroke-width="3.4"'
                       f' opacity="{.75+.2*A.w(t,4.0,i*.3):.2f}"/>')
    s += SL(Z_DAL, f'<rect x="420" y="268" width="170" height="64" rx="6"'
                   f' fill="#b9a082" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_DAL, goloe_derevo_ld(1000, 640, 520, t, 127, 8, False))
    s += SL(Z_SRED, zabor_shtaket(-40, 600, 1000, 200, 103, 60, "url(#derev)", False))
    s += SL(Z_SRED, f'<rect x="1140" y="300" width="22" height="520" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1150,300 q{40:.0f},{-30:.0f} {80:.0f},{-4:.0f}"'
                    f' fill="none" stroke="{BETON2}" stroke-width="12"/>')
    s += SL(Z_SRED, lampa(1232, 300, t, 1.2, True) + teplo(1232, 310, 220, 180, .35))
    s += SL(Z_SRED, f'<rect x="1500" y="640" width="120" height="150" rx="10"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1520" y="676" width="80" height="16" rx="4"'
                    f' fill="#2b2016"/>'
                    f'<rect x="1546" y="790" width="24" height="120" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(800, 113, False))
    s += SL(Z_SRED, f'<rect x="0" y="820" width="{W}" height="90" fill="#8a8078"'
                    f' opacity=".85"/>')
    # ЛУЖА-ПРОЁМ: вид, метка, кромка поверх
    lx, ly, lw, lh = 820, 700, 480, 360
    luzha = (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.54:.0f}"'
             f' ry="{lh*.52:.0f}" fill="#2f4a52"/>')
    luzha += korka_lda(lx + lw * .5, ly + lh * .5, lw * .48, lh * .46, t, .3, .0, .8)
    luzha += mesto_stoka(lx, ly, lw, lh, "ellips")
    luzha += (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.56:.0f}"'
              f' ry="{lh*.54:.0f}" fill="none" stroke="#6f6256" stroke-width="18"'
              f' opacity=".9"/>')
    s += SL(Z_SRED, luzha)
    # белые лучи разбегаются по льду от каблука
    luch_ = A.ease(A.seg(t, 1.0, .9))
    if luch_ > .02:
        s += SL(Z_PERED, treschina(lx + lw * .46, ly + lh * .40, 240 * luch_, 131, 6,
                                   "#ffffff", 5.0))
    # ШКОЛЬНИК: портфель в правой, левая в кармане, каблук на лужу
    shx, shy, shh = 660, 1040, 650
    nast = A.ease(A.seg(t, .5, .8))
    s += SL(Z_SRED, figura(shx, shy, shh, t, col="#6f6256", kant="#ffd9a8",
                           shapka=True, ph=.2, naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(shx, shy, shh, 1, shh * .28, 50, t, "#6f6256", "#ffd9a8", .2, 6)
    s += SL(Z_SRED, r1)
    kach = 7 * A.w(t, 1.1, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-60:.0f}" y="{e1y+10:.0f}" width="120" height="86"'
                    f' rx="10" fill="#6b4428" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{e1x-60:.0f},{e1y+40:.0f} h120" stroke="#54351f"'
                    f' stroke-width="6"/>'
                    f'<rect x="{e1x-16:.0f}" y="{e1y+32:.0f}" width="32" height="20"'
                    f' rx="4" fill="{MED}" stroke="{K}" stroke-width="2.6"/></g>')
    s += SL(Z_SRED, f'<path d="M{shx+70:.0f},{shy-120:.0f} q{60*nast:.0f},{40*nast:.0f}'
                    f' {140*nast:.0f},{66*nast:.0f}" fill="none" stroke="#6f6256"'
                    f' stroke-width="30" stroke-linecap="round"/>'
            + _valenok(shx + 210 * nast, shy - 40 + 36 * nast, .60, 20))
    s += SL(Z_SRED, para_izo_rta(shx - 32, shy - shh * .80, t, .4, .9, .5))
    s += SL(Z_SRED, ten(shx, shy + 6, 120, 20, .4))
    # голуби взлетают, скамейка, дворник-силуэт
    for i in range(4):
        vzl = A.ease(A.seg(t, 1.1 + i * .1, 1.0))
        gx = 1360 + i * 90 + 70 * vzl
        gy = 1000 - 260 * vzl
        s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="28" ry="18"'
                        f' fill="#9aa3a8" stroke="{K}" stroke-width="3"/>'
                        f'<circle cx="{gx+22:.0f}" cy="{gy-12:.0f}" r="12" fill="#9aa3a8"'
                        f' stroke="{K}" stroke-width="2.6"/>'
                        f'<path d="M{gx-4:.0f},{gy-6:.0f} q{18:.0f},{-26-20*vzl:.0f}'
                        f' {44:.0f},{-12:.0f}" fill="none" stroke="#cfd6de"'
                        f' stroke-width="10"/>')
    s += SL(Z_SRED, f'<rect x="120" y="920" width="300" height="20" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="140" y="940" width="20" height="90" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="380" y="940" width="20" height="90" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    dvx, dvy, dvh = 1760, 1050, 520
    s += SL(Z_SRED, figura(dvx, dvy, dvh, t, col="#4a4450", kant="#cfe4f5",
                           shapka=True, ph=.8))
    r2, (e2x, e2y), _ = _ruka(dvx, dvy, dvh, -1, dvh * .30, 40, t, "#4a4450", "#cfe4f5", .5, 6)
    s += SL(Z_SRED, r2 + f'<path d="M{e2x:.0f},{e2y:.0f} l{-120:.0f},{150:.0f}"'
                         f' stroke="#8a6342" stroke-width="10"/>')
    for i in range(8):
        s += SL(Z_SRED, f'<path d="M{e2x-120:.0f},{e2y+150:.0f} l{-30+i*8:.0f},{40:.0f}"'
                        f' stroke="#9a7c45" stroke-width="4" opacity=".9"/>')
    s += SL(Z_SRED, inej_mel(109, 40, 900, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def okrik_iz_okna(t):
    """Окно первого этажа с распахнутой створкой и столетником: бабушка
    высунулась по пояс и грозит свёрнутым полотенцем. Школьник у лужи
    оглядывается, втянув голову, мокрый ботинок тянет тёмный след."""
    rnd = random.Random(1924)
    s = nebo("rassv", t, False, 113)
    s += SL(Z_DAL, oblaka(t, 140, 4, 97, .36))
    # СТЕНА ДОМА во весь кадр с окном
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W}" height="760" fill="{BETON}"/>')
    for i in range(10):
        s += SL(Z_SRED, f'<path d="M0,{70+i*70:.0f} h{W}" stroke="{BETON2}"'
                        f' stroke-width="4" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="0" y="700" width="{W}" height="80" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="5"/>')
    ox, oy, ow, oh = 420, 180, 620, 500
    s += SL(Z_SRED, f'<rect x="{ox-30:.0f}" y="{oy-30:.0f}" width="{ow+60:.0f}"'
                    f' height="{oh+60:.0f}" rx="8" fill="#d8cbb0" stroke="{K}"'
                    f' stroke-width="6"/>'
                    f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="{ox+ow*.5:.0f}" y="{oy:.0f}" width="{ow*.5:.0f}"'
                    f' height="{oh:.0f}" fill="#9fc4d8" opacity=".55"'
                    f' transform="skewY(-6)" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="{ox-40:.0f}" y="{oy+oh:.0f}" width="{ow+80:.0f}"'
                    f' height="30" rx="5" fill="#e4d8bd" stroke="{K}" stroke-width="5"/>')
    # столетник на подоконнике
    s += SL(Z_SRED, f'<path d="M{ox+40:.0f},{oy+oh:.0f} h100 l-12,-70 h-76 Z"'
                    f' fill="#a8743c" stroke="{K}" stroke-width="4"/>')
    for i in range(6):
        a = -1.2 + i * .42
        s += SL(Z_SRED, f'<path d="M{ox+90:.0f},{oy+oh-66:.0f}'
                        f' q{40*math.sin(a):.0f},{-70:.0f} {70*math.sin(a):.0f},{-130:.0f}'
                        f' q{14:.0f},{30:.0f} {-26*math.sin(a):.0f},{130:.0f} Z"'
                        f' fill="#56763f" stroke="{K}" stroke-width="3.4"/>')
    # БАБУШКА высунулась по пояс и грозит полотенцем
    bx, by, bh = 760, oy + oh + 10, 560
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#8a2f22", kant="#ffd9a8",
                           platok=True, ph=.2))
    groz = A.w(t, .8, .0)
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, 1, bh * .30, -40 + 26 * groz, t,
                              "#8a2f22", "#ffd9a8", .2, 10)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, -1, bh * .24, 30, t, "#8a2f22", "#ffd9a8", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<g transform="rotate({-24+20*groz:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-16:.0f}" y="{e1y-10:.0f}" width="190" height="34"'
                    f' rx="16" fill="{RUSH}" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e1x+60:.0f},{e1y-10:.0f} v34 M{e1x+120:.0f},{e1y-10:.0f}'
                    f' v34" stroke="{TKAN}" stroke-width="6"/></g>')
    # СТЕНА ОБЖИТА: второе окно, водосточная труба, кусты, санки, ящик
    s += SL(Z_SRED, f'<rect x="1180" y="210" width="330" height="300" rx="6"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1150" y="180" width="390" height="34" rx="6"'
                    f' fill="#d8cbb0" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1180" y="210" width="330" height="300" fill="#9fc4d8"'
                    f' opacity=".35"/>'
                    f'<path d="M1345,210 v300 M1180,360 h330" stroke="#e4d8bd"'
                    f' stroke-width="12"/>'
                    f'<rect x="1150" y="510" width="390" height="26" rx="5"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<ellipse cx="1260" cy="420" rx="52" ry="40" fill="#56763f"'
                    f' opacity=".9" stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="1230" y="452" width="62" height="58" rx="6"'
                    f' fill="#a8743c" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<rect x="1620" y="0" width="40" height="780" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="1612" y="{90+i*130:.0f}" width="56" height="18"'
                        f' rx="4" fill="#8a8078" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M1620,780 q{-10:.0f},{40:.0f} {-46:.0f},{54:.0f}'
                    f' l{40:.0f},{20:.0f} q{40:.0f},{-26:.0f} {46:.0f},{-74:.0f} Z"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="4"/>')
    for i, (kx, kb, kh) in enumerate(((1100, 840, 180), (1290, 850, 150))):
        s += SL(Z_SRED, goloe_derevo_ld(kx, kb, kh, t, 131 + i, 5, True))
    s += SL(Z_SRED, sanki_derev(1180, 940, .74, t, .6, True))
    s += SL(Z_SRED, f'<rect x="1340" y="840" width="150" height="100" rx="8"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M1340,876 h150" stroke="#54351f" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="1690" y="300" width="170" height="220" rx="6"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M1710,{340+i*30:.0f} q{40:.0f},{-6:.0f} {80:.0f},0'
                        f' q{30:.0f},{6:.0f} {50:.0f},{-2:.0f}" fill="none"'
                        f' stroke="#8a7a62" stroke-width="4" opacity=".8"/>')
    # ШКОЛЬНИК оглядывается, портфель к груди, мокрый след
    shx, shy, shh = 1480, 1050, 620
    s += SL(Z_SRED, figura(shx, shy, shh, t, col="#6f6256", kant="#ffd9a8",
                           shapka=True, ph=.5, naklon=3.0))
    r3, (e3x, e3y), _ = _ruka(shx, shy, shh, -1, shh * .22, 16, t, "#6f6256", "#ffd9a8", .3, 4)
    r4, (e4x, e4y), _ = _ruka(shx, shy, shh, 1, shh * .20, 20, t, "#6f6256", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r3 + r4
            + f'<rect x="{shx-70:.0f}" y="{shy-shh*.52:.0f}" width="140" height="100"'
              f' rx="10" fill="#6b4428" stroke="{K}" stroke-width="4.5"/>'
              f'<path d="M{shx-70:.0f},{shy-shh*.52+34:.0f} h140" stroke="#54351f"'
              f' stroke-width="6"/>')
    s += SL(Z_SRED, para_izo_rta(shx - 34, shy - shh * .80, t, .5, 1.0, .5))
    # мокрый след за ботинком
    for i in range(6):
        s += SL(Z_SRED, f'<ellipse cx="{1700-i*86:.0f}" cy="{1056+((i*3)%2)*14:.0f}"'
                        f' rx="{40-i*4:.0f}" ry="{15-i:.0f}" fill="#4a4038"'
                        f' opacity="{.65-i*.08:.2f}"/>')
    s += SL(Z_SRED, f'<ellipse cx="1180" cy="1010" rx="220" ry="62" fill="#2f4a52"'
                    f' opacity=".9"/>' + korka_lda(1180, 1008, 200, 54, t, .2, .6, .85))
    # завалинка, кошка прячется, бельевая верёвка, скамейка
    s += SL(Z_SRED, f'<rect x="0" y="780" width="{W}" height="60" rx="8" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="5"/>')
    pryach = A.ease(A.seg(t, .9, 1.0))
    s += SL(Z_SRED, kot(330 - 120 * pryach, 780, t, 1.5, "#4a423a", False))
    s += SL(Z_SRED, f'<path d="M60,420 q400,{40:.0f} 320,{-120:.0f}" fill="none"'
                    f' stroke="#b9a37a" stroke-width="4"/>')
    for i, (px_, pw_) in enumerate(((120, 90), (240, 70), (330, 60))):
        kch = 5 * A.w(t, 2.2, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {px_+pw_*.5:.0f} 430)">'
                        f'<rect x="{px_:.0f}" y="430" width="{pw_:.0f}" height="130"'
                        f' rx="5" fill="{["#e8e2d6","#8aa8b4","#d6a63f"][i]}"'
                        f' stroke="{K}" stroke-width="3.6"/></g>')
    s += SL(Z_SRED, f'<rect x="1540" y="820" width="320" height="20" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1560" y="840" width="20" height="80" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<rect x="1820" y="840" width="20" height="80" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, dvorovye_veschi(140, 1066, 360, t, 113, ["vedro", "churbak", "metla"]))
    s += SL(Z_SRED, inej_mel(127, 40, 860, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def dvor_i_netronutaya_luzha(t):
    """Двор между двухэтажными домами: посреди гладкая нетронутая лужа на
    пол-кадра, вокруг кружком стоят пятеро детей — руки в карманах и за
    спиной, каждый косится на соседа. Самый маленький делает полшага."""
    rnd = random.Random(1925)
    s = nebo("den", t, False, 131)
    s += oblaka(t, 140, 5, 101, .42)
    s += SL(Z_DAL, f'<rect x="-20" y="150" width="900" height="520" rx="6"'
                   f' fill="#c3ab8a" stroke="{K}" stroke-width="6"/>'
                   f'<rect x="1020" y="190" width="920" height="490" rx="6"'
                   f' fill="#b9a082" stroke="{K}" stroke-width="6"/>')
    for i in range(16):
        dx_ = 20 + (i % 8) * 108; dy_ = 220 + (i // 8) * 220
        s += SL(Z_DAL, f'<rect x="{dx_:.0f}" y="{dy_:.0f}" width="66" height="96" rx="5"'
                       f' fill="#8aa8b4" stroke="{K}" stroke-width="3.4"'
                       f' opacity="{.7+.25*A.w(t,4.0,i*.27):.2f}"/>')
        s += SL(Z_DAL, f'<rect x="{1060+(i%8)*108:.0f}" y="{dy_+30:.0f}" width="64"'
                       f' height="92" rx="5" fill="#8aa8b4" stroke="{K}"'
                       f' stroke-width="3.4" opacity="{.7+.25*A.w(t,3.6,i*.31):.2f}"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(680, 137, False))
    # ЛУЖА на пол-кадра, гладкая и нетронутая
    s += SL(Z_SRED, f'<ellipse cx="960" cy="880" rx="520" ry="170" fill="#2f4a52"/>')
    s += SL(Z_SRED, korka_lda(960, 876, 490, 150, t, .1, .0, .95))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="880" rx="528" ry="176" fill="none"'
                    f' stroke="#6b5438" stroke-width="20" opacity=".85"/>')
    # ПЯТЕРО ДЕТЕЙ кружком
    deti = ((300, 1016, 430, "#8a2f22"), (560, 1060, 400, "#3f5a6a"),
            (1380, 1054, 420, "#6b3a6a"), (1640, 1010, 440, "#4a6a3a"),
            (960, 1076, 330, "#c8301f"))
    for i, (dx_, dy_, dh_, col) in enumerate(deti):
        shag = A.ease(A.seg(t, 1.2, 1.0)) if i == 4 else .0
        s += SL(Z_SRED, figura(dx_, dy_ - 10 * shag, dh_, t, col=col, kant="#ffd9a8",
                               shapka=True, ph=i * .3, naklon=1.5))
        rk, (ex, ey), _ = _ruka(dx_, dy_, dh_, 1 if i % 2 else -1, dh_ * .22,
                                48, t, col, "#ffd9a8", i * .2, 4)
        s += SL(Z_SRED, rk)
        s += SL(Z_SRED, para_izo_rta(dx_ - 22, dy_ - dh_ * .80, t, i * .3, .8, .45))
        s += SL(Z_SRED, ten(dx_, dy_ + 5, 80, 14, .35))
    s += SL(Z_SRED, f'<circle cx="960" cy="{1070-330-46:.0f}" r="16" fill="{RUSH}"'
                    f' stroke="{K}" stroke-width="3"/>')
    # песочница в инее, бельевые столбы, сарай, качели, кот на заборе
    s += SL(Z_SRED, f'<rect x="60" y="820" width="300" height="130" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="80" y="800" width="260" height="30" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="210" cy="860" rx="120" ry="34" fill="#d8cbb0"'
                    f' opacity=".9"/>')
    for i, px_ in enumerate((1640, 1840)):
        s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="640" width="24" height="330"'
                        f' fill="{BETON2}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M1652,660 q100,{40:.0f} 200,{-10:.0f}" fill="none"'
                    f' stroke="#b9a37a" stroke-width="4"/>')
    for i, (px_, pw_, col) in enumerate(((1670, 70, "#e8e2d6"), (1760, 60, "#8aa8b4"))):
        kch = 6 * A.w(t, 2.4, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {px_+pw_*.5:.0f} 672)">'
                        f'<rect x="{px_:.0f}" y="672" width="{pw_:.0f}" height="120"'
                        f' rx="5" fill="{col}" stroke="{K}" stroke-width="3.4"/></g>')
    s += SL(Z_SRED, f'<rect x="1380" y="690" width="60" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1386,690 l-6,-120 M1434,690 l6,-120" stroke="#6b5230"'
                    f' stroke-width="5"/>')
    s += SL(Z_SRED, zabor_shtaket(-40, 700, 420, 150, 139, 58))
    s += SL(Z_SRED, kot(180, 700, t, 1.3, "#4a423a", False))
    s += SL(Z_SRED, dym(1500, 240, t, 6, .22, 260, .38, "#d7dee6", 1.0))
    s += SL(Z_SRED, inej_mel(137, 50, 940, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 14, 41, .32, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def ldinka_protiv_solnca(t):
    """Девочка держит перед лицом большую льдинку обеими варежками и смотрит
    сквозь неё на солнце: льдинка — круглый проём с настоящим кадром. Над
    ней по словам встают три значка: след, ухо, льдинка с солнцем."""
    rnd = random.Random(1926)
    s = nebo("rassv", t, False, 139)
    s += oblaka(t, 150, 4, 103, .34, "#ffe9c8")
    s += SL(Z_NEBO, f'<circle cx="1480" cy="230" r="120" fill="#ffe9ac" opacity=".45"/>'
                    f'<circle cx="1480" cy="230" r="68" fill="#fff4d8" opacity=".9"/>')
    s += SL(Z_DAL, zabor_shtaket(-40, 420, 2000, 230, 149, 62))
    s += SL(Z_DAL, goloe_derevo_ld(300, 660, 420, t, 151, 7, True))
    s += SL(Z_DAL, izba_snaruzhi(1660, 650, 280, t, True, True, 37)
            + dym(1690, 500, t, 6, .22, 240, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(650, 149, True))
    # проломленная лужа рядом, воробьи
    s += SL(Z_SRED, f'<ellipse cx="420" cy="980" rx="250" ry="80" fill="#2f4a52"/>'
            + korka_lda(420, 978, 230, 70, t, .4, .85))
    for i, (vx, vy) in enumerate(((620, 940), (700, 980), (760, 920))):
        s += SL(Z_SRED, ptica(vx, vy, t, 1.4, "#8a7a62", i * .3, "#6f6256"))
    # ДЕВОЧКА с льдинкой: проём-круг 420 по центру
    dx, dy, dh = 1060, 1066, 700
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#8a2f22", kant="#ffd9a8",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, 1, dh * .28, -42, t, "#8a2f22", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, -1, dh * .28, -46, t, "#8a2f22", "#ffd9a8", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    lx, ly, ld = dx - 210, dy - dh * .95, 420
    put = kontur_proema(lx, ly, ld, ld, "ellips")
    ldin = (f'<path d="{put}" fill="#9fc4d8"/>')
    ldin += (f'<path d="{put}" fill="#eaf6ff" opacity=".45"/>')
    ldin += mesto_stoka(lx, ly, ld, ld, "ellips")
    ldin += (f'<circle cx="{lx+ld*.5:.0f}" cy="{ly+ld*.5:.0f}" r="{ld*.5:.0f}"'
             f' fill="none" stroke="#dcecf8" stroke-width="18" opacity=".9"/>')
    ldin += (f'<path d="M{lx+40:.0f},{ly+ld*.78:.0f} q{ld*.26:.0f},{-26:.0f}'
             f' {ld*.5:.0f},{-6:.0f}" fill="none" stroke="#ffffff" stroke-width="10"'
             f' opacity=".45"/>')
    s += SL(Z_SRED, ldin)
    s += SL(Z_SRED, varezhka(e1x + 6, e1y + 10, 1.1, 16, TKAN, t, .2)
            + varezhka(e2x - 6, e2y + 10, 1.1, -16, TKAN, t, .6))
    s += SL(Z_SRED, _valenok(dx - 54, dy, .64, -3) + _valenok(dx + 36, dy + 4, .64, 4))
    s += SL(Z_SRED, para_izo_rta(dx - 30, dy - dh * .74, t, .5, .9, .45))
    s += SL(Z_SRED, ten(dx, dy + 6, 130, 22, .45))
    # ТРИ ЗНАЧКА встают по словам: след, ухо, льдинка с солнцем
    for i, zx in enumerate((300, 560, 820)):
        vst = A.out(A.seg(t, .6 + i * .5, .6))
        if vst < .02:
            continue
        zy = 300
        s += SL(Z_SRED, f'<g opacity="{vst:.2f}" transform="translate(0,{40*(1-vst):.0f})">'
                        f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="86" fill="#f2ead6"'
                        f' stroke="{K}" stroke-width="5"/>')
        if i == 0:
            s += SL(Z_SRED, f'<ellipse cx="{zx:.0f}" cy="{zy+14:.0f}" rx="34" ry="20"'
                            f' fill="#4a3526"/>'
                            f'<ellipse cx="{zx:.0f}" cy="{zy-18:.0f}" rx="26" ry="16"'
                            f' fill="#4a3526"/>')
        elif i == 1:
            s += SL(Z_SRED, f'<path d="M{zx-20:.0f},{zy+40:.0f} q{-40:.0f},{-60:.0f}'
                            f' {10:.0f},{-80:.0f} q{50:.0f},{-20:.0f} {50:.0f},{30:.0f}'
                            f' q0,{30:.0f} {-26:.0f},{30:.0f}" fill="none" stroke="#8a5a3a"'
                            f' stroke-width="11"/>')
        else:
            s += SL(Z_SRED, f'<path d="M{zx-40:.0f},{zy+30:.0f} l{14:.0f},{-80:.0f}'
                            f' l{56:.0f},{-6:.0f} l{14:.0f},{86:.0f} Z" fill="#cfe4f5"'
                            f' stroke="#eaf6ff" stroke-width="5"/>'
                            f'<circle cx="{zx+4:.0f}" cy="{zy-10:.0f}" r="18"'
                            f' fill="#ffe9ac" opacity=".9"/>')
        s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, ryabina(1820, 940, t, 1.4, 6)
            + kalina_grozd(1850, 880, t, 1.0, 11, 157, .4))
    s += SL(Z_SRED, dvorovye_veschi(120, 1066, 340, t, 149, ["vedro", "korzina"]))
    s += SL(Z_SRED, inej_mel(151, 46, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def babushka_rasskazyvaet_vnuku_u_luzh(t):
    """Дорожка у подъезда: внук уже поднял ногу над лужей, бабушка приседает
    рядом и показывает на лёд. Над ними всплывает рисованная картинка —
    пруд в разрезе со спящими рыбами; внук опускает ногу и слушает."""
    rnd = random.Random(1927)
    s = nebo("den", t, False, 151)
    s += oblaka(t, 140, 5, 107, .40)
    s += SL(Z_DAL, panelka(60, 520, 820, t, 5, True, 11))
    s += SL(Z_DAL, panelka(1140, 540, 760, t, 4, True, 13))
    s += SL(Z_SRED, _merzlaya_zemlya(620, 157, False))
    s += SL(Z_SRED, f'<rect x="0" y="700" width="{W}" height="140" fill="#9aa3a8"'
                    f' opacity=".85"/>'
                    f'<path d="M0,700 h{W}" stroke="#8a8078" stroke-width="7"/>')
    # ЛУЖА
    s += SL(Z_SRED, f'<ellipse cx="760" cy="900" rx="330" ry="110" fill="#2f4a52"/>'
            + korka_lda(760, 898, 310, 100, t, .2, .0, .9))
    # КАРТИНКА-ВСПЛЫВАШКА: пруд в разрезе со спящими рыбами
    vsp = A.out(A.seg(t, 1.4, 1.2))
    if vsp > .02:
        kx, ky, kw, kh = 1180, 180, 620, 380
        s += SL(Z_SRED, f'<g opacity="{vsp:.2f}" transform="translate(0,{60*(1-vsp):.0f})">'
                        f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw:.0f}" height="{kh:.0f}"'
                        f' rx="14" fill="#cfe4f5" stroke="{K}" stroke-width="6"/>'
                        f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw:.0f}" height="{kh*.22:.0f}"'
                        f' fill="url(#led)"/>'
                        f'<rect x="{kx:.0f}" y="{ky+kh*.22:.0f}" width="{kw:.0f}"'
                        f' height="{kh*.78:.0f}" fill="{VODA}"/>')
        for i in range(5):
            fx = kx + 90 + (i % 3) * 170; fy = ky + 140 + (i // 3) * 110
            s += SL(Z_SRED, f'<path d="M{fx-36:.0f},{fy:.0f} q{36:.0f},{-22:.0f} {72:.0f},0'
                            f' q{-36:.0f},{22:.0f} {-72:.0f},0 Z" fill="#b58a3a"'
                            f' stroke="{K}" stroke-width="3"/>'
                            f'<circle cx="{fx-20:.0f}" cy="{fy-3:.0f}" r="3.6" fill="{K}"/>')
        s += SL(Z_SRED, f'<path d="M{kx+40:.0f},{ky+kh-30:.0f} q{kw*.5:.0f},{-40:.0f}'
                        f' {kw-80:.0f},{-10:.0f}" fill="none" stroke="#2f6b5a"'
                        f' stroke-width="9"/></g>')
    # ВНУК опускает ногу, БАБУШКА на корточках показывает
    opusk = A.ease(A.seg(t, 2.0, 1.2))
    vx, vy, vh = 840, 1040, 480
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#c8301f", kant="#ffd9a8",
                           shapka=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(vx, vy, vh, 1, vh * .26, -30 + 40 * opusk, t,
                              "#c8301f", "#ffd9a8", .2, 6)
    r2, (e2x, e2y), _ = _ruka(vx, vy, vh, -1, vh * .26, -26 + 36 * opusk, t,
                              "#c8301f", "#ffd9a8", .6, 6)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{vx+50:.0f},{vy-130:.0f} q{50*(1-opusk):.0f},{-60*(1-opusk):.0f}'
                    f' {110*(1-opusk):.0f},{-40*(1-opusk)+70*opusk:.0f}" fill="none"'
                    f' stroke="#c8301f" stroke-width="26" stroke-linecap="round"/>'
            + _valenok(vx + 160 * (1 - opusk) + 40 * opusk,
                       vy - 120 * (1 - opusk) + 110 * opusk, .58, 14))
    bx, by, bh = 540, 1056, 430
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd9a8",
                           platok=True, ph=.5, naklon=2.0))
    r3, (e3x, e3y), _ = _ruka(bx, by, bh, 1, bh * .40, 4, t, "#4a3a52", "#ffd9a8", .3, 4)
    r4, (e4x, e4y), _ = _ruka(bx, by, bh, -1, bh * .30, 28, t, "#4a3a52", "#ffd9a8", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, f'<path d="M{e4x:.0f},{e4y:.0f} L{vx-60:.0f},{vy-vh*.58:.0f}"'
                    f' stroke="#4a3a52" stroke-width="14" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(vx - 26, vy - vh * .80, t, .3, .8, .45)
            + para_izo_rta(bx - 26, by - bh * .80, t, .8, .9, .45))
    s += SL(Z_SRED, ten(vx, vy + 6, 100, 18, .4) + ten(bx, by + 6, 120, 20, .4))
    # скамейка, клумба в инее, урна, голуби
    s += SL(Z_SRED, f'<rect x="140" y="860" width="340" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="140" y="800" width="340" height="20" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="160" y="882" width="22" height="110" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="440" y="882" width="22" height="110" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<path d="M1300,1070 q{40:.0f},{-110:.0f} {170:.0f},{-104:.0f}'
                    f' q{130:.0f},{10:.0f} {160:.0f},{104:.0f} Z" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="5"/>')
    for i in range(7):
        s += SL(Z_SRED, _trava_suhaya(rnd, 1, 930, 980, 1340 + i * 50, 1380 + i * 50))
    s += SL(Z_SRED, f'<rect x="1700" y="900" width="110" height="140" rx="10"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="1690" y="884" width="130" height="22" rx="6"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="3.6"/>')
    for i, (gx, gy) in enumerate(((240, 1020), (330, 1046), (430, 1010))):
        s += SL(Z_SRED, ptica(gx, gy, t, 1.6, "#9aa3a8", i * .3, "#6f7a84"))
    s += SL(Z_SRED, inej_mel(157, 44, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def varezhka_stuchit_po_korke(t):
    """Та же лужа крупно, корка с вмёрзшим листом: внук на корточках легонько
    стучит по ней варежкой и наклоняет ухо, от каждого стука расходятся
    рисованные звуковые колечки. Бабушкин рукав рядом показывает «тише»."""
    rnd = random.Random(1928)
    s = nebo("den", t, False, 163)
    s += SL(Z_DAL, panelka(1280, 420, 640, t, 4, True, 17))
    s += SL(Z_DAL, zabor_shtaket(-40, 380, 1100, 170, 163, 60))
    s += SL(Z_SRED, _merzlaya_zemlya(520, 167, False))
    s += SL(Z_SRED, f'<rect x="0" y="640" width="{W}" height="60" fill="#9aa3a8"'
                    f' stroke="{K}" stroke-width="5"/>')
    # ЛУЖА КРУПНО с вмёрзшим листом
    s += SL(Z_SRED, f'<ellipse cx="880" cy="870" rx="640" ry="210" fill="#2f4a52"/>')
    s += SL(Z_SRED, korka_lda(880, 866, 600, 190, t, .2, .0, .95))
    s += SL(Z_SRED, f'<path d="M700,900 l{48:.0f},{-36:.0f} l{-10:.0f},{36:.0f}'
                    f' l{50:.0f},{-10:.0f} l{-36:.0f},{34:.0f} l{32:.0f},{24:.0f}'
                    f' l{-50:.0f},{4:.0f} l{-6:.0f},{36:.0f} l{-32:.0f},{-28:.0f}'
                    f' l{-38:.0f},{18:.0f} l{14:.0f},{-38:.0f} l{-42:.0f},{-10:.0f} Z"'
                    f' fill="#9a5a28" stroke="#7d4a24" stroke-width="4" opacity=".92"/>')
    s += SL(Z_SRED, f'<ellipse cx="880" cy="870" rx="650" ry="218" fill="none"'
                    f' stroke="#6b5438" stroke-width="22" opacity=".85"/>')
    # ВНУК на корточках: правая варежка стучит, левая на колене, ухо к луже
    stuk = abs(A.w(t, .9, .0))
    vx, vy, vh = 1240, 1056, 470
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#c8301f", kant="#ffd9a8",
                           shapka=True, ph=.2, naklon=3.0))
    r1, (e1x, e1y), _ = _ruka(vx, vy, vh, -1, vh * .42, 30 + 18 * stuk, t,
                              "#c8301f", "#ffd9a8", .1, 5)
    r2, (e2x, e2y), _ = _ruka(vx, vy, vh, 1, vh * .28, 58, t, "#c8301f", "#ffd9a8", .6, 3)
    s += SL(Z_SRED, r1 + varezhka(e1x - 8, e1y + 14, 1.15, -12 + 16 * stuk, TKAN, t, .1)
            + r2 + varezhka(e2x + 8, e2y + 12, 1.0, 12, TKAN, t, .6))
    # ЗВУКОВЫЕ КОЛЕЧКИ от стука
    for i in range(4):
        d = ((t * 1.1 + i * .25) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{e1x-10:.0f}" cy="{e1y+40:.0f}"'
                        f' rx="{60+260*d:.0f}" ry="{18+80*d:.0f}" fill="none"'
                        f' stroke="#eaf6ff" stroke-width="{7-4*d:.1f}"'
                        f' opacity="{(1-d)*.7:.2f}"/>')
    s += SL(Z_SRED, para_izo_rta(vx - 30, vy - vh * .74, t, .4, .9, .45))
    s += SL(Z_SRED, ten(vx, vy + 6, 120, 20, .4))
    # БАБУШКИН РУКАВ показывает «тише» — рука ничья (крупный план)
    ruk, (kx_, ky_) = rukav(1760, 700, 240, 150, t, "#4a3a52", "#ffd9a8", .3, 5, True)
    s += SL(Z_SRED, ruk + varezhka(kx_, ky_ + 10, 1.2, -40, TKAN, t, .3))
    # бордюр, жёлтые листья, камешек, воробей
    s += SL(Z_SRED, f'<rect x="0" y="1010" width="{W}" height="40" rx="6"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="5"/>')
    for i in range(8):
        lx_ = 120 + i * 230 + rnd.uniform(-30, 30)
        s += SL(Z_SRED, f'<path d="M{lx_:.0f},{1056+((i*5)%3)*8:.0f} l{30:.0f},{-22:.0f}'
                        f' l{-6:.0f},{22:.0f} l{32:.0f},{-6:.0f} l{-24:.0f},{20:.0f}'
                        f' l{20:.0f},{14:.0f} l{-30:.0f},{2:.0f} l{-4:.0f},{22:.0f}'
                        f' l{-20:.0f},{-18:.0f} l{-24:.0f},{12:.0f} l{8:.0f},{-24:.0f}'
                        f' l{-26:.0f},{-6:.0f} Z"'
                        f' fill="{["#b4762f","#9a5a28","#c08a3a"][i%3]}"'
                        f' stroke="#7d4a24" stroke-width="3"/>')
    s += SL(Z_SRED, f'<ellipse cx="560" cy="1046" rx="40" ry="24" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, ptica(380, 1000, t, 1.8, "#8a7a62", .2, "#6f6256"))
    s += SL(Z_SRED, dvorovye_veschi(120, 1060, 300, t, 167, ["vedro", "korzina"]))
    s += SL(Z_SRED, dym(1500, 180, t, 5, .22, 220, .36, "#d7dee6", .9))
    s += SL(Z_SRED, inej_mel(163, 44, 1000, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def bochka_u_saraya(t):
    """Развилка, свой дом: дождевая бочка под водостоком на пол-кадра, на
    воде тонкая корка. Хозяин заносит ковш и останавливается — листок
    численника отлетает на день назад, и он же вчера вычерпывает бочку ведром."""
    rnd = random.Random(1929)
    s = nebo("sumer", t, False, 167)
    s += oblaka(t, 130, 5, 109, .42)
    s += SL(Z_DAL, ulica_dal(1240, 430, 700, t, True, 83))
    s += SL(Z_DAL, goloe_derevo_ld(1480, 520, 360, t, 167, 6, True))
    # СТЕНА САРАЯ и водосточный жёлоб
    s += SL(Z_SRED, doski(0, 140, 1200, 740, 76, True, "dosk"))
    s += SL(Z_SRED, f'<path d="M-20,140 l620,-120 l620,120 Z" fill="#5e4430"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<path d="M-20,140 l620,-120 l620,120" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="18" opacity=".9"/>')
    s += SL(Z_SRED, f'<rect x="560" y="150" width="46" height="520" rx="8"'
                    f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M560,670 q{-6:.0f},{50:.0f} {-56:.0f},{64:.0f}'
                    f' l{40:.0f},{26:.0f} q{56:.0f},{-30:.0f} {62:.0f},{-90:.0f} Z"'
                    f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(860, 173, False))
    # БОЧКА на пол-кадра
    bx, by = 560, 1020
    boch = (f'<path d="M{bx-170:.0f},{by-440:.0f} q{-40:.0f},{220:.0f} {14:.0f},{440:.0f}'
            f' h{312:.0f} q{54:.0f},{-220:.0f} {14:.0f},{-440:.0f} Z"'
            f' fill="url(#derev)" stroke="{K}" stroke-width="7"/>')
    for k in (.18, .52, .86):
        boch += (f'<rect x="{bx-178+18*k:.0f}" y="{by-440+440*k:.0f}"'
                 f' width="{356-36*k:.0f}" height="20" fill="{ZHELEZ}" opacity=".95"/>')
    for i in range(7):
        boch += (f'<path d="M{bx-150+i*50:.0f},{by-434:.0f} q{-8:.0f},{220:.0f}'
                 f' {2:.0f},{428:.0f}" fill="none" stroke="#6b4428" stroke-width="4"'
                 f' opacity=".7"/>')
    boch += (f'<ellipse cx="{bx:.0f}" cy="{by-440:.0f}" rx="172" ry="48"'
             f' fill="#5f3f27" stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, boch)
    s += SL(Z_SRED, korka_lda(bx, by - 440, 150, 40, t, .2, .0, .95))
    # ХОЗЯИН с ковшом: заносит и останавливается
    hx, hy, hh = 1180, 1056, 680
    zanos = A.ease(A.seg(t, .4, .9)) - A.ease(A.seg(t, 2.0, .8))
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a3a", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .34, 30 - 46 * zanos, t,
                              "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .24, 48, t, "#3f4a3a", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{-90:.0f},{-20:.0f}"'
                    f' stroke="#8a6342" stroke-width="10"/>'
                    f'<path d="M{e1x-90:.0f},{e1y-20:.0f} q{-50:.0f},{10:.0f}'
                    f' {-60:.0f},{50:.0f} q{40:.0f},{30:.0f} {70:.0f},{-6:.0f} Z"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, para_izo_rta(hx - 36, hy - hh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    # ЧИСЛЕННИК: листок отлетает на день назад
    s += SL(Z_SRED, f'<rect x="880" y="260" width="170" height="220" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="880" y="260" width="170" height="44" rx="8"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="4"/>')
    d = ((t * .45) % 1.0)
    s += SL(Z_LETIT, f'<rect x="{900-200*d:.0f}" y="{320+260*d*d:.0f}" width="110"'
                     f' height="140" rx="6" fill="#f2ead6" opacity="{(1-d)*.9:.2f}"'
                     f' transform="rotate({-d*140:.0f} {955-200*d:.0f} {390+260*d*d:.0f})"'
                     f' stroke="{K}" stroke-width="3"/>')
    # «ВЧЕРА»: полупрозрачный силуэт с ведром вычерпывает бочку
    vch = max(.0, A.w(t, 3.0, .4))
    s += SL(Z_SRED, f'<g opacity="{.35*vch:.2f}">'
            + figura(820, 1040, 620, t, col="#6f7a84", kant="#cfe4f5", shapka=True, ph=.9)
            + '</g>')
    s += SL(Z_SRED, f'<g opacity="{.4*vch:.2f}">'
                    f'<path d="M700,760 h110 l-10,96 h-90 Z" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="755" cy="760" rx="55" ry="16" fill="#8f979f"'
                    f' stroke="{K}" stroke-width="3.4"/></g>')
    # лейка, грабли, поленница, кот
    s += SL(Z_SRED, f'<path d="M1480,1000 h130 l-12,66 h-106 Z" fill="#3f6b7a"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M1610,1012 q{60:.0f},{-10:.0f} {90:.0f},{30:.0f}"'
                    f' fill="none" stroke="#3f6b7a" stroke-width="10"/>'
                    f'<path d="M1480,996 q{64:.0f},{-54:.0f} {128:.0f},{-4:.0f}"'
                    f' fill="none" stroke="{CHUGUN}" stroke-width="6"/>')
    s += SL(Z_SRED, dvorovye_veschi(1700, 1066, 240, t, 173, ["grabli", "churbak"]))
    s += SL(Z_SRED, f'<rect x="60" y="880" width="260" height="170" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<circle cx="{80+(i%6)*46:.0f}" cy="{906+(i//6)*60:.0f}" r="23"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, kot(190, 880, t, 1.4, "#4a423a", True))
    s += SL(Z_SRED, lampa(1000, 200, t, 1.1, False) + teplo(1000, 210, 200, 170, .40))
    s += SL(Z_SRED, inej_mel(173, 42, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def luzha_u_podezda_k_poludnyu(t):
    """Развилка, город: бочка становится лужей у крыльца многоэтажки.
    Женщина с сумкой выходит из подъезда и обходит лужу по бордюру, а
    солнце идёт к полудню — корка подтаивает с краёв."""
    rnd = random.Random(1930)
    s = nebo("den", t, False, 173)
    s += oblaka(t, 140, 5, 113, .40)
    sol = A.ease(A.seg(t, .3, 4.0))
    s += SL(Z_NEBO, f'<circle cx="{420+900*sol:.0f}" cy="{300-120*sol:.0f}" r="110"'
                    f' fill="#ffe9ac" opacity=".45"/>'
                    f'<circle cx="{420+900*sol:.0f}" cy="{300-120*sol:.0f}" r="64"'
                    f' fill="#fff4d8" opacity=".9"/>')
    s += SL(Z_DAL, panelka(60, 760, 980, t, 5, True, 19))
    s += SL(Z_DAL, panelka(1500, 700, 420, t, 4, True, 23))
    # КРЫЛЬЦО подъезда
    s += SL(Z_SRED, f'<rect x="1060" y="400" width="420" height="420" rx="8"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="1140" y="470" width="260" height="350" rx="6"'
                    f' fill="#3f5a6a" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1270" y="470" width="130" height="350" rx="6"'
                    f' fill="#8aa8b4" opacity=".55" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1040" y="820" width="460" height="30" rx="6"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1060" y="850" width="420" height="26" rx="5"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1080" y="876" width="380" height="24" rx="5"'
                    f' fill="#7a736a" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(1270, 420, t, 1.0, True) + teplo(1270, 430, 180, 150, .34))
    s += SL(Z_SRED, _merzlaya_zemlya(880, 179, False))
    s += SL(Z_SRED, f'<rect x="0" y="920" width="{W}" height="36" rx="6"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="5"/>')
    # ЛУЖА: корка подтаивает с краёв
    tay = A.ease(A.seg(t, 1.0, 4.4))
    s += SL(Z_SRED, f'<ellipse cx="700" cy="1000" rx="420" ry="120" fill="#2f4a52"/>')
    s += SL(Z_SRED, korka_lda(700, 998, 390 * (1 - .32 * tay), 108 * (1 - .3 * tay),
                              t, .2, .0, .92))
    s += SL(Z_SRED, f'<ellipse cx="700" cy="1000" rx="424" ry="124" fill="none"'
                    f' stroke="#6f6256" stroke-width="16" opacity=".8"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{420+i*94:.0f}" cy="{1000+((i*7)%3-1)*44:.0f}"'
                        f' rx="{30*tay:.0f}" ry="{12*tay:.0f}" fill="#4a7a88"'
                        f' opacity="{.55*tay:.2f}"/>')
    # ЖЕНЩИНА обходит по бордюру
    obh = A.ease(A.seg(t, .6, 3.2))
    zx, zy, zh = 1260 - 420 * obh, 940 + 40 * obh, 640
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#6b3a6a", kant="#ffd9a8",
                           platok=False, ph=.3))
    r1, (e1x, e1y), _ = _ruka(zx, zy, zh, 1, zh * .28, 54, t, "#6b3a6a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(zx, zy, zh, -1, zh * .24, 34 - 30 * obh, t,
                              "#6b3a6a", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    kach = 8 * A.w(t, 1.2, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-48:.0f}" y="{e1y+6:.0f}" width="96" height="76"'
                    f' rx="10" fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{e1x-30:.0f},{e1y+6:.0f} q{30:.0f},{-40:.0f} {60:.0f},0"'
                    f' fill="none" stroke="#6b2419" stroke-width="7"/></g>')
    s += SL(Z_SRED, para_izo_rta(zx - 32, zy - zh * .80, t, .4, .9, .45))
    s += SL(Z_SRED, ten(zx, zy + 6, 120, 20, .4))
    # скамейка, урна, велосипед, рябина, голуби
    s += SL(Z_SRED, f'<rect x="180" y="800" width="330" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="180" y="740" width="330" height="20" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="200" y="822" width="22" height="100" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="470" y="822" width="22" height="100" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="580" y="800" width="100" height="130" rx="10"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<circle cx="1660" cy="960" r="76" fill="none" stroke="{CHUGUN}"'
                    f' stroke-width="11"/>'
                    f'<circle cx="1850" cy="960" r="76" fill="none" stroke="{CHUGUN}"'
                    f' stroke-width="11"/>'
                    f'<path d="M1660,960 L1760,860 L1850,960 M1760,860 L1790,900'
                    f' M1700,900 L1760,860" fill="none" stroke="#8a2f22"'
                    f' stroke-width="10"/>'
                    f'<path d="M1736,842 h60" stroke="{CHUGUN}" stroke-width="9"/>')
    s += SL(Z_SRED, ryabina(1480, 1000, t, 1.5, 6))
    for i, (gx, gy) in enumerate(((320, 1030), (420, 1056), (520, 1016))):
        s += SL(Z_SRED, ptica(gx, gy, t, 1.6, "#9aa3a8", i * .3, "#6f7a84"))
    s += SL(Z_SRED, inej_mel(179, 40, 950, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def pervyy_shag_na_led(t):
    """Плашка второго запрета: кромка тёмного тонкого льда у берега. Валенок
    с галошей ставится на лёд на треть кадра — лёд прогибается, из-под него
    выступает тёмная полоса, и валенок отдёргивается на берег."""
    rnd = random.Random(1931)
    s = nebo("sumer", t, False, 179)
    s += oblaka(t, 130, 5, 127, .42)
    s += SL(Z_DAL, ulica_dal(60, 330, 760, t, True, 89))
    s += SL(Z_DAL, goloe_derevo_ld(1540, 420, 440, t, 179, 7, True))
    s += SL(Z_DAL, izba_snaruzhi(1180, 380, 260, t, True, True, 41)
            + dym(1206, 240, t, 6, .22, 240, .40, "#d7dee6", .9))
    s += SL(Z_SRED, mostki(1300, 520, 500, t, True, 180))
    s += SL(Z_SRED, f'<rect x="0" y="430" width="{W}" height="650" fill="{VODA2}"/>')
    s += SL(Z_SRED, f'<rect x="0" y="430" width="{W}" height="300" fill="url(#led)"'
                    f' opacity=".8"/>')
    s += SL(Z_SRED, korka_lda(960, 600, 800, 150, t, .2, .0, .85, .35))
    # БЕРЕГ в инее со следами только до кромки
    s += SL(Z_SRED, f'<path d="M-40,1080 Q420,880 980,840 L1920,810 L1920,1080 Z"'
                    f' fill="#5f4a32" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-40,1080 Q420,890 980,850 L1920,820" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="26" opacity=".9"/>')
    s += SL(Z_SRED, sledy_valenok(1860, 1056, 900, 866, 8, 181, "#4a4038", 1.2))
    # ВАЛЕНОК на треть кадра: ставится и отдёргивается
    stav = A.ease(A.seg(t, .4, .8)) - A.ease(A.seg(t, 1.5, .7))
    vx, vy = 760, 780 + 60 * stav
    s += SL(Z_SRED, f'<g transform="rotate({-10+8*stav:.1f} {vx:.0f} {vy:.0f})">'
            + _valenok(vx, vy, 2.6, 0, "#b9ae9a")
            + f'<path d="M{vx-110:.0f},{vy-36:.0f} h{220:.0f} q{30:.0f},{20:.0f}'
              f' {6:.0f},{56:.0f} h{-230:.0f} Z" fill="#23242a" stroke="{K}"'
              f' stroke-width="7"/></g>')
    # прогиб льда и тёмная полоса из-под него
    s += SL(Z_SRED, f'<ellipse cx="{vx:.0f}" cy="{vy+70:.0f}" rx="{210+90*stav:.0f}"'
                    f' ry="{40+22*stav:.0f}" fill="#17424c" opacity="{.4+.4*stav:.2f}"/>')
    if stav > .1:
        s += SL(Z_SRED, treschina(vx, vy + 74, 300 * stav, 191, 5, "#eaf6ff", 4.5))
    s += SL(Z_SRED, f'<path d="M{vx-260:.0f},{vy+96:.0f} q{260:.0f},{40*stav:.0f}'
                    f' {520:.0f},{-10*stav:.0f}" fill="none" stroke="#0f2a32"'
                    f' stroke-width="{10+16*stav:.0f}" opacity=".75"/>')
    # сухой камыш, вмёрзшее ведёрко, ива
    s += SL(Z_SRED, kamysh(180, 900, 260, t, 8, 191, True)
            + kamysh(1880, 940, 230, t, 7, 193, True))
    s += SL(Z_SRED, f'<path d="M1120,700 h96 l-10,84 h-76 Z" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="1168" cy="700" rx="48" ry="14" fill="#8f979f"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<ellipse cx="1168" cy="706" rx="38" ry="10" fill="{INEY}"'
                    f' opacity=".8"/>'
                    f'<ellipse cx="1168" cy="790" rx="90" ry="22" fill="#cfe4f5"'
                    f' opacity=".55"/>')
    s += SL(Z_SRED, goloe_derevo_ld(300, 1020, 520, t, 197, 7, True))
    s += SL(Z_SRED, dvorovye_veschi(1560, 1070, 320, t, 181, ["kadka", "korzina"]))
    # ЦЕНТР КАДРА ОБЖИТ: битые льдины, коряги, вешки, перевёрнутая лодка
    for i in range(9):
        ox_ = 260 + i * 180 + rnd.uniform(-30, 30)
        oy_ = 520 + ((i * 5) % 3) * 70
        s += SL(Z_SRED, f'<path d="M{ox_:.0f},{oy_:.0f} l{rnd.uniform(60,120):.0f},'
                        f'{rnd.uniform(-20,14):.0f} l{rnd.uniform(-20,30):.0f},'
                        f'{rnd.uniform(30,56):.0f} l{rnd.uniform(-80,-50):.0f},'
                        f'{rnd.uniform(6,20):.0f} Z" fill="#dcecf8" stroke="#9fc4d8"'
                        f' stroke-width="4" opacity=".92"/>')
    for i, (kx_, kb_) in enumerate(((430, 780), (1120, 760), (1600, 790))):
        s += SL(Z_SRED, f'<path d="M{kx_:.0f},{kb_:.0f} q{40:.0f},{-80:.0f}'
                        f' {10:.0f},{-150:.0f} q{60:.0f},{54:.0f} {96:.0f},{26:.0f}"'
                        f' fill="none" stroke="#54351f" stroke-width="12"/>')
    for i, vx_ in enumerate((640, 980, 1320)):
        kch = 3.0 * A.w(t, 3.0, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {vx_:.0f} {660:.0f})">'
                        f'<rect x="{vx_:.0f}" y="440" width="12" height="220"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{vx_-22:.0f},440 q{28:.0f},{-30:.0f} {56:.0f},{-4:.0f}'
                        f' q{-26:.0f},{22:.0f} {-56:.0f},{4:.0f} Z" fill="#8a7a52"'
                        f' stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, f'<path d="M1480,700 q{140:.0f},{-60:.0f} {280:.0f},0 Z"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1480,700 h280" stroke="url(#sneg)" stroke-width="11"'
                    f' opacity=".9"/>')
    s += SL(Z_SRED, inej_mel(191, 50, 860, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 18, 43, .36, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def most_cherez_reku(t):
    """Деревянный мост через реку на пол-кадра: в пролёте под ним — проём с
    настоящей рекой в первом льду. По мосту идут мужик с лошадью и санями,
    баба с корзиной и мальчик у перил. На льду под мостом ни следа."""
    rnd = random.Random(1932)
    s = nebo("rassv", t, False, 181)
    s += oblaka(t, 140, 5, 131, .40)
    s += SL(Z_DAL, ulica_dal(1180, 300, 740, t, True, 97))
    s += SL(Z_DAL, izba_snaruzhi(160, 330, 280, t, True, True, 43)
            + dym(188, 190, t, 6, .22, 250, .40, "#d7dee6", .9))
    s += SL(Z_DAL, goloe_derevo_ld(600, 360, 320, t, 199, 6, True))
    # БЕРЕГА и река
    s += SL(Z_SRED, f'<rect x="0" y="420" width="{W}" height="660" fill="{VODA2}"/>')
    s += SL(Z_SRED, f'<path d="M0,420 q480,{40:.0f} 960,{10:.0f} T1920,430 L1920,560'
                    f' L0,560 Z" fill="#5f4a32"/>')
    # ПРОЁМ в пролёте: вид, метка, обвязка (мост поверх)
    px, py, pw, ph_ = 570, 640, 780, 300
    pr = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
          f' fill="#9fc4d8"/>')
    pr += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.4:.0f}"'
           f' fill="#c4d8e8"/>')
    pr += mesto_stoka(px, py, pw, ph_, "pryam")
    pr += (f'<rect x="{px-10:.0f}" y="{py-10:.0f}" width="{pw+20:.0f}"'
           f' height="{ph_+20:.0f}" fill="none" stroke="#54351f" stroke-width="20"/>')
    s += SL(Z_SRED, pr)
    s += SL(Z_SRED, korka_lda(300, 820, 260, 80, t, .3, .0, .8, .3)
            + korka_lda(1640, 840, 250, 76, t, .6, .0, .8, .3))
    # МОСТ на пол-кадра
    most = (f'<rect x="-20" y="520" width="1960" height="60" rx="6" fill="url(#derev)"'
            f' stroke="{K}" stroke-width="6"/>')
    for i in range(26):
        most += (f'<rect x="{-20+i*76:.0f}" y="516" width="62" height="68" rx="4"'
                 f' fill="{DOSKA}" stroke="{K}" stroke-width="2.6"/>')
    for i in range(14):
        most += (f'<rect x="{10+i*146:.0f}" y="440" width="18" height="90"'
                 f' fill="{DOSKA2}" stroke="{K}" stroke-width="3"/>')
    most += (f'<rect x="-20" y="430" width="1960" height="18" rx="6" fill="{DOSKA2}"'
             f' stroke="{K}" stroke-width="4"/>')
    for sx_ in (520, 1400):
        most += (f'<rect x="{sx_:.0f}" y="580" width="46" height="420" fill="#6b4428"'
                 f' stroke="{K}" stroke-width="5"/>'
                 f'<path d="M{sx_-30:.0f},660 h106" stroke="#54351f" stroke-width="12"/>')
    s += SL(Z_SRED, most)
    # ЛОШАДЬ с САНЯМИ и трое людей на мосту
    edet = A.ease(A.seg(t, .3, 4.2))
    lx = 420 + 300 * edet
    kiv = 9 * A.w(t, 1.4, .1)
    s += SL(Z_SRED, f'<ellipse cx="{lx:.0f}" cy="430" rx="140" ry="74" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{lx+120:.0f},400 q{70:.0f},{-30+kiv:.0f} {96:.0f},{20+kiv:.0f}'
                    f' l{-30:.0f},{40:.0f} q{-40:.0f},{-20:.0f} {-76:.0f},{-10:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{lx+196:.0f},{378+kiv:.0f} l{14:.0f},{-44:.0f}'
                    f' l{18:.0f},{40:.0f} Z" fill="#6b5230" stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="{lx+206:.0f}" cy="{408+kiv:.0f}" r="6" fill="{K}"/>'
                    f'<path d="M{lx-140:.0f},410 q{-50:.0f},{-30:.0f} {-74:.0f},{10:.0f}"'
                    f' fill="none" stroke="#54351f" stroke-width="12"/>'
                    f'<path d="M{lx-80:.0f},496 l-10,34 M{lx-10:.0f},500 l0,30'
                    f' M{lx+70:.0f},496 l10,34 M{lx+120:.0f},490 l12,40"'
                    f' stroke="#54351f" stroke-width="13"/>')
    s += SL(Z_SRED, sani_s_rogozhey(lx - 300, 500, .82, t, .2, True))
    mx, my, mh = lx - 120, 520, 560
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f4a3a", kant="#ffd9a8",
                           shapka=True, tulup=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -8, t, "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .26, 36, t, "#3f4a3a", "#ffd9a8", .7, 5)
    s += SL(Z_SRED, r1 + r2 + f'<path d="M{e1x:.0f},{e1y:.0f} L{lx+150:.0f},{382+kiv:.0f}"'
                              f' stroke="#6b4428" stroke-width="6"/>'
                              f'<path d="M{e2x:.0f},{e2y:.0f} q{-40:.0f},{40:.0f}'
                              f' {-70:.0f},{86:.0f}" fill="none" stroke="#5e4a2a"'
                              f' stroke-width="5"/>')
    bx, by, bh = 1480, 524, 560
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.6))
    r3, (e3x, e3y), _ = _ruka(bx, by, bh, 1, bh * .24, 46, t, "#4a3a52", "#ffd9a8", .3, 4)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x-44:.0f},{e3y+4:.0f} q{44:.0f},{18:.0f} {88:.0f},0'
                         f' l{-10:.0f},{64:.0f} h{-68:.0f} Z" fill="#b08a52"'
                         f' stroke="{K}" stroke-width="4"/>')
    for k in range(4):
        s += SL(Z_SRED, f'<circle cx="{e3x-30+k*20:.0f}" cy="{e3y+14:.0f}" r="12"'
                        f' fill="#c8301f" stroke="{K}" stroke-width="2.6"/>')
    mlx, mly, mlh = 1700, 528, 400
    s += SL(Z_SRED, figura(mlx, mly, mlh, t, col="#3f5a6a", kant="#ffd9a8",
                           shapka=True, ph=.9))
    r4, (e4x, e4y), _ = _ruka(mlx, mly, mlh, -1, mlh * .30, -22, t,
                              "#3f5a6a", "#ffd9a8", .4, 5)
    s += SL(Z_SRED, r4)
    s += SL(Z_SRED, para_izo_rta(mx - 34, my - mh * .80, t, .3, .9, .45)
            + para_izo_rta(bx - 30, by - bh * .80, t, .7, .9, .45))
    # вороны на перилах, бани и лодки на берегу
    for i, (vx_, vy_) in enumerate(((760, 410), (900, 404))):
        vor = 6 * A.w(t, 2.0, i * .4)
        s += SL(Z_SRED, f'<ellipse cx="{vx_+vor:.0f}" cy="{vy_:.0f}" rx="40" ry="26"'
                        f' fill="#23242a" stroke="{K}" stroke-width="3.4"/>'
                        f'<circle cx="{vx_+26+vor:.0f}" cy="{vy_-22:.0f}" r="18"'
                        f' fill="#23242a" stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{vx_+42+vor:.0f},{vy_-24:.0f} l24,5 l-24,7 Z"'
                        f' fill="#6f6256" stroke="{K}" stroke-width="2.4"/>')
    for i, (lx_, ly_, ls_) in enumerate(((240, 1000, 1.0), (1720, 1020, .9))):
        s += SL(Z_SRED, f'<path d="M{lx_-150*ls_:.0f},{ly_:.0f} q{150*ls_:.0f},{-70*ls_:.0f}'
                        f' {300*ls_:.0f},0 Z" fill="#6b4428" stroke="{K}"'
                        f' stroke-width="{5*ls_:.1f}"/>'
                        f'<path d="M{lx_-150*ls_:.0f},{ly_:.0f} h{300*ls_:.0f}"'
                        f' stroke="url(#sneg)" stroke-width="{10*ls_:.1f}" opacity=".9"/>')
    s += SL(Z_SRED, kamysh(80, 1040, 220, t, 7, 211, True)
            + kamysh(1880, 1046, 230, t, 7, 223, True))
    s += SL(Z_SRED, inej_mel(197, 44, 900, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


# ═══ из chast2.py ═══
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


# ═══ из chast3.py ═══
def krepkiy_led_i_peshnya(t):
    """Река под толстым белым льдом в морозный день: мужик обеими руками бьёт
    пешнёй — она отскакивает, лёд не поддаётся, летит белая крошка. Он топает
    ногой и довольно кивает."""
    rnd = random.Random(3001)
    s = nebo("den", t, False, 373)
    s += oblaka(t, 150, 5, 179, .38)
    s += SL(Z_DAL, ulica_dal(60, 330, 820, t, True, 139))
    s += SL(Z_DAL, izba_snaruzhi(1500, 350, 300, t, True, True, 97)
            + dym_stolbom(1534, 200, t, 300, .5, .4, 7))
    s += SL(Z_DAL, f'<rect x="980" y="300" width="520" height="22" fill="#6b4428"'
                   f' stroke="{K}" stroke-width="4"/>')
    for i in range(4):
        s += SL(Z_DAL, f'<rect x="{1020+i*130:.0f}" y="322" width="18" height="90"'
                       f' fill="#54351f" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<rect x="0" y="420" width="{W}" height="660" fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(960, 760, 860, 220, t, .2, .0, .95))
    for i in range(9):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(60,1860):.0f}"'
                        f' cy="{rnd.uniform(560,1040):.0f}" rx="{rnd.uniform(80,220):.0f}"'
                        f' ry="{rnd.uniform(16,40):.0f}" fill="url(#sneg)"'
                        f' opacity="{rnd.uniform(.5,.9):.2f}"/>')
    # МУЖИК бьёт пешнёй
    ud = abs(A.w(t, 1.0, .0))
    mx, my, mh = 760, 900, 700
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f4a3a", kant="#cfe4f5",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -10 + 40 * ud, t,
                              "#3f4a3a", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .28, -6 + 36 * ud, t,
                              "#3f4a3a", "#cfe4f5", .5, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<g transform="rotate({-30+34*ud:.1f} {e1x:.0f} {e1y:.0f})">'
            + peshnya(e1x, e1y + 120, 1.3, 0, t, .1) + '</g>')
    # белая крошка от удара
    for i in range(9):
        d = ((t * 1.6 + i / 9.0) % 1.0)
        s += SL(Z_SRED, f'<path d="M{e1x+40+((i*37)%120)-60+120*d*math.cos(i):.0f},'
                        f'{e1y+220-180*d+120*d*d:.0f} l{10:.0f},{-8:.0f} l{4:.0f},{10:.0f} Z"'
                        f' fill="#ffffff" opacity="{(1-d)*.9:.2f}"/>')
    s += SL(Z_SRED, para_izo_rta(mx - 36, my - mh * .80, t, .3, 1.1, .55))
    s += SL(Z_SRED, ten(mx, my + 6, 140, 24, .4))
    # сани на берегу, лошадь под попоной
    s += SL(Z_SRED, sani_s_rogozhey(1480, 980, 1.0, t, .3, True))
    kiv = 8 * A.w(t, 1.8, .2)
    s += SL(Z_SRED, f'<ellipse cx="1760" cy="900" rx="150" ry="80" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1630,860 q{140:.0f},{-40:.0f} {270:.0f},{-10:.0f}'
                    f' l{-20:.0f},{90:.0f} q{-120:.0f},{20:.0f} {-240:.0f},0 Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="{1636+kiv:.0f}" cy="{830+kiv:.0f}" r="46"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{1612+kiv:.0f},{794+kiv:.0f} l{-10:.0f},{-34:.0f}'
                    f' l{26:.0f},{24:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3"/>'
                    f'<path d="M1680,980 l-10,60 M1760,984 l0,56 M1840,978 l10,62"'
                    f' stroke="#54351f" stroke-width="14"/>')
    s += SL(Z_SRED, goloe_derevo_ld(240, 1020, 520, t, 373, 7, True)
            + goloe_derevo_ld(420, 1050, 420, t, 379, 6, True))
    s += SL(Z_SRED, kamysh(80, 1000, 220, t, 7, 383, True))
    s += SL(Z_SRED, par(1760, 820, t, 4, .5, 170, .45, 1.0))
    s += SL(Z_SRED, inej_mel(373, 46, 900, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def sani_cherez_reku_i_konki(t):
    """Та же река, лёд крепкий: по льду едут сани, ближе к берегу двое детей
    на коньках, привязанных к валенкам. Листки численника перелистывают годы:
    в одном лёд белый, в других на этот день тёмная вода."""
    rnd = random.Random(3002)
    s = nebo("den", t, False, 379)
    s += oblaka(t, 140, 5, 181, .40)
    s += SL(Z_DAL, ulica_dal(1120, 320, 800, t, True, 149))
    s += SL(Z_DAL, izba_snaruzhi(300, 340, 280, t, True, True, 101)
            + dym_stolbom(330, 200, t, 280, .48, .4, 6))
    s += SL(Z_SRED, f'<rect x="0" y="420" width="{W}" height="660" fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(960, 720, 880, 200, t, .3, .0, .9))
    s += SL(Z_SRED, mostki(1480, 520, 420, t, True, 160))
    # САНИ едут по льду
    edet = A.ease(A.seg(t, .3, 3.4))
    lx = 300 + 500 * edet
    s += SL(Z_SRED, sani_s_rogozhey(lx - 260, 700, .95, t, .2, False))
    kiv = 9 * A.w(t, 1.5, .1)
    s += SL(Z_SRED, f'<ellipse cx="{lx:.0f}" cy="640" rx="130" ry="70" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="{lx+116:.0f}" cy="{594+kiv:.0f}" r="42" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{lx+138:.0f},{560+kiv:.0f} l{12:.0f},{-40:.0f}'
                    f' l{18:.0f},{36:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3.4"/>'
                    f'<path d="M{lx-70:.0f},720 l-10,56 M{lx:.0f},724 l0,52'
                    f' M{lx+70:.0f},718 l10,58" stroke="#54351f" stroke-width="13"/>')
    mx, my, mh = lx - 230, 660, 460
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f4a3a", kant="#cfe4f5",
                           tulup=True, shapka=True, boroda=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -4, t, "#3f4a3a", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .28, 0, t, "#3f4a3a", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2
            + f'<path d="M{e1x:.0f},{e1y:.0f} L{lx+90:.0f},{600+kiv:.0f}"'
              f' stroke="#6b4428" stroke-width="5"/>'
              f'<path d="M{e2x:.0f},{e2y:.0f} L{lx+80:.0f},{620+kiv:.0f}"'
              f' stroke="#6b4428" stroke-width="5"/>')
    # ДВОЕ ДЕТЕЙ на коньках
    kat = A.ease(A.seg(t, .5, 3.0))
    dx, dy, dh = 760 + 260 * kat, 1010, 440
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#3f5a6a", kant="#cfe4f5",
                           shapka=True, ph=.2, naklon=4.0))
    r3, (e3x, e3y), _ = _ruka(dx, dy, dh, 1, dh * .30, -34, t, "#3f5a6a", "#cfe4f5", .2, 7)
    r4, (e4x, e4y), _ = _ruka(dx, dy, dh, -1, dh * .30, -30, t, "#3f5a6a", "#cfe4f5", .6, 7)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, konki_snegurki(dx - 30, dy, .68, 0, True, t, .1)
            + konki_snegurki(dx + 40, dy + 4, .68, 0, True, t, .5))
    gx, gy, gh = dx - 220, 1020, 400
    s += SL(Z_SRED, figura(gx, gy, gh, t, col="#8a2f22", kant="#cfe4f5",
                           platok=True, ph=.7, naklon=4.0))
    r5, (e5x, e5y), _ = _ruka(gx, gy, gh, 1, gh * .34, -16, t, "#8a2f22", "#cfe4f5", .3, 5)
    r6, (e6x, e6y), _ = _ruka(gx, gy, gh, -1, gh * .30, -12, t, "#8a2f22", "#cfe4f5", .8, 5)
    s += SL(Z_SRED, r5 + r6)
    s += SL(Z_SRED, f'<path d="M{e5x:.0f},{e5y:.0f} q{60:.0f},{-20:.0f} {130:.0f},{-30:.0f}"'
                    f' fill="none" stroke="{TKAN}" stroke-width="16"/>')
    s += SL(Z_SRED, konki_snegurki(gx - 26, gy, .62, 0, True, t, .3)
            + konki_snegurki(gx + 36, gy + 4, .62, 0, True, t, .8))
    s += SL(Z_SRED, para_izo_rta(dx - 26, dy - dh * .80, t, .3, .9, .45)
            + para_izo_rta(gx - 24, gy - gh * .80, t, .8, .8, .45))
    # ЛИСТКИ ЧИСЛЕННИКА перелистывают годы
    s += SL(Z_SRED, f'<rect x="120" y="200" width="200" height="260" rx="10"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="120" y="200" width="200" height="50" rx="10"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="5"/>')
    god = int((t * .7) % 3)
    s += SL(Z_SRED, f'<rect x="150" y="280" width="140" height="140" rx="8"'
                    f' fill="{"#dcecf8" if god == 0 else "#2f4a52"}" stroke="{K}"'
                    f' stroke-width="4"/>')
    for i in range(3):
        d = ((t * .7 + i * .33) % 1.0)
        s += SL(Z_LETIT, f'<rect x="{140+260*d:.0f}" y="{280+300*d*d:.0f}" width="120"'
                         f' height="140" rx="6" fill="#f2ead6" opacity="{(1-d)*.85:.2f}"'
                         f' transform="rotate({d*150:.0f} {200+260*d:.0f}'
                         f' {350+300*d*d:.0f})" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, goloe_derevo_ld(1800, 1000, 460, t, 389, 7, True))
    s += SL(Z_SRED, kamysh(60, 1020, 200, t, 6, 397, True))
    # СЕРЕДИНА ЛЬДА НЕ ПУСТАЯ: вешки, наметённые гряды, прорубь, санный след
    for i, vx_ in enumerate((620, 900, 1180, 1420)):
        kch = 3.0 * A.w(t, 3.2, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {vx_:.0f} {620:.0f})">'
                        f'<rect x="{vx_:.0f}" y="430" width="12" height="190"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{vx_-20:.0f},430 q{26:.0f},{-28:.0f} {52:.0f},{-4:.0f}'
                        f' q{-24:.0f},{20:.0f} {-52:.0f},{4:.0f} Z" fill="#8a7a52"'
                        f' stroke="{K}" stroke-width="3"/></g>')
    for i in range(8):
        s += SL(Z_SRED, f'<ellipse cx="{320+i*210:.0f}" cy="{520+((i*7)%4)*40:.0f}"'
                        f' rx="{90+((i*5)%3)*40:.0f}" ry="{18+((i*3)%2)*10:.0f}"'
                        f' fill="url(#sneg)" opacity=".85"/>')
    s += SL(Z_SRED, prorub(1640, 760, 120, t, .3, True))
    s += SL(Z_SRED, sledy_valenok(1880, 900, 1200, 700, 7, 401, "#9fc4d8", 1.1))
    s += SL(Z_SRED, par(lx + 150, 580, t, 4, .5, 160, .45, 1.0))
    s += SL(Z_SRED, inej_mel(379, 44, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def konki_na_valenkah(t):
    """Валенок на пол-кадра, к нему верёвкой и палочкой-закруткой прикручен
    конёк-«снегурка». Мальчик на лавочке у катка затягивает верёвку; рядом
    самодельная клюшка из гнутой ветки и консервная крышка вместо шайбы."""
    rnd = random.Random(3003)
    s = nebo("noch", t, True, 383)
    s += SL(Z_NEBO, luna_v_gorode(300, 160, t, .7, True))
    s += SL(Z_DAL, panelka(1180, 540, 740, t, 5, True, 47))
    s += SL(Z_DAL, zabor_shtaket(-40, 420, 1100, 200, 383, 62))
    s += SL(Z_SRED, f'<rect x="0" y="620" width="{W}" height="460" fill="#dce7f2"/>')
    s += SL(Z_SRED, sneg_lezhit(640, 34, "url(#sneg)"))
    # ФОНАРЬ
    s += SL(Z_SRED, f'<rect x="1520" y="260" width="22" height="560" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(1531, 260, t, 1.4, True) + teplo(1531, 280, 320, 270, .42))
    # ЛАВОЧКА и мальчик
    s += SL(Z_SRED, f'<rect x="900" y="800" width="700" height="26" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="900" y="740" width="700" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="930" y="826" width="24" height="140" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1550" y="826" width="24" height="140" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    mx, my, mh = 1240, 800, 520
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f5a6a", kant="#cfe4f5",
                           shapka=True, tulup=True, ph=.3, naklon=3.0))
    zakr = A.ease(A.seg(t, .6, 2.0))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, -1, mh * .38, 40 + 10 * zakr, t,
                              "#3f5a6a", "#cfe4f5", .2, 6)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, 1, mh * .36, 44 + 10 * zakr, t,
                              "#3f5a6a", "#cfe4f5", .6, 6)
    s += SL(Z_SRED, r1 + varezhka(e1x - 8, e1y + 10, .9, -14, TKAN, t, .2)
            + r2 + varezhka(e2x + 8, e2y + 10, .9, 14, TKAN, t, .6))
    s += SL(Z_SRED, para_izo_rta(mx - 28, my - mh * .78, t, .4, .9, .5))
    # ВАЛЕНОК С КОНЬКОМ на пол-кадра
    vx, vy = 540, 980
    s += SL(Z_SRED, f'<g transform="rotate(-6 {vx:.0f} {vy:.0f})">'
            + _valenok(vx, vy, 3.6, 0, "#c9bfa6") + '</g>')
    s += SL(Z_SRED, teplo(vx, vy - 140, 420, 340, .30))
    s += SL(Z_SRED, konki_snegurki(vx + 10, vy + 24, 2.8, -6, False, t, .2))
    # верёвка и палочка-закрутка
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{vx-130:.0f},{vy-90-i*46:.0f} q{130:.0f},{-26:.0f}'
                        f' {270:.0f},{6:.0f}" fill="none" stroke="#b9a37a"'
                        f' stroke-width="9"/>')
    s += SL(Z_SRED, f'<g transform="rotate({zakr*220:.0f} {vx+80:.0f} {vy-136:.0f})">'
                    f'<rect x="{vx+56:.0f}" y="{vy-150:.0f}" width="48" height="24"'
                    f' rx="8" fill="#7d5636" stroke="{K}" stroke-width="4"/></g>')
    # КЛЮШКА и крышка вместо шайбы
    s += SL(Z_SRED, f'<g transform="rotate(14 1760 1000)">'
                    f'<path d="M1754,520 q{20:.0f},{240:.0f} {-10:.0f},{420:.0f}'
                    f' q{-6:.0f},{60:.0f} {70:.0f},{60:.0f}" fill="none"'
                    f' stroke="#8a6342" stroke-width="18" stroke-linecap="round"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{1744+i*3:.0f},{600+i*54:.0f} q{16:.0f},{10:.0f}'
                        f' {26:.0f},{2:.0f}" fill="none" stroke="{TKAN}"'
                        f' stroke-width="7" opacity=".9"/>')
    s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="1040" rx="46" ry="16" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="1500" cy="1034" rx="36" ry="11" fill="#8f979f"/>')
    s += SL(Z_SRED, _valenok(960, 1050, 1.5, 6))
    s += SL(Z_SRED, konki_snegurki(980, 1066, 1.1, 4, False, t, .7))
    s += SL(Z_SRED, inej_mel(389, 50, 940, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 26, 101, .5, .6))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def tochilschik_s_tochilnym_krugom(t):
    """Двор, точильный станок с ножным приводом на пол-кадра: точильщик качает
    педаль и прижимает конёк к вращающемуся кругу, трое мальчишек ждут
    очереди со своими коньками. Над двором расходятся звуковые кольца."""
    rnd = random.Random(3004)
    s = nebo("den", t, False, 397)
    s += oblaka(t, 140, 5, 191, .40)
    s += SL(Z_DAL, panelka(60, 560, 860, t, 4, True, 53))
    s += SL(Z_DAL, panelka(1240, 540, 680, t, 5, True, 59))
    s += SL(Z_SRED, f'<rect x="0" y="640" width="{W}" height="440" fill="#dce7f2"/>')
    s += SL(Z_SRED, sneg_lezhit(660, 32, "url(#sneg)"))
    # САРАЙ и поленница
    s += SL(Z_SRED, f'<rect x="1480" y="420" width="440" height="300" rx="8"'
                    f' fill="#5e4430" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1450,420 l230,-110 l250,110 Z" fill="#4a3526"'
                    f' stroke="{K}" stroke-width="5.5"/>'
                    f'<path d="M1450,420 l230,-110 l250,110" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="16" opacity=".9"/>')
    s += SL(Z_SRED, f'<rect x="80" y="520" width="280" height="190" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(15):
        s += SL(Z_SRED, f'<circle cx="{104+(i%5)*56:.0f}" cy="{550+(i//5)*58:.0f}" r="26"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    # ТОЧИЛЬНЫЙ СТАНОК на пол-кадра
    sx_, sy_ = 820, 980
    s += SL(Z_SRED, f'<rect x="{sx_-220:.0f}" y="{sy_-80:.0f}" width="440" height="40"'
                    f' rx="8" fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="{sx_-190:.0f}" y="{sy_-40:.0f}" width="40" height="80"'
                    f' fill="#54351f" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{sx_+150:.0f}" y="{sy_-40:.0f}" width="40" height="80"'
                    f' fill="#54351f" stroke="{K}" stroke-width="4"/>')
    for i in (-1, 1):
        s += SL(Z_SRED, f'<rect x="{sx_+i*150-14:.0f}" y="{sy_-440:.0f}" width="28"'
                        f' height="360" fill="#7d5636" stroke="{K}" stroke-width="4"/>')
    ug = (t * 520) % 360
    s += SL(Z_SRED, f'<g transform="rotate({ug:.0f} {sx_:.0f} {sy_-430:.0f})">'
                    f'<circle cx="{sx_:.0f}" cy="{sy_-430:.0f}" r="130" fill="#9aa3a8"'
                    f' stroke="{K}" stroke-width="6"/>')
    for i in range(6):
        a = i * 1.05
        s += SL(Z_SRED, f'<line x1="{sx_:.0f}" y1="{sy_-430:.0f}"'
                        f' x2="{sx_+120*math.cos(a):.0f}" y2="{sy_-430+120*math.sin(a):.0f}"'
                        f' stroke="#8a8078" stroke-width="5" opacity=".8"/>')
    s += SL(Z_SRED, f'<circle cx="{sx_:.0f}" cy="{sy_-430:.0f}" r="30" fill="#6f7a84"'
                    f' stroke="{K}" stroke-width="4"/></g>')
    ped = 16 * A.w(t, .9, .0)
    s += SL(Z_SRED, f'<path d="M{sx_-170:.0f},{sy_+30+ped:.0f} h200 l0,20 h-200 Z"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{sx_-70:.0f},{sy_+30+ped:.0f} L{sx_-30:.0f},{sy_-380:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="7"/>')
    # искры от круга
    for i in range(8):
        d = ((t * 1.8 + i / 8.0) % 1.0)
        s += SL(Z_SRED, f'<path d="M{sx_+120+200*d:.0f},{sy_-440+120*d*d:.0f}'
                        f' l{12:.0f},{4:.0f}" stroke="#ffd98a" stroke-width="4"'
                        f' opacity="{(1-d)*.9:.2f}"/>')
    # ТОЧИЛЬЩИК
    tx, ty, th = 620, 1046, 700
    s += SL(Z_SRED, figura(tx, ty, th, t, col="#3f4a3a", kant="#ffd9a8",
                           shapka=True, ph=.2, naklon=2.0))
    s += SL(Z_SRED, f'<path d="M{tx-90:.0f},{ty-th*.52:.0f} q{90:.0f},{-20:.0f}'
                    f' {180:.0f},0 l{10:.0f},{th*.34:.0f} q{-100:.0f},{24:.0f}'
                    f' {-200:.0f},0 Z" fill="#8a7a62" stroke="{K}" stroke-width="4.5"/>')
    r1, (e1x, e1y), _ = _ruka(tx, ty, th, 1, th * .32, -16, t, "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(tx, ty, th, -1, th * .30, -12, t, "#3f4a3a", "#ffd9a8", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, konki_snegurki((e1x + e2x) * .5 + 40, e1y + 10, .9, -24, False, t, .2))
    s += SL(Z_SRED, para_izo_rta(tx - 34, ty - th * .80, t, .3, 1.0, .5))
    # ЗВУКОВЫЕ КОЛЬЦА над двором
    for i in range(4):
        d = ((t * .7 + i * .25) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="{sy_-430:.0f}"'
                        f' rx="{180+620*d:.0f}" ry="{70+240*d:.0f}" fill="none"'
                        f' stroke="#cfe4f5" stroke-width="{6-3*d:.1f}"'
                        f' opacity="{(1-d)*.5:.2f}"/>')
    # ТРОЕ МАЛЬЧИШЕК в очереди
    for i, (bx_, by_, bh_, col) in enumerate(((1200, 1050, 470, "#3f5a6a"),
                                              (1390, 1060, 440, "#8a2f22"),
                                              (1570, 1046, 490, "#4a6a3a"))):
        s += SL(Z_SRED, figura(bx_, by_, bh_, t, col=col, kant="#ffd9a8",
                               shapka=True, ph=i * .35))
        rk, (ex, ey), _ = _ruka(bx_, by_, bh_, 1, bh_ * .26, 40, t, col, "#ffd9a8", i * .3, 4)
        rk2, (e2x_, e2y_), _ = _ruka(bx_, by_, bh_, -1, bh_ * .26, 44, t, col,
                                     "#ffd9a8", i * .3 + .4, 4)
        s += SL(Z_SRED, rk + rk2
                + konki_snegurki((ex + e2x_) * .5, ey + 70, .6, 10, False, t, i * .3))
        s += SL(Z_SRED, para_izo_rta(bx_ - 24, by_ - bh_ * .80, t, i * .3, .8, .45))
    s += SL(Z_SRED, kot(1700, 400, t, 1.4, "#4a423a", False))
    s += SL(Z_SRED, dym_stolbom(1680, 300, t, 260, .45, .4, 6))
    s += SL(Z_SRED, inej_mel(397, 46, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def katok_vo_dvore(t):
    """Двор между домами: вечером отец широким взмахом выплёскивает ведро на
    тёмную площадку, утром она становится блестящим катком, и со всех
    подъездов сбегаются дети. В окне над катком — настоящие коньки на льду."""
    rnd = random.Random(3005)
    utro = A.ease(A.seg(t, 1.6, 1.8))
    s = nebo("noch" if utro < .5 else "rassv", t, utro < .5, 401)
    s += SL(Z_DAL, panelka(40, 620, 860, t, 5, True, 61))
    s += SL(Z_DAL, panelka(1180, 600, 740, t, 5, True, 67))
    # ОКНО-ПРОЁМ над катком (сверху справа)
    px, py, pw, ph_ = 1120, 180, 780, 320
    okno = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
            f' fill="#9fc4d8"/>')
    okno += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.4:.0f}"'
             f' fill="#c4d8e8"/>')
    okno += mesto_stoka(px, py, pw, ph_, "pryam")
    okno += (f'<rect x="{px-18:.0f}" y="{py-18:.0f}" width="{pw+36:.0f}"'
             f' height="{ph_+36:.0f}" rx="6" fill="none" stroke="#d8cbb0"'
             f' stroke-width="26"/>')
    okno += (f'<path d="M{px+pw*.5:.0f},{py:.0f} v{ph_:.0f} M{px:.0f},{py+ph_*.5:.0f}'
             f' h{pw:.0f}" stroke="#e4d8bd" stroke-width="16"/>')
    s += SL(Z_DAL, okno)
    s += SL(Z_SRED, _merzlaya_zemlya(700, 401, False))
    s += SL(Z_SRED, sneg_lezhit(720, 30, "url(#sneg)"))
    # ПЛОЩАДКА: тёмная вечером, каток утром
    s += SL(Z_SRED, f'<ellipse cx="900" cy="880" rx="620" ry="180" fill="#3f4a56"/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="880" rx="620" ry="180" fill="url(#led)"'
                    f' opacity="{utro:.2f}"/>')
    if utro > .3:
        s += SL(Z_SRED, korka_lda(900, 876, 580, 160, t, .2, .0, utro * .85))
    # бортики из снега
    for i in range(14):
        a = 3.14 + i * .25
        s += SL(Z_SRED, f'<ellipse cx="{900+640*math.cos(a):.0f}"'
                        f' cy="{880+190*math.sin(a):.0f}" rx="70" ry="26"'
                        f' fill="url(#sneg)" opacity=".92"/>')
    # ВЕЧЕР: отец выплёскивает ведро
    if utro < .75:
        ox, oy, oh = 420, 1040, 700
        vzmah = A.ease(A.seg(t, .4, .8))
        s += SL(Z_SRED, f'<g opacity="{1-utro:.2f}">'
                + figura(ox, oy, oh, t, col="#3f4a3a", kant="#ffd9a8",
                         tulup=True, shapka=True, ph=.2) + '</g>')
        r1, (e1x, e1y), _ = _ruka(ox, oy, oh, 1, oh * .32, -40 + 50 * vzmah, t,
                                  "#3f4a3a", "#ffd9a8", .2, 6)
        r2, (e2x, e2y), _ = _ruka(ox, oy, oh, -1, oh * .28, -36 + 46 * vzmah, t,
                                  "#3f4a3a", "#ffd9a8", .6, 6)
        s += SL(Z_SRED, f'<g opacity="{1-utro:.2f}">' + r1 + r2
                + f'<g transform="rotate({-40+90*vzmah:.0f} {e1x:.0f} {e1y:.0f})">'
                  f'<path d="M{e1x-44:.0f},{e1y:.0f} h88 l-10,92 h-68 Z"'
                  f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4.5"/>'
                  f'<ellipse cx="{e1x:.0f}" cy="{e1y:.0f}" rx="44" ry="13"'
                  f' fill="#8f979f" stroke="{K}" stroke-width="3.6"/></g></g>')
        for i in range(12):
            d = ((t * 1.2 + i / 12.0) % 1.0)
            s += SL(Z_SRED, f'<ellipse cx="{e1x+80+500*d:.0f}"'
                            f' cy="{e1y+40+260*d*d-120*d:.0f}" rx="{20+26*d:.0f}"'
                            f' ry="{10+14*d:.0f}" fill="#9fd0e4"'
                            f' opacity="{(1-d)*.6*(1-utro):.2f}"/>')
        for i in range(6):
            s += SL(Z_SRED, par(700 + i * 140, 900, t, 3, .4 * (1 - utro), 150, .4, 1.0))
    # УТРО: дети сбегаются на каток
    if utro > .25:
        for i, (dx_, dy_, dh_, col) in enumerate(((700, 1000, 420, "#8a2f22"),
                                                  (1020, 1020, 440, "#3f5a6a"),
                                                  (1300, 990, 400, "#4a6a3a"),
                                                  (480, 1030, 380, "#6b3a6a"))):
            beg = A.ease(A.seg(t, 1.8 + i * .2, 1.4))
            px_ = dx_ + (900 - dx_) * .4 * beg
            s += SL(Z_SRED, f'<g opacity="{min(1.0, (utro-.25)*3):.2f}">'
                    + figura(px_, dy_, dh_, t, col=col, kant="#ffd9a8",
                             shapka=True, ph=i * .3, naklon=4.0) + '</g>')
            rk, (ex, ey), _ = _ruka(px_, dy_, dh_, 1 if i % 2 else -1, dh_ * .28,
                                    -30, t, col, "#ffd9a8", i * .25, 7)
            s += SL(Z_SRED, f'<g opacity="{min(1.0, (utro-.25)*3):.2f}">' + rk + '</g>')
            s += SL(Z_SRED, konki_snegurki(px_, dy_, .6, 0, True, t, i * .3))
    # фонарь, скамейка, санки, собака
    s += SL(Z_SRED, f'<rect x="300" y="420" width="22" height="420" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(311, 420, t, 1.3, True) + teplo(311, 440, 300, 250, .40))
    s += SL(Z_SRED, f'<rect x="1560" y="880" width="300" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1580" y="902" width="22" height="110" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="1810" y="902" width="22" height="110" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, sanki_derev(180, 1040, .9, t, .5, True))
    s += SL(Z_SRED, f'<ellipse cx="1700" cy="1020" rx="74" ry="36" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="1766" cy="986" r="30" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3.6"/>'
                    f'<path d="M1784,962 l{12:.0f},{-30:.0f} l{14:.0f},{28:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="3"/>'
                    f'<path d="M1636,1010 q{-38:.0f},{-28:.0f} {-54:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#6b5230" stroke-width="9"/>')
    s += SL(Z_SRED, inej_mel(401, 44, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def primerka_konkov_v_prihozhey(t):
    """Прихожая, коробка с коньками: внучка на пуфе вставляет ногу в белый
    ботинок и тянет шнурки, дед на корточках придерживает ботинок и
    проверяет рукавицей лезвие. На стене карта: пруд перечёркнут, каток обведён."""
    rnd = random.Random(3006)
    s = (f'<rect width="{W}" height="{H}" fill="#c3ab8a"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="760" fill="#cbb492"/>')
    for i in range(14):
        s += SL(Z_DAL, f'<path d="M{70+i*140:.0f},0 v760" stroke="#b9a082"'
                       f' stroke-width="4" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(760, "#8a6342"))
    # ВЕШАЛКА с шапками
    s += SL(Z_SRED, f'<rect x="120" y="180" width="440" height="20" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{170+i*110:.0f},200 l0,30" stroke="{ZHELEZ}"'
                        f' stroke-width="7"/>')
    for i, (hx_, col) in enumerate(((180, "#3f4a7a"), (290, "#6b3a2a"), (400, "#4a6a3a"))):
        s += SL(Z_SRED, f'<path d="M{hx_:.0f},240 q{44:.0f},{-24:.0f} {88:.0f},0'
                        f' l{8:.0f},{150:.0f} q{-50:.0f},{20:.0f} {-104:.0f},0 Z"'
                        f' fill="{col}" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<ellipse cx="520" cy="250" rx="54" ry="30" fill="#4a3a2c"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="520" cy="236" rx="54" ry="20" fill="#8a6a4a"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    # КАРТА на стене: пруд перечёркнут, каток обведён
    s += SL(Z_SRED, f'<rect x="1180" y="160" width="620" height="420" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, f'<ellipse cx="1380" cy="330" rx="130" ry="80" fill="#9fc4d8"'
                    f' stroke="#6f7a84" stroke-width="5"/>')
    s += SL(Z_SRED, _cherta_zapreta(1380, 330, 130, t, .0, 14))
    obv = A.out(A.seg(t, 1.0, .8))
    s += SL(Z_SRED, f'<rect x="1560" y="380" width="200" height="130" rx="10"'
                    f' fill="#dce7f2" stroke="#6f7a84" stroke-width="5"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1590+i*60:.0f}" y="350" width="10" height="36"'
                        f' fill="{BETON2}"/>'
                        f'<circle cx="{1595+i*60:.0f}" cy="346" r="11" fill="#ffd98a"'
                        f' opacity=".9"/>')
    if obv > .02:
        s += SL(Z_SRED, f'<ellipse cx="1660" cy="444" rx="{170*obv:.0f}"'
                        f' ry="{110*obv:.0f}" fill="none" stroke="#3f8a4a"'
                        f' stroke-width="12" opacity="{obv:.2f}"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{1220+i*80:.0f},520 q{30:.0f},{-14:.0f} {60:.0f},0"'
                        f' fill="none" stroke="#b9a082" stroke-width="4"/>')
    # КОРОБКА с коньками
    s += SL(Z_SRED, f'<rect x="760" y="880" width="320" height="180" rx="10"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5.5"/>'
                    f'<path d="M760,930 h320" stroke="#6b4428" stroke-width="7"/>')
    s += SL(Z_SRED, konki_snegurki(900, 880, 1.0, -12, False, t, .2))
    # ВНУЧКА на пуфе
    vx, vy, vh = 420, 900, 520
    s += SL(Z_SRED, f'<ellipse cx="{vx:.0f}" cy="{vy:.0f}" rx="130" ry="56"'
                    f' fill="#8a2f8a" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="{vx:.0f}" cy="{vy-20:.0f}" rx="130" ry="50"'
                    f' fill="#a03aa0" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(vx, vy - 20, vh, t, col="#c8301f", kant="#ffd98a",
                           ph=.3, naklon=3.0))
    tyan = A.ease(A.seg(t, .6, 1.6))
    r1, (e1x, e1y), _ = _ruka(vx, vy - 20, vh, 1, vh * .38, 40 - 14 * tyan, t,
                              "#c8301f", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(vx, vy - 20, vh, -1, vh * .38, 44 - 12 * tyan, t,
                              "#c8301f", "#ffd98a", .6, 5)
    s += SL(Z_SRED, r1 + r2)
    # БЕЛЫЙ БОТИНОК конька на ноге
    bx_, by_ = vx + 150, vy + 60
    s += SL(Z_SRED, f'<path d="M{vx+40:.0f},{vy-40:.0f} q{60:.0f},{40:.0f}'
                    f' {110:.0f},{70:.0f}" fill="none" stroke="#c8301f"'
                    f' stroke-width="30" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M{bx_-50:.0f},{by_-110:.0f} h{90:.0f} q{20:.0f},{60:.0f}'
                    f' {10:.0f},{110:.0f} l{-100:.0f},0 q{-16:.0f},{-56:.0f}'
                    f' {0:.0f},{-110:.0f} Z" fill="#f4f1e8" stroke="{K}"'
                    f' stroke-width="5"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{bx_-44+i*4:.0f},{by_-96+i*20:.0f}'
                        f' l{76-i*8:.0f},{6:.0f}" stroke="#c9bfa6"'
                        f' stroke-width="{4-tyan:.1f}"/>')
    s += SL(Z_SRED, konki_snegurki(bx_ - 4, by_ + 10, 1.0, 0, False, t, .4))
    # ДЕД на корточках
    dx, dy, dh = 760, 1056, 470
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, ph=.6, naklon=2.0))
    kch = 3.0 * A.w(t, 1.8, .2)
    r3, (e3x, e3y), _ = _ruka(dx, dy, dh, -1, dh * .40, 6, t, "#4a4038", "#ffd98a", .3, 4)
    r4, (e4x, e4y), _ = _ruka(dx, dy, dh, 1, dh * .34, 20, t, "#4a4038", "#ffd98a", .8, 4)
    s += SL(Z_SRED, r3 + r4 + varezhka(e4x + 8, e4y + 8, 1.0, 16 + kch, "#6b4428", t, .3))
    s += SL(Z_SRED, f'<rect x="1020" y="1020" width="130" height="44" rx="8"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, sanki_derev(1500, 1050, .8, t, .4, True))
    s += SL(Z_SRED, f'<rect x="1660" y="900" width="220" height="160" rx="10"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, kot(1770, 900, t, 1.4, "#3b3430", True))
    s += SL(Z_SRED, lampa(960, 100, t, 1.3, True) + teplo(960, 120, 320, 260, .42))
    s += SL(Z_SRED, ten(dx, dy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def chaynik_i_travy_pod_potolkom(t):
    """Деревенская кухня: под потолком на жерди сушатся пучки трав, на столе
    пузатый фарфоровый чайник на пол-кадра. Стеклянная дверца буфета — проём
    с настоящим травяным чаем. Хозяйка кладёт в чайник щепоть травы."""
    rnd = random.Random(3007)
    s = stena_gornicy_19(t, 37, 840, True, True)
    s += SL(Z_SRED, pech(60, 260, 460, 580, t, True, True, False))
    s += SL(Z_SRED, ogon(200, 700, t, 1.3, .1, 6) + teplo(200, 680, 360, 300, .5))
    # ЖЕРДЬ с пучками трав
    s += SL(Z_SRED, f'<path d="M520,220 h1100" stroke="#8a6342" stroke-width="13"/>')
    for i, (px_, ph2, sc) in enumerate(((620, .1, 1.0), (780, .4, .9), (940, .7, 1.1),
                                        (1100, .2, .85), (1260, .6, 1.0),
                                        (1420, .9, .9))):
        s += SL(Z_SRED, puchok_trav(px_, 230, sc, t, ph2, 67 + i, "#8a7a4a"))
    # БУФЕТ со стеклянной дверцей — проём
    bx, by, bw, bh = 1180, 420, 760, 440
    s += SL(Z_SRED, f'<rect x="{bx-40:.0f}" y="{by-40:.0f}" width="{bw+80:.0f}"'
                    f' height="{bh+120:.0f}" rx="10" fill="url(#derev)" stroke="{K}"'
                    f' stroke-width="7"/>')
    put = kontur_proema(bx, by, bw, 320, "pryam")
    buf = (f'<path d="{put}" fill="#b9a082"/>')
    buf += (f'<path d="{put}" fill="#dce7f2" opacity=".35"/>')
    buf += mesto_stoka(bx, by, bw, 320, "pryam")
    buf += (f'<path d="{put}" fill="none" stroke="#6b4428" stroke-width="22"/>')
    buf += (f'<path d="M{bx+bw*.5:.0f},{by:.0f} v320" stroke="#6b4428"'
            f' stroke-width="14"/>')
    buf += (f'<path d="M{bx+30:.0f},{by+290:.0f} q{bw*.2:.0f},{-40:.0f}'
            f' {bw*.42:.0f},{-16:.0f}" fill="none" stroke="#ffffff" stroke-width="9"'
            f' opacity=".28"/>')
    s += SL(Z_SRED, buf)
    s += SL(Z_SRED, f'<rect x="{bx-20:.0f}" y="{by+340:.0f}" width="{bw+40:.0f}"'
                    f' height="26" rx="6" fill="{DOSKA}" stroke="{K}" stroke-width="5"/>')
    for i in range(4):
        s += SL(Z_SRED, banka_moloka(bx + 110 + i * 180, by + 340, .58, t, True, .78,
                                     ["#8a2f22", "#d6a63f", "#6b3a6a", "#b5803a"][i]))
    # СТОЛ и ЧАЙНИК на пол-кадра
    s += SL(Z_SRED, stol(120, 800, 900, 44, True))
    s += SL(Z_SRED, chaynik_s_parom(520, 800, 2.3, t, .1, True))
    # розетки мёда и варенья, ложка, полотенце
    s += SL(Z_SRED, f'<ellipse cx="880" cy="796" rx="76" ry="24" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="880" cy="788" rx="58" ry="17" fill="#d6a63f"'
                    f' stroke="#b5803a" stroke-width="3"/>')
    s += SL(Z_SRED, f'<ellipse cx="1030" cy="800" rx="70" ry="22" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="1030" cy="792" rx="54" ry="15" fill="#8a2f22"'
                    f' stroke="#6b2419" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M960,790 l{70:.0f},{-36:.0f}" stroke="#c9ccd1"'
                    f' stroke-width="7"/>'
                    f'<ellipse cx="1040" cy="748" rx="24" ry="14" fill="#dde3e8"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="140" y="860" width="90" height="170" rx="6"'
                    f' fill="{RUSH}" stroke="{K}" stroke-width="4"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M150,{900+i*44:.0f} h70" stroke="{TKAN}"'
                        f' stroke-width="7" opacity=".9"/>')
    # ХОЗЯЙКА кладёт щепоть травы
    hx, hy, hh = 860, 1050, 680
    syp = ((t * 1.1) % 1.0)
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.3))
    s += SL(Z_SRED, f'<path d="M{hx-110:.0f},{hy-hh*.46:.0f} q{110:.0f},{-24:.0f}'
                    f' {220:.0f},0 l0,{hh*.32:.0f} q{-110:.0f},{24:.0f} {-220:.0f},0 Z"'
                    f' fill="{RUSH}" opacity=".9" stroke="{K}" stroke-width="4"/>')
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .34, -24, t, "#8a2f22", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .24, 20, t, "#8a2f22", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    for i in range(6):
        d = ((syp + i / 6.0) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{e1x-40+i*7:.0f}" cy="{e1y+30+150*d:.0f}"'
                        f' rx="5" ry="8" fill="#7d7040" opacity="{1-d:.2f}"'
                        f' transform="rotate({d*120:.0f} {e1x-40+i*7:.0f}'
                        f' {e1y+30+150*d:.0f})"/>')
    s += SL(Z_SRED, kot(1280, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, polka_s_bankami(560, 380, 520, t, 71, 4, False))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def puchok_s_cherdaka_korobka_i_meshoc(t):
    """Развилка из трёх частей: слева чердак — хозяин на стремянке снимает с
    жерди пучок мяты; в середине городская кухня — рукав достаёт с полки
    коробку с нарисованной ромашкой; справа посылка с полотняным мешочком."""
    rnd = random.Random(3008)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    # ЛЕВАЯ ЧАСТЬ: чердак
    s += SL(Z_DAL, f'<rect x="0" y="0" width="640" height="{H}" fill="#3f3122"/>')
    s += SL(Z_DAL, doski(0, 0, 640, H, 66, True, "dosk"))
    s += SL(Z_SRED, f'<path d="M0,180 L320,20 L640,180" fill="none" stroke="#5e4430"'
                    f' stroke-width="22"/>'
                    f'<path d="M100,240 h440" stroke="#8a6342" stroke-width="12"/>')
    for i, (px_, ph2) in enumerate(((180, .2), (300, .5), (420, .8))):
        s += SL(Z_SRED, puchok_trav(px_, 250, .9, t, ph2, 73 + i, "#6f8c4a"))
    s += SL(Z_SRED, f'<path d="M140,1070 l60,-520 M300,1070 l-20,-520" stroke="#7d5636"'
                    f' stroke-width="14"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{150+i*6:.0f},{620+i*100:.0f} h{130-i*8:.0f}"'
                        f' stroke="#8a6342" stroke-width="13"/>')
    hx, hy, hh = 300, 760, 560
    snyat = A.ease(A.seg(t, .5, 1.4))
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a3a", kant="#ffd98a",
                           boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .36, -40 - 14 * snyat, t,
                              "#3f4a3a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .28, -34, t, "#3f4a3a", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, puchok_trav(e1x, e1y + 10, .8, t, .3, 79, "#6f8c4a"))
    s += SL(Z_SRED, lampa(540, 200, t, 1.1, False) + teplo(540, 210, 240, 200, .40))
    # СРЕДНЯЯ ЧАСТЬ: городская кухня, рукав достаёт коробку
    s += SL(Z_DAL, f'<rect x="640" y="0" width="640" height="{H}" fill="#cbb492"/>')
    for i in range(6):
        s += SL(Z_DAL, f'<path d="M{660+i*110:.0f},0 v{H}" stroke="#b9a082"'
                       f' stroke-width="4" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="680" y="420" width="560" height="22" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="680" y="640" width="560" height="22" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4.5"/>')
    for i in range(4):
        s += SL(Z_SRED, banka_moloka(740 + i * 130, 640, .56, t, True, .75,
                                     ["#8a2f22", "#d6a63f", "#6b3a6a", "#b5803a"][i]))
    dost = A.ease(A.seg(t, 1.0, 1.4))
    s += SL(Z_SRED, f'<rect x="{900+60*dost:.0f}" y="{300+40*dost:.0f}" width="170"'
                    f' height="120" rx="8" fill="#f2ead6" stroke="{K}"'
                    f' stroke-width="5"/>')
    s += SL(Z_SRED, f'<circle cx="{985+60*dost:.0f}" cy="{356+40*dost:.0f}" r="32"'
                    f' fill="#f8f4e8" stroke="#c9bfa6" stroke-width="3"/>')
    for i in range(8):
        a = i * .785
        s += SL(Z_SRED, f'<ellipse cx="{985+60*dost+26*math.cos(a):.0f}"'
                        f' cy="{356+40*dost+26*math.sin(a):.0f}" rx="12" ry="7"'
                        f' fill="#ffffff" stroke="#d8cbb0" stroke-width="2.4"'
                        f' transform="rotate({math.degrees(a):.0f}'
                        f' {985+60*dost+26*math.cos(a):.0f}'
                        f' {356+40*dost+26*math.sin(a):.0f})"/>')
    s += SL(Z_SRED, f'<circle cx="{985+60*dost:.0f}" cy="{356+40*dost:.0f}" r="12"'
                    f' fill="#d6a63f"/>')
    ruk, (kx_, ky_) = rukav(1270, 240, 300, 150, t, "#6b3a6a", "#ffd98a", .3, 4, True)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, chaynik_s_parom(760, 900, .9, t, .4, True))
    s += SL(Z_SRED, f'<rect x="640" y="900" width="640" height="24" fill="#8a7a62"'
                    f' stroke="{K}" stroke-width="4"/>')
    # ПРАВАЯ ЧАСТЬ: посылка с мешочком
    s += SL(Z_DAL, f'<rect x="1280" y="0" width="640" height="{H}" fill="#b9a082"/>')
    s += SL(Z_SRED, stol(1300, 760, 600, 40, True))
    s += SL(Z_SRED, f'<rect x="1400" y="520" width="420" height="240" rx="8"'
                    f' fill="#c9a05a" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1400,600 h420 M1610,520 v240" stroke="#a8824a"'
                    f' stroke-width="9"/>'
                    f'<path d="M1400,520 q{210:.0f},{-60:.0f} {420:.0f},0 l0,{40:.0f}'
                    f' q{-210:.0f},{-54:.0f} {-420:.0f},0 Z" fill="#b08a52"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    vyn = A.ease(A.seg(t, 1.6, 1.4))
    mx_, my_ = 1620, 520 - 120 * vyn
    s += SL(Z_SRED, f'<path d="M{mx_-60:.0f},{my_:.0f} q{60:.0f},{-30:.0f} {120:.0f},0'
                    f' q{14:.0f},{90:.0f} {-10:.0f},{150:.0f} q{-50:.0f},{20:.0f}'
                    f' {-100:.0f},0 q{-24:.0f},{-60:.0f} {-10:.0f},{-150:.0f} Z"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{mx_-50:.0f},{my_+10:.0f} q{50:.0f},{20:.0f} {100:.0f},0"'
                    f' fill="none" stroke="#b9a37a" stroke-width="7"/>')
    s += SL(Z_SRED, f'<rect x="{mx_+40:.0f}" y="{my_+40:.0f}" width="80" height="54"'
                    f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="3.6"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{mx_+50:.0f},{my_+58+i*14:.0f} q{24:.0f},{-6:.0f}'
                        f' {52:.0f},0" fill="none" stroke="#8a7a62" stroke-width="3"/>')
    ruk2, (k2x, k2y) = rukav(1900, 420, 280, 160, t, "#4a4450", "#ffd98a", .6, 4, True)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, lampa(1600, 180, t, 1.2, True) + teplo(1600, 200, 280, 230, .40))
    # ВСЕ ТРИ ЧАСТИ ОБЖИТЫ: на чердаке короба и связки, на кухне полка с посудой,
    # на почтовом столе бумаги, бечёвка и вторая посылка
    for i, (kx2, ky2, ks2) in enumerate(((120, 980, 1.0), (430, 1000, .85),
                                         (520, 880, .7))):
        s += SL(Z_SRED, f'<rect x="{kx2-70*ks2:.0f}" y="{ky2-90*ks2:.0f}"'
                        f' width="{140*ks2:.0f}" height="{90*ks2:.0f}" rx="8"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="{4*ks2:.1f}"/>'
                        f'<path d="M{kx2-70*ks2:.0f},{ky2-60*ks2:.0f} h{140*ks2:.0f}"'
                        f' stroke="#6b4428" stroke-width="{5*ks2:.1f}"/>')
    for i, (lx2, ly2) in enumerate(((180, 520), (380, 560))):
        for k in range(4):
            s += SL(Z_SRED, f'<ellipse cx="{lx2+((k*7)%3-1)*24:.0f}"'
                            f' cy="{ly2+k*48:.0f}" rx="24" ry="30" fill="#c9a05a"'
                            f' stroke="{K}" stroke-width="3.2"/>')
    s += SL(Z_SRED, polka_s_bankami(700, 500, 520, t, 83, 4, False))
    s += SL(Z_SRED, hodiki(1180, 520, t, 1.1))
    s += SL(Z_SRED, f'<rect x="660" y="300" width="240" height="170" rx="10"'
                    f' fill="#b9c2c8" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M660,380 h240" stroke="#8a98a8" stroke-width="7"/>'
                    f'<circle cx="876" cy="340" r="10" fill="{MED}"/>')
    for i, (bx2, by2) in enumerate(((960, 760), (1120, 770), (820, 764))):
        s += SL(Z_SRED, kruzhka_moloka(bx2, by2, .8, t, False, i * .3, "#e8e2d6"))
    s += SL(Z_SRED, f'<rect x="1140" y="700" width="120" height="200" rx="10"'
                    f' fill="#dde3e8" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1140,790 h120" stroke="#b9c2c8" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="420" y="420" width="160" height="240" rx="8"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M420,540 h160" stroke="#54351f" stroke-width="6"/>')
    s += SL(Z_SRED, puchok_trav(560, 250, .8, t, .9, 89, "#6f8c4a"))
    s += SL(Z_SRED, f'<rect x="1300" y="300" width="200" height="150" rx="8"'
                    f' fill="#8a7a62" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1300,370 h200" stroke="#6f6256" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="700" y="1000" width="180" height="70" rx="8"'
                    f' fill="#b9a082" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="920" y="1010" width="150" height="60" rx="8"'
                    f' fill="#8a7a62" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="1320" y="620" width="180" height="120" rx="8"'
                    f' fill="#c9a05a" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1320,680 h180 M1410,620 v120" stroke="#a8824a"'
                    f' stroke-width="7"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="{1340+i*90:.0f}" y="{780+((i*5)%3)*16:.0f}"'
                        f' width="76" height="54" rx="5" fill="#f2ead6" stroke="{K}"'
                        f' stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<circle cx="1860" cy="760" r="46" fill="#b9a37a" stroke="{K}"'
                    f' stroke-width="4.5"/>'
                    f'<circle cx="1860" cy="760" r="18" fill="#8a7a52"/>')
    s += SL(Z_PERED, f'<rect x="634" y="0" width="12" height="{H}" fill="#1d1611"'
                     f' opacity=".9"/>'
                     f'<rect x="1274" y="0" width="12" height="{H}" fill="#1d1611"'
                     f' opacity=".9"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def paketik_otdyhaet_chaynik_rabotaet(t):
    """Современная кухня: рукав опускает чайный пакетик обратно в коробку, а
    на стол ставят заварочный чайник — в него по словам ложатся липовый цвет,
    мята и зверобой. Женщина сыплет травы из трёх баночек."""
    rnd = random.Random(3009)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="660" fill="#d8cbb0"/>')
    for i in range(16):
        s += SL(Z_DAL, f'<rect x="{-10+i*124:.0f}" y="0" width="112" height="660"'
                       f' fill="#cfc2a8" opacity=".45"/>')
    s += SL(Z_DAL, okno_izby(1500, 130, 380, 380, t, None, .2, False, True))
    s += SL(Z_SRED, f'<rect x="0" y="660" width="{W}" height="40" fill="#8a7a62"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<rect x="0" y="700" width="{W}" height="380" fill="#b9a082"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{30+i*270:.0f}" y="720" width="230" height="340"'
                        f' rx="8" fill="#a8956f" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{145+i*270:.0f}" cy="760" r="12" fill="{MED}"/>')
    # ЗАВАРОЧНЫЙ ЧАЙНИК на столе
    s += SL(Z_SRED, chaynik_s_parom(820, 660, 1.9, t, .1, True))
    # ТРИ БАНОЧКИ с травами, травы ложатся по словам
    for i, (bx_, col, nm) in enumerate(((1180, "#d6a63f", "липа"),
                                        (1320, "#56763f", "мята"),
                                        (1460, "#e4c46a", "зверобой"))):
        s += SL(Z_SRED, banka_moloka(bx_, 660, .62, t, True, .68, col))
        syp = A.ease(A.seg(t, .7 + i * .6, .6))
        if syp > .02:
            for k in range(5):
                d = ((t * 1.3 + k / 5.0) % 1.0)
                s += SL(Z_SRED, f'<ellipse cx="{bx_-(bx_-860)*d:.0f}"'
                                f' cy="{560+120*d*d:.0f}" rx="6" ry="9" fill="{col}"'
                                f' opacity="{syp*(1-d)*.95:.2f}"'
                                f' transform="rotate({d*160:.0f} {bx_-(bx_-860)*d:.0f}'
                                f' {560+120*d*d:.0f})"/>')
    # ПАКЕТИК возвращается в коробку
    vern = A.ease(A.seg(t, .3, 1.0))
    px_, py_ = 420 + 120 * vern, 520 + 80 * vern
    s += SL(Z_SRED, f'<rect x="500" y="600" width="150" height="100" rx="6"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M500,640 h150" stroke="#c9bfa6" stroke-width="5"/>')
    s += SL(Z_SRED, f'<path d="M{px_:.0f},{py_-120:.0f} l{4:.0f},{90:.0f}"'
                    f' stroke="#c9bfa6" stroke-width="3"/>'
                    f'<path d="M{px_-24:.0f},{py_-30:.0f} h48 l-6,56 h-36 Z"'
                    f' fill="#c9a05a" stroke="{K}" stroke-width="3.6"/>'
                    f'<rect x="{px_-14:.0f}" y="{py_-136:.0f}" width="28" height="20"'
                    f' rx="4" fill="#e8e2d6" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<path d="M300,660 h120 l-10,-96 h-100 Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="360" cy="564" rx="50" ry="14" fill="#f2ead6"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    # ЖЕНЩИНА у стола
    zx, zy, zh = 1020, 1050, 700
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#6b3a6a", kant="#ffd98a", ph=.3))
    s += SL(Z_SRED, f'<path d="M{zx-120:.0f},{zy-zh*.60:.0f} q{120:.0f},{-24:.0f}'
                    f' {240:.0f},0 l{14:.0f},{zh*.34:.0f} q{-134:.0f},{26:.0f}'
                    f' {-268:.0f},0 Z" fill="#8a5a8a" opacity=".9" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    r1, (e1x, e1y), _ = _ruka(zx, zy, zh, -1, zh * .30, -26, t, "#6b3a6a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(zx, zy, zh, 1, zh * .26, -18, t, "#6b3a6a", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    # электрочайник без названия, мёд, ложка, полотенце
    s += SL(Z_SRED, f'<path d="M1660,660 q{-10:.0f},{-120:.0f} {70:.0f},{-130:.0f}'
                    f' q{80:.0f},{10:.0f} {70:.0f},{130:.0f} Z" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1690" y="518" width="80" height="18" rx="5"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1800,580 q{40:.0f},{30:.0f} {0:.0f},{60:.0f}"'
                    f' fill="none" stroke="#8a98a8" stroke-width="11"/>')
    s += SL(Z_SRED, banka_moloka(220, 660, .78, t, True, .8, "#d6a63f"))
    s += SL(Z_SRED, f'<rect x="1880" y="700" width="40" height="160" rx="6"'
                    f' fill="{TKAN2}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, polka_s_bankami(440, 240, 520, t, 97, 5, False))
    s += SL(Z_SRED, hodiki(1180, 250, t, 1.2))
    s += SL(Z_SRED, lampa(960, 70, t, 1.3, True) + teplo(960, 90, 320, 260, .40))
    s += SL(Z_SRED, ten(zx, zy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.40)
    return s


def chay_nastaivaetsya(t):
    """Стол под абажуром: заварник с отбитым носиком под вязаной
    грелкой-курицей на пол-кадра, четыре блюдца с вареньем, сушки. Семья
    сидит вокруг, никто не тянется к чашкам, по циферблату ползёт улитка."""
    rnd = random.Random(3010)
    s = (f'<rect width="{W}" height="{H}" fill="#3f3122"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="700" fill="#5f4a32"/>')
    s += SL(Z_DAL, brevna(0, 0, W, 700, 84, 3))
    s += SL(Z_DAL, okno_izby(1560, 180, 320, 300, t, None, .6, False, True))
    s += SL(Z_SRED, polovicy(820, "#6b4428"))
    # ПЛИТА с большим чайником за столом
    s += SL(Z_SRED, f'<rect x="80" y="520" width="340" height="300" rx="8"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="100" y="546" width="300" height="60" rx="6"'
                    f' fill="#6f6256" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, chaynik_s_parom(250, 540, 1.3, t, .2, True))
    # СТОЛ со скатертью
    s += SL(Z_SRED, f'<rect x="420" y="760" width="1180" height="40" rx="8"'
                    f' fill="#e8e2d6" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M420,800 q{590:.0f},{36:.0f} {1180:.0f},0 l0,{90:.0f}'
                    f' q{-590:.0f},{36:.0f} {-1180:.0f},0 Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<path d="M{450+i*100:.0f},800 l{-10:.0f},{90:.0f}"'
                        f' stroke="#d8cbb0" stroke-width="5"/>')
    # ЗАВАРНИК под грелкой-курицей
    gx, gy = 960, 760
    s += SL(Z_SRED, f'<path d="M{gx-120:.0f},{gy:.0f} q{-20:.0f},{-130:.0f}'
                    f' {120:.0f},{-150:.0f} q{140:.0f},{20:.0f} {120:.0f},{150:.0f} Z"'
                    f' fill="#c8301f" stroke="{K}" stroke-width="6"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{gx-110+i*36:.0f},{gy-10:.0f} q{10:.0f},{-70:.0f}'
                        f' {2:.0f},{-120:.0f}" fill="none" stroke="#a8321c"'
                        f' stroke-width="5" opacity=".85"/>')
    s += SL(Z_SRED, f'<circle cx="{gx+86:.0f}" cy="{gy-146:.0f}" r="44" fill="#c8301f"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{gx+112:.0f},{gy-168:.0f} q{26:.0f},{-14:.0f}'
                    f' {40:.0f},{6:.0f} l{-34:.0f},{22:.0f} Z" fill="{ZOL}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="{gx+100:.0f}" cy="{gy-156:.0f}" r="5" fill="{K}"/>'
                    f'<path d="M{gx+70:.0f},{gy-186:.0f} q{14:.0f},{-20:.0f}'
                    f' {28:.0f},{-2:.0f} q{-6:.0f},{16:.0f} {-28:.0f},{2:.0f} Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M{gx-140:.0f},{gy-30:.0f} q{-44:.0f},{-12:.0f}'
                    f' {-56:.0f},{-36:.0f} l{18:.0f},{-12:.0f} q{12:.0f},{22:.0f}'
                    f' {44:.0f},{30:.0f} Z" fill="#b5803a" stroke="{K}"'
                    f' stroke-width="4"/>')
    # блюдца с вареньем, сахарница, сушки
    for i, bx_ in enumerate((560, 740, 1180, 1360)):
        s += SL(Z_SRED, f'<ellipse cx="{bx_:.0f}" cy="760" rx="72" ry="22"'
                        f' fill="#e8e2d6" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{bx_:.0f}" cy="752" rx="54" ry="15"'
                        f' fill="#8a2f22" stroke="#6b2419" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M1480,760 q{-6:.0f},{-70:.0f} {58:.0f},{-74:.0f}'
                    f' q{64:.0f},{4:.0f} {58:.0f},{74:.0f} Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{480+i*34:.0f}" cy="{730-((i*5)%3)*16:.0f}" r="26"'
                        f' fill="none" stroke="#c9a05a" stroke-width="13"/>')
    # ЧЕТВЕРО за столом
    for i, (fx_, fy_, fh_, col, pl) in enumerate(((620, 1060, 560, "#4a4038", False),
                                                  (820, 1070, 520, "#8a2f22", True),
                                                  (1180, 1066, 480, "#3f5a6a", False),
                                                  (1400, 1056, 500, "#6b3a6a", True))):
        s += SL(Z_SRED, figura(fx_, fy_, fh_, t, col=col, kant="#ffd98a",
                               platok=pl, boroda=(i == 0), ph=i * .3))
        rk, (ex, ey), _ = _ruka(fx_, fy_, fh_, 1, fh_ * .24, 46, t, col, "#ffd98a", i * .25, 3)
        rk2, (e2x_, e2y_), _ = _ruka(fx_, fy_, fh_, -1, fh_ * .24, 50, t, col,
                                     "#ffd98a", i * .25 + .4, 3)
        s += SL(Z_SRED, rk + rk2)
    # АБАЖУР и ходики с улиткой
    s += SL(Z_SRED, f'<path d="M700,0 v120" stroke="#6b4428" stroke-width="7"/>')
    s += SL(Z_SRED, lampa(700, 120, t, 2.0, True) + teplo(700, 170, 520, 420, .55))
    s += SL(Z_SRED, hodiki(1760, 560, t, 1.8))
    ulit = ((t * .12) % 1.0)
    a = -1.57 + ulit * 6.283
    s += SL(Z_SRED, f'<ellipse cx="{1760+54*math.cos(a):.0f}"'
                    f' cy="{560+54*math.sin(a)+40:.0f}" rx="18" ry="11" fill="#9a7c45"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<circle cx="{1760+54*math.cos(a)+6:.0f}"'
                    f' cy="{560+54*math.sin(a)+34:.0f}" r="11" fill="#b08a52"'
                    f' stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, kot(500, 1050, t, 1.5, "#3b3430", True))
    s += SL(Z_SRED, polka_s_bankami(1180, 300, 420, t, 101, 4, False))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def kust_kaliny_v_inee(t):
    """Куст калины у забора на пол-кадра, красные кисти в белом инее; просвет
    между досками расширен до окна — в нём настоящая калина. Рисованный Мороз
    дышит на куст, ягоды разгораются, горечь улетает зелёными рожицами."""
    rnd = random.Random(3011)
    s = nebo("rassv", t, False, 409)
    s += oblaka(t, 150, 4, 193, .34, "#ffe9c8")
    s += SL(Z_DAL, ulica_dal(1180, 360, 740, t, True, 151))
    s += SL(Z_DAL, izba_snaruzhi(1560, 380, 280, t, True, True, 103)
            + dym_stolbom(1588, 240, t, 260, .45, .4, 6))
    s += SL(Z_SRED, _merzlaya_zemlya(560, 409, False))
    s += SL(Z_SRED, sneg_lezhit(600, 30, "url(#sneg)"))
    # ЗАБОР с дорисованным окном-просветом
    s += SL(Z_SRED, zabor_shtaket(-40, 300, 1060, 420, 409, 64))
    px, py, pw, ph_ = 120, 340, 780, 320
    pr = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
          f' fill="#8aa8b4"/>')
    pr += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.4:.0f}"'
           f' fill="#c4d8e8"/>')
    pr += mesto_stoka(px, py, pw, ph_, "pryam")
    pr += (f'<rect x="{px-16:.0f}" y="{py-16:.0f}" width="{pw+32:.0f}"'
           f' height="{ph_+32:.0f}" rx="6" fill="none" stroke="#7d5636"'
           f' stroke-width="24"/>')
    s += SL(Z_SRED, pr)
    # КУСТ КАЛИНЫ на пол-кадра
    kx, kb = 1180, 1010
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{kb:.0f} q{-20:.0f},{-200:.0f} {-80:.0f},{-360:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{10:.0f},{-220:.0f} {70:.0f},{-380:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{40:.0f},{-180:.0f} {170:.0f},{-300:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{-60:.0f},{-160:.0f} {-190:.0f},{-250:.0f}"'
                    f' fill="none" stroke="#5e4430" stroke-width="14"/>')
    razg = A.ease(A.seg(t, 1.0, 1.6))
    for i, (gx_, gy_, gs) in enumerate(((1100, 660, 1.5), (1250, 630, 1.3),
                                        (1350, 720, 1.2), (990, 760, 1.25),
                                        (1180, 790, 1.4), (1430, 660, 1.0))):
        s += SL(Z_SRED, kalina_grozd(gx_, gy_, t, gs * (1 + .06 * razg), 13,
                                     409 + i, i * .2, True))
    for i in range(8):
        s += SL(Z_SRED, f'<path d="M{980+i*70:.0f},{600+((i*7)%4)*60:.0f}'
                        f' q{30:.0f},{-20:.0f} {60:.0f},{4:.0f}" fill="none"'
                        f' stroke="{INEY}" stroke-width="5" opacity=".7"/>')
    # МОРОЗ дышит на куст
    s += SL(Z_SRED, moroz_ded(1700, 1040, t, 1.0, .3))
    dyh = ((t * .7) % 1.0)
    for i in range(6):
        d = ((dyh + i / 6.0) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{1640-320*d:.0f}" cy="{760+30*math.sin(i+d*4):.0f}"'
                        f' rx="{24+50*d:.0f}" ry="{16+30*d:.0f}" fill="#eaf6ff"'
                        f' opacity="{(1-d)*.5:.2f}"/>')
    # РОЖИЦЫ-ГОРЕЧИ улетают
    for i in range(5):
        d = ((t * .5 + i / 5.0) % 1.0)
        rx_ = 1180 + 300 * d
        ry_ = 700 - 320 * d
        s += SL(Z_LETIT, f'<g opacity="{(1-d)*.85:.2f}">'
                         f'<circle cx="{rx_:.0f}" cy="{ry_:.0f}" r="22" fill="#6f8c4a"'
                         f' stroke="{K}" stroke-width="3.4"/>'
                         f'<circle cx="{rx_-7:.0f}" cy="{ry_-5:.0f}" r="4" fill="{K}"/>'
                         f'<circle cx="{rx_+7:.0f}" cy="{ry_-5:.0f}" r="4" fill="{K}"/>'
                         f'<path d="M{rx_-9:.0f},{ry_+9:.0f} q{9:.0f},{-8:.0f} {18:.0f},0"'
                         f' fill="none" stroke="{K}" stroke-width="3"/></g>')
    # ХОЗЯЙКА с корзиной тянется к кисти
    hx, hy, hh = 760, 1056, 660
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a3a52", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.3))
    tyan = A.ease(A.seg(t, .8, 1.4))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * (.28 + .08 * tyan), -34, t,
                              "#4a3a52", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .26, 40, t, "#4a3a52", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x + 8, e1y + 6, 1.0, 16, "#8a2f22", t, .2) + r2)
    s += SL(Z_SRED, f'<path d="M{e2x-54:.0f},{e2y+10:.0f} q{54:.0f},{20:.0f} {108:.0f},0'
                    f' l{-12:.0f},{76:.0f} h{-84:.0f} Z" fill="#b08a52" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    s += SL(Z_SRED, para_izo_rta(hx - 32, hy - hh * .80, t, .4, 1.0, .5))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    # синицы и калитка
    for i, (sx_, sy_) in enumerate(((1320, 560), (1460, 620))):
        s += SL(Z_SRED, ptica(sx_, sy_, t, 1.5, "#d6a63f", i * .4, "#4a6a78"))
    s += SL(Z_SRED, kalitka_rez(1760, 620, 180, 280, t, .12, True))
    s += SL(Z_SRED, inej_mel(409, 50, 960, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 16, 103, .34, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def vetka_s_kusta_i_puchok_s_rynka(t):
    """Кадр надвое: слева свой куст — хозяин секатором срезает ветку с тремя
    кистями; справа рыночный прилавок под навесом — продавщица протягивает
    покупательнице пучок калины, перевязанный ниткой."""
    rnd = random.Random(3012)
    s = nebo("den", t, False, 419)
    s += oblaka(t, 140, 5, 197, .40)
    # ЛЕВАЯ ПОЛОВИНА: свой куст
    s += SL(Z_DAL, ulica_dal(40, 420, 820, t, True, 157))
    s += SL(Z_SRED, _merzlaya_zemlya(600, 419, False))
    s += SL(Z_SRED, sneg_lezhit(640, 30, "url(#sneg)"))
    s += SL(Z_SRED, zabor_shtaket(-40, 420, 940, 220, 419, 62))
    kx, kb = 420, 1000
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{kb:.0f} q{-20:.0f},{-180:.0f} {-70:.0f},{-320:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{14:.0f},{-200:.0f} {80:.0f},{-340:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{50:.0f},{-150:.0f} {160:.0f},{-250:.0f}"'
                    f' fill="none" stroke="#5e4430" stroke-width="13"/>')
    srez = A.ease(A.seg(t, .8, .8))
    for i, (gx_, gy_, gs) in enumerate(((330, 700, 1.3), (470, 660, 1.2),
                                        (560, 760, 1.1))):
        dy_ = 180 * srez if i == 2 else 0
        s += SL(Z_SRED, kalina_grozd(gx_, gy_ + dy_, t, gs, 12, 419 + i, i * .25, True))
    hx, hy, hh = 700, 1056, 680
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a3a", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .34, -30, t, "#3f4a3a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .26, -22, t, "#3f4a3a", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x - 8, e1y + 8, 1.0, -16, "#6b4428", t, .2) + r2)
    rask = 26 * (1 - srez)
    s += SL(Z_SRED, f'<g transform="rotate(-24 {e1x:.0f} {e1y:.0f})">'
                    f'<path d="M{e1x-10:.0f},{e1y-10:.0f} l{-70:.0f},{-30-rask:.0f}'
                    f' M{e1x-10:.0f},{e1y+6:.0f} l{-70:.0f},{14+rask:.0f}"'
                    f' stroke="#c9ccd1" stroke-width="9"/>'
                    f'<circle cx="{e1x-6:.0f}" cy="{e1y-2:.0f}" r="9" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, para_izo_rta(hx - 34, hy - hh * .80, t, .3, 1.0, .5))
    # ПРАВАЯ ПОЛОВИНА: рыночный прилавок
    s += SL(Z_DAL, f'<rect x="{W*.5:.0f}" y="0" width="{W*.5:.0f}" height="{H}"'
                   f' fill="#8a98a8" opacity=".25"/>')
    nav = 4.0 * A.w(t, 3.0, .2)
    s += SL(Z_SRED, f'<g transform="rotate({nav:.1f} 1440 420)">'
                    f'<path d="M1020,420 q{420:.0f},{-80:.0f} {840:.0f},0 l{-20:.0f},{44:.0f}'
                    f' q{-400:.0f},{-70:.0f} {-800:.0f},0 Z" fill="#8a2f22"'
                    f' stroke="{K}" stroke-width="5.5"/></g>'
                    f'<rect x="1030" y="440" width="18" height="300" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="1840" y="440" width="18" height="300" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="1000" y="740" width="900" height="50" rx="8"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="1020" y="790" width="860" height="26" rx="5"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="4"/>')
    # весы, банки с мёдом, клюква в лотке
    s += SL(Z_SRED, f'<path d="M1120,740 l0,-120" stroke="{ZHELEZ}" stroke-width="9"/>'
                    f'<path d="M1040,620 h160" stroke="{ZHELEZ}" stroke-width="7"/>'
                    f'<path d="M1050,620 q{10:.0f},{50:.0f} {-6:.0f},{64:.0f}'
                    f' M1190,620 q{-10:.0f},{50:.0f} {6:.0f},{64:.0f}" fill="none"'
                    f' stroke="#9aa3a8" stroke-width="3.4"/>'
                    f'<ellipse cx="1046" cy="690" rx="46" ry="14" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<ellipse cx="1196" cy="690" rx="46" ry="14" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    for i in range(3):
        s += SL(Z_SRED, banka_moloka(1280 + i * 100, 740, .66, t, True, .82, "#d6a63f"))
    s += SL(Z_SRED, f'<rect x="1600" y="672" width="260" height="68" rx="8"'
                    f' fill="#b08a52" stroke="{K}" stroke-width="4.5"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<circle cx="{1620+((i*53)%230):.0f}" cy="{690+((i*31)%40):.0f}"'
                        f' r="9" fill="#c8301f" stroke="#7d1b11" stroke-width="2"/>')
    # ПРОДАВЩИЦА и ПОКУПАТЕЛЬНИЦА
    per = A.ease(A.seg(t, 1.0, 1.6))
    px_, py_, ph_ = 1200, 1050, 640
    s += SL(Z_SRED, figura(px_, py_, ph_, t, col="#3f4a3a", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.4))
    r3, (e3x, e3y), _ = _ruka(px_, py_, ph_, 1, ph_ * .30, -10, t, "#3f4a3a", "#ffd9a8", .3, 4)
    s += SL(Z_SRED, r3)
    zx_, zy_, zh_ = 1680, 1056, 650
    s += SL(Z_SRED, figura(zx_, zy_, zh_, t, col="#6b3a6a", kant="#ffd9a8", ph=.8))
    r4, (e4x, e4y), _ = _ruka(zx_, zy_, zh_, -1, zh_ * .30, -6, t, "#6b3a6a", "#ffd9a8", .5, 4)
    r5, (e5x, e5y), _ = _ruka(zx_, zy_, zh_, 1, zh_ * .24, 52, t, "#6b3a6a", "#ffd9a8", .9, 4)
    s += SL(Z_SRED, r4 + r5)
    s += SL(Z_SRED, f'<path d="M{e5x-40:.0f},{e5y+12:.0f} h80 l-8,72 h-64 Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    bx_ = e3x + (e4x - e3x) * per
    by_ = e3y + (e4y - e3y) * per
    s += SL(Z_SRED, kalina_grozd(bx_, by_ + 60, t, 1.1, 12, 431, .3, True)
            + f'<path d="M{bx_-24:.0f},{by_+18:.0f} h48" stroke="#b9a37a"'
              f' stroke-width="7"/>')
    s += SL(Z_SRED, para_izo_rta(px_ - 32, py_ - ph_ * .80, t, .3, .9, .45)
            + para_izo_rta(zx_ - 30, zy_ - zh_ * .80, t, .8, .9, .45))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45) + ten(px_, py_ + 6, 120, 20, .4)
            + ten(zx_, zy_ + 6, 120, 20, .4))
    s += SL(Z_PERED, f'<rect x="{W*.5-7:.0f}" y="0" width="14" height="{H}"'
                     f' fill="#dcecf8" opacity=".45"/>')
    s += SL(Z_SRED, dym_stolbom(240, 420, t, 280, .45, .4, 6))
    s += SL(Z_SRED, par(1240, 1000, t, 4, .5, 160, .45, 1.0))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def kalina_s_saharom_v_banke(t):
    """Кухонный стол: миска с калиной, деревянная толкушка, сахар в совке и
    чистая банка на пол-кадра. Хозяйка давит ягоды и перекладывает красное с
    прослойками сахара в банку; листки численника отлетают."""
    rnd = random.Random(3013)
    s = stena_gornicy_19(t, 41, 820, True, True)
    s += SL(Z_DAL, okno_izby(1500, 180, 360, 320, t, None, .7, False, True))
    s += SL(Z_SRED, stol(120, 760, 1120, 46, True))
    # МИСКА с калиной и толкушка
    s += SL(Z_SRED, f'<path d="M260,760 q{-16:.0f},{-110:.0f} {150:.0f},{-120:.0f}'
                    f' q{170:.0f},{10:.0f} {150:.0f},{120:.0f} Z" fill="#b9a082"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<ellipse cx="410" cy="648" rx="152" ry="38" fill="#8a2f22"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    davl = abs(A.w(t, 1.1, .0))
    for i in range(14):
        a = i * .45
        s += SL(Z_SRED, f'<circle cx="{410+110*math.cos(a)*.9:.0f}"'
                        f' cy="{644+26*math.sin(a):.0f}" r="{12-4*davl:.0f}"'
                        f' fill="#c8301f" stroke="#7d1b11" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<rect x="{392:.0f}" y="{420+60*davl:.0f}" width="36" height="200"'
                    f' rx="12" fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="410" cy="{620+60*davl:.0f}" rx="56" ry="22"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="4.5"/>')
    # САХАР в совке
    s += SL(Z_SRED, f'<path d="M700,760 h190 l-14,-80 h-162 Z" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="795" cy="680" rx="81" ry="20" fill="#f8f4e8"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M880,700 l{70:.0f},{-40:.0f}" stroke="#9aa3a8"'
                    f' stroke-width="9"/>')
    # БАНКА на пол-кадра, наполняется прослойками
    nap = A.ease(A.seg(t, .8, 3.2))
    bx, by = 1180, 780
    s += SL(Z_SRED, f'<path d="M{bx-110:.0f},{by-420:.0f} q0,{-50:.0f} {30:.0f},{-60:.0f}'
                    f' h{160:.0f} q{30:.0f},{10:.0f} {30:.0f},{60:.0f} l0,{420:.0f}'
                    f' q{-110:.0f},{30:.0f} {-220:.0f},0 Z" fill="{STEKLO}"'
                    f' opacity=".55" stroke="{K}" stroke-width="6"/>')
    for i in range(6):
        if nap * 6 < i:
            break
        yy = by - 30 - i * 64
        s += SL(Z_SRED, f'<rect x="{bx-104:.0f}" y="{yy-40:.0f}" width="208" height="44"'
                        f' rx="6" fill="#8a2f22" opacity=".95"/>'
                        f'<rect x="{bx-104:.0f}" y="{yy-56:.0f}" width="208" height="18"'
                        f' rx="4" fill="#f8f4e8" opacity=".9"/>')
    s += SL(Z_SRED, f'<path d="M{bx-86:.0f},{by-400:.0f} q{-10:.0f},{200:.0f}'
                    f' {4:.0f},{340:.0f}" fill="none" stroke="#ffffff"'
                    f' stroke-width="12" opacity=".4"/>')
    # ЛИСТКИ численника отлетают
    s += SL(Z_SRED, f'<rect x="1560" y="560" width="170" height="220" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1560" y="560" width="170" height="44" rx="8"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="4"/>')
    for i in range(3):
        d = ((t * .55 + i * .33) % 1.0)
        s += SL(Z_LETIT, f'<rect x="{1580-240*d:.0f}" y="{620+280*d*d:.0f}" width="110"'
                         f' height="140" rx="6" fill="#f2ead6" opacity="{(1-d)*.85:.2f}"'
                         f' transform="rotate({-d*150:.0f} {1635-240*d:.0f}'
                         f' {690+280*d*d:.0f})" stroke="{K}" stroke-width="3"/>')
    # ХОЗЯЙКА
    hx, hy, hh = 700, 1050, 680
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.3))
    s += SL(Z_SRED, f'<path d="M{hx-110:.0f},{hy-hh*.46:.0f} q{110:.0f},{-24:.0f}'
                    f' {220:.0f},0 l0,{hh*.32:.0f} q{-110:.0f},{24:.0f} {-220:.0f},0 Z"'
                    f' fill="{RUSH}" opacity=".9" stroke="{K}" stroke-width="4"/>')
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .34, -24 + 12 * davl, t,
                              "#8a2f22", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .24, 6, t, "#8a2f22", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, kot(1480, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, polka_s_bankami(180, 400, 520, t, 103, 5, False))
    s += SL(Z_SRED, f'<rect x="900" y="820" width="90" height="170" rx="6"'
                    f' fill="{RUSH}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(960, 120, t, 1.3, True) + teplo(960, 150, 340, 280, .45))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def pirog_s_kalinoy(t):
    """Стол: на доске большой закрытый пирог на пол-кадра, в прорезях сверху
    видна тёмно-красная начинка, идёт пар. Бабушка держит край доски
    прихватками, двое внуков подняли носы и принюхиваются."""
    rnd = random.Random(3014)
    s = stena_gornicy_19(t, 43, 820, True, True)
    s += SL(Z_SRED, pech(1500, 280, 420, 540, t, True, True, False))
    s += SL(Z_SRED, ogon(1660, 700, t, 1.2, .2, 6) + teplo(1660, 680, 360, 300, .5))
    s += SL(Z_SRED, stol(160, 780, 1120, 46, True))
    # ДОСКА и ПИРОГ на пол-кадра
    s += SL(Z_SRED, f'<rect x="300" y="740" width="840" height="46" rx="10"'
                    f' fill="#b9a082" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1140,760 q{70:.0f},{4:.0f} {90:.0f},{-14:.0f}'
                    f' l0,{34:.0f} q{-30:.0f},{20:.0f} {-90:.0f},{10:.0f} Z"'
                    f' fill="#a8956f" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<path d="M360,740 q{360:.0f},{-230:.0f} {720:.0f},0'
                    f' q{-40:.0f},{40:.0f} {-360:.0f},{40:.0f} q{-320:.0f},0'
                    f' {-360:.0f},{-40:.0f} Z" fill="#d6a63f" stroke="{K}"'
                    f' stroke-width="7"/>')
    for i in range(5):
        px_ = 520 + i * 90
        s += SL(Z_SRED, f'<path d="M{px_:.0f},{640+((i*5)%3)*18:.0f}'
                        f' q{30:.0f},{-26:.0f} {60:.0f},{-2:.0f} q{-26:.0f},{22:.0f}'
                        f' {-60:.0f},{2:.0f} Z" fill="#8a2f22" stroke="#6b2419"'
                        f' stroke-width="3.4"/>')
        s += SL(Z_SRED, par(px_ + 30, 600 + ((i * 5) % 3) * 18, t, 3, .5, 150, .4, .9))
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{420+i*110:.0f},720 q{30:.0f},{-20:.0f} {56:.0f},{-2:.0f}"'
                        f' fill="none" stroke="#c09a3a" stroke-width="5" opacity=".8"/>')
    # струйка запаха
    for i in range(6):
        d = ((t * .5 + i / 6.0) % 1.0)
        s += SL(Z_SRED, f'<path d="M{700+40*math.sin(i+d*5):.0f},{560-220*d:.0f}'
                        f' q{40:.0f},{-40:.0f} {4:.0f},{-80:.0f}" fill="none"'
                        f' stroke="#d89a90" stroke-width="{7-3*d:.1f}"'
                        f' opacity="{(1-d)*.55:.2f}"/>')
    # БАБУШКА держит край доски
    bx, by, bh = 1240, 1050, 680
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd98a",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, -1, bh * .34, -12, t, "#4a3a52", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, 1, bh * .26, 22, t, "#4a3a52", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x - 10, e1y + 8, 1.2, -14, "#8a2f22", t, .2)
            + r2 + varezhka(e2x + 10, e2y + 10, 1.2, 14, "#8a2f22", t, .7))
    # ДВОЕ ВНУКОВ принюхиваются
    for i, (vx_, vy_, vh_, col) in enumerate(((620, 1066, 440, "#3f5a6a"),
                                              (860, 1056, 420, "#c8301f"))):
        nos = 6 * A.w(t, 1.6, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({-10-nos:.1f} {vx_:.0f} {vy_-vh_*.5:.0f})">'
                + figura(vx_, vy_, vh_, t, col=col, kant="#ffd98a", ph=i * .4) + '</g>')
        rk, (ex, ey), _ = _ruka(vx_, vy_, vh_, 1, vh_ * .24, 52, t, col, "#ffd98a", i * .3, 4)
        s += SL(Z_SRED, rk)
    # нож, полотенце, чайник, кот
    s += SL(Z_SRED, f'<path d="M200,780 l{150:.0f},{-26:.0f} l{14:.0f},{20:.0f}'
                    f' l{-160:.0f},{30:.0f} Z" fill="#c9ccd1" stroke="{K}"'
                    f' stroke-width="4"/>'
                    f'<rect x="348" y="736" width="64" height="22" rx="6"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="180" y="840" width="90" height="170" rx="6"'
                    f' fill="{RUSH}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, chaynik_s_parom(1440, 780, 1.0, t, .4, True))
    kot_ = A.ease(A.seg(t, 1.4, 1.2))
    s += SL(Z_SRED, f'<g transform="translate(0,{-60*kot_:.0f})">'
            + kot(1060, 1060, t, 1.6, "#3b3430", False) + '</g>')
    s += SL(Z_SRED, polka_s_bankami(240, 380, 500, t, 107, 4, False))
    s += SL(Z_SRED, ten(bx, by + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def kalinovoe_varene_v_rozetke(t):
    """Стол с чаем, две розетки калинового варенья: дед подносит ложку ко рту
    и крякает от горчинки, внучка высунула язык от старания и вылавливает
    ягоды по одной на край блюдца."""
    rnd = random.Random(3015)
    s = stena_gornicy_19(t, 47, 840, True, True)
    s += SL(Z_DAL, okno_izby(1540, 200, 340, 300, t, None, .5, False, True))
    s += SL(Z_SRED, stol(200, 780, 1180, 46, True))
    # ДВЕ РОЗЕТКИ варенья на треть кадра
    for i, rx_ in enumerate((620, 1120)):
        s += SL(Z_SRED, f'<ellipse cx="{rx_:.0f}" cy="780" rx="170" ry="54"'
                        f' fill="#e8e2d6" stroke="{K}" stroke-width="6"/>'
                        f'<ellipse cx="{rx_:.0f}" cy="762" rx="140" ry="42"'
                        f' fill="#f2ead6" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{rx_:.0f}" cy="758" rx="112" ry="32"'
                        f' fill="#8a2f22" stroke="#6b2419" stroke-width="4"/>')
        for k in range(7):
            a = k * .9
            s += SL(Z_SRED, f'<circle cx="{rx_+72*math.cos(a)*.9:.0f}"'
                            f' cy="{756+18*math.sin(a):.0f}" r="12" fill="#c8301f"'
                            f' stroke="#7d1b11" stroke-width="2.6"/>')
    # ДЕД с ложкой и стаканом в подстаканнике
    dx, dy, dh = 420, 1050, 660
    lozh = A.ease(A.seg(t, .6, 1.2))
    s += SL(Z_SRED, f'<rect x="{dx-90:.0f}" y="{dy-20:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(dx, dy - 10, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, ph=.2))
    s += SL(Z_SRED, f'<path d="M{dx-80:.0f},{dy-dh*.62:.0f} q{80:.0f},{-20:.0f}'
                    f' {160:.0f},0 l{10:.0f},{dh*.30:.0f} q{-90:.0f},{24:.0f}'
                    f' {-180:.0f},0 Z" fill="#3f4a3a" stroke="{K}" stroke-width="4.5"/>')
    r1, (e1x, e1y), _ = _ruka(dx, dy - 10, dh, 1, dh * .30, -34 - 16 * lozh, t,
                              "#4a4038", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy - 10, dh, -1, dh * .26, 20, t,
                              "#4a4038", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{50:.0f},{-20:.0f}"'
                    f' stroke="#c9ccd1" stroke-width="6"/>'
                    f'<ellipse cx="{e1x+62:.0f}" cy="{e1y-24:.0f}" rx="22" ry="13"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<path d="M{e2x-30:.0f},{e2y+10:.0f} h60 l-6,74 h-48 Z"'
                    f' fill="{STEKLO}" opacity=".6" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e2x-34:.0f},{e2y+6:.0f} h68 l-8,86 h-52 Z"'
                    f' fill="none" stroke="{MED}" stroke-width="6"/>'
                    f'<path d="M{e2x+34:.0f},{e2y+30:.0f} q{28:.0f},{16:.0f} {0:.0f},{34:.0f}"'
                    f' fill="none" stroke="{MED}" stroke-width="6"/>')
    s += SL(Z_SRED, par(e2x, e2y - 10, t, 3, .45, 130, .4, .8))
    # ВНУЧКА вылавливает ягоды
    vx, vy, vh = 1320, 1056, 520
    vyl = A.ease(A.seg(t, 1.0, 1.4))
    s += SL(Z_SRED, f'<rect x="{vx-80:.0f}" y="{vy-20:.0f}" width="160" height="24"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(vx, vy - 10, vh, t, col="#c8301f", kant="#ffd98a",
                           ph=.6, naklon=2.0))
    r3, (e3x, e3y), _ = _ruka(vx, vy - 10, vh, -1, vh * .34, -16 + 14 * vyl, t,
                              "#c8301f", "#ffd98a", .3, 5)
    r4, (e4x, e4y), _ = _ruka(vx, vy - 10, vh, 1, vh * .24, 36, t,
                              "#c8301f", "#ffd98a", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, f'<path d="M{e3x:.0f},{e3y:.0f} l{-54:.0f},{-16:.0f}"'
                    f' stroke="#c9ccd1" stroke-width="6"/>'
                    f'<ellipse cx="{e3x-66:.0f}" cy="{e3y-20:.0f}" rx="20" ry="12"'
                    f' fill="#dde3e8" stroke="{K}" stroke-width="3.2"/>'
                    f'<circle cx="{e3x-66:.0f}" cy="{e3y-24:.0f}" r="9" fill="#c8301f"'
                    f' opacity="{vyl:.2f}"/>')
    # ягоды, сложенные на край блюдца
    for i in range(4):
        if vyl * 4 < i:
            break
        s += SL(Z_SRED, f'<circle cx="{1240+i*26:.0f}" cy="742" r="11" fill="#c8301f"'
                        f' stroke="#7d1b11" stroke-width="2.6"/>')
    # сушки, чайник, сахарница, кот
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{880+i*30:.0f}" cy="{740-((i*5)%3)*14:.0f}" r="24"'
                        f' fill="none" stroke="#c9a05a" stroke-width="12"/>')
    s += SL(Z_SRED, chaynik_s_parom(1600, 780, 1.0, t, .3, True))
    s += SL(Z_SRED, f'<path d="M260,780 q{-6:.0f},{-66:.0f} {56:.0f},{-70:.0f}'
                    f' q{62:.0f},{4:.0f} {56:.0f},{70:.0f} Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="316" cy="706" rx="52" ry="14" fill="#d8cbb0"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, kot(900, 1056, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, polka_s_bankami(240, 400, 480, t, 109, 4, False))
    s += SL(Z_SRED, lampa(960, 130, t, 1.4, True) + teplo(960, 160, 360, 300, .46))
    s += SL(Z_SRED, ten(dx, dy + 20, 130, 22, .45) + ten(vx, vy + 20, 110, 19, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def obuh_po_uglam_doma(t):
    """Угол бревенчатого дома зимним днём: хозяин обухом топора стучит по
    углу сруба, по косяку, по перилам и воротам — и от каждого удара из щелей
    выскакивают мелкие рисованные чертенята и улепётывают за забор."""
    rnd = random.Random(3016)
    s = nebo("den", t, False, 431)
    s += oblaka(t, 140, 5, 199, .40)
    s += SL(Z_DAL, ulica_dal(1240, 420, 700, t, True, 163))
    # УГОЛ ДОМА на пол-кадра
    s += SL(Z_SRED, f'<rect x="0" y="120" width="980" height="760" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, brevna(0, 120, 980, 760, 86, 1))
    s += SL(Z_SRED, f'<path d="M980,120 l340,120 l0,760 l-340,-120 Z" fill="#5e4430"'
                    f' stroke="{K}" stroke-width="6"/>')
    for i in range(8):
        s += SL(Z_SRED, f'<path d="M980,{160+i*86:.0f} l340,120" stroke="#4a3526"'
                        f' stroke-width="7" opacity=".8"/>')
    s += SL(Z_SRED, f'<path d="M-20,120 l500,-110 l860,230 l0,60 l-860,-220 l-500,110 Z"'
                    f' fill="#4a3526" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-20,110 l500,-112 l860,232" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="20" opacity=".92"/>')
    # крыльцо с перилами, дверь с косяком
    s += SL(Z_SRED, f'<rect x="200" y="620" width="300" height="260" rx="6"'
                    f' fill="#3f2d1c" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="170" y="590" width="360" height="36" rx="6"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="120" y="880" width="520" height="30" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="140" y="910" width="480" height="26" rx="5"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M150,880 l0,-120 M600,880 l0,-120" stroke="#7d5636"'
                    f' stroke-width="14"/>'
                    f'<path d="M150,790 h450" stroke="#8a6342" stroke-width="11"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(920, 431, False))
    s += SL(Z_SRED, sneg_lezhit(940, 28, "url(#sneg)"))
    # ХОЗЯИН с топором
    ud = abs(A.w(t, .9, .0))
    hx, hy, hh = 1180, 1050, 700
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a3a", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .32, -14 + 30 * ud, t,
                              "#3f4a3a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .28, -8 + 26 * ud, t,
                              "#3f4a3a", "#ffd9a8", .5, 5)
    s += SL(Z_SRED, r1 + varezhka(e1x - 8, e1y + 8, 1.0, -14, "#6b4428", t, .2) + r2)
    s += SL(Z_SRED, f'<g transform="rotate({-26+30*ud:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-120:.0f}" y="{e1y-10:.0f}" width="150" height="20"'
                    f' rx="8" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e1x-160:.0f},{e1y-56:.0f} q{-38:.0f},{56:.0f}'
                    f' {0:.0f},{112:.0f} l{44:.0f},{-14:.0f} l0,{-86:.0f} Z"'
                    f' fill="#c9ccd1" stroke="{K}" stroke-width="6"/></g>')
    s += SL(Z_SRED, para_izo_rta(hx - 34, hy - hh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    # ЧЕРТЕНЯТА выскакивают из щелей и улепётывают за забор
    for i in range(5):
        d = ((t * .55 + i / 5.0) % 1.0)
        cx_ = 900 + 760 * d
        cy_ = 940 - 120 * math.sin(d * 3.14)
        s += SL(Z_SRED, f'<g opacity="{.95*(1-d*.35):.2f}">'
                + chertenok(cx_, cy_, t, 1.15, i * .3, "#5e3a6a") + '</g>')
    s += SL(Z_SRED, zabor_shtaket(1560, 700, 420, 240, 431, 58))
    # поленница, сани, собака, ворона на крыше
    s += SL(Z_SRED, f'<rect x="700" y="940" width="240" height="130" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(10):
        s += SL(Z_SRED, f'<circle cx="{722+(i%5)*48:.0f}" cy="{968+(i//5)*52:.0f}" r="22"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, sani_s_rogozhey(1700, 1040, .72, t, .3, False))
    lay = 8 * A.w(t, 1.2, .2)
    s += SL(Z_SRED, f'<ellipse cx="1480" cy="1010" rx="70" ry="34" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{1544+lay:.0f}" cy="976" r="28" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M{1566+lay:.0f},{962:.0f} l{14:.0f},{-26:.0f}'
                    f' l{10:.0f},{26:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3"/>'
                    f'<path d="M{1570+lay:.0f},{988:.0f} q{16:.0f},{10:.0f} {-2:.0f},{18:.0f}"'
                    f' fill="none" stroke="{K}" stroke-width="4"/>')
    vor = 6 * A.w(t, 2.0, .4)
    s += SL(Z_SRED, f'<ellipse cx="{520+vor:.0f}" cy="40" rx="46" ry="30"'
                    f' fill="#23242a" stroke="{K}" stroke-width="3.6"/>'
                    f'<circle cx="{554+vor:.0f}" cy="10" r="21" fill="#23242a"'
                    f' stroke="{K}" stroke-width="3.2"/>'
                    f'<path d="M{574+vor:.0f},8 l26,6 l-26,7 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="2.4"/>')
    s += SL(Z_SRED, dym_stolbom(320, 100, t, 240, .42, .4, 6))
    s += SL(Z_SRED, par(1480, 960, t, 3, .45, 140, .4, .9))
    s += SL(Z_SRED, inej_mel(431, 44, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def meteoploschadka(t):
    """Смена главы: метеоплощадка в поле — белая будка на ножках с жалюзи на
    пол-кадра, мачта с флюгером и вертушкой, дождемер, сетчатая ограда, без
    флагов и надписей. Наблюдатель открывает дверцу и пишет в журнал."""
    rnd = random.Random(3017)
    s = nebo("den", t, False, 433)
    s += oblaka(t, 130, 6, 211, .45)
    s += SL(Z_DAL, ulica_dal(60, 480, 700, t, True, 167))
    s += SL(Z_DAL, f'<rect x="1500" y="420" width="380" height="200" rx="8"'
                   f' fill="#d8cbb0" stroke="{K}" stroke-width="6"/>'
                   f'<path d="M1470,420 l210,-110 l230,110 Z" fill="#8a7a62"'
                   f' stroke="{K}" stroke-width="5.5"/>'
                   f'<rect x="1560" y="480" width="90" height="90" rx="5"'
                   f' fill="#8aa8b4" stroke="{K}" stroke-width="4"'
                   f' opacity="{.7+.25*A.w(t,4.0,.3):.2f}"/>')
    s += SL(Z_DAL, dym_stolbom(1700, 300, t, 260, .45, .4, 6))
    s += SL(Z_SRED, f'<rect x="0" y="620" width="{W}" height="460" fill="#dce7f2"/>')
    s += SL(Z_SRED, sneg_lezhit(650, 32, "url(#sneg)"))
    # СЕТЧАТАЯ ОГРАДА
    for i in range(16):
        s += SL(Z_SRED, f'<path d="M{40+i*126:.0f},700 v220" stroke="#9aa3a8"'
                        f' stroke-width="4" opacity=".75"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M0,{710+i*56:.0f} h{W}" stroke="#9aa3a8"'
                        f' stroke-width="4" opacity=".75"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="{80+i*440:.0f}" y="680" width="20" height="260"'
                        f' fill="{BETON2}" stroke="{K}" stroke-width="3.6"/>')
    # БУДКА на ножках
    bx, by, bw, bh = 540, 420, 520, 360
    s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}"'
                    f' rx="8" fill="#f2ead6" stroke="{K}" stroke-width="7"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{bx+14:.0f},{by+30+i*36:.0f} h{bw-28:.0f}"'
                        f' stroke="#d8cbb0" stroke-width="12"/>')
    otkr = A.ease(A.seg(t, .8, 1.2))
    s += SL(Z_SRED, f'<g transform="rotate({-46*otkr:.1f} {bx+bw:.0f} {by:.0f})">'
                    f'<rect x="{bx+bw*.5:.0f}" y="{by:.0f}" width="{bw*.5:.0f}"'
                    f' height="{bh:.0f}" rx="6" fill="#f8f4e8" stroke="{K}"'
                    f' stroke-width="6"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{bx+bw*.5+12:.0f},{by+30+i*36:.0f} h{bw*.5-24:.0f}"'
                        f' stroke="#dde3e8" stroke-width="10"/>')
    s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, f'<path d="M{bx-30:.0f},{by:.0f} l{bw*.5+30:.0f},{-70:.0f}'
                    f' l{bw*.5+30:.0f},{70:.0f} Z" fill="#c9ccd1" stroke="{K}"'
                    f' stroke-width="6"/>')
    for i in (-1, 1):
        s += SL(Z_SRED, f'<rect x="{bx+bw*.5+i*bw*.38-12:.0f}" y="{by+bh:.0f}"'
                        f' width="24" height="300" fill="#c9ccd1" stroke="{K}"'
                        f' stroke-width="4.5"/>')
    # МАЧТА с флюгером и вертушкой
    s += SL(Z_SRED, f'<rect x="1230" y="240" width="20" height="700" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    fl = 12 * A.w(t, 3.0, .2)
    s += SL(Z_SRED, f'<g transform="rotate({fl:.1f} 1240 260)">'
                    f'<path d="M1240,260 l{130:.0f},{30:.0f} l{-130:.0f},{30:.0f} Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1240,260 l{-80:.0f},{30:.0f} l{80:.0f},{30:.0f}"'
                    f' fill="none" stroke="{ZHELEZ}" stroke-width="7"/></g>')
    vert = (t * 400) % 360
    s += SL(Z_SRED, f'<g transform="rotate({vert:.0f} 1240 420)">')
    for i in range(4):
        a = i * 1.57
        s += SL(Z_SRED, f'<ellipse cx="{1240+60*math.cos(a):.0f}"'
                        f' cy="{420+60*math.sin(a):.0f}" rx="26" ry="18" fill="#dde3e8"'
                        f' stroke="{K}" stroke-width="3.4"'
                        f' transform="rotate({math.degrees(a):.0f}'
                        f' {1240+60*math.cos(a):.0f} {420+60*math.sin(a):.0f})"/>')
    s += SL(Z_SRED, '</g>')
    # ДОЖДЕМЕР и столбик со шкалой без цифр
    s += SL(Z_SRED, f'<path d="M1500,940 h120 l-14,-200 h-92 Z" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="1560" cy="740" rx="46" ry="14" fill="#dde3e8"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<rect x="1550" y="700" width="20" height="44" fill="{BETON2}"/>')
    s += SL(Z_SRED, f'<rect x="1780" y="620" width="30" height="330" fill="#f2ead6"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<path d="M1784,{650+i*26:.0f} h{16 if i%3 else 24:.0f}"'
                        f' stroke="#5f5a4e" stroke-width="3"/>')
    # НАБЛЮДАТЕЛЬ
    nx, ny, nh = 1000, 1000, 680
    s += SL(Z_SRED, figura(nx, ny, nh, t, col="#3f4a56", kant="#ffd9a8",
                           tulup=True, shapka=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(nx, ny, nh, -1, nh * .32, -22, t, "#3f4a56", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(nx, ny, nh, 1, nh * .26, 10, t, "#3f4a56", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<rect x="{e2x-50:.0f}" y="{e2y:.0f}" width="110" height="80"'
                    f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="4"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{e2x-40:.0f},{e2y+18+i*16:.0f} q{28:.0f},{-5:.0f}'
                        f' {56:.0f},0" fill="none" stroke="#8a7a62" stroke-width="3"/>')
    pish = 5 * A.w(t, 1.4, .1)
    s += SL(Z_SRED, f'<path d="M{e2x+30+pish:.0f},{e2y+10:.0f} l{26:.0f},{-54:.0f}"'
                    f' stroke="#d6a63f" stroke-width="7"/>')
    s += SL(Z_SRED, para_izo_rta(nx - 34, ny - nh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(nx, ny + 6, 130, 22, .45))
    vor = 6 * A.w(t, 2.2, .4)
    s += SL(Z_SRED, f'<ellipse cx="{300+vor:.0f}" cy="700" rx="44" ry="28"'
                    f' fill="#23242a" stroke="{K}" stroke-width="3.6"/>'
                    f'<circle cx="{332+vor:.0f}" cy="672" r="20" fill="#23242a"'
                    f' stroke="{K}" stroke-width="3.2"/>'
                    f'<path d="M{352+vor:.0f},670 l26,6 l-26,7 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="2.4"/>')
    s += SL(Z_SRED, inej_mel(433, 46, 960, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 14, 107, .3, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def tulup_naraspashku_u_peril(t):
    """Крыльцо избы утром: хозяин в тулупе нараспашку поднял рукавицу вверх,
    держась за столб. Вокруг него по словам встают три значка — струя ветра,
    воробей на ветке, огонёк в печной заслонке."""
    rnd = random.Random(3018)
    s = nebo("rassv", t, False, 439)
    s += oblaka(t, 150, 5, 223, .38)
    s += SL(Z_DAL, ulica_dal(1180, 460, 740, t, True, 173))
    s += SL(Z_DAL, goloe_derevo_ld(1420, 560, 420, t, 439, 7, True))
    # ИЗБА и КРЫЛЬЦО
    s += SL(Z_SRED, f'<rect x="0" y="120" width="1060" height="700" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, brevna(0, 120, 1060, 700, 88, 2))
    s += SL(Z_SRED, f'<path d="M-20,120 l540,-120 l560,120 l0,50 l-560,-116 l-540,120 Z"'
                    f' fill="#4a3526" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-20,110 l540,-122 l560,122" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="20" opacity=".92"/>')
    s += SL(Z_SRED, dver(220, 340, 300, 480, .0, "url(#derev)", True, False))
    s += SL(Z_SRED, okno_izby(640, 340, 300, 260, t, None, .4, True, True))
    s += SL(Z_SRED, f'<rect x="60" y="820" width="900" height="34" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="80" y="854" width="860" height="26" rx="5"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="100" y="880" width="820" height="26" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<rect x="120" y="500" width="30" height="330" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="900" y="500" width="30" height="330" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M135,620 h780" stroke="#8a6342" stroke-width="13"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(900, 439, False))
    s += SL(Z_SRED, sneg_lezhit(920, 28, "url(#sneg)"))
    # ХОЗЯИН в тулупе нараспашку
    hx, hy, hh = 560, 820, 700
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a4038", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    s += SL(Z_SRED, f'<path d="M{hx-120:.0f},{hy-hh*.64:.0f} q{30:.0f},{200:.0f}'
                    f' {10:.0f},{380:.0f} l{-70:.0f},{-10:.0f} q{10:.0f},{-200:.0f}'
                    f' {-10:.0f},{-380:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="5"/>'
                    f'<path d="M{hx+120:.0f},{hy-hh*.64:.0f} q{-30:.0f},{200:.0f}'
                    f' {-10:.0f},{380:.0f} l{70:.0f},{-10:.0f} q{-10:.0f},{-200:.0f}'
                    f' {10:.0f},{-380:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="5"/>')
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .34, -52, t, "#4a4038", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .26, -34, t, "#4a4038", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x + 6, e1y - 10, 1.1, 10, "#6b4428", t, .2) + r2)
    s += SL(Z_SRED, para_izo_rta(hx - 36, hy - hh * .80, t, .3, 1.1, .55))
    # ТРИ ЗНАЧКА по словам
    for i, (zx_, zy_) in enumerate(((1300, 300), (1520, 450), (1700, 640))):
        vst = A.out(A.seg(t, .6 + i * .5, .6))
        if vst < .02:
            continue
        s += SL(Z_SRED, f'<g opacity="{vst:.2f}" transform="translate(0,{50*(1-vst):.0f})">'
                        f'<circle cx="{zx_:.0f}" cy="{zy_:.0f}" r="90" fill="#f2ead6"'
                        f' stroke="{K}" stroke-width="5"/>')
        if i == 0:
            for k in range(3):
                s += SL(Z_SRED, f'<path d="M{zx_-60:.0f},{zy_-20+k*22:.0f}'
                                f' q{50:.0f},{-14:.0f} {100:.0f},{4:.0f}" fill="none"'
                                f' stroke="#6f7a84" stroke-width="7"/>')
        elif i == 1:
            s += SL(Z_SRED, ptica(zx_, zy_ + 10, t, 1.6, "#8a7a62", .2, "#6f6256"))
        else:
            s += SL(Z_SRED, f'<path d="M{zx_-54:.0f},{zy_+40:.0f} h108 l-10,-80 h-88 Z"'
                            f' fill="#3f2d1c" stroke="{K}" stroke-width="4"/>'
                    + ogon(zx_, zy_ + 30, t, .8, i * .2, 5))
        s += SL(Z_SRED, '</g>')
    # веник, вёдра, рябина, собака, дым
    s += SL(Z_SRED, dvorovye_veschi(180, 900, 320, t, 439, ["metla", "vedro"]))
    s += SL(Z_SRED, ryabina(1120, 980, t, 1.5, 6)
            + kalina_grozd(1160, 900, t, 1.0, 11, 443, .3))
    zev = A.ease(A.seg(t, 1.2, .8))
    s += SL(Z_SRED, f'<ellipse cx="1000" cy="1020" rx="72" ry="34" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="1064" cy="988" r="28" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3.6"/>'
                    f'<path d="M1086,{968:.0f} l{12:.0f},{-26:.0f} l{12:.0f},{26:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="3"/>'
                    f'<ellipse cx="1086" cy="{1000+6*zev:.0f}" rx="{10:.0f}"'
                    f' ry="{6+10*zev:.0f}" fill="#4a2a1e"/>')
    s += SL(Z_SRED, dym_stolbom(400, 60, t, 220, .45, .4, 6))
    s += SL(Z_SRED, ten(hx, hy + 6, 140, 24, .4))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def dym_stolbom_nad_derevney(t):
    """Деревня в тихий день: из каждой трубы дым стоит ровным столбом, бельё
    на верёвке висит не шелохнувшись, флюгер замер. Дед держит послюнявленную
    рукавицу над головой, а из-за леса выглядывает Мороз и потирает руки."""
    rnd = random.Random(3019)
    s = nebo("den", t, False, 443)
    s += oblaka(t, 110, 3, 227, .28)
    # ЛЕС на горизонте
    for i in range(22):
        ex_ = -40 + i * 92
        eh = rnd.uniform(140, 260)
        s += SL(Z_DAL, f'<path d="M{ex_:.0f},520 l{36:.0f},{-eh:.0f} l{36:.0f},{eh:.0f} Z"'
                       f' fill="#2f4a3a" stroke="{K}" stroke-width="4"/>')
    # ДОМА с дымами столбом
    for i, (ix, iw, sd) in enumerate(((120, 300, 109), (560, 340, 113),
                                      (1060, 320, 127), (1520, 360, 131))):
        s += SL(Z_SRED, izba_snaruzhi(ix, 640 + (i % 2) * 20, iw, t, True, True, sd))
        s += SL(Z_SRED, dym_stolbom(ix + iw * .12, 640 - iw * .62, t, 480, .55, .38, 8))
    s += SL(Z_SRED, _merzlaya_zemlya(700, 443, False))
    s += SL(Z_SRED, sneg_lezhit(740, 34, "url(#sneg)"))
    s += SL(Z_SRED, zabor_shtaket(-40, 740, 2000, 160, 443, 64))
    # БЕЛЬЁ не шелохнётся
    s += SL(Z_SRED, f'<path d="M400,660 h420" stroke="#b9a37a" stroke-width="5"/>')
    for i, (px_, pw_, col) in enumerate(((430, 90, "#e8e2d6"), (560, 76, "#8aa8b4"),
                                         (680, 84, "#d6a63f"))):
        s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="660" width="{pw_:.0f}" height="150"'
                        f' rx="6" fill="{col}" stroke="{K}" stroke-width="4"/>')
    # ФЛЮГЕР замер
    s += SL(Z_SRED, f'<rect x="1360" y="400" width="14" height="300" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1367,400 l{90:.0f},{26:.0f} l{-90:.0f},{26:.0f} Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    # ДЕД с рукавицей над головой
    dx, dy, dh = 880, 1040, 700
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#4a4038", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, 1, dh * .34, -56, t, "#4a4038", "#ffd9a8", .2, 3)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, -1, dh * .28, 44, t, "#4a4038", "#ffd9a8", .7, 3)
    s += SL(Z_SRED, r1 + varezhka(e1x + 4, e1y - 14, 1.2, 6, "#6b4428", t, .1) + r2)
    s += SL(Z_SRED, f'<path d="M{e2x:.0f},{e2y:.0f} l{20:.0f},{dy-e2y-10:.0f}"'
                    f' stroke="#7d5636" stroke-width="12" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(dx - 36, dy - dh * .80, t, .3, 1.1, .55))
    s += SL(Z_SRED, ten(dx, dy + 6, 134, 23, .45))
    # МОРОЗ выглядывает из-за леса и потирает руки
    vygl = A.ease(A.seg(t, .8, 1.6))
    s += SL(Z_SRED, f'<g transform="translate(0,{200-140*vygl:.0f})">'
            + moroz_ded(1760, 640, t, .9, .2) + '</g>')
    # колодец, сани, воробьи
    s += SL(Z_SRED, f'<rect x="300" y="880" width="220" height="110" rx="8"'
                    f' fill="{KAMEN}" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="410" cy="880" rx="110" ry="24" fill="{KAMEN2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M330,880 l-8,-140 h176 l-8,140" fill="none"'
                    f' stroke="#6b4428" stroke-width="12"/>'
                    f'<path d="M322,740 h190" stroke="#54351f" stroke-width="13"/>')
    s += SL(Z_SRED, sani_s_rogozhey(620, 1040, .8, t, .4, True))
    for i, (vx_, vy_) in enumerate(((1200, 900), (1280, 930), (1360, 890))):
        s += SL(Z_SRED, ptica(vx_, vy_, t, 1.4, "#8a7a62", i * .4, "#6f6256"))
    s += SL(Z_SRED, inej_mel(443, 48, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def alaya_zarya_za_oknom(t):
    """Окно избы на пол-кадра: за стеклом настоящая алая заря. Хозяйка
    отодвигает занавеску, снимает с гвоздя зонт и ставит рядом валенки с
    галошами; на подоконнике горшок с луком и чашка."""
    rnd = random.Random(3020)
    s = stena_gornicy_19(t, 53, 860, True, True)
    # ОКНО-ПРОЁМ по центру
    px, py, pw, ph_ = 520, 200, 780, 320
    okno = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
            f' fill="#c8604a"/>')
    okno += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.45:.0f}"'
             f' fill="#e08a5a"/>')
    okno += mesto_stoka(px, py, pw, ph_, "pryam")
    okno += (f'<rect x="{px-18:.0f}" y="{py-18:.0f}" width="{pw+36:.0f}"'
             f' height="{ph_+36:.0f}" rx="6" fill="none" stroke="#6b4428"'
             f' stroke-width="26"/>')
    okno += (f'<path d="M{px+pw*.5:.0f},{py:.0f} v{ph_:.0f} M{px:.0f},{py+ph_*.5:.0f}'
             f' h{pw:.0f}" stroke="#6b4428" stroke-width="16"/>')
    okno += (f'<rect x="{px-50:.0f}" y="{py+ph_+18:.0f}" width="{pw+100:.0f}"'
             f' height="32" rx="6" fill="{DOSKA}" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, okno)
    s += SL(Z_SRED, teplo(px + pw * .5, py + ph_ * .5, 520, 420, .35))
    # ЗАНАВЕСКА отодвигается
    otod = A.ease(A.seg(t, .5, 1.2))
    for i in (0, 1):
        sdv = (-1 if i == 0 else 1) * 120 * otod
        s += SL(Z_SRED, f'<path d="M{px+i*(pw-180)+sdv:.0f},{py-20:.0f}'
                        f' q{80:.0f},{40:.0f} {70:.0f},{ph_*.9:.0f} q{-50:.0f},{26:.0f}'
                        f' {-120:.0f},{10:.0f} Z" fill="{RUSH}" opacity=".95"'
                        f' stroke="{K}" stroke-width="4.5"/>')
    # ГОРШОК С ЛУКОМ и чашка на подоконнике
    s += SL(Z_SRED, f'<path d="M560,{py+ph_+18:.0f} h120 l-14,-80 h-92 Z"'
                    f' fill="#a8743c" stroke="{K}" stroke-width="4.5"/>')
    for i in range(5):
        a = -1.1 + i * .55
        s += SL(Z_SRED, f'<path d="M620,{py+ph_-62:.0f} q{40*math.sin(a):.0f},{-60:.0f}'
                        f' {64*math.sin(a):.0f},{-130:.0f} q{16:.0f},{34:.0f}'
                        f' {-30*math.sin(a):.0f},{130:.0f} Z" fill="#6f8c4a"'
                        f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, kruzhka_moloka(1240, py + ph_ + 18, .8, t, False, .3, "#d8cbb0"))
    # ХОЗЯЙКА снимает зонт с гвоздя
    hx, hy, hh = 1560, 1050, 700
    snyat = A.ease(A.seg(t, 1.2, 1.4))
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a3a52", kant="#ffd98a",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .34, -40 + 16 * snyat, t,
                              "#4a3a52", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .30, -24, t, "#4a3a52", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    zx_, zy_ = e1x + 10, e1y + 40 * snyat
    s += SL(Z_SRED, f'<path d="M{zx_-14:.0f},{zy_:.0f} l{12:.0f},{220:.0f}"'
                    f' stroke="#3f3a33" stroke-width="10"/>'
                    f'<path d="M{zx_-90:.0f},{zy_:.0f} q{90:.0f},{-80:.0f} {180:.0f},0 Z"'
                    f' fill="#3f5a6a" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{zx_:.0f},{zy_+220:.0f} q{26:.0f},{16:.0f} {30:.0f},{-14:.0f}"'
                    f' fill="none" stroke="#3f3a33" stroke-width="8"/>')
    s += SL(Z_SRED, f'<rect x="{zx_-30:.0f}" y="{zy_-60:.0f}" width="16" height="30"'
                    f' rx="4" fill="{ZHELEZ}" stroke="{K}" stroke-width="3"/>')
    # ВАЛЕНКИ с галошами у двери
    s += SL(Z_SRED, _valenok(1180, 1050, 1.2, -4) + _valenok(1290, 1056, 1.2, 5)
            + f'<ellipse cx="1180" cy="1056" rx="40" ry="14" fill="#23242a"'
              f' stroke="{K}" stroke-width="3.4"/>'
              f'<ellipse cx="1290" cy="1062" rx="40" ry="14" fill="#23242a"'
              f' stroke="{K}" stroke-width="3.4"/>')
    # лавка, ходики, кот, печь
    s += SL(Z_SRED, lavka(220, 940, 420))
    s += SL(Z_SRED, hodiki(220, 300, t, 1.4))
    s += SL(Z_SRED, kot(420, 940, t, 1.5, "#3b3430", True))
    s += SL(Z_SRED, pech(1680, 320, 260, 420, t, True, True, False))
    s += SL(Z_SRED, ogon(1760, 640, t, .9, .3, 5) + teplo(1760, 620, 260, 210, .42))
    s += SL(Z_SRED, polka_s_bankami(140, 500, 400, t, 113, 4, False))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def nahohlennye_pticy_na_vetke(t):
    """Ветка рябины за окном, а чердачное окошко дома рядом — круглый проём с
    настоящими нахохленными воробьями. На рисованной ветке сидят пять
    воробьёв-шариков; мальчик прижался к стеклу, бабушка несёт вторую шаль."""
    rnd = random.Random(3021)
    s = stena_gornicy_19(t, 59, 880, True, True)
    # ОКНО комнаты
    s += SL(Z_SRED, f'<rect x="200" y="160" width="900" height="620" rx="8"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="7"/>'
                    f'<rect x="230" y="190" width="840" height="560" fill="#9fc4d8"'
                    f' opacity=".55"/>'
                    f'<path d="M650,160 v620 M200,470 h900" stroke="#e4d8bd"'
                    f' stroke-width="18"/>'
                    f'<rect x="170" y="780" width="960" height="34" rx="6"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="5"/>')
    # ВЕТКА РЯБИНЫ с пятью воробьями-шариками
    s += SL(Z_SRED, f'<path d="M230,330 q{220:.0f},{60:.0f} {460:.0f},{20:.0f}'
                    f' q{200:.0f},{-20:.0f} {380:.0f},{40:.0f}" fill="none"'
                    f' stroke="#5e4430" stroke-width="16"/>')
    for i in range(5):
        vx_ = 300 + i * 160
        vy_ = 330 + (20 if i % 2 else -10)
        puh = 1.0 + .05 * A.w(t, 2.4, i * .3)
        s += SL(Z_SRED, f'<ellipse cx="{vx_:.0f}" cy="{vy_-34:.0f}" rx="{44*puh:.0f}"'
                        f' ry="{40*puh:.0f}" fill="#8a7a62" stroke="{K}"'
                        f' stroke-width="4"/>'
                        f'<circle cx="{vx_+26:.0f}" cy="{vy_-54:.0f}" r="{20*puh:.0f}"'
                        f' fill="#9a8a6a" stroke="{K}" stroke-width="3.4"/>'
                        f'<path d="M{vx_+44:.0f},{vy_-56:.0f} l20,5 l-20,6 Z"'
                        f' fill="#5f5a4e"/>'
                        f'<circle cx="{vx_+32:.0f}" cy="{vy_-60:.0f}" r="4" fill="{K}"/>'
                        f'<path d="M{vx_-40:.0f},{vy_-20:.0f} l{-26:.0f},{16:.0f}'
                        f' l{26:.0f},{6:.0f} Z" fill="#6f6256" stroke="{K}"'
                        f' stroke-width="2.6"/>')
    for i in range(4):
        s += SL(Z_SRED, kalina_grozd(360 + i * 190, 380, t, .9, 10, 59 + i, i * .25, True))
    # ЧЕРДАЧНОЕ ОКОШКО — круглый проём
    ox, oy, od = 1360, 200, 400
    put = kontur_proema(ox, oy, od, od, "ellips")
    cher = (f'<path d="{put}" fill="#8aa8b4"/>')
    cher += (f'<path d="{put}" fill="#cfe4f5" opacity=".35"/>')
    cher += mesto_stoka(ox, oy, od, od, "ellips")
    cher += (f'<circle cx="{ox+od*.5:.0f}" cy="{oy+od*.5:.0f}" r="{od*.5:.0f}"'
             f' fill="none" stroke="#6b4428" stroke-width="24"/>')
    for i in range(4):
        a = i * 1.57 + .78
        cher += (f'<path d="M{ox+od*.5:.0f},{oy+od*.5:.0f}'
                 f' l{od*.5*math.cos(a):.0f},{od*.5*math.sin(a):.0f}" stroke="#6b4428"'
                 f' stroke-width="10"/>')
    s += SL(Z_SRED, cher)
    s += SL(Z_SRED, f'<rect x="{ox-60:.0f}" y="{oy+od+20:.0f}" width="{od+120:.0f}"'
                    f' height="28" rx="6" fill="{DOSKA2}" stroke="{K}" stroke-width="5"/>')
    # МАЛЬЧИК на табурете у окна
    mx, my, mh = 760, 980, 480
    s += SL(Z_SRED, f'<rect x="{mx-80:.0f}" y="{my:.0f}" width="160" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{mx-60:.0f}" y="{my+26:.0f}" width="18" height="80"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>'
                    f'<rect x="{mx+42:.0f}" y="{my+26:.0f}" width="18" height="80"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>')
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f5a6a", kant="#ffd98a", ph=.3))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -40, t, "#3f5a6a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .30, -36, t, "#3f5a6a", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    # БАБУШКА со второй шалью
    bx, by, bh = 1680, 1056, 660
    idt = A.ease(A.seg(t, 1.0, 1.6))
    s += SL(Z_SRED, f'<g opacity=".95">'
            + figura(bx - 140 * idt, by, bh, t, col="#4a3a52", kant="#ffd98a",
                     platok=True, ph=.7) + '</g>')
    r3, (e3x, e3y), _ = _ruka(bx - 140 * idt, by, bh, -1, bh * .28, -14, t,
                              "#4a3a52", "#ffd98a", .4, 4)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x-70:.0f},{e3y:.0f} q{70:.0f},{-30:.0f}'
                         f' {140:.0f},0 l{10:.0f},{120:.0f} q{-80:.0f},{26:.0f}'
                         f' {-160:.0f},0 Z" fill="#8a2f8a" stroke="{K}"'
                         f' stroke-width="4.5"/>')
    # кактус, кот на подоконнике, занавеска
    s += SL(Z_SRED, f'<path d="M300,812 h110 l-12,-70 h-86 Z" fill="#a8743c"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M332,742 q{24:.0f},{-90:.0f} {46:.0f},{-4:.0f}'
                    f' q{-6:.0f},{80:.0f} {-46:.0f},{4:.0f} Z" fill="#4a6a3a"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(1700, 420, t, 1.3, True) + teplo(1700, 440, 280, 230, .42))
    s += SL(Z_SRED, kot(1060, 812, t, 1.5, "#3b3430", False))
    kch = 5 * A.w(t, 2.6, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} 1180 160)">'
                    f'<path d="M1120,160 q{70:.0f},{40:.0f} {140:.0f},0 l0,{380:.0f}'
                    f' q{-70:.0f},{34:.0f} {-140:.0f},0 Z" fill="{RUSH}" opacity=".9"'
                    f' stroke="{K}" stroke-width="4.5"/></g>')
    s += SL(Z_SRED, ten(bx - 140 * idt, by + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def drova_progoreli_do_zoly(t):
    """Устье печи: охапка поленьев вспыхивает и на глазах оседает в кучку
    серой золы, а рисованные песочные часы над устьем пересыпаются слишком
    быстро. Дед с кочергой чешет затылок и идёт за второй охапкой."""
    rnd = random.Random(3022)
    s = (f'<rect width="{W}" height="{H}" fill="#241c16"/>')
    s += SL(Z_DAL, brevna(0, 0, W, 900, 86, 3))
    s += SL(Z_SRED, polovicy(900, "#6b4428"))
    # ПЕЧЬ с устьем на пол-кадра
    s += SL(Z_SRED, pech(240, 120, 1000, 780, t, True, True, False))
    ux, uy, uw, uh = 520, 480, 460, 330
    put = kontur_proema(ux, uy, uw, uh, "ustie")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a0d06" stroke="{K}" stroke-width="7"/>')
    # ПОЛЕНЬЯ оседают в золу
    osad = A.ease(A.seg(t, .4, 2.2))
    for i in range(6):
        px_ = ux + 80 + i * 56
        py_ = uy + 250 - 30 * (1 - osad) * ((i % 3) + 1)
        s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="{py_:.0f}" width="{44*(1-osad*.6):.0f}"'
                        f' height="{90*(1-osad*.75):.0f}" rx="10" fill="#7d5636"'
                        f' opacity="{1-osad*.7:.2f}" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, ogon(ux + uw * .5, uy + 230, t, 1.5 * (1 - osad * .55), .1, 7))
    s += SL(Z_SRED, ugli(ux + 70, uy + 280, uw - 140, t, 8, 2))
    s += SL(Z_SRED, f'<ellipse cx="{ux+uw*.5:.0f}" cy="{uy+292:.0f}"'
                    f' rx="{160*osad:.0f}" ry="{30*osad:.0f}" fill="#9aa3a8"'
                    f' opacity="{.85*osad:.2f}"/>')
    s += SL(Z_SRED, teplo(ux + uw * .5, uy + 220, 520, 420, .55))
    s += SL(Z_SRED, iskra_let(t, ux + uw * .5, uy + 200, 8, 4, 300, .5))
    # ПЕСОЧНЫЕ ЧАСЫ над устьем
    pes = ((t * .9) % 1.0)
    s += SL(Z_SRED, f'<path d="M{ux+uw*.5-70:.0f},{uy-230:.0f} h140 l-60,{100:.0f}'
                    f' l60,{100:.0f} h-140 l60,{-100:.0f} Z" fill="#dce7f2"'
                    f' opacity=".5" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{ux+uw*.5-54:.0f},{uy-222:.0f} h108 l-54,{90:.0f} Z"'
                    f' fill="#d6a63f" opacity="{1-pes:.2f}"/>'
                    f'<path d="M{ux+uw*.5-54:.0f},{uy-32:.0f} h108 l-54,{-90:.0f} Z"'
                    f' fill="#d6a63f" opacity="{pes:.2f}"/>'
                    f'<path d="M{ux+uw*.5:.0f},{uy-132:.0f} l0,{60:.0f}"'
                    f' stroke="#d6a63f" stroke-width="5"/>')
    # ДЕД на скамеечке с кочергой
    dx, dy, dh = 1420, 1050, 560
    vst = A.ease(A.seg(t, 1.8, 1.0))
    s += SL(Z_SRED, f'<rect x="{dx-90:.0f}" y="{dy-20:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(dx, dy - 10 - 40 * vst, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, shapka=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(dx, dy - 10 - 40 * vst, dh, -1, dh * .34, -4, t,
                              "#4a4038", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy - 10 - 40 * vst, dh, 1, dh * .30, -44, t,
                              "#4a4038", "#ffd98a", .7, 5)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{-240:.0f},{80:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="9"/>'
                    f'<path d="M{e1x-240:.0f},{e1y+80:.0f} l{-40:.0f},{-26:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="9"/>')
    # заслонка, ухват, чугунок, кот, вязанка дров
    s += SL(Z_SRED, f'<rect x="1020" y="520" width="160" height="240" rx="8"'
                    f' fill="{CHUGUN}" stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="1100" cy="640" r="20" fill="#5d6168" stroke="{K}"'
                    f' stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M180,1060 l{26:.0f},{-420:.0f}" stroke="#8a6342"'
                    f' stroke-width="12"/>'
                    f'<path d="M194,650 q{-36:.0f},{-46:.0f} {8:.0f},{-74:.0f}'
                    f' M232,644 q{36:.0f},{-46:.0f} {-6:.0f},{-76:.0f}" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="10"/>')
    s += SL(Z_SRED, f'<path d="M340,1040 q{-18:.0f},{-66:.0f} {52:.0f},{-70:.0f}'
                    f' q{70:.0f},{4:.0f} {52:.0f},{70:.0f} Z" fill="{CHUGUN}"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, kot(1700 + 60 * vst, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, f'<g transform="rotate(-10 1840 940)">')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{1790+i*9:.0f}" y="{780:.0f}" width="26" height="170"'
                        f' rx="8" fill="#7d5636" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<path d="M1788,860 h110" stroke="#b9a37a" stroke-width="9"/></g>')
    s += SL(Z_SRED, ten(dx, dy + 20, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.46)
    return s


def pticy_na_dereve_u_doma(t):
    """Городской двор утром: берёза у подъезда и забор детской площадки. На
    ветках сидят рисованные синицы — одни распушились шариками, другие
    прыгают. На перилах балкона встают две карточки-подсказки."""
    rnd = random.Random(3023)
    s = nebo("rassv", t, False, 449)
    s += oblaka(t, 150, 5, 229, .36, "#ffe9c8")
    s += SL(Z_DAL, panelka(1180, 760, 740, t, 5, True, 71))
    # БЕРЁЗА у подъезда
    bx, bb = 700, 1000
    s += SL(Z_SRED, f'<path d="M{bx-26:.0f},{bb:.0f} q{6:.0f},{-400:.0f} {16:.0f},{-820:.0f}'
                    f' l{32:.0f},0 q{12:.0f},{420:.0f} {18:.0f},{820:.0f} Z"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>')
    for i in range(16):
        yy = bb - 60 - i * 50
        s += SL(Z_SRED, f'<path d="M{bx-22+((i*7)%10):.0f},{yy:.0f} h{16+((i*5)%14):.0f}"'
                        f' stroke="#3f3a33" stroke-width="{4+((i*3)%3):.0f}"'
                        f' opacity=".85"/>')
    for i in range(8):
        p = .32 + .66 * i / 7.0
        sgn = 1 if i % 2 else -1
        y0 = bb - 820 * p
        dl = 320 * (1.1 - p)
        s += SL(Z_SRED, f'<path d="M{bx:.0f},{y0:.0f} q{sgn*dl*.5:.0f},{-dl*.2:.0f}'
                        f' {sgn*dl:.0f},{-dl*.1:.0f}" fill="none" stroke="#c9bfa6"'
                        f' stroke-width="{max(3, 11-i):.0f}"/>')
    # СИНИЦЫ: часть шариками, часть прыгают
    for i in range(7):
        sgn = 1 if i % 2 else -1
        vx_ = bx + sgn * (120 + (i % 4) * 90)
        vy_ = bb - 300 - i * 70
        if i % 3 == 0:
            puh = 1.0 + .06 * A.w(t, 2.2, i * .3)
            s += SL(Z_SRED, f'<ellipse cx="{vx_:.0f}" cy="{vy_:.0f}" rx="{36*puh:.0f}"'
                            f' ry="{34*puh:.0f}" fill="#d6a63f" stroke="{K}"'
                            f' stroke-width="4"/>'
                            f'<circle cx="{vx_+20:.0f}" cy="{vy_-20:.0f}" r="16"'
                            f' fill="#4a5664" stroke="{K}" stroke-width="3.2"/>'
                            f'<path d="M{vx_+34:.0f},{vy_-22:.0f} l16,4 l-16,5 Z"'
                            f' fill="#5f5a4e"/>')
        else:
            pr = 16 * abs(A.w(t, 1.2, i * .25))
            s += SL(Z_SRED, f'<g transform="translate(0,{-pr:.0f})">'
                    + ptica(vx_, vy_, t, 1.5, "#d6a63f", i * .2, "#4a6a78") + '</g>')
    # БАЛКОН с женщиной и карточками-подсказками
    s += SL(Z_SRED, f'<rect x="1240" y="520" width="520" height="34" rx="6"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1240" y="554" width="520" height="190" rx="6"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="5"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="{1260+i*56:.0f}" y="560" width="12" height="180"'
                        f' fill="#9aa3a8"/>')
    zx, zy, zh = 1480, 520, 520
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#8a2f8a", kant="#ffd98a", ph=.3))
    r1, (e1x, e1y), _ = _ruka(zx, zy, zh, 1, zh * .26, 40, t, "#8a2f8a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(zx, zy, zh, -1, zh * .24, 44, t, "#8a2f8a", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2 + kruzhka_moloka(e1x + 10, e1y + 50, .8, t, False, .2))
    s += SL(Z_SRED, par(e1x + 10, e1y + 10, t, 3, .45, 130, .4, .8))
    for i, (kx_, ky_) in enumerate(((1300, 420), (1620, 430))):
        vst = A.out(A.seg(t, .8 + i * .6, .6))
        if vst < .02:
            continue
        s += SL(Z_SRED, f'<g opacity="{vst:.2f}">'
                        f'<rect x="{kx_-80:.0f}" y="{ky_-70:.0f}" width="160"'
                        f' height="140" rx="12" fill="#f2ead6" stroke="{K}"'
                        f' stroke-width="5"/>')
        if i == 0:
            s += SL(Z_SRED, f'<circle cx="{kx_:.0f}" cy="{ky_+6:.0f}" r="40"'
                            f' fill="#d6a63f" stroke="{K}" stroke-width="3.6"/>'
                            f'<path d="M{kx_-40:.0f},{ky_-40:.0f} h{80:.0f}'
                            f' M{kx_:.0f},{ky_-60:.0f} v{40:.0f}" stroke="#4a6a78"'
                            f' stroke-width="5"/>')
        else:
            s += SL(Z_SRED, ptica(kx_, ky_ + 20, t, 1.3, "#d6a63f", .3, "#4a6a78")
                    + f'<circle cx="{kx_+46:.0f}" cy="{ky_-40:.0f}" r="20"'
                      f' fill="#ffe9ac" opacity=".9"/>')
        s += SL(Z_SRED, '</g>')
    # бельевая верёвка, лыжи, ящик для цветов, кот
    s += SL(Z_SRED, f'<path d="M1260,600 h480" stroke="#b9a37a" stroke-width="4"/>')
    for i, (px_, pw_, col) in enumerate(((1300, 70, "#e8e2d6"), (1420, 60, "#8aa8b4"))):
        kch = 5 * A.w(t, 2.4, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {px_+pw_*.5:.0f} 612)">'
                        f'<rect x="{px_:.0f}" y="612" width="{pw_:.0f}" height="110"'
                        f' rx="5" fill="{col}" stroke="{K}" stroke-width="3.4"/></g>')
    s += SL(Z_SRED, f'<path d="M1700,560 l{10:.0f},{-180:.0f} M1740,560 l{10:.0f},{-180:.0f}"'
                    f' stroke="#8a2f22" stroke-width="12"/>')
    s += SL(Z_SRED, f'<rect x="1260" y="690" width="160" height="56" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, kot(1660, 744, t, 1.3, "#3b3430", False))
    # двор: забор площадки, скамейка, сугробы
    s += SL(Z_SRED, _merzlaya_zemlya(940, 449, False))
    s += SL(Z_SRED, sneg_lezhit(960, 28, "url(#sneg)"))
    s += SL(Z_SRED, zabor_shtaket(-40, 860, 620, 180, 449, 58))
    s += SL(Z_SRED, f'<rect x="120" y="980" width="280" height="20" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="140" y="1000" width="20" height="70" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="360" y="1000" width="20" height="70" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    # ДВОР ОБЖИТ: второй дом, качели, песочница, фонарь, кусты, сугробы
    s += SL(Z_DAL, panelka(40, 720, 560, t, 5, True, 73))
    s += SL(Z_SRED, f'<rect x="300" y="620" width="22" height="420" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(311, 620, t, 1.1, True) + teplo(311, 640, 220, 180, .34))
    s += SL(Z_SRED, f'<rect x="900" y="700" width="20" height="300" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1120" y="700" width="20" height="300" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="880" y="690" width="280" height="20" rx="5"'
                    f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4"/>')
    kach = 7 * A.w(t, 2.6, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 1020 700)">'
                    f'<path d="M960,710 l{10:.0f},{170:.0f} M1080,710 l{-10:.0f},{170:.0f}"'
                    f' stroke="#b9a37a" stroke-width="5"/>'
                    f'<rect x="950" y="878" width="140" height="22" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<rect x="420" y="880" width="300" height="120" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="440" y="860" width="260" height="26" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="570" cy="912" rx="120" ry="30" fill="url(#sneg)"'
                    f' opacity=".9"/>')
    for i, (kx2, kb2, kh2) in enumerate(((240, 1000, 220), (1180, 1010, 200),
                                         (1400, 990, 240))):
        s += SL(Z_SRED, goloe_derevo_ld(kx2, kb2, kh2, t, 457 + i, 5, True))
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{160+i*260:.0f}" cy="{1020+((i*5)%3)*16:.0f}"'
                        f' rx="{90+((i*7)%4)*26:.0f}" ry="{26+((i*3)%2)*10:.0f}"'
                        f' fill="url(#sneg)" opacity=".92"/>')
    s += SL(Z_SRED, inej_mel(449, 44, 980, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def shkolnaya_parta_s_uchebnikom(t):
    """Школьная парта с раскрытым учебником: на правой странице в овальном
    медальоне — настоящий портрет Ломоносова, гравюра XVIII века. Рядом
    чернильница, ручка, мел; за партой сидит ученик."""
    rnd = random.Random(3024)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="560" fill="#d8cbb0"/>'
                   f'<rect x="0" y="560" width="{W}" height="56" fill="#8a7a52"'
                   f' opacity=".85"/>')
    s += SL(Z_DAL, klassnaya_doska(120, 90, 700, 380, t, 11))
    s += SL(Z_DAL, okno_izby(1500, 110, 380, 380, t, None, .3, False, True))
    s += SL(Z_DAL, f'<rect x="1020" y="200" width="200" height="260" rx="8"'
                   f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                   f'<circle cx="1120" cy="300" r="76" fill="#3f6b7a" stroke="{K}"'
                   f' stroke-width="5"/>'
                   f'<path d="M1046,286 q{74:.0f},{44:.0f} {148:.0f},0" fill="none"'
                   f' stroke="#56763f" stroke-width="8"/>')
    s += SL(Z_SRED, polovicy(700, "#8a6342"))
    # ПАРТА и УЧЕБНИК
    s += SL(Z_SRED, parta_shkolnaya(260, 1010, 1300, t, 13, True))
    ux, uy, uw, uh = 420, 620, 1000, 420
    s += SL(Z_SRED, uchebnik_razvorot(ux, uy, uw, uh, t, True, .2))
    # ОВАЛЬНЫЙ МЕДАЛЬОН на правой странице — проём с портретом
    ox, oy, ow, oh2 = ux + uw * .54, uy + 36, 420, 330
    put = kontur_proema(ox, oy, ow, oh2, "ellips")
    med = (f'<path d="{put}" fill="#e4d8bd"/>')
    med += (f'<path d="{put}" fill="#d8cbb0" opacity=".5"/>')
    med += mesto_stoka(ox, oy, ow, oh2, "ellips")
    med += (f'<ellipse cx="{ox+ow*.5:.0f}" cy="{oy+oh2*.5:.0f}" rx="{ow*.5:.0f}"'
            f' ry="{oh2*.5:.0f}" fill="none" stroke="#8a6342" stroke-width="18"/>')
    med += (f'<ellipse cx="{ox+ow*.5:.0f}" cy="{oy+oh2*.5:.0f}" rx="{ow*.5+14:.0f}"'
            f' ry="{oh2*.5+14:.0f}" fill="none" stroke="#c9a05a" stroke-width="6"'
            f' opacity=".9"/>')
    s += SL(Z_SRED, med)
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{ox-10:.0f},{oy+oh2+30+i*26:.0f} q{90:.0f},{-6:.0f}'
                        f' {180:.0f},0 q{70:.0f},{6:.0f} {120:.0f},{-2:.0f}" fill="none"'
                        f' stroke="#6f6354" stroke-width="3.4" opacity=".75"/>')
    # УЧЕНИК за партой
    px_, py_, ph_ = 1600, 1066, 560
    s += SL(Z_SRED, figura(px_, py_, ph_, t, col="#3f3a4a", kant="#ffd98a", ph=.3))
    r1, (e1x, e1y), _ = _ruka(px_, py_, ph_, -1, ph_ * .30, 10, t, "#3f3a4a", "#ffd98a", .2, 4)
    s += SL(Z_SRED, r1)
    # мел, чернильница, ручка уже в parta_shkolnaya; добавим стопку тетрадей
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1380+i*6:.0f}" y="{620-i*16:.0f}" width="150"'
                        f' height="18" rx="4" fill="#f2ead6" stroke="{K}"'
                        f' stroke-width="3.2"/>')
    s += SL(Z_SRED, lampa(960, 60, t, 1.3, True) + teplo(960, 80, 300, 250, .40))
    s += SL(Z_SRED, ten(px_, py_ + 6, 120, 20, .4))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def pomorskaya_derevnya_u_morya(t):
    """Северный берег: серое море, дома на высоких подклетах, карбас на
    берегу, сети на шестах. Распахнутые ворота лодочного сарая — проём с
    настоящим северным морем. Помор поднимает свёрток с младенцем к небу."""
    rnd = random.Random(3025)
    s = nebo("sumer", t, False, 457)
    s += oblaka(t, 140, 6, 233, .44)
    s += SL(Z_DAL, f'<rect x="0" y="420" width="{W}" height="240" fill="#4a5664"/>')
    for i in range(12):
        yy = 440 + i * 18
        s += SL(Z_DAL, f'<path d="M{rnd.uniform(-60,200):.0f},{yy:.0f}'
                       f' q{rnd.uniform(300,700):.0f},{rnd.uniform(-8,8):.0f}'
                       f' {rnd.uniform(1200,1960):.0f},{rnd.uniform(-6,6):.0f}"'
                       f' fill="none" stroke="#5e6a78" stroke-width="{rnd.uniform(2,5):.1f}"'
                       f' opacity=".6"/>')
    # ДОМА на высоких подклетах
    for i, (ix, iw) in enumerate(((60, 320), (1480, 360))):
        s += SL(Z_SRED, f'<rect x="{ix:.0f}" y="{600-i*20:.0f}" width="{iw:.0f}"'
                        f' height="200" fill="#5e4430" stroke="{K}" stroke-width="6"/>')
        s += SL(Z_SRED, brevna(ix, 600 - i * 20, iw, 200, 54, i))
        s += SL(Z_SRED, f'<path d="M{ix-40:.0f},{600-i*20:.0f} l{iw*.5+40:.0f},{-130:.0f}'
                        f' l{iw*.5+40:.0f},{130:.0f} Z" fill="#4a3526" stroke="{K}"'
                        f' stroke-width="5.5"/>'
                        f'<path d="M{ix-40:.0f},{600-i*20:.0f} l{iw*.5+40:.0f},{-130:.0f}'
                        f' l{iw*.5+40:.0f},{130:.0f}" fill="none" stroke="url(#sneg)"'
                        f' stroke-width="16" opacity=".9"/>')
        for k in range(4):
            s += SL(Z_SRED, f'<rect x="{ix+30+k*(iw-80)/3:.0f}" y="800" width="26"'
                            f' height="200" fill="#54351f" stroke="{K}"'
                            f' stroke-width="4"/>')
        s += SL(Z_SRED, f'<rect x="{ix+iw*.3:.0f}" y="{650-i*20:.0f}" width="90"'
                        f' height="80" rx="5" fill="#ffd98a"'
                        f' opacity="{.7+.2*A.w(t,4.0,i*.4):.2f}" stroke="{K}"'
                        f' stroke-width="4"/>')
        s += SL(Z_SRED, dym_stolbom(ix + iw * .18, 460 - i * 20, t, 300, .45, .4, 6))
    # ЛОДОЧНЫЙ САРАЙ с проёмом
    sx, sy, sw, sh_ = 920, 480, 820, 420
    s += SL(Z_SRED, f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="{sh_:.0f}"'
                    f' fill="#5e4430" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M{sx-50:.0f},{sy:.0f} l{sw*.5+50:.0f},{-150:.0f}'
                    f' l{sw*.5+50:.0f},{150:.0f} Z" fill="#4a3526" stroke="{K}"'
                    f' stroke-width="5.5"/>')
    px, py, pw, ph_ = sx + 20, sy + 60, 780, 320
    pr = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
          f' fill="#6f7a84"/>')
    pr += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.4:.0f}"'
           f' fill="#8a98a8"/>')
    pr += mesto_stoka(px, py, pw, ph_, "pryam")
    pr += (f'<rect x="{px-14:.0f}" y="{py-14:.0f}" width="{pw+28:.0f}"'
           f' height="{ph_+28:.0f}" fill="none" stroke="#3f2d1c" stroke-width="22"/>')
    s += SL(Z_SRED, pr)
    for i in (-1, 1):
        s += SL(Z_SRED, f'<g transform="rotate({i*22} {px + (0 if i<0 else pw):.0f}'
                        f' {py:.0f})">'
                        f'<rect x="{px + (0 if i<0 else pw) - (70 if i>0 else 0):.0f}"'
                        f' y="{py-10:.0f}" width="70" height="{ph_+30:.0f}"'
                        f' fill="url(#derev)" stroke="{K}" stroke-width="5"/></g>')
    # БЕРЕГ, карбас, сети на шестах, бочки, якорь
    s += SL(Z_SRED, f'<path d="M-40,1080 Q500,900 1080,870 L1920,850 L1920,1080 Z"'
                    f' fill="#6f6256" stroke="{K}" stroke-width="5"/>')
    for i in range(24):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(890,1070):.0f}" rx="{rnd.uniform(14,46):.0f}"'
                        f' ry="{rnd.uniform(6,16):.0f}" fill="#8a8078" opacity=".7"/>')
    s += SL(Z_SRED, karbas_pod_parusom(420, 960, 420, t, .2))
    for i, nx_ in enumerate((200, 420, 640)):
        s += SL(Z_SRED, f'<rect x="{nx_:.0f}" y="640" width="14" height="300"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="3.4"/>')
        kch = 6 * A.w(t, 3.0, i * .4)
        for k in range(6):
            s += SL(Z_SRED, f'<path d="M{nx_+7:.0f},{680+k*40:.0f}'
                            f' q{100+kch:.0f},{20:.0f} {210:.0f},{-6:.0f}" fill="none"'
                            f' stroke="#b9a37a" stroke-width="2.6" opacity=".85"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{1500+i*110:.0f},1050 q{-14:.0f},{-80:.0f}'
                        f' {40:.0f},{-86:.0f} q{54:.0f},{6:.0f} {40:.0f},{86:.0f} Z"'
                        f' fill="url(#derev)" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<path d="M1300,1000 l0,-120 M1240,900 h120 M1300,1000'
                    f' q{-60:.0f},{-10:.0f} {-70:.0f},{-60:.0f} M1300,1000'
                    f' q{60:.0f},{-10:.0f} {70:.0f},{-60:.0f}" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="12"/>')
    # ПОМОР поднимает свёрток, ЖЕНА на крыльце
    pod = A.ease(A.seg(t, .6, 1.6))
    hx, hy, hh = 940, 1050, 720
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a56", kant="#cfe4f5",
                           boroda=True, shapka=True, tulup=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .30, -30 - 24 * pod, t,
                              "#3f4a56", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .30, -28 - 22 * pod, t,
                              "#3f4a56", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<ellipse cx="{(e1x+e2x)*.5:.0f}" cy="{e1y-20:.0f}" rx="86"'
                    f' ry="44" fill="{RUSH}" stroke="{K}" stroke-width="5"'
                    f' transform="rotate(-14 {(e1x+e2x)*.5:.0f} {e1y-20:.0f})"/>'
                    f'<circle cx="{(e1x+e2x)*.5+60:.0f}" cy="{e1y-34:.0f}" r="26"'
                    f' fill="#f0cfae" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, para_izo_rta(hx - 36, hy - hh * .80, t, .3, 1.1, .5))
    zx, zy, zh = 1660, 800, 560
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, ph=.7))
    r3, (e3x, e3y), _ = _ruka(zx, zy, zh, -1, zh * .26, 50, t, "#4a3a52", "#cfe4f5", .4, 4)
    s += SL(Z_SRED, r3)
    for i in range(5):
        a = (t * .22 + i * .2) % 1.0
        s += SL(Z_LETIT, f'<path d="M{200+1400*a:.0f},{260+70*math.sin(a*6+i):.0f}'
                         f' q{16:.0f},{-14:.0f} {32:.0f},0 q{16:.0f},{-14:.0f} {32:.0f},0"'
                         f' fill="none" stroke="#f4f1e8" stroke-width="4" opacity=".9"/>')
    s += SL(Z_SRED, par(1400, 1000, t, 4, .5, 160, .45, 1.0))
    s += SL(Z_SRED, ten(hx, hy + 6, 140, 24, .45))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def malchik_s_knigoy_na_karbase(t):
    """Карбас под парусом в море, корма на пол-кадра: отец-помор у рулевого
    весла, мальчик в тулупчике сидит на бочонке с рыбой и читает толстую
    книгу, губы шевелятся; рядом в коробе ещё две книги."""
    rnd = random.Random(3026)
    s = nebo("rassv", t, False, 461)
    s += oblaka(t, 150, 5, 239, .40, "#ffe9c8")
    s += SL(Z_DAL, f'<rect x="0" y="480" width="{W}" height="600" fill="#4a6a78"/>')
    for i in range(16):
        yy = 500 + i * 36
        s += SL(Z_DAL, f'<path d="M{rnd.uniform(-60,200):.0f},{yy:.0f}'
                       f' q{rnd.uniform(200,500):.0f},{rnd.uniform(-16,16):.0f}'
                       f' {rnd.uniform(900,1960):.0f},{rnd.uniform(-10,10):.0f}"'
                       f' fill="none" stroke="#5f8a98" stroke-width="{rnd.uniform(3,8):.1f}"'
                       f' opacity=".6"/>')
    # берег вдали
    s += SL(Z_DAL, f'<path d="M0,470 q{300:.0f},{-40:.0f} {600:.0f},{-6:.0f}'
                   f' q{400:.0f},{30:.0f} {1320:.0f},{-10:.0f} l0,{40:.0f} l{-1920:.0f},0 Z"'
                   f' fill="#4a5664" opacity=".9"/>')
    # КАРБАС на пол-кадра
    s += SL(Z_SRED, karbas_pod_parusom(900, 820, 1180, t, .1))
    # ОТЕЦ у рулевого весла
    ox, oy, oh = 1420, 800, 600
    s += SL(Z_SRED, figura(ox, oy, oh, t, col="#3f4a56", kant="#cfe4f5",
                           boroda=True, shapka=True, tulup=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(ox, oy, oh, 1, oh * .30, 20, t, "#3f4a56", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ox, oy, oh, -1, oh * .26, 26, t, "#3f4a56", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{200:.0f},{180:.0f}"'
                    f' stroke="#7d5636" stroke-width="14" stroke-linecap="round"/>'
                    f'<path d="M{e1x+200:.0f},{e1y+180:.0f} l{60:.0f},{60:.0f}'
                    f' l{-30:.0f},{30:.0f} Z" fill="#6b4428" stroke="{K}"'
                    f' stroke-width="4"/>')
    bor = 10 * A.w(t, 1.8, .2)
    s += SL(Z_SRED, f'<path d="M{ox-20:.0f},{oy-oh*.80:.0f} q{-60-bor:.0f},{40:.0f}'
                    f' {-110-bor:.0f},{70:.0f}" fill="none" stroke="#ded3c4"'
                    f' stroke-width="18" stroke-linecap="round"/>')
    # МАЛЬЧИК на бочонке с книгой
    mx, my, mh = 760, 880, 440
    s += SL(Z_SRED, f'<path d="M{mx-70:.0f},{my:.0f} h140 l-10,-110 h-120 Z"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="{mx:.0f}" cy="{my-110:.0f}" rx="60" ry="18"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    for k in (.3, .7):
        s += SL(Z_SRED, f'<rect x="{mx-68:.0f}" y="{my-110+110*k:.0f}" width="136"'
                        f' height="10" fill="{ZHELEZ}" opacity=".9"/>')
    s += SL(Z_SRED, figura(mx, my - 110, mh, t, col="#8a7a62", kant="#cfe4f5",
                           ph=.5, naklon=2.0))
    r3, (e3x, e3y), _ = _ruka(mx, my - 110, mh, 1, mh * .30, 14, t,
                              "#8a7a62", "#cfe4f5", .3, 4)
    r4, (e4x, e4y), _ = _ruka(mx, my - 110, mh, -1, mh * .30, 18, t,
                              "#8a7a62", "#cfe4f5", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    kn_x, kn_y = (e3x + e4x) * .5 - 90, e3y - 20
    s += SL(Z_SRED, uchebnik_razvorot(kn_x, kn_y, 180, 130, t, False, .3))
    s += SL(Z_SRED, f'<path d="M{kn_x-14:.0f},{kn_y-10:.0f} q{100:.0f},{-26:.0f}'
                    f' {208:.0f},0 l0,{18:.0f} q{-104:.0f},{-20:.0f} {-208:.0f},0 Z"'
                    f' fill="#6b3a2a" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, para_izo_rta(mx - 24, my - 110 - mh * .78, t, .4, .8, .45))
    # КОРОБ с двумя книгами, сети, бочки
    s += SL(Z_SRED, f'<rect x="420" y="880" width="200" height="120" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="{440+i*18:.0f}" y="{850-i*20:.0f}" width="150"'
                        f' height="36" rx="5" fill="#6b3a2a" stroke="{K}"'
                        f' stroke-width="4"/>')
    for i, nx_ in enumerate((300, 560)):
        for k in range(5):
            s += SL(Z_SRED, f'<path d="M{nx_:.0f},{720+k*34:.0f} q{90:.0f},{24:.0f}'
                            f' {180:.0f},{-6:.0f}" fill="none" stroke="#b9a37a"'
                            f' stroke-width="2.6" opacity=".8"/>')
    # ЧАЙКА садится на борт
    sad = A.ease(A.seg(t, 1.2, 1.6))
    cx_, cy_ = 1180 - 180 * sad, 420 + 280 * sad
    s += SL(Z_SRED, f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="34" ry="20"'
                    f' fill="#f4f1e8" stroke="{K}" stroke-width="3.6"/>'
                    f'<circle cx="{cx_+26:.0f}" cy="{cy_-16:.0f}" r="14" fill="#f4f1e8"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{cx_+40:.0f},{cy_-18:.0f} l20,5 l-20,6 Z" fill="{ZOL}"/>'
                    f'<path d="M{cx_-10:.0f},{cy_-8:.0f} q{20:.0f},{-30*(1-sad)-10:.0f}'
                    f' {50:.0f},{-14:.0f}" fill="none" stroke="#dde3e8"'
                    f' stroke-width="11"/>')
    for i in range(4):
        a = (t * .25 + i * .25) % 1.0
        s += SL(Z_LETIT, f'<path d="M{300+1300*a:.0f},{220+60*math.sin(a*6+i):.0f}'
                         f' q{16:.0f},{-14:.0f} {32:.0f},0 q{16:.0f},{-14:.0f} {32:.0f},0"'
                         f' fill="none" stroke="#f4f1e8" stroke-width="4" opacity=".85"/>')
    s += SL(Z_SRED, par(1420, 760, t, 4, .5, 160, .45, 1.0))
    s += SL(Z_PERED, f'<path d="M-40,1080 q{300:.0f},{-120:.0f} {700:.0f},{-60:.0f}'
                     f' l0,200 l{-740:.0f},0 Z" fill="#2f4a52" opacity=".85"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def oboz_na_zimney_doroge(t):
    """Зимняя ночная дорога через лес под луной: впереди тянется обоз с
    мороженой рыбой, за последними санями идёт рослый парень с книгами у
    груди. В глубине дорога уходит в просвет между елями — настоящий кадр."""
    rnd = random.Random(3027)
    s = nebo("noch", t, True, 463)
    s += SL(Z_NEBO, luna_v_gorode(1560, 170, t, .9, True))
    # ПРОЁМ: дорога уходит в просвет между елями (по центру чуть выше середины)
    px, py, pw, ph_ = 560, 330, 800, 340
    pr = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
          f' fill="#2b3550"/>')
    pr += (f'<rect x="{px:.0f}" y="{py+ph_*.5:.0f}" width="{pw:.0f}"'
           f' height="{ph_*.5:.0f}" fill="#dce7f2" opacity=".55"/>')
    pr += mesto_stoka(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, pr)
    # ЕЛИ по сторонам — ПОВЕРХ проёма (передний план)
    for i, (ex_, eb, eh) in enumerate(((60, 980, 620), (260, 1010, 540),
                                       (420, 940, 460), (1500, 990, 580),
                                       (1700, 1020, 640), (1860, 960, 500))):
        s += SL(Z_SRED, f'<path d="M{ex_:.0f},{eb:.0f} l{eh*.26:.0f},{-eh*.34:.0f}'
                        f' l{-eh*.10:.0f},0 l{eh*.20:.0f},{-eh*.30:.0f}'
                        f' l{-eh*.08:.0f},0 l{eh*.16:.0f},{-eh*.36:.0f}'
                        f' l{eh*.16:.0f},{eh*.36:.0f} l{-eh*.08:.0f},0'
                        f' l{eh*.20:.0f},{eh*.30:.0f} l{-eh*.10:.0f},0'
                        f' l{eh*.26:.0f},{eh*.34:.0f} Z" fill="#2f4a3a"'
                        f' stroke="{K}" stroke-width="5"/>')
        s += SL(Z_SRED, f'<path d="M{ex_+eh*.20:.0f},{eb-eh*.40:.0f}'
                        f' q{eh*.14:.0f},{-eh*.06:.0f} {eh*.28:.0f},0" fill="none"'
                        f' stroke="url(#sneg)" stroke-width="12" opacity=".9"/>')
    # ДОРОГА с санным следом
    s += SL(Z_SRED, f'<path d="M-40,1080 Q560,780 860,672 L1060,672 Q1400,790 1960,1080 Z"'
                    f' fill="#dce7f2" stroke="{K}" stroke-width="5"/>')
    for i in (-1, 1):
        s += SL(Z_SRED, f'<path d="M{960+i*300:.0f},1080 Q{960+i*120:.0f},820'
                        f' {960+i*40:.0f},690" fill="none" stroke="#9fb0c0"'
                        f' stroke-width="26" opacity=".8"/>')
    s += SL(Z_SRED, inej_mel(463, 60, 700, 1070))
    # ОБОЗ уходит вперёд
    uh = A.ease(A.seg(t, .3, 4.0))
    for i in range(3):
        sx_ = 1060 - i * 230 + 160 * uh
        sy_ = 760 + i * 90
        s += SL(Z_SRED, sani_s_rogozhey(sx_, sy_, .5 + i * .18, t, i * .3, True))
        s += SL(Z_SRED, f'<ellipse cx="{sx_-150-i*40:.0f}" cy="{sy_-60-i*20:.0f}"'
                        f' rx="{40+i*12:.0f}" ry="{70+i*20:.0f}" fill="#2b2419"'
                        f' opacity=".92" stroke="{K}" stroke-width="4"/>')
    # ПАРЕНЬ с книгами у груди
    px_, py_, ph2 = 760, 1050, 700
    shag = A.ease(A.seg(t, .4, 3.4))
    s += SL(Z_SRED, figura(px_ + 120 * shag, py_, ph2, t, col="#5e4430",
                           kant="#cfe4f5", tulup=True, shapka=True, ph=.2,
                           naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(px_ + 120 * shag, py_, ph2, 1, ph2 * .24, 24, t,
                              "#5e4430", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(px_ + 120 * shag, py_, ph2, -1, ph2 * .24, 28, t,
                              "#5e4430", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    kx_, ky_ = px_ + 120 * shag, py_ - ph2 * .48
    s += SL(Z_SRED, f'<rect x="{kx_-80:.0f}" y="{ky_-20:.0f}" width="160" height="44"'
                    f' rx="6" fill="#6b3a2a" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="{kx_-72:.0f}" y="{ky_+24:.0f}" width="150" height="40"'
                    f' rx="6" fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<path d="M{kx_-100:.0f},{ky_-60:.0f} q{-50:.0f},{80:.0f}'
                    f' {-20:.0f},{170:.0f} q{50:.0f},{20:.0f} {80:.0f},{-20:.0f} Z"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, para_izo_rta(kx_ - 40, py_ - ph2 * .80, t, .3, 1.2, .6))
    s += SL(Z_SRED, f'<path d="M{kx_-40:.0f},{py_-ph2*.84:.0f} h{80:.0f}"'
                    f' stroke="{INEY}" stroke-width="7" opacity=".8"/>')
    s += SL(Z_SRED, ten(kx_, py_ + 6, 130, 22, .4))
    # СЧЁТЧИК ВЁРСТ растёт (палочки, без цифр)
    n = 1 + int((t * 1.2) % 6)
    for i in range(n):
        s += SL(Z_SRED, f'<rect x="{1180+i*46:.0f}" y="200" width="16" height="70"'
                        f' rx="6" fill="#d6a63f" opacity=".9"/>')
    # деревня позади: гаснущее окно
    gas = max(.0, 1 - A.ease(A.seg(t, 1.6, 1.6)))
    s += SL(Z_DAL, izba_snaruzhi(120, 700, 220, t, gas > .4, True, 107))
    s += SL(Z_SRED, f'<rect x="160" y="620" width="80" height="60" rx="5"'
                    f' fill="#ffd98a" opacity="{gas:.2f}"/>')
    # верстовой столб и заячий след
    s += SL(Z_SRED, verstovoy_stolb(1420, 940, 300, t, 1.0, .2))
    for i in range(6):
        sx2 = 300 + i * 90
        sy2 = 980 + ((i * 7) % 3) * 22
        s += SL(Z_SRED, f'<ellipse cx="{sx2:.0f}" cy="{sy2:.0f}" rx="13" ry="20"'
                        f' fill="#9fb0c0" opacity=".8"/>'
                        f'<ellipse cx="{sx2+22:.0f}" cy="{sy2-10:.0f}" rx="11" ry="17"'
                        f' fill="#9fb0c0" opacity=".8"/>')
    s += SL(Z_LETIT, sneg_letit(t, 28, 109, .45, .6))
    s += ramka_pp("oba", "#0e0c0b", .55)
    s += vinetka(.46)
    return s


def sannyy_sled_do_vorot(t):
    """Вид сверху: два ровных санных следа тянутся от деревни у моря через
    леса и поля до городских ворот с башнями. По следу идёт фигурка с
    котомкой и книгами; над деревней значок-рыба, над воротами значок-книга."""
    rnd = random.Random(3028)
    s = (f'<rect width="{W}" height="{H}" fill="#dce7f2"/>')
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#cfe0ee" opacity=".6"/>')
    # ПОЛЯ и ЛЕСА сверху
    for i in range(9):
        s += SL(Z_DAL, f'<path d="M{rnd.uniform(-100,400):.0f},{80+i*120:.0f}'
                       f' q{rnd.uniform(400,900):.0f},{rnd.uniform(-50,50):.0f}'
                       f' {rnd.uniform(1400,2000):.0f},{rnd.uniform(-30,30):.0f}"'
                       f' fill="none" stroke="#c4d8e8" stroke-width="{rnd.uniform(14,40):.0f}"'
                       f' opacity=".8"/>')
    for i in range(34):
        ex_ = rnd.uniform(-20, 1900)
        ey_ = rnd.uniform(120, 1040)
        eh = rnd.uniform(40, 90)
        s += SL(Z_DAL, f'<path d="M{ex_:.0f},{ey_:.0f} l{eh*.4:.0f},{-eh:.0f}'
                       f' l{eh*.4:.0f},{eh:.0f} Z" fill="#2f4a3a" opacity=".92"'
                       f' stroke="{K}" stroke-width="3"/>')
    # РЕКИ подо льдом
    for i in range(2):
        s += SL(Z_SRED, f'<path d="M{-40+i*700:.0f},{1080:.0f}'
                        f' Q{400+i*500:.0f},{700-i*200:.0f} {900+i*600:.0f},{120:.0f}"'
                        f' fill="none" stroke="#9fc4d8" stroke-width="46"'
                        f' opacity=".85"/>')
    # ДЕРЕВНЯ у моря (слева внизу) и ГОРОД с воротами (справа вверху)
    s += SL(Z_SRED, f'<path d="M-40,1080 q{200:.0f},{-120:.0f} {420:.0f},{-80:.0f}'
                    f' l0,{200:.0f} l{-440:.0f},0 Z" fill="#6f7a84" opacity=".8"/>')
    for i, (ix, iy) in enumerate(((120, 960), (240, 1010), (330, 940))):
        s += SL(Z_SRED, izba_snaruzhi(ix, iy, 120, t, True, True, 113 + i)
                + dym_stolbom(ix + 14, iy - 76, t, 160, .4, .35, 5))
    s += SL(Z_SRED, f'<rect x="1480" y="120" width="380" height="240" rx="8"'
                    f' fill="#c3ab8a" stroke="{K}" stroke-width="6"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{1490+i*62:.0f}" y="100" width="32" height="24"'
                        f' fill="#c3ab8a" stroke="{K}" stroke-width="3"/>')
    for bx in (1460, 1820):
        s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="60" width="80" height="300"'
                        f' fill="#cbb492" stroke="{K}" stroke-width="5"/>'
                        f'<path d="M{bx-14:.0f},60 l{47:.0f},{-44:.0f} l{47:.0f},{44:.0f} Z"'
                        f' fill="#a8552f" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M1600,360 l0,-110 q{70:.0f},{-60:.0f} {140:.0f},0 l0,110 Z"'
                    f' fill="#3f2d1c" stroke="{K}" stroke-width="5"/>')
    # САННЫЙ СЛЕД: две ровные колеи через весь кадр
    put = "M300,1000 Q700,860 980,620 Q1240,420 1600,330"
    for i, off in enumerate((-16, 16)):
        s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#9fb0c0"'
                        f' stroke-width="14" opacity=".9"'
                        f' transform="translate({off},{off*.5:.0f})"/>')
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#eaf6ff" stroke-width="46"'
                    f' opacity=".35"/>')
    # ФИГУРКА идёт по следу
    idt = A.ease(A.seg(t, .3, 3.6))
    fx = 300 + (1600 - 300) * idt
    fy = 1000 - 670 * (idt ** .92)
    s += SL(Z_SRED, figura(fx, fy, 170, t, col="#5e4430", kant="#cfe4f5",
                           shapka=True, tulup=True, ph=.3))
    s += SL(Z_SRED, f'<rect x="{fx-26:.0f}" y="{fy-100:.0f}" width="52" height="30"'
                    f' rx="5" fill="#6b3a2a" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<path d="M{fx-34:.0f},{fy-120:.0f} q{-20:.0f},{30:.0f}'
                    f' {-8:.0f},{60:.0f} q{20:.0f},{8:.0f} {30:.0f},{-8:.0f} Z"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="3.4"/>')
    # ЗНАЧКИ: рыба над деревней, книга над воротами
    s += SL(Z_SRED, f'<g opacity="{1-idt*.7:.2f}">'
                    f'<ellipse cx="260" cy="860" rx="56" ry="30" fill="#8aa8b4"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M316,860 l{30:.0f},{-20:.0f} l0,{40:.0f} Z"'
                    f' fill="#6f7a84" stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="236" cy="854" r="5" fill="{K}"/></g>')
    gor_ = A.ease(A.seg(t, 2.4, 1.2))
    s += SL(Z_SRED, f'<g opacity="{gor_:.2f}">'
                    f'<rect x="1600" y="180" width="120" height="86" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M1660,180 v86" stroke="#c9bfa6" stroke-width="6"/>'
                    f'<circle cx="1660" cy="222" r="{70*gor_:.0f}" fill="#ffe9ac"'
                    f' opacity="{.35*gor_:.2f}"/></g>')
    # верстовые столбы вдоль следа
    for i, (vx_, vy_) in enumerate(((520, 920), (820, 760), (1120, 560), (1400, 420))):
        s += SL(Z_SRED, verstovoy_stolb(vx_, vy_, 90, t, .5, i * .2))
    s += SL(Z_LETIT, sneg_letit(t, 22, 113, .4, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def kabinet_uchenogo(t):
    """Кабинет восемнадцатого века: стол с колбами, телескоп на треноге,
    глобус, стопы книг, мозаичное панно без сюжета, гусиные перья. Учёный в
    камзоле стоит со спины и держит колбу на свету."""
    rnd = random.Random(3029)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="840" fill="#5e4430"/>')
    for i in range(14):
        s += SL(Z_DAL, f'<rect x="{-10+i*140:.0f}" y="0" width="118" height="840"'
                       f' fill="#6b4c32" opacity=".55"/>')
    s += SL(Z_DAL, svody(t, "#4b443b", 3))
    s += SL(Z_SRED, polovicy(840, "#7a5436"))
    # ОКНО и ПЕЧЬ с изразцами
    s += SL(Z_SRED, f'<rect x="1480" y="140" width="380" height="440" rx="10"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="7"/>'
                    f'<rect x="1510" y="170" width="320" height="380" fill="#8aa8b4"'
                    f' opacity=".5"/>'
                    f'<path d="M1670,140 v440 M1480,360 h380" stroke="#e4d8bd"'
                    f' stroke-width="16"/>')
    s += SL(Z_SRED, f'<rect x="60" y="180" width="300" height="660" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="6"/>')
    for i in range(18):
        s += SL(Z_SRED, f'<rect x="{80+(i%3)*94:.0f}" y="{210+(i//3)*100:.0f}"'
                        f' width="84" height="88" rx="6" fill="#dce7f2" stroke="#9fc4d8"'
                        f' stroke-width="4"/>'
                        f'<path d="M{96+(i%3)*94:.0f},{250+(i//3)*100:.0f}'
                        f' q{26:.0f},{-26:.0f} {52:.0f},0" fill="none" stroke="#6f8ca8"'
                        f' stroke-width="4"/>')
    # СТОЛ с колбами, перьями, стопами книг
    s += SL(Z_SRED, stol(420, 760, 1000, 46, True))
    for i, (kx_, ks) in enumerate(((560, 1.0), (680, .78), (780, .9))):
        s += SL(Z_SRED, f'<path d="M{kx_-40*ks:.0f},{760:.0f} q{-20*ks:.0f},{-80*ks:.0f}'
                        f' {30*ks:.0f},{-110*ks:.0f} l0,{-50*ks:.0f} h{20*ks:.0f}'
                        f' l0,{50*ks:.0f} q{50*ks:.0f},{30*ks:.0f} {30*ks:.0f},{110*ks:.0f} Z"'
                        f' fill="{STEKLO}" opacity=".55" stroke="{K}"'
                        f' stroke-width="{4*ks:.1f}"/>'
                        f'<path d="M{kx_-30*ks:.0f},{740:.0f} q{30*ks:.0f},{14*ks:.0f}'
                        f' {60*ks:.0f},0 l0,{20*ks:.0f} h{-60*ks:.0f} Z"'
                        f' fill="{["#6f8c4a","#8a2f22","#3f6b7a"][i]}" opacity=".85"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1180+i*10:.0f}" y="{700-i*26:.0f}" width="170"'
                        f' height="26" rx="5" fill="#6b3a2a" stroke="{K}"'
                        f' stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M1420,760 h90 l-10,-50 h-70 Z" fill="#3f3a33"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1470,712 l{60:.0f},{-120:.0f}" stroke="#e8e2d6"'
                    f' stroke-width="8"/>'
                    f'<path d="M1524,596 q{24:.0f},{-36:.0f} {36:.0f},{-8:.0f}'
                    f' q{-16:.0f},{24:.0f} {-30:.0f},{28:.0f} Z" fill="#f4f1e8"'
                    f' stroke="{K}" stroke-width="3"/>')
    # ГЛОБУС с бегущими лучами
    gx, gy = 980, 640
    s += SL(Z_SRED, f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="110" fill="#8aa8b4"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<path d="M{gx-110:.0f},{gy:.0f} q{110:.0f},{-50:.0f} {220:.0f},0'
                    f' q{-110:.0f},{50:.0f} {-220:.0f},0 Z" fill="#6f8c4a" opacity=".8"/>'
                    f'<path d="M{gx-70:.0f},{gy-70:.0f} q{70:.0f},{30:.0f} {140:.0f},{10:.0f}"'
                    f' fill="none" stroke="#56763f" stroke-width="12" opacity=".85"/>'
                    f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="110" ry="40" fill="none"'
                    f' stroke="#c9bfa6" stroke-width="4"/>'
                    f'<path d="M{gx:.0f},{gy+110:.0f} l0,{50:.0f} h{-40:.0f} h{80:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="9"/>')
    for i in range(5):
        d = ((t * .6 + i / 5.0) % 1.0)
        a = -2.2 + i * .7
        s += SL(Z_SRED, f'<path d="M{gx:.0f},{gy:.0f} l{(110+120*d)*math.cos(a):.0f},'
                        f'{(110+120*d)*math.sin(a):.0f}" stroke="#ffd98a"'
                        f' stroke-width="{6-3*d:.1f}" opacity="{(1-d)*.8:.2f}"/>')
    # ТЕЛЕСКОП на треноге
    s += SL(Z_SRED, f'<g transform="rotate(-24 1600 820)">'
                    f'<rect x="1500" y="520" width="220" height="60" rx="26"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1700" y="534" width="70" height="34" rx="14"'
                    f' fill="{MED}" stroke="{K}" stroke-width="4"/></g>'
                    f'<path d="M1600,820 l{-80:.0f},{220:.0f} M1600,820 l{10:.0f},{230:.0f}'
                    f' M1600,820 l{90:.0f},{210:.0f}" stroke="#6b4428" stroke-width="11"/>')
    bl = .5 + .5 * A.w(t, 2.6, .2)
    s += SL(Z_SRED, f'<circle cx="1772" cy="548" r="14" fill="#cfe4f5"'
                    f' opacity="{bl:.2f}"/>')
    # УЧЁНЫЙ со спины и вполоборота
    ux, uy, uh = 760, 1050, 720
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#4a3a52", kant="#ffd98a",
                           ph=.2, profil=True))
    s += SL(Z_SRED, f'<path d="M{ux-110:.0f},{uy-uh*.62:.0f} q{110:.0f},{-24:.0f}'
                    f' {220:.0f},0 l{20:.0f},{uh*.40:.0f} q{-130:.0f},{30:.0f}'
                    f' {-260:.0f},0 Z" fill="#6b4a6a" stroke="{K}" stroke-width="5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{ux-10:.0f}" cy="{uy-uh*.56+i*44:.0f}" r="9"'
                        f' fill="{ZOL}" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<path d="M{ux-70:.0f},{uy-uh*.84:.0f} q{70:.0f},{-40:.0f}'
                    f' {140:.0f},0 q{-10:.0f},{80:.0f} {-70:.0f},{86:.0f}'
                    f' q{-60:.0f},{-6:.0f} {-70:.0f},{-86:.0f} Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    r1, (e1x, e1y), _ = _ruka(ux, uy, uh, 1, uh * .30, -34, t, "#4a3a52", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ux, uy, uh, -1, uh * .26, 30, t, "#4a3a52", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x-26:.0f},{e1y:.0f} q{-10:.0f},{-60:.0f}'
                    f' {26:.0f},{-80:.0f} q{36:.0f},{20:.0f} {26:.0f},{80:.0f} Z"'
                    f' fill="{STEKLO}" opacity=".6" stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{e1x:.0f}" cy="{e1y-60:.0f}" r="{24+8*bl:.0f}"'
                    f' fill="#ffe9ac" opacity="{.3+.3*bl:.2f}"/>')
    s += SL(Z_SRED, svecha(1300, 760, t, .2, 1.4, 100) + teplo(1300, 700, 300, 250, .45))
    s += SL(Z_SRED, hodiki(1180, 240, t, 1.4))
    s += SL(Z_SRED, ten(ux, uy + 6, 140, 24, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def klass_uchit_naizust(t):
    """Школьный класс: ученица с косичками читает наизусть у доски, над ней
    всплывают строчки-завитки; учительница водит ручкой по журналу, двое за
    первой партой подсказывают из-за учебника."""
    rnd = random.Random(3030)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="600" fill="#d8cbb0"/>'
                   f'<rect x="0" y="600" width="{W}" height="56" fill="#8a7a52"'
                   f' opacity=".85"/>')
    s += SL(Z_DAL, klassnaya_doska(300, 140, 760, 400, t, 17))
    s += SL(Z_DAL, okno_izby(1560, 130, 320, 340, t, None, .25, False, True))
    s += SL(Z_SRED, polovicy(740, "#8a6342"))
    # ПОРТРЕТНАЯ РАМА над доской — нарисованная контуром
    s += SL(Z_SRED, f'<rect x="560" y="20" width="240" height="110" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="580" y="36" width="200" height="78" rx="5"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="3.6"/>'
                    f'<ellipse cx="680" cy="86" rx="40" ry="34" fill="none"'
                    f' stroke="#8a7a62" stroke-width="5"/>'
                    f'<path d="M652,110 q{28:.0f},{-20:.0f} {56:.0f},0" fill="none"'
                    f' stroke="#8a7a62" stroke-width="5"/>')
    # УЧЕНИЦА у доски
    ux, uy, uh = 1180, 1000, 560
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#3f3a4a", kant="#ffd98a", ph=.2))
    s += SL(Z_SRED, f'<path d="M{ux-26:.0f},{uy-uh*.84:.0f} q{26:.0f},{80:.0f}'
                    f' {10:.0f},{150:.0f}" fill="none" stroke="#6b4428"'
                    f' stroke-width="16"/>'
                    f'<path d="M{ux+26:.0f},{uy-uh*.84:.0f} q{-20:.0f},{80:.0f}'
                    f' {-6:.0f},{150:.0f}" fill="none" stroke="#6b4428"'
                    f' stroke-width="16"/>')
    r1, (e1x, e1y), _ = _ruka(ux, uy, uh, 1, uh * .26, 64, t, "#3f3a4a", "#ffd98a", .2, 3)
    r2, (e2x, e2y), _ = _ruka(ux, uy, uh, -1, uh * .26, 66, t, "#3f3a4a", "#ffd98a", .6, 3)
    s += SL(Z_SRED, r1 + r2)
    # СТРОЧКИ-ЗАВИТКИ всплывают
    for i in range(5):
        d = ((t * .45 + i / 5.0) % 1.0)
        s += SL(Z_SRED, f'<path d="M{ux-130+30*math.sin(i+d*4):.0f},{uy-uh-40-200*d:.0f}'
                        f' q{50:.0f},{-16:.0f} {100:.0f},0 q{40:.0f},{14:.0f}'
                        f' {80:.0f},{-4:.0f}" fill="none" stroke="#6f6354"'
                        f' stroke-width="{5-2*d:.1f}" opacity="{(1-d)*.8:.2f}"/>')
    # УЧИТЕЛЬНИЦА за столом
    s += SL(Z_SRED, f'<rect x="1480" y="820" width="380" height="40" rx="8"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1500" y="860" width="30" height="180" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1810" y="860" width="30" height="180" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="4"/>')
    ux2, uy2, uh2 = 1700, 820, 520
    s += SL(Z_SRED, figura(ux2, uy2, uh2, t, col="#6b3a6a", kant="#ffd98a", ph=.6))
    pish = 6 * A.w(t, 1.3, .2)
    r3, (e3x, e3y), _ = _ruka(ux2, uy2, uh2, -1, uh2 * .32, 20 + 6 * pish, t,
                              "#6b3a6a", "#ffd98a", .3, 5)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x:.0f},{e3y:.0f} l{-40:.0f},{-26:.0f}"'
                         f' stroke="#8a6342" stroke-width="7"/>'
                         f'<rect x="{e3x-160:.0f}" y="{e3y-10:.0f}" width="150"'
                         f' height="60" rx="6" fill="#f2ead6" stroke="{K}"'
                         f' stroke-width="4"/>')
    # ДВОЕ за первой партой, один прикрыл рот учебником
    s += SL(Z_SRED, parta_shkolnaya(380, 1040, 460, t, 19, True))
    for i, (px_, ph_) in enumerate(((480, 440), (700, 460))):
        s += SL(Z_SRED, figura(px_, 880, ph_, t, col=["#3f5a6a", "#4a6a3a"][i],
                               kant="#ffd98a", ph=i * .4))
        rk, (ex, ey), _ = _ruka(px_, 880, ph_, 1, ph_ * .28, 10, t,
                                ["#3f5a6a", "#4a6a3a"][i], "#ffd98a", i * .3, 4)
        rk2, (e2x_, e2y_), _ = _ruka(px_, 880, ph_, -1, ph_ * .28, 14, t,
                                     ["#3f5a6a", "#4a6a3a"][i], "#ffd98a", i * .3 + .4, 4)
        s += SL(Z_SRED, rk + rk2)
        if i == 1:
            s += SL(Z_SRED, f'<rect x="{px_-80:.0f}" y="{880-ph_*.86:.0f}" width="160"'
                            f' height="110" rx="8" fill="#6b3a2a" stroke="{K}"'
                            f' stroke-width="4.5"/>'
                            f'<path d="M{px_:.0f},{880-ph_*.86:.0f} v110" stroke="#54351f"'
                            f' stroke-width="6"/>')
    # глобус, карта, цветы
    s += SL(Z_SRED, f'<circle cx="1320" cy="640" r="60" fill="#3f6b7a" stroke="{K}"'
                    f' stroke-width="5"/>'
                    f'<path d="M1262,626 q{58:.0f},{34:.0f} {116:.0f},0" fill="none"'
                    f' stroke="#56763f" stroke-width="7"/>'
                    f'<path d="M1320,700 l0,40 h-30 h60" fill="none" stroke="#6b4428"'
                    f' stroke-width="7"/>')
    s += SL(Z_SRED, f'<rect x="120" y="160" width="140" height="380" rx="6"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M140,{200+i*50:.0f} q{34:.0f},{-10:.0f} {68:.0f},0'
                        f' q{20:.0f},{10:.0f} {32:.0f},{-4:.0f}" fill="none"'
                        f' stroke="#9fc4d8" stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M1600,500 h110 l-12,-60 h-86 Z" fill="#a8743c"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        a = -1.1 + i * .55
        s += SL(Z_SRED, f'<path d="M1655,440 q{40*math.sin(a):.0f},{-50:.0f}'
                        f' {62*math.sin(a):.0f},{-110:.0f} q{14:.0f},{30:.0f}'
                        f' {-30*math.sin(a):.0f},{110:.0f} Z" fill="#56763f"'
                        f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, lampa(960, 60, t, 1.3, True) + teplo(960, 80, 300, 250, .40))
    s += SL(Z_SRED, ten(ux, uy + 6, 120, 20, .4))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def gorka_vo_dvore(t):
    """Ледяная горка во дворе на пол-кадра в зимних сумерках под фонарём:
    трое съезжают один за другим — на коньках, на санках со спинкой и верхом
    на школьном портфеле. Внизу куча-мала из валенок и варежек."""
    rnd = random.Random(3031)
    s = nebo("sumer", t, True, 467)
    s += SL(Z_DAL, panelka(60, 620, 760, t, 5, True, 79))
    s += SL(Z_DAL, panelka(1420, 600, 500, t, 5, True, 83))
    s += SL(Z_SRED, _merzlaya_zemlya(760, 467, False))
    s += SL(Z_SRED, sneg_lezhit(790, 32, "url(#sneg)"))
    # ГОРКА на пол-кадра
    s += SL(Z_SRED, f'<path d="M420,980 L820,380 L1020,380 L1020,980 Z"'
                    f' fill="#dce7f2" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1020,380 L1020,980 L1560,1000 Q1300,740 1020,380 Z"'
                    f' fill="url(#led)" stroke="{K}" stroke-width="6"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{1040+i*16:.0f},{420+i*76:.0f}'
                        f' q{120:.0f},{100:.0f} {260:.0f},{180:.0f}" fill="none"'
                        f' stroke="#eaf6ff" stroke-width="5" opacity=".6"/>')
    for i in range(6):                 # ступени с другой стороны
        s += SL(Z_SRED, f'<rect x="{480+i*58:.0f}" y="{900-i*88:.0f}" width="80"'
                        f' height="22" rx="5" fill="{DOSKA}" stroke="{K}"'
                        f' stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<path d="M420,980 l0,-120 M820,380 l0,-60" stroke="#8a6342"'
                    f' stroke-width="11"/>'
                    f'<rect x="800" y="300" width="240" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>')
    # ТРОЕ съезжают один за другим
    for i, (vid, col) in enumerate((("konki", "#3f5a6a"), ("sanki", "#8a2f22"),
                                    ("portfel", "#4a6a3a"))):
        d = A.ease(A.seg(t, .4 + i * .9, 1.6))
        if d <= .01:
            continue
        gx_ = 1020 + 520 * d
        gy_ = 400 + 580 * (d ** 1.6)
        if vid == "konki":
            s += SL(Z_SRED, figura(gx_, gy_, 400, t, col=col, kant="#cfe4f5",
                                   shapka=True, ph=.2, naklon=4.0))
            rk, (ex, ey), _ = _ruka(gx_, gy_, 400, 1, 400 * .30, -34, t,
                                    col, "#cfe4f5", .2, 7)
            rk2, (e2x_, e2y_), _ = _ruka(gx_, gy_, 400, -1, 400 * .30, -30, t,
                                         col, "#cfe4f5", .6, 7)
            s += SL(Z_SRED, rk + rk2)
            s += SL(Z_SRED, konki_snegurki(gx_ - 24, gy_, .6, 0, True, t, .2)
                    + konki_snegurki(gx_ + 34, gy_ + 4, .6, 0, True, t, .6))
        elif vid == "sanki":
            s += SL(Z_SRED, sanki_derev(gx_, gy_ + 20, .9, t, .3, True))
            s += SL(Z_SRED, figura(gx_, gy_ - 40, 380, t, col=col, kant="#cfe4f5",
                                   platok=True, ph=.5, naklon=3.0))
            rk, (ex, ey), _ = _ruka(gx_, gy_ - 40, 380, 1, 380 * .28, -12, t,
                                    col, "#cfe4f5", .3, 5)
            rk2, (e2x_, e2y_), _ = _ruka(gx_, gy_ - 40, 380, -1, 380 * .28, -8, t,
                                         col, "#cfe4f5", .8, 5)
            s += SL(Z_SRED, rk + rk2)
            s += SL(Z_SRED, f'<path d="M{gx_+70:.0f},{gy_-120:.0f} q{90:.0f},{-20:.0f}'
                            f' {170:.0f},{-50:.0f} l{8:.0f},{34:.0f} q{-84:.0f},{30:.0f}'
                            f' {-176:.0f},{50:.0f} Z" fill="{TKAN}" stroke="{K}"'
                            f' stroke-width="4"/>')
        else:
            s += SL(Z_SRED, f'<rect x="{gx_-70:.0f}" y="{gy_-20:.0f}" width="140"'
                            f' height="90" rx="10" fill="#6b4428" stroke="{K}"'
                            f' stroke-width="4.5"/>'
                            f'<path d="M{gx_-70:.0f},{gy_+14:.0f} h140" stroke="#54351f"'
                            f' stroke-width="6"/>')
            s += SL(Z_SRED, figura(gx_, gy_ - 20, 370, t, col=col, kant="#cfe4f5",
                                   shapka=True, ph=.8, naklon=5.0))
            rk, (ex, ey), _ = _ruka(gx_, gy_ - 20, 370, 1, 370 * .32, -54, t,
                                    col, "#cfe4f5", .4, 8)
            rk2, (e2x_, e2y_), _ = _ruka(gx_, gy_ - 20, 370, -1, 370 * .32, -50, t,
                                         col, "#cfe4f5", .9, 8)
            s += SL(Z_SRED, rk + rk2)
            s += SL(Z_SRED, f'<ellipse cx="{gx_:.0f}" cy="{gy_-20-370*.80:.0f}" rx="52"'
                            f' ry="26" fill="#4a3a2c" stroke="{K}" stroke-width="4"/>')
    # КУЧА-МАЛА из валенок и варежек внизу
    for i in range(5):
        s += SL(Z_SRED, _valenok(1500 + i * 60, 1050 - ((i * 7) % 3) * 12,
                                 .72, -20 + i * 12))
    for i in range(4):
        s += SL(Z_SRED, varezhka(1480 + i * 80, 990 - ((i * 5) % 3) * 16, .9,
                                 -30 + i * 22, TKAN, t, i * .25))
    # фонарь, собака, дома с жёлтыми окнами
    s += SL(Z_SRED, f'<rect x="300" y="400" width="24" height="520" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(312, 400, t, 1.5, True) + teplo(312, 430, 360, 300, .45))
    beg = ((t * .6) % 1.0)
    sx_ = 1740 - 400 * beg
    s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="1010" rx="70" ry="34" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{sx_-62:.0f}" cy="976" r="28" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M{sx_-80:.0f},{956:.0f} l{-12:.0f},{-26:.0f}'
                    f' l{-10:.0f},{26:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3"/>'
                    f'<path d="M{sx_+66:.0f},1000 q{36:.0f},{-28:.0f} {52:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#6b5230" stroke-width="9"/>')
    # ДВОР У ГОРКИ: бортики, скамейка, санки у забора, ёлочки, сугробы
    for i in range(9):
        s += SL(Z_SRED, f'<ellipse cx="{120+i*210:.0f}" cy="{1010+((i*5)%3)*18:.0f}"'
                        f' rx="{80+((i*7)%4)*22:.0f}" ry="{24+((i*3)%2)*10:.0f}"'
                        f' fill="url(#sneg)" opacity=".92"/>')
    s += SL(Z_SRED, zabor_shtaket(-40, 820, 460, 180, 467, 58))
    s += SL(Z_SRED, f'<rect x="120" y="940" width="280" height="20" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="140" y="960" width="20" height="80" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="360" y="960" width="20" height="80" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, sanki_derev(220, 1050, .8, t, .4, True))
    for i, (ex_, eb_, eh_) in enumerate(((1760, 1000, 300), (1880, 1030, 260))):
        s += SL(Z_SRED, f'<path d="M{ex_:.0f},{eb_:.0f} l{eh_*.26:.0f},{-eh_*.36:.0f}'
                        f' l{-eh_*.10:.0f},0 l{eh_*.20:.0f},{-eh_*.32:.0f}'
                        f' l{-eh_*.08:.0f},0 l{eh_*.16:.0f},{-eh_*.32:.0f}'
                        f' l{eh_*.16:.0f},{eh_*.32:.0f} l{-eh_*.08:.0f},0'
                        f' l{eh_*.20:.0f},{eh_*.32:.0f} l{-eh_*.10:.0f},0'
                        f' l{eh_*.26:.0f},{eh_*.36:.0f} Z" fill="#2f4a3a"'
                        f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(6):
        s += SL(Z_SRED, varezhka(560 + i * 90, 1056 - ((i * 5) % 3) * 14, .7,
                                 -24 + i * 16, TKAN2, t, i * .2))
    s += SL(Z_SRED, inej_mel(467, 44, 980, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 26, 127, .45, .6))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def vecherniy_stol_u_okna_na_prud(t):
    """Вечерний стол у окна на пруд: липовый чай с мёдом, калина в розетке,
    тёплая лампа. В проёме окна над столом — настоящий замёрзший пруд на
    закате; за столом хозяйка и хозяин, кот спит на лавке."""
    rnd = random.Random(3032)
    s = stena_gornicy_19(t, 61, 860, True, True)
    # ОКНО-ПРОЁМ над столом (сверху)
    px, py, pw, ph_ = 560, 140, 780, 320
    okno = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
            f' fill="#c88a6a"/>')
    okno += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.45:.0f}"'
             f' fill="#e0a07a"/>')
    okno += mesto_stoka(px, py, pw, ph_, "pryam")
    okno += (f'<rect x="{px-18:.0f}" y="{py-18:.0f}" width="{pw+36:.0f}"'
             f' height="{ph_+36:.0f}" rx="6" fill="none" stroke="#6b4428"'
             f' stroke-width="26"/>')
    okno += (f'<path d="M{px+pw*.5:.0f},{py:.0f} v{ph_:.0f} M{px:.0f},{py+ph_*.5:.0f}'
             f' h{pw:.0f}" stroke="#6b4428" stroke-width="16"/>')
    okno += (f'<rect x="{px-50:.0f}" y="{py+ph_+18:.0f}" width="{pw+100:.0f}"'
             f' height="32" rx="6" fill="{DOSKA}" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, okno)
    s += SL(Z_SRED, teplo(px + pw * .5, py + ph_ * .5, 520, 420, .30))
    kch = 5 * A.w(t, 2.8, .3)
    for i in (0, 1):
        sdv = (-1 if i == 0 else 1) * 10
        s += SL(Z_SRED, f'<g transform="rotate({kch*(1 if i else -1):.1f}'
                        f' {px+i*(pw-160):.0f} {py-10:.0f})">'
                        f'<path d="M{px+i*(pw-160)+sdv:.0f},{py-16:.0f}'
                        f' q{80:.0f},{40:.0f} {80:.0f},{ph_*.88:.0f} q{-50:.0f},{20:.0f}'
                        f' {-120:.0f},{10:.0f} Z" fill="{RUSH}" opacity=".95"'
                        f' stroke="{K}" stroke-width="4.5"/></g>')
    # СТОЛ: чайник, мёд, калина в розетке, кружки
    s += SL(Z_SRED, stol(240, 780, 1200, 46, True))
    s += SL(Z_SRED, chaynik_s_parom(560, 780, 1.5, t, .1, True))
    s += SL(Z_SRED, banka_moloka(820, 780, .8, t, True, .78, "#d6a63f"))
    s += SL(Z_SRED, f'<ellipse cx="1020" cy="776" rx="92" ry="28" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="1020" cy="766" rx="72" ry="20" fill="#8a2f22"'
                    f' stroke="#6b2419" stroke-width="3.4"/>')
    for i in range(6):
        a = i * 1.05
        s += SL(Z_SRED, f'<circle cx="{1020+46*math.cos(a):.0f}"'
                        f' cy="{764+12*math.sin(a):.0f}" r="11" fill="#c8301f"'
                        f' stroke="#7d1b11" stroke-width="2.6"/>')
    s += SL(Z_SRED, kruzhka_moloka(1220, 780, 1.0, t, False, .2, "#e8e2d6")
            + kruzhka_moloka(1380, 780, 1.0, t, False, .6, "#dce4ea"))
    s += SL(Z_SRED, karavay(340, 776, .9, True))
    # ХОЗЯЙКА и ХОЗЯИН за столом
    for i, (fx_, fy_, fh_, col, pl, bor) in enumerate(
            ((760, 1050, 660, "#4a3a52", True, False),
             (1300, 1056, 680, "#4a4038", False, True))):
        s += SL(Z_SRED, figura(fx_, fy_, fh_, t, col=col, kant="#ffd98a",
                               platok=pl, boroda=bor, ph=i * .4))
        rk, (ex, ey), _ = _ruka(fx_, fy_, fh_, 1, fh_ * .24, 44, t, col, "#ffd98a", i * .3, 3)
        rk2, (e2x_, e2y_), _ = _ruka(fx_, fy_, fh_, -1, fh_ * .24, 48, t, col,
                                     "#ffd98a", i * .3 + .4, 3)
        s += SL(Z_SRED, rk + rk2)
        s += SL(Z_SRED, ten(fx_, fy_ + 6, 128, 22, .45))
    # лавка с котом, печь, полка, ходики
    s += SL(Z_SRED, lavka(1580, 980, 320))
    s += SL(Z_SRED, kot(1700, 980, t, 1.6, "#3b3430", True))
    s += SL(Z_SRED, pech(60, 300, 300, 520, t, True, True, False))
    s += SL(Z_SRED, ogon(150, 700, t, 1.1, .2, 6) + teplo(150, 680, 300, 250, .45))
    s += SL(Z_SRED, polka_s_bankami(1480, 380, 400, t, 127, 4, False))
    s += SL(Z_SRED, hodiki(420, 260, t, 1.3))
    s += SL(Z_SRED, lampa(960, 540, t, 1.6, True) + teplo(960, 580, 460, 380, .5))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


# источники света сцен: сюда ставится блик в объектив (C16/K17)
BLIKI = {
    "alaya_zarya_za_oknom": (1760, 640),
    "bant_za_pervoy_partoy": (960, 80),
    "bochka_u_saraya": (1000, 200),
    "chay_nastaivaetsya": (700, 120),
    "chaynik_i_travy_pod_potolkom": (200, 700),
    "chuzhoy_karavay": (1830, 700),
    "dedov_rybackiy_yaschik": (760, 150),
    "doroga_v_shkolu_i_luzha": (1232, 300),
    "dva_imeni_na_svitke": (370, 610),
    "dva_puti_krynki": (1760, 560),
    "gorka_vo_dvore": (312, 400),
    "gorod_u_yuzhnogo_morya": (1860, 404),
    "imperator_vozvraschaetsya": (300, 560),
    "izba_s_chetyrmya_zabotami": (220, 930),
    "kabinet_uchenogo": (1300, 760),
    "kalina_s_saharom_v_banke": (960, 120),
    "kalinovoe_varene_v_rozetke": (960, 130),
    "katok_vo_dvore": (311, 420),
    "klass_uchit_naizust": (960, 60),
    "konki_na_valenkah": (1531, 260),
    "korotkiy_put_cherez_prud": (1680, 300),
    "kruzhki_moloka_po_schetu": (1660, 640),
    "krynka_i_moneta": (240, 180),
    "kryuchki_v_probke": (640, 160),
    "listok_na_shkolnoy_doske_obyavleni": (960, 90),
    "luzha_u_podezda_k_poludnyu": (1270, 420),
    "mokrye_valenki_na_pechi": (380, 640),
    "molochnyy_sup_i_prostokvasha": (960, 90),
    "nahohlennye_pticy_na_vetke": (1700, 420),
    "novaya_shuba_sosedki": (960, 80),
    "paketik_otdyhaet_chaynik_rabotaet": (960, 70),
    "penka_v_kruzhke": (960, 80),
    "pirog_s_kalinoy": (1660, 700),
    "ploschad_stolicy": (1671, 548),
    "polnyy_podoynik": (240, 240),
    "posoh_i_led": (760, 1010),
    "primerka_konkov_v_prihozhey": (960, 100),
    "pticy_na_dereve_u_doma": (311, 620),
    "puchok_s_cherdaka_korobka_i_meshoc": (540, 200),
    "razgovor_o_proshlyh_ulovah": (960, 150),
    "rybak_i_ledobur_u_steny": (120, 240),
    "schety_u_okna": (1760, 200),
    "shkolnaya_parta_s_uchebnikom": (960, 60),
    "smetana_i_syr_na_svoem_stole": (1800, 660),
    "snasti_na_stole_pod_lampoy": (960, 140),
    "svoe_bogatstvo_na_polkah": (1240, 180),
    "treugolnyy_paket_i_stakan": (960, 90),
    "vecherniy_stol_u_okna_na_prud": (150, 700),
    "vorota_otkryvayutsya_i_zakryvayuts": (960, 700),
}
