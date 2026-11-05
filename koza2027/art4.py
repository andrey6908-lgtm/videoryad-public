# -*- coding: utf-8 -*-
"""ПРОБНИК РЕЦЕПТА: приготовление оливье в стиле «Года козы».

Проверяем одну мысль: ляжет ли рецепт на тот же язык, что и ролик про стол.
Поэтому ни одного нового приёма — та же сцена `art3.stage` (стена с окном,
стол, свет, виньетка, ход камеры по имени `@ход`), та же палитра и тот же
толстый контур. Своё здесь только то, чего в еде ролика не было: ПРОЦЕСС —
нож ходит, кубики падают на доску, вода кипит, пар идёт.

Каждый предмет — функция времени, поэтому кадр живой и на паузе тоже:
без этого рецепт превращается в слайд-шоу (правило 2 скилла).
"""
import math
import anim as A
import art
import art2 as A2
import art3 as A3
from art2 import W, H, OUT, RED, ORA, TER, PCH, CRM, GLD, GRN, HRB, SNOW, WOOL, g, ST

POT   = "#9aa3ab"
POTD  = "#767f88"
WATER = "#8fc0dc"
BLADE = "#cfd6dc"
HAND  = "#6b3f1c"
POTAT = "#e3c478"
POTIN = "#f2e3b8"
ONION = "#f2ead6"
ONSKN = "#d8b45e"
YOLK  = "#f0c43c"


# --------------------------------------------------------------- предметы
def board(rx=228, ry=36):
    """Доска: круглая, лежит на столе. Толщина сбоку — без неё плоско."""
    return (f'<path d="M{-rx} 0 L{-rx} 15 C{-rx} {15+ry*0.78} {rx} {15+ry*0.78} {rx} 15 L{rx} 0 Z"'
            f' fill="#6b4320"{ST(7)}/>'
            f'<ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="url(#wood)"{ST(7)}/>'
            f'<ellipse cx="{rx*0.74:.0f}" cy="{-ry*0.1:.0f}" rx="13" ry="9" fill="#5c3a1c"{ST(4)}/>')


def knife(x, y, ang, L=150):
    """Нож: лезвие и ручка. Вращается вокруг конца ручки — как в руке."""
    b = (f'<path d="M0 -4 L{L} -13 L{L} 11 L0 16 Z" fill="{BLADE}"{ST(6)}/>'
         f'<path d="M8 -1 L{L-10} -9" stroke="#eef3f7" stroke-width="4" opacity=".8"/>'
         f'<rect x="-74" y="-9" width="80" height="26" rx="8" fill="{HAND}"{ST(6)}/>'
         f'<rect x="-66" y="-3" width="62" height="6" rx="3" fill="#8a5527" opacity=".8"/>')
    return f'<g transform="translate({x},{y}) rotate({ang:.2f})">{b}</g>'


def potato(x, y, r=30, raw=True):
    c = POTAT if raw else POTIN
    b = (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*0.78:.1f}" fill="{c}"{ST(6)}/>'
         f'<ellipse cx="{x-r*0.3:.0f}" cy="{y-r*0.3:.0f}" rx="{r*0.3:.0f}" ry="{r*0.2:.0f}"'
         f' fill="#ffffff" opacity=".22"/>')
    if raw:
        b += "".join(f'<circle cx="{x-r*0.4+i*r*0.4:.0f}" cy="{y-r*0.1+(i%2)*r*0.3:.0f}" r="3"'
                     f' fill="#b88e3e"/>' for i in range(3))
    return b


def cube(x, y, s=17, col=POTIN, top="#fbf3df"):
    """Кубик: верхняя грань светлее — отсюда и объём, без всякого 3D."""
    return (f'<path d="M{x-s} {y} L{x} {y-s*0.52:.1f} L{x+s} {y} L{x+s} {y+s*0.72:.1f}'
            f' L{x} {y+s*1.24:.1f} L{x-s} {y+s*0.72:.1f} Z" fill="{col}"{ST(5)}/>'
            f'<path d="M{x-s} {y} L{x} {y-s*0.52:.1f} L{x+s} {y} L{x} {y+s*0.52:.1f} Z"'
            f' fill="{top}"{ST(4)}/>')


def onion_half(x, y, r=40):
    b = (f'<path d="M{x-r} {y} C{x-r} {y-r*1.25:.0f} {x+r} {y-r*1.25:.0f} {x+r} {y} Z"'
         f' fill="{ONION}"{ST(6)}/>')
    for k in (0.72, 0.46, 0.22):
        b += (f'<path d="M{x-r*k:.0f} {y} C{x-r*k:.0f} {y-r*1.25*k:.0f} {x+r*k:.0f} {y-r*1.25*k:.0f}'
              f' {x+r*k:.0f} {y}" fill="none" stroke="{ONSKN}" stroke-width="4"/>')
    b += f'<path d="M{x-2} {y-r*1.2:.0f} L{x+2} {y-r*1.46:.0f}" stroke="{HRB}" stroke-width="6"/>'
    return b


