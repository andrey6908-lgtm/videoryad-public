# -*- coding: utf-8 -*-
"""Второй ролик серии «Что нельзя готовить на Новый год козы»:
новые персонажи (коза, гости, ёлка, Дед Мороз, снеговик) и КАМЕРА.

Камера взята из лаборатории `camera-lab` и переложена на вектор: кадр
собирается из планов по глубине, каждый план получает свой масштаб
    s = F / (z - camz)
Одна эта формула даёт и параллакс (планы расходятся с разной скоростью),
и наезд (всё растёт, ближнее быстрее). Ни тряски, ни зум-аута — камера
идёт медленно и в одну сторону.
"""
import anim as A
import art

W, H = 960, 540
OUT = "#17130f"
RED, ORA, TER = "#d6202f", "#e07f23", "#a8512c"
PCH, CRM, GLD = "#efb07a", "#e4d4b6", "#c9922f"
GRN, HRB, NGT = "#6abf4b", "#4e7a35", "#22304a"
SNOW, WOOL = "#f2ead6", "#efe3c6"


def g(body, x=0, y=0, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})">{body}</g>'


def ST(w=8):
    return f' stroke="{OUT}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * u * (u * (u * 6 - 15) + 10)


# ============================= КАМЕРА =============================
BASE_Z = 2000.0          # глубина, на которой масштаб равен единице


def plane(body, z, camx=0.0, camz=0.0, camy=0.0, F=BASE_Z):
    """Один план по глубине. Чем он дальше, тем меньше его сдвиг и рост —
    параллакс и наезд выходят из одной формулы, писать их порознь не нужно."""
    s = F / max(60.0, z - camz)
    return (f'<g transform="translate({W/2:.2f},{H/2:.2f}) scale({s:.5f})'
            f' translate({-W/2 - camx:.2f},{-H/2 - camy:.2f})">{body}</g>')


def dolly(t, dur, z0=0.0, z1=260.0, x0=0.0, x1=0.0, y0=0.0, y1=0.0):
    """Ход камеры за сцену: медленно, в одну сторону, со смягчёнными концами."""
    u = ease(t / max(0.001, dur))
    return (x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, y0 + (y1 - y0) * u)


_VEIL = 0


def warm_light(cx, cy, r, op=.42, col="#ffcf7a"):
    """Тёплый свет лампы или свечей: пятно света поверх кадра."""
    global _VEIL
    _VEIL += 1
    i = f"wl{_VEIL}"
    return (f'<defs><radialGradient id="{i}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset=".55" stop-color="{col}" stop-opacity="{op*.4:.3f}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{i})"/>')


def side_dark(side="left", op=.5):
    """Тёмный бок кадра — глубина и объём, как вуаль по свету в лаборатории."""
    global _VEIL
    _VEIL += 1
    i = f"sd{_VEIL}"
    x1, x2 = ("0", "1") if side == "left" else ("1", "0")
    return (f'<defs><linearGradient id="{i}" x1="{x1}" y1="0" x2="{x2}" y2="0">'
            f'<stop offset="0" stop-color="#000000" stop-opacity="{op}"/>'
            f'<stop offset=".6" stop-color="#000000" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{i})"/>')


def ground_shadow(cx, cy, rx, ry=None, op=.5):
    """Пятно под фигурой: прижимает её к полу (блок 4 лаборатории)."""
    ry = ry if ry is not None else rx * .3
    s = ""
    for k, o in ((1.0, op * .35), (.76, op * .45), (.52, op * .55)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*k:.1f}" ry="{ry*k:.1f}" fill="#000000" opacity="{o:.2f}"/>'
    return s


def candles(items, t):
    """Свечи на столе: столбик, живое пламя, тёплый нимб."""
    s = ""
    for i, (x, y, h, sc) in enumerate(items):
        s += f'<rect x="{x-9*sc:.1f}" y="{y-h*sc:.1f}" width="{18*sc:.1f}" height="{h*sc:.1f}" rx="4" fill="{CRM}"{ST(6)}/>'
        s += f'<ellipse cx="{x}" cy="{y-h*sc:.1f}" rx="{9*sc:.1f}" ry="{3.4*sc:.1f}" fill="#d9c9a4"/>'
        s += A.flame(x, y - h * sc - 4 * sc, t, s=.9 * sc, glow=56 * sc, phase=i * .37)
    return s


