# -*- coding: utf-8 -*-
"""СКВОЗНЫЕ ОБРАЗЫ РОЛИКА «В чём встречать Новый год 2027».

Ролик о нарядах, и почти весь его предметный мир — это вещи, которых в
прошлых роликах проекта не было вовсе: портновский манекен, плечики, штанга
вешалки, раскрытый шкаф, трюмо, отрез ткани, бирка, коробка с туфлями,
гирлянда. Они собраны здесь, чтобы 122 декорации не повторяли друг друга
кодом и чтобы оттенки нарядов задавались В ОДНОМ МЕСТЕ.

ПОЧЕМУ НАРЯДЫ НА МАНЕКЕНАХ, А НЕ НА ЛЮДЯХ: так решила раскадровка, и это
прямо помогает R-0051 — у манекена рук нет вовсе, третьей руке взяться
неоткуда, а наряд виден целиком, от выреза до подола.

ОТТЕНКИ — ГЛАВНОЕ ТРЕБОВАНИЕ ЭТОГО РОЛИКА (первая строка таблицы): алый,
рубиновый, винный, коралловый, терракотовый, изумрудный, тёмно-синий обязаны
читаться РАЗНЫМИ. Поэтому они заданы именами ниже и в сценах берутся только
отсюда — иначе «красный» расползётся по семи сценам одним пятном.

Механика двух проходов (учёт рук, R-0051) лежит в каркасном `anat.py`.
"""
import math, random
from baza import *
import anim as A
from anat import (pervyy_prohod, zapomnit_ruku, ruki_na_pleche, uchest_figuru)


# ── ОТТЕНКИ НАРЯДОВ: семь обязательных и их спутники ──────────────────────
ALYY      = "#d81f2a"   # алый — чистый красный, как мак
RUBIN     = "#9e1230"   # рубиновый — тёмный с синевой, как камень в перстне
VINO      = "#6d1028"   # винный — ещё темнее и глуше, как вишня
KORALL    = "#e8674f"   # коралловый — красный с оранжевым, как бусы
TERRAKOT  = "#b4542e"   # терракотовый — обожжённая глина
IZUMRUD   = "#0f6b4a"   # изумрудный
HVOYA     = "#1d4536"   # тёмно-зелёный, хвойный
TSINIY    = "#1b2a52"   # тёмно-синий
LAVANDA   = "#9b8fc0"
PUDRA     = "#e3bfb4"
MOLOKO    = "#f2ece0"
KREM2     = "#e8d9bd"
BEZH      = "#cbb496"
SERYY     = "#8b8b90"
GRAFIT    = "#2e3238"
ZOLOTO    = "#d8b046"
SEREBRO   = "#c9ced6"
DEREVO    = "#6b4a2f"
DEREVO2   = "#8a6440"

# Гамма ролика по каналу — новогодняя: тёплый свет ламп, холодная улица.
TEPLO_SVET = "#ffd98a"
HOLOD_KANT = "#cfe4f5"


def tkan_blesk(x, y, w_, h_, t, col, sila=.35, ph=.0):
    """Блик, бегущий по ткани: он и отличает атлас от матовой ткани.

    Его правило этого ролика: «блестит что-то одно» — поэтому сила блика
    задаётся сценой, а не ставится одинаковой везде.
    """
    p = (A.w(t, 3.4, ph) + 1) / 2
    bx = x - w_ * .3 + w_ * 1.6 * p
    return (f'<rect x="{bx-w_*.16:.0f}" y="{y:.0f}" width="{w_*.32:.0f}"'
            f' height="{h_:.0f}" fill="{col}" opacity="{sila*.5:.2f}"'
            f' transform="skewX(-9)"/>')


