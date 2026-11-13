# -*- coding: utf-8 -*-
"""Декорации планов 105-131 ролика «Как встречать год хозяйки года 2027»."""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob
OKNO = (860, 300, 980, 551)

# ── СОБСТВЕННЫЕ КИРПИЧИКИ БЛОКА ────────────────────────────────────────────
# Нарисованы заново от кирпичиков baza/obrazy. Рук в кадре нет (правило 6):
# там, где текст говорит «рука берёт», работает сам предмет, а где ладонь
# названа главным героем кадра — её играет ВЯЗАНАЯ ВАРЕЖКА: предмет, который
# читается как ладонь, но рукой не является.


def _g(nid, c1, c2, vert=True):
    """Свой градиент: у каждого предмета должен быть объём (правило 5)."""
    return (f'<linearGradient id="{nid}" x1="0" y1="0" x2="{0 if vert else 1}"'
            f' y2="{1 if vert else 0}"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def _mix(c1, c2, k):
    """Перетекание цвета: им бледнеют яблоки и гаснет лампа."""
    k = max(0.0, min(1.0, k))
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def _stena(c1, c2, y_pol=None, pol="url(#pol)"):
    """Стена комнаты одним куском плюс пол: дешёвая глубина для крупных планов."""
    s = _g("stnb", c1, c2) + f'<rect width="{W}" height="{H}" fill="url(#stnb)"/>'
    if y_pol:
        s += baza.polovicy(y_pol, pol)
    return s


def _moneta(cx, cy, rx, ry, t, ph=0.0, op=1.0, ten_=True):
    """Монета: золотой градиент, ободок, бегающий блик."""
    bl = .3 + .7 * abs(A.w(t, 2.3, ph))
    s = f'<g opacity="{op:.2f}">'
    if ten_:
        s += ten(cx + 3, cy + ry * 1.2, rx * 1.05, ry * .75, .45)
    s += (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"'
          f' fill="url(#zol)" {o(max(2.0, rx * .13))}/>')
    s += (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx * .62:.1f}" ry="{ry * .62:.1f}"'
          f' fill="none" stroke="{ob.ZOLOTO2}" stroke-width="{max(1.6, rx * .09):.1f}" opacity=".6"/>')
    s += (f'<ellipse cx="{cx - rx * .3:.1f}" cy="{cy - ry * .34:.1f}" rx="{rx * .3:.1f}"'
          f' ry="{ry * .28:.1f}" fill="#fff8de" opacity="{bl:.2f}"/>')
    return s + "</g>"


def _kupyura(cx, cy, w_, h_, ang=0.0, op=1.0, slozh=False):
    """Купюра БЕЗ цифр и названий: рамка, розетка и волна — узор, не текст."""
    s = (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.2f})" opacity="{op:.2f}">'
         + ten(4, h_ * .62, w_ * .52, h_ * .22, .4))
    s += (f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6"'
          f' fill="url(#list)" {o(max(3, w_ * .018))}/>')
    s += (f'<rect x="{-w_/2 + w_*.06:.0f}" y="{-h_/2 + h_*.12:.0f}" width="{w_*.88:.0f}"'
          f' height="{h_*.76:.0f}" rx="4" fill="none" stroke="{ob.ZOLOTO2}"'
          f' stroke-width="{max(2, w_*.012):.0f}" opacity=".55"/>')
    s += (f'<circle cx="{-w_*.26:.0f}" cy="0" r="{h_*.26:.0f}" fill="none"'
          f' stroke="{MED}" stroke-width="{max(2, w_*.01):.0f}" opacity=".5"/>')
    s += (f'<path d="M{-w_*.06:.0f},{-h_*.16:.0f} q{w_*.12:.0f},{h_*.22:.0f} {w_*.24:.0f},0'
          f' q{w_*.12:.0f},{-h_*.22:.0f} {w_*.24:.0f},0" fill="none" stroke="{MED}"'
          f' stroke-width="{max(2, w_*.011):.0f}" opacity=".45"/>')
    if slozh:
        s += (f'<line x1="0" y1="{-h_/2:.0f}" x2="0" y2="{h_/2:.0f}" stroke="#b9a87e"'
              f' stroke-width="{max(2, w_*.014):.0f}" opacity=".7"/>')
        s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} h{w_/2:.0f} v{h_:.0f} h{-w_/2:.0f} z"'
              f' fill="#ffffff" opacity=".12"/>')
    return s + "</g>"


def _tarelka(cx, cy, rx, t, podem=0.0, s_=1.0):
    """Тарелка. `podem` 0..1 — левый край приподнят, правый лежит на столе."""
    ry = rx * .36
    ang = -13 * podem
    lift = -18 * podem
    s = (f'<g transform="translate({cx:.1f},{cy + lift:.1f}) rotate({ang:.2f})">'
         + ten(0, ry * 1.5 + 12 * podem, rx * 1.02, ry * .7, .5))
    s += f'<ellipse rx="{rx:.0f}" ry="{ry:.0f}" fill="url(#krem)" {o(6)}/>'
    s += (f'<ellipse rx="{rx*.72:.0f}" ry="{ry*.72:.0f}" fill="none" stroke="{ob.ALYJ}"'
          f' stroke-width="5" opacity=".55"/>')
    s += (f'<ellipse rx="{rx*.58:.0f}" ry="{ry*.58:.0f}" fill="#fbf4e3" opacity=".8" {o(3)}/>')
    s += (f'<path d="M{-rx*.72:.0f},{-ry*.26:.0f} q{rx*.4:.0f},{-ry*.6:.0f} {rx*.82:.0f},{-ry*.1:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="8" opacity=".5"/>')
    return s + "</g>"


def _varezhka(x, y, s_, t, szhat=0.0, ph=0.0, zerk=False, dr=1.6):
    """ВАРЕЖКА вместо ладони (правило 6). `szhat` 0..1 — верх ладони
    загибается вниз и накрывает то, что лежит на ней."""
    drog = dr * A.w(t, 3.1, ph)
    sx = -s_ if zerk else s_
    g = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({drog:.2f})'
         f' scale({sx:.3f},{s_:.3f})">')
    g += ten(6, 120, 104, 24, .5)
    # рукав кофты уходит за нижний край
    g += f'<path d="M-84,96 h168 l22,150 q-102,30 -206,0 z" fill="url(#tkan)" {o(7)}/>'
    for yy in (132, 176, 220):
        g += f'<path d="M-80,{yy} q84,22 168,0" fill="none" stroke="{ob.ALYJ2}" stroke-width="9" opacity=".6"/>'
    # ладонь: от запястья до кончиков пальцев
    g += (f'<path d="M-88,100 q-32,-204 12,-266 q68,-46 152,-8 q46,42 22,274 z"'
          f' fill="url(#rush)" {o(7)}/>')
    # большой палец сбоку
    g += (f'<path d="M-84,-18 q-62,-24 -70,-84 q8,-36 44,-24 q36,14 42,68 z"'
          f' fill="url(#rush)" {o(6)}/>')
    for i in range(5):
        g += (f'<path d="M-72,{-128 + i*50} q74,22 148,0" fill="none" stroke="#cdb98d"'
              f' stroke-width="7" opacity=".5"/>')
    g += f'<ellipse cx="-24" cy="-110" rx="40" ry="26" fill="#ffffff" opacity=".22"/>'
    # верх ладони загибается вниз — «кулак»
    if szhat > .01:
        g += (f'<g transform="rotate({-88*szhat:.1f} -82 -24)">'
              f'<path d="M-88,-24 q34,-176 92,-212 q62,-22 86,46 q20,72 -4,172 q-82,28 -174,-6 z"'
              f' fill="url(#rush)" {o(7)}/>'
              f'<path d="M-62,-150 q66,24 130,2 M-70,-84 q72,24 142,0" fill="none"'
              f' stroke="#cdb98d" stroke-width="7" opacity=".55"/></g>')
    return g + "</g>"


def _listok(x, y, w_, h_, t, ph=0.0, ang=0.0, op=1.0, col="url(#list)"):
    """Чистый листок календаря/квитанция: текст на него кладёт over.py."""
    kach = 2.6 * A.w(t, 3.6, ph)
    s = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang + kach:.2f})" opacity="{op:.2f}">'
         + ten(6, h_ * .56, w_ * .5, h_ * .14, .4))
    s += (f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="7"'
          f' fill="{col}" {o(5)}/>')
    s += (f'<path d="M{w_/2 - w_*.2:.0f},{h_/2:.0f} l{w_*.2:.0f},{-h_*.2:.0f} l0,{h_*.2:.0f} z"'
          f' fill="#cdbf9f" opacity=".8"/>')
    s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} h{w_*.5:.0f} l{-w_*.5:.0f},{h_*.4:.0f} z"'
          f' fill="#ffffff" opacity=".2"/>')
    return s + "</g>"


def _kvitancia(x, y, w_, h_, ang, t, ph=0.0, op=1.0):
    """Квитанция без названий и цифр: строки только намёком."""
    s = _listok(x, y, w_, h_, t, ph, ang, op)
    s += f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f})" opacity="{op*.75:.2f}">'
    for i in range(4):
        s += (f'<line x1="{-w_*.34:.0f}" y1="{-h_*.26 + i*h_*.17:.0f}"'
              f' x2="{w_*(.3 - .07*i):.0f}" y2="{-h_*.26 + i*h_*.17:.0f}"'
              f' stroke="#9d8f74" stroke-width="5" opacity=".6"/>')
    return s + "</g>"


