# -*- coding: utf-8 -*-
"""Кирпичики мира «13 ноября — Спиридон и Никодим»: изба, печь, двор, пекарня
XII века, панельный дом. Плоский вектор с толстым контуром, но с объёмом:
у каждого предмета градиент, блик и падающая тень (правило R-0017).

Палитра поздней осени: холодная улица — тёплый свет внутри. Ночь синяя,
день серый, огонь и лампа — единственное тёплое пятно в кадре.
"""
import math, random
import anim as A

W, H = 1920, 1080

# ── палитра ────────────────────────────────────────────────────────────────
K      = "#140f0c"                       # контур
NOCH   = "#141d33"; SUMER = "#2b3550"; RASSV = "#4a5a78"
DEN    = "#8ba0b2"; SERO  = "#6f7f8c"
BREVNO = "#8a5f3c"; BREVNO2 = "#6b4428"; DOSKA = "#9c7049"; DOSKA2 = "#7d5636"
POL    = "#7a5436"; POL2 = "#5f3f27"
POBEL  = "#e8e0cf"; PECH = "#efe6d2"; PECH2 = "#d8cbb0"
CHUGUN = "#2e2b2a"; ZHELEZ = "#5d6168"
SNEG   = "#eaf1fb"; INEY = "#cbdcec"; LED = "#9fc4d8"
ORA    = "#e8812a"; SVET = "#ffd98a"; KRAS = "#d6452a"; UGOL = "#a8321c"
ZOL    = "#d6a63f"; MED = "#b5803a"
KREM   = "#efe3c8"; RUSH = "#e7d7b4"; TKAN = "#b8323a"; TKAN2 = "#3f5c7a"
ZEL    = "#3c5a3a"; ZEL2 = "#56763f"; TRAVA = "#6f8c4a"
KAMEN  = "#7d7265"; KAMEN2 = "#5e564c"
BETON  = "#9aa3a8"; BETON2 = "#7a8288"
STEKLO = "#b9d6e8"
VODA   = "#2f6b78"; VODA2 = "#17424c"


def o(w_=7, col=None):
    return (f'stroke="{col or K}" stroke-width="{w_}" stroke-linecap="round"'
            f' stroke-linejoin="round"')


def defs():
    """Градиенты. Без них кадр плоский — его правка R-0017."""
    g = ""
    for i, (nm, c1, c2) in enumerate((
            ("brev",  "#a0733f", BREVNO2), ("dosk", "#ad7f4f", DOSKA2),
            ("pol",   "#8d6440", POL2),    ("pech", "#fbf5e6", PECH2),
            ("kamen", "#8c8275", KAMEN2),  ("beton", "#aab3b8", BETON2),
            ("chug",  "#4a4645", "#1d1b1a"), ("zhel", "#7e848c", "#3c4047"),
            ("sneg",  "#ffffff", "#c6d8ea"), ("led", "#cfe6f2", "#7fa9c2"),
            ("zol",   "#f0cf7a", "#9c6f20"), ("med", "#dcae63", "#7d5220"),
            ("tkan",  "#d9534a", "#7a1c22"), ("rush", "#f6ecd2", "#cdb98d"),
            ("vosk",  "#fff6e0", "#c8b08a"), ("voda", "#4e93a0", VODA2),
            ("solom", "#e3c272", "#a07c2e"), ("krem", "#f7eeda", "#cfbf9c"),
            ("glina", "#c98c55", "#7d4a23"), ("derev", "#9a6540", "#6d4423"),
            ("list",  "#f7f1df", "#d3c7a8"), ("stekl", "#dff0fa", "#8fb8ce"))):
        g += (f'<linearGradient id="{nm}" x1="0" y1="0" x2="0" y2="1">'
              f'<stop offset="0" stop-color="{c1}"/>'
              f'<stop offset="1" stop-color="{c2}"/></linearGradient>')
    g += ('<radialGradient id="teplo" cx=".5" cy=".5" r=".5">'
          f'<stop offset="0" stop-color="{SVET}" stop-opacity=".62"/>'
          f'<stop offset="1" stop-color="{SVET}" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="holod" cx=".5" cy=".5" r=".5">'
          '<stop offset="0" stop-color="#9ec8e8" stop-opacity=".45"/>'
          '<stop offset="1" stop-color="#9ec8e8" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="ten" cx=".5" cy=".5" r=".5">'
          '<stop offset="0" stop-color="#000000" stop-opacity=".58"/>'
          '<stop offset="1" stop-color="#000000" stop-opacity="0"/></radialGradient>'
          '<linearGradient id="nnoch" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="#0d1426"/><stop offset=".6" stop-color="{NOCH}"/>'
          f'<stop offset="1" stop-color="#2a3550"/></linearGradient>'
          '<linearGradient id="nsumer" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="#1e2b49"/><stop offset=".55" stop-color="{SUMER}"/>'
          '<stop offset="1" stop-color="#8a6a62"/></linearGradient>'
          '<linearGradient id="nrassv" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#36507a"/><stop offset=".6" stop-color="#8f9fb4"/>'
          '<stop offset="1" stop-color="#e4c9a8"/></linearGradient>'
          '<linearGradient id="nden" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#7d93a6"/><stop offset="1" stop-color="#c8d2d8"/></linearGradient>'
          '<linearGradient id="zakat" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#3f4a72"/><stop offset=".55" stop-color="#c47a48"/>'
          '<stop offset="1" stop-color="#eec07a"/></linearGradient>')
    return g



# ── СЛОИ ПО ГЛУБИНЕ ────────────────────────────────────────────────────────
# Метку глубины ставят сами кирпичики — камера (kamera.py) по ней разводит
# планы с разной скоростью. Это наш объём (C1/K9): без него «зум» остаётся
# плоским растягиванием картинки.
def SL(z, svg):
    return f'<g data-z="{z}">{svg}</g><!--/z-->'


Z_NEBO, Z_DAL, Z_SRED, Z_PERED, Z_LETIT, Z_FIX = 1500, 520, 420, -230, -120, "fix"


def ten(cx, cy, rx, ry, op=1.0):
    return (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}"'
            f' fill="url(#ten)" opacity="{op:.2f}"/>')


def teplo(cx, cy, rx, ry=None, op=.8):
    return (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{(ry or rx):.0f}"'
            f' fill="url(#teplo)" opacity="{op:.2f}"/>')


# ── поверхности ────────────────────────────────────────────────────────────
def brevna(x, y, w_, h_, hh=78, sdvig=0):
    """Бревенчатая стена: брёвна с торцевым бликом снизу."""
    s = f'<g>'
    n = int(h_ / hh) + 1
    for i in range(n):
        yy = y + i * hh
        s += (f'<rect x="{x}" y="{yy:.0f}" width="{w_}" height="{hh}" rx="{hh*.46:.0f}"'
              f' fill="url(#brev)" {o(5)}/>'
              f'<rect x="{x+10}" y="{yy+hh*.62:.0f}" width="{w_-20}" height="{hh*.18:.0f}"'
              f' rx="9" fill="#5a3721" opacity=".45"/>')
    return s + "</g>"


def doski(x, y, w_, h_, step=66, vert=True, grad="dosk"):
    s = ""
    if vert:
        n = int(w_ / step) + 1
        for i in range(n):
            xx = x + i * step
            s += (f'<rect x="{xx:.0f}" y="{y}" width="{step-5}" height="{h_}"'
                  f' fill="url(#{grad})" {o(4)}/>')
    else:
        n = int(h_ / step) + 1
        for i in range(n):
            yy = y + i * step
            s += (f'<rect x="{x}" y="{yy:.0f}" width="{w_}" height="{step-5}"'
                  f' fill="url(#{grad})" {o(4)}/>')
    return s


