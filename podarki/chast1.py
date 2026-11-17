# -*- coding: utf-8 -*-
"""Декорации 1-34 ролика «Что дарить на Новый год 2027»."""
import math, random
from baza import *
import anim as A
from lok_obshchee import (figura, rukav, kirpich_ustya, para_izo_rta,
                           tusklaya_lampochka, luchina, mokryy_sneg,
                           goloe_derevo, gryaz_polosa, sumerki_fon)

IMP = "#5c2a4a"


# ───────────────────────── МЕСТНЫЕ КИРПИЧИКИ ПОРЦИИ ─────────────────────────
def _korobka(x, y, w_, h_, t, col=None, lenta=None, bant=True, otkryta=0.0, ph=0.0):
    """Подарочная коробка: крышка приоткрывается на otkryta (0..1)."""
    col = col or TKAN2
    lenta = lenta or ZOL
    kach = 2.0 * A.w(t, 2.4, ph)
    kr = h_ * (0.22 + 0.5 * otkryta)
    s = ten(x + w_ * .5, y + h_ + 10, w_ * .5, 12, .4)
    s += (f'<rect x="{x:.0f}" y="{y+kr:.0f}" width="{w_:.0f}" height="{h_-kr:.0f}" rx="8"'
          f' fill="{col}" {o(6)}/>')
    s += (f'<rect x="{x-4:.0f}" y="{y+kr:.0f}" width="{w_+8:.0f}" height="{(h_-kr)*.46:.0f}"'
          f' fill="{lenta}" opacity=".85"/>')
    s += (f'<rect x="{x+w_*.42:.0f}" y="{y+kr:.0f}" width="{w_*.16:.0f}" height="{h_-kr:.0f}"'
          f' fill="{lenta}" opacity=".85"/>')
    s += f'<g transform="rotate({-16*otkryta:.1f} {x:.0f} {y+kr:.0f})">'
    s += f'<rect x="{x-8:.0f}" y="{y:.0f}" width="{w_+16:.0f}" height="{kr+6:.0f}" rx="8" fill="{col}" {o(6)}/>'
    s += (f'<rect x="{x+w_*.42:.0f}" y="{y:.0f}" width="{w_*.16:.0f}" height="{kr+6:.0f}"'
          f' fill="{lenta}" opacity=".85"/>')
    if bant:
        bx, by = x + w_ * .5, y + kr * .3 + kach
        s += (f'<path d="M{bx:.0f},{by:.0f} q{-w_*.22:.0f},{-h_*.14:.0f} {-w_*.03:.0f},{-h_*.26:.0f}'
              f' q{w_*.12:.0f},{-h_*.02:.0f} {w_*.03:.0f},{h_*.1:.0f} q{w_*.02:.0f},{-h_*.1:.0f}'
              f' {w_*.24:.0f},{h_*.18:.0f} Z" fill="{lenta}" {o(4)}/>')
        s += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{w_*.07:.0f}" fill="{lenta}" {o(3)}/>'
    return s + '</g>'


def _svertok(x, y, s_, t, col=None, lenta=None, ph=0.0):
    """Мелкий свёрток-кулёк: ткнутый сверху узел, маленький бант."""
    col = col or RUSH
    lenta = lenta or TKAN
    bob = 3 * A.w(t, 1.8, ph)
    s = ten(x, y + 14 * s_, 38 * s_, 9 * s_, .35)
    s += (f'<path d="M{x-40*s_:.0f},{y+bob:.0f} q-4,{-56*s_:.0f} 40,{-60*s_:.0f}'
          f' q44,4 40,{60*s_:.0f} q-40,{14*s_:.0f} -80,0 Z" fill="{col}" {o(5)}/>')
    s += (f'<path d="M{x-28*s_:.0f},{y-20*s_+bob:.0f} q28,{-34*s_:.0f} 56,0" fill="none"'
          f' stroke="{lenta}" stroke-width="{7*s_:.0f}"/>')
    s += f'<circle cx="{x:.0f}" cy="{y-46*s_+bob:.0f}" r="{9*s_:.0f}" fill="{lenta}" {o(3)}/>'
    return s


def _varezhka(x, y, s_, ang, col=None, uzor=None):
    col = col or TKAN
    uzor = uzor or SVET
    s = f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x-24*s_:.0f},{y:.0f} q-6,{-56*s_:.0f} 26,{-62*s_:.0f}'
          f' q30,6 26,{62*s_:.0f} q-26,{14*s_:.0f} -52,0 Z" fill="{col}" {o(5)}/>')
    s += (f'<path d="M{x-24*s_:.0f},{y-10*s_:.0f} q-22,{-4*s_:.0f} -22,{-26*s_:.0f}'
          f' q0,{-14*s_:.0f} 20,{-14*s_:.0f} q6,{20*s_:.0f} 2,{40*s_:.0f} Z" fill="{col}" {o(4)}/>')
    s += (f'<path d="M{x-20*s_:.0f},{y-58*s_:.0f} q20,{-10*s_:.0f} 40,0" fill="none"'
          f' stroke="{uzor}" stroke-width="{4*s_:.0f}" opacity=".7"/>')
    return s + '</g>'


def _banka(x, y, s_, col=MED, tkan=None):
    tkan = tkan or TKAN
    s = ten(x, y + 6 * s_, 36 * s_, 9 * s_, .4)
    s += (f'<path d="M{x-34*s_:.0f},{y:.0f} v{-78*s_:.0f} q0,-10 10,-10 h{48*s_:.0f}'
          f' q10,0 10,10 v{78*s_:.0f} Z" fill="url(#{"med" if col==MED else "glina"})" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-92*s_:.0f}" rx="{30*s_:.0f}" ry="{10*s_:.0f}"'
          f' fill="{tkan}" {o(4)}/>')
    s += (f'<path d="M{x-28*s_:.0f},{y-92*s_:.0f} q28,{14*s_:.0f} 56,0" fill="none"'
          f' stroke="{tkan}" stroke-width="{5*s_:.0f}" opacity=".7"/>')
    return s


def _svistulka(x, y, s_, ang=0.0, col=None):
    """Глиняная свистулька-птичка: тело, хвост веером, клюв, дырочка."""
    col = col or KRAS
    s = f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{44*s_:.0f}" ry="{30*s_:.0f}" fill="{col}" {o(4)}/>'
    s += (f'<path d="M{x+34*s_:.0f},{y-4*s_:.0f} l{24*s_:.0f},{-14*s_:.0f} l{-2*s_:.0f},{18*s_:.0f}'
          f' l{-2*s_:.0f},{18*s_:.0f} Z" fill="{col}" {o(3)}/>')
    s += f'<path d="M{x-40*s_:.0f},{y:.0f} l{-18*s_:.0f},{-8*s_:.0f} l2,{16*s_:.0f} Z" fill="{ZOL}" {o(2)}/>'
    s += f'<circle cx="{x-6*s_:.0f}" cy="{y-8*s_:.0f}" r="{3*s_:.0f}" fill="{K}"/>'
    s += f'<circle cx="{x+10*s_:.0f}" cy="{y+8*s_:.0f}" r="{4*s_:.0f}" fill="#1a1410"/>'
    return s + '</g>'


def _oblachko(x, y, s_, t, ph, kind):
    rise = 10 * A.ease(A.seg(t, ph, 1.0)) % 10
    bob = 6 * A.w(t, 1.6, ph)
    s = (f'<ellipse cx="{x:.0f}" cy="{y+bob:.0f}" rx="{70*s_:.0f}" ry="{46*s_:.0f}"'
         f' fill="#ffffff" opacity=".92" {o(4)}/>')
    s += (f'<ellipse cx="{x-40*s_:.0f}" cy="{y+16*s_+bob:.0f}" rx="{26*s_:.0f}" ry="{18*s_:.0f}"'
          f' fill="#ffffff" opacity=".92" {o(3)}/>')
    s += (f'<circle cx="{x-54*s_:.0f}" cy="{y+40*s_+bob:.0f}" r="{9*s_:.0f}"'
          f' fill="#ffffff" opacity=".9" {o(2)}/>')
    cy_ = y + bob
    if kind == "serdce":
        s += (f'<path d="M{x:.0f},{cy_+16*s_:.0f} q-30,-30 -30,-50 q0,-18 16,-18 q14,0 14,14'
              f' q0,-14 14,-14 q16,0 16,18 q0,20 -30,50 Z" fill="{KRAS}"/>')
    elif kind == "moneta":
        s += f'<circle cx="{x:.0f}" cy="{cy_:.0f}" r="{22*s_:.0f}" fill="url(#med)" {o(3)}/>'
    elif kind == "ruki":
        s += (f'<ellipse cx="{x-16*s_:.0f}" cy="{cy_:.0f}" rx="{16*s_:.0f}" ry="{10*s_:.0f}"'
              f' fill="#e0b08a" {o(2)}/>')
        s += (f'<ellipse cx="{x+16*s_:.0f}" cy="{cy_:.0f}" rx="{16*s_:.0f}" ry="{10*s_:.0f}"'
              f' fill="#e0b08a" {o(2)}/>')
    elif kind == "doroga":
        s += (f'<path d="M{x-24*s_:.0f},{cy_+16*s_:.0f} L{x:.0f},{cy_-16*s_:.0f}'
              f' L{x+24*s_:.0f},{cy_+16*s_:.0f}" fill="none" stroke="#6f7f8c"'
              f' stroke-width="{8*s_:.0f}" stroke-dasharray="6 6"/>')
    elif kind == "ravno":
        s += (f'<line x1="{x-22*s_:.0f}" y1="{cy_-8*s_:.0f}" x2="{x+22*s_:.0f}" y2="{cy_-8*s_:.0f}"'
              f' stroke="{K}" stroke-width="{6*s_:.0f}"/>')
        s += (f'<line x1="{x-22*s_:.0f}" y1="{cy_+8*s_:.0f}" x2="{x+22*s_:.0f}" y2="{cy_+8*s_:.0f}"'
              f' stroke="{K}" stroke-width="{6*s_:.0f}"/>')
    elif kind == "chasy":
        s += f'<circle cx="{x:.0f}" cy="{cy_:.0f}" r="{22*s_:.0f}" fill="#efe3c8" {o(3)}/>'
        s += (f'<line x1="{x:.0f}" y1="{cy_:.0f}" x2="{x:.0f}" y2="{cy_-14*s_:.0f}" stroke="{K}" stroke-width="3"/>'
              f'<line x1="{x:.0f}" y1="{cy_:.0f}" x2="{x+10*s_:.0f}" y2="{cy_:.0f}" stroke="{K}" stroke-width="3"/>')
    return s


def _chasy_sten(x, y, s_, t, col=None):
    """Настенные/настольные часы: циферблат, две стрелки, деления без цифр."""
    col = col or KREM
    a_min = (t * 11) % 360
    a_hr = (t * .9) % 360
    s = ten(x, y + 60 * s_, 46 * s_, 10 * s_, .4)
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{52*s_:.0f}" fill="url(#derev)" {o(6)}/>'
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{40*s_:.0f}" fill="{col}" {o(4)}/>'
    for i in range(12):
        a = math.radians(i * 30)
        x1, y1 = x + math.sin(a) * 34 * s_, y - math.cos(a) * 34 * s_
        x2, y2 = x + math.sin(a) * 40 * s_, y - math.cos(a) * 40 * s_
        s += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{K}" stroke-width="2.4"/>'
    s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.sin(math.radians(a_hr))*20*s_:.0f}"'
          f' y2="{y-math.cos(math.radians(a_hr))*20*s_:.0f}" stroke="{K}" stroke-width="4" stroke-linecap="round"/>')
    s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.sin(math.radians(a_min))*30*s_:.0f}"'
          f' y2="{y-math.cos(math.radians(a_min))*30*s_:.0f}" stroke="{K}" stroke-width="3" stroke-linecap="round"/>')
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{4*s_:.0f}" fill="{K}"/>'
    return s


def _chasy_karman(x, y, s_, t, otkryt=1.0):
    a_min = (t * 24) % 360
    s = f'<g transform="rotate({6*A.w(t,2.1):.1f} {x:.0f} {y:.0f})">'
    s += f'<path d="M{x:.0f},{y-56*s_:.0f} q22,-14 22,{14*s_:.0f}" fill="none" stroke="url(#zhel)" stroke-width="{5*s_:.0f}"/>'
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{48*s_:.0f}" fill="url(#zol)" {o(6)}/>'
    if otkryt > .2:
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{36*s_:.0f}" fill="{KREM}" {o(4)}/>'
        for i in range(12):
            a = math.radians(i * 60)
            s += (f'<line x1="{x+math.sin(a)*30*s_:.0f}" y1="{y-math.cos(a)*30*s_:.0f}"'
                  f' x2="{x+math.sin(a)*34*s_:.0f}" y2="{y-math.cos(a)*34*s_:.0f}" stroke="{K}" stroke-width="2"/>')
        s += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.sin(math.radians(a_min))*24*s_:.0f}"'
              f' y2="{y-math.cos(math.radians(a_min))*24*s_:.0f}" stroke="{K}" stroke-width="3"/>')
    return s + '</g>'


def _servant(x, y, w_, h_, t, col=None):
    """Полированный сервант с хрусталём за стеклом — крупный объект от 600 px."""
    col = col or "#6b4428"
    s = ten(x + w_ * .5, y + h_ + 14, w_ * .5, 18, .5)
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="url(#derev)" {o(7)}/>'
    s += (f'<rect x="{x+w_*.08:.0f}" y="{y+h_*.06:.0f}" width="{w_*.84:.0f}" height="{h_*.42:.0f}"'
          f' rx="8" fill="url(#stekl)" opacity=".7" {o(5)}/>')
    rnd = random.Random(int(x) + int(y))
    for i in range(7):
        hx = x + w_ * .14 + rnd.random() * w_ * .7
        hy = y + h_ * .12 + rnd.random() * h_ * .3
        bl = .4 + .6 * abs(A.w(t, 1.7 + i * .2, i * .15))
        s += (f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="{10+rnd.random()*7:.0f}"'
              f' ry="{14+rnd.random()*8:.0f}" fill="#eaf4ff" opacity="{bl:.2f}"/>')
    s += (f'<rect x="{x+w_*.08:.0f}" y="{y+h_*.54:.0f}" width="{w_*.84:.0f}" height="{h_*.36:.0f}"'
          f' rx="6" fill="{col}" {o(5)}/>')
    for i in range(3):
        s += (f'<circle cx="{x+w_*.2+i*w_*.3:.0f}" cy="{y+h_*.72:.0f}" r="7" fill="url(#zol)" {o(2)}/>')
    return s


def _shkaf_proem(x, y, w_, h_, t, pw, ph_, vid):
    """Шкаф/полка с проёмом под настоящий кадр — объём от 600 px."""
    s = ten(x + w_ * .5, y + h_ + 14, w_ * .5, 16, .5)
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8" fill="url(#derev)" {o(7)}/>'
    px, py = x + (w_ - pw) / 2, y + (h_ - ph_) / 2
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += f'<path d="{put}" fill="#1a140e"/>' + vid
    s += mesto_stoka(px, py, pw, ph_, "pryam")
    s += f'<path d="{put}" fill="none" {o(8)}/>'
    return s, (px, py, pw, ph_)


def _zapret(x, y, r_, t, ph=0.0):
    puls = .8 + .2 * abs(A.w(t, 1.4, ph))
    s = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_:.0f}" fill="none" stroke="{KRAS}" stroke-width="{14*puls:.0f}" opacity=".9"/>'
    a = math.radians(40)
    s += (f'<line x1="{x-r_*.8*math.cos(a):.0f}" y1="{y-r_*.8*math.sin(a):.0f}"'
          f' x2="{x+r_*.8*math.cos(a):.0f}" y2="{y+r_*.8*math.sin(a):.0f}"'
          f' stroke="{KRAS}" stroke-width="{14*puls:.0f}" opacity=".9" stroke-linecap="round"/>')
    return s


def _galochka(x, y, s_, t, ph=0.0):
    puls = .7 + .3 * abs(A.w(t, 1.8, ph))
    s = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{30*s_:.0f}" fill="{ZEL2}" opacity="{puls:.2f}" {o(3)}/>'
    s += (f'<path d="M{x-14*s_:.0f},{y:.0f} l{8*s_:.0f},{10*s_:.0f} l{18*s_:.0f},{-20*s_:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{6*s_:.0f}" stroke-linecap="round" stroke-linejoin="round"/>')
    return s


def _koshelek(x, y, s_, otkryt=True, n_monet=0, moly=False, t=0.0):
    s = ten(x, y + 20 * s_, 56 * s_, 10 * s_, .35)
    s += (f'<path d="M{x-54*s_:.0f},{y:.0f} q-6,{-50*s_:.0f} 54,{-50*s_:.0f}'
          f' q60,0 54,{50*s_:.0f} q-54,{16*s_:.0f} -108,0 Z" fill="#5a3a26" {o(5)}/>')
    if otkryt:
        s += (f'<path d="M{x-48*s_:.0f},{y-6*s_:.0f} q48,{-38*s_:.0f} 96,0" fill="none"'
              f' stroke="#2e1d12" stroke-width="{6*s_:.0f}"/>')
        for i in range(n_monet):
            s += (f'<circle cx="{x-20*s_+i*18*s_:.0f}" cy="{y-20*s_:.0f}" r="{11*s_:.0f}"'
                  f' fill="url(#med)" {o(2)}/>')
        if moly:
            fl = 8 * A.w(t, 2.3)
            s += (f'<ellipse cx="{x+30*s_+fl:.0f}" cy="{y-40*s_-abs(fl):.0f}" rx="{10*s_:.0f}" ry="{6*s_:.0f}"'
                  f' fill="#9a8a78" opacity=".7"/>')
    return s


def _elka(x, y, h_, t, seed=3, ogonki=True):
    """Ёлка с гирляндой — один путь силуэта держит крупный габарит."""
    rnd = random.Random(seed)
    sway = 1.6 * A.w(t, 3.2, seed * .1)
    s = f'<g transform="rotate({sway:.2f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x:.0f},{y-h_:.0f} l{h_*.34:.0f},{h_*.46:.0f} l{-h_*.12:.0f},0'
          f' l{h_*.3:.0f},{h_*.4:.0f} l{-h_*.14:.0f},0 l{h_*.26:.0f},{h_*.3:.0f}'
          f' l{-h_*.76:.0f},0 l{h_*.26:.0f},{-h_*.3:.0f} l{-h_*.14:.0f},0'
          f' l{h_*.3:.0f},{-h_*.4:.0f} l{-h_*.12:.0f},0 Z" fill="{ZEL}" {o(6)}/>')
    s += f'<rect x="{x-10:.0f}" y="{y:.0f}" width="20" height="30" fill="#6b4428" {o(4)}/>'
    for i in range(14):
        yy = y - h_ * (.12 + rnd.random() * .82)
        xx = x + rnd.uniform(-1, 1) * h_ * .28
        col = (KRAS, ZOL, "#4a7fb0")[i % 3]
        s += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="9" fill="{col}" {o(2)}/>'
    if ogonki:
        for i in range(10):
            yy = y - h_ * (.08 + i * .085)
            xx = x + math.sin(i * 1.3) * h_ * .22
            mig = 1.0 if ((t * 1.6 + i * .3) % 1.0) > .18 else .4
            s += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="6" fill="{SVET}" opacity="{mig:.2f}"/>'
    return s + '</g>'


