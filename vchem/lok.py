# -*- coding: utf-8 -*-
"""Декорации ролика «В чём встречать Новый год 2027».

Каждая — функция времени f(t) -> svg. Все нарисованы ЗАНОВО под этот текст
(R-0019): ни один кадр не взят у прошлых роликов проекта, в том числе у
похожего по названию «Как встречать 2027 год Козы» (каталог vstrechat).
Его правила 14.11: настоящий кадр лежит ВНУТРИ сцены (метка mesto_stoka),
сцены не пустые, предметы узнаваемые, в каждой сцене живой огонёк.

СОБИРАЕТСЯ sobrat_lok.py из частей — руками этот файл не правят.
"""
import math, random
from baza import *
from anat import *
import anim as A

# ═══ из lok_obshchee.py ═══
ALYY      = "#d81f2a"   # алый — чистый красный, как мак
RUBIN     = "#9e1230"   # рубиновый — тёмный с синевой, как камень в перстне
VINO      = "#6d1028"   # винный — ещё темнее и глуше, как вишня
BORDO     = "#722232"   # бордовый — коричневатый подтон, глуше рубинового и теплее винного (добавлен 17.11)
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


# ═══ из chast1.py ═══
FLOOR = 940

# ── ЛОКАЛЬНЫЕ КИРПИЧИКИ ЧАСТИ 1 (не сквозные образы — только для этой порции) ──

def _okno_noch(x, y, w_, h_, t, seed=1, moroz=.35, svet=False, krest=False):
    """Окно с видом на ночную метель: тонкая обёртка над okno_izby/sneg_letit."""
    vid = f'<rect width="{W}" height="{H}" fill="#1c2946"/>' + sneg_letit(t, 16, seed, .55, .85)
    return okno_izby(x, y, w_, h_, t, vid=vid, moroz=moroz, svet=svet, krest=krest)


def _shveynaya_mashinka(x, y, t, s_=1.0, ph=0.0):
    """Швейная машинка: игла ходит вверх-вниз — живой элемент ателье."""
    ig = 9 * s_ * abs(A.w(t, .7, ph))
    s = ten(x, y + 6 * s_, 90 * s_, 14 * s_, .4)
    s += (f'<rect x="{x-86*s_:.0f}" y="{y-54*s_:.0f}" width="{172*s_:.0f}" height="{54*s_:.0f}"'
          f' rx="10" fill="{GRAFIT}" {o(5)}/>')
    s += (f'<path d="M{x-80*s_:.0f},{y-54*s_:.0f} q{40*s_:.0f},{-70*s_:.0f} {120*s_:.0f},{-56*s_:.0f}'
          f' l0,{24*s_:.0f} q{-70*s_:.0f},{-6*s_:.0f} {-104*s_:.0f},{40*s_:.0f} Z" fill="{GRAFIT}" {o(5)}/>')
    s += (f'<rect x="{x+28*s_:.0f}" y="{y-110*s_+ig:.0f}" width="{7*s_:.0f}" height="{30*s_:.0f}"'
          f' fill="{SEREBRO}" {o(3)}/>')
    s += f'<circle cx="{x+6*s_:.0f}" cy="{y-150*s_:.0f}" r="{16*s_:.0f}" fill="{ZOLOTO}" {o(4)}/>'
    s += (f'<rect x="{x-86*s_:.0f}" y="{y-6*s_:.0f}" width="{172*s_:.0f}" height="{10*s_:.0f}"'
          f' fill="{DOSKA2}" {o(4)}/>')
    return s


def _katushki(x, y, n=5, seed=2, s_=1.0):
    """Катушки ниток в ряд — предметный мусор ателье, сразу много предметов."""
    r = random.Random(seed)
    cols = (ALYY, RUBIN, VINO, KORALL, TERRAKOT, IZUMRUD, ZOLOTO, TSINIY)
    s = ""
    for i in range(n):
        xx = x + i * 44 * s_
        c = r.choice(cols)
        s += (f'<rect x="{xx-16*s_:.0f}" y="{y-40*s_:.0f}" width="{32*s_:.0f}" height="{40*s_:.0f}"'
              f' rx="6" fill="{c}" {o(3)}/>')
        s += (f'<ellipse cx="{xx:.0f}" cy="{y-40*s_:.0f}" rx="{16*s_:.0f}" ry="{6*s_:.0f}"'
              f' fill="{MOLOKO}" {o(2)}/>')
        s += (f'<ellipse cx="{xx:.0f}" cy="{y:.0f}" rx="{16*s_:.0f}" ry="{6*s_:.0f}"'
              f' fill="{MOLOKO}" {o(2)}/>')
    return s


def _instrumenty_stol(x, y, t, seed=1):
    """Ножницы, мел, сантиметр, игольница на столе — мелкий реквизит ателье."""
    r = random.Random(seed)
    a = 8 * A.w(t, 3.0, seed * .1)
    s = (f'<g transform="rotate({a:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x:.0f},{y:.0f} l44,-10 M{x:.0f},{y:.0f} l44,10" stroke="{SEREBRO}"'
         f' stroke-width="6" stroke-linecap="round"/>'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{GRAFIT}"/></g>')
    s += f'<rect x="{x+60:.0f}" y="{y-6:.0f}" width="28" height="12" rx="4" fill="{MOLOKO}" {o(2)}/>'
    s += f'<ellipse cx="{x+118:.0f}" cy="{y:.0f}" rx="22" ry="20" fill="{MOLOKO}" {o(3)}/>'
    s += f'<path d="M{x+98:.0f},{y:.0f} q20,-18 40,0" fill="none" stroke="{K}" stroke-width="2" opacity=".6"/>'
    s += f'<ellipse cx="{x+170:.0f}" cy="{y:.0f}" rx="24" ry="18" fill="{KORALL}" {o(3)}/>'
    for i in range(5):
        ang = r.uniform(0, 6.28)
        s += (f'<line x1="{x+170+14*math.cos(ang):.0f}" y1="{y+8*math.sin(ang):.0f}"'
              f' x2="{x+170+22*math.cos(ang):.0f}" y2="{y+14*math.sin(ang):.0f}"'
              f' stroke="{SEREBRO}" stroke-width="2"/>')
    return s


def _fonarik(x, y, t, s_=1.0, col=ALYY, ph=0.0):
    """Красный бумажный фонарик на нитке, покачивается."""
    a = 5.0 * A.w(t, 2.4, ph)
    s = f'<g transform="rotate({a:.2f} {x:.0f} {y-60*s_:.0f})">'
    s += f'<line x1="{x:.0f}" y1="{y-134*s_:.0f}" x2="{x:.0f}" y2="{y-60*s_:.0f}" stroke="{K}" stroke-width="3"/>'
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{46*s_:.0f}" ry="{58*s_:.0f}" fill="{col}" {o(4)}/>'
    s += teplo(x, y, 90 * s_, 90 * s_, .3)
    for i in range(5):
        yy = y - 44 * s_ + i * 22 * s_
        s += (f'<line x1="{x-46*s_:.0f}" y1="{yy:.0f}" x2="{x+46*s_:.0f}" y2="{yy:.0f}"'
              f' stroke="{K}" stroke-width="2" opacity=".5"/>')
    s += f'<path d="M{x:.0f},{y+58*s_:.0f} l0,{24*s_:.0f}" stroke="{ZOLOTO}" stroke-width="4"/>'
    s += "</g>"
    return s


def _sofit(x, y, t, ph=0.0, s_=1.0):
    """Софит сверху: качает луч и мигает лампой."""
    yar = .5 + .5 * abs(A.w(t, 1.6, ph))
    s = (f'<path d="M{x-10*s_:.0f},{y:.0f} l{20*s_:.0f},0 l{60*s_:.0f},{220*s_:.0f}'
         f' l{-140*s_:.0f},0 Z" fill="{TEPLO_SVET}" opacity="{.10+.12*yar:.2f}"/>')
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{22*s_:.0f}" ry="{14*s_:.0f}" fill="{GRAFIT}" {o(3)}/>'
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{10*s_:.0f}" fill="#fff6d8" opacity="{yar:.2f}"/>'
    return s


def _zriteli(x, y, n=6, seed=1, h_=220, dx=86):
    """Ряд зрителей-силуэтов на подиуме — фон, не считанные «Людей»."""
    r = random.Random(seed)
    s = ""
    for i in range(n):
        s += siluet(x + i * dx, y, h_ * r.uniform(.9, 1.08), "#15141a", .92)
    return s


def _podium_pod(x, y, w_, h_=26, col=GRAFIT):
    """Помост подиума: плита с бликом сверху."""
    s = ten(x + w_ * .5, y + h_ + 10, w_ * .52, 16, .4)
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="{col}" {o(4)}/>'
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="6" fill="#ffffff" opacity=".18"/>'
    return s


def _vesy_kalendar(x, y, w_, h_, t, seed=1):
    """Настенный восточный календарь: лист, коза, иероглиф-пятно, фонарик сбоку."""
    r = random.Random(seed)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10"'
         f' fill="{MOLOKO}" {o(6)}/>')
    s += (f'<rect x="{x+10:.0f}" y="{y+10:.0f}" width="{w_-20:.0f}" height="{h_*.18:.0f}"'
          f' fill="{ALYY}" {o(4)}/>')
    s += koza(x + w_ * .5, y + h_ * .78, h_ * .38, t, seed * .3, True)
    for i in range(3):
        s += (f'<rect x="{x+16+i*(w_-32)/3:.0f}" y="{y+h_*.86:.0f}" width="{(w_-32)/3-6:.0f}"'
              f' height="10" fill="{RUBIN}" opacity=".6"/>')
    return s


def ognennaya_koza_v_atele(t):
    """Коза носом разворачивает рулон ткани перед большим зеркалом ателье."""
    rnd = random.Random(101)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 11))
    s += SL(650, _okno_noch(1560, 70, 300, 360, t, 21, .4, False, False))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(460, mebel_hlam(1180, FLOOR - 4, 420, t, 14))
    # зеркало слева: рисованный вид → метка → рама поверх (порядок опоры)
    mx, my, mw, mh = 70, 260, 780, 340
    put = kontur_proema(mx, my, mw, mh, "pryam")
    vid = (f'<path d="{put}" fill="#241217"/>'
           + otrez(mx + 20, my + 10, mw - 40, mh - 20, VINO, t, 6, .30, .3)
           + skladki(mx + 30, my + 30, mw - 60, mh - 60, VINO, 7, 31, t, 4.0))
    s += SL(420, vid + mesto_stoka(mx, my, mw, mh, "pryam") + zerkalo(mx, my, mw, mh, t, "pryam", ZOLOTO, True))
    s += SL(420, manekken(430, FLOOR, 640, t, KREM2, "zh", VINO, .3, ZOLOTO, .18, 23, True))
    s += SL(400, _shveynaya_mashinka(760, FLOOR - 4, t, 1.1, .2))
    s += SL(380, _katushki(820, FLOOR - 50, 6, 7))
    s += SL(360, _instrumenty_stol(640, FLOOR - 30, t, 3))
    s += SL(300, elka(1720, FLOOR + 20, 420, t, 1.0, True, 5))
    s += SL(280, girlyanda(560, 150, 760, t, 11, 4, 54))
    # коза крупно справа, перед ней рулон, разворачивающийся и переливающийся
    rx = 1300 + 16 * A.w(t, 2.6, .1)
    s += SL(0, otrez(rx - 260, FLOOR - 60, 180, 60, ALYY, t, 8, .25, .0))
    s += SL(0, otrez(rx - 90, FLOOR - 60, 180, 60, RUBIN, t, 9, .25, .3))
    s += SL(0, otrez(rx + 90, FLOOR - 60, 190, 64, VINO, t, 10, .30, .6))
    s += SL(0, koza(rx, FLOOR, 520, t, .0, True))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def velvetovyy_pidzhak_na_manekene(t):
    """Вельветовый пиджак на мужском манекене, рядом гладильная доска, коза кивает."""
    rnd = random.Random(102)
    s = f'<rect width="{W}" height="{H}" fill="#241c17"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 12))
    s += SL(700, _okno_noch(1600, 120, 260, 300, t, 22, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#dosk)"))
    s += SL(460, mebel_hlam(60, FLOOR - 4, 360, t, 15))
    s += SL(420, manekken(960, FLOOR, 880, t, MOLOKO, "m", TERRAKOT, .15, MOLOKO, .10, 4, True))
    # вешалка с брюками рядом
    s += SL(420, shtanga(1240, FLOOR, 60, t, 360, False))
    s += SL(400, naryad_plechiki(1240, FLOOR - 360, 300, t, GRAFIT, .62, .4, False, None, .0, 8))
    # гладильная доска и утюг
    gy = FLOOR - 4
    s += SL(380, f'<path d="M700,{gy:.0f} q220,-34 420,0 l-14,-16 q-196,-30 -392,0 Z" fill="{MOLOKO}" {o(5)}/>')
    s += SL(380, f'<rect x="900" y="{gy-62:.0f}" width="80" height="34" rx="8" fill="{SEREBRO}" {o(5)}/>')
    s += SL(380, par(940, gy - 70, t, 4, .5, 130, .5, .8))
    s += SL(360, korobka(560, FLOOR, 150, t, 90, True, BEZH, MOLOKO))
    s += SL(300, elka(1800, FLOOR + 10, 380, t, .95, True, 6))
    s += SL(250, girlyanda(60, 120, 1760, t, 13, 3, 60))
    # коза подходит слева и кивает
    kiv = 4.0 * A.w(t, 1.3, .2)
    s += SL(0, f'<g transform="rotate({kiv:.2f} 300 {FLOOR-260})">' + koza(300, FLOOR, 360, t, .2, True) + "</g>")
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.4)
    return s


def kalendar_i_podium(t):
    """Слева восточный календарь, справа подиум с манекенщицей, бант в центре."""
    rnd = random.Random(103)
    s = f'<rect width="{W}" height="{H}" fill="#120f14"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 13))
    s += SL(700, _sofit(560, 40, t, .0)) + SL(700, _sofit(1000, 40, t, .4)) + SL(700, _sofit(1440, 40, t, .8))
    s += SL(560, _zriteli(1180, FLOOR + 40, 7, 4, 230, 92))
    s += SL(520, _podium_pod(760, FLOOR + 30, 1000, 30))
    s += SL(460, _vesy_kalendar(70, 170, 420, 560, t, 2))
    s += SL(420, _fonarik(560, 220, t, 1.2, ALYY, .3))
    # лента завязывается бантом между половинами
    uz = .5 + .5 * A.w(t, 2.0, .1)
    s += SL(400, f'<path d="M700,540 q120,{-60+40*uz:.0f} 240,0" fill="none" stroke="{ALYY}" stroke-width="20"'
                 f' stroke-linecap="round"/>')
    s += SL(400, f'<ellipse cx="820" cy="{520-20*uz:.0f}" rx="{40+20*uz:.0f}" ry="26" fill="{ALYY}" {o(4)}/>')
    s += SL(380, svecha(640, FLOOR - 4, t, .2, 1.1))
    # манекенщица идёт по подиуму
    shag = A.seg(t % 2.6, .0, 1.3)
    nx = 900 + 480 * A.ease(shag)
    s += SL(0, figura(nx, FLOOR + 20, 560, t, ALYY, HOLOD_KANT, .0, False, False, 1.0, 5 * A.w(t, 1.1), True, True))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def primeta_i_moda_v_odnom_zerkale(t):
    """Трюмо с двумя створками: отражения сходятся и сливаются в одно."""
    rnd = random.Random(104)
    s = f'<rect width="{W}" height="{H}" fill="#201a22"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 14))
    s += SL(650, _okno_noch(1640, 100, 220, 280, t, 23, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(460, mebel_hlam(1300, FLOOR - 4, 300, t, 16))
    s += SL(420, trumo(760, FLOOR, 420, 420, t))
    sx = .5 + .5 * A.w(t, 3.6, .0)          # 0 разведены .. 1 сошлись заподлицо
    for sgn, col in ((-1, MOLOKO), (1, LAVANDA)):
        otstup = 300 * (1 - sx)             # створки сходятся к центру, сливаясь
        cxz = 960 + sgn * otstup
        nak = sgn * 4 * A.w(t, 2.6, .2)     # лёгкий наклон своей же оси, без петли
        s += SL(400, f'<g transform="rotate({nak:.1f} {cxz:.0f} {FLOOR-230})">'
                     + zerkalo(cxz - 150, FLOOR - 440, 300, 420, t, "pryam", ZOLOTO, True) + "</g>")
    s += SL(360, birka(1200, FLOOR - 460, 1.3, t, MOLOKO, .4))
    s += SL(340, svecha(1260, FLOOR - 4, t, .5, 1.0))
    s += SL(300, naryad_plechiki(1360, FLOOR - 40, 360, t, PUDRA, .9, .6, True, MOLOKO, .12, 9))
    s += SL(0, figura(760, FLOOR + 10, 600, t, VINO, HOLOD_KANT, .0, False, False, 1.0, 0.0, True, True, "#f0cfae",
                      True, MOLOKO))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def zakrytyy_magazin_i_svoy_shkaf(t):
    """Зимняя улица, закрытая витрина без вывески, женщина проходит мимо."""
    rnd = random.Random(105)
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 15))
    s += SL(Z_DAL, panelka(0, 700, 900, t, 4, True, 6))
    s += SL(Z_DAL, ulica_dal(900, 700, 1020, t, True, 8))
    s += SL(Z_DAL, sneg_lezhit(760))
    s += SL(Z_LETIT, sneg_letit(t, 40, 9, .75, 1.0))
    # витрина без вывески
    vx, vy, vw, vh = 120, 420, 520, 360
    s += SL(520, f'<rect x="{vx-20}" y="{vy-20}" width="{vw+40}" height="{vh+60}" fill="{GRAFIT}" {o(7)}/>')
    s += SL(500, f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" fill="{STEKLO}" opacity=".30"/>')
    s += SL(500, otrez(vx + 30, vy + 30, vw - 60, vh - 90, TERRAKOT, t, 12, .2))
    s += SL(480, f'<rect x="{vx+vw+30}" y="{vy+vh-30}" width="70" height="90" rx="4" fill="{GRAFIT}" {o(4)}/>'
                 f'<circle cx="{vx+vw+65}" cy="{vy+vh+10}" r="6" fill="{ZOLOTO}"/>')
    s += SL(460, _fonarik(760, 380, t, 1.3, ALYY, .2))
    s += SL(440, elka(1760, 820, 320, t, .9, True, 10))
    # дом за углом с раскрытым шкафом в окне
    ox, oy = 1480, 440
    svet_okno = okno_izby(ox, oy, 220, 260, t, vid=shkaf(ox + 10, oy + 250, 190, 230, t, .9), svet=True, moroz=.2)
    s += SL(420, svet_okno)
    s += SL(Z_DAL, sneg_lezhit(oy + 300, 18))
    # женщина идёт мимо витрины
    shag = (t * .5) % 1.0
    wx = 300 + 420 * shag
    s += SL(0, figura(wx, 800, 480, t, TSINIY, HOLOD_KANT, 2 * A.w(t, .8), False, False, 1.0,
                      6 * A.w(t, 1.2), True, True))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.46)
    return s


def veshalka_s_semyu_naryadami(t):
    """Напольная штанга с семью нарядами, из шкафа выезжают ещё три платья."""
    rnd = random.Random(106)
    s = f'<rect width="{W}" height="{H}" fill="#221b1d"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 16))
    s += SL(650, _okno_noch(1620, 90, 260, 300, t, 24, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, shkaf(80, FLOOR, 360, 760, t, .85))
    vyezd = A.ease(A.seg((t * .4) % 1.0, .0, .7))
    for i, col in enumerate((ALYY, VINO, IZUMRUD)):
        dx = 420 * vyezd * (i + 1) / 3.2
        s += SL(460, naryad_plechiki(140 + dx, FLOOR - 380, 320, t, col, .78, .3 + i * .2, True, MOLOKO, .1, 20 + i))
    s += SL(420, shtanga(1080, FLOOR, 760, t, 460, True))
    naryady = ((ALYY, True), (RUBIN, True), (VINO, True), (KORALL, True),
               (GRAFIT, False), (TSINIY, False), (TERRAKOT, False))
    for i, (col, platye) in enumerate(naryady):
        nx = 760 + i * 100
        nom = .5 + .5 * math.cos(2 * math.pi * ((t * 1.1 + i * .3) % 1.0))
        s += SL(400, naryad_plechiki(nx, FLOOR - 460, 300, t, col, .62, i * .25, platye, MOLOKO, .08, 30 + i))
        s += SL(400, f'<circle cx="{nx:.0f}" cy="{FLOOR-460:.0f}" r="16" fill="{ZOLOTO}" opacity="{.3+.6*nom:.2f}"/>')
    s += SL(360, korobka(1620, FLOOR, 140, t, 86, True, BEZH, MOLOKO))
    s += SL(340, korobka(1480, FLOOR, 130, t, 80, False, TERRAKOT, MOLOKO))
    s += SL(300, girlyanda(60, 120, 1800, t, 14, 2, 50))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def kolyuchiy_dzhemper_uhodit_v_shkaf(t):
    """Колючий серый джемпер с иголками уходит на плечиках в шкаф."""
    rnd = random.Random(107)
    s = f'<rect width="{W}" height="{H}" fill="#1e1a1c"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 17))
    s += SL(650, _okno_noch(1600, 100, 260, 300, t, 25, .45))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, mebel_hlam(60, FLOOR - 4, 320, t, 18))
    raskr = .78 + .1 * A.w(t, 3.0, .2)
    s += SL(460, shkaf(1180, FLOOR, 420, 760, t, raskr))
    s += SL(380, korobka(980, FLOOR - 460, 180, t, 120, False, MOLOKO, MOLOKO))
    s += SL(360, tufli(1020, FLOOR - 4, 1.0, GRAFIT, t))
    s += SL(340, girlyanda(60, 140, 760, t, 15, 3, 48))
    # джемпер колючий на пол-кадра, плечики уезжают в угол шкафа
    ygl = A.ease(A.seg((t * .35) % 1.0, .0, .8))
    jx = 560 + 520 * ygl
    jy = FLOOR - 420
    s += SL(0, naryad_plechiki(jx, jy, 420, t, SERYY, .9, .0, False, GRAFIT, .0, 19))
    r9 = random.Random(9)
    for i in range(26):
        a = r9.uniform(0, 6.28); rr = r9.uniform(70, 150)
        ix, iy = jx + math.cos(a) * rr, jy + 60 + math.sin(a) * rr * 1.3
        s += SL(0, f'<line x1="{jx:.0f}" y1="{jy+90:.0f}" x2="{ix:.0f}" y2="{iy:.0f}"'
                   f' stroke="{GRAFIT}" stroke-width="3"/>')
    # женщина держит плечики, потирает шею
    s += SL(20, figura(640, FLOOR + 10, 560, t, MOLOKO, BEZH, .0, False, False, 1.0, 0.0, True, True))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def koza_probuet_tkani(t):
    """Коза трётся щекой о три вещи на стульях и каждый раз отдёргивает морду."""
    rnd = random.Random(108)
    s = f'<rect width="{W}" height="{H}" fill="#241c19"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 18))
    s += SL(650, _okno_noch(1600, 90, 260, 300, t, 26, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, elka(120, FLOOR + 20, 420, t, 1.0, True, 11))
    s += SL(460, girlyanda(40, 120, 420, t, 16, 4, 46))
    s += SL(440, kot(1700, FLOOR - 4, t, 1.1))
    stulya = ((560, SERYY, .62), (900, KORALL, .0), (1240, IZUMRUD, .0))
    for i, (sx, col, _) in enumerate(stulya):
        s += SL(420, lavka(sx - 70, FLOOR - 260, 140))
        s += SL(420, naryad_plechiki(sx, FLOOR - 400, 240, t, col, .58, i * .3, i != 0, MOLOKO, .1, 40 + i))
        if i == 2:
            s += SL(420, birka(sx + 60, FLOOR - 470, .9, t, MOLOKO, .5))
        # вещь на плечиках реально занимает FLOOR-400..FLOOR-100 (подол +
        # скамья под ней) — пояснению сюда нельзя (поймано 17.11: «Принято
        # считать» легло на одежду). До пола метку НЕ тянуть — иначе внизу
        # не остаётся ни одной свободной полосы и пояснение уезжает на
        # соседнюю плашку-пункт (поймано при проверке той же правки)
        s += SL(0, mesto_figury(sx - 120, FLOOR - 400, 240, 300))
    s += SL(360, f'<rect x="80" y="{FLOOR-4}" width="200" height="140" rx="16" fill="{TERRAKOT}" opacity=".85"'
                 f' {o(5)}/>')
    otdyor = abs(A.w(t, 1.6, .0))
    tryot = (t * 1.6) % 3.0
    idx = int(tryot)
    kx = stulya[idx % 3][0]
    kdx = -40 + 80 * A.ease(A.seg(tryot % 1.0, .0, .6)) - otdyor * 30
    s += SL(0, koza(kx + kdx, FLOOR, 460, t, .0, True))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def yarlyk_i_malenkie_nozhnicy(t):
    """Крупно воротник платья изнутри: рукава срезают жёсткий ярлык ножницами."""
    rnd = random.Random(109)
    s = f'<rect width="{W}" height="{H}" fill="#16130f"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 19))
    s += SL(700, svecha(1700, 220, t, .2, 1.0))
    s += SL(520, _instrumenty_stol(1200, 760, t, 5))
    s += SL(480, _katushki(1360, 700, 5, 6))
    s += SL(460, hodiki(1700, 420, t, .9))
    s += SL(440, f'<ellipse cx="760" cy="640" rx="80" ry="60" fill="{MOLOKO}" {o(4)}/>')
    s += SL(420, par(760, 580, t, 3, .4, 120, .5, .7))
    # воротник платья изнутри, крупно
    vx, vy = 820, 540
    s += SL(0, f'<path d="M{vx-260},{vy+360} q260,-70 520,0 l-30,220 q-230,60 -460,0 Z" fill="{VINO}" {o(7)}/>')
    s += SL(0, skladki(vx - 240, vy + 300, 480, 240, VINO, 6, 32, t, 3.0))
    yarl_j = 6 * A.w(t, 2.2, .0)
    s += SL(10, f'<path d="M{vx-20},{vy+360} l50,{-30+yarl_j:.0f} l10,40 Z" fill="{MOLOKO}" {o(4)}/>')
    # рукав халата слева придерживает воротник
    ruk1, (h1x, h1y) = rukav(vx - 420, vy + 560, 300, -36, t, GRAFIT, HOLOD_KANT, .1, 5.0, True)
    s += SL(20, ruk1)
    # рукав халата справа подводит ножницы и срезает ярлык
    srez = (t * .7) % 1.0
    ruk2, (h2x, h2y) = rukav(vx + 420, vy + 560, 300, -150 + 30 * A.ease(srez), t, GRAFIT, HOLOD_KANT, .3, 6.0, True)
    s += SL(20, ruk2)
    rot = -20 + 40 * A.w(t, .9, .5)
    s += SL(22, f'<g transform="rotate({rot:.1f} {h2x:.0f} {h2y:.0f})">'
                f'<path d="M{h2x:.0f},{h2y:.0f} l40,-8 M{h2x:.0f},{h2y:.0f} l40,8" stroke="{SEREBRO}"'
                f' stroke-width="6" stroke-linecap="round"/><circle cx="{h2x:.0f}" cy="{h2y:.0f}" r="7"'
                f' fill="{GRAFIT}"/></g>')
    if srez > .7:
        s += SL(24, f'<ellipse cx="{vx-10}" cy="{vy+420}" rx="26" ry="18" fill="{MOLOKO}" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def tri_kislotnye_veschi(t):
    """Три кислотные вещи сохнут на верёвке, кот жмурится, их снимают в коробку."""
    rnd = random.Random(110)
    kisl_z = "#9fe62e"; kisl_l = "#f3f23a"; kisl_r = "#ff4fb0"
    s = f'<rect width="{W}" height="{H}" fill="#1b1e17"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 20))
    s += SL(650, _okno_noch(1600, 100, 260, 300, t, 27, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, mebel_hlam(60, FLOOR - 4, 320, t, 21))
    s += SL(460, kot(1640, 560, t, 1.1))
    s += SL(460, lampa_stolika(1700, 420, t, .9))
    s += SL(440, f'<circle cx="1050" cy="300" r="900" fill="{kisl_z}" opacity=".05"/>')
    s += SL(420, f'<line x1="300" y1="320" x2="1500" y2="320" stroke="#3b3b3b" stroke-width="5"/>')
    veschi = ((460, kisl_z, "кофта"), (820, kisl_l, "блузка"), (1180, kisl_r, "шарф"))
    tabur_x = 980 + 40 * A.w(t, 1.1, .0)
    for i, (vx, col, _) in enumerate(veschi):
        kach = 6 * A.w(t, 2.0, i * .3)
        s += SL(400, f'<g transform="rotate({kach:.1f} {vx} 300)">'
                     f'<rect x="{vx-100}" y="320" width="200" height="260" rx="20" fill="{col}" {o(6)}/>'
                     + skladki(vx - 90, 330, 180, 240, col, 4, 40 + i, t, 2.6) + "</g>")
        s += SL(400, f'<path d="M{vx-10},300 l20,0 l0,24 l-20,0 Z" fill="{SEREBRO}" {o(2)}/>')
        yar = .5 + .5 * abs(A.w(t, 1.0 + i * .3, i * .5))
        s += SL(400, f'<circle cx="{vx}" cy="420" r="150" fill="{col}" opacity="{yar*.14:.2f}"/>')
    s += SL(360, f'<rect x="{tabur_x-60:.0f}" y="560" width="120" height="30" rx="8" fill="{DOSKA2}" {o(5)}/>'
                 f'<rect x="{tabur_x-50:.0f}" y="590" width="16" height="200" fill="{DOSKA2}" {o(4)}/>'
                 f'<rect x="{tabur_x+34:.0f}" y="590" width="16" height="200" fill="{DOSKA2}" {o(4)}/>')
    s += SL(340, korobka(640, FLOOR, 220, t, 150, True, BEZH, MOLOKO))
    snyat = A.ease(A.seg((t * .4) % 1.0, .0, .7))
    s += SL(0, figura(tabur_x, 790, 420, t, TSINIY, HOLOD_KANT, .0, False, False, 1.0,
                      3 * A.w(t, 1.2), True, True))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def chernyy_naryad_na_manekene(t):
    """Чёрный наряд по частям появляется на манекене, сливающемся с тенью."""
    rnd = random.Random(111)
    s = f'<rect width="{W}" height="{H}" fill="#0f0e10"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 22))
    s += SL(650, _okno_noch(1560, 80, 280, 320, t, 28, .35))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, f'<path d="M1300,220 q260,0 260,340 v420 h-520 v-420 q0,-340 260,-340 Z" fill="{POL2}"'
                 f' opacity=".30"/>')
    s += SL(460, f'<rect x="1500" y="340" width="300" height="440" rx="10" fill="{MOLOKO}" opacity=".9" {o(5)}/>'
                 f'<rect x="1540" y="620" width="60" height="160" rx="10" fill="{ALYY}" {o(4)}/>')
    s += SL(420, elka(1780, FLOOR + 10, 420, t, 1.0, True, 23))
    s += SL(400, girlyanda(1440, 180, 400, t, 17, 5, 44))
    poyav = ((t * .3) % 4.0)
    tiers = (("платье", .0), ("колготки", 1.0), ("туфли", 2.0), ("сумка", 3.0))
    s += SL(0, manekken(960, FLOOR, 880, t, KREM2, "zh",
                        GRAFIT if poyav >= 0 else None, .1, GRAFIT if poyav >= 0 else None, .22, 24, True))
    if poyav >= 1.0:
        s += SL(0, f'<rect x="900" y="{FLOOR-180}" width="120" height="170" fill="{GRAFIT}" opacity=".85"/>')
    if poyav >= 2.0:
        s += SL(0, tufli(900, FLOOR, 1.0, GRAFIT, t))
    if poyav >= 3.0:
        s += SL(0, f'<path d="M1120,{FLOOR-500} q60,-20 70,40 l-10,160 q-40,30 -70,0 Z" fill="{GRAFIT}" {o(5)}/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.5)
    return s


def kartochka_drugogo_video_v_ramke(t):
    """В рамке на стене встаёт карточка другого ролика, коза показывает носом."""
    rnd = random.Random(112)
    s = f'<rect width="{W}" height="{H}" fill="#201a16"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 24))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, f'<rect x="60" y="{FLOOR-620}" width="560" height="180" rx="12" fill="{DEREVO}" {o(6)}/>'
                 f'<rect x="80" y="{FLOOR-600}" width="200" height="30" fill="{KORALL}" opacity=".7"/>')
    poy = A.ease(A.seg((t * .35) % 1.0, .0, .7))
    rx, ry, rw, rh = 760, 220, 480, 400
    s += SL(460, f'<rect x="{rx-24}" y="{ry-24}" width="{rw+48}" height="{rh+48}" rx="10" fill="{ZOLOTO}" {o(4)}/>')
    s += SL(460, f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="#1a1410"/>')
    # карточка-обложка: бабушка у шкафа отодвигает чёрное платье
    s += SL(460, f'<g opacity="{poy:.2f}" transform="translate(0,{(1-poy)*40:.0f})">'
                 + shkaf(rx + 60, ry + rh - 20, 200, 300, t, .4)
                 + siluet(rx + 300, ry + rh - 20, 300, "#0e0d0f", .95)
                 + naryad_plechiki(rx + 150, ry + rh - 300, 220, t, GRAFIT, .7, .0, True) + "</g>")
    s += SL(420, karavay(300, FLOOR - 4, .9))
    s += SL(400, f'<rect x="420" y="{FLOOR-180}" width="90" height="170" rx="14" fill="{MOLOKO}" {o(5)}/>'
                 + skladki(420, FLOOR - 170, 90, 150, MOLOKO, 3, 50, t, 2.0))
    s += SL(380, svecha(540, FLOOR - 4, t, .3, 1.1))
    s += SL(360, girlyanda(60, 140, 560, t, 18, 2, 46))
    pokaz = 6 * A.w(t, 1.4, .0)
    s += SL(0, f'<g transform="rotate({pokaz:.1f} 1260 {FLOOR-220})">'
               + koza(1260, FLOOR, 420, t, .0, True) + "</g>")
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def edinstvennoe_naryadnoe_plate_temno(t):
    """Одно нарядное чёрное платье на дверце шкафа, стрелка вперёд мигает."""
    rnd = random.Random(113)
    s = f'<rect width="{W}" height="{H}" fill="#19151a"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 25))
    s += SL(650, _okno_noch(1600, 120, 240, 280, t, 29, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, shkaf(680, FLOOR, 460, 820, t, .55))
    s += SL(440, naryad_plechiki(900, FLOOR - 460, 320, t, GRAFIT, .78, .2, True, MOLOKO, .18, 26))
    s += SL(440, naryad_plechiki(780, FLOOR - 380, 220, t, BEZH, .5, .5, False, None, .0, 27))
    s += SL(440, naryad_plechiki(780, FLOOR - 300, 220, t, PUDRA, .5, .8, True, None, .0, 28))
    mig = .4 + .6 * abs(A.w(t, 1.4, .0))
    s += SL(420, f'<path d="M980,{FLOOR-620} l60,30 l-60,30 l0,-20 l-40,0 l0,-20 l40,0 Z" fill="{ZOLOTO}"'
                 f' opacity="{mig:.2f}"/>')
    s += SL(400, tufli(600, FLOOR, 1.0, VINO, t))
    s += SL(380, girlyanda(60, 140, 560, t, 19, 3, 44))
    s += SL(0, figura(1220, FLOOR + 20, 560, t, PUDRA, HOLOD_KANT, .0, False, False, .96,
                      0.0, True, True))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.42)
    return s


def vitrina_atele_s_otrezami(t):
    """Витрина ателье с отрезами, коза смотрит в стекло. Смена главы."""
    rnd = random.Random(114)
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, False, 26))
    s += SL(Z_DAL, panelka(1300, 760, 620, t, 4, False, 10))
    s += SL(Z_DAL, sneg_lezhit(740))
    vx, vy, vw, vh = 460, 300, 800, 340
    s += SL(520, f'<rect x="{vx-30}" y="{vy-30}" width="{vw+60}" height="{vh+100}" rx="8" fill="{GRAFIT}" {o(7)}/>')
    put = kontur_proema(vx, vy, vw, vh, "pryam")
    vid = (f'<path d="{put}" fill="#14110d"/>'
           + otrez(vx + 30, vy + 20, 220, vh - 60, ALYY, t, 40, .25)
           + otrez(vx + 280, vy + 20, 220, vh - 60, RUBIN, t, 41, .25, .3)
           + otrez(vx + 530, vy + 20, 220, vh - 60, VINO, t, 42, .25, .6))
    s += SL(500, vid + mesto_stoka(vx, vy, vw, vh, "pryam") + f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}"'
                 f' fill="none" stroke="{SEREBRO}" stroke-width="16"/>')
    kol = .5 + .5 * A.w(t, 4.0, .0)
    s += SL(480, f'<circle cx="{vx+40}" cy="{vy-20}" r="{8+3*kol:.1f}" fill="{ZHELEZ}" opacity=".8"/>')
    s += SL(460, _fonarik(vx + vw + 120, 360, t, 1.1, ALYY, .3))
    s += SL(440, elka(vx - 140, FLOOR + 10, 300, t, .9, True, 27))
    s += SL(Z_LETIT, sneg_letit(t, 30, 30, .6, .9))
    kiv = 3.0 * A.w(t, 1.2, .0)
    s += SL(0, f'<g transform="rotate({kiv:.1f} {vx+vw*.5:.0f} {FLOOR-180})">'
               + koza(vx + vw * .5, FLOOR, 360, t, .0, True) + "</g>")
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.3)
    return s