# ============================ ПЕРСОНАЖИ ============================
def koza_head(t, cx=480, cy=292, s=.86):
    """Новая коза: добрая и ОГНЕННАЯ — вытянутая козья морда, большие
    круглые глаза, улыбка, румянец; грива живым пламенем, рога поверх неё."""
    blink = A.blink(t, 4.3, .2)
    look = 2.6 * A.w(t, 7.1, .3)
    b = f'<circle cx="0" cy="-6" r="214" fill="{ORA}" opacity=".16"/>'
    b += f'<circle cx="0" cy="-6" r="140" fill="{GLD}" opacity=".13"/>'
    for i, (ax, ay, sc, per, ph) in enumerate(((-168, -40, 1.0, 1.9, .0), (-128, -124, .86, 1.6, .3),
                                               (-44, -178, .95, 2.2, .6), (46, -182, .9, 1.7, .2),
                                               (132, -126, .88, 2.0, .5), (170, -36, 1.0, 1.8, .8),
                                               (-186, 48, .8, 2.3, .4), (188, 52, .8, 2.1, .1))):
        k = 1 + .09 * A.w(t, per, ph)
        q = 1 + .13 * A.w(t, per * 1.4, ph + .3)
        fill = "url(#fl1)" if i % 2 else "url(#fl2)"
        b += (f'<g transform="translate({ax},{ay}) scale({sc*k:.3f},{sc*q:.3f})">'
              f'<path d="M0 54 C-42 26 -46 -18 -22 -54 C-26 -24 -10 -16 -2 -30'
              f' C6 -46 2 -70 -12 -92 C34 -72 62 -30 56 6 C52 36 28 58 0 54 Z"'
              f' fill="{fill}"{ST(7)}/></g>')
    for i, (ex, ey, r, per) in enumerate(((-214, -96, 6, 3.1), (206, -104, 5, 2.6), (-96, -214, 4.4, 3.6),
                                          (104, -210, 5, 2.9), (232, 4, 4, 3.3), (-238, 10, 4.4, 2.7))):
        ph = (t / per + i * .27) % 1.0
        b += (f'<circle cx="{ex + 11*A.w(t, per*1.5, i*.3):.0f}" cy="{ey - 52*ph:.0f}" r="{r*(1-.4*ph):.1f}"'
              f' fill="#ffd36e" opacity="{.9*(1-ph):.2f}"/>')
    HORN, HORN2 = "#7a6246", "#4f3e2c"
    for sg in (-1, 1):
        b += (f'<path d="M{sg*58} -124 C{sg*84} -178 {sg*152} -224 {sg*230} -228'
              f' C{sg*264} -230 {sg*272} -202 {sg*246} -192 C{sg*188} -172 {sg*144} -146 {sg*112} -96 Z"'
              f' fill="{HORN}" stroke="{OUT}" stroke-width="9" stroke-linejoin="round"/>')
        b += (f'<path d="M{sg*78} -140 C{sg*116} -172 {sg*170} -200 {sg*236} -212"'
              f' stroke="{HORN2}" stroke-width="7" fill="none" opacity=".7"/>')
        for i in range(6):
            b += (f'<path d="M{sg*(80+i*28)} {-132-i*16} q{sg*13} {-15} {sg*27} {-17}"'
                  f' stroke="{HORN2}" stroke-width="6" fill="none" opacity=".85"/>')
    for sg in (-1, 1):
        rot = A.sway(t, 6.1, .2 + .3 * (sg > 0), 2.4)
        b += (f'<g transform="rotate({rot*sg:.2f} {sg*92} 10)">'
              f'<path d="M{sg*78} -14 C{sg*134} -22 {sg*192} 10 {sg*194} 52'
              f' C{sg*156} 70 {sg*100} 44 {sg*74} 14 Z" fill="{WOOL}"{ST(8)}/>'
              f'<path d="M{sg*100} 2 C{sg*140} 0 {sg*172} 20 {sg*178} 40'
              f' C{sg*150} 46 {sg*116} 30 {sg*98} 14 Z" fill="{PCH}" opacity=".7"/></g>')
    b += (f'<path d="M0 -140 C84 -140 140 -84 140 -16 C140 36 124 74 100 108'
          f' C80 136 50 176 0 196 C-50 176 -80 136 -100 108 C-124 74 -140 36 -140 -16'
          f' C-140 -84 -84 -140 0 -140 Z" fill="{SNOW}"{ST(9)}/>')
    b += (f'<path d="M50 -130 C106 -106 140 -64 140 -16 C140 36 124 74 100 108 C80 136 50 176 0 196'
          f' C44 158 74 110 86 58 C98 0 86 -90 50 -130 Z" fill="{PCH}" opacity=".4"/>')
    fk = 1 + .12 * A.w(t, 1.6, .2)
    b += (f'<g transform="translate(0,-116) scale({fk:.3f})">'
          f'<path d="M0 26 C-30 10 -34 -18 -16 -44 C-18 -22 -6 -16 0 -28'
          f' C8 -44 4 -62 -6 -78 C28 -62 48 -28 42 2 C38 22 20 34 0 26 Z" fill="url(#fl1)"{ST(6)}/></g>')
    for sg in (-1, 1):
        ex = sg * 56
        if blink:
            b += (f'<path d="M{ex-30} 6 C{ex-12} -14 {ex+12} -14 {ex+30} 6"'
                  f' stroke="{OUT}" stroke-width="11" fill="none" stroke-linecap="round"/>')
        else:
            b += f'<circle cx="{ex}" cy="2" r="35" fill="#fff8e6"{ST(8)}/>'
            b += f'<circle cx="{ex+look:.1f}" cy="6" r="24" fill="#f7cb53"/>'
            b += f'<circle cx="{ex+look:.1f}" cy="6" r="15" fill="#2a1105"/>'
            b += f'<circle cx="{ex-8+look:.1f}" cy="-4" r="7.5" fill="#fff" opacity=".95"/>'
            b += f'<circle cx="{ex+10+look:.1f}" cy="14" r="4" fill="#fff" opacity=".7"/>'
        b += (f'<path d="M{ex-30} -52 C{ex-12} -66 {ex+12} -66 {ex+30} -52"'
              f' stroke="{GLD}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/>')
    b += f'<ellipse cx="-100" cy="48" rx="25" ry="16" fill="{RED}" opacity=".26"/>'
    b += f'<ellipse cx="100" cy="48" rx="25" ry="16" fill="{RED}" opacity=".26"/>'
    b += (f'<path d="M-44 76 C-24 66 24 66 44 76 C42 106 24 136 0 146 C-24 136 -42 106 -44 76 Z"'
          f' fill="{WOOL}" opacity=".55" stroke="{PCH}" stroke-width="4"/>')
    b += (f'<path d="M-26 90 C-22 82 -13 82 -10 92" stroke="{OUT}" stroke-width="6" fill="none" stroke-linecap="round"/>'
          f'<path d="M26 90 C22 82 13 82 10 92" stroke="{OUT}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    b += (f'<path d="M0 104 L0 120 M-26 124 C-15 140 -5 142 0 132 C5 142 15 140 26 124"'
          f' stroke="{OUT}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    sw_b = A.sway(t, 5.2, .4, 1.6)
    b += (f'<g transform="rotate({sw_b:.2f} 0 186)">'
          f'<path d="M-36 176 C-48 216 -30 254 0 272 C32 248 52 206 36 176 C20 196 -20 196 -36 176 Z"'
          f' fill="{WOOL}"{ST(8)}/>'
          f'<g stroke="{PCH}" stroke-width="4.5" fill="none" opacity=".75">'
          f'<path d="M-11 202 q-6 30 4 50 M11 202 q6 30 -4 50"/></g></g>')
    b += (f'<path d="M-128 222 C-62 256 62 256 128 222 C136 250 130 272 116 284'
          f' C46 318 -46 318 -116 284 C-132 272 -136 250 -128 222 Z" fill="{RED}"{ST(9)}/>')
    b += f'<g stroke="#8d1420" stroke-width="5" fill="none" opacity=".8">'
    for i in range(7):
        b += f'<path d="M{-106+i*35} 236 q4 30 -2 48"/>'
    b += '</g>'
    b += f'<path d="M98 266 C130 288 144 332 136 372 C114 368 88 342 80 304 Z" fill="{RED}"{ST(8)}/>'
    return g(b, cx, cy, s)


def guest(t, x, y, s, skin, hair, cloth, kind="hat", ph=0.0, glass=True):
    b = ""
    sw = A.sway(t, 5.4, ph, 1.4)
    b += f'<g transform="rotate({sw:.2f} 0 120)">'
    b += f'<path d="M-78 118 C-62 72 -28 52 0 52 C28 52 62 72 78 118 L78 160 L-78 160 Z" fill="{cloth}"{ST(8)}/>'
    b += f'<ellipse cx="0" cy="0" rx="54" ry="60" fill="{skin}"{ST(8)}/>'
    if kind == "hat":
        b += f'<path d="M-58 -16 C-54 -74 -20 -96 0 -96 C20 -96 54 -74 58 -16 Z" fill="{RED}"{ST(8)}/>'
        b += f'<path d="M-62 -18 C-20 -34 20 -34 62 -18 C62 -2 -62 -2 -62 -18 Z" fill="{WOOL}"{ST(7)}/>'
    elif kind == "bun":
        b += f'<path d="M-56 -10 C-52 -70 -18 -92 0 -92 C20 -92 54 -70 56 -10 C30 -36 -28 -36 -56 -10 Z" fill="{hair}"{ST(8)}/>'
        b += f'<circle cx="0" cy="-94" r="22" fill="{hair}"{ST(7)}/>'
        b += f'<circle cx="-52" cy="18" r="6" fill="{GLD}"/><circle cx="52" cy="18" r="6" fill="{GLD}"/>'
    elif kind == "bald":
        b += f'<path d="M-56 -12 C-48 -46 -24 -60 0 -60 C24 -60 48 -46 56 -12 C40 -30 -40 -30 -56 -12 Z" fill="{hair}" opacity=".9"{ST(6)}/>'
        b += f'<path d="M-26 28 q26 12 52 0" stroke="{hair}" stroke-width="9" fill="none"/>'
    else:
        b += f'<path d="M-58 -14 C-46 -86 12 -112 46 -92 L58 -16 Z" fill="{GRN}"{ST(8)}/>'
        b += f'<circle cx="52" cy="-96" r="14" fill="{WOOL}"{ST(7)}/>'
        b += f'<path d="M-60 -16 C-20 -32 20 -32 60 -16 C60 -2 -60 -2 -60 -16 Z" fill="{WOOL}"{ST(7)}/>'
    if A.blink(t, 4.6, ph):
        b += f'<path d="M-32 2 q10 -10 20 0 M12 2 q10 -10 20 0" stroke="{OUT}" stroke-width="6" fill="none"/>'
    else:
        b += f'<circle cx="-22" cy="2" r="7" fill="{OUT}"/><circle cx="22" cy="2" r="7" fill="{OUT}"/>'
    b += f'<path d="M-4 10 q-8 14 4 18" stroke="{OUT}" stroke-width="5" fill="none"/>'
    b += f'<path d="M-20 38 q20 16 40 -2" stroke="{OUT}" stroke-width="6" fill="none"/>'
    b += f'<circle cx="-40" cy="24" r="10" fill="{RED}" opacity=".25"/><circle cx="40" cy="24" r="10" fill="{RED}" opacity=".25"/>'
    if glass:
        lift = -8 * A.w(t, 4.2, ph)
        b += (f'<path d="M52 108 C72 96 86 80 90 {64+lift:.0f}" stroke="{cloth}" stroke-width="20"'
              f' fill="none" stroke-linecap="round"/>'
              f'<circle cx="90" cy="{62+lift:.0f}" r="13" fill="{skin}"{ST(6)}/>')
        b += g(f'<path d="M-20 0 L20 0 L12 44 L-12 44 Z" fill="#cfe6f2" opacity=".8"{ST(6)}/>'
               f'<path d="M-20 0 L20 0 L16 14 L-16 14 Z" fill="{GLD}" opacity=".85"/>'
               f'<path d="M0 44 L0 64 M-14 66 L14 66" stroke="{OUT}" stroke-width="6" fill="none"/>',
               62, 60 + lift, .9)
    b += '</g>'
    return g(b, x, y, s)


def tree_new(t, cx=480, base=470, s=1.0):
    b = f'<rect x="-22" y="-10" width="44" height="52" fill="#6b3f1c"{ST(7)}/>'
    tiers = ((-320, 64), (-248, 104), (-168, 148), (-74, 196))
    for i, (ty, hw) in enumerate(tiers):
        bot = tiers[i + 1][0] + 26 if i + 1 < len(tiers) else 6
        b += f'<path d="M0 {ty} L{hw} {bot} L{-hw} {bot} Z" fill="{HRB if i%2 else "#2f5c2a"}"{ST(8)}/>'
    for i, (ty, hw) in enumerate(tiers):
        bot = tiers[i + 1][0] + 26 if i + 1 < len(tiers) else 6
        b += (f'<path d="M{-hw+6} {bot} C{-hw*0.55} {bot-18} {-hw*0.26} {bot+4} 0 {bot-12}'
              f' C{hw*0.3} {bot+4} {hw*0.58} {bot-18} {hw-6} {bot}'
              f' C{hw*0.55} {bot+13} {-hw*0.55} {bot+13} {-hw+6} {bot} Z" fill="{SNOW}"{ST(5)}/>')
    b += (f'<path d="M-96 -228 C-30 -202 40 -236 104 -206 M-126 -150 C-44 -118 44 -156 128 -124'
          f' M-160 -58 C-56 -22 58 -62 166 -24" stroke="{GLD}" stroke-width="11" fill="none" opacity=".95"/>')
    for tx, ty, r, c in ((-44, -238, 17, RED), (46, -196, 15, GLD), (-78, -142, 18, ORA),
                         (84, -110, 16, RED), (-6, -88, 15, PCH), (-116, -40, 17, GLD), (120, -30, 16, RED)):
        b += f'<circle cx="{tx}" cy="{ty}" r="{r}" fill="{c}"{ST(5)}/>'
        b += f'<circle cx="{tx-r*.35:.0f}" cy="{ty-r*.4:.0f}" r="{r*.28:.1f}" fill="#fff" opacity=".6"/>'
    b += A.lights([(-62, -214, "#ffd45e"), (18, -256, "#7fd0ff"), (72, -164, "#ff8c6b"),
                   (-104, -104, "#9ae06a"), (10, -60, "#ffd45e"), (136, -62, "#7fd0ff"),
                   (-150, -22, "#ff8c6b"), (62, -14, "#9ae06a")], t)
    pl = 1 + .06 * A.w(t, 2.2)
    b += (f'<g transform="translate(0,-348) scale({pl:.3f})"><circle r="34" fill="{GLD}" opacity=".3"/>'
          f'<path d="M0 -40 L11 -12 L41 -12 L17 7 L26 37 L0 19 L-26 37 L-17 7 L-41 -12 L-11 -12 Z"'
          f' fill="{GLD}"{ST(7)}/></g>')
    b += g(f'<rect x="-44" y="-48" width="88" height="48" rx="5" fill="{RED}"{ST(7)}/>'
           f'<path d="M0 -48 L0 0 M-44 -26 L44 -26" stroke="{GLD}" stroke-width="9"/>', -142, 40, 1)
    b += g(f'<rect x="-34" y="-62" width="68" height="62" rx="5" fill="{NGT}"{ST(7)}/>'
           f'<path d="M0 -62 L0 0 M-34 -32 L34 -32" stroke="{SNOW}" stroke-width="8"/>', 150, 40, .9)
    return g(b, cx, base, s)


def ded_new(t, x=300, y=300, s=1.0):
    b = ""
    sw = A.sway(t, 6.6, .1, 1.1)
    b += f'<g transform="rotate({sw:.2f} 0 160)">'
    b += f'<path d="M-96 170 C-96 60 -52 10 0 10 C52 10 96 60 96 170 Z" fill="{NGT}"{ST(9)}/>'
    b += f'<path d="M-96 170 C-70 150 70 150 96 170 C96 196 -96 196 -96 170 Z" fill="{SNOW}"{ST(7)}/>'
    b += f'<path d="M-14 16 C-6 70 -6 120 -14 168 L22 168 C14 120 14 70 22 16 Z" fill="{SNOW}" opacity=".9"{ST(6)}/>'
    b += f'<path d="M-82 110 C-40 122 40 122 82 110 L82 136 C40 148 -40 148 -82 136 Z" fill="{GLD}"{ST(7)}/>'
    b += f'<path d="M80 50 C118 70 134 108 128 142 L96 136 C98 106 90 78 66 64 Z" fill="{NGT}"{ST(8)}/>'
    b += f'<circle cx="126" cy="150" r="22" fill="{SNOW}"{ST(7)}/>'
    b += f'<path d="M126 -160 L126 152" stroke="#8a5a2c" stroke-width="13" stroke-linecap="round"/>'
    gl = 1 + .09 * A.w(t, 2.6)
    b += (f'<g transform="translate(126,-176) scale({gl:.3f})"><circle r="26" fill="#7fd0ff" opacity=".28"/>'
          f'<path d="M0 -26 L14 0 L0 26 L-14 0 Z" fill="#bfe6ff"{ST(6)}/></g>')
    b += f'<ellipse cx="0" cy="-44" rx="50" ry="54" fill="#f2d2ae"{ST(8)}/>'
    b += f'<path d="M-44 -40 C-52 14 -24 52 0 52 C24 52 52 14 44 -40 C28 -18 -28 -18 -44 -40 Z" fill="{SNOW}"{ST(8)}/>'
    b += (f'<path d="M-40 -28 C-26 -16 -8 -14 0 -20 C8 -14 26 -16 40 -28"'
          f' stroke="{SNOW}" stroke-width="15" fill="none" stroke-linecap="round"/>')
    if A.blink(t, 5.1, .3):
        b += f'<path d="M-30 -56 q10 -8 18 0 M12 -56 q10 -8 18 0" stroke="{OUT}" stroke-width="6" fill="none"/>'
    else:
        b += f'<circle cx="-21" cy="-56" r="7" fill="{OUT}"/><circle cx="21" cy="-56" r="7" fill="{OUT}"/>'
    b += f'<path d="M-44 -72 q22 -12 30 -2 M14 -74 q18 -8 30 4" stroke="{SNOW}" stroke-width="8" fill="none"/>'
    b += f'<circle cx="0" cy="-36" r="11" fill="{RED}" opacity=".5"/>'
    b += f'<path d="M-56 -84 C-50 -150 -16 -176 6 -176 C34 -176 62 -148 58 -84 Z" fill="{NGT}"{ST(8)}/>'
    b += f'<path d="M-60 -86 C-20 -102 20 -102 62 -86 C62 -66 -60 -66 -60 -86 Z" fill="{SNOW}"{ST(7)}/>'
    b += f'<circle cx="30" cy="-176" r="15" fill="{SNOW}"{ST(6)}/>'
    b += '</g>'
    return g(b, x, y, s)


def snowman_new(t, x=680, y=330, s=1.0):
    b = ""
    sq = 1 + .02 * A.w(t, 3.4)
    b += f'<g transform="scale(1,{sq:.3f})">'
    b += f'<ellipse cx="0" cy="118" rx="98" ry="86" fill="{SNOW}"{ST(9)}/>'
    b += f'<ellipse cx="0" cy="6" rx="72" ry="66" fill="{SNOW}"{ST(9)}/>'
    b += f'<ellipse cx="22" cy="118" rx="60" ry="64" fill="#dcd2bb" opacity=".45"/>'
    b += f'<ellipse cx="18" cy="8" rx="44" ry="48" fill="#dcd2bb" opacity=".4"/>'
    b += f'<path d="M-50 -46 L50 -46 L38 -102 L-38 -102 Z" fill="{TER}"{ST(8)}/>'
    b += f'<path d="M-56 -46 L56 -46 L56 -30 L-56 -30 Z" fill="{ORA}"{ST(7)}/>'
    b += f'<path d="M-44 -96 C-10 -118 10 -118 44 -96" stroke="{OUT}" stroke-width="6" fill="none"/>'
    if A.blink(t, 5.4, .6):
        b += f'<path d="M-32 -12 q10 -8 18 0 M14 -12 q10 -8 18 0" stroke="{OUT}" stroke-width="6" fill="none"/>'
    else:
        b += f'<circle cx="-23" cy="-12" r="9" fill="#241a12"/><circle cx="23" cy="-12" r="9" fill="#241a12"/>'
    b += f'<path d="M-6 6 L58 22 L-6 30 Z" fill="{ORA}"{ST(6)}/>'
    b += "".join(f'<circle cx="{-30+i*15}" cy="{44 - abs(2-i)*5}" r="5" fill="#241a12"/>' for i in range(5))
    b += f'<path d="M-66 54 C-20 76 20 76 66 54 C68 76 62 90 52 96 C14 112 -14 112 -52 96 C-62 90 -68 76 -66 54 Z" fill="{RED}"{ST(8)}/>'
    b += f'<path d="M50 90 C74 108 82 140 76 166 C58 160 42 136 38 112 Z" fill="{RED}"{ST(7)}/>'
    b += f'<path d="M-96 96 L-168 56 M-150 60 L-164 36 M-152 68 L-178 66" stroke="#6b4a2c" stroke-width="8" fill="none"/>'
    b += f'<path d="M96 104 L168 72" stroke="#6b4a2c" stroke-width="8" fill="none"/>'
    b += '</g>'
    return g(b, x, y, s)


def no_sign(x, y, r=118, w=22):
    return (f'<g><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{RED}" stroke-width="{w}" opacity=".92"/>'
            f'<path d="M{x-r*.68:.0f} {y+r*.68:.0f} L{x+r*.68:.0f} {y-r*.68:.0f}" stroke="{RED}"'
            f' stroke-width="{w}" stroke-linecap="round" opacity=".92"/></g>')


def salad_bowl(t, x=480, y=320, s=1.0):
    b = f'<path d="M-150 -26 C-150 56 -110 98 0 98 C110 98 150 56 150 -26 Z" fill="#cfe6f2" opacity=".35"{ST(8)}/>'
    for c, yy in (("#8e2b4a", -16), ("#efe7d2", -40), ("#d98b2a", -60), ("#f2d85a", -78)):
        b += (f'<path d="M-142 {yy} C-100 {yy+22} 100 {yy+22} 142 {yy} L142 {yy+24}'
              f' C100 {yy+44} -100 {yy+44} -142 {yy+24} Z" fill="{c}"{ST(5)}/>')
    b += (f'<path d="M-146 -78 C-120 -120 -60 -136 0 -136 C60 -136 120 -120 146 -78'
          f' C100 -56 -100 -56 -146 -78 Z" fill="{SNOW}"{ST(8)}/>')
    b += f'<path d="M-158 -24 C-178 24 -168 70 -150 92" stroke="{OUT}" stroke-width="8" fill="none"/>'
    return g(b, x, y, s)


def video_window(x, y, w, h, kind, label=""):
    """Окно живой вставки: скруглённый кадр с тем же толстым контуром.
    В пробнике внутри рисунок-заглушка — в ролике сюда ляжет настоящее видео."""
    i = f"cpw{kind}"
    b = f'<defs><clipPath id="{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/></clipPath></defs>'
    b += f'<g clip-path="url(#{i})">'
    if kind == 1:
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#6b4a2c"/>'
        b += f'<ellipse cx="{x+w*.5}" cy="{y+h*.72}" rx="{w*.42}" ry="{h*.3}" fill="{CRM}"/>'
        b += f'<ellipse cx="{x+w*.5}" cy="{y+h*.66}" rx="{w*.34}" ry="{h*.2}" fill="{SNOW}"/>'
        b += f'<ellipse cx="{x+w*.36}" cy="{y+h*.58}" rx="{w*.08}" ry="{h*.07}" fill="#e2b23c"/>'
        b += f'<ellipse cx="{x+w*.58}" cy="{y+h*.6}" rx="{w*.07}" ry="{h*.06}" fill="#8e2b4a"/>'
    else:
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#7d5a33"/>'
        for i2 in range(5):
            b += (f'<ellipse cx="{x+w*(.2+i2*.15)}" cy="{y+h*(.6+.04*(i2%2))}" rx="{w*.08}" ry="{h*.1}"'
                  f' fill="{"#b8463f" if i2%2 else "#d98b6a"}" stroke="#5d2016" stroke-width="4"/>')
        b += f'<rect x="{x}" y="{y+h*.78}" width="{w}" height="{h*.22}" fill="#6b4a2c"/>'
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h*.3}" fill="#fff" opacity=".06"/></g>'
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="none"{ST(9)}/>'
    return b


