# -*- coding: utf-8 -*-
"""Декорации планов 158-185 ролика «Как встречать год хозяйки года 2027»."""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob
OKNO = (860, 300, 980, 551)


# ═══════════════════ КИРПИЧИКИ ЭТОГО БЛОКА ═══════════════════
# Написаны здесь и только здесь: блок про три заботы и финал живёт своими
# предметами — календарь-кармашки, тетрадный листок, узорный ковёр, медальон.

def _grad(i_, c1, c2, x2=0, y2=1):
    return (f'<linearGradient id="{i_}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def _komnata(y_pol=780, obo="#6f5a46", obo2="#50412f", polosy=True):
    """Стена комнаты с обоями в полоску и дощатый пол. Без неё кадр висит
    в пустоте, а наезд камеры не за что зацепить."""
    s = _grad("b8obo", obo, obo2)
    s += f'<rect width="{W}" height="{y_pol+20}" fill="url(#b8obo)"/>'
    if polosy:
        for i in range(17):
            x = i * (W / 16.0)
            s += (f'<rect x="{x:.0f}" y="0" width="22" height="{y_pol:.0f}"'
                  f' fill="#ffffff" opacity=".05"/>')
            s += (f'<rect x="{x+44:.0f}" y="0" width="7" height="{y_pol:.0f}"'
                  f' fill="#2b2016" opacity=".10"/>')
    s += baza.polovicy(y_pol)
    return s


def _kalendar(x, y, t, w_=1420, zapiski=3, goryat=(), n=7, h_=300):
    """Полотняный календарь: n кармашков-дней, последний красный.
    Записки выглядывают из кармашков и дышат — живой элемент главы."""
    kach = 3.4 * A.w(t, 5.2)
    s = ten(x + w_ / 2, y + h_ + 34, w_ * .45, 24, .34)
    s += (f'<rect x="{x-34:.0f}" y="{y-40:.0f}" width="{w_+68:.0f}" height="24" rx="11"'
          f' fill="url(#derev)" {o(6)}/>')
    for k in (0.08, 0.5, 0.92):
        kol = ob.ALYJ2 if k == 0.5 else "#4a3c2c"
        s += (f'<path d="M{x+w_*k:.0f},{y-28:.0f} v24" fill="none" stroke="{kol}"'
              f' stroke-width="6"/>')
    s += (f'<path d="M{x:.0f},{y:.0f} h{w_:.0f} v{h_:.0f}'
          f' q{-w_/2:.0f},{20+kach:.0f} {-w_:.0f},0 z" fill="url(#rush)" {o(7)}/>')
    s += (f'<path d="M{x+14:.0f},{y+20:.0f} h{w_-28:.0f}" fill="none" stroke="{ob.ALYJ}"'
          f' stroke-width="6" opacity=".55"/>')
    pw = w_ / n * .80
    for i in range(n):
        cx = x + w_ * (i + .5) / n
        posl = (i == n - 1)
        col = ob.ALYJ if posl else "#e4d4ad"
        gor = (.74 + .26 * abs(A.w(t, 1.7))) if posl else 1.0
        puls = .55 + .45 * abs(A.w(t, 1.9, i * .3))
        if i in goryat:
            s += teplo(cx, y + h_ * .60, pw * 1.6, h_ * 1.0, .60 * puls)
        # записка выглядывает ИЗ-ЗА кармашка — рисуется раньше него
        if i < zapiski:
            vy = -104 - 17 * A.w(t, 3.3 + i * .55, i * .2)
            kr = 3.4 * A.w(t, 4.1, i * .3)
            s += (f'<g transform="rotate({kr:.2f} {cx:.0f} {y+h_*.34:.0f})">'
                  f'<rect x="{cx-pw*.40:.0f}" y="{y+h_*.34+vy:.0f}" width="{pw*.80:.0f}"'
                  f' height="{-vy+36:.0f}" rx="7" fill="url(#list)" {o(5)}/>')
            for k in range(3):
                s += (f'<path d="M{cx-pw*.28:.0f},{y+h_*.34+vy+30+k*28:.0f} h{pw*.56:.0f}"'
                      f' fill="none" stroke="#6d6258" stroke-width="5" opacity=".75"/>')
            s += '</g>'
        s += (f'<rect x="{cx-pw/2:.0f}" y="{y+h_*.34:.0f}" width="{pw:.0f}"'
              f' height="{h_*.52:.0f}" rx="12" fill="{col}" opacity="{gor:.2f}" {o(6)}/>')
        s += (f'<rect x="{cx-pw/2+6:.0f}" y="{y+h_*.34:.0f}" width="{pw-12:.0f}"'
              f' height="{h_*.10:.0f}" rx="7" fill="#000000" opacity=".22"/>')
        s += (f'<path d="M{cx-pw/2+10:.0f},{y+h_*.48:.0f} h{pw-20:.0f}" fill="none"'
              f' stroke="#ffffff" stroke-width="5" opacity=".32"/>')
        # ПРОШИВКА по краю кармана и ярлык дня — иначе это просто прямоугольник
        s += (f'<rect x="{cx-pw/2+9:.0f}" y="{y+h_*.34+9:.0f}" width="{pw-18:.0f}"'
              f' height="{h_*.52-18:.0f}" rx="9" fill="none" stroke="{"#f6e6c0" if posl else "#9c8a63"}"'
              f' stroke-width="4" stroke-dasharray="11 8" opacity=".85"/>')
        s += (f'<rect x="{cx-pw*.30:.0f}" y="{y+h_*.38:.0f}" width="{pw*.60:.0f}"'
              f' height="{h_*.11:.0f}" rx="6" fill="{"#f3dcc6" if posl else "#cdb98d"}"'
              f' opacity=".9" {o(3)}/>')
        s += (f'<path d="M{cx-pw*.22:.0f},{y+h_*.62:.0f} h{pw*.44:.0f}" fill="none"'
              f' stroke="{"#8d1b1c" if posl else "#b2a075"}" stroke-width="6"'
              f' opacity=".8" stroke-linecap="round"/>')
        if i in goryat:
            s += (f'<rect x="{cx-pw/2:.0f}" y="{y+h_*.34:.0f}" width="{pw:.0f}"'
                  f' height="{h_*.52:.0f}" rx="12" fill="{SVET}" opacity="{.62*puls:.2f}"/>')
            s += (f'<rect x="{cx-pw/2:.0f}" y="{y+h_*.34:.0f}" width="{pw:.0f}"'
                  f' height="{h_*.52:.0f}" rx="12" fill="none" stroke="#fff6d2"'
                  f' stroke-width="8" opacity="{.85*puls:.2f}"/>')
    return s


def _listok(x, y, w_, h_, t, rost=(1.0, 1.0, 1.0), zacherk=(0.0, 0.0, 0.0),
            galka=0.0, ang=-3.0, svet=0.0):
    """Тетрадный листок в линейку: строчки пишутся, зачёркиваются, галочка."""
    s = f'<g transform="rotate({ang:.2f} {x+w_/2:.0f} {y+h_/2:.0f})">'
    s += ten(x + w_ / 2 + 12, y + h_ + 16, w_ * .46, 15, .45)
    if svet > 0:
        s += teplo(x + w_ / 2, y + h_ / 2, w_ * 1.15, h_ * 1.1, svet)
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="7"'
          f' fill="url(#list)" {o(5)}/>')
    for i in range(7):
        yy = y + h_ * (.16 + i * .115)
        s += (f'<line x1="{x+w_*.08:.0f}" y1="{yy:.0f}" x2="{x+w_*.92:.0f}" y2="{yy:.0f}"'
              f' stroke="#8fb6cf" stroke-width="3" opacity=".65"/>')
    s += (f'<line x1="{x+w_*.15:.0f}" y1="{y+6:.0f}" x2="{x+w_*.15:.0f}" y2="{y+h_-6:.0f}"'
          f' stroke="#d9918e" stroke-width="3" opacity=".6"/>')
    wmax = w_ * .60
    for i in range(3):
        yy = y + h_ * (.275 + i * .23)
        u = max(0.0, min(1.0, rost[i]))
        if u <= .01:
            continue
        d = f'M{x+w_*.21:.0f},{yy:.0f}'
        for k in range(1, 11):
            uu = k / 10.0
            if uu > u:
                break
            d += f' L{x+w_*.21+wmax*uu:.0f},{yy + (4 if k % 2 else -4):.0f}'
        s += f'<path d="{d}" fill="none" stroke="#39322e" stroke-width="{max(4,h_*.018):.0f}" stroke-linecap="round"/>'
        z = max(0.0, min(1.0, zacherk[i]))
        if z > .01:
            s += (f'<line x1="{x+w_*.18:.0f}" y1="{yy+3:.0f}"'
                  f' x2="{x+w_*.21+wmax*z:.0f}" y2="{yy-6:.0f}" stroke="{ob.ALYJ}"'
                  f' stroke-width="{max(4,h_*.018):.0f}" stroke-linecap="round"/>')
    if galka > .01:
        gx, gy = x + w_ * .56, y + h_ * .84
        r_ = h_ * .10
        p1 = min(1.0, galka * 2.0); p2 = max(0.0, galka * 2.0 - 1.0)
        s += (f'<path d="M{gx-r_*1.5:.0f},{gy-r_*.2:.0f} l{r_*p1:.0f},{r_*p1:.0f}"'
              f' fill="none" stroke="{ob.ALYJ}" stroke-width="{r_*.42:.0f}" stroke-linecap="round"/>')
        if p2 > .01:
            s += (f'<path d="M{gx-r_*.5:.0f},{gy+r_*.8:.0f} l{r_*2.1*p2:.0f},{-r_*2.5*p2:.0f}"'
                  f' fill="none" stroke="{ob.ALYJ}" stroke-width="{r_*.42:.0f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x+10:.0f},{y+h_*.06:.0f} l{w_*.34:.0f},{h_*.38:.0f}"'
          f' stroke="#ffffff" stroke-width="{max(6,w_*.03):.0f}" opacity=".20"/>')
    return s + '</g>'


def _karandash(tx, ty, ang=-28, L=330, col1="#e6b345", col2="#a3701b"):
    """Карандаш, который пишет сам: рук в этом ролике не рисуем."""
    s = _grad("b8kar", col1, col2)
    s += f'<g transform="translate({tx:.0f},{ty:.0f}) rotate({ang:.1f})">'
    s += ten(L * .5, 54, L * .42, 15, .35)
    s += f'<path d="M0,0 L44,-21 L44,21 Z" fill="#edd6a8" {o(4)}/>'
    s += f'<path d="M0,0 L16,-8 L16,8 Z" fill="#2a2320"/>'
    s += (f'<rect x="42" y="-21" width="{L-96:.0f}" height="42" fill="url(#b8kar)" {o(5)}/>')
    s += (f'<rect x="42" y="-16" width="{L-96:.0f}" height="9" fill="#ffffff" opacity=".22"/>')
    s += f'<rect x="{L-54:.0f}" y="-21" width="28" height="42" fill="url(#zhel)" {o(4)}/>'
    s += f'<rect x="{L-26:.0f}" y="-19" width="26" height="38" rx="9" fill="#cf8e86" {o(4)}/>'
    return s + '</g>'


def _ruchka(tx, ty, ang=-32, L=250):
    """Шариковая ручка — дописывает строчку сама."""
    s = _grad("b8ruch", "#2f5f7a", "#15303f")
    s += f'<g transform="translate({tx:.0f},{ty:.0f}) rotate({ang:.1f})">'
    s += ten(L * .5, 42, L * .4, 12, .3)
    s += f'<path d="M0,0 L34,-15 L34,15 Z" fill="url(#zhel)" {o(4)}/>'
    s += f'<rect x="32" y="-16" width="{L-70:.0f}" height="32" rx="6" fill="url(#b8ruch)" {o(5)}/>'
    s += f'<rect x="32" y="-12" width="{L-70:.0f}" height="7" fill="#ffffff" opacity=".2"/>'
    s += f'<rect x="{L-40:.0f}" y="-16" width="40" height="32" rx="10" fill="#1b2a33" {o(4)}/>'
    return s + '</g>'


