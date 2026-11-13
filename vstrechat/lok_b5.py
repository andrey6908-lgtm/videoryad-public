# -*- coding: utf-8 -*-
"""Декорации планов 77-104 ролика «Как встречать год хозяйки года 2027»."""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob
OKNO = (860, 300, 980, 551)

# Блок «Что поставить на стол». Еда — СИЛУЭТ И ПЯТНО ЦВЕТА: кадр смотрят с
# телефона, мелкая кухня там пропадает. Рuk не рисуем: тесто, стакан,
# пельмень и нож работают сами (правило 05.11).

BAND = 830          # полоса для главного, когда справа стоит окно вставки
MUKA = "#f3ecdc"
TESTO = "#ead9b4"
FARSH = "#9c4a3a"
HOLOD = "#1a2440"   # холодный вечер за окном
STENA = "#2b3449"
STENA2 = "#1a2130"
CHAY = "#c9892f"


# ═══════════════════ ОБЩИЕ КИРПИЧИКИ БЛОКА ═══════════════════

def _gladko(pts, zamknut=False):
    """Ломаную — в мягкую кривую: через середины отрезков."""
    d = "M%.0f,%.0f" % (pts[0][0], pts[0][1])
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        d += " Q%.0f,%.0f %.0f,%.0f" % (x0, y0, (x0 + x1) / 2, (y0 + y1) / 2)
    d += " L%.0f,%.0f" % (pts[-1][0], pts[-1][1])
    return d + (" Z" if zamknut else "")


def _tochka_lomanoy(pts, u):
    """Точка на ломаной по доле пути: по ней едут запах, чек, мандарин."""
    dl = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
          for i in range(len(pts) - 1)]
    L = sum(dl) or 1.0
    s = max(0.0, min(.999, u)) * L
    for i, d in enumerate(dl):
        if s <= d:
            k = s / (d or 1.0)
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k,
                    pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k)
        s -= d
    return pts[-1]


def _stena(t, teplo_x=520, teplo_y=520, col=STENA, col2=STENA2, R=820):
    """Холодная стена комнаты и ОДНО тёплое пятно — гамма праздника."""
    s = f'<rect width="{W}" height="{H}" fill="{col2}"/>'
    s += f'<rect y="{H*.08:.0f}" width="{W}" height="{H*.92:.0f}" fill="{col}" opacity=".9"/>'
    for i in range(7):
        s += (f'<rect x="{i*W/7:.0f}" y="{H*.08:.0f}" width="4" height="{H*.92:.0f}"'
              f' fill="#0e131d" opacity=".25"/>')
    s += teplo(teplo_x, teplo_y, R, R * .82, .62)
    return s


def _za_oknom(x, y, w_, h_, t, col=HOLOD, seed=21, n=15):
    """Что видно за стеклом: синяя ночь и падающий снег."""
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="{col}"/>'
    r = random.Random(seed)
    for i in range(n):
        x0 = r.uniform(x, x + w_)
        per = r.uniform(4.0, 9.0)
        ph = r.random()
        u = ((t / per) + ph) % 1.0
        s += (f'<circle cx="{x0 + 24*A.w(t,5.2,ph):.0f}" cy="{y + u*h_:.0f}"'
              f' r="{r.uniform(2.2,4.8):.1f}" fill="{SNEG}" opacity=".8"/>')
    return s


def _skatert(x, y, w_, t, svis=104, col="url(#rush)", kant=None, amp=9.0,
             ph=0.0, n=6, polosa=True, gl=130):
    """Скатерть на столе: ПЛОСКОСТЬ столешницы в перспективе, передняя кромка,
    свисающий край волной, красная полоса. Без плоскости стол читается доской."""
    kant = kant or ob.ALYJ
    bot = y + 26 + svis
    pts = []
    for i in range(n + 1):
        u = 1 - i / n
        pts.append((x - 12 + (w_ + 24) * u,
                    bot + amp * A.w(t, 2.4 + i * .32, ph + i * .17)))
    s = ten(x + w_ / 2, bot + 44, w_ * .52, 30, .5)
    # ПЛОСКОСТЬ столешницы в перспективе: дальняя кромка уже передней
    dd = min(w_ * .17, 190.0)
    s += (f'<path d="M{x+dd:.0f},{y-gl:.0f} L{x+w_-dd:.0f},{y-gl:.0f}'
          f' L{x+w_+20:.0f},{y:.0f} L{x-20:.0f},{y:.0f} Z" fill="{col}" {o(6)}/>')
    s += (f'<path d="M{x+dd:.0f},{y-gl:.0f} L{x+w_-dd:.0f},{y-gl:.0f}" fill="none"'
          f' stroke="#ffffff" stroke-width="8" opacity=".3"/>')
    for i in range(1, 5):
        u = i / 5.0
        s += (f'<path d="M{x + dd + (w_ - 2*dd)*u:.0f},{y-gl:.0f}'
              f' L{x - 20 + (w_ + 40)*u:.0f},{y:.0f}" stroke="#d9c8a4"'
              f' stroke-width="3" opacity=".35"/>')
    d = ("M%.0f,%.0f h%.0f v26 L%.0f,%.0f " % (x - 20, y, w_ + 40, pts[0][0], pts[0][1])
         + _gladko(pts)[1:] + " L%.0f,%.0f Z" % (x - 20, y + 26))
    s += f'<path d="{d}" fill="{col}" {o(6)}/>'
    if polosa:
        up = [(px, py - 34) for px, py in pts]
        s += (f'<path d="{_gladko(up)}" fill="none" stroke="{kant}"'
              f' stroke-width="9" opacity=".75" stroke-linecap="round"/>')
    for i in range(1, n):
        px = pts[i][0]
        s += (f'<path d="M{px:.0f},{y+28:.0f} q{6*A.w(t,3.4,i*.2):.0f},{svis*.5:.0f}'
              f' {2:.0f},{svis*.9:.0f}" fill="none" stroke="#cdb98d"'
              f' stroke-width="4" opacity=".55"/>')
    s += (f'<rect x="{x-20:.0f}" y="{y:.0f}" width="{w_+40:.0f}" height="12" rx="6"'
          f' fill="#ffffff" opacity=".35"/>')
    return s


def _blyudo(cx, cy, r_, t=0.0, col="url(#krem)", obod=None, ph=0.0):
    """Блюдо силуэтом: овал, золотой ободок, блик. Без кухонной мелочи."""
    obod = obod or ob.ZOLOTO
    s = ten(cx, cy + r_ * .30, r_ * .92, r_ * .22, .5)
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r_:.0f}" ry="{r_*.34:.0f}"'
          f' fill="{col}" {o(6)}/>')
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy-2:.0f}" rx="{r_*.74:.0f}" ry="{r_*.24:.0f}"'
          f' fill="none" stroke="{obod}" stroke-width="5" opacity=".8"/>')
    bl = .3 + .3 * abs(A.w(t, 3.6, ph))
    s += (f'<ellipse cx="{cx-r_*.36:.0f}" cy="{cy-r_*.13:.0f}" rx="{r_*.24:.0f}"'
          f' ry="{r_*.07:.0f}" fill="#ffffff" opacity="{.25+bl:.2f}"/>')
    return s


def _pelmen(cx, cy, s_=1.0, a=0.0, iney=0.0, vyh=1.0):
    """Пельмень силуэтом: тело, защип дугой, блик. Иней — белая вуаль."""
    if vyh <= .02:
        return ""
    w_ = 42 * s_ * vyh
    h_ = 27 * s_ * vyh
    s = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({a:.1f})">'
    s += ten(0, h_ * 1.05, w_ * .9, h_ * .36, .4)
    s += f'<ellipse rx="{w_:.1f}" ry="{h_:.1f}" fill="url(#krem)" {o(max(3, 4*s_)):s}/>'
    s += (f'<path d="M{-w_*.8:.1f},{h_*.1:.1f} q{w_*.8:.1f},{h_*.95:.1f} {w_*1.6:.1f},0"'
          f' fill="none" stroke="#d6c097" stroke-width="{max(2.4, 4*s_):.1f}"/>')
    for i in range(4):
        u = -.6 + i * .4
        s += (f'<path d="M{w_*u:.1f},{h_*.5:.1f} q{w_*.1:.1f},{h_*.36:.1f} {w_*.2:.1f},0"'
              f' fill="none" stroke="#c3ab7e" stroke-width="{max(1.8, 2.8*s_):.1f}"/>')
    s += (f'<ellipse cx="{-w_*.3:.1f}" cy="{-h_*.36:.1f}" rx="{w_*.25:.1f}"'
          f' ry="{h_*.22:.1f}" fill="#ffffff" opacity=".5"/>')
    if iney > .01:
        s += f'<ellipse rx="{w_:.1f}" ry="{h_:.1f}" fill="{INEY}" opacity="{min(.8, iney*.8):.2f}"/>'
        for i in range(5):
            s += (f'<circle cx="{-w_*.6 + i*w_*.3:.1f}" cy="{h_*(-.3 + (i%2)*.5):.1f}"'
                  f' r="{2.4*s_:.1f}" fill="#ffffff" opacity="{min(.9, iney):.2f}"/>')
    return s + "</g>"


