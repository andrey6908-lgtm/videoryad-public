# -*- coding: utf-8 -*-
"""СКВОЗНЫЕ ОБРАЗЫ ролика «Как встречать год хозяйки года 2027».

Нарисованы для этого ролика и только для него (R-0019): ни один образ не
взят у «13 ноября», «14 ноября», «15 ноября» и «16 ноября».

Гамма новогодняя и ТЁПЛАЯ, в отличие от морозных роликов ноября: красный
и золото на синем вечере, одно тёплое пятно в кадре — ёлка, окно, свеча,
циферблат. Хозяйка года — КРАСНАЯ КОЗА с золотыми рожками и бубенчиком:
она открывает ролик у крыльца и приходит к двери в последнем кадре.

РУК НЕ РИСУЕМ (его правило 05.11): где нужно действие — работает предмет.
"""
import math, random
import anim as A
from baza import (W, H, K, o, ten, teplo, SL, KRAS, UGOL, ZOL, MED, SVET, ORA,
                  SNEG, INEY, KREM, ZEL, ZEL2, TKAN, CHUGUN, STEKLO, NOCH)

# ── палитра праздника ──────────────────────────────────────────────────────
ALYJ   = "#c9322b"      # красное платье, шар, флажок
ALYJ2  = "#8d1b1c"
ZOLOTO = "#e3b64a"
ZOLOTO2 = "#9a6f1d"
HVOYA  = "#2f4a33"
HVOYA2 = "#1d3122"
MANDA  = "#ef8b2c"


# ═══════════════════ ХОЗЯЙКА ГОДА — ОГНЕННАЯ КОЗА ═══════════════════