def onion_slice(x, y, w=26):
    return (f'<path d="M{x-w} {y} C{x-w} {y-w*0.9:.0f} {x+w} {y-w*0.9:.0f} {x+w} {y}"'
            f' fill="none" stroke="{ONION}" stroke-width="7" stroke-linecap="round"'
            f' stroke-linejoin="round"/>'
            f'<path d="M{x-w} {y} C{x-w} {y-w*0.9:.0f} {x+w} {y-w*0.9:.0f} {x+w} {y}"'
            f' fill="none" stroke="{OUT}" stroke-width="2.4" opacity=".7"/>')


def carrot(x, y, L=96, r=22, ang=-16):
    b = (f'<path d="M{-L*0.5} {-r} C{-L*0.1} {-r*1.18:.0f} {L*0.3} {-r*0.7:.0f} {L*0.5} 0'
         f' C{L*0.3} {r*0.7:.0f} {-L*0.1} {r*1.18:.0f} {-L*0.5} {r} Z" fill="{ORA}"{ST(6)}/>'
         f'<g stroke="#b85f12" stroke-width="3.4" opacity=".8">'
         f'<path d="M{-L*0.24} {-r*0.5:.0f} L{-L*0.18} {r*0.5:.0f}"/>'
         f'<path d="M{-L*0.02} {-r*0.42:.0f} L{L*0.04} {r*0.42:.0f}"/>'
         f'<path d="M{L*0.2} {-r*0.3:.0f} L{L*0.24} {r*0.3:.0f}"/></g>'
         f'<g stroke="{HRB}" stroke-width="6" fill="none" stroke-linecap="round">'
         f'<path d="M{-L*0.5} {-r*0.2:.0f} C{-L*0.72} {-r*0.9:.0f} {-L*0.78} {-r*1.5:.0f} {-L*0.66} {-r*1.9:.0f}"/>'
         f'<path d="M{-L*0.5} 0 C{-L*0.78} {-r*0.2:.0f} {-L*0.92} {-r*0.7:.0f} {-L*0.9} {-r*1.2:.0f}"/></g>')
    return f'<g transform="translate({x},{y}) rotate({ang})">{b}</g>'


def carrot_round(x, y, r=15):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{ORA}"{ST(5)}/>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.56:.1f}" fill="#f0921f"{ST(3)}/>')


def egg(x, y, r=22, half=False):
    if not half:
        return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*1.24:.1f}" fill="#f6edd2"{ST(6)}/>'
                f'<ellipse cx="{x-r*0.3:.0f}" cy="{y-r*0.4:.0f}" rx="{r*0.26:.0f}" ry="{r*0.34:.0f}"'
                f' fill="#ffffff" opacity=".4"/>')
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*1.2:.1f}" fill="#fbf6e6"{ST(6)}/>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.52:.1f}" fill="{YOLK}"{ST(5)}/>')


def pot(t, w=96, h=84):
    """Кастрюля: вода, пузыри, пар. Пузыри поднимаются и лопаются у края."""
    b = (f'<path d="M{-w} {-h} L{-w*0.86:.0f} 12 C{-w*0.86:.0f} 30 {w*0.86:.0f} 30 {w*0.86:.0f} 12'
         f' L{w} {-h} Z" fill="{POT}"{ST(7)}/>'
         f'<path d="M{-w*0.5:.0f} {-h+8} L{-w*0.42:.0f} 8" stroke="#b7bfc6" stroke-width="7" opacity=".55"/>'
         f'<ellipse cx="0" cy="{-h}" rx="{w}" ry="{w*0.26:.0f}" fill="{POTD}"{ST(7)}/>'
         f'<ellipse cx="0" cy="{-h+5}" rx="{w*0.86:.0f}" ry="{w*0.2:.0f}" fill="{WATER}"{ST(5)}/>')
    for i in range(7):                       # пузыри: своя фаза у каждого
        p = ((t*0.9) + i*0.137) % 1.0
        rr = 3.0 + 5.0*p
        op = max(0.0, 1.0 - p)*0.85
        bx = -w*0.6 + i*w*0.2 + 6*A.w(t, 1.9, i*0.21)
        b += (f'<circle cx="{bx:.0f}" cy="{-h+6-p*7:.0f}" r="{rr:.1f}" fill="#dff0fa"'
              f' opacity="{op:.2f}" stroke="{OUT}" stroke-width="1.6"/>')
    for i, (ex, ez) in enumerate(((-44, 0.0), (-6, -3.0), (34, 1.0), (66, -2.0))):
        b += egg(ex, -h + 2 + ez, 19)
    # ручки: толстая тёмная дуга под цветом металла, контур рисовать нечему
    for sx in (-1, 1):
        b += (f'<path d="M{sx*(w+4)} {-h+26} C{sx*(w+30)} {-h+26} {sx*(w+30)} {-h-4}'
              f' {sx*(w+4)} {-h-2}" fill="none" stroke="{OUT}" stroke-width="15"'
              ' stroke-linecap="round"/>'
              f'<path d="M{sx*(w+4)} {-h+26} C{sx*(w+30)} {-h+26} {sx*(w+30)} {-h-4}'
              f' {sx*(w+4)} {-h-2}" fill="none" stroke="{POTD}" stroke-width="9"'
              ' stroke-linecap="round"/>')
    b += A.smoke(0, -h - 6, t, 3, 150, 1.0, .30)
    return b


