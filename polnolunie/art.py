# -*- coding: utf-8 -*-
"""Рисунки формата ПОЛНОЛУНИЕ как ФУНКЦИИ ВРЕМЕНИ. Плоский мультяшный
вектор, толстый контур, палитра «Года Козы» плюс ночная ветка.
Зум делается окном просмотра (правило №1 «Козы»), внутри кадра всё живёт:
звёзды мерцают, Луна моргает, дымок идёт, хвост качается, волны воя бегут.
Эффекты текста рисуются ЗДЕСЬ ЖЕ, покадрово, а не кладутся картинкой сверху."""
import math
import anim as A
import tekst as T

K = "#17130f"
NOCH, NOCH2 = "#16203a", "#22304a"
VIOLET = "#4a3b86"
SER, SVET, ZOL, ORA = "#eef2f7", "#ffd36e", "#c9922f", "#e07f23"
KRAS, KREM, PERS, TERRA = "#d6202f", "#e4d4b6", "#efb07a", "#a8512c"
ZEL, ZEL2 = "#6abf4b", "#4e7a35"
W, H = 1920, 1080


def o(w=7, col=None):
    return f'stroke="{col or K}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


# ─────────────────────────────── НЕБО ───────────────────────────────
def stars(n, w, h, t, seed=1, r0=1.6, r1=3.4, col="#ffffff", op=.9, tw=False):
    """Звёзды по сетке со сдвигом — одинаковые в каждом кадре, мерцают фазой."""
    s = ""
    x, y = seed * 37 % w, seed * 61 % h
    for i in range(n):
        x = (x * 1.07 + 97 * (i + seed)) % w
        y = (y * 1.11 + 53 * (i + seed * 3)) % h
        r = r0 + (i * 7 % 10) / 10 * (r1 - r0)
        oo = op * (0.55 + 0.45 * A.w(t, 2.8 + (i % 5) * 0.37, i * 0.21)) if tw else op
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{col}" opacity="{oo:.2f}"/>'
    return s


def clouds(w, h, t, y0=0.34, sp=7.0, col="#1b2744", op=.85):
    """Средний слой: облака медленно едут, два пера с разной скоростью."""
    s = ""
    for k, (mul, oy, sc) in enumerate(((1.0, 0.0, 1.0), (0.62, 0.11, 0.7))):
        dx = (-t * sp * mul) % (w + 900) - 450
        yy = h * (y0 + oy)
        s += (f'<path d="M{dx-20:.0f},{yy:.0f} q{120*sc:.0f},{-50*sc:.0f} {260*sc:.0f},{-10*sc:.0f}'
              f' q{140*sc:.0f},{40*sc:.0f} {380*sc:.0f},{-20*sc:.0f} l0,{80*sc:.0f}'
              f' q{-240*sc:.0f},{70*sc:.0f} {-380*sc:.0f},{20*sc:.0f}'
              f' q{-150*sc:.0f},{-50*sc:.0f} {-260*sc:.0f},0 Z"'
              f' fill="{col}" opacity="{op*(1-k*0.35):.2f}"/>')
    return s


def sky(w, h, t, mw=True, seed=1, cl=True):
    s = f'<rect width="{w}" height="{h}" fill="url(#sky{seed})"/>'
    if mw:
        s += (f'<path d="M0,{h*.22:.0f} Q{w*.4:.0f},{h*.04:.0f} {w},{h*.3:.0f} '
              f'L{w},{h*.46:.0f} Q{w*.4:.0f},{h*.2:.0f} 0,{h*.4:.0f} Z"'
              f' fill="{VIOLET}" opacity=".35"/>')
    s += stars(26, w, h, t, seed, 1.2, 2.4, "#cfe0ff", .55)
    s += stars(16, w, h, t, seed + 4, 2.0, 3.8, "#ffffff", .95, tw=True)
    if cl:
        s += clouds(w, h, t)
    return s


def sky_def(seed=1):
    return (f'<linearGradient id="sky{seed}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#101a33"/><stop offset=".55" stop-color="{NOCH}"/>'
            f'<stop offset="1" stop-color="#243352"/></linearGradient>')


