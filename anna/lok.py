# -*- coding: utf-8 -*-
"""104 декорации ролика «16 ноября — Анна Холодная».

Каждая — функция времени f(t) -> svg. Все нарисованы ЗАНОВО под этот текст
(R-0019): ни один кадр не взят у «13 ноября», «14 ноября» и «15 ноября».
Где в плане стоит окно вставки, главное живёт в ЛЕВОЙ полосе 0-830 (R-0007).
В каждой декорации минимум три живых элемента (R-0006).

Общий холод дня: первый настоящий мороз, иней, пар изо рта, белое на синем.
Тёплое пятно в кадре всегда одно — окно, лампа, печка, кружка.
"""
import math, random
from baza import *
from baza import (_nebo, _oblaka, _tuman, _ulica_dal, _panelka, _sneg_lezhit,
                  _sneg_letit, _utvar_izby, _utvar_pekarni, _kvartira_veschi,
                  _mebel_hlam, _ramka_pp, _vinetka)
import anim as A

OKNO = (860, 300, 980, 551)          # неподвижный контейнер вставки
DEN, MESYAC = "16", "НОЯБРЯ"


# ═══════════════ СКВОЗНЫЕ ОБРАЗЫ ЭТОГО РОЛИКА ═══════════════

def figura(x, y, h_, t, col="#1b1822", kant="#cfe4f5", platok=False, ph=.0,
           profil=False, op=1.0, telogreyka=False):
    """Человек со спины или в профиль. Всегда с КАНТОМ — тёмная фигура без
    канта сливается с тёмным фоном. Кант этого ролика ХОЛОДНЫЙ (морозный
    день), тёплый ставится вручную там, где человек стоит у огня."""
    dy = 3.0 * A.w(t, .55, ph)
    s = f'<g transform="translate(0,{dy:.1f})" opacity="{op:.2f}">'
    s += siluet(x, y, h_, col, 1.0, platok, kant)
    if telogreyka:                     # простёганная зимняя спина
        for i in range(4):
            yy = y - h_ * (.62 - i * .11)
            s += (f'<path d="M{x-h_*.17:.0f},{yy:.0f} q{h_*.17:.0f},{8} {h_*.34:.0f},0"'
                  f' stroke="{kant}" stroke-width="3" fill="none" opacity=".30"/>')
    if profil:                         # светлая скула со стороны света
        s += (f'<circle cx="{x+h_*.07:.0f}" cy="{y-h_*.86:.0f}" r="{h_*.035:.0f}"'
              f' fill="{kant}" opacity=".40"/>')
    s += '</g>'
    return s


def par_izo_rta(x, y, t, ph=0.0, s_=1.0, op=.55):
    """Пар изо рта на морозе: три облачка, рождаются и тают. Живой элемент
    дня — без него мороз в кадре не читается."""
    s = ""
    for i in range(3):
        k = ((t * .55 + ph + i * .33) % 1.0)
        r = (16 + 46 * k) * s_
        s += (f'<ellipse cx="{x + 52*k*s_:.0f}" cy="{y - 30*k*s_:.0f}"'
              f' rx="{r:.0f}" ry="{r*.66:.0f}" fill="#eaf4ff"'
              f' opacity="{op*(1-k)*(1-k):.2f}"/>')
    return s


def inej(x, y, w_, t, n=14, seed=3, col="#eaf6ff", R=0):
    """Иней искрит: мелкие звёздочки, зажигаются вразнобой."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        px = x + rnd.random() * w_
        py = y + rnd.random() * (R or 40)
        bl = .25 + .75 * (0.5 + 0.5 * A.w(t, 1.1 + rnd.random(), rnd.random()))
        r = 3 + rnd.random() * 4
        s += (f'<path d="M{px:.0f},{py-r:.0f} v{2*r:.0f} M{px-r:.0f},{py:.0f} h{2*r:.0f}"'
              f' stroke="{col}" stroke-width="2" opacity="{bl*.8:.2f}"/>')
    return s


def morozny_uzor(x, y, w_, h_, t, op=.5, col="#dcefff"):
    """Морозный узор по стеклу: папоротниковые ветки из углов, дышат."""
    s = ""
    for i, (ax, ay, sx, sy) in enumerate(((x, y, 1, 1), (x + w_, y, -1, 1),
                                          (x, y + h_, 1, -1), (x + w_, y + h_, -1, -1))):
        gr = .8 + .2 * A.w(t, 3.4, i * .3)
        d = f'M{ax},{ay} '
        for j in range(5):
            dx = sx * (26 + j * 22) * gr
            dy = sy * (20 + j * 26) * gr
            d += f'q{sx*18:.0f},{dy*.5:.0f} {dx:.0f},{dy:.0f} '
        s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5" opacity="{op:.2f}"/>'
        for j in range(4):
            bx = ax + sx * (30 + j * 30) * gr
            by = ay + sy * (26 + j * 34) * gr
            s += (f'<path d="M{bx:.0f},{by:.0f} l{sx*22:.0f},{-sy*14:.0f}'
                  f' M{bx:.0f},{by:.0f} l{sx*14:.0f},{sy*22:.0f}"'
                  f' stroke="{col}" stroke-width="3" opacity="{op*.8:.2f}"/>')
    return s


def sosulka(x, y, dl, t, ph=0.0, kap=True, svet=False):
    """Сосулька под крышей: прозрачная, с бликом, иногда срывается капля.
    Сквозной образ дня и основа памятки в финале."""
    w_ = max(10, dl * .13)
    s = (f'<path d="M{x-w_:.0f},{y:.0f} h{2*w_:.0f} l{-w_:.0f},{dl:.0f} Z"'
         f' fill="url(#led)" opacity=".92" {o(3, "#bcdcef")}/>'
         f'<path d="M{x-w_*.35:.0f},{y+6:.0f} l{w_*.2:.0f},{dl*.72:.0f}"'
         f' stroke="#ffffff" stroke-width="{w_*.28:.1f}" opacity=".55"/>')
    if svet:
        s += f'<ellipse cx="{x:.0f}" cy="{y+dl*.6:.0f}" rx="{w_*3.4:.0f}" ry="{dl*.5:.0f}" fill="url(#teplo)" opacity=".5"/>'
    if kap:
        k = ((t * .42 + ph) % 1.0)
        if k > .55:
            kk = (k - .55) / .45
            s += (f'<ellipse cx="{x:.0f}" cy="{y+dl+kk*kk*180:.0f}" rx="{w_*.42:.0f}"'
                  f' ry="{w_*.6:.0f}" fill="#dff0fa" opacity="{1-kk*.6:.2f}"/>')
        else:
            s += (f'<circle cx="{x:.0f}" cy="{y+dl+6:.0f}" r="{w_*.42*(0.6+0.4*k/.55):.1f}"'
                  f' fill="#dff0fa" opacity=".9"/>')
    return s


def strekha(x, y, w_, t, n=5, dl=None, seed=5, svet=False):
    """Край крыши со снежной шапкой и рядом сосулек."""
    rnd = random.Random(seed)
    dl = dl or [120 + rnd.random() * 120 for _ in range(n)]
    s = (f'<path d="M{x:.0f},{y:.0f} h{w_:.0f} v26 h{-w_:.0f} Z" fill="url(#dosk)" {o(5)}/>'
         + _sneg_lezhit_polosa(x, y - 46, w_, 46))
    for i in range(n):
        s += sosulka(x + w_ * (i + .5) / n, y + 26, dl[i], t, i * .27, True, svet)
    return s


def _sneg_lezhit_polosa(x, y, w_, h_, col="url(#sneg)"):
    """Снежная шапка ПОЛОСОЙ, а не заливкой вниз: заливка от y вниз закрасила
    бы весь кадр (мина 12.11)."""
    d = f'M{x:.0f},{y+h_:.0f} '
    n = max(3, int(w_ / 120))
    for i in range(n + 1):
        px = x + w_ * i / n
        py = y + 10 * math.sin(i * 1.7)
        d += f'L{px:.0f},{py:.0f} '
    d += f'L{x+w_:.0f},{y+h_:.0f} Z'
    return f'<path d="{d}" fill="{col}" {o(4, "#cfe0f0")}/>'


def holodny_svet(cx, cy, rx, ry=None, op=.45):
    """Холодное голубое пятно — зимний контражур, противовес teplo()."""
    ry = ry or rx * .72
    return (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}"'
            f' fill="url(#holod)" opacity="{op:.2f}"/>')
def bele_kolom_na_verevke(t):
    """Двор в морозных сумерках: бельё стоит колом, вдали дом с тёплым окном."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 9))
    s += SL(Z_NEBO, oblaka(t, 150, 3, 4, .3))
    s += SL(Z_DAL, izba_snaruzhi(1430, 760, 360, t, svet=True, truba=True, seed=6))
    s += SL(Z_DAL, ulica_dal(40, 820, 480, t, zima=True, seed=3))
    s += SL(Z_DAL, sneg_lezhit(900, 22))
    postx, posty, w_ = 160, 430, 980
    s += SL(Z_SRED, f'<line x1="{postx}" y1="248" x2="{postx}" y2="{posty}" stroke="url(#derev)" stroke-width="16"/>')
    s += SL(Z_SRED, f'<line x1="{postx+w_}" y1="248" x2="{postx+w_}" y2="{posty-20}" stroke="url(#derev)" stroke-width="16"/>')
    s += SL(Z_SRED, f'<line x1="{postx}" y1="260" x2="{postx+w_}" y2="258" stroke="#3a3a3a" stroke-width="5"/>')
    rnd = random.Random(4)
    sway = 2.0 * A.w(t, 2.7)        # стоят колом — качается ЦЕЛЫМ листом, не трепещет
    lst = ""
    for i in range(3):
        cx = postx + 140 + i * 350
        ph = rnd.uniform(0, 1)
        dx = sway + 1.3 * A.w(t, 3.1, ph)
        h_ = 206 + i * 22
        lst += (f'<g transform="translate({dx:.1f},0)">'
                f'<path d="M{cx-118},259 L{cx+118},259 L{cx+94},{259+h_} Q{cx},{259+h_+16} {cx-94},{259+h_} Z"'
                f' fill="url(#sneg)" {o(5,"#9fc4d8")}/></g>')
        lst += inej(cx - 108, 259, 216, t, 9, i + 2, "#eaf6ff", h_ * .55)
    s += SL(Z_SRED, lst)
    pin_k = abs(A.w(t, 2.4, .1))
    s += SL(Z_SRED, f'<g transform="translate({postx+80+pin_k*4:.1f},257)">'
                     f'<rect x="-7" y="-20" width="14" height="30" rx="4" fill="{MED}" {o(3)}/></g>')
    s += SL(Z_LETIT, sneg_letit(t, 40, 8, .82, 1.6))
    s += vinetka(.46)
    return s


def stol_s_nesdelannym_nachalom(t):
    """Стол у окна: ножницы закрываются, мел осыпается, лист сворачивается в трубку."""
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="520" fill="{SUMER}" opacity=".55"/>')
    s += SL(Z_DAL, okno_izby(520, 80, 420, 360, t, svet=True, moroz=.35))
    s += SL(Z_DAL, luch(540, 440, 320, 420, t, .16))
    s += SL(Z_SRED, polovicy(760))
    tx, ty, tw = 660, 700, 560
    s += SL(Z_SRED, stol(tx, ty, tw, 36))
    s += SL(Z_SRED, f'<rect x="{tx+30}" y="{ty-78}" width="{tw-220}" height="150" rx="10" fill="url(#tkan)" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{tx+66},{ty-46} l150,0 l-28,66 l-94,0 Z" fill="none" stroke="#f3e9cf"'
                     f' stroke-width="4" stroke-dasharray="6 7" opacity=".82"/>')
    melk = ""
    for i in range(6):
        p = ((t * .46) + i / 6) % 1.0
        melk += (f'<circle cx="{tx+90+i*16}" cy="{ty-18+p*58:.0f}" r="{2.8*(1-p):.1f}"'
                 f' fill="#f3e9cf" opacity="{(1-p)*.8:.2f}"/>')
    s += SL(Z_SRED, melk)
    close = A.ease(A.seg(t, 1.6, 1.0))
    ang = 24 * (1 - close)
    scx, scy = tx + tw - 160, ty - 24
    nozh = f'<circle cx="{scx}" cy="{scy}" r="8" fill="{K}"/>'
    for sgn in (-1, 1):
        nozh += (f'<g transform="rotate({sgn*ang:.1f} {scx} {scy})">'
                 f'<path d="M{scx},{scy} l{sgn*66},-13 l{sgn*9},10 l{-sgn*57},17 Z" fill="{ZHELEZ}" {o(3)}/></g>')
    s += SL(Z_SRED, nozh)
    roll = A.ease(A.seg(t, 2.8, 0.8))
    lx, ly = tx + tw - 280, ty - 24
    if roll < .04:
        s += SL(Z_SRED, f'<rect x="{lx-66}" y="{ly-46}" width="140" height="86" rx="4" fill="url(#list)" {o(4)}/>')
    else:
        rr = 10 + 28 * roll
        s += SL(Z_SRED, f'<rect x="{lx-66+120*roll*.5:.0f}" y="{ly-46}" width="{140*(1-roll*.55):.0f}"'
                         f' height="86" rx="4" fill="url(#list)" {o(4)}/>'
                         f'<ellipse cx="{lx-56:.0f}" cy="{ly-3}" rx="{rr:.0f}" ry="43" fill="#cfc29a" {o(3)}/>')
    s += vinetka(.4)
    return s


def zima_s_kistyu_nad_derevney(t):
    """Над деревней Зима широкой кистью белит крыши, снег сыплется из рукава."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += SL(Z_NEBO, nebo("rassv", t, True, 5))
    s += SL(Z_NEBO, oblaka(t, 180, 4, 7, .4))
    rnd = random.Random(2)
    bx = 90 + A.ease(A.seg(t, .6, 6.2)) * (W - 320)
    dal = ""
    for i in range(5):
        rx = 110 + i * 350
        rw = 300
        dh = rnd.uniform(70, 130)
        dal += (f'<rect x="{rx}" y="690" width="{rw*.7:.0f}" height="{dh+70:.0f}" fill="#2f3646" opacity=".92"/>'
                f'<path d="M{rx-14},690 L{rx+rw*.35:.0f},{690-dh:.0f} L{rx+rw*.84:.0f},690 Z"'
                f' fill="#23283a" {o(5)}/>')
        vis = max(0.0, min(1.0, (bx - rx) / rw))
        if vis > .03:
            dal += (f'<path d="M{rx-14},690 L{rx+rw*.35:.0f},{690-dh:.0f} L{rx+rw*.84:.0f},690 Z"'
                    f' fill="url(#sneg)" opacity="{vis:.2f}"/>')
        dal += dym(rx + rw * .55, 686 - dh, t, 4, .22 + i * .02, 260 + i * 20, .32 + .22 * vis, "#cfd6de", .8)
    s += SL(Z_DAL, dal)
    zy = 440
    s += SL(Z_SRED, figura(bx, zy, 430, t, col=POBEL, kant="#5f6f7c", platok=True, ph=.3,
                           profil=True, telogreyka=True))
    brx, bry = bx + 150, zy - 300
    tilt = 10 * A.w(t, .9, .2)
    s += SL(Z_SRED, f'<g transform="rotate({tilt:.1f} {brx:.0f} {bry:.0f})">'
                     f'<rect x="{brx-10:.0f}" y="{bry-60:.0f}" width="20" height="60" fill="{MED}" {o(3)}/>'
                     f'<path d="M{brx-26:.0f},{bry:.0f} h52 l-8,26 h-36 Z" fill="#efe3c8" {o(3)}/></g>')
    letit = ""
    for i in range(14):
        p = ((t * .5) + i / 14) % 1.0
        letit += (f'<circle cx="{bx-210+rnd.uniform(-30,30)+40*A.w(t,2.0,i*.2):.0f}"'
                  f' cy="{zy-520+p*420:.0f}" r="{(2+2*(1-p)):.1f}" fill="#ffffff" opacity="{(1-p)*.85:.2f}"/>')
    s += SL(Z_LETIT, letit)
    s += vinetka(.4)
    return s


def nachatyy_srub_vo_ldu(t):
    """Начатый сруб: ледяная корка ползёт по брёвнам, растут сосульки."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, False))
    s += SL(Z_DAL, ulica_dal(1200, 760, 560, t, zima=True, seed=9))
    x, y, w_, hh = 420, 760, 980, 92
    s += SL(Z_SRED, brevna(x, y - 3 * hh, w_, 3 * hh, hh))
    kro = A.ease(A.seg(t, 1.0, 4.4))
    s += SL(Z_SRED, f'<rect x="{x}" y="{y-3*hh:.0f}" width="{w_}" height="{3*hh*kro:.0f}"'
                     f' fill="url(#led)" opacity="{.5*kro:.2f}"/>')
    dl = 30 + 70 * A.ease(A.seg(t, 1.4, 4.0))
    ic = ""
    for i in range(6):
        ic += sosulka(x + 60 + i * (w_ - 120) / 5, y - 3 * hh, dl * (.7 + .3 * ((i % 3) / 2)), t, i * .2, True)
    s += SL(Z_SRED, ic)
    dx0, dy0 = x + 260, y - 60
    vib = 2 * A.w(t, 7.0)
    s += SL(Z_PERED, f'<g transform="translate({vib:.1f},0)">'
                      f'<path d="M{dx0-16},{dy0} l32,-10 l10,26 l-32,10 Z" fill="{ZHELEZ}" {o(3)}/></g>')
    rnd = random.Random(8)
    strug = ""
    for i in range(9):
        p = ((t * .3) + i / 9) % 1.0
        ex, ey = dx0 + rnd.uniform(-40, 120), dy0 + 40 + p * 30
        strug += f'<path d="M{ex:.0f},{ey:.0f} q18,-8 30,4" fill="none" stroke="{DOSKA}" stroke-width="4" opacity="{(1-p*.6):.2f}"/>'
    s += SL(Z_PERED, strug)
    s += SL(Z_DAL, f'<ellipse cx="1760" cy="940" rx="70" ry="26" fill="{TRAVA}" opacity=".55"/>')
    s += SL(Z_LETIT, sneg_letit(t, 30, 6, .7, 1.0))
    s += vinetka(.42)
    return s


def teplyy_dom_na_ledyanom_pole(t):
    """Тёплый круг среди ледяного поля: лёд подступает и стоит, дверь выпускает девочек."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, False))
    s += SL(Z_DAL, f'<ellipse cx="{W/2}" cy="1040" rx="1400" ry="340" fill="url(#led)" opacity=".85" {o(4,"#8fb8ce")}/>')
    pulse = 18 * A.w(t, 3.6)
    s += SL(Z_DAL, f'<ellipse cx="{W/2}" cy="980" rx="{560+pulse:.0f}" ry="{220+pulse*.4:.0f}"'
                    f' fill="#eaf6ff" opacity=".35"/>')
    s += SL(Z_SRED, f'<ellipse cx="{W/2}" cy="980" rx="430" ry="170" fill="url(#glina)" opacity=".4" {o(3)}/>')
    s += SL(Z_SRED, izba_snaruzhi(W/2 - 180, 900, 360, t, svet=True, truba=True, seed=4))
    dvx, dvy = W/2 - 46, 790
    op_d = A.ease(A.seg(t, .4, .6))
    s += SL(Z_SRED, dver(dvx, dvy, 92, 150, op_d))
    dev = ""
    rnd = random.Random(1)
    for i in range(2):
        t0 = .7 + i * .5
        p = A.out(A.seg(t, t0, 1.6))
        gx = dvx + 46 + p * (260 + i * 120)
        gy = dvy + 150 - p * 10
        dev += figura(gx, gy, 170, t, platok=True, ph=i * .4)
        dev += f'<rect x="{gx-6:.0f}" y="{gy-120:.0f}" width="40" height="12" rx="4" fill="{DOSKA}" opacity="{min(1,p*2):.2f}"/>'
    s += SL(Z_SRED, dev)
    s += SL(Z_LETIT, sneg_letit(t, 26, 3, .6, .8))
    s += vinetka(.38)
    return s


def devochki_s_berestoy_i_pyalcami(t):
    """Девочки на лавке: писала скребут по бересте, иглы ходят в пяльцах."""
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="560" fill="{SUMER}" opacity=".5"/>')
    s += SL(Z_DAL, okno_izby(1500, 120, 300, 300, t, svet=True, moroz=.3))
    s += SL(Z_SRED, polovicy(780))
    lx, ly, lw = 220, 760, 1300
    s += SL(Z_SRED, lavka(lx, ly, lw))
    s += SL(Z_DAL, figura(lx + lw * .5, ly - 40, 460, t, platok=True, ph=.5))
    rnd = random.Random(6)
    girls = ""
    for i in range(5):
        gx = lx + 120 + i * (lw - 240) / 4
        girls += figura(gx, ly, 240, t, platok=True, ph=i * .22)
        if i % 2 == 0:
            wig = 5 * A.w(t, 1.4, i * .3)
            girls += (f'<g transform="rotate({wig:.1f} {gx-30:.0f} {ly-170:.0f})">'
                      f'<rect x="{gx-70:.0f}" y="{ly-180:.0f}" width="80" height="26" rx="4" fill="{KREM}" {o(3)}/>'
                      f'<line x1="{gx-30:.0f}" y1="{ly-190:.0f}" x2="{gx-30:.0f}" y2="{ly-150:.0f}" stroke="{K}" stroke-width="3"/></g>')
        else:
            needle = 10 * abs(A.w(t, 1.1, i * .25))
            girls += (f'<ellipse cx="{gx+20:.0f}" cy="{ly-170:.0f}" rx="40" ry="34" fill="none"'
                      f' stroke="{DOSKA}" stroke-width="6"/>'
                      f'<line x1="{gx+20:.0f}" y1="{ly-200+needle:.0f}" x2="{gx+20:.0f}" y2="{ly-150-needle:.0f}"'
                      f' stroke="#dcdcdc" stroke-width="2"/>')
        if i == 1:
            braid = 6 * A.w(t, 2.0, .1)
            girls += (f'<g transform="rotate({braid:.1f} {gx+6:.0f} {ly-300:.0f})">'
                      f'<path d="M{gx+6:.0f},{ly-300:.0f} q10,30 0,70" fill="none" stroke="#3b2a1c" stroke-width="10"/></g>')
    s += SL(Z_SRED, girls)
    s += vinetka(.4)
    return s


def rostok_pod_ledyanym_kolpakom(t):
    """Росток тянется из горшка и на слове «не будет» застывает под ледяным колпаком."""
    s = f'<rect width="{W}" height="{H}" fill="{SUMER}"/>'
    s += SL(Z_DAL, okno_izby(560, 120, 820, 560, t, svet=False, moroz=.2))
    fog = .3 + .2 * abs(A.w(t, 3.0))
    s += SL(Z_DAL, f'<ellipse cx="960" cy="420" rx="260" ry="200" fill="#ffffff" opacity="{fog:.2f}"/>')
    px, py = 960, 760
    s += SL(Z_SRED, f'<path d="M{px-70},{py} l16,-110 q54,-18 108,0 l16,110 Z" fill="url(#glina)" {o(5)}/>')
    grow = A.ease(A.seg(t, .3, 2.0))
    stem_h = 18 + 150 * grow
    s += SL(Z_SRED, f'<path d="M{px},{py-100} q{10*A.w(t,2.2):.0f},{-stem_h*.5:.0f} 0,{-stem_h:.0f}"'
                     f' fill="none" stroke="{TRAVA}" stroke-width="10"/>')
    leaf_op = min(1.0, grow * 1.4)
    s += SL(Z_SRED, f'<path d="M{px},{py-100-stem_h*.7:.0f} q40,-10 56,18 q-34,20 -56,-6 Z"'
                     f' fill="{ZEL2}" opacity="{leaf_op:.2f}" {o(3)}/>')
    kolp = A.over(A.seg(t, 3.0, 1.2))
    kolp = max(0.0, min(1.15, kolp))
    if kolp > .03:
        s += SL(Z_SRED, f'<ellipse cx="{px}" cy="{py-100-stem_h*.4:.0f}" rx="{80*kolp:.0f}" ry="{150*kolp:.0f}"'
                         f' fill="url(#stekl)" opacity="{.55*min(1,kolp):.2f}" {o(3,"#bcdcef")}/>')
    s += vinetka(.4)
    return s


def bumazhnyy_korablik_na_podokonnike(t):
    """Листок складывается в кораблик на подоконнике, за окном ночь светлеет."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    night = 1.0 - A.ease(A.seg(t, .2, 2.6))
    s += SL(Z_DAL, okno_izby(520, 80, 600, 460, t, svet=False, moroz=0))
    s += SL(Z_DAL, f'<rect x="520" y="80" width="600" height="460" fill="url(#nnoch)" opacity="{night:.2f}"/>')
    s += SL(Z_DAL, f'<rect x="520" y="80" width="600" height="460" fill="url(#nrassv)" opacity="{1-night:.2f}"/>')
    s += SL(Z_SRED, polovicy(760))
    hx, hy = 1360, 760
    s += SL(Z_SRED, hodiki(hx, hy - 170, t, 1.1))
    fold = A.ease(A.seg(t, 1.0, 1.0))
    px, py = 760, 700
    rock = 4 * A.w(t, 1.6)
    if fold < .5:
        s += SL(Z_SRED, f'<rect x="{px-70}" y="{py-10}" width="140" height="90" rx="4" fill="url(#list)"'
                         f' opacity="{1-fold*1.6:.2f}" {o(3)}/>')
    if fold > .15:
        op = min(1.0, (fold - .15) * 1.4)
        s += SL(Z_SRED, f'<g transform="rotate({rock:.1f} {px:.0f} {py+40:.0f})" opacity="{op:.2f}">'
                         f'<path d="M{px-60:.0f},{py+30:.0f} l120,0 l-20,40 l-80,0 Z" fill="url(#list)" {o(4)}/>'
                         f'<path d="M{px:.0f},{py+30:.0f} l0,-70 l50,70 Z" fill="#dff0fa" opacity=".8" {o(3)}/></g>')
    s += vinetka(.42)
    return s


def sani_u_vorot(t):
    """Сани запряжены у открытых ворот: хозяин смотрит на небо и распрягает лошадь."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, False))
    gswing = 3 * A.w(t, 4.0)
    s += SL(Z_DAL, f'<g transform="rotate({gswing:.1f} 260 880)">{pleten(60, 880, 420)}</g>')
    s += SL(Z_DAL, f'<g transform="rotate({-gswing:.1f} 1100 880)">{pleten(680, 880, 420)}</g>')
    hx, hy = 980, 900
    legshift = 6 * A.w(t, 1.3)
    s += SL(Z_SRED, f'<ellipse cx="{hx}" cy="{hy}" rx="150" ry="80" fill="#4a3324" {o(5)}/>'
                     f'<ellipse cx="{hx+170}" cy="{hy-70}" rx="60" ry="46" fill="#4a3324" {o(4)}/>'
                     f'<path d="M{hx+200},{hy-110} l20,-26 l6,24 Z" fill="#4a3324" {o(3)}/>'
                     f'<line x1="{hx-80}" y1="{hy+70}" x2="{hx-80+legshift:.0f}" y2="{hy+150}" stroke="#2e2018" stroke-width="12"/>'
                     f'<line x1="{hx+60}" y1="{hy+70}" x2="{hx+60-legshift:.0f}" y2="{hy+150}" stroke="#2e2018" stroke-width="12"/>')
    s += SL(Z_SRED, par(hx + 220, hy - 120, t, 3, .45, 120, .6))
    sx, sy = 1300, 940
    s += SL(Z_SRED, f'<path d="M{sx-160},{sy} q-30,0 -30,-30 l0,-70 l220,0 l0,70 q0,30 -30,30 Z"'
                     f' fill="url(#derev)" {o(5)}/>'
                     f'<path d="M{sx-190},{sy} q-40,10 -40,40" fill="none" stroke="url(#zhel)" stroke-width="10"/>')
    hom = A.ease(A.seg(t, 1.6, 1.6))
    s += SL(Z_SRED, f'<path d="M{hx+150},{hy-130-hom*90:.0f} q20,-10 40,0" fill="none"'
                     f' stroke="{DOSKA2}" stroke-width="14" opacity="{1-hom*.9:.2f}"/>')
    s += SL(Z_SRED, figura(hx + 320, hy + 40, 380, t, kant="#cfe4f5"))
    s += vinetka(.4)
    return s


def pozemka_pakostnica_na_doroge(t):
    """Путник идёт дорогой, у ног вьётся позёмка-пакостница и сбивает шапку."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 4))
    scroll = (t * 60) % 120
    road = ""
    for i in range(18):
        rx = -120 + i * 120 - scroll
        road += f'<ellipse cx="{rx:.0f}" cy="980" rx="40" ry="8" fill="#cfe0f0" opacity=".3"/>'
    s += SL(Z_DAL, road)
    px, py = 900, 920
    look = 8 * A.ease(A.seg(t, 3.2, 1.0)) * A.w(t, .5)
    s += SL(Z_SRED, f'<g transform="rotate({look:.1f} {px} {py-150})">{figura(px, py, 420, t, kant="#cfe4f5")}</g>')
    hat0 = (px, py - 406)
    fly = A.ease(A.seg(t, 2.0, 1.0))
    hx = hat0[0] + fly * 160
    hy = hat0[1] - fly * fly * 260
    s += SL(Z_SRED, f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="42" ry="22" fill="{K}" opacity="{1-fly*.1:.2f}"/>')
    rnd = random.Random(3)
    sx, sy = px - 80, py + 60
    swirl_a = (t * 220) % 360
    sw = f'<g transform="translate({sx+30*A.w(t,1.0):.0f},{sy}) rotate({swirl_a:.0f})">'
    for i in range(5):
        a = i / 5 * 300
        rr = 14 + i * 7
        ex = rr * math.cos(math.radians(a))
        ey = rr * math.sin(math.radians(a)) * .5
        sw += f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{16-i:.0f}" ry="7" fill="#dfeefb" opacity="{.7-i*.1:.2f}"/>'
    sw += ('<circle cx="18" cy="-4" r="3" fill="#1c2733"/><circle cx="26" cy="-2" r="3" fill="#1c2733"/>'
           '<path d="M16,4 q8,6 14,0" fill="none" stroke="#1c2733" stroke-width="2"/></g>')
    s += SL(Z_PERED, sw)
    s += SL(Z_LETIT, sneg_letit(t, 24, 2, .6, 1.2))
    s += vinetka(.42)
    return s


def bilet_na_komode(t):
    """Комод: билет вертится в воздухе, перчатка и ваза прячут его по очереди."""
    s = f'<rect width="{W}" height="{H}" fill="{SUMER}"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="620" fill="{NOCH}" opacity=".4"/>')
    cx, cy, cw = 760, 760, 480
    s += SL(Z_SRED, f'<rect x="{cx}" y="{cy}" width="{cw}" height="220" rx="12" fill="url(#derev)" {o(6)}/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="{cx+30}" y="{cy+30+i*90}" width="{cw-60}" height="70" rx="8"'
                         f' fill="{DOSKA2}" {o(4)}/><circle cx="{cx+cw/2:.0f}" cy="{cy+65+i*90}" r="8" fill="url(#zhel)"/>')
    s += SL(Z_SRED, hodiki(cx + cw - 70, cy - 90, t, .7))
    turn = 16 * A.w(t, 1.6)
    bx, by = cx + 150, cy - 30
    s += SL(Z_SRED, f'<g transform="rotate({turn:.1f} {bx} {by})">'
                     f'<rect x="{bx-50:.0f}" y="{by-34:.0f}" width="100" height="68" rx="6" fill="{KREM}" {o(4)}/></g>')
    glove_ph = A.ease(A.seg(t, 1.0, 1.0)) - A.ease(A.seg(t, 2.6, 1.0))
    glove_ph = max(0.0, min(1.0, glove_ph))
    gx = bx - 70 + 140 * (1 - glove_ph)
    s += SL(Z_SRED, f'<path d="M{gx-40:.0f},{by-20:.0f} h80 v50 q-40,14 -80,0 Z" fill="{TKAN2}" opacity=".9" {o(4)}/>')
    vase = A.ease(A.seg(t, 3.0, 1.2))
    if vase > .02:
        vy = by - 220 + vase * 190
        s += SL(Z_SRED, f'<path d="M{bx-36:.0f},{vy:.0f} q-10,70 10,96 h52 q20,-26 10,-96 Z" fill="url(#glina)" {o(4)}/>')
    s += vinetka(.4)
    return s


