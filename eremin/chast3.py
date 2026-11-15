# -*- coding: utf-8 -*-
"""Декорации 69-102 ролика «17 ноября — Ерёмин день»."""
import math, random
from baza import *
import anim as A
from lok_obshchee import *


# ── предметы последней трети ───────────────────────────────────────────────
# Здесь живут вещи, которых нет ни в baza.py, ни в lok_obshchee.py: зимняя
# обувка и рукавицы, батарея, чайник, светец, кинокамера, афиша, мышь в
# платочке. Каждая опознаётся силуэтом с первого взгляда — его правило 14.11.

def _rozhica(x, y, r_, t, ph=.0, hitraya=True, col="#2b1708"):
    """Рожица рисованного героя (огонёк, Ветер, Вихрь): глаза с бликом,
    брови домиком и косая ухмылка. Букв нет — только мимика."""
    kos = r_ * .22 * A.w(t, 1.3, ph)
    mig = A.blink(t, 3.4, ph)
    s = ""
    for i in (-1, 1):
        ex = x + i * r_ * .42
        s += (f'<ellipse cx="{ex:.0f}" cy="{y:.0f}" rx="{r_*.26:.0f}"'
              f' ry="{(r_*.07 if mig else r_*.30):.1f}" fill="#fff6e2"'
              f' stroke="{col}" stroke-width="{max(2, r_*.05):.1f}"/>')
        if not mig:
            s += (f'<circle cx="{ex+kos:.0f}" cy="{y+r_*.04:.0f}" r="{r_*.12:.0f}"'
                  f' fill="{col}"/>')
            s += (f'<circle cx="{ex+kos-r_*.05:.0f}" cy="{y-r_*.07:.0f}"'
                  f' r="{r_*.045:.0f}" fill="#ffffff" opacity=".9"/>')
        s += (f'<path d="M{ex-r_*.30:.0f},{y-r_*.44+(0 if hitraya else r_*.1)*i:.0f}'
              f' q{r_*.30:.0f},{-r_*.22 if hitraya else -r_*.05:.0f} {r_*.60:.0f},'
              f'{r_*.06 if hitraya else 0:.0f}" fill="none" stroke="{col}"'
              f' stroke-width="{max(3, r_*.08):.1f}" stroke-linecap="round"/>')
    if hitraya:
        s += (f'<path d="M{x-r_*.34:.0f},{y+r_*.44:.0f} q{r_*.40:.0f},{r_*.34:.0f}'
              f' {r_*.74:.0f},{-r_*.12:.0f}" fill="none" stroke="{col}"'
              f' stroke-width="{max(3, r_*.09):.1f}" stroke-linecap="round"/>')
    else:
        s += (f'<ellipse cx="{x:.0f}" cy="{y+r_*.50:.0f}" rx="{r_*.24:.0f}"'
              f' ry="{r_*.16+r_*.06*A.w(t,.9,ph):.1f}" fill="{col}"/>')
    return s


def _valenok(x, y, s_=1.0, t=0.0, ph=.0, galosha=True, col="#c4b091", naklon=0.0):
    """Валенок ПРОСТОЙ И УЗНАВАЕМОЙ геометрией: толстое прямое голенище и
    отдельная ступня с тупым носком, выступающая вперёд. Сложный контур
    читался корзиной — поправлено по осмотру."""
    hh, w_ = 200 * s_, 92 * s_
    ug = naklon + 1.2 * A.w(t, 2.8, ph)
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    s += ten(x + w_ * .3, y + 8 * s_, w_ * .9, 12 * s_, .42)
    # ступня: длинный блок с круглым носком
    s += (f'<path d="M{x-w_*.42:.0f},{y-hh*.40:.0f} h{w_*.70:.0f}'
          f' q{w_*.56:.0f},{hh*.04:.0f} {w_*.60:.0f},{hh*.22:.0f}'
          f' q{w_*.04:.0f},{hh*.16:.0f} {-w_*.22:.0f},{hh*.17:.0f}'
          f' h{-w_*1.08:.0f} Z" fill="{col}" {o(max(4, 7*s_))}/>')
    # голенище: прямой толстый рукав с валиком сверху
    s += (f'<rect x="{x-w_*.46:.0f}" y="{y-hh:.0f}" width="{w_*.92:.0f}"'
          f' height="{hh*.64:.0f}" rx="{w_*.14:.0f}" fill="{col}"'
          f' {o(max(4, 7*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*.46:.0f}"'
          f' ry="{14*s_:.0f}" fill="#9c8c72" {o(max(3, 5*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh+6*s_:.0f}" rx="{w_*.34:.0f}"'
          f' ry="{8*s_:.0f}" fill="#7d7160" opacity=".8"/>')
    for i in range(4):                   # войлок: короткие вертикальные штрихи
        s += (f'<path d="M{x-w_*.28+i*w_*.19:.0f},{y-hh*.88:.0f}'
              f' q{4*s_:.0f},{hh*.14:.0f} {1*s_:.0f},{hh*.28:.0f}" fill="none"'
              f' stroke="#ded0b4" stroke-width="{max(3, 7*s_):.0f}"'
              f' opacity=".55"/>')
    s += (f'<path d="M{x-w_*.44:.0f},{y-hh*.44:.0f} h{w_*.88:.0f}"'
          f' stroke="#9c8c72" stroke-width="{max(3, 7*s_):.0f}" opacity=".7"/>')
    if galosha:                          # галоша: тёмная глянцевая опушка
        s += (f'<path d="M{x-w_*.50:.0f},{y-hh*.26:.0f}'
              f' q{-w_*.04:.0f},{hh*.30:.0f} {w_*.34:.0f},{hh*.30:.0f}'
              f' h{w_*.62:.0f} q{w_*.30:.0f},{-hh*.02:.0f}'
              f' {w_*.12:.0f},{-hh*.20:.0f} q{-w_*.28:.0f},{-hh*.14:.0f}'
              f' {-w_*1.08:.0f},{-hh*.08:.0f} Z" fill="#26282b"'
              f' {o(max(3, 5*s_))}/>')
        s += (f'<path d="M{x-w_*.50:.0f},{y-hh*.26:.0f} q{w_*.50:.0f},{hh*.06:.0f}'
              f' {w_*1.10:.0f},{hh*.02:.0f}" fill="none" stroke="#dfe8ef"'
              f' stroke-width="{max(3, 7*s_):.0f}" opacity=".85"/>')
        s += (f'<path d="M{x-w_*.36:.0f},{y-hh*.16:.0f} q{w_*.46:.0f},{hh*.10:.0f}'
              f' {w_*.96:.0f},{hh*.01:.0f}" fill="none" stroke="#9fb4c2"'
              f' stroke-width="{max(3, 6*s_):.0f}"'
              f' opacity="{.4+.3*abs(A.w(t,2.4,ph)):.2f}"/>')
    return s + '</g>'


def _varezhka(x, y, s_=1.0, t=0.0, ph=.0, col=TKAN, visit=True):
    """Рукавица: ладонь овалом, отставленный большой палец, манжет полосками."""
    w_, hh = 70 * s_, 112 * s_
    ug = (9 if visit else 0) * A.w(t, 2.2, ph)
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x-w_*.44:.0f},{y:.0f} q{-w_*.14:.0f},{hh*.52:.0f} {w_*.10:.0f},{hh*.70:.0f}'
          f' q{w_*.38:.0f},{hh*.16:.0f} {w_*.72:.0f},0 q{w_*.22:.0f},{-hh*.22:.0f}'
          f' {w_*.04:.0f},{-hh*.70:.0f} Z" fill="{col}" {o(max(3, 5*s_))}/>')
    s += (f'<path d="M{x-w_*.40:.0f},{y+hh*.22:.0f} q{-w_*.40:.0f},{hh*.06:.0f}'
          f' {-w_*.30:.0f},{hh*.34:.0f} q{w_*.20:.0f},{hh*.10:.0f} {w_*.36:.0f},{-hh*.14:.0f} Z"'
          f' fill="{col}" {o(max(3, 5*s_))}/>')
    s += (f'<rect x="{x-w_*.46:.0f}" y="{y-hh*.16:.0f}" width="{w_*.92:.0f}"'
          f' height="{hh*.20:.0f}" rx="{8*s_:.0f}" fill="{KREM}" {o(max(2, 4*s_))}/>')
    for i in range(3):
        s += (f'<line x1="{x-w_*.42:.0f}" y1="{y-hh*.10+i*hh*.055:.0f}"'
              f' x2="{x+w_*.42:.0f}" y2="{y-hh*.10+i*hh*.055:.0f}" stroke="#c2ab86"'
              f' stroke-width="{max(2, 4*s_):.0f}" opacity=".8"/>')
    s += (f'<path d="M{x-w_*.20:.0f},{y+hh*.30:.0f} q{w_*.20:.0f},{hh*.14:.0f}'
          f' {w_*.40:.0f},0" fill="none" stroke="#f3e0c4"'
          f' stroke-width="{max(2, 5*s_):.0f}" opacity=".5"/>')
    return s + '</g>'


def _shapka_meh(x, y, s_=1.0, t=0.0, ph=.0, razdvinut=0.0):
    """Шапка-ушанка: меховой купол, толстый светлый околыш и два широких уха,
    прижатых к бокам (не палки в стороны — поправлено по осмотру)."""
    w_, hh = 150 * s_, 86 * s_
    s = ten(x, y + 16 * s_, w_ * .62, 14 * s_, .42)
    for i in (-1, 1):                    # уши-лопасти прижаты к бокам купола
        ug = i * (4 + 3 * A.w(t, 2.6, ph + (0 if i < 0 else .3)))
        s += (f'<g transform="rotate({ug:.1f} {x+i*w_*.40:.0f} {y-hh*.30:.0f})">'
              f'<path d="M{x+i*w_*.30:.0f},{y-hh*.56:.0f}'
              f' q{i*w_*.30:.0f},{hh*.06:.0f} {i*w_*.32:.0f},{hh*.52:.0f}'
              f' q{i*w_*.01:.0f},{hh*.52:.0f} {-i*w_*.14:.0f},{hh*.54:.0f}'
              f' q{-i*w_*.18:.0f},{-hh*.14:.0f} {-i*w_*.18:.0f},{-hh*1.06:.0f} Z"'
              f' fill="#c2a078" {o(max(3, 5*s_))}/>')
        for j in range(4):
            s += (f'<path d="M{x+i*w_*(.26+j*.015):.0f},{y-hh*.16+j*hh*.26:.0f}'
                  f' l{i*16*s_:.0f},{4*s_:.0f}" stroke="#e0c49a"'
                  f' stroke-width="{max(3, 7*s_):.0f}" stroke-linecap="round"'
                  f' opacity=".85"/>')
        s += '</g>'
    s += (f'<path d="M{x-w_*.52:.0f},{y-hh*.20:.0f}'
          f' q{w_*.02:.0f},{-hh*1.16:.0f} {w_*.52:.0f},{-hh*1.16:.0f}'
          f' q{w_*.50:.0f},0 {w_*.52:.0f},{hh*1.16:.0f} Z" fill="#6b5236"'
          f' {o(max(4, 6*s_))}/>')
    for i in range(11):                  # мех на куполе
        a = -3.0 + i * .30
        s += (f'<path d="M{x+math.cos(a)*w_*.47:.0f},'
              f'{y-hh*.20+math.sin(a)*hh*1.02:.0f}'
              f' l{math.cos(a)*18*s_:.0f},{math.sin(a)*18*s_:.0f}"'
              f' stroke="#8f6f48" stroke-width="{max(3, 9*s_):.0f}"'
              f' stroke-linecap="round" opacity=".9"/>')
    if razdvinut > .02:                  # мех раздвинут пробором на просвет
        s += (f'<path d="M{x-w_*.07:.0f},{y-hh*.26:.0f}'
              f' q{w_*.04:.0f},{-hh*.54:.0f} {w_*.01:.0f},{-hh*1.02:.0f}'
              f' l{w_*.18*razdvinut:.0f},0 q{w_*.03:.0f},{hh*.48:.0f}'
              f' {w_*.04:.0f},{hh*1.02:.0f} Z" fill="#fff0cc"'
              f' opacity="{.92*razdvinut:.2f}" {o(max(2, 3*s_))}/>')
    s += (f'<path d="M{x-w_*.58:.0f},{y-hh*.26:.0f}'
          f' q{w_*.58:.0f},{hh*.24:.0f} {w_*1.16:.0f},0'
          f' l0,{hh*.48:.0f} q{-w_*.58:.0f},{hh*.28:.0f} {-w_*1.16:.0f},0 Z"'
          f' fill="#d8b98a" {o(max(4, 6*s_))}/>')
    for i in range(9):
        xx = x - w_ * .50 + i * w_ * .125
        s += (f'<path d="M{xx:.0f},{y-hh*.20:.0f} q{6*s_:.0f},{hh*.28:.0f}'
              f' {-2*s_:.0f},{hh*.48:.0f}" fill="none" stroke="#f0d9b4"'
              f' stroke-width="{max(3, 8*s_):.0f}" opacity=".75"/>')
    s += (f'<ellipse cx="{x-w_*.20:.0f}" cy="{y-hh*.94:.0f}" rx="{w_*.16:.0f}"'
          f' ry="{hh*.14:.0f}" fill="#b08f62" opacity=".45"/>')
    return s


def _tulup_vis(x, y, w_, h_, t, ph=.0, udar=0.0):
    """Овчинный тулуп на гвозде или верёвке: ШИРОКИЙ меховой воротник, светлая
    опушка по борту, обшлагам и подолу, рукава висят по бокам. Без опушки он
    читался мешком — поправлено по осмотру."""
    ug = 2.4 * A.w(t, 2.2, ph) + 7 * udar
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    for i in (-1, 1):                    # рукава СНАЧАЛА — они за полой
        ru = i * (3.0 + 2.4 * A.w(t, 1.8, ph + .2)) + 9 * udar * i
        s += (f'<g transform="rotate({ru:.2f} {x+i*w_*.46:.0f} {y+h_*.16:.0f})">'
              f'<path d="M{x+i*w_*.40:.0f},{y+h_*.12:.0f}'
              f' q{i*w_*.30:.0f},{h_*.06:.0f} {i*w_*.30:.0f},{h_*.50:.0f}'
              f' q{-i*w_*.14:.0f},{h_*.10:.0f} {-i*w_*.30:.0f},{-h_*.04:.0f} Z"'
              f' fill="#b4915f" {o(7)}/>'
              f'<path d="M{x+i*w_*.42:.0f},{y+h_*.60:.0f}'
              f' q{i*w_*.14:.0f},{h_*.08:.0f} {i*w_*.26:.0f},{-h_*.02:.0f}'
              f' l0,{-h_*.08:.0f} q{-i*w_*.12:.0f},{h_*.06:.0f}'
              f' {-i*w_*.26:.0f},{-h_*.01:.0f} Z" fill="#f2ead6" {o(4)}/></g>')
    # пола тулупа
    s += (f'<path d="M{x-w_*.5:.0f},{y+h_*.14:.0f} q{w_*.16:.0f},{-h_*.16:.0f}'
          f' {w_*.5:.0f},{-h_*.14:.0f} q{w_*.34:.0f},{-h_*.02:.0f} {w_*.5:.0f},{h_*.14:.0f}'
          f' L{x+w_*.62:.0f},{y+h_:.0f} q{-w_*.62:.0f},{h_*.07:.0f} {-w_*1.24:.0f},0 Z"'
          f' fill="#b4915f" {o(9)}/>')
    # борт с опушкой наискось — главный признак тулупа
    s += (f'<path d="M{x+w_*.04:.0f},{y+h_*.10:.0f} L{x+w_*.18:.0f},{y+h_*.98:.0f}'
          f' l{-w_*.16:.0f},0 L{x-w_*.10:.0f},{y+h_*.12:.0f} Z" fill="#f2ead6"'
          f' {o(5)}/>')
    for i in range(4):                   # деревянные пуговицы по борту
        s += (f'<circle cx="{x+w_*(.07+i*.03):.0f}" cy="{y+h_*(.26+i*.19):.0f}"'
              f' r="{h_*.022:.0f}" fill="#5e4428" {o(3)}/>')
    # меховой воротник шалькой
    s += (f'<path d="M{x-w_*.34:.0f},{y+h_*.04:.0f} q{w_*.34:.0f},{-h_*.14:.0f}'
          f' {w_*.68:.0f},0 q{-w_*.06:.0f},{h_*.20:.0f} {-w_*.22:.0f},{h_*.22:.0f}'
          f' q{-w_*.14:.0f},{-h_*.12:.0f} {-w_*.24:.0f},{-h_*.02:.0f}'
          f' q{-w_*.12:.0f},{-h_*.10:.0f} {-w_*.22:.0f},{-h_*.20:.0f} Z"'
          f' fill="#f6efdd" {o(6)}/>')
    for i in range(7):                   # клочья меха по воротнику
        s += (f'<path d="M{x-w_*.28+i*w_*.09:.0f},{y+h_*.02:.0f}'
              f' l{4:.0f},{h_*.05:.0f}" stroke="#d8cbb0" stroke-width="7"'
              f' opacity=".8"/>')
    # опушка подола
    s += (f'<path d="M{x-w_*.58:.0f},{y+h_*.90:.0f} q{w_*.58:.0f},{h_*.12:.0f}'
          f' {w_*1.18:.0f},0 l0,{h_*.08:.0f} q{-w_*.60:.0f},{h_*.08:.0f}'
          f' {-w_*1.18:.0f},0 Z" fill="#f2ead6" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.02:.0f}" rx="{w_*.05:.0f}"'
          f' ry="{h_*.016:.0f}" fill="#8d949b" {o(3)}/>')
    return s + '</g>'


def _batareya(x, y, w_, h_, t, n=9):
    """Чугунная батарея: гармошка секций, подводка с вентилем, тёплый воздух."""
    s = (f'<rect x="{x-16:.0f}" y="{y:.0f}" width="{w_+32:.0f}" height="{h_:.0f}"'
         f' rx="14" fill="#b9bdc2" opacity=".35"/>')
    for i in range(n):
        sx = x + i * (w_ / n)
        s += (f'<rect x="{sx:.0f}" y="{y:.0f}" width="{w_/n*.72:.0f}" height="{h_:.0f}"'
              f' rx="{w_/n*.34:.0f}" fill="url(#zhel)" {o(5)}/>')
        s += (f'<rect x="{sx+w_/n*.16:.0f}" y="{y+10:.0f}" width="{w_/n*.16:.0f}"'
              f' height="{h_-20:.0f}" rx="8" fill="#cfd6dc" opacity=".45"/>')
    s += (f'<rect x="{x-20:.0f}" y="{y+h_*.16:.0f}" width="{w_+40:.0f}" height="16"'
          f' rx="8" fill="#8d949b" {o(4)}/>')
    s += (f'<rect x="{x-20:.0f}" y="{y+h_*.74:.0f}" width="{w_+40:.0f}" height="16"'
          f' rx="8" fill="#8d949b" {o(4)}/>')
    s += (f'<rect x="{x+w_+20:.0f}" y="{y-40:.0f}" width="20" height="{h_+80:.0f}"'
          f' rx="10" fill="#9aa1a8" {o(4)}/>')
    s += (f'<circle cx="{x+w_+30:.0f}" cy="{y-46:.0f}" r="26" fill="url(#zhel)" {o(5)}/>')
    s += (f'<circle cx="{x+w_+30:.0f}" cy="{y-46:.0f}" r="10" fill="#6e757c"/>')
    for i in range(4):                   # тёплый воздух дрожит над секциями
        k = ((t * .4) + i * .25) % 1.0
        s += (f'<path d="M{x+w_*(.12+i*.24):.0f},{y-10-k*110:.0f} q22,-26 0,-52"'
              f' fill="none" stroke="#ffd9a0" stroke-width="7"'
              f' opacity="{.34*(1-k):.2f}"/>')
    return s


def _chaynik(x, y, s_=1.0, t=0.0, svistok=True, col="url(#zhel)"):
    """Пузатый чайник: округлый бок, гнутый носик, дуга ручки, шишечка."""
    w_, hh = 150 * s_, 130 * s_
    s = ten(x, y + 10 * s_, w_ * .72, 14 * s_, .45)
    s += (f'<path d="M{x-w_*.46:.0f},{y:.0f} q{-w_*.22:.0f},{-hh*.52:.0f} {w_*.06:.0f},{-hh*.84:.0f}'
          f' q{w_*.40:.0f},{-hh*.22:.0f} {w_*.80:.0f},0 q{w_*.28:.0f},{hh*.32:.0f}'
          f' {w_*.06:.0f},{hh*.84:.0f} Z" fill="{col}" {o(max(4, 7*s_))}/>')
    s += (f'<path d="M{x-w_*.30:.0f},{y-hh*.60:.0f} q{w_*.10:.0f},{hh*.30:.0f}'
          f' {-w_*.02:.0f},{hh*.52:.0f}" fill="none" stroke="#e8f1f8"'
          f' stroke-width="{max(4, 12*s_):.0f}"'
          f' opacity="{.22+.2*abs(A.w(t,2.8)):.2f}"/>')
    s += (f'<path d="M{x+w_*.40:.0f},{y-hh*.56:.0f} q{w_*.44:.0f},{-hh*.06:.0f}'
          f' {w_*.46:.0f},{-hh*.40:.0f} l{w_*.14:.0f},{hh*.10:.0f}'
          f' q{-w_*.08:.0f},{hh*.44:.0f} {-w_*.52:.0f},{hh*.44:.0f} Z"'
          f' fill="{col}" {o(max(3, 6*s_))}/>')
    s += (f'<path d="M{x-w_*.22:.0f},{y-hh*.88:.0f} q{w_*.22:.0f},{-hh*.56:.0f}'
          f' {w_*.44:.0f},0" fill="none" stroke="#4a4f55"'
          f' stroke-width="{max(5, 16*s_):.0f}" stroke-linecap="round"/>')
    s += (f'<ellipse cx="{x+w_*.04:.0f}" cy="{y-hh*.86:.0f}" rx="{w_*.30:.0f}"'
          f' ry="{hh*.10:.0f}" fill="#8d949b" {o(max(3, 5*s_))}/>')
    if svistok:
        s += (f'<ellipse cx="{x+w_*.86:.0f}" cy="{y-hh*.96:.0f}" rx="{15*s_:.0f}"'
              f' ry="{18*s_:.0f}" fill="{KRAS}" {o(max(2, 4*s_))}/>')
    s += (f'<circle cx="{x+w_*.04:.0f}" cy="{y-hh*.98:.0f}" r="{13*s_:.0f}"'
          f' fill="#2f3337" {o(max(2, 4*s_))}/>')
    return s


def _chashka(x, y, s_=1.0, t=0.0, ph=.0, col=KREM, blyudce=True):
    """Чашка с блюдцем: бочок, ушко, чай внутри, пар над краем."""
    w_, hh = 62 * s_, 58 * s_
    s = ""
    if blyudce:
        s += (f'<ellipse cx="{x:.0f}" cy="{y+6*s_:.0f}" rx="{w_*.96:.0f}"'
              f' ry="{13*s_:.0f}" fill="{col}" {o(max(2, 4*s_))}/>')
    s += (f'<path d="M{x-w_*.5:.0f},{y-hh:.0f} h{w_:.0f} l{-w_*.09:.0f},{hh:.0f}'
          f' q{-w_*.32:.0f},{12*s_:.0f} {-w_*.82:.0f},0 Z" fill="{col}"'
          f' {o(max(2, 5*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*.5:.0f}" ry="{10*s_:.0f}"'
          f' fill="#6b4a2a" {o(max(2, 3*s_))}/>')
    s += (f'<ellipse cx="{x-w_*.14:.0f}" cy="{y-hh:.0f}" rx="{w_*.16:.0f}"'
          f' ry="{4*s_:.0f}" fill="#d8b98a"'
          f' opacity="{.35+.3*abs(A.w(t,1.7,ph)):.2f}"/>')
    s += (f'<path d="M{x+w_*.44:.0f},{y-hh*.78:.0f} q{w_*.40:.0f},{hh*.22:.0f}'
          f' {-w_*.06:.0f},{hh*.52:.0f}" fill="none" stroke="{col}"'
          f' stroke-width="{max(3, 9*s_):.0f}"/>')
    s += (f'<path d="M{x+w_*.44:.0f},{y-hh*.78:.0f} q{w_*.40:.0f},{hh*.22:.0f}'
          f' {-w_*.06:.0f},{hh*.52:.0f}" fill="none" stroke="{K}" stroke-width="3"/>')
    return s


def _vaza(x, y, s_=1.0, t=0.0, voda=True):
    """Стеклянная ваза: ровное цилиндрическое тулово с лёгкой талией и широким
    устьем, видно насквозь. Пузатая колба с синей заливкой читалась ретортой."""
    w_, hh = 118 * s_, 300 * s_
    s = ten(x, y + 8 * s_, w_ * .58, 13 * s_, .45)
    s += (f'<path d="M{x-w_*.44:.0f},{y-hh:.0f}'
          f' q{-w_*.04:.0f},{hh*.34:.0f} {w_*.02:.0f},{hh*.52:.0f}'
          f' q{w_*.04:.0f},{hh*.36:.0f} {w_*.40:.0f},{hh*.48:.0f}'
          f' q{w_*.40:.0f},{-hh*.12:.0f} {w_*.44:.0f},{-hh*.48:.0f}'
          f' q{w_*.06:.0f},{-hh*.18:.0f} {w_*.02:.0f},{-hh*.52:.0f} Z"'
          f' fill="url(#stekl)" opacity=".62" {o(max(4, 6*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*.44:.0f}"'
          f' ry="{13*s_:.0f}" fill="#dff0fa" {o(max(3, 5*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh+5*s_:.0f}" rx="{w_*.34:.0f}"'
          f' ry="{9*s_:.0f}" fill="#8fb8ce" opacity=".55"/>')
    if voda:
        s += (f'<path d="M{x-w_*.42:.0f},{y-hh*.42:.0f}'
              f' q{w_*.42:.0f},{hh*.05:.0f} {w_*.84:.0f},0'
              f' q{-w_*.02:.0f},{hh*.30:.0f} {-w_*.42:.0f},{hh*.34:.0f}'
              f' q{-w_*.40:.0f},{-hh*.04:.0f} {-w_*.42:.0f},{-hh*.34:.0f} Z"'
              f' fill="#8fc4d2" opacity=".40"/>')
        s += (f'<path d="M{x-w_*.41:.0f},{y-hh*.42+4*A.w(t,1.9):.0f}'
              f' q{w_*.41:.0f},{hh*.04:.0f} {w_*.82:.0f},0" fill="none"'
              f' stroke="#cfeaf6" stroke-width="{max(4, 8*s_):.0f}" opacity=".8"/>')
    s += (f'<path d="M{x-w_*.30:.0f},{y-hh*.84:.0f} q{-w_*.05:.0f},{hh*.30:.0f}'
          f' {w_*.01:.0f},{hh*.56:.0f}" fill="none" stroke="#ffffff"'
          f' stroke-width="{max(5, 12*s_):.0f}"'
          f' opacity="{.30+.14*abs(A.w(t,2.6)):.2f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-2*s_:.0f}" rx="{w_*.40:.0f}"'
          f' ry="{11*s_:.0f}" fill="#b9d6e8" opacity=".55" {o(max(3, 4*s_))}/>')
    return s


def _svetec(x, y, h_, t, s_=1.0, koryto=True):
    """Светец: КОВАНАЯ стойка — тренога внизу, витой стержень с кольцами, на
    макушке железная развилка-зажим, в неё косо вставлена длинная щепка-лучина.
    Корытце с водой МАЛЕНЬКОЕ и висит на стержне под лучиной. Прежняя версия
    читалась деревцем с тазом — поправлено по осмотру."""
    s = ten(x, y + 10, 100 * s_, 18 * s_, .5)
    # тренога: три кованые лапы с завитками
    for i, sg in ((0, -1), (1, 0), (2, 1)):
        s += (f'<path d="M{x+sg*8*s_:.0f},{y-70*s_:.0f}'
              f' q{sg*40*s_:.0f},{40*s_:.0f} {sg*92*s_:.0f},{66*s_:.0f}'
              f' q{sg*22*s_:.0f},{6*s_:.0f} {sg*8*s_:.0f},{10*s_:.0f}"'
              f' fill="none" stroke="#6b7278" stroke-width="{17*s_:.0f}"'
              f' stroke-linecap="round"/>')
        s += (f'<circle cx="{x+sg*100*s_:.0f}" cy="{y-2*s_:.0f}" r="{11*s_:.0f}"'
              f' fill="#8d949b" {o(max(2, 3*s_))}/>')
    # витой стержень: чередование утолщений даёт ковку, а не ствол
    s += (f'<rect x="{x-11*s_:.0f}" y="{y-h_:.0f}" width="{22*s_:.0f}"'
          f' height="{h_-60*s_:.0f}" rx="{10*s_:.0f}" fill="#7d848c"'
          f' {o(max(3, 5*s_))}/>')
    n = max(4, int((h_ - 120 * s_) / (54 * s_)))
    for i in range(n):
        yy = y - 80 * s_ - i * (h_ - 150 * s_) / n
        s += (f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{20*s_:.0f}"'
              f' ry="{9*s_:.0f}" fill="#9aa1a8" {o(max(2, 3*s_))}/>')
        bl = .25 + .45 * (0.5 + 0.5 * A.w(t, 1.9, i * .14))
        s += (f'<path d="M{x-14*s_:.0f},{yy-4*s_:.0f} q{14*s_:.0f},{-10*s_:.0f}'
              f' {28*s_:.0f},0" fill="none" stroke="#eaf2f8"'
              f' stroke-width="{5*s_:.0f}" opacity="{bl:.2f}"/>')
    # развилка-зажим на макушке: два кованых рога и поперечина
    sj = 3 * s_ * A.ease(A.seg(t, 1.4, .6))
    s += (f'<rect x="{x-30*s_:.0f}" y="{y-h_-18*s_:.0f}" width="{60*s_:.0f}"'
          f' height="{20*s_:.0f}" rx="{8*s_:.0f}" fill="#6b7278"'
          f' {o(max(2, 4*s_))}/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*(24*s_-sj):.0f},{y-h_-14*s_:.0f}'
              f' q{i*10*s_:.0f},{-34*s_:.0f} {i*2*s_:.0f},{-62*s_:.0f}"'
              f' fill="none" stroke="#7d848c" stroke-width="{13*s_:.0f}"'
              f' stroke-linecap="round"/>')
        s += (f'<circle cx="{x+i*(26*s_-sj):.0f}" cy="{y-h_-76*s_:.0f}"'
              f' r="{8*s_:.0f}" fill="#9aa1a8"/>')
    if koryto:                           # корытце висит на стержне, небольшое
        ky_ = y - 150 * s_
        s += (f'<path d="M{x-26*s_:.0f},{ky_-34*s_:.0f} h{52*s_:.0f}"'
              f' stroke="#6b7278" stroke-width="{7*s_:.0f}"/>')
        s += (f'<path d="M{x-62*s_:.0f},{ky_:.0f} h{124*s_:.0f}'
              f' l{-16*s_:.0f},{34*s_:.0f} h{-92*s_:.0f} Z" fill="url(#chug)"'
              f' {o(max(3, 5*s_))}/>')
        s += (f'<path d="M{x-50*s_:.0f},{ky_+8*s_:.0f} h{100*s_:.0f}'
              f' l{-10*s_:.0f},{18*s_:.0f} h{-80*s_:.0f} Z" fill="url(#voda)"'
              f' opacity=".9"/>')
        s += (f'<ellipse cx="{x-14*s_:.0f}" cy="{ky_+14*s_:.0f}" rx="{20*s_:.0f}"'
              f' ry="{5*s_:.0f}" fill="#bfe6f2"'
              f' opacity="{.3+.4*abs(A.w(t,1.6,.2)):.2f}"/>')
    return s


def _luchina_v_razvilke(x, y, t, s_=1.0, gorit=1.0, ph=.0):
    """Длинная щепка-лучина, косо вставленная в развилку: сама щепка с волокном,
    на верхнем конце огонёк, под ней уголёк. Рисуется поверх `_svetec`."""
    dl = 230 * s_
    ax, ay = x + dl * .42, y - dl * .86
    s = (f'<path d="M{x-10*s_:.0f},{y+34*s_:.0f} L{ax:.0f},{ay:.0f}'
         f' l{14*s_:.0f},{10*s_:.0f} L{x+6*s_:.0f},{y+40*s_:.0f} Z"'
         f' fill="url(#derev)" {o(max(3, 5*s_))}/>')
    s += (f'<path d="M{x-4*s_:.0f},{y+28*s_:.0f} L{ax+4*s_:.0f},{ay+6*s_:.0f}"'
          f' stroke="#c9a771" stroke-width="{4*s_:.0f}" opacity=".6"/>')
    if gorit > .02:
        s += ogon(ax + 8 * s_, ay - 6 * s_, t, .62 * s_ * gorit + .1, ph, 6)
        s += teplo(ax, ay, 320 * s_ * gorit + 90, 280 * s_ * gorit + 80,
                   .5 * gorit + .1)
    return s


def _mysh(x, y, s_=1.0, t=0.0, ph=.0, platok=True, hvost=1):
    """Мышь в платочке: капля тела, круглые уши, бусина глаза, длинный хвост."""
    w_ = 54 * s_
    sh = 3 * s_ * A.w(t, .9, ph)
    s = f'<g transform="translate({sh:.1f},0)">'
    s += ten(x, y + 5 * s_, w_ * .7, 7 * s_, .4)
    s += (f'<path d="M{x-w_*.9:.0f},{y:.0f} q{-w_*.12:.0f},{-w_*.56:.0f} {w_*.44:.0f},{-w_*.70:.0f}'
          f' q{w_*.78:.0f},{-w_*.12:.0f} {w_*1.24:.0f},{w_*.30:.0f}'
          f' q{w_*.24:.0f},{w_*.26:.0f} {-w_*.06:.0f},{w_*.40:.0f} Z"'
          f' fill="#8f8880" {o(max(2, 4*s_))}/>')
    s += (f'<ellipse cx="{x-w_*.56:.0f}" cy="{y-w_*.60:.0f}" rx="{w_*.28:.0f}"'
          f' ry="{w_*.30:.0f}" fill="#a39b92" {o(max(2, 3*s_))}/>')
    s += (f'<ellipse cx="{x+w_*.56:.0f}" cy="{y-w_*.34:.0f}" rx="{w_*.26:.0f}"'
          f' ry="{w_*.22:.0f}" fill="#f0cfae" opacity=".5"/>')
    if not A.blink(t, 3.2, ph):
        s += (f'<circle cx="{x+w_*.62:.0f}" cy="{y-w_*.40:.0f}" r="{w_*.09:.0f}"'
              f' fill="{K}"/>')
    s += (f'<circle cx="{x+w_*.94:.0f}" cy="{y-w_*.22:.0f}" r="{w_*.07:.0f}"'
          f' fill="#c97f72"/>')
    if platok:
        s += (f'<path d="M{x+w_*.22:.0f},{y-w_*.62:.0f} q{w_*.34:.0f},{-w_*.34:.0f}'
              f' {w_*.66:.0f},{-w_*.06:.0f} q{-w_*.20:.0f},{w_*.22:.0f}'
              f' {-w_*.66:.0f},{w_*.06:.0f} Z" fill="{TKAN}" {o(max(2, 3*s_))}/>')
    hv = 16 * s_ * A.w(t, 1.1, ph + .3)
    s += (f'<path d="M{x-w_*.86:.0f},{y-w_*.10:.0f} q{-w_*.70:.0f},{hvost*w_*.20:.0f}'
          f' {-w_*1.10:.0f},{hv:.0f}" fill="none" stroke="#7d766e"'
          f' stroke-width="{max(2, 6*s_):.0f}" stroke-linecap="round"/>')
    for i in (-1, 1):                    # лапки переступают
        st = 7 * s_ * A.w(t, .7, ph + (0 if i < 0 else .45))
        s += (f'<path d="M{x+i*w_*.34:.0f},{y-w_*.04:.0f} l{st:.0f},{w_*.18:.0f}"'
              f' stroke="#7d766e" stroke-width="{max(2, 5*s_):.0f}"'
              f' stroke-linecap="round"/>')
    return s + '</g>'


def _golub(x, y, s_=1.0, t=0.0, ph=.0, letit=0.0):
    """Голубь: сизое тело, белая оторочка крыла, лапки. В полёте крылья бьют."""
    w_ = 62 * s_
    vz = letit * 160
    s = f'<g transform="translate({letit*110:.0f},{-vz:.0f})">'
    if letit < .05:
        s += ten(x, y + 6 * s_, w_ * .6, 7 * s_, .35)
    s += (f'<ellipse cx="{x:.0f}" cy="{y-w_*.42:.0f}" rx="{w_*.64:.0f}"'
          f' ry="{w_*.40:.0f}" fill="#6a7684" {o(max(2, 4*s_))}/>')
    s += (f'<circle cx="{x+w_*.56:.0f}" cy="{y-w_*.76:.0f}" r="{w_*.25:.0f}"'
          f' fill="#7c889a" {o(max(2, 3*s_))}/>')
    s += (f'<path d="M{x+w_*.78:.0f},{y-w_*.78:.0f} l{w_*.26:.0f},{w_*.06:.0f}'
          f' l{-w_*.24:.0f},{w_*.10:.0f} Z" fill="#2f3337"/>')
    if not A.blink(t, 3.0, ph):
        s += (f'<circle cx="{x+w_*.62:.0f}" cy="{y-w_*.82:.0f}" r="{w_*.06:.0f}"'
              f' fill="#f2b03c"/>')
    kr = (-28 if letit > .05 else -4) * (1 + .9 * A.w(t, .36 if letit > .05 else 2.4, ph))
    s += (f'<g transform="rotate({kr:.1f} {x:.0f} {y-w_*.52:.0f})">'
          f'<path d="M{x-w_*.20:.0f},{y-w_*.60:.0f} q{w_*.30:.0f},{-w_*.30:.0f}'
          f' {w_*.74:.0f},{-w_*.08:.0f} q{-w_*.24:.0f},{w_*.34:.0f} {-w_*.74:.0f},{w_*.26:.0f} Z"'
          f' fill="#8b97a6" {o(max(2, 3*s_))}/>'
          f'<path d="M{x-w_*.10:.0f},{y-w_*.56:.0f} q{w_*.28:.0f},{-w_*.10:.0f}'
          f' {w_*.52:.0f},{-w_*.04:.0f}" fill="none" stroke="#e8eef6"'
          f' stroke-width="{max(2, 5*s_):.0f}" opacity=".8"/></g>')
    s += (f'<path d="M{x-w_*.56:.0f},{y-w_*.40:.0f} l{-w_*.46:.0f},{-w_*.14:.0f}'
          f' l{w_*.08:.0f},{w_*.26:.0f} Z" fill="#59636f" {o(max(2, 3*s_))}/>')
    if letit < .05:
        for i in (-1, 1):
            s += (f'<path d="M{x+i*w_*.12:.0f},{y-w_*.06:.0f} l0,{w_*.10:.0f}"'
                  f' stroke="#c97f52" stroke-width="{max(2, 5*s_):.0f}"/>')
    return s + '</g>'


def _pes(x, y, s_=1.0, t=0.0, ph=.0, col="#6b5a46"):
    """Пёс: вытянутое тело, висячее ухо, нос у земли, хвост метёт."""
    w_ = 110 * s_
    nos = 8 * s_ * A.w(t, 1.2, ph)
    s = ten(x, y + 8 * s_, w_ * .66, 12 * s_, .42)
    s += (f'<ellipse cx="{x:.0f}" cy="{y-w_*.40:.0f}" rx="{w_*.58:.0f}"'
          f' ry="{w_*.30:.0f}" fill="{col}" {o(max(3, 5*s_))}/>')
    s += (f'<ellipse cx="{x+w_*.62:.0f}" cy="{y-w_*.42+nos:.0f}" rx="{w_*.26:.0f}"'
          f' ry="{w_*.24:.0f}" fill="{col}" {o(max(3, 4*s_))}/>')
    s += (f'<path d="M{x+w_*.80:.0f},{y-w_*.40+nos:.0f} q{w_*.26:.0f},{w_*.04:.0f}'
          f' {w_*.24:.0f},{w_*.16:.0f} q{-w_*.14:.0f},{w_*.06:.0f} {-w_*.26:.0f},{-w_*.02:.0f} Z"'
          f' fill="{col}" {o(max(2, 3*s_))}/>')
    s += (f'<circle cx="{x+w_*1.04:.0f}" cy="{y-w_*.26+nos:.0f}" r="{w_*.07:.0f}"'
          f' fill="#23201c"/>')
    if not A.blink(t, 3.6, ph):
        s += (f'<circle cx="{x+w_*.68:.0f}" cy="{y-w_*.50+nos:.0f}" r="{w_*.05:.0f}"'
              f' fill="#1c1813"/>')
    s += (f'<path d="M{x+w_*.48:.0f},{y-w_*.60+nos:.0f} q{w_*.16:.0f},{w_*.30:.0f}'
          f' {-w_*.06:.0f},{w_*.40:.0f} q{-w_*.18:.0f},{-w_*.18:.0f} {-w_*.10:.0f},{-w_*.40:.0f} Z"'
          f' fill="#54463a" {o(max(2, 3*s_))}/>')
    hv = 34 * A.w(t, .55, ph)
    s += (f'<path d="M{x-w_*.56:.0f},{y-w_*.52:.0f} q{-w_*.30:.0f},{-w_*.20:.0f}'
          f' {-w_*.24:.0f},{-w_*.52+hv*.01:.0f}" fill="none" stroke="{col}"'
          f' stroke-width="{max(4, 13*s_):.0f}" stroke-linecap="round"'
          f' transform="rotate({hv*.5:.1f} {x-w_*.56:.0f} {y-w_*.52:.0f})"/>')
    for i, sgn in ((0, -1), (1, 1)):
        st = 6 * s_ * A.w(t, .8, ph + i * .4)
        s += (f'<rect x="{x+sgn*w_*.34:.0f}" y="{y-w_*.20:.0f}" width="{w_*.14:.0f}"'
              f' height="{w_*.22:.0f}" rx="{w_*.06:.0f}" fill="{col}"'
              f' transform="rotate({st:.1f} {x+sgn*w_*.34:.0f} {y-w_*.20:.0f})"'
              f' {o(max(2, 3*s_))}/>')
    return s


def _afisha(x, y, w_, h_, t, vid="traktor", seed=5, ug=0.0, otgib=0.0):
    """Афиша: бумага и ОДИН крупный предмет. Букв нет — название даёт
    волнистая полоса под предметом (правило: текст в декорации не рисуем)."""
    rnd = random.Random(seed)
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' rx="6" fill="url(#list)" {o(6)}/>')
    s += (f'<rect x="{x-w_/2+14:.0f}" y="{y-h_/2+14:.0f}" width="{w_-28:.0f}"'
          f' height="{h_-28:.0f}" rx="4" fill="none" stroke="{KRAS}"'
          f' stroke-width="8" opacity=".7"/>')
    cx, cy = x, y - h_ * .10
    if vid == "traktor":
        s += (f'<rect x="{cx-w_*.30:.0f}" y="{cy-h_*.10:.0f}" width="{w_*.46:.0f}"'
              f' height="{h_*.20:.0f}" rx="10" fill="{KRAS}" {o(6)}/>')
        s += (f'<rect x="{cx-w_*.06:.0f}" y="{cy-h_*.26:.0f}" width="{w_*.22:.0f}"'
              f' height="{h_*.18:.0f}" rx="8" fill="#b43a22" {o(5)}/>')
        s += (f'<rect x="{cx-w_*.26:.0f}" y="{cy-h_*.26:.0f}" width="{w_*.10:.0f}"'
              f' height="{h_*.14:.0f}" rx="5" fill="#4a4f55" {o(4)}/>')
        kol = (t * 120) % 360
        s += (f'<circle cx="{cx+w_*.14:.0f}" cy="{cy+h_*.14:.0f}" r="{h_*.16:.0f}"'
              f' fill="#2f3337" {o(6)}/>')
        s += (f'<g transform="rotate({kol:.0f} {cx+w_*.14:.0f} {cy+h_*.14:.0f})">')
        for i in range(6):
            a = i * 1.047
            s += (f'<line x1="{cx+w_*.14:.0f}" y1="{cy+h_*.14:.0f}"'
                  f' x2="{cx+w_*.14+math.cos(a)*h_*.14:.0f}"'
                  f' y2="{cy+h_*.14+math.sin(a)*h_*.14:.0f}" stroke="#8d949b"'
                  f' stroke-width="6"/>')
        s += '</g>'
        s += (f'<circle cx="{cx-w_*.22:.0f}" cy="{cy+h_*.18:.0f}" r="{h_*.10:.0f}"'
              f' fill="#2f3337" {o(5)}/>')
        for i in range(5):               # борозда поля
            s += (f'<path d="M{cx-w_*.40+i*w_*.18:.0f},{cy+h_*.30:.0f}'
                  f' q{w_*.06:.0f},{h_*.06:.0f} 0,{h_*.12:.0f}" fill="none"'
                  f' stroke="#7d5636" stroke-width="7" opacity=".8"/>')
    elif vid == "rozhok":
        # длинный изогнутый рог: от узкого мундштука слева к небольшому
        # раструбу справа вверху, лента повязана посередине
        s += (f'<path d="M{cx-w_*.40:.0f},{cy+h_*.16:.0f}'
              f' q{w_*.30:.0f},{h_*.04:.0f} {w_*.56:.0f},{-h_*.18:.0f}'
              f' q{w_*.18:.0f},{-h_*.12:.0f} {w_*.26:.0f},{-h_*.26:.0f}'
              f' l{w_*.05:.0f},{h_*.15:.0f}'
              f' q{-w_*.08:.0f},{h_*.12:.0f} {-w_*.24:.0f},{h_*.24:.0f}'
              f' q{-w_*.26:.0f},{h_*.18:.0f} {-w_*.58:.0f},{h_*.14:.0f} Z"'
              f' fill="#c9a06a" {o(7)}/>')
        s += (f'<path d="M{cx+w_*.40:.0f},{cy-h_*.28:.0f}'
              f' q{w_*.11:.0f},{-h_*.09:.0f} {w_*.16:.0f},{h_*.01:.0f}'
              f' q{w_*.02:.0f},{h_*.11:.0f} {-w_*.11:.0f},{h_*.14:.0f}'
              f' q{-w_*.07:.0f},{-h_*.05:.0f} {-w_*.05:.0f},{-h_*.15:.0f} Z"'
              f' fill="url(#zol)" {o(6)}/>')
        s += (f'<ellipse cx="{cx+w_*.50:.0f}" cy="{cy-h_*.24:.0f}"'
              f' rx="{w_*.045:.0f}" ry="{h_*.055:.0f}" fill="#5e3a16"'
              f' opacity=".9"/>')
        s += (f'<ellipse cx="{cx-w_*.40:.0f}" cy="{cy+h_*.19:.0f}"'
              f' rx="{w_*.035:.0f}" ry="{h_*.035:.0f}" fill="#8d949b"'
              f' {o(4)}/>')
        for i in range(4):               # берестяные обручи по рогу
            s += (f'<path d="M{cx-w_*.24+i*w_*.17:.0f},'
                  f'{cy+h_*.14-i*h_*.055:.0f} l{w_*.02:.0f},{h_*.085:.0f}"'
                  f' stroke="#7d5220" stroke-width="10" opacity=".9"/>')
        lent = 12 * A.w(t, 2.2, seed * .1)
        s += (f'<path d="M{cx-w_*.02:.0f},{cy+h_*.02:.0f}'
              f' q{-w_*.07:.0f},{h_*.05:.0f} {w_*.01:.0f},{h_*.11:.0f}'
              f' q{w_*.08:.0f},{-h_*.04:.0f} {w_*.03:.0f},{-h_*.12:.0f} Z"'
              f' fill="{KRAS}" {o(3)}/>')
        for j in (0, 1):                 # два хвоста ленты
            s += (f'<path d="M{cx:.0f},{cy+h_*.08:.0f}'
                  f' q{-w_*.08+lent*.2:.0f},{h_*.14+j*h_*.05:.0f}'
                  f' {-w_*.16-j*w_*.07:.0f},{h_*.24+j*h_*.07:.0f}'
                  f' l{w_*.08:.0f},{h_*.04:.0f}'
                  f' q{w_*.09:.0f},{-h_*.12:.0f} {w_*.14:.0f},{-h_*.28:.0f} Z"'
                  f' fill="{KRAS}" {o(4)}/>')
        lent = 10 * A.w(t, 2.2, seed * .1)
        s += (f'<path d="M{cx-w_*.24:.0f},{cy+h_*.16:.0f} q{-w_*.18:.0f},{h_*.16+lent:.0f}'
              f' {-w_*.06:.0f},{h_*.34:.0f} q{w_*.14:.0f},{-h_*.12:.0f}'
              f' {w_*.18:.0f},{-h_*.30:.0f} Z" fill="{KRAS}" {o(4)}/>')
    elif vid == "snop":
        # сноп: низ раскинут веером, перевясло посередине, вверху колосья
        for i in range(15):
            a = -1.15 + i * .164
            bx_ = cx + math.sin(a) * w_ * .34
            s += (f'<path d="M{cx+math.sin(a)*w_*.22:.0f},{cy+h_*.30:.0f}'
                  f' Q{cx+math.sin(a)*w_*.06:.0f},{cy+h_*.02:.0f}'
                  f' {bx_:.0f},{cy-h_*.26:.0f}" fill="none"'
                  f' stroke="url(#solom)" stroke-width="{8+(i%3)*3}"'
                  f' stroke-linecap="round"/>')
            for j in (-1, 1):            # зёрна парами по колосу
                s += (f'<ellipse cx="{bx_+j*h_*.022:.0f}"'
                      f' cy="{cy-h_*.30+4*A.w(t,2.4,i*.1):.0f}"'
                      f' rx="{h_*.022:.0f}" ry="{h_*.045:.0f}" fill="#e3c272"'
                      f' {o(2)}/>')
                s += (f'<ellipse cx="{bx_+j*h_*.020:.0f}"'
                      f' cy="{cy-h_*.38+4*A.w(t,2.4,i*.1+.2):.0f}"'
                      f' rx="{h_*.020:.0f}" ry="{h_*.040:.0f}" fill="#d8b96a"'
                      f' {o(2)}/>')
        s += (f'<path d="M{cx-w_*.20:.0f},{cy+h_*.02:.0f} q{w_*.20:.0f},{h_*.10:.0f}'
              f' {w_*.40:.0f},0 l0,{h_*.07:.0f} q{-w_*.20:.0f},{h_*.10:.0f}'
              f' {-w_*.40:.0f},0 Z" fill="{KRAS}" {o(4)}/>')
    elif vid == "parovoz":
        s += (f'<rect x="{cx-w_*.30:.0f}" y="{cy-h_*.04:.0f}" width="{w_*.56:.0f}"'
              f' height="{h_*.20:.0f}" rx="{h_*.09:.0f}" fill="#2f3337" {o(6)}/>')
        s += (f'<rect x="{cx-w_*.34:.0f}" y="{cy-h_*.22:.0f}" width="{w_*.16:.0f}"'
              f' height="{h_*.20:.0f}" rx="6" fill="#3f454a" {o(5)}/>')
        s += (f'<rect x="{cx+w_*.04:.0f}" y="{cy-h_*.24:.0f}" width="{w_*.10:.0f}"'
              f' height="{h_*.22:.0f}" rx="4" fill="#4a4f55" {o(4)}/>')
        for i in range(2):
            s += (f'<circle cx="{cx-w_*.18+i*w_*.34:.0f}" cy="{cy+h_*.20:.0f}"'
                  f' r="{h_*.09:.0f}" fill="#23262a" {o(5)}/>')
        for i in range(5):               # клубы пара на афише живут
            k = ((t * .34) + i * .2) % 1.0
            s += (f'<circle cx="{cx+w_*.10+k*w_*.26:.0f}" cy="{cy-h_*.28-k*h_*.22:.0f}"'
                  f' r="{h_*(.05+.08*k):.0f}" fill="#e8eef6"'
                  f' opacity="{.7*(1-k):.2f}"/>')
        s += (f'<path d="M{cx-w_*.34:.0f},{cy+h_*.30:.0f} h{w_*.68:.0f}"'
              f' stroke="#6b645c" stroke-width="8"/>')
    elif vid == "shlyapka":
        s += (f'<ellipse cx="{cx:.0f}" cy="{cy+h_*.02:.0f}" rx="{w_*.30:.0f}"'
              f' ry="{h_*.07:.0f}" fill="#2b2a30" {o(6)}/>')
        s += (f'<path d="M{cx-w_*.17:.0f},{cy:.0f} q{w_*.17:.0f},{-h_*.26:.0f}'
              f' {w_*.34:.0f},0 Z" fill="#3a3842" {o(5)}/>')
        s += (f'<path d="M{cx-w_*.16:.0f},{cy-h_*.10:.0f} q{w_*.18:.0f},{-h_*.10:.0f}'
              f' {w_*.34:.0f},{h_*.02:.0f}" fill="none" stroke="{TKAN}"'
              f' stroke-width="10"/>')
        for i in range(7):               # вуаль сеточкой
            vv = 4 * A.w(t, 2.6, i * .12)
            s += (f'<path d="M{cx-w_*.26+i*w_*.09:.0f},{cy+h_*.02:.0f}'
                  f' q{vv:.0f},{h_*.10:.0f} {vv*.4:.0f},{h_*.22:.0f}" fill="none"'
                  f' stroke="#2b2a30" stroke-width="4" opacity=".65"/>')
        s += (f'<path d="M{cx-w_*.26:.0f},{cy+h_*.14:.0f} q{w_*.26:.0f},{h_*.08:.0f}'
              f' {w_*.52:.0f},0" fill="none" stroke="#2b2a30" stroke-width="4"'
              f' opacity=".6"/>')
    else:                                # меч в зелёном холме
        s += (f'<path d="M{cx-w_*.42:.0f},{cy+h_*.30:.0f} q{w_*.42:.0f},{-h_*.26:.0f}'
              f' {w_*.84:.0f},0 Z" fill="{ZEL2}" {o(6)}/>')
        s += f'<g transform="rotate(18 {cx:.0f} {cy+h_*.16:.0f})">'
        s += (f'<rect x="{cx-w_*.105:.0f}" y="{cy-h_*.30:.0f}"'
              f' width="{w_*.21:.0f}" height="{h_*.46:.0f}" fill="#dfe8ef"'
              f' {o(7)}/>')
        s += (f'<line x1="{cx:.0f}" y1="{cy-h_*.28:.0f}" x2="{cx:.0f}"'
              f' y2="{cy+h_*.12:.0f}" stroke="#aebfc9" stroke-width="7"/>')
        s += (f'<path d="M{cx-w_*.105:.0f},{cy-h_*.30:.0f} l{w_*.105:.0f},'
              f'{-h_*.14:.0f} l{w_*.105:.0f},{h_*.14:.0f} Z" fill="#f2f8fc"'
              f' {o(6)}/>')
        s += (f'<path d="M{cx-w_*.30:.0f},{cy-h_*.34:.0f}'
              f' q{w_*.30:.0f},{-h_*.09:.0f} {w_*.60:.0f},0'
              f' l{-w_*.05:.0f},{h_*.09:.0f} q{-w_*.25:.0f},{h_*.06:.0f}'
              f' {-w_*.50:.0f},0 Z" fill="url(#zol)" {o(6)}/>')
        s += (f'<rect x="{cx-w_*.075:.0f}" y="{cy-h_*.52:.0f}"'
              f' width="{w_*.15:.0f}" height="{h_*.18:.0f}" rx="7"'
              f' fill="#6b4a2a" {o(6)}/>')
        for i in range(3):               # обмотка рукояти
            s += (f'<line x1="{cx-w_*.075:.0f}" y1="{cy-h_*.48+i*h_*.05:.0f}"'
                  f' x2="{cx+w_*.075:.0f}" y2="{cy-h_*.46+i*h_*.05:.0f}"'
                  f' stroke="#4a3018" stroke-width="5"/>')
        s += (f'<circle cx="{cx:.0f}" cy="{cy-h_*.57:.0f}" r="{w_*.065:.0f}"'
              f' fill="url(#zol)" {o(5)}/>')
        s += '</g>'
        bl = .3 + .5 * (0.5 + 0.5 * A.w(t, 2.0, seed * .2))
        s += (f'<line x1="{cx:.0f}" y1="{cy-h_*.26:.0f}" x2="{cx:.0f}"'
              f' y2="{cy+h_*.10:.0f}" stroke="#ffffff" stroke-width="7"'
              f' opacity="{bl:.2f}"/>')
    for i in range(3):                   # «название» — волна, не буквы
        s += (f'<path d="M{x-w_*.34:.0f},{y+h_*.30+i*h_*.07:.0f}'
              f' q{w_*.17:.0f},{rnd.uniform(-6,6):.0f} {w_*.68:.0f},0" fill="none"'
              f' stroke="#6b645c" stroke-width="{12-i*3}" opacity=".85"/>')
    if otgib > .02:                      # уголок отгибается
        s += (f'<path d="M{x+w_/2:.0f},{y-h_/2:.0f} l{-w_*.16*otgib:.0f},0'
              f' l0,{h_*.16*otgib:.0f} Z" fill="#d3c7a8" {o(3)}/>')
    return s + '</g>'


def _lampochki(x, y, w_, n, t, r=12, col=SVET):
    """Бегущие лампочки по фасаду: волна бежит, часть перегорела."""
    s = ""
    for i in range(n):
        xx = x + i * (w_ / max(1, n - 1))
        f = ((t * .9) + i / n) % 1.0
        yar = .22 + .78 * max(0.0, 1 - abs(f - .5) * 3.2)
        if i % 7 == 5:
            yar *= .25
        s += (f'<circle cx="{xx:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{col}"'
              f' opacity="{yar:.2f}"/>')
        s += (f'<circle cx="{xx:.0f}" cy="{y:.0f}" r="{r*.42:.0f}" fill="#fffaf0"'
              f' opacity="{yar:.2f}"/>')
        s += (f'<circle cx="{xx:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="none" {o(3)}/>')
        if yar > .6:
            s += teplo(xx, y, r * 5, r * 5, .22 * yar)
    return s


def _botinok(x, y, s_=1.0, t=0.0, ph=.0, col="#4a3526", blesk=0.0):
    """Зимний ботинок: толстая подошва, язычок, шнуровка крест-накрест."""
    w_, hh = 150 * s_, 110 * s_
    s = ten(x, y + 6 * s_, w_ * .56, 11 * s_, .42)
    s += (f'<path d="M{x-w_*.42:.0f},{y:.0f} q{-w_*.06:.0f},{-hh*.62:.0f} {w_*.14:.0f},{-hh*.74:.0f}'
          f' q{w_*.26:.0f},{-hh*.08:.0f} {w_*.34:.0f},{hh*.22:.0f}'
          f' q{w_*.10:.0f},{hh*.30:.0f} {w_*.46:.0f},{hh*.40:.0f}'
          f' q{w_*.16:.0f},{hh*.06:.0f} {w_*.08:.0f},{hh*.14:.0f} Z"'
          f' fill="{col}" {o(max(3, 6*s_))}/>')
    s += (f'<path d="M{x-w_*.44:.0f},{y-hh*.02:.0f} q{w_*.46:.0f},{hh*.16:.0f}'
          f' {w_*1.04:.0f},{hh*.02:.0f} q{w_*.06:.0f},{hh*.14:.0f} {-w_*.06:.0f},{hh*.16:.0f}'
          f' q{-w_*.56:.0f},{hh*.08:.0f} {-w_*1.00:.0f},{-hh*.04:.0f} Z"'
          f' fill="#23211e" {o(max(3, 5*s_))}/>')
    for i in range(6):                   # рубчик подошвы
        s += (f'<line x1="{x-w_*.36+i*w_*.17:.0f}" y1="{y+hh*.04:.0f}"'
              f' x2="{x-w_*.36+i*w_*.17:.0f}" y2="{y+hh*.16:.0f}" stroke="#3b3835"'
              f' stroke-width="{max(2, 5*s_):.0f}"/>')
    s += (f'<path d="M{x-w_*.22:.0f},{y-hh*.70:.0f} q{w_*.14:.0f},{hh*.22:.0f}'
          f' {w_*.06:.0f},{hh*.44:.0f} l{-w_*.22:.0f},{-hh*.04:.0f} Z"'
          f' fill="#6b5234" {o(max(2, 4*s_))}/>')
    for i in range(4):                   # шнуровка крест-накрест
        yy = y - hh * .60 + i * hh * .13
        s += (f'<line x1="{x-w_*.26:.0f}" y1="{yy:.0f}" x2="{x-w_*.04:.0f}"'
              f' y2="{yy+hh*.09:.0f}" stroke="#d8cbb0"'
              f' stroke-width="{max(2, 5*s_):.0f}"/>')
        s += (f'<line x1="{x-w_*.04:.0f}" y1="{yy:.0f}" x2="{x-w_*.26:.0f}"'
              f' y2="{yy+hh*.09:.0f}" stroke="#d8cbb0"'
              f' stroke-width="{max(2, 5*s_):.0f}"/>')
    if blesk > .01:                      # наведённый блеск на носке
        s += (f'<ellipse cx="{x+w_*.52:.0f}" cy="{y-hh*.20:.0f}" rx="{w_*.16:.0f}"'
              f' ry="{hh*.10:.0f}" fill="#ffffff"'
              f' opacity="{(.18+.3*abs(A.w(t,1.8,ph)))*blesk:.2f}"/>')
    return s


def _ochki(x, y, s_=1.0, t=0.0, verevka=True):
    """Очки на верёвочке: два ободка, переносица, шнурок за ушами."""
    r = 34 * s_
    bl = .3 + .4 * abs(A.w(t, 2.2))
    s = ""
    for i in (-1, 1):
        s += (f'<circle cx="{x+i*r*1.25:.0f}" cy="{y:.0f}" r="{r:.0f}"'
              f' fill="url(#stekl)" opacity=".55" {o(max(2, 5*s_))}/>')
        s += (f'<path d="M{x+i*r*1.25-r*.5:.0f},{y-r*.4:.0f} q{r*.4:.0f},{-r*.3:.0f}'
              f' {r*.8:.0f},{r*.1:.0f}" fill="none" stroke="#ffffff"'
              f' stroke-width="{max(2, 6*s_):.0f}" opacity="{bl:.2f}"/>')
    s += (f'<path d="M{x-r*.3:.0f},{y-r*.1:.0f} q{r*.3:.0f},{-r*.3:.0f} {r*.6:.0f},0"'
          f' fill="none" stroke="#4a4f55" stroke-width="{max(3, 7*s_):.0f}"/>')
    if verevka:
        for i in (-1, 1):
            s += (f'<path d="M{x+i*r*2.3:.0f},{y:.0f} q{i*r*.9:.0f},{r*.4:.0f}'
                  f' {i*r*1.1:.0f},{r*1.9+6*A.w(t,2.0,i*.2):.0f}" fill="none"'
                  f' stroke="#8d7a5a" stroke-width="{max(2, 5*s_):.0f}"/>')
    return s


def _kinokamera(x, y, s_=1.0, t=0.0, krutit=True, trenoga=True):
    """Деревянная кинокамера на треноге: корпус-ящик, две бобины сверху,
    объектив гармошкой, ручка сбоку крутится."""
    w_, hh = 240 * s_, 170 * s_
    s = ten(x, y + 10 * s_, w_ * .7, 18 * s_, .5)
    if trenoga:
        for i, sgn in ((0, -1), (1, 0), (2, 1)):  # ноги треноги
            s += (f'<path d="M{x+sgn*18*s_:.0f},{y-200*s_:.0f}'
                  f' L{x+sgn*150*s_+(0 if sgn else 20*s_):.0f},{y:.0f}"'
                  f' stroke="url(#derev)" stroke-width="{18*s_:.0f}"'
                  f' stroke-linecap="round"/>')
    s += (f'<rect x="{x-50*s_:.0f}" y="{y-250*s_:.0f}" width="{100*s_:.0f}"'
          f' height="{54*s_:.0f}" rx="{10*s_:.0f}" fill="#4a4f55" {o(5)}/>')
    s += (f'<rect x="{x-w_*.5:.0f}" y="{y-250*s_-hh:.0f}" width="{w_:.0f}"'
          f' height="{hh:.0f}" rx="{12*s_:.0f}" fill="url(#derev)" {o(8)}/>')
    s += (f'<rect x="{x-w_*.42:.0f}" y="{y-250*s_-hh*.86:.0f}" width="{w_*.84:.0f}"'
          f' height="{hh*.64:.0f}" rx="{8*s_:.0f}" fill="none" stroke="#6d4423"'
          f' stroke-width="{7*s_:.0f}"/>')
    # кожаная ручка на крышке: по ней камеру и узнают
    s += (f'<path d="M{x-w_*.14:.0f},{y-250*s_-hh:.0f} q{w_*.14:.0f},{-46*s_:.0f}'
          f' {w_*.28:.0f},0" fill="none" stroke="#4a3526"'
          f' stroke-width="{14*s_:.0f}" stroke-linecap="round"/>')
    for i, sgn in ((0, -1), (1, 1)):     # бобины
        rot = (t * (150 if krutit else 0) + i * 40) % 360
        bx, by = x + sgn * w_ * .26, y - 250 * s_ - hh - 6 * s_
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{56*s_:.0f}" fill="#3f454a" {o(6)}/>')
        s += (f'<g transform="rotate({rot:.0f} {bx:.0f} {by:.0f})">')
        for j in range(4):
            a = j * 1.5708
            s += (f'<line x1="{bx:.0f}" y1="{by:.0f}"'
                  f' x2="{bx+math.cos(a)*50*s_:.0f}" y2="{by+math.sin(a)*50*s_:.0f}"'
                  f' stroke="#8d949b" stroke-width="{8*s_:.0f}"/>')
        s += '</g>'
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{14*s_:.0f}" fill="url(#zhel)"'
              f' {o(3)}/>')
        s += (f'<rect x="{bx-16*s_:.0f}" y="{by+30*s_:.0f}" width="{32*s_:.0f}"'
              f' height="{40*s_:.0f}" rx="{6*s_:.0f}" fill="#2f3337"'
              f' {o(max(2, 3*s_))}/>')
    ox = x + w_ * .5
    s += (f'<rect x="{ox:.0f}" y="{y-250*s_-hh*.66:.0f}" width="{46*s_:.0f}"'
          f' height="{44*s_:.0f}" rx="6" fill="#4a4f55" {o(5)}/>')
    for i in range(5):                   # гармошка объектива, рёбрами
        s += (f'<rect x="{ox+40*s_+i*22*s_:.0f}" y="{y-250*s_-hh*.74+i*4*s_:.0f}"'
              f' width="{18*s_:.0f}" height="{66*s_-i*6*s_:.0f}" rx="5"'
              f' fill="#4a5056" {o(max(2, 4*s_))}/>')
        s += (f'<rect x="{ox+40*s_+i*22*s_:.0f}" y="{y-250*s_-hh*.74+i*4*s_:.0f}"'
              f' width="{18*s_:.0f}" height="{10*s_:.0f}" rx="4" fill="#737b82"'
              f' opacity=".8"/>')
    s += (f'<circle cx="{ox+118*s_:.0f}" cy="{y-250*s_-hh*.46:.0f}" r="{26*s_:.0f}"'
          f' fill="#1d2024" {o(5)}/>')
    s += (f'<circle cx="{ox+112*s_:.0f}" cy="{y-250*s_-hh*.52:.0f}" r="{9*s_:.0f}"'
          f' fill="#cfe4f5" opacity="{.4+.4*abs(A.w(t,2.2)):.2f}"/>')
    rh = (t * 300) % 360 if krutit else 0
    hx_, hy_ = x - w_ * .5 - 30 * s_, y - 250 * s_ - hh * .40
    s += (f'<circle cx="{hx_:.0f}" cy="{hy_:.0f}" r="{20*s_:.0f}" fill="#5d6168"'
          f' {o(max(2, 4*s_))}/>')
    s += (f'<g transform="rotate({rh:.0f} {hx_:.0f} {hy_:.0f})">'
          f'<line x1="{hx_:.0f}" y1="{hy_:.0f}" x2="{hx_:.0f}"'
          f' y2="{hy_+74*s_:.0f}" stroke="#8d949b"'
          f' stroke-width="{14*s_:.0f}" stroke-linecap="round"/>'
          f'<rect x="{hx_-9*s_:.0f}" y="{hy_+66*s_:.0f}" width="{18*s_:.0f}"'
          f' height="{40*s_:.0f}" rx="{9*s_:.0f}" fill="url(#derev)"'
          f' {o(max(2, 3*s_))}/></g>')
    s += (f'<rect x="{x-w_*.5-22*s_:.0f}" y="{y-250*s_-hh*.46:.0f}" width="{18*s_:.0f}"'
          f' height="{18*s_:.0f}" rx="4" fill="#2f3337"/>')
    return s


def _hlopushka(x, y, s_=1.0, t=0.0, shchel=0.0, ug=-12.0):
    """Хлопушка: доска с косыми полосами и откидная планка, которая хлопает."""
    w_, hh = 200 * s_, 130 * s_
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-hh/2:.0f}" width="{w_:.0f}" height="{hh:.0f}"'
          f' rx="{8*s_:.0f}" fill="#2b2a2e" {o(max(3, 6*s_))}/>')
    for i in range(4):                   # поля под запись — пустые полосы
        s += (f'<rect x="{x-w_*.44:.0f}" y="{y-hh*.34+i*hh*.18:.0f}"'
              f' width="{w_*.88:.0f}" height="{hh*.12:.0f}" rx="3" fill="#4b4a50"'
              f' opacity=".75"/>')
    otk = -46 * (1 - shchel)
    s += f'<g transform="rotate({otk:.1f} {x-w_/2:.0f} {y-hh/2:.0f})">'
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-hh/2-34*s_:.0f}" width="{w_:.0f}"'
          f' height="{34*s_:.0f}" rx="{6*s_:.0f}" fill="#1f1e22" {o(max(3, 5*s_))}/>')
    for i in range(7):                   # косые полосы — узнаваемый знак
        xx = x - w_ / 2 + i * (w_ / 7)
        s += (f'<path d="M{xx:.0f},{y-hh/2:.0f} l{w_/14:.0f},{-34*s_:.0f}'
              f' l{w_/14:.0f},0 l{-w_/14:.0f},{34*s_:.0f} Z" fill="#f2efe6"/>')
    s += '</g>'
    if shchel > .9:
        for i in range(5):               # пыль от хлопка
            a = -2.4 + i * .5
            s += (f'<circle cx="{x-w_/2+math.cos(a)*44*s_:.0f}"'
                  f' cy="{y-hh/2+math.sin(a)*44*s_:.0f}" r="{(7+i)*s_:.0f}"'
                  f' fill="#e8eef6" opacity=".4"/>')
    return s + '</g>'


def _loshadka(x, y, s_=1.0, t=0.0, op=1.0):
    """Рисованная лошадка-мечта: ВЫСОКИЕ ноги, глубокая грудь, длинная шея
    дугой вверх и голова с вытянутой мордой. Прежние короткие ножки при
    длинном низком корпусе давали собаку (осмотр 14.11)."""
    w_ = 150 * s_                        # масштабная единица
    kiv = 3.0 * A.w(t, 1.5)
    bx, by = x - w_ * .20, y - w_ * 1.36  # центр корпуса — высоко над землёй
    s = f'<g opacity="{op:.2f}">'
    s += ten(bx, y + w_ * .04, w_ * .60, w_ * .08, .32 * op)
    for i, (lx_, ph_, zad) in enumerate(((-.62, .0, True), (-.44, .3, True),
                                         (.22, .5, False), (.40, .8, False))):
        sh = w_ * .08 * A.w(t, .9, ph_)
        # бедро/плечо
        s += (f'<ellipse cx="{bx+w_*lx_+w_*.07:.0f}" cy="{by+w_*.34:.0f}"'
              f' rx="{w_*.17:.0f}" ry="{w_*.24:.0f}" fill="#7d5f40" {o(5)}/>')
        # голень: длинная, до самой земли
        s += (f'<g transform="rotate({sh*.3:.1f} {bx+w_*lx_+w_*.07:.0f}'
              f' {by+w_*.40:.0f})">'
              f'<rect x="{bx+w_*lx_:.0f}" y="{by+w_*.40:.0f}"'
              f' width="{w_*.14:.0f}" height="{w_*.92:.0f}" rx="{w_*.06:.0f}"'
              f' fill="#7d5f40" {o(5)}/>'
              f'<rect x="{bx+w_*lx_-w_*.02:.0f}" y="{by+w_*1.22:.0f}"'
              f' width="{w_*.18:.0f}" height="{w_*.14:.0f}" rx="{w_*.04:.0f}"'
              f' fill="#4a3526" {o(4)}/></g>')
    hv = 9 * A.w(t, 1.1, .2)             # хвост от крупа
    s += (f'<path d="M{bx-w_*.80:.0f},{by-w_*.22:.0f}'
          f' q{-w_*.34:.0f},{w_*.30:.0f} {-w_*.26:.0f},{w_*.76:.0f}'
          f' l{w_*.18:.0f},{w_*.04:.0f} q{w_*.02:.0f},{-w_*.46:.0f}'
          f' {w_*.26:.0f},{-w_*.70:.0f} Z" fill="#5e4428"'
          f' transform="rotate({hv:.1f} {bx-w_*.80:.0f} {by-w_*.22:.0f})"'
          f' {o(5)}/>')
    # корпус: глубокая грудь спереди, круп сзади, спина с провисанием
    s += (f'<path d="M{bx-w_*.84:.0f},{by-w_*.26:.0f}'
          f' q{w_*.40:.0f},{-w_*.22:.0f} {w_*.84:.0f},{-w_*.10:.0f}'
          f' q{w_*.44:.0f},{w_*.02:.0f} {w_*.78:.0f},{w_*.18:.0f}'
          f' q{w_*.14:.0f},{w_*.40:.0f} {-w_*.10:.0f},{w_*.60:.0f}'
          f' q{-w_*.60:.0f},{w_*.18:.0f} {-w_*1.46:.0f},{w_*.02:.0f}'
          f' q{-w_*.24:.0f},{-w_*.26:.0f} {-w_*.06:.0f},{-w_*.70:.0f} Z"'
          f' fill="#8a6a4a" {o(7)}/>')
    s += (f'<ellipse cx="{bx-w_*.16:.0f}" cy="{by+w_*.18:.0f}" rx="{w_*.50:.0f}"'
          f' ry="{w_*.22:.0f}" fill="#9a7a56" opacity=".5"/>')
    # шея дугой ВВЕРХ и голова с длинной мордой — кивают как одно целое
    s += f'<g transform="rotate({kiv:.1f} {bx+w_*.62:.0f} {by-w_*.24:.0f})">'
    s += (f'<path d="M{bx+w_*.46:.0f},{by-w_*.34:.0f}'
          f' q{w_*.26:.0f},{-w_*.42:.0f} {w_*.56:.0f},{-w_*.70:.0f}'
          f' l{w_*.34:.0f},{w_*.22:.0f}'
          f' q{-w_*.22:.0f},{w_*.46:.0f} {-w_*.40:.0f},{w_*.68:.0f} Z"'
          f' fill="#8a6a4a" {o(6)}/>')
    hx_, hy_ = bx + w_ * 1.10, by - w_ * 1.04
    s += (f'<path d="M{hx_-w_*.22:.0f},{hy_-w_*.06:.0f}'
          f' q{w_*.16:.0f},{-w_*.26:.0f} {w_*.40:.0f},{-w_*.16:.0f}'
          f' q{w_*.22:.0f},{w_*.10:.0f} {w_*.26:.0f},{w_*.36:.0f}'
          f' q{w_*.02:.0f},{w_*.16:.0f} {-w_*.16:.0f},{w_*.18:.0f}'
          f' q{-w_*.30:.0f},{w_*.02:.0f} {-w_*.50:.0f},{-w_*.14:.0f} Z"'
          f' fill="#8a6a4a" {o(6)}/>')
    s += (f'<ellipse cx="{hx_+w_*.36:.0f}" cy="{hy_+w_*.30:.0f}"'
          f' rx="{w_*.15:.0f}" ry="{w_*.13:.0f}" fill="#9a7a56" {o(5)}/>')
    s += (f'<ellipse cx="{hx_+w_*.40:.0f}" cy="{hy_+w_*.30:.0f}"'
          f' rx="{w_*.05:.0f}" ry="{w_*.04:.0f}" fill="#4a3526"/>')
    for i in (-1, 1):                    # уши торчком
        s += (f'<path d="M{hx_-w_*.06+i*w_*.08:.0f},{hy_-w_*.20:.0f}'
              f' l{w_*.03:.0f},{-w_*.22:.0f} l{w_*.11:.0f},{w_*.17:.0f} Z"'
              f' fill="#8a6a4a" {o(4)}/>')
    if not A.blink(t, 3.4, .2):
        s += (f'<circle cx="{hx_+w_*.08:.0f}" cy="{hy_-w_*.02:.0f}"'
              f' r="{w_*.055:.0f}" fill="{K}"/>')
    for i in range(7):                   # грива по гребню шеи
        gr = 9 * A.w(t, .8, i * .12)
        s += (f'<path d="M{bx+w_*(.58+i*.08):.0f},{by-w_*(.42+i*.11):.0f}'
              f' q{-w_*.15+gr*.01:.0f},{w_*.16:.0f}'
              f' {-w_*.28+gr*.02:.0f},{w_*.26:.0f}" fill="none"'
              f' stroke="#5e4428" stroke-width="{13*s_:.0f}"'
              f' stroke-linecap="round"/>')
    s += (f'<path d="M{hx_-w_*.08:.0f},{hy_+w_*.14:.0f} q{w_*.20:.0f},'
          f'{w_*.08:.0f} {w_*.38:.0f},{w_*.06:.0f}" fill="none" stroke="{MED}"'
          f' stroke-width="{10*s_:.0f}"/>')
    s += (f'<circle cx="{hx_-w_*.06:.0f}" cy="{hy_+w_*.16:.0f}"'
          f' r="{w_*.08:.0f}" fill="none" stroke="{MED}"'
          f' stroke-width="{8*s_:.0f}"/>')
    s += '</g>'
    return s + '</g>'


def _podkova_rzh(x, y, s_=1.0, t=0.0, kach=0.0):
    """Ржавая подкова: кольцо с ВЫРЕЗАННОЙ серединой и широким разрывом внизу
    (evenodd), пятки с шипами, гнёзда под гвозди, наклон. Дуга обводкой всё
    ещё читалась радугой — теперь это настоящее кольцо с дыркой."""
    rnd = random.Random(int(x) + 7)
    R, w_ = 118 * s_, 50 * s_
    ro, ri = R + w_ / 2, R - w_ / 2
    ug = kach - 22 + 3.0 * A.w(t, 1.8, x * .001)
    oy_ = y + R * .42                    # уровень, где подкова разомкнута
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    d = (f'M{x-ro:.0f},{oy_:.0f} A{ro:.0f},{ro:.0f} 0 1 1 {x+ro:.0f},{oy_:.0f}'
         f' L{x+ri:.0f},{oy_:.0f} A{ri:.0f},{ri:.0f} 0 1 0 {x-ri:.0f},{oy_:.0f} Z')
    s += f'<path d="{d}" fill="#9c5a24" fill-rule="evenodd" {o(max(4, 7*s_))}/>'
    s += (f'<path d="M{x-R:.0f},{oy_:.0f} A{R:.0f},{R:.0f} 0 1 1 {x+R:.0f},{oy_:.0f}"'
          f' fill="none" stroke="#c07a3a" stroke-width="{w_*.30:.0f}"'
          f' opacity=".7"/>')
    for i in range(7):                   # гнёзда под гвозди
        a = math.radians(196 + i * 24.6)
        s += (f'<ellipse cx="{x+R*math.cos(a):.0f}" cy="{y-R*math.sin(a):.0f}"'
              f' rx="{7*s_:.0f}" ry="{10*s_:.0f}" fill="#3a2110"'
              f' {o(max(2, 3*s_))}/>')
    for i in (-1, 1):                    # пятки с шипами ниже разрыва
        s += (f'<path d="M{x+i*ri:.0f},{oy_-4*s_:.0f} h{i*w_:.0f}'
              f' l{-i*w_*.18:.0f},{w_*.76:.0f} h{-i*w_*.64:.0f} Z"'
              f' fill="#7a4418" {o(max(3, 5*s_))}/>')
    for i in range(18):                  # рыжие потёки
        a = rnd.uniform(3.3, 6.1)
        rr = R + rnd.uniform(-w_ * .32, w_ * .32)
        s += (f'<circle cx="{x+math.cos(a)*rr:.0f}" cy="{y-math.sin(a)*rr:.0f}"'
              f' r="{rnd.uniform(5,12)*s_:.0f}" fill="#b5651d" opacity=".55"/>')
    bl = .25 + .3 * (0.5 + 0.5 * A.w(t, 2.4))
    s += (f'<path d="M{x-R*.70:.0f},{y-R*.62:.0f} a{R*.95:.0f},{R*.95:.0f} 0 0 1'
          f' {R*.56:.0f},{-R*.26:.0f}" fill="none" stroke="#f0c088"'
          f' stroke-width="{9*s_:.0f}" opacity="{bl:.2f}"/>')
    s += '</g>'
    for i in (-1, 1):
        s += (f'<circle cx="{x+i*R*.52:.0f}" cy="{y-R*.80:.0f}" r="{13*s_:.0f}"'
              f' fill="#8d949b" {o(max(3, 4*s_))}/>')
        s += (f'<circle cx="{x+i*R*.52-4*s_:.0f}" cy="{y-R*.84:.0f}"'
              f' r="{5*s_:.0f}" fill="#e8eef6" opacity=".7"/>')
    return s


def _vihr(x, y, s_=1.0, t=0.0, lico=True):
    """Вихрь с хитрой рожицей: воронка из витков, листья и сор кружатся."""
    rot = (t * 110) % 360
    s = f'<g transform="rotate({rot*.06:.1f} {x:.0f} {y:.0f})">'
    for i in range(7):                   # витки воронки
        rr = (40 + i * 46) * s_
        fz = i * .18 + t * .5
        s += (f'<ellipse cx="{x+14*s_*A.w(t,1.6,i*.2):.0f}" cy="{y-i*52*s_:.0f}"'
              f' rx="{rr:.0f}" ry="{rr*.30:.0f}" fill="none" stroke="#cfd6de"'
              f' stroke-width="{(16-i):.0f}" opacity="{.75-i*.07:.2f}"'
              f' stroke-dasharray="{60+i*20:.0f} {30+i*8:.0f}"'
              f' stroke-dashoffset="{fz*120:.0f}"/>')
    for i in range(12):                  # сор и листья летят по спирали
        a = t * 2.4 + i * .52
        rr = (60 + (i % 4) * 60) * s_
        s += (f'<path d="M{x+math.cos(a)*rr:.0f},{y-((i*41)%320)*s_:.0f}'
              f' l{10*s_:.0f},{-14*s_:.0f} l{8*s_:.0f},{12*s_:.0f} Z"'
              f' fill="{"#a8641e" if i % 3 else "#6b5a3a"}" opacity=".85"/>')
    if lico:                             # голова-облако под рожицей
        s += (f'<ellipse cx="{x:.0f}" cy="{y-190*s_:.0f}" rx="{104*s_:.0f}"'
              f' ry="{84*s_:.0f}" fill="#e6edf5" opacity=".9" {o(5)}/>')
        s += _rozhica(x, y - 190 * s_, 78 * s_, t, .1, True, "#3a3f48")
    return s + '</g>'


def _mol(x, y, s_=1.0, t=0.0, ph=.0):
    """Наглая моль с салфеткой на шее: пыльные крылья, усики, глазки."""
    w_ = 56 * s_
    fl = A.w(t, .22, ph)
    s = f'<g transform="translate(0,{6*A.w(t,.5,ph):.1f})">'
    for i in (-1, 1):                    # крылья машут
        s += (f'<g transform="rotate({i*fl*26:.1f} {x:.0f} {y:.0f})">'
              f'<ellipse cx="{x+i*w_*.52:.0f}" cy="{y-w_*.10:.0f}" rx="{w_*.56:.0f}"'
              f' ry="{w_*.30:.0f}" fill="#cdbfa2" opacity=".9" {o(max(2, 3*s_))}/>'
              f'<ellipse cx="{x+i*w_*.62:.0f}" cy="{y-w_*.06:.0f}" rx="{w_*.22:.0f}"'
              f' ry="{w_*.12:.0f}" fill="#a79a80" opacity=".7"/></g>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_*.22:.0f}" ry="{w_*.42:.0f}"'
          f' fill="#8d8371" {o(max(2, 3*s_))}/>')
    s += (f'<circle cx="{x:.0f}" cy="{y-w_*.46:.0f}" r="{w_*.21:.0f}" fill="#a3998a"'
          f' {o(max(2, 3*s_))}/>')
    for i in (-1, 1):
        if not A.blink(t, 2.8, ph):
            s += (f'<circle cx="{x+i*w_*.09:.0f}" cy="{y-w_*.48:.0f}"'
                  f' r="{w_*.055:.0f}" fill="{K}"/>')
        s += (f'<path d="M{x+i*w_*.10:.0f},{y-w_*.60:.0f} q{i*w_*.22:.0f},{-w_*.26:.0f}'
              f' {i*w_*.34:.0f},{-w_*.14+3*A.w(t,1.3,ph+i*.2):.0f}" fill="none"'
              f' stroke="#6b645c" stroke-width="{max(2, 4*s_):.0f}"/>')
    s += (f'<path d="M{x-w_*.20:.0f},{y-w_*.30:.0f} q{w_*.20:.0f},{w_*.16:.0f}'
          f' {w_*.40:.0f},0 l{-w_*.14:.0f},{w_*.30:.0f} q{-w_*.12:.0f},{w_*.06:.0f}'
          f' {-w_*.14:.0f},0 Z" fill="#f2efe6" {o(max(2, 3*s_))}/>')
    return s + '</g>'


def _komar(x, y, s_=1.0, t=0.0, ph=.0, chemodan=True):
    """Комар-путешественник: длинный хоботок, дрожащие крылья, шесть ног,
    ПОЛОСАТЫЙ ШАРФ с развевающимся концом и саквояж с дужкой."""
    w_ = 60 * s_
    sh = 5 * s_ * A.w(t, .7, ph)
    s = f'<g transform="translate({sh:.1f},{2*A.w(t,.9,ph):.1f})">'
    for i in range(6):                   # шесть ног, переступают
        sgn = -1 if i < 3 else 1
        st = 12 * s_ * A.w(t, .62, ph + i * .17)
        s += (f'<path d="M{x+sgn*w_*.2:.0f},{y-w_*.3:.0f}'
              f' q{sgn*w_*.5:.0f},{-w_*.2:.0f} {sgn*w_*.74+st:.0f},{w_*.46:.0f}"'
              f' fill="none" stroke="#3f4650" stroke-width="{max(3, 7*s_):.0f}"'
              f' stroke-linecap="round"/>')
    for i in (-1, 1):                    # крылья дрожат
        s += (f'<ellipse cx="{x+i*w_*.34:.0f}" cy="{y-w_*.78:.0f}"'
              f' rx="{w_*.50:.0f}"'
              f' ry="{w_*(.12+.07*abs(A.w(t,.12,ph))):.1f}" fill="#dfeaf2"'
              f' opacity=".6" {o(3)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-w_*.40:.0f}" rx="{w_*.46:.0f}"'
          f' ry="{w_*.26:.0f}" fill="#4a5260" {o(max(3, 5*s_))}/>')
    for i in range(4):                   # сегменты брюшка
        s += (f'<path d="M{x-w_*.30+i*w_*.18:.0f},{y-w_*.60:.0f}'
              f' q{w_*.03:.0f},{w_*.20:.0f} 0,{w_*.38:.0f}" fill="none"'
              f' stroke="#394150" stroke-width="{max(2, 5*s_):.0f}"'
              f' opacity=".7"/>')
    s += (f'<circle cx="{x+w_*.50:.0f}" cy="{y-w_*.58:.0f}" r="{w_*.22:.0f}"'
          f' fill="#5a6272" {o(max(2, 4*s_))}/>')
    s += (f'<path d="M{x+w_*.66:.0f},{y-w_*.50:.0f} l{w_*.50:.0f},{w_*.18:.0f}"'
          f' stroke="#2f3337" stroke-width="{max(3, 6*s_):.0f}"'
          f' stroke-linecap="round"/>')
    if not A.blink(t, 3.0, ph):
        s += (f'<circle cx="{x+w_*.54:.0f}" cy="{y-w_*.64:.0f}"'
              f' r="{w_*.08:.0f}" fill="#f2efe6"/>')
        s += (f'<circle cx="{x+w_*.56:.0f}" cy="{y-w_*.64:.0f}"'
              f' r="{w_*.04:.0f}" fill="{K}"/>')
    # ШАРФ: обмотка вокруг шеи и длинный конец, полосами
    s += (f'<path d="M{x+w_*.20:.0f},{y-w_*.40:.0f} q{w_*.20:.0f},{w_*.16:.0f}'
          f' {w_*.42:.0f},{w_*.04:.0f} l{w_*.02:.0f},{w_*.18:.0f}'
          f' q{-w_*.26:.0f},{w_*.12:.0f} {-w_*.48:.0f},{-w_*.04:.0f} Z"'
          f' fill="{TKAN}" {o(max(2, 4*s_))}/>')
    vey = w_ * .12 * A.w(t, .8, ph)
    s += (f'<path d="M{x+w_*.22:.0f},{y-w_*.26:.0f}'
          f' q{-w_*.30:.0f},{w_*.30+vey:.0f} {-w_*.76:.0f},{w_*.40:.0f}'
          f' l{-w_*.04:.0f},{-w_*.22:.0f} q{w_*.40:.0f},{-w_*.10:.0f}'
          f' {w_*.66:.0f},{-w_*.34:.0f} Z" fill="{TKAN}" {o(max(2, 4*s_))}/>')
    for i in range(3):                   # полоски на шарфе
        s += (f'<line x1="{x-w_*.10-i*w_*.18:.0f}" y1="{y-w_*.06+i*w_*.05:.0f}"'
              f' x2="{x-w_*.06-i*w_*.18:.0f}" y2="{y+w_*.14+i*w_*.04:.0f}"'
              f' stroke="#f2efe6" stroke-width="{max(2, 5*s_):.0f}"'
              f' opacity=".9"/>')
    if chemodan:                         # саквояж с дужкой и замком
        bx_, by_ = x - w_ * .92, y - w_ * .04
        s += (f'<path d="M{bx_-w_*.30:.0f},{by_:.0f} h{w_*.60:.0f}'
              f' q{w_*.06:.0f},{w_*.30:.0f} {-w_*.03:.0f},{w_*.42:.0f}'
              f' h{-w_*.54:.0f} q{-w_*.09:.0f},{-w_*.12:.0f}'
              f' {-w_*.03:.0f},{-w_*.42:.0f} Z" fill="#8a5a2a"'
              f' {o(max(3, 5*s_))}/>')
        s += (f'<path d="M{bx_-w_*.18:.0f},{by_-w_*.02:.0f}'
              f' q{w_*.18:.0f},{-w_*.26:.0f} {w_*.36:.0f},0" fill="none"'
              f' stroke="#5e3a16" stroke-width="{max(3, 6*s_):.0f}"/>')
        s += (f'<rect x="{bx_-w_*.32:.0f}" y="{by_+w_*.12:.0f}"'
              f' width="{w_*.64:.0f}" height="{w_*.08:.0f}" fill="{ZOL}"'
              f' opacity=".9"/>')
        s += (f'<rect x="{bx_-w_*.05:.0f}" y="{by_-w_*.04:.0f}"'
              f' width="{w_*.10:.0f}" height="{w_*.12:.0f}" rx="{w_*.02:.0f}"'
              f' fill="{ZOL}" {o(2)}/>')
    return s + '</g>'


def _sekator(x, y, s_=1.0, t=0.0, szhat=0.0, ug=0.0):
    """Садовые ножницы-секатор: два лезвия сходятся в точке x,y, за шарниром
    две КРАСНЫЕ ПЕТЛИ-рукоятки. Петли — главный признак, по ним ножницы и
    узнают (прежние прямые бруски читались палками)."""
    raz = 13 * (1 - szhat)
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    for i, sgn in ((0, -1), (1, 1)):
        a = sgn * raz
        s += f'<g transform="rotate({a:.1f} {x:.0f} {y:.0f})">'
        s += (f'<path d="M{x:.0f},{y:.0f} q{-46*s_:.0f},{sgn*6*s_:.0f}'
              f' {-92*s_:.0f},{sgn*18*s_:.0f} l{-6*s_:.0f},{-sgn*18*s_:.0f}'
              f' q{46*s_:.0f},{-sgn*10*s_:.0f} {96*s_:.0f},{-sgn*4*s_:.0f} Z"'
              f' fill="#e8eef4" {o(max(3, 4*s_))}/>')
        s += (f'<rect x="{x-152*s_:.0f}" y="{y+sgn*22*s_-11*s_:.0f}"'
              f' width="{64*s_:.0f}" height="{22*s_:.0f}" rx="{11*s_:.0f}"'
              f' fill="{KRAS}" {o(max(2, 4*s_))}/>')
        s += (f'<ellipse cx="{x-192*s_:.0f}" cy="{y+sgn*34*s_:.0f}"'
              f' rx="{44*s_:.0f}" ry="{32*s_:.0f}" fill="none" stroke="{KRAS}"'
              f' stroke-width="{20*s_:.0f}"/>')
        s += (f'<ellipse cx="{x-192*s_:.0f}" cy="{y+sgn*34*s_:.0f}"'
              f' rx="{44*s_:.0f}" ry="{32*s_:.0f}" fill="none" stroke="{K}"'
              f' stroke-width="{4*s_:.0f}"/>')
        s += '</g>'
    s += (f'<circle cx="{x-96*s_:.0f}" cy="{y+10*s_:.0f}" r="{14*s_:.0f}"'
          f' fill="#8d949b" {o(max(2, 3*s_))}/>')
    s += (f'<circle cx="{x-96*s_:.0f}" cy="{y+10*s_:.0f}" r="{5*s_:.0f}"'
          f' fill="#3f454a"/>')
    bl = .3 + .4 * abs(A.w(t, 2.0))
    s += (f'<line x1="{x-12*s_:.0f}" y1="{y-6*s_:.0f}" x2="{x-64*s_:.0f}"'
          f' y2="{y-16*s_:.0f}" stroke="#ffffff" stroke-width="{5*s_:.0f}"'
          f' opacity="{bl:.2f}"/>')
    return s + '</g>'


def _busy(x, y, n, t, s_=1.0, ph=.0, dl=1.0):
    """Бусы из рябины на суровой нитке: провисают дугой, ягоды качаются."""
    s = ""
    w_ = 300 * s_ * dl
    for i in range(n):
        p = i / max(1, n - 1)
        bx = x - w_ / 2 + p * w_
        by = y + math.sin(p * 3.14159) * 90 * s_ * dl + 4 * A.w(t, 1.8, ph + p)
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{11*s_:.0f}"'
              f' fill="{"#8e2a1c" if i % 5 == 0 else KRAS}" {o(max(2, 3*s_))}/>')
        s += (f'<circle cx="{bx-3*s_:.0f}" cy="{by-4*s_:.0f}" r="{3.4*s_:.1f}"'
              f' fill="#ffd0b0" opacity=".6"/>')
    s += (f'<path d="M{x-w_/2:.0f},{y:.0f} q{w_/2:.0f},{120*s_*dl:.0f} {w_:.0f},0"'
          f' fill="none" stroke="#d8cbb0" stroke-width="{max(2, 4*s_):.0f}"'
          f' opacity=".8"/>')
    return s


def _shkaf(x, y, w_, h_, t, open_=0.0, zerkalo=False):
    """Платяной шкаф: две дверцы, одна приоткрыта, ручки, карниз."""
    s = ten(x + w_ / 2, y + h_ + 12, w_ * .5, 18, .5)
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8"'
          f' fill="#3a2b1d" {o(8)}/>')
    s += (f'<rect x="{x-14:.0f}" y="{y-34:.0f}" width="{w_+28:.0f}" height="38" rx="8"'
          f' fill="url(#derev)" {o(7)}/>')
    s += (f'<rect x="{x+w_*.02:.0f}" y="{y+6:.0f}" width="{w_*.47:.0f}"'
          f' height="{h_-12:.0f}" rx="6" fill="url(#derev)" {o(6)}/>')
    pv = x + w_ * .51                   # створка открывается от своей кромки
    s += (f'<g transform="translate({pv:.0f},0) scale({1-open_*.62:.3f},1)'
          f' translate({-pv:.0f},0)">'
          f'<rect x="{pv:.0f}" y="{y+6:.0f}" width="{w_*.47:.0f}"'
          f' height="{h_-12:.0f}" rx="6" fill="url(#derev)" {o(6)}/></g>')
    if zerkalo:
        s += (f'<rect x="{x+w_*.08:.0f}" y="{y+h_*.08:.0f}" width="{w_*.35:.0f}"'
              f' height="{h_*.56:.0f}" rx="6" fill="url(#stekl)" opacity=".6" {o(4)}/>')
        s += (f'<path d="M{x+w_*.12:.0f},{y+h_*.52:.0f} l{w_*.22:.0f},{-h_*.36:.0f}"'
              f' stroke="#ffffff" stroke-width="16"'
              f' opacity="{.16+.1*abs(A.w(t,3.0)):.2f}"/>')
    for i, px in ((0, x + w_ * .44),
                  (1, x + w_ * .51 + w_ * .47 * (1 - open_ * .62) - w_ * .03)):
        s += (f'<ellipse cx="{px:.0f}" cy="{y+h_*.5:.0f}" rx="9" ry="22"'
              f' fill="url(#zhel)" {o(3)}/>')
    return s


def _veshalka(x, y, w_, t, kryuchkov=5, odezhda=True):
    """Вешалка в прихожей: планка, крючки, на них пальто и шарф."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="34" rx="8"'
         f' fill="url(#derev)" {o(7)}/>')
    for i in range(kryuchkov):
        hx = x + 40 + i * (w_ - 80) / max(1, kryuchkov - 1)
        s += (f'<path d="M{hx:.0f},{y+34:.0f} l0,26 q0,16 16,16" fill="none"'
              f' stroke="#8d949b" stroke-width="11" stroke-linecap="round"/>')
        s += (f'<circle cx="{hx:.0f}" cy="{y+17:.0f}" r="7" fill="#5d6168"/>')
    if odezhda:
        for i, (ox_, col, ww) in enumerate(((.22, "#3f4a5e", 150),
                                            (.56, "#5b2f3a", 130))):
            hx = x + w_ * ox_
            kach = 1.8 * A.w(t, 2.6, i * .3)
            s += (f'<g transform="rotate({kach:.2f} {hx:.0f} {y+60:.0f})">'
                  f'<path d="M{hx-ww*.5:.0f},{y+104:.0f} q{ww*.16:.0f},{-44:.0f}'
                  f' {ww*.5:.0f},{-44:.0f} q{ww*.34:.0f},0 {ww*.5:.0f},{44:.0f}'
                  f' l{ww*.08:.0f},{250:.0f} q{-ww*.58:.0f},{26:.0f} {-ww*1.16:.0f},0 Z"'
                  f' fill="{col}" {o(6)}/>'
                  f'<path d="M{hx:.0f},{y+66:.0f} l0,{250:.0f}" stroke="{K}"'
                  f' stroke-width="4" opacity=".5"/></g>')
        sh = x + w_ * .82
        s += (f'<path d="M{sh:.0f},{y+54:.0f} q{-34:.0f},{90+6*A.w(t,2.2):.0f}'
              f' {-16:.0f},{200:.0f} l{44:.0f},{10:.0f} q{-10:.0f},{-110:.0f}'
              f' {10:.0f},{-196:.0f} Z" fill="{TKAN}" {o(5)}/>')
    return s


# ── 69 ─────────────────────────────────────────────────────────────────────
def rzhavaya_podkova_na_dachnoy_dveri(t):
    """Дверь дачного домика с облупленной голубой краской, над ней ОГРОМНАЯ
    ржавая подкова на двух гвоздях. Дед держит внука у себя на плечах, тот
    трогает подкову и смотрит на рыжий от ржавчины палец."""
    rnd = random.Random(6911)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 691)
    s += oblaka(t, 150, 4, 701, .3, "#c6d2e0", 14.0)
    s += SL(Z_DAL, goloe_derevo(180, 840, 480, t, 709, 7, "#363844"))
    s += SL(Z_DAL, pleten(1560, 880, 360, 190, 7))
    s += SL(Z_DAL, gryaz_polosa(820, 170, "#4f4a40"))
    # стена дачи во всю ширину: голубые доски с проплешинами краски
    st = doski(60, 60, 1800, 1020, 96, True, "dosk")
    st += f'<rect x="60" y="60" width="1800" height="1020" fill="#7ea2b6" opacity=".8"/>'
    for i in range(34):
        px, py = 80 + rnd.random() * 1760, 100 + rnd.random() * 940
        st += (f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{rnd.uniform(20,62):.0f}"'
               f' ry="{rnd.uniform(12,40):.0f}" fill="#ad7f4f" opacity=".88"/>')
    st += f'<path d="M20,120 L960,-170 L1900,120 Z" fill="#55493c" opacity=".96" {o(9)}/>'
    s += SL(Z_DAL, st)
    # ДВЕРЬ в центре и ПОДКОВА над ней — крупно
    dx, dy, dw, dh = 660, 430, 620, 650
    dv = (f'<rect x="{dx-30}" y="{dy-30}" width="{dw+60}" height="{dh+30}" rx="10"'
          f' fill="url(#derev)" {o(9)}/>')
    dv += dver(dx, dy, dw, dh, 0.0, "#5f88a0", True, False)
    for i in range(26):                  # шелушинки краски на двери
        px, py = dx + 30 + rnd.random() * (dw - 60), dy + 40 + rnd.random() * (dh - 80)
        dv += (f'<path d="M{px:.0f},{py:.0f} q{rnd.uniform(10,28):.0f},-10'
               f' {rnd.uniform(22,50):.0f},{rnd.uniform(5,18):.0f}'
               f' q{-rnd.uniform(12,24):.0f},13 {-rnd.uniform(24,52):.0f},0 Z"'
               f' fill="#a67a4e" opacity=".92"/>')
    dv += (f'<rect x="{dx+dw*.12:.0f}" y="{dy+dh*.10:.0f}" width="{dw*.76:.0f}"'
           f' height="{dh*.30:.0f}" rx="8" fill="none" stroke="#3f5e70"'
           f' stroke-width="14" opacity=".85"/>')
    dv += (f'<ellipse cx="{dx+dw-70:.0f}" cy="{dy+dh*.52:.0f}" rx="24" ry="34"'
           f' fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, dv)
    s += SL(Z_SRED, f'<path d="M{dx-130},{dy-44} h{dw+260} l-70,-70 h{-dw-120} Z"'
                    f' fill="{DOSKA2}" {o(9)}/>')
    px_, py_ = dx + dw / 2, dy - 210
    s += SL(Z_SRED, _podkova_rzh(px_, py_, 1.3, t,
                                 7 * A.ease(A.seg(t, 2.6, .6)) * A.w(t, .8)))
    # лампочка над крыльцом: тёплое пятно на двери и подкове
    flx, fly = dx + dw + 190, dy - 90
    s += SL(Z_SRED, f'<rect x="{flx-12:.0f}" y="{fly-170:.0f}" width="24"'
                    f' height="80" rx="8" fill="#3a3f46" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{flx-80:.0f},{fly-90:.0f} h160 l-22,-52 h-116 Z"'
                    f' fill="#2f3337" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{flx-66:.0f},{fly-90:.0f} h132 l-14,170 h-104 Z"'
                    f' fill="url(#stekl)" opacity=".7" {o(6)}/>')
    s += SL(Z_SRED, ogon(flx, fly + 40, t, .95, .2, 5))
    s += SL(Z_SRED, f'<path d="M{flx-76:.0f},{fly+82:.0f} h152 l16,38 h-184 Z"'
                    f' fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, teplo(flx - 60, fly + 60, 1000, 840,
                          .5 + .12 * abs(A.w(t, 1.6))))
    # дед держит внука на плечах, внук тянется к подкове
    pod = A.ease(A.seg(t, .4, 1.6))
    gx = px_ - 40
    s += SL(Z_SRED, figura(gx, 1076, 540, t, "#3a3a46", "#ffd0a0", False, .2,
                           False, 1.0, True, 1.0, True))
    s += SL(Z_SRED, para_izo_rta(gx + 70, 700, t, .2, 1.2, .55))
    # дед поднимает внука НА РУКАХ, сбоку от себя — так читаются оба
    ruk0, (hx0, hy0) = rukav(gx + 120, 790, 180, -52, t, "#3a3a46", "#ffd0a0",
                             .1, 3.0)
    s += SL(Z_SRED, ruk0)
    vy = 790 - pod * 150
    s += SL(Z_SRED, figura(gx + 250, vy, 330, t, "#6b3a44", "#ffd0a0", False, .55,
                           False, 1.0, False, 1.4, False, True))
    ruk, (kx, ky) = rukav(gx + 290, vy - 260, 130, -68 + 8 * A.w(t, 1.2), t,
                          "#6b3a44", "#ffd0a0", .4, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="30" ry="23"'
                    f' fill="#6b3a44" {o(5)}/>')
    if pod > .85:                        # палец рыжий от ржавчины
        s += SL(Z_SRED, f'<ellipse cx="{kx+6:.0f}" cy="{ky-14:.0f}" rx="18"'
                        f' ry="14" fill="#a86a3a"'
                        f' opacity="{.5+.45*abs(A.w(t,1.4)):.2f}"/>')
    for i in range(10):                  # чешуйки краски сыплются вниз
        k = ((t * .5) + i * .1) % 1.0
        s += SL(Z_LETIT, f'<path d="M{dx+60+i*62:.0f},{dy+140+k*560:.0f}'
                         f' l18,-8 l7,14 Z" fill="#a9c6d6"'
                         f' opacity="{.9*(1-k):.2f}"/>')
    s += SL(Z_SRED, _valenok(400, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_SRED, _valenok(510, 1012, .86, t, .6, True, "#6e6358"))
    s += SL(Z_SRED, _vedro_dach(1620, 1012, 1.2, t))
    s += SL(Z_PERED, f'<rect x="120" y="340" width="100" height="740" rx="10"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_PERED, f'<path d="M80,350 h190 l-26,-64 h-140 Z" fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_PERED, grozd_ryabiny(1790, 460, t, 1.7, 16, 733, .2))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 739, .45, .9))
    s += vinetka(.44)
    return s


# ── 70 ─────────────────────────────────────────────────────────────────────
def ryabinovye_busy_na_nitke(t):
    """Осеннее крыльцо: посреди него большая миска рябины, две девочки нижут
    ягоды толстой иглой на суровую нитку, готовые бусы висят дугой."""
    rnd = random.Random(7013)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 743)
    s += oblaka(t, 180, 4, 751, .3, "#cbd6e2", 15.0)
    s += ulica_dal(1300, 690, 640, t, False, 757)
    s += SL(Z_DAL, goloe_derevo(140, 840, 470, t, 761, 7, "#363844"))
    s += SL(Z_DAL, gryaz_polosa(820, 180, "#4f4a40"))
    st = brevna(200, 0, 1540, 870, 112)
    st += f'<rect x="200" y="0" width="1540" height="870" fill="#9c7049" opacity=".3"/>'
    st += f'<path d="M160,40 L970,-220 L1780,40 Z" fill="#55493c" opacity=".95" {o(9)}/>'
    s += SL(Z_DAL, st)
    # окно сеней с лампой за стеклом — тёплое пятно
    s += SL(Z_DAL, okno_izby(1330, 160, 330, 260, t, svet=True, moroz=.15))
    s += SL(Z_DAL, lampa(1490, 400, t, .7))
    s += SL(Z_DAL, teplo(1490, 300, 560, 470, .46 + .1 * abs(A.w(t, 1.8))))
    s += SL(Z_SRED, dver(300, 270, 420, 610, 0.0, "url(#derev)", True, False))
    s += SL(Z_SRED, f'<rect x="170" y="880" width="1620" height="56" rx="10"'
                    f' fill="url(#dosk)" {o(9)}/>')
    s += SL(Z_SRED, polovicy(936, "url(#pol)"))
    s += SL(Z_SRED, lavka(700, 880, 480))
    # МИСКА РЯБИНЫ в центре, крупно
    mx, my = 940, 900
    ms = (f'<path d="M{mx-270:.0f},{my-190:.0f} q0,200 {270:.0f},202'
          f' q{270:.0f},-2 {270:.0f},-202 Z" fill="url(#glina)" {o(10)}/>')
    ms += (f'<ellipse cx="{mx:.0f}" cy="{my-190:.0f}" rx="270" ry="50"'
           f' fill="#9c6a3c" {o(7)}/>')
    ms += (f'<path d="M{mx-230:.0f},{my-140:.0f} q50,70 150,92" fill="none"'
           f' stroke="#e0b183" stroke-width="14" opacity=".5"/>')
    for i in range(60):                  # ягоды горкой, часть уже тёмная
        a = rnd.uniform(0, 6.283)
        rr = rnd.uniform(0, 1) ** .5 * 246
        bx, by = mx + math.cos(a) * rr, my - 196 + math.sin(a) * rr * .24
        tem = A.ease(A.seg(t, 1.6 + (i % 7) * .22, 1.2))
        col = "#8e2a1c" if (i % 5 == 0 or tem > .7) else KRAS
        ms += (f'<circle cx="{bx:.0f}" cy="{by+4*A.w(t,2.0,i*.07):.0f}"'
               f' r="{16-2.5*tem:.1f}" fill="{col}" {o(2)}/>')
        if i % 3 == 0:
            ms += (f'<circle cx="{bx-5:.0f}" cy="{by-6:.0f}" r="5"'
                   f' fill="#ffd0b0" opacity="{.6-.3*tem:.2f}"/>')
    s += SL(Z_SRED, ms)
    # девочки по сторонам миски
    s += SL(Z_SRED, figura(470, 1020, 470, t, "#5b2f3a", "#ffd0a0", False, .3,
                           False, 1.0, False, 1.4, False, False))
    s += SL(Z_SRED, figura(1480, 1024, 460, t, "#2e4a5a", "#ffd0a0", True, .65,
                           False, 1.0, False, 1.2))
    s += SL(Z_SRED, para_izo_rta(516, 740, t, .3, 1.0, .5))
    s += SL(Z_SRED, para_izo_rta(1520, 748, t, .7, 1.0, .5))
    # рукав девочки заканчивается НАД миской, в нём игла с нитью
    sh = A.w(t, .9, .1)
    ruk, (ix, iy) = rukav(560, 740, 150, 34 + 14 * sh, t, "#5b2f3a", "#ffd0a0",
                          .1, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{ix:.0f}" cy="{iy:.0f}" rx="32" ry="24"'
                    f' fill="#5b2f3a" {o(5)}/>')
    igl = (f'<line x1="{ix+18:.0f}" y1="{iy+6:.0f}" x2="{ix+190:.0f}"'
           f' y2="{iy+54+16*sh:.0f}" stroke="#cfd6dc" stroke-width="13"'
           f' stroke-linecap="round"/>')
    igl += (f'<ellipse cx="{ix+26:.0f}" cy="{iy+8:.0f}" rx="16" ry="11"'
            f' fill="none" stroke="#8d949b" stroke-width="7"/>')
    igl += (f'<circle cx="{ix+150:.0f}" cy="{iy+44+13*sh:.0f}" r="9"'
            f' fill="#ffffff" opacity="{.4+.5*abs(A.w(t,1.6)):.2f}"/>')
    igl += (f'<circle cx="{ix+192:.0f}" cy="{iy+56+16*sh:.0f}" r="20"'
            f' fill="{KRAS}" {o(4)}/>')
    igl += (f'<path d="M{ix+26:.0f},{iy+10:.0f} q-70,90 -170,130" fill="none"'
            f' stroke="#e2d6bc" stroke-width="6" opacity=".9"/>')
    s += SL(Z_SRED, igl)
    # бусы растут и девочки ими меряются
    rost = A.ease(A.seg(t, .3, 3.2))
    s += SL(Z_SRED, _busy(700, 700, int(8 + 16 * rost), t, 1.7, .2, .5 + .7 * rost))
    s += SL(Z_SRED, _busy(1450, 690, int(6 + 10 * rost), t, 1.35, .5,
                          .4 + .5 * rost))
    ruk2, (jx, jy) = rukav(1400, 760, 150, 182 - 18 * A.w(t, 1.1, .4), t,
                           "#2e4a5a", "#ffd0a0", .4, 5.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<ellipse cx="{jx:.0f}" cy="{jy:.0f}" rx="30" ry="22"'
                    f' fill="#2e4a5a" {o(5)}/>')
    s += SL(Z_SRED, _korzina_ryab(1740, 1012, 240, 170, t, 769))
    s += SL(Z_SRED, kura(1660, 1012, t, .9, .4))
    s += SL(Z_PERED, grozd_ryabiny(150, 320, t, 1.9, 17, 773, .1))
    s += SL(Z_PERED, f'<rect x="1810" y="150" width="110" height="930" rx="12"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 787, .4, .85))
    s += vinetka(.42)
    return s


def _korzina_ryab(x, y, w_, h_, t, seed=7):
    """Корзинка с рябиновыми кистями: лоза, дужка, ягоды горкой."""
    rnd = random.Random(seed)
    s = ten(x, y + 10, w_ * .52, 15, .45)
    s += (f'<path d="M{x-w_/2:.0f},{y-h_:.0f} L{x+w_/2:.0f},{y-h_:.0f}'
          f' L{x+w_*.36:.0f},{y:.0f} L{x-w_*.36:.0f},{y:.0f} Z" fill="url(#solom)" {o(6)}/>')
    for i in range(5):
        yy = y - h_ + 16 + i * (h_ - 24) / 4
        kk = (w_ / 2) * (1 - .26 * (i / 4))
        d = f'M{x-kk:.0f},{yy:.0f}'
        for j in range(5):
            xx = x - kk + j * (kk * 2 / 5)
            d += (f' Q{xx+kk/5:.0f},{yy+(10 if j % 2 == 0 else -10):.0f}'
                  f' {xx+kk*2/5:.0f},{yy:.0f}')
        s += f'<path d="{d}" fill="none" stroke="#b78a46" stroke-width="8"/>'
    for i in range(16):
        bx = x + rnd.uniform(-w_ * .42, w_ * .42)
        by = y - h_ - rnd.uniform(-6, 26)
        s += (f'<circle cx="{bx:.0f}" cy="{by+3*A.w(t,2.2,i*.09):.0f}" r="11"'
              f' fill="{KRAS if i % 4 else "#8e2a1c"}" {o(2)}/>')
    duga = 2.6 * A.w(t, 3.0, seed * .05)
    s += (f'<g transform="rotate({duga:.2f} {x:.0f} {y-h_+2:.0f})">'
          f'<path d="M{x-w_*.40:.0f},{y-h_*.98:.0f} q{w_*.40:.0f},{-h_*.76:.0f}'
          f' {w_*.80:.0f},{-h_*.01:.0f}" fill="none" stroke="#9a7238"'
          f' stroke-width="13"/></g>')
    return s


# ── 71 ─────────────────────────────────────────────────────────────────────
def grozd_ryabiny_u_svoego_krylca(t):
    """Крыльцо дачного дома с горящим фонарём: женщина в куртке срезает
    секатором тяжёлую гроздь рябины у забора и вешает её на гвоздь у двери,
    пёс нюхает упавшие ягоды."""
    rnd = random.Random(7121)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 797)
    s += oblaka(t, 150, 5, 809, .28, "#c2cfdd", 16.0)
    s += SL(Z_DAL, ulica_dal(40, 640, 760, t, False, 811))
    s += SL(Z_DAL, gryaz_polosa(790, 200, "#4a463c"))
    s += SL(Z_DAL, pleten(60, 790, 560, 200, 9))
    # стена дачного дома во всю ширину, крыльцо под навесом
    dom = doski(0, 60, 1920, 1020, 92, True, "dosk")
    dom += f'<rect x="0" y="60" width="1920" height="1020" fill="#8a9aa2" opacity=".5"/>'
    dom += f'<path d="M-40,130 L960,-150 L1960,130 Z" fill="#50483e" opacity=".96" {o(9)}/>'
    s += SL(Z_DAL, dom)
    dx, dy, dw, dh = 1320, 390, 470, 690
    s += SL(Z_SRED, dver(dx, dy, dw, dh, 0.0, "#4a5a46", True, False))
    s += SL(Z_SRED, f'<rect x="{dx+dw*.16:.0f}" y="{dy+dh*.10:.0f}"'
                    f' width="{dw*.68:.0f}" height="{dh*.28:.0f}" rx="8"'
                    f' fill="url(#stekl)" opacity=".5" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="{dx-30}" y="{dy-34}" width="{dw+60}" height="34" rx="8"'
                    f' fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="1140" y="1000" width="780" height="50" rx="10"'
                    f' fill="url(#dosk)" {o(9)}/>')
    # фонарь на крыльце: качается и горит
    fk = 3.4 * A.w(t, 2.4, .1)
    fx_, fy_ = dx - 190, dy - 60
    fon = f'<g transform="rotate({fk:.2f} {fx_:.0f} {fy_:.0f})">'
    fon += (f'<line x1="{fx_:.0f}" y1="{fy_:.0f}" x2="{fx_:.0f}" y2="{fy_+90:.0f}"'
            f' stroke="#3a3f46" stroke-width="12"/>')
    fon += (f'<path d="M{fx_-86:.0f},{fy_+100:.0f} h172 l-20,-48 h-132 Z"'
            f' fill="#2f3337" {o(6)}/>')
    fon += (f'<path d="M{fx_-72:.0f},{fy_+100:.0f} h144 l-12,190 h-120 Z"'
            f' fill="url(#stekl)" opacity=".68" {o(6)}/>')
    fon += ogon(fx_, fy_ + 250, t, .85, .2, 5)
    fon += (f'<path d="M{fx_-80:.0f},{fy_+290:.0f} h160 l16,40 h-192 Z"'
            f' fill="#2f3337" {o(6)}/>')
    fon += '</g>'
    s += SL(Z_SRED, fon)
    s += SL(Z_SRED, teplo(fx_, fy_ + 230, 820, 700, .46 + .1 * abs(A.w(t, 1.6))))
    # РЯБИНА У ЗАБОРА и ТЯЖЁЛАЯ ГРОЗДЬ — главный предмет
    s += SL(Z_SRED, goloe_derevo(520, 1010, 720, t, 823, 8, "#443a2c"))
    for i in range(3):
        s += SL(Z_SRED, grozd_ryabiny(300 + i * 70, 400 + (i % 2) * 120, t,
                                      1.1, 13, 827 + i, i * .2))
    srez = A.ease(A.seg(t, .6, 1.0))
    gx, gy = 620, 560
    if srez < .98:
        s += SL(Z_SRED, grozd_ryabiny(gx, gy, t, 4.0, 30, 829, .1))
    s += SL(Z_SRED, f'<path d="M520,860 q{(gx-520)*.5:.0f},{-180:.0f}'
                    f' {gx-500:.0f},{gy-830:.0f}" fill="none" stroke="#5e4428"'
                    f' stroke-width="16"/>')
    s += SL(Z_SRED, _sekator(gx + 300, gy - 110, 1.9, t, srez, -16))
    # женщина рядом с гроздью, рукав короткий и к секатору
    zx = 880
    s += SL(Z_SRED, figura(zx, 1060, 540, t, "#2e4a5a", "#ffd0a0", False, .3,
                           True, 1.0, True, 1.2, False, True))
    ruk, _ = rukav(zx - 120, 730, 190, 206, t, "#2e4a5a", "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, para_izo_rta(zx + 56, 700, t, .2, 1.2, .5))
    # гроздь переезжает на гвоздь у двери
    pere = A.ease(A.seg(t, 2.2, 1.6))
    hx = gx + (dx - 80 - gx) * pere
    hy = gy + (dy + 210 - gy) * pere - math.sin(pere * 3.14159) * 130
    if srez > .5:
        s += SL(Z_SRED, grozd_ryabiny(hx, hy, t, 2.6, 22, 839, .3))
    s += SL(Z_SRED, f'<circle cx="{dx-80:.0f}" cy="{dy+160:.0f}" r="13"'
                    f' fill="#8d949b" {o(4)}/>')
    # пёс нюхает упавшие ягоды
    s += SL(Z_SRED, _pes(1200, 1004, 1.9, t, .4, "#6b5a46"))
    for i in range(9):
        s += SL(Z_SRED, f'<circle cx="{1230+i*26+6*A.w(t,2.2,i*.2):.0f}"'
                        f' cy="{1062+(i%3)*8:.0f}" r="11"'
                        f' fill="{KRAS if i % 3 else "#8e2a1c"}" {o(2)}/>')
    s += SL(Z_SRED, _vedro_dach(1010, 1012, 1.2, t))
    s += SL(Z_SRED, _valenok(1760, 1012, .86, t, .2, True, "#5f6a72"))
    s += SL(Z_PERED, f'<rect x="1176" y="360" width="80" height="720" rx="10"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_PERED, f'<rect x="1856" y="360" width="80" height="720" rx="10"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_PERED, goloe_derevo(80, 1080, 640, t, 853, 7, "#2a2c34"))
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 857, .45, .95))
    s += vinetka(.44)
    return s


def _vedro_dach(x, y, s_=1.0, t=0.0):
    """Садовое ведро: пластиковый конус, ободок, дуга ручки, пара ягод внутри."""
    w1, w2, hh = 70 * s_, 52 * s_, 94 * s_
    kach = 2.2 * A.w(t, 2.0, x * .001)
    s = ten(x, y + 8 * s_, w1 * .9, 11 * s_, .4)
    s += f'<g transform="rotate({kach:.2f} {x:.0f} {y-hh*1.8:.0f})">'
    s += (f'<path d="M{x-w1:.0f},{y-hh:.0f} h{w1*2:.0f}'
          f' L{x+w2:.0f},{y:.0f} h{-w2*2:.0f} Z" fill="#4a6a52" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w1:.0f}" ry="{12*s_:.0f}"'
          f' fill="#3a5742" {o(4)}/>')
    for i in range(7):
        s += (f'<circle cx="{x-w1*.6+i*w1*.2:.0f}" cy="{y-hh+4*s_:.0f}"'
              f' r="{10*s_:.0f}" fill="{KRAS if i % 3 else "#8e2a1c"}"'
              f' opacity=".95"/>')
    s += (f'<path d="M{x-w1:.0f},{y-hh*.96:.0f} q{w1:.0f},{-hh*.72:.0f} {w1*2:.0f},0"'
          f' fill="none" stroke="#2f3337" stroke-width="{7*s_:.0f}"/>')
    s += (f'<path d="M{x-w1*.7:.0f},{y-hh*.7:.0f} L{x-w2*.66:.0f},{y-hh*.1:.0f}"'
          f' stroke="#cfe4d8" stroke-width="{8*s_:.0f}"'
          f' opacity="{.25+.25*abs(A.w(t,2.4)):.2f}"/>')
    return s + '</g>'


# ── 72 ─────────────────────────────────────────────────────────────────────
def vetka_ryabiny_v_vaze(t):
    """Прихожая у входной двери: высокая стеклянная ваза с большой веткой
    рябины стоит на тумбочке и занимает пол-кадра, рядом горит лампа под
    абажуром, хозяйка поправляет гроздья и переставляет вазу на подоконник."""
    rnd = random.Random(7219)
    s = f'<rect width="{W}" height="{H}" fill="#3a3028"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 120, True, "dosk"))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#8a7a6a" opacity=".42"/>')
    for i in range(9):
        s += SL(Z_DAL, f'<path d="M{70+i*220:.0f},40 q20,300 0,1000" fill="none"'
                       f' stroke="#9c8a78" stroke-width="14" opacity=".45"/>')
    s += SL(Z_DAL, polovicy(900, "url(#pol)"))
    s += SL(Z_DAL, hodiki(150, 280, t, 1.2))
    # входная дверь справа, обведённая красноватым светом
    dx, dy, dw, dh = 1450, 120, 450, 790
    obv = .4 + .5 * A.ease(A.seg(t, 2.6, 1.2)) * (.6 + .4 * abs(A.w(t, 1.5)))
    dv = dver(dx, dy, dw, dh, 0.0, "#6b5440", True, True)
    dv += (f'<rect x="{dx+dw*.14:.0f}" y="{dy+dh*.08:.0f}" width="{dw*.72:.0f}"'
           f' height="{dh*.34:.0f}" rx="8" fill="none" stroke="#4a382a"'
           f' stroke-width="14"/>')
    dv += (f'<rect x="{dx-16:.0f}" y="{dy-16:.0f}" width="{dw+32:.0f}"'
           f' height="{dh+32:.0f}" rx="10" fill="none" stroke="#c4502e"'
           f' stroke-width="18" opacity="{obv:.2f}"/>')
    dv += (f'<rect x="{dx-36:.0f}" y="{dy-36:.0f}" width="{dw+72:.0f}"'
           f' height="{dh+72:.0f}" rx="12" fill="none" stroke="#e8743c"'
           f' stroke-width="7" opacity="{obv*.6:.2f}"/>')
    mel = A.ease(A.seg(t, 3.4, .8))
    if mel > .02:
        for i in range(3):
            dv += (f'<path d="M{dx+dw*.28+i*58:.0f},{dy-62:.0f} l20,{-48*mel:.0f}'
                   f' l18,{48*mel:.0f}" fill="none" stroke="#f2ecd8"'
                   f' stroke-width="12" opacity="{.9*mel:.2f}"/>')
    s += SL(Z_SRED, dv)
    s += SL(Z_SRED, _podkova_rzh(dx + dw / 2, dy - 120, 1.0, t))
    # тумбочка, ЛАМПА С АБАЖУРОМ и ВАЗА С ВЕТКОЙ — главное
    perevoz = A.ease(A.seg(t, 2.0, 1.6))
    tx, ty = 700, 900
    tum = (f'<rect x="{tx-250:.0f}" y="{ty-300:.0f}" width="500" height="300" rx="10"'
           f' fill="url(#derev)" {o(9)}/>')
    tum += (f'<rect x="{tx-272:.0f}" y="{ty-320:.0f}" width="544" height="28" rx="8"'
            f' fill="{DOSKA}" {o(6)}/>')
    for i in range(2):
        tum += (f'<rect x="{tx-220:.0f}" y="{ty-266+i*132:.0f}" width="440"'
                f' height="116" rx="8" fill="#7d5636" {o(5)}/>')
        tum += (f'<rect x="{tx-40:.0f}" y="{ty-218+i*132:.0f}" width="80" height="18"'
                f' rx="9" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, tum)
    s += SL(Z_SRED, _lampa_abazhur(tx - 190, ty - 318, t, 1.9, 1.0))
    s += SL(Z_SRED, teplo(tx - 190, ty - 520, 820, 700,
                          .52 + .1 * abs(A.w(t, 1.7))))
    vx = tx + 110 + (560 * perevoz)
    vy = ty - 320 - (120 * math.sin(perevoz * 3.14159))
    s += SL(Z_SRED, _vaza(vx, vy, 1.15, t, True))
    # ВЕТКА РЯБИНЫ из вазы — на пол-кадра
    vet = f'<g transform="rotate({1.6*A.w(t,3.2):.2f} {vx:.0f} {vy-340:.0f})">'
    vet += (f'<path d="M{vx:.0f},{vy-340:.0f} q{-30:.0f},{-80:.0f} {-14:.0f},{-200:.0f}"'
            f' fill="none" stroke="#5e4428" stroke-width="22"/>')
    for i in range(6):
        p = i / 5
        bx = vx - 6 - p * 16
        by = vy - 370 - p * 160
        sgn = -1 if i % 2 else 1
        vet += (f'<path d="M{bx:.0f},{by:.0f} q{sgn*80:.0f},{-26:.0f}'
                f' {sgn*160:.0f},{-46:.0f}" fill="none" stroke="#6b5234"'
                f' stroke-width="{13-i}"/>')
        vet += (f'<ellipse cx="{bx+sgn*110:.0f}"'
                f' cy="{by-34+6*A.w(t,2.6,p):.0f}" rx="42" ry="16"'
                f' fill="#7d5a2e" opacity=".92" {o(3)}/>')
    vet += '</g>'
    s += SL(Z_SRED, vet)
    for i in range(5):
        if i > 3:
            continue
        s += SL(Z_SRED, grozd_ryabiny(vx + (-1 if i % 2 else 1) * (120 + i * 12),
                                      vy - 330 - i * 52, t, 1.7, 18, 863 + i,
                                      i * .18))
    # хозяйка справа от вазы, рукав короткий, к гроздьям
    hx = 1230 - perevoz * 60
    s += SL(Z_SRED, figura(hx, 1046, 540, t, "#4a3140", "#ffd98a", True, .3,
                           True, 1.0, False, 1.0))
    ruk, (kx, ky) = rukav(hx - 120, 700, 150, 198 + 14 * A.w(t, 1.2), t,
                          "#4a3140", "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="32" ry="24"'
                    f' fill="#4a3140" {o(5)}/>')
    # тень уходит по лестнице за дверью
    ten_ = A.ease(A.seg(t, 3.0, 1.4))
    s += SL(Z_SRED, f'<path d="M{dx+40:.0f},{dy+dh-40:.0f} l{150:.0f},{-200*ten_:.0f}'
                    f' l{70:.0f},{40:.0f} l{-160:.0f},{210*ten_:.0f} Z"'
                    f' fill="#1a1620" opacity="{.45*(1-ten_*.4):.2f}"/>')
    s += SL(Z_SRED, _veshalka(1060, 200, 330, t, 3, True))
    s += SL(Z_SRED, kot(330, 1012, t, 1.35, "#3b3430", False))
    s += SL(Z_SRED, _valenok(200, 1012, .86, t, .3, False, "#6e6358"))
    s += SL(Z_SRED, _valenok(300, 1012, .82, t, .6, False, "#6e6358"))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="60" height="1080" fill="#241f1a"'
                     f' opacity=".9"/>')
    s += SL(Z_PERED, _chashka(1760, 1012, 1.4, t, .2, KREM, True))
    s += SL(Z_PERED, par(1870, 960, t, 3, .4, 150, .4, .8))
    s += vinetka(.44)
    return s


# ── 73 ─────────────────────────────────────────────────────────────────────
def hozyayka_ugovarivaet_ogon(t):
    """Хозяйка на коленях перед открытой печной дверцей: лицо освещено снизу,
    из устья выглядывает рисованный огонёк с озорной рожицей и косится на трубу."""
    rnd = random.Random(7307)
    s = f'<rect width="{W}" height="{H}" fill="#241a14"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 760, 118))
    s += SL(Z_DAL, f'<rect width="{W}" height="760" fill="#2e2118" opacity=".45"/>')
    s += SL(Z_DAL, polovicy(760, "url(#pol)"))
    s += SL(Z_DAL, utvar_izby(1560, 180, 340, t, 877))
    s += SL(Z_DAL, mebel_hlam(60, 740, 300, t, 881))
    # ПЕЧЬ НА ПОЛ-КАДРА: побелённый массив, шесток, заслонка у стены
    px, py, pw, ph_ = 420, 120, 1120, 740
    pch = (f'<rect x="{px}" y="{py+110}" width="{pw}" height="{ph_-110}" rx="22"'
           f' fill="url(#pech)" {o(10)}/>')
    # свод: русскую печь узнают по горбу над устьём, без него это камин
    pch += (f'<path d="M{px:.0f},{py+130:.0f} q{pw*.5:.0f},{-220:.0f}'
            f' {pw:.0f},0 Z" fill="url(#pech)" {o(10)}/>')
    pch += (f'<path d="M{px+50:.0f},{py+130:.0f} q{pw*.44:.0f},{-170:.0f}'
            f' {pw-100:.0f},0" fill="none" stroke="{PECH2}" stroke-width="12"'
            f' opacity=".8"/>')
    pch += (f'<rect x="{px+40}" y="{py+96}" width="{pw-80}" height="44" rx="12"'
            f' fill="{PECH2}" {o(7)}/>')
    pch += kladka(px + 10, py + 150, pw - 20, ph_ - 170, 92, "url(#pech)")
    pch += (f'<rect x="{px+pw*.60:.0f}" y="{py-130:.0f}" width="{pw*.16:.0f}"'
            f' height="260" rx="8" fill="url(#kamen)" {o(8)}/>')
    pch += (f'<rect x="{px+pw*.57:.0f}" y="{py-150:.0f}" width="{pw*.22:.0f}"'
            f' height="36" rx="8" fill="{KAMEN2}" {o(6)}/>')
    for i in range(5):                   # швы побелки
        pch += (f'<line x1="{px+16}" y1="{py+90+i*132:.0f}" x2="{px+pw-16:.0f}"'
                f' y2="{py+90+i*132:.0f}" stroke="{PECH2}" stroke-width="6"'
                f' opacity=".55"/>')
    pch += (f'<rect x="{px+pw*.62:.0f}" y="{py+ph_*.50:.0f}" width="{pw*.34:.0f}"'
            f' height="{ph_*.34:.0f}" rx="12" fill="{PECH2}" {o(7)}/>')
    s += SL(Z_SRED, pch)
    # устье с дверцей: дверца откинута, за ней угли и огонь
    ux, uy, uw, uh = px + 130, py + 300, 440, 330
    s += SL(Z_SRED, kirpich_ustya(ux, uy, uw, uh, t, True))
    put = kontur_proema(ux, uy, uw, uh, "ustie")
    vn = f'<path d="{put}" fill="#190b05"/>'
    vn += ugli(ux + 40, uy + uh - 36, uw - 80, t, 9, 883)
    vn += ogon(ux + uw * .5, uy + uh - 26, t, 1.45, .1, 7)
    vn += ogon(ux + uw * .24, uy + uh - 20, t, .8, .5, 4)
    for i in range(7):                   # полешки в устье
        vn += (f'<rect x="{ux+36+i*52:.0f}" y="{uy+uh-82+(i%3)*14:.0f}" width="48"'
               f' height="26" rx="12" fill="#4a2f1c" {o(4)}/>')
    s += SL(Z_SRED, vn)
    # ОГОНЁК С РОЖИЦЕЙ выглядывает из устья и косится на трубу
    vyh = A.ease(A.seg(t, .3, .8))
    ustroilsya = A.ease(A.seg(t, 1.7, .7))
    ox_ = ux + uw * .5 + 30 * vyh
    oy_ = uy + uh - 120 - 140 * vyh + 90 * ustroilsya
    kos = 26 * A.ease(A.seg(t, .9, .6)) * (1 - ustroilsya)
    ogl = f'<g transform="translate({kos:.0f},{-kos*.7:.0f})" opacity="{vyh:.2f}">'
    for i in range(3):                   # тельце огонька язычками
        hh = (120 - i * 22) * (1 + .18 * A.w(t, .8, i * .3))
        ogl += (f'<path d="M{ox_-56+i*34:.0f},{oy_+70:.0f}'
                f' q{-30:.0f},{-hh*.5:.0f} {16:.0f},{-hh:.0f}'
                f' q{34:.0f},{hh*.44:.0f} {24:.0f},{hh:.0f} Z"'
                f' fill="{ORA if i != 1 else SVET}" opacity=".92"/>')
    ogl += (f'<ellipse cx="{ox_:.0f}" cy="{oy_:.0f}" rx="86" ry="78" fill="{SVET}"'
            f' {o(5)}/>')
    ogl += (f'<ellipse cx="{ox_:.0f}" cy="{oy_+16:.0f}" rx="62" ry="52" fill="#ffeab8"'
            f' opacity=".85"/>')
    ogl += _rozhica(ox_, oy_ - 6, 64, t, .2, True, "#7d2f10")
    ogl += '</g>'
    s += SL(Z_SRED, ogl)
    s += SL(Z_SRED, teplo(ux + uw * .5, uy + uh * .6, 760, 640,
                          .52 + .14 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, iskra_let(t, ux + uw * .5, uy + uh - 40, 10, 887, 340, .7))
    # заслонка откинута на шестке
    s += SL(Z_SRED, f'<g transform="rotate({-18+6*A.w(t,2.6):.1f} {ux-60:.0f}'
                    f' {uy+uh+40:.0f})">'
                    f'<rect x="{ux-130:.0f}" y="{uy+uh-250:.0f}" width="90"'
                    f' height="290" rx="10" fill="url(#chug)" {o(7)}/>'
                    f'<circle cx="{ux-86:.0f}" cy="{uy+uh-110:.0f}" r="20"'
                    f' fill="url(#zhel)" {o(5)}/></g>')
    # хозяйка на коленях, лицо освещено снизу
    s += SL(Z_SRED, figura(1300, 1030, 470, t, "#4a2f3a", "#ffd98a", True, .25,
                           True, 1.0, False, 2.2))
    s += SL(Z_SRED, teplo(1240, 700, 420, 360, .40 + .1 * abs(A.w(t, 1.4))))
    # щепка подкладывается в устье
    pod = A.ease(A.seg(t, 1.0, .9))
    ruk, (kx, ky) = rukav(1190, 830, 150, 196 + 10 * A.w(t, 1.1), t,
                          "#4a2f3a", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    sx_ = kx - pod * 80
    s += SL(Z_SRED, f'<path d="M{sx_:.0f},{ky:.0f} l-150,-18 l6,22 l150,14 Z"'
                    f' fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="30" ry="22"'
                    f' fill="#4a2f3a" {o(4)}/>')
    # шёпот: три дужки у лица
    for i in range(3):
        k = ((t * .8) + i * .33) % 1.0
        s += SL(Z_SRED, f'<path d="M{1200-k*110:.0f},{690-k*40:.0f} q-26,-20 -8,-46"'
                        f' fill="none" stroke="#ffe6b8" stroke-width="6"'
                        f' opacity="{.5*(1-k):.2f}"/>')
    s += SL(Z_SRED, krynka(1620, 1012, 1.5))
    s += SL(Z_SRED, _chugunok(1700, 1012, 1.1, t))
    s += SL(Z_SRED, kot(300, 1012, t, 1.2, "#3b3430", True))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="150" height="1080" fill="#140f0c"'
                     f' opacity=".92"/>')
    s += SL(Z_LETIT, iskra_let(t, ux + uw * .5, uy + 40, 7, 907, 420, .5))
    s += vinetka(.5)
    return s


def _chugunok(x, y, s_=1.0, t=0.0, par_=False):
    """Чугунок: пузатое чугунное тулово, узкое горло, дуга ушка, блик."""
    w_, hh = 84 * s_, 100 * s_
    s = ten(x, y + 6 * s_, w_ * .8, 11 * s_, .45)
    s += (f'<path d="M{x-w_*.34:.0f},{y-hh:.0f} q{-w_*.56:.0f},{hh*.30:.0f}'
          f' {-w_*.30:.0f},{hh*.68:.0f} q{w_*.22:.0f},{hh*.34:.0f} {w_*.64:.0f},{hh*.32:.0f}'
          f' q{w_*.64:.0f},{hh*.02:.0f} {w_*.64:.0f},{-hh*.32:.0f}'
          f' q{w_*.26:.0f},{-hh*.38:.0f} {-w_*.30:.0f},{-hh*.68:.0f} Z"'
          f' fill="url(#chug)" {o(max(3, 6*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*.34:.0f}" ry="{10*s_:.0f}"'
          f' fill="#1d1b1a" {o(max(2, 4*s_))}/>')
    s += (f'<path d="M{x-w_*.72:.0f},{y-hh*.56:.0f} q{w_*.10:.0f},{-hh*.22:.0f}'
          f' {w_*.26:.0f},{-hh*.06:.0f}" fill="none" stroke="#6b6a68"'
          f' stroke-width="{max(3, 7*s_):.0f}"/>')
    s += (f'<path d="M{x-w_*.56:.0f},{y-hh*.46:.0f} q{w_*.08:.0f},{hh*.26:.0f}'
          f' {w_*.02:.0f},{hh*.42:.0f}" fill="none" stroke="#9aa0a6"'
          f' stroke-width="{max(3, 9*s_):.0f}"'
          f' opacity="{.22+.2*abs(A.w(t,2.6,x*.002)):.2f}"/>')
    if par_:
        s += par(x, y - hh - 10 * s_, t, 4, .5, 150 * s_, .4, .9)
    return s


def _ohvat(x, y, s_=1.0, t=0.0):
    """Ухват: длинная рукоять и железная дуга-рога. Стоит у печи, подрагивает."""
    ug = 4.0 + 2.0 * A.w(t, 3.4, x * .001)
    s = f'<g transform="rotate({ug:.2f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-12*s_:.0f}" y="{y-620*s_:.0f}" width="{24*s_:.0f}"'
          f' height="{620*s_:.0f}" rx="{10*s_:.0f}" fill="url(#derev)" {o(6)}/>')
    s += (f'<path d="M{x-66*s_:.0f},{y-660*s_:.0f} q{66*s_:.0f},{70*s_:.0f}'
          f' {132*s_:.0f},0" fill="none" stroke="#5d6168"'
          f' stroke-width="{18*s_:.0f}" stroke-linecap="round"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*66*s_:.0f},{y-660*s_:.0f} q{i*18*s_:.0f},{-56*s_:.0f}'
              f' {i*4*s_:.0f},{-96*s_:.0f}" fill="none" stroke="#5d6168"'
              f' stroke-width="{15*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<circle cx="{x-30*s_:.0f}" cy="{y-640*s_:.0f}" r="{8*s_:.0f}"'
          f' fill="#e8f1f8" opacity="{.3+.3*abs(A.w(t,2.2)):.2f}"/>')
    return s + '</g>'


# ── 74 ─────────────────────────────────────────────────────────────────────
def luchina_v_svetce(t):
    """Тёмная изба: посреди неё высокая кованая стойка-светец на пол-кадра,
    в её развилке горит лучина, под ней корытце с водой. Рядом полено, от
    которого ножом откалывают длинную тонкую щепку."""
    rnd = random.Random(7411)
    s = f'<rect width="{W}" height="{H}" fill="#241a18"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 820, 122))
    s += SL(Z_DAL, f'<rect width="{W}" height="820" fill="#3f2d20" opacity=".4"/>')
    s += SL(Z_DAL, polovicy(820, "#6b4a2a"))
    s += SL(Z_DAL, utvar_izby(70, 200, 380, t, 911))
    s += SL(Z_DAL, okno_izby(1540, 190, 330, 270, t, moroz=.5))
    # печь справа с углями — заполняет пустое поле и греет кадр
    s += SL(Z_SRED, pech(1440, 440, 480, 480, t, True, True, False))
    s += SL(Z_SRED, kirpich_ustya(1520, 640, 240, 180, t, True))
    put2 = kontur_proema(1520, 640, 240, 180, "ustie")
    s += SL(Z_SRED, f'<path d="{put2}" fill="#190b05"/>'
                    + ugli(1544, 790, 200, t, 7, 913)
                    + ogon(1640, 798, t, .8, .3, 5))
    s += SL(Z_SRED, teplo(1640, 740, 520, 440, .34 + .1 * abs(A.w(t, 1.7))))
    # СВЕТЕЦ НА ПОЛ-КАДРА в центре
    sx, sy = 900, 1030
    s += SL(Z_SRED, _svetec(sx, sy, 470, t, 2.1, True))
    razg = A.ease(A.seg(t, 1.0, 1.1))
    lx, ly = sx, sy - 470
    s += SL(Z_SRED, _luchina_v_razvilke(lx, ly - 76, t, 1.45, razg, .1))
    s += SL(Z_SRED, teplo(lx + 160, ly - 290, 880 * razg + 200,
                          760 * razg + 180, .54 * razg + .12))
    s += SL(Z_SRED, iskra_let(t, lx + 170, ly - 300, 10, 919, 400, .9))
    kr = 300 + 520 * razg
    s += SL(Z_SRED, f'<ellipse cx="{sx:.0f}" cy="1016" rx="{kr:.0f}"'
                    f' ry="{kr*.26:.0f}" fill="url(#teplo)"'
                    f' opacity="{.34*razg+.12:.2f}"/>')
    for i in range(3):                   # уголёк падает с лучины в корытце
        k = ((t * .55) + i * .34) % 1.0
        s += SL(Z_SRED, f'<circle cx="{lx+168-150*k+8*A.w(t,1.6,i*.3):.0f}"'
                        f' cy="{ly-290+k*(sy-320-(ly-290)):.0f}"'
                        f' r="{9-3*k:.1f}" fill="{ORA}"'
                        f' opacity="{.95*(1-k*.5):.2f}"/>')
    # ПОЛЕНО И НОЖ крупно на переднем плане
    pol_x, pol_y = 420, 1010
    pln = (f'<rect x="{pol_x-230:.0f}" y="{pol_y-190:.0f}" width="460"'
           f' height="196" rx="90" fill="#f2ece0" {o(9)}/>')
    for i in range(5):
        pln += (f'<path d="M{pol_x-170+i*96:.0f},{pol_y-168:.0f} l0,52"'
                f' stroke="#2f2a26" stroke-width="13" stroke-linecap="round"'
                f' opacity=".88"/>')
        pln += (f'<path d="M{pol_x-150+i*96:.0f},{pol_y-86:.0f} l0,34"'
                f' stroke="#2f2a26" stroke-width="11" stroke-linecap="round"'
                f' opacity=".7"/>')
    pln += (f'<ellipse cx="{pol_x+230:.0f}" cy="{pol_y-92:.0f}" rx="40" ry="98"'
            f' fill="#d8b98a" {o(6)}/>')
    pln += (f'<ellipse cx="{pol_x+230:.0f}" cy="{pol_y-92:.0f}" rx="19" ry="52"'
            f' fill="#a9823f" opacity=".85"/>')
    s += SL(Z_SRED, pln)
    nozh = A.ease(A.seg(t, .2, .9))
    nx = pol_x - 180 + nozh * 340
    s += SL(Z_SRED, f'<g transform="rotate({-10+5*A.w(t,1.4):.1f} {nx:.0f}'
                    f' {pol_y-240:.0f})">'
                    f'<rect x="{nx-20:.0f}" y="{pol_y-370:.0f}" width="40"'
                    f' height="176" rx="8" fill="#cfd6dc" {o(5)}/>'
                    f'<rect x="{nx-28:.0f}" y="{pol_y-400:.0f}" width="56"'
                    f' height="44" rx="10" fill="#6b4a2a" {o(5)}/>'
                    f'<line x1="{nx+12:.0f}" y1="{pol_y-362:.0f}" x2="{nx+12:.0f}"'
                    f' y2="{pol_y-206:.0f}" stroke="#ffffff" stroke-width="8"'
                    f' opacity="{.3+.3*abs(A.w(t,2.0)):.2f}"/></g>')
    s += SL(Z_SRED, f'<path d="M{pol_x-210:.0f},{pol_y-196:.0f}'
                    f' l{300*nozh:.0f},{-22*nozh:.0f} l0,24 l{-300*nozh:.0f},'
                    f'{16*nozh:.0f} Z" fill="#f8f0dc" opacity=".96" {o(4)}/>')
    for i in range(12):                  # стружка летит
        k = ((t * .8) + i * .085) % 1.0
        s += SL(Z_LETIT, f'<path d="M{pol_x-120+i*40+k*70:.0f},'
                         f'{pol_y-200+k*150:.0f} q16,-14 30,2" fill="none"'
                         f' stroke="#f2e8d4" stroke-width="6"'
                         f' opacity="{.85*(1-k):.2f}"/>')
    s += SL(Z_SRED, figura(250, 1070, 520, t, "#453a4a", "#ffd98a", False, .4,
                           True, 1.0, False, 1.4, True))
    ruk, _ = rukav(330, 740, 170, 42, t, "#453a4a", "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, lavka(1180, 920, 300))
    s += SL(Z_SRED, figura(1300, 920, 320, t, "#4a4450", "#ffd98a", True, .7,
                           True, .95))
    s += SL(Z_SRED, krynka(1760, 1012, 1.7))
    s += SL(Z_SRED, _chugunok(1120, 1012, 1.3, t, True))
    s += SL(Z_PERED, f'<rect x="1840" y="0" width="100" height="1080"'
                     f' fill="url(#brev)" {o(9)}/>')
    s += SL(Z_PERED, ramka_pp("levo", "#1a120e", .78))
    s += vinetka(.48)
    return s


# ── 75 ─────────────────────────────────────────────────────────────────────
def semya_prosit_svetec(t):
    """Семья полукругом перед светцом: дед впереди кланяется ему в пояс и
    грозит пальцем, а в светлое окно просовывается тонкая чёрная лапа тени и
    тянется к огоньку лучины."""
    rnd = random.Random(7517)
    s = f'<rect width="{W}" height="{H}" fill="#241c20"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 800, 120))
    s += SL(Z_DAL, f'<rect width="{W}" height="800" fill="#3a2b24" opacity=".42"/>')
    s += SL(Z_DAL, polovicy(800, "#6b4a2a"))
    s += SL(Z_DAL, utvar_izby(70, 190, 300, t, 929))
    # окно СВЕТЛОЕ, чтобы чёрная лапа тени читалась
    okx, oky, okw, okh = 1240, 170, 460, 380
    vid = (f'<rect x="{okx}" y="{oky}" width="{okw}" height="{okh}"'
           f' fill="#8fa8c4"/>')
    vid += (f'<rect x="{okx}" y="{oky+okh*.56:.0f}" width="{okw}"'
            f' height="{okh*.44:.0f}" fill="#7892ad"/>')
    for i in range(3):
        bx = okx + 40 + i * 150
        vid += (f'<rect x="{bx:.0f}" y="{oky+okh*.48:.0f}" width="110"'
                f' height="{okh*.3:.0f}" fill="#64809c" opacity=".9"/>')
        vid += (f'<path d="M{bx-16:.0f},{oky+okh*.48:.0f} l71,-54 l71,54 Z"'
                f' fill="#5a768f" opacity=".92"/>')
    vid += (f'<circle cx="{okx+okw*.78:.0f}" cy="{oky+okh*.22:.0f}" r="46"'
            f' fill="#eef5fb" opacity=".9"/>')
    for i in range(14):
        vid += (f'<circle cx="{okx+rnd.random()*okw:.0f}"'
                f' cy="{oky+rnd.random()*okh:.0f}" r="{rnd.uniform(3,7):.1f}"'
                f' fill="#f2f8ff"'
                f' opacity="{.5+.4*abs(A.w(t,2.6+i*.2,i*.1)):.2f}"/>')
    s += SL(Z_SRED, okno_izby(okx, oky, okw, okh, t, vid, .12, False, True))
    # ЛАПА ТЕНИ: чёрная, толстая, тянется из окна к огоньку
    lapa = A.ease(A.seg(t, 1.0, 1.8))
    lp = ""
    if lapa > .03:
        lp += (f'<path d="M{okx+okw*.42:.0f},{oky+okh*.46:.0f}'
               f' q{-160*lapa:.0f},{110*lapa:.0f} {-400*lapa:.0f},{190*lapa:.0f}"'
               f' fill="none" stroke="#0d0a10" stroke-width="{44*lapa+8:.0f}"'
               f' stroke-linecap="round" opacity=".95"/>')
        ex = okx + okw * .42 - 400 * lapa
        ey = oky + okh * .46 + 190 * lapa
        for i in range(4):               # когти лапы
            a = -.75 + i * .42
            lp += (f'<path d="M{ex:.0f},{ey:.0f} q{-70*lapa:.0f},'
                   f'{math.sin(a)*70*lapa:.0f} {-130*lapa:.0f},'
                   f'{math.sin(a)*112*lapa:.0f}" fill="none" stroke="#0d0a10"'
                   f' stroke-width="{24-i*3:.0f}" stroke-linecap="round"'
                   f' opacity=".95"/>')
        lp += (f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{54*lapa:.0f}"'
               f' ry="{40*lapa:.0f}" fill="#0d0a10" opacity=".95"/>')
    s += SL(Z_SRED, lp)
    # СВЕТЕЦ большой в центре, лучина вспыхивает
    sx, sy = 820, 1020
    s += SL(Z_SRED, _svetec(sx, sy, 450, t, 1.9, True))
    vsp = .6 + .4 * A.ease(A.seg(t, 2.6, .5)) + .18 * abs(A.w(t, 1.1))
    lx, ly = sx, sy - 450
    s += SL(Z_SRED, _luchina_v_razvilke(lx, ly - 72, t, 1.4, vsp, .2))
    s += SL(Z_SRED, teplo(lx + 150, ly - 280, 900 * vsp, 780 * vsp, .52 * vsp))
    s += SL(Z_SRED, iskra_let(t, lx + 160, ly - 290, 10, 937, 420, .9))
    s += SL(Z_SRED, f'<ellipse cx="{sx:.0f}" cy="1006" rx="{600*vsp:.0f}"'
                    f' ry="{160*vsp:.0f}" fill="url(#teplo)"'
                    f' opacity="{.3*vsp:.2f}"/>')
    # дед кланяется в пояс и грозит пальцем — крупно, слева
    pokl = A.ease(A.seg(t, .4, 1.2)) * (1 - A.ease(A.seg(t, 2.4, .9)))
    gx = 420
    s += SL(Z_SRED, figura(gx, 1066, 600, t, "#2f2a36", "#ffd98a", False, .2,
                           True, 1.0, False, 2.0 + 20 * pokl, True))
    ruk, (kx, ky) = rukav(gx + 120, 676 + pokl * 120, 200,
                          -54 - 20 * A.w(t, .9), t, "#2f2a36", "#ffd98a", .3, 8.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{ky:.0f} l{10:.0f},{-80:.0f}"'
                    f' stroke="#2f2a36" stroke-width="28" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx+12:.0f}" cy="{ky-92:.0f}" rx="18" ry="26"'
                    f' fill="#f0cfae" {o(4)}/>')
    # три фигуры семьи справа, с интервалом
    for i, (fx_, h_, col, pl, bo) in enumerate((
            (1200, 480, "#4a2f3a", True, False),
            (1480, 430, "#2e4a5a", True, False),
            (1740, 360, "#5b3f2a", False, False))):
        s += SL(Z_SRED, figura(fx_, 1058 + i * 8, h_, t, col, "#ffd98a", pl,
                               .2 * i, True, 1.0, False, 1.0, bo))
    s += SL(Z_SRED, lavka(1180, 940, 440))
    s += SL(Z_SRED, _lampa_abazhur(170, 700, t, 1.5, 1.0))
    s += SL(Z_SRED, teplo(170, 540, 640, 540, .42 + .1 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, kot(330, 1012, t, 1.3, "#3b3430", False))
    s += SL(Z_SRED, krynka(170, 1012, 1.5))
    s += SL(Z_SRED, _chugunok(600, 1012, 1.2, t, True))
    s += SL(Z_PERED, ramka_pp("pravo", "#16111a", .8))
    s += vinetka(.48)
    return s


# ── 76 ─────────────────────────────────────────────────────────────────────
def vecher_pochinki_zimnego(t):
    """Изба в свете открытой печи, всё зимнее вытащено наружу: мать выбивает
    тулуп прутом на верёвке, рукавицы сушатся на шестке, отец пришивает к
    валенку кожаную заплату, малыш сидит в огромной шапке, съехавшей на нос."""
    rnd = random.Random(7619)
    s = f'<rect width="{W}" height="{H}" fill="#2a2018"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 800, 116))
    s += SL(Z_DAL, f'<rect width="{W}" height="800" fill="#45321f" opacity=".4"/>')
    s += SL(Z_DAL, polovicy(800, "url(#pol)"))
    s += SL(Z_DAL, utvar_izby(1680, 170, 230, t, 941))
    # ПЕЧЬ слева с ОТКРЫТЫМ устьём — тёплое пятно сцены
    s += SL(Z_SRED, pech(10, 250, 440, 560, t, True, True, False))
    ux, uy, uw, uh = 60, 470, 250, 210
    s += SL(Z_SRED, kirpich_ustya(ux, uy, uw, uh, t, True))
    put = kontur_proema(ux, uy, uw, uh, "ustie")
    s += SL(Z_SRED, f'<path d="{put}" fill="#190b05"/>'
                    + ugli(ux + 28, uy + uh - 28, uw - 56, t, 8, 943)
                    + ogon(ux + uw * .5, uy + uh - 22, t, 1.15, .1, 6))
    s += SL(Z_SRED, teplo(ux + uw * .5, uy + uh * .6, 700, 600,
                          .52 + .12 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, iskra_let(t, ux + uw * .5, uy + uh - 40, 9, 953, 340, .7))
    # рукавицы сушатся на шестке над устьём
    s += SL(Z_SRED, f'<rect x="{ux-40:.0f}" y="{uy-70:.0f}" width="{uw+90:.0f}"'
                    f' height="26" rx="8" fill="url(#chug)" {o(5)}/>')
    for i, px in ((0, ux + 60), (1, ux + 220)):
        s += SL(Z_SRED, _varezhka(px, uy - 46, 1.15, t, .2 + i * .4, TKAN, True))
        s += SL(Z_SRED, par(px, uy - 150, t, 3, .45, 160, .5, .7))
    # ТУЛУП НА ВЕРЁВКЕ в центре, его выбивают прутом
    s += SL(Z_SRED, f'<path d="M900,230 q380,60 760,-10" fill="none"'
                    f' stroke="#c2ab86" stroke-width="9"/>')
    udar = max(0.0, A.w(t, 1.1, .1))
    s += SL(Z_SRED, _tulup_vis(1200, 250, 470, 600, t, .2, udar))
    for i in range(12):                  # пыль вылетает от удара
        k = ((t * 1.0) + i * .085) % 1.0
        s += SL(Z_SRED, f'<circle cx="{1200+rnd.uniform(-200,200)+k*140:.0f}"'
                        f' cy="{520+rnd.uniform(-140,140)-k*100:.0f}"'
                        f' r="{7+12*k:.0f}" fill="#e4d6bc"'
                        f' opacity="{.5*(1-k)*udar:.2f}"/>')
    prut = -36 + 56 * udar
    s += SL(Z_SRED, f'<g transform="rotate({prut:.1f} 1620 620)">'
                    f'<path d="M1620,620 q100,-96 230,-152" fill="none"'
                    f' stroke="url(#derev)" stroke-width="20"'
                    f' stroke-linecap="round"/>'
                    f'<path d="M1842,470 q34,-18 60,-4" fill="none"'
                    f' stroke="#8a6238" stroke-width="12"'
                    f' stroke-linecap="round"/></g>')
    if udar > .85:
        for i in range(5):
            a = -2.4 + i * .5
            s += SL(Z_SRED, f'<line x1="1420" y1="520"'
                            f' x2="{1420+math.cos(a)*70:.0f}"'
                            f' y2="{520+math.sin(a)*70:.0f}" stroke="#ffe6b8"'
                            f' stroke-width="7" opacity=".6"/>')
    s += SL(Z_SRED, figura(1700, 1046, 520, t, "#4a2f3a", "#ffd98a", True, .3,
                           True, 1.0, False, 1.6))
    ruk, _ = rukav(1660, 710, 150, -40 + 30 * udar, t, "#4a2f3a", "#ffd98a",
                   .1, 6.0)
    s += SL(Z_SRED, ruk)
    # отец и БОЛЬШОЙ ВАЛЕНОК С ЗАПЛАТОЙ справа внизу
    s += SL(Z_SRED, lavka(460, 930, 360))
    s += SL(Z_SRED, figura(540, 930, 400, t, "#3a3346", "#ffd98a", False, .5,
                           True, 1.0, False, 1.0, True))
    vx_, vy_ = 800, 1046
    s += SL(Z_SRED, _valenok(vx_, vy_, 2.6, t, .3, False, "#bda98a", -10))
    zap = (f'M{vx_-60:.0f},{vy_-400:.0f} q100,-40 184,22'
           f' q-16,110 -172,86 Z')
    s += SL(Z_SRED, f'<path d="{zap}" fill="#b5803a" {o(8)}/>')
    s += SL(Z_SRED, f'<path d="{zap}" fill="none" stroke="#f2e8d4"'
                    f' stroke-width="7" stroke-dasharray="16 14"/>')
    dra = A.w(t, .7, .2)
    ruk2, (dx_, dy_) = rukav(620, 790, 150, 26 + 24 * dra, t, "#3a3346",
                             "#ffd98a", .3, 6.0)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, f'<line x1="{dx_:.0f}" y1="{dy_:.0f}" x2="{vx_+40:.0f}"'
                    f' y2="{vy_-300:.0f}" stroke="#e2d6bc" stroke-width="6"'
                    f' opacity=".9"/>')
    for i in range(5):                   # стежки по заплате
        st = A.ease(A.seg(t, .6 + i * .3, .3))
        if st > .02:
            s += SL(Z_SRED, f'<line x1="{vx_+48+i*28:.0f}" y1="{vy_-322+i*12:.0f}"'
                            f' x2="{vx_+64+i*28:.0f}" y2="{vy_-280+i*12:.0f}"'
                            f' stroke="#f8f0dc" stroke-width="8"'
                            f' opacity="{.9*st:.2f}"/>')
    # малыш в огромной шапке, съехавшей на нос
    mx, my = 1640, 1046
    s += SL(Z_SRED, figura(mx, my, 300, t, "#6b3a44", "#ffd98a", False, .8,
                           False, 1.0, False, 1.2, False, False))
    sdv = 30 * A.ease(A.seg(t, 1.4, .8))
    s += SL(Z_SRED, _shapka_meh(mx, my - 244 + sdv, 1.7, t, .4, 0.0))
    s += SL(Z_SRED, para_izo_rta(mx + 48, my - 224 + sdv, t, .5, .9, .45))
    s += SL(Z_SRED, _valenok(420, 1012, 1.0, t, .1, True, "#6e6358"))
    s += SL(Z_SRED, _chugunok(300, 1012, 1.2, t, True))
    s += SL(Z_PERED, ramka_pp("pravo", "#1a120c", .76))
    s += SL(Z_PERED, _shapka_meh(170, 1012, 1.5, t, .2, 0.0))
    s += vinetka(.46)
    return s


def _lampa_abazhur(x, y, t, s_=1.0, zazh=1.0):
    """Настольная лампа под абажуром: кремово-зелёный конус абажура с бахромой,
    точёная ножка, круглое основание и тёплый шар света под абажуром.
    `baza.lampa(abazhur=True)` даёт красную трапецию и читалась шторой."""
    w_, hh = 140 * s_, 230 * s_
    s = ten(x, y + 8 * s_, w_ * .46, 12 * s_, .42)
    s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_*.40:.0f}" ry="{14*s_:.0f}"'
          f' fill="url(#med)" {o(max(3, 5*s_))}/>')
    s += (f'<path d="M{x-12*s_:.0f},{y-6*s_:.0f} q{-8*s_:.0f},{-hh*.30:.0f}'
          f' {4*s_:.0f},{-hh*.46:.0f} l{16*s_:.0f},0'
          f' q{12*s_:.0f},{hh*.16:.0f} {4*s_:.0f},{hh*.46:.0f} Z"'
          f' fill="url(#med)" {o(max(3, 4*s_))}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh*.48:.0f}" rx="{22*s_:.0f}"'
          f' ry="{10*s_:.0f}" fill="#b5803a" {o(max(2, 3*s_))}/>')
    if zazh > .02:                       # шар света под абажуром
        s += teplo(x, y - hh * .58, 230 * s_ * zazh, 190 * s_ * zazh, .62 * zazh)
        s += (f'<circle cx="{x:.0f}" cy="{y-hh*.60:.0f}" r="{26*s_:.0f}"'
              f' fill="{SVET}" opacity="{(.6+.3*abs(A.w(t,1.6)))*zazh:.2f}"/>')
    s += (f'<path d="M{x-w_*.5:.0f},{y-hh*.56:.0f} L{x-w_*.24:.0f},{y-hh*.98:.0f}'
          f' L{x+w_*.24:.0f},{y-hh*.98:.0f} L{x+w_*.5:.0f},{y-hh*.56:.0f} Z"'
          f' fill="#e8dfae" {o(max(4, 6*s_))}/>')
    s += (f'<path d="M{x-w_*.44:.0f},{y-hh*.63:.0f} L{x-w_*.22:.0f},{y-hh*.94:.0f}'
          f' L{x+w_*.22:.0f},{y-hh*.94:.0f} L{x+w_*.44:.0f},{y-hh*.63:.0f} Z"'
          f' fill="#f4ecc8" opacity=".75"/>')
    for i in range(9):                   # бахрома по краю абажура
        xx = x - w_ * .48 + i * w_ * .12
        s += (f'<path d="M{xx:.0f},{y-hh*.56:.0f} q{3*s_:.0f},{18*s_:.0f}'
              f' {-2*s_+2*A.w(t,2.4,i*.2):.0f},{30*s_:.0f}" fill="none"'
              f' stroke="#d8cb92" stroke-width="{max(3, 6*s_):.0f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh*.98:.0f}" rx="{w_*.24:.0f}"'
          f' ry="{9*s_:.0f}" fill="#d8cb92" {o(max(2, 4*s_))}/>')
    return s


def _gruzovichok(x, y, s_=1.0, t=0.0):
    """Пузатый фургончик: капот, кабина с окном, высокий кузов, два колеса со
    спицами, бампер и круглая фара. Прежнее одно пятно читалось диваном."""
    w_, hh = 420 * s_, 200 * s_
    rot = (t * 40) % 360
    s = ten(x, y + 10 * s_, w_ * .52, 18 * s_, .5)
    # кузов-фургон
    s += (f'<rect x="{x-w_*.52:.0f}" y="{y-hh*1.45:.0f}" width="{w_*.62:.0f}"'
          f' height="{hh*1.25:.0f}" rx="{14*s_:.0f}" fill="#3f5c7a" {o(max(4, 8*s_))}/>')
    for i in range(4):                   # доски борта
        s += (f'<line x1="{x-w_*.48+i*w_*.15:.0f}" y1="{y-hh*1.40:.0f}"'
              f' x2="{x-w_*.48+i*w_*.15:.0f}" y2="{y-hh*.26:.0f}"'
              f' stroke="#324c66" stroke-width="{max(3, 8*s_):.0f}"/>')
    # кабина
    s += (f'<path d="M{x+w_*.10:.0f},{y-hh*1.45:.0f} h{w_*.30:.0f}'
          f' q{w_*.10:.0f},{hh*.10:.0f} {w_*.12:.0f},{hh*.52:.0f}'
          f' l0,{hh*.57:.0f} h{-w_*.52:.0f} Z" fill="#4a6a8a" {o(max(4, 7*s_))}/>')
    s += (f'<path d="M{x+w_*.16:.0f},{y-hh*1.34:.0f} h{w_*.22:.0f}'
          f' q{w_*.08:.0f},{hh*.06:.0f} {w_*.09:.0f},{hh*.38:.0f}'
          f' h{-w_*.31:.0f} Z" fill="url(#stekl)" opacity=".8" {o(max(3, 5*s_))}/>')
    # капот
    s += (f'<path d="M{x+w_*.40:.0f},{y-hh*.84:.0f} q{w_*.16:.0f},{hh*.04:.0f}'
          f' {w_*.17:.0f},{hh*.30:.0f} l0,{hh*.26:.0f} h{-w_*.17:.0f} Z"'
          f' fill="#3f5c7a" {o(max(4, 6*s_))}/>')
    s += (f'<rect x="{x+w_*.40:.0f}" y="{y-hh*.56:.0f}" width="{w_*.17:.0f}"'
          f' height="{hh*.18:.0f}" rx="{5*s_:.0f}" fill="#2a3c50" {o(max(2, 4*s_))}/>')
    s += (f'<circle cx="{x+w_*.52:.0f}" cy="{y-hh*.66:.0f}" r="{22*s_:.0f}"'
          f' fill="url(#zhel)" {o(max(3, 5*s_))}/>')
    s += (f'<circle cx="{x+w_*.52:.0f}" cy="{y-hh*.66:.0f}" r="{12*s_:.0f}"'
          f' fill="{SVET}" opacity="{.55+.35*abs(A.w(t,1.9)):.2f}"/>')
    s += (f'<rect x="{x-w_*.56:.0f}" y="{y-hh*.26:.0f}" width="{w_*1.16:.0f}"'
          f' height="{hh*.12:.0f}" rx="{7*s_:.0f}" fill="#2a3c50" {o(max(3, 5*s_))}/>')
    for sgn in (-1, 1):                  # два колеса со спицами
        wx = x + sgn * w_ * .33
        s += (f'<circle cx="{wx:.0f}" cy="{y-hh*.10:.0f}" r="{58*s_:.0f}"'
              f' fill="#23262a" {o(max(4, 7*s_))}/>')
        s += (f'<circle cx="{wx:.0f}" cy="{y-hh*.10:.0f}" r="{28*s_:.0f}"'
              f' fill="#9aa1a8" {o(max(3, 4*s_))}/>')
        s += f'<g transform="rotate({rot:.0f} {wx:.0f} {y-hh*.10:.0f})">'
        for j in range(4):
            a = j * .7854
            s += (f'<line x1="{wx-math.cos(a)*24*s_:.0f}"'
                  f' y1="{y-hh*.10-math.sin(a)*24*s_:.0f}"'
                  f' x2="{wx+math.cos(a)*24*s_:.0f}"'
                  f' y2="{y-hh*.10+math.sin(a)*24*s_:.0f}" stroke="#5d6168"'
                  f' stroke-width="{max(3, 6*s_):.0f}"/>')
        s += '</g>'
    return s


def _gazeta_list(x, y, w_, h_, t, ug=0.0, seed=3, komok=0.0):
    """Газетный лист: серая полоса фотографии и волнистые строки, без букв.
    `komok` сминает лист в комок — им набивают ботинок."""
    rnd = random.Random(seed)
    k = komok
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    if k < .55:
        s += (f'<rect x="{x-w_/2:.0f}" y="{y-h_/2:.0f}" width="{w_:.0f}"'
              f' height="{h_:.0f}" rx="3" fill="url(#list)" opacity="{1-k*1.4:.2f}"'
              f' {o(4)}/>')
        s += (f'<rect x="{x-w_*.44:.0f}" y="{y-h_*.38:.0f}" width="{w_*.34:.0f}"'
              f' height="{h_*.30:.0f}" fill="#8f979c" opacity="{.8*(1-k*1.4):.2f}"/>')
        for i in range(8):
            yy = y - h_ * .32 + i * h_ * .09
            s += (f'<path d="M{x-w_*.06:.0f},{yy:.0f} q{w_*.12:.0f},'
                  f'{rnd.uniform(-4,4):.1f} {w_*.46:.0f},0" fill="none"'
                  f' stroke="#6b645c" stroke-width="4"'
                  f' opacity="{.85*(1-k*1.4):.2f}"/>')
        for i in range(5):
            yy = y + h_ * .08 + i * h_ * .08
            s += (f'<path d="M{x-w_*.44:.0f},{yy:.0f} q{w_*.22:.0f},'
                  f'{rnd.uniform(-3,3):.1f} {w_*.88:.0f},0" fill="none"'
                  f' stroke="#6b645c" stroke-width="4"'
                  f' opacity="{.8*(1-k*1.4):.2f}"/>')
        s += (f'<line x1="{x:.0f}" y1="{y-h_/2:.0f}" x2="{x:.0f}" y2="{y+h_/2:.0f}"'
              f' stroke="#b8ae9a" stroke-width="3" opacity="{.8*(1-k*1.4):.2f}"/>')
    if k > .1:                           # комок: мятые дольки
        rr = (w_ * .22) * min(1.0, k * 1.5)
        s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="url(#list)"'
              f' opacity="{min(1.0, k*1.6):.2f}" {o(4)}/>')
        for i in range(9):
            a = i * .7
            s += (f'<path d="M{x+math.cos(a)*rr*.3:.0f},{y+math.sin(a)*rr*.3:.0f}'
                  f' q{math.cos(a)*rr*.5:.0f},{math.sin(a)*rr*.3:.0f}'
                  f' {math.cos(a)*rr*.95:.0f},{math.sin(a)*rr*.9:.0f}" fill="none"'
                  f' stroke="#c3b89c" stroke-width="5"'
                  f' opacity="{min(1.0, k*1.4):.2f}"/>')
    return s + '</g>'


def _shchetka(x, y, s_=1.0, t=0.0, ug=0.0):
    """Сапожная щётка: деревянная колодка и густая щетина."""
    w_, hh = 150 * s_, 40 * s_
    s = f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-hh:.0f}" width="{w_:.0f}" height="{hh:.0f}"'
          f' rx="{hh*.4:.0f}" fill="url(#derev)" {o(max(3, 5*s_))}/>')
    for i in range(16):
        xx = x - w_ * .46 + i * (w_ * .92 / 15)
        s += (f'<line x1="{xx:.0f}" y1="{y:.0f}" x2="{xx+2*A.w(t,1.4,i*.1):.0f}"'
              f' y2="{y+hh*.62:.0f}" stroke="#4a3a28"'
              f' stroke-width="{max(2, 5*s_):.0f}"/>')
    s += (f'<path d="M{x-w_*.3:.0f},{y-hh*.64:.0f} q{w_*.3:.0f},{-hh*.2:.0f}'
          f' {w_*.6:.0f},0" fill="none" stroke="#c9a771"'
          f' stroke-width="{max(2, 5*s_):.0f}" opacity=".6"/>')
    return s + '</g>'


# ── 77 ─────────────────────────────────────────────────────────────────────
def ded_pletet_vozhzhi(t):
    """Дед на лавке плетёт из трёх толстых кожаных полос косу: один конец
    зажат в зубах, другой на крюке в стене. Внук держит готовый конец и
    правит понарошку — над лавкой стоит рисованная лошадка и ждёт вожжей."""
    rnd = random.Random(7723)
    s = f'<rect width="{W}" height="{H}" fill="#2e2318"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 840, 118))
    s += SL(Z_DAL, f'<rect width="{W}" height="840" fill="#4a3620" opacity=".38"/>')
    s += SL(Z_DAL, polovicy(840, "url(#pol)"))
    s += SL(Z_DAL, utvar_izby(80, 180, 300, t, 971))
    s += SL(Z_SRED, svecha(1830, 700, t, .3, 1.6, 110))
    s += SL(Z_SRED, teplo(1830, 660, 420, 360, .3 + .1 * abs(A.w(t, 1.7))))
    s += SL(Z_SRED, lampa(560, 250, t, 1.3, False))
    s += SL(Z_SRED, teplo(560, 290, 860, 720, .46 + .1 * abs(A.w(t, 1.4))))
    # крюк в стене — от него идёт коса
    kx_, ky_ = 500, 620
    s += SL(Z_SRED, f'<rect x="{kx_-52:.0f}" y="{ky_-60:.0f}" width="104"'
                    f' height="112" rx="12" fill="#6b7278" {o(6)}/>')
    for i in (-1, 1):                    # шляпки гвоздей на пластине крюка
        s += SL(Z_SRED, f'<circle cx="{kx_+i*32:.0f}" cy="{ky_-32:.0f}" r="10"'
                        f' fill="#cfd6dc" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{kx_:.0f},{ky_+50:.0f} q70,60 6,122" fill="none"'
                    f' stroke="#9aa1a8" stroke-width="30" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M{kx_:.0f},{ky_+50:.0f} q70,60 6,122" fill="none"'
                    f' stroke="#e8eef6" stroke-width="7" opacity=".4"/>')
    s += SL(Z_SRED, lavka(700, 930, 620))
    # ДЕД крупно на лавке
    gx = 980
    s += SL(Z_SRED, figura(gx, 930, 520, t, "#3a3040", "#ffd98a", False, .2,
                           True, 1.0, False, 1.2, True))
    # КОСА ИЗ ТРЁХ ПОЛОС: короткий пролёт, явный перехлёст
    kos = ""
    for i in range(3):
        col = ("#7d5428", "#a07340", "#59391c")[i]
        d = f'M{kx_+16:.0f},{ky_+100:.0f}'
        for j in range(14):
            p = j / 13
            xx = kx_ + 30 + p * (gx - kx_ - 120)
            fz = p * 7.4 + i * 2.1 + t * 2.0
            yy = ky_ + 120 + p * 60 + math.sin(fz) * 54
            d += f' L{xx:.0f},{yy:.0f}'
        kos += (f'<path d="{d}" fill="none" stroke="{K}" stroke-width="44"'
                f' stroke-linecap="round" opacity=".9"/>')
        kos += (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="34"'
                f' stroke-linecap="round"/>')
        kos += (f'<path d="{d}" fill="none" stroke="#e4c79a" stroke-width="5"'
                f' opacity=".3"/>')
    s += SL(Z_SRED, kos)
    s += SL(Z_SRED, f'<path d="M{gx-70:.0f},{930-520*.80:.0f} l-110,52"'
                    f' stroke="#7d5428" stroke-width="22" stroke-linecap="round"/>')
    # готовая коса уходит к внуку одной толстой плетёнкой
    rost = A.ease(A.seg(t, .6, 2.2))
    vx = 1300
    s += SL(Z_SRED, figura(vx, 1050, 360, t, "#6b3a44", "#ffd98a", False, .6,
                           True, 1.0, False, 1.4, False, False))
    ruk, (rx_, ry_) = rukav(vx - 80, 850, 150, -40 + 16 * A.w(t, 1.0), t,
                            "#6b3a44", "#ffd98a", .3, 7.0)
    s += SL(Z_SRED, ruk)
    gotov = (f'<path d="M{gx+70:.0f},{790:.0f} q{(rx_-gx)*.5:.0f},{40:.0f}'
             f' {rx_-gx-20:.0f},{ry_-790:.0f}" fill="none" stroke="#59391c"'
             f' stroke-width="{26+14*rost:.0f}" stroke-linecap="round"/>')
    for i in range(8):                   # перехлёсты готовой косы
        p = i / 7
        gotov += (f'<ellipse cx="{gx+70+(rx_-gx-20)*p:.0f}"'
                  f' cy="{790+(ry_-790)*p+8*A.w(t,1.6,p):.0f}" rx="22" ry="15"'
                  f' fill="#a07340" {o(3)}/>')
    s += SL(Z_SRED, gotov)
    # ЛОШАДКА-МЕЧТА целиком, в открытом воздухе над лавкой
    pr = A.ease(A.seg(t, 1.2, 1.2))
    lgx, lgy = 1300, 660
    s += SL(Z_SRED, teplo(lgx - 70, lgy - 140, 620, 520, .2 * pr))
    s += SL(Z_SRED, _loshadka(lgx, lgy, 1.35, t, .70 + .28 * pr))
    for i in range(14):                  # пунктир мечты вокруг лошадки
        a = i * .449
        s += SL(Z_SRED, f'<circle cx="{lgx-100+math.cos(a)*280:.0f}"'
                        f' cy="{lgy-200+math.sin(a)*200:.0f}" r="6"'
                        f' fill="#ffe6b8" opacity="{.45*pr:.2f}"/>')
    s += SL(Z_SRED, f'<path d="M{rx_:.0f},{ry_:.0f} q{(lgx-rx_)*.5:.0f},{-90:.0f}'
                    f' {lgx+100-rx_:.0f},{lgy-180-ry_:.0f}" fill="none"'
                    f' stroke="#a07340" stroke-width="13"'
                    f' opacity="{.4+.5*pr:.2f}"/>')
    # обрезки кожи и шило на лавке
    for i in range(6):
        s += SL(Z_SRED, f'<path d="M{760+i*74:.0f},{916:.0f} q24,{-14-i*2:.0f} 52,2'
                        f' l-7,16 q-24,{-11:.0f} -48,2 Z" fill="#5f4126"'
                        f' opacity=".95" {o(3)}/>')
    s += SL(Z_SRED, f'<line x1="700" y1="912" x2="766" y2="872" stroke="#cfd6dc"'
                    f' stroke-width="8" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<rect x="672" y="902" width="44" height="24" rx="8"'
                    f' fill="#6b4a2a" {o(4)}/>')
    s += SL(Z_SRED, _chugunok(1760, 1012, 1.2, t, True))
    s += SL(Z_SRED, kot(300, 1012, t, 1.3, "#3b3430", False))
    s += SL(Z_SRED, _valenok(170, 1012, .9, t, .4, False, "#7d6f5e"))
    s += SL(Z_PERED, ramka_pp("levo", "#1c140d", .76))
    s += SL(Z_LETIT, iskra_let(t, 560, 310, 6, 977, 300, .4))
    s += vinetka(.46)
    return s


# ── 78 ─────────────────────────────────────────────────────────────────────
def valenki_shkaf_i_varezhki_na_rezink(t):
    """Городская прихожая: пара детских валенок с галошами сушится на чугунной
    батарее, из приоткрытого шкафа выплывает нафталиновое облачко, девочка
    морщит нос, варежки качаются на резинке из рукавов."""
    rnd = random.Random(7829)
    s = f'<rect width="{W}" height="{H}" fill="#2b2622"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#6f655c"/>')
    for i in range(11):                  # обои в полоску
        s += SL(Z_DAL, f'<rect x="{i*176:.0f}" y="0" width="86" height="840"'
                       f' fill="#7d7266" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect y="820" width="{W}" height="36" fill="#8d7f6e" {o(5)}/>')
    s += SL(Z_DAL, polovicy(856, "#6b4a2a"))
    s += SL(Z_DAL, kvartira_veschi(1480, 240, 420, t, 983))
    s += SL(Z_SRED, tusklaya_lampochka(960, 130, t, 1.5, True))
    # ШКАФ слева, дверца приоткрыта, из него плывёт облачко нафталина
    otk = A.ease(A.seg(t, .6, 1.3))
    s += SL(Z_SRED, _shkaf(90, 180, 520, 680, t, .5 * otk, True))
    for i in range(6):                   # нафталиновое облачко
        k = ((t * .34) + i * .17) % 1.0
        s += SL(Z_SRED, f'<ellipse cx="{470+k*320:.0f}" cy="{520-k*200:.0f}"'
                        f' rx="{54+86*k:.0f}" ry="{40*0+36+56*k:.0f}"'
                        f' fill="#e2f0f8" opacity="{.62*(1-k)*otk:.2f}"/>')
    s += SL(Z_SRED, _veshalka(640, 230, 420, t, 4, True))
    # БАТАРЕЯ и ВАЛЕНКИ на ней — главный предмет кадра
    bx, by, bw, bh = 900, 620, 660, 300
    s += SL(Z_SRED, _batareya(bx, by, bw, bh, t, 10))
    s += SL(Z_SRED, f'<rect x="{bx-40:.0f}" y="{by+bh:.0f}" width="{bw+80:.0f}"'
                    f' height="24" rx="8" fill="#8d949b" {o(5)}/>')
    for i, px in ((0, bx + 170), (1, bx + 420)):
        s += SL(Z_SRED, _valenok(px, by - 56, 2.05, t, .2 + i * .45, True,
                                 "#bda98a", -6 + i * 12))
        s += SL(Z_SRED, par(px, by - 430, t, 4, .5, 210, .42, 1.0))
    s += SL(Z_SRED, teplo(bx + bw / 2, by + bh * .4, 620, 420, .26))
    # варежки на резинке, продетой через рукава
    rez_y = 400
    s += SL(Z_SRED, f'<path d="M640,{rez_y:.0f} q{130:.0f},'
                    f'{80+10*A.w(t,2.0):.0f} {280:.0f},{-14:.0f}" fill="none"'
                    f' stroke="#c2ab86" stroke-width="8"/>')
    s += SL(Z_SRED, _varezhka(700, rez_y + 110, 1.6, t, .1, TKAN, True))
    s += SL(Z_SRED, _varezhka(880, rez_y + 76, 1.6, t, .55, TKAN2, True))
    # девочка морщит нос
    dx_ = 1730
    s += SL(Z_SRED, figura(dx_, 1050, 480, t, "#5b2f3a", "#ffd0a0", False, .35,
                           True, 1.0, False, 1.4, False, False))
    mor = A.ease(A.seg(t, 1.6, .5))
    s += SL(Z_SRED, f'<path d="M{dx_+36:.0f},{1050-480*.84:.0f}'
                    f' q{14:.0f},{-10-8*mor:.0f} {26:.0f},{2:.0f}" fill="none"'
                    f' stroke="#b08763" stroke-width="7" opacity="{.4+.6*mor:.2f}"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{dx_-10+i*14:.0f},{1050-480*.90:.0f}'
                        f' q6,{-14*mor:.0f} 12,0" fill="none" stroke="#9c7a5a"'
                        f' stroke-width="5" opacity="{.7*mor:.2f}"/>')
    ruk, (kx, ky) = rukav(dx_ - 90, 760, 170, 212 - 20 * mor, t, "#5b2f3a",
                          "#ffd0a0", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="26" ry="20"'
                    f' fill="#5b2f3a" {o(4)}/>')
    # коврик, галоши и ведро у двери
    s += SL(Z_SRED, f'<rect x="700" y="990" width="520" height="70" rx="12"'
                    f' fill="{TKAN2}" {o(6)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<line x1="{720+i*58:.0f}" y1="992" x2="{720+i*58:.0f}"'
                        f' y2="1058" stroke="#2f4a62" stroke-width="7" opacity=".7"/>')
    s += SL(Z_SRED, _botinok(1340, 1012, .86, t, .3, "#3a3630", .2))
    s += SL(Z_SRED, _botinok(1470, 1012, .82, t, .7, "#3a3630", .2))
    s += SL(Z_SRED, hodiki(250, 940, t, 1.2))
    s += SL(Z_SRED, kot(560, 1012, t, 1.15, "#4a4440", True))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="70" height="1080" fill="#1d1a16"'
                     f' opacity=".9"/>')
    s += vinetka(.44)
    return s


# ── 79 ─────────────────────────────────────────────────────────────────────
def tulup_s_gvozdya_i_chemodan_s_zimni(t):
    """Кадр надвое: слева сени — хозяин снимает с гвоздя овчинный тулуп и
    встряхивает его, валенки встают к печной дверце; справа городская комната,
    где щёлкают замки чемодана и шапки выскакивают пружиной."""
    rnd = random.Random(7919)
    s = f'<rect width="{W}" height="{H}" fill="#1e1812"/>'
    # ── левая половина: сени
    s += SL(Z_DAL, brevna(0, 0, 960, 840, 114))
    s += SL(Z_DAL, f'<rect width="960" height="840" fill="#271d14" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(840, "url(#pol)"))
    s += SL(Z_DAL, f'<rect y="840" width="960" height="240" fill="#3a2a1c"'
                   f' opacity=".55"/>')
    s += SL(Z_DAL, mebel_hlam(40, 820, 260, t, 991))
    # печь с дверцей, к ней ставят валенки
    s += SL(Z_SRED, pech(640, 300, 330, 540, t, True, True, False))
    px_, py_, pw_, ph2 = 686, 520, 240, 200
    s += SL(Z_SRED, kirpich_ustya(px_, py_, pw_, ph2, t, True))
    put = kontur_proema(px_, py_, pw_, ph2, "ustie")
    s += SL(Z_SRED, f'<path d="{put}" fill="#190b05"/>'
                    + ugli(px_ + 24, py_ + ph2 - 24, pw_ - 48, t, 7, 997)
                    + ogon(px_ + pw_ / 2, py_ + ph2 - 20, t, .95, .2, 6))
    s += SL(Z_SRED, teplo(px_ + pw_ / 2, py_ + ph2 * .7, 520, 440,
                          .46 + .12 * abs(A.w(t, 1.6))))
    vst = A.ease(A.seg(t, 1.8, 1.2))
    for i, sg in ((0, -1), (1, 1)):
        vxx = 300 + (px_ - 240 - 300) * vst + sg * 70
        s += SL(Z_SRED, _valenok(vxx, 850 - math.sin(vst * 3.14159) * 70, 1.25, t,
                                 .2 + i * .4, False, "#7d6f5e", sg * 8))
    # гвоздь и тулуп, который встряхивают
    s += SL(Z_SRED, f'<circle cx="250" cy="300" r="22" fill="#9aa1a8" {o(5)}/>')
    s += SL(Z_SRED, f'<circle cx="244" cy="294" r="8" fill="#e8eef6" opacity=".7"/>')
    snyat = A.ease(A.seg(t, .3, 1.1))
    tx_ = 250 + snyat * 120
    ty_ = 220 + snyat * 110
    tryas = max(0.0, A.w(t, .8, .1)) * snyat
    s += SL(Z_SRED, _tulup_vis(tx_ + 80, ty_, 440, 580, t, .2, tryas))
    for i in range(9):                   # пыль и шерстинки при встряхивании
        k = ((t * 1.1) + i * .11) % 1.0
        s += SL(Z_SRED, f'<circle cx="{tx_+rnd.uniform(-170,170):.0f}"'
                        f' cy="{ty_+260+rnd.uniform(-120,120)-k*80:.0f}"'
                        f' r="{5+9*k:.0f}" fill="#e4d6bc"'
                        f' opacity="{.5*(1-k)*tryas:.2f}"/>')
    s += SL(Z_SRED, figura(300, 1046, 580, t, "#3a3346", "#ffd98a", False, .2,
                           True, 1.0, False, 1.2, True))
    ruk, _ = rukav(370, 690, 150, -46 + 30 * tryas, t, "#3a3346", "#ffd98a",
                   .1, 7.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, para_izo_rta(222, 690, t, .3, 1.0, .45))
    # ── правая половина: городская комната
    s += SL(Z_DAL, f'<rect x="960" width="960" height="1080" fill="#6a6056"/>')
    for i in range(6):
        s += SL(Z_DAL, f'<rect x="{980+i*160:.0f}" y="0" width="76" height="880"'
                       f' fill="#786d61" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(880, "#6b4a2a"))
    s += SL(Z_DAL, kvartira_veschi(1560, 230, 360, t, 1009))
    s += SL(Z_SRED, tusklaya_lampochka(1440, 150, t, 1.35, True))
    # чемодан на пол-кадра, замки щёлкают, крышка откидывается
    chx, chy, chw, chh = 1100, 690, 680, 300
    shchel = A.ease(A.seg(t, 1.0, .6))
    otk = A.out(A.seg(t, 1.7, 1.0))
    ch = ten(chx + chw / 2, chy + chh + 18, chw * .45, 22, .5)
    ch += (f'<rect x="{chx}" y="{chy}" width="{chw}" height="{chh}" rx="18"'
           f' fill="#6b4a2a" {o(9)}/>')
    ch += (f'<rect x="{chx+20}" y="{chy+30}" width="{chw-40}" height="{chh-60}"'
           f' rx="10" fill="none" stroke="#4f351c" stroke-width="10"/>')
    for i in (0, 1):
        ch += (f'<rect x="{chx+chw*(.22+i*.42):.0f}" y="{chy-16:.0f}" width="90"'
               f' height="{34+10*shchel:.0f}" rx="8" fill="url(#zhel)" {o(5)}/>')
        ch += (f'<circle cx="{chx+chw*(.22+i*.42)+45:.0f}" cy="{chy+2:.0f}" r="12"'
               f' fill="{ZOL}" opacity="{.5+.5*shchel:.2f}"/>')
    ch += (f'<g transform="rotate({-34*otk:.1f} {chx:.0f} {chy:.0f})">'
           f'<rect x="{chx}" y="{chy-170}" width="{chw}" height="170" rx="14"'
           f' fill="#7d5636" {o(8)}/>'
           f'<rect x="{chx+26}" y="{chy-148}" width="{chw-52}" height="124" rx="10"'
           f' fill="none" stroke="#4f351c" stroke-width="9"/>'
           f'<rect x="{chx+chw*.42:.0f}" y="{chy-186}" width="{chw*.16:.0f}"'
           f' height="24" rx="8" fill="url(#zhel)" {o(4)}/></g>')
    ch += (f'<path d="M{chx+chw*.44:.0f},{chy+chh:.0f} h{chw*.12:.0f} l0,34'
           f' h{-chw*.12:.0f} Z" fill="#4f351c" {o(4)}/>')
    s += SL(Z_SRED, ch)
    # шапки выскакивают из чемодана пружиной
    for i in range(3):
        vy_ = A.over(A.seg(t, 1.9 + i * .34, .7)) * (1.0 + i * .45)
        s += SL(Z_SRED, _shapka_meh(chx + 140 + i * 210,
                                    chy + 30 - vy_ * (230 + i * 30), 1.45, t,
                                    .2 + i * .3, 0.0))
        s += SL(Z_SRED, f'<path d="M{chx+150+i*200:.0f},{chy+60:.0f}'
                        f' q{14:.0f},{-60*vy_:.0f} 0,{-120*vy_:.0f}" fill="none"'
                        f' stroke="#9aa1a8" stroke-width="7" opacity="{.6*vy_:.2f}"'
                        f' stroke-dasharray="14 10"/>')
    s += SL(Z_SRED, _varezhka(1760, 760, 1.1, t, .3, TKAN, True))
    s += SL(Z_SRED, f'<rect x="950" y="0" width="22" height="1080" fill="#15110d"'
                    f' opacity=".85"/>')
    s += SL(Z_SRED, kot(1760, 1012, t, 1.1, "#4a4440", False))
    s += SL(Z_PERED, ramka_pp("levo", "#100c09", .8))
    s += SL(Z_PERED, _valenok(1020, 1012, 1.0, t, .5, True, "#6e6358"))
    s += SL(Z_LETIT, iskra_let(t, px_ + pw_ / 2, py_ + 30, 6, 1013, 260, .4))
    s += vinetka(.46)
    return s


# ── 80 ─────────────────────────────────────────────────────────────────────
def shapka_na_prosvet(t):
    """Меховую шапку поднимают к лампе и раздвигают мех на просвет: из меха
    вылетает одна наглая моль с салфеткой на шее, ладони хлопают мимо,
    а на столе уже ждут мешочки лаванды."""
    rnd = random.Random(8011)
    s = f'<rect width="{W}" height="{H}" fill="#241c18"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 110, True, "dosk"))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#3a2c22" opacity=".55"/>')
    s += SL(Z_DAL, polovicy(900, "url(#pol)"))
    s += SL(Z_DAL, kvartira_veschi(60, 260, 380, t, 1019))
    # ЛАМПА — источник просвета
    lx, ly = 980, 300
    s += SL(Z_SRED, lampa(lx, ly, t, 1.7, True))
    s += SL(Z_SRED, teplo(lx, ly + 40, 900, 760, .5 + .12 * abs(A.w(t, 1.5))))
    s += SL(Z_SRED, luch(lx - 170, ly + 60, 340, 620, t, .17))
    # ШАПКА НА ПРОСВЕТ, крупно: мех раздвигается
    razd = A.ease(A.seg(t, .4, 1.0))
    shx, shy = lx, ly + 420
    s += SL(Z_SRED, _shapka_meh(shx, shy, 2.1, t, .1, razd))
    # R-0053: внутри шапки — настоящий мех на просвет (эллипс, порог 360).
    s += SL(Z_SRED, mesto_stoka(shx - 230, shy - 170, 460, 310, "ellips"))
    s += SL(Z_SRED, f'<ellipse cx="{shx:.0f}" cy="{shy-150:.0f}" rx="{90*razd:.0f}"'
                    f' ry="{150*razd:.0f}" fill="{SVET}" opacity="{.26*razd:.2f}"/>')
    # рукава держат шапку с двух сторон, без кистей
    for i, sg in ((0, -1), (1, 1)):
        ruk, (kx, ky) = rukav(shx + sg * 420, shy + 190, 140,
                              (-160 if sg > 0 else -20) + sg * 10 * A.w(t, 1.1, i * .3),
                              t, "#43394a", "#ffd98a", .2 + i * .3, 5.0, nichya=True)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="34" ry="26"'
                        f' fill="#43394a" {o(5)}/>')
    # МОЛЬ вылетает из меха и нагло кружит
    vyl = A.ease(A.seg(t, 1.2, 1.4))
    mx = shx + 60 + vyl * 420
    my = shy - 170 - vyl * 230 + 40 * A.w(t, .9)
    s += SL(Z_SRED, _mol(mx, my, 2.3, t, .2))
    for i in range(7):                   # пыльца с крыльев
        k = ((t * .7) + i * .14) % 1.0
        s += SL(Z_SRED, f'<circle cx="{mx-40-k*90:.0f}" cy="{my+30+k*70:.0f}"'
                        f' r="{4+4*k:.0f}" fill="#e8dcc0" opacity="{.6*(1-k)*vyl:.2f}"/>')
    # ладони хлопают мимо — два рукава сходятся
    hlop = max(0.0, A.w(t, 1.3, .4)) * A.ease(A.seg(t, 2.0, .5))
    for sg in (-1, 1):
        hx = mx + sg * (210 - 170 * hlop)
        s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{my+40:.0f}" rx="52" ry="34"'
                        f' fill="#3f3546" transform="rotate({sg*-24:.0f} {hx:.0f}'
                        f' {my+40:.0f})" {o(5)}/>')
        s += SL(Z_SRED, f'<line x1="{hx+sg*44:.0f}" y1="{my+56:.0f}"'
                        f' x2="{hx+sg*180:.0f}" y2="{my+150:.0f}" stroke="#3f3546"'
                        f' stroke-width="34" stroke-linecap="round"/>')
    if hlop > .8:
        for i in range(6):
            a = -2.6 + i * .5
            s += SL(Z_SRED, f'<line x1="{mx+math.cos(a)*70:.0f}"'
                            f' y1="{my+40+math.sin(a)*70:.0f}"'
                            f' x2="{mx+math.cos(a)*130:.0f}"'
                            f' y2="{my+40+math.sin(a)*130:.0f}" stroke="#ffe6b8"'
                            f' stroke-width="8" opacity=".6"/>')
    # стол: мешочки лаванды ложатся в шапки
    s += SL(Z_SRED, stol(1380, 880, 520, 40, True))
    for i in range(3):
        lv = A.ease(A.seg(t, 2.2 + i * .3, .7))
        mxx = 1440 + i * 170
        s += SL(Z_SRED, f'<path d="M{mxx-66:.0f},{880-lv*40:.0f}'
                        f' q{-26:.0f},{-86:.0f} {18:.0f},{-120:.0f}'
                        f' q{48:.0f},{-18:.0f} {96:.0f},0 q{44:.0f},{34:.0f}'
                        f' {18:.0f},{120:.0f} Z" fill="#cbbb93" opacity=".97"'
                        f' {o(6)}/>')
        for j in range(4):               # складки холста
            s += SL(Z_SRED, f'<path d="M{mxx-44+j*30:.0f},{870-lv*40:.0f}'
                            f' q{4:.0f},{-46:.0f} {0:.0f},{-88:.0f}"'
                            f' fill="none" stroke="#b0a07c" stroke-width="6"'
                            f' opacity=".7"/>')
        s += SL(Z_SRED, f'<path d="M{mxx-52:.0f},{766-lv*40:.0f} q{52:.0f},{-26:.0f}'
                        f' {104:.0f},0" fill="none" stroke="#8a6238"'
                        f' stroke-width="14"/>')
        for j in range(4):               # веточки лаванды торчат
            s += SL(Z_SRED, f'<line x1="{mxx-20+j*14:.0f}" y1="{790-lv*40:.0f}"'
                            f' x2="{mxx-26+j*16+3*A.w(t,2.0,j*.2):.0f}"'
                            f' y2="{748-lv*40:.0f}" stroke="#7a6a9a"'
                            f' stroke-width="6"/>')
    s += SL(Z_SRED, _chugunok(1700, 880, 1.2, t, False))
    s += SL(Z_SRED, figura(560, 1070, 520, t, "#43394a", "#ffd98a", False, .25,
                           True, 1.0, False, 1.0, True))
    s += SL(Z_SRED, _varezhka(300, 820, 1.2, t, .3, TKAN, True))
    s += SL(Z_SRED, _valenok(240, 1012, .9, t, .5, False, "#7d6f5e"))
    s += SL(Z_PERED, ramka_pp("pravo", "#120e0b", .82))
    s += SL(Z_PERED, _shkaf(1760, 120, 220, 760, t, .18, False))
    s += SL(Z_LETIT, iskra_let(t, lx, ly + 60, 6, 1021, 240, .35))
    s += vinetka(.48)
    return s


# ── 81 ─────────────────────────────────────────────────────────────────────
def botinki_s_gazetoy_i_kremom(t):
    """Пара зимних ботинок на расстеленной газете: от них идёт пар, газета
    комкается и уходит внутрь, щётка с кремом наводит блеск на носок,
    а за окном падает первая снежинка."""
    rnd = random.Random(8111)
    s = f'<rect width="{W}" height="{H}" fill="#2a241e"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#726758"/>')
    for i in range(8):                   # кафельный поясок прихожей
        s += SL(Z_DAL, f'<rect x="{i*244:.0f}" y="520" width="226" height="190"'
                       f' rx="6" fill="#8d8172" opacity=".55" {o(3)}/>')
    s += SL(Z_DAL, f'<rect y="700" width="{W}" height="30" fill="#8d7f6e" {o(5)}/>')
    s += SL(Z_DAL, polovicy(730, "#6b4a2a"))
    s += SL(Z_DAL, kvartira_veschi(70, 180, 340, t, 1031))
    # окно справа: за ним падает снежинка
    okx, oky, okw, okh = 1420, 120, 420, 440
    vid = (f'<rect x="{okx}" y="{oky}" width="{okw}" height="{okh}"'
           f' fill="url(#nsumer)"/>')
    for i in range(4):
        vid += (f'<rect x="{okx+40+i*96:.0f}" y="{oky+okh*.5:.0f}" width="70"'
                f' height="{okh*.5:.0f}" fill="#3a4254" opacity=".9"/>')
        if i % 2:
            vid += (f'<rect x="{okx+58+i*96:.0f}" y="{oky+okh*.58:.0f}" width="30"'
                    f' height="30" fill="{SVET}" opacity=".5"/>')
    sn = ((t * .3) % 1.0)
    vid += (f'<circle cx="{okx+okw*.5+30*A.w(t,2.4):.0f}" cy="{oky+sn*okh:.0f}"'
            f' r="11" fill="#f2f8ff" opacity=".95"/>')
    for i in range(5):
        a = i * 1.25
        vid += (f'<line x1="{okx+okw*.5+30*A.w(t,2.4):.0f}" y1="{oky+sn*okh:.0f}"'
                f' x2="{okx+okw*.5+30*A.w(t,2.4)+math.cos(a)*20:.0f}"'
                f' y2="{oky+sn*okh+math.sin(a)*20:.0f}" stroke="#f2f8ff"'
                f' stroke-width="4" opacity=".8"/>')
    s += SL(Z_SRED, okno_izby(okx, oky, okw, okh, t, vid, .25, False, True))
    s += SL(Z_SRED, tusklaya_lampochka(700, 120, t, 1.4, True))
    # батарея, к которой ставят ботинки
    s += SL(Z_SRED, _batareya(1180, 560, 420, 230, t, 7))
    # ГАЗЕТА и ПАРА БОТИНОК на ней — крупно
    s += SL(Z_SRED, _gazeta_list(760, 930, 820, 320, t, -3, 1033, 0.0))
    s += SL(Z_SRED, _gazeta_list(1120, 960, 600, 260, t, 5, 1039, 0.0))
    pere = A.ease(A.seg(t, .4, 1.0))
    bl = A.ease(A.seg(t, 2.4, 1.2))
    for i, sg in ((0, -1), (1, 1)):
        bxx = 760 + sg * 145 + pere * 150
        s += SL(Z_SRED, _botinok(bxx, 900 + i * 14, 2.0, t, .2 + i * .4,
                                 "#4a3526", bl))
        s += SL(Z_SRED, par(bxx, 760, t, 4, .55, 220, .44, 1.0))
    s += SL(Z_SRED, teplo(1300, 700, 560, 420, .28))
    # комок газеты летит в ботинок
    kom = A.ease(A.seg(t, 1.3, 1.0))
    s += SL(Z_SRED, _gazeta_list(520 + kom * 380, 700 - math.sin(kom * 3.14159) * 160,
                                 300, 220, t, 14 + kom * 90, 1049, kom))
    # щётка ходит по носку
    hod = A.w(t, .8, .1)
    s += SL(Z_SRED, _shchetka(1360 + hod * 90, 880, 1.5, t, -12 + 8 * hod))
    s += SL(Z_SRED, f'<rect x="1660" y="960" width="130" height="80" rx="14"'
                    f' fill="#3f3a36" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1725" cy="960" rx="65" ry="18" fill="#6b645c"'
                    f' {o(4)}/>')
    s += SL(Z_SRED, f'<ellipse cx="1725" cy="958" rx="48" ry="12" fill="#23211e"'
                    f' opacity=".9"/>')
    # рукава работают: один держит ботинок, другой ведёт щётку
    ruk, (kx, ky) = rukav(1140, 600, 170, 66 + 14 * hod, t, "#3f4a5e",
                          "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="32" ry="24"'
                    f' fill="#3f4a5e" {o(5)}/>')
    s += SL(Z_SRED, figura(250, 1070, 520, t, "#3f4a5e", "#ffd98a", False, .3,
                           True, 1.0, False, 1.0, False, False))
    s += SL(Z_SRED, _valenok(1760, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_SRED, kot(1540, 1012, t, 1.15, "#3b3430", True))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="80" height="1080" fill="#1a1612"'
                     f' opacity=".9"/>')
    s += SL(Z_PERED, _chashka(170, 1012, 1.5, t, .2, KREM, True))
    s += SL(Z_PERED, par(130, 960, t, 3, .4, 160, .4, .8))
    s += vinetka(.46)
    return s


# ── 82 ─────────────────────────────────────────────────────────────────────
def zhena_derzhit_muzha_za_kushak(t):
    """Ворота двора: муж в шапке набекрень уже взялся за кольцо калитки и
    подмигивает приятелям за забором, а жена держит его за кушак, упёршись
    лаптями в землю. Справа у избы накрытый стол и численник на стене."""
    rnd = random.Random(8221)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 1051)
    s += oblaka(t, 170, 5, 1061, .32, "#c8d4e2", 15.0)
    s += SL(Z_DAL, ulica_dal(60, 660, 820, t, False, 1063))
    s += SL(Z_DAL, izba_snaruzhi(1500, 720, 420, t, True, True, 1069))
    s += SL(Z_DAL, goloe_derevo(760, 700, 400, t, 1087, 6, "#303240"))
    s += SL(Z_DAL, gryaz_polosa(740, 220, "#443f36"))
    s += SL(Z_DAL, sneg_lezhit(900, 22, "url(#sneg)"))
    # ВОРОТА ДВОРА на пол-кадра: столбы, тёс, кольцо калитки
    vx, vy, vw, vh = 150, 260, 540, 820
    vor = (f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="8"'
           f' fill="url(#dosk)" {o(10)}/>')
    for i in range(9):
        vor += (f'<rect x="{vx+14+i*(vw-28)/9:.0f}" y="{vy+10}"'
                f' width="{(vw-28)/9-10:.0f}" height="{vh-20}" rx="6"'
                f' fill="url(#dosk)" {o(5)}/>')
    vor += (f'<path d="M{vx-50},{vy+10} h{vw+100} l-60,-90 h{-vw+20} Z"'
            f' fill="{DOSKA2}" {o(9)}/>')
    vor += (f'<rect x="{vx-70}" y="{vy-20}" width="80" height="{vh+20}" rx="10"'
            f' fill="url(#derev)" {o(9)}/>')
    vor += (f'<rect x="{vx+vw-10:.0f}" y="{vy-20}" width="80" height="{vh+20}" rx="10"'
            f' fill="url(#derev)" {o(9)}/>')
    vor += (f'<line x1="{vx+40}" y1="{vy+vh*.34:.0f}" x2="{vx+vw-40:.0f}"'
            f' y2="{vy+vh*.22:.0f}" stroke="#6b4a2a" stroke-width="22"/>')
    s += SL(Z_SRED, vor)
    s += SL(Z_SRED, podkova(vx + vw / 2, vy - 110, 2.3, t, "url(#zhel)"))
    kol = 3.0 * A.w(t, 1.2, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kol:.2f} {vx+vw-120:.0f} {vy+vh*.52:.0f})">'
                    f'<circle cx="{vx+vw-120:.0f}" cy="{vy+vh*.58:.0f}" r="42"'
                    f' fill="none" stroke="url(#zhel)" stroke-width="16"/>'
                    f'<rect x="{vx+vw-134:.0f}" y="{vy+vh*.48:.0f}" width="28"'
                    f' height="30" rx="8" fill="#5d6168" {o(4)}/></g>')
    # приятели машут из-за забора
    s += SL(Z_DAL, pleten(1380, 700, 480, 210, 9))
    for i, fx_ in ((0, 1450), (1, 1600), (2, 1740)):
        s += SL(Z_DAL, figura(fx_, 700, 230 + i * 20, t, "#2e3a46", "#cfe4f5", False,
                              .2 * i, True, 1.0, False, 1.0, i == 2, i != 2))
        mah = -40 - 36 * A.w(t, .8, i * .3)
        ruk, _ = rukav(fx_ + 40, 560, 130, mah, t, "#2e3a46", "#cfe4f5", i * .3, 10.0)
        s += SL(Z_DAL, ruk)
    # муж у кольца калитки, жена держит за кушак
    mx = 830 - 40 * A.ease(A.seg(t, .4, 1.6))
    s += SL(Z_SRED, figura(mx, 1060, 540, t, "#3a3346", "#ffd0a0", False, .1,
                           True, 1.0, True, -3.0, True, True))
    s += SL(Z_SRED, para_izo_rta(mx + 64, 690, t, .2, 1.3, .55))
    ruk, (kx, ky) = rukav(mx + 70, 760, 230, -22 + 8 * A.w(t, 1.1), t,
                          "#3a3346", "#ffd0a0", .1, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="34" ry="26"'
                    f' fill="#3a3346" {o(5)}/>')
    zx = 1180
    s += SL(Z_SRED, figura(zx, 1066, 500, t, "#5b2f3a", "#ffd0a0", True, .4,
                           True, 1.0, False, 4.0))
    s += SL(Z_SRED, para_izo_rta(zx - 60, 700, t, .6, 1.2, .5))
    # КУШАК НАТЯНУТ СТРУНОЙ между ними
    nat = .4 + .6 * abs(A.w(t, .7, .1))
    kus = (f'<path d="M{mx+30:.0f},{830:.0f} q{(zx-mx)*.5:.0f},{60-40*nat:.0f}'
           f' {zx-mx-110:.0f},{10:.0f}" fill="none" stroke="{TKAN}"'
           f' stroke-width="{30+8*nat:.0f}" stroke-linecap="round"/>')
    kus += (f'<path d="M{mx+30:.0f},{830:.0f} q{(zx-mx)*.5:.0f},{60-40*nat:.0f}'
            f' {zx-mx-110:.0f},{10:.0f}" fill="none" stroke="#f0d3a8"'
            f' stroke-width="6" opacity=".5"/>')
    for i in range(5):                   # кисти кушака трясутся
        kus += (f'<path d="M{zx-80+i*12:.0f},{842:.0f} q{6:.0f},{40:.0f}'
                f' {-4+8*A.w(t,1.1,i*.2):.0f},{72:.0f}" fill="none" stroke="{TKAN}"'
                f' stroke-width="9" stroke-linecap="round"/>')
    s += SL(Z_SRED, kus)
    ruk2, _ = rukav(zx - 70, 820, 180, 188 + 10 * A.w(t, .9, .3), t,
                    "#5b2f3a", "#ffd0a0", .4, 4.0)
    s += SL(Z_SRED, ruk2)
    for i in (-1, 1):                    # лапти жены упёрлись в землю
        s += SL(Z_SRED, f'<path d="M{zx+i*60-40:.0f},{1058:.0f} h80 q16,0 10,20'
                        f' h-96 q-10,-20 6,-20 Z" fill="#b78a46" {o(4)}/>')
        for j in range(4):
            s += SL(Z_SRED, f'<line x1="{zx+i*60-34+j*18:.0f}" y1="1060"'
                            f' x2="{zx+i*60-30+j*18:.0f}" y2="1076"'
                            f' stroke="#8a6534" stroke-width="5"/>')
    # стол у избы справа и численник: листки летят
    s += SL(Z_SRED, stol(1560, 900, 320, 36, True))
    s += SL(Z_SRED, karavay(1660, 896, .9, True))
    s += SL(Z_SRED, _chugunok(1760, 872, 1.0, t, True))
    s += SL(Z_SRED, svecha(1570, 790, t, .2, 1.8, 120))
    s += SL(Z_SRED, teplo(1570, 750, 560, 470, .44 + .1 * abs(A.w(t, 1.5))))
    for i in range(5):                   # листки численника летят по ветру
        k = ((t * .45) + i * .2) % 1.0
        s += SL(Z_LETIT, f'<g transform="rotate({k*160+i*30:.0f}'
                         f' {1540+k*300:.0f} {520-k*260:.0f})">'
                         f'<rect x="{1540+k*300:.0f}" y="{520-k*260:.0f}" width="54"'
                         f' height="72" rx="5" fill="url(#list)" opacity="{1-k*.6:.2f}"'
                         f' {o(3)}/>'
                         f'<path d="M{1550+k*300:.0f},{556-k*260:.0f} q16,4 34,0"'
                         f' fill="none" stroke="#7d756a" stroke-width="4"/></g>')
    s += SL(Z_SRED, kura(640, 1012, t, .9, .3))
    s += SL(Z_SRED, kura(720, 1012, t, .8, .7))
    s += SL(Z_PERED, ramka_pp("levo", "#141019", .8))
    s += SL(Z_PERED, goloe_derevo(1900, 1080, 640, t, 1091, 7, "#22242c"))
    s += SL(Z_LETIT, mokryy_sneg(t, 28, 1093, .5, 1.0))
    s += vinetka(.46)
    return s


# ── 83 ─────────────────────────────────────────────────────────────────────
def bolshoe_okno_s_lavkoy(t):
    """Широкое окно избы с частым переплётом на две трети кадра, под ним лавка
    и горшок с луком на подоконнике: дед усаживается смотреть небо, кот
    запрыгивает рядом. За стеклом идёт НАСТОЯЩЕЕ небо."""
    rnd = random.Random(8311)
    s = f'<rect width="{W}" height="{H}" fill="#3a2c20"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 120))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#2f2318" opacity=".42"/>')
    s += SL(Z_DAL, utvar_izby(1600, 220, 300, t, 1097))
    s += SL(Z_DAL, polovicy(900, "url(#pol)"))
    # печь краем кадра — единственное тёплое пятно в ровном дневном свете
    pch = (f'<rect x="-60" y="60" width="330" height="840" rx="18"'
           f' fill="url(#pech)" {o(9)}/>')
    pch += (f'<rect x="-40" y="20" width="290" height="44" rx="10" fill="{PECH2}"'
            f' {o(6)}/>')
    s += SL(Z_SRED, pch)
    s += SL(Z_SRED, kirpich_ustya(20, 450, 240, 230, t, True))
    s += SL(Z_SRED, f'<path d="{kontur_proema(20, 450, 240, 230, "ustie")}"'
                    f' fill="#190b05"/>'
                    + ugli(40, 660, 200, t, 8, 1103)
                    + ogon(140, 666, t, 1.15, .2, 6))
    s += SL(Z_SRED, teplo(140, 610, 560, 470, .46 + .12 * abs(A.w(t, 1.6))))
    # ОКНО: сначала нарисованный вид по форме проёма, потом метка, потом переплёт
    ox, oy, ow, oh = 400, 120, 1140, 620
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="bo83"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="url(#nden)"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#nden)"/>')
    for i in range(6):                   # облака за стеклом плывут
        k = ((t * .035) + i * .17) % 1.2 - .1
        cx_ = ox - 200 + k * (ow + 400)
        cy_ = oy + 90 + (i % 3) * 86
        za += (f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="{150+i*22:.0f}"'
               f' ry="{44+i*7:.0f}" fill="#eef3f8" opacity=".72"/>')
        za += (f'<ellipse cx="{cx_+90:.0f}" cy="{cy_+16:.0f}" rx="{110+i*14:.0f}"'
               f' ry="{34+i*5:.0f}" fill="#e2eaf2" opacity=".66"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.70:.0f}" width="{ow}" height="{oh*.30:.0f}"'
           f' fill="#8a9aa2" opacity=".55"/>')
    # кольцо вокруг солнца: иначе верх кадра — ровная заливка
    sx0, sy0 = ox + ow * .68, oy + oh * .26
    za += (f'<circle cx="{sx0:.0f}" cy="{sy0:.0f}" r="{150+6*A.w(t,2.6):.0f}"'
           f' fill="none" stroke="#fff3cf" stroke-width="22" opacity=".65"/>')
    za += (f'<circle cx="{sx0:.0f}" cy="{sy0:.0f}" r="{196+8*A.w(t,2.2):.0f}"'
           f' fill="none" stroke="#ffeeb8" stroke-width="9" opacity=".45"/>')
    za += (f'<circle cx="{sx0:.0f}" cy="{sy0:.0f}" r="56" fill="#fffaf0"'
           f' opacity=".9"/>')
    for i in range(6):               # птицы за стеклом тянутся клином
        k = ((t * .05) + i * .09) % 1.1
        bx_ = ox + 80 + k * (ow - 160)
        by_ = oy + 120 + i * 26 + 10 * A.w(t, 1.6, i * .2)
        za += (f'<path d="M{bx_:.0f},{by_:.0f} q14,-12 28,0 q14,-12 28,0"'
               f' fill="none" stroke="#4a5560" stroke-width="5" opacity=".7"/>')
    for i in range(5):                   # дальние избы и деревья за стеклом
        bx = ox + 60 + i * 230
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.64:.0f}" width="130"'
               f' height="{oh*.22:.0f}" fill="#7d8690" opacity=".8"/>')
        za += (f'<path d="M{bx-18:.0f},{oy+oh*.64:.0f} l83,-62 l83,62 Z"'
               f' fill="#6f7a85" opacity=".85"/>')
        za += (f'<path d="M{bx+180:.0f},{oy+oh*.66:.0f} l-26,0 l26,-72 l26,72 Z"'
               f' fill="#5e6a72" opacity=".8"/>')
    vid += f'<g clip-path="url(#bo83)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    # обвязка: частый переплёт, наличники, откосы
    ob = (f'<rect x="{ox-46}" y="{oy-46}" width="{ow+92}" height="{oh+92}" rx="10"'
          f' fill="none" stroke="url(#derev)" stroke-width="92"/>')
    for i in range(1, 6):                # частый переплёт по вертикали
        ob += (f'<rect x="{ox+i*ow/6-17:.0f}" y="{oy}" width="34"'
               f' height="{oh}" fill="url(#derev)"/>')
        ob += (f'<line x1="{ox+i*ow/6:.0f}" y1="{oy}" x2="{ox+i*ow/6:.0f}"'
               f' y2="{oy+oh}" stroke="{K}" stroke-width="4" opacity=".5"/>')
    for i in range(1, 4):
        ob += (f'<line x1="{ox}" y1="{oy+i*oh/4:.0f}" x2="{ox+ow}"'
               f' y2="{oy+i*oh/4:.0f}" stroke="url(#derev)" stroke-width="34"/>')
        ob += (f'<line x1="{ox}" y1="{oy+i*oh/4:.0f}" x2="{ox+ow}"'
               f' y2="{oy+i*oh/4:.0f}" stroke="{K}" stroke-width="4"'
               f' opacity=".5"/>')
    ob += (f'<path d="M{ox+30},{oy+40} l{ow*.36:.0f},{oh*.5:.0f}" stroke="#ffffff"'
           f' stroke-width="16" opacity=".16"/>')
    ob += f'<path d="{put}" fill="none" {o(10)}/>'
    ob += (f'<path d="M{ox-120},{oy-56} h{ow+240} l-66,-78 h{-ow-108} Z"'
           f' fill="{DOSKA2}" {o(9)}/>')
    for i in range(11):                  # резные зубцы наличника
        ob += (f'<path d="M{ox-96+i*(ow+192)/10:.0f},{oy-62} l32,-26 l32,26 Z"'
               f' fill="{MED}" opacity=".9" {o(3)}/>')
    ob += (f'<rect x="{ox-130}" y="{oy+oh+50}" width="{ow+260}" height="54" rx="10"'
           f' fill="url(#dosk)" {o(9)}/>')
    vid += ob
    s += SL(Z_SRED, vid)
    # подоконник с горшком лука
    s += SL(Z_SRED, f'<rect x="{ox-80}" y="{oy+oh+104}" width="{ow+160}" height="34"'
                    f' rx="8" fill="{DOSKA}" {o(6)}/>')
    gx, gy = ox + 190, oy + oh + 104
    s += SL(Z_SRED, f'<path d="M{gx-80:.0f},{gy-130:.0f} h160 l-20,130 h-120 Z"'
                    f' fill="url(#glina)" {o(7)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy-130:.0f}" rx="80" ry="20"'
                    f' fill="#9c6a3c" {o(5)}/>')
    for i in range(7):                   # перья лука покачиваются
        a = -1.1 + i * .34
        kach = 9 * A.w(t, 2.2, i * .17)
        s += SL(Z_SRED, f'<path d="M{gx+math.cos(a)*30:.0f},{gy-134:.0f}'
                        f' q{math.cos(a)*40+kach:.0f},{-80:.0f}'
                        f' {math.cos(a)*62+kach*1.6:.0f},{-168:.0f}" fill="none"'
                        f' stroke="{ZEL2}" stroke-width="{15-i}"'
                        f' stroke-linecap="round"/>')
        s += SL(Z_SRED, f'<ellipse cx="{gx+math.cos(a)*22:.0f}" cy="{gy-146:.0f}"'
                        f' rx="26" ry="20" fill="#c9a771" {o(3)}/>')
    # лавка под окном, дед усаживается, кот запрыгивает
    s += SL(Z_SRED, lavka(540, 880, 880))
    sad = A.ease(A.seg(t, .5, 1.4))
    s += SL(Z_SRED, figura(1300, 900 + 26 * sad, 520 - 70 * sad, t, "#3a3346",
                           "#ffd98a", False, .2, True, 1.0, True, 1.0, True))
    pr = A.ease(A.seg(t, 2.0, .9))
    s += SL(Z_SRED, kot(700, 880 + 180 * (1 - pr), t, 1.35, "#3b3430", False))
    s += SL(Z_SRED, f'<ellipse cx="700" cy="{886:.0f}" rx="70" ry="14"'
                    f' fill="#000000" opacity="{.3*pr:.2f}"/>')
    s += SL(Z_SRED, krynka(1620, 1012, 1.6))
    s += SL(Z_SRED, _valenok(300, 1012, .9, t, .4, False, "#7d6f5e"))
    s += SL(Z_SRED, _chashka(1480, 1012, 1.4, t, .3, KREM, True))
    s += SL(Z_SRED, par(1480, 968, t, 3, .4, 160, .4, .8))
    s += SL(Z_PERED, zanaveska(360, 60, 460, 200, RUSH, t, 1))
    s += SL(Z_PERED, zanaveska(1580, 60, 460, 200, RUSH, t, -1))
    s += vinetka(.42)
    return s


# ── 84 ─────────────────────────────────────────────────────────────────────
def ded_chitaet_nebo(t):
    """Дед на лавке вполоборота, очки на верёвочке, палец поднят: он читает
    небо, как газету, — по нему справа налево бегут рисованные строчки из
    облаков, а бабка рядом мелькает спицами."""
    rnd = random.Random(8419)
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, False, 1109)
    s += oblaka(t, 140, 5, 1117, .3, "#e4ebf2", 20.0)
    # облачные строчки бегут справа налево
    for r in range(5):                   # пять строк «слов» из облаков
        yy = 120 + r * 96
        for i in range(10):
            k = ((t * .07) + i * .105 + r * .04) % 1.25 - .12
            xx = W + 200 - k * (W + 500)
            ln = 56 + ((i * 37 + r * 19) % 110)
            s += SL(Z_NEBO, f'<path d="M{xx:.0f},{yy:.0f}'
                            f' q{ln*.16:.0f},-22 {ln*.33:.0f},0'
                            f' q{ln*.16:.0f},22 {ln*.33:.0f},0'
                            f' q{ln*.16:.0f},-22 {ln*.34:.0f},0"'
                            f' fill="none" stroke="#fbfdff" stroke-width="20"'
                            f' stroke-linecap="round"'
                            f' opacity="{.80+.16*((i+r) % 3)/2:.2f}"/>')
    s += SL(Z_DAL, ulica_dal(40, 720, 900, t, False, 1123))
    s += SL(Z_DAL, izba_snaruzhi(1560, 760, 380, t, True, True, 1129))
    s += SL(Z_DAL, pleten(1180, 800, 420, 190, 8))
    s += SL(Z_DAL, gryaz_polosa(790, 210, "#4a443a"))
    # изба за спиной: тёплое окно и дымок из трубы
    izb = brevna(60, 300, 900, 600, 112)
    izb += (f'<path d="M20,310 L510,60 L1000,310 Z" fill="#4a3b2c" opacity=".96" {o(9)}/>')
    izb += (f'<rect x="700" y="20" width="96" height="190" fill="url(#kamen)" {o(7)}/>')
    s += SL(Z_DAL, izb)
    s += SL(Z_DAL, dym(748, 30, t, 6, .24, 340, .4, "#d8cbbd", 1.2))
    s += SL(Z_DAL, okno_izby(150, 420, 400, 300, t, svet=True, moroz=.1))
    s += SL(Z_DAL, lampa(350, 700, t, 1.1, False))
    s += SL(Z_DAL, teplo(350, 580, 680, 560, .46 + .12 * abs(A.w(t, 1.7))))
    s += SL(Z_SRED, lavka(560, 1000, 760))
    # ДЕД на пол-кадра: вполоборота, очки, палец вверх
    dx = 820
    s += SL(Z_SRED, figura(dx, 1000, 680, t, "#3a3346", "#ffd98a", False, .15,
                           True, 1.0, True, 1.4, True))
    s += SL(Z_SRED, _ochki(dx + 56, 1000 - 680 * .845, 1.7, t, True))
    vedet = A.w(t, 1.6, .1)
    ruk, (kx, ky) = rukav(dx + 100, 700, 210, -78 + 16 * vedet, t, "#3a3346",
                          "#ffd98a", .1, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{ky:.0f} l{8:.0f},{-70:.0f}"'
                    f' stroke="#3a3346" stroke-width="26" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx+10:.0f}" cy="{ky-82:.0f}" rx="16" ry="22"'
                    f' fill="#f0cfae" {o(4)}/>')
    # губы шевелятся: дужки у лица
    for i in range(3):
        k = ((t * .9) + i * .33) % 1.0
        s += SL(Z_SRED, f'<path d="M{dx+120+k*60:.0f},{1000-680*.80:.0f}'
                        f' q24,-18 10,-44" fill="none" stroke="#f2e2c8"'
                        f' stroke-width="6" opacity="{.6*(1-k):.2f}"/>')
    s += SL(Z_SRED, para_izo_rta(dx + 110, 1000 - 680 * .80, t, .2, 1.3, .45))
    # бабка со спицами
    bx = 420
    s += SL(Z_SRED, figura(bx, 1010, 500, t, "#5b2f3a", "#ffd98a", True, .5,
                           False, 1.0, True, 1.0))
    sp = 24 * A.w(t, .5, .2)
    for i in range(2):
        s += SL(Z_SRED, f'<line x1="{bx-110+i*20:.0f}" y1="{780+sp*.5:.0f}"'
                        f' x2="{bx-10+i*24:.0f}" y2="{830-sp:.0f}" stroke="{KREM}"'
                        f' stroke-width="8" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="{bx-140:.0f}" cy="{856:.0f}" rx="56" ry="46"'
                    f' fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{bx-130:.0f},{826:.0f} q-44,-40 -96,-6" fill="none"'
                    f' stroke="{TKAN2}" stroke-width="7"/>')
    s += SL(Z_SRED, _chashka(1280, 940, 1.5, t, .2, KREM, True))
    s += SL(Z_SRED, par(1280, 850, t, 4, .45, 180, .42, .9))
    s += SL(Z_SRED, kura(1400, 1012, t, 1.0, .3))
    s += SL(Z_SRED, kot(1600, 1012, t, 1.2, "#4a4440", True))
    s += SL(Z_SRED, _korzina_ryab(1760, 1012, 220, 160, t, 1153))
    s += SL(Z_PERED, ramka_pp("pravo", "#17140f", .76))
    s += SL(Z_PERED, grozd_ryabiny(120, 220, t, 1.8, 17, 1163, .2))
    s += vinetka(.42)
    return s


# ── 85 ─────────────────────────────────────────────────────────────────────
def vihr_za_porogom(t):
    """Распахнутая дверь избы: за порогом рисованный Вихрь с хитрой рожицей
    срывает с мужика шапку, вертит её, кружит самого мужика волчком, а жена
    возвращает его за ворот."""
    rnd = random.Random(8521)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 1171)
    s += SL(Z_DAL, ulica_dal(900, 640, 1020, t, False, 1181))
    s += SL(Z_DAL, gryaz_polosa(720, 230, "#3f3a32"))
    s += SL(Z_DAL, goloe_derevo(1640, 760, 520, t, 1187, 7, "#2a2c34"))
    # стена избы с распахнутой дверью: изнутри тёплый свет
    st = brevna(0, 0, 860, 1080, 118)
    s += SL(Z_SRED, st)
    dx, dy, dw, dh = 230, 180, 540, 820
    s += SL(Z_SRED, f'<rect x="{dx-40}" y="{dy-40}" width="{dw+80}" height="{dh+40}"'
                    f' rx="10" fill="url(#derev)" {o(9)}/>')
    vn = (f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#2a1a10"/>')
    vn += teplo(dx + dw * .5, dy + dh * .6, 420, 500, .62)
    vn += (f'<rect x="{dx+60}" y="{dy+dh*.52:.0f}" width="{dw-120}" height="30"'
           f' rx="8" fill="#5a4026" opacity=".9"/>')
    vn += ogon(dx + dw * .36, dy + dh * .70, t, 1.0, .1, 6)
    vn += ugli(dx + dw * .22, dy + dh * .74, dw * .36, t, 7, 1193)
    vn += (f'<rect x="{dx+dw*.62:.0f}" y="{dy+dh*.30:.0f}" width="{dw*.3:.0f}"'
           f' height="{dh*.44:.0f}" rx="10" fill="url(#pech)" opacity=".92" {o(5)}/>')
    s += SL(Z_SRED, vn)
    stv = (f'<path d="M{dx+dw:.0f},{dy:.0f} L{dx+dw+250:.0f},{dy+110:.0f}'
           f' L{dx+dw+250:.0f},{dy+dh-60:.0f} L{dx+dw:.0f},{dy+dh:.0f} Z"'
           f' fill="url(#derev)" {o(8)}/>')
    for i in range(4):                   # доски створки в перспективе
        stv += (f'<line x1="{dx+dw+30+i*55:.0f}" y1="{dy+20+i*24:.0f}"'
                f' x2="{dx+dw+30+i*55:.0f}" y2="{dy+dh-14-i*12:.0f}"'
                f' stroke="#6b4a2a" stroke-width="9" opacity=".8"/>')
    stv += (f'<circle cx="{dx+dw+60:.0f}" cy="{dy+dh*.56:.0f}" r="20"'
            f' fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, stv)
    s += SL(Z_SRED, f'<rect x="{dx-20}" y="{dy+dh-20}" width="{dw+40}" height="46"'
                    f' rx="10" fill="{DOSKA2}" {o(7)}/>')
    s += SL(Z_SRED, podkova(dx + dw / 2, dy - 120, 2.1, t, "url(#zhel)"))
    # ВИХРЬ за порогом, крупно
    s += SL(Z_SRED, _vihr(1520, 1010, 2.1, t, True))
    # шапка вертится в вихре
    ug = (t * 420) % 360
    shx = 1520 + 150 * math.cos(t * 2.2)
    shy = 330 + 50 * math.sin(t * 2.6)
    s += SL(Z_SRED, f'<g transform="rotate({ug:.0f} {shx:.0f} {shy:.0f})">'
                    + _shapka_meh(shx, shy, 1.15, t, .3, 0.0) + '</g>')
    # мужика кружит волчком, он шагает не туда
    kruzh = A.ease(A.seg(t, 1.0, 1.6))
    mx = 1060 + kruzh * 90
    naklon = 16 * math.sin(t * 3.2)
    s += SL(Z_SRED, f'<g transform="rotate({kruzh*34:.1f} {mx:.0f} 1060)">'
                    + figura(mx, 1060, 500, t, "#2e3a46", "#cfe4f5", False, .2,
                             True, 1.0, True, naklon, True, False) + '</g>')
    s += SL(Z_SRED, para_izo_rta(mx + 60, 700, t, .2, 1.2, .55))
    for i in range(3):                   # круговые штрихи: его закрутило
        rr = 150 + i * 60
        s += SL(Z_SRED, f'<path d="M{mx-rr:.0f},{900:.0f} a{rr:.0f},{rr*.3:.0f} 0 1 0'
                        f' {rr*2:.0f},0" fill="none" stroke="#dfe8f2"'
                        f' stroke-width="{8-i*2}" opacity="{.5*kruzh:.2f}"'
                        f' stroke-dasharray="{50+i*20} {26+i*8}"'
                        f' stroke-dashoffset="{t*160:.0f}"/>')
    # жена возвращает его за ворот
    vozv = A.ease(A.seg(t, 2.6, 1.2))
    zx = 860 + 40 * vozv
    s += SL(Z_SRED, figura(zx, 1056, 470, t, "#5b2f3a", "#ffd98a", True, .5,
                           False, 1.0, False, -4.0 * vozv))
    ruk, (kx, ky) = rukav(zx + 80, 760, 260 * (.5 + .5 * vozv), -12, t,
                          "#5b2f3a", "#ffd98a", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="30" ry="22"'
                    f' fill="#5b2f3a" {o(4)}/>')
    s += SL(Z_SRED, kura(1760, 1012, t, .9, .4))
    s += SL(Z_SRED, _vedro_dach(960, 1012, 1.0, t))
    s += SL(Z_PERED, ramka_pp("levo", "#120f14", .8))
    s += SL(Z_PERED, f'<rect x="1850" y="0" width="90" height="1080"'
                     f' fill="url(#derev)" {o(9)}/>')
    s += SL(Z_LETIT, mokryy_sneg(t, 30, 1201, .55, 1.3))
    s += vinetka(.48)
    return s


# ── 86 ─────────────────────────────────────────────────────────────────────
def mokryy_sneg_na_stekle(t):
    """Окошко сеней во весь кадр: в большом стекле НАСТОЯЩИЙ мокрый снег, а
    внук рисует пальцем солнце на СОСЕДНЕЙ, запотевшей створке.

    Внутри проёма под настоящий кадр не лежит ничего нашего: ни рисунка, ни
    запотевания, ни потёков — только нарисованная подложка под меткой. Солнце
    с лицом сидело посреди проёма и перекрывало живое видео (осмотр 14.11)."""
    rnd = random.Random(8623)
    s = f'<rect width="{W}" height="{H}" fill="#241c16"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 124))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#2a1f16" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(930))
    s += SL(Z_DAL, mebel_hlam(1700, 940, 300, t, 1213))
    s += SL(Z_SRED, tusklaya_lampochka(170, 120, t, 1.15, False))
    # БОЛЬШАЯ СТВОРКА — под настоящий кадр; рядом УЗКАЯ — наша, запотевшая
    ox, oy, ow, oh = 250, 120, 940, 700
    fx, fy, fw, fh = 1270, 120, 360, 700          # форточка-створка рядом
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="mo86"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#3f4a5a"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#41506a"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.62:.0f}" width="{ow}" height="{oh*.38:.0f}"'
           f' fill="#3a4454" opacity=".9"/>')
    for i in range(4):                   # дальние избы и забор сквозь снег
        bx = ox + 40 + i * 240
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.56:.0f}" width="150"'
               f' height="{oh*.24:.0f}" fill="#4a5466" opacity=".9"/>')
        za += (f'<path d="M{bx-20:.0f},{oy+oh*.56:.0f} l95,-70 l95,70 Z"'
               f' fill="#3f4858" opacity=".95"/>')
        if i % 2 == 0:
            za += (f'<rect x="{bx+50:.0f}" y="{oy+oh*.62:.0f}" width="46"'
                   f' height="46" fill="{SVET}" opacity=".45"/>')
    for i in range(34):                  # мокрые хлопья сползают по стеклу
        x0 = ox + rnd.random() * ow
        k = ((t * .22) + rnd.random()) % 1.0
        yy = oy + k * oh
        rr = 6 + rnd.random() * 11
        za += (f'<ellipse cx="{x0:.0f}" cy="{yy:.0f}" rx="{rr*.8:.1f}"'
               f' ry="{rr*1.5:.1f}" fill="#eef5ff" opacity=".82"/>')
        za += (f'<path d="M{x0:.0f},{yy-rr:.0f} q4,{rr*2:.0f} 0,{rr*3.4:.0f}"'
               f' fill="none" stroke="#dce9f6" stroke-width="4" opacity=".5"/>')
    vid += f'<g clip-path="url(#mo86)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    # ОБВЯЗКА: короб рамы, импост между створками, наличник и подоконник
    ob = (f'<rect x="{ox-44}" y="{oy-44}" width="{fx+fw-ox+88}" height="{oh+88}"'
          f' rx="10" fill="none" stroke="url(#derev)" stroke-width="88"/>')
    ob += (f'<rect x="{ox+ow:.0f}" y="{oy}" width="{fx-ox-ow:.0f}" height="{oh}"'
           f' fill="url(#derev)" {o(6)}/>')
    ob += f'<path d="{put}" fill="none" {o(10)}/>'
    ob += (f'<path d="M{ox-110},{oy-54} h{fx+fw-ox+220} l-58,-74'
           f' h{-(fx+fw-ox)-104} Z" fill="{DOSKA2}" {o(9)}/>')
    for i in range(10):
        ob += (f'<circle cx="{ox-70+i*(fx+fw-ox+140)/9:.0f}" cy="{oy-74}" r="14"'
               f' fill="{MED}" opacity=".9" {o(2)}/>')
    ob += (f'<rect x="{ox-120}" y="{oy+oh+46}" width="{fx+fw-ox+240}" height="58"'
           f' rx="10" fill="url(#dosk)" {o(9)}/>')
    s += SL(Z_SRED, vid + ob)
    # НАША СТВОРКА: запотевшее стекло и рисунок пальцем — ВНЕ проёма со стоком
    stv = f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#44536b"/>'
    for i in range(3):                   # за нашей створкой тоже двор
        stv += (f'<path d="M{fx+30+i*110:.0f},{fy+fh*.62:.0f} l70,-60 l70,60 Z"'
                f' fill="#3f4858"/>')
        stv += (f'<rect x="{fx+34+i*110:.0f}" y="{fy+fh*.62:.0f}" width="120"'
                f' height="{fh*.22:.0f}" fill="#4a5466"/>')
    dyh = max(0.0, A.w(t, 2.2, .1))
    stv += (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#dfe9f2"'
            f' opacity="{.40+.28*dyh:.2f}"/>')
    ris = A.ease(A.seg(t, .5, 1.6))
    sx_, sy_ = fx + fw * .5, fy + fh * .42
    if ris > .02:
        stv += (f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="88" fill="none"'
                f' stroke="#f6fbff" stroke-width="15" opacity="{.95*ris:.2f}"'
                f' stroke-dasharray="{556*ris:.0f} 999"/>')
        for i in range(10):              # лучи солнышка
            a = i * .628
            lk = max(0.0, min(1.0, ris * 10 - i))
            stv += (f'<line x1="{sx_+math.cos(a)*102:.0f}"'
                    f' y1="{sy_+math.sin(a)*102:.0f}"'
                    f' x2="{sx_+math.cos(a)*(102+46*lk):.0f}"'
                    f' y2="{sy_+math.sin(a)*(102+46*lk):.0f}" stroke="#f6fbff"'
                    f' stroke-width="12" opacity="{.9*lk:.2f}"/>')
        if ris > .7:                     # улыбка и глаза
            stv += (f'<path d="M{sx_-42:.0f},{sy_+18:.0f} q42,44 84,0" fill="none"'
                    f' stroke="#f6fbff" stroke-width="13" opacity=".95"/>')
            for i in (-1, 1):
                stv += (f'<circle cx="{sx_+i*30:.0f}" cy="{sy_-24:.0f}" r="11"'
                        f' fill="#f6fbff" opacity=".95"/>')
    for i in range(5):                   # потёки по нашей створке
        stv += (f'<path d="M{fx+40+i*70:.0f},{fy+fh*.58:.0f} q6,90 -2,{fh*.38:.0f}"'
                f' fill="none" stroke="#eaf4ff" stroke-width="6" opacity=".45"/>')
    stv += (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" {o(9)}/>')
    stv += (f'<line x1="{fx}" y1="{fy+fh*.48:.0f}" x2="{fx+fw}"'
            f' y2="{fy+fh*.48:.0f}" stroke="url(#derev)" stroke-width="28"/>')
    s += SL(Z_SRED, stv)
    # ВНУК у нашей створки: дышит на стекло и ведёт пальцем
    vx = fx + fw * .5
    s += SL(Z_SRED, figura(vx, 1070, 400, t, "#6b3a44", "#ffd98a", False, .4,
                           False, 1.0, False, 1.4, False, False))
    ruk, (kx, ky) = rukav(vx - 40, 820, 230, -74 + 16 * A.w(t, 1.1), t,
                          "#6b3a44", "#ffd98a", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="26" ry="20"'
                    f' fill="#6b3a44" {o(4)}/>')
    s += SL(Z_SRED, para_izo_rta(vx + 54, 1070 - 400 * .80, t, .1, 1.3, .55))
    # тулуп возвращается на гвоздь справа, за окном
    vozv = A.ease(A.seg(t, 1.6, 1.4))
    s += SL(Z_SRED, f'<circle cx="1790" cy="300" r="14" fill="#8d949b" {o(4)}/>')
    s += SL(Z_SRED, _tulup_vis(1790 - 70 * (1 - vozv), 320 + 160 * (1 - vozv),
                               270, 400, t, .2, 0.0))
    s += SL(Z_SRED, _valenok(1760, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_SRED, _vedro_dach(130, 1012, 1.1, t))
    s += SL(Z_PERED, ramka_pp("levo", "#140f0c", .74))
    s += vinetka(.46)
    return s


# ── 87 ─────────────────────────────────────────────────────────────────────
def dym_stolbom_i_karavay(t):
    """Деревня в тихий день: из каждой трубы дым стоит ровным столбом до неба,
    бельё на верёвке не шелохнётся, флюгер-петушок замер. Самый высокий столб
    дыма на глазах превращается в пышный румяный каравай на рушнике.

    Превращение заканчивается К СЕРЕДИНЕ плана, а не тянется до конца: прежде
    в кадре весь план стоял полупрозрачный серый эллипс, и ни дымом, ни
    караваем он не читался. Бельё перенесено влево, чтобы верёвка не резала
    каравай пополам (осмотр 14.11)."""
    rnd = random.Random(8713)
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, False, 1217)
    s += SL(Z_DAL, tuman(t, 700, .34, "#dfe7ee"))
    s += SL(Z_DAL, gryaz_polosa(880, 200, "#4a443a"))
    s += SL(Z_DAL, sneg_lezhit(900, 24, "url(#sneg)"))
    # три избы: у каждой труба и свой ровный густой столб дыма
    for i, (bx, bw, hh) in enumerate(((40, 440, 300), (1440, 460, 330),
                                      (720, 280, 210))):
        iz = brevna(bx, 900 - hh, bw, hh + 60, 92)
        iz += (f'<path d="M{bx-40:.0f},{900-hh:.0f} L{bx+bw*.5:.0f},{900-hh-150:.0f}'
               f' L{bx+bw+40:.0f},{900-hh:.0f} Z" fill="#4a3b2c" {o(8)}/>')
        iz += (f'<path d="M{bx-36:.0f},{900-hh-6:.0f} L{bx+bw*.5:.0f},{900-hh-146:.0f}'
               f' L{bx+bw+36:.0f},{900-hh-6:.0f} l-46,-26 L{bx+bw*.5:.0f},'
               f'{900-hh-112:.0f} l{-bw*.5+46:.0f},{86:.0f} Z"'
               f' fill="url(#sneg)" opacity=".85"/>')
        iz += (f'<rect x="{bx+bw*.62:.0f}" y="{900-hh-250:.0f}" width="80"'
               f' height="110" fill="url(#kamen)" {o(7)}/>')
        iz += okno_izby(bx + bw * .16, 900 - hh * .62, bw * .3, hh * .34, t,
                        svet=True, moroz=.2)
        s += SL(Z_DAL, iz)
        s += SL(Z_DAL, teplo(bx + bw * .3, 900 - hh * .45, 260, 220, .3))
        # ровный столб дыма: густой, почти без вихря
        cx_ = bx + bw * .62 + 40
        stolb = ""
        for j in range(16):
            yy = 900 - hh - 250 - j * 62
            rr = 40 - j * .9 + 4 * A.w(t, 7.0, j * .06)
            stolb += (f'<ellipse cx="{cx_+3*A.w(t,8.0,j*.1):.0f}" cy="{yy:.0f}"'
                      f' rx="{max(10, rr):.0f}" ry="{max(12, rr*1.2):.0f}"'
                      f' fill="#dfe5ec" opacity="{.80-j*.030:.2f}"/>')
        s += SL(Z_DAL, stolb)
        s += SL(Z_DAL, dym(cx_, 900 - hh - 250, t, 6, .12, 300, .46, "#d8dee6", .8))
    # бельё на верёвке СЛЕВА — не шелохнётся и каравай не режет
    s += SL(Z_SRED, f'<path d="M60,700 q220,26 440,6" fill="none" stroke="#c2ab86"'
                    f' stroke-width="6"/>')
    for i, (col, ww, hh2) in enumerate(((KREM, 130, 165), (TKAN2, 115, 140),
                                        (RUSH, 140, 180))):
        bx = 130 + i * 140
        dr = .4 * A.w(t, 9.0, i * .2)
        s += SL(Z_SRED, f'<g transform="rotate({dr:.2f} {bx:.0f} {706:.0f})">'
                        f'<path d="M{bx-ww/2:.0f},{706:.0f} h{ww:.0f}'
                        f' l{-8:.0f},{hh2:.0f} q{-ww*.4:.0f},{14:.0f}'
                        f' {-ww+16:.0f},0 Z" fill="{col}" {o(5)}/>'
                        f'<rect x="{bx-ww/2-6:.0f}" y="{700:.0f}" width="{ww+12:.0f}"'
                        f' height="14" rx="6" fill="#8d949b" {o(3)}/></g>')
    # флюгер-петушок замер
    fx_, fy_ = 1760, 300
    s += SL(Z_SRED, f'<rect x="{fx_-7:.0f}" y="{fy_:.0f}" width="14" height="170"'
                    f' rx="6" fill="#5d6168" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_-70:.0f},{fy_-40:.0f} q40,-54 92,-34'
                    f' q44,18 44,56 q-4,36 -50,40 l-16,34 l-18,-34'
                    f' q-46,-8 -52,-62 Z" fill="#2f3337" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_+66:.0f},{fy_-30:.0f} l40,-16 l-6,26 l34,8'
                    f' l-62,16 Z" fill="#8a3a22" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M{fx_-74:.0f},{fy_-66:.0f} q24,-30 44,-8'
                    f' q-18,18 -44,8 Z" fill="{KRAS}" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{fx_-48:.0f}" cy="{fy_-42:.0f}" r="6"'
                    f' fill="#f2efe6"/>')
    for i in range(4):                   # лучи-указатели флюгера
        a = i * 1.5708
        s += SL(Z_SRED, f'<line x1="{fx_:.0f}" y1="{fy_+30:.0f}"'
                        f' x2="{fx_+math.cos(a)*54:.0f}" y2="{fy_+30+math.sin(a)*54:.0f}"'
                        f' stroke="#5d6168" stroke-width="7"/>')
    # СТОЛБ ДЫМА ПРЕВРАЩАЕТСЯ В КАРАВАЙ — главный предмет, крупно и непрозрачно
    prev = A.ease(A.seg(t, .25, .9))
    kx_, ky_ = 960, 420
    for j in range(8):                   # столб дыма входит прямо в каравай
        s += SL(Z_SRED, f'<ellipse cx="{kx_+4*A.w(t,7.0,j*.1):.0f}"'
                        f' cy="{760-j*44:.0f}" rx="{44-j*2:.0f}"'
                        f' ry="{48-j*2:.0f}" fill="#dfe5ec"'
                        f' opacity="{.78-j*.055:.2f}"/>')
    s += SL(Z_SRED, f'<ellipse cx="{kx_:.0f}" cy="{ky_+40:.0f}"'
                    f' rx="{46+60*(1-prev):.0f}" ry="{320*(1-prev)+60:.0f}"'
                    f' fill="#dfe5ec" opacity="{.7*(1-prev):.2f}"/>')
    kar = f'<g opacity="{prev:.2f}" transform="translate(0,{(1-prev)*-60:.0f})">'
    kar += ten(kx_, ky_ + 300, 330, 34, .45)
    kar += (f'<path d="M{kx_-350:.0f},{ky_+150:.0f} h700 l-22,156 h-656 Z"'
            f' fill="url(#rush)" {o(8)}/>')
    for i in (-1, 1):                    # концы рушника свисают
        kar += (f'<path d="M{kx_+i*340:.0f},{ky_+160:.0f} l{i*42:.0f},{44:.0f}'
                f' l{-i*20:.0f},{140:.0f} l{-i*32:.0f},{-22:.0f} Z"'
                f' fill="url(#rush)" {o(6)}/>')
    kar += (f'<path d="M{kx_-350:.0f},{ky_+198:.0f} h700" stroke="{KRAS}"'
            f' stroke-width="16" opacity=".9"/>')
    kar += (f'<path d="M{kx_-350:.0f},{ky_+270:.0f} h656" stroke="{KRAS}"'
            f' stroke-width="11" opacity=".75"/>')
    for i in range(6):                   # вышивка по рушнику — узор, не буквы
        kar += (f'<path d="M{kx_-290+i*110:.0f},{ky_+210:.0f} l28,-28 l28,28 l-28,28 Z"'
                f' fill="{KRAS}" opacity=".9"/>')
    kar += (f'<ellipse cx="{kx_:.0f}" cy="{ky_+40:.0f}" rx="320" ry="196"'
            f' fill="#a8641e" {o(9)}/>')
    kar += (f'<ellipse cx="{kx_:.0f}" cy="{ky_+16:.0f}" rx="306" ry="180"'
            f' fill="#c98c55"/>')
    kar += (f'<ellipse cx="{kx_:.0f}" cy="{ky_-2:.0f}" rx="282" ry="160"'
            f' fill="#d9a263"/>')
    kar += (f'<ellipse cx="{kx_-90:.0f}" cy="{ky_-62:.0f}" rx="140" ry="66"'
            f' fill="#e8bd84" opacity=".8"/>')
    for i in range(7):                   # насечки на румяной корке
        kar += (f'<path d="M{kx_-236+i*78:.0f},{ky_-86:.0f} q22,42 4,90"'
                f' fill="none" stroke="#a8641e" stroke-width="11" opacity=".85"/>')
    kar += (f'<path d="M{kx_-260:.0f},{ky_+72:.0f} q260,54 520,0" fill="none"'
            f' stroke="#a8641e" stroke-width="9" opacity=".6"/>')
    for i in range(5):                   # верхушка-завиток из теста
        a = -2.0 + i * .5
        kar += (f'<ellipse cx="{kx_+math.cos(a)*110:.0f}"'
                f' cy="{ky_-120+math.sin(a)*26:.0f}" rx="44" ry="24"'
                f' fill="#e8bd84" {o(5)}/>')
    kar += '</g>'
    s += SL(Z_SRED, kar)
    s += SL(Z_SRED, par(kx_, ky_ - 190, t, 6, .5 * prev + .05, 280, .45, 1.5))
    s += SL(Z_SRED, teplo(kx_, ky_ + 20, 660 * prev, 470 * prev, .32 * prev))
    s += SL(Z_SRED, figura(360, 1060, 460, t, "#3a3346", "#ffd0a0", False, .3,
                           True, 1.0, True, 1.0, True))
    s += SL(Z_SRED, para_izo_rta(410, 700, t, .2, 1.2, .5))
    s += SL(Z_SRED, figura(210, 1066, 330, t, "#5b2f3a", "#ffd0a0", True, .6,
                           True, 1.0, False, 1.2))
    # фонарь у ближней избы: без живого огня кадр оставался сине-серым
    s += SL(Z_SRED, f'<rect x="1696" y="640" width="18" height="250" rx="8"'
                    f' fill="#3a3f46" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1652,640 h106 l-16,-42 h-74 Z" fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M1662,640 h86 l-10,112 h-66 Z" fill="url(#stekl)"'
                    f' opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, ogon(1705, 716, t, .95, .3, 5))
    s += SL(Z_SRED, teplo(1705, 690, 620, 540, .46 + .12 * abs(A.w(t, 1.6))))
    s += SL(Z_SRED, kura(1300, 1012, t, 1.0, .2))
    s += SL(Z_SRED, kura(1400, 1012, t, .9, .6))
    s += SL(Z_SRED, pleten(540, 1046, 420, 170, 8))
    s += SL(Z_PERED, goloe_derevo(110, 1080, 680, t, 1223, 7, "#2e3038"))
    s += SL(Z_PERED, ramka_pp("pravo", "#191510", .72))
    s += vinetka(.42)
    return s


# ── 88 ─────────────────────────────────────────────────────────────────────
def seyatel_i_risovannyy_veter(t):
    """Окно сарая: за стеклом НАСТОЯЩИЕ деревья гнутся под ветром. Слева от
    окна мужик с лукошком зерна уже замахнулся сеять, но рисованный Ветер над
    крышей качает головой — зерно сыплется обратно в мешок.

    Проём чистый: сеятель и лукошко стоят СЛЕВА ОТ окна, Ветер — НАД ним, и
    жердей поверх стекла больше нет. Прежде мужик закрывал нижнюю половину
    настоящего кадра, а Ветер — его правый край (осмотр 14.11)."""
    rnd = random.Random(8819)
    s = f'<rect width="{W}" height="{H}" fill="#2b2118"/>'
    s += SL(Z_DAL, doski(0, 0, W, 1080, 104, True, "dosk"))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#372a1c" opacity=".5"/>')
    s += SL(Z_DAL, svody(t, "#4b3f31", 3))
    s += SL(Z_DAL, polovicy(900))
    s += SL(Z_DAL, utvar_pekarni(120, 300, 300, t, 1229))
    # ОКНО САРАЯ справа: рисованный вид, метка, рама поверх
    ox, oy, ow, oh = 900, 300, 900, 560
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="sa88"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="url(#nsumer)"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#9fb0c2"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.64:.0f}" width="{ow}" height="{oh*.36:.0f}"'
           f' fill="#7d8a6a" opacity=".92"/>')
    for i in range(4):                   # деревья за стеклом гнутся
        gib = 11 * A.w(t, 1.1, i * .22)
        tx_ = ox + 110 + i * 230
        za += (f'<g transform="rotate({gib:.1f} {tx_:.0f} {oy+oh*.70:.0f})">'
               f'<path d="M{tx_-18:.0f},{oy+oh*.70:.0f} l9,{-oh*.44:.0f}'
               f' l18,0 l9,{oh*.44:.0f} Z" fill="#6b5a46" {o(5)}/>')
        for j in range(5):
            a = -2.4 + j * .5
            za += (f'<path d="M{tx_:.0f},{oy+oh*(.40+j*.04):.0f}'
                   f' q{math.cos(a)*60:.0f},{math.sin(a)*40:.0f}'
                   f' {math.cos(a)*120:.0f},{math.sin(a)*58:.0f}" fill="none"'
                   f' stroke="#4f4335" stroke-width="{10-j}"/>')
        za += '</g>'
    for i in range(20):                  # сор летит по ветру
        k = ((t * .7) + i * .05) % 1.0
        za += (f'<path d="M{ox+k*ow:.0f},{oy+oh*(.3+(i%6)*.09)+20*A.w(t,2.0,i*.1):.0f}'
               f' l22,-8 l-6,14 Z" fill="#8a7a5a" opacity=".8"/>')
    vid += f'<g clip-path="url(#sa88)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    ob = (f'<rect x="{ox-44}" y="{oy-44}" width="{ow+88}" height="{oh+88}" rx="8"'
          f' fill="none" stroke="url(#derev)" stroke-width="88"/>')
    ob += (f'<rect x="{ox+ow/2-15:.0f}" y="{oy}" width="30" height="{oh}"'
           f' fill="url(#derev)"/>')
    ob += (f'<line x1="{ox}" y1="{oy+oh*.5:.0f}" x2="{ox+ow}" y2="{oy+oh*.5:.0f}"'
           f' stroke="url(#derev)" stroke-width="30"/>')
    ob += f'<path d="{put}" fill="none" {o(10)}/>'
    ob += (f'<path d="M{ox-100},{oy-54} h{ow+200} l-56,-70 h{-ow-88} Z"'
           f' fill="{DOSKA2}" {o(9)}/>')
    ob += (f'<rect x="{ox-110}" y="{oy+oh+48}" width="{ow+220}" height="50" rx="10"'
           f' fill="url(#dosk)" {o(9)}/>')
    s += SL(Z_SRED, vid + ob)
    for i in range(4):                   # косые жерди сарая — ПО СТЕНЕ, не по стеклу
        s += SL(Z_SRED, f'<line x1="20" y1="{120+i*210:.0f}" x2="{ox-150:.0f}"'
                        f' y2="{90+i*210:.0f}" stroke="#6b5234" stroke-width="14"'
                        f' opacity=".7"/>')
    s += SL(Z_SRED, lampa(1860, 230, t, 1.0, False))
    s += SL(Z_SRED, teplo(1860, 270, 560, 480, .4 + .1 * abs(A.w(t, 1.5))))
    # РИСОВАННЫЙ ВЕТЕР — НАД ОКНОМ, у самого верха кадра
    vx, vy = 650, 190
    kach = 26 * A.w(t, 1.2, .1)
    vet = f'<g transform="rotate({kach*.3:.1f} {vx:.0f} {vy:.0f})">'
    for i in range(5):                   # щёки-облака
        rr = 128 - i * 14
        vet += (f'<ellipse cx="{vx+i*20-38+kach*.6:.0f}" cy="{vy+i*9-16:.0f}"'
                f' rx="{rr:.0f}" ry="{rr*.74:.0f}" fill="#cdd9e6"'
                f' opacity="{.5-i*.06:.2f}"/>')
    vet += (f'<ellipse cx="{vx+kach*.6:.0f}" cy="{vy:.0f}" rx="178" ry="142"'
            f' fill="#dde7f2" opacity=".94" {o(6)}/>')
    vet += _rozhica(vx + kach * .6, vy - 12, 118, t, .2, False, "#3f4a58")
    for i in range(6):                   # струи ветра изо рта
        k = ((t * .9) + i * .17) % 1.0
        vet += (f'<path d="M{vx+150+kach*.6+k*240:.0f},{vy+70+i*16-k*26:.0f}'
                f' q70,{-18+i*7:.0f} 150,{6:.0f}" fill="none" stroke="#e8f1f8"'
                f' stroke-width="{9-i:.0f}" opacity="{.6*(1-k):.2f}"/>')
    vet += '</g>'
    s += SL(Z_SRED, vet)
    # СЕЯТЕЛЬ СЛЕВА ОТ ОКНА: лукошко у него перед грудью, проёма не касается
    mx = 450
    s += SL(Z_SRED, figura(mx, 1066, 620, t, "#4a3a2c", "#ffd98a", False, .2,
                           True, 1.0, False, 2.0, True))
    zam = A.w(t, 1.4, .1)
    ruk, (kx, ky) = rukav(mx + 120, 720, 160, 22 + 16 * zam, t, "#4a3a2c",
                          "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    luk_x, luk_y = mx + 180, 880
    luk = (f'<path d="M{luk_x-170:.0f},{luk_y-220:.0f} h340 l-46,220 h-248 Z"'
           f' fill="url(#solom)" {o(9)}/>')
    for i in range(6):               # лоза лукошка
        luk += (f'<path d="M{luk_x-162+i*8:.0f},{luk_y-198+i*36:.0f}'
                f' q{160-i*8:.0f},{20:.0f} {322-i*16:.0f},0" fill="none"'
                f' stroke="#b78a46" stroke-width="11"/>')
    luk += (f'<ellipse cx="{luk_x:.0f}" cy="{luk_y-220:.0f}" rx="170" ry="38"'
            f' fill="#d8b96a" {o(7)}/>')
    for i in range(30):              # зерно горкой с верхом
        a = rnd.uniform(0, 6.283); rr = rnd.uniform(0, 1) ** .5 * 152
        luk += (f'<ellipse cx="{luk_x+math.cos(a)*rr:.0f}"'
                f' cy="{luk_y-244+math.sin(a)*rr*.20+3*A.w(t,2.2,i*.1):.0f}"'
                f' rx="13" ry="9" fill="#e3c272" {o(3)}/>')
    luk += (f'<path d="M{luk_x-170:.0f},{luk_y-214:.0f} q{170:.0f},{-116:.0f}'
            f' {340:.0f},0" fill="none" stroke="#9a7238" stroke-width="16"/>')
    s += SL(Z_SRED, luk)
    syp = A.ease(A.seg(t, .6, 1.8))
    msx, msy = 150, 1030
    for i in range(20):                  # зерно сыплется ОБРАТНО в мешок
        p = ((t * .9) + i * .05) % 1.0
        xx = luk_x + (msx - luk_x) * p
        yy = luk_y - 150 + (msy - 260 - (luk_y - 150)) * p + 170 * p * p
        s += SL(Z_SRED, f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="7" ry="5"'
                        f' fill="#e3c272" opacity="{.95*syp*(1-p*.3):.2f}"/>')
    # мешок завязывается
    zav = A.ease(A.seg(t, 2.2, 1.0))
    mesh = (f'<path d="M{msx-140:.0f},{msy:.0f} q{-36:.0f},{-190:.0f} {10:.0f},{-282:.0f}'
            f' q{130:.0f},{-38:.0f} {260:.0f},0 q{46:.0f},{94:.0f} {10:.0f},{282:.0f} Z"'
            f' fill="url(#solom)" {o(9)}/>')
    mesh += (f'<path d="M{msx-130:.0f},{msy-170:.0f} q{140:.0f},{28:.0f} {270:.0f},0"'
             f' fill="none" stroke="#a07c2e" stroke-width="11" opacity=".7"/>')
    gor = 130 - 84 * zav
    mesh += (f'<path d="M{msx-gor:.0f},{msy-282:.0f} q{gor:.0f},{-66:.0f}'
             f' {gor*2:.0f},0 q{-gor*.5:.0f},{-38:.0f} {-gor*2:.0f},0 Z"'
             f' fill="#d8b96a" {o(6)}/>')
    mesh += (f'<path d="M{msx-gor:.0f},{msy-298:.0f} q{gor:.0f},{38:.0f} {gor*2:.0f},0"'
             f' fill="none" stroke="#6b4a2a" stroke-width="{10+8*zav:.0f}"/>')
    if zav > .5:
        mesh += (f'<path d="M{msx-20:.0f},{msy-310:.0f} q{-40:.0f},{-40:.0f}'
                 f' {-70:.0f},{-14:.0f}" fill="none" stroke="#6b4a2a"'
                 f' stroke-width="8"/>')
        mesh += (f'<path d="M{msx+20:.0f},{msy-310:.0f} q{40:.0f},{-40:.0f}'
                 f' {70:.0f},{-14:.0f}" fill="none" stroke="#6b4a2a"'
                 f' stroke-width="8"/>')
    s += SL(Z_SRED, mesh)
    s += SL(Z_SRED, kura(840, 1000, t, 1.2, .4))
    s += SL(Z_PERED, ramka_pp("levo", "#150f0a", .72))
    s += SL(Z_LETIT, iskra_let(t, 1860, 280, 6, 1237, 240, .3))
    s += vinetka(.46)
    return s


# ── 89 ─────────────────────────────────────────────────────────────────────
def myshi_gotovyatsya_k_zime(t):
    """Разрез пола и стены избы: в подполе кипит мышиный переезд — мыши в
    платочках катят орехи, тащат колоски, одна несёт на спине перину из пуха,
    другая заколачивает дощечкой вход в норку. Хозяйка сверху прислушивается."""
    rnd = random.Random(8923)
    s = f'<rect width="{W}" height="{H}" fill="#1d1712"/>'
    # верх: изба в разрезе
    s += SL(Z_DAL, brevna(0, 0, W, 470, 108))
    s += SL(Z_DAL, f'<rect width="{W}" height="470" fill="#2a2018" opacity=".48"/>')
    s += SL(Z_DAL, utvar_izby(1480, 60, 400, t, 1249))
    s += SL(Z_SRED, f'<rect y="470" width="{W}" height="60" fill="url(#pol)" {o(7)}/>')
    for i in range(11):
        s += SL(Z_SRED, f'<line x1="{i*176:.0f}" y1="470" x2="{i*176:.0f}" y2="530"'
                        f' stroke="#4e3220" stroke-width="5" opacity=".7"/>')
    s += SL(Z_SRED, f'<rect y="530" width="{W}" height="26" fill="#3f2a18" {o(5)}/>')
    # хозяйка прислушивается, со свечой
    hx = 1180
    s += SL(Z_SRED, figura(hx, 470, 420, t, "#4a2f3a", "#ffd98a", True, .3,
                           True, 1.0, False, 3.0))
    s += SL(Z_SRED, svecha(hx - 150, 300, t, .2, 1.5, 100))
    s += SL(Z_SRED, teplo(hx - 150, 250, 560, 460, .46 + .12 * abs(A.w(t, 1.5))))
    for i in range(3):                   # дужки «слышно»
        k = ((t * .8) + i * .33) % 1.0
        s += SL(Z_SRED, f'<path d="M{hx+90:.0f},{300-k*60:.0f} q40,{-26:.0f}'
                        f' {30-k*20:.0f},{-60:.0f}" fill="none" stroke="#ffe6b8"'
                        f' stroke-width="6" opacity="{.6*(1-k):.2f}"/>')
    s += SL(Z_SRED, lavka(180, 380, 420))
    s += SL(Z_SRED, krynka(300, 376, 1.3))
    s += SL(Z_SRED, karavay(520, 374, .8, True))
    # ПОДПОЛ: земляной разрез, норки, мышиный переезд
    s += SL(Z_SRED, f'<rect y="556" width="{W}" height="524" fill="#6b5240"/>')
    for i in range(70):                  # земля комками
        s += SL(Z_SRED, f'<circle cx="{rnd.random()*W:.0f}"'
                        f' cy="{570+rnd.random()*500:.0f}"'
                        f' r="{rnd.uniform(5,20):.0f}" fill="#8a6c52"'
                        f' opacity="{rnd.uniform(.3,.7):.2f}"/>')
    s += SL(Z_SRED, f'<rect y="556" width="{W}" height="22" fill="#5a4530" {o(4)}/>')
    for i, (nx, nr) in enumerate(((240, 110), (1020, 92), (1700, 120))):
        s += SL(Z_SRED, f'<path d="M{nx-nr:.0f},1080 q0,{-nr*1.5:.0f} {nr:.0f},'
                        f'{-nr*1.5:.0f} q{nr:.0f},0 {nr:.0f},{nr*1.5:.0f} Z"'
                        f' fill="#1a120c" {o(6)}/>')
    s += SL(Z_SRED, teplo(1020, 900, 420, 300, .14))
    # мыши катят орехи
    for i in range(3):
        p = ((t * .22) + i * .3) % 1.0
        mxx = 200 + p * 900
        s += SL(Z_SRED, f'<circle cx="{mxx+130:.0f}" cy="{886+i*58:.0f}"'
                        f' r="{56-i*6:.0f}" fill="#9c6a3c" {o(5)}/>')
        s += SL(Z_SRED, f'<path d="M{mxx+96:.0f},{880+i*58:.0f} q34,{-30:.0f}'
                        f' {68:.0f},0" fill="none" stroke="#6b4a2a" stroke-width="8"/>')
        s += SL(Z_SRED, _mysh(mxx, 898 + i * 58, 2.3 - i * .25, t, i * .3, True))
    # мышь тащит колосок
    kp = ((t * .18) + .4) % 1.0
    kxx = 1500 - kp * 700
    s += SL(Z_SRED, _mysh(kxx, 760, 2.4, t, .5, True))
    s += SL(Z_SRED, f'<path d="M{kxx+70:.0f},{752:.0f} q140,-40 300,-72"'
                    f' fill="none" stroke="#a07c2e" stroke-width="11"/>')
    for i in range(11):                  # зёрна колоска парами, с усиками
        gxx = kxx + 160 + i * 20
        gyy = 726 - i * 5 + 4 * A.w(t, 2.2, i * .1)
        for sg in (-1, 1):
            s += SL(Z_SRED, f'<ellipse cx="{gxx:.0f}" cy="{gyy+sg*13:.0f}"'
                            f' rx="16" ry="11" fill="#e3c272" {o(3)}/>')
            s += SL(Z_SRED, f'<line x1="{gxx+10:.0f}" y1="{gyy+sg*13:.0f}"'
                            f' x2="{gxx+40:.0f}" y2="{gyy+sg*30:.0f}"'
                            f' stroke="#c9a04a" stroke-width="4"/>')
    # мышь с периной из пуха на спине
    pp = ((t * .16) + .7) % 1.0
    pxx = 300 + pp * 1200
    s += SL(Z_SRED, _mysh(pxx, 1010, 2.5, t, .2, True))
    s += SL(Z_SRED, f'<ellipse cx="{pxx-10:.0f}" cy="{906+6*A.w(t,1.2,.2):.0f}"'
                    f' rx="130" ry="68" fill="#f2efe6" {o(6)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{pxx-70+i*22:.0f},{920:.0f} q8,{-16:.0f} 16,{-2:.0f}"'
                        f' fill="none" stroke="#dfe3e8" stroke-width="6"/>')
    for i in range(6):                   # пушинки летят
        k = ((t * .5) + i * .17) % 1.0
        s += SL(Z_LETIT, f'<circle cx="{pxx+60+k*120:.0f}" cy="{910-k*90:.0f}"'
                         f' r="{6+5*k:.0f}" fill="#f6f6f2"'
                         f' opacity="{.6*(1-k):.2f}"/>')
    # мышь заколачивает дощечкой вход в норку
    zx_, zy_ = 1700, 1000
    s += SL(Z_SRED, _mysh(zx_ - 150, zy_ + 20, 2.3, t, .7, True))
    s += SL(Z_SRED, f'<rect x="{zx_-70:.0f}" y="{zy_-80:.0f}" width="200" height="34"'
                    f' rx="6" fill="url(#dosk)" {o(5)}/>')
    stuk = max(0.0, A.w(t, .9, .1))
    s += SL(Z_SRED, f'<g transform="rotate({-30+34*stuk:.1f} {zx_-60:.0f} {zy_-100:.0f})">'
                    f'<rect x="{zx_-70:.0f}" y="{zy_-170:.0f}" width="22" height="80"'
                    f' rx="6" fill="url(#derev)" {o(4)}/>'
                    f'<rect x="{zx_-96:.0f}" y="{zy_-196:.0f}" width="74" height="34"'
                    f' rx="8" fill="#5d6168" {o(4)}/></g>')
    if stuk > .85:
        for i in range(5):
            a = -2.4 + i * .5
            s += SL(Z_SRED, f'<line x1="{zx_-56:.0f}" y1="{zy_-96:.0f}"'
                            f' x2="{zx_-56+math.cos(a)*42:.0f}"'
                            f' y2="{zy_-96+math.sin(a)*42:.0f}" stroke="#ffe6b8"'
                            f' stroke-width="6" opacity=".7"/>')
    for i in range(2):                   # припасы в подполе
        s += SL(Z_SRED, _banka_krupy(560 + i * 150, 1000, 1.5, t))
    s += SL(Z_SRED, kartoshka(430, 1040, t, 11, 1259, 1.3))
    s += SL(Z_PERED, f'<rect x="0" y="470" width="90" height="610"'
                     f' fill="url(#brev)" {o(9)}/>')
    s += SL(Z_PERED, ramka_pp("pravo", "#120d0a", .7))
    s += SL(Z_PERED, kot(170, 540, t, 1.3, "#3b3430", False))
    s += vinetka(.5)
    return s


def _banka_krupy(x, y, s_=1.0, t=0.0, zerno="url(#solom)"):
    """Банка крупы в подполе: стекло, крышка-кружок, уровень зерна, блик."""
    w_, hh = 46 * s_, 110 * s_
    s = ten(x, y + 5 * s_, w_ * .9, 8 * s_, .35)
    s += (f'<path d="M{x-w_:.0f},{y-hh:.0f} h{w_*2:.0f} l{-5*s_:.0f},{hh:.0f}'
          f' h{-w_*2+10*s_:.0f} Z" fill="url(#stekl)" opacity=".75" {o(4)}/>')
    s += (f'<path d="M{x-w_*.9:.0f},{y-hh*.6:.0f} h{w_*1.8:.0f} l{-4*s_:.0f},'
          f'{hh*.58:.0f} h{-w_*1.8+8*s_:.0f} Z" fill="{zerno}" {o(3)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh*.6:.0f}" rx="{w_*.9:.0f}" ry="{7*s_:.0f}"'
          f' fill="#d8b96a" opacity=".9"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-hh:.0f}" rx="{w_*1.1:.0f}" ry="{9*s_:.0f}"'
          f' fill="url(#zhel)" {o(3)}/>')
    s += (f'<line x1="{x-w_*.5:.0f}" y1="{y-hh*.9:.0f}" x2="{x-w_*.5:.0f}"'
          f' y2="{y-hh*.2:.0f}" stroke="#ffffff" stroke-width="{7*s_:.0f}"'
          f' opacity="{.2+.2*abs(A.w(t,2.8,x*.002)):.2f}"/>')
    return s


# ── 90 ─────────────────────────────────────────────────────────────────────
def komar_na_noyabrskom_okne(t):
    """Оконное стекло с первым инеем по краям: по нему, как по катку, деловито
    идёт большой рисованный комар в шарфе и с саквояжем. Газета замахивается
    и опускается, дед улыбается, комар раскланивается."""
    rnd = random.Random(9029)
    s = f'<rect width="{W}" height="{H}" fill="#2a2420"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 122))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#30241a" opacity=".45"/>')
    s += SL(Z_DAL, polovicy(950, "url(#pol)"))
    s += SL(Z_DAL, utvar_izby(60, 240, 300, t, 1277))
    # окно крупно: за стеклом сумерки, по краям иней
    ox, oy, ow, oh = 420, 110, 1120, 700
    s += SL(Z_SRED, f'<rect x="{ox-54}" y="{oy-54}" width="{ow+108}"'
                    f' height="{oh+108}" rx="10" fill="url(#derev)" {o(10)}/>')
    st_ = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#3e4a60"/>')
    st_ += (f'<rect x="{ox}" y="{oy+oh*.60:.0f}" width="{ow}" height="{oh*.40:.0f}"'
            f' fill="#333c4e" opacity=".92"/>')
    for i in range(5):                   # дальние дома и огоньки за стеклом
        bx = ox + 30 + i * 226
        st_ += (f'<rect x="{bx:.0f}" y="{oy+oh*.52:.0f}" width="140"'
                f' height="{oh*.26:.0f}" fill="#3a4354" opacity=".9"/>')
        st_ += (f'<path d="M{bx-18:.0f},{oy+oh*.52:.0f} l88,-66 l88,66 Z"'
                f' fill="#333b4a" opacity=".95"/>')
        if i % 2:
            st_ += (f'<rect x="{bx+48:.0f}" y="{oy+oh*.58:.0f}" width="44"'
                    f' height="44" fill="{SVET}"'
                    f' opacity="{.4+.25*abs(A.w(t,2.2,i*.3)):.2f}"/>')
    st_ += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#stekl)"'
            f' opacity=".30"/>')
    for i in range(16):                  # иней по краям стекла
        side = i % 4
        if side == 0:
            cx_, cy_ = ox + rnd.random() * ow, oy + rnd.random() * 90
        elif side == 1:
            cx_, cy_ = ox + rnd.random() * ow, oy + oh - rnd.random() * 90
        elif side == 2:
            cx_, cy_ = ox + rnd.random() * 110, oy + rnd.random() * oh
        else:
            cx_, cy_ = ox + ow - rnd.random() * 110, oy + rnd.random() * oh
        rr = (12 + rnd.random() * 22) * (.7 + .3 * abs(A.w(t, 8 + i * .3, i * .1)))
        st_ += (f'<circle cx="{cx_:.0f}" cy="{cy_:.0f}" r="{rr:.0f}" fill="#e8f4ff"'
                f' opacity=".24"/>')
        for j in range(5):
            a = j * 1.25
            st_ += (f'<line x1="{cx_:.0f}" y1="{cy_:.0f}"'
                    f' x2="{cx_+math.cos(a)*rr:.0f}" y2="{cy_+math.sin(a)*rr:.0f}"'
                    f' stroke="#f2faff" stroke-width="3" opacity=".4"/>')
    s += SL(Z_SRED, st_)
    s += SL(Z_SRED, f'<line x1="{ox+ow/2:.0f}" y1="{oy}" x2="{ox+ow/2:.0f}"'
                    f' y2="{oy+oh}" stroke="url(#derev)" stroke-width="32"/>'
                    f'<line x1="{ox}" y1="{oy+oh*.5:.0f}" x2="{ox+ow}"'
                    f' y2="{oy+oh*.5:.0f}" stroke="url(#derev)" stroke-width="32"/>')
    s += SL(Z_SRED, f'<rect x="{ox-100}" y="{oy+oh+54}" width="{ow+200}" height="56"'
                    f' rx="10" fill="url(#dosk)" {o(9)}/>')
    # КОМАР идёт по стеклу, крупно
    hod = A.ease(A.seg(t, .2, 2.2))
    kx_ = ox + 180 + hod * 560
    ky_ = oy + oh * .48 + 26 * A.w(t, 1.5)
    s += SL(Z_SRED, _komar(kx_, ky_, 4.6, t, .1, True))
    for i in range(7):                   # следы-царапины на стекле
        p = i / 6
        s += SL(Z_SRED, f'<path d="M{ox+180+p*hod*560:.0f},{ky_+70:.0f} l24,8"'
                        f' stroke="#eaf4ff" stroke-width="5" opacity=".4"/>')
    # газета замахивается и опускается
    zam = A.ease(A.seg(t, 1.6, .5)) - A.ease(A.seg(t, 2.3, .7))
    gx_, gy_ = kx_ + 480, ky_ - 90 - zam * 120
    ruk, (rx_, ry_) = rukav(gx_ + 170, gy_ + 230, 130, -118 + 40 * zam, t,
                            "#3a3346", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, _gazeta_list(gx_, gy_, 480, 350, t, -20 + 36 * zam, 1279, 0.0))
    # дед улыбается, лампа рядом
    dx_ = 1700
    s += SL(Z_SRED, figura(dx_, 1070, 520, t, "#3a3346", "#ffd98a", False, .2,
                           True, 1.0, True, 1.4, True))
    s += SL(Z_SRED, _lampa_abazhur(250, 700, t, 1.9, 1.0))
    s += SL(Z_SRED, teplo(250, 520, 820, 700, .48 + .1 * abs(A.w(t, 1.6))))
    # комар раскланивается: шляпу долой
    rask = A.ease(A.seg(t, 2.6, .8))
    if rask > .02:
        s += SL(Z_SRED, f'<g transform="rotate({-26*rask:.1f} {kx_:.0f} {ky_:.0f})">'
                        f'<ellipse cx="{kx_+150:.0f}" cy="{ky_-110:.0f}" rx="56"'
                        f' ry="18" fill="#2b2a30" {o(4)}/>'
                        f'<path d="M{kx_+118:.0f},{ky_-112:.0f} q32,-52 64,0 Z"'
                        f' fill="#3a3842" {o(4)}/></g>')
    s += SL(Z_SRED, _chashka(1280, 940, 1.4, t, .3, KREM, True))
    s += SL(Z_SRED, par(1280, 866, t, 3, .4, 160, .4, .8))
    s += SL(Z_SRED, hodiki(1760, 300, t, 1.1))
    s += SL(Z_SRED, kot(620, 1012, t, 1.2, "#3b3430", True))
    s += SL(Z_PERED, zanaveska(380, 60, 440, 190, TKAN, t, 1))
    s += SL(Z_PERED, zanaveska(1580, 60, 440, 190, TKAN, t, -1))
    s += SL(Z_PERED, _chugunok(170, 1012, 1.2, t, True))
    s += vinetka(.46)
    return s


# ── 91 ─────────────────────────────────────────────────────────────────────
def gorodskoe_okno_s_chashkoy(t):
    """Широкое окно городской квартиры: за стеклом НАСТОЯЩЕЕ небо с солнцем,
    на подоконнике по краям — чашка чая и очки, человек в халате со спины.

    Из проёма убрано всё наше: чашка, цветок, ящик, ползунок ручки и три
    зелёные галочки. Вещи стоят на подоконнике ЗА пределами стекла, галочки
    отмечены на настенном листке сбоку. Прежде проём со стоком был завален
    нашими предметами целиком (осмотр 14.11)."""
    rnd = random.Random(9137)
    s = f'<rect width="{W}" height="{H}" fill="#2e2a26"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#6e6558"/>')
    for i in range(10):                  # обои тонкой полоской
        s += SL(Z_DAL, f'<rect x="{i*196:.0f}" y="0" width="70" height="1080"'
                       f' fill="#7a7164" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(930, "#6b4a2a"))
    s += SL(Z_SRED, tusklaya_lampochka(960, 70, t, 1.1, True))
    # ОКНО: проём по центру, но УЖЕ подоконника — вещи встают по его краям
    ox, oy, ow, oh = 540, 110, 900, 510
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="go91"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="url(#nden)"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#nden)"/>')
    sx_, sy_ = ox + ow * .72, oy + oh * .26
    za += (f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="{80+5*A.w(t,2.4):.0f}"'
           f' fill="#fff3cf" opacity=".95"/>')
    for i in range(14):                  # лучи солнца за стеклом
        a = i * .449 + t * .1
        za += (f'<line x1="{sx_:.0f}" y1="{sy_:.0f}"'
               f' x2="{sx_+math.cos(a)*(140+28*abs(A.w(t,2.0,i*.1))):.0f}"'
               f' y2="{sy_+math.sin(a)*(140+28*abs(A.w(t,2.0,i*.1))):.0f}"'
               f' stroke="#ffeeb8" stroke-width="8" opacity=".55"/>')
    for i in range(6):                   # облака плывут
        k = ((t * .03) + i * .18) % 1.2 - .1
        cx_ = ox - 180 + k * (ow + 360)
        cy_ = oy + 110 + (i % 3) * 86
        za += (f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="{130+i*18:.0f}"'
               f' ry="{38+i*6:.0f}" fill="#f4f8fc" opacity=".7"/>')
        za += (f'<ellipse cx="{cx_+80:.0f}" cy="{cy_+14:.0f}" rx="{94+i*11:.0f}"'
               f' ry="{28+i*5:.0f}" fill="#e8f0f8" opacity=".6"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.68:.0f}" width="{ow}" height="{oh*.32:.0f}"'
           f' fill="#8a949c" opacity=".6"/>')
    for i in range(5):                   # панельки города за стеклом
        bx = ox + 20 + i * 184
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.54:.0f}" width="150"'
               f' height="{oh*.32:.0f}" fill="#79838c" opacity=".85"/>')
        for j in range(8):
            za += (f'<rect x="{bx+14+(j % 4)*34:.0f}"'
                   f' y="{oy+oh*.58+(j//4)*48:.0f}" width="22" height="30"'
                   f' fill="#9fa9b0" opacity=".8"/>')
    vid += f'<g clip-path="url(#go91)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    # обвязка: пластиковый короб рамы, импост, откосы, широкий подоконник
    ob = (f'<rect x="{ox-50}" y="{oy-50}" width="{ow+100}" height="{oh+100}" rx="8"'
          f' fill="none" stroke="#e8e4da" stroke-width="100"/>')
    ob += (f'<line x1="{ox+ow*.46:.0f}" y1="{oy}" x2="{ox+ow*.46:.0f}"'
           f' y2="{oy+oh}" stroke="#e8e4da" stroke-width="36"/>')
    ob += f'<path d="{put}" fill="none" {o(8)}/>'
    ob += (f'<path d="M{ox+40},{oy+60} l{ow*.26:.0f},{oh*.40:.0f}" stroke="#ffffff"'
           f' stroke-width="18" opacity=".2"/>')
    ob += (f'<rect x="{ox-310}" y="{oy+oh+54}" width="{ow+620}" height="70" rx="12"'
           f' fill="#efebe2" {o(8)}/>')
    ob += (f'<rect x="{ox-310}" y="{oy+oh+54}" width="{ow+620}" height="18" rx="9"'
           f' fill="#ffffff" opacity=".55"/>')
    s += SL(Z_SRED, vid + ob)
    pw_y = oy + oh + 54                  # уровень подоконника
    # ПОДОКОННИК СЛЕВА: чашка чая с паром и очки — левее стекла
    s += SL(Z_SRED, _chashka(ox - 130, pw_y, 2.6, t, .2, KREM, True))
    s += SL(Z_SRED, par(ox - 130, pw_y - 170, t, 6, .6, 280, .42, 1.2))
    s += SL(Z_SRED, _ochki(ox - 270, pw_y - 24, 1.3, t, False))
    # ПОДОКОННИК СПРАВА: горшок с цветком — правее стекла
    s += SL(Z_SRED, f'<path d="M{ox+ow+150:.0f},{pw_y-140:.0f} h150 l-18,140 h-114 Z"'
                    f' fill="url(#glina)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{ox+ow+142:.0f}" y="{pw_y-154:.0f}" width="166"'
                    f' height="26" rx="8" fill="#b07a46" {o(5)}/>')
    for i in range(5):                   # домашний цветок
        a = -1.2 + i * .5
        s += SL(Z_SRED, f'<path d="M{ox+ow+225:.0f},{pw_y-150:.0f}'
                        f' q{math.cos(a)*44:.0f},{-66:.0f}'
                        f' {math.cos(a)*78+6*A.w(t,2.4,i*.2):.0f},{-120:.0f}"'
                        f' fill="none" stroke="{ZEL2}" stroke-width="{12-i}"'
                        f' stroke-linecap="round"/>')
        s += SL(Z_SRED, f'<ellipse cx="{ox+ow+225+math.cos(a)*80:.0f}"'
                        f' cy="{pw_y-272:.0f}" rx="30" ry="16" fill="#56763f"'
                        f' {o(3)}/>')
    # ЛИСТОК НА СТЕНЕ СПРАВА: три галочки встают на нём по словам
    lx_, ly_ = 1700, 250
    s += SL(Z_SRED, f'<rect x="{lx_-110:.0f}" y="{ly_-130:.0f}" width="220"'
                    f' height="300" rx="10" fill="url(#list)" {o(7)}/>')
    s += SL(Z_SRED, f'<circle cx="{lx_:.0f}" cy="{ly_-144:.0f}" r="12"'
                    f' fill="{ZHELEZ}" {o(3)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<line x1="{lx_-66:.0f}" y1="{ly_-30+i*76:.0f}"'
                        f' x2="{lx_+76:.0f}" y2="{ly_-30+i*76:.0f}"'
                        f' stroke="#d6cbae" stroke-width="6"/>')
        gk = A.out(A.seg(t, 1.2 + i * .4, .5))
        if gk > .02:
            gx_ = lx_ - 74
            gy_ = ly_ - 44 + i * 76
            s += SL(Z_SRED, f'<path d="M{gx_:.0f},{gy_:.0f} l{24*gk:.0f},{24*gk:.0f}'
                            f' l{46*gk:.0f},{-60*gk:.0f}" fill="none" stroke="#5ec07a"'
                            f' stroke-width="16" stroke-linecap="round"'
                            f' opacity="{.95*gk:.2f}"/>')
    # ЧЕЛОВЕК В ХАЛАТЕ СО СПИНЫ — слева, крупно, пальцы загибаются рукавом
    hx = 190
    s += SL(Z_PERED, figura(hx, 1080, 680, t, "#5b4a62", "#e8dcc0", False, .2,
                            False, 1.0, False, 1.0, False, False))
    s += SL(Z_PERED, f'<path d="M{hx-134:.0f},{1080-680*.64:.0f}'
                     f' q{134:.0f},{48:.0f} {268:.0f},0 l{-18:.0f},{400:.0f}'
                     f' q{-116:.0f},{30:.0f} {-232:.0f},0 Z" fill="#6b5a72"'
                     f' opacity=".55"/>')
    zag = A.ease(A.seg(t, 1.2, 1.4))
    ruk, (kx_, ky_) = rukav(hx + 110, 764, 180, -40 + 16 * zag, t, "#5b4a62",
                            "#e8dcc0", .2, 4.0)
    s += SL(Z_PERED, ruk)
    for i in range(3):                   # загнутые пальцы — овалами, без кистей
        zz = A.ease(A.seg(t, 1.2 + i * .4, .4))
        s += SL(Z_PERED, f'<ellipse cx="{kx_-20+i*26:.0f}"'
                         f' cy="{ky_-30+22*zz:.0f}" rx="13"'
                         f' ry="{28-15*zz:.0f}" fill="#f0cfae" {o(3)}/>')
    s += SL(Z_SRED, _batareya(640, 760 + 180, 700, 150, t, 9))
    s += SL(Z_SRED, kot(1620, 1012, t, 1.2, "#4a4440", False))
    s += SL(Z_SRED, hodiki(1870, 560, t, 1.1))
    s += SL(Z_PERED, zanaveska(420, 40, 480, 200, TKAN2, t, 1))
    s += SL(Z_PERED, zanaveska(1540, 40, 480, 200, TKAN2, t, -1))
    s += vinetka(.42)
    return s


# ── 92 ─────────────────────────────────────────────────────────────────────
def kinokamera_i_hlopushka(t):
    """Тёплый луч прожектора в темноте: старая деревянная кинокамера на
    треноге занимает пол-кадра, рядом складной режиссёрский стул и хлопушка.
    Ручка камеры крутится, в луче пляшут пылинки, луч рисует силуэты."""
    rnd = random.Random(9221)
    s = f'<rect width="{W}" height="{H}" fill="#120f14"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#1b1720"/>')
    for i in range(7):                   # дощатый задник в полутьме
        s += SL(Z_DAL, f'<rect x="{i*280:.0f}" y="0" width="246" height="880"'
                       f' fill="#241f2a" opacity=".7" {o(3)}/>')
    s += SL(Z_DAL, f'<rect y="880" width="{W}" height="200" fill="#1d1a22"/>')
    s += SL(Z_DAL, polovicy(900, "#3a3038"))
    # прожектор слева: тёплый конус через кадр
    px_, py_ = 150, 260
    pr = (f'<rect x="{px_-70:.0f}" y="{py_-90:.0f}" width="190" height="180"'
          f' rx="20" fill="#3a3f46" {o(7)}/>')
    pr += (f'<ellipse cx="{px_+124:.0f}" cy="{py_:.0f}" rx="26" ry="92"'
           f' fill="url(#zol)" {o(5)}/>')
    pr += (f'<rect x="{px_-20:.0f}" y="{py_+90:.0f}" width="46" height="150"'
           f' fill="#2f3337" {o(5)}/>')
    pr += (f'<path d="M{px_-80:.0f},{py_+240:.0f} h166 l24,34 h-214 Z"'
           f' fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, pr)
    s += SL(Z_SRED, lampa(px_ + 40, py_ + 60, t, .8, False))
    s += SL(Z_SRED, f'<path d="M{px_+140:.0f},{py_-80:.0f} L1920,80 L1920,900'
                    f' L{px_+140:.0f},{py_+80:.0f} Z" fill="{SVET}"'
                    f' opacity="{.13+.03*abs(A.w(t,2.2)):.2f}"/>')
    s += SL(Z_SRED, luch(px_ + 150, py_ - 60, 300, 780, t, .14))
    s += SL(Z_SRED, teplo(px_ + 200, py_ + 60, 900, 760, .3))
    for i in range(26):                  # пылинки пляшут в луче
        k = ((t * .22) + rnd.random()) % 1.0
        xx = px_ + 200 + k * 1500
        yy = py_ + rnd.uniform(-60, 420) + 40 * A.w(t, 2.4 + rnd.random(), k)
        s += SL(Z_SRED, f'<circle cx="{xx:.0f}" cy="{yy:.0f}"'
                        f' r="{rnd.uniform(2,6):.1f}" fill="#fff3d0"'
                        f' opacity="{.3+.5*abs(A.w(t,1.8,k)):.2f}"/>')
    # луч рисует силуэты на заднике
    for i, (sx_, h_) in enumerate(((1430, 470),)):
        s += SL(Z_DAL, f'<g opacity="{.42+.18*abs(A.w(t,2.6,i*.3)):.2f}">'
                       + figura(sx_, 880, h_, t, "#0d0b10", "#2a2430", False,
                                .2 * i, True, 1.0, False, 1.0, True, False,
                                False)
                       + '</g>')
    # КИНОКАМЕРА НА ТРЕНОГЕ — главный предмет в центре
    s += SL(Z_SRED, _kinokamera(860, 1010, 1.85, t, True))
    s += SL(Z_SRED, teplo(860, 560, 620, 520, .22))
    # складной режиссёрский стул
    stx, sty = 1350, 1010
    st_ = ten(stx, sty + 8, 120, 16, .5)
    for i in (-1, 1):
        st_ += (f'<line x1="{stx+i*110:.0f}" y1="{sty:.0f}" x2="{stx-i*30:.0f}"'
                f' y2="{sty-290:.0f}" stroke="url(#derev)" stroke-width="20"'
                f' stroke-linecap="round"/>')
        st_ += (f'<line x1="{stx+i*110:.0f}" y1="{sty:.0f}" x2="{stx+i*86:.0f}"'
                f' y2="{sty-180:.0f}" stroke="url(#derev)" stroke-width="16"/>')
    st_ += (f'<path d="M{stx-116:.0f},{sty-290:.0f} h232 q-10,36 -116,38'
            f' q-106,-2 -116,-38 Z" fill="{TKAN}" {o(6)}/>')
    st_ += (f'<rect x="{stx-116:.0f}" y="{sty-430:.0f}" width="232" height="76"'
            f' rx="10" fill="{TKAN}" {o(6)}/>')
    for i in (-1, 1):
        st_ += (f'<rect x="{stx+i*116-10:.0f}" y="{sty-440:.0f}" width="20"'
                f' height="170" rx="8" fill="url(#derev)" {o(4)}/>')
    s += SL(Z_SRED, st_)
    # ХЛОПУШКА щёлкает в правой нижней четверти
    shch = A.out(A.seg(t, .6, .35)) * (1 - A.ease(A.seg(t, 1.4, .5)))
    s += SL(Z_SRED, _hlopushka(1540, 820, 1.45, t, shch, -14 + 10 * shch))
    ruk, _ = rukav(1760, 1010, 150, -116, t, "#2a2430", "#ffd98a", .2, 4.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, _chashka(560, 1012, 1.3, t, .2, "#9aa1a8", True))
    s += SL(Z_SRED, par(560, 950, t, 3, .35, 150, .4, .8))
    for i in range(5):                   # бобины с плёнкой у ног камеры
        s += SL(Z_SRED, f'<circle cx="{660+i*58:.0f}" cy="{1058-(i%2)*18:.0f}"'
                        f' r="{34-(i%3)*4:.0f}" fill="#2f3337" {o(5)}/>')
        s += SL(Z_SRED, f'<circle cx="{660+i*58:.0f}" cy="{1058-(i%2)*18:.0f}"'
                        f' r="10" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_PERED, ramka_pp("oba", "#0a0810", .8))
    s += SL(Z_LETIT, iskra_let(t, px_ + 120, py_, 6, 9227, 260, .3))
    s += vinetka(.54)
    return s


# ── 93 ─────────────────────────────────────────────────────────────────────
def ekran_selskogo_kluba(t):
    """Сельский клуб: простыня-экран на стене, перед ней ряды лавок со
    зрителями в тулупах, киномеханик крутит ручку передвижки.

    Экран заполнен нарисованным кадром кинохроники ЦЕЛИКОМ — деревня, обоз,
    двое бегут навстречу друг другу, зерно плёнки и царапины, — а не схемным
    домиком посреди пустого поля. Зал тоже наполнен: три ряда лавок, зрители
    со спины, луч проектора с пылью (осмотр 14.11)."""
    rnd = random.Random(9323)
    s = f'<rect width="{W}" height="{H}" fill="#15121a"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 1080, 126))
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#241d22" opacity=".62"/>')
    s += SL(Z_DAL, polovicy(960, "#4a3a34"))
    # простыня-экран: углы на гвоздях, лёгкие волны по полотну
    shx, shy, shw, shh = 460, 30, 1000, 900
    pol_ = (f'<rect x="{shx}" y="{shy}" width="{shw}" height="{shh}" rx="6"'
            f' fill="#efeadf" {o(8)}/>')
    for i in range(7):                   # складки простыни
        pol_ += (f'<path d="M{shx+40+i*136:.0f},{shy+10}'
                 f' q{14+6*A.w(t,4.0,i*.2):.0f},{shh*.5:.0f} 0,{shh-20:.0f}"'
                 f' fill="none" stroke="#d8d2c4" stroke-width="10" opacity=".7"/>')
    s += SL(Z_SRED, pol_)
    # ПРОЁМ ПОД НАСТОЯЩИЙ КАДР — он же поле нарисованной кинохроники
    ox, oy, ow, oh = 540, 70, 840, 820
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="ek93"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#cfc8ba"/>'
    za = ""
    # НАРИСОВАННЫЙ КАДР КИНОХРОНИКИ ВО ВЕСЬ ЭКРАН: небо, поле, деревня, обоз
    za += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh*.46:.0f}"'
           f' fill="#e6e0d2"/>')
    za += (f'<rect x="{ox}" y="{oy+oh*.46:.0f}" width="{ow}" height="{oh*.54:.0f}"'
           f' fill="#8d8778"/>')
    for i in range(5):                   # облака кинохроники
        k = ((t * .04) + i * .22) % 1.2 - .1
        za += (f'<ellipse cx="{ox-120+k*(ow+240):.0f}" cy="{oy+oh*(.10+(i%3)*.07):.0f}"'
               f' rx="{120+i*16:.0f}" ry="{34+i*5:.0f}" fill="#f2eee2" opacity=".8"/>')
    for i in range(4):                   # дальняя гряда изб
        bx = ox + 20 + i * 220
        za += (f'<rect x="{bx:.0f}" y="{oy+oh*.40:.0f}" width="150"'
               f' height="{oh*.14:.0f}" fill="#5f5a4e"/>')
        za += (f'<path d="M{bx-24:.0f},{oy+oh*.40:.0f} l87,-56 l87,56 Z"'
               f' fill="#454138"/>')
        za += (f'<rect x="{bx+108:.0f}" y="{oy+oh*.30:.0f}" width="26"'
               f' height="{oh*.08:.0f}" fill="#55503f"/>')
        for j in range(5):               # дым над каждой избой живёт
            k = ((t * .22) + j * .2 + i * .1) % 1.0
            za += (f'<circle cx="{ox+133+i*220+16*A.w(t,2.2,j*.2):.0f}"'
                   f' cy="{oy+oh*.30-k*oh*.12:.0f}" r="{10+18*k:.0f}"'
                   f' fill="#efe9db" opacity="{.6*(1-k):.2f}"/>')
    for i in range(8):                   # пашня полосами к горизонту
        yy = oy + oh * (.56 + i * .055)
        za += (f'<path d="M{ox:.0f},{yy:.0f} q{ow*.5:.0f},{14+i*3:.0f} {ow:.0f},0"'
               f' fill="none" stroke="#a79f8e" stroke-width="{5+i}" opacity=".7"/>')
    # обоз уходит вдоль поля
    for i in range(3):
        wx = ox + 90 + i * 150 + ((t * 26) % 120)
        wy = oy + oh * .52 + i * 10
        za += (f'<rect x="{wx:.0f}" y="{wy-28:.0f}" width="88" height="34" rx="6"'
               f' fill="#6f6a5c"/>')
        for j in (0, 1):
            za += (f'<circle cx="{wx+14+j*60:.0f}" cy="{wy+10:.0f}" r="16"'
                   f' fill="none" stroke="#5e594d" stroke-width="7"/>')
        za += (f'<ellipse cx="{wx-34:.0f}" cy="{wy-14:.0f}" rx="32" ry="18"'
               f' fill="#6f6a5c"/>')
    # ДВОЕ НА ЭКРАНЕ БЕГУТ НАВСТРЕЧУ И ОБНИМАЮТСЯ
    vst = A.ease(A.seg(t, .6, 2.6))
    ax_ = ox + ow * .28 + vst * ow * .16
    bx_ = ox + ow * .72 - vst * ow * .16
    for px_, h_, pl_ in ((ax_, oh * .30, False), (bx_, oh * .27, True)):
        za += figura(px_, oy + oh * .88, h_, t, "#2f2c26", "#efe9db", pl_, .2,
                     False, .95, False, 2.0 * (1 - vst), False, True)
    za += (f'<ellipse cx="{(ax_+bx_)/2:.0f}" cy="{oy+oh*.70:.0f}"'
           f' rx="{90*vst:.0f}" ry="{60*vst:.0f}" fill="#f2eee2"'
           f' opacity="{.25*vst:.2f}"/>')
    for i in range(10):                  # зерно плёнки
        za += (f'<circle cx="{ox+rnd.uniform(0,ow):.0f}" cy="{oy+rnd.uniform(0,oh):.0f}"'
               f' r="{rnd.uniform(2,5):.1f}" fill="#fffaf0" opacity=".3"/>')
    for i in range(4):                   # плёночные царапины бегут
        xx = ox + ((t * 220 + i * 230) % ow)
        za += (f'<line x1="{xx:.0f}" y1="{oy}" x2="{xx-14:.0f}" y2="{oy+oh}"'
               f' stroke="#fffaf0" stroke-width="3" opacity=".35"/>')
    za += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#vig)"'
           f' opacity=".5"/>')
    vid += f'<g clip-path="url(#ek93)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    # обвязка: только короб экрана и гвозди по углам простыни
    ob = (f'<rect x="{ox-40}" y="{oy-40}" width="{ow+80}" height="{oh+80}" rx="8"'
          f' fill="none" stroke="#efeadf" stroke-width="80"/>')
    ob += (f'<path d="{put}" fill="none" stroke="#b9b2a2" stroke-width="7"/>')
    for gx_, gy_ in ((shx + 20, shy + 20), (shx + shw - 20, shy + 20),
                     (shx + 20, shy + shh - 20), (shx + shw - 20, shy + shh - 20)):
        ob += (f'<circle cx="{gx_:.0f}" cy="{gy_:.0f}" r="14" fill="#8d949b"'
               f' {o(3)}/>')
    s += SL(Z_SRED, vid + ob)
    # ЛУЧ ПРОЕКТОРА С ПЫЛЬЮ — от передвижки к экрану, мимо проёма
    kmx, kmy = 1740, 900
    drozh = 14 * A.w(t, 1.7, .1)
    s += SL(Z_SRED, f'<path d="M{kmx:.0f},{kmy-190:.0f} L{ox+ow+44:.0f},'
                    f'{oy+drozh-40:.0f} L{ox+ow+44:.0f},{oy+oh+drozh+40:.0f} Z"'
                    f' fill="{SVET}" opacity="{.17+.05*abs(A.w(t,1.3)):.2f}"/>')
    for i in range(22):                  # пыль пляшет в луче
        q = rnd.random()
        px_ = kmx - q * (kmx - ox - ow - 40)
        py_ = kmy - 190 + q * ((oy + oh * .5) - (kmy - 190)) + \
            (q * 180) * math.sin(i * 1.7 + t * 1.3)
        s += SL(Z_SRED, f'<circle cx="{px_:.0f}" cy="{py_:.0f}"'
                        f' r="{1.8+2.6*q:.1f}" fill="#fff6dd"'
                        f' opacity="{.25+.45*abs(A.w(t,2.0,i*.13)):.2f}"/>')
    s += SL(Z_SRED, teplo(kmx - 120, kmy - 200, 620, 520, .3))
    # передвижка и киномеханик
    pd = (f'<rect x="{kmx-110:.0f}" y="{kmy-270:.0f}" width="220" height="150"'
          f' rx="16" fill="#3a3f46" {o(7)}/>')
    for i, sgn in ((0, -1), (1, 1)):
        rot = (t * 120 + i * 50) % 360
        bx2, by2 = kmx + sgn * 70, kmy - 320
        pd += (f'<circle cx="{bx2:.0f}" cy="{by2:.0f}" r="52" fill="#2f3337" {o(6)}/>')
        pd += f'<g transform="rotate({rot:.0f} {bx2:.0f} {by2:.0f})">'
        for j in range(4):
            a = j * 1.5708
            pd += (f'<line x1="{bx2:.0f}" y1="{by2:.0f}"'
                   f' x2="{bx2+math.cos(a)*46:.0f}" y2="{by2+math.sin(a)*46:.0f}"'
                   f' stroke="#8d949b" stroke-width="8"/>')
        pd += '</g>'
    pd += (f'<rect x="{kmx-130:.0f}" y="{kmy-120:.0f}" width="260" height="30"'
           f' rx="10" fill="#2f3337" {o(5)}/>')
    for i in (-1, 1):
        pd += (f'<line x1="{kmx+i*90:.0f}" y1="{kmy-90:.0f}" x2="{kmx+i*110:.0f}"'
               f' y2="{kmy:.0f}" stroke="url(#derev)" stroke-width="18"/>')
    rh = (t * 300) % 360
    pd += (f'<g transform="rotate({rh:.0f} {kmx-120:.0f} {kmy-200:.0f})">'
           f'<line x1="{kmx-120:.0f}" y1="{kmy-200:.0f}" x2="{kmx-120:.0f}"'
           f' y2="{kmy-150:.0f}" stroke="#5d6168" stroke-width="12"/>'
           f'<circle cx="{kmx-120:.0f}" cy="{kmy-144:.0f}" r="14"'
           f' fill="url(#derev)" {o(3)}/></g>')
    s += SL(Z_SRED, pd)
    s += SL(Z_SRED, figura(kmx + 130, 1060, 450, t, "#3a3346", "#ffd98a", False,
                           .2, True, 1.0, False, 1.2, False, True))
    ruk, _ = rukav(kmx + 70, 820, 150, 188, t, "#3a3346", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    # ЗАЛ: три ряда лавок со зрителями со спины, ближний ряд крупнее
    for r, (ry_, h0, n_, x0, step, op_) in enumerate((
            (952, 230, 9, 150, 160, .85),
            (1012, 290, 8, 110, 190, .92),
            (1080, 360, 7, 90, 230, 1.0))):
        s += SL(Z_SRED if r < 2 else Z_PERED,
                f'<rect x="{x0-70:.0f}" y="{ry_-26:.0f}" width="{n_*step+60:.0f}"'
                f' height="26" rx="8" fill="url(#derev)" {o(6)}/>')
        for i in range(n_):
            zx_ = x0 + i * step + ((r % 2) * 40)
            s += SL(Z_SRED if r < 2 else Z_PERED,
                    figura(zx_, ry_, h0, t, "#241e2a", "#5a6a7a", i % 2 == 0,
                           .13 * i + r * .2, False, op_, i % 3 == 0, 1.0, False,
                           False, False))
    s += SL(Z_PERED, _shapka_meh(1820, 1046, 1.2, t, .3, 0.0))
    s += SL(Z_LETIT, iskra_let(t, kmx - 60, kmy - 320, 5, 9329, 220, .3))
    s += vinetka(.5)
    return s


# ── 94 ─────────────────────────────────────────────────────────────────────
def tri_afishi_na_stene_kluba(t):
    """Бревенчатая стена клуба: завклубом в кепке мажет кистью клей и клеит
    одну за другой три большие афиши — трактор в поле, пастуший рожок с
    лентой, золотой сноп. Мальчишки сбегаются смотреть."""
    rnd = random.Random(9421)
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 9431)
    s += SL(Z_DAL, oblaka(t, 120, 4, 9433, .28, "#c8d4e2", 16.0))
    s += SL(Z_DAL, gryaz_polosa(900, 180, "#4a443a"))
    st = brevna(0, 60, W, 880, 120)
    st += f'<rect y="60" width="{W}" height="880" fill="#9c7049" opacity=".26"/>'
    st += f'<path d="M-40,130 L960,-140 L1960,130 Z" fill="#524638" opacity=".96" {o(9)}/>'
    s += SL(Z_DAL, st)
    s += SL(Z_DAL, f'<rect x="760" y="-90" width="110" height="220"'
                   f' fill="url(#kamen)" {o(7)}/>')
    s += SL(Z_DAL, dym(812, -80, t, 6, .24, 340, .38, "#d8cbbd", 1.2))
    s += SL(Z_SRED, tusklaya_lampochka(1760, 200, t, 1.6, True))
    s += SL(Z_SRED, teplo(1760, 330, 760, 640, .36 + .1 * abs(A.w(t, 1.6))))
    # ТРИ АФИШИ ложатся на стену по одной
    for i, (ax, vid_) in enumerate(((440, "traktor"), (960, "rozhok"),
                                    (1470, "snop"))):
        k = A.out(A.seg(t, .3 + i * .40, .55))
        if k < .03:
            continue
        s += SL(Z_SRED, f'<g opacity="{k:.2f}" transform="translate(0,'
                        f'{(1-k)*-120:.0f})">'
                        + _afisha(ax, 480, 430, 600, t, vid_, 9437 + i,
                                  (1 - k) * 12 - 2,
                                  A.ease(A.seg(t, 2.6 + i * .2, .6)) if i == 2 else 0.0)
                        + '</g>')
        for j in range(4):               # мазки клея под афишей
            s += SL(Z_SRED, f'<path d="M{ax-190+j*110:.0f},{760:.0f}'
                            f' q50,{-16+j*6:.0f} 96,2" fill="none"'
                            f' stroke="#e8e0cc" stroke-width="12"'
                            f' opacity="{.4*k:.2f}"/>')
    # завклубом с кистью и ведром клея
    zx = 1760
    maz = A.w(t, .8, .1)
    s += SL(Z_SRED, figura(zx, 1040, 520, t, "#3f4a3a", "#ffd98a", False, .2,
                           True, 1.0, False, 1.2, False, True))
    s += SL(Z_SRED, f'<path d="M{zx-70:.0f},{1040-520*.86:.0f} q70,-40 140,-6'
                    f' l6,22 q-74,-26 -146,10 Z" fill="#2e3a46" {o(5)}/>')
    ruk, (kx, ky) = rukav(zx - 100, 700, 180, 186 + 22 * maz, t, "#3f4a3a",
                          "#ffd98a", .2, 6.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<rect x="{kx-24:.0f}" y="{ky-10:.0f}" width="48" height="90"'
                    f' rx="10" fill="url(#derev)"'
                    f' transform="rotate({-24+16*maz:.0f} {kx:.0f} {ky:.0f})"'
                    f' {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{kx-32:.0f}" y="{ky+76:.0f}" width="64" height="46"'
                    f' rx="8" fill="#d8cbb0"'
                    f' transform="rotate({-24+16*maz:.0f} {kx:.0f} {ky:.0f})"'
                    f' {o(4)}/>')
    s += SL(Z_SRED, _vedro_dach(1620, 1012, 1.2, t))
    # мальчишки сбегаются
    for i in range(4):
        beg = A.ease(A.seg(t, .8 + i * .22, 1.4))
        mxx = 120 + beg * (260 + i * 120)
        s += SL(Z_SRED, figura(mxx, 1056 + (i % 2) * 8, 300 + i * 18, t,
                               ("#5b2f3a", "#2e4a5a", "#4a3a2c", "#3f3a46")[i],
                               "#ffd0a0", False, .2 * i, True, 1.0, False, 1.6,
                               False, i % 2 == 0))
        s += SL(Z_SRED, para_izo_rta(mxx + 40, 1056 - (300 + i * 18) * .80, t,
                                     i * .3, .9, .45))
    s += SL(Z_SRED, kura(1180, 1012, t, 1.0, .4))
    s += SL(Z_SRED, _korzina_ryab(1340, 1012, 200, 150, t, 9439))
    s += SL(Z_PERED, f'<rect x="0" y="100" width="90" height="980" rx="10"'
                     f' fill="url(#brev)" {o(9)}/>')
    s += SL(Z_PERED, goloe_derevo(1890, 1080, 620, t, 9443, 7, "#2c2e36"))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 9449, .42, .9))
    s += vinetka(.44)
    return s


# ── 95 ─────────────────────────────────────────────────────────────────────
def semochnaya_ploschadka_sorok_chetve(t):
    """Съёмочный павильон: режиссёр в кепке с рупором стоит со спины у большой
    кинокамеры на тележке, перед ним декорация — городские часы на башне,
    стрелки встают на шесть. Осветитель поворачивает прожектор."""
    rnd = random.Random(9521)
    s = f'<rect width="{W}" height="{H}" fill="#161320"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#1f1b28"/>')
    s += SL(Z_DAL, svody(t, "#2e2838", 3))
    for i in range(9):                   # фермы и тросы павильона
        s += SL(Z_DAL, f'<line x1="{i*240:.0f}" y1="0" x2="{i*240+90:.0f}"'
                       f' y2="260" stroke="#3a3346" stroke-width="9"'
                       f' opacity=".7"/>')
    s += SL(Z_DAL, polovicy(930, "#423848"))
    # ДЕКОРАЦИЯ: городские часы на башне — главный предмет
    bx, by, bw = 1100, 930, 420
    bash = (f'<rect x="{bx-bw/2:.0f}" y="{by-700:.0f}" width="{bw:.0f}"'
            f' height="700" rx="10" fill="url(#kamen)" {o(9)}/>')
    bash += kladka(bx - bw / 2 + 8, by - 690, bw - 16, 680, 76, "url(#kamen)")
    bash += (f'<path d="M{bx-bw/2-40:.0f},{by-700:.0f} h{bw+80:.0f} l-60,-90'
             f' h{-bw+40:.0f} Z" fill="#5e564c" {o(8)}/>')
    bash += (f'<path d="M{bx-80:.0f},{by-790:.0f} h160 l-80,-150 Z"'
             f' fill="#4a443c" {o(7)}/>')
    for i in range(3):                   # арочные окна башни
        bash += (f'<path d="M{bx-50:.0f},{by-180-i*180:.0f} v-90'
                 f' q50,-54 100,0 v90 Z" fill="#241f2a" {o(5)}/>')
    s += SL(Z_SRED, bash)
    chx, chy, chr_ = bx, by - 560, 160
    ch = (f'<circle cx="{chx:.0f}" cy="{chy:.0f}" r="{chr_+22:.0f}"'
          f' fill="#5e564c" {o(8)}/>')
    ch += (f'<circle cx="{chx:.0f}" cy="{chy:.0f}" r="{chr_:.0f}"'
           f' fill="url(#krem)" {o(6)}/>')
    for i in range(12):                  # часовые деления — не цифры
        a = i * .5236
        r1 = chr_ * (.82 if i % 3 else .74)
        ch += (f'<line x1="{chx+math.cos(a)*r1:.0f}"'
               f' y1="{chy+math.sin(a)*r1:.0f}"'
               f' x2="{chx+math.cos(a)*chr_*.94:.0f}"'
               f' y2="{chy+math.sin(a)*chr_*.94:.0f}" stroke="#4a443c"'
               f' stroke-width="{10 if i % 3 == 0 else 6}"/>')
    vst = A.ease(A.seg(t, .8, 1.6))
    ach = math.radians(-90 + vst * 180 + (1 - vst) * 40)   # часовая встаёт вниз
    amn = math.radians(-90 + (1 - vst) * 300)              # минутная — вверх
    ch += (f'<line x1="{chx:.0f}" y1="{chy:.0f}"'
           f' x2="{chx+math.cos(ach)*chr_*.56:.0f}"'
           f' y2="{chy+math.sin(ach)*chr_*.56:.0f}" stroke="#2b2a2e"'
           f' stroke-width="20" stroke-linecap="round"/>')
    ch += (f'<line x1="{chx:.0f}" y1="{chy:.0f}"'
           f' x2="{chx+math.cos(amn)*chr_*.82:.0f}"'
           f' y2="{chy+math.sin(amn)*chr_*.82:.0f}" stroke="#2b2a2e"'
           f' stroke-width="13" stroke-linecap="round"/>')
    ch += (f'<circle cx="{chx:.0f}" cy="{chy:.0f}" r="16" fill="#2b2a2e"/>')
    s += SL(Z_SRED, ch)
    s += SL(Z_SRED, teplo(chx, chy, 620, 540, .26 + .08 * abs(A.w(t, 1.6))))
    # прожектор осветителя: поворачивается
    pov = 22 * A.ease(A.seg(t, 1.6, 1.4)) - 10
    plx, ply = 1740, 520
    s += SL(Z_SRED, f'<g transform="rotate({pov:.1f} {plx:.0f} {ply:.0f})">'
                    f'<rect x="{plx-90:.0f}" y="{ply-80:.0f}" width="180"'
                    f' height="160" rx="18" fill="#3a3f46" {o(7)}/>'
                    f'<ellipse cx="{plx-96:.0f}" cy="{ply:.0f}" rx="24" ry="80"'
                    f' fill="url(#zol)" {o(5)}/>'
                    f'<path d="M{plx-110:.0f},{ply-80:.0f} L{chx+200:.0f},'
                    f'{chy-120:.0f} L{chx+200:.0f},{chy+260:.0f} Z" fill="{SVET}"'
                    f' opacity="{.12+.03*abs(A.w(t,2.0)):.2f}"/></g>')
    s += SL(Z_SRED, lampa(plx - 40, ply + 40, t, .75, False))
    s += SL(Z_SRED, f'<rect x="{plx-16:.0f}" y="{ply+80:.0f}" width="34"'
                    f' height="330" fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, figura(1850, 1030, 460, t, "#2e3a46", "#ffd98a", False, .4,
                           True, 1.0, False, 1.2, False, True))
    # кинокамера на тележке едет
    ezd = A.ease(A.seg(t, .4, 2.4))
    kcx = 520 + ezd * 150
    s += SL(Z_SRED, f'<rect x="{kcx-230:.0f}" y="1010" width="460" height="40"'
                    f' rx="12" fill="#3a3f46" {o(7)}/>')
    for i in (-1, 1):
        rot = (ezd * 600 + (0 if i < 0 else 40)) % 360
        s += SL(Z_SRED, f'<circle cx="{kcx+i*160:.0f}" cy="1058" r="40"'
                        f' fill="#23262a" {o(6)}/>')
        s += SL(Z_SRED, f'<g transform="rotate({rot:.0f} {kcx+i*160:.0f} 1058)">'
                        f'<line x1="{kcx+i*160-34:.0f}" y1="1058"'
                        f' x2="{kcx+i*160+34:.0f}" y2="1058" stroke="#8d949b"'
                        f' stroke-width="8"/></g>')
    for i in range(13):                  # шпалы под рельсами
        s += SL(Z_SRED, f'<rect x="{i*150:.0f}" y="1024" width="56" height="64"'
                        f' rx="6" fill="#6b5a46" {o(3)}/>')
    for yy in (1030, 1072):              # две светлые нитки рельсов
        s += SL(Z_SRED, f'<rect x="0" y="{yy}" width="{W}" height="16" rx="8"'
                        f' fill="#c7ced4" {o(3)}/>')
        s += SL(Z_SRED, f'<rect x="0" y="{yy+2}" width="{W}" height="5"'
                        f' fill="#f0f5f8" opacity=".8"/>')
    s += SL(Z_SRED, f'<rect x="{kcx-210:.0f}" y="908" width="420" height="54"'
                    f' rx="10" fill="#7d6a52" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="{kcx-180:.0f}" y="962" width="360" height="30"'
                    f' rx="8" fill="#56483c" {o(5)}/>')
    s += SL(Z_SRED, _kinokamera(kcx, 908, 1.05, t, True, False))
    # режиссёр со спины с рупором
    rx_ = 280
    vzmah = A.ease(A.seg(t, 1.0, .5)) - A.ease(A.seg(t, 2.0, .6))
    s += SL(Z_SRED, figura(rx_, 1060, 560, t, "#3a3346", "#ffd98a", False, .1,
                           False, 1.0, True, 1.0, False, True, False))
    ruk, (kx, ky) = rukav(rx_ + 110, 740, 220, -70 - 40 * vzmah, t, "#3a3346",
                          "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<g transform="rotate({-30-30*vzmah:.0f} {kx:.0f} {ky:.0f})">'
                    f'<rect x="{kx-30:.0f}" y="{ky-18:.0f}" width="54" height="36"'
                    f' rx="10" fill="#5d6168" {o(5)}/>'
                    f'<path d="M{kx+24:.0f},{ky-30:.0f} l150,-86 l0,232'
                    f' l-150,-80 Z" fill="url(#zhel)" {o(7)}/>'
                    f'<ellipse cx="{kx+174:.0f}" cy="{ky+16:.0f}" rx="22"'
                    f' ry="116" fill="#cfd6dc" {o(5)}/>'
                    f'<ellipse cx="{kx+174:.0f}" cy="{ky+16:.0f}" rx="12"'
                    f' ry="100" fill="#3f454a" opacity=".8"/></g>')
    s += SL(Z_SRED, _hlopushka(780, 940, .9, t, 0.0, -18))
    s += SL(Z_SRED, _chashka(940, 1012, 1.2, t, .3, "#9aa1a8", True))
    s += SL(Z_SRED, par(940, 990, t, 3, .35, 140, .4, .8))
    s += SL(Z_PERED, ramka_pp("oba", "#0d0b12", .8))
    s += SL(Z_LETIT, iskra_let(t, plx - 80, ply, 6, 9529, 240, .3))
    s += vinetka(.5)
    return s


# ── 96 ─────────────────────────────────────────────────────────────────────
def parizhskaya_ulica_s_gruzovichkom(t):
    """Улочка парижского пригорода: серые дома со ставнями, у тротуара стоит
    пузатый грузовичок, шофёр в берете выскакивает из кабины с букетом,
    продавщица выбегает из булочной, голуби взлетают с мостовой.
    В витрине магазина идёт НАСТОЯЩИЙ кадр."""
    rnd = random.Random(9623)
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, False, 9629)
    s += oblaka(t, 130, 5, 9631, .3, "#dfe6ee", 18.0)
    # дома со ставнями во всю ширину
    dom = (f'<rect x="0" y="170" width="{W}" height="690" fill="#9aa0a0" {o(8)}/>')
    dom += kladka(0, 170, W, 690, 80, "#a8aeae")
    dom += (f'<path d="M-40,230 h2000 l-80,-86 h-1840 Z" fill="#6f7472" {o(7)}/>')
    for i in range(8):                   # мансардные окошки под крышей
        dom += (f'<rect x="{60+i*240:.0f}" y="178" width="92" height="44" rx="6"'
                f' fill="#3f4a52" {o(4)}/>')
    for i in range(7):                   # окна со ставнями
        wx = 40 + i * 268
        dom += (f'<rect x="{wx:.0f}" y="300" width="130" height="190" rx="6"'
                f' fill="#3f4a52" {o(5)}/>')
        for sgn in (-1, 1):
            otk = A.ease(A.seg(t, 1.2 + i * .18, .6))
            ug = sgn * (10 + 62 * otk)
            dom += (f'<g transform="rotate({ug:.0f} {wx+(0 if sgn<0 else 130):.0f} 370)">'
                    f'<rect x="{wx+(0 if sgn<0 else 92):.0f}" y="298" width="40"'
                    f' height="194" rx="5" fill="#5b7a62" {o(4)}/>'
                    f'<line x1="{wx+(20 if sgn<0 else 112):.0f}" y1="310"'
                    f' x2="{wx+(20 if sgn<0 else 112):.0f}" y2="480"'
                    f' stroke="#3f5a46" stroke-width="7"/></g>')
        dom += (f'<rect x="{wx-14:.0f}" y="494" width="158" height="18" rx="6"'
                f' fill="#7d8286" {o(3)}/>')
    s += SL(Z_DAL, dom)
    s += SL(Z_DAL, f'<rect y="860" width="{W}" height="220" fill="#6b6f72" {o(6)}/>')
    for r in range(3):                   # брусчатка уходит в перспективу
        for i in range(14 - r * 2):
            s += SL(Z_DAL, f'<rect x="{-40+i*(150+r*22):.0f}"'
                           f' y="{906+r*62:.0f}" width="{120+r*20:.0f}"'
                           f' height="{44+r*10:.0f}" rx="8" fill="#7a7e82"'
                           f' opacity="{.5+r*.12:.2f}"/>')
    s += SL(Z_DAL, f'<rect y="846" width="{W}" height="34" fill="#8d9296" {o(4)}/>')
    for i in range(7):                   # линии тротуара в точку схода
        s += SL(Z_DAL, f'<line x1="{i*280:.0f}" y1="1080" x2="{700+i*80:.0f}"'
                       f' y2="880" stroke="#5e6266" stroke-width="5"'
                       f' opacity=".45"/>')
    # фонарь улицы — тёплое пятно
    s += SL(Z_SRED, f'<rect x="196" y="300" width="30" height="580" rx="10"'
                    f' fill="#3a3f46" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M136,300 h150 l-24,-60 h-102 Z" fill="#2f3337" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M148,300 h126 l-14,140 h-98 Z" fill="url(#stekl)"'
                    f' opacity=".7" {o(5)}/>')
    s += SL(Z_SRED, ogon(211, 400, t, .85, .2, 5))
    s += SL(Z_SRED, teplo(211, 370, 700, 600, .44 + .1 * abs(A.w(t, 1.6))))
    # БУЛОЧНАЯ С ВИТРИНОЙ: нарисованный вид, метка, рама поверх
    s += SL(Z_SRED, f'<rect x="1050" y="196" width="840" height="884" rx="8"'
                    f' fill="#8a6a52" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="1030" y="182" width="880" height="52" rx="10"'
                    f' fill="#5b3f2a" {o(7)}/>')
    # проём витрины ВЫСОКИЙ: в него ложится портрет
    ox, oy, ow, oh = 1080, 240, 780, 800
    put = kontur_proema(ox, oy, ow, oh, "pryam")
    vid = f'<clipPath id="pa96"><path d="{put}"/></clipPath>'
    vid += f'<path d="{put}" fill="#2e2a26"/>'
    za = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#3a332c"/>')
    za += teplo(ox + ow * .5, oy + oh * .4, 520, 480, .5)
    for i in range(4):                   # полки с хлебами внутри витрины
        yy = oy + oh * (.30 + i * .17)
        za += (f'<rect x="{ox+40:.0f}" y="{yy:.0f}" width="{ow-80:.0f}"'
               f' height="22" rx="8" fill="#6b4a2a" {o(4)}/>')
        for j in range(4):
            za += (f'<ellipse cx="{ox+110+j*180:.0f}" cy="{yy-26:.0f}" rx="74"'
                   f' ry="30" fill="#c98c55" {o(4)}/>')
            za += (f'<ellipse cx="{ox+110+j*180:.0f}" cy="{yy-34:.0f}" rx="58"'
                   f' ry="20" fill="#e8bd84" opacity=".7"/>')
    za += (f'<ellipse cx="{ox+ow*.5:.0f}" cy="{oy+oh*.14:.0f}" rx="150" ry="60"'
           f' fill="{SVET}" opacity="{.3+.1*abs(A.w(t,1.7)):.2f}"/>')
    vid += f'<g clip-path="url(#pa96)">{za}</g>'
    vid += mesto_stoka(ox, oy, ow, oh, "pryam")
    ob = (f'<rect x="{ox-40}" y="{oy-40}" width="{ow+80}" height="{oh+80}" rx="8"'
          f' fill="none" stroke="#5b3f2a" stroke-width="80"/>')
    ob += (f'<rect x="{ox+ow/2-13:.0f}" y="{oy}" width="26" height="{oh}"'
           f' fill="#5b3f2a"/>')
    ob += (f'<path d="M{ox+40},{oy+70} l{ow*.3:.0f},{oh*.4:.0f}" stroke="#ffffff"'
           f' stroke-width="20" opacity=".16"/>')
    ob += f'<path d="{put}" fill="none" {o(9)}/>'
    ob += (f'<path d="M{ox-60},{oy-56} h{ow+120} l-40,-50 h{-ow-40} Z"'
           f' fill="#4a3220" {o(7)}/>')
    for i in range(9):                   # полосатый маркизный козырёк
        ob += (f'<path d="M{ox-40+i*(ow+80)/9:.0f},{oy-96:.0f}'
               f' l{(ow+80)/9:.0f},0 l{-16:.0f},{-64:.0f} l{-(ow+80)/9:.0f},0 Z"'
               f' fill="{KRAS if i % 2 else KREM}" {o(3)}/>')
    s += SL(Z_SRED, vid + ob)
    # пузатый грузовичок у тротуара
    gx, gy = 700, 1010
    s += SL(Z_SRED, _gruzovichok(gx, gy, 1.25, t))
    s += SL(Z_SRED, par(gx - 300, gy - 30, t, 4, .45, 170, .4, 1.0))
    # шофёр в берете выскакивает с букетом
    vysk = A.ease(A.seg(t, .5, 1.3))
    shx = gx - 120 + vysk * 240
    s += SL(Z_SRED, figura(shx + 300, 1066 + 20 * (1 - vysk), 500, t, "#2e3a46",
                           "#ffd0a0", False, .2, True, 1.0, False, 1.4, False,
                           True))
    s += SL(Z_SRED, f'<ellipse cx="{shx+300:.0f}" cy="{1066-500*.86:.0f}" rx="60"'
                    f' ry="26" fill="#2b3a4a" {o(4)}/>')
    ruk, (kx, ky) = rukav(shx + 360, 810, 150, -62, t, "#2e3a46", "#ffd0a0",
                          .2, 5.0)
    s += SL(Z_SRED, ruk)
    for i in range(9):                   # букет
        a = -1.2 + i * .3
        s += SL(Z_SRED, f'<line x1="{kx:.0f}" y1="{ky:.0f}"'
                        f' x2="{kx+math.cos(a)*70:.0f}"'
                        f' y2="{ky+math.sin(a)*70-30:.0f}" stroke="{ZEL2}"'
                        f' stroke-width="7"/>')
        s += SL(Z_SRED, f'<circle cx="{kx+math.cos(a)*76:.0f}"'
                        f' cy="{ky+math.sin(a)*76-36+4*A.w(t,2.2,i*.2):.0f}"'
                        f' r="16" fill="{(KRAS, "#e8743c", "#f2c14e")[i%3]}"'
                        f' {o(3)}/>')
    # продавщица выбегает из булочной
    vyb = A.ease(A.seg(t, 1.6, 1.2))
    s += SL(Z_SRED, figura(1000 - vyb * 110, 1060, 500, t, "#8a4a52", "#ffd0a0",
                           True, .5, True, 1.0, False, -2.0))
    s += SL(Z_SRED, f'<path d="M{940-vyb*110:.0f},{890:.0f} h120 l-10,130 h-100 Z"'
                    f' fill="#f2efe6" opacity=".9" {o(4)}/>')
    # голуби взлетают с мостовой
    for i in range(5):
        let = A.ease(A.seg(t, .9 + i * .14, .9))
        s += SL(Z_SRED, _golub(170 + i * 76, 1012, 1.4, t, i * .2, let))

    s += SL(Z_PERED, ramka_pp("levo", "#1a1a1e", .72))
    s += SL(Z_LETIT, iskra_let(t, 213, 520, 5, 9637, 220, .3))
    s += vinetka(.44)
    return s


# ── 97 ─────────────────────────────────────────────────────────────────────
def dve_podrugi_na_kinoprobah(t):
    """Коридор киностудии: длинная очередь девочек со спины, две подруги с
    косичками и школьными сумками стоят в хвосте — одна волнуется и поправляет
    бант, вторая зевает и ест булку. Дверь открывается, рука с хлопушкой зовёт."""
    rnd = random.Random(9721)
    s = f'<rect width="{W}" height="{H}" fill="#2b2a28"/>'
    # коридор с перспективой: стены и пол сходятся
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#7d7a70"/>')
    s += SL(Z_DAL, f'<path d="M0,0 L560,300 L560,800 L0,1080 Z" fill="#6b6860"/>')
    s += SL(Z_DAL, f'<path d="M{W},0 L1360,300 L1360,800 L{W},1080 Z"'
                   f' fill="#6b6860"/>')
    s += SL(Z_DAL, f'<rect x="560" y="300" width="800" height="500"'
                   f' fill="#8a8780" {o(7)}/>')
    s += SL(Z_DAL, f'<path d="M0,1080 L560,800 L1360,800 L{W},1080 Z"'
                   f' fill="#5e5a52"/>')
    for i in range(9):                   # половицы коридора в точку схода
        s += SL(Z_DAL, f'<line x1="{-60+i*250:.0f}" y1="1080"'
                       f' x2="{600+i*90:.0f}" y2="802" stroke="#4a463f"'
                       f' stroke-width="6" opacity=".55"/>')
    for i in range(4):
        s += SL(Z_DAL, f'<line x1="{120-i*30:.0f}" y1="{1060-i*80:.0f}"'
                       f' x2="{1800+i*30:.0f}" y2="{1060-i*80:.0f}"'
                       f' stroke="#4a463f" stroke-width="4" opacity=".3"/>')
    for i in range(7):                   # панель-поясок по стенам
        s += SL(Z_DAL, f'<path d="M{i*90:.0f},{640+i*18:.0f} L560,{700:.0f}"'
                       f' stroke="#56534c" stroke-width="10" opacity=".6"/>')
    s += SL(Z_DAL, f'<rect x="560" y="690" width="800" height="26"'
                   f' fill="#56534c" {o(3)}/>')
    s += SL(Z_SRED, tusklaya_lampochka(960, 120, t, 1.5, True))
    s += SL(Z_SRED, tusklaya_lampochka(700, 230, t, .9, True))
    s += SL(Z_SRED, teplo(960, 260, 900, 700, .34 + .1 * abs(A.w(t, 1.6))))
    # дверь в конце коридора открывается, из неё бьёт свет
    otk = A.ease(A.seg(t, 1.0, 1.0))
    dx, dy, dw, dh = 820, 360, 300, 440
    s += SL(Z_SRED, f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="6"'
                    f' fill="#2a2620" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}"'
                    f' fill="{SVET}" opacity="{.5*otk:.2f}"/>')
    s += SL(Z_SRED, dver(dx, dy, dw * (1 - otk * .62) + 6, dh, 0.0,
                         "url(#derev)", True, False))
    s += SL(Z_SRED, teplo(dx + dw * .5, dy + dh * .5, 520 * otk + 60,
                          440 * otk + 60, .4 * otk))
    # рука с хлопушкой указывает из двери
    if otk > .4:
        ruk, (kx, ky) = rukav(dx + dw - 20, dy + 210, 150, 12, t, "#3a3346",
                              "#ffd98a", .2, 5.0)
        s += SL(Z_SRED, ruk)
        s += SL(Z_SRED, _hlopushka(kx + 44, ky + 6, .45, t,
                                   A.out(A.seg(t, 2.0, .3)), -16))
    # ОЧЕРЕДЬ ДЕВОЧЕК со спины: от двери к нам, растут по размеру
    step = A.w(t, 1.6, .1)
    for i in range(7):
        p = i / 6
        zx_ = 1180 - p * 220 + (i % 2) * 34
        zy_ = 790 + p * 130
        h_ = 210 + p * 150
        s += SL(Z_SRED, figura(zx_, zy_ + 6 * step * ((i % 2) * 2 - 1), h_, t,
                               ("#5b2f3a", "#2e4a5a", "#4a3a5a", "#3f4a3a",
                                "#6b3a44", "#2e3a46", "#5a4a3a")[i],
                               "#ffd0a0", i % 3 == 0, .14 * i, False, 1.0,
                               False, 1.0, False, False, False))
        for sgn in (-1, 1):             # косички
            s += SL(Z_SRED, f'<path d="M{zx_+sgn*h_*.06:.0f},{zy_-h_*.78:.0f}'
                            f' q{sgn*h_*.05:.0f},{h_*.14:.0f}'
                            f' {sgn*h_*.02+2*step:.0f},{h_*.26:.0f}" fill="none"'
                            f' stroke="#5e4428" stroke-width="{max(4, h_*.028):.0f}"'
                            f' stroke-linecap="round"/>')
    # ДВЕ ПОДРУГИ крупно в хвосте очереди
    ax, bx_ = 330, 700
    s += SL(Z_SRED, figura(ax, 1076, 680, t, "#8a4a52", "#ffd0a0", False, .3,
                           False, 1.0, False, 1.2, False, True))
    s += SL(Z_SRED, figura(bx_, 1080, 650, t, "#2e4a5a", "#ffd0a0", False, .7,
                           False, 1.0, False, -1.2, False, True))
    for sgn in (-1, 1):                 # косички подруг
        for cx_, h_ in ((ax, 680), (bx_, 650)):
            s += SL(Z_SRED, f'<path d="M{cx_+sgn*h_*.07:.0f},{1076-h_*.78:.0f}'
                            f' q{sgn*h_*.06:.0f},{h_*.16:.0f}'
                            f' {sgn*h_*.02+4*step:.0f},{h_*.30:.0f}" fill="none"'
                            f' stroke="#5e4428" stroke-width="{h_*.03:.0f}"'
                            f' stroke-linecap="round"/>')
    # бант: её поправляют
    pop = A.w(t, 1.1, .2)
    bny = 1076 - 680 * .96
    s += SL(Z_SRED, f'<g transform="rotate({6*pop:.1f} {ax:.0f} {bny:.0f})">'
                    f'<path d="M{ax-90:.0f},{bny:.0f} q52,-56 86,-6'
                    f' q34,-52 86,6 q-38,52 -86,12 q-46,38 -86,-12 Z"'
                    f' fill="{TKAN}" {o(6)}/>'
                    f'<circle cx="{ax-4:.0f}" cy="{bny+6:.0f}" r="18"'
                    f' fill="#8a1c24" {o(4)}/></g>')
    ruk, (kx, ky) = rukav(ax + 90, 740, 150, -78 + 14 * pop, t, "#8a4a52",
                          "#ffd0a0", .2, 6.0)
    s += SL(Z_SRED, ruk)
    # вторая зевает и ест булку, булка падает
    zev = max(0.0, A.w(t, 2.4, .3))
    s += SL(Z_SRED, f'<ellipse cx="{bx_+30:.0f}" cy="{1080-650*.80:.0f}" rx="26"'
                    f' ry="{10+22*zev:.0f}" fill="#7d2f28" {o(3)}/>')
    pad = A.ease(A.seg(t, 2.2, .8))
    bulx = bx_ + 150
    buly = 860 + pad * 200
    s += SL(Z_SRED, f'<g transform="rotate({pad*140:.0f} {bulx:.0f} {buly:.0f})">'
                    f'<ellipse cx="{bulx:.0f}" cy="{buly:.0f}" rx="66" ry="44"'
                    f' fill="#c98c55" {o(6)}/>'
                    f'<ellipse cx="{bulx-14:.0f}" cy="{buly-12:.0f}" rx="40"'
                    f' ry="22" fill="#e8bd84" opacity=".8"/>'
                    f'<path d="M{bulx-40:.0f},{buly-16:.0f} q40,-18 80,0"'
                    f' fill="none" stroke="#a8641e" stroke-width="7"/></g>')
    ruk2, _ = rukav(bx_ + 80, 800, 130, -24, t, "#2e4a5a", "#ffd0a0", .4, 6.0)
    s += SL(Z_SRED, ruk2)
    for i, cx_ in ((0, ax - 150), (1, bx_ + 190)):   # школьные сумки
        s += SL(Z_SRED, f'<rect x="{cx_-70:.0f}" y="{950-i*10:.0f}" width="140"'
                        f' height="110" rx="14" fill="{("#5a3a22", "#3a4a5a")[i]}"'
                        f' {o(6)}/>')
        s += SL(Z_SRED, f'<path d="M{cx_-70:.0f},{966-i*10:.0f} h140" stroke="#2f2a22"'
                        f' stroke-width="8"/>')
        s += SL(Z_SRED, f'<path d="M{cx_-40:.0f},{950-i*10:.0f} q40,-80 80,0"'
                        f' fill="none" stroke="{("#5a3a22", "#3a4a5a")[i]}"'
                        f' stroke-width="12"/>')
    s += SL(Z_SRED, lavka(1420, 920, 380))
    s += SL(Z_SRED, _chashka(1620, 916, 1.2, t, .2, KREM, True))
    s += SL(Z_SRED, par(1620, 850, t, 3, .4, 150, .4, .8))
    s += SL(Z_PERED, ramka_pp("pravo", "#1d1b16", .7))
    s += vinetka(.44)
    return s


# ── 98 ─────────────────────────────────────────────────────────────────────
def dve_afishi_parizhskogo_kinoteatra(t):
    """Фасад кинотеатра с бегущими лампочками: в двух световых коробах две
    афиши — паровоз в клубах пара и женская шляпка с вуалью, меч, воткнутый в
    зелёный холм. Прохожие останавливаются, огни отражаются в мокрой мостовой."""
    rnd = random.Random(9829)
    s = f'<rect width="{W}" height="{H}" fill="#161822"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#1f2230"/>')
    fas = (f'<rect x="0" y="40" width="{W}" height="860" fill="#3a3a48" {o(8)}/>')
    fas += kladka(0, 40, W, 860, 82, "#44445a")
    fas += (f'<path d="M-40,120 h2000 l-90,-90 h-1820 Z" fill="#2e2e3c" {o(7)}/>')
    s += SL(Z_DAL, fas)
    s += SL(Z_DAL, f'<rect y="880" width="{W}" height="200" fill="#2a2c36" {o(5)}/>')
    # бегущие лампочки по фасаду и вокруг коробов
    s += SL(Z_SRED, _lampochki(60, 140, 1800, 26, t, 15, SVET))
    s += SL(Z_SRED, _lampochki(60, 862, 1800, 26, t, 13, "#ffd0a0"))
    s += SL(Z_SRED, teplo(960, 480, 1500, 900, .22 + .05 * abs(A.w(t, 1.4))))
    # ДВА СВЕТОВЫХ КОРОБА С АФИШАМИ
    for i, (cx_, vid_) in enumerate(((520, "parovoz"), (1420, "mech"))):
        kor = (f'<rect x="{cx_-310:.0f}" y="190" width="620" height="700" rx="14"'
               f' fill="#2b2b36" {o(8)}/>')
        kor += (f'<rect x="{cx_-280:.0f}" y="220" width="560" height="640" rx="8"'
                f' fill="#efe7d2" opacity=".2"/>')
        s += SL(Z_SRED, kor)
        s += SL(Z_SRED, _afisha(cx_, 540, 530, 610, t, vid_, 9833 + i, 0.0, 0.0))
        if vid_ == "parovoz":            # шляпка с вуалью — на той же афише
            s += SL(Z_SRED, _afisha(cx_ + 140, 700, 180, 190, t, "shlyapka",
                                    9839, -4, 0.0))
        s += SL(Z_SRED, _lampochki(cx_ - 300, 196, 600, 13, t, 12, SVET))
        s += SL(Z_SRED, _lampochki(cx_ - 300, 884, 600, 13, t, 12, SVET))
        s += SL(Z_SRED, teplo(cx_, 540, 700, 700, .20))
    s += SL(Z_SRED, par(640, 520, t, 5, .4, 230, .42, 1.2))
    # козырёк над входом и фонари
    s += SL(Z_SRED, f'<path d="M820,900 h280 l40,-70 h-360 Z" fill="#3a3a48" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="860" y="900" width="200" height="180" rx="8"'
                    f' fill="#241f28" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="880" y="920" width="160" height="160"'
                    f' fill="{SVET}" opacity="{.28+.1*abs(A.w(t,1.8)):.2f}"/>')
    for i, fx_ in ((0, 790), (1, 1130)):
        s += SL(Z_SRED, f'<rect x="{fx_-10:.0f}" y="620" width="20" height="280"'
                        f' rx="8" fill="#2f3337" {o(5)}/>')
        s += SL(Z_SRED, f'<path d="M{fx_-54:.0f},620 h108 l-14,-40 h-80 Z"'
                        f' fill="#2f3337" {o(4)}/>')
        s += SL(Z_SRED, ogon(fx_, 580, t, .55, .2 + i * .3, 4))
        s += SL(Z_SRED, teplo(fx_, 580, 420, 360, .34))
    # прохожие останавливаются
    for i, (zx_, h_, col, pl) in enumerate(((240, 430, "#2b3040", False),
                                            (1020, 470, "#3f2f3a", True),
                                            (1700, 440, "#2e3a46", False))):
        stop = A.ease(A.seg(t, .6 + i * .5, 1.0))
        s += SL(Z_SRED, figura(zx_ + (1 - stop) * (60 - i * 50), 1010, h_, t,
                               col, "#cfe4f5", pl, .2 * i, True, 1.0, True,
                               1.0, i == 2, i != 2))
        s += SL(Z_SRED, para_izo_rta(zx_ + 54, 1010 - h_ * .80, t, i * .3, 1.1,
                                     .5))
    # мокрая мостовая: огни отражаются полосами
    s += SL(Z_SRED, f'<rect y="1000" width="{W}" height="80" fill="#30333e"'
                    f' opacity=".9"/>')
    for i in range(14):
        xx = 60 + i * 136
        yar = .18 + .24 * max(0.0, 1 - abs(((t * .9 + i / 14) % 1.0) - .5) * 3.2)
        s += SL(Z_SRED, f'<rect x="{xx:.0f}" y="1000" width="26" height="80"'
                        f' fill="{SVET}" opacity="{yar:.2f}"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{160+i*260:.0f}" cy="{1046+(i%3)*10:.0f}"'
                        f' rx="{90+i*8:.0f}" ry="14" fill="#6a7a84"'
                        f' opacity=".32"/>')
    s += SL(Z_SRED, _golub(1760, 1012, 1.1, t, .3, 0.0))
    s += SL(Z_PERED, ramka_pp("oba", "#101218", .76))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 9851, .4, .9))
    s += vinetka(.46)
    return s


# ── 99 ─────────────────────────────────────────────────────────────────────
def devochka_vybegaet_za_dver(t):
    """Дверь с пятью подковами над притолокой, рядом на лавке Ерёма грозит
    пальцем. Девочка с косичками весело проскальзывает у него под рукой и
    распахивает дверь: за ней красная дорожка и вспышки."""
    rnd = random.Random(9931)
    s = f'<rect width="{W}" height="{H}" fill="#2a2018"/>'
    s += SL(Z_DAL, brevna(0, 0, W, 900, 118))
    s += SL(Z_DAL, f'<rect width="{W}" height="900" fill="#49351f" opacity=".4"/>')
    s += SL(Z_DAL, polovicy(900, "url(#pol)"))
    s += SL(Z_DAL, pech(40, 300, 300, 560, t, True, True, False))
    s += SL(Z_SRED, svecha(1330, 760, t, .2, 2.4, 150))
    s += SL(Z_SRED, teplo(1330, 690, 720, 600, .48 + .12 * abs(A.w(t, 1.5))))
    # ДВЕРЬ распахивается: за ней красная дорожка и вспышки
    otk = A.out(A.seg(t, 1.0, 1.2))
    dx, dy, dw, dh = 560, 230, 640, 850
    s += SL(Z_SRED, f'<rect x="{dx-40}" y="{dy-40}" width="{dw+80}"'
                    f' height="{dh+40}" rx="10" fill="url(#derev)" {o(9)}/>')
    za = (f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#1a1824"/>')
    za += (f'<path d="M{dx+60:.0f},{dy+dh:.0f} L{dx+dw*.34:.0f},{dy+dh*.46:.0f}'
           f' L{dx+dw*.66:.0f},{dy+dh*.46:.0f} L{dx+dw-60:.0f},{dy+dh:.0f} Z"'
           f' fill="{KRAS}" {o(6)}/>')
    for i in range(6):                   # ступени дорожки
        za += (f'<path d="M{dx+70+i*18:.0f},{dy+dh-40-i*58:.0f}'
               f' h{dw-140-i*36:.0f}" stroke="#8a1c24" stroke-width="8"'
               f' opacity=".7"/>')
    for i in range(7):                   # вспышки сверкают
        yar = max(0.0, A.w(t, .5 + i * .13, i * .21))
        za += (f'<circle cx="{dx+70+i*78:.0f}" cy="{dy+dh*.30+(i%3)*50:.0f}"'
               f' r="{24+40*yar:.0f}" fill="#ffffff"'
               f' opacity="{.85*yar*otk:.2f}"/>')
        if yar > .6:
            for j in range(6):
                a = j * 1.047
                za += (f'<line x1="{dx+70+i*78:.0f}"'
                       f' y1="{dy+dh*.30+(i%3)*50:.0f}"'
                       f' x2="{dx+70+i*78+math.cos(a)*90*yar:.0f}"'
                       f' y2="{dy+dh*.30+(i%3)*50+math.sin(a)*90*yar:.0f}"'
                       f' stroke="#ffffff" stroke-width="7"'
                       f' opacity="{.6*yar*otk:.2f}"/>')
    za += (f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#fff6dc"'
           f' opacity="{.12*otk:.2f}"/>')
    s += SL(Z_SRED, za)
    s += SL(Z_SRED, f'<g transform="translate({dx:.0f},0)'
                    f' scale({1-otk*.72:.3f},1) translate({-dx:.0f},0)">'
                    + dver(dx, dy, dw, dh, 0.0, "url(#derev)", True, False)
                    + '</g>')
    s += SL(Z_SRED, teplo(dx + dw * .5, dy + dh * .4, 700 * otk + 80,
                          600 * otk + 80, .34 * otk))
    # ПЯТЬ ПОДКОВ над притолокой
    for i in range(5):
        s += SL(Z_SRED, _podkova_rzh(dx + 70 + i * 130, dy - 100, .62, t,
                                     2.0 * (i - 2)))
    s += SL(Z_SRED, f'<path d="M{dx-120},{dy-180} h{dw+240} l-64,-70 h{-dw-112} Z"'
                    f' fill="{DOSKA2}" {o(9)}/>')
    # Ерёма на лавке грозит пальцем и хохочет в бороду
    s += SL(Z_SRED, lavka(1380, 960, 440))
    ex = 1560
    hoh = 8 * A.w(t, 1.0, .2)
    s += SL(Z_SRED, f'<g transform="rotate({hoh*.3:.1f} {ex:.0f} 960)">'
                    + figura(ex, 960, 640, t, "#4a3a2c", "#ffd98a", False, .2,
                             False, 1.0, True, 1.0 + hoh * .2, True)
                    + '</g>')
    ruk, (kx, ky) = rukav(ex - 150, 660, 120, 196 - 16 * A.w(t, .9), t,
                          "#4a3a2c", "#ffd98a", .2, 7.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky+6:.0f}" rx="52" ry="46"'
                    f' fill="#f0cfae" {o(6)}/>')
    s += SL(Z_SRED, f'<path d="M{kx-10:.0f},{ky-24:.0f} l{-6:.0f},{-86:.0f}"'
                    f' fill="none" stroke="#f0cfae" stroke-width="34"'
                    f' stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M{kx-10:.0f},{ky-24:.0f} l{-6:.0f},{-86:.0f}"'
                    f' fill="none" stroke="{K}" stroke-width="4" opacity=".6"/>')
    for i in range(3):                   # согнутые пальцы кулака
        s += SL(Z_SRED, f'<ellipse cx="{kx+16+i*6:.0f}" cy="{ky-10+i*26:.0f}"'
                        f' rx="20" ry="13" fill="#e2bb98" {o(3)}/>')
    # девочка проскальзывает под рукой к двери
    skol = A.ease(A.seg(t, .3, 1.6))
    gx = 1300 - skol * 420
    s += SL(Z_SRED, f'<g transform="rotate({-10-8*skol:.1f} {gx:.0f} 1070)">'
                    + figura(gx, 1070, 430, t, "#8a4a52", "#ffd98a", False, .6,
                             True, 1.0, False, 1.0, False, True)
                    + '</g>')
    for sgn in (-1, 1):                 # косички на бегу
        s += SL(Z_SRED, f'<path d="M{gx+sgn*30:.0f},{1070-430*.78:.0f}'
                        f' q{40+sgn*10:.0f},{30:.0f} {70:.0f},{70+10*A.w(t,1.2,sgn*.2):.0f}"'
                        f' fill="none" stroke="#5e4428" stroke-width="13"'
                        f' stroke-linecap="round"/>')
    s += SL(Z_SRED, kot(1180, 1000, t, 1.2, "#3b3430", False))
    s += SL(Z_PERED, ramka_pp("levo", "#1a120c", .78))
    s += SL(Z_PERED, _valenok(1760, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_LETIT, iskra_let(t, 1500, 720, 6, 9941, 260, .35))
    s += vinetka(.46)
    return s


# ── 100 ────────────────────────────────────────────────────────────────────
def babushkina_dver_s_sekretami(t):
    """Старая дверь бабушкиного дома изнутри на пол-кадра: обита дерматином в
    клетку, цепкий крючок, половик у порога. По очереди подсвечиваются три
    места — ржавая подкова над притолокой, пучок сухой рябины за наличником и
    английская булавка, воткнутая в косяк. Внучка встаёт на цыпочки."""
    rnd = random.Random(10007)
    s = f'<rect width="{W}" height="{H}" fill="#2e2620"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#7a6a58"/>')
    for i in range(10):                  # обои прихожей
        s += SL(Z_DAL, f'<rect x="{i*196:.0f}" y="0" width="74" height="1080"'
                       f' fill="#8a7a66" opacity=".45"/>')
    s += SL(Z_DAL, polovicy(930, "#6b4a2a"))
    s += SL(Z_DAL, _veshalka(60, 230, 300, t, 3, True))
    s += SL(Z_SRED, tusklaya_lampochka(300, 110, t, 1.4, True))
    s += SL(Z_SRED, teplo(300, 250, 820, 700, .38 + .1 * abs(A.w(t, 1.6))))
    # ДВЕРЬ, обитая дерматином — главный предмет
    dx, dy, dw, dh = 620, 180, 720, 890
    dv = (f'<rect x="{dx-44}" y="{dy-44}" width="{dw+88}" height="{dh+44}" rx="10"'
          f' fill="url(#derev)" {o(10)}/>')
    dv += (f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="8"'
           f' fill="#5a3f3a" {o(9)}/>')
    for i in range(5):                   # дерматин в клетку на гвоздиках
        for j in range(6):
            cx_ = dx + 70 + i * (dw - 140) / 4
            cy_ = dy + 80 + j * (dh - 160) / 5
            dv += (f'<circle cx="{cx_:.0f}" cy="{cy_:.0f}" r="11"'
                   f' fill="url(#zhel)" {o(3)}/>')
            dv += (f'<circle cx="{cx_-3:.0f}" cy="{cy_-3:.0f}" r="4"'
                   f' fill="#e8eef6" opacity=".5"/>')
    for i in range(5):                  # прошивка дерматина — ромбы наискось
        for j in range(6):
            cx_ = dx + 70 + i * (dw - 140) / 4
            cy_ = dy + 80 + j * (dh - 160) / 5
            dv += (f'<path d="M{cx_:.0f},{cy_:.0f} l{(dw-140)/8:.0f},'
                   f'{(dh-160)/10:.0f}" stroke="#3f2b26" stroke-width="12"'
                   f' opacity=".85"/>')
            dv += (f'<path d="M{cx_:.0f},{cy_:.0f} l{(dw-140)/8:.0f},'
                   f'{-(dh-160)/10:.0f}" stroke="#3f2b26" stroke-width="12"'
                   f' opacity=".85"/>')
            dv += (f'<path d="M{cx_+6:.0f},{cy_+6:.0f} l{(dw-140)/8:.0f},'
                   f'{(dh-160)/10:.0f}" stroke="#7a5a52" stroke-width="5"'
                   f' opacity=".5"/>')
    dv += (f'<ellipse cx="{dx+dw-80:.0f}" cy="{dy+dh*.50:.0f}" rx="26" ry="38"'
           f' fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, dv)
    # цепкий крючок с цепочкой
    s += SL(Z_SRED, f'<rect x="{dx-30:.0f}" y="{dy+dh*.40:.0f}" width="54"'
                    f' height="26" rx="8" fill="#5d6168" {o(5)}/>')
    kch = 7 * A.w(t, 2.2, .1)
    s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {dx+24:.0f} {dy+dh*.42:.0f})">'
                    f'<path d="M{dx+24:.0f},{dy+dh*.42:.0f} q80,16 120,-10'
                    f' q16,-12 4,-28" fill="none" stroke="#8d949b"'
                    f' stroke-width="14" stroke-linecap="round"/></g>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{dx+40+i*22:.0f}"'
                        f' cy="{dy+dh*.44+5*A.w(t,2.0,i*.2):.0f}" r="9"'
                        f' fill="none" stroke="#8d949b" stroke-width="5"/>')
    # три секрета подсвечиваются по очереди
    pod1 = A.ease(A.seg(t, .5, .6)) * (1 - A.ease(A.seg(t, 2.6, .6)))
    pod2 = A.ease(A.seg(t, 1.6, .6)) * (1 - A.ease(A.seg(t, 3.6, .6)))
    pod3 = A.ease(A.seg(t, 2.8, .6))
    px_, py_ = dx + dw / 2, dy - 120
    s += SL(Z_SRED, teplo(px_, py_ + 110, 560 * pod1 + 80, 460 * pod1 + 80,
                          .54 * pod1 + .08))
    s += SL(Z_SRED, _podkova_rzh(px_, py_ + 110, 1.05, t))
    s += SL(Z_SRED, f'<path d="M{dx-130},{dy-184} h{dw+260} l-62,-66 h{-dw-136} Z"'
                    f' fill="{DOSKA2}" {o(9)}/>')
    # пучок сухой рябины за наличником
    rx_, ry_ = dx - 70, dy + 250
    s += SL(Z_SRED, teplo(rx_, ry_, 420 * pod2 + 50, 360 * pod2 + 50, .46 * pod2))
    for i in range(5):                  # пучок стянут в кисть, не враскид
        a = -.5 + i * .25
        s += SL(Z_SRED, f'<line x1="{rx_:.0f}" y1="{ry_+118:.0f}"'
                        f' x2="{rx_+math.cos(a)*34:.0f}"'
                        f' y2="{ry_+118-abs(math.sin(a))*20-86:.0f}"'
                        f' stroke="#6b5234" stroke-width="{11-i}"'
                        f' stroke-linecap="round"/>')
    s += SL(Z_SRED, grozd_ryabiny(rx_ + 20, ry_ + 30, t, 1.5, 16, 10009, .2))
    s += SL(Z_SRED, f'<path d="M{rx_-30:.0f},{ry_+120:.0f} q34,16 68,0"'
                    f' fill="none" stroke="#c2ab86" stroke-width="10"/>')
    # английская булавка в косяке поблёскивает
    bx_, by_ = dx + dw + 60, dy + 480
    s += SL(Z_SRED, teplo(bx_, by_, 320 * pod3 + 40, 280 * pod3 + 40, .42 * pod3))
    bl = .35 + .55 * (0.5 + 0.5 * A.w(t, 1.6, .2))
    s += SL(Z_SRED, f'<path d="M{bx_-16:.0f},{by_-120:.0f} q-54,118 4,232'
                    f' q48,-16 22,-90" fill="none" stroke="#e2e9ef"'
                    f' stroke-width="18" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<circle cx="{bx_-12:.0f}" cy="{by_+118:.0f}" r="24"'
                    f' fill="none" stroke="#e2e9ef" stroke-width="13"/>')
    s += SL(Z_SRED, f'<circle cx="{bx_-6:.0f}" cy="{by_-66:.0f}" r="15"'
                    f' fill="#ffffff" opacity="{bl:.2f}"/>')
    # половик у порога сминается
    sm = A.w(t, 1.3, .1)
    s += SL(Z_SRED, f'<rect x="{dx+60:.0f}" y="{dy+dh-54:.0f}" width="{dw-120:.0f}"'
                    f' height="72" rx="14" fill="{TKAN2}" {o(7)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{dx+90+i*62:.0f},{dy+dh-46:.0f}'
                        f' q{6+5*sm:.0f},32 0,60" fill="none" stroke="#2f4a62"'
                        f' stroke-width="9" opacity=".8"/>')
    # внучка встаёт на цыпочки к подкове
    cyp = A.ease(A.seg(t, .8, 1.2))
    vx = dx + dw * .32
    s += SL(Z_SRED, figura(vx, 1058 - 26 * cyp, 480, t, "#8a4a52", "#ffd98a",
                           False, .4, False, 1.0, False, 1.2, False, True))
    ruk, (kx, ky) = rukav(vx + 80, 760 - 26 * cyp, 190, -78, t, "#8a4a52",
                          "#ffd98a", .3, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="28" ry="21"'
                    f' fill="#8a4a52" {o(5)}/>')
    s += SL(Z_SRED, _valenok(400, 1012, .9, t, .3, True, "#6e6358"))
    s += SL(Z_SRED, _valenok(510, 1012, .86, t, .6, True, "#6e6358"))
    s += SL(Z_SRED, kot(1700, 1012, t, 1.3, "#4a4440", True))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="70" height="1080" fill="#241d16"'
                     f' opacity=".9"/>')
    s += SL(Z_PERED, _varezhka(1800, 440, 1.5, t, .3, TKAN, True))
    s += vinetka(.44)
    return s


# ── 101 ────────────────────────────────────────────────────────────────────
def vecherniy_dom_okno_ryabina_valenki(t):
    """Уютная прихожая и комната вечером одним кадром: на окне загорается
    настольная лампа под абажуром, у входной двери вспыхивает красным ветка
    рябины в вазе, под вешалкой встают рядком три пары валенок — большие,
    средние и крошечные. Кот проходит вдоль валенок."""
    rnd = random.Random(10111)
    s = f'<rect width="{W}" height="{H}" fill="#2b2420"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#6f6052"/>')
    for i in range(10):                  # обои в мелкий цветок — пятнами
        for j in range(7):
            s += SL(Z_DAL, f'<circle cx="{70+i*196:.0f}" cy="{80+j*140:.0f}"'
                           f' r="13" fill="#8a7a64" opacity=".45"/>')
    s += SL(Z_DAL, f'<rect y="860" width="{W}" height="34" fill="#8d7f6e" {o(5)}/>')
    s += SL(Z_DAL, polovicy(894, "#6b4a2a"))
    s += SL(Z_DAL, kvartira_veschi(1520, 300, 380, t, 10113))
    # окно слева с настольной лампой: лампа загорается
    okx, oky, okw, okh = 160, 150, 540, 460
    vid = (f'<rect x="{okx}" y="{oky}" width="{okw}" height="{okh}"'
           f' fill="url(#nnoch)"/>')
    for i in range(18):
        vid += (f'<circle cx="{okx+rnd.random()*okw:.0f}"'
                f' cy="{oky+rnd.random()*okh*.62:.0f}"'
                f' r="{rnd.uniform(1.5,3):.1f}" fill="#cfe4f5"'
                f' opacity="{.4+.5*abs(A.w(t,2.6+i*.2,i*.1)):.2f}"/>')
    for i in range(4):
        bx = okx + 40 + i * 130
        vid += (f'<rect x="{bx:.0f}" y="{oky+okh*.56:.0f}" width="90"'
                f' height="{okh*.44:.0f}" fill="#242c3c" opacity=".92"/>')
        if i % 2 == 0:
            vid += (f'<rect x="{bx+24:.0f}" y="{oky+okh*.62:.0f}" width="36"'
                    f' height="36" fill="{SVET}" opacity=".5"/>')
    s += SL(Z_SRED, okno_izby(okx, oky, okw, okh, t, vid, .18, False, True))
    s += SL(Z_SRED, f'<rect x="{okx-60}" y="{okh+oky+20}" width="{okw+120}"'
                    f' height="36" rx="10" fill="{DOSKA}" {o(6)}/>')
    zazh = A.ease(A.seg(t, .4, .9))
    s += SL(Z_SRED, _lampa_abazhur(okx + 160, okh + oky + 16, t, 2.0, zazh))
    s += SL(Z_SRED, teplo(okx + 160, okh + oky - 190, 940 * zazh + 160,
                          800 * zazh + 160, .56 * zazh + .08))
    s += SL(Z_SRED, _chashka(okx + 400, okh + oky + 18, 1.3, t, .2, KREM, True))
    s += SL(Z_SRED, par(okx + 400, okh + oky - 60, t, 3, .4 * zazh + .1, 160,
                        .4, .8))
    # входная дверь справа и ваза с рябиной у неё
    dx, dy, dw, dh = 1300, 130, 440, 760
    s += SL(Z_SRED, dver(dx, dy, dw, dh, 0.0, "#6b5440", True, True))
    s += SL(Z_SRED, f'<rect x="{dx+dw*.16:.0f}" y="{dy+dh*.08:.0f}"'
                    f' width="{dw*.68:.0f}" height="{dh*.32:.0f}" rx="8"'
                    f' fill="none" stroke="#4a382a" stroke-width="14"/>')
    s += SL(Z_SRED, _podkova_rzh(dx + dw / 2, dy - 110, .95, t))
    vsp = A.ease(A.seg(t, 1.4, 1.0))
    vx_, vy_ = 1250, 890
    s += SL(Z_SRED, f'<rect x="{vx_-130:.0f}" y="{vy_-230:.0f}" width="260"'
                    f' height="230" rx="10" fill="url(#derev)" {o(8)}/>')
    s += SL(Z_SRED, _vaza(vx_, vy_ - 240, 1.15, t, False))
    s += SL(Z_SRED, f'<path d="M{vx_:.0f},{vy_-630:.0f} q-18,-120 -8,-250"'
                    f' fill="none" stroke="#5e4428" stroke-width="16"/>')
    for i in range(4):
        s += SL(Z_SRED, grozd_ryabiny(vx_ + (-1 if i % 2 else 1) * (70 + i * 10),
                                      vy_ - 660 - i * 60, t, 1.5 + .3 * vsp, 18,
                                      10117 + i, i * .2))
    s += SL(Z_SRED, teplo(vx_, vy_ - 700, 520 * vsp, 440 * vsp, .3 * vsp))
    # вешалка и ТРИ ПАРЫ ВАЛЕНОК рядком
    s += SL(Z_SRED, _veshalka(420, 210, 440, t, 4, True))
    for i, (sc, px_) in enumerate(((2.9, 500), (1.7, 830), (.85, 1040))):
        vst = A.out(A.seg(t, 1.0 + i * .34, .6))
        for j, sgn in ((0, -1), (1, 1)):
            s += SL(Z_SRED, _valenok(px_ + sgn * 40 * sc,
                                     1056 + 80 * (1 - vst) + j * 10, sc, t,
                                     .2 + i * .3 + j * .2, True,
                                     ("#c4b091", "#a89878", "#d8c7a6")[i],
                                     sgn * 4))
    s += SL(Z_SRED, f'<rect x="300" y="1050" width="880" height="28" rx="10"'
                    f' fill="{TKAN2}" opacity=".75" {o(4)}/>')
    # кот проходит вдоль валенок
    hod = A.ease(A.seg(t, 1.8, 2.2))
    s += SL(Z_SRED, kot(640 + hod * 620, 1066, t, 1.35, "#3b3430", False))
    s += SL(Z_PERED, zanaveska(120, 90, 300, 150, TKAN, t, 1))
    s += SL(Z_PERED, zanaveska(760, 90, 300, 150, TKAN, t, -1))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="60" height="1080" fill="#241d18"'
                     f' opacity=".88"/>')
    s += vinetka(.42)
    return s


# ── 102 ────────────────────────────────────────────────────────────────────
def chaynik_na_svoem_ogne(t):
    """Кухонная плита: под пузатым чайником на пол-кадра горит синий венчик
    газа, чайник пускает пар. Вокруг плиты за столом собирается семья с
    чашками, хозяйка возвращается к столу."""
    rnd = random.Random(10213)
    s = f'<rect width="{W}" height="{H}" fill="#2a2622"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="1080" fill="#79706a"/>')
    for i in range(9):                   # кафель над плитой
        for j in range(4):
            s += SL(Z_DAL, f'<rect x="{30+i*212:.0f}" y="{60+j*150:.0f}"'
                           f' width="190" height="128" rx="6" fill="#8d8780"'
                           f' opacity=".55" {o(3)}/>')
    s += SL(Z_DAL, polovicy(900, "#6b5a4a"))
    s += SL(Z_DAL, kvartira_veschi(1600, 200, 320, t, 10219))
    s += SL(Z_SRED, tusklaya_lampochka(1180, 100, t, 1.4, True))
    # ПЛИТА и ЧАЙНИК — главный предмет слева-центре
    plx, ply, plw = 540, 900, 700
    pl = (f'<rect x="{plx-plw/2:.0f}" y="{ply-320:.0f}" width="{plw:.0f}"'
          f' height="320" rx="14" fill="#cfd2d4" {o(9)}/>')
    pl += (f'<rect x="{plx-plw/2+14:.0f}" y="{ply-300:.0f}" width="{plw-28:.0f}"'
           f' height="120" rx="10" fill="#9aa1a8" opacity=".6"/>')
    pl += (f'<rect x="{plx-plw/2:.0f}" y="{ply-360:.0f}" width="{plw:.0f}"'
           f' height="54" rx="12" fill="#5d6168" {o(7)}/>')
    for i in range(4):                   # ручки-краны плиты
        pl += (f'<circle cx="{plx-plw/2+90+i*(plw-180)/3:.0f}" cy="{ply-200:.0f}"'
               f' r="26" fill="#3f454a" {o(5)}/>')
        ang = -40 + i * 26 + 8 * A.w(t, 2.4, i * .2)
        pl += (f'<line x1="{plx-plw/2+90+i*(plw-180)/3:.0f}" y1="{ply-200:.0f}"'
               f' x2="{plx-plw/2+90+i*(plw-180)/3+math.cos(math.radians(ang))*22:.0f}"'
               f' y2="{ply-200+math.sin(math.radians(ang))*22:.0f}"'
               f' stroke="#e8eef6" stroke-width="7"/>')
    pl += (f'<rect x="{plx-plw/2+40:.0f}" y="{ply-160:.0f}" width="{plw-80:.0f}"'
           f' height="130" rx="10" fill="#3a3f46" {o(6)}/>')
    pl += (f'<rect x="{plx-plw/2+60:.0f}" y="{ply-140:.0f}" width="{plw-120:.0f}"'
           f' height="90" rx="8" fill="#8a5a2a" opacity=".45"/>')
    s += SL(Z_SRED, pl)
    # синий венчик огня под чайником
    gx_, gy_ = plx - 120, ply - 362
    s += SL(Z_SRED, f'<circle cx="{gx_:.0f}" cy="{gy_:.0f}" r="92" fill="#3a3f46"'
                    f' {o(6)}/>')
    s += SL(Z_SRED, f'<circle cx="{gx_:.0f}" cy="{gy_:.0f}" r="56" fill="#23262a"'
                    f' {o(4)}/>')
    for i in range(16):                  # венчик: синие язычки по кругу
        a = i * .3927
        hh = 34 + 14 * abs(A.w(t, .5, i * .11))
        s += SL(Z_SRED, f'<path d="M{gx_+math.cos(a)*58:.0f},'
                        f'{gy_+math.sin(a)*58*.4:.0f}'
                        f' q{math.cos(a)*10:.0f},{-hh*.5:.0f}'
                        f' {math.cos(a)*4:.0f},{-hh:.0f}'
                        f' q{-math.cos(a)*14:.0f},{hh*.5:.0f}'
                        f' {-math.cos(a)*14:.0f},{hh:.0f} Z" fill="#4aa3e0"'
                        f' opacity=".85"/>')
        s += SL(Z_SRED, f'<path d="M{gx_+math.cos(a)*58:.0f},'
                        f'{gy_+math.sin(a)*58*.4:.0f}'
                        f' q{math.cos(a)*6:.0f},{-hh*.3:.0f}'
                        f' {math.cos(a)*2:.0f},{-hh*.52:.0f}" fill="none"'
                        f' stroke="#d8f0ff" stroke-width="6" opacity=".7"/>')
    s += SL(Z_SRED, ogon(gx_, gy_ + 6, t, .5, .2, 4, "#5aa0e0"))
    s += SL(Z_SRED, f'<ellipse cx="{gx_:.0f}" cy="{gy_:.0f}" rx="150" ry="70"'
                    f' fill="#4aa3e0" opacity="{.16+.07*abs(A.w(t,1.4)):.2f}"/>')
    s += SL(Z_SRED, teplo(gx_, gy_ - 60, 640, 520, .34 + .1 * abs(A.w(t, 1.5))))
    for i in range(6):                   # решётка горелки: чайник стоит ВЫШЕ огня
        a = i * 1.047
        s += SL(Z_SRED, f'<line x1="{gx_+math.cos(a)*30:.0f}"'
                        f' y1="{gy_+math.sin(a)*12-66:.0f}"'
                        f' x2="{gx_+math.cos(a)*104:.0f}"'
                        f' y2="{gy_+math.sin(a)*40-66:.0f}" stroke="#4a4f55"'
                        f' stroke-width="13" stroke-linecap="round"/>')
    s += SL(Z_SRED, _chaynik(gx_, gy_ - 76, 2.3, t, True, "url(#zhel)"))
    s += SL(Z_SRED, par(gx_ + 170, gy_ - 380, t, 6, .6, 320, .45, 1.4))
    s += SL(Z_SRED, par(gx_ - 20, gy_ - 400, t, 4, .45, 260, .4, 1.1))
    # стол справа, семья собирается с чашками
    s += SL(Z_SRED, stol(1240, 820, 660, 44, True))
    for i, (cx_, ph_) in enumerate(((1330, .1), (1480, .4), (1630, .7),
                                    (1770, .95))):
        pri = A.out(A.seg(t, .6 + i * .34, .7))
        s += SL(Z_SRED, _chashka(cx_, 820 - 50 * pri + 50, 1.35, t, ph_, KREM,
                                 True))
        s += SL(Z_SRED, par(cx_, 760, t, 3, .4 * pri, 160, .4, .8))
    s += SL(Z_SRED, karavay(1200, 816, 1.0, True))
    for i, (fx_, h_, col, pl_, bo) in enumerate((
            (1340, 480, "#3a3346", False, True),
            (1560, 440, "#2e4a5a", True, False),
            (1780, 350, "#6b3a44", False, False))):
        sbor = A.ease(A.seg(t, .4 + i * .4, 1.2))
        s += SL(Z_SRED, figura(fx_ + (1 - sbor) * (120 - i * 40), 1060, h_, t,
                               col, "#ffd98a", pl_, .2 * i, True, 1.0, False,
                               1.0, bo))
    # хозяйка возвращается к столу от плиты
    vozv = A.ease(A.seg(t, 1.2, 1.6))
    hx = 820 + vozv * 260
    s += SL(Z_SRED, figura(hx, 1070, 540, t, "#4a2f3a", "#ffd98a", True, .3,
                           True, 1.0, False, 1.4))
    ruk, (kx, ky) = rukav(hx + 90, 760, 160, -34, t, "#4a2f3a", "#ffd98a", .2, 5.0)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, _chashka(kx + 30, ky + 20, 1.1, t, .5, KREM, False))
    s += SL(Z_SRED, kot(300, 1012, t, 1.3, "#4a4440", False))
    s += SL(Z_SRED, _chugunok(260, 560, 1.1, t, False))
    s += SL(Z_PERED, f'<rect x="0" y="0" width="70" height="1080" fill="#201c18"'
                     f' opacity=".88"/>')
    s += SL(Z_PERED, _banka_krupy(1760, 1012, 1.5, t))
    s += vinetka(.42)
    return s
