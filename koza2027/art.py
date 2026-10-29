# -*- coding: utf-8 -*-
"""Рисунки ролика «Год козы 2027». Каждая сцена — функция времени,
поэтому кадр живой, а зум идёт вектором и не дёргается."""
import anim as A

W, H = 960, 540
SERIF, SANS = "DejaVu Serif", "DejaVu Sans"

DEFS = """
<defs>
<radialGradient id="room" cx="56%" cy="40%"><stop offset="0" stop-color="#5a3a1e"/><stop offset=".55" stop-color="#301c0e"/><stop offset="1" stop-color="#140d07"/></radialGradient>
<radialGradient id="roomc" cx="46%" cy="44%"><stop offset="0" stop-color="#5e4524"/><stop offset=".6" stop-color="#32210f"/><stop offset="1" stop-color="#150e07"/></radialGradient>
<radialGradient id="roomr" cx="50%" cy="42%"><stop offset="0" stop-color="#5d2418"/><stop offset=".6" stop-color="#2e130c"/><stop offset="1" stop-color="#150806"/></radialGradient>
<radialGradient id="roomb" cx="50%" cy="46%"><stop offset="0" stop-color="#3a3524"/><stop offset=".6" stop-color="#211a10"/><stop offset="1" stop-color="#110c07"/></radialGradient>
<linearGradient id="fl1" x1="0" y1="1" x2=".2" y2="0"><stop offset="0" stop-color="#b8320f"/><stop offset=".55" stop-color="#e8701b"/><stop offset="1" stop-color="#f7b740"/></linearGradient>
<linearGradient id="fl2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#8f2408"/><stop offset="1" stop-color="#d9601a"/></linearGradient>
<linearGradient id="cloth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b03c2d"/><stop offset="1" stop-color="#5e1c14"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2b48"/><stop offset="1" stop-color="#2d4064"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfe6f2" stop-opacity=".75"/><stop offset=".45" stop-color="#eaf5fb" stop-opacity=".35"/><stop offset="1" stop-color="#b6d4e4" stop-opacity=".7"/></linearGradient>
<linearGradient id="duck" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#c06a1e"/><stop offset=".5" stop-color="#9c4a12"/><stop offset="1" stop-color="#6d300b"/></linearGradient>
<radialGradient id="candle"><stop offset="0" stop-color="#ffd27a" stop-opacity=".85"/><stop offset="1" stop-color="#ffb43c" stop-opacity="0"/></radialGradient>
<radialGradient id="sepia" cx="50%" cy="44%"><stop offset="0" stop-color="#6b5736"/><stop offset=".6" stop-color="#3a2d1a"/><stop offset="1" stop-color="#1a140c"/></radialGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8702f"/><stop offset="1" stop-color="#6b4320"/></linearGradient>
<radialGradient id="vign" cx="50%" cy="48%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>
</defs>
"""

# ---------------- кирпичики ----------------

def window(x, y, w, h, t=0.0, frost=True):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="url(#night)" stroke="#120b06" stroke-width="9"/>'
    s += f'<path d="M{x+w/2} {y} L{x+w/2} {y+h} M{x} {y+h/2} L{x+w} {y+h/2}" stroke="#120b06" stroke-width="7"/>'
    import random
    r = random.Random(int(x) * 31 + int(y))
    s += '<g fill="#e8f2fb" opacity=".75">'
    for i in range(7):
        px, p0, spd, ph, rr = r.uniform(.06, .94), r.uniform(0, 1), r.uniform(.05, .12), r.uniform(0, 1), r.uniform(2.4, 4.4)
        p = (p0 + t * spd) % 1.0
        s += f'<circle cx="{x + w*px + 9*A.w(t, 4.6, ph):.0f}" cy="{y + h*p:.0f}" r="{rr:.1f}"/>'
    s += '</g>'
    if frost:
        s += (f'<path d="M{x+4} {y+h*0.9} C{x+w*0.2} {y+h*0.82} {x+w*0.36} {y+h*0.88} {x+w*0.56} {y+h*0.8}'
              f' C{x+w*0.74} {y+h*0.72} {x+w*0.9} {y+h*0.8} {x+w-4} {y+h*0.74} L{x+w-4} {y+h} L{x+4} {y+h} Z"'
              ' fill="#eef5fb" opacity=".3"/>')
    return s


def tinsel(y=24):
    return (f'<path d="M0 {y-2} Q120 {y+38} 240 {y} Q360 {y-38} 480 {y} Q600 {y+38} 720 {y}'
            f' Q840 {y-38} 960 {y}" stroke="#c9922f" stroke-width="10" fill="none" opacity=".8"/>')


def table(y=452, top="#c6523a"):
    return (f'<path d="M0 {y} L960 {y} L960 540 L0 540 Z" fill="url(#cloth)"/>'
            f'<path d="M0 {y-8} L960 {y-8} L960 {y+12} L0 {y+12} Z" fill="{top}"/>')


def tree(cx, base, t=0.0, scale=1.0, opacity=1.0, star=True):
    """Ёлка: игрушки, звезда, МИГАЮЩАЯ гирлянда."""
    s = f'<g opacity="{opacity}" transform="translate({cx},{base}) scale({scale})">'
    s += '<g stroke="#10180c" stroke-width="7" stroke-linejoin="round">'
    s += '<rect x="-15" y="-6" width="30" height="44" fill="#6b3f1c"/>'
    s += ('<path d="M0 -318 L85 -204 L45 -204 L115 -100 L67 -100 L147 0 L-147 0'
          ' L-67 -100 L-115 -100 L-45 -204 L-85 -204 Z" fill="#2f5c2a"/></g>')
    s += ('<path d="M0 -292 L61 -208 L29 -208 L89 -110 L51 -110 L121 -6 L0 -6 Z"'
          ' fill="#3b7334" opacity=".85"/>')
    s += '<g stroke="#10180c" stroke-width="5">'
    for tx, ty, r, c in ((-29, -188, 15, "#d6202f"), (35, -164, 13, "#c9922f"),
                         (-61, -110, 14, "#e07f23"), (71, -80, 15, "#d6202f"),
                         (-1, -58, 13, "#efb07a"), (-77, -32, 14, "#c9922f"),
                         (93, -24, 13, "#d6202f"), (23, -236, 12, "#c9922f")):
        s += f'<circle cx="{tx}" cy="{ty}" r="{r}" fill="{c}"/>'
        s += f'<circle cx="{tx-r*0.35:.0f}" cy="{ty-r*0.4:.0f}" r="{r*0.26:.1f}" fill="#fff" opacity=".55"/>'
    s += '</g>'
    s += ('<path d="M-77 -210 Q0 -178 79 -204 M-101 -128 Q0 -92 103 -122 M-123 -46 Q0 -10 125 -38"'
          ' stroke="#8a6a3a" stroke-width="4" fill="none"/>')
    s += A.lights([(-55, -196, "#ffd45e"), (0, -186, "#7fd0ff"), (55, -196, "#ff8c6b"),
                   (-73, -112, "#9ae06a"), (0, -100, "#ffd45e"), (75, -110, "#ff8c6b"),
                   (-91, -30, "#7fd0ff"), (0, -18, "#ffd45e"), (97, -28, "#9ae06a")], t)
    if star:
        g = .72 + .28 * A.w(t, 2.7)
        s += (f'<circle cx="0" cy="-306" r="54" fill="#ffd45e" opacity="{g*0.22:.2f}"/>'
              '<path d="M0 -356 L14 -320 L53 -318 L23 -293 L33 -255 L0 -277 L-33 -255'
              ' L-23 -293 L-53 -318 L-14 -320 Z" fill="#f6c84e" stroke="#10180c" stroke-width="6" stroke-linejoin="round"/>')
    return s + '</g>'


def herbs_glass(x, y, w=40, h=56):
    s = (f'<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="url(#glass)"/></g>')
    cx = x + w / 2
    s += ('<g stroke="#4e7a35" stroke-width="6" fill="none" stroke-linecap="round">'
          f'<path d="M{cx} {y} L{cx-4} {y-52}"/><path d="M{cx-4} {y-36} C{cx-22} {y-46} {cx-28} {y-66} {cx-24} {y-82}"/>'
          f'<path d="M{cx-4} {y-22} C{cx+18} {y-32} {cx+26} {y-52} {cx+22} {y-68}"/></g>')
    return s


