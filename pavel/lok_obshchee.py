# -*- coding: utf-8 -*-
"""СКВОЗНЫЕ ОБРАЗЫ РОЛИКА «19 ноября — Павел Ледостав».

День ледостава: ночью схватывает первая корка, днём она обманчиво блестит.
Лужа у калитки, пруд под тонким льдом, мостки, прорубь, санный след, иней на
калине, дым столбом, нахохленные птицы — это и есть сквозные вещи ролика.
Холод снаружи, тепло внутри: тёплое пятно в кадре всегда одно.

Эти кирпичики нарисованы ЗАНОВО под этот текст (R-0019) и живут отдельно от
`baza.py`, чтобы 96 декораций не повторяли друг друга кодом. Технический
каркас анатомии (R-0051) ниже — он часть сборки кадра, а не декорация.
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
