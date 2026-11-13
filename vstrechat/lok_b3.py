# -*- coding: utf-8 -*-
"""Декорации планов 43-56 ролика «Как встречать год хозяйки года 2027»."""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob
OKNO = (860, 300, 980, 551)

# ── палитра шестьдесят седьмого ────────────────────────────────────────────
# Лето и вечер: асфальт двора, выгоревшая штукатурка кинотеатра, бордовый
# бархат зала. Тёплое пятно в кадре всегда одно — шкала радиолы, лампа
# проектора, экран, свечи. Красное и золото остаются акцентом.
ASFALT  = "#4f555c"; ASFALT2 = "#373d43"
TRAV67  = "#5d7a42"; TRAV68  = "#3f5730"
SHTUK   = "#e3d6b6"; SHTUK2  = "#bfae86"
BORDO   = "#6e1f26"; BORDO2  = "#43131a"
BUMAGA  = "#f0e4c3"; BUMAGA2 = "#cdbb8e"
SINKA   = "#2f4c70"; SEPIA   = "#b49c76"; SEPIA2 = "#6d5c45"
PLENKA  = "#2a2724"
SERIF   = 'font-family="DejaVu Serif"'


# ═══════════════════ ОБЩИЕ КИРПИЧИКИ ЭТОГО БЛОКА ═══════════════════

def _lampochki(x, y, w_, h_, t, n=24, col=SVET, r_=11, sp=.7):
    """Цепочка лампочек по периметру афиши: огонёк бежит по кругу."""
    s = ""
    per = 2.0 * (w_ + h_)
    for i in range(n):
        u = per * i / n
        if u < w_:
            px, py = x + u, y
        elif u < w_ + h_:
            px, py = x + w_, y + (u - w_)
        elif u < 2 * w_ + h_:
            px, py = x + w_ - (u - w_ - h_), y + h_
        else:
            px, py = x, y + h_ - (u - 2 * w_ - h_)
        gor = .26 + .74 * (.5 + .5 * math.sin(2 * math.pi * (t * sp - 2.2 * i / n)))
        s += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r_*2.6:.0f}" fill="{col}"'
              f' opacity="{gor*.18:.2f}"/>')
        s += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r_*(.62+.38*gor):.1f}" fill="{col}"'
              f' opacity="{.35+.65*gor:.2f}" stroke="{K}" stroke-width="3"/>')
    return s


def _stroka(x, y, shir, s_, kegl, col="#2a1d12"):
    """Строка названия на афише. Единственный текст, который блок разрешает:
    фильмы показываем БЕЗ кадров и лиц — только буквами."""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" {SERIF}'
            f' font-size="{kegl:.0f}" font-weight="bold" letter-spacing="2"'
            f' fill="{col}">{s_}</text>')


def _gory(x, y, w_, h_, seed=3, noch=False):
    """Рисунок афиши: горы и светило. Ни кадра из фильма, ни лица."""
    r = random.Random(seed)
    sx = x + w_ * (.70 if seed % 2 else .26)
    if noch:
        s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
             f' fill="#334058" opacity=".55"/>')
        s += (f'<circle cx="{sx:.0f}" cy="{y+h_*.30:.0f}" r="{h_*.20:.0f}" fill="{KREM}"/>'
              f'<circle cx="{sx+h_*.11:.0f}" cy="{y+h_*.23:.0f}" r="{h_*.19:.0f}" fill="#3b4761"/>')
        gory = ((.16, .86, "#3f4c66"), (.42, 1.0, "#2d3a50"), (.72, .74, "#1f2838"))
    else:
        s = (f'<circle cx="{sx:.0f}" cy="{y+h_*.34:.0f}" r="{h_*.20:.0f}"'
             f' fill="{ORA}" opacity=".85"/>')
        gory = ((.16, .86, "#6d7f8c"), (.42, 1.0, "#55697a"), (.72, .74, "#3f5466"))
    for i, (u, hh, col) in enumerate(gory):
        px = x + w_ * u
        ph_ = h_ * hh * .78
        s += (f'<path d="M{px-w_*.30:.0f},{y+h_:.0f} L{px:.0f},{y+h_-ph_:.0f}'
              f' L{px+w_*.30:.0f},{y+h_:.0f} Z" fill="{col}" {o(5)}/>')
        s += (f'<path d="M{px-w_*.055:.0f},{y+h_-ph_*.78:.0f} L{px:.0f},{y+h_-ph_:.0f}'
              f' L{px+w_*.055:.0f},{y+h_-ph_*.78:.0f} q{-w_*.04:.0f},{h_*.05:.0f}'
              f' {-w_*.085:.0f},0 q{-w_*.04:.0f},{-h_*.05:.0f} {-w_*.085:.0f},0 Z"'
              f' fill="{KREM}" opacity=".85"/>')
    return s