def _kover(cid, nl, nr, ny, fl, fr, fy, t, c1="#9c4036", c2="#5a2220",
           uzor="#e3b64a", uop=.9, iznanka=False):
    """Большой узорный ковёр трапецией: ближний край шире дальнего."""
    d = (f'M{nl:.0f},{ny:.0f} L{nr:.0f},{ny:.0f} L{fr:.0f},{fy:.0f} L{fl:.0f},{fy:.0f} Z')
    s = _grad(cid + "g", c1, c2)
    s += f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
    s += f'<path d="{d}" fill="url(#{cid}g)" {o(7)}/>'
    s += f'<g clip-path="url(#{cid})" opacity="{uop:.2f}">'
    if iznanka:
        for i in range(34):
            v = i / 33.0
            yy = fy + (ny - fy) * v
            s += (f'<line x1="{fl+(nl-fl)*v-30:.0f}" y1="{yy:.0f}"'
                  f' x2="{fr+(nr-fr)*v+30:.0f}" y2="{yy:.0f}" stroke="#f3e8d2"'
                  f' stroke-width="{3+3*v:.1f}" opacity=".30"/>')
        for i in range(22):
            u = i / 21.0
            s += (f'<line x1="{fl+(fr-fl)*u:.0f}" y1="{fy:.0f}"'
                  f' x2="{nl+(nr-nl)*u:.0f}" y2="{ny:.0f}" stroke="#4a3a2a"'
                  f' stroke-width="4" opacity=".26"/>')
        # прошитая кайма изнанки и заплата — ковёр, а не плоскость
        cx_ = (nl + nr + fl + fr) / 4.0; cy_ = (ny + fy) / 2.0
        for k_, wd, col_ in ((.955, 16, "#6d5a42"), (.90, 7, "#efe0c4")):
            pts = " ".join("%.0f,%.0f" % (cx_ + (px - cx_) * k_, cy_ + (py - cy_) * k_)
                           for px, py in ((nl, ny), (nr, ny), (fr, fy), (fl, fy)))
            s += (f'<polygon points="{pts}" fill="none" stroke="{col_}"'
                  f' stroke-width="{wd}" opacity=".75"/>')
        s += (f'<rect x="{cx_-150:.0f}" y="{cy_-46:.0f}" width="230" height="130" rx="10"'
              f' fill="#8d7757" opacity=".55" stroke="#5c4a34" stroke-width="6"'
              f' stroke-dasharray="16 12"/>')
    else:
        cx_ = (nl + nr + fl + fr) / 4.0; cy_ = (ny + fy) / 2.0
        for k, wd in ((.92, 11), (.82, 6)):
            pts = " ".join("%.0f,%.0f" % (cx_ + (px - cx_) * k, cy_ + (py - cy_) * k)
                           for px, py in ((nl, ny), (nr, ny), (fr, fy), (fl, fy)))
            s += f'<polygon points="{pts}" fill="none" stroke="{uzor}" stroke-width="{wd}" opacity=".8"/>'
        for r_ in range(5):
            v = (r_ + .5) / 5.0
            yy = fy + (ny - fy) * v
            hl = fl + (nl - fl) * v; hr = fr + (nr - fr) * v
            for c_ in range(9):
                u = (c_ + .5) / 9.0
                xx = hl + (hr - hl) * u
                rr = 22 + 30 * v
                col = uzor if (r_ + c_) % 2 == 0 else "#f0e2c2"
                s += (f'<polygon points="{xx:.0f},{yy-rr*.62:.0f} {xx+rr*.52:.0f},{yy:.0f}'
                      f' {xx:.0f},{yy+rr*.62:.0f} {xx-rr*.52:.0f},{yy:.0f}"'
                      f' fill="{col}" opacity=".85"/>')
                s += (f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{rr*.16:.0f}" fill="#7d2420" opacity=".7"/>')
    s += '</g>'
    return s


def _vedro(x, y, s_, t, dnom_vverh=False, tryapka=False, ph=0.0):
    """Оцинкованное ведро. Тряпка свешивается через край и покачивается."""
    s = ten(x, y + 10 * s_, 96 * s_, 20 * s_, .5)
    if dnom_vverh:
        s += (f'<path d="M{x-78*s_:.0f},{y:.0f} l{14*s_:.0f},{-150*s_:.0f}'
              f' h{128*s_:.0f} l{14*s_:.0f},{150*s_:.0f} z" fill="url(#zhel)" {o(7)}/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{y-150*s_:.0f}" rx="{64*s_:.0f}" ry="{17*s_:.0f}"'
              f' fill="#8a9099" {o(6)}/>')
        s += (f'<path d="M{x-56*s_:.0f},{y-20*s_:.0f} q{56*s_:.0f},{18*s_:.0f} {112*s_:.0f},0"'
              f' fill="none" stroke="#c7d0d8" stroke-width="{7*s_:.0f}" opacity=".6"/>')
    else:
        s += (f'<path d="M{x-92*s_:.0f},{y-170*s_:.0f} l{20*s_:.0f},{170*s_:.0f}'
              f' h{144*s_:.0f} l{20*s_:.0f},{-170*s_:.0f} z" fill="url(#zhel)" {o(7)}/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{y-170*s_:.0f}" rx="{92*s_:.0f}" ry="{24*s_:.0f}"'
              f' fill="#5f6a74" {o(6)}/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{y-170*s_:.0f}" rx="{72*s_:.0f}" ry="{16*s_:.0f}"'
              f' fill="#2c3740" opacity=".75"/>')
        s += (f'<path d="M{x-84*s_:.0f},{y-120*s_:.0f} q{84*s_:.0f},{26*s_:.0f} {168*s_:.0f},0"'
              f' fill="none" stroke="#cdd6de" stroke-width="{8*s_:.0f}" opacity=".55"/>')
        dug = 24 * s_ * A.w(t, 4.6, ph)
        s += (f'<path d="M{x-96*s_:.0f},{y-180*s_:.0f} q{96*s_+dug:.0f},{-120*s_:.0f} {192*s_:.0f},0"'
              f' fill="none" stroke="#7d868f" stroke-width="{9*s_:.0f}"/>')
    if tryapka:
        dx = 13 * s_ * A.w(t, 3.1, ph + .2)
        s += (f'<path d="M{x+36*s_:.0f},{y-186*s_:.0f} q{44*s_:.0f},{-16*s_:.0f} {72*s_:.0f},{10*s_:.0f}'
              f' q{10*s_+dx:.0f},{86*s_:.0f} {-16*s_+dx:.0f},{140*s_:.0f}'
              f' q{-30*s_:.0f},{10*s_:.0f} {-44*s_:.0f},{-14*s_:.0f}'
              f' q{14*s_:.0f},{-66*s_:.0f} {-12*s_:.0f},{-136*s_:.0f} z"'
              f' fill="#8fb0c4" {o(6)}/>')
        s += (f'<path d="M{x+50*s_:.0f},{y-120*s_:.0f} q{26*s_:.0f},{40*s_:.0f} {10*s_+dx:.0f},{96*s_:.0f}"'
              f' fill="none" stroke="#cfe1ec" stroke-width="{7*s_:.0f}" opacity=".7"/>')
    return s


def _shchetka(x, y, s_, ang=0.0):
    """Щётка на длинной ручке."""
    s = f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
    s += (f'<rect x="{x-11*s_:.0f}" y="{y-420*s_:.0f}" width="{22*s_:.0f}" height="{420*s_:.0f}"'
          f' rx="10" fill="url(#derev)" {o(5)}/>')
    s += (f'<rect x="{x-62*s_:.0f}" y="{y-46*s_:.0f}" width="{124*s_:.0f}" height="{36*s_:.0f}"'
          f' rx="8" fill="url(#derev)" {o(6)}/>')
    for i in range(9):
        xx = x - 54 * s_ + i * 13.5 * s_
        s += (f'<line x1="{xx:.0f}" y1="{y-12*s_:.0f}" x2="{xx:.0f}" y2="{y+30*s_:.0f}"'
              f' stroke="#b98a46" stroke-width="{6*s_:.0f}" stroke-linecap="round"/>')
    return s + '</g>'


def _medalon(cx, cy, r, t, gor=1.0, nutro=""):
    """Медальон в золотой рамке: загорается и держит картинку."""
    s = ""
    if gor > .02:
        s += teplo(cx, cy, r * 2.1, r * 2.1, .50 * gor)
    s += ten(cx, cy + r + 20, r * .82, 18, .42)
    s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#zol)" {o(8)}/>'
    s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.88:.0f}" fill="#2a2a33"'
          f' opacity="{1-.0*gor:.2f}"/>')
    s += _grad(f"b8m{int(cx)}", "#8a7350", "#4a3a28")
    s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.86:.0f}" fill="url(#b8m{int(cx)})"/>')
    s += f'<clipPath id="b8mc{int(cx)}"><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.86:.0f}"/></clipPath>'
    s += f'<g clip-path="url(#b8mc{int(cx)})" opacity="{.22+.78*gor:.2f}">{nutro}</g>'
    s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.86:.0f}" fill="none"'
          f' stroke="{ob.ZOLOTO2}" stroke-width="5" opacity=".8"/>')
    s += (f'<path d="M{cx-r*.72:.0f},{cy-r*.44:.0f} a{r*.84:.0f},{r*.84:.0f} 0 0 1 {r*.72:.0f},{-r*.42:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{r*.1:.0f}" opacity="{.24*gor:.2f}"/>')
    return s


def _tarelka(cx, cy, r, t, podyom=0.0, moneta=False):
    """Тарелка; при подъёме её край отходит и из-под него бьёт свет."""
    s = ""
    if podyom > .02:
        s += teplo(cx - r * .55, cy + r * .05, r * 1.35, r * .55, .50 + .40 * podyom)
        s += (f'<path d="M{cx-r*1.00:.0f},{cy+r*.06:.0f}'
              f' L{cx-r*1.75:.0f},{cy-r*(.10+.26*podyom):.0f}'
              f' L{cx-r*.30:.0f},{cy-r*(.16+.30*podyom):.0f}'
              f' L{cx+r*.26:.0f},{cy+r*.08:.0f} Z"'
              f' fill="{SVET}" opacity="{.34+.34*podyom:.2f}"/>')
        s += (f'<ellipse cx="{cx-r*.62:.0f}" cy="{cy+r*.02:.0f}" rx="{r*.52:.0f}"'
              f' ry="{r*.13*(1+podyom):.0f}" fill="#fff6d2" opacity="{.45*podyom:.2f}"/>')
    if moneta:
        bl = .45 + .55 * abs(A.w(t, 2.2))
        s += (f'<ellipse cx="{cx-r*.72:.0f}" cy="{cy+r*.20:.0f}" rx="{r*.22:.0f}"'
              f' ry="{r*.09:.0f}" fill="url(#zol)" {o(4)}/>')
        s += (f'<ellipse cx="{cx-r*.76:.0f}" cy="{cy+r*.18:.0f}" rx="{r*.09:.0f}"'
              f' ry="{r*.04:.0f}" fill="#fff0bd" opacity="{bl:.2f}"/>')
    s += ten(cx + 8, cy + r * .30, r * .92, r * .18, .45)
    ang = -11 * podyom
    s += f'<g transform="rotate({ang:.2f} {cx+r:.0f} {cy:.0f}) translate(0,{-r*.10*podyom:.0f})">'
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r:.0f}" ry="{r*.30:.0f}"'
          f' fill="url(#krem)" {o(6)}/>')
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy-r*.03:.0f}" rx="{r*.70:.0f}" ry="{r*.20:.0f}"'
          f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="{r*.035:.0f}" opacity=".8"/>')
    s += (f'<path d="M{cx-r*.76:.0f},{cy-r*.10:.0f} a{r*.8:.0f},{r*.28:.0f} 0 0 1 {r*.70:.0f},{-r*.09:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{r*.07:.0f}" opacity=".35"/>')
    return s + '</g>'


def _gazety(x, y, s_, t, ph=0.0):
    """Стопка пожелтевших газет, перевязанная бечёвкой; уголки шевелятся."""
    s = ten(x, y + 10 * s_, 108 * s_, 18 * s_, .45)
    for i in range(7):
        yy = y - i * 20 * s_
        dx = (i % 2 * 2 - 1) * 7 * s_
        s += (f'<rect x="{x-104*s_+dx:.0f}" y="{yy-22*s_:.0f}" width="{208*s_:.0f}"'
              f' height="{22*s_:.0f}" rx="4" fill="{"#e2d4ac" if i%2 else "#d5c494"}" {o(4)}/>')
        if i >= 4:
            ug = 11 * s_ * A.w(t, 2.3 + i * .4, ph + i * .17)
            s += (f'<path d="M{x+104*s_+dx:.0f},{yy-22*s_:.0f} q{26*s_:.0f},{-6*s_+ug:.0f}'
                  f' {34*s_:.0f},{14*s_+ug:.0f} l{-34*s_:.0f},{8*s_:.0f} z"'
                  f' fill="#efe3bd" {o(4)}/>')
    for k in range(4):
        yy = y - (146 - k * 13) * s_
        wd = (150 if k else 96) * s_
        s += (f'<path d="M{x-86*s_:.0f},{yy:.0f} h{wd:.0f}" fill="none"'
              f' stroke="#9a8c62" stroke-width="{4*s_:.1f}" opacity=".7"/>')
    s += (f'<path d="M{x-30*s_:.0f},{y+6*s_:.0f} v{-150*s_:.0f}" fill="none"'
          f' stroke="#b59a63" stroke-width="{9*s_:.0f}"/>')
    s += (f'<path d="M{x-104*s_:.0f},{y-74*s_:.0f} h{208*s_:.0f}" fill="none"'
          f' stroke="#b59a63" stroke-width="{9*s_:.0f}"/>')
    s += (f'<path d="M{x-44*s_:.0f},{y-82*s_:.0f} q{14*s_:.0f},{-18*s_:.0f} {28*s_:.0f},0"'
          f' fill="none" stroke="#b59a63" stroke-width="{7*s_:.0f}"/>')
    return s