def hills(w, h, top=.72, col=NOCH2, col2="#1b2740"):
    y = h * top
    return (f'<path d="M0,{y:.0f} Q{w*.18:.0f},{y-h*.12:.0f} {w*.42:.0f},{y-h*.02:.0f} '
            f'Q{w*.62:.0f},{y+h*.05:.0f} {w*.8:.0f},{y-h*.07:.0f} '
            f'Q{w*.93:.0f},{y-h*.12:.0f} {w},{y-h*.04:.0f} L{w},{h} L0,{h} Z" fill="{col2}"/>'
            f'<path d="M0,{y+h*.1:.0f} Q{w*.3:.0f},{y-h*.01:.0f} {w*.55:.0f},{y+h*.09:.0f} '
            f'Q{w*.8:.0f},{y+h*.17:.0f} {w},{y+h*.06:.0f} L{w},{h} L0,{h} Z" fill="{col}"/>')


def firs(w, y, xs, sc=1.0, col="#111a2c"):
    s = ""
    for i, x in enumerate(xs):
        hh = (70 + (i * 13) % 40) * sc
        ww = hh * .42
        s += (f'<path d="M{x:.0f},{y-hh:.0f} L{x-ww:.0f},{y:.0f} L{x+ww:.0f},{y:.0f} Z" fill="{col}"/>'
              f'<path d="M{x:.0f},{y-hh*1.25:.0f} L{x-ww*.7:.0f},{y-hh*.45:.0f} '
              f'L{x+ww*.7:.0f},{y-hh*.45:.0f} Z" fill="{col}"/>')
    return s


# ─────────────────────────────── ЛУНА ───────────────────────────────
def moon_defs(p="m"):
    return (f'<radialGradient id="{p}g" cx=".36" cy=".32" r=".78">'
            f'<stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="{SER}"/>'
            f'<stop offset="1" stop-color="#c3cee0"/></radialGradient>'
            f'<radialGradient id="{p}h" cx=".5" cy=".5" r=".5">'
            f'<stop offset=".55" stop-color="{SVET}" stop-opacity=".40"/>'
            f'<stop offset="1" stop-color="{SVET}" stop-opacity="0"/></radialGradient>')


def craters(cx, cy, r):
    c = [(-.42, -.30, .13), (.30, -.44, .09), (.46, .20, .12),
         (-.26, .44, .10), (.04, .56, .06), (-.56, .14, .07)]
    s = ""
    for dx, dy, dr in c:
        s += (f'<circle cx="{cx+dx*r:.0f}" cy="{cy+dy*r:.0f}" r="{dr*r:.0f}"'
              f' fill="#dae2ee" opacity=".55"/>'
              f'<path d="M{cx+dx*r-dr*r:.1f},{cy+dy*r:.1f} a{dr*r:.1f},{dr*r:.1f} 0 0 0'
              f' {dr*r*2:.1f},0" fill="#c6d0e0" opacity=".32"/>')
    return s


def face(cx, cy, r, mood="smile", shut=False):
    """Лицо Луны. shut=True — глаза закрыты (моргание приходит снаружи)."""
    ex, ey, er = r * .30, r * .10, r * .085
    s = (f'<ellipse cx="{cx-ex*1.75:.0f}" cy="{cy+r*.30:.0f}" rx="{r*.15:.0f}"'
         f' ry="{r*.09:.0f}" fill="{PERS}" opacity=".55"/>'
         f'<ellipse cx="{cx+ex*1.75:.0f}" cy="{cy+r*.30:.0f}" rx="{r*.15:.0f}"'
         f' ry="{r*.09:.0f}" fill="{PERS}" opacity=".55"/>')
    for sx in (-1, 1):
        if mood == "wink" and sx > 0:
            s += (f'<path d="M{cx+ex-er*1.2:.0f},{cy-ey:.0f} q{er*1.2:.0f},{er*1.1:.0f}'
                  f' {er*2.4:.0f},0" fill="none" {o(max(4, r*.05))}/>')
        elif shut or mood == "yawn":
            s += (f'<path d="M{cx+sx*ex-er*1.2:.0f},{cy-ey:.0f} q{er*1.2:.0f},{er*1.0:.0f}'
                  f' {er*2.4:.0f},0" fill="none" {o(max(4, r*.05))}/>')
        else:
            s += (f'<ellipse cx="{cx+sx*ex:.0f}" cy="{cy-ey:.0f}" rx="{er:.0f}"'
                  f' ry="{er*1.18:.0f}" fill="{K}"/>'
                  f'<circle cx="{cx+sx*ex-er*.34:.0f}" cy="{cy-ey-er*.42:.0f}"'
                  f' r="{er*.33:.0f}" fill="#ffffff"/>')
    bw = er * 2.1
    for sx in (-1, 1):
        s += (f'<path d="M{cx+sx*ex-bw*.5:.0f},{cy-r*.26:.0f} q{bw*.5:.0f},{-r*.07:.0f}'
              f' {bw:.0f},{r*.01:.0f}" fill="none" {o(max(4, r*.045))}/>')
    mw = r * .34
    if mood == "oh":
        s += f'<ellipse cx="{cx:.0f}" cy="{cy+r*.34:.0f}" rx="{mw*.42:.0f}" ry="{mw*.55:.0f}" fill="{K}"/>'
    else:
        s += (f'<path d="M{cx-mw:.0f},{cy+r*.24:.0f} q{mw:.0f},{r*.26:.0f} {mw*2:.0f},0"'
              f' fill="none" {o(max(5, r*.055))}/>'
              f'<path d="M{cx-mw*1.08:.0f},{cy+r*.235:.0f} l{-r*.05:.0f},{-r*.03:.0f}"'
              f' {o(max(4, r*.04))}/>'
              f'<path d="M{cx+mw*1.08:.0f},{cy+r*.235:.0f} l{r*.05:.0f},{-r*.03:.0f}"'
              f' {o(max(4, r*.04))}/>')
    return s


