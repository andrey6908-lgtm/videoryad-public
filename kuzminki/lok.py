# -*- coding: utf-8 -*-
"""77 декораций ролика «13 ноября — Спиридон и Никодим».
Каждая — функция времени f(t) -> svg. Главное живёт в ЛЕВОЙ полосе 0-830:
правую половину занимает окно вставки (R-0007, мина 3 «Ёлки»).
В каждой декорации минимум три живых элемента (R-0006).
"""
import math, random
from baza import *
# необёрнутые версии: внутри окна вставки слои глубины не нужны
from baza import (_nebo, _oblaka, _tuman, _ulica_dal, _panelka, _sneg_lezhit,
                  _sneg_letit, _utvar_izby, _utvar_pekarni, _kvartira_veschi,
                  _mebel_hlam, _ramka_pp, _vinetka)
import anim as A

OKNO = (860, 300, 980, 551)          # неподвижный контейнер вставки

# Дата ролика. У Спиридона число было вшито прямо в рисунок календаря, и на
# Кузьминках в кадре весь ролик стояло «13 ноября» (поймано на пробнике 11.11).
DEN, MESYAC, DEN_NED = "14", "НОЯБРЯ", "суббота"


# ─────────────────────────── 1. ОТКРЫТИЕ ───────────────────────────
def kalendar(t):
    """Стена в обоях, КРУПНЫЙ отрывной календарь, ходики, комод.
    Правая половина 830-1920 свободна под титр-обещание (R-0004)."""
    s = f'<rect width="{W}" height="{H}" fill="#6d5a4a"/>'
    for r in range(11):
        for c in range(17):
            x, y = c * 118 + (59 if r % 2 else 0), r * 104
            s += (f'<path d="M{x},{y+44} q13,-28 28,0 q-15,9 -28,0 Z" fill="{TKAN}" opacity=".26"/>'
                  f'<circle cx="{x+14}" cy="{y+26}" r="6" fill="{ZOL}" opacity=".24"/>')
    s += f'<rect y="{H-210}" width="{W}" height="36" fill="{DOSKA2}" {o(5)}/>'
    s += polovicy(H - 174)
    s += teplo(390, 480, 680, 580, .85)
    # комод под календарём — второй план
    s += ten(400, 1010, 300, 26, .5)
    s += f'<rect x="120" y="790" width="560" height="190" rx="10" fill="url(#derev)" {o(7)}/>'
    s += f'<path d="M140,788 q260,-26 520,0 q-260,20 -520,0 Z" fill="url(#rush)" {o(5)}/>'
    for i, x in enumerate((230, 560)):
        s += krynka(x, 784, .62)
    # КАЛЕНДАРЬ крупно
    s += ten(400, 772, 200, 22, .5)
    s += f'<rect x="156" y="170" width="490" height="600" rx="14" fill="url(#derev)" {o(8)}/>'
    s += f'<rect x="192" y="214" width="418" height="520" rx="10" fill="url(#list)" {o(6)}/>'
    kach = 2.4 * A.w(t, 3.4)
    s += (f'<g transform="rotate({kach:.2f} 401 236)">'
          f'<rect x="196" y="232" width="410" height="490" rx="8" fill="url(#krem)" {o(6)}/>'
          f'<text x="401" y="520" font-family="DejaVu Serif, Georgia, serif" font-size="252"'
          f' fill="{KRAS}" text-anchor="middle" font-weight="bold">{DEN}</text>'
          f'<text x="401" y="620" font-family="DejaVu Sans" font-size="66" fill="{K}"'
          f' text-anchor="middle" letter-spacing="8">{MESYAC}</text>'
          f'<line x1="236" y1="664" x2="566" y2="664" stroke="{K}" stroke-width="4" opacity=".4"/>'
          f'<text x="401" y="700" font-family="DejaVu Sans" font-size="34" fill="{K}"'
          f' text-anchor="middle" opacity=".65">{DEN_NED}</text></g>')
    s += f'<circle cx="401" cy="196" r="15" fill="url(#zhel)" {o(5)}/>'
    s += hodiki(740, 300, t, 1.5)
    s += zanaveska(0, -20, 420, 190, TKAN, t, 1)
    s += ramka_pp("levo", "#120e0b", .5)
    s += mebel_hlam(1560, 1010, 360, t, 21)
    s += vinetka(.4)
    return s


def bufet(t):
    """Буфет: на столе узелок с добром — платок, посуда, связка ключей."""
    s = brevna(-20, -20, W + 40, H + 40, 102)
    s += f'<rect width="{W}" height="{H}" fill="#1e1a22" opacity=".42"/>'
    s += polovicy(900)
    s += teplo(400, 520, 480, 420, .62)
    # буфет: верхние полки со посудой, нижние створки
    s += ten(400, 910, 330, 24, .5)
    s += f'<rect x="90" y="150" width="620" height="760" rx="14" fill="url(#derev)" {o(8)}/>'
    s += f'<rect x="120" y="186" width="560" height="330" rx="8" fill="#2a2029" {o(5)}/>'
    for i, y in enumerate((300, 440)):
        s += polka(130, y, 540)
        for j in range(4):
            x = 190 + j * 130
            if (i + j) % 2:
                s += krynka(x, y - 6, .55)
            else:
                s += (f'<ellipse cx="{x}" cy="{y-18}" rx="44" ry="14" fill="url(#krem)" {o(5)}/>'
                      f'<path d="M{x-44},{y-18} q44,26 88,0 l-6,22 h-76 Z" fill="url(#krem)" {o(4)}/>')
    s += (f'<rect x="120" y="540" width="560" height="30" rx="8" fill="url(#dosk)" {o(6)}/>')
    for x in (130, 410):
        s += (f'<rect x="{x}" y="590" width="270" height="300" rx="8" fill="url(#dosk)" {o(6)}/>'
              f'<circle cx="{x+230}" cy="740" r="12" fill="url(#zhel)" {o(4)}/>')
    # узелок на откинутой доске
    s += (f'<rect x="60" y="560" width="660" height="26" rx="8" fill="url(#derev)" {o(6)}/>')
    s += ten(350, 560, 120, 14, .4)
    s += (f'<path d="M240,556 q110,-150 220,0 Z" fill="url(#tkan)" {o(7)}/>'
          f'<path d="M300,470 q50,-56 100,0 q-50,26 -100,0 Z" fill="#c2524a" {o(5)}/>')
    for i in range(6):
        s += (f'<circle cx="{268+i*32}" cy="{520+(i%3)*10}" r="7" fill="#f2d9b0" opacity=".7"/>')
    # связка ключей качается на гвозде
    kach = 4.6 * A.w(t, 2.4)
    s += (f'<g transform="rotate({kach:.2f} 760 470)">'
          f'<circle cx="760" cy="470" r="16" fill="none" stroke="url(#zhel)" stroke-width="8"/>')
    for i, a_ in enumerate((-16, 0, 18)):
        s += (f'<g transform="rotate({a_} 760 486)">'
              f'<rect x="754" y="486" width="12" height="96" rx="5" fill="url(#med)" {o(3)}/>'
              f'<path d="M754,560 h-14 v14 h14 M766,540 h12 v12 h-12" fill="url(#med)" {o(3)}/></g>')
    s += "</g>"
    s += blik(760, 470, t, .8, "#ffe9b0", SVET, .5)
    s += mebel_hlam(1420, 960, 500, t, 85)
    s += ramka_pp("levo", "#0d0b10", .46)
    s += vinetka(.46)
    return s