def kladka(x, y, w_, h_, kh=74, col="url(#kamen)"):
    s = ""
    rows = int(h_ / kh) + 1
    for r in range(rows):
        yy = y + r * kh
        off = 0 if r % 2 == 0 else 92
        for c in range(int(w_ / 184) + 2):
            xx = x - 92 + off + c * 184
            s += (f'<rect x="{xx:.0f}" y="{yy:.0f}" width="176" height="{kh-8}" rx="10"'
                  f' fill="{col}" opacity=".92" stroke="#4b443b" stroke-width="3"/>')
    return f'<g clip-path="none">{s}</g>'


def polovicy(y, col="url(#pol)"):
    s = f'<rect y="{y}" width="{W}" height="{H-y}" fill="{col}"/>'
    for i in range(9):
        yy = y + 14 + i * (H - y) / 8
        s += f'<line x1="0" y1="{yy:.0f}" x2="{W}" y2="{yy:.0f}" stroke="#4e3220" stroke-width="3" opacity=".5"/>'
    return s + f'<rect y="{y-10}" width="{W}" height="14" fill="{POL2}" {o(4)}/>'


def nebo(kind="noch", t=0.0, zvezdy=True, seed=3):
    """Небо тремя слоями: заливка, светила, облака."""
    s = f'<rect width="{W}" height="{H}" fill="url(#n{kind})"/>' if kind in (
        "noch", "sumer", "rassv", "den") else f'<rect width="{W}" height="{H}" fill="url(#{kind})"/>'
    if zvezdy and kind in ("noch", "sumer"):
        r = random.Random(seed)
        for i in range(60):
            x, y = r.uniform(0, W), r.uniform(0, H * .55)
            op = .25 + .6 * abs(A.w(t, 2.2 + r.uniform(0, 2), i * .11))
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.4,3.2):.1f}" fill="#fdf6e0" opacity="{op:.2f}"/>'
    return s


def oblaka(t, y=180, n=4, seed=7, op=.5, col="#e8eef6", sp=10.0):
    r = random.Random(seed)
    s = ""
    for i in range(n):
        base = r.uniform(-300, W)
        x = (base + t * sp * r.uniform(.6, 1.4)) % (W + 700) - 350
        yy = y + r.uniform(-70, 90)
        sc = r.uniform(.7, 1.5)
        s += (f'<g transform="translate({x:.0f},{yy:.0f}) scale({sc:.2f})" opacity="{op:.2f}">'
              f'<ellipse cx="0" cy="0" rx="170" ry="52" fill="{col}"/>'
              f'<ellipse cx="-90" cy="16" rx="110" ry="40" fill="{col}"/>'
              f'<ellipse cx="96" cy="14" rx="124" ry="42" fill="{col}"/>'
              f'<ellipse cx="10" cy="-30" rx="92" ry="44" fill="{col}"/></g>')
    return s


def sneg_letit(t, n=46, seed=5, op=.8, sp=1.0):
    r = random.Random(seed)
    s = f'<g fill="#ffffff" opacity="{op}">'
    for i in range(n):
        x0 = r.uniform(0, W); p0 = r.uniform(0, 1)
        v = r.uniform(14, 40) * sp; rr = r.uniform(2.2, 5.6); ph = r.uniform(0, 1)
        p = (p0 + t * v / H) % 1.0
        s += (f'<circle cx="{x0 + 40*A.w(t,5.0,ph):.0f}" cy="{p*H:.0f}" r="{rr:.1f}"'
              f' opacity="{.3+.6*abs(A.w(t,3.0,ph)):.2f}"/>')
    return s + "</g>"


def sneg_lezhit(y, amp=26, col="url(#sneg)"):
    return (f'<path d="M-20,{y+amp} q240,{-amp*1.8} 480,{-6} q240,{amp*1.2} 480,{-10}'
            f' q240,{-amp*1.6} 480,{-4} q240,{amp} 520,{-12} L1940,{H} L-20,{H} Z"'
            f' fill="{col}" {o(5)}/>')


def tuman(t, y=560, op=.42, col="#dde7f0"):
    s = ""
    for i in range(3):
        dx = 70 * A.w(t, 22 + i * 7, i * .3)
        s += (f'<ellipse cx="{W*.5+dx:.0f}" cy="{y+i*54}" rx="{1200-i*140}" ry="{70-i*12}"'
              f' fill="{col}" opacity="{op*(1-i*.22):.2f}"/>')
    return s


# ── огонь, свет, дым ───────────────────────────────────────────────────────
def ogon(cx, cy, t, s_=1.0, ph=0.0, iskry_n=6, col=None):
    out = teplo(cx, cy - 24 * s_, 104 * s_, 84 * s_)
    for i in range(3):
        f = i * .33 + ph
        hh = (118 if i == 1 else 82) * s_ * (1 + .22 * A.w(t, .85, f))
        bx = cx + (i - 1) * 40 * s_
        dx = 17 * s_ * A.w(t, 1.55, f)
        c = (col or (SVET if i == 1 else ORA))
        out += (f'<path d="M{bx:.0f},{cy:.0f} C{bx-30*s_:.0f},{cy-hh*.45:.0f}'
                f' {bx-12*s_+dx:.0f},{cy-hh*.75:.0f} {bx+dx:.0f},{cy-hh:.0f}'
                f' C{bx+18*s_+dx:.0f},{cy-hh*.7:.0f} {bx+30*s_:.0f},{cy-hh*.4:.0f} {bx:.0f},{cy:.0f} Z"'
                f' fill="{c}" opacity="{.78+.2*abs(A.w(t,1.05,f)):.2f}"/>')
    for i in range(iskry_n):
        p = ((t * .42) + i * (1.0 / max(1, iskry_n))) % 1.0
        out += (f'<circle cx="{cx + 54*s_*A.w(t,2.1,i*.2):.0f}" cy="{cy-30*s_-p*230*s_:.0f}"'
                f' r="{(2.6+1.8*(1-p))*s_:.1f}" fill="{SVET}" opacity="{(1-p)*.8:.2f}"/>')
    return out


def ugli(x, y, w_, t, n=7, seed=2):
    r = random.Random(seed)
    s = ""
    for i in range(n):
        xx = x + r.uniform(0, w_); rr = r.uniform(12, 26)
        op = .45 + .5 * abs(A.w(t, 1.6 + r.uniform(0, 1.4), i * .2))
        s += (f'<ellipse cx="{xx:.0f}" cy="{y + r.uniform(-8,8):.0f}" rx="{rr:.0f}" ry="{rr*.6:.0f}"'
              f' fill="{UGOL}" opacity="{op:.2f}"/>')
    return s


def iskra_let(t, x, y, n=10, seed=4, R=320, sp=.5):
    r = random.Random(seed)
    s = ""
    for i in range(n):
        p = ((t * sp) + r.uniform(0, 1)) % 1.0
        s += (f'<circle cx="{x + r.uniform(-60,60) + 40*A.w(t,1.4,i*.3):.0f}"'
              f' cy="{y - p*R:.0f}" r="{(1.8+2.6*(1-p)):.1f}" fill="{SVET}"'
              f' opacity="{(1-p)*.9:.2f}"/>')
    return s


def dym(x, y, t, n=5, sp=.26, R=300, op=.4, col="#cfd6de", wide=1.0):
    s = ""
    for i in range(n):
        p = ((t * sp) + i / n) % 1.0
        rr = (16 + 54 * p) * wide
        s += (f'<ellipse cx="{x + 70*wide*A.w(t,6.0,i*.27)*p:.0f}" cy="{y - p*R:.0f}"'
              f' rx="{rr:.0f}" ry="{rr*.8:.0f}" fill="{col}" opacity="{op*(1-p):.2f}"/>')
    return s


