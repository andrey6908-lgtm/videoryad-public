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
    s += lens_flare([scr(190, 408, Z_TABLE, cx, cz)[:2] + (.5, 17 * scr(190, 408, Z_TABLE, cx, cz)[2]),
                     scr(742, 408, Z_TABLE, cx, cz)[:2] + (.42, 15 * scr(742, 408, Z_TABLE, cx, cz)[2])])
    return s


def cam_koza(t, dur=10.0):
    """Коза крупно: медленный наезд, пламя гривы живёт, свет свечей слева."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=150, x0=16, x1=-12)
    s = f'<rect width="{W}" height="{H}" fill="url(#room)"/>'
    s += plane(art.window(44, 70, 220, 164, t) + art.tinsel(34), Z_WALL, cx, cz)
    s += plane(tree_new(t, 840, 470, .46), Z_TREE, cx, cz)
    s += plane(koza_head(t, 468, 282, .60), Z_HERO, cx, cz)
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
    s += lens_flare([scr(206, 452, Z_TABLE, cx, cz)[:2] + (.5, 17 * scr(206, 452, Z_TABLE, cx, cz)[2]),
                     scr(96, 440, Z_NEAR, cx, cz)[:2] + (.6, 19 * scr(96, 440, Z_NEAR, cx, cz)[2])])
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
    s += lens_flare([scr(130, 470, Z_TABLE, cx, cz)[:2] + (.5, 17 * scr(130, 470, Z_TABLE, cx, cz)[2]),
                     scr(826, 470, Z_TABLE, cx, cz)[:2] + (.45, 16 * scr(826, 470, Z_TABLE, cx, cz)[2])])
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


# ---------------------- предметы стола (кирпичики) ----------------------
def dish_greens(x, y, s=1.0):
    b = f'<ellipse cx="0" cy="0" rx="118" ry="34" fill="{CRM}"{ST(7)}/>'
    b += f'<path d="M-88 -8 C-54 -68 54 -68 88 -8 C54 14 -54 14 -88 -8 Z" fill="{HRB}"{ST(7)}/>'
    b += "".join(f'<path d="M{-64+i*26} -14 q10 -32 22 -42" stroke="{GRN}" stroke-width="7" fill="none"/>' for i in range(6))
    return g(b, x, y, s)


def dish_bird(x, y, s=1.0):
    b = f'<ellipse cx="0" cy="0" rx="128" ry="36" fill="{CRM}"{ST(7)}/>'
    b += (f'<path d="M-92 -12 C-80 -74 -24 -104 12 -98 C62 -90 96 -56 96 -12 C56 12 -52 12 -92 -12 Z"'
          f' fill="url(#duck)"{ST(8)}/>')
    b += f'<path d="M-52 -58 C-30 -74 10 -76 34 -62" stroke="#5d2f0d" stroke-width="5" fill="none" opacity=".8"/>'
    for i, cx2 in enumerate((-66, -22, 28, 70)):
        b += f'<circle cx="{cx2}" cy="{-4 - (i%2)*10}" r="17" fill="{ORA}"{ST(5)}/>'
    return g(b, x, y, s)


def dish_cheese(x, y, s=1.0):
    b = f'<path d="M-104 0 L104 0 L92 26 L-92 26 Z" fill="#8a5a2c"{ST(7)}/>'
    b += f'<path d="M-84 -2 L-18 -2 L-28 -46 L-74 -46 Z" fill="#f2d85a"{ST(6)}/>'
    b += f'<circle cx="-56" cy="-26" r="7" fill="#d9bd3c"/><circle cx="-36" cy="-14" r="5" fill="#d9bd3c"/>'
    b += f'<path d="M-6 -2 L52 -2 L44 -40 L4 -40 Z" fill="{SNOW}"{ST(6)}/>'
    b += f'<path d="M58 -2 L100 -2 L96 -30 L62 -30 Z" fill="{PCH}"{ST(6)}/>'
    b += "".join(f'<circle cx="{-70+i*34}" cy="8" r="7" fill="{TER}"{ST(4)}/>' for i in range(6))
    return g(b, x, y, s)


def dish_fruit(x, y, s=1.0):
    b = f'<path d="M-96 -10 C-96 44 -60 72 0 72 C60 72 96 44 96 -10 Z" fill="#9a6a34"{ST(8)}/>'
    for i, (fx, fy, r, c) in enumerate(((-54, -22, 26, "#d8622a"), (-6, -34, 28, "#e2b23c"),
                                        (46, -20, 25, "#d8622a"), (18, 2, 24, "#b8463f"),
                                        (-32, 6, 23, "#e2b23c"))):
        b += f'<circle cx="{fx}" cy="{fy}" r="{r}" fill="{c}"{ST(6)}/>'
        b += f'<circle cx="{fx-r*.3:.0f}" cy="{fy-r*.35:.0f}" r="{r*.22:.1f}" fill="#fff" opacity=".45"/>'
    return g(b, x, y, s)


def jug_mors(x, y, s=1.0):
    b = (f'<path d="M-44 -70 L44 -70 L52 46 C52 66 -52 66 -52 46 Z" fill="#b8463f" opacity=".92"{ST(8)}/>')
    b += f'<path d="M44 -52 C86 -44 88 6 48 18" stroke="{OUT}" stroke-width="9" fill="none"/>'
    b += f'<path d="M-40 -34 L40 -34" stroke="{SNOW}" stroke-width="6" opacity=".5"/>'
    b += f'<path d="M-18 -92 C-10 -112 10 -112 18 -92" stroke="{HRB}" stroke-width="7" fill="none"/>'
    return g(b, x, y, s)


def sausage_plate(x, y, s=1.0):
    """Нарезка веером: ломтики ложатся по дуге, а не кучей в центре."""
    b = f'<ellipse cx="0" cy="0" rx="176" ry="50" fill="{CRM}"{ST(8)}/>'
    b += f'<ellipse cx="0" cy="-6" rx="152" ry="40" fill="#efe7d2"/>'
    for i in range(9):
        a = -64 + i * 16
        b += (f'<g transform="rotate({a} 0 46)"><ellipse cx="0" cy="-54" rx="50" ry="21"'
              f' fill="{"#b8463f" if i%2 else "#d98b6a"}"{ST(6)}/>'
              + "".join(f'<circle cx="{-28+j*14}" cy="{-58+(j%2)*9}" r="4.2" fill="{CRM}" opacity=".85"/>'
                        for j in range(5))
              + '</g>')
    return g(b, x, y, s)


# ---------------------- новые камерные сцены ----------------------
def _wall(t, pairs, tins=34):
    return "".join(art.window(x, y, w, h, t) for x, y, w, h in pairs) + art.tinsel(tins)


def cam_room2(t, dur=10.0):
    """Комната с другого угла: ёлка слева, гости справа, камера ведёт влево."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=150, x0=40, x1=-34)
    s = f'<rect width="{W}" height="{H}" fill="url(#room)"/>'
    s += plane(_wall(t, [(560, 92, 240, 176)]), Z_WALL, cx, cz)
    s += plane(tree_new(t, 190, 460, .8), Z_TREE, cx, cz)
    s += plane(guest(t, 560, 288, .84, "#eec49c", "#4a2c18", RED, "cap", .15)
               + guest(t, 740, 296, .80, "#f0c9a4", "#5a3a22", HRB, "bun", .55), Z_HERO, cx, cz)
    s += plane(art.table(412) + dish_greens(300, 402, .62) + dish_cheese(640, 400, .6)
               + candles([(470, 412, 54, 1.0)], t), Z_TABLE, cx, cz)
    s += plane(candles([(830, 436, 72, 1.1)], t), Z_NEAR, cx, cz)
    s += warm_light(470, 360, 320, .34) + air() + side_dark("right", .24)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".68"/>'
    return s