def moon(cx, cy, r, t, mood="smile", halo=1.0, p="m", ph=0.0):
    """halo — сила ореола 0..1.4: им и делается «наливается светом»."""
    s = ""
    if halo > 0.01:
        s += (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*(1.18+0.3*halo):.1f}"'
              f' fill="url(#{p}h)" opacity="{min(1.0, halo):.2f}"/>')
    s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="url(#{p}g)" {o(8)}/>'
    s += craters(cx, cy, r)
    s += face(cx, cy, r, mood, A.blink(t, 4.6, ph))
    return s


# ─────────────────────────────── СОВА ───────────────────────────────
def owl(cx, cy, t, s=1.0):
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})">'
    g += (f'<path d="M-200,150 Q-40,132 200,146" fill="none" stroke="{TERRA}"'
          f' stroke-width="26" stroke-linecap="round"/>'
          f'<path d="M-200,150 Q-40,132 200,146" fill="none" {o(8)} opacity=".5"/>')
    g += f'<path d="M-30,120 L0,185 L30,120 Z" fill="{TERRA}" {o(7)}/>'
    br = 1 + 0.012 * A.w(t, 3.4)              # дыхание
    g += f'<g transform="scale({br:.4f},{2-br:.4f})">'
    g += f'<ellipse cx="0" cy="40" rx="105" ry="118" fill="{TERRA}" {o(8)}/>'
    g += f'<ellipse cx="0" cy="62" rx="68" ry="88" fill="{PERS}"/>'
    for i in range(3):
        for j in range(4 - i % 2):
            x = -42 + j * 28 + (14 if i % 2 else 0)
            y = 30 + i * 30
            g += (f'<path d="M{x-13},{y} q13,16 26,0" fill="none" stroke="{TERRA}"'
                  f' stroke-width="5" opacity=".65"/>')
    g += '</g>'
    g += (f'<path d="M-82,-72 L-58,-116 L-30,-82 Z" fill="{TERRA}" {o(7)}/>'
          f'<path d="M82,-72 L58,-116 L30,-82 Z" fill="{TERRA}" {o(7)}/>')
    g += (f'<path d="M-104,10 q-34,52 -14,104 q22,-16 30,-54" fill="{TERRA}" {o(7)}/>'
          f'<path d="M104,10 q34,52 14,104 q-22,-16 -30,-54" fill="{TERRA}" {o(7)}/>')
    g += f'<ellipse cx="0" cy="-44" rx="94" ry="76" fill="{KREM}" {o(8)}/>'
    shut = A.blink(t, 3.9, 0.2)
    for sx in (-1, 1):
        g += (f'<circle cx="{sx*42}" cy="-50" r="37" fill="#ffffff" {o(7)}/>'
              f'<circle cx="{sx*42}" cy="-50" r="37" fill="none" stroke="{ZOL}" stroke-width="7"/>')
        if shut:
            g += (f'<path d="M{sx*42-20},-50 q20,16 40,0" fill="none" {o(6)}/>')
        else:
            g += (f'<circle cx="{sx*42+4}" cy="-46" r="15" fill="{K}"/>'
                  f'<circle cx="{sx*42-2}" cy="-53" r="5.5" fill="#ffffff"/>')
    g += f'<path d="M-6,-50 h12" {o(7, ZOL)}/>'
    g += f'<path d="M-79,-50 l-18,-6" {o(6, ZOL)}/><path d="M79,-50 l18,-6" {o(6, ZOL)}/>'
    g += (f'<path d="M-72,-92 q30,-16 56,-6" fill="none" {o(8)}/>'
          f'<path d="M72,-92 q-30,-16 -56,-6" fill="none" {o(8)}/>')
    g += f'<path d="M0,-26 L-15,-6 L0,4 L15,-6 Z" fill="{ORA}" {o(6)}/>'
    g += (f'<path d="M-34,148 l0,-18 M-34,148 l-16,10 M-34,148 l0,12 M-34,148 l16,10" {o(7, ZOL)}/>'
          f'<path d="M34,148 l0,-18 M34,148 l-16,10 M34,148 l0,12 M34,148 l16,10" {o(7, ZOL)}/>')
    # указка постукивает по схеме
    tap = 34 + 5 * A.w(t, 2.2)
    g += (f'<g transform="rotate({tap:.2f} 126 78)"><rect x="120" y="-54" width="12"'
          f' height="208" rx="6" fill="{KREM}" {o(6)}/>'
          f'<rect x="115" y="-72" width="22" height="24" rx="5" fill="{KRAS}" {o(6)}/></g>')
    g += (f'<ellipse cx="118" cy="86" rx="26" ry="20" fill="{TERRA}" {o(7)}'
          f' transform="rotate(18 118 86)"/>')
    return g + '</g>'