def korka_nad_vedrom(t):
    """Чёрствая корка зависает над ведром, летит в миску с тёркой, Зима заглядывает в окно."""
    s = f'<rect width="{W}" height="{H}" fill="{POL2}"/>'
    s += SL(Z_DAL, f'<rect width="{W}" height="560" fill="{SUMER}" opacity=".5"/>')
    winx, winy = 1480, 140
    zima_p = A.seg(t, 4.5, 2.5)
    sil = ""
    if .02 < zima_p < .98:
        wx_ = -40 + zima_p * 360
        sil = (f'<ellipse cx="{wx_:.0f}" cy="150" rx="22" ry="70" fill="#141d26" opacity=".85"/>'
               f'<circle cx="{wx_:.0f}" cy="68" r="20" fill="#141d26" opacity=".85"/>')
    s += SL(Z_DAL, okno_izby(winx, winy, 320, 300, t, svet=False, moroz=.3, vid=sil))
    s += SL(Z_SRED, polovicy(760))
    vx, vy = 1160, 900
    s += SL(Z_SRED, f'<path d="M{vx-80},{vy} q-6,-170 80,-170 q86,0 80,170 Z" fill="{ZHELEZ}" opacity=".9" {o(4)}/>')
    nx, ny = 430, 450
    s += SL(Z_SRED, f'<circle cx="{nx}" cy="{ny}" r="7" fill="url(#zhel)"/>'
                     f'<path d="M{nx},{ny} q20,70 10,160" fill="none" stroke="#5a4028" stroke-width="3"/>'
                     f'<path d="M{nx-36},{ny+160} q6,70 46,78 q40,-8 46,-78 Z" fill="{RUSH}" opacity=".9" {o(4)}/>')
    bwlx, bwly = 650, 920
    s += SL(Z_SRED, f'<ellipse cx="{bwlx}" cy="{bwly}" rx="90" ry="34" fill="{KREM}" {o(4)}/>'
                     f'<rect x="{bwlx-60}" y="{bwly-60}" width="120" height="36" rx="6" fill="{ZHELEZ}" opacity=".85" {o(3)}/>')
    hover = A.seg(t, .3, 1.0)
    recoil = A.ease(A.seg(t, 1.3, .9))
    land = A.ease(A.seg(t, 1.3, .9))
    cxp = vx - 10 + (bwlx - vx) * land
    cyp = (vy - 210 + 14 * A.w(t, 1.8) * (1 - recoil)) * (1 - land) + (bwly - 50) * land
    s += SL(Z_SRED, f'<ellipse cx="{cxp:.0f}" cy="{cyp:.0f}" rx="30" ry="18" fill="{DOSKA2}" {o(3)}/>')
    put_away = A.ease(A.seg(t, 3.5, 1.4))
    if put_away > .02:
        bagx = nx - 36 + 36 * put_away
        bagy = ny + 190 - 20 * put_away
        s += SL(Z_SRED, f'<ellipse cx="{bagx:.0f}" cy="{bagy:.0f}" rx="24" ry="16" fill="{DOSKA2}"'
                         f' opacity="{put_away:.2f}"/>')
    s += vinetka(.42)
    return s


def derevyannyy_gorod_v_snegu(t):
    """СМЕНА ГЛАВЫ. Деревянный город на холмах: дымы, сани на улице, галки над теремами."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, False))
    s += SL(Z_NEBO, oblaka(t, 150, 5, 2, .35))
    rnd = random.Random(12)
    terem = ""
    heights = [260, 340, 300, 420, 320, 260, 360]
    for i, hh in enumerate(heights):
        tx = 60 + i * 270
        tw = 220
        terem += (f'<rect x="{tx}" y="{760-hh}" width="{tw}" height="{hh}" fill="#55606e" opacity=".92" {o(4)}/>'
                  f'<path d="M{tx-16},{760-hh} L{tx+tw/2:.0f},{760-hh-tw*.42:.0f} L{tx+tw+16},{760-hh} Z"'
                  f' fill="#3c4a58" {o(5)}/>'
                  f'<path d="M{tx-16},{766-hh} L{tx+tw/2:.0f},{766-hh-tw*.4:.0f} L{tx+tw+16},{766-hh} Z"'
                  f' fill="url(#sneg)" {o(4)}/>')
        terem += dym(tx + tw * .3, 758 - hh - tw * .4, t, 4, .18 + i * .015, 260 + i * 14, .4, "#d7dde4", .9)
    s += SL(Z_DAL, terem)
    s += SL(Z_DAL, pleten(0, 900, W, 150, 15))
    scroll = (t * 90) % (W + 300)
    sx = -200 + scroll
    s += SL(Z_SRED, f'<g transform="translate({sx:.0f},0)">'
                     f'<path d="M0,880 q-20,0 -20,-22 l0,-40 l150,0 l0,40 q0,22 -20,22 Z" fill="url(#derev)" {o(4)}/></g>')
    galki = ""
    for i in range(6):
        a = t * 40 + i * 60
        gx = 960 + 420 * math.cos(math.radians(a))
        gy = 420 + 70 * math.sin(math.radians(a * 1.3)) - 60
        galki += f'<path d="M{gx-16:.0f},{gy:.0f} q16,-14 32,0 q-16,10 -32,0" fill="#20242c" opacity=".85"/>'
    s += SL(Z_DAL, galki)
    s += vinetka(.4)
    return s
def troe_v_tereme(t):
    """Горница терема: три силуэта у цветного окна, затем венец и уход в дверь."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 118))
    s += polovicy(840)
    f1 = 1.0 - A.seg(t, 4.2, .7)
    f2 = A.seg(t, 4.3, .7)
    g = f'<g opacity="{f1:.2f}">'
    for i, (cx0, cc) in enumerate(((120, TKAN), (330, ZEL2), (560, ZOL))):
        dx = 70 * A.w(t, 7 + i * 2, i * .3)
        g += f'<path d="M{cx0-60+dx:.0f},0 l150,0 l60,840 l-270,0 Z" fill="{cc}" opacity=".22"/>'
    g += teplo(420, 640, 420, 360, .5)
    g += figura(230, 760, 360, t, col="#1d1926", kant=INEY, profil=True)
    g += (f'<path d="M190,420 q40,-34 80,0 q-10,30 -40,34 q-30,-4 -40,-34 Z" fill="{SNEG}" opacity=".85"/>')
    g += figura(420, 790, 380, t, col="#211a1e", kant=INEY, telogreyka=True)
    g += f'<rect x="470" y="560" width="54" height="150" rx="10" fill="url(#zhel)" {o(6)}/>'
    g += figura(610, 740, 340, t, col="#241f2a", kant=INEY)
    kos = 10 * A.w(t, 2.3, .4)
    g += (f'<g transform="rotate({kos:.1f} 620 560)">'
          f'<path d="M620,560 q18,70 4,170" fill="none" stroke="#3b2a22" stroke-width="16" stroke-linecap="round"/></g>')
    g += svecha(760, 700, t, .2, 1.1)
    s += SL(Z_SRED, g + '</g>')
    g2 = f'<g opacity="{f2:.2f}">'
    pil_x, pil_y = 420, 760
    g2 += f'<ellipse cx="{pil_x}" cy="{pil_y}" rx="230" ry="70" fill="url(#rush)" {o(6)}/>'
    vshift = 160 * A.seg(t, 5.0, 1.0)
    g2 += (f'<g transform="translate({vshift:.0f},{-vshift*.3:.0f})">'
           f'<ellipse cx="{pil_x-40}" cy="{pil_y-40}" rx="90" ry="34" fill="none" stroke="url(#zol)" stroke-width="10" opacity=".9"/>'
           f'<ellipse cx="{pil_x-40}" cy="{pil_y-40}" rx="58" ry="20" fill="none" stroke="{SVET}" stroke-width="4"'
           f' opacity="{.5+.4*abs(A.w(t,2.2)):.2f}"/></g>')
    g2 += figura(560, 820, 360, t, col="#231d28", kant=SVET)
    plat_op = A.seg(t, 5.6, .8)
    g2 += (f'<path d="M520,560 q40,-26 80,0 q10,90 -40,110 q-50,-20 -40,-110 Z"'
           f' fill="{TKAN}" opacity="{plat_op*.92:.2f}"/>')
    op_ = A.seg(t, 6.6, 1.0)
    g2 += dver(920, 420, 260, 560, open_=op_)
    g2 += teplo(920 + 260 * .3, 420 + 560 * .5, 300, 260, .4 + .3 * op_)
    s += SL(Z_SRED, g2 + '</g>')
    s += ramka_pp("levo", "#120e0b", .5)
    s += vinetka(.42)
    return s


def stroyka_na_holme(t):
    """Вершина холма: плотники ставят венец стены, бревно идёт на верёвках."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += oblaka(t, 150, 5, 31, .55)
    s += ulica_dal(40, 720, 760, t, True, 9)
    s += f'<path d="M-20,900 q400,-90 820,-20 q400,70 820,-10 L1940,1080 L-20,1080 Z" fill="#cfd8e0" {o(5)}/>'
    wallh = 60 + 220 * A.seg(t, 1.0, 3.2)
    g = ''
    for i in range(6):
        g += f'<rect x="{80+i*110}" y="{880-wallh:.0f}" width="96" height="{wallh:.0f}" rx="8" fill="url(#brev)" {o(5)}/>'
    g += f'<path d="M80,{880-wallh:.0f} L740,{880-wallh:.0f} L800,{820-wallh:.0f} L20,{820-wallh:.0f} Z" fill="url(#dosk)" {o(6)}/>'
    g += f'<rect x="280" y="760" width="26" height="160" fill="url(#brev)" {o(5)}/><rect x="470" y="760" width="26" height="160" fill="url(#brev)" {o(5)}/>'
    liftk = A.seg(t, .8, 2.6)
    ly = 980 - 300 * liftk
    g += (f'<line x1="200" y1="700" x2="200" y2="{ly:.0f}" stroke="#caa06a" stroke-width="5" stroke-dasharray="3 7"/>'
          f'<line x1="400" y1="700" x2="400" y2="{ly:.0f}" stroke="#caa06a" stroke-width="5" stroke-dasharray="3 7"/>'
          f'<rect x="150" y="{ly:.0f}" width="300" height="46" rx="20" fill="url(#brev)" {o(6)}/>')
    for i in range(9):
        p = ((t * .8) + i * .11) % 1.0
        g += (f'<rect x="{620+40*math.sin(i)+110*p:.0f}" y="{700-60*p:.0f}" width="12" height="20"'
              f' transform="rotate({360*p:.0f} {620+40*math.sin(i)+110*p:.0f} {700-60*p:.0f})" fill="{DOSKA}" opacity="{(1-p)*.8:.2f}"/>')
    for i, px in enumerate((660, 760)):
        ang = 30 * abs(A.w(t, .9, i * .5)) - 15
        g += f'<g transform="rotate({ang:.0f} {px} 640)"><path d="M{px},640 l-14,-70 l40,16 Z" fill="{ZHELEZ}" {o(4)}/></g>'
    g += figura(190, 860, 280, t, col="#241f24", kant=SNEG, profil=True)
    g += figura(680, 700, 300, t, col="#211c1f", kant=SNEG)
    s += SL(Z_SRED, g)
    s += holodny_svet(400, 260, 460)
    s += ramka_pp("levo", "#141210", .5)
    s += vinetka(.4)
    return s


def klyuchi_u_novyh_vorot(t):
    """Готовые ворота: связка ключей отпирает створку, снег сыплется с них."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += ulica_dal(0, 640, W, t, True, 21)
    s += f'<path d="M-20,760 q480,-60 960,0 q480,60 980,-10 L1940,1080 L-20,1080 Z" fill="{SNEG}" {o(5)}/>'
    op_ = A.seg(t, 2.2, 2.0)
    s += SL(Z_SRED, dver(700, 280, 520, 660, open_=op_, kruchok=True, cepochka=True))
    s += teplo(700 + 520 * (.4 + .5 * op_), 280 + 660 * .5, 280, 260, .3 + .4 * op_)
    sw = 9 * A.w(t, 1.6)
    g = f'<g transform="rotate({sw:.1f} 1300 540)">'
    g += '<line x1="1300" y1="540" x2="1300" y2="600" stroke="url(#zhel)" stroke-width="8"/>'
    for i in range(3):
        ry = 600 + i * 42
        g += f'<ellipse cx="1300" cy="{ry}" rx="28" ry="22" fill="none" stroke="url(#zhel)" stroke-width="10"/>'
    g += '</g>'
    s += SL(Z_PERED, g)
    for i in range(14):
        p = ((t * .5) + i * .09) % 1.0
        s += f'<circle cx="{660+i*12+10*A.w(t,2.0,i*.2):.0f}" cy="{260+p*620:.0f}" r="{2.6+2.4*(1-p):.1f}" fill="#ffffff" opacity="{.8*(1-p):.2f}"/>'
    s += vinetka(.4)
    return s


def shkolnaya_gornica(t):
    """Горница школы: девочки входят вереницей, затем четыре стола оживают."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 108))
    s += polovicy(820)
    s += SL(Z_SRED, pech(1500, 480, 320, 460, t))
    f1 = 1.0 - A.seg(t, 4.2, .7)
    f2 = A.seg(t, 4.3, .8) * (1 - A.seg(t, 8.4, .8))
    f3 = A.seg(t, 8.6, 1.0)
    g1 = f'<g opacity="{f1:.2f}">'
    op_ = A.seg(t, .6, 1.6)
    g1 += dver(60, 360, 220, 460, open_=op_)
    for i in range(3):
        step = A.seg(t, 1.2 + i * .9, 1.4)
        x0 = 60 + step * (260 + i * 150)
        snow = A.seg(t, 2.0 + i * .9, .6)
        g1 += figura(x0, 760, 230, t, col="#201c23", kant=INEY, platok=True, ph=i * .3)
        g1 += f'<ellipse cx="{x0+10:.0f}" cy="750" rx="22" ry="10" fill="{SNEG}" opacity="{.8*(1-snow):.2f}"/>'
    g1 += '</g>'
    s += SL(Z_SRED, g1)
    g2 = f'<g opacity="{f2:.2f}">'
    for i in range(4):
        x0 = 120 + i * 420
        g2 += stol(x0, 700, 300)
        if i == 0:
            d = A.seg(t, 4.8, 3.0)
            g2 += f'<path d="M{x0+40},740 l{d*220:.0f},0" stroke="#3b2a22" stroke-width="4" opacity=".8"/>'
            g2 += f'<rect x="{x0+40+d*220:.0f}" y="730" width="10" height="26" fill="{ZHELEZ}" {o(2)}/>'
        elif i == 1:
            yop = abs(A.w(t, .7, .1))
            g2 += f'<ellipse cx="{x0+150}" cy="{720-30*yop:.0f}" rx="40" ry="{14+10*yop:.0f}" fill="{K}" opacity=".7"/>'
        elif i == 2:
            sw = 6 * A.w(t, 1.3)
            g2 += f'<g transform="rotate({sw:.1f} {x0+150} 700)"><rect x="{x0+90}" y="690" width="120" height="70" rx="30" fill="none" stroke="{TKAN2}" stroke-width="8"/></g>'
        else:
            braid = A.seg(t, 5.4, 3.0)
            g2 += f'<path d="M{x0+40},740 q{60*braid:.0f},-20 {120*braid:.0f},0 q{60*braid:.0f},20 {160*braid:.0f},0" fill="none" stroke="{TKAN}" stroke-width="6" opacity=".85"/>'
        g2 += figura(x0 + 150, 940, 200, t, col="#201c23", kant=INEY, ph=i * .2)
    g2 += '</g>'
    s += SL(Z_SRED, g2)
    g3 = f'<g opacity="{f3:.2f}">'
    for i in range(4):
        x0 = 120 + i * 420
        g3 += stol(x0, 700, 300)
        g3 += figura(x0 + 150, 940, 200, t, col="#201c23", kant=INEY, ph=i * .2)
        sway = 6 * A.w(t, 2.4, i * .3)
        g3 += f'<rect x="{x0+40+sway:.0f}" y="330" width="220" height="80" rx="6" fill="url(#rush)" {o(5)}/>'
    g3 += figura(960, 900, 340, t, col="#1d1926", kant=SVET)
    g3 += '</g>'
    s += SL(Z_SRED, g3)
    s += ramka_pp("oba", "#120e0b", .45)
    s += vinetka(.4)
    return s


def knyazhna_nad_berestoy_uchenicy(t):
    """Крупно стол: женщина со спины наклоняется, береста учится писать."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, brevna(-20, -20, 860, H + 40, 100))
    s += teplo(420, 560, 500, 420, .55)
    s += SL(Z_SRED, stol(140, 660, 680))
    lean = A.seg(t, .6, 1.4)
    s += figura(700, 1000 - 60 * lean, 380, t, col="#211c21", kant=INEY, profil=True)
    s += figura(330, 980, 190, t, col="#231d28", kant=INEY, ph=.4)
    nod = 5 * A.w(t, 1.4, .1) * A.seg(t, .8, .6)
    s += f'<g transform="rotate({nod:.1f} 330 870)"></g>'
    write = A.seg(t, 1.6, 2.6)
    curl = .06 * abs(A.w(t, 3.0, .2))
    s += (f'<path d="M260,700 q{30-curl*300:.0f},-10 {220-curl*260:.0f},6 l{10+curl*120:.0f},80'
          f' q{-110+curl*260:.0f},16 {-220+curl*240:.0f},-6 Z" fill="url(#krem)" {o(5)}/>')
    s += f'<path d="M280,730 l{write*180:.0f},10" stroke="#3b2a22" stroke-width="4" opacity=".85"/>'
    s += f'<rect x="{280+write*180:.0f}" y="724" width="8" height="22" fill="{ZHELEZ}" {o(2)}/>'
    s += ramka_pp("levo", "#120e0b", .5)
    s += vinetka(.42)
    return s


def bukva_vyshitaya_nityu(t):
    """Очень крупно пяльцы: игла красной нитью стежками вышивает букву «А»."""
    s = f'<rect width="{W}" height="{H}" fill="#241b1e"/>'
    s += f'<circle cx="960" cy="540" r="440" fill="url(#krem)" {o(10)}/>'
    s += f'<circle cx="960" cy="540" r="440" fill="none" stroke="url(#derev)" stroke-width="30"/>'
    s += f'<circle cx="960" cy="540" r="410" fill="none" stroke="url(#derev)" stroke-width="14" opacity=".7"/>'
    pts = ((760, 760), (960, 320), (1160, 760), (840, 600), (1080, 600))
    n_on = A.seg(t, .8, 4.2) * 5
    g = ''
    for i in range(5):
        a, b = (pts[i], pts[(i + 1) if i < 3 else 4])
        seg_t = max(0.0, min(1.0, n_on - i))
        if seg_t <= 0:
            continue
        ex = a[0] + (b[0] - a[0]) * seg_t
        ey = a[1] + (b[1] - a[1]) * seg_t
        g += f'<path d="M{a[0]},{a[1]} L{ex:.0f},{ey:.0f}" stroke="{KRAS}" stroke-width="14" stroke-linecap="round"/>'
    s += g
    ndl = (n_on - int(n_on)) if n_on < 5 else .5 + .5 * A.w(t, .6)
    nx = 960 + 260 * A.w(t, 1.1)
    ny = 320 + 440 * (ndl)
    dive = abs(A.w(t, 2.0))
    s += f'<line x1="{nx:.0f}" y1="{ny-70*dive:.0f}" x2="{nx:.0f}" y2="{ny+70*dive:.0f}" stroke="{ZHELEZ}" stroke-width="5"/>'
    s += f'<circle cx="{nx:.0f}" cy="{ny-70*dive:.0f}" r="5" fill="{ZHELEZ}"/>'
    thr = 40 + 30 * abs(A.w(t, .9, .2))
    s += f'<path d="M{nx:.0f},{ny+70*dive:.0f} q{thr:.0f},{thr*.6:.0f} 0,{thr*1.4:.0f}" fill="none" stroke="{KRAS}" stroke-width="4" opacity=".7"/>'
    s += vinetka(.46)
    return s


def tri_devushki_s_shitem_u_okna(t):
    """Изба в инее: три девушки на лавке шьют разом, кот под лавкой играет."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 108))
    s += polovicy(840)
    s += okno_izby(1480, 220, 340, 300, t, moroz=.8, svet=True)
    s += inej(1460, 180, 400, t, 20, 4, "#eaf6ff", 360)
    s += teplo(760, 640, 560, 420, .45)
    s += SL(Z_SRED, lavka(360, 760, 760))
    items = ((TKAN, "передник"), (RUSH, "полотенце"), ("#dfe6ee", "наволочка"))
    for i, (col, _) in enumerate(items):
        x0 = 460 + i * 260
        s += figura(x0, 1000, 260, t, col="#201c23", kant=INEY, ph=i * .25)
        needle = 18 * abs(A.w(t, .7, .05))
        s += f'<path d="M{x0-70},900 h140" stroke="{col}" stroke-width="40" opacity=".85"/>'
        s += f'<line x1="{x0}" y1="{880-needle:.0f}" x2="{x0}" y2="{900-needle:.0f}" stroke="{ZHELEZ}" stroke-width="4"/>'
    s += SL(Z_PERED, kot(600, 920, t, 1.0))
    loskut_x = 600 + 60 * A.w(t, 2.6, .3)
    s += f'<rect x="{loskut_x:.0f}" y="950" width="50" height="34" rx="6" fill="{TKAN2}" opacity=".85" {o(3)}/>'
    s += ramka_pp("oba", "#141210", .45)
    s += vinetka(.4)
    return s


def pyat_sosulek_pod_kryshey(t):
    """Карниз с пятью сосульками: номера, затем пять карточек-памяток под ними."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_DAL, ulica_dal(0, 300, W, t, True, 17))
    warm = A.seg(t, 3.2, 1.4)
    cx = (230, 580, 930, 1280, 1630)
    dl = (150, 190, 140, 210, 170)
    s += f'<rect x="-20" y="260" width="{W+40}" height="60" fill="url(#dosk)" {o(6)}/>'
    s += _sneg_lezhit_polosa(-20, 214, W + 40, 60)
    s += inej(0, 214, W, t, 30, 9, "#eaf6ff", 56)
    for i, (x0, d0) in enumerate(zip(cx, dl)):
        svet = (i == 2) and warm > .1
        s += sosulka(x0, 320, d0, t, i * .22, True, svet)
        num_on = A.seg(t, .6 + i * .45, .5) * (1 - A.seg(t, 4.0, 1.0))
        if num_on > .02:
            s += (f'<text x="{x0:.0f}" y="{320+d0*.55:.0f}" font-family="DejaVu Sans" font-size="48"'
                  f' font-weight="bold" fill="{SVET}" text-anchor="middle" opacity="{num_on:.2f}">{i+1}</text>')
    s += teplo(960, 700, 400 + 400 * warm, 420, .3 + .35 * warm)
    wallbase = 900
    s += SL(Z_SRED, f'<rect x="60" y="380" width="{W-120}" height="{wallbase-380}" fill="url(#brev)" {o(6)}/>')
    icons = (KRAS, MED, "#caa37a", TKAN2, ZOL)
    for i, x0 in enumerate(cx):
        appear = A.seg(t, 6.0 + i * 3.0, .5)
        if appear < .02:
            continue
        bounce = A.over(appear, 1.6)
        yy = (wallbase - 130) + (1 - bounce) * 160
        g = f'<g transform="translate({x0:.0f},{yy:.0f})">'
        g += f'<rect x="-90" y="-90" width="180" height="180" rx="16" fill="url(#krem)" {o(6)}/>'
        if i == 0:
            g += f'<rect x="-40" y="-40" width="80" height="60" fill="{icons[0]}" {o(4)}/><ellipse cx="0" cy="-42" rx="42" ry="10" fill="{ZHELEZ}" {o(3)}/>'
        elif i == 1:
            g += f'<rect x="-50" y="-30" width="100" height="70" rx="14" fill="{icons[1]}" {o(4)}/><path d="M-26,-30 q26,-26 52,0" fill="none" stroke="{K}" stroke-width="6"/>'
        elif i == 2:
            g += f'<path d="M-6,30 Q-40,0 -30,-50 Q-16,-70 -4,-50 Q2,-70 12,-50 Q24,-70 36,-50 Q48,-20 10,30 Z" fill="{icons[2]}" {o(4)}/>'
        elif i == 3:
            g += f'<path d="M-50,30 Q-54,-50 -10,-50 Q-4,-20 -50,30 Z" fill="{icons[3]}" {o(4)}/><path d="M6,30 Q2,-50 46,-50 Q50,-20 6,30 Z" fill="{icons[3]}" {o(4)}/>'
        else:
            g += f'<ellipse cx="0" cy="0" rx="60" ry="40" fill="{icons[4]}" {o(4)}/><path d="M-50,-6 q50,-18 100,0" fill="none" stroke="{MED}" stroke-width="5" opacity=".6"/>'
        g += f'<circle cx="60" cy="-60" r="26" fill="{KRAS}" {o(3)}/><text x="60" y="-50" font-family="DejaVu Sans" font-size="30" font-weight="bold" fill="#fff" text-anchor="middle">{i+1}</text>'
        g += '</g>'
        s += SL(Z_PERED, g)
    sweep = A.seg(t, 21.0, 1.0)
    if sweep > .02:
        s += begushchiy_blik(t, 2.2, 0, .22 * sweep, 300)
    s += vinetka(.42)
    return s