def _eyes(x1, x2, y, t, r=6, ph=0.0, per=4.3, look=0.0):
    """Пара глаз с морганием и лёгким поворотом зрачка."""
    if A.blink(t, per, ph):
        return (f'<path d="M{x1-r*1.5} {y} C{x1-r*0.5} {y+r} {x1+r*0.5} {y+r} {x1+r*1.5} {y}"'
                f' stroke="#241208" stroke-width="{r*0.9:.1f}" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x2-r*1.5} {y} C{x2-r*0.5} {y+r} {x2+r*0.5} {y+r} {x2+r*1.5} {y}"'
                f' stroke="#241208" stroke-width="{r*0.9:.1f}" fill="none" stroke-linecap="round"/>')
    d = look * r * 0.5
    return (f'<circle cx="{x1+d:.1f}" cy="{y}" r="{r}" fill="#241208"/>'
            f'<circle cx="{x2+d:.1f}" cy="{y}" r="{r}" fill="#241208"/>'
            f'<circle cx="{x1+d-r*0.3:.1f}" cy="{y-r*0.35:.1f}" r="{r*0.3:.1f}" fill="#fff" opacity=".7"/>'
            f'<circle cx="{x2+d-r*0.3:.1f}" cy="{y-r*0.35:.1f}" r="{r*0.3:.1f}" fill="#fff" opacity=".7"/>')


# ---------------- КОЗА (принята пользователем, геометрию не меняем) ----------------

def _koza_head(t, fire=True, force_closed=False, blink_ph=0.0):
    s = ""
    if fire:
        p = 1 + .035 * A.w(t, 1.9)
        q = 1 + .05 * A.w(t, 1.3, .4)
        s += f'<g transform="translate(596,236) scale({p:.3f},{q:.3f}) translate(-596,-236)">'
        s += '<g stroke="#2a1105" stroke-width="7" stroke-linejoin="round">'
        s += '<path d="M596 236 C640 150 622 88 568 44 C646 68 706 124 710 206 C713 272 678 318 626 332 Z" fill="url(#fl2)"/>'
        s += '<path d="M664 286 C726 228 732 170 708 118 C780 166 806 240 778 306 C760 348 716 368 678 358 Z" fill="url(#fl1)"/>'
        s += '<path d="M548 206 C572 134 556 78 512 42 C578 52 626 110 620 184 C616 230 592 262 562 270 Z" fill="url(#fl1)"/>'
        s += '<path d="M726 356 C772 330 792 290 786 246 C832 288 836 348 800 384 C778 406 748 410 730 398 Z" fill="url(#fl2)"/></g></g>'
        for i, (x, y, r, per) in enumerate(((820, 128, 6, 3.1), (866, 188, 4, 2.4), (782, 80, 4.5, 3.7),
                                            (890, 300, 3.6, 2.8), (748, 38, 3, 4.1))):
            yy = y - 26 * ((t / per + i * .2) % 1.0)
            o = .9 * (1 - ((t / per + i * .2) % 1.0))
            s += f'<circle cx="{x + 10*A.w(t, per*1.4, i*.3):.0f}" cy="{yy:.0f}" r="{r}" fill="#ffd36e" opacity="{o:.2f}"/>'
    s += ('<path d="M498 196 C478 140 500 90 556 62 C588 46 616 56 620 78 C600 66 578 74 560 88'
          ' C518 122 504 158 512 202 Z" fill="#6d4a28" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>'
          '<g stroke="#4a3018" stroke-width="5" fill="none" opacity=".8">'
          '<path d="M516 170 C532 158 548 148 562 142 M524 142 C540 128 556 118 570 112 M536 116 C552 102 570 94 584 90"/></g>')
    s += ('<path d="M556 190 C624 198 654 258 646 318 C638 382 602 434 540 452 C484 468 426 458 390 432'
          ' C354 406 350 362 380 316 C416 262 492 182 556 190 Z" fill="#e9c99c" stroke="#2a1105" stroke-width="9" stroke-linejoin="round"/>'
          '<path d="M596 206 C640 226 658 274 648 322 C638 378 606 426 552 448 C580 408 596 360 596 310'
          ' C596 262 586 228 596 206 Z" fill="#c8a173" opacity=".55"/>'
          '<path d="M372 302 C404 286 446 296 462 332 C478 370 456 406 414 412 C372 418 340 394 338 358'
          ' C336 328 350 312 372 302 Z" fill="#f6e0bc"/>'
          '<g stroke="#c49b6c" stroke-width="5" fill="none" stroke-linecap="round" opacity=".85">'
          '<path d="M470 236 C486 244 492 258 490 272 M504 254 C520 262 526 276 524 290 M536 276 C552 284 558 298 556 312"/></g>')
    s += ('<path d="M554 188 C534 126 558 72 618 44 C652 28 682 40 686 62 C664 50 640 58 620 74'
          ' C576 110 562 150 570 196 Z" fill="#8e6436" stroke="#2a1105" stroke-width="9" stroke-linejoin="round"/>'
          '<g stroke="#5c3d1c" stroke-width="6" fill="none" opacity=".85">'
          '<path d="M572 166 C590 152 608 142 624 134 M580 136 C598 120 616 110 632 104'
          ' M592 108 C610 94 630 84 646 80 M606 82 C622 68 644 58 660 56"/></g>')
    ear = A.sway(t, 6.3, .2, 1.6)
    s += (f'<g transform="rotate({ear:.2f} 640 272)">'
          '<path d="M636 254 C680 244 722 258 740 284 C720 304 674 306 636 284 Z" fill="#d8ad7c" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>'
          '<path d="M654 268 C684 262 710 270 722 282 C704 290 676 288 654 276 Z" fill="#b4825a"/></g>')
    if force_closed or A.blink(t, 4.1, blink_ph):
        s += '<path d="M512 268 C532 250 572 250 588 268" stroke="#2a1105" stroke-width="12" fill="none" stroke-linecap="round"/>'
    else:
        look = 3 * A.w(t, 7.3, .3)
        s += ('<ellipse cx="548" cy="268" rx="38" ry="25" fill="#f7cb53" stroke="#2a1105" stroke-width="8"/>'
              f'<rect x="{528+look:.1f}" y="260" width="42" height="16" rx="8" fill="#2a1105"/>'
              f'<circle cx="{534+look:.1f}" cy="256" r="7" fill="#fff" opacity=".9"/>'
              '<path d="M512 246 C534 232 570 234 582 248" stroke="#2a1105" stroke-width="7" fill="none" stroke-linecap="round" opacity=".55"/>')
    brow = 4 * A.w(t, 9.1, .6)
    s += (f'<path d="M506 {230+brow:.1f} C534 {212+brow:.1f} 578 {214+brow:.1f} 602 {232+brow:.1f}"'
          ' stroke="#2a1105" stroke-width="15" fill="none" stroke-linecap="round"/>')
    s += '<path d="M364 324 C372 314 388 314 394 326 C388 338 370 338 364 324 Z" fill="#2a1105"/>'
    m = 3 * A.w(t, 6.7, .15)
    s += (f'<path d="M358 368 C382 {384+m:.1f} 414 {384+m:.1f} 436 370" stroke="#2a1105" stroke-width="9"'
          ' fill="none" stroke-linecap="round"/>'
          '<path d="M398 384 L398 398" stroke="#2a1105" stroke-width="7" stroke-linecap="round"/>')
    bd = A.sway(t, 7.9, .5, 1.1)
    s += (f'<g transform="rotate({bd:.2f} 424 452)">'
          '<path d="M424 452 C408 498 416 528 440 540 L392 540 C382 506 394 472 414 454 Z" fill="#e9c99c" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>'
          '<g stroke="#c49b6c" stroke-width="5" fill="none" stroke-linecap="round"><path d="M414 476 L408 520 M428 474 L426 522"/></g></g>')
    s += ('<path d="M540 450 C562 498 594 522 648 540 L330 540 C352 506 404 470 540 450 Z" fill="#cfa473" stroke="#2a1105" stroke-width="9" stroke-linejoin="round"/>'
          '<g stroke="#a67c4e" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M470 486 C478 506 476 524 466 540 M520 472 C532 496 532 518 522 540 M572 476 C588 500 594 520 590 540"/></g>')
    return s


def koza(t):
    s = '<rect width="960" height="540" fill="url(#room)"/>'
    s += window(748, 54, 186, 214, t)
    s += ('<g opacity=".16" stroke="#f0c98a" stroke-width="3" fill="none">'
          '<path d="M70 70 q16 22 0 44 q-16 -22 0 -44 M70 170 q16 22 0 44 q-16 -22 0 -44'
          ' M150 120 q16 22 0 44 q-16 -22 0 -44 M150 220 q16 22 0 44 q-16 -22 0 -44"/></g>')
    s += '<ellipse cx="96" cy="150" rx="150" ry="130" fill="url(#candle)" opacity=".5"/>'
    s += tree(118, 470, t, 0.46, 0.5)
    s += table(470)
    s += '<ellipse cx="860" cy="505" rx="64" ry="15" fill="#e4d4b6" opacity=".45"/>'
    s += A.candle(206, 392, t, 78, 52)
    s += _koza_head(t)
    return s


def koza_fire(t):
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += window(748, 54, 186, 214, t)
    s += tree(118, 470, t, 0.46, 0.4)
    s += table(470)
    s += A.candle(206, 392, t, 78, 62)
    pulse = .3 + .12 * A.w(t, 1.6)
    s += f'<ellipse cx="640" cy="240" rx="340" ry="290" fill="#d9601a" opacity="{pulse:.2f}"/>'
    s += _koza_head(t)
    s += A.confetti(t, 16, seed=11)
    return s


