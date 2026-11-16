# -*- coding: utf-8 -*-
"""ПОРЦИЯ 1: декорации ролика «19 ноября — Павел Ледостав».

Каждая функция — f(t) -> SVG (без внешнего <svg> и без <defs>). Все сцены
нарисованы ЗАНОВО под текст ЭТОГО дня (R-0019): ни одна не взята у «13»-«18
ноября». Люди — только figura() из lok_obshchee, руки — через _ruka() от
плеча, кистей и пальцев не рисуем (R-0051). Источник — его таблица
«2027 — РАСКАДРОВКА 19 ноября Павел Ледостав», задание — zadaniya/porciya1.md.
"""
import math, random
from baza import *
import anim as A
from lok_obshchee import *
from lok_obshchee import (
    _plecho, _predmet_naruzhu, _ruka, _ruka_ekr, _ruka_so_sgibom)


# ── помощники этой порции ──────────────────────────────────────────────────

def _merzlaya_zemlya(y0, seed=3, luzhi=True):
    """Мёрзлая земля ноября: бурая, с комьями, схваченной колеёй и инеем."""
    rnd = random.Random(seed * 17 + 1)
    s = (f'<rect x="0" y="{y0:.0f}" width="{W}" height="{H-y0:.0f}" fill="#4a3a2a"/>')
    s += (f'<path d="M-40,{H} Q420,{y0+180:.0f} 760,{y0+40:.0f} L1240,{y0+40:.0f}'
          f' Q1520,{y0+180:.0f} 1960,{H} Z" fill="#5f4a32" opacity=".95"/>')
    for i in range(26):
        kx, ky = rnd.uniform(-40, 1960), rnd.uniform(y0 + 20, H - 10)
        s += (f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="{rnd.uniform(14,46):.0f}"'
              f' ry="{rnd.uniform(5,15):.0f}" fill="#3f3122"'
              f' opacity="{rnd.uniform(.35,.75):.2f}"/>')
    for i in range(9):
        gy = rnd.uniform(y0 + 40, H - 20)
        s += (f'<path d="M{rnd.uniform(-60,400):.0f},{gy:.0f}'
              f' Q{rnd.uniform(700,1200):.0f},{gy+rnd.uniform(-22,22):.0f}'
              f' {rnd.uniform(1500,1980):.0f},{gy+rnd.uniform(-14,14):.0f}" fill="none"'
              f' stroke="#6b5438" stroke-width="{rnd.uniform(4,12):.1f}" opacity=".5"/>')
    if luzhi:
        for i in range(3):
            lx, ly = rnd.uniform(120, 1800), rnd.uniform(y0 + 70, H - 40)
            s += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rnd.uniform(40,86):.0f}"'
                  f' ry="{rnd.uniform(12,24):.0f}" fill="#9fc4d8" opacity=".55"/>')
    s += inej_mel(seed + 4, 44, y0 + 20, H - 6)
    return s


def _trava_suhaya(rnd, n, y0, y1, x0=0, x1=W):
    """Сухой бурьян по кромке: пучки разной высоты, чуть качаются."""
    s = ""
    for i in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        for k in range(rnd.randint(3, 6)):
            hh = rnd.uniform(18, 54)
            s += (f'<path d="M{x:.0f},{y:.0f} q{rnd.uniform(-10,10):.0f},{-hh*.6:.0f}'
                  f' {rnd.uniform(-16,16):.0f},{-hh:.0f}" fill="none" stroke="#8a7a4e"'
                  f' stroke-width="{rnd.uniform(1.8,3.2):.1f}" opacity="{rnd.uniform(.5,.9):.2f}"/>')
    return s


def _petuh(x, y, t, s_=1.0, ph=.0):
    """Петух на калитке: гребень, бородка, хвост косицами, тянет шею."""
    shea = 16 * s_ * A.ease(abs(A.w(t, 2.4, ph)))
    s = (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{54*s_:.0f}" ry="{40*s_:.0f}"'
         f' fill="#8d4a2a" stroke="{K}" stroke-width="{3.4*s_:.1f}"/>')
    s += (f'<path d="M{x-46*s_:.0f},{y+6*s_:.0f} q{-54*s_:.0f},{-30*s_:.0f}'
          f' {-30*s_:.0f},{-66*s_:.0f} q{30*s_:.0f},{20*s_:.0f} {24*s_:.0f},{58*s_:.0f} Z"'
          f' fill="#5e2f1a" stroke="{K}" stroke-width="{2.8*s_:.1f}"/>')
    for i in range(3):
        s += (f'<path d="M{x-40*s_:.0f},{y+2*s_:.0f} q{-56*s_-i*10*s_:.0f},{-26*s_-i*18*s_:.0f}'
              f' {-40*s_-i*22*s_:.0f},{-72*s_-i*14*s_:.0f}" fill="none" stroke="#7d3f22"'
              f' stroke-width="{5*s_:.1f}"/>')
    s += (f'<path d="M{x+32*s_:.0f},{y-20*s_:.0f} q{18*s_+shea:.0f},{-20*s_-shea:.0f}'
          f' {20*s_+shea:.0f},{-50*s_-shea:.0f} l{-26*s_:.0f},{-2*s_:.0f}'
          f' q{-2*s_:.0f},{26*s_:.0f} {-18*s_:.0f},{44*s_:.0f} Z" fill="#9c5630"'
          f' stroke="{K}" stroke-width="{2.8*s_:.1f}"/>')
    gx, gy = x + 34 * s_ + shea, y - 66 * s_ - shea
    s += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="{21*s_:.0f}" fill="#a85c33"'
          f' stroke="{K}" stroke-width="{3*s_:.1f}"/>')
    for i in range(3):
        s += (f'<path d="M{gx-10*s_+i*9*s_:.0f},{gy-18*s_:.0f} q{5*s_:.0f},{-16*s_:.0f}'
              f' {11*s_:.0f},{-2*s_:.0f} Z" fill="#c8301f" stroke="{K}" stroke-width="{2*s_:.1f}"/>')
    s += (f'<path d="M{gx+18*s_:.0f},{gy+2*s_:.0f} l{20*s_:.0f},{6*s_:.0f}'
          f' l{-20*s_:.0f},{7*s_:.0f} Z" fill="{ZOL}" stroke="{K}" stroke-width="{2*s_:.1f}"/>')
    s += (f'<ellipse cx="{gx+4*s_:.0f}" cy="{gy+22*s_:.0f}" rx="{7*s_:.0f}" ry="{12*s_:.0f}"'
          f' fill="#c8301f" stroke="{K}" stroke-width="{2*s_:.1f}"/>')
    s += (f'<circle cx="{gx+8*s_:.0f}" cy="{gy-4*s_:.0f}" r="{3.6*s_:.1f}" fill="{K}"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*12*s_:.0f},{y+36*s_:.0f} l{i*4*s_:.0f},{22*s_:.0f}"'
              f' stroke="{ZOL}" stroke-width="{4.4*s_:.1f}"/>')
    return s


def _ramka_lubok(x, y, w_, h_, col="#8a6342"):
    """Рамка «картинки в ряд»: тёсаная доска с уголками — внутри вид."""
    s = (f'<rect x="{x-10:.0f}" y="{y-10:.0f}" width="{w_+20:.0f}" height="{h_+20:.0f}"'
         f' rx="8" fill="{col}" stroke="{K}" stroke-width="5"/>')
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' fill="#2b3550" stroke="{K}" stroke-width="3"/>')
    for ax, ay in ((x - 6, y - 6), (x + w_ - 20, y - 6),
                   (x - 6, y + h_ - 20), (x + w_ - 20, y + h_ - 20)):
        s += (f'<rect x="{ax:.0f}" y="{ay:.0f}" width="26" height="26" rx="5"'
              f' fill="{MED}" stroke="{K}" stroke-width="2.6"/>')
    return s


def _cherta_zapreta(cx, cy, r, t, ph=.0, w_=16):
    """Красная запрещающая черта: круг и косая, встаёт рывком."""
    k = A.out(A.seg(t, .3 + ph, .5))
    if k <= .01:
        return ""
    s = (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*k:.0f}" fill="none"'
         f' stroke="#d6452a" stroke-width="{w_:.0f}" opacity=".92"/>')
    s += (f'<line x1="{cx-r*.72*k:.0f}" y1="{cy+r*.72*k:.0f}" x2="{cx+r*.72*k:.0f}"'
          f' y2="{cy-r*.72*k:.0f}" stroke="#d6452a" stroke-width="{w_:.0f}"'
          f' opacity=".92"/>')
    return s


def _valenok(x, y, s_=1.0, ug=0.0, col="#6f6256"):
    """Валенок: голенище, толстая подошва, заплата — узнаётся силуэтом."""
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x-30*s_:.0f},{y-130*s_:.0f} h{58*s_:.0f} q{14*s_:.0f},{66*s_:.0f}'
         f' {10*s_:.0f},{96*s_:.0f} q{26*s_:.0f},{6*s_:.0f} {30*s_:.0f},{26*s_:.0f}'
         f' l{-124*s_:.0f},0 q{-12*s_:.0f},{-52*s_:.0f}'
         f' {8*s_:.0f},{-104*s_:.0f} Z" fill="{col}" stroke="{K}"'
         f' stroke-width="{3.8*s_:.1f}"/>'
         f'<path d="M{x-33*s_:.0f},{y-134*s_:.0f} h{64*s_:.0f} q{6*s_:.0f},{16*s_:.0f}'
         f' {-2*s_:.0f},{26*s_:.0f} h{-60*s_:.0f} q{-6*s_:.0f},{-12*s_:.0f}'
         f' {-2*s_:.0f},{-26*s_:.0f} Z" fill="#8a8078" opacity=".55"/>')
    s += (f'<path d="M{x-40*s_:.0f},{y-26*s_:.0f} h{84*s_:.0f} q{12*s_:.0f},{10*s_:.0f}'
          f' {2*s_:.0f},{26*s_:.0f} l{-92*s_:.0f},0 Z" fill="#4a4038" stroke="{K}"'
          f' stroke-width="{3.2*s_:.1f}"/>')
    s += (f'<path d="M{x-28*s_:.0f},{y-124*s_:.0f} h{54*s_:.0f}" stroke="#55493f"'
          f' stroke-width="{5*s_:.1f}"/>')
    s += (f'<ellipse cx="{x+14*s_:.0f}" cy="{y-70*s_:.0f}" rx="{13*s_:.0f}"'
          f' ry="{17*s_:.0f}" fill="#7d7066" opacity=".8" stroke="{K}"'
          f' stroke-width="{2*s_:.1f}"/>')
    return s + '</g>'


# ── ДЕКОРАЦИИ ──────────────────────────────────────────────────────────────

def luzha_u_kalitki_pod_pervoy_korkoy(t):
    """Калитка двора морозным утром, перед ней большая лужа: её овал — проём
    с настоящим первым льдом. Мальчик занёс над лужей ногу, бабушка держит
    его за хлястик. Петух на калитке тянет шею."""
    rnd = random.Random(1901)
    gor = 430
    s = nebo("rassv", t, False, 19)
    s += oblaka(t, 150, 5, 11, .40)
    s += SL(Z_DAL, izba_snaruzhi(250, gor + 40, 330, t, True, True, 5)
            + dym(286, gor - 210, t, 6, .24, 300, .42, "#d7dee6", 1.0))
    s += SL(Z_DAL, ulica_dal(1180, gor + 30, 760, t, True, 9))
    s += SL(Z_DAL, goloe_derevo_ld(1620, gor + 46, 380, t, 7, 6, True))
    s += SL(Z_DAL, zabor_shtaket(-30, gor - 110, 760, 190, 5, 58)
            + zabor_shtaket(1190, gor - 96, 760, 176, 8, 60))
    s += SL(Z_SRED, _merzlaya_zemlya(gor + 20, 4, False))
    s += SL(Z_SRED, kalitka_rez(812, gor - 150, 300, 350, t, .10, True))
    s += SL(Z_SRED, ryabina(1468, gor + 140, t, 1.5, 6)
            + kalina_grozd(1510, gor + 60, t, 1.15, 12, 6, .3))

    # ЛУЖА: сначала рисованный вид, потом метка, потом кромка поверх
    lx, ly, lw, lh = 700, 712, 520, 360
    luzha = (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.56:.0f}"'
             f' ry="{lh*.56:.0f}" fill="#2f4a52"/>')
    luzha += korka_lda(lx + lw * .5, ly + lh * .5, lw * .50, lh * .48, t, .1, .0, .9)
    luzha += mesto_stoka(lx, ly, lw, lh, "ellips")
    luzha += (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.56:.0f}"'
              f' ry="{lh*.56:.0f}" fill="none" stroke="#6b5438" stroke-width="18"'
              f' opacity=".85"/>')
    luzha += (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.60:.0f}"'
              f' ry="{lh*.60:.0f}" fill="none" stroke="{INEY}" stroke-width="9"'
              f' opacity=".55"/>')
    luzha += _trava_suhaya(rnd, 7, ly + lh * .72, ly + lh + 30, lx - 40, lx + lw + 40)
    s += SL(Z_SRED, luzha)

    # МАЛЬЧИК: стоит на мёрзлой земле у края лужи, заносит правую ногу
    mx, my, mh = 520, 1012, 560
    noga = A.ease(A.seg(t, .4, 1.1))
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f4a6a", kant="#cfe4f5",
                           shapka=True, ph=.1))
    rk1, (e1x, e1y), _ = _ruka(mx, my, mh, -1, mh * .30, 18, t, "#3f4a6a", "#cfe4f5", .2, 7)
    rk2, (e2x, e2y), _ = _ruka(mx, my, mh, 1, mh * .30, 14, t, "#3f4a6a", "#cfe4f5", .5, 7)
    s += SL(Z_SRED, rk1 + varezhka(e1x - 10, e1y + 10, .9, -18, TKAN, t, .2)
            + rk2 + varezhka(e2x + 10, e2y + 10, .9, 16, TKAN, t, .6))
    s += SL(Z_SRED, _valenok(mx + 96 + 54 * noga, my - 36 - 74 * noga, .62, 16 + 14 * noga)
            + f'<path d="M{mx+40:.0f},{my-70:.0f} q{60*noga:.0f},{-40*noga:.0f}'
              f' {104*noga:.0f},{-54*noga:.0f}" fill="none" stroke="#3f4a6a"'
              f' stroke-width="26" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(mx + 34, my - mh * .80, t, .2, .9, .55))

    # БАБУШКА: за ним, правой держит хлястик, в левой ведро
    bx, by, bh = 356, 1046, 650
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.45))
    rk3, (e3x, e3y), _ = _ruka(bx, by, bh, 1, bh * .34, 26, t, "#4a3a52", "#cfe4f5", .3, 5)
    s += SL(Z_SRED, rk3 + f'<path d="M{e3x:.0f},{e3y:.0f} L{mx-70:.0f},{my-mh*.52:.0f}"'
                          f' stroke="#4a3a52" stroke-width="16" stroke-linecap="round"/>')
    rk4, (e4x, e4y), _ = _ruka(bx, by, bh, -1, bh * .30, 58, t, "#4a3a52", "#cfe4f5", .7, 4)
    kach = 5 * A.w(t, 1.5, .2)
    s += SL(Z_SRED, rk4
            + f'<g transform="rotate({kach:.1f} {e4x:.0f} {e4y:.0f})">'
              f'<path d="M{e4x-36:.0f},{e4y+10:.0f} h72 l-8,86 h-56 Z" fill="{ZHELEZ}"'
              f' stroke="{K}" stroke-width="4"/>'
              f'<ellipse cx="{e4x:.0f}" cy="{e4y+10:.0f}" rx="36" ry="11" fill="#8f979f"'
              f' stroke="{K}" stroke-width="3.4"/>'
              f'<path d="M{e4x-36:.0f},{e4y+6:.0f} q{36:.0f},{-34:.0f} {72:.0f},0"'
              f' fill="none" stroke="{CHUGUN}" stroke-width="5"/></g>')
    s += SL(Z_SRED, para_izo_rta(bx - 30, by - bh * .80, t, .6, 1.0, .5))
    s += SL(Z_SRED, ten(mx, my + 6, 120, 22, .45) + ten(bx, by + 6, 140, 24, .45))

    s += SL(Z_SRED, lavka(1240, 940, 300) + dvorovye_veschi(1300, 1066, 420, t, 12,
                                                            ["kadka", "churbak", "korzina"]))
    s += SL(Z_SRED, sledy_valenok(1860, 1066, 1180, 860, 6, 5, "#352a1c", 1.2))
    s += SL(Z_PERED, _petuh(900, gor - 196, t, 1.0, .2))
    s += SL(Z_PERED, goloe_derevo_ld(90, 1080, 560, t, 3, 5, True))
    s += ramka_pp("oba", "#0e0c0b", .55)
    s += vinetka(.40)
    return s


def tri_lda_prud_ozero_luzha(t):
    """Три картинки в ряд: пруд с мостками, озеро с вмёрзшей лодкой, лужа с
    кленовым листом. Над каждой встаёт красная черта, валенок заносится и
    отдёргивается. Людей нет."""
    rnd = random.Random(1902)
    s = nebo("sumer", t, True, 23)
    s += oblaka(t, 130, 6, 17, .38)
    s += SL(Z_DAL, ulica_dal(60, 470, 860, t, True, 13))
    s += SL(Z_DAL, izba_snaruzhi(1520, 500, 300, t, True, True, 8)
            + dym(1552, 300, t, 6, .22, 280, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(560, 6, True))

    # три «картинки»: вид внутри рамки
    for i, vid in enumerate(("prud", "ozero", "luzha")):
        x = 120 + i * 580
        y = 300
        w_, h_ = 500, 340
        s += SL(Z_SRED, _ramka_lubok(x, y, w_, h_))
        kus = ""
        if vid == "prud":
            kus += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_*.52:.0f}"'
                    f' fill="url(#nsumer)"/>')
            kus += (f'<rect x="{x:.0f}" y="{y+h_*.52:.0f}" width="{w_:.0f}"'
                    f' height="{h_*.48:.0f}" fill="url(#led)"/>')
            kus += korka_lda(x + w_ * .5, y + h_ * .74, w_ * .44, h_ * .20, t, .1)
            kus += mostki(x + 40, y + h_ * .62, 230, t, True, 60)
            kus += goloe_derevo_ld(x + w_ - 90, y + h_ * .56, 170, t, 9, 5, True)
            kus += kamysh(x + w_ - 44, y + h_ * .70, 70, t, 4, 3, True)
        elif vid == "ozero":
            kus += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_*.40:.0f}"'
                    f' fill="url(#nsumer)"/>')
            kus += (f'<rect x="{x:.0f}" y="{y+h_*.40:.0f}" width="{w_:.0f}"'
                    f' height="{h_*.60:.0f}" fill="#b9d6e8"/>')
            kus += treschina(x + w_ * .55, y + h_ * .70, 170, 11, 5)
            # лодка, вмёрзшая у берега
            kus += (f'<path d="M{x+90:.0f},{y+h_*.70:.0f} q{60:.0f},{44:.0f} {170:.0f},{10:.0f}'
                    f' q{-20:.0f},{-30:.0f} {-170:.0f},{-10:.0f} Z" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="4"/>')
            kus += (f'<path d="M{x+120:.0f},{y+h_*.70:.0f} l{-26:.0f},{-54:.0f}"'
                    f' stroke="#8a6342" stroke-width="7" fill="none"/>')
            kus += (f'<ellipse cx="{x+176:.0f}" cy="{y+h_*.78:.0f}" rx="96" ry="16"'
                    f' fill="{INEY}" opacity=".6"/>')
            kus += kamysh(x + 54, y + h_ * .60, 92, t, 5, 7, True)
        else:
            kus += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
                    f' fill="#5f4a32"/>')
            kus += (f'<path d="M{x:.0f},{y+h_*.66:.0f} q{w_*.5:.0f},{-30:.0f} {w_:.0f},{10:.0f}'
                    f' l0,{h_*.34:.0f} l{-w_:.0f},0 Z" fill="#4a3a2a"/>')
            kus += korka_lda(x + w_ * .5, y + h_ * .60, w_ * .36, h_ * .22, t, .4)
            # вмёрзший кленовый лист
            kus += (f'<path d="M{x+w_*.5:.0f},{y+h_*.52:.0f} l{34:.0f},{-26:.0f}'
                    f' l{-8:.0f},{26:.0f} l{34:.0f},{-6:.0f} l{-26:.0f},{24:.0f}'
                    f' l{22:.0f},{18:.0f} l{-34:.0f},{2:.0f} l{-4:.0f},{26:.0f}'
                    f' l{-22:.0f},{-20:.0f} l{-28:.0f},{14:.0f} l{10:.0f},{-28:.0f}'
                    f' l{-30:.0f},{-6:.0f} Z" fill="#9a5a28" stroke="#7d4a24"'
                    f' stroke-width="3"/>')
            kus += inej_mel(13, 16, y + h_ * .40, y + h_ * .92, x + 20, x + w_ - 20)
        s += SL(Z_SRED, kus)
        # валенок заносится над картинкой и отдёргивается
        faza = (t * .9 + i * .33) % 1.0
        pod = A.ease(min(1.0, faza * 2.2)) - A.ease(max(.0, faza * 2.2 - 1.1))
        s += SL(Z_PERED, _valenok(x + w_ * .5, y - 40 - 80 * pod, .78, -8 + 10 * pod))
        s += SL(Z_PERED, _cherta_zapreta(x + w_ * .5, y + h_ * .5, 150, t, i * .22, 15))

    s += SL(Z_SRED, kamysh(1870, 700, 180, t, 6, 19, True)
            + kamysh(40, 740, 150, t, 5, 21, True))
    # колодец с журавлём и корзина — обжитой низ кадра
    s += SL(Z_SRED, f'<rect x="760" y="880" width="260" height="120" rx="10"'
                    f' fill="{KAMEN}" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="890" cy="880" rx="130" ry="26" fill="{KAMEN2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1000,880 L1060,660" stroke="#6b4428" stroke-width="14"'
                    f' fill="none"/>'
                    f'<path d="M1060,660 L820,700" stroke="#6b4428" stroke-width="11"'
                    f' fill="none"/>'
                    f'<path d="M846,700 l6,80" stroke="#b9a37a" stroke-width="5"'
                    f' fill="none"/>'
                    f'<path d="M826,780 h52 l-6,44 h-40 Z" fill="{ZHELEZ}" stroke="{K}"'
                    f' stroke-width="3.4"/>')
    s += SL(Z_SRED, dvorovye_veschi(180, 1060, 420, t, 15, ["korzina", "vedro", "koryto"]))
    for i, (ux, uy) in enumerate(((1310, 1012), (1390, 1030), (1466, 1008))):
        s += SL(Z_SRED, ptica(ux, uy, t, 1.5, "#4a4038", i * .3, "#5b6a78"))
    s += SL(Z_LETIT, sneg_letit(t, 26, 9, .55, .7))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def slomannyy_led_i_pustoy_zakrom(t):
    """Озорник убегает от проломленной лужи, от пролома через двор к амбару
    бежит чёрная дорожка: в амбаре пустеют закрома, худеет мешок. У амбара
    стоит семья — отец со снятой шапкой, мать, дед на палке."""
    rnd = random.Random(1903)
    gor = 400
    s = nebo("den", t, False, 29)
    s += oblaka(t, 120, 5, 23, .45)
    s += SL(Z_DAL, ulica_dal(40, gor + 10, 700, t, True, 17))
    s += SL(Z_DAL, goloe_derevo_ld(680, gor + 24, 320, t, 11, 6, True))
    s += SL(Z_SRED, _merzlaya_zemlya(gor + 18, 7, False))

    # АМБАР справа: раскрытые ворота, закрома, полка с караваями, мешок
    ax, ay, aw, ah = 1120, 300, 700, 540
    amb = (f'<rect x="{ax:.0f}" y="{ay:.0f}" width="{aw:.0f}" height="{ah:.0f}"'
           f' fill="#4a3526" stroke="{K}" stroke-width="6"/>')
    amb += (f'<path d="M{ax-50:.0f},{ay:.0f} L{ax+aw*.5:.0f},{ay-170:.0f}'
            f' L{ax+aw+50:.0f},{ay:.0f} Z" fill="#5e4430" stroke="{K}" stroke-width="6"/>')
    amb += (f'<path d="M{ax-50:.0f},{ay:.0f} L{ax+aw*.5:.0f},{ay-170:.0f}'
            f' L{ax+aw+50:.0f},{ay:.0f}" fill="none" stroke="url(#sneg)" stroke-width="16"'
            f' opacity=".9"/>')
    amb += doski(ax + 40, ay + 40, aw - 80, ah - 60, 64, True)
    s += SL(Z_DAL, amb)
    # пустеющие закрома: уровень зерна падает, караваи исчезают по очереди
    uh = A.ease(A.seg(t, .5, 2.6))
    zak = ""
    for i in range(3):
        zx = ax + 70 + i * 200
        zak += (f'<rect x="{zx:.0f}" y="{ay+250:.0f}" width="160" height="190" rx="8"'
                f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
        hh = 120 * (1 - uh * (.55 + i * .15))
        zak += (f'<rect x="{zx+12:.0f}" y="{ay+430-hh:.0f}" width="136" height="{hh:.0f}"'
                f' fill="#c8a05a" opacity=".95"/>')
        zak += (f'<ellipse cx="{zx+80:.0f}" cy="{ay+430-hh:.0f}" rx="68" ry="13"'
                f' fill="#dbb771"/>')
    s += SL(Z_SRED, zak)
    pol = polka(ax + 90, ay + 170, 520)
    for i in range(4):
        if uh * 4 < 3 - i + .6:
            pol += karavay(ax + 150 + i * 140, ay + 168, .62, i % 2 == 0)
    s += SL(Z_SRED, pol)
    msh = 1 - .45 * uh
    s += SL(Z_SRED, f'<path d="M{ax+560:.0f},{ay+440:.0f} q{-30*msh:.0f},{-150*msh:.0f}'
                    f' {40*msh:.0f},{-190*msh:.0f} q{70*msh:.0f},{40*msh:.0f}'
                    f' {40*msh:.0f},{190*msh:.0f} Z" fill="#b9a37a" stroke="{K}"'
                    f' stroke-width="4.5"/>'
                    f'<path d="M{ax+590:.0f},{ay+260:.0f} q{20:.0f},{-26:.0f} {42:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#8a7a52" stroke-width="6"/>')

    # ПРОЛОМЛЕННАЯ ЛУЖА слева и чёрная дорожка от неё к амбару
    s += SL(Z_SRED, korka_lda(300, 940, 210, 96, t, .2, .95))
    beg = A.ease(A.seg(t, .3, 2.2))
    put = f'M320,960'
    for i in range(1, 9):
        p = i / 8.0
        put += f' Q{320+ (ax-320)*p - 60:.0f},{960 - 150*math.sin(p*3.14):.0f} {320 + (ax+120-320)*p:.0f},{950 - 240*p:.0f}'
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#17120d" stroke-width="22"'
                    f' opacity=".75" stroke-dasharray="{2400*beg:.0f} 4000"/>')

    # ОЗОРНИК убегает влево, обе руки машут, шарф летит
    bx, by, bh = 470, 1012, 470
    beg2 = A.ease(A.seg(t, .2, 1.8))
    bx -= 120 * beg2
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#6b3a2a", kant="#ffd9a8",
                           shapka=True, ph=.1, naklon=4.0))
    r1, (q1x, q1y), _ = _ruka(bx, by, bh, -1, bh * .32, -36, t, "#6b3a2a", "#ffd9a8", .1, 16)
    r2, (q2x, q2y), _ = _ruka(bx, by, bh, 1, bh * .32, 46, t, "#6b3a2a", "#ffd9a8", .5, 16)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{bx+30:.0f},{by-bh*.62:.0f} q{90:.0f},{10+14*A.w(t,.8,.2):.0f}'
                    f' {170:.0f},{-20:.0f} l{6:.0f},{34:.0f} q{-86:.0f},{26:.0f}'
                    f' {-176:.0f},{14:.0f} Z" fill="{TKAN}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, para_izo_rta(bx - 40, by - bh * .80, t, .3, .9, .5))

    # СЕМЬЯ у амбара: отец со снятой шапкой, мать, дед на палке, ребёнок
    ox, oy, oh = 980, 1040, 540
    s += SL(Z_SRED, figura(ox, oy, oh, t, col="#3f3a4a", kant="#ffd9a8", ph=.2, boroda=True))
    r3, (e3x, e3y), _ = _ruka(ox, oy, oh, 1, oh * .26, 54, t, "#3f3a4a", "#ffd9a8", .2, 3)
    s += SL(Z_SRED, r3 + f'<ellipse cx="{e3x+14:.0f}" cy="{e3y+18:.0f}" rx="44" ry="26"'
                         f' fill="#4a3a2c" stroke="{K}" stroke-width="4"/>'
                         f'<ellipse cx="{e3x+14:.0f}" cy="{e3y+8:.0f}" rx="44" ry="13"'
                         f' fill="#8a6a4a" stroke="{K}" stroke-width="3"/>')
    mx2, my2, mh2 = 820, 1052, 520
    s += SL(Z_SRED, figura(mx2, my2, mh2, t, col="#5a3a4a", kant="#ffd9a8",
                           platok=True, ph=.5))
    r4, _, _ = _ruka(mx2, my2, mh2, 1, mh2 * .22, 70, t, "#5a3a4a", "#ffd9a8", .4, 4)
    s += SL(Z_SRED, r4)
    dx, dy, dh = 1120, 1066, 520
    kach = 3.0 * A.w(t, 2.2, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {dx:.0f} {dy:.0f})">'
            + figura(dx, dy, dh, t, col="#4a443c", kant="#ffd9a8", boroda=True, ph=.8)
            + '</g>')
    r5, (e5x, e5y), _ = _ruka(dx, dy, dh, 1, dh * .30, 62, t, "#4a443c", "#ffd9a8", .6, 3)
    s += SL(Z_SRED, r5 + f'<path d="M{e5x:.0f},{e5y-20:.0f} l{18:.0f},{dy-e5y+16:.0f}"'
                         f' stroke="#7d5636" stroke-width="12" stroke-linecap="round"/>')
    s += SL(Z_SRED, ten(ox, oy + 6, 110, 20, .4) + ten(mx2, my2 + 6, 104, 19, .4)
            + ten(dx, dy + 6, 110, 20, .4) + ten(bx, by + 6, 96, 18, .4))

    # двор: телега, корыто, ворота, собака
    s += SL(Z_SRED, f'<rect x="580" y="820" width="300" height="34" rx="6" fill="{DOSKA}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="640" cy="900" r="54" fill="none" stroke="#6b4428"'
                    f' stroke-width="13"/>'
                    f'<circle cx="830" cy="900" r="54" fill="none" stroke="#6b4428"'
                    f' stroke-width="13"/>'
                    f'<path d="M580,838 L470,790" stroke="#7d5636" stroke-width="10"'
                    f' fill="none"/>')
    s += SL(Z_SRED, dvorovye_veschi(120, 1066, 420, t, 19, ["koryto", "grabli", "churbak"]))
    s += SL(Z_SRED, kot(700, 1044, t, 1.4, "#55493f", False))
    s += SL(Z_SRED, sledy_valenok(640, 1070, 300, 962, 6, 9, "#352a1c", 1.1))
    s += SL(Z_PERED, zabor_shtaket(-40, 880, 420, 200, 13, 56))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def prud_pod_pervym_ldom(t):
    """Пруд на рассвете под первым льдом: под прозрачным льдом спит сама
    Вода — девица с длинными волосами под ледяным одеялом, рядом дремлют
    карась и лягушка. В окне избы на берегу — настоящий замёрзший пруд."""
    rnd = random.Random(1904)
    gor = 430
    s = nebo("rassv", t, False, 31)
    s += oblaka(t, 140, 5, 29, .40)
    s += SL(Z_DAL, goloe_derevo_ld(300, gor + 30, 420, t, 13, 7, True))
    s += SL(Z_DAL, f'<path d="M120,{gor+20:.0f} q60,-180 180,-210 q-40,120 -40,210 Z"'
                   f' fill="#4a4a3a" opacity=".8"/>')
    # баня с дымом на дальнем берегу
    s += SL(Z_DAL, izba_snaruzhi(1660, gor + 16, 250, t, True, True, 11)
            + dym(1686, gor - 150, t, 6, .22, 260, .40, "#d7dee6", .9))

    # ИЗБА НА БЕРЕГУ с окном-проёмом (справа сверху)
    ix, iy, iw, ih = 1020, 150, 880, 470
    izba = (f'<rect x="{ix:.0f}" y="{iy:.0f}" width="{iw:.0f}" height="{ih:.0f}"'
            f' fill="#5e4430" stroke="{K}" stroke-width="6"/>')
    izba += brevna(ix, iy, iw, ih, 82, 1)
    izba += (f'<path d="M{ix-60:.0f},{iy:.0f} L{ix+iw*.5:.0f},{iy-160:.0f}'
             f' L{ix+iw+60:.0f},{iy:.0f} Z" fill="#4a3526" stroke="{K}" stroke-width="6"/>')
    izba += (f'<path d="M{ix-60:.0f},{iy:.0f} L{ix+iw*.5:.0f},{iy-160:.0f}'
             f' L{ix+iw+60:.0f},{iy:.0f}" fill="none" stroke="url(#sneg)"'
             f' stroke-width="18" opacity=".92"/>')
    s += SL(Z_DAL, izba)
    px, py, pw, ph_ = 1120, 230, 780, 320
    okno = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
            f' fill="#9fc4d8"/>')
    okno += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.45:.0f}"'
             f' fill="#c4d8e8"/>')
    okno += mesto_stoka(px, py, pw, ph_, "pryam")
    okno += (f'<rect x="{px-16:.0f}" y="{py-16:.0f}" width="{pw+32:.0f}"'
             f' height="{ph_+32:.0f}" rx="6" fill="none" stroke="#6b4428"'
             f' stroke-width="26"/>')
    okno += (f'<path d="M{px+pw*.5:.0f},{py:.0f} l0,{ph_:.0f} M{px:.0f},{py+ph_*.5:.0f}'
             f' l{pw:.0f},0" stroke="#6b4428" stroke-width="16"/>')
    okno += (f'<path d="M{px+20:.0f},{py+ph_-24:.0f} q{pw*.2:.0f},{-40:.0f}'
             f' {pw*.42:.0f},{-16:.0f}" fill="none" stroke="#ffffff" stroke-width="9"'
             f' opacity=".30"/>')
    okno += (f'<rect x="{px-46:.0f}" y="{py-46:.0f}" width="{pw+92:.0f}" height="34"'
             f' rx="6" fill="{DOSKA2}" stroke="{K}" stroke-width="5"/>')
    for i in range(7):
        okno += (f'<path d="M{px-30+i*(pw+60)/6:.0f},{py-12:.0f} q{12:.0f},{-22:.0f}'
                 f' {24:.0f},0 Z" fill="{DOSKA}" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_DAL, okno)

    # ПРУД: лёд, под ним спящая Вода
    led_y = 640
    s += SL(Z_SRED, ledyanoe_pole(led_y, t, 23, True, True))
    dyh = 7 * A.w(t, 5.2, .1)
    voda = (f'<ellipse cx="760" cy="{880+dyh:.0f}" rx="420" ry="150" fill="#2f6b78"'
            f' opacity=".45"/>')
    voda += (f'<path d="M420,{900+dyh:.0f} q180,{-120:.0f} 420,{-70:.0f}'
             f' q180,{24:.0f} 260,{70:.0f} q-60,{80:.0f} -340,{80:.0f}'
             f' q-280,0 -340,{-80:.0f} Z" fill="#dcecf8" opacity=".55"/>')
    # девица: голова, плечи, длинные струящиеся волосы, ледяное одеяло
    voda += (f'<ellipse cx="560" cy="{852+dyh:.0f}" rx="76" ry="84" fill="#eaf6ff"'
             f' opacity=".97" stroke="#4a7a8a" stroke-width="7"/>')
    for i in (-1, 1):
        voda += (f'<path d="M{560+i*26:.0f},{842+dyh:.0f} q{i*10:.0f},{8:.0f} {i*22:.0f},0"'
                 f' fill="none" stroke="#2f4a56" stroke-width="7"/>')
    voda += (f'<path d="M524,{886+dyh:.0f} q36,{20:.0f} 72,0" fill="none"'
             f' stroke="#2f4a56" stroke-width="7"/>')
    for i in range(9):
        vl = 8 * A.w(t, 3.4, i * .2)
        voda += (f'<path d="M{520+i*10:.0f},{812+dyh:.0f} q{-120-vl:.0f},{60:.0f}'
                 f' {-300-vl*2:.0f},{54+i*8:.0f}" fill="none" stroke="#9fd0e4"'
                 f' stroke-width="7" opacity=".7"/>')
    voda += (f'<path d="M600,{890+dyh:.0f} q180,{-40:.0f} 370,{20:.0f} l0,{70:.0f}'
             f' q-190,{-30:.0f} -370,{20:.0f} Z" fill="#eaf6ff" opacity=".65"'
             f' stroke="#cfe4f5" stroke-width="4"/>')
    # карась и лягушка
    plav = 9 * A.w(t, 2.0, .3)
    voda += (f'<path d="M1080,{930:.0f} q40,{-26:.0f} 92,0 q-44,{26:.0f} -92,0 Z"'
             f' fill="#b58a3a" stroke="{K}" stroke-width="3.4"/>'
             f'<path d="M1172,{930:.0f} l{26+plav:.0f},{-16:.0f} l0,{32:.0f} Z"'
             f' fill="#9a722c" stroke="{K}" stroke-width="3"/>'
             f'<circle cx="1098" cy="926" r="4.6" fill="{K}"/>')
    voda += (f'<ellipse cx="1300" cy="968" rx="46" ry="30" fill="#5f7a3a"'
             f' stroke="{K}" stroke-width="3.4"/>'
             f'<circle cx="1282" cy="946" r="12" fill="#6f8c4a" stroke="{K}"'
             f' stroke-width="3"/><circle cx="1318" cy="946" r="12" fill="#6f8c4a"'
             f' stroke="{K}" stroke-width="3"/>'
             f'<circle cx="1282" cy="944" r="4" fill="{K}"/>'
             f'<circle cx="1318" cy="944" r="4" fill="{K}"/>')
    s += SL(Z_SRED, voda)
    s += SL(Z_SRED, korka_lda(760, 880, 440, 160, t, .3, .0, .55, .5))

    # мостки и двое на них
    s += SL(Z_SRED, mostki(180, 700, 520, t, True, 180))
    bx, by, bh = 330, 712, 420
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.3, naklon=3.0))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, -1, bh * .26, -14, t, "#4a3a52", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, 1, bh * .22, -30, t, "#4a3a52", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    cyp = 10 * A.ease(abs(A.w(t, 2.6, .2)))
    vx, vy, vh = 540, 706 - cyp, 330
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#6b4a5a", kant="#cfe4f5",
                           platok=True, ph=.7))
    s += SL(Z_SRED, para_izo_rta(bx - 26, by - bh * .80, t, .4, .8, .5)
            + para_izo_rta(vx - 20, vy - vh * .80, t, .9, .7, .45))
    s += SL(Z_SRED, ten(bx, by + 4, 90, 16, .4) + ten(vx, vy + 4, 70, 13, .4))
    # лодка у берега, камыши, ведро
    s += SL(Z_SRED, f'<path d="M60,900 q80,{60:.0f} 300,{20:.0f} q-40,{-54:.0f}'
                    f' -300,{-20:.0f} Z" fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M120,890 l-30,-70" stroke="#8a6342" stroke-width="9"'
                    f' fill="none"/>')
    s += SL(Z_SRED, kamysh(90, 1000, 200, t, 6, 27, True)
            + kamysh(1780, 1010, 230, t, 7, 31, True))
    s += SL(Z_SRED, dvorovye_veschi(1450, 1066, 380, t, 23, ["vedro", "korzina"]))
    s += SL(Z_PERED, goloe_derevo_ld(1870, 1080, 620, t, 17, 6, True))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.40)
    return s


