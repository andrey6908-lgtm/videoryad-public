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
    """Бабушкин буфет во всю левую полосу: стекло, коробка мелочи, соль, спички."""
    s = f'<rect width="{W}" height="{H}" fill="#584437"/>'
    s += doski(0, 0, W, H, 164, True, "dosk")
    s += f'<rect width="{W}" height="{H}" fill="#2a1d14" opacity=".42"/>'
    s += polovicy(960)
    s += teplo(400, 420, 700, 620, .9)
    s += ten(420, 990, 400, 30, .55)
    # корпус
    s += f'<rect x="56" y="150" width="740" height="840" rx="16" fill="url(#derev)" {o(9)}/>'
    s += f'<rect x="30" y="108" width="792" height="54" rx="12" fill="{DOSKA2}" {o(8)}/>'
    s += f'<path d="M30,108 q396,-56 792,0" fill="{DOSKA2}" {o(7)}/>'
    # верх: две стеклянные дверцы, по стеклу бежит блик
    for i, x in enumerate((94, 440)):
        s += f'<rect x="{x}" y="{196}" width="314" height="400" rx="10" fill="url(#stekl)" opacity=".78" {o(7)}/>'
        bl = (t * .32 + i * .5) % 1.0
        s += f'<path d="M{x+16+bl*250:.0f},200 l62,0 l-92,392 l-62,0 Z" fill="#ffffff" opacity=".2"/>'
        s += f'<rect x="{x}" y="196" width="314" height="400" rx="10" fill="none" {o(7)}/>'
    s += polka(104, 392, 680)
    for i, x in enumerate((170, 300, 430, 560, 690)):
        s += krynka(x, 386, .92 + .1 * (i % 2))
    for i, x in enumerate((230, 500)):
        s += (f'<rect x="{x}" y="252" width="110" height="130" rx="8" fill="url(#krem)" {o(5)}/>'
              f'<rect x="{x+14}" y="286" width="82" height="16" fill="{TKAN}" opacity=".7"/>')
    # нижняя полка крупно: коробка мелочи, солонка, спички
    s += polka(84, 724, 700)
    s += f'<rect x="130" y="610" width="250" height="114" rx="10" fill="url(#med)" {o(7)}/>'
    s += f'<rect x="146" y="626" width="218" height="20" rx="6" fill="#8a6128" opacity=".7"/>'
    s += monety(255, 600, t, 7, 3, 1.3)
    s += f'<rect x="430" y="624" width="128" height="100" rx="10" fill="url(#krem)" {o(7)}/>'
    s += f'<ellipse cx="494" cy="624" rx="64" ry="18" fill="{POBEL}" {o(5)}/>'
    s += f'<path d="M470,600 q24,-30 48,0" fill="none" stroke="{POBEL}" stroke-width="8" opacity=".8"/>'
    s += f'<rect x="606" y="636" width="170" height="88" rx="8" fill="{TKAN}" {o(7)}/>'
    s += f'<rect x="628" y="658" width="126" height="44" rx="5" fill="url(#krem)"/>'
    s += f'<rect x="644" y="670" width="94" height="20" rx="4" fill="#9c7049" opacity=".7"/>'
    # крючки дверец позвякивают
    for i, dx in enumerate((-6, 6)):
        s += (f'<circle cx="{414+dx}" cy="{400+i*4}" r="11" fill="url(#zhel)"'
              f' opacity="{.55+.45*abs(A.w(t,2.2,i*.3)):.2f}"/>')
    s += f'<rect x="76" y="752" width="700" height="230" rx="10" fill="{DOSKA2}" {o(7)}/>'
    for x in (160, 480):
        s += f'<rect x="{x}" y="790" width="280" height="150" rx="8" fill="url(#derev)" {o(6)}/>'
        s += f'<circle cx="{x+140}" cy="865" r="14" fill="url(#zhel)" {o(4)}/>'
    s += lampa(690, 300, t, 1.3)
    s += ramka_pp("levo", "#140f0b", .45)
    s += utvar_izby(1140, 620, 700, t, 22)
    s += mebel_hlam(1080, 1010, 700, t, 23)
    s += vinetka(.44)
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
    """Сени: приоткрытая дверь, лавка, кружка на гвозде, холодный пар."""
    s = brevna(-20, -20, W + 40, H + 40, 104)
    s += f'<rect width="{W}" height="{H}" fill="#1c222e" opacity=".42"/>'
    s += polovicy(900)
    s += dver(140, 180, 400, 740, .45, "url(#derev)", kruchok=True)
    s += f'<rect x="150" y="190" width="150" height="720" fill="#9fc2de" opacity=".5"/>'
    s += f'<g opacity=".55">{par(230, 820, t, 5, .5, 420, .22, 1.6)}</g>'
    s += lavka(600, 840, 230)
    s += f'<circle cx="700" cy="420" r="10" fill="url(#zhel)" {o(3)}/>'
    kach = 5 * A.w(t, 3.0)
    s += (f'<g transform="rotate({kach:.1f} 700 420)">'
          f'<path d="M662,440 v120 q38,22 76,0 v-120 Z" fill="url(#krem)" {o(6)}/>'
          f'<path d="M738,470 q40,30 0,60" fill="none" stroke="{KREM}" stroke-width="14"/></g>')
    s += teplo(640, 700, 420, 380, .5)
    s += mebel_hlam(1120, 900, 720, t, 5)
    s += utvar_izby(1000, 420, 820, t, 6)
    return s


def polka_zapasy(t):
    """Полка с крынками, мешочками и караваем: тёплый свет сменяется сквозняком."""
    s = brevna(-20, -20, W + 40, H + 40, 112)
    hol = max(0.0, A.w(t, 7.0))
    s += f'<rect width="{W}" height="{H}" fill="#2b3550" opacity="{.25+.3*hol:.2f}"/>'
    s += teplo(380, 540, 560, 460, .85 - .4 * hol)
    s += polka(80, 620, 700)
    for i, x in enumerate((150, 270, 390)):
        s += krynka(x, 614, .95 - i * .08)
    for i, x in enumerate((500, 600)):
        s += (f'{ten(x, 620, 46, 10, .4)}'
              f'<path d="M{x-46},614 q0,-120 46,-120 q46,0 46,120 Z" fill="url(#rush)" {o(6)}/>'
              f'<path d="M{x-30},520 q30,-18 60,0" fill="none" stroke="{TKAN}" stroke-width="9"/>')
    s += karavay(690, 606, .8)
    s += polka(120, 880, 600)
    for i, x in enumerate((200, 340, 480, 600)):
        s += krynka(x, 874, .6)
    # золотой огонёк летит к двери, синий сквозняк клубится
    p = (t * .33) % 1.0
    s += (f'<circle cx="{300+p*560:.0f}" cy="{500-120*math.sin(p*math.pi):.0f}" r="{12*(1-p*.5):.1f}"'
          f' fill="{SVET}" opacity="{1-p:.2f}"/>')
    s += f'<g opacity="{.3*hol+.12:.2f}">{par(840, 980, t, 4, .6, 520, .3, 2.0)}</g>'
    s += utvar_izby(960, 760, 880, t, 7)
    s += mebel_hlam(880, 1010, 600, t, 8)
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
    """Тихая изба вечером: стол под лампой, дверь с крючком, окно сеней."""
    s = brevna(-20, -20, W + 40, H + 40, 116)
    s += f'<rect width="{W}" height="{H}" fill="#1d2233" opacity=".42"/>'
    s += polovicy(900)
    s += lampa(360, 540, t, 1.0, abazhur=True)
    s += stol(170, 700, 420)
    s += f'<ellipse cx="380" cy="700" rx="190" ry="28" fill="{SVET}" opacity=".18"/>'
    s += krynka(300, 700, .6)
    s += karavay(450, 700, .55, False)
    s += dver(660, 240, 300, 680, 0, "url(#derev)", kruchok=True)
    kach = 7 * A.w(t, 2.8)
    s += (f'<g transform="rotate({kach:.1f} 972 552)">'
          f'<rect x="966" y="552" width="14" height="70" rx="6" fill="url(#zhel)" {o(4)}/></g>')
    s += kot(640, 980, t, .72, "#3b3430", spit=True)
    s += teplo(380, 660, 480, 420, .7)
    s += utvar_izby(1080, 620, 780, t, 9)
    s += vinetka(.38)
    return s


def okno_chuzhoj(t):
    """Вид из избы в окно: у калитки тёмная фигура; изба перетекает в город."""
    gorod = A.ease(A.seg(t, 3.2, 2.0))
    s = brevna(-20, -20, W + 40, H + 40, 110)
    s += f'<rect width="{W}" height="{H}" fill="#9aa3a8" opacity="{.5*gorod:.2f}"/>'
    s += f'<rect width="{W}" height="{H}" fill="#1b2130" opacity=".4"/>'
    vid = (f'<rect x="120" y="200" width="620" height="560" fill="{"#5a6a7c" if gorod>.5 else "#2b3550"}"/>'
           + _sneg_lezhit(600, 16, "#dfe9f5")
           + f'<rect x="240" y="470" width="24" height="150" fill="#3a3027"/>'
           + f'<rect x="420" y="470" width="24" height="150" fill="#3a3027"/>'
           + pleten(200, 620, 300, 120, 6)
           + siluet(470 + 10 * A.w(t, 4.0), 630, 210, "#15171d", .94, kant="#8fa8c4")
           + _sneg_letit(t, 14, 4, .5, .7))
    s += okno_izby(120, 200, 620, 560, t, vid=vid, moroz=.55 + .3 * abs(A.w(t, 9.0)))
    s += f'<path d="M86,180 q60,420 34,620" fill="none" stroke="{TKAN}" stroke-width="40" opacity=".85"/>'
    s += (f'<path d="M{770+8*A.w(t,6.0):.0f},180 q-60,420 -34,620" fill="none" stroke="{TKAN}"'
          f' stroke-width="40" opacity=".85"/>')
    s += f'<rect y="840" width="{W}" height="240" fill="url(#pol)" {o(5)}/>'
    s += teplo(430, 900, 420, 240, .35)
    s += utvar_izby(900, 700, 940, t, 10)
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
    """Сумерки, широкая река, высокий берег с пещерами, частокол поверху."""
    s = nebo("sumer", t, True, 12)
    s += oblaka(t, 210, 5, 3, .42, "#c9b4ac", 7)
    s += f'<ellipse cx="1520" cy="300" rx="120" ry="120" fill="#f3d9a8" opacity=".4"/>'
    s += f'<path d="M0,700 Q420,650 900,700 Q1420,748 1920,690 L1920,1080 L0,1080 Z" fill="url(#voda)"/>'
    for i in range(11):
        y = 730 + i * 32
        s += (f'<path d="M{-100+60*A.w(t,7+i*.6,i*.2):.0f},{y} q300,{10-i} 640,0 q340,{-8+i} 680,0"'
              f' fill="none" stroke="#9fd0d8" stroke-width="5" opacity="{.34-.018*i:.2f}"/>')
    # ХОЛМ выше и с фактурой
    s += (f'<path d="M-20,706 L-20,200 Q300,96 620,250 Q830,360 960,706 Z" fill="#3a3340" {o(8)}/>')
    s += (f'<path d="M-20,706 L-20,230 Q300,130 600,280 Q800,384 920,706 Z" fill="#2c2733"/>')
    for i in range(14):
        x = -20 + i * 72
        s += f'<path d="M{x},706 q24,-120 46,-210" fill="none" stroke="#231f2b" stroke-width="7" opacity=".55"/>'
    # пещеры крупно, с огоньками
    for i, (x, y) in enumerate(((150, 520), (330, 430), (520, 500), (680, 610), (250, 640))):
        s += f'<ellipse cx="{x}" cy="{y}" rx="62" ry="78" fill="#120f18" {o(6)}/>'
        s += teplo(x, y + 20, 92, 92, .8)
        s += (f'<circle cx="{x}" cy="{y+22}" r="{18+4*A.w(t,2.0+i*.4,i*.2):.1f}" fill="{SVET}"'
              f' opacity="{.6+.4*abs(A.w(t,1.8,i*.3)):.2f}"/>')
    # частокол и постройки поверху
    for i in range(16):
        s += (f'<rect x="{96+i*42}" y="{206-abs(i-8)*6}" width="30" height="110" rx="14"'
              f' fill="url(#derev)" {o(5)}/>')
    s += f'<rect x="300" y="146" width="230" height="110" fill="url(#brev)" {o(6)}/>'
    s += f'<path d="M278,146 L414,70 L552,146 Z" fill="{DOSKA2}" {o(6)}/>'
    s += f'<rect x="458" y="60" width="40" height="92" fill="url(#kamen)" {o(5)}/>'
    s += dym(478, 60, t, 4, .2, 220, .3, "#b8bfc8", .7)
    # лодка на реке
    s += (f'<path d="M1180,{836+6*A.w(t,4.0):.0f} q80,36 180,0 q-80,-28 -180,0 Z" fill="#2c2733" {o(5)}/>')
    s += tuman(t, 700, .34)
    s += ramka_pp("pravo", "#161322", .4)
    s += ulica_dal(1100, 700, 760, t, False, 56)
    s += vinetka(.46)
    return s