def cam_koza_eye(t, dur=10.0):
    """Глаз хозяйки года крупно: огонь по краю кадра, медленный наезд."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=120, x0=-10, x1=10)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomr)"/>'
    s += plane(koza_head(t, 480, 300, 2.1), Z_HERO, cx, cz)
    s += warm_light(300, 240, 340, .3) + air(.05) + side_dark("right", .26)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".7"/>'
    return s


def cam_koza_turn(t, dur=10.0):
    """«Она просто отвернётся»: голова медленно уходит в сторону, глаза
    закрываются, пламя гривы опадает."""
    u = ease(min(1.0, t / max(.1, dur * .72)))
    cx, cz, _ = dolly(t, dur, z0=0, z1=90, x0=0, x1=26)
    s = f'<rect width="{W}" height="{H}" fill="url(#room)"/>'
    s += plane(_wall(t, [(62, 78, 210, 158)]), Z_WALL, cx, cz)
    head = koza_head(t if u < .55 else t + 100.0, 0, 0, .84)
    s += plane(f'<g transform="translate({480 - 60*u:.1f},{300 + 10*u:.1f}) rotate({-26*u:.2f})'
               f' scale({1 - .12*u:.3f},1)">{head}</g>', Z_HERO, cx, cz)
    s += plane(candles([(140, 436, 76, 1.05)], t), Z_NEAR, cx, cz)
    s += warm_light(170, 360, 280, .34 - .1 * u) + air(.06)
    s += side_dark("right", .24 + .16 * u) + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".7"/>'
    return s


def cam_koza_door(t, dur=10.0):
    """Гостья на пороге: светлый проём, снег за дверью, коза входит в дом."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=160, x0=30, x1=-24)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    door = (f'<rect x="300" y="60" width="360" height="420" rx="10" fill="{NGT}"{ST(9)}/>'
            f'<rect x="318" y="78" width="324" height="384" rx="6" fill="#33496f"/>'
            + A.snowfall(t, 24, 3) .replace('width="960"', 'width="360"') if False else
            f'<rect x="300" y="60" width="360" height="420" rx="10" fill="{NGT}"{ST(9)}/>'
            f'<rect x="318" y="78" width="324" height="384" rx="6" fill="#33496f"/>')
    for i in range(14):
        ph = (t / (3.2 + i % 4) + i * .13) % 1.0
        door += (f'<circle cx="{330 + (i*23) % 300:.0f}" cy="{80 + 380*ph:.0f}" r="{2.6 + (i%3):.1f}"'
                 f' fill="#eef5fb" opacity=".8"/>')
    door += f'<path d="M300 480 L660 480 L690 500 L270 500 Z" fill="{SNOW}"{ST(8)}/>'
    s += plane(door + art.tinsel(30), Z_WALL, cx, cz)
    s += plane(ground_shadow(470, 486, 150, 28, .45) + koza_head(t, 470, 300, .78), Z_HERO, cx, cz)
    s += plane(candles([(118, 442, 78, 1.05), (846, 446, 70, .95)], t), Z_NEAR, cx, cz)
    s += warm_light(480, 230, 360, .34) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_koza_window(t, dur=10.0):
    """Коза у окна: снег за стеклом, тёплая комната, камера чуть отъезжает вбок."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=110, x0=-30, x1=24)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    s += plane(art.window(520, 70, 330, 250, t) + art.tinsel(30), Z_WALL, cx, cz)
    s += plane(koza_head(t, 330, 306, .72), Z_HERO, cx, cz)
    s += plane(art.table(470) + candles([(640, 470, 58, 1.0)], t), Z_TABLE, cx, cz)
    s += plane(candles([(120, 440, 80, 1.1)], t), Z_NEAR, cx, cz)
    s += warm_light(160, 370, 300, .36) + air() + side_dark("right", .22)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_stol_kozy(t, dur=10.0):
    """Стол хозяйки года: зелень, сыры, птица, фрукты, морс — и воздух
    между тарелками. Камера медленно наезжает."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=150, x0=-20, x1=18)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += plane(_wall(t, [(60, 84, 220, 168), (680, 84, 220, 168)], 30), Z_WALL, cx, cz)
    s += plane(tree_new(t, 480, 300, .4), Z_TREE, cx, cz)
    s += plane(art.table(372, "#b8463f")
               + dish_greens(170, 356, .68) + dish_bird(470, 350, .78) + dish_cheese(760, 352, .66)
               + candles([(300, 372, 58, 1.0), (640, 372, 52, .95)], t), Z_TABLE, cx, cz)
    s += plane(dish_fruit(190, 470, .72) + jug_mors(780, 452, .72), Z_NEAR, cx, cz)
    s += warm_light(300, 340, 320, .34) + warm_light(650, 344, 290, .3) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".62"/>'
    return s