def koza(x, base, t, s_=1.0, idet=0.0, smotrit=True, ph=0.0, op=1.0):
    """Красная коза с золотыми рожками и бубенчиком — хозяйка года.

    Голова ВЫШЕ корпуса и в профиль вправо: с морды начинается чтение кадра.
    `idet` — доля шага вперёд (0 — стоит), корпус покачивается всегда,
    бубенчик отстаёт на полтакта, глаз моргает, ухо подрагивает. Три живых
    элемента в самой фигуре, поэтому коза годится и для статичного плана.
    """
    s = s_
    kach = 2.6 * s * A.w(t, 1.9, ph)
    shag = 150 * s * idet
    g = f'<g transform="translate({x + shag:.1f},{base:.1f}) scale({s:.3f})" opacity="{op:.2f}">'
    g += ten(0, 6, 160, 27, .5)
    # НОГИ: задняя пара темнее — объём; копыта чугунные
    for i, (nx, dl, col) in enumerate(((-96, 0.0, ALYJ2), (-52, .5, ALYJ2),
                                       (56, .5, ALYJ), (100, 0.0, ALYJ))):
        sw = 15 * math.sin(2 * math.pi * (t / .9 + dl + ph)) * (1 if idet else .22)
        g += (f'<path d="M{nx},-104 q{sw*.4:.1f},50 {sw:.1f},98" fill="none"'
              f' stroke="{col}" stroke-width="30" stroke-linecap="round"/>')
        g += f'<rect x="{nx+sw-16:.1f}" y="-10" width="32" height="18" rx="6" fill="{CHUGUN}" {o(4)}/>'
    # КОРПУС — бочонком, круп выше холки
    g += (f'<g transform="translate(0,{kach:.1f})">'
          f'<path d="M-140,-180 q-10,-86 60,-104 q92,-24 168,2 q66,22 58,96'
          f' q-8,66 -72,80 q-104,20 -176,0 q-44,-12 -38,-74 z" fill="{ALYJ}" {o(9)}/>'
          f'<path d="M-112,-238 q84,-22 162,-4" fill="none" stroke="#f2776a"'
          f' stroke-width="16" stroke-linecap="round" opacity=".55"/>'
          f'<path d="M-130,-150 q80,26 170,6" fill="none" stroke="{ALYJ2}"'
          f' stroke-width="14" stroke-linecap="round" opacity=".5"/></g>')
    # хвостик
    hv = 15 * A.w(t, 1.1, ph * 1.7)
    g += (f'<path d="M-140,-238 q-32,{-12+hv:.1f} -40,{-50+hv:.1f}" fill="none"'
          f' stroke="{ALYJ2}" stroke-width="20" stroke-linecap="round"/>')
    # ШЕЯ: толстая, вверх-вправо от холки
    nak = 4.0 * A.w(t, 2.4, ph + .3)
    g += (f'<g transform="translate(150,{-236+kach:.1f}) rotate({nak:.2f})">'
          f'<path d="M-36,46 q10,-82 46,-130" fill="none" stroke="{ALYJ}"'
          f' stroke-width="56" stroke-linecap="round"/>'
          f'<path d="M-30,30 q10,-70 40,-112" fill="none" stroke="#f2776a"'
          f' stroke-width="12" stroke-linecap="round" opacity=".45"/>')
    # ГОЛОВА в профиль вправо: лоб, морда клином
    g += (f'<path d="M-24,-150 q44,-34 92,-10 q44,22 62,54 q10,20 -14,30'
          f' q-40,16 -80,2 q-50,-18 -60,-50 z" fill="{ALYJ}" {o(9)}/>')
    # ухо подрагивает
    uh = 8 * A.w(t, 1.3, ph + .6)
    g += (f'<ellipse cx="-14" cy="-150" rx="34" ry="16" fill="{ALYJ2}" {o(6)}'
          f' transform="rotate({-30+uh:.1f},-14,-150)"/>')
    # РОЖКИ золотые, изгибом назад
    for i, (bx, by) in enumerate(((4, -176), (34, -170))):
        g += (f'<path d="M{bx},{by} q22,-50 -2,-92 q-4,-12 -16,-12" fill="none"'
              f' stroke="url(#zol)" stroke-width="18" stroke-linecap="round"/>')
        g += (f'<path d="M{bx},{by} q22,-50 -2,-92 q-4,-12 -16,-12" fill="none"'
              f' {o(4)} opacity=".4"/>')
    # глаз, ноздря, бородка
    if smotrit and not A.blink(t, 4.1, ph):
        g += '<ellipse cx="42" cy="-128" rx="12" ry="13" fill="#1a1414"/>'
        g += '<circle cx="46" cy="-132" r="4.5" fill="#fff" opacity=".9"/>'
    else:
        g += f'<path d="M30,-128 q12,9 24,0" fill="none" {o(6)}/>'
    g += '<circle cx="116" cy="-96" r="6" fill="#5e1b18"/>'
    bor = 7 * A.w(t, 1.5, ph)
    g += (f'<path d="M66,-72 q{6+bor:.1f},44 {-6+bor:.1f},64" fill="none"'
          f' stroke="{KREM}" stroke-width="14" stroke-linecap="round"/>')
    g += '</g>'
    # БУБЕНЧИК на красной ленте — отстаёт от качания на полтакта
    bub = 9 * A.w(t, 1.9, ph + .5)
    g += (f'<g transform="translate({120+bub*.5:.1f},{-206+kach:.1f})">'
          f'<path d="M-26,-16 q26,10 52,-4" fill="none" stroke="{ALYJ2}" stroke-width="9"/>'
          f'<circle cx="{bub*.5:.1f}" cy="30" r="22" fill="url(#zol)" {o(6)}/>'
          f'<path d="M{-15+bub*.5:.1f},30 h30" fill="none" {o(5)} opacity=".55"/>'
          f'<circle cx="{bub*.5-7:.1f}" cy="22" r="5" fill="#fff6d2" opacity=".8"/></g>')
    g += '</g>'
    return g


def koza_malaya(x, y, t, s_=.42, ph=0.0):
    """Коза-значок: для углов, табличек и карточек — та же фигура мельче."""
    return koza(x, y, t, s_, 0.0, True, ph)


# ═══════════════════ ЧЕЛОВЕК ═══════════════════