def par(x, y, t, n=4, op=.5, R=150, sp=.4, wide=1.0):
    return dym(x, y, t, n, sp, R, op, "#f2f6fa", wide)


def svecha(x, y, t, ph=0.0, s_=1.0, h_=92):
    hh = 40 * s_ * (1 + .16 * A.w(t, .8, ph))
    dx = 5 * s_ * A.w(t, 1.45, ph)
    return (ten(x + 4, y + h_ * s_ + 6, 32 * s_, 9 * s_, .45)
            + f'<rect x="{x-15*s_:.0f}" y="{y:.0f}" width="{30*s_:.0f}" height="{h_*s_:.0f}"'
            f' rx="6" fill="url(#vosk)" {o(5)}/>'
            + teplo(x, y - hh * .4, 64 * s_, 74 * s_)
            + f'<path d="M{x+dx:.0f},{y-hh:.0f} c16,{hh*.5:.0f} 12,{hh*.8:.0f} -2,{hh:.0f}'
            f' c-14,{-hh*.2:.0f} -16,{-hh*.5:.0f} 2,{-hh:.0f} Z" fill="{SVET}"/>')


def lampa(x, y, t, s_=1.0, abazhur=False):
    """Керосиновая лампа или абажур — главный тёплый источник в избе."""
    sw = 1.6 * A.w(t, 5.4)
    s = f'<g transform="rotate({sw:.2f} {x:.0f} {y-220*s_:.0f})">'
    s += f'<line x1="{x:.0f}" y1="{y-420*s_:.0f}" x2="{x:.0f}" y2="{y-150*s_:.0f}" stroke="{K}" stroke-width="6"/>'
    if abazhur:
        s += (f'<path d="M{x-140*s_:.0f},{y-60*s_:.0f} L{x-54*s_:.0f},{y-170*s_:.0f}'
              f' L{x+54*s_:.0f},{y-170*s_:.0f} L{x+140*s_:.0f},{y-60*s_:.0f} Z"'
              f' fill="url(#tkan)" {o(6)}/>')
        s += teplo(x, y + 40 * s_, 320 * s_, 240 * s_)
    else:
        s += (f'<path d="M{x-44*s_:.0f},{y-150*s_:.0f} q44,{-40*s_:.0f} 88,0 l-10,{110*s_:.0f}'
              f' q-34,{22*s_:.0f} -68,0 Z" fill="url(#stekl)" opacity=".75" {o(5)}/>')
        s += teplo(x, y - 90 * s_, 240 * s_, 200 * s_)
        s += (f'<path d="M{x:.0f},{y-130*s_:.0f} c12,{26*s_:.0f} 8,{40*s_:.0f} -2,{52*s_:.0f}'
              f' c-10,{-12*s_:.0f} -12,{-26*s_:.0f} 2,{-52*s_:.0f} Z" fill="{SVET}"'
              f' opacity="{.8+.2*abs(A.w(t,1.2)):.2f}"/>')
        s += (f'<rect x="{x-50*s_:.0f}" y="{y-44*s_:.0f}" width="{100*s_:.0f}" height="{52*s_:.0f}"'
              f' rx="10" fill="url(#med)" {o(5)}/>')
    return s + "</g>"


def luch(x, y, w_, h_, t, op=.2):
    """Косой луч света из окна, в нём плавают пылинки."""
    s = (f'<path d="M{x:.0f},{y:.0f} l{w_:.0f},0 l{w_*.5:.0f},{h_:.0f} l{-w_*1.6:.0f},0 Z"'
         f' fill="{SVET}" opacity="{op:.2f}"/>')
    r = random.Random(11)
    for i in range(16):
        u = r.uniform(0, 1)
        px = x + w_ * r.uniform(-.3, 1.3) + 26 * A.w(t, 7 + i, i * .2)
        py = y + h_ * ((u + t * .03) % 1.0)
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(1.6,3.4):.1f}" fill="#fff6dd" opacity=".55"/>'
    return s


# ── предметы избы ──────────────────────────────────────────────────────────
def okno_izby(x, y, w_, h_, t, vid=None, moroz=0.0, svet=False, krest=True):
    """Окно с крестовиной. vid — что видно за стеклом (svg), moroz — узор."""
    s = ten(x + w_ / 2 + 10, y + h_ + 16, w_ * .55, 16, .4)
    s += f'<rect x="{x-16}" y="{y-16}" width="{w_+32}" height="{h_+32}" rx="8" fill="url(#derev)" {o(7)}/>'
    s += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="url(#stekl)" opacity=".92"/>'
    if vid:
        s += f'<g clip-path="url(#ok{int(x)}_{int(y)})">{vid}</g>'
        s = (f'<clipPath id="ok{int(x)}_{int(y)}"><rect x="{x}" y="{y}" width="{w_}" height="{h_}"/></clipPath>') + s
    if svet:
        s += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="{SVET}" opacity=".35"/>'
    if moroz > 0:
        r = random.Random(int(x) + 3)
        for i in range(18):
            cx = x + r.uniform(0, w_); cy = y + r.uniform(0, h_)
            rr = r.uniform(18, 54) * (.6 + .4 * abs(A.w(t, 9 + i * .4, i * .1))) * moroz
            s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="#ffffff" opacity=".2"/>'
        s += (f'<path d="M{x},{y+h_} q{w_*.25:.0f},{-h_*.5:.0f} {w_*.5:.0f},{-h_*.2:.0f}'
              f' q{w_*.25:.0f},{h_*.3:.0f} {w_*.5:.0f},{-h_*.35:.0f}" fill="none"'
              f' stroke="#ffffff" stroke-width="6" opacity="{.35*moroz:.2f}"/>')
    if krest:
        s += (f'<line x1="{x+w_/2:.0f}" y1="{y}" x2="{x+w_/2:.0f}" y2="{y+h_}" stroke="url(#derev)" stroke-width="16"/>'
              f'<line x1="{x}" y1="{y+h_/2:.0f}" x2="{x+w_}" y2="{y+h_/2:.0f}" stroke="url(#derev)" stroke-width="16"/>')
    s += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="none" {o(7)}/>'
    s += (f'<path d="M{x+10},{y+h_*.08:.0f} l{w_*.42:.0f},{h_*.5:.0f}" stroke="#ffffff"'
          f' stroke-width="10" opacity=".22"/>')
    return s


def pech(x, y, w_, h_, t, ogon_on=True, belaya=True, zaslonka=False):
    """Русская печь: побелённый массив, устье с огнём, лежанка."""
    s = ten(x + w_ / 2, y + h_ + 14, w_ * .55, 22, .5)
    s += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="18" fill="url(#pech)" {o(8)}/>'
    s += (f'<rect x="{x+w_*.06:.0f}" y="{y-28}" width="{w_*.88:.0f}" height="36" rx="10"'
          f' fill="{PECH2}" {o(6)}/>')
    uw, uh = w_ * .42, h_ * .3
    ux, uy = x + w_ * .14, y + h_ * .42
    s += f'<path d="M{ux:.0f},{uy+uh:.0f} v{-uh*.55:.0f} q{uw*.5:.0f},{-uh*.75:.0f} {uw:.0f},0 v{uh*.55:.0f} Z" fill="{CHUGUN}" {o(6)}/>'
    if zaslonka:
        s += (f'<path d="M{ux-8:.0f},{uy+uh:.0f} v{-uh*.6:.0f} q{uw*.5:.0f},{-uh*.8:.0f} {uw+16:.0f},0'
              f' v{uh*.6:.0f} Z" fill="url(#chug)" {o(6)}/>'
              f'<circle cx="{ux+uw/2:.0f}" cy="{uy+uh*.5:.0f}" r="16" fill="url(#zhel)" {o(5)}/>')
    elif ogon_on:
        s += ugli(ux + 20, uy + uh - 16, uw - 40, t, 6)
        s += ogon(ux + uw / 2, uy + uh - 10, t, uw / 260, 0, 5)
    s += (f'<rect x="{x+w_*.6:.0f}" y="{y+h_*.52:.0f}" width="{w_*.34:.0f}" height="{h_*.3:.0f}"'
          f' rx="10" fill="{PECH2}" {o(6)}/>')
    for i in range(3):
        s += (f'<line x1="{x+10}" y1="{y+h_*(.2+i*.26):.0f}" x2="{x+w_-10:.0f}"'
              f' y2="{y+h_*(.2+i*.26):.0f}" stroke="{PECH2}" stroke-width="4" opacity=".6"/>')
    return s