def koza_turn(t):
    s = '<rect width="960" height="540" fill="#241a12"/>'
    s += window(748, 54, 186, 214, t)
    s += tree(118, 470, t, 0.46, 0.3)
    s += table(470, "#8c3a2a")
    s += A.candle(206, 392, t, 78, 30)
    s += '<g transform="translate(960,0) scale(-1,1)">' + _koza_head(t, fire=False, force_closed=True) + '</g>'
    s += '<rect width="960" height="540" fill="#22304a" opacity=".3"/>'
    return s


def koza_eye(t):
    """Только глаз во весь кадр — другой план той же козы."""
    s = '<rect width="960" height="540" fill="#3a2410"/>'
    s += '<rect width="960" height="540" fill="url(#room)" opacity=".8"/>'
    s += '<g transform="translate(-1740,-760) scale(4.0)">'
    s += ('<path d="M556 190 C624 198 654 258 646 318 C638 382 602 434 540 452 C484 468 426 458 390 432'
          ' C354 406 350 362 380 316 C416 262 492 182 556 190 Z" fill="#e9c99c" stroke="#2a1105" stroke-width="9"/>'
          '<path d="M596 206 C640 226 658 274 648 322 C638 378 606 426 552 448 C580 408 596 360 596 310'
          ' C596 262 586 228 596 206 Z" fill="#c8a173" opacity=".55"/>'
          '<g stroke="#c49b6c" stroke-width="5" fill="none" stroke-linecap="round" opacity=".9">'
          '<path d="M470 236 C486 244 492 258 490 272 M504 254 C520 262 526 276 524 290 M460 300 C476 308 482 322 480 336"/></g>')
    if A.blink(t, 3.4, .1):
        s += '<path d="M512 268 C532 248 572 248 588 268" stroke="#2a1105" stroke-width="12" fill="none" stroke-linecap="round"/>'
    else:
        look = 4 * A.w(t, 5.1, .2)
        s += ('<ellipse cx="548" cy="268" rx="38" ry="25" fill="#f7cb53" stroke="#2a1105" stroke-width="8"/>'
              f'<rect x="{528+look:.1f}" y="260" width="42" height="16" rx="8" fill="#2a1105"/>'
              f'<circle cx="{534+look:.1f}" cy="256" r="7" fill="#fff" opacity=".95"/>'
              f'<circle cx="{566+look:.1f}" cy="274" r="3.5" fill="#fff" opacity=".6"/>')
    brow = 4 * A.w(t, 6.3, .4)
    s += (f'<path d="M506 {230+brow:.1f} C534 {210+brow:.1f} 578 {212+brow:.1f} 602 {232+brow:.1f}"'
          ' stroke="#2a1105" stroke-width="16" fill="none" stroke-linecap="round"/></g>')
    s += '<rect width="960" height="540" fill="url(#vign)"/>'
    return s


def koza_shadow(t):
    """Тень козы на стене рядом с ёлкой — её нет в кадре, а она есть."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += ('<g opacity=".2" stroke="#f0c98a" stroke-width="3" fill="none">'
          + "".join(f'<path d="M{60+i*110} {70+(i%2)*90} q16 22 0 44 q-16 -22 0 -44"/>' for i in range(9)) + '</g>')
    w1 = 2.2 * A.w(t, 4.4)
    s += (f'<g opacity=".42" fill="#120b06" transform="translate(470,120) rotate({w1:.2f}) scale(1.35,1.5) translate(-470,-120)">'
          '<path d="M452 86 C520 94 550 154 542 214 C534 278 498 330 436 348 C380 364 322 354 286 328'
          ' C250 302 246 258 276 212 C312 158 388 78 452 86 Z"/>'
          '<path d="M394 92 C374 36 398 -14 458 -42 C492 -58 522 -46 526 -24 C504 -36 480 -28 460 -12'
          ' C416 24 402 64 410 102 Z"/>'
          '<path d="M394 90 C374 34 396 -16 452 -44 C484 -60 512 -50 516 -28 C496 -40 472 -32 454 -16'
          ' C416 18 402 58 410 104 Z" transform="translate(-56,8)"/>'
          '<path d="M532 150 C576 140 618 154 636 180 C616 200 570 202 532 180 Z"/>'
          '<path d="M320 348 C304 394 312 424 336 436 L288 436 C278 402 290 368 310 350 Z"/></g>')
    s += tree(820, 470, t, 0.72, 1.0)
    s += table(470)
    s += A.candle(150, 392, t, 78, 70)
    s += A.confetti(t, 14, seed=5)
    return s


def koza_far(t):
    """Общий план комнаты: коза далеко, у накрытого стола."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(60, 70, 150, 160, t)
    s += tinsel(26)
    s += tree(816, 400, t, 0.62, 1.0)
    s += '<path d="M0 316 L960 316 L960 400 L0 400 Z" fill="#6b4524" opacity=".6"/>'
    s += '<g transform="translate(316,116) scale(0.42)">' + _koza_head(t, blink_ph=.3) + '</g>'
    s += table(400)
    s += ('<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<ellipse cx="300" cy="462" rx="150" ry="34" fill="#e4d4b6"/>'
          '<path d="M216 450 C214 416 252 396 302 396 C352 396 386 414 386 446 C386 460 354 459 306 459 C258 459 230 460 216 450 Z" fill="#9a4a14"/>'
          '<ellipse cx="690" cy="470" rx="110" ry="28" fill="#dccbab"/>'
          '<path d="M640 460 L672 420 L704 460 Z" fill="#f0d98a"/>'
          '<rect x="710" y="436" width="40" height="24" rx="4" fill="#f6edd2"/></g>')
    s += herbs_glass(470, 406, 42, 56) + herbs_glass(538, 414, 38, 50)
    s += A.candle(600, 340, t, 58, 44)
    s += A.confetti(t, 18, seed=3)
    return s


def koza_table(t):
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(42, 48, 180, 190, t)
    s += tinsel(24)
    s += tree(820, 404, t, 0.62, 0.95)
    s += '<path d="M0 330 L960 330 L960 540 L0 540 Z" fill="url(#cloth)"/>'
    s += '<path d="M0 322 L960 322 L960 344 L0 344 Z" fill="#c6523a"/>'
    s += '<g transform="translate(222,-74) scale(0.56)">' + _koza_head(t, blink_ph=.55) + '</g>'
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<ellipse cx="236" cy="452" rx="150" ry="36" fill="#e4d4b6"/>'
          '<path d="M150 440 C148 404 188 382 240 382 C292 382 326 402 326 436 C326 452 294 450 244 450 C196 450 166 452 150 440 Z" fill="#9a4a14"/>'
          '<circle cx="160" cy="452" r="14" fill="#f0921f"/><circle cx="316" cy="450" r="14" fill="#f0921f"/>'
          '<ellipse cx="760" cy="466" rx="120" ry="30" fill="#dccbab"/>'
          '<path d="M706 456 L742 414 L778 456 Z" fill="#f0d98a"/>'
          '<rect x="782" y="430" width="44" height="26" rx="4" fill="#f6edd2"/></g>')
    s += A.smoke(236, 382, t, 3, 150, 1.0, .26)
    s += herbs_glass(452, 400, 44, 60) + herbs_glass(528, 408, 40, 54)
    s += A.candle(640, 330, t, 62, 46)
    return s


# ---------------- ПЕРЕРИСОВАНО: звери в профиль, узнаваемые ----------------

def _legs(x0, t, ph, n=4, top=44, bot=118, col="#e9c99c", wd=15):
    """Ноги с копытами, чуть переступают."""
    out = ""
    for i, lx in enumerate((-56, -27, 26, 55)[:n]):
        a = 2.6 * A.w(t, 3.4 + i * .4, ph + i * .22)
        out += (f'<g transform="rotate({a:.2f} {x0+lx} {top})">'
                f'<rect x="{x0+lx-wd/2:.0f}" y="{top}" width="{wd}" height="{bot-top}" rx="5"'
                f' fill="{col}" stroke="#2a1105" stroke-width="6"/>'
                f'<rect x="{x0+lx-wd/2-2:.0f}" y="{bot-12}" width="{wd+4}" height="14" rx="4"'
                ' fill="#4a3018" stroke="#2a1105" stroke-width="5"/></g>')
    return out


def _cloud(rx, ry, n=13, bulge=1.30, cy=0.0):
    """Замкнутый контур «барашком»: ровная дуга наружу между точками эллипса."""
    import math
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        pts.append((rx * math.cos(a), cy + ry * math.sin(a)))
    d = "M%.1f %.1f " % pts[0]
    for i in range(n):
        x2, y2 = pts[(i + 1) % n]
        x1, y1 = pts[i]
        r = math.hypot(x2 - x1, y2 - y1) * bulge / 2
        d += "A%.1f %.1f 0 0 1 %.1f %.1f " % (r, r, x2, y2)
    return d + "Z"