def _konvert(cx, cy, w_, h_, ang=0.0, op=1.0):
    s = (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.2f})" opacity="{op:.2f}">'
         + ten(5, h_ * .66, w_ * .5, h_ * .18, .42))
    s += (f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6"'
          f' fill="url(#krem)" {o(6)}/>')
    s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} L0,{h_*.12:.0f} L{w_/2:.0f},{-h_/2:.0f} z"'
          f' fill="url(#rush)" {o(5)}/>')
    s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} L0,{h_*.12:.0f} L{w_/2:.0f},{-h_/2:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="5" opacity=".35"/>')
    return s + "</g>"


def _kniga(x, y, w_, h_, t, ang=0.0):
    s = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f})">'
         + ten(6, h_ * .9, w_ * .52, h_ * .3, .5))
    s += f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="7" fill="url(#tkan)" {o(7)}/>'
    s += (f'<rect x="{-w_/2 + 10:.0f}" y="{-h_/2 + 7:.0f}" width="{w_ - 26:.0f}"'
          f' height="{h_ - 14:.0f}" rx="4" fill="url(#list)" {o(3)}/>')
    for i in range(4):
        s += (f'<line x1="{-w_/2 + 14:.0f}" y1="{-h_/2 + 14 + i*(h_-28)/4:.0f}"'
              f' x2="{w_/2 - 18:.0f}" y2="{-h_/2 + 14 + i*(h_-28)/4:.0f}"'
              f' stroke="#cdbf9f" stroke-width="3" opacity=".8"/>')
    zak = 7 * A.w(t, 2.6)
    s += (f'<path d="M{w_*.18:.0f},{-h_/2:.0f} v{h_*1.5:.0f} l{zak:.0f},18 l{-18 + zak:.0f},-18 z"'
          f' fill="{ob.ALYJ}" {o(3)}/>')
    return s + "</g>"


def _banka(x, y, s_, t, ph=0.0):
    """Чистая трёхлитровая банка: стекло с бликом и тенью."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(4, 12, 66, 14, .45)
    g += (f'<path d="M-58,0 q-10,-120 2,-168 l112,0 q12,48 2,168 z" fill="url(#stekl)"'
          f' opacity=".78" {o(6)}/>')
    g += f'<rect x="-44" y="-194" width="88" height="30" rx="8" fill="url(#stekl)" opacity=".9" {o(5)}/>'
    g += f'<ellipse cx="0" cy="-194" rx="44" ry="13" fill="#e8f3fa" opacity=".85" {o(4)}/>'
    g += f'<path d="M-38,-158 q-6,78 -2,132" fill="none" stroke="#ffffff" stroke-width="10" opacity=".5"/>'
    return g + "</g>"


def _stakan(x, y, s_, t, par_op=.5):
    """Стакан чая в подстаканнике: пар слабеет — чай остывает."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(4, 10, 46, 11, .4)
    g += f'<path d="M-40,0 l6,-118 h68 l6,118 z" fill="url(#stekl)" opacity=".7" {o(5)}/>'
    g += f'<path d="M-33,-16 l5,-86 h56 l5,86 z" fill="url(#med)" opacity=".85"/>'
    g += f'<path d="M-26,-96 q26,12 52,0" fill="none" stroke="#f2cf8c" stroke-width="6" opacity=".6"/>'
    g += f'<path d="M40,-92 q38,26 2,58" fill="none" {o(8, ZHELEZ)}/>'
    g += "</g>"
    g += baza.par(x, y - 120 * s_, t, 4, par_op, 150 * s_, .42, s_)
    return g


def _ochki(x, y, s_, t):
    bl = .3 + .7 * abs(A.w(t, 3.4))
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(4, 22, 110, 12, .4)
    for dx in (-62, 62):
        g += (f'<ellipse cx="{dx}" cy="0" rx="54" ry="38" fill="url(#stekl)" opacity=".55"'
              f' stroke="{MED}" stroke-width="8"/>')
        g += (f'<path d="M{dx-34},-16 q30,-22 60,-6" fill="none" stroke="#ffffff"'
              f' stroke-width="9" opacity="{bl:.2f}"/>')
    g += f'<path d="M-10,-4 q10,-16 20,0" fill="none" stroke="{MED}" stroke-width="8"/>'
    g += f'<path d="M-114,-10 q-46,8 -58,38" fill="none" stroke="{MED}" stroke-width="8"/>'
    return g + "</g>"


def _vedro(x, y, s_, t, kach=0.0):
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({kach:.2f}) scale({s_:.3f})">'
    g += ten(0, 12, 78, 17, .5)
    g += f'<path d="M-72,-152 h144 l-18,152 h-108 z" fill="url(#zhel)" {o(7)}/>'
    g += f'<ellipse cx="0" cy="-152" rx="72" ry="19" fill="url(#zhel)" {o(6)}/>'
    g += f'<ellipse cx="0" cy="-152" rx="57" ry="13" fill="#262c33" opacity=".6"/>'
    g += f'<path d="M-72,-170 q72,-90 144,0" fill="none" {o(9, ZHELEZ)}/>'
    g += f'<path d="M-52,-122 l10,120" fill="none" stroke="#e3ebf2" stroke-width="8" opacity=".4"/>'
    return g + "</g>"


def _korobka(x, y, w_, h_, t, ang=0.0, op=1.0):
    s = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f})" opacity="{op:.2f}">'
         + ten(6, h_ * .56, w_ * .5, h_ * .16, .45))
    s += (f'<rect x="{-w_/2:.0f}" y="{-h_/2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="6"'
          f' fill="url(#solom)" {o(6)}/>')
    s += (f'<path d="M{-w_/2:.0f},{-h_/2:.0f} h{w_:.0f} l{-w_*.16:.0f},{-h_*.3:.0f}'
          f' h{-w_*.68:.0f} z" fill="#d4b267" {o(5)}/>')
    s += (f'<line x1="0" y1="{-h_/2:.0f}" x2="0" y2="{h_/2:.0f}" stroke="#a07c2e"'
          f' stroke-width="7" opacity=".7"/>')
    return s + "</g>"


def _ochistka(x, y, ang, s_, op=1.0):
    """Картофельная кожурка: витая лента."""
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.0f}) scale({s_:.3f})"'
            f' opacity="{op:.2f}"><path d="M-44,0 q22,-30 50,-10 q28,20 48,-6"'
            f' fill="none" stroke="#b07c42" stroke-width="18" stroke-linecap="round"/>'
            f'<path d="M-44,0 q22,-30 50,-10 q28,20 48,-6" fill="none" stroke="#e4c48d"'
            f' stroke-width="7" stroke-linecap="round" opacity=".7"/></g>')


def _prischepka(x, y, ang, s_=1.0):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f}) scale({s_:.3f})">'
            f'<rect x="-13" y="-6" width="26" height="62" rx="7" fill="url(#derev)" {o(4)}/>'
            f'<rect x="-13" y="-6" width="11" height="62" rx="5" fill="#8d6440" opacity=".7"/>'
            f'<path d="M-11,10 h22" stroke="{ZHELEZ}" stroke-width="5"/></g>')


def _pyos(x, y, t, s_=1.0, col="#6b5a46"):
    hv = 28 * A.w(t, .72)
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 8, 90, 16, .45)
    g += (f'<g transform="rotate({hv:.1f} -66 -74)"><path d="M-66,-74 q-46,-26 -42,-78"'
          f' fill="none" stroke="{col}" stroke-width="18" stroke-linecap="round"/></g>')
    g += f'<ellipse cx="0" cy="-68" rx="82" ry="45" fill="{col}" {o(6)}/>'
    for nx in (-48, -16, 28, 60):
        g += f'<rect x="{nx}" y="-36" width="19" height="42" rx="9" fill="{col}" {o(4)}/>'
    g += f'<circle cx="76" cy="-114" r="37" fill="{col}" {o(6)}/>'
    g += f'<path d="M102,-106 l30,7 l-28,15 z" fill="{col}" {o(4)}/>'
    g += f'<path d="M54,-142 l-8,-36 l32,17 z" fill="{col}" {o(4)}/>'
    g += f'<circle cx="88" cy="-122" r="4.6" fill="{K}"/>'
    return g + "</g>"


def _venik(x, y, t, s_=1.0, ang=0.0):
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f}) scale({s_:.3f})">'
    g += f'<rect x="-13" y="-320" width="26" height="210" rx="12" fill="url(#derev)" {o(5)}/>'
    g += f'<path d="M-46,-120 h92 l34,138 q-80,26 -160,0 z" fill="url(#solom)" {o(6)}/>'
    r = random.Random(21)
    for i in range(13):
        dx = -52 + i * 9
        g += (f'<path d="M{dx},-116 q{r.uniform(-12,12):.0f},70 {dx*.34 + r.uniform(-16,16):.0f},142"'
              f' fill="none" stroke="#c2982f" stroke-width="5" opacity=".75"/>')
    g += f'<path d="M-48,-96 q50,16 100,0" fill="none" stroke="{ob.ALYJ2}" stroke-width="11"/>'
    return g + "</g>"


def _taz(x, y, w_, t, pena=1.0):
    """Таз с мокрым бельём: вода, бельё комками, пена оседает."""
    h_ = w_ * .34
    s = ten(x, y + h_ * .5, w_ * .55, h_ * .3, .5)
    s += (f'<path d="M{x-w_/2:.0f},{y-h_*.5:.0f} h{w_:.0f} l{-w_*.1:.0f},{h_:.0f}'
          f' h{-w_*.8:.0f} z" fill="url(#zhel)" {o(7)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.5:.0f}" rx="{w_/2:.0f}" ry="{h_*.2:.0f}"'
          f' fill="url(#zhel)" {o(6)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.48:.0f}" rx="{w_*.43:.0f}" ry="{h_*.16:.0f}"'
          f' fill="url(#voda)" opacity=".92"/>')
    for i, dx in enumerate((-.22, .04, .26)):
        s += (f'<ellipse cx="{x + dx*w_:.0f}" cy="{y-h_*.52 + 8*A.w(t,4.0,i*.3):.0f}"'
              f' rx="{w_*.15:.0f}" ry="{h_*.11:.0f}" fill="url(#krem)" opacity=".92" {o(4)}/>')
    r = random.Random(33)
    for i in range(26):
        u = (i / 26.0 + .04)
        rr = (12 + 24 * r.random()) * (.25 + .75 * pena)
        s += (f'<circle cx="{x + (u-.5)*w_*.8:.0f}"'
              f' cy="{y - h_*.5 - 10 + 14*A.w(t, 3.0, i*.14):.0f}" r="{rr:.1f}"'
              f' fill="#ffffff" opacity="{.2 + .55*pena*abs(A.w(t, 2.4, i*.11)):.2f}"/>')
    s += (f'<path d="M{x-w_*.42:.0f},{y-h_*.3:.0f} l{w_*.06:.0f},{h_*.72:.0f}"'
          f' fill="none" stroke="#e3ebf2" stroke-width="9" opacity=".4"/>')
    return s


