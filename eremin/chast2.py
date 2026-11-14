# -*- coding: utf-8 -*-
"""Декорации 35-68 ролика «17 ноября — Ерёмин день»."""
import math, random
from baza import *
import anim as A
from lok_obshchee import *


# ── мелкие предметы этой порции ────────────────────────────────────────────
# Здесь живут только те вещи, которых нет в baza.py и в lok_obshchee.py:
# ведро, корзина, газета, банка, глаза утвари, ножки припасов, листок
# численника. Каждая опознаётся силуэтом — его правило 14.11.

def _vedro(x, y, s_=1.0, t=0.0, polnoe=True, col="url(#zhel)"):
    """Ведро: конус кверху шире, обруч, дуга ручки, блик по боку."""
    w1, w2, hh = 62 * s_, 46 * s_, 84 * s_
    kach = 2.6 * A.w(t, 1.9, x * .001)
    s = ten(x, y + 8 * s_, w1 * .9, 10 * s_, .4)
    s += f'<g transform="rotate({kach:.2f} {x:.0f} {y-hh*1.9:.0f})">'
    s += (f'<path d="M{x-w1:.0f},{y-hh:.0f} L{x+w1:.0f},{y-hh:.0f}'
          f' L{x+w2:.0f},{y:.0f} L{x-w2:.0f},{y:.0f} Z" fill="{col}" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w1:.0f}" ry="{10*s_:.0f}"'
          f' fill="{ZHELEZ}" {o(4)}/>')
    if polnoe:
        s += (f'<ellipse cx="{x:.0f}" cy="{y-hh+2*s_:.0f}" rx="{w1*.86:.0f}"'
              f' ry="{8*s_:.0f}" fill="url(#voda)" opacity=".9"/>')
        s += (f'<ellipse cx="{x-w1*.3:.0f}" cy="{y-hh:.0f}" rx="{w1*.3:.0f}"'
              f' ry="{4*s_:.0f}" fill="#bfe6f2"'
              f' opacity="{.4+.4*abs(A.w(t,1.4,x*.002)):.2f}"/>')
    s += (f'<path d="M{x-w1:.0f},{y-hh*.96:.0f} q{w1:.0f},{-hh*.8:.0f} {w1*2:.0f},0"'
          f' fill="none" stroke="{ZHELEZ}" stroke-width="{7*s_:.0f}"/>')
    s += (f'<path d="M{x-w1*.72:.0f},{y-hh*.74:.0f} L{x-w2*.66:.0f},{y-hh*.12:.0f}"'
          f' stroke="#e6f1f8" stroke-width="{8*s_:.0f}"'
          f' opacity="{.3+.35*abs(A.w(t,2.2,x*.003)):.2f}"/>')
    s += (f'<path d="M{x-w1*.9:.0f},{y-hh*.5:.0f} q{w1*.9:.0f},{10*s_:.0f} {w1*1.76:.0f},0"'
          f' fill="none" stroke="{ZHELEZ}" stroke-width="{5*s_:.0f}" opacity=".8"/>')
    return s + '</g>'


def _korzina(x, y, w_, h_, t, seed=7, pustaya=True):
    """Плетёная корзина: лоза в два хода, дужка, тёмное дно."""
    rnd = random.Random(seed)
    s = ten(x, y + 10, w_ * .52, 16, .45)
    s += (f'<path d="M{x-w_/2:.0f},{y-h_:.0f} L{x+w_/2:.0f},{y-h_:.0f}'
          f' L{x+w_*.36:.0f},{y:.0f} L{x-w_*.36:.0f},{y:.0f} Z"'
          f' fill="url(#solom)" {o(6)}/>')
    for i in range(6):
        yy = y - h_ + 14 + i * (h_ - 20) / 5
        kk = (w_ / 2) * (1 - .28 * (i / 5))
        d = f'M{x-kk:.0f},{yy:.0f}'
        for j in range(6):
            xx = x - kk + j * (kk * 2 / 6)
            d += f' Q{xx+kk/6:.0f},{yy+(11 if j % 2 == 0 else -11):.0f} {xx+kk*2/6:.0f},{yy:.0f}'
        s += f'<path d="{d}" fill="none" stroke="#b78a46" stroke-width="9"/>'
    for i in range(7):
        xx = x - w_ / 2 + 10 + i * (w_ - 20) / 6
        s += (f'<line x1="{xx:.0f}" y1="{y-h_+6:.0f}" x2="{xx*.94+x*.06:.0f}" y2="{y-4:.0f}"'
              f' stroke="#8a6534" stroke-width="6" opacity=".7"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_:.0f}" rx="{w_/2:.0f}" ry="{h_*.13:.0f}"'
          f' fill="{"#3a2c1c" if pustaya else "url(#solom)"}" {o(5)}/>')
    duga = 3.0 * A.w(t, 3.1, seed * .07)
    s += (f'<g transform="rotate({duga:.2f} {x:.0f} {y-h_:.0f})">'
          f'<path d="M{x-w_*.42:.0f},{y-h_*.98:.0f} q{w_*.42:.0f},{-h_*.78:.0f}'
          f' {w_*.84:.0f},0" fill="none" stroke="#9a7238" stroke-width="13"/></g>')
    return s


def _glaza(x, y, r_, t, ph=.0, col="#f6e39a"):
    """Пара испуганных глаз: моргают и косятся. Утварь ими и оживает."""
    kos = r_ * .3 * A.w(t, 1.7, ph)
    s = ""
    for i in (-1, 1):
        s += (f'<ellipse cx="{x+i*r_*1.25:.0f}" cy="{y:.0f}" rx="{r_:.0f}"'
              f' ry="{(r_*.34 if A.blink(t, 3.6, ph) else r_*1.02):.1f}" fill="{col}" {o(3)}/>')
        if not A.blink(t, 3.6, ph):
            s += (f'<circle cx="{x+i*r_*1.25+kos:.0f}" cy="{y+r_*.1:.0f}" r="{r_*.42:.0f}"'
                  f' fill="{K}"/>')
            s += (f'<circle cx="{x+i*r_*1.25+kos-r_*.2:.0f}" cy="{y-r_*.22:.0f}"'
                  f' r="{r_*.16:.0f}" fill="#ffffff" opacity=".85"/>')
    return s


def _nozhki(x, y, w_, t, ph=.0, col="#4a3a28", dl=40):
    """Тонкие ножки припаса: шагают, пятки отрываются от земли."""
    s = ""
    for i in (-1, 1):
        sh = 16 * A.w(t, .8, ph + (0 if i < 0 else .5))
        s += (f'<path d="M{x+i*w_*.3:.0f},{y:.0f} q{sh*.4:.0f},{dl*.6:.0f} {sh:.0f},{dl:.0f}"'
              f' fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/>')
        s += (f'<ellipse cx="{x+i*w_*.3+sh*1.2:.0f}" cy="{y+dl+6:.0f}" rx="18" ry="8"'
              f' fill="{col}" {o(3)}/>')
    return s


def _gazeta(x, y, w_, h_, ang=0.0, seed=3, col="url(#list)"):
    """Газетный лист: без букв — волнистые строки и серая полоса-фото."""
    rnd = random.Random(seed)
    s = (f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
         f'<rect x="{x-w_/2:.0f}" y="{y-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="4" fill="{col}" {o(4)}/>')
    s += (f'<rect x="{x-w_*.42:.0f}" y="{y-h_*.40:.0f}" width="{w_*.38:.0f}"'
          f' height="{h_*.26:.0f}" fill="#9aa3a8" opacity=".75" {o(2)}/>')
    for i in range(9):
        yy = y - h_ * .36 + i * h_ * .09
        if i < 3:
            s += (f'<path d="M{x+w_*.02:.0f},{yy:.0f} q{w_*.12:.0f},{-4+rnd.uniform(-2,2):.1f}'
                  f' {w_*.44:.0f},0" fill="none" stroke="#6b645c" stroke-width="4"/>')
        else:
            s += (f'<path d="M{x-w_*.42:.0f},{yy:.0f} q{w_*.22:.0f},{rnd.uniform(-3,3):.1f}'
                  f' {w_*.86:.0f},0" fill="none" stroke="#6b645c" stroke-width="4"'
                  f' opacity=".85"/>')
    s += (f'<line x1="{x:.0f}" y1="{y-h_/2:.0f}" x2="{x:.0f}" y2="{y+h_/2:.0f}"'
          f' stroke="#b8ae9a" stroke-width="3" opacity=".8"/>')
    return s + '</g>'


def _banka(x, y, s_=1.0, zerno="url(#solom)", t=0.0):
    """Банка с крупой: стекло, крышка, уровень зерна, блик."""
    w_, hh = 54 * s_, 128 * s_
    s = ten(x, y + 6 * s_, w_ * .9, 9 * s_, .35)
    s += (f'<path d="M{x-w_:.0f},{y-hh:.0f} h{w_*2:.0f} l{-6*s_:.0f},{hh:.0f}'
          f' h{-w_*2+12*s_:.0f} Z" fill="url(#stekl)" opacity=".8" {o(5)}/>')
    s += (f'<path d="M{x-w_*.9:.0f},{y-hh*.56:.0f} h{w_*1.8:.0f} l{-5*s_:.0f},{hh*.54:.0f}'
          f' h{-w_*1.8+10*s_:.0f} Z" fill="{zerno}" {o(3)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh*.56:.0f}" rx="{w_*.9:.0f}" ry="{9*s_:.0f}"'
          f' fill="#d8b96a" opacity=".9"/>')
    s += (f'<rect x="{x-w_*1.08:.0f}" y="{y-hh-16*s_:.0f}" width="{w_*2.16:.0f}"'
          f' height="{20*s_:.0f}" rx="{6*s_:.0f}" fill="url(#zhel)" {o(4)}/>')
    s += (f'<path d="M{x-w_*.6:.0f},{y-hh*.9:.0f} l0,{hh*.7:.0f}" stroke="#ffffff"'
          f' stroke-width="{9*s_:.0f}" opacity="{.25+.2*abs(A.w(t,3.0,x*.002)):.2f}"/>')
    return s


def _listok(x, y, w_, h_, t, krest=False, kolco=False, otryv=0.0):
    """Листок численника: только бумага и пометки — крест или кольцо.
    Букв и цифр на нём нет (правило ролика), строки идут волной."""
    ug = -14 * otryv
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y-h_/2:.0f}) translate(0,{otryv*60:.0f})">'
         f'<rect x="{x-w_/2:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="6" fill="url(#list)" {o(5)}/>')
    for i in range(4):
        s += (f'<path d="M{x-w_*.34:.0f},{y-h_*.62+i*h_*.14:.0f} q{w_*.17:.0f},5'
              f' {w_*.68:.0f},0" fill="none" stroke="#7d756a" stroke-width="5"'
              f' opacity=".8"/>')
    if krest:
        bl = .6 + .4 * abs(A.w(t, 1.5))
        for d in (1, -1):
            s += (f'<line x1="{x-w_*.36*d:.0f}" y1="{y-h_*.82:.0f}"'
                  f' x2="{x+w_*.36*d:.0f}" y2="{y-h_*.16:.0f}" stroke="{KRAS}"'
                  f' stroke-width="14" stroke-linecap="round" opacity="{bl:.2f}"/>')
    if kolco:
        s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.48:.0f}" rx="{w_*.38:.0f}"'
              f' ry="{h_*.33:.0f}" fill="none" stroke="{ZEL2}" stroke-width="12"'
              f' opacity="{.55+.4*abs(A.w(t,1.2,.3)):.2f}"/>')
    s += (f'<path d="M{x-w_/2:.0f},{y-h_:.0f} h{w_:.0f}" stroke="{ZHELEZ}"'
          f' stroke-width="8"/>')
    return s + '</g>'


# ── 35 ─────────────────────────────────────────────────────────────────────
def okno_so_svetom_v_nochi(t):
    """Окно деревенского дома снаружи на пол-кадра: за кружевной занавеской
    горит лампа и вяжет бабушка, а по тёмной улице к огоньку идёт путник."""
    rnd = random.Random(3511)
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 353)
    s += ulica_dal(-60, 700, 820, t, False, 359)
    s += SL(Z_DAL, gryaz_polosa(792, 150, "#2c2822"))
    st = brevna(300, 60, 1500, 900, 116)
    st += (f'<path d="M260,120 L1060,-130 L1860,120 Z" fill="#43372c" opacity=".95" {o(8)}/>')
    s += SL(Z_DAL, st)
    s += SL(Z_DAL, f'<rect x="1380" y="-60" width="104" height="210"'
                   f' fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, dym(1432, -40, t, 5, .22, 320, .32, "#c8d0da", 1.1))
    ox, oy, ow, oh = 540, 230, 880, 560
    gas = A.ease(A.seg(t, 4.0, 1.0))
    yarko = (1 - gas) * (.84 + .16 * abs(A.w(t, 1.6)))
    vn = f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#2a1d12"/>'
    vn += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="{SVET}"'
           f' opacity="{.30*yarko:.2f}"/>')
    vn += teplo(ox + ow * .30, oy + oh * .52, 420, 360, .62 * yarko)
    vn += (f'<rect x="{ox+ow*.08:.0f}" y="{oy+oh*.66:.0f}" width="{ow*.5:.0f}"'
           f' height="26" rx="8" fill="#5a4026" opacity=".9"/>')
    vn += lampa(ox + ow * .22, oy + oh * .64, t, .72)
    bx = ox + ow * .66
    vn += figura(bx, oy + oh * .98, 430, t, "#4a3140", "#ffd98a", True, .2,
                 True, 1.0 * yarko + .02, False, .8)
    sp = 26 * A.w(t, .55, .1)
    for i in range(2):
        vn += (f'<line x1="{bx-130+i*18:.0f}" y1="{oy+oh*.46+sp*.5:.0f}"'
               f' x2="{bx-30+i*22:.0f}" y2="{oy+oh*.62-sp:.0f}" stroke="{KREM}"'
               f' stroke-width="7" stroke-linecap="round"'
               f' opacity="{.9*yarko+.05:.2f}"/>')
    vn += (f'<ellipse cx="{bx-156:.0f}" cy="{oy+oh*.74:.0f}" rx="52" ry="44"'
           f' fill="{TKAN2}" opacity="{.95*yarko+.05:.2f}" {o(4)}/>')
    vn += (f'<path d="M{bx-150:.0f},{oy+oh*.70:.0f} q-40,-40 -90,-8" fill="none"'
           f' stroke="{TKAN2}" stroke-width="6" opacity="{yarko:.2f}"/>')
    kr = ""
    for i in range(11):
        kx = ox + 20 + i * (ow - 40) / 10
        kr += (f'<path d="M{kx:.0f},{oy+10} q{(ow-40)/20:.0f},86 {(ow-40)/10:.0f},0"'
               f' fill="none" stroke="#f4efe2" stroke-width="7" opacity=".72"/>')
        kr += (f'<circle cx="{kx+(ow-40)/20:.0f}" cy="{oy+54}" r="9" fill="none"'
               f' stroke="#f4efe2" stroke-width="5" opacity=".6"/>')
    kr += (f'<rect x="{ox+6}" y="{oy+6}" width="{ow-12}" height="30" fill="#f4efe2"'
           f' opacity=".5"/>')
    s += SL(Z_SRED, vn + kr)
    s += SL(Z_SRED, zanaveska(ox + 24, oy + 30, 480, 190, "#efe8d6", t, 1))
    s += SL(Z_SRED, zanaveska(ox + ow - 24, oy + 30, 480, 190, "#efe8d6", t, -1))
    ob = (f'<rect x="{ox-54}" y="{oy-54}" width="{ow+108}" height="{oh+108}" rx="10"'
          f' fill="none" stroke="url(#derev)" stroke-width="96"/>')
    ob += (f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}" y2="{oy+oh}"'
           f' stroke="url(#derev)" stroke-width="30"/>'
           f'<line x1="{ox}" y1="{oy+oh*.45:.0f}" x2="{ox+ow}" y2="{oy+oh*.45:.0f}"'
           f' stroke="url(#derev)" stroke-width="30"/>')
    ob += (f'<path d="M{ox-120},{oy-64} h{ow+240} l-72,-74 h{-ow-96} Z"'
           f' fill="{DOSKA2}" {o(8)}/>')
    for i in range(9):
        nx = ox - 90 + i * (ow + 180) / 8
        ob += (f'<path d="M{nx:.0f},{oy-70} l30,-22 l30,22 Z" fill="{MED}"'
               f' opacity=".9" {o(3)}/>')
    for sgn in (-1, 1):
        sx = ox + ow / 2 + sgn * (ow / 2 + 120)
        kach = 2.2 * sgn * A.w(t, 4.6, .2)
        ob += (f'<g transform="rotate({kach:.2f} {sx:.0f} {oy-20:.0f})">'
               f'<rect x="{sx-70 if sgn < 0 else sx-10:.0f}" y="{oy-30}" width="80"'
               f' height="{oh+60}" rx="8" fill="url(#dosk)" {o(7)}/>'
               f'<path d="M{sx-50 if sgn < 0 else sx+10:.0f},{oy+90} q34,70 0,140"'
               f' fill="none" stroke="#5a3a22" stroke-width="9" opacity=".7"/></g>')
    ob += (f'<rect x="{ox-130}" y="{oy+oh+54}" width="{ow+260}" height="46" rx="10"'
           f' fill="url(#dosk)" {o(8)}/>')
    s += SL(Z_SRED, ob)
    s += SL(Z_SRED, teplo(ox + ow / 2, oy + oh + 120, 640, 260, .34 * yarko))
    hod = A.ease(A.seg(t, .3, 2.6))
    px = 1790 - hod * 300
    s += SL(Z_SRED, figura(px, 1060, 470, t, "#1d1a24", "#cfe4f5", False, .6,
                           True, 1.0, True, 1.2, True, True))
    s += SL(Z_SRED, para_izo_rta(px + 54, 672, t, .3, 1.2, .6))
    ruk, (fx, fy) = rukav(px - 100, 780, 140, 76, t, "#1d1a24", "#cfe4f5", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, teplo(fx, fy + 86, 300, 260, .5 + .12 * abs(A.w(t, 1.5))))
    fon = (f'<path d="M{fx-40:.0f},{fy:.0f} q40,-54 80,0" fill="none"'
           f' stroke="{ZHELEZ}" stroke-width="9"/>'
           f'<path d="M{fx-78:.0f},{fy+44:.0f} h156 l-18,-34 h-120 Z" fill="{ZHELEZ}" {o(6)}/>'
           f'<path d="M{fx-66:.0f},{fy+44:.0f} h132 l-14,170 h-104 Z"'
           f' fill="url(#stekl)" opacity=".78" {o(7)}/>')
    fon += ogon(fx, fy + 196, t, .72, .4, 5)
    fon += (f'<path d="M{fx-72:.0f},{fy+214:.0f} h144 l14,40 h-172 Z"'
            f' fill="{ZHELEZ}" {o(6)}/>')
    fon += (f'<line x1="{fx-54:.0f}" y1="{fy+56:.0f}" x2="{fx-44:.0f}"'
            f' y2="{fy+200:.0f}" stroke="#ffffff" stroke-width="9" opacity=".3"/>')
    s += SL(Z_SRED, fon)
    kal = A.out(A.seg(t, 2.0, 1.2))
    kal_g = (f'<rect x="130" y="600" width="34" height="470" rx="10"'
             f' fill="url(#derev)" {o(7)}/>'
             f'<rect x="420" y="600" width="34" height="470" rx="10"'
             f' fill="url(#derev)" {o(7)}/>')
    kal_g += f'<g transform="rotate({-38*kal:.1f} 150 1040)">'
    kal_g += (f'<rect x="150" y="660" width="280" height="400" rx="8"'
              f' fill="url(#dosk)" {o(7)}/>')
    for i in range(4):
        kal_g += (f'<rect x="{162+i*68:.0f}" y="666" width="56" height="388" rx="6"'
                  f' fill="url(#dosk)" {o(5)}/>')
    kal_g += (f'<line x1="150" y1="700" x2="430" y2="800" stroke="#5a3a22"'
              f' stroke-width="14"/>'
              f'<line x1="150" y1="1010" x2="430" y2="910" stroke="#5a3a22"'
              f' stroke-width="14"/>'
              f'<circle cx="400" cy="860" r="14" fill="url(#zhel)" {o(4)}/></g>')
    s += SL(Z_PERED, kal_g)
    s += SL(Z_PERED, pleten(440, 1070, 300, 180, 6))
    s += SL(Z_PERED, goloe_derevo(1810, 1080, 560, t, 37, 7, "#232630"))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 361, .5, .9))
    s += vinetka(.5)
    return s


# ── 36 ─────────────────────────────────────────────────────────────────────
def drova_vedra_i_seno_do_temnoty(t):
    """Закатное крыльцо: хозяин тащит охапку берёзовых дров, хозяйка два
    полных ведра, сын несёт сено на вилах, из хлева тянется морда коровы."""
    rnd = random.Random(3617)
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += nebo("zakat", t, False, 367)
    s += oblaka(t, 210, 5, 373, .4, "#e4b58a", 9.0)
    s += ulica_dal(1180, 690, 760, t, False, 379)
    s += SL(Z_DAL, goloe_derevo(1300, 760, 420, t, 41, 6, "#4a3b2c"))
    s += SL(Z_DAL, gryaz_polosa(780, 190, "#4a3b2c"))
    izb = brevna(60, 180, 1020, 640, 108)
    izb += (f'<path d="M20,190 L570,-80 L1120,190 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<path d="M20,196 L570,-74 L1120,196 L1066,160 L570,-32 L74,160 Z"'
            f' fill="url(#sneg)" opacity=".8" {o(4)}/>')
    izb += (f'<rect x="760" y="-150" width="96" height="200" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(808, -140, t, 5, .2, 300, .34, "#d8cbbd", 1.0))
    ok = okno_izby(170, 330, 250, 190, t, svet=True, moroz=.2)
    ok += (f'<path d="M130,312 h330 l-28,-44 h-274 Z" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, ok)
    s += SL(Z_SRED, teplo(295, 440, 330, 280, .40 + .12 * abs(A.w(t, 1.8))))
    hl = doski(1180, 420, 700, 420, 74, True, "dosk")
    hl += (f'<path d="M1150,430 L1530,250 L1910,430 Z" fill="#6b5436" {o(8)}/>')
    s += SL(Z_SRED, hl)
    okh = (f'<path d="M1290,760 L1290,580 Q1440,500 1590,580 L1590,760 Z"'
           f' fill="#1d1711" {o(9)}/>')
    okh += (f'<path d="M1270,774 h340 l0,-26 h-340 Z" fill="url(#dosk)" {o(6)}/>')
    s += SL(Z_SRED, okh)
    mu = A.ease(A.seg(t, 1.0, 1.4))
    mx = 1420 - mu * 90
    kor = (f'<ellipse cx="{mx:.0f}" cy="640" rx="118" ry="112" fill="#d6c0a2" {o(7)}/>')
    kor += (f'<ellipse cx="{mx-46:.0f}" cy="712" rx="86" ry="58" fill="#f0dcc0" {o(6)}/>')
    for i in (-1, 1):
        kor += (f'<ellipse cx="{mx-70:.0f}" cy="{712+i*22:.0f}" rx="15" ry="20"'
                f' fill="#6b5240" {o(2)}/>')
    kor += (f'<path d="M{mx-96:.0f},712 q50,26 100,0" fill="none" stroke="#b08763"'
            f' stroke-width="7"/>')
    for i, sgn in ((0, -1), (1, 1)):
        kor += (f'<ellipse cx="{mx+sgn*48:.0f}" cy="{586:.0f}" rx="24"'
                f' ry="{8 if A.blink(t, 3.2, .1) else 22}" fill="#f2e8da" {o(4)}/>')
        if not A.blink(t, 3.2, .1):
            kor += (f'<circle cx="{mx+sgn*48:.0f}" cy="588" r="12" fill="#2b2118"/>')
    for sgn in (-1, 1):                 # рога и уши
        kor += (f'<path d="M{mx+sgn*96:.0f},572 q{sgn*52:.0f},-40 {sgn*44:.0f},-96'
                f' q{-sgn*34:.0f},34 {-sgn*52:.0f},70 Z" fill="#e8dcc6" {o(5)}/>')
        kor += (f'<ellipse cx="{mx+sgn*126:.0f}" cy="640" rx="40" ry="24"'
                f' fill="#c3a888" {o(5)}/>')
    kor += (f'<path d="M{mx-30:.0f},532 q30,-30 62,-6" fill="none" stroke="#b09876"'
            f' stroke-width="12" stroke-linecap="round"/>')
    s += SL(Z_SRED, kor)
    s += SL(Z_SRED, par(mx - 86, 726, t, 4, .55, 170, .5, 1.0))
    s += SL(Z_SRED, lavka(1660, 790, 240))
    hx = 560 + A.ease(A.seg(t, .2, 3.4)) * -120
    s += SL(Z_SRED, figura(hx, 1040, 470, t, "#3a3040", "#ffd0a0", False, .2,
                           True, 1.0, True, 1.4, True))
    kach = 4.0 * A.w(t, 1.3, .1)
    for i, sgn in enumerate((-1, 1)):   # руки держат охапку снизу
        ruk, _ = rukav(hx + sgn * 86, 800, 120, -sgn * 150 + sgn * 14, t,
                       "#3a3040", "#ffd0a0", .2 + i * .3, 4.0)
        s += SL(Z_SRED, ruk)
    oh_ = f'<g transform="rotate({kach:.2f} {hx:.0f} 820)">'
    for i in range(12):                 # берёзовые поленья лежат поперёк
        row, col = i // 4, i % 4
        lx = hx - 150 + col * 94 + row * 22
        ly = 770 - row * 68
        oh_ += (f'<rect x="{lx-54:.0f}" y="{ly-30:.0f}" width="108" height="60"'
                f' rx="26" fill="#efe8dc" {o(5)}/>')
        for j in range(3):              # чёрные чёрточки бересты
            oh_ += (f'<path d="M{lx-34+j*32:.0f},{ly-24:.0f} l0,18" stroke="#2f2a26"'
                    f' stroke-width="7" stroke-linecap="round" opacity=".85"/>')
            oh_ += (f'<path d="M{lx-22+j*32:.0f},{ly+8:.0f} l0,12" stroke="#2f2a26"'
                    f' stroke-width="6" stroke-linecap="round" opacity=".7"/>')
        oh_ += (f'<ellipse cx="{lx+54:.0f}" cy="{ly:.0f}" rx="16" ry="30"'
                f' fill="#d8b98a" {o(4)}/>')
        oh_ += (f'<ellipse cx="{lx+54:.0f}" cy="{ly:.0f}" rx="8" ry="16"'
                f' fill="#a9823f" opacity=".8"/>')
    oh_ += '</g>'
    s += SL(Z_SRED, oh_)
    s += SL(Z_SRED, para_izo_rta(hx + 50, 700, t, .1, 1.1, .5))
    zx = 900 + A.ease(A.seg(t, .4, 3.2)) * -130
    s += SL(Z_SRED, figura(zx, 1056, 440, t, "#5b2f3a", "#ffd0a0", True, .5))
    for i, sgn in enumerate((-1, 1)):
        s += SL(Z_SRED, _vedro(zx + sgn * 150, 1050 - i * 8, 1.55, t, True))
        s += SL(Z_SRED, f'<line x1="{zx+sgn*96:.0f}" y1="912" x2="{zx+sgn*128:.0f}"'
                        f' y2="958" stroke="#5b2f3a" stroke-width="22"'
                        f' stroke-linecap="round"/>')
    sy = 1180
    s += SL(Z_SRED, figura(sy, 1010, 390, t, "#2e3a46", "#ffd0a0", False, .7,
                           True, 1.0, False, 1.0, False, True))
    vil_a = -46 + 22 * A.w(t, 1.0, .2)
    ruk, _ = rukav(sy + 60, 790, 130, -24, t, "#2e3a46", "#ffd0a0", .3, 5.0)
    s += SL(Z_SRED, ruk)
    vil = f'<g transform="rotate({vil_a:.1f} {sy+50:.0f} 810)">'
    vil += (f'<line x1="{sy-60:.0f}" y1="810" x2="{sy+330:.0f}" y2="810"'
            f' stroke="url(#derev)" stroke-width="24" stroke-linecap="round"/>')
    for i in range(3):
        vil += (f'<path d="M{sy+320:.0f},810 q50,{-14+i*14:.0f} 120,{-50+i*50:.0f}"'
                f' fill="none" stroke="{ZHELEZ}" stroke-width="13"'
                f' stroke-linecap="round"/>')
    for i in range(16):                 # охапка сена на зубьях
        a = rnd.uniform(-.9, .5)
        ln = rnd.uniform(60, 130)
        vil += (f'<line x1="{sy+360+rnd.uniform(-26,26):.0f}"'
                f' y1="{800+rnd.uniform(-40,30):.0f}"'
                f' x2="{sy+360+math.cos(a)*ln:.0f}" y2="{790+math.sin(a)*ln:.0f}"'
                f' stroke="#d8b96a" stroke-width="7" stroke-linecap="round"/>')
    vil += '</g>'
    s += SL(Z_SRED, vil)
    for i in range(14):                 # сено летит с вил
        p = ((t * .7) + i * .07) % 1.0
        s += SL(Z_SRED, f'<line x1="{sy+380+p*170+rnd.uniform(-20,20):.0f}"'
                        f' y1="{740+p*p*260+rnd.uniform(-20,20):.0f}"'
                        f' x2="{sy+416+p*180:.0f}" y2="{764+p*p*270:.0f}"'
                        f' stroke="#e3c272" stroke-width="6" opacity="{1-p:.2f}"/>')
    stp = (f'<rect x="420" y="1040" width="520" height="40" rx="8" fill="url(#dosk)" {o(7)}/>')
    stp += (f'<rect x="286" y="640" width="70" height="440" rx="10"'
            f' fill="url(#derev)" {o(8)}/>')
    stp += (f'<rect x="292" y="700" width="58" height="250" rx="6" fill="#6b4a2a"'
            f' opacity=".45"/>')
    for i in range(3):                  # меловые зарубки: сделанное за день
        pok = A.ease(A.seg(t, .8 + i * .35, .4))
        if pok > .02:
            stp += (f'<path d="M{302+i*18:.0f},{740:.0f} l{6:.0f},{180*pok:.0f}"'
                    f' stroke="#efe6d2" stroke-width="11" stroke-linecap="round"'
                    f' opacity="{.9*pok:.2f}"/>')
            stp += (f'<path d="M{300+i*18:.0f},{742:.0f} l{4:.0f},{30*pok:.0f}"'
                    f' stroke="#fffaf0" stroke-width="5" stroke-linecap="round"'
                    f' opacity="{.6*pok:.2f}"/>')
    s += SL(Z_SRED, stp)
    s += SL(Z_SRED, kura(690, 1070, t, .8, .3))
    s += SL(Z_SRED, kura(770, 1058, t, .7, .6))
    s += ramka_pp("pravo", "#2a1a12", .5)
    s += SL(Z_PERED, _korzina(230, 1070, 230, 170, t, 383, False))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 389, .4, .8))
    s += vinetka(.44)
    return s