def vorota(t):
    """Деревянные ворота в бревенчатой стене на вершине холма, фонарь, тропа."""
    s = nebo("sumer", t, True, 15)
    s += oblaka(t, 180, 3, 8, .32, "#b9a79e", 6)
    s += f'<path d="M0,900 Q400,820 830,880 L830,1080 L0,1080 Z" fill="#2c3a2e" {o(6)}/>'
    s += brevna(60, 300, 760, 600, 86)
    otkr = A.ease(A.seg(t, 2.0, 2.2))
    s += f'<rect x="300" y="420" width="300" height="480" rx="10" fill="#120f12"/>'
    s += (f'<g transform="translate(300,420) scale({1-otkr*.8:.3f},1)">'
          f'{doski(0, 0, 300, 480, 62, True, "derev")}'
          f'<rect x="0" y="0" width="300" height="480" fill="none" {o(8)}/>'
          f'<path d="M10,70 h280 M10,400 h280" stroke="url(#zhel)" stroke-width="14"/></g>')
    s += teplo(440, 700, 300 * otkr + 60, 280 * otkr + 60, .8 * otkr)
    kach = 6 * A.w(t, 3.6)
    s += (f'<g transform="rotate({kach:.1f} 660 360)">'
          f'<line x1="660" y1="360" x2="660" y2="440" stroke="{K}" stroke-width="6"/>'
          f'<rect x="624" y="440" width="72" height="90" rx="10" fill="url(#zhel)" opacity=".9" {o(5)}/>'
          f'{teplo(660, 486, 150, 140, .9)}</g>')
    s += (f'<path d="M430,1080 Q470,980 440,900" fill="none" stroke="#8d8372" stroke-width="56" opacity=".6"/>')
    s += siluet(430, 1010, 300, "#16141a", .92, kant="#6b7fa0")
    s += ulica_dal(900, 900, 1000, t, True, 53)
    s += vinetka(.46)
    return s