def _boke(t, tochki, seed=5, r_=34):
    """Огоньки ёлки/гирлянды расфокусом — тёплое пятно для дальнего плана."""
    rr = random.Random(seed)
    s = ""
    for i, (bx, by) in enumerate(tochki):
        col = (SVET, ob.ALYJ, ob.ZOLOTO, "#8fd6ff")[i % 4]
        gor = .28 + .62 * (.5 + .5 * math.sin(2 * math.pi * (t / (1.8 + (i % 5) * .35) + i * .21)))
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r_ * rr.uniform(.7, 1.35):.0f}"'
              f' fill="{col}" opacity="{gor * .32:.2f}"/>')
        s += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r_*.3:.0f}" fill="{col}" opacity="{gor:.2f}"/>'
    return s


# ═══════════════════ 105 ═══════════════════
def girlyanda_iz_semi_flazhkov(t):
    """Смена главы: вдоль стены избы натянута гирлянда из семи флажков,
    бабушка и внучка стоят под ней со спины.
    Живое: номера загораются на флажках по очереди; гирлянда провисает и
    снова натягивается; огоньки за окном мигают."""
    x0, shir, y0 = 120, 1500, 210
    # провисла — потянули: вся гирлянда идёт вниз и возвращается
    dy = 54 - 54 * A.out(A.seg(t, .7, 1.5)) + 7 * A.w(t, 2.6)

    nebo_v = (f'<rect x="110" y="470" width="420" height="300" fill="{NOCH}"/>'
              + _boke(t, [(180, 690), (258, 650), (338, 712), (420, 664), (496, 718)], 3, 26)
              + baza.sneg_letit(t, 16, 9, .55))

    s = SL(Z_NEBO, _stena("#20283f", "#131a2c"))
    dal = baza.brevna(-20, 60, W + 40, 880, hh=96)
    dal += baza.okno_izby(110, 470, 420, 300, t, vid=nebo_v, moroz=.35)
    dal += baza.polovicy(905)
    s += SL(Z_DAL, dal)

    sred = baza.mebel_hlam(640, 900, 480, t, 13)
    sred += ob.elka(1700, 1015, 540, t, seed=6)
    sred += f'<g transform="translate(0,{dy:.1f})">' + ob.flazhki(x0, y0, shir, 7, t) + "</g>"
    # номера на флажках — подпись ВНУТРИ предмета, задание просит её прямо
    cx_, cy_ = x0 + shir / 2, y0 + 60
    for i in range(7):
        u = (i + .5) / 7
        fx = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx_ + u * u * (x0 + shir)
        fy = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy_ + u * u * y0 + dy
        gl = A.out(A.seg(t, 1.3 + i * .52, .42))
        if gl > .01:
            sred += (f'<circle cx="{fx:.0f}" cy="{fy + 44:.0f}" r="34" fill="{SVET}"'
                     f' opacity="{gl * .45:.2f}"/>')
            sred += (f'<text x="{fx:.0f}" y="{fy + 62:.0f}" text-anchor="middle"'
                     f' font-family="DejaVu Serif" font-size="46" font-weight="bold"'
                     f' fill="#2a1d12" opacity="{gl:.2f}">{i + 1}</text>')
    s += SL(Z_SRED, sred)

    per = ob.figura(1180, 1090, 560, t, kant="#f0c070", platok=True)
    per += ob.figura(1370, 1094, 410, t, col="#2b2030", kant="#f0c070", ph=.4)
    per += baza.ramka_pp("levo", "#0d0b14", .55)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1720, 700, 620, 520, .3) + baza.vinetka(.4))
    return s


# ═══════════════════ 106 ═══════════════════
def pustoy_karman_pidzhaka(t):
    """Крупно боковой карман праздничного пиджака на спинке стула.
    Живое: карман просвечивает и внутри пусто; нитка качается; пиджак
    покачивается на спинке."""
    kach = 1.3 * A.w(t, 4.6)
    skvoz = .10 + .20 * abs(A.w(t, 2.7))
    nit = 9 * A.w(t, 2.1)

    s = SL(Z_NEBO, _stena("#1c2439", "#101728"))
    dal = baza.okno_izby(1430, 190, 380, 300, t,
                         vid=f'<rect x="1430" y="190" width="380" height="300" fill="{NOCH}"/>'
                             + _boke(t, [(1490, 400), (1580, 350), (1680, 410), (1760, 360)], 7, 24),
                         moroz=.4)
    dal += _boke(t, [(170, 420), (250, 330), (330, 440), (120, 560), (300, 600)], 4, 54)
    dal += baza.polovicy(930)
    s += SL(Z_DAL, dal)

    sred = _g("pidzh", "#46557a", "#1a2133") + _g("podkl", "#f3e4c2", "#c3a878")
    # стул
    sred += ten(820, 1010, 420, 40, .55)
    for sx in (430, 1210):
        sred += f'<rect x="{sx}" y="190" width="40" height="740" rx="14" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="430" y="200" width="820" height="46" rx="16" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="430" y="470" width="820" height="34" rx="12" fill="url(#derev)" {o(6)}/>'
    # пиджак
    sred += f'<g transform="rotate({kach:.2f} 840 230)">'
    sred += ten(850, 955, 350, 34, .5)
    # корпус пиджака: плечи уже, пола шире
    sred += ('<path d="M560,250 q140,-70 280,-62 q150,-8 290,66 q36,330 18,650'
             ' q-156,54 -318,48 q-166,4 -300,-54 q-14,-320 30,-648 z"'
             f' fill="url(#pidzh)" {o(8)}/>')
    # воротник и лацканы клином
    sred += ('<path d="M840,188 l-120,70 l70,290 l54,-186 z" fill="#2b3450" {}/>'.format(o(6)))
    sred += ('<path d="M840,188 l122,72 l-62,288 l-56,-184 z" fill="#2b3450" {}/>'.format(o(6)))
    sred += ('<path d="M840,188 l-120,70 l34,-96 q86,-28 172,2 l36,96 z"'
             f' fill="#36426a" {o(6)}/>')
    # рукав свисает вправо
    sred += ('<path d="M1118,286 q104,56 112,196 q10,170 -34,330 q-72,24 -112,-16'
             ' q34,-250 14,-492 z" fill="#38456b" {}/>'.format(o(7)))
    # КАРМАН: ткань просвечивает, внутри пусто
    sred += f'<rect x="648" y="572" width="340" height="212" rx="18" fill="#394668" {o(7)}/>'
    sred += (f'<rect x="668" y="596" width="300" height="168" rx="12" fill="url(#podkl)"'
             f' opacity="{skvoz:.2f}"/>')
    sred += ('<path d="M668,596 h300 v168 h-300 z" fill="none" stroke="#f3e4c2"'
             f' stroke-width="4" opacity="{skvoz + .24:.2f}" stroke-dasharray="14 12"/>')
    # клапан кармана
    sred += (f'<path d="M640,534 h356 q10,34 -4,52 q-176,22 -348,0 q-14,-20 -4,-52 z"'
             f' fill="#2f3b5c" {o(6)}/>')
    sred += ('<path d="M652,546 q174,-20 334,-4" fill="none" stroke="#8ea0c6"'
             ' stroke-width="7" opacity=".45"/>')
    # нитка внутри кармана — просвечивает
    sred += (f'<path d="M712,610 q{36 + nit:.0f},78 {14 + nit*1.6:.0f},152" fill="none"'
             f' stroke="#efe0bd" stroke-width="5" opacity="{skvoz + .36:.2f}"/>')
    sred += "</g>"
    s += SL(Z_SRED, sred)

    # нитка, свисающая из угла кармана
    per = (f'<g transform="rotate({kach:.2f} 840 230)">'
           f'<path d="M972,778 q{14 + nit:.0f},80 {-10 + nit*2.1:.0f},156" fill="none"'
           f' stroke="#efe0bd" stroke-width="6" stroke-linecap="round"/>'
           f'<circle cx="{962 + nit*2.1:.0f}" cy="936" r="8" fill="#efe0bd"/></g>')
    per += baza.ramka_pp("oba", "#0b0a12", .6)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(250, 470, 440, 400, .3) + baza.vinetka(.44))
    return s


# ═══════════════════ 107, 112 ═══════════════════
def moneta_pod_tarelkoy(t):
    """Праздничный стол крупно: край тарелки приподнят, под неё сама ложится
    сложенная купюра и три монеты (рук не рисуем — правило 6).
    Живое: тарелка приподнимается; монеты ложатся; свеча рядом горит."""
    pod = A.ease(A.seg(t, .35, .95)) * (1 - .3 * A.ease(A.seg(t, 2.8, .8)))
    kx = 430 + 250 * A.ease(A.seg(t, .7, .8))

    s = SL(Z_NEBO, _stena("#1e2740", "#121a2c"))
    dal = baza.brevna(-20, 60, W + 40, 560, hh=92)
    dal += ob.girlyanda(-60, 210, W + 60, 230, t, 14, 120)
    dal += _boke(t, [(180, 390), (330, 330), (1600, 360), (1780, 300)], 8, 46)
    s += SL(Z_DAL, dal)

    sred = ob.stol_prazdnik(-80, 620, W + 160, t)
    sred += (f'<rect y="654" width="{W}" height="{H - 654}" fill="url(#rush)"/>')
    sred += (f'<path d="M0,690 q480,46 960,10 q480,-36 960,28" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".4"/>')
    sred += baza.svecha(1560, 480, t, .2, 1.7, 100)
    sred += ob.bokal(1760, 660, t, .9, .3)
    sred += ob.mandarin(190, 640, 1.2, .4, t)
    s += SL(Z_SRED, sred)

    per = ""
    # купюра въезжает под приподнятый край тарелки
    per += _kupyura(kx, 760, 290, 132, -7, min(1.0, A.seg(t, .7, .4)), slozh=True)
    # три монеты ложатся одна за другой
    for i in range(3):
        k = A.out(A.seg(t, 1.05 + i * .32, .5))
        if k > .01:
            per += _moneta(500 + i * 104, 836 - 210 * (1 - k), 38, 23, t, i * .3, min(1.0, k * 1.6))
    per += _tarelka(1080, 724, 340, t, pod)
    per += baza.ramka_pp("levo", "#0c0a10", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1500, 520, 520, 450, .34) + baza.vinetka(.4))
    return s