def figura(x, base, h_, t, col="#241b24", kant=None, platok=False, ph=0.0,
           profil=False, op=1.0, krasnoe=False):
    """Силуэт со спины или в профиль, всегда с КАНТОМ: без него тёмная фигура
    пропадает на тёмном вечернем фоне. Кант этого ролика ТЁПЛЫЙ — в доме
    горит ёлка. Рук не рисуем: действие отдано предмету."""
    kant = kant or "#f0c070"
    sh = h_ / 300.0
    dy = 3.2 * sh * A.w(t, .62, ph)
    telo = ALYJ if krasnoe else col
    g = f'<g transform="translate({x:.1f},{base + dy:.1f})" opacity="{op:.2f}">'
    g += ten(0, 4, 78 * sh, 17 * sh, .55)
    g += (f'<path d="M{-60*sh:.0f},0 q{-6*sh:.0f},{-150*sh:.0f} {36*sh:.0f},{-196*sh:.0f}'
          f' q{24*sh:.0f},{-10*sh:.0f} {48*sh:.0f},0'
          f' q{42*sh:.0f},{46*sh:.0f} {36*sh:.0f},{196*sh:.0f} z"'
          f' fill="{telo}" stroke="{kant}" stroke-width="{3.4*sh:.1f}" stroke-opacity=".75"/>')
    gy = -232 * sh
    g += (f'<circle cx="{(14 if profil else 0)*sh:.0f}" cy="{gy:.0f}" r="{42*sh:.0f}"'
          f' fill="{telo}" stroke="{kant}" stroke-width="{3.4*sh:.1f}" stroke-opacity=".75"/>')
    if platok:
        pc = ZOLOTO if krasnoe else ALYJ   # платок всегда контрастен телу
        g += (f'<path d="M{-46*sh:.0f},{gy-8*sh:.0f} q{46*sh:.0f},{-56*sh:.0f} {92*sh:.0f},0'
              f' q{4*sh:.0f},{54*sh:.0f} {-46*sh:.0f},{76*sh:.0f}'
              f' q{-50*sh:.0f},{-22*sh:.0f} {-46*sh:.0f},{-76*sh:.0f} z"'
              f' fill="{pc}" {o(max(3, 4*sh))}/>')
        g += (f'<path d="M{-10*sh:.0f},{gy+62*sh:.0f} q{18*sh:.0f},{18*sh:.0f} {36*sh:.0f},{4*sh:.0f}"'
              f' fill="none" stroke="{pc}" stroke-width="{10*sh:.1f}" stroke-linecap="round"/>')
    g += '</g>'
    return g


# ═══════════════════ ЁЛКА, ГИРЛЯНДЫ, ЧАСЫ ═══════════════════