# ─────────────────────── КОТ НА КРЫШЕ ───────────────────────
def cat(cx, cy, t, s=1.0):
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})">'
    rot = -9 * (0.5 + 0.5 * A.w(t, 3.4))       # хвост качается
    g += (f'<g transform="rotate({rot:.2f} 66 22)"><path d="M66,22 q58,10 54,-54'
          f' q-2,-30 -26,-26" fill="none" stroke="{K}" stroke-width="20"'
          f' stroke-linecap="round"/></g>')
    br = 1 + 0.016 * A.w(t, 3.0, .3)
    g += f'<g transform="scale({br:.4f},{2-br:.4f})">'
    g += f'<path d="M-62,34 q-16,-96 48,-96 q64,0 54,96 Z" fill="{K}"/>'
    g += f'<ellipse cx="-6" cy="34" rx="66" ry="16" fill="{K}"/>'
    g += '</g>'
    g += (f'<ellipse cx="-40" cy="36" rx="18" ry="11" fill="{K}"/>'
          f'<ellipse cx="18" cy="36" rx="18" ry="11" fill="{K}"/>')
    nod = 2.2 * A.w(t, 5.2, .15)
    g += f'<g transform="translate(0,{nod:.2f})">'
    g += f'<circle cx="-14" cy="-78" r="42" fill="{K}"/>'
    g += (f'<path d="M-50,-104 L-56,-146 L-22,-120 Z" fill="{K}"/>'
          f'<path d="M20,-104 L30,-144 L-6,-120 Z" fill="{K}"/>'
          f'<path d="M-45,-108 L-48,-132 L-29,-118 Z" fill="{TERRA}" opacity=".75"/>'
          f'<path d="M18,-108 L24,-130 L3,-118 Z" fill="{TERRA}" opacity=".75"/>')
    glow = .72 + .28 * A.w(t, 2.2)
    shut = A.blink(t, 5.4, .45, 0.2)
    for dx in (-30, 2):
        if shut:
            g += f'<path d="M{dx-11},-84 q11,9 22,0" fill="none" {o(5, "#8a8f98")}/>'
        else:
            g += (f'<ellipse cx="{dx}" cy="-84" rx="13" ry="16" fill="{SVET}"'
                  f' opacity="{glow:.2f}"/>'
                  f'<ellipse cx="{dx}" cy="-84" rx="4" ry="14" fill="{K}"/>')
    g += f'<path d="M-14,-62 l-7,-7 l14,0 Z" fill="{PERS}"/>'
    for dy, ln in ((-64, 30), (-57, 29), (-50, 26)):
        g += (f'<path d="M-30,{dy} l-{ln},-4" stroke="#dfe6f4" stroke-width="3" opacity=".8"/>'
              f'<path d="M4,{dy} l{ln},-4" stroke="#dfe6f4" stroke-width="3" opacity=".8"/>')
    return g + '</g></g>'