def kelya(t):
    """Тесная келья: свеча, стол, доска с вырезанными буквами."""
    s = kladka(-20, -20, W + 40, H + 40, 92, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#120f14" opacity=".55"/>'
    s += teplo(360, 560, 440, 420, 1.0)
    s += f'<rect y="930" width="{W}" height="150" fill="#3b332a"/>'
    s += stol(150, 680, 500)
    s += svecha(230, 560, t, .1, 1.1)
    # доска с буквами, они загораются по одной
    s += ten(450, 700, 150, 16, .45)
    s += f'<rect x="320" y="520" width="310" height="160" rx="10" fill="url(#dosk)" {o(7)}/>'
    bukvy = "АБВГДЕ"
    for i, b in enumerate(bukvy):
        on = A.seg(t, .6 + i * .55, .5)
        s += (f'<text x="{348+i*48}" y="{610}" font-family="DejaVu Serif, Georgia, serif"'
              f' font-size="54" fill="{SVET if on>.5 else "#6b4428"}"'
              f' opacity="{.45+.55*on:.2f}">{b}</text>')
    s += lavka(640, 840, 180)
    s += siluet(560, 700, 330, "#14110f", .9, kant=SVET)
    s += mebel_hlam(1120, 940, 700, t, 27)
    s += utvar_izby(1000, 500, 800, t, 28)
    s += vinetka(.55)
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
    """Полиэкран: слева целая мантия в углях, справа рубаха с водой на крюке."""
    hw = W / 2
    s = f'<rect width="{W}" height="{H}" fill="#140f0e"/>'
    s += f'<clipPath id="dvL"><rect width="{hw:.0f}" height="{H}"/></clipPath><g clip-path="url(#dvL)">'
    s += kladka(-20, -20, hw + 40, H + 40, 88, "url(#kamen)")
    s += f'<rect width="{hw:.0f}" height="{H}" fill="#120c0a" opacity=".55"/>'
    s += teplo(hw * .5, 640, 380, 340, .9)
    s += f'<path d="M160,880 v-210 q300,-170 600,0 v210 Z" fill="#190f0a" {o(7)}/>'
    s += ugli(220, 850, 480, t, 10)
    s += (f'<path d="M300,840 q160,-120 330,0 q-160,60 -330,0 Z" fill="{TKAN2}" {o(6)}/>')
    s += f'<path d="M330,826 q150,-96 280,0" fill="none" stroke="#6d8aa8" stroke-width="10" opacity=".7"/>'
    s += "</g>"
    s += f'<clipPath id="dvR"><rect x="{hw:.0f}" width="{hw:.0f}" height="{H}"/></clipPath><g clip-path="url(#dvR)">'
    s += kladka(hw - 20, -20, hw + 40, H + 40, 88, "url(#kamen)")
    s += f'<rect x="{hw:.0f}" width="{hw:.0f}" height="{H}" fill="#0f1620" opacity=".6"/>'
    s += f'<path d="M{hw+120:.0f},200 h520" stroke="{ZHELEZ}" stroke-width="16"/>'
    s += f'<path d="M{hw+440:.0f},200 v70" stroke="url(#zhel)" stroke-width="14"/>'
    kach = 2.6 * A.w(t, 4.4)
    s += (f'<g transform="rotate({kach:.2f} {hw+440:.0f} 270)">'
          f'<path d="M{hw+330:.0f},300 q110,-44 220,0 l-22,330 q-88,34 -176,0 Z" fill="url(#krem)" {o(7)}/>')
    for sgn, x0 in ((-1, hw + 330), (1, hw + 550)):
        s += (f'<path d="M{x0:.0f},310 q{sgn*90:.0f},70 {sgn*34:.0f},180" fill="none"'
              f' stroke="{KREM}" stroke-width="40" stroke-linecap="round"/>')
    s += "</g>"
    for i in range(4):
        p = ((t * .5) + i * .25) % 1.0
        s += (f'<ellipse cx="{hw+420+i*22:.0f}" cy="{660+p*300:.0f}" rx="7" ry="12"'
              f' fill="{STEKLO}" opacity="{(1-p)*.9:.2f}"/>')
    s += f'<ellipse cx="{hw+450:.0f}" cy="980" rx="160" ry="34" fill="url(#voda)" opacity=".65"/>'
    s += "</g>"
    s += f'<rect x="{hw-4:.0f}" width="8" height="{H}" fill="{K}" opacity=".85"/>'
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
    """Ночь, в ряд: окно пекарни, окно избы, окно панельного дома."""
    s = nebo("noch", t, True, 27)
    s += sneg_lezhit(860, 22, "#39445c")
    s += f'<rect y="960" width="{W}" height="120" fill="#232c3e"/>'
    bases = ((60, "kamen", 0), (330, "brev", 1), (610, "beton", 2))
    for i, (x, grad, k) in enumerate(bases):
        s += f'<rect x="{x}" y="340" width="230" height="640" fill="url(#{grad})" {o(7)}/>'
        per = (t * .33 + i * .33) % 1.0
        gl = .45 + .55 * max(0.0, 1 - abs(per - i / 3.0) * 4)
        s += okno_izby(x + 40, 460, 150, 180, t, svet=True, moroz=.3 if i == 1 else 0)
        s += teplo(x + 115, 550, 220 * gl + 60, 200 * gl + 60, .7 * gl)
    s += f'<rect x="100" y="250" width="54" height="110" fill="url(#kamen)" {o(5)}/>'
    s += dym(127, 250, t, 5, .2, 260, .35, "#b8bfc8", .7)
    s += f'<rect x="420" y="240" width="46" height="110" fill="url(#kamen)" {o(5)}/>'
    s += dym(443, 240, t, 5, .22, 260, .3, "#b8bfc8", .7)
    s += sneg_letit(t, 22, 13, .5, .7)
    s += ulica_dal(900, 960, 1000, t, True, 36)
    s += vinetka(.45)
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
    """Лестничная площадка панельного дома: две двери, ящики, тумбочка."""
    s = f'<rect width="{W}" height="{H}" fill="#7e8a7a"/>'
    s += f'<rect width="{W}" height="520" fill="#9aa894"/>'
    s += f'<rect y="500" width="{W}" height="26" fill="#6d7a68" {o(4)}/>'
    s += f'<rect y="900" width="{W}" height="180" fill="#6a6358"/>'
    for c in range(14):
        s += f'<rect x="{c*140}" y="900" width="132" height="180" fill="#746c60" opacity="{.5 if c%2 else .25}"/>'
    mig = .55 + .45 * (1 if abs(A.w(t, 1.9)) > .25 else .25)
    s += f'<circle cx="430" cy="90" r="46" fill="{SVET}" opacity="{mig:.2f}"/>'
    s += teplo(430, 130, 520, 460, .8 * mig)
    for i, x in enumerate((90, 470)):
        s += f'<rect x="{x}" y="250" width="300" height="650" rx="6" fill="url(#derev)" {o(8)}/>'
        s += f'<rect x="{x+26}" y="286" width="248" height="250" rx="6" fill="none" stroke="{DOSKA2}" stroke-width="8"/>'
        s += f'<circle cx="{x+252}" cy="600" r="13" fill="url(#zhel)" {o(4)}/>'
        s += f'<rect x="{x+60}" y="310" width="180" height="56" rx="6" fill="{ZHELEZ}" opacity=".8" {o(4)}/>'
    s += f'<rect x="100" y="880" width="280" height="30" rx="8" fill="{TKAN}" {o(5)}/>'
    # тумбочка с будильником
    s += ten(1030, 970, 150, 20, .45)
    s += f'<rect x="900" y="700" width="260" height="250" rx="10" fill="url(#derev)" {o(7)}/>'
    s += hodiki(1030, 640, t, .85)
    s += ramka_pp("levo", "#2a2d28", .45)
    s += kvartira_veschi(1300, 900, 560, t, 58)
    s += vinetka(.4)
    return s


def yarmarka(t):
    """Осенний торговый ряд под навесом: самовар, шаль, сапоги, сундук."""
    s = nebo("den", t, False)
    s += oblaka(t, 170, 5, 33, .5, "#dfe7ee", 11)
    s += f'<path d="M0,780 Q480,756 960,780 Q1440,804 1920,776 L1920,1080 L0,1080 Z" fill="#8a8470" {o(5)}/>'
    # навес
    s += f'<path d="M-20,260 L400,150 L860,260 Z" fill="{TKAN}" {o(8)}/>'
    for i in range(7):
        s += f'<path d="M{-20+i*130},262 l{(400-(-20+i*130))*.26:.0f},-70" stroke="#8c2026" stroke-width="7" opacity=".5"/>'
    for x in (40, 790):
        s += f'<rect x="{x}" y="260" width="34" height="560" fill="url(#derev)" {o(6)}/>'
    s += ten(420, 880, 350, 26, .5)
    s += f'<rect x="60" y="640" width="740" height="200" rx="10" fill="url(#derev)" {o(8)}/>'
    s += f'<path d="M60,638 q370,-28 740,0 q-370,22 -740,0 Z" fill="url(#rush)" {o(5)}/>'
    # самовар блестит
    s += ten(220, 646, 80, 14, .45)
    s += (f'<path d="M150,636 q-26,-150 70,-176 q96,26 70,176 Z" fill="url(#med)" {o(7)}/>'
          f'<ellipse cx="220" cy="458" rx="54" ry="18" fill="url(#zol)" {o(6)}/>'
          f'<rect x="196" y="420" width="48" height="42" rx="10" fill="url(#med)" {o(5)}/>'
          f'<ellipse cx="196" cy="540" rx="18" ry="30" fill="#f4dba0" opacity="{.3+.6*abs(A.w(t,2.6)):.2f}"/>')
    # шаль колышется
    dx = 10 * A.w(t, 4.2)
    s += (f'<path d="M400,470 q{60+dx:.0f},160 -10,330 q-90,-170 -40,-330 Z" fill="{TKAN}" {o(7)}/>'
          f'<path d="M398,520 q40,120 -10,230" fill="none" stroke="{ZOL}" stroke-width="7" opacity=".7"/>')
    for i, x in enumerate((560, 640)):
        s += (f'<path d="M{x},636 v-150 q34,-16 56,0 v150 Z" fill="#3a2b22" {o(6)}/>'
              f'<path d="M{x-10},636 h80 v22 h-80 Z" fill="#241a14" {o(5)}/>')
    s += f'<rect x="700" y="700" width="180" height="130" rx="10" fill="url(#derev)" {o(7)}/>'
    s += f'<path d="M700,702 q90,-40 180,0" fill="url(#med)" {o(6)}/>'
    s += f'<g opacity=".5">{sneg_letit(t, 10, 37, .5, .4)}</g>'
    s += mebel_hlam(1040, 900, 820, t, 31)
    s += ulica_dal(900, 620, 1000, t, False, 32)
    s += vinetka(.4)
    return s


def izba_den(t):
    """Изба днём: прялка, полка с копилкой, печь. Свет из окна."""
    s = brevna(-20, -20, W + 40, H + 40, 118)
    s += f'<rect width="{W}" height="{H}" fill="#f2e6cc" opacity=".16"/>'
    s += polovicy(880)
    s += luch(620, 0, 230, 1080, t, .24)
    s += pech(560, 300, 300, 580, t, True, True)
    s += polka(70, 400, 420)
    s += krynka(140, 394, .7)
    # копилка, в неё падает монета
    s += (f'<path d="M250,394 q-28,-120 48,-134 q74,14 48,134 Z" fill="url(#glina)" {o(7)}/>'
          f'<rect x="276" y="268" width="44" height="12" rx="5" fill="#4a2e16"/>')
    p = ((t * .55) % 1.0)
    s += (f'<ellipse cx="298" cy="{180+p*86:.0f}" rx="20" ry="14" fill="url(#med)"'
          f' opacity="{1-max(0,(p-.85)/.15):.2f}" {o(4)}/>')
    s += krynka(400, 394, .62)
    # прялка: колесо вертится
    s += ten(240, 880, 130, 20, .45)
    s += f'<rect x="150" y="700" width="190" height="24" rx="8" fill="url(#derev)" {o(6)}/>'
    s += f'<rect x="166" y="724" width="22" height="150" fill="url(#derev)" {o(5)}/>'
    s += f'<rect x="302" y="724" width="22" height="150" fill="url(#derev)" {o(5)}/>'
    ang = (t * 150) % 360
    s += (f'<g transform="rotate({ang:.0f} 250 640)">'
          f'<circle cx="250" cy="640" r="92" fill="none" stroke="url(#derev)" stroke-width="14"/>')
    for i in range(8):
        a = i * math.pi / 4
        s += (f'<line x1="250" y1="640" x2="{250+92*math.cos(a):.0f}" y2="{640+92*math.sin(a):.0f}"'
              f' stroke="#8a5f3c" stroke-width="7"/>')
    s += "</g>"
    s += f'<circle cx="250" cy="640" r="16" fill="url(#med)" {o(4)}/>'
    s += utvar_izby(1000, 700, 860, t, 11)
    s += mebel_hlam(900, 1010, 560, t, 12)
    s += vinetka(.36)
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
    """Замёрзшая река на рассвете, сани, рыбацкая артель вдали."""
    s = nebo("rassv", t, False)
    s += oblaka(t, 240, 4, 41, .38, "#f0d6b8", 6)
    s += f'<ellipse cx="1350" cy="520" rx="110" ry="110" fill="#ffe6bb" opacity=".6"/>'
    s += f'<path d="M0,560 Q500,538 1000,556 Q1460,572 1920,548 L1920,640 L0,640 Z" fill="#4e5f74" {o(5)}/>'
    s += f'<rect y="620" width="{W}" height="460" fill="url(#led)"/>'
    for i in range(9):
        s += (f'<path d="M{-120+i*240},620 l{200+i*18},460" stroke="#ffffff" stroke-width="4" opacity=".28"/>')
    s += f'<path d="M0,640 Q500,668 1000,644 Q1460,624 1920,652" fill="none" stroke="#ffffff" stroke-width="7" opacity=".5"/>'
    # сани крупно слева
    s += ten(360, 930, 220, 20, .4)
    s += (f'<path d="M160,900 h420 l-30,-120 h-360 Z" fill="url(#derev)" {o(8)}/>'
          f'<path d="M140,912 q230,34 460,0" fill="none" stroke="#6b4428" stroke-width="18" stroke-linecap="round"/>'
          f'<path d="M200,780 h320 v-60 h-320 Z" fill="url(#rush)" {o(6)}/>')
    # артель идёт вдали
    for i, x in enumerate((1120, 1230, 1330)):
        s += siluet(x + 6 * A.w(t, 3.0, i * .3), 700, 150, "#2b3444", .85, kant="#f0d6b8")
    s += f'<g opacity=".7">{tuman(t, 600, .34, "#e8eef6")}</g>'
    s += ramka_pp("levo", "#2b3444", .35)
    s += ulica_dal(60, 560, 520, t, True, 51)
    s += vinetka(.36)
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
    """Три комнаты в ряд: кладовка с дрелью, ванная, комната с телевизором."""
    s = f'<rect width="{W}" height="{H}" fill="#6c6358"/>'
    tr = W / 3
    for i in range(3):
        x = i * tr
        s += f'<rect x="{x:.0f}" width="{tr-8:.0f}" height="{H}" fill="{["#8a7e6e","#7e8c90","#7a7284"][i]}"/>'
        s += f'<rect x="{x:.0f}" y="880" width="{tr-8:.0f}" height="200" fill="url(#pol)" {o(4)}/>'
    s += f'<rect x="{tr-10:.0f}" width="16" height="{H}" fill="{K}" opacity=".7"/>'
    s += f'<rect x="{tr*2-10:.0f}" width="16" height="{H}" fill="{K}" opacity=".7"/>'
    # дрель трясётся
    sh = 7 * A.w(t, .18)
    s += (f'<g transform="translate({sh:.1f},{sh*.6:.1f})">'
          f'{ten(300, 740, 110, 16, .45)}'
          f'<rect x="200" y="580" width="230" height="110" rx="24" fill="{ORA}" {o(8)}/>'
          f'<rect x="420" y="612" width="190" height="34" rx="12" fill="{ZHELEZ}" {o(6)}/>'
          f'<rect x="250" y="690" width="90" height="120" rx="16" fill="#2b2b2b" {o(7)}/></g>')
    for i in range(5):
        s += (f'<path d="M{640+i*26},{566+i*14} l40,-28" stroke="{SVET}" stroke-width="7"'
              f' opacity="{.3+.6*abs(A.w(t,.5,i*.2)):.2f}"/>')
    # стиральная машина: барабан крутится
    cx = tr + tr / 2
    s += ten(cx, 920, 150, 20, .45)
    s += f'<rect x="{cx-170:.0f}" y="520" width="340" height="390" rx="16" fill="url(#krem)" {o(8)}/>'
    s += f'<circle cx="{cx:.0f}" cy="720" r="118" fill="{ZHELEZ}" {o(7)}/>'
    ang = (t * 260) % 360
    s += (f'<g transform="rotate({ang:.0f} {cx:.0f} 720)">'
          f'<circle cx="{cx:.0f}" cy="720" r="92" fill="#cfe0ea" opacity=".7"/>'
          f'<path d="M{cx-60:.0f},690 q60,40 120,-20" fill="none" stroke="{TKAN}" stroke-width="22"/></g>')
    s += f'<rect x="{cx-140:.0f}" y="552" width="120" height="30" rx="8" fill="{ZHELEZ}" {o(4)}/>'
    # телевизор мигает
    cx2 = tr * 2 + tr / 2
    s += ten(cx2, 900, 160, 20, .45)
    s += f'<rect x="{cx2-200:.0f}" y="480" width="400" height="300" rx="18" fill="#2b2b33" {o(8)}/>'
    fl = .4 + .6 * abs(A.w(t, .42))
    s += f'<rect x="{cx2-170:.0f}" y="510" width="340" height="240" rx="8" fill="#9fd0e8" opacity="{fl:.2f}"/>'
    s += teplo(cx2, 630, 420, 330, .5 * fl)
    s += f'<rect x="{cx2-40:.0f}" y="780" width="80" height="110" fill="#2b2b33" {o(6)}/>'
    for i in range(4):
        s += (f'<path d="M{cx2+220+i*30:.0f},{560-i*20} q40,{40+i*20} 0,{80+i*40}" fill="none"'
              f' stroke="#cfe0ea" stroke-width="6" opacity="{.2+.5*abs(A.w(t,1.1,i*.25)):.2f}"/>')
    s += vinetka(.4)
    return s


def doroga(t):
    """Серый ноябрьский день: обледеневшая разъезженная дорога, изба, калитка."""
    s = nebo("den", t, False)
    s += oblaka(t, 180, 6, 51, .55, "#b9c4ce", 8)
    s += f'<path d="M0,620 Q480,596 960,618 Q1440,638 1920,608 L1920,1080 L0,1080 Z" fill="#6f7262" {o(5)}/>'
    s += izba_snaruzhi(60, 660, 520, t, True, True, 3)
    s += pleten(620, 700, 240, 130, 5)
    s += f'<rect x="860" y="560" width="30" height="150" fill="url(#derev)" {o(5)}/>'
    # дорога в перспективе
    s += (f'<path d="M700,620 L1180,620 L1920,1080 L300,1080 Z" fill="#5c5e52" {o(6)}/>')
    for i in range(5):
        u = i / 4
        s += (f'<path d="M{760+u*340:.0f},630 L{520+u*1200:.0f},1080" fill="none"'
              f' stroke="#4a4c42" stroke-width="{10+u*26:.0f}" opacity=".8"/>')
    # лёд в колеях блестит
    for i in range(6):
        u = i / 5
        x = 800 + u * 700; y = 700 + u * 330
        s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{40+u*70:.0f}" ry="{10+u*14:.0f}"'
              f' fill="#cfe0ea" opacity="{.3+.5*abs(A.w(t,2.4,i*.3)):.2f}"/>')
    s += f'<g opacity=".6">{tuman(t, 640, .3, "#c8d2da")}</g>'
    s += ramka_pp("levo", "#3a3b32", .4)
    s += ulica_dal(1080, 620, 820, t, True, 38)
    s += vinetka(.42)
    return s