def elka(x, base, h_, t, ogni=True, zvezda=True, seed=4, igrushki=True):
    """Ёлка тремя ярусами: хвоя двумя тонами, мигающие огни по спирали,
    шары и звезда. Огни — живой элемент, они дышат вразнобой."""
    r = random.Random(seed)
    s = h_ / 520.0
    g = f'<g transform="translate({x:.1f},{base:.1f}) scale({s:.3f})">'
    g += ten(0, 8, 210, 34, .55)
    g += f'<rect x="-26" y="-34" width="52" height="40" rx="8" fill="url(#derev)" {o(6)}/>'
    yar = ((-40, 215, 150), (-190, 170, 140), (-320, 120, 130))
    for i, (yy, pw, ph_) in enumerate(yar):
        col = HVOYA if i % 2 == 0 else HVOYA2
        g += (f'<path d="M0,{yy - ph_} L{pw},{yy} q{-pw*.5:.0f},26 {-pw:.0f},26'
              f' q{-pw*.5:.0f},0 {-pw:.0f},-26 z" fill="{col}" {o(7)}/>')
        for k in range(7):
            hx = -pw + 2 * pw * (k + .5) / 7
            g += (f'<path d="M{hx:.0f},{yy+16} l{r.uniform(-18,18):.0f},{-34-r.uniform(0,22):.0f}"'
                  f' fill="none" stroke="{HVOYA2 if i%2==0 else HVOYA}" stroke-width="7"'
                  f' stroke-linecap="round" opacity=".8"/>')
    if igrushki:
        for k, (bx, by, col) in enumerate(((-110, -20, ALYJ), (92, -34, ZOLOTO),
                                           (-72, -170, ZOLOTO), (76, -186, ALYJ),
                                           (-30, -300, ALYJ), (44, -312, ZOLOTO))):
            kol = 4 * A.w(t, 2.6, k * .17)
            g += (f'<g transform="translate({bx + kol:.1f},{by:.0f})">'
                  f'<path d="M0,-26 v12" fill="none" {o(4)}/>'
                  f'<circle r="21" fill="{col}" {o(6)}/>'
                  f'<circle cx="-7" cy="-8" r="6" fill="#fff" opacity=".55"/></g>')
    if ogni:
        for k in range(22):
            u = k / 22.0
            ox = math.sin(u * 7.6) * (205 * (1 - u) + 20)
            oy = -30 - u * 400
            gor = .35 + .65 * (0.5 + 0.5 * math.sin(2 * math.pi * (t / (1.6 + (k % 5) * .4) + k * .21)))
            col = (SVET, ALYJ, ZOLOTO, "#8fd6ff")[k % 4]
            g += (f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="{7:.0f}" fill="{col}"'
                  f' opacity="{gor:.2f}"/>')
            g += (f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="{20:.0f}" fill="{col}"'
                  f' opacity="{gor*.22:.2f}"/>')
    if zvezda:
        pul = .9 + .1 * A.w(t, 2.2)
        g += f'<g transform="translate(0,-470) scale({pul:.3f})">{_zvezda(0, 0, 44, ZOLOTO)}</g>'
        g += teplo(0, -470, 150, 150, .5)
    g += '</g>'
    return g


def _zvezda(cx, cy, r, col=ZOLOTO, luchey=5):
    p = []
    for i in range(luchey * 2):
        a = -math.pi / 2 + i * math.pi / luchey
        rr = r if i % 2 == 0 else r * .44
        p.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return f'<polygon points="{" ".join(p)}" fill="{col}" {o(5)}/>'


def girlyanda(x1, y1, x2, y2, t, n=12, prov=90, ph=0.0):
    """Провисающая гирлянда лампочек: сама нить качается, огни мигают."""
    g = ""
    kach = 7 * A.w(t, 3.4, ph)
    g += (f'<path d="M{x1:.0f},{y1:.0f} Q{(x1+x2)/2:.0f},{(y1+y2)/2 + prov + kach:.0f}'
          f' {x2:.0f},{y2:.0f}" fill="none" stroke="#3b3b3b" stroke-width="5"/>')
    for i in range(n):
        u = (i + .5) / n
        bx = (1 - u) ** 2 * x1 + 2 * (1 - u) * u * (x1 + x2) / 2 + u * u * x2
        by = ((1 - u) ** 2 * y1 + 2 * (1 - u) * u * ((y1 + y2) / 2 + prov + kach)
              + u * u * y2)
        col = (SVET, ALYJ, "#8fd6ff", ZOLOTO)[i % 4]
        gor = .35 + .65 * (0.5 + 0.5 * math.sin(2 * math.pi * (t / 1.9 + i * .23 + ph)))
        g += f'<path d="M{bx:.0f},{by:.0f} v10" fill="none" stroke="#3b3b3b" stroke-width="4"/>'
        g += f'<circle cx="{bx:.0f}" cy="{by + 20:.0f}" r="10" fill="{col}" opacity="{gor:.2f}" {o(3)}/>'
        g += f'<circle cx="{bx:.0f}" cy="{by + 20:.0f}" r="26" fill="{col}" opacity="{gor*.2:.2f}"/>'
    return g