def _legs(t, ph, col, dark, top=52, bot=136, wd=22):
    back = f'<g opacity=".75">'
    front = "<g>"
    for i, lx in enumerate((-50, 44, -22, 72)):
        a = 2.4 * A.w(t, 3.6 + i * .37, ph + i * .26)
        g = (f'<g transform="rotate({a:.2f} {lx} {top})">'
             f'<rect x="{lx-wd/2:.0f}" y="{top}" width="{wd}" height="{bot-top}" rx="6"'
             f' fill="{dark if i < 2 else col}" stroke="#2a1105" stroke-width="7"/>'
             f'<rect x="{lx-wd/2-3:.0f}" y="{bot-14}" width="{wd+6}" height="16" rx="5"'
             ' fill="#4a3018" stroke="#2a1105" stroke-width="6"/></g>')
        if i < 2:
            back += g
        else:
            front += g
    return back + "</g>", front + "</g>"


def _goat_side(x, y, t, ph=0.0):
    c, dark, horn1, horn2 = "#e9c99c", "#c9a071", "#8e6436", "#6d4a28"
    back, front = _legs(t, ph, c, dark)
    s = f'<g transform="translate({x},{y})">'
    s += '<ellipse cx="6" cy="128" rx="128" ry="18" fill="#120b06" opacity=".3"/>'
    s += back
    s += f'<ellipse cx="0" cy="0" rx="104" ry="58" fill="{c}" stroke="#2a1105" stroke-width="8"/>'
    s += f'<path d="M-44 -50 C14 -64 76 -46 100 -10 C72 16 -14 20 -52 -4 Z" fill="{dark}" opacity=".4"/>'
    s += (f'<path d="M98 -30 C128 -48 146 -26 138 4 C132 28 114 34 104 22 Z"'
          f' fill="{c}" stroke="#2a1105" stroke-width="7"/>')
    s += front
    # шея
    s += (f'<path d="M-66 -40 C-92 -72 -120 -96 -146 -110 L-112 -150 C-82 -128 -58 -92 -48 -54 Z"'
          f' fill="{c}" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>')
    hn = A.sway(t, 5.6, ph, 1.5)
    s += f'<g transform="rotate({hn:.2f} -120 -120) translate(-120,-120) scale(0.80) translate(150,150)">'
    # рога — длинные, назад и вверх
    s += (f'<path d="M-148 -174 C-120 -216 -58 -232 18 -214 C24 -196 -22 -188 -66 -176'
          f' C-104 -166 -132 -158 -140 -150 Z" fill="{horn2}" stroke="#2a1105" stroke-width="7" stroke-linejoin="round"/>'
          f'<path d="M-166 -156 C-136 -200 -74 -218 4 -200 C10 -182 -36 -172 -82 -160'
          f' C-120 -150 -148 -140 -158 -132 Z" fill="{horn1}" stroke="#2a1105" stroke-width="7" stroke-linejoin="round"/>'
          '<g stroke="#5c3d1c" stroke-width="5" fill="none" opacity=".85">'
          '<path d="M-120 -176 C-114 -164 -112 -156 -114 -148 M-80 -186 C-74 -174 -72 -164 -74 -156'
          ' M-40 -194 C-34 -182 -32 -172 -34 -164"/></g>')
    # голова: клин с вытянутой мордой влево
    s += (f'<path d="M-146 -182 C-104 -180 -84 -152 -88 -122 C-92 -92 -116 -70 -156 -62'
          f' C-196 -54 -228 -62 -240 -82 C-250 -100 -238 -120 -210 -138 C-184 -156 -168 -182 -146 -182 Z"'
          f' fill="{c}" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>')
    s += f'<path d="M-200 -76 C-226 -72 -244 -80 -246 -92 C-228 -102 -204 -98 -192 -88 Z" fill="#f6e0bc"/>'
    # ухо
    ea = A.sway(t, 4.9, ph + .3, 3.0)
    s += (f'<g transform="rotate({ea:.2f} -104 -140)">'
          f'<path d="M-104 -146 C-72 -158 -44 -150 -36 -132 C-54 -118 -86 -120 -102 -132 Z"'
          f' fill="{dark}" stroke="#2a1105" stroke-width="7" stroke-linejoin="round"/></g>')
    # бородка
    bd = A.sway(t, 7.2, ph + .5, 2.2)
    s += (f'<g transform="rotate({bd:.2f} -200 -62)">'
          f'<path d="M-212 -64 C-226 -34 -222 -8 -206 2 C-212 -22 -210 -44 -200 -60 Z"'
          f' fill="{c}" stroke="#2a1105" stroke-width="7" stroke-linejoin="round"/></g>')
    if A.blink(t, 4.6, ph):
        s += '<path d="M-176 -126 C-166 -134 -148 -134 -140 -126" stroke="#2a1105" stroke-width="7" fill="none" stroke-linecap="round"/>'
    else:
        s += ('<ellipse cx="-158" cy="-128" rx="20" ry="15" fill="#f7cb53" stroke="#2a1105" stroke-width="6"/>'
              '<ellipse cx="-160" cy="-127" rx="10" ry="12" fill="#2a1105"/>'
              '<circle cx="-164" cy="-132" r="4" fill="#fff" opacity=".9"/>')
    s += '<path d="M-242 -92 C-236 -99 -226 -99 -222 -92 C-226 -85 -236 -85 -242 -92 Z" fill="#2a1105"/>'
    s += '<path d="M-238 -74 C-226 -68 -210 -68 -200 -74" stroke="#2a1105" stroke-width="6" fill="none" stroke-linecap="round"/>'
    return s + '</g></g>'


def _sheep_side(x, y, t, ph=0.0, ram=False):
    wool, face, dark = "#f6f1e6", "#d9c3a0", "#c0a67f"
    back, front = _legs(t, ph, face, dark)
    s = f'<g transform="translate({x},{y})">'
    s += '<ellipse cx="6" cy="128" rx="128" ry="18" fill="#120b06" opacity=".3"/>'
    s += back
    s += (f'<path d="{_cloud(104, 58, 13, 1.34)}" fill="{wool}"'
          ' stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>')
    s += f'<path d="{_cloud(78, 40, 11, 1.3, 8)}" fill="#e9e2d2" opacity=".5"/>'
    s += f'<circle cx="112" cy="-6" r="24" fill="{wool}" stroke="#2a1105" stroke-width="7"/>'
    s += front
    s += (f'<path d="M-62 -44 C-88 -74 -116 -96 -142 -108 L-108 -148 C-80 -126 -56 -92 -46 -56 Z"'
          f' fill="{face}" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>')
    hn = A.sway(t, 6.1, ph, 1.3)
    s += f'<g transform="rotate({hn:.2f} -120 -116) translate(-120,-116) scale(0.80) translate(150,145)">'
    s += (f'<path d="M-142 -176 C-100 -174 -80 -146 -84 -118 C-88 -90 -112 -70 -150 -64'
          f' C-190 -58 -222 -66 -232 -86 C-242 -104 -228 -124 -202 -140 C-178 -156 -164 -176 -142 -176 Z"'
          f' fill="{face}" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>')
    if not ram:
        s += (f'<path d="{_cloud(46, 24, 7, 1.4)}" transform="translate(-126,-168)" fill="{wool}"'
              ' stroke="#2a1105" stroke-width="7" stroke-linejoin="round"/>')
    ea = A.sway(t, 4.4, ph + .4, 4.0)
    s += (f'<g transform="rotate({ea:.2f} -106 -134)">'
          f'<path d="M-106 -138 C-74 -144 -44 -124 -38 -96 C-60 -92 -90 -110 -104 -126 Z"'
          f' fill="{dark}" stroke="#2a1105" stroke-width="7" stroke-linejoin="round"/></g>')
    if ram:
        s += ('<path d="M-118 -150 C-62 -168 -14 -138 -18 -92 C-22 -46 -68 -22 -118 -30'
              ' C-86 -46 -68 -70 -72 -98 C-76 -126 -94 -144 -118 -150 Z"'
              ' fill="#9c7a4a" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>'
              '<path d="M-110 -138 C-66 -150 -34 -124 -36 -92 C-38 -62 -66 -42 -104 -40"'
              ' stroke="#6e5230" stroke-width="6" fill="none"/>'
              '<path d="M-98 -122 C-70 -130 -52 -112 -54 -90" stroke="#6e5230" stroke-width="5" fill="none"/>')
    s += f'<path d="M-192 -78 C-218 -74 -236 -82 -238 -94 C-220 -104 -196 -100 -184 -90 Z" fill="#efe4d0"/>'
    if A.blink(t, 5.2, ph + .3):
        s += '<path d="M-172 -122 C-162 -130 -144 -130 -136 -122" stroke="#2a1105" stroke-width="7" fill="none" stroke-linecap="round"/>'
    else:
        s += ('<ellipse cx="-154" cy="-124" rx="16" ry="14" fill="#2e1c0c" stroke="#2a1105" stroke-width="5"/>'
              '<circle cx="-159" cy="-128" r="4.4" fill="#fff" opacity=".8"/>')
    s += '<path d="M-234 -94 C-228 -101 -218 -101 -214 -94 C-218 -87 -228 -87 -234 -94 Z" fill="#2a1105"/>'
    s += '<path d="M-230 -76 C-218 -70 -202 -70 -192 -76" stroke="#2a1105" stroke-width="6" fill="none" stroke-linecap="round"/>'
    return s + '</g></g>'