def stol(x, y, w_, h_=34, nog=True):
    s = ten(x + w_ / 2, y + (150 if nog else 20), w_ * .5, 20, .45)
    s += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="8" fill="url(#derev)" {o(7)}/>'
    if nog:
        for xx in (x + 24, x + w_ - 54):
            s += f'<rect x="{xx:.0f}" y="{y+h_:.0f}" width="30" height="150" fill="url(#derev)" {o(6)}/>'
    return s


def lavka(x, y, w_):
    return (ten(x + w_ / 2, y + 112, w_ * .45, 14, .4)
            + f'<rect x="{x}" y="{y}" width="{w_}" height="24" rx="8" fill="url(#derev)" {o(6)}/>'
            + f'<rect x="{x+16}" y="{y+24}" width="22" height="96" fill="url(#derev)" {o(5)}/>'
            + f'<rect x="{x+w_-38:.0f}" y="{y+24}" width="22" height="96" fill="url(#derev)" {o(5)}/>')


def polka(x, y, w_):
    return (f'<rect x="{x}" y="{y}" width="{w_}" height="20" rx="6" fill="url(#derev)" {o(6)}/>'
            + f'<path d="M{x+30},{y+20} l22,34 M{x+w_-52:.0f},{y+20} l-22,34" {o(5)} fill="none"/>')


def krynka(x, y, s_=1.0, col="url(#glina)"):
    return (ten(x, y + 8 * s_, 34 * s_, 9 * s_, .4)
            + f'<path d="M{x-26*s_:.0f},{y:.0f} q-14,{-46*s_:.0f} 4,{-62*s_:.0f}'
            f' q{22*s_:.0f},{-12*s_:.0f} {44*s_:.0f},0 q18,{16*s_:.0f} 4,{62*s_:.0f} Z"'
            f' fill="{col}" {o(6)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y-62*s_:.0f}" rx="{26*s_:.0f}" ry="{9*s_:.0f}"'
            f' fill="#8a5a30" {o(5)}/>')


def karavay(x, y, s_=1.0, rushnik=True):
    s = ten(x, y + 14 * s_, 70 * s_, 14 * s_, .45)
    if rushnik:
        s += (f'<path d="M{x-96*s_:.0f},{y+6*s_:.0f} h{192*s_:.0f} l-14,{26*s_:.0f} h{-164*s_:.0f} Z"'
              f' fill="url(#rush)" {o(5)}/>')
        s += (f'<rect x="{x-78*s_:.0f}" y="{y+16*s_:.0f}" width="{156*s_:.0f}" height="8"'
              f' fill="{TKAN}" opacity=".8"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-26*s_:.0f}" rx="{76*s_:.0f}" ry="{44*s_:.0f}"'
          f' fill="url(#med)" {o(6)}/>')
    s += (f'<path d="M{x-48*s_:.0f},{y-40*s_:.0f} q{48*s_:.0f},{-20*s_:.0f} {96*s_:.0f},0"'
          f' fill="none" stroke="#f2cf8c" stroke-width="{7*s_:.0f}" opacity=".7"/>')
    return s


def monety(x, y, t, n=5, seed=1, s_=1.0):
    r = random.Random(seed)
    s = ""
    for i in range(n):
        xx = x + r.uniform(-50, 50) * s_; yy = y + r.uniform(-14, 14) * s_
        bl = .4 + .6 * abs(A.w(t, 2.4 + i * .5, i * .2))
        s += (f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="{20*s_:.0f}" ry="{14*s_:.0f}"'
              f' fill="url(#med)" {o(4)}/>'
              f'<ellipse cx="{xx-5*s_:.0f}" cy="{yy-4*s_:.0f}" rx="{8*s_:.0f}" ry="{5*s_:.0f}"'
              f' fill="#f4dba0" opacity="{bl:.2f}"/>')
    return s


def hodiki(x, y, t, s_=1.0):
    ang = 14 * A.w(t, 2.0)
    return (f'<rect x="{x-56*s_:.0f}" y="{y-70*s_:.0f}" width="{112*s_:.0f}" height="{120*s_:.0f}"'
            f' rx="12" fill="url(#derev)" {o(6)}/>'
            f'<circle cx="{x:.0f}" cy="{y-16*s_:.0f}" r="{40*s_:.0f}" fill="url(#krem)" {o(5)}/>'
            f'<line x1="{x:.0f}" y1="{y-16*s_:.0f}" x2="{x+22*s_:.0f}" y2="{y-30*s_:.0f}" stroke="{K}" stroke-width="5"/>'
            f'<line x1="{x:.0f}" y1="{y-16*s_:.0f}" x2="{x-12*s_:.0f}" y2="{y-44*s_:.0f}" stroke="{K}" stroke-width="4"/>'
            f'<g transform="rotate({ang:.1f} {x:.0f} {y+50*s_:.0f})">'
            f'<line x1="{x:.0f}" y1="{y+50*s_:.0f}" x2="{x:.0f}" y2="{y+160*s_:.0f}" stroke="{MED}" stroke-width="{6*s_:.0f}"/>'
            f'<circle cx="{x:.0f}" cy="{y+164*s_:.0f}" r="{20*s_:.0f}" fill="url(#zol)" {o(4)}/></g>')


def kot(x, y, t, s_=1.0, col="#3b3430", spit=False):
    """Кот: хвост качается, ухо поводит, глаза моргают."""
    hv = 16 * A.w(t, 3.2)
    uh = 5 * A.w(t, 2.1)
    s = ten(x, y + 10 * s_, 74 * s_, 14 * s_, .4)
    s += (f'<g transform="rotate({hv:.1f} {x-56*s_:.0f} {y-18*s_:.0f})">'
          f'<path d="M{x-56*s_:.0f},{y-18*s_:.0f} q{-54*s_:.0f},{-20*s_:.0f} {-40*s_:.0f},{-72*s_:.0f}"'
          f' fill="none" stroke="{col}" stroke-width="{20*s_:.0f}" stroke-linecap="round"/></g>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-30*s_:.0f}" rx="{76*s_:.0f}" ry="{42*s_:.0f}" fill="{col}" {o(6)}/>')
    hx, hy = x + 56 * s_, y - 70 * s_
    s += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{36*s_:.0f}" fill="{col}" {o(6)}/>'
    for sgn in (-1, 1):
        s += (f'<g transform="rotate({uh*sgn:.1f} {hx:.0f} {hy:.0f})">'
              f'<path d="M{hx+sgn*22*s_:.0f},{hy-24*s_:.0f} l{sgn*6*s_:.0f},{-28*s_:.0f}'
              f' l{-sgn*26*s_:.0f},{10*s_:.0f} Z" fill="{col}" {o(5)}/></g>')
    if spit or A.blink(t, 4.6, .2):
        s += (f'<path d="M{hx-16*s_:.0f},{hy-2*s_:.0f} h{12*s_:.0f} M{hx+8*s_:.0f},{hy-2*s_:.0f} h{12*s_:.0f}"'
              f' stroke="{K}" stroke-width="{4*s_:.0f}"/>')
    else:
        for dx in (-11, 13):
            s += (f'<ellipse cx="{hx+dx*s_:.0f}" cy="{hy-2*s_:.0f}" rx="{7*s_:.0f}" ry="{9*s_:.0f}"'
                  f' fill="{SVET}"/><ellipse cx="{hx+dx*s_:.0f}" cy="{hy-2*s_:.0f}" rx="{2.6*s_:.0f}"'
                  f' ry="{8*s_:.0f}" fill="{K}"/>')
    return s