# ═══════════════════ 108 ═══════════════════
def moneta_katitsya_cherez_god(t):
    """От тарелки монета катится по дорожке из двенадцати плиток-месяцев.
    Живое: монета катится; на пройденных плитках остаются монетки; плитки
    подсвечиваются одна за другой."""
    p = A.ease(A.seg(t, .3, 6.0))
    cur = p * 12.0
    bx0, shag = 196, 134

    s = SL(Z_NEBO, _stena("#232b44", "#121a2c"))
    dal = baza.brevna(-20, 40, W + 40, 560, hh=94)
    dal += ob.elka(1700, 640, 430, t, seed=9)
    dal += ob.girlyanda(-60, 130, W + 60, 150, t, 15, 110)
    dal += _boke(t, [(210, 330), (350, 270), (120, 440)], 8, 48)
    s += SL(Z_DAL, dal)

    sred = _g("plit", "#9a8d78", "#52483a")
    sred += (f'<rect y="640" width="{W}" height="{H - 640}" fill="url(#rush)"/>')
    sred += (f'<rect y="640" width="{W}" height="20" fill="#cdb98d"/>')
    sred += (f'<path d="M0,742 q480,44 960,8 q480,-34 960,26" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".3"/>')
    for i in range(12):
        x = bx0 + i * shag
        y = 862 - i * 4
        w_ = 132 - i * 1.6
        gor = 1.0 if cur > i + .35 else (.24 + .5 * A.seg(t, .3 + i * .45, .3))
        sred += ten(x + 6, y + 34, w_ * .55, 16, .45)
        sred += (f'<rect x="{x - w_/2:.0f}" y="{y - 26:.0f}" width="{w_:.0f}" height="52"'
                 f' rx="10" fill="url(#plit)" {o(5)}/>')
        sred += (f'<rect x="{x - w_/2 + 8:.0f}" y="{y - 19:.0f}" width="{w_ - 16:.0f}"'
                 f' height="38" rx="7" fill="{ob.ZOLOTO}" opacity="{.18 + .55*gor:.2f}"/>')
        sred += (f'<path d="M{x - w_/2 + 11:.0f},{y - 14:.0f} h{w_*.5:.0f}" fill="none"'
                 f' stroke="#ffffff" stroke-width="5" opacity="{.22 + .4*gor:.2f}"/>')
        if gor > .9:
            sred += baza.teplo(x, y, w_ * .9, 70, .3)
        if cur > i + .6:
            pop = A.out(min(1.0, (cur - i - .6) * 3.2))
            sred += _moneta(x, y - 36, 22 * pop, 14 * pop, t, i * .17, 1.0, False)
    s += SL(Z_SRED, sred)

    per = _tarelka(120, 838, 250, t, .2)
    mx = bx0 + 46 + cur * shag
    my = 808 - cur * 4
    rx = 11 + 41 * abs(math.cos(cur * 2.3))
    per += ten(mx + 4, my + 60, 44, 15, .5)
    per += (f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{rx:.1f}" ry="46" fill="url(#zol)" {o(6)}/>')
    per += (f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{rx*.55:.1f}" ry="27" fill="none"'
            f' stroke="{ob.ZOLOTO2}" stroke-width="5" opacity=".65"/>')
    per += (f'<ellipse cx="{mx - rx*.25:.0f}" cy="{my - 16:.0f}" rx="{rx*.3:.1f}" ry="12"'
            f' fill="#fff8de" opacity="{.4 + .6*abs(A.w(t, 1.2)):.2f}"/>')
    per += baza.teplo(mx, my, 180, 160, .45)
    per += baza.ramka_pp("levo", "#0c0b12", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.42))
    return s


# ═══════════════════ 109 ═══════════════════
def tri_monetki_na_ladoni(t):
    """Крупно раскрытая вязаная варежка (ладонь играет предмет — правило 6),
    на ней три мелкие монетки.
    Живое: монетки пересчитываются по одной; ладонь закрывается; рукав
    кофты подрагивает."""
    szhat = A.ease(A.seg(t, 2.45, .85))
    schet = (t * 1.15) % 3.3

    s = SL(Z_NEBO, _stena("#232b42", "#141a2b"))
    dal = baza.brevna(-20, 40, W + 40, 700, hh=98)
    dal += baza.lampa(1560, 560, t, 1.25, abazhur=True)
    dal += _boke(t, [(250, 300), (360, 240), (170, 400)], 6, 48)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 830, W + 120, 46, False)
    sred += (f'<path d="M-60,876 h{W+120} v140 q-520,50 -1040,8 q-460,-38 -1040,16 z"'
             f' fill="url(#rush)" {o(6)}/>')
    sred += _varezhka(800, 820, 2.2, t, szhat, .0, False, 2.2)
    s += SL(Z_SRED, sred)

    per = ""
    for i in range(3):
        aktiv = 1.0 if (i <= schet < i + 1) else 0.0
        podn = 20 * aktiv * abs(A.w(t, .9, i * .2))
        op = max(0.0, 1.0 - A.seg(t, 2.55 + i * .06, .3))
        per += _moneta(680 + i * 120, 560 - podn, 48, 30, t, i * .33, op)
        if aktiv and op > .3:
            per += baza.teplo(680 + i * 120, 560 - podn, 130, 110, .45)
    per += baza.ramka_pp("oba", "#0c0b13", .55)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1540, 620, 640, 520, .3) + baza.vinetka(.46))
    return s


# ═══════════════════ 110 ═══════════════════
def rebenok_zaglyadyvaet_pod_tarelku(t):
    """МОСТИК В ПАМЯТЬ: край стола на уровне детских глаз, тарелка сама
    приподнимается и под ней блестит монета.
    Живое: тарелка приподнимается; монета блестит; ребёнок подаётся вперёд."""
    pod = A.ease(A.seg(t, .5, 1.0))
    vper = A.ease(A.seg(t, .9, 1.3))
    bl = .35 + .65 * abs(A.w(t, 1.5))

    s = SL(Z_NEBO, _stena("#4a3524", "#1d1510"))
    dal = baza.brevna(-20, 30, W + 40, 560, hh=96)
    dal += ob.elka(1680, 690, 430, t, seed=12)
    dal += ob.figura(1330, 700, 470, t, col="#2a2018", kant="#f2c47c", platok=True, ph=.3)
    dal += _boke(t, [(210, 250), (340, 200), (120, 330)], 2, 52)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 600, W + 120, 54, False)
    sred += (f'<rect y="654" width="{W}" height="{H - 654}" fill="url(#rush)"/>')
    sred += (f'<path d="M0,712 q480,44 960,8 q480,-34 960,26" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="7" opacity=".35"/>')
    sred += _moneta(760, 640, 52, 30, t, .1)
    sred += baza.teplo(760, 636, 210, 150, .34 + .3 * bl)
    sred += _tarelka(1090, 616, 310, t, pod)
    s += SL(Z_SRED, sred)

    # ребёнок со спины снизу слева: тёмная масса, лиц не рисуем
    rx = 330 + 54 * vper
    ry = 1010 - 36 * vper
    per = ten(rx, 1070, 250, 30, .6)
    per += (f'<path d="M{rx-250:.0f},{H + 20} q10,-230 70,-300 q120,-96 300,-30'
            f' q90,54 96,330 z" fill="#1a1410" stroke="#f2c47c" stroke-width="5"'
            f' stroke-opacity=".55"/>')
    per += (f'<circle cx="{rx + 6:.0f}" cy="{ry - 250:.0f}" r="118" fill="#1a1410"'
            f' stroke="#f2c47c" stroke-width="5" stroke-opacity=".55"/>')
    per += baza.ramka_pp("pravo", "#120d09", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(900, 560, 900, 700, .3) + baza.vinetka(.52))
    return s


# ═══════════════════ 113 ═══════════════════
def moneta_v_karmashek_vnuka(t):
    """Монеты сами падают в нагрудные кармашки двоих внуков, клапаны
    прихлопываются, а дальше вглубь уходит цепь маленьких фигурок с монетками.
    Живое: монеты падают в кармашки; клапаны прихлопывают; фигурки бегут вдаль."""
    deti = ((540, 1020, 540, .0), (880, 1026, 490, .45))

    s = SL(Z_NEBO, _stena("#2a3049", "#161c2e"))
    dal = baza.brevna(-20, 40, W + 40, 820, hh=96)
    dal += baza.dver(1540, 190, 330, 760, .35, kruchok=True)
    dal += baza.teplo(1700, 560, 360, 440, .5)
    # цепь фигурок уходит вдаль
    for j in range(7):
        u = ((t * .2 + j / 7.0) % 1.0)
        fx = 1120 + u * 700
        fb = 980 - u * 320
        fh = 270 * (1 - u * .74)
        op = max(.1, 1 - u * .72)
        dal += ob.figura(fx, fb, fh, t, col="#232a3e", kant="#e7b96e", ph=j * .21, op=op)
        dal += _moneta(fx + fh * .12, fb - fh * .5, fh * .07, fh * .045, t, j * .2, op, False)
    dal += baza.polovicy(950)
    s += SL(Z_DAL, dal)

    sred = ""
    for i, (x, b, h_, ph) in enumerate(deti):
        sred += ob.figura(x, b, h_, t, col="#2d2335", kant="#f0c070", ph=ph)
    s += SL(Z_SRED, sred)

    per = ""
    for i, (x, b, h_, ph) in enumerate(deti):
        px, py = x + h_ * .12, b - h_ * .54
        pw, phh = h_ * .2, h_ * .15
        # кармашек
        per += (f'<rect x="{px - pw/2:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{phh:.0f}"'
                f' rx="7" fill="url(#rush)" {o(5)}/>')
        per += (f'<path d="M{px - pw/2 + 8:.0f},{py + phh*.55:.0f} h{pw - 16:.0f}" fill="none"'
                f' stroke="#cdb98d" stroke-width="5" opacity=".7"/>')
        k = A.out(A.seg(t, .9 + i * 1.2, .7))
        if k < 1.0:
            per += _moneta(px, py + phh * .4 - 360 * (1 - k), 26, 26, t, i * .4, 1.0, False)
        klap = A.ease(A.seg(t, 1.65 + i * 1.2, .45))
        per += (f'<g transform="rotate({-78 + 78*klap:.1f} {px - pw/2:.0f} {py:.0f})">'
                f'<rect x="{px - pw/2:.0f}" y="{py - 5:.0f}" width="{pw:.0f}" height="{phh*.46:.0f}"'
                f' rx="6" fill="#bda47a" {o(5)}/></g>')
    per += baza.ramka_pp("levo", "#0c0b13", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.42))
    return s