def pervyy_kolyshek_i_bechevka(t):
    """Плашка первого запрета: один колышек, бечёвка сматывается без начатого забора."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += SL(Z_DAL, ulica_dal(0, 560, W, t, True, 31))
    s += f'<path d="M-20,620 q480,-40 960,0 q480,40 980,-14 L1940,1080 L-20,1080 Z" fill="#1f2a22" opacity=".9"/>'
    s += inej(200, 660, 700, t, 18, 2, "#eaf6ff", 220)
    pullk = A.seg(t, 1.0, 3.6)
    s += (f'<path d="M420,780 q{120*(1-pullk):.0f},{-40*(1-pullk):.0f} {300*(1-pullk):.0f},{-10*(1-pullk):.0f}'
          f' q{120*(1-pullk):.0f},{30*(1-pullk):.0f} {460*(1-pullk):.0f},{-20*(1-pullk):.0f}"'
          f' fill="none" stroke="#caa06a" stroke-width="7" stroke-dasharray="4 10" opacity="{.9-.3*pullk:.2f}"/>')
    riseк = A.seg(t, 3.0, 1.6)
    ky = 820 - 140 * riseк
    s += SL(Z_SRED, f'<rect x="400" y="{ky:.0f}" width="30" height="{160-140*riseк:.0f}" rx="6" fill="url(#brev)" {o(5)}/>')
    spool = A.seg(t, 2.0, 2.4)
    s += (f'<g transform="translate({420+spool*160:.0f},780)">'
          f'<ellipse cx="0" cy="0" rx="{30+18*(1-spool):.0f}" ry="{30+18*(1-spool):.0f}" fill="none"'
          f' stroke="#caa06a" stroke-width="6"/></g>')
    s += ramka_pp("oba", "#141210", .4)
    s += vinetka(.4)
    return s


def nizkoe_solnce_za_oknom_masterskoy(t):
    """Мастерская у окна: солнце едва встаёт над забором и за три секунды скатывается обратно."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 110))
    s += SL(Z_SRED, stol(560, 760, 560))
    cyc = (t % 3.0) / 3.0
    arc = math.sin(cyc * math.pi)
    sun_x, sun_y = 1200, 760 - arc * 220
    s += SL(Z_DAL, f'<rect x="900" y="560" width="480" height="340" rx="10" fill="url(#stekl)" opacity=".9" {o(8)}/>')
    s += SL(Z_DAL, f'<rect x="880" y="820" width="520" height="40" fill="url(#dosk)" {o(6)}/>')
    s += SL(Z_DAL, f'<circle cx="{sun_x}" cy="{sun_y:.0f}" r="60" fill="url(#zol)" opacity=".92"/>')
    s += teplo(sun_x, sun_y, 180, 160, .4 * arc + .15)
    for i in range(3):
        sx = 560 + i * 170 - arc * 60
        s += f'<ellipse cx="{sx:.0f}" cy="800" rx="90" ry="18" fill="{K}" opacity="{.25+.2*arc:.2f}"/>'
    s += figura(760, 1000, 300, t, col="#211c22", kant=SNEG)
    yawn = max(0.0, math.sin(t * .6)) ** 6
    s += f'<ellipse cx="760" cy="{820-120*yawn:.0f}" rx="14" ry="{8+14*yawn:.0f}" fill="#2a1c16" opacity="{.6*yawn:.2f}"/>'
    droop = 30 * (1 - A.ease(min(1.0, t / 4.0)))
    s += f'<g transform="translate(0,{-droop:.0f})"></g>'
    s += ramka_pp("oba", "#141210", .45)
    s += vinetka(.42)
    return s