def _banka(x, y, w_, h_, t, soderzh="#b63b27", ph=0.0, kryshka=True, zontik=False):
    """Банка припасов: стекло, содержимое ПЯТНОМ, крышка, бегущий блик."""
    s = ten(x, y + 10, w_ * .62, w_ * .17, .45)
    s += (f'<rect x="{x-w_/2:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' rx="{w_*.18:.0f}" fill="url(#stekl)" opacity=".88" {o(5)}/>')
    s += (f'<rect x="{x-w_/2+7:.0f}" y="{y-h_*.8:.0f}" width="{w_-14:.0f}"'
          f' height="{h_*.74:.0f}" rx="{w_*.14:.0f}" fill="{soderzh}" opacity=".92"/>')
    for i in range(3):
        s += (f'<circle cx="{x - w_*.2 + i*w_*.2:.0f}" cy="{y - h_*(.24 + .2*(i % 2)):.0f}"'
              f' r="{w_*.13:.0f}" fill="#ffffff" opacity=".16"/>')
    if zontik:
        for i in range(5):
            a = -1.5 + i * .55
            s += (f'<path d="M{x:.0f},{y-h_*.52:.0f} l{math.cos(a)*w_*.3:.0f},'
                  f'{-abs(math.sin(a))*h_*.2 - h_*.1:.0f}" fill="none" stroke="#8fae5a"'
                  f' stroke-width="4" opacity=".85"/>')
    if kryshka:
        s += (f'<rect x="{x-w_*.57:.0f}" y="{y-h_-22:.0f}" width="{w_*1.14:.0f}"'
              f' height="28" rx="9" fill="url(#zhel)" {o(5)}/>')
    bl = ((t * .5 + ph) % 1.0)
    s += (f'<rect x="{x - w_*.42 + bl*w_*.6:.0f}" y="{y-h_*.88:.0f}" width="{w_*.1:.0f}"'
          f' height="{h_*.7:.0f}" rx="{w_*.05:.0f}" fill="#ffffff"'
          f' opacity="{.18 + .3*math.sin(math.pi*bl):.2f}"/>')
    return s


def _muka(x, y, w_, t, n=20, seed=3, R=180, sp=.55, op=.6):
    """Мучная пыль: поднимается и оседает — живой элемент всех кухонных планов."""
    r = random.Random(seed)
    s = ""
    for i in range(n):
        ph = r.random()
        per = r.uniform(1.7, 3.4) / sp
        u = ((t / per) + ph) % 1.0
        xx = x + r.uniform(0, w_) + 46 * A.w(t, 3.0 + i * .19, ph)
        yy = y - R * math.sin(math.pi * u) * r.uniform(.45, 1.0)
        s += (f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{r.uniform(2.6,6.8):.1f}"'
              f' fill="{MUKA}" opacity="{op*(1-abs(2*u-1)):.2f}"/>')
    return s


def _drozh(x, y, w_, t, n=5, R=160, op=.32, col="#ffd49a"):
    """Дрожь тёплого воздуха — над батареей и над горячим блюдом."""
    s = ""
    for i in range(n):
        xx = x + (i + .5) * w_ / n
        d = "M%.0f,%.0f" % (xx, y)
        for k in range(1, 5):
            dy = -R * k / 4.0
            dx = 15 * A.w(t, 1.5 + i * .27, k * .26)
            d += " Q%.0f,%.0f %.0f,%.0f" % (xx + dx * 1.7, y + dy + R / 8.0, xx + dx, y + dy)
        s += (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5"'
              f' opacity="{op:.2f}" stroke-linecap="round"/>')
    return s


def _vilka(cx, cy, a, s_=1.0, dl=1.0):
    """Вилка силуэтом: черенок и три зубца. Тянется к блюду сама, без рukи."""
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({a:.1f}) scale({s_:.3f})">'
    g += f'<rect x="0" y="-9" width="{230*dl:.0f}" height="18" rx="9" fill="url(#zhel)" {o(4)}/>'
    g += f'<rect x="-46" y="-26" width="52" height="52" rx="10" fill="url(#zhel)" {o(4)}/>'
    for i in (-1, 0, 1):
        g += (f'<rect x="-96" y="{i*18-5:.0f}" width="54" height="10" rx="5"'
              f' fill="url(#zhel)" {o(3)}/>')
    g += '<rect x="-40" y="-20" width="8" height="40" rx="4" fill="#ffffff" opacity=".4"/>'
    return g + "</g>"


def _stul(x, y, t, s_=1.0, spinka=True, otodvinut=0.0):
    """Табурет или стул со спинкой — сиденье и ножки, с тенью и бликом."""
    g = f'<g transform="translate({x + otodvinut:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 14, 108, 22, .5)
    if spinka:
        g += f'<rect x="-82" y="-430" width="164" height="30" rx="12" fill="url(#derev)" {o(6)}/>'
        g += f'<rect x="-74" y="-400" width="22" height="180" rx="8" fill="url(#derev)" {o(5)}/>'
        g += f'<rect x="52" y="-400" width="22" height="180" rx="8" fill="url(#derev)" {o(5)}/>'
    g += f'<rect x="-104" y="-232" width="208" height="34" rx="12" fill="url(#derev)" {o(6)}/>'
    g += f'<rect x="-96" y="-226" width="190" height="10" rx="5" fill="#ffffff" opacity=".28"/>'
    for xx in (-88, 66):
        g += f'<rect x="{xx}" y="-198" width="24" height="198" rx="8" fill="url(#derev)" {o(5)}/>'
    g += '<rect x="-80" y="-120" width="160" height="14" rx="6" fill="#6d4423" opacity=".8"/>'
    return g + "</g>"


def _kuvshin(x, y, s_=1.0, col="#eef3f8"):
    """Кувшин молока: тулово, горло, носик, блик."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 10, 66, 15, .45)
    g += (f'<path d="M-60,0 q-16,-108 14,-146 l0,-40 q46,-14 92,0 l0,40'
          f' q30,38 14,146 z" fill="{col}" {o(6)}/>')
    g += '<path d="M46,-186 q44,10 30,54" fill="none" stroke="#dfe6ee" stroke-width="16"/>'
    g += '<ellipse cx="-22" cy="-104" rx="16" ry="54" fill="#ffffff" opacity=".55"/>'
    g += f'<path d="M-56,-56 q56,20 112,0" fill="none" stroke="#c6d2dd" stroke-width="7"/>'
    return g + "</g>"


def _zelen(x, y, t, s_=1.0, n=9, ph=0.0, col=None, vyh=1.0):
    """Пучок зелени: перья качаются вразнобой — живой элемент стола."""
    if vyh <= .02:
        return ""
    col = col or "#5f8a3e"
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_*vyh:.3f})">'
    g += ten(0, 8, 70, 14, .4)
    for i in range(n):
        u = (i / (n - 1.0)) - .5
        kch = 13 * A.w(t, 2.2 + i * .21, ph + i * .13)
        c = (col, "#79a44f", "#486f31")[i % 3]
        g += (f'<path d="M{u*54:.0f},6 q{u*40 + kch*.5:.0f},-70 {u*66 + kch:.0f},-136"'
              f' fill="none" stroke="{c}" stroke-width="13" stroke-linecap="round"/>')
        g += (f'<circle cx="{u*66 + kch:.0f}" cy="-138" r="15" fill="{c}" opacity=".9"/>')
    g += f'<path d="M-30,6 q30,16 60,0" fill="none" stroke="{ob.ALYJ}" stroke-width="10"/>'
    return g + "</g>"


def _syr(x, y, s_=1.0, vyh=1.0):
    """Тарелка с сыром: три клина жёлтым пятном, дырки — три точки."""
    if vyh <= .02:
        return ""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_*vyh:.3f})">'
    g += _blyudo(0, 0, 96, 0.0, "url(#krem)")
    for i, dx in enumerate((-48, 0, 48)):
        g += (f'<path d="M{dx:.0f},-12 l62,-10 l-16,-46 z" fill="url(#zol)" {o(5)}'
              f' transform="rotate({-14 + i*14},{dx},-12)"/>')
        g += f'<circle cx="{dx+28:.0f}" cy="-32" r="6" fill="#b58a28" opacity=".8"/>'
    return g + "</g>"


def _ogurcy(x, y, s_=1.0, vyh=1.0):
    """Огурцы и редиска силуэтом: зелёные веретёна и красные шарики."""
    if vyh <= .02:
        return ""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_*vyh:.3f})">'
    g += _blyudo(0, 0, 102, 0.0, "url(#krem)")
    for i, (dx, a) in enumerate(((-54, -14), (-6, 6), (42, -8))):
        g += (f'<ellipse cx="{dx:.0f}" cy="-22" rx="44" ry="17" fill="#4f7a37" {o(5)}'
              f' transform="rotate({a},{dx},-22)"/>')
        g += (f'<ellipse cx="{dx-12:.0f}" cy="-28" rx="18" ry="5" fill="#8fb866" opacity=".7"/>')
    for i, dx in enumerate((-30, 16, 58)):
        g += f'<circle cx="{dx:.0f}" cy="-50" r="20" fill="{ob.ALYJ}" {o(4)}/>'
        g += f'<circle cx="{dx-6:.0f}" cy="-56" r="6" fill="#ffffff" opacity=".45"/>'
        g += f'<path d="M{dx:.0f},-68 q8,-18 22,-16" fill="none" stroke="#6f9a46" stroke-width="6"/>'
    return g + "</g>"


def _rukavichka(x, y, s_=1.0, col=None, t=0.0, ph=0.0):
    """Вязаная рukавичка: ладонь не рисуем — варежка работает сама."""
    col = col or ob.ALYJ
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(0, 16, 92, 18, .45)
    g += (f'<path d="M-78,10 q-20,-104 24,-140 q54,-32 112,-4 q44,26 26,144 z"'
          f' fill="{col}" {o(6)}/>')
    g += (f'<path d="M66,-86 q54,-14 52,34 q-2,40 -50,28" fill="{col}" {o(5)}/>')
    g += f'<rect x="-82" y="-4" width="168" height="40" rx="18" fill="{ob.ALYJ2}" {o(5)}/>'
    for i in range(6):
        g += (f'<path d="M{-70 + i*28:.0f},-2 v34" fill="none" stroke="#6d1316"'
              f' stroke-width="6" opacity=".6"/>')
    for i in range(4):
        g += (f'<path d="M{-58 + i*32:.0f},-116 q10,30 0,60" fill="none"'
              f' stroke="#ffffff" stroke-width="5" opacity=".2"/>')
    return g + "</g>"


def _kozhura(x, y, a=0.0, s_=1.0, zagib=0.0):
    """Кусочек кожуры: подсыхая, загибается — живой элемент батареи."""
    k = 1.0 + zagib
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({a:.1f}) scale({s_:.3f})">'
            f'{ten(0, 16, 46, 10, .4)}'
            f'<path d="M-54,10 q{26*k:.0f},{-58*k:.0f} 54,{-18*k:.0f}'
            f' q{30*k:.0f},{14*k:.0f} 54,{18*k:.0f} q-54,{26:.0f} -108,0 z"'
            f' fill="{ob.MANDA}" {o(5)}/>'
            f'<path d="M-44,2 q52,{-40*k:.0f} 98,{-4*k:.0f}" fill="none"'
            f' stroke="#fff0dc" stroke-width="7" opacity=".6"/></g>')


def _kartochka_video(x, y, w_, h_, t, vyh=1.0, ph=0.0, tema=0):
    """Карточка-обложка другого видео: рамка, рисованный стол и хозяйка года.
    Текста НЕ рисуем — заголовок кладёт over.py."""
    if vyh <= .02:
        return ""
    g = (f'<g transform="translate({x + w_/2:.1f},{y + h_:.1f}) scale({vyh:.3f})'
         f' translate({-w_/2:.1f},{-h_:.1f})">')
    g += ten(w_ / 2, h_ + 20, w_ * .48, 24, .55)
    fon = (ob.HVOYA, ob.ALYJ2, "#243a52")[tema % 3]
    g += f'<rect width="{w_:.0f}" height="{h_:.0f}" rx="22" fill="{fon}" {o(7)}/>'
    g += (f'<rect x="10" y="10" width="{w_-20:.0f}" height="{h_-20:.0f}" rx="16"'
          f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="6" opacity=".85"/>')
    g += teplo(w_ * .5, h_ * .42, w_ * .5, h_ * .36, .45)
    # рисованный стол внутри обложки
    ty = h_ * .70
    g += (f'<rect x="{w_*.12:.0f}" y="{ty:.0f}" width="{w_*.76:.0f}" height="{h_*.05:.0f}"'
          f' rx="8" fill="url(#rush)" {o(4)}/>')
    for i, dx in enumerate((.24, .42, .62)):
        g += (f'<ellipse cx="{w_*dx:.0f}" cy="{ty-6:.0f}" rx="{w_*.08:.0f}"'
              f' ry="{w_*.03:.0f}" fill="{(KREM, ob.MANDA, "#7f9f55")[i]}" {o(3)}/>')
    g += baza.svecha(w_ * .80, ty - 46, t, ph, .34, 70)
    g += ob.koza_malaya(w_ * .34, ty - 10, t, w_ / 2100.0 * 1.5, ph)
    # бегущий блик по глянцу обложки
    bl = ((t * .34 + ph) % 1.0)
    g += (f'<path d="M{w_*bl - w_*.5:.0f},0 l{w_*.2:.0f},0 l{-w_*.3:.0f},{h_:.0f}'
          f' l{-w_*.2:.0f},0 z" fill="#ffffff" opacity=".10"/>')
    return g + "</g>"


def _tetrad(x, y, w_, h_, t, ph=0.0):
    """Тетрадка в клетку, исписанная: страница переворачивается сама."""
    g = f'<g transform="translate({x:.1f},{y:.1f})">'
    g += ten(w_ / 2, h_ + 14, w_ * .5, 18, .5)
    g += f'<rect width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="#f3f0e2" {o(6)}/>'
    for i in range(int(w_ / 26)):
        g += (f'<line x1="{i*26:.0f}" y1="0" x2="{i*26:.0f}" y2="{h_:.0f}"'
              f' stroke="#9db7cf" stroke-width="2" opacity=".55"/>')
    for i in range(int(h_ / 26)):
        g += (f'<line x1="0" y1="{i*26:.0f}" x2="{w_:.0f}" y2="{i*26:.0f}"'
              f' stroke="#9db7cf" stroke-width="2" opacity=".55"/>')
    r = random.Random(17)
    for i in range(9):
        yy = 34 + i * (h_ - 56) / 8.0
        ww = r.uniform(.4, .86) * w_
        g += (f'<path d="M{w_*.08:.0f},{yy:.0f} h{ww:.0f}" stroke="#2f4256"'
              f' stroke-width="5" opacity=".7" stroke-linecap="round"/>')
    # страница переворачивается: ширина листа идёт от полной к нулю и обратно
    u = ((t / 3.4) + ph) % 1.0
    k = abs(math.cos(math.pi * u))
    g += (f'<g transform="translate({w_/2:.0f},0) scale({k:.3f},1) translate({-w_/2:.0f},0)">'
          f'<rect width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="#fbf8ec" {o(5)}/>'
          f'<path d="M{w_*.1:.0f},{h_*.3:.0f} h{w_*.7:.0f} M{w_*.1:.0f},{h_*.52:.0f}'
          f' h{w_*.5:.0f} M{w_*.1:.0f},{h_*.74:.0f} h{w_*.64:.0f}" stroke="#2f4256"'
          f' stroke-width="5" opacity=".6" stroke-linecap="round"/></g>')
    g += f'<rect x="{w_*.46:.0f}" y="0" width="10" height="{h_:.0f}" fill="#b9a884" opacity=".7"/>'
    return g + "</g>"


def _vetka_eli(x, y, dl, t, s_=1.0, ph=0.0, vniz=1.0):
    """Еловая лапа: ось и иглы двумя тонами, лёгкое дыхание от t."""
    kach = 2.2 * A.w(t, 4.6, ph)
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({kach:.2f}) scale({s_:.3f})">'
    g += f'<path d="M0,0 q{dl*.5:.0f},{26*vniz:.0f} {dl:.0f},{54*vniz:.0f}" fill="none" stroke="#3a2a1c" stroke-width="18"/>'
    n = 16
    for i in range(n):
        u = (i + .5) / n
        bx = dl * u
        by = 26 * vniz * u + 28 * vniz * u * u
        ln = (90 - 38 * u) * (1 + .12 * A.w(t, 3.2, ph + i * .11))
        for sgn in (-1, 1):
            c = ob.HVOYA if (i + (sgn > 0)) % 2 == 0 else ob.HVOYA2
            g += (f'<path d="M{bx:.0f},{by:.0f} l{ln*.42:.0f},{sgn*ln:.0f}"'
                  f' fill="none" stroke="{c}" stroke-width="12" stroke-linecap="round"/>')
    return g + "</g>"


# ═══════════════════ ДЕКОРАЦИИ ПЛАНОВ 77-104 ═══════════════════

def skatert_lozhitsya_na_stol(t):
    """Комната под абажуром, белая скатерть парусом садится на раздвинутый стол.
    Живое: скатерть летит и садится, складки расправляются, абажур покачивается."""
    p = A.out(A.seg(t, .20, 1.80))
    s = SL(Z_NEBO, _stena(t, 820, 430, "#2c3650", "#171d2b", 900)
           + ob.girlyanda(-60, 150, 1980, 196, t, 16, 120))
    dal = okno_izby(1430, 250, 330, 290, t, vid=_za_oknom(1430, 250, 330, 290, t),
                    moroz=.45, krest=True)
    dal += ob.elka(300, 1010, 470, t, seed=6)
    s += SL(Z_DAL, dal)
    # стол раздвинут: видно вставную доску посередине
    sred = ten(960, 1066, 800, 46, .55)
    sred += (f'<path d="M420,640 L1500,640 L1760,790 L160,790 Z" fill="url(#derev)" {o(7)}/>')
    sred += (f'<rect x="160" y="780" width="1600" height="46" rx="14" fill="url(#derev)" {o(7)}/>')
    sred += '<path d="M930,642 L1010,642 L1016,788 L924,788 Z" fill="#6d4423" opacity=".5"/>'
    for xx in (268, 1584):
        sred += f'<rect x="{xx}" y="826" width="46" height="240" fill="url(#derev)" {o(6)}/>'
    sred += _stul(420, 700, t, .5) + _stul(1480, 700, t, .5)
    s += SL(Z_SRED, sred)
    # ПАРУС: верх держится, низ полощет; к p=1 скатерть ложится на столешницу
    x0, w0 = 150, 1620
    y0 = 250 + (660 - 250) * p
    amp = 150 * (1 - p) + 11
    verh, niz = [], []
    for i in range(8):
        u = i / 7.0
        verh.append((x0 + w0 * u, y0 + 38 * math.sin(math.pi * u) * (1 - p)))
        niz.append((x0 + w0 * (1 - u),
                    y0 + 130 + 190 * (1 - p) + amp * A.w(t, 1.0 + .8 * p, (1 - u) * 1.7)))
    d = _gladko(verh) + " " + _gladko(niz)[1:] + " Z"
    per = ten(960, 1032, 700 * (.4 + .6 * p), 30, .4 * p)
    per += f'<path d="{d}" fill="url(#rush)" {o(6)} opacity=".98"/>'
    for i in range(1, 7):
        u = i / 7.0
        vx, vy = verh[i]
        per += (f'<path d="M{vx:.0f},{vy:.0f} q{26*(1-p)*A.w(t,1.6,u):.0f},'
                f'{(130 + 190*(1-p))*.5:.0f} {10*(1-p)*A.w(t,1.2,u):.0f},'
                f'{130 + 190*(1-p):.0f}" fill="none" stroke="#d8c7a2"'
                f' stroke-width="{4 + 5*(1-p):.0f}" opacity="{.35 + .4*(1-p):.2f}"/>')
    per += (f'<path d="{_gladko([(px, py - 30) for px, py in niz])}" fill="none"'
            f' stroke="{ob.ALYJ}" stroke-width="9" opacity=".7" stroke-linecap="round"/>')
    per += baza.lampa(820, 430, t, 1.35, True)
    s += SL(Z_PERED, per)
    s += vinetka(.4)
    return s


def dva_blyuda_mandariny_i_pelmeni(t):
    """Два блюда на скатерти: горка мандаринов и дымящиеся пельмени.
    Живое: пар от пельменей, листик качается, вилки тянутся к блюду."""
    s = SL(Z_NEBO, _stena(t, 960, 420, "#2e3850", "#191f2d", 980)
           + ob.girlyanda(-60, 130, 1980, 170, t, 18, 100))
    s += SL(Z_DAL, ob.elka(1700, 1030, 540, t, seed=9)
            + okno_izby(90, 200, 300, 270, t, vid=_za_oknom(90, 200, 300, 270, t), moroz=.4))
    s += SL(Z_SRED, _skatert(60, 700, 1800, t, 150))
    # ГОРКА МАНДАРИНОВ слева — пятна цвета, никаких долек
    gor = ""
    for i, (dx, dy, sc) in enumerate(((-150, 10, 1.5), (-40, 18, 1.6), (72, 8, 1.5),
                                      (-96, -58, 1.5), (14, -52, 1.6), (-42, -116, 1.5))):
        gor += ob.mandarin(430 + dx, 672 + dy, sc, 0.0, t)
    # листик на верхнем мандарине качается
    kch = 11 * A.w(t, 2.0)
    gor += (f'<g transform="translate(388,560) rotate({kch:.1f})">'
            f'<path d="M0,0 q46,-34 96,-10 q-40,40 -96,10 z" fill="#5f8a3e" {o(5)}/>'
            f'<path d="M4,-2 q44,-20 86,-6" fill="none" stroke="#8fb866" stroke-width="5"/></g>')
    # БЛЮДО ПЕЛЬМЕНЕЙ справа
    pel = _blyudo(1360, 690, 250, t, "url(#krem)")
    r = random.Random(4)
    for i in range(11):
        a = i * 2.39996
        rr = 160 * math.sqrt((i + .6) / 11.0)
        pel += _pelmen(1360 + math.cos(a) * rr, 668 + math.sin(a) * rr * .36,
                       1.25, r.uniform(-26, 26))
    pel += baza.par(1300, 600, t, 5, .72, 280, .38, 1.5)
    pel += baza.par(1420, 610, t, 4, .66, 250, .32, 1.3)
    pel += _drozh(1240, 590, 240, t, 4, 170, .3)
    s += SL(Z_PERED, gor + pel)
    # ЧЕТЫРЕ ВИЛКИ тянутся к блюду с четырёх сторон (рukи не рисуем)
    vil = ""
    for i, (vx, vy, a, t0) in enumerate(((1900, 690, 180, .5), (860, 700, 0, 1.0),
                                         (1300, 1070, -72, 1.5), (1430, 300, 104, 2.0))):
        k = A.ease(A.seg(t, t0, 1.5))
        dxp = (1360 - vx) * .46 * k
        dyp = (690 - vy) * .46 * k
        vil += _vilka(vx + dxp, vy + dyp, a, 1.5, .8 + .2 * k)
    s += SL(Z_LETIT, vil)
    s += vinetka(.38)
    return s


def mandarin_v_detskih_rukah(t):
    """Крупно мандарин над вязаными рukавами: кожура сходит одной спиралью.
    Живое: спираль кожуры растёт, капли сока летят, дольки раскрываются."""
    p = A.ease(A.seg(t, .35, 2.6))
    s = SL(Z_NEBO, _stena(t, 400, 520, "#2a3348", "#171d29", 780))
    # тёплое боке гирлянды на фоне
    bok = ""
    r = random.Random(13)
    for i in range(14):
        bx, by = r.uniform(20, BAND), r.uniform(80, 560)
        gor = .25 + .5 * abs(A.w(t, 2.6 + r.uniform(0, 2), i * .17))
        col = (SVET, ob.ALYJ, ob.ZOLOTO, "#8fd6ff")[i % 4]
        bok += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r.uniform(22,54):.0f}"'
                f' fill="{col}" opacity="{gor*.3:.2f}"/>')
    s += SL(Z_DAL, bok + f'<rect y="900" width="{BAND}" height="180" fill="#3a2b22" opacity=".8"/>')
    # вязаные рukава: манжеты, без ладоней
    muf = ""
    for i, (mx, col) in enumerate(((190, ob.ALYJ), (640, "#2f5a78"))):
        kch = 3.4 * A.w(t, 3.0, i * .4)
        muf += (f'<g transform="translate({mx:.0f},{940 + kch:.0f})">'
                f'{ten(0, 150, 230, 38, .55)}'
                f'<rect x="-210" y="-10" width="420" height="200" rx="46" fill="{col}" {o(8)}/>')
        for k in range(13):
            muf += (f'<path d="M{-186 + k*31:.0f},-4 q14,70 0,146" fill="none"'
                    f' stroke="#ffffff" stroke-width="9" opacity=".2"/>')
        muf += (f'<rect x="-218" y="-44" width="436" height="56" rx="28" fill="{col}"'
                f' {o(7)} opacity=".96"/>'
                f'<rect x="-200" y="-34" width="400" height="14" rx="7" fill="#ffffff"'
                f' opacity=".18"/></g>')
    s += SL(Z_SRED, muf)
    # МАНДАРИН: шар, спираль кожуры, раскрытые дольки
    cx, cy, R = 408, 596, 168
    man = ten(cx, cy + R + 34, R * .9, 30, .55)
    man += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{ob.MANDA}" {o(9)}/>'
    man += f'<circle cx="{cx - R*.34:.0f}" cy="{cy - R*.36:.0f}" r="{R*.3:.0f}" fill="#ffc98a" opacity=".6"/>'
    # ОТКРЫТАЯ МЯКОТЬ: светлее кожуры, дольки расходятся лучами
    man += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R*.80:.0f}" fill="#fbb962"'
            f' opacity="{min(1.0, p*1.4):.2f}"/>')
    for i in range(9):
        a = -math.pi / 2 + i * (2 * math.pi / 9)
        man += (f'<path d="M{cx:.0f},{cy:.0f} L{cx + math.cos(a)*R*.78:.0f},'
                f'{cy + math.sin(a)*R*.78:.0f}" stroke="#f6e2bd" stroke-width="9"'
                f' stroke-linecap="round" opacity="{min(1.0, p*1.4)*.9:.2f}"/>')
    man += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R*.16:.0f}" fill="#f6e2bd"'
            f' opacity="{min(1.0, p*1.4)*.9:.2f}"/>')
    # две дольки отходят в сторону — «дольки раскрываются»
    for i, (dax, day) in enumerate(((1.0, .2), (.72, -.62))):
        raz = p * 118
        man += (f'<g transform="translate({cx + dax*raz:.0f},{cy + day*raz:.0f})'
                f' rotate({16 + i*26:.0f})" opacity="{min(1.0, p*1.5):.2f}">'
                f'<path d="M0,0 q{R*.5:.0f},{-R*.3:.0f} {R*.74:.0f},{R*.06:.0f}'
                f' q{-R*.3:.0f},{R*.4:.0f} {-R*.74:.0f},{-R*.06:.0f} z" fill="#fbb962" {o(5)}/>'
                f'<path d="M{R*.08:.0f},{R*.02:.0f} q{R*.38:.0f},{-R*.2:.0f} {R*.6:.0f},{R*.03:.0f}"'
                f' fill="none" stroke="#f6e2bd" stroke-width="7"/></g>')
    man += (f'<path d="M{cx:.0f},{cy-R:.0f} q16,-26 44,-22" fill="none"'
            f' stroke="{ZEL}" stroke-width="12" stroke-linecap="round"/>')
    # СПИРАЛЬ КОЖУРЫ — одной лентой свисает справа, длина растёт от t
    sp = []
    N = 52
    sx, sy = cx + R * 1.05, cy - R * .34
    for i in range(N + 1):
        u = (i / N) * p
        a = -1.4 + u * 6.9
        rr = 34 + u * 104
        sp.append((sx + math.cos(a) * rr, sy + math.sin(a) * rr * .62 + u * 268))
    if p > .03:
        man += (f'<path d="{_gladko(sp)}" fill="none" stroke="{ob.MANDA}"'
                f' stroke-width="40" stroke-linecap="round"/>')
        man += (f'<path d="{_gladko(sp)}" fill="none" stroke="#fff0dc"'
                f' stroke-width="14" stroke-linecap="round" opacity=".5"/>')
        man += (f'<circle cx="{sp[-1][0]:.0f}" cy="{sp[-1][1]:.0f}" r="22"'
                f' fill="{ob.MANDA}" {o(5)}/>')
    s += SL(Z_PERED, man)
    # КАПЛИ СОКА
    kap = ""
    rr = random.Random(5)
    for i in range(16):
        ph = rr.random()
        u = ((t * .9 + ph) % 1.0)
        a = rr.uniform(-2.6, .4)
        d = 60 + u * 300
        kap += (f'<ellipse cx="{cx + math.cos(a)*d:.0f}" cy="{cy + math.sin(a)*d + u*u*160:.0f}"'
                f' rx="{7*(1-u*.5):.1f}" ry="{11*(1-u*.5):.1f}" fill="#ffd089"'
                f' opacity="{(1-u)*.85:.2f}"/>')
    s += SL(Z_LETIT, kap)
    s += vinetka(.44)
    return s


def zapah_idet_po_komnatam(t):
    """Дом в разрезе, четыре комнаты: оранжевая струйка запаха идёт из кухни.
    Живое: струйка плывёт, дед поднимает нос и кот просыпается, малыш бежит."""
    s = SL(Z_NEBO, nebo("noch", t) + sneg_letit(t, 44))
    x0, y0, x1, y1 = 150, 220, 1770, 985
    cw, ch = (x1 - x0) / 2.0, (y1 - y0) / 2.0
    dal = (f'<path d="M{x0-70:.0f},{y0:.0f} L{(x0+x1)/2:.0f},{y0-220:.0f}'
           f' L{x1+70:.0f},{y0:.0f} Z" fill="{DOSKA2}" {o(7)}/>')
    dal += (f'<path d="M{x0-80:.0f},{y0+8:.0f} L{(x0+x1)/2:.0f},{y0-228:.0f}'
            f' L{x1+80:.0f},{y0+8:.0f} l-34,-26 L{(x0+x1)/2:.0f},{y0-196:.0f}'
            f' l{-(x1-x0)/2-46:.0f},0 Z" fill="url(#sneg)" {o(5)}/>')
    dal += f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1-x0:.0f}" height="{y1-y0:.0f}" fill="#2a2a38" {o(8)}/>'
    s += SL(Z_DAL, dal)
    # четыре комнаты
    kom = ""
    for r_ in range(2):
        for c in range(2):
            kx, ky = x0 + c * cw, y0 + r_ * ch
            tep = (r_ == 1 and c == 0)
            kom += (f'<rect x="{kx+10:.0f}" y="{ky+10:.0f}" width="{cw-20:.0f}"'
                    f' height="{ch-20:.0f}" rx="10" fill="{"#4a3a2c" if tep else "#38404f"}"/>')
            kom += (f'<rect x="{kx+10:.0f}" y="{ky+ch-70:.0f}" width="{cw-20:.0f}"'
                    f' height="60" fill="url(#pol)" opacity=".9"/>')
            kom += f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{cw:.0f}" height="{ch:.0f}" fill="none" {o(8)}/>'
    # КУХНЯ (низ слева): плита, кастрюля, пар
    kx, ky = x0, y0 + ch
    kom += teplo(kx + cw * .5, ky + ch * .55, 420, 340, .75)
    kom += (f'<rect x="{kx+120:.0f}" y="{ky+ch-230:.0f}" width="300" height="170" rx="12"'
            f' fill="url(#zhel)" {o(6)}/>')
    kom += (f'<ellipse cx="{kx+270:.0f}" cy="{ky+ch-238:.0f}" rx="94" ry="34"'
            f' fill="url(#chug)" {o(6)}/>')
    kom += baza.par(kx + 270, ky + ch - 266, t, 5, .55, 210, .4, 1.3)
    kom += (f'<rect x="{kx+470:.0f}" y="{ky+ch-300:.0f}" width="200" height="22" rx="8"'
            f' fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        kom += _banka(kx + 510 + i * 66, ky + ch - 300, 52, 78, t, (ob.ALYJ2, "#6f8c4a", CHAY)[i], i * .3)
    # ДЕД с газетой (верх слева) — поднимает нос
    nos = -9 * A.ease(A.seg(t, .5, .9))
    dx, dy = x0 + cw * .54, y0 + ch - 70
    kom += (f'<g transform="rotate({nos:.1f} {dx:.0f} {dy:.0f})">'
            + ob.figura(dx, dy, 330, t, "#2a2430", "#f0c070", False, .1, True) + '</g>')
    kom += (f'<rect x="{dx-250:.0f}" y="{dy-250:.0f}" width="210" height="160" rx="8"'
            f' fill="#e7e2d4" {o(5)} transform="rotate(-16 {dx-150:.0f} {dy-170:.0f})"/>')
    kom += (f'<path d="M{dx-236:.0f},{dy-216:.0f} h170 M{dx-236:.0f},{dy-186:.0f} h140'
            f' M{dx-236:.0f},{dy-156:.0f} h164" stroke="#8c8778" stroke-width="7" opacity=".6"/>')
    kom += _stul(dx + 100, dy, t, .54)
    # КОТ (верх справа) — просыпается
    kom += baza.kot(x0 + cw * 1.5, y0 + ch - 80, t, 1.0, "#3b3430", spit=(t < 1.1))
    kom += (f'<rect x="{x0+cw*1.18:.0f}" y="{y0+ch-150:.0f}" width="360" height="70"'
            f' rx="22" fill="{TKAN2}" {o(6)}/>')
    # МАЛЫШ (низ справа) — бежит на кухню
    beg = A.ease(A.seg(t, .55, 1.6))
    mx = x0 + cw * 1.78 - 430 * beg
    kom += ob.figura(mx, y1 - 60 + 8 * A.w(t, .32), 310, t, "#2b2436", "#ffd79a",
                     False, .3, True, 1.0, True)
    s += SL(Z_SRED, kom)
    # СТРУЙКА ЗАПАХА — из кухни через все комнаты
    put = [(x0 + 270, y0 + ch + ch - 300), (x0 + 300, y0 + ch - 60),
           (x0 + 420, y0 + ch * .5), (x0 + cw * .9, y0 + 150),
           (x0 + cw * 1.3, y0 + 180), (x0 + cw * 1.62, y0 + ch * .8),
           (x0 + cw * 1.5, y0 + ch + 140), (x0 + cw * 1.62, y1 - 160)]
    zap = (f'<path d="{_gladko(put)}" fill="none" stroke="{ob.MANDA}" stroke-width="22"'
           f' stroke-linecap="round" opacity=".5" stroke-dasharray="58 42"'
           f' stroke-dashoffset="{-t*190:.0f}"/>')
    zap += (f'<path d="{_gladko(put)}" fill="none" stroke="{SVET}" stroke-width="9"'
            f' stroke-linecap="round" opacity=".55" stroke-dasharray="30 70"'
            f' stroke-dashoffset="{-t*190:.0f}"/>')
    for i in range(7):
        u = ((t * .34 + i / 7.0) % 1.0)
        px, py = _tochka_lomanoy(put, u)
        zap += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{16 + 12*math.sin(math.pi*u):.0f}"'
                f' fill="{ob.MANDA}" opacity="{.5*(1-abs(2*u-1))+.15:.2f}"/>')
    s += SL(Z_PERED, zap + ramka_pp("oba", "#0b0d14", .55).replace("<g data-z=\"-230\">", "").replace("</g><!--/z-->", ""))
    s += vinetka(.42)
    return s


def kozhura_na_bataree(t):
    """Мандарины ложатся в варежки, камера уходит к батарее с сохнущей кожурой.
    Живое: мандарины падают в варежки, кожура загибается, над батареей дрожит воздух."""
    s = SL(Z_NEBO, _stena(t, 1380, 560, "#2d3750", "#181e2c", 900))
    dal = okno_izby(1130, 150, 520, 420, t, vid=_za_oknom(1130, 150, 520, 420, t),
                    moroz=.55)
    dal += ob.girlyanda(1050, 96, 1760, 112, t, 11, 64)
    s += SL(Z_DAL, dal)
    # ЧУГУННАЯ БАТАРЕЯ под окном
    bat = ten(1390, 960, 300, 28, .5)
    for i in range(9):
        bx = 1130 + i * 58
        bat += (f'<rect x="{bx:.0f}" y="640" width="44" height="282" rx="20"'
                f' fill="url(#chug)" {o(6)}/>')
        bat += f'<rect x="{bx+8:.0f}" y="660" width="10" height="240" rx="5" fill="#8f949a" opacity=".3"/>'
    bat += f'<rect x="1120" y="690" width="546" height="22" rx="10" fill="url(#zhel)" {o(5)}/>'
    bat += f'<rect x="1120" y="846" width="546" height="22" rx="10" fill="url(#zhel)" {o(5)}/>'
    bat += teplo(1390, 700, 420, 300, .5)
    # кожура на батарее — подсыхает и загибается
    zag = A.ease(A.seg(t, .4, 3.4))
    for i, bx in enumerate((1180, 1286, 1392, 1498, 1604)):
        bat += _kozhura(bx, 630, -14 + i * 7, .82, zag * (.5 + .12 * i))
    bat += _drozh(1140, 606, 520, t, 6, 230, .34)
    s += SL(Z_SRED, bat)
    # ДВЕ ВАРЕЖКИ на табурете, в них падают по два мандарина
    per = ten(470, 1000, 440, 34, .5)
    per += (f'<path d="M140,790 L800,790 L880,900 L60,900 Z" fill="url(#derev)" {o(7)}/>'
            f'<rect x="60" y="890" width="820" height="40" rx="14" fill="url(#derev)" {o(7)}/>'
            f'<rect x="80" y="898" width="780" height="12" rx="6" fill="#ffffff" opacity=".25"/>')
    for xx in (180, 700):
        per += f'<rect x="{xx}" y="930" width="40" height="150" fill="url(#derev)" {o(6)}/>'
    per += _rukavichka(260, 836, 1.35, ob.ALYJ, t, 0.0)
    per += _rukavichka(680, 842, 1.35, "#2f5a78", t, .3)
    for i, (mx, my, t0) in enumerate(((208, 756, .25), (310, 770, .75),
                                      (628, 760, 1.25), (734, 776, 1.75))):
        k = A.out(A.seg(t, t0, .85))
        if k <= .01:
            continue
        y = -220 + (my + 220) * k
        per += ob.mandarin(mx, y, 1.7, 0.0, t)
    per += _muka(220, 790, 560, t, 8, 9, 90, .4, .16)
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def vaza_s_mandarinami(t):
    """Дверца холодильника закрывается, мандарины катятся в стеклянную вазу.
    Живое: мандарины катятся, дверца закрывается, ваза встаёт на скатерть."""
    zak = A.ease(A.seg(t, .15, 1.2))
    s = SL(Z_NEBO, _stena(t, 480, 520, "#2b3449", "#171d2a", 820))
    # ХОЛОДИЛЬНИК слева, дверца закрывается
    hol = ten(180, 980, 150, 26, .5)
    hol += f'<rect x="40" y="200" width="300" height="760" rx="22" fill="#2b3340" {o(7)}/>'
    hol += (f'<rect x="64" y="226" width="252" height="296" rx="12" fill="#3a4654" {o(4)}/>'
            f'<rect x="64" y="542" width="252" height="392" rx="12" fill="#3a4654" {o(4)}/>')
    for i in range(3):
        hol += _banka(132 + i * 62, 500, 48, 74, t, (ob.ALYJ2, "#6f8c4a", CHAY)[i], i * .3, True)
    hol += teplo(190, 560, 230, 330, .55 * (1 - zak))
    hol += (f'<g transform="translate(40,200) scale({1-zak*.78:.3f},1)">'
            f'<rect width="300" height="760" rx="22" fill="url(#beton)" {o(7)}/>'
            f'<rect x="24" y="24" width="252" height="300" rx="14" fill="#b5bec4" opacity=".6"/>'
            f'<rect x="252" y="330" width="22" height="200" rx="11" fill="url(#zhel)" {o(4)}/>'
            f'<rect x="30" y="30" width="20" height="690" rx="10" fill="#ffffff" opacity=".3"/></g>')
    s += SL(Z_DAL, hol + ob.girlyanda(-40, 120, 860, 150, t, 9, 70))
    s += SL(Z_SRED, _skatert(60, 730, 790, t, 150))
    # ВАЗА НА НОЖКЕ встаёт в середину стола
    vst = A.over(A.seg(t, 1.0, 1.1))
    vx, vy = 560, 730
    vaz = (f'<g transform="translate({vx:.0f},{vy - 300*(1-vst):.0f})'
           f' scale({1.12 + .14*vst:.3f})">')
    vaz += ten(0, 36, 150, 26, .5)
    vaz += '<path d="M-150,-170 q22,118 150,142 q128,-24 150,-142 z" fill="url(#stekl)" opacity=".62" stroke="#d6e8f2" stroke-width="6"/>'
    vaz += '<path d="M0,-28 v54" fill="none" stroke="#cfe3ef" stroke-width="22"/>'
    vaz += '<path d="M-96,30 q96,26 192,0 q-96,16 -192,0 z" fill="#cfe3ef" stroke="#b7d2e2" stroke-width="5"/>'
    # мандарины, уже лежащие в вазе
    for i, (dx, dy) in enumerate(((-78, -122), (-6, -112), (66, -124), (-40, -186), (36, -192))):
        kk = A.out(A.seg(t, 1.5 + i * .33, .55))
        if kk > .02:
            vaz += (f'<g opacity="{kk:.2f}" transform="translate({dx},{dy - 70*(1-kk):.0f})">'
                    + ob.mandarin(0, 0, 1.25, 0.0, t) + '</g>')
    vaz += '<path d="M-130,-150 q16,96 76,126" fill="none" stroke="#ffffff" stroke-width="12" opacity=".4"/>'
    vaz += '</g>'
    # мандарины КАТЯТСЯ по столу от холодильника к вазе
    kat = ""
    for i, t0 in enumerate((.3, .62, .94)):
        k = A.ease(A.seg(t, t0, 1.25))
        if k <= .01 or k >= .999:
            continue
        mx = 120 + (vx - 150 - 120) * k
        my = 706 - 26 * math.sin(math.pi * k)
        kat += (f'<g transform="rotate({k*420:.0f} {mx:.0f} {my:.0f})">'
                + ob.mandarin(mx, my, 1.3, 0.0, t) + '</g>')
    s += SL(Z_PERED, vaz + kat + baza.svecha(760, 640, t, .2, 1.0, 96))
    s += vinetka(.42)
    return s


def semya_lepit_pelmeni(t):
    """Большой кухонный стол в мukе, вокруг вся семья: дед, мать, отец и двое детей.
    Живое: мukа летит, пельмени ложатся на доску, фигуры покачиваются."""
    s = SL(Z_NEBO, _stena(t, 960, 380, "#2f3950", "#1a202e", 1000)
           + baza.lampa(960, 330, t, 1.1, True))
    dal = ob.figura(430, 740, 620, t, "#2a2432", "#f3c884", False, .0, False)
    dal += ob.figura(760, 730, 600, t, "#31273a", "#ffd79a", True, .3, False)
    dal += ob.figura(1240, 742, 630, t, "#262031", "#f0c070", False, .6, False)
    dal += _muka(420, 640, 900, t, 14, 21, 140, .5, .35)
    s += SL(Z_DAL, dal)
    # СТОЛ в мukе
    sred = ten(960, 1030, 820, 46, .55)
    sred += f'<rect x="110" y="700" width="1700" height="46" rx="14" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="110" y="700" width="1700" height="18" rx="9" fill="{MUKA}" opacity=".75"/>'
    for xx in (210, 1640):
        sred += f'<rect x="{xx}" y="746" width="44" height="290" fill="url(#derev)" {o(6)}/>'
    r = random.Random(7)
    for i in range(16):
        sred += (f'<ellipse cx="{r.uniform(150, 1760):.0f}" cy="{r.uniform(690, 712):.0f}"'
                 f' rx="{r.uniform(24, 70):.0f}" ry="{r.uniform(5, 11):.0f}" fill="{MUKA}"'
                 f' opacity="{r.uniform(.35, .8):.2f}"/>')
    # кружочки теста
    for i, dx in enumerate((300, 420, 1420, 1540)):
        sred += (f'<ellipse cx="{dx}" cy="686" rx="54" ry="19" fill="{TESTO}" {o(5)}/>'
                 f'<ellipse cx="{dx-16}" cy="680" rx="22" ry="7" fill="#f6e9c8" opacity=".6"/>')
    # скалка
    sred += (f'<rect x="1560" y="664" width="230" height="30" rx="15" fill="url(#derev)" {o(5)}/>'
             f'<rect x="1532" y="672" width="40" height="14" rx="7" fill="url(#derev)" {o(4)}/>'
             f'<rect x="1778" y="672" width="40" height="14" rx="7" fill="url(#derev)" {o(4)}/>')
    # ДОСКА с пельменями — ложатся по одному
    sred += f'<rect x="700" y="640" width="520" height="68" rx="14" fill="url(#dosk)" {o(6)}/>'
    for i in range(14):
        k = A.over(A.seg(t, .18 + i * .11, .42))
        if k <= .02:
            continue
        px = 740 + (i % 7) * 68
        py = 660 + (i // 7) * 32
        sred += (f'<g transform="translate(0,{-90*(1-k):.0f})" opacity="{min(1.0,k):.2f}">'
                 + _pelmen(px, py, .78, -18 + (i * 29) % 36) + '</g>')
    s += SL(Z_SRED, sred)
    # ПЕРЕДНИЙ ПЛАН: отец и двое детей спиной, срезаны нижним краем
    per = ob.figura(250, 1480, 1020, t, "#191520", "#f6cf8a", False, .15, False)
    per += ob.figura(1700, 1460, 990, t, "#1c1724", "#ffd79a", False, .45, False)
    per += ob.figura(1000, 1520, 760, t, "#20192a", "#ffd79a", False, .7, False, 1.0, True)
    per += _muka(260, 760, 1400, t, 22, 5, 240, .6, .55)
    s += SL(Z_PERED, per)
    s += vinetka(.44)
    return s


def doska_s_pelmenyami_na_moroze(t):
    """Кадр надвое: балкон многоэтажки и крыльцо дома, на обоих — доска пельменей.
    Живое: доски ставят разом, пельмени белеют инеем, пар изо рта."""
    stav = A.out(A.seg(t, .2, 1.0))
    iney = A.ease(A.seg(t, 1.3, 2.6))
    s = SL(Z_NEBO, nebo("noch", t) + sneg_letit(t, 52))
    dal = panelka(-120, 1080, 900, t, 6, True, 4).replace('<g data-z="520">', '').replace('</g><!--/z-->', '')
    dal += ulica_dal(990, 880, 900, t, True, 11).replace('<g data-z="520">', '').replace('</g><!--/z-->', '')
    dal += baza.izba_snaruzhi(1180, 900, 520, t, True, True, 3)
    s += SL(Z_DAL, dal)
    # ЛЕВО — балкон многоэтажки
    lev = f'<rect x="0" y="300" width="950" height="780" fill="url(#beton)" opacity=".92" {o(6)}/>'
    lev += f'<rect x="0" y="300" width="950" height="40" fill="{BETON2}"/>'
    lev += okno_izby(90, 380, 300, 300, t, svet=True, moroz=.5, krest=True)
    lev += f'<rect x="0" y="880" width="950" height="40" rx="12" fill="url(#zhel)" {o(6)}/>'
    for i in range(9):
        lev += f'<rect x="{30 + i*104:.0f}" y="900" width="18" height="180" rx="8" fill="url(#zhel)" {o(4)}/>'
    lev += sneg_lezhit(1004, 18).replace('<g data-z="520">', '').replace('</g><!--/z-->', '')
    lev += teplo(240, 530, 420, 340, .5)
    lev += _stul(560, 1010, t, .74, False)
    lev += (f'<path d="M402,784 q88,-22 176,0 q-88,16 -176,0 z" fill="url(#sneg)" {o(4)}/>')
    for i in range(9):
        lev += (f'<ellipse cx="{36 + i*104:.0f}" cy="898" rx="22" ry="9"'
                f' fill="url(#sneg)" {o(3)}/>')
    # ПРАВО — крыльцо дома
    pra = f'<rect x="970" y="240" width="950" height="840" fill="url(#brev)" opacity=".2"/>'
    pra += brevna(970, 240, 950, 560, 92)
    pra += okno_izby(1560, 330, 290, 270, t, vid=_za_oknom(1560, 330, 290, 270, t, "#3c2a16"),
                     svet=True, moroz=.4)
    pra += baza.dver(1040, 380, 240, 420, .0, "url(#derev)", True)
    pra += f'<rect x="970" y="800" width="950" height="40" rx="10" fill="url(#dosk)" {o(6)}/>'
    pra += doski(970, 840, 950, 240, 72, True, "dosk")
    pra += f'<rect x="980" y="700" width="930" height="34" rx="16" fill="url(#derev)" {o(6)}/>'
    for i in range(6):
        pra += f'<rect x="{1040 + i*160:.0f}" y="734" width="20" height="108" rx="8" fill="url(#derev)" {o(4)}/>'
    s += SL(Z_SRED, lev + pra)
    # ДОСКИ с пельменями ставят разом
    per = ""
    for j, (bx, by) in enumerate(((330, 830), (1230, 672))):
        yy = by - 260 * (1 - stav)
        per += f'<g transform="translate(0,{yy - by:.0f})">'
        per += ten(bx + 190, by + 48, 210, 20, .5)
        per += f'<rect x="{bx:.0f}" y="{by:.0f}" width="400" height="56" rx="12" fill="url(#dosk)" {o(6)}/>'
        for i in range(12):
            px = bx + 44 + (i % 6) * 62
            py = by + 14 + (i // 6) * 26
            per += _pelmen(px, py, .72, -20 + (i * 37) % 40, iney)
        per += '</g>'
    # пар изо рта — у края каждой половины
    per += baza.par(690, 760, t, 4, .45, 190, .35, 1.2)
    per += baza.par(1030, 640, t, 4, .4, 180, .32, 1.1)
    per += f'<rect x="952" y="0" width="16" height="{H}" fill="#0b0f18" opacity=".85"/>'
    s += SL(Z_PERED, per)
    s += vinetka(.46)
    return s


def svobodnyy_stul_u_testa(t):
    """За столом в мukе свободный стул: он отодвигается, с сиденья взлетает мukа.
    Живое: стул отодвигается, мучное облачко от хлопка, кружочек теста ложится."""
    ot = A.out(A.seg(t, .25, 1.05))
    hlop = max(0.0, math.sin(math.pi * A.seg(t, 1.35, .55)))
    klad = A.over(A.seg(t, 1.9, .95))
    s = SL(Z_NEBO, _stena(t, 820, 430, "#2c3650", "#181e2c", 900)
           + baza.lampa(820, 300, t, 1.0, True))
    # дальняя сторона стола: тесто, скалка, миска
    dal = f'<rect x="120" y="590" width="1700" height="34" rx="12" fill="url(#derev)" {o(6)}/>'
    for i, dx in enumerate((300, 430, 1340, 1470, 1600)):
        dal += (f'<ellipse cx="{dx}" cy="582" rx="48" ry="17" fill="{TESTO}" {o(5)}/>'
                f'<ellipse cx="{dx-14}" cy="577" rx="20" ry="6" fill="#f6e9c8" opacity=".6"/>')
    dal += (f'<rect x="1540" y="548" width="220" height="28" rx="14" fill="url(#derev)" {o(5)}/>')
    dal += baza.krynka(230, 580, 1.05)
    dal += _muka(260, 560, 1300, t, 14, 31, 130, .45, .3)
    s += SL(Z_DAL, dal)
    # СТОЛ
    sred = ten(960, 1040, 800, 44, .55)
    sred += f'<rect x="120" y="700" width="1700" height="46" rx="14" fill="url(#derev)" {o(7)}/>'
    sred += f'<rect x="120" y="700" width="1700" height="18" rx="9" fill="{MUKA}" opacity=".8"/>'
    for xx in (220, 1650):
        sred += f'<rect x="{xx}" y="746" width="44" height="294" fill="url(#derev)" {o(6)}/>'
    r = random.Random(23)
    for i in range(14):
        sred += (f'<ellipse cx="{r.uniform(160, 1770):.0f}" cy="{r.uniform(690, 712):.0f}"'
                 f' rx="{r.uniform(26, 76):.0f}" ry="{r.uniform(5, 12):.0f}" fill="{MUKA}"'
                 f' opacity="{r.uniform(.3, .8):.2f}"/>')
    s += SL(Z_SRED, sred)
    # СВОБОДНЫЙ СТУЛ отодвигается, с сиденья бьёт мучное облачко
    per = _stul(860, 1046, t, .96, True, 180 * ot)
    cx = 860 + 180 * ot
    per += (f'<ellipse cx="{cx:.0f}" cy="{1046-222:.0f}" rx="{104 + 26*hlop:.0f}"'
            f' ry="{16 + 6*hlop:.0f}" fill="{MUKA}" opacity="{.35 + .45*hlop:.2f}"/>')
    per += _muka(cx - 120, 1046 - 226, 240, t, 16, 13, 230, 1.0, .55 * (.3 + .7 * hlop))
    # кружочек теста и ложка фарша перед стулом
    if klad > .02:
        ky = 672 - 150 * (1 - klad)
        per += (f'<g opacity="{min(1.0,klad):.2f}">'
                f'<ellipse cx="{cx:.0f}" cy="{ky:.0f}" rx="{72*klad:.0f}" ry="{26*klad:.0f}"'
                f' fill="{TESTO}" {o(6)}/>'
                f'<ellipse cx="{cx-20:.0f}" cy="{ky-7:.0f}" rx="{28*klad:.0f}"'
                f' ry="{9*klad:.0f}" fill="#f6e9c8" opacity=".6"/></g>')
        per += (f'<g transform="translate({cx+150:.0f},{672:.0f}) rotate(-14)">'
                f'{ten(0, 18, 60, 12, .45)}'
                f'<rect x="34" y="-10" width="190" height="20" rx="10" fill="url(#zhel)" {o(4)}/>'
                f'<ellipse rx="52" ry="26" fill="url(#zhel)" {o(5)}/>'
                f'<ellipse cx="0" cy="-4" rx="38" ry="17" fill="{FARSH}" {o(3)}/>'
                f'<ellipse cx="-14" cy="-10" rx="12" ry="5" fill="#c06a54" opacity=".7"/></g>')
    s += SL(Z_PERED, per)
    s += vinetka(.44)
    return s


def babushka_i_vnuki_v_muke(t):
    """Сегодняшняя кухня: бабушка и двое внukов, на доске три ровных ряда по десять.
    Живое: ряды пельменей растут, внuk сдувает мukу, бабушка поправляет пельмень."""
    s = SL(Z_NEBO, _stena(t, 400, 420, "#2e3850", "#1a202e", 860))
    # кухонный гарнитур слева, в полосе 0-830
    dal = f'<rect x="0" y="180" width="{BAND}" height="250" rx="14" fill="url(#beton)" {o(6)}/>'
    for i in range(4):
        dal += (f'<rect x="{20 + i*200:.0f}" y="196" width="180" height="218" rx="10"'
                f' fill="url(#derev)" {o(5)}/>'
                f'<rect x="{34 + i*200:.0f}" y="210" width="152" height="60" rx="8"'
                f' fill="#ffffff" opacity=".12"/>'
                f'<rect x="{90 + i*200:.0f}" y="384" width="42" height="12" rx="6" fill="url(#zhel)"/>')
    dal += ob.girlyanda(-30, 110, 850, 140, t, 10, 60)
    s += SL(Z_DAL, dal)
    # БАБУШКА и ДВОЕ ВНУКОВ
    sred = ob.figura(210, 818, 470, t, "#2a2432", "#f3c884", True, .1, False)
    sred += ob.figura(470, 820, 300, t, "#272134", "#ffd79a", False, .45, True)
    sred += ob.figura(650, 822, 286, t, "#231e2e", "#ffd79a", False, .8, True, 1.0, True)
    # внuk сдувает мukу — облачко от его лица к доске
    sdu = max(0.0, math.sin(math.pi * ((t / 2.6) % 1.0))) ** 2
    sred += _muka(430, 700, 300, t, 14, 29, 200, .9, .5 * (.25 + .75 * sdu))
    sred += (f'<ellipse cx="520" cy="712" rx="{90*sdu + 20:.0f}" ry="{26*sdu + 8:.0f}"'
             f' fill="{MUKA}" opacity="{.5*sdu:.2f}"/>')
    s += SL(Z_SRED, sred)
    # ДОСКА: три ряда по десять
    per = ten(430, 1046, 390, 28, .55)
    per += (f'<path d="M50,812 L810,812 L860,1012 L0,1012 Z" fill="url(#dosk)" {o(7)}/>')
    per += (f'<path d="M52,818 L806,818" fill="none" stroke="{MUKA}" stroke-width="10" opacity=".55"/>')
    per += _muka(40, 1000, 820, t, 14, 3, 120, .5, .35)
    rost = A.seg(t, .15, 2.6)
    for row in range(3):
        for i in range(10):
            idx = row * 10 + i
            k = A.over(A.seg(t, .1 + idx * .055, .35))
            if k <= .02:
                continue
            sc = .62 + row * .07
            px = 86 + i * 72 + row * 10
            py = 856 + row * 62
            popr = 0.0
            if idx == 24:                       # бабушка поправляет один пельмень
                popr = 9 * A.w(t, 1.5)
            per += (f'<g transform="translate({popr:.1f},{-70*(1-k) + popr*.3:.1f})"'
                    f' opacity="{min(1.0,k):.2f}">'
                    + _pelmen(px, py, sc, -16 + (idx * 31) % 34) + '</g>')
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def stopka_zhurnalov(t):
    """Журнальный столик, стопка глянцевых журналов без названий; верхний раскрывается.
    Живое: журнал раскрывается, страницы идут веером, закладка выпадает."""
    otk = A.ease(A.seg(t, .35, 1.5))
    ver = A.seg(t, 1.3, 1.8)
    s = SL(Z_NEBO, _stena(t, 1500, 420, "#2a3348", "#171d2a", 880))
    dal = ob.elka(1640, 1020, 560, t, seed=12)
    dal += (f'<path d="M-60,1080 L-60,700 q30,-80 150,-80 h520 q70,0 70,80 v380 z"'
            f' fill="#3c4a63" {o(7)}/>')
    dal += (f'<rect x="-40" y="800" width="700" height="150" rx="34" fill="#4a5a76" {o(6)}/>')
    dal += (f'<rect x="-20" y="690" width="300" height="120" rx="26" fill="#55668a" {o(5)}/>'
            f'<rect x="300" y="690" width="300" height="120" rx="26" fill="#55668a" {o(5)}/>')
    dal += (f'<rect x="40" y="712" width="200" height="22" rx="11" fill="#ffffff" opacity=".14"/>')
    s += SL(Z_DAL, dal)
    # столик + стопка
    sred = ten(960, 1040, 460, 32, .55)
    sred += f'<rect x="500" y="790" width="920" height="34" rx="12" fill="url(#derev)" {o(7)}/>'
    for xx in (570, 1300):
        sred += f'<rect x="{xx}" y="824" width="36" height="216" fill="url(#derev)" {o(6)}/>'
    for i in range(5):
        sred += (f'<rect x="{540 + (i % 2)*16:.0f}" y="{770 - i*22:.0f}" width="760"'
                 f' height="24" rx="6" fill="{("#c2402c", "#2f5a78", "#d8a63a", "#3f6b4a", "#8d3a5e")[i]}"'
                 f' {o(5)}/>')
        sred += (f'<rect x="{546 + (i % 2)*16:.0f}" y="{772 - i*22:.0f}" width="748"'
                 f' height="7" rx="4" fill="#ffffff" opacity=".28"/>')
    s += SL(Z_SRED, sred)
    # ВЕРХНИЙ ЖУРНАЛ раскрывается сам
    bx, by = 920, 660
    per = ten(bx, by + 44, 420, 26, .5)
    per += (f'<rect x="{bx:.0f}" y="{by-14:.0f}" width="380" height="26" rx="6"'
            f' fill="#f3eee0" {o(5)}/>')
    # ОБЛОЖКА откидывается влево, под ней разворот двух страниц
    kr = max(.04, math.cos(math.pi * .92 * otk))
    per += (f'<g transform="translate({bx:.0f},{by:.0f}) scale({kr:.3f},1)">'
            f'<path d="M0,10 L-376,-14 L-376,-44 L0,-20 Z" fill="{ob.ALYJ}" {o(5)}/>'
            f'<path d="M-30,-18 L-352,-40" stroke="#ffffff" stroke-width="9" opacity=".3"/></g>')
    # РАЗВОРОТ: две страницы под углом, обе с полосами текста (без букв)
    for sgn in (-1, 1):
        per += (f'<path d="M0,0 L{sgn*372:.0f},{-34:.0f} L{sgn*366:.0f},{14:.0f} L0,{34:.0f} Z"'
                f' fill="#faf6ea" {o(5)} transform="translate({bx:.0f},{by-14:.0f})"/>')
        for i in range(5):
            per += (f'<path d="M{bx + sgn*60:.0f},{by - 26 + i*11:.0f}'
                    f' L{bx + sgn*(300 - i*34):.0f},{by - 46 + i*11:.0f}" stroke="#93a2b2"'
                    f' stroke-width="6" opacity=".7" stroke-linecap="round"/>')
    per += (f'<rect x="{bx-7:.0f}" y="{by-54:.0f}" width="14" height="92" rx="7"'
            f' fill="#e2dbc8" {o(4)}/>')
    # СТРАНИЦЫ ВЕЕРОМ: три листа в перевороте, выгнутые дугой
    for i in range(3):
        k = A.ease(A.seg(t, 1.0 + i * .34, 1.0))
        if k <= .02:
            continue
        u = 1 - 2 * k
        per += (f'<path d="M{bx:.0f},{by-14:.0f} q{u*230:.0f},{-150 - 40*abs(u):.0f}'
                f' {u*376:.0f},{-34:.0f} q{-u*150:.0f},{70:.0f} {-u*376:.0f},{48:.0f} z"'
                f' fill="#fdfaf0" stroke="#cdc2a6" stroke-width="4" opacity=".95"/>')
    s += SL(Z_PERED, per)
    # ЗАКЛАДКА выпадает
    if ver > .01:
        zx = bx - 120 + 230 * ver
        zy = by + 20 + 420 * ver * ver
        s += SL(Z_LETIT, f'<g transform="translate({zx:.0f},{zy:.0f}) rotate({ver*300:.0f})">'
                f'<rect x="-14" y="-70" width="28" height="140" rx="8" fill="{ob.ZOLOTO}" {o(4)}/>'
                f'<path d="M-14,70 l14,-22 l14,22 z" fill="{ob.ZOLOTO2}"/></g>')
    s += vinetka(.44)
    return s


def hozyayka_goda_za_stolom(t):
    """Хозяйка года с салфеткой на шее: на столе по одному встают зелень,
    огурцы с редиской, сыр и молоко. Живое: она жуёт, угощения появляются, бубенчик качается."""
    s = SL(Z_NEBO, _stena(t, 380, 460, "#2c3650", "#181e2c", 860)
           + ob.girlyanda(-40, 120, 870, 150, t, 10, 70))
    dal = (f'<rect x="20" y="300" width="250" height="430" rx="12" fill="url(#derev)" {o(6)}/>'
           f'<rect x="40" y="326" width="210" height="180" rx="8" fill="url(#stekl)" opacity=".6" {o(4)}/>')
    for i in range(4):
        dal += _banka(72 + i * 52, 500, 44, 72, t, (ob.ALYJ2, "#6f8c4a", CHAY, "#7a4a2a")[i], i * .3, True)
    dal += baza.hodiki(170, 230, t, .7)
    s += SL(Z_DAL, dal)
    # ХОЗЯЙКА ГОДА за столом: ноги скрывает скатерть
    koz = ob.koza(286, 884, t, .80, 0.0, True, .0)
    # салфетка на шее — белый треугольник на груди
    koz += (f'<g transform="translate(404,712) rotate({2.4*A.w(t,2.4,.3):.1f})">'
            f'<path d="M-52,-26 q52,-22 104,0 l-24,112 q-28,14 -56,0 z" fill="#f6f2e4" {o(6)}/>'
            f'<path d="M-42,-12 q42,-16 84,0" fill="none" stroke="{ob.ALYJ}" stroke-width="7"/></g>')
    # петрушка во рту: жуёт
    zh = 6 * A.w(t, .72)
    koz += (f'<g transform="translate({516 + zh*.4:.0f},{596 + zh:.0f})">'
            + _zelen(0, 0, t, .5, 5, .6) + '</g>')
    s += SL(Z_SRED, koz)
    # СТОЛ ПЕРЕД НЕЙ + угощения по одному
    per = _skatert(-60, 760, 900, t, 180)
    for i, (f, fx, t0) in enumerate(((0, 480, 1.1), (1, 620, 2.2), (2, 760, 3.4), (3, 862, 4.6))):
        k = A.over(A.seg(t, t0, .9))
        if k <= .02:
            continue
        if f == 0:
            per += _zelen(fx, 752, t, .88, 9, i * .2, None, k)
        elif f == 1:
            per += _ogurcy(fx, 752, .82, k)
        elif f == 2:
            per += _syr(fx, 752, .82, k)
        else:
            per += (f'<g opacity="{min(1.0,k):.2f}" transform="translate(0,{-120*(1-k):.0f})">'
                    + _kuvshin(fx, 752, .72) + '</g>')
    per += baza.svecha(120, 700, t, .4, 1.0, 100)
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def blyudo_pod_kryshkoy_unosyat(t):
    """Блюдо под блестящей крышкой уплывает на кухню, хозяйка года выдыхает.
    Живое: блюдо уплывает, из-под крышки идёт пар, хозяйка выдыхает."""
    p = A.ease(A.seg(t, .30, 2.40))
    s = SL(Z_NEBO, _stena(t, 1620, 520, "#2b3449", "#171d2a", 820))
    # дверь кухни справа, свет оттуда
    dal = f'<rect x="1430" y="210" width="360" height="760" rx="10" fill="#1b2029" {o(7)}/>'
    dal += (f'<rect x="1468" y="230" width="300" height="720" rx="8" fill="{SVET}"'
            f' opacity="{.42 + .1*abs(A.w(t, 4.0)):.2f}"/>')
    dal += baza.luch(1420, 210, 380, 870, t, .18)
    dal += baza.dver(1150, 240, 290, 720, .65, "url(#derev)", True)
    dal += teplo(1620, 560, 460, 480, .6)
    s += SL(Z_DAL, dal)
    # хозяйка года за столом слева, выдыхает
    sred = ob.koza(300, 900, t, .86, 0.0, True, .2)
    vyd = max(0.0, math.sin(math.pi * A.seg(t, 1.9, 1.0)))
    for i in range(4):
        u = ((t * .6 + i * .25) % 1.0)
        sred += (f'<ellipse cx="{582 + 130*u:.0f}" cy="{570 - 50*u:.0f}"'
                 f' rx="{16 + 52*u:.0f}" ry="{(16 + 52*u)*.6:.0f}" fill="#f2f6fa"'
                 f' opacity="{.55*vyd*(1-u)*(1-u):.2f}"/>')
    s += SL(Z_SRED, sred + _skatert(-40, 740, 940, t, 170))
    # БЛЮДО ПОД КРЫШКОЙ уплывает к двери (прихватки — не рukи)
    bx = 700 + 700 * p
    by = 690 - 70 * math.sin(math.pi * p)
    per = f'<g transform="translate({bx:.0f},{by:.0f}) scale({1 - .22*p:.3f})">'
    per += ten(0, 96, 190, 28, .5)
    per += _blyudo(0, 60, 196, t, "url(#krem)")
    per += (f'<path d="M-178,56 q14,-146 178,-150 q164,4 178,150 q-178,44 -356,0 z"'
            f' fill="url(#zhel)" {o(7)}/>')
    per += '<path d="M-130,10 q80,-96 190,-70" fill="none" stroke="#ffffff" stroke-width="22" opacity=".45"/>'
    per += f'<circle cx="0" cy="-104" r="26" fill="url(#zol)" {o(5)}/>'
    for sgn in (-1, 1):
        per += (f'<path d="M{sgn*174:.0f},54 q{sgn*62:.0f},-6 {sgn*70:.0f},50'
                f' q{-sgn*10:.0f},44 {-sgn*66:.0f},36 z" fill="{ob.ALYJ}" {o(6)}/>')
        for k in range(3):
            per += (f'<path d="M{sgn*(182 + k*18):.0f},58 v70" fill="none"'
                    f' stroke="#ffffff" stroke-width="5" opacity=".22"/>')
    per += '</g>'
    per += baza.par(bx - 110, by - 54, t, 5, .5, 240, .4, 1.3)
    per += baza.par(bx + 110, by - 48, t, 4, .45, 220, .34, 1.2)
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def babushkin_nakrytyy_stol(t):
    """Раздвинутый стол под ковром на стене, заставлен посудой без просвета;
    бабушка со спины ставит последнюю вазочку. Живое: вазочка встаёт, графин
    поблёскивает, от миски идёт пар."""
    vst = A.over(A.seg(t, .7, 1.1))
    s = SL(Z_NEBO, _stena(t, 1100, 380, "#2b3449", "#171d2a", 980))
    s += kvartira_veschi(1180, 980, 700, t, 11)
    # ковёр на стене слева
    dal = f'<rect x="90" y="190" width="820" height="540" rx="14" fill="{ob.ALYJ2}" {o(7)}/>'
    dal += f'<rect x="124" y="222" width="752" height="476" rx="10" fill="none" stroke="{ob.ZOLOTO}" stroke-width="9" opacity=".8"/>'
    for i in range(5):
        dal += (f'<path d="M150,{266 + i*96:.0f} q350,52 700,0" fill="none"'
                f' stroke="{ob.ZOLOTO}" stroke-width="7" opacity=".6"/>')
    for i in range(4):
        dal += (f'<path d="M{260 + i*170:.0f},300 l60,120 l-60,120 l-60,-120 z"'
                f' fill="{ob.ZOLOTO2}" opacity=".5"/>')
    dal += teplo(500, 420, 520, 380, .35)
    s += SL(Z_DAL, dal)
    # СТОЛ без просвета
    sred = ten(960, 1046, 840, 44, .55)
    sred += f'<rect x="90" y="760" width="1740" height="46" rx="14" fill="url(#derev)" {o(7)}/>'
    sred += _skatert(90, 760, 1740, t, 170, "url(#rush)", ob.ALYJ, 8.0, .2, 7)
    r = random.Random(33)
    poz = []
    for i in range(11):
        poz.append((180 + i * 156, 748 - (i % 3) * 10))
    for i, (px, py) in enumerate(poz):
        k = i % 5
        if k == 0:
            sred += _blyudo(px, py, 92, t, "url(#krem)", ob.ZOLOTO, i * .2)
            sred += (f'<ellipse cx="{px:.0f}" cy="{py-12:.0f}" rx="60" ry="19"'
                     f' fill="{("#9c4a3a", "#6f8c4a", CHAY, "#8d3a5e")[i % 4]}" opacity=".9"/>')
        elif k == 1:
            sred += _banka(px, py + 8, 92, 148, t, (ob.ALYJ2, "#6f8c4a", CHAY)[i % 3], i * .17, False)
        elif k == 2:
            sred += baza.krynka(px, py + 6, 1.25)
        elif k == 3:
            # графин поблёскивает
            bl = .3 + .55 * abs(A.w(t, 2.4, i * .2))
            sred += (f'<g transform="translate({px:.0f},{py+8:.0f})">{ten(0, 10, 54, 12, .45)}'
                     f'<path d="M-46,0 q-12,-92 10,-124 l0,-56 q22,-10 44,0 l0,56'
                     f' q22,32 10,124 z" fill="url(#stekl)" opacity=".8" {o(5)}/>'
                     f'<rect x="-14" y="-200" width="28" height="26" rx="8" fill="url(#zhel)" {o(4)}/>'
                     f'<path d="M-30,-70 q30,16 60,0" fill="none" stroke="{ob.ALYJ}" stroke-width="22" opacity=".55"/>'
                     f'<rect x="-32" y="-116" width="14" height="92" rx="7" fill="#ffffff"'
                     f' opacity="{bl:.2f}"/></g>')
        else:
            sred += _syr(px, py, .8, 1.0)
    # пар от миски
    sred += baza.par(620, 706, t, 5, .5, 230, .38, 1.3)
    sred += baza.par(1250, 700, t, 4, .45, 200, .32, 1.2)
    s += SL(Z_SRED, sred)
    # БАБУШКА со спины ставит последнюю вазочку
    per = ob.figura(1480, 1080, 680, t, "#221c2c", "#f3c884", True, .1, False)
    vx, vy = 1230, 742
    per += (f'<g transform="translate(0,{-280*(1-vst):.0f})" opacity="{min(1.0,vst+.2):.2f}">'
            f'{ten(vx, vy+18, 58, 14, .45)}'
            f'<path d="M{vx-62:.0f},{vy-92:.0f} q62,66 124,0 q-20,88 -62,96'
            f' q-42,-8 -62,-96 z" fill="url(#stekl)" opacity=".82" {o(5)}/>'
            f'<ellipse cx="{vx:.0f}" cy="{vy-86:.0f}" rx="62" ry="18" fill="#f0c86a" {o(4)}/>'
            f'<rect x="{vx-26:.0f}" y="{vy-2:.0f}" width="52" height="18" rx="8" fill="#cfe3ef" {o(4)}/>'
            f'<path d="M{vx-44:.0f},{vy-70:.0f} q10,56 30,70" fill="none" stroke="#ffffff"'
            f' stroke-width="9" opacity=".45"/></g>')
    per += _stul(330, 1080, t, .76)
    s += SL(Z_PERED, per)
    s += vinetka(.44)
    return s


def verhnyaya_polka_s_pripasami(t):
    """Верхняя полка шкафа снизу, как смотрит ребёнок: банка, плоская банка,
    коробка с бантом. Живое: ребёнок тянется на цыпочках, бант качается, банки поблёскивают."""
    tyan = abs(math.sin(math.pi * ((t / 2.2) % 1.0)))
    s = SL(Z_NEBO, _stena(t, 960, 300, "#29324a", "#161b28", 980))
    # корпус шкафа, вид снизу: верх далеко, низ уходит на зрителя
    dal = (f'<path d="M150,120 L1770,120 L1700,760 L220,760 Z" fill="#3a3024" {o(8)}/>')
    dal += (f'<path d="M200,180 L1720,180 L1664,560 L256,560 Z" fill="#2b2419" opacity=".9"/>')
    dal += teplo(960, 460, 760, 420, .4)
    s += SL(Z_DAL, dal)
    # ПРИПАСЫ на полке: низ предметов скрыт передней кромкой доски
    sred = ""
    sred += _banka(520, 560, 190, 280, t, "#6f8c4a", .1, True)
    for i in range(6):                       # «нарисованный горошек» — зелёные точки
        sred += (f'<circle cx="{470 + (i % 3)*48:.0f}" cy="{430 + (i//3)*54:.0f}" r="22"'
                 f' fill="#9ec266" opacity=".85" stroke="#4f6b31" stroke-width="4"/>')
    # плоская банка со шпротами
    sred += ten(900, 574, 150, 20, .45)
    sred += (f'<rect x="770" y="470" width="270" height="96" rx="16" fill="url(#zhel)" {o(6)}/>')
    sred += (f'<rect x="790" y="484" width="230" height="30" rx="12" fill="#cfd6dd" opacity=".55"/>')
    bl = .3 + .5 * abs(A.w(t, 2.8, .4))
    sred += f'<rect x="800" y="488" width="60" height="18" rx="9" fill="#ffffff" opacity="{bl:.2f}"/>'
    sred += f'<circle cx="1010" cy="480" r="16" fill="#9aa4ad" {o(4)}/>'
    # коробка конфет с бантом
    sred += ten(1340, 578, 190, 22, .5)
    sred += f'<rect x="1150" y="402" width="390" height="170" rx="14" fill="{ob.ALYJ}" {o(7)}/>'
    sred += f'<rect x="1150" y="402" width="390" height="22" rx="10" fill="#ffffff" opacity=".28"/>'
    sred += f'<rect x="1320" y="402" width="50" height="170" fill="{ob.ZOLOTO}" opacity=".9"/>'
    sred += f'<rect x="1150" y="470" width="390" height="40" fill="{ob.ZOLOTO}" opacity=".9"/>'
    ban = 9 * A.w(t, 2.3)
    sred += (f'<g transform="translate(1345,420) rotate({ban:.1f})">'
             f'<path d="M0,0 q-96,-64 -104,-6 q-8,54 104,6 z" fill="{ob.ZOLOTO}" {o(5)}/>'
             f'<path d="M0,0 q96,-64 104,-6 q8,54 -104,6 z" fill="{ob.ZOLOTO}" {o(5)}/>'
             f'<circle r="20" fill="{ob.ZOLOTO2}" {o(4)}/>'
             f'<path d="M-24,10 q-30,60 -70,76 M24,10 q30,60 70,76" fill="none"'
             f' stroke="{ob.ZOLOTO}" stroke-width="12" stroke-linecap="round"/></g>')
    s += SL(Z_SRED, sred)
    # ПЕРЕДНЯЯ КРОМКА доски и ребёнок на цыпочках
    per = (f'<path d="M228,556 L1692,556 L1720,660 L200,660 Z" fill="url(#derev)" {o(7)}/>')
    per += f'<path d="M232,562 L1688,562" fill="none" stroke="#ffffff" stroke-width="7" opacity=".25"/>'
    bx, bby = 1160, 1080
    per += (f'<g transform="translate(0,{-44*tyan:.1f})">'
            + ob.figura(bx, bby, 560, t, "#1d1826", "#ffd79a", False, .2, True)
            + f'<ellipse cx="{bx-34:.0f}" cy="{bby-6 + 44*tyan:.0f}" rx="38" ry="13"'
            f' fill="#1a1522" opacity=".85"/>'
            f'<ellipse cx="{bx+40:.0f}" cy="{bby-6 + 44*tyan:.0f}" rx="38" ry="13"'
            f' fill="#1a1522" opacity=".85"/></g>')
    s += SL(Z_PERED, per)
    s += vinetka(.5)
    return s


def pogreb_s_letnimi_bankami(t):
    """Погреб со светом фонарика: луч идёт по банкам, самая красивая поднимается
    к люку. Живое: луч идёт по полкам, банка поднимается, паутинка качается."""
    pod = A.ease(A.seg(t, 4.0, 2.6))
    a = -58 + 30 * A.w(t, 6.0)
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1a1510"/>'
           + kladka(-60, -40, W + 120, H + 80, 86, "#3a2f23"))
    # ПОЛКИ С БАНКАМИ
    dal = ""
    for row, py in enumerate((420, 650, 880)):
        dal += (f'<rect x="60" y="{py:.0f}" width="1300" height="26" rx="8"'
                f' fill="url(#derev)" {o(6)}/>')
        dal += (f'<path d="M140,{py+26:.0f} l26,46 M1240,{py+26:.0f} l-26,46" {o(5)} fill="none"/>')
        for i in range(8):
            bx = 130 + i * 156
            col = ("#b63b27", "#6f8c4a", CHAY, "#7a4a2a", "#8d3a5e")[(i + row) % 5]
            dal += _banka(bx, py, 104, 150 - (row % 2) * 16, t, col, (i + row) * .13, True)
    dal += teplo(300, 940, 520, 300, .22)
    s += SL(Z_DAL, dal)
    # ЛУЧ ФОНАРИКА
    fx, fy = 180, 1040
    ar = math.radians(a)
    L = 1500
    sred = (f'<path d="M{fx:.0f},{fy:.0f} L{fx + math.cos(ar-.22)*L:.0f},'
            f'{fy + math.sin(ar-.22)*L:.0f} L{fx + math.cos(ar+.22)*L:.0f},'
            f'{fy + math.sin(ar+.22)*L:.0f} Z" fill="{SVET}" opacity=".16"/>')
    sred += (f'<path d="M{fx:.0f},{fy:.0f} L{fx + math.cos(ar-.09)*L:.0f},'
             f'{fy + math.sin(ar-.09)*L:.0f} L{fx + math.cos(ar+.09)*L:.0f},'
             f'{fy + math.sin(ar+.09)*L:.0f} Z" fill="{SVET}" opacity=".2"/>')
    sred += teplo(fx + math.cos(ar) * 760, fy + math.sin(ar) * 760, 300, 260, .45)
    sred += (f'<rect x="{fx-60:.0f}" y="{fy-40:.0f}" width="150" height="56" rx="20"'
             f' fill="url(#zhel)" {o(6)} transform="rotate({a:.0f} {fx:.0f} {fy:.0f})"/>')
    # ВЫБРАННАЯ БАНКА поднимается к люку
    byx = 598
    byy = 650 - (650 - 220) * pod
    sred += (f'<g transform="translate({28*pod:.0f},0)">'
             + _banka(byx, byy, 128, 190, t, "#b63b27", .0, True, True)
             + f'<rect x="{byx-72:.0f}" y="{byy-196:.0f}" width="144" height="202" rx="26"'
               f' fill="none" stroke="{ob.ZOLOTO}" stroke-width="7"'
               f' opacity="{.45 + .45*abs(A.w(t, 1.8)):.2f}"/>' + '</g>')
    sred += teplo(byx, byy - 90, 230, 230, .4 * pod)
    s += SL(Z_SRED, sred)
    # ЛЮК сверху и ПАУТИНКА в углу
    per = (f'<path d="M520,-20 L1180,-20 L1120,210 L580,210 Z" fill="#101722"/>'
           f'<path d="M560,0 L1140,0 L1096,180 L604,180 Z" fill="#93b6cf"'
           f' opacity="{.35 + .1*abs(A.w(t, 5.0)):.2f}"/>')
    per += baza.luch(600, 180, 480, 760, t, .13)
    per += (f'<path d="M500,-20 L560,0 L604,180 L540,200 Z" fill="url(#dosk)" {o(6)}/>')
    kch = 2.6 * A.w(t, 4.4)
    per += f'<g transform="rotate({kch:.2f} 1880 40)">'
    for i in range(5):
        rr = 70 + i * 62
        per += (f'<path d="M1880,{40:.0f} m{-rr:.0f},0 q{rr*.5:.0f},{rr*.55:.0f} {rr:.0f},{rr:.0f}"'
                f' fill="none" stroke="#c9d6e2" stroke-width="3" opacity=".35"/>')
    for i in range(6):
        aa = math.pi * (.5 + i * .09)
        per += (f'<path d="M1880,40 L{1880 + math.cos(aa)*400:.0f},{40 + abs(math.sin(aa))*400:.0f}"'
                f' stroke="#c9d6e2" stroke-width="3" opacity=".3"/>')
    per += '</g>'
    per += ramka_pp("levo", "#070a0e", .8).replace('<g data-z="-230">', '').replace('</g><!--/z-->', '')
    s += SL(Z_PERED, per)
    s += vinetka(.56)
    return s


def polka_kuhonnogo_shkafa(t):
    """Люк погреба стал дверцей кухонного шкафа: она открывается, на полке те же
    припасы, только поменьше. Живое: дверца открывается, банки поблёскивают,
    свет кухни ложится на полку."""
    otk = A.ease(A.seg(t, .35, 1.5))
    plit = f'<rect width="{W}" height="{H}" fill="#2b3a4e"/>'
    for r_ in range(3):
        for c in range(int(W / 120) + 1):
            plit += (f'<rect x="{c*120 + (0 if r_ % 2 == 0 else 60):.0f}" y="{r_*100:.0f}"'
                     f' width="112" height="92" rx="8" fill="#5f7183" opacity=".8"'
                     f' stroke="#3d4e60" stroke-width="4"/>')
    plit += f'<rect y="300" width="{W}" height="{H-300}" fill="#2b3a4e"/>'
    s += SL(Z_NEBO, plit)
    # корпус шкафа и полка с припасами
    dal = ten(960, 1024, 640, 30, .5)
    dal += f'<rect x="300" y="160" width="1320" height="780" rx="16" fill="#3d3225" {o(8)}/>'
    dal += f'<rect x="340" y="200" width="1240" height="700" rx="10" fill="#2c2419"/>'
    dal += teplo(960, 560, 640, 400, .45 * otk)
    for row, py in enumerate((520, 830)):
        dal += (f'<rect x="340" y="{py:.0f}" width="1240" height="22" rx="8"'
                f' fill="url(#derev)" {o(5)}/>')
        for i in range(7):
            bx = 420 + i * 190
            col = ("#b63b27", "#6f8c4a", CHAY, "#7a4a2a", "#8d3a5e")[(i + row) % 5]
            dal += _banka(bx, py, 86, 118 - (row % 2) * 12, t, col, (i + row) * .15, True)
    # коробка с бантом на верхней полке — та же, что была на шкафу
    dal += f'<rect x="1300" y="412" width="250" height="106" rx="10" fill="{ob.ALYJ}" {o(6)}/>'
    dal += f'<rect x="1300" y="450" width="250" height="26" fill="{ob.ZOLOTO}" opacity=".9"/>'
    dal += f'<rect x="1402" y="412" width="32" height="106" fill="{ob.ZOLOTO}" opacity=".9"/>'
    s += SL(Z_DAL, dal)
    # свет кухни падает на полку
    s += SL(Z_SRED, baza.luch(240, 60, 520, 900, t, .2 * otk)
            + f'<rect x="340" y="200" width="1240" height="700" fill="{SVET}" opacity="{.1*otk:.2f}"/>')
    # ДВЕРЦА открывается
    per = (f'<g transform="translate(300,160) scale({1 - otk*.78:.3f},1)">'
           f'<rect width="1320" height="780" rx="16" fill="url(#derev)" {o(8)}/>'
           f'<rect x="60" y="60" width="1200" height="660" rx="12" fill="none"'
           f' stroke="{DOSKA2}" stroke-width="12"/>'
           f'<rect x="90" y="90" width="60" height="600" rx="30" fill="#ffffff" opacity=".2"/>'
           f'<rect x="1200" y="360" width="34" height="120" rx="17" fill="url(#zhel)" {o(5)}/></g>')
    per += f'<rect x="120" y="940" width="1680" height="44" rx="14" fill="url(#beton)" {o(7)}/>'
    per += f'<rect x="120" y="940" width="1680" height="14" rx="7" fill="#ffffff" opacity=".22"/>'
    per += _banka(400, 940, 92, 126, t, "#6f8c4a", .5, True)
    per += baza.krynka(1600, 936, 1.1)
    s += SL(Z_PERED, per)
    s += vinetka(.42)
    return s


def otkrytaya_korobka_konfet(t):
    """Коробка конфет на праздничной скатерти, крышка снимается сама; на миг
    коробка становится хрустальной салатницей. Живое: крышка снимается,
    золотые бумажки блестят, коробка превращается и возвращается."""
    kr = A.out(A.seg(t, .35, 1.1))
    mor = max(0.0, math.sin(math.pi * A.seg(t, 1.45, .95)))
    s = SL(Z_NEBO, _stena(t, 1460, 420, "#2b3449", "#171d2a", 900)
           + ob.girlyanda(-60, 130, 1980, 170, t, 16, 110))
    s += SL(Z_DAL, ob.elka(1680, 1020, 560, t, seed=15)
            + okno_izby(120, 210, 310, 280, t, vid=_za_oknom(120, 210, 310, 280, t), moroz=.45))
    s += SL(Z_SRED, _skatert(120, 720, 1680, t, 170))
    cx, cy = 880, 690
    # коробка
    kor = f'<g opacity="{1 - mor:.2f}">'
    kor += ten(cx, cy + 86, 300, 30, .55)
    kor += f'<rect x="{cx-290:.0f}" y="{cy-40:.0f}" width="580" height="130" rx="16" fill="{ob.ALYJ}" {o(7)}/>'
    kor += f'<rect x="{cx-290:.0f}" y="{cy-40:.0f}" width="580" height="20" rx="10" fill="#ffffff" opacity=".25"/>'
    kor += (f'<path d="M{cx-290:.0f},{cy-40:.0f} q290,-54 580,0 q-290,56 -580,0 z"'
            f' fill="{ob.ALYJ2}" {o(5)}/>')
    # конфеты в золотых бумажках
    for i in range(12):
        bx = cx - 232 + (i % 6) * 93
        by = cy - 48 + (i // 6) * 42
        gor = .45 + .55 * abs(A.w(t, 1.8 + (i % 4) * .4, i * .19))
        kor += (f'<g transform="translate({bx:.0f},{by:.0f}) rotate({-14 + (i*23) % 28})">'
                f'<ellipse rx="38" ry="23" fill="url(#zol)" {o(4)}/>'
                f'<path d="M-38,0 l-24,-16 l0,32 z" fill="{ob.ZOLOTO2}" {o(3)}/>'
                f'<path d="M38,0 l24,-16 l0,32 z" fill="{ob.ZOLOTO2}" {o(3)}/>'
                f'<ellipse cx="-10" cy="-8" rx="13" ry="7" fill="#fff8dc" opacity="{gor:.2f}"/></g>')
    kor += '</g>'
    # хрустальная салатница — на миг вместо коробки
    hru = f'<g opacity="{mor:.2f}">'
    hru += ten(cx, cy + 90, 250, 28, .5)
    hru += (f'<path d="M{cx-250:.0f},{cy-60:.0f} q40,164 250,176 q210,-12 250,-176 z"'
            f' fill="#cfe7f5" opacity=".92" stroke="#ffffff" stroke-width="8"/>')
    for i in range(9):
        hx = cx - 210 + i * 52
        hru += (f'<path d="M{hx:.0f},{cy-56:.0f} l{(i-4)*7:.0f},150" fill="none"'
                f' stroke="#ffffff" stroke-width="7" opacity=".4"/>')
    hru += (f'<ellipse cx="{cx:.0f}" cy="{cy-60:.0f}" rx="250" ry="34" fill="#dff0fa"'
            f' opacity=".6" {o(5)}/>')
    hru += f'<rect x="{cx-70:.0f}" y="{cy+110:.0f}" width="140" height="22" rx="10" fill="#cfe3ef" {o(4)}/>'
    hru += '</g>'
    s += SL(Z_PERED, kor + hru + baza.svecha(1500, 700, t, .3, 1.1, 110))
    # КРЫШКА снимается и уходит вверх
    ly = cy - 40 - 300 * kr
    s += SL(Z_LETIT, f'<g transform="translate({cx + 36*kr:.0f},{ly:.0f}) rotate({-7*kr:.1f})"'
            f' opacity="{1 - .25*kr:.2f}">'
            f'<rect x="-300" y="-46" width="600" height="92" rx="16" fill="{ob.ALYJ2}" {o(7)}/>'
            f'<rect x="-300" y="-46" width="600" height="18" rx="9" fill="#ffffff" opacity=".22"/>'
            f'<rect x="-120" y="-30" width="240" height="60" rx="12" fill="none"'
            f' stroke="{ob.ZOLOTO}" stroke-width="7" opacity=".9"/></g>')
    s += vinetka(.42)
    return s


def dlinnyy_chek_uletaet(t):
    """Над столом вьётся длинная лента чека; она сминается в комок, и под ней
    открывается простой красивый стол. Живое: лента вьётся, комок летит прочь,
    свечи горят."""
    sm = A.ease(A.seg(t, 2.2, 1.2))
    let = A.ease(A.seg(t, 3.2, 1.6))
    s = SL(Z_NEBO, _stena(t, 860, 560, "#2a3348", "#161c29", 880))
    s += SL(Z_DAL, okno_izby(1420, 200, 360, 320, t,
                             vid=_za_oknom(1420, 200, 360, 320, t), moroz=.5)
            + ob.girlyanda(-40, 130, 1980, 170, t, 16, 110))
    # ПРОСТОЙ КРАСИВЫЙ СТОЛ — открывается по мере ухода чека
    otk = min(1.0, sm * 1.1)
    sred = _skatert(300, 740, 1320, t, 170)
    sred += (f'<g opacity="{.25 + .75*otk:.2f}">'
             + _blyudo(960, 726, 190, t, "url(#krem)")
             + _zelen(960, 700, t, .7, 9, .2)
             + _ogurcy(680, 726, .78, 1.0)
             + _syr(1250, 726, .8, 1.0)
             + ob.mandarin(560, 700, 1.3, 0.0, t)
             + ob.mandarin(1420, 702, 1.25, 0.0, t) + '</g>')
    sred += baza.svecha(430, 660, t, .0, 1.25, 120)
    sred += baza.svecha(1510, 664, t, .45, 1.2, 116)
    sred += ob.bokal(820, 726, t, .72, .1, .6, True)
    sred += ob.bokal(1110, 726, t, .72, .5, .55, True)
    s += SL(Z_SRED, sred)
    # ЛЕНТА ЧЕКА — вьётся над столом, без цифр и названий
    per = ""
    if sm < .98:
        pts = []
        for i in range(26):
            u = i / 25.0
            x = 120 + u * 1700
            y = 300 + 130 * math.sin(2 * math.pi * (u * 1.7 + t * .22)) \
                + 60 * math.sin(2 * math.pi * (u * 3.4 - t * .15))
            pts.append((x, y))
        d = _gladko(pts)
        per += (f'<g opacity="{1 - sm:.2f}">'
                f'<path d="{d}" fill="none" stroke="#f4f1e6" stroke-width="{86*(1-sm*.5):.0f}"'
                f' stroke-linecap="round" {""}/>'
                f'<path d="{d}" fill="none" stroke="#d6cfbd" stroke-width="{86*(1-sm*.5):.0f}"'
                f' stroke-linecap="round" opacity=".25"/>')
        for i in range(1, 25):
            px, py = pts[i]
            per += (f'<path d="M{px-26:.0f},{py-8:.0f} h52" stroke="#b7b0a0"'
                    f' stroke-width="5" opacity=".65"/>')
            per += (f'<path d="M{px-20:.0f},{py+10:.0f} h34" stroke="#c6bfae"'
                    f' stroke-width="5" opacity=".5"/>')
        per += '</g>'
    # КОМОК летит прочь
    if sm > .05:
        kx = 980 + 900 * let
        ky = 360 - 300 * let - 160 * math.sin(math.pi * let)
        rr = 90 * sm * (1 - .3 * let)
        per += (f'<g transform="translate({kx:.0f},{ky:.0f}) rotate({let*520:.0f})"'
                f' opacity="{1 - let*.6:.2f}">'
                f'<circle r="{rr:.0f}" fill="#f4f1e6" {o(6)}/>')
        rnd = random.Random(19)
        for i in range(9):
            a1 = rnd.uniform(0, 6.28)
            per += (f'<path d="M{math.cos(a1)*rr*.2:.0f},{math.sin(a1)*rr*.2:.0f}'
                    f' L{math.cos(a1)*rr*.9:.0f},{math.sin(a1)*rr*.9:.0f}" stroke="#c0b9a7"'
                    f' stroke-width="6" opacity=".7"/>')
        per += '</g>'
    s += SL(Z_LETIT, per)
    s += vinetka(.44)
    return s


def novogodniy_stol_sverhu(t):
    """Круглый стол строго сверху: блюда встают по одному, в середине блюдо под
    вышитым полотенцем. Живое: блюда встают, полотенце приподнимается, свечи горят."""
    vr = t * 2.1
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1b2231"/>'
           + polovicy(0, "url(#pol)")
           + f'<rect width="{W}" height="{H}" fill="#121a28" opacity=".55"/>'
           + teplo(960, 540, 1000, 820, .5))
    # четыре стула вокруг — видны спинками сверху
    dal = ""
    for i in range(6):
        a = vr + i * 60
        ar = math.radians(a)
        sx, sy = 960 + math.cos(ar) * 560, 540 + math.sin(ar) * 470
        dal += (f'<g transform="translate({sx:.0f},{sy:.0f}) rotate({a + 90:.0f})">'
                f'{ten(0, 22, 86, 30, .5)}'
                f'<rect x="-84" y="-56" width="168" height="112" rx="16" fill="url(#derev)" {o(6)}/>'
                f'<rect x="-76" y="-50" width="152" height="24" rx="10" fill="#ffffff" opacity=".2"/></g>')
    s += SL(Z_DAL, dal)
    # КРУГЛЫЙ СТОЛ
    sred = ten(960, 600, 440, 420, .6)
    sred += f'<ellipse cx="960" cy="540" rx="432" ry="420" fill="url(#derev)" {o(8)}/>'
    sred += f'<ellipse cx="960" cy="540" rx="404" ry="392" fill="url(#rush)" {o(6)}/>'
    sred += (f'<ellipse cx="960" cy="540" rx="364" ry="352" fill="none"'
             f' stroke="{ob.ALYJ}" stroke-width="10" opacity=".65"/>')
    sred += f'<ellipse cx="820" cy="400" rx="150" ry="110" fill="#ffffff" opacity=".2"/>'
    s += SL(Z_SRED, sred)
    # ВРАЩЕНИЕ + блюда по одному
    per = f'<g transform="rotate({vr:.2f} 960 540)">'
    bl = ((0, 286, .5, "zelen"), (120, 286, 1.6, "syr"), (240, 286, 2.7, "manda"))
    for a0, rr, t0, kind in bl:
        k = A.over(A.seg(t, t0, .95))
        if k <= .02:
            continue
        ar = math.radians(a0 - 90)
        px, py = 960 + math.cos(ar) * rr, 540 + math.sin(ar) * rr * .95
        per += (f'<g transform="translate({px:.0f},{py:.0f})'
                f' scale({k*1.45:.3f}) rotate({-vr:.2f})">'
        if kind == "zelen":
            per += (f'<ellipse rx="112" ry="108" fill="url(#krem)" {o(6)}/>'
                    f'<ellipse rx="86" ry="82" fill="none" stroke="{ob.ZOLOTO}" stroke-width="5" opacity=".8"/>')
            rr2 = random.Random(5)
            for i in range(12):
                aa = rr2.uniform(0, 6.28)
                dd = rr2.uniform(0, 70)
                per += (f'<ellipse cx="{math.cos(aa)*dd:.0f}" cy="{math.sin(aa)*dd:.0f}"'
                        f' rx="34" ry="13" fill="{("#5f8a3e","#79a44f","#486f31")[i%3]}"'
                        f' transform="rotate({aa*57:.0f},{math.cos(aa)*dd:.0f},{math.sin(aa)*dd:.0f})"/>')
        elif kind == "syr":
            per += (f'<ellipse rx="112" ry="108" fill="url(#krem)" {o(6)}/>')
            for i in range(5):
                aa = i * 1.256
                per += (f'<path d="M0,0 l{math.cos(aa)*86:.0f},{math.sin(aa)*86:.0f}'
                        f' A86,86 0 0 1 {math.cos(aa+1.1)*86:.0f},{math.sin(aa+1.1)*86:.0f} z"'
                        f' fill="url(#zol)" {o(4)}/>')
        else:
            per += (f'<ellipse rx="120" ry="116" fill="url(#stekl)" opacity=".6" {o(6)}/>')
            for i in range(7):
                aa = i * .9
                dd = 0 if i == 0 else 56
                per += (f'<circle cx="{math.cos(aa)*dd:.0f}" cy="{math.sin(aa)*dd:.0f}" r="38"'
                        f' fill="{ob.MANDA}" {o(5)}/>'
                        f'<circle cx="{math.cos(aa)*dd-12:.0f}" cy="{math.sin(aa)*dd-12:.0f}"'
                        f' r="12" fill="#ffc98a" opacity=".6"/>')
        per += '</g>'
    # СВЕЧИ сверху: пламя как горящая точка с ореолом
    for i in range(3):
        ar = math.radians(60 + i * 120)
        px, py = 960 + math.cos(ar) * 340, 540 + math.sin(ar) * 330
        gor = .72 + .28 * abs(A.w(t, .9, i * .3))
        per += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="26" fill="url(#vosk)" {o(5)}/>'
                f'{teplo(px, py, 120*gor, 120*gor, .75)}'
                f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{13*gor:.0f}" fill="{SVET}"/>')
    # БЛЮДО ПОД ВЫШИТЫМ ПОЛОТЕНЦЕМ в середине
    pr = A.over(A.seg(t, 3.8, 1.0))
    lift = 26 * max(0.0, math.sin(math.pi * ((t / 2.8) % 1.0)))
    if pr > .02:
        per += f'<g transform="translate(960,540) scale({pr:.3f})">'
        per += ten(0, 40, 200, 180, .5)
        per += f'<ellipse rx="196" ry="188" fill="url(#krem)" {o(7)}/>'
        per += (f'<path d="M-196,{-10 - lift:.0f} q196,{-150 - lift:.0f} 392,0'
                f' q-30,196 -196,206 q-166,-10 -196,-206 z" fill="url(#rush)" {o(6)}/>')
        for i in range(3):
            per += (f'<path d="M-168,{34 + i*58 - lift*.4:.0f} q168,46 336,0" fill="none"'
                    f' stroke="{ob.ALYJ}" stroke-width="9" opacity=".75"/>')
        for i in range(7):
            px = -150 + i * 50
            per += (f'<path d="M{px:.0f},{-26-lift:.0f} l18,26 l-18,26 l-18,-26 z"'
                    f' fill="{ob.ALYJ2}" opacity=".8"/>')
        per += baza.par(0, -40 - lift, t, 4, .45, 150, .3, 1.0)
        per += '</g>'
    per += '</g>'
    s += SL(Z_PERED, per)
    s += vinetka(.46)
    return s


def tri_okna_tri_blyuda(t):
    """Три светящихся окна в зимней стене: холодец, слоёный салат в хрустале,
    пирог и раскрытая тетрадка. Живое: окна загораются по одному, холодец
    дрожит, страница тетрадки переворачивается."""
    s = SL(Z_NEBO, nebo("noch", t) + sneg_letit(t, 46))
    s += SL(Z_DAL, brevna(-20, 120, BAND + 40, 960, 104)
            + f'<rect x="-20" y="120" width="{BAND+40}" height="30" rx="10" fill="url(#sneg)" {o(5)}/>')
    sred = ""
    for i, ox in enumerate((40, 300, 560)):
        gor = A.ease(A.seg(t, .35 + i * .75, .7))
        oy, ow, oh = 380, 230, 300
        vid = (f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
               f' fill="{"#3a2a16" if gor > .05 else "#1a1e2c"}"/>')
        vid += (f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
                f' fill="{SVET}" opacity="{.42*gor:.2f}"/>')
        # стол внутри окна и блюдо силуэтом
        ty = oy + oh - 76
        vid += (f'<rect x="{ox+16:.0f}" y="{ty:.0f}" width="{ow-32:.0f}" height="16"'
                f' rx="7" fill="url(#rush)" opacity="{.3 + .7*gor:.2f}"/>')
        cx = ox + ow / 2
        if i == 0:
            # ХОЛОДЕЦ дрожит
            dr = 7 * A.w(t, .55) * gor
            vid += (f'<g transform="translate({cx:.0f},{ty:.0f}) scale({1 + dr*.012:.3f},'
                    f'{1 - dr*.012:.3f})" opacity="{gor:.2f}">'
                    f'<rect x="-82" y="-62" width="164" height="62" rx="14" fill="#cfd8c0" {o(5)}/>'
                    f'<rect x="-82" y="-62" width="164" height="16" rx="8" fill="#e6ecd8" opacity=".8"/>'
                    f'<ellipse cx="-26" cy="-28" rx="20" ry="11" fill="#9a6b4a" opacity=".8"/>'
                    f'<ellipse cx="28" cy="-34" rx="18" ry="10" fill="#9a6b4a" opacity=".8"/>'
                    f'<ellipse cx="2" cy="-16" rx="16" ry="8" fill="#6f8c4a" opacity=".8"/></g>')
        elif i == 1:
            # СЛОЁНЫЙ САЛАТ в хрустале
            vid += (f'<g transform="translate({cx:.0f},{ty:.0f})" opacity="{gor:.2f}">'
                    f'<path d="M-84,-8 q14,-104 84,-110 q70,6 84,110 z" fill="url(#stekl)"'
                    f' opacity=".55" {o(5)}/>')
            for k, c in enumerate(("#b63b27", "#f0d79a", "#6f8c4a", "#e8c15a")):
                vid += (f'<path d="M{-78 + k*7:.0f},{-20 - k*22:.0f} q{78 - k*7:.0f},-22'
                        f' {156 - k*14:.0f},0 l0,22 q{-78 + k*7:.0f},20 {-156 + k*14:.0f},0 z"'
                        f' fill="{c}" opacity=".95"/>')
            vid += '</g>'
        else:
            # ПИРОГ
            vid += (f'<g transform="translate({cx:.0f},{ty:.0f})" opacity="{gor:.2f}">'
                    f'<ellipse cx="0" cy="-12" rx="86" ry="34" fill="url(#med)" {o(5)}/>'
                    f'<ellipse cx="0" cy="-26" rx="86" ry="34" fill="url(#med)" {o(5)}/>'
                    f'<path d="M-62,-36 q62,-22 124,0" fill="none" stroke="#f2cf8c" stroke-width="8" opacity=".8"/>'
                    f'<path d="M-40,-50 l80,24 M40,-50 l-80,24" stroke="#c48f3c" stroke-width="7"/></g>')
            vid += baza.par(cx, ty - 70, t, 4, .35 * gor, 140, .4, 1.0)
        vid += teplo(cx, oy + oh * .5, 180 * gor, 170 * gor, .55)
        sred += okno_izby(ox, oy, ow, oh, t, vid=vid, moroz=.3, krest=True)
        sred += teplo(cx, oy + oh * .5, 260 * gor, 240 * gor, .4)
    s += SL(Z_SRED, sred)
    # ТЕТРАДКА В КЛЕТКУ на снежном приступке
    per = sneg_lezhit(934, 20).replace('<g data-z="520">', '').replace('</g><!--/z-->', '')
    per += _tetrad(250, 786, 430, 270, t, .1)
    per += (f'<g transform="translate(738,866) rotate(-18)">'
            f'{ten(0, 16, 20, 8, .4)}'
            f'<rect x="-9" y="-130" width="18" height="150" rx="8" fill="#2f5a78" {o(4)}/>'
            f'<path d="M-9,20 l9,22 l9,-22 z" fill="#1d1a16"/></g>')
    s += SL(Z_PERED, per)
    s += vinetka(.44)
    return s


def tri_kartochki_drugih_video(t):
    """Тёмно-красный фон, слева встаёт первая карточка-обложка, хозяйка года
    показывает на неё копытцем. Живое: карточка встаёт с отскоком, копытце
    показывает, фон мерцает."""
    mer = .82 + .18 * abs(A.w(t, 3.4))
    vst = A.over(A.seg(t, .25, 1.0))
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#3a0f14"/>'
           + f'<rect width="{W}" height="{H}" fill="{ob.ALYJ2}" opacity="{.5*mer:.2f}"/>'
           + teplo(620, 560, 980, 820, .5 * mer))
    # круги-ореолы вокруг места карточки
    dal = ""
    for i in range(4):
        u = ((t * .3 + i * .25) % 1.0)
        dal += (f'<circle cx="620" cy="560" r="{180 + u*520:.0f}" fill="none"'
                f' stroke="{ob.ZOLOTO}" stroke-width="5" opacity="{(1-u)*.2:.2f}"/>')
    dal += ob.konfetti(t, 18, 9, .35, .6)
    s += SL(Z_DAL, dal)
    s += SL(Z_SRED, _kartochka_video(350, 300, 540, 700, t, vst, .0, 0))
    # ХОЗЯЙКА ГОДА справа, развёрнута к карточке
    XC = 1420
    per = (f'<g transform="matrix(-1,0,0,1,{2*XC:.0f},0)">'
           + ob.koza(XC, 1010, t, .92, 0.0, True, .1) + '</g>')
    # копытце показывает на карточку
    uk = 14 * A.w(t, 1.5)
    per += (f'<g transform="translate({1330 + uk*.5:.0f},{842 + uk:.0f})">'
            f'<path d="M0,0 q-70,-44 -150,-52" fill="none" stroke="{ob.ALYJ}"'
            f' stroke-width="36" stroke-linecap="round"/>'
            f'<path d="M0,0 q-70,-44 -150,-52" fill="none" stroke="{ob.ALYJ2}"'
            f' stroke-width="13" stroke-linecap="round" opacity=".5"/>'
            f'<rect x="-186" y="-72" width="44" height="34" rx="10" fill="{CHUGUN}" {o(5)}/></g>')
    s += SL(Z_PERED, per)
    s += vinetka(.5)
    return s


def elochnaya_vetka_s_krasnym_sharom(t):
    """Крупно еловая ветка с красным шаром, в шаре отражается карточка-обложка;
    на второй фразе под веткой встают все три. Живое: шар покачивается,
    отражение блестит, карточки встают в ряд."""
    kch = 4.4 * A.w(t, 2.6)
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#121b26"/>'
           + f'<rect width="{W}" height="{H}" fill="{ob.HVOYA2}" opacity=".5"/>'
           + teplo(640, 420, 820, 700, .45))
    # боке огней
    bok = ""
    r = random.Random(27)
    for i in range(18):
        bx, by = r.uniform(40, W - 40), r.uniform(60, H - 60)
        gor = .25 + .55 * abs(A.w(t, 2.4 + r.uniform(0, 2.4), i * .13))
        col = (SVET, ob.ALYJ, ob.ZOLOTO, "#8fd6ff")[i % 4]
        bok += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r.uniform(20,60):.0f}"'
                f' fill="{col}" opacity="{gor*.26:.2f}"/>')
    s += SL(Z_NEBO, bok)
    # ТРИ КАРТОЧКИ встают в ряд под веткой
    dal = ""
    for i, cx in enumerate((190, 790, 1390)):
        k = A.over(A.seg(t, 2.6 + i * .32, .95))
        dal += _kartochka_video(cx, 700, 340, 330, t, k, i * .3, i)
    s += SL(Z_DAL, dal)
    # ШАР с отражением карточки
    bx, by, R = 640, 470, 168
    sred = f'<g transform="rotate({kch:.2f} {bx:.0f} {by-250:.0f})">'
    sred += f'<path d="M{bx:.0f},{by-250:.0f} v{250-R:.0f}" stroke="{ob.ZOLOTO2}" stroke-width="7"/>'
    sred += f'<rect x="{bx-26:.0f}" y="{by-R-42:.0f}" width="52" height="46" rx="10" fill="url(#zol)" {o(5)}/>'
    sred += ten(bx + 16, by + R + 34, R * .8, 26, .5)
    sred += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{R:.0f}" fill="{ob.ALYJ}" {o(9)}/>'
    sred += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{R:.0f}" fill="{ob.ALYJ2}" opacity=".35"/>'
    # отражение третьей обложки внутри шара
    sred += (f'<clipPath id="shar5"><circle cx="{bx:.0f}" cy="{by:.0f}" r="{R-10:.0f}"/></clipPath>'
             f'<g clip-path="url(#shar5)" opacity=".8">'
             f'<g transform="translate({bx-92:.0f},{by-96:.0f}) scale(.52)">'
             + _kartochka_video(0, 0, 340, 330, t, 1.0, .5, 2) + '</g></g>')
    # блик по отражению бежит
    bl = ((t * .4) % 1.0)
    sred += (f'<g clip-path="url(#shar5)"><path d="M{bx - R + bl*2*R:.0f},{by-R:.0f}'
             f' l60,0 l-96,{2*R:.0f} l-60,0 z" fill="#ffffff" opacity=".28"/></g>')
    sred += (f'<ellipse cx="{bx-R*.4:.0f}" cy="{by-R*.42:.0f}" rx="{R*.26:.0f}"'
             f' ry="{R*.18:.0f}" fill="#ffffff" opacity="{.4 + .3*abs(A.w(t,2.0)):.2f}"/>')
    sred += teplo(bx, by, 330, 330, .4)
    sred += '</g>'
    s += SL(Z_SRED, sred)
    # ВЕТКА поверх, с краю кадра
    per = _vetka_eli(-60, 150, 1180, t, 1.0, .0, 1.0)
    per += _vetka_eli(1980, 120, 900, t, 1.0, .4, 1.0).replace(
        'translate(1980.0,120.0)', 'translate(1980.0,120.0) scale(-1,1)')
    per += _vetka_eli(240, 90, 640, t, .74, .7, 1.0)
    s += SL(Z_PERED, per)
    s += vinetka(.48)
    return s