def kalitka_zasov(t):
    """Калитка со стороны двора, дубовый засов в скобах — крупно."""
    s = nebo("den", t, False)
    s += f'<rect y="820" width="{W}" height="260" fill="#6f7262" {o(5)}/>'
    s += pleten(-40, 900, 460, 300, 7)
    s += pleten(1140, 900, 820, 300, 11)
    s += ten(700, 1000, 300, 26, .45)
    s += f'<rect x="400" y="140" width="620" height="880" rx="10" fill="#241a12" {o(9)}/>'
    s += doski(412, 152, 596, 856, 96, True, "derev")
    s += f'<path d="M412,320 L1008,200" stroke="#6b4428" stroke-width="26" opacity=".8"/>'
    s += f'<path d="M412,760 L1008,880" stroke="#6b4428" stroke-width="26" opacity=".8"/>'
    # скобы и засов
    for x in (470, 900):
        s += f'<path d="M{x},480 v120 h56 v-120" fill="none" stroke="url(#zhel)" stroke-width="22" stroke-linecap="round"/>'
    dv = 70 * A.ease(A.seg(t, 1.2, 1.4))
    s += (f'<rect x="{360+dv:.0f}" y="508" width="640" height="64" rx="14" fill="url(#derev)" {o(8)}/>'
          f'<rect x="{376+dv:.0f}" y="524" width="600" height="16" rx="6" fill="#6b4428" opacity=".6"/>')
    s += f'<circle cx="{980+dv:.0f}" cy="540" r="26" fill="url(#zhel)" {o(6)}/>'
    s += f'<g opacity=".6">{sneg_letit(t, 14, 53, .5, .5)}</g>'
    s += ramka_pp("levo", "#2b2c26", .45)
    s += ulica_dal(1100, 820, 800, t, True, 39)
    s += vinetka(.44)
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
    """Двор: поленница под навесом, крыльцо избы."""
    s = nebo("den", t, False)
    s += oblaka(t, 180, 5, 71, .5, "#cfd8e2", 7)
    s += f'<path d="M0,740 Q480,716 960,740 Q1440,764 1920,736 L1920,1080 L0,1080 Z" fill="#6f7262" {o(5)}/>'
    s += sneg_lezhit(800, 18, "#dfe8f2")
    s += brevna(880, 240, 1060, 640, 94)
    # крыльцо
    s += ten(1250, 1000, 280, 24, .45)
    for i in range(4):
        s += (f'<rect x="{1020+i*18}" y="{880-i*60}" width="{420-i*36}" height="60" rx="6"'
              f' fill="url(#derev)" {o(6)}/>')
    s += dver(1180, 400, 260, 290, 0, "url(#derev)")
    # поленница под навесом
    s += f'<path d="M20,300 L440,220 L840,300 Z" fill="{DOSKA2}" {o(7)}/>'
    for x in (50, 790):
        s += f'<rect x="{x}" y="300" width="34" height="580" fill="url(#derev)" {o(6)}/>'
    r = random.Random(29)
    for row in range(7):
        for c in range(9):
            x = 110 + c * 74 + (36 if row % 2 else 0)
            y = 840 - row * 76
            s += (f'<ellipse cx="{x}" cy="{y}" rx="36" ry="34" fill="url(#derev)" {o(5)}/>'
                  f'<ellipse cx="{x}" cy="{y}" rx="22" ry="20" fill="#a8744a" {o(3)}/>'
                  f'<path d="M{x-16},{y-10} l32,20 M{x-14},{y+12} l28,-26" stroke="#7a4e2a" stroke-width="4"/>')
    s += f'<g opacity=".6">{sneg_letit(t, 16, 73, .6, .5)}</g>'
    s += ulica_dal(880, 740, 420, t, True, 41)
    s += vinetka(.4)
    return s


def dvor_bulochnaya(t):
    """Вечерний двор многоэтажки: хлебный киоск, подъезд."""
    s = nebo("noch", t, True, 77)
    s += panelka(960, 940, 960, t, 6, True, 13)
    s += f'<rect y="900" width="{W}" height="180" fill="#3b4250"/>'
    s += sneg_lezhit(900, 16, "#cfd8e6")
    # киоск
    s += ten(400, 1000, 280, 24, .5)
    s += f'<rect x="120" y="440" width="580" height="470" rx="12" fill="{TKAN2}" {o(8)}/>'
    s += f'<path d="M90,440 L410,330 L730,440 Z" fill="#3a5570" {o(7)}/>'
    s += f'<rect x="170" y="520" width="480" height="250" rx="8" fill="url(#stekl)" opacity=".85" {o(7)}/>'
    s += teplo(410, 640, 420, 330, .9)
    for i, x in enumerate((250, 400, 550)):
        s += karavay(x, 740, .62, False)
    s += (f'<rect x="200" y="432" width="420" height="80" rx="10" fill="url(#zol)" {o(6)}/>'
          f'<text x="410" y="492" font-family="DejaVu Sans" font-size="54" fill="{K}"'
          f' text-anchor="middle" letter-spacing="10">ХЛЕБ</text>')
    # фонарь двора мигает
    mig = .5 + .5 * (1 if abs(A.w(t, 2.3)) > .3 else .3)
    s += f'<rect x="840" y="300" width="18" height="600" fill="{ZHELEZ}" {o(5)}/>'
    s += f'<ellipse cx="849" cy="300" rx="70" ry="30" fill="{SVET}" opacity="{mig:.2f}" {o(5)}/>'
    s += teplo(849, 420, 300, 420, .7 * mig)
    s += sneg_letit(t, 26, 79, .7, .6)
    s += ulica_dal(60, 900, 320, t, True, 49)
    s += vinetka(.46)
    return s


def palto(t):
    """Прихожая: крупно драповое пальто на крючке, шапка, шарф."""
    s = f'<rect width="{W}" height="{H}" fill="#7e7265"/>'
    for c in range(10):
        s += f'<rect x="{c*192}" width="180" height="{H}" fill="#8c8073" opacity="{.4 if c%2 else .15}"/>'
    s += f'<rect y="920" width="{W}" height="160" fill="url(#pol)" {o(5)}/>'
    s += teplo(430, 460, 560, 560, .55)
    s += f'<rect x="90" y="220" width="720" height="40" rx="10" fill="url(#derev)" {o(7)}/>'
    for x in (200, 420, 640):
        s += f'<path d="M{x},260 v50 q0,22 24,22" fill="none" stroke="url(#zhel)" stroke-width="16" stroke-linecap="round"/>'
    kach = 1.3 * A.w(t, 5.2)
    s += (f'<g transform="rotate({kach:.2f} 420 300)">'
          f'{ten(420, 980, 180, 18, .4)}'
          f'<path d="M300,320 q120,-54 240,0 l56,110 l-70,40 l6,420 q-128,36 -256,0 l6,-420 l-70,-40 Z"'
          f' fill="#4a5466" {o(9)}/>'
          f'<path d="M420,330 v530" stroke="#2f3744" stroke-width="7" opacity=".8"/>')
    for i in range(4):
        s += f'<circle cx="398" cy="{470+i*104}" r="15" fill="#2f3744" {o(4)}/>'
    s += (f'<path d="M300,320 q60,100 120,60 q60,40 120,-60 l-40,-20 q-80,70 -160,0 Z" fill="#5a6678" {o(6)}/></g>')
    # шапка и шарф
    s += (f'<ellipse cx="640" cy="360" rx="96" ry="76" fill="#5a4030" {o(7)}/>'
          f'<path d="M550,380 q90,60 180,0 l0,40 q-90,56 -180,0 Z" fill="#6d4e3a" {o(6)}/>')
    sw = 9 * A.w(t, 4.4)
    s += (f'<g transform="rotate({sw:.1f} 200 300)">'
          f'<path d="M170,300 q70,150 20,330 q-70,-160 -20,-330 Z" fill="{TKAN}" {o(7)}/>')
    for i in range(4):
        s += f'<path d="M{178+i*2},{360+i*80} q30,14 46,2" fill="none" stroke="#8c2026" stroke-width="7"/>'
    s += "</g>"
    s += ramka_pp("pravo", "#2a251e", .4)
    s += kvartira_veschi(1000, 920, 840, t, 62)
    s += vinetka(.42)
    return s


# ─────────────────────── 5. ДЕЛА ЭТОГО ДНЯ ───────────────────────
def ptichiy_dvor(t):
    """Морозное утро, птичий двор в инее, жердь."""
    s = nebo("rassv", t, False)
    s += oblaka(t, 200, 4, 81, .4, "#f0dcc4", 6)
    s += f'<path d="M0,700 Q480,676 960,700 Q1440,724 1920,696 L1920,1080 L0,1080 Z" fill="#8a8a6e" {o(5)}/>'
    s += f'<g opacity=".8">{sneg_lezhit(740, 14, "#e6eef6")}</g>'
    s += brevna(1120, 320, 820, 420, 86)
    s += f'<path d="M1100,320 L1520,210 L1940,320 Z" fill="{DOSKA2}" {o(7)}/>'
    s += pleten(60, 780, 520, 170, 8)
    # жердь
    s += f'<rect x="120" y="560" width="620" height="26" rx="12" fill="url(#derev)" {o(6)}/>'
    for x in (160, 700):
        s += f'<rect x="{x}" y="586" width="24" height="200" fill="url(#derev)" {o(5)}/>'
    for i, x in enumerate((240, 380, 530)):
        s += kura(x, 556, t, .72, i * .3, ["#e2d6c2", "#d8c0a0", "#efe6d2"][i])
    for i, x in enumerate((340, 520, 650)):
        s += kura(x, 900, t, .95, i * .4 + .15, ["#efe6d2", "#e2d6c2", "#cdb89a"][i])
    # зерно и пар от дыхания
    r = random.Random(31)
    for i in range(18):
        s += (f'<circle cx="{r.uniform(260,700):.0f}" cy="{r.uniform(900,1000):.0f}" r="5"'
              f' fill="{ZOL}" opacity=".85"/>')
    s += f'<g opacity=".45">{par(420, 860, t, 3, .4, 150, .35, .6)}</g>'
    # иней искрит
    for i in range(20):
        x, y = r.uniform(0, W), r.uniform(700, 1060)
        s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#ffffff"'
              f' opacity="{.2+.8*abs(A.w(t,1.5,i*.11)):.2f}"/>')
    s += ulica_dal(840, 700, 300, t, True, 43)
    s += vinetka(.38)
    return s


def kuryatnik_soloma(t):
    """Низкий сарай-птичник, обложенный снопами соломы, оконце."""
    s = nebo("den", t, False)
    s += oblaka(t, 170, 4, 83, .45, "#cfd8e2", 7)
    s += f'<path d="M0,720 Q480,700 960,722 Q1440,742 1920,714 L1920,1080 L0,1080 Z" fill="#7a7a62" {o(5)}/>'
    s += sneg_lezhit(790, 16, "#e2eaf4")
    s += brevna(70, 380, 760, 420, 80)
    s += f'<path d="M30,380 L450,250 L870,380 Z" fill="url(#solom)" {o(8)}/>'
    for i in range(16):
        s += (f'<path d="M{60+i*52},378 l{(450-(60+i*52))*.22:.0f},-56" stroke="#a07c2e"'
              f' stroke-width="6" opacity=".6"/>')
    s += okno_izby(540, 470, 180, 150, t, svet=True, moroz=.25)
    s += f'<rect x="170" y="520" width="220" height="280" rx="8" fill="#2a1f14" {o(7)}/>'
    s += teplo(280, 680, 260, 280, .7)
    # снопы соломы вдоль стены
    r = random.Random(37)
    for i in range(7):
        x = 90 + i * 112
        kach = 1.6 * A.w(t, 4.0 + i * .3, i * .2)
        s += (f'<g transform="rotate({kach:.2f} {x+50} 800)">'
              f'<path d="M{x},800 q50,-190 100,0 Z" fill="url(#solom)" {o(6)}/>')
        for j in range(5):
            s += (f'<path d="M{x+14+j*18},798 q{6-j*2},-120 {14-j*3},-150" fill="none"'
                  f' stroke="#c9a349" stroke-width="5"/>')
        s += f'<path d="M{x+6},740 q44,-20 88,0" fill="none" stroke="{TKAN}" stroke-width="9"/></g>'
    for i, x in enumerate((900, 1010)):
        s += kura(x, 900, t, .85, i * .35)
    s += f'<g opacity=".5">{sneg_letit(t, 14, 89, .5, .5)}</g>'
    s += ulica_dal(1180, 720, 740, t, True, 44)
    s += vinetka(.4)
    return s