def _zont(x, y, s_, t, spica=True, ph=0.0):
    """Сложенный зонт; одна спица торчит вбок и дрожит."""
    s = ten(x + 10 * s_, y + 8 * s_, 44 * s_, 12 * s_, .4)
    s += (f'<path d="M{x:.0f},{y:.0f} v{-300*s_:.0f}" fill="none" stroke="{CHUGUN}"'
          f' stroke-width="{13*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x-62*s_:.0f},{y-306*s_:.0f} q{62*s_:.0f},{-150*s_:.0f} {124*s_:.0f},0'
          f' q{-16*s_:.0f},{170*s_:.0f} {-62*s_:.0f},{196*s_:.0f}'
          f' q{-46*s_:.0f},{-24*s_:.0f} {-62*s_:.0f},{-196*s_:.0f} z"'
          f' fill="{ob.HVOYA}" {o(7)}/>')
    for k in range(3):
        s += (f'<path d="M{x-34*s_+k*34*s_:.0f},{y-298*s_:.0f}'
              f' q{14*s_:.0f},{150*s_:.0f} {6*s_:.0f},{186*s_:.0f}"'
              f' fill="none" stroke="{ob.HVOYA2}" stroke-width="{7*s_:.0f}" opacity=".75"/>')
    s += (f'<path d="M{x-48*s_:.0f},{y-280*s_:.0f} q{30*s_:.0f},{-54*s_:.0f} {58*s_:.0f},{-20*s_:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{9*s_:.0f}" opacity=".22"/>')
    s += (f'<path d="M{x:.0f},{y-420*s_:.0f} v{120*s_:.0f}" fill="none" stroke="{ZHELEZ}"'
          f' stroke-width="{10*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<path d="M{x:.0f},{y:.0f} q{-26*s_:.0f},{20*s_:.0f} {-40*s_:.0f},{-6*s_:.0f}"'
          f' fill="none" stroke="{CHUGUN}" stroke-width="{13*s_:.0f}" stroke-linecap="round"/>')
    if spica:
        dr = 5.6 * A.w(t, .55, ph) + 2.4 * A.w(t, .17, ph * 2)
        s += (f'<g transform="rotate({dr:.2f} {x+34*s_:.0f} {y-256*s_:.0f})">'
              f'<path d="M{x+34*s_:.0f},{y-256*s_:.0f} l{186*s_:.0f},{-52*s_:.0f}"'
              f' fill="none" stroke="{K}" stroke-width="{15*s_:.0f}" stroke-linecap="round"/>'
              f'<path d="M{x+34*s_:.0f},{y-256*s_:.0f} l{186*s_:.0f},{-52*s_:.0f}"'
              f' fill="none" stroke="#c8d2dc" stroke-width="{8*s_:.0f}" stroke-linecap="round"/>'
              f'<circle cx="{x+220*s_:.0f}" cy="{y-308*s_:.0f}" r="{11*s_:.0f}" fill="#c8d2dc" {o(4)}/></g>')
    return s


def _chashka(x, y, s_, t, ph=0.0, ruchka_ryadom=True):
    """Чашка без ручки — ручка лежит рядом; чашка покачивается."""
    kach = 3.4 * A.w(t, 2.7, ph)
    s = ten(x + 6 * s_, y + 8 * s_, 70 * s_, 14 * s_, .45)
    s += f'<g transform="rotate({kach:.2f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x-62*s_:.0f},{y-128*s_:.0f} q{10*s_:.0f},{128*s_:.0f} {62*s_:.0f},{128*s_:.0f}'
          f' q{52*s_:.0f},0 {62*s_:.0f},{-128*s_:.0f} z" fill="url(#krem)" {o(7)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-128*s_:.0f}" rx="{62*s_:.0f}" ry="{19*s_:.0f}"'
          f' fill="#cfc0a1" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-128*s_:.0f}" rx="{48*s_:.0f}" ry="{13*s_:.0f}"'
          f' fill="#8f8572" opacity=".65"/>')
    s += (f'<path d="M{x-58*s_:.0f},{y-104*s_:.0f} q{58*s_:.0f},{18*s_:.0f} {116*s_:.0f},0"'
          f' fill="none" stroke="{ob.ALYJ}" stroke-width="{8*s_:.0f}" opacity=".75"/>')
    s += (f'<path d="M{x+36*s_:.0f},{y-116*s_:.0f} q{14*s_:.0f},{54*s_:.0f} {2*s_:.0f},{96*s_:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="{9*s_:.0f}" opacity=".3"/>')
    s += (f'<path d="M{x+56*s_:.0f},{y-110*s_:.0f} q{10*s_:.0f},{4*s_:.0f} {12*s_:.0f},{14*s_:.0f}"'
          f' fill="none" stroke="#8f8572" stroke-width="{6*s_:.0f}"/>')
    s += '</g>'
    if ruchka_ryadom:
        hx, hy = x + 162 * s_, y - 12 * s_
        s += ten(hx, y + 8 * s_, 64 * s_, 12 * s_, .4)
        # ушко ручки: наружная и внутренняя дуги одним контуром
        s += (f'<path d="M{hx-56*s_:.0f},{hy+30*s_:.0f}'
              f' a{62*s_:.0f},{58*s_:.0f} 0 1 1 {112*s_:.0f},0'
              f' l{-26*s_:.0f},{4*s_:.0f}'
              f' a{38*s_:.0f},{36*s_:.0f} 0 1 0 {-60*s_:.0f},0 z"'
              f' fill="#e4d6b8" {o(max(4, 6*s_))}/>')
        s += (f'<path d="M{hx-44*s_:.0f},{hy+6*s_:.0f}'
              f' a{50*s_:.0f},{48*s_:.0f} 0 0 1 {34*s_:.0f},{-40*s_:.0f}"'
              f' fill="none" stroke="#ffffff" stroke-width="{8*s_:.0f}" opacity=".45"/>')
        s += (f'<path d="M{hx-56*s_:.0f},{hy+30*s_:.0f} l{14*s_:.0f},{10*s_:.0f}'
              f' M{hx+56*s_:.0f},{hy+30*s_:.0f} l{-14*s_:.0f},{10*s_:.0f}"'
              f' fill="none" stroke="#b5a582" stroke-width="{6*s_:.0f}"/>')
    return s


def _stul(x, y, s_, ang=0.0):
    s = f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
    s += ten(x, y + 8 * s_, 60 * s_, 12 * s_, .4)
    s += (f'<rect x="{x-56*s_:.0f}" y="{y-120*s_:.0f}" width="{112*s_:.0f}" height="{22*s_:.0f}"'
          f' rx="8" fill="url(#derev)" {o(5)}/>')
    s += (f'<rect x="{x-48*s_:.0f}" y="{y-300*s_:.0f}" width="{18*s_:.0f}" height="{190*s_:.0f}"'
          f' rx="7" fill="url(#derev)" {o(4)}/>')
    s += (f'<rect x="{x-48*s_:.0f}" y="{y-280*s_:.0f}" width="{96*s_:.0f}" height="{18*s_:.0f}"'
          f' rx="7" fill="url(#derev)" {o(4)}/>')
    for dx in (-46, 40):
        s += (f'<rect x="{x+dx*s_:.0f}" y="{y-100*s_:.0f}" width="{14*s_:.0f}"'
              f' height="{100*s_:.0f}" fill="url(#derev)" {o(4)}/>')
    return s + '</g>'


def _blyudo_pelmeni(cx, cy, s_, t, ph=0.0, par_on=True):
    """Блюдо пельменей: горка, пар, золотой ободок."""
    s = ten(cx + 6 * s_, cy + 22 * s_, 150 * s_, 26 * s_, .45)
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{156*s_:.0f}" ry="{48*s_:.0f}"'
          f' fill="url(#krem)" {o(6)}/>')
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy-4*s_:.0f}" rx="{126*s_:.0f}" ry="{36*s_:.0f}"'
          f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="{6*s_:.0f}" opacity=".8"/>')
    r = random.Random(21)
    for i in range(13):
        a = r.uniform(0, 6.28)
        rr = r.uniform(0, 1) ** .5
        px = cx + math.cos(a) * 104 * s_ * rr
        py = cy - 16 * s_ - abs(math.sin(a)) * 16 * s_ * rr - r.uniform(0, 26) * s_
        s += (f'<path d="M{px-30*s_:.0f},{py:.0f} q{30*s_:.0f},{-34*s_:.0f} {60*s_:.0f},0'
              f' q{-30*s_:.0f},{18*s_:.0f} {-60*s_:.0f},0 z" fill="#f2e6cc" {o(4)}/>')
        s += (f'<path d="M{px-18*s_:.0f},{py-10*s_:.0f} q{18*s_:.0f},{-10*s_:.0f} {36*s_:.0f},0"'
              f' fill="none" stroke="#ffffff" stroke-width="{4*s_:.0f}" opacity=".6"/>')
    if par_on:
        s += baza.par(cx - 40 * s_, cy - 54 * s_, t + ph, 4, .45, 170 * s_, .45, s_)
        s += baza.par(cx + 46 * s_, cy - 48 * s_, t + ph + .7, 4, .4, 150 * s_, .42, s_)
    return s


def _struyka(x, y, t, L=420, ph=0.0, col=None, op=.8):
    """Оранжевая струйка запаха — волна, которая плывёт вверх."""
    c = col or ob.MANDA
    d = f'M{x:.0f},{y:.0f}'
    for i in range(1, 13):
        u = i / 12.0
        yy = y - L * u
        xx = x + 34 * u * math.sin(2 * math.pi * (u * 1.3 - t * .32 + ph))
        d += f' L{xx:.0f},{yy:.0f}'
    s = (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="13"'
         f' stroke-linecap="round" opacity="{op*.55:.2f}"/>')
    s += (f'<path d="{d}" fill="none" stroke="{SVET}" stroke-width="5"'
          f' stroke-linecap="round" opacity="{op*.5:.2f}"/>')
    return s


def _proyom(x, y, w_, h_, t, sila=1.0):
    """Светящийся дверной проём: из него льётся тёплый свет на пол."""
    s = _grad("b8pro", "#fff6d8", "#efba55")
    s += teplo(x + w_ / 2, y + h_ * .42, w_ * 2.0, h_ * 1.05, .75 * sila)
    s += (f'<rect x="{x-22:.0f}" y="{y-24:.0f}" width="{w_+44:.0f}" height="{h_+28:.0f}"'
          f' rx="12" fill="url(#derev)" {o(8)}/>')
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="url(#b8pro)"/>'
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="{SVET}"'
          f' opacity="{.14+.10*abs(A.w(t,2.6)):.2f}"/>')
    # глубина проёма: притолока в тени, косяки темнее, светлее к полу
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_*.30:.0f}"'
          f' fill="#8a5a1e" opacity=".34"/>')
    for sgn, xx in ((1, x), (-1, x + w_)):
        s += (f'<rect x="{xx if sgn>0 else xx-54:.0f}" y="{y:.0f}" width="54"'
              f' height="{h_:.0f}" fill="#a87324" opacity=".26"/>')
    s += (f'<ellipse cx="{x+w_/2:.0f}" cy="{y+h_*.86:.0f}" rx="{w_*.44:.0f}"'
          f' ry="{h_*.20:.0f}" fill="#ffffff" opacity=".30"/>')
    # ПОРОГ: проём стоит на полу, а не висит прямоугольником
    s += (f'<rect x="{x-26:.0f}" y="{y+h_-10:.0f}" width="{w_+52:.0f}" height="30"'
          f' rx="9" fill="url(#med)" {o(7)}/>')
    s += (f'<path d="M{x:.0f},{y+h_:.0f} L{x-300:.0f},{H+40} L{x+w_+340:.0f},{H+40}'
          f' L{x+w_:.0f},{y+h_:.0f} Z" fill="{SVET}" opacity="{.22*sila:.2f}"/>')
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="none" {o(8)}/>'
    return s