def skladki(x, y, w_, h_, col, n=6, seed=3, t=0.0, amp=5.0):
    """Складки ткани: без них любой наряд читается плоским пятном."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        fx = x + w_ * (i + .5) / n + amp * A.w(t, 2.2 + .3 * i, i * .2)
        gl = h_ * rnd.uniform(.55, .95)
        s += (f'<path d="M{fx:.0f},{y:.0f} q{rnd.uniform(-10,10):.0f},{gl*.5:.0f}'
              f' {rnd.uniform(-14,14):.0f},{gl:.0f}" fill="none" stroke="{K}"'
              f' stroke-width="{max(2, h_*.012):.1f}" opacity=".22"/>')
        s += (f'<path d="M{fx+6:.0f},{y:.0f} q{rnd.uniform(-10,10):.0f},{gl*.5:.0f}'
              f' {rnd.uniform(-14,14):.0f},{gl:.0f}" fill="none" stroke="#ffffff"'
              f' stroke-width="{max(1.5, h_*.008):.1f}" opacity=".14"/>')
    return s


def otrez(x, y, w_, h_, col, t, seed=4, blesk=.0, ph=.0):
    """Отрез ткани: полотно со складками, по желанию с бегущим бликом.

    Лежит в витрине, на прилавке, на столе — сквозной предмет ролика.
    """
    s = (f'<path d="M{x:.0f},{y:.0f} h{w_:.0f} v{h_:.0f}'
         f' q{-w_*.5:.0f},{h_*.06:.0f} {-w_:.0f},0 Z" fill="{col}" {o(6)}/>')
    s += skladki(x, y, w_, h_, col, max(4, int(w_ // 90)), seed, t)
    if blesk > 0:
        s += tkan_blesk(x, y, w_, h_, t, "#ffffff", blesk, ph)
    s += (f'<path d="M{x:.0f},{y+h_*.03:.0f} q{w_*.5:.0f},{h_*.05:.0f} {w_:.0f},0"'
          f' fill="none" stroke="#ffffff" stroke-width="2" opacity=".18"/>')
    return s


def plechiki(x, y, s_=1.0, col="#7a5a3a", t=0.0, ph=.0, kach=2.2):
    """Деревянные плечики с крючком. Качаются — это живое движение сцены."""
    w_ = 150 * s_
    a = kach * A.w(t, 2.6, ph)
    s = f'<g transform="rotate({a:.2f} {x:.0f} {y-52*s_:.0f})">'
    s += (f'<path d="M{x:.0f},{y-52*s_:.0f} q0,{-22*s_:.0f} {14*s_:.0f},{-22*s_:.0f}'
          f' q{14*s_:.0f},0 {14*s_:.0f},{18*s_:.0f}" fill="none" stroke="{SEREBRO}"'
          f' stroke-width="{max(3, 5*s_):.1f}"/>')
    s += (f'<path d="M{x-w_*.5:.0f},{y:.0f} q{w_*.5:.0f},{-30*s_:.0f} {w_:.0f},0"'
          f' fill="none" stroke="{col}" stroke-width="{max(5, 11*s_):.1f}"'
          f' stroke-linecap="round"/>')
    s += (f'<path d="M{x-w_*.5:.0f},{y:.0f} h{w_:.0f}" fill="none" stroke="{col}"'
          f' stroke-width="{max(3, 6*s_):.1f}" opacity=".75"/>')
    s += "</g>"
    return s


def naryad_plechiki(x, y, h_, t, col, s_=1.0, ph=.0, platye=True,
                    vorot=None, blesk=.0, seed=5, kach=2.2):
    """Наряд НА ПЛЕЧИКАХ: платье или пиджак висят и чуть качаются.

    Это второй по частоте предмет ролика после манекена. Платье — трапеция
    от плеч до подола, пиджак — прямой силуэт с бортами и лацканами.
    """
    w_ = h_ * (.62 if platye else .70)
    a = kach * A.w(t, 2.6, ph)
    s = f'<g transform="rotate({a:.2f} {x:.0f} {y:.0f})">'
    s += plechiki(x, y, s_, "#7a5a3a", 0.0)
    pl = y + h_ * .03
    pod = y + h_
    if platye:
        s += (f'<path d="M{x-w_*.30:.0f},{pl:.0f} q{w_*.30:.0f},{-h_*.055:.0f} {w_*.60:.0f},0'
              f' L{x+w_*.52:.0f},{pod:.0f} q{-w_*.52:.0f},{h_*.05:.0f} {-w_*1.04:.0f},0 Z"'
              f' fill="{col}" {o(6)}/>')
    else:
        s += (f'<path d="M{x-w_*.34:.0f},{pl:.0f} h{w_*.68:.0f} l{w_*.05:.0f},{h_*.92:.0f}'
              f' h{-w_*.78:.0f} Z" fill="{col}" {o(6)}/>')
        for sgn in (-1, 1):
            s += (f'<path d="M{x+sgn*4:.0f},{pl+h_*.02:.0f} l{sgn*w_*.17:.0f},{h_*.10:.0f}'
                  f' l{-sgn*w_*.05:.0f},{h_*.14:.0f} Z" fill="{col}"'
                  f' stroke="{K}" stroke-width="3" opacity=".88"/>')
        s += (f'<path d="M{x:.0f},{pl+h_*.26:.0f} v{h_*.66:.0f}" stroke="{K}"'
              f' stroke-width="3" opacity=".5"/>')
    s += skladki(x - w_ * .42, pl + h_ * .12, w_ * .84, h_ * .80, col,
                 max(4, int(h_ // 110)), seed, t, 3.0)
    if vorot:
        s += (f'<ellipse cx="{x:.0f}" cy="{pl+h_*.015:.0f}" rx="{w_*.21:.0f}"'
              f' ry="{h_*.035:.0f}" fill="{vorot}" {o(4)}/>')
    if blesk > 0:
        s += tkan_blesk(x - w_ * .5, pl, w_, h_ * .95, t, "#ffffff", blesk, ph)
    s += "</g>"
    return s


def manekken(x, y, h_, t, col=KREM2, pol="zh", naryad=None, ph=.0,
             vorot=None, blesk=.0, seed=7, podol=True):
    """ПОРТНОВСКИЙ МАНЕКЕН — главный герой ролика.

    `pol="zh"` — женский на стойке с круглым основанием, талия забрана;
    `pol="m"` — мужской торс-плечи без талии, на треноге.
    `naryad` — цвет наряда; None оставляет сам манекен (бежевое полотно).
    `y` — уровень ПОЛА, `h_` — высота всей стойки с манекеном.

    Манекен дышит: едва заметное колебание, чтобы кадр не замирал (R-0006).
    """
    dy = 1.8 * A.w(t, .9, ph)
    tors_h = h_ * (.52 if pol == "zh" else .44)
    tors_w = h_ * (.26 if pol == "zh" else .30)
    verh = y - h_
    s = f'<g transform="translate(0,{dy:.1f})">'
    s += ten(x, y + 6, tors_w * .95, h_ * .018, .45)
    # стойка
    s += (f'<rect x="{x-5:.0f}" y="{verh+tors_h:.0f}" width="10"'
          f' height="{h_-tors_h:.0f}" fill="{SEREBRO}" {o(4)}/>')
    if pol == "zh":
        s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{h_*.11:.0f}"'
              f' ry="{h_*.022:.0f}" fill="{SEREBRO}" {o(5)}/>')
    else:
        for sgn in (-1, 0, 1):
            s += (f'<path d="M{x:.0f},{y-h_*.16:.0f} l{sgn*h_*.10:.0f},{h_*.16:.0f}"'
                  f' stroke="{SEREBRO}" stroke-width="7" stroke-linecap="round"/>')
    # торс
    telo = naryad or col
    if pol == "zh":
        put = (f'M{x-tors_w*.52:.0f},{verh+tors_h*.12:.0f}'
               f' q{tors_w*.52:.0f},{-tors_h*.17:.0f} {tors_w*1.04:.0f},0'
               f' q{tors_w*.10:.0f},{tors_h*.34:.0f} {-tors_w*.22:.0f},{tors_h*.50:.0f}'
               f' q{tors_w*.30:.0f},{tors_h*.22:.0f} {tors_w*.16:.0f},{tors_h*.38:.0f}'
               f' h{-tors_w*1.92:.0f}'
               f' q{-tors_w*.14:.0f},{-tors_h*.16:.0f} {tors_w*.16:.0f},{-tors_h*.38:.0f}'
               f' q{-tors_w*.32:.0f},{-tors_h*.16:.0f} {-tors_w*.22:.0f},{-tors_h*.50:.0f} Z')
    else:
        put = (f'M{x-tors_w*.54:.0f},{verh+tors_h*.14:.0f}'
               f' q{tors_w*.54:.0f},{-tors_h*.20:.0f} {tors_w*1.08:.0f},0'
               f' l{tors_w*.06:.0f},{tors_h*.86:.0f} h{-tors_w*1.26:.0f} Z')
    s += f'<path d="{put}" fill="{telo}" {o(6)}/>'
    # вырез горловины — без него торс читается мешком
    s += (f'<path d="M{x-tors_w*.26:.0f},{verh+tors_h*.05:.0f}'
          f' q{tors_w*.26:.0f},{tors_h*.14:.0f} {tors_w*.52:.0f},0"'
          f' fill="none" stroke="{K}" stroke-width="4" opacity=".65"/>')
    if vorot:
        s += (f'<path d="M{x-tors_w*.30:.0f},{verh+tors_h*.03:.0f}'
              f' q{tors_w*.30:.0f},{tors_h*.17:.0f} {tors_w*.60:.0f},0"'
              f' fill="none" stroke="{vorot}" stroke-width="{max(6, tors_w*.11):.0f}"'
              f' stroke-linecap="round"/>')
    if naryad and podol:
        # юбка/пола наряда ниже торса: наряд виден целиком, а не «по пояс»
        yl = verh + tors_h
        s += (f'<path d="M{x-tors_w*.60:.0f},{yl-tors_h*.06:.0f}'
              f' L{x-tors_w*.95:.0f},{yl+h_*.30:.0f}'
              f' q{tors_w*.95:.0f},{h_*.045:.0f} {tors_w*1.90:.0f},0'
              f' L{x+tors_w*.60:.0f},{yl-tors_h*.06:.0f} Z" fill="{naryad}" {o(6)}/>')
        s += skladki(x - tors_w * .86, yl, tors_w * 1.72, h_ * .30, naryad, 6, seed, t, 3.5)
    s += skladki(x - tors_w * .46, verh + tors_h * .18, tors_w * .92,
                 tors_h * .72, telo, 4, seed + 1, t, 2.0)
    if blesk > 0:
        s += tkan_blesk(x - tors_w * .6, verh + tors_h * .1, tors_w * 1.2,
                        tors_h * .9, t, "#ffffff", blesk, ph)
    s += "</g>"
    return s


def shtanga(x, y, w_, t, vysota=430, nog=True):
    """Напольная вешалка-штанга: перекладина на стойках, на неё вешают наряды."""
    s = ""
    for sgn in (-1, 1):
        sx = x + sgn * w_ * .5
        s += (f'<rect x="{sx-5:.0f}" y="{y-vysota:.0f}" width="10" height="{vysota:.0f}"'
              f' fill="{SEREBRO}" {o(4)}/>')
        if nog:
            s += (f'<path d="M{sx-70:.0f},{y:.0f} h140" stroke="{SEREBRO}"'
                  f' stroke-width="9" stroke-linecap="round"/>')
            s += ten(sx, y + 5, 74, 9, .4)
    s += (f'<rect x="{x-w_*.5:.0f}" y="{y-vysota:.0f}" width="{w_:.0f}" height="11"'
          f' rx="5" fill="{SEREBRO}" {o(4)}/>')
    return s


def perekladina(x, y, w_, col=SEREBRO):
    """Перекладина внутри шкафа — короткая штанга без стоек."""
    return (f'<rect x="{x-w_*.5:.0f}" y="{y:.0f}" width="{w_:.0f}" height="12"'
            f' rx="6" fill="{col}" {o(4)}/>'
            f'<rect x="{x-w_*.5:.0f}" y="{y+3:.0f}" width="{w_:.0f}" height="4"'
            f' fill="#ffffff" opacity=".25"/>')


def shkaf(x, y, w_, h_, t, raskryt=1.0, zerkalo_v_dverce=False, nutro="#2a211b"):
    """Шкаф: корпус, задняя стенка, раскрытая створка, перекладина.

    `raskryt` 0..1 — насколько отведена створка. Возвращает ТОЛЬКО корпус;
    то, что висит внутри, сцена рисует сама между корпусом и створкой.
    """
    s = (f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' fill="{nutro}" {o(7)}/>')
    s += (f'<rect x="{x+10:.0f}" y="{y-h_+10:.0f}" width="{w_-20:.0f}"'
          f' height="{h_-20:.0f}" fill="url(#derev)" opacity=".30"/>')
    # боковины дают объём
    s += (f'<path d="M{x:.0f},{y-h_:.0f} l26,22 v{h_-44:.0f} l-26,22 Z"'
          f' fill="#1b1512" opacity=".55"/>')
    ug = -46 * raskryt
    s += (f'<g transform="rotate({ug:.1f} {x+w_:.0f} {y-h_*.5:.0f})">'
          f'<rect x="{x+w_-14:.0f}" y="{y-h_:.0f}" width="{w_*.46:.0f}"'
          f' height="{h_:.0f}" fill="url(#derev)" {o(7)}/>')
    if zerkalo_v_dverce:
        s += (f'<rect x="{x+w_+16:.0f}" y="{y-h_+40:.0f}" width="{w_*.46-60:.0f}"'
              f' height="{h_-80:.0f}" fill="{STEKLO}" opacity=".55" {o(5)}/>')
    s += (f'<circle cx="{x+w_+w_*.40:.0f}" cy="{y-h_*.5:.0f}" r="9"'
          f' fill="{ZOLOTO}" {o(3)}/></g>')
    return s


def zerkalo(x, y, w_, h_, t, forma="pryam", rama=ZOLOTO, blik_=True):
    """РАМА зеркала: кладётся ПОВЕРХ того, что в зеркале отражается.

    Порядок в сцене строгий (опора 14.11): сначала рисованное отражение или
    метка настоящего кадра, потом эта рама и блик — иначе кадр выглядит
    наклейкой поверх сцены, а не отражением в стекле.
    """
    if forma == "ellips":
        s = (f'<ellipse cx="{x+w_*.5:.0f}" cy="{y+h_*.5:.0f}" rx="{w_*.5:.0f}"'
             f' ry="{h_*.5:.0f}" fill="none" stroke="{rama}"'
             f' stroke-width="{max(10, w_*.045):.0f}"/>')
    else:
        s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
             f' fill="none" stroke="{rama}" stroke-width="{max(10, w_*.035):.0f}"/>')
    s += (f'<rect x="{x+6:.0f}" y="{y+6:.0f}" width="{w_-12:.0f}" height="{h_-12:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="2" opacity=".25"/>')
    if blik_:
        p = (A.w(t, 5.2, .2) + 1) / 2
        bx = x + w_ * (.12 + .62 * p)
        s += (f'<path d="M{bx:.0f},{y+10:.0f} l{w_*.14:.0f},0 l{-w_*.26:.0f},{h_-20:.0f}'
              f' l{-w_*.14:.0f},0 Z" fill="#ffffff" opacity=".10"/>')
    return s


def trumo(x, y, w_, h_, t):
    """Трюмо: столик с зеркалом и двумя створками — сквозная мебель ролика."""
    s = (f'<rect x="{x:.0f}" y="{y-h_*.34:.0f}" width="{w_:.0f}" height="{h_*.12:.0f}"'
         f' rx="8" fill="url(#derev)" {o(6)}/>')
    for sgn in (-1, 1):
        nx = x + (w_ * .12 if sgn < 0 else w_ * .80)
        s += (f'<rect x="{nx:.0f}" y="{y-h_*.22:.0f}" width="{w_*.08:.0f}"'
              f' height="{h_*.22:.0f}" fill="{DEREVO}" {o(4)}/>')
    s += ten(x + w_ * .5, y + 4, w_ * .52, 12, .4)
    return s


def birka(x, y, s_=1.0, t=0.0, col=MOLOKO, ph=.0):
    """Бирка-ярлык на нитке: на ней держится памятка ролика (пять бирок)."""
    a = 4.0 * A.w(t, 2.9, ph)
    w_, h_ = 96 * s_, 62 * s_
    s = f'<g transform="rotate({a:.2f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x:.0f},{y:.0f} l0,{-26*s_:.0f}" stroke="{BEZH}"'
          f' stroke-width="{max(2, 3*s_):.1f}"/>')
    s += (f'<path d="M{x-w_*.5:.0f},{y:.0f} h{w_:.0f} v{h_:.0f} h{-w_:.0f} Z"'
          f' fill="{col}" {o(4)}/>')
    s += (f'<circle cx="{x:.0f}" cy="{y+h_*.16:.0f}" r="{6*s_:.1f}" fill="none"'
          f' stroke="{K}" stroke-width="{max(1.5, 2*s_):.1f}"/>')
    s += "</g>"
    return s


def girlyanda(x, y, w_, t, n=9, seed=3, provis=48, col=None):
    """Гирлянда: провод провисает дугой, огоньки загораются по очереди.

    Это ЖИВОЙ ОГОНЁК комнатных сцен ролика — в избе его давала печь, здесь
    даёт гирлянда и лампа. Гейт сцен знает её по имени.
    """
    rnd = random.Random(seed)
    s = (f'<path d="M{x:.0f},{y:.0f} q{w_*.5:.0f},{provis:.0f} {w_:.0f},0"'
         f' fill="none" stroke="#3b3b3b" stroke-width="4"/>')
    for i in range(n):
        p = (i + .5) / n
        gx = x + w_ * p
        gy = y + provis * .5 * (1 - (2 * p - 1) ** 2) * 2
        fase = (t * 1.6 + i * .37) % 1.0
        yar = .35 + .65 * (0.5 + 0.5 * math.cos(2 * math.pi * fase))
        c = col or rnd.choice(("#ffd36b", "#ff8f6b", "#8fd6ff", "#9bf0a8", "#ffffff"))
        s += (f'<circle cx="{gx:.0f}" cy="{gy+12:.0f}" r="{8:.0f}" fill="{c}"'
              f' opacity="{yar:.2f}"/>')
        s += (f'<circle cx="{gx:.0f}" cy="{gy+12:.0f}" r="{20:.0f}" fill="{c}"'
              f' opacity="{yar*.22:.2f}"/>')
        s += (f'<path d="M{gx:.0f},{gy:.0f} l0,10" stroke="#3b3b3b" stroke-width="3"/>')
    return s


def elka(x, base, h_, t, s_=1.0, ogonki=True, seed=5):
    """Ёлка углом кадра: три яруса хвои, звезда, огоньки.

    В этом ролике ёлка — не главный предмет, а знак праздника на втором
    плане; главным остаётся наряд (R-0047: крупный предмет — один).
    """
    rnd = random.Random(seed)
    w_ = h_ * .62
    s = (f'<rect x="{x-14*s_:.0f}" y="{base-h_*.08:.0f}" width="{28*s_:.0f}"'
         f' height="{h_*.08:.0f}" fill="{DEREVO}" {o(4)}/>')
    for i, k in enumerate((1.0, .74, .48)):
        yv = base - h_ * (.08 + .30 * i)
        yn = yv - h_ * .34
        s += (f'<path d="M{x:.0f},{yn:.0f} L{x-w_*.5*k:.0f},{yv:.0f}'
              f' q{w_*.5*k:.0f},{h_*.04:.0f} {w_*k:.0f},0 Z" fill="{HVOYA}" {o(6)}/>')
        for j in range(6):
            lx = x - w_ * .45 * k + w_ * .9 * k * rnd.random()
            s += (f'<path d="M{lx:.0f},{yv-h_*.04:.0f} l{rnd.uniform(-12,12):.0f},{-18:.0f}"'
                  f' stroke="#2c5f44" stroke-width="4" opacity=".8"/>')
    zv = base - h_ * 1.06
    mig = .7 + .3 * abs(A.w(t, 2.2))
    s += (f'<path d="M{x:.0f},{zv-26:.0f} l9,20 l22,3 l-16,15 l5,22 l-20,-11 l-20,11'
          f' l5,-22 l-16,-15 l22,-3 Z" fill="{ZOLOTO}" opacity="{mig:.2f}" {o(3)}/>')
    if ogonki:
        for i in range(10):
            p = i / 10.0
            gx = x + (w_ * .44) * math.sin(p * 7.3) * (1 - p * .5)
            gy = base - h_ * (.12 + .84 * p)
            fase = (t * 1.4 + i * .3) % 1.0
            yar = .3 + .7 * (0.5 + 0.5 * math.cos(2 * math.pi * fase))
            s += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="7" fill="#ffd36b"'
                  f' opacity="{yar:.2f}"/>')
    return s


def koza(x, y, h_, t, ph=.0, smotrit=True):
    """ОГНЕННАЯ КОЗА — хозяйка года (R-0013): пламя в гриве и хвосте,
    рога дугой назад, живой глаз с бликом, свечение вокруг.

    Открывает и закрывает ролик. Морда в профиль: так читается силуэт козы,
    а не собаки — на прошлом ролике проекта именно это было претензией.
    """
    w_ = h_ * 1.35
    dy = 3.0 * A.w(t, 1.1, ph)
    s = f'<g transform="translate(0,{dy:.1f})">'
    s += teplo(x, y - h_ * .45, w_ * .95, h_ * .85, .40 + .10 * abs(A.w(t, 1.6)))
    s += ten(x, y + 6, w_ * .42, h_ * .035, .45)
    # ноги: две опорные впереди, две сзади — опора под ногами названа (R-0051)
    for i, (dx, zad) in enumerate(((-w_ * .26, False), (-w_ * .16, True),
                                   (w_ * .20, False), (w_ * .30, True))):
        kach = 3.0 * A.w(t, 1.8, ph + i * .25)
        s += (f'<path d="M{x+dx:.0f},{y-h_*.46:.0f} q{kach:.0f},{h_*.24:.0f}'
              f' {kach*.4:.0f},{h_*.46:.0f}" fill="none"'
              f' stroke="{"#5a3320" if zad else "#7a4426"}"'
              f' stroke-width="{h_*.075:.0f}" stroke-linecap="round"/>')
        s += (f'<ellipse cx="{x+dx+kach*.4:.0f}" cy="{y:.0f}" rx="{h_*.045:.0f}"'
              f' ry="{h_*.022:.0f}" fill="{K}"/>')
    # туловище
    s += (f'<path d="M{x-w_*.36:.0f},{y-h_*.52:.0f}'
          f' q{w_*.10:.0f},{-h_*.26:.0f} {w_*.38:.0f},{-h_*.22:.0f}'
          f' q{w_*.30:.0f},{-h_*.04:.0f} {w_*.34:.0f},{h_*.20:.0f}'
          f' q{w_*.02:.0f},{h_*.22:.0f} {-w_*.26:.0f},{h_*.24:.0f}'
          f' q{-w_*.34:.0f},{h_*.04:.0f} {-w_*.46:.0f},{-h_*.22:.0f} Z"'
          f' fill="#8a4a27" {o(7)}/>')
    # грива пламенем вдоль хребта
    for i in range(7):
        gx = x - w_ * .30 + w_ * .50 * i / 6.0
        gy = y - h_ * .74 - h_ * .03 * math.sin(i)
        s += ogon(gx, gy, t, .38 + .06 * (i % 3), ph + i * .18, 2)
    # хвост пламенем
    hv = 9 * A.w(t, 1.5, ph)
    s += (f'<path d="M{x-w_*.36:.0f},{y-h_*.62:.0f} q{-w_*.14:.0f},{-h_*.10+hv:.0f}'
          f' {-w_*.10:.0f},{-h_*.26:.0f}" fill="none" stroke="#8a4a27"'
          f' stroke-width="{h_*.06:.0f}" stroke-linecap="round"/>')
    s += ogon(x - w_ * .46, y - h_ * .88, t, .5, ph + .4, 4)
    # шея и голова в профиль
    gx, gy = x + w_ * .40, y - h_ * .92
    nak = 4.0 * A.w(t, 1.3, ph + .3)
    s += (f'<g transform="rotate({nak:.2f} {x+w_*.30:.0f} {y-h_*.66:.0f})">')
    s += (f'<path d="M{x+w_*.20:.0f},{y-h_*.68:.0f} L{gx-h_*.10:.0f},{gy+h_*.10:.0f}'
          f' l{h_*.16:.0f},{h_*.06:.0f} L{x+w_*.30:.0f},{y-h_*.56:.0f} Z"'
          f' fill="#8a4a27" {o(6)}/>')
    s += (f'<path d="M{gx-h_*.16:.0f},{gy+h_*.04:.0f}'
          f' q{h_*.10:.0f},{-h_*.14:.0f} {h_*.30:.0f},{-h_*.04:.0f}'
          f' q{h_*.12:.0f},{h_*.06:.0f} {h_*.02:.0f},{h_*.16:.0f}'
          f' q{-h_*.18:.0f},{h_*.08:.0f} {-h_*.34:.0f},{-h_*.02:.0f} Z"'
          f' fill="#9c5529" {o(6)}/>')
    # борода козы — от подбородка, а не от носа (R-0051)
    s += (f'<path d="M{gx+h_*.02:.0f},{gy+h_*.16:.0f} q{h_*.03:.0f},{h_*.16:.0f}'
          f' {-h_*.04:.0f},{h_*.22:.0f}" fill="none" stroke="#e8c27a"'
          f' stroke-width="{h_*.045:.0f}" stroke-linecap="round"/>')
    # рога дугой назад
    for sgn in (0, 1):
        s += (f'<path d="M{gx-h_*.02+sgn*h_*.05:.0f},{gy-h_*.10:.0f}'
              f' q{h_*.16:.0f},{-h_*.16:.0f} {h_*.30:.0f},{-h_*.04:.0f}"'
              f' fill="none" stroke="#e5d6b4" stroke-width="{h_*.045:.0f}"'
              f' stroke-linecap="round"/>')
    # ухо
    s += (f'<path d="M{gx-h_*.10:.0f},{gy-h_*.04:.0f} q{-h_*.14:.0f},{-h_*.06:.0f}'
          f' {-h_*.18:.0f},{h_*.06:.0f} q{h_*.08:.0f},{h_*.05:.0f} {h_*.18:.0f},{-h_*.01:.0f} Z"'
          f' fill="#7a4426" {o(4)}/>')
    # глаз с бликом и морганием
    if smotrit:
        r = 3.0 if A.blink(t, 3.6) else h_ * .030
        s += (f'<ellipse cx="{gx+h_*.06:.0f}" cy="{gy+h_*.02:.0f}" rx="{h_*.040:.0f}"'
              f' ry="{r:.1f}" fill="#f6e3b0" {o(3)}/>')
        s += (f'<ellipse cx="{gx+h_*.07:.0f}" cy="{gy+h_*.02:.0f}" rx="{h_*.016:.0f}"'
              f' ry="{min(r, h_*.022):.1f}" fill="{K}"/>')
        s += (f'<circle cx="{gx+h_*.085:.0f}" cy="{gy+h_*.005:.0f}" r="{h_*.008:.0f}"'
              f' fill="#ffffff" opacity=".9"/>')
    s += (f'<circle cx="{gx+h_*.19:.0f}" cy="{gy+h_*.09:.0f}" r="{h_*.012:.0f}"'
          f' fill="#5a2f1a"/>')
    s += "</g></g>"
    return s


def rukav(x, y, dl, ug, t, col="#2a2430", kant=HOLOD_KANT, ph=.0, amp=7.0,
          nichya=False):
    """Рукав без кисти: правило проекта — пальцев не рисуем, работает предмет.

    `nichya=True` — рука ничья: крупный план рукава там, где человека в
    кадре нет (рукав снимает плечики с перекладины). Такая рука не гасит
    рукав соседней фигуры и третьей рукой в гейте не считается (R-0051).
    """
    a = math.radians(ug + amp * A.w(t, .9, ph))
    x2, y2 = x + dl * math.cos(a), y + dl * math.sin(a)
    zapomnit_ruku(x, y, nichya)
    tol = max(14, dl * .19)
    return (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"'
            f' stroke="{col}" stroke-width="{tol:.0f}" stroke-linecap="round"/>'
            f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"'
            f' stroke="{kant}" stroke-width="3" opacity=".30"/>'
            f'<ellipse cx="{x2:.0f}" cy="{y2:.0f}" rx="{tol*.62:.0f}"'
            f' ry="{tol*.46:.0f}" fill="{col}" {o(3)}/>'), (x2, y2)


def figura(x, y, h_, t, col=TSINIY, kant=HOLOD_KANT, ph=.0, platok=False,
           profil=False, op=1.0, naklon=0.0, prichyoska=True, lico=True,
           koja="#f0cfae", platye=True, vorot=None, tufli_=True):
    """ЧЕЛОВЕК В НАРЯДНОЙ ОДЕЖДЕ — узнаваемый с первого взгляда (R-0047).

    У фигуры есть лицо (глаза с бликом и морганием, брови, нос, рот, румянец),
    причёска или платок, наряд с поясом и оторочкой, рукава и обувь.
    `platye=True` — женский силуэт с юбкой, иначе брюки.

    Кант обязателен: тёмная фигура без канта пропадает на тёмной мебели.
    Рукав НЕ рисуется на том плече, откуда сцена уже вывела свою руку через
    `rukav()` — иначе у человека три руки (R-0051).

    x, y — середина и уровень пола, h_ — полный рост.
    """
    w_ = h_ * .42
    hh = h_ * .145
    gy = y - h_ * .845
    dy = 2.6 * A.w(t, .66, ph)
    ug = naklon * A.w(t, 1.5, ph)
    plech = y - h_ * .66
    pod = y - (h_ * .07 if platye else h_ * .10)
    s = (f'<g transform="translate(0,{dy:.1f}) rotate({ug:.2f} {x:.0f} {y:.0f})"'
         f' opacity="{op:.2f}">')
    s += ten(x, y + h_ * .012, w_ * .60, h_ * .020, .45)
    # обувь
    if tufli_:
        for i in (-1, 1):
            s += (f'<path d="M{x+i*w_*.20-w_*.10:.0f},{y-h_*.055:.0f} h{w_*.20:.0f}'
                  f' q{w_*.05:.0f},{h_*.030:.0f} {-w_*.03:.0f},{h_*.055:.0f}'
                  f' h{-w_*.14:.0f} q{-w_*.05:.0f},{-h_*.018:.0f} {-w_*.03:.0f},{-h_*.055:.0f} Z"'
                  f' fill="#2b2420" stroke="{K}" stroke-width="{max(2, h_*.010):.1f}"/>')
    if platye:
        s += (f'<path d="M{x-w_*.31:.0f},{plech:.0f} q{w_*.31:.0f},{-h_*.05:.0f} {w_*.62:.0f},0'
              f' L{x+w_*.54:.0f},{pod:.0f} q{-w_*.54:.0f},{h_*.045:.0f} {-w_*1.08:.0f},0 Z"'
              f' fill="{col}" stroke="{K}" stroke-width="{max(2, h_*.012):.1f}"/>')
    else:
        s += (f'<path d="M{x-w_*.33:.0f},{plech:.0f} q{w_*.33:.0f},{-h_*.05:.0f} {w_*.66:.0f},0'
              f' l{w_*.03:.0f},{h_*.34:.0f} h{-w_*.72:.0f} Z"'
              f' fill="{col}" stroke="{K}" stroke-width="{max(2, h_*.012):.1f}"/>')
        for i in (-1, 1):
            s += (f'<path d="M{x+i*w_*.06:.0f},{plech+h_*.34:.0f}'
                  f' l{i*w_*.26:.0f},{h_*.02:.0f} l{-i*w_*.04:.0f},{h_*.24:.0f}'
                  f' h{-i*w_*.17:.0f} Z" fill="{col}" stroke="{K}"'
                  f' stroke-width="{max(2, h_*.010):.1f}"/>')
    s += skladki(x - w_ * .46, plech + h_ * .12, w_ * .92, h_ * .40, col, 4, 9, t, 2.4)
    # пояс и оторочка — без них наряд читается мешком
    s += (f'<path d="M{x-w_*.44:.0f},{y-h_*.40:.0f} q{w_*.44:.0f},{h_*.028:.0f} {w_*.88:.0f},0"'
          f' fill="none" stroke="{ZOLOTO}" stroke-width="{max(3, h_*.020):.1f}" opacity=".85"/>')
    if vorot:
        s += (f'<path d="M{x-w_*.22:.0f},{plech+h_*.01:.0f} q{w_*.22:.0f},{h_*.06:.0f} {w_*.44:.0f},0"'
              f' fill="none" stroke="{vorot}" stroke-width="{max(5, h_*.028):.1f}"'
              f' stroke-linecap="round"/>')
    # рукава: гасим тот, откуда сцена уже вывела свою руку
    _pog = 0
    for i in (-1, 1):
        rx = x + i * w_ * .39
        ry = plech + h_ * .02
        if ruki_na_pleche(rx, ry, w_ * .80, h_ * .30):
            _pog += 1
            continue
        a = i * (11 + 5 * A.w(t, 1.9, ph + (0 if i < 0 else .4)))
        s += (f'<g transform="rotate({a:.1f} {rx:.0f} {ry:.0f})">'
              f'<rect x="{rx-w_*.10:.0f}" y="{plech+h_*.01:.0f}" width="{w_*.20:.0f}"'
              f' height="{h_*.38:.0f}" rx="{w_*.10:.0f}" fill="{col}" stroke="{K}"'
              f' stroke-width="{max(2, h_*.011):.1f}"/>'
              f'<ellipse cx="{rx:.0f}" cy="{plech+h_*.40:.0f}" rx="{w_*.085:.0f}"'
              f' ry="{h_*.030:.0f}" fill="{koja}" {o(3)}/></g>')
    uchest_figuru(x, plech + h_ * .02, _pog, w_, h_)
    # шея и голова
    s += (f'<rect x="{x-w_*.07:.0f}" y="{gy+hh*.72:.0f}" width="{w_*.14:.0f}"'
          f' height="{h_*.045:.0f}" fill="{koja}" {o(3)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{gy:.0f}" rx="{hh*.80:.0f}" ry="{hh:.0f}"'
          f' fill="{koja}" stroke="{K}" stroke-width="{max(2, h_*.009):.1f}"/>')
    # УБОР РИСУЕТСЯ ДО ЛИЦА (поправлено 16.11.2026 по осмотру кадров):
    # платок и причёска шли ПОВЕРХ лица и закрывали его сплошным пятном —
    # ровно тот брак, на который он указывал («у человека нет лица»,
    # R-0047). Сначала убор, потом глаза, брови, нос и рот.
    if platok:
        s += (f'<path d="M{x-hh*.95:.0f},{gy-hh*.42:.0f} q{hh*.95:.0f},{-hh*.95:.0f}'
              f' {hh*1.90:.0f},0 q{-hh*.12:.0f},{hh*1.05:.0f} {-hh*.52:.0f},{hh*1.25:.0f}'
              f' l{-hh*.86:.0f},0 q{-hh*.40:.0f},{-hh*.20:.0f} {-hh*.52:.0f},{-hh*1.25:.0f} Z"'
              f' fill="{KORALL}" {o(4)}/>')
    elif prichyoska:
        s += (f'<path d="M{x-hh*.88:.0f},{gy-hh*.40:.0f} q{hh*.88:.0f},{-hh*1.02:.0f}'
              f' {hh*1.76:.0f},0 q{-hh*.14:.0f},{hh*.30:.0f} {-hh*.50:.0f},{hh*.16:.0f}'
              f' q{-hh*.38:.0f},{-hh*.20:.0f} {-hh*.76:.0f},0'
              f' q{-hh*.36:.0f},{hh*.14:.0f} {-hh*.50:.0f},{-hh*.16:.0f} Z"'
              f' fill="#53392a" {o(4)}/>')
    if lico and h_ >= 220:
        r = 2.2 if A.blink(t, 3.4) else hh * .11
        for i in (-1, 1):
            ex = x + i * hh * .30 + (hh * .10 if profil else 0)
            s += (f'<ellipse cx="{ex:.0f}" cy="{gy-hh*.06:.0f}" rx="{hh*.12:.0f}"'
                  f' ry="{r:.1f}" fill="#ffffff"/>')
            s += (f'<circle cx="{ex+(hh*.03 if profil else 0):.0f}" cy="{gy-hh*.06:.0f}"'
                  f' r="{min(r, hh*.06):.1f}" fill="{K}"/>')
            s += (f'<path d="M{ex-hh*.14:.0f},{gy-hh*.26:.0f} q{hh*.14:.0f},{-hh*.08:.0f}'
                  f' {hh*.28:.0f},0" fill="none" stroke="#5b4030"'
                  f' stroke-width="{max(2, hh*.05):.1f}"/>')
            s += (f'<ellipse cx="{ex+i*hh*.14:.0f}" cy="{gy+hh*.22:.0f}" rx="{hh*.17:.0f}"'
                  f' ry="{hh*.09:.0f}" fill="#d1685a" opacity=".45"/>')
        s += (f'<path d="M{x:.0f},{gy-hh*.02:.0f} l{hh*.08:.0f},{hh*.22:.0f}'
              f' l{-hh*.10:.0f},0" fill="none" stroke="{K}"'
              f' stroke-width="{max(1.5, hh*.045):.1f}" opacity=".7"/>')
        s += (f'<path d="M{x-hh*.18:.0f},{gy+hh*.45:.0f} q{hh*.18:.0f},{hh*.14:.0f}'
              f' {hh*.36:.0f},0" fill="none" stroke="#a33b3b"'
              f' stroke-width="{max(2, hh*.055):.1f}" stroke-linecap="round"/>')
    s += "</g>"
    return s


def lampa_stolika(x, y, t, s_=1.0, col=TEPLO_SVET):
    """Настольная лампа у зеркала: тёплое пятно комнатных сцен.

    Имя своё, но внутри зовёт `lampa` из базы — гейт сцен ищет живой огонёк
    именно по её имени, и сцена с одной лишь нашей обёрткой не прошла бы.
    """
    return lampa(x, y, t, s_, abazhur=True) + teplo(x, y - 40 * s_, 240 * s_,
                                                    200 * s_, .30 + .08 * abs(A.w(t, 1.9)))


def tufli(x, y, s_=1.0, col="#2b2420", t=0.0, para=True, kabluk=True):
    """Туфли-лодочки: сквозной предмет ролика, стоят парой на полу или полке."""
    s = ""
    for i in range(2 if para else 1):
        tx = x + i * 92 * s_
        s += ten(tx + 34 * s_, y + 4, 46 * s_, 8 * s_, .42)
        s += (f'<path d="M{tx:.0f},{y:.0f} q{6*s_:.0f},{-46*s_:.0f} {44*s_:.0f},{-48*s_:.0f}'
              f' q{34*s_:.0f},{2*s_:.0f} {28*s_:.0f},{34*s_:.0f}'
              f' q{-6*s_:.0f},{14*s_:.0f} {-30*s_:.0f},{14*s_:.0f} Z"'
              f' fill="{col}" {o(4)}/>')
        if kabluk:
            s += (f'<path d="M{tx+62*s_:.0f},{y-14*s_:.0f} l{5*s_:.0f},{14*s_:.0f}'
                  f' l{-7*s_:.0f},0 Z" fill="{col}" {o(3)}/>')
        s += (f'<path d="M{tx+8*s_:.0f},{y-30*s_:.0f} q{18*s_:.0f},{-10*s_:.0f}'
              f' {32*s_:.0f},{-8*s_:.0f}" fill="none" stroke="#ffffff"'
              f' stroke-width="{max(1.5, 2.4*s_):.1f}" opacity=".30"/>')
    return s


def korobka(x, y, w_, t, h_=None, otkryta=True, col="#c9b79a", bumaga=MOLOKO):
    """Обувная коробка с папиросной бумагой — предмет сцен про обувь."""
    h_ = h_ or w_ * .42
    s = ten(x + w_ * .5, y + 5, w_ * .55, 10, .4)
    s += (f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' rx="6" fill="{col}" {o(5)}/>')
    if otkryta:
        a = -16 + 3 * A.w(t, 2.4)
        s += (f'<g transform="rotate({a:.1f} {x:.0f} {y-h_:.0f})">'
              f'<rect x="{x:.0f}" y="{y-h_-22:.0f}" width="{w_*.96:.0f}" height="22"'
              f' rx="5" fill="{col}" {o(4)}/></g>')
        s += (f'<path d="M{x+w_*.12:.0f},{y-h_*.86:.0f} q{w_*.20:.0f},{-h_*.26:.0f}'
              f' {w_*.38:.0f},{-h_*.04:.0f} q{w_*.18:.0f},{h_*.20:.0f} {w_*.34:.0f},{h_*.02:.0f}"'
              f' fill="none" stroke="{bumaga}" stroke-width="{max(4, h_*.12):.0f}"'
              f' opacity=".85"/>')
    return s


def para_izo_rta(x, y, t, ph=0.0, s_=1.0, op=.5):
    """Пар изо рта — живой огонёк уличных сцен (мороз 31 декабря)."""
    return par(x, y, t, 3, op, 110 * s_, .45, .8 * s_)


def stena(vid, t, seed=3, niz=1080):
    """СТЕНА КОМНАТЫ — пять разных видов вместо одних и тех же досок.

    Поймано глазами на первом контактном листе 16.11.2026: восемь кадров из
    двенадцати шли на одинаковой бревенчато-дощатой стене, и ролик про наряды
    читался как один длинный кадр. Вид стены выбирается сценой и разводит
    эпизоды: ателье — доски, квартира — обои, кухня — крашеная панель,
    подъезд и ресторан — кладка, спальня семидесятых — ковровые обои.

    `vid`: "doski" | "oboi" | "kraska" | "kirpich" | "paneli".
    """
    rnd = random.Random(seed)
    if vid == "doski":
        return doski(0, 0, W, niz, 92)
    if vid == "kirpich":
        return kladka(0, 0, W, niz, 78)
    if vid == "oboi":
        s = f'<rect width="{W}" height="{niz}" fill="#4a3c46"/>'
        for i in range(24):
            x = i * 80
            s += (f'<rect x="{x}" y="0" width="40" height="{niz}" fill="#53444e"'
                  f' opacity=".7"/>')
        for i in range(40):
            ux = rnd.randint(20, W - 20)
            uy = rnd.randint(40, niz - 60)
            for j in range(5):
                a = j * 72
                s += (f'<ellipse cx="{ux+16*math.cos(math.radians(a)):.0f}"'
                      f' cy="{uy+16*math.sin(math.radians(a)):.0f}" rx="8" ry="12"'
                      f' fill="#6b5a66" opacity=".55"/>')
        s += (f'<rect x="0" y="{niz-40}" width="{W}" height="40" fill="{DEREVO2}"'
              f' opacity=".9"/>')
        return s
    if vid == "kraska":
        s = f'<rect width="{W}" height="{niz}" fill="#4c5a52"/>'
        s += (f'<rect x="0" y="0" width="{W}" height="{niz*.52:.0f}" fill="#5a6a60"'
              f' opacity=".9"/>')
        s += (f'<rect x="0" y="{niz*.52:.0f}" width="{W}" height="18" fill="{MOLOKO}"'
              f' opacity=".55"/>')
        for i in range(16):
            s += (f'<rect x="{i*120}" y="{niz*.56:.0f}" width="86"'
                  f' height="{niz*.40:.0f}" rx="6" fill="#44524a" opacity=".55"/>')
        s += (f'<rect x="0" y="{niz-44}" width="{W}" height="44" fill="{DEREVO2}"'
              f' opacity=".85"/>')
        return s
    # paneli
    s = f'<rect width="{W}" height="{niz}" fill="#53412f"/>'
    for i in range(int(niz // 86) + 1):
        y = i * 86
        s += (f'<rect x="0" y="{y}" width="{W}" height="78" fill="url(#derev)"'
              f' opacity="{.55 if i % 2 else .75:.2f}"/>')
        s += f'<path d="M0,{y+78} h{W}" stroke="{K}" stroke-width="3" opacity=".35"/>'
    s += (f'<rect x="0" y="{niz*.62:.0f}" width="{W}" height="16" fill="{MED}"'
          f' opacity=".7"/>')
    return s