def roof(ax, ay, bottom, half=None, col=TERRA):
    half = half or (bottom - ay) * 1.9
    s = (f'<path d="M{ax-half:.0f},{bottom:.0f} L{ax:.0f},{ay:.0f} L{ax+half:.0f},{bottom:.0f} Z"'
         f' fill="{col}" {o(8)}/>')
    n = max(3, int((bottom - ay) / 56))
    for i in range(1, n + 1):
        yy = ay + (bottom - ay) * i / (n + 1)
        dx = (yy - ay) * half / (bottom - ay)
        s += (f'<path d="M{ax-dx*.92:.0f},{yy:.0f} L{ax+dx*.92:.0f},{yy:.0f}"'
              f' stroke="{K}" stroke-width="4" opacity=".3"/>')
    return s


def chimney(x, y, t, w=74, h=120):
    """Труба с живым дымком: три струйки ползут вверх и расходятся."""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#7a4a2e" {o(8)}/>'
         f'<rect x="{x-10}" y="{y-14}" width="{w+20}" height="26" rx="6" fill="{TERRA}" {o(7)}/>')
    s += f'<g stroke="#cfd8ea" stroke-width="11" fill="none" stroke-linecap="round">'
    for i in range(3):
        ph = i * .34
        p = ((t * .23) + ph) % 1.0
        yy = y - 26 - p * 230
        fade = min(1.0, p * 3.4) * max(0.0, 1 - max(0.0, p - .5) / .5)
        if fade <= .03:
            continue
        a = 26 * A.w(t, 2.6, ph)
        s += (f'<path d="M{x+w*.5+(i-1)*16:.0f},{yy:.0f} q{a:.0f},-42 {a*.3:.0f},-84"'
              f' opacity="{fade*.55:.2f}"/>')
    return s + '</g>'


def houses(w, y, t=0.0, col="#0d1424"):
    s, x = "", -40
    for i in range(9):
        bw = 120 + (i * 37) % 110
        bh = 90 + (i * 53) % 140
        s += f'<rect x="{x:.0f}" y="{y-bh:.0f}" width="{bw}" height="{bh+40}" fill="{col}"/>'
        s += (f'<path d="M{x-10:.0f},{y-bh:.0f} L{x+bw*.5:.0f},{y-bh-46:.0f} '
              f'L{x+bw+10:.0f},{y-bh:.0f} Z" fill="{col}"/>')
        if i % 2:
            s += f'<rect x="{x+bw*.6:.0f}" y="{y-bh-64:.0f}" width="26" height="46" fill="{col}"/>'
        for r in range(2):
            for c in range(2):
                if (i + r + c) % 3:
                    base = .22 if (i + c) % 2 else .5
                    # редкое окно гаснет и зажигается — город живой
                    flick = 1.0 if (i + r * 3 + c) % 5 else (.25 + .75 * (A.w(t, 6.4, i * .2) > 0))
                    s += (f'<rect x="{x+22+c*52:.0f}" y="{y-bh+26+r*44:.0f}" width="26"'
                          f' height="30" rx="4" fill="{SVET}" opacity="{base*flick:.2f}"/>')
        x += bw + 46
    return s