def _napolnenie(x0, y0, w_, h_, t, seed, n=22):
    """Утварь у ОДНОЙ линии опоры (низ полосы x0..x0+w_, y0+h_): книга,
    банка, скрутка холста, рамка, яблоко, пряник — не висят в воздухе и не
    читаются пятном (R-0045, его слово 15.11: вещи узнаются по силуэту)."""
    rnd = random.Random(seed)
    vidy = ("kniga", "jar", "cloth", "frame", "yabloko", "bulka")
    s, posl = "", None
    baza_y = y0 + h_
    for i in range(n):
        v = rnd.choice([x for x in vidy if x != posl])
        posl = v
        cx = x0 + (i + rnd.uniform(.25, .75)) / n * w_
        sc = rnd.uniform(.75, 1.25)
        if v == "kniga":
            ww, hh = rnd.uniform(60, 86) * sc, rnd.uniform(90, 130) * sc
            cy = baza_y - hh
            col = rnd.choice((TKAN, TKAN2, MED, ZEL2, "#6b4428"))
            s += (f'<rect x="{cx-ww/2:.0f}" y="{cy:.0f}" width="{ww:.0f}" height="{hh:.0f}" rx="4"'
                  f' fill="{col}" {o(3)}/>'
                  f'<rect x="{cx-ww/2+6:.0f}" y="{cy+8:.0f}" width="{ww-12:.0f}" height="5"'
                  f' fill="#efe3c8" opacity=".6"/>')
        elif v == "jar":
            s += _banka(cx, baza_y - 6, sc * .82, rnd.choice((MED, "#8c8275")))
        elif v == "cloth":
            ww = rnd.uniform(80, 130) * sc
            col = rnd.choice((RUSH, KREM, TKAN))
            s += (f'<path d="M{cx-ww/2:.0f},{baza_y-36:.0f} q{ww*.5:.0f},{14*sc:.0f} {ww:.0f},0'
                  f' l0,{28*sc:.0f} q{-ww*.5:.0f},{10*sc:.0f} {-ww:.0f},0 Z" fill="{col}" {o(3)}/>')
        elif v == "frame":
            ww, hh = rnd.uniform(70, 96) * sc, rnd.uniform(90, 120) * sc
            cy = baza_y - hh
            s += (f'<rect x="{cx-ww/2:.0f}" y="{cy:.0f}" width="{ww:.0f}" height="{hh:.0f}" rx="4"'
                  f' fill="url(#derev)" {o(4)}/>'
                  f'<rect x="{cx-ww*.36+ww/2:.0f}" y="{cy+hh*.14:.0f}" width="{ww*.72:.0f}" height="{hh*.62:.0f}"'
                  f' fill="#cfd6de" opacity=".55"/>')
        elif v == "yabloko":
            r_ = rnd.uniform(20, 28) * sc
            cy = baza_y - r_
            s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r_:.0f}" fill="{rnd.choice((KRAS,ZOL))}" {o(2)}/>'
                  f'<path d="M{cx:.0f},{cy-r_:.0f} q6,-10 14,-6" fill="none" stroke="{ZEL}" stroke-width="3"/>')
        else:
            rx_, ry_ = rnd.uniform(30, 42) * sc, rnd.uniform(16, 22) * sc
            cy = baza_y - ry_
            s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx_:.0f}" ry="{ry_:.0f}" fill="{KREM}" {o(3)}/>'
                  f'<path d="M{cx-rx_*.4:.0f},{cy:.0f} q{rx_*.4:.0f},-7 {rx_*.8:.0f},0"'
                  f' fill="none" stroke="#c8a876" stroke-width="2" opacity=".6"/>')
    return s


def _sloi_fona(x0, y0, w_, h_, t, seed, n=5):
    """Несколько крупных перекрывающихся плоскостей (панели, драпировка,
    коврик) — поднимает число слоёв в центре кадра без раздувания объёма
    текста мелкими деталями."""
    # ВРЕМЕННО ОТКЛЮЧЕНО вкладкой 15.11: пять случайных полупрозрачных
    # прямоугольников поверх сцены накручивали метрику «слоёв», а в кадре
    # давали мутные цветные плашки поверх предметов. Насыщенность даём
    # настоящими вещами, а не подложками.
    return ""
    rnd = random.Random(seed + 900)
    cols = (TKAN2, "#4a3a2c", ZEL2, MED, "#2e3a4a", KAMEN2, DOSKA2, "#5a3a4a")
    s = ""
    for i in range(n):
        ww = w_ * rnd.uniform(.46, .82)
        hh = h_ * rnd.uniform(.4, .78)
        xx = x0 + rnd.uniform(0, max(1, w_ - ww))
        yy = y0 + rnd.uniform(0, max(1, h_ - hh))
        s += (f'<rect x="{xx:.0f}" y="{yy:.0f}" width="{ww:.0f}" height="{hh:.0f}" rx="14"'
              f' fill="{cols[(seed+i)%len(cols)]}" opacity=".5" {o(2)}/>')
    return s


def _chertenok(x, y, s_, t, ph=0.0):
    """Мелкий чертёнок: тянется к острому, хвост закручен, рожки и уши."""
    tyan = 10 * A.ease(A.seg((t + ph) % 2.4, .1, .6))
    s = f'<g transform="translate({tyan:.0f},0)">'
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{20*s_:.0f}" ry="{26*s_:.0f}" fill="{IMP}" {o(4)}/>'
    s += (f'<path d="M{x-14*s_:.0f},{y+20*s_:.0f} q{-10*s_:.0f},{20*s_:.0f} {2*s_:.0f},{30*s_:.0f}'
          f' q{10*s_:.0f},{-6*s_:.0f} {4*s_:.0f},{-26*s_:.0f} Z" fill="{IMP}" {o(3)}/>')
    for sgn in (-1, 1):
        s += (f'<path d="M{x+sgn*8*s_:.0f},{y-20*s_:.0f} l{sgn*10*s_:.0f},{-16*s_:.0f}'
              f' l{-sgn*4*s_:.0f},{18*s_:.0f} Z" fill="#2e1520" {o(3)}/>')
    s += f'<circle cx="{x-6*s_:.0f}" cy="{y-2*s_:.0f}" r="{3*s_:.0f}" fill="{SVET}"/>'
    s += f'<circle cx="{x+8*s_:.0f}" cy="{y-2*s_:.0f}" r="{3*s_:.0f}" fill="{SVET}"/>'
    return s + '</g>'


def _vesy(x, y, s_, t, nak=0.0, seed=1):
    """Чашечные весы: держат равновесие, но слегка качаются."""
    kach = 3 * A.w(t, 1.6, seed * .2) + nak
    s = f'<rect x="{x-8*s_:.0f}" y="{y-220*s_:.0f}" width="{16*s_:.0f}" height="{220*s_:.0f}" rx="6" fill="url(#zhel)" {o(5)}/>'
    s += f'<ellipse cx="{x:.0f}" cy="{y-220*s_:.0f}" rx="{30*s_:.0f}" ry="{10*s_:.0f}" fill="{ZHELEZ}" {o(4)}/>'
    s += f'<g transform="rotate({kach:.2f} {x:.0f} {y-220*s_:.0f})">'
    s += (f'<line x1="{x-150*s_:.0f}" y1="{y-220*s_:.0f}" x2="{x+150*s_:.0f}" y2="{y-220*s_:.0f}"'
          f' stroke="url(#zhel)" stroke-width="{8*s_:.0f}"/>')
    for sgn in (-1, 1):
        cx_ = x + sgn * 150 * s_
        s += (f'<line x1="{cx_:.0f}" y1="{y-220*s_:.0f}" x2="{cx_-26*s_:.0f}" y2="{y-120*s_:.0f}"'
              f' stroke="{K}" stroke-width="3"/>')
        s += (f'<line x1="{cx_:.0f}" y1="{y-220*s_:.0f}" x2="{cx_+26*s_:.0f}" y2="{y-120*s_:.0f}"'
              f' stroke="{K}" stroke-width="3"/>')
        s += (f'<ellipse cx="{cx_:.0f}" cy="{y-110*s_:.0f}" rx="{46*s_:.0f}" ry="{16*s_:.0f}"'
              f' fill="url(#zhel)" {o(5)}/>')
    s += '</g>'
    return s


def _kovrik_pol(x, y, w_, h_, col1=None, col2=None, seed=1):
    """Половик на полу: бордюр и ряд узорных кружков — настоящая вещь."""
    rnd = random.Random(seed)
    col1 = col1 or TKAN
    col2 = col2 or KREM
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="{col1}" {o(5)}/>'
    s += (f'<rect x="{x+16:.0f}" y="{y+16:.0f}" width="{w_-32:.0f}" height="{h_-32:.0f}"'
          f' fill="none" stroke="{col2}" stroke-width="6" opacity=".7"/>')
    n = max(2, int(w_ / 90))
    for i in range(n):
        s += (f'<circle cx="{x+50+i*(w_-100)/max(1,n-1):.0f}" cy="{y+h_*.5:.0f}" r="12"'
              f' fill="{col2}" opacity=".6"/>')
    return s