def three_animals(t):
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += tinsel(22)
    s += tree(876, 440, t, 0.42, 0.45)
    s += '<path d="M0 452 L960 452 L960 540 L0 540 Z" fill="#4a3620"/>'
    s += '<path d="M0 446 L960 446 L960 460 L0 460 Z" fill="#6b4f2c"/>'
    s += ('<g opacity=".3"><ellipse cx="250" cy="462" rx="120" ry="16" fill="#120b06"/>'
          '<ellipse cx="540" cy="462" rx="120" ry="16" fill="#120b06"/>'
          '<ellipse cx="820" cy="462" rx="120" ry="16" fill="#120b06"/></g>')
    s += '<g transform="translate(0,34) scale(0.82) translate(0,-34)">'
    s += _goat_side(268, 326, t, 0.0)
    s += _sheep_side(600, 326, t, 0.35, ram=False)
    s += _sheep_side(930, 326, t, 0.7, ram=True)
    s += '</g>' 
    s += A.confetti(t, 14, seed=9, top=0, bot=460)
    return s


# ---------------- ПЕРЕРИСОВАНО: художник, музыкант, мастер ----------------

def _person(x, y, t, s, coat, skin, hair, ph=0.0, beard=None):
    """Фигура по пояс, 3/4. Возвращает голову и торс, руки рисуются снаружи."""
    g = A.sway(t, 5.8, ph, .8)
    out = f'<g transform="translate({x},{y}) scale({s}) rotate({g:.2f} 0 60)">'
    out += (f'<path d="M-96 170 C-92 92 -50 56 0 56 C50 56 92 92 96 170 Z" fill="{coat}"'
            ' stroke="#1b1309" stroke-width="8" stroke-linejoin="round"/>')
    out += f'<path d="M-24 58 L24 58 L24 14 L-24 14 Z" fill="{skin}" stroke="#1b1309" stroke-width="8"/>'
    out += f'<ellipse cx="0" cy="-34" rx="56" ry="62" fill="{skin}" stroke="#1b1309" stroke-width="8"/>'
    out += (f'<path d="M-56 -40 C-58 -94 -32 -118 0 -118 C34 -118 58 -94 56 -44'
            f' C40 -74 -38 -74 -56 -40 Z" fill="{hair}" stroke="#1b1309" stroke-width="8" stroke-linejoin="round"/>')
    out += _eyes(-19, 19, -32, t, 7, ph)
    out += (f'<path d="M-3 -24 C4 -14 3 -6 -6 -4" stroke="#1b1309" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<path d="M-18 8 C-8 18 10 18 20 6" stroke="#1b1309" stroke-width="7" fill="none" stroke-linecap="round"/>')
    if beard:
        out += (f'<path d="M-40 -12 C-36 34 -18 52 0 56 C18 52 36 34 40 -12 C24 14 -24 14 -40 -12 Z"'
                f' fill="{beard}" stroke="#1b1309" stroke-width="7" stroke-linejoin="round"/>')
    return out + '</g>'


def makers(t):
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += tinsel(20)
    s += tree(898, 430, t, 0.36, 0.4)
    s += '<path d="M0 448 L960 448 L960 540 L0 540 Z" fill="#4a3620"/>'
    s += '<path d="M0 442 L960 442 L960 456 L0 456 Z" fill="#6b4f2c"/>'

    # ХУДОЖНИК: мольберт, холст с картиной, кисть поднята, палитра
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M64 448 L128 212 M232 448 L168 212 M86 360 L210 360" stroke="#8a5c2a" fill="none"/>'
          '<rect x="58" y="150" width="180" height="150" rx="5" fill="#f4eede"/></g>')
    s += ('<g stroke="#1b1309" stroke-width="5">'
          '<path d="M74 282 L120 206 L166 282 Z" fill="#3f7a38"/>'
          '<circle cx="196" cy="188" r="20" fill="#f0c33c"/>'
          '<path d="M58 282 L238 282 L238 300 L58 300 Z" fill="#9a7b4a"/></g>')
    s += _person(214, 312, t, 0.78, "#9c5a3c", "#eec194", "#5e3718", .1)
    hand = 7 * A.w(t, 2.3, .1)
    s += (f'<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          f'<path d="M180 364 C150 356 128 {330+hand:.0f} 126 {300+hand:.0f} C126 {288+hand:.0f} 142 {286+hand:.0f} 146 {298+hand:.0f}'
          f' C150 {316+hand:.0f} 164 332 188 338 Z" fill="#eec194"/>'
          f'<path d="M132 {300+hand:.0f} L116 {262+hand:.0f}" stroke="#8a5c2a" stroke-width="9"/>'
          f'<path d="M116 {262+hand:.0f} L110 {248+hand:.0f}" stroke="#c0203a" stroke-width="11"/></g>')
    s += ('<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
          '<path d="M248 392 C280 380 310 392 312 414 C314 436 286 448 258 440 C236 434 230 400 248 392 Z" fill="#c2914f"/></g>'
          '<g><circle cx="262" cy="406" r="7" fill="#c0203a"/><circle cx="286" cy="402" r="7" fill="#2f6fb0"/>'
          '<circle cx="298" cy="422" r="7" fill="#f0c33c"/><circle cx="270" cy="428" r="7" fill="#3f7a38"/></g>')

    # МУЗЫКАНТ: скрипка у подбородка, смычок ходит
    s += _person(500, 300, t, 0.84, "#53647a", "#e5b184", "#3e2a18", .45)
    s += ('<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round" transform="translate(-26,58) rotate(-26 470 300)">'
          '<path d="M424 278 C396 278 382 300 386 322 C390 346 410 358 434 354 C436 372 472 372 474 354'
          ' C498 358 518 346 522 322 C526 300 512 278 484 278 C478 258 430 258 424 278 Z" fill="#9c4a1e"/>'
          '<path d="M452 262 L452 232" stroke="#6b3214" stroke-width="13"/>'
          '<ellipse cx="454" cy="318" rx="9" ry="22" fill="#4a230c"/></g>')
    bow = 14 * A.w(t, 1.9, .2)
    s += (f'<g transform="rotate(-46 446 392)"><rect x="{352+bow:.0f}" y="386" width="196" height="10" rx="5"'
          ' fill="#c2914f" stroke="#1b1309" stroke-width="6"/></g>')
    s += (f'<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          f'<path d="M548 418 C578 404 596 {380+bow*0.4:.0f} 592 {358+bow*0.4:.0f} C590 346 574 346 570 358'
          f' C566 376 552 392 530 398 Z" fill="#e5b184"/></g>')
    # МАСТЕР: гончарный круг, руки на глине, круг вращается
    s += _person(800, 288, t, 0.80, "#7d8f6a", "#f0c79c", "#4a3a22", .8)
    wob = 3 * A.w(t, 0.6)
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<rect x="690" y="430" width="220" height="18" rx="6" fill="#8a5c2a"/>'
          '<ellipse cx="800" cy="424" rx="104" ry="24" fill="#a9762f"/></g>')
    s += (f'<g transform="rotate({wob:.2f} 800 400)" stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M744 418 C732 380 748 348 774 336 C762 326 764 310 784 305 C806 300 822 312 820 328'
          ' C818 340 810 346 802 346 C832 360 856 384 852 418 Z" fill="#b5651f"/>'
          '<path d="M768 392 C788 384 816 384 834 392" stroke="#7d3f12" stroke-width="6" fill="none"/></g>')
    s += ('<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          '<path d="M726 384 C742 366 764 358 780 362 C786 372 780 384 766 388 C752 392 738 396 730 404 Z" fill="#f0c79c"/>'
          '<path d="M874 384 C858 366 836 358 820 362 C814 372 820 384 834 388 C848 392 862 396 870 404 Z" fill="#f0c79c"/></g>')
    s += A.confetti(t, 12, seed=4, top=0, bot=450)
    return s


# ---------------- ДЕД МОРОЗ ----------------