def palka_i_kamen_nad_ldom(t):
    """Край пруда и мостки: мальчик занёс над льдом палку, мужик взвесил
    камень. Над обоими встают красные черты — палка ложится на мостки,
    камень возвращается на берег."""
    rnd = random.Random(1905)
    s = nebo("den", t, False, 37)
    s += oblaka(t, 150, 6, 31, .42)
    s += SL(Z_DAL, ulica_dal(1180, 430, 760, t, True, 19))
    s += SL(Z_DAL, goloe_derevo_ld(250, 470, 460, t, 19, 7, True))
    s += SL(Z_DAL, izba_snaruzhi(760, 452, 240, t, True, True, 13)
            + dym(786, 300, t, 5, .22, 240, .38, "#d7dee6", .9))
    s += SL(Z_SRED, ledyanoe_pole(560, t, 29, True, True))
    s += SL(Z_SRED, korka_lda(1180, 820, 430, 150, t, .2, .0, .75, .35))
    s += SL(Z_SRED, mostki(120, 740, 780, t, True, 220))
    # вмёрзшая лодка, ведро, верша на колу, ворона
    s += SL(Z_SRED, f'<path d="M1480,880 q90,{64:.0f} 330,{16:.0f} q-44,{-58:.0f}'
                    f' -330,{-16:.0f} Z" fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="1640" cy="906" rx="180" ry="26" fill="{INEY}"'
                    f' opacity=".55"/>')
    s += SL(Z_SRED, f'<path d="M1320,1066 l14,-250" stroke="#7d5636" stroke-width="14"'
                    f' fill="none"/>'
                    f'<path d="M1300,830 q40,{-70:.0f} 86,{-6:.0f} q-30,{70:.0f} -86,{6:.0f} Z"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{1302+i*16:.0f},{824-i*4:.0f} q{30:.0f},{-30:.0f}'
                        f' {56:.0f},{6:.0f}" fill="none" stroke="#8a7a52" stroke-width="3"/>')
    vor = 7 * A.w(t, 2.2, .2)
    s += SL(Z_SRED, f'<ellipse cx="{1340+vor:.0f}" cy="790" rx="44" ry="30"'
                    f' fill="#23242a" stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="{1370+vor:.0f}" cy="764" r="20" fill="#23242a"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{1388+vor:.0f},762 l26,6 l-26,7 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="2.4"/>'
                    f'<circle cx="{1376+vor:.0f}" cy="758" r="3.6" fill="#e8e2d6"/>'
                    f'<path d="M{1300+vor:.0f},790 q{-40:.0f},{10:.0f} {-56:.0f},{-14:.0f}"'
                    f' fill="none" stroke="#17181c" stroke-width="9"/>')

    # МАЛЬЧИК с палкой: опускает её на мостки
    opusk = A.ease(A.seg(t, .6, 1.6))
    mx, my, mh = 470, 742, 480
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#4a5a6a", kant="#ffd9a8",
                           tulup=True, shapka=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -20 + 70 * opusk, t,
                              "#4a5a6a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .24, -4 + 60 * opusk, t,
                              "#4a5a6a", "#ffd9a8", .5, 5)
    s += SL(Z_SRED, r1 + r2)
    pal_ug = -34 + 54 * opusk
    s += SL(Z_SRED, f'<g transform="rotate({pal_ug:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-20:.0f}" y="{e1y-10:.0f}" width="320" height="17"'
                    f' rx="8" fill="#7d5636" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e1x+240:.0f},{e1y-10:.0f} q{26:.0f},{-16:.0f}'
                    f' {46:.0f},{6:.0f}" fill="none" stroke="#6b4428" stroke-width="7"/></g>')
    s += SL(Z_SRED, para_izo_rta(mx - 30, my - mh * .80, t, .3, .9, .5))

    # МУЖИК: взвесил камень на правой рукавице, левая на поясе
    ux, uy, uh = 900, 752, 620
    vzves = 16 * A.w(t, 1.6, .1) * (1 - A.ease(A.seg(t, 1.6, 1.4)))
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#3a3f4a", kant="#ffd9a8",
                           shapka=True, tulup=True, boroda=True, ph=.6))
    r3, (e3x, e3y), _ = _ruka(ux, uy, uh, 1, uh * .30, 30 + 26 * A.ease(A.seg(t, 1.6, 1.4)),
                              t, "#3a3f4a", "#ffd9a8", .3, 4)
    r4, (e4x, e4y), _ = _ruka(ux, uy, uh, -1, uh * .22, 60, t, "#3a3f4a", "#ffd9a8", .8, 3)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, varezhka(e3x + 8, e3y + 16, 1.1, 8, "#5a4a3a", t, .3)
            + f'<ellipse cx="{e3x+14:.0f}" cy="{e3y-4+vzves:.0f}" rx="40" ry="31"'
              f' fill="{KAMEN}" stroke="{K}" stroke-width="4"/>'
              f'<path d="M{e3x-10:.0f},{e3y-16+vzves:.0f} q{22:.0f},{-14:.0f}'
              f' {44:.0f},{4:.0f}" fill="none" stroke="{KAMEN2}" stroke-width="7"/>')
    s += SL(Z_SRED, para_izo_rta(ux - 36, uy - uh * .80, t, .7, 1.0, .5))
    s += SL(Z_SRED, ten(mx, my + 4, 90, 16, .4) + ten(ux, uy + 4, 110, 19, .4))
    s += SL(Z_SRED, dvorovye_veschi(1560, 1066, 340, t, 29, ["vedro", "kadka"]))
    s += SL(Z_PERED, _cherta_zapreta(470, 470, 180, t, .0, 17)
            + _cherta_zapreta(930, 430, 200, t, .25, 17))
    s += SL(Z_PERED, kamysh(60, 1060, 240, t, 7, 33, True))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def sled_do_serediny_reki(t):
    """Река под первым льдом: цепь следов обрывается у почерневшего пятна,
    на льду осталась одна рукавица. Мужик с жердью стоит на твёрдом берегу
    и поворачивает к мосту вдали. Беды в кадре нет."""
    rnd = random.Random(1906)
    s = nebo("sumer", t, False, 41)
    s += oblaka(t, 130, 5, 37, .40)
    s += SL(Z_DAL, ulica_dal(1240, 420, 700, t, True, 23))
    s += SL(Z_DAL, izba_snaruzhi(1480, 436, 260, t, True, True, 17)
            + dym(1506, 280, t, 6, .22, 250, .40, "#d7dee6", .9))
    # мост вдали
    most = (f'<rect x="980" y="372" width="620" height="26" fill="#6b4428"'
            f' stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        most += (f'<rect x="{1020+i*140:.0f}" y="398" width="20" height="120"'
                 f' fill="#54351f" stroke="{K}" stroke-width="3"/>')
    for i in range(9):
        most += (f'<rect x="{990+i*72:.0f}" y="330" width="12" height="46"'
                 f' fill="#7d5636" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_DAL, most)
    s += SL(Z_SRED, ledyanoe_pole(500, t, 37, True, True))
    # тёмное пятно, где лёд прогнулся
    s += SL(Z_SRED, f'<ellipse cx="1140" cy="760" rx="210" ry="74" fill="#17424c"'
                    f' opacity=".82"/>'
                    f'<ellipse cx="1140" cy="760" rx="150" ry="48" fill="#0f2a32"'
                    f' opacity=".9"/>'
            + treschina(1140, 760, 250, 43, 6))
    s += SL(Z_SRED, sledy_valenok(360, 1010, 1180, 772, 11, 47, "#3a4a52", 1.25, .72))
    # одинокая рукавица на льду
    s += SL(Z_SRED, varezhka(1012, 836, 1.0, -28, TKAN, t, .4)
            + ten(1012, 866, 44, 11, .35))
    s += SL(Z_SRED, korka_lda(620, 900, 330, 110, t, .5, .0, .6, .4))

    # МУЖИК на берегу: жердь поперёк груди обеими руками, поворачивает к мосту
    pov = A.ease(A.seg(t, 1.2, 1.8))
    ux, uy, uh = 420, 1050, 640
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#3f3a33", kant="#cfe4f5",
                           tulup=True, shapka=True, boroda=True, ph=.3,
                           naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(ux, uy, uh, 1, uh * .26, 8 - 20 * pov, t,
                              "#3f3a33", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ux, uy, uh, -1, uh * .26, 10 - 18 * pov, t,
                              "#3f3a33", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    zh_ug = -8 + 14 * pov
    s += SL(Z_SRED, f'<g transform="rotate({zh_ug:.1f} {ux:.0f} {e1y:.0f})">'
                    f'<rect x="{ux-300:.0f}" y="{e1y-9:.0f}" width="620" height="18"'
                    f' rx="9" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{ux+300:.0f},{e1y:.0f} l{34:.0f},{-12:.0f} l0,{24:.0f} Z"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, para_izo_rta(ux - 40 + 20 * pov, uy - uh * .80, t, .4, 1.0, .55))
    s += SL(Z_SRED, ten(ux, uy + 6, 120, 20, .45))
    # ивняк на берегу, сани на том берегу
    for i, (kx, kb) in enumerate(((120, 1066), (250, 1050), (1860, 1040))):
        s += SL(Z_SRED, goloe_derevo_ld(kx, kb, 300 + i * 40, t, 47 + i, 6, True))
    s += SL(Z_SRED, sani_s_rogozhey(1700, 560, .62, t, .3, True))
    s += SL(Z_SRED, _trava_suhaya(rnd, 9, 980, 1070, 60, 700))
    s += SL(Z_PERED, kamysh(1880, 1070, 280, t, 8, 53, True))
    s += SL(Z_LETIT, sneg_letit(t, 22, 11, .45, .6))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def neudacha_idet_sledom(t):
    """Баба у чужого забора смотрит на новую шубу соседки и уходит прочь, а
    за ней семенит Неудача — тощая серая кошка с рваным ухом и дырявым
    мешком. Соседка на крыльце выбивает половик."""
    rnd = random.Random(1907)
    gor = 470
    s = nebo("den", t, False, 43)
    s += oblaka(t, 140, 6, 41, .44)
    s += SL(Z_DAL, ulica_dal(60, gor - 10, 900, t, True, 29))
    s += SL(Z_DAL, izba_snaruzhi(1180, gor + 40, 460, t, True, True, 19)
            + dym(1226, gor - 206, t, 7, .24, 300, .44, "#d7dee6", 1.0))
    s += SL(Z_DAL, goloe_derevo_ld(820, gor + 40, 360, t, 23, 6, True))
    s += SL(Z_SRED, sneg_lezhit(gor + 60, 30, "url(#sneg)"))
    s += SL(Z_SRED, _merzlaya_zemlya(gor + 180, 11, False))
    s += SL(Z_SRED, f'<rect x="0" y="{gor+160:.0f}" width="{W}" height="{H-gor-160:.0f}"'
                    f' fill="url(#sneg)" opacity=".92"/>'
            + inej_mel(17, 70, gor + 170, H - 10))

    # ЗАБОР посреди кадра: по эту сторону — баба, по ту — двор соседки
    s += SL(Z_SRED, zabor_shtaket(880, gor + 60, 1040, 230, 23, 62))
    # верёвка с новой шубой во дворе соседки
    kch = 6 * A.w(t, 2.4, .2)
    s += SL(Z_SRED, f'<path d="M1180,{gor+30:.0f} q260,{30:.0f} 540,{-10:.0f}"'
                    f' fill="none" stroke="#b9a37a" stroke-width="5"/>'
                    f'<g transform="rotate({kch:.1f} 1420 {gor+40:.0f})">'
                    f'<path d="M1330,{gor+44:.0f} q90,{-28:.0f} 180,0 l{30:.0f},{250:.0f}'
                    f' q{-120:.0f},{40:.0f} {-240:.0f},0 Z" fill="#6b3a2a" stroke="{K}"'
                    f' stroke-width="5"/>'
                    f'<path d="M1330,{gor+44:.0f} q90,{34:.0f} 180,0" fill="none"'
                    f' stroke="#e8e2d6" stroke-width="16" opacity=".9"/>'
                    f'<path d="M1420,{gor+60:.0f} l0,{240:.0f}" stroke="#4a2a1e"'
                    f' stroke-width="6" opacity=".8"/>'
                    f'<path d="M1310,{gor+70:.0f} l{-34:.0f},{170:.0f}" stroke="#6b3a2a"'
                    f' stroke-width="34" stroke-linecap="round"/>'
                    f'<path d="M1530,{gor+70:.0f} l{34:.0f},{170:.0f}" stroke="#6b3a2a"'
                    f' stroke-width="34" stroke-linecap="round"/></g>')

    # СОСЕДКА на крыльце выбивает половик
    kx, ky, kh = 1700, 820, 540
    s += SL(Z_SRED, f'<rect x="1560" y="820" width="340" height="30" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1580" y="850" width="300" height="24" rx="5"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="3.5"/>')
    s += SL(Z_SRED, figura(kx, ky, kh, t, col="#5a3a4a", kant="#ffd9a8",
                           platok=True, ph=.4))
    vzmah = A.w(t, 1.0, .0)
    r1, (e1x, e1y), _ = _ruka(kx, ky, kh, -1, kh * .30, -16 + 26 * vzmah, t,
                              "#5a3a4a", "#ffd9a8", .1, 9)
    s += SL(Z_SRED, r1 + f'<g transform="rotate({-16+20*vzmah:.1f} {e1x:.0f} {e1y:.0f})">'
                         f'<rect x="{e1x-150:.0f}" y="{e1y:.0f}" width="160" height="110"'
                         f' rx="6" fill="{TKAN2}" stroke="{K}" stroke-width="4"/>'
                         f'<path d="M{e1x-144:.0f},{e1y+30:.0f} h148 M{e1x-144:.0f},'
                         f'{e1y+66:.0f} h148" stroke="{RUSH}" stroke-width="8"'
                         f' opacity=".8"/></g>')
    s += SL(Z_SRED, para_izo_rta(kx - 30, ky - kh * .80, t, .3, .9, .5))

    # БАБА: смотрит через жердь забора и уходит прочь
    uh = A.ease(A.seg(t, .8, 1.4))
    bx, by, bh = 640 - 150 * uh, 1040, 650
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#5e5a55", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.6, naklon=2.0))
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, 1, bh * .26, 16 + 30 * uh, t,
                              "#5e5a55", "#cfe4f5", .2, 4)
    r3, (e3x, e3y), _ = _ruka(bx, by, bh, -1, bh * .24, 20 + 26 * uh, t,
                              "#5e5a55", "#cfe4f5", .7, 4)
    s += SL(Z_SRED, r2 + r3)
    s += SL(Z_SRED, para_izo_rta(bx - 36, by - bh * .80, t, .5, 1.0, .5))
    s += SL(Z_SRED, ten(bx, by + 6, 120, 20, .4) + ten(kx, ky + 6, 110, 19, .4))
    # НЕУДАЧА семенит следом
    s += SL(Z_SRED, neudacha_figurka(bx + 240 - 120 * uh, 1066, t, .85, .3))
    s += SL(Z_SRED, sledy_valenok(960, 1070, 700, 1006, 5, 59, "#8aa0b4", 1.1))
    # колодец, поленница, сани, синицы
    s += SL(Z_SRED, f'<rect x="120" y="760" width="230" height="110" rx="8"'
                    f' fill="{KAMEN}" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="235" cy="760" rx="115" ry="24" fill="{KAMEN2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M150,760 l-10,-150 h190 l-10,150" fill="none"'
                    f' stroke="#6b4428" stroke-width="12"/>'
                    f'<path d="M140,616 h200" stroke="#54351f" stroke-width="14"/>'
                    f'<path d="M240,616 l6,120" stroke="#b9a37a" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="420" y="800" width="250" height="150" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<circle cx="{436+(i%6)*44:.0f}" cy="{824+(i//6)*52:.0f}" r="21"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, sanki_derev(300, 1050, .9, t, .4, True))
    for i, (px, py) in enumerate(((1020, 560), (1086, 596))):
        s += SL(Z_SRED, ptica(px, py, t, 1.3, "#4a6a78", i * .4, "#b5803a"))
    s += SL(Z_LETIT, sneg_letit(t, 20, 13, .40, .55))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def gorod_u_yuzhnogo_morya(t):
    """Смена главы: тёплый южный свет. Каменный город на холмах у моря —
    стены с башнями, черепица, колоннада, маяк, корабли в гавани. По дороге
    к воротам идёт человек со спины: в правой руке посох, левая на суме."""
    rnd = random.Random(1908)
    s = (f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>')
    s += nebo("den", t, False, 47)
    s += oblaka(t, 120, 4, 43, .30, "#ffe9c8")
    s += SL(Z_NEBO, f'<circle cx="1560" cy="250" r="110" fill="#ffe9ac" opacity=".55"/>'
                    f'<circle cx="1560" cy="250" r="64" fill="#fff4d8" opacity=".9"/>')
    # море и гавань
    s += SL(Z_DAL, f'<rect x="0" y="430" width="{W}" height="300" fill="#2f6b78"/>')
    for i in range(14):
        yy = 440 + i * 20
        s += SL(Z_DAL, f'<path d="M{rnd.uniform(-60,200):.0f},{yy:.0f}'
                       f' q{rnd.uniform(200,420):.0f},{rnd.uniform(-8,8):.0f}'
                       f' {rnd.uniform(700,1200):.0f},{rnd.uniform(-5,5):.0f}" fill="none"'
                       f' stroke="#4a8a94" stroke-width="{rnd.uniform(2,5):.1f}" opacity=".6"/>')
    for i, (kx, ky, ks) in enumerate(((330, 640, 1.0), (620, 600, .76), (170, 586, .62))):
        puz = 10 * A.w(t, 3.0, i * .3)
        s += SL(Z_DAL, f'<path d="M{kx-70*ks:.0f},{ky:.0f} q{70*ks:.0f},{40*ks:.0f}'
                       f' {140*ks:.0f},0 q{-20*ks:.0f},{-26*ks:.0f} {-140*ks:.0f},0 Z"'
                       f' fill="#6b4428" stroke="{K}" stroke-width="{3.4*ks:.1f}"/>'
                       f'<rect x="{kx-4*ks:.0f}" y="{ky-120*ks:.0f}" width="{8*ks:.0f}"'
                       f' height="{120*ks:.0f}" fill="#8a6342"/>'
                       f'<path d="M{kx:.0f},{ky-116*ks:.0f} q{(50+puz)*ks:.0f},{40*ks:.0f}'
                       f' {4*ks:.0f},{86*ks:.0f} Z" fill="{"#c8301f" if i%2 else "#d6a63f"}"'
                       f' stroke="{K}" stroke-width="{3*ks:.1f}"/>')
    # город на холмах: стены, башни, черепица, колоннада, маяк
    gor = ""
    gor += (f'<path d="M820,730 L920,470 L1500,420 L1920,520 L1920,730 Z"'
            f' fill="#b9a082" stroke="{K}" stroke-width="5"/>')
    for i in range(9):
        bx = 900 + i * 110
        bh = rnd.uniform(90, 180)
        gor += (f'<rect x="{bx:.0f}" y="{560-bh:.0f}" width="86" height="{bh+170:.0f}"'
                f' fill="#cbb492" stroke="{K}" stroke-width="4"/>')
        gor += (f'<path d="M{bx-10:.0f},{560-bh:.0f} l{53:.0f},{-44:.0f} l{53:.0f},{44:.0f} Z"'
                f' fill="#a8552f" stroke="{K}" stroke-width="3.6"/>')
        for k in range(3):
            gor += (f'<rect x="{bx+12+k*24:.0f}" y="{600-bh*.4:.0f}" width="15" height="34"'
                    f' rx="4" fill="#5e4430" opacity=".9"/>')
    for i in range(6):                 # колоннада
        cx = 1000 + i * 92
        gor += (f'<rect x="{cx:.0f}" y="600" width="30" height="150" fill="#e4d8bd"'
                f' stroke="{K}" stroke-width="3.4"/>'
                f'<rect x="{cx-8:.0f}" y="592" width="46" height="16" fill="#d8c7a4"'
                f' stroke="{K}" stroke-width="3"/>')
    gor += (f'<rect x="1000" y="576" width="520" height="22" fill="#e4d8bd"'
            f' stroke="{K}" stroke-width="3.6"/>')
    # крепостная стена с башнями и воротами
    gor += (f'<rect x="760" y="660" width="1160" height="150" fill="#c3ab8a"'
            f' stroke="{K}" stroke-width="5"/>')
    for i in range(16):
        gor += (f'<rect x="{770+i*72:.0f}" y="640" width="40" height="26"'
                f' fill="#c3ab8a" stroke="{K}" stroke-width="3"/>')
    for bx in (1080, 1600):
        gor += (f'<rect x="{bx:.0f}" y="560" width="130" height="250" fill="#cbb492"'
                f' stroke="{K}" stroke-width="5"/>'
                f'<path d="M{bx-16:.0f},560 l{73:.0f},{-56:.0f} l{73:.0f},{56:.0f} Z"'
                f' fill="#a8552f" stroke="{K}" stroke-width="4"/>')
    gor += (f'<path d="M1300,810 l0,-120 q60,{-80:.0f} 120,0 l0,120 Z" fill="#3f2d1c"'
            f' stroke="{K}" stroke-width="5"/>')
    # маяк с живым огнём
    gor += (f'<path d="M1810,660 l26,-230 h44 l26,230 Z" fill="#e4d8bd" stroke="{K}"'
            f' stroke-width="4.5"/>'
            f'<rect x="1828" y="392" width="64" height="44" rx="6" fill="#b9a082"'
            f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_DAL, gor)
    s += SL(Z_DAL, ogon(1860, 404, t, .9, .2, 5) + teplo(1860, 404, 160, 130, .5))
    s += SL(Z_SRED, f'<rect x="0" y="730" width="{W}" height="350" fill="#b08a52"/>'
            + f'<path d="M-40,1080 Q560,840 1120,790 L1920,760 L1920,1080 Z"'
              f' fill="#c89a62"/>')
    for i in range(30):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(800,1070):.0f}" rx="{rnd.uniform(10,34):.0f}"'
                        f' ry="{rnd.uniform(4,11):.0f}" fill="#a8824a" opacity=".6"/>')
    # кипарисы, виноградник, ослик
    for i, (kx, kb, kh) in enumerate(((120, 880, 420), (300, 840, 330), (1780, 900, 380))):
        kach = 2.0 * A.w(t, 3.6, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {kx:.0f} {kb:.0f})">'
                        f'<path d="M{kx-38:.0f},{kb:.0f} q{10:.0f},{-kh*.7:.0f} {38:.0f},{-kh:.0f}'
                        f' q{28:.0f},{kh*.3:.0f} {38:.0f},{kh:.0f} Z" fill="#3c5a3a"'
                        f' stroke="{K}" stroke-width="4"/></g>')
    for i in range(7):
        vx = 460 + i * 86
        s += SL(Z_SRED, f'<rect x="{vx:.0f}" y="860" width="12" height="90"'
                        f' fill="#6b4428" stroke="{K}" stroke-width="2.6"/>'
                        f'<path d="M{vx-28:.0f},864 q{34:.0f},{-22:.0f} {68:.0f},0"'
                        f' fill="none" stroke="#56763f" stroke-width="7"/>'
                        f'<circle cx="{vx+6:.0f}" cy="890" r="13" fill="#6b3a6a"'
                        f' stroke="{K}" stroke-width="2.4"/>')
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="980" rx="96" ry="56" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="1584" cy="936" r="38" fill="#8a8078" stroke="{K}"'
                    f' stroke-width="4"/>'
                    f'<path d="M1604,906 l10,-40 l16,38 Z" fill="#8a8078" stroke="{K}"'
                    f' stroke-width="3"/>'
                    f'<path d="M1430,1012 l-8,52 M1480,1024 l-4,46 M1540,1020 l6,46"'
                    f' stroke="#6f6256" stroke-width="11"/>'
                    f'<rect x="1452" y="930" width="110" height="46" rx="8"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="3.6"/>')
    # ЧЕЛОВЕК со спины: посох в правой руке, левая на суме
    px, py, ph_ = 860, 1056, 620
    idt = A.ease(A.seg(t, .4, 3.0))
    px += 120 * idt
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e4d8bd", kant="#8a7a52", ph=.3))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .30, 40, t, "#e4d8bd", "#8a7a52", .2, 4)
    r2, (e2x, e2y), _ = _ruka(px, py, ph_, -1, ph_ * .22, 56, t, "#e4d8bd", "#8a7a52", .6, 3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y-320:.0f} l{10:.0f},{py-e1y+300:.0f}"'
                    f' stroke="#7d5636" stroke-width="13" stroke-linecap="round"/>'
                    f'<path d="M{e1x-6:.0f},{e1y-320:.0f} q{22:.0f},{-30:.0f} {42:.0f},{-6:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="10"/>')
    s += SL(Z_SRED, f'<path d="M{e2x-50:.0f},{e2y:.0f} h92 l-10,86 h-72 Z" fill="#b9a37a"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e2x-50:.0f},{e2y+6:.0f} q{46:.0f},{-54:.0f} {92:.0f},0"'
                    f' fill="none" stroke="#8a7a52" stroke-width="6"/>')
    s += SL(Z_SRED, ten(px, py + 6, 130, 22, .4))
    for i in range(5):                 # чайки
        a = (t * .22 + i * .2) % 1.0
        cx_, cy_ = 300 + 1300 * a, 300 + 70 * math.sin(a * 6 + i)
        s += SL(Z_LETIT, f'<path d="M{cx_:.0f},{cy_:.0f} q{16:.0f},{-14:.0f} {32:.0f},0'
                         f' q{16:.0f},{-14:.0f} {32:.0f},0" fill="none" stroke="#f4f1e8"'
                         f' stroke-width="4" opacity=".9"/>')
    # ОБЖИТОЙ ЮЖНЫЙ НИЗ: лавки под навесами, амфоры, корзины смокв, козы,
    # придорожные камни — без них дорога к воротам шла по пустому склону
    for i, (lx, ly) in enumerate(((980, 880), (1240, 900), (1660, 920))):
        kch = 3.0 * A.w(t, 3.2, i * .4)
        s += SL(Z_SRED, f'<rect x="{lx:.0f}" y="{ly:.0f}" width="190" height="90" rx="6"'
                        f' fill="#b9a37a" stroke="{K}" stroke-width="4"/>'
                        f'<g transform="rotate({kch:.1f} {lx+95:.0f} {ly-70:.0f})">'
                        f'<path d="M{lx-20:.0f},{ly-60:.0f} q{105:.0f},{-34:.0f} {230:.0f},0'
                        f' l{-16:.0f},{26:.0f} q{-100:.0f},{-20:.0f} {-198:.0f},0 Z"'
                        f' fill="{"#c8301f" if i % 2 else "#3f6b7a"}" stroke="{K}"'
                        f' stroke-width="3.6"/></g>'
                        f'<rect x="{lx-14:.0f}" y="{ly-62:.0f}" width="12" height="62"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="2.6"/>'
                        f'<rect x="{lx+192:.0f}" y="{ly-62:.0f}" width="12" height="62"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="2.6"/>')
        for k in range(4):
            s += SL(Z_SRED, f'<circle cx="{lx+24+k*44:.0f}" cy="{ly+14:.0f}" r="17"'
                            f' fill="#6b3a6a" stroke="{K}" stroke-width="2.6"/>')
    for i, (ax_, ay_, as_) in enumerate(((690, 1000, 1.0), (760, 1016, .8), (1380, 1030, .9))):
        s += SL(Z_SRED, f'<path d="M{ax_-34*as_:.0f},{ay_-96*as_:.0f}'
                        f' q{-18*as_:.0f},{70*as_:.0f} {30*as_:.0f},{96*as_:.0f}'
                        f' q{48*as_:.0f},{-26*as_:.0f} {30*as_:.0f},{-96*as_:.0f} Z"'
                        f' fill="#a8743c" stroke="{K}" stroke-width="{4*as_:.1f}"/>'
                        f'<rect x="{ax_-16*as_:.0f}" y="{ay_-124*as_:.0f}"'
                        f' width="{32*as_:.0f}" height="{30*as_:.0f}" fill="#8a5a2e"'
                        f' stroke="{K}" stroke-width="{3*as_:.1f}"/>'
                        f'<path d="M{ax_-34*as_:.0f},{ay_-104*as_:.0f}'
                        f' q{-22*as_:.0f},{24*as_:.0f} {4*as_:.0f},{44*as_:.0f}"'
                        f' fill="none" stroke="#8a5a2e" stroke-width="{6*as_:.1f}"/>')
    for i, (kz, kzy) in enumerate(((430, 960), (560, 986))):
        hv = 8 * A.w(t, 2.2, i * .5)
        s += SL(Z_SRED, f'<ellipse cx="{kz:.0f}" cy="{kzy:.0f}" rx="62" ry="38"'
                        f' fill="#d8cbb0" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{kz+58:.0f}" cy="{kzy-30:.0f}" r="26" fill="#d8cbb0"'
                        f' stroke="{K}" stroke-width="3.4"/>'
                        f'<path d="M{kz+72:.0f},{kzy-48:.0f} q{18:.0f},{-26:.0f} {4:.0f},{-40:.0f}"'
                        f' fill="none" stroke="#8a7a52" stroke-width="7"/>'
                        f'<path d="M{kz-56:.0f},{kzy-10:.0f} q{-26+hv:.0f},{16:.0f}'
                        f' {-34:.0f},{-14:.0f}" fill="none" stroke="#d8cbb0"'
                        f' stroke-width="9"/>'
                        f'<path d="M{kz-30:.0f},{kzy+30:.0f} l-6,40 M{kz+20:.0f},'
                        f'{kzy+34:.0f} l4,38" stroke="#b9a37a" stroke-width="9"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<ellipse cx="{200+i*190:.0f}" cy="{1040+(i%3)*14:.0f}"'
                        f' rx="{26+(i%4)*9:.0f}" ry="{12+(i%3)*5:.0f}" fill="#8a7a62"'
                        f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_PERED, f'<path d="M-20,1080 q220,{-120:.0f} 420,{-40:.0f} l0,180 l-440,0 Z"'
                     f' fill="#7d5636" opacity=".9"/>')
    s += ramka_pp("oba", "#120d08", .45)
    s += vinetka(.38)
    return s