def polovina_lodki_pod_snegom(t):
    """Берег: лодка-рёбра на подпорках, снег наполняет её, сорока садится."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, ulica_dal(0, 600, W, t, True, 41))
    s += SL(Z_DAL, f'<path d="M-20,760 q960,-30 1960,0 L1940,1080 L-20,1080 Z" fill="{INEY}" opacity=".7"/>')
    bx, by, bw = 760, 820, 420
    s += SL(Z_SRED, f'<rect x="{bx-20}" y="{by}" width="40" height="160" fill="url(#brev)" {o(5)}/>'
                     f'<rect x="{bx+bw-20}" y="{by}" width="40" height="160" fill="url(#brev)" {o(5)}/>')
    g = f'<path d="M{bx},{by} q{bw/2},90 {bw},0" fill="none" stroke="{DOSKA2}" stroke-width="12"/>'
    for i in range(6):
        rx = bx + bw * i / 5
        g += f'<path d="M{rx:.0f},{by:.0f} q0,70 0,80" stroke="{DOSKA2}" stroke-width="10"/>'
    fillk = A.seg(t, .6, 5.0)
    g += f'<path d="M{bx+10},{by+16+fillk*50:.0f} q{bw/2-10},{60*fillk:.0f} {bw-20},0 l0,30 q{-(bw/2-10)},30 {-(bw-20)},0 Z" fill="url(#sneg)" {o(4)}/>'
    s += SL(Z_SRED, g)
    cap = A.seg(t, 1.5, 3.5)
    s += SL(Z_PERED, f'<rect x="{bx+bw*.55:.0f}" y="{by+40}" width="150" height="24" rx="8" fill="url(#derev)" {o(5)}/>'
                      f'<ellipse cx="{bx+bw*.55+75:.0f}" cy="{by+40}" rx="{20+70*cap:.0f}" ry="{10+22*cap:.0f}" fill="{SNEG}" {o(3)}/>')
    land = A.seg(t, 4.0, 1.0)
    bird_y = (by - 40) - (1 - land) * 160
    s += f'<g opacity="{min(1.0,land*2):.2f}">{ptica(bx+bw*.15, bird_y, t, 1.3, "#1c1c1c", .2, "#5b6a78")}</g>'
    s += vinetka(.4)
    return s


def poslednyaya_doska_na_kryshe(t):
    """Крыша сарая: молоток бьёт по последней доске, хлопья летят, телега с листьями уезжает."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += f'<path d="M-20,540 L960,180 L1940,540 L1940,660 L-20,660 Z" fill="url(#dosk)" {o(7)}/>'
    for i in range(7):
        s += f'<line x1="{140+i*250}" y1="{540-(i%2)*10}" x2="{300+i*250}" y2="{540-(i%2)*10}" stroke="{DOSKA2}" stroke-width="4" opacity=".5"/>'
    hammer = abs(A.w(t, .55))
    hx, hy = 1280, 420
    s += SL(Z_SRED, figura(hx - 60, hy + 320, 300, t, col="#211c22", kant=SNEG))
    s += f'<g transform="rotate({-30+40*hammer:.0f} {hx} {hy})"><rect x="{hx-8}" y="{hy-70}" width="16" height="90" fill="{DOSKA2}" {o(3)}/><rect x="{hx-26}" y="{hy-92}" width="52" height="28" rx="6" fill="{ZHELEZ}" {o(4)}/></g>'
    s += SL(Z_LETIT, sneg_letit(t, 30, 7, .7, .7))
    s += SL(Z_DAL, ulica_dal(0, 920, W, t, False, 51))
    cart_x = 1700 - A.seg(t, 3.4, 2.4) * 2200
    g = (f'<g transform="translate({cart_x:.0f},860)">'
         f'<rect x="-70" y="-40" width="160" height="60" rx="10" fill="url(#derev)" {o(6)}/>'
         f'<circle cx="-40" cy="24" r="26" fill="{ZHELEZ}" {o(4)}/><circle cx="60" cy="24" r="26" fill="{ZHELEZ}" {o(4)}/>')
    for i in range(5):
        g += f'<ellipse cx="{-30+i*20}" cy="-50" rx="16" ry="10" fill="{ZOL}" opacity=".85"/>'
    g += '</g>'
    s += SL(Z_DAL, g)
    s += ramka_pp("oba", "#141210", .4)
    s += vinetka(.42)
    return s


def sviter_s_odnim_rukavom(t):
    """Кресло: свитер с одним рукавом на спицах, клубок откатывается, кот трогает нить."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_DAL, brevna(-20, -20, W + 40, H + 40, 110))
    s += teplo(760, 620, 520, 440, .55)
    s += ten(760, 920, 260, 40, .5)
    s += f'<path d="M560,920 q-30,-320 200,-360 q230,-30 260,200 q20,170 -60,240 q-220,80 -400,-80 Z" fill="url(#tkan)" {o(7)}/>'
    sway = 6 * A.w(t, 2.6)
    s += f'<g transform="rotate({sway:.1f} 980 700)"><path d="M980,560 q90,10 60,220" fill="none" stroke="{TKAN}" stroke-width="40"/></g>'
    for i in range(6):
        s += f'<line x1="{1000+i*8}" y1="620" x2="{1006+i*8}" y2="760" stroke="url(#zhel)" stroke-width="5" opacity="{.6+.3*abs(A.w(t,1.4,i*.2)):.2f}"/>'
    roll = A.seg(t, .6, 6.0)
    ball_x = 900 + roll * 220
    s += SL(Z_PERED, f'<circle cx="{ball_x:.0f}" cy="1000" r="46" fill="{TKAN2}" {o(5)}/><path d="M{ball_x-30:.0f},980 q30,30 60,0" fill="none" stroke="{TKAN2}" stroke-width="4" opacity=".6"/>')
    s += SL(Z_PERED, kot(ball_x - 160, 980, t, .9))
    paw = 14 * abs(A.w(t, .8, .1))
    s += f'<circle cx="{ball_x-120+paw:.0f}" cy="1004" r="16" fill="#3b3430" {o(3)}/>'
    s += ramka_pp("oba", "#120e0b", .5)
    s += vinetka(.44)
    return s
def shkaf_nedodelannogo(t):
    """Открытый шкаф: недошитое платье на плечиках, книга с закладкой на полке."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_NEBO, holodny_svet(300, 160, 500, 380, .22))
    wx, wy, ww, wh = 430, 160, 760, 760
    s += SL(Z_DAL, f'<rect x="{wx-40}" y="{wy-40}" width="{ww+80}" height="{wh+80}" rx="14" fill="url(#derev)" {o(8)}/>')
    s += SL(Z_SRED, f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="8" fill="#15110d" opacity=".92"/>')
    s += SL(Z_SRED, f'<rect x="{wx-40}" y="{wy}" width="30" height="{wh}" fill="url(#derev)" {o(6)}/>'
                     f'<rect x="{wx+ww+10}" y="{wy}" width="30" height="{wh}" fill="url(#derev)" {o(6)}/>')
    bar_y = wy + 90
    s += SL(Z_SRED, f'<line x1="{wx+40}" y1="{bar_y}" x2="{wx+ww-40}" y2="{bar_y}" stroke="{ZHELEZ}" stroke-width="8"/>')
    sway = 6 * A.w(t, 2.8)
    hx = wx + ww * .5
    s += SL(Z_SRED, f'<g transform="translate({sway:.1f},0)">'
                     f'<path d="M{hx-40:.0f},{bar_y+6} q40,-24 80,0" fill="none" stroke="{ZHELEZ}" stroke-width="6"/>'
                     f'<path d="M{hx-120:.0f},{bar_y+16} q120,-50 240,0 l-10,360 q-110,36 -220,0 Z" fill="#f3ecdd" {o(6)}/>'
                     f'<path d="M{hx-60:.0f},{bar_y+30} h120" stroke="#ffffff" stroke-width="5" stroke-dasharray="3 9" opacity=".8"/>'
                     '</g>')
    rnd = random.Random(7)
    pins = ""
    for i in range(5):
        px = hx - 90 + rnd.random() * 180
        py = bar_y + 60 + rnd.random() * 260
        bl = .3 + .7 * (0.5 + 0.5 * A.w(t, .9 + rnd.random() * .6, rnd.random()))
        pins += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="4" fill="#f3f6fa" opacity="{bl:.2f}"/>'
    s += SL(Z_SRED, pins)
    shy = wy + wh - 170
    s += SL(Z_SRED, polka(wx + 40, shy, ww - 80))
    bx = wx + ww * .5
    s += SL(Z_SRED, f'<rect x="{bx-70:.0f}" y="{shy-16}" width="140" height="30" rx="4" fill="{TKAN2}" {o(5)}/>')
    card_dy = 4 * A.w(t, 3.3, .4)
    s += SL(Z_SRED, f'<rect x="{bx-26:.0f}" y="{shy-46+card_dy:.0f}" width="52" height="40" rx="2" fill="{KREM}" {o(3)}/>')
    rnd2 = random.Random(9)
    dust = ""
    for i in range(6):
        p = (t * .05 + i / 6) % 1.0
        ddx = bx - 60 + rnd2.random() * 120
        ddy = shy - 20 - p * 140
        dust += f'<circle cx="{ddx:.0f}" cy="{ddy:.0f}" r="2.4" fill="#eef4fb" opacity="{(1-p)*.6:.2f}"/>'
    s += SL(Z_PERED, dust)
    s += vinetka(.46)
    return s


def cherdak_s_taburetkoy(t):
    """Чердак в луче из слухового окна: табуретка на трёх ногах, паук спускается на сиденье."""
    s = f'<rect width="{W}" height="{H}" fill="#241c16"/>'
    s += SL(Z_NEBO, holodny_svet(960, 120, 700, 300, .18))
    s += SL(Z_DAL, f'<path d="M0,0 L960,220 L1920,0 L1920,140 L960,340 L0,140 Z" fill="#30251b" {o(7)}/>')
    for i in range(4):
        bx = 260 + i * 470
        s += SL(Z_DAL, f'<rect x="{bx}" y="90" width="26" height="520" fill="url(#brev)" {o(5)}/>')
    s += SL(Z_SRED, okno_izby(880, 40, 160, 150, t, moroz=.3, svet=True))
    s += SL(Z_SRED, luch(860, 190, 220, 760, t, op=.22))
    bob_x = 1180 + 40 * math.sin(t * .35)
    s += SL(Z_SRED, f'<rect x="200" y="470" width="1500" height="22" fill="url(#brev)" {o(5)}/>')
    s += SL(Z_SRED, ptica(bob_x, 460, t, 1.0, col="#8a8f93"))
    tx, ty = 560, 880
    s += SL(Z_SRED, f'<ellipse cx="{tx}" cy="{ty+40}" rx="140" ry="20" fill="#4a3a28" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="{tx-90}" y="{ty-30}" width="180" height="26" rx="6" fill="url(#derev)" {o(6)}/>')
    for lx in (-70, 0, 70):
        s += SL(Z_SRED, f'<rect x="{tx+lx-10}" y="{ty-4}" width="20" height="110" fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{tx+160},{ty+60} q40,-10 70,10 q-30,20 -70,10 Z" fill="{DOSKA2}" opacity=".7"/>')
    s += SL(Z_SRED, f'<rect x="{tx+170}" y="{ty+40}" width="18" height="90" fill="url(#derev)" {o(4)}/>')
    drop = A.ease(A.seg(t % 6.0, 0.8, 3.2))
    sy = ty - 30 - (1 - drop) * 360
    s += SL(Z_PERED, f'<line x1="{tx+10}" y1="{ty-200}" x2="{tx+10}" y2="{sy:.0f}" stroke="#cfcfcf" stroke-width="2" opacity=".6"/>')
    s += SL(Z_PERED, f'<circle cx="{tx+10}" cy="{sy:.0f}" r="10" fill="#1c1a18" {o(2)}/>')
    for ang in range(4):
        aa = ang * 1.2
        s += SL(Z_PERED, f'<line x1="{tx+10}" y1="{sy:.0f}" x2="{tx+10+14*math.cos(aa):.0f}" y2="{sy+10*math.sin(aa):.0f}" stroke="#1c1a18" stroke-width="2"/>')
    s += vinetka(.5)
    return s


def otkrytaya_fortochka(t):
    """Форточка приоткрыта, золотые струйки уходят на улицу — и сама захлопывается."""
    close = A.ease(A.seg(t, 2.6, 1.0))
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{H}" fill="#1c2434"/>')
    wx, wy, ww, wh = 1180, 180, 420, 520
    s += SL(Z_SRED, okno_izby(wx, wy, ww, wh, t, moroz=.4 * close))
    fx, fy, fw, fh = wx + ww - 150, wy + 30, 120, 140
    open_ = 1 - close
    s += SL(Z_SRED, f'<g transform="rotate({40*open_:.1f} {fx} {fy})">'
                     f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="url(#stekl)" opacity=".8" {o(5)}/></g>')
    lever_ang = 70 * close
    s += SL(Z_SRED, f'<g transform="rotate({lever_ang:.1f} {fx+fw-10} {fy+fh+10})">'
                     f'<rect x="{fx+fw-10}" y="{fy+fh+6}" width="40" height="10" rx="4" fill="url(#zhel)" {o(3)}/></g>')
    for i in range(3):
        p = (t * .5 + i * .33) % 1.0
        sx = fx + fw * .5 + 60 * p
        sy = fy + fh * .5 - 40 * p
        s += SL(Z_SRED, f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{(10+10*p)*(1-close*.8):.1f}" fill="url(#zol)" opacity="{(1-p)*.6*(1-close*.8):.2f}"/>')
    cx0 = wx - 40
    s += SL(Z_SRED, zanaveska(cx0, wy + 20, wh - 60, 150, t=t, sgn=1 if open_ > 0.5 else -1))
    tx, ty = 420, 760
    s += SL(Z_SRED, stol(tx, ty, 420))
    s += SL(Z_SRED, teplo(tx + 210, ty - 60, 260 * close, 180 * close, .5 * close))
    fin = A.ease(A.seg(t, 4.2, 1.4))
    s += SL(Z_SRED, f'<g opacity="{fin:.2f}">' + karavay(tx + 90, ty - 10, .8) + '</g>')
    s += SL(Z_SRED, f'<rect x="{tx+200}" y="{ty-70}" width="150" height="60" rx="14" fill="{TKAN2}" opacity="{fin:.2f}"/>')
    s += SL(Z_SRED, par(tx + 90, ty - 70, t, 3, .4 * fin))
    s += SL(Z_SRED, figura(1680, 980, 300, t, kant="#cfe4f5", ph=.3))
    s += vinetka(.45)
    return s


def tri_dodelki(t):
    """Три доделки по словам: рукав дорастает, страница перелистывается, пуговица пришивается."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{H}" fill="#201a2c" opacity=".6"/>')
    s += SL(Z_DAL, teplo(W * .5, H * .3, 900, 500, .3))
    kx, ky = 330, 760
    grow = A.ease(A.seg(t, 0.8, 2.6))
    s += SL(Z_SRED, f'<rect x="{kx-20}" y="{ky-220*grow:.0f}" width="40" height="{220*grow:.0f}" rx="18" fill="{TKAN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<line x1="{kx-60}" y1="{ky-220*grow:.0f}" x2="{kx+70}" y2="{ky-240*grow-30:.0f}" stroke="#cfd6de" stroke-width="7"/>')
    s += SL(Z_SRED, f'<line x1="{kx+30}" y1="{ky-220*grow:.0f}" x2="{kx+140}" y2="{ky-240*grow-30:.0f}" stroke="#cfd6de" stroke-width="7"/>')
    bx, by = 870, 820
    flip = A.ease(A.seg(t % 3.0, 1.0, .8))
    scl = (1 - 2 * flip) if flip < 0.5 else (2 * flip - 1)
    s += SL(Z_SRED, f'<rect x="{bx-120}" y="{by-20}" width="240" height="40" rx="6" fill="{KREM}" {o(5)}/>')
    s += SL(Z_SRED, f'<g transform="translate({bx},{by-10}) scale({scl:.3f},1)">'
                     f'<path d="M0,0 h120 v-200 q-60,-20 -120,0 Z" fill="{RUSH}" {o(3)}/></g>')
    mark_y = by - 180 + 60 * flip
    s += SL(Z_PERED, f'<rect x="{bx-6}" y="{mark_y:.0f}" width="12" height="70" fill="{TKAN}" opacity="{1-flip:.2f}"/>')
    sx, sy = 1480, 820
    s += SL(Z_SRED, f'<ellipse cx="{sx}" cy="{sy+40}" rx="60" ry="16" fill="{KREM}" {o(4)}/>')
    stitch = A.ease(A.seg(t, 2.2, 2.0))
    btn_x = sx - 60 + 60 * stitch
    btn_y = sy + 40 - 40 * stitch * .6
    s += SL(Z_SRED, f'<rect x="{sx+10}" y="{sy-220}" width="150" height="260" rx="12" fill="{TKAN2}" {o(6)}/>')
    s += SL(Z_SRED, f'<circle cx="{btn_x:.0f}" cy="{btn_y:.0f}" r="18" fill="#2b2420" {o(3)}/>')
    s += SL(Z_PERED, f'<line x1="{btn_x-10:.0f}" y1="{btn_y:.0f}" x2="{btn_x+10:.0f}" y2="{btn_y:.0f}" stroke="#e8e0cf" stroke-width="2" opacity="{stitch:.2f}"/>')
    s += vinetka(.4)
    return s


def lopata_papka_i_aptechka(t):
    """Три отложенных дела во дворе: лопата у ямы, папка, аптечка — иней и снег."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, False))
    s += SL(Z_NEBO, oblaka(t, 150, 4, 11, .40))
    s += SL(Z_DAL, _ulica_dal(0, 700, W, t, True, 9))
    s += SL(Z_DAL, pleten(60, 560, 1800, 150, 16))
    s += SL(Z_SRED, _sneg_lezhit_polosa(0, 690, W, 120))
    s += SL(Z_SRED, f'<rect y="760" width="{W}" height="{H-760}" fill="url(#sneg)"/>')
    s += holodny_svet(960, 560, 900, 520, .30)
    # 1. лопата воткнута у размеченной ямы
    nak = 2.0 * A.w(t, 3.2)
    s += SL(Z_SRED, f'<g transform="rotate({-9+nak:.1f} 300 880)">'
                    f'<rect x="288" y="430" width="24" height="450" rx="10" fill="url(#derev)" {o(5)}/>'
                    f'<path d="M262,860 h76 l-10,120 h-56 Z" fill="url(#zhel)" {o(5)}/></g>')
    s += SL(Z_SRED, f'<ellipse cx="420" cy="930" rx="150" ry="34" fill="#4c4036" opacity=".55"/>')
    s += SL(Z_SRED, f'<path d="M300,930 q120,-26 240,0" stroke="#3b332c" stroke-width="7"'
                    f' fill="none" stroke-dasharray="26 18" opacity=".8"/>')
    s += SL(Z_SRED, inej(258, 430, 90, t, 7, 4, "#f2fbff", 460))
    # 2. толстая папка с тесёмками — тесёмки завязываются сами
    kk = A.ease(A.seg(t, 2.0, 1.2))
    s += SL(Z_SRED, f'<g transform="translate(830,700)">'
                    f'<rect x="-150" y="-10" width="300" height="210" rx="10" fill="url(#krem)" {o(6)}/>'
                    f'<rect x="-150" y="-10" width="300" height="24" rx="8" fill="url(#list)" {o(4)}/>'
                    f'<rect x="-150" y="60" width="300" height="10" fill="#c9b894" opacity=".7"/>'
                    f'<path d="M-150,96 h300" stroke="#c9b894" stroke-width="8" opacity=".7"/>'
                    f'<path d="M-8,96 q{-40+40*kk:.0f},{46-20*kk:.0f} {-70+56*kk:.0f},{80-30*kk:.0f}"'
                    f' stroke="{TKAN}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                    f'<path d="M8,96 q{40-40*kk:.0f},{46-20*kk:.0f} {70-56*kk:.0f},{80-30*kk:.0f}"'
                    f' stroke="{TKAN}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                    f'</g>')
    s += SL(Z_SRED, _sneg_lezhit_polosa(680, 666, 300, 30))
    s += SL(Z_SRED, inej(690, 672, 280, t, 9, 7, "#f2fbff", 26))
    # 3. аптечка — крышка закрывается
    ug = 74 * (1 - A.ease(A.seg(t, 4.0, 1.1)))
    s += SL(Z_SRED, f'<g transform="translate(1480,760)">'
                    f'<rect x="-170" y="0" width="340" height="150" rx="12" fill="#eef2f4" {o(6)}/>'
                    f'<rect x="-22" y="40" width="44" height="14" rx="4" fill="{KRAS}"/>'
                    f'<rect x="-8" y="26" width="16" height="42" rx="4" fill="{KRAS}"/>'
                    f'<g transform="rotate({-ug:.0f} -170 0)">'
                    f'<rect x="-170" y="-26" width="340" height="30" rx="8" fill="#dfe6ea" {o(5)}/></g>'
                    f'</g>')
    s += SL(Z_SRED, ten(1480, 915, 180, 22, .5))
    s += SL(Z_LETIT, sneg_letit(t, 40, 6, .65, .8))
    s += SL(Z_PERED, _mebel_hlam(1810, 980, 200, t, 21))
    s += vinetka(.44)
    return s
def merzlaya_gryadka_i_kolyshki(t):
    """Лопата отскакивает от мёрзлой земли; рядом колышки в инее; хозяин уносит лопату."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, oblaka(t, 150, 3, 9))
    s += SL(Z_DAL, _sneg_lezhit_polosa(0, 640, W, 90))
    s += SL(Z_DAL, f'<path d="M0,700 q480,-40 960,0 q480,40 960,0 L{W},760 L0,760 Z" fill="#5a5142" opacity=".8"/>')
    bounce = abs(A.w(t, 1.2))
    lx, ly = 560, 760 - 50 * bounce
    s += SL(Z_SRED, f'<ellipse cx="{lx}" cy="800" rx="70" ry="16" fill="#2a241c" opacity=".35"/>')
    s += SL(Z_SRED, f'<rect x="{lx-10}" y="{ly-320:.0f}" width="20" height="320" fill="url(#derev)" {o(5)}/>'
                     f'<path d="M{lx-44},{ly:.0f} q44,-28 88,0 l-8,60 q-36,16 -72,0 Z" fill="{ZHELEZ}" {o(5)}/>')
    for i in range(4):
        kx = 860 + i * 90
        s += SL(Z_SRED, f'<rect x="{kx-7}" y="700" width="14" height="110" fill="url(#derev)" {o(4)}/>')
        s += SL(Z_PERED, inej(kx - 20, 690, 40, t, 4, 10 + i, R=40))
    walk = A.ease(A.seg(t, 1.2, 3.0))
    hx = 1400 + walk * 420
    s += SL(Z_SRED, figura(hx, 850, 330, t, kant="#cfe4f5", telogreyka=True))
    s += SL(Z_SRED, f'<rect x="{hx+20:.0f}" y="640" width="12" height="220" fill="url(#derev)"/>')
    s += vinetka(.4)
    return s


def komnata_pered_remontom(t):
    """Комната перед ремонтом: стремянка, обои, мебель под плёнкой, шкаф посреди комнаты."""
    revert = A.ease(A.seg(t, 3.0, 1.6))
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{H}" fill="#8a8f93"/>')
    s += SL(Z_SRED, f'<rect x="80" y="620" width="420" height="260" rx="20" fill="#c9d3d6" opacity=".82" {o(5)}/>')
    ripple = 6 * A.w(t, 2.1)
    s += SL(Z_SRED, f'<path d="M80,{700+ripple:.0f} q210,-30 420,0" fill="none" stroke="#ffffff" stroke-width="5" opacity=".5"/>')
    lad_sway = 3 * A.w(t, 3.4)
    s += SL(Z_SRED, f'<g transform="rotate({lad_sway*(1-revert*.7):.2f} 760 980)">'
                     f'<path d="M700,980 L760,560 L820,980 Z" fill="none" stroke="url(#derev)" stroke-width="12"/>'
                     f'<line x1="712" y1="860" x2="808" y2="860" stroke="url(#derev)" stroke-width="8"/>'
                     f'<line x1="722" y1="740" x2="798" y2="740" stroke="url(#derev)" stroke-width="8"/></g>')
    step = 70 * (1 - revert)
    sx = 1260 + step
    s += SL(Z_SRED, f'<rect x="{sx-100:.0f}" y="560" width="200" height="420" rx="10" fill="url(#derev)" {o(7)}/>')
    s += SL(Z_SRED, ten(sx, 990, 120, 20, .4))
    roll = 1 - revert
    s += SL(Z_SRED, f'<rect x="1560" y="900" width="{80+260*roll:.0f}" height="36" rx="16" fill="url(#list)" {o(4)}/>')
    s += SL(Z_SRED, f'<circle cx="1560" cy="918" r="40" fill="url(#list)" {o(4)}/>')
    s += vinetka(.38)
    return s


def zakrytaya_banka_kraski(t):
    """Крупно банка краски без этикетки: отвёртка поддевает крышку и замирает."""
    s = f'<rect width="{W}" height="{H}" fill="#2a2c30"/>'
    s += SL(Z_DAL, teplo(W * .55, H * .4, 700, 500, .22))
    cx, cy = 980, 660
    s += SL(Z_SRED, ten(cx, cy + 190, 260, 36, .5))
    s += SL(Z_SRED, f'<rect x="{cx-220}" y="{cy-180}" width="440" height="380" rx="26" fill="#9aa3a8" {o(9)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{cx}" cy="{cy-180}" rx="220" ry="34" fill="#c3cbce" {o(7)}/>')
    pry = A.ease(A.seg(t, 1.0, 2.2))
    lid_dy = -18 * pry
    s += SL(Z_SRED, f'<ellipse cx="{cx}" cy="{cy-180+lid_dy:.0f}" rx="226" ry="30" fill="#d7dde0" {o(7)}/>')
    ang = -40 * pry
    s += SL(Z_PERED, f'<g transform="rotate({ang:.1f} {cx+220} {cy-190})">'
                     f'<rect x="{cx+218}" y="{cy-230}" width="16" height="140" fill="{ZHELEZ}" {o(4)}/>'
                     f'<rect x="{cx+206}" y="{cy-120}" width="40" height="60" rx="8" fill="{TKAN}" {o(4)}/></g>')
    glisten = .75 + .1 * abs(A.w(t, 3.0))
    s += SL(Z_PERED, f'<path d="M{cx-220},{cy-40} q-18,30 0,60 q18,-10 0,-60 Z" fill="url(#zol)" opacity="{glisten:.2f}"/>')
    s += SL(Z_PERED, blik(cx, cy - 190, t, .5))
    s += vinetka(.5)
    return s


def sobrannyy_chemodan_u_dveri(t):
    """Собранный чемодан у открытой двери, в которую метёт снег — дверь закрывается сама."""
    close = A.ease(A.seg(t, 2.0, 1.2))
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{H}" fill="#161b26"/>')
    dx, dy_, dw, dh = 1200, 160, 360, 760
    s += SL(Z_SRED, dver(dx, dy_, dw, dh, open_=1 - close))
    s += SL(Z_LETIT, sneg_letit(t, 30, 21, .7 * (1 - close)))
    cx, cy = 640, 820
    s += SL(Z_SRED, ten(cx, cy + 90, 180, 22, .45))
    s += SL(Z_SRED, f'<rect x="{cx-170}" y="{cy-120}" width="340" height="220" rx="18" fill="{TKAN2}" {o(7)}/>')
    sway = 6 * A.w(t, 2.6)
    s += SL(Z_SRED, f'<rect x="{cx-200+sway:.0f}" y="{cy-40}" width="36" height="140" fill="{DOSKA2}" opacity=".85"/>'
                     f'<rect x="{cx+170+sway:.0f}" y="{cy-40}" width="36" height="140" fill="{DOSKA2}" opacity=".85"/>')
    reopen = A.ease(A.seg(t, 3.6, 1.2))
    s += SL(Z_SRED, f'<g transform="translate(0,{-80*reopen:.0f})">'
                     f'<rect x="{cx-170}" y="{cy-160}" width="340" height="40" rx="10" fill="{TKAN2}" opacity="{reopen:.2f}" {o(5)}/></g>')
    item_y = cy - 170 - 260 * reopen
    s += SL(Z_PERED, f'<rect x="{cx-60}" y="{item_y:.0f}" width="120" height="50" rx="10" fill="{KREM}" opacity="{reopen:.2f}" {o(3)}/>')
    s += SL(Z_SRED, teplo(1750, 700, 300, 400, .5 * reopen))
    s += vinetka(.42)
    return s


def ulichnyy_gradusnik(t):
    """За окном уличный градусник без цифр: столбик падает, иней ползёт по стеклу."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{H}" fill="#121722"/>')
    wx, wy, ww, wh = 120, 200, 640, 680
    s += SL(Z_SRED, okno_izby(wx, wy, ww, wh, t, moroz=.2))
    gx, gy = wx + ww * .6, wy + 60
    s += SL(Z_SRED, f'<rect x="{gx-14:.0f}" y="{gy}" width="28" height="420" rx="12" fill="#e7eef3" {o(5)}/>')
    drop_ = A.ease(A.seg(t, 0.9, 3.2))
    s += SL(Z_SRED, f'<rect x="{gx-8:.0f}" y="{gy+6}" width="16" height="{20+320*drop_:.0f}" rx="6" fill="{KRAS}"/>')
    frost = A.ease(A.seg(t, 1.6, 3.0))
    s += SL(Z_PERED, morozny_uzor(wx, wy, ww, wh, t, op=.45 * frost))
    cr = 4 * A.w(t, 5.0)
    s += SL(Z_SRED, f'<line x1="{gx-30:.0f}" y1="{gy+440}" x2="{gx+30:.0f}" y2="{gy+452+cr:.0f}" stroke="#c9d6df" stroke-width="2" opacity=".5"/>')
    s += vinetka(.44)
    return s


def peremetennaya_doroga_i_tonkiy_led(t):
    """Вешки тонут в снегу у дороги; у реки нога пробует тонкий лёд и отдёргивается."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 14))
    s += SL(Z_DAL, _sneg_lezhit_polosa(0, 560, W, 160))
    for i in range(6):
        vx = 140 + i * 260
        bank = 10 * A.w(t, 3.0, i * .2)
        s += SL(Z_SRED, f'<line x1="{vx+bank:.0f}" y1="700" x2="{vx:.0f}" y2="560" stroke="url(#derev)" stroke-width="10"/>')
        s += SL(Z_SRED, inej(vx - 18, 640, 36, t, 3, 20 + i, R=40))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="920" rx="760" ry="90" fill="url(#led)" opacity=".85" {o(6)}/>')
    bend = abs(A.w(t, 1.6))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="{910+6*bend:.0f}" rx="140" ry="{26+bend*10:.0f}" fill="#2a5560" opacity="{.35+.3*bend:.2f}"/>')
    test = (t * .4) % 2.0
    foot_y = 860 - 20 * max(0, 1 - abs(test - 1.0))
    s += SL(Z_PERED, f'<ellipse cx="960" cy="{foot_y:.0f}" rx="40" ry="18" fill="#2b2420" opacity=".8"/>')
    s += SL(Z_SRED, figura(1500, 980, 320, t, kant="#cfe4f5", ph=.6))
    s += SL(Z_SRED, par_izo_rta(1500, 760, t, .2))
    s += SL(Z_NEBO, f'<circle cx="300" cy="640" r="10" fill="{SVET}" opacity="{.4+.4*abs(A.w(t,2.3)):.2f}"/>')
    s += vinetka(.42)
    return s


def sani_pod_navesom(t):
    """Сани под навесом, оглобли вверх; дым над крышей, конь в стойле жуёт сено."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += SL(Z_NEBO, nebo("rassv", t, False))
    s += SL(Z_DAL, _sneg_lezhit_polosa(0, 760, W, 140))
    s += SL(Z_DAL, izba_snaruzhi(1180, 860, 560, t, svet=True, truba=True))
    s += SL(Z_DAL, f'<ellipse cx="1348" cy="610" rx="50" ry="60" fill="{SVET}" opacity="{.2+.15*abs(A.w(t,3.3)):.2f}"/>')
    nx, ny = 160, 760
    s += SL(Z_SRED, f'<path d="M{nx-20},{ny} h520 l-40,-90 h-440 Z" fill="{DOSKA2}" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{nx}" y="{ny}" width="18" height="220" fill="url(#derev)" {o(4)}/>'
                     f'<rect x="{nx+460}" y="{ny}" width="18" height="220" fill="url(#derev)" {o(4)}/>')
    sway = 2 * A.w(t, 4.2)
    s += SL(Z_SRED, f'<g transform="rotate({sway:.1f} {nx+250} {ny+180})">'
                     f'<path d="M{nx+60},{ny+180} q180,20 360,0 q0,30 -30,40 l-300,0 q-30,-10 -30,-40 Z" fill="{TKAN}" {o(6)}/>'
                     f'<path d="M{nx+60},{ny+170} q-40,-120 -10,-220" fill="none" stroke="url(#derev)" stroke-width="12"/>'
                     f'<path d="M{nx+420},{ny+170} q40,-120 10,-220" fill="none" stroke="url(#derev)" stroke-width="12"/></g>')
    hx, hy = 820, 940
    chew = 4 * A.w(t, 2.0)
    s += SL(Z_SRED, f'<rect x="{hx-10}" y="{hy-260}" width="300" height="260" fill="none" stroke="url(#derev)" stroke-width="10"/>')
    s += SL(Z_SRED, f'<ellipse cx="{hx+130}" cy="{hy-140}" rx="110" ry="130" fill="#4a3426" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{hx+30}" cy="{hy-220+chew:.0f}" rx="40" ry="60" fill="#4a3426" {o(5)}/>')
    s += SL(Z_PERED, f'<path d="M{hx+10},{hy-180+chew/2:.0f} q20,10 40,0" stroke="{RUSH}" stroke-width="6" fill="none"/>')
    s += vinetka(.4)
    return s


def maminy_ruki_nad_sumkoy(t):
    """Раскрытая сумка на табуретке: шарф не помещается, бечёвка затягивается, молния ползёт."""
    morph = A.ease(A.seg(t, 3.4, 1.3))
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{H}" fill="#241f2c"/>')
    s += SL(Z_DAL, teplo(W * .5, H * .35, 700, 440, .3))
    tx, ty = 920, 760
    s += SL(Z_SRED, f'<rect x="{tx-120}" y="{ty}" width="240" height="30" rx="8" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, f'<rect x="{tx-100}" y="{ty-170}" width="200" height="170" rx="26" fill="{TKAN2}" {o(7)}/>')
    wig = 14 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<path d="M{tx-80+wig:.0f},{ty-170} q20,-70 60,-60 q10,50 -20,70 Z" fill="{KREM}" {o(4)}/>')
    tie = A.ease(A.seg(t, 1.4, 1.6))
    s += SL(Z_SRED, f'<path d="M{tx-100},{ty-30} q{100*(1-tie):.0f},{20*tie:.0f} 200,0" fill="none" stroke="{DOSKA2}" stroke-width="6"/>')
    zp = (t * .3) % 1.0
    s += SL(Z_PERED, f'<circle cx="{tx-100+200*zp:.0f}" cy="{ty-100}" r="8" fill="{ZHELEZ}" {o(3)}/>')
    sleeve = 20 * A.w(t, 2.4)
    s += SL(Z_PERED, f'<path d="M{tx-60},{ty-260} q40,{40+sleeve:.0f} 60,120 q-40,20 -70,-10 q-10,-80 10,-110 Z" fill="{TKAN}" opacity=".85" {o(5)}/>')
    pkt_x, pkt_y = tx + 220, ty - 90
    s += SL(Z_SRED, f'<g opacity="{1-morph:.2f}">'
                     f'<rect x="{pkt_x-28}" y="{pkt_y-70}" width="56" height="140" rx="20" fill="#cfd6de" {o(4)}/></g>')
    s += SL(Z_SRED, f'<g opacity="{morph:.2f}">'
                     f'<path d="M{pkt_x-40},{pkt_y-60} h80 v120 h-80 Z" fill="{KREM}" {o(4)}/>'
                     f'<path d="M{pkt_x-40},{pkt_y} q40,-20 80,0" stroke="{DOSKA2}" stroke-width="5" fill="none"/></g>')
    s += vinetka(.42)
    return s
def sharf_na_zimney_platforme(t):
    """Платформа в сумерках: фонарь качается, человек спиной прячет лицо в шарф."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, zvezdy=True, seed=9)
    s += oblaka(t, y=140, n=3, seed=4, op=.35)
    s += tuman(t, y=720, op=.4)
    pf = (f'<rect x="0" y="760" width="{W}" height="320" fill="url(#beton)" {o(6)}/>')
    for i in range(14):
        xx = 40 + i * 140
        pf += f'<line x1="{xx}" y1="700" x2="{xx}" y2="760" stroke="{ZHELEZ}" stroke-width="10"/>'
    pf += f'<rect x="0" y="690" width="{W}" height="14" fill="{ZHELEZ}" {o(4)}/>'
    s += SL(Z_SRED, pf)
    lx, ly = 1500, 760
    sw = 3.2 * A.w(t, 2.6)
    lamp = (f'<g transform="rotate({sw:.2f} {lx} {ly-420})">'
            f'<rect x="{lx-9}" y="{ly-420}" width="18" height="420" fill="{ZHELEZ}" {o(4)}/>'
            f'<path d="M{lx-46},{ly-420} h92 l-14,70 h-64 Z" fill="{CHUGUN}" {o(5)}/>'
            + teplo(lx, ly - 390, 160, 150, .6)
            + f'<ellipse cx="{lx}" cy="{ly-390}" rx="30" ry="36" fill="{SVET}" opacity=".85"/>'
            '</g>')
    s += SL(Z_SRED, lamp)
    fx, fy = 760, 920
    fig = figura(fx, fy, 420, t, col="#17161c", kant=LED, telogreyka=True)
    scarf = ""
    for i, dx in enumerate((-1, 1)):
        ph = i * .4
        wig = 18 * A.w(t, 1.6, ph)
        scarf += (f'<path d="M{fx+dx*38},{fy-300} q{dx*10+wig:.0f},70 {dx*26+wig*1.4:.0f},150"'
                  f' stroke="{TKAN}" stroke-width="30" stroke-linecap="round" fill="none" opacity=".92"/>')
    s += SL(Z_SRED, fig + scarf)
    s += SL(Z_SRED, par_izo_rta(fx + 6, fy - 360, t, .1, 1.0, .6))
    s += SL(Z_PERED, inej(40, 820, 400, t, 10, 7))
    s += sneg_letit(t, n=50, seed=12)
    s += vinetka(.46)
    return s


def sbory_u_zerkala(t):
    """Прихожая: свитер натягивают, термос убирают в сумку, идут стрелки часов."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += f'<rect width="{W}" height="{H}" fill="#cfd6de"/>'
    s += f'<rect y="{H-70}" width="{W}" height="70" fill="{POL2}" {o(4)}/>'
    s += SL(Z_DAL, okno_izby(120, 160, 260, 320, t, svet=False, moroz=.3))
    s += SL(Z_DAL, holodny_svet(260, 300, 300, 260, .3))
    s += SL(Z_SRED, lampa(1250, 300, t, .6, abazhur=True))
    mx, my = 1250, 540
    mirror = (f'<ellipse cx="{mx}" cy="{my}" rx="150" ry="230" fill="url(#zol)" {o(7)}/>'
              f'<ellipse cx="{mx}" cy="{my}" rx="118" ry="196" fill="url(#stekl)" opacity=".85"/>'
              f'<ellipse cx="{mx-30}" cy="{my-60}" rx="30" ry="90" fill="#ffffff" opacity=".22"/>')
    s += SL(Z_SRED, mirror)
    fx, fy = 1020, 880
    fig = figura(fx, fy, 480, t, col="#232030", kant=SVET, profil=True)
    k1 = A.ease(A.seg(t, .9, 1.6))
    sw_y = fy - 60 - k1 * 220
    sweater = (f'<path d="M{fx-90},{fy-40} q90,-24 180,0 L{fx+74},{sw_y:.0f}'
               f' q-74,-30 -148,0 Z" fill="{TKAN2}" opacity="{.5+.5*k1:.2f}" {o(5)}/>')
    s += SL(Z_SRED, fig + sweater)
    bx, by = 760, 980
    bag = f'<path d="M{bx-70},{by} q-6,-110 70,-120 q76,10 70,120 Z" fill="url(#derev)" {o(5)}/>'
    k2 = A.ease(A.seg(t, 2.0, 1.4))
    termy = by - 220 + k2 * 180
    term = (f'<rect x="{bx-18:.0f}" y="{termy:.0f}" width="36" height="100" rx="12"'
            f' fill="{ZHELEZ}" opacity="{1-k2*.7:.2f}" {o(4)}/>')
    s += SL(Z_SRED, bag + term)
    s += SL(Z_SRED, hodiki(1500, 320, t, 1.1))
    s += vinetka(.4)
    return s


def dve_kumushki_na_lavke(t):
    """Лавка у ворот: платки качаются, воробей, облачка «ох» и монеты прочь."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t)
    s += SL(Z_DAL, pleten(140, 760, 1500, 180, 11))
    s += SL(Z_DAL, sneg_lezhit(640, 20))
    lx, ly = 760, 900
    s += SL(Z_SRED, lavka(lx, ly, 420))
    f1 = figura(lx + 90, ly, 300, t, col="#241f2c", kant=INEY, platok=True, ph=0)
    f2 = figura(lx + 300, ly, 300, t, col="#2c2230", kant=INEY, platok=True, ph=.5)
    s += SL(Z_SRED, f1 + f2)
    s += SL(Z_SRED, ptica(1400, 680, t, 1.0, KRAS, .2, "#5b6a78"))
    oh = ""
    for i in range(4):
        t0 = .9 + i * 1.0
        k = A.ease(A.seg(t, t0, .8))
        if k <= 0:
            continue
        ox = lx + 90 + (i % 2) * 210
        oy = ly - 260 - k * 160
        r = 34 + 10 * k
        oh += (f'<ellipse cx="{ox:.0f}" cy="{oy:.0f}" rx="{r:.0f}" ry="{r*.7:.0f}" fill="#ffffff"'
               f' opacity="{(1-k)*.85:.2f}"/>'
               f'<circle cx="{ox-r*.6:.0f}" cy="{oy+r*.4:.0f}" r="{r*.3:.0f}" fill="#ffffff" opacity="{(1-k)*.8:.2f}"/>')
    s += SL(Z_SRED, oh)
    coins = ""
    for i in range(3):
        t0 = 2.4 + i * .9
        k = A.seg(t, t0, 1.6)
        if k <= 0:
            continue
        cx_ = lx + 300 + k * 260
        cy_ = ly + 30 - 20 * math.sin(k * 3.1)
        coins += (f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="18" ry="12" fill="url(#med)"'
                  f' opacity="{1-k*.4:.2f}" {o(3)}/>')
    s += SL(Z_SRED, coins)
    s += SL(Z_PERED, inej(0, 1000, W, t, 20, 4))
    s += sneg_letit(t, n=40, seed=9)
    s += vinetka(.42)
    return s


def sani_s_drovami_i_ohi(t):
    """Сани с дровами стоят, человек охает, а за лесом быстро садится солнце."""
    s = f'<rect width="{W}" height="{H}" fill="url(#zakat)"/>'
    k = A.ease(A.seg(t, .8, 3.0))
    sx, sy0, sy1 = 1500, 260, 660
    sun = f'<circle cx="{sx}" cy="{sy0+(sy1-sy0)*k:.0f}" r="90" fill="{SVET}" opacity=".9"/>'
    s += SL(Z_NEBO, sun)
    forest = ""
    rnd1 = random.Random(6)
    for i in range(9):
        tx = i * (W / 8)
        th = 140 + rnd1.uniform(-30, 60)
        forest += f'<path d="M{tx:.0f},700 l-40,0 l40,{-th:.0f} l40,{th:.0f} Z" fill="#1c2436" opacity=".88"/>'
    s += SL(Z_DAL, forest)
    s += SL(Z_DAL, sneg_lezhit(700, 18))
    sax, say = 560, 940
    sani = f'<path d="M{sax-170},{say} q-16,30 10,50 h330 q26,-20 10,-50 Z" fill="url(#derev)" {o(6)}/>'
    logs = ""
    for i in range(5):
        lx_ = sax - 130 + i * 60
        logs += f'<ellipse cx="{lx_}" cy="{say-70}" rx="36" ry="30" fill="url(#brev)" {o(4)}/>'
    kl = A.seg(t, 3.0, 1.6)
    if kl > 0:
        lxx = sax - 130 + kl * 340
        lyy = say - 70 + kl * kl * 70
        logs += (f'<ellipse cx="{lxx:.0f}" cy="{lyy:.0f}" rx="30" ry="26" fill="url(#brev)"'
                 f' opacity="{1-kl*.3:.2f}" {o(4)}/>')
    s += SL(Z_SRED, sani + logs)
    fig = figura(sax + 260, say + 20, 420, t, col="#1d1a22", kant=SVET, telogreyka=True)
    sway = 6 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<g transform="rotate({sway:.1f} {sax+260} {say-150})">{fig}</g>')
    k2 = (t * .5) % 1.0
    oh_r = 30 + 16 * (1 - abs(k2 - .5) * 2)
    s += SL(Z_SRED, f'<ellipse cx="{sax+360}" cy="{say-220-k2*80:.0f}" rx="{oh_r:.0f}" ry="{oh_r*.7:.0f}"'
                     f' fill="#ffffff" opacity="{(1-k2)*.8:.2f}"/>')
    s += vinetka(.4)
    return s


def babushka_podnimaet_ladon(t):
    """Мостик в память: бабушка поднимает рукав, облачко «ох» тает, чай дрожит."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += f'<rect width="{W}" height="{H}" fill="#c7cdd3"/>'
    s += SL(Z_DAL, pech(120, 560, 420, 460, t, ogon_on=True))
    s += SL(Z_SRED, stol(640, 820, 520))
    g = figura(760, 980, 360, t, col="#2a2430", kant=SVET, profil=True)
    s += SL(Z_SRED, g)
    bx, by = 1260, 960
    bab = figura(bx, by, 380, t, col="#241e28", kant=ORA, platok=True, profil=True)
    k = A.ease(A.seg(t, 1.0, 1.2))
    sleeve = (f'<path d="M{bx-40},{by-220} q{-10-k*30:.0f},{-60-k*160:.0f} {10-k*10:.0f},{-80-k*210:.0f}"'
              f' stroke="{TKAN}" stroke-width="34" stroke-linecap="round" fill="none"/>')
    s += SL(Z_SRED, bab + sleeve)
    k2 = A.seg(t, .8, 1.0)
    if k2 < 1:
        r = 40 * (1 - k2 * .5)
        s += SL(Z_SRED, f'<ellipse cx="{bx-220}" cy="{by-300-k2*60:.0f}" rx="{r:.0f}" ry="{r*.7:.0f}"'
                         f' fill="#ffffff" opacity="{1-k2:.2f}"/>')
    cx_, cy_ = 700, 800
    trem = 2 * A.w(t, .6)
    s += SL(Z_SRED, f'<ellipse cx="{cx_+trem:.0f}" cy="{cy_}" rx="26" ry="10" fill="#8a5a2a" {o(3)}/>'
                     f'<ellipse cx="{cx_+trem:.0f}" cy="{cy_}" rx="34" ry="14" fill="none" {o(4)}/>')
    s += vinetka(.4)
    return s


def babushka_u_skripuchey_kalitki(t):
    """Калитка в плетне скрипит и качается, ведро качается, бабушка улыбается."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t)
    s += SL(Z_DAL, pleten(0, 760, 760, 170, 7))
    s += SL(Z_DAL, pleten(1080, 760, 760, 170, 13))
    kalx, kaly = 840, 600
    sw = 10 * A.w(t, 1.4)
    gate = (f'<g transform="rotate({sw:.1f} {kalx} {kaly+160})">'
            + dver(kalx - 100, kaly, 200, 320, open_=.12, kruchok=True) + '</g>')
    s += SL(Z_SRED, gate)
    bx, by = 600, 940
    bab = figura(bx, by, 380, t, col="#241f28", kant=SVET, platok=True)
    sw2 = 8 * A.w(t, 2.0, .3)
    vedro = (f'<g transform="rotate({sw2:.1f} {bx-80} {by-80})">'
             f'<path d="M{bx-120},{by-60} h80 l-10,120 h-60 Z" fill="{ZHELEZ}" {o(4)}/>'
             f'<path d="M{bx-108},{by-60} q40,-50 68,0" fill="none" stroke="{ZHELEZ}" stroke-width="6"/></g>')
    s += SL(Z_SRED, bab + vedro)
    sos = figura(1180, 900, 340, t, col="#2c2634", kant=SVET, platok=True, profil=True)
    s += SL(Z_SRED, sos)
    s += SL(Z_PERED, sneg_lezhit(960, 16))
    s += sneg_letit(t, n=30, seed=15)
    s += vinetka(.4)
    return s


def tri_oblachka_zhalob(t):
    """Героиня идёт по улице, над ней встают и гаснут три облачка-значка."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, seed=14)
    s += SL(Z_DAL, panelka(200, 820, 1500, t, 5))
    kf = A.ease(A.seg(t, 3.0, 1.4))
    fonari = ""
    for fx in (260, 900, 1540):
        fonari += (f'<rect x="{fx-8}" y="600" width="16" height="200" fill="{ZHELEZ}"/>'
                   + teplo(fx, 600, 90 * kf + 10, 80 * kf + 10, .5 * kf))
    s += SL(Z_SRED, fonari)
    hx = 300 + (t * 60) % 1400
    fig = figura(hx, 940, 400, t, col="#201c28", kant=INEY, telogreyka=True)
    s += SL(Z_SRED, fig)
    icons = (("grad", "#e9eef2"), ("cena", ZOL), ("tuch", "#cfd7e0"))
    out = ""
    for i, (kind, col) in enumerate(icons):
        t0 = .8 + i * 1.1
        rise = A.ease(A.seg(t, t0, .7))
        gone = A.ease(A.seg(t, t0 + 1.3, .6))
        if rise <= 0:
            continue
        ix = hx - 60 + i * 70
        iy = 620 - rise * 150 + gone * -120
        op = rise * (1 - gone)
        if op <= 0:
            continue
        if kind == "grad":
            out += (f'<rect x="{ix-10:.0f}" y="{iy-40:.0f}" width="20" height="70" rx="10" fill="#fff"'
                     f' opacity="{op:.2f}" {o(3)}/>'
                     f'<circle cx="{ix:.0f}" cy="{iy+40:.0f}" r="16" fill="{KRAS}" opacity="{op:.2f}"/>')
        elif kind == "cena":
            out += (f'<path d="M{ix-24:.0f},{iy:.0f} h40 l14,16 l-14,16 h-40 Z" fill="{col}"'
                     f' opacity="{op:.2f}" {o(3)}/>'
                     f'<circle cx="{ix-14:.0f}" cy="{iy:.0f}" r="5" fill="#fff" opacity="{op:.2f}"/>')
        else:
            out += (f'<ellipse cx="{ix:.0f}" cy="{iy:.0f}" rx="40" ry="24" fill="{col}" opacity="{op:.2f}"/>'
                     f'<circle cx="{ix+2}" cy="{iy+22:.0f}" r="5" fill="#9fc4d8" opacity="{op*.8:.2f}"/>')
    s += SL(Z_SRED, out)
    s += sneg_letit(t, n=34, seed=21)
    s += vinetka(.42)
    return s


def selskiy_magazin_i_ostanovka(t):
    """Крыльцо магазина с вывеской и остановка рядом — героиня проходит мимо."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t)
    s += SL(Z_DAL, ulica_dal(0, 760, W, t, True, 8))
    mx, my = 300, 700
    rise = A.seg(t, .9, .2)
    fall = A.seg(t, 1.2, .2)
    op_ = .4 * max(0.0, rise - fall)
    shop = (f'<rect x="{mx}" y="{my}" width="420" height="300" fill="url(#dosk)" {o(6)}/>'
            f'<rect x="{mx+40}" y="{my+40}" width="100" height="160" fill="url(#stekl)" opacity=".8" {o(4)}/>')
    shop += dver(mx + 200, my + 60, 150, 220, open_=op_)
    shop += f'<rect x="{mx+20}" y="{my-50}" width="380" height="60" rx="8" fill="url(#zol)" {o(5)}/>'
    shop += (f'<text x="{mx+210}" y="{my-10}" font-family="Georgia,serif" font-size="34" font-weight="700"'
             f' text-anchor="middle" fill="#2a1d0c">Магазин</text>')
    s += SL(Z_SRED, shop)
    ax = 1200
    stop = (f'<path d="M{ax},780 h360 v30 h-360 Z" fill="{ZHELEZ}" {o(5)}/>'
            f'<rect x="{ax+20}" y="810" width="20" height="160" fill="{ZHELEZ}"/>'
            f'<rect x="{ax+320}" y="810" width="20" height="160" fill="{ZHELEZ}"/>')
    s += SL(Z_SRED, stop)
    folks = ""
    for i, fx in enumerate((mx + 120, mx + 330, ax + 90, ax + 260)):
        turn = 6 * A.w(t, 1.5, i * .4) * A.seg(t, 1.0, .5)
        folks += (f'<g transform="rotate({turn:.1f} {fx} 920)">'
                  + siluet(fx, 980, 280, "#1c1a22", 1, False, INEY) + '</g>')
    s += SL(Z_SRED, folks)
    hx = 500 + (t * 110) % 1200
    s += SL(Z_SRED, figura(hx, 1000, 400, t, col="#231f29", kant=SVET))
    dog_x = hx - 110 + 14 * A.w(t, 4.0)
    dog = (f'<ellipse cx="{dog_x:.0f}" cy="1040" rx="46" ry="22" fill="#4a3a2a" {o(3)}/>'
           f'<circle cx="{dog_x+40:.0f}" cy="1020" r="16" fill="#4a3a2a" {o(3)}/>')
    s += SL(Z_SRED, dog)
    s += vinetka(.4)
    return s


def koridor_polikliniki(t):
    """Коридор поликлиники: лампа мигает, дверь кабинета открывается, облако растёт."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#beton)"/>'
    s += polovicy(820)
    flick = .85 if A.blink(t, 2.3, .08) else .2 + .5 * abs(A.w(t, .4))
    s += SL(Z_DAL, f'<rect x="700" y="40" width="520" height="40" rx="10" fill="#eaf6ff" opacity="{flick:.2f}"/>')
    chairs = ""
    for i in range(5):
        cx_ = 120 + i * 330
        chairs += lavka(cx_, 760, 260)
        chairs += siluet(cx_ + 130, 740, 300, "#211f28", 1, False, INEY)
    s += SL(Z_SRED, chairs)
    px = 1700
    s += SL(Z_SRED, siluet(px, 740, 300, "#1e1c26", 1, False, INEY))
    s += SL(Z_SRED, f'<rect x="{px-14}" y="500" width="24" height="40" rx="6" fill="{K}" opacity=".8"/>')
    gr = A.ease(A.seg(t, .8, 5.0))
    s += SL(Z_SRED, f'<ellipse cx="{px+60}" cy="{460-gr*60:.0f}" rx="{40+gr*60:.0f}" ry="{28+gr*40:.0f}"'
                     f' fill="#ffffff" opacity=".7"/>')
    op_ = A.ease(A.seg(t, 2.0, 2.0))
    s += SL(Z_SRED, dver(1420, 660, 180, 300, open_=op_ * .6))
    s += vinetka(.42)
    return s


def otvet_u_podezda(t):
    """У подъезда: героиня улыбается, буханка торчит из сумки, рядом голуби."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t)
    s += SL(Z_DAL, panelka(0, 820, W, t, 5, seed=3))
    s += SL(Z_SRED, dver(760, 640, 220, 340))
    sosx = 1180
    lean = 6 * math.sin(min(1.0, A.seg(t, .8, 1.0)) * math.pi / 2)
    s += SL(Z_SRED, f'<g transform="rotate({lean:.1f} {sosx} 820)">'
                     + figura(sosx, 980, 360, t, col="#272230", kant=SVET, platok=True) + '</g>')
    hx = 820
    tilt = 4 * A.w(t, 2.0)
    s += SL(Z_SRED, f'<g transform="rotate({tilt:.1f} {hx} 980)">'
                     + figura(hx, 1000, 380, t, col="#201c28", kant=ORA) + '</g>')
    bag = f'<path d="M{hx+60},940 q-4,-70 46,-78 q50,8 46,78 Z" fill="url(#derev)" {o(5)}/>'
    bag += karavay(hx + 106, 870, .36, False)
    s += SL(Z_SRED, bag)
    s += SL(Z_SRED, par_izo_rta(hx + 20, 760, t, .2, .8, .4))
    s += SL(Z_SRED, ptica(560, 1040, t, .8, "#8a8f96", .1, "#5b6a78"))
    s += SL(Z_SRED, ptica(640, 1050, t, .7, "#8a8f96", .6, "#5b6a78"))
    s += vinetka(.4)
    return s


def tolpa_sverhu(t):
    """Площадь сверху: плотная толпа шапок и платков шевелится, как каша в котле."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += f'<rect width="{W}" height="{H}" fill="{KAMEN2}"/>'
    rnd1 = random.Random(2)
    cols = ["#1c1a22", "#2a2634", "#3a3240", "#1e2230", "#241e28"]
    pts = []
    for row in range(9):
        for col_i in range(14):
            ox = 60 + col_i * 132 + rnd1.uniform(-20, 20)
            oy = 60 + row * 110 + rnd1.uniform(-16, 16)
            pts.append((ox, oy, rnd1.random(), rnd1.choice(cols)))
    heads = ""
    for ox, oy, ph, col in pts:
        jig = 10 * A.w(t, 1.0 + ph, ph * 3)
        jiy = 6 * A.w(t, 1.3 + ph, ph * 5)
        bump = 1.0 + .12 * max(0.0, A.w(t, .7 + ph, ph * 4))
        heads += f'<ellipse cx="{ox+jig:.0f}" cy="{oy+jiy:.0f}" rx="{50*bump:.0f}" ry="{42*bump:.0f}" fill="{col}" {o(3)}/>'
    s += SL(Z_SRED, heads)
    steam = ""
    for sx, sy in ((300, 200), (900, 160), (1500, 220)):
        steam += dym(sx, sy, t, 4, .3, 260, .3, "#e8eef4", .8)
    s += SL(Z_PERED, steam)
    s += vinetka(.45)
    return s


def sherstyanye_noski_u_batarei(t):
    """Носки тянутся к батарее, кот щурится, пар от чашки на подоконнике."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += f'<rect width="{W}" height="{H}" fill="#d2d8de"/>'
    s += SL(Z_DAL, okno_izby(1400, 220, 300, 400, t, svet=False, moroz=.4))
    bx, by, bw = 120, 820, 480
    bat = f'<rect x="{bx}" y="{by}" width="{bw}" height="140" rx="14" fill="{CHUGUN}" {o(6)}/>'
    for i in range(8):
        bat += f'<rect x="{bx+20+i*58}" y="{by+10}" width="34" height="120" rx="14" fill="{ZHELEZ}" opacity=".85"/>'
    s += SL(Z_SRED, bat + teplo(bx + bw / 2, by + 70, 420, 320, .55))
    legs = ""
    for i, lx_ in enumerate((bx + 200, bx + 340)):
        wig = 6 * A.w(t, 2.4, i * .4)
        legs += (f'<path d="M{lx_},940 q10,-140 0,-280" stroke="{TKAN2}" stroke-width="54"'
                 f' stroke-linecap="round" fill="none"/>'
                 f'<g transform="rotate({wig:.1f} {lx_} 920)">'
                 f'<ellipse cx="{lx_}" cy="920" rx="54" ry="34" fill="{TKAN2}" {o(4)}/>'
                 f'<path d="M{lx_-30},900 q-16,-6 -28,6 M{lx_-10},894 q-10,-10 -20,0"'
                 f' stroke="{TKAN2}" stroke-width="10" fill="none"/></g>')
    s += SL(Z_PERED, legs)
    s += SL(Z_SRED, kot(bx + bw + 140, 980, t, 1.1))
    cx_, cy_ = 1460, 660
    cup = f'<path d="M{cx_-40},{cy_} h80 l-8,40 h-64 Z" fill="url(#krem)" {o(4)}/>'
    s += SL(Z_SRED, cup + par(cx_, cy_ - 10, t, 4, .45, 140, .5))
    s += vinetka(.4)
    return s


def repi_na_palto(t):
    """Человек выходит из толпы — на пальто шевелят колючками сердитые репьи."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, seed=18)
    crowd = ""
    rnd1 = random.Random(9)
    for i in range(10):
        cx_ = i * (W / 9) + rnd1.uniform(-20, 20)
        crowd += siluet(cx_, 740, 220, "#232028", .5, False, "#4a5570")
    s += SL(Z_DAL, crowd)
    glow = .5 + .2 * abs(A.w(t, 2.0))
    door = dver(1480, 560, 220, 360, kruchok=True) + teplo(1590, 760, 200, 160, glow)
    s += SL(Z_SRED, door)
    hx = 500 + (t * 90) % 700
    shiver = 4 * A.w(t, 6.0)
    fig = figura(hx + shiver, 960, 420, t, col="#1c1926", kant=INEY, telogreyka=True)
    s += SL(Z_SRED, fig)
    burrs = ""
    for i in range(4):
        bx_ = hx - 40 + (i % 2) * 60
        byy = 760 + (i // 2) * 70
        ph = i * .5
        burrs += f'<g transform="translate({bx_:.0f},{byy})">'
        for j in range(8):
            a = j * math.pi / 4 + .3 * A.w(t, 1.6, ph + j * .1)
            ex, ey = 22 * math.cos(a), 22 * math.sin(a)
            burrs += f'<line x1="0" y1="0" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{UGOL}" stroke-width="4"/>'
        burrs += (f'<circle r="16" fill="{UGOL}" {o(3)}/>'
                  f'<circle cx="-5" cy="-3" r="2.4" fill="{K}"/><circle cx="5" cy="-3" r="2.4" fill="{K}"/>'
                  f'<path d="M-5,6 q5,5 10,0" stroke="{K}" stroke-width="2" fill="none"/>')
        burrs += '</g>'
    s += SL(Z_SRED, burrs)
    s += sneg_letit(t, n=26, seed=31)
    s += vinetka(.44)
    return s
def nabityy_avtobus(t):
    """Салон переполненного автобуса: иней на окнах, чихание рассыпается зелёными точками по салону."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, teplo(W * .5, 60, 900, 260, .35))
    for i, wx in enumerate((40, 420, 800, 1180, 1560)):
        s += SL(Z_DAL, okno_izby(wx, 70, 300, 230, t, vid=teplo(150, 140, 200, 120, .25), moroz=.85, krest=False))
        s += SL(Z_DAL, inej(wx, 70, 300, t, 10, 11 + i, R=230))
    for i, rx in enumerate((260, 700, 1140, 1580)):
        dx = 14 * A.w(t, 2.2, i * .4)
        s += SL(Z_SRED, f'<line x1="{rx}" y1="330" x2="{rx+dx:.0f}" y2="520" stroke="{ZHELEZ}" stroke-width="10" stroke-linecap="round"/>'
                         f'<circle cx="{rx}" cy="330" r="12" fill="url(#zhel)"/>')
    for i, (px, py, hh, kk) in enumerate([(160, 760, 340, SNEG), (420, 800, 380, INEY), (680, 740, 320, SNEG),
                                           (1000, 820, 400, INEY), (1300, 770, 350, SNEG), (1620, 810, 370, INEY)]):
        s += SL(Z_SRED if i % 2 else Z_PERED, figura(px, py, hh, t, col="#20222b", kant=kk, ph=i * .3, op=1.0))
    t0 = 1.4
    ex, ey = 700, 560
    for i, (tx, ty) in enumerate([(420, 760), (1000, 780), (260, 820), (1300, 740)]):
        k = A.out(A.seg(t, t0 + i * .08, 1.1))
        gx = ex + (tx - ex) * k
        gy = ey + (ty - ey) * k - 90 * k * (1 - k)
        s += SL(Z_PERED, f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="{5+3*(1-k):.1f}" fill="#8fd35a" opacity="{(.3+.7*k)*(1 if k>0 else 0):.2f}"/>')
    s += par_izo_rta(700, 540, t, .1, .7, .4)
    s += vinetka(.4)
    return s


def sumka_na_kryuchke(t):
    """Прихожая: хозяйственная сумка качается на крючке, у двери встают сапоги, за окном далеко шумит рынок."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, doski(0, 0, W, H, step=90, vert=False, grad="dosk"))
    s += SL(Z_DAL, okno_izby(1400, 160, 420, 360, t, vid=ulica_dal(0, 520, 420, t, True, 9), moroz=.3))
    for i, (fx, sp) in enumerate([(1430, .6), (1560, .5), (1680, .7)]):
        k = (t * sp + i * .33) % 1.0
        s += SL(Z_DAL, f'<rect x="{fx+(k-.5)*40:.0f}" y="420" width="10" height="34" rx="3" fill="#2a2a30" opacity=".6"/>')
    s += SL(Z_SRED, dver(120, 260, 260, 560, open_=.12, kruchok=True))
    hx, hy = 520, 300
    s += SL(Z_SRED, f'<circle cx="{hx}" cy="{hy}" r="14" fill="url(#zhel)"/>')
    sway = 10 * A.w(t, 2.6)
    s += SL(Z_SRED, f'<g transform="rotate({sway:.1f} {hx} {hy})">'
                     f'<path d="M{hx-4},{hy} v30" stroke="{ZHELEZ}" stroke-width="6"/>'
                     f'<path d="M{hx-70},{hy+30} q-10,120 20,210 h100 q30,-90 20,-210 Z" fill="{TKAN2}" {o(6)}/>'
                     f'<path d="M{hx-40},{hy+30} q0,-26 40,-26 q40,0 40,26" fill="none" stroke="{TKAN2}" stroke-width="10"/></g>')
    t0 = 1.6
    k = A.out(A.seg(t, t0, 1.0))
    by = 760 + (1 - k) * 180
    s += SL(Z_SRED, f'<g opacity="{.2+.8*k:.2f}" transform="translate(0,{(1-k)*40:.0f})">'
                     f'<ellipse cx="{hx-50}" cy="{by:.0f}" rx="34" ry="18" fill="{CHUGUN}" {o(5)}/>'
                     f'<path d="M{hx-84},{by:.0f} v-120 q0,-20 24,-20 h30 v140 Z" fill="{CHUGUN}" {o(5)}/>'
                     f'<ellipse cx="{hx+30}" cy="{by+6:.0f}" rx="34" ry="18" fill="{CHUGUN}" {o(5)}/>'
                     f'<path d="M{hx-4},{by+6:.0f} v-120 q0,-20 24,-20 h30 v140 Z" fill="{CHUGUN}" {o(5)}/></g>')
    s += par_izo_rta(220, 420, t, .4, .6, .3)
    s += vinetka(.4)
    return s


def gorbushka_na_doske(t):
    """Крупно хлебная доска: горбушка под ножом, крошки подпрыгивают от удара, пар над свежим срезом."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, teplo(960, 500, 760, 420, .3))
    bx, by, bw, bh = 500, 760, 980, 90
    s += SL(Z_SRED, f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="url(#dosk)" {o(7)}/>')
    gx, gy = 880, 700
    s += SL(Z_SRED, f'<path d="M{gx-220},{gy+60} q-30,-140 160,-170 q260,-30 300,110 q20,90 -80,130 q-220,60 -380,-70 Z"'
                     f' fill="{DOSKA}" {o(7)}/>')
    s += SL(Z_SRED, f'<path d="M{gx-150},{gy+40} q140,-110 360,-30" fill="none" stroke="{DOSKA2}" stroke-width="10" opacity=".6"/>')
    s += par(gx + 260, gy - 10, t, 4, .5, 130, .5)
    t0 = 1.0
    cyc = (t - t0) % 1.4 if t >= t0 else 0
    chop = A.ease(1 - abs(cyc / 1.4 - .5) * 2) if t >= t0 else 0
    ky = gy - 260 + chop * 210
    s += SL(Z_PERED, f'<g transform="translate({gx+190},{ky:.0f})">'
                      f'<path d="M-14,0 h200 l40,18 l-40,18 h-200 Z" fill="url(#zhel)" {o(6)}/>'
                      f'<rect x="-50" y="-10" width="40" height="40" rx="6" fill="{BREVNO2}" {o(5)}/>'
                      f'<path d="M20,4 l180,10" stroke="#ffffff" stroke-width="4" opacity=".55"/></g>')
    r = random.Random(7)
    for i in range(8):
        ph = r.random()
        hop = math.sin(t * 3 + ph * 6) if chop > .8 else 0
        cx0 = gx + 160 + r.uniform(-20, 220)
        cy0 = by - 6 - max(0, hop) * 26
        s += SL(Z_PERED, f'<circle cx="{cx0:.0f}" cy="{cy0:.0f}" r="{3+r.random()*3:.1f}" fill="{DOSKA2}"/>')
    s += vinetka(.4)
    return s


def hlebnaya_polka_pod_polotencem(t):
    """Полка с караваями под полотенцем: по счёту вспыхивает каждый, в окне метёт снег над полем до горизонта."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += SL(Z_DAL, okno_izby(1280, 160, 480, 420, t, vid=f'<rect width="480" height="420" fill="url(#nrassv)"/>' + sneg_lezhit(320), moroz=.4))
    s += sneg_letit(t, 30, 21, .5, .8)
    s += SL(Z_SRED, polka(260, 560, 820))
    for i, (kx, ky) in enumerate([(360, 520), (560, 520), (760, 520)]):
        s += SL(Z_SRED, karavay(kx, ky, .85, rushnik=False))
        t0 = 1.0 + i * .7
        gl = A.out(A.seg(t, t0, .4)) * (1 - A.out(A.seg(t, t0 + .5, .5)))
        s += SL(Z_SRED, f'<ellipse cx="{kx}" cy="{ky-40}" rx="90" ry="60" fill="{SVET}" opacity="{.5*gl:.2f}"/>')
    k = A.out(A.seg(t, .2, 1.4))
    ty = 300 + k * 40
    s += SL(Z_PERED, f'<path d="M180,{ty:.0f} h900 l-20,60 q-430,40 -860,0 Z" fill="url(#rush)" {o(6)} opacity="{1-.1*k:.2f}"/>')
    s += SL(Z_PERED, f'<rect x="220" y="{ty+40:.0f}" width="760" height="10" fill="{TKAN}" opacity=".8"/>')
    s += vinetka(.4)
    return s


def karavay_vo_glave_stola(t):
    """Длинный стол: каравай во главе как хозяин, ложки вдоль стола поворачиваются к нему, пар поднимается."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, doski(0, 0, W, 540, step=120, vert=False, grad="dosk"))
    s += SL(Z_SRED, stol(260, 640, 1500, 50, nog=True))
    hx, hy = 960, 560
    s += SL(Z_SRED, karavay(hx, hy, 1.3, rushnik=True))
    s += par(hx + 10, hy - 150, t, 5, .45, 170, .35)
    for i, (lx, ly) in enumerate([(360, 660), (560, 660), (1360, 660), (1560, 660), (460, 700), (1460, 700)]):
        ang0 = -70 if lx < hx else 70
        k = A.ease(A.seg(t, .6 + i * .15, 1.3))
        ang = ang0 * (1 - k)
        s += SL(Z_SRED, f'<g transform="rotate({ang:.1f} {lx} {ly})">'
                         f'<ellipse cx="{lx}" cy="{ly}" rx="46" ry="30" fill="url(#krem)" {o(5)}/>'
                         f'<path d="M{lx},{ly-30} q10,-40 0,-70" stroke="{MED}" stroke-width="10" fill="none" stroke-linecap="round"/></g>')
    sway = 6 * A.w(t, 3.2)
    s += SL(Z_PERED, f'<path d="M{hx-70},{hy+40} q{sway:.0f},80 0,170 h140 q{-sway:.0f},-90 0,-170 Z" fill="url(#rush)" {o(5)} opacity=".9"/>')
    s += vinetka(.4)
    return s


def kroshki_v_ladon(t):
    """Очень крупно: клетчатая клеёнка, крошки катятся к краю и падают в миску."""
    s = f'<rect width="{W}" height="{H}" fill="#cfd9df"/>'
    # клеёнка в клетку во весь кадр
    s += SL(Z_SRED, f'<rect y="120" width="{W}" height="{H-120}" fill="#e8efe2"/>')
    for i in range(14):
        s += SL(Z_SRED, f'<rect x="{i*150-20}" y="120" width="54" height="{H-120}" fill="#bcd3b4" opacity=".55"/>')
    for j in range(7):
        s += SL(Z_SRED, f'<rect y="{150+j*150}" width="{W}" height="54" fill="#bcd3b4" opacity=".55"/>')
    s += SL(Z_SRED, f'<rect y="120" width="{W}" height="26" fill="#8fa98a" opacity=".5"/>')
    s += teplo(520, 420, 760, 520, .45)
    # край стола внизу и глиняная миска под ним
    s += SL(Z_PERED, f'<rect y="900" width="{W}" height="36" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_PERED, f'<path d="M1180,940 q180,150 360,0 Z" fill="url(#glina)" {o(6)}/>')
    s += SL(Z_PERED, f'<ellipse cx="1360" cy="940" rx="180" ry="32" fill="#e0b183" {o(5)}/>')
    # крошки катятся к краю; последняя подпрыгивает
    rnd = random.Random(12)
    for i in range(16):
        y0 = 300 + rnd.random() * 520
        x0 = 120 + rnd.random() * 820
        k = A.ease(A.seg(t, .6 + i * .12, 1.6))
        x = x0 + (1180 - x0) * k
        y = y0 + (900 - y0) * k * k
        r = 9 + rnd.random() * 9
        s += SL(Z_SRED, f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r*.72:.0f}"'
                        f' fill="#c89a5c" {o(3, "#8d6534")} transform="rotate({k*220:.0f} {x:.0f} {y:.0f})"/>')
    kp = A.seg(t, 3.4, 1.5)
    if kp > 0:
        pr = math.sin(math.pi * kp)
        s += SL(Z_SRED, f'<ellipse cx="{1250+90*kp:.0f}" cy="{880-150*pr:.0f}" rx="13" ry="10"'
                        f' fill="#d7a765" {o(3, "#8d6534")}/>')
    # рукав у края кадра — кисть руки не рисуем (его правило 05.11)
    s += SL(Z_PERED, f'<path d="M-40,560 q220,-40 330,30 l-26,150 q-170,70 -304,20 Z"'
                     f' fill="{TKAN2}" {o(6)}/>')
    s += SL(Z_PERED, f'<path d="M250,578 q60,16 60,60" stroke="#dfe9f0" stroke-width="10" fill="none" opacity=".5"/>')
    s += vinetka(.42)
    return s
def dedova_lozhka(t):
    """Дед в профиль смотрит строго, ложка щёлкает мальчика по лбу, мальчик вздрагивает и сдувает пыль с кусочка."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_DAL, teplo(1500, 500, 500, 360, .3))
    dx, dy = 1500, 820
    s += SL(Z_SRED, figura(dx, dy, 460, t, col="#17161c", kant=INEY, profil=True, op=1.0))
    mus = 4 * A.w(t, 1.6)
    s += SL(Z_SRED, f'<path d="M{dx+28},{dy-370} q{20+mus:.0f},6 {38+mus:.0f},-2" fill="none" stroke="#e8e4da" stroke-width="7" stroke-linecap="round" opacity=".8"/>')
    t0 = 1.2
    hit = A.out(A.seg(t, t0, .18)) * (1 - A.out(A.seg(t, t0 + .5, .5)))
    bx, by = 1060, 900
    rec = 10 * hit
    s += SL(Z_SRED, figura(bx + rec, by, 300, t, col="#20222c", kant=SNEG, ph=.4))
    sx, sy = dx - 140, dy - 520
    ang = -40 + 70 * A.out(A.seg(t, t0 - .4, .4))
    s += SL(Z_PERED, f'<g transform="rotate({ang:.1f} {sx} {sy})">'
                      f'<rect x="{sx-6}" y="{sy}" width="12" height="150" rx="6" fill="url(#derev)" {o(5)}/>'
                      f'<ellipse cx="{sx}" cy="{sy+160}" rx="34" ry="46" fill="url(#derev)" {o(5)}/></g>')
    px, py = 1020, 980
    s += SL(Z_PERED, f'<ellipse cx="{px}" cy="{py}" rx="40" ry="20" fill="{DOSKA}" {o(5)}/>')
    t1 = 2.4
    for i in range(6):
        kd = A.out(A.seg(t, t1 + i * .03, .6))
        s += SL(Z_PERED, f'<circle cx="{px-20+i*16+kd*60:.0f}" cy="{py-10-kd*40:.0f}" r="{3*(1-kd)+1:.1f}" fill="#d8cdb0" opacity="{(1-kd)*.7:.2f}"/>')
    s += par_izo_rta(bx, by - 260, t, .2, .6, .4)
    s += vinetka(.4)
    return s


def malchik_s_buhankoy_po_doroge_domoy(t):
    """Мальчик идёт с буханкой в сетке, на каждом шагу отщипывает кусок: у двери подъезда угол уже обкусан."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += panelka(240, 1080, 1500, t, etazh=5, okna_svet=True, seed=9)
    s += SL(Z_DAL, sneg_lezhit(840))
    s += sneg_letit(t, 26, 18, .5, .7)
    s += SL(Z_SRED, dver(1540, 760, 170, 300, open_=.05, kruchok=True))
    bx = 300 + (min(t, 6.0) / 6.0) * 1180
    s += SL(Z_SRED, figura(bx, 960, 360, t, col="#232433", kant=SNEG, ph=.2))
    s += SL(Z_SRED, f'<ellipse cx="{bx:.0f}" cy="908" rx="46" ry="30" fill="{POL2}" {o(5)}/>')
    nx, ny = bx + 60, 1020
    sway = 10 * A.w(t, 2.0)
    s += SL(Z_SRED, f'<g transform="rotate({sway:.1f} {nx:.0f} {ny-60:.0f})">'
                     f'<path d="M{nx-10:.0f},{ny-120:.0f} v120" stroke="{ZHELEZ}" stroke-width="5"/>'
                     f'<path d="M{nx-38:.0f},{ny-30:.0f} q-10,40 10,70 q28,22 56,0 q20,-30 10,-70 Z" fill="{DOSKA}" {o(4)} opacity=".9"/>'
                     f'<path d="M{nx-40:.0f},{ny-28:.0f} l80,70 M{nx+40:.0f},{ny-28:.0f} l-80,70" stroke="{ZHELEZ}" stroke-width="2" opacity=".5"/></g>')
    kf = min(1.0, t / 6.0)
    for i in range(3):
        bk = A.out(A.seg(t, i * 1.8 + .4, .3))
        s += SL(Z_PERED, f'<circle cx="{nx-6+i*10:.0f}" cy="{ny-10:.0f}" r="{9*(1-bk)*(1-.3*kf):.1f}" fill="#eee4cc" opacity="{1-bk:.2f}"/>')
    s += vinetka(.4)
    return s


def lomot_s_maslom_i_saharom(t):
    """Двор, лавочка: толстый ломоть с маслом, сахар сыплется и блестит, чужой рукав тянется сбоку."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, pleten(0, 760, 820, 170, 7))
    s += sneg_letit(t, 20, 15, .4, .6)
    s += SL(Z_SRED, lavka(120, 820, 620))
    bx, by = 420, 760
    s += SL(Z_SRED, f'<rect x="{bx-150}" y="{by-70}" width="300" height="130" rx="14" fill="{KREM}" {o(7)}/>')
    melt = min(1.0, t / 5.0)
    s += SL(Z_SRED, f'<path d="M{bx-140},{by-66} q150,{-30+40*melt:.0f} 280,0 q-10,{30*melt:.0f} -280,{20*melt:.0f} Z" fill="{SVET}" opacity=".85"/>')
    r = random.Random(5)
    for i in range(16):
        ph = r.random()
        p = (t * .7 + ph) % 1.0
        sxp = bx - 120 + r.uniform(0, 240)
        syp = by - 110 + p * 110
        bl = .4 + .6 * abs(A.w(t, 1.3 + ph, ph))
        s += SL(Z_PERED, f'<circle cx="{sxp:.0f}" cy="{syp:.0f}" r="{2+2*(1-p):.1f}" fill="#fffdf2" opacity="{bl*(1-p*.4):.2f}"/>')
    t0 = 1.6
    k = A.out(A.seg(t, t0, 1.4))
    rx = 760 - k * 180
    s += SL(Z_PERED, f'<path d="M820,980 q{-80-k*40:.0f},{-60-k*30:.0f} {rx-820:.0f},{-140-k*60:.0f}'
                      f' l40,30 q{80+k*40:.0f},{40+k*20:.0f} 90,{130-k*20:.0f} Z" fill="#2b2e38" {o(6)}/>')
    s += vinetka(.4)
    return s


def grenki_v_moloke(t):
    """Миска молока: ломтик окунается и всплывает, на сковороде ломтики румянятся, вилка переворачивает крайний."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, teplo(400, 500, 500, 320, .3))
    mx, my = 300, 760
    s += SL(Z_SRED, f'<ellipse cx="{mx}" cy="{my}" rx="190" ry="60" fill="url(#krem)" {o(7)}/>')
    s += SL(Z_SRED, f'<ellipse cx="{mx}" cy="{my-10}" rx="170" ry="46" fill="#fbfaf2" opacity=".95"/>')
    dip = A.ease((A.w(t, 2.4) + 1) / 2)
    ly = my - 40 - dip * 160
    s += SL(Z_SRED, f'<rect x="{mx-70}" y="{ly:.0f}" width="140" height="60" rx="8" fill="{KREM}" {o(6)} opacity="{.6+.4*dip:.2f}"/>')
    px, py = 680, 820
    s += SL(Z_SRED, f'<ellipse cx="{px}" cy="{py}" rx="150" ry="40" fill="{CHUGUN}" {o(7)}/>')
    for i, (fx, ph) in enumerate([(-80, .1), (0, .4), (80, .7)]):
        br = min(1.0, t / 6.0 + ph * .1)
        col = f'rgb({240-60*br:.0f},{210-90*br:.0f},{150-70*br:.0f})'
        s += SL(Z_SRED, f'<ellipse cx="{px+fx}" cy="{py-10}" rx="46" ry="26" fill="{col}"/>')
    t0 = 2.0
    ang = -50 * A.out(A.seg(t, t0, .5)) * (1 - A.out(A.seg(t, t0 + .6, .5)))
    s += SL(Z_PERED, f'<g transform="rotate({ang:.1f} {px+80} {py-40})">'
                      f'<rect x="{px+74}" y="{py-140}" width="12" height="110" fill="url(#zhel)" {o(4)}/>'
                      f'<path d="M{px+68},{py-140} l0,-20 M{px+80},{py-140} l0,-24 M{px+92},{py-140} l0,-20"'
                      f' stroke="url(#zhel)" stroke-width="7" stroke-linecap="round"/></g>')
    s += par(mx, my - 80, t, 3, .4, 110, .4)
    s += vinetka(.4)
    return s


def korki_v_koryte(t):
    """Двор у хлева: из ведра в корыто сыплют размоченные корки, куры клюют, поросёнок хрюкает и толкается боком."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, pleten(0, 820, 1920, 190, 11))
    s += sneg_letit(t, 24, 20, .4, .7)
    cx, cy = 960, 900
    s += SL(Z_SRED, f'<path d="M{cx-220},{cy} q0,70 220,70 q220,0 220,-70 q0,-40 -220,-40 q-220,0 -220,40 Z" fill="url(#derev)" {o(7)}/>')
    bx, by = cx - 20, cy - 260
    tilt = 30 * A.ease(A.seg(t, .3, .6)) * (1 - .3 * A.ease(A.seg(t, 2.6, .5)))
    s += SL(Z_SRED, f'<g transform="rotate({tilt:.1f} {bx} {by})">'
                     f'<path d="M{bx-50},{by} q-10,90 10,120 h80 q20,-30 10,-120 Z" fill="{ZHELEZ}" {o(5)}/></g>')
    r = random.Random(9)
    for i in range(10):
        ph = r.random()
        p = (t * .9 + ph) % 1.0
        kx = bx + (cx - bx) * p + r.uniform(-20, 20)
        ky = by + (cy - by) * p - 160 * p * (1 - p)
        s += SL(Z_SRED, f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="10" ry="7" fill="{DOSKA2}" opacity="{.9-.2*p:.2f}"/>')
    s += SL(Z_SRED, kura(cx - 140, cy + 60, t, .9, 0))
    s += SL(Z_SRED, kura(cx + 170, cy + 50, t, .85, .5))
    pig_x = cx - 20 + 40 * A.w(t, 1.8)
    s += SL(Z_SRED, f'<g transform="translate({pig_x:.0f},0)">'
                     f'<ellipse cx="{cx}" cy="{cy+140}" rx="110" ry="64" fill="#e0a6ad" {o(6)}/>'
                     f'<circle cx="{cx+90}" cy="{cy+110}" r="40" fill="#e0a6ad" {o(5)}/>'
                     f'<ellipse cx="{cx+118}" cy="{cy+112}" rx="14" ry="10" fill="#b57078"/>'
                     f'<path d="M{cx+70},{cy+80} l20,-24 l20,10 Z" fill="#cf8f98" {o(3)}/></g>')
    s += vinetka(.4)
    return s


def buhanka_na_kuhonnoy_doske(t):
    """Корыто превращается в кухонную доску: от чёрствой буханки разбегаются три дорожки крошек, нож ложится рядом."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_DAL, teplo(960, 420, 700, 300, .25))
    bx, by = 960, 760
    s += SL(Z_SRED, f'<rect x="{bx-340}" y="{by-30}" width="680" height="90" rx="16" fill="url(#dosk)" {o(7)}/>')
    shake = 3 * A.w(t, 9.0)
    s += SL(Z_SRED, f'<g transform="translate({shake:.1f},0)">'
                     f'<ellipse cx="{bx}" cy="{by-70}" rx="170" ry="80" fill="{DOSKA}" {o(7)}/>'
                     f'<path d="M{bx-140},{by-90} q140,-50 280,0" fill="none" stroke="{DOSKA2}" stroke-width="8" opacity=".6"/></g>')
    for i, (ddx, ddy) in enumerate([(-1, -.3), (0, 1), (1, -.3)]):
        grow = A.out(A.seg(t, .4 + i * .3, 2.0))
        ln = 420 * grow
        r = random.Random(20 + i)
        for j in range(8):
            jp = j / 8.0
            px = bx + ddx * ln * jp + r.uniform(-14, 14)
            py = by + ddy * ln * jp * .5 + r.uniform(-10, 10)
            s += SL(Z_SRED, f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{4+r.random()*3:.1f}" fill="{DOSKA2}" opacity="{.8*grow:.2f}"/>')
    k = A.out(A.seg(t, 1.6, 1.0))
    nx = bx + 260
    ny = by - 90 + (1 - k) * (-200)
    s += SL(Z_PERED, f'<g transform="translate({nx:.0f},{ny:.0f}) rotate({20*(1-k):.0f})">'
                      f'<path d="M-14,0 h190 l36,16 l-36,16 h-190 Z" fill="url(#zhel)" {o(6)}/>'
                      f'<rect x="-50" y="-8" width="40" height="40" rx="6" fill="{BREVNO2}" {o(5)}/></g>')
    s += vinetka(.4)
    return s


def tri_puti_cherstvogo_hleba(t):
    """Три дорожки от чёрствого хлеба: противень едет в духовку, ломтик румянится на сковороде, синица клюёт крошки на подоконнике."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += SL(Z_DAL, teplo(400, 900, 260, 160, .4))
    ox, oy = 180, 860
    s += SL(Z_SRED, f'<rect x="{ox}" y="{oy}" width="260" height="200" rx="12" fill="{CHUGUN}" {o(7)}/>')
    s += SL(Z_SRED, f'<rect x="{ox+16}" y="{oy+16}" width="228" height="168" rx="8" fill="#1a1a1a" opacity=".9"/>')
    slide = A.out(A.seg(t, .3, 1.6))
    trx = ox + 300 - slide * 260
    s += SL(Z_SRED, f'<rect x="{trx:.0f}" y="{oy+150:.0f}" width="150" height="20" rx="4" fill="{ZHELEZ}" {o(4)} opacity="{1-slide*.4:.2f}"/>')
    r = random.Random(13)
    for i in range(6):
        s += SL(Z_SRED, f'<ellipse cx="{trx+20+i*22:.0f}" cy="{oy+146:.0f}" rx="12" ry="8" fill="{DOSKA}" opacity="{1-slide*.3:.2f}"/>')
    px, py = 560, 940
    s += SL(Z_SRED, f'<ellipse cx="{px}" cy="{py}" rx="120" ry="34" fill="{CHUGUN}" {o(6)}/>')
    br = min(1.0, t / 6.0)
    col = f'rgb({238-50*br:.0f},{205-80*br:.0f},{150-60*br:.0f})'
    s += SL(Z_SRED, f'<ellipse cx="{px}" cy="{py-10}" rx="90" ry="24" fill="{col}"/>')
    wx, wy = 740, 760
    s += SL(Z_SRED, f'<rect x="{wx}" y="{wy}" width="80" height="20" rx="4" fill="url(#derev)" {o(5)}/>')
    for i in range(6):
        p = (t * .6 + i * .15) % 1.0
        s += SL(Z_SRED, f'<circle cx="{wx+10+i*10:.0f}" cy="{wy-6-6*math.sin(p*math.pi):.0f}" r="3" fill="{DOSKA2}"/>')
    land = A.out(A.seg(t, 1.0, 1.0))
    s += SL(Z_PERED, ptica(wx + 40, wy - 14 - (1 - land) * 120, t, .8, KRAS, 0))
    s += vinetka(.4)
    return s
def pribrannaya_gornica(t):
    """Прибранная горница: скатерть на столе расправляется, веник встаёт в угол, зайчик от снега гуляет по потолку."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, brevna(0, 0, W, H * .58, hh=84))
    zx = 760 + 160 * A.w(t, 8.0, .12)
    s += SL(Z_NEBO, f'<ellipse cx="{zx:.0f}" cy="104" rx="150" ry="48" fill="#eef7ff"'
                     f' opacity="{.16+.12*abs(A.w(t,2.3)):.2f}"/>')
    s += SL(Z_DAL, okno_izby(1240, 180, 250, 300, t, svet=True, moroz=.35)
            + polka(300, 230, 340) + krynka(360, 268, .64) + krynka(456, 274, .54))
    s += SL(Z_SRED, polovicy(760))
    p_ven = A.out(A.seg(t, 1.6, 1.3))
    ang = 24 * (1 - p_ven)
    s += SL(Z_SRED, f'<g transform="translate(150,878) rotate({-ang:.1f})">'
            f'<rect x="-10" y="-198" width="20" height="196" rx="8" fill="url(#derev)" {o(5)}/>'
            + ''.join(f'<path d="M0,-6 l{(i-4)*9:.0f},104" stroke="#9c7049" stroke-width="7"'
                      f' stroke-linecap="round"/>' for i in range(9)) + '</g>')
    p_sk = A.ease(A.seg(t, .8, 1.7))
    amp = 24 * (1 - p_sk)
    s += SL(Z_SRED, f'<g transform="translate(980,700)">{stol(-210, 0, 420)}</g>')
    s += SL(Z_SRED, f'<path d="M770,662 q110,{amp:.0f} 220,0 l18,40 q-128,{amp*.6:.0f} -256,0 Z"'
                     f' fill="url(#krem)" {o(4)}/>')
    s += SL(Z_SRED, karavay(890, 650, .6))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.42)
    return s


def polovik_na_snegu(t):
    """Двор: половик на снегу выбивают лозиной — пыль встаёт облаком, снег под ним сереет."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, zvezdy=False))
    s += SL(Z_DAL, ulica_dal(0, 540, W, t))
    s += SL(Z_DAL, pleten(100, 700, 860))
    s += SL(Z_SRED, sneg_lezhit(700, 30))
    p_ser = A.ease(A.seg(t, 1.0, 3.2))
    s += SL(Z_SRED, f'<ellipse cx="960" cy="760" rx="230" ry="56" fill="#9aa6ae"'
                     f' opacity="{.5*p_ser:.2f}"/>')
    s += SL(Z_SRED, f'<rect x="760" y="556" width="400" height="220" rx="12" fill="url(#tkan)" {o(7)}/>'
            + ''.join(f'<line x1="770" y1="{600+i*48}" x2="1150" y2="{600+i*48}"'
                      f' stroke="{TKAN2}" stroke-width="9" opacity=".7"/>' for i in range(4)))
    sw = 36 * A.w(t, .7)
    s += SL(Z_SRED, f'<g transform="rotate({sw:.1f} 1190 520)">'
            f'<rect x="1180" y="280" width="20" height="300" rx="8" fill="url(#derev)" {o(5)}/></g>')
    s += SL(Z_LETIT, dym(930, 630, t, 6, .5, 220, .42, "#cfd6de", 1.2))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.4)
    return s


def taburetka_v_masterskoy(t):
    """Мастерская: киянка вбивает четвёртую ножку, стружка летит, табуретка встаёт на четыре ножки."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, doski(0, 0, W, H * .62, step=90, vert=True, grad="dosk"))
    s += SL(Z_DAL, f'<rect x="120" y="130" width="70" height="320" rx="8" fill="url(#zhel)" {o(5)}/>'
            + f'<rect x="1700" y="150" width="60" height="280" rx="8" fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, f'<rect x="420" y="700" width="900" height="60" rx="10" fill="url(#derev)" {o(7)}/>'
            + f'<rect x="460" y="760" width="40" height="220" fill="url(#derev)" {o(5)}/>'
            + f'<rect x="1240" y="760" width="40" height="220" fill="url(#derev)" {o(5)}/>')
    p = A.out(A.seg(t, 3.2, 1.6))
    ang = 180 * (1 - p)
    yy = 660 - 220 * p
    stul = (f'<rect x="-110" y="-20" width="220" height="40" rx="10" fill="url(#derev)" {o(6)}/>'
            + ''.join(f'<rect x="{lx-14}" y="20" width="28" height="180" fill="url(#derev)" {o(5)}/>'
                      for lx in (-80, 80)))
    p4 = A.seg(t, .8, 2.2)
    stul += (f'<rect x="-14" y="{20+180*(1-p4):.0f}" width="28" height="{180*p4:.0f}"'
             f' fill="url(#derev)" {o(5)}/>')
    s += SL(Z_SRED, f'<g transform="translate(900,{yy:.0f}) rotate({ang:.1f})">{stul}</g>')
    if t < 3.4:
        mw = 18 * A.w(t, .45)
        s += SL(Z_SRED, f'<g transform="translate(900,{yy-220:.0f}) rotate({mw:.1f})">'
                f'<rect x="-14" y="-170" width="28" height="140" rx="6" fill="url(#derev)" {o(5)}/>'
                f'<rect x="-40" y="-40" width="80" height="60" rx="14" fill="{CHUGUN}" {o(6)}/></g>')
    frag = ""
    for i in range(7):
        p_f = (t * .9 + i * .14) % 1.0
        fx = 860 + i * 24 + 60 * A.w(t, 1.6, i * .3)
        fy = (yy - 60) + p_f * 160
        frag += (f'<path d="M{fx:.0f},{fy:.0f} q16,-10 28,6 q-10,14 -28,8 Z" fill="url(#dosk)"'
                 f' opacity="{(1-p_f)*.85:.2f}"/>')
    s += SL(Z_LETIT, frag)
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.4)
    return s


def lnyanoe_polotno_na_stane(t):
    """Ткацкий стан у окна: нить вспыхивает золотом, бёрдо стучит, полотно прибывает — на миг проступает корона."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, brevna(0, 0, 900, H * .6, hh=80))
    s += SL(Z_NEBO, okno_izby(560, 140, 220, 280, t, svet=True, moroz=.2))
    s += SL(Z_DAL, utvar_izby(0, 640, 760, t, seed=9))
    fx, fw, fh = 160, 420, 560
    pf = A.ease(A.seg(t, .5, 7.0))
    gold = 3.0 <= t <= 4.2
    tcol = ZOL if gold else "#e7d7b4"
    frame = (f'<rect x="{fx}" y="160" width="40" height="560" fill="url(#derev)" {o(6)}/>'
             f'<rect x="{fx+fw-40}" y="160" width="40" height="560" fill="url(#derev)" {o(6)}/>'
             f'<rect x="{fx}" y="160" width="{fw}" height="40" fill="url(#derev)" {o(6)}/>')
    for i in range(10):
        tx = fx + 50 + i * (fw - 100) / 9
        frame += (f'<line x1="{tx:.0f}" y1="200" x2="{tx:.0f}" y2="{200+fh*pf:.0f}"'
                  f' stroke="{tcol}" stroke-width="4" opacity=".9"/>')
    sw = 14 * A.w(t, .9)
    frame += (f'<rect x="{fx+20}" y="{200+fh*pf-10+sw:.0f}" width="{fw-40}" height="20" rx="6"'
              f' fill="url(#derev)" {o(5)}/>'
              f'<rect x="{fx+40}" y="200" width="{fw-80}" height="{fh*pf:.0f}" rx="4"'
              f' fill="url(#rush)" opacity=".85"/>')
    if gold:
        pc = A.ease(min((t - 3.0) / .6, (4.2 - t) / .6, 1.0))
        frame += (f'<g opacity="{pc:.2f}" transform="translate({fx+fw/2:.0f},{260+fh*pf*.4:.0f})">'
                  f'<path d="M-30,10 L-30,-14 L-14,0 L0,-26 L14,0 L30,-14 L30,10 Z" fill="{ZOL}" {o(4)}/></g>')
    s += SL(Z_SRED, frame)
    s += SL(Z_PERED, figura(fx + fw + 40, 760, 360, t, "#262230", "#f0d8a8", False, .3, False))
    s += vinetka(.4)
    return s


def zybka_pod_polotnom(t):
    """Зыбка на шесте: полотно ложится, тучка с глазом улетает — позже полотно становится лоскутным одеялом, зыбка кроваткой."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, brevna(0, 0, W, H * .55, hh=80))
    s += SL(Z_NEBO, okno_izby(1240, 150, 240, 260, t, svet=True, moroz=.3))
    cx, cy = 820, 560
    sw = 5 * A.w(t, 2.4)
    p_cl = A.ease(A.seg(t, 1.1, 1.3))
    p_kv = A.ease(A.seg(t, 6.5, 2.2))
    grp = (f'<path d="M{cx-180},{cy-220} q180,-60 360,0" fill="none"'
           f' stroke="url(#derev)" stroke-width="12"/>'
           f'<path d="M{cx-150},{cy-200} L{cx-120},{cy+40} q150,46 300,0 L{cx+150},{cy-200} Z"'
           f' fill="url(#derev)" {o(6)}/>')
    if p_kv < .02:
        grp += (f'<rect x="{cx-150}" y="{cy-190}" width="300" height="{160*p_cl:.0f}" rx="18"'
                f' fill="url(#rush)" opacity="{p_cl:.2f}" {o(5)}/>'
                f'<rect x="{cx-150}" y="{cy-190}" width="300" height="20" fill="{TKAN}" opacity="{p_cl:.2f}"/>')
    else:
        for row in range(2):
            for col in range(4):
                cxx = cx - 150 + col * 75
                cyy = cy - 190 + row * 80
                col_ = (TKAN, ZEL2, TKAN2, MED)[(row + col) % 4]
                grp += (f'<rect x="{cxx}" y="{cyy}" width="72" height="76" fill="{col_}"'
                        f' opacity="{p_kv:.2f}" {o(3)}/>')
    s += SL(Z_NEBO, f'<line x1="{cx}" y1="0" x2="{cx}" y2="{cy}" stroke="url(#derev)" stroke-width="18"/>')
    s += SL(Z_SRED, f'<g transform="rotate({sw:.1f} {cx} {cy-220})">{grp}</g>')
    if t < 3.4:
        p_t = A.ease(A.seg(t, 1.4, 1.8))
        tx_, ty_ = 1500 - p_t * 500, 220 - p_t * 60
        s += SL(Z_DAL, f'<g opacity="{1-p_t:.2f}" transform="translate({tx_:.0f},{ty_:.0f})">'
                f'<ellipse cx="0" cy="0" rx="90" ry="52" fill="#dfe8f0" {o(4)}/>'
                f'<ellipse cx="-50" cy="12" rx="54" ry="34" fill="#dfe8f0" {o(3)}/>'
                f'<circle cx="24" cy="-8" r="7" fill="{K}"/><circle cx="50" cy="-6" r="7" fill="{K}"/>'
                f'<path d="M14,8 q16,10 32,0" stroke="{K}" stroke-width="4" fill="none"/></g>')
    if p_kv > .1:
        s += SL(Z_SRED, teplo(cx, cy - 60, 300, 220, .45 * p_kv))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.4)
    return s


def babushkin_shkaf_s_belem(t):
    """Бабушкин шкаф: дверца открывается, зеркало ловит блик, мешочек с травой качается — позже свёрток разворачивается в одеяло на кресле, и кот тут же забирается на него."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, doski(0, 0, W, H * .62, step=100, vert=True, grad="dosk"))
    sx, sy, sw_, sh_ = 220, 120, 420, 640
    p_dv = A.out(A.seg(t, 1.0, 1.4))
    shkaf = (f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh_}" rx="12" fill="url(#derev)" {o(7)}/>'
             + dver(sx + 20, sy + 20, sw_ * .42, sh_ - 40, open_=p_dv, kruchok=True))
    blx = sx + 20 + sw_ * .42 * (1 - p_dv * .3)
    sweep = (t * .5) % 1.0
    shkaf += (f'<g opacity="{.5*p_dv:.2f}"><path d="M{blx:.0f},{sy+40+sweep*500:.0f}'
              f' l70,-70 l20,20 l-70,70 Z" fill="#ffffff"/></g>')
    for i in range(3):
        shkaf += (f'<rect x="{sx+sw_*.5:.0f}" y="{sy+60+i*90:.0f}" width="{sw_*.42:.0f}" height="70"'
                  f' rx="8" fill="url(#rush)" opacity="{p_dv:.2f}" {o(4)}/>')
    ph = 6 * A.w(t, 2.0)
    shkaf += (f'<g opacity="{p_dv:.2f}" transform="rotate({ph:.1f} {sx+sw_*.72:.0f} {sy+70:.0f})">'
              f'<path d="M{sx+sw_*.72-20:.0f},{sy+70:.0f} q-6,30 20,46 q26,-16 20,-46 Z"'
              f' fill="#6f8c4a" {o(3)}/></g>')
    bx, by = sx + sw_ * .7, sy + 70
    p_sv = A.ease(A.seg(t, 6.0, 1.6))
    chx, chy = 1420, 820
    bwx = bx + (chx - bx) * p_sv
    bwy = by + (chy - by) * p_sv
    bw_ = 90 + 260 * p_sv
    bh_ = 70 + 70 * p_sv
    shkaf += (f'<rect x="{bwx-bw_/2:.0f}" y="{bwy-bh_/2:.0f}" width="{bw_:.0f}" height="{bh_:.0f}"'
              f' rx="{20*(1-p_sv)+10:.0f}" fill="url(#rush)" {o(5)}/>')
    s += SL(Z_SRED, shkaf)
    s += SL(Z_SRED, f'<path d="M{chx-70},{chy+60} v-140 q0,-50 70,-50 h60 q70,0 70,50 v140 Z"'
            f' fill="url(#derev)" {o(6)}/>')
    if p_sv > .6:
        s += SL(Z_PERED, kot(chx, chy - 30, t, .9))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.4)
    return s


def loskutnoe_odeyalo(t):
    """Лоскутное одеяло разворачивается, швы поблёскивают, мягкий блик скользит по лоскутам — по одному подсвечиваются, и над каждым всплывает вещь."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="url(#teplo)" opacity=".12"/>')
    cols, rows = 5, 4
    cw, ch = 140, 150
    x0, y0 = 90, 160
    cols_list = (TKAN, ZEL2, TKAN2, MED, ZOL, "#6b4428")
    highlights = {4: (3.6, 5.0), 9: (5.1, 6.4), 14: (6.5, 7.8)}
    garments = (4, 9, 14)
    quilt = ""
    seams = ""
    for ridx in range(rows):
        p_row = A.ease(A.seg(t, .6 + ridx * .35, 1.0))
        for cidx in range(cols):
            idx = ridx * cols + cidx
            cx, cy = x0 + cidx * cw, y0 + ridx * ch
            bright = 1.0
            if idx in highlights:
                t0, t1 = highlights[idx]
                if t0 <= t <= t1:
                    bright = 1.0 + .5 * A.ease(min((t - t0) / .3, (t1 - t) / .3, 1.0))
            col_ = cols_list[idx % len(cols_list)]
            s_y = cy + ch * (1 - p_row) * .5
            quilt += (f'<rect x="{cx}" y="{s_y:.0f}" width="{cw-6}" height="{ch-6}" fill="{col_}"'
                      f' opacity="{p_row:.2f}" {o(3)}/>')
            if bright > 1.0:
                quilt += (f'<rect x="{cx}" y="{s_y:.0f}" width="{cw-6}" height="{ch-6}"'
                          f' fill="#ffffff" opacity="{(bright-1)*.6:.2f}"/>')
            if idx in garments and idx in highlights:
                t0, t1 = highlights[idx]
                if t0 <= t <= t1 + .6:
                    pg = A.ease(min((t - t0) / .4, (t1 + .6 - t) / .4, 1.0))
                    quilt += (f'<ellipse cx="{cx+cw/2-3:.0f}" cy="{s_y-60:.0f}" rx="52" ry="68"'
                              f' fill="#efe3c8" opacity="{pg*.85:.2f}" {o(3)}/>')
            seams += (f'<line x1="{cx}" y1="{s_y:.0f}" x2="{cx+cw-6}" y2="{s_y:.0f}"'
                      f' stroke="#f4dba0" stroke-width="2"'
                      f' opacity="{.4*abs(A.w(t,1.7,idx*.1))*p_row:.2f}"/>')
    glide = (t * .18) % 1.0
    gx = x0 + glide * cols * cw
    gy = y0 + ((t * .11) % 1.0) * rows * ch
    s += SL(Z_SRED, quilt + seams)
    s += SL(Z_SRED, f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="90" ry="70" fill="#ffffff" opacity=".10"/>')
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.38)
    return s


def detskoe_odeyalce_po_rukam(t):
    """Ряд детей передаёт байковое одеяльце по росту — у кроватки под ним сменяются младенцы, мишки на одеяльце бледнеют."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, doski(0, 0, W, H * .6, step=110, vert=True, grad="dosk"))
    if t < 5.0:
        heights = (300, 260, 210, 160, 120)
        xs = (260, 560, 860, 1140, 1380)
        kids = ""
        for h_, x in zip(heights, xs):
            kids += figura(x, 860, h_, t, "#262230", "#f0d8a8", False, x * .01, False)
        seg = min(int(t / 1.0), 3)
        frac = A.ease((t / 1.0) % 1.0) if t < 4.0 else 1.0
        x0b, x1b = xs[seg], xs[min(seg + 1, 4)]
        bx = x0b + (x1b - x0b) * frac
        hb = heights[min(seg + 1, 4)]
        fringe = 4 * A.w(t, 1.6)
        s += SL(Z_SRED, kids)
        s += SL(Z_PERED, f'<g transform="translate({bx:.0f},{860-hb*.7:.0f}) rotate({fringe:.1f})">'
                f'<rect x="-70" y="-50" width="140" height="100" rx="14" fill="url(#krem)" {o(5)}/>'
                + ''.join(f'<circle cx="{dx}" cy="{dy}" r="10" fill="{MED}" opacity=".7"/>'
                          for dx, dy in ((-30, -10), (0, 10), (30, -10))) + '</g>')
    else:
        s += SL(Z_SRED, f'<rect x="700" y="680" width="520" height="220" rx="24" fill="url(#derev)" {o(7)}/>')
        breathe = 1.0 + .02 * A.w(t, 1.3)
        fade = min((t - 5.0) / 6.0, .75)
        s += SL(Z_SRED, f'<g transform="translate(960,700) scale({breathe:.3f})">'
                f'<rect x="-230" y="-40" width="460" height="130" rx="18" fill="url(#krem)" {o(6)}/>'
                + ''.join(f'<circle cx="{dx}" cy="{dy}" r="12" fill="{MED}" opacity="{.75*(1-fade):.2f}"/>'
                          for dx, dy in ((-130, 0), (0, 20), (130, 0))) + '</g>')
        baby = int(t * .8) % 4
        s += SL(Z_SRED, f'<ellipse cx="960" cy="690" rx="{44+baby*4}" ry="34" fill="#f0d8c0" {o(4)}/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def stol_s_yagodnym_pitem(t):
    """Стол у окна: питьё льётся в кружку, пар идёт от пирога, на миг встают миски мёрзлых ягод в инее."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, brevna(0, 0, 820, H * .55, hh=80))
    s += SL(Z_NEBO, okno_izby(520, 130, 230, 260, t, svet=True, moroz=.3))
    s += SL(Z_SRED, f'<g transform="translate(140,760)">{stol(-60, 0, 620)}</g>')
    s += SL(Z_SRED, krynka(220, 720, .9, "url(#glina)"))
    if (t * .5) % 2.0 < .5:
        s += SL(Z_SRED, f'<path d="M248,690 q30,30 10,70" stroke="{TKAN}" stroke-width="6" fill="none"/>')
    lvl = min((t * .1) % 1.0 + .2, 1.0)
    s += SL(Z_SRED, f'<rect x="300" y="{770-40*lvl:.0f}" width="60" height="{40*lvl:.0f}" fill="{TKAN}"'
            f' opacity=".85"/><ellipse cx="330" cy="728" rx="34" ry="14" fill="none" {o(5)}/>')
    s += SL(Z_SRED, karavay(520, 700, .8, True))
    s += SL(Z_LETIT, par(520, 630, t, 4, .45, 140, .5, 1.0))
    p_mi = A.ease(A.seg(t, 2.0, 1.4))
    if p_mi > .02:
        for bx in (420, 660):
            s += SL(Z_SRED, f'<g opacity="{p_mi:.2f}" transform="translate({bx},740)">'
                    f'<ellipse cx="0" cy="20" rx="70" ry="24" fill="url(#glina)" {o(5)}/>'
                    f'<ellipse cx="0" cy="0" rx="60" ry="26" fill="{KRAS}" {o(4)}/></g>')
            s += SL(Z_LETIT, dym(bx, 710, t, 4, .3, 90, .3 * p_mi, "#eaf6ff", .7))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.4)
    return s


def molochnaya_struzhka(t):
    """Нож строгает мороженое молоко, стружка завивается и тает на стопке блинов, от блинов идёт пар."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, doski(0, 0, W, H * .6, step=100, vert=True, grad="dosk"))
    s += SL(Z_SRED, f'<ellipse cx="560" cy="700" rx="260" ry="90" fill="url(#sneg)" {o(7)}/>')
    sw = 10 * A.w(t, 1.1)
    s += SL(Z_SRED, f'<g transform="translate(700,680) rotate({14+sw:.1f})">'
            f'<rect x="-20" y="-10" width="220" height="24" rx="6" fill="url(#zhel)" {o(5)}/>'
            f'<rect x="200" y="-16" width="120" height="36" rx="8" fill="url(#derev)" {o(5)}/></g>')
    curl = (t * 1.1) % 1.0
    cx = 620 + curl * 420
    cy = 690 - 40 * math.sin(curl * math.pi)
    s += SL(Z_SRED, f'<path d="M{cx:.0f},{cy:.0f} q30,-20 10,-46 q-24,-20 -4,-50"'
            f' fill="none" stroke="#f5fbff" stroke-width="10" stroke-linecap="round"'
            f' opacity="{1-curl*.3:.2f}"/>')
    s += SL(Z_SRED, f'<g transform="translate(1180,760)">'
            + ''.join(f'<ellipse cx="0" cy="{-i*18}" rx="130" ry="26" fill="url(#krem)" {o(4)}/>'
                      for i in range(4)) + '</g>')
    melt = A.ease(A.seg(t, 2.0, 2.0))
    s += SL(Z_SRED, f'<ellipse cx="1180" cy="696" rx="{70*(1-melt):.0f}" ry="{20*(1-melt):.0f}"'
            f' fill="#f5fbff" opacity="{1-melt:.2f}"/>')
    s += SL(Z_LETIT, par(1180, 700, t, 4, .5, 150, .45, 1.1))
    s += SL(Z_SRED, f'<ellipse cx="1480" cy="780" rx="60" ry="24" fill="url(#glina)" {o(4)}/>'
            f'<ellipse cx="1480" cy="770" rx="48" ry="16" fill="{KRAS}" opacity=".9"/>')
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.4)
    return s


def holodnye_seni_s_miskami(t):
    """Холодные сени: иней на брёвнах искрит, пар идёт изо рта, крышка погреба слегка поскрипывает."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, brevna(0, 0, W, H * .6, hh=80))
    s += SL(Z_NEBO, inej(60, 40, W - 120, t, 26, 3))
    s += SL(Z_DAL, lavka(220, 700, 360))
    s += SL(Z_DAL, f'<g transform="translate(260,660)">'
            + ''.join(f'<ellipse cx="{i*120}" cy="0" rx="58" ry="22" fill="url(#glina)" {o(4)}/>'
                      f'<ellipse cx="{i*120}" cy="-6" rx="48" ry="16" fill="{KRAS}" opacity=".9"/>'
                      for i in range(2)) + '</g>')
    s += SL(Z_DAL, polka(900, 400, 420)
            + f'<ellipse cx="980" cy="440" rx="60" ry="22" fill="url(#sneg)" {o(5)}/>'
            + f'<ellipse cx="1120" cy="440" rx="60" ry="22" fill="url(#sneg)" {o(5)}/>')
    ang = 3 * A.w(t, .8)
    s += SL(Z_SRED, f'<g transform="rotate({ang:.1f} 1500 820)">'
            f'<rect x="1400" y="800" width="200" height="40" rx="6" fill="url(#dosk)" {o(6)}/></g>')
    s += SL(Z_PERED, figura(760, 940, 380, t, "#1b1822", "#cfe4f5", False, .2, False))
    s += SL(Z_PERED, par_izo_rta(800, 820, t, .1))
    s += vinetka(.46)
    return s


def balkon_i_morozilka(t):
    """Дверь сеней растворяется в белую дверцу морозилки: за окном — снежный балкон с кастрюлей в сугробе."""
    p_tr = A.ease(A.seg(t, .3, 3.0))
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    seni = (SL(Z_NEBO, brevna(0, 0, W, H * .6, hh=84))
            + SL(Z_SRED, f'<g opacity="{1-p_tr:.2f}">'
                 + dver(760, 300, 300, 500, open_=0.0, kruchok=True) + '</g>'))
    p_open = A.out(A.seg(t, 2.6, 1.4))
    kitchen = (SL(Z_NEBO, f'<rect width="{W}" height="{H*.6:.0f}" fill="url(#beton)"/>')
               + SL(Z_DAL, okno_izby(1240, 150, 300, 280, t, krest=True,
                    vid=(f'<rect width="300" height="280" fill="#dfe8f0"/>'
                         f'<ellipse cx="150" cy="200" rx="60" ry="22" fill="#eef5fa"/>'
                         f'<ellipse cx="150" cy="190" rx="48" ry="26" fill="{CHUGUN}"/>')))
               + SL(Z_SRED, f'<g opacity="{p_tr:.2f}">'
                    f'<rect x="760" y="300" width="300" height="500" rx="20" fill="#eef4f8" {o(7)}/>'
                    f'<g transform="translate(900,560) scale({1-p_open*.1:.2f},1)">'
                    f'<rect x="-10" y="-200" width="20" height="400" fill="#c7dbe8"/></g></g>'))
    s += seni + kitchen
    s += SL(Z_DAL, inej(1170, 170, 100, t, 8, 5))
    s += SL(Z_LETIT, dym(910, 500, t, 5, .35, 200, .4 * p_open, "#eaf6ff", 1.0))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s


def yaschik_morozilki_s_yagodami(t):
    """Крупно выдвинутый ящик морозилки: иней на пакетах, бумажки шевелятся, ягоды перекатываются — один пакет сам поднимается из ящика."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H*.5:.0f}" fill="url(#beton)"/>')
    s += SL(Z_DAL, f'<rect x="260" y="500" width="1400" height="420" rx="22" fill="#e9eef2" {o(8)}/>')
    packs = (("Клюква, август", KRAS, 540, 620),
             ("Брусника, август", "#5a2430", 980, 620))
    inner = ""
    for i, (label, col, px, py) in enumerate(packs):
        lift = A.out(A.seg(t, 2.0 + i * .3, 1.4)) if i == 0 else 0.0
        py_ = py - 160 * lift
        wob = 3 * A.w(t, 1.4, i * .4)
        inner += f'<g transform="translate({px},{py_:.0f}) rotate({wob:.1f})">'
        inner += f'<rect x="-150" y="-110" width="300" height="220" rx="24" fill="#eaf4fb" opacity=".88" {o(5)}/>'
        r = random.Random(i + 1)
        for _ in range(10):
            bx = r.uniform(-110, 110)
            by = r.uniform(-70, 70) + 10 * A.w(t, 1.0 + r.random(), r.random())
            inner += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="14" fill="{col}" {o(2)}/>'
        inner += (f'<rect x="-70" y="-150" width="140" height="48" rx="6" fill="#ffffff" {o(4)}/>'
                  f'<text x="0" y="-122" font-size="20" text-anchor="middle" fill="{K}"'
                  f' font-family="Georgia,serif">{label}</text>')
        inner += '</g>'
    s += SL(Z_SRED, inner)
    s += SL(Z_NEBO, inej(300, 520, 1300, t, 30, 6))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.4)
    return s
def setka_za_fortochkoy(t):
    """Форточка пятиэтажки с сеткой продуктов — вид с улицы, наезд и отъезд."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, zvezdy=False)
    s += panelka(60, H - 40, W - 120, t, etazh=6, seed=9)
    wx, wy, ww, wh = 760, 300, 360, 430
    s += SL(Z_SRED, okno_izby(wx, wy, ww, wh, t, moroz=.35, svet=False))
    fx, fy = wx + ww * .72, wy + 30
    sway = 4 * A.w(t, 1.6, .1)
    netg = (f'<g transform="rotate({sway:.1f} {fx:.0f} {fy:.0f})">'
            f'<line x1="{fx:.0f}" y1="{fy:.0f}" x2="{fx:.0f}" y2="{fy+150:.0f}" stroke="#cdd8e2" stroke-width="2" opacity=".6"/>'
            + "".join(f'<line x1="{fx-26+i*13:.0f}" y1="{fy+40:.0f}" x2="{fx-18+i*13:.0f}" y2="{fy+150:.0f}"'
                      f' stroke="#cdd8e2" stroke-width="2" opacity=".55"/>' for i in range(5))
            + f'<rect x="{fx-30:.0f}" y="{fy+50:.0f}" width="60" height="70" rx="8" fill="url(#rush)" opacity=".9"/>'
            + _sneg_lezhit_polosa(fx - 30, fy + 44, 60, 14)
            + f'<rect x="{fx-16:.0f}" y="{fy+126:.0f}" width="22" height="46" rx="6" fill="url(#stekl)" opacity=".8"/>'
            + f'<ellipse cx="{fx-5:.0f}" cy="{fy+126:.0f}" rx="12" ry="7" fill="{ZHELEZ}"/>'
            + '</g>')
    s += SL(Z_SRED, netg)
    s += SL(Z_SRED, inej(wx + 10, wy + 10, ww - 20, t, 10, 4, R=ww - 20))
    for ex in (240, 1260):
        s += SL(Z_DAL, okno_izby(ex, 420, 150, 180, t, moroz=.5, svet=(ex == 1260)))
        s += SL(Z_DAL, f'<rect x="{ex+60:.0f}" y="460" width="28" height="36" rx="5" fill="url(#rush)" opacity=".8"/>')
    s += vinetka(.4)
    return s


def klyukva_v_sahare(t):
    """Блюдце клюквы в сахаре — ребёнок пробует и морщится от кислого."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, zvezdy=False)
    s += kvartira_veschi(40, 900, 700, t, seed=4)
    bx, by = 420, 760
    s += SL(Z_SRED, ten(bx, by + 10, 150, 26, .4))
    s += SL(Z_SRED, f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="150" ry="36" fill="url(#krem)" {o(6)}/>')
    r = random.Random(8)
    berries = "".join(f'<circle cx="{bx+r.uniform(-120,120):.0f}" cy="{by-8+r.uniform(-14,14):.0f}" r="9"'
                       f' fill="{KRAS}" {o(2)}/>' for _ in range(20))
    s += SL(Z_SRED, berries)
    s += SL(Z_SRED, inej(bx - 120, by - 22, 240, t, 16, 6, col="#fff8ea", R=28))
    ring = A.seg(t, 1.0, .15) * (1 - A.seg(t, 1.3, .6))
    s += SL(Z_SRED, f'<ellipse cx="{bx-40:.0f}" cy="{by-4:.0f}" rx="{60+ring*40:.0f}" ry="{14+ring*8:.0f}"'
                     f' fill="none" stroke="#ffffff" stroke-width="3" opacity="{ring*.6:.2f}"/>')
    s += SL(Z_SRED, f'<g transform="rotate(-18 {bx-10} {by-20})">'
                     f'<ellipse cx="{bx-10:.0f}" cy="{by-20:.0f}" rx="16" ry="44" fill="url(#zhel)" {o(3)}/></g>')
    shiver = A.seg(t, 1.6, .25) * (1 - A.seg(t, 2.6, 1.2))
    shx = 6 * shiver * A.w(t, 9.0)
    s += SL(Z_SRED, f'<g transform="translate({shx:.1f},{-shiver*6:.1f})">'
                     + figura(300, 940, 460, t, col="#2a3040", kant="#cfe4f5", ph=.3) + '</g>')
    s += vinetka(.42)
    return s


def mamin_mors_u_krovati(t):
    """Ребёнок в подушках, мать несёт кружку морса — кислый, красный, горячий."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, seed=2)
    s += kvartira_veschi(1200, 940, 680, t, seed=7)
    s += SL(Z_SRED, f'<rect x="120" y="760" width="520" height="220" rx="40" fill="{TKAN2}" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="260" cy="770" rx="110" ry="60" fill="{KREM}" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="440" cy="770" rx="110" ry="60" fill="{KREM}" {o(5)}/>')
    sh = 4 * A.w(t, 2.2, .1)
    s += SL(Z_SRED, f'<g transform="translate({sh:.1f},0)">'
                     + figura(360, 860, 300, t, col="#8a2f33", kant="#f2c9b0", ph=.4) + '</g>')
    s += SL(Z_SRED, f'<rect x="300" y="700" width="140" height="70" rx="20" fill="#5c2730" opacity=".9"/>')
    s += SL(Z_SRED, figura(760, 980, 520, t, col="#243049", kant="#cfe4f5", platok=True, telogreyka=True))
    mx, my = 860, 760
    s += SL(Z_SRED, f'<rect x="{mx-28:.0f}" y="{my:.0f}" width="56" height="60" rx="10" fill="{KRAS}" {o(5)}/>')
    s += SL(Z_SRED, par(mx, my, t, n=4, op=.6, R=160))
    s += SL(Z_SRED, teplo(mx, my - 20, 180, 150, .7))
    s += SL(Z_SRED, f'<rect x="150" y="980" width="90" height="16" fill="url(#derev)" {o(4)}/>'
                     f'<rect x="186" y="920" width="10" height="56" rx="5" fill="#eef4f8" {o(3)}/>'
                     f'<rect x="188" y="{960-10*abs(A.w(t,3.0)):.0f}" width="6"'
                     f' height="{10+10*abs(A.w(t,3.0)):.0f}" fill="{KRAS}"/>')
    k = A.seg(t, 1.5, .5) * (1 - A.seg(t, 2.6, 1.3))
    s += SL(Z_SRED, f'<ellipse cx="360" cy="760" rx="{40+k*14:.0f}" ry="18" fill="none"'
                     f' stroke="#f2c9b0" stroke-width="3" opacity="{k*.5:.2f}"/>')
    s += vinetka(.46)
    return s


def mors_v_kastryulke(t):
    """Кухня: толкушка мнёт клюкву, из чайника льётся кипяток, сверху полотенце."""
    s = f'<rect width="{W}" height="{H}" fill="#7d6a58"/>'
    s += SL(Z_DAL, doski(-20, -20, W + 40, 760, 96, False))
    s += SL(Z_DAL, f'<rect width="{W}" height="{H}" fill="#2e2418" opacity=".28"/>')
    # окно с инеем слева, за ним синий вечер
    vid = f'<rect width="360" height="300" fill="#4a5a78"/>{_sneg_lezhit(210, 12, "#dbe7f4")}'
    s += SL(Z_DAL, okno_izby(90, 150, 360, 300, t, vid, .30, False, True))
    s += SL(Z_DAL, morozny_uzor(96, 156, 348, 288, t, .45))
    s += SL(Z_DAL, polka(1480, 330, 380))
    s += SL(Z_DAL, krynka(1560, 330, .85))
    s += SL(Z_DAL, f'<rect x="1700" y="250" width="110" height="80" rx="8" fill="url(#krem)" {o(5)}/>')
    s += teplo(960, 600, 880, 600, .62)
    # стол
    s += SL(Z_SRED, stol(360, 700, 1300, 40))
    s += SL(Z_SRED, polovicy(980))
    # кастрюлька с клюквой, толкушка мнёт
    tol = 54 * abs(A.w(t, 1.1))
    s += SL(Z_SRED, f'<path d="M760,560 h420 l-34,170 h-352 Z" fill="url(#zhel)" {o(6)}/>')
    s += SL(Z_SRED, f'<ellipse cx="970" cy="560" rx="212" ry="40" fill="#8f969e" {o(5)}/>')
    s += SL(Z_SRED, f'<ellipse cx="970" cy="566" rx="180" ry="30" fill="{KRAS}" opacity=".9"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<circle cx="{860+i*38:.0f}" cy="{560+8*A.w(t,1.1,i*.3):.0f}" r="13"'
                        f' fill="#e2563a" {o(2,"#8f2418")}/>')
    s += SL(Z_SRED, f'<g transform="translate(0,{-tol:.0f})">'
                    f'<rect x="950" y="300" width="40" height="230" rx="14" fill="url(#derev)" {o(5)}/>'
                    f'<rect x="896" y="516" width="148" height="46" rx="14" fill="url(#derev)" {o(5)}/></g>')
    # чайник льёт кипяток
    kv = A.seg(t, 2.2, 2.0)
    s += SL(Z_SRED, f'<g transform="translate(1340,470) rotate({-26*A.ease(kv):.0f} -60 90)">'
                    f'<path d="M-110,0 h190 q30,0 30,34 v76 q0,34 -30,34 h-190 q-30,0 -30,-34 v-76 q0,-34 30,-34 Z"'
                    f' fill="url(#chug)" {o(6)}/>'
                    f'<path d="M-140,30 q-56,36 -36,92" stroke="url(#chug)" stroke-width="22" fill="none"/>'
                    f'<path d="M-10,0 q40,-54 92,-6" stroke="#2e2b2a" stroke-width="16" fill="none"/></g>')
    if kv > .12:
        s += SL(Z_SRED, f'<path d="M1176,588 q-40,60 -74,112" stroke="#dff0fa" stroke-width="12"'
                        f' fill="none" opacity=".75"/>')
        s += par(1110, 560, t, 5, .5, 200, .5)
    s += par(970, 520, t, 5, .6, 240, .45)
    # полотенце накрывает крышку
    kp = A.ease(A.seg(t, 5.2, 1.3))
    s += SL(Z_SRED, f'<g transform="translate(0,{-240+240*kp:.0f})">'
                    f'<rect x="830" y="470" width="280" height="54" rx="12" fill="url(#rush)" {o(5)}/>'
                    f'<path d="M830,524 h280 l-18,40 h-244 Z" fill="#e2d3ae" {o(4)}/></g>')
    s += SL(Z_PERED, _utvar_pekarni(300, 980, 420, t, 9))
    s += vinetka(.46)
    return s
def kruzhka_nad_batareey(t):
    """Кружка морса на подоконнике ярче греет, чем батарея под ней."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, seed=5)
    s += panelka(1100, H - 60, 760, t, etazh=5, seed=12)
    wx, wy, ww, wh = 660, 220, 560, 560
    melt = A.seg(t, 1.0, 3.0)
    s += SL(Z_SRED, okno_izby(wx, wy, ww, wh, t, moroz=max(0.0, .65 * (1 - melt)), svet=False))
    rx, ry = wx + 60, wy + wh + 40
    s += SL(Z_SRED, f'<rect x="{rx:.0f}" y="{ry:.0f}" width="440" height="80" rx="10" fill="url(#zhel)" {o(6)}/>')
    s += SL(Z_SRED, "".join(f'<line x1="{rx+30+i*70:.0f}" y1="{ry+8:.0f}" x2="{rx+30+i*70:.0f}" y2="{ry+72:.0f}"'
                             f' stroke="{ZHELEZ}" stroke-width="6"/>' for i in range(6)))
    rglow = .5 + .1 * abs(A.w(t, 2.0))
    s += SL(Z_SRED, teplo(rx + 220, ry + 40, 260, 90, rglow * .4))
    mx, my = wx + ww * .55, wy + wh * .42
    s += SL(Z_SRED, f'<rect x="{mx-30:.0f}" y="{my:.0f}" width="60" height="64" rx="10" fill="{KRAS}" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M{mx+30:.0f},{my+16:.0f} q26,6 26,24 q0,18 -26,22" fill="none" stroke="{ZHELEZ}" stroke-width="8"/>')
    pulse = .7 + .3 * abs(A.w(t, 2.6, .2))
    s += SL(Z_SRED, teplo(mx, my - 10, 260 + 40 * pulse, 220 + 30 * pulse, .7))
    s += SL(Z_SRED, par(mx, my - 10, t, n=4, op=.55, R=170))
    s += vinetka(.46)
    return s


def kasha_prohozhemu_u_vorot(t):
    """Ворота: хозяйка подаёт кашу прохожему; тот уходит, и за ним до дома бежит золотая дорожка."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, seed=9)
    s += SL(Z_DAL, izba_snaruzhi(1180, H - 40, 640, t, svet=True, truba=True, seed=6))
    s += SL(Z_DAL, pleten(60, H - 120, 1760, kolya=14))
    gx = 420
    s += SL(Z_SRED, f'<rect x="{gx-16:.0f}" y="{H-620:.0f}" width="32" height="500" fill="url(#derev)" {o(6)}/>')
    s += SL(Z_SRED, figura(gx - 90, H - 120, 420, t, col="#2a3040", kant="#cfe4f5", platok=True, telogreyka=True))
    walk = A.ease(A.seg(t, 2.2, 3.2))
    px = gx + 90 + walk * 700
    s += SL(Z_SRED, figura(px, H - 120, 440, t, col="#3a3228", kant="#e8d8b8", telogreyka=True))
    if walk < .97:
        bx = (gx + 30) + (px - gx - 30) * min(1.0, walk * 1.3)
        by = H - 320
        s += SL(Z_SRED, f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="38" ry="18" fill="url(#zhel)" {o(4)}/>')
        s += SL(Z_SRED, par(bx, by - 16, t, n=3, op=.5, R=90))
    trail = A.ease(A.seg(t, 2.6, 3.6))
    if trail > .01:
        d = f'M{px:.0f},{H-80} Q{(px+gx)/2:.0f},{H-40} {gx:.0f},{H-80}'
        s += SL(Z_SRED, f'<path d="{d}" fill="none" stroke="{ZOL}" stroke-width="16" stroke-linecap="round"'
                         f' stroke-dasharray="1400" stroke-dashoffset="{1400*(1-trail):.0f}" opacity=".85"/>')
    wave = .5 + .3 * abs(A.w(t, 2.4))
    s += SL(Z_SRED, dym(1500, H - 460, t, n=5, sp=.22, R=260, op=.4 * wave))
    s += vinetka(.42)
    return s


def stuk_v_sosedkinu_dver(t):
    """Лестничная площадка: тарелка под полотенцем, стук в дверь, соседка открывает."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, seed=11, zvezdy=False)
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BETON2}" opacity=".5"/>')
    s += SL(Z_DAL, f'<rect x="0" y="900" width="{W}" height="180" fill="{KAMEN2}"/>')
    dx, dy, dw, dh = 760, 220, 420, 760
    ring = 0.0
    for i in range(3):
        t0 = .5 + i * .45
        ring = max(ring, A.seg(t, t0, .12) * (1 - A.seg(t, t0 + .12, .35)))
    open_ = A.ease(A.seg(t, 2.1, 1.3))
    s += SL(Z_SRED, dver(dx, dy, dw, dh, open_=open_, kruchok=True))
    s += SL(Z_SRED, f'<circle cx="{dx+dw*.82:.0f}" cy="{dy+dh*.5:.0f}" r="{30+ring*50:.0f}" fill="none"'
                     f' stroke="#e8e0cf" stroke-width="4" opacity="{ring*.6:.2f}"/>')
    if open_ > .1:
        s += SL(Z_SRED, f'<rect x="{dx:.0f}" y="{dy:.0f}" width="{dw*.35:.0f}" height="{dh:.0f}" fill="{SVET}"'
                         f' opacity="{open_*.35:.2f}"/>')
        s += SL(Z_SRED, figura(dx + dw * .4, dy + dh - 20, dh * .74, t, col="#5a4a3c", kant="#f2e6c8",
                                op=min(1.0, open_ * 1.6)))
    px, py = 420, dy + dh - 40
    s += SL(Z_SRED, figura(px, py, dh * .86, t, col="#243049", kant="#cfe4f5", platok=True, telogreyka=True, profil=True))
    s += SL(Z_SRED, f'<rect x="{px-48:.0f}" y="{py-520:.0f}" width="96" height="20" rx="8" fill="url(#rush)" opacity=".9"/>')
    s += SL(Z_SRED, par(px, py - 540, t, n=3, op=.5, R=90))
    s += SL(Z_SRED, par_izo_rta(px + 40, py - 540, t, .1, .7, .4))
    s += vinetka(.46)
    return s


def ozimoe_pole(t):
    """Серое поле с озимыми до горизонта, старик у межи — смена главы «Погода по приметам»."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, zvezdy=False)
    s += oblaka(t, y=120, n=6, seed=14, op=.55, col="#aab3bd", sp=16.0)
    horizon = 560
    s += SL(Z_DAL, f'<rect x="0" y="{horizon}" width="{W}" height="{H-horizon}" fill="{SERO}"/>')
    r = random.Random(21)
    rows = ""
    for row in range(10):
        ry = horizon + row * 48
        n = 26 - row
        for i in range(n):
            rx = (i / n) * W + r.uniform(-14, 14)
            sway = 10 * A.w(t, 2.0 + row * .05, (rx / W) + row * .07)
            rows += f'<path d="M{rx:.0f},{ry:.0f} q{sway:.0f},-26 0,-40" fill="none" stroke="{TRAVA}" stroke-width="4" opacity="{.4+.4*(row/10):.2f}"/>'
    s += SL(Z_SRED, rows)
    ox = 1500
    s += SL(Z_SRED, figura(ox, horizon + 70, 300, t, col="#20242e", kant="#cfe4f5", telogreyka=True))
    lean = 3 * A.w(t, 3.0, .3)
    s += SL(Z_SRED, f'<g transform="rotate({lean:.1f} {ox+55} {horizon+60})">'
                     f'<line x1="{ox+40:.0f}" y1="{horizon+30:.0f}" x2="{ox+70:.0f}" y2="{horizon+90:.0f}"'
                     f' stroke="url(#derev)" stroke-width="7"/></g>')
    s += vinetka(.4)
    return s


def vzglyad_iz_seney(t):
    """Дверь сеней приоткрыта на ладонь: прищуренный глаз хозяина — и дверь закрывается."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, seed=17)
    s += SL(Z_DAL, f'<rect x="0" y="560" width="{W}" height="520" fill="{KAMEN2}"/>')
    close = A.ease(A.seg(t, 3.0, 1.4))
    op_ = .16 * (1 - close)
    dx, dy, dw, dh = 700, 200, 520, 760
    s += SL(Z_SRED, dver(dx, dy, dw, dh, open_=op_, kruchok=True, cepochka=True))
    gapx = dx + dw * (1 - op_ * .55)
    gapw = max(2, dw * op_ * .55)
    if gapw > 3:
        s += SL(Z_SRED, f'<clipPath id="seni_gap"><rect x="{gapx:.0f}" y="{dy+dh*.32:.0f}" width="{gapw:.0f}" height="{dh*.2:.0f}"/></clipPath>')
        squint = .4 + .3 * abs(A.w(t, 1.6, .2))
        s += SL(Z_SRED, f'<g clip-path="url(#seni_gap)">'
                         f'<rect x="{gapx-40:.0f}" y="{dy+dh*.3:.0f}" width="120" height="{dh*.26:.0f}" fill="#0c0c0e"/>'
                         f'<ellipse cx="{gapx:.0f}" cy="{dy+dh*.42:.0f}" rx="22" ry="{12*squint:.0f}" fill="#e8dcc8"/>'
                         f'<circle cx="{gapx:.0f}" cy="{dy+dh*.42:.0f}" r="7" fill="{K}"/>'
                         f'<path d="M{gapx-20:.0f},{dy+dh*.52:.0f} q20,20 50,6" stroke="#4a3b2c" stroke-width="10" fill="none"/>'
                         f'</g>')
        s += SL(Z_SRED, par_izo_rta(gapx + 10, dy + dh * .5, t, .2, .5, .35))
    s += vinetka(.48)
    return s


def dvor_pod_rastuschimi_sugrobami(t):
    """Двор бело от снега: сугробы растут выше забора, тропинка к крыльцу сужается."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, zvezdy=False)
    s += izba_snaruzhi(1240, 760, 560, t, svet=True, truba=True, seed=8)
    grow = A.ease(A.seg(t, .6, 4.0))
    fence_y = 700
    s += SL(Z_DAL, pleten(40, fence_y, 1840, h_=160, kolya=16))
    drift_h = 40 + grow * 170
    s += SL(Z_DAL, _sneg_lezhit_polosa(0, fence_y - drift_h * .4, W, drift_h))
    s += sneg_lezhit(fence_y + 60)
    trench_w = 180 - grow * 110
    tx0, ty0 = 300, fence_y + 70
    s += SL(Z_SRED, f'<path d="M{tx0-trench_w/2:.0f},{H:.0f} L{tx0-trench_w*.3:.0f},{ty0:.0f}'
                     f' L{tx0+trench_w*.3:.0f},{ty0:.0f} L{tx0+trench_w/2:.0f},{H:.0f} Z" fill="{POL2}" opacity=".5"/>')
    s += sneg_letit(t, n=50, seed=19, op=.75)
    s += vinetka(.42)
    return s


def yasnaya_i_pasmurnaya_polovina(t):
    """Кадр разделён пополам: слева солнце и сосульки, справа хмурое небо и капель."""
    s = f'<rect width="{W/2:.0f}" height="{H}" fill="url(#nden)"/>'
    s += f'<rect x="{W/2:.0f}" width="{W/2:.0f}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_DAL, ulica_dal(0, 760, W / 2, t, zima=True, seed=22))
    s += SL(Z_DAL, f'<rect x="{W/2:.0f}" y="560" width="{W/2:.0f}" height="520" fill="{BETON}"/>')
    sunx, suny = 260, 220
    sunpulse = .8 + .2 * abs(A.w(t, 3.0))
    s += SL(Z_SRED, teplo(sunx, suny, 220 * sunpulse, 220 * sunpulse, .55))
    s += SL(Z_SRED, strekha(60, 560, 760, t, n=5, svet=True))
    s += SL(Z_SRED, dym(360, 520, t, n=5, sp=.3, R=320, op=.4, wide=.5))
    r = random.Random(27)
    drips = ""
    for i in range(6):
        dxp = W / 2 + 60 + i * 120 + r.uniform(-10, 10)
        p = (t * .5 + i * .17) % 1.0
        drips += f'<ellipse cx="{dxp:.0f}" cy="{620+p*160:.0f}" rx="6" ry="9" fill="#dff0fa" opacity="{1-p:.2f}"/>'
    s += SL(Z_SRED, drips)
    s += SL(Z_SRED, dym(W / 2 + 500, 520, t, n=5, sp=.26, R=260, op=.35, wide=1.6))
    r2 = random.Random(31)
    flakes = ""
    for i in range(24):
        fx = W / 2 + r2.uniform(0, W / 2)
        fp = (t * .12 + r2.uniform(0, 1)) % 1.0
        flakes += f'<circle cx="{fx+20*A.w(t,4.0,i*.1):.0f}" cy="{fp*H:.0f}" r="4" fill="#ffffff"' \
                  f' opacity="{.5+.4*abs(A.w(t,2.0,i*.2)):.2f}"/>'
    s += SL(Z_LETIT, flakes)
    s += vinetka(.4)
    return s


def sad_v_inee(t):
    """Яблоневый сад в инее: ветки белые, облака задевают верхушки — первые хлопья."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, seed=33)
    s += oblaka(t, y=160, n=5, seed=34, op=.6, col="#dfe6ef", sp=14.0)
    r = random.Random(40)
    trees = ""
    for i in range(3):
        tx = 120 + i * 260
        th = 360 + r.uniform(-20, 20)
        sway = 5 * A.w(t, 2.4 + i * .2, i * .3)
        trees += (f'<g transform="translate({sway:.1f},0)">'
                  f'<path d="M{tx:.0f},720 v{-th:.0f}" stroke="url(#derev)" stroke-width="20"/>'
                  f'<path d="M{tx:.0f},{720-th:.0f} q-70,-10 -110,-80 M{tx:.0f},{720-th:.0f} q70,-10 110,-80"'
                  f' fill="none" stroke="url(#derev)" stroke-width="14"/>'
                  f'<ellipse cx="{tx:.0f}" cy="{720-th-60:.0f}" rx="150" ry="110" fill="#eef4fa" opacity=".88"/>'
                  + inej(tx - 140, 720 - th - 150, 280, t, 20, 12 + i, R=160) + '</g>')
    s += SL(Z_SRED, trees)
    flake_on = A.seg(t, 1.6, 1.2)
    if flake_on > .01:
        r2 = random.Random(41)
        fl = ""
        for i in range(int(18 * flake_on)):
            fx = r2.uniform(0, W)
            fp = (t * .15 + r2.uniform(0, 1)) % 1.0
            fl += f'<circle cx="{fx+20*A.w(t,3.5,i*.1):.0f}" cy="{fp*H*.7:.0f}" r="4" fill="#ffffff"' \
                  f' opacity="{flake_on*.7:.2f}"/>'
        s += SL(Z_LETIT, fl)
    s += oblaka(t, y=220, n=2, seed=44, op=.4, col="#c8d4e2", sp=8.0)
    s += vinetka(.44)
    return s


def okno_u_kotorogo_zapominayut_den(t):
    """У окна фигура в халате; на стекле морозом проступает и тает слово «февраль»."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, seed=50)
    wx, wy, ww, wh = 560, 160, 800, 700
    r3 = random.Random(53)
    vidsnow = "".join(f'<circle cx="{r3.uniform(0,ww):.0f}" cy="{((r3.uniform(0,1)+t*.15)%1.0)*wh:.0f}" r="3"'
                       f' fill="#ffffff" opacity=".5"/>' for _ in range(16))
    s += SL(Z_DAL, okno_izby(wx, wy, ww, wh, t, moroz=.2, svet=False, vid=vidsnow))
    nod = 2 * A.w(t, 2.0, .2)
    s += SL(Z_SRED, f'<g transform="rotate({nod:.1f} {wx+ww*.5:.0f} {wy+wh-40:.0f})">'
                     + figura(wx + ww * .5, wy + wh + 40, 560, t, col="#4a3b2c", kant="#e8d8b8", telogreyka=True) + '</g>')
    appear = A.seg(t, 1.6, 1.0)
    fade = A.seg(t, 3.2, 1.3)
    k = max(0.0, appear - fade)
    if k > .01:
        s += SL(Z_SRED, f'<text x="{wx+ww*.5:.0f}" y="{wy+wh*.42:.0f}" text-anchor="middle"'
                         f' font-family="Georgia, serif" font-size="92" fill="#eaf6ff"'
                         f' opacity="{k*.85:.2f}" stroke="#ffffff" stroke-width="1" letter-spacing="6">февраль</text>')
        s += SL(Z_SRED, morozny_uzor(wx + ww * .2, wy + wh * .2, ww * .6, wh * .3, t, op=k * .3))
    s += sneg_letit(t, n=20, seed=52, op=.5)
    s += vinetka(.46)
    return s
def okoshko_s_poloskoy_neba(t):
    """Городское окно: узкая полоска неба между двух домов, облако и голубь на карнизе."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    gap0, gap1 = 740, 1150
    s += SL(Z_NEBO, oblaka(t, y=210, n=2, seed=21, op=.65, sp=18.0))
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{gap0}" height="{H}" fill="#242b38"/>'
                   f'<rect x="{gap1}" y="0" width="{W-gap1}" height="{H}" fill="#1c222e"/>')
    rnd = random.Random(31)
    for wx in (40, gap1 + 60):
        for r_ in range(3):
            for c_ in range(2):
                ox, oy = wx + 40 + c_ * 140, 120 + r_ * 220
                on = rnd.random() < .4
                s += (f'<rect x="{ox}" y="{oy}" width="90" height="120" rx="4"'
                      f' fill="{SVET if on else "#394459"}" opacity="{.8 if on else 1:.2f}" {o(5,"#131821")}/>')
    s += SL(Z_SRED, f'<rect x="{gap0-16}" y="600" width="{gap1-gap0+32}" height="30" rx="6" fill="url(#dosk)" {o(4)}/>')
    sadka = A.out(A.seg(t, 1.0, 1.3))
    by = 598 - 150 * (1 - sadka)
    s += SL(Z_SRED, ptica(gap0 + 200, by, max(0.0, t - 1.3), 1.05, col="#aeb6bf", seryj="#70788a"))
    s += morozny_uzor(gap0 - 40, 60, gap1 - gap0 + 80, H - 160, t, .28)
    s += SL(Z_PERED, zanaveska(gap0 - 70, 10, 460, 140, t=t, sgn=1))
    s += SL(Z_PERED, zanaveska(gap1 + 70, 10, 460, 140, t=t, sgn=-1))
    s += ramka_pp("oba")
    s += vinetka(.42)
    return s


def listok_kalendarya_s_karandashom_na(t):
    """Крупно листок отрывного календаря, карандаш на нитке выводит слово «снег»."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="url(#dosk)" opacity=".55"/>')
    s += holodny_svet(1500, 260, 380, 300, .35)
    lx, ly, lw, lh = 560, 230, 760, 620
    s += ten(lx + lw * .55, ly + lh + 30, lw * .55, 30, .4)
    s += f'<rect x="{lx-14}" y="{ly-14}" width="{lw+28}" height="{lh+28}" rx="10" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="4" fill="url(#krem)" {o(5)}/>'
    s += f'<rect x="{lx}" y="{ly}" width="{lw}" height="56" fill="{TKAN}" opacity=".88"/>'
    s += f'<text x="{lx+lw/2:.0f}" y="{ly+40}" font-size="34" fill="{KREM}" text-anchor="middle" font-family="Georgia">{DEN} {MESYAC}</text>'
    pish = A.seg(t, .8, 3.2)
    s += f'<path d="M{lx+90},{ly+300} q{lw*.25:.0f},{-28*pish:.0f} {lw*.5:.0f},0 q{lw*.18:.0f},{20*pish:.0f} {lw*.34:.0f},{-6*pish:.0f}"' \
         f' fill="none" stroke="{K}" stroke-width="7" opacity="{A.ease(pish):.2f}" stroke-linecap="round"/>'
    pencx = lx + 90 + pish * (lw * .78)
    pency = ly + 300 - 28 * A.w(t, 1.3) * .3
    swing = 5 * A.w(t, .9, .1)
    s += (f'<g transform="rotate({swing:.1f} {pencx:.0f} {ly-140})">'
          f'<line x1="{pencx:.0f}" y1="{ly-140}" x2="{pencx:.0f}" y2="{pency:.0f}"'
          f' stroke="#cfcfcf" stroke-width="2" opacity=".65"/>'
          f'<rect x="{pencx-9:.0f}" y="{pency-70:.0f}" width="18" height="70" rx="3" fill="{KRAS}" {o(4)}/>'
          f'<path d="M{pencx-9:.0f},{pency:.0f} l9,22 l9,-22 Z" fill="#2a2a2a"/></g>')
    nail_y = ly - 90
    s += f'<circle cx="{lx+lw-120}" cy="{nail_y}" r="6" fill="{ZHELEZ}" {o(3)}/>'
    sway = 3 * A.w(t, 2.2, .3)
    s += (f'<g transform="rotate({sway:.1f} {lx+lw-120} {nail_y})">'
          f'<rect x="{lx+lw-176}" y="{nail_y+4}" width="118" height="94" rx="4" fill="#f3ecd8" {o(4)}'
          f' opacity=".92"/><text x="{lx+lw-120}" y="{nail_y+58}" font-size="30" fill="{K}"'
          f' text-anchor="middle" font-family="Georgia">ясно</text></g>')
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.46)
    return s


def konki_i_klavishi(t):
    """Тёплый вечер: белые фигурные коньки на столике и раскрытая нотная тетрадь."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#121521" opacity=".5"/>')
    s += SL(Z_DAL, utvar_izby(80, 980, 560, t, 8))
    s += vozduh(1120, 640, t, 900, .32)
    s += SL(Z_SRED, lampa(1120, 560, t, 1.2, abazhur=True))
    s += SL(Z_SRED, stol(760, 760, 640, 36))
    perev = A.seg(t, 2.2, 1.6)
    s += (f'<g transform="translate(1040,{764-18*A.ease(perev):.0f})">'
          f'<rect x="-120" y="0" width="240" height="150" rx="6" fill="#f4efe0" {o(5)}/>'
          f'<line x1="0" y1="6" x2="0" y2="144" stroke="{K}" stroke-width="3"/>')
    for i in range(5):
        s += f'<line x1="-96" y1="{30+i*18}" x2="-16" y2="{30+i*18}" stroke="{K}" stroke-width="1.5" opacity=".7"/>'
    turn = A.ease(perev)
    s += (f'<g transform="scale({1-turn*.45:.2f},1)">'
          + "".join(f'<line x1="16" y1="{30+i*18}" x2="96" y2="{30+i*18}" stroke="{K}" stroke-width="1.5" opacity="{.7*(1-turn):.2f}"/>' for i in range(5))
          + '</g></g>')
    kach = 4 * A.w(t, 1.6, .2)
    s += (f'<g transform="translate(800,790)">'
          f'<path d="M-70,0 q-6,86 10,110" fill="none" stroke="#e8e2d2" stroke-width="7" opacity=".85"/>'
          f'<ellipse cx="-70" cy="-16" rx="60" ry="30" fill="#f4f1e6" {o(5)}/>'
          f'<path d="M-130,-14 q-30,10 -16,36" fill="none" stroke="{ZHELEZ}" stroke-width="5"/>'
          f'<g transform="rotate({kach:.1f} -40 40)"><line x1="-40" y1="20" x2="-40" y2="90" stroke="#d8c7a6" stroke-width="4" opacity=".8"/></g>'
          f'<path d="M50,0 q-6,86 10,110" fill="none" stroke="#e8e2d2" stroke-width="7" opacity=".85"/>'
          f'<ellipse cx="50" cy="-16" rx="60" ry="30" fill="#f4f1e6" {o(5)}/>'
          f'<path d="M-10,-14 q-30,10 -16,36" fill="none" stroke="{ZHELEZ}" stroke-width="5"/>'
          f'<g transform="rotate({-kach:.1f} 80 40)"><line x1="80" y1="20" x2="80" y2="90" stroke="#d8c7a6" stroke-width="4" opacity=".8"/></g>'
          f'</g>')
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.44)
    return s


def dvorovyy_katok(t):
    """Дворовый каток в сумерках: девочка делает первые шаги, потом едет сама."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, nebo("sumer", t, True, 44))
    s += SL(Z_DAL, ulica_dal(0, 760, 830, t, True, 51))
    fonar_x, fonar_y = 240, 560
    s += SL(Z_SRED, f'<rect x="{fonar_x-8}" y="{fonar_y}" width="16" height="260" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, teplo(fonar_x, fonar_y - 10, 260, 220, .55 + .1 * abs(A.w(t, 2.1))))
    s += SL(Z_SRED, f'<circle cx="{fonar_x}" cy="{fonar_y-10}" r="22" fill="{SVET}" {o(4)}/>')
    s += SL(Z_DAL, holodny_svet(400, 900, 560, 160, .4))
    first = A.seg(t, .8, 2.4)
    free = A.seg(t, 4.0, 2.8)
    gx = 300 + 260 * A.ease(free)
    wob = (1 - A.ease(free)) * 10 * A.w(t, 1.4) + A.ease(free) * 4 * A.w(t, 2.2)
    adult_x = gx - 70 * (1 - A.ease(free))
    if free < 1.0:
        s += SL(Z_SRED, figura(adult_x, 900, 300, t, kant="#cfe4f5", telogreyka=True))
    s += (f'<g transform="translate({gx:.0f},900) rotate({wob:.1f})">'
          f'<path d="M-30,-180 q-10,70 0,130 l60,0 q10,-60 0,-130 Z" fill="#20222c" {o(4,"#cfe4f5")}/>'
          f'<circle cx="0" cy="-200" r="30" fill="#20222c" {o(4,"#cfe4f5")}/>'
          f'<path d="M-30,-224 a30,20 0 0 1 60,0 q-6,20 -30,22 q-24,-2 -30,-22 Z" fill="{KRAS}"/>'
          f'<circle cx="0" cy="-236" r="10" fill="{KRAS}"/>'
          f'<path d="M-24,-52 l10,56 M24,-52 l-10,56" fill="none" stroke="#20222c" stroke-width="10"/></g>')
    led_glow = .35 + .35 * A.ease(free)
    s += SL(Z_SRED, teplo(gx, 902, 180, 40, led_glow))
    s += SL(Z_LETIT, sneg_letit(t, 30, 71, .7, .8))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.44)
    return s


def led_bolshoy_areny(t):
    """Большая арена: фигуристка кружится во вращении, под лучами опускается медаль."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#10141f"/>')
    s += SL(Z_DAL, holodny_svet(830, 820, 760, 260, .55))
    for i in range(3):
        s += SL(Z_DAL, luch(140 + i * 260, 0, 90, 900, t, .14))
    cx, cy = 420, 860
    rot = t * 70 % 360
    s += (f'<g transform="translate({cx:.0f},{cy:.0f}) rotate({rot:.1f})">'
          f'<path d="M0,-210 q-54,20 -40,110 l80,0 q14,-90 -40,-110 Z" fill="#b24a6a" {o(4,"#f3d7e2")}/>'
          f'<circle cx="0" cy="-226" r="28" fill="#20222c" {o(4,"#f3d7e2")}/>'
          f'<path d="M-50,-96 q50,30 100,0" fill="none" stroke="#b24a6a" stroke-width="18" opacity=".8"/>'
          f'</g>')
    s += SL(Z_SRED, teplo(cx, 900, 220, 40, .4))
    s += SL(Z_LETIT, iskra_let(t, cx + 60, 880, 10, 14, 220, .9))
    zolo = A.seg(t, 2.6, 1.6)
    my = -40 + 560 * A.ease(zolo)
    sw = 6 * A.w(t, 1.1)
    if zolo > 0.02:
        s += (f'<line x1="1460" y1="-20" x2="1460" y2="{my-30:.0f}" stroke="{KREM}" stroke-width="3" opacity=".7"/>'
              f'<g transform="rotate({sw:.1f} 1460 {my:.0f})">'
              f'<circle cx="1460" cy="{my:.0f}" r="46" fill="url(#zol)" {o(5)}/>'
              f'<circle cx="1460" cy="{my:.0f}" r="20" fill="{ZOL}" opacity=".7"/></g>')
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.5)
    return s


def semya_u_televizora(t):
    """Комната: экран со силуэтом фигуристки, семья на диване замерла."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#111623" opacity=".55"/>')
    tvx, tvy = 420, 560
    mig = .7 + .3 * abs(A.w(t, .35))
    s += SL(Z_DAL, f'<rect x="{tvx-220}" y="{tvy-180}" width="440" height="320" rx="10" fill="#1a1a1a" {o(6)}/>'
                   f'<rect x="{tvx-190}" y="{tvy-150}" width="380" height="248" fill="#dfe8ef" opacity="{mig:.2f}"/>'
                   f'<rect x="{tvx-100}" y="{tvy+140}" width="200" height="60" fill="{ZHELEZ}" {o(4)}/>')
    s += (f'<g transform="translate({tvx:.0f},{tvy+30}) rotate({10*A.w(t,2.6):.1f})">'
          f'<ellipse cx="0" cy="0" rx="40" ry="90" fill="#9fb4c4" opacity="{mig:.2f}"/>'
          f'<circle cx="0" cy="-104" r="22" fill="#9fb4c4" opacity="{mig:.2f}"/></g>')
    s += SL(Z_SRED, teplo(tvx, tvy, 360, 220, .3))
    s += SL(Z_SRED, f'<rect x="900" y="760" width="760" height="180" rx="30" fill="{TKAN2}" {o(6)}/>'
                     f'<rect x="900" y="700" width="760" height="100" rx="40" fill="{TKAN2}" {o(6)}/>')
    s += SL(Z_SRED, figura(1060, 870, 300, t * 0, kant="#cfe4f5", profil=True))
    s += SL(Z_SRED, figura(1360, 870, 280, t * 0, kant="#cfe4f5"))
    cup_shiver = .3 * A.w(t, 7.0)
    s += (f'<g transform="translate(1020,760) rotate({cup_shiver:.1f})">'
          f'<path d="M-18,0 h36 v26 q0,16 -18,16 q-18,0 -18,-16 Z" fill="{KREM}" {o(3)}/>'
          f'<path d="M18,6 q20,2 14,20 q-6,14 -18,10" fill="none" stroke="{KREM}" stroke-width="4"/></g>')
    s += SL(Z_SRED, kot(1460, 880, t, 1.0, spit=A.w(t, 9.0) > .9))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def pianino_u_okna(t):
    """Пианино у окна, руки на клавишах; за окном вечерний город без примет."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1a2030" opacity=".5"/>')
    city = panelka(540, 1080, 400, t, 6, True, 19)
    s += SL(Z_DAL, okno_izby(260, 420, 260, 360, t, vid=city, moroz=.15))
    s += SL(Z_SRED, svecha(170, 760, t, .3, 1.1))
    px, py, pw = 90, 820, 700
    s += SL(Z_SRED, f'<rect x="{px}" y="{py}" width="{pw}" height="170" rx="10" fill="#1c1a1f" {o(6)}/>'
                    f'<rect x="{px+30}" y="{py+20}" width="{pw-60}" height="70" rx="4" fill="#f4f1e6" {o(4)}/>')
    for i in range(18):
        bx = px + 46 + i * ((pw - 92) / 17)
        s += f'<rect x="{bx:.0f}" y="{py+22}" width="{(pw-92)/17-3:.1f}" height="64" fill="#15131a"/>' if i % 7 in (1, 2, 4, 5, 6) else ""
    press = abs(A.w(t, .6, .1))
    s += (f'<g transform="translate({px+pw*.42:.0f},{py+30+press*4:.0f})">'
          f'<path d="M-70,0 q0,-16 70,-16 q70,0 70,16 l0,10 l-140,0 Z" fill="{K}" opacity=".88"/></g>')
    turn = A.seg(t, 1.6, 2.4)
    s += (f'<g transform="translate({px+pw*.2:.0f},{py-60}) rotate({-6+6*A.ease(turn):.1f})">'
          f'<rect x="-70" y="-50" width="140" height="80" rx="4" fill="#f4efe0" {o(4)}/>'
          + "".join(f'<line x1="{-56}" y1="{-30+i*14}" x2="{56}" y2="{-30+i*14}" stroke="{K}" stroke-width="1.3" opacity=".6"/>' for i in range(5))
          + '</g>')
    s += SL(Z_SRED, figura(px + pw * .42, py + 190, 300, t, kant="#e7c7a0", profil=False))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.44)
    return s


def afishnaya_tumba_v_snegu(t):
    """Круглая афишная тумба под снегом, на ней по словам встают три листа с названиями."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 61))
    s += SL(Z_DAL, ulica_dal(0, 760, W, t, True, 72))
    cx, base = 960, 980
    s += SL(Z_SRED, ten(cx, base + 10, 220, 30, .5))
    s += SL(Z_SRED, f'<rect x="{cx-170}" y="{base-440}" width="340" height="440" rx="170" fill="#2d3340" {o(7)}/>')
    sway = 4 * A.w(t, 3.2)
    s += (f'<g transform="translate({cx+240},{base-520}) rotate({sway:.1f} 0 0)">'
          f'<line x1="0" y1="0" x2="0" y2="140" stroke="{ZHELEZ}" stroke-width="10"/>'
          f'<circle cx="0" cy="-10" r="20" fill="{SVET}" {o(4)}/></g>')
    s += SL(Z_SRED, teplo(cx + 240, base - 390, 340, 280, .5))
    nazvania = ("Дожди", "Билет на балет", "Город, которого нет")
    for i, nm in enumerate(nazvania):
        app = A.ease(A.seg(t, .9 + i * 1.1, .9))
        if app <= 0:
            continue
        yy = base - 360 + i * 110
        s += (f'<g opacity="{app:.2f}" transform="translate({cx:.0f},{yy:.0f}) scale({.6+.4*app:.2f})">'
              f'<rect x="-150" y="-50" width="300" height="100" rx="4" fill="#efe9d8" opacity=".92" {o(3)}/>'
              f'<text x="0" y="8" font-size="26" text-anchor="middle" fill="{K}" font-family="Georgia">{nm}</text></g>')
    s += SL(Z_SRED, _sneg_lezhit_polosa(cx - 170, base - 56, 340, 56))
    s += SL(Z_LETIT, sneg_letit(t, 48, 81, .85, 1.0))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def okno_doma_vdali(t):
    """Тёмное снежное поле, вдали одно тёплое окно; силуэт с чемоданом идёт к нему."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_NEBO, nebo("noch", t, True, 91))
    s += SL(Z_DAL, f'<rect x="0" y="760" width="{W}" height="{H-760}" fill="#0e1420"/>')
    wx, wy = 1420, 660
    mig = .55 + .35 * abs(A.w(t, 4.0))
    s += SL(Z_DAL, teplo(wx, wy, 220, 170, .5))
    s += SL(Z_DAL, f'<rect x="{wx-220}" y="{wy-20}" width="440" height="260" fill="#0c0f16" {o(7)}/>'
                   f'<rect x="{wx-50}" y="{wy-70}" width="100" height="120" rx="4" fill="{SVET}" opacity="{mig:.2f}"/>')
    step = A.ease(A.seg(t, 2.0, 3.6))
    hx = 420 + (wx - 500 - 420) * step
    s += SL(Z_SRED, figura(hx, 980, 280, t, kant="#9fc4d8"))
    s += SL(Z_SRED, f'<rect x="{hx+30:.0f}" y="920" width="60" height="70" rx="6" fill="#20222c" {o(4,"#9fc4d8")}/>')
    s += SL(Z_SRED, par_izo_rta(hx - 10, 870, t, .1, .9, .5))
    s += SL(Z_LETIT, sneg_letit(t, 60, 101, .9, 1.1))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.5)
    return s


def sviter_s_dvumya_rukavami(t):
    """Готовый свитер поднимают за плечи, надевают — рукавов два."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#201c26" opacity=".5"/>')
    s += SL(Z_DAL, mebel_hlam(1300, 820, 420, t, 44))
    s += SL(Z_SRED, lampa(260, 480, t, 1.0))
    lift = A.ease(A.seg(t, .6, 1.8))
    x, y = 940, 500 - 60 * lift
    sway = 4 * A.w(t, 1.4)
    s += (f'<g transform="translate({x:.0f},{y:.0f}) rotate({sway:.1f} 0 0)">'
          f'<path d="M-170,0 q170,-70 340,0 l-20,260 q-150,40 -300,0 Z" fill="{TKAN}" {o(6)}/>')
    put_on = A.ease(A.seg(t, 2.6, 2.4))
    lr = -40 * (1 - put_on)
    rr = 40 * (1 - put_on)
    s += (f'<g transform="rotate({lr:.1f} -170 20)"><rect x="-290" y="0" width="120" height="50" rx="20" fill="{TKAN}" {o(5)}/></g>'
          f'<g transform="rotate({rr:.1f} 170 20)"><rect x="170" y="0" width="120" height="50" rx="20" fill="{TKAN}" {o(5)}/></g>'
          f'</g>')
    s += SL(Z_SRED, figura(940, 1000, 300, t, kant="#e7c7a0", op=.25 + .75 * put_on))
    s += SL(Z_SRED, f'<ellipse cx="640" cy="940" rx="70" ry="36" fill="url(#rush)" opacity=".85" {o(4)}/>')
    blesk = .5 + .5 * abs(A.w(t, 2.0))
    s += (f'<line x1="610" y1="920" x2="670" y2="920" stroke="#d8d8e0" stroke-width="5" opacity="{blesk:.2f}"/>'
          f'<line x1="610" y1="936" x2="670" y2="936" stroke="#d8d8e0" stroke-width="5" opacity="{blesk*.8:.2f}"/>')
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s


def korobka_nedodelok(t):
    """Коробка на антресоли с рамкой, варежкой и проволокой — едет вниз, на боку «потом»."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1c1a22" opacity=".55"/>')
    s += SL(Z_DAL, luch(1200, 0, 260, 900, t, .18))
    edet = A.ease(A.seg(t, .8, 2.4))
    cy = 320 + 420 * edet
    pyl = A.seg(t, .8, 1.4)
    if pyl < 1:
        for i in range(10):
            s += f'<circle cx="{860+i*20}" cy="{300-60*pyl}" r="{3+2*(1-pyl)}" fill="#cfcfcf" opacity="{.5*(1-pyl):.2f}"/>'
    s += SL(Z_SRED, ten(960, cy + 190, 260, 24, .4))
    s += (f'<g transform="translate(760,{cy:.0f})">'
          f'<rect x="0" y="0" width="400" height="260" rx="8" fill="#b9915f" {o(6)}/>'
          f'<path d="M0,40 h400 M0,160 h400" stroke="#8a6a40" stroke-width="6"/>'
          f'<text x="200" y="230" font-size="30" fill="#5a4426" text-anchor="middle" font-family="Georgia" opacity=".85">потом</text>')
    svis = 6 * A.w(t, 1.6)
    s += (f'<g transform="rotate({svis:.1f} 40 260)"><path d="M10,230 l20,70 l40,-10 l-16,-64 Z" fill="{TKAN2}" {o(4)}/></g>'
          f'<rect x="-30" y="-50" width="60" height="90" rx="4" fill="url(#derev)" {o(5)}/>'
          f'<circle cx="300" cy="-30" r="36" fill="none" stroke="{ZHELEZ}" stroke-width="8"/>'
          f'<circle cx="300" cy="-30" r="36" fill="none" stroke="{ZHELEZ}" stroke-width="3" stroke-dasharray="4 6" opacity=".6"/>'
          f'</g>')
    s += SL(Z_PERED, ramka_pp("levo"))
    s += vinetka(.46)
    return s


def kreslo_s_morsom_i_odeyalom(t):
    """Кресло у инея в окне; на слова в руке — кружка морса, на плечи — одеяло, рядом хлеб и табуретка."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#0f1420" opacity=".5"/>')
    s += SL(Z_DAL, okno_izby(120, 300, 360, 480, t, moroz=.8))
    s += inej(120, 300, 360, t, 16, 71, "#dcefff", 60)
    s += SL(Z_SRED, teplo(900, 760, 420, 320, .4))
    s += SL(Z_SRED, figura(900, 1000, 320, t, kant="#cfe4f5", profil=False))
    cup = A.seg(t, .8, 1.4)
    if cup > 0:
        s += (f'<g opacity="{A.ease(cup):.2f}" transform="translate(1020,860)">'
              f'<path d="M-20,0 h40 v30 q0,18 -20,18 q-20,0 -20,-18 Z" fill="{KREM}" {o(3)}/>'
              + par(1020, 850, t, 3, .5, 120, .45) + '</g>')
    odeyalo = A.ease(A.seg(t, 2.4, 1.8))
    s += (f'<path d="M760,{860-30*odeyalo:.0f} q140,{-40*odeyalo:.0f} 280,0 l10,{140*odeyalo:.0f}'
          f' q-150,{30*odeyalo:.0f} -300,0 Z" fill="{TKAN2}" opacity="{odeyalo:.2f}" {o(5)}/>')
    stol_t = A.ease(A.seg(t, 4.2, 1.6))
    if stol_t > 0:
        s += SL(Z_SRED, stol(1240, 980 - 10 * stol_t, 260, 30))
        s += (f'<g opacity="{stol_t:.2f}" transform="translate(1370,978)">'
              f'<rect x="-100" y="-20" width="200" height="30" rx="6" fill="url(#derev)" {o(5)}/>'
              + par(1370, 950, t, 3, .5, 130, .5) + '</g>')
    tab = A.ease(A.seg(t, 5.2, 1.4))
    if tab > 0:
        s += SL(Z_SRED, lavka(1580, 1040 - 20 * (1 - tab) + 20, 140))
        if tab > .7:
            s += SL(Z_SRED, kot(1620, 1000, t, .8))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += vinetka(.48)
    return s


def podokonnik_s_tem_chto_podozhdet(t):
    """Подоконник: банка краски и бумажный кораблик; за стеклом снег и далёкая проталина."""
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += SL(Z_NEBO, nebo("den", t, False, 101))
    s += holodny_svet(960, 280, 700, 240, .4)
    prot = .2 + .08 * abs(A.w(t, 3.0))
    s += SL(Z_NEBO, f'<ellipse cx="1660" cy="320" rx="90" ry="40" fill="{TRAVA}" opacity="{prot:.2f}"/>')
    s += SL(Z_DAL, f'<rect x="0" y="560" width="{W}" height="{H-560}" fill="url(#stekl)" opacity=".2"/>')
    s += SL(Z_LETIT, sneg_letit(t, 44, 111, .75, .9))
    sx, sy, sw = 420, 780, 1080
    s += SL(Z_SRED, f'<rect x="{sx}" y="{sy}" width="{sw}" height="70" rx="6" fill="url(#dosk)" {o(6)}/>')
    s += SL(Z_SRED, ten(sx + 260, sy + 90, 150, 20, .4))
    blik_op = .4 + .4 * abs(A.w(t, 2.4))
    s += (f'<g transform="translate({sx+220},{sy-10})">'
          f'<rect x="-70" y="-180" width="140" height="180" rx="8" fill="{TKAN2}" {o(6)}/>'
          f'<ellipse cx="0" cy="-180" rx="70" ry="18" fill="{ZHELEZ}" {o(5)}/>'
          f'<ellipse cx="0" cy="-180" rx="30" ry="9" fill="#dfe6ea" opacity="{blik_op:.2f}"/></g>')
    bob = 3 * A.w(t, 2.0, .4)
    s += (f'<g transform="translate({sx+620},{sy-14}) rotate({bob:.1f} 0 0)">'
          f'<path d="M-70,0 l140,0 l-70,50 Z" fill="#f2ecd8" {o(4)}/>'
          f'<path d="M-70,0 q70,-30 140,0" fill="none" stroke="{K}" stroke-width="3" opacity=".6"/></g>')
    s += SL(Z_PERED, ramka_pp("verh"))
    s += vinetka(.4)
    return s