# ============================== СЦЕНЫ ==============================
# Планы по глубине: стена 2600 (почти стоит), ёлка 2200, герой 2000 (масштаб 1),
# стол 1800, передний план 1500 (уходит из кадра быстрее всех).
Z_WALL, Z_TREE, Z_HERO, Z_TABLE, Z_NEAR = 2600, 2200, 2000, 1800, 1500


def air(op=.07):
    """Тёплый воздух комнаты: чуть поднимает полутона, чтобы кадр не чернел."""
    return f'<rect width="{W}" height="{H}" fill="#ffcf7a" opacity="{op}"/>'


def cam_room(t, dur=10.0):
    """Общий план: камера едет ВПЕРЁД и чуть вправо. Дальняя стена почти
    стоит, стол и свечи наезжают — это и есть параллакс."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=170, x0=-34, x1=26)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += plane(art.window(60, 96, 250, 180, t) + art.window(650, 96, 250, 180, t) + art.tinsel(40),
               Z_WALL, cx, cz)
    s += plane(tree_new(t, 800, 452, .84), Z_TREE, cx, cz)
    s += plane(guest(t, 258, 288, .80, "#f0c9a4", "#5a3a22", TER, "hat", .0)
               + guest(t, 428, 280, .84, "#e8bd94", "#3b2416", HRB, "bun", .35)
               + guest(t, 598, 288, .82, "#f2d2ae", "#6b4a2c", NGT, "bald", .7), Z_HERO, cx, cz)
    s += plane(art.table(408) + candles([(190, 408, 56, 1.0), (742, 408, 50, .9)], t), Z_TABLE, cx, cz)
    s += plane(candles([(140, 438, 74, 1.1)], t), Z_NEAR, cx, cz)
    s += warm_light(200, 360, 330, .34) + warm_light(740, 366, 280, .3) + air()
    s += side_dark("left", .26) + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".7"/>'
    return s


def cam_koza(t, dur=10.0):
    """Коза крупно: медленный наезд, пламя гривы живёт, свет свечей слева."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=150, x0=16, x1=-12)
    s = f'<rect width="{W}" height="{H}" fill="url(#room)"/>'
    s += plane(art.window(44, 70, 220, 164, t) + art.tinsel(34), Z_WALL, cx, cz)
    s += plane(tree_new(t, 840, 470, .46), Z_TREE, cx, cz)
    s += plane(koza_head(t, 468, 258, .80), Z_HERO, cx, cz)
    s += plane(candles([(150, 430, 78, 1.05), (820, 436, 68, .95)], t), Z_NEAR, cx, cz)
    s += warm_light(170, 350, 300, .4) + warm_light(820, 370, 230, .26) + air(.08)
    s += side_dark("right", .24) + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".65"/>'
    return s