def kura(x, y, t, s_=1.0, ph=0.0, col="#e2d6c2", greben=True):
    kl = 7 * A.w(t, 1.7, ph)          # клюёт
    s = ten(x, y + 8 * s_, 44 * s_, 10 * s_, .35)
    s += (f'<g transform="rotate({kl:.1f} {x:.0f} {y:.0f})">'
          f'<ellipse cx="{x:.0f}" cy="{y-30*s_:.0f}" rx="{52*s_:.0f}" ry="{38*s_:.0f}" fill="{col}" {o(5)}/>'
          f'<path d="M{x-48*s_:.0f},{y-36*s_:.0f} q{-34*s_:.0f},{10*s_:.0f} {-10*s_:.0f},{26*s_:.0f}"'
          f' fill="{col}" {o(5)}/>'
          f'<circle cx="{x+34*s_:.0f}" cy="{y-66*s_:.0f}" r="{22*s_:.0f}" fill="{col}" {o(5)}/>'
          f'<path d="M{x+54*s_:.0f},{y-66*s_:.0f} l{18*s_:.0f},{6*s_:.0f} l{-18*s_:.0f},{8*s_:.0f} Z" fill="{ORA}" {o(3)}/>'
          f'<circle cx="{x+40*s_:.0f}" cy="{y-72*s_:.0f}" r="{3.4*s_:.0f}" fill="{K}"/>')
    if greben:
        s += (f'<path d="M{x+22*s_:.0f},{y-84*s_:.0f} q{6*s_:.0f},{-16*s_:.0f} {14*s_:.0f},0'
              f' q{6*s_:.0f},{-16*s_:.0f} {14*s_:.0f},0 Z" fill="{KRAS}" {o(4)}/>')
    s += "</g>"
    for i, dx in enumerate((-12, 14)):
        s += (f'<line x1="{x+dx*s_:.0f}" y1="{y:.0f}" x2="{x+dx*s_:.0f}" y2="{y+18*s_:.0f}"'
              f' stroke="{ORA}" stroke-width="{5*s_:.0f}"/>')
    return s


def ptica(x, y, t, s_=1.0, col=KRAS, ph=0.0, seryj="#5b6a78"):
    """Снегирь/воробей на ветке: поворачивает голову, дёргает хвостом."""
    hv = 10 * A.w(t, 1.3, ph)
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<g transform="rotate({hv:.1f} 0 0)">'
            f'<path d="M-34,-6 l-26,-12 l24,22 Z" fill="{seryj}" {o(3)}/></g>'
            f'<ellipse cx="0" cy="-16" rx="30" ry="24" fill="{col}" {o(4)}/>'
            f'<circle cx="20" cy="-34" r="16" fill="{seryj}" {o(4)}/>'
            f'<path d="M34,-34 l14,5 l-14,6 Z" fill="{ZOL}" {o(2)}/>'
            f'<circle cx="24" cy="-38" r="2.8" fill="{K}"/></g>')


def siluet(x, y, h_=300, col="#1a1c22", op=1.0, platok=False, kant=None):
    """Человек со спины: плечи, шея, пола одежды. Рук не рисуем (правило 05.11)."""
    w_ = h_ * .40
    hh = h_ * .145
    s = f'<g opacity="{op:.2f}">'
    s += (f'<path d="M{x-w_*.30:.0f},{y-h_*.66:.0f} q{w_*.30:.0f},{-h_*.10:.0f} {w_*.60:.0f},0'
          f' L{x+w_*.56:.0f},{y-h_*.16:.0f} q{-w_*.56:.0f},{h_*.07:.0f} {-w_*1.12:.0f},0 Z" fill="{col}"/>')
    s += (f'<path d="M{x-w_*.56:.0f},{y-h_*.20:.0f} q{w_*.56:.0f},{h_*.08:.0f} {w_*1.12:.0f},0'
          f' L{x+w_*.50:.0f},{y:.0f} q{-w_*.50:.0f},{h_*.05:.0f} {-w_*1.0:.0f},0 Z" fill="{col}"/>')
    s += f'<rect x="{x-w_*.13:.0f}" y="{y-h_*.76:.0f}" width="{w_*.26:.0f}" height="{h_*.14:.0f}" fill="{col}"/>'
    s += f'<ellipse cx="{x:.0f}" cy="{y-h_*.84:.0f}" rx="{hh:.0f}" ry="{hh*1.08:.0f}" fill="{col}"/>'
    if platok:
        s += (f'<path d="M{x-hh*1.1:.0f},{y-h_*.86:.0f} a{hh*1.1:.0f},{hh*1.1:.0f} 0 0 1 {hh*2.2:.0f},0'
              f' q{-hh*.2:.0f},{hh*2.1:.0f} {-hh*1.1:.0f},{hh*2.3:.0f}'
              f' q{-hh*.9:.0f},{-hh*.2:.0f} {-hh*1.1:.0f},{-hh*2.3:.0f} Z" fill="{TKAN}" opacity=".92"/>')
    if kant:
        # кант по контуру: без него тёмная фигура сливается с тёмным фоном
        s += (f'<path d="M{x-w_*.30:.0f},{y-h_*.66:.0f} q{w_*.30:.0f},{-h_*.10:.0f} {w_*.60:.0f},0'
              f' L{x+w_*.56:.0f},{y-h_*.16:.0f}" fill="none" stroke="{kant}" stroke-width="5"'
              f' opacity=".75" stroke-linecap="round"/>')
        s += (f'<path d="M{x-hh*.98:.0f},{y-h_*.88:.0f} a{hh:.0f},{hh:.0f} 0 0 1 {hh*1.96:.0f},0"'
              f' fill="none" stroke="{kant}" stroke-width="5" opacity=".75" stroke-linecap="round"/>')
    return s + "</g>"


def ramka_pp(storona="oba", col="#0e0c0b", op=.85):
    """Передний план тёмным силуэтом — даёт кадру глубину (его «Голливуд»)."""
    s = ""
    if storona in ("levo", "oba"):
        s += (f'<path d="M-10,-10 h210 q-40,300 -16,620 q-26,300 10,480 h-204 Z"'
              f' fill="{col}" opacity="{op}"/>')
    if storona in ("pravo", "oba"):
        s += (f'<path d="M{W+10},-10 h-180 q36,320 14,600 q24,320 -8,490 h174 Z"'
              f' fill="{col}" opacity="{op}"/>')
    if storona == "verh":
        s += (f'<path d="M-10,-10 h{W+20} v150 q-480,70 -960,10 q-480,-60 -960,30 Z"'
              f' fill="{col}" opacity="{op}"/>')
    return s


def zanaveska(x, y, h_, w_=120, col=None, t=0.0, sgn=1):
    c = col or TKAN
    dx = 7 * A.w(t, 6.4)
    return (f'<path d="M{x:.0f},{y:.0f} q{sgn*w_*.5:.0f},{h_*.4:.0f} {sgn*(w_*.3+dx):.0f},{h_:.0f}'
            f' l{-sgn*w_:.0f},0 q{sgn*w_*.2:.0f},{-h_*.5:.0f} {-sgn*w_*.2:.0f},{-h_:.0f} Z"'
            f' fill="{c}" opacity=".92" {o(5)}/>')