def okno_balkon(t):
    """Окно панельного дома с балконом, подоконник с геранью."""
    s = f'<rect width="{W}" height="{H}" fill="#9aa3a8"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#beton)" opacity=".75"/>'
    for r_ in range(8):
        s += f'<line x1="0" y1="{r_*140}" x2="{W}" y2="{r_*140}" stroke="#7a8288" stroke-width="5" opacity=".5"/>'
    vid = (f'<rect x="120" y="180" width="680" height="560" fill="#6f8aa6"/>'
           + _oblaka(t, 300, 3, 91, .5, "#e8eef6", 6)
           + f'<rect x="120" y="560" width="680" height="180" fill="#5c6a54"/>')
    s += okno_izby(120, 180, 680, 560, t, vid=vid, moroz=.35, svet=False)
    s += f'<rect x="70" y="740" width="790" height="56" rx="10" fill="url(#krem)" {o(8)}/>'
    # герань: листья покачиваются, цветок пульсирует
    for i, x in enumerate((220, 420, 640)):
        kach = 3.0 * A.w(t, 4.2, i * .3)
        s += (f'<g transform="rotate({kach:.2f} {x} 740)">'
              f'<path d="M{x-46},738 l14,-96 h64 l14,96 Z" fill="url(#glina)" {o(6)}/>')
        for j in range(5):
            a = -2.2 + j * .55
            s += (f'<ellipse cx="{x+math.cos(a)*54:.0f}" cy="{620+math.sin(a)*34:.0f}" rx="30" ry="22"'
                  f' fill="{ZEL2}" {o(4)}/>')
        s += (f'<circle cx="{x}" cy="{566}" r="{24+3*A.w(t,2.2,i*.2):.1f}" fill="{KRAS}" {o(4)}/>'
              f'<circle cx="{x-18}" cy="{580}" r="16" fill="#e8564a" {o(3)}/>'
              f'<circle cx="{x+20}" cy="{578}" r="16" fill="#e8564a" {o(3)}/></g>')
    # балконная дверь и перила справа
    s += f'<rect x="1120" y="140" width="420" height="760" rx="8" fill="url(#stekl)" opacity=".7" {o(8)}/>'
    for i in range(7):
        s += f'<rect x="{1180+i*52}" y="620" width="16" height="280" rx="6" fill="{ZHELEZ}" {o(4)}/>'
    s += f'<rect x="1150" y="600" width="370" height="24" rx="8" fill="{ZHELEZ}" {o(5)}/>'
    s += f'<rect y="900" width="{W}" height="180" fill="url(#pol)" {o(5)}/>'
    s += kvartira_veschi(900, 900, 200, t, 63)
    s += vinetka(.4)
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
    """Заснеженный балкон, деревянный утеплённый ящик с картошкой."""
    s = nebo("noch", t, True, 97)
    s += panelka(1180, 1080, 740, t, 6, True, 17)
    s += f'<rect y="820" width="{W}" height="260" fill="url(#beton)" {o(6)}/>'
    s += f'<rect y="780" width="{W}" height="48" fill="#8a9298" {o(5)}/>'
    for i in range(9):
        s += f'<rect x="{60+i*92}" y="400" width="18" height="384" rx="7" fill="{ZHELEZ}" {o(4)}/>'
    s += f'<rect x="40" y="376" width="830" height="26" rx="10" fill="{ZHELEZ}" {o(5)}/>'
    s += sneg_lezhit(790, 14, "#e2eaf4")
    # ящик
    s += ten(420, 1010, 280, 22, .5)
    s += f'<rect x="150" y="560" width="560" height="440" rx="10" fill="url(#derev)" {o(9)}/>'
    s += doski(160, 570, 540, 420, 90, True, "derev")
    s += f'<path d="M140,560 q290,-50 580,0 l0,52 q-290,-44 -580,0 Z" fill="{TKAN}" opacity=".92" {o(6)}/>'
    otkr = A.ease(A.seg(t, 1.6, 1.6))
    s += (f'<g transform="rotate({-28*otkr:.1f} 160 556)">'
          f'<rect x="140" y="520" width="580" height="46" rx="10" fill="url(#derev)" {o(7)}/></g>')
    if otkr > .35:
        s += f'<g opacity="{(otkr-.35)/.65:.2f}">{kartoshka(420, 600, t, 10, 6, 1.1)}</g>'
    s += f'<g opacity=".8">{sneg_letit(t, 22, 99, .7, .5)}</g>'
    s += kvartira_veschi(820, 780, 300, t, 67)
    s += vinetka(.46)
    return s


def prazdnichnyj_stol(t):
    """Стол под вышитой скатертью, вид сверху: лапша, курник, рыбный пирог."""
    s = f'<rect width="{W}" height="{H}" fill="url(#pol)"/>'
    s += polovicy(0)
    s += teplo(420, 540, 700, 620, .75)
    s += ten(440, 1010, 420, 30, .5)
    s += f'<rect x="60" y="180" width="780" height="820" rx="26" fill="url(#rush)" {o(9)}/>'
    for i in range(10):
        y = 212 + i * 84
        s += (f'<path d="M80,{y} q58,-26 116,0 q58,26 116,0 q58,-26 116,0 q58,26 116,0'
              f' q58,-26 116,0 q58,26 116,0" fill="none" stroke="{TKAN}" stroke-width="6" opacity=".6"/>')
    # лапша в миске: пар идёт
    s += f'<circle cx="250" cy="400" r="130" fill="url(#glina)" {o(7)}/>'
    s += f'<circle cx="250" cy="400" r="104" fill="#e8cf96" {o(5)}/>'
    for i in range(9):
        a = i * .7
        s += (f'<path d="M{200+i*12},{360+20*math.sin(a):.0f} q30,{26+6*A.w(t,3,i*.2):.0f} 60,0"'
              f' fill="none" stroke="#f4e4b8" stroke-width="7"/>')
    s += f'<g opacity=".6">{par(250, 300, t, 4, .55, 220, .9, .8)}</g>'
    # курник
    s += f'<ellipse cx="610" cy="430" rx="160" ry="120" fill="url(#med)" {o(7)}/>'
    s += f'<ellipse cx="610" cy="406" rx="120" ry="80" fill="#e0a95c" {o(5)}/>'
    s += f'<path d="M530,400 q80,-44 160,0" fill="none" stroke="#f2cf8c" stroke-width="8"/>'
    s += f'<g opacity=".5">{par(610, 330, t, 3, .5, 180, .7, .8)}</g>'
    # рыбный пирог
    s += f'<rect x="150" y="660" width="560" height="220" rx="34" fill="url(#med)" {o(7)}/>'
    for i in range(6):
        s += f'<path d="M{200+i*86},700 q26,60 0,140" fill="none" stroke="#c98c42" stroke-width="9"/>'
    s += f'<ellipse cx="430" cy="690" rx="70" ry="22" fill="#e0a95c" {o(4)}/>'
    # свеча и блики
    s += svecha(880, 560, t, .4, 1.1)
    s += utvar_izby(1040, 700, 820, t, 33)
    s += vinetka(.42)
    return s


def kuhnya_duhovka(t):
    """Городская кухня: стол, духовка со светящимся окошком, чайник."""
    s = f'<rect width="{W}" height="{H}" fill="#b4c0b4"/>'
    for r_ in range(9):
        for c in range(16):
            s += (f'<rect x="{c*122+4}" y="{r_*122+4}" width="112" height="112" rx="6"'
                  f' fill="#c6d2c6" opacity="{.55 if (r_+c)%2 else .25}"/>')
    s += f'<rect y="900" width="{W}" height="180" fill="url(#pol)" {o(5)}/>'
    s += teplo(420, 640, 620, 520, .62)
    # духовка
    s += ten(400, 1000, 260, 22, .5)
    s += f'<rect x="130" y="480" width="560" height="520" rx="14" fill="url(#krem)" {o(9)}/>'
    s += f'<rect x="170" y="560" width="480" height="300" rx="10" fill="#2b2b33" {o(7)}/>'
    gl = .6 + .4 * abs(A.w(t, 2.4))
    s += f'<rect x="196" y="586" width="428" height="248" rx="8" fill="{ORA}" opacity="{gl*.8:.2f}"/>'
    s += teplo(410, 710, 420, 300, gl)
    s += f'<rect x="250" y="720" width="320" height="90" rx="18" fill="url(#med)" {o(5)}/>'
    s += f'<rect x="170" y="500" width="480" height="40" rx="10" fill="{ZHELEZ}" {o(5)}/>'
    for i, x in enumerate((230, 330, 430, 530)):
        s += f'<circle cx="{x}" cy="520" r="15" fill="url(#zhel)" {o(4)}/>'
    s += f'<rect x="150" y="900" width="520" height="30" rx="10" fill="{ZHELEZ}" {o(5)}/>'
    # стол и чайник
    s += stol(840, 660, 600, 36)
    s += (f'<path d="M1020,658 q-20,-120 80,-134 q100,14 80,134 Z" fill="url(#zhel)" {o(7)}/>'
          f'<path d="M1180,600 q50,-16 40,40" fill="none" stroke="{ZHELEZ}" stroke-width="12"/>'
          f'<rect x="1072" y="508" width="56" height="26" rx="10" fill="{ZHELEZ}" {o(4)}/>')
    s += f'<g opacity=".55">{par(1200, 600, t, 4, .55, 280, .7, .9)}</g>'
    s += krynka(1320, 650, .7)
    s += kvartira_veschi(1500, 900, 400, t, 60)
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
    """Длинный стол под клеёнкой, разные стулья, абажур — бабушкин дом."""
    s = f'<rect width="{W}" height="{H}" fill="#9a8c78"/>'
    for c in range(12):
        s += f'<rect x="{c*160}" width="150" height="{H}" fill="#a8997f" opacity="{.4 if c%2 else .15}"/>'
    s += f'<rect y="880" width="{W}" height="200" fill="url(#pol)" {o(5)}/>'
    s += lampa(620, 520, t, 1.5, abazhur=True)
    s += teplo(620, 620, 760, 560, .8)
    s += ten(760, 1020, 620, 26, .45)
    # стол длинный
    s += f'<rect x="120" y="640" width="1480" height="46" rx="12" fill="url(#derev)" {o(9)}/>'
    s += f'<path d="M120,638 q740,-36 1480,0 q-740,28 -1480,0 Z" fill="{TKAN}" opacity=".85" {o(5)}/>'
    for i in range(16):
        s += (f'<circle cx="{170+i*94}" cy="{652}" r="12" fill="url(#krem)" opacity=".5"/>')
    for x in (200, 1480):
        s += f'<rect x="{x}" y="686" width="36" height="250" fill="url(#derev)" {o(6)}/>'
    # разные стулья
    for i, (x, col, h_) in enumerate(((180, "#6d4e3a", 290), (430, TKAN2, 250),
                                      (700, "#5c6a54", 310), (1180, "#7a5436", 270),
                                      (1430, TKAN, 240))):
        s += f'<rect x="{x}" y="{940-h_*.35:.0f}" width="150" height="26" rx="8" fill="{col}" {o(6)}/>'
        s += f'<rect x="{x+10}" y="{940-h_:.0f}" width="26" height="{h_*.68:.0f}" rx="8" fill="{col}" {o(5)}/>'
        s += f'<rect x="{x+114}" y="{940-h_:.0f}" width="26" height="{h_*.68:.0f}" rx="8" fill="{col}" {o(5)}/>'
        s += f'<rect x="{x+14}" y="{940-h_:.0f}" width="124" height="30" rx="10" fill="{col}" {o(5)}/>'
    # на столе: чашки, пар
    for i, x in enumerate((420, 700, 980)):
        s += (f'<path d="M{x-40},636 v-70 q40,-16 80,0 v70 Z" fill="url(#krem)" {o(5)}/>'
              f'<path d="M{x+40},580 q30,16 0,40" fill="none" stroke="{KREM}" stroke-width="10"/>')
        s += f'<g opacity=".45">{par(x, 560, t, 3, .5, 140, .6, .5)}</g>'
    s += karavay(1240, 634, .75)
    s += kvartira_veschi(60, 880, 420, t, 61)
    s += vinetka(.42)
    return s