def _meshok(x, y, s_, t, ph=0.0, szhat=0.0):
    """Огромный мешок старья: зонт и газеты торчат из горловины."""
    sx = 1.0 - .13 * szhat
    s = ten(x, y + 12 * s_, 210 * s_, 32 * s_, .5)
    s += f'<g transform="translate({x:.0f},{y:.0f}) scale({s_*sx:.3f},{s_:.3f})">'
    s += (f'<path d="M-196,0 q-34,-212 36,-318 q58,-46 136,-46 q96,0 150,56'
          f' q68,104 40,308 z" fill="url(#solom)" {o(9)}/>')
    s += (f'<path d="M-150,-54 q140,34 286,-10" fill="none" stroke="#a07c2e"'
          f' stroke-width="12" opacity=".6"/>')
    s += (f'<path d="M-120,-200 q114,38 236,-14" fill="none" stroke="#a07c2e"'
          f' stroke-width="10" opacity=".45"/>')
    s += (f'<path d="M-114,-330 q110,-44 218,6 q-30,46 -108,46 q-80,0 -110,-52 z"'
          f' fill="#c9ad72" {o(7)}/>')
    s += (f'<path d="M-100,-336 q104,-40 198,4" fill="none" stroke="#8a6d33"'
          f' stroke-width="12" stroke-dasharray="14 12"/>')
    # ВЕРЁВКА с узлом на горловине
    s += (f'<path d="M-118,-290 q112,52 224,-8" fill="none" stroke="#7d5f28"'
          f' stroke-width="19" stroke-linecap="round"/>')
    s += (f'<path d="M-118,-282 q112,52 224,-8" fill="none" stroke="#c0a055"'
          f' stroke-width="8" stroke-linecap="round" opacity=".8"/>')
    s += (f'<path d="M96,-298 q34,-14 42,16 q-26,22 -48,8 z" fill="#7d5f28" {o(5)}/>'
          f'<path d="M126,-278 q24,44 6,86" fill="none" stroke="#7d5f28"'
          f' stroke-width="11" stroke-linecap="round"/>')
    # углы содержимого распирают бок — мешок, а не гладкий купол
    for lx_, ly_, rr_ in ((-132, -176, 52), (108, -222, 44), (-52, -96, 58), (74, -84, 40)):
        s += (f'<ellipse cx="{lx_}" cy="{ly_}" rx="{rr_}" ry="{rr_*.78:.0f}"'
              f' fill="#b99a5e" opacity=".32"/>')
        s += (f'<path d="M{lx_-rr_},{ly_+rr_*.3:.0f} q{rr_},{-rr_*.9:.0f} {rr_*2},0"'
              f' fill="none" stroke="#8a6d33" stroke-width="7" opacity=".45"/>')
    s += f'<path d="M-160,-250 q50,-70 70,-110" fill="none" stroke="#ffffff" stroke-width="16" opacity=".16"/>'
    s += '</g>'
    s += _zont(x + 66 * s_, y - 316 * s_, s_ * .86, t, True, ph)
    s += (f'<g transform="translate({x-120*s_:.0f},{y-336*s_:.0f}) rotate(-24)">'
          + _gazety(0, 0, s_ * .72, t, ph + .3) + '</g>')
    return s


def _figury_vokrug(cx, cy, rx, ry, t, n=6, h0=250, seed=3, krasnyh=(0, 3)):
    """Родные вокруг круглого стола: дальние мельче, ближние крупнее."""
    r = random.Random(seed)
    out = []
    for i in range(n):
        a = math.pi * (.08 + .84 * (i + .5) / n) + math.pi
        x = cx + math.cos(a) * rx * 1.02
        y = cy + math.sin(a) * ry * 1.02
        k = .72 + .5 * (y - (cy - ry)) / (2 * ry + 1)
        out.append((y, x, k, i))
    out.sort()
    s = ""
    for y, x, k, i in out:
        s += ob.figura(x, y + 96 * k, h0 * k, t,
                       col=("#2e2330", "#243040", "#33262c")[i % 3],
                       kant="#f0c070", platok=(i % 3 == 1), ph=i * .19,
                       krasnoe=(i in krasnyh))
    return s


# ═══════════════════ 158 ═══════════════════

def sem_karmashkov_do_prazdnika(t):
    """Морозное утро, стена с полотняным календарём из семи кармашков-дней.
    Живое: записки выглядывают, солнечный зайчик ползёт, красный кармашек мерцает."""
    vid = (baza._nebo("den", t, zvezdy=False)
           + baza._oblaka(t, 240, 3, 9, .55, "#ffffff", 5.0)
           + baza._sneg_letit(t, 18, 8, .45, .5))
    for i, (ex, eh) in enumerate(((1430, 150), (1560, 196), (1690, 126))):
        vid += (f'<path d="M{ex:.0f},470 l{-eh*.34:.0f},0 l{eh*.34:.0f},{-eh:.0f}'
                f' l{eh*.34:.0f},{eh:.0f} z" fill="#56687d" opacity=".75"/>')
    zx = 170 + 880 * ((t * .055) % 1.0)

    s = SL(Z_DAL,
           _komnata(820, "#8a7158", "#63513a")
           + baza.doski(0, 0, W, 820, 118, False, "dosk")
           + f'<rect width="{W}" height="820" fill="#f2e2c4" opacity=".15"/>'
           + baza.okno_izby(1390, 150, 440, 360, t, vid=vid, moroz=.09, svet=True)
           + teplo(1610, 330, 640, 540, .62)
           + teplo(zx, 500, 260, 210, .40)
           + f'<ellipse cx="{zx:.0f}" cy="500" rx="140" ry="104" fill="{SVET}" opacity=".20"/>')

    s += SL(Z_SRED,
            _kalendar(130, 430, t, 1160, zapiski=3, goryat=(), n=7, h_=320)
            + baza.luch(1280, 250, 250, 740, t, .20))

    s += baza.mebel_hlam(40, 1010, 560, t, 13)

    s += SL(Z_PERED,
            baza._ramka_pp("levo", "#120e0a", .72)
            + baza.lavka(1240, 940, 520)
            + baza.krynka(1360, 930, .9)
            + ob.mandarin(1530, 900, .9, 0.0, t)
            + ob.mandarin(1620, 916, .78, 0.0, t))
    s += baza.vinetka(.40)
    return s


# ═══════════════════ 159, 161 ═══════════════════

def listok_s_dolgami(t):
    """Стол, тетрадный листок, карандаш пишет три строчки и ставит значки.
    Живое: карандаш пишет, значки появляются, листок чуть сдвигается."""
    rost = [A.ease(A.seg(t, .25 + i * 1.05, .85)) for i in range(3)]
    sdv = 5 * A.w(t, 6.4)
    lx, ly, lw, lh = 250, 290, 620, 730

    s = SL(Z_DAL,
           _komnata(360, "#5c4b3c", "#3b3025")
           + baza.vozduh(520, 220, t, 940, .34)
           + baza.lampa(430, 180, t, .95, abazhur=True)
           + baza.polka(1130, 180, 690)
           + baza.krynka(1240, 176, .7) + baza.krynka(1710, 176, .62)
           + ob.mandarin(1430, 150, .66, 0.0, t))

    stol = (f'<rect y="360" width="{W}" height="{H-360}" fill="url(#derev)"/>'
            + f'<rect y="352" width="{W}" height="24" fill="{DOSKA2}" {o(6)}/>')
    for i in range(10):
        stol += (f'<line x1="0" y1="{430+i*74}" x2="{W}" y2="{430+i*74}"'
                 f' stroke="#5a3b22" stroke-width="4" opacity=".4"/>')
    s += SL(Z_SRED, stol + teplo(620, 640, 920, 520, .42))

    # значки у строчек: монета, книга, трубка
    zn = ""
    for i in range(3):
        u = A.over(A.seg(t, 1.0 + i * 1.05, .45))
        if u <= .02:
            continue
        zx, zy = lx + lw + 330, ly + lh * (.275 + i * .23) - 4
        zn += f'<g transform="translate({zx:.0f},{zy:.0f}) scale({u*1.75:.3f})">'
        zn += f'<circle r="64" fill="{SVET}" opacity=".12"/>'
        if i == 0:
            bl = .4 + .6 * abs(A.w(t, 2.3))
            zn += f'<circle r="46" fill="url(#zol)" {o(7)}/>'
            zn += f'<circle r="30" fill="none" stroke="{ob.ZOLOTO2}" stroke-width="6"/>'
            zn += f'<circle cx="-15" cy="-15" r="13" fill="#fff0bd" opacity="{bl:.2f}"/>'
        elif i == 1:
            zn += f'<rect x="-48" y="-38" width="96" height="78" rx="8" fill="{ob.ALYJ}" {o(7)}/>'
            zn += f'<rect x="-34" y="-30" width="74" height="62" rx="5" fill="url(#list)" {o(5)}/>'
            zn += f'<path d="M3,-30 v62" fill="none" {o(6)}/>'
            zn += f'<path d="M-22,-14 h22 M-22,2 h22 M8,-14 h22 M8,2 h22" stroke="#8f8572" stroke-width="4"/>'
        else:
            zn += (f'<path d="M-52,26 q-18,-38 12,-54 q20,-9 27,11 q-14,7 -9,20'
                   f' q27,27 61,18 q7,-14 23,-7 q18,11 7,32 q-45,25 -121,-20 z"'
                   f' fill="{CHUGUN}" {o(7)}/>')
            zn += f'<path d="M-34,-20 q7,-11 18,-7" fill="none" stroke="#9aa3ac" stroke-width="7"/>'
            zn += f'<path d="M34,16 q10,-9 20,-3" fill="none" stroke="#9aa3ac" stroke-width="7"/>'
        zn += '</g>'

    # карандаш: остриё стоит на конце текущей строчки
    akt = 0
    for i in range(3):
        if rost[i] > .01:
            akt = i
    px = lx + lw * .21 + lw * .60 * rost[akt]
    py = ly + lh * (.275 + akt * .23) + 6

    s += SL(Z_PERED,
            _listok(lx + sdv, ly, lw, lh, t, rost=rost, ang=-3.4, svet=.0)
            + zn
            + _karandash(px + sdv, py, -29, 360)
            + baza._ramka_pp("levo", "#140f0b", .55))
    s += baza.vinetka(.46)
    return s


# ═══════════════════ 160 ═══════════════════