def flazhki(x, y, w_, n, t, podpisi=None, ph=0.0):
    """Гирлянда флажков — памятка ролика: под каждым встаёт карточка.
    Подписи короткие, одно-два слова; длинный текст кладёт над ними over."""
    g = ""
    kach = 6 * A.w(t, 3.0, ph)
    g += (f'<path d="M{x:.0f},{y:.0f} Q{x + w_/2:.0f},{y + 54 + kach:.0f} {x + w_:.0f},{y:.0f}"'
          f' fill="none" stroke="#4a3c2c" stroke-width="5"/>')
    for i in range(n):
        u = (i + .5) / n
        fx = (1 - u) ** 2 * x + 2 * (1 - u) * u * (x + w_ / 2) + u * u * (x + w_)
        fy = (1 - u) ** 2 * y + 2 * (1 - u) * u * (y + 54 + kach) + u * u * y
        vih = A.out(A.seg(t, .25 + i * .18, .5))
        col = (ALYJ, ZOLOTO)[i % 2]
        g += (f'<g transform="translate({fx:.0f},{fy:.0f}) scale({vih:.3f})">'
              f'<path d="M-42,0 h84 l-42,96 z" fill="{col}" {o(6)}/>')
        if podpisi and i < len(podpisi) and podpisi[i]:
            g += (f'<text x="0" y="40" text-anchor="middle" font-family="DejaVu Serif"'
                  f' font-size="34" font-weight="bold" fill="#241b14">{podpisi[i]}</text>')
        g += '</g>'
    return g


def kuranty(x, y, t, s_=1.0, k_polnochi=None, boy=False):
    """Часы с циферблатом: стрелки идут к двенадцати. `k_polnochi` 0..1 —
    доля пути до полуночи; без него стрелки живут своим ходом."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 128, 118, 22, .5)
    g += f'<circle r="120" fill="url(#zol)" {o(9)}/>'
    g += f'<circle r="100" fill="#faf3e0" {o(5)}/>'
    for i in range(12):
        a = i * math.pi / 6
        g += (f'<line x1="{84*math.sin(a):.1f}" y1="{-84*math.cos(a):.1f}"'
              f' x2="{94*math.sin(a):.1f}" y2="{-94*math.cos(a):.1f}" {o(5)}/>')
    k = k_polnochi if k_polnochi is not None else ((t / 9.0) % 1.0)
    am = 2 * math.pi * (.82 + .18 * A.ease(k))
    ah = 2 * math.pi * (.90 + .10 * A.ease(k))
    g += (f'<line x1="0" y1="0" x2="{56*math.sin(ah):.1f}" y2="{-56*math.cos(ah):.1f}" {o(10)}/>')
    g += (f'<line x1="0" y1="0" x2="{86*math.sin(am):.1f}" y2="{-86*math.cos(am):.1f}" {o(7)}/>')
    sek = 2 * math.pi * ((t * .9) % 1.0)
    g += (f'<line x1="0" y1="0" x2="{88*math.sin(sek):.1f}" y2="{-88*math.cos(sek):.1f}"'
          f' fill="none" stroke="{ALYJ}" stroke-width="4"/>')
    g += f'<circle r="9" fill="{CHUGUN}"/>'
    if boy:
        pul = .5 + .5 * A.w(t, .8)
        g += teplo(0, 0, 230, 230, .35 * pul)
    g += '</g>'
    return g


# ═══════════════════ ПРЕДМЕТЫ ПРАЗДНИКА ═══════════════════

def mandarin(x, y, s_=1.0, ochischen=0.0, t=0.0):
    """Мандарин. `ochischen` 0..1 — доля снятой кожуры, она ложится рядом."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(4, 42, 46, 12, .45)
    g += f'<circle r="42" fill="{MANDA}" {o(6)}/>'
    g += f'<circle cx="-14" cy="-16" r="12" fill="#ffc07a" opacity=".6"/>'
    g += f'<path d="M0,-42 q10,-14 24,-12" fill="none" stroke="{ZEL}" stroke-width="7" stroke-linecap="round"/>'
    if ochischen > .01:
        for i in range(3):
            a = -.6 + i * .6
            g += (f'<path d="M{54+i*26:.0f},26 q22,-28 44,-6 q-18,26 -44,6 z"'
                  f' fill="{MANDA}" {o(5)} opacity="{min(1.0, ochischen*1.4):.2f}"'
                  f' transform="rotate({a*30:.0f},{66+i*26:.0f},20)"/>')
    g += '</g>'
    return g