def dver(x, y, w_, h_, open_=0.0, col="url(#derev)", kruchok=False, cepochka=False):
    s = f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="6" fill="#1b2029"/>'
    s += (f'<g transform="translate({x:.0f},{y:.0f}) scale({1-open_*.55:.3f},1)">'
          f'<rect x="0" y="0" width="{w_}" height="{h_}" rx="6" fill="{col}" {o(7)}/>'
          f'<rect x="{w_*.12:.0f}" y="{h_*.08:.0f}" width="{w_*.76:.0f}" height="{h_*.36:.0f}"'
          f' rx="6" fill="none" stroke="{DOSKA2}" stroke-width="6"/>'
          f'<circle cx="{w_*.84:.0f}" cy="{h_*.54:.0f}" r="11" fill="url(#zhel)" {o(4)}/></g>')
    if kruchok:
        s += (f'<path d="M{x+w_+6:.0f},{y+h_*.46:.0f} h40" stroke="url(#zhel)" stroke-width="12" stroke-linecap="round"/>'
              f'<circle cx="{x+w_+50:.0f}" cy="{y+h_*.46:.0f}" r="10" fill="{ZHELEZ}" {o(4)}/>')
    if cepochka:
        s += (f'<path d="M{x+w_*.9:.0f},{y+h_*.4:.0f} q40,26 86,10" fill="none"'
              f' stroke="url(#zhel)" stroke-width="9" stroke-dasharray="4 9" stroke-linecap="round"/>')
    return s


def pleten(x, y, w_, h_=170, kolya=9):
    s = ""
    for i in range(kolya):
        xx = x + i * (w_ / (kolya - 1))
        s += f'<rect x="{xx-7:.0f}" y="{y-h_:.0f}" width="14" height="{h_+20}" rx="6" fill="url(#derev)" {o(4)}/>'
    for r in range(5):
        yy = y - h_ + 22 + r * (h_ - 30) / 4
        d = f'M{x-10},{yy:.0f}'
        for i in range(kolya):
            xx = x + i * (w_ / (kolya - 1))
            d += f' Q{xx:.0f},{yy + (16 if i % 2 == 0 else -16):.0f} {xx+w_/(kolya-1)/2:.0f},{yy:.0f}'
        s += f'<path d="{d}" fill="none" stroke="#a97f4e" stroke-width="13" stroke-linecap="round"/>'
    return s


def izba_snaruzhi(x, base, w_, t, svet=True, truba=True, seed=2):
    """Избушка снаружи: сруб, двускатная крыша со снегом, тёплое окно, дымок."""
    h_ = w_ * .62
    s = ten(x + w_ / 2, base + 16, w_ * .55, 22, .5)
    s += brevna(x, base - h_, w_, h_, hh=w_ * .11)
    s += (f'<path d="M{x-w_*.1:.0f},{base-h_:.0f} L{x+w_/2:.0f},{base-h_-w_*.42:.0f}'
          f' L{x+w_*1.1:.0f},{base-h_:.0f} Z" fill="{DOSKA2}" {o(7)}/>')
    s += (f'<path d="M{x-w_*.12:.0f},{base-h_+6:.0f} L{x+w_/2:.0f},{base-h_-w_*.44:.0f}'
          f' L{x+w_*1.12:.0f},{base-h_+6:.0f} l-30,-26 L{x+w_/2:.0f},{base-h_-w_*.38:.0f}'
          f' l{-w_*1.12+30+w_*.12:.0f},0 Z" fill="url(#sneg)" {o(5)}/>')
    ox = x + w_ * .3
    s += okno_izby(ox, base - h_ * .72, w_ * .26, w_ * .22, t, svet=svet, moroz=.5)
    if truba:
        tx = x + w_ * .72
        s += (f'<rect x="{tx:.0f}" y="{base-h_-w_*.3:.0f}" width="{w_*.1:.0f}" height="{w_*.2:.0f}"'
              f' fill="url(#kamen)" {o(6)}/>')
        s += dym(tx + w_ * .05, base - h_ - w_ * .32, t, 5, .2, 300, .36, "#cfd6de", .8)
    return s


def panelka(x, base, w_, t, etazh=5, okna_svet=True, seed=4):
    """Панельный дом: ряды окон, часть загорается."""
    h_ = etazh * 130
    r = random.Random(seed)
    s = ten(x + w_ / 2, base + 14, w_ * .5, 20, .45)
    s += f'<rect x="{x}" y="{base-h_:.0f}" width="{w_}" height="{h_}" fill="url(#beton)" {o(7)}/>'
    for e in range(etazh):
        for c in range(int(w_ / 120)):
            ox = x + 34 + c * 120; oy = base - h_ + 30 + e * 130
            on = okna_svet and (r.random() < .55)
            ph = r.uniform(0, 1)
            op = (.55 + .45 * abs(A.w(t, 9 + r.uniform(0, 6), ph))) if on else .25
            col = SVET if on else "#4a5a68"
            s += (f'<rect x="{ox:.0f}" y="{oy:.0f}" width="84" height="76" rx="5"'
                  f' fill="{col}" opacity="{op:.2f}" stroke="{K}" stroke-width="4"/>')
    return s


def kartoshka(x, y, t, n=9, seed=6, s_=1.0):
    r = random.Random(seed)
    s = ""
    for i in range(n):
        xx = x + r.uniform(-90, 90) * s_; yy = y + r.uniform(-20, 20) * s_
        s += (f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="{r.uniform(20,30)*s_:.0f}"'
              f' ry="{r.uniform(15,22)*s_:.0f}" fill="url(#glina)" {o(4)}/>')
    return s


def ryabina(x, y, t, s_=1.0, n=5):
    s = ""
    for i in range(n):
        a = -1.0 + i * .45
        ex = x + math.cos(a) * 110 * s_ + 8 * A.w(t, 4.0, i * .2)
        ey = y - 60 * s_ + math.sin(a) * 40 * s_
        s += (f'<path d="M{x:.0f},{y:.0f} Q{(x+ex)/2:.0f},{y-60*s_:.0f} {ex:.0f},{ey:.0f}"'
              f' fill="none" stroke="#6b4428" stroke-width="{9*s_:.0f}"/>')
        for j in range(7):
            s += (f'<circle cx="{ex + (j%3-1)*16*s_:.0f}" cy="{ey + (j//3)*16*s_:.0f}"'
                  f' r="{8*s_:.0f}" fill="{KRAS}" {o(2)}/>')
    return s


