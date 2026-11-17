# -*- coding: utf-8 -*-
"""Декорации ролика «В чём встречать Новый год 2027», часть 1 (планы 1-34)."""
import math, random
from baza import *
from lok_obshchee import *
import anim as A

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
