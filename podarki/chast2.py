# -*- coding: utf-8 -*-
"""Декорации 35-68 ролика «Что дарить на Новый год 2027».
План 9/63 «monetka_za_podarok» уже написан в chast1.py — не дублируется."""
import math, random
from baza import *
import anim as A
from lok_obshchee import (figura, rukav, siluet, mokryy_sneg, goloe_derevo,
                           gryaz_polosa, para_izo_rta, sumerki_fon,
                           grozd_ryabiny, tusklaya_lampochka, kirpich_ustya)
from chast1 import (_korobka, _svertok, _varezhka, _banka, _svistulka,
                     _oblachko, _chasy_sten, _chasy_karman, _servant,
                     _shkaf_proem, _zapret, _galochka, _koshelek, _elka,
                     _napolnenie, _chertenok, _vesy, _kovrik_pol,
                     _kartiny_ryad, _oboi_fon, _nozh_bolshoy, _nozhnicy_bolshie,
                     _veshalka_seni, _dvertsy_shkafa)

IMP2 = "#3a2a4a"


# ───────────────────────── МЕСТНЫЕ КИРПИЧИКИ ПОРЦИИ ─────────────────────────
def _samovar(x, y, s_, t, par_on=True):
    s = ten(x, y + 90 * s_, 60 * s_, 14 * s_, .4)
    s += f'<ellipse cx="{x:.0f}" cy="{y+70*s_:.0f}" rx="56*{s_:.0f}" ry="14" fill="url(#zol)" {o(4)}/>'.replace("56*", "")
    s += (f'<path d="M{x-54*s_:.0f},{y+70*s_:.0f} q{-6*s_:.0f},{-120*s_:.0f} 54*{s_:.0f},{-126*s_:.0f}'
          .replace("54*", "") + f' q{60*s_:.0f},6 {54*s_:.0f},{126*s_:.0f} Z" fill="url(#zol)" {o(5)}/>')
    s += f'<rect x="{x-14*s_:.0f}" y="{y-86*s_:.0f}" width="{28*s_:.0f}" height="{18*s_:.0f}" rx="4" fill="url(#zol)" {o(3)}/>'
    s += f'<circle cx="{x-50*s_:.0f}" cy="{y:.0f}" r="{10*s_:.0f}" fill="{ZHELEZ}" {o(2)}/>'
    s += f'<circle cx="{x+50*s_:.0f}" cy="{y:.0f}" r="{10*s_:.0f}" fill="{ZHELEZ}" {o(2)}/>'
    s += f'<rect x="{x-6*s_:.0f}" y="{y+30*s_:.0f}" width="{12*s_:.0f}" height="{10*s_:.0f}" fill="{ZHELEZ}" {o(2)}/>'
    if par_on:
        s += par(x, y - 92 * s_, t, 3, .45, 90 * s_, .5)
    return s


def _tryumo_otrazhenie(x, y, s_, t, vid):
    """Мини-фигура внутри створки трюмо: `vid` — young|staraya|babka."""
    if vid == "babka":
        fig = figura(x, y, 210 * s_, t, "#5a5560", "#cfd6de", True, .0, False, 1.0, False, 0, True, True)
        ruk, _ = rukav(x - 28 * s_, y - 150 * s_, 70 * s_, -120 + 20 * A.w(t, 1.2), t, "#5a5560", "#cfd6de", .0, 12)
        return fig + ruk
    col = "#6b2a44" if vid == "young" else "#4a3a4a"
    return figura(x, y, 210 * s_, t, col, "#ffd98a", False, .3 if vid == "young" else .0)