def bokal(x, y, t, s_=1.0, ph=0.0, polnyy=.6, igristoe=True):
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 8, 42, 10, .4)
    g += f'<path d="M-34,-150 h68 q-2,70 -34,92 q-32,-22 -34,-92 z" fill="{STEKLO}" opacity=".5" {o(5)}/>'
    g += f'<path d="M0,-58 v52" fill="none" {o(6)}/><path d="M-30,-4 h60" fill="none" {o(7)}/>'
    yv = -150 + 92 * (1 - polnyy)
    g += (f'<path d="M{-33 + (92-(-yv))*0:.0f},{yv:.0f} h66 q-4,{-yv-58:.0f} -33,{-yv-58+14:.0f}'
          f' q-29,-14 -33,{-yv-58:.0f} z" fill="url(#zol)" opacity=".75"/>')
    if igristoe:
        for i in range(7):
            u = ((t * .5 + i * .14) % 1.0)
            g += (f'<circle cx="{-18 + (i*7) % 36:.0f}" cy="{yv + 40 - 56*u:.0f}" r="3"'
                  f' fill="#fff" opacity="{(1-u)*.8:.2f}"/>')
    g += '</g>'
    return g


def konfetti(t, n=40, seed=9, op=.9, sp=1.0):
    """Конфетти через весь кадр — только праздничные планы (ставить редко)."""
    r = random.Random(seed)
    s = ""
    for i in range(n):
        x0 = r.uniform(0, W); per = r.uniform(5.5, 11.0) / sp; ph = r.random()
        u = ((t / per) + ph) % 1.0
        y = -60 + u * (H + 120)
        x = x0 + 70 * math.sin(2 * math.pi * (u * 2 + ph))
        col = (ALYJ, ZOLOTO, "#8fd6ff", "#f3f0e6")[i % 4]
        a = (t * 220 + i * 37) % 360
        s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="14" height="22" rx="3" fill="{col}"'
              f' opacity="{op:.2f}" transform="rotate({a:.0f},{x:.0f},{y:.0f})"/>')
    return s


def stol_prazdnik(x, y, w_, t, skatert=True, seed=5):
    """Накрытый стол: скатерть, блюда пятнами, свеча и бокал. Предметы —
    силуэтами, без мелкой кухни: кадр должен читаться на телефоне."""
    g = ""
    g += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="34" rx="10" fill="url(#derev)" {o(7)}/>'
    if skatert:
        g += (f'<path d="M{x-20:.0f},{y:.0f} h{w_+40:.0f} v34 q{-w_/2:.0f},26 {-w_-40:.0f},0 z"'
              f' fill="url(#rush)" {o(6)}/>')
        g += (f'<path d="M{x-20:.0f},{y+34:.0f} q{w_/2:.0f},26 {w_+40:.0f},0" fill="none"'
              f' stroke="{ALYJ}" stroke-width="6" opacity=".7"/>')
    g += ten(x + w_ / 2, y + 96, w_ * .52, 26, .5)
    return g