def pekarnya_noch(t):
    """Ночная пекарня через широкий дверной проём: силуэт пекаря, печь, ведро."""
    s = f'<rect width="{W}" height="{H}" fill="#0f1420"/>'
    s += kladka(0, 0, W, H, 92, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#0b1018" opacity=".58"/>'
    s += f'<path d="M80,1080 V300 q320,-230 640,0 V1080 Z" fill="#1a120d" {o(10)}/>'
    s += f'<clipPath id="proem"><path d="M80,1080 V300 q320,-230 640,0 V1080 Z"/></clipPath>'
    s += '<g clip-path="url(#proem)">'
    s += f'<rect x="80" y="60" width="640" height="1020" fill="#231610"/>'
    s += kladka(80, 60, 640, 1020, 86, "url(#kamen)")
    s += f'<rect x="80" y="60" width="640" height="1020" fill="#1b0f09" opacity=".62"/>'
    s += teplo(400, 760, 460, 420, 1.0)
    # печь крупно
    s += f'<path d="M150,960 v-300 q250,-210 500,0 v300 Z" fill="{CHUGUN}" {o(8)}/>'
    s += f'<path d="M210,950 v-240 q190,-170 380,0 v240 Z" fill="#160d08" {o(6)}/>'
    s += ugli(250, 930, 300, t, 8)
    s += ogon(400, 930, t, 1.9, .2, 9)
    s += ogon(310, 936, t, 1.0, .7, 5)
    s += ogon(500, 936, t, 1.0, 1.4, 5)
    s += f'<g opacity=".45">{dym(400, 620, t, 5, .3, 420, .5, "#8d8a86", 1.5)}</g>'
    s += siluet(330, 1010, 540, "#0f0b08", .97, kant=ORA)
    s += "</g>"
    s += iskra_let(t, 400, 700, 10, 5, 380, .42)
    # ведро у стены, снаружи
    s += ten(880, 1006, 70, 14, .5)
    s += f'<path d="M812,896 l20,110 q48,16 96,0 l20,-110 Z" fill="url(#zhel)" {o(7)}/>'
    s += f'<path d="M812,900 q68,-50 136,0" fill="none" stroke="{ZHELEZ}" stroke-width="11"/>'
    s += ramka_pp("pravo", "#0a0d14", .55)
    s += utvar_pekarni(1060, 1000, 780, t, 24)
    s += vinetka(.52)
    return s


def kolodec(t):
    """Колодезный сруб крупно, отсвет пожара на стенах, рубаха с рукавами."""
    s = nebo("noch", t, True, 9)
    s += f'<ellipse cx="640" cy="240" rx="1200" ry="440" fill="{UGOL}" opacity="{.24+.1*abs(A.w(t,1.6)):.2f}"/>'
    # стена двора сзади — второй план, небо больше не пустует
    s += brevna(-20, 300, 1000, 460, 92)
    s += f'<rect x="-20" y="300" width="1000" height="460" fill="#1a2234" opacity=".55"/>'
    s += f'<path d="M-20,300 L480,170 L1000,300 Z" fill="{DOSKA2}" {o(7)}/>'
    s += teplo(300, 700, 620, 480, .55)
    s += sneg_lezhit(790, 18, "#3c4a60")
    s += f'<rect y="900" width="{W}" height="180" fill="#2a3346"/>'
    # сруб крупно
    s += ten(400, 1012, 310, 30, .6)
    s += brevna(130, 660, 540, 330, 78)
    s += f'<ellipse cx="400" cy="672" rx="268" ry="60" fill="#0d1726" {o(8)}/>'
    ryab = 6 * A.w(t, 2.2)
    s += (f'<ellipse cx="400" cy="{688+ryab:.0f}" rx="{216+10*A.w(t,2.6):.0f}" ry="42"'
          f' fill="url(#voda)" opacity=".92"/>')
    s += (f'<ellipse cx="340" cy="{682+ryab:.0f}" rx="58" ry="14" fill="{SVET}"'
          f' opacity="{.3+.35*abs(A.w(t,1.9)):.2f}"/>')
    for x in (150, 618):
        s += f'<rect x="{x}" y="300" width="46" height="376" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="120" y="262" width="572" height="42" rx="10" fill="url(#derev)" {o(7)}/>'
    s += f'<path d="M100,262 L406,150 L712,262 Z" fill="{DOSKA2}" {o(7)}/>'
    ang = 9 * A.w(t, 5.0)
    s += (f'<g transform="rotate({ang:.1f} 400 440)">'
          f'<rect x="172" y="416" width="456" height="50" rx="22" fill="url(#derev)" {o(7)}/>'
          f'<circle cx="648" cy="441" r="30" fill="url(#derev)" {o(6)}/></g>')
    # РУБАХА с завязанными рукавами — крупно, с неё каплет
    s += (f'<path d="M286,476 q116,-44 232,0 l-20,286 q-96,36 -192,0 Z" fill="url(#krem)" {o(8)}/>')
    s += f'<path d="M330,500 q72,-22 144,0" fill="none" stroke="#cdbf9f" stroke-width="8" opacity=".8"/>'
    for sgn, x0 in ((-1, 286), (1, 518)):
        s += (f'<path d="M{x0},486 q{sgn*96},64 {sgn*40},176" fill="none" stroke="{KREM}"'
              f' stroke-width="46" stroke-linecap="round"/>')
        s += f'<circle cx="{x0+sgn*42}" cy="{668}" r="27" fill="{PECH2}" {o(6)}/>'
        s += f'<path d="M{x0+sgn*26},654 q{sgn*34},18 {sgn*8},34" fill="none" stroke="{PECH2}" stroke-width="12"/>'
    kap = (t * .6) % 1.0
    s += f'<ellipse cx="402" cy="{770+kap*60:.0f}" rx="9" ry="14" fill="{STEKLO}" opacity="{1-kap:.2f}"/>'
    s += ramka_pp("levo", "#0a0f1a", .5)
    s += ulica_dal(1020, 900, 880, t, True, 34)
    s += vinetka(.48)
    return s


def dom_na_ladonyah(t):
    """Образ: дом на двух ладонях. Слева пламя тянется, справа пустой кошелёк."""
    s = f'<rect width="{W}" height="{H}" fill="#120e14"/>'
    s += teplo(430, 500, 620, 560, .6)
    kach = 1.4 * A.w(t, 5.6)
    s += f'<g transform="rotate({kach:.2f} 430 790)">'
    for sgn in (-1, 1):
        s += (f'<path d="M{430+sgn*20:.0f},840 q{sgn*250:.0f},-56 {sgn*268:.0f},96'
              f' q{-sgn*56:.0f},92 {-sgn*244:.0f},44 Z" fill="#c98c55" opacity=".95" {o(8)}/>')
        s += (f'<path d="M{430+sgn*60:.0f},858 q{sgn*180:.0f},-34 {sgn*196:.0f},64" fill="none"'
              f' stroke="#a8703c" stroke-width="7" opacity=".8"/>')
    # ДОМ крупно: слева изба, справа панельная стена
    s += ten(430, 834, 250, 24, .65)
    s += f'<rect x="246" y="520" width="188" height="316" fill="url(#brev)" {o(8)}/>'
    for i in range(4):
        s += f'<line x1="246" y1="{560+i*74}" x2="434" y2="{560+i*74}" stroke="#5a3721" stroke-width="5" opacity=".5"/>'
    s += f'<rect x="434" y="520" width="188" height="316" fill="url(#beton)" {o(8)}/>'
    s += f'<path d="M214,520 L430,336 L646,520 Z" fill="{DOSKA2}" {o(8)}/>'
    s += f'<path d="M214,520 L430,336 L646,520 l-34,-28 L430,372 L248,492 Z" fill="url(#sneg)" {o(5)}/>'
    s += okno_izby(292, 596, 104, 94, t, svet=True, moroz=.35)
    for i in range(2):
        for j in range(2):
            on = abs(A.w(t, 3.2 + i + j)) > .4
            s += (f'<rect x="{464+j*70}" y="{584+i*96}" width="54" height="66" rx="5"'
                  f' fill="{SVET if on else "#4a5a68"}" opacity="{.9 if on else .32}" {o(5)}/>')
    s += f'<rect x="398" y="712" width="64" height="124" rx="6" fill="url(#derev)" {o(6)}/>'
    s += "</g>"
    pl = .7 + .5 * abs(A.w(t, 2.8))
    s += ogon(118, 960, t, 3.4 * pl, 0, 12)
    s += ogon(208, 966, t, 1.8 * pl, .6, 6)
    s += f'<g opacity=".5">{dym(110, 760, t, 4, .25, 420, .4, "#6a6460", 1.2)}</g>'
    # кошелёк крупно: щёлкает и пуст
    s += ten(790, 962, 128, 20, .55)
    op = 9 * A.w(t, 3.0)
    s += (f'<path d="M650,950 v-160 q140,-58 280,0 v160 Z" fill="{TKAN2}" {o(8)}/>'
          f'<path d="M680,900 q110,-26 220,0" fill="none" stroke="#2f4760" stroke-width="8" opacity=".8"/>'
          f'<g transform="rotate({op:.1f} 790 796)">'
          f'<path d="M650,800 q140,-96 280,0 q-140,-32 -280,0 Z" fill="#2f4760" {o(7)}/></g>'
          f'<circle cx="790" cy="826" r="19" fill="url(#zhel)" opacity="{.5+.5*abs(A.w(t,3.0)):.2f}" {o(4)}/>')
    s += vinetka(.6)
    return s


def doschechki(t, den=False):
    """Семь пронумерованных дощечек на гвоздиках — опора счёта запретов."""
    s = brevna(-20, -20, W + 40, H + 40, 118)
    s += f'<rect width="{W}" height="{H}" fill="{"#f0e6d2" if den else "#1a1420"}" opacity="{.18 if den else .42}"/>'
    s += teplo(420, 520, 620, 520, .75 if not den else .45)
    for i in range(7):
        x = 110 + i * 100
        y = 420 + (18 if i % 2 else 0)
        kach = 3.4 * A.w(t, 2.6 + i * .3, i * .2)
        s += f'<circle cx="{x+34}" cy="{y-26}" r="9" fill="url(#zhel)" {o(3)}/>'
        s += (f'<g transform="rotate({kach:.2f} {x+34} {y-26})">'
              f'{ten(x+40, y+176, 40, 10, .4)}'
              f'<rect x="{x}" y="{y}" width="68" height="168" rx="10" fill="url(#dosk)" {o(6)}/>'
              f'<text x="{x+34}" y="{y+108}" font-family="DejaVu Serif, Georgia, serif"'
              f' font-size="74" fill="{K}" text-anchor="middle"'
              f' opacity="{.35+.65*A.seg(t,.3+i*.28,.5):.2f}">{i+1}</text></g>')
    s += f'<rect y="{H-120}" width="{W}" height="120" fill="url(#pol)" {o(5)}/>'
    s += f'<g opacity=".25">{dym(300, 980, t, 3, .12, 200, .3)}</g>'
    s += utvar_izby(900, 700, 940, t, 4)
    return s


def seni(t):
    """Сени Кузьминок: порог, на холстине горсть мелочи, за дверью сумрак.
    Рук не рисуем — подаянное лежит само (его правка 06.11)."""
    s = brevna(-20, -20, W + 40, H + 40, 98)
    s += f'<rect width="{W}" height="{H}" fill="#1b2230" opacity=".46"/>'
    s += polovicy(820, "url(#derev)")
    s += dver(96, 150, 360, 760, .42, "url(#derev)", kruchok=True)
    s += f'<rect x="104" y="162" width="136" height="736" fill="#9cc0dd" opacity=".46"/>'
    s += luch(150, 170, 430, 720, t, .17)
    s += f'<g opacity=".5">{par(200, 790, t, 5, .5, 400, .2, 1.7)}</g>'
    # порог первым планом, на нём холстина и мелочь
    s += ten(560, 940, 300, 26, .55)
    s += f'<rect x="300" y="880" width="520" height="54" rx="12" fill="url(#derev)" {o(7)}/>'
    s += (f'<path d="M360,878 q190,-40 380,0 l-26,46 h-328 Z" fill="url(#rush)" {o(5)}/>'
          f'<rect x="384" y="898" width="330" height="7" fill="{TKAN}" opacity=".75"/>')
    s += monety(548, 860, t, 7, 4, 1.15)
    s += lavka(612, 690, 240)
    s += krynka(700, 684, .7)
    s += teplo(520, 760, 420, 320, .5)
    s += utvar_izby(1040, 470, 780, t, 61)
    s += mebel_hlam(1300, 930, 620, t, 62)
    s += ramka_pp("levo", "#0d1016", .5)
    s += vinetka(.46)
    return s


def polka_zapasy(t):
    """Полка в сарае: молоток, стамеска, рубанок — каждый на своём месте."""
    s = doski(-20, -20, W + 40, H + 40, 118, True, "dosk")
    s += f'<rect width="{W}" height="{H}" fill="#241c14" opacity=".48"/>'
    s += luch(520, -30, 420, 980, t, .2)
    s += teplo(420, 520, 460, 380, .5)
    # жердь с крючками: инструмент висит ровно, по тени видно порядок
    s += f'<rect x="60" y="300" width="800" height="26" rx="10" fill="url(#derev)" {o(6)}/>'
    ins = []
    # молоток
    ins.append((150, lambda x: (
        f'<rect x="{x-9}" y="326" width="18" height="190" rx="8" fill="url(#derev)" {o(5)}/>'
        f'<rect x="{x-54}" y="516" width="108" height="46" rx="10" fill="url(#chug)" {o(6)}/>'
        f'<rect x="{x+54}" y="524" width="34" height="30" rx="6" fill="url(#chug)" {o(5)}/>')))
    # стамеска
    ins.append((330, lambda x: (
        f'<rect x="{x-11}" y="326" width="22" height="150" rx="9" fill="url(#med)" {o(5)}/>'
        f'<rect x="{x-8}" y="476" width="16" height="150" fill="url(#zhel)" {o(4)}/>'
        f'<path d="M{x-8},626 h16 l-8,22 Z" fill="#e8e2d2" {o(3)}/>')))
    # рубанок
    ins.append((560, lambda x: (
        f'<rect x="{x-96}" y="340" width="192" height="80" rx="12" fill="url(#derev)" {o(6)}/>'
        f'<path d="M{x-30},340 l50,-54 h30 l-40,54 Z" fill="url(#zhel)" {o(5)}/>'
        f'<rect x="{x-96}" y="402" width="192" height="18" rx="8" fill="#5f3f27" {o(4)}/>')))
    # клещи
    ins.append((760, lambda x: (
        f'<path d="M{x-10},326 l-30,230 M{x+10},326 l30,230" fill="none" stroke="url(#zhel)"'
        f' stroke-width="16" stroke-linecap="round"/>'
        f'<circle cx="{x}" cy="420" r="13" fill="{ZHELEZ}" {o(4)}/>')))
    for i, (x, f_) in enumerate(ins):
        bl = .25 + .75 * abs(A.w(t, 3.0 + i * .6, i * .25))
        s += ten(x, 660, 60, 14, .3)
        s += f_(x)
        s += (f'<rect x="{x-50}" y="300" width="100" height="14" rx="6" fill="{SVET}"'
              f' opacity="{.18*bl:.2f}"/>')
    # ремень на гвозде качается, на полу ровно уложены заготовки
    kach = 5.0 * A.w(t, 2.6)
    s += (f'<g transform="rotate({kach:.2f} 880 330)">'
          f'<path d="M880,330 q46,160 -10,300" fill="none" stroke="#6b4428" stroke-width="20"'
          f' stroke-linecap="round"/></g>')
    s += f'<rect y="900" width="{W}" height="180" fill="url(#pol)"/>'
    for i in range(5):
        s += (f'<rect x="{80+i*150}" y="{940+(i%2)*30}" width="130" height="26" rx="10"'
              f' fill="url(#zhel)" {o(4)}/>')
    s += f'<g opacity=".4">{par(520, 880, t, 4, .3, 320, .2, 2.2)}</g>'
    s += mebel_hlam(1480, 1000, 440, t, 95)
    s += ramka_pp("levo", "#0e0a07", .48)
    s += vinetka(.48)
    return s


def kuryatnik_lunka(t, uzko=True):
    """Полиэкран: слева курятник с пустым гнездом, справа лунка с пустой сетью.
    При uzko обе половины живут слева — правую занимает окно вставки."""
    X0, XW = (0, 830) if uzko else (0, W)
    hw = XW / 2
    s = f'<rect width="{W}" height="{H}" fill="#101722"/>'
    # левая: курятник
    s += f'<clipPath id="plL"><rect x="{X0}" y="0" width="{hw:.0f}" height="{H}"/></clipPath>'
    s += f'<g clip-path="url(#plL)">'
    s += doski(X0 - 20, 0, hw + 40, H, 92, True, "dosk")
    s += f'<rect x="{X0}" width="{hw:.0f}" height="{H}" fill="#2a1f16" opacity=".4"/>'
    s += teplo(X0 + hw * .5, 560, 300, 300, .5)
    s += f'<rect x="{X0+20}" y="700" width="{hw-60:.0f}" height="28" rx="10" fill="url(#derev)" {o(6)}/>'
    for i in range(3):
        s += kura(X0 + 90 + i * 110, 700, t, .62, i * .3, "#ded0b8")
    s += (f'<path d="M{X0+60},980 q{hw*.5:.0f},-110 {hw-120:.0f},0 Z" fill="url(#solom)" {o(6)}/>')
    s += f'<ellipse cx="{X0+hw*.5:.0f}" cy="965" rx="86" ry="36" fill="#6b5424" {o(5)}/>'
    pp = (t * .5) % 1.0
    s += (f'<ellipse cx="{X0+hw*.5+30*A.w(t,3.0):.0f}" cy="{820+pp*120:.0f}" rx="16" ry="6"'
          f' fill="#fffaf0" opacity="{1-pp:.2f}" transform="rotate({pp*120:.0f} {X0+hw*.5:.0f} {820+pp*120:.0f})"/>')
    s += "</g>"
    # правая: лёд и лунка
    s += f'<clipPath id="plR"><rect x="{X0+hw:.0f}" y="0" width="{hw:.0f}" height="{H}"/></clipPath>'
    s += f'<g clip-path="url(#plR)">'
    s += f'<rect x="{X0+hw:.0f}" width="{hw:.0f}" height="{H}" fill="url(#led)"/>'
    for i in range(7):
        s += (f'<path d="M{X0+hw+i*60:.0f},0 l40,1080" stroke="#ffffff" stroke-width="3" opacity=".25"/>')
    cx = X0 + hw * 1.5
    s += f'<ellipse cx="{cx:.0f}" cy="640" rx="118" ry="60" fill="{VODA2}" {o(7)}/>'
    s += (f'<ellipse cx="{cx:.0f}" cy="{640+5*A.w(t,2.4):.0f}" rx="{100+6*A.w(t,2.0):.0f}" ry="46"'
          f' fill="url(#voda)" opacity=".95"/>')
    s += (f'<path d="M{cx-60:.0f},640 q60,160 120,0" fill="none" stroke="{KREM}"'
          f' stroke-width="4" stroke-dasharray="10 12" opacity=".8"/>')
    s += f'<path d="M{cx-70:.0f},700 q70,130 140,0 q-70,40 -140,0 Z" fill="#cfe0ea" opacity=".5" {o(4)}/>'
    s += sneg_letit(t, 16, 8, .5, .6)
    s += "</g>"
    s += f'<rect x="{X0+hw-4:.0f}" width="8" height="{H}" fill="{K}" opacity=".85"/>'
    return s


def izba_vecher(t):
    """Стол, две кружки, свеча между ними — и две тени на стене ВРОЗЬ."""
    s = brevna(-20, -20, W + 40, H + 40, 106)
    s += f'<rect width="{W}" height="{H}" fill="#161d2b" opacity=".5"/>'
    # тени расходятся по стене
    raz = 36 * (.5 + .5 * A.w(t, 7.0))
    for sgn, x in ((-1, 300), (1, 560)):
        s += (f'<g opacity=".4" transform="translate({sgn*raz:.0f},0)">'
              f'{siluet(x, 560, 420, "#0b0e14", .9)}</g>')
    s += polovicy(880)
    s += teplo(430, 600, 400, 330, .66)
    s += stol(190, 690, 520)
    s += (f'<path d="M210,686 q260,-40 520,0 l-28,38 h-464 Z" fill="url(#rush)" {o(5)}/>')
    s += svecha(452, 596, t, 0, 1.3)
    for i, x in enumerate((300, 604)):
        s += ten(x, 694, 52, 10, .4)
        s += (f'<path d="M{x-42},612 v56 q42,24 84,0 v-56 Z" fill="url(#krem)" {o(6)}/>'
              f'<path d="M{x+42},628 q38,26 0,52" fill="none" stroke="{KREM}" stroke-width="13"/>'
              f'<ellipse cx="{x}" cy="612" rx="42" ry="11" fill="#dcc9a4" {o(4)}/>')
        s += f'<g opacity=".4">{par(x, 600, t, 3, .4, 150, .34)}</g>'
    s += lavka(170, 790, 200)
    s += lavka(560, 790, 200)
    s += utvar_izby(1120, 560, 740, t, 70)
    s += mebel_hlam(1460, 950, 460, t, 71)
    s += ramka_pp("levo", "#0a0c12", .5)
    s += vinetka(.5)
    return s


def okno_chuzhoj(t):
    """Из тёмной избы видно дорогу: по ней идёт прохожий с котомкой."""
    s = brevna(-20, -20, W + 40, H + 40, 102)
    s += f'<rect width="{W}" height="{H}" fill="#121926" opacity=".66"/>'
    s += polovicy(900)
    p = (t * .055) % 1.0
    vid = (f'<rect x="150" y="190" width="520" height="520" fill="#6d8aa8"/>'
           f'<rect x="150" y="470" width="520" height="240" fill="#cfdeee"/>'
           + ulica_dal(150, 470, 520, t, True, 71)
           + siluet(200 + p * 420, 660, 150, "#242a33", .95, False, "#9fb6cc")
           + f'<g opacity=".5">{sneg_letit(t, 22, 9, .6, .8)}</g>')
    s += okno_izby(150, 190, 520, 520, t, vid, moroz=.85, svet=False)
    s += f'<g opacity=".55">{par(400, 700, t, 4, .45, 260, .25, 1.4)}</g>'
    s += zanaveska(130, 176, 540, 150, TKAN2, t, 1)
    s += zanaveska(690, 176, 540, 150, TKAN2, t, -1)
    s += teplo(760, 860, 420, 300, .34)
    s += svecha(770, 806, t, .2, 1.1)
    s += lavka(140, 790, 230)
    s += utvar_izby(1100, 520, 760, t, 68)
    s += mebel_hlam(1440, 940, 480, t, 69)
    s += ramka_pp("levo", "#0a0d13", .55)
    s += vinetka(.5)
    return s


def prihozhaya(t):
    """Городская прихожая: тумбочка, телефон на салфетке, зеркало, дверь."""
    s = f'<rect width="{W}" height="{H}" fill="#8a7f72"/>'
    for c in range(9):
        s += f'<rect x="{c*96}" width="90" height="{H}" fill="#9c8f80" opacity="{.3 if c%2 else .14}"/>'
    s += f'<rect y="880" width="{W}" height="200" fill="url(#pol)" {o(5)}/>'
    s += f'<rect y="840" width="{W}" height="46" fill="{POL2}" {o(4)}/>'
    s += teplo(380, 420, 520, 460, .55)
    s += dver(560, 120, 330, 760, 0, "url(#derev)", cepochka=True)
    s += f'<rect x="896" y="430" width="30" height="110" rx="8" fill="url(#zhel)" {o(5)}/>'
    # зеркало
    s += f'<rect x="120" y="170" width="230" height="330" rx="14" fill="url(#stekl)" opacity=".8" {o(7)}/>'
    s += f'<path d="M140,470 l190,-280" stroke="#ffffff" stroke-width="22" opacity=".22"/>'
    # тумбочка с салфеткой и телефоном
    s += ten(290, 900, 190, 20, .5)
    s += f'<rect x="130" y="620" width="330" height="270" rx="10" fill="url(#derev)" {o(7)}/>'
    s += f'<path d="M150,618 q145,-28 290,0 q-145,22 -290,0 Z" fill="url(#rush)" {o(5)}/>'
    dx = 7 * A.w(t, 1.1)
    s += (f'<g transform="translate({dx:.1f},0)">'
          f'{ten(292, 616, 60, 8, .4)}'
          f'<rect x="232" y="548" width="120" height="66" rx="12" fill="{CHUGUN}" {o(5)}/>'
          f'<rect x="242" y="556" width="100" height="50" rx="6"'
          f' fill="{SVET if abs(A.w(t,1.0))>.2 else "#2b3a4a"}" opacity=".95"/></g>')
    s += f'<rect x="700" y="300" width="110" height="26" rx="8" fill="url(#derev)" {o(5)}/>'
    for i, x in enumerate((720, 770)):
        s += f'<circle cx="{x}" cy="336" r="10" fill="{ZHELEZ}" {o(3)}/>'
    s += kvartira_veschi(1020, 880, 860, t, 57)
    return s


# ─────────────────────── 2. ИСТОРИЯ ДНЯ ───────────────────────
def holm(t):
    """Холм над рекой: два свежих холмика врозь, рябина, осень, низкое небо."""
    s = nebo("rassv", t, False, 41)
    s += f'<g opacity=".6">{oblaka(t, 190, 5, 43, .55, "#c3ccd8", 15.0)}</g>'
    s += SL(Z_DAL, f'<path d="M-20,620 q500,-120 1000,-40 q500,80 960,-30 L{W},1080 H-20 Z"'
                   f' fill="#55634a" opacity=".75"/>')
    # река лентой в глубине
    s += (f'<path d="M-20,700 q420,60 900,20 q520,-44 1060,30 l0,60 q-540,-60 -1060,-10'
          f' q-480,46 -900,-20 Z" fill="url(#voda)" opacity=".9"/>')
    for i in range(5):
        p = ((t * .18 + i * .2) % 1.0)
        s += (f'<path d="M{100+p*1500:.0f},{712+i*12} h120" stroke="#cfe6f2"'
              f' stroke-width="4" opacity="{.35*(1-p):.2f}"/>')
    # холм первым планом, трава клонится
    s += (f'<path d="M-20,900 q460,-160 980,-110 q520,50 980,120 L{W},1080 H-20 Z"'
          f' fill="#6b7a52" {o(0)}/>')
    for i in range(46):
        x = 20 + i * 42
        h_ = 40 + (i % 5) * 18
        kl = 7 * A.w(t, 3.2, i * .07)
        s += (f'<path d="M{x},960 q{kl:.1f},-{h_*.6:.0f} {kl*2:.1f},-{h_}" fill="none"'
              f' stroke="{TRAVA}" stroke-width="5" opacity=".8"/>')
    # два холмика ВРОЗЬ, у каждого свой крест
    for i, (x, sc) in enumerate(((240, 1.0), (680, .86))):
        w_ = 210 * sc
        y = 960 - i * 40
        s += ten(x, y, w_ * 1.05, 28, .45)
        s += (f'<path d="M{x-w_:.0f},{y:.0f} q{w_:.0f},-{150*sc:.0f} {w_*2:.0f},0 Z"'
              f' fill="#6f5c3c" {o(7)}/>'
              f'<path d="M{x-w_:.0f},{y:.0f} q{w_:.0f},-{150*sc:.0f} {w_*2:.0f},0 Z"'
              f' fill="#7d8b55" opacity=".4"/>')
        kach = 1.0 * A.w(t, 5.0, i * .4)
        s += (f'<g transform="rotate({kach:.2f} {x:.0f} {y:.0f})">'
              f'<rect x="{x-18*sc:.0f}" y="{y-420*sc:.0f}" width="{36*sc:.0f}"'
              f' height="{420*sc:.0f}" rx="10" fill="url(#derev)" {o(6)}/>'
              f'<rect x="{x-110*sc:.0f}" y="{y-320*sc:.0f}" width="{220*sc:.0f}"'
              f' height="{34*sc:.0f}" rx="10" fill="url(#derev)" {o(6)}/>'
              f'<path d="M{x-70*sc:.0f},{y-180*sc:.0f} h{140*sc:.0f}" stroke="#8a6a46"'
              f' stroke-width="{10*sc:.0f}"/></g>')
    s += ryabina(820, 900, t, 1.25, 6)
    # листья летят
    for i in range(10):
        p = ((t * .12 + i * .1) % 1.0)
        x = 760 - p * 760
        y = 560 + 300 * p + 40 * A.w(t, 2.0, i * .2)
        s += (f'<path d="M{x:.0f},{y:.0f} q16,-14 32,2 q-16,14 -32,-2 Z" fill="{ORA}"'
              f' opacity="{.8*(1-p*.5):.2f}" transform="rotate({p*320:.0f} {x:.0f} {y:.0f})"/>')
    s += ramka_pp("levo", "#1b2018", .42)
    s += vinetka(.44)
    return s


def vorota(t):
    """Ворота обители: у створок стоят люди, спорят — фигуры покачиваются."""
    s = nebo("sumer", t, False, 47)
    s += f'<g opacity=".5">{oblaka(t, 170, 4, 49, .5, "#a9b4c2", 16.0)}</g>'
    s += kladka(-20, 120, 980, 840, 86, "url(#kamen)")
    s += (f'<path d="M-40,130 L460,30 L960,130 Z" fill="#3b342c" {o(8)}/>')
    # арка ворот
    s += (f'<path d="M190,960 V520 q270,-230 540,0 V960 Z" fill="#17120f" {o(9)}/>')
    s += f'<g opacity=".5">{teplo(460, 820, 300, 260, .6)}</g>'
    # створки приоткрыты, одна движется
    dv = 5 * A.w(t, 9.0)
    s += (f'<g transform="rotate({dv:.2f} 206 960)">'
          f'<rect x="206" y="560" width="240" height="400" fill="url(#derev)" {o(7)}/>'
          f'{doski(212, 566, 228, 388, 76, True, "dosk")}</g>'
          f'<rect x="474" y="560" width="240" height="400" fill="url(#derev)" {o(7)}/>'
          f'{doski(480, 566, 228, 388, 76, True, "dosk")}')
    for y in (640, 860):
        s += f'<rect x="206" y="{y}" width="508" height="24" rx="8" fill="url(#zhel)" {o(5)}/>'
    # люди у ворот: наклоны врозь — спорят
    for i, (x, h_, ph) in enumerate(((160, 340, .0), (300, 320, .3), (820, 330, .55), (960, 310, .8))):
        kach = 3.4 * A.w(t, 3.0 + i * .4, ph)
        s += (f'<g transform="rotate({kach:.2f} {x} 960)">'
              f'{siluet(x, 960, h_, "#1d2027", .95, i % 2 == 0, "#8d9aa8")}</g>')
    s += sneg_lezhit(956, 16)
    s += f'<g opacity=".5">{tuman(t, 880, .4, "#c8d4e0")}</g>'
    for i in range(4):
        s += ptica(1100 + i * 90, 240 + (i % 2) * 60, t, .7, "#3a4450", i * .3)
    s += ramka_pp("oba", "#0a0c11", .5)
    s += vinetka(.48)
    return s


def kelya(t):
    """Стол с книгами и свитками, светец с лучиной, две склонённые фигуры."""
    s = kladka(-20, -20, W + 40, H + 40, 88, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#191410" opacity=".6"/>'
    s += svody(t, "#423a30", 3)
    s += polovicy(900, "url(#dosk)")
    s += teplo(400, 560, 480, 400, .78)
    # светец с лучиной: трещит и роняет искру
    s += (f'<rect x="760" y="430" width="20" height="470" rx="8" fill="url(#chug)" {o(5)}/>'
          f'<path d="M742,430 q28,-40 56,-10" fill="none" stroke="{ZHELEZ}" stroke-width="10"/>')
    s += ogon(786, 404, t, .9, .3, 4)
    s += iskra_let(t, 786, 404, 7, 11, 220, .4)
    s += stol(170, 660, 540)
    # две склонённые фигуры за столом
    s += siluet(300, 660, 330, "#2b2219", .96, False, "#b98b4e")
    s += siluet(520, 666, 318, "#251e16", .96, False, "#b98b4e")
    # книга раскрыта, страница шевелится
    kach = 2.2 * A.w(t, 3.6)
    s += (f'<path d="M250,648 q170,-40 340,0 l0,-54 q-170,-36 -340,0 Z" fill="url(#list)" {o(6)}/>'
          f'<g transform="rotate({kach:.2f} 420 600)">'
          f'<path d="M420,594 q86,-26 170,0 l0,52 q-84,-24 -170,0 Z" fill="#f6efdc" {o(5)}/></g>'
          f'<line x1="420" y1="594" x2="420" y2="648" stroke="#8a7a58" stroke-width="4"/>')
    for i in range(4):
        s += (f'<line x1="282" y1="{612+i*11}" x2="396" y2="{608+i*11}" stroke="#7d6a45"'
              f' stroke-width="3" opacity=".7"/>')
    # свитки на столе и в корзине
    for i, (x, y) in enumerate(((620, 640), (668, 648))):
        s += (f'<rect x="{x}" y="{y}" width="120" height="26" rx="13" fill="url(#list)" {o(5)}/>')
    s += f'<g opacity=".35">{par(400, 640, t, 3, .3, 220, .2, 1.8)}</g>'
    s += mebel_hlam(1480, 1000, 440, t, 77)
    s += ramka_pp("levo", "#0b0806", .52)
    s += vinetka(.52)
    return s


def pekarnya_gody(t):
    """Стена пекарни с одним тёплым окном; вокруг сменяются времена года."""
    sez = (t * .22) % 4.0
    k = int(sez)
    fon = ["#5e7a4a", "#8a6f3e", "#6a7480", "#cfdcea"][k]
    s = f'<rect width="{W}" height="{H}" fill="{fon}"/>'
    s += oblaka(t, 200, 4, 6, .35, "#eef3f8", 14)
    s += kladka(0, 300, 830, 780, 90, "url(#kamen)")
    s += f'<path d="M-20,300 L420,180 L860,300 Z" fill="{DOSKA2}" {o(7)}/>'
    s += okno_izby(280, 480, 280, 240, t, svet=True, moroz=.3 if k == 3 else 0)
    s += teplo(420, 600, 380, 340, .8)
    # годы летят: листья / снег / травинки вокруг окна
    r = random.Random(4)
    for i in range(22):
        p = ((t * .35) + r.uniform(0, 1)) % 1.0
        x = r.uniform(0, W); y = p * H
        col = ["#8fbf57", "#d78b2a", "#9aa7b2", "#ffffff"][k]
        s += (f'<ellipse cx="{x + 70*A.w(t,4.0,i*.1):.0f}" cy="{y:.0f}" rx="9" ry="5"'
              f' fill="{col}" opacity="{.5+.4*abs(A.w(t,2.0,i*.2)):.2f}"'
              f' transform="rotate({p*360:.0f} {x:.0f} {y:.0f})"/>')
    s += f'<g opacity=".5">{dym(620, 300, t, 4, .2, 280, .35)}</g>'
    s += ulica_dal(900, 1000, 1000, t, False, 30)
    return s


def pech_pekarni(t):
    """Пекарня изнутри ночью: устье печи, стропила, ведро у стены."""
    s = kladka(-20, -20, W + 40, H + 40, 88, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#0f0c10" opacity=".5"/>'
    for i in range(4):
        s += (f'<path d="M{-100+i*260},0 l420,330" stroke="#5a4028" stroke-width="30" opacity=".85"/>')
    s += f'<rect y="950" width="{W}" height="130" fill="#3a2f26"/>'
    s += teplo(360, 700, 520, 440, 1.0)
    s += f'<path d="M140,900 v-230 q220,-170 440,0 v230 Z" fill="{CHUGUN}" {o(8)}/>'
    s += f'<path d="M190,890 v-190 q170,-140 340,0 v190 Z" fill="#160d08" {o(6)}/>'
    s += ugli(230, 870, 260, t, 7)
    s += ogon(360, 872, t, 1.7, 0, 9)
    s += ogon(270, 876, t, .9, .6, 5)
    s += ogon(450, 876, t, .9, 1.3, 5)
    s += iskra_let(t, 360, 700, 12, 7, 620, .55)
    # пламя ползёт по балкам
    for i, (x, y) in enumerate(((180, 230), (470, 320), (720, 180))):
        s += ogon(x, y + 40, t, .5 + .2 * abs(A.w(t, 2.0, i * .3)), i * .4, 3)
    s += f'<g opacity=".4">{dym(400, 320, t, 5, .3, 340, .5, "#8d8a86", 1.4)}</g>'
    s += f'<rect x="690" y="800" width="100" height="120" rx="12" fill="url(#zhel)" {o(6)}/>'
    s += f'<path d="M690,806 q50,-40 100,0" fill="none" stroke="{ZHELEZ}" stroke-width="10"/>'
    s += utvar_pekarni(1000, 950, 860, t, 25)
    s += vinetka(.5)
    return s


def dvor_kolodec_noch(t):
    """Монастырский двор ночью: дверь пекарни, колодец, окна загораются."""
    s = nebo("noch", t, True, 21)
    s += f'<ellipse cx="300" cy="420" rx="700" ry="400" fill="{UGOL}" opacity="{.2+.12*abs(A.w(t,1.4)):.2f}"/>'
    s += f'<rect y="880" width="{W}" height="200" fill="#2a2a33"/>'
    s += kladka(0, 300, 830, 580, 86, "url(#kamen)")
    s += f'<rect x="90" y="560" width="200" height="320" rx="8" fill="#2a1a12" {o(7)}/>'
    s += teplo(190, 740, 240, 260, .9)
    s += ogon(190, 850, t, .7, .2, 4)
    for i, x in enumerate((400, 560, 700)):
        on = A.seg(t, 1.0 + i * .9, .4)
        s += (f'<rect x="{x}" y="500" width="96" height="120" rx="8"'
              f' fill="{SVET if on>.5 else "#2a3550"}" opacity="{.3+.6*on:.2f}" {o(6)}/>')
    s += ten(1020, 1000, 190, 24, .5)
    s += brevna(880, 740, 300, 200, 58)
    s += f'<ellipse cx="1030" cy="748" rx="150" ry="36" fill="#0d1726" {o(6)}/>'
    s += (f'<ellipse cx="1030" cy="{756+4*A.w(t,2.2):.0f}" rx="120" ry="26" fill="url(#voda)" opacity=".9"/>')
    for x in (906, 1140):
        s += f'<rect x="{x}" y="520" width="28" height="230" fill="url(#derev)" {o(5)}/>'
    s += f'<rect x="890" y="498" width="260" height="26" rx="8" fill="url(#derev)" {o(5)}/>'
    s += iskra_let(t, 300, 560, 10, 9, 400, .45)
    s += sneg_letit(t, 12, 11, .4, .5)
    s += ulica_dal(1300, 880, 600, t, True, 35)
    s += vinetka(.5)
    return s


def dve_veschi(t, uzko=False):
    """Полиэкран: слева пустая холстина, справа три яйца. Граница дрожит."""
    XW = 830 if uzko else 830
    hw = XW / 2
    s = f'<rect width="{W}" height="{H}" fill="#14110d"/>'
    # левая половина: пустая холстина
    s += f'<rect x="0" y="0" width="{hw:.0f}" height="{H}" fill="#1b1712"/>'
    s += teplo(hw * .5, 620, 300, 300, .45)
    s += f'<rect x="0" y="700" width="{hw:.0f}" height="380" fill="url(#derev)"/>'
    s += (f'<path d="M30,700 h{hw-60:.0f} l-26,150 h-{hw-112:.0f} Z" fill="url(#rush)" {o(5)}/>')
    s += f'<text x="{hw*.5:.0f}" y="300" text-anchor="middle" font-family="Georgia,serif" font-size="0"> </text>'
    # правая половина: три яйца на холстине
    s += f'<rect x="{hw:.0f}" y="0" width="{hw:.0f}" height="{H}" fill="#221a12"/>'
    s += teplo(hw * 1.5, 600, 320, 320, .7)
    s += f'<rect x="{hw:.0f}" y="700" width="{hw:.0f}" height="380" fill="url(#derev)"/>'
    s += (f'<path d="M{hw+30:.0f},700 h{hw-60:.0f} l-26,150 h-{hw-112:.0f} Z" fill="url(#rush)" {o(5)}/>')
    for i, (dx, dy, r) in enumerate(((-96, 8, 58), (0, 24, 64), (94, 4, 56))):
        x = hw * 1.5 + dx
        y = 640 + dy
        kat = 3.2 * A.w(t, 3.4, i * .35)
        s += ten(x, y + r * .8, r * .9, 14, .45)
        s += (f'<g transform="rotate({kat:.2f} {x:.0f} {y+r*.7:.0f})">'
              f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r*.75:.0f}" ry="{r:.0f}"'
              f' fill="url(#krem)" {o(6)}/>'
              f'<ellipse cx="{x-r*.26:.0f}" cy="{y-r*.3:.0f}" rx="{r*.2:.0f}" ry="{r*.28:.0f}"'
              f' fill="#fffaf0" opacity=".6"/></g>')
    s += svecha(hw * 1.5 + 230, 660, t, .2, 1.0)
    # дрожащая граница
    dx = 5 * A.w(t, 1.7)
    s += (f'<rect x="{hw-6+dx:.1f}" y="0" width="12" height="{H}" fill="#f2e2bc" opacity=".5"/>'
          f'<rect x="{hw-2+dx:.1f}" y="0" width="4" height="{H}" fill="#fff6e0" opacity=".85"/>')
    s += vinetka(.5)
    return s


def kvashnya(t):
    """Утренняя пекарня: квашня, две хлебные лопаты, две тени — одна тает."""
    s = kladka(-20, -20, W + 40, H + 40, 92, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#e8dcc4" opacity=".18"/>'
    s += f'<rect y="930" width="{W}" height="150" fill="#4a3c2e"/>'
    s += luch(560, 0, 260, 1080, t, .26)
    # лопаты на стене
    for i, (x, op) in enumerate(((180, 1.0), (330, .45))):
        s += (f'<g opacity="{op}"><rect x="{x}" y="200" width="56" height="420" rx="12"'
              f' fill="url(#dosk)" {o(6)}/>'
              f'<path d="M{x-30},200 h116 v-90 q-58,-40 -116,0 Z" fill="url(#dosk)" {o(6)}/></g>')
    # квашня
    s += ten(560, 940, 150, 22, .5)
    s += (f'<path d="M430,920 q-30,-200 30,-240 q100,-34 200,0 q60,40 30,240 Z" fill="url(#derev)" {o(7)}/>')
    podem = 10 * A.ease(((t * .3) % 1.0))
    s += (f'<ellipse cx="560" cy="{684-podem:.0f}" rx="{104+podem:.0f}" ry="{36+podem*.6:.0f}"'
          f' fill="url(#krem)" {o(6)}/>')
    # две тени на полу: вторая тает
    s += f'<ellipse cx="300" cy="1000" rx="120" ry="40" fill="#1c1510" opacity=".5"/>'
    s += (f'<ellipse cx="520" cy="1010" rx="120" ry="40" fill="#1c1510"'
          f' opacity="{max(0.0, .45-.4*A.seg(t,1.4,3.0)):.2f}"/>')
    # мука в луче
    r = random.Random(9)
    for i in range(18):
        p = ((t * .08) + r.uniform(0, 1)) % 1.0
        s += (f'<circle cx="{600+r.uniform(-90,180)+26*A.w(t,6+i,i*.2):.0f}" cy="{p*H:.0f}"'
              f' r="{r.uniform(1.8,3.6):.1f}" fill="#fff8e6" opacity=".6"/>')
    s += utvar_pekarni(1020, 930, 840, t, 26)
    return s


def tri_okna(t):
    """Фасад избы ночью: два окна тёплые, третье тёмное. Снег идёт."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 11)
    s += SL(Z_DAL, ulica_dal(900, 700, 1020, t, True, 72))
    s += brevna(-20, 240, 900, 700, 92)
    s += (f'<path d="M-60,250 L420,70 L900,250 Z" fill="#4b3526" {o(8)}/>'
          f'<path d="M-60,250 L420,70 L900,250 Z" fill="url(#sneg)" opacity=".5"/>')
    s += sneg_lezhit(250, 18)
    for i, (x, svet) in enumerate(((70, True), (330, True), (590, False))):
        vid = (f'<rect x="{x}" y="420" width="220" height="250" fill="#f3dca8"/>'
               if svet else f'<rect x="{x}" y="420" width="220" height="250" fill="#1b2330"/>')
        if svet and i == 1:                      # в среднем окне кто-то проходит
            p = (t * .22) % 1.0
            vid += siluet(x + 20 + p * 180, 650, 180, "#6a4a2e", .8)
        s += okno_izby(x, 420, 220, 250, t, vid, moroz=.3, svet=svet)
        if svet:
            s += teplo(x + 110, 545, 300, 240, .5 + .08 * A.w(t, 4.0 + i))
    s += sneg_lezhit(880, 26)
    s += f'<g opacity=".85">{sneg_letit(t, 54, 13, .8, 1.0)}</g>'
    s += SL(Z_PERED, pleten(-40, 860, 1000, 150, 12))
    s += ramka_pp("oba", "#07090f", .5)
    s += vinetka(.5)
    return s


# ─────────────────────── 4. СЕМЬ ЗАПРЕТОВ ───────────────────────
def ambar(t):
    """Двор в инее, амбар с меловыми зарубками на двери, ворота."""
    s = nebo("den", t, False)
    s += oblaka(t, 190, 5, 21, .45, "#e6edf4", 9)
    s += f'<path d="M0,760 Q500,724 960,758 Q1440,790 1920,752 L1920,1080 L0,1080 Z" fill="#b9c6d2" {o(5)}/>'
    s += f'<rect y="800" width="{W}" height="280" fill="#aab8c6"/>'
    s += brevna(70, 300, 720, 500, 86)
    s += f'<path d="M30,300 L430,130 L830,300 Z" fill="{DOSKA2}" {o(8)}/>'
    s += f'<path d="M30,300 L430,130 L830,300 l-40,-30 L430,172 L70,270 Z" fill="url(#sneg)" {o(5)}/>'
    # дверь с зарубками
    s += f'<rect x="250" y="430" width="330" height="370" rx="8" fill="#241a12" {o(8)}/>'
    s += doski(258, 438, 314, 356, 64, True, "derev")
    for i in range(9):
        on = A.seg(t, .4 + i * .22, .4)
        x = 282 + (i % 5) * 54
        y = 500 + (i // 5) * 90
        s += (f'<path d="M{x},{y} l10,70" stroke="#f4efe2" stroke-width="9" stroke-linecap="round"'
          f' opacity="{.25+.7*on:.2f}"/>')
    s += f'<path d="M282,646 l230,0" stroke="#f4efe2" stroke-width="9" opacity=".8"/>'
    # ворота справа, покачиваются
    ang = 2.2 * A.w(t, 6.0)
    s += (f'<g transform="rotate({ang:.2f} 900 400)">'
          f'{doski(900, 400, 250, 400, 60, True, "derev")}'
          f'<rect x="900" y="400" width="250" height="400" fill="none" {o(7)}/></g>')
    s += f'<g opacity=".55">{sneg_letit(t, 18, 23, .6, .5)}</g>'
    # иней искрит
    r = random.Random(14)
    for i in range(22):
        x, y = r.uniform(0, W), r.uniform(760, 1050)
        s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#ffffff"'
              f' opacity="{.2+.8*abs(A.w(t,1.4+r.uniform(0,2),i*.1)):.2f}"/>')
    s += ulica_dal(900, 800, 1000, t, True, 37)
    s += vinetka(.34)
    return s


def pleten_sosed(t, zakat=True):
    """Плетень между дворами на закате; вдали обгоревшая стена сарая."""
    s = nebo("zakat", t, False) if zakat else nebo("sumer", t, True, 31)
    s += oblaka(t, 230, 4, 17, .42, "#f0c9a0", 8)
    s += f'<ellipse cx="300" cy="640" rx="190" ry="190" fill="#ffd9a0" opacity=".55"/>'
    s += f'<path d="M0,720 Q480,690 960,718 Q1440,744 1920,712 L1920,1080 L0,1080 Z" fill="#6a6a4e" {o(5)}/>'
    # обгоревший сарай вдали
    s += f'<rect x="1180" y="560" width="300" height="160" fill="#3b332c" {o(5)}/>'
    s += f'<path d="M1160,560 L1330,470 L1500,560 Z" fill="#2c261f" {o(5)}/>'
    s += f'<g opacity=".4">{dym(1330, 470, t, 4, .14, 300, .36, "#8c8880", 1.1)}</g>'
    s += pleten(60, 800, 720, 230, 11)
    # горшки на кольях
    for i, x in enumerate((180, 420, 660)):
        kach = 2.0 * A.w(t, 4.0, i * .3)
        s += (f'<g transform="rotate({kach:.2f} {x} 580)">'
              f'{krynka(x, 594, .9, "url(#glina)")}</g>')
    s += ten(420, 1010, 300, 26, .4)
    s += f'<g opacity=".7">{tuman(t, 940, .3, "#d8d0bc")}</g>'
    # воробьи прыгают по жерди
    for i, x in enumerate((300, 520)):
        s += ptica(x, 672 - 8 * abs(A.w(t, 1.6, i * .4)), t, .6, "#8a7f6e", i * .3, "#6b6356")
    s += ramka_pp("levo", "#2b2418", .4)
    s += ulica_dal(860, 720, 1060, t, False, 52)
    s += vinetka(.4)
    return s


def ploshchadka(t):
    """Лестничная площадка: у двери соседки оставлен пакет с лекарством."""
    s = f'<rect width="{W}" height="{H}" fill="#55606a"/>'
    s += kladka(-20, -20, W + 40, H + 40, 96, "#6d7781")
    s += f'<rect width="{W}" height="{H}" fill="#2b333c" opacity=".46"/>'
    s += doski(-20, 880, W + 40, 220, 150, False, "beton")
    s += f'<rect y="872" width="{W}" height="16" fill="#49535d"/>'
    # дверь с номером и глазком
    s += f'<rect x="150" y="190" width="420" height="700" rx="8" fill="#6f4a33" {o(8)}/>'
    s += (f'<rect x="178" y="220" width="364" height="300" rx="6" fill="none"'
          f' stroke="#4e3122" stroke-width="10"/>'
          f'<rect x="178" y="560" width="364" height="300" rx="6" fill="none"'
          f' stroke="#4e3122" stroke-width="10"/>')
    s += (f'<circle cx="360" cy="540" r="14" fill="#1d2228" {o(4)}/>')
    # в глазке мелькает тень
    if A.blink(t, 7.0, .2, .5):
        s += f'<circle cx="360" cy="540" r="9" fill="#d8c08a" opacity=".8"/>'
    s += (f'<text x="520" y="268" text-anchor="end" font-family="Georgia,serif"'
          f' font-size="62" font-weight="bold" fill="#e8d7ae" stroke="#2a1c12"'
          f' stroke-width="6" paint-order="stroke">14</text>')
    s += f'<circle cx="534" cy="560" r="13" fill="url(#zhel)" {o(4)}/>'
    # пакет с лекарством у порога: шевелится от сквозняка
    kach = 2.4 * A.w(t, 3.0)
    s += ten(400, 886, 110, 18, .5)
    s += (f'<g transform="rotate({kach:.2f} 400 760)">'
          f'<path d="M318,760 h164 l-18,126 h-128 Z" fill="#e8e2d2" {o(6)}/>'
          f'<path d="M340,760 q60,-54 120,0" fill="none" stroke="#cfc6b2" stroke-width="9"/>'
          f'<rect x="352" y="800" width="96" height="58" rx="8" fill="#ffffff" {o(4)}/>'
          f'<path d="M400,812 v34 M383,829 h34" stroke="{KRAS}" stroke-width="10"/></g>')
    # лампочка мигает, тени от перил
    mig = 1.0 if not A.blink(t, 4.2, .1, .18) else .3
    s += (f'<path d="M980,0 v150" stroke="#39434d" stroke-width="7"/>'
          f'<circle cx="980" cy="176" r="34" fill="#fff0c0" opacity="{mig:.2f}" {o(4)}/>')
    s += teplo(980, 200, 620, 520, .4 * mig)
    s += (f'<path d="M1240,890 v-360 M1420,890 v-360 M1600,890 v-360" stroke="#5a646e"'
          f' stroke-width="14"/>'
          f'<path d="M1180,520 h620" stroke="#6f7a84" stroke-width="20"/>')
    s += f'<g opacity=".3">{par(1300, 880, t, 4, .3, 300, .2, 2.0)}</g>'
    s += ramka_pp("pravo", "#13181d", .5)
    s += vinetka(.5)
    return s


def yarmarka(t):
    """Вечерние посиделки: фонарь, гармонь, силуэты парами у плетня."""
    s = nebo("noch", t, True, 113)
    s += SL(Z_DAL, ulica_dal(1000, 680, 920, t, True, 114))
    s += sneg_lezhit(700, 18)
    s += pleten(-40, 700, 1960, 170, 22)
    # фонарь на шесте качается, от него круг света
    kach = 3.6 * A.w(t, 3.0)
    s += f'<rect x="420" y="200" width="24" height="700" rx="10" fill="url(#derev)" {o(6)}/>'
    s += (f'<g transform="rotate({kach:.2f} 432 230)">'
          f'<path d="M432,230 h150" stroke="{K}" stroke-width="7"/>'
          f'<rect x="548" y="240" width="90" height="110" rx="10" fill="url(#zhel)"'
          f' opacity=".9" {o(6)}/>'
          f'<rect x="562" y="254" width="62" height="82" fill="#ffe9b0" opacity=".95"/>'
          f'{ogon(593, 330, t, .7, .2, 4)}</g>')
    s += teplo(593, 420, 620, 520, .55 + .06 * A.w(t, 3.0))
    # силуэты парами, покачиваются в такт
    for i, (x, h_, ph) in enumerate(((200, 330, .0), (268, 316, .12),
                                     (720, 340, .4), (790, 322, .52),
                                     (1130, 330, .7), (1198, 318, .82))):
        kach2 = 2.6 * A.w(t, 2.2, ph)
        s += (f'<g transform="rotate({kach2:.2f} {x} 900)">'
              f'{siluet(x, 900, h_, "#1b1f27", .96, i % 2 == 1, "#d8a96a")}</g>')
    # гармонист: меха раскрываются и сходятся
    rast = 36 * (.5 + .5 * A.w(t, 1.6))
    s += siluet(470, 900, 346, "#171b22", .97, False, "#d8a96a")
    s += (f'<rect x="{418-rast*.5:.0f}" y="660" width="{40+rast:.0f}" height="110" rx="10"'
          f' fill="url(#tkan)" {o(6)}/>')
    for i in range(6):
        s += (f'<line x1="{422-rast*.5+i*(36+rast)/6:.0f}" y1="664"'
              f' x2="{422-rast*.5+i*(36+rast)/6:.0f}" y2="766" stroke="#f2d9b0"'
              f' stroke-width="3" opacity=".6"/>')
    s += (f'<rect x="{396-rast*.5:.0f}" y="652" width="26" height="126" rx="8"'
          f' fill="url(#derev)" {o(5)}/>'
          f'<rect x="{454+rast*.5:.0f}" y="652" width="26" height="126" rx="8"'
          f' fill="url(#derev)" {o(5)}/>')
    # искры из костерка и снег
    s += ugli(880, 920, 180, t, 7, 115)
    s += ogon(970, 912, t, 1.0, .4, 6)
    s += iskra_let(t, 970, 880, 14, 117, 420, .5)
    s += f'<g opacity=".7">{sneg_letit(t, 34, 119, .6, .8)}</g>'
    s += ramka_pp("oba", "#080a10", .5)
    s += vinetka(.48)
    return s


def izba_den(t):
    """Изба днём: на столе травяной сбор лекарей, миска, холстина, пучки трав."""
    s = brevna(-20, -20, W + 40, H + 40, 104)
    s += polovicy(860)
    s += luch(420, -30, 520, 900, t, .22)
    s += teplo(430, 430, 520, 430, .5)
    # пучки трав на жерди: качаются от сквозняка
    s += f'<line x1="60" y1="150" x2="820" y2="132" stroke="{K}" stroke-width="7"/>'
    for i, x in enumerate((140, 300, 470, 640)):
        kach = 2.6 * A.w(t, 3.4 + i * .5, i * .27)
        s += (f'<g transform="rotate({kach:.2f} {x} 142)">'
              f'<path d="M{x-34},142 q34,170 0,250 q-34,-80 0,-250 Z" fill="{ZEL}" {o(5)}/>'
              f'<path d="M{x+6},142 q40,150 10,230 q-40,-80 -10,-230 Z" fill="{TRAVA}" {o(5)}/>'
              f'<rect x="{x-14}" y="134" width="28" height="26" rx="8" fill="url(#rush)" {o(4)}/></g>')
    s += stol(170, 700, 560)
    s += (f'<path d="M190,696 q280,-44 560,0 l-30,40 h-500 Z" fill="url(#rush)" {o(5)}/>')
    # миска с настоем: пар и круги по поверхности
    s += ten(360, 712, 110, 16, .4)
    s += (f'<path d="M258,636 h206 q-16,74 -103,74 q-87,0 -103,-74 Z" fill="url(#glina)" {o(7)}/>'
          f'<ellipse cx="361" cy="638" rx="104" ry="20" fill="#5c7a4a" {o(5)}/>')
    r_ = 20 + 26 * ((t * .5) % 1.0)
    s += (f'<ellipse cx="361" cy="638" rx="{r_:.0f}" ry="{r_*.2:.0f}" fill="none"'
          f' stroke="#cfe3bb" stroke-width="4" opacity="{.5*(1-(t*.5)%1.0):.2f}"/>')
    s += f'<g opacity=".55">{par(361, 620, t, 4, .5, 230, .3)}</g>'
    # рассыпанный сбор и ступка
    for i, (x, y) in enumerate(((520, 690), (570, 700), (610, 686), (650, 698))):
        s += (f'<path d="M{x},{y} q18,-22 36,-4 q-14,20 -36,4 Z" fill="{ZEL2}" {o(4)}/>')
    s += (f'<path d="M688,636 h92 q-8,60 -46,60 q-38,0 -46,-60 Z" fill="url(#chug)" {o(6)}/>'
          f'<rect x="{728}" y="{588}" width="16" height="60" rx="7" fill="url(#derev)"'
          f' transform="rotate(16 736 618)" {o(4)}/>')
    s += utvar_izby(1080, 520, 760, t, 63)
    s += mebel_hlam(1420, 940, 500, t, 64)
    s += ramka_pp("levo", "#0f0c08", .42)
    s += vinetka(.44)
    return s


def gorod_korobka(t):
    """Комната в квартире: большая коробка с бантом, кресло, плита с чайником."""
    s = f'<rect width="{W}" height="{H}" fill="#b9ad9a"/>'
    for c in range(12):
        s += f'<rect x="{c*160}" width="150" height="{H}" fill="#c6baa6" opacity="{.4 if c%2 else .15}"/>'
    s += f'<rect y="880" width="{W}" height="200" fill="url(#pol)" {o(5)}/>'
    s += f'<rect y="846" width="{W}" height="40" fill="{POL2}" {o(4)}/>'
    s += teplo(420, 500, 620, 520, .5)
    # коробка с бантом крупно
    s += ten(400, 900, 260, 26, .5)
    s += f'<rect x="150" y="470" width="500" height="410" rx="12" fill="url(#med)" {o(9)}/>'
    s += f'<rect x="150" y="470" width="500" height="80" rx="10" fill="{ZOL}" opacity=".5" {o(6)}/>'
    s += f'<rect x="368" y="470" width="64" height="410" fill="{TKAN}" opacity=".9" {o(5)}/>'
    s += f'<rect x="150" y="620" width="500" height="58" fill="{TKAN}" opacity=".9" {o(5)}/>'
    kach = 3.0 * A.w(t, 4.0)
    s += (f'<g transform="rotate({kach:.2f} 400 470)">'
          f'<path d="M400,470 q-120,-96 -36,-130 q70,-18 36,130 Z" fill="{TKAN}" {o(7)}/>'
          f'<path d="M400,470 q120,-96 36,-130 q-70,-18 -36,130 Z" fill="{TKAN}" {o(7)}/>'
          f'<circle cx="400" cy="462" r="24" fill="#8c2026" {o(5)}/></g>')
    # кресло
    s += ten(930, 920, 150, 22, .45)
    s += f'<rect x="800" y="640" width="280" height="270" rx="26" fill="{TKAN2}" {o(8)}/>'
    s += f'<rect x="786" y="560" width="308" height="130" rx="30" fill="#4a6b8c" {o(8)}/>'
    # календарь без чисел
    s += f'<rect x="1200" y="260" width="220" height="280" rx="10" fill="url(#list)" {o(7)}/>'
    for r_ in range(5):
        for c in range(5):
            s += f'<rect x="{1222+c*38}" y="{330+r_*44}" width="28" height="30" rx="4" fill="#cfc2a4" opacity=".7"/>'
    # чайник на плите свистит
    s += f'<rect x="1540" y="700" width="300" height="210" rx="10" fill="{ZHELEZ}" {o(7)}/>'
    s += f'<ellipse cx="1660" cy="704" rx="70" ry="18" fill="#3c4047" {o(5)}/>'
    s += (f'<path d="M1600,700 q-16,-110 60,-126 q76,16 60,126 Z" fill="url(#zhel)" {o(6)}/>')
    s += f'<g opacity=".6">{par(1676, 570, t, 4, .55, 260, .6, 1.0)}</g>'
    s += kvartira_veschi(700, 880, 760, t, 59)
    s += vinetka(.38)
    return s


def led_rassvet(t):
    """Река на рассвете: у берега встаёт первый лёд — кованая полоса."""
    s = nebo("rassv", t, False, 103)
    s += f'<g opacity=".65">{oblaka(t, 150, 5, 107, .5, "#e8dfd2", 19.0)}</g>'
    s += (f'<path d="M-20,520 q500,-60 1000,-20 q500,40 960,-24 L{W},640 H-20 Z"'
          f' fill="#4e5a48" opacity=".8"/>')
    s += SL(Z_DAL, ulica_dal(1180, 560, 740, t, True, 108))
    # вода
    s += f'<rect y="600" width="{W}" height="480" fill="url(#voda)"/>'
    for i in range(9):
        p = ((t * .14 + i * .11) % 1.0)
        s += (f'<path d="M{-100+p*2100:.0f},{640+i*44} h200" stroke="#9fd0de"'
              f' stroke-width="5" opacity="{.3*(1-abs(.5-p)*1.4):.2f}"/>')
    # лёд у берега: растёт к середине, кромка зубчатая и блестит
    rost = .62 + .38 * A.ease(A.seg(t, .4, 6.0))
    kr = 1080 - 380 * rost
    puti = f'M-20,1080 L-20,{kr+60:.0f} '
    for i in range(21):
        x = -20 + i * 98
        y = kr + 30 * math.sin(i * 1.3 + t * .4) + (14 if i % 2 else -10)
        puti += f'L{x},{y:.0f} '
    puti += f'L{W+20},{kr+50:.0f} L{W+20},1080 Z'
    s += f'<path d="{puti}" fill="url(#led)" opacity=".95" {o(5)}/>'
    for i in range(7):
        s += (f'<path d="M{60+i*280},{kr+120+i*14:.0f} q140,-40 280,10" fill="none"'
              f' stroke="#ffffff" stroke-width="5" opacity=".35"/>')
    bl = (t * .18) % 1.0
    s += (f'<rect x="{-400+bl*2600:.0f}" y="{kr+40:.0f}" width="280" height="{1080-kr:.0f}"'
          f' fill="#ffffff" opacity=".12" transform="skewX(-22)"/>')
    # пар над открытой водой и камыш первым планом
    s += f'<g opacity=".5">{par(900, 640, t, 6, .45, 420, .22, 2.4)}</g>'
    s += f'<g opacity=".4">{tuman(t, 620, .4, "#dfe9f0")}</g>'
    for i, x in enumerate((60, 150, 240, 1700, 1810)):
        kl = 8 * A.w(t, 3.4, i * .2)
        s += (f'<path d="M{x},1080 q{kl:.1f},-180 {kl*2:.1f},-330" fill="none" stroke="#8a7a4e"'
              f' stroke-width="8"/>'
              f'<path d="M{x+kl*2:.1f},740 q22,-40 0,-80 q-22,40 0,80 Z" fill="#6b5a36" {o(3)}/>')
    s += ptica(1500, 700, t, .9, "#4a5560", .3)
    s += ramka_pp("oba", "#1b2026", .36)
    s += vinetka(.42)
    return s


def pod_lunkoy(t):
    """Разрез: лёд и лунка сверху, зелёная вода и рыба внизу."""
    s = f'<rect width="{W}" height="{H}" fill="url(#voda)"/>'
    s += f'<rect width="{W}" height="300" fill="url(#led)"/>'
    s += f'<rect y="290" width="{W}" height="26" fill="#cfe6f2" {o(4)}/>'
    for i in range(10):
        s += f'<path d="M{i*200},0 l70,290" stroke="#ffffff" stroke-width="5" opacity=".3"/>'
    s += f'<rect x="290" y="0" width="230" height="300" fill="{VODA2}" {o(6)}/>'
    s += (f'<ellipse cx="405" cy="{300+6*A.w(t,2.4):.0f}" rx="{116+6*A.w(t,2.0):.0f}" ry="30"'
          f' fill="#2a7a88" opacity=".95"/>')
    # лучи света в воде
    for i in range(4):
        s += (f'<path d="M{330+i*44},316 l{60+i*20},620 l70,0 l{-60-i*20},-620 Z" fill="#9fe0d8"'
              f' opacity="{.08+.05*abs(A.w(t,5+i,i*.2)):.2f}"/>')
    # сеть пустая
    s += f'<path d="M360,316 v420" stroke="{KREM}" stroke-width="6" opacity=".85"/>'
    for r_ in range(7):
        s += (f'<path d="M{300-r_*6},{740+r_*34} q{60+r_*6},{44},{120+r_*12},0" fill="none"'
              f' stroke="{KREM}" stroke-width="4" stroke-dasharray="12 14" opacity=".8"/>')
    # рыба проплывает
    for i, (y, sp, sc) in enumerate(((560, .16, 1.0), (760, .11, 1.4), (900, .2, .7))):
        p = ((t * sp) + i * .33) % 1.2 - .1
        x = p * W
        hv = 14 * A.w(t, .7, i * .3)
        s += (f'<g transform="translate({x:.0f},{y}) scale({sc:.2f})">'
              f'<ellipse cx="0" cy="0" rx="92" ry="38" fill="#4e8a6e" {o(5)}/>'
              f'<g transform="rotate({hv:.1f} -86 0)">'
              f'<path d="M-86,0 l-70,-44 l0,88 Z" fill="#3c6f58" {o(5)}/></g>'
              f'<circle cx="56" cy="-10" r="9" fill="#f4efe2" {o(3)}/>'
              f'<circle cx="58" cy="-10" r="4" fill="{K}"/>'
              f'<path d="M-20,-34 q30,-26 60,-4" fill="none" stroke="#3c6f58" stroke-width="10"/></g>')
    # пузырьки
    r = random.Random(17)
    for i in range(14):
        p = ((t * .25) + r.uniform(0, 1)) % 1.0
        s += (f'<circle cx="{r.uniform(0,W):.0f}" cy="{1080-p*760:.0f}" r="{r.uniform(4,10):.0f}"'
              f' fill="#cfeef0" opacity="{(1-p)*.5:.2f}"/>')
    s += vinetka(.4)
    return s


def panelka_razrez(t):
    """Вечерний панельный дом в разрезе: на каждом этаже своя комната."""
    s = nebo("noch", t, True, 44)
    s += panelka(1120, 1080, 720, t, 6, True, 9)
    s += f'<rect y="1000" width="{W}" height="80" fill="#2a3040"/>'
    s += ten(440, 1006, 420, 24, .5)
    s += f'<rect x="60" y="180" width="760" height="820" fill="url(#beton)" {o(8)}/>'
    for e in range(4):
        y = 180 + e * 205
        s += f'<rect x="76" y="{y}" width="728" height="16" fill="{BETON2}" {o(4)}/>'
        for c in range(2):
            x = 96 + c * 364
            on = abs(A.w(t, 6.0 + e * 1.3 + c * .7)) > .25
            s += (f'<rect x="{x}" y="{y+22}" width="340" height="168" rx="6"'
                  f' fill="{"#3a2f28" if on else "#20232c"}" {o(5)}/>')
            if on:
                s += teplo(x + 170, y + 110, 210, 130, .85)
                s += f'<rect x="{x+40}" y="{y+120}" width="120" height="68" rx="8" fill="{TKAN2}" {o(4)}/>'
                s += f'<rect x="{x+200}" y="{y+60}" width="110" height="128" rx="8" fill="url(#derev)" {o(4)}/>'
                s += f'<circle cx="{x+170}" cy="{y+52}" r="18" fill="{SVET}" opacity="{.6+.4*abs(A.w(t,3.0,e*.2)):.2f}"/>'
    s += sneg_letit(t, 20, 47, .5, .6)
    s += ulica_dal(60, 1000, 640, t, True, 71)
    s += vinetka(.44)
    return s


def izba_pech_tishina(t):
    """Изба с печью и лежанкой: кот, дверь, верстак. Самая тихая декорация."""
    s = brevna(-20, -20, W + 40, H + 40, 116)
    s += f'<rect width="{W}" height="{H}" fill="#1f2430" opacity=".4"/>'
    s += polovicy(900)
    s += pech(70, 260, 440, 640, t, True, True)
    s += teplo(290, 700, 520, 440, .8)
    s += kot(560, 960, t, .95, "#3b3430", spit=True)
    s += f'<rect x="700" y="760" width="300" height="30" rx="8" fill="url(#derev)" {o(6)}/>'
    s += f'<rect x="724" y="790" width="26" height="150" fill="url(#derev)" {o(5)}/>'
    s += f'<rect x="950" y="790" width="26" height="150" fill="url(#derev)" {o(5)}/>'
    for i, x in enumerate((760, 830, 900)):
        s += f'<rect x="{x}" y="716" width="18" height="44" rx="5" fill="url(#zhel)" {o(4)}/>'
    s += dver(1120, 240, 300, 660, 0, "url(#derev)", kruchok=True)
    s += lampa(640, 480, t, .8)
    s += utvar_izby(1480, 620, 420, t, 13)
    s += vinetka(.42)
    return s


def kvartira_shum(t):
    """Кухня в квартире: две чашки на столе, телефон экраном вниз, часы."""
    s = f'<rect width="{W}" height="{H}" fill="#d8cdbb"/>'
    s += f'<rect width="{W}" height="700" fill="#cdbfa8"/>'
    for i in range(14):
        s += (f'<line x1="{i*140}" y1="0" x2="{i*140}" y2="700" stroke="#bda98c"'
              f' stroke-width="4" opacity=".5"/>')
    s += doski(-20, 700, W + 40, 400, 140, False, "dosk")
    s += f'<rect y="690" width="{W}" height="16" fill="#8a6f4c"/>'
    s += kvartira_veschi(1180, 700, 740, t, 94)
    s += teplo(420, 520, 460, 380, .45)
    # кухонный стол
    s += ten(400, 940, 330, 26, .5)
    s += f'<rect x="90" y="640" width="640" height="40" rx="10" fill="#e8dcc6" {o(7)}/>'
    for x in (130, 650):
        s += f'<rect x="{x}" y="680" width="34" height="260" fill="#c8b393" {o(6)}/>'
    # две чашки, пар редкий — остыли
    for i, x in enumerate((260, 560)):
        s += ten(x, 648, 54, 10, .35)
        s += (f'<path d="M{x-46},540 h92 l-10,100 h-72 Z" fill="#ffffff" {o(6)}/>'
              f'<path d="M{x+46},566 q40,30 0,58" fill="none" stroke="{K}" stroke-width="19"/>'
              f'<path d="M{x+46},566 q40,30 0,58" fill="none" stroke="#ffffff" stroke-width="11"/>'
              f'<ellipse cx="{x}" cy="540" rx="46" ry="13" fill="#6b4a32" {o(4)}/>')
        s += f'<g opacity=".22">{par(x, 528, t, 3, .3, 120, .22)}</g>'
    # телефон экраном вниз: в щель пробивается свет уведомления
    mig = 1.0 if A.blink(t, 6.0, .1, .9) else .0
    s += (f'<rect x="380" y="612" width="150" height="26" rx="7" fill="#22262c" {o(5)}/>'
          f'<rect x="386" y="636" width="138" height="6" rx="3" fill="{SVET}"'
          f' opacity="{.55*mig:.2f}"/>')
    s += teplo(455, 644, 180, 60, .25 * mig)
    # часы: маятник ходит
    s += hodiki(830, 230, t, 1.15)
    s += f'<g opacity=".3">{luch(120, 0, 420, 900, t, .22)}</g>'
    s += ramka_pp("levo", "#2a2318", .34)
    s += vinetka(.4)
    return s


def doroga(t):
    """Подмёрзшая дорога под снегопадом: следы заметает на глазах."""
    s = nebo("sumer", t, False, 133)
    s += SL(Z_DAL, ulica_dal(60, 600, 1800, t, True, 134))
    s += f'<g opacity=".45">{tuman(t, 620, .4, "#cfdae6")}</g>'
    s += f'<rect y="640" width="{W}" height="440" fill="#c9d6e4"/>'
    # колея сходится к горизонту
    for sgn, x0 in ((-1, 760), (1, 1160)):
        s += (f'<path d="M{x0},648 L{x0+sgn*700},1080 L{x0+sgn*940},1080 L{x0+sgn*74},648 Z"'
              f' fill="#93a6ba" opacity=".9"/>'
              f'<path d="M{x0+sgn*20},648 L{x0+sgn*760},1080" fill="none" stroke="#7d90a6"'
              f' stroke-width="9" opacity=".8"/>')
    # вехи вдоль обочины уходят к горизонту
    for i in range(7):
        x = 300 - i * 34
        y = 1040 - i * 56
        h_ = 230 - i * 30
        s += (f'<rect x="{x}" y="{y-h_}" width="{max(6,16-i*2)}" height="{h_}" rx="5"'
              f' fill="#5f4a32" {o(4)}/>'
              f'<path d="M{x-6},{y-h_} h{max(14,28-i*3)}" stroke="#e8e2d2"'
              f' stroke-width="{max(5,12-i)}"/>')
        x2 = 1620 + i * 34
        s += (f'<rect x="{x2}" y="{y-h_}" width="{max(6,16-i*2)}" height="{h_}" rx="5"'
              f' fill="#5f4a32" {o(4)}/>')
    s += (f'<path d="M-20,1080 q480,-120 980,-80 q500,40 960,70 L{W},1080 Z"'
          f' fill="url(#sneg)" opacity=".5"/>')
    # следы: чем старше, тем сильнее заметены
    for i in range(7):
        zan = A.clamp((t * .22 + i * .14) % 1.0)
        x = 820 + (i % 2) * 150 - i * 36
        y = 700 + i * 54
        s += (f'<ellipse cx="{x}" cy="{y}" rx="{34-i*2}" ry="{14-i*.8:.0f}"'
              f' fill="#8ea0b4" opacity="{.55*(1-zan):.2f}"/>')
        s += (f'<ellipse cx="{x+54}" cy="{y+26}" rx="{32-i*2}" ry="{13-i*.8:.0f}"'
              f' fill="#8ea0b4" opacity="{.5*(1-zan):.2f}"/>')
    # позёмка течёт поперёк дороги
    for i in range(10):
        p = ((t * .35 + i * .1) % 1.0)
        s += (f'<path d="M{-200+p*2300:.0f},{700+i*40} q160,{-14 if i%2 else 14} 320,0"'
              f' fill="none" stroke="#ffffff" stroke-width="7" opacity="{.3*(1-abs(.5-p)*1.6):.2f}"/>')
    s += f'<g opacity=".95">{sneg_letit(t, 72, 137, .9, 1.25)}</g>'
    # верстовой столб и ветка первым планом
    s += ten(760, 1020, 90, 18, .4)
    s += (f'<rect x="716" y="420" width="56" height="600" rx="14" fill="url(#derev)" {o(7)}/>')
    for i in range(5):
        s += (f'<rect x="716" y="{440+i*120}" width="56" height="60" fill="#e8e2d2"'
              f' opacity=".9"/>')
    s += (f'<path d="M700,406 h88 l-14,-40 h-60 Z" fill="url(#sneg)" {o(5)}/>')
    s += sneg_lezhit(934, 16)
    s += SL(Z_PERED, f'<path d="M1960,120 q-300,120 -520,90 q220,60 520,30 Z"'
                     f' fill="#3f352c" opacity=".9"/>')
    s += ramka_pp("oba", "#0e131a", .44)
    s += vinetka(.46)
    return s


def kalitka_zasov(t):
    """Дверь мастерской на засове, рядом лопата. Снег, подкова на петле."""
    s = nebo("sumer", t, False, 81)
    s += kladka(-20, 120, 980, 840, 82, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#1d2430" opacity=".3"/>'
    s += SL(Z_DAL, ulica_dal(1080, 740, 840, t, True, 97))
    # дверь
    s += f'<rect x="170" y="300" width="470" height="640" rx="8" fill="url(#derev)" {o(8)}/>'
    s += doski(178, 308, 454, 626, 92, True, "dosk")
    # кованый засов поперёк, пробой и накладка
    s += (f'<rect x="150" y="600" width="520" height="44" rx="14" fill="url(#chug)" {o(7)}/>'
          f'<rect x="196" y="586" width="56" height="72" rx="10" fill="url(#zhel)" {o(5)}/>'
          f'<rect x="560" y="586" width="56" height="72" rx="10" fill="url(#zhel)" {o(5)}/>')
    bl = .3 + .7 * abs(A.w(t, 3.4))
    s += (f'<rect x="170" y="606" width="480" height="10" rx="5" fill="#e8e2d2"'
          f' opacity="{.28*bl:.2f}"/>')
    # подкова на петле качается
    kach = 3.4 * A.w(t, 2.8)
    s += (f'<g transform="rotate({kach:.2f} 404 360)">'
          f'<path d="M352,440 a54,54 0 1 1 104,0 l-28,0 a30,30 0 1 0 -48,0 Z"'
          f' fill="url(#zhel)" {o(6)}/></g>')
    # лопата прислонена
    s += (f'<g transform="rotate(-12 760 940)">'
          f'<rect x="748" y="420" width="24" height="520" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<path d="M716,920 h88 l-10,96 h-68 Z" fill="url(#zhel)" {o(6)}/>'
          f'<rect x="736" y="400" width="48" height="26" rx="10" fill="url(#derev)" {o(4)}/></g>')
    s += sneg_lezhit(940, 22)
    s += f'<g opacity=".8">{sneg_letit(t, 42, 83, .75, .9)}</g>'
    s += ptica(900, 520, t, .8, "#4a5560", .4)
    s += teplo(420, 760, 420, 280, .3)
    s += ramka_pp("oba", "#0a0d13", .48)
    s += vinetka(.48)
    return s


def dver_cepochka(t):
    """Очень крупно дверная цепочка, дверь приоткрыта на ладонь, подъезд за ней."""
    s = f'<rect width="{W}" height="{H}" fill="#4a4036"/>'
    s += doski(0, 0, 820, H, 190, True, "derev")
    s += f'<rect x="820" width="200" height="{H}" fill="#1a1d22"/>'
    s += f'<rect x="1020" width="900" height="{H}" fill="#56606a"/>'
    for c in range(6):
        s += f'<rect x="{1020+c*150}" width="140" height="{H}" fill="#616c76" opacity="{.4 if c%2 else .15}"/>'
    s += f'<ellipse cx="1180" cy="300" rx="260" ry="200" fill="{SVET}" opacity=".18"/>'
    # цепочка крупно, качается
    ang = 3.4 * A.w(t, 2.6)
    s += f'<rect x="690" y="420" width="90" height="130" rx="14" fill="url(#zhel)" {o(8)}/>'
    s += f'<circle cx="735" cy="470" r="22" fill="{ZHELEZ}" {o(5)}/>'
    s += (f'<g transform="rotate({ang:.2f} 735 500)">')
    for i in range(9):
        s += (f'<ellipse cx="{760+i*46}" cy="{520+i*8}" rx="30" ry="18" fill="none"'
              f' stroke="url(#zhel)" stroke-width="13"/>')
    s += f'<rect x="1170" y="564" width="80" height="54" rx="10" fill="url(#zhel)" {o(6)}/></g>'
    s += ten(760, 1020, 300, 24, .4)
    s += ramka_pp("levo", "#1c1812", .55)
    s += kvartira_veschi(1300, 1000, 600, t, 66)
    s += vinetka(.46)
    return s


def ekran_telefona(t):
    """Телефон на вязаной салфетке крупно, рядом сберкнижка."""
    s = f'<rect width="{W}" height="{H}" fill="#8a7f72"/>'
    s += f'<rect y="300" width="{W}" height="780" fill="url(#derev)" {o(6)}/>'
    s += teplo(460, 560, 620, 520, .6)
    # салфетка
    s += f'<ellipse cx="470" cy="760" rx="420" ry="220" fill="url(#rush)" {o(7)}/>'
    for i in range(26):
        a = i * math.pi / 13
        s += (f'<ellipse cx="{470+math.cos(a)*420:.0f}" cy="{760+math.sin(a)*220:.0f}"'
              f' rx="26" ry="16" fill="url(#rush)" {o(4)}/>')
    # телефон вибрирует
    dx = 6 * A.w(t, .9); dy = 3 * A.w(t, 1.3)
    s += (f'<g transform="translate({dx:.1f},{dy:.1f})">'
          f'{ten(470, 940, 170, 20, .45)}'
          f'<rect x="300" y="470" width="340" height="470" rx="40" fill="{CHUGUN}" {o(9)}/>'
          f'<rect x="322" y="500" width="296" height="410" rx="22" fill="#1b2430"/>')
    zv = abs(A.w(t, 1.0)) > .2
    if zv:
        s += f'<rect x="322" y="500" width="296" height="410" rx="22" fill="#2a4a6a" opacity=".9"/>'
        s += f'<circle cx="400" cy="830" r="44" fill="#3fa05a" {o(5)}/>'
        s += f'<circle cx="546" cy="830" r="44" fill="{KRAS}" {o(5)}/>'
    s += "</g>"
    for i in range(3):
        rr = 190 + i * 80 + 30 * abs(A.w(t, 1.0, i * .2))
        s += (f'<circle cx="470" cy="700" r="{rr:.0f}" fill="none" stroke="{SVET}"'
              f' stroke-width="5" opacity="{.3*(1-i*.3)*abs(A.w(t,1.0,i*.2)):.2f}"/>')
    # сберкнижка
    s += ten(1120, 960, 190, 18, .4)
    s += f'<rect x="920" y="700" width="420" height="260" rx="12" fill="{TKAN2}" {o(8)}/>'
    s += f'<rect x="960" y="760" width="250" height="20" rx="6" fill="{ZOL}" opacity=".8"/>'
    s += f'<rect x="960" y="810" width="190" height="14" rx="6" fill="#cfd8e2" opacity=".7"/>'
    s += kvartira_veschi(1480, 300, 420, t, 65)
    s += vinetka(.44)
    return s


def svecha_okno(t):
    """Ночной подоконник: свеча догорает, ходики, луна за окном."""
    s = f'<rect width="{W}" height="{H}" fill="#121a2c"/>'
    s += brevna(-20, -20, W + 40, H + 40, 118)
    s += f'<rect width="{W}" height="{H}" fill="#101828" opacity=".66"/>'
    vid = (f'<rect x="820" y="140" width="700" height="620" fill="#16233e"/>'
           + f'<circle cx="1280" cy="330" r="110" fill="#f6ecd0" opacity=".9"/>'
           + f'<circle cx="1240" cy="306" r="22" fill="#e4dcc0" opacity=".5"/>'
           + _sneg_lezhit(640, 14, "#2b3550"))
    s += okno_izby(820, 140, 700, 620, t, vid=vid, moroz=.4)
    s += f'<rect x="760" y="760" width="840" height="46" rx="10" fill="url(#derev)" {o(7)}/>'
    dogor = max(.25, 1.0 - .09 * t)
    s += svecha(500, 560 + 92 * (1 - dogor), t, .2, 1.9, 92 * dogor)
    s += teplo(500, 620, 520, 460, .8)
    s += hodiki(240, 440, t, 1.25)
    s += ten(500, 980, 180, 20, .4)
    s += f'<rect x="300" y="820" width="420" height="40" rx="10" fill="url(#derev)" {o(6)}/>'
    s += utvar_izby(1660, 700, 260, t, 19)
    s += mebel_hlam(820, 1010, 560, t, 20)
    s += vinetka(.52)
    return s


def spalnya(t):
    """Изба с прялкой перетекает в городскую спальню с ночником."""
    g = A.ease(A.seg(t, 2.6, 2.2))
    s = brevna(-20, -20, W + 40, H + 40, 118)
    s += f'<rect width="{W}" height="{H}" fill="#b9ad9a" opacity="{.72*g:.2f}"/>'
    s += f'<rect width="{W}" height="{H}" fill="#16203a" opacity=".42"/>'
    s += polovicy(900)
    # кровать/лежанка
    s += ten(420, 1000, 330, 26, .5)
    s += f'<rect x="120" y="700" width="620" height="240" rx="14" fill="url(#derev)" {o(8)}/>'
    s += f'<rect x="100" y="560" width="90" height="390" rx="12" fill="url(#derev)" {o(7)}/>'
    s += f'<path d="M140,700 q300,-50 600,0 l0,80 q-300,-44 -600,0 Z" fill="url(#krem)" {o(6)}/>'
    s += f'<path d="M150,660 q110,-56 220,0 q-110,30 -220,0 Z" fill="url(#rush)" {o(6)}/>'
    s += f'<path d="M180,760 q280,-40 540,0 l-20,180 q-260,-34 -500,0 Z" fill="{TKAN}" opacity=".9" {o(6)}/>'
    # ночник / лучина
    s += ten(930, 960, 120, 18, .4)
    s += f'<rect x="820" y="760" width="230" height="200" rx="12" fill="url(#derev)" {o(7)}/>'
    if g > .5:
        s += (f'<path d="M900,760 v-80 h90 v80 Z" fill="{ZHELEZ}" {o(5)}/>'
              f'<path d="M870,680 q75,-70 150,0 Z" fill="{SVET}" opacity="{.7+.3*abs(A.w(t,2.6)):.2f}" {o(5)}/>')
        s += teplo(945, 700, 340, 300, .85)
    else:
        s += svecha(930, 640, t, .3, 1.1)
    s += f'<circle cx="1480" cy="300" r="90" fill="#f6ecd0" opacity="{.5*(1-g)+.15:.2f}"/>'
    s += utvar_izby(1180, 640, 680, t, 18)
    s += vinetka(.5)
    return s


def tropa(t):
    """Сумерки, первый снег, тропа к избе с огоньком в окне."""
    s = nebo("sumer", t, True, 61)
    s += oblaka(t, 220, 4, 63, .35, "#8a8296", 6)
    s += f'<path d="M0,700 Q420,668 900,700 Q1420,732 1920,692 L1920,1080 L0,1080 Z" fill="#3c4356" {o(5)}/>'
    s += sneg_lezhit(740, 22, "#cfd8e6")
    # лес вдали
    for i in range(14):
        x = 60 + i * 140 + 20 * (i % 3)
        h_ = 180 + 60 * ((i * 7) % 4)
        s += (f'<path d="M{x},760 l{-44},0 l44,{-h_} l44,{h_} Z" fill="#2a3348" opacity=".9"/>')
    s += izba_snaruzhi(1180, 880, 520, t, True, True, 5)
    # тропа
    s += (f'<path d="M560,1080 Q760,900 1180,840 L1320,870 Q860,940 700,1080 Z" fill="#e2eaf4"'
          f' opacity=".9" {o(5)}/>')
    for i in range(7):
        u = i / 6
        s += (f'<ellipse cx="{700+u*520:.0f}" cy="{1020-u*160:.0f}" rx="{26-u*14:.0f}"'
              f' ry="{12-u*6:.0f}" fill="#b9c6d8" opacity=".7"/>')
    s += sneg_letit(t, 34, 67, .8, .7)
    s += ramka_pp("levo", "#1c2234", .45)
    s += ulica_dal(60, 760, 460, t, True, 40)
    s += vinetka(.46)
    return s


def stol_pirog(t):
    """Порог избы и кухонный стол с раскатанным тестом."""
    s = brevna(-20, -20, W + 40, H + 40, 116)
    s += f'<rect width="{W}" height="{H}" fill="#f0e2c4" opacity=".2"/>'
    s += polovicy(880)
    s += luch(980, 0, 220, 1080, t, .22)
    s += ten(420, 940, 340, 26, .5)
    s += stol(90, 600, 680, 40)
    s += f'<path d="M110,598 q330,-30 660,0 q-330,24 -660,0 Z" fill="url(#rush)" {o(6)}/>'
    # раскатанное тесто
    s += (f'<ellipse cx="420" cy="586" rx="220" ry="74" fill="url(#krem)" {o(7)}/>')
    s += f'<ellipse cx="370" cy="566" rx="70" ry="22" fill="#fbf4e0" opacity=".7"/>'
    # скалка катается сама (рук не рисуем)
    rx = 420 + 150 * A.w(t, 3.6)
    s += (f'<g transform="translate({rx-420:.0f},0)">'
          f'<rect x="300" y="540" width="240" height="34" rx="17" fill="url(#derev)" {o(6)}/>'
          f'<rect x="250" y="548" width="56" height="18" rx="9" fill="url(#derev)" {o(5)}/>'
          f'<rect x="534" y="548" width="56" height="18" rx="9" fill="url(#derev)" {o(5)}/></g>')
    # мука подлетает
    r = random.Random(23)
    for i in range(14):
        p = ((t * .5) + r.uniform(0, 1)) % 1.0
        s += (f'<circle cx="{300+r.uniform(0,250)+30*A.w(t,4,i*.2):.0f}" cy="{560-p*160:.0f}"'
              f' r="{r.uniform(2,5):.1f}" fill="#fff8e6" opacity="{(1-p)*.7:.2f}"/>')
    s += krynka(760, 590, .7)
    s += dver(1180, 210, 320, 700, .25, "url(#derev)")
    s += f'<rect x="1190" y="220" width="110" height="690" fill="#9fc2de" opacity=".45"/>'
    s += utvar_izby(820, 480, 520, t, 14)
    s += vinetka(.4)
    return s


def krylco_polennica(t):
    """Кузня закрыта: на дверях навесной замок, поленница под снегом,
    подкова над входом, труба холодная."""
    s = nebo("sumer", t, False, 14)
    s += SL(Z_DAL, ulica_dal(1080, 720, 840, t, True, 73))
    s += kladka(-20, 200, 900, 760, 78)
    s += (f'<path d="M-60,210 L420,40 L900,210 Z" fill="#3c2c22" {o(8)}/>'
          f'<path d="M-60,210 L420,40 L900,210 Z" fill="url(#sneg)" opacity=".55"/>')
    # холодная труба: ни дыма
    s += f'<rect x="620" y="60" width="90" height="150" fill="url(#kamen)" {o(7)}/>'
    s += f'<rect x="604" y="46" width="122" height="28" rx="8" fill="url(#sneg)" {o(5)}/>'
    # подкова над дверью
    kach = 2.6 * A.w(t, 3.2)
    s += (f'<g transform="rotate({kach:.2f} 330 300)">'
          f'<path d="M278,386 a56,56 0 1 1 104,0 l-28,0 a30,30 0 1 0 -48,0 Z"'
          f' fill="url(#zhel)" {o(6)}/></g>')
    # створки и замок
    s += f'<rect x="170" y="430" width="330" height="480" rx="8" fill="url(#derev)" {o(8)}/>'
    s += doski(176, 436, 318, 468, 78, True, "dosk")
    s += f'<line x1="335" y1="430" x2="335" y2="910" stroke="{K}" stroke-width="8"/>'
    for y in (520, 800):
        s += f'<rect x="176" y="{y}" width="318" height="26" rx="8" fill="url(#zhel)" {o(5)}/>'
    kz = 3.0 * A.w(t, 2.1)
    s += (f'<g transform="rotate({kz:.2f} 335 650)">'
          f'<rect x="298" y="650" width="74" height="58" rx="14" fill="url(#chug)" {o(6)}/>'
          f'<path d="M312,650 v-30 a23,23 0 0 1 46,0 v30" fill="none" stroke="{ZHELEZ}" stroke-width="12"/>'
          f'<circle cx="335" cy="682" r="9" fill="#d8cdb8"/></g>')
    # поленница под снегом, на ней снегирь
    s += ten(690, 930, 190, 20, .45)
    for r_ in range(4):
        for c in range(7):
            x = 560 + c * 52
            y = 900 - r_ * 48
            s += (f'<circle cx="{x}" cy="{y}" r="24" fill="url(#derev)" {o(4)}/>'
                  f'<circle cx="{x}" cy="{y}" r="11" fill="#c89a62" opacity=".8"/>')
    s += sneg_lezhit(772, 14)
    s += ptica(700, 742, t, 1.15, KRAS, .2)
    s += sneg_lezhit(900, 24)
    s += f'<g opacity=".8">{sneg_letit(t, 46, 17, .75, .9)}</g>'
    s += ramka_pp("levo", "#0a0b10", .48)
    s += vinetka(.48)
    return s


def dvor_bulochnaya(t):
    """Двор многоэтажки: под окнами составлены столы, каждый несёт своё."""
    s = nebo("sumer", t, False, 121)
    s += SL(Z_NEBO, f'<g opacity=".5">{oblaka(t, 130, 4, 123, .45, "#8e9aa8", 16.0)}</g>')
    s += SL(Z_DAL, panelka(60, 700, 900, t, 6, True, 124))
    s += SL(Z_DAL, panelka(1060, 700, 820, t, 5, True, 125))
    s += f'<rect y="700" width="{W}" height="380" fill="#6f7a6a"/>'
    s += sneg_lezhit(700, 16)
    # два стола встык, на них своё у каждого
    s += ten(560, 950, 430, 26, .5)
    s += f'<rect x="150" y="760" width="420" height="34" rx="8" fill="#b79a72" {o(7)}/>'
    s += f'<rect x="570" y="766" width="400" height="34" rx="8" fill="#a88a64" {o(7)}/>'
    for x in (190, 500, 620, 920):
        s += f'<rect x="{x}" y="794" width="26" height="160" fill="#8a6f4c" {o(5)}/>'
    # на столах: кастрюля, тазик салата, торт, банка
    s += (f'<path d="M210,700 h150 q-14,60 -75,60 q-61,0 -75,-60 Z" fill="url(#zhel)" {o(6)}/>'
          f'<ellipse cx="285" cy="702" rx="76" ry="18" fill="#8a9398" {o(4)}/>')
    s += f'<g opacity=".45">{par(285, 686, t, 4, .45, 220, .3)}</g>'
    s += (f'<path d="M400,716 h160 q-16,46 -80,46 q-64,0 -80,-46 Z" fill="#e8dcc6" {o(6)}/>'
          f'<ellipse cx="480" cy="716" rx="81" ry="16" fill="#c9823a" opacity=".9"/>')
    for i in range(7):
        s += (f'<circle cx="{428+i*18}" cy="{710+(i%3)*6}" r="7" fill="{KRAS}" opacity=".85"/>')
    s += (f'<path d="M640,724 h150 l-8,42 h-134 Z" fill="#f6efdc" {o(6)}/>'
          f'<ellipse cx="715" cy="724" rx="76" ry="16" fill="#ffffff" {o(4)}/>')
    for i in range(5):
        s += f'<circle cx="{660+i*28}" cy="716" r="9" fill="{TKAN}" opacity=".9"/>'
    s += (f'<path d="M842,700 h86 l-8,66 h-70 Z" fill="url(#stekl)" opacity=".85" {o(5)}/>'
          f'<rect x="838" y="690" width="94" height="18" rx="7" fill="url(#zhel)" {o(4)}/>')
    for i in range(6):
        s += (f'<ellipse cx="{860+(i%3)*24}" cy="{720+(i//3)*22}" rx="12" ry="9"'
              f' fill="{ZEL2}" opacity=".9"/>')
    # жильцы подходят: один несёт кастрюлю (силуэт), окна зажигаются
    p = (t * .09) % 1.0
    s += siluet(1250 - p * 220, 950, 390, "#1d2128", .96, False, "#c9b07a")
    s += siluet(1420, 950, 370, "#1a1e24", .96, True, "#c9b07a")
    s += teplo(560, 800, 520, 300, .3)
    s += f'<g opacity=".7">{sneg_letit(t, 30, 127, .6, .7)}</g>'
    s += ramka_pp("oba", "#0b0e13", .46)
    s += vinetka(.46)
    return s


def palto(t):
    """Вешалка в сенях: рабочая куртка, под ней ровно поставлены сапоги."""
    s = brevna(-20, -20, W + 40, H + 40, 100)
    s += f'<rect width="{W}" height="{H}" fill="#1c1a22" opacity=".44"/>'
    s += polovicy(880)
    s += luch(560, -30, 380, 920, t, .18)
    s += teplo(380, 480, 420, 380, .5)
    # жердь-вешалка
    s += f'<rect x="60" y="250" width="820" height="24" rx="10" fill="url(#derev)" {o(6)}/>'
    for x in (180, 420, 700):
        s += f'<path d="M{x},274 l0,36" stroke="{ZHELEZ}" stroke-width="10"/>'
    # куртка покачивается
    kach = 1.6 * A.w(t, 4.6)
    s += (f'<g transform="rotate({kach:.2f} 420 290)">'
          f'<path d="M420,300 l-120,70 l-26,440 h292 l-26,-440 Z" fill="#4a5f46" {o(8)}/>'
          f'<path d="M300,370 l-50,240 l56,22 l40,-210 Z" fill="#3f5340" {o(6)}/>'
          f'<path d="M540,370 l50,240 l-56,22 l-40,-210 Z" fill="#3f5340" {o(6)}/>'
          f'<path d="M420,300 l-44,110 l44,40 l44,-40 Z" fill="#6b7f5f" {o(5)}/>'
          f'<rect x="404" y="420" width="32" height="300" fill="#36482f" opacity=".8"/>')
    for i in range(4):
        s += f'<circle cx="420" cy="{470+i*74}" r="11" fill="url(#med)" {o(3)}/>'
    s += "</g>"
    # рукавицы на гвозде, чуть качаются врозь
    for i, x in enumerate((180, 700)):
        k2 = 3.0 * A.w(t, 3.2, i * .4)
        s += (f'<g transform="rotate({k2:.2f} {x} 310)">'
              f'<path d="M{x-40},310 h80 l-6,120 q-34,20 -68,0 Z" fill="url(#tkan)" {o(6)}/>'
              f'<path d="M{x+40},340 q34,16 20,54" fill="none" stroke="{TKAN}" stroke-width="22"/></g>')
    # сапоги ровно под курткой
    for i, x in enumerate((352, 470)):
        s += ten(x, 908, 64, 14, .5)
        s += (f'<path d="M{x-46},760 h92 v96 l44,16 v40 h-136 Z" fill="url(#derev)" {o(7)}/>'
              f'<path d="M{x-46},760 h92 v24 h-92 Z" fill="#5f3f27" {o(4)}/>')
    s += f'<g opacity=".35">{par(420, 860, t, 4, .3, 280, .2, 2.0)}</g>'
    s += mebel_hlam(1420, 960, 500, t, 96)
    s += ramka_pp("levo", "#0c0a10", .46)
    s += vinetka(.46)
    return s


# ─────────────────────── 5. ДЕЛА ЭТОГО ДНЯ ───────────────────────
def ptichiy_dvor(t):
    """Двор утром: куры клюют у крыльца, рядом ведро с очистками."""
    s = nebo("rassv", t, False, 87)
    s += f'<g opacity=".55">{oblaka(t, 180, 4, 89, .5, "#d8dde6", 17.0)}</g>'
    s += SL(Z_DAL, ulica_dal(1020, 700, 900, t, True, 101))
    s += SL(Z_SRED, izba_snaruzhi(60, 820, 560, t, True, True, 102))
    # крыльцо
    s += ten(420, 900, 240, 22, .45)
    for i in range(3):
        s += (f'<rect x="{300-i*20}" y="{820+i*40}" width="{280+i*40}" height="40" rx="8"'
              f' fill="url(#derev)" {o(6)}/>')
    s += f'<rect y="940" width="{W}" height="140" fill="#9c8b6a"/>'
    s += sneg_lezhit(940, 14)
    # куры клюют: головы ходят, зерно рассыпано
    for i, (x, sc, ph) in enumerate(((240, 1.15, .0), (430, 1.0, .35), (620, 1.25, .6), (760, .9, .85))):
        s += ten(x, 1000, 60 * sc, 12, .35)
        s += kura(x, 1000, t, sc, ph, "#e2d6c2" if i % 2 else "#d8bf92", True)
    r = random.Random(13)
    for i in range(40):
        s += (f'<circle cx="{r.uniform(100,860):.0f}" cy="{r.uniform(980,1060):.0f}" r="5"'
              f' fill="{ZOL}" opacity=".85"/>')
    # ведро с очистками
    s += ten(880, 1010, 80, 16, .45)
    s += (f'<path d="M808,870 h150 l-18,140 h-114 Z" fill="url(#zhel)" {o(7)}/>'
          f'<path d="M812,870 q70,-40 142,0" fill="none" stroke="{ZHELEZ}" stroke-width="9"/>')
    for i in range(7):
        x = 830 + (i * 23) % 100
        s += (f'<path d="M{x},{856-(i%3)*12} q20,-20 40,-2 q-20,16 -40,2 Z" fill="#c9a05a"'
              f' opacity=".9" {o(3)}/>')
    # пёрышко летит
    p = (t * .19) % 1.0
    s += (f'<ellipse cx="{300+p*560:.0f}" cy="{760-180*math.sin(p*3.1):.0f}" rx="15" ry="7"'
          f' fill="#fff8e6" opacity="{.75*(1-p*.5):.2f}"'
          f' transform="rotate({p*260:.0f} {300+p*560:.0f} {760-180*math.sin(p*3.1):.0f})"/>')
    s += ramka_pp("oba", "#171a14", .4)
    s += vinetka(.42)
    return s


def kuryatnik_soloma(t):
    """Курятник: солома, миска со скорлупой, курица на насесте щурится."""
    s = doski(-20, -20, W + 40, H + 40, 110, True, "dosk")
    s += f'<rect width="{W}" height="{H}" fill="#241b12" opacity=".46"/>'
    # щель в стене: косой свет и пылинки
    s += (f'<path d="M700,0 l90,0 l-30,1080 l-90,0 Z" fill="{SVET}" opacity=".12"/>')
    s += luch(680, -20, 300, 1100, t, .22)
    s += teplo(360, 620, 460, 380, .5)
    # солома на полу
    s += f'<rect y="820" width="{W}" height="260" fill="url(#solom)"/>'
    r = random.Random(7)
    for i in range(80):
        x = r.uniform(-20, 1000); y = r.uniform(810, 1060)
        a_ = r.uniform(-40, 40)
        s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+58:.0f}" y2="{y+a_*.5:.0f}"'
              f' stroke="#c7a44e" stroke-width="5" opacity=".75"/>')
    # насест, на нём курица
    s += f'<rect x="60" y="520" width="700" height="28" rx="12" fill="url(#derev)" {o(6)}/>'
    s += ten(300, 560, 90, 14, .35)
    s += kura(300, 520, t, 1.5, .0, "#e2d6c2", True)
    s += kura(560, 520, t, 1.25, .4, "#cdbda4", True)
    # гнездо в углу с одним яйцом
    s += (f'<path d="M620,900 q120,-80 240,0 q-60,70 -120,70 q-60,0 -120,-70 Z"'
          f' fill="#b58a42" {o(6)}/>')
    s += (f'<ellipse cx="740" cy="880" rx="44" ry="56" fill="url(#krem)" {o(6)}/>'
          f'<ellipse cx="726" cy="860" rx="12" ry="17" fill="#fffaf0" opacity=".6"/>')
    # миска со скорлупой первым планом
    s += ten(220, 940, 130, 20, .5)
    s += (f'<path d="M100,830 h240 q-18,100 -120,100 q-102,0 -120,-100 Z" fill="url(#glina)" {o(7)}/>'
          f'<ellipse cx="220" cy="832" rx="121" ry="22" fill="#a86a38" {o(5)}/>')
    for i in range(9):
        x = 150 + (i * 37) % 150
        y = 824 - (i % 3) * 10
        dy = 1.4 * A.w(t, 2.6, i * .2)
        s += (f'<path d="M{x},{y+dy:.1f} q22,-26 44,-2 q-22,16 -44,2 Z" fill="#f6efdc" {o(4)}/>')
    # пушинка летит
    p = (t * .22) % 1.0
    s += (f'<ellipse cx="{420+p*300:.0f}" cy="{620+120*math.sin(p*3.1):.0f}" rx="13" ry="7"'
          f' fill="#fff8e6" opacity="{.8*(1-p*.6):.2f}"/>')
    s += mebel_hlam(1460, 1000, 460, t, 99)
    s += ramka_pp("levo", "#0e0a06", .48)
    s += vinetka(.48)
    return s


def okno_balkon(t):
    """Распахнутое окно избы: утренний свет, на подоконнике кринка с водой."""
    s = brevna(-20, -20, W + 40, H + 40, 104)
    s += f'<rect width="{W}" height="{H}" fill="#2b3340" opacity=".3"/>'
    s += polovicy(900)
    vid = (f'<rect x="140" y="170" width="560" height="560" fill="#bcd6ea"/>'
           f'<rect x="140" y="520" width="560" height="210" fill="#e8f1f8"/>'
           + ulica_dal(140, 520, 560, t, True, 81))
    s += okno_izby(140, 170, 560, 560, t, vid, moroz=.12, svet=True)
    # створка открыта наружу, свет косо падает в комнату
    s += (f'<g transform="rotate(-9 700 440)">'
          f'<rect x="700" y="170" width="250" height="560" rx="8" fill="url(#derev)" opacity=".92" {o(7)}/>'
          f'<rect x="724" y="196" width="202" height="508" fill="url(#stekl)" opacity=".5"/></g>')
    s += luch(170, 190, 620, 860, t, .3)
    s += teplo(430, 500, 520, 440, .7)
    # подоконник, кринка, над ней пар; рядом рушник
    s += f'<rect x="110" y="730" width="620" height="40" rx="10" fill="url(#derev)" {o(7)}/>'
    s += krynka(260, 726, 1.25)
    s += f'<g opacity=".5">{par(260, 646, t, 4, .45, 240, .3)}</g>'
    s += (f'<path d="M430,730 h250 l-20,120 h-210 Z" fill="url(#rush)" {o(5)}/>'
          f'<rect x="452" y="770" width="206" height="8" fill="{TKAN}" opacity=".7"/>')
    s += ptica(690, 700, t, .95, "#5b6a78", .3)
    s += zanaveska(110, 160, 580, 160, KREM, t, 1)
    s += utvar_izby(1140, 560, 720, t, 82)
    s += mebel_hlam(1480, 950, 440, t, 83)
    s += ramka_pp("levo", "#0d1016", .42)
    s += vinetka(.42)
    return s


def mezhdu_ramami(t):
    """Очень крупно старое двойное окно: вата между рамами, бумажные полоски."""
    s = f'<rect width="{W}" height="{H}" fill="#5e6a74"/>'
    s += f'<rect x="60" y="60" width="1800" height="960" rx="10" fill="url(#derev)" {o(10)}/>'
    s += f'<rect x="140" y="140" width="1640" height="800" fill="url(#stekl)" opacity=".85" {o(8)}/>'
    s += f'<rect x="920" y="140" width="40" height="800" fill="url(#derev)" {o(6)}/>'
    s += f'<rect x="140" y="520" width="1640" height="36" fill="url(#derev)" {o(6)}/>'
    # вата между рамами — объёмные комья
    r = random.Random(43)
    for i in range(18):
        x = 180 + i * 92
        y = 880 + 10 * A.w(t, 7 + i * .3, i * .1)
        s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(48,66):.0f}"'
              f' ry="{r.uniform(30,44):.0f}" fill="url(#sneg)" {o(5)}/>')
    # бумажные полоски по швам
    for i, (x, y, w_, h_) in enumerate(((150, 500, 1620, 54), (900, 150, 60, 780))):
        kach_m = 0
        s += (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="6" fill="url(#list)"'
              f' opacity=".92" {o(5)}/>')
    ug = 4 * A.w(t, 3.4)
    s += (f'<g transform="rotate({ug:.1f} 1700 200)">'
          f'<path d="M1660,180 h130 l-10,160 h-110 Z" fill="url(#list)" opacity=".95" {o(5)}/></g>')
    # свет и иней на стекле
    s += f'<path d="M260,180 l420,740" stroke="#ffffff" stroke-width="40" opacity=".14"/>'
    for i in range(14):
        cx = r.uniform(160, 1760); cy = r.uniform(160, 880)
        s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r.uniform(20,56)*(0.6+0.4*abs(A.w(t,8+i*.3,i*.1))):.0f}"'
              f' fill="#ffffff" opacity=".15"/>')
    s += vinetka(.44)
    return s


def dve_hozyayki(t):
    """Полиэкран: слева дверь птичника, справа кухня с овощами на газете."""
    hw = W / 2
    s = f'<rect width="{W}" height="{H}" fill="#1a1c20"/>'
    s += f'<clipPath id="hzL"><rect width="{hw:.0f}" height="{H}"/></clipPath><g clip-path="url(#hzL)">'
    s += nebo("den", t, False)
    s += f'<rect y="740" width="{hw:.0f}" height="340" fill="#7a7a62" {o(5)}/>'
    s += brevna(60, 300, 840, 460, 80)
    s += f'<path d="M20,300 L440,180 L880,300 Z" fill="url(#solom)" {o(7)}/>'
    s += f'<rect x="300" y="470" width="280" height="290" rx="8" fill="#2a1f14" {o(7)}/>'
    s += teplo(440, 640, 300, 280, .7)
    for i, x in enumerate((360, 500)):
        s += kura(x, 740, t, .8, i * .3)
    s += "</g>"
    s += f'<clipPath id="hzR"><rect x="{hw:.0f}" width="{hw:.0f}" height="{H}"/></clipPath><g clip-path="url(#hzR)">'
    s += f'<rect x="{hw:.0f}" width="{hw:.0f}" height="{H}" fill="#b9ad9a"/>'
    for c in range(7):
        s += f'<rect x="{hw+c*140:.0f}" width="130" height="{H}" fill="#c6baa6" opacity="{.4 if c%2 else .14}"/>'
    s += f'<rect x="{hw:.0f}" y="880" width="{hw:.0f}" height="200" fill="url(#pol)" {o(4)}/>'
    s += stol(hw + 80, 620, 780, 40)
    s += f'<rect x="{hw+110:.0f}" y="600" width="720" height="24" fill="url(#list)" opacity=".9" {o(4)}/>'
    for i in range(9):
        s += f'<line x1="{hw+130+i*78:.0f}" y1="604" x2="{hw+180+i*78:.0f}" y2="604" stroke="#8a8070" stroke-width="4"/>'
    s += kartoshka(hw + 330, 586, t, 11, 6, 1.2)
    for i, x in enumerate((hw + 640, hw + 740)):
        s += (f'<ellipse cx="{x:.0f}" cy="584" rx="36" ry="48" fill="{ORA}" {o(5)}/>'
              f'<path d="M{x:.0f},536 q10,-30 26,-34" fill="none" stroke="{ZEL2}" stroke-width="8"/>')
    s += teplo(hw + 400, 500, 420, 360, .5)
    s += "</g>"
    s += f'<rect x="{hw-4:.0f}" width="8" height="{H}" fill="{K}" opacity=".85"/>'
    return s


def yaschik_balkon(t):
    """Балкон: горшок, в землю уходит толчёная скорлупа, рядом совок."""
    s = nebo("den", t, False, 93)
    s += f'<g opacity=".6">{oblaka(t, 160, 4, 97, .5, "#ffffff", 18.0)}</g>'
    s += SL(Z_DAL, panelka(1180, 760, 740, t, 6, False, 107))
    # парапет балкона
    s += f'<rect y="640" width="{W}" height="60" rx="10" fill="#9aa3a8" {o(7)}/>'
    s += f'<rect y="700" width="{W}" height="380" fill="url(#beton)"/>'
    for i in range(13):
        s += f'<rect x="{i*150}" y="700" width="18" height="380" fill="#8a9398" opacity=".7"/>'
    s += doski(-20, 980, W + 40, 120, 140, False, "beton")
    # ящик-горшок крупно
    s += ten(400, 1000, 300, 24, .5)
    s += (f'<path d="M140,760 h540 l-54,250 h-432 Z" fill="url(#glina)" {o(8)}/>'
          f'<rect x="130" y="736" width="560" height="40" rx="10" fill="#b5703a" {o(6)}/>')
    s += (f'<path d="M168,790 h484 l-14,60 h-456 Z" fill="#4e3a26" {o(4)}/>')
    # скорлупа сыплется сверху в землю
    for i in range(9):
        p = ((t * .5 + i * .11) % 1.0)
        x = 300 + i * 30
        y = 560 + p * 240
        s += (f'<path d="M{x},{y:.0f} q18,-20 36,-2 q-18,14 -36,2 Z" fill="#fdf8ea"'
              f' opacity="{.9*(1-p*.4):.2f}"'
              f' transform="rotate({p*300:.0f} {x} {y:.0f})"/>')
    for i in range(12):
        x = 190 + (i * 43) % 430
        s += (f'<path d="M{x},{800+(i%3)*14} q20,-22 40,-2 q-20,14 -40,2 Z" fill="#f6efdc"'
              f' opacity=".85" {o(3)}/>')
    # росток и совок
    for i, x in enumerate((280, 420, 560)):
        kl = 5.0 * A.w(t, 3.2, i * .3)
        s += (f'<path d="M{x},790 q{kl:.1f},-70 {kl*2:.1f},-120" fill="none" stroke="{ZEL2}"'
              f' stroke-width="9"/>'
              f'<path d="M{x+kl*2:.1f},660 q26,-18 42,8 q-26,18 -42,-8 Z" fill="{TRAVA}" {o(4)}/>')
    s += (f'<g transform="rotate(26 760 860)">'
          f'<rect x="748" y="700" width="24" height="170" rx="10" fill="url(#derev)" {o(5)}/>'
          f'<path d="M716,860 h88 l-14,80 h-60 Z" fill="url(#zhel)" {o(6)}/></g>')
    s += ptica(900, 640, t, .9, "#5b6a78", .3)
    s += ramka_pp("oba", "#2e3640", .34)
    s += vinetka(.4)
    return s


def prazdnichnyj_stol(t):
    """Девичий пир: снятая изба, длинный стол, платки на лавке, горшок каши."""
    s = brevna(-20, -20, W + 40, H + 40, 102)
    s += f'<rect width="{W}" height="{H}" fill="#241c26" opacity=".3"/>'
    s += polovicy(910)
    s += lampa(420, 380, t, 1.05, True)
    s += teplo(430, 540, 560, 440, .7)
    # стол вдоль кадра, рушник, девичьи платки по лавке
    s += ten(460, 940, 420, 26, .5)
    s += f'<rect x="50" y="650" width="830" height="44" rx="10" fill="url(#derev)" {o(8)}/>'
    s += (f'<path d="M70,646 q410,-54 830,0 l-34,54 h-762 Z" fill="url(#rush)" {o(6)}/>'
          f'<rect x="110" y="676" width="750" height="9" fill="{TKAN}" opacity=".7"/>')
    # горшок каши в середине: пар валит
    s += ten(440, 656, 120, 18, .4)
    s += (f'<path d="M352,520 q88,-26 176,0 q22,120 -88,120 q-110,0 -88,-120 Z"'
          f' fill="url(#glina)" {o(7)}/>'
          f'<ellipse cx="440" cy="524" rx="90" ry="22" fill="#b5703a" {o(5)}/>'
          f'<ellipse cx="440" cy="524" rx="72" ry="16" fill="#e8d2a0" opacity=".95"/>')
    s += f'<g opacity=".6">{par(440, 500, t, 6, .55, 300, .34, 1.2)}</g>'
    # миски девушек по кругу и ложки
    for i, x in enumerate((150, 270, 620, 760)):
        s += (f'<path d="M{x-48},618 h96 q-10,52 -48,52 q-38,0 -48,-52 Z" fill="url(#krem)" {o(5)}/>'
              f'<ellipse cx="{x}" cy="618" rx="48" ry="13" fill="#dcc9a4" {o(4)}/>'
              f'<rect x="{x+34}" y="600" width="58" height="12" rx="6" fill="url(#derev)"'
              f' transform="rotate(-18 {x+60} 606)" {o(3)}/>')
    s += karavay(700, 640, .72)
    # лавка с платками: два платка яркие, качаются от сквозняка
    s += lavka(80, 780, 300)
    s += lavka(560, 780, 300)
    for i, (x, c) in enumerate(((160, TKAN), (300, "#c9823a"), (640, TKAN2), (790, "#8a4a6a"))):
        kach = 2.0 * A.w(t, 3.6, i * .3)
        s += (f'<g transform="rotate({kach:.2f} {x} 780)">'
              f'<path d="M{x-56},778 q56,-40 112,0 q-20,80 -56,80 q-36,0 -56,-80 Z"'
              f' fill="{c}" {o(6)}/></g>')
    s += utvar_izby(1140, 560, 720, t, 111)
    s += mebel_hlam(1500, 960, 420, t, 112)
    s += ramka_pp("levo", "#0f0b12", .44)
    s += vinetka(.44)
    return s


def kuhnya_duhovka(t):
    """Кухня в ремонте: на табурете отложены отвёртка и снятая дверца шкафа."""
    s = f'<rect width="{W}" height="{H}" fill="#cfc6b4"/>'
    s += f'<rect width="{W}" height="680" fill="#c6bba6"/>'
    s += doski(-20, 680, W + 40, 420, 150, False, "dosk")
    s += f'<rect y="670" width="{W}" height="16" fill="#8a6f4c"/>'
    # шкаф со снятой дверцей: видна полка с посудой
    s += f'<rect x="120" y="160" width="520" height="420" rx="10" fill="#9c7f5c" {o(8)}/>'
    s += f'<rect x="150" y="190" width="460" height="360" rx="6" fill="#4e3f30" {o(5)}/>'
    s += polka(160, 370, 440)
    for i in range(4):
        x = 220 + i * 110
        s += (f'<ellipse cx="{x}" cy="352" rx="40" ry="13" fill="#ffffff" {o(4)}/>'
              f'<path d="M{x-40},352 q40,24 80,0 l-6,20 h-68 Z" fill="#ffffff" {o(3)}/>')
    for i in range(3):
        s += krynka(230 + i * 120, 540, .5)
    # пустые петли там, где была дверца
    for y in (220, 500):
        s += (f'<rect x="628" y="{y}" width="34" height="56" rx="8" fill="url(#zhel)" {o(5)}/>')
    # табурет с дверцей и отвёрткой
    s += ten(880, 930, 160, 20, .45)
    s += (f'<rect x="760" y="700" width="240" height="30" rx="8" fill="#b79a72" {o(6)}/>')
    for x in (780, 960):
        s += f'<rect x="{x}" y="730" width="22" height="200" fill="#a88a64" {o(5)}/>'
    kach = 1.2 * A.w(t, 5.0)
    s += (f'<g transform="rotate({-6+kach:.2f} 880 700)">'
          f'<rect x="770" y="612" width="220" height="90" rx="8" fill="#9c7f5c" {o(6)}/>'
          f'<rect x="786" y="628" width="188" height="58" rx="6" fill="none"'
          f' stroke="#7d6346" stroke-width="7"/>'
          f'<circle cx="956" cy="656" r="11" fill="url(#zhel)" {o(3)}/></g>')
    bl = .3 + .7 * abs(A.w(t, 2.8))
    s += (f'<g transform="rotate(14 880 690)">'
          f'<rect x="824" y="676" width="150" height="16" rx="7" fill="#d8d2c4" {o(4)}/>'
          f'<rect x="800" y="670" width="40" height="28" rx="9" fill="{KRAS}" {o(4)}/>'
          f'<rect x="900" y="678" width="70" height="12" rx="5" fill="#ffffff"'
          f' opacity="{.4*bl:.2f}"/></g>')
    # шурупы в блюдце — чтобы не потерялись
    s += (f'<ellipse cx="1140" cy="712" rx="60" ry="20" fill="#ffffff" {o(5)}/>')
    for i in range(5):
        s += (f'<rect x="{1108+i*14}" y="{700+(i%2)*8}" width="10" height="22" rx="4"'
              f' fill="{ZHELEZ}" {o(0)}/>')
    s += luch(140, 0, 420, 900, t, .22)
    s += kvartira_veschi(1420, 690, 500, t, 98)
    s += f'<g opacity=".3">{par(700, 660, t, 4, .3, 300, .18, 2.2)}</g>'
    s += ramka_pp("levo", "#2a2318", .32)
    s += vinetka(.4)
    return s


def zimnyaya_noch(t):
    """Ночная деревня под снегом: избы, трубы, искра летит над крышей."""
    s = nebo("noch", t, True, 101)
    s += f'<circle cx="1560" cy="220" r="96" fill="#f6ecd0" opacity=".85"/>'
    s += teplo(1560, 220, 360, 360, .4)
    s += f'<path d="M0,820 Q480,780 960,816 Q1440,850 1920,806 L1920,1080 L0,1080 Z" fill="#2b3550" {o(5)}/>'
    s += sneg_lezhit(840, 26, "#cfd8e6")
    for i, (x, b, w_) in enumerate(((40, 880, 380), (420, 920, 330), (760, 890, 300))):
        s += izba_snaruzhi(x, b, w_, t, True, True, i + 2)
    s += panelka(1240, 900, 420, t, 4, True, 23)
    # искра летит над крышей
    p = (t * .22) % 1.0
    s += (f'<circle cx="{200+p*900:.0f}" cy="{560-240*math.sin(p*math.pi):.0f}"'
          f' r="{8+4*abs(A.w(t,2.0)):.1f}" fill="{SVET}" opacity="{.9-.4*p:.2f}"/>')
    s += (f'<circle cx="{200+p*900:.0f}" cy="{560-240*math.sin(p*math.pi):.0f}"'
          f' r="{26+8*abs(A.w(t,2.0)):.1f}" fill="{SVET}" opacity=".25"/>')
    s += sneg_letit(t, 40, 103, .85, .7)
    s += ulica_dal(1600, 900, 320, t, True, 42)
    s += vinetka(.48)
    return s


def zaslonka(t):
    """Крупно белёная печь, чугунная заслонка, дымоход."""
    s = brevna(-20, -20, W + 40, H + 40, 118)
    s += f'<rect width="{W}" height="{H}" fill="#1c2230" opacity=".3"/>'
    s += polovicy(960)
    s += teplo(460, 620, 700, 620, .85)
    s += ten(480, 1000, 400, 26, .5)
    s += f'<rect x="80" y="120" width="860" height="880" rx="24" fill="url(#pech)" {o(10)}/>'
    s += f'<rect x="120" y="80" width="780" height="52" rx="12" fill="{PECH2}" {o(7)}/>'
    s += f'<rect x="420" y="-40" width="200" height="130" rx="10" fill="url(#kamen)" {o(7)}/>'
    for i in range(4):
        s += f'<line x1="100" y1="{240+i*180}" x2="920" y2="{240+i*180}" stroke="{PECH2}" stroke-width="6" opacity=".55"/>'
    # устье и заслонка, она отъезжает
    s += f'<path d="M200,780 v-240 q230,-190 460,0 v240 Z" fill="#160d08" {o(8)}/>'
    s += ugli(250, 756, 360, t, 8)
    s += ogon(430, 760, t, 1.5, .1, 7)
    dv = 300 * A.ease(A.seg(t, 1.4, 1.8))
    s += (f'<g transform="translate({dv:.0f},0)">'
          f'<path d="M180,790 v-260 q250,-210 500,0 v260 Z" fill="url(#chug)" {o(8)}/>'
          f'<circle cx="430" cy="640" r="34" fill="url(#zhel)" {o(6)}/>'
          f'<rect x="398" y="606" width="64" height="26" rx="10" fill="{ZHELEZ}" {o(4)}/></g>')
    s += f'<g opacity=".4">{dym(520, 80, t, 4, .25, 200, .4, "#aab0b8", .8)}</g>'
    s += utvar_izby(1060, 700, 800, t, 15)
    s += mebel_hlam(1000, 1010, 560, t, 16)
    s += vinetka(.42)
    return s


def rozetka_plita(t):
    """Три крупных плана в ряд: розетка с тройниками, газовая плита, обогреватель."""
    tr = W / 3
    s = f'<rect width="{W}" height="{H}" fill="#6c6358"/>'
    for i, col in enumerate(("#c6baa6", "#b4c0b4", "#b9aa9a")):
        s += f'<rect x="{i*tr:.0f}" width="{tr-8:.0f}" height="{H}" fill="{col}"/>'
    # розетка с тройниками
    cx = tr / 2
    s += f'<rect x="{cx-120:.0f}" y="380" width="240" height="240" rx="24" fill="url(#krem)" {o(9)}/>'
    for dx in (-48, 48):
        s += f'<circle cx="{cx+dx:.0f}" cy="500" r="26" fill="#3b3b42" {o(5)}/>'
    for i, (ax, ay) in enumerate(((-160, 700), (160, 700), (0, 800))):
        s += (f'<rect x="{cx+ax-70:.0f}" y="{ay:.0f}" width="140" height="90" rx="16"'
              f' fill="url(#krem)" {o(7)}/>')
        s += (f'<path d="M{cx:.0f},600 q{ax*.6:.0f},{(ay-600)*.5:.0f} {ax:.0f},{ay-600:.0f}"'
              f' fill="none" stroke="#3b3b42" stroke-width="16"/>')
    gr = abs(A.w(t, 1.2))
    s += f'<circle cx="{cx:.0f}" cy="500" r="{60+30*gr:.0f}" fill="{ORA}" opacity="{.25*gr:.2f}"/>'
    for i in range(5):
        a = i * 1.25 + t * 2
        s += (f'<path d="M{cx:.0f},500 l{math.cos(a)*90:.0f},{math.sin(a)*90:.0f}" stroke="{SVET}"'
              f' stroke-width="6" opacity="{.2+.6*gr:.2f}"/>')
    # газовая плита
    cx = tr * 1.5
    s += f'<rect x="{cx-240:.0f}" y="420" width="480" height="420" rx="16" fill="{ZHELEZ}" {o(9)}/>'
    for i, (dx, dy) in enumerate(((-110, 540), (110, 540), (-110, 720), (110, 720))):
        s += f'<circle cx="{cx+dx:.0f}" cy="{dy}" r="66" fill="#2b2b33" {o(6)}/>'
        if i < 2:
            for j in range(10):
                a = j * math.pi / 5
                s += (f'<ellipse cx="{cx+dx+math.cos(a)*42:.0f}" cy="{dy+math.sin(a)*42:.0f}"'
                      f' rx="12" ry="{16+5*A.w(t,.8,j*.1):.0f}" fill="#5aa8e8"'
                      f' opacity="{.6+.4*abs(A.w(t,.9,j*.1)):.2f}"/>')
            s += teplo(cx + dx, dy, 140, 120, .5)
    # обогреватель
    cx = tr * 2.5
    s += ten(cx, 900, 190, 20, .45)
    s += f'<rect x="{cx-200:.0f}" y="440" width="400" height="430" rx="20" fill="{KREM}" {o(9)}/>'
    for i in range(6):
        gl = .4 + .6 * abs(A.w(t, 2.0, i * .15))
        s += (f'<rect x="{cx-160+i*56:.0f}" y="500" width="34" height="300" rx="16"'
              f' fill="{UGOL}" opacity="{gl:.2f}" {o(4)}/>')
    s += teplo(cx, 650, 400, 360, .75)
    for i in range(3):
        s += (f'<path d="M{cx-90+i*90:.0f},430 q20,-{60+20*abs(A.w(t,1.6,i*.3)):.0f} 0,-120"'
              f' fill="none" stroke="#e8c8a0" stroke-width="7" opacity=".4"/>')
    s += f'<rect x="{tr-10:.0f}" width="16" height="{H}" fill="{K}" opacity=".7"/>'
    s += f'<rect x="{tr*2-10:.0f}" width="16" height="{H}" fill="{K}" opacity=".7"/>'
    return s


def pod_maticey(t):
    """Изба вечером: потолочная балка с травами, под ней семья силуэтами."""
    s = brevna(-20, -20, W + 40, H + 40, 116)
    s += f'<rect width="{W}" height="{H}" fill="#1f2534" opacity=".42"/>'
    s += polovicy(920)
    s += f'<rect x="-20" y="150" width="{W+40}" height="78" rx="20" fill="url(#derev)" {o(9)}/>'
    s += ten(960, 250, 820, 20, .4)
    # травы на балке покачиваются
    for i in range(9):
        x = 110 + i * 190
        kach = 2.4 * A.w(t, 4.0 + i * .3, i * .2)
        s += (f'<g transform="rotate({kach:.2f} {x} 228)">')
        for j in range(6):
            s += (f'<path d="M{x},228 q{-30+j*12},90 {-20+j*9},170" fill="none"'
                  f' stroke="{["#6f8c4a","#8a9a58","#5c7a40"][j%3]}" stroke-width="7"/>')
        s += f'<path d="M{x-24},232 q24,-16 48,0" fill="none" stroke="{TKAN}" stroke-width="9"/></g>'
    s += lampa(420, 620, t, 1.0, abazhur=True)
    s += stol(170, 760, 540)
    s += teplo(430, 740, 520, 400, .7)
    for i, (x, h_) in enumerate(((240, 310), (420, 330), (590, 250), (700, 230))):
        s += siluet(x, 760, h_, "#1a1b22", .92, platok=(i == 0), kant="#c8a86a")
    s += utvar_izby(1100, 820, 760, t, 17)
    s += vinetka(.48)
    return s


def bolshoy_stol(t):
    """Большой стол в избе: общая миска, рушник, вокруг пустые места."""
    s = brevna(-20, -20, W + 40, H + 40, 104)
    s += f'<rect width="{W}" height="{H}" fill="#1d1a22" opacity=".36"/>'
    s += polovicy(900)
    s += lampa(430, 400, t, 1.0, True)
    s += teplo(430, 560, 560, 420, .66)
    # длинный стол поперёк кадра
    s += ten(470, 930, 430, 28, .5)
    s += f'<rect x="60" y="640" width="840" height="46" rx="10" fill="url(#derev)" {o(8)}/>'
    for x in (120, 800):
        s += f'<rect x="{x}" y="686" width="40" height="250" fill="url(#derev)" {o(6)}/>'
    s += (f'<path d="M80,636 q420,-56 840,0 l-36,56 h-768 Z" fill="url(#rush)" {o(6)}/>'
          f'<rect x="120" y="668" width="760" height="9" fill="{TKAN}" opacity=".7"/>')
    # общая миска посередине: пар и круги
    s += ten(470, 648, 140, 18, .4)
    s += (f'<path d="M340,556 h262 q-20,92 -131,92 q-111,0 -131,-92 Z" fill="url(#glina)" {o(7)}/>'
          f'<ellipse cx="471" cy="558" rx="132" ry="24" fill="#b5703a" {o(5)}/>'
          f'<ellipse cx="471" cy="558" rx="112" ry="18" fill="#d8a05a" opacity=".9"/>')
    r_ = 18 + 30 * ((t * .45) % 1.0)
    s += (f'<ellipse cx="471" cy="558" rx="{r_:.0f}" ry="{r_*.18:.0f}" fill="none"'
          f' stroke="#f2cf8c" stroke-width="4" opacity="{.5*(1-(t*.45)%1.0):.2f}"/>')
    s += f'<g opacity=".55">{par(471, 540, t, 5, .5, 260, .32)}</g>'
    s += karavay(720, 630, .78)
    # пустые места: лавки и перевёрнутые кружки
    s += lavka(90, 760, 320)
    s += lavka(560, 760, 320)
    for i, x in enumerate((200, 330, 640, 760)):
        s += (f'<path d="M{x-34},636 v-44 q34,-20 68,0 v44 Z" fill="url(#krem)" {o(5)}/>'
              f'<ellipse cx="{x}" cy="592" rx="34" ry="10" fill="#dcc9a4" {o(4)}/>')
    s += utvar_izby(1160, 560, 700, t, 92)
    s += mebel_hlam(1500, 960, 420, t, 93)
    s += ramka_pp("levo", "#0d0b10", .44)
    s += vinetka(.44)
    return s


# ─────────────────────── 6. ПОГОДА ПО ПРИМЕТАМ ───────────────────────
def krylco_rassvet(t):
    """Крыльцо на рассвете: фигура в тулупе смотрит на реку, пар дыхания."""
    s = nebo("rassv", t, False, 129)
    s += f'<g opacity=".6">{oblaka(t, 170, 4, 131, .5, "#f0dfc8", 18.0)}</g>'
    # заря наливается
    zar = .5 + .5 * A.ease(A.seg(t, .5, 5.0))
    s += (f'<path d="M-20,420 q500,-80 1000,-30 q500,50 960,-40 L{W},620 H-20 Z"'
          f' fill="{ORA}" opacity="{.18*zar:.2f}"/>')
    s += (f'<path d="M-20,540 q480,-50 980,-14 q500,36 960,-20 L{W},640 H-20 Z"'
          f' fill="#4e5a48" opacity=".8"/>')
    # река в глубине со льдом у берега
    s += f'<rect y="620" width="{W}" height="140" fill="url(#voda)" opacity=".9"/>'
    s += (f'<path d="M-20,700 q480,-30 980,-6 q500,24 960,-10 l0,70 H-20 Z"'
          f' fill="url(#led)" opacity=".8"/>')
    s += f'<g opacity=".45">{tuman(t, 660, .45, "#e4ecf2")}</g>'
    # крыльцо первым планом справа, фигура на верхней ступени
    s += brevna(820, 180, 1120, 620, 96)
    s += (f'<path d="M780,190 L1380,40 L1960,190 Z" fill="#46342a" {o(8)}/>')
    for i in range(3):
        s += (f'<rect x="{900-i*40}" y="{800+i*44}" width="{520+i*80}" height="44" rx="8"'
              f' fill="url(#derev)" {o(6)}/>')
    s += siluet(1120, 800, 430, "#242a30", .97, False, "#f0c387")
    s += f'<g opacity=".6">{par(1070, 640, t, 5, .55, 180, .5, 1.0)}</g>'
    # перила и сосулька
    s += (f'<rect x="880" y="700" width="560" height="20" rx="8" fill="url(#derev)" {o(5)}/>')
    for i, x in enumerate((940, 1120, 1320)):
        s += f'<rect x="{x}" y="720" width="18" height="120" fill="url(#derev)" {o(4)}/>'
    dl = 50 + 18 * abs(A.w(t, 6.4))
    s += f'<path d="M1420,190 l16,0 l-8,{dl:.0f} Z" fill="url(#led)" opacity=".9" {o(3)}/>'
    s += sneg_lezhit(930, 20)
    s += ptica(420, 560, t, .9, "#4a5560", .2)
    s += ptica(560, 600, t, .75, "#5b6a78", .5)
    s += ramka_pp("pravo", "#191d16", .4)
    s += vinetka(.42)
    return s


def pleten_pticy(t):
    """Плетень с горшками, рябина, большое небо — примета по птицам."""
    s = nebo("den", t, False)
    s += oblaka(t, 180, 6, 109, .55, "#dde6ee", 9)
    s += f'<path d="M0,780 Q480,756 960,780 Q1440,804 1920,772 L1920,1080 L0,1080 Z" fill="#6f7a58" {o(5)}/>'
    s += pleten(40, 860, 780, 240, 11)
    for i, x in enumerate((180, 420, 660)):
        kach = 2.0 * A.w(t, 4.4, i * .3)
        s += f'<g transform="rotate({kach:.2f} {x} 600)">{krynka(x, 616, 1.0)}</g>'
    s += ryabina(1180, 820, t, 1.6, 6)
    s += f'<rect x="1160" y="820" width="46" height="260" fill="#6b4428" {o(6)}/>'
    for i, (x, y, col) in enumerate(((1120, 640, KRAS), (1270, 700, KRAS), (1200, 560, "#8a7f6e"))):
        s += ptica(x, y - 8 * abs(A.w(t, 1.5, i * .3)), t, .95, col, i * .3)
    for i, x in enumerate((320, 520)):
        s += ptica(x, 600 - 10 * abs(A.w(t, 1.7, i * .4)), t, .8, "#8a7f6e", i * .35, "#6b6356")
    s += f'<g opacity=".5">{sneg_letit(t, 10, 113, .4, .35)}</g>'
    s += ulica_dal(60, 780, 420, t, True, 46)
    s += vinetka(.36)
    return s


def pole_nebo(t):
    """Поле: валы борозды сходятся к горизонту, плуг брошен на краю."""
    s = nebo("rassv", t, False, 99)
    s += f'<g opacity=".7">{oblaka(t, 170, 6, 101, .6, "#e4e9f0", 20.0)}</g>'
    GOR = 560                                   # линия горизонта
    s += f'<rect y="{GOR}" width="{W}" height="{H-GOR}" fill="#6f5a3c"/>'
    s += (f'<path d="M-20,{GOR} q500,-26 1000,-8 q480,18 960,-14 l0,70 H-20 Z"'
          f' fill="#5a4a30" opacity=".8"/>')
    # борозды: гребни валов уходят к горизонту — шаг и толщина растут к камере
    bl = (t * .1) % 1.0
    y = GOR + 6
    i = 0
    while y < 1140:
        shag = 9 + i * 5.0
        tol = max(3.5, shag * .62)
        proval = 960 + 40 * math.sin(i * .7)      # лёгкий изгиб валов
        svet = .3 + .5 * max(0.0, 1 - abs((y - GOR) / 580.0 - bl) * 5)
        s += (f'<path d="M-40,{y+tol:.0f} q{proval:.0f},{-tol*1.6:.0f} {W+80},{tol*.4:.0f}'
              f' l0,{shag*.75:.0f} q{-proval:.0f},{tol*1.2:.0f} {-W-80},{-tol*.3:.0f} Z"'
              f' fill="#473622" opacity=".92"/>')
        s += (f'<path d="M-40,{y+tol:.0f} q{proval:.0f},{-tol*1.6:.0f} {W+80},{tol*.4:.0f}"'
              f' fill="none" stroke="#d8b474" stroke-width="{tol*.85:.0f}"'
              f' opacity="{.45+svet*.5:.2f}"/>')
        y += shag
        i += 1
    # поперечные перепады земли, чтобы поле не было плоским
    for i, yy in enumerate((640, 760, 900)):
        s += (f'<path d="M-20,{yy} q520,{-26-i*10} 1000,{-10-i*6} q480,{14+i*6} 960,{-12-i*8}'
              f' l0,{40+i*20} H-20 Z" fill="#000000" opacity="{.08+i*.03:.2f}"/>')
    # кромка озими у нижнего края
    for i in range(60):
        x = -20 + i * 34
        kl = 7 * A.w(t, 3.0, i * .06)
        s += (f'<path d="M{x},1080 q{kl:.1f},-36 {kl*2:.1f},-68" fill="none" stroke="{TRAVA}"'
              f' stroke-width="6" opacity=".75"/>')
    # плуг крупно слева, лемех блестит
    bl2 = .35 + .65 * abs(A.w(t, 4.0))
    s += ten(360, 1020, 280, 28, .5)
    s += (f'<path d="M120,980 l400,-110 l40,76 l-400,110 Z" fill="url(#derev)" {o(8)}/>'
          f'<path d="M520,870 l164,116 l-68,54 l-116,-94 Z" fill="url(#zhel)" {o(8)}/>'
          f'<path d="M540,892 l136,96" fill="none" stroke="#fff3d0" stroke-width="10"'
          f' opacity="{.45*bl2:.2f}"/>'
          f'<rect x="92" y="980" width="34" height="120" rx="12" fill="url(#derev)" {o(6)}/>'
          f'<rect x="248" y="930" width="30" height="170" rx="12" fill="url(#derev)" {o(6)}/>')
    # птицы над полем
    for i in range(5):
        p = ((t * .05 + i * .2) % 1.0)
        x = -60 + p * 2040
        y = 230 + 40 * math.sin(p * 6.0 + i)
        s += (f'<path d="M{x:.0f},{y:.0f} q22,-16 44,0 q-22,8 -44,0" fill="none"'
              f' stroke="#3f4a55" stroke-width="5" opacity=".75"/>')
    s += ramka_pp("levo", "#2b2a20", .34)
    s += vinetka(.42)
    return s


































# ─────────────────────── 5. ДЕЛА ЭТОГО ДНЯ ───────────────────────


























# ─────────────────────── 6. ПОГОДА ПО ПРИМЕТАМ ───────────────────────






def okno_kormushka(t):
    """Подоконник: газета, сохнет скорлупа, ступка, ящик с рассадой."""
    s = f'<rect width="{W}" height="{H}" fill="#cdc2ae"/>'
    s += f'<rect width="{W}" height="620" fill="#c3b7a1"/>'
    vid = (f'<rect x="150" y="90" width="620" height="420" fill="#a9c6de"/>'
           f'<rect x="150" y="340" width="620" height="170" fill="#e4eef7"/>'
           + ulica_dal(150, 340, 620, t, True, 103)
           + f'<g opacity=".7">{sneg_letit(t, 18, 91, .6, .7)}</g>')
    s += okno_izby(150, 90, 620, 420, t, vid, moroz=.3, svet=False)
    s += luch(170, 110, 640, 820, t, .24)
    s += teplo(430, 420, 480, 380, .4)
    # подоконник первым планом
    s += f'<rect x="100" y="600" width="740" height="46" rx="10" fill="#e8dcc6" {o(7)}/>'
    # газета, на ней скорлупа
    s += (f'<path d="M140,598 h330 l-10,-120 h-310 Z" fill="#efe9d8" {o(5)}/>')
    for i in range(7):
        s += (f'<line x1="156" y1="{492+i*14}" x2="452" y2="{492+i*14}" stroke="#9c927c"'
              f' stroke-width="4" opacity=".55"/>')
    for i in range(10):
        x = 170 + (i * 41) % 270
        y = 588 - (i % 4) * 16
        dy = 1.2 * A.w(t, 2.4, i * .18)
        s += (f'<path d="M{x},{y+dy:.1f} q24,-28 48,-2 q-24,18 -48,2 Z" fill="#fdf8ea" {o(4)}/>')
    # ступка с толкушкой
    s += ten(560, 604, 60, 12, .4)
    s += (f'<path d="M498,500 h124 q-12,100 -62,100 q-50,0 -62,-100 Z" fill="url(#chug)" {o(7)}/>'
          f'<ellipse cx="560" cy="502" rx="62" ry="16" fill="#3f3b3a" {o(5)}/>'
          f'<rect x="{600}" y="{424}" width="20" height="90" rx="9" fill="url(#derev)"'
          f' transform="rotate(14 610 470)" {o(4)}/>')
    # ящик с рассадой: росток качается
    s += ten(760, 616, 90, 14, .4)
    s += (f'<rect x="672" y="520" width="190" height="90" rx="8" fill="url(#derev)" {o(7)}/>'
          f'<rect x="684" y="532" width="166" height="30" rx="6" fill="#5a4330" {o(4)}/>')
    for i, x in enumerate((716, 768, 820)):
        kl = 4.0 * A.w(t, 3.0, i * .3)
        s += (f'<path d="M{x},532 q{kl:.1f},-40 {kl*2:.1f},-70" fill="none" stroke="{ZEL2}"'
              f' stroke-width="7"/>'
              f'<path d="M{x+kl*2:.1f},462 q22,-14 34,6 q-22,14 -34,-6 Z" fill="{TRAVA}" {o(3)}/>')
    s += ptica(690, 470, t, .85, KRAS, .2)
    s += kvartira_veschi(1180, 620, 740, t, 104)
    s += ramka_pp("levo", "#2a2318", .3)
    s += vinetka(.4)
    return s


def balkon_dvor(t):
    """Полиэкран: слева балкон многоэтажки, справа двор избы, небо общее."""
    hw = W / 2
    s = nebo("den", t, False)
    s += oblaka(t, 170, 6, 149, .55, "#e2eaf2", 10)
    s += f'<clipPath id="bdL"><rect width="{hw:.0f}" height="{H}"/></clipPath><g clip-path="url(#bdL)">'
    s += f'<rect y="700" width="{hw:.0f}" height="380" fill="url(#beton)" {o(6)}/>'
    for i in range(9):
        s += f'<rect x="{40+i*96}" y="380" width="18" height="330" rx="7" fill="{ZHELEZ}" {o(4)}/>'
    s += f'<rect x="20" y="356" width="900" height="26" rx="10" fill="{ZHELEZ}" {o(5)}/>'
    s += f'<rect x="760" y="60" width="200" height="900" fill="url(#beton)" {o(6)}/>'
    s += f'<rect x="120" y="560" width="360" height="150" rx="10" fill="url(#derev)" {o(7)}/>'
    s += sneg_lezhit(680, 12, "#e2eaf4")
    s += "</g>"
    s += f'<clipPath id="bdR"><rect x="{hw:.0f}" width="{hw:.0f}" height="{H}"/></clipPath><g clip-path="url(#bdR)">'
    s += f'<path d="M{hw:.0f},760 Q{hw+480:.0f},736 {W},760 L{W},1080 L{hw:.0f},1080 Z" fill="#6f7a58" {o(5)}/>'
    s += izba_snaruzhi(hw + 420, 880, 440, t, True, True, 7)
    s += pleten(hw + 40, 860, 340, 160, 6)
    s += sneg_lezhit(800, 14, "#dfe8f2")
    s += "</g>"
    s += f'<rect x="{hw-4:.0f}" width="8" height="{H}" fill="{K}" opacity=".85"/>'
    s += f'<g opacity=".7">{sneg_letit(t, 22, 151, .6, .5)}</g>'
    return s


# ─────────────────────── 7. РОДИЛИСЬ В ЭТОТ ДЕНЬ ───────────────────────
def stena_ramki(t):
    """Тёмная стена, три пустые рамки; в средней проявляются два силуэта."""
    s = brevna(-20, -20, W + 40, H + 40, 112)
    s += f'<rect width="{W}" height="{H}" fill="#141019" opacity=".62"/>'
    s += teplo(430, 460, 460, 420, .42)
    s += luch(240, -30, 420, 900, t, .13)
    pr = A.ease(A.seg(t, .8, 2.6))
    for i, (x, y, w_, h_) in enumerate(((100, 300, 230, 290), (380, 240, 300, 360),
                                        (730, 320, 200, 250))):
        kach = 1.2 * A.w(t, 4.4 + i * .7, i * .3)
        s += (f'<g transform="rotate({kach:.2f} {x+w_/2:.0f} {y})">'
              f'{ten(x+w_/2+14, y+h_+18, w_*.5, 14, .4)}'
              f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="10" fill="url(#zol)" {o(7)}/>'
              f'<rect x="{x+16}" y="{y+16}" width="{w_-32}" height="{h_-32}" fill="#1a1620" {o(5)}/>')
        if i == 1:
            s += (f'<g opacity="{pr:.2f}">'
                  f'{siluet(x+w_*.36, y+h_-44, h_*.74, "#4a3a2c", .95, False, "#c69a5e")}'
                  f'{siluet(x+w_*.66, y+h_-44, h_*.70, "#43352a", .95, False, "#c69a5e")}</g>')
            s += teplo(x + w_ / 2, y + h_ / 2, 230, 200, .3 * pr)
        else:
            s += (f'<rect x="{x+16}" y="{y+16}" width="{w_-32}" height="{h_-32}"'
                  f' fill="url(#teplo)" opacity=".12"/>')
        s += "</g>"
    s += f'<g opacity=".4">{par(430, 820, t, 4, .3, 300, .18, 2.2)}</g>'
    s += mebel_hlam(1300, 980, 620, t, 74)
    s += ramka_pp("levo", "#0a0810", .5)
    s += vinetka(.52)
    return s


def tkackij_stanok(t):
    """Угол избы: станок с натянутой основой, прялка, корзина клубков."""
    s = brevna(-20, -20, W + 40, H + 40, 110)
    s += f'<rect width="{W}" height="{H}" fill="#2a2033" opacity=".18"/>'
    s += polovicy(880)
    s += teplo(330, 480, 480, 420, .52)
    s += luch(560, -30, 380, 900, t, .15)
    # рама станка
    s += ten(400, 900, 330, 26, .5)
    for x in (120, 660):
        s += f'<rect x="{x}" y="250" width="46" height="650" rx="12" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="120" y="250" width="586" height="40" rx="12" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="120" y="610" width="586" height="34" rx="10" fill="url(#derev)" {o(6)}/>'
    # основа: нити подрагивают
    for i in range(26):
        x = 150 + i * 21
        dx = 2.2 * A.w(t, 1.5 + i * .09, i * .13)
        s += (f'<line x1="{x:.0f}" y1="292" x2="{x+dx:.1f}" y2="608" stroke="{KREM}"'
              f' stroke-width="4" opacity=".85"/>')
    # бёрдо ходит вверх-вниз
    by = 400 + 54 * A.w(t, 2.6)
    s += (f'<rect x="130" y="{by:.0f}" width="566" height="26" rx="8" fill="url(#zhel)" {o(5)}/>')
    # уже сотканное полотно внизу
    s += (f'<path d="M150,640 h520 q-14,150 -260,150 q-246,0 -260,-150 Z" fill="url(#tkan)" {o(6)}/>')
    for i in range(5):
        s += (f'<line x1="{170+i*8}" y1="{660+i*24}" x2="{650-i*8}" y2="{660+i*24}"'
              f' stroke="#f0d9c4" stroke-width="3" opacity=".4"/>')
    # прялка и корзина с клубками
    s += (f'<rect x="742" y="470" width="22" height="420" rx="9" fill="url(#derev)" {o(5)}/>'
          f'<path d="M736,470 q18,-80 46,-46 q-8,46 -46,46 Z" fill="{KREM}" {o(5)}/>')
    s += ten(820, 900, 110, 18, .45)
    s += (f'<path d="M726,806 h190 l-22,96 h-146 Z" fill="url(#solom)" {o(6)}/>')
    for i, (x, y, c) in enumerate(((766, 800, KREM), (830, 806, "#c8a87e"), (876, 798, TKAN2))):
        dy = 2.4 * A.w(t, 2.2, i * .33)
        s += (f'<circle cx="{x}" cy="{y+dy:.1f}" r="30" fill="{c}" {o(5)}/>'
              f'<path d="M{x-22},{y+dy-8:.1f} q22,16 44,-4" fill="none" stroke="#8a6a46" stroke-width="3"/>')
    s += utvar_izby(1120, 560, 740, t, 65)
    s += mebel_hlam(1480, 950, 440, t, 66)
    s += ramka_pp("levo", "#120e14", .46)
    s += vinetka(.46)
    return s


def parizh_yarmarka(t):
    """Ярмарочная площадь XVIII века: балаган с помостом, фонарики, толпа."""
    s = nebo("sumer", t, True, 163)
    s += f'<rect y="820" width="{W}" height="260" fill="#4a4238"/>'
    for i in range(10):
        s += f'<rect x="{i*200}" y="820" width="190" height="260" fill="#564d42" opacity="{.5 if i%2 else .2}"/>'
    # дома по сторонам
    for x, h_ in ((0, 560), (1560, 620)):
        s += f'<rect x="{x}" y="{880-h_}" width="360" height="{h_}" fill="#6b6054" {o(7)}/>'
        for r_ in range(3):
            s += (f'<rect x="{x+50}" y="{900-h_+60+r_*140}" width="90" height="110" rx="6"'
                  f' fill="{SVET}" opacity="{.3+.4*abs(A.w(t,5+r_,x*.001)):.2f}" {o(4)}/>')
            s += (f'<rect x="{x+200}" y="{900-h_+60+r_*140}" width="90" height="110" rx="6"'
                  f' fill="{SVET}" opacity="{.25+.45*abs(A.w(t,6+r_,x*.002)):.2f}" {o(4)}/>')
    # балаган
    s += f'<path d="M420,380 L880,250 L1340,380 Z" fill="{TKAN}" {o(8)}/>'
    for i in range(9):
        s += f'<path d="M{430+i*102},382 l{(880-(430+i*102))*.28:.0f},-74" stroke="#8c2026" stroke-width="7" opacity=".55"/>'
    s += f'<rect x="440" y="380" width="880" height="330" rx="10" fill="#5c4634" {o(8)}/>'
    s += f'<rect x="480" y="700" width="800" height="50" rx="10" fill="url(#derev)" {o(7)}/>'
    s += teplo(880, 560, 520, 340, .7)
    # фигуры на помосте
    for i, x in enumerate((640, 760, 880, 1000, 1120)):
        s += siluet(x, 700, 230 + 20 * (i % 2), "#241c18", .95, kant=SVET)
    # фонарики качаются
    for i in range(9):
        x = 440 + i * 112
        kach = 5 * A.w(t, 3.4, i * .2)
        s += (f'<g transform="rotate({kach:.1f} {x} 370)">'
              f'<line x1="{x}" y1="370" x2="{x}" y2="420" stroke="{K}" stroke-width="4"/>'
              f'<circle cx="{x}" cy="448" r="26" fill="{SVET}"'
              f' opacity="{.6+.4*abs(A.w(t,2.0,i*.2)):.2f}" {o(4)}/></g>')
    # толпа силуэтами
    for i in range(13):
        x = 60 + i * 150 + 12 * A.w(t, 5.0, i * .2)
        s += siluet(x, 1020, 240 + 30 * ((i * 7) % 3), "#1a1620", .9)
    s += vinetka(.5)
    return s


def vypuklye_bukvy(t):
    """Кованые выпуклые литеры на тёмном: по рельефу идёт свет из горна."""
    s = f'<rect width="{W}" height="{H}" fill="#14100c"/>'
    s += kladka(-20, -20, W + 40, H + 40, 92, "#2a241d")
    s += f'<rect width="{W}" height="{H}" fill="#120e0a" opacity=".55"/>'
    s += teplo(300, 900, 620, 320, .6)
    s += ugli(120, 1010, 560, t, 10, 12)
    s += iskra_let(t, 400, 990, 12, 13, 520, .5)
    # две строки литер: рельеф даёт тень и верхний блик
    bl = (t * .22) % 1.0
    for row, (y, txt, sz) in enumerate(((430, "КУЗЬМА", 150), (610, "ДЕМЬЯН", 150))):
        s += (f'<text x="60" y="{y}" font-family="Georgia,serif" font-size="{sz}"'
              f' font-weight="bold" fill="none" stroke="#070505" stroke-width="20"'
              f' stroke-linejoin="round">{txt}</text>')
        s += (f'<text x="54" y="{y-8}" font-family="Georgia,serif" font-size="{sz}"'
              f' font-weight="bold" fill="url(#zol)">{txt}</text>')
        s += (f'<text x="54" y="{y-8}" font-family="Georgia,serif" font-size="{sz}"'
              f' font-weight="bold" fill="none" stroke="#ffe9b0" stroke-width="3"'
              f' opacity=".55">{txt}</text>')
    s += (f'<rect x="{-500+bl*2400:.0f}" y="300" width="300" height="460" fill="{SVET}"'
          f' opacity=".14" transform="skewX(-18)"/>')
    s += f'<g opacity=".4">{dym(360, 960, t, 5, .2, 360, .3)}</g>'
    s += ramka_pp("oba", "#070504", .5)
    s += vinetka(.5)
    return s


def shkolnyj_klass(t):
    """Класс: доска с рисунком, парта, тетрадь, мел — утренний свет."""
    s = f'<rect width="{W}" height="{H}" fill="#cbbfa6"/>'
    s += f'<rect width="{W}" height="700" fill="#c0b298"/>'
    s += doski(-20, 700, W + 40, 400, 150, False, "dosk")
    s += f'<rect y="690" width="{W}" height="16" fill="#8a6f4c"/>'
    s += luch(1180, 0, 560, 900, t, .26)
    # доска
    s += ten(430, 660, 360, 20, .35)
    s += f'<rect x="90" y="140" width="700" height="440" rx="10" fill="#2e4038" {o(8)}/>'
    s += f'<rect x="110" y="160" width="660" height="400" fill="#35493f"/>'
    # анатомический рисунок мелом: контур тела и подпись
    s += (f'<path d="M300,220 q40,-40 80,0 q-10,50 -40,60 q-30,-10 -40,-60 Z" fill="none"'
          f' stroke="#e8e2d2" stroke-width="6"/>'
          f'<path d="M340,282 q-70,30 -80,150 q-6,90 10,120 M340,282 q70,30 80,150'
          f' q6,90 -10,120" fill="none" stroke="#e8e2d2" stroke-width="6"/>'
          f'<path d="M300,420 q40,20 80,0" fill="none" stroke="#e8e2d2" stroke-width="5"/>')
    # поджелудочная помечена и подсвечена пульсом
    pul = .45 + .55 * abs(A.w(t, 2.0))
    s += (f'<ellipse cx="352" cy="400" rx="46" ry="20" fill="{KRAS}" opacity="{.55*pul:.2f}"/>'
          f'<path d="M398,398 h120" stroke="#f2d9b0" stroke-width="5"/>'
          f'<circle cx="352" cy="400" r="{54*pul:.0f}" fill="none" stroke="{SVET}"'
          f' stroke-width="4" opacity="{.4*(1-pul):.2f}"/>')
    for i in range(3):
        s += (f'<line x1="520" y1="{250+i*44}" x2="730" y2="{250+i*44}" stroke="#d8d2c4"'
              f' stroke-width="5" opacity=".7"/>')
    # полка с мелом, пыль
    s += f'<rect x="90" y="580" width="700" height="24" rx="8" fill="url(#derev)" {o(6)}/>'
    for i, x in enumerate((140, 190, 250)):
        s += f'<rect x="{x}" y="564" width="42" height="16" rx="7" fill="#ffffff" {o(3)}/>'
    s += f'<g opacity=".4">{par(300, 600, t, 4, .3, 260, .2, 2.0)}</g>'
    # парта первым планом с тетрадью и чернильницей
    s += ten(560, 940, 280, 24, .5)
    s += (f'<path d="M300,700 h520 l-30,60 h-460 Z" fill="#b79a72" {o(7)}/>'
          f'<rect x="330" y="760" width="460" height="22" rx="8" fill="#a88a64" {o(5)}/>')
    for x in (360, 740):
        s += f'<rect x="{x}" y="782" width="28" height="170" fill="#8a6f4c" {o(5)}/>'
    kach = 1.0 * A.w(t, 5.4)
    s += (f'<g transform="rotate({-4+kach:.2f} 520 716)">'
          f'<rect x="420" y="684" width="210" height="46" rx="6" fill="#f6efdc" {o(5)}/>')
    for i in range(4):
        s += (f'<line x1="436" y1="{696+i*9}" x2="612" y2="{696+i*9}" stroke="#9c927c"'
              f' stroke-width="3" opacity=".7"/>')
    s += "</g>"
    s += (f'<path d="M680,688 h56 l-6,42 h-44 Z" fill="url(#chug)" {o(5)}/>'
          f'<ellipse cx="708" cy="688" rx="28" ry="9" fill="#1d2b3a"/>')
    s += ramka_pp("levo", "#2a2318", .34)
    s += vinetka(.42)
    return s


def dve_gramoty(t):
    """Полиэкран: слева двое лекарей с посохами, справа врач у стола.
    Свет один и тот же — он и сшивает половины."""
    hw = 830 / 2
    s = f'<rect width="{W}" height="{H}" fill="#15120e"/>'
    # левая: древняя половина
    s += f'<rect x="0" width="{hw:.0f}" height="{H}" fill="#1e1811"/>'
    s += kladka(-20, -20, hw + 20, H + 40, 84, "#3a332a")
    s += f'<rect x="0" width="{hw:.0f}" height="{H}" fill="#15110c" opacity=".5"/>'
    s += teplo(hw * .5, 520, 300, 420, .6)
    s += teplo(hw * .5, 700, 340, 300, .5)
    for i, (x, h_) in enumerate(((hw * .36, 460), (hw * .70, 440))):
        kach = 1.4 * A.w(t, 4.0, i * .3)
        s += (f'<g transform="rotate({kach:.2f} {x:.0f} 960)">'
              f'{siluet(x, 960, h_, "#3a2d20", .97, False, "#f0c070")}'
              f'<rect x="{x+h_*.34:.0f}" y="{960-h_*1.02:.0f}" width="14" height="{h_*1.02:.0f}"'
              f' rx="7" fill="url(#derev)" {o(4)}/></g>')
    s += f'<g opacity=".4">{par(hw*.5, 900, t, 4, .3, 220, .2, 1.8)}</g>'
    # правая: наша половина
    s += f'<rect x="{hw:.0f}" width="{hw:.0f}" height="{H}" fill="#e8eef2"/>'
    s += f'<rect x="{hw:.0f}" y="700" width="{hw:.0f}" height="380" fill="#d8e2e8"/>'
    s += teplo(hw * 1.5, 520, 300, 420, .4)
    s += siluet(hw * 1.5, 880, 460, "#49535d", .96, False, "#ffffff")
    s += (f'<rect x="{hw*1.5-190:.0f}" y="880" width="380" height="34" rx="8"'
          f' fill="#f2f6f9" {o(6)}/>'
          f'<rect x="{hw*1.5-160:.0f}" y="914" width="28" height="140" fill="#dde6ec" {o(4)}/>'
          f'<rect x="{hw*1.5+134:.0f}" y="914" width="28" height="140" fill="#dde6ec" {o(4)}/>')
    # склянка стоит НА СТОЛЕ перед врачом, в ней пузырьки
    s += (f'<path d="M{hw*1.5-46:.0f},772 h92 l-12,106 h-68 Z" fill="url(#stekl)"'
          f' opacity=".9" {o(5)}/>'
          f'<path d="M{hw*1.5-38:.0f},812 h76 l-8,66 h-60 Z" fill="#9fd3e4" opacity=".95"/>'
          f'<rect x="{hw*1.5-26:.0f}" y="752" width="52" height="24" rx="8"'
          f' fill="#cfd8de" {o(4)}/>')
    for i in range(4):
        p = ((t * .6 + i * .25) % 1.0)
        s += (f'<circle cx="{hw*1.5-20+i*14:.0f}" cy="{872-p*56:.0f}" r="5"'
              f' fill="#ffffff" opacity="{.7*(1-p):.2f}"/>')
    # один свет на две половины: полоса идёт сверху через обе
    bl = (t * .16) % 1.0
    s += (f'<rect x="{-300+bl*1500:.0f}" y="0" width="220" height="{H}" fill="{SVET}"'
          f' opacity=".14" transform="skewX(-16)"/>')
    s += (f'<circle cx="{hw:.0f}" cy="200" r="{90+16*A.w(t,3.0):.0f}" fill="{SVET}" opacity=".2"/>')
    # дрожащая граница
    dx = 4 * A.w(t, 1.9)
    s += (f'<rect x="{hw-5+dx:.1f}" y="0" width="10" height="{H}" fill="#f2e2bc" opacity=".55"/>')
    s += vinetka(.48)
    return s


def dom_dozhd(t):
    """Дом под дождём: светится одно окно, у стены отцовская палка, лужа."""
    s = f'<rect width="{W}" height="{H}" fill="#2a3340"/>'
    s += nebo("sumer", t, False, 21)
    s += f'<g opacity=".5">{oblaka(t, 150, 5, 23, .5, "#8e9cae", 14.0)}</g>'
    s += SL(Z_DAL, ulica_dal(1020, 740, 900, t, False, 76))
    s += kladka(-20, 260, 860, 700, 80, "url(#kamen)")
    s += (f'<path d="M-60,270 L400,96 L860,270 Z" fill="#413026" {o(8)}/>')
    vid = f'<rect x="200" y="470" width="260" height="260" fill="#f6dfa6"/>'
    s += okno_izby(200, 470, 260, 260, t, vid, moroz=0, svet=True)
    s += teplo(330, 600, 420, 360, .5 + .06 * A.w(t, 5.0))
    # палка у стены
    s += (f'<rect x="596" y="560" width="22" height="380" rx="10" fill="url(#derev)"'
          f' transform="rotate(7 607 750)" {o(5)}/>'
          f'<circle cx="632" cy="566" r="22" fill="url(#med)" {o(5)}/>')
    # дождь: струи и круги в луже
    for i in range(70):
        x = (i * 97 + int(t * 900)) % 1900
        y = (i * 173 + int(t * 1500)) % 1060
        s += (f'<line x1="{x}" y1="{y}" x2="{x-9}" y2="{y+46}" stroke="#cfe0f0"'
              f' stroke-width="3" opacity=".45"/>')
    s += ten(420, 980, 420, 40, .5)
    s += (f'<path d="M80,962 q340,-34 700,0 q-60,70 -350,70 q-290,0 -350,-70 Z"'
          f' fill="{VODA2}" opacity=".75"/>')
    for i in range(4):
        p = ((t * .7 + i * .25) % 1.0)
        s += (f'<ellipse cx="{200+i*170}" cy="{992+i*8}" rx="{14+p*72:.0f}" ry="{4+p*18:.0f}"'
              f' fill="none" stroke="#bcd8e8" stroke-width="3" opacity="{.5*(1-p):.2f}"/>')
    s += ramka_pp("oba", "#090c11", .5)
    s += vinetka(.52)
    return s


def stol_karta(t):
    """Стол лекарей: свеча, старая карта побережья, циркуль и камешки."""
    s = kladka(-20, -20, W + 40, H + 40, 86, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#1a1611" opacity=".58"/>'
    s += svody(t, "#3f382f", 3)
    s += teplo(420, 640, 520, 400, .72)
    s += f'<rect y="700" width="{W}" height="380" fill="url(#derev)" {o(0)}/>'
    s += doski(-20, 700, W + 40, 400, 104, False)
    # карта: край подрагивает
    kach = 3.0 * A.w(t, 4.2)
    s += ten(430, 880, 330, 26, .45)
    s += (f'<g transform="rotate({-2.4+kach*.2:.2f} 430 790)">'
          f'<path d="M140,700 h580 l-18,190 h-544 Z" fill="url(#list)" {o(6)}/>'
          f'<path d="M160,744 q150,-30 300,10 q140,44 240,-8" fill="none" stroke="#7d6a45"'
          f' stroke-width="7" opacity=".85"/>'
          f'<path d="M160,800 q180,36 330,-14 q130,-44 210,6" fill="none" stroke="#9a8558"'
          f' stroke-width="5" opacity=".7"/>'
          f'<circle cx="470" cy="786" r="13" fill="{KRAS}" {o(4)}/>'
          f'<path d="M700,700 q26,96 -14,190" fill="none" stroke="#b9a478" stroke-width="5"/></g>')
    # циркуль и камешки-грузики
    s += (f'<path d="M620,742 l56,130 M676,872 l54,-130" fill="none" stroke="url(#zhel)"'
          f' stroke-width="11" stroke-linecap="round"/>'
          f'<circle cx="676" cy="874" r="12" fill="{ZHELEZ}" {o(4)}/>')
    for x, y in ((176, 714), (716, 884)):
        s += f'<ellipse cx="{x}" cy="{y}" rx="26" ry="17" fill="url(#kamen)" {o(5)}/>'
    s += svecha(790, 640, t, .1, 1.5)
    s += f'<g opacity=".4">{par(430, 690, t, 3, .3, 190, .22)}</g>'
    s += krynka(196, 690, .72)
    s += mebel_hlam(1500, 1010, 420, t, 75)
    s += ramka_pp("levo", "#0c0a07", .5)
    s += vinetka(.5)
    return s


def hutor(t):
    """Шведский хутор: красный дом с белыми наличниками, луг, низкое небо."""
    s = nebo("den", t, False, 139)
    s += f'<g opacity=".7">{oblaka(t, 180, 6, 141, .6, "#ffffff", 22.0)}</g>'
    s += (f'<path d="M-20,560 q520,-70 1020,-26 q500,44 940,-34 L{W},720 H-20 Z"'
          f' fill="#6f8c4a" opacity=".9"/>')
    s += f'<rect y="700" width="{W}" height="380" fill="{TRAVA}"/>'
    # дом: красные доски, белые наличники, крыша черепицей
    s += ten(520, 880, 330, 26, .45)
    s += (f'<rect x="200" y="420" width="640" height="440" rx="8" fill="#a8372c" {o(8)}/>')
    s += doski(208, 428, 624, 424, 78, True, "tkan")
    s += (f'<path d="M150,430 L520,230 L890,430 Z" fill="#5f4030" {o(8)}/>'
          f'<path d="M150,430 L520,230 L890,430 Z" fill="#7d5636" opacity=".5"/>')
    for i in range(7):
        s += (f'<line x1="{200+i*100}" y1="{430-i*0}" x2="{330+i*100}" y2="260"'
              f' stroke="#4e3526" stroke-width="4" opacity=".4"/>')
    s += f'<rect x="700" y="250" width="70" height="120" fill="#8a7a6a" {o(6)}/>'
    s += f'<g opacity=".5">{dym(735, 240, t, 5, .2, 300, .3)}</g>'
    for i, x in enumerate((280, 460, 640)):
        vid = f'<rect x="{x}" y="520" width="140" height="170" fill="#f0dca8"/>'
        s += okno_izby(x, 520, 140, 170, t, vid, moroz=0, svet=True)
        s += (f'<rect x="{x-24}" y="496" width="188" height="22" rx="7" fill="#f2f0e4" {o(5)}/>')
    s += f'<rect x="420" y="700" width="160" height="160" rx="6" fill="#f2f0e4" {o(7)}/>'
    s += teplo(520, 620, 460, 360, .34)
    # луг: трава клонится волной, пара берёз, птицы
    for i in range(54):
        x = -20 + i * 36
        kl = 9 * A.w(t, 3.6, i * .05)
        s += (f'<path d="M{x},1070 q{kl:.1f},-50 {kl*2:.1f},-96" fill="none" stroke="#88a55a"'
              f' stroke-width="6" opacity=".85"/>')
    for i, x in enumerate((1180, 1320)):
        s += (f'<rect x="{x}" y="520" width="26" height="400" fill="#f2f0e4" {o(5)}/>')
        for j in range(5):
            s += (f'<rect x="{x-2}" y="{560+j*70}" width="30" height="12" fill="#3f352c" opacity=".8"/>')
        s += (f'<ellipse cx="{x+13}" cy="480" rx="120" ry="90" fill="{ZEL2}" opacity=".9" {o(5)}/>')
    for i in range(4):
        p = ((t * .06 + i * .25) % 1.0)
        x = -60 + p * 2040
        y = 200 + 36 * math.sin(p * 6 + i)
        s += (f'<path d="M{x:.0f},{y:.0f} q20,-14 40,0 q-20,8 -40,0" fill="none"'
              f' stroke="#4a5560" stroke-width="5" opacity=".7"/>')
    s += ramka_pp("levo", "#2b3320", .34)
    s += vinetka(.4)
    return s


def prival(t):
    """Осенняя опушка: костёр, котелок, ружьё, охотничья сумка."""
    s = nebo("sumer", t, True, 211)
    s += oblaka(t, 230, 3, 213, .3, "#8a7a6a", 5)
    for i in range(16):
        x = 60 + i * 124
        h_ = 320 + 90 * ((i * 11) % 4)
        s += f'<path d="M{x},760 l-54,0 l54,{-h_} l54,{h_} Z" fill="#2c3a2e" opacity=".9"/>'
    s += f'<path d="M0,740 Q480,716 960,740 Q1440,764 1920,732 L1920,1080 L0,1080 Z" fill="#5a4e38" {o(5)}/>'
    r = random.Random(223)
    for i in range(34):
        x, y = r.uniform(0, W), r.uniform(750, 1060)
        s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="16" ry="10" fill="{["#a8702a","#c08a2a","#8a5a28"][i%3]}"'
              f' opacity=".85" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
    # костёр
    s += teplo(400, 880, 560, 460, .9)
    for i, (bx, by, bw, rot) in enumerate(((250, 940, 320, -8), (280, 910, 280, 9), (330, 880, 200, -4))):
        s += (f'<g transform="rotate({rot} {bx+bw/2:.0f} {by})">'
              f'<rect x="{bx}" y="{by}" width="{bw}" height="40" rx="19" fill="url(#derev)" {o(6)}/>'
              f'<ellipse cx="{bx+8}" cy="{by+20}" rx="14" ry="20" fill="#a8744a" {o(4)}/></g>')
    s += ugli(280, 946, 260, t, 8)
    s += ogon(410, 930, t, 2.0, 0, 10)
    s += iskra_let(t, 410, 800, 12, 227, 520, .5)
    # котелок на треноге
    for dx in (-130, 0, 130):
        s += f'<line x1="{410+dx}" y1="940" x2="410" y2="520" stroke="#3b332a" stroke-width="10"/>'
    kach_m = 2.4 * A.w(t, 3.6)
    s += (f'<g transform="rotate({kach_m:.2f} 410 540)">'
          f'<path d="M320,620 q90,-26 180,0 l-24,170 q-66,24 -132,0 Z" fill="url(#chug)" {o(7)}/>'
          f'<path d="M320,620 q90,-70 180,0" fill="none" stroke="{ZHELEZ}" stroke-width="10"/></g>')
    s += f'<g opacity=".55">{par(410, 600, t, 4, .55, 240, .8, .9)}</g>'
    # ружьё и сумка
    s += (f'<g transform="rotate(-24 980 900)">'
          f'<rect x="860" y="880" width="420" height="20" rx="8" fill="#3b2a1e" {o(5)}/>'
          f'<rect x="1180" y="874" width="180" height="14" rx="6" fill="{ZHELEZ}" {o(4)}/></g>')
    s += ten(1320, 1000, 110, 16, .4)
    s += (f'<path d="M1220,1000 v-150 q100,-34 200,0 v150 Z" fill="#6d4e3a" {o(7)}/>'
          f'<path d="M1220,880 q100,-56 200,0 q-100,-18 -200,0 Z" fill="#5c4030" {o(6)}/>')
    s += mebel_hlam(1500, 1010, 400, t, 54)
    s += vinetka(.46)
    return s


def dve_sosedki(t):
    """Калитка: две фигуры в платках, свёрток переходит через перекладину."""
    s = nebo("sumer", t, False, 57)
    s += SL(Z_DAL, ulica_dal(60, 660, 1800, t, True, 86))
    s += sneg_lezhit(700, 20)
    s += f'<g opacity=".4">{tuman(t, 720, .35, "#d2dde8")}</g>'
    # калитка в плетне
    s += pleten(-40, 700, 420, 190, 7)
    s += pleten(760, 700, 1200, 190, 16)
    s += (f'<rect x="420" y="640" width="30" height="330" fill="url(#derev)" {o(6)}/>'
          f'<rect x="700" y="640" width="30" height="330" fill="url(#derev)" {o(6)}/>')
    kal = 3.0 * A.w(t, 8.0)
    s += (f'<g transform="rotate({kal:.2f} 436 960)">'
          f'<rect x="436" y="720" width="270" height="250" rx="6" fill="url(#derev)" opacity=".95" {o(6)}/>'
          f'<path d="M444,730 L698,956 M698,730 L444,956" stroke="#6d4423" stroke-width="12"/></g>')
    # две фигуры по разные стороны, в платках
    s += siluet(300, 980, 420, "#242932", .97, True, "#9fb0c0")
    s += siluet(840, 980, 404, "#1f242c", .97, True, "#9fb0c0")
    s += f'<g opacity=".55">{par(300, 790, t, 4, .5, 150, .5, 1.1)}</g>'
    s += f'<g opacity=".55">{par(840, 800, t, 4, .5, 150, .5, 1.1)}</g>'
    # свёрток над перекладиной: плывёт от одной к другой
    p = (t * .25) % 1.0
    x = 420 + 300 * A.ease(p)
    y = 740 - 26 * math.sin(p * math.pi)
    s += ten(x, 790, 60, 12, .4)
    s += (f'<g transform="rotate({-8+16*p:.1f} {x:.0f} {y:.0f})">'
          f'<path d="M{x-56:.0f},{y:.0f} h112 l-14,78 h-84 Z" fill="url(#rush)" {o(6)}/>'
          f'<path d="M{x-34:.0f},{y:.0f} q34,-40 68,0" fill="none" stroke="#c9b58c" stroke-width="8"/>'
          f'<rect x="{x-24:.0f}" y="{y+26:.0f}" width="48" height="34" rx="7" fill="#f2e6cc" {o(4)}/></g>')
    s += f'<g opacity=".8">{sneg_letit(t, 40, 61, .7, .85)}</g>'
    s += sneg_lezhit(960, 24)
    s += ramka_pp("oba", "#0b0e14", .46)
    s += vinetka(.46)
    return s


# ─────────────────────── 8. ФИНАЛ ───────────────────────
def dom_vecherom(t):
    """Дом вечером снаружи: одно окно светится, во дворе ни одного следа."""
    s = nebo("noch", t, True, 63)
    s += f'<g opacity=".5">{oblaka(t, 140, 4, 67, .4, "#5b6676", 18.0)}</g>'
    s += SL(Z_DAL, ulica_dal(1100, 700, 820, t, True, 87))
    s += SL(Z_SRED, izba_snaruzhi(120, 880, 760, t, True, True, 88))
    s += teplo(430, 620, 420, 340, .5 + .06 * A.w(t, 5.4))
    # ровный снег во дворе: ни следа
    s += sneg_lezhit(880, 26)
    s += (f'<path d="M-20,900 q480,-40 980,-16 q500,24 980,40 L{W},1080 H-20 Z"'
          f' fill="url(#sneg)" opacity=".96"/>')
    for i in range(7):
        s += (f'<path d="M{-40+i*300},{980+(i%3)*22} q160,-18 320,0" fill="none"'
              f' stroke="#c3d6ea" stroke-width="5" opacity=".5"/>')
    s += f'<g opacity=".8">{sneg_letit(t, 44, 71, .75, .8)}</g>'
    s += ryabina(1180, 1000, t, 1.1, 5)
    s += SL(Z_PERED, pleten(1300, 900, 660, 160, 9))
    s += ramka_pp("oba", "#070910", .5)
    s += vinetka(.5)
    return s


def pamyatka(t):
    """Памятка кузнеца: брус над горном, на нём ПЯТЬ подков с номерами.
    Старая доска-«азбука» его правкой 11.11 выброшена."""
    s = kladka(-20, -20, W + 40, H + 40, 82)
    s += f'<rect width="{W}" height="{H}" fill="#241b14" opacity=".52"/>'
    s += polovicy(H - 80, "url(#dosk)")
    s += teplo(300, 820, 560, 300, .8)
    # горн внизу слева, от него свет на подковы
    s += f'<path d="M40,1000 L40,700 q220,-46 440,0 L480,1000 Z" fill="url(#kamen)" {o(8)}/>'
    s += ugli(90, 676, 340, t, 9, 5)
    s += ogon(250, 668, t, 1.2, .1, 7)
    s += iskra_let(t, 250, 640, 14, 7, 460, .55)
    # брус и пять подков, каждая со своим номером
    s += f'<rect x="60" y="196" width="760" height="44" rx="12" fill="url(#derev)" {o(7)}/>'
    for i in range(5):
        x = 160 + i * 164
        kach = 3.4 * A.w(t, 2.4 + i * .3, i * .2)
        gor = .5 + .5 * abs(A.w(t, 3.0, i * .2))
        s += (f'<g transform="rotate({kach:.2f} {x} 236)">'
              f'<line x1="{x}" y1="238" x2="{x}" y2="312" stroke="{ZHELEZ}" stroke-width="8"/>'
              f'<path d="M{x-76},500 a82,82 0 1 1 152,0 l-40,0 a44,44 0 1 0 -72,0 Z"'
              f' fill="url(#zol)" {o(7)}/>'
              f'<path d="M{x-76},500 a82,82 0 1 1 152,0" fill="none" stroke="{SVET}"'
              f' stroke-width="7" opacity="{.3+.4*gor:.2f}"/>'
              # обводку текста кладём ОТДЕЛЬНЫМ слоем: cairosvg не знает paint-order
              f'<text x="{x}" y="458" text-anchor="middle" font-family="Georgia,serif"'
              f' font-size="76" font-weight="bold" fill="none" stroke="#2a1c10"'
              f' stroke-width="12" stroke-linejoin="round">{i+1}</text>'
              f'<text x="{x}" y="458" text-anchor="middle" font-family="Georgia,serif"'
              f' font-size="76" font-weight="bold" fill="#ffe9b0">{i+1}</text></g>')
    # наковальня и молот у стены
    s += ten(700, 980, 170, 22, .55)
    s += (f'<path d="M596,792 h244 l-30,42 h-184 Z" fill="url(#zhel)" {o(7)}/>'
          f'<rect x="658" y="834" width="120" height="44" fill="url(#chug)" {o(6)}/>'
          f'<path d="M616,878 h204 l-22,52 h-160 Z" fill="url(#chug)" {o(6)}/>')
    kach_m = 2.0 * A.w(t, 1.3)
    s += (f'<g transform="rotate({kach_m:.2f} 860 700)">'
          f'<rect x="846" y="700" width="26" height="240" rx="9" fill="url(#derev)" {o(5)}/>'
          f'<rect x="812" y="660" width="96" height="56" rx="12" fill="url(#chug)" {o(6)}/></g>')
    s += f'<g opacity=".4">{dym(250, 600, t, 5, .22, 320, .3)}</g>'
    s += mebel_hlam(1560, 1000, 360, t, 67)
    s += ramka_pp("levo", "#0d0906", .52)
    s += vinetka(.5)
    return s


def tri_okna_zakleeny(t):
    """Три старых деревянных окна в ряд, заклеенных тремя способами."""
    s = f'<rect width="{W}" height="{H}" fill="#5c6a74"/>'
    s += kladka(-20, -20, W + 40, H + 40, 92, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#2b3340" opacity=".35"/>'
    for i in range(3):
        x = 70 + i * 610
        vid = (f'<rect x="{x+30}" y="230" width="460" height="560" fill="#9fb8cc"/>'
               + f'<rect x="{x+30}" y="640" width="460" height="150" fill="#cfd8e6"/>')
        s += okno_izby(x + 30, 230, 460, 560, t, vid=vid, moroz=.3)
        if i == 0:   # бумажные полоски
            for j, (px, py, pw, ph) in enumerate(((x + 20, 490, 480, 46), (x + 240, 240, 46, 540))):
                s += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="url(#list)" opacity=".95" {o(5)}/>'
            ug = 4 * A.w(t, 3.4, .1)
            s += (f'<g transform="rotate({ug:.1f} {x+460} 260)">'
                  f'<path d="M{x+420},240 h90 l-8,120 h-74 Z" fill="url(#list)" opacity=".95" {o(4)}/></g>')
        elif i == 1:  # вата между рамами
            r = random.Random(251)
            for j in range(8):
                s += (f'<ellipse cx="{x+70+j*58}" cy="{770+8*A.w(t,6+j*.3,j*.1):.0f}" rx="{r.uniform(34,46):.0f}"'
                      f' ry="{r.uniform(22,30):.0f}" fill="url(#sneg)" {o(4)}/>')
        else:         # газета
            for j in range(2):
                s += (f'<rect x="{x+20+j*240}" y="{250+j*300}" width="240" height="260" rx="6"'
                      f' fill="url(#list)" opacity=".92" {o(5)}/>')
                for q in range(8):
                    s += (f'<line x1="{x+40+j*240}" y1="{280+j*300+q*30}" x2="{x+230+j*240}"'
                          f' y2="{280+j*300+q*30}" stroke="#8a8070" stroke-width="4" opacity=".7"/>')
        s += teplo(x + 260, 520, 300, 300, .4)
    s += f'<rect y="840" width="{W}" height="240" fill="url(#derev)" {o(6)}/>'
    s += vinetka(.42)
    return s


def albom(t):
    """Полка с детскими книгами: корешки плотно, лампа, одна книга вынута."""
    s = brevna(-20, -20, W + 40, H + 40, 106)
    s += f'<rect width="{W}" height="{H}" fill="#1c1824" opacity=".44"/>'
    s += lampa(780, 420, t, .95, True)
    s += teplo(520, 470, 520, 400, .62)
    # две полки с книгами
    for ryad, y in enumerate((440, 760)):
        s += polka(80, y, 640)
        r = random.Random(151 + ryad)
        x = 110
        i = 0
        while x < 690:
            w_ = r.choice((42, 54, 64))
            h_ = r.choice((150, 170, 190))
            c = r.choice((TKAN, TKAN2, "#c9823a", ZEL, "#6a4a7a", "#2f6b78"))
            nak = r.choice((0, 0, 0, 7))
            s += (f'<g transform="rotate({nak} {x+w_/2:.0f} {y})">'
                  f'<rect x="{x}" y="{y-h_}" width="{w_}" height="{h_}" rx="5"'
                  f' fill="{c}" {o(5)}/>'
                  f'<rect x="{x+6}" y="{y-h_+14}" width="{w_-12}" height="10" rx="4"'
                  f' fill="#f2e2bc" opacity=".7"/>'
                  f'<rect x="{x+6}" y="{y-40}" width="{w_-12}" height="8" rx="4"'
                  f' fill="#f2e2bc" opacity=".5"/></g>')
            x += w_ + 6
            i += 1
    # одна книга вынута и лежит раскрытой на полке: страница шевелится
    kach = 2.0 * A.w(t, 3.8)
    s += (f'<g transform="rotate({kach*.3:.2f} 420 470)">'
          f'<path d="M300,470 q120,-40 240,0 l0,-50 q-120,-36 -240,0 Z" fill="url(#list)" {o(6)}/>'
          f'<g transform="rotate({kach:.2f} 420 430)">'
          f'<path d="M420,424 q62,-22 122,0 l0,46 q-60,-20 -122,0 Z" fill="#faf4e2" {o(4)}/></g></g>')
    s += f'<g opacity=".35">{par(520, 860, t, 4, .3, 300, .18, 2.2)}</g>'
    s += kot(900, 900, t, .95, "#4a4038", True)
    s += mebel_hlam(1400, 960, 520, t, 153)
    s += ramka_pp("levo", "#0c0a12", .46)
    s += vinetka(.46)
    return s


def okno_snaruzhi(t):
    """Снаружи зимний дом: за окном две фигуры в РАЗНЫХ углах комнаты."""
    s = nebo("noch", t, True, 73)
    s += SL(Z_DAL, ulica_dal(1040, 720, 880, t, True, 91))
    s += brevna(-20, 240, 940, 720, 96)
    s += (f'<path d="M-60,250 L430,78 L920,250 Z" fill="#46342a" {o(8)}/>'
          f'<path d="M-60,250 L430,78 L920,250 Z" fill="url(#sneg)" opacity=".5"/>')
    raz = 1.0 + .35 * A.w(t, 9.0)
    vid = (f'<rect x="150" y="380" width="620" height="420" fill="#f0d79c"/>'
           + siluet(230 - 18 * raz, 790, 300, "#7a5333", .9)
           + siluet(690 + 18 * raz, 790, 290, "#6d4a2e", .9)
           + f'<rect x="440" y="520" width="40" height="280" fill="#c39a60" opacity=".5"/>')
    s += okno_izby(150, 380, 620, 420, t, vid, moroz=.45, svet=True)
    s += teplo(460, 580, 480, 380, .45)
    # наличник и сосулька
    s += (f'<path d="M120,352 h680 l-26,36 h-628 Z" fill="url(#derev)" {o(6)}/>')
    for i, x in enumerate((220, 400, 620)):
        dl = 40 + 16 * abs(A.w(t, 7.0, i * .3))
        s += (f'<path d="M{x},388 l14,0 l-7,{dl:.0f} Z" fill="url(#led)" opacity=".9" {o(3)}/>')
    s += sneg_lezhit(956, 26)
    s += f'<g opacity=".85">{sneg_letit(t, 52, 77, .8, .95)}</g>'
    s += SL(Z_PERED, pleten(-40, 880, 1000, 170, 12))
    s += ramka_pp("oba", "#070910", .5)
    s += vinetka(.5)
    return s


# ═══════════════ ДЕКОРАЦИИ «14 ноября — Кузьминки» (19 новых) ═══════════════
# Главное — в левой полосе 0-830: правую половину занимает окно вставки.
# В каждой минимум три живых элемента (R-0006).

def kuznya(t):
    """Кузня: горн слева во всю высоту, наковальня справа, подковы между ними."""
    s = kladka(-20, -20, W + 40, H + 40, 86)
    s += f'<rect width="{W}" height="{H}" fill="#2a2119" opacity=".5"/>'
    s += polovicy(H - 90, "url(#dosk)")
    s += teplo(260, 560, 700, 520, .95)
    s += f'<path d="M-20,300 L520,300 L420,40 L60,40 Z" fill="#241c16" {o(8)}/>'
    s += dym(250, 50, t, 6, .2, 300, .28)
    s += ten(260, 1000, 280, 30, .6)
    s += f'<path d="M20,1000 L20,560 q240,-56 480,0 L500,1000 Z" fill="url(#kamen)" {o(9)}/>'
    s += f'<rect x="52" y="492" width="420" height="80" rx="14" fill="url(#chug)" {o(7)}/>'
    s += ugli(90, 524, 350, t, 10, 4)
    s += ogon(262, 516, t, 1.6, .2, 9)
    s += iskra_let(t, 262, 476, 16, 6, 500, .62)
    # подковы выше наковальни, на свободной стене
    for i, (x, y, r) in enumerate(((600, 180, 48), (720, 300, 44))):
        dy = 5 * A.w(t, .8, i * .3)
        s += (f'<path d="M{x},{y+dy:.0f} a{r},{r} 0 1 1 {r*1.4:.0f},0 l-{r*.4:.0f},0'
              f' a{r*.6:.0f},{r*.6:.0f} 0 1 0 -{r*.6:.0f},0 Z" fill="url(#zhel)" {o(6)}/>')
    # наковальня справа, первый план
    s += ten(660, 1020, 220, 26, .6)
    s += (f'<path d="M500,790 h340 l-40,54 h-260 Z" fill="url(#zhel)" {o(8)}/>'
          f'<rect x="586" y="844" width="170" height="54" fill="url(#chug)" {o(7)}/>'
          f'<path d="M528,898 h284 l-28,62 h-228 Z" fill="url(#chug)" {o(7)}/>'
          f'<path d="M496,794 q-74,20 -76,56 q42,14 78,-18 Z" fill="url(#zhel)" {o(6)}/>')
    kach_m = 1.6 * A.w(t, 1.1)
    s += (f'<g transform="rotate({kach_m:.2f} 668 776)">'
          f'<rect x="560" y="750" width="210" height="34" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="760" y="724" width="92" height="80" rx="12" fill="url(#chug)" {o(7)}/></g>')
    s += f'<g opacity=".45">{par(262, 450, t, 4, .4, 220, .3)}</g>'
    s += mebel_hlam(1580, 1010, 320, t, 29)
    s += ramka_pp("levo", "#0f0b08", .55)
    s += vinetka(.46)
    return s


def tri_yaica(t):
    """Тёмный стол, холстина, ТРИ ЯЙЦА крупно. Свеча сбоку."""
    s = f'<rect width="{W}" height="{H}" fill="#1b1510"/>'
    s += teplo(420, 620, 700, 460, .8)
    s += f'<rect y="{H-420}" width="{W}" height="420" fill="url(#derev)" {o(0)}/>'
    s += doski(-20, H - 420, W + 40, 440, 96, False)
    s += ten(420, 880, 380, 34, .6)
    s += f'<path d="M60,600 q360,-56 720,0 q-50,210 -360,210 q-310,0 -360,-210 Z" fill="url(#rush)" {o(7)}/>'
    for i, (x, y, r) in enumerate(((236, 660, 92), (420, 700, 100), (604, 662, 88))):
        dy = 3.0 * A.w(t, .7, i * .4)
        s += ten(x, y + r * .78, r * .9, 18, .45)
        s += (f'<ellipse cx="{x}" cy="{y+dy:.0f}" rx="{r*.76:.0f}" ry="{r:.0f}"'
              f' fill="url(#krem)" {o(6)}/>'
              f'<ellipse cx="{x-r*.26:.0f}" cy="{y-r*.32+dy:.0f}" rx="{r*.22:.0f}" ry="{r*.3:.0f}"'
              f' fill="#fffaf0" opacity=".55"/>')
    s += svecha(790, 640, t, .0, 1.5)
    s += f'<g opacity=".5">{par(420, 600, t, 3, .35, 170, .26)}</g>'
    s += mebel_hlam(1560, 1020, 330, t, 17)
    s += vinetka(.52)
    return s


def mogila(t):
    """Холм и КРУПНЫЙ крест с двумя именами. Ворон садится на перекладину."""
    s = nebo("sumer", t, False)
    s += oblaka(t, 190, 5, 21, .5, "#cbd4e0", 9)
    s += f'<path d="M0,700 Q480,656 960,688 Q1440,720 1920,682 L1920,1080 L0,1080 Z" fill="#6d6b55" {o(5)}/>'
    s += f'<path d="M0,820 Q560,782 1120,820 L1120,1080 L0,1080 Z" fill="#5d5b47" {o(4)}/>'
    for i in range(34):
        x = 40 + i * 46
        a = 9 * A.w(t, 1.1, i * .17)
        s += (f'<path d="M{x},{900+(i%5)*14} q{a:.0f},-34 {a*1.5:.0f},-62"'
              f' stroke="{TRAVA}" stroke-width="5" fill="none" opacity=".75"/>')
    s += ten(400, 940, 320, 32, .5)
    s += f'<path d="M100,940 q300,-130 600,0 Z" fill="#6b6650" {o(7)}/>'
    # крест во всю высоту полосы
    s += (f'<rect x="366" y="180" width="68" height="770" fill="url(#derev)" {o(8)}/>'
          f'<rect x="180" y="330" width="440" height="62" rx="10" fill="url(#derev)" {o(8)}/>')
    s += (f'<text x="400" y="520" font-family="DejaVu Serif, Georgia, serif" font-size="68"'
          f' fill="{KREM}" text-anchor="middle" opacity=".9">КУЗЬМА</text>'
          f'<text x="400" y="606" font-family="DejaVu Serif, Georgia, serif" font-size="68"'
          f' fill="{KREM}" text-anchor="middle" opacity=".9">ДЕМЬЯН</text>')
    vz = -8 * A.w(t, .5)
    s += f'<g transform="translate(0,{vz:.0f})">{ptica(600, 322, t, 1.25, "#23262c", .3, "#1a1d22")}</g>'
    s += f'<g opacity=".4">{tuman(t, 800, .4)}</g>'
    s += ulica_dal(1480, 660, 820, t, False, 23)
    s += vinetka(.44)
    return s


def nishchiy(t):
    """Ворота: хозяйка на пороге и сгорбленный путник, между ними узелок."""
    s = nebo("sumer", t, False)
    s += f'<path d="M0,790 L1920,766 L1920,1080 L0,1080 Z" fill="#6a6252" {o(5)}/>'
    s += sneg_lezhit(802, 20)
    s += pleten(760, 600, 1140, 210, 11)
    for x in (60, 720):
        s += f'<rect x="{x}" y="300" width="62" height="560" fill="url(#derev)" {o(8)}/>'
    s += f'<path d="M44,300 q350,-70 712,0 l0,46 q-370,-64 -712,0 Z" fill="url(#derev)" {o(7)}/>'
    # хозяйка слева у порога, путник справа, оба со спины-вполоборота
    s += ten(200, 980, 120, 22, .45)
    s += siluet(200, 980, 560, "#2b2630", 1.0, True)
    s += ten(560, 990, 130, 24, .5)
    s += f'<g transform="rotate(7 560 990)">{siluet(560, 990, 540, "#201d26", 1.0, True)}</g>'
    # узелок между ними — он и есть главное
    uz = 7 * A.w(t, 1.1)
    s += (f'<path d="M330,{700+uz:.0f} q90,-66 180,0 q-26,104 -90,104 q-64,0 -90,-104 Z"'
          f' fill="url(#rush)" {o(7)}/>'
          f'<path d="M398,{688+uz:.0f} q22,-40 46,-6 q-22,16 -46,6 Z" fill="{DOSKA2}" {o(5)}/>'
          f'<path d="M352,{740+uz:.0f} q68,24 136,0" stroke="{DOSKA2}" stroke-width="7" fill="none"/>')
    # котомка путника
    kx = 8 * A.w(t, .9, .4)
    s += (f'<path d="M{660+kx:.0f},720 q76,-18 98,76 q-50,116 -122,66 Z" fill="{TKAN}" {o(6)}/>')
    s += f'<g opacity=".7">{sneg_letit(t, 28, 13, .7, .5)}</g>'
    s += f'<g opacity=".45">{par(380, 640, t, 3, .4, 150, .3)}</g>'
    s += ulica_dal(1460, 700, 860, t, True, 19)
    s += vinetka(.46)
    return s


def dva_lekarya(t):
    """Дорога, ДВЕ КРУПНЫЕ фигуры путников уходят от нас."""
    s = nebo("zakat", t, False)
    s += oblaka(t, 200, 5, 29, .45, "#e8d6c0", 10)
    s += f'<path d="M0,700 Q480,640 960,686 Q1440,732 1920,680 L1920,1080 L0,1080 Z" fill="#7b7254" {o(5)}/>'
    s += f'<path d="M0,800 Q560,756 1120,800 L1120,1080 L0,1080 Z" fill="#6a6246" {o(4)}/>'
    s += (f'<path d="M140,1080 Q330,860 470,716 L660,716 Q540,880 760,1080 Z"'
          f' fill="#8d8160" {o(0)}/>')
    for i in range(9):
        p = ((t * .18) + i / 9.0) % 1.0
        s += (f'<ellipse cx="{520-80*p:.0f}" cy="{730+330*p:.0f}" rx="{10+40*p:.0f}" ry="{4+12*p:.0f}"'
              f' fill="#a79a74" opacity="{.5*(1-p):.2f}"/>')
    for i, (x, h_, y) in enumerate(((380, 560, 1000), (580, 500, 960))):
        kach = 2.6 * A.w(t, 1.0, i * .5)
        s += ten(x, y, 96, 18, .42)
        s += f'<g transform="rotate({kach:.2f} {x} {y})">{siluet(x, y, h_, "#2a2630")}</g>'
        s += (f'<line x1="{x+92}" y1="{y-h_*.75:.0f}" x2="{x+74}" y2="{y+4}"'
              f' stroke="{DOSKA2}" stroke-width="11" stroke-linecap="round"/>')
    for i in range(16):
        x = 20 + i * 54
        a = 8 * A.w(t, 1.3, i * .2)
        s += (f'<path d="M{x},{980+(i%4)*22} q{a:.0f},-34 {a*1.4:.0f},-60"'
              f' stroke="{TRAVA}" stroke-width="5" fill="none" opacity=".7"/>')
    s += f'<circle cx="{1180+70*A.w(t,.3):.0f}" cy="{210+18*A.w(t,.45):.0f}" r="7" fill="#2b2b33" opacity=".6"/>'
    s += ulica_dal(1470, 680, 860, t, False, 27)
    s += vinetka(.42)
    return s


def bolnaya(t):
    """Тёмная комната, КРУПНАЯ постель, свеча у изголовья, тень на стене."""
    s = brevna(-20, -20, W + 40, H + 40, 116)
    s += f'<rect width="{W}" height="{H}" fill="#120f14" opacity=".6"/>'
    s += polovicy(H - 90)
    s += teplo(380, 520, 560, 420, .85)
    s += ten(440, 1000, 420, 30, .55)
    s += f'<rect x="60" y="760" width="780" height="200" rx="14" fill="url(#derev)" {o(8)}/>'
    s += f'<rect x="30" y="470" width="62" height="490" rx="12" fill="url(#derev)" {o(7)}/>'
    dy = 6 * A.w(t, .55)
    s += (f'<path d="M100,{772+dy:.0f} q240,-74 560,-14 q54,92 14,194 l-574,0 Z"'
          f' fill="{TKAN2}" {o(7)}/>')
    s += f'<ellipse cx="186" cy="{726+dy:.0f}" rx="96" ry="62" fill="url(#rush)" {o(6)}/>'
    s += f'<circle cx="218" cy="{706+dy:.0f}" r="50" fill="#d9bb94" {o(6)}/>'
    s += f'<rect x="700" y="640" width="130" height="120" rx="10" fill="url(#derev)" {o(7)}/>'
    s += svecha(765, 634, t, .2, 1.5)
    s += (f'<path d="M600,140 q110,300 40,560 l-96,0 q54,-300 -40,-554 Z"'
          f' fill="#000" opacity="{.2+.1*abs(A.w(t,1.4)):.2f}"/>')
    s += f'<g opacity=".45">{par(220, 680, t, 3, .4, 150, .25)}</g>'
    s += mebel_hlam(1560, 1010, 340, t, 33)
    s += ramka_pp("levo", "#0c0a0d", .55)
    s += vinetka(.5)
    return s


def verblyud(t):
    """Верблюд у ворот, пыль, низкое солнце, застывшие силуэты людей."""
    s = nebo("zakat", t, False)
    s += oblaka(t, 180, 4, 35, .4, "#f0dcc0", 8)
    s += f'<path d="M0,790 L1920,766 L1920,1080 L0,1080 Z" fill="#9b8a63" {o(5)}/>'
    # ворота справа
    s += f'<rect x="700" y="380" width="44" height="420" fill="url(#derev)" {o(7)}/>'
    s += f'<path d="M690,380 q140,-40 300,0 l0,34 q-160,-36 -300,0 Z" fill="url(#derev)" {o(6)}/>'
    # верблюд
    s += ten(400, 812, 230, 24, .5)
    mig = 1.0 if A.w(t, .7) > -.9 else .2
    zhuy = 3.4 * A.w(t, 2.1)
    s += (f'<path d="M190,800 q-14,-150 90,-176 q60,-70 150,-40 q90,-20 130,60'
          f' q70,20 60,156 Z" fill="#c69a63" {o(7)}/>'
          f'<path d="M250,636 q46,-78 92,-6 q-46,24 -92,6 Z" fill="#b98a55" {o(5)}/>'
          f'<path d="M430,620 q50,-74 96,-4 q-48,26 -96,4 Z" fill="#b98a55" {o(5)}/>')
    for i, x in enumerate((230, 300, 450, 520)):
        sh = 5 * A.w(t, .9, i * .25)
        s += (f'<rect x="{x}" y="{790+sh:.0f}" width="26" height="110" rx="8"'
              f' fill="#b58d5a" {o(5)}/>')
    # шея и голова
    s += (f'<path d="M520,660 q110,-70 150,-180 q50,10 40,70 q-20,110 -130,170 Z"'
          f' fill="#c69a63" {o(6)}/>')
    s += (f'<g transform="rotate({zhuy:.1f} 690 470)">'
          f'<ellipse cx="700" cy="462" rx="66" ry="42" fill="#c69a63" {o(6)}/>'
          f'<path d="M744,470 q40,8 34,34 q-36,10 -50,-14 Z" fill="#b58d5a" {o(5)}/>'
          f'<circle cx="716" cy="442" r="7" fill="{K}" opacity="{mig:.2f}"/>'
          f'<path d="M662,424 q14,-30 36,-8" stroke="{K}" stroke-width="5" fill="none"/></g>')
    # пыль и силуэты
    s += f'<g opacity=".35">{tuman(t, 840, .45, "#e0cda8")}</g>'
    for i, x in enumerate((880, 960, 1030)):
        s += siluet(x, 820, 250 - i * 12, "#3a3026", .75)
    s += f'<g opacity=".3">{sneg_letit(t, 16, 41, .35, .3)}</g>'
    s += ulica_dal(1420, 700, 900, t, False, 31)
    s += vinetka(.44)
    return s


def plug_borozda(t):
    """Поле, КРУПНЫЙ плуг с лемехом и отвалом, борозда к горизонту."""
    s = nebo("den", t, False)
    s += oblaka(t, 160, 6, 13, .55, "#e6edf4", 12)
    s += f'<path d="M0,660 Q480,628 960,652 Q1440,676 1920,644 L1920,1080 L0,1080 Z" fill="#6b5c42" {o(5)}/>'
    s += (f'<path d="M-60,1080 Q320,840 860,668 L980,672 Q500,860 240,1080 Z"'
          f' fill="#3f3326" {o(0)}/>')
    for i in range(12):
        p = ((t * .16) + i / 12.0) % 1.0
        s += (f'<ellipse cx="{860-760*p:.0f}" cy="{672+380*p:.0f}" rx="{8+56*p:.0f}" ry="{4+16*p:.0f}"'
              f' fill="#8a7450" opacity="{.45*(1-p):.2f}"/>')
    # грядиль и две рукояти
    s += (f'<path d="M60,660 L470,820" stroke="{DOSKA2}" stroke-width="30" stroke-linecap="round"/>'
          f'<path d="M90,640 L160,700" stroke="{DOSKA2}" stroke-width="20" stroke-linecap="round"/>')
    s += ten(430, 1010, 300, 28, .5)
    # корпус плуга: отвал и лемех
    s += (f'<path d="M300,820 q180,-10 280,70 q-60,120 -210,120 q-130,-20 -70,-190 Z"'
          f' fill="url(#zhel)" {o(9)}/>'
          f'<path d="M560,884 q90,10 112,80 q-96,46 -170,2 Z" fill="url(#chug)" {o(8)}/>'
          f'<path d="M320,836 q150,0 240,66" stroke="#cfd6dd" stroke-width="8" fill="none" opacity=".5"/>')
    s += f'<circle cx="286" cy="930" r="56" fill="none" stroke="{DOSKA2}" stroke-width="18"/>'
    for i in range(5):
        x = 760 + i * 94 + 60 * A.w(t, .32, i * .3)
        y = 280 + 24 * A.w(t, .5, i * .4)
        s += (f'<path d="M{x:.0f},{y:.0f} q18,-16 34,0 q16,-16 34,0" stroke="#3a3b44"'
              f' stroke-width="5" fill="none" opacity=".65"/>')
    for i in range(14):
        x = 24 + i * 60
        a = 7 * A.w(t, 1.2, i * .2)
        s += (f'<path d="M{x},{1040+(i%3)*16} q{a:.0f},-30 {a*1.4:.0f},-54"'
              f' stroke="{TRAVA}" stroke-width="5" fill="none" opacity=".6"/>')
    s += ulica_dal(1470, 630, 860, t, False, 37)
    s += vinetka(.4)
    return s


def svadba_kuznya(t):
    """КРУПНАЯ наковальня, на ней два кольца; в глубине пылает горн."""
    s = kladka(-20, -20, W + 40, H + 40, 86)
    s += f'<rect width="{W}" height="{H}" fill="#2a2119" opacity=".46"/>'
    s += polovicy(H - 90, "url(#dosk)")
    s += teplo(420, 620, 620, 440, .9)
    s += f'<path d="M540,820 L540,520 q200,-40 400,0 L940,820 Z" fill="url(#kamen)" {o(8)}/>'
    s += ugli(580, 508, 320, t, 9, 9)
    s += ogon(740, 504, t, 1.2, .4, 8)
    s += iskra_let(t, 740, 470, 14, 11, 420, .55)
    # наковальня крупно
    s += ten(330, 1000, 240, 28, .6)
    s += (f'<path d="M140,810 h380 l-44,56 h-292 Z" fill="url(#zhel)" {o(8)}/>'
          f'<rect x="236" y="866" width="190" height="56" fill="url(#chug)" {o(7)}/>'
          f'<path d="M176,922 h316 l-32,64 h-252 Z" fill="url(#chug)" {o(7)}/>')
    for i, x in enumerate((252, 406)):
        bl = .45 + .5 * abs(A.w(t, 1.9, i * .5))
        s += (f'<circle cx="{x}" cy="760" r="62" fill="none" stroke="url(#zol)" stroke-width="24"/>'
              f'<circle cx="{x}" cy="760" r="62" fill="none" stroke="{SVET}" stroke-width="7"'
              f' opacity="{bl:.2f}"/>')
    s += (f'<rect x="470" y="792" width="150" height="26" rx="7" fill="url(#derev)" {o(6)}/>'
          f'<rect x="606" y="770" width="70" height="62" rx="10" fill="url(#chug)" {o(7)}/>')
    s += f'<g opacity=".4">{dym(740, 460, t, 4, .22, 320, .3)}</g>'
    s += mebel_hlam(1570, 1010, 330, t, 41)
    s += ramka_pp("levo", "#0f0b08", .5)
    s += vinetka(.46)
    return s


def lunnyj_svet(t):
    """Комната ночью, окно настежь, холодная лунная полоса на полу."""
    s = brevna(-20, -20, W + 40, H + 40, 116)
    s += f'<rect width="{W}" height="{H}" fill="#0f1526" opacity=".72"/>'
    s += polovicy(H - 150)
    # окно
    s += f'<rect x="150" y="190" width="430" height="440" rx="10" fill="#0a0f1c" {o(8)}/>'
    s += f'<rect x="178" y="218" width="374" height="384" fill="#1b2a44" {o(5)}/>'
    s += f'<circle cx="300" cy="330" r="62" fill="#e7eefc" opacity=".92"/>'
    s += f'<circle cx="300" cy="330" r="98" fill="url(#holod)"/>'
    for i in range(9):
        s += (f'<circle cx="{200+i*42}" cy="{250+(i%4)*52}" r="2.6" fill="#dbe6f7"'
              f' opacity="{.3+.5*abs(A.w(t,1.1,i*.3)):.2f}"/>')
    # створка качается
    ug = 3.2 * A.w(t, .55)
    s += (f'<g transform="rotate({ug:.2f} 580 400)">'
          f'<rect x="578" y="206" width="150" height="408" rx="8" fill="#16203a" {o(7)}/>'
          f'<rect x="596" y="228" width="114" height="364" fill="{STEKLO}" opacity=".22"/></g>')
    # лунная полоса на полу
    sd = 14 * A.w(t, .3)
    s += (f'<path d="M{190+sd:.0f},640 L{560+sd:.0f},640 L{740+sd:.0f},1080 L{60+sd:.0f},1080 Z"'
          f' fill="#cfe0fa" opacity=".16"/>')
    # занавеска летит
    s += zanaveska(120, 170, 470, 210, "#cdd8ea", t, 1)
    s += f'<g opacity=".5">{par(300, 620, t, 3, .4, 140, .22)}</g>'
    s += mebel_hlam(1500, 1000, 400, t, 43)
    s += ramka_pp("levo", "#070a12", .6)
    s += vinetka(.5)
    return s


def skorlupa(t):
    """Грядка у дома: миска со скорлупой, совок, ростки. Рук в кадре нет."""
    s = nebo("den", t, False)
    s += f'<path d="M0,480 L1920,462 L1920,1080 L0,1080 Z" fill="#6e6a4e" {o(0)}/>'
    s += izba_snaruzhi(1240, 560, 580, t, False, 6)
    s += f'<path d="M0,620 Q480,588 960,614 L1920,596 L1920,1080 L0,1080 Z" fill="#4a3c2c" {o(5)}/>'
    s += f'<path d="M-40,900 q440,-130 880,0 q-440,140 -880,0 Z" fill="#33281d" {o(7)}/>'
    for i in range(12):
        x = 60 + i * 70
        s += (f'<path d="M{x},{858+(i%3)*14} q16,-34 34,0" stroke="#5a4a36" stroke-width="8"'
              f' fill="none" opacity=".7"/>')
    # миска со скорлупой — крупно, первый план
    s += ten(300, 862, 170, 24, .5)
    s += f'<path d="M140,742 q160,-40 320,0 q-30,120 -160,120 q-130,0 -160,-120 Z" fill="url(#glina)" {o(8)}/>'
    for i, (x, y, r) in enumerate(((210, 744, 1.1), (300, 730, 1.3), (390, 748, 1.0))):
        dy = 2.4 * A.w(t, .8, i * .4)
        s += (f'<path d="M{x},{y+dy:.0f} q{30*r:.0f},-40 {60*r:.0f},0 q{-30*r:.0f},22 {-60*r:.0f},0 Z"'
              f' fill="#f3ead6" {o(5)}/>')
    # совок воткнут в землю
    s += (f'<path d="M560,880 q70,-30 120,16 q-50,56 -120,26 Z" fill="url(#zhel)" {o(7)}/>'
          f'<line x1="650" y1="856" x2="742" y2="700" stroke="{DOSKA2}" stroke-width="18"'
          f' stroke-linecap="round"/>')
    # ростки и червяк
    for i in range(6):
        x = 160 + i * 118
        a = 8 * A.w(t, 1.4, i * .3)
        s += (f'<path d="M{x},900 q{a:.0f},-60 {a*1.3:.0f},-96" stroke="{ZEL2}" stroke-width="10"'
              f' fill="none"/>'
              f'<path d="M{x+a*1.3:.0f},{804:.0f} q26,-18 44,2 q-24,20 -44,-2 Z" fill="{ZEL2}" {o(4)}/>')
    s += (f'<path d="M640,980 q28,{-16+9*A.w(t,1.6):.0f} 56,0 q28,16 56,0" stroke="#b4766a"'
          f' stroke-width="10" fill="none" opacity=".85"/>')
    p = (t * .22) % 1.0
    s += (f'<path d="M{800+80*p:.0f},{540+340*p:.0f} q28,-26 50,6 q-26,28 -50,-6 Z"'
          f' fill="{ORA}" opacity="{.9-.3*p:.2f}"'
          f' transform="rotate({p*220:.0f} {825+80*p:.0f} {552+340*p:.0f})"/>')
    s += vinetka(.4)
    return s


def yaschik_instrument(t):
    """Сарай: открытый ящик, инструмент светлым металлом на тёмном войлоке."""
    s = doski(-20, -20, W + 40, H + 40, 118, True)
    s += f'<rect width="{W}" height="{H}" fill="#241a12" opacity=".38"/>'
    s += polovicy(H - 90, "url(#dosk)")
    s += luch(420, 0, 460, 820, t, .26)
    s += teplo(420, 700, 520, 320, .5)
    s += ten(420, 1010, 400, 26, .5)
    s += f'<rect x="20" y="820" width="820" height="52" rx="10" fill="url(#derev)" {o(8)}/>'
    for x in (80, 740):
        s += f'<rect x="{x}" y="872" width="52" height="180" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="90" y="540" width="660" height="280" rx="14" fill="url(#dosk)" {o(8)}/>'
    s += f'<rect x="124" y="576" width="592" height="210" fill="#2e2219" {o(6)}/>'
    s += (f'<rect x="402" y="420" width="40" height="124" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="262" y="396" width="320" height="32" rx="10" fill="url(#derev)" {o(6)}/>')
    # молоток
    s += (f'<rect x="150" y="660" width="210" height="26" rx="8" fill="url(#derev)" {o(5)}/>'
          f'<path d="M352,632 h86 q22,0 22,22 v34 q0,22 -22,22 h-86 Z" fill="url(#zhel)" {o(6)}/>')
    # стамеска
    s += (f'<rect x="150" y="724" width="170" height="22" rx="7" fill="url(#derev)" {o(5)}/>'
          f'<path d="M320,722 l96,14 l-96,16 Z" fill="url(#zhel)" {o(5)}/>')
    # рубанок
    s += (f'<path d="M470,700 q130,-26 200,22 l0,70 q-108,-36 -200,-16 Z" fill="url(#derev)" {o(7)}/>'
          f'<path d="M520,712 l100,20 l-4,28 l-98,-20 Z" fill="url(#zhel)" {o(5)}/>')
    for i in range(6):
        x = 120 + i * 118
        a = 6 * A.w(t, 1.5, i * .3)
        s += (f'<path d="M{x},806 q26,{-18+a:.0f} 56,2 q-28,16 -56,-2 Z" fill="#e0c79a"'
              f' opacity=".8"/>')
    s += (f'<line x1="790" y1="240" x2="790" y2="{320+8*A.w(t,.9):.0f}" stroke="{ZHELEZ}"'
          f' stroke-width="8"/>')
    s += f'<g opacity=".5">{par(420, 680, t, 3, .35, 170, .2)}</g>'
    s += mebel_hlam(1580, 1010, 320, t, 47)
    s += ramka_pp("levo", "#0d0a07", .5)
    s += vinetka(.46)
    return s


def gus_na_ldu(t):
    """Гусь стоит на тонком льду у берега, переступает лапами."""
    s = nebo("den", t, False)
    s += oblaka(t, 150, 5, 51, .5, "#e3ebf3", 10)
    s += f'<path d="M0,560 L1920,546 L1920,700 L0,716 Z" fill="#5c6552" {o(0)}/>'
    s += f'<path d="M0,700 L1920,676 L1920,1080 L0,1080 Z" fill="url(#led)" {o(0)}/>'
    # полыньи и блики
    for i in range(7):
        x = 120 + i * 250
        s += (f'<ellipse cx="{x}" cy="{880+(i%3)*50}" rx="{70+(i%4)*26}" ry="{18+(i%3)*8}"'
              f' fill="{VODA}" opacity=".45"/>')
    for i in range(10):
        s += (f'<line x1="{80+i*190}" y1="{760+(i%4)*60}" x2="{180+i*190}" y2="{764+(i%4)*60}"'
              f' stroke="#ffffff" stroke-width="4" opacity="{.2+.3*abs(A.w(t,1.2,i*.3)):.2f}"/>')
    # гусь
    sh = 6 * A.w(t, 1.1)
    kr = 10 * A.w(t, .8, .3)
    s += ten(400, 880, 120, 18, .35)
    s += (f'<g transform="translate({sh:.0f},0)">'
          f'<ellipse cx="400" cy="790" rx="150" ry="92" fill="#f4f1e8" {o(6)}/>'
          f'<path d="M520,760 q90,-130 48,-200 q-74,-12 -84,76 q-10,70 -6,120 Z" fill="#f4f1e8" {o(6)}/>'
          f'<ellipse cx="548" cy="556" rx="46" ry="34" fill="#f4f1e8" {o(5)}/>'
          f'<path d="M588,560 q40,6 34,28 q-34,12 -46,-10 Z" fill="{ORA}" {o(4)}/>'
          f'<circle cx="562" cy="542" r="6" fill="{K}"/>'
          f'<path d="M300,744 q{-30+kr:.0f},56 24,96 q40,-44 18,-104 Z" fill="#e6e1d4" {o(5)}/>'
          f'<path d="M352,880 l0,46 l-30,16" stroke="{ORA}" stroke-width="9" fill="none"/>'
          f'<path d="M444,880 l0,46 l30,16" stroke="{ORA}" stroke-width="9" fill="none"/></g>')
    s += f'<g opacity=".45">{par(400, 720, t, 4, .4, 160, .25)}</g>'
    s += f'<g opacity=".4">{tuman(t, 660, .4)}</g>'
    s += ulica_dal(1480, 600, 820, t, True, 53)
    s += vinetka(.4)
    return s


def voronyo(t):
    """Голое дерево и поле, вороны на ветвях и в небе."""
    s = nebo("den", t, False)
    s += f'<rect width="{W}" height="{H}" fill="#5c6472" opacity=".35"/>'
    s += oblaka(t, 180, 6, 57, .6, "#aeb8c4", 14)
    s += f'<path d="M0,800 Q480,764 960,792 Q1440,820 1920,784 L1920,1080 L0,1080 Z" fill="#6a6450" {o(5)}/>'
    # дерево
    s += f'<path d="M360,900 q-24,-260 10,-420 q40,160 20,420 Z" fill="#3b2f26" {o(7)}/>'
    vetvi = ((380, 560, 190, 420), (372, 620, -170, 500), (384, 480, 150, 380),
             (368, 700, -150, 620), (388, 420, 120, 330))
    for i, (x1, y1, dx, y2) in enumerate(vetvi):
        a = 5 * A.w(t, .7, i * .3)
        s += (f'<path d="M{x1},{y1} q{dx*.5+a:.0f},{-40:.0f} {dx+a*1.6:.0f},{y2-y1}"'
              f' stroke="#3b2f26" stroke-width="{11-i}" fill="none"/>')
    # вороны на ветвях
    for i, (x, y) in enumerate(((520, 520), (240, 600), (560, 428), (226, 686), (490, 360))):
        s += f'<g transform="translate(0,{3*A.w(t,.9,i*.4):.0f})">{ptica(x, y, t, .72, "#20232a", i*.3, "#171a1f")}</g>'
    # стая в небе
    for i in range(16):
        x = 700 + (i * 73 + 120 * A.w(t, .22, i * .19)) % 1180
        y = 160 + (i % 6) * 54 + 26 * A.w(t, .5, i * .3)
        s += (f'<path d="M{x:.0f},{y:.0f} q14,-12 26,0 q12,-12 26,0" stroke="#22252c"'
              f' stroke-width="5" fill="none" opacity=".75"/>')
    for i in range(18):
        x = 30 + i * 48
        a = 9 * A.w(t, 1.3, i * .2)
        s += (f'<path d="M{x},{960+(i%4)*18} q{a:.0f},-32 {a*1.4:.0f},-58"'
              f' stroke="#6f6a4a" stroke-width="5" fill="none" opacity=".7"/>')
    s += vinetka(.44)
    return s


def vishnya_list(t):
    """Голая вишня, на ветке один красный лист."""
    s = nebo("rassv", t, False)
    s += oblaka(t, 200, 4, 61, .45, "#e6dfe6", 9)
    s += f'<path d="M0,860 Q480,826 960,852 Q1440,878 1920,844 L1920,1080 L0,1080 Z" fill="#6c6752" {o(5)}/>'
    s += sneg_lezhit(872, 14)
    # ствол и ветви
    s += f'<path d="M300,960 q-20,-300 6,-470 q36,170 22,470 Z" fill="#4a3a33" {o(7)}/>'
    for i, (y1, dx, y2, w_) in enumerate(((620, 230, 470, 10), (680, -190, 540, 9),
                                          (540, 180, 400, 8), (740, -150, 640, 8),
                                          (500, 120, 360, 7))):
        a = 6 * A.w(t, .8, i * .35)
        s += (f'<path d="M318,{y1} q{dx*.5+a:.0f},-40 {dx+a*1.5:.0f},{y2-y1}"'
              f' stroke="#4a3a33" stroke-width="{w_}" fill="none"/>')
        for k in range(3):
            s += (f'<path d="M{318+dx*(.5+k*.16)+a:.0f},{y1-20-k*26} q{18*(1 if dx>0 else -1)},-24'
                  f' {34*(1 if dx>0 else -1)},-36" stroke="#4a3a33" stroke-width="4" fill="none"/>')
    # ОДИН лист
    kach = 11 * A.w(t, 1.6)
    s += (f'<g transform="rotate({kach:.1f} 548 470)">'
          f'<path d="M548,470 q54,-26 76,22 q-44,44 -76,-22 Z" fill="{KRAS}" {o(5)}/>'
          f'<path d="M552,476 q36,10 64,20" stroke="#8c2a1c" stroke-width="4" fill="none"/></g>')
    s += f'<line x1="520" y1="452" x2="550" y2="470" stroke="#4a3a33" stroke-width="5"/>'
    # синица и позёмка
    s += f'<g transform="translate(0,{4*A.w(t,1.0):.0f})">{ptica(236, 662, t, .66, "#d8c24a", .2, "#4f6a7a")}</g>'
    s += f'<g opacity=".55">{sneg_letit(t, 20, 67, .55, .35)}</g>'
    s += ulica_dal(1440, 780, 900, t, True, 59)
    s += vinetka(.42)
    return s


def ferma_kanada(t):
    """Ферма среди полей: деревянный дом, изгородь, флюгер."""
    s = nebo("den", t, False)
    s += oblaka(t, 150, 6, 71, .6, "#eef3f8", 13)
    s += f'<path d="M0,740 Q480,706 960,732 Q1440,758 1920,724 L1920,1080 L0,1080 Z" fill="#8a8a52" {o(5)}/>'
    s += f'<path d="M0,860 Q560,822 1120,862 L1120,1080 L0,1080 Z" fill="#79793f" {o(4)}/>'
    # дом
    s += ten(420, 876, 260, 22, .45)
    s += f'<rect x="200" y="600" width="440" height="280" fill="#a8452f" {o(8)}/>'
    s += f'<path d="M170,604 L420,440 L670,604 Z" fill="#6f3a2a" {o(8)}/>'
    s += doski(200, 600, 440, 280, 56, False, "dosk")
    s += f'<rect width="440" height="280" x="200" y="600" fill="#a8452f" opacity=".55"/>'
    for x in (262, 398, 534):
        s += f'<rect x="{x}" y="662" width="76" height="96" rx="5" fill="{STEKLO}" opacity=".7" {o(5)}/>'
    s += f'<rect x="384" y="786" width="86" height="94" rx="5" fill="#5a2e22" {o(6)}/>'
    # флюгер крутится
    ug = (t * 42) % 360
    s += (f'<line x1="420" y1="440" x2="420" y2="368" stroke="{ZHELEZ}" stroke-width="7"/>'
          f'<g transform="rotate({ug:.0f} 420 368)">'
          f'<path d="M386,368 L454,368 L436,352 L454,368 L436,384" stroke="{CHUGUN}"'
          f' stroke-width="6" fill="none"/></g>')
    # изгородь
    for i in range(12):
        x = 60 + i * 78
        s += f'<rect x="{x}" y="836" width="14" height="110" fill="url(#derev)" {o(4)}/>'
    s += (f'<line x1="60" y1="870" x2="990" y2="862" stroke="{DOSKA2}" stroke-width="10"/>'
          f'<line x1="60" y1="916" x2="990" y2="908" stroke="{DOSKA2}" stroke-width="10"/>')
    # трава волнами
    for i in range(20):
        x = 30 + i * 46
        a = 10 * A.w(t, 1.0, i * .2)
        s += (f'<path d="M{x},{1010+(i%3)*18} q{a:.0f},-34 {a*1.5:.0f},-60"'
              f' stroke="{TRAVA}" stroke-width="5" fill="none" opacity=".7"/>')
    s += ulica_dal(1460, 700, 860, t, False, 73)
    s += vinetka(.4)
    return s


def palata_ukol(t):
    """Палата: КРУПНАЯ кровать, тумбочка с пузырьком и шприцем, светлое окно."""
    s = f'<rect width="{W}" height="{H}" fill="#c3ced3"/>'
    s += f'<rect y="0" width="{W}" height="600" fill="#dfe8ec"/>'
    s += f'<rect y="596" width="{W}" height="16" fill="#9aa8ad"/>'
    s += polovicy(H - 90, "url(#beton)")
    s += f'<rect x="110" y="110" width="460" height="420" rx="10" fill="{STEKLO}" {o(9)}/>'
    s += f'<rect x="142" y="142" width="396" height="356" fill="#eaf4fb" opacity=".9"/>'
    s += f'<line x1="340" y1="110" x2="340" y2="530" stroke="{K}" stroke-width="8"/>'
    s += luch(160, 110, 460, 760, t, .22)
    s += zanaveska(90, 90, 460, 170, "#e8eef2", t, 1)
    s += ten(440, 1010, 400, 26, .42)
    s += f'<rect x="60" y="800" width="760" height="170" rx="12" fill="#f2f4f5" {o(8)}/>'
    s += f'<rect x="30" y="600" width="52" height="370" rx="10" fill="{ZHELEZ}" {o(7)}/>'
    dy = 5 * A.w(t, .5)
    s += f'<path d="M100,{806+dy:.0f} q260,-58 560,-8 q40,80 14,164 l-574,0 Z" fill="#dfe6ea" {o(7)}/>'
    s += f'<ellipse cx="180" cy="{776+dy:.0f}" rx="86" ry="56" fill="#fbfcfc" {o(6)}/>'
    s += f'<rect x="700" y="760" width="230" height="230" rx="10" fill="url(#dosk)" {o(8)}/>'
    bl = .3 + .6 * abs(A.w(t, 1.7))
    s += (f'<rect x="742" y="610" width="76" height="150" rx="12" fill="{STEKLO}" {o(6)}/>'
          f'<rect x="752" y="658" width="56" height="96" fill="#d9b24a" opacity=".85"/>'
          f'<rect x="752" y="{654+4*A.w(t,1.2):.0f}" width="56" height="12" fill="#f0d98a" opacity="{bl:.2f}"/>'
          f'<rect x="730" y="588" width="98" height="26" rx="8" fill="{ZHELEZ}" {o(5)}/>')
    s += (f'<rect x="836" y="700" width="130" height="34" rx="9" fill="#eef3f6" {o(6)}/>'
          f'<line x1="966" y1="717" x2="1030" y2="717" stroke="{ZHELEZ}" stroke-width="7"/>')
    s += f'<g opacity=".35">{par(440, 720, t, 3, .3, 170, .2)}</g>'
    s += ramka_pp("levo", "#1a2024", .4)
    s += vinetka(.38)
    return s


def patent(t):
    """Стол, лист патента, поверх него одна монета."""
    s = brevna(-20, -20, W + 40, H + 40, 118)
    s += f'<rect width="{W}" height="{H}" fill="#1d1711" opacity=".5"/>'
    s += f'<rect y="{H-420}" width="{W}" height="420" fill="url(#derev)" {o(0)}/>'
    s += doski(-20, H - 420, W + 40, 440, 96, False)
    s += teplo(420, 760, 480, 320, .8)
    # лист
    ug = .5 * A.w(t, .6)
    s += ten(420, 952, 300, 24, .45)
    s += (f'<g transform="rotate({ug:.2f} 420 800)">'
          f'<rect x="150" y="620" width="540" height="330" rx="6" fill="url(#list)" {o(6)}/>')
    for i in range(9):
        w_ = 420 - (i % 3) * 90
        s += (f'<line x1="200" y1="{676+i*30}" x2="{200+w_}" y2="{676+i*30}"'
              f' stroke="#8c8068" stroke-width="5" opacity=".55"/>')
    s += (f'<rect x="200" y="640" width="200" height="22" fill="#6d6250" opacity=".7"/>'
          f'<circle cx="610" cy="900" r="40" fill="none" stroke="{TKAN}" stroke-width="6" opacity=".7"/>'
          f'</g>')
    # монета поверх
    bl = .35 + .55 * abs(A.w(t, 1.8))
    s += ten(430, 818, 54, 12, .5)
    s += (f'<ellipse cx="430" cy="790" rx="62" ry="60" fill="url(#zol)" {o(6)}/>'
          f'<ellipse cx="430" cy="790" rx="44" ry="42" fill="none" stroke="{MED}" stroke-width="5"/>'
          f'<text x="430" y="810" font-family="DejaVu Serif, Georgia, serif" font-size="58"'
          f' fill="#6b4a12" text-anchor="middle" font-weight="bold">$1</text>'
          f'<ellipse cx="408" cy="766" rx="16" ry="12" fill="{SVET}" opacity="{bl:.2f}"/>')
    s += svecha(790, 700, t, .3, 1.0)
    s += f'<g opacity=".4">{par(420, 700, t, 3, .35, 130, .22)}</g>'
    s += mebel_hlam(1520, 980, 380, t, 79)
    s += vinetka(.48)
    return s


def peppi(t):
    """Детская: кровать, свеча, на одеяле раскрытая тетрадь."""
    s = doski(-20, -20, W + 40, H + 40, 120, True)
    s += f'<rect width="{W}" height="{H}" fill="#241c20" opacity=".52"/>'
    s += polovicy(H - 140)
    s += teplo(400, 620, 440, 320, .82)
    # кровать
    s += ten(430, 946, 320, 24, .5)
    s += f'<rect x="130" y="790" width="620" height="140" rx="12" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="106" y="628" width="44" height="310" rx="10" fill="url(#derev)" {o(6)}/>'
    dy = 5 * A.w(t, .5)
    s += f'<path d="M160,{800+dy:.0f} q190,-50 440,-8 q36,64 12,142 l-452,0 Z" fill="#6a7fa0" {o(6)}/>'
    s += f'<ellipse cx="214" cy="{772+dy:.0f}" rx="64" ry="42" fill="url(#rush)" {o(5)}/>'
    s += f'<circle cx="238" cy="{760+dy:.0f}" r="32" fill="#e3c39a" {o(5)}/>'
    # две рыжие косички торчат
    for i, dx in enumerate((-36, 36)):
        a = 8 * A.w(t, 1.2, i * .5)
        s += (f'<path d="M{238+dx},{750+dy:.0f} q{dx*.8+a:.0f},-34 {dx*1.3:.0f},-58"'
              f' stroke="#d4722a" stroke-width="11" fill="none" stroke-linecap="round"/>')
    # тетрадь на одеяле
    ug = .8 * A.w(t, .7)
    s += (f'<g transform="rotate({ug:.2f} 520 830)">'
          f'<path d="M400,840 q120,-34 240,0 l0,70 q-120,-30 -240,0 Z" fill="url(#list)" {o(5)}/>'
          f'<line x1="520" y1="828" x2="520" y2="906" stroke="#9b8f78" stroke-width="4"/>')
    for i in range(4):
        s += (f'<line x1="{424+i*4}" y1="{862+i*12}" x2="{500-i*2}" y2="{858+i*12}"'
              f' stroke="#8d8268" stroke-width="4" opacity=".6"/>'
              f'<line x1="{546+i*2}" y1="{858+i*12}" x2="{622-i*4}" y2="{862+i*12}"'
              f' stroke="#8d8268" stroke-width="4" opacity=".6"/>')
    s += "</g>"
    s += f'<rect x="710" y="700" width="96" height="84" rx="8" fill="url(#derev)" {o(6)}/>'
    s += svecha(758, 696, t, .15, 1.1)
    s += f'<g opacity=".45">{par(300, 700, t, 3, .4, 130, .22)}</g>'
    s += mebel_hlam(1520, 1000, 380, t, 83)
    s += ramka_pp("levo", "#120e11", .5)
    s += vinetka(.48)
    return s


def koridor_bolnicy(t):
    """Тёмный коридор, одна дверь приоткрыта — за ней свет. Пол блестит."""
    s = f'<rect width="{W}" height="{H}" fill="#1d242e"/>'
    s += f'<rect y="0" width="{W}" height="700" fill="url(#beton)" opacity=".5"/>'
    s += doski(-20, 700, W + 40, 400, 120, False, "beton")
    s += f'<rect y="690" width="{W}" height="18" fill="#59646e"/>'
    # перспектива коридора
    s += (f'<path d="M-20,0 L520,250 L520,760 L-20,1080 Z" fill="#273039" {o(0)}/>'
          f'<path d="M{W+20},0 L1180,250 L1180,760 L{W+20},1080 Z" fill="#222a33" {o(0)}/>')
    for i in range(5):
        x = 560 + i * 120
        s += f'<line x1="{x}" y1="250" x2="{x}" y2="760" stroke="#39434d" stroke-width="5"/>'
    # приоткрытая дверь: полоса света дышит
    dy = .5 + .5 * abs(A.w(t, 6.0))
    s += f'<rect x="300" y="300" width="230" height="470" rx="6" fill="#2e3842" {o(7)}/>'
    s += (f'<path d="M530,300 L690,330 L690,742 L530,770 Z" fill="{SVET}"'
          f' opacity="{.5+.3*dy:.2f}"/>')
    s += (f'<path d="M530,770 L690,742 L980,1080 L300,1080 Z" fill="{SVET}"'
          f' opacity="{.16+.1*dy:.2f}"/>')
    s += teplo(640, 560, 330, 420, .4 + .12 * dy)
    # тень проходит мимо света
    p = (t * .13) % 1.0
    s += f'<g opacity=".5">{siluet(1300 - p * 520, 900, 380, "#141a21", .9)}</g>'
    # каталка силуэтом и лампа дневного света, мигает
    s += ten(1480, 940, 160, 20, .5)
    s += (f'<rect x="1360" y="770" width="260" height="22" rx="8" fill="#49535d" {o(5)}/>'
          f'<circle cx="1400" cy="900" r="26" fill="#2b333c" {o(5)}/>'
          f'<circle cx="1580" cy="900" r="26" fill="#2b333c" {o(5)}/>')
    mig = 1.0 if not A.blink(t, 5.4, 0, .1) else .35
    s += (f'<rect x="700" y="120" width="420" height="26" rx="10" fill="#dfe9f2"'
          f' opacity="{mig:.2f}"/>')
    s += teplo(910, 150, 420, 160, .3 * mig)
    s += ramka_pp("oba", "#080b0f", .55)
    s += vinetka(.54)
    return s


def kreslo_vyazanie(t):
    """Кресло у окна, корзинка с пряжей, носок на спицах — зимняя работа."""
    s = brevna(-20, -20, W + 40, H + 40, 108)
    s += f'<rect width="{W}" height="{H}" fill="#241e2c" opacity=".28"/>'
    s += polovicy(890)
    vid = (f'<rect x="560" y="150" width="300" height="420" fill="#9fc0dc"/>'
           f'<rect x="560" y="400" width="300" height="170" fill="#e4eef7"/>'
           + f'<g opacity=".7">{sneg_letit(t, 16, 31, .6, .7)}</g>')
    s += okno_izby(560, 150, 300, 420, t, vid, moroz=.5, svet=False)
    s += luch(580, 170, 420, 740, t, .18)
    s += teplo(360, 560, 480, 420, .6)
    # кресло с подушкой
    s += ten(330, 920, 250, 24, .5)
    s += (f'<path d="M110,900 v-300 q0,-120 120,-120 h200 q120,0 120,120 v300 Z"'
          f' fill="url(#tkan)" {o(8)}/>'
          f'<path d="M150,720 h320 q18,120 -10,180 h-300 q-28,-60 -10,-180 Z"'
          f' fill="#c2524a" {o(6)}/>'
          f'<path d="M150,630 h320 q10,60 -16,92 h-288 q-26,-32 -16,-92 Z"'
          f' fill="#a8453f" opacity=".9" {o(5)}/>')
    # недовязанный носок: полотно на спицах, петли рядами, спицы блестят
    kach_v = 2.2 * A.w(t, 2.4)
    s += (f'<g transform="rotate({kach_v:.2f} 300 640)">'
          f'<path d="M236,640 h128 q16,-96 -14,-150 q-50,-26 -100,0 q-30,54 -14,150 Z"'
          f' fill="{KREM}" {o(6)}/>')
    for r_ in range(5):
        for c_ in range(6):
            s += (f'<ellipse cx="{252+c_*20}" cy="{604-r_*26}" rx="8" ry="6"'
                  f' fill="#dcc9a4" opacity=".9"/>')
    for i, a_ in enumerate((-28, 16)):
        bl = .35 + .65 * abs(A.w(t, 2.6, i * .4))
        s += (f'<g transform="rotate({a_} 300 560)">'
              f'<rect x="294" y="430" width="13" height="200" rx="6" fill="#cfc8b6" {o(3)}/>'
              f'<rect x="294" y="430" width="13" height="70" rx="6" fill="#fff8e6"'
              f' opacity="{bl:.2f}"/></g>')
    s += (f'<path d="M236,640 q-60,40 -96,120" fill="none" stroke="{KREM}"'
          f' stroke-width="6" opacity=".9"/></g>')
    # корзина с клубками, один клубок свесил нить
    s += ten(630, 912, 120, 18, .45)
    s += (f'<path d="M520,800 h210 l-24,112 h-162 Z" fill="url(#solom)" {o(6)}/>')
    for i, (x, y, c) in enumerate(((560, 796, "#d8c7a4"), (620, 802, TKAN), (676, 794, TKAN2))):
        dy = 2.6 * A.w(t, 2.0, i * .3)
        s += (f'<circle cx="{x}" cy="{y+dy:.1f}" r="30" fill="{c}" {o(5)}/>'
              f'<path d="M{x-24},{y+dy-6:.1f} q24,18 48,-6" fill="none" stroke="#7d5f3e" stroke-width="3"/>')
    dl = 60 + 26 * (1 + A.w(t, 4.4))
    s += (f'<path d="M676,790 q-70,{dl*.5:.0f} -150,{dl:.0f}" fill="none" stroke="{TKAN2}"'
          f' stroke-width="5" opacity=".9"/>')
    s += kot(840, 900, t, 1.0, "#4a4038", True)
    s += mebel_hlam(1300, 960, 620, t, 84)
    s += ramka_pp("levo", "#100d14", .44)
    s += vinetka(.46)
    return s


def okno_palaty(t):
    """Окно палаты распахнуто, на подоконнике стакан воды, за стеклом утро."""
    s = f'<rect width="{W}" height="{H}" fill="#e6eef4"/>'
    s += f'<rect width="{W}" height="700" fill="#dfe8ef"/>'
    s += doski(-20, 700, W + 40, 400, 130, False, "beton")
    s += f'<rect y="690" width="{W}" height="16" fill="#aab6bf"/>'
    vid = (f'<rect x="150" y="150" width="520" height="470" fill="#a9cde8"/>'
           f'<rect x="150" y="430" width="520" height="190" fill="#cfe0d2"/>'
           + f'<g opacity=".8">{oblaka(t, 240, 3, 33, .6, "#ffffff", 16.0)}</g>'
           + ryabina(600, 600, t, .9, 5))
    s += okno_izby(150, 150, 520, 470, t, vid, moroz=0, svet=True)
    s += (f'<g transform="rotate(8 670 380)">'
          f'<rect x="670" y="150" width="210" height="470" rx="6" fill="#eef4f8" opacity=".9" {o(6)}/>'
          f'<rect x="692" y="172" width="166" height="426" fill="url(#stekl)" opacity=".55"/></g>')
    s += luch(180, 170, 600, 820, t, .3)
    s += teplo(420, 440, 520, 420, .5)
    s += f'<rect x="120" y="620" width="600" height="36" rx="10" fill="#f2f6f9" {o(6)}/>'
    # стакан воды: блик и дрожь поверхности
    s += ten(300, 622, 46, 10, .3)
    s += (f'<path d="M258,500 h84 l-10,120 h-64 Z" fill="url(#stekl)" opacity=".8" {o(5)}/>'
          f'<path d="M262,540 h76 l-8,80 h-60 Z" fill="#9fd3e4" opacity=".85"/>')
    dy = 1.6 * A.w(t, 2.2)
    s += (f'<ellipse cx="300" cy="{540+dy:.1f}" rx="38" ry="7" fill="#d8f0fa" opacity=".9"/>'
          f'<rect x="270" y="520" width="9" height="86" fill="#ffffff" opacity=".5"/>')
    s += ptica(640, 596, t, .9, "#5b6a78", .15)
    # штатив капельницы силуэтом в стороне, не загораживая окна
    s += (f'<rect x="1150" y="300" width="14" height="640" rx="7" fill="#b7c2c9" {o(4)}/>'
          f'<path d="M1120,300 h88" stroke="#b7c2c9" stroke-width="12"/>'
          f'<path d="M1150,320 h52 l-8,100 h-36 Z" fill="#dff0fa" opacity=".9" {o(4)}/>')
    kap = (t * .9) % 1.0
    s += (f'<circle cx="1176" cy="{430+kap*120:.0f}" r="7" fill="#9fd3e4"'
          f' opacity="{1-kap:.2f}"/>')
    s += ramka_pp("pravo", "#8fa0ac", .3)
    s += vinetka(.3)
    return s


def zmej_ten(t):
    """Люди у ворот под нависшей тенью змея: дань в мешках, тень ходит."""
    s = nebo("sumer", t, False, 51)
    s += f'<g opacity=".45">{oblaka(t, 150, 4, 53, .45, "#8a93a4", 13.0)}</g>'
    s += kladka(-20, 260, 1000, 700, 84, "url(#kamen)")
    s += (f'<path d="M190,960 V560 q270,-200 540,0 V960 Z" fill="#14100e" {o(9)}/>')
    s += f'<rect x="206" y="600" width="508" height="360" fill="url(#derev)" {o(7)}/>'
    # тень змея: крыло и шея ходят над людьми
    hd = 40 * A.w(t, 6.0)
    s += (f'<g opacity=".52" transform="translate({hd:.0f},0)">'
          f'<path d="M-60,120 q420,-70 720,110 q300,160 620,70 l0,180'
          f' q-340,70 -660,-100 q-380,-200 -680,-120 Z" fill="#0b0d12"/>'
          f'<path d="M980,300 q140,-30 230,60 q-120,70 -230,-60 Z" fill="#0b0d12"/></g>')
    # люди спинами, пригнулись
    for i, (x, h_, ph) in enumerate(((300, 320, .0), (470, 300, .3), (640, 310, .6))):
        kach = 2.2 * A.w(t, 4.0, ph)
        s += (f'<g transform="rotate({kach:.2f} {x} 950) translate(0,{10*abs(A.w(t,3.0,ph)):.0f})">'
              f'{siluet(x, 950, h_, "#1a1d24", .95, i == 1, "#7d8898")}</g>')
    # мешки дани у ворот
    for i, (x, r) in enumerate(((210, 60), (330, 52), (760, 58))):
        dy = 1.8 * A.w(t, 3.4, i * .3)
        s += ten(x, 952, r * 1.1, 16, .45)
        s += (f'<path d="M{x-r},{950+dy:.1f} q0,-{r*1.5:.0f} {r}, -{r*1.6:.0f}'
              f' q{r},{r*.1:.0f} {r},{r*1.6:.0f} Z" fill="url(#rush)" {o(6)}/>'
              f'<path d="M{x-r*.5:.0f},{950-r*1.5+dy:.1f} q{r*.5:.0f},-{r*.3:.0f} {r:.0f},0"'
              f' fill="none" stroke="#8a6a46" stroke-width="7"/>')
    s += f'<g opacity=".4">{tuman(t, 900, .45, "#aeb9c6")}</g>'
    s += ramka_pp("oba", "#080a0e", .54)
    s += vinetka(.52)
    return s


def kreslo_lampa(t):
    """Вечер: кресло, лампа с абажуром, раскрытая книга, детская фигурка рядом."""
    s = brevna(-20, -20, W + 40, H + 40, 110)
    s += f'<rect width="{W}" height="{H}" fill="#191320" opacity=".52"/>'
    s += polovicy(900)
    s += lampa(690, 560, t, 1.15, True)
    s += teplo(520, 620, 520, 420, .66)
    # кресло с высокой спинкой
    s += ten(330, 930, 260, 24, .55)
    s += (f'<path d="M110,920 v-340 q0,-130 130,-130 h190 q130,0 130,130 v340 Z"'
          f' fill="url(#tkan)" {o(8)}/>'
          f'<path d="M150,700 h320 q20,130 -12,200 h-296 q-32,-70 -12,-200 Z"'
          f' fill="#bf4f48" {o(6)}/>')
    # раскрытая книга «на коленях»
    kach = 1.8 * A.w(t, 4.0)
    s += (f'<g transform="rotate({kach:.2f} 310 690)">'
          f'<path d="M180,700 q130,-44 260,0 l0,-60 q-130,-40 -260,0 Z" fill="url(#list)" {o(6)}/>'
          f'<path d="M310,640 q66,-22 130,0 l0,60 q-64,-20 -130,0 Z" fill="#faf4e2" {o(4)}/>'
          f'<line x1="310" y1="640" x2="310" y2="700" stroke="#8a7a58" stroke-width="5"/></g>')
    for i in range(4):
        s += (f'<line x1="206" y1="{662+i*10}" x2="300" y2="{658+i*10}" stroke="#7d6a45"'
              f' stroke-width="3" opacity=".6"/>')
    # детская фигурка сидит у кресла
    s += siluet(560, 920, 230, "#2a2130", .95, False, "#d8a96a")
    s += kot(840, 910, t, .9, "#4a4038", True)
    s += f'<g opacity=".3">{par(520, 860, t, 4, .3, 320, .2, 2.0)}</g>'
    s += mebel_hlam(1340, 960, 580, t, 89)
    s += ramka_pp("levo", "#0c0912", .48)
    s += vinetka(.48)
    return s


def okno_derevo(t):
    """Городское окно: во дворе дерево, на ветке держится один лист."""
    s = f'<rect width="{W}" height="{H}" fill="#c6bba6"/>'
    s += f'<rect width="{W}" height="700" fill="#bdb199"/>'
    # вид: панельки, двор, дерево с одним листом
    vid = (f'<rect x="140" y="120" width="660" height="520" fill="#9fb8cd"/>'
           + panelka(560, 520, 300, t, 5, True, 105)
           + f'<rect x="140" y="500" width="660" height="140" fill="#dfe8ef"/>')
    s += okno_izby(140, 120, 660, 520, t, vid, moroz=.2, svet=False)
    # дерево — поверх вида, в пределах окна
    s += (f'<g clip-path="url(#okno_der)">'
          f'<clipPath id="okno_der"><rect x="140" y="120" width="660" height="520"/></clipPath>'
          f'<rect x="300" y="300" width="36" height="340" fill="#4e3b2a" {o(5)}/>')
    for i, (a_, ln) in enumerate(((-38, 150), (-14, 180), (16, 165), (42, 140))):
        kl = 1.6 * A.w(t, 4.0, i * .3)
        s += (f'<g transform="rotate({a_+kl:.2f} 318 360)">'
              f'<rect x="310" y="{360-ln}" width="18" height="{ln}" fill="#4e3b2a" {o(4)}/></g>')
    # единственный лист дрожит на ветке
    dr = 7 * A.w(t, 1.7)
    s += (f'<g transform="rotate({dr:.1f} 236 250)">'
          f'<path d="M236,250 q30,-26 58,4 q-30,26 -58,-4 Z" fill="{ORA}" {o(4)}/>'
          f'<path d="M236,250 q28,0 58,4" fill="none" stroke="#9c6a28" stroke-width="3"/></g>')
    s += "</g>"
    s += luch(160, 140, 660, 820, t, .18)
    s += f'<rect x="100" y="640" width="740" height="44" rx="10" fill="#e8dcc6" {o(7)}/>'
    # кружка на подоконнике и отражение в стекле
    s += ten(240, 644, 50, 10, .35)
    s += (f'<path d="M196,556 h88 l-10,86 h-68 Z" fill="#ffffff" {o(6)}/>'
          f'<path d="M284,578 q38,28 0,54" fill="none" stroke="{K}" stroke-width="5"/>'
          f'<ellipse cx="240" cy="556" rx="44" ry="12" fill="#6b4a32" {o(4)}/>')
    s += f'<g opacity=".2">{par(240, 544, t, 3, .3, 110, .2)}</g>'
    s += (f'<rect x="150" y="130" width="640" height="500" fill="{STEKLO}" opacity=".12"/>')
    s += kvartira_veschi(1180, 700, 740, t, 106)
    s += ramka_pp("levo", "#2a2318", .3)
    s += vinetka(.4)
    return s


def klubok_pol(t):
    """Пол избы: клубок катится через кадр, за ним тянется нить, кот следит."""
    s = brevna(-20, -20, W + 40, H + 40, 110)
    s += f'<rect width="{W}" height="{H}" fill="#1e1a20" opacity=".4"/>'
    s += polovicy(560)
    s += teplo(500, 760, 620, 380, .55)
    s += luch(260, -30, 420, 900, t, .16)
    # корзина, откуда он выкатился
    s += ten(150, 710, 110, 18, .45)
    s += (f'<path d="M48,598 h204 l-26,112 h-152 Z" fill="url(#solom)" {o(7)}/>'
          f'<rect x="40" y="580" width="220" height="26" rx="12" fill="#c7a44e" {o(5)}/>')
    for i in range(6):
        s += (f'<path d="M{64+i*30},606 q6,54 0,100" fill="none" stroke="#a07c2e"'
              f' stroke-width="6" opacity=".7"/>')
    s += (f'<circle cx="110" cy="586" r="30" fill="{TKAN2}" {o(5)}/>'
          f'<circle cx="190" cy="590" r="26" fill="#d8c7a4" {o(5)}/>')
    # нить тянется от корзины к клубку
    p = (t * .17) % 1.0
    x = 180 + p * 640
    y = 820 + 30 * math.sin(p * 6.2)
    s += (f'<path d="M150,660 q{(x-150)*.4:.0f},{(y-660)*.8:.0f} {x-150:.0f},{y-660:.0f}"'
          f' fill="none" stroke="{TKAN}" stroke-width="7" opacity=".9"/>')
    # клубок крутится
    s += ten(x, y + 44, 52, 14, .45)
    s += (f'<g transform="rotate({p*720:.0f} {x:.0f} {y:.0f})">'
          f'<circle cx="{x:.0f}" cy="{y:.0f}" r="52" fill="{TKAN}" {o(6)}/>'
          f'<path d="M{x-40:.0f},{y-18:.0f} q40,34 80,-6" fill="none" stroke="#8a2b32"'
          f' stroke-width="5"/>'
          f'<path d="M{x-34:.0f},{y+20:.0f} q36,28 70,-10" fill="none" stroke="#f0a9a2"'
          f' stroke-width="4" opacity=".6"/></g>')
    # кот следит: голова поворачивается за клубком
    s += kot(1020, 900, t, 1.25, "#4a4038", False)
    s += (f'<g transform="rotate({-6+12*p:.1f} 1020 820)">'
          f'<ellipse cx="1020" cy="800" rx="52" ry="44" fill="#4a4038" {o(5)}/>'
          f'<path d="M980,772 l-10,-44 l40,20 Z" fill="#4a4038" {o(4)}/>'
          f'<path d="M1060,772 l10,-44 l-40,20 Z" fill="#4a4038" {o(4)}/>')
    if not A.blink(t, 3.6):
        s += (f'<ellipse cx="1002" cy="798" rx="9" ry="12" fill="{ZOL}"/>'
              f'<ellipse cx="1038" cy="798" rx="9" ry="12" fill="{ZOL}"/>')
    else:
        s += (f'<path d="M993,798 h18 M1029,798 h18" stroke="#2a2420" stroke-width="5"/>')
    s += "</g>"
    s += lavka(560, 540, 260)
    s += utvar_izby(1300, 520, 600, t, 155)
    s += ramka_pp("levo", "#0d0a10", .44)
    s += vinetka(.46)
    return s


def hutor_kuhnya(t):
    """Кухня хутора: стол, тесто на доске, детская кроватка в углу."""
    s = doski(-20, -20, W + 40, H + 40, 124, True, "dosk")
    s += f'<rect width="{W}" height="{H}" fill="#e8dcc6" opacity=".18"/>'
    s += f'<rect width="{W}" height="{H}" fill="#2a2218" opacity=".2"/>'
    s += polovicy(900)
    vid = (f'<rect x="640" y="150" width="280" height="300" fill="#a9c6de"/>'
           f'<rect x="640" y="340" width="280" height="110" fill="#8ea55a"/>')
    s += okno_izby(640, 150, 280, 300, t, vid, moroz=0, svet=True)
    s += luch(660, 170, 420, 740, t, .26)
    s += teplo(420, 520, 480, 400, .6)
    # стол с мукой и тестом: тесто дышит под рушником
    s += ten(400, 930, 320, 24, .5)
    s += f'<rect x="90" y="620" width="640" height="42" rx="10" fill="url(#derev)" {o(8)}/>'
    for x in (130, 650):
        s += f'<rect x="{x}" y="662" width="32" height="270" fill="url(#derev)" {o(6)}/>'
    s += (f'<path d="M150,616 h420 l-20,-10 h-380 Z" fill="#f6efdc" opacity=".5"/>')
    dysh = 1.0 + .05 * (1 + A.w(t, 4.4))
    s += (f'<g transform="translate(330,590) scale({dysh:.3f},{dysh:.3f}) translate(-330,-590)">'
          f'<path d="M226,614 q104,-96 208,0 Z" fill="url(#krem)" {o(6)}/>'
          f'<path d="M248,590 q82,-54 164,0 q-82,22 -164,0 Z" fill="#f6efdc" opacity=".8"/></g>')
    # мука рассыпана и скалка
    r = random.Random(157)
    for i in range(26):
        s += (f'<circle cx="{r.uniform(150,700):.0f}" cy="{r.uniform(604,618):.0f}"'
              f' r="{r.uniform(3,8):.0f}" fill="#ffffff" opacity=".7"/>')
    s += (f'<rect x="470" y="596" width="210" height="26" rx="13" fill="url(#derev)" {o(5)}/>'
          f'<rect x="446" y="602" width="34" height="14" rx="7" fill="url(#derev)" {o(4)}/>'
          f'<rect x="670" y="602" width="34" height="14" rx="7" fill="url(#derev)" {o(4)}/>')
    # кроватка в углу: качается, над ней висит игрушка
    kach = 2.4 * A.w(t, 2.6)
    s += ten(1180, 950, 180, 22, .45)
    s += (f'<g transform="rotate({kach:.2f} 1180 940)">'
          # короб люльки
          f'<path d="M1010,740 h340 l-34,170 h-272 Z" fill="url(#derev)" {o(7)}/>'
          f'<rect x="1000" y="716" width="360" height="34" rx="12" fill="#8a5f3c" {o(6)}/>')
    for i in range(9):                                  # точёные прутья боковины
        s += (f'<rect x="{1030+i*36}" y="752" width="13" height="150" rx="6"'
              f' fill="#a0733f" {o(3)}/>')
    s += (f'<path d="M1040,752 q140,-70 280,0 q-26,56 -140,56 q-114,0 -140,-56 Z"'
          f' fill="url(#krem)" {o(5)}/>'                # подушка
          f'<path d="M1048,804 h264 l-22,104 h-220 Z" fill="{TKAN}" opacity=".9" {o(5)}/>'
          # полозья, на которых люлька качается
          f'<path d="M980,910 q200,60 400,0 l0,34 q-200,60 -400,0 Z" fill="#6d4423" {o(6)}/></g>')
    s += (f'<path d="M1180,420 v120" stroke="{K}" stroke-width="5"/>')
    k2 = 5.0 * A.w(t, 3.0)
    s += (f'<g transform="rotate({k2:.2f} 1180 420)">'
          f'<circle cx="1180" cy="566" r="30" fill="{TKAN}" {o(5)}/>'
          f'<circle cx="1180" cy="566" r="12" fill="#f2d9b0" opacity=".8"/></g>')
    s += f'<g opacity=".4">{par(330, 580, t, 4, .3, 260, .2, 1.8)}</g>'
    s += mebel_hlam(1560, 980, 360, t, 159)
    s += ramka_pp("levo", "#120e08", .42)
    s += vinetka(.44)
    return s