def _pryalka_stan(x, y, w_, h_, t):
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6" fill="url(#derev)" {o(5)}/>'
    for i in range(6):
        lx = x + w_ * .12 + i * w_ * .76 / 5
        sh = 3 * A.w(t, 1.1, i * .1)
        s += f'<line x1="{lx+sh:.0f}" y1="{y:.0f}" x2="{lx-sh:.0f}" y2="{y+h_:.0f}" stroke="{KREM}" stroke-width="3" opacity=".8"/>'
    return s


def _schyoty(x, y, s_, t):
    s = f'<rect x="{x-60*s_:.0f}" y="{y-50*s_:.0f}" width="{120*s_:.0f}" height="{100*s_:.0f}" rx="6" fill="url(#derev)" {o(5)}/>'
    for row in range(4):
        ry = y - 30 * s_ + row * 20 * s_
        sh = 18 * s_ * A.w(t, 1.6, row * .2)
        for i in range(4):
            s += f'<circle cx="{x-40*s_+i*26*s_+sh*((i%2)*2-1)*.3:.0f}" cy="{ry:.0f}" r="{8*s_:.0f}" fill="{ZOL}" {o(2)}/>'
    return s


def _pochta_yashchiki(x, y, w_, h_, n=6):
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="4" fill="{ZHELEZ}" {o(5)}/>'
    for i in range(n):
        cx_ = x + (i % 3 + .5) * w_ / 3
        cy_ = y + (i // 3 + .5) * h_ / 2
        s += f'<rect x="{cx_-w_/7:.0f}" y="{cy_-h_/6:.0f}" width="{w_/3.5:.0f}" height="{h_/3.5:.0f}" rx="3" fill="#3a3e44" {o(2)}/>'
    return s


def _rusalka(x, y, h_, t):
    """Русалка сидит на камне: хвост свёрнут у бедра, торс и плечи,
    обеими руками закрывает лицо, волосы падают по спине. `y` — уровень
    камня под бёдрами, `h_` — рост от бедра до макушки."""
    plach = A.seg(t % 3.0, 0, 2.0)
    kach = 2 * A.w(t, 1.1)
    hip = (x, y)
    s = ten(x - h_ * .1, y + h_ * .04, h_ * .55, 14, .45)
    # хвост: плавная дуга-«колбаска» от бедра влево, веер-плавник на конце
    s += (f'<path d="M{x-h_*.04:.0f},{y+h_*.02:.0f}'
          f' Q{x-h_*.42:.0f},{y+h_*.1:.0f} {x-h_*.68:.0f},{y-h_*.1+kach:.0f}'
          f' Q{x-h_*.42:.0f},{y-h_*.22:.0f} {x-h_*.08:.0f},{y-h_*.14:.0f} Z"'
          f' fill="url(#led)" {o(5)}/>')
    fx, fy = x - h_ * .7, y - h_ * .1 + kach
    s += (f'<path d="M{fx:.0f},{fy:.0f} l{-h_*.16:.0f},{-h_*.14:.0f} l{h_*.05:.0f},{h_*.13:.0f}'
          f' l{-h_*.18:.0f},{h_*.01:.0f} l{h_*.18:.0f},{h_*.11:.0f} l{-h_*.05:.0f},{h_*.12:.0f} Z"'
          f' fill="#9fc4d8" {o(3)}/>')
    # торс: от бедра вверх к плечам, тот же силуэт одним плавным телом
    tcx, tcy = x + h_ * .02, y - h_ * .34
    s += f'<ellipse cx="{tcx:.0f}" cy="{tcy:.0f}" rx="{h_*.17:.0f}" ry="{h_*.24:.0f}" fill="#e0b08a" {o(5)}/>'
    shx, shy = tcx, y - h_ * .54
    # волосы: прядь от затылка вдоль спины
    s += (f'<path d="M{shx+h_*.1:.0f},{shy-h_*.06:.0f} q{h_*.14:.0f},{h_*.2:.0f} {h_*.04:.0f},{h_*.42:.0f}'
          f' q{-h_*.04:.0f},{h_*.14:.0f} {-h_*.16:.0f},{h_*.14:.0f}'
          f' q{h_*.1:.0f},{-h_*.18:.0f} {h_*.02:.0f},{-h_*.5:.0f} Z" fill="#caa64a" {o(4)}/>')
    # голова — вплотную к плечам, без зазора
    hcx, hcy = shx, shy - h_ * .13
    s += f'<ellipse cx="{hcx:.0f}" cy="{hcy:.0f}" rx="{h_*.12:.0f}" ry="{h_*.13:.0f}" fill="#e0b08a" {o(5)}/>'
    s += (f'<path d="M{hcx-h_*.1:.0f},{hcy-h_*.05:.0f} q{-h_*.02:.0f},{-h_*.14:.0f} {h_*.1:.0f},{-h_*.17:.0f}'
          f' q{h_*.1:.0f},{-h_*.01:.0f} {h_*.1:.0f},{h_*.1:.0f} Z" fill="#caa64a" {o(3)}/>')
    # руки закрывают лицо: от плеч к подбородку, кисти сходятся перед лицом
    for sgn in (-1, 1):
        ruka_d = (f'M{shx+sgn*h_*.12:.0f},{shy:.0f}'
                  f' Q{shx+sgn*h_*.1:.0f},{hcy+h_*.02:.0f} {hcx+sgn*h_*.03:.0f},{hcy+h_*.03:.0f}')
        s += f'<path d="{ruka_d}" fill="none" stroke="{K}" stroke-width="{h_*.08:.0f}" stroke-linecap="round"/>'
        s += f'<path d="{ruka_d}" fill="none" stroke="#e0b08a" stroke-width="{h_*.062:.0f}" stroke-linecap="round"/>'
    if plach < .7:
        dy = plach * h_ * .5
        s += f'<circle cx="{hcx:.0f}" cy="{hcy+h_*.1+dy:.0f}" r="{h_*.017:.0f}" fill="#cfe8ff" opacity="{1-plach:.2f}"/>'
    else:
        s += f'<circle cx="{hcx:.0f}" cy="{y-h_*.1:.0f}" r="{h_*.024:.0f}" fill="{SNEG}" {o(2)}/>'
    return s


def _primeta_vorona(x, y, s_, t, uhodit=0.0):
    off = uhodit * 260 * s_
    s = f'<g transform="translate({off:.0f},0)">'
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{36*s_:.0f}" ry="{48*s_:.0f}" fill="#2a2a32" {o(4)}/>'
    s += f'<path d="M{x:.0f},{y-30*s_:.0f} l{14*s_:.0f},{-10*s_:.0f} l{-4*s_:.0f},{10*s_:.0f} Z" fill="{K}"/>'
    ug = -40 * (1 - uhodit)
    s += (f'<path d="M{x-10*s_:.0f},{y-10*s_:.0f} l{70*s_:.0f},{ug*s_:.0f}" stroke="{ZHELEZ}"'
          f' stroke-width="{4*s_:.0f}"/>')
    pleso = (1 - uhodit) * 20 * A.w(t, 1.6)
    s += f'<path d="M{x-30*s_:.0f},{y:.0f} q{-20*s_:.0f},{pleso:.0f} {-10*s_:.0f},{30*s_:.0f}" fill="none" stroke="#2a2a32" stroke-width="{8*s_:.0f}"/>'
    if uhodit > .5:
        s += f'<ellipse cx="{x-50*s_:.0f}" cy="{y+20*s_:.0f}" rx="{14*s_:.0f}" ry="{10*s_:.0f}" fill="{ZHELEZ}" {o(2)}/>'
    s += f'<rect x="{x-20*s_:.0f}" y="{y+40*s_:.0f}" width="{40*s_:.0f}" height="{18*s_:.0f}" fill="{TKAN2}" {o(2)}/>'
    return s + '</g>'


# ═══════════════════════════ ДЕКОРАЦИИ 36-38 ══════════════════════════════
# план 35 «struzhka_i_svistulka» уже написан в chast1.py — не дублируется.
def babushkin_nozh_poloska(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("den", t, False, 8)
    s += SL(Z_DAL, okno_izby(1500, 140, 260, 260, t, svet=False, moroz=.2))
    s += utvar_izby(80, 420, 420, t, 17)
    s += SL(Z_SRED, polovicy(780))
    s += SL(Z_SRED, stol(520, 700, 900, 34))
    s += SL(Z_SRED, kartoshka(900, 700, t, 7, 9))
    s += SL(Z_SRED, f'<circle cx="760" cy="696" r="46" fill="{TKAN}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1080" cy="690" rx="90" ry="34" fill="{MED}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="600" y="650" width="80" height="28" rx="6" fill="{KAMEN}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1240,660 v60" stroke="{STEKLO}" stroke-width="30" opacity=".7"/>')
    s += SL(Z_SRED, f'<path d="M560,640 q40,-10 80,0 l0,30 q-40,10 -80,0 Z" fill="{RUSH}" {o(3)}/>')
    nx, ny = 700, 650
    s += SL(Z_SRED, f'<g transform="rotate({2*A.w(t,1.1):.1f} {nx:.0f} {ny:.0f})">'
                    f'<rect x="{nx-110:.0f}" y="{ny-10:.0f}" width="80" height="22" rx="8" fill="#2a1d14" {o(4)}/>'
                    f'<path d="M{nx-10:.0f},{ny-2:.0f} L{nx+150:.0f},{ny:.0f} L{nx-10:.0f},{ny+2:.0f} Z"'
                    f' fill="{ZHELEZ}" {o(2)}/><line x1="{nx-80:.0f}" y1="{ny:.0f}" x2="{nx-40:.0f}" y2="{ny:.0f}"'
                    f' stroke="#eef4fa" stroke-width="2" opacity=".5"/></g>')
    s += SL(Z_SRED, figura(560, 960, 480, t, "#6b4a3a", KREM, True, .2))
    ruk1, (r1x, r1y) = rukav(640, 700, 150, -40, t, "#6b4a3a", KREM, .2)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(560, 690, 170, -10, t, "#6b4a3a", KREM, .5)
    s += SL(Z_SRED, ruk2)
    kozhura = A.seg(t % 4.0, 0, 3.6)
    ln = kozhura * 260
    s += SL(Z_SRED, f'<path d="M{r2x:.0f},{r2y:.0f} q{40:.0f},{20:.0f} {30:.0f},{60:.0f}'
                    f' q{-10:.0f},{40:.0f} {30:.0f},{50:.0f}" fill="none" stroke="{POL}"'
                    f' stroke-width="5" stroke-dasharray="{ln:.0f} 400"/>')
    s += SL(Z_SRED, _napolnenie(1200, 540, 500, 200, t, 36, 6))
    s += SL(Z_SRED, svecha(120, 760, t, 0.0, .8))
    s += SL(Z_PERED, ramka_pp("levo", "#120e0e", .4))
    s += vinetka(.4)
    return s


def nabor_nosovyh_platkov(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 12)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(420, 720, 1100, 34))
    bx, by, bw, bh = 700, 560, 520, 160
    s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw}" height="{bh}" rx="12" fill="{KREM}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{bx+16:.0f}" y="{by+16:.0f}" width="{bw-32}" height="{bh-32}" rx="8" fill="url(#stekl)" opacity=".4" {o(3)}/>')
    for i in range(3):
        rot = -14 + i * 14
        s += SL(Z_SRED, f'<g transform="rotate({rot} {bx+140+i*110:.0f} {by+bh*.6:.0f})">'
                        f'<rect x="{bx+70+i*110:.0f}" y="{by+40:.0f}" width="120" height="100" fill="{TKAN}" {o(3)}/>'
                        f'<rect x="{bx+70+i*110+16:.0f}" y="{by+56:.0f}" width="88" height="68" fill="none"'
                        f' stroke="{KREM}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<rect x="{bx+bw-120:.0f}" y="{by+bh*.3:.0f}" width="110" height="70" rx="6" fill="{RUSH}" {o(3)}/>')
    lenta_sh = 6 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<line x1="{bx+bw-80:.0f}" y1="{by+bh*.3+10:.0f}" x2="{bx+bw-30+lenta_sh:.0f}" y2="{by+bh*.3+70:.0f}" stroke="{KRAS}" stroke-width="10"/>')
    drop_y = by - 40 + 16 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<path d="M{bx+bw*.5:.0f},{drop_y-30:.0f} q-18,22 0,40 q18,-18 0,-40 Z" fill="{STEKLO}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{bx-180:.0f}" y="{by+40:.0f}" width="140" height="190" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{bx+bw+40:.0f}" y="{by+60:.0f}" width="90" height="130" rx="6" fill="#efe3c8" {o(3)}/>')
    shisha_x = bx + 80 + 200 * ((t * 40) % 300) / 300
    s += SL(Z_SRED, f'<circle cx="{shisha_x:.0f}" cy="{by+bh+40:.0f}" r="18" fill="#6b4428" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{bx-60:.0f}" cy="{by+bh+30:.0f}" r="28" fill="{ZOL}" {o(3)}/>')
    s += SL(Z_SRED, begushchiy_blik(t, 6.0, .2, .18, 300))
    s += SL(Z_SRED, svecha(444, 796, t, 1.64, .8))
    s += SL(Z_SRED, _napolnenie(60, 560, 260, 120, t, 206, 2))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def yarmarochnyy_larek_s_platkami(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("den", t, True, 19)
    s += SL(Z_DAL, oblaka(t, 160, 3, 12, .4))
    s += SL(Z_DAL, _elka(260, 940, 440, t, 6))
    s += SL(Z_DAL, _elka(1760, 920, 400, t, 7))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="980" rx="900" ry="60" fill="{SNEG}" {o(4)}/>')
    lx, ly, lw, lh = 660, 320, 600, 520
    s += SL(Z_SRED, f'<path d="M{lx-40:.0f},{ly:.0f} L{lx+lw+40:.0f},{ly:.0f} L{lx+lw:.0f},{ly+80:.0f}'
                    f' L{lx:.0f},{ly+80:.0f} Z" fill="{TKAN}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{lx:.0f}" y="{ly+80:.0f}" width="{lw}" height="{lh-80}" fill="url(#derev)" {o(6)}/>')
    pw, ph_ = 800, 320
    px, py = lx + (lw - pw) / 2, ly + 140
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="{lx+40:.0f}" y="{ly+lh-40:.0f}" width="{lw-80}" height="60" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, _samovar(lx + 90, ly + lh - 10, .7, t))
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{lx+lw-180+i*34:.0f}" cy="{ly+lh-30:.0f}" r="14" fill="{MED}" {o(2)}/>')
    s += SL(Z_DAL, f'<path d="M1260,900 l60,-140 l60,140 Z" fill="{SNEG}" {o(3)}/>')
    s += SL(Z_DAL, f'<circle cx="1440" cy="860" r="40" fill="{SNEG}" {o(3)}/><circle cx="1440" cy="800" r="28" fill="{SNEG}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="120" y="780" width="200" height="130" rx="20" fill="{KREM}" {o(5)}/>')
    povorot = A.ease(A.seg(t % 6.0, 2.0, 1.4))
    razv = A.ease(A.seg(t % 6.0, .2, 1.4))
    stoy1 = figura(lx + 120, ly + lh + 60, 460, t, "#6b2a38", KREM, True, .0, True)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(lx + 197, ly + lh + 60 - 460 * .64, 130, -30, t, "#6b2a38", KREM, .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y:.0f} h{150*razv:.0f} v40 h{-150*razv:.0f} Z" fill="{KRAS}" {o(3)}/>')
    stoy2 = figura(1240 + povorot * 10, ly + lh + 80, 470, t, "#3a2a4a", KREM, False, .3, True)
    s += SL(Z_SRED, f'<g transform="rotate({povorot*18:.1f} 1240 {ly+lh+40:.0f})">{stoy2}</g>')
    bahroma = povorot * 40
    s += SL(Z_SRED, f'<path d="M1150,{ly+lh-80:.0f} q90,-20 180,0" fill="none" stroke="{KRAS}" stroke-width="40" opacity=".92"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<line x1="{1150+i*30:.0f}" y1="{ly+lh-60:.0f}" x2="{1150+i*30+bahroma:.0f}" y2="{ly+lh-20:.0f}" stroke="{KRAS}" stroke-width="4"/>')
    s += SL(Z_SRED, svecha(728, 812, t, 1.28, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#1a1a1a", .3))
    s += SL(Z_LETIT, sneg_letit(t, 26, 13, .5, .9))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 39-44 ══════════════════════════════
def platok_dlya_slez_i_shal_dlya_tepla(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W//2}" height="{H}" fill="{SUMER}"/>')
    s += SL(Z_SRED, f'<rect x="{W//2}" y="0" width="{W//2}" height="{H}" fill="{POL2}"/>')
    s += SL(Z_DAL, okno_izby(80, 120, 280, 300, t, svet=False, moroz=.2))
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{100+i*50}" y1="150" x2="{80+i*50}" y2="380" stroke="{STEKLO}" stroke-width="3" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="420" y="780" width="420" height="40" rx="10" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="460" y="700" width="340" height="90" rx="20" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="560" y="660" width="80" height="50" fill="#fff" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="860" cy="760" rx="34" ry="16" fill="#6b4428" {o(3)}/>')
    figl = figura(560, 1040, 480, t, "#2a3a55", "#cfd6de", False, .0)
    s += SL(Z_SRED, figl)
    ruk1, (rlx, rly) = rukav(620, 780, 150, -150, t, "#2a3a55", "#cfd6de", .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<rect x="{rlx-30:.0f}" y="{rly-16:.0f}" width="60" height="40" rx="10" fill="#fff" {o(3)}/>')
    s += SL(Z_DAL, okno_izby(W - 360, 120, 280, 300, t, svet=True, moroz=0))
    s += SL(Z_SRED, teplo(W - 220, 280, 240, 220, .4))
    s += SL(Z_SRED, kirpich_ustya(W - 360, 700, 220, 220, t))
    s += SL(Z_SRED, svecha(W - 760, 900, t, .3, 1.0))
    s += SL(Z_SRED, kot(W - 900, 980, t, 1.0, "#3b3430", False))
    figr = figura(W - 540, 1040, 480, t, "#6b2a38", SVET, True, .2, True)
    s += SL(Z_SRED, figr)
    shawl = .3 + .15 * A.w(t, 2.0)
    ruk2, (rrx, rry) = rukav(W - 470, 760, 160, -60 - shawl * 30, t, "#6b2a38", SVET, .2)
    s += SL(Z_SRED, ruk2)
    ruk3, (rr2x, rr2y) = rukav(W - 610, 760, 160, -120 + shawl * 30, t, "#6b2a38", SVET, .5)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, f'<rect x="{W-620:.0f}" y="800" width="60" height="60" rx="12" fill="{KAMEN}" {o(3)}/>')
    s += SL(Z_SRED, par(W - 620, 790, t, 3, .4, 90))
    s += SL(Z_PERED, f'<rect x="{W//2-4}" y="0" width="8" height="{H}" fill="{K}"/>')
    s += vinetka(.4)
    return s


def chto_v_podarochnyy_paket(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 15)
    s += SL(Z_DAL, _oboi_fon())
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, _veshalka_seni(1280, 300, 420, t, 4))
    s += SL(Z_SRED, f'<rect x="420" y="320" width="220" height="420" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="530" cy="460" rx="90" ry="140" fill="#cfd6de" opacity=".6" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="700" width="420" height="40" rx="10" fill="url(#derev)" {o(5)}/>')
    kx = 900
    s += SL(Z_SRED, f'<path d="M{kx-80:.0f},680 l20,-170 h120 l20,170 Z" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="510" rx="80" ry="20" fill="{TKAN2}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+140:.0f}" y="600" width="160" height="120" rx="10" fill="{KREM}" {o(4)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<circle cx="{kx+170+i*50:.0f}" cy="630" r="16" fill="{(KRAS,ZOL,ZEL2)[i]}" {o(2)}/>')
    s += SL(Z_SRED, figura(900, 1020, 480, t, "#7a5a6a", KREM, False, .0))
    plat_move = A.seg(t, .2, 1.0)
    ruk1, (r1x, r1y) = rukav(840, 760, 150, -170 + 20 * plat_move, t, "#7a5a6a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<rect x="{r1x-10:.0f}" y="{r1y-40*(1-plat_move):.0f}" width="80" height="60" rx="8" fill="{RUSH}" opacity="{1-plat_move:.2f}"/>')
    shal_in = A.ease(A.seg(t, 1.2, 1.0))
    ruk2, (r2x, r2y) = rukav(960, 760, 150, -10 - 20 * shal_in, t, "#7a5a6a", KREM, .4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<rect x="{r2x-40:.0f}" y="{r2y-30+shal_in*60:.0f}" width="90" height="36" rx="8" fill="{TKAN}" opacity=".9" {o(2)}/>')
    kach = 3 * A.w(t, 1.3)
    s += SL(Z_SRED, f'<circle cx="{700+kach:.0f}" cy="560" r="8" fill="{ZHELEZ}"/>')
    s += SL(Z_SRED, svecha(279, 871, t, 1.11, .8))
    s += SL(Z_PERED, ramka_pp("levo", "#120e14", .4))
    s += vinetka(.4)
    return s


def polotence_ot_sestry(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 17)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_DAL, okno_izby(120, 140, 280, 260, t, svet=True, moroz=.3))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _pryalka_stan(1500, 280, 220, 420, t))
    s += SL(Z_SRED, f'<path d="M1600,760 q-70,0 -70,60 q0,40 70,40 q70,0 70,-40 q0,-60 -70,-60 Z" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, kot(1700, 500, t, .9, "#3b3430", True))
    s += SL(Z_SRED, stol(300, 760, 700, 34))
    s += SL(Z_SRED, _samovar(500, 740, .8, t))
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{880+i*20:.0f},680 q{10*A.w(t,1.2,i*.2):.0f},-16 {20+i*20:.0f},0" fill="none" stroke="{ZEL2}" stroke-width="5"/>')
    s += SL(Z_SRED, _kovrik_pol(500, 900, 700, 120, TKAN, KREM, 31))
    pol_w = 360
    razv = A.ease(A.seg(t, .2, 1.4))
    cx, cy = 900, 680
    s += SL(Z_SRED, f'<rect x="{cx-pol_w*razv/2:.0f}" y="{cy:.0f}" width="{pol_w*razv:.0f}" height="90" fill="{KREM}" {o(4)}/>')
    petuh_on = .5 + .5 * abs(A.w(t, 1.0))
    if razv > .5:
        for i in range(3):
            s += SL(Z_SRED, f'<circle cx="{cx-pol_w*.3+i*pol_w*.3:.0f}" cy="{cy+45:.0f}" r="18" fill="{KRAS}" opacity="{petuh_on:.2f}"/>')
    s += SL(Z_SRED, figura(cx - pol_w * .5 - 40, 1020, 480, t, "#8c3a3a", KREM, True, .0))
    ruk1, _ = rukav(cx - pol_w * .4, 720, 130, -20, t, "#8c3a3a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    obnyat = A.ease(A.seg(t, 1.6, 1.0))
    ruk2, _ = rukav(cx - pol_w * .4 - 60, 740, 120 + obnyat * 60, 40 + obnyat * 30, t, "#8c3a3a", KREM, .4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, figura(cx + pol_w * .5 + 40, 1020, 470, t, "#3a5a4a", KREM, False, .3))
    ruk3, _ = rukav(cx + pol_w * .4, 720, 130, -160, t, "#3a5a4a", KREM, .3)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, par(500, 650, t, 3, .4, 80))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.4)
    return s


def polotence_ot_chuzhoy(t):
    s = f'<rect width="{W}" height="{H}" fill="{SUMER}"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 23))
    s += SL(Z_DAL, goloe_derevo(240, 880, 420, t, 8, 6, inej_=True))
    s += SL(Z_DAL, grozd_ryabiny(300, 700, t, 1.2, 16))
    s += SL(Z_DAL, f'<circle cx="1600" cy="760" r="60" fill="{KAMEN}" {o(5)}/><path d="M1540,760 a60,40 0 0 1 120,0" fill="none" stroke="{KAMEN}" stroke-width="10"/>')
    s += SL(Z_SRED, sneg_lezhit(840))
    s += SL(Z_SRED, pleten(680, 760, 560, 160))
    kx = 960
    s += SL(Z_SRED, f'<rect x="{kx-50:.0f}" y="640" width="100" height="220" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{kx:.0f},640 L{kx-60:.0f},600 L{kx+60:.0f},600 Z" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, figura(kx - 220, 940, 420, t, "#2a2a30", "#5a5560", True, .0))
    ruk1, (r1x, r1y) = rukav(kx - 160, 720, 160, -10, t, "#2a2a30", "#5a5560", .0)
    s += SL(Z_SRED, ruk1)
    polo_x = kx - 160 + (260) * A.ease(A.seg(t, 0, 1.0))
    s += SL(Z_SRED, f'<path d="M{polo_x-50:.0f},740 q50,-20 100,0 l0,30 q-50,20 -100,0 Z" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, _chertenok(polo_x, 750, .7, t, .3))
    s += SL(Z_SRED, figura(kx + 220, 940, 420, t, "#3a3a2a", "#cfe4f5", True, .3, True))
    ruk2, (r2x, r2y) = rukav(kx + 160, 720, 160, -170, t, "#3a3a2a", "#cfe4f5", .3)
    s += SL(Z_SRED, ruk2)
    moneta = A.ease(A.seg(t, 1.6, .6))
    s += SL(Z_SRED, f'<circle cx="{r1x+10:.0f}" cy="{r1y-40*moneta:.0f}" r="14" fill="url(#med)" {o(2)}/>')
    beg = A.ease(A.seg(t, 1.0, 1.4))
    s += SL(Z_SRED, _chertenok(polo_x - beg * 200, 770 + beg * 40, .55, t, 0) if beg > .05 else "")
    s += SL(Z_DAL, siluet(1640, 940, 260, "#1a1c22", .8))
    s += SL(Z_SRED, svecha(968, 872, t, 1.92, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c10", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 14, 17, .4, .6))
    s += vinetka(.44)
    return s


def babushkina_shal(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 25)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, pech(1340, 320, 420, 540, t))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _kovrik_pol(460, 900, 700, 120, TKAN, KREM, 33))
    s += SL(Z_SRED, hodiki(1760, 320, t, 1.0))
    s += SL(Z_SRED, f'<rect x="300" y="880" width="420" height="34" rx="10" fill="url(#derev)" {o(5)}/>')
    kach = 4 * A.w(t, 1.2)
    s += SL(Z_SRED, f'<ellipse cx="{480+kach:.0f}" cy="860" rx="110" ry="34" fill="{KREM}" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{430+kach+i*36:.0f}" cy="850" r="16" fill="{(KRAS,ZOL)[i%2]}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M680,860 l-30,40 l20,-100" stroke="{ZHELEZ}" stroke-width="8" fill="none"/>')
    s += SL(Z_SRED, kot(760, 920, t, .9, "#3b3430", False))
    s += SL(Z_SRED, f'<rect x="860" y="860" width="60" height="40" rx="6" fill="{TKAN2}" {o(3)}/>')
    sway = 2 * A.w(t, .9)
    stoy = figura(900, 1020, 500, t, "#5a5560", KREM, True, .0, False, naklon=sway)
    s += SL(Z_SRED, stoy)
    ruk1, (r1x, r1y) = rukav(840, 880, 100, 60 - sway * 5, t, "#5a5560", KREM, .0, 4)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(960, 880, 100, 120 + sway * 5, t, "#5a5560", KREM, .3, 4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, figura(900, 1060, 220, t, "#efe3c8", SVET, False, .2))
    shawl = .4 + .1 * A.w(t, 1.4)
    s += SL(Z_SRED, f'<path d="M740,900 q160,{-120-shawl*40:.0f} 320,0" fill="none" stroke="#6f7f8c" stroke-width="60" opacity=".92"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{740+i*20}" y1="900" x2="{730+i*20}" y2="960" stroke="#6f7f8c" stroke-width="5"/>')
        s += SL(Z_SRED, f'<line x1="{1060-i*20}" y1="900" x2="{1070-i*20}" y2="960" stroke="#6f7f8c" stroke-width="5"/>')
    zav_y = 760 - 60 * ((t * .5) % 1.0)
    s += SL(Z_SRED, f'<path d="M900,780 q20,{-40+zav_y*.1:.0f} 0,{-80:.0f}" fill="none" stroke="#cfd6de" stroke-width="5" opacity="{1-((t*.5)%1.0):.2f}"/>')
    s += SL(Z_SRED, f'<circle cx="940" cy="700" r="10" fill="{KRAS}" opacity=".7"/><rect x="860" y="690" width="24" height="20" fill="{POBEL}" {o(2)}/>')
    s += SL(Z_SRED, svecha(173, 797, t, 0.37, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def tapochki_v_podarochnoy_korobke(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 27)
    s += SL(Z_DAL, _elka(1500, 960, 560, t, 9))
    s += SL(Z_SRED, polovicy(840))
    bx, by = 760, 660
    s += SL(Z_SRED, _korobka(bx, by, 420, 240, t, TKAN2, ZOL, True, .55, .1))
    s += SL(Z_SRED, f'<ellipse cx="{bx+120:.0f}" cy="{by+150:.0f}" rx="130" ry="16" fill="#fdf8ec" opacity=".8"/>')
    pomp = 8 * A.w(t, 1.6)
    for i, sgn in enumerate((-1, 1)):
        tx = bx + 150 + sgn * 70
        s += SL(Z_SRED, f'<path d="M{tx-50:.0f},{by+160:.0f} q0,-40 50,-40 q50,0 50,40 q-10,20 -50,20 q-40,0 -50,-20 Z" fill="#b8323a" {o(4)}/>')
        s += SL(Z_SRED, f'<circle cx="{tx:.0f}" cy="{by+108+pomp*.3*(1 if sgn>0 else -1):.0f}" r="16" fill="#efe3c8" {o(2)}/>')
    kor_t = A.ease(A.seg(t, .4, 1.4))
    s += SL(Z_SRED, f'<path d="M{bx+420:.0f},{by+200:.0f} q{-120*kor_t:.0f},{-20*kor_t:.0f} {-220*kor_t:.0f},{-10*kor_t:.0f}"'
                    f' fill="none" stroke="{MED}" stroke-width="10" opacity="{kor_t:.2f}"/>')
    s += SL(Z_SRED, f'<rect x="{bx+180:.0f}" y="{by+210:.0f}" width="380" height="40" rx="6" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{bx+180:.0f},{by+230:.0f} h-40" stroke="{POL2}" stroke-width="4" stroke-dasharray="4 6"/>')
    for i, sgn in enumerate((-1, 1, -1)):
        s += SL(Z_SRED, _svertok(bx - 160 + i * 60, by + 210 + sgn * 10, .9, t, (KRAS, TKAN2, ZEL2)[i], ZOL, i * .2))
    for i in range(3):
        s += SL(Z_LETIT, f'<line x1="{bx+500+i*10}" y1="{by-40-i*20}" x2="{bx+500+i*10+10*A.w(t,1.2,i*.3):.0f}" y2="{by+200}" stroke="#d8d0a8" stroke-width="2" opacity=".7"/>')
    s += SL(Z_SRED, f'<circle cx="{bx+440:.0f}" cy="{by+60:.0f}" r="26" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, kot(bx + 460, by + 230, t, .85, "#3b3430", False))
    shar_x = bx - 240 + 60 * ((t * 60) % 200) / 200
    s += SL(Z_SRED, f'<circle cx="{shar_x:.0f}" cy="{by+220:.0f}" r="22" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1339, 771, t, 0.51, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 45-51 ══════════════════════════════
def vnuk_prines_tapochki(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 29)
    s += SL(Z_DAL, _oboi_fon("#4a3a4a", "#3a2e3a"))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<circle cx="300" cy="500" r="80" fill="{STEKLO}" opacity=".55" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M500,500 v360" stroke="{ZHELEZ}" stroke-width="6"/><path d="M460,540 q40,-10 80,0" fill="none" stroke="{ZHELEZ}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="1500" y="720" width="160" height="140" rx="20" fill="{TKAN}" {o(4)}/>')
    s += SL(Z_SRED, kot(1400, 940, t, .9, "#3b3430", False))
    s += SL(Z_SRED, _kovrik_pol(760, 900, 500, 110, TKAN2, KREM, 37))
    pasyol = A.ease(A.seg(t, .2, 1.2))
    bx = 900 - pasyol * 120
    s += SL(Z_SRED, figura(700, 1020, 460, t, "#2a4a3a", "#cfd6de", False, .0, True, shapka=True))
    ruk1, (r1x, r1y) = rukav(760, 760, 140, -50, t, "#2a4a3a", "#cfd6de", .0, 4)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(700, 760, 140, -130, t, "#2a4a3a", "#cfd6de", .3, 4)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<rect x="{bx-80:.0f}" y="700" width="160" height="120" rx="10" fill="{TKAN2}" {o(4)}/>')
    s += SL(Z_SRED, figura(1100, 1020, 460, t, "#8c3a3a", KREM, True, .2))
    ruk2, (r2x, r2y) = rukav(1030, 760, 140, -140, t, "#8c3a3a", KREM, .2, 4)
    s += SL(Z_SRED, ruk2)
    ruk2b, (r2bx, r2by) = rukav(1100, 760, 140, -50, t, "#8c3a3a", KREM, .5, 4)
    s += SL(Z_SRED, ruk2b)
    s += SL(Z_SRED, figura(1420, 1080, 160, t, "#6b4428", KREM, False, .4))
    nadet = A.ease(A.seg(t, 1.6, 1.0))
    s += SL(Z_SRED, f'<g transform="rotate({-20*nadet:.1f} 1440 1060)">'
                    f'<path d="M1400,1060 q10,-20 60,-16 q20,2 20,16 q0,14 -40,16 q-40,2 -40,-16 Z" fill="#b8323a" {o(3)}/></g>')
    s += SL(Z_SRED, svecha(1392, 808, t, 0.88, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e14", .36))
    s += vinetka(.4)
    return s


def gostevye_tapochki_u_vhoda(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 31)
    s += SL(Z_DAL, _oboi_fon("#5a4a4a", "#4a3a3a"))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _veshalka_seni(1420, 260, 420, t, 7))
    s += SL(Z_SRED, _kovrik_pol(700, 920, 500, 120, TKAN, KREM, 41))
    shx, shy, shw = 420, 760, 560
    s += SL(Z_SRED, f'<rect x="{shx:.0f}" y="{shy:.0f}" width="{shw}" height="40" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<ellipse cx="{shx+70+i*160:.0f}" cy="{shy-16:.0f}" rx="60" ry="22" fill="#8c3a3a" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{shx+shw-80:.0f}" cy="{shy-18:.0f}" rx="86" ry="28" fill="{ZEL2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{shx+shw-150:.0f}" y="{shy-40:.0f}" width="140" height="18" fill="none" stroke="{K}" stroke-width="3" opacity=".5"/>')
    diskx, disky = 1180, 700
    s += SL(Z_SRED, f'<rect x="{diskx-60:.0f}" y="{disky:.0f}" width="120" height="90" rx="10" fill="{POBEL}" {o(4)}/>')
    blikf = .5 + .5 * abs(A.w(t, 1.4))
    s += SL(Z_SRED, f'<circle cx="{diskx:.0f}" cy="{disky-10:.0f}" r="44" fill="#2a2a30" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{diskx:.0f}" cy="{disky-10:.0f}" r="34" fill="#fff" opacity="{.3+.4*blikf:.2f}"/>')
    sn = A.ease(A.seg(t, .3, 1.5))
    stoy = figura(760, 1040, 480, t, "#3a3a4a", "#cfd6de", False, .0, False)
    s += SL(Z_SRED, stoy)
    ruk1, (r1x, r1y) = rukav(820, 820, 140, -30, t, "#3a3a4a", "#cfd6de", .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(700, 820, 140, -170, t, "#3a3a4a", "#cfd6de", .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<path d="M820,1060 l0,{-60*sn:.0f} l40,{20*sn:.0f} Z" fill="#2a2420" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="700" cy="{1100-10*sn:.0f}" rx="56" ry="24" fill="#8c3a3a" {o(3)}/>')
    s += SL(Z_SRED, svecha(438, 862, t, 0.22, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def tri_pustyh_podarka(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 33)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(220, 760, 1480, 34))
    gifts = (("koshelek", 420), ("sumka", 900), ("vaza", 1380))
    for i, (kind, gx) in enumerate(gifts):
        app = A.ease(A.seg(t, i * 1.4, .6))
        if kind == "koshelek":
            s += SL(Z_SRED, _koshelek(gx, 740, 1.6))
        elif kind == "sumka":
            s += SL(Z_SRED, f'<path d="M{gx-70:.0f},740 q-10,-90 70,-90 q80,0 70,90 Z" fill="#5a3a26" {o(5)}/>')
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="700" rx="40" ry="14" fill="#1a1410"/>')
        else:
            s += SL(Z_SRED, f'<path d="M{gx-60:.0f},740 L{gx-40:.0f},600 L{gx+40:.0f},600 L{gx+60:.0f},740 Z" fill="{STEKLO}" opacity=".5" {o(4)}/>')
            dr = (t * 30) % 40
            s += SL(Z_SRED, f'<path d="M{gx:.0f},{620+dr:.0f} q10,20 0,40" fill="none" stroke="#cfe8ee" stroke-width="3" opacity=".5"/>')
        if app > .05:
            s += SL(Z_SRED, _zapret(gx, 560, 80, t, i * .3) if app > .98 else
                    f'<g opacity="{app:.2f}">' + _zapret(gx, 560, 80, t, i * .3) + '</g>')
    for i in range(3):
        kach = 3 * A.w(t, 1.1, i * .3)
        s += SL(Z_SRED, svecha(200 + i * 1500 // 2, 700, t, i * .2, .9))
    s += SL(Z_SRED, f'<path d="M700,620 l-30,-80 l60,0 Z" fill="{ZEL}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1140" cy="650" r="34" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1600" y="680" width="80" height="60" rx="6" fill="{KREM}" {o(3)}/>')
    razv = A.ease(A.seg(t, 1.8, 1.0))
    s += SL(Z_SRED, f'<path d="M{420+80*razv:.0f},700 q20,10 30,30" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def koshelek_s_monetoy_na_donyshke(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 35)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(220, 760, 1480, 34))
    s += SL(Z_SRED, _koshelek(420, 740, 1.6, True, 0))
    s += SL(Z_SRED, f'<path d="M900,740 q-10,-90 70,-90 q80,0 70,90 Z" fill="#5a3a26" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1320,740 L1340,600 L1420,600 L1440,740 Z" fill="{STEKLO}" opacity=".5" {o(4)}/>')
    pad = A.ease(A.seg(t % 3.0, .3, .8))
    mx, my = 420 + 10, 650 - (1 - pad) * 160
    s += SL(Z_SRED, f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="18" fill="url(#zol)" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1380" cy="700" rx="40" ry="20" fill="{KRAS}" {o(3)}/>')
    for i in range(4):
        fall = A.ease(A.seg(t % 3.0, 1.3 + i * .3, .5))
        s += SL(Z_SRED, f'<circle cx="{1380-30+i*18:.0f}" cy="{700-(1-fall)*120:.0f}" r="9" fill="{(KRAS,ZOL)[i%2]}" opacity="{.3+.7*fall:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M1280,700 q-30,-50 0,-90" fill="none" stroke="{KREM}" stroke-width="20" opacity=".9"/>')
    gone = A.ease(A.seg(t % 3.0, 2.3, .6))
    if gone < .95:
        s += SL(Z_SRED, f'<g opacity="{1-gone:.2f}">' + _zapret(420, 560, 80, t, .0) + _zapret(900, 560, 80, t, .3) + '</g>')
    for i in range(3):
        s += SL(Z_SRED, svecha(1650, 700, t, i * .3, .9))
    s += SL(Z_SRED, f'<path d="M620,650 q10,-30 30,0" fill="none" stroke="{ZOL}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(650, 1060, 460, t, "#6b3a4a", KREM, True, .0))
    s += SL(Z_SRED, f'<circle cx="760" cy="1000" r="18" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def gostincy_iz_svoego_sada(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    sneg_vid = nebo("den", t, True, 39) + SL(Z_LETIT, sneg_letit(t, 12, 20, .5, .6))
    s += SL(Z_DAL, okno_izby(1420, 140, 400, 340, t, vid=sneg_vid, moroz=.15, svet=True))
    s += SL(Z_SRED, f'<ellipse cx="1760" cy="260" rx="46" ry="60" fill="{POBEL}" {o(4)}/>')
    s += SL(Z_DAL, doski(0, 40, W, 720, 70))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, stol(160, 700, 980, 34))
    s += SL(Z_SRED, krynka(360, 690, 1.3, "url(#med)"))
    s += SL(Z_SRED, f'<path d="M560,700 q-10,-40 30,-50 q40,-10 50,20 q-20,30 -50,30 q-20,0 -30,0 Z" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="696" rx="80" ry="24" fill="{KREM}" {o(3)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<ellipse cx="{710+i*20:.0f}" cy="690" rx="16" ry="8" fill="#d8b878" opacity=".85"/>')
    bx, by, bw_, bh_ = 960, 360, 840, 440
    s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw_}" height="{bh_}" rx="10" fill="url(#derev)" {o(7)}/>')
    pw, ph_ = 760, 300
    px, py = bx + 40, by + 90
    put = kontur_proema(px, py, pw, ph_, "pryam")
    stok_content = krynka(px + pw * .3, py + ph_ * .8, .6, "url(#med)") + _napolnenie(px, py + ph_ * .5, pw, ph_ * .5, t, 44, 4)
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>' + stok_content)
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M{bx+bw_:.0f},{by+10:.0f} q40,{bh_*.5:.0f} 0,{bh_-20:.0f}" fill="none" stroke="#2a1d14" stroke-width="6"/>')
    s += SL(Z_SRED, figura(600, 1020, 480, t, "#5a4a3a", KREM, False, .0))
    zav = A.ease(A.seg(t, .3, 1.2))
    ruk1, (r1x, r1y) = rukav(540, 720, 140, -90, t, "#5a4a3a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(620, 720, 150, -10 - zav * 20, t, "#5a4a3a", KREM, .3, 4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<path d="M{r2x:.0f},{r2y:.0f} q{30*zav:.0f},{-10*zav:.0f} {50*zav:.0f},{10*zav:.0f}" fill="none" stroke="{MED}" stroke-width="4"/>')
    s += SL(Z_SRED, _napolnenie(900, 560, 260, 160, t, 40, 5))
    s += SL(Z_SRED, svecha(231, 809, t, 0.41, .8))
    s += SL(Z_PERED, ramka_pp("levo", "#120e0e", .32))
    s += vinetka(.4)
    return s


def podokonnik_s_konfetami(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    city = _oboi_fon("#2a3550", "#1e2638")
    for i in range(10):
        wx, wy = 60 + i * 190 % 1800, 80 + (i * 97) % 380
        on = ((t * 1.2 + i) % 4) > .6
        city += f'<rect x="{wx}" y="{wy}" width="26" height="36" fill="{SVET if on else "#3a4258"}" opacity="{.9 if on else .4}"/>'
    s += SL(Z_DAL, okno_izby(1360, 140, 420, 360, t, vid=city, moroz=0, svet=False))
    s += SL(Z_DAL, _oboi_fon("#5a4a5a", "#4a3a4a"))
    s += SL(Z_SRED, polovicy(800))
    px, py, pw = 1340, 500, 460
    s += SL(Z_SRED, f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw}" height="200" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{px+70:.0f}" cy="{py+40:.0f}" rx="50" ry="60" fill="{ZEL2}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{px+180:.0f},{py+100:.0f} L{px+150:.0f},{py+20:.0f} L{px+210:.0f},{py+20:.0f} Z" fill="{ZEL2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{px+280:.0f}" y="{py+40:.0f}" width="60" height="80" rx="20" fill="url(#stekl)" opacity=".5" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<line x1="{px+300:.0f}" y1="{py+100-i*18:.0f}" x2="{px+320:.0f}" y2="{py+100-i*18:.0f}" stroke="{ZEL}" stroke-width="3"/>')
    bowl_x, bowl_y = 900, 760
    s += SL(Z_SRED, f'<ellipse cx="{bowl_x:.0f}" cy="{bowl_y:.0f}" rx="120" ry="34" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{bowl_x-120:.0f},{bowl_y:.0f} q0,70 120,70 q120,0 120,-70" fill="{KREM}" {o(4)}/>')
    nasyp = A.ease(A.seg(t, .3, 1.6))
    for i in range(int(10 * nasyp)):
        rnd = random.Random(i)
        s += SL(Z_SRED, f'<circle cx="{bowl_x-80+rnd.random()*160:.0f}" cy="{bowl_y-10-rnd.random()*40*nasyp:.0f}" r="14" fill="{(KRAS,ZOL,TKAN2)[i%3]}" {o(2)}/>')
    stoy = figura(900, 1060, 470, t, "#8c6a7a", KREM, False, .0)
    s += SL(Z_SRED, stoy)
    ruk1, (r1x, r1y) = rukav(840, 820, 140, -70, t, "#8c6a7a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(960, 820, 140, -150, t, "#8c6a7a", KREM, .3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, svecha(862, 798, t, 1.18, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e18", .36))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 52-59 ══════════════════════════════
def banka_s_konfetami_i_tarelka_s_yabl(t):
    s = f'<rect width="{W}" height="{H}" fill="{KAMEN2}"/>'
    s += SL(Z_DAL, kladka(0, 0, W, 900))
    s += SL(Z_SRED, polovicy(900, "url(#beton)"))
    dx = 960
    s += SL(Z_SRED, f'<rect x="{dx-220:.0f}" y="240" width="440" height="660" fill="#5a4a3a" {o(7)}/>')
    for yy in range(280, 860, 60):
        s += SL(Z_SRED, f'<line x1="{dx-220:.0f}" y1="{yy}" x2="{dx+220:.0f}" y2="{yy}" stroke="#3a2e22" stroke-width="3" opacity=".5"/>')
    s += SL(Z_SRED, f'<circle cx="{dx+140:.0f}" cy="560" r="16" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<circle cx="{dx-260:.0f}" cy="540" r="22" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{dx+260:.0f}" y="700" width="120" height="100" rx="10" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, _pochta_yashchiki(140, 400, 300, 240, 6))
    s += SL(Z_SRED, f'<path d="M700,860 l-40,-160 l80,0 Z" fill="#6b4428" {o(3)}/><ellipse cx="700" cy="860" rx="40" ry="10" fill="#9aa0a4" {o(2)}/>')
    s += SL(Z_SRED, _kovrik_pol(dx - 160, 850, 320, 60, TKAN, KREM, 45))
    perehod = A.ease(A.seg(t, .3, 1.6))
    tx = dx - 200 + perehod * 200
    s += SL(Z_SRED, figura(dx - 260, 1060, 460, t, "#5a5560", KREM, True, .0))
    ruk1, (r1x, r1y) = rukav(dx - 200, 800, 160, -50, t, "#5a5560", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk1b, (r1bx, r1by) = rukav(dx - 240, 800, 160, -130, t, "#5a5560", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, f'<ellipse cx="{tx:.0f}" cy="760" rx="100" ry="24" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{tx-40:.0f}" cy="750" r="26" fill="{KRAS}" {o(2)}/><circle cx="{tx+40:.0f}" cy="750" r="26" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M{tx:.0f},700 v-180 q0,-20 40,-20 q40,0 40,20 v180 Z" fill="{STEKLO}" opacity=".55" {o(4)}/>')
    for i in range(5):
        jig = 4 * A.w(t, 1.3, i * .2)
        s += SL(Z_SRED, f'<circle cx="{tx+20+jig:.0f}" cy="{660-i*22:.0f}" r="10" fill="{(KRAS,ZOL)[i%2]}"/>')
    s += SL(Z_SRED, figura(dx + 240, 1060, 460, t, "#3a5a4a", KREM, False, .4, True))
    ruk2, (r2x, r2y) = rukav(dx + 180, 800, 160, -130, t, "#3a5a4a", KREM, .4, 3)
    s += SL(Z_SRED, ruk2)
    ruk2b, (r2bx, r2by) = rukav(dx + 220, 800, 160, -50, t, "#3a5a4a", KREM, .7, 3)
    s += SL(Z_SRED, ruk2b)
    s += SL(Z_SRED, svecha(226, 834, t, 0.74, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0c", .42))
    s += vinetka(.42)
    return s


def moneta_iz_otcovskogo_yaschika(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 47)
    s += SL(Z_DAL, _oboi_fon("#3a3a4a", "#2e2e3e"))
    s += SL(Z_SRED, polovicy(820))
    dx, dy, dw = 640, 640, 760
    s += SL(Z_SRED, f'<rect x="{dx:.0f}" y="{dy:.0f}" width="{dw}" height="200" rx="8" fill="url(#derev)" {o(6)}/>')
    yasch = A.ease(A.seg(t, 0, .4))
    s += SL(Z_SRED, f'<g transform="translate(0,{-20*yasch:.0f})">'
                    f'<rect x="{dx+30:.0f}" y="{dy+60:.0f}" width="{dw-60}" height="100" rx="6" fill="#4a3a28" {o(5)}/>')
    s += f'<rect x="{dx+60:.0f}" y="{dy+80:.0f}" width="100" height="60" rx="8" fill="{KREM}" {o(3)}/>'
    for i in range(3):
        s += f'<circle cx="{dx+85+i*24:.0f}" cy="{dy+110:.0f}" r="10" fill="url(#zol)" {o(2)}/>'
    s += f'<rect x="{dx+200:.0f}" y="{dy+90:.0f}" width="70" height="30" rx="4" fill="{ZHELEZ}" {o(2)}/>'
    for i in range(3):
        s += f'<circle cx="{dx+220+i*20:.0f}" cy="{dy+105:.0f}" r="6" fill="{ZOL}" {o(1)}/>'
    s += f'<rect x="{dx+310:.0f}" y="{dy+95:.0f}" width="26" height="40" rx="6" fill="{ZHELEZ}" {o(2)}/><rect x="{dx+344:.0f}" y="{dy+95:.0f}" width="26" height="40" rx="6" fill="{ZHELEZ}" {o(2)}/>'
    s += f'<path d="M{dx+410:.0f},{dy+130:.0f} L{dx+470:.0f},{dy+90:.0f} L{dx+478:.0f},{dy+100:.0f} L{dx+420:.0f},{dy+136:.0f} Z" fill="{ZHELEZ}" {o(2)}/>'
    for i in range(4):
        s += f'<line x1="{dx+500+i*10:.0f}" y1="{dy+90:.0f}" x2="{dx+500+i*10:.0f}" y2="{dy+140:.0f}" stroke="#2a1f14" stroke-width="3"/>'
    lupa_blik = .5 + .5 * abs(A.w(t, 1.6))
    s += f'<circle cx="{dx+600:.0f}" cy="{dy+100:.0f}" r="36" fill="none" stroke="{ZHELEZ}" stroke-width="6"/>'
    s += f'<circle cx="{dx+600:.0f}" cy="{dy+100:.0f}" r="30" fill="#cfe8ee" opacity="{.3+.5*lupa_blik:.2f}"/>'
    s += f'<rect x="{dx+36:.0f}" y="{dy+160:.0f}" width="90" height="26" fill="#efe3c8" opacity=".6" {o(2)}/>'
    s += '</g>'
    s += SL(Z_SRED, figura(dx + 60, 1060, 480, t, "#4a3a2c", KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(dx + 140, 820, 150, -40, t, "#4a3a2c", KREM, .0)
    s += SL(Z_SRED, ruk1)
    beret = A.ease(A.seg(t, .8, .8))
    s += SL(Z_SRED, f'<circle cx="{dx+120+beret*20:.0f}" cy="{820-beret*60:.0f}" r="20" fill="url(#zol)" {o(2)}/>')
    s += SL(Z_SRED, figura(dx + 460, 1040, 480, t, "#6b2a44", KREM, False, .3, True))
    ruk2a, (r2ax, r2ay) = rukav(dx + 380, 780, 150, 160, t, "#6b2a44", KREM, .3)
    s += SL(Z_SRED, ruk2a)
    ruk2b, (r2bx, r2by) = rukav(dx + 420, 780, 150, -140, t, "#6b2a44", KREM, .6)
    s += SL(Z_SRED, ruk2b)
    kopeek = A.ease(A.seg(t, 1.8, .5))
    s += SL(Z_SRED, f'<rect x="{(r2ax+r2bx)/2-50:.0f}" y="{(r2ay+r2by)/2-20:.0f}" width="100" height="40" rx="6" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    if kopeek > .05:
        s += SL(Z_SRED, f'<circle cx="{(r2ax+r2bx)/2+beret*20*0:.0f}" cy="{(r2ay+r2by)/2+kopeek*10:.0f}" r="18" fill="url(#zol)" opacity="{min(1,kopeek*2):.2f}"/>')
    s += SL(Z_SRED, svecha(756, 844, t, 0.44, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def zerkalo_dver(t):
    s = f'<rect width="{W}" height="{H}" fill="{NOCH}"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="{K}" opacity=".3"/>')
    mx, my, mw, mh = 960, 480, 480, 600
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{mw*.52:.0f}" ry="{mh*.52:.0f}" fill="url(#zol)" {o(8)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{mw*.44:.0f}" ry="{mh*.44:.0f}" fill="#0a1420" {o(3)}/>')
    otkr = A.ease(A.seg(t, .4, 1.6))
    s += SL(Z_SRED, f'<path d="M{mx-20:.0f},{my-mh*.42:.0f} l{-40-80*otkr:.0f},10 l0,{mh*.8:.0f} l{40+80*otkr:.0f},10 Z" fill="#0a1420" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{mx-60-80*otkr:.0f},{my-mh*.3:.0f} v{mh*.6:.0f}" stroke="#3a7fb0" stroke-width="{10+30*otkr:.0f}" opacity="{.3+.5*otkr:.2f}"/>')
    s += SL(Z_SRED, f'<rect x="{mx-160:.0f}" y="{my+mh*.48:.0f}" width="320" height="60" rx="10" fill="url(#derev)" {o(5)}/>')
    for i, sgn in enumerate((-1, 1)):
        tyan = 10 * A.ease(A.seg(t, otkr + .1, .6))
        s += SL(Z_SRED, svecha(mx + sgn * 120, my + mh * .48, t, i * .3, 1.0 + .2 * otkr))
    s += SL(Z_SRED, f'<circle cx="{mx-40:.0f}" cy="{my+mh*.48:.0f}" r="20" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{mx+60:.0f}" cy="{my+mh*.5:.0f}" rx="30" ry="10" fill="{KREM}" {o(2)}/><circle cx="{mx+60:.0f}" cy="{my+mh*.5:.0f}" r="8" fill="{ZOL}" {o(1)}/>')
    s += SL(Z_SRED, f'<path d="M{mx+100:.0f},{my+mh*.48:.0f} q30,10 20,40" fill="none" stroke="{SVET}" stroke-width="4"/>')
    naklon = 3 * A.ease(A.seg(t, 1.2, 1.0))
    stoy = figura(mx, my + mh * .9, 420, t, "#8c6a9a", KREM, False, .0, naklon=naklon)
    s += SL(Z_SRED, stoy)
    s += SL(Z_SRED, f'<path d="M{mx-20:.0f},{my+mh*.6:.0f} q30,20 0,80" fill="none" stroke="{K}" stroke-width="8"/>')
    s += SL(Z_SRED, _napolnenie(1400, 700, 440, 180, t, 207, 8))
    s += SL(Z_PERED, ramka_pp("oba", "#060608", .48))
    s += vinetka(.5)
    return s


def devushka_u_tryumo(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 51)
    s += SL(Z_DAL, _oboi_fon())
    s += SL(Z_SRED, polovicy(840))
    tx, ty, tw = 960, 320, 760
    for i, sgn in enumerate((-1, 0, 1)):
        px = tx + sgn * tw * .34
        s += SL(Z_SRED, f'<rect x="{px-tw*.16:.0f}" y="{ty:.0f}" width="{tw*.32:.0f}" height="500" rx="8" fill="url(#zol)" {o(6)}/>')
        s += SL(Z_SRED, f'<rect x="{px-tw*.13:.0f}" y="{ty+16:.0f}" width="{tw*.26:.0f}" height="468" fill="#0a1420" {o(3)}/>')
        vid = ("young", "mid", "babka")[i]
        s += SL(Z_SRED, _tryumo_otrazhenie(px, ty + 430, .72, t, vid))
    s += SL(Z_SRED, f'<rect x="{tx-200:.0f}" y="{ty+500:.0f}" width="400" height="60" rx="10" fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{tx-120+i*110:.0f},{ty+480:.0f} q0,-40 16,-40 q16,0 16,40 Z" fill="{STEKLO}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{tx+180:.0f}" cy="{ty+470:.0f}" rx="40" ry="20" fill="#efe3c8" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M{tx-150:.0f},{ty+460:.0f} q20,-16 40,0" fill="none" stroke="{ZOL}" stroke-width="3"/>')
    for i in range(5):
        kach = 3 * A.w(t, 1.2, i * .2)
        s += SL(Z_SRED, f'<circle cx="{tx-180+i*20+kach:.0f}" cy="{ty+440:.0f}" r="10" fill="#fdf8ec" {o(2)}/>')
    s += SL(Z_SRED, figura(tx, ty + 1000, 420, t, "#efe3c8", KRAS, False, .0))
    lokon = A.ease(A.seg(t % 3.0, 0, .5))
    ruk1, (r1x, r1y) = rukav(tx - 60, ty + 820, 140, -90 + lokon * 10, t, "#efe3c8", KRAS, .0, 3)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(tx + 60, ty + 820, 140, -170, t, "#efe3c8", KRAS, .3, 2)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<circle cx="{r2x:.0f}" cy="{r2y:.0f}" r="18" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, svecha(332, 788, t, 1.48, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


def pudrenica_s_zerkalcem(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 53)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(360, 700, 1100, 34))
    kx, ky = 1000, 760
    s += SL(Z_SRED, f'<rect x="{kx-260:.0f}" y="{ky:.0f}" width="520" height="130" rx="18" fill="{TKAN}" {o(5)}/>')
    px, py, pw, ph_ = kx - 190, ky - 420, 380, 380
    put = kontur_proema(px, py, pw, ph_, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(6)}/>')
    s += SL(Z_SRED, f'<circle cx="{kx:.0f}" cy="{ky+30:.0f}" r="110" fill="#8c3a3a" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+200:.0f}" y="{ky-10:.0f}" width="30" height="100" rx="10" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+260:.0f}" y="{ky+20:.0f}" width="80" height="26" rx="8" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M{kx-280:.0f},{ky+10:.0f} q40,-10 80,0 l0,30 q-40,10 -80,0 Z" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{kx+320:.0f}" y="{ky-40:.0f}" width="120" height="80" rx="6" fill="{KREM}" {o(3)}/>')
    bant_sh = 6 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<path d="M{kx+380+bant_sh:.0f},{ky-50:.0f} q-30,10 -10,30 q20,-6 10,-30 Z" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx+540:.0f}" cy="{ky+40:.0f}" rx="60" ry="22" fill="{POL}" {o(3)}/>')
    s += SL(Z_SRED, par(kx + 540, ky + 20, t, 3, .4, 70))
    s += SL(Z_SRED, figura(kx - 60, 1060, 480, t, "#5a6a4a", KREM, False, .0))
    ruk1, (r1x, r1y) = rukav(kx + 20, 780, 130, -80, t, "#5a6a4a", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    puh = 10 * A.w(t, 2.0)
    ruk2, (r2x, r2y) = rukav(kx - 130, 780, 140, -30 + puh * .2, t, "#5a6a4a", KREM, .4, 3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<circle cx="{r2x:.0f}" cy="{r2y:.0f}" r="22" fill="#fdf8ec" opacity=".85"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.4)
    return s


def slezy_rusalki(t):
    s = f'<rect width="{W}" height="{H}" fill="{NOCH}"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 55))
    s += SL(Z_DAL, f'<circle cx="1620" cy="220" r="90" fill="{KREM}" opacity=".9" {o(2)}/><circle cx="1620" cy="220" r="130" fill="{KREM}" opacity=".18"/>')
    s += SL(Z_SRED, f'<path d="M0,760 q960,-40 1920,0 l0,80 q-960,40 -1920,0 Z" fill="url(#voda)" {o(4)}/>')
    kach = 2 * A.w(t, 2.4)
    for i in range(6):
        s += SL(Z_SRED, f'<line x1="{200+i*60+kach}" y1="900" x2="{196+i*60}" y2="700" stroke="{ZEL}" stroke-width="7"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<ellipse cx="{1400+i*90}" cy="{800+10*math.sin(t+i)}" rx="36" ry="12" fill="{ZEL2}" {o(2)}/>')
    s += SL(Z_DAL, f'<path d="M1600,900 q0,-200 -60,-260" stroke="#2a2a2a" stroke-width="16" fill="none"/>')
    s += SL(Z_DAL, goloe_derevo(1700, 900, 380, t, 5, 6, inej_=True))
    s += SL(Z_SRED, f'<path d="M1500,820 q60,-30 140,-10 l0,30 q-70,20 -140,0 Z" fill="#6b4428" {o(4)}/>')
    kx, ky = 760, 820
    rkx, rky = 880, 600
    s += SL(Z_SRED, f'<ellipse cx="{rkx:.0f}" cy="{rky:.0f}" rx="230" ry="50" fill="{KAMEN}" opacity=".9" {o(4)}/>')
    s += SL(Z_SRED, _rusalka(rkx, rky - 6, 300, t))
    s += SL(Z_SRED, f'<rect x="{kx-100:.0f}" y="{ky:.0f}" width="200" height="110" rx="16" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kx-70:.0f}" y="{ky-10:.0f}" width="140" height="18" fill="#0a1420" {o(2)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{kx-50+i*24:.0f}" cy="{ky+40:.0f}" r="10" fill="#f4f0e2" {o(2)}/>')
    s += SL(Z_SRED, svecha(1180, 780, t, 1.4, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#040608", .5))
    s += vinetka(.52)
    return s


def mamina_shkatulka_s_zhemchugom(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 59)
    s += SL(Z_DAL, _oboi_fon("#4a3a3a", "#3a2e2e"))
    s += SL(Z_SRED, polovicy(820))
    dx, dy, dw = 740, 700, 700
    s += SL(Z_SRED, f'<rect x="{dx:.0f}" y="{dy:.0f}" width="{dw}" height="160" rx="10" fill="url(#derev)" {o(6)}/>')
    skx, sky = dx + 350, dy - 220
    s += SL(Z_SRED, f'<rect x="{skx-230:.0f}" y="{sky-10:.0f}" width="460" height="400" rx="16" fill="#6b3a4a" {o(6)}/>')
    px, py, pw, ph_ = skx - 200, sky + 10, 400, 360
    put = kontur_proema(px, py, pw, ph_, "ellips")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a140e"/>')
    s += SL(Z_SRED, mesto_stoka(px, py, pw, ph_, "ellips"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" {o(6)}/>')
    sping = (t * 180) % 360
    s += SL(Z_SRED, f'<g transform="translate({dx+100:.0f},{dy-40:.0f}) rotate({sping:.1f})">'
                    f'<ellipse cx="0" cy="0" rx="10" ry="30" fill="#efe3c8" {o(2)}/></g>')
    s += SL(Z_SRED, f'<path d="M{dx+200:.0f},{dy-60:.0f} q40,-10 40,-60" fill="none" stroke="{ZOL}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<circle cx="{dx-180:.0f}" cy="{dy+20:.0f}" r="26" fill="url(#stekl)" opacity=".7" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{dx-80:.0f},{dy+10:.0f} l40,-20 l-6,30 Z" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{dx+dw+30:.0f}" y="{dy+30:.0f}" width="90" height="70" rx="4" fill="{KREM}" opacity=".9" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{dx+dw+140:.0f}" y="{dy+10:.0f}" width="70" height="90" rx="4" fill="url(#derev)" {o(3)}/>')
    s += SL(Z_SRED, _elka(dx + dw + 250, dy + 200, 220, t, 11))
    s += SL(Z_SRED, figura(dx - 60, 1040, 480, t, "#6b2a38", KREM, False, .0))
    zastyog = A.ease(A.seg(t, .5, 1.2))
    ruk1, (r1x, r1y) = rukav(dx + 10, 820, 140, -140 + zastyog * 10, t, "#6b2a38", KREM, .0)
    s += SL(Z_SRED, ruk1)
    ruk2, (r2x, r2y) = rukav(dx - 130, 820, 140, -40 - zastyog * 10, t, "#6b2a38", KREM, .3)
    s += SL(Z_SRED, ruk2)
    cypo = 8 * A.ease(A.seg(t, 1.0, 1.0)) % 8
    s += SL(Z_SRED, figura(dx - 380, 1080 - cypo, 260, t, "#cfe4f5", SVET, False, .4))
    s += SL(Z_SRED, f'<path d="M{dx-320:.0f},1040 h40" stroke="{K}" stroke-width="4" opacity=".4"/>')
    s += SL(Z_SRED, svecha(373, 867, t, 1.23, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .36))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 60-68 ══════════════════════════════
def spornye_podarki_na_vesah(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 61)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(560, 760, 800, 34))
    nak = 30 * math.sin(t * .7)
    s += SL(Z_SRED, _vesy(960, 760, 1.5, t, nak, 5))
    cycle = (t * .4) % 3.0
    stage = int(cycle)
    item_svg = (
        f'<rect x="-40" y="-14" width="80" height="28" rx="10" fill="{KRAS}" {o(3)}/><rect x="-40" y="4" width="80" height="4" fill="{KREM}"/>',
        f'<path d="M-50,10 q0,-40 50,-40 q50,0 50,40 l0,10 l-100,0 Z" fill="#6b4428" {o(3)}/>',
        f'<rect x="-10" y="-50" width="20" height="60" rx="6" fill="{KREM}" {o(2)}/><circle cx="0" cy="-54" r="8" fill="{SVET}"/>')[stage]
    nak_r = math.radians(nak)
    for sgn in (-1, 1):
        ipx = 960 + sgn * 150 * math.cos(nak_r) * 1.5 - nak * 0
        ipy = 760 - 220 * 1.5 + sgn * 150 * math.sin(nak_r) * 1.5 - 120 * 1.5
    s += SL(Z_SRED, f'<g transform="translate({960-150*1.5*math.cos(nak_r):.0f},{760-220*1.5+150*1.5*math.sin(nak_r)-100*1.5:.0f})">{item_svg}</g>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="700" rx="40" ry="16" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1160" cy="700" r="30" fill="{KRAS}" {o(2)}/>')
    stoy1 = figura(600, 1020, 460, t, "#6b4a3a", KREM, True, .0)
    s += SL(Z_SRED, stoy1)
    da = 10 * A.w(t, 1.1)
    ruk1, _ = rukav(680, 780, 130, -60 + da, t, "#6b4a3a", KREM, .0, 5)
    s += SL(Z_SRED, ruk1)
    stoy2 = figura(1320, 1020, 460, t, "#4a5a6b", KREM, False, .3, True)
    s += SL(Z_SRED, stoy2)
    net = 10 * A.w(t, 1.3, .4)
    ruk2, _ = rukav(1240, 780, 130, -120 - net, t, "#4a5a6b", KREM, .3, 5)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, par(760, 680, t, 3, .4, 70))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += vinetka(.42)
    return s


def monetka_na_krasnoy_varezhke(t):
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    s += SL(Z_NEBO, teplo(960, 300, 900, 500, .5))
    s += SL(Z_DAL, _elka(260, 940, 460, t, 13))
    s += SL(Z_DAL, _elka(1700, 920, 440, t, 14))
    s += SL(Z_DAL, okno_izby(1560, 140, 220, 220, t, svet=True, moroz=.2))
    for i in range(3):
        s += SL(Z_SRED, svecha(1200 + i * 60, 820, t, i * .3, .9))
    gifts = (("chasy", 320), ("nozhnicy", 500), ("platok", 660), ("tapochki", 820),
             ("koshelek", 980), ("zerkalo", 1120), ("zhemchug", 1260))
    for i, (kind, gx) in enumerate(gifts):
        jit = 2 * A.w(t, .35, i * .1)
        if kind == "chasy":
            s += SL(Z_SRED, _chasy_sten(gx, 700, .55, t))
        elif kind == "nozhnicy":
            s += SL(Z_SRED, _nozhnicy_bolshie(gx, 760, 90, t))
        elif kind == "platok":
            s += SL(Z_SRED, f'<rect x="{gx-30:.0f}" y="720" width="60" height="60" fill="{TKAN}" {o(2)}/>')
        elif kind == "tapochki":
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="750" rx="40" ry="18" fill="#8c3a3a" {o(2)}/>')
        elif kind == "koshelek":
            s += SL(Z_SRED, _koshelek(gx, 760, .8))
        elif kind == "zerkalo":
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="740" rx="36" ry="48" fill="url(#zol)" {o(3)}/><ellipse cx="{gx:.0f}" cy="740" rx="26" ry="38" fill="#0a1420"/>')
        else:
            s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="750" rx="40" ry="14" fill="#f4f0e2" {o(2)}/>')
        s += SL(Z_SRED, f'<g transform="translate({jit:.0f},0)">' + _zapret(gx, 700, 50, t, i * .2) + '</g>')
    vx, vy = 640, 960
    s += SL(Z_SRED, _varezhka(vx, vy, 3.0, 6 * A.w(t, 1.4)))
    s += SL(Z_SRED, f'<circle cx="{vx-30:.0f}" cy="{vy-70:.0f}" r="26" fill="url(#med)" {o(3)}/>')
    luch_x = vx + 20 + ((t * 200) % 900)
    s += SL(Z_SRED, f'<line x1="{vx:.0f}" y1="{vy-80:.0f}" x2="{luch_x:.0f}" y2="700" stroke="{SVET}" stroke-width="5" opacity=".7"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#1a0e08", .3))
    s += SL(Z_LETIT, sneg_letit(t, 16, 63, .4, .6))
    s += vinetka(.36)
    return s


def podarok_s_yarlykom(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 65)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, stol(260, 740, 1400, 40))
    s += SL(Z_SRED, _schyoty(680, 680, .9, t))
    s += SL(Z_SRED, f'<rect x="860" y="680" width="200" height="30" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1120" y="640" width="160" height="110" rx="8" fill="{TKAN}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1140" y="660" width="120" height="70" fill="#2a1f14" {o(2)}/>')
    bx = 1500
    s += SL(Z_SRED, _korobka(bx, 620, 220, 150, t, TKAN2, ZOL, True, .0, .1))
    ярlyk_y = 600 + 20 * A.ease(A.seg(t, .4, .8)) % 20
    s += SL(Z_SRED, f'<line x1="{bx+40:.0f}" y1="{560:.0f}" x2="{bx+40:.0f}" y2="{ярlyk_y:.0f}" stroke="{K}" stroke-width="2"/>')
    s += SL(Z_SRED, f'<rect x="{bx+10:.0f}" y="{ярlyk_y:.0f}" width="60" height="36" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1000" cy="700" rx="70" ry="24" fill="#6b4428" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M940,690 h120" stroke="{KREM}" stroke-width="4" opacity=".6"/>')
    s += SL(Z_SRED, f'<circle cx="400" cy="700" r="28" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1760, 720, t, .4, .9))
    stoy = figura(500, 1040, 480, t, "#4a3a2c", KREM, True, .0)
    s += SL(Z_SRED, stoy)
    ruk1, (r1x, r1y) = rukav(560, 800, 140, -40, t, "#4a3a2c", KREM, .0, 3)
    s += SL(Z_SRED, ruk1)
    mig = A.ease(A.seg(t % 4.0, 2.0, .3)) * (1 - A.ease(A.seg(t % 4.0, 2.3, .3)))
    ruk2, (r2x, r2y) = rukav(bx - 60, 800, 150, -140, t, "#4a3a2c", KREM, .3, 3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{500-40:.0f}" cy="{960-60*mig:.0f}" rx="14" ry="{10*(1-mig*.6):.0f}" fill="{K}"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def primeta_uhodit(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 67)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="200" y="700" width="1520" height="60" rx="10" fill="{KREM}" {o(5)}/>')
    bx = 900
    s += SL(Z_SRED, _korobka(bx, 580, 220, 150, t, TKAN2, SVET, True, .3, .1))
    uhodit = A.ease(A.seg(t, .4, 1.6))
    s += SL(Z_SRED, _primeta_vorona(bx + 20, 560, .9, t, uhodit))
    zvon = 1 - A.ease(A.seg(t, 0, .3))
    s += SL(Z_SRED, f'<circle cx="{bx+40:.0f}" cy="640" r="16" fill="url(#zol)" opacity="{max(0,zvon):.2f}" {o(2)}/>')
    cross = A.ease(A.seg(t, .2, .5))
    if cross < .95:
        s += SL(Z_SRED, f'<g opacity="{1-cross:.2f}">' + _zapret(bx, 700, 50, t, 0) + '</g>')
    if cross > .1:
        s += SL(Z_SRED, f'<g opacity="{cross:.2f}">' + _galochka(bx, 700, 1.0, t, 0) + '</g>')
    s += SL(Z_SRED, svecha(400, 700, t, .2, .9))
    s += SL(Z_SRED, svecha(1500, 700, t, .5, .9))
    s += SL(Z_SRED, f'<circle cx="640" cy="700" r="26" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="1200" y="690" width="90" height="60" rx="6" fill="{KREM}" {o(3)}/>')
    lenta = 5 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<path d="M1350,700 q{20+lenta:.0f},10 10,30" fill="none" stroke="{KRAS}" stroke-width="6"/>')
    s += SL(Z_SRED, f'<ellipse cx="1660" cy="700" rx="60" ry="22" fill="{KREM}" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def tri_vykuplennyh_podarka(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 69)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="260" y="700" width="1400" height="70" rx="12" fill="{KREM}" {o(5)}/>')
    items = (("nozh", 500), ("chasy", 960), ("platok", 1420))
    for i, (kind, gx) in enumerate(items):
        if kind == "nozh":
            s += SL(Z_SRED, f'<path d="M{gx-80:.0f},700 h160 l-20,-24 h-120 Z" fill="{ZHELEZ}" {o(3)}/><rect x="{gx-30:.0f}" y="674" width="60" height="18" rx="4" fill="#5a3a26" {o(2)}/>')
        elif kind == "chasy":
            s += SL(Z_SRED, _chasy_karman(gx, 660, 1.0, t))
        else:
            s += SL(Z_SRED, f'<path d="M{gx-60:.0f},700 l120,0 l-20,-40 l-80,0 Z" fill="{TKAN}" {o(3)}/>')
        app = A.ease(A.seg(t, i * 1.0, .5))
        moneta_y = 650 - (1 - app) * 150
        s += SL(Z_SRED, f'<circle cx="{gx:.0f}" cy="{moneta_y:.0f}" r="16" fill="url(#zol)" {o(2)}/>')
        if app > .98:
            s += SL(Z_SRED, _galochka(gx, 600, .9, t, i * .2))
    s += SL(Z_SRED, f'<path d="M700,690 h40" stroke="{KREM}" stroke-width="4" opacity=".5"/>')
    s += SL(Z_SRED, svecha(300, 700, t, .3, .9))
    s += SL(Z_SRED, f'<path d="M1180,620 l-30,-70 l60,0 Z" fill="{ZEL}" {o(3)}/>')
    mand_x = 1650 + 20 * math.sin(t * 1.2)
    s += SL(Z_SRED, f'<circle cx="{mand_x:.0f}" cy="700" r="24" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1750" cy="690" rx="70" ry="24" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="150" cy="660" r="20" fill="none" stroke="{ZHELEZ}" stroke-width="4"/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .38))
    s += vinetka(.4)
    return s


def s_tebya_kopeyka(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 71)
    s += SL(Z_DAL, _oboi_fon("#5a3a4a", "#4a2e3a"))
    s += SL(Z_DAL, _elka(1600, 960, 520, t, 17))
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, f'<rect x="120" y="760" width="320" height="140" rx="20" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="80" y="620" width="40" height="280" fill="{ZHELEZ}" {o(4)}/><ellipse cx="100" cy="610" rx="60" ry="20" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="500" cy="840" rx="70" ry="24" fill="{KREM}" {o(3)}/><path d="M460,830 l-40,-80 l40,20 l30,60 Z" fill="#6b4428" {o(3)}/>')
    s += SL(Z_SRED, kot(600, 900, t, .85, "#3b3430", False))
    for i in range(3):
        s += SL(Z_SRED, _svertok(1500 + i * 60, 900, .9, t, (KRAS, TKAN2, ZEL2)[i], ZOL, i * .2))
    s += SL(Z_SRED, hodiki(1760, 420, t, .9))
    topnуt = 10 * abs(math.sin(t * 3))
    stoy1 = figura(820, 1040 - topnуt * .3, 460, t, "#8c3a6a", KREM, False, .0)
    s += SL(Z_SRED, stoy1)
    ruk1, (r1x, r1y) = rukav(900, 800, 150, -40, t, "#8c3a6a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, _korobka(r1x + 40, r1y - 30, 140, 100, t, TKAN2, ZOL, True, .0, .2))
    ruk1b, (r1bx, r1by) = rukav(780, 820, 140, -160, t, "#8c3a6a", KREM, .3, 3)
    s += SL(Z_SRED, ruk1b)
    s += SL(Z_SRED, _oblachko(820, 680, .7, t, .2, "moneta"))
    stoy2 = figura(1200, 1040, 470, t, "#3a5a6b", KREM, False, .3, True)
    s += SL(Z_SRED, stoy2)
    hlopok = abs(A.w(t, .6)) > .8
    ruk2, (r2x, r2y) = rukav(1140, 800, 140, -110 + (10 if hlopok else 0), t, "#3a5a6b", KREM, .3)
    s += SL(Z_SRED, ruk2)
    ruk2b, (r2bx, r2by) = rukav(1260, 800, 150, -70, t, "#3a5a6b", KREM, .6)
    s += SL(Z_SRED, ruk2b)
    s += SL(Z_SRED, svecha(1021, 789, t, 0.29, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#120e18", .36))
    s += vinetka(.4)
    return s


def pokupayu(t):
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("noch", t, True, 73)
    s += SL(Z_DAL, _oboi_fon("#3a3a4a", "#2e2e3e"))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _veshalka_seni(1380, 260, 420, t, 9))
    s += SL(Z_SRED, f'<rect x="420" y="640" width="200" height="220" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="520" cy="720" rx="80" ry="40" fill="url(#zol)" {o(3)}/>')
    kach = 4 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 900 600)"><circle cx="900" cy="600" r="80" fill="{ZEL}" {o(4)}/>'
                    f'<circle cx="870" cy="590" r="10" fill="{KRAS}"/><circle cx="930" cy="610" r="10" fill="{KRAS}"/>'
                    f'<path d="M900,520 q30,30 0,80" fill="none" stroke="{KRAS}" stroke-width="6"/></g>')
    s += SL(Z_SRED, _kovrik_pol(760, 900, 500, 110, TKAN, KREM, 77))
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{500+i*20:.0f}" cy="728" r="8" fill="{ZOL}" opacity="{.6+.4*abs(A.w(t,1.2,i*.2)):.2f}"/>')
    s += SL(Z_SRED, figura(900, 1060, 480, t, "#5a6a4a", KREM, False, .0, False, shapka=False))
    ruk1, (r1x, r1y) = rukav(840, 800, 150, -70, t, "#5a6a4a", KREM, .0)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, _korobka(r1x + 30, r1y - 20, 160, 130, t, TKAN2, SVET, True, .0, .2))
    s += SL(Z_SRED, f'<rect x="{r1x+60:.0f}" y="{r1y-10:.0f}" width="100" height="90" rx="6" fill="url(#zol)" {o(3)}/>')
    s += SL(Z_SRED, figura(1220, 1060, 470, t, "#8c3a6a", SVET, False, .3, True))
    moneta = A.ease(A.seg(t, .5, 1.0))
    ruk2, (r2x, r2y) = rukav(1150, 800, 140, -150 + moneta * 20, t, "#8c3a6a", SVET, .3)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<circle cx="{r2x+20*moneta:.0f}" cy="{r2y-10*moneta:.0f}" r="14" fill="url(#zol)" {o(2)}/>')
    ruk3, (r3x, r3y) = rukav(1290, 800, 140, -30 - moneta * 10, t, "#8c3a6a", SVET, .6)
    s += SL(Z_SRED, ruk3)
    s += SL(Z_SRED, svecha(915, 835, t, 1.55, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c10", .4))
    s += vinetka(.42)
    return s