def chop(t, period, x0, step, nmax):
    """Рубка: нож опирается КОНЦОМ на доску и качается, как в руке.

    Возвращает (угол, x ножа, сколько кусков отрезано, фаза). Куски отделяются
    РОВНО в тот момент, когда лезвие дошло до доски, а между ударами нож
    переезжает к следующей линии — поэтому видно, что режется сам предмет, а
    не что куски появляются рядом сами по себе.
    """
    p = (t/period) % 1.0
    n = min(nmax, max(0, int(t/period - 0.32) + 1) if t >= 0.32*period else 0)
    down = p < 0.32
    ang = (-26.0*(1.0 - A2.ease(p/0.32)) if down
           else -26.0*A2.ease((p - 0.32)/0.68))
    base = x0 + step*n
    kx = base + step if down else base + step*A2.ease((p - 0.32)/0.68)
    if n >= nmax:
        # всё нарезано: нож не прыгает в сторону, а мягко поднимается над
        # последней линией — рывок в один шаг ножа на кадре было видно
        d = t - (nmax - 1 + 0.32)*period
        ang = -16.0*A2.ease(min(1.0, max(0.0, d)/0.5))
        kx = x0 + step*nmax
    return ang, kx, n, p


def _cut_face(x, y, ry=22, col="#fbf6e6"):
    """Свежий срез на остатке: без него предмет выглядит просто обрезанным."""
    return f'<ellipse cx="{x}" cy="{y}" rx="7" ry="{ry}" fill="{col}"{ST(5)}/>'


def _clip(cid, x, w=640, y=-260, h=440):
    return (f'<defs><clipPath id="{cid}">'
            f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}"/></clipPath></defs>')


def _drop(t, tcut, h=14):
    """Кусок отваливается: короткое падение с затуханием, без отскока."""
    d = max(0.0, t - tcut)
    return -h*max(0.0, 1.0 - A2.ease(min(1.0, d/0.22)))


# ----------------------------------------------------------------- сцены
def sc_r_kart(t, dur=8.0):
    """Шаг 1: картошку кубиком. Нож рубит картошку, ломтики отваливаются,
    остаток убывает; в конце ломтики на том же месте рубятся в кубик."""
    X0, STEP, NMAX, PER = -92.0, 26.0, 5, 0.74
    ang, kx, n, p = chop(t, PER, X0, STEP, NMAX)
    b = board(236, 36)
    b += _clip("ck", X0 + STEP*n)
    b += (f'<g clip-path="url(#ck)">'
          + potato(38, -22, 44, raw=False) + '</g>')
    if n:
        b += _cut_face(X0 + STEP*n, -22, 26)
    tall = PER*NMAX + 0.32*PER                      # когда нарезано всё
    for i in range(n):
        tc = (i + 1 - 0.68)*PER
        px, py = -188 + i*30, -8 + _drop(t, tc)
        if t > tall + 0.5 + i*0.26:                 # ломтик превратился в кубик
            b += cube(px, py - 2, 15, POTIN)
        else:
            rot = -16 + i*5
            b += (f'<g transform="translate({px},{py:.1f}) rotate({rot})">'
                  f'<ellipse cx="0" cy="0" rx="12" ry="26" fill="{POTIN}"{ST(5)}/>'
                  f'<ellipse cx="-3" cy="0" rx="5" ry="20" fill="#fbf3df" opacity=".7"/></g>')
    if t > tall + 0.4:                              # вторая проходка: рубим ломтики
        a2, kx2, _, _ = chop(t - tall - 0.4, 0.42, -196.0, 0.0, 99)
        b += knife(-150, -6, a2, 150)
    else:
        b += knife(kx, -6, ang, 150)
    return A3.stage(t, dur, g(b, 470, 356, 1.12), bg="roomr", table=396, cloth="#b8463f",
                    shadow=(470, 404, 230, 32, .42), light=(620, 330, 300, .32),
                    dark=("left", .22), z1=112)