def _afisha(x, y, w_, h_, naz, t=0.0, kegl=54, otgib=0.0, seed=3, lampy=False,
            noch=False):
    """Рисованная киноафиша: рама, выгоревшая бумага, горы, название буквами.
    `otgib` 0..1 — отстающий уголок внизу справа."""
    s = ten(x + w_ / 2 + 14, y + h_ + 18, w_ * .48, 16, .45)
    s += (f'<rect x="{x-14:.0f}" y="{y-14:.0f}" width="{w_+28:.0f}" height="{h_+28:.0f}"'
          f' rx="8" fill="url(#derev)" {o(7)}/>')
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' fill="url(#list)" {o(5)}/>')
    stroki = [naz]
    if len(naz) > 13:
        m = naz.rfind(" ", 0, len(naz) // 2 + 4)
        if m > 0:
            stroki = [naz[:m], naz[m + 1:]]
    nl = len(stroki)
    kg = max(30, min(kegl, (w_ - 44) * 1.70 / max(1, max(len(u) for u in stroki)),
                     h_ * .30 / nl))
    tband = min(.66, .10 + kg * 1.20 * nl / h_)
    s += _gory(x + 10, y + h_ * tband, w_ - 20, h_ * (1 - tband) - 12, seed, noch)
    for i, u in enumerate(stroki):
        s += _stroka(x + w_ / 2, y + h_ * .06 + kg * .82 + i * kg * 1.18, w_, u.upper(), kg)
    pw = min(w_ * .70, kg * .60 * max(len(u) for u in stroki))
    s += (f'<path d="M{x+w_/2-pw/2:.0f},{y+h_*tband-10:.0f} h{pw:.0f}" {o(4, "#a4381f")}/>')
    if otgib > .01:
        a = 26 * otgib
        s += (f'<g transform="rotate({a:.1f} {x+w_:.0f} {y+h_:.0f})">'
              f'<path d="M{x+w_-110*otgib:.0f},{y+h_:.0f} L{x+w_:.0f},{y+h_:.0f}'
              f' L{x+w_:.0f},{y+h_-110*otgib:.0f} Z" fill="{BUMAGA2}" {o(4)}/></g>')
    s += (f'<path d="M{x+16:.0f},{y+h_*.06:.0f} l{w_*.36:.0f},{h_*.5:.0f}"'
          f' stroke="#ffffff" stroke-width="12" opacity=".16"/>')
    if lampy:
        s += _lampochki(x - 26, y - 26, w_ + 52, h_ + 52, t, 26)
    return s


def _golova(x, y, r_, t, col="#1d2029", kant="#f0c070", ph=0.0, tryas=0.0, plechi=1.0):
    """Затылок и плечи зрителя. Тряска от смеха — живой элемент зала."""
    dy = tryas * (2.6 * A.w(t, .33, ph) + 1.6 * A.w(t, .19, ph * 1.7))
    return (f'<g transform="translate({x:.0f},{y+dy:.1f})">'
            f'<path d="M{-r_*2.6*plechi:.0f},{r_*3.0:.0f} q{r_*2.6*plechi:.0f},{-r_*2.3:.0f}'
            f' {r_*5.2*plechi:.0f},0 Z" fill="{col}"/>'
            f'<circle cx="0" cy="0" r="{r_:.0f}" fill="{col}"/>'
            f'<circle cx="0" cy="0" r="{r_:.0f}" fill="none" stroke="#0d1119"'
            f' stroke-width="{max(2,r_*.10):.1f}" opacity=".8"/>'
            f'<path d="M{-r_*.52:.0f},{-r_*.78:.0f} a{r_:.0f},{r_:.0f} 0 0 1 {r_*1.04:.0f},0"'
            f' fill="none" stroke="{kant}" stroke-width="{max(2,r_*.17):.1f}" opacity=".65"/></g>')


def _katushka(x, y, r_, t, sp=1.0, col="#6a6f76", lenta=True):
    """Катушка киноплёнки: обод, три окна, плёнка намотана. Вращается."""
    a = (t * sp * 150.0) % 360
    s = f'<g transform="translate({x:.0f},{y:.0f})">'
    s += f'<circle r="{r_:.0f}" fill="url(#zhel)" {o(6)}/>'
    if lenta:
        s += f'<circle r="{r_*.78:.0f}" fill="{PLENKA}" {o(4)}/>'
        s += f'<circle r="{r_*.44:.0f}" fill="{col}" {o(4)}/>'
    s += f'<g transform="rotate({a:.1f})">'
    for i in range(3):
        aa = i * 120
        s += (f'<g transform="rotate({aa})"><ellipse cx="0" cy="{-r_*.60:.0f}"'
              f' rx="{r_*.20:.0f}" ry="{r_*.26:.0f}" fill="#1b1d20" opacity=".8"/></g>')
    s += (f'<line x1="{-r_*.9:.0f}" y1="0" x2="{r_*.9:.0f}" y2="0" stroke="#d7dde4"'
          f' stroke-width="4" opacity=".55"/>')
    s += '</g>'
    s += f'<circle r="{r_*.14:.0f}" fill="{CHUGUN}" {o(3)}/>'
    s += f'<circle cx="{-r_*.34:.0f}" cy="{-r_*.42:.0f}" r="{r_*.16:.0f}" fill="#ffffff" opacity=".2"/>'
    return s + '</g>'


def _kreslo(x, y, w_, h_, col=BORDO, col2=BORDO2):
    """Кресло зала фронтально: спинка валиком, подлокотники, тень под сиденьем."""
    return (ten(x + w_ / 2, y + h_ + 10, w_ * .52, 14, .45)
            + f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
              f' rx="{w_*.22:.0f}" fill="{col}" {o(6)}/>'
            + f'<rect x="{x+w_*.12:.0f}" y="{y+h_*.12:.0f}" width="{w_*.76:.0f}"'
              f' height="{h_*.6:.0f}" rx="{w_*.16:.0f}" fill="{col2}" opacity=".55"/>'
            + f'<rect x="{x-w_*.12:.0f}" y="{y+h_*.52:.0f}" width="{w_*.18:.0f}"'
              f' height="{h_*.5:.0f}" rx="10" fill="url(#derev)" {o(5)}/>'
            + f'<rect x="{x+w_*.94:.0f}" y="{y+h_*.52:.0f}" width="{w_*.18:.0f}"'
              f' height="{h_*.5:.0f}" rx="10" fill="url(#derev)" {o(5)}/>'
            + f'<path d="M{x+w_*.2:.0f},{y+h_*.1:.0f} q{w_*.3:.0f},{-h_*.06:.0f} {w_*.6:.0f},0"'
              f' stroke="#ffffff" stroke-width="7" opacity=".16" fill="none"/>')


def _svechka(x, y, h_, t, gorit=1.0, ph=0.0, w_=12):
    """Свечка на пироге: воск, фитиль, огонёк, который загорается в свой срок."""
    s = (f'<rect x="{x-w_/2:.1f}" y="{y-h_:.1f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="4" fill="{ob.ALYJ}" {o(3)}/>')
    s += (f'<rect x="{x-w_/2:.1f}" y="{y-h_*.60:.1f}" width="{w_:.0f}"'
          f' height="{h_*.26:.1f}" fill="#fbf3e4"/>')
    s += f'<path d="M{x:.1f},{y-h_:.1f} v-8" fill="none" {o(3)}/>'
    if gorit > .02:
        hh = (21 + 5 * A.w(t, .72, ph)) * gorit
        dx = 1.6 * A.w(t, 1.25, ph)
        s += teplo(x, y - h_ - hh * .5, 26 * gorit, 30 * gorit, .42 * gorit)
        s += (f'<path d="M{x+dx:.1f},{y-h_-8-hh:.1f} c7,{hh*.5:.1f} 5,{hh*.8:.1f} -1,{hh:.1f}'
              f' c-6,{-hh*.2:.1f} -7,{-hh*.5:.1f} 1,{-hh:.1f} Z" fill="{SVET}"'
              f' opacity="{min(1.0,gorit):.2f}"/>')
    return s


def _tochki_60(cx, cy, r_):
    """Точки по контуру цифр «60» — на них встают свечки пирога.

    Цифры стоят почти фронтально (сжатие .76), кольца РАЗНОЙ высоты и свечек
    мало: при плоской раскладке по ободу и частой расстановке ряды свечек
    сливаются и число читается частоколом (поймано на трёх осмотрах)."""
    p = []
    szh = .45

    def tochka(u, v):
        p.append((cx + u * r_, cy + v * r_ * szh))

    for i in range(7):                        # кольцо шестёрки — внизу и мельче
        a_ = 2 * math.pi * i / 7
        tochka(-.78 + .42 * math.cos(a_), .36 + .56 * math.sin(a_))
    for i in range(4):                        # хвост шестёрки вверх-вправо
        u = (i + 1) / 4.0
        tochka(-1.20 + .68 * u * u, -.22 - .74 * u)
    for i in range(12):                       # кольцо нуля — во всю высоту
        a_ = 2 * math.pi * i / 12
        tochka(.82 + .44 * math.cos(a_), .96 * math.sin(a_))
    return p


def _dom67(x, base, w_, t, seed=1, svet=True):
    """Частный дом летнего вечера: обшивка, шиферная крыша с трубой, окно со
    ставнями, палисадник. Снега на крыше нет — это июнь, а не ноябрь."""
    r = random.Random(seed)
    h_ = w_ * .74
    s = ten(x + w_ / 2, base + 14, w_ * .52, 20, .5)
    s += baza.doski(x, base - h_, w_, h_, max(34, int(w_ * .13)), True,
                    r.choice(("dosk", "derev")))
    kh_ = w_ * r.uniform(.19, .25)
    s += (f'<path d="M{x-w_*.10:.0f},{base-h_:.0f} L{x+w_/2:.0f},{base-h_-kh_:.0f}'
          f' L{x+w_*1.10:.0f},{base-h_:.0f} Z" fill="#4d535c" {o(7)}/>')
    for i in range(4):
        s += (f'<path d="M{x-w_*.10+w_*.07:.0f},{base-h_-kh_*(.16+i*.2):.0f}'
              f' L{x+w_*1.10-w_*.07:.0f},{base-h_-kh_*(.16+i*.2):.0f}" fill="none"'
              f' stroke="#5e656f" stroke-width="4" opacity=".45"/>')
    s += (f'<path d="M{x-w_*.10:.0f},{base-h_:.0f} L{x+w_/2:.0f},{base-h_-kh_:.0f}"'
          f' fill="none" stroke="#7d848e" stroke-width="7" opacity=".75"/>')
    tx = x + w_ * r.choice((.30, .66))
    s += (f'<rect x="{tx:.0f}" y="{base-h_-kh_*.92:.0f}" width="{w_*.10:.0f}"'
          f' height="{kh_*.62:.0f}" fill="url(#kamen)" {o(5)}/>'
          f'<rect x="{tx-w_*.015:.0f}" y="{base-h_-kh_*.96:.0f}" width="{w_*.13:.0f}"'
          f' height="{kh_*.10:.0f}" rx="4" fill="{KAMEN2}" {o(4)}/>')
    s += (f'<rect x="{x-w_*.12:.0f}" y="{base-h_-10:.0f}" width="{w_*1.24:.0f}" height="20"'
          f' rx="7" fill="{DOSKA2}" {o(5)}/>')
    ox, oy = x + w_ * .30, base - h_ * .80
    ow, oh = w_ * .28, w_ * .22
    s += baza.okno_izby(ox, oy, ow, oh, t, None, 0.0, svet, True)
    for sgn, sx in ((-1, ox - 16), (1, ox + ow + 16)):
        s += (f'<rect x="{sx-(ow*.22 if sgn<0 else 0):.0f}" y="{oy-14:.0f}"'
              f' width="{ow*.22:.0f}" height="{oh+28:.0f}" rx="5" fill="#2c4a52" {o(5)}/>')
        s += (f'<path d="M{sx-(ow*.16 if sgn<0 else -ow*.06):.0f},{oy+oh*.3:.0f}'
              f' h{ow*.12:.0f}" stroke="#4f727a" stroke-width="5"/>')
    s += (f'<rect x="{x+w_*.70:.0f}" y="{base-h_*.40:.0f}" width="{w_*.17:.0f}"'
          f' height="{h_*.40:.0f}" rx="6" fill="{DOSKA2}" {o(6)}/>')
    for i in range(3):
        bx = x + w_ * (.10 + i * .36)
        s += (f'<ellipse cx="{bx:.0f}" cy="{base-18:.0f}" rx="{w_*.12:.0f}"'
              f' ry="{w_*.10:.0f}" fill="{TRAV68}" opacity=".92" {o(4)}/>')
    return s


def _belyo(x, y, w_, h_, col, t, ph=0.0):
    """Бельё на верёвке: прищепки сверху, подол чуть дышит на вечернем воздухе."""
    k = 5 * A.w(t, 4.6, ph)
    return (f'<path d="M{x:.0f},{y:.0f} h{w_:.0f} q{6+k:.0f},{h_*.55:.0f} {k*.4:.0f},{h_:.0f}'
            f' h{-w_:.0f} q{-6-k:.0f},{-h_*.45:.0f} {-k*.4:.0f},{-h_:.0f} Z"'
            f' fill="{col}" opacity=".93" {o(4)}/>'
            f'<rect x="{x+4:.0f}" y="{y-14:.0f}" width="12" height="26" rx="4" fill="url(#derev)" {o(3)}/>'
            f'<rect x="{x+w_-16:.0f}" y="{y-14:.0f}" width="12" height="26" rx="4" fill="url(#derev)" {o(3)}/>')


def _kartochka_bw(x, y, w_, h_, vid, t, otkl=0.0, ph=0.0):
    """Чёрно-белая рисованная карточка в альбомных уголках. Чуть отходит
    от уголка — это её живой элемент."""
    a = 2.6 * otkl * (1 + .4 * A.w(t, 3.0, ph))
    s = f'<g transform="rotate({a:.2f} {x:.0f} {y+h_:.0f})">'
    s += ten(x + w_ / 2 + 8, y + h_ + 12, w_ * .46, 12, .5)
    s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="#efe8da" {o(4)}/>'
    s += (f'<rect x="{x+10:.0f}" y="{y+10:.0f}" width="{w_-20:.0f}" height="{h_-28:.0f}"'
          f' fill="{SEPIA}" opacity=".55"/>')
    ix, iy, iw, ih = x + 10, y + 10, w_ - 20, h_ - 28
    if vid == "dom":
        s += (f'<path d="M{ix+iw*.18:.0f},{iy+ih*.86:.0f} v{-ih*.4:.0f} h{iw*.5:.0f}'
              f' v{ih*.4:.0f} Z" fill="{SEPIA2}"/>'
              f'<path d="M{ix+iw*.12:.0f},{iy+ih*.46:.0f} L{ix+iw*.43:.0f},{iy+ih*.2:.0f}'
              f' L{ix+iw*.74:.0f},{iy+ih*.46:.0f} Z" fill="#4e4234"/>')
    elif vid == "para":
        s += ob.figura(ix + iw * .36, iy + ih * .9, ih * .72, t, "#4e4234", "#d9cdb4", False, ph)
        s += ob.figura(ix + iw * .64, iy + ih * .9, ih * .66, t, "#5d503f", "#d9cdb4", False, ph + .4)
    elif vid == "elka":
        s += ob.elka(ix + iw * .5, iy + ih * .92, ih * .8, t, False, True, 6, False)
    else:
        s += ob.koza_malaya(ix + iw * .34, iy + ih * .88, t, ih * .0013, ph)
    s += (f'<rect x="{x+10:.0f}" y="{y+10:.0f}" width="{w_-20:.0f}" height="{h_-28:.0f}"'
          f' fill="#cdc1a6" opacity=".52"/>')
    for sx, sy, d in ((x, y, "l34,0 l-34,34"), (x + w_, y, "l-34,0 l34,34"),
                      (x, y + h_, "l34,0 l-34,-34"), (x + w_, y + h_, "l-34,0 l34,-34")):
        s += f'<path d="M{sx:.0f},{sy:.0f} {d} Z" fill="#2d2721" opacity=".85"/>'
    return s + '</g>'


# ═══════════════════ ПЛАН 43 ═══════════════════

def dvor_shestdesyat_sedmogo(t):
    """Двор между пятиэтажками на закате: бельевые столбы, стол для домино,
    дети с мячом, радиола в открытом окне. Живое: мяч прыгает, костяшка
    домино стучит по столу, занавески в окне колышутся."""
    s = baza.nebo("zakat", t, False)
    s += baza.oblaka(t, 170, 5, 21, .42, "#f7ddba", 6.0)
    s += baza.panelka(-120, 700, 700, t, 5, True, 12)
    s += baza.panelka(1260, 700, 760, t, 5, True, 19)
    # дальний план: тополя и торец дальнего дома между корпусами
    d = f'<rect x="580" y="500" width="700" height="210" fill="#4a5262" opacity=".9" {o(5)}/>'
    for i in range(6):
        tx = 620 + i * 118
        d += (f'<ellipse cx="{tx:.0f}" cy="{640 - (i % 3) * 26:.0f}" rx="44"'
              f' ry="{104 + (i % 3) * 18:.0f}" fill="#33442f" opacity=".92" {o(4)}/>'
              f'<rect x="{tx-7:.0f}" y="{700 - (i % 3) * 26:.0f}" width="14" height="40" fill="#3a2a1c"/>')
    d += f'<rect y="700" width="{W}" height="36" fill="{TRAV68}" opacity=".9"/>'
    s += SL(Z_DAL, d)
    # ── средний план: двор
    m = f'<rect y="736" width="{W}" height="{H-736}" fill="{ASFALT}"/>'
    m += (f'<path d="M0,736 q480,22 960,8 q480,-16 960,10 L1920,860 L0,860 Z"'
          f' fill="{TRAV67}" opacity=".9"/>')
    for i in range(7):
        m += (f'<path d="M{-60+i*300:.0f},{880+i*22:.0f} q300,{18-i*4:.0f} 620,{-10:.0f}"'
              f' fill="none" stroke="{ASFALT2}" stroke-width="5" opacity=".45"/>')
    # бельевые столбы с верёвками
    for i, (bx, bh) in enumerate(((580, 250), (1030, 250))):
        m += ten(bx, 846, 44, 13, .5)
        m += (f'<rect x="{bx-13:.0f}" y="{846-bh:.0f}" width="26" height="{bh:.0f}"'
              f' rx="8" fill="url(#derev)" {o(6)}/>'
              f'<rect x="{bx-74:.0f}" y="{846-bh-16:.0f}" width="148" height="20" rx="8"'
              f' fill="url(#derev)" {o(5)}/>')
    for k, (y0, col) in enumerate(((618, "#eef1f3"), (660, "#dfe6ec"))):
        m += (f'<path d="M{516:.0f},{y0:.0f} Q815,{y0+46:.0f} 1094,{y0:.0f}" fill="none"'
              f' stroke="#cfd6dd" stroke-width="4"/>')
        for j in range(3):
            u = .22 + j * .28
            bx = 516 + 578 * u
            by = y0 + 46 * (4 * u * (1 - u)) * .92
            m += _belyo(bx, by, 86 - j * 8, 118 - k * 26,
                        ("#eef1f3", "#e7d9c2", "#cfd9e4", "#e9c7bd")[(j + k) % 4], t, j * .3 + k * .17)
    # стол для домино, два силуэта по сторонам, костяшка стучит
    m += baza.stol(560, 920, 300, 30)
    m += ob.figura(518, 1002, 236, t, "#242a33", "#f0c070", False, .2, True)
    m += ob.figura(902, 1002, 230, t, "#2a2420", "#f0c070", False, .7, True)
    r = random.Random(4)
    for i in range(7):
        dx = 576 + (i % 4) * 66 + (i // 4) * 30
        dy = 906 + (i // 4) * 16
        m += (f'<g transform="rotate({r.uniform(-14,14):.0f} {dx:.0f} {dy:.0f})">'
              f'<rect x="{dx-13:.0f}" y="{dy-22:.0f}" width="26" height="44" rx="5"'
              f' fill="#f3ecdc" {o(3)}/>'
              f'<line x1="{dx-11:.0f}" y1="{dy:.0f}" x2="{dx+11:.0f}" y2="{dy:.0f}" {o(2)}/>'
              f'<circle cx="{dx-4:.0f}" cy="{dy-11:.0f}" r="3" fill="{K}"/>'
              f'<circle cx="{dx+4:.0f}" cy="{dy+11:.0f}" r="3" fill="{K}"/></g>')
    stuk = max(0.0, math.sin(2 * math.pi * (t / .92))) ** 5
    m += (f'<g transform="translate(802,{900-44*stuk:.1f}) rotate({-16*stuk:.1f})">'
          f'<rect x="-14" y="-24" width="28" height="48" rx="6" fill="#fbf5e8" {o(4)}/>'
          f'<line x1="-12" y1="0" x2="12" y2="0" {o(3)}/>'
          f'<circle cx="-5" cy="-12" r="3.4" fill="{K}"/><circle cx="5" cy="-12" r="3.4" fill="{K}"/>'
          f'<circle cx="0" cy="13" r="3.4" fill="{K}"/></g>')
    m += (f'<ellipse cx="802" cy="916" rx="{26+16*stuk:.0f}" ry="7" fill="#000"'
          f' opacity="{.18+.2*stuk:.2f}"/>')
    # дети с мячом
    m += ob.figura(1216, 1000, 196, t, "#2b2733", "#f6cf8c", False, .1, False, 1.0, True)
    m += ob.figura(1452, 1004, 182, t, "#242d33", "#f6cf8c", False, .55)
    bu = abs(math.sin(math.pi * t / .64))
    by = 1012 - 250 * (bu ** .78)
    sq = 1.0 + .20 * (1 - bu) ** 2
    m += ten(1334, 1018, 46 * (1 + .35 * (1 - bu)), 13, .75 - .25 * bu)
    m += (f'<g transform="translate(1334,{by:.0f}) scale({sq:.2f},{2-sq:.2f})">'
          f'<circle r="38" fill="#e8e2d4" {o(6)}/>'
          f'<path d="M-38,-4 q38,22 76,0" fill="none" stroke="{ob.ALYJ}" stroke-width="11"/>'
          f'<path d="M-30,-22 q30,16 60,0" fill="none" stroke="{SINKA}" stroke-width="9"/>'
          f'<circle cx="-13" cy="-15" r="9" fill="#ffffff" opacity=".5"/></g>')
    s += SL(Z_SRED, m)
    # ── ближний угол дома с открытым окном: занавески и радиола
    p = f'<rect x="-40" y="150" width="420" height="{H-150}" fill="url(#beton)" {o(7)}/>'
    p += (f'<rect x="-40" y="150" width="420" height="{H-150}" fill="#1a2330" opacity=".22"/>')
    for i in range(4):
        p += (f'<line x1="-40" y1="{280+i*210:.0f}" x2="380" y2="{280+i*210:.0f}"'
              f' stroke="{BETON2}" stroke-width="5" opacity=".55"/>')
    ox, oy, ow, oh = 72, 420, 256, 240
    p += baza.okno_izby(ox, oy, ow, oh, t, None, 0.0, False, False)
    p += f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}" fill="#26303c" opacity=".88"/>'
    p += teplo(ox + ow * .62, oy + oh * .72, 150, 120, .75)
    p += (f'<rect x="{ox-6:.0f}" y="{oy-4:.0f}" width="{ow+12:.0f}" height="14" rx="6"'
          f' fill="{DOSKA2}" {o(4)}/>')
    p += baza.zanaveska(ox + 8, oy + 8, oh - 16, 68, "#ddd0b4", t, 1)
    p += baza.zanaveska(ox + ow - 8, oy + 8, oh - 16, 68, "#ddd0b4", t, -1)
    rx, ry = ox + ow * .50, oy + oh * .92
    p += (f'{ten(rx+8, ry+10, 100, 14, .45)}'
          f'<rect x="{rx-104:.0f}" y="{ry-104:.0f}" width="208" height="112" rx="12"'
          f' fill="url(#derev)" {o(6)}/>'
          f'<rect x="{rx-86:.0f}" y="{ry-88:.0f}" width="112" height="46" rx="8"'
          f' fill="{SVET}" opacity="{.66+.28*abs(A.w(t,2.6)):.2f}" {o(4)}/>')
    for i in range(5):
        p += (f'<line x1="{rx-78+i*22:.0f}" y1="{ry-86:.0f}" x2="{rx-78+i*22:.0f}"'
              f' y2="{ry-50:.0f}" stroke="#8c6b32" stroke-width="3" opacity=".7"/>')
    p += (f'<line x1="{rx-54:.0f}" y1="{ry-90:.0f}" x2="{rx-54:.0f}" y2="{ry-40:.0f}"'
          f' stroke="{KRAS}" stroke-width="5"/>'
          f'<circle cx="{rx+62:.0f}" cy="{ry-62:.0f}" r="22" fill="url(#zhel)" {o(5)}/>'
          f'<circle cx="{rx+62:.0f}" cy="{ry-62:.0f}" r="7" fill="{SVET}"/>'
          f'<rect x="{rx-86:.0f}" y="{ry-34:.0f}" width="170" height="16" rx="7"'
          f' fill="{DOSKA2}" opacity=".8"/>')
    p += teplo(rx, ry - 70, 210, 170, .7)
    p += (f'<rect x="{ox-14:.0f}" y="{oy+oh:.0f}" width="{ow+28:.0f}" height="22" rx="6"'
          f' fill="url(#beton)" {o(5)}/>')
    p += (f'<path d="M1790,1080 q-30,-220 60,-330 q90,120 70,330 Z" fill="{TRAV68}" {o(6)}/>'
          f'<path d="M1690,1080 q-18,-150 48,-230 q66,86 54,230 Z" fill="#35492a" {o(5)}/>')
    s += SL(Z_PERED, p)
    s += baza.vinetka(.40)
    return s


# ═══════════════════ ПЛАН 44 ═══════════════════

def kinoteatr_s_afishey(t):
    """Фасад кинотеатра с колоннами, над входом рисованная афиша (только
    название буквами и горы). Живое: лампочки вокруг афиши бегут, двери
    открываются, голуби ходят по карнизу. Окно вставки занимает 860-1840."""
    s = baza.nebo("den", t, False)
    s += baza.oblaka(t, 150, 5, 15, .5, "#eef3f8", 7.0)
    d = ""
    for i in range(7):
        bx = 760 + i * 190
        bh = 190 + (i % 3) * 70
        d += (f'<rect x="{bx:.0f}" y="{790-bh:.0f}" width="168" height="{bh:.0f}"'
              f' fill="#6a7788" opacity=".8" {o(4)}/>')
        for j in range(3):
            d += (f'<rect x="{bx+18+j*48:.0f}" y="{810-bh:.0f}" width="30" height="40" rx="4"'
                  f' fill="{SVET}" opacity="{.2+.25*abs(A.w(t,8+i,j*.3)):.2f}"/>')
    for i in range(9):
        d += (f'<ellipse cx="{60+i*230:.0f}" cy="{700+(i%2)*26:.0f}" rx="86" ry="110"'
              f' fill="#3c5235" opacity=".8"/>'
              f'<rect x="{52+i*230:.0f}" y="{790+(i%2)*26:.0f}" width="18" height="46" fill="#3a2a1c"/>')
    d += f'<rect y="836" width="{W}" height="36" fill="#7b8794" opacity=".75"/>'
    s += SL(Z_DAL, d)
    # ── фасад
    m = ten(420, 960, 460, 26, .5)
    m += (f'<rect x="-40" y="96" width="880" height="800" fill="url(#krem)" {o(8)}/>')
    m += (f'<rect x="-40" y="96" width="880" height="800" fill="{SHTUK2}" opacity=".30"/>')
    m += (f'<path d="M-60,120 L400,34 L860,120 Z" fill="{SHTUK}" {o(8)}/>'
          f'<path d="M-60,120 L400,34 L860,120 Z" fill="#8f8160" opacity=".22"/>')
    m += (f'<rect x="-50" y="118" width="900" height="34" rx="8" fill="{SHTUK2}" {o(6)}/>')
    # афиша над входом
    m += _afisha(84, 146, 640, 228, "Кавказская пленница", t, 54, 0.0, 5, True)
    # карниз с голубями
    m += (f'<rect x="-40" y="420" width="880" height="32" rx="8" fill="{SHTUK2}" {o(6)}/>'
          f'<rect x="-40" y="420" width="880" height="10" fill="#ffffff" opacity=".18"/>')
    for i, (gx, ph) in enumerate(((150, .0), (438, .4), (712, .75))):
        m += baza.ptica(gx, 416, t, .58, "#c3ccd6", ph, "#7d8894")
    # колонны
    for i, cx in enumerate((22, 196, 592, 766)):
        m += ten(cx + 38, 902, 56, 14, .45)
        m += (f'<rect x="{cx:.0f}" y="{444:.0f}" width="76" height="430" rx="10"'
              f' fill="url(#krem)" {o(6)}/>')
        for j in range(5):
            m += (f'<line x1="{cx+14+j*12:.0f}" y1="462" x2="{cx+14+j*12:.0f}" y2="862"'
                  f' stroke="{SHTUK2}" stroke-width="5" opacity=".75"/>')
        m += (f'<rect x="{cx-12:.0f}" y="{424:.0f}" width="100" height="26" rx="6" fill="{SHTUK}" {o(5)}/>'
              f'<rect x="{cx-12:.0f}" y="{868:.0f}" width="100" height="26" rx="6" fill="{SHTUK}" {o(5)}/>')
    # вход: тёмный портал и две створки, которые открываются
    m += f'<rect x="288" y="500" width="266" height="378" rx="10" fill="#1b1f27" {o(7)}/>'
    m += teplo(421, 700, 170, 200, .5)
    otk = .18 + .82 * (.5 + .5 * math.sin(2 * math.pi * (t / 3.4)))
    for sgn, bx in ((1, 288), (-1, 554)):
        m += (f'<g transform="translate({bx:.0f},500) scale({sgn*(1-otk*.72):.3f},1)">'
              f'<rect x="0" y="0" width="133" height="378" fill="url(#derev)" {o(6)}/>'
              f'<rect x="18" y="26" width="97" height="150" rx="6" fill="url(#stekl)" opacity=".7" {o(4)}/>'
              f'<circle cx="112" cy="220" r="9" fill="url(#zhel)" {o(3)}/></g>')
    # площадь и ступени
    m += f'<rect y="896" width="{W}" height="{H-896}" fill="#6e6f6c"/>'
    m += (f'<path d="M-20,916 q480,-22 960,-8 q480,14 980,16 L1940,1080 L-20,1080 Z"'
          f' fill="#7b7c78" opacity=".8"/>')
    for i in range(6):
        m += (f'<path d="M{-40+i*340:.0f},{990+i*16:.0f} q200,14 420,-8" fill="none"'
              f' stroke="#5f605d" stroke-width="5" opacity=".4"/>')
    for i in range(3):
        m += (f'<rect x="{196-i*34:.0f}" y="{878+i*22:.0f}" width="{452+i*68:.0f}" height="24"'
              f' rx="5" fill="{SHTUK2}" {o(5)}/>')
    s += SL(Z_SRED, m)
    # ── народ у входа
    p = ""
    for i, (fx, hh, kr, pl, ph) in enumerate(((118, 272, False, True, .1),
                                              (236, 286, True, False, .5),
                                              (640, 278, False, False, .8),
                                              (760, 292, False, True, .3))):
        p += ob.figura(fx, 1000, hh, t, "#272231", "#f3d2a0", pl, ph, False, 1.0, kr)
    p += baza.ramka_pp("levo", "#141008", .34)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.42)
    return s


# ═══════════════════ ПЛАН 45 ═══════════════════

def polnyy_zritelnyy_zal(t):
    """Зрительный зал со спины: все места заняты, над головами луч проектора,
    над залом наливается счётчик, над экраном встаёт пьедестал первого места.
    Живое: плечи трясутся от смеха, пылинки в луче, счётчик бежит."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#0e1118"/>'
           + f'<rect width="{W}" height="{H}" fill="#1a2030" opacity=".6"/>')
    # ── экран и занавес
    d = ""
    mig = .78 + .22 * (.5 + .5 * math.sin(2 * math.pi * (t * .9)) * math.sin(2 * math.pi * (t * .37)))
    d += f'<rect x="300" y="150" width="1320" height="470" rx="8" fill="#2a2b31" {o(8)}/>'
    d += (f'<rect x="336" y="182" width="1248" height="406" fill="#d2dbe6"'
          f' opacity="{.82*mig:.2f}"/>')
    d += (f'<rect x="336" y="182" width="1248" height="406" fill="{SVET}" opacity="{.26*mig:.2f}"/>')
    d += (f'<ellipse cx="960" cy="385" rx="560" ry="200" fill="#ffffff" opacity="{.22*mig:.2f}"/>')
    d += (f'<rect x="336" y="500" width="1248" height="88" fill="#6b7686" opacity=".30"/>')
    d += teplo(960, 390, 760, 330, .4 * mig)
    for i, bx in enumerate((150, 1620)):
        d += (f'<path d="M{bx:.0f},120 q60,260 0,540 l{-150 if i else 150:.0f},0'
              f' q-50,-280 0,-540 Z" fill="{BORDO}" {o(6)}/>')
        for j in range(5):
            d += (f'<path d="M{bx+(j*26-60 if i==0 else -j*26+60):.0f},130'
                  f' q{40 if i==0 else -40:.0f},260 0,520" fill="none" stroke="{BORDO2}"'
                  f' stroke-width="9" opacity=".7"/>')
    # пьедестал первого места встаёт над экраном
    vst = A.out(A.seg(t, 1.5, 1.1))
    if vst > .01:
        py = 232 - 136 * vst
        d += (f'<g opacity="{vst:.2f}"><g transform="translate(960,{py:.0f})">'
              f'{ten(0, 112, 150, 18, .5)}'
              f'<rect x="-168" y="54" width="110" height="60" rx="6" fill="url(#med)" {o(5)}/>'
              f'<rect x="58" y="76" width="110" height="38" rx="6" fill="url(#med)" {o(5)}/>'
              f'<rect x="-58" y="-6" width="116" height="120" rx="8" fill="url(#zol)" {o(6)}/>'
              f'<path d="M-44,-6 h88" stroke="#fff6cf" stroke-width="7" opacity=".55"/>'
              f'</g></g>')
        d += teplo(960, 170, 300, 180, .35 * vst)
    s += SL(Z_DAL, d)
    # ── счётчик над залом
    f_ = ""
    cx0, cw = 300, 1320
    nap = A.ease(min(1.0, t / 3.0))
    f_ += (f'<rect x="{cx0:.0f}" y="48" width="{cw:.0f}" height="46" rx="23"'
           f' fill="#1d222c" {o(5)}/>')
    f_ += (f'<rect x="{cx0+6:.0f}" y="54" width="{(cw-12)*nap:.0f}" height="34" rx="17"'
           f' fill="url(#zol)"/>')
    for i in range(22):
        u = i / 21.0
        gor = .25 + .75 * (1.0 if u <= nap else .0) * (.6 + .4 * abs(A.w(t, .6, i * .12)))
        f_ += (f'<rect x="{cx0+16+u*(cw-44):.0f}" y="{62:.0f}" width="6" height="18" rx="3"'
               f' fill="{SVET if u <= nap else "#555c68"}" opacity="{gor:.2f}"/>')
    f_ += (f'<circle cx="{cx0+6+(cw-12)*nap:.0f}" cy="71" r="18" fill="{SVET}"'
           f' opacity="{.55+.45*abs(A.w(t,.9)):.2f}" {o(4)}/>')
    s += SL(Z_SRED, f_)
    # ── луч проектора над головами
    b = ""
    b += (f'<path d="M2010,1150 L600,196 L1420,196 Z" fill="#cfe4ff" opacity=".16"/>'
          f'<path d="M2010,1150 L760,210 L1300,210 Z" fill="#eaf4ff" opacity=".16"/>'
          f'<path d="M2010,1150 L900,226 L1160,226 Z" fill="#ffffff" opacity=".13"/>')
    r = random.Random(17)
    for i in range(44):
        u = r.uniform(.04, 1.0)
        px = 2010 - u * (2010 - r.uniform(640, 1380))
        py = 1150 - u * (1150 - 200)
        b += (f'<circle cx="{px+22*A.w(t,6+i*.3,i*.11):.0f}" cy="{py+((t*9+i*17)%40)-20:.0f}"'
              f' r="{r.uniform(1.8,4.2):.1f}" fill="#fff6dd" opacity="{r.uniform(.3,.85):.2f}"/>')
    s += SL(Z_SRED, b)
    # ── ряды голов: дальние мелкие, ближние крупные
    z = ""
    for row, (yy, rr, n, col) in enumerate(((654, 26, 13, "#4b5478"),
                                            (726, 33, 11, "#404868"),
                                            (814, 41, 9, "#353c5a"))):
        rnd = random.Random(30 + row)
        for i in range(n):
            x = 120 + (W - 240) * (i + .5) / n + rnd.uniform(-16, 16)
            z += _golova(x, yy, rr, t, col, "#8fb4d8", i * .23 + row * .4, .9, 1.05)
    s += SL(Z_SRED, z)
    p = ""
    for row, (yy, rr, n, col) in enumerate(((926, 52, 7, "#2b3250"),
                                            (1068, 68, 6, "#222841"))):
        rnd = random.Random(60 + row)
        for i in range(n):
            x = 90 + (W - 180) * (i + .5) / n + rnd.uniform(-22, 22)
            p += _golova(x, yy, rr, t, col, "#9ec2e6", i * .31 + row * .6, 1.25, 1.1)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.5)
    return s


# ═══════════════════ ПЛАН 46 ═══════════════════

def dve_afishi_na_zabore(t):
    """Дощатый забор с двумя свежими афишами: только названия крупными
    буквами. Живое: кисть разглаживает вторую афишу, уголок первой
    отгибается, кот идёт по верхней планке забора."""
    s = baza.nebo("den", t, False)
    s += baza.oblaka(t, 196, 5, 31, .46, "#f1f5f9", 6.0)
    d = ""
    for i in range(5):
        bx = -60 + i * 430
        d += (f'<rect x="{bx:.0f}" y="300" width="300" height="180" fill="#5a6475" opacity=".75"/>'
              f'<path d="M{bx-24:.0f},300 L{bx+150:.0f},214 L{bx+324:.0f},300 Z"'
              f' fill="#49536a" opacity=".8"/>')
    for i in range(7):
        d += (f'<ellipse cx="{40+i*300:.0f}" cy="{360+(i%3)*22:.0f}" rx="96" ry="128"'
              f' fill="#3b5333" opacity=".8"/>')
    s += SL(Z_DAL, d)
    # ── забор
    m = ten(960, 1006, 900, 26, .45)
    m += baza.doski(-30, 400, 1990, 580, 78, True, "dosk")
    m += (f'<rect x="-30" y="368" width="1990" height="40" rx="8" fill="url(#derev)" {o(6)}/>')
    for yy in (560, 848):
        m += (f'<rect x="-30" y="{yy:.0f}" width="1990" height="30" fill="{DOSKA2}"'
              f' opacity=".8" {o(4)}/>')
    for bx in (120, 700, 1300, 1820):
        m += (f'<rect x="{bx-22:.0f}" y="352" width="44" height="640" rx="8"'
              f' fill="{DOSKA2}" {o(6)}/>')
    m += f'<rect y="968" width="{W}" height="24" fill="#4b4237" opacity=".8"/>'
    # афиша первая — с отгибающимся уголком
    otg = .35 + .65 * (.5 + .5 * math.sin(2 * math.pi * (t / 2.3)))
    m += _afisha(190, 470, 500, 330, "Свадьба в Малиновке", t, 60, otg, 7)
    # афиша вторая — её разглаживает кисть
    m += _afisha(1020, 456, 450, 348, "Вий", t, 128, 0.0, 12, False, True)
    # мокрый блик свежего клея под кистью
    ku = .5 + .5 * math.sin(2 * math.pi * (t / 1.9))
    kx = 1060 + 380 * ku
    ky = 640 + 110 * (.5 + .5 * math.sin(2 * math.pi * (t / 3.8)))
    m += (f'<ellipse cx="{kx:.0f}" cy="{ky+40:.0f}" rx="96" ry="54" fill="#ffffff"'
          f' opacity=".16"/>')
    m += (f'<g transform="translate({kx:.0f},{ky:.0f}) rotate({-24+16*ku:.1f})">'
          f'{ten(10, 36, 46, 11, .4)}'
          f'<rect x="-26" y="-6" width="52" height="56" rx="7" fill="#c9a86a" {o(5)}/>'
          f'<path d="M-30,46 h60 l-8,54 h-44 Z" fill="#8b7a5f" {o(5)}/>'
          f'<rect x="-15" y="-150" width="30" height="150" rx="10" fill="url(#derev)" {o(5)}/>'
          f'<path d="M-24,92 q24,18 48,0" fill="none" stroke="#e8eef4" stroke-width="7" opacity=".7"/></g>')
    # кот идёт по верхней планке
    kx2 = -40 + ((t * 78) % 2060)
    m += baza.kot(kx2, 372, t, .56, "#3a342f")
    s += SL(Z_SRED, m)
    # ── трава и лопухи переднего плана
    p = (f'<path d="M-20,1080 q180,-120 400,-96 q240,26 480,-40 q300,-80 560,-16'
         f' q300,74 520,-30 L1940,1080 Z" fill="{TRAV68}" {o(6)}/>')
    r = random.Random(23)
    for i in range(14):
        lx = r.uniform(-20, W + 20)
        ly = r.uniform(980, 1072)
        p += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{r.uniform(44,86):.0f}"'
              f' ry="{r.uniform(26,46):.0f}" fill="{TRAV67}" opacity=".85" {o(4)}/>')
    p += baza.ramka_pp("pravo", "#15190f", .30)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.4)
    return s


# ═══════════════════ ПЛАН 47 ═══════════════════

def ryad_kresel_smeh_i_strah(t):
    """Один ряд кресел лицом к зрителю, свет экрана на силуэтах. Слева
    взрослые хохочут и раскачиваются, справа трое детей закрылись
    программками, у одного программка отходит — он подглядывает в щель.
    Живое: взрослые хохочут, щель программки раздвигается, свет мигает."""
    mig = .70 + .30 * (.5 + .5 * math.sin(2 * math.pi * (t * 1.15))
                       * math.sin(2 * math.pi * (t * .43 + .2)))
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#0c0f16"/>')
    d = (f'<rect y="0" width="{W}" height="560" fill="#161c28"/>')
    for i in range(9):
        d += (f'<rect x="{-40+i*230:.0f}" y="0" width="140" height="560" rx="12"'
              f' fill="{BORDO2}" opacity=".5"/>')
    d += teplo(960, 240, 1100, 420, .26 * mig)
    for i, bx in enumerate((250, 700, 1200, 1660)):
        gor = .55 + .45 * abs(A.w(t, 5.4 + i, i * .2))
        d += (f'<path d="M{bx-44:.0f},300 q44,-54 88,0 q-44,34 -88,0 Z" fill="url(#zol)" {o(5)}/>'
              f'<rect x="{bx-9:.0f}" y="300" width="18" height="46" rx="6" fill="{MED}" {o(4)}/>')
        d += teplo(bx, 290, 150, 130, .5 * gor)
    for i, dx in enumerate((160, 560, 960, 1360, 1760)):
        gor = .5 + .5 * abs(A.w(t, 6.2 + i, i * .17))
        d += (f'<path d="M{dx:.0f},0 v54" stroke="{CHUGUN}" stroke-width="7"/>'
              f'<ellipse cx="{dx:.0f}" cy="76" rx="56" ry="26" fill="{KREM}"'
              f' opacity="{.45+.35*gor:.2f}" {o(5)}/>')
        d += teplo(dx, 86, 140, 110, .34 * gor)
    d += (f'<rect x="1700" y="150" width="190" height="400" rx="10" fill="#101620" {o(6)}/>'
          f'<rect x="1716" y="166" width="158" height="368" rx="8" fill="{BORDO2}" {o(4)}/>'
          f'<rect x="60" y="170" width="170" height="380" rx="10" fill="#101620" {o(6)}/>'
          f'<rect x="74" y="186" width="142" height="348" rx="8" fill="{BORDO2}" {o(4)}/>')
    d += (f'<rect y="540" width="{W}" height="40" fill="#1d2430" {o(4)}/>')
    s += SL(Z_DAL, d)
    # ── зрители сидят В креслах: сперва фигуры, кресла ложатся поверх
    m = ""
    # взрослые слева: корпус раскачивается от хохота
    for i, (fx, hh, kr, pl, ph) in enumerate(((160, 364, False, False, .0),
                                              (398, 348, False, True, .42),
                                              (636, 370, True, False, .8),
                                              (874, 354, False, False, .25))):  # noqa
        kach = 7.5 * A.w(t, .66, ph) + 3.2 * A.w(t, .33, ph * 1.4)
        col = "#2c3348" if i % 2 == 0 else "#434a66"
        m += (f'<g transform="rotate({kach:.2f} {fx:.0f} 782)">'
              + ob.figura(fx, 782, hh, t, col, "#dceeff", pl, ph, False, 1.0, kr)
              + f'</g>')
    # дети справа: вместо рук работает предмет — программка кинотеатра
    for i, (fx, hh, ph, otk) in enumerate(((1174, 300, .1, .0), (1412, 312, .5, .0),
                                           (1650, 294, .8, 1.0))):
        m += ob.figura(fx, 782, hh, t, "#4a5476", "#dceeff", False, ph)
        gy = 782 - hh * .74
        if otk < .5:
            kch = 2.4 * A.w(t, 2.4, ph)
            m += (f'<g transform="rotate({kch:.2f} {fx:.0f} {gy+70:.0f})">'
                  f'<rect x="{fx-62:.0f}" y="{gy+16:.0f}" width="124" height="120" rx="8"'
                  f' fill="{BUMAGA}" {o(5)}/>'
                  f'<path d="M{fx-44:.0f},{gy+46:.0f} h88 M{fx-44:.0f},{gy+74:.0f} h70"'
                  f' stroke="{SEPIA2}" stroke-width="6" opacity=".7"/></g>')
        else:
            # щель раздвигается: программка отходит, в зазор бьёт свет экрана
            sch = .18 + .82 * (.5 + .5 * math.sin(2 * math.pi * (t / 1.45)))
            a = -34 * sch
            m += (f'<g transform="rotate({a:.1f} {fx-60:.0f} {gy+72:.0f})">'
                  f'<rect x="{fx-62:.0f}" y="{gy+16:.0f}" width="124" height="120" rx="8"'
                  f' fill="{BUMAGA}" {o(5)}/>'
                  f'<path d="M{fx-44:.0f},{gy+46:.0f} h88 M{fx-44:.0f},{gy+74:.0f} h70"'
                  f' stroke="{SEPIA2}" stroke-width="6" opacity=".7"/></g>')
            # свет экрана бьёт В ЩЕЛЬ поверх программки — иначе приём не виден
            shch = 5 + 15 * sch
            for k in range(3):
                m += (f'<path d="M{fx-50:.0f},{gy+18-k*5:.0f} l{100:.0f},{-shch*.7:.0f}'
                      f' l0,{shch*(1-k*.3):.1f} l{-100:.0f},{shch*.7:.0f} Z"'
                      f' fill="#fff8e2" opacity="{(.75-k*.22)*(.3+.7*sch)*mig:.2f}"/>')
            m += teplo(fx, gy + 14, 70 + 40 * sch, 44, .5 * sch * mig)
            m += (f'<circle cx="{fx+16:.0f}" cy="{gy+12:.0f}" r="{4+3*sch:.1f}"'
                  f' fill="#fff6dd" opacity="{.5+.5*sch:.2f}"/>')
    # глухой низ ряда: без него тела просвечивают в щелях между креслами
    m += f'<rect y="668" width="{W}" height="{H-668}" fill="#131727"/>'
    # кресла ложатся поверх: из-за спинок видны головы и плечи — ряд сидит
    for i in range(8):
        m += _kreslo(32 + i * 238, 622, 222, 330)
    s += SL(Z_SRED, m)
    # ── спинки переднего ряда и мигающий свет экрана
    p = (f'<rect y="840" width="{W}" height="{H-840}" fill="#0a0d13"/>')
    for i in range(5):                        # спинки переднего ряда крупно
        p += (f'<rect x="{-120+i*430:.0f}" y="876" width="330" height="240" rx="64"'
              f' fill="#2a2030" {o(6)}/>'
              f'<rect x="{-80+i*430:.0f}" y="912" width="250" height="150" rx="48"'
              f' fill="{BORDO}" opacity=".45"/>'
              f'<path d="M{-70+i*430:.0f},904 q{120:.0f},-26 {240:.0f},0" fill="none"'
              f' stroke="#cfe4ff" stroke-width="5" opacity=".2"/>')
    for i in range(7):
        p += (f'<path d="M{-80+i*300:.0f},1080 q130,-180 260,0 Z" fill="#101520" {o(5)}/>')
    p += (f'<rect width="{W}" height="{H}" fill="#cfe4ff" opacity="{.09+.14*mig:.2f}"/>')
    p += teplo(960, 1080, 1200, 560, .3 * mig)
    p += baza.ramka_pp("oba", "#07090e", .5)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.52)
    return s


# ═══════════════════ ПЛАН 48 ═══════════════════

def budka_kinomehanika(t):
    """Будка киномеханика: проектор с двумя катушками, окошко в зал, на стене
    маленький календарь с красной рогатой хозяйкой. Живое: катушки
    вращаются, луч бьёт в окошко, календарь покачивается."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#161a22"/>')
    # ── стена будки с окошком в зал
    d = (f'<rect width="{W}" height="{H}" fill="#2c3240"/>')
    d += baza.kladka(-40, 60, 2000, 700, 86, "#3a4150")
    d += (f'<rect y="0" width="{W}" height="60" fill="#232936" {o(5)}/>')
    okx, oky, okw, okh = 980, 300, 230, 196
    d += (f'<rect x="{okx-34:.0f}" y="{oky-34:.0f}" width="{okw+68:.0f}" height="{okh+68:.0f}"'
          f' rx="10" fill="{CHUGUN}" {o(8)}/>')
    d += (f'<rect x="{okx-20:.0f}" y="{oky-20:.0f}" width="{okw+40:.0f}" height="{okh+40:.0f}"'
          f' rx="8" fill="url(#zhel)" {o(5)}/>')
    d += (f'<rect x="{okx-44:.0f}" y="{oky+okh+34:.0f}" width="{okw+88:.0f}" height="22"'
          f' rx="8" fill="url(#zhel)" {o(5)}/>')
    d += (f'<rect x="{okx:.0f}" y="{oky:.0f}" width="{okw:.0f}" height="{okh:.0f}"'
          f' fill="#8a6a2e" {o(5)}/>')
    puls = .72 + .28 * (.5 + .5 * math.sin(2 * math.pi * (t * 1.05)))
    d += (f'<rect x="{okx:.0f}" y="{oky:.0f}" width="{okw:.0f}" height="{okh:.0f}"'
          f' fill="{SVET}" opacity="{.58*puls:.2f}"/>')
    d += (f'<rect x="{okx+16:.0f}" y="{oky+14:.0f}" width="{okw-32:.0f}" height="{okh-28:.0f}"'
          f' fill="#fff6dd" opacity="{.45*puls:.2f}"/>')
    d += teplo(okx + okw / 2, oky + okh / 2, 280, 240, .6 * puls)
    # календарь на стене: красная рогатая хозяйка года, качается на гвозде
    kach = 2.6 * A.w(t, 3.6)
    kx, ky = 1450, 300
    d += (f'<g transform="rotate({kach:.2f} {kx:.0f} {ky:.0f})">'
          f'{ten(kx+10, ky+350, 110, 16, .45)}'
          f'<rect x="{kx-120:.0f}" y="{ky:.0f}" width="240" height="330" rx="10"'
          f' fill="{BUMAGA}" {o(6)}/>'
          f'<rect x="{kx-120:.0f}" y="{ky:.0f}" width="240" height="74" rx="10"'
          f' fill="{ob.ALYJ}" {o(5)}/>'
          f'<text x="{kx:.0f}" y="{ky+54:.0f}" text-anchor="middle" {SERIF} font-size="44"'
          f' font-weight="bold" fill="#fdf0d2">1967</text>')
    d += ob.koza_malaya(kx - 54, ky + 248, t, .30, .3)
    for i in range(4):
        d += (f'<path d="M{kx-96:.0f},{ky+272+i*16:.0f} h{192:.0f}" stroke="{SEPIA2}"'
              f' stroke-width="4" opacity=".45"/>')
    d += (f'<path d="M{kx:.0f},{ky-10:.0f} v-26" stroke="{ZHELEZ}" stroke-width="7"/>')
    d += f'<circle cx="{kx:.0f}" cy="{ky-10:.0f}" r="9" fill="url(#zhel)" {o(4)}/></g>'
    d += (f'<rect x="96" y="500" width="400" height="24" rx="8" fill="url(#derev)" {o(6)}/>'
          f'<path d="M140,524 l26,40 M444,524 l-26,40" {o(5)} fill="none"/>')
    for i in range(4):
        jx = 150 + i * 94
        d += (f'<ellipse cx="{jx:.0f}" cy="{470:.0f}" rx="42" ry="34" fill="url(#zhel)" {o(5)}/>'
              f'<ellipse cx="{jx:.0f}" cy="{462:.0f}" rx="24" ry="19" fill="{ZHELEZ}" opacity=".7"/>')
    d += (f'<rect x="120" y="640" width="340" height="22" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        jx = 180 + i * 104
        d += (f'<rect x="{jx-40:.0f}" y="{564:.0f}" width="80" height="76" rx="7"'
              f' fill="{CHUGUN}" {o(5)}/>'
              f'<path d="M{jx-30:.0f},{600:.0f} h60" stroke="{ZHELEZ}" stroke-width="6"/>')
    d += baza.hodiki(1740, 250, t, .9)
    d += (f'<rect x="1540" y="690" width="330" height="22" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        jx = 1600 + i * 104
        d += (f'<ellipse cx="{jx:.0f}" cy="{668:.0f}" rx="40" ry="32" fill="url(#zhel)" {o(5)}/>'
              f'<ellipse cx="{jx:.0f}" cy="{660:.0f}" rx="22" ry="17" fill="{ZHELEZ}" opacity=".7"/>')
    s += SL(Z_DAL, d)
    # ── луч от проектора в окошко
    b = (f'<path d="M806,700 L{okx:.0f},{oky+10:.0f} L{okx:.0f},{oky+okh-10:.0f} Z"'
         f' fill="{SVET}" opacity="{.26*puls:.2f}"/>'
         f'<path d="M806,700 L{okx:.0f},{oky+54:.0f} L{okx:.0f},{oky+okh-54:.0f} Z"'
         f' fill="#fff6dd" opacity="{.20*puls:.2f}"/>')
    r = random.Random(29)
    for i in range(26):
        u = r.uniform(.05, .98)
        bx = 806 + u * (okx - 806)
        by = 700 + u * ((oky + okh / 2) - 700) + r.uniform(-.5, .5) * u * okh * .8
        b += (f'<circle cx="{bx:.0f}" cy="{by+((t*11+i*23)%30)-15:.0f}"'
              f' r="{r.uniform(1.6,3.6):.1f}" fill="#fff6dd" opacity="{r.uniform(.3,.8):.2f}"/>')
    s += SL(Z_SRED, b)
    # ── проектор
    m = ten(420, 1006, 330, 28, .55)
    m += (f'<rect x="150" y="860" width="560" height="34" rx="8" fill="url(#chug)" {o(6)}/>'
          f'<rect x="206" y="894" width="46" height="130" rx="10" fill="url(#zhel)" {o(5)}/>'
          f'<rect x="600" y="894" width="46" height="130" rx="10" fill="url(#zhel)" {o(5)}/>'
          f'<rect x="170" y="1016" width="520" height="24" rx="8" fill="{CHUGUN}" {o(5)}/>')
    m += (f'<rect x="250" y="600" width="400" height="270" rx="22" fill="url(#chug)" {o(8)}/>'
          f'<rect x="286" y="636" width="140" height="106" rx="10" fill="{ZHELEZ}" opacity=".7" {o(4)}/>')
    m += (f'<rect x="628" y="660" width="112" height="86" rx="12" fill="url(#zhel)" {o(6)}/>'
          f'<circle cx="760" cy="703" r="48" fill="#1b1e24" {o(7)}/>'
          f'<circle cx="760" cy="703" r="30" fill="{SVET}" opacity="{.6+.4*puls:.2f}"/>'
          f'<circle cx="748" cy="692" r="10" fill="#ffffff" opacity=".7"/>')
    m += teplo(760, 703, 230, 190, .55 * puls)
    m += _katushka(330, 520, 118, t, 1.0)
    m += _katushka(560, 544, 96, t, -1.2)
    m += (f'<path d="M330,402 q118,-46 230,38" fill="none" stroke="{PLENKA}" stroke-width="13"/>'
          f'<path d="M330,402 q118,-46 230,38" fill="none" stroke="#54504a"'
          f' stroke-width="4" stroke-dasharray="7 11"/>')
    m += (f'<path d="M420,636 q60,-20 134,30" fill="none" stroke="{PLENKA}" stroke-width="11"/>')
    s += SL(Z_SRED, m)
    # ── ближний край стола с бобинами
    p = (f'<rect y="996" width="{W}" height="{H-996}" fill="#201f1e" {o(6)}/>')
    p += f'<rect y="988" width="{W}" height="18" fill="#35312c" {o(4)}/>'
    p += _katushka(1430, 1056, 118, t, .55, "#5a5f66")
    for i in range(3):                        # стопка жестянок рядом с бобиной
        p += (f'<ellipse cx="1760" cy="{1050-i*34:.0f}" rx="118" ry="40" fill="url(#zhel)" {o(6)}/>'
              f'<ellipse cx="1760" cy="{1042-i*34:.0f}" rx="74" ry="24" fill="{ZHELEZ}"'
              f' opacity=".65"/>')
    p += baza.ramka_pp("levo", "#0c0b0a", .4)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.48)
    return s


# ═══════════════════ ПЛАН 49 ═══════════════════

def kassa_i_lishniy_biletik(t):
    """Окошко кассы кинотеатра, очередь со спины в летних платьях, у входа над
    головой трепещет лишний билетик; во дворе за спиной мальчишки показывают
    сценку из кино, соседи смеются. Живое: очередь переступает, билетик
    трепещет, мальчишки размахивают. Окно вставки занимает 860-1840."""
    s = baza.nebo("zakat", t, False)
    s += baza.oblaka(t, 150, 4, 41, .4, "#f8e0bd", 5.0)
    # ── двор за кассой: сценка из кино и соседи-зрители
    d = ""
    for i in range(7):
        bx = 350 + i * 250
        bh = 240 + (i % 3) * 70
        d += (f'<rect x="{bx:.0f}" y="{748-bh:.0f}" width="214" height="{bh:.0f}"'
              f' fill="#5b6575" opacity=".82" {o(4)}/>')
        for j in range(2):
            d += (f'<rect x="{bx+28+j*104:.0f}" y="{774-bh:.0f}" width="72" height="62" rx="5"'
                  f' fill="{SVET}" opacity="{.24+.3*abs(A.w(t,7+i,j*.3)):.2f}" {o(3)}/>')
    for i in range(6):
        d += (f'<ellipse cx="{380+i*290:.0f}" cy="{660+(i%2)*22:.0f}" rx="68" ry="94"'
              f' fill="#3b5333" opacity=".8"/>')
    d += f'<rect y="744" width="{W}" height="152" fill="#6e7886" opacity=".8"/>'
    d += (f'<path d="M-20,792 q480,22 960,8 q480,-14 980,14 L1940,896 L-20,896 Z"'
          f' fill="#5f6a52" opacity=".75"/>')
    for i, (mx, ph) in enumerate(((432, .0), (524, .45), (614, .8))):
        rot = 15 * A.w(t, .8, ph)
        d += (f'<g transform="rotate({rot:.1f} {mx:.0f} 778)">'
              + ob.figura(mx, 778, 164, t, "#2a2535", "#f5d6a4", False, ph, False, .95)
              + f'<path d="M{mx-50:.0f},{692:.0f} q50,-44 100,0" fill="none"'
                f' stroke="#2a2535" stroke-width="13" stroke-linecap="round"/></g>')
    for i, (sx, pl) in enumerate(((706, True), (772, False), (830, True))):
        d += ob.figura(sx, 782, 150, t, "#262430", "#f5d6a4", pl, i * .3, False, .9)
    s += SL(Z_DAL, d)
    # ── стена кинотеатра с окошком кассы
    m = (f'<rect x="-40" y="100" width="380" height="980" fill="url(#krem)" {o(7)}/>')
    m += (f'<rect x="-40" y="100" width="380" height="980" fill="{SHTUK2}" opacity=".32"/>')
    m += (f'<rect x="-40" y="100" width="380" height="44" rx="8" fill="{SHTUK}" {o(5)}/>')
    m += (f'<path d="M-30,140 l150,300" stroke="#ffffff" stroke-width="22" opacity=".10"/>')
    kx, ky, kw, kh = 48, 544, 236, 198
    m += (f'<rect x="{kx-26:.0f}" y="{ky-26:.0f}" width="{kw+52:.0f}" height="{kh+52:.0f}"'
          f' rx="10" fill="url(#derev)" {o(7)}/>')
    m += f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw:.0f}" height="{kh:.0f}" fill="#1a1f28" {o(5)}/>'
    m += (f'<rect x="{kx:.0f}" y="{ky+kh*.50:.0f}" width="{kw:.0f}" height="{kh*.50:.0f}"'
          f' fill="{SVET}" opacity="{.5+.18*abs(A.w(t,4.0)):.2f}"/>')
    m += teplo(kx + kw * .5, ky + kh * .72, 210, 170, .7)
    for i in range(4):
        m += (f'<rect x="{kx+16+i*58:.0f}" y="{ky-6:.0f}" width="13" height="{kh*.46:.0f}"'
              f' rx="6" fill="url(#zhel)" {o(3)}/>')
    m += (f'<rect x="{kx-36:.0f}" y="{ky+kh:.0f}" width="{kw+72:.0f}" height="28" rx="7"'
          f' fill="url(#derev)" {o(6)}/>')
    for i in range(4):                       # синие билетики на полочке кассы
        m += (f'<rect x="{kx+18+i*54:.0f}" y="{ky+kh+4:.0f}" width="48" height="23" rx="4"'
              f' fill="{SINKA}" {o(3)}'
              f' transform="rotate({-8+i*5},{kx+42+i*54:.0f},{ky+kh+15:.0f})"/>')
    # ── тротуар на всю ширину: под окном вставки не должно быть пусто
    m += f'<rect y="868" width="{W}" height="{H-868}" fill="#6f6c64"/>'
    m += f'<rect y="856" width="{W}" height="20" fill="#86826f" {o(4)}/>'
    m += (f'<path d="M-20,906 q480,-20 960,-8 q480,12 980,14 L1940,1080 L-20,1080 Z"'
          f' fill="#7d7a70" opacity=".82"/>')
    for i in range(7):
        m += (f'<path d="M{-40+i*300:.0f},{972+i*12:.0f} q160,12 330,-8" fill="none"'
              f' stroke="#5e5b53" stroke-width="5" opacity=".4"/>')
    # ── очередь со спины: переступает с ноги на ногу
    for i, (fx, hh, pl, kr, ph) in enumerate(((352, 282, True, False, .0),
                                              (474, 294, False, True, .33),
                                              (596, 306, True, False, .66),
                                              (716, 318, False, False, .18))):
        per = 7 * A.w(t, 1.35, ph)
        col = "#241f30" if i % 2 == 0 else "#6a5f82"
        m += (f'<g transform="translate({per:.1f},{-abs(per)*.35:.1f})">'
              + ob.figura(fx, 1014, hh, t, col, "#ffe4b4", pl, ph, False, 1.0, kr)
              + '</g>')
    # парень у входа: лишний билетик над головой трепещет
    m += ob.figura(788, 1020, 344, t, "#242c36", "#f6d6a0", False, .5)
    bx, by = 788, 1020 - 344 * .96
    trep = 12 * A.w(t, .42) + 5 * A.w(t, .19, .3)
    m += (f'<g transform="rotate({trep:.1f} {bx:.0f} {by+40:.0f})">'
          f'<path d="M{bx:.0f},{by-18:.0f} v46" stroke="{SINKA}" stroke-width="8"/>'
          f'<rect x="{bx-42:.0f}" y="{by-78:.0f}" width="84" height="54" rx="6"'
          f' fill="{SINKA}" {o(5)}/>'
          f'<path d="M{bx-28:.0f},{by-62:.0f} h56 M{bx-28:.0f},{by-44:.0f} h38"'
          f' stroke="#cfe0f2" stroke-width="6" opacity=".85"/>'
          f'<circle cx="{bx+26:.0f}" cy="{by-42:.0f}" r="7" fill="{SVET}" opacity=".8"/></g>')
    s += SL(Z_SRED, m)
    p = (f'<path d="M-20,1080 q150,-104 340,-70 L320,1080 Z" fill="#43502f" {o(5)}/>'
         f'<path d="M1740,1080 q-36,-190 60,-266 q96,98 76,266 Z" fill="#3d4d2d" {o(5)}/>')
    p += baza.ramka_pp("levo", "#150f0a", .3)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.42)
    return s