def cam_stol_kozy2(t, dur=10.0):
    """Тот же стол ближе: фрукты и морс на переднем плане, свечи горят."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=120, x0=26, x1=-22)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomr)"/>'
    s += plane(_wall(t, [(640, 70, 230, 172)], 28), Z_WALL, cx, cz)
    s += plane(art.table(340, "#b8463f") + dish_bird(300, 324, .72) + dish_greens(650, 326, .6)
               + candles([(150, 340, 60, 1.0), (820, 340, 54, .95)], t), Z_TABLE, cx, cz)
    s += plane(dish_fruit(620, 468, .8) + jug_mors(240, 450, .8), Z_NEAR, cx, cz)
    s += warm_light(240, 360, 300, .34) + air() + side_dark("left", .22)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".62"/>'
    return s


def cam_stol_loshadi(t, dur=10.0):
    """Стол Лошади: всё навалено, тарелки в два этажа, бокал ставить некуда."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=140, x0=22, x1=-18)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomr)"/>'
    s += plane(_wall(t, [(690, 76, 200, 150)], 30), Z_WALL, cx, cz)
    s += plane(art.table(356, "#b8463f")
               + sausage_plate(260, 336, .58) + dish_greens(560, 332, .5)
               + g(f'<ellipse cx="0" cy="0" rx="96" ry="30" fill="{CRM}"{ST(7)}/>'
                   f'<path d="M-74 -6 C-54 -42 54 -42 74 -6 C50 10 -50 10 -74 -6 Z" fill="{SNOW}"{ST(6)}/>', 760, 330, .9)
               + candles([(120, 356, 50, .9)], t), Z_TABLE, cx, cz)
    s += plane(g(f'<ellipse cx="0" cy="0" rx="104" ry="32" fill="{CRM}"{ST(7)}/>'
                 f'<ellipse cx="0" cy="-30" rx="86" ry="27" fill="{PCH}"{ST(7)}/>'
                 f'<ellipse cx="0" cy="-58" rx="68" ry="22" fill="{CRM}"{ST(7)}/>'
                 f'<path d="M-50 -70 C-30 -96 30 -96 50 -70 C30 -58 -30 -58 -50 -70 Z" fill="#b8463f"{ST(6)}/>',
                 380, 470, .92)
               + sausage_plate(790, 472, .6), Z_NEAR, cx, cz)
    s += warm_light(300, 360, 280, .3) + air() + side_dark("right", .24)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".68"/>'
    return s


def cam_kolbasa(t, dur=10.0):
    """Колбасная нарезка веером и запрещающий знак."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=140, x0=-14, x1=12)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    s += plane(_wall(t, [(96, 72, 196, 148)], 28), Z_WALL, cx, cz)
    s += plane(art.table(376, "#a8512c"), Z_TABLE, cx, cz)
    s += plane(ground_shadow(520, 398, 150, 26, .4) + sausage_plate(490, 362, 1.15), Z_HERO, cx, cz)
    s += plane(no_sign(490, 316, 178, 28), Z_HERO - 120, cx, cz)
    s += plane(candles([(140, 432, 76, 1.05)], t), Z_NEAR, cx, cz)
    s += warm_light(180, 370, 270, .3) + air() + side_dark("right", .22)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_guests_new(t, dur=10.0):
    """Гости за столом: моргают, покачиваются, поднимают бокалы."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=130, x0=-26, x1=22)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += plane(_wall(t, [(70, 84, 210, 160), (700, 84, 210, 160)], 32), Z_WALL, cx, cz)
    s += plane(guest(t, 220, 292, .84, "#f0c9a4", "#5a3a22", TER, "hat", .0)
               + guest(t, 420, 284, .88, "#e8bd94", "#3b2416", HRB, "bun", .35)
               + guest(t, 620, 290, .86, "#f2d2ae", "#6b4a2c", NGT, "bald", .7)
               + guest(t, 800, 300, .80, "#eec49c", "#4a2c18", RED, "cap", .15), Z_HERO, cx, cz)
    s += plane(art.table(420) + candles([(160, 420, 56, 1.0), (760, 420, 50, .9)], t), Z_TABLE, cx, cz)
    s += warm_light(200, 368, 300, .32) + warm_light(760, 372, 280, .3) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_kuranty_new(t, dur=10.0):
    """Полночь: часы, стол под ними, свечи и тёплый свет."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=130, x0=16, x1=-14)
    ang = -6 + 12 * ease(t / max(.1, dur))
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    s += plane(art.tinsel(28), Z_WALL, cx, cz)
    clock = (f'<circle cx="480" cy="230" r="146" fill="{CRM}"{ST(10)}/>'
             f'<circle cx="480" cy="230" r="120" fill="{SNOW}"{ST(6)}/>')
    for i in range(12):
        import math
        a = math.radians(i * 30)
        clock += (f'<circle cx="{480 + 100*math.sin(a):.1f}" cy="{230 - 100*math.cos(a):.1f}"'
                  f' r="{7 if i%3==0 else 4.5}" fill="{OUT}"/>')
    import math
    ra = math.radians(ang)
    clock += (f'<path d="M480 230 L{480 + 72*math.sin(ra):.1f} {230 - 72*math.cos(ra):.1f}"'
              f' stroke="{OUT}" stroke-width="12" stroke-linecap="round"/>')
    clock += (f'<path d="M480 230 L{480 + 96*math.sin(ra*1.4):.1f} {230 - 96*math.cos(ra*1.4):.1f}"'
              f' stroke="{TER}" stroke-width="8" stroke-linecap="round"/>')
    clock += f'<circle cx="480" cy="230" r="12" fill="{RED}"{ST(5)}/>'
    s += plane(clock, Z_HERO, cx, cz)
    s += plane(art.table(440, "#b8463f") + dish_fruit(760, 432, .62)
               + candles([(220, 440, 64, 1.05), (560, 440, 56, .95)], t), Z_TABLE, cx, cz)
    s += warm_light(480, 250, 330, .34) + air() + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".64"/>'
    s += lens_flare([scr(220, 440, Z_TABLE, cx, cz)[:2] + (.5, 18 * scr(220, 440, Z_TABLE, cx, cz)[2]),
                     scr(560, 440, Z_TABLE, cx, cz)[:2] + (.45, 16 * scr(560, 440, Z_TABLE, cx, cz)[2])])
    return s


def cam_finale_new(t, dur=10.0):
    """Финал: коза у накрытого стола, 2027 растёт, конфетти."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=120, x0=0, x1=0)
    u = ease(min(1.0, t / max(.1, dur)))
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += plane(_wall(t, [(70, 80, 210, 160)], 30), Z_WALL, cx, cz)
    s += plane(tree_new(t, 800, 430, .62), Z_TREE, cx, cz)
    s += plane(koza_head(t, 300, 286, .66), Z_HERO, cx, cz)
    s += plane(art.table(420, "#b8463f") + dish_bird(620, 404, .64) + dish_greens(840, 408, .5)
               + candles([(470, 420, 58, 1.0)], t), Z_TABLE, cx, cz)
    sc = .5 + .5 * u
    s += (f'<g transform="translate(640,210) scale({sc:.3f})" opacity="{min(1.0, u*1.6):.2f}">'
          f'<text x="0" y="0" text-anchor="middle" font-family="DejaVu Serif" font-size="150"'
          f' font-weight="bold" fill="{GLD}" stroke="{OUT}" stroke-width="8">2027</text></g>')
    s += A.confetti(t, 26)
    s += warm_light(300, 330, 320, .34) + air() + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".6"/>'
    s += lens_flare([scr(470, 420, Z_TABLE, cx, cz)[:2] + (.6, 19 * scr(470, 420, Z_TABLE, cx, cz)[2])])
    return s