def tri_nevypolnennyh_obeschaniya(t):
    """Три вещи ждут своей очереди: телефон с диском, чужая дверь с ковриком,
    открытка с недописанным рецептом. Живое: диск крутится, свет под дверью
    дышит, ручка дописывает строку."""
    s = SL(Z_DAL,
           _komnata(700, "#5a4a3e", "#372c24")
           + baza.vozduh(960, 300, t, 1000, .30)
           + f'<rect y="700" width="{W}" height="{H-700}" fill="url(#derev)" opacity=".9"/>')

    # тумбы под тремя вещами
    tum = ""
    for cx in (330, 1590):
        tum += ten(cx, 952, 250, 24, .45)
        tum += (f'<rect x="{cx-240:.0f}" y="770" width="480" height="180" rx="12"'
                f' fill="url(#derev)" {o(7)}/>')
        tum += (f'<rect x="{cx-220:.0f}" y="790" width="440" height="20" rx="8"'
                f' fill="#ffffff" opacity=".12"/>')
    s += SL(Z_SRED, tum)

    # ── телефон с диском
    p = (t / 1.7) % 1.0
    ang = 300 * A.ease(min(1.0, p * 2.3)) if p < .44 else 300 * (1 - A.ease((p - .44) / .56))
    tel = ten(370, 784, 240, 24, .45)
    tel += teplo(370, 650, 440, 380, .34)
    tel += f'<path d="M170,774 q0,-170 200,-170 q200,0 200,170 z" fill="url(#chug)" {o(8)}/>'
    tel += f'<path d="M206,652 q164,-76 328,0" fill="none" stroke="#5d5956" stroke-width="16"/>'
    tel += f'<circle cx="370" cy="638" r="104" fill="#ded6c6" {o(7)}/>'
    tel += f'<g transform="rotate({ang:.1f} 370 638)">'
    for i in range(10):
        a = -1.9 + i * .62
        tel += (f'<circle cx="{370+math.cos(a)*72:.0f}" cy="{638+math.sin(a)*72:.0f}"'
                f' r="17" fill="#3a3733" opacity=".85"/>')
    tel += f'<circle cx="370" cy="638" r="28" fill="#a79e92" {o(5)}/></g>'
    tel += f'<circle cx="370" cy="638" r="104" fill="none" {o(7)}/>'
    tel += (f'<path d="M288,586 a104,104 0 0 1 78,-50" fill="none" stroke="#ffffff"'
            f' stroke-width="14" opacity=".35"/>')
    # снятая трубка лежит рядом, шнур спиралью
    tel += f'<g transform="translate(252,786) rotate(-10) scale(1.3)">'
    tel += ten(60, 14, 100, 14, .4)
    tel += (f'<path d="M-52,0 q-20,-32 6,-44 q18,-8 24,10 l92,-10 q6,-18 24,-10'
            f' q26,12 6,44 q-78,24 -152,10 z" fill="{CHUGUN}" {o(6)}/>')
    tel += (f'<path d="M-30,-22 q66,16 128,-6" fill="none" stroke="#8b9199"'
            f' stroke-width="7" opacity=".6"/>')
    tel += '</g>'
    sh = f'M316,758'
    for i in range(9):
        sh += f' q16,{20 if i % 2 == 0 else -20} 32,0'
    tel += f'<path d="{sh}" fill="none" stroke="#2b2724" stroke-width="11" opacity=".9"/>'

    # ── чужая дверь с ковриком
    svs = .35 + .35 * abs(A.w(t, 2.9))
    dv = (f'<rect x="724" y="258" width="472" height="520" rx="6" fill="#4a3728" {o(7)}/>'
          + f'<rect x="748" y="282" width="424" height="496" rx="4" fill="#2a1f16" {o(5)}/>'
          + f'<rect x="760" y="296" width="400" height="482" rx="4" fill="#1d2129"/>'
          + baza.dver(770, 310, 380, 456, 0.0, "url(#derev)", True, False)
          + f'<rect x="716" y="770" width="488" height="22" rx="8" fill="{MED}" {o(6)}/>')
    dv += (f'<rect x="770" y="752" width="380" height="16" fill="{SVET}"'
           f' opacity="{svs:.2f}"/>')
    dv += teplo(960, 770, 320, 110, svs * .85)
    ug = 11 * A.w(t, 3.6)
    dv += ten(960, 828, 240, 20, .45)
    dv += (f'<path d="M760,778 h400 l{-42+ug:.0f},74 h{-316-ug*2:.0f} z"'
           f' fill="#a3875f" {o(7)}/>')
    for i in range(7):
        dv += (f'<path d="M{792+i*60:.0f},786 l-10,60" fill="none" stroke="#6d5736"'
               f' stroke-width="8" opacity=".85"/>')
    dv += f'<path d="M776,794 h368" fill="none" stroke="#d6bd8c" stroke-width="7" opacity=".7"/>'

    # ── открытка с недописанным рецептом
    rost = A.ease(A.seg(t, 1.1, 2.4))
    otk = ""
    ox, oy, ow, oh = 1380, 470, 420, 300
    otk += ten(1600, 786, 220, 18, .42)
    otk += f'<g transform="rotate(-5 {ox+ow/2:.0f} {oy+oh/2:.0f})">'
    otk += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="9" fill="url(#list)" {o(6)}/>'
    otk += (f'<rect x="{ox}" y="{oy}" width="{ow}" height="54" rx="9" fill="{ob.ALYJ}" opacity=".85"/>')
    otk += (f'<path d="M{ox+18},{oy+30} q{ow*.2:.0f},-26 {ow*.4:.0f},0" fill="none"'
            f' stroke="{ob.ZOLOTO}" stroke-width="7" opacity=".9"/>')
    for i in range(4):
        yy = oy + 100 + i * 46
        w2 = ow * .72 if i < 3 else ow * .72 * rost
        otk += (f'<path d="M{ox+36},{yy} h{w2:.0f}" fill="none" stroke="#3b342f"'
                f' stroke-width="7" stroke-linecap="round" opacity=".85"/>')
    otk += f'<path d="M{ox+12},{oy+70} l{ow*.3:.0f},{oh*.3:.0f}" stroke="#ffffff" stroke-width="14" opacity=".2"/>'
    otk += '</g>'
    otk += _ruchka(ox + 36 + ow * .72 * rost + 22, oy + 244, -34, 250)

    s += SL(Z_PERED, tel + dv + otk + baza._ramka_pp("oba", "#120e0a", .6))
    s += baza.vinetka(.45)
    return s


# ═══════════════════ 162 ═══════════════════

def vedro_tryapka_i_dva_dnya(t):
    """Комната: ведро с отжатой тряпкой и щётка, на стене загораются два дня.
    Живое: числа загораются, тряпка свешивается, щётка падает и встаёт."""
    p = (t / 3.6) % 1.0
    if p < .30:
        ang = 0.0
    elif p < .52:
        ang = -74 * A.ease((p - .30) / .22)
    elif p < .66:
        ang = -74
    else:
        ang = -74 * (1 - A.ease((p - .66) / .34))

    s = SL(Z_DAL,
           _komnata(760, "#6b5846", "#473828")
           + baza.vozduh(760, 420, t, 980, .32)
           + _kalendar(170, 130, t, 1120, zapiski=0, goryat=(4, 5), n=7, h_=280))

    s += baza.mebel_hlam(1390, 1020, 520, t, 9)
    # тёплая лампа и полотенце на гвозде: кадр был пустой бурой стеной
    s += SL(Z_DAL,
            baza.lampa(1660, 420, t, .78, True)
            + f'<rect x="300" y="520" width="28" height="18" rx="6" fill="{ZHELEZ}" {o(4)}/>'
            + f'<path d="M258,534 q58,-26 114,0 q18,150 -12,250 q-54,20 -94,-4'
              f' q-28,-98 -8,-246 z" fill="{ob.ALYJ}" {o(6)}/>'
            + f'<path d="M266,660 h100 M266,706 h100" stroke="{ob.ZOLOTO}"'
              f' stroke-width="8" opacity=".85"/>'
            + baza.teplo(1660, 470, 420, 380, .46))

    s += SL(Z_SRED,
            teplo(840, 890, 780, 420, .40)
            + _vedro(700, 1000, 1.42, t, False, True)
            + _shchetka(1180, 1006, 1.30, ang))

    luzha = (f'<ellipse cx="930" cy="1026" rx="380" ry="50" fill="#9fc4d8" opacity=".30"/>'
             f'<ellipse cx="860" cy="1020" rx="210" ry="28" fill="#dff0fa" opacity=".24"/>')
    s += SL(Z_PERED,
            luzha
            + baza._ramka_pp("levo", "#120e0a", .55))
    s += baza.vinetka(.44)
    return s


# ═══════════════════ 163 ═══════════════════

def kover_na_chistom_snegu(t):
    """Двор пятиэтажки: большой узорный ковёр узором вниз на снегу, его метут
    вдвоём и поднимают. Живое: веник метёт, ковёр поднимают, остаётся серый след."""
    pod = A.ease(A.seg(t, 2.9, 1.5))            # подъём ковра
    met = A.seg(t, .1, 2.7)
    vx = 560 + 620 * (.5 + .5 * A.w(t, 1.5)) * (1 - pod)

    s = baza.nebo("den", t, zvezdy=False)
    s += baza.oblaka(t, 180, 4, 9, .5, "#f2f6fb", 7.0)
    s += SL(Z_DAL,
            baza._panelka(60, 690, 760, t, 5, True, 4)
            + baza._panelka(1180, 690, 640, t, 5, True, 9)
            + baza._ulica_dal(820, 690, 380, t, True, 5)
            + baza._sneg_lezhit(690, 30))
    s += SL(Z_SRED,
            f'<rect y="700" width="{W}" height="{H-700}" fill="url(#sneg)"/>'
            + f'<path d="M0,760 q480,-34 960,-10 q480,24 960,-14 L1920,{H} L0,{H} Z"'
              f' fill="#ffffff" opacity=".55"/>')

    # серый прямоугольник остаётся на снегу
    sled = (f'<path d="M430,1010 L1490,1010 L1300,742 L620,742 Z" fill="#8fa0b4"'
            f' opacity="{.22+.78*pod:.2f}" stroke="#6f8096" stroke-width="6"/>'
            f'<path d="M470,990 L1450,990 L1290,762 L630,762 Z" fill="#7b8da4"'
            f' opacity="{.16+.58*pod:.2f}"/>')

    # ковёр изнанкой вверх, поднимается за углы
    bahroma = ""
    for i in range(26):
        u = i / 25.0
        bx = 420 + 1080 * u
        bahroma += (f'<path d="M{bx:.0f},1012 l{-4+8*((i%2)):.0f},26" fill="none"'
                    f' stroke="#8d7f63" stroke-width="5" stroke-linecap="round"/>')
    kov = (f'<g transform="translate(0,{-290*pod:.0f}) scale(1,{1-.46*pod:.3f})'
           f' rotate({-4.5*pod:.2f})" transform-origin="960 1010">'
           + _kover("b8kv1", 420, 1500, 1012, 614, 1306, 740, t,
                    "#b9a687", "#85715a",
                    "#9c8a66", .9, iznanka=True)
           + bahroma
           + f'<path d="M470,990 L1450,990 L1292,762 L628,762 Z" fill="none"'
             f' stroke="#8d7f63" stroke-width="9" opacity=".7"/>'
           + '</g>')

    # веник метёт по ковру, пока его не подняли
    venik = ""
    if met > .01 and pod < .5:
        venik += f'<g transform="translate({vx:.0f},{900 - 220*pod:.0f}) rotate({-22+10*A.w(t,1.5):.1f})">'
        venik += (f'<rect x="-10" y="-330" width="21" height="330" rx="9"'
                  f' fill="url(#derev)" {o(5)}/>')
        for i in range(11):
            venik += (f'<path d="M{-2+i*2:.0f},-24 q{-46+i*9:.0f},50 {-54+i*11:.0f},96"'
                      f' fill="none" stroke="#c6a152" stroke-width="7" stroke-linecap="round"/>')
        venik += f'<rect x="-30" y="-46" width="62" height="24" rx="8" fill="{ob.ALYJ}" {o(4)}/>'
        venik += '</g>'
        venik += (f'<ellipse cx="{vx:.0f}" cy="{916-220*pod:.0f}" rx="130" ry="26"'
                  f' fill="#ffffff" opacity="{.22*(1-pod):.2f}"/>')

    # отец и сын держат ковёр за углы
    ded = ob.figura(330, 1046, 430, t, col="#2b2430", kant="#cfe0f2", ph=.0)
    syn = ob.figura(1620, 1030, 270, t, col="#32242a", kant="#cfe0f2", ph=.4, krasnoe=True)

    s += SL(Z_SRED, sled + kov + venik + ded + syn)
    s += SL(Z_PERED,
            baza._sneg_lezhit(1004, 44)
            + baza._ramka_pp("oba", "#1a2232", .5))
    s += baza.sneg_letit(t, 46, 5, .72)
    s += baza.vinetka(.40)
    return s


# ═══════════════════ 164 ═══════════════════

def pylesos_na_kovre(t):
    """Комната: пылесос идёт по узорному ковру и оставляет яркую чистую полосу.
    Живое: щётка идёт, узор яснеет полосой, шнур тянется."""
    u = (t / 3.4) % 1.0
    xb = 300 + 1200 * A.ease(u)

    s = SL(Z_DAL,
           _komnata(600, "#64533f", "#3f3326")
           + baza.vozduh(960, 280, t, 980, .28)
           + baza.kvartira_veschi(40, 600, 700, t, 11)
           + _kalendar(1060, 130, t, 760, zapiski=0, goryat=(4, 5), n=7, h_=270))

    pol = (f'<rect y="600" width="{W}" height="{H-600}" fill="url(#pol)"/>')
    for i in range(9):
        pol += (f'<line x1="0" y1="{650+i*56}" x2="{W}" y2="{650+i*56}"'
                f' stroke="#4e3220" stroke-width="4" opacity=".45"/>')

    kov_tus = _kover("b8kv2", 120, 1820, 1070, 410, 1540, 620, t,
                     "#6d3b35", "#3f1f1e", "#9d8552", .55)
    kov_yar = _kover("b8kv3", 120, 1820, 1070, 410, 1540, 620, t,
                     "#b04a3c", "#6b2724", "#f0c766", 1.0)
    polosa = (f'<clipPath id="b8pol"><rect x="80" y="580" width="{max(0,xb-80):.0f}"'
              f' height="520"/></clipPath>'
              f'<g clip-path="url(#b8pol)">{kov_yar}</g>')

    s += SL(Z_SRED, pol + kov_tus + polosa
            + f'<rect x="{xb-14:.0f}" y="600" width="16" height="470" fill="{SVET}" opacity=".24"/>'
            + teplo(xb, 880, 280, 220, .28))

    # шнур тянется от пылесоса к левому краю
    shn = f'M{xb-70:.0f},940'
    for i in range(9):
        shn += f' Q{xb-70-(i+.5)*(xb+120)/9:.0f},{958+26*A.w(t,3.0,i*.2):.0f} {xb-70-(i+1)*(xb+120)/9:.0f},944'
    pyl = f'<path d="{shn}" fill="none" stroke="#2c2a28" stroke-width="10"/>'

    # корпус, шланг, щётка
    bx = xb - 300
    pyl += ten(bx, 1020, 150, 24, .45)
    pyl += (f'<path d="M{bx-140:.0f},1012 q-16,-150 60,-176 q80,-26 160,-2'
            f' q70,26 56,178 z" fill="url(#zhel)" {o(8)}/>')
    pyl += (f'<ellipse cx="{bx-10:.0f}" cy="866" rx="92" ry="34" fill="#5f6a74" {o(5)}/>')
    pyl += (f'<path d="M{bx-120:.0f},930 q110,30 230,-6" fill="none" stroke="#ffffff"'
            f' stroke-width="12" opacity=".2"/>')
    for dx in (-110, 110):
        pyl += (f'<circle cx="{bx+dx:.0f}" cy="1012" r="34" fill="url(#chug)" {o(5)}/>'
                f'<circle cx="{bx+dx:.0f}" cy="1012" r="13" fill="#8a9099"/>')
    pyl += (f'<path d="M{bx+96:.0f},880 Q{bx+240:.0f},700 {xb-40:.0f},880"'
            f' fill="none" stroke="#3a3734" stroke-width="30" stroke-linecap="round"/>')
    pyl += (f'<path d="M{bx+96:.0f},880 Q{bx+240:.0f},700 {xb-40:.0f},880"'
            f' fill="none" stroke="#6a6560" stroke-width="12" stroke-dasharray="10 16"/>')
    pyl += (f'<rect x="{xb-56:.0f}" y="876" width="28" height="90" rx="10"'
            f' fill="url(#zhel)" {o(5)}/>')
    pyl += ten(xb - 42, 1010, 110, 16, .4)
    pyl += (f'<rect x="{xb-140:.0f}" y="952" width="200" height="46" rx="12"'
            f' fill="url(#chug)" {o(6)}/>')
    pyl += (f'<rect x="{xb-128:.0f}" y="992" width="176" height="14" rx="6"'
            f' fill="#6a6560"/>')

    s += SL(Z_PERED, pyl + baza._ramka_pp("levo", "#120e0a", .5))
    s += baza.vinetka(.44)
    return s