# ─────────────────────── ЗВЕЗДОЧЁТ ───────────────────────
def star(x, y, r, col=SVET, op=1.0, k=5):
    pts = []
    for i in range(k * 2):
        rr = r if i % 2 == 0 else r * .44
        a = -math.pi / 2 + i * math.pi / k
        pts.append(f"{x + rr*math.cos(a):.1f},{y + rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{col}" opacity="{op}"/>'


# ─────────────────────── ВОЛК ───────────────────────
def wolf(cx, cy, t, s=1.0, howl=True):
    """Воющий волк в профиль. Собран из плотных тел (круп, грудь, шея, череп,
    морда), а не из одной длинной кривой: три предыдущих варианта читались
    таксой, конём и ламой — виновата была ДЛИННАЯ ТОНКАЯ ШЕЯ.
    Земля — y=0, холка −236, нос −384. Лунный кант идёт по верхнему краю."""
    br = 1 + 0.016 * A.w(t, 2.4)
    head = 2.2 * A.w(t, 3.6, .1)
    sw = 7 * A.w(t, 4.1)
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})">'
    L = f'fill="none" stroke="{K}" stroke-linecap="round" stroke-linejoin="round"'
    D = 'fill="none" stroke="#0b0907" stroke-linecap="round" stroke-linejoin="round"'
    # хвост полотном
    g += (f'<g transform="rotate({sw:.2f} -176 -176)"><path d="M-176,-176 '
          f'C-234,-180 -268,-142 -258,-80 C-256,-58 -250,-48 -238,-44 '
          f'C-248,-64 -250,-90 -238,-116 C-226,-138 -200,-154 -166,-152 Z"'
          f' fill="{K}"/></g>')
    g += f'<path d="M-150,-168 L-172,-98 L-150,-12" {D} stroke-width="28"/>'
    g += f'<path d="M26,-176 L14,-12" {D} stroke-width="28"/>'
    g += (f'<g transform="rotate({head*0.3:.2f} 56 -210) scale({br:.4f},{2-br:.4f})'
          f' translate(0,{(br-1)*200:.1f})">')
    # корпус: круп + бочка + грудь, всё плотное и низкое
    g += f'<ellipse cx="-125" cy="-174" rx="72" ry="64" fill="{K}"/>'
    g += f'<ellipse cx="-30" cy="-172" rx="110" ry="60" fill="{K}"/>'
    g += f'<ellipse cx="66" cy="-180" rx="74" ry="64" fill="{K}"/>'
    # шея — КОРОТКАЯ и толстая, иначе зверь превращается в коня
    g += f'<path d="M58,-206 L112,-286" {L} stroke-width="88"/>'
    # воротник: шея должна быть шире головы, иначе зверь похож на птицу
    g += f'<ellipse cx="74" cy="-230" rx="78" ry="52" fill="{K}" transform="rotate(-34 74 -230)"/>'
    # череп и морда
    g += f'<ellipse cx="146" cy="-316" rx="64" ry="52" fill="{K}" transform="rotate(-28 146 -316)"/>'
    g += f'<path d="M166,-332 L236,-376" {L} stroke-width="46"/>'
    g += f'<path d="M228,-370 L262,-388 L246,-352 Z" fill="{K}"/>'
    # уши прижаты назад
    g += f'<path d="M106,-348 L94,-412 L146,-366 Z" fill="{K}"/>'
    g += f'<path d="M140,-360 L170,-412 L184,-362 Z" fill="{K}"/>'
    g += f'<path d="M147,-367 L166,-400 L174,-368 Z" fill="{TERRA}" opacity=".45"/>'
    # пасть приоткрыта — воет
    g += f'<path d="M222,-356 C202,-342 188,-330 176,-316 L208,-328 Z" fill="#2b2420"/>'
    g += f'<circle cx="252" cy="-378" r="10" fill="#3a332e"/>'
    g += f'<circle cx="172" cy="-328" r="8.5" fill="{SVET}" opacity=".9"/>'
    g += (f'<path d="M-192,-158 C-204,-212 -162,-240 -100,-238 C-42,-236 8,-230 52,-222'
          f' C78,-216 98,-250 118,-282 C128,-298 140,-320 152,-342"'
          f' fill="none" stroke="#cfd8ea" stroke-width="7" stroke-linecap="round"'
          f' stroke-linejoin="round" opacity=".38"/>'
          f'<path d="M160,-352 L244,-400" fill="none" stroke="#cfd8ea"'
          f' stroke-width="6" stroke-linecap="round" opacity=".32"/>')
    if howl:
        for i in range(3):
            p = ((t * .62) + i * .33) % 1.0
            rr = 36 + p * 130
            g += (f'<path d="M{272+p*34:.0f},{-398-p*22:.0f} a{rr:.0f},{rr:.0f} 0 0 1'
                  f' {rr*.42:.0f},{rr*.86:.0f}" fill="none" stroke="{SER}" stroke-width="7"'
                  f' opacity="{max(0.0, .8-p):.2f}"/>')
    g += '</g>'
    g += f'<path d="M-118,-172 L-140,-96 L-116,-12" {L} stroke-width="36"/>'
    g += f'<path d="M72,-182 L76,-12" {L} stroke-width="34"/>'
    for x in (-116, 76):
        g += f'<ellipse cx="{x+4}" cy="-8" rx="23" ry="11" fill="{K}"/>'
    return g + '</g>'