# ═══════════════════ 115, 116 ═══════════════════
def protyanutaya_i_zakrytaya_ladon(t):
    """Плашка второго запрета: над столом раскрытая варежка-ладонь тянется
    вперёд, вторая сжимается в кулак над купюрой и покачивает отказом.
    Позади на прищепках два чистых листка — текст на них кладёт over.py.
    Живое: ладонь протягивается; кулак закрывается; листки покачиваются."""
    dx = 120 * A.ease(A.seg(t, .4, 1.0))
    szhat = A.ease(A.seg(t, 1.35, .9))
    otkaz = 8 * A.w(t, 1.05) * A.seg(t, 2.2, .7)

    s = SL(Z_NEBO, _stena("#222a42", "#131a2b"))
    dal = baza.brevna(-20, 30, W + 40, 620, hh=96)
    dal += (f'<path d="M820,186 q320,44 980,-6" fill="none" stroke="#5a4c38" stroke-width="6"/>')
    for i, lx in enumerate((1040, 1480)):
        dal += _prischepka(lx, 196 + i * 10, -4 + 3 * A.w(t, 4.2, i * .3), 1.1)
        dal += _listok(lx, 372 + i * 8, 310, 250, t, i * .35, -3 + 4 * A.w(t, 4.0, i * .3))
    dal += baza.lampa(420, 440, t, 1.1, abazhur=True)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 780, W + 120, 44, False)
    sred += (f'<rect y="824" width="{W}" height="{H - 824}" fill="url(#rush)"/>')
    sred += (f'<path d="M0,878 q480,42 960,8 q480,-32 960,24" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="6" opacity=".35"/>')
    s += SL(Z_SRED, sred)

    per = _varezhka(400 + dx, 902, 1.35, t, .0, .2, False, 2.4)
    per += _kupyura(1260, 772, 300, 138, -5)
    per += (f'<g transform="rotate({otkaz:.2f} 1260 900)">'
            + _varezhka(1260, 876, 1.35, t, szhat, .55, True, 1.4) + "</g>")
    per += baza.ramka_pp("oba", "#0b0a12", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(430, 520, 560, 460, .3) + baza.vinetka(.44))
    return s


# ═══════════════════ 117 ═══════════════════
def blagopoluchie_uhodit_za_kupyuroy(t):
    """Купюра уходит за дверь, и за ней на золотой нити тянется из дома
    каравай, свет лампы и румянец яблок.
    Живое: золотая нить тянется за дверь; свет лампы тускнеет; яблоки бледнеют."""
    uh = A.ease(A.seg(t, .1, 1.9))
    kx = 880 + 700 * uh
    ky = 540 - 60 * uh
    gasnet = A.ease(A.seg(t, .35, 1.6))
    yabl = _mix(ob.ALYJ, "#98918a", A.ease(A.seg(t, .55, 1.5)))

    s = SL(Z_NEBO, _stena("#232b42", "#141b2c"))
    dal = baza.brevna(-20, 30, W + 40, 900, hh=96)
    dal += baza.dver(1480, 160, 380, 800, .55, kruchok=True)
    dal += (f'<rect x="1480" y="160" width="190" height="800" fill="#9ec8e8" opacity=".3"/>')
    dal += baza.polovicy(958)
    s += SL(Z_DAL, dal)

    sred = baza.lampa(620, 420, t, 1.2, abazhur=True)
    sred += (f'<ellipse cx="620" cy="620" rx="420" ry="330" fill="url(#teplo)"'
             f' opacity="{.75 * (1 - .7*gasnet):.2f}"/>')
    sred += baza.stol(120, 700, 900, 40)
    sred += baza.karavay(430, 690, 1.5)
    for i, ax in enumerate((700, 800, 756)):
        ay = 686 - (26 if i == 2 else 0)
        sred += ten(ax + 3, ay + 30, 42, 11, .4)
        sred += f'<circle cx="{ax}" cy="{ay}" r="40" fill="{yabl}" {o(5)}/>'
        sred += (f'<circle cx="{ax-13}" cy="{ay-14}" r="12" fill="#ffffff" opacity=".35"/>')
        sred += (f'<path d="M{ax},{ay-40} q8,-16 22,-14" fill="none" stroke="{ZEL}"'
                 f' stroke-width="6" stroke-linecap="round"/>')
    s += SL(Z_SRED, sred)

    per = ""
    for i, (sx, sy) in enumerate(((430, 650), (620, 500), (756, 660))):
        per += (f'<path d="M{sx},{sy} Q{(sx + kx)/2:.0f},{sy - 160 - i*50:.0f} {kx:.0f},{ky:.0f}"'
                f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="{7 - i}"'
                f' stroke-linecap="round" stroke-dasharray="26 16"'
                f' stroke-dashoffset="{-t * 120:.0f}" opacity="{.35 + .5*uh:.2f}"/>')
    per += _kupyura(kx, ky, 300, 138, -11 + 16 * uh, max(0.0, 1.0 - A.seg(t, 1.5, .8)))
    per += baza.ramka_pp("levo", "#0b0a12", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.46))
    return s


# ═══════════════════ 118 ═══════════════════
def sosed_vozvraschaet_dolg_u_zabora(t):
    """Зимний день у плетня: три монеты сами перелетают через забор к хозяйке,
    на столбе стоит пустая кринка, оба кланяются.
    Живое: монеты переходят из рук в руки; пар изо рта; пёс виляет хвостом."""
    poklon_a = -7 * A.ease(A.seg(t, 2.4, .5)) * (1 - A.ease(A.seg(t, 3.1, .5)))
    poklon_b = 7 * A.ease(A.seg(t, 2.5, .5)) * (1 - A.ease(A.seg(t, 3.2, .5)))

    s = SL(Z_NEBO, baza.nebo("den", t) + baza.oblaka(t, 180, 5, 7, .55))
    dal = baza.ulica_dal(60, 640, 1800, t)
    dal += baza.izba_snaruzhi(1320, 690, 520, t)
    dal += baza.sneg_lezhit(690, 30)
    s += SL(Z_DAL, dal)

    sred = baza.pleten(230, 880, 1460, 210, 11)
    sred += baza.krynka(900, 700, 1.25)
    sred += (f'<g transform="rotate({poklon_a:.2f} 520 920)">'
             + ob.figura(520, 920, 580, t, col="#3b3026", kant="#ffe2a8") + "</g>")
    sred += (f'<g transform="rotate({poklon_b:.2f} 1250 920)">'
             + ob.figura(1250, 920, 556, t, col="#33283a", kant="#ffe2a8", platok=True, ph=.4) + "</g>")
    sred += baza.par(560, 690, t, 4, .5, 150, .4, .9)
    sred += baza.par(1210, 700, t, 4, .45, 140, .38, .85)
    s += SL(Z_SRED, sred)

    per = ""
    for i in range(3):
        u = A.ease(A.seg(t, .6 + i * .45, .95))
        if u > .01:
            mx = 660 + 450 * u
            my = 740 - 190 * math.sin(math.pi * u)
            per += _moneta(mx, my, 30, 30, t, i * .3, 1.0, False)
    per += _pyos(1640, 960, t, 1.05)
    per += baza.sneg_lezhit(1010, 22)
    per += baza.ramka_pp("levo", "#1b2434", .45)
    s += SL(Z_PERED, per)
    s += baza.sneg_letit(t, 34, 5, .55, .7)
    s += SL(Z_FIX, baza.vinetka(.34))
    return s


# ═══════════════════ 119 ═══════════════════
def svetyaschiysya_porog_novogo_goda(t):
    """Дверной проём, за ним свет. Человек со спины подходит к порогу, мешок
    с биркой сам сползает с плеч (бирку надписывает over.py).
    Живое: мешок сползает с плеч; свет из проёма льётся; человек распрямляется."""
    idet = A.ease(A.seg(t, .2, 2.5))
    fx = 700 + 250 * idet
    rovno = A.ease(A.seg(t, 1.5, 1.1))
    sk = A.ease(A.seg(t, .95, 1.15))
    puls = .8 + .2 * abs(A.w(t, 2.4))

    s = SL(Z_NEBO, _stena("#f6e6bf", "#e0b878"))
    dal = _g("proem", "#fff6dc", "#f0c878")
    dal += f'<rect width="{W}" height="{H}" fill="#19202f"/>'
    dal += (f'<path d="M790,1080 V380 q270,-230 540,0 V1080 z" fill="url(#proem)"'
            f' opacity="{puls:.2f}"/>')
    dal += baza.teplo(1060, 640, 620, 620, .8 * puls)
    dal += baza.brevna(-20, 0, 800, 1080, hh=100)
    dal += baza.brevna(1330, 0, 620, 1080, hh=100)
    dal += (f'<path d="M790,1080 V380 q270,-230 540,0 V1080" fill="none" stroke="{K}"'
            f' stroke-width="14"/>')
    s += SL(Z_DAL, dal)

    sred = baza.luch(820, 380, 460, 700, t, .26 * puls)
    sred += (f'<rect x="790" y="986" width="540" height="42" rx="10" fill="url(#derev)" {o(7)}/>')
    sred += ob.figura(fx, 1010, 640 + 60 * rovno, t, col="#201a26", kant="#ffd79a")
    s += SL(Z_SRED, sred)

    # мешок сползает с плеч и остаётся у порога
    mx = fx - 150 + 24 * sk
    my = 1010 - 470 + 430 * sk
    rot = 26 * sk
    per = (f'<g transform="translate({mx:.1f},{my:.1f}) rotate({rot:.1f})">'
           + ten(0, 96, 100, 22, .55)
           + f'<path d="M-96,88 q-24,-150 16,-196 q70,-34 148,2 q34,52 10,194 z"'
             f' fill="url(#solom)" {o(7)}/>'
           + f'<path d="M-80,-104 q78,-36 156,-2" fill="none" stroke="{ob.ALYJ2}" stroke-width="12"/>'
           + f'<path d="M-40,-116 q40,-28 84,-4" fill="none" stroke="#8a6a3a" stroke-width="9"/>'
           + f'<path d="M62,-96 q46,26 44,70" fill="none" stroke="#6b4428" stroke-width="6"/>'
           + _listok(118, 2, 104, 76, t, .2, 9) + "</g>")
    per += baza.ramka_pp("oba", "#0b0a10", .72)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.4))
    return s