def sc_r_luk(t, dur=8.0):
    """Шаг 2: лук. Нож идёт по луковице, полукольца отваливаются одно за другим."""
    X0, STEP, NMAX, PER = -66.0, 23.0, 6, 0.66
    ang, kx, n, p = chop(t, PER, X0, STEP, NMAX)
    b = board(236, 36)
    b += _clip("cl", X0 + STEP*n)
    b += f'<g clip-path="url(#cl)">' + onion_half(52, -8, 54) + '</g>'
    if n:
        b += _cut_face(X0 + STEP*n, -34, 30, "#f7f2e2")
    for i in range(n):
        tc = (i + 1 - 0.68)*PER
        px, py = -186 + i*28, -6 + _drop(t, tc)
        rot = -22 + i*7
        b += (f'<g transform="translate({px},{py:.1f}) rotate({rot})">'
              + onion_slice(0, 0, 23) + '</g>')
    b += knife(kx, -6, ang, 150)
    return A3.stage(t, dur, g(b, 470, 356, 1.12), bg="roomb", table=396, cloth="#a8512c",
                    shadow=(470, 404, 230, 32, .42), light=(330, 330, 300, .32),
                    dark=("right", .20), z1=112, x0=12, x1=-10)


def sc_r_mork(t, dur=8.0):
    """Шаг 3: морковь. Нож отрубает кружок за кружком, морковка укорачивается."""
    X0, STEP, NMAX, PER = -74.0, 21.0, 7, 0.60
    ang, kx, n, p = chop(t, PER, X0, STEP, NMAX)
    b = board(236, 36)
    b += _clip("cm", X0 + STEP*n)
    b += f'<g clip-path="url(#cm)">' + carrot(66, -18, 190, 26, 0) + '</g>'
    if n:
        b += _cut_face(X0 + STEP*n, -18, 22, "#f4a24a")
    for i in range(n):
        tc = (i + 1 - 0.68)*PER
        px, py = -190 + i*27, -6 + _drop(t, tc)
        b += carrot_round(px, py, 14)
    b += knife(kx, -6, ang, 150)
    return A3.stage(t, dur, g(b, 470, 356, 1.12), bg="roomc", table=396, cloth="#b8463f",
                    shadow=(470, 404, 230, 32, .42), light=(560, 330, 300, .32),
                    dark=("left", .20), z1=112)


def sc_r_yaytsa(t, dur=8.0):
    """Шаг 4: яйца отварить. Вода кипит, пар идёт, рядом уже разрезанное."""
    b = f'<ellipse cx="0" cy="26" rx="150" ry="30" fill="#000000" opacity=".28"/>'
    b += pot(t, 100, 88)
    b += (f'<g transform="translate(212,6)">' + board(92, 20) +
          egg(-32, -14, 18, half=True) + egg(16, -10, 18, half=True) + '</g>')
    return A3.stage(t, dur, g(b, 440, 338, 1.04), bg="roomr", table=392, cloth="#b8463f",
                    light=(430, 300, 320, .34), dark=("left", .20), z1=116)


def sc_r_tazik(t, dur=8.0):
    """Финал: всё сошлось в тазу. Рисунок таза — тот же, что в ролике про стол."""
    return A3.sc_tazik(t, dur)


def sc_r_stol(t, dur=8.0):
    """Общий кадр: всё, из чего собираем, лежит на столе."""
    b = board(240, 38)
    b += potato(-150, -16, 32) + potato(-86, -10, 27) + potato(-118, -44, 24)
    b += onion_half(-16, -8, 38)
    b += carrot(72, -18, 100, 23, -12)
    b += egg(170, -24, 21) + egg(206, -14, 20)
    b += knife(-250, -30, -8, 140)
    return A3.stage(t, dur, g(b, 470, 352, 1.06), bg="roomc", table=392, cloth="#b8463f",
                    shadow=(470, 400, 236, 34, .40), light=(470, 330, 320, .32),
                    dark=("left", .20), z1=118)


SCENES = {n[3:]: f for n, f in list(globals().items()) if n.startswith("sc_")}
for _n, _f in list(SCENES.items()):
    for _m in A3.MOVES:
        SCENES[f"{_n}@{_m}"] = A3._variant(_f, _m)
NO_GLARE = set()