def _kartiny_ryad(x, y, n=3, seed=1, w_=110, h_=150):
    """Ряд рамок на стене: рама, паспарту и пятно рисунка — не пустая стена."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        fx = x + i * (w_ + 50)
        s += f'<rect x="{fx:.0f}" y="{y:.0f}" width="{w_}" height="{h_}" rx="4" fill="url(#derev)" {o(4)}/>'
        s += (f'<rect x="{fx+14:.0f}" y="{y+14:.0f}" width="{w_-28}" height="{h_-28}"'
              f' fill="{rnd.choice((KREM,"#cfd6de",TKAN2))}" opacity=".85"/>')
    return s


def _oboi_fon(col1=None, col2=None, n=14):
    """Оклеенная стена городской комнаты — отличает её от сруба избы."""
    col1 = col1 or "#5a4a5a"
    col2 = col2 or "#4a3a4a"
    s = f'<rect width="{W}" height="780" fill="{col1}"/>'
    for i in range(n):
        xx = i * (W / n)
        s += f'<rect x="{xx:.0f}" y="0" width="{W/n*.5:.0f}" height="780" fill="{col2}" opacity=".4"/>'
    s += f'<rect y="760" width="{W}" height="26" fill="#2a2420" {o(4)}/>'
    return s


def _nozh_bolshoy(x, y, h_, t, ang=0.0, col=None):
    """Большой нож: лезвие и рукоять ОДНИМ силуэтом (острие сверху, у
    острия чуть колышется), заклёпки на рукояти, блик по лезвию."""
    col = col or ZHELEZ
    w_ = h_ * .24
    sway = 2 * A.w(t, 1.6) + ang
    s = f'<g transform="rotate({sway:.1f} {x:.0f} {y:.0f})">'
    s += ten(x, y + h_ * .04, w_ * 1.6, 14, .4)
    s += (f'<path d="M{x:.0f},{y-h_:.0f} L{x+w_*.9:.0f},{y-h_*.42:.0f}'
          f' L{x+w_*.5:.0f},{y-h_*.2:.0f} L{x+w_*.5:.0f},{y:.0f}'
          f' L{x-w_*.5:.0f},{y:.0f} L{x-w_*.5:.0f},{y-h_*.2:.0f}'
          f' L{x-w_*.9:.0f},{y-h_*.4:.0f} Z" fill="{col}" {o(6)}/>')
    s += (f'<rect x="{x-w_*.42:.0f}" y="{y-h_*.2:.0f}" width="{w_*.84:.0f}" height="{h_*.2:.0f}"'
          f' rx="8" fill="#5a3a26" {o(5)}/>')
    for i in range(3):
        s += f'<circle cx="{x:.0f}" cy="{y-h_*.16+i*h_*.06:.0f}" r="{w_*.08:.0f}" fill="{K}"/>'
    s += (f'<path d="M{x-w_*.28:.0f},{y-h_*.9:.0f} L{x-w_*.06:.0f},{y-h_*.28:.0f}"'
          f' stroke="#eef4fa" stroke-width="{max(3,w_*.05):.0f}" opacity=".55" stroke-linecap="round"/>')
    return s + '</g>'


def _nozhnicy_bolshie(x, y, h_, t, ang=0.0):
    """Большие портновские ножницы: два лезвия и колечки одним крестом,
    заклёпка-винт в середине."""
    sway = 3 * A.w(t, 1.4) + ang
    s = f'<g transform="rotate({sway:.1f} {x:.0f} {y:.0f})">'
    s += ten(x, y + h_ * .42, h_ * .32, 16, .4)
    for sgn in (-1, 1):
        s += (f'<path d="M{x:.0f},{y-h_:.0f} L{x+sgn*h_*.16:.0f},{y-h_*.08:.0f}'
              f' L{x+sgn*h_*.3:.0f},{y+h_*.3:.0f} Q{x+sgn*h_*.3:.0f},{y+h_*.42:.0f}'
              f' {x+sgn*h_*.18:.0f},{y+h_*.42:.0f} Q{x+sgn*h_*.08:.0f},{y+h_*.42:.0f}'
              f' {x+sgn*h_*.08:.0f},{y+h_*.3:.0f} Z" fill="{ZHELEZ}" {o(5)}/>')
    s += f'<circle cx="{x:.0f}" cy="{y-h_*.08:.0f}" r="{h_*.05:.0f}" fill="{K}"/>'
    s += f'<circle cx="{x:.0f}" cy="{y-h_*.08:.0f}" r="{h_*.02:.0f}" fill="{SVET}" opacity=".7"/>'
    return s + '</g>'


def _veshalka_seni(x, y, w_, t, seed=1, kant=None):
    """Вешалка в сенях: крюки, тулуп на плечиках, ведро, корзина."""
    rnd = random.Random(seed)
    s = f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+w_:.0f}" y2="{y:.0f}" stroke="url(#derev)" stroke-width="16"/>'
    for i in range(3):
        hx = x + w_ * .18 + i * w_ * .32
        s += (f'<path d="M{hx-10:.0f},{y:.0f} q0,{30:.0f} 20,30 q20,0 20,-30"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="6"/>')
    cx = x + w_ * .22
    kach = 2 * A.w(t, 1.6, seed * .1)
    s += (f'<g transform="rotate({kach:.1f} {cx:.0f} {y+30:.0f})">'
          f'<path d="M{cx-66:.0f},{y+16:.0f} q-14,160 10,318 q56,30 112,0 q24,-158 10,-318'
          f' q-66,-28 -132,0 Z" fill="{TKAN2}" {o(6)}/>'
          f'<ellipse cx="{cx:.0f}" cy="{y+24:.0f}" rx="48" ry="16" fill="{TKAN2}" {o(4)}/>'
          f'<path d="M{cx-40:.0f},{y+40:.0f} q40,20 80,0" fill="none" stroke="{kant or SVET}"'
          f' stroke-width="4" opacity=".5"/></g>')
    bx = x + w_ * .58
    s += (f'<path d="M{bx-42:.0f},{y+300:.0f} l10,-130 h64 l10,130 Z" fill="{ZHELEZ}" {o(5)}/>'
          f'<ellipse cx="{bx:.0f}" cy="{y+170:.0f}" rx="42" ry="10" fill="{ZHELEZ}" {o(3)}/>'
          f'<path d="M{bx-30:.0f},{y+160:.0f} q30,-26 60,0" fill="none" stroke="{ZHELEZ}" stroke-width="5"/>')
    kx_ = x + w_ * .86
    s += (f'<path d="M{kx_-54:.0f},{y+300:.0f} q10,-64 54,-64 q44,0 54,64 Z" fill="url(#solom)" {o(5)}/>')
    for i in range(4):
        s += (f'<line x1="{kx_-42+i*28:.0f}" y1="{y+246:.0f}" x2="{kx_-42+i*28:.0f}" y2="{y+298:.0f}"'
              f' stroke="#a07c2e" stroke-width="4"/>')
    s += f'<rect x="{x+w_*.4:.0f}" y="{y+300:.0f}" width="80" height="60" rx="8" fill="#4a3a2a" {o(4)}/>'
    s += f'<rect x="{x+w_*.4+6:.0f}" y="{y+300:.0f}" width="34" height="56" rx="6" fill="#2a1f14" {o(3)}/>'
    return s


def _koza_hozyayka(x, y, h_, t):
    """Огненная Коза — хозяйка года: крупная, рога дугой, пламя в гриве и хвосте."""
    w_ = h_ * .62
    dy = 3 * A.w(t, .9)
    s = f'<g transform="translate(0,{dy:.1f})">'
    s += ten(x, y + 10, w_ * .55, 16, .5)
    for i, sgn in enumerate((-1, 1)):
        lx = x + sgn * w_ * .22
        s += f'<rect x="{lx-16:.0f}" y="{y-h_*.30:.0f}" width="32" height="{h_*.30:.0f}" rx="12" fill="#b23a2c" {o(6)}/>'
    s += (f'<path d="M{x-w_*.5:.0f},{y-h_*.30:.0f} q{w_*.1:.0f},{-h_*.5:.0f} {w_*.5:.0f},{-h_*.56:.0f}'
          f' q{w_*.4:.0f},{h_*.06:.0f} {w_*.5:.0f},{h_*.5:.0f} q0,{h_*.14:.0f} {-w_*.5:.0f},{h_*.16:.0f}'
          f' q{-w_*.5:.0f},{-h_*.02:.0f} {-w_*.5:.0f},{-h_*.6:.0f} Z" fill="#c23c2e" {o(7)}/>')
    hx, hy = x + w_ * .46, y - h_ * .78
    s += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{h_*.17:.0f}" fill="#c23c2e" {o(6)}/>'
    for sgn in (-1, 1):
        s += (f'<path d="M{hx+sgn*8:.0f},{hy-h_*.1:.0f} q{sgn*h_*.12:.0f},{-h_*.18:.0f} {sgn*h_*.02:.0f},{-h_*.3:.0f}'
              f' q{-sgn*h_*.1:.0f},{h_*.04:.0f} {-sgn*h_*.02:.0f},{h_*.3:.0f} Z" fill="#7a2a20" {o(4)}/>')
    bl = 1 if not A.blink(t, 3.6) else 0
    s += f'<ellipse cx="{hx+h_*.08:.0f}" cy="{hy:.0f}" rx="{h_*.035:.0f}" ry="{(h_*.045) if bl else 1.4:.1f}" fill="#1a1008"/>'
    if bl:
        s += f'<circle cx="{hx+h_*.09:.0f}" cy="{hy-h_*.012:.0f}" r="{h_*.014:.0f}" fill="#fff"/>'
    s += ogon(hx - h_ * .02, hy - h_ * .22, t, h_ / 540, .2, 5, SVET)
    s += ogon(x - w_ * .32, y - h_ * .3, t, h_ / 560, .5, 5, ORA)
    s += teplo(x, y - h_ * .4, h_ * .62, h_ * .5, .42 + .1 * abs(A.w(t, 1.3)))
    return s + '</g>'


# ═══════════════════════════ ДЕКОРАЦИИ 1-10 ═══════════════════════════════
def ognennaya_koza_u_elki_s_podarkami(t):
    """Коза-хозяйка носом подталкивает гору свёртков к зрителю, ёлка в
    огоньках слева. Единственное тёплое пятно — пламя в её гриве и хвосте."""
    rnd = random.Random(401)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, _oboi_fon("#3a2c38", "#2e2230"))
    s += SL(Z_DAL, okno_izby(1540, 160, 260, 320, t, svet=False, moroz=.5))
    s += SL(Z_DAL, _kartiny_ryad(1020, 150, 2, 6, 100, 130))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _kovrik_pol(560, 940, 700, 130, TKAN, KREM, 2))
    s += SL(Z_SRED, _servant(1300, 240, 520, 600, t))
    s += SL(Z_SRED, _elka(300, 900, 660, t, 7, True))
    rnd2 = random.Random(2)
    svertki = []
    for i in range(6):
        svertki.append((760 + i * 86 + rnd2.uniform(-10, 10), 920 - (i % 3) * 20))
    push = 14 * A.ease(A.seg(t % 2.4, .2, .9))
    sv = ""
    for i, (sx, sy) in enumerate(svertki):
        if i % 3 == 0:
            sv += _korobka(sx + push - 30, sy - 60, 90, 70, t, (TKAN2, ZEL2, MED)[i % 3], ZOL, True, .0, i * .2)
        else:
            sv += _svertok(sx + push, sy, 1.3 + (i % 2) * .3, t, (RUSH, KREM, TKAN2)[i % 3],
                            (TKAN, ZOL, MED)[i % 3], i * .3)
        if i % 2 == 0:
            sv += (f'<circle cx="{sx+push-10:.0f}" cy="{sy-50:.0f}" r="10" fill="url(#med)"'
                   f' opacity="{.5+.4*abs(A.w(t,2.1,i*.2)):.2f}" {o(2)}/>')
    s += SL(Z_SRED, sv)
    s += SL(Z_SRED, _koza_hozyayka(1140, 980, 580, t))
    s += SL(Z_SRED, f'<path d="M700,1010 q380,40 760,0 l20,70 h-800 Z" fill="#6b4a3c" opacity=".85"/>')
    s += SL(Z_SRED, hodiki(1700, 420, t, 1.0))
    s += SL(Z_SRED, lampa(220, 420, t, .9, True))
    s += SL(Z_SRED, f'<rect x="360" y="700" width="260" height="50" rx="10" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, krynka(430, 700, 1.3))
    s += SL(Z_PERED, ramka_pp("pravo", "#120e10", .5))
    s += SL(Z_PERED, goloe_derevo(60, 1040, 260, t, 4, 5, "#241820"))
    s += vinetka(.44)
    return s


def tri_pravilnyh_podarka(t):
    """Три подарка на столе под ёлкой подпрыгивают по очереди и получают
    бирки."""
    rnd = random.Random(402)
    s = sumerki_fon(t)
    s += SL(Z_DAL, ulica_dal(0, 760, W, t, True, 12))
    s += SL(Z_DAL, okno_izby(1560, 120, 260, 300, t, svet=True, moroz=.4))
    s += SL(Z_SRED, teplo(1690, 270, 260, 220, .4))
    s += SL(Z_SRED, _kartiny_ryad(620, 260, 3, 6, 110, 150))
    s += SL(Z_SRED, f'<rect x="470" y="420" width="420" height="18" rx="5" fill="url(#derev)" {o(4)}/>')
    s += mebel_hlam(410, 760, 260, t, 4)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, _kovrik_pol(460, 900, 760, 120, TKAN2, KREM, 4))
    s += SL(Z_SRED, _elka(1400, 940, 640, t, 14, True))
    s += SL(Z_SRED, stol(560, 760, 820, 36))
    jump = lambda ph: 20 * A.out(A.seg((t + ph) % 2.6, .05, .4)) * (1 if (t + ph) % 2.6 < .5 else 0)
    items = [(740, "varezhka"), (1000, "banka"), (1260, "svistulka")]
    for i, (ix, kind) in enumerate(items):
        iy = 740 - jump(i * .5)
        if kind == "varezhka":
            s += SL(Z_SRED, _varezhka(ix, iy, 2.6, 8 * A.w(t, 2.0, i * .3)))
            s += SL(Z_SRED, _varezhka(ix + 70, iy + 4, 2.3, -6))
        elif kind == "banka":
            s += SL(Z_SRED, _banka(ix, iy, 2.3))
        else:
            s += SL(Z_SRED, _svistulka(ix, iy, 1.8, 6 * A.w(t, 2.2, .4)))
        birka = 1 if (t + i * .5) % 2.6 > 1.2 else 0
        if birka:
            s += SL(Z_SRED, f'<rect x="{ix-16:.0f}" y="{iy-96:.0f}" width="40" height="26" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M560,738 l820,0 l-4,-6 l-812,0 Z" fill="{DOSKA2}" opacity=".7"/>')
    s += SL(Z_SRED, lampa(1660, 360, t, 1.0, True))
    s += SL(Z_SRED, _napolnenie(460, 300, 900, 560, t, 16, 8))
    s += SL(Z_SRED, _napolnenie(900, 260, 500, 480, t, 17, 5))
    s += SL(Z_PERED, goloe_derevo(1900, 1040, 220, t, 6, 4, "#2a2b33"))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 7, .5, .8))
    s += vinetka(.4)
    return s


def tri_podarka_u_zakrytoy_dveri(t):
    """У входной двери три коробки, рукав бабушки в проёме отодвигает их от
    порога."""
    rnd = random.Random(403)
    s = sumerki_fon(t)
    s += SL(Z_DAL, ulica_dal(0, 700, W, t, True, 4))
    s += SL(Z_DAL, panelka(60, 1020, 560, t, 5, True, 6))
    dx_, dy_, dw, dh = 760, 300, 380, 700
    s += SL(Z_SRED, dver(dx_, dy_, dw, dh, .22, kruchok=True))
    s += SL(Z_SRED, f'<path d="M{dx_-20:.0f},{dy_-40:.0f} q{dw*.5:.0f},-30 {dw+40:.0f},0 l0,30 l{-dw-40:.0f},0 Z" fill="{ZEL}" {o(5)}/>')
    for i in range(8):
        a = i / 8 * 6.28
        s += (f'<circle cx="{dx_+dw*.5+math.cos(a)*(dw*.5+8):.0f}" cy="{dy_-18+math.sin(a)*22:.0f}"'
              f' r="8" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="{dx_-40:.0f}" y="{dy_+dh:.0f}" width="{dw+80:.0f}" height="30" rx="8" fill="#5a4a3a" {o(4)}/>')
    box1 = _korobka(dx_ + 20, dy_ + dh - 160, 160, 150, t, TKAN, ZOL, True, .0, .1)
    box1 += (f'<ellipse cx="{dx_+100:.0f}" cy="{dy_+dh-200:.0f}" rx="40" ry="14" fill="url(#zol)" {o(3)}/>')
    box2 = _korobka(dx_ + 190, dy_ + dh - 140, 150, 130, t, TKAN2, SVET, True, .0, .4)
    box2 += (f'<rect x="{dx_+230:.0f}" y="{dy_+dh-180:.0f}" width="12" height="60" rx="4" fill="#5a4a3a" {o(3)}/>')
    box3 = _korobka(dx_ + 20, dy_ + dh - 100, 320, 90, t, KREM, TKAN, True, .4, .7)
    box3 += (f'<path d="M{dx_+160:.0f},{dy_+dh-140:.0f} q30,-10 50,20 q-30,10 -50,-20 Z" fill="none" stroke="#9aa0a4" stroke-width="2" opacity=".6"/>')
    push = -40 * A.ease(A.seg(t, .4, 1.2))
    s += SL(Z_SRED, f'<g transform="translate({push:.0f},0)">{box1}{box2}{box3}</g>')
    open_ = A.ease(A.seg(t, .2, .5)) - A.ease(A.seg(t, 1.6, .5))
    rx = dx_ + dw * .5
    s += SL(Z_SRED, f'<rect x="{rx-20:.0f}" y="{dy_+dh*.35:.0f}" width="40" height="{140*max(.1,open_):.0f}"'
                    f' rx="16" fill="#8f353c" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{dy_+dh*.35+140*max(.1,open_):.0f}" rx="26" ry="19" fill="#8f353c" {o(4)}/>')
    s += SL(Z_SRED, teplo(rx, dy_ + dh * .5, 260, 220, .3))
    s += SL(Z_SRED, lampa(dx_ + dw + 220, dy_ + 160, t, .85, False))
    s += SL(Z_DAL, gryaz_polosa(1024, 90, "#2a2e38"))
    # санки у стены — две полозья и дощатый настил
    skx, sky = 500, 980
    s += SL(Z_SRED, f'<path d="M{skx-70:.0f},{sky:.0f} q-10,-20 20,-30 l0,-90 q-10,-16 10,-20"'
                    f' fill="none" stroke="url(#derev)" stroke-width="10"/>')
    s += SL(Z_SRED, f'<path d="M{skx+10:.0f},{sky:.0f} q-10,-20 20,-30 l0,-90 q-10,-16 10,-20"'
                    f' fill="none" stroke="url(#derev)" stroke-width="10"/>')
    s += SL(Z_SRED, f'<rect x="{skx-66:.0f}" y="{sky-110:.0f}" width="130" height="70" rx="6" fill="url(#dosk)" {o(5)}/>')
    # лыжи у крыльца
    lx = 1360
    for sgn in (-1, 1):
        s += SL(Z_SRED, f'<path d="M{lx+sgn*16:.0f},{dy_+dh:.0f} l0,-440 q0,-16 {sgn*14:.0f},-16"'
                        f' fill="none" stroke="#8a5a30" stroke-width="12" stroke-linecap="round"/>')
    # почтовый ящик на столбе
    pyx, pyy = 1460, 760
    s += SL(Z_SRED, f'<rect x="{pyx-12:.0f}" y="{pyy:.0f}" width="24" height="120" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{pyx-34:.0f}" y="{pyy-50:.0f}" width="68" height="54" rx="10" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{pyx-10:.0f}" y="{pyy-30:.0f}" width="20" height="8" fill="{KREM}" opacity=".8"/>')
    # веник у крыльца
    vx = 1240
    s += SL(Z_SRED, f'<line x1="{vx:.0f}" y1="{dy_+dh:.0f}" x2="{vx:.0f}" y2="{dy_+dh-160:.0f}" stroke="#6b4428" stroke-width="10"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{vx-18+i*9:.0f}" y1="{dy_+dh:.0f}" x2="{vx+i*2-10:.0f}" y2="{dy_+dh-60:.0f}" stroke="#a07c2e" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="60" y="860" width="30" height="220" rx="10" fill="#6b4a2e" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="100" y="880" width="30" height="200" rx="10" fill="#6b4a2e" {o(4)}/>')
    s += SL(Z_SRED, _napolnenie(900, 700, 300, 220, t, 17, 3))
    s += SL(Z_PERED, ramka_pp("levo", "#100c0e", .55))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 9, .6, 1.0))
    s += vinetka(.42)
    return s


def podarok_govorit(t):
    """Коробка приподнимает крышку и выпускает облачко-слово; бабушка за
    столом слушает и кивает."""
    rnd = random.Random(404)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 8)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 90))
    s += SL(Z_DAL, okno_izby(1500, 160, 260, 220, t, svet=False, moroz=.4))
    s += SL(Z_DAL, _kartiny_ryad(560, 160, 2, 8, 100, 130))
    s += utvar_izby(100, 400, 280, t, 8)
    s += SL(Z_SRED, polovicy(840))
    s += SL(Z_SRED, _kovrik_pol(420, 940, 680, 110, TKAN, KREM, 8))
    s += SL(Z_SRED, stol(360, 780, 820, 34))
    s += SL(Z_SRED, krynka(1080, 780, 1.0))
    s += SL(Z_SRED, karavay(680, 760, .8, True))
    otkr = .3 + .25 * abs(A.w(t, 1.2, .1))
    s += SL(Z_SRED, _korobka(560, 640, 220, 180, t, TKAN, ZOL, True, otkr, .2))
    rost = A.out(A.seg(t % 3.2, .3, 1.0))
    s += SL(Z_SRED, _oblachko(760, 560 - 60 * rost, .7 + .5 * rost, t, .2, "serdce"))
    s += SL(Z_SRED, svecha(900, 700, t, .1, 1.1))
    s += SL(Z_SRED, f'<rect x="300" y="660" width="90" height="20" rx="6" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="420" cy="700" rx="40" ry="16" fill="#efe3c8" {o(3)}/>')
    s += SL(Z_SRED, par(420, 684, t, 3, .4, 120, .5))
    s += SL(Z_SRED, f'<ellipse cx="1000" cy="680" rx="60" ry="30" fill="{KREM}" {o(4)}/>')
    kiv = 5 * A.w(t, 1.4, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kiv:.1f} 1150 940)">'
                    + figura(1150, 1060, 520, t, "#3a2c3c", "#ffe2a8", True, .2) + '</g>')
    s += SL(Z_SRED, f'<rect x="1030" y="1010" width="300" height="20" rx="6" fill="{TKAN}" opacity=".7"/>')
    s += SL(Z_SRED, pech(1140, 300, 460, 640, t, True, True, False))
    s += SL(Z_SRED, _napolnenie(420, 600, 600, 260, t, 19, 6))
    s += SL(Z_SRED, f'<rect x="420" y="320" width="320" height="420" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="350" width="280" height="160" rx="6" fill="url(#stekl)" opacity=".6" {o(4)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#120e0c", .45))
    s += SL(Z_LETIT, mokryy_sneg(t, 14, 6, .4, .7))
    s += vinetka(.42)
    return s


def babushka_i_cennik(t):
    """Продавщица показывает на ценник, бабушка отводит его рукавом и
    слушает платок у уха."""
    rnd = random.Random(405)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("den", t, False, 2)
    s += SL(Z_DAL, brevna(0, 40, W, 700, 86))
    s += SL(Z_DAL, okno_izby(1560, 120, 240, 220, t, svet=False, moroz=.2))
    s += utvar_pekarni(1180, 720, 420, t, 2)
    s += SL(Z_SRED, polovicy(760))
    s += SL(Z_SRED, lampa(960, 160, t, 1.0, True))
    pril = f'<rect x="200" y="640" width="1200" height="140" rx="10" fill="url(#derev)" {o(7)}/>'
    pril += f'<rect x="200" y="780" width="1200" height="220" fill="#4a3528" {o(6)}/>'
    s += SL(Z_SRED, pril)
    s += SL(Z_SRED, f'<rect x="280" y="560" width="220" height="100" rx="8" fill="{ZHELEZ}" {o(5)}/>')
    kach = 2 * A.w(t, 1.6, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 390 600)"><line x1="330" y1="600" x2="450" y2="600"'
                    f' stroke="url(#zhel)" stroke-width="6"/>'
                    f'<circle cx="330" cy="600" r="26" fill="{TKAN}" opacity=".7"/>'
                    f'<circle cx="450" cy="600" r="26" fill="{TKAN}" opacity=".7"/></g>')
    s += SL(Z_SRED, f'<rect x="560" y="560" width="200" height="50" rx="10" fill="#6b4a2e" {o(4)}/>')
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{570+i*30}" y="580" width="24" height="60" rx="3" fill="{(KRAS,SVET)[i%2]}" opacity=".7"/>')
    cen_off = 46 * A.ease(A.seg(t, .3, .9))
    s += SL(Z_SRED, f'<rect x="{820+cen_off:.0f}" y="600" width="160" height="40" rx="6" fill="{TKAN}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{830+cen_off:.0f}" y="608" width="60" height="24" rx="3" fill="{KREM}" {o(2)}/>')
    s += SL(Z_SRED, figura(430, 780, 480, t, "#8a6a4a", "#efe3c8", False, .0))
    ruk1, (r1x, r1y) = rukav(560, 600, 150, -4 + 6 * A.w(t, 1.9, .1), t, "#8a6a4a", "#efe3c8", .1)
    s += SL(Z_SRED, ruk1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="24" ry="17" fill="#8a6a4a" {o(4)}/>')
    s += SL(Z_SRED, figura(1000, 940, 520, t, "#2a2c3c", "#cfe4f5", False, .3))
    plat_ear = 6 * A.w(t, 1.5, .4)
    ruk2, (r2x, r2y) = rukav(1120, 760, 170, -70 + plat_ear, t, "#2a2c3c", "#cfe4f5", .4)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="24" ry="17" fill="#2a2c3c" {o(4)}/>')
    s += SL(Z_SRED, _varezhka(r2x, r2y - 10, 1.4, 0, TKAN))
    s += SL(Z_SRED, f'<rect x="{900-cen_off*.3:.0f}" y="620" width="140" height="130" rx="10" fill="{TKAN}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="260" width="420" height="340" rx="10" fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="720" y="{280+i*108:.0f}" width="380" height="90" rx="6" fill="none" {o(3)}/>')
    rnd3 = random.Random(9)
    for i in range(7):
        jx = 740 + i * 52
        jy = 280 + (i % 3) * 108 + 70
        s += SL(Z_SRED, _banka(jx, jy, .7, rnd3.choice((MED, "#8c8275"))))
    s += SL(Z_SRED, _napolnenie(420, 600, 300, 200, t, 19, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, luch(1560, 160, 160, 500, t, .18))
    s += vinetka(.4)
    return s


def tri_govoryaschie_veschi(t):
    """На подоконнике три вещи по словам всплывают облачками; рядом коробка
    с проёмом под настоящий кадр."""
    rnd = random.Random(406)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, True, 14)
    s += SL(Z_DAL, oblaka(t, 150, 3, 9, .3, "#c3cedd", 11.0))
    s += SL(Z_DAL, okno_izby(120, 140, 900, 420, t, svet=False, moroz=.55))
    s += SL(Z_SRED, f'<rect x="60" y="560" width="1020" height="80" rx="10" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, _kovrik_pol(460, 900, 600, 110, TKAN2, KREM, 9))
    seg = A.seg(t % 6.8, 0, 6.8)
    stage = 0 if seg < .34 else (1 if seg < .67 else 2)
    items = (("koshelek", 460), ("banka", 680), ("varezhka", 900))
    for i, (kind, ix) in enumerate(items):
        rise = 30 * A.out(A.seg(t % 6.8, i * .2, .5))
        iy = 560 - rise
        if kind == "koshelek":
            s += SL(Z_SRED, _koshelek(ix, iy, 1.2, True, 1))
            kinds = "moneta"
        elif kind == "banka":
            s += SL(Z_SRED, _banka(ix, iy, 1.3))
            kinds = "serdce"
        else:
            s += SL(Z_SRED, _varezhka(ix, iy, 1.9, 6 * A.w(t, 1.6, i * .2)))
            kinds = "ruki"
        if i <= stage:
            s += SL(Z_SRED, _oblachko(ix, iy - 110, .8, t, i * .3, kinds))
    s += SL(Z_SRED, f'<rect x="1140" y="540" width="40" height="200" rx="14" fill="{ZEL}" {o(4)}/>')
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M1160,{560+i*30} l-22,10 M1160,{560+i*30} l22,10" stroke="{ZEL}" stroke-width="5"/>')
    pw, ph_ = 760, 320
    px, py = 1180, 480
    # план 6: настоящий кадр (вязаные варежки) ставится в проём стенки;
    # план 7 той же декорации сток не требует, но метка должна быть всегда.
    put = kontur_proema(px, py, pw, ph_, "pryam")
    korob = f'<path d="{put}" fill="#1a140e"/>'
    korob += mesto_stoka(px, py, pw, ph_, "pryam")
    korob += f'<path d="{put}" fill="none" {o(6)}/>'
    korob += f'<rect x="{px-30:.0f}" y="{py-30:.0f}" width="{pw+60}" height="40" fill="{TKAN2}" {o(6)}/>'
    korob += f'<rect x="{px-30:.0f}" y="{py+ph_:.0f}" width="{pw+60}" height="180" fill="{TKAN2}" {o(6)}/>'
    s += SL(Z_SRED, korob)
    s += SL(Z_SRED, svecha(1120, 760, t, .2, 1.0))
    s += SL(Z_SRED, f'<path d="M160,780 l-16,-120 l40,20 l16,100 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="1000" cy="720" r="30" fill="url(#glina)" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="280" width="340" height="300" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _dvertsy_shkafa(420, 280, 340, 300, 150))
    s += SL(Z_SRED, _napolnenie(420, 600, 900, 200, t, 20, 6))
    s += SL(Z_PERED, ramka_pp("levo", "#120e10", .42))
    s += SL(Z_LETIT, sneg_letit(t, 20, 11, .5, .9))
    s += vinetka(.4)
    return s


def _dvertsy_shkafa(x, y, w_, h_, glass_h, col="#3a2416"):
    """Дверцы шкафа/буфета: за стеклом сверху посуда, на глухой нижней части
    филёнка и ручки, шов между створками по всей высоте. Довод четырёх сцен,
    где мебель стояла серой плашкой без деталей (хвост 15.11)."""
    mid = x + w_ * .5
    gx, gy, gw, gh = x + w_ * .07, y + 16, w_ * .86, glass_h - 30
    s = (f'<ellipse cx="{gx+gw*.28:.0f}" cy="{gy+gh*.74:.0f}" rx="{gw*.16:.0f}" ry="8"'
         f' fill="{KREM}" opacity=".85"/>')
    s += (f'<ellipse cx="{gx+gw*.28:.0f}" cy="{gy+gh*.58:.0f}" rx="{gw*.16:.0f}" ry="8"'
          f' fill="{KREM}" opacity=".85"/>')
    s += (f'<path d="M{gx+gw*.6:.0f},{gy+gh*.82:.0f} v{-gh*.46:.0f} q0,-10 10,-10'
          f' h{gw*.2:.0f} q10,0 10,10 v{gh*.46:.0f} Z" fill="url(#glina)" opacity=".85" {o(2)}/>')
    s += (f'<rect x="{gx:.0f}" y="{gy:.0f}" width="{gw:.0f}" height="{gh:.0f}" rx="4"'
          f' fill="url(#stekl)" opacity=".4" {o(3)}/>')
    s += f'<line x1="{mid:.0f}" y1="{y:.0f}" x2="{mid:.0f}" y2="{y+h_:.0f}" stroke="{col}" stroke-width="4" opacity=".6"/>'
    pan_y, pan_h = y + glass_h + 16, h_ - glass_h - 32
    if pan_h > 24:
        for lx in (x + w_ * .08, mid + w_ * .08):
            s += (f'<rect x="{lx:.0f}" y="{pan_y:.0f}" width="{w_*.34:.0f}" height="{pan_h:.0f}" rx="8"'
                  f' fill="none" stroke="{col}" stroke-width="5" opacity=".55"/>')
    hy = y + h_ * .52
    for hx in (mid - w_ * .07, mid + w_ * .07):
        s += f'<rect x="{hx:.0f}" y="{hy:.0f}" width="10" height="46" rx="5" fill="{ZHELEZ}" {o(2)}/>'
    return s


def kalendar_s_novym_godom(t):
    """Отрывной календарь: бабушка со стремянки отрывает последний листок
    декабря, под ним новогодняя обложка."""
    rnd = random.Random(407)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 5)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += utvar_izby(1200, 420, 360, t, 5)
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _kovrik_pol(500, 900, 560, 110, TKAN, KREM, 21))
    s += SL(Z_SRED, f'<rect x="1200" y="300" width="300" height="600" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _dvertsy_shkafa(1200, 300, 300, 600, 280))
    s += SL(Z_SRED, f'<rect x="420" y="420" width="260" height="480" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="440" width="220" height="18" rx="5" fill="url(#derev)" {o(4)}/>')
    kx, ky = 760, 320
    s += SL(Z_SRED, f'<rect x="{kx-130:.0f}" y="{ky-200:.0f}" width="260" height="360" rx="10" fill="{KREM}" {o(6)}/>')
    otr = A.ease(A.seg(t, .5, 1.0))
    s += SL(Z_SRED, f'<g transform="rotate({otr*60:.1f} {kx-110:.0f} {ky-80:.0f})">'
                    f'<rect x="{kx-110:.0f}" y="{ky-170:.0f}" width="220" height="160" fill="#fff" {o(4)}/></g>')
    s += SL(Z_SRED, f'<rect x="{kx-110:.0f}" y="{ky:.0f}" width="220" height="130" fill="{KRAS}" {o(5)}/>')
    s += SL(Z_SRED, _koza_hozyayka(kx, ky + 100, 160, t))
    s += SL(Z_SRED, hodiki(1400, 300, t, 1.1))
    s += SL(Z_SRED, f'<rect x="300" y="500" width="180" height="24" rx="6" fill="url(#derev)" {o(5)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="{320+i*50}" y="420" width="40" height="80" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M560,560 l-30,-60 l60,0 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="530" cy="500" r="16" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="80" y="520" width="12" height="440" fill="#6b4a2e" {o(4)}/>')
    stoy = figura(120, 980, 540, t, "#3a2c3c", "#ffd98a", True, .0)
    s += SL(Z_SRED, stoy)
    ruk, (rx, ry) = rukav(190, 640, 150, -70, t, "#3a2c3c", "#ffd98a", .0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="24" ry="17" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, lampa(1660, 420, t, .95, True))
    s += SL(Z_SRED, f'<rect x="760" y="500" width="380" height="400" rx="10" fill="#3a3028" opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 1080, 200, t, 21, 7))
    s += SL(Z_PERED, ramka_pp("pravo", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 8, .5, .7))
    s += vinetka(.42)
    return s


def monetka_za_podarok(t):
    """Две руки над столом: коробка с ножницами переходит, монетка ложится
    на ладонь, запрещающая черта гаснет и зажигается галочка."""
    rnd = random.Random(408)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 9)
    s += SL(Z_DAL, okno_izby(1560, 120, 260, 260, t, svet=True, moroz=.3))
    s += SL(Z_SRED, teplo(1690, 260, 260, 220, .38))
    s += utvar_izby(80, 440, 480, t, 11)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="320" width="300" height="500" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="340" width="260" height="220" rx="6" fill="url(#stekl)" opacity=".55" {o(4)}/>')
    s += SL(Z_SRED, hodiki(1420, 360, t, 1.0))
    s += SL(Z_SRED, f'<rect x="900" y="260" width="340" height="260" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, _kartiny_ryad(940, 290, 2, 12, 110, 150))
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN, KREM, 24))
    s += SL(Z_SRED, stol(460, 760, 900, 36))
    s += SL(Z_SRED, svecha(560, 700, t, .0, 1.1))
    s += SL(Z_SRED, svecha(1260, 700, t, .4, 1.1))
    s += SL(Z_SRED, f'<ellipse cx="800" cy="720" rx="80" ry="30" fill="{KREM}" {o(4)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{760+i*20}" cy="710" r="10" fill="{ZEL2}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1050" cy="700" rx="40" ry="16" fill="url(#derev)" {o(3)}/>')
    seg = A.seg(t, .2, .8)
    box = _korobka(640, 580, 140, 110, t, TKAN2, SVET, True, .2, .1)
    offx = -40 * (1 - seg)
    s += SL(Z_SRED, f'<g transform="translate({offx:.0f},0)">{box}</g>')
    moneta_fall = A.out(A.seg(t, 1.0, .6))
    mx, my = 1100, 560 - 30 + 30 * moneta_fall
    s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="22" ry="15" fill="url(#med)" {o(3)}/>')
    zapr_on = 1 - A.ease(A.seg(t, 1.0, .5))
    if zapr_on > .05:
        s += SL(Z_SRED, _zapret(760, 440, 60, t))
    else:
        s += SL(Z_SRED, _galochka(760, 440, 1.2, t))
    r1, (r1x, r1y) = rukav(760, 620, 160, -150 + 10 * A.w(t, 1.6), t, "#5a3a26", "#ffd98a", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="26" ry="18" fill="#5a3a26" {o(4)}/>')
    r2, (r2x, r2y) = rukav(1160, 620, 160, -30 + 10 * A.w(t, 1.6, .2), t, "#2a3450", "#cfe4f5", .3)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="26" ry="18" fill="#2a3450" {o(4)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 1000, 180, t, 24, 7))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .42))
    s += SL(Z_LETIT, mokryy_sneg(t, 12, 5, .35, .6))
    s += vinetka(.42)
    return s


def chasy_i_dvoe_na_perrone(t):
    """Вокзальные часы на столбе, их циферблат — проём под настоящий кадр;
    на перроне он и она, между ними растёт трещина."""
    rnd = random.Random(409)
    s = sumerki_fon(t)
    s += SL(Z_DAL, ulica_dal(0, 760, W, t, True, 3))
    s += SL(Z_DAL, f'<rect x="0" y="760" width="{W}" height="100" fill="#4a4e58" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="60" y="860" width="{W-120}" height="200" fill="#5a5e68" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{80+i*380}" y1="880" x2="{80+i*380}" y2="1050" stroke="#3a3e48" stroke-width="3" opacity=".5"/>')
    vid = f'<circle cx="960" cy="400" r="190" fill="{KREM}"/>'
    pw, ph_ = 400, 400
    px, py = 760, 200
    vid2 = ""
    for i in range(6):
        a = math.radians(i * 30)
        vid2 += (f'<line x1="{960+math.sin(a)*160:.0f}" y1="{400-math.cos(a)*160:.0f}"'
                 f' x2="{960+math.sin(a)*180:.0f}" y2="{400-math.cos(a)*180:.0f}" stroke="#333" stroke-width="4"/>')
    a_sec = (t * 70) % 360
    vid2 += (f'<line x1="960" y1="400" x2="{960+math.sin(math.radians(a_sec))*150:.0f}"'
             f' y2="{400-math.cos(math.radians(a_sec))*150:.0f}" stroke="{KRAS}" stroke-width="3"/>')
    stolb = f'<rect x="920" y="400" width="80" height="420" rx="10" fill="{ZHELEZ}" {o(5)}/>'
    put = kontur_proema(px, py, pw, ph_, "ellips")
    sten = f'<path d="{put}" fill="#1a140e"/>' + vid + vid2 + mesto_stoka(px, py, pw, ph_, "ellips")
    sten += f'<path d="{put}" fill="none" {o(10)}/>'
    s += SL(Z_SRED, stolb + sten)
    s += SL(Z_SRED, f'<rect x="300" y="900" width="220" height="30" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="320" y="840" width="24" height="60" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="480" y="840" width="24" height="60" fill="url(#derev)" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M160,900 h140 v30 l-10,40 h-120 l-10,-40 Z" fill="{ZHELEZ}" {o(4)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<ellipse cx="{200+i*40}" cy="900" rx="28" ry="24" fill="#8a7a5a" opacity=".8" {o(2)}/>')
    # станционный киоск слева от столба — крытая будка
    kx_ = 500
    s += SL(Z_SRED, f'<rect x="{kx_:.0f}" y="350" width="260" height="620" rx="8" fill="#5a3a2a" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{kx_-20:.0f},480 h300 l-20,-40 h-260 Z" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kx_+30:.0f}" y="540" width="200" height="140" rx="4" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1500" y="700" width="50" height="320" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, ogon(1525, 660, t, .5, .3, 5))
    s += SL(Z_SRED, teplo(1525, 700, 260, 210, .32))
    s += SL(Z_SRED, dym(300, 1040, t, 4, .3, 200, .3, "#cfd6de"))
    s += SL(Z_SRED, f'<rect x="1620" y="980" width="90" height="20" rx="6" fill="{ZHELEZ}" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="600" width="140" height="90" rx="6" fill="{ZHELEZ}" opacity=".6" {o(3)}/>')
    trech = 160 * A.ease(A.seg(t, .3, 2.0))
    s += SL(Z_SRED, f'<path d="M960,1040 l{trech*.3:.0f},-10 l{-trech*.4:.0f},-14 l{trech*.5:.0f},-10'
                    f' l{-trech*.2:.0f},-10" fill="none" stroke="#1a1c22" stroke-width="4" opacity="{min(1,trech/150):.2f}"/>')
    s += SL(Z_SRED, figura(840, 1030, 540, t, "#2a2e3c", "#cfe4f5", False, .0))
    s += SL(Z_SRED, f'<rect x="770" y="920" width="60" height="100" rx="10" fill="#4a3c2e" {o(4)}/>')
    s += SL(Z_SRED, figura(1080, 1020, 500, t, "#3a2c3c", "#ffd98a", True, .2))
    s += SL(Z_SRED, para_izo_rta(850, 780, t, .1, .9, .4))
    s += SL(Z_SRED, para_izo_rta(1090, 790, t, .4, .8, .35))
    s += SL(Z_SRED, _napolnenie(420, 850, 1000, 100, t, 22, 5))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c10", .5))
    s += SL(Z_LETIT, sneg_letit(t, 30, 15, .5, .9))
    s += vinetka(.44)
    return s


def nozh_rezhet_lentu_druzhby(t):
    """Нож в коробке сам приподнимается и перерезает ленту, которую держат
    две подруги за столом."""
    rnd = random.Random(410)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 6)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_DAL, okno_izby(140, 140, 280, 240, t, svet=True, moroz=.4))
    s += SL(Z_SRED, teplo(280, 260, 260, 220, .36))
    s += utvar_izby(1200, 420, 300, t, 13)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="320" width="280" height="440" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _dvertsy_shkafa(420, 320, 280, 440, 210))
    s += SL(Z_SRED, hodiki(1420, 360, t, 1.0))
    s += SL(Z_SRED, f'<rect x="760" y="260" width="340" height="300" rx="8" fill="{KAMEN2}" {o(5)}/>')
    s += SL(Z_SRED, _kartiny_ryad(800, 300, 2, 14, 110, 150))
    s += SL(Z_SRED, _kovrik_pol(500, 900, 700, 110, TKAN2, KREM, 23))
    s += SL(Z_SRED, stol(560, 760, 820, 34))
    podn = A.out(A.seg(t % 3.0, .2, .4)) * (1 if (t % 3.0) < 1.4 else 1 - A.ease(A.seg(t % 3.0, 1.4, .4)))
    s += SL(Z_SRED, f'<rect x="700" y="{700-podn*40:.0f}" width="220" height="60" rx="8" fill="#5a3a26" {o(5)}/>')
    nx, ny = 810, 700 - podn * 70
    s += SL(Z_SRED, f'<g transform="rotate({podn*20:.0f} {nx:.0f} {ny:.0f})">'
                    f'<path d="M{nx-70:.0f},{ny:.0f} l140,-10 l-20,20 l-120,6 Z" fill="{ZHELEZ}" {o(4)}/>'
                    f'<rect x="{nx+60:.0f}" y="{ny-10:.0f}" width="50" height="20" rx="6" fill="#5a3a26" {o(3)}/></g>')
    rezka = A.ease(A.seg(t, 1.6, .4))
    lenta_y = 640
    if rezka < .98:
        s += SL(Z_SRED, f'<path d="M560,{lenta_y} h{360*(1-rezka):.0f}" stroke="{KRAS}" stroke-width="14"/>')
        s += SL(Z_SRED, f'<path d="M{560+360*(1-rezka)+440*rezka:.0f},{lenta_y} h{360*(1-rezka):.0f}" stroke="{KRAS}" stroke-width="14"/>')
    else:
        lx1 = 560 - 60 * (rezka - .98) * 20
        lx2 = 1300 + 60 * (rezka - .98) * 20
        s += SL(Z_SRED, f'<path d="M{lx1:.0f},{lenta_y} h300" stroke="{KRAS}" stroke-width="14"/>')
        s += SL(Z_SRED, f'<path d="M{lx2-300:.0f},{lenta_y} h300" stroke="{KRAS}" stroke-width="14"/>')
    for bx in (560, 1340):
        s += SL(Z_SRED, f'<circle cx="{bx:.0f}" cy="{lenta_y:.0f}" r="26" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="640" cy="720" rx="60" ry="26" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1240" cy="720" rx="100" ry="30" fill="#caa86a" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="860" y="700" width="60" height="50" rx="8" fill="{KAMEN}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1000" cy="720" rx="36" ry="14" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, figura(600, 940, 480, t, "#6b2a38", "#ffd98a", False, .0))
    s += SL(Z_SRED, figura(1300, 940, 480, t, "#2a4a3a", "#ffd98a", False, .2))
    s += SL(Z_SRED, svecha(1000, 680, t, .3, 1.0))
    s += SL(Z_SRED, _napolnenie(900, 550, 400, 160, t, 23, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 14, 9, .4, .7))
    s += vinetka(.42)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 11-18 ══════════════════════════════
def pustoy_koshelek_i_pustoy_god(t):
    """Пустой кошелёк на комоде, из него вылетает моль; за ним ряд из
    двенадцати листков календаря с пустыми тарелками."""
    rnd = random.Random(411)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 10)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += kvartira_veschi(1480, 680, 380, t, 14)
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="230" width="300" height="610" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _dvertsy_shkafa(420, 230, 300, 610, 250))
    s += SL(Z_SRED, _kovrik_pol(480, 840, 760, 160, TKAN2, KREM, 25))
    s += SL(Z_SRED, f'<rect x="160" y="560" width="1200" height="40" rx="10" fill="url(#derev)" {o(6)}/>')
    for i in range(12):
        lx = 200 + i * 88
        rot = 3 * A.w(t, 1.4, i * .15)
        s += SL(Z_SRED, f'<g transform="rotate({rot:.1f} {lx+30:.0f} {520:.0f})">'
                        f'<rect x="{lx:.0f}" y="420" width="60" height="100" rx="4" fill="{KREM}" {o(3)}/>'
                        f'<ellipse cx="{lx+30:.0f}" cy="470" rx="18" ry="14" fill="none" stroke="#9aa0a4" stroke-width="2"/></g>')
    moly = 20 * A.w(t, 2.4)
    s += SL(Z_SRED, _koshelek(640, 760, 3.2, True, 0, True, t))
    s += SL(Z_SRED, f'<ellipse cx="{700+moly:.0f}" cy="{660-abs(moly):.0f}" rx="12" ry="7" fill="#9a8a78" opacity=".7"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="600" width="260" height="220" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1360" cy="660" rx="40" ry="40" fill="#cfd6de" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1430" y="640" width="14" height="60" rx="5" fill="{K}" {o(2)}/>')
    kach = 4 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 1500 700)"><circle cx="1490" cy="700" r="10" fill="{ZHELEZ}"/>'
                    f'<circle cx="1510" cy="700" r="10" fill="{ZHELEZ}"/>'
                    f'<line x1="1480" y1="700" x2="1480" y2="650" stroke="{ZHELEZ}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="800" rx="30" ry="18" fill="#cfd6de" opacity=".85" {o(2)}/>')
    s += SL(Z_SRED, svecha(1000, 740, t, .2, 1.0))
    s += SL(Z_SRED, f'<rect x="760" y="800" width="160" height="22" rx="6" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="900" y="230" width="320" height="370" rx="8" fill="{KAMEN2}" {o(5)}/>')
    s += SL(Z_SRED, _kartiny_ryad(940, 310, 2, 26, 110, 150))
    s += SL(Z_SRED, _napolnenie(900, 600, 500, 150, t, 25, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .42))
    s += SL(Z_LETIT, mokryy_sneg(t, 10, 6, .3, .6))
    s += vinetka(.42)
    return s


def derevo_s_tremya_kornyami(t):
    """Яблоня в разрезе земли: над землёй свёртки на ветках, под землёй три
    корня с загорающимися номерами. Холодный дневной свет, смена главы."""
    rnd = random.Random(412)
    s = f'<rect width="{W}" height="{H}" fill="{DEN}"/>'
    s += nebo("den", t, False, 1)
    s += SL(Z_DAL, oblaka(t, 140, 4, 13, .4, "#e8eef6", 9.0))
    zemlya_y = 700
    s += SL(Z_DAL, f'<rect x="0" y="{zemlya_y}" width="{W}" height="{H-zemlya_y}" fill="#4a3a2c" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="{zemlya_y-14}" width="{W}" height="20" fill="url(#sneg)" {o(4)}/>')
    sway = 2 * A.w(t, 2.8)
    stvol = (f'<g transform="rotate({sway:.1f} 960 {zemlya_y})">'
             f'<path d="M900,{zemlya_y} L930,{zemlya_y-440} L1010,{zemlya_y-440} L1040,{zemlya_y} Z"'
             f' fill="url(#derev)" {o(7)}/>')
    for i, (dx, dy, dl) in enumerate(((-260, -360, 220), (240, -380, 240), (-140, -460, 200), (180, -480, 210))):
        stvol += (f'<path d="M970,{zemlya_y-400+i*20} q{dx*.5:.0f},{dy*.25:.0f} {dx:.0f},{dy:.0f}"'
                  f' fill="none" stroke="{DOSKA2}" stroke-width="14" stroke-linecap="round"/>')
    stvol += '</g>'
    s += SL(Z_SRED, stvol)
    rnd2 = random.Random(5)
    for i, (dx, dy) in enumerate(((-250, -380), (220, -400), (-120, -480), (160, -500), (0, -560))):
        qx, qy = 970 + dx, zemlya_y + dy
        bob = 6 * A.w(t, 1.6, i * .2)
        s += SL(Z_SRED, _svertok(qx, qy + bob, 1.4, t, (RUSH, KREM, TKAN2)[i % 3], (TKAN, ZOL)[i % 2], i * .2))
    s += SL(Z_SRED, f'<path d="M300,{zemlya_y} h1320" stroke="url(#derev)" stroke-width="10"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="{320+i*140}" y="{zemlya_y-70}" width="18" height="70" fill="url(#derev)" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1500,{zemlya_y-220} q20,-40 60,-40 q0,40 -40,60 Z" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="1520" cy="{zemlya_y-260}" r="16" fill="#2a2420" {o(2)}/>')
    s += SL(Z_DAL, izba_snaruzhi(420, zemlya_y + 20, 480, t, True, True, 9))
    s += SL(Z_DAL, dym(260, zemlya_y - 480, t, 4, .22, 260, .4, "#dde4ec"))
    sugrob = f'<path d="M1600,{zemlya_y} q80,-60 220,-10 l0,30 h-220 Z" fill="url(#sneg)" {o(5)}/>'
    s += SL(Z_SRED, sugrob)
    fly = (t * 90) % 1920
    s += SL(Z_SRED, f'<g transform="translate({fly-200:.0f},{280+30*A.w(t,2.2):.0f})">'
                    f'<ellipse cx="0" cy="0" rx="30" ry="16" fill="#1a1c22" {o(3)}/>'
                    f'<ellipse cx="34" cy="-4" rx="16" ry="20" fill="#fff" {o(2)}/></g>')
    korni = []
    for dx, dy, lb in ((-220, 220, 1), (0, 280, 2), (220, 220, 3)):
        korni.append((960 + dx, zemlya_y + dy))
    korn_svg = f'<g transform="rotate({sway*.3:.1f} 960 {zemlya_y})">'
    for i, (kx, ky) in enumerate(korni):
        korn_svg += (f'<path d="M960,{zemlya_y} Q{(960+kx)/2:.0f},{zemlya_y+40}'
                     f' {kx:.0f},{ky:.0f}" fill="none" stroke="url(#derev)" stroke-width="{36-i*4}"/>')
        on = ((t * 1.2 + i * .4) % 3.0) < 1.5
        s_op = .9 if on else .25
        korn_svg += f'<circle cx="{kx:.0f}" cy="{ky+20:.0f}" r="22" fill="{ZOL}" opacity="{s_op:.2f}" {o(3)}/>'
    korn_svg += '</g>'
    s += SL(Z_SRED, korn_svg)
    s += SL(Z_SRED, f'<rect x="700" y="{zemlya_y-120}" width="26" height="120" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="686" y="{zemlya_y-150}" width="54" height="36" rx="8" fill="#6b4428" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="710" cy="{zemlya_y-132}" r="10" fill="#2a2420"/>')
    # колодец у забора — сруб, два столба и двускатная крыша, своя высота
    kolx = 1320
    s += SL(Z_SRED, f'<rect x="{kolx-60:.0f}" y="{zemlya_y-70:.0f}" width="120" height="70" rx="6" fill="url(#brev)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kolx-70:.0f}" y="{zemlya_y-320:.0f}" width="16" height="250" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{kolx+54:.0f}" y="{zemlya_y-320:.0f}" width="16" height="250" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{kolx-90:.0f},{zemlya_y-310:.0f} h180 l-20,-50 h-140 Z" fill="{DOSKA2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{kolx-6:.0f}" y="{zemlya_y-280:.0f}" width="12" height="200" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, pleten(1180, zemlya_y + 60, 340, 170, 5))
    s += SL(Z_SRED, _napolnenie(420, 330, 460, 180, t, 26, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#1a1c22", .3))
    s += vinetka(.3)
    return s


def platki_u_vorot(t):
    """У ворот стол с платками и полотенцами: платок переходит из рук
    хозяйки к старику и соседке; лица опущены, сцена тихая."""
    rnd = random.Random(413)
    s = f'<rect width="{W}" height="{H}" fill="{SERO}"/>'
    s += nebo("den", t, False, 4)
    s += SL(Z_DAL, pleten(60, 760, 1200, 170, 7))
    s += SL(Z_DAL, f'<rect x="760" y="300" width="340" height="480" fill="#8a7a6a" opacity=".6" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="1300" y="640" width="60" height="320" fill="url(#kamen)" {o(5)}/>')
    s += SL(Z_DAL, f'<path d="M1260,640 h140 l-20,-50 h-100 Z" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="850" y="600" width="220" height="160" rx="30" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, goloe_derevo(1440, 940, 300, t, 10, 6, "#3a3a44"))
    # поленница у плетня — настоящие дрова со срезами
    for row in range(3):
        for col in range(5):
            s += SL(Z_SRED, f'<circle cx="{430+col*42:.0f}" cy="{880-row*40:.0f}" r="20" fill="url(#derev)" {o(3)}/>')
            s += SL(Z_SRED, f'<circle cx="{430+col*42:.0f}" cy="{880-row*40:.0f}" r="12" fill="{KREM}" opacity=".5"/>')
    s += SL(Z_SRED, sneg_lezhit(900))
    s += SL(Z_SRED, stol(560, 820, 760, 36))
    s += SL(Z_SRED, f'<rect x="540" y="800" width="800" height="30" rx="6" fill="#fff" opacity=".9" {o(4)}/>')
    stopka = 5
    seg = A.seg(t, 1.0, 7.0)
    stopka_now = max(2, round(stopka - seg * 3))
    for i in range(stopka_now):
        s += SL(Z_SRED, f'<rect x="{620+i*4:.0f}" y="{790-i*16:.0f}" width="180" height="20" rx="4" fill="{KREM}" {o(3)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="{900+i*4:.0f}" y="{784-i*16:.0f}" width="150" height="18" rx="4" fill="{RUSH}" {o(3)}/>')
    peredacha = A.ease(A.seg(t % 3.0, .2, 1.0))
    px_ = 980 + 220 * peredacha
    s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="760" width="100" height="16" rx="4" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, figura(700, 1000, 480, t, "#3a3a44", "#9aa0a4", True, .0, naklon=6))
    r1, (r1x, r1y) = rukav(800, 700, 150, -20, t, "#3a3a44", "#9aa0a4", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="24" ry="17" fill="#3a3a44" {o(4)}/>')
    s += SL(Z_SRED, figura(1220, 1010, 500, t, "#3a3028", "#8a8a8a", False, .2, boroda=True, naklon=8))
    r2a, (r2ax, r2ay) = rukav(1130, 740, 130, -150, t, "#3a3028", "#8a8a8a", .3)
    r2b, (r2bx, r2by) = rukav(1310, 740, 130, -30, t, "#3a3028", "#8a8a8a", .5)
    s += SL(Z_SRED, r2a + r2b)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="24" ry="17" fill="#3a3028" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2bx:.0f}" cy="{r2by:.0f}" rx="24" ry="17" fill="#3a3028" {o(4)}/>')
    s += SL(Z_SRED, figura(1420, 1010, 480, t, "#44403a", "#9aa0a4", True, .4, naklon=6))
    s += SL(Z_SRED, f'<rect x="1370" y="900" width="100" height="70" rx="8" fill="{RUSH}" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 27, 4))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 27, 4))
    s += SL(Z_SRED, lampa(240, 540, t, .8, False))
    s += SL(Z_PERED, goloe_derevo(1800, 1040, 240, t, 9, 5, "#3a3a44"))
    s += SL(Z_LETIT, sneg_letit(t, 10, 7, .3, .5))
    s += vinetka(.3)
    return s


def platok_polotence_i_tapochki(t):
    """Раскрытый шкаф, на средней полке платок, полотенце и тапочки; над
    ними капли-слёзы. Средняя полка — проём под настоящий кадр."""
    rnd = random.Random(414)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 2)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(800))
    shx, shy, shw, shh = 560, 160, 900, 800
    kach = 2 * A.w(t, 1.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {shx:.0f} {shy:.0f})">'
                    f'<rect x="{shx:.0f}" y="{shy:.0f}" width="{shw}" height="{shh}" rx="10" fill="url(#derev)" {o(7)}/></g>')
    s += SL(Z_SRED, f'<rect x="{shx+20:.0f}" y="{shy+20:.0f}" width="{shw-40}" height="{shh*.32:.0f}" rx="6" fill="{KREM}" {o(4)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{shx+40+i*60:.0f}" y="{shy+40:.0f}" width="50" height="{shh*.26:.0f}" rx="4" fill="{(RUSH,TKAN,KREM,TKAN2)[i]}" {o(3)}/>')
    pw, ph_ = 760, 300
    px, py = shx + 60, shy + shh * .42
    vid = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw}" height="{ph_}" fill="{RUSH}"/>'
           f'<rect x="{px+40:.0f}" y="{py+40:.0f}" width="{pw-80}" height="80" fill="{KRAS}" opacity=".7"/>'
           f'<rect x="{px+40:.0f}" y="{py+150:.0f}" width="{pw-80}" height="80" fill="{KRAS}" opacity=".5"/>')
    put = kontur_proema(px, py, pw, ph_, "pryam")
    polka_s = f'<path d="{put}" fill="#1a140e"/>' + vid + mesto_stoka(px, py, pw, ph_, "pryam")
    polka_s += f'<path d="{put}" fill="none" {o(8)}/>'
    s += SL(Z_SRED, polka_s)
    s += SL(Z_SRED, f'<rect x="{shx+20:.0f}" y="{shy+shh*.74:.0f}" width="{shw-40}" height="{shh*.22:.0f}" rx="6" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{shx+40:.0f}" y="{shy+shh*.76:.0f}" width="140" height="50" rx="6" fill="#efe3c8" {o(3)}/>')
    tapn = A.out(A.seg(t, .3, .8))
    s += SL(Z_SRED, f'<ellipse cx="{shx+260:.0f}" cy="{shy+shh*.86-tapn*20:.0f}" rx="40" ry="18" fill="{TKAN}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{shx+330:.0f}" cy="{shy+shh*.86-tapn*20:.0f}" rx="40" ry="18" fill="{TKAN}" {o(3)}/>')
    for i, dx in enumerate((-30, 20, 60)):
        drop = ((t * .6 + i * .3) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{shx+120+dx:.0f}" cy="{shy+shh*.36+drop*40:.0f}" rx="6" ry="10" fill="#aee0ff" opacity="{1-drop:.2f}"/>')
    s += SL(Z_SRED, f'<rect x="{shx+20:.0f}" y="{shy+10:.0f}" width="140" height="70" rx="8" fill="{TKAN2}" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="{shx+90:.0f}" cy="{shy+44:.0f}" r="16" fill="{KREM}" opacity=".8"/>')
    s += SL(Z_SRED, lampa(260, 300, t, .8, True))
    s += SL(Z_SRED, _napolnenie(1460, 700, 380, 140, t, 28, 8))
    s += SL(Z_SRED, mebel_hlam(1440, 980, 300, t, 28))
    s += SL(Z_PERED, ramka_pp("levo", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 8, 5, .3, .5))
    s += vinetka(.4)
    return s


def polotence_na_vorotah_i_na_svadbe(t):
    """Кадр надвое: слева тесовые ворота с полотенцем в сумерках, справа
    светлая горница — жених и невеста держат каравай на том же узоре."""
    rnd = random.Random(415)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="960" height="{H}" fill="url(#nsumer)"/>')
    s += SL(Z_DAL, f'<rect x="960" y="0" width="960" height="{H}" fill="{KREM}"/>')
    s += SL(Z_DAL, pleten(0, 820, 900, 170, 7))
    vorx, vory = 300, 500
    s += SL(Z_SRED, dver(vorx, vory, 280, 480, .0, kruchok=False))
    kol = 3 * A.w(t, 1.8, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kol:.1f} {vorx+140:.0f} {vory+60:.0f})">'
                    f'<rect x="{vorx+100:.0f}" y="{vory+60:.0f}" width="80" height="220" rx="8" fill="{RUSH}" {o(4)}/>'
                    f'<rect x="{vorx+116:.0f}" y="{vory+90:.0f}" width="48" height="10" fill="{KRAS}"/></g>')
    s += SL(Z_SRED, f'<path d="M{vorx-60},{vory+420} q10,-130 -30,-160" fill="none" stroke="#5a4a3a" stroke-width="12" opacity=".7"/>')
    s += SL(Z_SRED, lavka(100, 920, 260))
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{620+i*20}" y="{700+i*10}" width="14" height="80" fill="#2a2e38" {o(2)}/>')
    s += SL(Z_SRED, okno_izby(1300, 300, 240, 220, t, svet=True, moroz=0, krest=True))
    s += SL(Z_SRED, teplo(1420, 420, 260, 220, .36))
    s += SL(Z_SRED, svecha(1500, 700, t, .2, .9))
    s += SL(Z_SRED, stol(1160, 760, 540, 34))
    s += SL(Z_SRED, f'<ellipse cx="1430" cy="780" rx="60" ry="30" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1410" y="740" width="40" height="60" fill="{ZHELEZ}" {o(3)}/>')
    karav_y = 740
    tow = f'<rect x="1150" y="{karav_y+10}" width="260" height="30" rx="6" fill="{RUSH}" {o(3)}/>'
    s += SL(Z_SRED, tow)
    s += SL(Z_SRED, karavay(1280, karav_y, 1.1, False))
    fata = 4 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, figura(1180, 980, 460, t, "#2a3a4a", "#efe3c8", False, .0))
    s += SL(Z_SRED, figura(1380, 980, 480, t, "#efe3c8", "#cfe4f5", True, .2))
    s += SL(Z_SRED, f'<g transform="rotate({fata:.1f} 1380 760)"><path d="M1340,740 q40,-60 80,0 l-10,120 h-60 Z"'
                    f' fill="#fff" opacity=".7" {o(3)}/></g>')
    kolyb = 6 * A.w(t, 1.4, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kolyb:.1f} 1700 920)">'
                    f'<path d="M1650,920 q50,-60 100,0 l0,60 h-100 Z" fill="url(#derev)" {o(4)}/>'
                    f'<ellipse cx="1700" cy="930" rx="30" ry="14" fill="#efe3c8" {o(3)}/></g>')
    s += SL(Z_SRED, siluet(700, 980, 300, "#2a2420", .5))
    s += SL(Z_SRED, siluet(780, 990, 280, "#2a2420", .5))
    s += SL(Z_SRED, f'<rect x="920" y="260" width="200" height="640" fill="{KAMEN2}" opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M920,260 h200 l-30,-60 h-140 Z" fill="{DOSKA2}" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="700" width="260" height="220" rx="8" fill="#5a3a2a" opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 1080, 100, t, 29, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e10", .34))
    s += SL(Z_LETIT, mokryy_sneg(t, 8, 9, .3, .5))
    s += vinetka(.36)
    return s


def polotence_na_vesah(t):
    """На столе чашечные весы, на обеих чашах одинаковое вышитое полотенце;
    тучка под левой, солнышко под правой; весы ровно."""
    rnd = random.Random(416)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 11)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_DAL, okno_izby(1480, 160, 260, 220, t, svet=True, moroz=.3))
    s += SL(Z_SRED, teplo(1600, 280, 260, 220, .34))
    s += utvar_izby(80, 420, 360, t, 17)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="520" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="220" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, stol(660, 780, 680, 34))
    s += SL(Z_SRED, _vesy(960, 780, 1.9, t, 0, 3))
    for sgn in (-1, 1):
        cx_ = 960 + sgn * 195
        s += SL(Z_SRED, f'<rect x="{cx_-50:.0f}" y="595" width="100" height="18" rx="5" fill="{RUSH}" {o(3)}/>')
    mig = .5 + .4 * abs(A.w(t, 1.2))
    s += SL(Z_SRED, f'<ellipse cx="820" cy="540" rx="34" ry="18" fill="#9aa8b8" opacity="{mig:.2f}"/>')
    s += SL(Z_SRED, f'<circle cx="1100" cy="540" r="26" fill="{ZOL}" opacity="{1-mig*.5:.2f}"/>')
    s += SL(Z_SRED, svecha(760, 700, t, .1, 1.0))
    s += SL(Z_SRED, karavay(1200, 720, .8, True))
    s += SL(Z_SRED, f'<path d="M700,700 l20,-10 l20,30 l-30,10 Z" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1300,700 q-40,20 -20,60 q50,-10 50,-40 Z" fill="#efe3c8" opacity=".8" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="900" y="700" width="40" height="46" rx="6" fill="{CHUGUN}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="280" height="500" rx="10" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1170, 310, 1, 30, 130, 170))
    s += SL(Z_SRED, _napolnenie(420, 620, 1000, 140, t, 30, 8))
    s += SL(Z_SRED, mebel_hlam(760, 950, 260, t, 30))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 8, 4, .3, .5))
    s += vinetka(.4)
    return s


def ostroe_zhelezo_i_nechistaya_sila(t):
    """Стена сарая с острым инструментом на гвоздях; чертенята тянутся к
    остриям; дед снимает нож и заворачивает его в тряпицу."""
    rnd = random.Random(417)
    s = f'<rect width="{W}" height="{H}" fill="#2a2420"/>'
    s += nebo("sumer", t, False, 12)
    s += SL(Z_DAL, doski(0, 0, W, 800, 90, True, "dosk"))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="700" y="160" width="700" height="40" rx="8" fill="url(#derev)" {o(5)}/>')
    kosa_s = (f'<line x1="760" y1="200" x2="760" y2="420" stroke="url(#derev)" stroke-width="12"/>'
              f'<path d="M760,420 q100,20 140,-60 q-80,0 -140,60 Z" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, kosa_s)
    s += SL(Z_SRED, f'<line x1="900" y1="200" x2="900" y2="360" stroke="url(#zhel)" stroke-width="8"/>')
    s += SL(Z_SRED, f'<path d="M870,360 q30,40 60,0 q-30,-16 -60,0 Z" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M930,360 q30,40 60,0 q-30,-16 -60,0 Z" fill="{ZHELEZ}" {o(3)}/>')
    nozh_on = 1 - A.ease(A.seg(t, .6, .8))
    if nozh_on > .05:
        s += SL(Z_SRED, f'<line x1="1040" y1="200" x2="1040" y2="340" stroke="{ZHELEZ}" stroke-width="6" opacity="{nozh_on:.2f}"/>')
        s += SL(Z_SRED, f'<path d="M1010,340 h60 l-10,40 h-40 Z" fill="{ZHELEZ}" opacity="{nozh_on:.2f}" {o(3)}/>')
    s += SL(Z_SRED, f'<line x1="1140" y1="200" x2="1140" y2="320" stroke="url(#zhel)" stroke-width="6"/>')
    vily = f'<line x1="1240" y1="200" x2="1240" y2="440" stroke="url(#derev)" stroke-width="10"/>'
    for sgn in (-1, 0, 1):
        vily += f'<line x1="1240" y1="200" x2="{1240+sgn*20}" y2="140" stroke="{ZHELEZ}" stroke-width="7"/>'
    s += SL(Z_SRED, vily)
    for i in range(3):
        ph = i * .4
        s += SL(Z_SRED, _chertenok(560 - i * 60, 420 + i * 60, .9, t, ph))
    s += SL(Z_SRED, f'<rect x="60" y="640" width="420" height="140" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="620" cy="760" rx="60" ry="80" fill="#5a4a3a" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1500" y="700" width="140" height="180" rx="12" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M1500,780 h140" stroke="{ZHELEZ}" stroke-width="10"/>')
    s += SL(Z_SRED, lampa(1760, 480, t, .9, False))
    s += SL(Z_SRED, kot(300, 900, t, .9, "#2a2420"))
    s += SL(Z_SRED, figura(950, 1000, 520, t, "#3a2c3c", "#ffd98a", True, .0, tulup=True, boroda=True))
    zavyaz = A.ease(A.seg(t, .8, .6))
    r, (rx, ry) = rukav(1030, 760, 160, -70 + 40 * zavyaz, t, "#3a2c3c", "#ffd98a", .1)
    s += SL(Z_SRED, r)
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="24" ry="17" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 31, 3))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 31, 3))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += SL(Z_LETIT, dym(300, 900, t, 3, .2, 180, .3, "#cfd6de"))
    s += vinetka(.44)
    return s


def pustaya_krinka(t):
    """Пустая кринка лежит на боку на полке, паук в горлышке; полные соседи
    отодвигаются от неё."""
    rnd = random.Random(418)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 13)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="260" width="280" height="440" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN2, KREM, 32))
    s += SL(Z_SRED, f'<rect x="300" y="620" width="1320" height="40" rx="8" fill="url(#derev)" {o(6)}/>')
    otpolz = 10 * A.ease(A.seg(t, .6, 1.2))
    s += SL(Z_SRED, f'<g transform="translate({otpolz:.0f},0)"><path d="M700,620 q-10,-70 50,-76 q50,4 50,76 h-100 Z"'
                    f' fill="url(#glina)" {o(5)}/></g>')
    s += SL(Z_SRED, f'<g transform="translate({-otpolz:.0f},0)">')
    s += SL(Z_SRED, f'<ellipse cx="500" cy="590" rx="40" ry="34" fill="url(#med)" {o(4)}/>')
    s += SL(Z_SRED, karavay(420, 610, .7, True))
    s += SL(Z_SRED, f'</g>')
    s += SL(Z_SRED, f'<g transform="translate({otpolz:.0f},0)">')
    s += SL(Z_SRED, _banka(1000, 600, 1.1))
    s += SL(Z_SRED, f'<path d="M1100,600 l-10,-60 l50,10 l20,50 Z" fill="{ZOL}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1200" y="560" width="70" height="60" rx="8" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, '</g>')
    pauk_y = 4 * A.w(t, 2.2)
    s += SL(Z_SRED, f'<circle cx="{750+otpolz:.0f}" cy="{560+pauk_y:.0f}" r="10" fill="#1a1410"/>')
    for sgn in (-1, 1):
        s += SL(Z_SRED, f'<line x1="{750+otpolz:.0f}" y1="{560+pauk_y:.0f}" x2="{750+otpolz+sgn*16:.0f}" y2="{580+pauk_y:.0f}" stroke="#1a1410" stroke-width="2"/>')
    s += SL(Z_SRED, lampa(1700, 380, t, .85, True))
    s += SL(Z_SRED, utvar_izby(60, 420, 420, t, 21))
    s += utvar_pekarni(620, 900, 760, t, 9)
    s += SL(Z_SRED, f'<rect x="1140" y="260" width="260" height="420" rx="10" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(900, 600, 500, 150, t, 32, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 8, 5, .3, .5))
    s += vinetka(.4)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 19-26 ══════════════════════════════
def chasy_na_zapyaste(t):
    """Рукав пиджака с манжетой на пол-кадра: второй рукав застёгивает
    наручные часы на запястье. Видны только рукав и плечо."""
    rnd = random.Random(419)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 15)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += kvartira_veschi(1260, 700, 420, t, 16)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="480" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="200" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, _kovrik_pol(460, 900, 700, 110, TKAN, KREM, 33))
    s += SL(Z_SRED, stol(360, 780, 820, 34))
    s += SL(Z_SRED, lampa(1660, 420, t, .95, True))
    zastyog = A.ease(A.seg(t % 4.0, .4, 1.4))
    mx, my = 860, 660
    s += SL(Z_SRED, f'<path d="M{mx-120:.0f},{my+40:.0f} l240,-10 l-20,-150 l-220,10 Z" fill="#2a2e3c" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{mx-100:.0f},{my+20:.0f} l200,-6 l-8,-40 l-190,6 Z" fill="#fff" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{mx+40:.0f}" cy="{my-10:.0f}" rx="34" ry="20" fill="url(#zol)" {o(3)}/>')
    strap = (f'<path d="M{mx+70:.0f},{my-20:.0f} q{40*zastyog:.0f},{-10*zastyog:.0f} {70*zastyog:.0f},{-4*zastyog:.0f}"'
             f' fill="none" stroke="#5a3a26" stroke-width="16" stroke-linecap="round"/>')
    s += SL(Z_SRED, strap)
    r2, (r2x, r2y) = rukav(mx + 160, my - 60, 150, -160 + 20 * A.w(t, 1.6), t, "#2a2e3c", "#cfe4f5", .2, nichya=True)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="24" ry="17" fill="#2a2e3c" {o(4)}/>')
    s += SL(Z_SRED, _chasy_karman(500, 700, 1.0, t, 1.0))
    s += SL(Z_SRED, f'<rect x="300" y="700" width="60" height="70" rx="8" fill="#1a1c22" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1000" y="730" width="140" height="18" rx="4" fill="{KREM}" {o(3)}/>')
    gaz = 3 * A.w(t, 1.7, .2)
    s += SL(Z_SRED, f'<g transform="rotate({gaz:.1f} 1120 720)"><rect x="1050" y="690" width="140" height="90" fill="#e8e2d0" {o(3)}/></g>')
    s += SL(Z_SRED, f'<ellipse cx="1280" cy="760" rx="32" ry="20" fill="#cfe4f5" opacity=".6" {o(3)}/>')
    s += SL(Z_SRED, par(1280, 740, t, 3, .4, 120, .5))
    s += SL(Z_SRED, _napolnenie(900, 580, 450, 150, t, 33, 6))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1170, 310, 2, 34, 100, 130))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def hodiki_i_budilnik(t):
    """Стенные часы с кукушкой и гирями-шишками, под ними будильник на
    тумбочке; над обоими загорается галочка."""
    rnd = random.Random(420)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 16)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += kvartira_veschi(80, 720, 420, t, 18)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, _kovrik_pol(460, 900, 700, 110, TKAN, KREM, 20))
    cx, cy = 900, 420
    kuk_on = ((t * 1.4) % 3.0) < .8
    s += SL(Z_SRED, f'<rect x="{cx-100:.0f}" y="{cy-280:.0f}" width="200" height="500" rx="14" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="{cx-50:.0f}" y="{cy-80:.0f}" width="100" height="{40 if kuk_on else 6:.0f}" rx="6" fill="{KREM}" {o(3)}/>')
    if kuk_on:
        s += SL(Z_SRED, f'<ellipse cx="{cx:.0f}" cy="{cy-60:.0f}" rx="18" ry="14" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, _chasy_sten(cx, cy + 40, 1.1, t))
    for sgn, ph in ((-1, 0), (1, .5)):
        gy = cy + 180 + 30 * A.w(t, .6, ph) * .3
        s += SL(Z_SRED, f'<line x1="{cx+sgn*30:.0f}" y1="{cy+90:.0f}" x2="{cx+sgn*30:.0f}" y2="{gy:.0f}" stroke="#5a3a26" stroke-width="4"/>')
        s += SL(Z_SRED, f'<ellipse cx="{cx+sgn*30:.0f}" cy="{gy:.0f}" rx="18" ry="24" fill="#6b4428" {o(4)}/>')
    tumba_x, tumba_y = 820, 700
    s += SL(Z_SRED, f'<rect x="{tumba_x:.0f}" y="{tumba_y:.0f}" width="220" height="200" rx="10" fill="url(#derev)" {o(6)}/>')
    bud_bounce = 6 * A.ease(A.seg(t % 1.0, .0, .2))
    s += SL(Z_SRED, f'<g transform="translate(0,{-bud_bounce:.0f})">'
                    f'<circle cx="{tumba_x+110:.0f}" cy="{tumba_y-20:.0f}" r="60" fill="url(#zhel)" {o(5)}/>'
                    f'<circle cx="{tumba_x+40:.0f}" cy="{tumba_y-70:.0f}" r="20" fill="{ZHELEZ}" {o(3)}/>'
                    f'<circle cx="{tumba_x+180:.0f}" cy="{tumba_y-70:.0f}" r="20" fill="{ZHELEZ}" {o(3)}/></g>')
    s += SL(Z_SRED, _galochka(cx + 140, cy - 160, 1.1, t, .0))
    s += SL(Z_SRED, _galochka(tumba_x + 110, tumba_y - 140, 1.0, t, .4))
    s += SL(Z_SRED, lampa(1660, 420, t, .9, True))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="280" height="500" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1170, 310, 2, 34, 100, 130))
    s += SL(Z_SRED, f'<path d="M1500,900 q-20,-200 0,-260 q20,60 0,260 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1180" y="860" width="320" height="30" rx="8" fill="{RUSH}" {o(4)}/>')
    s += SL(Z_SRED, _napolnenie(1140, 600, 350, 150, t, 34, 6))
    s += mebel_hlam(500, 850, 300, t, 34)
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 6, .25, .5))
    s += vinetka(.4)
    return s


def sem_podarkov_na_servante(t):
    """Сервант с семью коробками: бабушка ставит седьмую, номера загораются
    по очереди; над сервантом по ходу времени встают карточки главы."""
    rnd = random.Random(421)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 17)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _servant(360, 300, 1300, 480, t))
    boxcols = ((TKAN, ZOL), (TKAN2, SVET), (ZEL2, KREM), (MED, ZOL), (KAMEN2, SVET), ("#5a3a4a", ZOL), ("#2e3a4a", SVET))
    postav = A.ease(A.seg(t, .2, 1.0))
    for i in range(7):
        bx = 420 + i * 150
        by = 700 - (30 if i == 6 else 0) * (1 - postav)
        col, lenta = boxcols[i]
        s += SL(Z_SRED, _korobka(bx, by, 120, 100, t, col, lenta, True, .0, i * .3))
        on = (t % 9.0) > i * 1.1
        if on:
            s += SL(Z_SRED, f'<circle cx="{bx+60:.0f}" cy="{by-20:.0f}" r="14" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="300" cy="420" rx="40" ry="90" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, hodiki(1500, 380, t, 1.0))
    s += SL(Z_SRED, svecha(1300, 700, t, .2, 1.0))
    s += SL(Z_SRED, f'<rect x="1300" y="520" width="140" height="22" rx="5" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1600,700 l-16,-120 l40,20 l16,100 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1680" cy="720" rx="60" ry="24" fill="url(#med)" {o(4)}/>')
    kart = (t % 9.0) > 4.0
    if kart:
        kpop = A.out(A.seg((t % 9.0) % 4.0, .0, .6))
        s += SL(Z_SRED, f'<g transform="translate(0,{(1-kpop)*40:.0f})">'
                        f'<rect x="760" y="140" width="240" height="140" rx="10" fill="#fff" opacity=".92" {o(4)}/></g>')
    s += SL(Z_SRED, figura(1140, 940, 540, t, "#3a2c3c", "#ffd98a", True, .0))
    r, (rx, ry) = rukav(1260, 650, 150, -60 + 10 * A.w(t, 1.8), t, "#3a2c3c", "#ffd98a", .1)
    s += SL(Z_SRED, r)
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="24" ry="17" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 35, 3))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 35, 3))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def chasy_v_krasnoy_korobke(t):
    """Красная лаковая коробка с настольными часами на шёлке; старик обеими
    руками отодвигает её; два облачка сходятся знаком равенства."""
    rnd = random.Random(422)
    s = f'<rect width="{W}" height="{H}" fill="#4a2e26"/>'
    s += nebo("sumer", t, False, 18)
    s += SL(Z_DAL, f'<rect x="0" y="40" width="{W}" height="760" fill="#5a3630" {o(5)}/>')
    s += SL(Z_SRED, lampa(960, 180, t, 1.1, True))
    s += SL(Z_SRED, teplo(960, 420, 260, 220, .4))
    s += SL(Z_SRED, f'<rect x="420" y="300" width="280" height="420" rx="10" fill="#6b4428" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="320" width="240" height="180" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 120, "#8a2a2a", ZOL, 22))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="500" y="680" width="900" height="40" rx="8" fill="url(#derev)" {o(6)}/>')
    otodv = -40 * A.ease(A.seg(t, .3, 1.0))
    box = f'<rect x="700" y="580" width="260" height="100" rx="10" fill="{KRAS}" {o(6)}/>'
    box += f'<ellipse cx="830" cy="610" rx="20" ry="30" fill="url(#zol)" {o(3)}/>'
    box += _chasy_sten(830, 610, .6, t)
    s += SL(Z_SRED, f'<g transform="translate({otodv:.0f},0)">{box}</g>')
    stage = A.seg(t, 1.2, 1.5)
    s += SL(Z_SRED, _oblachko(660, 420 - 60 * stage, .8, t, .1, "chasy"))
    s += SL(Z_SRED, _oblachko(1080, 420 - 60 * stage, .8, t, .3, "doroga"))
    if stage > .9:
        s += SL(Z_SRED, _oblachko(870, 400, .6, t, .0, "ravno"))
    s += SL(Z_SRED, f'<rect x="1300" y="620" width="160" height="90" rx="14" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1380" cy="600" rx="70" ry="16" fill="{KREM}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1380" cy="640" rx="36" ry="24" fill="url(#med)" {o(3)}/>')
    fen_sw = 5 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<g transform="rotate({fen_sw:.1f} 300 500)">'
                    f'<ellipse cx="300" cy="500" rx="60" ry="100" fill="{KRAS}" opacity=".85" {o(4)}/></g>')
    s += SL(Z_SRED, dym(430, 660, t, 3, .3, 160, .4, "#dde4ec"))
    s += SL(Z_SRED, f'<path d="M1550,700 l-10,-90 l30,10 l12,80 Z" fill="#8a2a2a" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M1500,560 q60,-30 110,0 q-20,30 -110,0 Z" fill="none" stroke="{ZOL}" stroke-width="3" opacity=".7"/>')
    s += SL(Z_SRED, figura(930, 980, 480, t, "#3a2420", "#d6a63f", False, .0, tulup=True, naklon=4))
    push1 = A.ease(A.seg(t, .3, 1.0))
    r1, (r1x, r1y) = rukav(830, 760, 140, -170 - 20 * push1, t, "#3a2420", "#d6a63f", .1)
    r2, (r2x, r2y) = rukav(1030, 760, 140, -10 + 20 * push1, t, "#3a2420", "#d6a63f", .3)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="22" ry="9" fill="#d6a63f" opacity=".5"/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="22" ry="9" fill="#d6a63f" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="300" width="260" height="380" rx="10" fill="#6b4428" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(420, 620, 1080, 140, t, 36, 7))
    s += SL(Z_PERED, ramka_pp("oba", "#120a0a", .44))
    s += vinetka(.42)
    return s


def muzh_zhena_i_korobochka_s_chasami(t):
    """Муж держит коробочку с часами на ладони, жена закрывает щёки и
    качает головой у круглого стола."""
    rnd = random.Random(423)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 19)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, _elka(1400, 940, 640, t, 11, True))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="500" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="210" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN2, KREM, 23))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="820" rx="340" ry="60" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="772" width="400" height="30" rx="8" fill="#fff" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, _korobka(900, 740, 120, 80, t, KREM, TKAN, True, .2, .1))
    for i in range(3):
        s += SL(Z_SRED, f'<circle cx="{480+i*110}" cy="820" r="26" fill="{KREM}" opacity=".7"/>')
    s += SL(Z_SRED, hodiki(1700, 420, t, .9))
    s += SL(Z_SRED, svecha(1500, 740, t, .2, .9))
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="700" rx="60" ry="26" fill="{KAMEN2}" {o(4)}/>')
    s += SL(Z_SRED, figura(760, 1000, 500, t, "#3a3028", "#efe3c8", False, .0))
    podn = A.out(A.seg(t % 3.0, .2, .6))
    r1, (r1x, r1y) = rukav(840, 780, 150, -40 + 10 * podn, t, "#3a3028", "#efe3c8", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="26" ry="18" fill="#3a3028" {o(4)}/>')
    s += SL(Z_SRED, _korobka(r1x - 10, r1y - 30, 70, 50, t, KREM, ZOL, True, .3, .2))
    s += SL(Z_SRED, figura(1160, 1000, 500, t, "#7a2a44", "#ffe2a8", False, .3))
    kiv = 6 * A.w(t, 1.6, .3)
    r2a, (r2ax, r2ay) = rukav(1110, 820, 130, -150 + kiv, t, "#7a2a44", "#ffe2a8", .2)
    r2b, (r2bx, r2by) = rukav(1210, 820, 130, -30 - kiv, t, "#7a2a44", "#ffe2a8", .4)
    s += SL(Z_SRED, r2a + r2b)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="24" ry="17" fill="#7a2a44" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2bx:.0f}" cy="{r2by:.0f}" rx="24" ry="17" fill="#7a2a44" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(900, 580, 450, 170, t, 37, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def monetka_za_chasy(t):
    """Тот же стол: часы уже на запястье жены, она кладёт монетку мужу на
    ладонь и слушает ход у самого уха."""
    rnd = random.Random(424)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 20)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="460" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="200" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, hodiki(1420, 360, t, .95))
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN2, KREM, 24))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="820" rx="340" ry="60" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="772" width="400" height="30" rx="8" fill="#fff" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, _korobka(1060, 750, 110, 80, t, KREM, TKAN, True, .4, .1))
    s += SL(Z_SRED, f'<ellipse cx="880" cy="800" rx="70" ry="30" fill="url(#med)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="700" y="780" width="60" height="50" rx="8" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1300" cy="800" rx="30" ry="16" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, svecha(1400, 740, t, .2, 1.0))
    s += SL(Z_SRED, f'<circle cx="1200" cy="800" r="20" fill="{ORA}" {o(3)}/>')
    s += SL(Z_SRED, figura(760, 1000, 500, t, "#3a3028", "#efe3c8", False, .0))
    s += SL(Z_SRED, figura(1160, 1000, 500, t, "#7a2a44", "#ffe2a8", False, .3))
    moneta = A.out(A.seg(t % 3.0, .2, .5))
    r1, (r1x, r1y) = rukav(840, 780, 150, -40, t, "#3a3028", "#efe3c8", .1)
    s += SL(Z_SRED, r1)
    # кисть не рисуем — работает сама монетка, лежащая на обшлаге рукава
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="20" ry="8" fill="#efe3c8" opacity=".5"/>')
    s += SL(Z_SRED, f'<circle cx="{r1x:.0f}" cy="{r1y-10-10*moneta:.0f}" r="14" fill="url(#med)" {o(2)}/>')
    r2a, (r2ax, r2ay) = rukav(1090, 800, 140, -150, t, "#7a2a44", "#ffe2a8", .2)
    r2b, (r2bx, r2by) = rukav(1230, 740, 120, -90, t, "#7a2a44", "#ffe2a8", .4)
    s += SL(Z_SRED, r2a + r2b)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="18" ry="7" fill="#ffe2a8" opacity=".5"/>')
    s += SL(Z_SRED, _chasy_karman(r2bx, r2by, .42, t, 1.0))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(900, 580, 450, 150, t, 38, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def podarki_vnuku_i_dedu(t):
    """Диван под ёлкой: внук с детскими часами, дед застёгивает свои часы,
    бабушка между ними держит блюдце с двумя монетками."""
    rnd = random.Random(425)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 21)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_SRED, _elka(240, 940, 560, t, 13, True))
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="460" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(450, 310, 2, 25, 90, 120))
    s += SL(Z_SRED, f'<rect x="560" y="760" width="1240" height="220" rx="30" fill="{TKAN2}" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="620" cy="780" rx="60" ry="30" fill="{KREM}" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, figura(640, 980, 400, t, "#3a5a7a", "#ffe2a8", False, .0))
    ekr = .6 + .4 * abs(A.w(t, 2.2))
    s += SL(Z_SRED, f'<rect x="580" y="900" width="60" height="40" rx="6" fill="{TKAN2}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="590" y="908" width="40" height="24" rx="3" fill="{SVET}" opacity="{ekr:.2f}"/>')
    s += SL(Z_SRED, lampa(1760, 420, t, .85, True))
    s += SL(Z_SRED, figura(1300, 1000, 540, t, "#2c3a2c", "#ffd98a", False, .4, boroda=True))
    zastyog = A.ease(A.seg(t % 3.0, .3, 1.0))
    r1, (r1x, r1y) = rukav(1388, 700, 170, -150 + 20 * zastyog, t, "#2c3a2c", "#ffd98a", .2)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="24" ry="17" fill="#2c3a2c" {o(4)}/>')
    s += SL(Z_SRED, figura(970, 1010, 480, t, "#3a2c3c", "#ffd98a", True, .2))
    r2, (r2x, r2y) = rukav(1040, 750, 120, -30, t, "#3a2c3c", "#ffd98a", .3)
    r3, (r3x, r3y) = rukav(895, 720, 90, -80, t, "#3a2c3c", "#ffd98a", .5)
    s += SL(Z_SRED, r2 + r3)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="24" ry="17" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y-6:.0f}" rx="40" ry="16" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{r2x-14:.0f}" cy="{r2y-10:.0f}" r="9" fill="url(#med)" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r3x:.0f}" cy="{r3y:.0f}" rx="20" ry="14" fill="#3a2c3c" {o(4)}/>')
    s += SL(Z_SRED, kot(1620, 920, t, .9, "#3b3430"))
    s += SL(Z_SRED, _napolnenie(900, 580, 450, 170, t, 39, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def nagradnye_chasy(t):
    """Заводской красный уголок: директор обеими руками подаёт футляр с
    карманными часами, рабочий принимает и прижимает кепку к груди."""
    rnd = random.Random(426)
    s = f'<rect width="{W}" height="{H}" fill="#5a3a2e"/>'
    s += nebo("sumer", t, False, 22)
    s += SL(Z_DAL, f'<rect x="0" y="40" width="{W}" height="760" fill="#6a4536" {o(5)}/>')
    s += SL(Z_SRED, teplo(960, 420, 260, 220, .4))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="440" rx="10" fill="#5a3a2a" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(450, 310, 2, 26, 100, 140))
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 120, KRAS, ZOL, 26))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="700" y="640" width="900" height="40" rx="8" fill="{KRAS}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="760" y="600" width="200" height="60" rx="8" fill="{KAMEN2}" {o(4)}/>')
    stopka = 4
    for i in range(stopka):
        s += SL(Z_SRED, f'<rect x="{1020+i*4:.0f}" y="{620-i*12:.0f}" width="160" height="16" rx="3" fill="{KREM}" {o(3)}/>')
    znam_sw = 5 * A.w(t, 1.4)
    s += SL(Z_SRED, f'<line x1="200" y1="160" x2="200" y2="700" stroke="url(#derev)" stroke-width="12"/>')
    s += SL(Z_SRED, f'<g transform="rotate({znam_sw:.1f} 200 200)"><path d="M200,180 h260 l-30,220 h-230 Z" fill="{KRAS}" opacity=".9" {o(5)}/></g>')
    s += SL(Z_SRED, f'<rect x="1400" y="260" width="320" height="220" rx="10" fill="{KAMEN2}" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<ellipse cx="{1460+i*100:.0f}" cy="360" rx="36" ry="46" fill="#2a2420" opacity=".7" {o(2)}/>')
    s += SL(Z_SRED, f'<path d="M900,700 l-20,-150 l50,20 l20,130 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, lampa(1700, 420, t, .85, False))
    peredacha = A.ease(A.seg(t, .3, 1.5))
    futl_x = 860 + 160 * peredacha
    futl = f'<rect x="{futl_x:.0f}" y="560" width="140" height="80" rx="10" fill="{KAMEN2}" {o(6)}/>'
    glow = .5 + .5 * abs(A.w(t, 1.4))
    futl += f'<circle cx="{futl_x+70:.0f}" cy="600" r="30" fill="{ZOL}" opacity="{glow:.2f}" {o(3)}/>'
    s += SL(Z_SRED, futl)
    s += SL(Z_SRED, figura(700, 1000, 520, t, "#2a2a3a", "#d6d0c0", False, .0))
    r1a, (r1ax, r1ay) = rukav(790, 780, 140, -10, t, "#2a2a3a", "#d6d0c0", .1)
    r1b, (r1bx, r1by) = rukav(950, 780, 110, -60, t, "#2a2a3a", "#d6d0c0", .3)
    s += SL(Z_SRED, r1a + r1b)
    s += SL(Z_SRED, f'<ellipse cx="{r1ax:.0f}" cy="{r1ay:.0f}" rx="24" ry="17" fill="#2a2a3a" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r1bx:.0f}" cy="{r1by:.0f}" rx="22" ry="15" fill="#2a2a3a" {o(4)}/>')
    s += SL(Z_SRED, figura(1260, 1000, 520, t, "#3a3a2c", "#d6a63f", False, .2, boroda=True))
    r2a, (r2ax, r2ay) = rukav(1180, 780, 130, -170, t, "#3a3a2c", "#d6a63f", .2)
    s += SL(Z_SRED, r2a)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="24" ry="17" fill="#3a3a2c" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1310" cy="880" rx="60" ry="30" fill="#4a3a2c" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 40, 4))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 40, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120a0a", .44))
    s += vinetka(.42)
    return s


# ═══════════════════════════ ДЕКОРАЦИИ 27-34 ══════════════════════════════
def otcovskie_chasy_na_tumbochke(t):
    """Мостик в память. Тумбочка у кровати: часы, очки, газета, стакан с
    ложкой; над тумбочкой увеличительное стекло — проём под часовой
    механизм. Отец крутит заводную головку своих часов."""
    rnd = random.Random(427)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 23)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += kvartira_veschi(1300, 700, 400, t, 20)
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="580" rx="14" fill="{TKAN2}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="60" y="860" width="640" height="160" rx="14" fill="{TKAN2}" {o(6)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<ellipse cx="{160+i*140:.0f}" cy="880" rx="70" ry="30" fill="{KREM}" opacity=".85" {o(3)}/>')
    tx, ty = 820, 680
    s += SL(Z_SRED, f'<rect x="{tx:.0f}" y="{ty:.0f}" width="260" height="280" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{tx+20:.0f}" y="{ty+20:.0f}" width="220" height="16" rx="4" fill="#efe3c8" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{tx+20:.0f}" y="{ty+56:.0f}" width="80" height="60" fill="#1a1c22" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{tx+160:.0f}" cy="{ty+90:.0f}" rx="30" ry="34" fill="#cfe4f5" opacity=".6" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="{tx+150:.0f}" y="{ty+70:.0f}" width="12" height="40" rx="4" fill="{K}" {o(2)}/>')
    gaz = A.ease(A.seg(t, .5, 2.0)) * 20
    s += SL(Z_SRED, f'<rect x="{tx+20:.0f}" y="{ty+80+gaz:.0f}" width="150" height="100" fill="#e8e2d0" {o(3)}/>')
    s += SL(Z_SRED, lampa(tx + 230, ty - 40, t, .85, False))
    px, py, pr = tx + 40, ty - 220, 190
    vid = (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr:.0f}" fill="#cfd6de"/>'
           f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr*.6:.0f}" fill="none" stroke="{K}" stroke-width="2"/>')
    mech_a = (t * 160) % 360
    vid += f'<circle cx="{px-20:.0f}" cy="{py:.0f}" r="40" fill="url(#zol)" {o(2)}/>'
    vid += f'<g transform="rotate({mech_a:.1f} {px-20:.0f} {py:.0f})"><line x1="{px-20:.0f}" y1="{py:.0f}" x2="{px-20:.0f}" y2="{py-30:.0f}" stroke="{K}" stroke-width="3"/></g>'
    vid += f'<circle cx="{px+40:.0f}" cy="{py+10:.0f}" r="26" fill="{ZHELEZ}" {o(2)}/>'
    lupa = f'<rect x="{px-10:.0f}" y="{py+pr-10:.0f}" width="20" height="90" fill="url(#zhel)" {o(5)}/>'
    put = kontur_proema(px - pr, py - pr, pr * 2, pr * 2, "ellips")
    sten = lupa + f'<path d="{put}" fill="#1a140e"/>' + vid + mesto_stoka(px - pr, py - pr, pr * 2, pr * 2, "ellips")
    sten += f'<path d="{put}" fill="none" {o(10)}/>'
    s += SL(Z_SRED, sten)
    s += SL(Z_SRED, figura(600, 1010, 480, t, "#efe3c8", "#cfe4f5", False, .0))
    krut = (t * 300) % 360
    r, (rx, ry) = rukav(680, 820, 130, -20, t, "#efe3c8", "#cfe4f5", .1)
    s += SL(Z_SRED, r)
    s += SL(Z_SRED, f'<g transform="rotate({krut:.1f} {rx:.0f} {ry:.0f})"><ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="22" ry="16" fill="#efe3c8" {o(4)}/></g>')
    s += SL(Z_SRED, f'<ellipse cx="500" cy="920" rx="80" ry="30" fill="#5a3a26" opacity=".5" {o(2)}/>')
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 41, 5))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 41, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.42)
    return s


def chasy_iz_vitriny_dlya_sebya(t):
    """Витрина часового отдела: покупательница прикладывает часы к
    запястью и смотрит в зеркало, довольная; продавец за прилавком."""
    rnd = random.Random(428)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 24)
    s += SL(Z_DAL, f'<rect x="0" y="40" width="{W}" height="760" fill="{KAMEN2}" opacity=".6" {o(5)}/>')
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="300" y="620" width="1300" height="160" rx="10" fill="url(#stekl)" opacity=".5" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="760" width="1300" height="200" fill="#3a3028" {o(6)}/>')
    rnd2 = random.Random(7)
    for i in range(9):
        wx = 340 + i * 140
        kind = i % 3
        if kind == 0:
            s += SL(Z_SRED, _chasy_karman(wx, 700, .55, t, 1.0))
        elif kind == 1:
            s += SL(Z_SRED, f'<circle cx="{wx:.0f}" cy="700" r="30" fill="url(#med)" {o(3)}/>')
        else:
            s += SL(Z_SRED, f'<ellipse cx="{wx:.0f}" cy="700" rx="34" ry="14" fill="{KREM}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="900" y="260" width="300" height="360" rx="8" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _chasy_sten(1050, 420, 1.0, t))
    s += SL(Z_SRED, f'<rect x="1400" y="250" width="280" height="370" rx="8" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(1430, 280, 2, 24, 100, 140))
    s += SL(Z_SRED, f'<rect x="1500" y="700" width="200" height="30" rx="6" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="340" rx="8" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="220" height="140" rx="4" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    galka_on = ((t * .8) % 3.0) > 1.6
    if galka_on:
        s += SL(Z_SRED, _galochka(900, 480, 1.2, t))
    s += SL(Z_SRED, figura(560, 1000, 520, t, "#2a2e3c", "#cfe4f5", False, .0))
    s += SL(Z_SRED, f'<rect x="490" y="840" width="140" height="60" rx="8" fill="{KREM}" opacity=".7" {o(3)}/>')
    s += SL(Z_SRED, figura(1140, 1010, 500, t, "#3a3028", "#9aa0a4", False, .2, shapka=False))
    prikl = A.ease(A.seg(t % 4.0, .3, 1.0))
    r, (rx, ry) = rukav(1220, 840, 140, -100 - 30 * prikl, t, "#3a3028", "#9aa0a4", .1)
    s += SL(Z_SRED, r)
    s += SL(Z_SRED, f'<ellipse cx="{rx:.0f}" cy="{ry:.0f}" rx="24" ry="17" fill="#3a3028" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="{rx:.0f}" cy="{ry-6:.0f}" r="16" fill="url(#med)" {o(2)}/>')
    s += SL(Z_SRED, svecha(260, 680, t, .2, .8))
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 42, 4))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 42, 4))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.4)
    return s


def ostroe_na_barhate(t):
    """Футляр на бархате: нож, ножницы, вилка, булавка вспыхивают по
    словам; запрещающая черта нависает над ним. Людей нет."""
    rnd = random.Random(429)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 25)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += utvar_izby(1240, 420, 380, t, 23)
    s += SL(Z_SRED, polovicy(820))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="420" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, _kartiny_ryad(450, 310, 1, 29, 110, 150))
    s += SL(Z_SRED, f'<rect x="500" y="680" width="900" height="40" rx="8" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="560" y="600" width="780" height="90" rx="12" fill="#2a1414" {o(6)}/>')
    items = (("nozh", 640), ("nozhnicy", 840), ("vilka", 1040), ("bulavka", 1240))
    for i, (kind, ix) in enumerate(items):
        on = (t % 4.0) > i * .9
        op = .3 + .7 * (1 if on else 0)
        if kind == "nozh":
            s += SL(Z_SRED, f'<g opacity="{op:.2f}"><path d="M{ix-50:.0f},630 l100,-6 l-14,16 l-86,4 Z" fill="{ZHELEZ}" {o(3)}/>'
                            f'<rect x="{ix+40:.0f}" y="624" width="40" height="16" rx="4" fill="#5a3a26" {o(2)}/></g>')
        elif kind == "nozhnicy":
            s += SL(Z_SRED, f'<g opacity="{op:.2f}"><path d="M{ix-30:.0f},610 l50,40 M{ix+20:.0f},610 l-50,40" stroke="{ZHELEZ}" stroke-width="8"/>'
                            f'<circle cx="{ix-5:.0f}" cy="630" r="7" fill="{ZHELEZ}"/></g>')
        elif kind == "vilka":
            s += SL(Z_SRED, f'<g opacity="{op:.2f}">')
            for j in range(3):
                s += SL(Z_SRED, f'<line x1="{ix-16+j*16:.0f}" y1="610" x2="{ix-16+j*16:.0f}" y2="650" stroke="{ZHELEZ}" stroke-width="6"/>')
            s += SL(Z_SRED, '</g>')
        else:
            s += SL(Z_SRED, f'<g opacity="{op:.2f}"><line x1="{ix:.0f}" y1="610" x2="{ix:.0f}" y2="650" stroke="{ZHELEZ}" stroke-width="4"/>'
                            f'<circle cx="{ix:.0f}" cy="608" r="8" fill="{KRAS}"/></g>')
    cherta_y = 480 + 140 * A.ease(A.seg(t, .6, 1.4))
    s += SL(Z_SRED, _zapret(950, cherta_y, 220, t))
    s += SL(Z_SRED, f'<rect x="300" y="700" width="160" height="30" rx="6" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1400" y="700" width="120" height="110" rx="10" fill="{TKAN}" opacity=".8" {o(4)}/>')
    bant_sw = 3 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<g transform="rotate({bant_sw:.1f} 1460 740)"><circle cx="1460" cy="740" r="18" fill="{ZOL}" {o(3)}/></g>')
    s += SL(Z_SRED, f'<path d="M600,720 l-16,-110 l40,20 l16,90 Z" fill="{ZEL}" {o(4)}/>')
    s += SL(Z_SRED, svecha(1600, 680, t, .3, 1.0))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN2, KREM, 43))
    s += SL(Z_SRED, _napolnenie(420, 600, 1080, 100, t, 43, 7))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .42))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.44)
    return s


def nozh_na_razdelochnoy_doske(t):
    """Кухонный стол: нож на доске, мать поднимает его выше, мальчик
    прячет руки за спину."""
    rnd = random.Random(430)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("den", t, False, 26)
    s += SL(Z_DAL, doski(0, 0, W, 760, 70, False, "dosk"))
    s += kvartira_veschi(1260, 700, 380, t, 25)
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, stol(460, 780, 900, 36))
    s += SL(Z_SRED, f'<rect x="700" y="740" width="320" height="24" rx="6" fill="url(#dosk)" {o(5)}/>')
    s += SL(Z_SRED, karavay(640, 740, .7, False))
    podn = A.out(A.seg(t % 3.0, .3, .6))
    s += SL(Z_SRED, f'<ellipse cx="560" cy="760" rx="34" ry="30" fill="#b5803a" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1100" cy="760" rx="36" ry="30" fill="{KRAS}" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1180" y="760" width="90" height="20" rx="5" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="1280" cy="790" r="26" fill="#efe3c8" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="760" cy="800" rx="46" ry="40" fill="{CHUGUN}" {o(4)}/>')
    укроп_sw = 4 * A.w(t, 2.2)
    s += SL(Z_SRED, f'<g transform="rotate({укроп_sw:.1f} 1000 790)"><path d="M1000,790 l0,-50" stroke="{ZEL}" stroke-width="5"/>'
                    f'<path d="M1000,750 q-14,-10 -24,-4 M1000,750 q14,-10 24,-4" fill="none" stroke="{ZEL}" stroke-width="3"/></g>')
    s += SL(Z_SRED, figura(560, 1010, 500, t, "#efe3c8", "#9c7049", False, .0))
    # кисть не рисуем: рукав оканчивается обшлагом прямо на рукояти ножа —
    # нож рисуется ПОСЛЕ рукава, на его же конце (R-0051, его слово 15.11)
    r1, (r1x, r1y) = rukav(640, 700, 150, -70 + 10 * podn, t, "#efe3c8", "#9c7049", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="18" ry="7" fill="#9c7049" opacity=".6"/>')
    s += SL(Z_SRED, _nozh_bolshoy(r1x, r1y, 280, t, 0))
    r2, (r2x, r2y) = rukav(480, 780, 120, -150, t, "#efe3c8", "#9c7049", .3)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="18" ry="7" fill="#9c7049" opacity=".6"/>')
    s += SL(Z_SRED, figura(1420, 1030, 320, t, "#2a4a6a", "#efe3c8", False, .3, naklon=-4))
    s += SL(Z_SRED, lampa(1700, 420, t, .9, True))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="260" height="420" rx="8" fill="{KAMEN2}" {o(5)}/>')
    s += SL(Z_SRED, _kovrik_pol(500, 900, 760, 110, TKAN2, KREM, 44))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="240" height="420" rx="8" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="1156" y="300" width="208" height="180" rx="5" fill="url(#stekl)" opacity=".5" {o(3)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 760, 150, t, 44, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .36))
    s += vinetka(.36)
    return s


def nozhnicy_za_kopeyku(t):
    """Швейный столик: новые ножницы с бантом придвигаются подруге;
    портниха кладёт на стол монетку. Ярлык «продано» загорается."""
    rnd = random.Random(431)
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += nebo("sumer", t, False, 27)
    s += SL(Z_DAL, brevna(0, 40, W, 760, 88))
    s += SL(Z_DAL, okno_izby(1500, 160, 260, 220, t, svet=True, moroz=.3))
    s += SL(Z_SRED, teplo(1620, 280, 260, 220, .34))
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="280" width="280" height="460" rx="10" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="440" y="300" width="240" height="200" rx="6" fill="url(#stekl)" opacity=".5" {o(4)}/>')
    s += SL(Z_SRED, _kovrik_pol(480, 900, 760, 110, TKAN, KREM, 31))
    s += SL(Z_SRED, stol(560, 780, 800, 34))
    s += SL(Z_SRED, f'<rect x="620" y="740" width="200" height="90" rx="10" fill="{ZHELEZ}" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="680" cy="800" r="26" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="770" rx="40" ry="22" fill="{TKAN}" {o(4)}/>')
    rnd2 = random.Random(3)
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{880+ (i%3)*22-22:.0f}" cy="{760+(i//3)*16:.0f}" r="3" fill="{ZHELEZ}"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<ellipse cx="{1050+i*40:.0f}" cy="770" rx="24" ry="30" fill="{(TKAN2,ZEL2,KREM)[i]}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1200" y="750" width="120" height="70" rx="6" fill="{RUSH}" opacity=".85" {o(3)}/>')
    pridv = A.ease(A.seg(t, .3, .9))
    nx = 780 + 140 * pridv
    s += SL(Z_SRED, f'<path d="M{nx-30:.0f},740 l50,40 M{nx+20:.0f},740 l-50,40" stroke="{ZHELEZ}" stroke-width="7"/>')
    s += SL(Z_SRED, f'<circle cx="{nx-5:.0f}" cy="760" r="20" fill="{KRAS}" {o(3)}/>')
    sant = 6 * A.w(t, 1.5)
    s += SL(Z_SRED, f'<path d="M700,740 q{sant:.0f},40 0,90" fill="none" stroke="{KREM}" stroke-width="8"/>')
    moneta = A.out(A.seg(t, 1.2, .6))
    s += SL(Z_SRED, f'<circle cx="1180" cy="{800-10*moneta:.0f}" r="16" fill="url(#med)" {o(2)}/>')
    yarl_on = (t % 4.0) > 2.2
    if yarl_on:
        s += SL(Z_SRED, f'<rect x="1300" y="680" width="70" height="40" rx="6" fill="{ZOL}" {o(3)}/>')
    s += SL(Z_SRED, figura(720, 1000, 440, t, "#3a3028", "#9aa0a4", False, .0))
    s += SL(Z_SRED, figura(1240, 1000, 440, t, "#7a2a44", "#ffe2a8", False, .2))
    r2, (r2x, r2y) = rukav(1160, 820, 110, -170, t, "#7a2a44", "#ffe2a8", .3)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="22" ry="15" fill="#7a2a44" {o(4)}/>')
    s += SL(Z_SRED, svecha(960, 700, t, .2, .9))
    s += SL(Z_SRED, f'<rect x="1140" y="280" width="260" height="420" rx="10" fill="#5a3a4a" {o(6)}/>')
    s += SL(Z_SRED, _napolnenie(420, 600, 1080, 100, t, 45, 6))
    s += SL(Z_PERED, ramka_pp("oba", "#120e0e", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 6, 5, .25, .5))
    s += vinetka(.4)
    return s


def nabor_nozhey_dlya_docheri(t):
    """Современная кухня: коробка ножей, подставка едет к дочери за
    монетку; в проёме открытой дверцы шкафчика — настоящая нарезка."""
    rnd = random.Random(432)
    s = f'<rect width="{W}" height="{H}" fill="#e8eef0"/>'
    s += nebo("den", t, False, 28)
    s += SL(Z_DAL, f'<rect x="0" y="40" width="{W}" height="760" fill="{BETON}" opacity=".5" {o(5)}/>')
    s += SL(Z_SRED, polovicy(800))
    s += SL(Z_SRED, f'<rect x="420" y="300" width="280" height="420" rx="8" fill="{KAMEN2}" {o(6)}/>')
    s += SL(Z_SRED, _kovrik_pol(460, 900, 700, 110, KAMEN, KREM, 32))
    s += SL(Z_SRED, f'<rect x="300" y="700" width="1200" height="40" rx="8" fill="{KAMEN}" {o(6)}/>')
    px, py, pw, ph_ = 1020, 300, 760, 300
    vid = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw}" height="{ph_}" fill="{KREM}"/>'
           f'<rect x="{px+60:.0f}" y="{py+100:.0f}" width="200" height="30" fill="#efe3c8"/>'
           f'<ellipse cx="{px+300:.0f}" cy="{py+140:.0f}" rx="40" ry="26" fill="{KRAS}" opacity=".7"/>')
    put = kontur_proema(px, py, pw, ph_, "pryam")
    shkf = f'<rect x="{px-30:.0f}" y="{py-40:.0f}" width="{pw+60}" height="60" fill="url(#derev)" {o(6)}/>'
    shkf += f'<path d="{put}" fill="#1a140e"/>' + vid + mesto_stoka(px, py, pw, ph_, "pryam")
    shkf += f'<path d="{put}" fill="none" {o(8)}/>'
    s += SL(Z_SRED, shkf)
    tyan = A.ease(A.seg(t, .4, 1.0))
    podx = 620 - 100 * tyan
    box_x = 640 - 60 * (1 - tyan)
    s += SL(Z_SRED, f'<rect x="{box_x:.0f}" y="640" width="260" height="90" rx="10" fill="{KAMEN2}" opacity=".3" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{podx:.0f}" y="650" width="220" height="60" rx="10" fill="url(#derev)" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="{podx+20+i*40:.0f}" y="590" width="10" height="70" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, f'<rect x="960" y="600" width="140" height="70" rx="8" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1240" cy="640" rx="50" ry="40" fill="{KAMEN2}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1420" cy="660" rx="40" ry="30" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1500" y="640" width="60" height="50" rx="6" fill="{RUSH}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1600,700 l-16,-100 l40,18 l16,82 Z" fill="{ZEL}" {o(4)}/>')
    kach = 4 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 1660 600)"><path d="M1660,600 h40 v16 h-40 Z" fill="{TKAN}" {o(3)}/></g>')
    s += SL(Z_SRED, figura(480, 1000, 500, t, "#efe3c8", "#9c7049", False, .0))
    r1a, (r1ax, r1ay) = rukav(560, 800, 140, -30, t, "#efe3c8", "#9c7049", .1)
    r1b, (r1bx, r1by) = rukav(400, 800, 140, -150, t, "#efe3c8", "#9c7049", .3)
    s += SL(Z_SRED, r1a + r1b)
    s += SL(Z_SRED, f'<ellipse cx="{r1ax:.0f}" cy="{r1ay:.0f}" rx="24" ry="17" fill="#efe3c8" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r1bx:.0f}" cy="{r1by:.0f}" rx="24" ry="17" fill="#efe3c8" {o(4)}/>')
    s += SL(Z_SRED, figura(800, 1010, 480, t, "#2a4a6a", "#efe3c8", False, .2))
    r2, (r2x, r2y) = rukav(870, 820, 110, -70, t, "#2a4a6a", "#efe3c8", .2)
    s += SL(Z_SRED, r2)
    s += SL(Z_SRED, f'<ellipse cx="{r2x:.0f}" cy="{r2y:.0f}" rx="22" ry="15" fill="#2a4a6a" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="{r2x:.0f}" cy="{r2y-6:.0f}" r="14" fill="url(#med)" {o(2)}/>')
    s += SL(Z_SRED, lampa(240, 420, t, .9, True))
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 46, 6))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 46, 5))
    s += SL(Z_PERED, ramka_pp("oba", "#1a1e20", .3))
    s += vinetka(.3)
    return s


def perochinnyy_nozhik_ot_deda(t):
    """Мостик в память. Летнее крыльцо: дед на раскрытой ладони держит
    складной ножик, внук тянется обеими руками принять его."""
    rnd = random.Random(433)
    s = f'<rect width="{W}" height="{H}" fill="#cfe4c8"/>'
    s += nebo("den", t, False, 29)
    s += SL(Z_DAL, oblaka(t, 140, 4, 31, .4, "#f4f8ee", 9.0))
    s += SL(Z_DAL, pleten(0, 820, 500, 170, 5))
    s += SL(Z_DAL, izba_snaruzhi(420, 820, 540, t, False, True, 29))
    s += SL(Z_DAL, f'<path d="M1240,820 l-16,-320 l32,0 Z" fill="{ZEL}" {o(4)}/>')
    for i in range(5):
        a = i * .9
        s += SL(Z_DAL, f'<circle cx="{1240+math.cos(a)*90:.0f}" cy="{620+math.sin(a)*40:.0f}" r="34" fill="{ZOL}" {o(3)}/>')
        s += SL(Z_DAL, f'<circle cx="{1240+math.cos(a)*90:.0f}" cy="{620+math.sin(a)*40:.0f}" r="14" fill="#5a3a26" {o(2)}/>')
    # поленница у крыльца и колодец — двор не пустой
    for row in range(3):
        for col in range(5):
            s += SL(Z_SRED, f'<circle cx="{1340+col*38:.0f}" cy="{880-row*36:.0f}" r="18" fill="url(#derev)" {o(3)}/>')
            s += SL(Z_SRED, f'<circle cx="{1340+col*38:.0f}" cy="{880-row*36:.0f}" r="10" fill="{KREM}" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="300" y="780" width="1300" height="60" rx="10" fill="url(#dosk)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="300" y="700" width="20" height="90" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="1560" y="700" width="20" height="90" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<line x1="300" y1="700" x2="1580" y2="700" stroke="url(#derev)" stroke-width="12"/>')
    s += SL(Z_SRED, f'<ellipse cx="1480" cy="840" rx="50" ry="40" fill="{ZHELEZ}" opacity=".85" {o(4)}/>')
    s += SL(Z_SRED, f'<line x1="400" y1="780" x2="440" y2="560" stroke="url(#derev)" stroke-width="8"/>')
    s += SL(Z_SRED, f'<line x1="440" y1="780" x2="480" y2="560" stroke="url(#derev)" stroke-width="8"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="800" width="60" height="50" rx="6" fill="#8a7a5a" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, svecha(1200, 760, t, .2, .7))
    s += SL(Z_SRED, figura(700, 940, 460, t, "#4a3a2a", "#f4e8c8", False, .0, shapka=True))
    kiv = 4 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kiv:.1f} 700 700)">')
    nozh_x, nozh_y = 800, 780
    s += SL(Z_SRED, f'<ellipse cx="{nozh_x:.0f}" cy="{nozh_y:.0f}" rx="40" ry="20" fill="#4a3a2a" opacity=".3"/>')
    s += SL(Z_SRED, f'<rect x="{nozh_x-22:.0f}" y="{nozh_y-8:.0f}" width="44" height="14" rx="5" fill="#6b4428" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{nozh_x+20:.0f},{nozh_y:.0f} l34,-4 l-6,8 l-28,4 Z" fill="{ZHELEZ}" {o(2)}/>')
    s += SL(Z_SRED, '</g>')
    tyan = A.ease(A.seg(t, .6, 1.4))
    s += SL(Z_SRED, figura(1000, 920, 320, t, "#cfe4c8", "#f4e8c8", False, .3, naklon=-4 * tyan))
    r2a, (r2ax, r2ay) = rukav(940, 795, 100, -20, t, "#cfe4c8", "#f4e8c8", .2)
    r2b, (r2bx, r2by) = rukav(1060, 795, 100, -160, t, "#cfe4c8", "#f4e8c8", .4)
    s += SL(Z_SRED, r2a + r2b)
    s += SL(Z_SRED, f'<ellipse cx="{r2ax:.0f}" cy="{r2ay:.0f}" rx="20" ry="14" fill="#cfe4c8" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{r2bx:.0f}" cy="{r2by:.0f}" rx="20" ry="14" fill="#cfe4c8" {o(4)}/>')
    s += SL(Z_SRED, kot(300, 860, t, .8, "#3b3430", True))
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 47, 4))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 47, 4))
    s += SL(Z_PERED, f'<rect x="0" y="980" width="{W}" height="100" fill="{TRAVA}" opacity=".6"/>')
    return s


def struzhka_i_svistulka(t):
    """Мостик в память. Тот же мальчик на бревне у реки режет ивовый прут
    ножиком, стружка летит; откладывает прут, берёт свистульку и свистит."""
    rnd = random.Random(434)
    s = f'<rect width="{W}" height="{H}" fill="#cfe4e8"/>'
    s += nebo("den", t, False, 30)
    s += SL(Z_DAL, oblaka(t, 140, 4, 33, .4, "#f4f8ee", 9.0))
    s += SL(Z_DAL, f'<rect x="0" y="760" width="{W}" height="320" fill="{VODA}" opacity=".7" {o(5)}/>')
    for i in range(6):
        bl = .3 + .4 * abs(A.w(t, 1.6 + i * .2, i * .3))
        s += SL(Z_DAL, f'<ellipse cx="{200+i*300:.0f}" cy="{820+i%2*60:.0f}" rx="120" ry="14" fill="#eaf4ff" opacity="{bl:.2f}"/>')
    s += SL(Z_DAL, f'<path d="M1500,900 q80,-160 220,-160 l0,340 h-220 Z" fill="{ZEL}" {o(5)}/>')
    s += SL(Z_DAL, goloe_derevo(560, 780, 420, t, 12, 8, "#3c5a3a", inej_=False))
    s += SL(Z_DAL, f'<path d="M420,780 q0,-90 60,-100 q60,10 60,100 Z" fill="{ZEL2}" {o(4)}/>')
    s += SL(Z_DAL, f'<path d="M1140,780 q0,-80 50,-90 q50,10 50,90 Z" fill="{ZEL2}" {o(4)}/>')
    s += SL(Z_DAL, izba_snaruzhi(1240, 800, 360, t, False, True, 34))
    s += SL(Z_DAL, f'<path d="M780,780 q0,-120 70,-130 q70,10 70,130 Z" fill="{ZEL}" {o(5)}/>')
    s += SL(Z_DAL, f'<path d="M950,780 q0,-100 60,-110 q60,10 60,110 Z" fill="{ZEL2}" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="920" rx="340" ry="62" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="896" rx="300" ry="30" fill="#6b4428" {o(4)}/>')
    stryazhka_sp = A.w(t, 1.4) * 10
    s += SL(Z_SRED, f'<g transform="rotate({3*A.w(t,1.2):.1f} 820 820)">'
                    f'<path d="M820,820 l-6,-200 l10,2 l4,198 Z" fill="#d8c8a4" {o(4)}/></g>')
    letit = (t * 1.6) % 1.0
    for i in range(5):
        p = (letit + i * .2) % 1.0
        s += SL(Z_SRED, f'<path d="M{880-40*p+stryazhka_sp:.0f},{780-60*p:.0f} q10,-6 16,2 q-4,8 -14,8 Z" fill="#e8d8b4" opacity="{1-p:.2f}"/>')
    svist_on = (t % 4.0) > 2.4
    s += SL(Z_SRED, figura(700, 1000, 380, t, "#3a5a3a", "#f4e8c8", False, .0, profil=False))
    ang = -110 if not svist_on else -40
    r1, (r1x, r1y) = rukav(760, 850, 130, ang, t, "#3a5a3a", "#f4e8c8", .1)
    s += SL(Z_SRED, r1)
    s += SL(Z_SRED, f'<ellipse cx="{r1x:.0f}" cy="{r1y:.0f}" rx="20" ry="14" fill="#3a5a3a" {o(4)}/>')
    if svist_on:
        s += SL(Z_SRED, f'<path d="M{r1x:.0f},{r1y:.0f} l20,6 l-4,10 l-18,-8 Z" fill="{ZOL}" {o(2)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1050" cy="900" rx="44" ry="18" fill="#8a7a5a" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, f'<line x1="1100" y1="900" x2="1300" y2="760" stroke="#6b4428" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="1140" y="900" width="60" height="50" rx="6" fill="#8a7a5a" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, f'<ellipse cx="500" cy="900" rx="60" ry="24" fill="{ZOL}" opacity=".8" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M580,900 h100 l-10,30 h-80 Z" fill="#c8a06a" {o(3)}/>')
    skok = abs(A.w(t, 2.4)) * 10
    s += SL(Z_SRED, f'<ellipse cx="{420+skok:.0f}" cy="920" rx="16" ry="10" fill="{ZEL2}" {o(2)}/>')
    s += SL(Z_SRED, svecha(1400, 820, t, .2, .6))
    s += SL(Z_SRED, f'<rect x="420" y="600" width="220" height="160" rx="10" fill="#6b4428" opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, _napolnenie(420, 620, 1080, 100, t, 48, 6))
    s += SL(Z_SRED, _sloi_fona(110, 240, 1700, 700, t, 48, 7))
    s += SL(Z_SRED, _napolnenie(110, 240, 1700, 700, t, 48, 6))
    s += SL(Z_PERED, f'<rect x="0" y="980" width="{W}" height="100" fill="{TRAVA}" opacity=".5"/>')
    return s