# ═══════════════════ 120 ═══════════════════
def zanyatoe_nesut_sosedke(t):
    """Лестничная площадка: стопка — книга с закладкой, чистая трёхлитровая
    банка и конверт — плывёт к открывающейся двери, соседка в дверях всплёскивает.
    Живое: банка покачивается на книге; дверь открывается; соседка всплёскивает."""
    otkr = A.ease(A.seg(t, .8, 1.5))
    kach = 4.2 * A.w(t, 2.2)
    vspl = A.ease(A.seg(t, 2.1, .6))
    dyf = -26 * vspl * (1 - .4 * A.ease(A.seg(t, 3.4, .8)))

    s = SL(Z_NEBO, _stena("#39414a", "#20262e"))
    dal = f'<rect y="0" width="{W}" height="980" fill="url(#beton)"/>'
    dal += (f'<rect y="560" width="{W}" height="22" fill="{BETON2}" opacity=".8"/>')
    for i in range(5):
        dal += (f'<rect x="-40" y="{980 + i*26:.0f}" width="{W+80}" height="26"'
                f' fill="{BETON2 if i % 2 else BETON}" opacity=".9" stroke="{K}" stroke-width="3"/>')
    dal += (f'<path d="M80,640 q0,-120 120,-120 h380" fill="none" stroke="{ZHELEZ}"'
            f' stroke-width="16" stroke-linecap="round"/>')
    dal += (f'<circle cx="1000" cy="130" r="42" fill="{SVET}"'
            f' opacity="{.6 + .35*abs(A.w(t, 5.2)):.2f}"/>')
    dal += baza.teplo(1000, 150, 420, 340, .45)
    s += SL(Z_DAL, dal)

    sred = (f'<rect x="1180" y="170" width="430" height="810" fill="{SVET}"'
            f' opacity="{.34*otkr:.2f}"/>')
    sred += baza.dver(1180, 170, 430, 810, otkr * .62, kruchok=True)
    sred += (f'<g transform="translate(0,{dyf:.1f}) rotate({5*vspl*A.w(t,1.1):.2f} 1370 1000)">'
             + ob.figura(1370, 1000, 610, t, col="#2e2436", kant="#f0c070", platok=True) + "</g>")
    s += SL(Z_SRED, sred)

    bx, by = 580, 880
    per = _kniga(bx, by, 430, 104, t, 1.4 * A.w(t, 3.0))
    per += f'<g transform="rotate({kach:.2f} {bx:.0f} {by - 52:.0f})">'
    per += _banka(bx + 12, by - 56, 1.55, t)
    per += _konvert(bx + 18, by - 400, 300, 196, -6 + .6 * kach)
    per += "</g>"
    per += baza.ramka_pp("levo", "#14181e", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.44))
    return s


# ═══════════════════ 121, 122 ═══════════════════
def stopka_kvitanciy(t):
    """Кухонный стол: веер чистых квитанций под магнитом-мандарином, они сами
    перелетают по одной в стопку «готово».
    Живое: квитанции перекладываются; блик бежит по очкам; чай в стакане остывает."""
    s = SL(Z_NEBO, _stena("#2b3348", "#171e2e"))
    dal = baza.doski(-20, 40, W + 40, 640, 150, True, "dosk")
    dal += baza.okno_izby(1380, 150, 440, 350, t,
                          vid=f'<rect x="1380" y="150" width="440" height="350" fill="{NOCH}"/>'
                              + _boke(t, [(1450, 400), (1560, 350), (1680, 420), (1770, 340)], 5, 26)
                              + baza.sneg_letit(t, 14, 4, .5),
                          moroz=.45)
    dal += baza.polka(180, 330, 520)
    for i in range(3):
        dal += baza.krynka(280 + i * 170, 324, .72)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 720, W + 120, 46, False)
    sred += (f'<path d="M-60,766 h{W+120} v120 q-520,52 -1040,10 q-460,-40 -1040,16 z"'
             f' fill="url(#rush)" {o(6)}/>')
    sred += _stakan(1180, 712, 1.25, t, .52 * (1 - .62 * A.seg(t, 0, 4.2)))
    sred += _ochki(820, 790, 1.15, t)
    s += SL(Z_SRED, sred)

    per = ""
    gotovo = 0
    for i in range(6):
        k = A.ease(A.seg(t, .55 + i * .6, .55))
        ang0 = -30 + i * 11
        x0, y0 = 450, 700
        x1, y1 = 1480, 706 - i * 9
        x = x0 + (x1 - x0) * k
        y = y0 + (y1 - y0) * k - 160 * math.sin(math.pi * k)
        ang = ang0 + (4 - ang0) * k
        per += _kvitancia(x, y, 260, 200, ang, t, i * .2)
        if k > .98:
            gotovo += 1
    per += ob.mandarin(452, 648, 1.0, .0, t)
    per += (f'<rect x="1340" y="{728 - gotovo*9:.0f}" width="280" height="14" rx="6"'
            f' fill="{MED}" opacity=".45"/>')
    per += baza.ramka_pp("levo", "#0d0c14", .48)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1600, 360, 520, 420, .26) + baza.vinetka(.44))
    return s


# ═══════════════════ 123 ═══════════════════
def zapiska_na_vtoroe_yanvarya(t):
    """Прихожая: на зеркало сама прикрепляется чистая записка (текст кладёт
    over.py), листки календаря отлетают, и конверт уходит в приоткрытую дверь.
    Живое: записка прикрепляется; листки отлетают; конверт уходит к соседу."""
    pri = A.over(A.seg(t, .3, .65))
    snyat = A.seg(t, 4.0, .4)
    kon = A.ease(A.seg(t, 4.3, 2.0))

    s = SL(Z_NEBO, _stena("#2a3148", "#161c2c"))
    dal = baza.doski(-20, 20, W + 40, 700, 160, True, "dosk")
    dal += (f'<path d="M1180,200 h620" fill="none" stroke="{ZHELEZ}" stroke-width="14"/>')
    for i, hx in enumerate((1270, 1400, 1530)):
        dal += (f'<path d="M{hx},200 v44" fill="none" stroke="{ZHELEZ}" stroke-width="8"/>')
        dal += (f'<path d="M{hx-56},250 q56,-30 112,0 l26,270 q-82,30 -164,0 z"'
                f' fill="{[TKAN2, ZEL, TKAN][i]}" opacity=".9" {o(6)}/>')
    dal += (f'<rect x="1600" y="150" width="310" height="830" fill="{SVET}" opacity=".2"/>')
    dal += baza.dver(1600, 150, 310, 830, .35 + .25 * A.ease(A.seg(t, 4.0, 1.2)), kruchok=True)
    dal += ob.figura(1790, 962, 520, t, col="#2a2234", kant="#f0c070", op=.9)
    dal += baza.polovicy(975)
    s += SL(Z_DAL, dal)

    sred = ten(650, 790, 260, 28, .5)
    sred += (f'<rect x="398" y="178" width="504" height="604" rx="18" fill="url(#med)" {o(8)}/>')
    sred += (f'<rect x="428" y="208" width="444" height="544" rx="10" fill="url(#stekl)"'
             f' opacity=".9" {o(5)}/>')
    sred += (f'<g clip-path="url(#zerk)"><clipPath id="zerk"><rect x="428" y="208"'
             f' width="444" height="544" rx="10"/></clipPath>'
             + _boke(t, [(520, 560), (640, 470), (760, 580), (700, 330), (540, 350)], 9, 44)
             + f'<path d="M428,640 h444 v112 h-444 z" fill="{SVET}" opacity=".12"/></g>')
    sred += (f'<path d="M444,230 l180,300" fill="none" stroke="#ffffff" stroke-width="16"'
             f' opacity=".22"/>')
    # календарь
    sred += ten(1060, 640, 130, 20, .45)
    sred += f'<rect x="950" y="270" width="230" height="330" rx="12" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="968" y="306" width="194" height="280" rx="8" fill="url(#list)" {o(5)}/>'
    for i in range(3):
        k = A.ease(A.seg(t, 1.5 + i * .5, .85))
        if k < .99:
            sred += _listok(1065 + 420 * k, 446 - 230 * k, 190, 272, t, i * .3,
                            -6 + 230 * k, max(0.0, 1 - k * 1.15))
    s += SL(Z_SRED, sred)

    per = ""
    if pri > .02 and snyat < 1.0:
        per += (f'<g transform="translate(652,392) scale({pri:.3f}) translate(-652,{-392 - 54*snyat:.0f})">'
                + _listok(652, 392, 282, 240, t, .1, -5, 1 - snyat, "#f6e6a8") + "</g>")
    per += _konvert(900 + 760 * kon, 760 - 200 * math.sin(math.pi * kon), 250, 162,
                    -8 + 20 * kon, 1.0 if kon > .02 else 0.0)
    per += baza.ramka_pp("levo", "#0c0b13", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1790, 540, 420, 520, .26) + baza.vinetka(.44))
    return s