def podium_v_krasnom(t):
    """Пять манекенщиц идут по подиуму, четыре в красном, одна в бежевом."""
    rnd = random.Random(115)
    s = f'<rect width="{W}" height="{H}" fill="#100e12"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 28))
    for i, px in enumerate((300, 640, 980, 1320, 1620)):
        s += SL(700, _sofit(px, 30, t, i * .3))
    s += SL(560, _zriteli(60, FLOOR + 50, 10, 5, 220, 92))
    s += SL(520, _podium_pod(0, FLOOR + 40, W, 34))
    s += SL(500, girlyanda(60, 20, 1800, t, 7, 3, 36))
    s += SL(460, f'<path d="M0,{FLOOR-20} h{W}" stroke="{ALYY}" stroke-width="6" opacity=".6"/>')
    schet = int((t * 1.3) % 5) + 1
    s += SL(440, f'<circle cx="1800" cy="200" r="60" fill="{GRAFIT}" {o(4)}/>'
                 + "".join(f'<circle cx="{1800-18+((i%3)*18):.0f}" cy="{188+((i//3)*18):.0f}" r="7"'
                           f' fill="{ZOLOTO if i < schet else "#3a3a3a"}"/>' for i in range(5)))
    naryady = ((ALYY, .0), (RUBIN, 1.0), (VINO, 2.0), (KORALL, 3.0), (BEZH, 4.0))
    for i, (col, ph) in enumerate(naryady):
        faza = ((t * .4 + ph * .2) % 1.0)
        nx = 200 + 1500 * faza
        pod = 12 * A.w(t, 1.0, ph)
        s += SL(0, figura(nx, FLOOR + 10 + i, 540, t, col, HOLOD_KANT, .0, False, False, 1.0,
                          4 * A.w(t, 1.1, ph), True, True))
        s += SL(0, f'<path d="M{nx-30:.0f},{FLOOR-40} q30,{10+pod:.0f} 60,0" fill="none" stroke="{col}"'
                   f' stroke-width="3" opacity=".5"/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def pyat_loskutov_i_pyat_predmetov(t):
    """Пять лоскутов на столе, над каждым проступает предмет-подсказка."""
    rnd = random.Random(116)
    s = f'<rect width="{W}" height="{H}" fill="#1a1510"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 30))
    s += SL(650, _okno_noch(1620, 110, 240, 280, t, 31, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, stol(260, FLOOR - 20, 1500, 40))
    s += SL(440, lampa_stolika(1700, FLOOR - 70, t, 1.1))
    s += SL(420, _instrumenty_stol(300, FLOOR - 60, t, 11))
    s += SL(400, _katushki(480, FLOOR - 100, 6, 12))
    # бордовый добавлен 17.11 (его слово: цвета не хватало в палитре) —
    # шестым лоскутом, шаг сужен со 220 до 200, чтобы все влезли на стол
    loskuty = ((ALYY, "мак"), (RUBIN, "перстень"), (VINO, "вишня"), (BORDO, "гранат"),
               (KORALL, "бусы"), (TERRAKOT, "горшок"))
    for i, (col, predmet) in enumerate(loskuty):
        lx = 400 + i * 210
        pripod = abs(A.w(t, 1.6, i * .4)) * 10
        s += SL(0, f'<rect x="{lx-80:.0f}" y="{FLOOR-60-pripod:.0f}" width="160" height="70" rx="10"'
                   f' fill="{col}" {o(5)}/>')
        s += SL(0, skladki(lx - 70, FLOOR - 50 - pripod, 140, 50, col, 3, 60 + i, t, 1.6))
        vid_p = .5 + .5 * math.cos(2 * math.pi * ((t * .5 + i * .25) % 1.0))
        if predmet == "мак":
            pr = f'<circle cx="{lx}" cy="{FLOOR-220}" r="34" fill="{ALYY}" opacity="{vid_p:.2f}"/>'
        elif predmet == "перстень":
            pr = (f'<circle cx="{lx}" cy="{FLOOR-220}" r="22" fill="none" stroke="{ZOLOTO}" stroke-width="8"'
                  f' opacity="{vid_p:.2f}"/><circle cx="{lx}" cy="{FLOOR-234}" r="12" fill="{RUBIN}"'
                  f' opacity="{vid_p:.2f}"/>')
        elif predmet == "вишня":
            pr = (f'<circle cx="{lx-10}" cy="{FLOOR-216}" r="18" fill="{VINO}" opacity="{vid_p:.2f}"/>'
                  f'<circle cx="{lx+16}" cy="{FLOOR-226}" r="18" fill="{VINO}" opacity="{vid_p:.2f}"/>')
        elif predmet == "гранат":
            pr = (f'<circle cx="{lx}" cy="{FLOOR-212}" r="26" fill="{BORDO}" opacity="{vid_p:.2f}"/>'
                  f'<path d="M{lx-14},{FLOOR-238} l6,-16 l8,10 l8,-10 l6,16 Z" fill="{BORDO}"'
                  f' opacity="{vid_p:.2f}"/>')
        elif predmet == "бусы":
            pr = "".join(f'<circle cx="{lx-40+j*16}" cy="{FLOOR-210+abs(j-4)*4}" r="9" fill="{KORALL}"'
                         f' opacity="{vid_p:.2f}"/>' for j in range(9))
        else:
            pr = f'<path d="M{lx-26},{FLOOR-190} q26,-40 52,0 l-6,40 q-20,16 -40,0 Z" fill="{TERRAKOT}"' \
                 f' opacity="{vid_p:.2f}"/>'
        s += SL(20, pr)
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def aloe_plate_i_mak(t):
    """Манекен в алом платье у распахнутого окна с настоящими маками в проёме."""
    rnd = random.Random(117)
    s = f'<rect width="{W}" height="{H}" fill="#241a18"/>'
    s += SL(Z_NEBO, nebo("rassv", t, False, 32))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, _shveynaya_mashinka(1500, FLOOR - 4, t, 1.0, .3))
    s += SL(460, korobka(1660, FLOOR, 160, t, 100, True, TERRAKOT, MOLOKO))
    s += SL(440, svecha(1560, FLOOR - 4, t, .2, .9))
    ox, oy, ow, oh = 1100, 260, 780, 320
    nak = 4 * A.w(t, 1.0, .0)
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<path d="{put}" fill="#0d1a08"/>' + f'<rect x="{ox+20}" y="{oy+20}" width="{ow-40}" height="{oh-40}"' \
          f' fill="{IZUMRUD}" opacity=".25"/>'
    r12 = random.Random(12)
    for i in range(10):
        mx = ox + 40 + r12.uniform(0, ow - 80)
        my = oy + 60 + r12.uniform(0, oh - 100)
        mk = 6 * A.w(t, 1.4, i * .3)
        vid += (f'<g transform="rotate({mk:.1f} {mx:.0f} {my:.0f})">'
                f'<line x1="{mx:.0f}" y1="{my:.0f}" x2="{mx:.0f}" y2="{my+60:.0f}" stroke="{HVOYA}"'
                f' stroke-width="4"/><circle cx="{mx:.0f}" cy="{my:.0f}" r="22" fill="{ALYY}" {o(3)}/>'
                f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="8" fill="{GRAFIT}"/></g>')
    s += SL(420, vid + mesto_stoka(ox, oy, ow, oh, "pryam") + f'<rect x="{ox-14}" y="{oy-14}" width="{ow+28}"'
                 f' height="{oh+28}" fill="none" stroke="{MOLOKO}" stroke-width="22"/>')
    s += SL(400, zanaveska(ox + ow + 10, oy, oh, 150, MOLOKO, t, 1))
    s += SL(0, manekken(640, FLOOR, 760, t, KREM2, "zh", ALYY, .0, ZOLOTO, .14, 33, True))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.4)
    return s


def babushkin_persten_s_rubinom(t):
    """Крупно рука в кресле: перстень с рубином у края кружевного рукава."""
    rnd = random.Random(118)
    s = f'<rect width="{W}" height="{H}" fill="#191318"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 34))
    s += SL(650, lampa(1680, 260, t, 1.0))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, f'<path d="M300,{FLOOR+60} q-60,-380 360,-420 q400,-30 420,330 l10,90 h-800 Z"'
                 f' fill="{VINO}" {o(7)}/>')
    s += SL(460, kot(1300, FLOOR - 4, t, 1.1))
    s += SL(440, hodiki(1500, 420, t, .95))
    s += SL(420, par(1120, FLOOR - 220, t, 3, .45, 120, .5, .7))
    # рукав кружевной на подлокотнике, перстень у края
    ruk, (hx, hy) = rukav(560, FLOOR - 40, 260, -172, t, MOLOKO, VINO, .1, 3.0, True)
    s += SL(0, ruk)
    bl = .5 + .5 * abs(A.w(t, 1.1, .0))
    s += SL(10, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="30" ry="22" fill="#e8cfae" {o(3)}/>')
    s += SL(12, f'<circle cx="{hx-4:.0f}" cy="{hy-6:.0f}" r="12" fill="{ZOLOTO}" {o(3)}/>'
                f'<circle cx="{hx-4:.0f}" cy="{hy-6:.0f}" r="7" fill="{RUBIN}" opacity="{.7+.3*bl:.2f}"/>')
    s += SL(0, naryad_plechiki(900, FLOOR - 460, 300, t, RUBIN, .8, .3, True, MOLOKO, .1, 35))
    ruk2, _ = rukav(560, FLOOR + 60, 220, -24, t, MOLOKO, VINO, .25, 2.0, True)
    s += SL(0, ruk2)
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.48)
    return s


def vinnoe_plate_i_vishnya(t):
    """Манекен в винном платье на веранде, в круге пялец настоящие вишни."""
    rnd = random.Random(119)
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += SL(Z_NEBO, nebo("rassv", t, False, 36))
    s += SL(Z_DAL, oblaka(t, 160, 3, 37, .5))
    s += SL(520, polovicy(FLOOR - 10, "url(#dosk)"))
    s += SL(480, f'<path d="M0,{FLOOR+20} h{W}" stroke="{DOSKA2}" stroke-width="10"/>')
    s += SL(460, pleten(1400, FLOOR + 60, 500, 150, 7))
    # пяльцы с настоящими вишнями — слева, на столике
    cx, cy, cr = 460, FLOOR - 280, 200
    put = kontur_proema(cx - cr, cy - cr, cr * 2, cr * 2, "ellips")
    r13 = random.Random(13)
    vid = f'<path d="{put}" fill="#2a0e10"/>'
    for i in range(10):
        a = r13.uniform(0, 6.28); rr = r13.uniform(0, cr - 40)
        vx, vy = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        q = .5 + .5 * A.w(t, 1.3, i * .2)
        vid += f'<circle cx="{vx:.0f}" cy="{vy+4*q:.0f}" r="24" fill="{VINO}" opacity="{.8+.2*q:.2f}" {o(3)}/>'
    s += SL(440, vid + mesto_stoka(cx - cr, cy - cr, cr * 2, cr * 2, "ellips")
                 + f'<circle cx="{cx}" cy="{cy}" r="{cr}" fill="none" stroke="{DEREVO}" stroke-width="18"/>')
    s += SL(420, stol(cx - 120, FLOOR - 20, 240, 36))
    s += SL(420, svecha(cx - 120, FLOOR - 56, t, .3, .9))
    s += SL(400, krynka(cx - 40, FLOOR - 56, 1.1))
    s += SL(380, zanaveska(cx - cr - 180, cy - cr - 40, cr * 2 + 60, 140, MOLOKO, t, -1))
    s += SL(0, manekken(1400, FLOOR, 700, t, KREM2, "zh", VINO, .2, MOLOKO, .2, 38, True))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.3)
    return s