# ═══════════════════ 165 ═══════════════════

def stare_vynosyat_iz_treh_mest(t):
    """Из шкафа коробка, с антресоли связка, из сарая тачка — всё к порогу.
    Живое: коробка выезжает, связка спускается, тачка катится."""
    k1 = A.out(A.seg(t, .25, 1.25))
    k2 = A.ease(A.seg(t, 1.5, 1.45))
    k3 = A.ease(A.seg(t, 2.4, 1.7))

    s = SL(Z_DAL,
           _komnata(800, "#5f4e3c", "#3a2f23")
           + baza.vozduh(1500, 420, t, 1000, .34))

    # шкаф слева
    shk = ten(300, 992, 250, 24, .45)
    shk += f'<rect x="60" y="300" width="470" height="690" rx="10" fill="url(#derev)" {o(8)}/>'
    shk += f'<rect x="86" y="326" width="200" height="638" rx="7" fill="{DOSKA2}" {o(5)}/>'
    shk += f'<circle cx="300" cy="650" r="13" fill="url(#zhel)" {o(4)}/>'
    shk += f'<rect x="306" y="326" width="200" height="638" rx="7" fill="#2a2119" opacity=".9"/>'
    shk += teplo(400, 640, 260, 420, .22)
    # коробка выезжает
    shk += (f'<g transform="translate({330 + 230*k1:.0f},{880:.0f})">'
            + ten(0, 96, 180, 24, .45)
            + f'<rect x="-168" y="-158" width="336" height="246" rx="10" fill="#c9a970" {o(8)}/>'
            + f'<path d="M-168,-82 h336" fill="none" stroke="#8d7345" stroke-width="9"/>'
            + f'<path d="M-36,-158 v246" fill="none" stroke="#8d7345" stroke-width="9"/>'
            + f'<path d="M-158,-148 l110,52" stroke="#ffffff" stroke-width="14" opacity=".22"/>'
            + '</g>')

    # антресоль посередине: связка спускается на верёвке
    ant = f'<rect x="620" y="170" width="560" height="150" rx="8" fill="url(#derev)" {o(8)}/>'
    ant += f'<rect x="642" y="190" width="516" height="112" rx="6" fill="#3a2d20" {o(5)}/>'
    ant += teplo(900, 250, 300, 150, .26)
    for i in range(4):
        ant += (f'<rect x="{676+i*118:.0f}" y="206" width="92" height="80" rx="6"'
                f' fill="#6a563c" {o(4)} opacity=".9"/>')
    ant += f'<path d="M900,310 v{130 + 320*k2:.0f}" fill="none" stroke="#b59a63" stroke-width="10"/>'
    sv_y = 440 + 320 * k2
    ant += (f'<g transform="translate(900,{sv_y:.0f}) rotate({3.2*A.w(t,2.6):.2f})">'
            + ten(0, 140, 160, 22, .42)
            + _gazety(0, 126, 1.12, t, .2)
            + f'<path d="M-132,-8 h264" fill="none" stroke="#b59a63" stroke-width="11"/>'
            + '</g>')

    # сарай справа: тачка катится
    sar = f'<rect x="1230" y="330" width="560" height="660" rx="10" fill="#3a3027" {o(8)}/>'
    sar += baza.doski(1250, 350, 520, 620, 86, True, "dosk")
    sar += f'<rect x="1250" y="350" width="520" height="620" fill="#140f0c" opacity=".30"/>'
    sar += (f'<rect x="1310" y="430" width="400" height="430" rx="10" fill="#f0c168"'
            f' opacity=".30"/>')
    sar += teplo(1510, 660, 420, 420, .45)
    tx = 1510 - 420 * k3
    sar += (f'<g transform="translate({tx:.0f},910) scale(1.34)">'
            + ten(0, 96, 160, 22, .45)
            + f'<path d="M-150,0 l40,-110 h230 l-26,110 z" fill="url(#zhel)" {o(8)}/>'
            + f'<path d="M-110,-110 h230 l-14,40 h-202 z" fill="#3c454e" {o(5)}/>'
            + f'<path d="M-110,-110 h230" fill="none" stroke="#d2dae2" stroke-width="10" opacity=".65"/>'
            + f'<path d="M-124,-40 h208" fill="none" stroke="#ffffff" stroke-width="8" opacity=".18"/>'
            + f'<path d="M100,-16 l132,74" fill="none" stroke="{CHUGUN}" stroke-width="18" stroke-linecap="round"/>'
            + f'<path d="M-136,-6 l-80,80" fill="none" stroke="{CHUGUN}" stroke-width="16" stroke-linecap="round"/>'
            + f'<circle cx="232" cy="58" r="13" fill="#8a6540" {o(4)}/>'
            + f'<g transform="rotate({-tx*.55:.0f} -94 70)">'
            + f'<circle cx="-94" cy="70" r="56" fill="url(#chug)" {o(6)}/>'
            + f'<circle cx="-94" cy="70" r="18" fill="#8a9099"/>'
            + f'<path d="M-150,70 h112 M-94,14 v112" stroke="#8a9099" stroke-width="7"/></g>'
            + _zont(-40, -116, .5, t, True, .5)
            + '</g>')

    s += SL(Z_SRED, shk + ant + sar)

    # куча у порога
    kuch = ""
    if k3 > .55:
        kop = min(1.0, (k3 - .55) / .45)
        kuch += f'<g opacity="{kop:.2f}">'
        kuch += ten(1660, 1020, 300, 30, .5)
        kuch += _gazety(1616, 1010, 1.0, t, .6)
        kuch += _zont(1782, 1010, .70, t, True, .2)
        kuch += (f'<rect x="1470" y="866" width="260" height="154" rx="8" fill="#c9a970" {o(7)}/>'
                 f'<path d="M1470,924 h260" fill="none" stroke="#8d7345" stroke-width="8"/>')
        kuch += '</g>'
    s += SL(Z_PERED,
            kuch
            + f'<rect y="1016" width="{W}" height="64" fill="{DOSKA2}" {o(6)}/>'
            + baza._ramka_pp("pravo", "#120e0a", .55))
    s += baza.vinetka(.44)
    return s


# ═══════════════════ 166 ═══════════════════

def tri_nenuzhnye_veschi(t):
    """Крупно три вещи в ряд: чашка без ручки, зонт с торчащей спицей,
    стопка газет. Живое: чашка качается, спица дрожит, уголки шевелятся."""
    s = SL(Z_DAL,
           _komnata(700, "#6a5744", "#42342a")
           + baza.vozduh(960, 280, t, 1050, .30)
           + baza.polka(240, 300, 1440)
           + baza.krynka(380, 296, .72) + baza.krynka(1540, 296, .64)
           + ob.mandarin(1380, 268, .66, 0.0, t))

    stol = f'<rect y="846" width="{W}" height="{H-846}" fill="url(#derev)"/>'
    stol += f'<rect y="838" width="{W}" height="24" fill="{DOSKA2}" {o(6)}/>'
    for i in range(4):
        stol += (f'<line x1="0" y1="{900+i*54}" x2="{W}" y2="{900+i*54}"'
                 f' stroke="#5a3b22" stroke-width="4" opacity=".4"/>')
    s += SL(Z_SRED, stol + teplo(960, 830, 1080, 470, .44))

    s += SL(Z_PERED,
            _chashka(300, 848, 2.05, t, .0, True)
            + _zont(950, 858, 1.78, t, True, .3)
            + _gazety(1610, 848, 1.85, t, .5)
            + baza._ramka_pp("oba", "#120e0a", .55))
    s += baza.vinetka(.46)
    return s


# ═══════════════════ 167 ═══════════════════

def meshok_starya_u_poroga_goda(t):
    """Светящийся проём года: мешок старья в него не пролезает, человек
    ставит мешок и проходит налегке. Живое: мешок застревает, свет льётся."""
    k_pod = A.ease(A.seg(t, .15, 1.35))          # подошли к проёму
    zastr = A.seg(t, 1.5, .85)                   # застрял, толчки
    stavit = A.ease(A.seg(t, 2.45, .85))         # ставит мешок
    uhod = A.ease(A.seg(t, 3.35, 1.5))           # проходит налегке

    tolch = 16 * math.sin(2 * math.pi * t * 3.1) * zastr * (1 - stavit)
    mx = 700 + 340 * k_pod + tolch
    my = 980 + 24 * stavit

    s = SL(Z_DAL,
           f'<rect width="{W}" height="{H}" fill="#191520"/>'
           + _grad("b8pri", "#2d2432", "#120e16")
           + f'<rect width="{W}" height="840" fill="url(#b8pri)"/>'
           + baza.doski(0, 0, W, 840, 150, True, "dosk")
           + f'<rect width="{W}" height="840" fill="#0d0a12" opacity=".58"/>'
           + f'<rect y="830" width="{W}" height="{H-830}" fill="url(#pol)" opacity=".8"/>'
           + _proyom(1120, 230, 420, 650, t, 1.0))

    s += SL(Z_SRED,
            baza.lampa(330, 420, t, .85, abazhur=False)
            + baza._mebel_hlam(60, 980, 420, t, 5)
            + teplo(1330, 640, 760, 620, .45))

    # мешок и человек
    chel = ob.figura(mx - 310 + 700 * uhod, 1030 - 50 * uhod, 520 - 110 * uhod, t,
                     col="#231a26", kant="#ffd89a", ph=.2,
                     op=1.0 - .30 * uhod, krasnoe=False)
    mesh = _meshok(mx, my, 1.02 - .05 * stavit, t, .1, szhat=zastr * (1 - stavit))

    s += SL(Z_PERED,
            mesh + chel
            + f'<path d="M0,1060 h{W}" stroke="{DOSKA2}" stroke-width="22"/>'
            + baza._ramka_pp("levo", "#0c0910", .75))
    s += baza.vinetka(.50)
    return s


# ═══════════════════ 169 ═══════════════════