# ─────────────────── СОЛНЦЕ · ЗЕМЛЯ · ЛУНА ───────────────────
def scheme(t):
    """Схема живая: лучи дышат, Земля крутится пятнами, Луна едет по орбите."""
    s = (f'<path d="M150,210 L760,210" stroke="{SVET}" stroke-width="5" opacity=".5"'
         f' stroke-dasharray="14 12" stroke-dashoffset="{-t*26:.0f}"/>')
    for i in range(16):
        a = i * math.pi / 8 + t * 0.12
        ln = 120 + 8 * A.w(t, 1.9, i * .11)
        s += (f'<path d="M{120+86*math.cos(a):.0f},{210+86*math.sin(a):.0f} '
              f'L{120+ln*math.cos(a):.0f},{210+ln*math.sin(a):.0f}" stroke="{ORA}"'
              f' stroke-width="9" stroke-linecap="round" opacity=".9"/>')
    s += f'<circle cx="120" cy="210" r="80" fill="{SVET}" {o(8)}/>'
    s += f'<circle cx="96" cy="186" r="22" fill="#fff3c9" opacity=".8"/>'
    s += f'<circle cx="520" cy="210" r="86" fill="#2f6fb5" {o(8)}/>'
    dx = 26 * A.w(t, 9.0)
    s += (f'<g transform="translate({dx:.1f},0)">'
          f'<path d="M462,172 q34,-20 64,2 q26,18 10,38 q-20,24 -54,10 q-30,-12 -20,-50 Z"'
          f' fill="{ZEL2}"/>'
          f'<path d="M520,258 q34,-14 58,6 q-18,26 -58,22 q-22,-12 0,-28 Z" fill="{ZEL}"/></g>')
    s += f'<path d="M448,232 q50,26 112,6" fill="none" stroke="#ffffff" stroke-width="7" opacity=".35"/>'
    s += (f'<ellipse cx="520" cy="210" rx="210" ry="86" fill="none" stroke="{SER}"'
          f' stroke-width="4" opacity=".4" stroke-dasharray="10 12"/>')
    a = -0.25 + t * 0.26
    mx, my = 520 + 210 * math.cos(a), 210 + 86 * math.sin(a)
    s += f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="40" fill="url(#mg)" {o(7)}/>'
    s += craters(mx, my, 40) + face(mx, my, 40, "smile", A.blink(t, 4.1, .6))
    for x, y, tt in ((120, 330, "СОЛНЦЕ"), (520, 330, "ЗЕМЛЯ")):
        s += (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{T.FAM[T.SERIF]}"'
              f' font-size="30" font-weight="bold" fill="#ffffff" letter-spacing="3">{tt}</text>')
    if math.cos(a) > 0.25:          # у Земли подпись налезала на «ЗЕМЛЯ»
        s += (f'<text x="{mx:.0f}" y="{my-54:.0f}" text-anchor="middle"'
              f' font-family="{T.FAM[T.SERIF]}" font-size="26" font-weight="bold"'
              f' fill="#ffffff" letter-spacing="2">ЛУНА</text>')
    return s


# ═══════════════════════════ СЦЕНЫ ═══════════════════════════
def hook(t):
    """Крючок. Луна выезжает и НАЛИВАЕТСЯ светом, титр наливается вместе с ней."""
    rise = A.ease(A.seg(t, 0.2, 3.4))
    my = 560 - 200 * rise
    halo = A.clamp((t - 0.6) / 3.0) * 1.25
    s = sky(W, H, t, True, 1)
    s += hills(W, H, .78)
    s += firs(W, H * .80, [120, 210, 300, 1660, 1770, 1860], 1.4)
    s += moon(1330, my, 230, t, "smile", halo)
    s += T.naliv(130, 700, "ПОЛНОЛУНИЕ", t, 2.6, 132, 1.6)
    p = A.out(A.seg(t, 3.5, 0.5))
    if p > 0:
        s += f'<rect x="134" y="736" width="{430*p:.0f}" height="9" rx="4" fill="{SVET}"/>'
    s += T.pechat(130, 804, "ночь, которая всем мешает спать", t, 4.0, 40, 21)
    return s