def loshad(x, base, t, s_=1.0, ph=0.0, op=1.0, bet_kopytom=True):
    """ОГНЕННАЯ ЛОШАДЬ — уходящая хозяйка 2026 года. Рыжая, грива горит и
    колышется, копыто бьёт по доскам, из ноздрей идёт пар. Появляется там,
    где текст говорит «год лошади ещё здесь» — и уступает место козе."""
    RYZH, RYZH2 = "#c2622a", "#8c3f18"
    s = s_
    kach = 2.4 * s * A.w(t, 2.1, ph)
    g = f'<g transform="translate({x:.1f},{base:.1f}) scale({s:.3f})" opacity="{op:.2f}">'
    g += ten(0, 6, 186, 29, .5)
    bit = max(0.0, math.sin(2 * math.pi * (t / 1.7 + ph))) ** 3 if bet_kopytom else 0.0
    for nx, dl, col, bej in ((-112, 0.0, RYZH2, False), (-66, .5, RYZH2, False),
                             (74, .5, RYZH, False), (118, 0.0, RYZH, True)):
        pod = -46 * bit if bej else 0.0
        g += (f'<path d="M{nx},-120 q6,{54 + pod*.4:.0f} 2,{108 + pod:.0f}" fill="none"'
              f' stroke="{col}" stroke-width="30" stroke-linecap="round"/>')
        g += (f'<rect x="{nx-16:.0f}" y="{-12 + pod:.0f}" width="34" height="19" rx="6"'
              f' fill="{CHUGUN}" {o(4)}/>')
    g += (f'<g transform="translate(0,{kach:.1f})">'
          f'<path d="M-166,-210 q-10,-96 70,-118 q104,-28 190,4 q74,26 64,110'
          f' q-10,74 -84,88 q-116,22 -196,0 q-48,-14 -44,-84 z" fill="{RYZH}" {o(9)}/>'
          f'<path d="M-140,-278 q96,-26 182,-4" fill="none" stroke="#e58a4a"'
          f' stroke-width="16" stroke-linecap="round" opacity=".5"/></g>')
    # хвост огнём
    for i in range(6):
        hv = 30 * A.w(t, 1.0 + i * .13, ph + i * .17)
        col = (UGOL, ORA, SVET, "#ffdca0", ORA, SVET)[i]
        g += (f'<path d="M-168,-262 q{-70+hv:.0f},46 {-86+hv*1.7:.0f},150" fill="none"'
              f' stroke="{col}" stroke-width="{26 - i*3}" stroke-linecap="round"'
              f' opacity="{.9 - i*.09:.2f}"/>')
    g += teplo(-230, -170, 190, 210, .35)
    # шея и голова
    nak = 3.6 * A.w(t, 2.6, ph + .4)
    g += f'<g transform="translate(176,{-286+kach:.1f}) rotate({nak:.2f})">'
    g += f'<path d="M-40,66 q22,-96 72,-150" fill="none" stroke="{RYZH}" stroke-width="62" stroke-linecap="round"/>'
    g += (f'<path d="M6,-178 q54,-26 104,16 q40,32 52,76 q6,22 -22,28'
          f' q-48,10 -92,-12 q-48,-26 -46,-62 z" fill="{RYZH}" {o(9)}/>')
    g += f'<ellipse cx="2" cy="-186" rx="16" ry="34" fill="{RYZH2}" {o(6)} transform="rotate(-16,2,-186)"/>'
    if not A.blink(t, 4.7, ph):
        g += '<ellipse cx="66" cy="-146" rx="12" ry="13" fill="#17100e"/>'
        g += '<circle cx="70" cy="-150" r="4.5" fill="#fff" opacity=".85"/>'
    g += '<circle cx="146" cy="-96" r="7" fill="#4a1a10"/>'
    # ГРИВА огнём — главный живой элемент
    g += f'<ellipse cx="22" cy="-196" rx="17" ry="38" fill="{RYZH2}" {o(6)} transform="rotate(-10,22,-196)"/>'
    for i in range(9):
        u = i / 8.0
        gx = -46 + u * 150
        gy = -168 + u * 16
        koleb = 26 * A.w(t, .8 + i * .09, ph + i * .17)
        col = (UGOL, ORA, SVET, "#ffd27a", ORA, "#ffe6b0", SVET, ORA, UGOL)[i]
        g += (f'<path d="M{gx:.0f},{gy:.0f} q{-48+koleb:.0f},{-66:.0f} {-26+koleb*1.5:.0f},{-132:.0f}"'
              f' fill="none" stroke="{col}" stroke-width="{24 - i*1.6:.0f}" stroke-linecap="round"'
              f' opacity="{.92 - i*.05:.2f}"/>')
    g += teplo(40, -150, 240, 200, .42)
    # пар из ноздрей
    for i in range(3):
        k = ((t * .5 + i * .33) % 1.0)
        g += (f'<ellipse cx="{156 + 60*k:.0f}" cy="{-92 - 26*k:.0f}" rx="{14 + 40*k:.0f}"'
              f' ry="{(14 + 40*k)*.6:.0f}" fill="#f0e2d2" opacity="{.5*(1-k)*(1-k):.2f}"/>')
    g += '</g></g>'
    return g