def etazh_i_zabor(t):
    """Развилка: слева окно высокого этажа, справа дом за дощатым забором,
    и там и там один листок. Живое: листки подсвечиваются разом, дым, занавеска."""
    gor = .30 + .55 * (0.5 + 0.5 * A.w(t, 2.4))

    vid_l = (f'<rect width="{W}" height="{H}" fill="#f6d79a"/>'
             + teplo(400, 520, 420, 400, .8)
             + baza.siluet(300, 700, 300, "#6a4a28", .55, False, "#ffe6b0")
             + f'<rect x="130" y="300" width="540" height="440" fill="{SVET}" opacity=".3"/>')

    s = baza.nebo("sumer", t)
    s += baza.oblaka(t, 210, 4, 7, .45, "#d8e0ee", 8.0)
    s += SL(Z_DAL,
            baza._panelka(-60, 1080, 1000, t, 7, True, 4)
            + baza._ulica_dal(1000, 800, 920, t, True, 11))

    # ── левая половина: окно высокого этажа
    lev = f'<rect x="0" y="0" width="930" height="{H}" fill="#3c4458" opacity=".55"/>'
    lev += baza.kladka(0, 180, 930, 900, 96, "url(#beton)")
    lev += f'<rect x="0" y="180" width="930" height="900" fill="#2c3346" opacity=".5"/>'
    lev += baza.okno_izby(130, 300, 540, 440, t, vid=vid_l, moroz=.12, svet=True)
    lev += baza.zanaveska(170, 318, 400, 150, "#c8d6e6", t, 1)
    lev += baza.zanaveska(632, 318, 400, 150, "#c8d6e6", t, -1)
    lev += teplo(400, 520, 460, 400, .50)
    lev += (f'<rect x="130" y="760" width="540" height="40" rx="8" fill="url(#beton)" {o(6)}/>'
            f'<path d="M130,760 q136,-22 270,-8 q136,14 270,-10 l0,20 h-540 z"'
            f' fill="url(#sneg)" {o(4)}/>')
    lev += _listok(716, 440, 180, 224, t, rost=(1, 1, 1), zacherk=(1, 1, 1),
                   galka=1.0, ang=-4.0, svet=gor)

    # ── правая половина: дом за дощатым забором
    prav = baza.izba_snaruzhi(1130, 820, 700, t, True, True, 3)
    prav += (f'<path d="M990,830 q230,-26 460,-10 q230,16 470,-12 L1920,{H} L990,{H} Z"'
             f' fill="url(#sneg)" {o(5)}/>')
    prav += baza.doski(990, 700, 930, 380, 92, True, "dosk")
    prav += f'<rect x="990" y="700" width="930" height="380" fill="#2a2016" opacity=".30"/>'
    for yy in (744, 1010):
        prav += f'<rect x="990" y="{yy}" width="930" height="24" fill="{DOSKA2}" {o(5)}/>'
    prav += (f'<path d="M990,700 q232,-20 464,-6 q232,14 466,-8 l0,18 h-930 z"'
             f' fill="url(#sneg)" {o(4)}/>')
    prav += _listok(1600, 788, 180, 224, t, rost=(1, 1, 1), zacherk=(1, 1, 1),
                    galka=1.0, ang=3.0, svet=gor)

    s += SL(Z_SRED, lev + prav)

    razdel = (f'<rect x="930" y="0" width="60" height="{H}" fill="#0f131c" opacity=".88"/>'
              f'<rect x="946" y="0" width="10" height="{H}" fill="{ob.ZOLOTO}" opacity=".30"/>')
    s += SL(Z_PERED,
            razdel
            + f'<path d="M-20,1052 q240,-24 480,-8 q240,16 480,-10 q240,-20 480,-4'
              f' q240,14 500,-12 L1940,{H} L-20,{H} Z" fill="url(#sneg)" {o(5)}/>'
            + baza._ramka_pp("oba", "#101624", .50))
    s += baza.sneg_letit(t, 52, 7, .78)
    s += baza.vinetka(.42)
    return s


# ═══════════════════ 170 ═══════════════════

def god_kakim_ego_hotyat_prozhit(t):
    """Вечер, золотой свет: семья за столом, вид от торца. Двое обнимаются,
    блюдо встаёт на стол, под тарелкой блестит монета, листок зачёркнут."""
    obn = .5 + .5 * A.w(t, 3.6)                       # двое обнимаются
    bl_u = A.out(A.seg(t, 1.3, 1.25))                 # блюдо опускается
    by = 330 + (700 - 330) * bl_u

    vid = baza._nebo("noch", t) + baza._sneg_letit(t, 22, 6, .6)

    s = SL(Z_DAL,
           _komnata(640, "#6b4f3a", "#3f2c1e")
           + baza.okno_izby(70, 190, 330, 290, t, vid=vid, moroz=.18)
           + ob.elka(1700, 650, 520, t, True, True, 4, True)
           + ob.girlyanda(120, 150, 1820, 170, t, 16, 110, .2)
           + baza.lampa(960, 330, t, 1.25, abazhur=True)
           + baza.vozduh(960, 360, t, 1050, .26))

    # стол от торца: трапеция
    stol = (f'<path d="M230,1050 L1690,1050 L1180,560 L740,560 Z" fill="url(#rush)" {o(7)}/>')
    stol += (f'<path d="M258,1030 L1662,1030 L1168,578 L752,578 Z" fill="#f6ecd2" opacity=".55"/>')
    stol += (f'<path d="M230,1050 L1690,1050 L1180,560 L740,560 Z" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".45"/>')
    stol += ten(960, 1062, 740, 30, .5)

    # блюда и свечи по столу
    pred = ""
    for i, (px, py, sc) in enumerate(((560, 950, 1.0), (1360, 950, 1.0),
                                      (780, 760, .72), (1140, 760, .72),
                                      (960, 660, .58))):
        pred += _tarelka(px, py, 96 * sc, t, 0.0, False)
    pred += baza.svecha(960, 820, t, .0, 1.1)
    pred += ob.bokal(700, 930, t, .9, .1)
    pred += ob.bokal(1230, 930, t, .9, .5)
    pred += baza.karavay(960, 900, .8, True)
    pred += ob.mandarin(840, 870, .78, 0.0, t)
    pred += ob.mandarin(1090, 876, .72, .3, t)

    # блюдо встаёт на стол
    pred += _blyudo_pelmeni(960, by, .9, t, .0, par_on=bl_u > .9)

    # семья: по левому и правому борту, в красном
    lyudi = ""
    for i, (px, py, hh, kr) in enumerate(((300, 1010, 330, True), (520, 880, 280, False),
                                          (690, 770, 236, True))):
        lyudi += ob.figura(px, py, hh, t, col="#2b2230", kant="#ffd89a",
                           platok=(i == 1), ph=i * .21, krasnoe=kr)
    for i, (px, py, hh, kr) in enumerate(((1620, 1010, 330, False), (1400, 880, 280, True),
                                          (1230, 770, 236, False))):
        lyudi += ob.figura(px, py, hh, t, col="#2a2630", kant="#ffd89a",
                           platok=(i == 2), ph=.1 + i * .23, krasnoe=kr)
    # двое у дальнего торца обнимаются
    lyudi += ob.figura(880 + 22 * obn, 650, 210, t, col="#2e2330", kant="#ffd89a",
                       platok=True, ph=.5, krasnoe=True)
    lyudi += ob.figura(1040 - 22 * obn, 650, 210, t, col="#262c38", kant="#ffd89a",
                       ph=.8, krasnoe=False)

    s += SL(Z_SRED, stol + lyudi + pred)

    # ближний край: тарелка с монетой и зачёркнутый листок
    s += SL(Z_PERED,
            _tarelka(540, 1000, 215, t, .26 + .08 * A.w(t, 3.0), moneta=True)
            + _listok(1250, 880, 220, 264, t, rost=(1, 1, 1), zacherk=(1, 1, 1),
                      galka=1.0, ang=5.0, svet=.34)
            + baza._ramka_pp("oba", "#1a1008", .50))
    s += baza.vinetka(.40)
    return s


# ═══════════════════ 180 ═══════════════════

def tarelka_i_karman_s_sekretom(t):
    """Крупно край стола: край тарелки сам приподнимается и из-под него идёт
    свет, из кармашка фартука — тоже. Живое: подъём, свет, скатерть."""
    pod = .18 + .82 * (0.5 + 0.5 * A.w(t, 4.2))
    kar = .58 + .42 * (0.5 + 0.5 * A.w(t, 3.1, .35))
    kol = 9 * A.w(t, 5.0)

    s = SL(Z_DAL,
           _komnata(520, "#60452f", "#35241a")
           + ob.elka(1700, 560, 380, t, True, True, 7, True)
           + ob.girlyanda(60, 120, 1860, 140, t, 14, 90, .4)
           + baza.lampa(620, 250, t, 1.0, abazhur=True)
           + baza.vozduh(760, 330, t, 1000, .32)
           + f'<rect width="{W}" height="{H}" fill="#120c08" opacity=".22"/>')

    # край стола крупно
    skat = (f'<path d="M-40,700 h2000 v{H-640} h-2000 z" fill="url(#rush)" {o(7)}/>')
    skat += (f'<path d="M-40,700 q480,{30+kol:.0f} 980,4 q480,{-26+kol:.0f} 1020,12"'
             f' fill="none" stroke="{DOSKA2}" stroke-width="11" opacity=".55"/>')
    for i in range(7):
        skat += (f'<path d="M{-40+i*300:.0f},724 q{22+kol*.6:.0f},180 {-8:.0f},380"'
                 f' fill="none" stroke="#cdb98d" stroke-width="11" opacity=".6"/>')
    skat += (f'<path d="M-40,784 q480,{34+kol:.0f} 980,6 q480,{-30+kol:.0f} 1020,14"'
             f' fill="none" stroke="{ob.ALYJ}" stroke-width="14" opacity=".65"/>')
    skat += (f'<path d="M-40,700 q480,{30+kol:.0f} 980,4 q480,{-26+kol:.0f} 1020,12 v-60 h-2000 z"'
             f' fill="#000000" opacity=".16"/>')
    s += SL(Z_SRED, skat + teplo(760, 860, 1000, 440, .32))

    # фартук с кармашком справа: складки и сноп света из кармана
    fart = f'<g transform="translate(1440,400)">'
    fart += ten(60, 660, 260, 30, .5)
    fart += (f'<path d="M-200,0 q200,-56 400,0 l46,640 q-246,54 -492,0 z"'
             f' fill="{ob.ALYJ}" {o(9)}/>')
    for i in range(5):
        fart += (f'<path d="M{-150+i*76:.0f},30 q{14+kol*.4:.0f},300 {4:.0f},604"'
                 f' fill="none" stroke="{ob.ALYJ2}" stroke-width="10" opacity=".55"/>')
    fart += (f'<path d="M-182,34 q182,-48 364,0" fill="none" stroke="{ob.ZOLOTO}"'
             f' stroke-width="11" opacity=".85"/>')
    fart += (f'<path d="M-160,60 q90,-30 160,-14" fill="none" stroke="#ffffff"'
             f' stroke-width="14" opacity=".16"/>')
    fart += teplo(0, 300, 360, 320, .40 * kar)
    fart += (f'<path d="M-150,228 h300 v150 q0,90 -150,86 q-150,4 -150,-86 z"'
             f' fill="{ob.ALYJ2}" {o(8)}/>')
    fart += (f'<path d="M-150,228 h300 v150 q0,90 -150,86 q-150,4 -150,-86 z"'
             f' fill="{SVET}" opacity="{.26*kar:.2f}"/>')
    fart += (f'<path d="M-132,250 h264 v132 q0,74 -132,70 q-132,4 -132,-70 z"'
             f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="5"'
             f' stroke-dasharray="15 11" opacity=".8"/>')
    fart += (f'<path d="M-158,214 h316 v34 q-158,18 -316,0 z" fill="{ob.ALYJ}" {o(6)}/>')
    # сноп света наружу из кармана
    fart += (f'<path d="M-110,234 L{-190-60*kar:.0f},{70-80*kar:.0f}'
             f' L{160+70*kar:.0f},{50-90*kar:.0f} L110,234 Z" fill="{SVET}"'
             f' opacity="{.17*kar:.2f}"/>')
    fart += (f'<ellipse cx="0" cy="234" rx="{168*kar:.0f}" ry="{54*kar:.0f}" fill="#fff6d2"'
             f' opacity="{.80*kar:.2f}"/>')
    fart += (f'<ellipse cx="0" cy="232" rx="{104*kar:.0f}" ry="{30*kar:.0f}" fill="#ffffff"'
             f' opacity="{.72*kar:.2f}"/>')
    fart += (f'<path d="M-138,244 h276" fill="none" stroke="{ob.ZOLOTO}" stroke-width="10"'
             f' opacity=".9"/>')
    fart += '</g>'

    s += SL(Z_PERED,
            _tarelka(560, 830, 360, t, pod, moneta=False)
            + fart
            + baza._ramka_pp("levo", "#140d08", .45))
    s += baza.vinetka(.46)
    return s


# ═══════════════════ 181 ═══════════════════