def _ded(x, y, t, s=1.0, ph=0.0):
    g = A.sway(t, 6.4, ph, .9)
    o = f'<g transform="translate({x},{y}) scale({s}) rotate({g:.2f} 0 180)">'
    o += '<g stroke="#1b0806" stroke-width="9" stroke-linejoin="round">'
    o += '<path d="M-182 300 C-176 200 -110 136 0 132 C110 136 176 200 182 300 Z" fill="#c22a24"/>'
    o += '<path d="M-182 272 C-110 256 110 256 182 272 L182 300 L-182 300 Z" fill="#f4efe8"/>'
    o += '<path d="M-54 138 C-40 212 -32 260 -36 300 L-98 300 C-98 226 -84 168 -54 138 Z" fill="#f4efe8"/>'
    o += '<path d="M54 138 C40 212 32 260 36 300 L98 300 C98 226 84 168 54 138 Z" fill="#f4efe8"/>'
    o += '<path d="M-118 246 C-60 230 60 230 118 246 L118 276 C60 260 -60 260 -118 276 Z" fill="#8a6a1e"/>'
    o += '<rect x="-26" y="232" width="52" height="46" rx="6" fill="#f6c84e"/>'
    o += '<circle cx="0" cy="22" r="92" fill="#f3c9a0"/>'
    o += '<path d="M-86 28 C-94 116 -56 180 0 196 C56 180 94 116 86 28 C62 78 26 94 0 94 C-26 94 -62 78 -86 28 Z" fill="#f4efe8"/>'
    o += '<path d="M-52 84 C-40 60 40 60 52 84 C42 106 -42 106 -52 84 Z" fill="#e8ddd0"/>'
    o += '<path d="M-66 50 C-42 36 -14 42 -2 58 C10 42 38 36 62 50 C50 76 18 82 -2 72 C-22 82 -54 76 -66 50 Z" fill="#f8f4ee"/>'
    o += '<path d="M-98 -26 C-102 -104 -58 -148 2 -148 C62 -148 104 -104 98 -26 C62 -58 -62 -58 -98 -26 Z" fill="#c22a24"/>'
    o += '<path d="M-106 -44 C-62 -70 64 -70 108 -44 C110 -14 98 2 82 4 C42 -18 -40 -18 -80 4 C-98 2 -108 -14 -106 -44 Z" fill="#f4efe8"/>'
    o += '<circle cx="110" cy="-130" r="26" fill="#f4efe8"/>'
    o += '<path d="M2 -148 C58 -152 98 -132 110 -130 C88 -122 54 -122 30 -128 Z" fill="#a8201c"/>'
    o += '<path d="M182 260 C190 196 166 156 128 148 C102 142 86 158 90 178 C94 200 118 210 136 216 C154 222 172 236 178 260 Z" fill="#c22a24"/>'
    o += '<path d="M150 156 C174 150 196 158 200 174 C192 186 164 188 146 180 Z" fill="#f3c9a0"/></g>'
    o += ('<g stroke="#1b0806" stroke-width="6" stroke-linejoin="round">'
          '<path d="M190 60 L250 60 L240 116 C236 132 204 132 200 116 Z" fill="url(#glass)"/>'
          '<path d="M220 132 L220 172 M196 172 L244 172" stroke="#1b0806" stroke-width="6" stroke-linecap="round"/>'
          '<path d="M196 98 L244 98 L240 116 C236 132 204 132 200 116 Z" fill="#f6c84e" opacity=".85"/></g>')
    for i in range(3):
        p = ((t * .5) + i * .33) % 1.0
        o += (f'<circle cx="{208+i*14}" cy="{104-p*34:.0f}" r="{4-i*0.6:.1f}" fill="#fff6d0"'
              f' opacity="{(1-p)*0.85:.2f}"/>')
    if A.blink(t, 4.9, ph + .2):
        o += ('<path d="M-38 10 C-28 2 -14 2 -6 10" stroke="#1b0806" stroke-width="7" fill="none" stroke-linecap="round"/>'
              '<path d="M6 10 C14 2 28 2 38 10" stroke="#1b0806" stroke-width="7" fill="none" stroke-linecap="round"/>')
    else:
        lk = 3 * A.w(t, 6.9, ph)
        o += (f'<ellipse cx="-34" cy="12" rx="17" ry="19" fill="#fff"/><circle cx="{-31+lk:.1f}" cy="14" r="10" fill="#2f4a6b"/>'
              f'<circle cx="{-35+lk:.1f}" cy="9" r="4" fill="#fff"/>'
              f'<ellipse cx="36" cy="12" rx="17" ry="19" fill="#fff"/><circle cx="{39+lk:.1f}" cy="14" r="10" fill="#2f4a6b"/>'
              f'<circle cx="{35+lk:.1f}" cy="9" r="4" fill="#fff"/>')
    o += ('<path d="M-62 -20 C-46 -34 -14 -34 -2 -22" stroke="#f4efe8" stroke-width="13" fill="none" stroke-linecap="round"/>'
          '<path d="M4 -22 C18 -34 48 -33 64 -19" stroke="#f4efe8" stroke-width="13" fill="none" stroke-linecap="round"/>'
          '<ellipse cx="0" cy="42" rx="20" ry="16" fill="#e4906c"/>'
          '<ellipse cx="-70" cy="44" rx="24" ry="15" fill="#e4906c" opacity=".6"/>'
          '<ellipse cx="70" cy="44" rx="24" ry="15" fill="#e4906c" opacity=".6"/>')
    return o + '</g>'


def ded(t):
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += window(690, 54, 214, 214, t)
    s += tinsel(26)
    s += ('<g stroke="#10180c" stroke-width="6" stroke-linejoin="round">'
          '<path d="M0 108 L96 136 L40 152 L140 186 L72 198 L176 236 L0 236 Z" fill="#2f5c2a"/></g>')
    s += A.lights([(64, 164, "#d6202f"), (118, 206, "#c9922f"), (30, 212, "#7fd0ff")], t)
    s += table(470)
    s += _ded(450, 240, t, 1.0)
    s += A.confetti(t, 20, seed=2)
    return s


# ---------------- ПЕРВЫЙ КАДР: новогодний стол ----------------

def open_newyear(t):
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(40, 58, 176, 186, t)
    s += tinsel(22)
    s += ('<g stroke="#120b06" stroke-width="7"><circle cx="300" cy="96" r="44" fill="#e4d4b6"/>'
          '<circle cx="300" cy="96" r="6" fill="#120b06"/>'
          f'<path d="M300 96 L300 62 M300 96 L{300+20*A.w(t,60):.1f} {96+14*A.w(t,60,.25):.1f}"'
          ' stroke="#120b06" stroke-width="6" stroke-linecap="round"/></g>')
    s += tree(828, 430, t, 0.78, 1.0)
    s += ('<g stroke="#10180c" stroke-width="6" stroke-linejoin="round">'
          '<rect x="700" y="384" width="68" height="46" rx="4" fill="#a8512c"/>'
          '<path d="M734 384 L734 430 M700 404 L768 404" stroke="#f6c84e" stroke-width="8"/>'
          '<rect x="884" y="392" width="58" height="38" rx="4" fill="#4e7a35"/>'
          '<path d="M913 392 L913 430 M884 410 L942 410" stroke="#efb07a" stroke-width="7"/></g>')
    s += _ded(420, 190, t, 0.72)
    s += table(432)
    s += ('<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          '<ellipse cx="208" cy="476" rx="128" ry="30" fill="#e4d4b6"/>'
          '<path d="M134 462 C132 426 170 404 212 404 C256 404 288 424 288 456 C288 470 254 469 214 469 C166 469 150 472 134 462 Z" fill="#9a4a14"/>'
          '<circle cx="146" cy="478" r="13" fill="#f0921f"/><circle cx="278" cy="476" r="13" fill="#f0921f"/>'
          '<ellipse cx="690" cy="492" rx="112" ry="26" fill="#dccbab"/>'
          '<path d="M640 482 L674 440 L708 482 Z" fill="#f0d98a"/>'
          '<rect x="712" y="458" width="42" height="24" rx="4" fill="#f6edd2"/></g>')
    s += A.smoke(208, 404, t, 3, 140, 1.0, .25)
    s += herbs_glass(330, 434, 44, 58) + herbs_glass(398, 442, 38, 50)
    s += A.candle(560, 366, t, 66, 50)
    s += A.candle(606, 380, t, 52, 40, phase=.4, s=.85)
    s += ('<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
          '<path d="M470 470 L516 470 L508 522 C504 536 482 536 478 522 Z" fill="url(#glass)"/>'
          '<path d="M476 496 L510 496 L508 522 C504 536 482 536 478 522 Z" fill="#f6c84e" opacity=".8"/></g>')
    s += A.confetti(t, 30, seed=1)
    s += '<rect width="960" height="540" fill="url(#vign)"/>'
    return s


# ---------------- остальные сцены ----------------