def vinetka(op=.42):
    return (f'<radialGradient id="vig" cx=".5" cy=".5" r=".72">'
            f'<stop offset=".55" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="{op}"/></radialGradient>'
            f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')


# ── НАПОЛНИТЕЛИ ВТОРОГО ПЛАНА ──────────────────────────────────────────────
# Пустая половина кадра — главный брак первого прохода: «одна сцена, и всё,
# и гоняешь на ней» (R-0010, R-0019). Эти функции закрывают дальний план
# предметами, которые НЕ жалко прикрыть окном вставки.

def mebel_hlam(x, y, w_, t, seed=13):
    """Нейтральный второй план: сундук, лавка, корзина, вёдра."""
    r = random.Random(seed)
    s = ten(x + w_ * .3, y + 10, w_ * .2, 16, .4)
    s += (f'<rect x="{x:.0f}" y="{y-150:.0f}" width="{w_*.38:.0f}" height="150" rx="10"'
          f' fill="url(#derev)" {o(7)}/>')
    s += (f'<path d="M{x:.0f},{y-150:.0f} q{w_*.19:.0f},-56 {w_*.38:.0f},0 Z"'
          f' fill="url(#med)" {o(6)}/>')
    s += (f'<rect x="{x+w_*.46:.0f}" y="{y-110:.0f}" width="{w_*.3:.0f}" height="22" rx="8"'
          f' fill="url(#derev)" {o(5)}/>')
    s += (f'<rect x="{x+w_*.5:.0f}" y="{y-88:.0f}" width="20" height="88" fill="url(#derev)" {o(4)}/>'
          f'<rect x="{x+w_*.72:.0f}" y="{y-88:.0f}" width="20" height="88" fill="url(#derev)" {o(4)}/>')
    bx = x + w_ * .86
    s += (f'<path d="M{bx-46:.0f},{y:.0f} l8,-96 q38,-14 76,0 l8,96 Z" fill="url(#solom)" {o(6)}/>')
    for i in range(3):
        s += f'<path d="M{bx-44:.0f},{y-26-i*28:.0f} q44,12 88,0" fill="none" stroke="#a07c2e" stroke-width="6"/>'
    return s


def utvar_izby(x, y, w_, t, seed=3):
    """Утварь избы. Набор и высоты РАЗНЫЕ по seed: одинаковая полка в шести
    избах подряд читается как одна и та же сцена (R-0021)."""
    r = random.Random(seed)
    s = ""
    y = y + r.choice((-60, 0, 40, 90))
    dve = r.random() < .7
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="20" rx="6"'
          f' fill="url(#derev)" {o(6)}/>')
    s += (f'<path d="M{x+30:.0f},{y+20:.0f} l22,34 M{x+w_-52:.0f},{y+20:.0f} l-22,34"'
          f' {o(5)} fill="none"/>')
    n = max(3, int(w_ / 120))
    for i in range(n):
        xx = x + 60 + i * (w_ - 120) / max(1, n - 1)
        k = r.random()
        if k < .22:
            s += (f'<rect x="{xx-36:.0f}" y="{y-86:.0f}" width="72" height="86" rx="8"'
                  f' fill="url(#solom)" {o(5)}/>'
                  f'<path d="M{xx-36:.0f},{y-58:.0f} h72" stroke="#a07c2e" stroke-width="5"/>')
        elif k < .34:
            s += karavay(xx, y - 6, .46, False)
        elif k < .46:
            s += (f'<path d="M{xx-30:.0f},{y-4:.0f} v-70 q30,-16 60,0 v70 Z" fill="url(#krem)" {o(5)}/>'
                  f'<path d="M{xx+30:.0f},{y-60:.0f} q28,16 0,38" fill="none" stroke="{KREM}" stroke-width="10"/>')
        else:
            s += krynka(xx, y - 6, r.uniform(.56, .86))
    if dve:
        y2 = y - r.choice((160, 190, 230))
        s += (f'<rect x="{x+r.choice((0,40,90)):.0f}" y="{y2:.0f}" width="{w_-80:.0f}" height="18" rx="6"'
              f' fill="url(#derev)" {o(5)}/>')
        for i in range(max(2, n - 1)):
            xx = x + 110 + i * (w_ - 220) / max(1, n - 2)
            s += krynka(xx, y2 - 6, r.uniform(.44, .6))
    else:
        y2 = y - 170
        s += _mebel_hlam(x + 20, y - 150, w_ * .7, t, seed + 1)
    if r.random() < .75:
        kach = 2.0 * A.w(t, 5.0, .2)
        rx = x + w_ * r.choice((.14, .5, .82))
        s += (f'<g transform="rotate({kach:.2f} {rx:.0f} {y2-230:.0f})">'
              f'<path d="M{rx-46:.0f},{y2-230:.0f} h92 l-12,250 h-68 Z" fill="url(#rush)" {o(5)}/>'
              f'<rect x="{rx-40:.0f}" y="{y2-150:.0f}" width="80" height="12" fill="{TKAN}" opacity=".8"/>'
              f'<rect x="{rx-40:.0f}" y="{y2-40:.0f}" width="80" height="12" fill="{TKAN}" opacity=".8"/></g>')
    if r.random() < .7:
        for i in range(r.choice((2, 3))):
            px = x + 70 + i * (w_ * r.uniform(.22, .34))
            kach = 1.8 * A.w(t, 4.2 + i * .4, i * .2)
            s += f'<g transform="rotate({kach:.2f} {px:.0f} {y2-300:.0f})">'
            for j in range(5):
                s += (f'<path d="M{px:.0f},{y2-300:.0f} q{-18+j*9:.0f},60 {-12+j*6:.0f},110"'
                      f' fill="none" stroke="{["#6f8c4a","#8a9a58","#5c7a40"][j%3]}" stroke-width="6"/>')
            s += f'<path d="M{px-18:.0f},{y2-296:.0f} q18,-14 36,0" fill="none" stroke="{TKAN}" stroke-width="8"/></g>'
    return s


def utvar_pekarni(x, y, w_, t, seed=5):
    """Второй план пекарни: хлебные лопаты, мешки муки, полка с хлебами, бочка."""
    s = ""
    for i in range(2):
        lx = x + 40 + i * 96
        s += (f'<rect x="{lx:.0f}" y="{y-470:.0f}" width="44" height="380" rx="10"'
              f' fill="url(#dosk)" {o(5)}/>'
              f'<path d="M{lx-26:.0f},{y-470:.0f} h96 v-74 q-48,-34 -96,0 Z" fill="url(#dosk)" {o(5)}/>')
    s += (f'<rect x="{x+230:.0f}" y="{y-330:.0f}" width="{max(180,w_*.42):.0f}" height="18" rx="6"'
          f' fill="url(#derev)" {o(5)}/>')
    for i in range(3):
        s += karavay(x + 290 + i * 110, y - 336, .5, False)
    for i in range(2):
        mx = x + 330 + i * 120
        s += (f'{ten(mx, y+6, 54, 11, .4)}'
              f'<path d="M{mx-52:.0f},{y:.0f} q-12,-128 52,-140 q64,12 52,140 Z" fill="#d8c8a4" {o(5)}/>'
              f'<path d="M{mx-24:.0f},{y-136:.0f} q24,-16 48,0" fill="none" stroke="{TKAN}" stroke-width="8"/>'
              f'<path d="M{mx-40:.0f},{y-70:.0f} q40,12 80,0" fill="none" stroke="#b8a883" stroke-width="5"/>')
    bx = x + w_ - 120
    s += (f'{ten(bx, y+8, 80, 14, .4)}'
          f'<path d="M{bx-78:.0f},{y:.0f} l10,-210 q68,-22 136,0 l10,210 Z" fill="url(#derev)" {o(6)}/>')
    for yy in (y - 40, y - 130):
        s += f'<path d="M{bx-80:.0f},{yy:.0f} q78,16 160,0" fill="none" stroke="{ZHELEZ}" stroke-width="10"/>'
    return s


def svody(t, col="#4b443b", n=3):
    """Своды и балки каменного интерьера — без них стена читается обоями."""
    s = ""
    for i in range(n):
        x0 = -200 + i * (W + 400) / n
        s += (f'<path d="M{x0:.0f},0 q{(W+400)/n/2:.0f},260 {(W+400)/n:.0f},0"'
              f' fill="none" stroke="{col}" stroke-width="34" opacity=".85"/>')
    s += f'<rect width="{W}" height="26" fill="{col}" opacity=".9"/>'
    for i in range(5):
        s += (f'<path d="M{-120+i*440},26 l300,240" stroke="#5a4028" stroke-width="26" opacity=".7"/>')
    return s