def bump(t):
    """Отбивка главы: волк воет, лента съезжается, титр в стыке."""
    s = sky(W, H, t, True, 2, cl=False)
    s += moon(1420, 330, 250, t, "oh", 1.0, ph=.3)
    s += hills(W, H, .70, "#0f1726", "#17213a")
    s += firs(W, H * .74, [90, 180, 1800, 1880], 1.6, "#0b1120")
    s += wolf(620, H * .74, t, 1.18)
    s += T.lenta(880, "ГЛАВА ПЕРВАЯ · ВОЛЧЬЯ ЛУНА", t, 0.25, W, 96, 0.7, 44)
    return s


def nelzya(t):
    """Блок «что нельзя»: кот на крыше, плашка-маска, падение слов, зачёркивание."""
    s = sky(W, H, t, False, 2)
    s += moon(1610, 212, 142, t, "wink", .9, ph=.15)
    s += houses(W, 700, t)
    s += roof(830, 600, H, 880, "#7e3c22")
    s += chimney(1150, 664, t, 74, 150)
    s += cat(790, 586, t, 1.9)
    s += T.plashka(120, 110, "ЧТО НЕЛЬЗЯ", "примета, в которую верили бабушки", t, 0.3, 0.9)
    words = ["НЕ", "СТРИГИСЬ"]
    wdt = T.padenie_width(words, 96, 2)
    pl = A.out(A.seg(t, 1.5, 0.45))
    if pl > 0:
        s += f'<rect x="118" y="272" width="{520*pl:.0f}" height="13" rx="7" fill="{KRAS}"/>'
    s += T.padenie(120, 380, words, t, 1.8, 96, 0.24, 0.5)
    s += T.zacherk(112, 352, wdt + 30, t, 4.4, 0.55)
    s += T.pechat(120, 470, "в полнолуние волосы растут иначе — так считали", t, 5.4, 34, 24)
    return s


def fact(t):
    """Блок «наука»: сова у схемы, росчерк под строкой, штамп ФАКТ."""
    s = sky(W, H, t, True, 1, cl=False)
    s += f'<rect y="{H*.86:.0f}" width="{W}" height="{H*.14:.0f}" fill="#141d33"/>'
    s += owl(420, 520, t, 1.5)
    s += f'<g transform="translate(900,330) scale(.95)">{scheme(t)}</g>'
    s += T.plashka(880, 120, "ПРИЛИВ И ОТЛИВ", "это её работа, а не магия", t, 0.2, 0.8)
    s += T.pechat(880, 300, "вода в океане идёт за Луной", t, 1.1, 38, 22)
    s += T.roscherk(880, 342, 520, t, 2.4, 0.8)
    s += T.shtamp(1200, 846, "ФАКТ", t, 3.6, 64)
    return s


SCENES = {"hook": hook, "bump": bump, "nelzya": nelzya, "fact": fact}


def svg(name, t, gt, z=1.0, cx=.5, cy=.5, out=(W, H)):
    """Кадр целиком. Зум — ОКНОМ ПРОСМОТРА, поэтому движение непрерывное."""
    vw, vh = W / z, H / z
    vx = min(max(0.0, cx * W - vw / 2), W - vw)
    vy = min(max(0.0, cy * H - vh / 2), H - vh)
    defs = (moon_defs("m") + moon_defs("ph") + sky_def(1) + sky_def(2)
            + f'<linearGradient id="plg" x1="0" y1="0" x2="1" y2="0">'
              f'<stop offset="0" stop-color="{ZOL}"/><stop offset="1" stop-color="{ORA}"/>'
              f'</linearGradient>')
    body = SCENES[name](t)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{out[0]}" height="{out[1]}"'
            f' viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}">'
            f'<defs>{defs}</defs><rect x="{vx:.0f}" y="{vy:.0f}" width="{vw:.0f}"'
            f' height="{vh:.0f}" fill="#101a33"/>{body}</svg>')