# ─────────────────────── 6. ПОГОДА ПО ПРИМЕТАМ ───────────────────────
def krylco_rassvet(t):
    """Синий рассвет, туман над огородами, крыльцо избы."""
    s = nebo("rassv", t, False)
    s += oblaka(t, 250, 4, 107, .4, "#e8d0b4", 5)
    s += f'<path d="M0,720 Q480,694 960,718 Q1440,742 1920,710 L1920,1080 L0,1080 Z" fill="#5c6a54" {o(5)}/>'
    s += brevna(60, 180, 700, 620, 92)
    s += f'<path d="M20,180 L410,40 L800,180 Z" fill="{DOSKA2}" {o(8)}/>'
    s += okno_izby(150, 300, 220, 190, t, svet=True, moroz=.4)
    s += dver(460, 330, 240, 470, 0, "url(#derev)")
    for i in range(4):
        s += (f'<rect x="{480-i*14}" y="{800+i*58}" width="{250+i*28}" height="58" rx="6"'
              f' fill="url(#derev)" {o(6)}/>')
    # грядки и туман
    for i in range(6):
        y = 780 + i * 52
        s += (f'<path d="M900,{y} q240,{14-i*2} 1020,0" fill="none" stroke="#4a5a42"'
              f' stroke-width="{14+i*3}" opacity=".7"/>')
    s += f'<g opacity=".85">{tuman(t, 760, .5, "#dfe8f0")}</g>'
    s += f'<g opacity=".6">{tuman(t, 880, .4, "#e8eef4")}</g>'
    for i, x in enumerate((1300, 1480)):
        s += ptica(x, 560 - 10 * abs(A.w(t, 1.8, i * .3)), t, .7, "#7a6f60", i * .4, "#5f574c")
    s += ulica_dal(820, 720, 300, t, False, 45)
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
    """Широкое поле с берёзой, большое небо; в углу косяк с зарубками."""
    s = nebo("den", t, False)
    s += oblaka(t, 200, 7, 127, .6, "#eef3f8", 11)
    s += f'<path d="M0,760 Q480,736 960,758 Q1440,780 1920,750 L1920,1080 L0,1080 Z" fill="#8a8a5e" {o(5)}/>'
    for i in range(9):
        y = 800 + i * 34
        s += (f'<path d="M-40,{y} q480,{10-i*2} 980,0 q500,{-8+i} 1000,0" fill="none"'
              f' stroke="#76764e" stroke-width="{8+i*2}" opacity=".6"/>')
    # берёза
    s += ten(560, 790, 90, 16, .4)
    s += f'<path d="M540,790 q-16,-320 30,-470 q46,150 30,470 Z" fill="#f0ece2" {o(7)}/>'
    for i in range(9):
        s += (f'<path d="M{536+ (i%3)*14},{380+i*44} h{26-(i%3)*8}" stroke="{K}" stroke-width="7"/>')
    for i in range(7):
        a = -2.4 + i * .42
        dx = 10 * A.w(t, 4.0, i * .2)
        s += (f'<path d="M566,330 q{math.cos(a)*140+dx:.0f},{math.sin(a)*90-40:.0f}'
              f' {math.cos(a)*230+dx*2:.0f},{math.sin(a)*120-60:.0f}" fill="none"'
              f' stroke="#cfc8ba" stroke-width="8"/>')
    r = random.Random(131)
    for i in range(26):
        a = r.uniform(-2.6, .4); d = r.uniform(80, 250)
        s += (f'<ellipse cx="{566+math.cos(a)*d+12*A.w(t,3.4,i*.1):.0f}"'
              f' cy="{320+math.sin(a)*d*.6:.0f}" rx="13" ry="9" fill="{ZOL}" opacity=".85"'
              f' transform="rotate({r.uniform(0,180):.0f} 566 320)"/>')
    # первый снег на зелёной траве
    s += sneg_letit(t, 30, 137, .75, .55)
    # косяк с зарубками в углу
    s += f'<rect x="1700" y="0" width="220" height="{H}" fill="url(#derev)" {o(8)}/>'
    for i in range(7):
        y = 240 + i * 94
        s += (f'<path d="M1736,{y} h150" stroke="{K}" stroke-width="7" opacity=".75"/>'
              f'<text x="1750" y="{y-14}" font-family="DejaVu Sans" font-size="30"'
              f' fill="{K}" opacity=".6">{1998+i*4}</text>')
    s += vinetka(.36)
    return s


def okno_kormushka(t):
    """Городское окно изнутри и снаружи: кормушка из молочного пакета."""
    s = f'<rect width="{W}" height="{H}" fill="#b9ad9a"/>'
    for c in range(12):
        s += f'<rect x="{c*160}" width="150" height="{H}" fill="#c6baa6" opacity="{.35 if c%2 else .12}"/>'
    s += f'<rect y="900" width="{W}" height="180" fill="url(#pol)" {o(5)}/>'
    vid = (f'<rect x="120" y="140" width="700" height="640" fill="#8fa8bf"/>'
           + _oblaka(t, 260, 3, 139, .5, "#e8eef6", 7)
           + _panelka(560, 780, 420, t, 4, True, 29)
           + _sneg_letit(t, 16, 141, .6, .5))
    s += okno_izby(120, 140, 700, 640, t, vid=vid, moroz=.3)
    s += f'<rect x="70" y="780" width="800" height="52" rx="10" fill="url(#krem)" {o(8)}/>'
    # кормушка из пакета висит снаружи
    kach = 3.0 * A.w(t, 3.6)
    s += (f'<g transform="rotate({kach:.2f} 470 180)">'
          f'<path d="M470,180 v120" stroke="{K}" stroke-width="5"/>'
          f'<path d="M350,300 h240 v190 h-240 Z" fill="url(#list)" {o(7)}/>'
          f'<path d="M376,300 h188 v-54 h-188 Z" fill="#dcd2b8" {o(5)}/>'
          f'<path d="M350,370 q120,-36 240,0 l0,60 q-120,-30 -240,0 Z" fill="#cfc4a8" opacity=".8"/>')
    for i in range(7):
        s += f'<circle cx="{372+i*32}" cy="448" r="7" fill="{ZOL}" {o(2)}/>'
    s += "</g>"
    for i, (x, y) in enumerate(((330, 380), (620, 410))):
        s += ptica(x + 8 * A.w(t, 1.4, i * .3), y, t, .8, "#8a7f6e", i * .4, "#6b6356")
    s += zanaveska(1180, 120, 760, 200, TKAN, t, -1)
    s += kvartira_veschi(900, 900, 640, t, 64)
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
    """Стена гостиной: три пустые резные рамки и настенные часы."""
    s = f'<rect width="{W}" height="{H}" fill="#7a5f52"/>'
    for c in range(14):
        s += f'<rect x="{c*138}" width="128" height="{H}" fill="#866a5c" opacity="{.45 if c%2 else .18}"/>'
    s += f'<rect y="900" width="{W}" height="180" fill="url(#pol)" {o(5)}/>'
    s += f'<rect y="866" width="{W}" height="40" fill="{POL2}" {o(4)}/>'
    s += teplo(700, 420, 900, 560, .55)
    for i, (x, y, w_, h_) in enumerate(((120, 260, 380, 460), (580, 210, 420, 500),
                                        (1090, 280, 360, 440))):
        kach = 1.1 * A.w(t, 5.0 + i * .5, i * .2)
        s += (f'<g transform="rotate({kach:.2f} {x+w_/2:.0f} {y})">'
              f'{ten(x+w_/2, y+h_+20, w_*.4, 12, .35)}'
              f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="12" fill="url(#zol)" {o(8)}/>'
              f'<rect x="{x+26}" y="{y+26}" width="{w_-52}" height="{h_-52}" rx="6"'
              f' fill="#2b2620" {o(6)}/>')
        for j in range(6):
            a = j * math.pi / 3
            s += (f'<circle cx="{x+w_/2+math.cos(a)*(w_/2-14):.0f}"'
                  f' cy="{y+h_/2+math.sin(a)*(h_/2-14):.0f}" r="13" fill="{ZOL}" {o(3)}/>')
        s += "</g>"
    s += hodiki(1640, 380, t, 1.6)
    s += ramka_pp("levo", "#2a211c", .4)
    s += kvartira_veschi(60, 900, 320, t, 68)
    s += vinetka(.42)
    return s