def dish(t):
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += tree(846, 262, t, 0.52, 0.45)
    s += tinsel(18)
    s += table(330)
    s += A.candle(96, 250, t, 78, 56)
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<ellipse cx="480" cy="452" rx="300" ry="64" fill="#cbb79a"/>'
          '<ellipse cx="480" cy="438" rx="262" ry="50" fill="#e8dac0"/>'
          '<path d="M238 424 C238 320 346 258 480 258 C614 258 722 320 722 424 Z" fill="#b9bec4"/>'
          '<path d="M276 404 C280 332 368 288 480 288 C592 288 680 332 684 404 Z" fill="#d6dadf"/>'
          '<path d="M452 258 L508 258 L508 240 C508 226 452 226 452 240 Z" fill="#9aa0a6"/>'
          '<ellipse cx="480" cy="226" rx="34" ry="16" fill="#c2c7cc"/></g>')
    s += '<path d="M318 356 C356 318 426 296 480 296" stroke="#f2f5f8" stroke-width="16" fill="none" stroke-linecap="round" opacity=".55"/>'
    s += A.smoke(690, 250, t, 3, 170, 1.0, .3)
    s += ('<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<path d="M60 470 C64 436 96 414 142 414 C172 414 190 430 186 450 C182 470 158 478 134 480 C106 482 80 494 70 510 Z" fill="#eec194"/>'
          '<path d="M900 476 C896 442 866 420 822 420 C794 420 776 436 780 456 C784 476 806 484 830 486 C856 488 880 500 890 516 Z" fill="#eec194"/></g>')
    s += A.confetti(t, 16, seed=6)
    return s


def table_top(t):
    s = '<rect width="960" height="540" fill="url(#cloth)"/>'
    s += '<g opacity=".22" stroke="#f0c98a" stroke-width="4" fill="none">'
    for i in range(6):
        for j in range(4):
            s += f'<path d="M{70+i*170} {60+j*140} q18 24 0 48 q-18 -24 0 -48"/>'
    s += '</g>'
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<ellipse cx="480" cy="270" rx="170" ry="92" fill="#e8dac0"/>'
          '<path d="M372 252 C370 206 418 178 480 178 C544 178 588 204 588 248 C588 268 552 266 486 266 C416 266 390 262 372 252 Z" fill="#9a4a14"/>'
          '<circle cx="382" cy="300" r="16" fill="#f0921f"/><circle cx="578" cy="296" r="16" fill="#f0921f"/>'
          '<ellipse cx="170" cy="180" rx="96" ry="52" fill="#dccbab"/><ellipse cx="170" cy="176" rx="70" ry="34" fill="#4e7a35"/>'
          '<ellipse cx="790" cy="178" rx="96" ry="52" fill="#dccbab"/>'
          '<path d="M734 168 L774 128 L814 168 Z" fill="#f0d98a"/><rect x="782" y="146" width="48" height="30" rx="4" fill="#f6edd2"/>'
          '<ellipse cx="180" cy="418" rx="100" ry="50" fill="#e8dac0"/>'
          '<path d="M126 404 C122 374 150 354 182 354 C214 354 238 372 236 400 Z" fill="#b8431f"/>'
          '<ellipse cx="790" cy="420" rx="100" ry="50" fill="#e8dac0"/>'
          '<rect x="742" y="382" width="42" height="34" rx="4" fill="#d8a85c"/><rect x="796" y="386" width="42" height="34" rx="4" fill="#d8a85c"/>'
          '<rect x="432" y="430" width="44" height="66" rx="5" fill="url(#glass)"/>'
          '<rect x="492" y="432" width="42" height="62" rx="5" fill="url(#glass)"/></g>')
    s += ('<g stroke="#4e7a35" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M454 430 L450 372"/><path d="M450 388 C428 376 420 354 424 336"/><path d="M450 404 C476 394 488 370 484 350"/>'
          '<path d="M513 432 L509 384"/><path d="M509 398 C490 388 484 368 488 352"/></g>')
    s += A.smoke(480, 178, t, 3, 150, 1.0, .22)
    s += A.candle(312, 60, t, 64, 48) + A.candle(650, 60, t, 64, 48, phase=.5)
    s += '<g fill="#c0203a" stroke="#1b0f07" stroke-width="5"><circle cx="300" cy="448" r="20"/><circle cx="662" cy="452" r="18"/></g>'
    s += A.confetti(t, 22, seed=8)
    return s


def guests(t):
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(24, 40, 168, 186, t)
    s += tree(800, 410, t, 0.9, 1.0)
    s += tinsel(22)
    s += ('<g stroke="#10180c" stroke-width="6" stroke-linejoin="round">'
          '<rect x="648" y="372" width="62" height="42" rx="4" fill="#a8512c"/>'
          '<path d="M679 372 L679 414 M648 390 L710 390" stroke="#f6c84e" stroke-width="7"/></g>')
    s += ('<g stroke="#120b06" stroke-width="7"><circle cx="300" cy="104" r="46" fill="#e4d4b6"/>'
          '<circle cx="300" cy="104" r="6" fill="#120b06"/>'
          f'<path d="M300 104 L300 70 M300 104 L{300+22*A.w(t,60):.1f} {104+16*A.w(t,60,.25):.1f}"'
          ' stroke="#120b06" stroke-width="6" stroke-linecap="round"/></g>')
    s += table(452)
    s += ('<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
          '<ellipse cx="430" cy="492" rx="92" ry="20" fill="#e4d4b6"/>'
          '<path d="M376 486 C374 462 404 448 436 448 C470 448 492 462 492 482 C492 492 468 491 440 491 C408 491 388 492 376 486 Z" fill="#9a4a14"/>'
          '<circle cx="382" cy="494" r="11" fill="#f0921f"/><circle cx="486" cy="492" r="11" fill="#f0921f"/></g>')
    s += herbs_glass(196, 466) + herbs_glass(596, 470, 38, 52)
    s += A.candle(309, 414, t, 52, 42)
    for i, (x, sc, coat, skin, hair, ph) in enumerate((
            (124, .62, "#8a6b8e", "#eec194", "#d9d4cb", .0),
            (300, .66, "#53647a", "#e5b184", "#3e2a18", .3),
            (536, .60, "#9c5a3c", "#f0c79c", "#7a4a24", .6),
            (676, .48, "#c9a23f", "#f3cfa6", "#a9712f", .85))):
        s += _person(x, 300, t, sc, coat, skin, hair, ph)
    s += A.confetti(t, 24, seed=12)
    return s


def cozy(t):
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(44, 54, 196, 198, t)
    s += tinsel(26)
    s += tree(790, 452, t, 0.78, 1.0)
    s += '<ellipse cx="330" cy="150" rx="150" ry="118" fill="url(#candle)" opacity=".45"/>'
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M300 146 L360 146 L350 112 L310 112 Z" fill="#c9922f"/>'
          '<path d="M276 112 L384 112 L370 60 L290 60 Z" fill="#efb07a"/>'
          '<path d="M330 146 L330 196" stroke="#1b1309" stroke-width="8"/></g>')
    s += '<path d="M0 404 L960 404 L960 540 L0 540 Z" fill="#6b4524"/>'
    s += '<path d="M0 398 L960 398 L960 414 L0 414 Z" fill="#96663a"/>'
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M96 540 C96 436 150 396 236 396 C322 396 376 436 376 540 Z" fill="#8a6b4a"/>'
          '<path d="M128 440 C128 404 168 388 236 388 C304 388 344 404 344 440 C344 462 300 468 236 468 C172 468 128 462 128 440 Z" fill="#a8845c"/>'
          '<path d="M452 540 C452 462 492 430 556 430 C620 430 660 462 660 540 Z" fill="#7d8f6a"/></g>')
    s += A.candle(468, 350, t, 56, 48)
    s += herbs_glass(612, 356)
    s += A.confetti(t, 18, seed=10)
    return s


