# -*- coding: utf-8 -*-
"""Декорации 69-121 ролика «Что дарить на Новый год 2027» (37 деклараций,
планы 69-121 по первому упоминанию — не все числа внутри диапазона заняты,
часть декораций между ними уже написана в chast1.py/chast2.py)."""
import math, random
from baza import *
import anim as A
from lok_obshchee import (figura, rukav, siluet, mokryy_sneg, goloe_derevo,
                           gryaz_polosa, para_izo_rta, sumerki_fon,
                           grozd_ryabiny, tusklaya_lampochka, kirpich_ustya,
                           luchina, podkova)
from chast1 import (_korobka, _svertok, _varezhka, _banka, _svistulka,
                     _oblachko, _chasy_sten, _chasy_karman, _servant,
                     _shkaf_proem, _zapret, _galochka, _koshelek, _elka,
                     _napolnenie, _chertenok, _vesy, _kovrik_pol,
                     _kartiny_ryad, _oboi_fon, _nozh_bolshoy, _nozhnicy_bolshie,
                     _veshalka_seni, _koza_hozyayka)
from chast2 import _samovar, _primeta_vorona, _schyoty


# ───────────────────────── МЕСТНЫЕ КИРПИЧИКИ ПОРЦИИ ─────────────────────────
def _oblako_rechi(x, y, s_, t, ph, nastroenie):
    """Облачко-реакция над подарком: grust/pusto/radost."""
    rise = 8 * A.w(t, 1.6, ph)
    s = (f'<ellipse cx="{x:.0f}" cy="{y+rise:.0f}" rx="{64*s_:.0f}" ry="{42*s_:.0f}"'
         f' fill="#ffffff" opacity=".92" {o(4)}/>')
    s += (f'<circle cx="{x-50*s_:.0f}" cy="{y+28*s_+rise:.0f}" r="{10*s_:.0f}" fill="#ffffff" opacity=".9" {o(2)}/>')
    cy_ = y + rise
    if nastroenie == "grust":
        s += f'<ellipse cx="{x:.0f}" cy="{cy_-4*s_:.0f}" rx="{14*s_:.0f}" ry="{18*s_:.0f}" fill="#6f7f8c" opacity=".8"/>'
        s += f'<path d="M{x-10*s_:.0f},{cy_+16*s_:.0f} q4,{10*s_:.0f} 0,{18*s_:.0f}" fill="none" stroke="{STEKLO}" stroke-width="3"/>'
    elif nastroenie == "pusto":
        s += f'<line x1="{x-16*s_:.0f}" y1="{cy_:.0f}" x2="{x+16*s_:.0f}" y2="{cy_:.0f}" stroke="{K}" stroke-width="3" stroke-dasharray="4 5" opacity=".5"/>'
    else:
        s += f'<circle cx="{x:.0f}" cy="{cy_-2*s_:.0f}" r="{14*s_:.0f}" fill="{SVET}" {o(2)}/>'
        s += f'<path d="M{x-16*s_:.0f},{cy_+16*s_:.0f} l{32*s_:.0f},0 l{-16*s_:.0f},{16*s_:.0f} Z" fill="#6b4428" {o(2)}/>'
        s += f'<path d="M{x-6*s_:.0f},{cy_-2*s_:.0f} q6,8 12,0" fill="none" stroke={K!r}/>'.replace("={K!r}", f'="{K}" stroke-width="2"')
    return s


def _olenok(x, y, h_, t):
    """Молодой олень (детская игрушка/силуэт) — не используется, резерв."""
    return ""