def cam_tree(t, dur=10.0):
    """Проезд мимо ёлки: передний план уезжает быстро, стена почти стоит."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=110, x0=-96, x1=96)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    s += plane(art.window(80, 86, 230, 170, t) + art.window(650, 86, 230, 170, t), Z_WALL, cx, cz)
    s += plane(art.tinsel(38), Z_WALL - 200, cx, cz)
    s += plane(tree_new(t, 480, 452, .92), Z_TREE, cx, cz)
    s += plane(art.table(452) + candles([(206, 452, 60, 1.0), (714, 452, 52, .9)], t), Z_TABLE, cx, cz)
    s += plane(candles([(96, 440, 86, 1.15)], t), Z_NEAR, cx, cz)
    s += warm_light(480, 300, 380, .3) + air() + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".7"/>'
    return s


def cam_ded(t, dur=10.0):
    """Дед Мороз и снеговик: камера наезжает, тени прижимают их к полу."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=150, x0=-44, x1=44)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    s += plane(art.window(372, 70, 216, 162, t) + art.tinsel(34), Z_WALL, cx, cz)
    s += plane(ground_shadow(276, 452, 124, 26, .5) + ded_new(t, 276, 272, .88)
               + ground_shadow(664, 452, 130, 28, .48) + snowman_new(t, 664, 270, .82), Z_HERO, cx, cz)
    s += plane(f'<path d="M0 466 C240 444 720 444 960 466 L960 540 L0 540 Z" fill="{SNOW}" opacity=".9"{ST(7)}/>'
               + candles([(130, 470, 66, 1.0), (826, 470, 58, .95)], t), Z_TABLE, cx, cz)
    s += warm_light(170, 400, 290, .3) + warm_light(810, 400, 260, .3) + air()
    s += side_dark("left", .22) + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".65"/>'
    return s