# ═══════════════════ ПЛАН 50 ═══════════════════

def ulica_idet_v_kino(t):
    """Вечерняя улица частных домов: из калиток выходят нарядные люди и
    собираются в одну весёлую колонну, бабушки под руку, дети впереди. Живое:
    калитки хлопают, дети бегут впереди, подолы платьев колышутся на ходу."""
    s = baza.nebo("zakat", t, False)
    s += baza.oblaka(t, 170, 5, 51, .44, "#f9ddb6", 5.0)
    d = ""
    for i in range(6):
        bx = -60 + i * 360
        d += (f'<rect x="{bx:.0f}" y="440" width="250" height="180" fill="#4c566a"'
              f' opacity=".7"/>'
              f'<path d="M{bx-20:.0f},440 L{bx+125:.0f},364 L{bx+270:.0f},440 Z"'
              f' fill="#404a60" opacity=".75"/>')
    for i in range(8):
        tx = -20 + i * 270
        d += (f'<ellipse cx="{tx:.0f}" cy="{450+(i%3)*26:.0f}" rx="76"'
              f' ry="{114+(i%3)*18:.0f}" fill="#2f4630" opacity=".88"/>'
              f'<rect x="{tx-9:.0f}" y="{548+(i%3)*26:.0f}" width="18" height="70"'
              f' fill="#33261a"/>')
    s += SL(Z_DAL, d)
    # ── дома и штакетник с калитками
    # глухая зелень за штакетником: без неё в просветы между усадьбами
    # светит небо и дома читаются навесами на пустом каркасе
    m = f'<rect y="560" width="{W}" height="260" fill="#2c3f2d"/>'
    r0 = random.Random(31)
    for i in range(22):
        m += (f'<ellipse cx="{-40+i*92:.0f}" cy="{r0.uniform(596,700):.0f}"'
              f' rx="{r0.uniform(62,96):.0f}" ry="{r0.uniform(48,74):.0f}"'
              f' fill="{"#36502f" if i % 2 else "#2a4228"}" opacity=".95"/>')
    for i, (hx, hw, seed, dy) in enumerate(((-150, 490, 2, 0), (330, 440, 5, 22),
                                            (750, 460, 8, -12), (1160, 440, 11, 18),
                                            (1560, 500, 14, -6))):
        m += _dom67(hx, 792 + dy, hw * .80, t, seed, i % 2 == 0)
    m += (f'<rect x="-30" y="748" width="1990" height="22" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(44):
        sx = -30 + i * 46
        m += (f'<rect x="{sx:.0f}" y="664" width="22" height="100" rx="6"'
              f' fill="url(#dosk)" {o(4)}/>')
    m += (f'<rect x="-30" y="690" width="1990" height="14" fill="{DOSKA2}" opacity=".75"/>')
    for i in range(5):                        # калитки хлопают
        gx = 150 + i * 430
        hlop = max(0.0, math.sin(2 * math.pi * (t / 2.6 + i * .19))) ** 2
        m += f'<rect x="{gx-6:.0f}" y="650" width="152" height="124" fill="#4a4336" opacity=".5"/>'
        m += (f'<g transform="translate({gx:.0f},650) scale({1-hlop*.74:.3f},1)">'
              f'<rect x="0" y="0" width="140" height="124" rx="8" fill="url(#derev)" {o(6)}/>'
              f'<path d="M8,22 h124 M8,62 h124 M8,102 h124" stroke="{DOSKA2}" stroke-width="8"/>'
              f'<circle cx="122" cy="68" r="9" fill="url(#zhel)" {o(3)}/></g>')
    m += (f'<rect y="764" width="{W}" height="{H-764}" fill="#6a6256"/>')
    m += (f'<path d="M-20,800 q480,32 960,10 q480,-22 980,16 L1940,1080 L-20,1080 Z"'
          f' fill="#787063" opacity=".85"/>')
    for i in range(8):
        m += (f'<path d="M{-60+i*260:.0f},{916+i*14:.0f} q180,16 360,-8" fill="none"'
              f' stroke="#5d5549" stroke-width="5" opacity=".45"/>')
    s += SL(Z_SRED, m)
    # ── колонна: бабушки под руку, нарядные, дети впереди
    p = ""
    hod = (t * 30.0) % 220
    for i, (fx, hh, pl, kr, ph) in enumerate(((228, 322, True, False, .0),
                                              (316, 316, True, True, .3),
                                              (486, 336, False, False, .55),
                                              (578, 330, False, True, .15),
                                              (742, 326, True, False, .75),
                                              (938, 340, False, False, .4))):
        x = fx + hod * .5
        p += ob.figura(x, 1024, hh, t, "#2a2334" if i % 2 == 0 else "#473c58",
                       "#ffe0ab", pl, ph, False, 1.0, kr)
        pod = 8 * A.w(t, .7, ph)                 # подол колышется на ходу
        hip = 1024 - hh * .40
        p += (f'<path d="M{x-hh*.145:.0f},{hip:.0f} q{hh*.145:.0f},{12+pod:.0f}'
              f' {hh*.29:.0f},0 l{hh*.025:.0f},{hh*.40:.0f}'
              f' q{-hh*.17:.0f},{16-pod:.0f} {-hh*.34:.0f},0 Z"'
              f' fill="{ob.ALYJ2 if kr else "#352e46"}" {o(4)}/>')
        p += (f'<path d="M{x-hh*.17:.0f},{1024:.0f} q{hh*.17:.0f},{16-pod:.0f} {hh*.34:.0f},0"'
              f' fill="none" stroke="#f8d8a2" stroke-width="4" opacity=".45"/>')
    for i, (bx, hh, ph) in enumerate(((1272, 206, .0), (1420, 192, .5))):
        beg = 96 * ((t * .42 + i * .2) % 1.0)
        pr = abs(math.sin(math.pi * (t * 2.4 + i * .5))) * 20
        p += ob.figura(bx + beg, 1030 - pr, hh, t, "#2d2838", "#ffd79a", False, ph,
                       False, 1.0, i == 0)
        p += ten(bx + beg, 1032, 42, 11, .45)
    s += SL(Z_PERED, p)
    s += SL(Z_PERED, baza._ramka_pp("pravo", "#160f0a", .32))
    s += baza.vinetka(.42)
    return s


# ═══════════════════ ПЛАН 51 ═══════════════════

def tetradka_pesennik(t):
    """Тетрадка-песенник в клеёнчатой обложке крупно: ручка выводит строчки
    волнистыми линиями, на поля ложится вырезанный цветок. За ней — стол,
    над тарелками плывёт вторая тетрадка, которую передают из рук в руки."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#1b2130"/>'
           + f'<rect width="{W}" height="{H}" fill="#2b2436" opacity=".6"/>')
    # ── комната и праздничный стол на дальнем плане
    d = f'<rect x="860" y="0" width="{W-860}" height="760" fill="#3a2f44"/>'
    for i in range(9):
        d += (f'<rect x="{880+i*120:.0f}" y="0" width="52" height="760" fill="#48384f"'
              f' opacity=".7"/>')
    d += f'<rect x="860" y="744" width="{W-860}" height="26" fill="#2b2434" {o(5)}/>'
    d += baza.lampa(1360, 300, t, 1.0, True)
    d += teplo(1360, 420, 620, 460, .55)
    # люди за столом: сперва фигуры, столешница ложится поверх — они СИДЯТ
    for i, (fx, hh, pl, ph) in enumerate(((1010, 320, True, .1), (1290, 330, False, .5),
                                          (1620, 324, True, .8))):
        d += ob.figura(fx, 582, hh, t, "#2a2436", "#f0c070", pl, ph, False, .95)
    d += ob.stol_prazdnik(900, 540, 1020, t)
    for i, (px, r_) in enumerate(((1020, 60), (1176, 54), (1332, 58), (1492, 52), (1646, 56))):
        d += (f'<ellipse cx="{px:.0f}" cy="538" rx="{r_:.0f}" ry="{r_*.34:.0f}"'
              f' fill="#f2ead8" {o(4)}/>'
              f'<ellipse cx="{px:.0f}" cy="534" rx="{r_*.62:.0f}" ry="{r_*.2:.0f}"'
              f' fill="{MED}" opacity=".55"/>'
              f'<ellipse cx="{px-r_*.20:.0f}" cy="530" rx="{r_*.26:.0f}"'
              f' ry="{r_*.13:.0f}" fill="{ob.ALYJ2}" opacity=".85"/>'
              f'<ellipse cx="{px+r_*.22:.0f}" cy="532" rx="{r_*.22:.0f}"'
              f' ry="{r_*.11:.0f}" fill="{ZEL2}" opacity=".85"/>')
    d += baza.svecha(1790, 430, t, .2, 1.0, 92)
    d += ob.bokal(1716, 544, t, .66, .3)
    s += SL(Z_DAL, d)
    # ── тетрадка плывёт над столом из рук в руки
    u = (t * .26) % 1.0
    tx = 980 + 760 * A.ease(u)
    ty = 470 - 60 * math.sin(math.pi * u)
    m = (f'<g transform="translate({tx:.0f},{ty:.0f}) rotate({-8+16*u:.1f})">'
         f'{ten(10, 54, 86, 14, .5)}'
         f'<rect x="-84" y="-58" width="168" height="112" rx="8" fill="{SINKA}" {o(5)}/>'
         f'<rect x="-70" y="-46" width="140" height="88" rx="5" fill="#eae3cf" opacity=".9"/>'
         f'<path d="M-56,-24 h112 M-56,0 h96 M-56,22 h112" stroke="#8d9bb0" stroke-width="5"/>'
         f'</g>')
    s += SL(Z_SRED, m)
    # ── тетрадка крупно, на столе
    p = (f'<path d="M-40,1080 q60,-150 300,-168 q420,-28 740,8 L1000,1080 Z"'
         f' fill="url(#derev)" {o(7)}/>')
    p += (f'<path d="M-40,938 q320,-40 700,-16" fill="none" stroke="#b78a52"'
          f' stroke-width="9" opacity=".5"/>')
    p += ten(470, 1006, 420, 34, .55)
    p += (f'<g transform="rotate(-3 470 700)">'
          f'<rect x="60" y="300" width="840" height="680" rx="18" fill="{SINKA}" {o(8)}/>'
          f'<rect x="60" y="300" width="840" height="680" rx="18" fill="#101a2a" opacity=".25"/>'
          f'<path d="M96,340 l240,420" stroke="#ffffff" stroke-width="22" opacity=".10"/>'
          f'<rect x="92" y="330" width="776" height="620" rx="10" fill="#f3eddb" {o(5)}/>')
    # клетка
    for i in range(13):
        p += (f'<line x1="{120+i*58:.0f}" y1="340" x2="{120+i*58:.0f}" y2="940"'
              f' stroke="#b9c8d6" stroke-width="2.5" opacity=".7"/>')
    for i in range(11):
        p += (f'<line x1="104" y1="{368+i*58:.0f}" x2="856" y2="{368+i*58:.0f}"'
              f' stroke="#b9c8d6" stroke-width="2.5" opacity=".7"/>')
    p += f'<line x1="186" y1="330" x2="186" y2="950" stroke="{KRAS}" stroke-width="4" opacity=".7"/>'
    # строчки появляются одна за другой, ручка идёт по последней
    nstrok = 6
    r = random.Random(7)
    volny = []
    for i in range(nstrok):
        y0 = 410 + i * 86
        volny.append((y0, r.uniform(.8, 1.3)))
    put = min(1.0, t / 2.4) * nstrok
    for i, (y0, am) in enumerate(volny):
        dolya = max(0.0, min(1.0, put - i))
        if dolya <= 0:
            continue
        shir = (600 if i % 2 == 0 else 520) * dolya
        d_ = f'M210,{y0:.0f}'
        n = 9
        for j in range(n):
            xx = 210 + shir * (j + 1) / n
            d_ += f' q{shir/n/2:.0f},{(-17 if j % 2 == 0 else 17)*am:.0f} {shir/n:.0f},0'
        p += f'<path d="{d_}" fill="none" stroke="#1f2a44" stroke-width="7" stroke-linecap="round"/>'
    # ручка над концом последней строки
    ai = min(nstrok - 1, int(put))
    ay = volny[ai][0]
    ax = 210 + (600 if ai % 2 == 0 else 520) * max(0.0, min(1.0, put - ai))
    p += (f'<g transform="translate({ax:.0f},{ay:.0f}) rotate({34+3*A.w(t,.5):.1f})">'
          f'<path d="M0,0 l14,-34 l-28,0 Z" fill="{CHUGUN}" {o(3)}/>'
          f'<rect x="-15" y="-250" width="30" height="218" rx="12" fill="{ob.ALYJ2}" {o(5)}/>'
          f'<rect x="-15" y="-250" width="12" height="218" rx="6" fill="#ffffff" opacity=".18"/>'
          f'<rect x="-18" y="-66" width="36" height="34" rx="6" fill="url(#zol)" {o(4)}/></g>')
    # вырезанный цветок приклеивается на поля
    pk = A.over(A.seg(t, 1.1, .9))
    fx, fy = 134, 690
    p += (f'<g transform="translate({fx:.0f},{fy:.0f}) scale({pk:.3f}) rotate({18*(1-pk)+4*A.w(t,5.0):.1f})"'
          f' opacity="{min(1.0, pk*1.3):.2f}">')
    for i in range(6):
        a = i * 60
        p += (f'<ellipse cx="0" cy="-34" rx="17" ry="30" fill="{ob.ALYJ}" {o(3)}'
              f' transform="rotate({a})"/>')
    p += f'<circle r="15" fill="url(#zol)" {o(3)}/></g>'
    pk2 = A.over(A.seg(t, 2.4, .9))
    if pk2 > .01:
        p += (f'<g transform="translate(140,838) scale({pk2*.78:.3f})"'
              f' opacity="{min(1.0, pk2*1.3):.2f}">')
        for i in range(6):
            p += (f'<ellipse cx="0" cy="-34" rx="17" ry="30" fill="{ZOL}" {o(3)}'
                  f' transform="rotate({i*60})"/>')
        p += f'<circle r="15" fill="{ob.ALYJ}" {o(3)}/></g>'
    p += '</g>'
    s += SL(Z_PERED, p)
    s += SL(Z_PERED, baza._ramka_pp("pravo", "#120e14", .26))
    s += baza.vinetka(.46)
    return s


# ═══════════════════ ПЛАН 52 ═══════════════════

def malchik_s_samokatom_i_devushka_s_k(t):
    """У стены кинотеатра рядом стоят мальчик с самодельным самокатом и
    девушка в платье в горошек. Живое: самокат катается туда-сюда, подол в
    горошек колышется, над обоими всплывают золотые кружки под цифры."""
    s = baza.nebo("den", t, False)
    s += baza.oblaka(t, 140, 4, 61, .4, "#eef4f9", 6.0)
    # ── дальний план: афишная тумба и тополя
    d = (f'<rect x="1430" y="300" width="500" height="630" fill="#60697a" opacity=".75" {o(4)}/>')
    for e in range(3):
        for c in range(3):
            d += (f'<rect x="{1466+c*150:.0f}" y="{340+e*150:.0f}" width="92" height="94" rx="5"'
                  f' fill="{SVET}" opacity="{.18+.26*abs(A.w(t,8+e,c*.3)):.2f}" {o(3)}/>')
    d += (f'<rect x="1410" y="276" width="540" height="34" rx="8" fill="#4e5666" {o(4)}/>')
    d += ten(1300, 834, 110, 20, .45)
    d += (f'<rect x="1222" y="470" width="156" height="364" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<ellipse cx="1300" cy="470" rx="92" ry="26" fill="{DOSKA2}" {o(5)}/>'
          f'<rect x="1238" y="512" width="124" height="190" rx="6" fill="{BUMAGA}" {o(4)}/>'
          f'<path d="M1252,560 h96 M1252,600 h78 M1252,640 h96" stroke="{SEPIA2}"'
          f' stroke-width="7" opacity=".6"/>')
    for i in range(4):
        d += (f'<ellipse cx="{1520+i*150:.0f}" cy="{380+(i%2)*26:.0f}" rx="74" ry="104"'
              f' fill="#3b5333" opacity=".75"/>')
    s += SL(Z_DAL, d)
    # ── стена кинотеатра
    m = (f'<rect x="-40" y="120" width="1300" height="780" fill="url(#krem)" {o(7)}/>'
         f'<rect x="-40" y="120" width="1300" height="780" fill="{SHTUK2}" opacity=".28"/>'
         f'<rect x="-40" y="120" width="1300" height="38" rx="8" fill="{SHTUK}" {o(5)}/>')
    for i in range(4):
        m += (f'<rect x="{40+i*300:.0f}" y="240" width="190" height="300" rx="8"'
              f' fill="#2d3a46" opacity=".5" {o(5)}/>'
              f'<path d="M{48+i*300:.0f},252 l60,120" stroke="#ffffff" stroke-width="12" opacity=".16"/>')
    m += (f'<rect x="-40" y="866" width="1300" height="58" rx="8" fill="{SHTUK2}" {o(6)}/>')
    m += f'<rect y="918" width="{W}" height="{H-918}" fill="#73695d"/>'
    m += (f'<path d="M-20,940 q960,-30 1940,0 L1920,1080 L0,1080 Z" fill="#80766a" opacity=".8"/>')
    m += (f'<path d="M-20,962 q480,-14 960,-6 q480,8 980,10" fill="none" stroke="#5f574c"'
          f' stroke-width="5" opacity=".45"/>')
    s += SL(Z_SRED, m)
    # ── мальчик с самодельным самокатом: катается туда-сюда
    p = ""
    kat = 150 * math.sin(2 * math.pi * (t / 2.9))
    mx = 430 + kat
    p += ob.figura(mx - 46, 1012, 310, t, "#2b3242", "#f3d79f", False, .2, True)
    p += ten(mx + 40, 1024, 134, 16, .5)
    p += (f'<g transform="translate({mx:.0f},1016)">'
          f'<rect x="-104" y="-26" width="288" height="26" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="-104" y="-26" width="288" height="9" fill="#ffffff" opacity=".16"/>'
          f'<rect x="142" y="-230" width="24" height="208" rx="9" fill="url(#derev)" {o(5)}/>'
          f'<rect x="86" y="-244" width="136" height="22" rx="10" fill="url(#derev)" {o(5)}/>'
          f'<path d="M92,-236 q62,-14 124,0" fill="none" stroke="{ob.ALYJ}" stroke-width="10"/>'
          f'<path d="M154,-222 L-66,-26" fill="none" stroke="{DOSKA2}" stroke-width="12"/>'
          f'<circle cx="-82" cy="8" r="28" fill="{CHUGUN}" {o(5)}/>'
          f'<circle cx="-82" cy="8" r="9" fill="{ZHELEZ}"/>'
          f'<circle cx="162" cy="8" r="28" fill="{CHUGUN}" {o(5)}/>'
          f'<circle cx="162" cy="8" r="9" fill="{ZHELEZ}"/></g>')
    # ── девушка лет двадцати в платье в горошек, коса через плечо
    gx, gh, gb = 1110, 392, 1018
    p += ob.figura(gx, gb, gh, t, "#b04a52", "#ffe0ae", False, .6)
    pod = 11 * A.w(t, 1.9)
    hip = gb - gh * .44
    p += (f'<path d="M{gx-gh*.15:.0f},{hip:.0f} q{gh*.15:.0f},{14+pod:.0f} {gh*.30:.0f},0'
          f' l{gh*.04:.0f},{gh*.44:.0f} q{-gh*.19:.0f},{18-pod:.0f} {-gh*.38:.0f},0 Z"'
          f' fill="#c75f68" {o(5)}/>')
    r = random.Random(3)
    for i in range(20):                      # горошек по подолу
        u = r.uniform(0, 1); v = r.uniform(0, 1)
        dx = (gh * .15 + gh * .04 * v) * r.uniform(-1, 1)
        dy = hip + gh * .44 * v
        p += (f'<circle cx="{gx+dx+pod*.12*v:.1f}" cy="{dy:.0f}" r="7" fill="#f8ece0"'
              f' opacity=".92"/>')
    p += (f'<path d="M{gx-gh*.14:.0f},{hip+18:.0f} q{gh*.14:.0f},{16-pod:.0f} {gh*.28:.0f},0"'
          f' fill="none" stroke="#ffe0ae" stroke-width="5" opacity=".5"/>')
    # коса: от ВИСКА вниз по плечу, к концу тоньше, на конце бант
    for k, (wd, t0, t1) in enumerate(((22, .00, .34), (17, .30, .60), (12, .56, .82))):
        p += (f'<path d="M{gx-gh*(.12+.015*k):.0f},{gb-gh*(.80-.22*t0):.0f}'
              f' q{-gh*.05:.0f},{gh*.12:.0f} {gh*.012:.0f},{gh*(.22*(t1-t0)+.04):.0f}"'
              f' fill="none" stroke="{"#7a5733" if k % 2 == 0 else "#64462a"}"'
              f' stroke-width="{wd}" stroke-linecap="round"/>')
    bx_ = gx - gh * .13
    by_ = gb - gh * .80 + gh * .26
    p += (f'<path d="M{bx_-16:.0f},{by_:.0f} q16,-16 32,0 q-16,16 -32,0 Z" fill="{ob.ALYJ}" {o(4)}/>'
          f'<circle cx="{bx_:.0f}" cy="{by_:.0f}" r="6" fill="{ob.ALYJ2}"/>')
    # ── золотые кружки под цифры возраста всплывают над обоими
    for i, (cx, t0) in enumerate(((mx + 20, .4), (gx, 1.0))):
        vs = A.out(A.seg(t, t0, .8))
        if vs <= .01:
            continue
        cy = 640 - 110 * vs - 16 * A.w(t, 2.6, i * .4)
        p += (f'<g opacity="{vs:.2f}">{teplo(cx, cy, 160, 160, .5)}'
              f'<path d="M{cx:.0f},{cy+66:.0f} v{(1 if i else 1)*96:.0f}" stroke="url(#zol)"'
              f' stroke-width="5" stroke-dasharray="10 9" opacity=".8"/>'
              f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{70*vs:.0f}" fill="url(#zol)" {o(6)}/>'
              f'<circle cx="{cx-22:.0f}" cy="{cy-24:.0f}" r="{17*vs:.0f}" fill="#fff6cf"'
              f' opacity=".6"/></g>')
    s += SL(Z_PERED, p)
    s += SL(Z_PERED, baza._ramka_pp("levo", "#141009", .28))
    s += baza.vinetka(.4)
    return s


# ═══════════════════ ПЛАН 53 ═══════════════════

def kolyaska_i_yubileynyy_pirog(t):
    """Низкая коляска шестидесятых у подъезда с торчащей погремушкой на глазах
    становится столом с именинным пирогом, на пироге шестьдесят из свечек.
    Живое: погремушка качается, коляска превращается в стол, свечки загораются."""
    s = baza.nebo("zakat", t, False)
    s += baza.oblaka(t, 190, 4, 71, .4, "#f6dcba", 5.0)
    # ── подъезд
    d = (f'<rect x="-60" y="60" width="2040" height="760" fill="url(#beton)" {o(7)}/>')
    for i in range(5):
        d += (f'<line x1="-60" y1="{170+i*150:.0f}" x2="1980" y2="{170+i*150:.0f}"'
              f' stroke="{BETON2}" stroke-width="6" opacity=".5"/>')
    for e, oy in enumerate((160, 420, 640)):
        for i in range(6):
            ox_ = 120 + i * 300
            if oy > 380 and 640 < ox_ < 1180:
                continue                      # над козырьком подъезда окон нет
            on = (i + e) % 2 == 0
            d += (f'<rect x="{ox_:.0f}" y="{oy:.0f}" width="152" height="122" rx="6"'
                  f' fill="{SVET if on else "#49596a"}"'
                  f' opacity="{(.4+.35*abs(A.w(t,8+i+e,i*.2))) if on else .3:.2f}" {o(4)}/>'
                  f'<line x1="{ox_+76:.0f}" y1="{oy:.0f}" x2="{ox_+76:.0f}" y2="{oy+122:.0f}"'
                  f' stroke="{BETON2}" stroke-width="7"/>')
    d += (f'<rect x="700" y="420" width="470" height="420" rx="10" fill="#1d2430" {o(7)}/>'
          f'<rect x="676" y="376" width="518" height="56" rx="10" fill="{BETON2}" {o(6)}/>')
    for bx in (420, 1120):                   # балконы по сторонам подъезда
        for i in range(3):
            by = 302 + i * 260
            d += (f'<rect x="{bx:.0f}" y="{by:.0f}" width="230" height="26" rx="7"'
                  f' fill="{BETON2}" {o(5)}/>')
            for k in range(7):
                d += (f'<line x1="{bx+14+k*34:.0f}" y1="{by:.0f}" x2="{bx+14+k*34:.0f}"'
                      f' y2="{by-70:.0f}" stroke="{BETON2}" stroke-width="6"/>')
            d += (f'<rect x="{bx-4:.0f}" y="{by-78:.0f}" width="238" height="12" rx="5"'
                  f' fill="{BETON2}" {o(4)}/>')
    d += (f'{ten(1620, 824, 120, 16, .5)}'
          f'<rect x="1546" y="744" width="20" height="78" fill="{DOSKA2}" {o(4)}/>'
          f'<rect x="1672" y="744" width="20" height="78" fill="{DOSKA2}" {o(4)}/>'
          f'<rect x="1530" y="722" width="180" height="24" rx="8" fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        d += (f'<ellipse cx="{520+i*180:.0f}" cy="{824:.0f}" rx="74" ry="56"'
              f' fill="{TRAV68}" opacity=".9" {o(5)}/>')
    d += teplo(935, 640, 260, 230, .45)
    d += (f'<rect x="724" y="452" width="200" height="388" rx="8" fill="url(#derev)" {o(5)}/>'
          f'<rect x="944" y="452" width="200" height="388" rx="8" fill="url(#derev)" {o(5)}/>')
    d += (f'<rect y="820" width="{W}" height="{H-820}" fill="#6f6a60"/>')
    d += (f'<path d="M-20,846 q960,-26 1940,0 L1920,1080 L0,1080 Z" fill="#7d786d" opacity=".8"/>')
    s += SL(Z_DAL, d)
    # ── превращение: коляска → стол с пирогом
    uhod = A.ease(A.seg(t, .9, .8))           # коляска уходит
    per = A.ease(A.seg(t, 1.5, .9))           # стол с пирогом приходит
    m = ""
    cx, cy = 935, 964
    if uhod < .99:
        op = 1 - uhod
        m += (f'<g opacity="{op:.2f}" transform="translate({cx:.0f},{cy:.0f}) scale({1-uhod*.18:.3f})">'
              f'{ten(0, 44, 230, 26, .55)}'
              f'<path d="M-210,-40 q0,-150 210,-150 q210,0 210,150 q0,54 -60,54 l-300,0 q-60,0 -60,-54 Z"'
              f' fill="{SINKA}" {o(8)}/>'
              f'<path d="M-186,-70 q40,-120 190,-120 q150,0 190,120 Z" fill="#3e6490" opacity=".8"/>'
              f'<path d="M-150,-140 q150,-70 300,0" fill="none" stroke="#dfe7ef" stroke-width="10" opacity=".55"/>'
              f'<rect x="-230" y="10" width="460" height="22" rx="10" fill="url(#zhel)" {o(5)}/>'
              f'<circle cx="-150" cy="44" r="42" fill="{CHUGUN}" {o(6)}/>'
              f'<circle cx="-150" cy="44" r="14" fill="{ZHELEZ}"/>'
              f'<circle cx="150" cy="44" r="42" fill="{CHUGUN}" {o(6)}/>'
              f'<circle cx="150" cy="44" r="14" fill="{ZHELEZ}"/>'
              f'<path d="M190,-150 q80,-40 120,-120" fill="none" stroke="url(#zhel)" stroke-width="14"/>')
        # погремушка качается на ручке
        kach = 22 * A.w(t, 1.25)
        m += (f'<g transform="translate(300,-282) rotate({kach:.1f})">'
              f'<path d="M0,0 v64" stroke="{ob.ALYJ2}" stroke-width="8"/>'
              f'<circle cx="0" cy="88" r="30" fill="{ob.ALYJ}" {o(5)}/>'
              f'<circle cx="-10" cy="78" r="9" fill="#ffd9cf" opacity=".7"/>'
              f'<circle cx="0" cy="88" r="46" fill="{ob.ALYJ}" opacity="{.12+.16*abs(A.w(t,1.25)):.2f}"/></g>')
        m += '</g>'
    if per > .01:
        m += (f'<g opacity="{per:.2f}" transform="translate({cx:.0f},{cy:.0f}) scale({.86+.14*per:.3f})">')
        for lx in (-310, 250):
            m += (f'<rect x="{lx:.0f}" y="-26" width="46" height="150" rx="8"'
                  f' fill="url(#derev)" {o(6)}/>')
        m += (f'<rect x="-300" y="86" width="606" height="22" rx="8" fill="{DOSKA2}" {o(5)}/>')
        m += ob.stol_prazdnik(-390, -30, 780, t)
        m += '</g>'
        # пирог со свечками
        px, py = cx, cy - 98
        m += (f'<g opacity="{per:.2f}">')
        m += ten(px + 16, py + 82, 250, 22, .55)
        m += (f'<path d="M{px-270:.0f},{py:.0f} q0,84 270,84 q270,0 270,-84 l0,-104'
              f' q0,-84 -270,-84 q-270,0 -270,84 Z" fill="url(#med)" {o(7)}/>')
        m += (f'<ellipse cx="{px:.0f}" cy="{py-104:.0f}" rx="270" ry="84" fill="url(#krem)" {o(6)}/>')
        m += (f'<ellipse cx="{px:.0f}" cy="{py-104:.0f}" rx="222" ry="64" fill="#f8ead0" opacity=".92"/>')
        for i in range(14):
            a = 2 * math.pi * i / 14
            m += (f'<circle cx="{px+248*math.cos(a):.0f}" cy="{py-6+76*math.sin(a):.0f}" r="12"'
                  f' fill="{ob.ALYJ}" opacity=".9"/>')
        # точки лежат НА верхней плоскости пирога (эллипс rx 270, ry 84)
        tochki = sorted(_tochki_60(px, py - 108, 120), key=lambda q: q[1])
        for i, (sx, sy) in enumerate(tochki):
            gor = A.out(A.seg(t, 2.1 + i * .05, .3))
            m += _svechka(sx, sy, 15, t, gor * per, i * .13, 9)
        m += teplo(px, py - 200, 480, 340, .55 * per)
        m += '</g>'
    s += SL(Z_SRED, m)
    p = (f'<path d="M1640,1080 q-40,-230 70,-330 q110,120 86,330 Z" fill="#3f5330" {o(6)}/>'
         f'<path d="M-20,1080 q80,-170 10,-250 q150,70 170,250 Z" fill="#3a4c2d" {o(5)}/>')
    p += baza.ramka_pp("pravo", "#130f0a", .3)
    s += SL(Z_PERED, p)
    s += baza.vinetka(.44)
    return s


# ═══════════════════ ПЛАНЫ 54, 55, 154 ═══════════════════

def barhatnyy_albom_s_ugolkami(t):
    """Бархатный альбом с уголками на коленях: открыта страница с подписью
    года, на ней четыре чёрно-белые рисованные карточки. Живое: страница
    переворачивается, карточки чуть отходят от уголков, закладка-тесьма
    ведёт по подписи."""
    s = SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#191520"/>')
    # ── комната за альбомом: тёплое окно и ёлка пятном
    d = f'<rect width="{W}" height="{H}" fill="#241d2c" opacity=".9"/>'
    d += (f'<rect x="1388" y="118" width="444" height="384" rx="10" fill="#1d1724" {o(8)}/>')
    d += baza.okno_izby(1420, 150, 380, 320, t, None, 0.0, False, True)
    d += (f'<rect x="1420" y="150" width="380" height="320" fill="{SVET}" opacity=".40"/>')
    d += (f'<rect x="1386" y="128" width="448" height="18" rx="8" fill="url(#derev)" {o(5)}/>'
          f'<circle cx="1392" cy="137" r="14" fill="{MED}" {o(4)}/>'
          f'<circle cx="1828" cy="137" r="14" fill="{MED}" {o(4)}/>')
    d += baza.zanaveska(1434, 146, 300, 84, "#e2d4b6", t, 1)
    d += baza.zanaveska(1786, 146, 300, 84, "#e2d4b6", t, -1)
    d += (f'<rect x="1396" y="470" width="428" height="26" rx="8" fill="url(#derev)" {o(5)}/>')
    d += baza.krynka(1470, 468, .7)
    d += teplo(1610, 310, 520, 440, .5)
    d += ob.elka(300, 620, 480, t, True, True, 9)
    d += (f'<rect y="620" width="{W}" height="24" fill="#2e2535" opacity=".9"/>')
    s += SL(Z_DAL, d)
    # ── альбом
    m = ten(950, 1010, 620, 40, .6)
    m += (f'<g transform="rotate(-2 940 700)">'
          f'<rect x="250" y="300" width="1400" height="690" rx="22" fill="#5c1f2c" {o(9)}/>'
          f'<rect x="250" y="300" width="1400" height="690" rx="22" fill="#2c0c14" opacity=".32"/>')
    for i in range(16):                     # ворс бархата
        m += (f'<path d="M{274+i*88:.0f},316 q22,330 0,660" fill="none" stroke="#7b2c3a"'
              f' stroke-width="7" opacity=".28"/>')
    m += (f'<rect x="286" y="332" width="1328" height="626" rx="14" fill="#efe6d2" {o(6)}/>'
          f'<rect x="286" y="332" width="1328" height="626" rx="14" fill="{SEPIA}" opacity=".34"/>')
    m += (f'<rect x="930" y="332" width="30" height="626" fill="#c9b690" opacity=".8"/>')
    # подпись года — волной чернил, цифры кладёт over
    m += (f'<rect x="384" y="812" width="474" height="76" rx="12" fill="#e4d8bc"'
          f' opacity=".85" {o(4)}/>')
    m += (f'<path d="M420,856 q52,-40 104,0 q52,40 104,0 q52,-40 104,0 q30,22 56,6"'
          f' fill="none" stroke="#24335a" stroke-width="11" stroke-linecap="round"/>')
    # закладка-тесьма ведёт по подписи
    vu = (t * .33) % 1.0
    vx = 420 + 368 * A.ease(vu)
    m += (f'<path d="M{vx:.0f},600 q{18*A.w(t,2.4):.0f},132 {-6:.0f},238" fill="none"'
          f' stroke="{ob.ALYJ}" stroke-width="22" stroke-linecap="round"/>'
          f'<path d="M{vx-10:.0f},838 l12,32 l12,-32 Z" fill="{ob.ALYJ2}" {o(3)}/>')
    # четыре карточки
    for i, (kx, ky, vid, otk, ph) in enumerate(((344, 364, "dom", .9, .0),
                                                (1004, 364, "para", .5, .3),
                                                (1004, 586, "elka", .3, .6),
                                                (344, 586, "koza", 1.0, .85))):
        m += _kartochka_bw(kx, ky, 540, 214, vid, t, otk, ph)
    m += '</g>'
    # страница переворачивается
    pu = ((t * .24) + .62) % 1.0
    if pu < .26:
        k = A.ease(pu / .26)
        shir = 660 * abs(math.cos(math.pi * k))
        m += (f'<g transform="translate(945,330)">'
              f'<path d="M0,0 l{shir:.0f},{18 if k < .5 else -18} l0,626 l{-shir:.0f},18 Z"'
              f' fill="#f3ebd8" {o(5)} opacity=".97"/>'
              f'<path d="M0,0 l{shir*.3:.0f},6 l0,626 l{-shir*.3:.0f},10 Z"'
              f' fill="#000000" opacity="{.22*(1-abs(.5-k)*2):.2f}"/></g>')
    s += SL(Z_SRED, m)
    # ── колени
    p = (f'<path d="M-40,1080 q120,-230 420,-236 q300,-6 420,236 Z" fill="#3b3348" {o(7)}/>'
         f'<path d="M1060,1080 q120,-242 420,-236 q300,6 420,236 Z" fill="#453a52" {o(7)}/>')
    p += (f'<path d="M160,980 q220,-120 420,-30" fill="none" stroke="#574c68"'
          f' stroke-width="10" opacity=".7"/>'
          f'<path d="M1260,984 q220,-120 420,-26" fill="none" stroke="#5f5372"'
          f' stroke-width="10" opacity=".7"/>')
    s += SL(Z_PERED, p)
    s += baza.vinetka(.5)
    return s