# ═══════════════════════════ 69-73 ══════════════════════════════
def pustoe_napolnyayut(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 73)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 740, 1200, 34))
    s += SL(Z_SRED, f'<ellipse cx="760" cy="720" rx="110" ry="30" fill="{CHUGUN}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M650,720 q110,-50 220,0" fill="none" stroke={K!r}'.replace("={K!r}", f'="{K}"') + ' stroke-width="4" opacity=".4"/>')
    s += SL(Z_SRED, _korobka(760, 660, 40, 24, t, KRAS, ZOL, True, .2))
    s += SL(Z_SRED, _koshelek(1140, 740, 1.4, True, 0))
    bounce = abs(math.sin(t * 2.6))
    mx, my = 940, 700 - bounce * 80
    s += SL(Z_SRED, f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="16" fill="url(#zol)" {o(2)}/>')
    sypet = A.ease(A.seg(t % 4.0, 2.0, 1.6))
    for i in range(int(6 * sypet)):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<circle cx="{700+rnd.random()*120:.0f}" cy="{700-rnd.random()*20:.0f}" r="18" fill="{ZOL}" {o(2)}/>')
    if sypet > .3:
        s += SL(Z_SRED, f'<rect x="1090" y="700" width="90" height="36" rx="4" fill="{ZEL2}" opacity="{sypet:.2f}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M500,690 q30,-20 60,0" fill="none" stroke="{MED}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="400" y="700" width="120" height="30" rx="6" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1400,690 q-10,-60 30,-70 q40,10 30,70 Z" fill="url(#zol)" {o(3)}/>')
    s += SL(Z_SRED, par(1340, 660, t, 3, .4, 70))
    ruk1, (r1x, r1y) = rukav(820, 560, 180, 100, t, "#5a4a3a", KREM, .0, 4)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def meloch_na_prazdnichnyy_vecher(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 74)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(260, 760, 1400, 36))
    s += SL(Z_SRED, f'<rect x="700" y="640" width="280" height="40" rx="8" fill="{TKAN}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M900,700 l-30,70 l50,0 Z" fill="{KREM}" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, svecha(400 + i * 60, 700, t, i * .2, .9))
    s += SL(Z_SRED, f'<ellipse cx="620" cy="700" rx="80" ry="24" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1200,660 v60" stroke="{STEKLO}" stroke-width="40" opacity=".7"/>')
    bx, by = 1500, 760
    s += SL(Z_SRED, f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="230" ry="60" fill="{POBEL}" {o(4)}/>')
    put = kontur_proema(bx - 190, by - 160, 380, 320, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(bx - 190, by - 160, 380, 320, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(5)}/>')
    s += SL(Z_SRED, figura(900, 1040, 480, t, "#6b4a3a", KREM, False, .0))
    sypet = A.seg(t % 3.0, 0, 2.2)
    ruk1, (r1x, r1y) = rukav(960, 760, 150, -40, t, "#6b4a3a", KREM, .0, 4)
    s += SL(Z_SRED, ruk1)
    for i in range(5):
        fall = A.ease(A.seg(t % 3.0, i * .3, .5))
        s += SL(Z_SRED, f'<circle cx="{r1x-10+i*8:.0f}" cy="{r1y+20+(1-fall)*(-60):.0f}" r="7" fill="{(ZOL,MED)[i%2]}" opacity="{.4+.6*fall:.2f}"/>')
    ruk2, (r2x, r2y) = rukav(840, 760, 150, -140, t, "#6b4a3a", KREM, .3, 3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<rect x="{r2x-20:.0f}" y="{r2y-10:.0f}" width="60" height="50" fill="{DOSKA}" opacity=".9" {o(2)}/>')
    carm = 4 * A.w(t, 1.1)
    s += SL(Z_SRED, f'<path d="M{r1x+carm:.0f},{r1y+30:.0f} q16,30 -6,{40+carm:.0f}" fill="none" stroke="{DOSKA}" stroke-width="6" opacity=".6"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def kopeechka_chtoby_ne_possoritsya(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 75)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    okvid = _primeta_vorona(0, 0, .6, t, min(1.0, A.ease(A.seg(t, 1.6, 1.0))))
    s += SL(Z_DAL, okno_izby(1500, 160, 280, 240, t, vid=f'<g transform="translate(160,170)">{okvid}</g>', svet=False, moroz=.2))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 760, 900, 34))
    s += SL(Z_SRED, _samovar(500, 740, .8, t))
    s += SL(Z_SRED, f'<ellipse cx="800" cy="720" rx="90" ry="28" fill="{MED}" {o(3)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{700+i*22}" cy="700" r="12" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1040" cy="712" rx="60" ry="20" fill="{STEKLO}" opacity=".6" {o(2)}/>')
    s += SL(Z_SRED, hodiki(1650, 320, t, 1.0))
    s += SL(Z_SRED, figura(560, 1020, 460, t, "#5a5560", KREM, True, .0))
    ruk1, (r1x, r1y) = rukav(640, 780, 140, -40, t, "#5a5560", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, _varezhka(r1x + 10, r1y + 10, 1.3, 0, KRAS))
    s += SL(Z_SRED, _nozhnicy_bolshie(r1x + 10, r1y - 20, 70, t))
    s += SL(Z_SRED, figura(900, 1020, 460, t, "#8c6a3a", KREM, False, .3))
    hohot = abs(A.w(t, .7)) > .6
    ruk2, (r2x, r2y) = rukav(840, 780, 140, -150 - (10 if hohot else 0), t, "#8c6a3a", KREM, .3, 4)
    s += SL(Z_SRED, ruk2)
    moneta_t = A.ease(A.seg(t, 1.2, .6))
    s += SL(Z_SRED, f'<circle cx="{r2x-10*moneta_t:.0f}" cy="{r2y+10*moneta_t:.0f}" r="14" fill="url(#med)" opacity="{moneta_t:.2f}" {o(2)}/>')
    s += SL(Z_SRED, svecha(597, 853, t, 1.33, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def ognennaya_koza_s_meshkom_podarkov(t):
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += SL(Z_NEBO, teplo(960, 300, 900, 500, .5))
    s += SL(Z_DAL, izba_snaruzhi(260, 940, 460, t, True, True, 17))
    s += SL(Z_DAL, _elka(1680, 960, 480, t, 19))
    s += SL(Z_SRED, sneg_lezhit(880))
    s += SL(Z_SRED, f'<path d="M1500,900 l60,-150 l60,150 Z" fill="{SNEG}" {o(3)}/><ellipse cx="1560" cy="900" rx="40" ry="14" fill="{SNEG}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1300" y="820" width="140" height="80" rx="10" fill="{ZHELEZ}" {o(3)}/><circle cx="1370" cy="800" r="40" fill="{SVET}" opacity=".8"/>')
    kx, ky = 900, 880
    s += SL(Z_SRED, _koza_hozyayka(kx, ky, 460, t))
    mesh_sw = 6 * A.w(t, 1.1)
    mx = kx + 160 + mesh_sw
    s += SL(Z_SRED, f'<path d="M{mx:.0f},{ky-220:.0f} q60,10 50,110 q-10,70 -60,70 q-50,0 -56,-70 q-6,-100 66,-110 Z" fill="#6b3a26" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{mx+30:.0f},{ky-230:.0f} l40,-30" stroke="{ZHELEZ}" stroke-width="5"/>')
    for i, (dx, col) in enumerate([(-10, TKAN2), (20, MED), (-25, ZEL2), (10, KRAS)]):
        s += SL(Z_SRED, f'<rect x="{mx+dx:.0f}" y="{ky-240-i*6:.0f}" width="26" height="18" rx="4" fill="{col}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M{mx-30:.0f},{ky-250:.0f} l10,-20 l10,20 Z" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#1a0e08", .3))
    s += SL(Z_LETIT, sneg_letit(t, 18, 29, .5, .8))
    s += vinetka(.38)
    return s


# ═══════════════════════════ 74-81 ══════════════════════════════
def krasnyy_konvert(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a1618"/>'
    s += SL(Z_DAL, teplo(960, 460, 1100, 760, .55))
    s += SL(Z_DAL, lampa(960, 220, t, 1.2, True))
    s += SL(Z_SRED, f'<path d="M1500,900 q-80,-200 -160,-260" stroke="#2a1a16" stroke-width="16" fill="none"/>')
    s += SL(Z_SRED, f'<rect x="1500" y="640" width="200" height="130" rx="30" fill="{KRAS}" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1600" cy="700" rx="30" ry="40" fill="{ZOL}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="300" cy="760" rx="120" ry="34" fill="{KREM}" {o(3)}/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{220+i*28}" cy="750" r="12" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1150" y="700" width="60" height="90" rx="8" fill="{KAMEN}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1180,690 q20,-10 30,-30" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    s += SL(Z_SRED, par(1180, 680, t, 3, .4, 70))
    kx, ky, kw, kh = 760, 640, 400, 240
    glow = .4 + .3 * abs(A.w(t, 1.3))
    s += SL(Z_SRED, f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw}" height="{kh}" rx="14" fill="{KRAS}" opacity="{.9+.1*glow:.2f}" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{ky:.0f} L{kx+kw/2:.0f},{ky+kh*.6:.0f} L{kx+kw:.0f},{ky:.0f}" fill="none" stroke="{ZOL}" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw}" height="{kh}" rx="14" fill="none" stroke="{ZOL}" stroke-width="6"/>')
    klap = A.ease(A.seg(t, .4, 1.0))
    s += SL(Z_SRED, f'<rect x="{kx+kw*.1:.0f}" y="{ky+kh*.5+klap*20:.0f}" width="{kw*.8:.0f}" height="30" fill="{KREM}" opacity=".9" {o(2)}/>')
    oblk = _oblachko(kx + kw * .5, ky - 60 - klap * 20, .7 + .3 * klap, t, .2, "serdce")
    s += SL(Z_SRED, f'<g opacity="{klap:.2f}">{oblk}</g>')
    s += SL(Z_SRED, _napolnenie(60, 560, 1000, 160, t, 204, 20))
    s += SL(Z_PERED, ramka_pp("oba", "#0c0608", .4))
    s += vinetka(.42)
    return s


def konvert_dvumya_rukami(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a1420"/>'
    s += SL(Z_DAL, teplo(500, 400, 600, 440, .4))
    s += SL(Z_DAL, teplo(1500, 400, 600, 440, .4))
    for fx in (300, 1700):
        s += SL(Z_SRED, f'<path d="M{fx-50:.0f},700 l50,-90 l50,90 Z" fill="{KRAS}" {o(4)}/><ellipse cx="{fx:.0f}" cy="700" rx="30" ry="12" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, stol(760, 860, 400, 30))
    s += SL(Z_SRED, f'<ellipse cx="900" cy="850" rx="80" ry="22" fill="{MED}" {o(3)}/>')
    naklon = 8 * A.ease(A.seg(t, .3, .6))
    stoy1 = figura(600, 1020, 460, t, "#3a2a40", KREM, False, .0, naklon=naklon)
    s += SL(Z_SRED, stoy1)
    konv_x = 600 + (320) * A.ease(A.seg(t, .6, 1.0))
    ruk1, (r1x, r1y) = rukav(680, 820, 150, -40, t, "#3a2a40", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(620, 820, 150, -140, t, "#3a2a40", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    klanyat = A.ease(A.seg(t, 1.6, .6))
    stoy2 = figura(1200, 1040 - 4 * klanyat, 420, t, "#8c3a3a", KREM, False, .3, naklon=10 * klanyat)
    s += SL(Z_SRED, stoy2)
    ruk2, (r2x, r2y) = rukav(1130, 820, 150, -150, t, "#8c3a3a", KREM, .3, 3)
    s += SL(Z_SRED, ruk2)
    ruk2b, (r2bx, r2by) = rukav(1270, 820, 150, -40, t, "#8c3a3a", KREM, .6, 3)
    s += SL(Z_SRED, ruk2b)
    s += SL(Z_SRED, f'<rect x="{konv_x-50:.0f}" y="760" width="100" height="70" rx="6" fill="{KRAS}" {o(4)}/>')
    vtoraya = A.ease(A.seg(t, 2.4, 1.0))
    if vtoraya > .1:
        s += SL(Z_SRED, f'<g opacity="{vtoraya:.2f}"><rect x="1400" y="860" width="260" height="140" rx="30" fill="#efe3c8" {o(4)}/>'
                        f'<circle cx="1480" cy="900" r="40" fill="#e0b08a" {o(2)}/>'
                        f'<rect x="1560" y="940" width="60" height="40" rx="6" fill="{KRAS}" opacity=".9"/></g>')
    s += SL(Z_SRED, svecha(544, 816, t, 0.96, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0810", .4))
    s += vinetka(.42)
    return s


def chay_i_frukty_v_podarok(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a1420"/>'
    s += SL(Z_DAL, teplo(960, 400, 700, 500, .35))
    s += SL(Z_SRED, stol(300, 780, 1340, 32))
    s += SL(Z_SRED, f'<path d="M400,780 q0,-50 80,-50 q80,0 80,50 Z" fill="url(#derev)" {o(4)}/>')
    for i in range(4):
        jig = 4 * A.w(t, 1.3, i * .2)
        s += SL(Z_SRED, f'<circle cx="{420+i*36+jig:.0f}" cy="730" r="18" fill="{(ZOL,ZEL2)[i%2]}" {o(2)}/>')
    lenta = 6 * A.w(t, 1.4)
    s += SL(Z_SRED, f'<path d="M{420+lenta:.0f},730 q80,-20 160,0" fill="none" stroke="{KRAS}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="700" y="740" width="260" height="40" rx="8" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="730" rx="50" ry="40" fill="{CHUGUN}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="736" rx="30" ry="14" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, par(760, 690, t, 3, .4, 70))
    s += SL(Z_SRED, svecha(1020, 770, t, .3, .9))
    kx, ky = 1540, 680
    s += SL(Z_SRED, f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="210" fill="url(#derev)" {o(6)}/>')
    px, py, pw, ph_ = kx - 190, ky - 190, 380, 380
    put = kontur_proema(px, py, pw, ph_, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M1180,700 l40,-70 l40,70 Z" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1130" cy="760" rx="40" ry="16" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1060, 220, 2, 7, 90, 120))
    s += SL(Z_SRED, f'<rect x="200" y="600" width="90" height="160" rx="8" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M160,780 l-16,-140 l40,20 l16,120 Z" fill="{ZEL}" {o(3)}/>')
    blik_i = 4 * A.w(t, 2.0)
    s += SL(Z_SRED, f'<ellipse cx="{kx+blik_i:.0f}" cy="{ky-120:.0f}" rx="40" ry="14" fill="#fff" opacity=".4"/>')
    s += SL(Z_SRED, _napolnenie(1600, 560, 260, 160, t, 201, 14))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0810", .38))
    s += vinetka(.4)
    return s


def babushka_pishet_zapisku_v_konvert(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("noch", t, True, 77)
    s += SL(Z_DAL, okno_izby(1480, 160, 300, 300, t, svet=False, moroz=.3))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(420, 760, 980, 34))
    s += SL(Z_SRED, lampa(1200, 700, t, 1.0, True))
    s += SL(Z_SRED, f'<rect x="540" y="700" width="140" height="90" rx="4" fill="{POBEL}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="560" y="680" width="110" height="70" rx="4" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M700,700 v60" stroke="{ZHELEZ}" stroke-width="3"/><path d="M680,700 q20,10 40,0" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<circle cx="840" cy="730" r="30" fill="{STEKLO}" opacity=".6" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="920" y="700" width="90" height="30" rx="4" fill="{MED}" opacity=".8"/>')
    s += SL(Z_SRED, f'<rect x="1040" y="700" width="60" height="50" rx="4" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, figura(680, 1040, 480, t, "#6b2a44", KREM, True, .2))
    ruk1, (r1x, r1y) = rukav(640, 780, 140, -30, t, "#6b2a44", KREM, .2, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(720, 780, 150, -20, t, "#6b2a44", KREM, .5, 2)
    s += SL(Z_SRED, ruk2)
    pish = A.seg(t % 3.0, .2, 2.4)
    s += SL(Z_SRED, f'<path d="M{r2x:.0f},{r2y+10:.0f} h{80*pish:.0f}" stroke="#2a1d14" stroke-width="3" stroke-dasharray="6 4"/>')
    ochki_sv = 4 * A.ease(A.seg(t % 5.0, 2.0, 1.0))
    s += SL(Z_SRED, f'<rect x="{676+ochki_sv:.0f}" y="{940+ochki_sv:.0f}" width="40" height="14" rx="6" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, par(840, 700, t, 3, .4, 60))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def koza_v_sharfe_plede_i_varezhkah(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 79)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, pech(1500, 320, 380, 500, t))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _kovrik_pol(500, 900, 700, 120, TKAN, KREM, 81))
    kx, ky = 820, 900
    s += SL(Z_SRED, _koza_hozyayka(kx, ky, 420, t))
    sharf_sw = 4 * A.w(t, 1.2)
    s += SL(Z_SRED, f'<path d="M{kx-60+sharf_sw:.0f},{ky-280:.0f} q60,30 0,60 q-60,-10 0,-60 Z" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{kx+30:.0f},{ky-220:.0f} q20,60 -10,120" fill="none" stroke="{TKAN2}" stroke-width="22" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M{kx-120:.0f},{ky-60:.0f} q120,-40 240,0 l0,60 q-120,40 -240,0 Z" fill="{KAMEN}" opacity=".85" {o(3)}/>')
    for i in range(2):
        s += SL(Z_SRED, _varezhka(kx - 40 + i * 110, ky - 320 + 8 * A.w(t, 1.6, i * .3), 1.0, 20 - i * 40, KRAS))
    s += SL(Z_SRED, kot(kx + 200, ky + 20, t, .9, "#3b3430", False))
    s += SL(Z_SRED, f'<path d="M{kx+220:.0f},{ky-20:.0f} q20,{-20*A.w(t,2.0):.0f} 10,-40" fill="none" stroke="{TKAN}" stroke-width="6"/>')
    uzel = A.ease(A.seg(t, .4, 1.4))
    s += SL(Z_SRED, figura(kx - 220, 1040, 460, t, "#5a6a4a", KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(kx - 160, 820, 140, -20 + uzel * 30, t, "#5a6a4a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(kx - 100, 820, 140, -60 - uzel * 30, t, "#5a6a4a", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<rect x="300" y="860" width="100" height="90" rx="30" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M340,860 v-30" stroke="{DOSKA}" stroke-width="6"/><path d="M360,860 v-30" stroke="{DOSKA}" stroke-width="6"/>')
    s += SL(Z_SRED, svecha(703, 807, t, 0.07, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def suvenir_v_shkafu(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 83)
    s += SL(Z_DAL, _oboi_fon("#4a3a4a", "#3a2e3a"))
    s += SL(Z_SRED, polovicy(840))
    sx, sy, sw, sh = 660, 380, 600, 500
    s += SL(Z_SRED, f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw}" height="{sh}" rx="10" fill="url(#derev)" {o(7)}/>')
    for row in range(2):
        gy = sy + 40 + row * 220
        s += SL(Z_SRED, f'<rect x="{sx+30:.0f}" y="{gy:.0f}" width="{sw-60}" height="180" rx="6" fill="url(#stekl)" opacity=".4" {o(3)}/>')
    suveniry = [(0, "slon", KREM), (1, "palma", ZEL), (2, "shar", STEKLO), (3, "figurka", MED), (4, "rakushka", "#e8d8c8")]
    for idx, kind, col in suveniry:
        gx = sx + 70 + idx * (sw - 140) / 4
        gy = sy + 180
        if kind == "slon":
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="22" ry="18" fill="{col}" {o(2)}/>')
        elif kind == "palma":
            s += SL(Z_SRED, f'<path d="M{gx:.0f},{gy+16:.0f} v-30 M{gx-14:.0f},{gy-14:.0f} l14,0 l10,-10" stroke="{col}" stroke-width="4" fill="none"/>')
        elif kind == "shar":
            s += SL(Z_SRED, f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="20" fill="{col}" opacity=".7" {o(2)}/>')
        elif kind == "figurka":
            s += SL(Z_SRED, f'<rect x="{gx-10:.0f}" y="{gy-20:.0f}" width="20" height="34" rx="6" fill="{col}" {o(2)}/>')
        else:
            s += SL(Z_SRED, f'<path d="M{gx-16:.0f},{gy+10:.0f} q16,-26 32,0 Z" fill="{col}" {o(2)}/>')
    nova = A.ease(A.seg(t, .4, 1.0))
    nx, ny = sx + sw + 60 - nova * 170, sy + 180
    s += SL(Z_SRED, f'<rect x="{nx-14:.0f}" y="{ny-20:.0f}" width="28" height="34" rx="6" fill="{ZOL}" {o(2)}/>')
    pautinka = A.ease(A.seg(t, 1.4, 1.2))
    if pautinka > .1:
        s += SL(Z_SRED, f'<path d="M{nx:.0f},{ny-20:.0f} q10,{-10*pautinka:.0f} 20,0 q-6,{10*pautinka:.0f} -20,0" fill="none" stroke="#cfd6de" stroke-width="2" opacity="{pautinka:.2f}"/>')
    zakr = A.ease(A.seg(t, 2.0, .6))
    s += SL(Z_SRED, f'<rect x="{sx+sw-20*zakr:.0f}" y="{sy:.0f}" width="20" height="{sh}" fill="url(#derev)" opacity="{zakr:.2f}" {o(2)}/>')
    ruk1, (r1x, r1y) = rukav(sx + sw + 140, 900, 160, -140, t, "#3a3a4a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    povorot = A.ease(A.seg(t, 2.4, .8))
    s += SL(Z_SRED, f'<g transform="rotate({povorot*20:.1f} {sx+150:.0f} {sy+100:.0f})">' + _koza_hozyayka(sx + 150, sy + 320, 180, t) + '</g>')
    s += SL(Z_SRED, svecha(1286, 854, t, 0.14, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e14", .38))
    s += vinetka(.4)
    return s


# ═══════════════════════════ 82-91 ══════════════════════════════
def vechera_nad_vyazanem(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    luna_x = 1500 + 300 * math.sin(t * .6)
    oknovid = nebo("noch", t, True, 85) + f'<circle cx="{luna_x-1300:.0f}" cy="200" r="34" fill="{KREM}" opacity=".9"/>'
    s += SL(Z_DAL, okno_izby(1300, 160, 360, 340, t, vid=oknovid, moroz=.1, svet=False))
    s += SL(Z_DAL, _oboi_fon("#4a3a3a", "#3a2e2e"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, f'<rect x="960" y="700" width="260" height="280" rx="20" fill="#6b4428" {o(6)}/>')
    s += SL(Z_SRED, lampa(1180, 620, t, 1.1, True))
    mx, my, mw, mh = 1080, 500, 460, 400
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{mw*.52:.0f}" ry="{mh*.52:.0f}" fill="url(#zol)" {o(5)}/>')
    put = kontur_proema(mx - mw * .42, my - mh * .42, mw * .84, mh * .84, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(mx - mw * .42, my - mh * .42, mw * .84, mh * .84, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(4)}/>')
    stopka_h = min(140, 10 + t * 12)
    s += SL(Z_SRED, f'<rect x="1340" y="{860-stopka_h:.0f}" width="140" height="{stopka_h:.0f}" rx="6" fill="{TKAN}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M100,760 q80,-40 160,0 l0,60 q-80,40 -160,0 Z" fill="#6b4428" {o(4)}/>')
    for i in range(3):
        s += SL(Z_SRED, _banka(140 + i * 50, 790, .6, (TKAN, TKAN2, MED)[i]))
    s += SL(Z_SRED, kot(420, 940, t, .9, "#3b3430", True))
    s += SL(Z_SRED, f'<circle cx="640" cy="760" r="60" fill="url(#derev)" {o(4)}/><circle cx="640" cy="760" r="46" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, figura(1060, 1040, 440, t, "#6b2a38", KREM, False, .0))
    sp1 = 6 * A.w(t, 4.0)
    sp2 = 6 * A.w(t, 4.0, .5)
    ruk1, (r1x, r1y) = rukav(1000, 840, 130, -20 + sp1, t, "#6b2a38", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(1120, 840, 130, -160 + sp2, t, "#6b2a38", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<circle cx="1060" cy="900" r="40" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def vyazanye_noski_idut_mimo_primety(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 87)
    s += SL(Z_DAL, _oboi_fon("#5a4a5a", "#4a3a4a"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _kovrik_pol(500, 880, 900, 140, TKAN, KREM, 89))
    idut = (t * 120) % 760
    for i, col in enumerate((KRAS, TKAN2)):
        nx = 560 + idut - i * 60
        tilt = 10 * math.sin(t * 6 + i)
        s += SL(Z_SRED, f'<g transform="rotate({tilt:.1f} {nx:.0f} 900)">'
                        f'<path d="M{nx-30:.0f},900 q0,-50 30,-50 q30,0 30,50 q-10,20 -30,20 q-20,0 -30,-20 Z"'
                        f' fill="{col}" {o(3)}/></g>')
    s += SL(Z_SRED, _varezhka(560 + idut - 140, 880, 1.0, 10 * math.sin(t * 5)))
    s += SL(Z_SRED, f'<path d="M{560+idut-220:.0f},860 q40,-10 80,0" fill="none" stroke="{TKAN2}" stroke-width="18"/>')
    px = 1500
    s += SL(Z_SRED, f'<path d="M{px:.0f},900 v-260" stroke="{ZHELEZ}" stroke-width="6"/>')
    zhezl = -20 * A.ease(A.seg(t % 3.0, .6, .5))
    s += SL(Z_SRED, f'<g transform="rotate({zhezl:.1f} {px:.0f} 760)">'
                    f'<line x1="{px:.0f}" y1="760" x2="{px+100:.0f}" y2="700" stroke="{ZHELEZ}" stroke-width="5"/></g>')
    s += SL(Z_SRED, _primeta_vorona(px, 660, 1.0, t, 0))
    s += SL(Z_SRED, _veshalka_seni(1600, 300, 300, t, 11))
    s += SL(Z_SRED, kot(1300, 900, t, .8, "#3b3430", False))
    s += SL(Z_SRED, f'<ellipse cx="1340" cy="700" rx="60" ry="90" fill="{STEKLO}" opacity=".5" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="400" y="820" width="100" height="40" rx="8" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M300,780 q10,-60 40,-70" fill="none" stroke="{ZOL}" stroke-width="6"/>')
    s += SL(Z_SRED, svecha(1498, 762, t, 1.62, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .38))
    s += vinetka(.4)
    return s


def stopka_noskov_s_birkami(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 91)
    s += SL(Z_DAL, _oboi_fon("#4a3a4a", "#3a2e3a"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, f'<rect x="260" y="700" width="700" height="200" rx="30" fill="{TKAN2}" {o(5)}/>')
    tvx, tvy = 1500, 540
    s += SL(Z_SRED, f'<rect x="{tvx-130:.0f}" y="{tvy-80:.0f}" width="260" height="190" rx="10" fill="{ZHELEZ}" {o(5)}/>')
    mig = ((t * 1.4) % 1.0) > .5
    s += SL(Z_SRED, f'<rect x="{tvx-100:.0f}" y="{tvy-60:.0f}" width="200" height="150" fill="{SVET if mig else "#4a5a68"}" opacity="{.7 if mig else .4}"/>')
    s += SL(Z_SRED, f'<rect x="{tvx-140:.0f}" y="{tvy+110:.0f}" width="280" height="30" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="900" y="700" width="260" height="40" rx="8" fill="url(#derev)" {o(5)}/>')
    stopka = min(170, 10 + t * 22)
    cols = (KRAS, TKAN2, ZEL2, TKAN)
    for i in range(4):
        hh = stopka / 4
        s += SL(Z_SRED, f'<rect x="920" y="{700-hh*(i+1):.0f}" width="220" height="{hh-4:.0f}" rx="8" fill="{cols[i]}" {o(2)}/>')
        if stopka > hh * (i + .6) * 4 / 4:
            s += SL(Z_SRED, f'<rect x="1000" y="{700-hh*(i+1)+6:.0f}" width="50" height="20" fill="{KREM}" {o(1)}/>')
    s += SL(Z_SRED, f'<circle cx="430" cy="690" r="60" fill="{TKAN}" {o(3)}/>')
    s += SL(Z_SRED, kot(300, 900, t, .9, "#3b3430", False))
    s += SL(Z_SRED, figura(700, 1040, 460, t, "#5a6a4a", KREM, True, .0))
    sp1 = 5 * A.w(t, 4.2)
    sp2 = 5 * A.w(t, 4.2, .5)
    ruk1, (r1x, r1y) = rukav(640, 820, 140, -30 + sp1, t, "#5a6a4a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(760, 820, 140, -150 + sp2, t, "#5a6a4a", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    ochki_dr = 3 * A.w(t, 1.0)
    s += SL(Z_SRED, f'<rect x="{676+ochki_dr:.0f}" y="950" width="40" height="14" rx="6" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, svecha(1233, 817, t, 1.77, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def banka_v_sitcevoy_shapochke(t):
    s = f'<rect width="{W}" height="{H}" fill="{KAMEN2}"/>'
    s += SL(Z_DAL, kladka(0, 0, W, 900))
    s += SL(Z_SRED, polovicy(900, "url(#beton)"))
    sx, sy, sw = 1060, 320, 820
    s += SL(Z_SRED, f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw}" height="80" fill="url(#derev)" {o(4)}/>')
    px, py, pw, ph_ = sx + 30, sy + 90, 760, 300
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{sx:.0f}" y="{py+ph_+10:.0f}" width="{sw}" height="80" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, stol(260, 760, 800, 34))
    s += SL(Z_SRED, _banka(460, 740, 1.5, RUSH))
    s += SL(Z_SRED, f'<ellipse cx="700" cy="720" rx="60" ry="40" fill="url(#med)" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{660+i*16:.0f},720 q8,-20 0,-40" fill="none" stroke="#6b4a2e" stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M880,730 q10,-60 30,-70" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<circle cx="340" cy="700" r="26" fill="{ZHELEZ}" {o(2)}/>')
    birka_i = int((t * .6) % 3)
    labels = (("Варенье",), ("Мёд",), ("Грибы",))[birka_i]
    s += SL(Z_SRED, f'<rect x="420" y="640" width="80" height="30" rx="4" fill="{KREM}" opacity="{.6+.4*abs(A.w(t,1.5)):.2f}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1000, 760, t, .3, .9))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0c", .4))
    s += vinetka(.4)
    return s


def banka_mezhdu_chaynikom_i_hlebnicey(t):
    s = f'<rect width="{W}" height="{H}" fill="#3a3e44"/>'
    s += SL(Z_DAL, _oboi_fon("#4a5258", "#3a4248"))
    s += SL(Z_DAL, f'<rect x="300" y="160" width="340" height="420" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_DAL, f'<rect x="320" y="180" width="300" height="160" rx="6" fill="url(#stekl)" opacity=".4" {o(3)}/>')
    s += SL(Z_DAL, f'<rect x="1260" y="200" width="300" height="260" rx="8" fill="#2a2e34" {o(5)}/>')
    s += SL(Z_DAL, _chasy_sten(1600, 300, 1.0, t))
    s += SL(Z_SRED, f'<rect x="200" y="700" width="1520" height="300" fill="{BETON}" {o(5)}/>')
    s += SL(Z_SRED, _samovar(460, 740, .7, t, True))
    s += SL(Z_SRED, f'<rect x="1300" y="700" width="220" height="110" rx="10" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1320" y="660" width="180" height="50" rx="6" fill="{KREM}" opacity=".8" {o(3)}/>')
    kladovka = max(0, 1 - A.ease(A.seg(t % 4.0, .3, 1.6)))
    if kladovka > .02:
        s += SL(Z_SRED, f'<g opacity="{kladovka*.5:.2f}">' + brevna(700, 300, 500, 440, 60) + '</g>')
    s += SL(Z_SRED, _banka(900, 760, 1.5, RUSH))
    bant_sh = 4 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<path d="M{900+bant_sh:.0f},700 q-20,10 0,20" fill="none" stroke="{KRAS}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="1080" y="750" width="40" height="20" fill="url(#zhel)" {o(2)}/>')
    s += SL(Z_SRED, svecha(160, 780, t, 0.0, .8))
    s += SL(Z_SRED, _napolnenie(60, 760, 220, 180, t, 208, 3))
    s += SL(Z_SRED, _napolnenie(700, 760, 540, 160, t, 211, 7))
    s += SL(Z_SRED, kot(1700, 920, t, .85, "#3b3430", False))
    s += SL(Z_PERED, ramka_pp("oba", "#1a1e22", .34))
    s += vinetka(.36)
    return s


def koshelek_s_monetoy_i_vaza_s_gostin(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 93)
    s += SL(Z_DAL, _elka(1500, 960, 520, t, 23))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, stol(360, 760, 1000, 34))
    s += SL(Z_SRED, _koshelek(600, 740, 1.3, True, 1))
    blesk = .5 + .5 * abs(A.w(t, 1.6))
    s += SL(Z_SRED, f'<circle cx="590" cy="708" r="10" fill="{SVET}" opacity="{blesk:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M900,700 v-80 q0,-20 40,-20 q40,0 40,20 v80 Z" fill="{STEKLO}" opacity=".5" {o(4)}/>')
    podn = 4 * A.w(t, 1.2)
    s += SL(Z_SRED, f'<path d="M{900+podn:.0f},690 q40,-6 80,0" fill="none" stroke="{KREM}" stroke-width="4" opacity=".7"/>')
    if abs(math.sin(t * .8)) > .5:
        s += SL(Z_SRED, _galochka(600, 650, .7, t, 0))
    if abs(math.sin(t * .8 + 1)) > .5:
        s += SL(Z_SRED, _galochka(940, 620, .7, t, .3))
    s += SL(Z_SRED, f'<path d="M1100,740 q10,-50 40,-60" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_SRED, svecha(1250, 740, t, .4, .9))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.4)
    return s


def kniga_s_nadpisyu(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 95)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 760, 1200, 34))
    s += SL(Z_SRED, lampa(600, 680, t, 1.1, True))
    s += SL(Z_SRED, f'<path d="M900,780 L900,700 Q900,680 940,680 L1180,680 Q1220,680 1220,700 L1220,780 Z" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<line x1="1060" y1="680" x2="1060" y2="780" stroke="{POL}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<rect x="1280" y="700" width="60" height="30" rx="6" fill="#1a1a2a" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1380,710 l30,-16 l6,6 l-26,18 Z" fill="{DOSKA}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1440" y="720" width="40" height="14" rx="6" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<ellipse cx="1550" cy="730" rx="40" ry="18" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, figura(900, 1060, 480, t, "#5a4a3a", KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(840, 800, 140, -40, t, "#5a4a3a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(1030, 800, 150, -140, t, "#5a4a3a", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    pero = A.seg(t % 3.0, .3, 2.2)
    s += SL(Z_SRED, f'<path d="M{r2x:.0f},{r2y+6:.0f} h{90*pero:.0f}" stroke="#1a1a2a" stroke-width="3" stroke-dasharray="4 5"/>')
    s += SL(Z_SRED, f'<path d="M{950+90*pero:.0f},{r2y:.0f} l10,0 l-4,-6" fill="none" stroke="#1a1a2a" stroke-width="2"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def kniga_na_polke_cherez_gody(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 97)
    s += SL(Z_DAL, _oboi_fon("#4a3a4a", "#3a2e3a"))
    s += SL(Z_SRED, polovicy(840))
    px, py = 760, 440
    s += SL(Z_SRED, f'<rect x="{px:.0f}" y="{py:.0f}" width="500" height="340" rx="8" fill="url(#derev)" {o(6)}/>')
    for i in range(10):
        bx = px + 30 + i * 44
        s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{py+40:.0f}" width="34" height="240" rx="3" fill="{(TKAN,TKAN2,MED,ZEL2)[i%4]}" {o(2)}/>')
    snyali = A.ease(A.seg(t, .3, .8))
    s += SL(Z_SRED, f'<rect x="{px+200+snyali*60:.0f}" y="{py+40-snyali*140:.0f}" width="34" height="240" rx="3" fill="{MED}" {o(3)}/>')
    oblk = A.ease(A.seg(t, 1.2, 1.4))
    if oblk > .05:
        s += SL(Z_SRED, f'<g opacity="{oblk:.2f}"><ellipse cx="{px+260:.0f}" cy="{py-30-oblk*40:.0f}" rx="70" ry="46" fill="#ffffff" opacity=".9" {o(3)}/>'
                        f'<circle cx="{px+230:.0f}" cy="{py-10-oblk*40:.0f}" r="22" fill="#e0b08a" {o(2)}/>'
                        f'<rect x="{px+200:.0f}" y="{py+6-oblk*40:.0f}" width="60" height="30" fill="#2a3a4a" {o(2)}/></g>')
    s += SL(Z_SRED, kot(1400, 920, t, .9, "#3b3430", False))
    s += SL(Z_SRED, f'<rect x="200" y="760" width="220" height="200" rx="16" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, figura(px + 150, 1040, 460, t, "#3a3a4a", KREM, False, .3))
    ruk1, (r1x, r1y) = rukav(px + 210, 820, 130, -50, t, "#3a3a4a", KREM, .3, 2)
    s += SL(Z_SRED, ruk1)
    prizh = A.ease(A.seg(t, 2.6, 1.0))
    s += SL(Z_SRED, f'<rect x="{px+150-20*prizh:.0f}" y="{960-prizh*60:.0f}" width="40" height="60" rx="4" fill="{MED}" opacity="{.5+.5*prizh:.2f}" {o(2)}/>')
    s += SL(Z_SRED, svecha(491, 779, t, 0.59, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def vnuki_s_konvertami(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 99)
    s += SL(Z_DAL, _elka(1500, 960, 520, t, 29))
    s += SL(Z_SRED, _kovrik_pol(500, 880, 900, 160, TKAN, KREM, 31))
    s += SL(Z_SRED, hodiki(1700, 300, t, .9))
    s += SL(Z_SRED, f'<path d="M1300,900 l60,-30 l-20,40 Z" fill="{ZEL2}" {o(2)}/>')
    s += SL(Z_SRED, figura(700, 1000, 300, t, "#3a5a6b", KREM, False, .0))
    svet = A.seg(t % 3.0, .3, 2.0)
    ruk1, (r1x, r1y) = rukav(750, 810, 90, -40, t, "#3a5a6b", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(650, 810, 90, -150, t, "#3a5a6b", KREM, .3, 2)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<g transform="rotate({8*math.sin(t*1.4):.1f} {(r1x+r1bx)/2:.0f} {(r1y+r1by)/2:.0f})">'
                    f'<rect x="{(r1x+r1bx)/2-40:.0f}" y="{(r1y+r1by)/2-28:.0f}" width="80" height="56" rx="4" fill="{KRAS}" {o(3)}/></g>')
    s += SL(Z_SRED, figura(1040, 1020, 280, t, "#8c3a4a", KREM, False, .3))
    ubyvaet = int(6 - (t * 1.5) % 6)
    ruk2, (r2x, r2y) = rukav(1100, 920, 90, -30, t, "#8c3a4a", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<path d="M{r2x-10:.0f},{r2y:.0f} l20,0 l-10,16 Z" fill="{MED}" {o(2)}/>')
    for i in range(max(0, 8 - ubyvaet)):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<circle cx="{980+rnd.random()*80:.0f}" cy="{1080+rnd.random()*30:.0f}" r="10" fill="{(ZOL,KRAS)[i%2]}" opacity=".6" {o(1)}/>')
    s += SL(Z_SRED, f'<path d="M1200,860 l-60,-30 l60,-10 Z" fill="{DOSKA}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1445, 845, t, 1.25, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .38))
    s += vinetka(.4)
    return s


def korzinka_dlya_vzroslyh_detey(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 101)
    s += SL(Z_DAL, _oboi_fon())
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, stol(460, 780, 1000, 34))
    kx = 900
    perehod = A.ease(A.seg(t, .3, 1.4))
    kkx = 700 + perehod * 260
    s += SL(Z_SRED, f'<path d="M{kkx-90:.0f},780 q90,-50 180,0 Z" fill="none" stroke="{MED}" stroke-width="8"/>'
                    f'<path d="M{kkx-100:.0f},780 q100,40 200,0 l0,40 q-100,40 -200,0 Z" fill="{MED}" {o(4)}/>')
    s += SL(Z_SRED, _banka(kkx - 40, 760, .6, RUSH))
    s += SL(Z_SRED, f'<rect x="{kkx+10:.0f}" y="750" width="50" height="30" rx="8" fill="{TKAN2}" {o(2)}/>')
    s += SL(Z_SRED, f'<circle cx="{kkx+60:.0f}" cy="770" r="14" fill="{ZOL}" {o(1)}/><circle cx="{kkx+80:.0f}" cy="770" r="14" fill="{ZOL}" {o(1)}/>')
    s += SL(Z_SRED, f'<path d="M1200,750 q10,-50 40,-60" fill="none" stroke="{KRAS}" stroke-width="5"/>')
    s += SL(Z_SRED, svecha(1350, 780, t, .3, .9))
    stoy1 = figura(600, 1060, 470, t, "#5a3a4a", KREM, False, .0)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(670, 820, 150, -30, t, "#5a3a4a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(540, 820, 150, -150, t, "#5a3a4a", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    stoy2 = figura(1260, 1060, 460, t, "#8c3a6a", KREM, False, .3, True)
    s += SL(Z_SRED, stoy2)
    poceluy = A.ease(A.seg(t, 2.0, .6))
    s += SL(Z_SRED, f'<g transform="translate({-20*poceluy:.0f},0)">'
                    f'<ellipse cx="640" cy="1000" rx="20" ry="14" fill="#e0b08a" {o(2)}/></g>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .38))
    s += vinetka(.4)
    return s


# ═══════════════════════════ 92-99 ══════════════════════════════
def chay_s_sosedkoy(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 103)
    s += SL(Z_DAL, _oboi_fon("#5a4a4a", "#4a3a3a"))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(420, 760, 1080, 34))
    s += SL(Z_SRED, _banka(560, 720, 1.0, RUSH))
    s += SL(Z_SRED, f'<path d="M520,700 q20,-20 20,-40" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<ellipse cx="720" cy="740" rx="40" ry="16" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="880" cy="740" rx="40" ry="16" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, _samovar(1100, 740, .55, t))
    s += SL(Z_SRED, f'<ellipse cx="1300" cy="750" rx="60" ry="22" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1480" cy="730" r="16" fill="{CHUGUN}" {o(2)}/>')
    s += SL(Z_SRED, figura(680, 1040, 460, t, "#6b4a3a", KREM, True, .0))
    nal_t = A.seg(t % 3.0, .2, 2.4)
    ruk1, (r1x, r1y) = rukav(760, 800, 140, -50, t, "#6b4a3a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y:.0f} q10,{30*nal_t:.0f} 0,{60*nal_t:.0f}" fill="none" stroke="{STEKLO}" stroke-width="3" opacity="{nal_t:.2f}"/>')
    ruk1b, (r1bx, r1by) = rukav(600, 800, 140, -150, t, "#6b4a3a", KREM, .3, 2)
    s += SL(Z_SRED, ruk1b)
    stoy2 = figura(1140, 1040, 460, t, "#3a5a6b", KREM, False, .4)
    s += SL(Z_SRED, stoy2)
    ruk2, (r2x, r2y) = rukav(1060, 800, 140, -30, t, "#3a5a6b", KREM, .4, 2)
    s += SL(Z_SRED, ruk2)
    zhmur = abs(A.w(t, 1.1)) > .7
    s += SL(Z_SRED, f'<ellipse cx="1050" cy="990" rx="14" ry="{3 if zhmur else 8}" fill="{K}"/>')
    s += SL(Z_SRED, par(560, 700, t, 3, .4, 60))
    s += SL(Z_SRED, par(1100, 660, t, 3, .4, 60, .5))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def sharf_dlya_muzha(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 105)
    s += SL(Z_DAL, okno_izby(1480, 160, 280, 280, t, svet=False, moroz=.6))
    s += SL(Z_DAL, _oboi_fon("#3a3a4a", "#2e2e3e"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _veshalka_seni(1200, 260, 400, t, 15))
    s += SL(Z_SRED, f'<path d="M160,900 l0,-260 l20,-10 l0,270 Z" fill="{DOSKA}" {o(3)}/><path d="M160,640 l120,30" stroke="{DOSKA}" stroke-width="10"/>')
    s += SL(Z_SRED, f'<path d="M320,900 l-30,-130 l60,0 Z" fill="#8c3a3a" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="760" width="90" height="60" rx="6" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, _kovrik_pol(700, 900, 500, 110, TKAN, KREM, 37))
    stoy1 = figura(900, 1040, 480, t, "#6b4a6b", KREM, False, .0)
    s += SL(Z_SRED, stoy1)
    stoy2 = figura(900, 1060, 500, t, "#2a3a4a", "#cfd6de", True, .3)
    s += SL(Z_SRED, stoy2)
    obmot = A.ease(A.seg(t % 3.0, .3, 2.0)) % 1.0
    wrap = min(obmot * 3, 3)
    for i in range(3):
        if wrap > i:
            rot = -30 + i * 35
            s += SL(Z_SRED, f'<g transform="rotate({rot:.1f} 900 840)"><rect x="840" y="800" width="120" height="40" rx="10" fill="{TKAN}" {o(2)}/></g>')
    s += SL(Z_SRED, f'<rect x="870" y="860" width="60" height="140" rx="20" fill="{TKAN}" {o(2)}/>')
    us_sh = 2 * A.w(t, 1.2)
    s += SL(Z_SRED, f'<path d="M{880+us_sh:.0f},880 q-20,4 -30,0 M{920-us_sh:.0f},880 q20,4 30,0" stroke="#2a1d14" stroke-width="4" fill="none"/>')
    s += SL(Z_SRED, f'<circle cx="300" cy="700" r="20" fill="none" stroke="{STEKLO}" stroke-width="3" opacity=".6"/>')
    s += SL(Z_SRED, svecha(1074, 826, t, 0.66, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e14", .36))
    s += vinetka(.4)
    return s


def sad_i_devyatyy_etazh(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W//2}" height="{H}" fill="{DEN}"/>')
    s += SL(Z_SRED, f'<rect x="{W//2}" y="0" width="{W//2}" height="{H}" fill="{SUMER}"/>')
    s += SL(Z_DAL, izba_snaruzhi(260, 880, 400, t, False, True, 7))
    s += SL(Z_SRED, sneg_lezhit(840))
    s += SL(Z_SRED, f'<rect x="600" y="640" width="200" height="200" rx="10" fill="{STEKLO}" opacity=".3" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M560,900 l-30,-200 l200,-20 l0,220 Z" fill="{ZEL}" opacity=".5" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="700" cy="920" rx="70" ry="24" fill="#6b4428" {o(3)}/>')
    stoy1 = figura(400, 1040, 480, t, "#3a4a3a", KREM, True, .0)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(480, 800, 140, -70, t, "#3a4a3a", KREM, .0, 4)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(400, 800, 140, -110, t, "#3a4a3a", KREM, .3, 4)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<rect x="{(r1x+r1bx)/2-60:.0f}" y="{(r1y+r1by)/2-30:.0f}" width="120" height="70" rx="8" fill="{DOSKA}" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{(r1x+r1bx)/2-40+i*26:.0f}" cy="{(r1y+r1by)/2-10:.0f}" r="14" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_DAL, panelka(W - 420, 900, 400, t, 6, True, 11))
    s += SL(Z_SRED, okno_izby(W - 360, 680, 280, 260, t, svet=True, moroz=0, krest=True))
    s += SL(Z_SRED, teplo(W - 220, 800, 260, 200, .4))
    ovx, ovy, ovw, ovh = W - 900, 760, 820, 340
    s += SL(Z_SRED, f'<rect x="{ovx:.0f}" y="{ovy:.0f}" width="{ovw}" height="{ovh}" rx="10" fill="{PECH}" {o(5)}/>')
    px, py, pw, ph_ = ovx + 30, ovy + 30, 760, 300
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(7)}/>')
    otkr = A.ease(A.seg(t, .4, .8))
    stoy2 = figura(W - 540, 1060, 480, t, "#8c3a4a", KREM, False, .3, True)
    s += SL(Z_SRED, stoy2)
    ruk2, (r2x, r2y) = rukav(ovx + ovw - 60, ovy + ovh - 60, 150, -140, t, "#8c3a4a", KREM, .3, 3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<rect x="{r2x-30:.0f}" y="{r2y-20:.0f}" width="60" height="40" rx="6" fill="{TKAN}" {o(2)}/>')
    s += SL(Z_SRED, par(ovx + ovw - 40, ovy + ovh - 40, t, 3, .4, 60) if otkr > .5 else "")
    s += SL(Z_PERED, f'<rect x="{W//2-4}" y="0" width="8" height="{H}" fill="{K}"/>')
    s += vinetka(.4)
    return s


def vecher_protiv_pensii(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 107)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(560, 760, 800, 34))
    nak = 22
    s += SL(Z_SRED, _vesy(960, 760, 1.4, t, nak, 9))
    s += SL(Z_SRED, f'<g transform="translate({960-150*1.4-50:.0f},{760-220*1.4-60:.0f})">'
                    f'<rect width="100" height="70" rx="6" fill="{TKAN2}" {o(3)}/>'
                    f'<rect x="10" y="50" width="30" height="20" fill="{KREM}" {o(2)}/></g>')
    s += SL(Z_SRED, f'<path d="M{960-150*1.4-20:.0f},{760-220*1.4+80:.0f} q-10,-90 60,-100" fill="none" stroke="{KREM}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<g transform="translate({960+150*1.4-50:.0f},{760-220*1.4+30:.0f})">'
                    + _varezhka(50, 40, 1.1, 0) + f'<path d="M80,20 l0,-50" stroke="{SVET}" stroke-width="6" opacity=".7"/></g>')
    s += SL(Z_SRED, figura(900, 1060, 480, t, "#6b4a3a", KREM, True, .0))
    s += SL(Z_SRED, f'<circle cx="840" cy="990" r="18" fill="none" stroke="{ZHELEZ}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<ellipse cx="700" cy="720" rx="40" ry="14" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, f'<circle cx="1200" cy="700" r="24" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, hodiki(1500, 320, t, .9))
    s += SL(Z_SRED, svecha(657, 783, t, 0.87, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def kartochka_drugogo_rolika(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a0e14"/>'
    s += SL(Z_DAL, teplo(960, 400, 800, 500, .4))
    for i in range(6):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<path d="M{200+rnd.random()*1500:.0f},{200+rnd.random()*700:.0f} l-10,-60 l20,0 Z" fill="{ZEL}" opacity=".5" {o(2)}/>')
    otskok = A.over(A.seg(t, .3, 1.0))
    cx, cy, cw, ch = 960, 580, 500, 320
    s += SL(Z_SRED, f'<g transform="translate(0,{(1-otskok)*300:.0f})"><rect x="{cx-cw/2:.0f}" y="{cy-ch/2:.0f}" width="{cw}" height="{ch}" rx="16" fill="{KREM}" {o(6)}/>'
                    f'<path d="M{cx-120:.0f},{cy+60:.0f} l40,-110 l80,0 l40,110 Z" fill="{KRAS}" {o(3)}/>'
                    f'<circle cx="{cx+120:.0f}" cy="{cy:.0f}" r="70" fill="url(#zol)" {o(3)}/>'
                    f'<line x1="{cx+120:.0f}" y1="{cy:.0f}" x2="{cx+120:.0f}" y2="{cy-40:.0f}" stroke="{K}" stroke-width="4"/>'
                    f'<line x1="{cx+120:.0f}" y1="{cy:.0f}" x2="{cx+150:.0f}" y2="{cy:.0f}" stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, _koza_hozyayka(400, 920, 340, t))
    s += SL(Z_SRED, f'<path d="M580,860 q30,-10 60,0" fill="none" stroke="{SVET}" stroke-width="4" opacity=".6"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<circle cx="{1500+i*60}" cy="{400+60*math.sin(t+i)}" r="20" fill="{(KRAS,ZOL,TKAN2)[i]}" opacity=".8" {o(2)}/>')
    s += SL(Z_SRED, svecha(1600, 800, t, .3, 1.0))
    s += SL(Z_SRED, _napolnenie(120, 700, 420, 160, t, 202, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#0c0608", .42))
    s += vinetka(.44)
    return s


def shkolnyy_zal_s_elkoy(t):
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += SL(Z_NEBO, teplo(960, 300, 900, 500, .4))
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="700" fill="{KAMEN2}"/>')
    for i in range(6):
        s += SL(Z_DAL, f'<rect x="{80+i*300}" y="200" width="160" height="320" rx="80" fill="{KAMEN}" opacity=".4" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M0,700 L1920,700 L1920,760 L0,760 Z" fill="{DOSKA}" {o(4)}/>')
    s += SL(Z_SRED, _elka(1500, 940, 560, t, 41))
    for i in range(10):
        s += SL(Z_SRED, f'<path d="M{1360+i*30:.0f},700 l-6,-40 l12,0 Z" fill="{KRAS}" opacity=".7"/>')
    s += SL(Z_SRED, f'<rect x="60" y="480" width="500" height="220" rx="10" fill="#3a2e2e" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="80" y="500" width="460" height="180" fill="#1a1414" opacity=".8"/>')
    s += SL(Z_SRED, f'<rect x="760" y="520" width="140" height="180" rx="8" fill="#2a1a10" {o(4)}/><rect x="770" y="530" width="120" height="60" fill="{KREM}" {o(2)}/>')
    for row in range(2):
        for col in range(6):
            s += SL(Z_SRED, f'<ellipse cx="{300+col*220}" cy="{820+row*110}" rx="40" ry="24" fill="{SUMER}" opacity=".7" {o(2)}/>')
    stoy = figura(900, 940, 300, t, KRAS, KREM, False, .0)
    s += SL(Z_SRED, stoy)
    s += SL(Z_SRED, f'<path d="M870,700 q30,-30 60,0" fill="none" stroke="{KREM}" stroke-width="10"/>')
    ushi = 8 * A.w(t, 1.4)
    s += SL(Z_SRED, f'<path d="M870,{700+ushi:.0f} l-10,-30 M930,{700+ushi:.0f} l10,-30" stroke="{KREM}" stroke-width="6" fill="none"/>')
    chitaet = A.seg(t % 2.0, 0, 1.6)
    s += SL(Z_SRED, f'<ellipse cx="900" cy="{880+6*chitaet:.0f}" rx="12" ry="{6+4*chitaet:.0f}" fill="#2a1d14"/>')
    ded = figura(1100, 980, 400, t, KRAS, "#efe3c8", False, .3, True, boroda=True)
    s += SL(Z_SRED, ded)
    kivok = 4 * A.w(t, 1.0)
    s += SL(Z_SRED, f'<path d="M1030,{900+kivok:.0f} v120" stroke="url(#derev)" stroke-width="10"/>')
    s += SL(Z_SRED, svecha(1127, 863, t, 1.03, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#1a0e08", .36))
    s += vinetka(.38)
    return s


# ═══════════════════════════ 99-106 ══════════════════════════════
def paket_s_detskogo_prazdnika(t):
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += SL(Z_DAL, teplo(960, 400, 800, 500, .36))
    s += SL(Z_DAL, _elka(1600, 940, 480, t, 43))
    s += SL(Z_SRED, f'<path d="M1300,900 q80,-60 180,0 l-20,40 q-70,30 -140,0 Z" fill="#6b3a26" {o(4)}/>')
    px, py, pw, ph_ = 640, 460, 820, 480
    s += SL(Z_SRED, f'<path d="M{px:.0f},{py+ph_:.0f} L{px-20:.0f},{py+60:.0f} L{px+pw+20:.0f},{py+60:.0f} L{px+pw:.0f},{py+ph_:.0f} Z"'
                    f' fill="{KREM}" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{px+60:.0f},{py+100:.0f} q30,-60 60,0" fill="none" stroke="{ZEL}" stroke-width="6"/>')
    put = kontur_proema(px + 20, py + 60, pw - 40, ph_ - 120, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px + 20, py + 60, pw - 40, ph_ - 120, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(5)}/>')
    ded = figura(500, 1020, 420, t, KRAS, "#efe3c8", False, .0, True, boroda=True)
    s += SL(Z_SRED, ded)
    ruk1, (r1x, r1y) = rukav(560, 860, 150, -40, t, KRAS, "#efe3c8", .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(440, 860, 150, -140, t, KRAS, "#efe3c8", .3, 2)
    s += SL(Z_SRED, ruk1b)
    stoy = figura(960, 1060, 320, t, "#4a5a6b", "#cfe4f5", False, .3)
    s += SL(Z_SRED, stoy)
    tyanet = A.ease(A.seg(t % 3.0, .3, 2.0))
    ruk2, (r2x, r2y) = rukav(900, 940, 140, -50 - tyanet * 20, t, "#4a5a6b", "#cfe4f5", .3, 2)
    s += SL(Z_SRED, ruk2)
    ushi2 = 6 * A.w(t, 1.3)
    s += SL(Z_SRED, f'<path d="M930,{860+ushi2:.0f} l-8,-24 M990,{860+ushi2:.0f} l8,-24" stroke="{KREM}" stroke-width="5" fill="none"/>')
    mesh_sw = 4 * A.w(t, 1.1)
    s += SL(Z_SRED, f'<path d="M{1700+mesh_sw:.0f},860 q60,10 50,100" fill="none" stroke="#6b3a26" stroke-width="30" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<rect x="1700" y="880" width="180" height="140" rx="20" fill="#6b3a26" {o(4)}/>')
    s += SL(Z_SRED, svecha(586, 854, t, 0.46, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#1a0e08", .32))
    s += vinetka(.34)
    return s


def paket_v_shkolnom_koridore(t):
    s = f'<rect width="{W}" height="{H}" fill="#2a2a30"/>'
    s += SL(Z_DAL, kladka(0, 0, W, 900, 80, "url(#kamen)"))
    for i in range(5):
        s += SL(Z_DAL, f'<rect x="{200+i*340}" y="200" width="30" height="620" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1400" y="200" width="420" height="700" fill="#1a1410" opacity=".85" {o(5)}/>')
    for h in range(6):
        s += SL(Z_SRED, f'<path d="M1420,{250+h*100:.0f} h380" stroke="{DOSKA}" stroke-width="10"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1440+i*110}" y="560" width="90" height="180" rx="8" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="500" width="200" height="320" rx="6" fill="{ZHELEZ}" {o(4)}/>')
    stup = (t * 60) % 400
    stoy_y = 760 + stup * .5
    boy = figura(900, stoy_y, 440, t, KREM, "#2a4a3a", False, .2)
    s += SL(Z_SRED, boy)
    ruk1, (r1x, r1y) = rukav(900, stoy_y - 320, 120, -40, t, KREM, "#2a4a3a", .2, 2)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<path d="M820,{stoy_y-100:.0f} v{-stup*.4:.0f}" stroke="{ZHELEZ}" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="{r1x-40:.0f}" y="{r1y-20:.0f}" width="80" height="60" fill="#6b3a26" {o(2)}/>')
    struyka_y = r1y - 60 - ((t * 40) % 300)
    s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y-30:.0f} q20,{-(r1y-30-struyka_y)*.3:.0f} 10,{struyka_y-r1y+30:.0f}"'
                    f' fill="none" stroke="#e8812a" stroke-width="6" opacity="{max(0,1-((t*40)%300)/300):.2f}"/>')
    s += SL(Z_SRED, f'<circle cx="{r1x+10:.0f}" cy="{struyka_y:.0f}" r="10" fill="{ZOL}" opacity="{max(0,1-((t*40)%300)/300):.2f}"/>')
    pov = 6 * A.w(t, 1.6)
    s += SL(Z_SRED, siluet(1600, 300, 220, "#0e0c10", .8))
    s += SL(Z_SRED, f'<g transform="rotate({pov:.1f} 1600 280)"><circle cx="1600" cy="280" r="4" fill="none"/></g>')
    s += SL(Z_SRED, f'<circle cx="960" cy="260" r="40" fill="{SVET}" opacity=".3"/>')
    s += SL(Z_SRED, svecha(809, 761, t, 0.81, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0c0c10", .4))
    s += vinetka(.42)
    return s


def paket_nesut_domoy(t):
    s = f'<rect width="{W}" height="{H}" fill="{NOCH}"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 45))
    s += SL(Z_DAL, izba_snaruzhi(1500, 900, 460, t, True, True, 7))
    s += SL(Z_DAL, f'<rect x="300" y="700" width="30" height="240" fill="{ZHELEZ}" {o(3)}/><ellipse cx="315" cy="690" rx="40" ry="16" fill="{SVET}" opacity=".8"/>')
    s += SL(Z_SRED, sneg_lezhit(880))
    s += SL(Z_SRED, pleten(1100, 800, 420, 140))
    s += SL(Z_SRED, f'<path d="M700,900 q200,-10 400,0" fill="none" stroke="{SNEG}" stroke-width="40" opacity=".6"/>')
    put = (t * 60) % 600
    boy = figura(300 + put, 1000, 460, t, "#2a4a5a", "#cfd6de", True, .0)
    s += SL(Z_SRED, boy)
    ruk1, (r1x, r1y) = rukav(380 + put, 706, 150, -40, t, "#2a4a5a", "#cfd6de", .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(220 + put, 706, 150, -140, t, "#2a4a5a", "#cfd6de", .3, 2)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<rect x="{(r1x+r1bx)/2-60:.0f}" y="{(r1y+r1by)/2+60:.0f}" width="120" height="70" rx="8" fill="#6b3a26" {o(3)}/>')
    girl = figura(1100, 1000, 300, t, "#8c3a3a", "#cfe4f5", True, .3)
    s += SL(Z_SRED, girl)
    tyanet = A.ease(A.seg(t % 4.0, 1.0, 1.0))
    ruk2, (r2x, r2y) = rukav(1180, 810, 110, -40 - tyanet * 10, t, "#8c3a3a", "#cfe4f5", .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, _varezhka(r2x, r2y, 1.1, 0, KRAS))
    if tyanet > .8:
        s += SL(Z_SRED, f'<rect x="{r2x-20:.0f}" y="{r2y-30:.0f}" width="40" height="18" rx="4" fill="{KREM}" {o(2)}/>')
    sobaka_x = 1300 + 20 * math.sin(t * 2)
    s += SL(Z_SRED, f'<ellipse cx="{sobaka_x:.0f}" cy="960" rx="60" ry="30" fill="#6b4a3a" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#040608", .42))
    s += SL(Z_LETIT, mokryy_sneg(t, 10, 47, .3, .5))
    s += vinetka(.46)
    return s


def konfety_po_poryadku(t):
    s = f'<rect width="{W}" height="{H}" fill="{DOSKA2}"/>'
    s += SL(Z_DAL, teplo(960, 300, 1200, 700, .3))
    s += SL(Z_SRED, f'<rect x="0" y="500" width="{W}" height="{H-500}" fill="{DOSKA}" {o(4)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{300+i*70}" cy="700" r="20" fill="{(KRAS,ZOL)[i%2]}" {o(2)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1100+i*80}" y="680" width="60" height="40" rx="6" fill="#6b4a2e" {o(2)}/>')
    otodv = A.ease(A.seg(t, .3, 1.4)) * 80
    s += SL(Z_SRED, f'<g transform="translate({otodv:.0f},0)">'
                    + ''.join(f'<rect x="{1060+i*80}" y="680" width="60" height="40" rx="6" fill="{TKAN}" opacity=".9" {o(2)}/>' for i in range(3))
                    + '</g>')
    s += SL(Z_SRED, f'<circle cx="760" cy="700" r="30" fill="{ZOL}" {o(2)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{900+i*18:.0f},700 q8,-16 0,-32" fill="none" stroke="#6b4a2e" stroke-width="4"/>')
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="700" rx="60" ry="30" fill="#efe3c8" opacity=".8" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1600" y="680" width="80" height="40" rx="6" fill="{KREM}" opacity=".5" {o(2)}/>')
    drozh = 3 * A.w(t, 2.4)
    s += SL(Z_SRED, f'<ellipse cx="{200+drozh:.0f}" cy="700" rx="60" ry="24" fill="{STEKLO}" opacity=".6" {o(2)}/>')
    rukx = 500
    ruk1, (r1x, r1y) = rukav(rukx, 500, 140, 70, t, KREM, KRAS, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(1140, 500, 140, 110, t, KREM, KRAS, .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, svecha(302, 838, t, 0.82, .8))
    s += SL(Z_SRED, _napolnenie(60, 560, 1800, 100, t, 203, 16))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .34))
    s += vinetka(.38)
    return s


def otkrytki_na_servante(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 49)
    s += SL(Z_DAL, okno_izby(1500, 160, 300, 300, t, svet=False, moroz=.2))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _servant(1120, 480, 420, 500, t))
    rnd = random.Random(104)
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{1150+i*54}" y="{860-i%2*10}" width="46" height="60" rx="3" fill="{(KRAS,KREM)[i%2]}" {o(2)}/>')
    s += SL(Z_SRED, stol(420, 760, 640, 34))
    s += SL(Z_SRED, lampa(500, 680, t, 1.0, True))
    s += SL(Z_SRED, f'<rect x="640" y="700" width="200" height="30" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="680" width="80" height="24" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, figura(560, 1040, 480, t, "#6b2a44", KREM, True, .2))
    ruk1, (r1x, r1y) = rukav(620, 780, 140, -30, t, "#6b2a44", KREM, .2, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(500, 780, 140, -150, t, "#6b2a44", KREM, .5, 2)
    s += SL(Z_SRED, ruk2)
    pero = A.seg(t % 3.0, .3, 2.4)
    s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y:.0f} h{-80*pero:.0f}" stroke="#2a1d14" stroke-width="3" stroke-dasharray="5 4"/>')
    marka = A.ease(A.seg(t, 2.6, .6))
    s += SL(Z_SRED, f'<rect x="{800-10*marka:.0f}" y="{690:.0f}" width="26" height="30" fill="{ZOL}" opacity="{marka:.2f}" {o(1)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.4)
    return s


def odekolon_v_korobochke(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 105)
    s += SL(Z_DAL, _oboi_fon("#4a4a4a", "#3a3a3a"))
    s += SL(Z_SRED, polovicy(840))
    zx, zy = 960, 500
    s += SL(Z_SRED, f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="220" fill="url(#zol)" {o(5)}/>')
    put = kontur_proema(zx - 190, zy - 190, 380, 380, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(zx - 190, zy - 190, 380, 380, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="680" width="400" height="60" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M740,680 q30,-30 60,0" fill="none" stroke="{SVET}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="820" y="630" width="30" height="50" rx="4" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M880,650 q30,10 30,40" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    kx, ky = 1200, 640
    s += SL(Z_SRED, _korobka(kx, ky, 220, 150, t, TKAN2, ZOL, True, .55, .1))
    flak = A.ease(A.seg(t, .3, .8))
    s += SL(Z_SRED, f'<rect x="{kx+80+flak*120:.0f}" y="{ky-60-flak*40:.0f}" width="36" height="70" rx="8" fill="{STEKLO}" opacity=".8" {o(3)}/>')
    zakr = A.ease(A.seg(t, 1.4, .8))
    s += SL(Z_SRED, f'<rect x="{kx-30:.0f}" y="{ky-40*(1-zakr):.0f}" width="150" height="20" fill="{KREM}" opacity="{zakr:.2f}"/>')
    polka_y = 320
    s += SL(Z_SRED, f'<rect x="1150" y="{polka_y:.0f}" width="260" height="30" rx="4" fill="url(#derev)" {o(4)}/>')
    vstal = A.ease(A.seg(t, 2.2, .8))
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1170+i*70}" y="{polka_y-40-vstal*10*0:.0f}" width="50" height="40" rx="4" fill="{(TKAN2,MED,ZEL2)[i]}" opacity=".9" {o(2)}/>')
    s += SL(Z_SRED, figura(600, 1060, 480, t, KREM, KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(660, 820, 140, -30, t, KREM, KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, svecha(515, 825, t, 0.05, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def dva_flakona_na_vidnom_meste(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 106)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _servant(760, 420, 420, 440, t))
    s += SL(Z_SRED, f'<rect x="760" y="860" width="420" height="30" rx="10" fill="{KREM}" {o(3)}/>')
    bx1, bx2 = 820, 1020
    otkr = A.ease(A.seg(t, .3, .8))
    s += SL(Z_SRED, f'<rect x="{bx1:.0f}" y="860" width="140" height="100" rx="10" fill="{TKAN2}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{bx1+20:.0f}" y="{860-otkr*30:.0f}" width="100" height="30" fill="{TKAN2}" opacity="{1-otkr:.2f}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{bx2:.0f}" y="860" width="110" height="80" rx="10" fill="{KRAS}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{bx2+55:.0f},860 q20,-20 0,-40" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<ellipse cx="1300" cy="700" rx="60" ry="30" fill="url(#zol)" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1420" cy="760" rx="50" ry="60" fill="{POBEL}" {o(3)}/><rect x="1400" y="700" width="40" height="30" rx="4" fill="#efe3c8" {o(2)}/>')
    stoy1 = figura(600, 1040, 470, t, "#8c3a6a", KREM, False, .0)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(680, 860, 140, -40, t, "#8c3a6a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    stoy2 = figura(1180, 1060, 480, t, "#3a3a5a", "#cfd6de", False, .3, True, shapka=True)
    s += SL(Z_SRED, f'<g transform="translate(0,{-10*(1-otkr):.0f})">{stoy2}</g>')
    nyuh = A.ease(A.seg(t, 1.6, 1.0))
    s += SL(Z_SRED, f'<g transform="rotate({-10*nyuh:.1f} 1100 900)">'
                    f'<ellipse cx="1100" cy="900" rx="20" ry="14" fill="#e0b08a" {o(2)}/></g>')
    s += SL(Z_SRED, svecha(385, 825, t, 1.85, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


# ═══════════════════════════ 109-121 ══════════════════════════════
def chto_govoryat_podarki(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 111)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="160" y="700" width="1600" height="60" rx="10" fill="url(#derev)" {o(5)}/>')
    items = [("chasy", 280, "grust"), ("nozh", 560, "grust"), ("platok", 840, "grust"),
             ("koshelek", 1120, "pusto"), ("banka", 1500, "radost")]
    for kind, gx, mood in items:
        if kind == "chasy":
            s += SL(Z_SRED, _chasy_sten(gx, 660, .6, t))
        elif kind == "nozh":
            s += SL(Z_SRED, _nozh_bolshoy(gx, 700, 90, t))
        elif kind == "platok":
            s += SL(Z_SRED, f'<rect x="{gx-30:.0f}" y="660" width="60" height="60" fill="{TKAN}" {o(2)}/>')
        elif kind == "koshelek":
            s += SL(Z_SRED, _koshelek(gx, 700, .9))
        else:
            s += SL(Z_SRED, _banka(gx, 700, .9, RUSH))
        app = A.ease(A.seg(t, items.index((kind, gx, mood)) * .9, .6))
        if app > .1:
            s += SL(Z_SRED, f'<g opacity="{app:.2f}">' + _oblako_rechi(gx, 560, .8 if mood != "radost" else 1.1, t, items.index((kind, gx, mood)) * .2, mood) + '</g>')
    s += SL(Z_SRED, svecha(200, 700, t, .3, .9))
    s += SL(Z_SRED, svecha(1780, 700, t, .5, .9))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def monetka_i_gorst_konfet(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 119)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 760, 1200, 34))
    s += SL(Z_SRED, _korobka(560, 660, 200, 140, t, TKAN2, ZOL, True, .0, .1))
    s += SL(Z_SRED, f'<path d="M1200,700 v-80 q0,-20 40,-20 q40,0 40,20 v80 Z" fill="{STEKLO}" opacity=".5" {o(4)}/>')
    app1 = A.ease(A.seg(t, .3, .6))
    s += SL(Z_SRED, f'<circle cx="640" cy="{650-(1-app1)*100:.0f}" r="16" fill="url(#zol)" {o(2)}/>')
    if app1 > .95:
        s += SL(Z_SRED, _galochka(560, 600, .8, t, 0))
    app2 = A.ease(A.seg(t, 1.3, .8))
    for i in range(int(6 * app2)):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<circle cx="{1240+rnd.random()*40:.0f}" cy="{620+rnd.random()*40:.0f}" r="10" fill="{(KRAS,ZOL)[i%2]}"/>')
    if app2 > .95:
        s += SL(Z_SRED, _galochka(1240, 560, .8, t, .3))
    s += SL(Z_SRED, f'<path d="M900,660 l-30,-70 l60,0 Z" fill="{ZEL}" {o(3)}/>')
    s += SL(Z_SRED, svecha(1000, 700, t, .4, .9))
    ruk1, (r1x, r1y) = rukav(640, 500, 160, 100, t, "#5a4a3a", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(1280, 500, 160, 80, t, "#5a4a3a", KREM, .4, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, _napolnenie(60, 560, 260, 120, t, 205, 2))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def korobka_detskih_sokrovisch(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 121)
    s += SL(Z_DAL, _elka(1600, 960, 480, t, 53))
    s += SL(Z_SRED, f'<rect x="700" y="860" width="500" height="200" rx="16" fill="#efe3c8" opacity=".3" {o(2)}/>')
    kx, ky = 940, 820
    s += SL(Z_SRED, f'<rect x="{kx-180:.0f}" y="{ky:.0f}" width="360" height="200" rx="10" fill="#9c7049" opacity=".9" {o(5)}/>')
    dostal = A.ease(A.seg(t, .3, 1.0))
    mx, my = kx - 40, ky - dostal * 160
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="50" ry="40" fill="#8c6a4a" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{mx-20:.0f}" cy="{my-10:.0f}" r="20" fill="#8c6a4a" {o(2)}/>')
    s += SL(Z_SRED, f'<circle cx="{mx+26:.0f}" cy="{my-18:.0f}" r="10" fill="#8c6a4a" {o(1)}/>')
    s += SL(Z_SRED, f'<circle cx="{kx+60:.0f}" cy="{ky+40:.0f}" r="34" fill="{STEKLO}" opacity=".6" {o(2)}/>')
    blik_k = (t * 90) % 360
    s += SL(Z_SRED, f'<line x1="{kx+60:.0f}" y1="{ky+40:.0f}" x2="{kx+60+30*math.cos(math.radians(blik_k)):.0f}"'
                    f' y2="{ky+40+30*math.sin(math.radians(blik_k)):.0f}" stroke="{SVET}" stroke-width="3" opacity=".7"/>')
    s += SL(Z_SRED, f'<circle cx="{kx+130:.0f}" cy="{ky+20:.0f}" r="20" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+150:.0f}" y="{ky+60:.0f}" width="50" height="40" rx="4" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, figura(900, 1080, 440, t, "#8c8a94", KREM, False, .0, False, False, 0, False, False))
    ruk1, (r1x, r1y) = rukav(840, 860, 130, -60, t, "#8c8a94", KREM, .0, 2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(960, 860, 130, -120, t, "#8c8a94", KREM, .3, 2)
    s += SL(Z_SRED, ruk2)
    prizh = A.ease(A.seg(t, 1.6, 1.0))
    s += SL(Z_SRED, f'<ellipse cx="{(r1x+r2x)/2:.0f}" cy="{(r1y+r2y)/2-prizh*60:.0f}" rx="30" ry="24" fill="#8c6a4a" opacity="{.4+.6*prizh:.2f}" {o(2)}/>')
    kot(300, 940, t, .9, "#3b3430", False)
    s += SL(Z_SRED, kot(300, 940, t, .9, "#3b3430", False))
    vopros = A.ease(A.seg(t, 2.4, .6))
    if vopros > .1:
        s += SL(Z_SRED, f'<g opacity="{vopros:.2f}"><ellipse cx="1500" cy="320" rx="140" ry="80" fill="#ffffff" opacity=".9" {o(3)}/>'
                        f'<text x="1500" y="340" font-size="60" text-anchor="middle" fill="{K}">?</text></g>')
    s += SL(Z_SRED, svecha(650, 770, t, 1.7, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def chetyre_podarka_na_podokonnike(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, _oboi_fon("#4a3a3a", "#3a2e2e"))
    px, py, pw, ph_ = 560, 260, 800, 340
    s += SL(Z_DAL, f'<rect x="{px-30:.0f}" y="{py-30:.0f}" width="{pw+60}" height="{ph_+60}" rx="10" fill="url(#derev)" {o(7)}/>')
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_DAL, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_DAL, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_DAL, f'<path d="{put}" fill="none" {o(8)}/>')
    s += SL(Z_DAL, f'<line x1="{px+pw/2:.0f}" y1="{py:.0f}" x2="{px+pw/2:.0f}" y2="{py+ph_:.0f}" stroke="#2a1d14" stroke-width="6"/>')
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="{px-20:.0f}" y="{py+ph_:.0f}" width="{pw+40}" height="60" rx="8" fill="url(#derev)" {o(5)}/>')
    items = [("konvert", px + 60), ("varezhki", px + 280), ("banka", px + 500), ("blyudce", px + 700)]
    for i, (kind, ix) in enumerate(items):
        glow = .4 + .6 * max(0, 1 - abs(((t * .3) % 4) - i))
        if kind == "konvert":
            s += SL(Z_SRED, f'<rect x="{ix-40:.0f}" y="{py+ph_-10:.0f}" width="80" height="55" rx="4" fill="{KRAS}" opacity="{.7+.3*glow:.2f}" {o(3)}/>')
        elif kind == "varezhki":
            s += SL(Z_SRED, _varezhka(ix, py + ph_ + 20, .9, -8, KRAS))
            s += SL(Z_SRED, _varezhka(ix + 50, py + ph_ + 24, .9, 8, KRAS))
        elif kind == "banka":
            s += SL(Z_SRED, _banka(ix, py + ph_ + 36, .7, RUSH))
        else:
            s += SL(Z_SRED, f'<ellipse cx="{ix:.0f}" cy="{py+ph_+40:.0f}" rx="40" ry="14" fill="{KREM}" opacity="{.7+.3*glow:.2f}" {o(2)}/>'
                            f'<circle cx="{ix:.0f}" cy="{py+ph_+32:.0f}" r="10" fill="url(#zol)"/>')
        s += SL(Z_SRED, f'<ellipse cx="{ix:.0f}" cy="{py+ph_+40:.0f}" rx="60" ry="20" fill="{SVET}" opacity="{glow*.3:.2f}"/>')
    s += SL(Z_SRED, zanaveska(px - 60, py - 20, ph_ + 80, 100, TKAN, t, -1))
    s += SL(Z_SRED, zanaveska(px + pw + 60, py - 20, ph_ + 80, 100, TKAN, t, 1))
    s += SL(Z_SRED, kot(1500, 900, t, .9, "#3b3430", False))
    s += SL(Z_SRED, svecha(1600, 800, t, .4, 1.0))
    s += SL(Z_SRED, f'<path d="M1700,760 l-30,-70 l60,0 Z" fill="{ZEL}" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#040608", .38))
    s += vinetka(.42)
    return s