def cam_zapret(t, dur=10.0):
    """Запрет: наезд на салат под майонезом, знак выходит вперёд."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=150, x0=8, x1=-8)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomr)"/>'
    s += plane(art.tinsel(34) + art.window(666, 80, 210, 158, t), Z_WALL, cx, cz)
    s += plane(art.table(370, "#b8463f"), Z_TABLE, cx, cz)
    s += plane(ground_shadow(430, 396, 150, 26, .42) + salad_bowl(t, 430, 300, .92), Z_HERO, cx, cz)
    s += plane(no_sign(430, 286, 148, 26), Z_HERO - 120, cx, cz)
    s += plane(candles([(812, 430, 78, 1.05)], t), Z_NEAR, cx, cz)
    s += warm_light(800, 380, 260, .32) + air() + side_dark("left", .22)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".65"/>'
    return s


def cam_okna(t, dur=10.0):
    """Два окна живого видео внутри рисунка: камера чуть ведёт вбок,
    сами окна держатся неподвижно — вставка не должна плыть."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=90, x0=-20, x1=20)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += plane(art.tinsel(30), Z_WALL, cx, cz)
    s += plane(art.table(404, "#b8463f") + candles([(150, 404, 58, 1.0), (812, 404, 52, .9)], t), Z_TABLE, cx, cz)
    s += plane(guest(t, 480, 336, .72, "#f0c9a4", "#5a3a22", NGT, "cap", .2)
               + guest(t, 272, 348, .62, "#e8bd94", "#3b2416", HRB, "bun", .5), Z_HERO, cx, cz)
    s += video_window(75, 52, 350, 197, 1) + video_window(535, 52, 350, 197, 2)
    s += warm_light(150, 370, 270, .3) + air() + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".6"/>'
    return s


SCENES = {
    "cam_room": cam_room,
    "cam_koza": cam_koza,
    "cam_tree": cam_tree,
    "cam_ded": cam_ded,
    "cam_zapret": cam_zapret,
    "cam_okna": cam_okna,
}
NO_GLARE = set()