def ulica_dal(x, y, w_, t, zima=True, seed=7):
    """Дальний план улицы: избы силуэтами, деревья, забор, стог."""
    r = random.Random(seed)
    s = ""
    for i in range(4):
        bx = x + i * (w_ / 4) + r.uniform(-20, 20)
        bw = w_ / 4 * .72
        bh = bw * .56
        s += f'<rect x="{bx:.0f}" y="{y-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="#3b4254" opacity=".9"/>'
        s += (f'<path d="M{bx-bw*.1:.0f},{y-bh:.0f} L{bx+bw/2:.0f},{y-bh-bw*.34:.0f}'
              f' L{bx+bw*1.1:.0f},{y-bh:.0f} Z" fill="#2f3646" opacity=".9"/>')
        on = r.random() < .6
        s += (f'<rect x="{bx+bw*.3:.0f}" y="{y-bh*.66:.0f}" width="{bw*.22:.0f}"'
              f' height="{bh*.3:.0f}" fill="{SVET if on else "#39415a"}"'
              f' opacity="{.5+.4*abs(A.w(t,6+i,i*.2)) if on else .3:.2f}"/>')
    for i in range(6):
        tx = x + 40 + i * (w_ / 6) + r.uniform(-14, 14)
        th = r.uniform(70, 150)
        s += (f'<path d="M{tx:.0f},{y:.0f} l{-th*.26:.0f},0 l{th*.26:.0f},{-th:.0f}'
              f' l{th*.26:.0f},{th:.0f} Z" fill="#2a3348" opacity=".85"/>')
    if zima:
        s += (f'<path d="M{x:.0f},{y:.0f} q{w_*.25:.0f},-18 {w_*.5:.0f},-6'
              f' q{w_*.25:.0f},12 {w_*.5:.0f},-10 L{x+w_:.0f},{y+60:.0f} L{x:.0f},{y+60:.0f} Z"'
              f' fill="#cfd8e6" opacity=".9"/>')
    return s


def kvartira_veschi(x, y, w_, t, seed=11):
    """Второй план квартиры: сервант, ковёр на стене, полка с книгами, часы."""
    s = ""
    s += (f'<rect x="{x:.0f}" y="{y-520:.0f}" width="{w_*.46:.0f}" height="330" rx="10"'
          f' fill="{TKAN}" opacity=".85" {o(6)}/>')
    for i in range(4):
        s += (f'<path d="M{x+20:.0f},{y-500+i*80:.0f} q{w_*.21:.0f},34 {w_*.42:.0f},0"'
              f' fill="none" stroke="{ZOL}" stroke-width="7" opacity=".7"/>')
    sx = x + w_ * .54
    s += ten(sx + w_ * .2, y + 12, w_ * .18, 18, .45)
    s += (f'<rect x="{sx:.0f}" y="{y-420:.0f}" width="{w_*.42:.0f}" height="420" rx="10"'
          f' fill="url(#derev)" {o(7)}/>')
    s += (f'<rect x="{sx+18:.0f}" y="{y-396:.0f}" width="{w_*.42-36:.0f}" height="190" rx="8"'
          f' fill="url(#stekl)" opacity=".75" {o(5)}/>')
    for i in range(5):
        s += (f'<rect x="{sx+36+i*34:.0f}" y="{y-376:.0f}" width="26" height="150" rx="4"'
              f' fill="{[TKAN, ZEL2, TKAN2, MED, "#6b4428"][i]}" {o(3)}/>')
    s += (f'<rect x="{sx+18:.0f}" y="{y-190:.0f}" width="{w_*.42-36:.0f}" height="170" rx="8"'
          f' fill="{DOSKA2}" {o(5)}/>')
    s += hodiki(x + w_ * .5, y - 640, t, .8)
    return s


# ── РАЗМЕТКА СЛОЁВ ─────────────────────────────────────────────────────────
# Кирпичики сами сообщают камере свою глубину. Декорации об этом не знают —
# поэтому параллакс получили все 77 сцен без переписывания каждой.
_nebo, _oblaka, _tuman = nebo, oblaka, tuman
_ulica_dal, _panelka, _sneg_lezhit = ulica_dal, panelka, sneg_lezhit
_utvar_izby, _utvar_pekarni = utvar_izby, utvar_pekarni
_kvartira_veschi, _mebel_hlam = kvartira_veschi, mebel_hlam
_ramka_pp, _sneg_letit, _vinetka = ramka_pp, sneg_letit, vinetka


def _sloy(f, z):
    def g(*a, **k):
        return SL(z, f(*a, **k))
    g.__name__ = f.__name__
    g.__doc__ = f.__doc__
    return g


nebo = _sloy(_nebo, Z_NEBO)
oblaka = _sloy(_oblaka, Z_NEBO)
tuman = _sloy(_tuman, Z_DAL)
ulica_dal = _sloy(_ulica_dal, Z_DAL)
panelka = _sloy(_panelka, Z_DAL)
sneg_lezhit = _sloy(_sneg_lezhit, Z_DAL)
utvar_izby = _sloy(_utvar_izby, Z_SRED)
utvar_pekarni = _sloy(_utvar_pekarni, Z_SRED)
kvartira_veschi = _sloy(_kvartira_veschi, Z_SRED)
mebel_hlam = _sloy(_mebel_hlam, Z_SRED)
ramka_pp = _sloy(_ramka_pp, Z_PERED)
sneg_letit = _sloy(_sneg_letit, Z_LETIT)
vinetka = _sloy(_vinetka, Z_FIX)


# ── СВЕТ: блик, бегущий блик, воздух комнаты (C16/K17, K5, K15) ────────────
def blik(cx, cy, t, s_=1.0, col="#bcd8ff", teplo_col=None, op=1.0):
    """Анаморфный блик в объектив: холодная полоса через источник, тёплый
    ореол, белое ядро, кольца по оси (C16/K17)."""
    tc = teplo_col or SVET
    puls = .82 + .18 * abs(A.w(t, 2.6))
    s = f'<g opacity="{op*puls:.2f}">'
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{620*s_:.0f}" ry="{9*s_:.0f}"'
          f' fill="{col}" opacity=".5"/>')
    s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{300*s_:.0f}" ry="{4*s_:.0f}"'
          f' fill="#ffffff" opacity=".65"/>')
    s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{86*s_:.0f}" fill="{tc}" opacity=".3"/>'
    s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{30*s_:.0f}" fill="#ffffff" opacity=".8"/>'
    dx, dy = (W / 2 - cx), (H / 2 - cy)
    for i, (k, r_, c) in enumerate(((.45, 44, tc), (.78, 30, col), (1.15, 56, tc), (1.5, 22, col))):
        s += (f'<circle cx="{cx+dx*k:.0f}" cy="{cy+dy*k:.0f}" r="{r_*s_:.0f}" fill="{c}"'
              f' opacity="{.16-.02*i:.2f}"/>')
    return s + "</g>"


def begushchiy_blik(t, period=9.0, phase=0.0, op=.16, shir=420):
    """Мягкая диагональная полоса пробегает по кадру (K5)."""
    k = ((t / period) + phase) % 1.0
    x = -600 + k * (W + 1200)
    return (f'<g opacity="{op:.2f}"><path d="M{x:.0f},-120 l{shir},0 l{-shir*.75:.0f},{H+240}'
            f' l{-shir:.0f},0 Z" fill="#ffffff"/></g>')


def vozduh(cx, cy, t, teplo_r=900, bok=.28):
    """Воздух сцены (K15): нимб от источника, притемнённый бок, общий тон."""
    s = teplo(cx, cy, teplo_r, teplo_r * .8, .55)
    s += (f'<linearGradient id="bok{int(cx)}" x1="0" y1="0" x2="1" y2="0">'
          f'<stop offset="0" stop-color="#0b1018" stop-opacity="0"/>'
          f'<stop offset="1" stop-color="#0b1018" stop-opacity="{bok}"/></linearGradient>'
          f'<rect width="{W}" height="{H}" fill="url(#bok{int(cx)})"/>')
    return s