# ── 37 ─────────────────────────────────────────────────────────────────────
def temnyy_podezd(t):
    """Крыльцо хрущёвки на пол-кадра, блестящее льдом: над дверью разбитый
    фонарь, жилец в пальто едет ногой и повисает на перилах."""
    rnd = random.Random(3719)
    s = f'<rect width="{W}" height="{H}" fill="#161d2a"/>'
    s += nebo("noch", t, True, 397)
    s += panelka(-120, 420, 760, t, 3, True, 401)
    s += panelka(1420, 430, 640, t, 3, True, 409)
    s += SL(Z_DAL, gryaz_polosa(880, 200, "#232a33"))
    st = (f'<rect x="420" y="40" width="1140" height="700" fill="url(#beton)" {o(9)}/>')
    for i in range(5):
        st += (f'<line x1="420" y1="{120+i*130:.0f}" x2="1560" y2="{120+i*130:.0f}"'
               f' stroke="{BETON2}" stroke-width="6" opacity=".7"/>')
    for i in range(4):
        st += (f'<rect x="{470+i*280:.0f}" y="70" width="150" height="150" rx="6"'
               f' fill="{"#39465a" if i % 2 else SVET}"'
               f' opacity="{.3 if i % 2 else .35+.3*abs(A.w(t,7+i,i*.2)):.2f}" {o(5)}/>')
    s += SL(Z_DAL, st)
    kz = (f'<path d="M520,420 h960 l-60,-120 h-840 Z" fill="{BETON2}" {o(9)}/>')
    kz += (f'<rect x="520" y="414" width="960" height="34" rx="8" fill="#6b747c" {o(7)}/>')
    s += SL(Z_SRED, kz)
    dx_, dy_, dw, dh = 760, 440, 420, 560
    hlop = abs(A.w(t, 2.6, .1))
    s += SL(Z_SRED, f'<rect x="{dx_-40}" y="{dy_-30}" width="{dw+80}" height="{dh+30}"'
                    f' rx="8" fill="#3d4650" {o(9)}/>')
    s += SL(Z_SRED, dver(dx_, dy_, dw, dh, .22 * hlop, "url(#zhel)", True, False))
    stek = (f'<rect x="{dx_+70}" y="{dy_+60}" width="{dw-140}" height="170" rx="8"'
            f' fill="url(#stekl)" opacity=".55" {o(6)}/>')
    s += SL(Z_SRED, stek)
    s += SL(Z_SRED, tusklaya_lampochka(dx_ + dw / 2, dy_ + 130, t, .8, False))
    f_x, f_y = dx_ + dw / 2, dy_ - 80
    fon = (f'<path d="M{f_x-80:.0f},{f_y:.0f} h160 l-26,-80 h-108 Z" fill="{ZHELEZ}" {o(7)}/>')
    for i in range(5):
        fon += (f'<path d="M{f_x-60+i*32:.0f},{f_y:.0f} l{10-i*4},34 l16,-34 Z"'
                f' fill="#8fb8ce" opacity=".5" {o(3)}/>')
    isk = 1.0 if ((t * 2.3) % 1.0) > .82 else .0
    if isk > .5:
        fon += (f'<circle cx="{f_x:.0f}" cy="{f_y+16:.0f}" r="16" fill="{SVET}"'
                f' opacity=".9"/>')
        fon += teplo(f_x, f_y + 20, 200, 160, .4)
    fon += (f'<line x1="{f_x:.0f}" y1="{f_y-80:.0f}" x2="{f_x:.0f}" y2="{f_y-120:.0f}"'
            f' stroke="{ZHELEZ}" stroke-width="9"/>')
    s += SL(Z_SRED, fon)
    sz = (f'<path d="M420,1000 h1120 l0,30 h-1120 Z" fill="#8b949c" {o(7)}/>')
    for i in range(3):
        yy = 1000 + i * 28
        sz += (f'<rect x="{440+i*22:.0f}" y="{yy:.0f}" width="{1080-i*44:.0f}"'
               f' height="30" rx="4" fill="url(#beton)" {o(6)}/>')
        for j in range(8):
            bl = .25 + .55 * abs(A.w(t, 1.4 + j * .2, i * .3 + j * .11))
            sz += (f'<ellipse cx="{500+j*130+i*18:.0f}" cy="{yy+12:.0f}" rx="46"'
                   f' ry="8" fill="url(#led)" opacity="{bl:.2f}"/>')
            sz += (f'<circle cx="{512+j*130+i*18:.0f}" cy="{yy+8:.0f}" r="6"'
                   f' fill="#ffffff" opacity="{bl*.9:.2f}"/>')
    s += SL(Z_SRED, sz)
    ned = A.ease(A.seg(t, 1.2, 1.6))
    zx, zy = 1240, 1010 + ned * 40
    s += SL(Z_SRED, figura(zx, zy, 540, t, "#2d3340", "#cfe4f5", False, .4,
                           True, 1.0, False, 3.0 + 7 * ned, False, True))
    s += SL(Z_SRED, para_izo_rta(zx + 46, zy - 460, t, .2, 1.2, .6))
    noga = 24 + 50 * ned
    s += SL(Z_SRED, f'<g transform="rotate({noga:.1f} {zx-30:.0f} {zy-120:.0f})">'
                    f'<rect x="{zx-56:.0f}" y="{zy-120:.0f}" width="56" height="140"'
                    f' rx="24" fill="#2d3340" {o(5)}/>'
                    f'<path d="M{zx-66:.0f},{zy+18:.0f} q42,-28 88,8 q-26,26 -88,-8 Z"'
                    f' fill="#4a3f36" {o(5)}/></g>')
    for sgn, px in ((-1, 660), (1, 1340)):   # перила: стойки, поручень, подзор
        per = (f'<path d="M{px:.0f},900 L{px+sgn*230:.0f},1070" stroke="url(#zhel)"'
               f' stroke-width="26" stroke-linecap="round"/>')
        per += (f'<path d="M{px:.0f},960 L{px+sgn*230:.0f},1080" stroke="{ZHELEZ}"'
                f' stroke-width="14" stroke-linecap="round"/>')
        for i in range(4):
            qx = px + sgn * i * 72
            per += (f'<rect x="{qx-9:.0f}" y="{900+i*44:.0f}" width="18"'
                    f' height="{130+i*20:.0f}" fill="{ZHELEZ}" {o(4)}/>')
        per += (f'<circle cx="{px:.0f}" cy="900" r="16" fill="url(#zhel)" {o(4)}/>')
        s += SL(Z_SRED, per)
    for i, (ug, ph) in enumerate(((128 + 14 * ned, .1), (56 - 18 * ned, .5))):
        ruk, (ax, ay) = rukav(zx + (-46 if i == 0 else 56), zy - 392, 150, ug, t,
                              "#2d3340", "#cfe4f5", ph, 3.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="28" ry="22"'
                        f' fill="#1f242c" {o(4)}/>')
    s += SL(Z_SRED, kot(520, 1072, t, .7, "#2a2622"))
    bak = (f'<rect x="200" y="760" width="230" height="300" rx="14" fill="#3f4a44" {o(8)}/>')
    bak += (f'<rect x="186" y="730" width="258" height="46" rx="12" fill="#55615a" {o(6)}/>')
    bak += (f'<line x1="240" y1="800" x2="240" y2="1050" stroke="#2c342f" stroke-width="8"/>'
            f'<line x1="390" y1="800" x2="390" y2="1050" stroke="#2c342f" stroke-width="8"/>')
    s += SL(Z_SRED, bak)
    s += SL(Z_PERED, goloe_derevo(130, 1080, 620, t, 43, 8, "#1f242c", True))
    s += ramka_pp("pravo", "#0c1016", .55)
    s += SL(Z_LETIT, mokryy_sneg(t, 30, 419, .62, 1.1))
    s += vinetka(.5)
    return s


# ── 38 ─────────────────────────────────────────────────────────────────────
def pochtovye_yaschiki_i_larek(t):
    """Ряд синих почтовых ящиков в подъезде на пол-кадра: из одного торчит
    газета, а за окном подъезда через тёмный двор догорает ларёк."""
    rnd = random.Random(3823)
    s = f'<rect width="{W}" height="{H}" fill="#4d5a5c"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="url(#beton)" opacity=".55"/>')
    sten = ""
    for i in range(7):
        sten += (f'<rect x="-20" y="{i*160:.0f}" width="1080" height="150"'
                 f' fill="{"#7d8a86" if i % 2 else "#8c9792"}" opacity=".9" {o(3)}/>')
    sten += (f'<rect x="-20" y="620" width="1080" height="30" fill="#5f6a66" {o(4)}/>')
    s += SL(Z_DAL, sten)
    s += SL(Z_DAL, f'<rect x="1040" y="0" width="880" height="1080" fill="#6e7a7c"'
                   f' opacity=".9"/>')
    s += SL(Z_SRED, tusklaya_lampochka(520, 110, t, 1.1, True))
    yx, yy, yw, yh = 150, 300, 740, 520
    ya = (f'<rect x="{yx-22}" y="{yy-26}" width="{yw+44}" height="{yh+52}" rx="12"'
          f' fill="{ZHELEZ}" {o(9)}/>')
    for r in range(4):
        for c in range(4):
            bx = yx + 10 + c * (yw - 20) / 4
            by = yy + 10 + r * (yh - 20) / 4
            ya += (f'<rect x="{bx:.0f}" y="{by:.0f}" width="{(yw-20)/4-12:.0f}"'
                   f' height="{(yh-20)/4-12:.0f}" rx="7" fill="{TKAN2}" {o(5)}/>')
            ya += (f'<rect x="{bx+10:.0f}" y="{by+16:.0f}" width="{(yw-20)/4-44:.0f}"'
                   f' height="14" rx="5" fill="#223449" {o(3)}/>')
            ya += (f'<circle cx="{bx+(yw-20)/4-32:.0f}" cy="{by+(yh-20)/4-36:.0f}"'
                   f' r="9" fill="url(#zhel)" {o(3)}/>')
            ya += (f'<path d="M{bx+6:.0f},{by+8:.0f} l{(yw-20)/4-26:.0f},0"'
                   f' stroke="#6f8ca8" stroke-width="5" opacity=".5"/>')
    s += SL(Z_SRED, ya)
    drozh = 3.0 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, _gazeta(430, 470 + drozh, 300, 220, -16 + drozh, 431))
    s += SL(Z_SRED, _gazeta(300, 1010, 280, 190, 6, 433))
    klyuch = A.ease(A.seg(t, .4, 1.3))
    s += SL(Z_SRED, figura(1120, 1070, 560, t, "#53432f", "#ffd0a0", False, .3,
                           True, 1.0, False, 1.6, True))
    ruk, (hx, hy) = rukav(1030, 700, 140, 194 + 10 * A.w(t, 1.2), t, "#53432f",
                          "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<g transform="translate({-klyuch*120:.0f},{klyuch*40:.0f})">'
                    f'<rect x="{hx-10:.0f}" y="{hy-10:.0f}" width="74" height="16"'
                    f' rx="6" fill="url(#zhel)" {o(4)}/>'
                    f'<circle cx="{hx+70:.0f}" cy="{hy-2:.0f}" r="18" fill="none"'
                    f' stroke="{MED}" stroke-width="9"/>'
                    f'<path d="M{hx-10:.0f},{hy+6:.0f} l0,16 l14,0" fill="none"'
                    f' stroke="url(#zhel)" stroke-width="8"/></g>')
    s += SL(Z_SRED, f'<ellipse cx="{hx+30:.0f}" cy="{hy:.0f}" rx="28" ry="20"'
                    f' fill="#53432f" {o(4)}/>')
    ox, oy, ow, oh = 1230, 240, 560, 500
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#121a26"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.6:.0f}" width="{ow}" height="{oh*.4:.0f}"'
           f' fill="#1b2430"/>')
    for i in range(3):
        za += (f'<rect x="{ox+30+i*190:.0f}" y="{oy+70+((i%2)*40):.0f}" width="150"'
               f' height="{oh*.52:.0f}" fill="#263040" opacity=".95"/>')
        for j in range(4):
            on = (i + j) % 3 == 0
            za += (f'<rect x="{ox+48+i*190+(j%2)*70:.0f}"'
                   f' y="{oy+100+((i%2)*40)+(j//2)*90:.0f}" width="50" height="52"'
                   f' fill="{SVET if on else "#39455a"}"'
                   f' opacity="{.3+.5*abs(A.w(t,6+j,i*.3)) if on else .25:.2f}"/>')
    gas = A.ease(A.seg(t, 3.4, 1.0))
    lx, ly = ox + ow * .50, oy + oh * .88
    lar = (f'<rect x="{lx-230:.0f}" y="{ly-330:.0f}" width="460" height="330" rx="10"'
           f' fill="#3c4a52" {o(7)}/>')
    lar += (f'<path d="M{lx-262:.0f},{ly-330:.0f} h524 l-26,-56 h-472 Z"'
            f' fill="#55646c" {o(6)}/>')
    lar += (f'<rect x="{lx-196:.0f}" y="{ly-292:.0f}" width="392" height="190" rx="8"'
            f' fill="{SVET}" opacity="{(.88-.76*gas)*(.74+.26*abs(A.w(t,.9))):.2f}" {o(5)}/>')
    for i in range(5):                  # товар на витрине силуэтами
        lar += (f'<rect x="{lx-170+i*76:.0f}" y="{ly-262+((i%2)*26):.0f}" width="52"'
                f' height="{120-((i%2)*26):.0f}" rx="6" fill="#6b5a3c"'
                f' opacity="{.8*(1-gas)+.15:.2f}" {o(3)}/>')
    lar += (f'<rect x="{lx-60:.0f}" y="{ly-92:.0f}" width="120" height="92" rx="6"'
            f' fill="#2a333a" {o(5)}/>')
    for i in range(11):
        mg = (.5 + .5 * A.w(t, .7 + i * .13, i * .2)) * (1 - gas)
        lar += (f'<circle cx="{lx-220+i*44:.0f}" cy="{ly-354:.0f}" r="14"'
                f' fill="{[SVET, KRAS, ZEL2][i%3]}" opacity="{.22+.72*mg:.2f}"/>')
    lar += teplo(lx, ly - 210, 420, 330, .55 * (1 - gas))
    za += lar
    za += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#0b1018"'
           f' opacity="{.1+.3*gas:.2f}"/>')
    s += SL(Z_SRED, f'<clipPath id="pyo38"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#pyo38)">{za}</g>')
    ram = (f'<rect x="{ox-30}" y="{oy-30}" width="{ow+60}" height="{oh+60}" rx="8"'
           f' fill="none" stroke="url(#beton)" stroke-width="62"/>')
    ram += (f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}" y2="{oy+oh}"'
            f' stroke="#cdd6d8" stroke-width="22"/>'
            f'<line x1="{ox}" y1="{oy+oh*.5:.0f}" x2="{ox+ow}" y2="{oy+oh*.5:.0f}"'
            f' stroke="#cdd6d8" stroke-width="22"/>')
    ram += (f'<rect x="{ox-46}" y="{oy+oh+30}" width="{ow+92}" height="34" rx="8"'
            f' fill="#b9c2c4" {o(6)}/>')
    ram += (f'<path d="M{ox+40},{oy+40} l200,220" stroke="#ffffff" stroke-width="12"'
            f' opacity=".2"/>')
    s += SL(Z_SRED, ram)
    s += SL(Z_SRED, teplo(ox + ow * .5, oy + oh * .62, 560, 440, .40 * (1 - gas)))
    s += SL(Z_SRED, f'<ellipse cx="{ox+ow*.4:.0f}" cy="1010" rx="420" ry="90"'
                    f' fill="{SVET}" opacity="{.20*(1-gas):.2f}"/>')
    rad = ""
    for i in range(7):
        rad += (f'<rect x="{1280+i*62:.0f}" y="800" width="42" height="190" rx="12"'
                f' fill="#cfd6d8" {o(5)}/>')
    rad += (f'<rect x="1264" y="830" width="470" height="18" fill="#b2babc" {o(4)}/>')
    s += SL(Z_SRED, rad)
    s += SL(Z_SRED, teplo(1500, 900, 300, 180, .18))
    lest = (f'<path d="M-20,1080 L420,1080 L420,860 L-20,990 Z" fill="#7d8a86"'
            f' opacity=".95" {o(6)}/>')
    for i in range(4):
        lest += (f'<path d="M{-20+i*110:.0f},{1010-i*34:.0f} h120 l0,34 h-120 Z"'
                 f' fill="#919c98" {o(5)}/>')
    s += SL(Z_PERED, lest)
    sh = A.ease(A.seg(t, 4.2, 1.4))
    for i, sgn in enumerate((-1, 1)):
        tx = 200 + sgn * 56 + sh * 180
        ty = 1000 - sh * 130 - i * 20 - abs(A.w(t, .5, i * .5)) * 18
        s += SL(Z_PERED, f'<path d="M{tx-64:.0f},{ty:.0f} q10,-40 64,-40'
                         f' q58,0 64,34 q-6,26 -64,26 q-54,0 -64,-20 Z"'
                         f' fill="#8f3a42" {o(5)}/>'
                         f'<path d="M{tx-50:.0f},{ty-28:.0f} q50,-26 96,4"'
                         f' fill="none" stroke="#d9a0a6" stroke-width="12"/>'
                         f'<ellipse cx="{tx+10:.0f}" cy="{ty+6:.0f}" rx="52" ry="12"'
                         f' fill="#5e2329" opacity=".8"/>')
    s += ramka_pp("levo", "#141a1c", .45)
    s += vinetka(.46)
    return s


# ── 39 ─────────────────────────────────────────────────────────────────────
def tri_nastoyaschie_nuzhdy(t):
    """Три картинки по словам: аптечный пакет под зелёным крестом, медсестра
    у остановки под тёплым фонарём, внучка с судками на лестнице."""
    rnd = random.Random(3929)
    s = f'<rect width="{W}" height="{H}" fill="#1b2230"/>'
    s += nebo("noch", t, True, 439)
    pw = 600
    for i in range(3):
        px = 20 + i * (pw + 20)
        s += SL(Z_DAL, f'<rect x="{px}" y="90" width="{pw}" height="900" rx="12"'
                       f' fill="#2a3340" {o(10)}/>')
    # 1: аптека
    px = 20
    ap = (f'<rect x="{px+10}" y="100" width="{pw-20}" height="880" rx="8" fill="#243043"/>')
    ap += (f'<rect x="{px+10}" y="620" width="{pw-20}" height="360" fill="#2f3b4a"/>')
    ap += (f'<rect x="{px+60}" y="300" width="{pw-120}" height="330" rx="8"'
           f' fill="{SVET}" opacity="{.26+.1*abs(A.w(t,2.4)):.2f}" {o(6)}/>')
    for j in range(3):
        ap += (f'<rect x="{px+100+j*150:.0f}" y="360" width="100" height="220" rx="6"'
               f' fill="#c9d8e2" opacity=".5" {o(4)}/>')
    mig = .35 + .65 * (1.0 if ((t * 1.1) % 1.0) > .3 else .25)
    kx, ky = px + pw / 2, 230
    ap += (f'<rect x="{kx-120:.0f}" y="{ky-86:.0f}" width="240" height="172" rx="14"'
           f' fill="#14301f" {o(7)}/>')
    for a, b, c, d in ((-34, -84, 68, 168), (-84, -34, 168, 68)):
        ap += (f'<rect x="{kx+a:.0f}" y="{ky+b:.0f}" width="{c}" height="{d}" rx="10"'
               f' fill="#3ad07a" opacity="{mig:.2f}"/>')
    ap += teplo(kx, ky, 300, 240, .3 * mig)
    ap += (f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="{30+10*abs(A.w(t,1.3)):.0f}"'
           f' fill="#9ff7c4" opacity="{.3*mig:.2f}"/>')
    pod = A.out(A.seg(t, .3, 1.2))
    bgx, bgy = px + pw * .5, 700 - pod * 50
    ruk, (hx, hy) = rukav(px + pw * .46, 1010, 190, -84, t, "#3a3f4c", "#cfe4f5", .2, 3.0)
    ap += ruk
    ap += (f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="32" ry="24" fill="#3a3f4c" {o(4)}/>')
    ap += (f'<path d="M{bgx-150:.0f},{bgy:.0f} h300 l-20,330 h-260 Z"'
           f' fill="url(#krem)" {o(8)}/>')
    ap += (f'<path d="M{bgx-150:.0f},{bgy:.0f} h300 l-16,42 h-268 Z"'
           f' fill="#e2d7bd" {o(5)}/>')
    for sgn in (-1, 1):                 # ручки пакета
        ap += (f'<path d="M{bgx+sgn*76:.0f},{bgy+6:.0f} q{sgn*10:.0f},-86'
                f' {-sgn*70:.0f},-84" fill="none" stroke="{MED}" stroke-width="13"'
                f' stroke-linecap="round"/>')
    for a, b, c, d in ((-40, -16, 80, 32), (-16, -40, 32, 80)):
        ap += (f'<rect x="{bgx+a:.0f}" y="{bgy+190+b:.0f}" width="{c}" height="{d}"'
               f' rx="8" fill="#2fae63" {o(4)}/>')
    ap += (f'<rect x="{bgx+54:.0f}" y="{bgy-96:.0f}" width="86" height="120" rx="10"'
           f' fill="url(#stekl)" opacity=".92" {o(6)}/>')
    ap += (f'<rect x="{bgx+66:.0f}" y="{bgy-128:.0f}" width="62" height="36" rx="8"'
           f' fill="{TKAN}" {o(5)}/>')
    ap += (f'<rect x="{bgx+62:.0f}" y="{bgy-52:.0f}" width="70" height="60" rx="6"'
           f' fill="#d8e8f2" opacity=".85"/>')
    ap += (f'<rect x="{bgx-130:.0f}" y="{bgy-70:.0f}" width="110" height="80" rx="10"'
           f' fill="#f2f6fa" {o(5)}/>')
    for i in range(3):
        ap += (f'<circle cx="{bgx-108+i*34:.0f}" cy="{bgy-30:.0f}" r="12"'
               f' fill="#9fb6cf" {o(3)}/>')
    s += SL(Z_SRED, ap)
    # 2: медсестра
    px = 640
    md = (f'<rect x="{px+10}" y="100" width="{pw-20}" height="880" rx="8" fill="#1f2a38"/>')
    md += (f'<rect x="{px+10}" y="800" width="{pw-20}" height="180" fill="#2b3340"/>')
    for j in range(5):
        md += (f'<rect x="{px+40+j*120:.0f}" y="{300+((j%2)*60):.0f}" width="90"'
               f' height="{480-((j%2)*60):.0f}" fill="#263141" opacity=".9"/>')
        for k_ in range(3):
            on = (j + k_) % 2 == 0
            md += (f'<rect x="{px+56+j*120:.0f}" y="{330+((j%2)*60)+k_*110:.0f}"'
                   f' width="58" height="66" fill="{SVET if on else "#39455a"}"'
                   f' opacity="{.3+.4*abs(A.w(t,5+j,k_*.3)) if on else .22:.2f}"/>')
    md += (f'<rect x="{px+60}" y="420" width="300" height="34" rx="6" fill="#4a5664" {o(5)}/>')
    md += (f'<rect x="{px+70}" y="446" width="22" height="360" fill="#4a5664" {o(4)}/>'
           f'<rect x="{px+330}" y="446" width="22" height="360" fill="#4a5664" {o(4)}/>')
    md += (f'<rect x="{px+90}" y="660" width="250" height="24" rx="8" fill="#5c6a76" {o(4)}/>')
    md += tusklaya_lampochka(px + 200, 380, t, .9, True)
    sp = A.ease(A.seg(t, .2, 2.6))
    mx = px + 480 - sp * 150
    md += figura(mx, 960, 440, t, "#3b4756", "#ffe6c8", False, .4, True, 1.0, False, 1.0)
    md += (f'<path d="M{mx-66:.0f},{960-310:.0f} q66,-26 132,0 l-12,250 h-108 Z"'
           f' fill="#f2f6fa" opacity=".92" {o(5)}/>')
    md += (f'<path d="M{mx-30:.0f},{960-300:.0f} l0,230" stroke="#cfd8e0"'
           f' stroke-width="6" opacity=".9"/>')
    md += para_izo_rta(mx + 44, 960 - 372, t, .2, 1.1, .6)
    md += (f'<ellipse cx="{mx-78:.0f}" cy="{960-180:.0f}" rx="52" ry="40"'
           f' fill="{TKAN}" {o(5)}/>')
    s += SL(Z_SRED, md)
    # 3: внучка с судками
    px = 1260
    vn = (f'<rect x="{px+10}" y="100" width="{pw-20}" height="880" rx="8" fill="#2b2a2c"/>')
    for j in range(5):
        vn += (f'<path d="M{px+10:.0f},{980-j*150:.0f} h{pw-20-j*40:.0f} l0,-60'
               f' h{-(pw-20-j*40):.0f} Z" fill="{"#6e6a66" if j % 2 else "#7a766f"}"'
               f' opacity=".95" {o(5)}/>')
    vn += (f'<path d="M{px+20},980 L{px+pw-120},300" stroke="#8d8880" stroke-width="20"'
           f' opacity=".9"/>')
    vn += tusklaya_lampochka(px + 150, 220, t, .8, False)
    pd = A.ease(A.seg(t, .4, 3.0))
    vx = px + 200 + pd * 180
    vy = 950 - pd * 250
    vn += figura(vx, vy, 400, t, "#4a2f3c", "#ffe6c8", True, .6)
    kach = 7.0 * A.w(t, 1.1, .2)
    ruk, _ = rukav(vx + 72, vy - 300, 120, 26, t, "#4a2f3c", "#ffe6c8", .3, 4.0)
    vn += ruk
    vn += f'<g transform="rotate({kach:.2f} {vx+150:.0f} {vy-290:.0f})">'
    vn += (f'<path d="M{vx+86:.0f},{vy-290:.0f} q64,-66 128,0" fill="none"'
           f' stroke="{ZHELEZ}" stroke-width="12"/>')
    for j in range(3):                  # судки: три бидона друг на друге
        cy_ = vy - 250 + j * 84
        vn += (f'<rect x="{vx+70:.0f}" y="{cy_:.0f}" width="160" height="76" rx="12"'
               f' fill="url(#zhel)" {o(6)}/>')
        vn += (f'<ellipse cx="{vx+150:.0f}" cy="{cy_:.0f}" rx="80" ry="18"'
               f' fill="#b9c2c6" {o(5)}/>')
        vn += (f'<path d="M{vx+86:.0f},{cy_+30:.0f} h128" stroke="#8a9398"'
               f' stroke-width="7" opacity=".8"/>')
        vn += (f'<path d="M{vx+94:.0f},{cy_+12:.0f} l0,42" stroke="#eef4f8"'
               f' stroke-width="9" opacity="{.3+.3*abs(A.w(t,2.0,j*.3)):.2f}"/>')
    for sgn in (-1, 1):                 # боковые дужки стяжки
        vn += (f'<line x1="{vx+150+sgn*84:.0f}" y1="{vy-282:.0f}"'
               f' x2="{vx+150+sgn*84:.0f}" y2="{vy-78:.0f}" stroke="{ZHELEZ}"'
               f' stroke-width="10"/>')
    vn += '</g>'
    vn += par(vx + 150, vy - 300, t, 4, .45, 150, .5, .8)
    buh = A.ease(A.seg(t, 2.4, 1.6))
    vn += (f'<path d="M{px+440:.0f},{620+buh*230:.0f} q70,-96 140,0 q-70,40 -140,0 Z"'
           f' fill="url(#med)" {o(6)}/>')
    vn += (f'<path d="M{px+470:.0f},{600+buh*230:.0f} q40,-20 80,0" fill="none"'
           f' stroke="#f2cf8c" stroke-width="7" opacity=".7"/>')
    vn += (f'<path d="M{px+400:.0f},{700+buh*230:.0f} h220 l-20,180 h-180 Z"'
           f' fill="{TKAN2}" opacity=".9" {o(6)}/>')
    s += SL(Z_SRED, vn)
    for i in range(2):
        s += SL(Z_PERED, f'<rect x="{620+i*620}" y="60" width="26" height="960"'
                         f' fill="#0d1118" opacity=".95"/>')
    s += ramka_pp("oba", "#0b0e14", .5)
    s += vinetka(.46)
    return s


# ── 40 ─────────────────────────────────────────────────────────────────────
def gorshok_s_uglyami_na_shestke(t):
    """Шесток печи: глиняный горшок на пол-кадра полон красных углей, жар
    дрожит, чужой рукав тянется — и крышка накрывает горшок."""
    rnd = random.Random(4001)
    s = f'<rect width="{W}" height="{H}" fill="#221711"/>'
    s += SL(Z_DAL, brevna(0, 0, 520, 1080, 104))
    s += SL(Z_DAL, f'<rect x="440" y="0" width="1480" height="1080" fill="url(#pech)"'
                   f' opacity=".96"/>')
    kl = kladka(440, 0, 1480, 420, 92, "url(#pech)")
    s += SL(Z_DAL, kl)
    s += utvar_izby(80, 300, 380, t, 443)
    ust = kirpich_ustya(1420, 300, 420, 360, t, True)
    s += SL(Z_SRED, ust)
    s += SL(Z_SRED, f'<path d="{kontur_proema(1420, 300, 420, 360, "ustie")}"'
                    f' fill="#1a0d06"/>'
                    + ugli(1460, 620, 340, t, 7, 449)
                    + ogon(1630, 630, t, 1.0, .3, 6))
    s += SL(Z_SRED, iskra_let(t, 1630, 560, 9, 457, 300, .5))
    sh = (f'<rect x="420" y="700" width="1500" height="110" rx="14"'
          f' fill="{PECH2}" {o(9)}/>')
    sh += (f'<rect x="420" y="792" width="1500" height="40" fill="#b9a98c" {o(6)}/>')
    for i in range(9):
        sh += (f'<line x1="{470+i*160:.0f}" y1="700" x2="{470+i*160:.0f}" y2="792"'
               f' stroke="#cdbb9c" stroke-width="5" opacity=".7"/>')
    s += SL(Z_SRED, sh)
    s += SL(Z_SRED, polovicy(900))
    gx, gy = 840, 700
    gor = ten(gx, gy + 4, 230, 30, .62)
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-6:.0f}" rx="196" ry="30"'
            f' fill="#7d4a23" opacity=".55"/>')
    gor += (f'<path d="M{gx-186:.0f},{gy-110:.0f} q-54,-200 46,-330'
            f' q{140:.0f},-56 {280:.0f},0 q100,130 46,330 Z"'
            f' fill="url(#glina)" {o(9)}/>')
    gor += (f'<path d="M{gx-186:.0f},{gy-110:.0f} q186,60 372,0 l-10,110'
            f' q-176,48 -352,0 Z" fill="#8e5a2c" {o(7)}/>')
    for i in range(4):
        gor += (f'<path d="M{gx-178+i*4:.0f},{gy-210-i*54:.0f} q{178-i*6:.0f},{44-i*6:.0f}'
                f' {356-i*12:.0f},0" fill="none" stroke="#a9693a" stroke-width="7"'
                f' opacity=".7"/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-440:.0f}" rx="206" ry="52"'
            f' fill="#7d4a23" {o(8)}/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-432:.0f}" rx="178" ry="40"'
            f' fill="#2c1206"/>')
    s += SL(Z_SRED, gor)
    for i in range(16):
        rr = 20 + rnd.uniform(0, 26)
        ux = gx - 150 + rnd.uniform(0, 300)
        uy = gy - 448 + rnd.uniform(-12, 18)
        pul = .45 + .55 * abs(A.w(t, 1.1 + rnd.uniform(0, 1.3), i * .14))
        s += SL(Z_SRED, f'<ellipse cx="{ux:.0f}" cy="{uy:.0f}" rx="{rr:.0f}"'
                        f' ry="{rr*.56:.0f}" fill="{UGOL}" opacity="{pul:.2f}"/>')
        s += SL(Z_SRED, f'<ellipse cx="{ux:.0f}" cy="{uy-4:.0f}" rx="{rr*.5:.0f}"'
                        f' ry="{rr*.28:.0f}" fill="{ORA}" opacity="{pul*.9:.2f}"/>')
    s += SL(Z_SRED, ugli(gx - 150, gy - 444, 300, t, 9, 461))
    s += SL(Z_SRED, ogon(gx, gy - 440, t, .9, .1, 7))
    s += SL(Z_SRED, teplo(gx, gy - 400, 520, 440, .5 + .14 * abs(A.w(t, 1.3))))
    for i in range(4):
        zh = .18 + .14 * abs(A.w(t, 1.0 + i * .3, i * .2))
        s += SL(Z_SRED, f'<ellipse cx="{gx+(i-1.5)*60:.0f}"'
                        f' cy="{gy-520-i*52-18*A.w(t,1.6,i*.3):.0f}"'
                        f' rx="{90+i*22:.0f}" ry="{26+i*8:.0f}" fill="{ORA}"'
                        f' opacity="{zh:.2f}"/>')
    s += SL(Z_SRED, iskra_let(t, gx, gy - 470, 12, 463, 420, .45))
    tyan = abs(A.w(t, 2.2, .1))
    s += SL(Z_SRED, f'<path d="M1920,180 q-60,120 -40,300 l140,0 l0,-300 Z"'
                    f' fill="#241d2c" {o(7)}/>')
    ruk, (chx, chy) = rukav(1900, 330, 420 + 40 * tyan, 172, t, "#2a2230",
                            "#9fb6cf", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{chx:.0f}" cy="{chy:.0f}" rx="44" ry="30"'
                    f' fill="#2a2230" {o(5)}/>'
                    f'<ellipse cx="{chx+16:.0f}" cy="{chy-8:.0f}" rx="22" ry="14"'
                    f' fill="#4a3f52" opacity=".8"/>')
    kry = A.ease(A.seg(t, 1.2, .7))
    ky_ = gy - 700 + kry * 200
    s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{ky_:.0f}" rx="214" ry="54"'
                    f' fill="url(#glina)" {o(8)}/>'
                    f'<ellipse cx="{gx:.0f}" cy="{ky_-26:.0f}" rx="150" ry="34"'
                    f' fill="#b07a44" {o(5)}/>'
                    f'<ellipse cx="{gx:.0f}" cy="{ky_-54:.0f}" rx="40" ry="22"'
                    f' fill="#8e5a2c" {o(6)}/>')
    s += SL(Z_SRED, krynka(400, 780, 1.5))
    s += SL(Z_SRED, f'<rect x="300" y="620" width="30" height="300" rx="10"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<path d="M250,620 q66,-90 130,0" fill="none" stroke="{ZHELEZ}"'
                    f' stroke-width="18"/>')
    s += SL(Z_SRED, f'<path d="M1240,700 q66,100 132,0 q-66,30 -132,0 Z"'
                    f' fill="url(#chug)" {o(7)}/>'
                    f'<ellipse cx="1306" cy="692" rx="70" ry="20" fill="#4a4645" {o(5)}/>')
    s += SL(Z_SRED, par(1306, 672, t, 4, .4, 150, .45, .8))
    s += ramka_pp("levo", "#160d08", .5)
    s += SL(Z_PERED, _korzina(1760, 1070, 240, 180, t, 467, False))
    s += vinetka(.46)
    return s