# ═══════════════════ 124 ═══════════════════
def paket_v_ruke_u_nochnoy_dveri(t):
    """Плашка третьего запрета: ночь, дверь квартиры приоткрыта, человек в
    тапочках замер на пороге, пакет висит у него сбоку, часы на двенадцати.
    Живое: пакет покачивается; дверь поскрипывает; стрелки часов на двенадцати."""
    skrip = .42 + .05 * A.w(t, 2.3) + .03 * A.w(t, 5.7, .3)
    kach = 7.5 * A.w(t, 2.15)

    s = SL(Z_NEBO, _stena("#1a2033", "#0d1220"))
    dal = baza.doski(-20, 10, W + 40, 740, 162, True, "dosk")
    dal += ob.kuranty(1430, 400, t, .92, 1.0, True)
    dal += (f'<path d="M1700,220 v420" fill="none" stroke="{ZHELEZ}" stroke-width="10"/>')
    dal += (f'<path d="M1644,266 q56,-30 112,0 l24,250 q-80,28 -160,0 z" fill="{TKAN2}"'
            f' opacity=".85" {o(6)}/>')
    dal += baza.polovicy(958)
    s += SL(Z_DAL, dal)

    sred = (f'<rect x="150" y="150" width="440" height="830" fill="#8fb6cf" opacity=".32"/>')
    sred += baza.dver(150, 150, 440, 830, skrip, kruchok=True, cepochka=True)
    sred += (f'<path d="M590,150 l150,-30 v890 l-150,-40 z" fill="#9ec8e8" opacity=".2"/>')
    sred += baza.teplo(640, 560, 420, 520, .22)
    s += SL(Z_SRED, sred)

    per = ob.figura(870, 1050, 760, t, col="#1b1726", kant="#9ec8e8")
    for dx in (-78, 30):
        per += ten(870 + dx + 30, 1056, 70, 16, .55)
        per += (f'<path d="M{870+dx:.0f},1046 q58,-34 116,-4 q6,28 -40,34 q-66,6 -76,-30 z"'
                f' fill="#3c3140" stroke="#9ec8e8" stroke-width="4" stroke-opacity=".6"/>')
    per += _g("paket", "#dbe3ec", "#8d99a7")
    per += (f'<g transform="rotate({kach:.2f} 1104 640)">'
            f'<path d="M1104,640 l-34,42 M1104,640 l34,42" fill="none" stroke="#b7c2cd" stroke-width="9"/>'
            f'{ten(1108, 952, 96, 20, .5)}'
            f'<path d="M1034,676 h140 l30,250 q-100,34 -200,0 z" fill="url(#paket)" opacity=".92" {o(6)}/>'
            f'<path d="M1052,712 q52,22 104,0 M1046,800 q58,24 116,0" fill="none"'
            f' stroke="#ffffff" stroke-width="7" opacity=".45"/>'
            f'<path d="M1080,700 q22,110 10,208" fill="none" stroke="#6f7b88"'
            f' stroke-width="6" opacity=".5"/></g>')
    per += baza.ramka_pp("pravo", "#0a0912", .6)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.52))
    return s


# ═══════════════════ 125 ═══════════════════
def venik_metet_ot_poroga(t):
    """Деревенская горница: веник метёт сор не к двери, а ОТ порога в угол к
    печи; порог остаётся чистым и закрытым.
    Живое: веник метёт; сор собирается в кучку; кот прыгает за веником."""
    hod = .5 + .5 * A.w(t, 2.6)
    vx = 540 + 460 * hod
    kucha = min(1.0, t / 4.4)
    pryg = max(0.0, math.sin(2 * math.pi * (t / 2.2))) ** 3

    s = SL(Z_NEBO, _stena("#232b40", "#141a2a"))
    dal = baza.brevna(-20, 20, W + 40, 820, hh=96)
    dal += baza.okno_izby(240, 210, 390, 310, t,
                          vid=f'<rect x="240" y="210" width="390" height="310" fill="{NOCH}"/>'
                              + baza.sneg_letit(t, 16, 6, .5),
                          moroz=.8)
    dal += baza.utvar_izby(700, 340, 520, t, 4)
    s += SL(Z_DAL, dal)

    sred = baza.pech(1260, 330, 580, 650, t)
    sred += baza.dver(60, 250, 320, 720, 0.0, kruchok=True)
    sred += baza.polovicy(910)
    # чистый порог
    sred += (f'<rect x="60" y="930" width="330" height="40" rx="10" fill="url(#derev)" {o(6)}/>')
    sred += (f'<rect x="72" y="938" width="306" height="14" rx="6" fill="#ffffff" opacity=".3"/>')
    s += SL(Z_SRED, sred)

    per = _venik(vx, 1000, t, 1.15, -20 + 28 * hod)
    # сор летит в кучку у печи
    r = random.Random(17)
    for i in range(11):
        u = min(1.0, max(0.0, (t - .4 - i * .3) / 1.6))
        sx = vx - 60 + r.uniform(-60, 60) + (1340 - vx + 60) * u
        sy = 1000 + r.uniform(-8, 8) - 26 * math.sin(math.pi * u)
        per += (f'<ellipse cx="{sx:.0f}" cy="{sy:.0f}" rx="{r.uniform(7,14):.0f}"'
                f' ry="{r.uniform(4,8):.0f}" fill="#8b6f3f" opacity=".85"/>')
    per += ten(1360, 1004, 140 * kucha + 30, 20, .5)
    per += (f'<path d="M{1360 - 150*kucha - 30:.0f},1004 q{75*kucha + 15:.0f},{-70*kucha - 16:.0f}'
            f' {150*kucha + 30:.0f},0 z" fill="#8b6f3f" {o(5)}/>')
    per += f'<g transform="translate(0,{-110*pryg:.0f})">' + baza.kot(vx + 250, 980, t, .92) + "</g>"
    per += baza.ramka_pp("levo", "#0c0b12", .5)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.teplo(1540, 700, 620, 520, .36) + baza.vinetka(.42))
    return s


# ═══════════════════ 127 ═══════════════════
def dvor_s_kalitkoy_dnem(t):
    """РАЗВИЛКА, свой двор: ясный зимний день, низкое солнце, хозяин в валенках
    идёт с ведром по расчищенной дорожке к калитке.
    Живое: ведро покачивается; калитка открывается; солнце блестит на снегу."""
    idet = A.ease(A.seg(t, .3, 4.3))
    hx = 420 + 430 * idet
    hb = 900 + 70 * idet
    hh = 540 + 70 * idet
    kach = 9 * A.w(t, 1.45)
    otkr = A.ease(A.seg(t, 2.9, 1.7))

    s = SL(Z_NEBO, baza.nebo("den", t, False) + baza.oblaka(t, 200, 5, 3, .55))
    nebo_add = (f'<circle cx="1620" cy="250" r="92" fill="#fff6d6" opacity=".97"/>'
                + baza.teplo(1620, 250, 520, 470, .75))
    s += SL(Z_NEBO, nebo_add)
    dal = baza.ulica_dal(40, 600, 1840, t, True, 9)
    dal += baza.izba_snaruzhi(60, 680, 450, t)
    dal += baza.sneg_lezhit(680, 30)
    s += SL(Z_DAL, dal)

    # расчищенная дорожка: от переднего края к калитке
    sred = (f'<path d="M420,1090 L1040,836 h240 L1700,1090 z" fill="#c2b391"'
            f' opacity=".85" {o(5)}/>')
    sred += (f'<path d="M520,1090 L1070,850 h180 L1600,1090 z" fill="#d8caa6" opacity=".6"/>')
    sred += baza.pleten(900, 880, 1020, 200, 9)
    # калитка в створе плетня
    sred += f'<rect x="1046" y="688" width="24" height="230" rx="8" fill="url(#derev)" {o(5)}/>'
    sred += f'<rect x="1330" y="688" width="24" height="230" rx="8" fill="url(#derev)" {o(5)}/>'
    sred += (f'<g transform="translate(1070,900) scale({math.cos(math.radians(74*otkr)):.3f},1)'
             f' translate(-1070,-900)">'
             f'<rect x="1070" y="716" width="258" height="196" rx="10" fill="url(#derev)" {o(6)}/>'
             f'<path d="M1080,770 h238 M1080,856 h238 M1080,726 l238,176" fill="none"'
             f' stroke="#a97f4e" stroke-width="13"/></g>')
    s += SL(Z_SRED, sred)

    per = ob.figura(hx, hb, hh, t, col="#2e2a22", kant="#ffe9bd")
    for dx in (-52, 22):
        per += ten(hx + dx + 22, hb + 6, 50, 13, .5)
        per += (f'<path d="M{hx+dx:.0f},{hb - 2:.0f} q46,-28 92,-4 q4,24 -32,28'
                f' q-54,4 -60,-24 z" fill="#4a3a26" {o(4)}/>')
    per += _vedro(hx + 128, hb - 190, .62, t, kach)
    per += baza.sneg_lezhit(1030, 26)
    r = random.Random(23)
    for i in range(26):
        sx, sy = r.uniform(0, W), r.uniform(880, 1070)
        per += (f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{r.uniform(2.4,5.2):.1f}"'
                f' fill="#ffffff" opacity="{.25 + .7*abs(A.w(t, 1.4 + r.uniform(0,1.6), i*.13)):.2f}"/>')
    per += baza.ramka_pp("levo", "#5a6d85", .35)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.blik(1560, 300, t, .8, "#cfe6ff", None, .5)
            + baza.begushchiy_blik(t, 9.0, .2, .12) + baza.vinetka(.3))
    return s