def ploschad_stolicy(t):
    """Мощёная площадь с фонтаном и колоннадой: на возвышении со спины и
    вполоборота стоит человек в длинной мантии, обе руки сложены на посохе.
    Горожане снимают шапки, мальчик выпускает голубя."""
    rnd = random.Random(1909)
    s = (f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>')
    s += nebo("den", t, False, 53)
    s += oblaka(t, 110, 5, 47, .30, "#ffe9c8")
    # колоннада и портик в глубине
    kol = (f'<rect x="0" y="250" width="{W}" height="300" fill="#cbb492" opacity=".65"/>')
    for i in range(10):
        cx = 60 + i * 200
        kol += (f'<rect x="{cx:.0f}" y="270" width="54" height="300" fill="#e4d8bd"'
                f' stroke="{K}" stroke-width="4.5"/>')
        for k in range(6):
            kol += (f'<path d="M{cx+8+k*8:.0f},274 l0,292" stroke="#cdbc9c"'
                    f' stroke-width="3" opacity=".8"/>')
        kol += (f'<rect x="{cx-12:.0f}" y="252" width="78" height="24" fill="#d8c7a4"'
                f' stroke="{K}" stroke-width="4"/>'
                f'<rect x="{cx-8:.0f}" y="566" width="70" height="20" fill="#d8c7a4"'
                f' stroke="{K}" stroke-width="3.6"/>')
    kol += (f'<rect x="-20" y="214" width="{W+40}" height="40" fill="#e4d8bd"'
            f' stroke="{K}" stroke-width="5"/>')
    s += SL(Z_DAL, kol)
    # мозаичная мостовая
    most = (f'<rect x="0" y="586" width="{W}" height="{H-586}" fill="#b9a082"/>')
    for i in range(26):
        for k in range(9):
            px = -40 + i * 78 + (39 if k % 2 else 0)
            py = 600 + k * 56
            most += (f'<rect x="{px:.0f}" y="{py:.0f}" width="70" height="48" rx="6"'
                     f' fill="{"#c7b391" if (i+k) % 3 else "#ab9573"}" opacity=".9"/>')
    s += SL(Z_SRED, most)
    # фонтан с играющей струёй
    s += SL(Z_SRED, f'<ellipse cx="520" cy="880" rx="300" ry="100" fill="#8aa8b4"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<ellipse cx="520" cy="866" rx="262" ry="80" fill="#2f6b78"/>'
                    f'<ellipse cx="520" cy="860" rx="200" ry="56" fill="#4a8a94"'
                    f' opacity=".7"/>'
                    f'<rect x="494" y="700" width="52" height="166" fill="#d8c7a4"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="520" cy="700" rx="110" ry="30" fill="#e4d8bd"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(9):
        a = (t * .8 + i / 9.0) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{520+(i-4)*34*a:.0f}" cy="{668-120*a+170*a*a:.0f}"'
                        f' rx="{7+6*a:.0f}" ry="{10+8*a:.0f}" fill="#cfe4f5"'
                        f' opacity="{.85-.5*a:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M470,676 q50,{-70:.0f} 100,0" fill="none" stroke="#9fd0e4"'
                    f' stroke-width="9" opacity=".75"/>')
    # возвышение и ГЛАВНЫЙ: со спины и вполоборота, обе руки на посохе
    s += SL(Z_SRED, f'<rect x="1140" y="880" width="520" height="52" rx="6"'
                    f' fill="#d8c7a4" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1180" y="932" width="440" height="46" rx="6"'
                    f' fill="#c7b391" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="1220" y="978" width="360" height="44" rx="6"'
                    f' fill="#b9a082" stroke="{K}" stroke-width="4"/>')
    px, py, ph_ = 1400, 880, 660
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#8a7a52",
                           ph=.2, boroda=True, profil=True))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .26, 44, t, "#e8e2d6", "#8a7a52", .2, 3)
    r2, (e2x, e2y), _ = _ruka(px, py, ph_, -1, ph_ * .24, 50, t, "#e8e2d6", "#8a7a52", .5, 3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{(e1x+e2x)/2:.0f},{e1y-210:.0f} l{6:.0f},{py-e1y+190:.0f}"'
                    f' stroke="#7d5636" stroke-width="14" stroke-linecap="round"/>'
                    f'<path d="M{(e1x+e2x)/2-6:.0f},{e1y-210:.0f} q{24:.0f},{-34:.0f}'
                    f' {46:.0f},{-6:.0f}" fill="none" stroke="#6b4428" stroke-width="11"/>')
    # мантия длинная, со складками
    s += SL(Z_SRED, f'<path d="M{px-130:.0f},{py-ph_*.60:.0f} q{130:.0f},{-40:.0f}'
                    f' {260:.0f},0 l{44:.0f},{ph_*.58:.0f} q{-174:.0f},{40:.0f}'
                    f' {-348:.0f},0 Z" fill="#efe6d2" opacity=".55" stroke="#c9bfa6"'
                    f' stroke-width="4"/>')
    s += SL(Z_SRED, ten(px, py + 8, 150, 24, .4))
    # ГОРОЖАНЕ снимают шапки
    for i, (hx, hy, hh, col) in enumerate(((760, 1046, 470, "#a8743c"),
                                           (960, 1056, 430, "#6b3a6a"),
                                           (1760, 1040, 450, "#3f6b7a"))):
        snyal = A.ease(A.seg(t, .4 + i * .2, .8))
        s += SL(Z_SRED, figura(hx, hy, hh, t, col=col, kant="#ffd9a8", ph=i * .3))
        rk, (ex, ey), _ = _ruka(hx, hy, hh, 1, hh * .26, 60 - 70 * snyal, t,
                                col, "#ffd9a8", i * .2, 4)
        s += SL(Z_SRED, rk + f'<ellipse cx="{ex+10:.0f}" cy="{ey+14:.0f}" rx="34"'
                             f' ry="20" fill="#8a6a4a" stroke="{K}" stroke-width="3.6"/>')
        s += SL(Z_SRED, ten(hx, hy + 6, 92, 16, .35))
    # торговец с корзиной смокв и женщина с кувшином
    tx, ty, th = 300, 1066, 500
    s += SL(Z_SRED, figura(tx, ty, th, t, col="#8a5a2e", kant="#ffd9a8", ph=.7))
    r3, (e3x, e3y), _ = _ruka(tx, ty, th, 1, th * .24, 62, t, "#8a5a2e", "#ffd9a8", .4, 4)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x-40:.0f},{e3y+8:.0f} q{40:.0f},{16:.0f} {80:.0f},0'
                         f' l{-10:.0f},{54:.0f} h{-60:.0f} Z" fill="#b08a52" stroke="{K}"'
                         f' stroke-width="3.6"/>')
    for k in range(5):
        s += SL(Z_SRED, f'<circle cx="{e3x-28+k*14:.0f}" cy="{e3y+18:.0f}" r="11"'
                        f' fill="#6b3a6a" stroke="{K}" stroke-width="2.4"/>')
    zx, zy, zh = 1900, 1060, 520
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#c8301f", kant="#ffd9a8",
                           platok=True, ph=.9))
    s += SL(Z_SRED, f'<path d="M{zx-120:.0f},{zy-zh*.70:.0f} q{-22:.0f},{44:.0f}'
                    f' {12:.0f},{70:.0f} q{40:.0f},{14:.0f} {54:.0f},{-20:.0f}'
                    f' q{10:.0f},{-44:.0f} {-20:.0f},{-56:.0f} Z" fill="#a8743c"'
                    f' stroke="{K}" stroke-width="4"/>')
    # МАЛЬЧИК с голубем: голубь взлетает
    mx, my, mh = 1080, 1062, 330
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#e4d8bd", kant="#8a7a52", ph=.5))
    r4, (e4x, e4y), _ = _ruka(mx, my, mh, 1, mh * .30, -24, t, "#e4d8bd", "#8a7a52", .3, 6)
    s += SL(Z_SRED, r4)
    vzl = A.ease(A.seg(t, 1.0, 1.4))
    gx, gy = e4x + 10 + 120 * vzl, e4y - 10 - 300 * vzl
    kr = 20 * A.w(t, .35, .0)
    s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="30" ry="20" fill="#e8eef6"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<circle cx="{gx+24:.0f}" cy="{gy-14:.0f}" r="13" fill="#e8eef6"'
                    f' stroke="{K}" stroke-width="2.6"/>'
                    f'<path d="M{gx+36:.0f},{gy-16:.0f} l14,4 l-14,5 Z" fill="{ORA}"/>'
                    f'<path d="M{gx-6:.0f},{gy-8:.0f} q{20:.0f},{-30-kr:.0f} {50:.0f},{-16:.0f}"'
                    f' fill="none" stroke="#cfd6de" stroke-width="12"/>'
                    f'<path d="M{gx-6:.0f},{gy+2:.0f} q{18:.0f},{26+kr:.0f} {46:.0f},{14:.0f}"'
                    f' fill="none" stroke="#cfd6de" stroke-width="11"/>')
    # навесы лавок и светильник на столбе — живой огонёк площади
    for i, (lx, ly) in enumerate(((60, 700), (1700, 690))):
        kch = 3.4 * A.w(t, 3.0, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {lx+100:.0f} {ly:.0f})">'
                        f'<path d="M{lx:.0f},{ly:.0f} q{100:.0f},{-40:.0f} {200:.0f},0'
                        f' l{-14:.0f},{30:.0f} q{-86:.0f},{-26:.0f} {-172:.0f},0 Z"'
                        f' fill="{"#c8301f" if i else "#3f6b7a"}" stroke="{K}"'
                        f' stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<rect x="1660" y="560" width="22" height="330" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, lampa(1671, 548, t, 1.3, False) + teplo(1671, 540, 190, 160, .45))
    s += SL(Z_PERED, f'<rect x="-10" y="250" width="70" height="830" fill="#1d1611"'
                     f' opacity=".85"/>')
    s += ramka_pp("oba", "#120d08", .45)
    s += vinetka(.40)
    return s