def cam_koza_fire(t, dur=10.0):
    """Огненная сторона хозяйки: пламя гривы во весь кадр, искры летят,
    камера идёт вбок — огонь проходит мимо зрителя."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=100, x0=28, x1=-26)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomr)"/>'
    s += plane(koza_head(t, 500, 330, 1.45), Z_HERO, cx, cz)
    for i in range(14):
        ph = (t / (2.2 + i % 5 * .4) + i * .17) % 1.0
        s += (f'<circle cx="{60 + (i*77) % 860:.0f}" cy="{H - 540*ph:.0f}" r="{2.6 + (i%3)*1.4:.1f}"'
              f' fill="#ffd36e" opacity="{.75*(1-ph):.2f}"/>')
    s += warm_light(500, 300, 380, .4) + air(.06) + side_dark("left", .24)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_koza_table(t, dur=10.0):
    """Хозяйка года за столом: смотрит на блюда, свечи между ними."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=130, x0=-24, x1=20)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += plane(_wall(t, [(640, 74, 220, 166)], 30), Z_WALL, cx, cz)
    s += plane(koza_head(t, 300, 268, .62), Z_HERO, cx, cz)
    s += plane(art.table(396, "#b8463f") + dish_greens(620, 378, .58) + dish_cheese(830, 380, .54)
               + candles([(470, 396, 56, 1.0)], t), Z_TABLE, cx, cz)
    s += plane(dish_fruit(700, 486, .66), Z_NEAR, cx, cz)
    s += warm_light(470, 350, 310, .34) + air() + side_dark("right", .2)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".64"/>'
    return s