def korallovye_busy_na_bluzke(t):
    """Коралловая блузка на плечиках на дверце шкафа, на вороте коралловые бусы."""
    rnd = random.Random(120)
    s = f'<rect width="{W}" height="{H}" fill="#1c1a20"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 39))
    s += SL(650, _okno_noch(1620, 100, 240, 280, t, 40, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, shkaf(680, FLOOR, 440, 760, t, .35))
    s += SL(440, f'<circle cx="1180" cy="{FLOOR-220}" r="90" fill="{MOLOKO}" opacity=".3" {o(4)}/>')
    s += SL(420, f'<path d="M1500,{FLOOR-120} q-40,-20 -70,20 l-20,60 q50,20 100,0 Z" fill="{MOLOKO}" {o(4)}/>')
    s += SL(0, naryad_plechiki(900, FLOOR - 460, 340, t, KORALL, .86, .0, False, MOLOKO, .2, 41))
    bl = .5 + .5 * A.w(t, 1.6, .0)
    busy = "".join(f'<circle cx="{900-56+j*16}" cy="{FLOOR-608+abs(j-3)*5}" r="10" fill="{KORALL}" {o(2)}/>'
                   for j in range(8))
    s += SL(2, busy + f'<circle cx="900" cy="{FLOOR-595}" r="12" fill="{KORALL}" opacity="{.8+.2*bl:.2f}" {o(2)}/>')
    s += SL(400, _katushki(1500, FLOOR - 40, 5, 42))
    s += SL(380, girlyanda(60, 140, 560, t, 21, 2, 46))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def terrakotovoe_plate_i_goncharnaya_p(t):
    """Манекен в терракотовом трикотаже у стеллажа с глиняными горшками (своё — кадр убран)."""
    rnd = random.Random(121)
    s = f'<rect width="{W}" height="{H}" fill="#201a14"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 43))
    s += SL(650, _okno_noch(1620, 110, 220, 260, t, 44, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#kamen)"))
    s += SL(480, f'<rect x="1120" y="{FLOOR-620}" width="500" height="620" rx="8" fill="{DEREVO}" {o(6)}/>')
    for i in range(3):
        py = FLOOR - 600 + i * 190
        s += SL(460, polka(1140, py, 460))
        for j in range(4):
            s += SL(460, krynka(1220 + j * 100, py + 60, .5 + .1 * (i + j) % 3, "url(#glina)"))
    s += SL(420, f'<circle cx="760" cy="{FLOOR-40}" r="200" fill="{DEREVO2}" opacity=".3"'
                 f' transform="rotate({(t*20)%360:.1f} 760 {FLOOR-40})"/>')
    s += SL(400, f'<rect x="640" y="{FLOOR-4}" width="80" height="60" rx="8" fill="{MOLOKO}" {o(4)}/>')
    s += SL(380, svecha(560, FLOOR - 4, t, .2, 1.0))
    s += SL(0, manekken(380, FLOOR, 680, t, KREM2, "zh", TERRAKOT, .15, BEZH, .06, 45, True))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def bordovoe_barhatnoe_plate_v_chehle(t):
    """Бордовое бархатное платье в расстёгнутом чехле на перекладине шкафа."""
    rnd = random.Random(122)
    s = f'<rect width="{W}" height="{H}" fill="#1c161a"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 46))
    s += SL(650, _okno_noch(1620, 110, 230, 270, t, 47, .42))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, shkaf(680, FLOOR, 420, 820, t, .62, True))
    s += SL(460, perekladina(900, FLOOR - 540, 320))
    rasstyog = .5 + .1 * A.w(t, 1.2, .0)
    s += SL(0, naryad_plechiki(900, FLOOR - 460, 360, t, RUBIN, .9, .0, True, None, .22, 48))
    s += SL(2, f'<path d="M740,{FLOOR-500} v300 q0,{40*rasstyog:.0f} 60,{40*rasstyog:.0f} v-340 Z" fill="{MOLOKO}"'
               f' opacity=".7" {o(4)}/>')
    s += SL(420, korobka(600, FLOOR, 150, t, 90, True, VINO, MOLOKO))
    s += SL(420, svecha(520, FLOOR - 4, t, .3, 1.0))
    s += SL(400, f'<ellipse cx="520" cy="{FLOOR-90}" rx="40" ry="24" fill="{LAVANDA}" opacity=".7" {o(3)}/>')
    s += SL(380, hodiki(1500, 400, t, .9))
    kalendar_dni = "".join(f'<circle cx="{1460+j*22}" cy="440" r="8" fill="{ALYY}"'
                           f' opacity="{.5+.5*abs(A.w(t,1.0,j*.5)):.2f}"/>' for j in (0, 1))
    s += SL(400, kalendar_dni)
    s += SL(0, figura(1140, FLOOR + 10, 560, t, MOLOKO, BEZH, .0, False, False, 1.0,
                      0.0, False, True))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tri_platya_i_tri_zhenschiny(t):
    """Примерочная, три зеркала, три женщины в алом, винном и терракотовом."""
    rnd = random.Random(123)
    s = f'<rect width="{W}" height="{H}" fill="#1a1620"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 49))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    zerkala = ((300, ALYY, False), (960, VINO, True), (1620, TERRAKOT, True))
    for i, (zx, col, galka) in enumerate(zerkala):
        s += SL(460, zerkalo(zx - 150, FLOOR - 620, 300, 540, t, "pryam", ZOLOTO, True))
        s += SL(440, f'<rect x="{zx-150}" y="{FLOOR-620}" width="300" height="540" fill="{GRAFIT}" opacity=".5"/>')
        if galka:
            mig = .4 + .6 * abs(A.w(t, 1.3, i * .4))
            s += SL(420, f'<circle cx="{zx}" cy="{FLOOR-660}" r="18" fill="{IZUMRUD}" opacity="{mig:.2f}"/>')
        else:
            s += SL(420, f'<path d="M{zx-20},{FLOOR-670} l40,0 m-30,-16 l-10,16 l10,16 m10,-32 l10,16 l-10,16"'
                         f' stroke="{RUBIN}" stroke-width="5" fill="none"/>')
        s += SL(0, figura(zx, FLOOR + 10, 520, t, col, HOLOD_KANT, .0, False, False, 1.0,
                          0.0, True, True))
    s += SL(380, zanaveska(60, FLOOR - 640, 600, 160, LAVANDA, t, 1))
    s += SL(360, lampa_stolika(1870, FLOOR - 60, t, .9))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def bolshoe_zerkalo_v_primerochnoy(t):
    """Большое напольное зеркало, женщина подносит к лицу винный шарф."""
    rnd = random.Random(124)
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, False, 50))
    s += SL(Z_DAL, oblaka(t, 140, 2, 51, .45))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, zerkalo(620, FLOOR - 760, 420, 760, t, "pryam", ZOLOTO, True))
    s += SL(460, f'<rect x="620" y="{FLOOR-760}" width="420" height="760" fill="{HOLOD_KANT}" opacity=".12"/>')
    s += SL(440, f'<path d="M0,{FLOOR+40} h{W}" stroke="{POL2}" stroke-width="4"/>')
    s += SL(420, stol(1400, FLOOR - 10, 320, 26))
    s += SL(420, lampa_stolika(1700, FLOOR - 70, t, .9))
    sharfy = ((ALYY, 1420), (TERRAKOT, 1560), (KORALL, 1680))
    for col, sx in sharfy:
        kach = 3 * A.w(t, 2.0, sx * .01)
        s += SL(400, f'<g transform="rotate({kach:.1f} {sx} {FLOOR-40})">'
                     f'<path d="M{sx-60},{FLOOR-40} q60,-20 120,0 l-10,30 q-50,10 -100,0 Z" fill="{col}" {o(4)}/></g>')
    s += SL(380, f'<circle cx="300" cy="{FLOOR-80}" r="60" fill="{HVOYA}" opacity=".6" {o(4)}/>')
    s += SL(0, figura(830, FLOOR + 10, 540, t, BEZH, HOLOD_KANT, .0, False, False, 1.0,
                      0.0, False, True, "#e0b792"))
    s += SL(2, f'<path d="M830,{FLOOR-420} q60,20 20,70" fill="none" stroke="{VINO}" stroke-width="14"'
               f' opacity="{.6+.4*abs(A.w(t,1.0,.0)):.2f}"/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.3)
    return s


def tri_sputnika_krasnogo(t):
    """Манекен в красном платье, вокруг кружат три шара-спутника оттенков."""
    rnd = random.Random(125)
    s = f'<rect width="{W}" height="{H}" fill="#1a1414"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 52))
    s += SL(650, _okno_noch(1620, 100, 240, 280, t, 53, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, _shveynaya_mashinka(1480, FLOOR - 4, t, 1.0, .5))
    s += SL(460, _katushki(300, FLOOR - 60, 6, 54))
    s += SL(440, elka(1760, FLOOR + 10, 360, t, .9, True, 55))
    cx, cy = 960, FLOOR - 420
    sput = ((ZOLOTO, 0.0, 260), (IZUMRUD, 2.1, 300), (PUDRA, 4.2, 340))
    for col, ph, R in sput:
        ang = t * .9 + ph
        sx, sy = cx + math.cos(ang) * R, cy + math.sin(ang) * R * .4
        s += SL(0, f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="34" fill="{col}" {o(4)}/>')
        s += SL(0, f'<circle cx="{sx-10:.0f}" cy="{sy-10:.0f}" r="10" fill="#ffffff" opacity=".4"/>')
    s += SL(0, manekken(cx, FLOOR, 760, t, KREM2, "zh", ALYY, .0, ZOLOTO, .25, 56, True))
    s += SL(380, girlyanda(60, 140, 560, t, 22, 2, 44))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def zolotye_melochi_na_zhakete(t):
    """Тёмный жакет на плечиках: по словам вспыхивают золотые мелочи."""
    rnd = random.Random(126)
    s = f'<rect width="{W}" height="{H}" fill="#191716"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 57))
    s += SL(650, lampa(1680, 260, t, .9))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, _katushki(1400, FLOOR - 80, 5, 58))
    s += SL(460, _instrumenty_stol(1200, FLOOR - 40, t, 59))
    s += SL(0, naryad_plechiki(900, FLOOR - 460, 320, t, GRAFIT, .8, .0, False, None, .05, 60))
    cikl = (t * .6) % 4.0
    pts = ((900, FLOOR - 540, "пуговица"), (900, FLOOR - 320, "пряжка"),
           (830, FLOOR - 480, "брошь"), (960, FLOOR - 400, "нить"))
    for i, (px, py, nm) in enumerate(pts):
        on = cikl >= i
        yar = .3 + .7 * abs(A.w(t, 1.2, i * .3)) if on else 0.0
        if nm == "нить":
            s += SL(2, f'<path d="M{px-60},{py} q60,-20 120,0" fill="none" stroke="{ZOLOTO}"'
                       f' stroke-width="3" opacity="{yar:.2f}"/>')
        else:
            s += SL(2, f'<circle cx="{px}" cy="{py}" r="14" fill="{ZOLOTO}" opacity="{.2+.8*yar:.2f}" {o(2)}/>')
    s += SL(420, girlyanda(60, 140, 560, t, 23, 3, 46))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def tri_zelenyh_i_elovaya_vetka(t):
    """Три манекена в зелёных тонах, за ними окно с настоящей еловой хвоей."""
    rnd = random.Random(127)
    s = f'<rect width="{W}" height="{H}" fill="#121a16"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 61))
    ox, oy, ow, oh = 600, 140, 780, 300
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    r14 = random.Random(14)
    vid = f'<path d="{put}" fill="#06100a"/>'
    for i in range(14):
        hx = ox + 40 + r14.uniform(0, ow - 80); hy = oy + 40 + r14.uniform(0, oh - 80)
        hk = 4 * A.w(t, 2.0, i * .2)
        vid += (f'<g transform="rotate({hk:.1f} {hx:.0f} {hy:.0f})">'
                f'<path d="M{hx:.0f},{hy:.0f} l-20,10 l20,4 l20,-4 Z" fill="{HVOYA}" {o(2)}/></g>')
    vid += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#ffffff" opacity=".10"/>'
    s += SL(480, vid + mesto_stoka(ox, oy, ow, oh, "pryam") + f'<rect x="{ox-14}" y="{oy-14}" width="{ow+28}"'
                 f' height="{oh+28}" fill="none" stroke="{DEREVO}" stroke-width="22"/>')
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(460, elka(140, FLOOR + 20, 380, t, 1.0, True, 15))
    # «оливковый» среди обязательных оттенков не назван — ближайший из палитры
    # ролика (его правило: своих HEX для нарядов не придумывать).
    manekeny = ((420, IZUMRUD, True), (960, IZUMRUD, False), (1500, HVOYA, True))
    for i, (mx, col, platye) in enumerate(manekeny):
        s += SL(0, manekken(mx, FLOOR, 700, t, KREM2, "zh", col, i * .2, MOLOKO, .18 if i == 0 else .0,
                            62 + i, platye))
    s += SL(420, f'<path d="M1700,{FLOOR-4} q20,-10 40,0" fill="none" stroke="{HVOYA}" stroke-width="8"/>')
    shishka = A.ease(A.seg((t * .4) % 1.0, .0, .7))
    s += SL(2, f'<circle cx="{1700+140*shishka:.0f}" cy="{FLOOR-10}" r="16" fill="{DEREVO2}" {o(3)}/>')
    s += SL(400, korobka(1700, FLOOR, 150, t, 90, False, TERRAKOT, MOLOKO))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def pudrovaya_bluzka_sharf_i_sumochka(t):
    """Пудровая блузка, шарф и сумочка на спинке стула; рукав отодвигает ленту."""
    rnd = random.Random(128)
    s = f'<rect width="{W}" height="{H}" fill="#1e1a1c"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 63))
    s += SL(650, lampa_stolika(1700, 320, t, 1.0))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    s += SL(480, trumo(1200, FLOOR, 380, 380, t))
    s += SL(0, f'<rect x="700" y="{FLOOR-380}" width="30" height="380" rx="10" fill="{DOSKA2}" {o(5)}/>'
               f'<path d="M700,{FLOOR-380} q90,-30 180,0" fill="none" stroke="{DOSKA2}" stroke-width="20"/>')
    kach = 4 * A.w(t, 2.6, .0)
    s += SL(0, f'<g transform="rotate({kach:.1f} 790 {FLOOR-340})">'
               + naryad_plechiki(790, FLOOR - 340, 320, t, PUDRA, .78, .0, False, None, .1, 70) + "</g>")
    s += SL(2, f'<path d="M700,{FLOOR-180} q50,{20+10*A.w(t,2.0,.2):.0f} 100,0" fill="none" stroke="{TERRAKOT}"'
               f' stroke-width="18" opacity=".85"/>')
    s += SL(4, f'<rect x="760" y="{FLOOR-90}" width="60" height="70" rx="14" fill="{KORALL}" {o(4)}/>')
    otdv = A.ease(A.seg((t * .5) % 1.0, .0, .8))
    lx = 980 + 160 * otdv
    s += SL(420, f'<path d="M1100,{FLOOR-20} l200,0" stroke="{GRAFIT}" stroke-width="2" opacity=".4"/>')
    s += SL(420, f'<rect x="{lx-60:.0f}" y="{FLOOR-28}" width="120" height="16" rx="6" fill="{ALYY}" {o(3)}/>')
    ruk, (hx, hy) = rukav(lx + 220, FLOOR + 80, 220, -170, t, GRAFIT, HOLOD_KANT, .2, 4.0, True)
    s += SL(430, ruk)
    s += SL(400, _katushki(1550, FLOOR - 40, 4, 71))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def molochnyy_kremovyy_bezhevyy(t):
    """Три светлых наряда: молочный, кремовый, бежевый; женщина примеряет пояс и брошь."""
    rnd = random.Random(129)
    s = f'<rect width="{W}" height="{H}" fill="#201f1a"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 64))
    s += SL(650, _okno_noch(1620, 100, 240, 280, t, 65, .4))
    s += SL(520, polovicy(FLOOR - 10, "url(#pol)"))
    naryady = ((520, MOLOKO), (860, KREM2), (1200, BEZH))
    for i, (nx, col) in enumerate(naryady):
        s += SL(440, naryad_plechiki(nx, FLOOR - 460, 320, t, col, .78, i * .3, i != 2, MOLOKO if i == 2 else None,
                                     .06, 72 + i))
    poyas_q = .5 + .5 * A.w(t, 1.6, .0)
    s += SL(2, f'<path d="M460,{FLOOR-280} q60,{10*poyas_q:.0f} 120,0" fill="none" stroke="{ALYY}"'
               f' stroke-width="16" opacity=".9"/>')
    s += SL(4, f'<circle cx="860" cy="{FLOOR-500}" r="14" fill="{ZOLOTO}" opacity="{.6+.4*abs(A.w(t,1.1,.3)):.2f}"'
               f' {o(2)}/>')
    s += SL(380, korobka(1500, FLOOR, 140, t, 86, True, MOLOKO, KREM2))
    s += SL(360, girlyanda(60, 140, 420, t, 24, 2, 42))
    s += SL(0, figura(1700, FLOOR + 20, 520, t, GRAFIT, HOLOD_KANT, .0, False, False, 1.0,
                      0.0, True, True, "#e8c9a6"))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.42)
    return s


def chernilnica_i_temno_sinee_plate(t):
    """Письменный стол с чернильницей, манекен в тёмно-синем, чёрное платье в тени."""
    rnd = random.Random(130)
    s = f'<rect width="{W}" height="{H}" fill="#14141c"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 66))
    s += SL(650, lampa(560, 320, t, .95))
    s += SL(520, polovicy(FLOOR - 10, "url(#dosk)"))
    s += SL(480, stol(360, FLOOR - 40, 460, 44))
    s += SL(460, f'<path d="M600,{FLOOR-90} q40,-12 80,0 l0,30 q-40,10 -80,0 Z" fill="{GRAFIT}" {o(4)}/>')
    kaplya = (t * .5) % 1.0
    ky = FLOOR - 60 + kaplya * 60
    s += SL(0, f'<circle cx="640" cy="{ky:.0f}" r="6" fill="{TSINIY}" opacity="{1-kaplya*.3:.2f}"/>')
    s += SL(2, f'<ellipse cx="640" cy="{FLOOR-4}" rx="{20+20*kaplya:.0f}" ry="8" fill="{TSINIY}"'
               f' opacity="{.2+.5*kaplya:.2f}"/>')
    s += SL(420, svecha(500, FLOOR - 40, t, .3, .9))
    otezd = A.ease(A.seg((t * .35) % 1.0, .0, .8))
    s += SL(380, naryad_plechiki(1500 + 60 * otezd, FLOOR - 420, 280, t, GRAFIT, .7, .4, True, None, .0, 75))
    s += SL(0, manekken(960, FLOOR, 760, t, KREM2, "zh", TSINIY, .1, MOLOKO, .18, 76, True))
    s += SL(400, girlyanda(60, 140, 560, t, 25, 2, 46))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


# ═══ из chast2.py ═══
def _polka_melochey(x, y, w_, t, seed, n=7):
    """Полка с мелочью ателье: катушки, напёрстки, флаконы, баночки.

    Этим добирается плотность кадра до нормы (от 60 предметов): своих крупных
    предметов в сцене пять-семь, остальное — обжитой второй план.
    """
    rnd = random.Random(seed)
    s = polka(x, y, w_)
    for i in range(n):
        px = x + w_ * (i + .5) / n + rnd.uniform(-8, 8)
        h_ = rnd.uniform(26, 54)
        c = rnd.choice((KORALL, IZUMRUD, ZOLOTO, MOLOKO, VINO, LAVANDA, BEZH))
        kach = 1.6 * A.w(t, 2.4 + .2 * i, i * .3)
        s += (f'<g transform="rotate({kach:.2f} {px:.0f} {y:.0f})">'
              f'<rect x="{px-11:.0f}" y="{y-h_:.0f}" width="22" height="{h_:.0f}"'
              f' rx="5" fill="{c}" {o(3)}/>'
              f'<rect x="{px-14:.0f}" y="{y-h_-5:.0f}" width="28" height="7"'
              f' rx="3" fill="{SEREBRO}" {o(2)}/></g>')
        s += (f'<path d="M{px:.0f},{y-h_*.5:.0f} q{rnd.uniform(-9,9):.0f},10'
              f' {rnd.uniform(-14,14):.0f},22" fill="none" stroke="{c}"'
              f' stroke-width="2" opacity=".7"/>')
    return s


def _katushki_tk(x, y, t, n=6, seed=11):
    """Катушки ниток россыпью — сквозная мелочь всех швейных сцен."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        cx = x + i * 46 + rnd.uniform(-7, 7)
        cy = y + rnd.uniform(-10, 10)
        c = rnd.choice((ALYY, VINO, IZUMRUD, ZOLOTO, TSINIY, MOLOKO))
        kr = 2.2 * A.w(t, 3.0, i * .4)
        s += (f'<g transform="rotate({kr:.2f} {cx:.0f} {cy:.0f})">'
              f'<rect x="{cx-13:.0f}" y="{cy-26:.0f}" width="26" height="52" rx="6"'
              f' fill="{c}" {o(3)}/>'
              f'<rect x="{cx-16:.0f}" y="{cy-30:.0f}" width="32" height="8" rx="3"'
              f' fill="{DEREVO2}" {o(2)}/>'
              f'<rect x="{cx-16:.0f}" y="{cy+22:.0f}" width="32" height="8" rx="3"'
              f' fill="{DEREVO2}" {o(2)}/></g>')
    return s


def lavandovyy_i_svetlo_seryy(t):
    """Окно, сухая лаванда в кувшине и серый кот; рядом на плечиках лавандовая
    блузка и светло-серая юбка — наряд повторяет то, что уже есть в комнате."""
    rnd = random.Random(2035)
    s = f'<rect width="{W}" height="{H}" fill="#2a2430"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 11))
    s += SL(Z_DAL, doski(0, 0, W, 820, 92))
    s += SL(Z_DAL, okno_izby(1060, 90, 700, 540, t, svet=False, moroz=.30))
    s += SL(Z_DAL, sneg_letit(t, 26, 7, .55, .7))
    s += SL(Z_DAL, zanaveska(1030, 80, 580, 150, "#e4e8f3", t, 1))
    s += SL(Z_DAL, zanaveska(1770, 80, 580, 150, "#e4e8f3", t, -1))
    s += SL(Z_SRED, _polka_melochey(70, 300, 420, t, 35, 6))
    # подоконник
    s += SL(Z_SRED, f'<rect x="1000" y="620" width="860" height="34" rx="8"'
                    f' fill="url(#derev)" {o(6)}/>')
    # кувшин с сухой лавандой: сам букет и есть «лавандовый» оттенок сцены
    kx, ky = 1180, 620
    s += SL(Z_SRED, f'<path d="M{kx-54},{ky} q-16,-96 20,-128 q-8,-26 14,-30'
                    f' q22,4 14,30 q36,32 20,128 Z" fill="url(#glina)" {o(6)}/>')
    for i in range(11):
        a = -74 + i * 9 + 3.2 * A.w(t, 2.2, i * .22)
        dl = rnd.uniform(130, 210)
        ex = kx + dl * math.cos(math.radians(a))
        ey = ky - 150 + dl * math.sin(math.radians(a))
        s += SL(Z_SRED, f'<path d="M{kx},{ky-150} Q{(kx+ex)/2+10:.0f},'
                        f'{(ky-150+ey)/2:.0f} {ex:.0f},{ey:.0f}" fill="none"'
                        f' stroke="#6f7a52" stroke-width="4"/>')
        for j in range(4):
            bx = ex + rnd.uniform(-9, 9)
            by = ey + j * 11
            s += SL(Z_SRED, f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="7" ry="11"'
                            f' fill="{LAVANDA}" opacity=".9"/>')
    # серый кот на пол-кадра: открывает один глаз
    s += SL(0, kot(1560, 620, t, 2.3, SERYY))
    # плечики с лавандовой блузкой и светло-серой юбкой
    s += SL(0, naryad_plechiki(430, 180, 440, t, LAVANDA, 1.25, .1, True, MOLOKO, .10, 21))
    s += SL(0, naryad_plechiki(760, 210, 380, t, "#b9bcc4", 1.15, .5, True, None, .06, 22))
    # стол с книгой, чашкой и салфеткой
    s += SL(Z_SRED, stol(240, 880, 620, 34))
    s += SL(Z_SRED, f'<path d="M300,870 h210 l-10,-54 h-190 Z" fill="{MOLOKO}" {o(4)}/>'
                    f'<path d="M305,845 h196" stroke="{K}" stroke-width="3" opacity=".4"/>')
    s += SL(Z_SRED, f'<path d="M560,872 q-8,-56 34,-58 q42,2 34,58 Z" fill="{KREM2}" {o(4)}/>'
                    f'<path d="M628,838 q26,6 22,26 q-6,16 -24,12" fill="none"'
                    f' stroke="{KREM2}" stroke-width="7"/>')
    s += SL(Z_SRED, par(594, 820, t, 3, .45, 120, .4, .8))
    for i in range(9):
        sx = 300 + i * 26
        s += SL(Z_SRED, f'<path d="M{sx},900 q13,14 26,0" fill="none"'
                        f' stroke="{MOLOKO}" stroke-width="3" opacity=".55"/>')
    s += SL(Z_SRED, svecha(840, 876, t, .3, 1.1))
    s += SL(Z_SRED, _katushki_tk(120, 848, t, 5, 7))
    s += SL(Z_SRED, teplo(840, 820, 420, 330, .26 + .07 * abs(A.w(t, 1.7))))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def albom_obrazcov_tkani(t):
    """Раскрытый альбом образцов: пары лоскутов приподнимаются по очереди и
    получают номер — это и есть действие сцены."""
    rnd = random.Random(2036)
    s = f'<rect width="{W}" height="{H}" fill="#241d19"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 5))
    s += SL(Z_DAL, doski(0, 0, W, 560, 84))
    s += SL(Z_DAL, _polka_melochey(1420, 300, 440, t, 36, 7))
    s += SL(Z_DAL, okno_izby(120, 90, 420, 330, t, svet=False, moroz=.42))
    s += SL(Z_SRED, stol(120, 980, 1700, 44))
    # альбом: два разворота, шесть пар лоскутов
    ax, ay = 420, 540
    s += SL(Z_SRED, f'<path d="M{ax},{ay} q540,-44 1080,0 l0,400 q-540,44 -1080,0 Z"'
                    f' fill="{KREM2}" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M{ax+540},{ay-22} l0,418" stroke="{K}"'
                    f' stroke-width="6" opacity=".55"/>')
    PARY = ((ALYY, MOLOKO), (VINO, ZOLOTO), (IZUMRUD, ZOLOTO),
            (TERRAKOT, BEZH), (TSINIY, SEREBRO), (KORALL, MOLOKO))
    for i, (c1, c2) in enumerate(PARY):
        kol, ryad = i % 3, i // 3
        px = ax + 90 + kol * 320 + ryad * 10
        py = ay + 70 + ryad * 190
        podnyat = A.out(A.seg(t, .4 + i * .35, .8)) if i < 3 else 0.0
        dy = -34 * podnyat
        for j, c in enumerate((c1, c2)):
            lx = px + j * 118
            s += SL(Z_SRED, f'<g transform="translate(0,{dy:.1f})">'
                            f'<path d="M{lx},{py} h104 l-6,132 h-92 Z" fill="{c}" {o(4)}/>'
                            f'{skladki(lx, py, 104, 132, c, 3, 40 + i * 3 + j, t, 2.0)}'
                            f'<circle cx="{lx+52}" cy="{py+8}" r="7" fill="{SEREBRO}" {o(2)}/>'
                            f'</g>')
        if i < 3 and podnyat > .25:
            s += SL(Z_SRED, f'<circle cx="{px+112:.0f}" cy="{py-52+dy:.0f}" r="26"'
                            f' fill="{ZOLOTO}" opacity="{min(1, podnyat):.2f}" {o(3)}/>')
    # мелочь портного вокруг
    s += SL(Z_SRED, _katushki_tk(190, 930, t, 6, 12))
    s += SL(Z_SRED, f'<path d="M1540,950 l120,-34 l10,22 l-120,34 Z" fill="{MOLOKO}" {o(3)}/>')
    for i in range(12):
        s += SL(Z_SRED, f'<path d="M{1546+i*10},{944-i*2.8:.0f} l0,16"'
                        f' stroke="{K}" stroke-width="2" opacity=".55"/>')
    s += SL(Z_SRED, f'<path d="M1420,978 l64,-56 l16,18 l-64,56 Z" fill="{SEREBRO}" {o(3)}/>'
                    f'<circle cx="1414" cy="984" r="15" fill="none" stroke="{SEREBRO}"'
                    f' stroke-width="6"/>')
    s += SL(0, lampa_stolika(1700, 880, t, 1.25))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def magazin_tkaney_vecherom(t):
    """Прилавок магазина тканей: рулоны стеной, продавщица разматывает винный
    отрез, покупательница трогает его рукавом."""
    rnd = random.Random(2038)
    s = f'<rect width="{W}" height="{H}" fill="#2b2119"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 7))
    s += SL(Z_DAL, doski(0, 0, W, 460, 78))
    # стена рулонов
    for i in range(14):
        rx = 70 + i * 132
        h_ = 300 + (i % 4) * 46
        c = (ALYY, VINO, IZUMRUD, TSINIY, TERRAKOT, MOLOKO, KORALL, LAVANDA,
             BEZH, HVOYA, RUBIN, KREM2, SERYY, PUDRA)[i]
        kach = 1.2 * A.w(t, 3.2, i * .2)
        s += SL(Z_DAL, f'<g transform="rotate({kach:.2f} {rx:.0f} 620)">'
                       f'<rect x="{rx-52:.0f}" y="{620-h_:.0f}" width="104" height="{h_:.0f}"'
                       f' rx="22" fill="{c}" {o(5)}/>'
                       f'<ellipse cx="{rx:.0f}" cy="{620-h_:.0f}" rx="52" ry="16"'
                       f' fill="{c}" stroke="{K}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<rect x="0" y="690" width="{W}" height="54" fill="url(#derev)" {o(6)}/>')
    # прилавок
    s += SL(Z_SRED, f'<rect x="120" y="744" width="1680" height="150" rx="10"'
                    f' fill="{DEREVO}" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="120" y="744" width="1680" height="16" fill="#ffffff"'
                    f' opacity=".14"/>')
    # винный отрез разматывается
    raz = A.out(A.seg(t, .3, 2.0))
    s += SL(0, otrez(430, 700, 300 + 620 * raz, 190, VINO, t, 14, .22, .1))
    s += SL(0, tkan_blesk(430, 700, 300 + 620 * raz, 190, t, "#ffffff", .30, .2))
    # продавщица за прилавком, обе руки на рулоне
    s += SL(Z_SRED, figura(320, 760, 420, t, IZUMRUD, TEPLO_SVET, .1, False, False,
                           1.0, 2.5, True, True, "#f0cfae", False, MOLOKO, False))
    ruk, (hx, hy) = rukav(452, 686, 118, -6 + 9 * A.w(t, 1.6), t, IZUMRUD, TEPLO_SVET, .2, 5.0)
    s += SL(Z_SRED, ruk)
    # покупательница перед прилавком, рукав трогает ткань, вторая рука с сумкой
    s += SL(0, figura(1430, 1010, 470, t, TSINIY, HOLOD_KANT, .5, False, False,
                      1.0, 2.0, True, True, "#eec9a6", True, KORALL, True))
    ruk2, (h2x, h2y) = rukav(1330, 836, 150, -170 + 7 * A.w(t, 1.9, .3), t,
                             TSINIY, HOLOD_KANT, .4, 6.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M1520,860 q34,-10 52,18 l12,92 h-96 l12,-92 Z"'
               f' fill="{GRAFIT}" {o(4)}/>')
    # касса, метр, ножницы на шнурке
    s += SL(Z_SRED, f'<rect x="1570" y="610" width="190" height="130" rx="12"'
                    f' fill="{CHUGUN}" {o(6)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<circle cx="{1596+(i%3)*58}" cy="{642+(i//3)*32}" r="11"'
                        f' fill="{KREM2}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M150,744 h260 l0,14 h-260 Z" fill="{MOLOKO}" {o(3)}/>')
    for i in range(13):
        s += SL(Z_SRED, f'<path d="M{160+i*20},744 l0,14" stroke="{K}" stroke-width="2"/>')
    kach = 7 * A.w(t, 2.1, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.2f} 1050 610)">'
                    f'<path d="M1050,610 l0,70" stroke="{BEZH}" stroke-width="4"/>'
                    f'<path d="M1030,680 l40,34 M1070,680 l-40,34" stroke="{SEREBRO}"'
                    f' stroke-width="8" stroke-linecap="round"/></g>')
    s += SL(0, lampa_stolika(1050, 470, t, 1.5))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def pyat_tkaney_na_prilavke(t):
    """Пять отрезов веером: рукав проводит по каждому, и каждый отзывается
    по-своему — бархат темнеет, шифон взлетает, кружево даёт тень, трикотаж
    тянется, атлас пускает блик."""
    rnd = random.Random(2039)
    s = f'<rect width="{W}" height="{H}" fill="#241b15"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 9))
    s += SL(Z_DAL, doski(0, 0, W, 420, 76))
    s += SL(Z_DAL, _polka_melochey(60, 300, 420, t, 39, 6))
    s += SL(Z_DAL, _polka_melochey(1440, 300, 420, t, 41, 6))
    # витрина за прилавком: сначала рисованный вид, потом метка, потом переплёт
    px, py, pw, ph = 570, 120, 780, 300
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#1d2630"/>'
            + otrez(px + 24, py + 30, pw - 48, ph - 70, TSINIY, t, 58, .25, .2)
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-14}" y="{py-14}" width="{pw+28}" height="{ph+28}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="22"/>'
            + f'<path d="M{px+pw/2:.0f},{py-14} l0,{ph+28}" stroke="{DEREVO2}"'
              f' stroke-width="12"/>')
    s += SL(Z_SRED, f'<rect x="0" y="560" width="{W}" height="520" fill="{DEREVO}" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="0" y="560" width="{W}" height="18" fill="#ffffff" opacity=".12"/>')
    TK = ((VINO, "бархат"), (MOLOKO, "шифон"), (KREM2, "кружево"),
          (TERRAKOT, "трикотаж"), (KREM2, "атлас"))
    hod = A.seg(t, .3, 4.2)
    aktiv = min(4, int(hod * 5))
    for i, (c, _) in enumerate(TK):
        x = 150 + i * 330
        ug = -16 + i * 8
        zhiv = (abs(A.w(t, 1.6, i * .3)) if i == aktiv else .18)
        s += SL(Z_SRED, f'<g transform="rotate({ug:.1f} {x+140:.0f} 700)">')
        if i == 0:        # бархат темнеет полосой
            s += SL(Z_SRED, otrez(x, 620, 280, 300, c, t, 50, 0, .1))
            s += SL(Z_SRED, f'<rect x="{x+40+90*zhiv:.0f}" y="620" width="80" height="300"'
                            f' fill="#000000" opacity="{.30*zhiv+.10:.2f}"/>')
        elif i == 1:      # шифон приподнимается
            s += SL(Z_SRED, otrez(x, 600 - 40 * zhiv, 280, 300, c, t, 51, .12, .2))
        elif i == 2:      # кружево бросает узорную тень
            s += SL(Z_SRED, otrez(x, 620, 280, 300, c, t, 52, 0, .3))
            for j in range(18):
                cx = x + 26 + (j % 6) * 44
                cy = 660 + (j // 6) * 74
                s += SL(Z_SRED, f'<circle cx="{cx}" cy="{cy}" r="15" fill="none"'
                                f' stroke="{K}" stroke-width="3" opacity=".45"/>')
                s += SL(Z_SRED, f'<circle cx="{cx+14}" cy="{cy+66}" r="9" fill="{K}"'
                                f' opacity="{.14+.12*zhiv:.2f}"/>')
        elif i == 3:      # трикотаж тянется
            s += SL(Z_SRED, otrez(x, 620, 280 + 54 * zhiv, 300, c, t, 53, 0, .4))
        else:             # атлас пускает блик
            s += SL(Z_SRED, otrez(x, 620, 280, 300, c, t, 54, .5, .5))
            s += SL(Z_SRED, tkan_blesk(x, 620, 280, 300, t, "#ffffff", .55, .5))
        s += SL(Z_SRED, "</g>")
    # рукав покупательницы идёт по тканям
    rx = 190 + 330 * aktiv + 120
    ruk, (hx, hy) = rukav(rx, 420, 190, 74, t, TSINIY, HOLOD_KANT, .2, 5.0, True)
    s += SL(0, ruk)
    s += SL(Z_SRED, _katushki_tk(120, 1010, t, 6, 21))
    s += SL(Z_SRED, f'<path d="M1500,1006 l80,-62 l18,20 l-80,62 Z" fill="{SEREBRO}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1660,1010 h180 l0,12 h-180 Z" fill="{MOLOKO}" {o(3)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{1668+i*20},1010 l0,12" stroke="{K}" stroke-width="2"/>')
    s += SL(0, lampa_stolika(960, 430, t, 1.4))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def barhatnaya_portera(t):
    """Тяжёлая рубиновая портьера с кистью; девочка обнимает её и прижимается
    щекой. В раме у окна — настоящий рубиновый бархат."""
    rnd = random.Random(2040)
    s = f'<rect width="{W}" height="{H}" fill="#1e1512"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 13))
    s += SL(Z_DAL, stena("oboi", t, 105))
    s += SL(Z_DAL, sneg_letit(t, 22, 9, .45, .6))
    # место настоящего кадра: рама портьеры у окна слева, 800x420 стоймя
    # НАСТОЯЩИЙ КАДР ОТСЮДА СНЯТ: клип бархата был почти чёрным и читался бы
    # пустой рамкой (гейт «в окне нет почти чёрного клипа»). Рисованный бархат
    # в раме остаётся — сцена от этого не беднеет.
    px, py, pw, ph = 60, 300, 780, 420
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#2a0d14"/>'
                    + otrez(px + 20, py + 16, pw - 40, ph - 40, RUBIN, t, 61, .18, .2)
                    + skladki(px + 40, py + 40, pw - 80, ph - 90, RUBIN, 7, 62, t, 4.0)
                    + zerkalo(px, py, pw, ph, t, "pryam", DEREVO2, True))
    # сама портьера справа, на пол-кадра
    for i in range(9):
        fx = 880 + i * 86
        tem = .22 + .22 * (0.5 + 0.5 * math.cos(2 * math.pi * ((t * .35 + i * .12) % 1.0)))
        s += SL(0, f'<path d="M{fx},180 q{18+8*A.w(t,2.6,i*.2):.0f},440 {-6:.0f},880'
                   f' l78,0 q{-10:.0f},-440 {-12:.0f},-880 Z" fill="{RUBIN}" {o(5)}/>')
        s += SL(0, f'<path d="M{fx},180 q{18:.0f},440 {-6:.0f},880 l78,0'
                   f' q{-10:.0f},-440 {-12:.0f},-880 Z" fill="#000000"'
                   f' opacity="{tem*.5:.2f}"/>')
    s += SL(0, f'<rect x="860" y="150" width="800" height="46" rx="12"'
               f' fill="{DEREVO2}" {o(6)}/>')
    # шнур с кистью
    kx = 1320
    kach = 6 * A.w(t, 1.9, .1)
    s += SL(0, f'<g transform="rotate({kach:.2f} {kx} 560)">'
               f'<path d="M{kx-180},560 q180,52 360,0" fill="none" stroke="{ZOLOTO}"'
               f' stroke-width="12"/>'
               f'<path d="M{kx},600 l0,56" stroke="{ZOLOTO}" stroke-width="10"/>'
               f'<path d="M{kx-44},656 h88 l-14,96 h-60 Z" fill="{ZOLOTO}" {o(4)}/>')
    for i in range(7):
        s += SL(0, f'<path d="M{kx-36+i*12},752 l{-2+i*.6:.1f},44" stroke="{ZOLOTO}"'
                   f' stroke-width="4"/>')
    s += SL(0, "</g>")
    # девочка обнимает портьеру и прижимается щекой
    s += SL(0, figura(860, 1020, 380, t, IZUMRUD, TEPLO_SVET, .3, False, True,
                      1.0, 3.5, True, True, "#f3d3b2", True, MOLOKO, True))
    ruk, _ = rukav(916, 800, 128, -24, t, IZUMRUD, TEPLO_SVET, .2, 4.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(916, 848, 120, 8, t, IZUMRUD, TEPLO_SVET, .5, 4.0)
    s += SL(0, ruk2)
    # комната: кресло, торшер, рояль, ёлка
    s += SL(Z_SRED, f'<path d="M820,1030 q-30,-180 70,-186 l0,186 Z" fill="#4a3a52" {o(5)}/>')
    s += SL(Z_DAL, elka(1840, 1040, 420, t, 1.0, True, 17))
    s += SL(Z_DAL, f'<rect x="300" y="880" width="520" height="150" rx="10"'
                   f' fill="#1b1b22" {o(6)}/>')
    for i in range(16):
        s += SL(Z_DAL, f'<rect x="{320+i*30}" y="884" width="20" height="40"'
                       f' fill="{MOLOKO}" {o(2)}/>')
    s += SL(Z_SRED, girlyanda(140, 180, 760, t, 8, 23, 56))
    s += SL(Z_SRED, lampa_stolika(960, 900, t, 1.1))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.46)
    return s


def shifon_i_trikotazh(t):
    """Кадр надвое: слева шифоновая блузка у балкона, справа трикотажное
    платье само садится по форме манекена."""
    rnd = random.Random(2041)
    s = f'<rect width="{W}" height="{H}" fill="#262029"/>'
    s += SL(Z_NEBO, nebo("sumer", t, False, 15))
    s += SL(Z_DAL, stena("kraska", t, 106))
    s += SL(Z_DAL, f'<path d="M960,0 l0,1080" stroke="{K}" stroke-width="6" opacity=".35"/>')
    # ЛЕВО: балконная дверь, за ней вечер и снег; ветер тянет ткань
    s += SL(Z_DAL, f'<rect x="150" y="150" width="620" height="760" rx="14"'
                   f' fill="#121a24" {o(7)}/>')
    s += SL(Z_DAL, sneg_letit(t, 30, 3, .6, .9))
    s += SL(Z_DAL, f'<rect x="150" y="150" width="620" height="760" rx="14" fill="none"'
                   f' stroke="{DEREVO2}" stroke-width="18"/>')
    s += SL(Z_DAL, f'<path d="M460,150 l0,760" stroke="{DEREVO2}" stroke-width="12"/>')
    for i in range(5):
        oy = 300 + i * 120
        s += SL(Z_DAL, f'<path d="M170,{oy} q200,{-26+10*A.w(t,2.2,i*.3):.0f} 580,0"'
                       f' fill="none" stroke="{MOLOKO}" stroke-width="3" opacity=".22"/>')
    veter = A.w(t, 1.8)
    s += SL(0, naryad_plechiki(420, 250, 430, t, MOLOKO, 1.2, .2, True, None, .18, 31, 5.0))
    for i in range(6):
        ax = 300 + i * 46
        s += SL(0, f'<path d="M{ax},420 q{40+26*veter:.0f},90 {24+34*veter:.0f},190"'
                   f' fill="none" stroke="{MOLOKO}" stroke-width="5" opacity=".55"/>')
    # ПРАВО: манекен, трикотажное платье садится по форме
    sad = A.out(A.seg(t, .45, 1.5))
    s += SL(0, manekken(1420, 980, 700, t, KREM2, "zh",
                        TERRAKOT if sad > .25 else None, .3, None, .06, 33))
    s += SL(0, f'<path d="M{1420-170-60*(1-sad):.0f},{430-70*(1-sad):.0f}'
               f' q{170+60*(1-sad):.0f},-40 {340+120*(1-sad):.0f},0'
               f' l-30,{90+40*(1-sad):.0f} q-150,30 -300,0 Z"'
               f' fill="{TERRAKOT}" opacity="{.35+.6*(1-sad):.2f}" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(1680, 260, 200, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1690" y="270" width="180" height="500" fill="{STEKLO}"'
                    f' opacity=".30"/>')
    s += SL(Z_SRED, f'<path d="M1740,420 q40,-16 80,0 l-14,320 h-54 Z" fill="{KREM2}"'
                    f' opacity=".55"/>')
    # обжитый второй план: стул, корзина, цветок, коробки
    s += SL(Z_SRED, f'<rect x="1020" y="760" width="150" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="1030" y="786" width="18" height="240" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1142" y="786" width="18" height="240" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1026" y="600" width="140" height="170" rx="8"'
                    f' fill="{DEREVO2}" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M820,1030 q-26,-130 58,-134 q84,4 58,134 Z"'
                    f' fill="url(#solom)" {o(5)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{806+i*22},940 l0,90" stroke="{MED}"'
                        f' stroke-width="3" opacity=".6"/>')
    s += SL(Z_SRED, f'<path d="M1240,1030 l0,-120" stroke="#3e5a3a" stroke-width="10"/>')
    for i in range(5):
        a = -60 + i * 30 + 4 * A.w(t, 2.6, i * .3)
        s += SL(Z_SRED, f'<ellipse cx="{1240+58*math.cos(math.radians(a)):.0f}"'
                        f' cy="{900+40*math.sin(math.radians(a)):.0f}" rx="30" ry="16"'
                        f' fill="#3e5a3a" {o(3)}/>')
    s += SL(Z_SRED, girlyanda(1000, 120, 860, t, 9, 37, 50))
    s += SL(Z_SRED, lampa_stolika(1120, 700, t, 1.0))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.42)
    return s


def tkan_na_oschup(t):
    """Четыре отреза, рукав ложится на каждый: над шерстью, вискозой и шёлком
    всплывают облачка-подушки, над синтетикой — ёжик с молниями."""
    rnd = random.Random(2042)
    s = f'<rect width="{W}" height="{H}" fill="#221c17"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 17))
    s += SL(Z_DAL, doski(0, 0, W, 480, 82))
    s += SL(Z_DAL, _polka_melochey(1400, 290, 460, t, 42, 7))
    s += SL(Z_SRED, stol(80, 1000, 1760, 46))
    CV = (BEZH, LAVANDA, KREM2, "#5f6b7a")
    hod = A.seg(t, .3, 4.0)
    akt = min(3, int(hod * 4))
    for i, c in enumerate(CV):
        x = 130 + i * 430
        s += SL(Z_SRED, otrez(x, 640, 360, 330, c, t, 70 + i, .10 if i == 2 else 0, i * .2))
        if i == 3:
            top = abs(A.w(t, 1.4)) if i == akt else .25
            for j in range(16):
                jx = x + 20 + j * 21
                s += SL(Z_SRED, f'<path d="M{jx},640 l{4-8*(j%2)},{-26-20*top:.0f}"'
                                f' stroke="#5f6b7a" stroke-width="5"/>')
    # рукав ведёт по тканям
    rx = 310 + 430 * akt
    ruk, (hx, hy) = rukav(rx, 330, 250, 86, t, VINO, TEPLO_SVET, .2, 4.0, True)
    s += SL(0, ruk)
    # облачка-подушки над мягкими и ёжик с молниями над синтетикой
    for i in range(3):
        if i > akt:
            continue
        ox = 310 + i * 430
        p = A.out(A.seg(t, .5 + i * .5, .7))
        s += SL(0, f'<g opacity="{p:.2f}">'
                   f'<ellipse cx="{ox}" cy="{540-40*p:.0f}" rx="118" ry="66"'
                   f' fill="{MOLOKO}" {o(4)}/>'
                   f'<ellipse cx="{ox-64}" cy="{566-40*p:.0f}" rx="62" ry="42"'
                   f' fill="{MOLOKO}" {o(3)}/>'
                   f'<ellipse cx="{ox+68}" cy="{566-40*p:.0f}" rx="56" ry="38"'
                   f' fill="{MOLOKO}" {o(3)}/></g>')
    if akt == 3:
        ex, ey = 1600, 520
        p = abs(A.w(t, 1.2))
        s += SL(0, f'<ellipse cx="{ex}" cy="{ey}" rx="96" ry="72" fill="#6b5a46" {o(4)}/>')
        for j in range(16):
            a = -170 + j * 21
            s += SL(0, f'<path d="M{ex+86*math.cos(math.radians(a)):.0f},'
                       f'{ey+64*math.sin(math.radians(a)):.0f}'
                       f' l{(26+12*p)*math.cos(math.radians(a)):.0f},'
                       f'{(26+12*p)*math.sin(math.radians(a)):.0f}"'
                       f' stroke="#4a3b2c" stroke-width="6" stroke-linecap="round"/>')
        for j in range(4):
            zx = ex - 150 + j * 100
            s += SL(0, f'<path d="M{zx},{ey+120} l26,44 l-18,6 l30,56 l-44,-50 l20,-8 Z"'
                       f' fill="{ZOLOTO}" opacity="{.4+.5*p:.2f}"/>')
    s += SL(Z_SRED, _katushki_tk(140, 1046, t, 5, 31))
    s += SL(Z_SRED, f'<path d="M1520,1040 l90,-66 l18,22 l-90,66 Z" fill="{SEREBRO}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1300,1052 q46,-26 92,0" fill="none" stroke="{SEREBRO}"'
                    f' stroke-width="5"/>')
    s += SL(0, lampa_stolika(900, 470, t, 1.35))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def ladon_na_tkani_i_vecher(t):
    """Рукав-варежка отдыхает на винной ткани, и над ним вырастает картинка
    вечера: та же женщина за праздничным столом, стрелки бегут к полуночи."""
    rnd = random.Random(2043)
    s = f'<rect width="{W}" height="{H}" fill="#241a18"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 19))
    s += SL(Z_DAL, doski(0, 0, W, 520, 80))
    s += SL(Z_DAL, _polka_melochey(80, 300, 400, t, 43, 6))
    s += SL(Z_SRED, stol(60, 1010, 1800, 46))
    s += SL(Z_SRED, otrez(180, 700, 820, 300, VINO, t, 44, .14, .1))
    # варежка-ладонь лежит и не уходит
    mx, my = 560, 700
    dy = 6 * A.w(t, 1.1)
    s += SL(0, f'<g transform="translate(0,{dy:.1f})">'
               f'<ellipse cx="{mx}" cy="{my+30}" rx="150" ry="86" fill="{GRAFIT}" {o(6)}/>'
               f'<ellipse cx="{mx-96}" cy="{my+58}" rx="54" ry="44" fill="{GRAFIT}" {o(4)}/>'
               f'<path d="M{mx+110},{my-20} q90,-30 150,-130" fill="none"'
               f' stroke="{GRAFIT}" stroke-width="64" stroke-linecap="round"/></g>')
    # картинка вечера растёт над рукой
    p = A.out(A.seg(t, .35, 1.5))
    kx, ky, kw, kh = 1060, 220, 740, 480
    s += SL(0, f'<g opacity="{p:.2f}" transform="translate({kx+kw/2:.0f},{ky+kh/2:.0f})'
               f' scale({.6+.4*p:.2f}) translate({-kx-kw/2:.0f},{-ky-kh/2:.0f})">')
    s += SL(0, f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="22"'
               f' fill="#2d2230" {o(6)}/>')
    s += SL(0, f'<rect x="{kx+28}" y="{ky+300}" width="{kw-56}" height="30" rx="8"'
               f' fill="{MOLOKO}" {o(4)}/>')
    for i in range(6):
        s += SL(0, f'<circle cx="{kx+90+i*110}" cy="{ky+288}" r="18" fill="{KREM2}" {o(2)}/>')
    s += SL(0, figura(kx + 250, ky + 300, 250, t, VINO, TEPLO_SVET, .2, False, False,
                      1.0, 1.5, True, True, "#f0cfae", True, ZOLOTO, False))
    s += SL(0, f'<path d="{kontur_proema(kx+360, ky+150, 110, 130, "ellips")}"'
               f' fill="{STEKLO}" opacity=".6"/>')
    # часы над столом: стрелки бегут к полуночи
    cx2, cy2 = kx + 580, ky + 120
    s += SL(0, f'<circle cx="{cx2}" cy="{cy2}" r="78" fill="{MOLOKO}" {o(5)}/>')
    for i in range(12):
        a = i * 30
        s += SL(0, f'<path d="M{cx2+62*math.cos(math.radians(a)):.0f},'
                   f'{cy2+62*math.sin(math.radians(a)):.0f} l'
                   f'{10*math.cos(math.radians(a)):.0f},'
                   f'{10*math.sin(math.radians(a)):.0f}" stroke="{K}" stroke-width="4"/>')
    beg = -90 + 320 * A.seg(t, .6, 1.8)
    s += SL(0, f'<path d="M{cx2},{cy2} l{54*math.cos(math.radians(beg)):.0f},'
               f'{54*math.sin(math.radians(beg)):.0f}" stroke="{K}" stroke-width="7"'
               f' stroke-linecap="round"/>')
    s += SL(0, f'<path d="M{cx2},{cy2} l0,-38" stroke="{K}" stroke-width="9"'
               f' stroke-linecap="round"/>')
    s += SL(0, "</g>")
    s += SL(Z_SRED, _katushki_tk(1180, 1046, t, 5, 47))
    s += SL(Z_SRED, f'<path d="M1420,1046 l88,-64 l18,22 l-88,64 Z" fill="{SEREBRO}" {o(3)}/>')
    s += SL(Z_SRED, svecha(1660, 1006, t, .2, 1.3))
    s += SL(0, lampa_stolika(300, 640, t, 1.2))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.44)
    return s


def tri_muzhskie_tkani(t):
    """Три мужских торса в ряд: вельвет, шерсть, твид. Мужское ателье вокруг —
    зеркало, галстуки, колодки, утюг с паром."""
    rnd = random.Random(2044)
    s = f'<rect width="{W}" height="{H}" fill="#241e18"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 23))
    s += SL(Z_DAL, stena("oboi", t, 109))
    s += SL(Z_DAL, _polka_melochey(60, 280, 420, t, 44, 6))
    # полка с галстуками
    gal = polka(1420, 300, 440)
    for i in range(7):
        gx = 1452 + i * 60
        kach = 3.4 * A.w(t, 2.4, i * .3)
        c = (VINO, TSINIY, IZUMRUD, GRAFIT, RUBIN, HVOYA, TERRAKOT)[i]
        gal += (f'<g transform="rotate({kach:.2f} {gx} 300)">'
                f'<path d="M{gx-13},300 l26,0 l-5,150 l-16,0 Z" fill="{c}" {o(3)}/>'
                f'<path d="M{gx-10},300 l20,0 l-4,26 l-12,0 Z" fill="#ffffff" opacity=".2"/>'
                f'</g>')
    s += SL(Z_DAL, gal)
    s += SL(Z_SRED, polovicy(1010))
    TK = ((TERRAKOT, "вельвет"), (GRAFIT, "шерсть"), (BEZH, "твид"))
    for i, (c, _) in enumerate(TK):
        x = 400 + i * 440
        s += SL(0, manekken(x, 960, 620, t, KREM2, "m", c, i * .3, MOLOKO, .05, 50 + i))
        if i == 0:                      # рубчик вельвета
            rub = "".join(f'<path d="M{x-150+j*14},520 l0,230" stroke="#8c3f22"'
                          f' stroke-width="3" opacity=".55"/>' for j in range(22))
            s += SL(0, rub)
        elif i == 2:                    # мелкая клетка твида
            kl = "".join(f'<path d="M{x-150+j*26},520 l0,230" stroke="#9a8460"'
                         f' stroke-width="2" opacity=".5"/>' for j in range(12))
            kl += "".join(f'<path d="M{x-150},{530+j*26} l300,0" stroke="#9a8460"'
                          f' stroke-width="2" opacity=".5"/>' for j in range(9))
            s += SL(0, kl)
        pod = A.out(A.seg(t, .4 + i * .3, .7))
        s += SL(0, f'<rect x="{x-110:.0f}" y="{300-30*pod:.0f}" width="220" height="56"'
                   f' rx="10" fill="{GRAFIT}" opacity="{pod*.9:.2f}" {o(3)}/>')
    # утюг с паром и гладильная доска
    s += SL(Z_SRED, f'<path d="M1560,900 l250,-30 l10,70 l-250,30 Z" fill="{MOLOKO}" {o(6)}/>'
                    f'<path d="M1600,970 l0,110 M1770,952 l0,128" stroke="{SEREBRO}"'
                    f' stroke-width="9"/>')
    s += SL(Z_SRED, f'<path d="M1640,884 q60,-44 120,-6 l6,34 l-130,16 Z"'
                    f' fill="{CHUGUN}" {o(5)}/>')
    s += SL(Z_SRED, par(1700, 864, t, 4, .5, 150, .45, 1.0))
    s += SL(Z_SRED, zerkalo(120, 420, 240, 560, t, "pryam", DEREVO2, True))
    s += SL(Z_SRED, f'<rect x="130" y="430" width="220" height="540" fill="{STEKLO}"'
                    f' opacity=".25"/>')
    kol = "".join(f'<path d="M{150+i*74},1006 q40,-66 84,-6 q-42,26 -84,6 Z"'
                  f' fill="{DEREVO2}" {o(3)}/>' for i in range(4))
    s += SL(Z_SRED, kol)
    s += SL(Z_SRED, girlyanda(60, 150, 1800, t, 11, 61, 62))
    s += SL(0, lampa_stolika(1180, 420, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def atlasnaya_bluzka_pod_lampoy(t):
    """Атласная блузка под лампой: по ней идёт мягкая волна света. В овальном
    зеркале на подставке — настоящий атлас."""
    rnd = random.Random(2046)
    s = f'<rect width="{W}" height="{H}" fill="#2a2026"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 27))
    s += SL(Z_DAL, stena("kraska", t, 110))
    s += SL(Z_DAL, elka(1840, 1060, 360, t, 1.0, True, 29))
    s += SL(Z_SRED, trumo(980, 1010, 820, 420, t))
    # овальное зеркало на подставке: сначала рисованный вид, потом метка, потом рама
    px, py, pw, ph = 170, 360, 420, 380
    put = kontur_proema(px, py, pw, ph, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#2b2420"/>'
            + otrez(px + 40, py + 60, pw - 80, ph - 140, KREM2, t, 62, .45, .2)
            + mesto_stoka(px, py, pw, ph, "ellips")
            + zerkalo(px, py, pw, ph, t, "ellips", ZOLOTO, True))
    s += SL(Z_SRED, f'<path d="M{px+pw/2-24:.0f},{py+ph:.0f} h48 l20,120 h-88 Z"'
                    f' fill="{DEREVO2}" {o(4)}/>')
    # блузка на плечиках под лампой
    s += SL(0, naryad_plechiki(880, 230, 520, t, KREM2, 1.4, .1, True, MOLOKO, .5, 63, 1.6))
    volna = (A.w(t, 3.6, .1) + 1) / 2
    s += SL(0, f'<path d="M{700+520*volna:.0f},280 q40,220 -30,480" fill="none"'
               f' stroke="#ffffff" stroke-width="54" opacity=".16"/>')
    # столик: флаконы, бусы, свеча, шарф сползает
    fl = ""
    for i in range(6):
        fx = 1180 + i * 92
        h_ = 54 + (i % 3) * 26
        fl += (f'<rect x="{fx-20}" y="{760-h_}" width="40" height="{h_}" rx="8"'
               f' fill="{(LAVANDA, KORALL, MOLOKO, ZOLOTO, PUDRA, IZUMRUD)[i]}" {o(3)}/>'
               f'<rect x="{fx-9}" y="{748-h_}" width="18" height="16" rx="4"'
               f' fill="{SEREBRO}" {o(2)}/>')
    s += SL(Z_SRED, fl)
    bus = ""
    for i in range(16):
        a = i * 22
        bus += (f'<circle cx="{1120+130*math.cos(math.radians(a)):.0f}"'
                f' cy="{800+34*math.sin(math.radians(a)):.0f}" r="11"'
                f' fill="{KORALL}" {o(2)}/>')
    s += SL(Z_SRED, bus)
    s += SL(Z_SRED, svecha(1760, 756, t, .2, 1.4))
    spolz = A.out(A.seg(t, .6, 1.6))
    s += SL(0, f'<path d="M1480,770 q70,{40+120*spolz:.0f} 20,{220+160*spolz:.0f}'
               f' l64,14 q46,{-150-160*spolz:.0f} -16,{-240-120*spolz:.0f} Z"'
               f' fill="{VINO}" {o(5)}/>')
    s += SL(0, lampa_stolika(880, 190, t, 1.6))
    s += SL(Z_SRED, teplo(880, 320, 520, 420, .30 + .08 * abs(A.w(t, 1.8))))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def nit_i_payetki(t):
    """Швейный столик: игла ведёт блестящую нить по вороту, на воротник
    ложится десяток пайеток, не больше."""
    rnd = random.Random(2047)
    s = f'<rect width="{W}" height="{H}" fill="#201a16"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 31))
    s += SL(Z_DAL, doski(0, 0, W, 520, 80))
    s += SL(Z_DAL, _polka_melochey(1400, 280, 460, t, 47, 7))
    s += SL(Z_SRED, stol(80, 1000, 1760, 48))
    # платье на столе, крупно — ворот в центре
    s += SL(Z_SRED, otrez(420, 620, 900, 380, TSINIY, t, 64, .08, .1))
    s += SL(0, f'<path d="M760,640 q110,120 220,0 q-26,96 -110,104 q-84,-8 -110,-104 Z"'
               f' fill="{TSINIY}" stroke="{K}" stroke-width="6"/>')
    # катушка блестящей нити крутится
    kx, ky = 300, 840
    kr = t * 180
    s += SL(0, f'<g transform="rotate({kr:.1f} {kx} {ky})">'
               f'<ellipse cx="{kx}" cy="{ky}" rx="86" ry="86" fill="{ZOLOTO}" {o(5)}/>'
               f'<ellipse cx="{kx}" cy="{ky}" rx="34" ry="34" fill="{DEREVO2}" {o(4)}/>'
               f'<path d="M{kx-86},{ky} h172" stroke="#ffffff" stroke-width="4"'
               f' opacity=".35"/></g>')
    # игла ведёт нить
    p = A.seg(t, .3, 2.6)
    ix = 700 + 460 * p
    s += SL(0, f'<path d="M{kx+70},{ky-30} Q{(kx+ix)/2:.0f},640 {ix:.0f},700"'
               f' fill="none" stroke="{ZOLOTO}" stroke-width="4"/>')
    s += SL(0, f'<path d="M{ix:.0f},700 l54,-40" stroke="{SEREBRO}" stroke-width="7"'
               f' stroke-linecap="round"/>')
    ruk, _ = rukav(ix + 140, 480, 170, 118, t, VINO, TEPLO_SVET, .2, 4.0, True)
    s += SL(0, ruk)
    ruk2, _ = rukav(640, 500, 160, 96, t, VINO, TEPLO_SVET, .6, 4.0, True)
    s += SL(0, ruk2)
    # пайетки ложатся по одной, их ровно десять
    pay = ""
    for i in range(10):
        if p < (i + 1) / 12.0:
            continue
        a = -74 + i * 16
        pay += (f'<circle cx="{870+96*math.cos(math.radians(a)):.0f}"'
                f' cy="{700+70*math.sin(math.radians(a)):.0f}" r="13"'
                f' fill="{SEREBRO}" opacity="{.7+.3*abs(A.w(t, 1.8, i*.2)):.2f}" {o(2)}/>')
    s += SL(0, pay)
    # блюдце с пайетками, игольница, напёрсток, ножницы
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="880" rx="140" ry="54" fill="{MOLOKO}" {o(5)}/>')
    bl = "".join(f'<circle cx="{1400+rnd.randint(0,200)}" cy="{860+rnd.randint(0,40)}"'
                 f' r="10" fill="{SEREBRO}" {o(2)}/>' for _ in range(16))
    s += SL(Z_SRED, bl)
    s += SL(Z_SRED, f'<ellipse cx="1700" cy="960" rx="62" ry="48" fill="{KORALL}" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{1660+i*18},940 l6,-30" stroke="{SEREBRO}"'
                            f' stroke-width="3"/>' for i in range(5)))
    s += SL(Z_SRED, _katushki_tk(140, 1046, t, 6, 71))
    s += SL(0, lampa_stolika(1180, 420, t, 1.4))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def blestit_chto_to_odno(t):
    """Манекен в матовом тёмном наряде: блестит по очереди что-то одно, а на
    попытку включить всё сразу манекен вспыхивает ёлкой."""
    rnd = random.Random(2048)
    s = f'<rect width="{W}" height="{H}" fill="#1f1c24"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 33))
    s += SL(Z_DAL, stena("doski", t, 112))
    s += SL(Z_DAL, elka(120, 1050, 460, t, 1.0, True, 35))
    s += SL(Z_SRED, polovicy(1030))
    s += SL(0, manekken(900, 1000, 720, t, KREM2, "zh", GRAFIT, .2, None, .04, 72))
    hod = A.seg(t, .3, 3.4)
    etap = min(4, int(hod * 5))
    yar = .55 + .45 * abs(A.w(t, 1.5))
    # 0 юбка · 1 жакет · 2 сумочка · 3 туфли · 4 всё сразу
    if etap in (0, 4):
        s += SL(0, f'<path d="M740,640 L690,980 q210,40 420,0 L1060,640 Z"'
                   f' fill="{SEREBRO}" opacity="{yar:.2f}" {o(4)}/>')
    if etap in (1, 4):
        s += SL(0, f'<path d="M760,420 h280 l24,250 h-328 Z" fill="{SEREBRO}"'
                   f' opacity="{yar:.2f}" {o(4)}/>')
    if etap in (2, 4):
        s += SL(0, f'<path d="M1120,560 q40,-14 62,16 l14,96 h-96 Z" fill="{ZOLOTO}"'
                   f' opacity="{yar:.2f}" {o(3)}/>')
    if etap in (3, 4):
        s += SL(0, tufli(1260, 1010, 1.3, SEREBRO, t))
    if etap == 4:
        for i in range(14):
            a = i * 26
            s += SL(0, f'<circle cx="{900+300*math.cos(math.radians(a)):.0f}"'
                       f' cy="{700+300*math.sin(math.radians(a)):.0f}" r="16"'
                       f' fill="{ZOLOTO}" opacity="{.3+.6*abs(A.w(t,1.1,i*.2)):.2f}"/>')
        s += SL(0, teplo(900, 700, 520, 480, .45))
    ruk, _ = rukav(640, 560, 180, 20, t, VINO, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    # зеркало «зажмуривается» на вспышке
    zm = 1.0 if etap < 4 else .22
    s += SL(Z_SRED, zerkalo(1480, 300, 360, 620, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1492" y="312" width="336" height="{596*zm:.0f}"'
                    f' fill="{STEKLO}" opacity=".32"/>')
    s += SL(Z_SRED, f'<path d="M1500,{312+596*zm:.0f} h320" stroke="{K}"'
                    f' stroke-width="10" opacity=".7"/>')
    s += SL(Z_SRED, f'<path d="M300,1030 q-26,-170 66,-176 l0,176 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, shtanga(420, 1030, 300, t, 380))
    s += SL(Z_SRED, girlyanda(60, 140, 1800, t, 12, 73, 64))
    s += SL(0, lampa_stolika(1700, 980, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def blestyaschee_i_matovoe_plate(t):
    """Два манекена рядом: у блестящего стрелки расходятся, у матового
    сходятся. Портниха показывает на правый."""
    rnd = random.Random(2049)
    s = f'<rect width="{W}" height="{H}" fill="#221f26"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 37))
    s += SL(Z_DAL, stena("oboi", t, 113))
    s += SL(Z_DAL, _polka_melochey(60, 270, 400, t, 49, 6))
    s += SL(Z_SRED, polovicy(1030))
    s += SL(0, manekken(470, 1000, 660, t, KREM2, "zh", SEREBRO, .1, None, .55, 74))
    s += SL(0, manekken(1410, 1000, 660, t, KREM2, "zh", TSINIY, .4, None, .03, 75))
    raz = A.out(A.seg(t, .4, 1.4))
    for sgn in (-1, 1):
        s += SL(0, f'<path d="M{470+sgn*(150+90*raz):.0f},700 l{sgn*86:.0f},0'
                   f' l{-sgn*26:.0f},-30 l{sgn*26:.0f},30 l{-sgn*26:.0f},30 Z"'
                   f' fill="{KORALL}" {o(3)}/>')
        s += SL(0, f'<path d="M{1410+sgn*(240-90*raz):.0f},700 l{-sgn*86:.0f},0'
                   f' l{sgn*26:.0f},-30 l{-sgn*26:.0f},30 l{sgn*26:.0f},30 Z"'
                   f' fill="{IZUMRUD}" {o(3)}/>')
    # серьги на подставке и сумочка у матового
    s += SL(0, f'<ellipse cx="1620" cy="760" rx="70" ry="46" fill="{VINO}" {o(4)}/>')
    for sgn in (-1, 1):
        s += SL(0, f'<path d="M{1620+sgn*26},740 l0,-44" stroke="{ZOLOTO}"'
                   f' stroke-width="5"/>'
                   f'<circle cx="{1620+sgn*26}" cy="{700-6*abs(A.w(t,1.7,sgn*.2)):.0f}"'
                   f' r="15" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(0, f'<path d="M1700,860 q42,-14 64,18 l14,100 h-100 Z" fill="{GRAFIT}" {o(4)}/>')
    # портниха между манекенами: правая рука показывает вправо
    s += SL(0, figura(940, 1020, 430, t, HVOYA, TEPLO_SVET, .3, False, False, 1.0,
                      2.0, True, True, "#eec9a6", False, MOLOKO, True))
    ruk, (hx, hy) = rukav(1020, 790, 190, -12 + 8 * A.w(t, 1.7), t, HVOYA, TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    s += SL(0, f'<path d="M900,700 q40,-10 80,0 l0,16 q-40,10 -80,0 Z" fill="{MOLOKO}"'
               f' {o(3)}/>')
    for i in range(6):
        s += SL(0, f'<path d="M{906+i*14},700 l0,16" stroke="{K}" stroke-width="2"/>')
    # очки
    s += SL(0, f'<circle cx="918" cy="628" r="20" fill="none" stroke="{SEREBRO}"'
               f' stroke-width="5"/><circle cx="966" cy="628" r="20" fill="none"'
               f' stroke="{SEREBRO}" stroke-width="5"/>'
               f'<path d="M938,628 h8" stroke="{SEREBRO}" stroke-width="4"/>')
    s += SL(Z_SRED, stol(60, 1020, 320, 34))
    s += SL(Z_SRED, _katushki_tk(90, 980, t, 5, 77))
    s += SL(Z_SRED, zerkalo(1760, 280, 150, 620, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(80, 150, 1760, t, 11, 79, 58))
    s += SL(0, lampa_stolika(240, 940, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def mamina_koftochka_s_lyureksom(t):
    """Комната семидесятых: мамина кофточка искрится люрексом, дочка трогает
    блестящий рукав. Сервант, проигрыватель, ёлка с дождиком."""
    rnd = random.Random(2050)
    s = f'<rect width="{W}" height="{H}" fill="#2b2119"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 41))
    s += SL(Z_DAL, stena("paneli", t, 114))
    # ковёр на стене — примета семидесятых
    s += SL(Z_DAL, f'<rect x="60" y="180" width="720" height="520" rx="8"'
                   f' fill="#7a3b2a" {o(6)}/>')
    uz = ""
    for i in range(5):
        for j in range(4):
            cx, cy = 150 + i * 140, 260 + j * 120
            uz += (f'<path d="M{cx},{cy-40} l34,40 l-34,40 l-34,-40 Z" fill="#c9a06a"'
                   f' opacity=".75"/>')
    s += SL(Z_DAL, uz)
    s += SL(Z_DAL, kvartira_veschi(1180, 700, 700, t, 11))
    s += SL(Z_SRED, polovicy(1020))
    s += SL(Z_DAL, elka(1740, 1040, 420, t, 1.0, True, 43))
    dozhd = ""
    for i in range(18):
        dx = 1600 + rnd.randint(0, 280)
        dy = 700 + rnd.randint(0, 300)
        dozhd += (f'<path d="M{dx},{dy} l0,54" stroke="{SEREBRO}" stroke-width="3"'
                  f' opacity="{.35+.5*abs(A.w(t,1.6,i*.2)):.2f}"/>')
    s += SL(Z_DAL, dozhd)
    # мама: обе руки поправляют причёску — обе рукава внешние
    s += SL(0, figura(760, 1010, 520, t, "#6a5b73", TEPLO_SVET, .2, False, False,
                      1.0, 2.0, True, True, "#f0cfae", False, None, True))
    for sgn in (-1, 1):
        ruk, _ = rukav(760 + sgn * 86, 700, 150, -70 - sgn * 16, t, "#6a5b73",
                       TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    isk = ""
    for i in range(26):
        ix = 640 + rnd.randint(0, 240)
        iy = 650 + rnd.randint(0, 180)
        fase = (t * 1.5 + i * .21) % 1.0
        isk += (f'<path d="M{ix},{iy-9} l3,9 l9,3 l-9,3 l-3,9 l-3,-9 l-9,-3 l9,-3 Z"'
                f' fill="#ffffff" opacity="{.25+.65*(0.5+0.5*math.cos(2*math.pi*fase)):.2f}"/>')
    s += SL(0, isk)
    # высокая причёска
    s += SL(0, f'<path d="M690,560 q70,-120 140,0 q-20,-70 -70,-74 q-50,4 -70,74 Z"'
               f' fill="#4a3528" {o(4)}/>')
    # дочка в бантах трогает рукав мамы
    s += SL(0, figura(1010, 1020, 300, t, KORALL, TEPLO_SVET, .6, False, False,
                      1.0, 3.0, True, True, "#f3d3b2", True, MOLOKO, True))
    ruk2, _ = rukav(956, 820, 120, -168, t, KORALL, TEPLO_SVET, .4, 5.0)
    s += SL(0, ruk2)
    for sgn in (-1, 1):
        s += SL(0, f'<path d="M{1010+sgn*48},752 q{sgn*40},-30 {sgn*54},6'
                   f' q{-sgn*30},16 {-sgn*54},-6 Z" fill="{MOLOKO}" {o(3)}/>')
    # проигрыватель на серванте
    s += SL(Z_SRED, f'<rect x="1180" y="820" width="300" height="60" rx="10"'
                    f' fill="{DEREVO2}" {o(5)}/>')
    kr = t * 90
    s += SL(Z_SRED, f'<g transform="rotate({kr:.1f} 1320 820)">'
                    f'<circle cx="1320" cy="820" r="76" fill="#1b1b1b" {o(4)}/>'
                    f'<circle cx="1320" cy="820" r="22" fill="{KORALL}" {o(2)}/>'
                    f'<path d="M1320,744 l0,152" stroke="#2d2d2d" stroke-width="3"/></g>')
    s += SL(Z_SRED, f'<path d="M1420,760 l-70,56" stroke="{SEREBRO}" stroke-width="7"'
                    f' stroke-linecap="round"/>')
    s += SL(Z_SRED, lampa_stolika(260, 900, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def krimplenovoe_plate_stoit_samo(t):
    """Кримпленовое платье стоит само, как колокол: дочка обходит его кругом,
    толкает рукавом — платье качается и встаёт обратно."""
    rnd = random.Random(2051)
    s = f'<rect width="{W}" height="{H}" fill="#2b2119"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 45))
    s += SL(Z_DAL, stena("paneli", t, 115))
    s += SL(Z_DAL, kvartira_veschi(1240, 680, 660, t, 13))
    s += SL(Z_SRED, polovicy(1030))
    s += SL(Z_DAL, elka(200, 1040, 400, t, 1.0, True, 47))
    # платье-колокол: цветастое, стоит само
    kach = 9 * A.w(t, 1.5, .1) * A.seg(t, .8, 2.4)
    s += SL(0, f'<g transform="rotate({kach:.2f} 900 1020)">')
    s += SL(0, f'<path d="M790,470 q110,-40 220,0 l130,550 q-240,50 -480,0 Z"'
               f' fill="{TERRAKOT}" {o(7)}/>')
    cv = ""
    for i in range(24):
        cx = 720 + rnd.randint(0, 360)
        cy = 520 + rnd.randint(0, 460)
        c = rnd.choice((MOLOKO, ZOLOTO, IZUMRUD, KORALL))
        for j in range(5):
            a = j * 72
            cv += (f'<ellipse cx="{cx+16*math.cos(math.radians(a)):.0f}"'
                   f' cy="{cy+16*math.sin(math.radians(a)):.0f}" rx="9" ry="13"'
                   f' fill="{c}" opacity=".85"/>')
        cv += f'<circle cx="{cx}" cy="{cy}" r="7" fill="{ZOLOTO}"/>'
    s += SL(0, cv)
    s += SL(0, skladki(700, 600, 400, 420, TERRAKOT, 7, 51, t, 3.0))
    s += SL(0, f'<ellipse cx="900" cy="470" rx="112" ry="34" fill="#20190f" opacity=".55"/>')
    s += SL(0, "</g>")
    # дочка обходит кругом и толкает рукавом
    p = A.seg(t, .2, 2.2)
    dx = 1240 - 320 * p
    s += SL(0, figura(dx, 1030, 310, t, KORALL, TEPLO_SVET, .4, False, p > .5,
                      1.0, 3.0, True, True, "#f3d3b2", True, MOLOKO, True))
    ruk, _ = rukav(dx - 60, 828, 140, -176, t, KORALL, TEPLO_SVET, .3, 6.0)
    s += SL(0, ruk)
    # утюг скучает на доске
    s += SL(Z_SRED, f'<path d="M1420,880 l260,-26 l8,62 l-260,26 Z" fill="{MOLOKO}" {o(6)}/>'
                    f'<path d="M1460,942 l0,96 M1640,926 l0,112" stroke="{SEREBRO}"'
                    f' stroke-width="8"/>')
    s += SL(Z_SRED, f'<path d="M1500,862 q56,-40 110,-6 l6,30 l-120,14 Z"'
                    f' fill="{CHUGUN}" {o(5)}/>')
    s += SL(Z_SRED, par(1560, 846, t, 2, .3, 90, .3, .6))
    s += SL(Z_SRED, f'<path d="M1760,1030 q-26,-190 70,-196 l0,196 Z" fill="#4a3a52" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(120, 160, 1700, t, 10, 53, 60))
    s += SL(0, lampa_stolika(1700, 700, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def lyureks_togda_i_segodnya(t):
    """Два плечика рядом: мамина колючая кофточка и сегодняшнее платье с
    мягкой нитью; между ними идёт стрелка времени."""
    rnd = random.Random(2052)
    s = f'<rect width="{W}" height="{H}" fill="#241f27"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 49))
    s += SL(Z_DAL, stena("paneli", t, 116))
    s += SL(Z_DAL, shkaf(60, 1040, 620, 880, t, .85, True))
    s += SL(Z_DAL, elka(1800, 1040, 380, t, 1.0, True, 55))
    s += SL(Z_SRED, polovicy(1040))
    # слева мамина кофточка: колючий яркий люрекс
    s += SL(0, naryad_plechiki(560, 260, 400, t, "#6a5b73", 1.2, .1, True, None, .0, 56))
    isk = ""
    for i in range(22):
        ix = 430 + rnd.randint(0, 260)
        iy = 320 + rnd.randint(0, 300)
        fase = (t * 1.9 + i * .17) % 1.0
        isk += (f'<path d="M{ix},{iy-11} l4,11 l11,4 l-11,4 l-4,11 l-4,-11 l-11,-4 l11,-4 Z"'
                f' fill="#ffffff" opacity="{.2+.75*(0.5+0.5*math.cos(2*math.pi*fase)):.2f}"/>')
    s += SL(0, isk)
    # справа сегодняшнее платье: мягкая нить
    s += SL(0, naryad_plechiki(1320, 250, 460, t, TSINIY, 1.3, .5, True, None, .22, 57))
    myag = ""
    for i in range(14):
        mx = 1210 + i * 18
        myag += (f'<path d="M{mx},330 q10,150 -6,300" fill="none" stroke="{SEREBRO}"'
                 f' stroke-width="2" opacity="{.18+.22*abs(A.w(t,2.6,i*.2)):.2f}"/>')
    s += SL(0, myag)
    # стрелка времени идёт от кофточки к платью
    p = A.out(A.seg(t, .4, 1.8))
    sx = 720 + 380 * p
    s += SL(0, f'<path d="M700,760 h{20+380*p:.0f}" stroke="{ZOLOTO}" stroke-width="8"'
               f' opacity=".85"/>'
               f'<path d="M{sx:.0f},760 l-30,-20 l0,40 Z" fill="{ZOLOTO}" {o(3)}/>')
    # взрослая дочь держит оба плечика, правое платье прикладывает к щеке
    s += SL(0, figura(980, 1040, 470, t, GRAFIT, HOLOD_KANT, .3, False, False,
                      1.0, 2.0, True, True, "#eec9a6", True, MOLOKO, True))
    for sgn, ug in ((-1, -150), (1, -36)):
        ruk, _ = rukav(980 + sgn * 92, 790, 170, ug, t, GRAFIT, HOLOD_KANT,
                       .2 + (0 if sgn < 0 else .35), 5.0)
        s += SL(0, ruk)
    s += SL(0, f'<circle cx="940" cy="640" r="20" fill="none" stroke="{SEREBRO}"'
               f' stroke-width="5"/><circle cx="1000" cy="640" r="20" fill="none"'
               f' stroke="{SEREBRO}" stroke-width="5"/>'
               f'<path d="M960,640 h20" stroke="{SEREBRO}" stroke-width="4"/>')
    # коробка с фотографиями и пуфик
    s += SL(Z_SRED, korobka(1560, 1040, 300, t, 120, True, BEZH, MOLOKO))
    fot = ""
    for i in range(5):
        fot += (f'<g transform="rotate({-12+i*7} {1620+i*30} 930)">'
                f'<rect x="{1600+i*30}" y="900" width="86" height="64" rx="4"'
                f' fill="{MOLOKO}" {o(3)}/>'
                f'<rect x="{1608+i*30}" y="908" width="70" height="40" fill="#9aa6b0"/></g>')
    s += SL(Z_SRED, fot)
    s += SL(Z_SRED, f'<path d="M760,1040 q-26,-150 62,-156 l0,156 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(60, 150, 1800, t, 11, 59, 60))
    s += SL(0, lampa_stolika(1700, 820, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def hozyayka_stavit_salatnik(t):
    """Кухня-столовая: хозяйка в винном трикотажном платье ставит салатник.
    В окне-раздаче — настоящая сервировка праздничного стола."""
    rnd = random.Random(2054)
    s = f'<rect width="{W}" height="{H}" fill="#241c18"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 57))
    s += SL(Z_DAL, stena("kraska", t, 117))
    # окно-раздача: рисованный вид, метка, наличник поверх
    px, py, pw, ph = 980, 150, 780, 300
    put = kontur_proema(px, py, pw, ph, "pryam")
    vid = (f'<path d="{put}" fill="#2e2620"/>'
           + f'<rect x="{px+30}" y="{py+150}" width="{pw-60}" height="40" rx="8"'
             f' fill="{MOLOKO}" {o(3)}/>')
    s += SL(Z_DAL, vid + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-16}" y="{py-16}" width="{pw+32}" height="{ph+32}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="26"/>'
            + f'<path d="M{px-16},{py+ph+16} h{pw+32}" stroke="{DEREVO}"'
              f' stroke-width="18"/>')
    s += SL(Z_SRED, polovicy(1040))
    # праздничный стол наполовину накрыт
    s += SL(Z_SRED, stol(120, 940, 1180, 44))
    sk = (f'<path d="M110,900 h1200 l-20,120 q-580,34 -1160,0 Z" fill="{MOLOKO}" {o(5)}/>')
    s += SL(Z_SRED, sk)
    tar = ""
    for i in range(6):
        tx = 220 + i * 180
        tar += (f'<ellipse cx="{tx}" cy="896" rx="62" ry="20" fill="{KREM2}" {o(3)}/>'
                f'<ellipse cx="{tx}" cy="890" rx="44" ry="13" fill="{MOLOKO}" {o(2)}/>')
    s += SL(Z_SRED, tar)
    s += SL(Z_SRED, svecha(400, 892, t, .1, 1.3) + svecha(1120, 892, t, .5, 1.2))
    # хозяйка ставит салатник: обе руки внешние, несут салатник
    s += SL(0, figura(760, 1040, 470, t, VINO, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    stav = A.out(A.seg(t, .3, 1.5))
    sx, sy = 760, 700 + 150 * stav
    for sgn in (-1, 1):
        ruk, _ = rukav(760 + sgn * 90, 790, 130, -60 + 40 * stav - sgn * 12, t,
                       VINO, TEPLO_SVET, .2 + (0 if sgn < 0 else .25), 4.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M{sx-96:.0f},{sy:.0f} q96,76 192,0 q-16,56 -96,60'
               f' q-80,-4 -96,-60 Z" fill="{IZUMRUD}" {o(5)}/>')
    s += SL(0, f'<ellipse cx="{sx:.0f}" cy="{sy:.0f}" rx="96" ry="22" fill="{KREM2}" {o(3)}/>')
    # кухонная часть: духовка, хлебница, стопка тарелок, полотенце
    s += SL(Z_SRED, f'<rect x="1420" y="700" width="420" height="340" rx="12"'
                    f' fill="{CHUGUN}" {o(6)}/>'
                    f'<rect x="1452" y="740" width="356" height="170" rx="8"'
                    f' fill="#20262c" {o(4)}/>')
    s += SL(Z_SRED, teplo(1630, 830, 190, 130, .34 + .10 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, f'<path d="M1452,950 h356" stroke="{SEREBRO}" stroke-width="10"/>')
    kach = 5 * A.w(t, 2.2, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.2f} 1400 700)">'
                    f'<path d="M1360,700 h80 l-10,170 h-60 Z" fill="{KORALL}" {o(4)}/></g>')
    st = "".join(f'<ellipse cx="1300" cy="{880-i*16}" rx="56" ry="16" fill="{KREM2}"'
                 f' {o(2)}/>' for i in range(6))
    s += SL(Z_SRED, st)
    s += SL(Z_DAL, elka(90, 1040, 420, t, 1.0, True, 59))
    s += SL(Z_SRED, girlyanda(140, 170, 760, t, 9, 61, 54))
    s += SL(0, lampa_stolika(1180, 560, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def naryad_pervyy_na_manekene(t):
    """Манекен в трикотажном платье: стрелки-выноски показывают длину, рукав и
    горловину, оттенок переключается с винного на терракотовый."""
    rnd = random.Random(2055)
    s = f'<rect width="{W}" height="{H}" fill="#241d22"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 61))
    s += SL(Z_DAL, stena("kraska", t, 118))
    s += SL(Z_DAL, okno_izby(120, 140, 460, 420, t, svet=False, moroz=.32))
    s += SL(Z_DAL, sneg_letit(t, 22, 63, .5, .7))
    s += SL(Z_DAL, elka(1820, 1040, 400, t, 1.0, True, 65))
    s += SL(Z_SRED, polovicy(1040))
    perekl = (t % 3.2) < 1.6
    s += SL(0, manekken(880, 1010, 760, t, KREM2, "zh",
                        VINO if perekl else TERRAKOT, .2, MOLOKO, .05, 80))
    # три стрелки-выноски встают по очереди
    VYN = ((640, 900, "длина ниже колена"), (1110, 640, "длинный рукав"),
           (880, 380, "круглая горловина"))
    for i, (vx, vy, _) in enumerate(VYN):
        p = A.out(A.seg(t, .4 + i * .55, .6))
        if p <= 0.02:
            continue
        ex = vx + (240 if vx > 900 else -240) * p
        s += SL(0, f'<path d="M{vx},{vy} L{ex:.0f},{vy-70*p:.0f}" stroke="{ZOLOTO}"'
                   f' stroke-width="6" opacity="{p:.2f}"/>'
                   f'<circle cx="{vx}" cy="{vy}" r="12" fill="{ZOLOTO}" opacity="{p:.2f}"/>'
                   f'<rect x="{min(vx,ex)-10:.0f}" y="{vy-110*p:.0f}" width="210"'
                   f' height="54" rx="10" fill="{GRAFIT}" opacity="{p*.9:.2f}" {o(3)}/>')
    # сантиметр свисает со стула
    s += SL(Z_SRED, f'<rect x="300" y="880" width="180" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="310" y="906" width="18" height="134" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="452" y="906" width="18" height="134" fill="{DEREVO}" {o(4)}/>')
    sv = 10 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<path d="M380,880 q{20+sv:.0f},120 {-14+sv:.0f},230"'
                    f' fill="none" stroke="{MOLOKO}" stroke-width="12"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{374+i*2},{900+i*25} l14,0" stroke="{K}"'
                        f' stroke-width="2" opacity=".6"/>')
    # столик с серьгами
    s += SL(Z_SRED, trumo(1420, 1040, 420, 300, t))
    s += SL(Z_SRED, f'<ellipse cx="1620" cy="760" rx="64" ry="40" fill="{VINO}" {o(4)}/>')
    for sgn in (-1, 1):
        s += SL(Z_SRED, f'<circle cx="{1620+sgn*24}" cy="{724-5*abs(A.w(t,1.8,sgn*.3)):.0f}"'
                        f' r="14" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(Z_SRED, zerkalo(1380, 300, 260, 460, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="1392" y="312" width="236" height="436" fill="{STEKLO}"'
                    f' opacity=".28"/>')
    s += SL(Z_SRED, girlyanda(60, 150, 1800, t, 12, 67, 58))
    s += SL(0, lampa_stolika(1620, 700, t, 1.15))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def naklon_k_duhovke(t):
    """Хозяйка наклоняется к духовке и вынимает противень: платье не задралось,
    ворот на месте — над ними встают две зелёные галочки."""
    rnd = random.Random(2056)
    s = f'<rect width="{W}" height="{H}" fill="#241c18"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 69))
    s += SL(Z_DAL, stena("kraska", t, 119))
    s += SL(Z_DAL, _polka_melochey(120, 300, 420, t, 56, 6))
    s += SL(Z_SRED, polovicy(1040))
    # плита с духовкой
    s += SL(Z_SRED, f'<rect x="1120" y="620" width="700" height="420" rx="14"'
                    f' fill="{CHUGUN}" {o(7)}/>'
                    f'<rect x="1160" y="680" width="620" height="230" rx="10"'
                    f' fill="#1d2228" {o(5)}/>')
    s += SL(Z_SRED, teplo(1470, 800, 300, 180, .38 + .10 * abs(A.w(t, 1.5))))
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{1200+i*180}" cy="640" r="34" fill="#2b3238" {o(3)}/>')
    # противень выезжает
    vyez = A.out(A.seg(t, .35, 1.3))
    px = 1160 - 320 * vyez
    s += SL(0, f'<rect x="{px:.0f}" y="810" width="420" height="40" rx="8"'
               f' fill="{ZHELEZ}" {o(5)}/>')
    for i in range(8):
        s += SL(0, f'<ellipse cx="{px+50+i*46:.0f}" cy="808" rx="24" ry="16"'
                   f' fill="{MED}" {o(3)}/>')
    s += SL(0, par(px + 210, 780, t, 4, .55, 170, .5, 1.0))
    # хозяйка: колени согнуты, обе руки в прихватках
    s += SL(0, figura(700, 1040, 500, t, VINO, TEPLO_SVET, .2, False, True, 1.0,
                      4.0, True, True, "#f0cfae", True, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(700 + sgn * 78, 790, 190, -8 + sgn * 14, t, VINO,
                              TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
        s += SL(0, f'<rect x="{hx-28:.0f}" y="{hy-24:.0f}" width="56" height="48"'
                   f' rx="12" fill="{KORALL}" {o(3)}/>')
    # две галочки
    for i, (gx, gy) in enumerate(((560, 560), (860, 500))):
        p = A.out(A.seg(t, .9 + i * .3, .5))
        if p <= .02:
            continue
        s += SL(0, f'<path d="M{gx},{gy} l34,40 l64,-86" fill="none" stroke="#3fae62"'
                   f' stroke-width="16" stroke-linecap="round" opacity="{p:.2f}"/>')
    # чайник, полотенце, стол с мукой, кот, часы
    s += SL(Z_SRED, f'<path d="M1880,620 q-40,-70 -110,-70 q-70,0 -110,70 Z"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    s += SL(Z_SRED, stol(120, 980, 420, 36))
    s += SL(Z_SRED, f'<ellipse cx="300" cy="944" rx="120" ry="30" fill="{MOLOKO}"'
                    f' opacity=".85"/>')
    s += SL(Z_SRED, kot(430, 1040, t, 1.5, "#6b5a46"))
    s += SL(Z_SRED, hodiki(960, 240, t, 1.3))
    s += SL(Z_SRED, girlyanda(100, 160, 820, t, 8, 71, 52))
    s += SL(0, lampa_stolika(960, 520, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def sergi_na_barhatnoy_podushechke(t):
    """Туалетный столик: пара серёг на бархатной подушечке, рукав закрывает
    крышку коробки с остальными украшениями — надето только одно."""
    rnd = random.Random(2058)
    s = f'<rect width="{W}" height="{H}" fill="#241f28"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 73))
    s += SL(Z_DAL, stena("doski", t, 120))
    s += SL(Z_DAL, elka(1840, 1050, 340, t, 1.0, True, 75))
    s += SL(Z_SRED, trumo(260, 1040, 1300, 460, t))
    # В ЗЕРКАЛЕ ДОЛЖНО ЧТО-ТО ОТРАЖАТЬСЯ (осмотр 16.11): пустая золотая рама
    # на пол-кадра читается как дыра. Ставим отражение наряда и флаконов.
    s += SL(Z_SRED, f'<rect x="634" y="184" width="592" height="492" fill="{STEKLO}"'
                    f' opacity=".26"/>')
    s += SL(Z_SRED, f'<g opacity=".5">'
                    + naryad_plechiki(930, 230, 380, t, VINO, 1.0, .3, True, None, .0, 85)
                    + f'<ellipse cx="760" cy="640" rx="90" ry="26" fill="{KREM2}"/>'
                    + f'<ellipse cx="1120" cy="640" rx="70" ry="22" fill="{LAVANDA}"/></g>')
    s += SL(Z_SRED, zerkalo(620, 170, 620, 520, t, "pryam", ZOLOTO, True))
    # подушечка с серьгами, крупно
    s += SL(0, f'<path d="M480,900 q280,-110 560,0 q-62,150 -280,156 q-218,-6 -280,-156 Z"'
               f' fill="{VINO}" {o(7)}/>')
    s += SL(0, skladki(520, 850, 480, 150, VINO, 6, 81, t, 2.0))
    # НАСТОЯЩИЕ серьги вместо рисованных (его слово 17.11: наряды и
    # аксессуары показываем реальным кадром, а не рисунком) — подушечка
    # под ними остаётся рисованной подставкой. Овал увеличен до нормы
    # проёма R-0024 (от 760 px по ширине) — маленькое окошко не читается
    s += SL(0, mesto_stoka(370, 650, 780, 320, "ellips"))
    # коробка с бусами, брошами, браслетами; крышка закрывается рукавом
    zak = A.out(A.seg(t, .5, 1.4))
    kx, ky, kw = 1180, 980, 460
    s += SL(0, f'<rect x="{kx}" y="{ky-130}" width="{kw}" height="130" rx="12"'
               f' fill="{DEREVO2}" {o(6)}/>')
    vn = ""
    for i in range(14):
        bx = kx + 30 + rnd.randint(0, kw - 70)
        by = ky - 110 + rnd.randint(0, 60)
        c = rnd.choice((ZOLOTO, SEREBRO, KORALL, IZUMRUD, MOLOKO))
        vn += f'<circle cx="{bx}" cy="{by}" r="{rnd.randint(8, 15)}" fill="{c}" {o(2)}/>'
    s += SL(0, vn)
    s += SL(0, f'<g transform="rotate({-70+70*zak:.1f} {kx} {ky-130})">'
               f'<rect x="{kx}" y="{ky-170}" width="{kw}" height="40" rx="8"'
               f' fill="{DEREVO}" {o(4)}/></g>')
    ruk, _ = rukav(kx + kw + 120, ky - 330, 230, 130 - 40 * zak, t, MOLOKO,
                   TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    # флаконы, гребень, свеча, ёлочная ветка
    fl = ""
    for i in range(5):
        fx = 320 + i * 86
        h_ = 52 + (i % 3) * 24
        fl += (f'<rect x="{fx-19}" y="{940-h_}" width="38" height="{h_}" rx="7"'
               f' fill="{(LAVANDA, PUDRA, KORALL, MOLOKO, ZOLOTO)[i]}" {o(3)}/>'
               f'<rect x="{fx-8}" y="{928-h_}" width="16" height="14" rx="4"'
               f' fill="{SEREBRO}" {o(2)}/>')
    s += SL(Z_SRED, fl)
    s += SL(Z_SRED, f'<path d="M980,960 h150 l0,22 h-150 Z" fill="{DEREVO2}" {o(3)}/>')
    s += SL(Z_SRED, "".join(f'<path d="M{988+i*12},982 l0,26" stroke="{DEREVO2}"'
                            f' stroke-width="3"/>' for i in range(12)))
    s += SL(Z_SRED, svecha(1700, 940, t, .3, 1.4))
    s += SL(Z_SRED, girlyanda(80, 150, 1780, t, 11, 83, 56))
    s += SL(0, lampa_stolika(1060, 880, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def hozyayka_ves_vecher(t):
    """Три картинки одного вечера — восемь, десять и полночь: платье везде без
    единой складки, хозяйка успевает всё."""
    rnd = random.Random(2059)
    s = f'<rect width="{W}" height="{H}" fill="#221b20"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 77))
    s += SL(Z_DAL, stena("oboi", t, 121))
    s += SL(Z_DAL, elka(1850, 1060, 320, t, 1.0, True, 79))
    CHASY = (8, 10, 12)
    for i in range(3):
        x0 = 60 + i * 620
        s += SL(Z_DAL, f'<rect x="{x0}" y="300" width="560" height="640" rx="18"'
                       f' fill="#2c242b" {o(6)}/>')
        s += SL(Z_DAL, f'<rect x="{x0+16}" y="316" width="528" height="608" rx="14"'
                       f' fill="#3a2f36" opacity=".55"/>')
        # часы над картинкой
        cx, cy = x0 + 280, 240
        s += SL(Z_SRED, f'<circle cx="{cx}" cy="{cy}" r="66" fill="{MOLOKO}" {o(5)}/>')
        for j in range(12):
            a = j * 30
            s += SL(Z_SRED, f'<path d="M{cx+52*math.cos(math.radians(a)):.0f},'
                            f'{cy+52*math.sin(math.radians(a)):.0f} l'
                            f'{8*math.cos(math.radians(a)):.0f},'
                            f'{8*math.sin(math.radians(a)):.0f}" stroke="{K}"'
                            f' stroke-width="4"/>')
        hod = CHASY[i] * 30 - 90 + 10 * A.seg(t, .3, 3.0)
        s += SL(Z_SRED, f'<path d="M{cx},{cy} l{44*math.cos(math.radians(hod)):.0f},'
                        f'{44*math.sin(math.radians(hod)):.0f}" stroke="{K}"'
                        f' stroke-width="7" stroke-linecap="round"/>'
                        f'<path d="M{cx},{cy} l0,-30" stroke="{K}" stroke-width="9"'
                        f' stroke-linecap="round"/>')
    # первая: идёт от плиты с блюдом в обеих руках
    idet = A.out(A.seg(t, .3, 1.8))
    fx = 180 + 160 * idet
    s += SL(0, figura(fx, 900, 380, t, VINO, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(fx + sgn * 68, 690, 110, -26 - sgn * 10, t, VINO,
                              TEPLO_SVET, .2, 4.0)
        s += SL(0, ruk)
    s += SL(0, f'<ellipse cx="{fx:.0f}" cy="620" rx="96" ry="26" fill="{KREM2}" {o(4)}/>'
               f'<ellipse cx="{fx:.0f}" cy="608" rx="70" ry="18" fill="{MED}" {o(2)}/>')
    s += SL(0, par(fx, 592, t, 3, .4, 110, .4, .8))
    # вторая: разливает компот
    s += SL(0, figura(960, 900, 380, t, VINO, TEPLO_SVET, .5, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, (hx, hy) = rukav(1026, 690, 130, -40, t, VINO, TEPLO_SVET, .3, 4.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(894, 710, 110, -8, t, VINO, TEPLO_SVET, .6, 4.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M{hx-30:.0f},{hy-40:.0f} q36,-54 72,0 l10,86 h-92 Z"'
               f' fill="url(#glina)" {o(4)}/>')
    liv = A.seg(t, .6, 1.6)
    s += SL(0, f'<path d="M{hx+34:.0f},{hy+40:.0f} l-10,{90*liv:.0f}" stroke="{KORALL}"'
               f' stroke-width="9" opacity=".85"/>')
    s += SL(0, f'<path d="M870,860 h180 l-14,70 h-152 Z" fill="{MOLOKO}" {o(3)}/>')
    # третья: сидит с бокалом среди гостей-силуэтов, фотограф щёлкает
    s += SL(0, figura(1560, 900, 360, t, VINO, TEPLO_SVET, .8, False, False, 1.0,
                      1.5, True, True, "#f0cfae", True, MOLOKO, False))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(1560 + sgn * 62, 700, 96, -62 - sgn * 8, t, VINO,
                              TEPLO_SVET, .4, 4.0)
        s += SL(0, ruk)
    s += SL(0, f'<path d="M1540,600 q20,54 40,0 Z" fill="{STEKLO}" opacity=".75"/>'
               f'<path d="M1560,600 l0,40 M1540,644 h40" stroke="{STEKLO}"'
               f' stroke-width="5"/>')
    go = ""
    for i in range(3):
        gx = 1400 + i * 120
        go += (f'<ellipse cx="{gx}" cy="800" rx="46" ry="90" fill="#1b1620"'
               f' opacity=".85"/><circle cx="{gx}" cy="690" r="34" fill="#1b1620"'
               f' opacity=".85"/>')
    s += SL(Z_SRED, go)
    vsp = 1.0 if (t % 2.2) < .18 else .0
    s += SL(0, f'<rect x="1300" y="320" width="560" height="620" fill="#ffffff"'
               f' opacity="{vsp*.35:.2f}"/>')
    s += SL(Z_SRED, svecha(1260, 930, t, .2, 1.2) + svecha(640, 930, t, .6, 1.2))
    s += SL(Z_SRED, girlyanda(60, 160, 1800, t, 12, 85, 54))
    s += SL(0, lampa_stolika(1180, 1000, t, 1.0))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def seroe_plate_i_vinnyy_sharf(t):
    """Простое серое платье на плечиках: винный поясок и винный шарф делают
    его праздничным прямо в кадре."""
    rnd = random.Random(2060)
    s = f'<rect width="{W}" height="{H}" fill="#242027"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 81))
    s += SL(Z_DAL, stena("kraska", t, 122))
    s += SL(Z_DAL, shkaf(900, 1050, 900, 940, t, .9, True))
    s += SL(Z_DAL, elka(120, 1050, 380, t, 1.0, True, 83))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, naryad_plechiki(1240, 250, 620, t, "#9b9ca4", 1.5, .1, True, None, .04, 86, 1.4))
    # поясок завязывается
    p1 = A.out(A.seg(t, .35, 1.2))
    s += SL(0, f'<path d="M{1240-190*p1:.0f},600 q{190*p1:.0f},36 {380*p1:.0f},0"'
               f' fill="none" stroke="{VINO}" stroke-width="26"/>')
    if p1 > .8:
        s += SL(0, f'<path d="M1240,600 l-54,-34 l10,70 Z" fill="{VINO}" {o(3)}/>'
                   f'<path d="M1240,600 l54,-34 l-10,70 Z" fill="{VINO}" {o(3)}/>')
    # шарф ложится на плечо
    p2 = A.out(A.seg(t, 1.1, 1.3))
    s += SL(0, f'<path d="M{1090:.0f},{300-160*(1-p2):.0f} q60,120 20,300'
               f' l70,16 q50,-200 -10,-320 Z" fill="{VINO}" opacity="{p2:.2f}" {o(5)}/>')
    # женщина завязывает поясок и накидывает шарф
    s += SL(0, figura(700, 1050, 520, t, GRAFIT, HOLOD_KANT, .3, False, False, 1.0,
                      2.0, True, True, "#eec9a6", True, MOLOKO, True))
    ruk, _ = rukav(790, 760, 230, -20 + 10 * A.w(t, 1.6), t, GRAFIT, HOLOD_KANT, .2, 5.0)
    s += SL(0, ruk)
    ruk2, _ = rukav(790, 690, 250, -44 + 12 * A.w(t, 1.9, .3), t, GRAFIT, HOLOD_KANT, .5, 5.0)
    s += SL(0, ruk2)
    # корзина с шарфами, туфли, пуфик, зеркало
    s += SL(Z_SRED, f'<path d="M300,1046 q-30,-150 70,-154 q100,4 70,154 Z"'
                    f' fill="url(#solom)" {o(5)}/>')
    sh = ""
    for i in range(5):
        c = (KORALL, IZUMRUD, TSINIY, ZOLOTO, LAVANDA)[i]
        sh += (f'<path d="M{320+i*26},900 q{14+6*A.w(t,2.4,i*.3):.0f},-70 30,-96"'
               f' fill="none" stroke="{c}" stroke-width="18" stroke-linecap="round"/>')
    s += SL(Z_SRED, sh)
    s += SL(Z_SRED, tufli(520, 1046, 1.1, GRAFIT, t))
    s += SL(Z_SRED, f'<path d="M160,1046 q-20,-130 56,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(60, 280, 220, 560, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, girlyanda(260, 150, 1560, t, 10, 87, 52))
    s += SL(0, lampa_stolika(1760, 960, t, 1.15))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def fartuk_poverh_naryadnogo(t):
    """Кухня шестидесятых: мама развязывает тесёмки ситцевого фартука, он
    слетает на спинку стула. В стекле окна — настоящий зимний двор."""
    rnd = random.Random(2061)
    s = f'<rect width="{W}" height="{H}" fill="#241d16"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 89))
    s += SL(Z_DAL, stena("kraska", t, 123))
    # окно кухни: рисованный вид, метка, переплёт поверх
    px, py, pw, ph = 120, 170, 800, 330
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#15202c"/>'
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-14}" y="{py-14}" width="{pw+28}" height="{ph+28}"'
              f' fill="none" stroke="{MOLOKO}" stroke-width="22"/>'
            + f'<path d="M{px+pw/2:.0f},{py-14} l0,{ph+28}" stroke="{MOLOKO}"'
              f' stroke-width="16"/>'
            + f'<path d="M{px-14},{py+ph/2:.0f} l{pw+28},0" stroke="{MOLOKO}"'
              f' stroke-width="12"/>')
    s += SL(Z_SRED, polovicy(1050))
    # плита, кастрюли, противень с пирожками
    s += SL(Z_SRED, f'<rect x="1180" y="640" width="660" height="410" rx="12"'
                    f' fill="{CHUGUN}" {o(7)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{1270+i*160}" cy="662" r="36" fill="#2b3238" {o(3)}/>')
    for i, (kx, kw) in enumerate(((1280, 180), (1530, 150))):
        s += SL(Z_SRED, f'<path d="M{kx},600 h{kw} l-14,-90 h{-kw+28} Z"'
                        f' fill="{SEREBRO}" {o(5)}/>')
        s += SL(Z_SRED, par(kx + kw / 2, 500, t, 4, .5, 160, .45, 1.0))
    s += SL(Z_SRED, f'<rect x="1230" y="760" width="420" height="34" rx="6"'
                    f' fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, "".join(f'<ellipse cx="{1270+i*58}" cy="756" rx="26" ry="17"'
                            f' fill="{MED}" {o(3)}/>' for i in range(7)))
    # мама: обе руки заведены за спину, развязывают тесёмки
    s += SL(0, figura(760, 1050, 520, t, IZUMRUD, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    raz = A.seg(t, .3, 1.8)
    for sgn in (-1, 1):
        ruk, _ = rukav(760 + sgn * 92, 760, 140, 150 - sgn * 24 + 20 * raz, t,
                       IZUMRUD, TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    # фартук слетает на спинку стула
    let = A.out(A.seg(t, 1.0, 1.4))
    fx = 760 + 420 * let
    fy = 820 + 120 * let
    s += SL(0, f'<g transform="rotate({40*let:.1f} {fx:.0f} {fy:.0f})">'
               f'<path d="M{fx-110:.0f},{fy-230:.0f} h220 l34,300 q-134,30 -268,0 Z"'
               f' fill="{MOLOKO}" {o(5)}/>')
    cvet = ""
    for i in range(14):
        cx = fx - 96 + rnd.randint(0, 190)
        cy = fy - 210 + rnd.randint(0, 260)
        cvet += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="{KORALL}"'
                 f' opacity=".9"/>')
    s += SL(0, cvet + "</g>")
    s += SL(Z_SRED, f'<rect x="1080" y="860" width="170" height="26" rx="6"'
                    f' fill="{DEREVO}" {o(5)}/>'
                    f'<rect x="1090" y="886" width="18" height="164" fill="{DEREVO}" {o(4)}/>'
                    f'<rect x="1222" y="886" width="18" height="164" fill="{DEREVO}" {o(4)}/>')
    # радио, скалка, полотенце, часы без пяти двенадцать
    s += SL(Z_SRED, f'<rect x="300" y="620" width="230" height="130" rx="10"'
                    f' fill="{DEREVO2}" {o(5)}/>'
                    f'<circle cx="360" cy="686" r="34" fill="#2b2b2b" {o(3)}/>'
                    f'<circle cx="470" cy="686" r="18" fill="{ZOLOTO}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="620" y="716" width="200" height="22" rx="11"'
                    f' fill="{DEREVO2}" {o(3)}/>')
    s += SL(Z_SRED, hodiki(1000, 230, t, 1.4))
    s += SL(Z_SRED, girlyanda(980, 150, 880, t, 9, 91, 50))
    s += SL(0, lampa_stolika(520, 560, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def fartuk_na_kryuchke(t):
    """Сегодняшняя кухня: фартук с пятном висит на крючке, хозяйка в чистом
    винном платье гасит свет и уходит к гостям."""
    rnd = random.Random(2062)
    s = f'<rect width="{W}" height="{H}" fill="#1f1b20"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 93))
    s += SL(Z_DAL, stena("kraska", t, 124))
    s += SL(Z_SRED, polovicy(1050))
    # фартук на крючке, крупно
    kach = 4.5 * A.w(t, 2.0, .1)
    s += SL(0, f'<g transform="rotate({kach:.2f} 620 300)">'
               f'<path d="M620,300 l0,46" stroke="{SEREBRO}" stroke-width="8"/>'
               f'<path d="M500,346 h240 l40,420 q-160,34 -320,0 Z" fill="{KREM2}" {o(6)}/>'
               f'<path d="M500,420 h240" stroke="{K}" stroke-width="4" opacity=".35"/>'
               f'<ellipse cx="660" cy="620" rx="52" ry="38" fill="{VINO}" opacity=".8"/>'
               f'<ellipse cx="688" cy="652" rx="22" ry="16" fill="{VINO}" opacity=".7"/></g>')
    s += SL(Z_SRED, f'<path d="M560,290 h120 l0,16 h-120 Z" fill="{SEREBRO}" {o(3)}/>')
    # хозяйка в дверях: правая рука к серьге, левая на выключателе
    s += SL(0, figura(1280, 1050, 520, t, VINO, TEPLO_SVET, .3, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, (hx, hy) = rukav(1216, 760, 150, -104, t, VINO, TEPLO_SVET, .2, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(1352, 770, 170, -22, t, VINO, TEPLO_SVET, .5, 5.0)
    s += SL(0, ruk2)
    s += SL(0, f'<circle cx="{hx:.0f}" cy="{hy+10:.0f}" r="13" fill="{ZOLOTO}" {o(2)}/>')
    gasnet = A.seg(t, .6, 1.6)
    s += SL(Z_SRED, f'<rect x="{h2x-22:.0f}" y="{h2y-30:.0f}" width="44" height="60"'
                    f' rx="8" fill="{MOLOKO}" {o(3)}/>')
    # кухня гаснет, столовая со свечами светится
    s += SL(Z_SRED, f'<rect x="0" y="0" width="1120" height="1080" fill="#000000"'
                    f' opacity="{.45*gasnet:.2f}"/>')
    s += SL(Z_DAL, f'<rect x="1480" y="200" width="420" height="850" rx="12"'
                   f' fill="#2d2129" {o(6)}/>')
    s += SL(Z_DAL, svecha(1580, 700, t, .1, 1.5) + svecha(1700, 690, t, .5, 1.4)
            + svecha(1810, 706, t, .8, 1.3))
    s += SL(Z_DAL, teplo(1690, 680, 300, 320, .34 + .10 * abs(A.w(t, 1.7))))
    # плита, полотенце, венок, часы
    s += SL(Z_SRED, f'<rect x="120" y="700" width="420" height="350" rx="12"'
                    f' fill="{CHUGUN}" {o(6)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{190+i*110}" cy="722" r="30" fill="#2b3238" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M880,640 h120 l0,230 h-120 Z" fill="{KORALL}" {o(4)}/>')
    ven = ""
    for i in range(16):
        a = i * 22.5
        ven += (f'<ellipse cx="{980+96*math.cos(math.radians(a)):.0f}"'
                f' cy="{330+96*math.sin(math.radians(a)):.0f}" rx="22" ry="13"'
                f' fill="{HVOYA}" transform="rotate({a:.0f} '
                f'{980+96*math.cos(math.radians(a)):.0f},'
                f'{330+96*math.sin(math.radians(a)):.0f})" {o(2)}/>')
    s += SL(Z_SRED, ven)
    s += SL(Z_SRED, hodiki(300, 300, t, 1.2))
    s += SL(0, lampa_stolika(880, 980, t, 1.0))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def taksi_u_podezda_vecherom(t):
    """Зимний вечер у подъезда в огоньках: женщина в шубке спускается с
    крыльца к машине с шашечками, в руке блестящая сумочка."""
    rnd = random.Random(2063)
    s = f'<rect width="{W}" height="{H}" fill="#101722"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 97))
    s += SL(Z_DAL, panelka(60, 760, 760, t, 5, True, 99))
    s += SL(Z_DAL, ulica_dal(900, 700, 1000, t, True, 101))
    s += SL(Z_DAL, sneg_letit(t, 44, 103, .75, 1.0))
    s += SL(Z_SRED, f'<rect x="0" y="880" width="{W}" height="200" fill="{SNEG}"'
                    f' opacity=".82"/>')
    # подъезд в огоньках и крыльцо
    s += SL(Z_SRED, f'<rect x="240" y="420" width="420" height="520" rx="10"'
                    f' fill="#2a2f3a" {o(6)}/>'
                    f'<rect x="300" y="520" width="300" height="420" rx="8"'
                    f' fill="#16202c" {o(4)}/>')
    s += SL(Z_SRED, girlyanda(250, 440, 400, t, 9, 105, 44))
    stup = "".join(f'<rect x="{250+i*18}" y="{900+i*26}" width="{380-i*36}"'
                   f' height="26" fill="{SNEG}" {o(3)}/>' for i in range(3))
    s += SL(Z_SRED, stup)
    # машина-силуэт с шашечками
    s += SL(Z_SRED, f'<path d="M1120,900 q40,-120 200,-130 l240,0 q150,20 190,130 Z"'
                    f' fill="#1d222c" {o(6)}/>'
                    f'<path d="M1240,790 q120,-70 260,0 Z" fill="{STEKLO}" opacity=".45"/>')
    sh = "".join(f'<rect x="{1180+i*40}" y="856" width="40" height="22"'
                 f' fill="{"#e9eef6" if i % 2 == 0 else "#20242c"}"/>' for i in range(10))
    s += SL(Z_SRED, sh)
    for cx in (1180, 1620):
        s += SL(Z_SRED, f'<circle cx="{cx}" cy="930" r="46" fill="#15181e" {o(4)}/>'
                        f'<circle cx="{cx}" cy="930" r="18" fill="{SEREBRO}" {o(2)}/>')
    s += SL(Z_SRED, teplo(1700, 880, 160, 90, .30 + .10 * abs(A.w(t, 1.4))))
    # женщина спускается: левая рука придерживает подол, правая с сумочкой
    p = A.out(A.seg(t, .25, 1.6))
    fx, fy = 620 + 260 * p, 900 + 60 * p
    s += SL(0, figura(fx, fy, 470, t, "#6b5347", HOLOD_KANT, .2, False, False, 1.0,
                      3.0, True, True, "#f0cfae", True, MOLOKO, True))
    ruk, (hx, hy) = rukav(fx - 76, fy - 300, 150, 62, t, "#6b5347", HOLOD_KANT, .2, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(fx + 76, fy - 300, 140, 50, t, "#6b5347", HOLOD_KANT, .5, 5.0)
    s += SL(0, ruk2)
    s += SL(0, f'<path d="M{h2x-34:.0f},{h2y:.0f} q34,-14 58,14 l10,70 h-82 Z"'
               f' fill="{SEREBRO}" opacity="{.75+.25*abs(A.w(t,1.9)):.2f}" {o(3)}/>')
    s += SL(0, f'<ellipse cx="{fx:.0f}" cy="{fy-420:.0f}" rx="66" ry="30"'
               f' fill="#8a7466" {o(4)}/>')
    s += SL(0, para_izo_rta(fx + 30, fy - 400, t, .2, 1.0, .45))
    # фонарь, ёлка у подъезда, скамейка
    s += SL(Z_SRED, f'<rect x="940" y="420" width="16" height="500" fill="{CHUGUN}" {o(4)}/>'
                    f'<path d="M900,420 q48,-56 96,0 Z" fill="{ZOLOTO}" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, teplo(948, 440, 260, 230, .30 + .08 * abs(A.w(t, 2.1))))
    s += SL(Z_DAL, elka(780, 920, 360, t, 1.0, True, 107))
    s += SL(Z_SRED, f'<rect x="1000" y="880" width="180" height="16" rx="6"'
                    f' fill="{DEREVO}" {o(3)}/>'
                    f'<rect x="1010" y="896" width="14" height="60" fill="{CHUGUN}" {o(2)}/>'
                    f'<rect x="1156" y="896" width="14" height="60" fill="{CHUGUN}" {o(2)}/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def naryad_vtoroy_na_manekene(t):
    """Манекен в бархатном платье: стрелки-выноски показывают силуэт, подол и
    рукав три четверти, оттенок переключается с рубинового на изумрудный."""
    rnd = random.Random(2064)
    s = f'<rect width="{W}" height="{H}" fill="#201d26"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 109))
    s += SL(Z_DAL, stena("kraska", t, 126))
    s += SL(Z_DAL, elka(140, 1050, 440, t, 1.0, True, 111))
    s += SL(Z_SRED, polovicy(1050))
    perekl = (t % 3.6) < 1.8
    s += SL(0, manekken(960, 1020, 780, t, KREM2, "zh",
                        RUBIN if perekl else IZUMRUD, .2, None, .14, 112))
    tem = ""
    for i in range(9):
        tx = 820 + i * 36
        tem += (f'<path d="M{tx},560 q{10+6*A.w(t,2.4,i*.2):.0f},180 -4,340"'
                f' fill="none" stroke="#000000" stroke-width="16" opacity=".22"/>')
    s += SL(0, tem)
    VYN = ((780, 640, 1), (1180, 880, -1), (1140, 560, -1))
    for i, (vx, vy, sgn) in enumerate(VYN):
        p = A.out(A.seg(t, .4 + i * .6, .6))
        if p <= .02:
            continue
        ex = vx - sgn * 230 * p
        s += SL(0, f'<path d="M{vx},{vy} L{ex:.0f},{vy-60*p:.0f}" stroke="{ZOLOTO}"'
                   f' stroke-width="6" opacity="{p:.2f}"/>'
                   f'<circle cx="{vx}" cy="{vy}" r="12" fill="{ZOLOTO}" opacity="{p:.2f}"/>'
                   f'<rect x="{min(vx,ex)-20:.0f}" y="{vy-100*p:.0f}" width="220"'
                   f' height="52" rx="10" fill="{GRAFIT}" opacity="{p*.9:.2f}" {o(3)}/>')
    s += SL(Z_SRED, tufli(1420, 1046, 1.2, GRAFIT, t))
    s += SL(Z_SRED, f'<path d="M1640,1046 q-24,-150 64,-154 l0,154 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, zerkalo(1700, 260, 180, 600, t, "pryam", ZOLOTO, True))
    # торшер: живой тёплый источник
    s += SL(Z_SRED, f'<rect x="420" y="620" width="14" height="430" fill="{CHUGUN}" {o(3)}/>'
                    f'<path d="M350,620 h154 l-24,-90 h-106 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, lampa_stolika(427, 600, t, 1.5))
    s += SL(Z_SRED, girlyanda(600, 150, 1200, t, 10, 113, 52))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tufli_lodochki_na_parkete(t):
    """Паркет у зеркала: подставка-нога в гладких колготках, рукав отодвигает
    упаковки с узорными и блестящими."""
    rnd = random.Random(2065)
    s = f'<rect width="{W}" height="{H}" fill="#241e1a"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 115))
    s += SL(Z_DAL, doski(0, 0, W, 620, 86))
    s += SL(Z_DAL, elka(1840, 1050, 320, t, 1.0, True, 117))
    s += SL(Z_SRED, polovicy(760))
    par_ = ""
    for i in range(16):
        par_ += (f'<path d="M{60+i*118},760 l0,320" stroke="#5a3d26"'
                 f' stroke-width="3" opacity=".5"/>')
    s += SL(Z_SRED, par_)
    # напольное зеркало: рисованный вид и рама (кадр отсюда снят)
    s += SL(Z_SRED, f'<rect x="150" y="150" width="620" height="720" rx="10"'
                    f' fill="#2a2420" {o(6)}/>'
            + zerkalo(150, 150, 620, 720, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="166" y="166" width="588" height="688" fill="{STEKLO}"'
                    f' opacity=".22"/>')
    # НАСТОЯЩИЙ КАДР ОТСЮДА СНЯТ (туфли сток даёт только на людях), поэтому
    # зеркало не остаётся пустым: в нём отражаются сами лодочки и край подола.
    s += SL(Z_SRED, f'<g opacity=".65">'
                    + f'<path d="M230,180 q150,40 300,0 l0,250 q-150,44 -300,0 Z"'
                      f' fill="{RUBIN}" {o(4)}/>'
                    + tufli(300, 800, 1.9, GRAFIT, t) + "</g>")
    # подставка-нога в гладких колготках
    nx = 1120
    s += SL(0, f'<path d="M{nx-56},1040 q-20,-280 56,-330 q76,50 56,330 Z"'
               f' fill="#d8b89c" {o(6)}/>')
    s += SL(0, f'<path d="M{nx-56},900 q56,-26 112,0" fill="none" stroke="#c7a68c"'
               f' stroke-width="5" opacity=".7"/>')
    s += SL(0, tufli(nx - 70, 1046, 1.3, GRAFIT, t, False))
    # упаковки колготок: рукав отодвигает две
    ot = A.out(A.seg(t, .4, 1.4))
    for i, c in enumerate((LAVANDA, SEREBRO)):
        ux = 1420 + i * 180 + 120 * ot
        s += SL(0, f'<g transform="rotate({8+14*ot:.1f} {ux} 940)">'
                   f'<rect x="{ux-80:.0f}" y="820" width="160" height="230" rx="10"'
                   f' fill="{c}" {o(5)}/>'
                   f'<rect x="{ux-60:.0f}" y="850" width="120" height="110" rx="8"'
                   f' fill="{MOLOKO}" opacity=".65"/></g>')
    ruk, _ = rukav(1380, 640, 230, 56 - 20 * ot, t, VINO, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    # край бархатного подола покачивается сверху
    s += SL(0, f'<path d="M980,150 q180,{40+14*A.w(t,2.0):.0f} 360,0 l0,120'
               f' q-180,{-30+10*A.w(t,2.0,.3):.0f} -360,0 Z" fill="{RUBIN}" {o(5)}/>')
    s += SL(Z_SRED, korobka(820, 1046, 260, t, 110, True, BEZH, MOLOKO))
    s += SL(Z_SRED, f'<path d="M1680,1046 q-20,-130 58,-134 l0,134 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1480,1046 l120,-16 l6,26 l-120,16 Z" fill="{DEREVO2}" {o(3)}/>')
    blik_hod = (A.w(t, 4.2, .2) + 1) / 2
    s += SL(Z_SRED, f'<path d="M{200+1300*blik_hod:.0f},760 l140,320 l-90,0 l-140,-320 Z"'
                    f' fill="#ffffff" opacity=".10"/>')
    s += SL(Z_SRED, girlyanda(820, 140, 1000, t, 9, 119, 48))
    s += SL(0, lampa_stolika(900, 560, t, 1.2))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def sumochka_brosh_i_kole(t):
    """Туалетный столик: маленькая сумочка с блеском, а над брошью и колье
    качаются весы — надеть нужно что-то одно."""
    rnd = random.Random(2066)
    s = f'<rect width="{W}" height="{H}" fill="#231f27"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 121))
    s += SL(Z_DAL, stena("doski", t, 128))
    s += SL(Z_DAL, elka(120, 1050, 340, t, 1.0, True, 123))
    s += SL(Z_SRED, trumo(380, 1050, 1200, 440, t))
    s += SL(Z_SRED, zerkalo(700, 160, 560, 520, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<rect x="714" y="174" width="532" height="492" fill="{STEKLO}"'
                    f' opacity=".26"/>')
    # сумочка на треть кадра
    sx, sy = 620, 900
    bl = .6 + .4 * abs(A.w(t, 1.6))
    s += SL(0, f'<path d="M{sx-150},{sy-170} q150,-60 300,0 l30,230 q-180,40 -360,0 Z"'
               f' fill="{GRAFIT}" {o(6)}/>')
    s += SL(0, f'<path d="M{sx-150},{sy-170} q150,-60 300,0" fill="none"'
               f' stroke="{SEREBRO}" stroke-width="10" opacity="{bl:.2f}"/>')
    s += SL(0, f'<path d="M{sx-110},{sy-180} q110,-190 230,-10" fill="none"'
               f' stroke="{SEREBRO}" stroke-width="7"/>')
    s += SL(0, tkan_blesk(sx - 150, sy - 170, 300, 230, t, "#ffffff", .5, .2))
    # две подушечки: брошь и колье, над ними весы
    for i, (px, c) in enumerate(((1180, ZOLOTO), (1480, SEREBRO))):
        s += SL(Z_SRED, f'<path d="M{px-90},{880} q90,-40 180,0 q-24,66 -90,70'
                        f' q-66,-4 -90,-70 Z" fill="{VINO}" {o(5)}/>')
        if i == 0:
            s += SL(0, f'<circle cx="{px}" cy="862" r="34" fill="{c}" {o(3)}/>')
            for j in range(8):
                a = j * 45
                s += SL(0, f'<circle cx="{px+44*math.cos(math.radians(a)):.0f}"'
                           f' cy="{862+44*math.sin(math.radians(a)):.0f}" r="10"'
                           f' fill="{c}" {o(2)}/>')
        else:
            s += SL(0, "".join(f'<circle cx="{px-70+j*20}" cy="{868+int(14*math.sin(j*.7))}"'
                               f' r="10" fill="{c}" {o(2)}/>' for j in range(8)))
    kach = 9 * A.w(t, 2.0, .2)
    s += SL(0, f'<g transform="rotate({kach:.2f} 1330 620)">'
               f'<path d="M1150,620 h360" stroke="{ZOLOTO}" stroke-width="8"/>'
               f'<path d="M1150,620 l0,60 M1510,620 l0,60" stroke="{ZOLOTO}"'
               f' stroke-width="5"/>'
               f'<path d="M1100,680 h100 l-16,46 h-68 Z" fill="{ZOLOTO}" {o(3)}/>'
               f'<path d="M1460,680 h100 l-16,46 h-68 Z" fill="{ZOLOTO}" {o(3)}/></g>')
    s += SL(0, f'<path d="M1330,620 l0,-130" stroke="{ZOLOTO}" stroke-width="7"/>')
    # рукава: правый берёт брошь, левый отодвигает колье
    ruk, _ = rukav(1120, 420, 230, 78, t, RUBIN, TEPLO_SVET, .2, 5.0, True)
    s += SL(0, ruk)
    ruk2, _ = rukav(1620, 450, 220, 112, t, RUBIN, TEPLO_SVET, .5, 5.0, True)
    s += SL(0, ruk2)
    fl = ""
    for i in range(5):
        fx = 320 + i * 70
        h_ = 46 + (i % 3) * 22
        fl += (f'<rect x="{fx-16}" y="{980-h_}" width="32" height="{h_}" rx="6"'
               f' fill="{(PUDRA, LAVANDA, MOLOKO, KORALL, ZOLOTO)[i]}" {o(3)}/>')
    s += SL(Z_SRED, fl)
    s += SL(Z_SRED, f'<path d="M1700,1000 q50,-30 96,-4 l-8,54 q-46,20 -92,-6 Z"'
                    f' fill="{MOLOKO}" {o(4)}/>')
    s += SL(Z_SRED, svecha(1800, 950, t, .4, 1.3))
    s += SL(Z_SRED, girlyanda(300, 140, 1400, t, 10, 125, 50))
    s += SL(0, lampa_stolika(980, 960, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def trikotazh_i_barhatnyy_zhaket(t):
    """Рубиновое трикотажное платье на плечиках: сверху ложится бархатный
    жакет, потом его сменяет бархатный шарф."""
    rnd = random.Random(2068)
    s = f'<rect width="{W}" height="{H}" fill="#241f23"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 127))
    s += SL(Z_DAL, stena("oboi", t, 129))
    s += SL(Z_DAL, shkaf(820, 1050, 940, 960, t, .95, True))
    s += SL(Z_DAL, elka(130, 1050, 360, t, 1.0, True, 129))
    s += SL(Z_SRED, polovicy(1050))
    s += SL(0, naryad_plechiki(1240, 230, 600, t, RUBIN, 1.5, .1, True, None, .05, 130, 1.5))
    # жакет ложится, потом сменяется шарфом
    faza = A.seg(t, .3, 3.2)
    zh = max(0.0, min(1.0, faza * 2.2))
    sh = max(0.0, min(1.0, (faza - .55) * 2.6))
    if sh < .1:
        s += SL(0, f'<g opacity="{zh:.2f}">'
                   f'<path d="M1090,{300-120*(1-zh):.0f} h300 l24,330 h-348 Z"'
                   f' fill="#4a1b2a" {o(6)}/>'
                   f'<path d="M1240,{300-120*(1-zh):.0f} l0,330" stroke="{K}"'
                   f' stroke-width="4" opacity=".5"/></g>')
    else:
        s += SL(0, f'<path d="M1130,{300-100*(1-sh):.0f} q60,150 24,360 l72,16'
                   f' q44,-230 -16,-380 Z" fill="#4a1b2a" opacity="{sh:.2f}" {o(5)}/>')
    # женщина обеими руками работает с плечиками
    s += SL(0, figura(660, 1050, 520, t, GRAFIT, HOLOD_KANT, .3, False, False, 1.0,
                      2.0, True, True, "#eec9a6", True, MOLOKO, True))
    for sgn, ug in ((-1, -46), (1, -26)):
        ruk, _ = rukav(660 + sgn * 92, 740, 250, ug, t, GRAFIT, HOLOD_KANT,
                       .2 + (0 if sgn < 0 else .3), 5.0)
        s += SL(0, ruk)
    s += SL(Z_SRED, f'<path d="M280,1046 q-30,-150 70,-154 q100,4 70,154 Z"'
                    f' fill="url(#solom)" {o(5)}/>')
    s += SL(Z_SRED, tufli(470, 1046, 1.1, RUBIN, t))
    s += SL(Z_SRED, zerkalo(60, 300, 200, 540, t, "pryam", ZOLOTO, True))
    s += SL(Z_SRED, f'<path d="M1760,1046 q-20,-140 60,-144 l0,144 Z" fill="#45384f" {o(5)}/>')
    s += SL(Z_SRED, girlyanda(300, 140, 1500, t, 11, 131, 54))
    s += SL(0, lampa_stolika(1700, 900, t, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def tufli_v_pakete(t):
    """Заснеженная улица под фонарями: мама с дочкой идут в гости, из пакета
    торчат каблучки нарядных туфель. В витрине — настоящая зимняя улица."""
    rnd = random.Random(2069)
    s = f'<rect width="{W}" height="{H}" fill="#101824"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 133))
    s += SL(Z_DAL, panelka(1180, 720, 700, t, 5, True, 135))
    s += SL(Z_DAL, ulica_dal(60, 680, 900, t, True, 137))
    s += SL(Z_DAL, sneg_letit(t, 46, 139, .8, 1.0))
    # витрина магазина: рисованный вид, метка, переплёт поверх
    px, py, pw, ph = 1040, 300, 800, 320
    put = kontur_proema(px, py, pw, ph, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#16202c"/>'
            + mesto_stoka(px, py, pw, ph, "pryam")
            + f'<rect x="{px-16}" y="{py-16}" width="{pw+32}" height="{ph+32}"'
              f' fill="none" stroke="{DEREVO2}" stroke-width="24"/>'
            + f'<path d="M{px+pw/2:.0f},{py-16} l0,{ph+32}" stroke="{DEREVO2}"'
              f' stroke-width="14"/>')
    s += SL(Z_SRED, f'<rect x="0" y="900" width="{W}" height="180" fill="{SNEG}"'
                    f' opacity=".85"/>')
    sug = "".join(f'<ellipse cx="{120+i*260}" cy="910" rx="150" ry="40" fill="{SNEG}"'
                  f' {o(2)}/>' for i in range(8))
    s += SL(Z_SRED, sug)
    # мама и дочка идут слева направо
    p = A.seg(t, .2, 3.0)
    mx = 260 + 420 * p
    s += SL(0, figura(mx, 1000, 500, t, "#5c4a3f", HOLOD_KANT, .2, False, False, 1.0,
                      2.5, True, True, "#f0cfae", False, "#8a7466", True))
    ruk, (hx, hy) = rukav(mx + 86, 740, 180, 76, t, "#5c4a3f", HOLOD_KANT, .2, 5.0)
    s += SL(0, ruk)
    ruk2, (h2x, h2y) = rukav(mx - 86, 760, 170, 104, t, "#5c4a3f", HOLOD_KANT, .5, 5.0)
    s += SL(0, ruk2)
    # пакет с каблучками
    kach = 7 * A.w(t, 1.5, .2)
    s += SL(0, f'<g transform="rotate({kach:.2f} {hx:.0f} {hy:.0f})">'
               f'<path d="M{hx-66:.0f},{hy:.0f} h132 l14,180 h-160 Z" fill="{KREM2}" {o(5)}/>'
               f'<path d="M{hx-36:.0f},{hy-14:.0f} q36,-40 72,0" fill="none"'
               f' stroke="{BEZH}" stroke-width="6"/>'
               f'<path d="M{hx-24:.0f},{hy-6:.0f} l-10,-58 l16,-2 l12,58 Z"'
               f' fill="{RUBIN}" {o(3)}/>'
               f'<path d="M{hx+22:.0f},{hy-6:.0f} l10,-54 l16,4 l-12,52 Z"'
               f' fill="{RUBIN}" {o(3)}/></g>')
    # дочка в шубке и валенках с мешочком
    dx = mx + 190
    s += SL(0, figura(dx, 1010, 330, t, "#7a5a4a", HOLOD_KANT, .6, False, False, 1.0,
                      3.0, True, True, "#f3d3b2", False, MOLOKO, False))
    s += SL(0, f'<path d="M{dx-52},1010 q20,-80 52,-80 q32,0 52,80 Z"'
               f' fill="#6b6256" {o(4)}/>')
    ruk3, (h3x, h3y) = rukav(dx + 56, 820, 120, 88, t, "#7a5a4a", HOLOD_KANT, .3, 5.0)
    s += SL(0, ruk3)
    s += SL(0, f'<path d="M{h3x-30:.0f},{h3y:.0f} q30,-16 60,0 l8,76 q-38,16 -76,0 Z"'
               f' fill="{KORALL}" {o(4)}/>')
    s += SL(0, para_izo_rta(mx + 40, 700, t, .2, 1.1, .5))
    s += SL(0, para_izo_rta(dx + 30, 810, t, .6, .8, .45))
    # фонари, троллейбус-силуэт, собака
    for i, fx2 in enumerate((160, 760)):
        s += SL(Z_SRED, f'<rect x="{fx2}" y="380" width="14" height="530"'
                        f' fill="{CHUGUN}" {o(4)}/>'
                        f'<path d="M{fx2-40},380 q47,-54 94,0 Z" fill="{ZOLOTO}"'
                        f' opacity=".9" {o(3)}/>')
        s += SL(Z_SRED, teplo(fx2 + 7, 400, 240, 220, .28 + .08 * abs(A.w(t, 2.0, i * .3))))
    s += SL(Z_DAL, f'<path d="M60,780 h420 l0,120 h-420 Z" fill="#1d2630" {o(5)}/>')
    sob = 40 * A.w(t, 2.6)
    s += SL(Z_SRED, f'<ellipse cx="{mx-220+sob:.0f}" cy="980" rx="56" ry="28"'
                    f' fill="#3a3028" {o(4)}/>'
                    f'<circle cx="{mx-170+sob:.0f}" cy="950" r="24" fill="#3a3028" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def sapogi_u_dveri(t):
    """Прихожая в гостях: гостья меняет сапоги на лодочки, рядом на коврике
    натекла снежная лужица, кот нюхает сапог."""
    rnd = random.Random(2070)
    s = f'<rect width="{W}" height="{H}" fill="#241d1c"/>'
    s += SL(Z_NEBO, nebo("noch", t, False, 141))
    s += SL(Z_DAL, stena("kirpich", t, 131))
    s += SL(Z_DAL, dver(1480, 120, 380, 820, .12, "url(#derev)", True, True))
    s += SL(Z_SRED, polovicy(1000))
    # вешалка с шубами
    s += SL(Z_SRED, f'<rect x="120" y="260" width="700" height="18" rx="8"'
                    f' fill="{SEREBRO}" {o(4)}/>')
    for i, c in enumerate(("#6b5347", "#4a3f38", "#7a6a58")):
        sx = 240 + i * 220
        s += SL(Z_SRED, naryad_plechiki(sx, 280, 420, t, c, 1.2, i * .3, False, MOLOKO, .0, 142 + i))
    # коврик, сапоги, лужица
    s += SL(Z_SRED, f'<rect x="900" y="940" width="560" height="110" rx="12"'
                    f' fill="#5a4038" {o(5)}/>')
    for i in range(10):
        s += SL(Z_SRED, f'<path d="M{920+i*56},944 l0,102" stroke="#7a5a4a"'
                        f' stroke-width="4" opacity=".7"/>')
    for i in range(2):
        bx = 980 + i * 120
        s += SL(0, f'<path d="M{bx-40},1000 q-12,-250 48,-256 q60,6 48,256 Z"'
                   f' fill="#3a3038" {o(5)}/>'
                   f'<path d="M{bx+8},760 l0,230" stroke="{SEREBRO}" stroke-width="5"/>')
    luzh = .5 + .5 * A.seg(t, .4, 2.4)
    s += SL(Z_SRED, f'<ellipse cx="1060" cy="1046" rx="{150*luzh:.0f}" ry="{28*luzh:.0f}"'
                    f' fill="{STEKLO}" opacity=".45"/>')
    # гостья на пуфе надевает вторую лодочку
    s += SL(0, f'<path d="M520,1000 q-30,-160 80,-166 q110,6 80,166 Z"'
               f' fill="#45384f" {o(6)}/>')
    s += SL(0, figura(600, 870, 430, t, RUBIN, TEPLO_SVET, .2, False, False, 1.0,
                      2.0, True, True, "#f0cfae", True, MOLOKO, False))
    nad = A.out(A.seg(t, .4, 1.4))
    for sgn in (-1, 1):
        ruk, (hx, hy) = rukav(600 + sgn * 70, 690, 200, 64 + sgn * 12 + 14 * nad, t,
                              RUBIN, TEPLO_SVET, .2 + (0 if sgn < 0 else .3), 4.0)
        s += SL(0, ruk)
    s += SL(0, tufli(540, 1000, 1.0, GRAFIT, t, False))
    s += SL(0, f'<g transform="translate({40*(1-nad):.0f},{-60*(1-nad):.0f})">'
               + tufli(660, 1000, 1.0, GRAFIT, t, False) + "</g>")
    # пакет, сумочка, венок, тапки, кот
    s += SL(Z_SRED, f'<path d="M820,1000 h120 l14,-150 h-148 Z" fill="{KREM2}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M760,960 q40,-16 62,14 l12,86 h-92 Z" fill="{GRAFIT}" {o(4)}/>')
    ven = ""
    for i in range(14):
        a = i * 26
        ven += (f'<ellipse cx="{1660+80*math.cos(math.radians(a)):.0f}"'
                f' cy="{300+80*math.sin(math.radians(a)):.0f}" rx="20" ry="12"'
                f' fill="{HVOYA}" {o(2)}/>')
    s += SL(Z_SRED, ven)
    s += SL(Z_SRED, "".join(f'<path d="M{1240+i*80},1020 q40,-40 80,0 q-40,24 -80,0 Z"'
                            f' fill="{KORALL}" {o(3)}/>' for i in range(2)))
    s += SL(Z_SRED, kot(1180, 1000, t, 1.4, "#6b5a46"))
    s += SL(Z_SRED, girlyanda(120, 150, 1700, t, 10, 145, 52))
    s += SL(0, lampa_stolika(1300, 420, t, 1.3))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


# ═══ из chast3.py ═══
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
    s += SL(Z_SRED, f'<rect x="1314" y="174" width="492" height="592" fill="{STEKLO}"'
                    f' opacity=".24"/>')
    # В ЗЕРКАЛЕ ОТРАЖАЕТСЯ НАРЯД, А НЕ ПУСТОТА (осмотр 16.11).
    s += SL(Z_SRED, f'<g opacity=".55">'
                    + naryad_plechiki(1560, 210, 440, t, VINO, 1.1, .4, True, None, .0, 196)
                    + "</g>")
    s += SL(Z_SRED, zerkalo(1300, 160, 520, 620, t, "pryam", ZOLOTO, True))
    # пуфик крупно
    s += SL(0, f'<path d="M620,1000 q-50,-230 160,-238 q210,8 160,238 Z"'
               f' fill="#45384f" {o(7)}/>')
    s += SL(0, f'<ellipse cx="780" cy="770" rx="170" ry="40" fill="#51425c" {o(4)}/>')
    bl = .6 + .4 * abs(A.w(t, 1.7))
    s += SL(0, f'<path d="M560,740 q140,-80 280,0 l30,190 q-170,46 -340,0 Z"'
               f' fill="{GRAFIT}" {o(6)}/>')
    s += SL(0, f'<path d="M560,740 q140,-80 280,0" fill="none" stroke="{SEREBRO}"'
               f' stroke-width="14" opacity="{bl:.2f}"/>')
    s += SL(0, f'<path d="M620,730 q80,-150 170,-16" fill="none" stroke="{SEREBRO}"'
               f' stroke-width="10"/>')
    s += SL(0, tkan_blesk(560, 720, 280, 210, t, "#ffffff", .5, .2))
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


# ═══ из chast4.py ═══
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


# источники света сцен: сюда ставится блик в объектив (C16/K17)
BLIKI = {
    "atlasnaya_bluzka_pod_lampoy": (1760, 756),
    "babushkin_persten_s_rubinom": (1680, 260),
    "chernilnica_i_temno_sinee_plate": (560, 320),
    "chernoe_plate_i_krasnaya_detal": (1480, 900),
    "dve_kartochki_na_veshalke": (300, 1046),
    "fartuk_na_kryuchke": (1580, 700),
    "fotografiya_u_elki": (560, 930),
    "hozyayka_stavit_salatnik": (400, 892),
    "hozyayka_ves_vecher": (1260, 930),
    "ladon_na_tkani_i_vecher": (1660, 1006),
    "lavandovyy_i_svetlo_seryy": (840, 876),
    "muzh_v_vyglazhennoy_rubashke_za_st": (640, 862),
    "sergi_na_barhatnoy_podushechke": (1700, 940),
    "sous_letit_na_rubashku": (760, 824),
    "sumochka_brosh_i_kole": (1800, 950),
    "svetlaya_rubashka_na_plechikah": (1320, 752),
    "tanec_v_polnoch": (1340, 866),
    "tri_ukrasheniya_na_vybor": (1300, 980),
    "yarlyk_i_malenkie_nozhnicy": (1700, 220),
    "zolotye_melochi_na_zhakete": (1680, 260),
}