# ═══════════════════ 128, 129 ═══════════════════
def paket_u_dveri_kvartiry(t):
    """РАЗВИЛКА, квартира: калитка растворяется и становится дверью лифта,
    створки сходятся без пассажира, а пакет сам затягивается на два узла и
    встаёт у входной двери на коврик.
    Живое: двери лифта закрываются; узел затягивается; пакет встаёт на коврик."""
    kalit = max(0.0, 1.0 - A.ease(A.seg(t, .15, 1.1)))
    zakr = A.ease(A.seg(t, .55, 1.55))
    uzel = A.ease(A.seg(t, 1.9, 1.1))
    stav = A.out(A.seg(t, 3.0, 1.1))
    sed = 1.0 - .12 * math.sin(math.pi * min(1.0, A.seg(t, 3.8, .45)))

    s = SL(Z_NEBO, _stena("#39414c", "#1f252e"))
    dal = f'<rect y="0" width="{W}" height="1000" fill="url(#beton)"/>'
    dal += (f'<rect y="520" width="{W}" height="20" fill="{BETON2}" opacity=".75"/>')
    if kalit > .01:
        dal += f'<g opacity="{kalit:.2f}">' + baza.pleten(240, 880, 700, 200, 7) + "</g>"
    dal += baza.polovicy(1000, "url(#kamen)")
    s += SL(Z_DAL, dal)

    sred = ten(760, 1004, 280, 26, .5)
    sred += (f'<rect x="488" y="190" width="546" height="814" rx="10" fill="url(#chug)" {o(8)}/>')
    sred += (f'<rect x="516" y="218" width="490" height="770" fill="#10151c"/>')
    for sgn, x0 in ((1, 516), (-1, 1006)):
        w_ = 245 * zakr
        xx = x0 if sgn > 0 else x0 - w_
        sred += (f'<rect x="{xx:.0f}" y="218" width="{w_:.0f}" height="770"'
                 f' fill="url(#zhel)" {o(6)}/>')
        sred += (f'<rect x="{xx + (w_*.2 if sgn>0 else w_*.6):.0f}" y="260" width="{max(2, w_*.2):.0f}"'
                 f' height="690" fill="#ffffff" opacity=".16"/>')
    sred += (f'<rect x="628" y="120" width="266" height="58" rx="10" fill="url(#chug)" {o(6)}/>')
    for i in range(3):
        sred += (f'<circle cx="{688 + i*84}" cy="149" r="15" fill="{ob.ALYJ if i == 1 else "#3a4049"}"'
                 f' opacity="{.45 + .5*abs(A.w(t, 1.8, i*.3)):.2f}"/>')
    s += SL(Z_SRED, sred)

    # дверь квартиры, коврик и пакет
    per = _g("kovr", "#7a5440", "#3c2a20")
    per += (f'<rect x="1340" y="140" width="520" height="880" rx="8" fill="url(#derev)" {o(8)}/>')
    per += (f'<rect x="1384" y="190" width="432" height="340" rx="8" fill="none"'
            f' stroke="{DOSKA2}" stroke-width="10"/>')
    per += f'<circle cx="1800" cy="600" r="18" fill="url(#zhel)" {o(5)}/>'
    per += ten(1600, 1038, 230, 26, .5)
    per += (f'<rect x="1400" y="1006" width="420" height="66" rx="10" fill="url(#kovr)" {o(6)}/>')
    for i in range(6):
        per += (f'<line x1="{1424 + i*66}" y1="1012" x2="{1424 + i*66}" y2="1066"'
                f' stroke="#2c1f18" stroke-width="5" opacity=".6"/>')
    py = 780 + 206 * stav
    per += _g("paket2", "#dde5ee", "#8e9aa7")
    per += (f'<g transform="translate(1600,{py:.1f}) scale(1,{sed:.3f})">'
            + ten(6, 196, 128, 26, .5)
            + f'<path d="M-132,-46 h264 l34,232 q-166,46 -332,0 z" fill="url(#paket2)"'
              f' opacity=".94" {o(7)}/>'
            + f'<path d="M-104,16 q104,34 208,0 M-96,116 q96,34 192,0" fill="none"'
              f' stroke="#ffffff" stroke-width="9" opacity=".45"/>')
    for i, ux in enumerate((-40, 42)):
        r_ = 40 - 24 * uzel
        per += (f'<path d="M{ux - r_:.0f},-52 q{r_:.0f},-58 {r_*2:.0f},0" fill="none"'
                f' stroke="#c3cdd8" stroke-width="{13 + 7*uzel:.0f}" stroke-linecap="round"/>')
        per += (f'<ellipse cx="{ux:.0f}" cy="-48" rx="{r_*.66:.0f}" ry="{14 - 5*uzel:.0f}"'
                f' fill="none" stroke="#aab6c2" stroke-width="{9 + 4*uzel:.0f}"/>')
    per += "</g>"
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.44))
    return s


# ═══════════════════ 130 ═══════════════════
def ochistki_i_korobki_na_kuhne(t):
    """Кухня днём в разгар готовки: гора картофельных очистков на газете и
    стопка пустых коробок сами сгребаются в ведро, за окном ещё светло.
    Живое: очистки сгребаются; коробки складываются; солнце за окном низко."""
    s = SL(Z_NEBO, _stena("#b7c7d2", "#7e93a4"))
    dal = baza.doski(-20, 0, W + 40, 900, 160, True, "dosk")
    okno_vid = (f'<rect x="1300" y="130" width="500" height="390" fill="#cfe0ec"/>'
                f'<circle cx="1420" cy="440" r="70" fill="#ffe7ad" opacity=".95"/>'
                + baza.teplo(1420, 440, 300, 260, .8)
                + f'<path d="M1300,470 q120,-34 250,-10 q130,24 250,-14 v74 h-500 z"'
                  f' fill="#e9f2f8"/>')
    dal += baza.okno_izby(1300, 130, 500, 390, t, vid=okno_vid, moroz=.12)
    dal += baza.luch(1240, 520, 320, 520, t, .2)
    dal += baza.polka(140, 300, 520)
    for i in range(3):
        dal += baza.krynka(240 + i * 180, 294, .74)
    dal += baza.dver(1832, 180, 240, 790, .3)
    dal += baza.polovicy(900)
    s += SL(Z_DAL, dal)

    sred = baza.stol(-60, 700, 1260, 48)
    # газета под очистками
    sred += ten(620, 740, 330, 22, .4)
    sred += (f'<path d="M280,702 h680 l-36,52 h-608 z" fill="url(#list)" {o(5)}/>')
    for i in range(5):
        sred += (f'<line x1="{306 + i*6}" y1="{712 + i*8}" x2="{936 - i*7}" y2="{712 + i*8}"'
                 f' stroke="#a9a08c" stroke-width="3" opacity=".6"/>')
    # коробки складываются стопкой
    for i in range(4):
        k = A.out(A.seg(t, .9 + i * .45, .7))
        sred += _korobka(1090, 646 - i * 86 + 210 * (1 - k), 300, 92, t,
                         -4 + i * 3, min(1.0, k * 1.4))
    s += SL(Z_SRED, sred)

    r = random.Random(29)
    per = ""
    # гора очистков: то, что ещё не улетело, лежит кучей на газете
    for i in range(18):
        u = A.ease(A.seg(t, 1.0 + i * .16, .55))
        ox = 600 + r.uniform(-170, 150)
        oy = 686 + r.uniform(-46, 14)
        tx, ty = 1560, 850
        x = ox + (tx - ox) * u
        y = oy + (ty - oy) * u - 200 * math.sin(math.pi * u)
        per += _ochistka(x, y, r.uniform(-60, 60) + 240 * u, 1.1 + .6 * r.random(),
                         1.0 if u < .97 else 0.0)
    per += _vedro(1570, 1060, 1.5, t, 2.2 * A.w(t, 3.4))
    per += baza.ramka_pp("levo", "#5d6a76", .4)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.begushchiy_blik(t, 10.0, .3, .1) + baza.vinetka(.32))
    return s


# ═══════════════════ 131, 132 ═══════════════════
def taz_i_prischepki(t):
    """Плашка четвёртого запрета: таз с мокрым бельём, над ним пустая верёвка
    с прищепками; наволочка сама тянется к верёвке и опускается обратно в таз.
    Живое: прищепки покачиваются; пена в тазу оседает; наволочка опускается в таз."""
    vverh = A.out(A.seg(t, .35, 1.15))
    vniz = A.ease(A.seg(t, 1.85, 1.2))
    ny = 720 - 420 * vverh + 430 * vniz
    nang = -6 + 10 * A.w(t, 2.4) * (1 - vniz)
    pena = 1.0 - .72 * A.seg(t, .2, 3.4)

    s = SL(Z_NEBO, _stena("#3d5668", "#1d2c38"))
    dal = _g("kafel", "#cfe0e6", "#92acb8")
    for r_ in range(7):
        for c in range(13):
            dal += (f'<rect x="{-20 + c*152:.0f}" y="{-10 + r_*120:.0f}" width="146"'
                    f' height="114" rx="6" fill="url(#kafel)" opacity=".92"'
                    f' stroke="#7e95a2" stroke-width="3"/>')
    dal += baza.okno_izby(1420, 140, 400, 300, t,
                          vid=f'<rect x="1420" y="140" width="400" height="300" fill="{SUMER}"/>'
                              + baza.sneg_letit(t, 14, 7, .5),
                          moroz=.5)
    dal += (f'<rect y="840" width="{W}" height="{H-840}" fill="#6f8290"/>')
    dal += (f'<rect y="832" width="{W}" height="18" fill="#54646f"/>')
    s += SL(Z_DAL, dal)

    prov = 56 + 8 * A.w(t, 4.0)
    sred = (f'<path d="M80,252 Q960,{252 + prov:.0f} 1860,252" fill="none"'
            f' stroke="#9b8a6e" stroke-width="8"/>')
    for i in range(7):
        u = (i + .5) / 7
        px = (1 - u) ** 2 * 80 + 2 * (1 - u) * u * 970 + u * u * 1860
        py = (1 - u) ** 2 * 252 + 2 * (1 - u) * u * (252 + prov) + u * u * 252
        sred += _prischepka(px, py - 6, 6 * A.w(t, 2.5, i * .19), 1.35)
    sred += baza.polka(130, 430, 430)
    sred += baza.krynka(230, 424, .72)
    sred += baza.krynka(380, 424, .6)
    sred += baza.krynka(500, 424, .52)
    # стопка сухого белья на табурете
    sred += ten(290, 1010, 150, 22, .45)
    for i in range(4):
        sred += (f'<rect x="178" y="{896 - i*34:.0f}" width="228" height="34" rx="9"'
                 f' fill="url(#krem)" {o(5)}/>')
    sred += f'<rect x="196" y="930" width="192" height="130" rx="8" fill="url(#derev)" {o(6)}/>'
    s += SL(Z_SRED, sred)

    per = _taz(900, 960, 820, t, max(0.0, pena))
    per += (f'<g transform="translate(900,{ny:.1f}) rotate({nang:.2f})">'
            + ten(6, 150, 140, 26, .45)
            + f'<path d="M-160,-130 h320 q24,140 -8,266 q-156,42 -310,0 q-28,-130 -2,-266 z"'
              f' fill="url(#krem)" {o(7)}/>'
            + f'<path d="M-130,-96 q130,34 260,0 M-136,10 q136,38 272,0 M-128,112 q128,34 256,0"'
              f' fill="none" stroke="#cfbf9c" stroke-width="8" opacity=".75"/>'
            + f'<path d="M-150,-120 q150,-26 300,0" fill="none" stroke="#ffffff"'
              f' stroke-width="10" opacity=".35"/></g>')
    per += baza.ramka_pp("oba", "#16222b", .45)
    s += SL(Z_PERED, per)
    s += SL(Z_FIX, baza.vinetka(.4))
    return s