# ── 41 ─────────────────────────────────────────────────────────────────────
def holodnaya_pech_utrom(t):
    """Серое утро: печь с чёрным холодным устьем на пол-кадра, хозяин дует в
    остывшую золу, семья дрожит под одеялом, а у соседа труба дымит."""
    rnd = random.Random(4103)
    s = f'<rect width="{W}" height="{H}" fill="#6b6a66"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 110))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#9aa3a8" opacity=".22"/>')
    s += utvar_izby(1180, 300, 480, t, 419)
    s += SL(Z_SRED, polovicy(900))
    pch = pech(60, 150, 640, 790, t, False, True, False)
    s += SL(Z_SRED, pch)
    ux, uy, uw, uh = 148, 480, 300, 250
    ust = (f'<path d="{kontur_proema(ux, uy, uw, uh, "ustie")}" fill="#0f0c0a"/>')
    ust += (f'<path d="{kontur_proema(ux, uy, uw, uh, "ustie")}" fill="none" {o(9)}/>')
    for i in range(14):                 # холодная зола: ни искры
        zx = ux + 26 + rnd.uniform(0, uw - 52)
        ust += (f'<ellipse cx="{zx:.0f}" cy="{uy+uh-24+rnd.uniform(-10,10):.0f}"'
                f' rx="{rnd.uniform(14,26):.0f}" ry="{rnd.uniform(6,12):.0f}"'
                f' fill="#8d8880" opacity=".65"/>')
    s += SL(Z_SRED, ust)
    s += SL(Z_SRED, f'<rect x="80" y="752" width="600" height="46" rx="10"'
                    f' fill="#c9bda4" {o(7)}/>')
    duy = (t * 1.4) % 1.0
    hx, hy = 620, 930
    s += SL(Z_SRED, figura(hx, hy, 520, t, "#3e4652", "#e8eef6", False, .2,
                           True, 1.0, False, 2.4, True))
    s += SL(Z_SRED, f'<ellipse cx="{hx-86:.0f}" cy="{hy+4:.0f}" rx="56" ry="18"'
                    f' fill="#e3c6a8" {o(5)}/>'
                    f'<ellipse cx="{hx+72:.0f}" cy="{hy+6:.0f}" rx="52" ry="16"'
                    f' fill="#e3c6a8" {o(5)}/>')
    for i in range(4):                  # струя воздуха в устье
        k = (duy + i * .25) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{hx-120-k*190:.0f}" cy="{hy-330+k*24:.0f}"'
                        f' rx="{24+k*62:.0f}" ry="{12+k*26:.0f}" fill="#e8eef6"'
                        f' opacity="{.5*(1-k):.2f}"/>')
    for i in range(10):                 # поднятая зола
        k = (duy * .8 + i * .1) % 1.0
        s += SL(Z_SRED, f'<circle cx="{ux+uw*.5-k*60+rnd.uniform(-40,40):.0f}"'
                        f' cy="{uy+uh-30-k*120:.0f}" r="{3+4*(1-k):.1f}"'
                        f' fill="#b8b2a6" opacity="{.6*(1-k):.2f}"/>')
    s += SL(Z_SRED, par(hx - 100, hy - 350, t, 4, .55, 170, .45, .9))
    lx, ly, lw = 760, 700, 520
    lezh = (f'<rect x="{lx}" y="{ly}" width="{lw}" height="250" rx="14"'
            f' fill="url(#derev)" {o(8)}/>')
    lezh += (f'<rect x="{lx-20}" y="{ly-28}" width="{lw+40}" height="40" rx="12"'
             f' fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_SRED, lezh)
    droz = 5.0 * A.w(t, .33, .1)
    od = f'<g transform="translate({droz:.1f},{abs(droz)*.4:.1f})">'
    od += (f'<path d="M{lx-30:.0f},{ly-10:.0f} q{lw*.5:.0f},-150 {lw+60:.0f},-10'
           f' l0,180 q{-lw*.5:.0f},60 {-lw-60:.0f},0 Z" fill="{TKAN2}" {o(8)}/>')
    for i in range(5):
        od += (f'<path d="M{lx-20+i*(lw/4.5):.0f},{ly-110+((i%2)*26):.0f}'
               f' q30,60 0,150" fill="none" stroke="#5e7ea0" stroke-width="9"'
               f' opacity=".7"/>')
    for i, dx in enumerate((110, 290, 430)):
        gy_ = ly - 128 - (i % 2) * 22
        od += (f'<ellipse cx="{lx+dx:.0f}" cy="{gy_:.0f}" rx="46" ry="50"'
               f' fill="#f0cfae" {o(5)}/>')
        od += (f'<path d="M{lx+dx-46:.0f},{gy_-18:.0f} a46,46 0 0 1 92,0 Z"'
               f' fill="{"#8a5a30" if i else "#4a3526"}" {o(4)}/>')
        for sgn in (-1, 1):
            od += (f'<ellipse cx="{lx+dx+sgn*18:.0f}" cy="{gy_+6:.0f}" rx="7"'
                   f' ry="{3 if A.blink(t, 3.0 + i, i * .2) else 8}" fill="#2b2118"/>')
        od += (f'<ellipse cx="{lx+dx:.0f}" cy="{gy_+30:.0f}" rx="12" ry="7"'
               f' fill="#9c4a3c" opacity=".8"/>')
        od += para_izo_rta(lx + dx + 20, gy_ + 34, t, i * .3, .7, .45)
    od += '</g>'
    s += SL(Z_SRED, od)
    ox, oy, ow, oh = 1340, 220, 500, 390
    moroz = .14 + .40 * A.ease(A.seg(t, .4, 3.2))
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#b9c6cf"/>')
    za += izba_snaruzhi(ox + 40, oy + oh - 20, 420, t, True, True, 421)
    s += SL(Z_SRED, f'<clipPath id="ok41"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok41)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, moroz, False, True))
    for i in range(12):                 # иней растёт лапами по стеклу
        rr = (16 + rnd.uniform(0, 40)) * moroz
        za2 = (f'<path d="M{ox+30+rnd.uniform(0,ow-60):.0f},'
               f'{oy+30+rnd.uniform(0,oh-60):.0f} l{rr:.0f},{-rr*.6:.0f}'
               f' l{-rr*.4:.0f},{rr*1.3:.0f} Z" fill="#ffffff"'
               f' opacity="{.3*moroz:.2f}"/>')
        s += SL(Z_SRED, za2)
    s += SL(Z_SRED, teplo(ox + 240, oy + 240, 300, 220, .22))
    s += SL(Z_SRED, dym(ox + 300, oy + 60, t, 5, .22, 240, .36, "#dfe6ec", .9))
    s += SL(Z_SRED, _vedro(1180, 980, 1.2, t, False, "url(#chug)"))
    s += SL(Z_SRED, kot(1480, 1010, t, .85, "#55504a", True))
    s += ramka_pp("pravo", "#2b2e33", .45)
    s += SL(Z_PERED, _korzina(230, 1080, 220, 170, t, 431, True))
    s += vinetka(.42)
    return s


# ── 42 ─────────────────────────────────────────────────────────────────────
def ten_i_polennica(t):
    """Лохматая тень с жёлтыми глазами крадётся к двери с пустым горшком, но
    хозяйка распахивает дверь — и тень сдувается в пустой тулуп на заборе."""
    rnd = random.Random(4217)
    s = sumerki_fon(t, True)
    s += ulica_dal(1180, 700, 740, t, False, 433)
    s += SL(Z_DAL, gryaz_polosa(790, 180, "#3a332b"))
    izb = brevna(0, 120, 1120, 700, 112)
    izb += (f'<path d="M-40,130 L560,-140 L1160,130 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="820" y="-180" width="100" height="220" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(870, -170, t, 5, .2, 300, .34, "#c8d0da", 1.0))
    raz = A.out(A.seg(t, 3.0, 1.0))
    zat = A.ease(A.seg(t, 6.4, 1.4))
    otk = raz * (1 - zat)
    dx_, dy_, dw, dh = 560, 300, 330, 560
    s += SL(Z_SRED, f'<rect x="{dx_-40}" y="{dy_-40}" width="{dw+80}"'
                    f' height="{dh+40}" rx="10" fill="{DOSKA2}" {o(9)}/>')
    s += SL(Z_SRED, f'<rect x="{dx_}" y="{dy_}" width="{dw}" height="{dh}"'
                    f' fill="#1a0f08"/>')
    s += SL(Z_SRED, teplo(dx_ + dw * .5, dy_ + dh * .6, 360 * otk + 40,
                          320 * otk + 40, .62 * otk))
    s += SL(Z_SRED, lampa(dx_ + dw * .34, dy_ + dh * .5, t, .62 * otk + .18))
    s += SL(Z_SRED, figura(dx_ + dw * .62, dy_ + dh - 6, 470 * (.3 + .7 * otk), t,
                           "#4a2f3a", "#ffd98a", True, .3, True, otk * .9 + .1))
    s += SL(Z_SRED, dver(dx_, dy_, dw, dh, otk * .9, "url(#derev)", True, False))
    s += SL(Z_SRED, podkova(dx_ + dw * .5, dy_ - 70, .95, t))
    s += SL(Z_SRED, f'<path d="M{dx_-60},{dy_+dh} h{dw+120} l-30,70 h{-dw-60} Z"'
                    f' fill="url(#dosk)" {o(8)}/>')
    pw, ph_ = 560, 460
    px, py = 1200, 980
    pol = ten(px + pw * .5, py + 14, pw * .5, 26, .45)
    pol += (f'<rect x="{px-20}" y="{py-ph_-30}" width="{pw+40}" height="30" rx="8"'
            f' fill="{DOSKA2}" {o(6)}/>')
    for r in range(6):
        for c in range(7):
            lx = px + 26 + c * 76 + (r % 2) * 12
            ly = py - 30 - r * 74
            pol += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="36" ry="33"'
                    f' fill="#d8b98a" {o(5)}/>')
            pol += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="22" ry="20"'
                    f' fill="#b08a52" opacity=".7"/>')
            for j in range(3):
                pol += (f'<path d="M{lx:.0f},{ly:.0f} l{math.cos(j*2.1+r)*34:.0f},'
                        f'{math.sin(j*2.1+r)*32:.0f}" stroke="#6b4a26"'
                        f' stroke-width="3" opacity=".7"/>')
    s += SL(Z_SRED, pol)
    schet = int(A.seg(t, 4.2, 2.4) * 6)
    for i in range(schet):
        s += SL(Z_SRED, f'<path d="M{px+40+i*86:.0f},{py-ph_-60:.0f} l16,26 l28,-48"'
                        f' fill="none" stroke="#f4efe2" stroke-width="10"'
                        f' stroke-linecap="round" opacity=".85"/>')
    sd = A.ease(A.seg(t, 3.2, 1.3))
    tx = 1020 - sd * 40
    ty = 1010
    th_ = 520 * (1 - sd * .42)
    tn = f'<g opacity="{1-sd*.55:.2f}">'
    tn += (f'<path d="M{tx-th_*.30:.0f},{ty:.0f} q{-th_*.08:.0f},{-th_*.62:.0f}'
           f' {th_*.10:.0f},{-th_*.80:.0f} q{th_*.22:.0f},{-th_*.20:.0f}'
           f' {th_*.42:.0f},0 q{th_*.18:.0f},{th_*.18:.0f} {th_*.08:.0f},{th_*.80:.0f} Z"'
           f' fill="#171521" {o(6)}/>')
    for i in range(20):                 # лохмы наружу по всему контуру
        a = -3.0 + i * .30
        lr = th_ * (.16 + .07 * abs(A.w(t, 1.2, i * .13)))
        bx_ = tx + math.cos(a) * th_ * .30
        by_ = ty - th_ * .46 + math.sin(a) * th_ * .40
        tn += (f'<path d="M{bx_:.0f},{by_:.0f}'
               f' l{math.cos(a)*lr:.0f},{math.sin(a)*lr:.0f}"'
               f' stroke="#171521" stroke-width="{20-i%4*4}" stroke-linecap="round"/>')
    tn += _glaza(tx, ty - th_ * .72, 17, t, .2, "#f6e39a")
    tn += '</g>'
    s += SL(Z_SRED, tn)
    s += SL(Z_SRED, f'<g opacity="{1-sd:.2f}">'
                    + krynka(tx + 180, ty - 330, 1.5, "#3a3142") + '</g>')
    kach = 4.4 * A.w(t, 2.3, .2)
    tul = f'<g opacity="{sd:.2f}" transform="rotate({kach:.2f} {tx:.0f} {ty-520:.0f})">'
    tul += (f'<path d="M{tx-150:.0f},{ty-520:.0f} q150,-60 300,0 l-40,420'
            f' q-110,40 -220,0 Z" fill="#7a6246" {o(8)}/>')
    tul += (f'<path d="M{tx-150:.0f},{ty-520:.0f} q150,56 300,0 l-18,60'
            f' q-134,46 -264,0 Z" fill="#cdbfa4" {o(5)}/>')
    tul += (f'<path d="M{tx:.0f},{ty-470:.0f} l-16,400" stroke="#5c4a34"'
            f' stroke-width="10" opacity=".8"/>')
    for sgn in (-1, 1):
        tul += (f'<path d="M{tx+sgn*140:.0f},{ty-490:.0f} q{sgn*70:.0f},120'
                f' {sgn*40:.0f},250" fill="none" stroke="#7a6246" stroke-width="54"'
                f' stroke-linecap="round"/>')
    tul += '</g>'
    s += SL(Z_SRED, tul)
    s += SL(Z_PERED, pleten(880, 1080, 1040, 230, 11))
    s += SL(Z_PERED, goloe_derevo(170, 1080, 640, t, 439, 8, "#232630"))
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 443, .5, .9))
    s += vinetka(.48)
    return s


# ── 43 ─────────────────────────────────────────────────────────────────────
def kerosinovaya_lampa_na_polke(t):
    """Пузатая керосиновая лампа на пол-кадра: между банкой крупы и
    будильником её снимают с полки, и в высоком стекле разгорается огонь."""
    rnd = random.Random(4327)
    s = f'<rect width="{W}" height="{H}" fill="#4a3a2c"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 108, True, "dosk"))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#2a1d14" opacity=".38"/>')
    pk = (f'<rect x="120" y="250" width="1680" height="34" rx="8"'
          f' fill="url(#derev)" {o(8)}/>')
    pk += (f'<rect x="120" y="284" width="1680" height="18" fill="{DOSKA2}" {o(5)}/>')
    for i in range(6):
        pk += (f'<path d="M{200+i*300:.0f},302 l30,54 M{420+i*300:.0f},302 l-30,54"'
               f' {o(6)} fill="none"/>')
    for i in range(9):                  # зубчатая подзорная кромка полки
        pk += (f'<path d="M{150+i*190:.0f},302 q46,42 92,0 Z" fill="{DOSKA2}"'
               f' opacity=".9" {o(3)}/>')
    s += SL(Z_DAL, pk)
    s += SL(Z_DAL, _banka(290, 250, 1.35, "url(#solom)", t))
    s += SL(Z_DAL, _banka(1700, 250, 1.1, "#c2a05c", t))
    bud_x, bud_y = 1520, 250
    bud = ten(bud_x, bud_y + 8, 70, 12, .4)
    for sgn in (-1, 1):                 # колокольчики будильника
        bud += (f'<circle cx="{bud_x+sgn*66:.0f}" cy="{bud_y-176:.0f}" r="34"'
                f' fill="url(#zhel)" {o(5)}/>')
        bud += (f'<path d="M{bud_x+sgn*22:.0f},{bud_y-28:.0f} l{sgn*16:.0f},28"'
                f' stroke="{ZHELEZ}" stroke-width="10"/>')
    bud += (f'<circle cx="{bud_x:.0f}" cy="{bud_y-110:.0f}" r="88"'
            f' fill="url(#zhel)" {o(7)}/>')
    bud += (f'<circle cx="{bud_x:.0f}" cy="{bud_y-110:.0f}" r="68"'
            f' fill="url(#krem)" {o(5)}/>')
    tik = 16 * A.w(t, 1.0)
    bud += (f'<line x1="{bud_x:.0f}" y1="{bud_y-110:.0f}"'
            f' x2="{bud_x+54*math.cos(math.radians(tik-60)):.0f}"'
            f' y2="{bud_y-110+54*math.sin(math.radians(tik-60)):.0f}"'
            f' stroke="{K}" stroke-width="7"/>')
    bud += (f'<line x1="{bud_x:.0f}" y1="{bud_y-110:.0f}"'
            f' x2="{bud_x+34*math.cos(math.radians(-tik*3+140)):.0f}"'
            f' y2="{bud_y-110+34*math.sin(math.radians(-tik*3+140)):.0f}"'
            f' stroke="{K}" stroke-width="9"/>')
    for i in range(12):
        a = math.radians(i * 30)
        bud += (f'<circle cx="{bud_x+56*math.cos(a):.0f}"'
                f' cy="{bud_y-110+56*math.sin(a):.0f}" r="4" fill="#6b645c"/>')
    bud += (f'<path d="M{bud_x-52:.0f},{bud_y-176:.0f} q52,-40 104,0" fill="none"'
            f' stroke="{ZHELEZ}" stroke-width="9"/>')
    s += SL(Z_DAL, bud)
    snyat = A.ease(A.seg(t, .6, 1.8))
    lx = 950
    ly = 820 + snyat * 180              # лампу опускают с полки на стол
    s += SL(Z_SRED, stol(600, 1004, 780, 42, False))
    s += SL(Z_SRED, f'<path d="M580,1002 h820 l-34,46 h-752 Z" fill="{RUSH}"'
                    f' opacity=".9" {o(5)}/>')
    ruk, (kx, ky) = rukav(520, 360 + snyat * 150, 230, 26 + 10 * A.w(t, 1.4), t,
                          "#4a2f3a", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="40" ry="28"'
                    f' fill="#4a2f3a" {o(5)}/>')
    lam = ten(lx, ly + 16, 230, 30, .5)
    lam += (f'<path d="M{lx-180:.0f},{ly:.0f} q-30,-110 60,-150 h240'
            f' q90,40 60,150 Z" fill="url(#med)" {o(9)}/>')
    lam += (f'<path d="M{lx-150:.0f},{ly-40:.0f} q150,40 300,0" fill="none"'
            f' stroke="#f2cf8c" stroke-width="10" opacity=".55"/>')
    lam += (f'<rect x="{lx-110:.0f}" y="{ly-212:.0f}" width="220" height="68" rx="14"'
            f' fill="url(#zhel)" {o(8)}/>')
    for i in range(7):
        lam += (f'<line x1="{lx-96+i*32:.0f}" y1="{ly-208:.0f}" x2="{lx-96+i*32:.0f}"'
                f' y2="{ly-150:.0f}" stroke="#4a4f55" stroke-width="6" opacity=".8"/>')
    lam += (f'<circle cx="{lx+150:.0f}" cy="{ly-176:.0f}" r="34" fill="url(#zhel)" {o(6)}/>')
    lam += (f'<circle cx="{lx+150:.0f}" cy="{ly-176:.0f}" r="14" fill="#8a9398" {o(3)}/>')
    s += SL(Z_SRED, lam)
    gx, gy, gw, gh = lx - 210, ly - 790, 420, 580
    put = kontur_proema(gx, gy, gw, gh, "ellips")
    razg = A.ease(A.seg(t, 2.2, 1.6))
    vid = f'<clipPath id="st43"><path d="{put}"/></clipPath>'
    vid += (f'<path d="{put}" fill="#2a1a0c"/>')
    vid += (f'<g clip-path="url(#st43)">'
            + teplo(gx + gw / 2, gy + gh * .62, 300, 320, .5 + .4 * razg)
            + ogon(gx + gw / 2, gy + gh * .86, t, 1.5 + .5 * razg, .1, 7)
            + ugli(gx + gw * .28, gy + gh * .9, gw * .44, t, 5, 449)
            + f'</g>')
    vid += mesto_stoka(gx, gy, gw, gh, "ellips")
    ob = (f'<path d="{put}" fill="url(#stekl)" opacity=".30"/>')
    ob += (f'<path d="{put}" fill="none" stroke="#e8f3ff" stroke-width="12"'
           f' opacity=".75"/>')
    ob += (f'<path d="{put}" fill="none" {o(7)}/>')
    ob += (f'<path d="M{gx+gw*.16:.0f},{gy+gh*.22:.0f} q{-gw*.06:.0f},{gh*.3:.0f}'
           f' {gw*.04:.0f},{gh*.5:.0f}" fill="none" stroke="#ffffff"'
           f' stroke-width="22" opacity="{.22+.12*abs(A.w(t,2.4)):.2f}"/>')
    ob += (f'<ellipse cx="{gx+gw/2:.0f}" cy="{gy+8:.0f}" rx="{gw*.33:.0f}" ry="26"'
           f' fill="none" stroke="#cfe4f5" stroke-width="10" opacity=".8"/>')
    ob += (f'<ellipse cx="{gx+gw/2:.0f}" cy="{gy+gh-6:.0f}" rx="{gw*.46:.0f}" ry="26"'
           f' fill="url(#zhel)" {o(6)}/>')
    s += SL(Z_SRED, vid + ob)
    s += SL(Z_SRED, teplo(lx, ly - 420, 640 * (.5 + .5 * razg),
                          560 * (.5 + .5 * razg), .42 * (.4 + .6 * razg)))
    chirk = A.seg(t, 1.6, .5)
    if chirk > .01 and chirk < .999:
        sx_, sy_ = lx + 330, ly - 330
        s += SL(Z_SRED, f'<line x1="{sx_:.0f}" y1="{sy_:.0f}" x2="{sx_+70:.0f}"'
                        f' y2="{sy_+40:.0f}" stroke="url(#derev)" stroke-width="12"'
                        f' stroke-linecap="round"/>')
        s += SL(Z_SRED, ogon(sx_, sy_ - 10, t, .42, .3, 4))
        s += SL(Z_SRED, iskra_let(t, sx_, sy_ - 20, 8, 457, 180, 1.2))
    s += SL(Z_SRED, f'<rect x="{lx+430}" y="{ly-86:.0f}" width="150" height="70"'
                    f' rx="10" fill="{TKAN}" {o(6)}/>'
                    f'<rect x="{lx+446}" y="{ly-74:.0f}" width="118" height="46"'
                    f' rx="6" fill="#e2c8a0" opacity=".9"/>')
    s += SL(Z_SRED, krynka(400, 998, 1.4))
    s += SL(Z_SRED, karavay(1600, 992, 1.05, True))
    for i, cx_ in enumerate((640, 1200, 1340)):
        s += SL(Z_DAL, f'<ellipse cx="{cx_:.0f}" cy="250" rx="78" ry="18"'
                       f' fill="url(#krem)" {o(5)}/>'
                       f'<path d="M{cx_-56:.0f},232 q8,-94 56,-98 q48,4 56,98'
                       f' q-56,22 -112,0 Z" fill="url(#krem)" {o(7)}/>'
                       f'<path d="M{cx_+56:.0f},170 q54,26 0,50" fill="none"'
                       f' stroke="url(#krem)" stroke-width="14"/>'
                       f'<path d="M{cx_-44:.0f},150 q44,16 88,0" fill="none"'
                       f' stroke="{TKAN}" stroke-width="9" opacity=".8"/>')
    ch_x = 1000
    s += SL(Z_DAL, f'<path d="M{ch_x-96:.0f},250 q-18,-130 96,-140'
                   f' q114,10 96,140 Z" fill="url(#chug)" {o(7)}/>'
                   f'<path d="M{ch_x+92:.0f},170 q60,-8 48,-60" fill="none"'
                   f' stroke="url(#chug)" stroke-width="18" stroke-linecap="round"/>'
                   f'<path d="M{ch_x-50:.0f},112 q50,-56 100,0" fill="none"'
                   f' stroke="{ZHELEZ}" stroke-width="13"/>')
    tb_x = 300
    s += SL(Z_SRED, f'<rect x="{tb_x-130:.0f}" y="880" width="260" height="40"'
                    f' rx="12" fill="url(#derev)" {o(8)}/>'
                    f'<rect x="{tb_x-110:.0f}" y="920" width="40" height="160"'
                    f' rx="12" fill="url(#derev)" {o(6)}/>'
                    f'<rect x="{tb_x+70:.0f}" y="920" width="40" height="160"'
                    f' rx="12" fill="url(#derev)" {o(6)}/>'
                    f'<rect x="{tb_x-100:.0f}" y="1000" width="200" height="20"'
                    f' rx="8" fill="{DOSKA2}" {o(4)}/>')
    puch_x = 1720
    kach2 = 2.6 * A.w(t, 4.0, .2)
    puch = f'<g transform="rotate({kach2:.2f} {puch_x:.0f} 340)">'
    puch += (f'<path d="M{puch_x-30:.0f},340 q30,-24 60,0" fill="none"'
             f' stroke="{TKAN}" stroke-width="12"/>')
    for j in range(6):
        puch += (f'<path d="M{puch_x:.0f},345 q{-22+j*9:.0f},80 {-30+j*12:.0f},150"'
                 f' fill="none" stroke="{["#6f8c4a", "#8a9a58", "#5c7a40"][j%3]}"'
                 f' stroke-width="11" stroke-linecap="round"/>')
        puch += (f'<ellipse cx="{puch_x-30+j*12:.0f}" cy="500" rx="13" ry="7"'
                 f' fill="#8a9a58" opacity=".9"/>')
    puch += '</g>'
    s += SL(Z_SRED, puch)
    s += SL(Z_PERED, zanaveska(60, 0, 520, 200, TKAN, t, 1))
    s += ramka_pp("pravo", "#160f0a", .42)
    s += vinetka(.46)
    return s


# ── 44 ─────────────────────────────────────────────────────────────────────
def svet_pogas_lampa_zazhglas(t):
    """Вечерняя кухня под абажуром: лампочка мигает и гаснет, в темноте
    остаются одни белки глаз, а потом растёт тёплый круг керосинки."""
    rnd = random.Random(4421)
    s = f'<rect width="{W}" height="{H}" fill="#3c3a42"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#6b5f58"/>')
    for i in range(16):                 # обои в полоску
        s += SL(Z_DAL, f'<rect x="{i*120}" y="0" width="56" height="760"'
                       f' fill="#7a6c62" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect x="0" y="740" width="{W}" height="36" fill="#574c45" {o(4)}/>')
    s += kvartira_veschi(1300, 760, 600, t, 463)
    s += SL(Z_SRED, polovicy(860))
    gas = A.ease(A.seg(t, .9, .3))
    mig = (1.0 if ((t * 5.0) % 1.0) > .35 else .3) * (1 - gas)
    zazh = A.ease(A.seg(t, 1.5, .9))
    st = stol(560, 740, 820, 40)
    s += SL(Z_SRED, st)
    s += SL(Z_SRED, f'<path d="M520,738 h900 l-34,46 h-832 Z" fill="{RUSH}"'
                    f' opacity=".9" {o(5)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{620+i*200:.0f},700 q66,80 132,0'
                        f' q-66,26 -132,0 Z" fill="url(#krem)" {o(6)}/>')
        s += SL(Z_SRED, f'<ellipse cx="{686+i*200:.0f}" cy="694" rx="68" ry="18"'
                        f' fill="#d8cbb0" {o(4)}/>')
    s += SL(Z_SRED, karavay(1310, 724, .95, False))
    s += SL(Z_SRED, par(900, 650, t, 4, .4 * (1 - gas) + .2, 160, .45, .8))
    ab_x, ab_y = 960, 250
    s += SL(Z_SRED, f'<line x1="{ab_x}" y1="0" x2="{ab_x}" y2="{ab_y-40}"'
                    f' stroke="#30343a" stroke-width="8"/>')
    s += SL(Z_SRED, f'<path d="M{ab_x-230},{ab_y+70} L{ab_x-96},{ab_y-40}'
                    f' L{ab_x+96},{ab_y-40} L{ab_x+230},{ab_y+70} Z"'
                    f' fill="{TKAN}" {o(8)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{ab_x-210+i*52:.0f},{ab_y+70}'
                        f' q6,40 {-4+4*A.w(t,2.6,i*.2):.1f},76" fill="none"'
                        f' stroke="{ZOL}" stroke-width="7" opacity=".85"/>')
    s += SL(Z_SRED, f'<circle cx="{ab_x}" cy="{ab_y+40}" r="40" fill="{SVET}"'
                    f' opacity="{mig:.2f}"/>')
    s += SL(Z_SRED, teplo(ab_x, ab_y + 220, 700 * mig + 40, 560 * mig + 40, .5 * mig))
    lamp_x, lamp_y = 1180, 736
    s += SL(Z_SRED, f'<g opacity="{.25+.75*zazh:.2f}">'
                    + lampa(lamp_x, lamp_y, t, .95) + '</g>')
    s += SL(Z_SRED, teplo(lamp_x, lamp_y - 160, 760 * zazh + 30,
                          640 * zazh + 30, .55 * zazh))
    ljudi = ((600, 980, 520, "#4a2f3a", True, .1), (1480, 1000, 540, "#3a4150", False, .4),
             (820, 1056, 390, "#5b4a2f", False, .7), (1300, 1060, 370, "#2f4a44", False, .9))
    for i, (fx, fy, fh, col, pl, ph) in enumerate(ljudi):
        vid_op = max(.1, min(1.0, (1 - gas) + zazh))
        s += SL(Z_SRED, figura(fx, fy, fh, t, col, "#ffd98a", pl, ph, i % 2 == 0,
                               vid_op))
        if gas > .4 and zazh < .5:      # в темноте видны только белки глаз
            for sgn in (-1, 1):
                s += SL(Z_SRED, f'<ellipse cx="{fx+sgn*fh*.045:.0f}"'
                                f' cy="{fy-fh*.855:.0f}" rx="{fh*.028:.0f}"'
                                f' ry="{fh*.018 if A.blink(t,3.4,i*.2) else fh*.030:.1f}"'
                                f' fill="#f6f2e6" opacity="{gas*(1-zazh):.2f}"/>')
    hlop = abs(A.w(t, .42, .1))
    for i, (fx, fy) in enumerate(((820, 1056), (1300, 1060))):
        for sgn in (-1, 1):
            ruk, (hx, hy) = rukav(fx + sgn * 70, fy - 250, 110,
                                  -sgn * (36 + 26 * hlop) - (0 if sgn > 0 else 180),
                                  t, "#5b4a2f" if i == 0 else "#2f4a44",
                                  "#ffd98a", i * .3, 3.0)
            s += SL(Z_SRED, ruk)
            s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="22" ry="17"'
                            f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, f'<rect width="{W}" height="{H}" fill="#0b0d14"'
                    f' opacity="{.66*gas*(1-zazh*.95):.2f}"/>')
    s += ramka_pp("levo", "#0e0c12", .5)
    s += SL(Z_PERED, kot(300, 1070, t, .9, "#49413a"))
    s += vinetka(.5)
    return s