def svoi_za_novogodnim_stolom(t):
    """Стол под абажуром со стороны хозяйки: красная лента в волосах, карман
    вздрагивает, ваза мандаринов, внук забирается на стул."""
    lenta = 8 * A.w(t, 2.9)
    vnuk = A.over(A.seg(t, 2.1, 1.35))
    hlop = max(0.0, math.sin(2 * math.pi * (t / 2.3))) ** 6

    vid = baza._nebo("noch", t) + baza._sneg_letit(t, 20, 4, .6)

    s = SL(Z_DAL,
           _komnata(600, "#664a36", "#3a291c")
           + baza.okno_izby(90, 170, 320, 280, t, vid=vid, moroz=.5)
           + ob.elka(1690, 640, 480, t, True, True, 5, True)
           + ob.girlyanda(80, 130, 1840, 150, t, 15, 100, .15)
           + baza.vozduh(960, 330, t, 1020, .26))

    # круглый стол
    stol = ten(960, 952, 640, 44, .5)
    stol += (f'<ellipse cx="960" cy="760" rx="600" ry="226" fill="url(#rush)" {o(8)}/>')
    stol += (f'<ellipse cx="960" cy="748" rx="540" ry="194" fill="#f6ecd2" opacity=".5"/>')
    stol += (f'<ellipse cx="960" cy="760" rx="600" ry="226" fill="none" stroke="{ob.ALYJ}"'
             f' stroke-width="8" opacity=".5"/>')
    stol += (f'<path d="M360,760 q600,286 1200,0 v96 q-600,286 -1200,0 z"'
             f' fill="url(#rush)" {o(6)}/>')

    # ваза мандаринов в середине
    vaza = ten(960, 742, 170, 22, .45)
    vaza += (f'<path d="M842,690 q118,78 236,0 q-14,58 -118,58 q-104,0 -118,-58 z"'
             f' fill="url(#stekl)" opacity=".8" {o(6)}/>')
    vaza += f'<path d="M912,748 h96 v18 h-96 z" fill="url(#zhel)" {o(5)}/>'
    for i, (dx, dy, sc) in enumerate(((-66, 672, .82), (0, 656, .9), (62, 672, .82),
                                      (-32, 630, .74), (34, 628, .74))):
        vaza += ob.mandarin(960 + dx, dy, sc, 0.0, t)
        bl = .35 + .65 * abs(A.w(t, 2.1 + i * .4, i * .2))
        vaza += (f'<ellipse cx="{960+dx-13:.0f}" cy="{dy-14:.0f}" rx="{13*sc:.0f}"'
                 f' ry="{9*sc:.0f}" fill="#fff3d2" opacity="{bl*.8:.2f}"/>')

    # родные вокруг стола + стул внука
    lyudi = _figury_vokrug(960, 680, 540, 196, t, 5, 268, 3, krasnyh=(1, 3))
    stul = _stul(1510, 920, 1.08, -3.0)
    if vnuk > .02:
        lyudi += ob.figura(1510, 920 - 126 * vnuk, 168 + 26 * vnuk, t,
                           col="#2f2330", kant="#ffd89a", ph=.6, krasnoe=True)

    s += SL(Z_SRED, stol + stul + lyudi + vaza
            + baza.svecha(700, 736, t, .2, 1.0)
            + baza.svecha(1230, 738, t, .6, 1.0)
            + ob.bokal(820, 782, t, .85, .2)
            + ob.bokal(1110, 784, t, .85, .7)
            + baza.lampa(960, 300, t, 1.35, abazhur=True))

    # хозяйка со спины крупно, ближний план
    hgy = 1560 - 940 * .77                     # макушка силуэта хозяйки
    hoz = ob.figura(900, 1560, 940, t, col="#2a1f28", kant="#ffd89a", ph=.0)
    # красная лента в волосах: бант НА затылке, концы вниз по центру
    hoz += (f'<g transform="rotate({lenta:.2f} 900 {hgy+40:.0f})">'
            f'<path d="M784,{hgy+36:.0f} q116,-74 232,0" fill="none" stroke="{ob.ALYJ}"'
            f' stroke-width="26" stroke-linecap="round"/>'
            f'<path d="M862,{hgy+30:.0f} q38,-40 76,0 q-38,34 -76,0 z" fill="{ob.ALYJ}" {o(6)}/>'
            f'<circle cx="900" cy="{hgy+32:.0f}" r="15" fill="{ob.ZOLOTO}" {o(4)}/>'
            f'<path d="M914,{hgy+40:.0f} q34,48 16,108 q-26,-18 -30,-70 z"'
            f' fill="{ob.ALYJ}" {o(5)}/>'
            f'<path d="M886,{hgy+40:.0f} q-34,48 -16,108 q26,-18 30,-70 z"'
            f' fill="{ob.ALYJ2}" {o(5)}/></g>')
    # карман вздрагивает — руки не рисуем, работает сам карман
    ksc = 1.0 + .09 * hlop
    hoz += (f'<g transform="translate(978,1046) rotate(-5) scale({ksc:.3f})">'
            f'<rect x="-96" y="-84" width="192" height="168" rx="14" fill="{ob.ALYJ2}" {o(7)}/>'
            f'<path d="M-86,-64 h172" fill="none" stroke="{ob.ZOLOTO}" stroke-width="10" opacity=".85"/>'
            f'<path d="M-70,-40 q70,-24 140,-8" fill="none" stroke="#ffffff"'
            f' stroke-width="10" opacity=".14"/>'
            f'<ellipse cx="0" cy="-74" rx="{94*hlop:.0f}" ry="{30*hlop:.0f}" fill="{SVET}"'
            f' opacity="{.50*hlop:.2f}"/></g>')

    s += SL(Z_PERED, hoz + baza._ramka_pp("oba", "#180f08", .5))
    s += baza.vinetka(.42)
    return s


# ═══════════════════ 182 ═══════════════════

def blyudo_pelmeney_idet_po_krugu(t):
    """Блюдо пельменей идёт по кругу вокруг стола и не пустеет, над столом
    плывёт оранжевая струйка запаха. Живое: круг, пар, струйка."""
    a = -math.pi / 2 + 2 * math.pi * ((t / 6.4) % 1.0)
    bx = 960 + math.cos(a) * 380
    by = 762 + math.sin(a) * 132
    bs = .80 + .30 * (0.5 + 0.5 * math.sin(a))

    s = SL(Z_DAL,
           _komnata(600, "#6a4c35", "#3a281b")
           + ob.elka(190, 640, 460, t, True, True, 9, True)
           + ob.girlyanda(70, 130, 1850, 150, t, 15, 96, .55)
           + baza.lampa(960, 290, t, 1.3, abazhur=True)
           + baza.vozduh(960, 350, t, 1020, .26))

    stol = ten(960, 960, 660, 44, .5)
    stol += f'<ellipse cx="960" cy="770" rx="620" ry="236" fill="url(#rush)" {o(8)}/>'
    stol += f'<ellipse cx="960" cy="756" rx="556" ry="202" fill="#f6ecd2" opacity=".5"/>'
    stol += (f'<ellipse cx="960" cy="770" rx="620" ry="236" fill="none" stroke="{ob.ALYJ}"'
             f' stroke-width="8" opacity=".5"/>')
    stol += (f'<path d="M340,770 q620,300 1240,0 v100 q-620,300 -1240,0 z"'
             f' fill="url(#rush)" {o(6)}/>')

    # тарелки по кругу — каждый себе положил
    tar = ""
    for i in range(7):
        aa = -math.pi / 2 + 2 * math.pi * (i / 7.0) + .22
        tx = 960 + math.cos(aa) * 430
        ty = 752 + math.sin(aa) * 148
        sc = .66 + .30 * (0.5 + 0.5 * math.sin(aa))
        tar += _tarelka(tx, ty, 108 * sc, t, 0.0, False)
        for k in range(3):
            tar += (f'<path d="M{tx-34*sc+k*34*sc:.0f},{ty-6*sc:.0f}'
                    f' q{16*sc:.0f},{-20*sc:.0f} {32*sc:.0f},0'
                    f' q{-16*sc:.0f},{10*sc:.0f} {-32*sc:.0f},0 z"'
                    f' fill="#f2e6cc" {o(3)}/>')

    lyudi = _figury_vokrug(960, 700, 580, 204, t, 6, 268, 8, krasnyh=(0, 4))

    s += SL(Z_SRED, stol + lyudi + tar
            + baza.svecha(660, 716, t, .3, 1.0)
            + baza.svecha(1280, 718, t, .8, 1.0))

    s += SL(Z_PERED,
            _blyudo_pelmeni(bx, by, bs, t, .0, True)
            + teplo(bx, by - 40 * bs, 300 * bs, 230 * bs, .40)
            + _struyka(bx, by - 70 * bs, t, 240, .0, ob.MANDA, .55)
            + _struyka(bx + 70 * bs, by - 56 * bs, t, 180, .45, SVET, .38)
            + baza._ramka_pp("oba", "#1a1008", .5))
    s += baza.vinetka(.42)
    return s


# ═══════════════════ 183 ═══════════════════

def tri_sdelannyh_dela(t):
    """Три медальона: стопка белья со скатертью, зачёркнутый листок с галочкой,
    пустое ведро вверх дном у двери. Живое: загораются по одному, галочка, кот."""
    gor = [A.ease(A.seg(t, .25 + i * .95, .7)) for i in range(3)]
    gal = A.ease(A.seg(t, 2.1, .9))
    kot_u = A.over(A.seg(t, 3.0, .85))

    vid = (baza._nebo("rassv", t, zvezdy=False)
           + baza._oblaka(t, 230, 3, 6, .5, "#f0ead8", 6.0))

    s = SL(Z_DAL,
           _komnata(760, "#6d5742", "#43331f")
           + baza.polka(1150, 236, 660)
           + baza.krynka(1270, 232, .64)
           + ob.mandarin(1470, 206, .6, 0.0, t)
           + baza.krynka(1700, 232, .58)
           + teplo(1680, 260, 520, 400, .40)
           + baza.vozduh(760, 400, t, 980, .28)
           + ob.girlyanda(60, 110, 1860, 130, t, 14, 86, .3))

    # ── нутро медальонов: рисуется вокруг центра своего круга
    # 1: стопка белья со скатертью
    n1 = teplo(330, 600, 260, 220, .40)
    for i in range(5):
        yy = 700 - i * 40
        wdt = 270 - i * 12
        n1 += (f'<rect x="{330-wdt/2:.0f}" y="{yy-38:.0f}" width="{wdt:.0f}" height="38"'
               f' rx="8" fill="{"#f3ecdc" if i%2 else "#e2d8c2"}" {o(5)}/>')
        n1 += (f'<path d="M{330-wdt/2+14:.0f},{yy-20:.0f} h{wdt-28:.0f}" fill="none"'
               f' stroke="#c7b997" stroke-width="5" opacity=".8"/>')
    n1 += f'<path d="M216,504 h228 l-20,58 h-188 z" fill="url(#rush)" {o(6)}/>'
    n1 += f'<path d="M232,532 h196" fill="none" stroke="{ob.ALYJ}" stroke-width="8" opacity=".85"/>'
    n1 += ten(330, 716, 150, 18, .4)

    # 2: зачёркнутый листок с галочкой
    n2 = teplo(960, 580, 250, 230, .35)
    n2 += _listok(850, 420, 230, 288, t, rost=(1, 1, 1), zacherk=(1, 1, 1),
                  galka=gal, ang=-4.0, svet=.0)

    # 3: пустое ведро вверх дном у двери, за окном ещё светло
    n3 = (f'<rect x="1398" y="400" width="200" height="330" rx="8" fill="url(#derev)" {o(7)}/>')
    n3 += (f'<rect x="1420" y="420" width="158" height="290" rx="6" fill="{DOSKA2}" {o(5)}/>')
    n3 += f'<circle cx="1562" cy="586" r="12" fill="url(#zhel)" {o(4)}/>'
    n3 += (f'<rect x="1618" y="430" width="170" height="200" rx="8" fill="#d6e8f4"'
           f' opacity=".9" {o(6)}/>')
    n3 += (f'<path d="M1703,430 v200 M1618,530 h170" stroke="url(#derev)" stroke-width="12"/>')
    n3 += teplo(1703, 530, 210, 190, .50)
    n3 += _vedro(1672, 722, .66, t, True, False)
    if kot_u > .02:
        n3 += baza.kot(1672, 722 - 106 - 34 * kot_u, t, .54 * kot_u, "#3b3430", False)

    # Три равных круга в ряд читались схемой. Подвесы на гвоздях, разные
    # размеры и высоты — это ВИСЯЩИЕ медальоны, а не выложенные кружки.
    podves = ""
    for mx_, my_, mr_ in ((330, 572, 244), (960, 548, 258), (1590, 580, 238)):
        podves += (f'<circle cx="{mx_}" cy="{my_-mr_-96}" r="11" fill="{ZHELEZ}" {o(4)}/>')
        podves += (f'<path d="M{mx_},{my_-mr_-92} l{-26},{86} m{26},{-86} l{26},{86}"'
                   f' fill="none" stroke="{MED}" stroke-width="9" opacity=".9"/>')
    s += SL(Z_SRED,
            podves
            + _medalon(330, 572, 244, t, gor[0], n1)
            + _medalon(960, 548, 258, t, gor[1], n2)
            + _medalon(1590, 580, 238, t, gor[2], n3))

    s += SL(Z_PERED,
            baza.polka(150, 906, 1340)
            + ob.mandarin(300, 896, .86, 0.0, t)
            + ob.mandarin(392, 900, .72, .3, t)
            + baza.krynka(640, 898, .78)
            + baza.karavay(1060, 900, .72, True)
            + baza.krynka(1380, 898, .7)
            + ob.elka(1874, 1128, 290, t, True, False, 3, True)
            + baza._ramka_pp("levo", "#140e08", .45))
    s += baza.vinetka(.42)
    return s