def cam_kitchen(t, dur=10.0):
    """Кухня тридцать первого: кастрюли, пар, доска с ножом — руки устали."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=140, x0=18, x1=-16)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    s += plane(_wall(t, [(120, 66, 190, 146)], 26), Z_WALL, cx, cz)
    pot = (f'<path d="M-104 -40 L104 -40 L88 70 C88 86 -88 86 -88 70 Z" fill="#6f6a60"{ST(9)}/>'
           f'<path d="M-118 -46 L118 -46 L118 -26 L-118 -26 Z" fill="#8a847a"{ST(7)}/>')
    s += plane(g(pot, 430, 300, 1.0) + A.smoke(430, 214, t, 3, 160, 1.0, .34)
               + g(f'<rect x="-150" y="86" width="300" height="26" rx="6" fill="#4a443c"{ST(7)}/>', 430, 300, 1.0),
               Z_HERO, cx, cz)
    s += plane(art.table(392) + g(f'<rect x="-120" y="-16" width="240" height="32" rx="8" fill="#9a6a34"{ST(7)}/>'
                                  f'<path d="M60 -30 L150 -52 L158 -38 L68 -14 Z" fill="#c9c4bb"{ST(6)}/>',
                                  700, 374, .8)
               + candles([(180, 392, 54, 1.0)], t), Z_TABLE, cx, cz)
    s += warm_light(480, 320, 330, .32) + air() + f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".68"/>'
    return s



# ===================== СВЕТОТЕНЬ ПО ФИГУРЕ (блок 3 лаборатории) =====================
import re as _re
_MASK = 0


def _white(body):
    """Тот же рисунок, залитый белым — из него делается маска по альфе."""
    b = _re.sub(r'fill="(?!none)[^"]*"', 'fill="#ffffff"', body)
    b = _re.sub(r'stroke="(?!none)[^"]*"', 'stroke="#ffffff"', b)
    b = _re.sub(r'opacity="[^"]*"', 'opacity="1"', b)
    return b


def light_figure(body, side="left", shade=.5, warm=.3, cx=480, half=230):
    """Свет ложится РОВНО ПО ФИГУРЕ, ни пикселя мимо: тёмный бок и тёплый
    освещённый. Приём из camera-lab (там вуаль умножалась на альфу слоя),
    здесь то же самое делает маска из того же рисунка, залитого белым."""
    global _MASK
    _MASK += 1
    m, d, w = f"mk{_MASK}", f"mkd{_MASK}", f"mkw{_MASK}"
    x1, x2 = ("1", "0") if side == "left" else ("0", "1")
    return (f'<defs><mask id="{m}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'{_white(body)}</mask>'
            f'<linearGradient id="{d}" x1="{x1}" y1="0" x2="{x2}" y2="0">'
            f'<stop offset="0" stop-color="#140d07" stop-opacity="{shade}"/>'
            f'<stop offset=".62" stop-color="#140d07" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="{w}" x1="{x2}" y1="0" x2="{x1}" y2="0">'
            f'<stop offset="0" stop-color="#ffcf7a" stop-opacity="{warm}"/>'
            f'<stop offset=".55" stop-color="#ffcf7a" stop-opacity="0"/></linearGradient></defs>'
            f'{body}'
            f'<g mask="url(#{m})"><rect width="{W}" height="{H}" fill="url(#{d})"/>'
            f'<rect width="{W}" height="{H}" fill="url(#{w})"/></g>')


# ===================== ОБЛЁТ 360° (блок 5 лаборатории) =====================
def koza_back(t, cx=480, cy=292, s=.86):
    """Коза со спины: затылок, рога уходят от зрителя, уши по бокам.
    Нужна для облёта — когда камера заходит за персонажа."""
    b = f'<circle cx="0" cy="-6" r="206" fill="{ORA}" opacity=".13"/>'
    for i, (ax, ay, sc, per, ph) in enumerate(((-150, -70, .9, 1.9, .0), (-50, -170, .95, 1.6, .3),
                                               (60, -168, .9, 2.2, .6), (158, -62, .9, 1.8, .2))):
        k = 1 + .09 * A.w(t, per, ph)
        fill = "url(#fl1)" if i % 2 else "url(#fl2)"
        b += (f'<g transform="translate({ax},{ay}) scale({sc*k:.3f})">'
              f'<path d="M0 54 C-42 26 -46 -18 -22 -54 C-26 -24 -10 -16 -2 -30'
              f' C6 -46 2 -70 -12 -92 C34 -72 62 -30 56 6 C52 36 28 58 0 54 Z"'
              f' fill="{fill}"{ST(7)}/></g>')
    HORN, HORN2 = "#6d5740", "#463726"
    for sg in (-1, 1):
        b += (f'<path d="M{sg*52} -116 C{sg*70} -168 {sg*120} -200 {sg*178} -198'
              f' C{sg*204} -196 {sg*210} -174 {sg*188} -166 C{sg*146} -152 {sg*110} -130 {sg*92} -92 Z"'
              f' fill="{HORN}" stroke="{OUT}" stroke-width="9" stroke-linejoin="round"/>')
        for i in range(5):
            b += (f'<path d="M{sg*(70+i*24)} {-128-i*14} q{sg*11} {-12} {sg*23} {-14}"'
                  f' stroke="{HORN2}" stroke-width="5" fill="none" opacity=".8"/>')
    for sg in (-1, 1):
        rot = A.sway(t, 6.1, .2 + .3 * (sg > 0), 2.0)
        b += (f'<g transform="rotate({rot*sg:.2f} {sg*96} 4)">'
              f'<path d="M{sg*86} -16 C{sg*140} -24 {sg*186} 6 {sg*188} 44'
              f' C{sg*152} 60 {sg*100} 38 {sg*80} 10 Z" fill="#e2d6bc"{ST(8)}/></g>')
    b += (f'<path d="M0 -136 C82 -136 136 -82 136 -14 C136 44 118 86 92 120'
          f' C70 150 42 176 0 190 C-42 176 -70 150 -92 120 C-118 86 -136 44 -136 -14'
          f' C-136 -82 -82 -136 0 -136 Z" fill="#ece0c8"{ST(9)}/>')
    b += (f'<g stroke="#d3c4a6" stroke-width="5" fill="none" opacity=".9">'
          f'<path d="M-70 -70 C-40 -46 -40 10 -62 54 M0 -92 C24 -50 22 14 -2 70'
          f' M70 -68 C96 -40 92 12 66 56"/></g>')
    b += (f'<path d="M-128 190 C-62 224 62 224 128 190 C136 218 130 240 116 252'
          f' C46 286 -46 286 -116 252 C-132 240 -136 218 -128 190 Z" fill="{RED}"{ST(9)}/>')
    return g(b, cx, cy, s)


def cam_oblet(t, dur=12.0):
    """ОБЛЁТ 360° вокруг хозяйки года: фигура стоит, кружит КАМЕРА.
    Когда камера заходит за спину, видно затылок и рога с обратной стороны;
    комната за ней едет в другую сторону, кольцо на полу показывает,
    что это именно облёт, а не поворот картинки."""
    import math
    k = ease(t / max(.1, dur))
    a = 2 * math.pi * k
    ca, sa = math.cos(a), math.sin(a)
    cx = 190 * sa                    # камера объезжает — фон едет в противоход
    cz = 60 + 40 * (1 - ca)
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    wall = (art.window(40, 70, 210, 158, t) + art.window(700, 70, 210, 158, t) + art.tinsel(32))
    s += plane(wall, Z_WALL, cx, cz)
    s += plane(tree_new(t, 820, 456, .62), Z_TREE, cx * .8, cz)
    # кольцо на полу: эллипс, который ходит вместе с камерой
    ring = ""
    for r, op in ((210, .5), (150, .34), (96, .22)):
        ring += (f'<ellipse cx="470" cy="430" rx="{r}" ry="{r*0.26:.0f}" fill="none"'
                 f' stroke="{GLD}" stroke-width="4" opacity="{op}"/>')
    for i in range(12):
        ang = a + i * math.pi / 6
        ring += (f'<path d="M{470 + 96*math.cos(ang):.1f} {430 + 25*math.sin(ang):.1f}'
                 f' L{470 + 210*math.cos(ang):.1f} {430 + 55*math.sin(ang):.1f}"'
                 f' stroke="{GLD}" stroke-width="3" opacity=".22"/>')
    s += plane(ring, Z_TABLE, cx, cz)
    # фигура: спереди или со спины, по знаку косинуса; ширина сжимается как cos
    squeeze = max(.18, abs(ca))
    body = koza_head(t, 0, 0, .78) if ca >= 0 else koza_back(t, 0, 0, .78)
    turn = (f'<g transform="translate(470,300) scale({squeeze:.3f},1)'
            f' translate({-0:.1f},{-0:.1f})">{body}</g>')
    s += plane(ground_shadow(470, 452, 150 * squeeze + 40, 26, .5)
               + light_figure(turn, "left" if sa < 0 else "right", .62, .42, 470, 210), Z_HERO, 0, cz)
    s += plane(candles([(130, 452, 78, 1.05), (830, 456, 70, .95)], t), Z_NEAR, cx * 1.3, cz)
    s += warm_light(160 if sa < 0 else 820, 360, 320, .36) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".64"/>'
    s += lens_flare([scr(130, 452, Z_NEAR, cx * 1.3, cz)[:2] + (.55, 18 * scr(130, 452, Z_NEAR, cx * 1.3, cz)[2]),
                     scr(830, 456, Z_NEAR, cx * 1.3, cz)[:2] + (.5, 17 * scr(830, 456, Z_NEAR, cx * 1.3, cz)[2])])
    return s


def cam_svet(t, dur=10.0):
    """Светотень по фигуре: источник едет, тёмный бок переезжает по козе."""
    import math
    k = ease(t / max(.1, dur))
    side = "left" if k < .5 else "right"
    cx, cz, _ = dolly(t, dur, z0=0, z1=120, x0=-18, x1=16)
    s = f'<rect width="{W}" height="{H}" fill="url(#room)"/>'
    s += plane(art.window(70, 70, 210, 160, t) + art.tinsel(30), Z_WALL, cx, cz)
    fig = koza_head(t, 470, 296, .74)
    s += plane(ground_shadow(470, 452, 150, 26, .5)
               + light_figure(fig, side, .66, .46, 470, 215), Z_HERO, cx, cz)
    lx = 150 + 660 * k
    s += plane(candles([(lx, 452, 82, 1.1)], t), Z_NEAR, cx, cz)
    s += warm_light(lx, 370, 300, .4) + air(.06)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    s += lens_flare([scr(lx, 452, Z_NEAR, cx, cz)[:2] + (.7, 20 * scr(lx, 452, Z_NEAR, cx, cz)[2])])
    return s




# ============ БЛОК 16 — АНАМОРФНЫЙ БЛИК В ОБЪЕКТИВ ============
_FL = 0


def lens_flare(srcs, cx=W / 2, cy=H / 2):
    """Блик объектива от ярких источников в кадре: холодная горизонтальная
    полоса с ядром, тёплый ореол, кольца-призраки по линии «источник — центр»
    и слабая вуаль у оси. Кладётся ПОСЛЕДНИМ, на собранный кадр.
    srcs — [(x, y, сила 0..1, радиус)]; больше четырёх не ставить,
    слабее 0.012 не рисовать (правило лаборатории)."""
    global _FL
    out = ""
    srcs = sorted((s for s in srcs if s[2] >= .012), key=lambda s: -s[2])[:4]
    for x, y, k, r in srcs:
        _FL += 1
        a, b, c = f"fla{_FL}", f"flb{_FL}", f"flc{_FL}"
        # у оси кадра блик разгорается, у края слабеет — так ведёт себя объектив
        ax = 1.0 - min(1.0, (abs(x - cx) / (W * .62) + abs(y - cy) / (H * .9)))
        kk = k * (.35 + .65 * max(0.0, ax))
        L = r * 9.5
        out += (f'<defs><linearGradient id="{a}" gradientUnits="userSpaceOnUse"'
                f' x1="{x - L}" y1="0" x2="{x + L}" y2="0">'
                f'<stop offset="0" stop-color="#bfe6ff" stop-opacity="0"/>'
                f'<stop offset=".5" stop-color="#dff2ff" stop-opacity="{kk*.5:.3f}"/>'
                f'<stop offset="1" stop-color="#bfe6ff" stop-opacity="0"/></linearGradient>'
                f'<radialGradient id="{b}"><stop offset="0" stop-color="#ffe6b8" stop-opacity="{kk*.75:.3f}"/>'
                f'<stop offset=".45" stop-color="#ffcf7a" stop-opacity="{kk*.28:.3f}"/>'
                f'<stop offset="1" stop-color="#ffcf7a" stop-opacity="0"/></radialGradient>'
                f'<radialGradient id="{c}"><stop offset="0" stop-color="#ffffff" stop-opacity="{kk*.9:.3f}"/>'
                f'<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>')
        out += f'<rect x="{x - L:.1f}" y="{y - r*.42:.1f}" width="{2*L:.1f}" height="{r*.84:.1f}" fill="url(#{a})"/>'
        out += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r*2.6:.1f}" ry="{r*2.6:.1f}" fill="url(#{b})"/>'
        out += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r*1.5:.1f}" ry="{r*.5:.1f}" fill="url(#{c})"/>'
        # призраки по линии «источник — центр» и дальше за центр
        for i, (p, rr, col, op) in enumerate(((.42, .5, "#9ad0ff", .16), (.78, .34, "#ffd1a0", .13),
                                              (1.26, .62, "#9ae0b0", .10), (1.62, .42, "#ffb0c0", .09))):
            gx, gy = x + (cx - x) * p, y + (cy - y) * p
            out += (f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{r*rr*1.9:.1f}" fill="none"'
                    f' stroke="{col}" stroke-width="{max(2.0, r*rr*.7):.1f}" opacity="{kk*op:.3f}"/>')
        if ax > .45:                      # вуаль, когда источник близко к оси
            out += f'<rect width="{W}" height="{H}" fill="#cfe4ff" opacity="{kk*.05:.3f}"/>'
    return out


def scr(x, y, z, camx=0.0, camz=0.0, F=BASE_Z):
    """Куда уезжает точка плана на экране — чтобы блик держался на источнике,
    а не висел в воздухе, когда камера едет."""
    k = F / max(60.0, z - camz)
    return (W / 2 + (x - W / 2 - camx) * k, H / 2 + (y - H / 2) * k, k)


def flare_from_candles(items, table_y, k=.55):
    """Источники блика прямо из свечей сцены: координата пламени и сила."""
    return [(x, table_y + dy - h * sc - 6 * sc, k * sc, 16 * sc) for x, dy, h, sc in items]


# ============ ОСТАЛЬНЫЕ ХОДЫ КАМЕРЫ (блоки 6-15 лаборатории) ============
def rig(planes, *, camx=0.0, camz=0.0, pan=0.0, tilt=0.0, roll=0.0, over=1.0):
    """Сборка кадра из планов плюс ходы камеры, которых нет в формуле глубины.
    pan/tilt — ПОВОРОТ камеры: сдвиг одинаковый для всех планов, параллакса
    нет (этим панорама и отличается от проезда). roll — наклон горизонта.
    over — оверскан, чтобы при сдвиге не оголялись края кадра."""
    inner = "".join(plane(b, z, camx, camz) for z, b in planes)
    return (f'<g transform="translate({W/2},{H/2}) rotate({roll:.3f}) scale({over:.4f})'
            f' translate({-W/2 + pan:.2f},{-H/2 + tilt:.2f})">{inner}</g>')


def punch(u):
    """Кривая удара: скорость на входе и выходе нулевая, но 65% хода
    проходит за первую треть — глаз читает удар, а не проезд."""
    return ease(max(0.0, min(1.0, u))) ** 0.62


def beats(t, table):
    """Серия ударов: (время удара, ход по глубине). Между ударами кадр живёт
    малым подъездом, полная остановка читается как стоп-кадр."""
    cz = 0.0
    for at, step in table:
        if t >= at:
            cz += step * punch((t - at) / 0.6)
    return cz + 6.0 * t


def _room(t, wins=((70, 80, 210, 158), (690, 80, 210, 158)), tins=30):
    return "".join(art.window(*w, t) for w in wins) + art.tinsel(tins)


def cam_pan(t, dur=10.0):
    """БЛОК 6 — ПАНОРАМА: камера стоит на месте и поворачивается.
    Планы уезжают ОДНИМ темпом, параллакса нет; движение читается по граням
    окон, ёлке и свечам, которые проходят через кадр."""
    k = ease(t / max(.1, dur))
    pan = -150 + 300 * k
    planes = [(Z_WALL, _room(t, ((40, 76, 230, 170), (430, 70, 230, 170), (820, 80, 230, 170)), 34)),
              (Z_TREE, tree_new(t, 300, 470, .72) + tree_new(t, 760, 470, .56)),
              (Z_TABLE, art.table(466) + candles([(180, 466, 58, 1.0), (560, 466, 52, .95),
                                                  (880, 466, 50, .9)], t)),
              (Z_NEAR, dish_fruit(120, 430, .7) + jug_mors(860, 420, .66))]
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += rig(planes, camx=0, camz=40, pan=pan, over=1.22)
    s += warm_light(480 - pan * .4, 360, 340, .32) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_crane(t, dur=10.0):
    """БЛОК 7 — ПОДЪЁМ-КРАН: камера идёт снизу вверх и раскрывает стол.
    Видно, как у блюд открываются «крыши», а свечи уходят вниз кадра."""
    k = ease(t / max(.1, dur))
    planes = [(Z_WALL, _room(t, ((60, 60, 220, 164), (680, 60, 220, 164)), 28)),
              (Z_TREE, tree_new(t, 820, 470, .66)),
              (Z_HERO, koza_head(t, 250, 300, .52)),
              (Z_TABLE, art.table(430, "#b8463f") + dish_greens(430, 414, .62)
               + dish_bird(660, 408, .66) + candles([(150, 430, 58, 1.0)], t)),
              (Z_NEAR, dish_fruit(300, 500, .8))]
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += rig(planes, camz=30 + 90 * k, tilt=150 - 230 * k, over=1.3)
    s += warm_light(300, 330, 340, .33) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".64"/>'
    return s


def cam_wipe(t, dur=10.0):
    """БЛОК 8 — УХОД ПЕРЕДНЕГО ПЛАНА: мимо объектива проходит кувшин и на
    треть секунды закрывает кадр целиком. Под этим прикрытием место
    меняется — склейки не видно, камера не останавливается."""
    k = t / max(.1, dur)
    fx = -520 + 2000 * k                       # кувшин идёт слева направо
    covered = abs(fx - 480) < 150              # окно полного накрытия
    first = fx < 480
    if first:
        planes = [(Z_WALL, _room(t, ((60, 76, 220, 166), (690, 76, 220, 166)), 30)),
                  (Z_TREE, tree_new(t, 810, 466, .64)),
                  (Z_TABLE, art.table(442) + dish_cheese(300, 424, .66)
                   + candles([(150, 442, 56, 1.0)], t))]
        bg = "roomc"
    else:
        planes = [(Z_WALL, _room(t, ((120, 70, 230, 170), (620, 70, 230, 170)), 26)),
                  (Z_HERO, koza_head(t, 470, 296, .66)),
                  (Z_TABLE, art.table(430, "#b8463f") + dish_bird(700, 410, .6)
                   + candles([(180, 430, 58, 1.0)], t))]
        bg = "roomr"
    s = f'<rect width="{W}" height="{H}" fill="url(#{bg})"/>'
    s += rig(planes, camx=-60 + 120 * k, camz=40)
    s += warm_light(300, 360, 300, .3) + air()
    # сам накрывающий предмет: ближе всех к объективу, поэтому огромный
    s += plane(jug_mors(fx, 300, 3.4), 700, 0, 0)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_push(t, dur=10.0):
    """БЛОК 9 — PUSH: три коротких удара по 0,6 с под слово, между ними
    выдержка; камера назад не отходит никогда."""
    cz = beats(t, ((1.2, 150.0), (4.6, 140.0), (7.8, 130.0)))
    planes = [(Z_WALL, _room(t, ((70, 80, 210, 158),), 30)),
              (Z_HERO, koza_head(t, 470, 292, .72)),
              (Z_TABLE, art.table(448) + candles([(140, 448, 60, 1.0), (820, 448, 54, .95)], t))]
    s = f'<rect width="{W}" height="{H}" fill="url(#room)"/>'
    s += rig(planes, camz=cz)
    s += warm_light(170, 360, 300, .34) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_follow(t, dur=10.0):
    """БЛОК 10 — ПРОВОДКА: коза идёт, камера идёт вместе с ней. Она стоит
    в кадре на месте, а комната проносится мимо."""
    k = t / max(.1, dur)
    shift = 1700 * k
    wall = ""
    for i in range(6):
        x = 60 + i * 320 - (shift % 1920)
        wall += art.window(x, 76, 210, 160, t)
    wall += art.tinsel(30)
    trees = tree_new(t, 1200 - (shift * .72) % 2400, 470, .62)
    tbl = art.table(452)
    for i in range(7):
        x = 120 + i * 300 - (shift * .9) % 2100
        tbl += candles([(x, 452, 56, 1.0)], t)
    bob = 5 * A.w(t, 0.9)
    planes = [(Z_WALL, wall), (Z_TREE, trees), (Z_TABLE, tbl),
              (Z_HERO, koza_head(t, 470, 300 + bob, .74))]
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    s += rig(planes, camz=40)
    s += warm_light(470, 360, 320, .3) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_tilt(t, dur=10.0):
    """БЛОК 11 — НАКЛОН ВВЕРХ: камера стоит, взгляд идёт снизу вверх по ёлке
    до звезды. Нужен предмет с гранями — потому ёлка, окна и подарки."""
    k = ease(t / max(.1, dur))
    planes = [(Z_WALL, _room(t, ((60, 110, 200, 150), (700, 110, 200, 150)), 40)),
              (Z_TREE, tree_new(t, 480, 620, 1.22)),
              (Z_TABLE, art.table(620) + candles([(150, 620, 60, 1.0), (810, 620, 54, .95)], t))]
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    s += rig(planes, camz=30, tilt=-250 + 420 * k, over=1.34)
    s += warm_light(480, 300 + 120 * (1 - k), 340, .3) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".64"/>'
    return s


def cam_arc(t, dur=10.0):
    """БЛОК 12 — ДУГА 32°: обрезанный облёт. Ракурс меняется, но кадр не
    превращается в номер, поэтому приём можно повторять в ролике."""
    import math
    k = ease(t / max(.1, dur))
    a = math.radians(-16 + 32 * k)
    ca, sa = math.cos(a), math.sin(a)
    planes = [(Z_WALL, _room(t, ((60, 76, 220, 166), (690, 76, 220, 166)), 30)),
              (Z_TREE, tree_new(t, 820, 468, .6))]
    fig = f'<g transform="translate(470,300) scale({ca:.3f},1) translate(-470,-300)">' \
          f'{koza_head(t, 470, 300, .74)}</g>'
    planes.append((Z_HERO, ground_shadow(470, 450, 150 * ca + 30, 26, .5)
                   + light_figure(fig, "left" if sa < 0 else "right", .6, .4, 470, 210)))
    planes.append((Z_TABLE, art.table(452) + candles([(150, 452, 58, 1.0), (820, 452, 52, .95)], t)))
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += rig(planes, camx=150 * sa, camz=60 - 20 * k)
    s += warm_light(470 - 220 * sa, 360, 320, .34) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_down(t, dur=10.0):
    """БЛОК 13 — СНИЖЕНИЕ: сверху над столом вниз, к одной тарелке.
    По дороге у блюд закрываются «крыши» и открываются бока."""
    k = ease(t / max(.1, dur))
    planes = [(Z_WALL, _room(t, ((60, 70, 220, 164), (690, 70, 220, 164)), 28)),
              (Z_TREE, tree_new(t, 830, 470, .6)),
              (Z_TABLE, art.table(420, "#b8463f") + dish_greens(200, 404, .6)
               + dish_cheese(760, 404, .58) + candles([(470, 420, 58, 1.0)], t)),
              (Z_HERO, dish_bird(470, 388, .9))]
    s = f'<rect width="{W}" height="{H}" fill="url(#roomc)"/>'
    s += rig(planes, camz=20 + 150 * k, tilt=-210 + 250 * k, over=1.3)
    s += warm_light(470, 380, 330, .34) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".64"/>'
    return s


def cam_dutch(t, dur=10.0):
    """БЛОК 14 — НАКЛОН ГОРИЗОНТА: кадр медленно валится набок под подъезд.
    Потолок 9°: дальше читается как ошибка, а не приём."""
    k = ease(t / max(.1, dur))
    planes = [(Z_WALL, _room(t, ((60, 76, 220, 166), (690, 76, 220, 166)), 30)),
              (Z_HERO, koza_head(t, 470, 296, .7)),
              (Z_TABLE, art.table(452) + candles([(150, 452, 58, 1.0), (820, 452, 52, .95)], t))]
    s = f'<rect width="{W}" height="{H}" fill="url(#roomr)"/>'
    s += rig(planes, camz=30 + 70 * k, roll=9.0 * k, over=1.26)
    s += warm_light(200, 360, 300, .32) + air() + side_dark("right", .22)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


def cam_vertigo(t, dur=10.0):
    """БЛОК 15 — ДОЛЛИ-ЗУМ: камера ОТЪЕЗЖАЕТ, а фокус растёт ровно настолько,
    чтобы коза осталась того же размера. Уменьшается не она — наваливается
    комната за ней. Нужна ГЛУБИНА, поэтому стена тут отнесена дальше обычного.
    Приём один раз на ролик и только под сильный смысл."""
    k = ease(t / max(.1, dur))
    ZW, ZT, ZH, ZN = 5200, 3000, 2000, 1500
    camz = -900 * k
    comp = (ZH - camz) / ZH            # зум ровно компенсирует отъезд
    planes = [(ZW, _room(t, ((20, 70, 250, 180), (690, 70, 250, 180)), 26)),
              (ZT, tree_new(t, 840, 470, .66) + tree_new(t, 120, 474, .5)),
              (ZH, koza_head(t, 470, 300, .72)),
              (ZN, art.table(452) + candles([(140, 452, 60, 1.0), (820, 452, 54, .95)], t))]
    s = f'<rect width="{W}" height="{H}" fill="url(#room)"/>'
    s += rig(planes, camz=camz, over=comp)
    s += warm_light(470, 360, 320, .32) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".66"/>'
    return s


# -------- старые рисунки с камерой: мягкий наезд вместо зума окна --------
def pushin(name, z1=120.0, x1=0.0):
    """Готовый рисунок из art.py, снятый камерой: плавный перспективный наезд.
    Масштаб всегда > 1, поэтому края кадра не оголяются."""
    def f(t, dur=8.0, _n=name, _z=z1, _x=x1):
        cx, cz, _ = dolly(t, dur, z0=55, z1=_z, x0=-_x, x1=_x)
        return plane(art.SCENES[_n](t), Z_HERO, cx, cz)
    return f


PUSH = ["salat_mayo", "pork", "meat_only", "cake_no", "two_floors", "heap", "lamb_no",
        "lamb_dishes", "empty_plate", "feast", "horse", "duck", "duck_cut", "duck_glaze",
        "cheese", "cheese_trio", "cheese_slice", "pumpkin", "pumpkin_goat", "pumpkin_slice",
        "pumpkin_topping", "pate_toast", "fish", "fish_serve", "fish_steam", "fish_left",
        "apples", "apple_cream", "fruit_basket", "round_fruits", "honey_nuts", "goat_milk",
        "mors", "greens", "greens_board", "herb_glasses", "herb_three", "white_no", "pear_no",
        "pelmeni_gold", "lanterns", "calendar_feb", "kuranty", "basics_six", "seafood",
        "table_wide", "table_top", "guests_toast", "retro", "finale_2027", "mushrooms_pan"]

SCENES = {
    "cam_room": cam_room, "cam_room2": cam_room2,
    "cam_koza": cam_koza, "cam_oblet": cam_oblet, "cam_svet": cam_svet,
    "cam_pan": cam_pan, "cam_wipe_s": (lambda t, dur=3.5: cam_wipe(t, 3.5)), "cam_crane": cam_crane, "cam_wipe": cam_wipe, "cam_push": cam_push,
    "cam_follow": cam_follow, "cam_tilt": cam_tilt, "cam_arc": cam_arc, "cam_down": cam_down,
    "cam_dutch": cam_dutch, "cam_vertigo": cam_vertigo, "cam_koza_eye": cam_koza_eye, "cam_koza_turn": cam_koza_turn,
    "cam_koza_door": cam_koza_door, "cam_koza_window": cam_koza_window,
    "cam_tree": cam_tree, "cam_ded": cam_ded, "cam_zapret": cam_zapret, "cam_okna": cam_okna,
    "cam_stol_kozy": cam_stol_kozy, "cam_stol_kozy2": cam_stol_kozy2,
    "cam_stol_loshadi": cam_stol_loshadi, "cam_kolbasa": cam_kolbasa,
    "cam_guests": cam_guests_new, "cam_koza_fire": cam_koza_fire,
    "cam_koza_table": cam_koza_table, "cam_kitchen": cam_kitchen, "cam_kuranty": cam_kuranty_new, "cam_finale": cam_finale_new,
}
for _n in PUSH:
    if _n in art.SCENES:
        SCENES["p_" + _n] = pushin(_n)
NO_GLARE = {"cam_koza_eye"}