def yang(t):
    """Иероглиф 羊: две откидные точки, три черты, вертикаль насквозь."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += tinsel(20)
    s += tree(874, 452, t, 0.4, 0.4)
    g = .14 + .05 * A.w(t, 3.3)
    s += f'<circle cx="470" cy="286" r="238" fill="#d6202f" opacity="{g:.2f}"/>'
    k = '<g fill="#f2e3c6" stroke="#2a1105" stroke-width="10" stroke-linejoin="round">'
    k += '<path d="M396 164 C386 134 378 116 366 100 L394 84 C408 108 416 134 422 160 Z"/>'
    k += '<path d="M544 164 C554 134 562 116 574 100 L546 84 C532 108 524 134 518 160 Z"/>'
    k += '<path d="M352 192 L588 192 L588 222 L352 222 Z"/>'
    k += '<path d="M330 278 L610 278 L610 308 L330 308 Z"/>'
    k += '<path d="M308 364 L632 364 L632 396 L308 396 Z"/>'
    k += '<path d="M452 150 L488 150 L488 472 L452 472 Z"/>'
    k += '</g>'
    s += k
    s += A.confetti(t, 16, seed=13)
    return s


def retro(t, child=False):
    s = '<rect width="960" height="540" fill="url(#sepia)"/>'
    s += ('<g opacity=".2" stroke="#d8c28a" stroke-width="3" fill="none">'
          + "".join(f'<path d="M{60+i*140} {60+(i%2)*100} q16 22 0 44 q-16 -22 0 -44"/>' for i in range(7)) + '</g>')
    s += ('<g stroke="#1a1208" stroke-width="8" stroke-linejoin="round">'
          '<rect x="708" y="96" width="196" height="150" rx="10" fill="#5a3f22"/>'
          '<rect x="730" y="118" width="134" height="106" rx="6" fill="#8ea7b4"/>'
          '<circle cx="884" cy="150" r="10" fill="#c9a86a"/><circle cx="884" cy="186" r="10" fill="#c9a86a"/>'
          '<path d="M806 96 L770 44 M806 96 L848 44" stroke="#8a7446" stroke-width="7"/></g>')
    fl = .22 + .14 * A.w(t, 0.21)
    s += (f'<g opacity="{fl:.2f}" fill="#cfe0ea"><rect x="736" y="124" width="124" height="18" rx="4"/>'
          '<rect x="736" y="178" width="124" height="14" rx="4"/></g>')
    s += ('<g stroke="#1a1208" stroke-width="7" stroke-linejoin="round">'
          '<path d="M60 152 L188 152 L176 96 L72 96 Z" fill="#9a8450"/>'
          '<path d="M124 152 L124 206" stroke="#1a1208" stroke-width="7"/></g>')
    s += tree(300, 408, t, 0.54, 0.8)
    s += '<path d="M0 420 L960 420 L960 540 L0 540 Z" fill="#8e7340"/>'
    s += '<path d="M0 412 L960 412 L960 430 L0 430 Z" fill="#a98c52"/>'
    s += ('<g stroke="#1a1208" stroke-width="8" stroke-linejoin="round">'
          '<ellipse cx="470" cy="478" rx="156" ry="34" fill="#ded0ae"/>'
          '<path d="M380 466 C378 434 416 414 470 414 C524 414 560 432 560 462 C560 476 528 474 476 474 C424 474 396 476 380 466 Z" fill="#8a5a2a"/>'
          '<ellipse cx="166" cy="490" rx="86" ry="22" fill="#cfc09e"/>'
          '<ellipse cx="166" cy="486" rx="62" ry="14" fill="#6b7a3a"/>'
          '<rect x="676" y="430" width="44" height="62" rx="5" fill="#cfd8dc" opacity=".65"/>'
          '<rect x="736" y="438" width="40" height="54" rx="5" fill="#cfd8dc" opacity=".65"/>'
          '<path d="M832 430 L876 430 L870 492 L838 492 Z" fill="#7a8a4a"/></g>')
    s += A.smoke(470, 414, t, 3, 130, 1.0, .2)
    s += A.candle(600, 356, t, 58, 40)
    if child:
        s += _person(240, 300, t, .46, "#7a6a3e", "#e8c79c", "#6b5330", .2)
        s += _person(712, 300, t, .44, "#6b5a3a", "#dcbb8e", "#4a3a22", .7)
    s += '<rect width="960" height="540" fill="#2a1f10" opacity=".22"/>'
    return s


def retro_child(t):
    return retro(t, child=True)


def _horse_head(t):
    s = '<g stroke="#1b0806" stroke-width="8" stroke-linejoin="round">'
    s += '<path d="M616 102 C700 106 772 166 790 254 C808 346 764 428 684 476 C736 394 744 310 704 236 C672 178 644 138 616 102 Z" fill="#9c2a12"/>'
    s += '<path d="M650 140 C726 152 780 212 788 284 C752 232 704 204 658 200 Z" fill="#c43c18"/>'
    s += '<path d="M600 78 C664 68 724 100 752 152 C708 122 660 112 624 124 Z" fill="#d9541f"/></g>'
    s += ('<g stroke="#7a1c0a" stroke-width="6" fill="none" opacity=".75">'
          '<path d="M660 150 C712 182 744 240 744 300 M688 196 C726 232 746 282 744 330 M632 122 C688 140 730 182 748 230"/></g>')
    e1 = A.sway(t, 5.2, .1, 2.0)
    s += (f'<g transform="rotate({e1:.2f} 600 100)">'
          '<path d="M578 96 C582 54 598 28 620 18 C632 48 628 84 612 110 Z" fill="#bc553c" stroke="#1b0806" stroke-width="8" stroke-linejoin="round"/>'
          '<path d="M642 108 C658 70 682 46 706 42 C706 78 690 114 666 134 Z" fill="#a0432e" stroke="#1b0806" stroke-width="8" stroke-linejoin="round"/></g>')
    s += ('<path d="M632 118 C692 146 704 218 680 286 C652 364 584 420 492 444 C420 462 364 440 336 400'
          ' C310 364 324 320 364 280 C432 212 540 96 632 118 Z" fill="#c95c3e" stroke="#1b0806" stroke-width="9" stroke-linejoin="round"/>'
          '<path d="M580 166 C608 186 612 234 588 286 C562 342 510 386 446 410 C426 390 430 358 458 322 C498 270 544 198 580 166 Z" fill="#e08157" opacity=".8"/>'
          '<path d="M676 240 C668 324 598 400 492 440 C560 396 614 330 640 254 Z" fill="#9c3c24" opacity=".6"/>')
    if A.blink(t, 4.4, .4):
        s += '<path d="M580 218 C590 208 606 208 614 218" stroke="#1b0806" stroke-width="9" fill="none" stroke-linecap="round"/>'
    else:
        lk = 3 * A.w(t, 7.1, .2)
        s += ('<ellipse cx="596" cy="220" rx="26" ry="24" fill="#2e0f06" stroke="#1b0806" stroke-width="7"/>'
              f'<circle cx="{588+lk:.1f}" cy="212" r="8" fill="#f6cf84"/>')
    s += '<path d="M560 188 C584 172 616 176 630 194" stroke="#1b0806" stroke-width="14" fill="none" stroke-linecap="round"/>'
    s += '<path d="M386 374 C400 362 424 366 430 384 C422 402 394 402 384 388 Z" fill="#1b0806"/>'
    s += '<path d="M352 404 C382 424 428 424 458 404" stroke="#1b0806" stroke-width="9" fill="none" stroke-linecap="round"/>'
    s += A.smoke(330, 372, t, 3, 110, .8, .3)
    s += ('<path d="M660 290 C692 376 724 436 782 500 L430 500 C488 450 584 362 660 290 Z" fill="#aa4630" stroke="#1b0806" stroke-width="9" stroke-linejoin="round"/>'
          '<g stroke="#7f3020" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M560 400 C586 430 604 464 610 500 M640 350 C668 392 688 444 692 500"/></g>')
    return s


def horse(t):
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    gl = .45 + .08 * A.w(t, 2.9)
    s += (f'<g opacity="{gl:.2f}"><ellipse cx="760" cy="420" rx="260" ry="150" fill="#d9601a"/>'
          '<ellipse cx="200" cy="440" rx="200" ry="120" fill="#b8320f"/></g>')
    s += '<path d="M0 452 L960 452 L960 540 L0 540 Z" fill="#6b2318"/>'
    s += '<path d="M0 446 L960 446 L960 462 L0 462 Z" fill="#9a3524"/>'
    s += ('<g stroke="#1b0806" stroke-width="7" stroke-linejoin="round" opacity=".9">'
          '<ellipse cx="120" cy="490" rx="86" ry="20" fill="#d9c7a6"/>'
          '<path d="M62 486 C60 460 92 444 132 444 C172 444 198 458 198 480 C198 492 170 490 136 490 C100 490 76 492 62 486 Z" fill="#7d3a12"/>'
          '<ellipse cx="840" cy="496" rx="78" ry="18" fill="#d9c7a6"/>'
          '<path d="M790 492 C788 470 814 456 846 456 C878 456 898 468 898 486 C898 496 876 494 848 494 C818 494 802 496 790 492 Z" fill="#8a4414"/>'
          '<ellipse cx="470" cy="508" rx="96" ry="20" fill="#cbb79a"/></g>')
    s += _horse_head(t)
    return s


SCENES = {
    "open": open_newyear, "dish": dish, "table_top": table_top, "three": three_animals,
    "yang": yang, "cozy": cozy, "makers": makers, "koza": koza, "koza_fire": koza_fire,
    "koza_turn": koza_turn, "koza_table": koza_table, "koza_eye": koza_eye,
    "koza_shadow": koza_shadow, "koza_far": koza_far,
    "guests": guests, "ded": ded, "horse": horse,
    "retro": retro, "retro_child": retro_child,
}

NO_GLARE = {"yang", "table_top"}


def svg(name, t=0.0, gt=0.0, zoom=1.0, cx=0.5, cy=0.5, out=(1920, 1080)):
    """Зум задаётся ОКНОМ ПРОСМОТРА, а не растягиванием картинки:
    поэтому движение непрерывное и кадр всегда резкий."""
    body = SCENES[name](t)
    if name not in NO_GLARE:
        body += A.glare(gt, 13.0, 1.6)
    vw, vh = W / zoom, H / zoom
    vx, vy = cx * (W - vw), cy * (H - vh)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{out[0]}" height="{out[1]}"'
            f' viewBox="{vx:.4f} {vy:.4f} {vw:.4f} {vh:.4f}">{DEFS}{body}</svg>')