# ── 45 ─────────────────────────────────────────────────────────────────────
def zapas_sveta_na_polke(t):
    """Полка в прихожей на пол-кадра: по одной встают свечи, коробок спичек,
    фонарик и сложенный плед, а в окнах напротив разом гаснет свет."""
    rnd = random.Random(4523)
    s = f'<rect width="{W}" height="{H}" fill="#55616b"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#6d7a84"/>')
    for i in range(13):
        s += SL(Z_DAL, f'<rect x="{i*150}" y="0" width="70" height="1080"'
                       f' fill="#7e8b95" opacity=".45"/>')
    s += SL(Z_DAL, f'<rect x="0" y="880" width="{W}" height="200" fill="#4e5a62" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="866" width="{W}" height="26" fill="#8e9aa2" {o(4)}/>')
    ves = (f'<rect x="80" y="250" width="420" height="30" rx="8" fill="url(#derev)" {o(7)}/>')
    for i in range(4):
        ves += (f'<circle cx="{150+i*110:.0f}" cy="300" r="16" fill="{ZHELEZ}" {o(4)}/>')
        ves += (f'<path d="M{150+i*110:.0f},316 q{-10+6*A.w(t,4.0,i*.2):.1f},120'
                f' {-30+10*A.w(t,4.0,i*.2):.1f},300" fill="none"'
                f' stroke="{[TKAN, TKAN2, "#5b5a4a", "#7a4a3a"][i]}" stroke-width="64"'
                f' stroke-linecap="round" opacity=".92"/>')
    s += SL(Z_DAL, ves)
    pw, px, py = 1120, 700, 620
    pk = (f'<rect x="{px}" y="{py}" width="{pw}" height="44" rx="10"'
          f' fill="url(#derev)" {o(9)}/>')
    pk += (f'<rect x="{px}" y="{py+44}" width="{pw}" height="22" fill="{DOSKA2}" {o(5)}/>')
    for i in range(3):
        pk += (f'<path d="M{px+120+i*420:.0f},{py+66} l40,70 M{px+320+i*420:.0f},'
               f'{py+66} l-40,70" {o(7)} fill="none"/>')
    pk += (f'<rect x="{px}" y="{py-430}" width="{pw}" height="30" rx="8"'
           f' fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, pk)
    for i in range(5):                  # вещи на верхней полке — не пусто
        pk2 = (f'<rect x="{px+60+i*210:.0f}" y="{py-540:.0f}" width="130"'
               f' height="110" rx="10" fill="{["#6b5a3c", TKAN2, "#4a5a4a", MED, "#5b4450"][i]}"'
               f' {o(5)}/>')
        s += SL(Z_SRED, pk2)
    stavit = [A.over(A.seg(t, .3 + i * .36, .5)) for i in range(4)]
    for i in range(3):                  # свечи
        k = stavit[0]
        cx_ = px + 120 + i * 90
        s += SL(Z_SRED, f'<g opacity="{min(1, k):.2f}" transform="translate(0,'
                        f'{(1-k)*-180:.0f})">'
                        + svecha(cx_, py - 150 - i % 2 * 20, t, i * .3, 1.5, 150)
                        + '</g>')
    s += SL(Z_SRED, teplo(px + 200, py - 240, 460, 400, .4 + .12 * abs(A.w(t, 1.4))))
    k = stavit[1]                       # коробок спичек
    kx_ = px + 440
    s += SL(Z_SRED, f'<g opacity="{min(1, k):.2f}" transform="translate(0,'
                    f'{(1-k)*-200:.0f})">'
                    f'<rect x="{kx_:.0f}" y="{py-130:.0f}" width="190" height="130"'
                    f' rx="10" fill="{TKAN}" {o(7)}/>'
                    f'<rect x="{kx_+16:.0f}" y="{py-110:.0f}" width="158" height="60"'
                    f' rx="6" fill="#e8d6b2" {o(4)}/>'
                    f'<rect x="{kx_:.0f}" y="{py-40:.0f}" width="190" height="40"'
                    f' fill="#5e4a3a" opacity=".85"/></g>')
    k = stavit[2]                       # фонарик
    fx_ = px + 700
    s += SL(Z_SRED, f'<g opacity="{min(1, k):.2f}" transform="translate(0,'
                    f'{(1-k)*-220:.0f})">'
                    f'<rect x="{fx_:.0f}" y="{py-96:.0f}" width="230" height="96"'
                    f' rx="22" fill="#2f3a44" {o(7)}/>'
                    f'<path d="M{fx_+220:.0f},{py-120:.0f} h70 l16,120 h-86 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<ellipse cx="{fx_+300:.0f}" cy="{py-60:.0f}" rx="16" ry="60"'
                    f' fill="url(#stekl)" opacity=".9" {o(4)}/>'
                    f'<rect x="{fx_+40:.0f}" y="{py-72:.0f}" width="60" height="30"'
                    f' rx="8" fill="{KRAS}" {o(4)}/></g>')
    k = stavit[3]                       # плед
    gx_ = px + 940
    spol = 26 * A.ease(A.seg(t, 3.0, 1.2))
    s += SL(Z_SRED, f'<g opacity="{min(1, k):.2f}" transform="translate(0,'
                    f'{(1-k)*-240+spol:.0f})">'
                    f'<rect x="{gx_:.0f}" y="{py-170:.0f}" width="210" height="170"'
                    f' rx="14" fill="{TKAN2}" {o(8)}/>'
                    + "".join(f'<rect x="{gx_:.0f}" y="{py-150+j*44:.0f}" width="210"'
                              f' height="18" fill="#e8d6b2" opacity=".65"/>'
                              for j in range(3))
                    + f'<path d="M{gx_:.0f},{py-170:.0f} q105,30 210,0" fill="none"'
                    f' stroke="#1d2a38" stroke-width="7"/></g>')
    ox, oy, ow, oh = 110, 420, 460, 380
    gas = A.ease(A.seg(t, 2.2, .5))
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#141b28"/>')
    for r in range(4):
        for c in range(4):
            on = ((r + c) % 2 == 0) and gas < .5
            za += (f'<rect x="{ox+40+c*100:.0f}" y="{oy+40+r*86:.0f}" width="68"'
                   f' height="58" rx="5" fill="{SVET if on else "#2b3648"}"'
                   f' opacity="{.45+.45*abs(A.w(t,6+c,r*.2)) if on else .5:.2f}"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.8:.0f}" width="{ow}" height="{oh*.2:.0f}"'
           f' fill="#1b2430"/>')
    s += SL(Z_SRED, f'<clipPath id="ok45"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok45)">{za}</g>')
    ram = (f'<rect x="{ox-26}" y="{oy-26}" width="{ow+52}" height="{oh+52}" rx="8"'
           f' fill="none" stroke="#dfe6ea" stroke-width="54"/>')
    ram += (f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}" y2="{oy+oh}"'
            f' stroke="#dfe6ea" stroke-width="20"/>')
    ram += (f'<rect x="{ox-40}" y="{oy+oh+26}" width="{ow+80}" height="30" rx="8"'
            f' fill="#cfd8dc" {o(5)}/>')
    s += SL(Z_SRED, ram)
    vz = A.ease(A.seg(t, 3.2, 1.0))
    ruk, (hx, hy) = rukav(1870, 760, 300, 196 - 14 * vz, t, "#3a4150", "#cfe4f5", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="34" ry="24"'
                    f' fill="#3a4150" {o(5)}/>')
    kov = (f'<rect x="120" y="940" width="760" height="140" rx="16"'
           f' fill="#7a3a42" {o(7)}/>')
    for i in range(6):
        kov += (f'<rect x="{150+i*120:.0f}" y="960" width="90" height="100" rx="8"'
                f' fill="#9c4a52" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, kov)
    for i, (bx_, col) in enumerate(((190, "#4a3f36"), (380, "#5b4450"),
                                    (560, "#2f3a44"), (740, "#6b5a3c"))):
        s += SL(Z_SRED, f'<path d="M{bx_-70:.0f},{980+((i%2)*26):.0f}'
                        f' q12,-56 76,-56 q70,0 76,48 q-6,30 -76,30'
                        f' q-64,0 -76,-22 Z" fill="{col}" {o(6)}/>'
                        f'<path d="M{bx_-54:.0f},{956+((i%2)*26):.0f} q58,-30 110,4"'
                        f' fill="none" stroke="#cfd6dc" stroke-width="9" opacity=".6"/>')
    zr_x, zr_y = 1700, 560
    s += SL(Z_SRED, f'<rect x="{zr_x-130:.0f}" y="{zr_y-250:.0f}" width="260"'
                    f' height="500" rx="18" fill="#cfd6dc" {o(8)}/>'
                    f'<rect x="{zr_x-104:.0f}" y="{zr_y-224:.0f}" width="208"'
                    f' height="448" rx="12" fill="#9fb6c6" {o(5)}/>'
                    f'<path d="M{zr_x-80:.0f},{zr_y-180:.0f} l120,180"'
                    f' stroke="#ffffff" stroke-width="18" opacity=".3"/>')
    s += SL(Z_SRED, f'<g opacity=".55">'
                    + svecha(zr_x - 20, zr_y + 120, t, .4, 1.1, 110) + '</g>')
    for i in range(4):                  # крючки с ключами
        s += SL(Z_SRED, f'<circle cx="{1380+i*70:.0f}" cy="330" r="12"'
                        f' fill="{ZHELEZ}" {o(4)}/>'
                        f'<path d="M{1380+i*70:.0f},342 q{-6+4*A.w(t,3.4,i*.2):.1f},36'
                        f' {2:.0f},70" fill="none" stroke="url(#zhel)"'
                        f' stroke-width="7"/>'
                        f'<circle cx="{1382+i*70:.0f}" cy="{418:.0f}" r="14"'
                        f' fill="none" stroke="{MED}" stroke-width="7"/>')
    s += SL(Z_SRED, f'<path d="M1240,360 q-16,260 -30,420" fill="none"'
                    f' stroke="#2f4a7a" stroke-width="54" stroke-linecap="round"/>'
                    f'<path d="M1240,360 q40,-60 90,-10" fill="none"'
                    f' stroke="#2f3a44" stroke-width="14" stroke-linecap="round"/>')
    s += SL(Z_SRED, kot(980, 1050, t, .85, "#3b3430"))
    s += ramka_pp("pravo", "#141a20", .42)
    s += vinetka(.44)
    return s


# ── 46 ─────────────────────────────────────────────────────────────────────
def rastopka_u_pechki(t):
    """Пол у печной дверцы: в плетёную корзину на пол-кадра ложатся смолистые
    щепки, свёрнутая береста и скрученная газета, топорик колет лучину."""
    rnd = random.Random(4639)
    s = f'<rect width="{W}" height="{H}" fill="#2f241a"/>'
    s += SL(Z_DAL, brevna(0, 0, 720, 820, 104))
    s += SL(Z_DAL, f'<rect x="700" y="0" width="1220" height="900" fill="url(#pech)"'
                   f' opacity=".97"/>')
    s += SL(Z_DAL, kladka(700, 0, 1220, 360, 90, "url(#pech)"))
    s += utvar_izby(60, 240, 420, t, 467)
    s += SL(Z_SRED, polovicy(880))
    dvx, dvy, dvw, dvh = 1360, 420, 380, 330
    dvr = (f'<rect x="{dvx-34}" y="{dvy-34}" width="{dvw+68}" height="{dvh+68}"'
           f' rx="12" fill="{CHUGUN}" {o(9)}/>')
    dvr += (f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}" rx="8"'
            f' fill="#160c06"/>')
    s += SL(Z_SRED, dvr)
    s += SL(Z_SRED, ugli(dvx + 40, dvy + dvh - 50, dvw - 80, t, 8, 479)
                    + ogon(dvx + dvw * .5, dvy + dvh - 36, t, 1.25, .2, 7))
    s += SL(Z_SRED, iskra_let(t, dvx + dvw * .5, dvy + dvh - 90, 9, 487, 280, .5))
    s += SL(Z_SRED, teplo(dvx + dvw * .5, dvy + dvh * .7, 560, 460,
                          .46 + .14 * abs(A.w(t, 1.3))))
    dvr2 = (f'<path d="M{dvx+dvw+34:.0f},{dvy+dvh*.5:.0f} h56" stroke="url(#zhel)"'
            f' stroke-width="16" stroke-linecap="round"/>')
    dvr2 += (f'<circle cx="{dvx+dvw+96:.0f}" cy="{dvy+dvh*.5:.0f}" r="22"'
             f' fill="url(#zhel)" {o(5)}/>')
    for i in range(4):
        dvr2 += (f'<circle cx="{dvx-20+i*(dvw/3):.0f}" cy="{dvy-20}" r="11"'
                 f' fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, dvr2)
    kx, ky = 820, 1000
    s += SL(Z_SRED, _korzina(kx, ky, 620, 440, t, 491, False))
    for i in range(11):                 # щепки сыплются в корзину
        p = A.ease(A.seg(t, .3 + i * .13, .7))
        sx_ = kx - 230 + i * 46
        sy_ = 300 + p * (ky - 420 - 300) + (1 - p) * -60
        ug = -40 + i * 16 + (1 - p) * 120
        s += SL(Z_SRED, f'<g transform="rotate({ug:.0f} {sx_:.0f} {sy_:.0f})">'
                        f'<rect x="{sx_-12:.0f}" y="{sy_-70:.0f}" width="24"'
                        f' height="140" rx="7" fill="url(#derev)" {o(4)}/>'
                        f'<rect x="{sx_-6:.0f}" y="{sy_-60:.0f}" width="7"'
                        f' height="118" fill="#c49a5c" opacity=".8"/></g>')
    ber = A.ease(A.seg(t, 2.2, 1.4))
    bx_, by_ = kx + 150, ky - 500
    s += SL(Z_SRED, f'<g transform="rotate({-18+28*ber:.1f} {bx_:.0f} {by_:.0f})">'
                    f'<path d="M{bx_-130:.0f},{by_:.0f} q130,{-60-60*ber:.0f} 260,0'
                    f' q-130,{70+40*ber:.0f} -260,0 Z" fill="#efe8dc" {o(6)}/>'
                    + "".join(f'<path d="M{bx_-100+j*52:.0f},{by_-30:.0f} l0,46"'
                              f' stroke="#2f2a26" stroke-width="8"'
                              f' stroke-linecap="round" opacity=".8"/>' for j in range(4))
                    + f'<path d="M{bx_-130:.0f},{by_:.0f} q130,{40+30*ber:.0f} 260,0"'
                    f' fill="none" stroke="#b9ab97" stroke-width="6"/></g>')
    s += SL(Z_SRED, _gazeta(kx - 330, ky - 560, 250, 180, -24 + 10 * A.w(t, 2.0), 499))
    skr = A.ease(A.seg(t, 3.4, 1.6))
    s += SL(Z_SRED, f'<g transform="rotate({40*skr:.0f} {kx-130:.0f} {ky-330:.0f})">'
                    f'<path d="M{kx-190:.0f},{ky-330:.0f} q60,{-40+20*skr:.0f}'
                    f' 120,0 l-14,{150-40*skr:.0f} q-46,20 -92,0 Z"'
                    f' fill="url(#list)" {o(6)}/>'
                    + "".join(f'<path d="M{kx-176+j*30:.0f},{ky-300:.0f} l-6,100"'
                              f' stroke="#9c948a" stroke-width="5"/>' for j in range(4))
                    + '</g>')
    tp_a = -62 + 58 * abs(A.w(t, .8, .1))
    tx_, ty_ = 380, 900
    s += SL(Z_SRED, f'<rect x="{tx_-180:.0f}" y="{ty_-30:.0f}" width="420"'
                    f' height="56" rx="12" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<g transform="rotate({tp_a:.0f} {tx_:.0f} {ty_-180:.0f})">'
                    f'<rect x="{tx_-20:.0f}" y="{ty_-430:.0f}" width="40" height="300"'
                    f' rx="12" fill="url(#derev)" {o(6)}/>'
                    f'<path d="M{tx_-24:.0f},{ty_-470:.0f} q120,-40 150,30'
                    f' l-34,110 q-60,-34 -116,-26 Z" fill="url(#zhel)" {o(7)}/>'
                    f'<path d="M{tx_+96:.0f},{ty_-440:.0f} q34,60 10,120"'
                    f' fill="none" stroke="#eef4f8" stroke-width="12" opacity=".6"/></g>')
    for i in range(6):                  # лучинки разлетаются
        p = ((t * .8) + i * .16) % 1.0
        s += SL(Z_SRED, f'<rect x="{tx_+60+p*180:.0f}" y="{ty_-90-p*120+p*p*180:.0f}"'
                        f' width="14" height="70" rx="5" fill="#c49a5c"'
                        f' opacity="{1-p*.7:.2f}" transform="rotate({p*160:.0f}'
                        f' {tx_+66+p*180:.0f} {ty_-60-p*120:.0f})" {o(3)}/>')
    s += SL(Z_SRED, kot(1620, 1040, t, 1.05, "#8a7a68"))
    s += SL(Z_SRED, par(1620, 980, t, 3, .3, 110, .5, .6))
    s += ramka_pp("levo", "#160e08", .46)
    s += SL(Z_PERED, krynka(1830, 1070, 1.5))
    s += vinetka(.46)
    return s


# ── 47 ─────────────────────────────────────────────────────────────────────
def fonarik_v_yaschike_komoda(t):
    """Корзина со щепками оборачивается выдвинутым ящиком комода: среди
    катушек и квитанций лежит большой фонарик, и луч вспыхивает в пыли."""
    rnd = random.Random(4703)
    s = f'<rect width="{W}" height="{H}" fill="#2a2630"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#3e3a46"/>')
    for i in range(12):
        s += SL(Z_DAL, f'<rect x="{i*170}" y="0" width="76" height="1080"'
                       f' fill="#474350" opacity=".6"/>')
    s += kvartira_veschi(60, 820, 520, t, 503)
    s += SL(Z_SRED, polovicy(900))
    km_x, km_y, km_w = 620, 940, 1120
    km = ten(km_x + km_w / 2, km_y + 16, km_w * .5, 24, .5)
    km += (f'<rect x="{km_x}" y="{km_y-700}" width="{km_w}" height="700" rx="14"'
           f' fill="url(#derev)" {o(9)}/>')
    km += (f'<rect x="{km_x-24}" y="{km_y-740}" width="{km_w+48}" height="46" rx="12"'
           f' fill="{DOSKA2}" {o(7)}/>')
    for r in range(2):
        km += (f'<rect x="{km_x+40}" y="{km_y-660+r*180:.0f}" width="{km_w-80}"'
               f' height="150" rx="10" fill="{DOSKA2}" {o(6)}/>')
        for c in (-1, 1):
            km += (f'<circle cx="{km_x+km_w/2+c*180:.0f}" cy="{km_y-585+r*180:.0f}"'
                   f' r="20" fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, km)
    prev = A.ease(A.seg(t, .2, .8))
    yx, yy, yw, yh = 560, 920, 1240, 430
    ya = (f'<path d="M{yx:.0f},{yy-yh:.0f} h{yw:.0f} l-50,{yh:.0f} h{-yw+100:.0f} Z"'
          f' fill="#6b4a2c" {o(9)}/>')
    ya += (f'<rect x="{yx-30:.0f}" y="{yy-yh-54:.0f}" width="{yw+60:.0f}" height="64"'
           f' rx="14" fill="url(#derev)" {o(9)}/>')
    ya += (f'<rect x="{yx+40:.0f}" y="{yy-yh-40:.0f}" width="{yw-80:.0f}" height="36"'
           f' rx="10" fill="{DOSKA2}" opacity=".8"/>')
    for c in (-1, 1):
        ya += (f'<circle cx="{yx+yw/2+c*260:.0f}" cy="{yy-yh-22:.0f}" r="22"'
               f' fill="url(#zhel)" {o(5)}/>')
    ya += (f'<path d="M{yx+30:.0f},{yy-yh+20:.0f} h{yw-60:.0f} l-40,{yh-50:.0f}'
           f' h{-yw+140:.0f} Z" fill="#3a2a1c" {o(5)}/>')
    s += SL(Z_SRED, ya)
    kor_op = 1 - prev
    if kor_op > .02:
        s += SL(Z_SRED, f'<g opacity="{kor_op:.2f}">'
                        + _korzina(yx + yw / 2, yy, 860, 420, t, 509, False) + '</g>')
    for i in range(9):                  # катушки ниток в ящике
        cx_ = yx + 110 + i * 86
        cy_ = yy - 110 - (i % 3) * 36
        col = ["#8f3a42", "#3a5a8f", "#4a7a4a", "#8a6a2a", "#6b4a6a"][i % 5]
        s += SL(Z_SRED, f'<g opacity="{prev:.2f}">'
                        f'<rect x="{cx_-24:.0f}" y="{cy_-44:.0f}" width="48"'
                        f' height="88" rx="8" fill="{col}" {o(4)}/>'
                        f'<ellipse cx="{cx_:.0f}" cy="{cy_-44:.0f}" rx="30" ry="10"'
                        f' fill="url(#derev)" {o(3)}/>'
                        f'<ellipse cx="{cx_:.0f}" cy="{cy_+44:.0f}" rx="30" ry="10"'
                        f' fill="url(#derev)" {o(3)}/></g>')
    for i in range(4):                  # квитанции
        s += SL(Z_SRED, f'<g opacity="{prev:.2f}">'
                        + _gazeta(yx + 190 + i * 150, yy - 250 - (i % 2) * 40, 190, 120,
                                  -22 + i * 13, 521) + '</g>')
    fx_, fy_ = yx + 820, yy - 180
    vsp = 1.0 if ((t * 1.3) % 1.0) > .42 else .25
    fon = (f'<g opacity="{prev:.2f}">'
           f'<rect x="{fx_-200:.0f}" y="{fy_-74:.0f}" width="400" height="148"'
           f' rx="34" fill="#2f3a44" {o(9)}/>')
    for i in range(7):
        fon += (f'<rect x="{fx_-170+i*46:.0f}" y="{fy_-70:.0f}" width="20"'
                f' height="140" rx="8" fill="#243038" opacity=".9"/>')
    fon += (f'<path d="M{fx_+190:.0f},{fy_-108:.0f} h96 l26,216 h-122 Z"'
            f' fill="{ZHELEZ}" {o(8)}/>')
    fon += (f'<ellipse cx="{fx_+312:.0f}" cy="{fy_+2:.0f}" rx="26" ry="108"'
            f' fill="url(#stekl)" opacity=".92" {o(6)}/>')
    fon += (f'<ellipse cx="{fx_+312:.0f}" cy="{fy_+2:.0f}" rx="18" ry="86"'
            f' fill="{SVET}" opacity="{vsp:.2f}"/>')
    fon += (f'<rect x="{fx_-120:.0f}" y="{fy_-100:.0f}" width="90" height="40"'
            f' rx="10" fill="{KRAS}" {o(5)}/>')
    fon += '</g>'
    s += SL(Z_SRED, fon)
    s += SL(Z_SRED, f'<g opacity="{prev*vsp:.2f}">'
                    + luch(fx_ + 330, fy_ - 120, 300, 560, t, .30) + '</g>')
    s += SL(Z_SRED, teplo(fx_ + 380, fy_ + 60, 420 * vsp, 340 * vsp, .4 * prev * vsp))
    for i in range(18):                 # пылинки пляшут в луче
        p = ((t * .22) + i * .055) % 1.0
        s += SL(Z_SRED, f'<circle cx="{fx_+340+p*420+40*A.w(t,3.4+i*.2,i*.1):.0f}"'
                        f' cy="{fy_-80+p*420+30*A.w(t,2.6,i*.13):.0f}"'
                        f' r="{2.4+2.6*(1-p):.1f}" fill="#fff6dd"'
                        f' opacity="{prev*vsp*(1-p)*.9:.2f}"/>')
    vz = A.ease(A.seg(t, 1.4, 1.1))
    ruk, (hx, hy) = rukav(fx_ - 260, 300 + vz * 120, 190, 74, t, "#3a4150",
                          "#cfe4f5", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="38" ry="26"'
                    f' fill="#3a4150" {o(5)}/>')
    s += SL(Z_SRED, svecha(1780, 180, t, .2, 1.7, 150))
    s += SL(Z_SRED, teplo(1800, 150, 460, 420, .4 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, hodiki(300, 300, t, 1.15))
    for i in range(3):                  # тени отпрыгивают в углы
        s += SL(Z_SRED, f'<ellipse cx="{200+i*760:.0f}" cy="{1000:.0f}"'
                        f' rx="{200+80*vsp:.0f}" ry="{70+20*vsp:.0f}" fill="#13111a"'
                        f' opacity="{.5-.22*vsp:.2f}"/>')
    s += ramka_pp("oba", "#120f16", .5)
    s += vinetka(.5)
    return s


# ── 48 ─────────────────────────────────────────────────────────────────────
def odeyalo_i_noski_nagotove(t):
    """Стул у кровати на пол-кадра: на него ложится толстое стёганое одеяло,
    сверху падают шерстяные носки с узором, запрыгивает кот."""
    rnd = random.Random(4801)
    s = f'<rect width="{W}" height="{H}" fill="#3a3640"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#55505e"/>')
    for i in range(10):
        s += SL(Z_DAL, f'<path d="M{80+i*200},0 q30,540 0,1080" fill="none"'
                       f' stroke="#5f5a6c" stroke-width="40" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect x="0" y="930" width="{W}" height="150" fill="#4a4550" {o(5)}/>')
    krv = (f'<rect x="1180" y="430" width="760" height="70" rx="16"'
           f' fill="url(#derev)" {o(9)}/>')
    krv += (f'<rect x="1180" y="500" width="40" height="440" rx="12"'
            f' fill="url(#derev)" {o(7)}/>')
    krv += (f'<rect x="1230" y="660" width="720" height="250" rx="18"'
            f' fill="{TKAN2}" {o(8)}/>')
    krv += (f'<path d="M1250,680 q180,-120 400,-40 l0,60 q-200,-60 -400,40 Z"'
            f' fill="#eef2f6" {o(6)}/>')
    for i in range(5):
        krv += (f'<path d="M{1280+i*140:.0f},760 q60,40 0,120" fill="none"'
                f' stroke="#5e7ea0" stroke-width="10" opacity=".7"/>')
    for i in range(4):
        krv += (f'<rect x="{1230+i*230:.0f}" y="900" width="36" height="140" rx="10"'
                f' fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, krv)
    tb = (f'<rect x="940" y="700" width="230" height="300" rx="12"'
          f' fill="url(#derev)" {o(8)}/>')
    tb += (f'<rect x="920" y="676" width="270" height="36" rx="10" fill="{DOSKA2}" {o(6)}/>')
    tb += (f'<rect x="962" y="760" width="186" height="80" rx="8" fill="{DOSKA2}" {o(5)}/>')
    tb += (f'<circle cx="1055" cy="800" r="14" fill="url(#zhel)" {o(4)}/>')
    s += SL(Z_SRED, tb)
    s += SL(Z_SRED, svecha(1000, 540, t, .1, 1.5, 140))
    s += SL(Z_SRED, teplo(1010, 520, 540, 480, .44 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, f'<path d="M1110,676 q40,-96 76,0 q-38,22 -76,0 Z"'
                    f' fill="url(#stekl)" opacity=".9" {o(5)}/>')
    sx, sy = 540, 980
    st = ten(sx, sy + 14, 180, 24, .5)
    st += (f'<rect x="{sx-170:.0f}" y="{sy-560:.0f}" width="54" height="560" rx="12"'
           f' fill="url(#derev)" {o(8)}/>')
    st += (f'<rect x="{sx+116:.0f}" y="{sy-560:.0f}" width="54" height="560" rx="12"'
           f' fill="url(#derev)" {o(8)}/>')
    for i in range(3):
        st += (f'<rect x="{sx-170:.0f}" y="{sy-540+i*86:.0f}" width="340" height="40"'
               f' rx="12" fill="{DOSKA2}" {o(6)}/>')
    st += (f'<rect x="{sx-200:.0f}" y="{sy-300:.0f}" width="400" height="60" rx="14"'
           f' fill="url(#derev)" {o(9)}/>')
    for dx in (-180, 160):
        st += (f'<rect x="{sx+dx:.0f}" y="{sy-240:.0f}" width="40" height="240"'
               f' rx="10" fill="url(#derev)" {o(7)}/>')
    st += (f'<rect x="{sx-160:.0f}" y="{sy-130:.0f}" width="320" height="26"'
           f' rx="8" fill="{DOSKA2}" {o(5)}/>')
    s += SL(Z_SRED, st)
    lozh = A.out(A.seg(t, .3, 1.2))
    oy_ = sy - 300 - (1 - lozh) * 420
    od = f'<g transform="translate(0,{oy_-(sy-300):.0f})">'
    od += (f'<path d="M{sx-230:.0f},{sy-300:.0f} q{230:.0f},-110 {460:.0f},0'
           f' q{-20:.0f},160 {-40:.0f},260 q{-200:.0f},70 {-400:.0f},0 Z"'
           f' fill="{TKAN}" {o(9)}/>')
    for r in range(3):
        for c in range(5):
            od += (f'<rect x="{sx-200+c*84:.0f}" y="{sy-310+r*76:.0f}" width="70"'
                   f' height="62" rx="14" fill="#c2574e" opacity=".85"'
                   f' stroke="#7a1c22" stroke-width="5"/>')
    od += (f'<path d="M{sx-230:.0f},{sy-40:.0f} q230,60 460,0" fill="none"'
           f' stroke="#efe3c8" stroke-width="12" opacity=".7"/>')
    od += '</g>'
    s += SL(Z_SRED, od)
    for i in range(2):                  # носки падают сверху
        pd = A.out(A.seg(t, 1.5 + i * .3, .9))
        nx = sx - 70 + i * 150
        ny = -160 + pd * (sy - 400)
        ug = -30 + 70 * pd + 10 * A.w(t, 1.2, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({ug:.0f} {nx:.0f} {ny:.0f})">'
                        f'<path d="M{nx-50:.0f},{ny-110:.0f} h100 l0,120'
                        f' q0,60 -60,70 q-80,10 -90,-40 q-6,-40 50,-50 Z"'
                        f' fill="#e8dcc0" {o(7)}/>'
                        + "".join(f'<path d="M{nx-50:.0f},{ny-80+j*34:.0f} h100"'
                                  f' stroke="{[TKAN, ZEL2, TKAN2][j%3]}"'
                                  f' stroke-width="11" opacity=".9"/>' for j in range(3))
                        + f'<path d="M{nx-50:.0f},{ny-110:.0f} h100" stroke="#b9a884"'
                        f' stroke-width="10"/></g>')
    pryg = A.out(A.seg(t, 3.0, .9))
    s += SL(Z_SRED, kot(sx + 230, sy - pryg * 300, t, 1.0 - .15 * pryg, "#3b3430"))
    lucha = -26 + 52 * A.w(t, 2.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({lucha:.0f} 120 980)" opacity=".5">'
                    + luch(120, 420, 240, 560, t, .26) + '</g>')
    s += SL(Z_SRED, f'<rect x="60" y="900" width="260" height="110" rx="26"'
                    f' fill="#2f3a44" {o(7)}/>'
                    f'<ellipse cx="330" cy="950" rx="24" ry="56" fill="{SVET}"'
                    f' opacity="{.5+.4*abs(A.w(t,1.8)):.2f}" {o(4)}/>')
    s += SL(Z_SRED, _vedro(1740, 1060, .9, t, False, "#6b5a4a"))
    kov = (f'<rect x="300" y="1000" width="760" height="80" rx="14"'
           f' fill="#5b3a44" {o(7)}/>')
    for i in range(7):
        kov += (f'<rect x="{330+i*104:.0f}" y="1014" width="76" height="60" rx="8"'
                f' fill="#7a4a56" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, kov)
    for i, sgn in enumerate((-1, 1)):   # валенки под стулом
        vx_ = sx + sgn * 90
        s += SL(Z_SRED, f'<path d="M{vx_-46:.0f},{sy+70:.0f} l0,-150'
                        f' q46,-24 92,0 l0,150 q-46,22 -92,0 Z" fill="#9c9282" {o(6)}/>'
                        f'<path d="M{vx_-46:.0f},{sy+40:.0f} q46,26 92,0"'
                        f' fill="none" stroke="#7a7266" stroke-width="8"/>')
    km = (f'<rect x="60" y="560" width="420" height="440" rx="14"'
          f' fill="url(#derev)" {o(9)}/>')
    km += (f'<rect x="44" y="530" width="452" height="40" rx="12" fill="{DOSKA2}" {o(6)}/>')
    for r in range(3):
        km += (f'<rect x="90" y="{600+r*140:.0f}" width="360" height="118" rx="10"'
               f' fill="{DOSKA2}" {o(5)}/>')
        for c in (-1, 1):
            km += (f'<circle cx="{270+c*110:.0f}" cy="{659+r*140:.0f}" r="16"'
                   f' fill="url(#zhel)" {o(4)}/>')
    s += SL(Z_SRED, km)
    s += SL(Z_SRED, hodiki(270, 380, t, 1.0))
    s += ramka_pp("levo", "#141019", .45)
    s += vinetka(.48)
    return s


# ── 49 ─────────────────────────────────────────────────────────────────────
def porog_svoe_i_chuzhoe(t):
    """Порог избы сбоку: решето и платок замирают над светящейся чертой
    порога — хозяйка забирает решето, гостья прижимает платок к груди."""
    rnd = random.Random(4903)
    s = f'<rect width="{W}" height="{H}" fill="#241a12"/>'
    s += nebo("sumer", t, False, 541)
    s += SL(Z_DAL, f'<rect x="0" y="0" width="900" height="1080" fill="#2a1f16"/>')
    s += SL(Z_DAL, brevna(0, 0, 900, 1080, 108))
    s += ulica_dal(980, 700, 900, t, False, 547)
    s += SL(Z_DAL, gryaz_polosa(760, 170, "#3c332a"))
    kos = (f'<rect x="860" y="0" width="120" height="900" rx="14"'
           f' fill="url(#derev)" {o(10)}/>')
    kos += (f'<rect x="860" y="0" width="1060" height="130" rx="14"'
            f' fill="{DOSKA2}" {o(10)}/>')
    for i in range(7):
        kos += (f'<path d="M{1000+i*120:.0f},20 q28,40 0,84" fill="none"'
                f' stroke="#5a3a22" stroke-width="8" opacity=".7"/>')
    s += SL(Z_SRED, kos)
    por = (f'<path d="M820,800 h1100 l0,120 h-1100 Z" fill="url(#dosk)" {o(10)}/>')
    por += (f'<path d="M820,780 h1100 l0,30 h-1100 Z" fill="{DOSKA2}" {o(7)}/>')
    por += (f'<path d="M820,920 h1100 l0,60 h-1100 Z" fill="#5a3a22" {o(8)}/>')
    for i in range(8):
        por += (f'<path d="M{880+i*130:.0f},812 q24,54 0,100" fill="none"'
                f' stroke="#6b4a2a" stroke-width="9" opacity=".6"/>')
    s += SL(Z_SRED, por)
    s += SL(Z_SRED, polovicy(980))
    sv = .5 + .4 * abs(A.w(t, 1.3))
    cher = (f'<path d="M840,790 q270,-16 540,-4 q270,12 540,-6" fill="none"'
            f' stroke="{SVET}" stroke-width="54" opacity="{sv*.4:.2f}"/>')
    cher += (f'<path d="M840,790 q270,-16 540,-4 q270,12 540,-6" fill="none"'
             f' stroke="#ffffff" stroke-width="22" opacity="{sv:.2f}"'
             f' stroke-linecap="round"/>')
    for i in range(12):
        cher += (f'<circle cx="{880+i*92:.0f}" cy="{786+((i%3)-1)*5}"'
                 f' r="{6+5*abs(A.w(t,1.5,i*.12)):.1f}" fill="#fff6dd"'
                 f' opacity="{.45+.45*abs(A.w(t,1.2,i*.1)):.2f}"/>')
    s += SL(Z_SRED, cher)
    s += SL(Z_SRED, teplo(1380, 790, 620, 180, .32 * sv))
    svetec = (f'<rect x="946" y="640" width="36" height="300" rx="10"'
              f' fill="url(#derev)" {o(6)}/>'
              f'<path d="M906,660 q58,-40 116,0 l-14,46 q-44,-24 -88,0 Z"'
              f' fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, svetec)
    s += SL(Z_SRED, luchina(964, 640, t, 1.9, .2))
    s += SL(Z_SRED, teplo(950, 500, 520, 460, .42 + .12 * abs(A.w(t, 1.4))))
    zab = A.ease(A.seg(t, 1.6, 1.1))
    hx = 700
    s += SL(Z_SRED, figura(hx, 980, 620, t, "#5b2f3a", "#ffd98a", True, .2, True))
    ruk, (rx2, ry2) = rukav(hx + 150, 640, 230 - 40 * zab, 16 - 26 * zab, t,
                            "#5b2f3a", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    sit_x, sit_y = rx2 + 70, ry2 + 20
    sit = (f'<path d="M{sit_x-132:.0f},{sit_y-40:.0f} q132,-70 264,0 l-14,96'
           f' q-118,66 -236,0 Z" fill="url(#solom)" {o(8)}/>')
    sit += (f'<ellipse cx="{sit_x:.0f}" cy="{sit_y-40:.0f}" rx="132" ry="56"'
            f' fill="#c9a877" {o(6)}/>')
    sit += (f'<ellipse cx="{sit_x:.0f}" cy="{sit_y-40:.0f}" rx="112" ry="44"'
            f' fill="#9c7a42" opacity=".7"/>')
    for i in range(9):                  # сетка решета по эллипсу
        kx_ = -112 + i * 28
        hr = (1 - (kx_ / 118.0) ** 2) ** .5 * 44
        sit += (f'<line x1="{sit_x+kx_:.0f}" y1="{sit_y-40-hr:.0f}"'
                f' x2="{sit_x+kx_:.0f}" y2="{sit_y-40+hr:.0f}" stroke="#8a6534"'
                f' stroke-width="5" opacity=".85"/>')
        sit += (f'<path d="M{sit_x-112:.0f},{sit_y-62+i*11:.0f}'
                f' q112,{22-i*4:.0f} 224,0" fill="none" stroke="#8a6534"'
                f' stroke-width="4" opacity=".75"/>')
    s += SL(Z_SRED, sit)
    prizh = A.ease(A.seg(t, 2.0, 1.2))
    gx = 1600
    s += SL(Z_SRED, figura(gx, 990, 580, t, "#36415a", "#cfe4f5", True, .6, True,
                           1.0, True))
    s += SL(Z_SRED, para_izo_rta(gx - 40, 520, t, .3, 1.1, .5))
    ruk2, (px2, py2) = rukav(gx - 140, 660, 200 - 70 * prizh, 196 + 24 * prizh, t,
                             "#36415a", "#cfe4f5", .4, 4.0)
    s += SL(Z_SRED, ruk2)
    kach = 7 * A.w(t, 1.7, .1) * (1 - prizh)
    pl = f'<g transform="rotate({kach:.1f} {px2:.0f} {py2:.0f})">'
    pl += (f'<path d="M{px2-140:.0f},{py2-40:.0f} q140,-60 280,0'
           f' q-20,120 -60,180 q-80,70 -160,0 q-40,-60 -60,-180 Z"'
           f' fill="{TKAN}" {o(8)}/>')
    pl += (f'<path d="M{px2-140:.0f},{py2-40:.0f} q140,56 280,0" fill="none"'
           f' stroke="#f2e2c8" stroke-width="12" opacity=".7"/>')
    for i in range(4):
        pl += (f'<path d="M{px2-100+i*62:.0f},{py2-10:.0f} q20,110 -10,210"'
               f' fill="none" stroke="#f2e2c8" stroke-width="7" opacity=".6"/>')
    for i in range(7):
        pl += (f'<path d="M{px2-110+i*38:.0f},{py2+218:.0f} l{-6+i*2},46"'
               f' stroke="{TKAN}" stroke-width="7" stroke-linecap="round"/>')
    pl += '</g>'
    s += SL(Z_SRED, pl)
    s += SL(Z_SRED, krynka(1030, 1060, 1.3))
    s += SL(Z_SRED, kura(1820, 940, t, .9, .4))
    s += ramka_pp("levo", "#160f0a", .5)
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 557, .38, .8))
    s += vinetka(.46)
    return s


# ── 50 ─────────────────────────────────────────────────────────────────────
def hozyain_zaslonyaet_svoe_dobro(t):
    """Широкоплечий хозяин в дверях сарая раскинул руки, а за его спиной
    жмётся друг к другу утварь с испуганными глазками."""
    rnd = random.Random(5003)
    s = sumerki_fon(t, True)
    s += ulica_dal(40, 720, 700, t, False, 563)
    s += SL(Z_DAL, gryaz_polosa(800, 180, "#443a30"))
    sar = doski(420, 120, 1180, 780, 84, True, "dosk")
    sar += (f'<path d="M380,130 L1010,-150 L1640,130 Z" fill="#6b5436" {o(9)}/>')
    sar += (f'<path d="M380,136 L1010,-144 L1640,136 L1580,106 L1010,-100 L440,106 Z"'
            f' fill="url(#sneg)" opacity=".7" {o(4)}/>')
    s += SL(Z_DAL, sar)
    s += SL(Z_DAL, dym(300, 320, t, 4, .2, 260, .3, "#c8d0da", .9))
    dvx, dvy, dvw, dvh = 700, 300, 640, 640
    s += SL(Z_SRED, f'<rect x="{dvx-40}" y="{dvy-40}" width="{dvw+80}"'
                    f' height="{dvh+40}" rx="12" fill="{DOSKA2}" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="#1b140d"/>')
    s += SL(Z_SRED, teplo(dvx + dvw * .5, dvy + dvh * .62, 520, 460, .55))
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="{ORA}" opacity=".16"/>')
    utv = []
    # ухват
    ux_ = dvx + 110
    utv.append(f'<rect x="{ux_-14:.0f}" y="{dvy+180}" width="28" height="430" rx="10"'
               f' fill="url(#derev)" {o(6)}/>'
               f'<path d="M{ux_-60:.0f},{dvy+200} q60,-90 120,0" fill="none"'
               f' stroke="{ZHELEZ}" stroke-width="22"/>' + _glaza(ux_, dvy + 300, 15, t, .1))
    # коромысло
    kx_ = dvx + 250
    utv.append(f'<path d="M{kx_-120:.0f},{dvy+260} q120,-90 240,0" fill="none"'
               f' stroke="url(#derev)" stroke-width="34" stroke-linecap="round"/>'
               + _glaza(kx_, dvy + 236, 14, t, .4))
    # кадушка
    kdx = dvx + 430
    utv.append(f'<path d="M{kdx-110:.0f},{dvy+620} l14,-260 q96,-34 192,0 l14,260 Z"'
               f' fill="url(#derev)" {o(7)}/>'
               f'<path d="M{kdx-104:.0f},{dvy+440} q104,26 208,0" fill="none"'
               f' stroke="{ZHELEZ}" stroke-width="13"/>'
               + _glaza(kdx, dvy + 420, 18, t, .7))
    # топор прячется за кадушку
    pryat = A.ease(A.seg(t, 1.4, 1.0))
    tpx = dvx + 560 - pryat * 120
    utv.append(f'<g opacity="{1-pryat*.55:.2f}">'
               f'<rect x="{tpx-12:.0f}" y="{dvy+330}" width="26" height="280" rx="9"'
               f' fill="url(#derev)" {o(5)}/>'
               f'<path d="M{tpx-16:.0f},{dvy+310} q86,-30 108,22 l-24,78'
               f' q-44,-26 -84,-20 Z" fill="url(#zhel)" {o(6)}/>'
               + _glaza(tpx + 30, dvy + 300, 13, t, .2) + '</g>')
    # корыто
    krx = dvx + 160
    utv.append(f'<path d="M{krx-150:.0f},{dvy+600} q150,80 300,0 q-20,80 -150,88'
               f' q-130,-8 -150,-88 Z" fill="url(#derev)" {o(7)}/>'
               + _glaza(krx, dvy + 620, 16, t, .9))
    for u in utv:
        s += SL(Z_SRED, u)
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="none" {o(10)}/>')
    mot = 5.0 * A.w(t, 1.5, .1)
    hx, hy = dvx + dvw * .5, 1010
    s += SL(Z_SRED, f'<g transform="rotate({mot:.1f} {hx:.0f} {hy-300:.0f})">'
                    + figura(hx, hy, 660, t, "#4a3a2c", "#ffd98a", False, .2, False,
                             1.0, True, 0.0, True) + '</g>')
    for sgn in (-1, 1):
        ruk, (ax, ay) = rukav(hx + sgn * 120, hy - 460, 280,
                              (0 if sgn > 0 else 180) + sgn * (6 + 5 * A.w(t, 1.3, .2)),
                              t, "#4a3a2c", "#ffd98a", .2 + (0 if sgn > 0 else .4), 3.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="34" ry="26"'
                        f' fill="#4a3a2c" {o(5)}/>')
    s += SL(Z_SRED, para_izo_rta(hx + 60, hy - 540, t, .1, 1.2, .5))
    fnx, fny = dvx - 120, 420
    s += SL(Z_SRED, f'<rect x="{fnx-16:.0f}" y="120" width="32" height="760"'
                    f' fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M{fnx-70:.0f},{fny:.0f} h140 l-16,-36 h-108 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-58:.0f},{fny:.0f} h116 l-12,130 h-92 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 116, t, .62, .3, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 80, 340, 300, .44 + .12 * abs(A.w(t, 1.6))))
    sos_x = 1700
    s += SL(Z_SRED, figura(sos_x, 1040, 470, t, "#3c4656", "#cfe4f5", False, .7,
                           True, 1.0, True, 1.4, False, True))
    ches = -70 + 16 * A.w(t, 1.1, .3)
    ruk3, (cx3, cy3) = rukav(sos_x - 60, 700, 150, ches, t, "#3c4656", "#cfe4f5", .3, 6.0)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, f'<ellipse cx="{cx3:.0f}" cy="{cy3:.0f}" rx="26" ry="20"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_PERED, pleten(-60, 1080, 420, 200, 6))
    s += SL(Z_PERED, _korzina(1860, 1080, 240, 190, t, 569, False))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 571, .44, .9))
    s += vinetka(.46)
    return s


# ── 51 ─────────────────────────────────────────────────────────────────────
def dostatok_uhodit_verenicey(t):
    """Ворота амбара: сосед уносит отданное решето, а следом на тонких ножках
    уходят мешок муки, окорок, кадка с капустой и крынка масла."""
    rnd = random.Random(5101)
    s = sumerki_fon(t, True)
    s += ulica_dal(1240, 700, 700, t, False, 577)
    s += SL(Z_DAL, gryaz_polosa(790, 190, "#473c30"))
    amb = doski(120, 60, 1180, 820, 92, True, "dosk")
    amb += (f'<path d="M80,70 L710,-180 L1340,70 Z" fill="#6b5436" {o(9)}/>')
    amb += (f'<rect x="640" y="-120" width="140" height="120" rx="8"'
            f' fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_DAL, amb)
    vx, vy, vw, vh = 330, 260, 760, 640
    s += SL(Z_SRED, f'<rect x="{vx-40}" y="{vy-40}" width="{vw+80}" height="{vh+40}"'
                    f' rx="12" fill="{DOSKA2}" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}"'
                    f' fill="#140e09"/>')
    pust = A.ease(A.seg(t, .6, 2.4))
    for i in range(5):                  # опустевшие полки амбара
        s += SL(Z_SRED, f'<rect x="{vx+40}" y="{vy+90+i*110:.0f}" width="{vw-80}"'
                        f' height="18" rx="6" fill="#3a2a1c" {o(4)}/>')
        if i % 2 == 0:
            s += SL(Z_SRED, f'<g opacity="{1-pust:.2f}">'
                            + krynka(vx + 150 + i * 90, vy + 86 + i * 110, .8) + '</g>')
    s += SL(Z_SRED, teplo(vx + vw * .5, vy + vh * .7, 380, 320, .24))
    for sgn, px in ((-1, vx), (1, vx + vw)):
        s += SL(Z_SRED, f'<g transform="rotate({sgn*18:.0f} {px:.0f} {vy:.0f})">'
                        f'<rect x="{px-(170 if sgn<0 else 0):.0f}" y="{vy}" width="170"'
                        f' height="{vh}" fill="url(#dosk)" {o(8)}/>'
                        f'<path d="M{px-(160 if sgn<0 else -10):.0f},{vy+60}'
                        f' l150,{vh-160:.0f}" stroke="#5a3a22" stroke-width="14"/></g>')
    gor = ((0, 320, "#d8c8a4"), (1, 300, "#b06a4a"), (2, 300, "#9a7238"), (3, 250, "#c98c55"))
    for i, (k, hh, col) in enumerate(gor):
        hod = A.ease(A.seg(t, .2 + i * .26, 2.8))
        gx = vx + 120 + i * 250 + hod * 480
        gy = 1000 - i * 26
        sh = 8 * A.w(t, .8, i * .3)
        g = f'<g transform="translate({sh:.1f},{-abs(sh)*.6:.1f})">'
        if k == 0:                      # мешок муки
            g += (f'<path d="M{gx-110:.0f},{gy-60:.0f} q-20,-230 110,-260'
                  f' q130,30 110,260 q-110,50 -220,0 Z" fill="{col}" {o(8)}/>')
            g += (f'<path d="M{gx-54:.0f},{gy-330:.0f} q54,-56 108,0'
                  f' q-54,30 -108,0 Z" fill="#c2b08a" {o(5)}/>')
            g += (f'<path d="M{gx-60:.0f},{gy-326:.0f} q60,-26 120,0" fill="none"'
                  f' stroke="{TKAN}" stroke-width="16"/>')
            mah = 16 * A.w(t, .9, .2)
            g += (f'<path d="M{gx+100:.0f},{gy-250:.0f} q{60+mah:.0f},-40 90,10'
                  f' q-60,30 -90,20 Z" fill="{col}" {o(5)}/>')
            g += _glaza(gx, gy - 220, 17, t, .1, "#2b2118")
        elif k == 1:                    # окорок
            g += (f'<path d="M{gx-120:.0f},{gy-120:.0f} q-30,-180 120,-180'
                  f' q150,0 110,190 q-110,60 -230,-10 Z" fill="{col}" {o(8)}/>')
            g += (f'<path d="M{gx+90:.0f},{gy-290:.0f} q50,-40 40,-80" fill="none"'
                  f' stroke="#e8dcc6" stroke-width="20" stroke-linecap="round"/>')
            g += (f'<path d="M{gx-110:.0f},{gy-180:.0f} q120,40 230,0" fill="none"'
                  f' stroke="#8a4a32" stroke-width="10" opacity=".8"/>')
            g += _glaza(gx, gy - 230, 15, t, .5, "#f0e4cc")
        elif k == 2:                    # кадка с капустой
            g += (f'<path d="M{gx-110:.0f},{gy-60:.0f} l16,-230 q94,-36 188,0'
                  f' l16,230 Z" fill="url(#derev)" {o(8)}/>')
            for j in range(2):
                g += (f'<path d="M{gx-104+j*8:.0f},{gy-120-j*90:.0f} q{104-j*8:.0f},26'
                      f' {208-j*16:.0f},0" fill="none" stroke="{ZHELEZ}"'
                      f' stroke-width="12"/>')
            g += (f'<ellipse cx="{gx:.0f}" cy="{gy-290:.0f}" rx="96" ry="26"'
                  f' fill="#b9c98a" {o(5)}/>')
            g += _glaza(gx, gy - 200, 16, t, .8)
        else:                           # крынка масла
            g += krynka(gx, gy - 40, 2.0, "url(#krem)")
            g += _glaza(gx, gy - 160, 14, t, .3, "#2b2118")
        g += _nozhki(gx, gy - 60, 130, t, i * .3, "#4a3a28", 66)
        g += '</g>'
        s += SL(Z_SRED, g)
    sos = A.ease(A.seg(t, .2, 2.4))
    sx = 1180 + sos * 480
    s += SL(Z_SRED, figura(sx, 1020, 520, t, "#3c4656", "#cfe4f5", False, .5,
                           True, 1.0, True, 1.2, True, True))
    ruk, (rx2, ry2) = rukav(sx - 110, 700, 180, 176, t, "#3c4656", "#cfe4f5", .3, 4.0)
    s += SL(Z_SRED, ruk)
    sit = (f'<ellipse cx="{rx2-60:.0f}" cy="{ry2+20:.0f}" rx="120" ry="104"'
           f' fill="url(#solom)" {o(8)}/>')
    sit += (f'<ellipse cx="{rx2-60:.0f}" cy="{ry2+20:.0f}" rx="94" ry="80"'
            f' fill="#c9a877" {o(5)}/>')
    for i in range(7):
        sit += (f'<line x1="{rx2-150+i*26:.0f}" y1="{ry2-56:.0f}"'
                f' x2="{rx2-150+i*26:.0f}" y2="{ry2+96:.0f}" stroke="#8a6534"'
                f' stroke-width="5" opacity=".75"/>')
    s += SL(Z_SRED, sit)
    s += SL(Z_SRED, para_izo_rta(sx + 46, 640, t, .2, 1.1, .5))
    fnx, fny = 1300, 380
    s += SL(Z_SRED, f'<rect x="{fnx-16:.0f}" y="100" width="32" height="700"'
                    f' fill="url(#derev)" {o(7)}/>'
                    f'<path d="M{fnx-64:.0f},{fny:.0f} h128 l-14,-34 h-100 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-54:.0f},{fny:.0f} h108 l-12,124 h-84 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 112, t, .58, .2, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 70, 330, 290, .42 + .12 * abs(A.w(t, 1.5))))
    gor_p = ((t * .35) % 1.0)           # горошина катится по земле
    s += SL(Z_SRED, f'<circle cx="{vx+vw*.5+gor_p*900:.0f}"'
                    f' cy="{1052-abs(math.sin(gor_p*14))*22:.0f}" r="17"'
                    f' fill="{ZEL2}" {o(4)}/>')
    s += SL(Z_PERED, pleten(1300, 1080, 620, 210, 7))
    s += SL(Z_PERED, goloe_derevo(140, 1080, 560, t, 587, 7, "#2a2b33"))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 593, .44, .9))
    s += vinetka(.46)
    return s


# ── 52 ─────────────────────────────────────────────────────────────────────
def chuzhoy_gorshok_s_neudachami(t):
    """Чужой расписной горшок на пол-кадра: крышка приподнимается, и из него
    выбираются три взъерошенных бесёнка-неудачи."""
    rnd = random.Random(5209)
    s = f'<rect width="{W}" height="{H}" fill="#2b2118"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 760, 104))
    s += utvar_izby(1340, 260, 520, t, 599)
    s += SL(Z_SRED, polovicy(900))
    s += SL(Z_SRED, pech(-140, 160, 480, 700, t, True, True, False))
    s += SL(Z_SRED, teplo(120, 620, 520, 420, .34 + .1 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, iskra_let(t, 120, 560, 7, 601, 280, .4))
    s += SL(Z_SRED, stol(520, 760, 960, 44))
    s += SL(Z_SRED, f'<path d="M500,758 h1000 l-40,54 h-920 Z" fill="{RUSH}"'
                    f' opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, svecha(1420, 620, t, .2, 1.6, 140))
    s += SL(Z_SRED, teplo(1430, 590, 520, 460, .42 + .12 * abs(A.w(t, 1.3))))
    gx, gy = 880, 756
    gor = ten(gx, gy + 10, 210, 26, .5)
    gor += (f'<path d="M{gx-190:.0f},{gy-110:.0f} q-60,-210 50,-330'
            f' q140,-56 280,0 q110,120 50,330 Z" fill="url(#glina)" {o(9)}/>')
    gor += (f'<path d="M{gx-190:.0f},{gy-110:.0f} q190,56 380,0 l-8,110'
            f' q-182,46 -364,0 Z" fill="#b06a3c" {o(7)}/>')
    for i in range(3):                  # роспись: пояски и ягоды
        yy = gy - 200 - i * 86
        gor += (f'<path d="M{gx-184+i*6:.0f},{yy:.0f} q{184-i*6:.0f},40'
                f' {368-i*12:.0f},0" fill="none" stroke="{KREM}" stroke-width="12"'
                f' opacity=".9"/>')
        for j in range(6):
            gor += (f'<circle cx="{gx-150+j*60:.0f}" cy="{yy-30:.0f}" r="13"'
                    f' fill="{[KRAS, ZEL2, ZOL][j%3]}" {o(3)}/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-452:.0f}" rx="200" ry="50"'
            f' fill="#8e5a2c" {o(8)}/>')
    gor += (f'<ellipse cx="{gx:.0f}" cy="{gy-452:.0f}" rx="172" ry="38"'
            f' fill="#1d0f06"/>')
    s += SL(Z_SRED, gor)
    pod = A.out(A.seg(t, .3, .8))
    kry_y = gy - 470 - pod * 150
    kach = 9 * A.w(t, 1.6, .2) * pod
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {gx:.0f} {kry_y:.0f})">'
                    f'<ellipse cx="{gx:.0f}" cy="{kry_y:.0f}" rx="206" ry="50"'
                    f' fill="url(#glina)" {o(8)}/>'
                    f'<ellipse cx="{gx:.0f}" cy="{kry_y-28:.0f}" rx="140" ry="34"'
                    f' fill="#b06a3c" {o(5)}/>'
                    f'<ellipse cx="{gx:.0f}" cy="{kry_y-58:.0f}" rx="40" ry="24"'
                    f' fill="#8e5a2c" {o(6)}/></g>')
    for i in range(3):                  # бесенята вылезают
        lez = A.out(A.seg(t, .8 + i * .34, 1.1))
        bx = gx - 130 + i * 130
        by = gy - 420 - lez * (60 + i * 16)
        bh = 120
        b = f'<g transform="translate({10*A.w(t,.9,i*.3):.1f},0)">'
        b += (f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{bh*.44:.0f}"'
              f' ry="{bh*.50:.0f}" fill="#2f2436" {o(6)}/>')
        for j in range(9):              # взъерошенная шерсть
            a = -3.0 + j * .38
            b += (f'<path d="M{bx+math.cos(a)*bh*.40:.0f},'
                  f'{by+math.sin(a)*bh*.44:.0f} l{math.cos(a)*22:.0f},'
                  f'{math.sin(a)*22:.0f}" stroke="#2f2436" stroke-width="12"'
                  f' stroke-linecap="round"/>')
        for sgn in (-1, 1):             # рожки
            b += (f'<path d="M{bx+sgn*30:.0f},{by-bh*.44:.0f} l{sgn*14:.0f},-38'
                  f' l{-sgn*26:.0f},12 Z" fill="#6b4a2a" {o(4)}/>')
        b += _glaza(bx, by - 10, 14, t, i * .3, "#f6e39a")
        b += (f'<path d="M{bx-20:.0f},{by+34:.0f} q20,22 40,0" fill="none"'
              f' stroke="#f6e39a" stroke-width="7" stroke-linecap="round"/>')
        b += (f'<path d="M{bx+bh*.42:.0f},{by+20:.0f} q50,20 30,70" fill="none"'
              f' stroke="#2f2436" stroke-width="12" stroke-linecap="round"/>')
        b += '</g>'
        s += SL(Z_SRED, b)
    let = A.ease(A.seg(t, 1.6, 1.0))
    chx = 1300 + let * 240
    chy = 700 + let * 320 - math.sin(let * 3.14) * 200
    s += SL(Z_SRED, f'<g transform="rotate({let*300:.0f} {chx:.0f} {chy:.0f})">'
                    f'<path d="M{chx-60:.0f},{chy-50:.0f} q60,90 120,0'
                    f' q-60,26 -120,0 Z" fill="url(#krem)" {o(6)}/>'
                    f'<ellipse cx="{chx:.0f}" cy="{chy-54:.0f}" rx="62" ry="18"'
                    f' fill="#d8cbb0" {o(4)}/>'
                    f'<path d="M{chx+58:.0f},{chy-44:.0f} q40,20 0,46" fill="none"'
                    f' stroke="url(#krem)" stroke-width="11"/></g>')
    for i in range(6):                  # брызги из чашки
        p = ((t * .9) + i * .16) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{chx-60+p*120:.0f}" cy="{chy+p*p*160:.0f}"'
                        f' rx="{10*(1-p)+3:.1f}" ry="{16*(1-p)+4:.1f}"'
                        f' fill="#c9b78a" opacity="{1-p:.2f}"/>')
    rv = A.ease(A.seg(t, 2.2, .7))
    s += SL(Z_SRED, f'<path d="M300,420 q120,{60+40*rv:.0f} {200-80*rv:.0f},'
                    f'{120+60*rv:.0f}" fill="none" stroke="{KREM}" stroke-width="7"/>'
                    f'<path d="M{560+60*rv:.0f},{600+40*rv:.0f} q60,40 120,20"'
                    f' fill="none" stroke="{KREM}" stroke-width="7"/>')
    nes = A.ease(A.seg(t, 2.6, 1.2))
    hx = 420 + nes * -260
    s += SL(Z_SRED, figura(hx, 1070, 560, t, "#5b2f3a", "#ffd98a", True, .4, True))
    s += SL(Z_SRED, kot(1700, 1060, t, .9, "#3b3430", True))
    s += ramka_pp("pravo", "#160f0a", .46)
    s += SL(Z_PERED, krynka(220, 1070, 1.4))
    s += vinetka(.46)
    return s


# ── 53 ─────────────────────────────────────────────────────────────────────
def stena_s_instrumentom(t):
    """Стена сарая во весь кадр: на гвоздях пила, топор, коса, грабли и хомут,
    под каждым обведён углём контур — пилу снимают, контур пустеет."""
    rnd = random.Random(5303)
    s = f'<rect width="{W}" height="{H}" fill="#5c452c"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 96, True, "dosk"))
    for i in range(21):                 # гвозди и сучки по доскам
        s += SL(Z_DAL, f'<ellipse cx="{40+i*92:.0f}" cy="{120+(i%5)*190:.0f}"'
                       f' rx="11" ry="8" fill="#6b4a2a" opacity=".7"/>')
    s += SL(Z_DAL, f'<rect x="0" y="940" width="{W}" height="140" fill="#4a3a26" {o(6)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="928" width="{W}" height="24" fill="#6b5436" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="0" y="40" width="{W}" height="40" fill="#4a3a26" {o(5)}/>')
    snyat = A.ease(A.seg(t, 2.6, 1.6))
    # контуры углём: что где висит
    kont = ""
    konturi = ((300, 420, 330, 150), (720, 360, 150, 330), (1130, 330, 420, 420),
               (1600, 380, 230, 420), (430, 820, 300, 180))
    for (cx_, cy_, cw, ch) in konturi:
        kont += (f'<rect x="{cx_-cw/2:.0f}" y="{cy_-ch/2:.0f}" width="{cw}"'
                 f' height="{ch}" rx="24" fill="none" stroke="#2f2418"'
                 f' stroke-width="9" stroke-dasharray="22 16" opacity=".75"/>')
    s += SL(Z_SRED, kont)
    # пила — её снимают
    px_, py_ = 300, 420
    pila = f'<g opacity="{1-snyat:.2f}" transform="translate({snyat*-260:.0f},{snyat*-80:.0f})">'
    pila += (f'<path d="M{px_-160:.0f},{py_-40:.0f} h300 l-20,70 h-280 Z"'
             f' fill="url(#zhel)" {o(7)}/>')
    for i in range(14):
        pila += (f'<path d="M{px_-156+i*22:.0f},{py_+30:.0f} l11,26 l11,-26 Z"'
                 f' fill="url(#zhel)" {o(3)}/>')
    pila += (f'<path d="M{px_+142:.0f},{py_-50:.0f} q60,-10 60,40 q0,46 -56,40'
             f' l-10,-80 Z" fill="url(#derev)" {o(6)}/>')
    pila += (f'<path d="M{px_-150:.0f},{py_-30:.0f} h280" stroke="#eef4f8"'
             f' stroke-width="8" opacity="{.3+.3*abs(A.w(t,2.2)):.2f}"/>')
    pila += '</g>'
    s += SL(Z_SRED, pila)
    s += SL(Z_SRED, f'<circle cx="{px_-150:.0f}" cy="{py_-62:.0f}" r="13"'
                    f' fill="{ZHELEZ}" {o(4)}/>')
    # топор
    tx_, ty_ = 720, 360
    s += SL(Z_SRED, f'<rect x="{tx_-18:.0f}" y="{ty_-120:.0f}" width="36" height="300"'
                    f' rx="12" fill="url(#derev)" {o(7)}/>'
                    f'<path d="M{tx_-24:.0f},{ty_-150:.0f} q120,-44 150,30 l-32,104'
                    f' q-58,-32 -116,-24 Z" fill="url(#zhel)" {o(8)}/>'
                    f'<path d="M{tx_+96:.0f},{ty_-120:.0f} q30,56 10,116" fill="none"'
                    f' stroke="#eef4f8" stroke-width="12" opacity=".55"/>')
    # коса
    kx_, ky_ = 1130, 330
    s += SL(Z_SRED, f'<path d="M{kx_-160:.0f},{ky_-180:.0f} q40,240 160,380"'
                    f' fill="none" stroke="url(#derev)" stroke-width="34"'
                    f' stroke-linecap="round"/>'
                    f'<path d="M{kx_-150:.0f},{ky_-170:.0f} q230,30 310,250'
                    f' q-170,-150 -320,-190 Z" fill="url(#zhel)" {o(8)}/>'
                    f'<path d="M{kx_-140:.0f},{ky_-150:.0f} q210,40 280,230"'
                    f' fill="none" stroke="#eef4f8" stroke-width="9"'
                    f' opacity="{.35+.3*abs(A.w(t,2.6,.2)):.2f}"/>'
                    f'<rect x="{kx_-40:.0f}" y="{ky_+110:.0f}" width="60"'
                    f' height="30" rx="10" fill="{ZHELEZ}" {o(4)}/>')
    # грабли
    gx_, gy_ = 1600, 380
    grab = (f'<rect x="{gx_-16:.0f}" y="{gy_-170:.0f}" width="32" height="400"'
            f' rx="11" fill="url(#derev)" {o(7)}/>')
    grab += (f'<rect x="{gx_-130:.0f}" y="{gy_-220:.0f}" width="260" height="34"'
             f' rx="12" fill="url(#derev)" {o(6)}/>')
    for i in range(7):
        grab += (f'<rect x="{gx_-120+i*38:.0f}" y="{gy_-186:.0f}" width="16"'
                 f' height="74" rx="7" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, grab)
    # хомут
    hx_, hy_ = 430, 820
    hom = (f'<path d="M{hx_-140:.0f},{hy_:.0f} q-30,-150 140,-160 q170,10 140,160'
           f' q-30,110 -140,110 q-110,0 -140,-110 Z" fill="#6b4a2a" {o(9)}/>')
    hom += (f'<path d="M{hx_-80:.0f},{hy_-10:.0f} q-16,-100 80,-104 q96,4 80,104'
            f' q-16,70 -80,70 q-64,0 -80,-70 Z" fill="#2f2418" {o(6)}/>')
    for i in range(6):
        hom += (f'<circle cx="{hx_-120+i*48:.0f}" cy="{hy_-120+((i%2)*16):.0f}"'
                f' r="10" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, hom)
    ox, oy, ow, oh = 1180, 740, 420, 300
    vesna = A.ease(A.seg(t, 4.4, 2.0))
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}"'
          f' fill="{"#b9d0e2" if vesna < .5 else "#9ec8a0"}"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.62:.0f}" width="{ow}" height="{oh*.38:.0f}"'
           f' fill="{"#e8f1fa" if vesna < .5 else "#6f8c4a"}"/>')
    for i in range(4):
        za += (f'<path d="M{ox+50+i*100:.0f},{oy+oh*.64:.0f} l-30,0 l30,-80 l30,80 Z"'
               f' fill="{"#8aa0b4" if vesna < .5 else "#4a6a34"}"/>')
        if vesna > .5:
            za += (f'<circle cx="{ox+50+i*100:.0f}" cy="{oy+oh*.42:.0f}" r="34"'
                   f' fill="#7a9a46" opacity=".9"/>')
    s += SL(Z_SRED, f'<clipPath id="ok53"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok53)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .1, False, True))
    fnx, fny = 240, 180
    s += SL(Z_SRED, f'<path d="M{fnx-20:.0f},{fny-100:.0f} q20,-40 40,0" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="9"/>'
                    f'<path d="M{fnx-78:.0f},{fny:.0f} h156 l-18,-38 h-120 Z"'
                    f' fill="{ZHELEZ}" {o(7)}/>'
                    f'<path d="M{fnx-66:.0f},{fny:.0f} h132 l-14,170 h-104 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(7)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 196, t, .72, .2, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 150, 440, 400, .44 + .12 * abs(A.w(t, 1.5))))
    ruk, (rx2, ry2) = rukav(-80, 470, 170 + snyat * 90, -16 - snyat * 14, t,
                            "#4a3a2c", "#ffd98a", .2, 3.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{rx2:.0f}" cy="{ry2:.0f}" rx="40" ry="28"'
                    f' fill="#4a3a2c" {o(5)}/>')
    ches = A.ease(A.seg(t, 4.0, 1.4))
    sx_ = 1820
    s += SL(Z_SRED, figura(sx_, 1060, 470, t, "#3c4656", "#ffd98a", False, .6,
                           True, 1.0, False, 1.2, True))
    ruk3, (cx3, cy3) = rukav(sx_ - 60, 760, 140, -64 - 20 * ches, t, "#3c4656",
                             "#ffd98a", .3, 6.0)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, f'<ellipse cx="{cx3:.0f}" cy="{cy3:.0f}" rx="26" ry="20"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, _korzina(960, 1070, 260, 190, t, 5309, False))
    s += ramka_pp("levo", "#1a120a", .4)
    s += vinetka(.44)
    return s


# ── 54 ─────────────────────────────────────────────────────────────────────
def babushka_zaslonyaet_dver(t):
    """Сени, за окошком ночь: внук с полным помойным ведром идёт к двери, а
    бабушка встаёт к двери и забирает ведро из рук."""
    rnd = random.Random(5407)
    s = f'<rect width="{W}" height="{H}" fill="#352a1e"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 108))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#1d1710" opacity=".35"/>')
    s += mebel_hlam(60, 980, 520, t, 5413)
    s += SL(Z_SRED, polovicy(920))
    dvx, dvy, dvw, dvh = 820, 160, 440, 760
    s += SL(Z_SRED, f'<rect x="{dvx-46}" y="{dvy-46}" width="{dvw+92}"'
                    f' height="{dvh+46}" rx="12" fill="{DOSKA2}" {o(10)}/>')
    s += SL(Z_SRED, dver(dvx, dvy, dvw, dvh, .0, "url(#derev)", True, True))
    s += SL(Z_SRED, podkova(dvx + dvw * .5, dvy - 86, 1.0, t))
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{dvx-46}" y="{dvy+i*200:.0f}" width="{dvw+92}"'
                        f' height="18" rx="6" fill="#5a3a22" opacity=".8"/>')
    ox, oy, ow, oh = 1460, 260, 380, 300
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#141d33"/>')
    for i in range(22):
        za += (f'<circle cx="{ox+rnd.uniform(10,ow-10):.0f}"'
               f' cy="{oy+rnd.uniform(10,oh*.7):.0f}"'
               f' r="{rnd.uniform(1.4,3.0):.1f}" fill="#fdf6e0"'
               f' opacity="{.3+.6*abs(A.w(t,2.4+rnd.uniform(0,2),i*.11)):.2f}"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.72:.0f}" width="{ow}" height="{oh*.28:.0f}"'
           f' fill="#232c3e"/>')
    za += izba_snaruzhi(ox + 40, oy + oh - 6, 220, t, True, True, 5417)
    s += SL(Z_SRED, f'<clipPath id="ok54"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok54)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .3, False, True))
    s += SL(Z_SRED, tusklaya_lampochka(640, 120, t, 1.1, True))
    s += SL(Z_SRED, svecha(1700, 820, t, .3, 1.4, 130))
    s += SL(Z_SRED, teplo(1700, 790, 420, 380, .34 + .1 * abs(A.w(t, 1.4))))
    pered = A.ease(A.seg(t, 1.4, 1.3))
    vx = 1420 - pered * 180
    s += SL(Z_SRED, figura(vx, 1020, 500, t, "#3a4656", "#ffd98a", False, .5,
                           True, 1.0, False, 1.2))
    ruk, (hx, hy) = rukav(vx - 90, 700, 150, 150, t, "#3a4656", "#ffd98a", .3, 4.0)
    s += SL(Z_SRED, ruk)
    vedx = hx + 110 - pered * 80
    vedy = hy + 80 + pered * 26
    s += SL(Z_SRED, _vedro(vedx, vedy, 1.5, t, True, "url(#chug)"))
    for i in range(5):                  # вонючий парок над ведром
        k = ((t * .5) + i * .2) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{vedx-20+30*A.w(t,2.2,i*.2):.0f}"'
                        f' cy="{vedy-150-k*90:.0f}" rx="{16+30*k:.0f}"'
                        f' ry="{10+20*k:.0f}" fill="#9aa37a"'
                        f' opacity="{.34*(1-k):.2f}"/>')
    bx = 900
    s += SL(Z_SRED, figura(bx, 1050, 640, t, "#5b2f3a", "#ffd98a", True, .2))
    lad = A.ease(A.seg(t, .4, .9))
    ruk2, (lx2, ly2) = rukav(bx + 130, 700, 170, -70 - 34 * lad, t, "#5b2f3a",
                             "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{lx2:.0f}" cy="{ly2:.0f}" rx="40" ry="52"'
                    f' fill="#e3c6a8" {o(6)}/>')
    ruk3, (bx3, by3) = rukav(bx + 110, 780, 180, 10 + 16 * pered, t, "#5b2f3a",
                             "#ffd98a", .5, 4.0)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, f'<ellipse cx="{bx3:.0f}" cy="{by3:.0f}" rx="30" ry="22"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, kot(500, 1060, t, .9, "#3b3430"))
    s += SL(Z_SRED, _korzina(280, 1040, 240, 180, t, 5419, False))
    s += ramka_pp("pravo", "#160f0a", .46)
    s += SL(Z_PERED, krynka(120, 1070, 1.4))
    s += vinetka(.48)
    return s


# ── 55 ─────────────────────────────────────────────────────────────────────
def stremyanka_kniga_i_forma_dlya_piro(t):
    """Прихожая квартиры: в открытой двери очередь из трёх соседей, а хозяйка
    выносит и тут же уносит обратно стремянку, толстую книгу и форму."""
    rnd = random.Random(5501)
    s = f'<rect width="{W}" height="{H}" fill="#4a4650"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#6b6472"/>')
    for i in range(14):
        s += SL(Z_DAL, f'<rect x="{i*145}" y="0" width="64" height="1080"'
                       f' fill="#766e7e" opacity=".5"/>')
    s += SL(Z_DAL, f'<rect x="0" y="900" width="{W}" height="180" fill="#54505c" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="886" width="{W}" height="26" fill="#8a8292" {o(4)}/>')
    s += SL(Z_SRED, tusklaya_lampochka(420, 120, t, 1.2, True))
    dvx, dvy, dvw, dvh = 1120, 170, 620, 760
    s += SL(Z_SRED, f'<rect x="{dvx-44}" y="{dvy-44}" width="{dvw+88}"'
                    f' height="{dvh+44}" rx="10" fill="#8f8898" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="#2a2b36"/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="{SVET}" opacity=".12"/>')
    for i in range(4):                  # лестничная клетка за дверью
        s += SL(Z_SRED, f'<path d="M{dvx:.0f},{dvy+dvh-i*120:.0f} h{dvw:.0f}'
                        f' l0,-26 h{-dvw:.0f} Z" fill="#3c3d4a" opacity=".9"/>')
    sos = ((dvx + 130, 900, 500, "#3c4656", False, True), (dvx + 310, 880, 470, "#5b4450", True, False),
           (dvx + 480, 860, 440, "#3f5c4a", False, False))
    for i, (fx, fy, fh, col, pl, sh) in enumerate(sos):
        pere = 4.0 * A.w(t, 1.6, i * .35)
        s += SL(Z_SRED, f'<g transform="rotate({pere:.1f} {fx:.0f} {fy:.0f})">'
                        + figura(fx, fy, fh, t, col, "#e8eef6", pl, i * .3, True,
                                 1.0, False, 0.0, False, sh) + '</g>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="none" {o(10)}/>')
    s += SL(Z_SRED, dver(dvx - 560, dvy, 520, dvh, .25, "#c9c2cc", False, True))
    hod = A.w(t, 3.4, .1)               # вещь едет к двери и обратно
    sx_ = 560 + hod * 180
    s += SL(Z_SRED, figura(sx_, 1020, 560, t, "#8f3a42", "#ffd98a", True, .2, True))
    strem_x = sx_ + 170 + hod * 90
    strem = (f'<g transform="rotate({-6+4*hod:.1f} {strem_x:.0f} 980)">')
    for sgn in (-1, 1):
        strem += (f'<rect x="{strem_x+sgn*90-16:.0f}" y="330" width="32" height="650"'
                  f' rx="10" fill="#b9bec6" {o(7)}/>')
    for i in range(6):
        strem += (f'<rect x="{strem_x-96:.0f}" y="{400+i*110:.0f}" width="192"'
                  f' height="26" rx="8" fill="#9aa3ab" {o(5)}/>')
    strem += (f'<rect x="{strem_x-110:.0f}" y="320" width="220" height="40" rx="12"'
              f' fill="#8a929a" {o(6)}/>')
    strem += '</g>'
    s += SL(Z_SRED, strem)
    ruk, (hx, hy) = rukav(sx_ + 90, 690, 130, -16, t, "#8f3a42", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    kn_y = 790 + 34 * A.w(t, 2.2, .3)
    kni = (f'<g transform="rotate({-8+6*A.w(t,2.2,.3):.1f} 620 {kn_y:.0f})">'
           f'<rect x="470" y="{kn_y-170:.0f}" width="300" height="340" rx="10"'
           f' fill="{TKAN}" {o(8)}/>'
           f'<rect x="470" y="{kn_y-170:.0f}" width="54" height="340" rx="8"'
           f' fill="#7a1c22" {o(6)}/>')
    for i in range(9):
        kni += (f'<rect x="{534:.0f}" y="{kn_y-150+i*34:.0f}" width="220"'
                f' height="22" fill="#efe8d6" opacity=".9"/>')
    kni += (f'<path d="M510,{kn_y-130:.0f} q0,160 0,250" fill="none" stroke="{ZOL}"'
            f' stroke-width="10" opacity=".8"/></g>')
    s += SL(Z_SRED, kni)
    fm_x, fm_y = 250, 930
    fm = (f'<ellipse cx="{fm_x:.0f}" cy="{fm_y:.0f}" rx="190" ry="76"'
          f' fill="#b9bec6" {o(8)}/>')
    fm += (f'<ellipse cx="{fm_x:.0f}" cy="{fm_y-20:.0f}" rx="160" ry="60"'
           f' fill="#cfd6dc" {o(5)}/>')
    for i in range(14):                 # волнистый край формы
        a = i * (6.28 / 14)
        fm += (f'<ellipse cx="{fm_x+math.cos(a)*175:.0f}"'
               f' cy="{fm_y+math.sin(a)*68:.0f}" rx="26" ry="16" fill="#b9bec6"'
               f' {o(4)}/>')
    fm += (f'<path d="M{fm_x-110:.0f},{fm_y-34:.0f} q110,-30 220,0" fill="none"'
           f' stroke="#eef4f8" stroke-width="12"'
           f' opacity="{.4+.4*abs(A.w(t,2.0,.2)):.2f}"/>')
    s += SL(Z_SRED, fm)
    s += SL(Z_SRED, svecha(880, 560, t, .2, 1.4, 130))
    s += SL(Z_SRED, teplo(890, 530, 460, 420, .38 + .12 * abs(A.w(t, 1.5))))
    tmb = (f'<rect x="700" y="760" width="320" height="180" rx="14"'
           f' fill="url(#derev)" {o(8)}/>')
    tmb += (f'<rect x="684" y="736" width="352" height="34" rx="10" fill="{DOSKA2}" {o(6)}/>')
    for i in range(3):
        tmb += (f'<rect x="{724+i*100:.0f}" y="800" width="76" height="100" rx="8"'
                f' fill="#8f8898" opacity=".9" {o(4)}/>')
    s += SL(Z_SRED, tmb)
    s += ramka_pp("levo", "#1a1620", .42)
    s += vinetka(.44)
    return s


# ── 56 ─────────────────────────────────────────────────────────────────────
def chuzhaya_shal_i_chuzhaya_drel(t):
    """Соседка через порог протягивает нарядную шаль с кистями, сосед из-за её
    плеча — дрель, а хозяйка прячет обе руки за спину."""
    rnd = random.Random(5603)
    s = f'<rect width="{W}" height="{H}" fill="#423c48"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#5e5766"/>')
    for i in range(12):
        s += SL(Z_DAL, f'<path d="M{70+i*170},0 q26,540 0,1080" fill="none"'
                       f' stroke="#6b6474" stroke-width="44" opacity=".5"/>')
    s += kvartira_veschi(40, 900, 520, t, 5609)
    s += SL(Z_SRED, polovicy(930))
    dvx, dvy, dvw, dvh = 980, 150, 700, 800
    s += SL(Z_SRED, f'<rect x="{dvx-48}" y="{dvy-48}" width="{dvw+96}"'
                    f' height="{dvh+48}" rx="12" fill="#8a8292" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="#2b2c38"/>')
    s += SL(Z_SRED, teplo(dvx + dvw * .5, dvy + dvh * .4, 420, 420, .22))
    s += SL(Z_SRED, tusklaya_lampochka(dvx + dvw * .5, dvy + 60, t, .9, False))
    s += SL(Z_SRED, f'<rect x="{dvx-20}" y="{dvy+dvh}" width="{dvw+40}" height="46"'
                    f' rx="10" fill="url(#derev)" {o(8)}/>')
    sx_ = dvx + 230
    s += SL(Z_SRED, figura(sx_, dvy + dvh - 6, 620, t, "#5b4450", "#ffd98a", True,
                           .3, True))
    sos_x = dvx + 520
    s += SL(Z_SRED, figura(sos_x, dvy + dvh - 30, 560, t, "#3c4656", "#cfe4f5",
                           False, .7, True, 1.0, False, 1.0, True))
    poj = A.ease(A.seg(t, 3.0, 1.2))
    s += SL(Z_SRED, f'<path d="M{sos_x-70:.0f},{dvy+dvh-430:.0f}'
                    f' q70,{-30-24*poj:.0f} 140,0" fill="none" stroke="#3c4656"'
                    f' stroke-width="44" stroke-linecap="round"/>')
    uezd = A.ease(A.seg(t, 2.6, 1.4))
    ruk_d, (dx2, dy2) = rukav(sos_x - 80, dvy + dvh - 380, 220 - 90 * uezd,
                              170 + 10 * A.w(t, 1.6), t, "#3c4656", "#cfe4f5", .4, 4.0)
    s += SL(Z_SRED, ruk_d)
    drl = (f'<g transform="rotate({-14+6*A.w(t,1.4,.2):.1f} {dx2:.0f} {dy2:.0f})">'
           f'<path d="M{dx2-96:.0f},{dy2-54:.0f} h150 q40,0 40,54 q0,54 -40,54'
           f' h-150 Z" fill="{KRAS}" {o(8)}/>'
           f'<rect x="{dx2-130:.0f}" y="{dy2-28:.0f}" width="46" height="56" rx="10"'
           f' fill="{ZHELEZ}" {o(5)}/>'
           f'<rect x="{dx2-180:.0f}" y="{dy2-14:.0f}" width="60" height="28" rx="8"'
           f' fill="#8a9398" {o(4)}/>'
           f'<path d="M{dx2-40:.0f},{dy2+54:.0f} h90 l10,110 h-110 Z"'
           f' fill="#2f3a44" {o(6)}/>'
           f'<circle cx="{dx2+34:.0f}" cy="{dy2:.0f}" r="16" fill="#cfd6dc"'
           f' opacity="{.5+.4*abs(A.w(t,.6)):.2f}"/></g>')
    s += SL(Z_SRED, drl)
    ruk_sh, (shx, shy) = rukav(sx_ - 110, dvy + dvh - 400, 230,
                               186 + 8 * A.w(t, 1.3), t, "#5b4450", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk_sh)
    kach = 6.0 * A.w(t, 1.5, .1)
    sh = f'<g transform="rotate({kach:.1f} {shx:.0f} {shy-40:.0f})">'
    sh += (f'<path d="M{shx-210:.0f},{shy-70:.0f} q210,-60 420,0'
           f' L{shx+30:.0f},{shy+250:.0f} q-30,30 -60,0 Z"'
           f' fill="{TKAN}" {o(9)}/>')
    for i in range(5):                  # складки сходятся к углу косынки
        sh += (f'<path d="M{shx-170+i*86:.0f},{shy-50:.0f}'
               f' Q{shx-40+i*20:.0f},{shy+120:.0f} {shx:.0f},{shy+240:.0f}"'
               f' fill="none" stroke="{ZOL}" stroke-width="8" opacity=".7"/>')
    sh += (f'<path d="M{shx-180:.0f},{shy-50:.0f} q180,70 360,0" fill="none"'
           f' stroke="#f2e2c8" stroke-width="13" opacity=".7"/>')
    for i in range(12):                 # кисти по обоим косым краям
        k = i / 11.0
        kx_ = shx - 210 + k * 210
        ky2 = shy - 70 + k * 316
        for sgn in (-1, 1):
            tx2 = shx + sgn * (210 - k * 210)
            sh += (f'<path d="M{tx2:.0f},{ky2:.0f}'
                   f' l{-4+3*A.w(t,1.8,i*.2):.1f},54" stroke="{TKAN}"'
                   f' stroke-width="9" stroke-linecap="round"/>')
            sh += (f'<circle cx="{tx2:.0f}" cy="{ky2:.0f}" r="8" fill="{ZOL}"/>')
    sh += '</g>'
    s += SL(Z_SRED, sh)
    hx = 560
    s += SL(Z_SRED, figura(hx, 1030, 660, t, "#4a2f3c", "#ffd98a", True, .5))
    pr = A.ease(A.seg(t, 1.6, 1.2))
    for i, sgn in enumerate((-1, 1)):
        ug = (16 + 40 * pr) * sgn + (180 if sgn < 0 else 0)
        ruk, (ax, ay) = rukav(hx + sgn * 120, 640, 170 - 50 * pr, ug, t,
                              "#4a2f3c", "#ffd98a", .2 + i * .3, 4.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="28" ry="22"'
                        f' fill="#e3c6a8" opacity="{1-pr*.75:.2f}" {o(4)}/>')
    s += SL(Z_SRED, svecha(260, 640, t, .2, 1.5, 140))
    s += SL(Z_SRED, teplo(270, 610, 480, 440, .4 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, kot(880, 1060, t, .85, "#3b3430"))
    s += ramka_pp("levo", "#181220", .44)
    s += vinetka(.46)
    return s


# ── 57 ─────────────────────────────────────────────────────────────────────
def sosed_u_dveri_zaglyanite_zavtra(t):
    """Хозяйка в дверях показывает соседу листки численника: сегодняшний
    перечёркнут, завтрашний обведён — сосед кивает и уходит со стремянкой."""
    rnd = random.Random(5701)
    s = f'<rect width="{W}" height="{H}" fill="#464050"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#67606e"/>')
    for i in range(12):
        s += SL(Z_DAL, f'<rect x="{i*165}" y="0" width="70" height="1080"'
                       f' fill="#746c7c" opacity=".45"/>')
    s += SL(Z_DAL, f'<rect x="0" y="910" width="{W}" height="170" fill="#514b5a" {o(5)}/>')
    dvx, dvy, dvw, dvh = 240, 150, 620, 800
    s += SL(Z_SRED, f'<rect x="{dvx-44}" y="{dvy-44}" width="{dvw+88}"'
                    f' height="{dvh+44}" rx="12" fill="#8a8292" {o(10)}/>')
    s += SL(Z_SRED, f'<rect x="{dvx}" y="{dvy}" width="{dvw}" height="{dvh}"'
                    f' fill="#2f2a26"/>')
    s += SL(Z_SRED, teplo(dvx + dvw * .5, dvy + dvh * .5, 460, 440, .4))
    s += SL(Z_SRED, tusklaya_lampochka(dvx + dvw * .5, dvy + 70, t, 1.0, True))
    s += SL(Z_SRED, dver(dvx + dvw, dvy, 440, dvh, .35, "#c9c2cc", False, True))
    hx = dvx + dvw * .52
    s += SL(Z_SRED, figura(hx, dvy + dvh - 10, 640, t, "#8f3a42", "#ffd98a", True, .2))
    ruk, (px2, py2) = rukav(hx + 150, dvy + 330, 210, -10 + 12 * A.w(t, 1.4), t,
                            "#8f3a42", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{px2:.0f}" cy="{py2:.0f}" rx="32" ry="24"'
                    f' fill="#e3c6a8" {o(5)}/>')
    chx, chy = 1180, 520
    chis = (f'<rect x="{chx-200:.0f}" y="{chy-330:.0f}" width="400" height="120"'
            f' rx="12" fill="#8a929a" {o(8)}/>')
    chis += (f'<circle cx="{chx:.0f}" cy="{chy-270:.0f}" r="26" fill="#cfd6dc" {o(5)}/>')
    s += SL(Z_SRED, chis)
    otr = A.ease(A.seg(t, 2.6, .9))
    s += SL(Z_SRED, _listok(chx, chy + 230, 360, 440, t, True, False, otr))
    if otr > .4:                        # под оторванным — завтрашний, обведён
        s += SL(Z_SRED, _listok(chx, chy + 210, 344, 424, t, False, True, 0.0))
    s += SL(Z_SRED, f'<rect x="{chx-176:.0f}" y="{chy-216:.0f}" width="352"'
                    f' height="40" rx="10" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, teplo(chx, chy, 420, 400, .26 + .08 * abs(A.w(t, 1.6))))
    paletz = A.ease(A.seg(t, .4, .8))
    ruk2, (fx2, fy2) = rukav(hx + 190, dvy + 430, 240 + 60 * paletz,
                             -6 + 6 * A.w(t, 1.1), t, "#8f3a42", "#ffd98a", .5, 3.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{fx2:.0f}" cy="{fy2:.0f}" rx="40" ry="26"'
                    f' fill="#e3c6a8" {o(5)}/>')
    kiv = 7.0 * A.w(t, 1.1, .2)
    sx_ = 1620
    s += SL(Z_SRED, f'<g transform="rotate({kiv:.1f} {sx_:.0f} 820)">'
                    + figura(sx_, 1040, 560, t, "#3c4656", "#e8eef6", False, .6,
                             True, 1.0, False, 0.0, True) + '</g>')
    uhod = A.ease(A.seg(t, 1.8, 1.6))
    strx = 1700 + uhod * 90
    strem = f'<g transform="rotate({12+6*A.w(t,2.4,.3):.1f} {strx:.0f} 1000)">'
    for sgn in (-1, 1):
        strem += (f'<rect x="{strx+sgn*80-14:.0f}" y="380" width="28" height="620"'
                  f' rx="10" fill="#b9bec6" {o(7)}/>')
    for i in range(5):
        strem += (f'<rect x="{strx-86:.0f}" y="{450+i*120:.0f}" width="172"'
                  f' height="24" rx="8" fill="#9aa3ab" {o(5)}/>')
    strem += '</g>'
    s += SL(Z_SRED, strem)
    s += SL(Z_SRED, svecha(1000, 980, t, .3, 1.3, 120))
    s += SL(Z_SRED, teplo(1010, 950, 400, 360, .34 + .1 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, f'<rect x="900" y="860" width="260" height="180" rx="12"'
                    f' fill="url(#derev)" {o(8)}/>'
                    f'<rect x="884" y="838" width="292" height="32" rx="10"'
                    f' fill="{DOSKA2}" {o(6)}/>')
    ves = (f'<rect x="1300" y="300" width="460" height="28" rx="8"'
           f' fill="url(#derev)" {o(7)}/>')
    for i in range(4):
        ves += (f'<circle cx="{1360+i*110:.0f}" cy="344" r="15" fill="{ZHELEZ}" {o(4)}/>')
        ves += (f'<path d="M{1360+i*110:.0f},358 q{-12+8*A.w(t,4.2,i*.2):.1f},140'
                f' {-34+12*A.w(t,4.2,i*.2):.1f},330" fill="none"'
                f' stroke="{[TKAN2, "#5b5a4a", "#7a4a3a", "#3f5c4a"][i]}"'
                f' stroke-width="70" stroke-linecap="round" opacity=".95"/>')
    s += SL(Z_SRED, ves)
    pol = (f'<rect x="1300" y="860" width="440" height="24" rx="8"'
           f' fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        pol += (f'<path d="M{1360+i*140:.0f},858 q10,-54 66,-54 q60,0 64,46'
                f' q-6,26 -64,26 q-56,0 -66,-18 Z"'
                f' fill="{["#4a3f36", "#5b4450", "#2f3a44"][i]}" {o(5)}/>')
    s += SL(Z_SRED, pol)
    kov = (f'<rect x="760" y="1000" width="620" height="80" rx="14"'
           f' fill="#5b4450" {o(7)}/>')
    for i in range(6):
        kov += (f'<rect x="{790+i*100:.0f}" y="1014" width="70" height="60" rx="8"'
                f' fill="#7a5a66" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, kov)
    s += SL(Z_SRED, hodiki(180, 300, t, 1.05))
    s += ramka_pp("pravo", "#1a1620", .42)
    s += vinetka(.44)
    return s


# ── 58 ─────────────────────────────────────────────────────────────────────
def telega_s_uzlami_u_vorot(t):
    """Телега на пол-кадра, нагруженная горой: узлы, перины, самовар, лавка
    вверх ногами и кот в корзине на самом верху."""
    rnd = random.Random(5801)
    s = sumerki_fon(t, True)
    s += ulica_dal(60, 700, 860, t, False, 5807)
    s += SL(Z_DAL, izba_snaruzhi(1320, 790, 560, t, True, True, 5813))
    s += SL(Z_DAL, gryaz_polosa(800, 200, "#473b2e"))
    for sgn, vx in ((-1, 170), (1, 1180)):
        s += SL(Z_DAL, f'<rect x="{vx:.0f}" y="340" width="54" height="520" rx="12"'
                       f' fill="url(#derev)" {o(8)}/>')
    s += SL(Z_DAL, f'<path d="M170,360 q490,-120 1060,0 l0,-50 q-570,-120 -1060,0 Z"'
                   f' fill="{DOSKA2}" {o(8)}/>')
    tx, ty = 820, 930
    kol = ""
    for i, (cx_, r_) in enumerate(((tx - 300, 130), (tx + 290, 150))):
        ang = (t * 30) % 360
        kol += (f'<g transform="rotate({ang:.1f} {cx_:.0f} {ty:.0f})">'
                f'<circle cx="{cx_:.0f}" cy="{ty:.0f}" r="{r_}" fill="none"'
                f' stroke="url(#derev)" stroke-width="26"/>')
        for j in range(8):
            a = j * .785
            kol += (f'<line x1="{cx_:.0f}" y1="{ty:.0f}"'
                    f' x2="{cx_+math.cos(a)*r_:.0f}" y2="{ty+math.sin(a)*r_:.0f}"'
                    f' stroke="url(#derev)" stroke-width="12"/>')
        kol += (f'<circle cx="{cx_:.0f}" cy="{ty:.0f}" r="26" fill="{ZHELEZ}" {o(5)}/></g>')
    s += SL(Z_SRED, kol)
    tel = (f'<rect x="{tx-400:.0f}" y="{ty-170:.0f}" width="800" height="120" rx="12"'
           f' fill="url(#dosk)" {o(9)}/>')
    for i in range(9):
        tel += (f'<rect x="{tx-390+i*88:.0f}" y="{ty-166:.0f}" width="70"'
                f' height="112" rx="8" fill="url(#dosk)" {o(5)}/>')
    tel += (f'<path d="M{tx-430:.0f},{ty-190:.0f} h860 l-20,30 h-820 Z"'
            f' fill="{DOSKA2}" {o(6)}/>')
    tel += (f'<path d="M{tx-420:.0f},{ty-120:.0f} l-260,-80" stroke="url(#derev)"'
            f' stroke-width="24" stroke-linecap="round"/>')
    s += SL(Z_SRED, tel)
    kach = 2.6 * A.w(t, 1.9, .1)
    gora = f'<g transform="rotate({kach:.2f} {tx:.0f} {ty-180:.0f})">'
    for i in range(6):                  # узлы
        ux = tx - 330 + (i % 3) * 230 + (i // 3) * 90
        uy = ty - 240 - (i // 3) * 190
        col = [TKAN, TKAN2, "#6b8a4a", "#8a6a3a", "#7a4a5a", "#4a6a7a"][i]
        gora += (f'<path d="M{ux-120:.0f},{uy+40:.0f} q-20,-130 120,-150'
                 f' q140,20 120,150 q-120,50 -240,0 Z" fill="{col}" {o(7)}/>')
        for sgn in (-1, 1):             # завязанные углы узла
            gora += (f'<path d="M{ux+sgn*70:.0f},{uy-110:.0f}'
                     f' q{sgn*60:.0f},-50 {sgn*86:.0f},-14'
                     f' q{-sgn*40:.0f},40 {-sgn*76:.0f},44 Z" fill="{col}" {o(5)}/>')
        gora += (f'<ellipse cx="{ux:.0f}" cy="{uy-110:.0f}" rx="46" ry="26"'
                 f' fill="{col}" {o(5)}/>')
        gora += (f'<path d="M{ux-100:.0f},{uy-20:.0f} q100,46 200,0" fill="none"'
                 f' stroke="#efe3c8" stroke-width="12" opacity=".75"/>')
        gora += (f'<path d="M{ux-96:.0f},{uy+28:.0f} q96,40 192,0" fill="none"'
                 f' stroke="#efe3c8" stroke-width="9" opacity=".5"/>')
    for i in range(2):                  # перины
        gora += (f'<path d="M{tx-320+i*300:.0f},{ty-540:.0f} q200,-80 400,0'
                 f' q-20,90 -200,96 q-180,-6 -200,-96 Z" fill="#eef2f6" {o(7)}/>')
        gora += (f'<path d="M{tx-300+i*300:.0f},{ty-520:.0f} q180,40 360,0"'
                 f' fill="none" stroke="#b9c6cf" stroke-width="9" opacity=".8"/>')
    lav = (f'<g transform="rotate(188 {tx+330:.0f} {ty-440:.0f})">'
           f'<rect x="{tx+180:.0f}" y="{ty-470:.0f}" width="300" height="30" rx="10"'
           f' fill="url(#derev)" {o(6)}/>'
           f'<rect x="{tx+200:.0f}" y="{ty-440:.0f}" width="26" height="120"'
           f' fill="url(#derev)" {o(5)}/>'
           f'<rect x="{tx+430:.0f}" y="{ty-440:.0f}" width="26" height="120"'
           f' fill="url(#derev)" {o(5)}/></g>')
    gora += lav
    gora += '</g>'
    s += SL(Z_SRED, gora)
    sx_, sy_ = tx - 150, ty - 660
    sam = (f'<path d="M{sx_-150:.0f},{sy_:.0f} q-54,-200 80,-256 q66,-26 134,0'
           f' q134,56 80,256 Z" fill="url(#zol)" {o(9)}/>')
    sam += (f'<path d="M{sx_-130:.0f},{sy_-120:.0f} q130,54 260,0" fill="none"'
            f' stroke="#fff3cc" stroke-width="10" opacity=".6"/>')
    sam += (f'<rect x="{sx_-70:.0f}" y="{sy_-250:.0f}" width="140" height="64" rx="10"'
            f' fill="url(#zol)" {o(6)}/>')
    sam += (f'<rect x="{sx_-40:.0f}" y="{sy_-330:.0f}" width="80" height="90" rx="8"'
            f' fill="url(#med)" {o(6)}/>')
    sam += (f'<path d="M{sx_+100:.0f},{sy_-90:.0f} q60,10 50,70" fill="none"'
            f' stroke="url(#zol)" stroke-width="18" stroke-linecap="round"/>')
    for sgn in (-1, 1):
        sam += (f'<path d="M{sx_+sgn*110:.0f},{sy_-130:.0f} q{sgn*60:.0f},10'
                f' {sgn*10:.0f},70" fill="none" stroke="url(#med)" stroke-width="16"/>')
    sam += (f'<ellipse cx="{sx_:.0f}" cy="{sy_+6:.0f}" rx="120" ry="24"'
            f' fill="url(#med)" {o(6)}/>')
    sam += (f'<path d="M{sx_-60:.0f},{sy_-150:.0f} q20,70 10,120" fill="none"'
            f' stroke="#fff3cc" stroke-width="16"'
            f' opacity="{.35+.35*abs(A.w(t,2.2,.1)):.2f}"/>')
    s += SL(Z_SRED, sam)
    s += SL(Z_SRED, dym(sx_, sy_ - 340, t, 5, .26, 300, .4, "#d8d2c6", .9))
    s += SL(Z_SRED, teplo(sx_, sy_ - 90, 360, 320, .3 + .1 * abs(A.w(t, 1.6))))
    kx_, ky_ = tx + 180, ty - 700
    s += SL(Z_SRED, _korzina(kx_, ky_, 300, 220, t, 5821, False))
    vygl = 24 * abs(A.w(t, 2.2, .2))
    s += SL(Z_SRED, f'<g transform="translate(0,{-vygl:.0f})">'
                    + kot(kx_, ky_ - 160, t, .8, "#4a4038") + '</g>')
    mah = 26 * A.w(t, 1.2, .1)
    zx_ = 1560
    s += SL(Z_SRED, figura(zx_, 980, 500, t, "#5b2f3a", "#ffd98a", True, .3, True))
    ruk, (ax, ay) = rukav(zx_ - 90, 700, 190, 236 + mah, t, "#5b2f3a", "#ffd98a", .2, 8.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="28" ry="22"'
                    f' fill="#e3c6a8" {o(4)}/>')
    fnx, fny = 230, 420
    s += SL(Z_SRED, f'<path d="M{fnx-62:.0f},{fny:.0f} h124 l-14,-34 h-96 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-52:.0f},{fny:.0f} h104 l-12,124 h-80 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 112, t, .56, .3, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 70, 330, 300, .42 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_PERED, pleten(1480, 1080, 440, 210, 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 5827, .46, .9))
    s += vinetka(.46)
    return s


# ── 59 ─────────────────────────────────────────────────────────────────────
def novaya_izba_bez_lada(t):
    """Новая изба из свежих брёвен в разрезе: гости с караваем на пороге, а
    внутри всё вкривь — лавку тянут врозь, ухват падает, каша лезет."""
    rnd = random.Random(5903)
    s = sumerki_fon(t, False)
    s += ulica_dal(1300, 660, 620, t, False, 5923)
    s += SL(Z_DAL, gryaz_polosa(820, 180, "#5a4c3a"))
    izb = (f'<rect x="70" y="180" width="1300" height="760" fill="#c49a62" {o(10)}/>')
    for i in range(9):                  # свежие светлые брёвна
        izb += (f'<rect x="70" y="{180+i*86:.0f}" width="1300" height="82" rx="38"'
                f' fill="#d8b07a" {o(5)}/>')
        izb += (f'<rect x="84" y="{232+i*86:.0f}" width="1272" height="14" rx="7"'
                f' fill="#b08a52" opacity=".5"/>')
    izb += (f'<path d="M20,190 L720,-120 L1420,190 Z" fill="#b98f5a" {o(9)}/>')
    izb += (f'<rect x="1060" y="-170" width="110" height="230" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(1116, -160, t, 5, .22, 320, .34, "#d8d2c6", 1.0))
    s += SL(Z_SRED, f'<rect x="130" y="260" width="1180" height="620" fill="#4a3826"'
                    f' opacity=".92" {o(8)}/>')
    s += SL(Z_SRED, f'<line x1="130" y1="580" x2="1310" y2="580" stroke="#6b4a2a"'
                    f' stroke-width="20"/>')
    s += SL(Z_SRED, polovicy(880))
    s += SL(Z_SRED, pech(880, 300, 400, 560, t, True, True, False))
    s += SL(Z_SRED, teplo(1060, 640, 460, 380, .4 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, iskra_let(t, 1000, 580, 8, 5927, 280, .45))
    chx, chy = 1180, 360
    s += SL(Z_SRED, f'<path d="M{chx-90:.0f},{chy:.0f} q90,150 180,0'
                    f' q-90,40 -180,0 Z" fill="url(#chug)" {o(7)}/>'
                    f'<ellipse cx="{chx:.0f}" cy="{chy-6:.0f}" rx="94" ry="26"'
                    f' fill="#4a4645" {o(5)}/>')
    for i in range(6):                  # каша лезет из чугунка
        k = ((t * .6) + i * .17) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{chx-70+i*28:.0f}" cy="{chy-18+k*110:.0f}"'
                        f' rx="{26-6*k:.0f}" ry="{20-5*k:.0f}" fill="#efe3c8"'
                        f' opacity="{.95-.4*k:.2f}" {o(3)}/>')
    s += SL(Z_SRED, par(chx, chy - 40, t, 4, .5, 170, .5, .9))
    lx_, ly_ = 540, 790
    tyan = A.w(t, 1.6, .1)
    s += SL(Z_SRED, f'<g transform="rotate({3*tyan:.1f} {lx_:.0f} {ly_:.0f})">'
                    + lavka(lx_ - 230 + tyan * 24, ly_, 460) + '</g>')
    for i, sgn in enumerate((-1, 1)):
        fx = lx_ + sgn * (330 + tyan * sgn * 26)
        s += SL(Z_SRED, figura(fx, 880, 520, t, "#5b2f3a" if sgn > 0 else "#3c4656",
                               "#ffd98a", sgn > 0, i * .4, True))
        ruk, (ax, ay) = rukav(fx - sgn * 90, 660, 170, 180 if sgn > 0 else 0, t,
                              "#5b2f3a" if sgn > 0 else "#3c4656", "#ffd98a", i * .3, 5.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="26" ry="20"'
                        f' fill="#e3c6a8" {o(4)}/>')
    pad = A.out(A.seg(t, 1.4, .9))
    uhx, uhy = 760, 500
    s += SL(Z_SRED, f'<g transform="rotate({-10+96*pad:.0f} {uhx:.0f} {uhy+260:.0f})">'
                    f'<rect x="{uhx-14:.0f}" y="{uhy:.0f}" width="28" height="300"'
                    f' rx="10" fill="url(#derev)" {o(6)}/>'
                    f'<path d="M{uhx-64:.0f},{uhy+10:.0f} q64,-92 128,0" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="22"/></g>')
    for i in range(3):
        s += SL(Z_SRED, krynka(690 + i * 86, 870 + (i % 2) * 10,
                               1.0 + .2 * (i % 2)))
    for i in range(5):                  # черепки и брызги от падения
        if pad > .5:
            s += SL(Z_SRED, f'<path d="M{700+i*60:.0f},{866:.0f} l26,-20 l10,24 Z"'
                            f' fill="#9c6a3c" opacity="{(pad-.5)*2:.2f}" {o(3)}/>')
    s += SL(Z_SRED, kot(330, 860, t, .95, "#3b3430", True))
    sob_x = 200
    s += SL(Z_SRED, f'<ellipse cx="{sob_x:.0f}" cy="840" rx="78" ry="48"'
                    f' fill="#7a6246" {o(6)}/>'
                    f'<circle cx="{sob_x-56:.0f}" cy="800" r="40" fill="#7a6246" {o(6)}/>'
                    f'<path d="M{sob_x-96:.0f},770 l-16,-44 l40,16 Z" fill="#6b5436" {o(4)}/>'
                    f'<path d="M{sob_x-96:.0f},812 q-30,8 -40,-6" fill="none"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<circle cx="{sob_x-72:.0f}" cy="792" r="6" fill="{K}"/>'
                    f'<path d="M{sob_x+70:.0f},824 q50,-20 40,-70" fill="none"'
                    f' stroke="#7a6246" stroke-width="18" stroke-linecap="round"/>')
    gx_ = 1560
    s += SL(Z_SRED, f'<rect x="1380" y="880" width="520" height="40" rx="10"'
                    f' fill="url(#dosk)" {o(7)}/>')
    s += SL(Z_SRED, figura(gx_, 880, 500, t, "#4a5a6b", "#ffd0a0", False, .3, True,
                           1.0, True, 1.0, True, True))
    s += SL(Z_SRED, figura(gx_ + 190, 884, 470, t, "#6b4450", "#ffd0a0", True, .7, True))
    s += SL(Z_SRED, karavay(gx_ + 90, 640, 1.3, True))
    s += SL(Z_SRED, para_izo_rta(gx_ + 46, 500, t, .2, 1.0, .5))
    s += ramka_pp("levo", "#1d150c", .42)
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 5939, .36, .8))
    s += vinetka(.44)
    return s


# ── 60 ─────────────────────────────────────────────────────────────────────
def gruzovik_u_podezda(t):
    """Фургон без надписей у подъезда на пол-кадра: двое грузчиков вертят в
    дверях диван, на балконе шарики, а женщина показывает им календарь."""
    rnd = random.Random(6007)
    s = f'<rect width="{W}" height="{H}" fill="#1c2430"/>'
    s += nebo("sumer", t, True, 6011)
    s += panelka(-200, 620, 1000, t, 4, True, 6029)
    s += panelka(1500, 600, 560, t, 4, True, 6037)
    s += SL(Z_DAL, gryaz_polosa(900, 190, "#2b3038"))
    pd = (f'<rect x="700" y="180" width="700" height="740" fill="url(#beton)" {o(9)}/>')
    pd += (f'<path d="M640,420 h820 l-50,-110 h-720 Z" fill="{BETON2}" {o(8)}/>')
    pd += (f'<rect x="900" y="440" width="320" height="480" rx="8" fill="#3d4650" {o(8)}/>')
    pd += (f'<rect x="950" y="490" width="220" height="200" rx="8"'
           f' fill="url(#stekl)" opacity=".5" {o(5)}/>')
    s += SL(Z_SRED, pd)
    s += SL(Z_SRED, tusklaya_lampochka(1060, 400, t, .9, False))
    bal = (f'<rect x="720" y="120" width="420" height="40" rx="8" fill="{BETON2}" {o(6)}/>')
    for i in range(9):
        bal += (f'<rect x="{736+i*46:.0f}" y="20" width="14" height="100" rx="5"'
                f' fill="#8a929a" {o(3)}/>')
    s += SL(Z_SRED, bal)
    for i in range(5):                  # шарики к новоселью
        kx_ = 760 + i * 84
        kach = 16 * A.w(t, 2.2 + i * .3, i * .2)
        bal_c = [KRAS, "#3a7ad0", ZEL2, ZOL, "#b05aa0"][i]
        s += SL(Z_SRED, f'<g transform="translate({kach:.1f},0)">'
                        f'<ellipse cx="{kx_:.0f}" cy="{210+((i%2)*26):.0f}" rx="40"'
                        f' ry="50" fill="{bal_c}" {o(5)}/>'
                        f'<path d="M{kx_:.0f},{260+((i%2)*26):.0f} q14,60 -10,120"'
                        f' fill="none" stroke="#e8eef6" stroke-width="4"/>'
                        f'<ellipse cx="{kx_-14:.0f}" cy="{194+((i%2)*26):.0f}" rx="12"'
                        f' ry="16" fill="#ffffff" opacity=".45"/></g>')
    fx_, fy_ = 400, 900
    fur = ten(fx_ + 60, fy_ + 16, 460, 26, .5)
    fur += (f'<rect x="{fx_-360:.0f}" y="{fy_-480:.0f}" width="760" height="420"'
            f' rx="16" fill="#cfd6dc" {o(10)}/>')
    fur += (f'<path d="M{fx_+400:.0f},{fy_-60:.0f} l0,-300 l120,-20 l90,140 l0,180 Z"'
            f' fill="#b9c2c8" {o(9)}/>')
    fur += (f'<path d="M{fx_+430:.0f},{fy_-340:.0f} l90,-14 l64,118 h-154 Z"'
            f' fill="url(#stekl)" opacity=".75" {o(5)}/>')
    fur += (f'<circle cx="{fx_+586:.0f}" cy="{fy_-120:.0f}" r="26" fill="{SVET}"'
            f' opacity="{.5+.4*abs(A.w(t,1.8)):.2f}" {o(4)}/>')
    fur += teplo(fx_ + 600, fy_ - 120, 260, 200, .34)
    zakr = A.ease(A.seg(t, 4.0, 1.6))
    fur += (f'<g transform="rotate({-20+18*zakr:.0f} {fx_-360:.0f} {fy_-60:.0f})">'
            f'<rect x="{fx_-540:.0f}" y="{fy_-470:.0f}" width="190" height="410"'
            f' rx="10" fill="#dfe6ea" {o(8)}/>'
            f'<rect x="{fx_-522:.0f}" y="{fy_-450:.0f}" width="154" height="370"'
            f' rx="8" fill="none" stroke="#9aa3ab" stroke-width="8"/>'
            f'<circle cx="{fx_-376:.0f}" cy="{fy_-266:.0f}" r="14" fill="#8a929a"/></g>')
    for cx_ in (fx_ - 230, fx_ + 310):
        ang = (t * 40) % 360
        fur += (f'<g transform="rotate({ang:.0f} {cx_:.0f} {fy_-30:.0f})">'
                f'<circle cx="{cx_:.0f}" cy="{fy_-30:.0f}" r="92" fill="#2b2f34" {o(6)}/>'
                f'<circle cx="{cx_:.0f}" cy="{fy_-30:.0f}" r="44" fill="#8a929a" {o(5)}/>'
                f'<line x1="{cx_-40:.0f}" y1="{fy_-30:.0f}" x2="{cx_+40:.0f}"'
                f' y2="{fy_-30:.0f}" stroke="#5e666c" stroke-width="10"/></g>')
    s += SL(Z_SRED, fur)
    div_a = -16 + 44 * abs(A.w(t, 1.1, .1))
    dvx_, dvy_ = 1030, 820
    div = f'<g transform="rotate({div_a:.0f} {dvx_:.0f} {dvy_:.0f})">'
    div += (f'<rect x="{dvx_-240:.0f}" y="{dvy_-120:.0f}" width="480" height="150"'
            f' rx="24" fill="#6b5a7a" {o(8)}/>')
    div += (f'<rect x="{dvx_-240:.0f}" y="{dvy_-250:.0f}" width="480" height="150"'
            f' rx="24" fill="#7a6a8a" {o(8)}/>')
    for i in range(3):
        div += (f'<rect x="{dvx_-220+i*156:.0f}" y="{dvy_-110:.0f}" width="140"'
                f' height="120" rx="18" fill="#8a7a9a" opacity=".9" {o(4)}/>')
    for sgn in (-1, 1):
        div += (f'<rect x="{dvx_+sgn*240-40:.0f}" y="{dvy_-250:.0f}" width="80"'
                f' height="280" rx="20" fill="#6b5a7a" {o(6)}/>')
    div += '</g>'
    s += SL(Z_SRED, div)
    for i, gx in enumerate((850, 1240)):
        s += SL(Z_SRED, figura(gx, 1040, 520, t, "#3a4a3a", "#cfe4f5", False,
                               i * .4, True, 1.0, False, 1.2, False, True))
        ruk, (ax, ay) = rukav(gx + (90 if i else -90), 740, 160,
                              (0 if i else 180) + (12 if i else -12), t, "#3a4a3a",
                              "#cfe4f5", i * .3, 4.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, para_izo_rta(gx + 44, 660, t, i * .4, 1.0, .5))
    zx_ = 1760
    s += SL(Z_SRED, figura(zx_, 980, 540, t, "#8f3a42", "#ffd0a0", False, .5, True))
    ruk2, (kx2, ky2) = rukav(zx_ - 110, 700, 150, 192, t, "#8f3a42", "#ffd0a0", .3, 4.0)
    s += SL(Z_SRED, ruk2)
    kal_x, kal_y = kx2 - 110, ky2 + 10
    kal = (f'<rect x="{kal_x-150:.0f}" y="{kal_y-190:.0f}" width="300" height="380"'
           f' rx="12" fill="url(#list)" {o(8)}/>')
    kal += (f'<rect x="{kal_x-150:.0f}" y="{kal_y-190:.0f}" width="300" height="80"'
            f' rx="12" fill="{TKAN2}" {o(5)}/>')
    for r in range(4):
        for c in range(5):
            kal += (f'<rect x="{kal_x-126+c*52:.0f}" y="{kal_y-86+r*62:.0f}"'
                    f' width="40" height="44" rx="6" fill="#dfd7c2" {o(2)}/>')
    kal += (f'<g opacity="{.6+.4*abs(A.w(t,1.3)):.2f}">'
            f'<line x1="{kal_x-100:.0f}" y1="{kal_y-70:.0f}" x2="{kal_x-40:.0f}"'
            f' y2="{kal_y-14:.0f}" stroke="{KRAS}" stroke-width="12"/>'
            f'<line x1="{kal_x-40:.0f}" y1="{kal_y-70:.0f}" x2="{kal_x-100:.0f}"'
            f' y2="{kal_y-14:.0f}" stroke="{KRAS}" stroke-width="12"/></g>')
    kal += (f'<ellipse cx="{kal_x+64:.0f}" cy="{kal_y+14:.0f}" rx="44" ry="38"'
            f' fill="none" stroke="{ZEL2}" stroke-width="11"'
            f' opacity="{.6+.4*abs(A.w(t,1.1,.3)):.2f}"/>')
    s += SL(Z_SRED, kal)
    s += SL(Z_SRED, f'<rect x="{zx_+40:.0f}" y="640" width="46" height="86" rx="10"'
                    f' fill="#2b2f34" {o(5)}/>'
                    f'<rect x="{zx_+46:.0f}" y="650" width="34" height="64" rx="4"'
                    f' fill="{SVET}" opacity="{.5+.4*abs(A.w(t,1.5,.2)):.2f}"/>')
    s += ramka_pp("pravo", "#0e131a", .44)
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 6043, .46, 1.0))
    s += vinetka(.48)
    return s


# ── 61 ─────────────────────────────────────────────────────────────────────
def kosa_do_poyasa(t):
    """Девушка у окна вполоборота расчёсывает костяным гребнем русую косу до
    пояса, а выпавший волосок прячет в щель между брёвнами."""
    rnd = random.Random(6101)
    s = f'<rect width="{W}" height="{H}" fill="#4a3728"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 112))
    s += utvar_izby(1420, 300, 420, t, 6113)
    s += SL(Z_SRED, polovicy(940))
    ox, oy, ow, oh = 1060, 180, 560, 470
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#b9c6cf"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.66:.0f}" width="{ow}" height="{oh*.34:.0f}"'
           f' fill="#8a9a74"/>')
    za += izba_snaruzhi(ox + 40, oy + oh - 10, 240, t, True, True, 6121)
    za += (f'<circle cx="{ox+ow*.78:.0f}" cy="{oy+oh*.22:.0f}" r="64" fill="#fff3cc"'
           f' opacity=".9"/>')
    s += SL(Z_SRED, f'<clipPath id="ok61"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok61)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .08, False, True))
    s += SL(Z_SRED, luch(ox - 40, oy + oh, 420, 480, t, .26))
    s += SL(Z_SRED, teplo(ox + 100, oy + oh + 160, 620, 520, .34))
    s += SL(Z_SRED, lavka(760, 980, 520))
    dx_, dy_ = 700, 980
    s += SL(Z_SRED, figura(dx_, dy_, 700, t, "#8f3a42", "#ffd98a", False, .2, True))
    s += SL(Z_SRED, f'<path d="M{dx_-90:.0f},{dy_-430:.0f} q90,-30 180,0'
                    f' l30,410 q-120,46 -240,0 Z" fill="#b8323a" opacity=".92" {o(7)}/>')
    for i in range(4):                  # поясок и оборки сарафана
        s += SL(Z_SRED, f'<path d="M{dx_-150:.0f},{dy_-120+i*30:.0f}'
                        f' q150,40 300,0" fill="none" stroke="{ZOL}"'
                        f' stroke-width="7" opacity=".6"/>')
    kx_, ky_ = dx_ - 190, dy_ - 500
    sway = 7 * A.w(t, 1.8, .1)
    kosa = f'<g transform="rotate({sway:.1f} {kx_:.0f} {ky_:.0f})">'
    kosa += (f'<path d="M{kx_+120:.0f},{ky_-80:.0f} q-110,-20 -130,80'
             f' q-16,130 6,260 q16,110 34,220" fill="none" stroke="#c49a4e"'
             f' stroke-width="84" stroke-linecap="round"/>')
    for i in range(7):                  # перевивы косы
        yy = ky_ + 50 + i * 76
        kosa += (f'<path d="M{kx_-52+i*5:.0f},{yy:.0f} q46,26 92,0"'
                 f' fill="none" stroke="#a87c38" stroke-width="10" opacity=".85"/>')
        kosa += (f'<path d="M{kx_-42+i*5:.0f},{yy-18:.0f} q40,22 80,-4"'
                 f' fill="none" stroke="#e8c57c" stroke-width="8"'
                 f' opacity="{.4+.4*abs(A.w(t,2.2,i*.15)):.2f}"/>')
    kosa += (f'<path d="M{kx_+30:.0f},{ky_+570:.0f} q20,40 -20,70" fill="none"'
             f' stroke="{TKAN}" stroke-width="22" stroke-linecap="round"/>')
    kosa += '</g>'
    s += SL(Z_SRED, kosa)
    greb = A.seg(t, .3, 1.8)
    gy_ = ky_ + 90 + greb * 420
    s += SL(Z_SRED, f'<g transform="rotate({8+8*A.w(t,1.4):.0f} {kx_-60:.0f} {gy_:.0f})">'
                    f'<rect x="{kx_-150:.0f}" y="{gy_-24:.0f}" width="180" height="48"'
                    f' rx="12" fill="#efe3c8" {o(6)}/>'
                    + "".join(f'<rect x="{kx_-140+j*24:.0f}" y="{gy_+22:.0f}"'
                              f' width="10" height="48" rx="4" fill="#efe3c8"'
                              f' {o(2)}/>' for j in range(7)) + '</g>')
    ruk, (hx, hy) = rukav(dx_ - 110, dy_ - 430, 150, 200 + 16 * A.w(t, 1.4, .2), t,
                          "#8f3a42", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    smot = A.ease(A.seg(t, 1.4, 1.0))
    vx_ = 330 + smot * 60
    s += SL(Z_SRED, f'<path d="M{vx_:.0f},{700-smot*60:.0f} q30,{60+40*smot:.0f}'
                    f' {-10-20*smot:.0f},{120+60*smot:.0f}" fill="none"'
                    f' stroke="#e8c57c" stroke-width="7" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="{vx_-20:.0f}" cy="{830+smot*40:.0f}"'
                    f' rx="{16+8*smot:.0f}" ry="{10+6*smot:.0f}" fill="none"'
                    f' stroke="#e8c57c" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="270" y="600" width="260" height="16" rx="6"'
                    f' fill="#2b1f14" opacity=".9"/>')
    s += SL(Z_SRED, svecha(260, 760, t, .2, 1.6, 150))
    s += SL(Z_SRED, teplo(270, 720, 520, 470, .4 + .12 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, krynka(1700, 1020, 1.4))
    s += SL(Z_PERED, zanaveska(1020, 140, 460, 190, TKAN, t, 1))
    s += ramka_pp("levo", "#1a1208", .42)
    s += vinetka(.44)
    return s


# ── 62 ─────────────────────────────────────────────────────────────────────
def strizhenyy_na_holode(t):
    """Парень со свежей стрижкой вышел на крыльцо без шапки, уши на глазах
    краснеют — и он чихает так, что с пугала слетает шапка."""
    rnd = random.Random(6203)
    s = sumerki_fon(t, True)
    s += ulica_dal(1180, 700, 740, t, False, 6211)
    s += SL(Z_DAL, gryaz_polosa(790, 200, "#473c30"))
    izb = brevna(0, 160, 1000, 700, 110)
    izb += (f'<path d="M-40,170 L500,-110 L1040,170 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="700" y="-160" width="100" height="220" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(750, -150, t, 5, .22, 300, .34, "#c8d0da", 1.0))
    ok = okno_izby(130, 340, 280, 210, t, None, .25, True, True)
    s += SL(Z_SRED, ok)
    s += SL(Z_SRED, teplo(270, 450, 340, 300, .36 + .1 * abs(A.w(t, 1.7))))
    kr = (f'<path d="M420,900 h620 l-40,-120 h-540 Z" fill="url(#dosk)" {o(9)}/>')
    kr += (f'<rect x="440" y="900" width="580" height="46" rx="10" fill="{DOSKA2}" {o(7)}/>')
    for i in range(3):
        kr += (f'<rect x="{460+i*16:.0f}" y="{946+i*40:.0f}" width="{560-i*32:.0f}"'
               f' height="34" rx="8" fill="url(#dosk)" {o(5)}/>')
    kr += (f'<rect x="980" y="400" width="34" height="500" fill="url(#derev)" {o(7)}/>')
    kr += (f'<path d="M400,400 h640 l-30,-54 h-580 Z" fill="{DOSKA2}" {o(7)}/>')
    s += SL(Z_SRED, kr)
    chih = A.seg(t, 2.4, .35)
    nak = -26 * math.sin(min(1.0, chih) * 3.14)
    px_ = 700
    s += SL(Z_SRED, f'<g transform="rotate({nak:.1f} {px_:.0f} 880)">'
                    + figura(px_, 880, 680, t, "#3c4656", "#ffd0a0", False, .2,
                             False, 1.0, False, 1.0) + '</g>')
    kras = A.ease(A.seg(t, .6, 1.8))
    gy_ = 880 - 680 * .845
    for sgn in (-1, 1):                 # уши торчат и краснеют
        s += SL(Z_SRED, f'<g transform="rotate({nak:.1f} {px_:.0f} 880)">'
                        f'<ellipse cx="{px_+sgn*100:.0f}" cy="{gy_+10:.0f}" rx="30"'
                        f' ry="42" fill="#f0cfae" {o(5)}/>'
                        f'<ellipse cx="{px_+sgn*100:.0f}" cy="{gy_+10:.0f}" rx="26"'
                        f' ry="38" fill="{KRAS}" opacity="{.72*kras:.2f}"/></g>')
    s += SL(Z_SRED, f'<g transform="rotate({nak:.1f} {px_:.0f} 880)">'
                    f'<ellipse cx="{px_:.0f}" cy="{gy_+36:.0f}" rx="20" ry="16"'
                    f' fill="{KRAS}" opacity="{.6*kras:.2f}"/>'
                    f'<path d="M{px_-86:.0f},{gy_-72:.0f} q86,-30 172,0" fill="none"'
                    f' stroke="#5a4a36" stroke-width="16" opacity=".9"/></g>')
    ruk, (hx, hy) = rukav(px_ + 110, 560, 150, -96 + 20 * A.w(t, 1.6), t,
                          "#3c4656", "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="34" ry="24"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, para_izo_rta(px_ + 60, gy_ + 40, t, .1,
                                 1.0 + 1.6 * math.sin(min(1.0, chih) * 3.14), .62))
    s += SL(Z_SRED, _vedro(470, 1040, .9, t, False, "url(#chug)"))
    kr_x, kr_y = 1080, 940
    s += SL(Z_SRED, f'<path d="M{kr_x-60:.0f},{kr_y-110:.0f} q60,120 120,0'
                    f' q-60,34 -120,0 Z" fill="url(#krem)" {o(7)}/>'
                    f'<path d="M{kr_x+58:.0f},{kr_y-96:.0f} q46,26 0,58" fill="none"'
                    f' stroke="url(#krem)" stroke-width="12"/>')
    s += SL(Z_SRED, par(kr_x, kr_y - 120, t, 5, .5, 190, .55, .9))
    pg_x, pg_y = 1500, 960
    pug = (f'<rect x="{pg_x-14:.0f}" y="{pg_y-480:.0f}" width="28" height="480"'
           f' fill="url(#derev)" {o(6)}/>')
    pug += (f'<rect x="{pg_x-170:.0f}" y="{pg_y-390:.0f}" width="340" height="24"'
            f' rx="10" fill="url(#derev)" {o(5)}/>')
    pug += (f'<path d="M{pg_x-120:.0f},{pg_y-380:.0f} q120,-60 240,0 l-40,250'
            f' q-80,40 -160,0 Z" fill="#6b5a3c" {o(7)}/>')
    for sgn in (-1, 1):                 # соломенные руки на перекладине
        for j in range(5):
            pug += (f'<path d="M{pg_x+sgn*160:.0f},{pg_y-378:.0f}'
                    f' l{sgn*(30+j*12):.0f},{-20+j*16:.0f}" stroke="#d8b96a"'
                    f' stroke-width="7" stroke-linecap="round"/>')
        pug += (f'<path d="M{pg_x+sgn*130:.0f},{pg_y-392:.0f}'
                f' q{sgn*20:.0f},24 {sgn*4:.0f},46" fill="none" stroke="{TKAN}"'
                f' stroke-width="9"/>')
    for j in range(7):                  # солома из-под подола
        pug += (f'<path d="M{pg_x-70+j*24:.0f},{pg_y-130:.0f} l{-6+j*2},54"'
                f' stroke="#d8b96a" stroke-width="7" stroke-linecap="round"/>')
    pug += (f'<circle cx="{pg_x:.0f}" cy="{pg_y-430:.0f}" r="64" fill="url(#solom)" {o(6)}/>')
    for i in (-1, 1):
        pug += (f'<circle cx="{pg_x+i*24:.0f}" cy="{pg_y-440:.0f}" r="9" fill="{K}"/>')
    for i in range(9):
        pug += (f'<path d="M{pg_x-60+i*16:.0f},{pg_y-480:.0f} l{-6+i*2},-40"'
                f' stroke="#d8b96a" stroke-width="6" stroke-linecap="round"/>')
    s += SL(Z_SRED, pug)
    sle = A.out(A.seg(t, 2.5, 1.2))
    shx = pg_x + sle * 240
    shy = pg_y - 500 - math.sin(sle * 3.14) * 180 + sle * 40
    s += SL(Z_SRED, f'<g transform="rotate({sle*260:.0f} {shx:.0f} {shy:.0f})">'
                    f'<path d="M{shx-70:.0f},{shy:.0f} q70,-96 140,0 q-70,30 -140,0 Z"'
                    f' fill="#53402e" {o(6)}/>'
                    f'<path d="M{shx-80:.0f},{shy-4:.0f} q80,40 160,0 l-8,34'
                    f' q-72,32 -144,0 Z" fill="#7a6246" {o(5)}/></g>')
    s += SL(Z_PERED, pleten(1180, 1080, 740, 220, 8))
    s += SL(Z_PERED, goloe_derevo(170, 1080, 560, t, 6229, 7, "#2a2b33"))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 6247, .46, .9))
    s += vinetka(.46)
    return s


# ── 63 ─────────────────────────────────────────────────────────────────────
def strizhka_posredi_kuhni(t):
    """Кухня, посреди неё на газетах табурет: мальчик, закутанный в простыню
    до ушей, вертит головой, пряди падают, чайник на плите пускает пар."""
    rnd = random.Random(6301)
    s = f'<rect width="{W}" height="{H}" fill="#6b6256"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#8a8072"/>')
    for r in range(8):                  # кафель по стене
        for c in range(14):
            s += SL(Z_DAL, f'<rect x="{c*140+6:.0f}" y="{r*86+6:.0f}" width="128"'
                           f' height="74" rx="6" fill="#9c9282" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect x="0" y="700" width="{W}" height="30" fill="#6b6256" {o(4)}/>')
    s += SL(Z_SRED, polovicy(900))
    s += SL(Z_SRED, tusklaya_lampochka(960, 90, t, 1.2, True))
    pl_x, pl_y = 1560, 880
    plt = (f'<rect x="{pl_x-280:.0f}" y="{pl_y-320:.0f}" width="560" height="320"'
           f' rx="14" fill="#cfd6dc" {o(9)}/>')
    plt += (f'<rect x="{pl_x-260:.0f}" y="{pl_y-360:.0f}" width="520" height="54"'
            f' rx="12" fill="#b9c2c8" {o(6)}/>')
    for i in range(4):
        plt += (f'<circle cx="{pl_x-170+i*110:.0f}" cy="{pl_y-150:.0f}" r="22"'
                f' fill="#8a929a" {o(4)}/>')
    for r in range(2):
        for c in range(2):
            plt += (f'<circle cx="{pl_x-150+c*280:.0f}" cy="{pl_y-250+r*70:.0f}"'
                    f' r="46" fill="#9aa3ab" {o(5)}/>')
    s += SL(Z_SRED, plt)
    s += SL(Z_SRED, ogon(pl_x - 150, pl_y - 330, t, .42, .2, 4))
    ch_x, ch_y = pl_x - 150, pl_y - 420
    s += SL(Z_SRED, f'<path d="M{ch_x-110:.0f},{ch_y:.0f} q-16,-120 110,-130'
                    f' q126,10 110,130 Z" fill="url(#zhel)" {o(8)}/>'
                    f'<path d="M{ch_x+100:.0f},{ch_y-80:.0f} q70,-10 56,-70"'
                    f' fill="none" stroke="url(#zhel)" stroke-width="20"'
                    f' stroke-linecap="round"/>'
                    f'<path d="M{ch_x-60:.0f},{ch_y-130:.0f} q60,-70 120,0"'
                    f' fill="none" stroke="{ZHELEZ}" stroke-width="14"/>'
                    f'<rect x="{ch_x-26:.0f}" y="{ch_y-156:.0f}" width="52"'
                    f' height="26" rx="8" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, par(ch_x + 150, ch_y - 150, t, 6, .6, 260, .6, 1.1))
    s += SL(Z_SRED, teplo(pl_x - 150, pl_y - 330, 420, 360, .34 + .1 * abs(A.w(t, 1.4))))
    for i in range(4):                  # газеты на полу
        s += SL(Z_SRED, _gazeta(760 + (i % 2) * 300, 1000 + (i // 2) * 50, 360, 250,
                                -12 + i * 9, 6311 + i))
    tx_, ty_ = 900, 1000
    tab = ten(tx_, ty_ + 14, 150, 22, .45)
    tab += (f'<rect x="{tx_-150:.0f}" y="{ty_-300:.0f}" width="300" height="50"'
            f' rx="14" fill="url(#derev)" {o(8)}/>')
    for dx in (-130, 90):
        tab += (f'<rect x="{tx_+dx:.0f}" y="{ty_-250:.0f}" width="44" height="250"'
                f' rx="12" fill="url(#derev)" {o(6)}/>')
    tab += (f'<rect x="{tx_-130:.0f}" y="{ty_-120:.0f}" width="260" height="22"'
            f' rx="8" fill="{DOSKA2}" {o(4)}/>')
    s += SL(Z_SRED, tab)
    vert = 16 * A.w(t, 1.3, .1)
    s += SL(Z_SRED, f'<g transform="rotate({vert:.1f} {tx_:.0f} {ty_-300:.0f})">'
                    + figura(tx_, ty_ - 290, 560, t, "#eef2f6", "#b9c2c8", False,
                             .2, False, 1.0) + '</g>')
    s += SL(Z_SRED, f'<g transform="rotate({vert:.1f} {tx_:.0f} {ty_-300:.0f})">'
                    f'<path d="M{tx_-180:.0f},{ty_-300:.0f} q180,-120 360,0'
                    f' q-40,40 -180,40 q-140,0 -180,-40 Z" fill="#eef2f6" {o(7)}/>'
                    f'<path d="M{tx_-150:.0f},{ty_-330:.0f} q150,60 300,0"'
                    f' fill="none" stroke="#b9c2c8" stroke-width="9"/></g>')
    for i in range(9):                  # пряди падают на газету
        p = ((t * .55) + i * .11) % 1.0
        s += SL(Z_SRED, f'<path d="M{tx_-120+i*32:.0f},'
                        f'{ty_-480+p*420:.0f} q14,{30+20*p:.0f} -8,{60+30*p:.0f}"'
                        f' fill="none" stroke="#6b4a2a" stroke-width="7"'
                        f' stroke-linecap="round" opacity="{1-p*.5:.2f}"/>')
    nozh_a = -30 + 24 * abs(A.w(t, .7, .2))
    nx_, ny_ = tx_ + 210, ty_ - 480
    s += SL(Z_SRED, f'<g transform="rotate({nozh_a:.0f} {nx_:.0f} {ny_:.0f})">'
                    f'<path d="M{nx_:.0f},{ny_:.0f} l-150,-40 l0,18 l150,36 Z"'
                    f' fill="url(#zhel)" {o(5)}/>'
                    f'<path d="M{nx_:.0f},{ny_+10:.0f} l-150,30 l0,18 l150,-28 Z"'
                    f' fill="url(#zhel)" {o(5)}/>'
                    f'<circle cx="{nx_+20:.0f}" cy="{ny_+8:.0f}" r="12"'
                    f' fill="{ZHELEZ}" {o(3)}/>'
                    f'<path d="M{nx_+30:.0f},{ny_-10:.0f} q60,-30 70,20" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="12"/>'
                    f'<path d="M{nx_+30:.0f},{ny_+26:.0f} q60,30 70,-16" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="12"/></g>')
    ruk, _ = rukav(tx_ + 330, ty_ - 420, 160, 190, t, "#5b2f3a", "#ffd98a", .3, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, figura(tx_ + 430, ty_ + 30, 600, t, "#5b2f3a", "#ffd98a", True, .4))
    for i, mx in enumerate((330, 500)):
        hih = 10 * abs(A.w(t, .9, i * .4))
        s += SL(Z_SRED, f'<g transform="translate(0,{-hih:.1f})">'
                        + figura(mx, 1040, 380 + i * 40, t,
                                 "#4a6a5a" if i else "#6b5a3c", "#ffd98a", False,
                                 i * .5, False, 1.0) + '</g>')
    s += ramka_pp("levo", "#1c1812", .4)
    s += SL(Z_PERED, _vedro(1800, 1070, 1.1, t, False, "#8a929a"))
    s += vinetka(.44)
    return s


# ── 64 ─────────────────────────────────────────────────────────────────────
def chelka_pered_zerkalom(t):
    """Зеркало в ванной на пол-кадра: женщина со спины и её отражение держит
    чёлку, в другой руке ножницы, на стекле листок с записью к мастеру."""
    rnd = random.Random(6421)
    s = f'<rect width="{W}" height="{H}" fill="#56606b"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#6e7a84"/>')
    for r in range(9):
        for c in range(16):
            s += SL(Z_DAL, f'<rect x="{c*122+5:.0f}" y="{r*122+5:.0f}" width="112"'
                           f' height="112" rx="8" fill="#7e8a94" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="0" y="880" width="{W}" height="200" fill="#5d6770" {o(6)}/>')
    rak = (f'<path d="M620,880 q340,-70 680,0 l-30,170 q-310,56 -620,0 Z"'
           f' fill="#eef2f6" {o(9)}/>')
    rak += (f'<ellipse cx="960" cy="900" rx="250" ry="60" fill="#dfe6ea" {o(6)}/>')
    rak += (f'<path d="M940,760 q0,-70 60,-70 q50,0 50,60" fill="none"'
            f' stroke="#b9c2c8" stroke-width="24" stroke-linecap="round"/>')
    rak += (f'<rect x="1030" y="740" width="60" height="26" rx="8" fill="#cfd6dc" {o(4)}/>')
    s += SL(Z_SRED, rak)
    zx, zy, zw, zh = 520, 120, 880, 660
    s += SL(Z_SRED, f'<rect x="{zx-34}" y="{zy-34}" width="{zw+68}" height="{zh+68}"'
                    f' rx="16" fill="#cfd6dc" {o(9)}/>')
    otr = (f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="#9fb6c6"/>')
    otr += (f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="#c9dbe6"'
            f' opacity=".5"/>')
    for r in range(6):                  # отражение кафеля
        otr += (f'<rect x="{zx}" y="{zy+r*110:.0f}" width="{zw}" height="100"'
                f' fill="#aec4d2" opacity=".45"/>')
    fx_ = zx + zw * .60
    otr += figura(fx_, zy + zh + 120, 660, t, "#4a3550", "#ffe6c8", False, .3, False, 1.0)
    chel = 30 * A.w(t, 1.6, .2)
    otr += (f'<path d="M{fx_-96:.0f},{zy+zh-540:.0f} q96,-70 192,0'
            f' q-20,80 -96,{90+chel*.4:.0f} q-76,{-10+chel*.3:.0f} -96,-90 Z"'
            f' fill="#6b4a2a" {o(6)}/>')
    for i in range(7):                  # пряди чёлки
        otr += (f'<path d="M{fx_-80+i*26:.0f},{zy+zh-580:.0f}'
                f' q{6+chel*.2:.1f},70 {-6:.0f},{110+chel*.3:.0f}" fill="none"'
                f' stroke="#8a6534" stroke-width="9" opacity=".9"/>')
    s += SL(Z_SRED, f'<clipPath id="zr64"><rect x="{zx}" y="{zy}" width="{zw}"'
                    f' height="{zh}"/></clipPath><g clip-path="url(#zr64)">{otr}</g>')
    nozh_y = zy + zh - 600 + 40 * A.w(t, 1.3, .1)
    pad = A.out(A.seg(t, 4.6, 1.0))
    nx_ = fx_ + 170
    ny_ = nozh_y + pad * 520
    s += SL(Z_SRED, f'<g transform="rotate({-16+pad*120:.0f} {nx_:.0f} {ny_:.0f})">'
                    f'<path d="M{nx_:.0f},{ny_:.0f} l-10,-120 l20,0 Z"'
                    f' fill="#cfd6dc" {o(4)}/>'
                    f'<path d="M{nx_+22:.0f},{ny_:.0f} l10,-120 l-20,0 Z"'
                    f' fill="#cfd6dc" {o(4)}/>'
                    f'<circle cx="{nx_-10:.0f}" cy="{ny_+30:.0f}" r="24" fill="none"'
                    f' stroke="{KRAS}" stroke-width="11"/>'
                    f'<circle cx="{nx_+34:.0f}" cy="{ny_+30:.0f}" r="24" fill="none"'
                    f' stroke="{KRAS}" stroke-width="11"/></g>')
    s += SL(Z_SRED, f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="none"'
                    f' {o(9)}/>')
    s += SL(Z_SRED, f'<path d="M{zx+60},{zy+50} l240,300" stroke="#ffffff"'
                    f' stroke-width="16" opacity=".22"/>')
    lx_, ly_ = zx + zw - 150, zy + 180
    zach = A.ease(A.seg(t, 2.0, 1.2))
    lst = (f'<g transform="rotate(-7 {lx_:.0f} {ly_:.0f})">'
           f'<rect x="{lx_-120:.0f}" y="{ly_-150:.0f}" width="240" height="300"'
           f' rx="10" fill="url(#list)" {o(6)}/>')
    for i in range(5):
        lst += (f'<path d="M{lx_-90:.0f},{ly_-100+i*50:.0f} q90,8 180,0"'
                f' fill="none" stroke="#7d756a" stroke-width="6" opacity=".8"/>')
    lst += (f'<line x1="{lx_-100:.0f}" y1="{ly_-70:.0f}" x2="{lx_+100*zach-20:.0f}"'
            f' y2="{ly_-40:.0f}" stroke="{KRAS}" stroke-width="11"'
            f' opacity="{zach:.2f}"/>')
    lst += (f'<path d="M{lx_-80:.0f},{ly_+70:.0f} q50,{-30*zach:.0f} 110,{10*zach:.0f}"'
            f' fill="none" stroke="#2f4a7a" stroke-width="8" opacity="{zach:.2f}"/>')
    lst += '</g>'
    s += SL(Z_SRED, lst)
    s += SL(Z_SRED, tusklaya_lampochka(zx + zw * .5, zy - 120, t, 1.0, True))
    s += SL(Z_SRED, teplo(zx + zw * .5, zy - 40, 640, 420, .3 + .1 * abs(A.w(t, 1.6))))
    s += SL(Z_PERED, figura(830, 1320, 780, t, "#2e2238", "#ffd98a", False, .3,
                            False, 1.0))
    pol = (f'<rect x="1500" y="520" width="360" height="26" rx="8"'
           f' fill="#cfd6dc" {o(6)}/>')
    s += SL(Z_SRED, pol)
    s += SL(Z_SRED, svecha(1600, 390, t, .3, 1.3, 120))
    s += SL(Z_SRED, teplo(1610, 360, 420, 380, .36 + .1 * abs(A.w(t, 1.4))))
    s += SL(Z_SRED, f'<path d="M1720,520 q-16,-120 36,-124 q54,4 38,124 Z"'
                    f' fill="url(#stekl)" opacity=".9" {o(5)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{1736+i*8:.0f}" y="{400-i*10:.0f}" width="10"'
                        f' height="90" rx="4" fill="#cfd6dc" {o(2)}/>')
    zak = A.ease(A.seg(t, 5.6, .9))
    s += SL(Z_SRED, f'<g transform="translate(0,{zak*40:.0f})">'
                    f'<path d="M200,700 q80,-40 160,0 q-80,30 -160,0 Z"'
                    f' fill="{KRAS}" {o(5)}/>'
                    f'<rect x="196" y="{698-10*(1-zak):.0f}" width="170" height="16"'
                    f' rx="7" fill="#8f2f33" {o(3)}/></g>')
    s += ramka_pp("levo", "#1a2028", .4)
    s += vinetka(.44)
    return s


# ── 65 ─────────────────────────────────────────────────────────────────────
def hozyain_obhodit_izbu_s_molotkom(t):
    """Белый дневной свет: хозяин в переднике с молотком и ящиком гвоздей
    обходит избу снаружи, подбивает ставню, в щель уходит пакля."""
    rnd = random.Random(6521)
    s = f'<rect width="{W}" height="{H}" fill="#b9c6cf"/>'
    s += nebo("den", t, False, 6529)
    s += oblaka(t, 190, 5, 6547, .5, "#f2f6fa", 11.0)
    s += ulica_dal(1300, 680, 620, t, False, 6551)
    s += SL(Z_DAL, gryaz_polosa(840, 200, "#6b5a46"))
    izb = brevna(60, 180, 1500, 700, 112)
    izb += (f'<path d="M20,190 L810,-110 L1600,190 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="1180" y="-150" width="110" height="220" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(1236, -140, t, 5, .2, 300, .3, "#dfe6ec", 1.0))
    for i, ox in enumerate((220, 1120)):
        s += SL(Z_SRED, okno_izby(ox, 420, 300, 230, t, None, .0, i == 1, True))
        s += SL(Z_SRED, f'<path d="M{ox-40:.0f},402 h380 l-30,-48 h-320 Z"'
                        f' fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, teplo(1270, 530, 320, 280, .3 + .1 * abs(A.w(t, 1.8))))
    stv_x, stv_y = 980, 410
    bit = abs(A.w(t, .9, .1))
    s += SL(Z_SRED, f'<g transform="rotate({-4+3*bit:.1f} {stv_x:.0f} {stv_y:.0f})">'
                    f'<rect x="{stv_x:.0f}" y="{stv_y:.0f}" width="190" height="300"'
                    f' rx="8" fill="url(#dosk)" {o(8)}/>'
                    + "".join(f'<rect x="{stv_x+10+j*60:.0f}" y="{stv_y+8:.0f}"'
                              f' width="50" height="284" rx="6" fill="url(#dosk)"'
                              f' {o(4)}/>' for j in range(3))
                    + f'<path d="M{stv_x+30:.0f},{stv_y+80:.0f} q65,-40 130,0"'
                    f' fill="none" stroke="{MED}" stroke-width="10"/></g>')
    mx_, my_ = stv_x + 250, stv_y + 110
    mol_a = -50 + 60 * bit
    s += SL(Z_SRED, f'<g transform="rotate({mol_a:.0f} {mx_:.0f} {my_+150:.0f})">'
                    f'<rect x="{mx_-12:.0f}" y="{my_:.0f}" width="26" height="190"'
                    f' rx="9" fill="url(#derev)" {o(5)}/>'
                    f'<rect x="{mx_-56:.0f}" y="{my_-54:.0f}" width="112" height="58"'
                    f' rx="10" fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{mx_+56:.0f},{my_-44:.0f} q40,20 0,40 Z"'
                    f' fill="{ZHELEZ}" {o(4)}/></g>')
    hx = 760
    s += SL(Z_SRED, figura(hx, 980, 600, t, "#4a3a2c", "#ffd0a0", False, .2, True,
                           1.0, False, 1.2, True, True))
    s += SL(Z_SRED, f'<path d="M{hx-96:.0f},{980-330:.0f} q96,-30 192,0 l-16,300'
                    f' q-80,26 -160,0 Z" fill="#c9bda4" opacity=".95" {o(6)}/>')
    ruk, _ = rukav(hx + 80, 640, 170, -22, t, "#4a3a2c", "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    yx_ = hx + 150
    s += SL(Z_SRED, f'<rect x="{yx_:.0f}" y="880" width="220" height="140" rx="10"'
                    f' fill="url(#derev)" {o(7)}/>'
                    f'<path d="M{yx_+20:.0f},880 q90,-60 180,0" fill="none"'
                    f' stroke="url(#derev)" stroke-width="14"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{yx_+30+i*26:.0f},890 l0,40 l6,16 l6,-16 l0,-40 Z"'
                        f' fill="{ZHELEZ}" {o(3)}/>')
    pak_x = 560
    for i in range(7):
        p = A.ease(A.seg(t, .4 + i * .18, .8))
        s += SL(Z_SRED, f'<path d="M{pak_x+i*8:.0f},{520-p*40:.0f}'
                        f' q{20-10*p:.0f},40 {-6:.0f},{70-20*p:.0f}" fill="none"'
                        f' stroke="#d8c8a4" stroke-width="{14-6*p:.0f}"'
                        f' stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M540,560 h120 l0,16 h-120 Z" fill="#3a2a1c"'
                    f' opacity=".9"/>')
    zx_ = 1620
    s += SL(Z_SRED, figura(zx_, 1030, 520, t, "#8f3a42", "#ffd0a0", True, .5, True))
    mel_y = 700 - abs(A.w(t, .8, .2)) * 90
    ruk2, (ax, ay) = rukav(zx_ - 90, 740, 140, 200, t, "#8f3a42", "#ffd0a0", .3, 5.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="30" ry="22"'
                    f' fill="#e3c6a8" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{ax-24:.0f}" y="{mel_y:.0f}" width="48" height="60"'
                    f' rx="10" fill="#f6f2e6" {o(5)}/>')
    for i in range(4):
        s += SL(Z_SRED, kura(420 + i * 150, 1040 - (i % 2) * 20, t,
                             .85 + .1 * (i % 2), i * .25))
    s += SL(Z_PERED, pleten(-40, 1080, 420, 200, 6))
    s += SL(Z_PERED, _korzina(1850, 1080, 250, 190, t, 6553, False))
    s += vinetka(.4)
    return s


# ── 66 ─────────────────────────────────────────────────────────────────────
def mel_nad_oknom(t):
    """Хозяйка встаёт на лавку у окна и тянется куском мела к бревну над
    наличником: двумя взмахами ставит метку и сдувает крошки."""
    rnd = random.Random(6607)
    s = sumerki_fon(t, False)
    s += ulica_dal(1340, 700, 580, t, False, 6619)
    s += SL(Z_DAL, gryaz_polosa(830, 190, "#5a4c3a"))
    izb = brevna(0, 60, 1400, 820, 116)
    izb += (f'<path d="M-40,70 L680,-190 L1400,70 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="1000" y="-220" width="110" height="240" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(1056, -210, t, 5, .22, 320, .32, "#cdd7e4", 1.0))
    ox, oy, ow, oh = 420, 420, 520, 400
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#2a1d12"/>')
    za += teplo(ox + ow * .5, oy + oh * .6, 360, 300, .62)
    za += lampa(ox + ow * .34, oy + oh * .74, t, .62)
    za += figura(ox + ow * .74, oy + oh + 10, 330, t, "#4a3140", "#ffd98a", True, .4, True)
    s += SL(Z_SRED, f'<clipPath id="ok66"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok66)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .12, False, True))
    nal = (f'<path d="M{ox-80:.0f},{oy-40:.0f} h{ow+160:.0f} l-50,-72'
           f' h{-ow-60:.0f} Z" fill="url(#derev)" {o(8)}/>')
    for i in range(7):
        nal += (f'<path d="M{ox-50+i*96:.0f},{oy-46:.0f} l32,-24 l32,24 Z"'
                f' fill="{MED}" opacity=".9" {o(3)}/>')
    for sgn in (-1, 1):
        nal += (f'<rect x="{ox+(0 if sgn<0 else ow)-(54 if sgn<0 else 0):.0f}"'
                f' y="{oy-30:.0f}" width="54" height="{oh+60:.0f}" rx="8"'
                f' fill="url(#dosk)" {o(6)}/>')
    s += SL(Z_SRED, nal)
    s += SL(Z_SRED, teplo(ox + ow * .5, oy + oh * .5, 460, 400, .3 + .1 * abs(A.w(t, 1.7))))
    lv_x, lv_y = 640, 1010
    s += SL(Z_SRED, lavka(lv_x - 230, lv_y, 480))
    skrip = 1.4 * A.w(t, 1.1, .2)
    hx = lv_x
    s += SL(Z_SRED, f'<g transform="rotate({skrip:.2f} {hx:.0f} {lv_y:.0f})">'
                    + figura(hx, lv_y, 560, t, "#8f3a42", "#ffd98a", True, .2, True)
                    + '</g>')
    vzm = abs(A.w(t, .8, .1))
    ruk, (mx, my) = rukav(hx + 160, lv_y - 400, 230, -78 - 14 * vzm, t,
                          "#8f3a42", "#ffd98a", .2, 7.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="30" ry="24"'
                    f' fill="#e3c6a8" {o(4)}/>'
                    f'<rect x="{mx-18:.0f}" y="{my-56:.0f}" width="36" height="56"'
                    f' rx="10" fill="#f6f2e6" {o(5)}/>')
    metka = A.ease(A.seg(t, .5, 1.2))
    s += SL(Z_SRED, f'<g opacity="{metka:.2f}">'
                    f'<path d="M{ox+140:.0f},{oy-130:.0f} l70,90" stroke="#f6f2e6"'
                    f' stroke-width="16" stroke-linecap="round"/>'
                    f'<path d="M{ox+230:.0f},{oy-134:.0f} l-66,94" stroke="#f6f2e6"'
                    f' stroke-width="16" stroke-linecap="round"/></g>')
    s += SL(Z_SRED, teplo(ox + 190, oy - 90, 260, 200, .22 * metka))
    for i in range(10):                 # крошки мела сыплются
        p = ((t * .6) + i * .1) % 1.0
        s += SL(Z_SRED, f'<circle cx="{ox+150+i*12+16*A.w(t,2.4,i*.2):.0f}"'
                        f' cy="{oy-100+p*260:.0f}" r="{4+3*(1-p):.1f}"'
                        f' fill="#f6f2e6" opacity="{(1-p)*.8:.2f}"/>')
    sdu = A.seg(t, 1.8, .6)
    if sdu > .02 and sdu < .98:
        s += SL(Z_SRED, par(ox + 230, oy - 120, t, 4, .5, 150, 1.2, .8))
    dvx, dvy, dvw, dvh = 1120, 480, 260, 400
    s += SL(Z_SRED, dver(dvx, dvy, dvw, dvh, .0, "url(#derev)", True, False))
    s += SL(Z_SRED, podkova(dvx + dvw * .5, dvy - 60, .8, t))
    s += SL(Z_SRED, f'<path d="M{dvx-60:.0f},{dvy+dvh:.0f} h{dvw+120:.0f}'
                    f' l-30,60 h{-dvw-60:.0f} Z" fill="url(#dosk)" {o(7)}/>')
    s += SL(Z_SRED, kura(1500, 1000, t, .9, .2))
    s += SL(Z_SRED, kura(1640, 1030, t, .8, .6))
    s += SL(Z_PERED, goloe_derevo(1800, 1080, 620, t, 6637, 8, "#2a2b33"))
    s += ramka_pp("levo", "#1a140c", .4)
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 6653, .36, .8))
    s += vinetka(.44)
    return s


# ── 67 ─────────────────────────────────────────────────────────────────────
def serp_na_stavne(t):
    """Расписная ставня на пол-кадра: хозяин вешает на гвоздь большой
    блестящий серп, а на соседнюю ставню — кованую железку."""
    rnd = random.Random(6701)
    s = sumerki_fon(t, True)
    s += ulica_dal(1300, 720, 620, t, False, 6703)
    s += SL(Z_DAL, gryaz_polosa(850, 190, "#473c30"))
    s += SL(Z_DAL, brevna(0, 0, W, 900, 116))
    ox, oy, ow, oh = 620, 250, 440, 400
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#2a1d12"/>')
    sv_on = A.ease(A.seg(t, 2.6, 1.0))
    za += teplo(ox + ow * .5, oy + oh * .6, 340, 300, .7 * sv_on + .1)
    za += lampa(ox + ow * .4, oy + oh * .8, t, .56 * sv_on + .2)
    s += SL(Z_SRED, f'<clipPath id="ok67"><rect x="{ox}" y="{oy}" width="{ow}"'
                    f' height="{oh}"/></clipPath><g clip-path="url(#ok67)">{za}</g>')
    s += SL(Z_SRED, okno_izby(ox, oy, ow, oh, t, None, .15, False, True))
    for i, sgn in enumerate((-1, 1)):
        kach = 2.6 * sgn * A.w(t, 2.8, .2 + i * .3)
        sx_ = ox + (0 if sgn < 0 else ow)
        stv = f'<g transform="rotate({kach:.2f} {sx_:.0f} {oy-20:.0f})">'
        stv += (f'<rect x="{sx_-(300 if sgn<0 else 0):.0f}" y="{oy-30:.0f}"'
                f' width="300" height="{oh+60:.0f}" rx="10" fill="url(#dosk)" {o(9)}/>')
        for j in range(3):
            stv += (f'<rect x="{sx_-(290 if sgn<0 else -10)+j*94:.0f}"'
                    f' y="{oy-20:.0f}" width="84" height="{oh+40:.0f}" rx="8"'
                    f' fill="url(#dosk)" {o(5)}/>')
        bx_ = sx_ - (150 if sgn < 0 else -150)
        for j in range(3):              # роспись по ставне
            stv += (f'<circle cx="{bx_:.0f}" cy="{oy+80+j*140:.0f}" r="34"'
                    f' fill="{[KRAS, ZOL, ZEL2][j]}" opacity=".45" {o(3)}/>')
            stv += (f'<path d="M{bx_-70:.0f},{oy+80+j*140:.0f} q70,-50 140,0'
                    f' q-70,50 -140,0 Z" fill="none" stroke="{KREM}"'
                    f' stroke-width="8" opacity=".8"/>')
        stv += '</g>'
        s += SL(Z_SRED, stv)
    nx_, ny_ = 330, 360
    s += SL(Z_SRED, f'<circle cx="{nx_:.0f}" cy="{ny_:.0f}" r="16" fill="{ZHELEZ}" {o(5)}/>')
    ves = A.out(A.seg(t, .4, 1.2))
    kach2 = (1 - ves) * 0 + 7 * A.w(t, 1.9, .1) * ves
    serp = f'<g transform="rotate({kach2:.1f} {nx_:.0f} {ny_:.0f}) translate(0,{(1-ves)*-180:.0f})">'
    serp += (f'<path d="M{nx_:.0f},{ny_:.0f} q300,70 330,430 q-100,-300 -354,-350 Z"'
             f' fill="#dfe8ee" {o(9)}/>')
    serp += (f'<path d="M{nx_+20:.0f},{ny_+16:.0f} q270,80 300,380" fill="none"'
             f' stroke="#8a929a" stroke-width="8" opacity=".8"/>')
    serp += (f'<path d="M{nx_+10:.0f},{ny_+20:.0f} q200,70 230,300" fill="none"'
             f' stroke="#eef4f8" stroke-width="12"'
             f' opacity="{.4+.4*abs(A.w(t,2.2,.1)):.2f}"/>')
    for i in range(9):                  # зубцы серпа
        k = i / 8.0
        serp += (f'<path d="M{nx_+40+k*190:.0f},{ny_+40+k*230:.0f} l18,-14 l4,22 Z"'
                 f' fill="#eef4f8" opacity=".75"/>')
    serp += (f'<g transform="rotate(-24 {nx_:.0f} {ny_:.0f})">'
             f'<rect x="{nx_-170:.0f}" y="{ny_-34:.0f}" width="180" height="66"'
             f' rx="22" fill="url(#derev)" {o(8)}/>'
             f'<rect x="{nx_-178:.0f}" y="{ny_-40:.0f}" width="34" height="78"'
             f' rx="12" fill="{DOSKA2}" {o(6)}/></g>')
    serp += '</g>'
    s += SL(Z_SRED, serp)
    s += SL(Z_SRED, teplo(nx_ + 120, ny_ + 180, 360, 320, .22 + .1 * abs(A.w(t, 1.8))))
    zay = ((t * .4) % 1.0)              # зайчик от серпа бежит по двору
    s += SL(Z_SRED, f'<ellipse cx="{200+zay*1500:.0f}" cy="{960-abs(math.sin(zay*6))*60:.0f}"'
                    f' rx="60" ry="26" fill="{SVET}" opacity="{.5-.2*zay:.2f}"/>')
    pod = A.ease(A.seg(t, 1.6, 1.2))
    sx_ = 1520
    s += SL(Z_SRED, figura(sx_, 1040, 470, t, "#3c4656", "#cfe4f5", False, .6, True,
                           1.0, False, 1.2, False, True))
    ruk, (ax, ay) = rukav(sx_ - 90, 740, 190 - 40 * pod, 196 - 20 * pod, t,
                          "#3c4656", "#cfe4f5", .3, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<path d="M{ax-80:.0f},{ay-20:.0f} q40,-40 90,-10'
                    f' q50,30 10,80 q-50,30 -100,-70 Z" fill="{ZHELEZ}" {o(6)}/>')
    hx_ = 1140
    s += SL(Z_SRED, figura(hx_, 1020, 580, t, "#4a3a2c", "#ffd98a", False, .2, True,
                           1.0, True, 1.0, True, True))
    ruk2, _ = rukav(hx_ - 110, 660, 190, 184, t, "#4a3a2c", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, para_izo_rta(hx_ + 50, 560, t, .2, 1.1, .5))
    fnx, fny = 150, 180
    s += SL(Z_SRED, f'<path d="M{fnx-60:.0f},{fny:.0f} h120 l-14,-32 h-92 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-50:.0f},{fny:.0f} h100 l-12,118 h-76 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 108, t, .54, .3, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 70, 320, 290, .4 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_PERED, pleten(1240, 1080, 680, 220, 8))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 6709, .44, .9))
    s += vinetka(.46)
    return s


# ── 68 ─────────────────────────────────────────────────────────────────────
def ryabina_u_vhoda(t):
    """Крыльцо и распахнутая дверь сеней на пол-кадра: в дверном проёме
    рябина в гроздьях, девочка несёт кисти, на перилах сидит синица."""
    rnd = random.Random(6803)
    s = sumerki_fon(t, True)
    s += ulica_dal(1420, 740, 500, t, False, 6823)
    s += SL(Z_DAL, gryaz_polosa(860, 190, "#4a3e30"))
    izb = brevna(80, 60, 1500, 860, 116)
    izb += (f'<path d="M40,70 L820,-200 L1600,70 Z" fill="{DOSKA2}" {o(9)}/>')
    izb += (f'<rect x="1220" y="-230" width="110" height="250" fill="url(#kamen)" {o(6)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(1276, -220, t, 5, .22, 320, .32, "#cdd7e4", 1.0))
    px, py, pw, ph_ = 500, 220, 800, 760
    put = kontur_proema(px, py, pw, ph_, "arka")
    vid = f'<clipPath id="st68"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#2a2016"/>'
    za = (f'<rect x="{px}" y="{py}" width="{pw}" height="{ph_}" fill="#3a4a3a"/>')
    za += (f'<rect x="{px}" y="{py+ph_*.62:.0f}" width="{pw}" height="{ph_*.38:.0f}"'
           f' fill="#4a4030"/>')
    za += goloe_derevo(px + pw * .5, py + ph_, 620, t, 6827, 9, "#4a3a2a")
    for i in range(9):                  # нарисованная рябина в проёме
        a = -2.4 + i * .5
        gx_ = px + pw * .5 + math.cos(a) * pw * .28
        gy_ = py + ph_ * .42 + math.sin(a) * ph_ * .22
        za += grozd_ryabiny(gx_, gy_, t, .95, 13, 6829 + i, i * .13)
        for j in range(4):              # листья
            za += (f'<ellipse cx="{gx_-60+j*34:.0f}" cy="{gy_+60+((j%2)*18):.0f}"'
                   f' rx="24" ry="11" fill="#7a6a2a"'
                   f' transform="rotate({-20+j*14} {gx_-60+j*34:.0f}'
                   f' {gy_+60+((j%2)*18):.0f})" {o(3)}/>')
    vid += f'<g clip-path="url(#st68)">{za}</g>'
    vid += mesto_stoka(px, py, pw, ph_, "arka")
    ob = (f'<path d="{put}" fill="none" stroke="url(#derev)" stroke-width="86"/>')
    ob += (f'<path d="{put}" fill="none" {o(9)}/>')
    ob += (f'<path d="M{px-120:.0f},{py+ph_*.38:.0f} h{pw+240:.0f}" stroke="url(#dosk)"'
           f' stroke-width="0" fill="none"/>')
    for sgn in (-1, 1):                 # наличники по бокам проёма
        bx_ = px + (0 if sgn < 0 else pw)
        ob += (f'<rect x="{bx_-(96 if sgn<0 else 0):.0f}" y="{py+pw*.5-40:.0f}"'
               f' width="96" height="{ph_-pw*.5+40:.0f}" rx="10" fill="url(#dosk)"'
               f' {o(8)}/>')
        for j in range(4):
            ob += (f'<path d="M{bx_-(76 if sgn<0 else -20):.0f},'
                   f'{py+pw*.5+40+j*130:.0f} q28,46 0,92" fill="none"'
                   f' stroke="#5a3a22" stroke-width="9" opacity=".7"/>')
    ob += (f'<path d="M{px-150:.0f},{py-30:.0f} q{pw*.5+150:.0f},-180'
           f' {pw+300:.0f},0 l-60,-70 q{-pw*.5-120:.0f},-150 {-pw-180:.0f},0 Z"'
           f' fill="{DOSKA2}" {o(8)}/>')
    for i in range(9):
        ob += (f'<path d="M{px-110+i*(pw+220)/8:.0f},{py-70:.0f} l30,-26 l30,26 Z"'
               f' fill="{MED}" opacity=".9" {o(3)}/>')
    vid += ob
    s += SL(Z_SRED, vid)
    s += SL(Z_SRED, teplo(px + pw * .5, py + ph_ + 80, 560, 240, .26))
    kr = (f'<path d="M{px-180:.0f},{py+ph_:.0f} h{pw+360:.0f} l60,70'
          f' h{-pw-480:.0f} Z" fill="url(#dosk)" {o(9)}/>')
    for i in range(3):
        kr += (f'<rect x="{px-160+i*20:.0f}" y="{py+ph_+70+i*42:.0f}"'
               f' width="{pw+320-i*40:.0f}" height="38" rx="8" fill="url(#dosk)" {o(5)}/>')
    s += SL(Z_SRED, kr)
    stx = px + pw + 190
    s += SL(Z_SRED, f'<rect x="{stx-28:.0f}" y="{py-130:.0f}" width="56"'
                    f' height="{ph_+280:.0f}" rx="12" fill="url(#derev)" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="{stx-130:.0f}" y="{py+ph_-120:.0f}" width="260"'
                    f' height="26" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, ptica(stx + 90, py + ph_ - 130, t, 1.2, KRAS, .2, "#5b6a78"))
    for i in range(3):                  # гроздья на столбе, качаются на лыке
        kach = 4.0 * A.w(t, 2.4, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {stx:.0f} {py-60+i*40:.0f})">'
                        f'<path d="M{stx:.0f},{py-60+i*40:.0f} q20,70 6,130"'
                        f' fill="none" stroke="#b9a884" stroke-width="9"/>'
                        + grozd_ryabiny(stx + 14, py + 120 + i * 60, t, .9, 12,
                                        6841 + i, i * .2) + '</g>')
    lyk = A.ease(A.seg(t, 1.2, 1.2))
    s += SL(Z_SRED, f'<path d="M{stx-50:.0f},{py-40:.0f} q50,{-30+20*lyk:.0f}'
                    f' 100,0 q{-40*lyk:.0f},30 {-100*lyk:.0f},10" fill="none"'
                    f' stroke="#d8c8a4" stroke-width="11" stroke-linecap="round"/>')
    dx_ = 300
    s += SL(Z_SRED, figura(dx_, 1050, 430, t, "#5b2f3a", "#ffd98a", True, .4, True))
    ruk, (ax, ay) = rukav(dx_ + 90, 800, 150, -34 + 14 * A.w(t, 1.3), t,
                          "#5b2f3a", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, grozd_ryabiny(ax + 30, ay + 40, t, 1.1, 15, 6857, .1))
    s += SL(Z_SRED, para_izo_rta(dx_ + 40, 720, t, .3, 1.0, .5))
    fnx, fny = 1700, 330
    s += SL(Z_SRED, f'<rect x="{fnx-16:.0f}" y="60" width="32" height="600"'
                    f' fill="url(#derev)" {o(7)}/>'
                    f'<path d="M{fnx-62:.0f},{fny:.0f} h124 l-14,-34 h-96 Z"'
                    f' fill="{ZHELEZ}" {o(6)}/>'
                    f'<path d="M{fnx-52:.0f},{fny:.0f} h104 l-12,124 h-80 Z"'
                    f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    s += SL(Z_SRED, ogon(fnx, fny + 112, t, .58, .2, 5))
    s += SL(Z_SRED, teplo(fnx, fny + 70, 340, 300, .42 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_PERED, _korzina(160, 1080, 240, 190, t, 6863, False))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 6869, .4, .85))
    s += vinetka(.46)
    return s