def dva_imeni_na_svitke(t):
    """Стол в каменной палате: развёрнутый свиток с двумя строчками-завитками,
    чернильница, перо, светильник. Старец в кресле указывает на свиток,
    старейшина кладёт камешек-жребий на верхнюю строчку — она загорается."""
    rnd = random.Random(1910)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    s += SL(Z_DAL, kladka(0, 0, W, 760, 86, "url(#kamen)"))
    s += SL(Z_DAL, svody(t, "#4b443b", 3))
    # окно с видом на море
    s += SL(Z_DAL, f'<path d="M1480,180 q120,{-150:.0f} 240,0 l0,330 l-240,0 Z"'
                   f' fill="#4a8a94" stroke="{K}" stroke-width="6"/>'
                   f'<path d="M1480,380 q120,{20:.0f} 240,{-10:.0f} l0,140 l-240,0 Z"'
                   f' fill="#2f6b78"/>'
                   f'<path d="M1480,300 q120,{-130:.0f} 240,0" fill="none" stroke="#e4d8bd"'
                   f' stroke-width="7" opacity=".5"/>'
                   f'<rect x="1590" y="40" width="18" height="470" fill="#6b4428"'
                   f' opacity=".9"/>')
    s += SL(Z_DAL, f'<path d="M1180,0 q40,{280:.0f} -10,{560:.0f} l-150,0 q50,{-280:.0f}'
                   f' 10,{-560:.0f} Z" fill="#8a2f22" stroke="{K}" stroke-width="5"/>')
    for i in range(5):
        s += SL(Z_DAL, f'<path d="M{1040+i*26:.0f},20 q{30:.0f},{280:.0f} {-6:.0f},{540:.0f}"'
                       f' fill="none" stroke="#6b2419" stroke-width="7" opacity=".7"/>')
    # СТОЛ во весь кадр
    s += SL(Z_SRED, f'<rect x="60" y="700" width="1800" height="60" rx="10"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="60" y="760" width="1800" height="26" fill="#54351f"'
                    f' opacity=".9"/>'
                    f'<rect x="200" y="786" width="54" height="294" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1640" y="786" width="54" height="294" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="4"/>')
    # СВИТОК с двумя строчками-завитками
    sx, sy, sw, sh_ = 560, 560, 820, 150
    svit = (f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="{sh_:.0f}"'
            f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>')
    for i in (0, 1):
        rx_ = sx - 40 if i == 0 else sx + sw
        svit += (f'<rect x="{rx_:.0f}" y="{sy-18:.0f}" width="40" height="{sh_+36:.0f}"'
                 f' rx="20" fill="#c9a05a" stroke="{K}" stroke-width="4.5"/>')
    gor_ = A.ease(A.seg(t, 1.3, 1.0))
    for i, yy in enumerate((sy + 46, sy + 104)):
        col = "#8a2f22" if i == 0 else "#6f6354"
        svit += (f'<path d="M{sx+70:.0f},{yy:.0f} q{60:.0f},{-14:.0f} {120:.0f},0'
                 f' q{60:.0f},{14:.0f} {120:.0f},0 q{60:.0f},{-14:.0f} {120:.0f},0'
                 f' q{60:.0f},{14:.0f} {120:.0f},0" fill="none" stroke="{col}"'
                 f' stroke-width="7" opacity=".9"/>')
    svit += (f'<rect x="{sx+54:.0f}" y="{sy+22:.0f}" width="{sw-110:.0f}" height="48"'
             f' rx="10" fill="#ffd98a" opacity="{.55*gor_:.2f}"/>')
    svit += (f'<rect x="{sx+54:.0f}" y="{sy+22:.0f}" width="{sw-110:.0f}" height="48"'
             f' rx="10" fill="none" stroke="#ffe9ac" stroke-width="5"'
             f' opacity="{.9*gor_:.2f}"/>')
    s += SL(Z_SRED, svit)
    # камешек-жребий ложится на верхнюю строчку
    kl = A.out(A.seg(t, .7, .9))
    s += SL(Z_SRED, f'<ellipse cx="{sx+300:.0f}" cy="{sy+46-180*(1-kl):.0f}" rx="26"'
                    f' ry="18" fill="{KAMEN}" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{sx+282:.0f},{sy+38-180*(1-kl):.0f} q{18:.0f},{-10:.0f}'
                    f' {36:.0f},{4:.0f}" fill="none" stroke="#9aa3a8" stroke-width="5"/>')
    # чернильница, перо, светильник
    s += SL(Z_SRED, f'<path d="M1430,700 h110 l-14,-66 h-82 Z" fill="#3f3a33"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="1485" cy="634" rx="42" ry="13" fill="#17120d"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1500,630 l80,-150" stroke="#e8e2d6" stroke-width="9"'
                    f' fill="none"/>'
                    f'<path d="M1572,490 q{26:.0f},{-40:.0f} {40:.0f},{-8:.0f}'
                    f' q{-18:.0f},{26:.0f} {-34:.0f},{30:.0f} Z" fill="#f4f1e8"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M300,700 h140 l-20,-40 h-100 Z" fill="#b5803a"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M330,660 q40,{-30:.0f} 80,0 l-10,-26 h-60 Z"'
                    f' fill="#c08a3a" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, ogon(370, 610, t, 1.15, .1, 6) + teplo(370, 600, 320, 260, .5))
    s += SL(Z_SRED, f'<path d="M1720,760 q-40,{-120:.0f} 10,{-190:.0f} q70,{40:.0f}'
                    f' {50:.0f},{190:.0f} Z" fill="#a8743c" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    # СТАРЕЦ в кресле: слабой правой рукой указывает на свиток
    kx, ky, kh = 1760, 1010, 560
    s += SL(Z_SRED, f'<rect x="{kx-150:.0f}" y="{ky-470:.0f}" width="300" height="470"'
                    f' rx="16" fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="{kx-130:.0f}" y="{ky-440:.0f}" width="260" height="300"'
                    f' rx="12" fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(kx, ky, kh, t, col="#e8e2d6", kant="#8a7a52",
                           boroda=True, ph=.8))
    uk = A.ease(A.seg(t, .3, 1.0))
    r1, (e1x, e1y), _ = _ruka(kx, ky, kh, -1, kh * .34, 16 - 30 * uk, t,
                              "#e8e2d6", "#8a7a52", .2, 3)
    s += SL(Z_SRED, r1)
    # ДВОЕ СТАРЕЙШИН у стола: один держит свиток обеими руками, второй — жребий
    for i, (ox, oy, oh, col) in enumerate(((420, 1066, 620, "#6f6354"),
                                           (980, 1070, 640, "#8a7a52"))):
        s += SL(Z_SRED, figura(ox, oy, oh, t, col=col, kant="#ffd9a8",
                               boroda=(i == 0), ph=.3 + i * .4))
        rk1, (ax_, ay_), _ = _ruka(ox, oy, oh, 1, oh * .26, -14 + i * 8, t,
                                   col, "#ffd9a8", .2 + i * .2, 4)
        rk2, (bx_, by_), _ = _ruka(ox, oy, oh, -1, oh * .24, -10 + i * 6, t,
                                   col, "#ffd9a8", .6 + i * .2, 4)
        s += SL(Z_SRED, rk1 + rk2)
    s += SL(Z_SRED, ten(420, 1072, 120, 20, .4) + ten(980, 1076, 124, 20, .4))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="90" height="{H}" fill="#120d08"'
                     f' opacity=".9"/>')
    s += ramka_pp("oba", "#120d08", .5)
    s += vinetka(.44)
    return s


def imperator_vozvraschaetsya(t):
    """Городские ворота: в них въезжает колесница. Император в пурпурном
    плаще резко указывает вперёд, возница с кнутом. Навстречу из города
    со спины выходит Павел с посохом и сумой, стражники провожают копьями."""
    rnd = random.Random(1911)
    s = (f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>')
    s += nebo("den", t, False, 59)
    s += oblaka(t, 120, 5, 53, .32, "#ffe9c8")
    # СТЕНА С ВОРОТАМИ во весь кадр
    st_ = (f'<rect x="0" y="200" width="{W}" height="640" fill="#c3ab8a"'
           f' stroke="{K}" stroke-width="6"/>')
    st_ += kladka(0, 200, W, 640, 88, "url(#kamen)")
    for i in range(20):
        st_ += (f'<rect x="{10+i*96:.0f}" y="168" width="54" height="36"'
                f' fill="#c3ab8a" stroke="{K}" stroke-width="3.4"/>')
    for bx in (120, 1560):
        st_ += (f'<rect x="{bx:.0f}" y="90" width="230" height="750" fill="#cbb492"'
                f' stroke="{K}" stroke-width="6"/>'
                f'<path d="M{bx-28:.0f},90 l{129:.0f},{-74:.0f} l{129:.0f},{74:.0f} Z"'
                f' fill="#a8552f" stroke="{K}" stroke-width="5"/>')
        for k in range(3):
            st_ += (f'<rect x="{bx+36+k*62:.0f}" y="280" width="34" height="72" rx="16"'
                    f' fill="#4a3526" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_DAL, st_)
    # проём ворот: тёмная арка, за ней город
    s += SL(Z_DAL, f'<path d="M700,840 l0,-330 q260,{-260:.0f} 520,0 l0,330 Z"'
                   f' fill="#3f2d1c" stroke="{K}" stroke-width="7"/>'
                   f'<path d="M740,840 l0,-310 q220,{-230:.0f} 440,0 l0,310 Z"'
                   f' fill="#6b5a44" opacity=".8"/>')
    for i in range(6):
        s += SL(Z_DAL, f'<rect x="{760+i*68:.0f}" y="{560+(i%2)*30:.0f}" width="52"'
                       f' height="{280-(i%2)*30:.0f}" fill="#8a7a62" opacity=".55"/>')
    # знамёна БЕЗ СИМВОЛОВ по сторонам ворот
    for i, zx in enumerate((640, 1270)):
        kch = 5 * A.w(t, 2.6, i * .4)
        s += SL(Z_SRED, f'<rect x="{zx:.0f}" y="300" width="14" height="360"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{zx+14:.0f},318 q{60+kch:.0f},{30:.0f} {110:.0f},{-6:.0f}'
                        f' l0,{130:.0f} q{-50:.0f},{24:.0f} {-110:.0f},{-6:.0f} Z"'
                        f' fill="{"#8a2f22" if i else "#3f4a7a"}" stroke="{K}"'
                        f' stroke-width="4"/>')
    # дорога и пыль
    s += SL(Z_SRED, f'<rect x="0" y="840" width="{W}" height="240" fill="#b08a52"/>'
            + f'<path d="M-40,1080 Q600,900 1180,860 L1920,846 L1920,1080 Z"'
              f' fill="#c89a62"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(870,1070):.0f}" rx="{rnd.uniform(12,40):.0f}"'
                        f' ry="{rnd.uniform(5,13):.0f}" fill="#a8824a" opacity=".55"/>')
    vezd = A.ease(A.seg(t, .3, 3.4))
    for i in range(7):
        d = ((t * .6 + i / 7.0) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{1500-400*vezd+90*d:.0f}" cy="{1000-60*d:.0f}"'
                        f' rx="{30+50*d:.0f}" ry="{16+26*d:.0f}" fill="#d8c7a4"'
                        f' opacity="{(1-d)*.45:.2f}"/>')
    # КОЛЕСНИЦА въезжает
    kx = 1520 - 420 * vezd
    kol = (f'<path d="M{kx-110:.0f},900 h220 q26,0 26,{-80:.0f} l{-10:.0f},{-70:.0f}'
           f' h{-252:.0f} Z" fill="#a8743c" stroke="{K}" stroke-width="5"/>')
    kol += (f'<path d="M{kx-110:.0f},760 h236" stroke="{ZOL}" stroke-width="10"/>')
    ug = (t * 260) % 360
    for wx in (kx - 90, kx + 90):
        kol += (f'<g transform="rotate({ug:.0f} {wx:.0f} 906)">'
                f'<circle cx="{wx:.0f}" cy="906" r="86" fill="none" stroke="#6b4428"'
                f' stroke-width="15"/>')
        for k in range(8):
            a = k * .785
            kol += (f'<line x1="{wx:.0f}" y1="906" x2="{wx+80*math.cos(a):.0f}"'
                    f' y2="{906+80*math.sin(a):.0f}" stroke="#7d5636" stroke-width="7"/>')
        kol += '</g>'
    kol += (f'<path d="M{kx+130:.0f},840 q{120:.0f},{-20:.0f} {210:.0f},{10:.0f}"'
            f' fill="none" stroke="#6b4428" stroke-width="9"/>')
    s += SL(Z_SRED, kol)
    # ИМПЕРАТОР: левая держит поводья, правая резко указывает вперёд
    ix, iy, ih = kx - 10, 820, 560
    ukaz = A.out(A.seg(t, .9, .7))
    s += SL(Z_SRED, figura(ix, iy, ih, t, col="#6b2a5a", kant="#ffd98a",
                           ph=.2, boroda=True))
    r1, (e1x, e1y), _ = _ruka(ix, iy, ih, -1, ih * .34, -6 - 24 * ukaz, t,
                              "#6b2a5a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ix, iy, ih, 1, ih * .26, 34, t, "#6b2a5a", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e2x:.0f},{e2y:.0f} q{90:.0f},{30:.0f} {170:.0f},{6:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="6"/>')
    # плащ отлетает назад
    pl = 40 + 26 * A.w(t, 1.4, .1)
    s += SL(Z_SRED, f'<path d="M{ix+40:.0f},{iy-ih*.64:.0f} q{-60-pl:.0f},{120:.0f}'
                    f' {-160-pl:.0f},{210:.0f} q{70:.0f},{20:.0f} {150:.0f},{-40:.0f} Z"'
                    f' fill="#7d2f66" stroke="{K}" stroke-width="4.5"/>')
    # венец
    s += SL(Z_SRED, f'<path d="M{ix-44:.0f},{iy-ih*.86:.0f} h88 l-8,-26 h-72 Z"'
                    f' fill="{ZOL}" stroke="{K}" stroke-width="3.6"/>')
    # ВОЗНИЦА с кнутом
    vx, vy, vh = kx + 86, 824, 500
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#8a7a52", kant="#ffd9a8", ph=.7))
    r3, (e3x, e3y), _ = _ruka(vx, vy, vh, 1, vh * .28, -28, t, "#8a7a52", "#ffd9a8", .4, 7)
    knut = 20 * A.w(t, .9, .2)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x:.0f},{e3y:.0f} q{70:.0f},{-60-knut:.0f}'
                         f' {150:.0f},{-20+knut:.0f}" fill="none" stroke="#5e4a2a"'
                         f' stroke-width="5"/>')
    # ПАВЕЛ со спины выходит из ворот, стражники провожают копьями
    px, py, ph_ = 860 - 60 * A.ease(A.seg(t, 1.4, 2.0)), 1000, 600
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#8a7a52", ph=.5))
    r4, (e4x, e4y), _ = _ruka(px, py, ph_, 1, ph_ * .28, 44, t, "#e8e2d6", "#8a7a52", .3, 3)
    r5, (e5x, e5y), _ = _ruka(px, py, ph_, -1, ph_ * .22, 56, t, "#e8e2d6", "#8a7a52", .8, 3)
    s += SL(Z_SRED, r4 + r5)
    s += SL(Z_SRED, f'<path d="M{e4x:.0f},{e4y-300:.0f} l{8:.0f},{py-e4y+280:.0f}"'
                    f' stroke="#7d5636" stroke-width="12" stroke-linecap="round"/>'
                    f'<path d="M{e5x-44:.0f},{e5y:.0f} h86 l-10,78 h-66 Z" fill="#b9a37a"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i, sx_ in enumerate((1010, 1150)):
        s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="980" rx="46" ry="110"'
                        f' fill="#4a4038" opacity=".92" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{sx_:.0f}" cy="844" r="38" fill="#4a4038"'
                        f' stroke="{K}" stroke-width="4"/>'
                        f'<path d="M{sx_+40:.0f},1070 l{-14:.0f},{-330:.0f}"'
                        f' stroke="#6b4428" stroke-width="8"/>'
                        f'<path d="M{sx_+24:.0f},740 l{8:.0f},{-44:.0f} l{10:.0f},{44:.0f} Z"'
                        f' fill="#c9ccd1" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, ten(px, py + 6, 130, 22, .4))
    s += SL(Z_SRED, lampa(300, 560, t, 1.2, False) + teplo(300, 560, 200, 170, .40))
    s += SL(Z_PERED, f'<path d="M-20,1080 q180,{-90:.0f} 360,{-30:.0f} l0,160 l-380,0 Z"'
                     f' fill="#7d5636" opacity=".9"/>')
    s += ramka_pp("oba", "#120d08", .45)
    s += vinetka(.40)
    return s


def vorota_otkryvayutsya_i_zakryvayuts(t):
    """Те же ворота во весь кадр: Павел со спины входит — створки
    распахиваются, выходит — захлопываются, и снова. Над воротами растёт
    рисованный счётчик, ослик у придорожного камня провожает его взглядом."""
    rnd = random.Random(1912)
    s = (f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>')
    s += nebo("den", t, False, 61)
    s += oblaka(t, 130, 4, 59, .30, "#ffe9c8")
    st_ = (f'<rect x="0" y="120" width="{W}" height="740" fill="#c3ab8a"'
           f' stroke="{K}" stroke-width="6"/>')
    st_ += kladka(0, 120, W, 740, 92, "url(#kamen)")
    for i in range(20):
        st_ += (f'<rect x="{6+i*98:.0f}" y="86" width="56" height="38"'
                f' fill="#c3ab8a" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_DAL, st_)
    s += SL(Z_DAL, f'<path d="M620,860 l0,-360 q340,{-300:.0f} 680,0 l0,360 Z"'
                   f' fill="#2b2016" stroke="{K}" stroke-width="8"/>')
    # что видно в проёме: улица города с огоньком
    s += SL(Z_DAL, f'<path d="M700,860 l0,-310 q280,{-250:.0f} 560,0 l0,310 Z"'
                   f' fill="#6b5a44" opacity=".85"/>')
    for i in range(5):
        s += SL(Z_DAL, f'<rect x="{720+i*110:.0f}" y="{600+(i%2)*34:.0f}" width="80"'
                       f' height="{260-(i%2)*34:.0f}" fill="#8a7a62" opacity=".6"/>')
    s += SL(Z_DAL, svecha(960, 700, t, .2, 1.6, 110) + teplo(960, 660, 220, 190, .40))
    # СТВОРКИ: распахиваются и захлопываются
    faza = (t * .75) % 1.0
    otkr = A.ease(min(1.0, faza * 2.6)) - A.ease(max(.0, faza * 2.6 - 1.5))
    for i in (-1, 1):
        ug = i * 52 * otkr
        cx_ = 960 + i * 340
        stv = (f'<g transform="rotate({ug:.1f} {cx_:.0f} 860)">'
               f'<rect x="{cx_-(340 if i>0 else 0):.0f}" y="500" width="340" height="360"'
               f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>')
        for k in range(5):
            stv += (f'<rect x="{cx_-(330 if i>0 else -10)+k*66:.0f}" y="510" width="52"'
                    f' height="340" rx="5" fill="{DOSKA}" opacity=".9" stroke="{K}"'
                    f' stroke-width="2.6"/>')
        stv += (f'<rect x="{cx_-(330 if i>0 else -10):.0f}" y="640" width="320"'
                f' height="26" fill="{ZHELEZ}" opacity=".9"/>')
        stv += (f'<circle cx="{cx_-i*60:.0f}" cy="700" r="24" fill="none"'
                f' stroke="{CHUGUN}" stroke-width="10"/></g>')
        s += SL(Z_SRED, stv)
    # ПАВЕЛ входит и выходит: по фазе
    hod = math.sin(faza * 6.283)
    px, py, ph_ = 960 + 260 * hod, 1020, 620
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#8a7a52", ph=.3))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .28, 42, t, "#e8e2d6", "#8a7a52", .2, 4)
    s += SL(Z_SRED, r1 + f'<path d="M{e1x:.0f},{e1y-300:.0f} l{8:.0f},{py-e1y+280:.0f}"'
                         f' stroke="#7d5636" stroke-width="13" stroke-linecap="round"/>')
    s += SL(Z_SRED, ten(px, py + 6, 130, 22, .4))
    # СЧЁТЧИК над воротами: рисованные палочки-засечки, их всё больше
    n = 1 + int((t * .9) % 4)
    for i in range(n):
        s += SL(Z_SRED, f'<rect x="{830+i*70:.0f}" y="300" width="18" height="86"'
                        f' rx="6" fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    # стражники-силуэты на стене
    for i, sx_ in enumerate((420, 1500)):
        s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="150" rx="40" ry="86"'
                        f' fill="#4a4038" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{sx_:.0f}" cy="48" r="32" fill="#4a4038"'
                        f' stroke="{K}" stroke-width="3.6"/>'
                        f'<path d="M{sx_+36:.0f},220 l{-10:.0f},{-260:.0f}"'
                        f' stroke="#6b4428" stroke-width="8"/>')
    # дорога, оливы, придорожный камень, ослик
    s += SL(Z_SRED, f'<rect x="0" y="860" width="{W}" height="220" fill="#b08a52"/>'
            + f'<path d="M-40,1080 Q620,920 1200,878 L1920,866 L1920,1080 Z"'
              f' fill="#c89a62"/>')
    for i in range(18):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(890,1070):.0f}" rx="{rnd.uniform(14,42):.0f}"'
                        f' ry="{rnd.uniform(5,14):.0f}" fill="#a8824a" opacity=".55"/>')
    for i, (ox, ob, oh) in enumerate(((120, 1010, 300), (1830, 1030, 340))):
        kch = 2.4 * A.w(t, 3.4, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {ox:.0f} {ob:.0f})">'
                        f'<path d="M{ox-16:.0f},{ob:.0f} q{6:.0f},{-oh*.6:.0f}'
                        f' {18:.0f},{-oh:.0f} l{20:.0f},0 q{10:.0f},{oh*.6:.0f}'
                        f' {14:.0f},{oh:.0f} Z" fill="#6b5230" stroke="{K}"'
                        f' stroke-width="4"/>'
                        f'<ellipse cx="{ox+14:.0f}" cy="{ob-oh-30:.0f}" rx="{oh*.38:.0f}"'
                        f' ry="{oh*.26:.0f}" fill="#56763f" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{ox-50:.0f}" cy="{ob-oh+40:.0f}" rx="{oh*.22:.0f}"'
                        f' ry="{oh*.16:.0f}" fill="#49693a" stroke="{K}" stroke-width="3.4"/></g>')
    s += SL(Z_SRED, f'<path d="M330,1066 q30,{-110:.0f} 130,{-96:.0f} q40,{60:.0f}'
                    f' {26:.0f},{96:.0f} Z" fill="#8a8078" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M360,1020 q50,{-24:.0f} 96,{-6:.0f}" fill="none"'
                    f' stroke="#6f6256" stroke-width="7"/>')
    glyad = 10 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<ellipse cx="1620" cy="990" rx="104" ry="58" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="{1716+glyad:.0f}" cy="936" r="40" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{1738+glyad:.0f},904 l10,-44 l18,40 Z" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="3.2"/>'
                    f'<circle cx="{1728+glyad:.0f}" cy="930" r="5" fill="{K}"/>'
                    f'<path d="M1540,1030 l-8,46 M1596,1042 l-4,40 M1664,1038 l6,42"'
                    f' stroke="#6f6256" stroke-width="11"/>'
                    f'<rect x="1560" y="930" width="120" height="50" rx="9"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="3.6"/>')
    s += ramka_pp("oba", "#120d08", .45)
    s += vinetka(.40)
    return s


def gornaya_doroga_v_ssylku(t):
    """Каменистая тропа над ущельем: в проёме старого каменного моста —
    настоящие заснеженные горы. Павел со спины идёт вверх, опираясь на
    посох; за ним стражник с копьём и щитом, выше кружит орёл."""
    rnd = random.Random(1913)
    s = (f'<rect width="{W}" height="{H}" fill="#6b7a88"/>')
    s += nebo("den", t, False, 67)
    s += oblaka(t, 150, 6, 61, .40)
    # дальние скалы
    for i, (sx, sb, sh_, col) in enumerate(((-100, 640, 520, "#6f7a84"),
                                            (420, 600, 460, "#5e6a74"),
                                            (1500, 660, 540, "#6f7a84"))):
        s += SL(Z_DAL, f'<path d="M{sx:.0f},{sb:.0f} l{sh_*.5:.0f},{-sh_:.0f}'
                       f' l{sh_*.35:.0f},{sh_*.42:.0f} l{sh_*.30:.0f},{-sh_*.28:.0f}'
                       f' l{sh_*.55:.0f},{sh_*.86:.0f} Z" fill="{col}" stroke="{K}"'
                       f' stroke-width="5"/>')
        s += SL(Z_DAL, f'<path d="M{sx+sh_*.5:.0f},{sb-sh_:.0f} l{sh_*.18:.0f},{sh_*.22:.0f}'
                       f' l{-sh_*.36:.0f},0 Z" fill="url(#sneg)" opacity=".9"/>')
    # КАМЕННАЯ АРКА МОСТА: сначала вид, потом метка, потом кладка поверх
    ax, ay, aw, ah = 120, 300, 780, 320
    put = kontur_proema(ax, ay, aw, ah, "arka")
    arka = (f'<path d="{put}" fill="#8aa0b4"/>')
    arka += (f'<path d="{put}" fill="#cfe4f5" opacity=".45"/>')
    arka += mesto_stoka(ax, ay, aw, ah, "arka")
    arka += (f'<path d="{put}" fill="none" stroke="#5e564c" stroke-width="26"/>')
    s += SL(Z_SRED, arka)
    most = (f'<path d="M{ax-180:.0f},{ay+ah:.0f} l0,-120 q{aw*.5+180:.0f},{-380:.0f}'
            f' {aw+360:.0f},0 l0,120 l-120,0 q{-aw*.4:.0f},{-280:.0f} {-aw-120:.0f},0 Z"'
            f' fill="#7d7265" stroke="{K}" stroke-width="6"/>')
    most += kladka(ax - 180, ay - 90, aw + 360, 150, 54, "url(#kamen)")
    most += (f'<rect x="{ax-200:.0f}" y="{ay-120:.0f}" width="{aw+400:.0f}" height="40"'
             f' rx="6" fill="#8a8078" stroke="{K}" stroke-width="5"/>')
    most += (f'<path d="M{ax-200:.0f},{ay-120:.0f} q{(aw+400)*.5:.0f},{-18:.0f}'
             f' {aw+400:.0f},0 l0,12 q{-(aw+400)*.5:.0f},{16:.0f} {-aw-400:.0f},0 Z"'
             f' fill="url(#sneg)" opacity=".9"/>')
    s += SL(Z_SRED, most)
    # ТРОПА по склону
    s += SL(Z_SRED, f'<path d="M-40,1080 Q560,900 1060,820 Q1480,756 1920,700'
                    f' L1920,1080 Z" fill="#7a6e5e" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-40,1080 Q600,940 1100,862 Q1500,800 1920,752"'
                    f' fill="none" stroke="#8d8070" stroke-width="40" opacity=".8"/>')
    for i in range(30):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(800,1070):.0f}" rx="{rnd.uniform(12,46):.0f}"'
                        f' ry="{rnd.uniform(6,18):.0f}" fill="#6b6050" opacity=".65"/>')
    s += SL(Z_SRED, inej_mel(19, 50, 820, 1070))
    # сухие кусты и каменная хижина
    for i in range(6):
        kx = rnd.uniform(60, 1860)
        s += SL(Z_SRED, _trava_suhaya(rnd, 1, 880, 1050, kx, kx + 90))
    s += SL(Z_SRED, f'<rect x="1540" y="560" width="300" height="190" rx="8"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1520,560 l170,-110 l170,110 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1520,560 l170,-110 l170,110" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="14" opacity=".9"/>'
                    f'<rect x="1640" y="640" width="80" height="110" rx="6"'
                    f' fill="#3f3a33" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, dym(1700, 440, t, 6, .22, 260, .42, "#d7dee6", 1.0))
    # ВЬЮЧНЫЙ МУЛ
    s += SL(Z_SRED, f'<ellipse cx="1320" cy="880" rx="110" ry="60" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="1420" cy="822" r="42" fill="#6f6256" stroke="{K}"'
                    f' stroke-width="4.5"/>'
                    f'<path d="M1440,786 l10,-46 l20,42 Z" fill="#6f6256" stroke="{K}"'
                    f' stroke-width="3.4"/>'
                    f'<path d="M1240,930 l-10,54 M1300,942 l-4,48 M1370,938 l8,46"'
                    f' stroke="#55493f" stroke-width="12"/>'
                    f'<rect x="1250" y="812" width="140" height="60" rx="10"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="4"/>')
    # ПАВЕЛ со спины вверх по тропе + СТРАЖНИК
    idt = A.ease(A.seg(t, .3, 3.2))
    px, py, ph_ = 760 + 150 * idt, 1000 - 60 * idt, 620
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#6f6354",
                           ph=.2, naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .30, 38, t, "#e8e2d6", "#6f6354", .2, 4)
    r2, (e2x, e2y), _ = _ruka(px, py, ph_, -1, ph_ * .22, -16, t, "#e8e2d6", "#6f6354", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y-290:.0f} l{10:.0f},{py-e1y+270:.0f}"'
                    f' stroke="#7d5636" stroke-width="13" stroke-linecap="round"/>')
    pl = 40 + 24 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<path d="M{px+30:.0f},{py-ph_*.66:.0f} q{-70-pl:.0f},{130:.0f}'
                    f' {-170-pl:.0f},{230:.0f} q{76:.0f},{22:.0f} {160:.0f},{-44:.0f} Z"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="4.5"/>')
    sx_, sy_, sh2 = px - 250, py + 34, 560
    s += SL(Z_SRED, figura(sx_, sy_, sh2, t, col="#5e564c", kant="#cfe4f5", ph=.6))
    r3, (e3x, e3y), _ = _ruka(sx_, sy_, sh2, 1, sh2 * .26, 24, t, "#5e564c", "#cfe4f5", .3, 4)
    r4, (e4x, e4y), _ = _ruka(sx_, sy_, sh2, -1, sh2 * .22, 40, t, "#5e564c", "#cfe4f5", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, f'<path d="M{e3x:.0f},{e3y-280:.0f} l{6:.0f},{sy_-e3y+250:.0f}"'
                    f' stroke="#6b4428" stroke-width="9"/>'
                    f'<path d="M{e3x-6:.0f},{e3y-280:.0f} l{10:.0f},{-54:.0f} l{14:.0f},{52:.0f} Z"'
                    f' fill="#c9ccd1" stroke="{K}" stroke-width="3.4"/>'
                    f'<ellipse cx="{e4x-16:.0f}" cy="{e4y+16:.0f}" rx="54" ry="64"'
                    f' fill="#8a7a52" stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="{e4x-16:.0f}" cy="{e4y+16:.0f}" r="16" fill="#c9a05a"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, ten(px, py + 6, 120, 20, .4) + ten(sx_, sy_ + 6, 110, 18, .4))
    # ОРЁЛ кружит
    oa = (t * .25) % 1.0
    ox_, oy_ = 400 + 900 * oa, 220 + 90 * math.sin(oa * 6.283)
    s += SL(Z_LETIT, f'<path d="M{ox_:.0f},{oy_:.0f} q{40:.0f},{-30:.0f} {80:.0f},{-6:.0f}'
                     f' q{-40:.0f},{14:.0f} {-80:.0f},{6:.0f} Z" fill="#3f3a33"/>'
                     f'<path d="M{ox_:.0f},{oy_:.0f} q{-40:.0f},{-30:.0f} {-80:.0f},{-6:.0f}'
                     f' q{40:.0f},{14:.0f} {80:.0f},{6:.0f} Z" fill="#3f3a33"/>'
                     f'<ellipse cx="{ox_:.0f}" cy="{oy_+4:.0f}" rx="16" ry="9"'
                     f' fill="#2b2419"/>')
    s += SL(Z_PERED, f'<path d="M-20,1080 q160,{-140:.0f} 300,{-80:.0f} l0,200 l-320,0 Z"'
                     f' fill="#4a4038" opacity=".92"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def posoh_u_steny_hizhiny(t):
    """Каменная хижина в горах: у стены стоит посох с дорожной сумой, на
    пороге сложен плащ. Светильник в оконце гаснет, над горами встаёт одна
    яркая звезда. Людей нет."""
    rnd = random.Random(1914)
    s = nebo("noch", t, True, 71)
    s += SL(Z_NEBO, luna_v_gorode(260, 170, t, .72, True))
    for i, (sx, sb, sh_) in enumerate(((-120, 700, 560), (1360, 720, 620))):
        s += SL(Z_DAL, f'<path d="M{sx:.0f},{sb:.0f} l{sh_*.48:.0f},{-sh_:.0f}'
                       f' l{sh_*.32:.0f},{sh_*.40:.0f} l{sh_*.30:.0f},{-sh_*.26:.0f}'
                       f' l{sh_*.52:.0f},{sh_*.86:.0f} Z" fill="#3a434e" stroke="{K}"'
                       f' stroke-width="5"/>'
                       f'<path d="M{sx+sh_*.48:.0f},{sb-sh_:.0f} l{sh_*.16:.0f},{sh_*.20:.0f}'
                       f' l{-sh_*.32:.0f},0 Z" fill="url(#sneg)" opacity=".85"/>')
    # ЗВЕЗДА встаёт над горами
    vst = A.ease(A.seg(t, 1.2, 1.6))
    zx, zy = 1180, 320 - 90 * vst
    s += SL(Z_NEBO, f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="{10+6*vst:.0f}"'
                    f' fill="#ffffff" opacity="{vst:.2f}"/>'
                    f'<path d="M{zx-70*vst:.0f},{zy:.0f} h{140*vst:.0f}'
                    f' M{zx:.0f},{zy-70*vst:.0f} v{140*vst:.0f}" stroke="#ffffff"'
                    f' stroke-width="4" opacity="{vst*.8:.2f}"/>'
                    f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="{46*vst:.0f}" fill="#cfe4f5"'
                    f' opacity="{vst*.22:.2f}"/>')
    # ХИЖИНА на пол-кадра
    hx, hy, hw, hh = 560, 320, 820, 540
    hiz = (f'<rect x="{hx:.0f}" y="{hy:.0f}" width="{hw:.0f}" height="{hh:.0f}"'
           f' fill="#6f6256" stroke="{K}" stroke-width="7"/>')
    hiz += kladka(hx, hy, hw, hh, 62, "url(#kamen)")
    hiz += (f'<path d="M{hx-70:.0f},{hy:.0f} l{hw*.5+70:.0f},{-200:.0f}'
            f' l{hw*.5+70:.0f},{200:.0f} Z" fill="#5e564c" stroke="{K}" stroke-width="6"/>')
    hiz += (f'<path d="M{hx-70:.0f},{hy:.0f} l{hw*.5+70:.0f},{-200:.0f}'
            f' l{hw*.5+70:.0f},{200:.0f}" fill="none" stroke="url(#sneg)"'
            f' stroke-width="22" opacity=".92"/>')
    hiz += (f'<path d="M{hx+300:.0f},{hy+hh:.0f} l0,-230 q{90:.0f},{-70:.0f} {180:.0f},0'
            f' l0,230 Z" fill="#3f352c" stroke="{K}" stroke-width="6"/>')
    for i in range(5):
        hiz += (f'<rect x="{hx+310+i*34:.0f}" y="{hy+hh-224:.0f}" width="26"'
                f' height="224" fill="#4a3f34" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_DAL, hiz)
    # ОКОНЦЕ: светильник догорает и гаснет
    gas = max(.0, 1 - A.ease(A.seg(t, 1.0, 1.8)))
    s += SL(Z_SRED, f'<rect x="{hx+600:.0f}" y="{hy+150:.0f}" width="140" height="130"'
                    f' rx="8" fill="#241c16" stroke="{K}" stroke-width="6"/>')
    if gas > .02:
        s += SL(Z_SRED, f'<g opacity="{gas:.2f}">' + svecha(hx + 670, hy + 268, t, .2, 1.3, 70)
                + teplo(hx + 670, hy + 230, 200, 170, .55 * gas) + '</g>')
    # ПОСОХ с сумой у стены — главный предмет
    kach = 1.6 * A.w(t, 2.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 400 1000)">'
                    f'<rect x="376" y="300" width="48" height="700" rx="20"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M370,300 q{34:.0f},{-54:.0f} {68:.0f},{-10:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="22"/>'
                    f'<path d="M400,470 q{110:.0f},{40:.0f} {160:.0f},{140:.0f}'
                    f' q{-20:.0f},{130:.0f} {-146:.0f},{134:.0f} q{-118:.0f},{-14:.0f}'
                    f' {-108:.0f},{-140:.0f} q{44:.0f},{-96:.0f} {94:.0f},{-134:.0f} Z"'
                    f' fill="#c9b78e" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M320,590 q{84:.0f},{-56:.0f} {162:.0f},{10:.0f}"'
                    f' fill="none" stroke="#8a7a52" stroke-width="12"/>'
                    f'<path d="M332,700 q{80:.0f},{26:.0f} {150:.0f},{-6:.0f}"'
                    f' fill="none" stroke="#a8956f" stroke-width="9"/></g>')
    # плащ на пороге, снег ложится
    s += SL(Z_SRED, f'<path d="M760,1010 q{140:.0f},{-56:.0f} {290:.0f},{-6:.0f}'
                    f' q{20:.0f},{60:.0f} {-10:.0f},{80:.0f} q{-150:.0f},{20:.0f}'
                    f' {-290:.0f},{-4:.0f} Z" fill="#9aa3a8" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M790,1000 q{130:.0f},{-40:.0f} {250:.0f},{-4:.0f}"'
                    f' fill="none" stroke="url(#sneg)" stroke-width="14" opacity=".9"/>')
    # вязанка хвороста, кувшин, следы только к двери
    s += SL(Z_SRED, f'<g transform="rotate(-8 1500 1000)">')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{1400+i*8:.0f},1040 q{70:.0f},{-30-i*4:.0f}'
                        f' {150:.0f},{-16:.0f}" fill="none" stroke="#6b5230"'
                        f' stroke-width="7"/>')
    s += SL(Z_SRED, f'<rect x="1470" y="1000" width="22" height="46" rx="6"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, krynka_moloka(1700, 1046, .9, t, False, False, .4))
    s += SL(Z_SRED, sledy_valenok(1880, 1070, 1000, 1000, 7, 73, "#8aa0b4", 1.1))
    s += SL(Z_SRED, sneg_lezhit(980, 26, "url(#sneg)"))
    s += SL(Z_SRED, inej_mel(23, 60, 960, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 30, 17, .55, .6))
    s += ramka_pp("oba", "#0e0c0b", .55)
    s += vinetka(.46)
    return s


def chelovek_protiv_vetra(t):
    """Навстречу человеку дует рисованный ветер-великан с надутыми щеками:
    гонит пыль и листья, срывает шапки с прохожих и поворачивает их назад.
    Человек стоит прямо, обе руки на посохе, ноги упёрты в землю."""
    rnd = random.Random(1915)
    s = nebo("sumer", t, False, 73)
    s += oblaka(t, 110, 7, 67, .50)
    s += SL(Z_DAL, ulica_dal(40, 520, 820, t, False, 31))
    s += SL(Z_DAL, izba_snaruzhi(250, 560, 260, t, True, True, 47)
            + dym(276, 420, t, 6, .24, 240, .44, "#d7dee6", .9))
    # ВЕТЕР-ВЕЛИКАН справа: лицо из туч с надутыми щеками
    dut = .5 + .5 * A.w(t, 1.2, .0)
    vx, vy = 1600, 330
    vel = (f'<ellipse cx="{vx:.0f}" cy="{vy:.0f}" rx="{300+30*dut:.0f}"'
           f' ry="{230+20*dut:.0f}" fill="#8a98a8" opacity=".55"/>')
    vel += (f'<ellipse cx="{vx:.0f}" cy="{vy:.0f}" rx="{230+20*dut:.0f}"'
            f' ry="{180+14*dut:.0f}" fill="#9fb0c0" opacity=".65"/>')
    for i in (-1, 1):
        vel += (f'<ellipse cx="{vx+i*110:.0f}" cy="{vy+30:.0f}" rx="{70+26*dut:.0f}"'
                f' ry="{58+20*dut:.0f}" fill="#b4c2d0" opacity=".75"/>')
        vel += (f'<path d="M{vx+i*96:.0f},{vy-40:.0f} q{-i*26:.0f},{18:.0f} {-i*52:.0f},{2:.0f}"'
                f' fill="none" stroke="#5e6a78" stroke-width="9"/>')
    vel += (f'<ellipse cx="{vx-60:.0f}" cy="{vy+74:.0f}" rx="{44+16*dut:.0f}"'
            f' ry="{30+10*dut:.0f}" fill="#4a5664"/>')
    for i in range(7):
        d = ((t * 1.1 + i / 7.0) % 1.0)
        vel += (f'<path d="M{vx-100-900*d:.0f},{vy+90+40*math.sin(i+d*6):.0f}'
                f' q{-120:.0f},{-26:.0f} {-240:.0f},{6:.0f}" fill="none" stroke="#cfd6de"'
                f' stroke-width="{10-6*d:.1f}" opacity="{(1-d)*.6:.2f}"/>')
    s += SL(Z_DAL, vel)
    # дорога, пыль и листья по ветру
    s += SL(Z_SRED, _merzlaya_zemlya(620, 29, True))
    for i in range(26):
        d = ((t * 1.4 + i / 26.0) % 1.0)
        lx = 1900 - 2000 * d
        ly = 700 + 300 * ((i * 7) % 10) / 10.0 + 40 * math.sin(d * 7 + i)
        s += SL(Z_LETIT, f'<path d="M{lx:.0f},{ly:.0f} l{18:.0f},{-12:.0f} l{6:.0f},{14:.0f}'
                         f' l{-16:.0f},{8:.0f} Z" fill="{"#9a5a28" if i%2 else "#b4762f"}"'
                         f' opacity="{.5+.4*(1-d):.2f}"/>')
    # ПРОХОЖИЕ-СИЛУЭТЫ, которых разворачивает; шапки летят
    for i, (hx, hy, hh) in enumerate(((320, 980, 420), (560, 1010, 450))):
        pov = A.ease(A.seg(t, .5 + i * .3, 1.0))
        s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a4450", kant="#cfe4f5",
                               ph=i * .4, naklon=5.0 + 4 * pov))
        rk, (ex, ey), _ = _ruka(hx, hy, hh, 1, hh * .26, -30 + 40 * pov, t,
                                "#4a4450", "#cfe4f5", i * .3, 8)
        s += SL(Z_SRED, rk)
        s += SL(Z_SRED, f'<ellipse cx="{hx-120-240*pov:.0f}" cy="{hy-hh-40-120*pov:.0f}"'
                        f' rx="40" ry="24" fill="#5e4a3a" stroke="{K}" stroke-width="3.6"'
                        f' transform="rotate({-40*pov:.0f} {hx-120-240*pov:.0f}'
                        f' {hy-hh-40-120*pov:.0f})"/>')
        s += SL(Z_SRED, ten(hx, hy + 6, 96, 17, .35))
    # ГЛАВНЫЙ: стоит прямо, обе руки на посохе, ноги расставлены
    px, py, ph_ = 1060, 1050, 660
    s += SL(Z_SRED, figura(px, py, ph_, t, col="#e8e2d6", kant="#8a7a52",
                           boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(px, py, ph_, 1, ph_ * .26, 34, t, "#e8e2d6", "#8a7a52", .2, 2)
    r2, (e2x, e2y), _ = _ruka(px, py, ph_, -1, ph_ * .24, 40, t, "#e8e2d6", "#8a7a52", .5, 2)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{(e1x+e2x)/2:.0f},{e1y-240:.0f} l{4:.0f},{py-e1y+220:.0f}"'
                    f' stroke="#7d5636" stroke-width="15" stroke-linecap="round"/>')
    odzh = 30 + 18 * dut
    s += SL(Z_SRED, f'<path d="M{px-70:.0f},{py-ph_*.58:.0f} q{-60-odzh:.0f},{150:.0f}'
                    f' {-130-odzh:.0f},{250:.0f} q{70:.0f},{26:.0f} {140:.0f},{-30:.0f} Z"'
                    f' fill="#d8cbb0" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, ten(px, py + 8, 150, 24, .45))
    # согнутое дерево, сорванный навес, придорожный камень
    s += SL(Z_SRED, f'<g transform="rotate(-18 1810 1020)">'
            + goloe_derevo_ld(1810, 1020, 420, t, 29, 6, False) + '</g>')
    nav = 14 * A.w(t, 1.0, .3)
    s += SL(Z_SRED, f'<g transform="rotate({-20+nav:.1f} 200 760)">'
                    f'<path d="M80,760 q{120:.0f},{-46:.0f} {240:.0f},0 l{-18:.0f},{34:.0f}'
                    f' q{-100:.0f},{-30:.0f} {-204:.0f},0 Z" fill="#8a2f22" stroke="{K}"'
                    f' stroke-width="4.5"/></g>'
                    f'<rect x="86" y="760" width="14" height="230" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M1390,1070 q30,{-120:.0f} 140,{-100:.0f} q46,{64:.0f}'
                    f' {30:.0f},{100:.0f} Z" fill="#8a8078" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, dvorovye_veschi(560, 1070, 320, t, 31, ["korzina", "churbak"]))
    # ЦЕНТР КАДРА НЕ ПУСТОЙ: вдоль дороги камни, бурьян, рассыпанная поклажа
    for i, (kx, ky, ks) in enumerate(((760, 940, .8), (1280, 900, .6), (900, 1020, 1.0))):
        s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="{54*ks:.0f}"'
                        f' ry="{30*ks:.0f}" fill="#8a8078" stroke="{K}"'
                        f' stroke-width="{4*ks:.1f}"/>'
                        f'<path d="M{kx-40*ks:.0f},{ky-10*ks:.0f} q{40*ks:.0f},{-18*ks:.0f}'
                        f' {80*ks:.0f},{4*ks:.0f}" fill="none" stroke="#6f6256"'
                        f' stroke-width="{6*ks:.1f}"/>')
    s += SL(Z_SRED, _trava_suhaya(rnd, 11, 760, 1060, 620, 1860))
    s += SL(Z_SRED, f'<path d="M1180,1040 q{54:.0f},{18:.0f} {108:.0f},0 l{-10:.0f},{34:.0f}'
                    f' h{-88:.0f} Z" fill="#b08a52" stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<ellipse cx="{1196+i*22:.0f}" cy="{1044:.0f}" rx="13" ry="9"'
                        f' fill="#9a5a28" stroke="{K}" stroke-width="2.4"/>')
    s += SL(Z_SRED, inej_mel(37, 44, 820, 1070, 400, 1900))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="80" height="{H}" fill="#1d1611"'
                     f' opacity=".85"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def imya_nad_zamerzshey_rekoy(t):
    """Деревня над рекой: река на глазах затягивается льдом от берегов к
    середине, над ней из морозного пара складывается имя дня. Дед в тулупе
    показывает внуку на реку."""
    rnd = random.Random(1916)
    gor = 460
    s = nebo("rassv", t, False, 79)
    s += oblaka(t, 140, 5, 71, .40)
    s += SL(Z_DAL, ulica_dal(0, gor - 20, 980, t, True, 37))
    for i, (ix, iw) in enumerate(((1120, 300), (1500, 260), (1760, 240))):
        s += SL(Z_DAL, izba_snaruzhi(ix, gor + 10, iw, t, True, True, 41 + i)
                + dym(ix + iw * .1, gor - iw * .62, t, 6, .22, 270, .42, "#d7dee6", 1.0))
    s += SL(Z_DAL, goloe_derevo_ld(980, gor + 24, 300, t, 43, 6, True))
    # РЕКА: лёд идёт от берегов к середине
    led = A.ease(A.seg(t, .4, 3.2))
    s += SL(Z_SRED, f'<rect x="0" y="{gor+120:.0f}" width="{W}" height="{H-gor-120:.0f}"'
                    f' fill="{VODA}"/>')
    for i in range(16):
        yy = gor + 140 + i * 36
        s += SL(Z_SRED, f'<path d="M{rnd.uniform(-40,300):.0f},{yy:.0f}'
                        f' q{rnd.uniform(400,800):.0f},{rnd.uniform(-10,10):.0f}'
                        f' {rnd.uniform(1400,1960):.0f},{rnd.uniform(-8,8):.0f}"'
                        f' fill="none" stroke="#3f8a94" stroke-width="{rnd.uniform(2,5):.1f}"'
                        f' opacity=".55"/>')
    for i in (-1, 1):
        shir = 520 * led
        s += SL(Z_SRED, f'<path d="M{(0 if i<0 else W):.0f},{gor+120:.0f}'
                        f' q{i*shir*.5:.0f},{140:.0f} {i*shir*.2:.0f},{H-gor-120:.0f}'
                        f' l{-i*shir*.4:.0f},0 l0,{-(H-gor-120):.0f} Z"'
                        f' fill="url(#led)" opacity=".92"/>')
        s += SL(Z_SRED, f'<path d="M{(0 if i<0 else W)+i*shir*.2:.0f},{gor+140:.0f}'
                        f' q{i*60:.0f},{220:.0f} {-i*20:.0f},{430:.0f}" fill="none"'
                        f' stroke="#eaf6ff" stroke-width="8" opacity=".7"/>')
    s += SL(Z_SRED, korka_lda(960, 880, 300 * led + 60, 90, t, .2, .0, .8, .4))
    # ПАР над рекой складывается в полосы-слово (своих букв не рисуем)
    for i in range(7):
        d = A.ease(A.seg(t, 1.0 + i * .12, 1.0))
        px_ = 560 + i * 130
        s += SL(Z_SRED, f'<path d="M{px_:.0f},{gor+80:.0f} q{26:.0f},{-40*d:.0f}'
                        f' {54:.0f},{-14*d:.0f} q{-24:.0f},{30*d:.0f} {-54:.0f},{14*d:.0f} Z"'
                        f' fill="#eef6ff" opacity="{.55*d:.2f}"/>')
    s += SL(Z_SRED, tuman(t, gor + 60, .34, "#dde7f0"))
    # ДЕД показывает внуку на реку
    dx, dy, dh = 420, 1040, 660
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#4a4038", kant="#ffd9a8",
                           tulup=True, boroda=True, shapka=True, ph=.2))
    uk = A.ease(A.seg(t, .5, 1.2))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, 1, dh * .34, 20 - 36 * uk, t,
                              "#4a4038", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, -1, dh * .26, 54, t, "#4a4038", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x + 14, e1y + 6, 1.0, 10 - 30 * uk, "#6b4428", t, .2)
            + r2)
    vx, vy, vh = 250, 1060, 400
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#3f5a6a", kant="#ffd9a8",
                           shapka=True, ph=.6))
    s += SL(Z_SRED, f'<path d="M{e2x:.0f},{e2y:.0f} L{vx+70:.0f},{vy-vh*.52:.0f}"'
                    f' stroke="#4a4038" stroke-width="15" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(dx - 36, dy - dh * .80, t, .3, 1.0, .5)
            + para_izo_rta(vx - 24, vy - vh * .80, t, .8, .8, .45))
    s += SL(Z_SRED, ten(dx, dy + 6, 124, 21, .4) + ten(vx, vy + 6, 86, 15, .4))
    # лодки вверх дном, мостки, баня
    for i, (lx, ly, ls) in enumerate(((760, 1012, 1.0), (1040, 1046, .84))):
        s += SL(Z_SRED, f'<path d="M{lx-150*ls:.0f},{ly:.0f} q{150*ls:.0f},{-70*ls:.0f}'
                        f' {300*ls:.0f},0 Z" fill="#6b4428" stroke="{K}"'
                        f' stroke-width="{5*ls:.1f}"/>'
                        f'<path d="M{lx-120*ls:.0f},{ly-16*ls:.0f} q{120*ls:.0f},{-46*ls:.0f}'
                        f' {240*ls:.0f},0" fill="none" stroke="#54351f"'
                        f' stroke-width="{5*ls:.1f}"/>'
                        f'<path d="M{lx-150*ls:.0f},{ly:.0f} h{300*ls:.0f}"'
                        f' stroke="url(#sneg)" stroke-width="{10*ls:.1f}" opacity=".9"/>')
    s += SL(Z_SRED, mostki(1340, 920, 480, t, True, 150))
    s += SL(Z_SRED, kamysh(1880, 1060, 240, t, 7, 47, True)
            + kamysh(60, 1040, 200, t, 6, 53, True))
    s += SL(Z_SRED, dvorovye_veschi(1500, 1070, 360, t, 43, ["kadka", "vedro", "grabli"]))
    s += SL(Z_LETIT, sneg_letit(t, 18, 19, .40, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def posoh_i_led(t):
    """Кадр надвое: слева посох стоит прямо в камнях, на него давят
    рисованные ладони-тучи и не гнут; справа над первым льдом занесён
    валенок — и отступает на берег. Обе половины вспыхивают ровным светом."""
    rnd = random.Random(1917)
    s = nebo("sumer", t, True, 83)
    s += SL(Z_NEBO, f'<rect x="0" y="0" width="{W*.5:.0f}" height="{H}" fill="#2f3b4e"'
                    f' opacity=".45"/>')
    # ЛЕВАЯ ПОЛОВИНА: камни, посох, ладони-тучи
    for i, (sx, sb, sh_) in enumerate(((-120, 700, 520), (420, 760, 420))):
        s += SL(Z_DAL, f'<path d="M{sx:.0f},{sb:.0f} l{sh_*.5:.0f},{-sh_:.0f}'
                       f' l{sh_*.34:.0f},{sh_*.40:.0f} l{sh_*.46:.0f},{sh_*.60:.0f} Z"'
                       f' fill="#4a5664" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="0" y="880" width="{W*.5:.0f}" height="200" fill="#6f6256"/>')
    for i in range(14):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(0,950):.0f}"'
                        f' cy="{rnd.uniform(900,1070):.0f}" rx="{rnd.uniform(26,70):.0f}"'
                        f' ry="{rnd.uniform(12,30):.0f}" fill="#8a8078" stroke="{K}"'
                        f' stroke-width="4"/>')
    davl = .5 + .5 * A.w(t, 1.4, .0)
    s += SL(Z_SRED, f'<rect x="418" y="300" width="74" height="640" rx="28"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="7"/>'
                    f'<path d="M420,320 q{36:.0f},{-56:.0f} {72:.0f},{-10:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="24"/>'
                    f'<path d="M426,460 h58 M426,620 h58 M426,780 h58"'
                    f' stroke="#6b4428" stroke-width="7" opacity=".8"/>')
    for i, (lx, ly) in enumerate(((300, 330), (640, 360))):
        s += SL(Z_SRED, f'<ellipse cx="{lx:.0f}" cy="{ly+30*davl:.0f}" rx="170" ry="104"'
                        f' fill="#6a7888" opacity=".95" stroke="#48525e" stroke-width="7"/>')
        for k in range(4):
            s += SL(Z_SRED, f'<ellipse cx="{lx-54+k*36:.0f}" cy="{ly+86+30*davl:.0f}"'
                            f' rx="20" ry="46" fill="#8a98a8" opacity=".85"'
                            f' stroke="#5e6a78" stroke-width="4"/>')
    vsp = max(.0, A.w(t, 2.4, .2))
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W*.5:.0f}" height="{H}" fill="#ffe9ac"'
                    f' opacity="{.16*vsp:.2f}"/>')
    # ПРАВАЯ ПОЛОВИНА: пруд, ива, мостки, валенок отступает
    s += SL(Z_SRED, f'<rect x="{W*.5:.0f}" y="640" width="{W*.5:.0f}" height="440"'
                    f' fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(1430, 860, 360, 140, t, .3))
    s += SL(Z_SRED, f'<rect x="{W*.5:.0f}" y="560" width="{W*.5:.0f}" height="90"'
                    f' fill="#5f4a32"/>' + sneg_lezhit(600, 24, "url(#sneg)"))
    s += SL(Z_SRED, mostki(1540, 700, 380, t, True, 160))
    s += SL(Z_SRED, goloe_derevo_ld(1120, 660, 420, t, 59, 7, True))
    s += SL(Z_SRED, kamysh(1880, 900, 190, t, 6, 61, True))
    otst = A.ease(A.seg(t, .8, 1.4))
    s += SL(Z_PERED, _valenok(1420 + 180 * otst, 760 - 120 * (1 - otst) + 200 * otst,
                              .9, -10 + 16 * otst))
    s += SL(Z_SRED, f'<rect x="{W*.5:.0f}" y="0" width="{W*.5:.0f}" height="{H}"'
                    f' fill="#ffe9ac" opacity="{.16*vsp:.2f}"/>')
    # шов кадра: столб света по центру
    s += SL(Z_PERED, f'<rect x="{W*.5-7:.0f}" y="0" width="14" height="{H}"'
                     f' fill="#dcecf8" opacity=".5"/>')
    s += SL(Z_SRED, dvorovye_veschi(1640, 1066, 280, t, 59, ["vedro", "korzina"])
            + dvorovye_veschi(140, 1066, 300, t, 61, ["churbak", "metla"]))
    s += SL(Z_SRED, svecha(760, 1010, t, .1, 1.5, 90) + teplo(760, 970, 230, 200, .45))
    # ОБЕ ПОЛОВИНЫ ОБЖИТЫ: слева осыпь и сухие кусты, справа берег с вещами
    for i in range(10):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(40,900):.0f}"'
                        f' cy="{rnd.uniform(820,1060):.0f}" rx="{rnd.uniform(18,44):.0f}"'
                        f' ry="{rnd.uniform(9,20):.0f}" fill="#7a6e5e" stroke="{K}"'
                        f' stroke-width="3.4"/>')
    s += SL(Z_SRED, _trava_suhaya(rnd, 8, 860, 1050, 60, 900))
    s += SL(Z_SRED, _trava_suhaya(rnd, 7, 900, 1060, 1000, 1880))
    for i, (kx, ky) in enumerate(((1180, 980), (1300, 1016), (1640, 1004))):
        s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="{44-i*6:.0f}"'
                        f' ry="{22-i*3:.0f}" fill="#8a8078" stroke="{K}"'
                        f' stroke-width="3.6"/>')
    s += SL(Z_SRED, sanki_derev(1000, 1050, .72, t, .5, True))
    s += SL(Z_SRED, kamysh(1060, 1030, 150, t, 5, 67, True))
    s += SL(Z_SRED, sledy_valenok(1900, 1060, 1500, 940, 6, 71, "#8aa0b4", 1.0))
    s += SL(Z_SRED, inej_mel(73, 50, 840, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 24, 23, .45, .6))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def chetyre_ldinki_na_perilah(t):
    """Перила крыльца на пол-кадра: в ряд стоят на ребре четыре прозрачные
    льдинки, солнце бросает сквозь них радужные пятна на стену. Бабушка
    ставит четвёртую, внук считает. Правая треть оставлена под памятку."""
    rnd = random.Random(1918)
    s = nebo("rassv", t, False, 89)
    s += oblaka(t, 130, 4, 73, .34, "#ffe9c8")
    s += SL(Z_NEBO, f'<circle cx="300" cy="250" r="96" fill="#ffe9ac" opacity=".5"/>'
                    f'<circle cx="300" cy="250" r="58" fill="#fff4d8" opacity=".9"/>')
    s += SL(Z_DAL, ulica_dal(1180, 520, 740, t, True, 59))
    s += SL(Z_DAL, goloe_derevo_ld(1020, 560, 340, t, 67, 6, True))
    # СТЕНА ИЗБЫ с дверью — на неё ложатся радужные пятна
    s += SL(Z_SRED, brevna(0, 120, 1120, 740, 88, 2))
    s += SL(Z_SRED, dver(140, 300, 300, 520, .0, "url(#derev)", True, False))
    s += SL(Z_SRED, f'<path d="M120,286 h340 l-14,-30 h-312 Z" fill="{DOSKA2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        rx_ = 520 + i * 110
        s += SL(Z_SRED, f'<ellipse cx="{rx_:.0f}" cy="{420+((i*7)%4)*40:.0f}" rx="54"'
                        f' ry="34" fill="{["#c8301f","#d6a63f","#56763f","#3f6b7a","#8a2f8a"][i%5]}"'
                        f' opacity="{.22+.12*A.w(t,2.6,i*.3):.2f}"/>')
    # ПЕРИЛА крыльца во всю ширину
    s += SL(Z_SRED, f'<rect x="-20" y="820" width="1600" height="40" rx="10"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="-20" y="940" width="1600" height="26" rx="8"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="4.5"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="{30+i*170:.0f}" y="860" width="28" height="200"'
                        f' fill="{DOSKA}" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<rect x="-20" y="1040" width="1920" height="40" fill="{DOSKA2}"'
                    f' stroke="{K}" stroke-width="5"/>')
    # ЧЕТЫРЕ ЛЬДИНКИ на ребре; четвёртая встаёт
    stav = A.out(A.seg(t, .8, 1.1))
    for i in range(4):
        lx = 300 + i * 220
        ly = 820 - (0 if i < 3 else 150 * (1 - stav))
        op = 1.0 if i < 3 else stav
        s += SL(Z_SRED, f'<g opacity="{op:.2f}">'
                        f'<path d="M{lx-58:.0f},{ly:.0f} l{18:.0f},{-120:.0f}'
                        f' l{80:.0f},{-8:.0f} l{20:.0f},{128:.0f} Z" fill="#cfe4f5"'
                        f' opacity=".75" stroke="#eaf6ff" stroke-width="5"/>'
                        f'<path d="M{lx-40:.0f},{ly-110:.0f} l{14:.0f},{104:.0f}"'
                        f' fill="none" stroke="#ffffff" stroke-width="6" opacity=".7"/>'
                        f'<path d="M{lx+22:.0f},{ly-118:.0f} l{10:.0f},{112:.0f}"'
                        f' fill="none" stroke="#9fd0e4" stroke-width="4" opacity=".7"/>'
                        f'<ellipse cx="{lx-6:.0f}" cy="{ly-64:.0f}" rx="22" ry="34"'
                        f' fill="#ffffff" opacity="{.18+.12*A.w(t,3.0,i*.4):.2f}"/></g>')
    # БАБУШКА ставит четвёртую, ВНУК считает
    bx, by, bh = 1300, 1046, 620
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, -1, bh * .34, 6 + 16 * (1 - stav), t,
                              "#4a3a52", "#ffd9a8", .2, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x - 10, e1y + 12, 1.0, -14, TKAN, t, .3))
    vx, vy, vh = 980, 1060, 420
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#3f5a6a", kant="#ffd9a8",
                           shapka=True, ph=.7))
    r2, (e2x, e2y), _ = _ruka(vx, vy, vh, 1, vh * .28, -34, t, "#3f5a6a", "#ffd9a8", .4, 5)
    r3, (e3x, e3y), _ = _ruka(vx, vy, vh, -1, vh * .26, -30, t, "#3f5a6a", "#ffd9a8", .9, 5)
    s += SL(Z_SRED, r2 + varezhka(e2x + 6, e2y + 8, .8, 10, TKAN, t, .4)
            + r3 + varezhka(e3x - 6, e3y + 8, .8, -10, TKAN, t, .9))
    s += SL(Z_SRED, para_izo_rta(bx - 34, by - bh * .80, t, .3, 1.0, .5)
            + para_izo_rta(vx - 24, vy - vh * .80, t, .8, .8, .45))
    s += SL(Z_SRED, ten(bx, by + 6, 120, 20, .4) + ten(vx, vy + 6, 90, 16, .4))
    # веник, валенки, рябина, сугроб
    s += SL(Z_SRED, dvorovye_veschi(60, 1040, 300, t, 67, ["metla", "vedro"]))
    s += SL(Z_SRED, _valenok(560, 1040, .62, -4) + _valenok(630, 1044, .62, 6))
    s += SL(Z_SRED, ryabina(1700, 1000, t, 1.5, 6)
            + kalina_grozd(1740, 930, t, 1.0, 12, 71, .2))
    s += SL(Z_SRED, sneg_lezhit(1000, 28, "url(#sneg)"))
    s += SL(Z_SRED, dym(1240, 300, t, 6, .22, 280, .40, "#d7dee6", 1.0))
    s += SL(Z_LETIT, sneg_letit(t, 16, 29, .36, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def kabluk_nad_korkoy(t):
    """Плашка первого запрета: лужа под белой коркой с вмёрзшей травинкой,
    над ней занесён детский ботинок с каблуком на треть кадра — зависает и
    возвращается на землю. В кадре только ноги до колен."""
    rnd = random.Random(1919)
    s = nebo("den", t, False, 97)
    s += oblaka(t, 150, 5, 79, .42)
    s += SL(Z_DAL, zabor_shtaket(-40, 300, 2000, 260, 79, 64))
    s += SL(Z_DAL, goloe_derevo_ld(1600, 560, 420, t, 83, 6, True))
    s += SL(Z_DAL, izba_snaruzhi(300, 560, 260, t, True, True, 23)
            + dym(326, 420, t, 6, .22, 240, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(560, 83, False))
    # КОЛЕЯ и лужа под коркой
    for i in range(2):
        s += SL(Z_SRED, f'<path d="M-40,{900+i*90:.0f} Q700,{840+i*80:.0f}'
                        f' 1960,{880+i*86:.0f}" fill="none" stroke="#3f3122"'
                        f' stroke-width="{26-i*6:.0f}" opacity=".55"/>')
    s += SL(Z_SRED, f'<ellipse cx="780" cy="900" rx="430" ry="150" fill="#2f4a52"/>')
    s += SL(Z_SRED, korka_lda(780, 898, 400, 130, t, .1, .0, .95))
    s += SL(Z_SRED, f'<ellipse cx="780" cy="900" rx="438" ry="156" fill="none"'
                    f' stroke="#6b5438" stroke-width="20" opacity=".85"/>')
    s += SL(Z_SRED, _trava_suhaya(rnd, 6, 940, 1050, 400, 1200))
    # БОТИНОК с каблуком на треть кадра: зависает и возвращается
    viс = A.ease(A.seg(t, .4, 1.0)) - A.ease(A.seg(t, 1.8, 1.0))
    bx, by = 900, 860 - 240 * viс
    s += SL(Z_SRED, f'<g transform="rotate({-14+10*viс:.1f} {bx:.0f} {by:.0f})">'
                    f'<path d="M{bx-150:.0f},{by-40:.0f} q{40:.0f},{-120:.0f} {150:.0f},{-110:.0f}'
                    f' q{90:.0f},{10:.0f} {120:.0f},{90:.0f} l{10:.0f},{70:.0f}'
                    f' q{-130:.0f},{40:.0f} {-280:.0f},{-10:.0f} Z" fill="#8a5a38"'
                    f' stroke="{K}" stroke-width="8"/>'
                    f'<path d="M{bx-160:.0f},{by-28:.0f} h{300:.0f} q{20:.0f},{20:.0f}'
                    f' {4:.0f},{46:.0f} h{-300:.0f} Z" fill="#2b2016" stroke="{K}"'
                    f' stroke-width="6"/>'
                    f'<rect x="{bx+60:.0f}" y="{by+16:.0f}" width="70" height="56"'
                    f' rx="6" fill="#241c16" stroke="{K}" stroke-width="5"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{bx-96+i*52:.0f},{by-96:.0f} l{34:.0f},{14:.0f}"'
                        f' stroke="#f2ead6" stroke-width="9"/>')
    s += SL(Z_SRED, f'<path d="M{bx-150:.0f},{by-146:.0f} q{120:.0f},{-30:.0f}'
                    f' {250:.0f},{10:.0f} l{10:.0f},{-170:.0f} q{-140:.0f},{-30:.0f}'
                    f' {-270:.0f},{-6:.0f} Z" fill="#5a6a7a" stroke="{K}"'
                    f' stroke-width="6"/></g>')
    # вторая нога стоит на земле
    s += SL(Z_SRED, f'<path d="M420,1000 q{30:.0f},{-90:.0f} {120:.0f},{-84:.0f}'
                    f' q{70:.0f},{8:.0f} {94:.0f},{70:.0f} l{8:.0f},{54:.0f}'
                    f' q{-100:.0f},{30:.0f} {-222:.0f},{-8:.0f} Z" fill="#4a3526"'
                    f' stroke="{K}" stroke-width="7"/>'
                    f'<path d="M412,1012 h236 q{16:.0f},{16:.0f} {2:.0f},{38:.0f}'
                    f' h{-238:.0f} Z" fill="#2b2016" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M420,916 q{100:.0f},{-24:.0f} {210:.0f},{8:.0f}'
                    f' l{8:.0f},{-150:.0f} q{-120:.0f},{-26:.0f} {-226:.0f},{-4:.0f} Z"'
                    f' fill="#5a6a7a" stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, ten(520, 1050, 130, 20, .4) + ten(bx, 1046, 150, 22, .35 + .2 * (1 - viс)))
    # жёлтый лист, камешек, воробьи
    s += SL(Z_SRED, f'<path d="M1320,980 l{40:.0f},{-30:.0f} l{-8:.0f},{30:.0f}'
                    f' l{40:.0f},{-8:.0f} l{-30:.0f},{28:.0f} l{26:.0f},{20:.0f}'
                    f' l{-40:.0f},{4:.0f} l{-6:.0f},{30:.0f} l{-26:.0f},{-24:.0f}'
                    f' l{-32:.0f},{16:.0f} l{12:.0f},{-32:.0f} l{-34:.0f},{-8:.0f} Z"'
                    f' fill="#b4762f" stroke="#7d4a24" stroke-width="3.4"/>'
                    f'<ellipse cx="1480" cy="1020" rx="40" ry="24" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i, (vx, vy) in enumerate(((1560, 940), (1680, 980), (1760, 920))):
        s += SL(Z_SRED, ptica(vx, vy, t, 1.5, "#8a7a62", i * .3, "#6f6256"))
    s += SL(Z_SRED, dvorovye_veschi(100, 1066, 300, t, 71, ["vedro", "korzina"]))
    s += SL(Z_SRED, inej_mel(79, 50, 940, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 14, 31, .34, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def prud_v_razreze_ledyanaya_krysha(t):
    """Пруд в разрезе: сверху тонкая пластина льда как стеклянная крыша, под
    ней толща воды с зимними жильцами — караси, щука в корягах, рак, лягушка
    в иле. Круглый иллюминатор в толще — настоящий лёд изнутри."""
    rnd = random.Random(1920)
    s = nebo("sumer", t, False, 101)
    s += SL(Z_DAL, ulica_dal(40, 220, 820, t, True, 73))
    s += SL(Z_DAL, goloe_derevo_ld(1640, 250, 320, t, 89, 6, True))
    s += SL(Z_DAL, izba_snaruzhi(1200, 240, 240, t, True, True, 29)
            + dym(1224, 118, t, 5, .22, 220, .38, "#d7dee6", .9))
    s += SL(Z_SRED, mostki(180, 230, 420, t, True, 120))
    # ЛЕДЯНАЯ КРЫША
    s += SL(Z_SRED, f'<rect x="0" y="300" width="{W}" height="86" fill="url(#led)"'
                    f' stroke="#eaf6ff" stroke-width="6"/>')
    s += SL(Z_SRED, korka_lda(960, 344, 900, 40, t, .2, .0, .85))
    # ТОЛЩА ВОДЫ
    s += SL(Z_SRED, f'<rect x="0" y="386" width="{W}" height="{H-386}" fill="{VODA}"/>'
            + f'<rect x="0" y="386" width="{W}" height="{H-386}" fill="{VODA2}"'
              f' opacity=".45"/>')
    for i in range(13):
        yy = 420 + i * 54
        s += SL(Z_SRED, f'<path d="M{rnd.uniform(-40,200):.0f},{yy:.0f}'
                        f' q{rnd.uniform(400,900):.0f},{rnd.uniform(-14,14):.0f}'
                        f' {rnd.uniform(1500,1980):.0f},{rnd.uniform(-10,10):.0f}"'
                        f' fill="none" stroke="#3f8a94" stroke-width="{rnd.uniform(2,6):.1f}"'
                        f' opacity=".4"/>')
    # СВАИ МОСТКОВ уходят в воду, а вокруг них стоит рыба — середина кадра
    for i, px_ in enumerate((430, 560, 690)):
        s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="360" width="30" height="700"'
                        f' fill="#54351f" stroke="{K}" stroke-width="4" opacity=".92"/>')
        for k in range(5):
            s += SL(Z_SRED, f'<ellipse cx="{px_+15:.0f}" cy="{460+k*130:.0f}" rx="26"'
                            f' ry="11" fill="#3f7f6a" opacity=".7"/>')
    for i in range(11):
        kx = 760 + (i % 4) * 150 + rnd.uniform(-26, 26)
        ky = 430 + (i // 4) * 120 + rnd.uniform(-22, 22)
        pl = 9 * A.w(t, 2.2, i * .21)
        s += SL(Z_SRED, f'<path d="M{kx-40:.0f},{ky:.0f} q{40:.0f},{-26:.0f} {80:.0f},0'
                        f' q{-40:.0f},{26:.0f} {-80:.0f},0 Z" fill="#b58a3a"'
                        f' stroke="{K}" stroke-width="3.2"/>'
                        f'<path d="M{kx+40:.0f},{ky:.0f} l{22+pl:.0f},{-14:.0f} l0,{28:.0f} Z"'
                        f' fill="#9a722c" stroke="{K}" stroke-width="2.8"/>'
                        f'<circle cx="{kx-24:.0f}" cy="{ky-4:.0f}" r="4" fill="{K}"/>')
    s += SL(Z_SRED, f'<path d="M420,760 q{260:.0f},{-60:.0f} {560:.0f},{-10:.0f}'
                    f' q{180:.0f},{30:.0f} {300:.0f},{40:.0f} l0,{46:.0f}'
                    f' q{-300:.0f},{-30:.0f} {-860:.0f},{14:.0f} Z" fill="#54351f"'
                    f' stroke="{K}" stroke-width="5"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{520+i*170:.0f},760 q{30:.0f},{-70:.0f}'
                        f' {70:.0f},{-96:.0f}" fill="none" stroke="#46301c"'
                        f' stroke-width="11"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{460+i*150:.0f}" cy="{880+((i*5)%3)*40:.0f}"'
                        f' rx="{34+((i*3)%4)*10:.0f}" ry="{16+((i*7)%3)*6:.0f}"'
                        f' fill="#5e564c" stroke="{K}" stroke-width="3.4"/>')
    # ТОЛЩА НЕ ПУСТАЯ: заросли рдеста, коряги, камни на дне, цепочки пузырьков
    for i in range(14):
        wx = 60 + i * 136 + rnd.uniform(-24, 24)
        wh = rnd.uniform(200, 460)
        kach = 10 * A.w(t, rnd.uniform(3.0, 5.0), i * .2)
        s += SL(Z_SRED, f'<path d="M{wx:.0f},1070 q{kach:.0f},{-wh*.5:.0f}'
                        f' {kach*1.6:.0f},{-wh:.0f}" fill="none" stroke="#2f6b5a"'
                        f' stroke-width="{rnd.uniform(5,11):.1f}" opacity=".8"/>')
        for k in range(4):
            py_ = 1070 - wh * (.3 + k * .18)
            s += SL(Z_SRED, f'<ellipse cx="{wx+kach*(.4+k*.3):.0f}" cy="{py_:.0f}"'
                            f' rx="{rnd.uniform(8,16):.0f}" ry="{rnd.uniform(16,30):.0f}"'
                            f' fill="#3f7f6a" opacity=".75"'
                            f' transform="rotate({rnd.uniform(-40,40):.0f}'
                            f' {wx:.0f} {py_:.0f})"/>')
    for i in range(10):
        cx_ = rnd.uniform(60, 1860); cy_ = rnd.uniform(980, 1060)
        s += SL(Z_SRED, f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}"'
                        f' rx="{rnd.uniform(26,62):.0f}" ry="{rnd.uniform(12,26):.0f}"'
                        f' fill="#5e564c" stroke="{K}" stroke-width="3.4" opacity=".9"/>')
    for i in range(8):
        bx_ = 140 + i * 230
        for k in range(5):
            d = ((t * .5 + i * .13 + k * .08) % 1.0)
            s += SL(Z_SRED, f'<circle cx="{bx_+10*math.sin(k+d*6):.0f}"'
                            f' cy="{960-520*d:.0f}" r="{3+5*d:.1f}" fill="#cfe4f5"'
                            f' opacity="{(1-d)*.5:.2f}"/>')
    # ИЛЛЮМИНАТОР: вид, метка, обвязка
    ox, oy, od = 1300, 520, 420
    put = kontur_proema(ox, oy, od, od, "ellips")
    ill = (f'<path d="{put}" fill="#9fc4d8"/>')
    ill += (f'<path d="{put}" fill="#cfe4f5" opacity=".5"/>')
    ill += mesto_stoka(ox, oy, od, od, "ellips")
    ill += (f'<circle cx="{ox+od*.5:.0f}" cy="{oy+od*.5:.0f}" r="{od*.5:.0f}"'
            f' fill="none" stroke="#5e6a78" stroke-width="22"/>')
    for i in range(10):
        a = i * .628
        ill += (f'<circle cx="{ox+od*.5+(od*.5+11)*math.cos(a):.0f}"'
                f' cy="{oy+od*.5+(od*.5+11)*math.sin(a):.0f}" r="9" fill="#8a98a8"'
                f' stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, ill)
    # ЗИМНИЕ ЖИЛЬЦЫ
    for i in range(6):
        kx = 300 + (i % 3) * 120 + rnd.uniform(-20, 20)
        ky = 620 + (i // 3) * 90 + rnd.uniform(-20, 20)
        pl = 8 * A.w(t, 2.4, i * .25)
        s += SL(Z_SRED, f'<path d="M{kx-46:.0f},{ky:.0f} q{46:.0f},{-30:.0f} {92:.0f},0'
                        f' q{-46:.0f},{30:.0f} {-92:.0f},0 Z" fill="#b58a3a"'
                        f' stroke="{K}" stroke-width="3.4"/>'
                        f'<path d="M{kx+46:.0f},{ky:.0f} l{24+pl:.0f},{-16:.0f} l0,{32:.0f} Z"'
                        f' fill="#9a722c" stroke="{K}" stroke-width="3"/>'
                        f'<circle cx="{kx-28:.0f}" cy="{ky-4:.0f}" r="4.6" fill="{K}"/>')
    s += SL(Z_SRED, f'<path d="M620,860 q{150:.0f},{-40:.0f} {300:.0f},{-6:.0f}'
                    f' q{-140:.0f},{52:.0f} {-300:.0f},{6:.0f} Z" fill="#5f7a3a"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M920,854 l{50:.0f},{-26:.0f} l0,{52:.0f} Z" fill="#4a6a30"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="{664:.0f}" cy="{848:.0f}" r="6" fill="{K}"/>')
    for i in range(4):                 # коряги
        s += SL(Z_SRED, f'<path d="M{500+i*180:.0f},1070 q{40:.0f},{-120:.0f}'
                        f' {-10:.0f},{-200:.0f} q{60:.0f},{60:.0f} {90:.0f},{30:.0f}"'
                        f' fill="none" stroke="#54351f" stroke-width="13"/>')
    rak = 16 * A.ease(A.seg(t, .6, 1.6))
    s += SL(Z_SRED, f'<ellipse cx="{1700-rak:.0f}" cy="980" rx="54" ry="34"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{1650-rak:.0f},962 q{-40:.0f},{-20:.0f} {-60:.0f},{6:.0f}'
                    f' q{24:.0f},{16:.0f} {56:.0f},{10:.0f} Z" fill="#8a2f22"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{1650-rak:.0f},1000 q{-40:.0f},{20:.0f} {-62:.0f},{-2:.0f}'
                    f' q{26:.0f},{-18:.0f} {58:.0f},{-12:.0f} Z" fill="#8a2f22"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<rect x="0" y="1010" width="{W}" height="70" fill="#4a4038"/>'
                    f'<ellipse cx="1060" cy="1030" rx="70" ry="26" fill="#5f7a3a"'
                    f' opacity=".9" stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="1030" cy="1020" r="9" fill="#6f8c4a" stroke="{K}"'
                    f' stroke-width="2.6"/>'
                    f'<circle cx="1062" cy="1018" r="9" fill="#6f8c4a" stroke="{K}"'
                    f' stroke-width="2.6"/>')
    for i in range(16):
        d = ((t * .32 + i / 16.0) % 1.0)
        s += SL(Z_SRED, f'<circle cx="{120+i*118:.0f}" cy="{1000-560*d:.0f}"'
                        f' r="{4+7*d:.0f}" fill="#cfe4f5" opacity="{(1-d)*.55:.2f}"/>')
    s += SL(Z_SRED, kamysh(90, 300, 180, t, 6, 97, True)
            + kamysh(1880, 310, 200, t, 6, 101, True))
    s += SL(Z_PERED, f'<rect x="0" y="300" width="{W}" height="14" fill="#eaf6ff"'
                     f' opacity=".7"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def tropinka_v_obhod_pruda(t):
    """Пруд сверху: гладкая ледяная крыша, под ней ровно горят тёплые
    огоньки-окошки рыбьих домиков. По берегу дугой идёт натоптанная тропинка:
    баба с коромыслом и девочка с бидончиком обходят пруд. Следов на льду нет."""
    rnd = random.Random(1921)
    s = nebo("sumer", t, True, 103)
    s += SL(Z_DAL, ulica_dal(1100, 300, 820, t, True, 79))
    s += SL(Z_DAL, izba_snaruzhi(260, 320, 300, t, True, True, 31)
            + dym(290, 170, t, 6, .22, 250, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(360, 89, False))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="720" rx="760" ry="330" fill="url(#led)"'
                    f' stroke="#eaf6ff" stroke-width="10"/>')
    s += SL(Z_SRED, korka_lda(960, 720, 700, 300, t, .2, .0, .7, .3))
    # огоньки-окошки рыбьих домиков подо льдом
    for i in range(9):
        hx = 480 + (i % 5) * 220 + rnd.uniform(-30, 30)
        hy = 640 + (i // 5) * 130 + rnd.uniform(-20, 20)
        s += SL(Z_SRED, f'<path d="M{hx-50:.0f},{hy+40:.0f} l0,-56 l{50:.0f},{-40:.0f}'
                        f' l{50:.0f},{40:.0f} l0,{56:.0f} Z" fill="#3f5a6a"'
                        f' opacity=".85" stroke="#2b3f4a" stroke-width="4"/>'
                        f'<rect x="{hx-18:.0f}" y="{hy-10:.0f}" width="36" height="34"'
                        f' rx="4" fill="#ffd98a"'
                        f' opacity="{.65+.25*A.w(t,3.0,i*.3):.2f}"/>')
        s += SL(Z_SRED, teplo(hx, hy + 6, 90, 70, .25))
    # ТРОПИНКА дугой по берегу
    s += SL(Z_SRED, f'<path d="M-40,980 Q400,820 960,1060 Q1500,820 1960,960"'
                    f' fill="none" stroke="#8a7a62" stroke-width="80" opacity=".9"/>'
                    f'<path d="M-40,980 Q400,820 960,1060 Q1500,820 1960,960"'
                    f' fill="none" stroke="#6f6256" stroke-width="40" opacity=".7"/>')
    s += SL(Z_SRED, sledy_valenok(1880, 950, 1180, 1030, 8, 103, "#4a4038", 1.1))
    # БАБА с коромыслом и ДЕВОЧКА
    bx, by, bh = 1480, 1066, 640
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, tulup=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, 1, bh * .24, -36, t, "#4a3a52", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, -1, bh * .24, -34, t, "#4a3a52", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    kach = 6 * A.w(t, 1.3, .1)
    s += SL(Z_SRED, f'<path d="M{bx-230:.0f},{e1y-60:.0f} q{230:.0f},{-40:.0f}'
                    f' {460:.0f},0" fill="none" stroke="#8a6342" stroke-width="16"/>')
    for i, vx_ in enumerate((bx - 220, bx + 220)):
        s += SL(Z_SRED, f'<g transform="rotate({kach*(1 if i else -1):.1f} {vx_:.0f}'
                        f' {e1y-50:.0f})">'
                        f'<path d="M{vx_:.0f},{e1y-50:.0f} l0,{110:.0f}" stroke="#b9a37a"'
                        f' stroke-width="5" fill="none"/>'
                        f'<path d="M{vx_-40:.0f},{e1y+60:.0f} h80 l-8,86 h-64 Z"'
                        f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{vx_:.0f}" cy="{e1y+60:.0f}" rx="40" ry="12"'
                        f' fill="#8f979f" stroke="{K}" stroke-width="3.4"/></g>')
    dx, dy, dh = 1180, 1070, 400
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#6b4a5a", kant="#cfe4f5",
                           platok=True, ph=.8))
    r3, (e3x, e3y), _ = _ruka(dx, dy, dh, 1, dh * .26, 52, t, "#6b4a5a", "#cfe4f5", .3, 5)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x-22:.0f},{e3y+6:.0f} h44 l-5,56 h-34 Z"'
                         f' fill="#9aa3a8" stroke="{K}" stroke-width="3.6"/>'
                         f'<path d="M{e3x-22:.0f},{e3y+2:.0f} q{22:.0f},{-20:.0f}'
                         f' {44:.0f},0" fill="none" stroke="{CHUGUN}" stroke-width="4"/>')
    s += SL(Z_SRED, para_izo_rta(bx - 34, by - bh * .80, t, .3, 1.0, .5)
            + para_izo_rta(dx - 22, dy - dh * .80, t, .9, .8, .45))
    s += SL(Z_SRED, ten(bx, by + 4, 120, 20, .4) + ten(dx, dy + 4, 84, 15, .4))
    # собака бежит по тропинке
    beg = ((t * .5) % 1.0)
    sx_ = 1500 - 700 * beg
    s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="1000" rx="76" ry="38" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{sx_+66:.0f}" cy="962" r="30" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M{sx_+84:.0f},940 l{12:.0f},{-30:.0f} l{14:.0f},{28:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{sx_-70:.0f},986 q{-40:.0f},{-30:.0f} {-56:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#6b5230" stroke-width="9"/>'
                    f'<path d="M{sx_-40:.0f},1032 l-6,34 M{sx_+10:.0f},1038 l4,30'
                    f' M{sx_+54:.0f},1030 l8,34" stroke="#54351f" stroke-width="9"/>')
    # ивы, мостки, баня, поленница
    s += SL(Z_SRED, goloe_derevo_ld(180, 900, 420, t, 107, 7, True)
            + goloe_derevo_ld(1800, 930, 380, t, 109, 6, True))
    s += SL(Z_SRED, mostki(1420, 560, 380, t, True, 120))
    s += SL(Z_SRED, f'<rect x="60" y="560" width="260" height="150" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<circle cx="{78+(i%6)*46:.0f}" cy="{586+(i//6)*54:.0f}" r="22"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_LETIT, sneg_letit(t, 20, 37, .40, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def rybak_i_ledobur_u_steny(t):
    """Стена сарая: прислонён ледобур на пол-кадра, рядом удочки-коротышки,
    сачок, валенки с галошами. Рыбак берётся за ледобур и убирает руку, пока
    листки численника отлетают, а пруд за спиной белеет; потом берёт его."""
    rnd = random.Random(1922)
    s = nebo("den", t, False, 107)
    s += oblaka(t, 140, 5, 83, .42)
    # пруд за спиной белеет по ходу плана
    bel = A.ease(A.seg(t, 1.4, 4.4))
    s += SL(Z_DAL, f'<rect x="1180" y="420" width="740" height="300" fill="{VODA2}"/>')
    s += SL(Z_DAL, f'<rect x="1180" y="420" width="740" height="300" fill="url(#led)"'
                   f' opacity="{bel:.2f}"/>')
    s += SL(Z_DAL, f'<ellipse cx="1550" cy="560" rx="{320*bel:.0f}" ry="{90*bel:.0f}"'
                   f' fill="#eaf6ff" opacity="{.5*bel:.2f}"/>')
    s += SL(Z_DAL, kamysh(1240, 700, 170, t, 6, 113, True)
            + kamysh(1880, 712, 190, t, 6, 127, True))
    s += SL(Z_DAL, goloe_derevo_ld(1300, 740, 300, t, 113, 6, True))
    # СТЕНА САРАЯ
    s += SL(Z_SRED, doski(0, 180, 1180, 700, 72, True, "dosk"))
    s += SL(Z_SRED, f'<rect x="0" y="150" width="1180" height="40" fill="{DOSKA2}"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-20,150 q600,{-54:.0f} 1200,{-10:.0f} l0,20'
                    f' q-600,{-40:.0f} -1200,{10:.0f} Z" fill="url(#sneg)"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(880, 97, False))
    # ЛЕДОБУР у стены — главный предмет
    s += SL(Z_SRED, f'<g transform="rotate(-9 420 1000)">' + ledobur(420, 1000, 1.9, t, .1)
            + '</g>')
    # удочки, сачок, валенки с галошами
    for i, ux in enumerate((640, 700, 758)):
        s += SL(Z_SRED, f'<g transform="rotate({-13+i*4} {ux:.0f} 1000)">'
                        f'<rect x="{ux:.0f}" y="640" width="13" height="360" rx="6"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>'
                        f'<circle cx="{ux+6:.0f}" cy="700" r="12" fill="none"'
                        f' stroke="{ZHELEZ}" stroke-width="4"/>'
                        f'<path d="M{ux+6:.0f},640 q{30:.0f},{60:.0f} {12:.0f},{150:.0f}"'
                        f' fill="none" stroke="#cfd6db" stroke-width="2.4"/></g>')
    s += SL(Z_SRED, f'<g transform="rotate(14 900 1000)">'
                    f'<rect x="894" y="700" width="14" height="300" rx="6" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<ellipse cx="901" cy="672" rx="74" ry="48" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="8"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M{840+i*25:.0f},648 q{18:.0f},{40:.0f} {4:.0f},{66:.0f}"'
                        f' fill="none" stroke="#b9c2c8" stroke-width="2.4" opacity=".8"/>')
    s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, _valenok(1020, 1040, .9, -3) + _valenok(1100, 1044, .9, 5)
            + f'<ellipse cx="1020" cy="1046" rx="44" ry="16" fill="#23242a"'
              f' stroke="{K}" stroke-width="3.4"/>'
              f'<ellipse cx="1100" cy="1050" rx="44" ry="16" fill="#23242a"'
              f' stroke="{K}" stroke-width="3.4"/>')
    # ЧИСЛЕННИК на стене: листки отлетают (цифр не рисуем — только листки)
    s += SL(Z_SRED, f'<rect x="150" y="300" width="190" height="240" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="150" y="300" width="190" height="46" rx="8"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    for i in range(4):
        d = ((t * .5 + i * .25) % 1.0)
        s += SL(Z_LETIT, f'<rect x="{200+260*d:.0f}" y="{360+300*d*d:.0f}" width="120"'
                         f' height="150" rx="6" fill="#f2ead6" opacity="{(1-d)*.9:.2f}"'
                         f' transform="rotate({d*120:.0f} {260+260*d:.0f} {430+300*d*d:.0f})"'
                         f' stroke="{K}" stroke-width="3"/>')
    # РЫБАК: правая берётся за ледобур и убирает, левая рвёт листок
    ryx, ryy, ryh = 760, 1060, 660
    hvat = A.ease(A.seg(t, .6, .8)) - A.ease(A.seg(t, 1.8, .8)) + A.ease(A.seg(t, 5.6, .9))
    s += SL(Z_SRED, figura(ryx, ryy, ryh, t, col="#3f4a3a", kant="#ffd9a8",
                           shapka=True, tulup=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(ryx, ryy, ryh, -1, ryh * .32, 10 + 24 * hvat, t,
                              "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ryx, ryy, ryh, 1, ryh * .26, -22, t,
                              "#3f4a3a", "#ffd9a8", .7, 5)
    s += SL(Z_SRED, r1 + varezhka(e1x - 10, e1y + 10, 1.0, -16, "#5a4a3a", t, .2) + r2)
    s += SL(Z_SRED, para_izo_rta(ryx - 36, ryy - ryh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(ryx, ryy + 6, 130, 22, .45))
    s += SL(Z_SRED, dvorovye_veschi(1280, 1066, 420, t, 101, ["kadka", "vedro", "korzina"]))
    s += SL(Z_SRED, yaschik_rybaka(1500, 1040, .9, t, .25, .3))
    s += SL(Z_SRED, inej_mel(97, 46, 920, 1070))
    s += SL(Z_SRED, lampa(120, 240, t, 1.1, False) + teplo(120, 250, 190, 160, .35))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def doroga_v_shkolu_i_luzha(t):
    """Мостик в память: утренняя улица шестидесятых — забор, фонарный столб,
    тополь, почтовый ящик, вдали школа. Школьник с портфелем наступает
    каблуком на замёрзшую лужу: её овал — проём с настоящим треснувшим льдом."""
    rnd = random.Random(1923)
    s = nebo("rassv", t, False, 109)
    s += oblaka(t, 150, 5, 89, .40)
    s += SL(Z_DAL, panelka(1280, 560, 620, t, 5, True, 7))
    s += SL(Z_DAL, f'<rect x="120" y="330" width="760" height="260" rx="8"'
                   f' fill="#d8cbb0" stroke="{K}" stroke-width="6"/>')
    for i in range(10):
        s += SL(Z_DAL, f'<rect x="{160+i*70:.0f}" y="370" width="44" height="76" rx="5"'
                       f' fill="#8aa8b4" stroke="{K}" stroke-width="3.4"'
                       f' opacity="{.75+.2*A.w(t,4.0,i*.3):.2f}"/>')
    s += SL(Z_DAL, f'<rect x="420" y="268" width="170" height="64" rx="6"'
                   f' fill="#b9a082" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_DAL, goloe_derevo_ld(1000, 640, 520, t, 127, 8, False))
    s += SL(Z_SRED, zabor_shtaket(-40, 600, 1000, 200, 103, 60, "url(#derev)", False))
    s += SL(Z_SRED, f'<rect x="1140" y="300" width="22" height="520" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1150,300 q{40:.0f},{-30:.0f} {80:.0f},{-4:.0f}"'
                    f' fill="none" stroke="{BETON2}" stroke-width="12"/>')
    s += SL(Z_SRED, lampa(1232, 300, t, 1.2, True) + teplo(1232, 310, 220, 180, .35))
    s += SL(Z_SRED, f'<rect x="1500" y="640" width="120" height="150" rx="10"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1520" y="676" width="80" height="16" rx="4"'
                    f' fill="#2b2016"/>'
                    f'<rect x="1546" y="790" width="24" height="120" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(800, 113, False))
    s += SL(Z_SRED, f'<rect x="0" y="820" width="{W}" height="90" fill="#8a8078"'
                    f' opacity=".85"/>')
    # ЛУЖА-ПРОЁМ: вид, метка, кромка поверх
    lx, ly, lw, lh = 820, 700, 480, 360
    luzha = (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.54:.0f}"'
             f' ry="{lh*.52:.0f}" fill="#2f4a52"/>')
    luzha += korka_lda(lx + lw * .5, ly + lh * .5, lw * .48, lh * .46, t, .3, .0, .8)
    luzha += mesto_stoka(lx, ly, lw, lh, "ellips")
    luzha += (f'<ellipse cx="{lx+lw*.5:.0f}" cy="{ly+lh*.5:.0f}" rx="{lw*.56:.0f}"'
              f' ry="{lh*.54:.0f}" fill="none" stroke="#6f6256" stroke-width="18"'
              f' opacity=".9"/>')
    s += SL(Z_SRED, luzha)
    # белые лучи разбегаются по льду от каблука
    luch_ = A.ease(A.seg(t, 1.0, .9))
    if luch_ > .02:
        s += SL(Z_PERED, treschina(lx + lw * .46, ly + lh * .40, 240 * luch_, 131, 6,
                                   "#ffffff", 5.0))
    # ШКОЛЬНИК: портфель в правой, левая в кармане, каблук на лужу
    shx, shy, shh = 660, 1040, 650
    nast = A.ease(A.seg(t, .5, .8))
    s += SL(Z_SRED, figura(shx, shy, shh, t, col="#6f6256", kant="#ffd9a8",
                           shapka=True, ph=.2, naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(shx, shy, shh, 1, shh * .28, 50, t, "#6f6256", "#ffd9a8", .2, 6)
    s += SL(Z_SRED, r1)
    kach = 7 * A.w(t, 1.1, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-60:.0f}" y="{e1y+10:.0f}" width="120" height="86"'
                    f' rx="10" fill="#6b4428" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{e1x-60:.0f},{e1y+40:.0f} h120" stroke="#54351f"'
                    f' stroke-width="6"/>'
                    f'<rect x="{e1x-16:.0f}" y="{e1y+32:.0f}" width="32" height="20"'
                    f' rx="4" fill="{MED}" stroke="{K}" stroke-width="2.6"/></g>')
    s += SL(Z_SRED, f'<path d="M{shx+70:.0f},{shy-120:.0f} q{60*nast:.0f},{40*nast:.0f}'
                    f' {140*nast:.0f},{66*nast:.0f}" fill="none" stroke="#6f6256"'
                    f' stroke-width="30" stroke-linecap="round"/>'
            + _valenok(shx + 210 * nast, shy - 40 + 36 * nast, .60, 20))
    s += SL(Z_SRED, para_izo_rta(shx - 32, shy - shh * .80, t, .4, .9, .5))
    s += SL(Z_SRED, ten(shx, shy + 6, 120, 20, .4))
    # голуби взлетают, скамейка, дворник-силуэт
    for i in range(4):
        vzl = A.ease(A.seg(t, 1.1 + i * .1, 1.0))
        gx = 1360 + i * 90 + 70 * vzl
        gy = 1000 - 260 * vzl
        s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="28" ry="18"'
                        f' fill="#9aa3a8" stroke="{K}" stroke-width="3"/>'
                        f'<circle cx="{gx+22:.0f}" cy="{gy-12:.0f}" r="12" fill="#9aa3a8"'
                        f' stroke="{K}" stroke-width="2.6"/>'
                        f'<path d="M{gx-4:.0f},{gy-6:.0f} q{18:.0f},{-26-20*vzl:.0f}'
                        f' {44:.0f},{-12:.0f}" fill="none" stroke="#cfd6de"'
                        f' stroke-width="10"/>')
    s += SL(Z_SRED, f'<rect x="120" y="920" width="300" height="20" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="140" y="940" width="20" height="90" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="380" y="940" width="20" height="90" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    dvx, dvy, dvh = 1760, 1050, 520
    s += SL(Z_SRED, figura(dvx, dvy, dvh, t, col="#4a4450", kant="#cfe4f5",
                           shapka=True, ph=.8))
    r2, (e2x, e2y), _ = _ruka(dvx, dvy, dvh, -1, dvh * .30, 40, t, "#4a4450", "#cfe4f5", .5, 6)
    s += SL(Z_SRED, r2 + f'<path d="M{e2x:.0f},{e2y:.0f} l{-120:.0f},{150:.0f}"'
                         f' stroke="#8a6342" stroke-width="10"/>')
    for i in range(8):
        s += SL(Z_SRED, f'<path d="M{e2x-120:.0f},{e2y+150:.0f} l{-30+i*8:.0f},{40:.0f}"'
                        f' stroke="#9a7c45" stroke-width="4" opacity=".9"/>')
    s += SL(Z_SRED, inej_mel(109, 40, 900, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def okrik_iz_okna(t):
    """Окно первого этажа с распахнутой створкой и столетником: бабушка
    высунулась по пояс и грозит свёрнутым полотенцем. Школьник у лужи
    оглядывается, втянув голову, мокрый ботинок тянет тёмный след."""
    rnd = random.Random(1924)
    s = nebo("rassv", t, False, 113)
    s += SL(Z_DAL, oblaka(t, 140, 4, 97, .36))
    # СТЕНА ДОМА во весь кадр с окном
    s += SL(Z_SRED, f'<rect x="0" y="0" width="{W}" height="760" fill="{BETON}"/>')
    for i in range(10):
        s += SL(Z_SRED, f'<path d="M0,{70+i*70:.0f} h{W}" stroke="{BETON2}"'
                        f' stroke-width="4" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="0" y="700" width="{W}" height="80" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="5"/>')
    ox, oy, ow, oh = 420, 180, 620, 500
    s += SL(Z_SRED, f'<rect x="{ox-30:.0f}" y="{oy-30:.0f}" width="{ow+60:.0f}"'
                    f' height="{oh+60:.0f}" rx="8" fill="#d8cbb0" stroke="{K}"'
                    f' stroke-width="6"/>'
                    f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="{ox+ow*.5:.0f}" y="{oy:.0f}" width="{ow*.5:.0f}"'
                    f' height="{oh:.0f}" fill="#9fc4d8" opacity=".55"'
                    f' transform="skewY(-6)" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="{ox-40:.0f}" y="{oy+oh:.0f}" width="{ow+80:.0f}"'
                    f' height="30" rx="5" fill="#e4d8bd" stroke="{K}" stroke-width="5"/>')
    # столетник на подоконнике
    s += SL(Z_SRED, f'<path d="M{ox+40:.0f},{oy+oh:.0f} h100 l-12,-70 h-76 Z"'
                    f' fill="#a8743c" stroke="{K}" stroke-width="4"/>')
    for i in range(6):
        a = -1.2 + i * .42
        s += SL(Z_SRED, f'<path d="M{ox+90:.0f},{oy+oh-66:.0f}'
                        f' q{40*math.sin(a):.0f},{-70:.0f} {70*math.sin(a):.0f},{-130:.0f}'
                        f' q{14:.0f},{30:.0f} {-26*math.sin(a):.0f},{130:.0f} Z"'
                        f' fill="#56763f" stroke="{K}" stroke-width="3.4"/>')
    # БАБУШКА высунулась по пояс и грозит полотенцем
    bx, by, bh = 760, oy + oh + 10, 560
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#8a2f22", kant="#ffd9a8",
                           platok=True, ph=.2))
    groz = A.w(t, .8, .0)
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, 1, bh * .30, -40 + 26 * groz, t,
                              "#8a2f22", "#ffd9a8", .2, 10)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, -1, bh * .24, 30, t, "#8a2f22", "#ffd9a8", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<g transform="rotate({-24+20*groz:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-16:.0f}" y="{e1y-10:.0f}" width="190" height="34"'
                    f' rx="16" fill="{RUSH}" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e1x+60:.0f},{e1y-10:.0f} v34 M{e1x+120:.0f},{e1y-10:.0f}'
                    f' v34" stroke="{TKAN}" stroke-width="6"/></g>')
    # СТЕНА ОБЖИТА: второе окно, водосточная труба, кусты, санки, ящик
    s += SL(Z_SRED, f'<rect x="1180" y="210" width="330" height="300" rx="6"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1150" y="180" width="390" height="34" rx="6"'
                    f' fill="#d8cbb0" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1180" y="210" width="330" height="300" fill="#9fc4d8"'
                    f' opacity=".35"/>'
                    f'<path d="M1345,210 v300 M1180,360 h330" stroke="#e4d8bd"'
                    f' stroke-width="12"/>'
                    f'<rect x="1150" y="510" width="390" height="26" rx="5"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<ellipse cx="1260" cy="420" rx="52" ry="40" fill="#56763f"'
                    f' opacity=".9" stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="1230" y="452" width="62" height="58" rx="6"'
                    f' fill="#a8743c" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<rect x="1620" y="0" width="40" height="780" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="1612" y="{90+i*130:.0f}" width="56" height="18"'
                        f' rx="4" fill="#8a8078" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M1620,780 q{-10:.0f},{40:.0f} {-46:.0f},{54:.0f}'
                    f' l{40:.0f},{20:.0f} q{40:.0f},{-26:.0f} {46:.0f},{-74:.0f} Z"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="4"/>')
    for i, (kx, kb, kh) in enumerate(((1100, 840, 180), (1290, 850, 150))):
        s += SL(Z_SRED, goloe_derevo_ld(kx, kb, kh, t, 131 + i, 5, True))
    s += SL(Z_SRED, sanki_derev(1180, 940, .74, t, .6, True))
    s += SL(Z_SRED, f'<rect x="1340" y="840" width="150" height="100" rx="8"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M1340,876 h150" stroke="#54351f" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="1690" y="300" width="170" height="220" rx="6"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M1710,{340+i*30:.0f} q{40:.0f},{-6:.0f} {80:.0f},0'
                        f' q{30:.0f},{6:.0f} {50:.0f},{-2:.0f}" fill="none"'
                        f' stroke="#8a7a62" stroke-width="4" opacity=".8"/>')
    # ШКОЛЬНИК оглядывается, портфель к груди, мокрый след
    shx, shy, shh = 1480, 1050, 620
    s += SL(Z_SRED, figura(shx, shy, shh, t, col="#6f6256", kant="#ffd9a8",
                           shapka=True, ph=.5, naklon=3.0))
    r3, (e3x, e3y), _ = _ruka(shx, shy, shh, -1, shh * .22, 16, t, "#6f6256", "#ffd9a8", .3, 4)
    r4, (e4x, e4y), _ = _ruka(shx, shy, shh, 1, shh * .20, 20, t, "#6f6256", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r3 + r4
            + f'<rect x="{shx-70:.0f}" y="{shy-shh*.52:.0f}" width="140" height="100"'
              f' rx="10" fill="#6b4428" stroke="{K}" stroke-width="4.5"/>'
              f'<path d="M{shx-70:.0f},{shy-shh*.52+34:.0f} h140" stroke="#54351f"'
              f' stroke-width="6"/>')
    s += SL(Z_SRED, para_izo_rta(shx - 34, shy - shh * .80, t, .5, 1.0, .5))
    # мокрый след за ботинком
    for i in range(6):
        s += SL(Z_SRED, f'<ellipse cx="{1700-i*86:.0f}" cy="{1056+((i*3)%2)*14:.0f}"'
                        f' rx="{40-i*4:.0f}" ry="{15-i:.0f}" fill="#4a4038"'
                        f' opacity="{.65-i*.08:.2f}"/>')
    s += SL(Z_SRED, f'<ellipse cx="1180" cy="1010" rx="220" ry="62" fill="#2f4a52"'
                    f' opacity=".9"/>' + korka_lda(1180, 1008, 200, 54, t, .2, .6, .85))
    # завалинка, кошка прячется, бельевая верёвка, скамейка
    s += SL(Z_SRED, f'<rect x="0" y="780" width="{W}" height="60" rx="8" fill="#8a6342"'
                    f' stroke="{K}" stroke-width="5"/>')
    pryach = A.ease(A.seg(t, .9, 1.0))
    s += SL(Z_SRED, kot(330 - 120 * pryach, 780, t, 1.5, "#4a423a", False))
    s += SL(Z_SRED, f'<path d="M60,420 q400,{40:.0f} 320,{-120:.0f}" fill="none"'
                    f' stroke="#b9a37a" stroke-width="4"/>')
    for i, (px_, pw_) in enumerate(((120, 90), (240, 70), (330, 60))):
        kch = 5 * A.w(t, 2.2, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {px_+pw_*.5:.0f} 430)">'
                        f'<rect x="{px_:.0f}" y="430" width="{pw_:.0f}" height="130"'
                        f' rx="5" fill="{["#e8e2d6","#8aa8b4","#d6a63f"][i]}"'
                        f' stroke="{K}" stroke-width="3.6"/></g>')
    s += SL(Z_SRED, f'<rect x="1540" y="820" width="320" height="20" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1560" y="840" width="20" height="80" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<rect x="1820" y="840" width="20" height="80" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, dvorovye_veschi(140, 1066, 360, t, 113, ["vedro", "churbak", "metla"]))
    s += SL(Z_SRED, inej_mel(127, 40, 860, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def dvor_i_netronutaya_luzha(t):
    """Двор между двухэтажными домами: посреди гладкая нетронутая лужа на
    пол-кадра, вокруг кружком стоят пятеро детей — руки в карманах и за
    спиной, каждый косится на соседа. Самый маленький делает полшага."""
    rnd = random.Random(1925)
    s = nebo("den", t, False, 131)
    s += oblaka(t, 140, 5, 101, .42)
    s += SL(Z_DAL, f'<rect x="-20" y="150" width="900" height="520" rx="6"'
                   f' fill="#c3ab8a" stroke="{K}" stroke-width="6"/>'
                   f'<rect x="1020" y="190" width="920" height="490" rx="6"'
                   f' fill="#b9a082" stroke="{K}" stroke-width="6"/>')
    for i in range(16):
        dx_ = 20 + (i % 8) * 108; dy_ = 220 + (i // 8) * 220
        s += SL(Z_DAL, f'<rect x="{dx_:.0f}" y="{dy_:.0f}" width="66" height="96" rx="5"'
                       f' fill="#8aa8b4" stroke="{K}" stroke-width="3.4"'
                       f' opacity="{.7+.25*A.w(t,4.0,i*.27):.2f}"/>')
        s += SL(Z_DAL, f'<rect x="{1060+(i%8)*108:.0f}" y="{dy_+30:.0f}" width="64"'
                       f' height="92" rx="5" fill="#8aa8b4" stroke="{K}"'
                       f' stroke-width="3.4" opacity="{.7+.25*A.w(t,3.6,i*.31):.2f}"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(680, 137, False))
    # ЛУЖА на пол-кадра, гладкая и нетронутая
    s += SL(Z_SRED, f'<ellipse cx="960" cy="880" rx="520" ry="170" fill="#2f4a52"/>')
    s += SL(Z_SRED, korka_lda(960, 876, 490, 150, t, .1, .0, .95))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="880" rx="528" ry="176" fill="none"'
                    f' stroke="#6b5438" stroke-width="20" opacity=".85"/>')
    # ПЯТЕРО ДЕТЕЙ кружком
    deti = ((300, 1016, 430, "#8a2f22"), (560, 1060, 400, "#3f5a6a"),
            (1380, 1054, 420, "#6b3a6a"), (1640, 1010, 440, "#4a6a3a"),
            (960, 1076, 330, "#c8301f"))
    for i, (dx_, dy_, dh_, col) in enumerate(deti):
        shag = A.ease(A.seg(t, 1.2, 1.0)) if i == 4 else .0
        s += SL(Z_SRED, figura(dx_, dy_ - 10 * shag, dh_, t, col=col, kant="#ffd9a8",
                               shapka=True, ph=i * .3, naklon=1.5))
        rk, (ex, ey), _ = _ruka(dx_, dy_, dh_, 1 if i % 2 else -1, dh_ * .22,
                                48, t, col, "#ffd9a8", i * .2, 4)
        s += SL(Z_SRED, rk)
        s += SL(Z_SRED, para_izo_rta(dx_ - 22, dy_ - dh_ * .80, t, i * .3, .8, .45))
        s += SL(Z_SRED, ten(dx_, dy_ + 5, 80, 14, .35))
    s += SL(Z_SRED, f'<circle cx="960" cy="{1070-330-46:.0f}" r="16" fill="{RUSH}"'
                    f' stroke="{K}" stroke-width="3"/>')
    # песочница в инее, бельевые столбы, сарай, качели, кот на заборе
    s += SL(Z_SRED, f'<rect x="60" y="820" width="300" height="130" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="80" y="800" width="260" height="30" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="210" cy="860" rx="120" ry="34" fill="#d8cbb0"'
                    f' opacity=".9"/>')
    for i, px_ in enumerate((1640, 1840)):
        s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="640" width="24" height="330"'
                        f' fill="{BETON2}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M1652,660 q100,{40:.0f} 200,{-10:.0f}" fill="none"'
                    f' stroke="#b9a37a" stroke-width="4"/>')
    for i, (px_, pw_, col) in enumerate(((1670, 70, "#e8e2d6"), (1760, 60, "#8aa8b4"))):
        kch = 6 * A.w(t, 2.4, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {px_+pw_*.5:.0f} 672)">'
                        f'<rect x="{px_:.0f}" y="672" width="{pw_:.0f}" height="120"'
                        f' rx="5" fill="{col}" stroke="{K}" stroke-width="3.4"/></g>')
    s += SL(Z_SRED, f'<rect x="1380" y="690" width="60" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1386,690 l-6,-120 M1434,690 l6,-120" stroke="#6b5230"'
                    f' stroke-width="5"/>')
    s += SL(Z_SRED, zabor_shtaket(-40, 700, 420, 150, 139, 58))
    s += SL(Z_SRED, kot(180, 700, t, 1.3, "#4a423a", False))
    s += SL(Z_SRED, dym(1500, 240, t, 6, .22, 260, .38, "#d7dee6", 1.0))
    s += SL(Z_SRED, inej_mel(137, 50, 940, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 14, 41, .32, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def ldinka_protiv_solnca(t):
    """Девочка держит перед лицом большую льдинку обеими варежками и смотрит
    сквозь неё на солнце: льдинка — круглый проём с настоящим кадром. Над
    ней по словам встают три значка: след, ухо, льдинка с солнцем."""
    rnd = random.Random(1926)
    s = nebo("rassv", t, False, 139)
    s += oblaka(t, 150, 4, 103, .34, "#ffe9c8")
    s += SL(Z_NEBO, f'<circle cx="1480" cy="230" r="120" fill="#ffe9ac" opacity=".45"/>'
                    f'<circle cx="1480" cy="230" r="68" fill="#fff4d8" opacity=".9"/>')
    s += SL(Z_DAL, zabor_shtaket(-40, 420, 2000, 230, 149, 62))
    s += SL(Z_DAL, goloe_derevo_ld(300, 660, 420, t, 151, 7, True))
    s += SL(Z_DAL, izba_snaruzhi(1660, 650, 280, t, True, True, 37)
            + dym(1690, 500, t, 6, .22, 240, .40, "#d7dee6", .9))
    s += SL(Z_SRED, _merzlaya_zemlya(650, 149, True))
    # проломленная лужа рядом, воробьи
    s += SL(Z_SRED, f'<ellipse cx="420" cy="980" rx="250" ry="80" fill="#2f4a52"/>'
            + korka_lda(420, 978, 230, 70, t, .4, .85))
    for i, (vx, vy) in enumerate(((620, 940), (700, 980), (760, 920))):
        s += SL(Z_SRED, ptica(vx, vy, t, 1.4, "#8a7a62", i * .3, "#6f6256"))
    # ДЕВОЧКА с льдинкой: проём-круг 420 по центру
    dx, dy, dh = 1060, 1066, 700
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#8a2f22", kant="#ffd9a8",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, 1, dh * .28, -42, t, "#8a2f22", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, -1, dh * .28, -46, t, "#8a2f22", "#ffd9a8", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    lx, ly, ld = dx - 210, dy - dh * .95, 420
    put = kontur_proema(lx, ly, ld, ld, "ellips")
    ldin = (f'<path d="{put}" fill="#9fc4d8"/>')
    ldin += (f'<path d="{put}" fill="#eaf6ff" opacity=".45"/>')
    ldin += mesto_stoka(lx, ly, ld, ld, "ellips")
    ldin += (f'<circle cx="{lx+ld*.5:.0f}" cy="{ly+ld*.5:.0f}" r="{ld*.5:.0f}"'
             f' fill="none" stroke="#dcecf8" stroke-width="18" opacity=".9"/>')
    ldin += (f'<path d="M{lx+40:.0f},{ly+ld*.78:.0f} q{ld*.26:.0f},{-26:.0f}'
             f' {ld*.5:.0f},{-6:.0f}" fill="none" stroke="#ffffff" stroke-width="10"'
             f' opacity=".45"/>')
    s += SL(Z_SRED, ldin)
    s += SL(Z_SRED, varezhka(e1x + 6, e1y + 10, 1.1, 16, TKAN, t, .2)
            + varezhka(e2x - 6, e2y + 10, 1.1, -16, TKAN, t, .6))
    s += SL(Z_SRED, _valenok(dx - 54, dy, .64, -3) + _valenok(dx + 36, dy + 4, .64, 4))
    s += SL(Z_SRED, para_izo_rta(dx - 30, dy - dh * .74, t, .5, .9, .45))
    s += SL(Z_SRED, ten(dx, dy + 6, 130, 22, .45))
    # ТРИ ЗНАЧКА встают по словам: след, ухо, льдинка с солнцем
    for i, zx in enumerate((300, 560, 820)):
        vst = A.out(A.seg(t, .6 + i * .5, .6))
        if vst < .02:
            continue
        zy = 300
        s += SL(Z_SRED, f'<g opacity="{vst:.2f}" transform="translate(0,{40*(1-vst):.0f})">'
                        f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="86" fill="#f2ead6"'
                        f' stroke="{K}" stroke-width="5"/>')
        if i == 0:
            s += SL(Z_SRED, f'<ellipse cx="{zx:.0f}" cy="{zy+14:.0f}" rx="34" ry="20"'
                            f' fill="#4a3526"/>'
                            f'<ellipse cx="{zx:.0f}" cy="{zy-18:.0f}" rx="26" ry="16"'
                            f' fill="#4a3526"/>')
        elif i == 1:
            s += SL(Z_SRED, f'<path d="M{zx-20:.0f},{zy+40:.0f} q{-40:.0f},{-60:.0f}'
                            f' {10:.0f},{-80:.0f} q{50:.0f},{-20:.0f} {50:.0f},{30:.0f}'
                            f' q0,{30:.0f} {-26:.0f},{30:.0f}" fill="none" stroke="#8a5a3a"'
                            f' stroke-width="11"/>')
        else:
            s += SL(Z_SRED, f'<path d="M{zx-40:.0f},{zy+30:.0f} l{14:.0f},{-80:.0f}'
                            f' l{56:.0f},{-6:.0f} l{14:.0f},{86:.0f} Z" fill="#cfe4f5"'
                            f' stroke="#eaf6ff" stroke-width="5"/>'
                            f'<circle cx="{zx+4:.0f}" cy="{zy-10:.0f}" r="18"'
                            f' fill="#ffe9ac" opacity=".9"/>')
        s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, ryabina(1820, 940, t, 1.4, 6)
            + kalina_grozd(1850, 880, t, 1.0, 11, 157, .4))
    s += SL(Z_SRED, dvorovye_veschi(120, 1066, 340, t, 149, ["vedro", "korzina"]))
    s += SL(Z_SRED, inej_mel(151, 46, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def babushka_rasskazyvaet_vnuku_u_luzh(t):
    """Дорожка у подъезда: внук уже поднял ногу над лужей, бабушка приседает
    рядом и показывает на лёд. Над ними всплывает рисованная картинка —
    пруд в разрезе со спящими рыбами; внук опускает ногу и слушает."""
    rnd = random.Random(1927)
    s = nebo("den", t, False, 151)
    s += oblaka(t, 140, 5, 107, .40)
    s += SL(Z_DAL, panelka(60, 520, 820, t, 5, True, 11))
    s += SL(Z_DAL, panelka(1140, 540, 760, t, 4, True, 13))
    s += SL(Z_SRED, _merzlaya_zemlya(620, 157, False))
    s += SL(Z_SRED, f'<rect x="0" y="700" width="{W}" height="140" fill="#9aa3a8"'
                    f' opacity=".85"/>'
                    f'<path d="M0,700 h{W}" stroke="#8a8078" stroke-width="7"/>')
    # ЛУЖА
    s += SL(Z_SRED, f'<ellipse cx="760" cy="900" rx="330" ry="110" fill="#2f4a52"/>'
            + korka_lda(760, 898, 310, 100, t, .2, .0, .9))
    # КАРТИНКА-ВСПЛЫВАШКА: пруд в разрезе со спящими рыбами
    vsp = A.out(A.seg(t, 1.4, 1.2))
    if vsp > .02:
        kx, ky, kw, kh = 1180, 180, 620, 380
        s += SL(Z_SRED, f'<g opacity="{vsp:.2f}" transform="translate(0,{60*(1-vsp):.0f})">'
                        f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw:.0f}" height="{kh:.0f}"'
                        f' rx="14" fill="#cfe4f5" stroke="{K}" stroke-width="6"/>'
                        f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw:.0f}" height="{kh*.22:.0f}"'
                        f' fill="url(#led)"/>'
                        f'<rect x="{kx:.0f}" y="{ky+kh*.22:.0f}" width="{kw:.0f}"'
                        f' height="{kh*.78:.0f}" fill="{VODA}"/>')
        for i in range(5):
            fx = kx + 90 + (i % 3) * 170; fy = ky + 140 + (i // 3) * 110
            s += SL(Z_SRED, f'<path d="M{fx-36:.0f},{fy:.0f} q{36:.0f},{-22:.0f} {72:.0f},0'
                            f' q{-36:.0f},{22:.0f} {-72:.0f},0 Z" fill="#b58a3a"'
                            f' stroke="{K}" stroke-width="3"/>'
                            f'<circle cx="{fx-20:.0f}" cy="{fy-3:.0f}" r="3.6" fill="{K}"/>')
        s += SL(Z_SRED, f'<path d="M{kx+40:.0f},{ky+kh-30:.0f} q{kw*.5:.0f},{-40:.0f}'
                        f' {kw-80:.0f},{-10:.0f}" fill="none" stroke="#2f6b5a"'
                        f' stroke-width="9"/></g>')
    # ВНУК опускает ногу, БАБУШКА на корточках показывает
    opusk = A.ease(A.seg(t, 2.0, 1.2))
    vx, vy, vh = 840, 1040, 480
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#c8301f", kant="#ffd9a8",
                           shapka=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(vx, vy, vh, 1, vh * .26, -30 + 40 * opusk, t,
                              "#c8301f", "#ffd9a8", .2, 6)
    r2, (e2x, e2y), _ = _ruka(vx, vy, vh, -1, vh * .26, -26 + 36 * opusk, t,
                              "#c8301f", "#ffd9a8", .6, 6)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{vx+50:.0f},{vy-130:.0f} q{50*(1-opusk):.0f},{-60*(1-opusk):.0f}'
                    f' {110*(1-opusk):.0f},{-40*(1-opusk)+70*opusk:.0f}" fill="none"'
                    f' stroke="#c8301f" stroke-width="26" stroke-linecap="round"/>'
            + _valenok(vx + 160 * (1 - opusk) + 40 * opusk,
                       vy - 120 * (1 - opusk) + 110 * opusk, .58, 14))
    bx, by, bh = 540, 1056, 430
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd9a8",
                           platok=True, ph=.5, naklon=2.0))
    r3, (e3x, e3y), _ = _ruka(bx, by, bh, 1, bh * .40, 4, t, "#4a3a52", "#ffd9a8", .3, 4)
    r4, (e4x, e4y), _ = _ruka(bx, by, bh, -1, bh * .30, 28, t, "#4a3a52", "#ffd9a8", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, f'<path d="M{e4x:.0f},{e4y:.0f} L{vx-60:.0f},{vy-vh*.58:.0f}"'
                    f' stroke="#4a3a52" stroke-width="14" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(vx - 26, vy - vh * .80, t, .3, .8, .45)
            + para_izo_rta(bx - 26, by - bh * .80, t, .8, .9, .45))
    s += SL(Z_SRED, ten(vx, vy + 6, 100, 18, .4) + ten(bx, by + 6, 120, 20, .4))
    # скамейка, клумба в инее, урна, голуби
    s += SL(Z_SRED, f'<rect x="140" y="860" width="340" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="140" y="800" width="340" height="20" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="160" y="882" width="22" height="110" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="440" y="882" width="22" height="110" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<path d="M1300,1070 q{40:.0f},{-110:.0f} {170:.0f},{-104:.0f}'
                    f' q{130:.0f},{10:.0f} {160:.0f},{104:.0f} Z" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="5"/>')
    for i in range(7):
        s += SL(Z_SRED, _trava_suhaya(rnd, 1, 930, 980, 1340 + i * 50, 1380 + i * 50))
    s += SL(Z_SRED, f'<rect x="1700" y="900" width="110" height="140" rx="10"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="1690" y="884" width="130" height="22" rx="6"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="3.6"/>')
    for i, (gx, gy) in enumerate(((240, 1020), (330, 1046), (430, 1010))):
        s += SL(Z_SRED, ptica(gx, gy, t, 1.6, "#9aa3a8", i * .3, "#6f7a84"))
    s += SL(Z_SRED, inej_mel(157, 44, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def varezhka_stuchit_po_korke(t):
    """Та же лужа крупно, корка с вмёрзшим листом: внук на корточках легонько
    стучит по ней варежкой и наклоняет ухо, от каждого стука расходятся
    рисованные звуковые колечки. Бабушкин рукав рядом показывает «тише»."""
    rnd = random.Random(1928)
    s = nebo("den", t, False, 163)
    s += SL(Z_DAL, panelka(1280, 420, 640, t, 4, True, 17))
    s += SL(Z_DAL, zabor_shtaket(-40, 380, 1100, 170, 163, 60))
    s += SL(Z_SRED, _merzlaya_zemlya(520, 167, False))
    s += SL(Z_SRED, f'<rect x="0" y="640" width="{W}" height="60" fill="#9aa3a8"'
                    f' stroke="{K}" stroke-width="5"/>')
    # ЛУЖА КРУПНО с вмёрзшим листом
    s += SL(Z_SRED, f'<ellipse cx="880" cy="870" rx="640" ry="210" fill="#2f4a52"/>')
    s += SL(Z_SRED, korka_lda(880, 866, 600, 190, t, .2, .0, .95))
    s += SL(Z_SRED, f'<path d="M700,900 l{48:.0f},{-36:.0f} l{-10:.0f},{36:.0f}'
                    f' l{50:.0f},{-10:.0f} l{-36:.0f},{34:.0f} l{32:.0f},{24:.0f}'
                    f' l{-50:.0f},{4:.0f} l{-6:.0f},{36:.0f} l{-32:.0f},{-28:.0f}'
                    f' l{-38:.0f},{18:.0f} l{14:.0f},{-38:.0f} l{-42:.0f},{-10:.0f} Z"'
                    f' fill="#9a5a28" stroke="#7d4a24" stroke-width="4" opacity=".92"/>')
    s += SL(Z_SRED, f'<ellipse cx="880" cy="870" rx="650" ry="218" fill="none"'
                    f' stroke="#6b5438" stroke-width="22" opacity=".85"/>')
    # ВНУК на корточках: правая варежка стучит, левая на колене, ухо к луже
    stuk = abs(A.w(t, .9, .0))
    vx, vy, vh = 1240, 1056, 470
    s += SL(Z_SRED, figura(vx, vy, vh, t, col="#c8301f", kant="#ffd9a8",
                           shapka=True, ph=.2, naklon=3.0))
    r1, (e1x, e1y), _ = _ruka(vx, vy, vh, -1, vh * .42, 30 + 18 * stuk, t,
                              "#c8301f", "#ffd9a8", .1, 5)
    r2, (e2x, e2y), _ = _ruka(vx, vy, vh, 1, vh * .28, 58, t, "#c8301f", "#ffd9a8", .6, 3)
    s += SL(Z_SRED, r1 + varezhka(e1x - 8, e1y + 14, 1.15, -12 + 16 * stuk, TKAN, t, .1)
            + r2 + varezhka(e2x + 8, e2y + 12, 1.0, 12, TKAN, t, .6))
    # ЗВУКОВЫЕ КОЛЕЧКИ от стука
    for i in range(4):
        d = ((t * 1.1 + i * .25) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{e1x-10:.0f}" cy="{e1y+40:.0f}"'
                        f' rx="{60+260*d:.0f}" ry="{18+80*d:.0f}" fill="none"'
                        f' stroke="#eaf6ff" stroke-width="{7-4*d:.1f}"'
                        f' opacity="{(1-d)*.7:.2f}"/>')
    s += SL(Z_SRED, para_izo_rta(vx - 30, vy - vh * .74, t, .4, .9, .45))
    s += SL(Z_SRED, ten(vx, vy + 6, 120, 20, .4))
    # БАБУШКИН РУКАВ показывает «тише» — рука ничья (крупный план)
    ruk, (kx_, ky_) = rukav(1760, 700, 240, 150, t, "#4a3a52", "#ffd9a8", .3, 5, True)
    s += SL(Z_SRED, ruk + varezhka(kx_, ky_ + 10, 1.2, -40, TKAN, t, .3))
    # бордюр, жёлтые листья, камешек, воробей
    s += SL(Z_SRED, f'<rect x="0" y="1010" width="{W}" height="40" rx="6"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="5"/>')
    for i in range(8):
        lx_ = 120 + i * 230 + rnd.uniform(-30, 30)
        s += SL(Z_SRED, f'<path d="M{lx_:.0f},{1056+((i*5)%3)*8:.0f} l{30:.0f},{-22:.0f}'
                        f' l{-6:.0f},{22:.0f} l{32:.0f},{-6:.0f} l{-24:.0f},{20:.0f}'
                        f' l{20:.0f},{14:.0f} l{-30:.0f},{2:.0f} l{-4:.0f},{22:.0f}'
                        f' l{-20:.0f},{-18:.0f} l{-24:.0f},{12:.0f} l{8:.0f},{-24:.0f}'
                        f' l{-26:.0f},{-6:.0f} Z"'
                        f' fill="{["#b4762f","#9a5a28","#c08a3a"][i%3]}"'
                        f' stroke="#7d4a24" stroke-width="3"/>')
    s += SL(Z_SRED, f'<ellipse cx="560" cy="1046" rx="40" ry="24" fill="#8a8078"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, ptica(380, 1000, t, 1.8, "#8a7a62", .2, "#6f6256"))
    s += SL(Z_SRED, dvorovye_veschi(120, 1060, 300, t, 167, ["vedro", "korzina"]))
    s += SL(Z_SRED, dym(1500, 180, t, 5, .22, 220, .36, "#d7dee6", .9))
    s += SL(Z_SRED, inej_mel(163, 44, 1000, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def bochka_u_saraya(t):
    """Развилка, свой дом: дождевая бочка под водостоком на пол-кадра, на
    воде тонкая корка. Хозяин заносит ковш и останавливается — листок
    численника отлетает на день назад, и он же вчера вычерпывает бочку ведром."""
    rnd = random.Random(1929)
    s = nebo("sumer", t, False, 167)
    s += oblaka(t, 130, 5, 109, .42)
    s += SL(Z_DAL, ulica_dal(1240, 430, 700, t, True, 83))
    s += SL(Z_DAL, goloe_derevo_ld(1480, 520, 360, t, 167, 6, True))
    # СТЕНА САРАЯ и водосточный жёлоб
    s += SL(Z_SRED, doski(0, 140, 1200, 740, 76, True, "dosk"))
    s += SL(Z_SRED, f'<path d="M-20,140 l620,-120 l620,120 Z" fill="#5e4430"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<path d="M-20,140 l620,-120 l620,120" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="18" opacity=".9"/>')
    s += SL(Z_SRED, f'<rect x="560" y="150" width="46" height="520" rx="8"'
                    f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M560,670 q{-6:.0f},{50:.0f} {-56:.0f},{64:.0f}'
                    f' l{40:.0f},{26:.0f} q{56:.0f},{-30:.0f} {62:.0f},{-90:.0f} Z"'
                    f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(860, 173, False))
    # БОЧКА на пол-кадра
    bx, by = 560, 1020
    boch = (f'<path d="M{bx-170:.0f},{by-440:.0f} q{-40:.0f},{220:.0f} {14:.0f},{440:.0f}'
            f' h{312:.0f} q{54:.0f},{-220:.0f} {14:.0f},{-440:.0f} Z"'
            f' fill="url(#derev)" stroke="{K}" stroke-width="7"/>')
    for k in (.18, .52, .86):
        boch += (f'<rect x="{bx-178+18*k:.0f}" y="{by-440+440*k:.0f}"'
                 f' width="{356-36*k:.0f}" height="20" fill="{ZHELEZ}" opacity=".95"/>')
    for i in range(7):
        boch += (f'<path d="M{bx-150+i*50:.0f},{by-434:.0f} q{-8:.0f},{220:.0f}'
                 f' {2:.0f},{428:.0f}" fill="none" stroke="#6b4428" stroke-width="4"'
                 f' opacity=".7"/>')
    boch += (f'<ellipse cx="{bx:.0f}" cy="{by-440:.0f}" rx="172" ry="48"'
             f' fill="#5f3f27" stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, boch)
    s += SL(Z_SRED, korka_lda(bx, by - 440, 150, 40, t, .2, .0, .95))
    # ХОЗЯИН с ковшом: заносит и останавливается
    hx, hy, hh = 1180, 1056, 680
    zanos = A.ease(A.seg(t, .4, .9)) - A.ease(A.seg(t, 2.0, .8))
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a3a", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .34, 30 - 46 * zanos, t,
                              "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .24, 48, t, "#3f4a3a", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{-90:.0f},{-20:.0f}"'
                    f' stroke="#8a6342" stroke-width="10"/>'
                    f'<path d="M{e1x-90:.0f},{e1y-20:.0f} q{-50:.0f},{10:.0f}'
                    f' {-60:.0f},{50:.0f} q{40:.0f},{30:.0f} {70:.0f},{-6:.0f} Z"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, para_izo_rta(hx - 36, hy - hh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    # ЧИСЛЕННИК: листок отлетает на день назад
    s += SL(Z_SRED, f'<rect x="880" y="260" width="170" height="220" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="880" y="260" width="170" height="44" rx="8"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="4"/>')
    d = ((t * .45) % 1.0)
    s += SL(Z_LETIT, f'<rect x="{900-200*d:.0f}" y="{320+260*d*d:.0f}" width="110"'
                     f' height="140" rx="6" fill="#f2ead6" opacity="{(1-d)*.9:.2f}"'
                     f' transform="rotate({-d*140:.0f} {955-200*d:.0f} {390+260*d*d:.0f})"'
                     f' stroke="{K}" stroke-width="3"/>')
    # «ВЧЕРА»: полупрозрачный силуэт с ведром вычерпывает бочку
    vch = max(.0, A.w(t, 3.0, .4))
    s += SL(Z_SRED, f'<g opacity="{.35*vch:.2f}">'
            + figura(820, 1040, 620, t, col="#6f7a84", kant="#cfe4f5", shapka=True, ph=.9)
            + '</g>')
    s += SL(Z_SRED, f'<g opacity="{.4*vch:.2f}">'
                    f'<path d="M700,760 h110 l-10,96 h-90 Z" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="755" cy="760" rx="55" ry="16" fill="#8f979f"'
                    f' stroke="{K}" stroke-width="3.4"/></g>')
    # лейка, грабли, поленница, кот
    s += SL(Z_SRED, f'<path d="M1480,1000 h130 l-12,66 h-106 Z" fill="#3f6b7a"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M1610,1012 q{60:.0f},{-10:.0f} {90:.0f},{30:.0f}"'
                    f' fill="none" stroke="#3f6b7a" stroke-width="10"/>'
                    f'<path d="M1480,996 q{64:.0f},{-54:.0f} {128:.0f},{-4:.0f}"'
                    f' fill="none" stroke="{CHUGUN}" stroke-width="6"/>')
    s += SL(Z_SRED, dvorovye_veschi(1700, 1066, 240, t, 173, ["grabli", "churbak"]))
    s += SL(Z_SRED, f'<rect x="60" y="880" width="260" height="170" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<circle cx="{80+(i%6)*46:.0f}" cy="{906+(i//6)*60:.0f}" r="23"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, kot(190, 880, t, 1.4, "#4a423a", True))
    s += SL(Z_SRED, lampa(1000, 200, t, 1.1, False) + teplo(1000, 210, 200, 170, .40))
    s += SL(Z_SRED, inej_mel(173, 42, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def luzha_u_podezda_k_poludnyu(t):
    """Развилка, город: бочка становится лужей у крыльца многоэтажки.
    Женщина с сумкой выходит из подъезда и обходит лужу по бордюру, а
    солнце идёт к полудню — корка подтаивает с краёв."""
    rnd = random.Random(1930)
    s = nebo("den", t, False, 173)
    s += oblaka(t, 140, 5, 113, .40)
    sol = A.ease(A.seg(t, .3, 4.0))
    s += SL(Z_NEBO, f'<circle cx="{420+900*sol:.0f}" cy="{300-120*sol:.0f}" r="110"'
                    f' fill="#ffe9ac" opacity=".45"/>'
                    f'<circle cx="{420+900*sol:.0f}" cy="{300-120*sol:.0f}" r="64"'
                    f' fill="#fff4d8" opacity=".9"/>')
    s += SL(Z_DAL, panelka(60, 760, 980, t, 5, True, 19))
    s += SL(Z_DAL, panelka(1500, 700, 420, t, 4, True, 23))
    # КРЫЛЬЦО подъезда
    s += SL(Z_SRED, f'<rect x="1060" y="400" width="420" height="420" rx="8"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="1140" y="470" width="260" height="350" rx="6"'
                    f' fill="#3f5a6a" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1270" y="470" width="130" height="350" rx="6"'
                    f' fill="#8aa8b4" opacity=".55" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1040" y="820" width="460" height="30" rx="6"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1060" y="850" width="420" height="26" rx="5"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1080" y="876" width="380" height="24" rx="5"'
                    f' fill="#7a736a" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(1270, 420, t, 1.0, True) + teplo(1270, 430, 180, 150, .34))
    s += SL(Z_SRED, _merzlaya_zemlya(880, 179, False))
    s += SL(Z_SRED, f'<rect x="0" y="920" width="{W}" height="36" rx="6"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="5"/>')
    # ЛУЖА: корка подтаивает с краёв
    tay = A.ease(A.seg(t, 1.0, 4.4))
    s += SL(Z_SRED, f'<ellipse cx="700" cy="1000" rx="420" ry="120" fill="#2f4a52"/>')
    s += SL(Z_SRED, korka_lda(700, 998, 390 * (1 - .32 * tay), 108 * (1 - .3 * tay),
                              t, .2, .0, .92))
    s += SL(Z_SRED, f'<ellipse cx="700" cy="1000" rx="424" ry="124" fill="none"'
                    f' stroke="#6f6256" stroke-width="16" opacity=".8"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{420+i*94:.0f}" cy="{1000+((i*7)%3-1)*44:.0f}"'
                        f' rx="{30*tay:.0f}" ry="{12*tay:.0f}" fill="#4a7a88"'
                        f' opacity="{.55*tay:.2f}"/>')
    # ЖЕНЩИНА обходит по бордюру
    obh = A.ease(A.seg(t, .6, 3.2))
    zx, zy, zh = 1260 - 420 * obh, 940 + 40 * obh, 640
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#6b3a6a", kant="#ffd9a8",
                           platok=False, ph=.3))
    r1, (e1x, e1y), _ = _ruka(zx, zy, zh, 1, zh * .28, 54, t, "#6b3a6a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(zx, zy, zh, -1, zh * .24, 34 - 30 * obh, t,
                              "#6b3a6a", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    kach = 8 * A.w(t, 1.2, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-48:.0f}" y="{e1y+6:.0f}" width="96" height="76"'
                    f' rx="10" fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{e1x-30:.0f},{e1y+6:.0f} q{30:.0f},{-40:.0f} {60:.0f},0"'
                    f' fill="none" stroke="#6b2419" stroke-width="7"/></g>')
    s += SL(Z_SRED, para_izo_rta(zx - 32, zy - zh * .80, t, .4, .9, .45))
    s += SL(Z_SRED, ten(zx, zy + 6, 120, 20, .4))
    # скамейка, урна, велосипед, рябина, голуби
    s += SL(Z_SRED, f'<rect x="180" y="800" width="330" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="180" y="740" width="330" height="20" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="200" y="822" width="22" height="100" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="470" y="822" width="22" height="100" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="580" y="800" width="100" height="130" rx="10"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<circle cx="1660" cy="960" r="76" fill="none" stroke="{CHUGUN}"'
                    f' stroke-width="11"/>'
                    f'<circle cx="1850" cy="960" r="76" fill="none" stroke="{CHUGUN}"'
                    f' stroke-width="11"/>'
                    f'<path d="M1660,960 L1760,860 L1850,960 M1760,860 L1790,900'
                    f' M1700,900 L1760,860" fill="none" stroke="#8a2f22"'
                    f' stroke-width="10"/>'
                    f'<path d="M1736,842 h60" stroke="{CHUGUN}" stroke-width="9"/>')
    s += SL(Z_SRED, ryabina(1480, 1000, t, 1.5, 6))
    for i, (gx, gy) in enumerate(((320, 1030), (420, 1056), (520, 1016))):
        s += SL(Z_SRED, ptica(gx, gy, t, 1.6, "#9aa3a8", i * .3, "#6f7a84"))
    s += SL(Z_SRED, inej_mel(179, 40, 950, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def pervyy_shag_na_led(t):
    """Плашка второго запрета: кромка тёмного тонкого льда у берега. Валенок
    с галошей ставится на лёд на треть кадра — лёд прогибается, из-под него
    выступает тёмная полоса, и валенок отдёргивается на берег."""
    rnd = random.Random(1931)
    s = nebo("sumer", t, False, 179)
    s += oblaka(t, 130, 5, 127, .42)
    s += SL(Z_DAL, ulica_dal(60, 330, 760, t, True, 89))
    s += SL(Z_DAL, goloe_derevo_ld(1540, 420, 440, t, 179, 7, True))
    s += SL(Z_DAL, izba_snaruzhi(1180, 380, 260, t, True, True, 41)
            + dym(1206, 240, t, 6, .22, 240, .40, "#d7dee6", .9))
    s += SL(Z_SRED, mostki(1300, 520, 500, t, True, 180))
    s += SL(Z_SRED, f'<rect x="0" y="430" width="{W}" height="650" fill="{VODA2}"/>')
    s += SL(Z_SRED, f'<rect x="0" y="430" width="{W}" height="300" fill="url(#led)"'
                    f' opacity=".8"/>')
    s += SL(Z_SRED, korka_lda(960, 600, 800, 150, t, .2, .0, .85, .35))
    # БЕРЕГ в инее со следами только до кромки
    s += SL(Z_SRED, f'<path d="M-40,1080 Q420,880 980,840 L1920,810 L1920,1080 Z"'
                    f' fill="#5f4a32" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-40,1080 Q420,890 980,850 L1920,820" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="26" opacity=".9"/>')
    s += SL(Z_SRED, sledy_valenok(1860, 1056, 900, 866, 8, 181, "#4a4038", 1.2))
    # ВАЛЕНОК на треть кадра: ставится и отдёргивается
    stav = A.ease(A.seg(t, .4, .8)) - A.ease(A.seg(t, 1.5, .7))
    vx, vy = 760, 780 + 60 * stav
    s += SL(Z_SRED, f'<g transform="rotate({-10+8*stav:.1f} {vx:.0f} {vy:.0f})">'
            + _valenok(vx, vy, 2.6, 0, "#b9ae9a")
            + f'<path d="M{vx-110:.0f},{vy-36:.0f} h{220:.0f} q{30:.0f},{20:.0f}'
              f' {6:.0f},{56:.0f} h{-230:.0f} Z" fill="#23242a" stroke="{K}"'
              f' stroke-width="7"/></g>')
    # прогиб льда и тёмная полоса из-под него
    s += SL(Z_SRED, f'<ellipse cx="{vx:.0f}" cy="{vy+70:.0f}" rx="{210+90*stav:.0f}"'
                    f' ry="{40+22*stav:.0f}" fill="#17424c" opacity="{.4+.4*stav:.2f}"/>')
    if stav > .1:
        s += SL(Z_SRED, treschina(vx, vy + 74, 300 * stav, 191, 5, "#eaf6ff", 4.5))
    s += SL(Z_SRED, f'<path d="M{vx-260:.0f},{vy+96:.0f} q{260:.0f},{40*stav:.0f}'
                    f' {520:.0f},{-10*stav:.0f}" fill="none" stroke="#0f2a32"'
                    f' stroke-width="{10+16*stav:.0f}" opacity=".75"/>')
    # сухой камыш, вмёрзшее ведёрко, ива
    s += SL(Z_SRED, kamysh(180, 900, 260, t, 8, 191, True)
            + kamysh(1880, 940, 230, t, 7, 193, True))
    s += SL(Z_SRED, f'<path d="M1120,700 h96 l-10,84 h-76 Z" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="1168" cy="700" rx="48" ry="14" fill="#8f979f"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<ellipse cx="1168" cy="706" rx="38" ry="10" fill="{INEY}"'
                    f' opacity=".8"/>'
                    f'<ellipse cx="1168" cy="790" rx="90" ry="22" fill="#cfe4f5"'
                    f' opacity=".55"/>')
    s += SL(Z_SRED, goloe_derevo_ld(300, 1020, 520, t, 197, 7, True))
    s += SL(Z_SRED, dvorovye_veschi(1560, 1070, 320, t, 181, ["kadka", "korzina"]))
    # ЦЕНТР КАДРА ОБЖИТ: битые льдины, коряги, вешки, перевёрнутая лодка
    for i in range(9):
        ox_ = 260 + i * 180 + rnd.uniform(-30, 30)
        oy_ = 520 + ((i * 5) % 3) * 70
        s += SL(Z_SRED, f'<path d="M{ox_:.0f},{oy_:.0f} l{rnd.uniform(60,120):.0f},'
                        f'{rnd.uniform(-20,14):.0f} l{rnd.uniform(-20,30):.0f},'
                        f'{rnd.uniform(30,56):.0f} l{rnd.uniform(-80,-50):.0f},'
                        f'{rnd.uniform(6,20):.0f} Z" fill="#dcecf8" stroke="#9fc4d8"'
                        f' stroke-width="4" opacity=".92"/>')
    for i, (kx_, kb_) in enumerate(((430, 780), (1120, 760), (1600, 790))):
        s += SL(Z_SRED, f'<path d="M{kx_:.0f},{kb_:.0f} q{40:.0f},{-80:.0f}'
                        f' {10:.0f},{-150:.0f} q{60:.0f},{54:.0f} {96:.0f},{26:.0f}"'
                        f' fill="none" stroke="#54351f" stroke-width="12"/>')
    for i, vx_ in enumerate((640, 980, 1320)):
        kch = 3.0 * A.w(t, 3.0, i * .4)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {vx_:.0f} {660:.0f})">'
                        f'<rect x="{vx_:.0f}" y="440" width="12" height="220"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{vx_-22:.0f},440 q{28:.0f},{-30:.0f} {56:.0f},{-4:.0f}'
                        f' q{-26:.0f},{22:.0f} {-56:.0f},{4:.0f} Z" fill="#8a7a52"'
                        f' stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, f'<path d="M1480,700 q{140:.0f},{-60:.0f} {280:.0f},0 Z"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1480,700 h280" stroke="url(#sneg)" stroke-width="11"'
                    f' opacity=".9"/>')
    s += SL(Z_SRED, inej_mel(191, 50, 860, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 18, 43, .36, .5))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def most_cherez_reku(t):
    """Деревянный мост через реку на пол-кадра: в пролёте под ним — проём с
    настоящей рекой в первом льду. По мосту идут мужик с лошадью и санями,
    баба с корзиной и мальчик у перил. На льду под мостом ни следа."""
    rnd = random.Random(1932)
    s = nebo("rassv", t, False, 181)
    s += oblaka(t, 140, 5, 131, .40)
    s += SL(Z_DAL, ulica_dal(1180, 300, 740, t, True, 97))
    s += SL(Z_DAL, izba_snaruzhi(160, 330, 280, t, True, True, 43)
            + dym(188, 190, t, 6, .22, 250, .40, "#d7dee6", .9))
    s += SL(Z_DAL, goloe_derevo_ld(600, 360, 320, t, 199, 6, True))
    # БЕРЕГА и река
    s += SL(Z_SRED, f'<rect x="0" y="420" width="{W}" height="660" fill="{VODA2}"/>')
    s += SL(Z_SRED, f'<path d="M0,420 q480,{40:.0f} 960,{10:.0f} T1920,430 L1920,560'
                    f' L0,560 Z" fill="#5f4a32"/>')
    # ПРОЁМ в пролёте: вид, метка, обвязка (мост поверх)
    px, py, pw, ph_ = 570, 640, 780, 300
    pr = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
          f' fill="#9fc4d8"/>')
    pr += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.4:.0f}"'
           f' fill="#c4d8e8"/>')
    pr += mesto_stoka(px, py, pw, ph_, "pryam")
    pr += (f'<rect x="{px-10:.0f}" y="{py-10:.0f}" width="{pw+20:.0f}"'
           f' height="{ph_+20:.0f}" fill="none" stroke="#54351f" stroke-width="20"/>')
    s += SL(Z_SRED, pr)
    s += SL(Z_SRED, korka_lda(300, 820, 260, 80, t, .3, .0, .8, .3)
            + korka_lda(1640, 840, 250, 76, t, .6, .0, .8, .3))
    # МОСТ на пол-кадра
    most = (f'<rect x="-20" y="520" width="1960" height="60" rx="6" fill="url(#derev)"'
            f' stroke="{K}" stroke-width="6"/>')
    for i in range(26):
        most += (f'<rect x="{-20+i*76:.0f}" y="516" width="62" height="68" rx="4"'
                 f' fill="{DOSKA}" stroke="{K}" stroke-width="2.6"/>')
    for i in range(14):
        most += (f'<rect x="{10+i*146:.0f}" y="440" width="18" height="90"'
                 f' fill="{DOSKA2}" stroke="{K}" stroke-width="3"/>')
    most += (f'<rect x="-20" y="430" width="1960" height="18" rx="6" fill="{DOSKA2}"'
             f' stroke="{K}" stroke-width="4"/>')
    for sx_ in (520, 1400):
        most += (f'<rect x="{sx_:.0f}" y="580" width="46" height="420" fill="#6b4428"'
                 f' stroke="{K}" stroke-width="5"/>'
                 f'<path d="M{sx_-30:.0f},660 h106" stroke="#54351f" stroke-width="12"/>')
    s += SL(Z_SRED, most)
    # ЛОШАДЬ с САНЯМИ и трое людей на мосту
    edet = A.ease(A.seg(t, .3, 4.2))
    lx = 420 + 300 * edet
    kiv = 9 * A.w(t, 1.4, .1)
    s += SL(Z_SRED, f'<ellipse cx="{lx:.0f}" cy="430" rx="140" ry="74" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{lx+120:.0f},400 q{70:.0f},{-30+kiv:.0f} {96:.0f},{20+kiv:.0f}'
                    f' l{-30:.0f},{40:.0f} q{-40:.0f},{-20:.0f} {-76:.0f},{-10:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{lx+196:.0f},{378+kiv:.0f} l{14:.0f},{-44:.0f}'
                    f' l{18:.0f},{40:.0f} Z" fill="#6b5230" stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="{lx+206:.0f}" cy="{408+kiv:.0f}" r="6" fill="{K}"/>'
                    f'<path d="M{lx-140:.0f},410 q{-50:.0f},{-30:.0f} {-74:.0f},{10:.0f}"'
                    f' fill="none" stroke="#54351f" stroke-width="12"/>'
                    f'<path d="M{lx-80:.0f},496 l-10,34 M{lx-10:.0f},500 l0,30'
                    f' M{lx+70:.0f},496 l10,34 M{lx+120:.0f},490 l12,40"'
                    f' stroke="#54351f" stroke-width="13"/>')
    s += SL(Z_SRED, sani_s_rogozhey(lx - 300, 500, .82, t, .2, True))
    mx, my, mh = lx - 120, 520, 560
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f4a3a", kant="#ffd9a8",
                           shapka=True, tulup=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -8, t, "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .26, 36, t, "#3f4a3a", "#ffd9a8", .7, 5)
    s += SL(Z_SRED, r1 + r2 + f'<path d="M{e1x:.0f},{e1y:.0f} L{lx+150:.0f},{382+kiv:.0f}"'
                              f' stroke="#6b4428" stroke-width="6"/>'
                              f'<path d="M{e2x:.0f},{e2y:.0f} q{-40:.0f},{40:.0f}'
                              f' {-70:.0f},{86:.0f}" fill="none" stroke="#5e4a2a"'
                              f' stroke-width="5"/>')
    bx, by, bh = 1480, 524, 560
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.6))
    r3, (e3x, e3y), _ = _ruka(bx, by, bh, 1, bh * .24, 46, t, "#4a3a52", "#ffd9a8", .3, 4)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x-44:.0f},{e3y+4:.0f} q{44:.0f},{18:.0f} {88:.0f},0'
                         f' l{-10:.0f},{64:.0f} h{-68:.0f} Z" fill="#b08a52"'
                         f' stroke="{K}" stroke-width="4"/>')
    for k in range(4):
        s += SL(Z_SRED, f'<circle cx="{e3x-30+k*20:.0f}" cy="{e3y+14:.0f}" r="12"'
                        f' fill="#c8301f" stroke="{K}" stroke-width="2.6"/>')
    mlx, mly, mlh = 1700, 528, 400
    s += SL(Z_SRED, figura(mlx, mly, mlh, t, col="#3f5a6a", kant="#ffd9a8",
                           shapka=True, ph=.9))
    r4, (e4x, e4y), _ = _ruka(mlx, mly, mlh, -1, mlh * .30, -22, t,
                              "#3f5a6a", "#ffd9a8", .4, 5)
    s += SL(Z_SRED, r4)
    s += SL(Z_SRED, para_izo_rta(mx - 34, my - mh * .80, t, .3, .9, .45)
            + para_izo_rta(bx - 30, by - bh * .80, t, .7, .9, .45))
    # вороны на перилах, бани и лодки на берегу
    for i, (vx_, vy_) in enumerate(((760, 410), (900, 404))):
        vor = 6 * A.w(t, 2.0, i * .4)
        s += SL(Z_SRED, f'<ellipse cx="{vx_+vor:.0f}" cy="{vy_:.0f}" rx="40" ry="26"'
                        f' fill="#23242a" stroke="{K}" stroke-width="3.4"/>'
                        f'<circle cx="{vx_+26+vor:.0f}" cy="{vy_-22:.0f}" r="18"'
                        f' fill="#23242a" stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{vx_+42+vor:.0f},{vy_-24:.0f} l24,5 l-24,7 Z"'
                        f' fill="#6f6256" stroke="{K}" stroke-width="2.4"/>')
    for i, (lx_, ly_, ls_) in enumerate(((240, 1000, 1.0), (1720, 1020, .9))):
        s += SL(Z_SRED, f'<path d="M{lx_-150*ls_:.0f},{ly_:.0f} q{150*ls_:.0f},{-70*ls_:.0f}'
                        f' {300*ls_:.0f},0 Z" fill="#6b4428" stroke="{K}"'
                        f' stroke-width="{5*ls_:.1f}"/>'
                        f'<path d="M{lx_-150*ls_:.0f},{ly_:.0f} h{300*ls_:.0f}"'
                        f' stroke="url(#sneg)" stroke-width="{10*ls_:.1f}" opacity=".9"/>')
    s += SL(Z_SRED, kamysh(80, 1040, 220, t, 7, 211, True)
            + kamysh(1880, 1046, 230, t, 7, 223, True))
    s += SL(Z_SRED, inej_mel(197, 44, 900, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s