def tkackij_stanok(t):
    """Мастерская ткача: станок, колыбель, окно на черепичные крыши."""
    s = kladka(-20, -20, W + 40, H + 40, 96, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#e8dcc4" opacity=".2"/>'
    s += f'<rect y="900" width="{W}" height="180" fill="url(#pol)" {o(5)}/>'
    vid = (f'<rect x="1180" y="180" width="620" height="520" fill="#9fb8cc"/>'
           + _oblaka(t, 260, 3, 157, .5, "#eef3f8", 6))
    for i in range(5):
        vid += (f'<path d="M{1200+i*130},700 l80,-150 l80,150 Z" fill="#9c4a3a" {o(5)}/>')
    s += okno_izby(1180, 180, 620, 520, t, vid=vid)
    s += luch(1150, 700, 200, 380, t, .2)
    # станок
    s += ten(480, 980, 330, 24, .45)
    s += f'<rect x="150" y="300" width="46" height="660" fill="url(#derev)" {o(8)}/>'
    s += f'<rect x="760" y="300" width="46" height="660" fill="url(#derev)" {o(8)}/>'
    s += f'<rect x="130" y="280" width="700" height="42" rx="10" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="130" y="660" width="700" height="34" rx="10" fill="url(#derev)" {o(6)}/>'
    for i in range(18):
        x = 200 + i * 34
        dy = 10 * A.w(t, 2.2, i * .12)
        s += (f'<line x1="{x}" y1="330" x2="{x}" y2="{650+dy:.0f}" stroke="{KREM}" stroke-width="5" opacity=".85"/>')
    chel = 300 + 420 * ((t * .35) % 1.0)
    s += f'<rect x="{chel:.0f}" y="470" width="120" height="30" rx="14" fill="url(#derev)" {o(5)}/>'
    s += f'<path d="M200,500 h560" stroke="{TKAN}" stroke-width="14" opacity=".85"/>'
    # колыбель качается
    ang = 4.5 * A.w(t, 3.0)
    s += (f'<g transform="rotate({ang:.1f} 1000 480)">'
          f'<path d="M900,620 q100,80 200,0 l-20,-140 q-80,-26 -160,0 Z" fill="url(#derev)" {o(7)}/>'
          f'<path d="M912,500 q88,-30 176,0" fill="url(#rush)" {o(5)}/>'
          f'<path d="M900,480 h200" stroke="{K}" stroke-width="6"/></g>')
    s += vinetka(.4)
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
    """Крупно: стол, лист с выпуклыми буквами, свеча."""
    s = f'<rect width="{W}" height="{H}" fill="#2a2018"/>'
    s += kladka(-20, -20, W + 40, H + 40, 96, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#1d1510" opacity=".6"/>'
    s += f'<rect y="620" width="{W}" height="460" fill="url(#derev)" {o(7)}/>'
    s += teplo(520, 640, 760, 620, .95)
    s += svecha(1380, 480, t, .1, 2.2)
    # лист с рельефом
    s += ten(560, 980, 380, 26, .5)
    ug = .8 * A.w(t, 7.0)
    s += (f'<g transform="rotate({ug:.2f} 560 800)">'
          f'<rect x="180" y="560" width="780" height="460" rx="10" fill="url(#list)" {o(8)}/>')
    r = random.Random(167)
    for row in range(4):
        for c in range(9):
            x = 230 + c * 82; y = 640 + row * 96
            on = A.seg(t, .3 + (row * 9 + c) * .07, .4)
            for j in range(6):
                dx = (j % 3) * 20; dy = (j // 3) * 24
                s += (f'<circle cx="{x+dx}" cy="{y+dy}" r="8" fill="#cbbf9e" {o(2)}/>'
                      f'<circle cx="{x+dx-2}" cy="{y+dy-3}" r="4" fill="#fdf8e8"'
                      f' opacity="{.4+.6*on:.2f}"/>')
    s += "</g>"
    s += ramka_pp("levo", "#140e0a", .55)
    s += utvar_pekarni(1500, 1010, 400, t, 29)
    s += vinetka(.5)
    return s


def shkolnyj_klass(t):
    """Светлый класс со сводами, ряды парт с большими книгами."""
    s = kladka(-20, -20, W + 40, H + 40, 100, "url(#kamen)")
    s += f'<rect width="{W}" height="{H}" fill="#f0ead8" opacity=".32"/>'
    for i in range(4):
        s += (f'<path d="M{-100+i*560},0 q280,220 560,0" fill="none" stroke="#b9ae96"'
              f' stroke-width="26" opacity=".7"/>')
    s += f'<rect y="900" width="{W}" height="180" fill="url(#pol)" {o(5)}/>'
    vid = f'<rect x="1400" y="160" width="420" height="440" fill="#bcd4e6"/>' + _oblaka(t, 300, 2, 173, .6, "#ffffff", 5)
    s += okno_izby(1400, 160, 420, 440, t, vid=vid)
    s += luch(1360, 600, 220, 420, t, .22)
    # парты рядами
    for row in range(3):
        sc = 1.0 - row * .18
        y = 980 - row * 210
        for c in range(3):
            x = 80 + c * 400 + row * 90
            s += (f'<g transform="translate({x},{y}) scale({sc:.2f})">'
                  f'{ten(150, 20, 130, 16, .4)}'
                  f'<rect x="0" y="-130" width="320" height="34" rx="8" fill="url(#derev)" {o(6)}/>'
                  f'<rect x="20" y="-96" width="26" height="96" fill="url(#derev)" {o(5)}/>'
                  f'<rect x="274" y="-96" width="26" height="96" fill="url(#derev)" {o(5)}/>'
                  # большая книга, страница переворачивается
                  f'<path d="M70,-134 q90,-30 180,0 l0,-60 q-90,-26 -180,0 Z" fill="url(#list)" {o(6)}/>'
                  f'<path d="M160,-194 v60" stroke="{K}" stroke-width="5"/>')
            per = ((t * .3) + row * .3 + c * .2) % 1.0
            s += (f'<path d="M160,-194 q{90*(1-per*2):.0f},-26 {180*(1-per*2):.0f},0 l0,60'
                  f' q{-90*(1-per*2):.0f},26 {-180*(1-per*2):.0f},0 Z" fill="#f6f0dc" opacity=".9" {o(4)}/>')
            s += "</g>"
    s += vinetka(.38)
    return s


def dve_gramoty(t):
    """Полиэкран: слева келья с доской букв, справа лист с выпуклыми буквами."""
    hw = W / 2
    s = f'<rect width="{W}" height="{H}" fill="#16110d"/>'
    s += f'<clipPath id="dgL"><rect width="{hw:.0f}" height="{H}"/></clipPath><g clip-path="url(#dgL)">'
    s += kladka(-20, -20, hw + 40, H + 40, 92, "url(#kamen)")
    s += f'<rect width="{hw:.0f}" height="{H}" fill="#120f14" opacity=".55"/>'
    s += teplo(hw * .5, 560, 420, 420, .9)
    s += svecha(200, 540, t, .1, 1.3)
    s += f'<rect x="300" y="460" width="420" height="300" rx="12" fill="url(#dosk)" {o(8)}/>'
    for i, b in enumerate("АБВГ"):
        on = A.seg(t, .5 + i * .6, .5)
        s += (f'<text x="{340+i*96}" y="620" font-family="DejaVu Serif, Georgia, serif"'
              f' font-size="92" fill="{SVET if on>.5 else "#6b4428"}" opacity="{.5+.5*on:.2f}">{b}</text>')
    s += f'<rect y="900" width="{hw:.0f}" height="180" fill="#3b332a"/>'
    s += "</g>"
    s += f'<clipPath id="dgR"><rect x="{hw:.0f}" width="{hw:.0f}" height="{H}"/></clipPath><g clip-path="url(#dgR)">'
    s += f'<rect x="{hw:.0f}" width="{hw:.0f}" height="{H}" fill="#2a2018"/>'
    s += kladka(hw - 20, -20, hw + 40, H + 40, 96, "url(#kamen)")
    s += f'<rect x="{hw:.0f}" width="{hw:.0f}" height="{H}" fill="#1d1510" opacity=".6"/>'
    s += teplo(hw + 460, 600, 460, 460, .9)
    s += f'<rect x="{hw:.0f}" y="760" width="{hw:.0f}" height="320" fill="url(#derev)" {o(6)}/>'
    s += f'<rect x="{hw+140:.0f}" y="420" width="640" height="400" rx="10" fill="url(#list)" {o(8)}/>'
    r = random.Random(179)
    for row in range(3):
        for c in range(7):
            x = hw + 190 + c * 86; y = 500 + row * 104
            on = A.seg(t, .4 + (row * 7 + c) * .08, .4)
            for j in range(6):
                s += (f'<circle cx="{x+(j%3)*20}" cy="{y+(j//3)*24}" r="8" fill="#cbbf9e" {o(2)}/>'
                      f'<circle cx="{x+(j%3)*20-2}" cy="{y+(j//3)*24-3}" r="4" fill="#fdf8e8"'
                      f' opacity="{.4+.6*on:.2f}"/>')
    s += "</g>"
    s += f'<rect x="{hw-4:.0f}" width="8" height="{H}" fill="{K}" opacity=".85"/>'
    return s


def dom_dozhd(t):
    """Вересковые холмы, каменный дом под ливнем."""
    s = f'<rect width="{W}" height="{H}" fill="#4a5260"/>'
    s += oblaka(t, 150, 6, 181, .6, "#5c6472", 12)
    s += f'<path d="M0,620 Q400,560 820,620 Q1300,684 1920,600 L1920,1080 L0,1080 Z" fill="#5c5a4e" {o(5)}/>'
    s += f'<path d="M0,760 Q480,720 980,764 Q1460,804 1920,752 L1920,1080 L0,1080 Z" fill="#6b5a5e" {o(5)}/>'
    r = random.Random(191)
    for i in range(60):
        x, y = r.uniform(0, W), r.uniform(770, 1070)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(5,11):.0f}" fill="#8a5f76" opacity=".5"/>'
    # дом
    s += ten(400, 1000, 300, 24, .45)
    s += kladka(120, 460, 580, 540, 76, "url(#kamen)")
    s += f'<path d="M80,460 L410,300 L740,460 Z" fill="#3b3a36" {o(8)}/>'
    s += okno_izby(240, 560, 160, 150, t, svet=True, moroz=0)
    s += okno_izby(480, 560, 160, 150, t, svet=True, moroz=0)
    s += f'<rect x="380" y="800" width="130" height="200" rx="6" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="620" y="250" width="56" height="130" fill="url(#kamen)" {o(5)}/>'
    s += f'<g opacity=".5">{dym(648, 250, t, 4, .3, 240, .4, "#8a8f96", 1.1)}</g>'
    # ливень
    for i in range(90):
        x = r.uniform(-200, W); y0 = r.uniform(0, H)
        y = (y0 + t * 900) % (H + 200) - 100
        s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x-26:.0f}" y2="{y+70:.0f}"'
              f' stroke="#cfe0ea" stroke-width="3" opacity=".45"/>')
    s += f'<g opacity=".6">{tuman(t, 700, .4, "#8a95a4")}</g>'
    s += ulica_dal(860, 760, 1060, t, False, 55)
    s += vinetka(.46)
    return s


def stol_karta(t):
    """Стол у дождливого окна: акварель, лист с картой острова."""
    s = f'<rect width="{W}" height="{H}" fill="#4a4038"/>'
    s += doski(0, 0, W, H, 170, True, "dosk")
    s += f'<rect width="{W}" height="{H}" fill="#2a2018" opacity=".4"/>'
    vid = f'<rect x="1180" y="120" width="660" height="560" fill="#5c6472"/>'
    r = random.Random(193)
    for i in range(40):
        x = r.uniform(1180, 1840); y0 = r.uniform(120, 680)
        y = 120 + ((y0 - 120) + t * 700) % 560
        vid += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x-20:.0f}" y2="{y+50:.0f}" stroke="#cfe0ea" stroke-width="3" opacity=".5"/>'
    s += okno_izby(1180, 120, 660, 560, t, vid=vid, moroz=0)
    s += f'<rect y="700" width="{W}" height="380" fill="url(#derev)" {o(7)}/>'
    s += svecha(1020, 560, t, .2, 1.4)
    s += teplo(520, 700, 700, 600, .85)
    # карта острова
    s += ten(480, 1030, 420, 24, .45)
    ug = .7 * A.w(t, 8.0)
    s += (f'<g transform="rotate({ug:.2f} 480 820)">'
          f'<rect x="120" y="560" width="760" height="500" rx="8" fill="url(#list)" {o(8)}/>'
          f'<path d="M260,760 q60,-140 220,-110 q180,34 200,150 q20,120 -140,160'
          f' q-200,48 -280,-60 q-50,-70 0,-140 Z" fill="#c9b98e" {o(6)}/>')
    for i in range(5):
        s += (f'<path d="M{300+i*90},{700+((i*37)%120)} q30,26 60,0" fill="none"'
              f' stroke="#8a7a52" stroke-width="5"/>')
    kr = .5 + .5 * abs(A.w(t, 1.8))
    s += (f'<path d="M560,860 l-34,-34 m34,34 l34,-34 m-34,34 l-34,34 m34,-34 l34,34"'
          f' stroke="{KRAS}" stroke-width="11" opacity="{kr:.2f}"/>')
    s += (f'<path d="M700,640 q40,-40 80,0 q-40,-10 -80,0 Z" fill="#8a7a52" {o(4)}/>'
          f'<text x="300" y="1020" font-family="DejaVu Serif, Georgia, serif" font-size="44"'
          f' fill="#6b5a32" opacity=".8">— — — — —</text></g>')
    # акварель
    for i, (x, col) in enumerate(((980, TKAN), (1040, ZEL2), (1100, TKAN2))):
        s += f'<circle cx="{x}" cy="860" r="34" fill="{col}" opacity=".9" {o(5)}/>'
    s += f'<rect x="950" y="900" width="220" height="30" rx="12" fill="url(#krem)" {o(5)}/>'
    s += kvartira_veschi(60, 700, 360, t, 70)
    s += vinetka(.46)
    return s


def hutor(t):
    """Осенний хутор: белёная хата под соломой, плетень, колодец-журавель."""
    s = nebo("den", t, False)
    s += oblaka(t, 190, 5, 197, .5, "#e2e8ee", 8)
    s += f'<path d="M0,760 Q480,732 960,756 Q1440,780 1920,748 L1920,1080 L0,1080 Z" fill="#8a8458" {o(5)}/>'
    # хата
    s += ten(420, 1000, 330, 24, .45)
    s += f'<rect x="120" y="440" width="640" height="560" rx="8" fill="{POBEL}" {o(9)}/>'
    s += f'<path d="M70,440 L440,270 L810,440 Z" fill="url(#solom)" {o(8)}/>'
    for i in range(14):
        s += f'<path d="M{90+i*52},438 l{(440-(90+i*52))*.24:.0f},-62" stroke="#a07c2e" stroke-width="6" opacity=".6"/>'
    s += okno_izby(200, 560, 170, 150, t, svet=True, moroz=0)
    s += okno_izby(480, 560, 170, 150, t, svet=True, moroz=0)
    s += f'<rect x="340" y="800" width="150" height="200" rx="6" fill="url(#derev)" {o(7)}/>'
    for i, x in enumerate((210, 490)):
        s += (f'<path d="M{x-50},714 q50,-18 100,0 l0,34 q-50,-16 -100,0 Z" fill="{TKAN}" opacity=".9" {o(4)}/>')
    s += pleten(820, 920, 420, 180, 7)
    # колодец-журавель
    s += f'<rect x="1340" y="400" width="44" height="560" fill="url(#derev)" {o(7)}/>'
    ang = 11 * A.w(t, 6.0)
    s += (f'<g transform="rotate({ang:.1f} 1362 400)">'
          f'<rect x="1100" y="380" width="620" height="30" rx="14" fill="url(#derev)" {o(6)}/>'
          f'<line x1="1690" y1="410" x2="1690" y2="620" stroke="{K}" stroke-width="6"/>'
          f'<path d="M1650,620 l16,100 q24,10 48,0 l16,-100 Z" fill="url(#zhel)" {o(6)}/></g>')
    s += f'<ellipse cx="1420" cy="980" rx="150" ry="40" fill="#5c4634" {o(6)}/>'
    s += f'<g opacity=".6">{sneg_letit(t, 10, 199, .4, .35)}</g>'
    s += ulica_dal(1560, 760, 360, t, False, 47)
    s += vinetka(.38)
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
    """Двор, две калитки рядом — о доброте по-соседски."""
    s = nebo("den", t, False)
    s += oblaka(t, 180, 5, 229, .5, "#dfe8f0", 8)
    s += f'<path d="M0,740 Q480,716 960,740 Q1440,764 1920,732 L1920,1080 L0,1080 Z" fill="#76805c" {o(5)}/>'
    s += sneg_lezhit(810, 14, "#e6eef6")
    s += pleten(-40, 880, 420, 210, 6)
    s += pleten(1540, 880, 420, 210, 6)
    for i, x in enumerate((380, 1000)):
        ang = (2.0 if i == 0 else -2.0) * A.w(t, 5.0, i * .3)
        s += f'<rect x="{x-20}" y="500" width="40" height="400" fill="url(#derev)" {o(6)}/>'
        s += f'<rect x="{x+520}" y="500" width="40" height="400" fill="url(#derev)" {o(6)}/>'
        s += (f'<g transform="rotate({ang:.2f} {x+20} 520)">'
              f'{doski(x+20, 520, 500, 380, 82, True, "derev")}'
              f'<rect x="{x+20}" y="520" width="500" height="380" fill="none" {o(7)}/>'
              f'<path d="M{x+20},620 L{x+520},560" stroke="#6b4428" stroke-width="20" opacity=".8"/></g>')
    # между калитками — узелок с пирогом переходит сам
    p = (t * .3) % 1.0
    xx = 860 + 200 * A.ease(p)
    s += (f'<g transform="translate({xx-960:.0f},{-60*math.sin(p*math.pi):.0f})">'
          f'{ten(960, 880, 70, 12, .4)}'
          f'<path d="M890,870 q70,-120 140,0 Z" fill="url(#rush)" {o(6)}/>'
          f'<path d="M928,792 q32,-40 64,0" fill="none" stroke="{TKAN}" stroke-width="11"/></g>')
    s += f'<g opacity=".6">{sneg_letit(t, 14, 233, .5, .4)}</g>'
    s += ulica_dal(620, 740, 680, t, True, 48)
    s += vinetka(.38)
    return s


# ─────────────────────── 8. ФИНАЛ ───────────────────────
def dom_vecherom(t):
    """Дом в разрезе: слева изба, справа квартира, подпол, порог."""
    s = nebo("noch", t, True, 239)
    s += f'<rect y="960" width="{W}" height="120" fill="#2b3550"/>'
    s += f'<rect x="60" y="180" width="1800" height="780" rx="14" fill="#3b332a" {o(9)}/>'
    s += f'<path d="M20,180 L960,40 L1900,180 Z" fill="{DOSKA2}" {o(8)}/>'
    s += f'<rect x="80" y="760" width="1760" height="26" fill="url(#derev)" {o(5)}/>'
    # левая половина — изба
    s += f'<rect x="80" y="200" width="860" height="560" fill="url(#brev)" opacity=".9"/>'
    s += f'<rect x="80" y="200" width="860" height="560" fill="#1f2534" opacity=".3"/>'
    s += pech(140, 330, 280, 430, t, True, True)
    s += teplo(300, 600, 440, 380, .8)
    s += stol(520, 600, 320)
    s += lampa(680, 440, t, .7, abazhur=True)
    s += kot(560, 750, t, .55, "#3b3430", spit=True)
    # правая половина — квартира
    s += f'<rect x="960" y="200" width="880" height="560" fill="url(#beton)" opacity=".85"/>'
    s += f'<rect x="960" y="200" width="880" height="560" fill="#2a2f3c" opacity=".3"/>'
    s += f'<rect x="1020" y="520" width="340" height="190" rx="16" fill="{TKAN2}" {o(7)}/>'
    s += f'<rect x="1420" y="420" width="300" height="290" rx="10" fill="url(#derev)" {o(7)}/>'
    s += f'<circle cx="1570" cy="340" r="54" fill="{SVET}" opacity="{.7+.3*abs(A.w(t,3.4)):.2f}" {o(5)}/>'
    s += teplo(1570, 480, 460, 400, .7)
    s += f'<rect x="1180" y="320" width="150" height="110" rx="8" fill="#2b2b33" {o(5)}/>'
    s += f'<rect x="1196" y="336" width="118" height="78" rx="5" fill="#9fd0e8" opacity="{.3+.4*abs(A.w(t,.5)):.2f}"/>'
    # подпол
    s += f'<rect x="80" y="786" width="1760" height="174" fill="#241c14" {o(5)}/>'
    s += kartoshka(420, 880, t, 12, 6, 1.0)
    for i, x in enumerate((900, 1040, 1180)):
        s += krynka(x, 920, .7)
    s += f'<rect x="1400" y="840" width="260" height="110" rx="10" fill="url(#derev)" {o(5)}/>'
    s += sneg_letit(t, 22, 241, .6, .5)
    s += vinetka(.48)
    return s


def pamyatka(t):
    """Тёплая дощатая стена под памятку. Карточки и шапку кладут НАЛОЖЕНИЯ —
    иначе под текстом стоят вторые, пустые карточки (поймано на сведении)."""
    s = f'<rect width="{W}" height="{H}" fill="#6b4c32"/>'
    s += doski(0, 0, W, H, 134, False, "dosk")
    s += f'<rect width="{W}" height="{H}" fill="#3a2a1c" opacity=".34"/>'
    s += teplo(960, 480, 1200, 760, .6)
    for i, x in enumerate((120, 1700)):
        s += f'<rect x="{x}" y="0" width="100" height="{H}" fill="#4a3324" opacity=".5"/>'
    for i in range(4):
        kach = 1.6 * A.w(t, 4.6 + i * .4, i * .2)
        px = 220 + i * 500
        s += f'<g transform="rotate({kach:.2f} {px} 40)" opacity=".85">'
        for j in range(5):
            s += (f'<path d="M{px},40 q{-18+j*9},70 {-12+j*6},130" fill="none"'
                  f' stroke="{["#6f8c4a","#8a9a58","#5c7a40"][j%3]}" stroke-width="7"/>')
        s += f'<path d="M{px-20},44 q20,-16 40,0" fill="none" stroke="{TKAN}" stroke-width="9"/></g>'
    s += vinetka(.42)
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
    """Стол, раскрытый альбом с нарисованными снимками без лиц, тетрадный лист."""
    s = f'<rect width="{W}" height="{H}" fill="#4a4038"/>'
    s += doski(0, 0, W, H, 180, True, "dosk")
    s += f'<rect width="{W}" height="{H}" fill="#2a2018" opacity=".35"/>'
    s += f'<rect y="260" width="{W}" height="820" fill="url(#derev)" {o(7)}/>'
    s += lampa(1500, 300, t, 1.0, abazhur=True)
    s += teplo(760, 640, 900, 640, .75)
    # альбом
    s += ten(760, 1030, 500, 24, .45)
    s += f'<rect x="200" y="420" width="1120" height="600" rx="14" fill="#5c3b2a" {o(9)}/>'
    s += f'<rect x="230" y="450" width="520" height="540" rx="8" fill="#2b2620" {o(6)}/>'
    s += f'<rect x="770" y="450" width="520" height="540" rx="8" fill="#2b2620" {o(6)}/>'
    s += f'<rect x="752" y="420" width="16" height="600" fill="#3b2a1e"/>'
    r = random.Random(257)
    for i, (x, y, w_, h_) in enumerate(((270, 490, 220, 170), (520, 490, 200, 170),
                                        (270, 700, 200, 170), (510, 700, 210, 170),
                                        (810, 490, 220, 170), (1060, 490, 200, 170),
                                        (810, 700, 440, 170))):
        ug = .8 * A.w(t, 6.0 + i * .4, i * .2)
        s += (f'<g transform="rotate({ug:.2f} {x+w_/2:.0f} {y+h_/2:.0f})">'
              f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="4" fill="url(#list)" {o(5)}/>'
              f'<rect x="{x+10}" y="{y+10}" width="{w_-20}" height="{h_-34}" fill="#b9ae96"/>')
        for j in range(2 + i % 3):
            s += siluet(x + 36 + j * 54, y + h_ - 30, h_ * .62, "#6b6356", .9)
        s += "</g>"
    # тетрадный лист и перо
    s += ten(1620, 1000, 160, 16, .4)
    ug = 1.4 * A.w(t, 5.0)
    s += (f'<g transform="rotate({ug:.2f} 1620 800)">'
          f'<rect x="1420" y="600" width="400" height="400" rx="6" fill="url(#list)" {o(6)}/>')
    for j in range(9):
        s += f'<line x1="1450" y1="{650+j*40}" x2="1790" y2="{650+j*40}" stroke="#9fb8cc" stroke-width="3" opacity=".8"/>'
    s += "</g>"
    s += f'<g transform="rotate(-30 1760 700)"><path d="M1700,700 q90,-180 140,-220 q-20,120 -100,250 Z" fill="url(#krem)" {o(5)}/></g>'
    s += kvartira_veschi(60, 260, 360, t, 69)
    s += vinetka(.46)
    return s


def okno_snaruzhi(t):
    """Стол с пирогом изнутри и тёплое окно снаружи, снежный вечер."""
    s = nebo("noch", t, True, 263)
    s += f'<path d="M0,840 Q480,806 960,838 Q1440,870 1920,828 L1920,1080 L0,1080 Z" fill="#2b3550" {o(5)}/>'
    s += sneg_lezhit(860, 24, "#cfd8e6")
    s += brevna(-20, 160, 1200, 700, 96)
    s += f'<path d="M-60,160 L560,20 L1240,160 Z" fill="{DOSKA2}" {o(8)}/>'
    s += f'<path d="M-60,160 L560,20 L1240,160 l-50,-34 L560,56 L-10,136 Z" fill="url(#sneg)" {o(5)}/>'
    # большое тёплое окно, внутри стол с пирогом и силуэты
    vid = (f'<rect x="200" y="320" width="760" height="520" fill="#3a2a1e"/>'
           + teplo(580, 640, 520, 440, 1.0)
           + stol(300, 700, 560, 36)
           + f'<ellipse cx="580" cy="686" rx="150" ry="52" fill="url(#med)" {o(6)}/>'
           + par(580, 620, t, 4, .5, 200, .7, .9))
    for i, (x, h_) in enumerate(((340, 300), (470, 330), (700, 290), (820, 260))):
        vid += siluet(x + 4 * A.w(t, 4.0, i * .3), 700, h_, "#1a1410", .9, platok=(i == 0), kant=SVET)
    s += okno_izby(200, 320, 760, 520, t, vid=vid, moroz=.25)
    s += teplo(580, 580, 760, 620, .65)
    s += f'<rect x="1060" y="280" width="70" height="140" fill="url(#kamen)" {o(5)}/>'
    s += dym(1095, 280, t, 5, .2, 300, .35, "#cfd6de", .8)
    s += sneg_letit(t, 44, 269, .9, .8)
    s += ramka_pp("pravo", "#16203a", .4)
    s += ulica_dal(1240, 860, 680, t, True, 50)
    s += vinetka(.46)
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
