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


def _clock(cx, cy, r, t, face="#e4d4b6", ink="#120b06"):
    """Круглые часы: стрелки идут ПО часовой стрелке (минутная и секундная).
    Раньше стрелка качалась синусом туда-обратно — это читалось как обратный ход."""
    import math as _m
    s = (f'<g stroke="{ink}" stroke-width="7">'
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{face}"/>'
         f'<circle cx="{cx}" cy="{cy}" r="6" fill="{ink}"/></g>')
    s += f'<g stroke="{ink}" stroke-width="5" stroke-linecap="round" opacity=".8">'
    for k in range(12):
        a = 2 * _m.pi * k / 12
        r1 = r - (r * 0.26 if k % 3 == 0 else r * 0.16)
        s += (f'<path d="M{cx + _m.sin(a)*r1:.1f} {cy - _m.cos(a)*r1:.1f}'
              f' L{cx + _m.sin(a)*(r-5):.1f} {cy - _m.cos(a)*(r-5):.1f}"/>')
    s += '</g>'
    ma = 2 * _m.pi * ((t / 60.0) % 1.0)          # минутная: круг за минуту
    sa = 2 * _m.pi * ((t / 6.0) % 1.0)           # секундная: круг за шесть секунд
    s += (f'<path d="M{cx} {cy} L{cx + _m.sin(ma)*r*0.60:.1f} {cy - _m.cos(ma)*r*0.60:.1f}"'
          f' stroke="{ink}" stroke-width="7" stroke-linecap="round"/>'
          f'<path d="M{cx} {cy} L{cx + _m.sin(sa)*r*0.80:.1f} {cy - _m.cos(sa)*r*0.80:.1f}"'
          ' stroke="#c0203a" stroke-width="4" stroke-linecap="round"/>')
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
    s += '<g transform="translate(960,0) scale(-1,1)">' + _koza_head(t, fire=False, blink_ph=.35) + '</g>'
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
    """Тень козы на освещённой стене: силуэт того же профиля, что и у зверей."""
    import re
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += '<ellipse cx="420" cy="230" rx="470" ry="330" fill="#c79a52" opacity=".42"/>'
    s += '<ellipse cx="420" cy="230" rx="330" ry="240" fill="#e0b263" opacity=".3"/>'
    s += ('<g opacity=".22" stroke="#7a5a2a" stroke-width="3" fill="none">'
          + "".join(f'<path d="M{60+i*110} {70+(i%2)*90} q16 22 0 44 q-16 -22 0 -44"/>' for i in range(9)) + '</g>')
    body = _goat_side(470, 320, t, .15)
    body = re.sub(r'fill="#[0-9a-fA-F]{6}"', 'fill="#1a120a"', body)
    body = re.sub(r'stroke="#[0-9a-fA-F]{6}"', 'stroke="#1a120a"', body)
    body = re.sub(r'fill="#[0-9a-fA-F]{3}"', 'fill="#1a120a"', body)
    body = body.replace('opacity=".3"', 'opacity="0"').replace('opacity=".4"', 'opacity="0"')
    s += f'<g opacity=".82" transform="translate(40,-20) scale(1.06)">{body}</g>'
    s += tree(862, 492, t, 0.62, 1.0)
    s += table(492)
    s += A.candle(120, 420, t, 70, 86)
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


def koza_table_right(t):
    """Тот же стол, но коза стоит СПРАВА, у ёлки: слева место под плашку
    (его правка 02.11 — на 1:37 текст накрывал козу)."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(42, 48, 180, 190, t)
    s += tinsel(24)
    s += tree(892, 404, t, 0.56, 0.9)
    s += '<path d="M0 330 L960 330 L960 540 L0 540 Z" fill="url(#cloth)"/>'
    s += '<path d="M0 322 L960 322 L960 344 L0 344 Z" fill="#c6523a"/>'
    s += '<g transform="translate(478,14) scale(0.56)">' + _koza_head(t, blink_ph=.2) + '</g>'
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<ellipse cx="236" cy="452" rx="150" ry="36" fill="#e4d4b6"/>'
          '<path d="M150 440 C148 404 188 382 240 382 C292 382 326 402 326 436 C326 452 294 450 244 450'
          ' C196 450 166 452 150 440 Z" fill="#9a4a14"/>'
          '<circle cx="160" cy="452" r="14" fill="#f0921f"/><circle cx="316" cy="450" r="14" fill="#f0921f"/></g>')
    s += A.smoke(236, 382, t, 3, 150, 1.0, .26)
    s += herbs_glass(392, 400, 44, 60)
    s += A.candle(86, 330, t, 62, 46)
    return s


def koza_table(t):
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(42, 48, 180, 190, t)
    s += tinsel(24)
    s += tree(820, 404, t, 0.62, 0.95)
    s += '<path d="M0 330 L960 330 L960 540 L0 540 Z" fill="url(#cloth)"/>'
    s += '<path d="M0 322 L960 322 L960 344 L0 344 Z" fill="#c6523a"/>'
    s += '<g transform="translate(222,14) scale(0.56)">' + _koza_head(t, blink_ph=.55) + '</g>'
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
    o += '<path d="M146 150 C168 142 192 150 198 168 C190 182 158 184 142 174 Z" fill="#f3c9a0"/></g>'
    # БОКАЛ ДЕРЖИТСЯ ЗА НОЖКУ (его правка 02.11): узкая чаша, видимая ножка,
    # пальцы обхватывают её поперёк, подставка висит под пальцами
    o += ('<g stroke="#1b0806" stroke-width="6" stroke-linejoin="round">'
          '<path d="M150 62 L206 62 L196 106 C192 122 164 122 160 106 Z" fill="url(#glass)"/>'
          '<path d="M157 92 L199 92 L196 106 C192 122 164 122 160 106 Z" fill="#f6c84e" opacity=".85"/></g>'
          '<path d="M178 120 L178 170" stroke="#1b0806" stroke-width="7" stroke-linecap="round"/>'
          '<ellipse cx="178" cy="176" rx="26" ry="7" fill="#dfe6ea" stroke="#1b0806" stroke-width="6"/>')
    for i in range(3):
        p = ((t * .5) + i * .33) % 1.0
        o += (f'<circle cx="{166+i*12}" cy="{104-p*28:.0f}" r="{4-i*0.6:.1f}" fill="#fff6d0"'
              f' opacity="{(1-p)*0.85:.2f}"/>')
    # пальцы поперёк ножки — рука реально держит бокал
    o += ('<g stroke="#1b0806" stroke-width="5" stroke-linejoin="round" fill="#f3c9a0">'
          '<path d="M150 132 C166 126 194 128 204 138 C192 148 160 146 150 132 Z"/>'
          '<path d="M150 148 C166 142 192 144 202 154 C190 164 158 162 150 148 Z"/>'
          '<path d="M186 126 C198 122 208 130 206 142 C198 148 188 142 186 126 Z"/></g>')
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
    s += tree(118, 468, t, 0.52, 1.0)
    s += table(470)
    s += _ded(392, 252, t, 0.92)
    s += _snowman(812, 452, t, 0.42, .35)
    s += A.confetti(t, 20, seed=2)
    return s


# ---------------- ПЕРВЫЙ КАДР: новогодний стол ----------------

def open_newyear(t):
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(40, 58, 176, 186, t)
    s += tinsel(22)
    s += _clock(300, 96, 44, t)
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
    s += _clock(300, 104, 46, t)
    s += table(452)
    # люди стоят ЗА столом, а предметы на столе — ПЕРЕД ними (его правка 02.11)
    for i, (x, sc, coat, skin, hair, ph) in enumerate((
            (124, .62, "#8a6b8e", "#eec194", "#d9d4cb", .0),
            (300, .66, "#53647a", "#e5b184", "#3e2a18", .3),
            (536, .60, "#9c5a3c", "#f0c79c", "#7a4a24", .6),
            (676, .48, "#c9a23f", "#f3cfa6", "#a9712f", .85))):
        s += _person(x, 300, t, sc, coat, skin, hair, ph)
    s += ('<g stroke="#10180c" stroke-width="6" stroke-linejoin="round">'
          '<rect x="640" y="392" width="78" height="54" rx="4" fill="#a8512c"/>'
          '<path d="M679 392 L679 446 M640 416 L718 416" stroke="#f6c84e" stroke-width="8"/>'
          '<path d="M664 392 C660 374 672 364 684 368 C696 360 710 370 704 390 Z" fill="#f6c84e"/></g>')
    s += ('<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
          '<ellipse cx="430" cy="492" rx="92" ry="20" fill="#e4d4b6"/>'
          '<path d="M376 486 C374 462 404 448 436 448 C470 448 492 462 492 482 C492 492 468 491 440 491 C408 491 388 492 376 486 Z" fill="#9a4a14"/>'
          '<circle cx="382" cy="494" r="11" fill="#f0921f"/><circle cx="486" cy="492" r="11" fill="#f0921f"/></g>')
    s += herbs_glass(196, 466) + herbs_glass(596, 470, 38, 52)
    s += A.candle(300, 452, t, 58, 46)
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
    """Иероглиф 羊: две откидные сверху, три горизонтали, вертикаль насквозь."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += tinsel(20)
    s += tree(876, 452, t, 0.38, 0.4)
    g = .15 + .05 * A.w(t, 3.3)
    s += f'<circle cx="470" cy="290" r="226" fill="#d6202f" opacity="{g:.2f}"/>'
    k = '<g fill="#f6ead2" stroke="#2a1105" stroke-width="9" stroke-linejoin="round">'
    # откидные точки: расходятся кверху, сходятся книзу
    k += '<path d="M408 104 L436 96 L462 176 L440 182 Z"/>'
    k += '<path d="M548 104 L520 96 L494 176 L516 182 Z"/>'
    # три горизонтали, книзу шире
    k += '<path d="M356 190 L600 190 L600 220 L356 220 Z"/>'
    k += '<path d="M332 276 L624 276 L624 308 L332 308 Z"/>'
    k += '<path d="M308 364 L648 364 L648 398 L308 398 Z"/>'
    # вертикаль насквозь, выходит ниже
    k += '<path d="M462 178 L498 178 L498 468 L462 468 Z"/>'
    k += '</g>'
    s += k
    s += A.confetti(t, 16, seed=13)
    return s


def retro(t, child=False):
    s = '<rect width="960" height="540" fill="url(#sepia)"/>'
    s += ('<g opacity=".2" stroke="#d8c28a" stroke-width="3" fill="none">'
          + "".join(f'<path d="M{60+i*140} {60+(i%2)*100} q16 22 0 44 q-16 -22 0 -44"/>' for i in range(7)) + '</g>')
    # телевизор КРУПНЕЕ (его правка 02.11): в экран едет ч/б вставка стока.
    # Экран в кадре 1920x1080 — это (1332,224) размером 496x356, см. plan.STOCK13
    s += ('<g stroke="#1a1208" stroke-width="8" stroke-linejoin="round">'
          '<rect x="632" y="80" width="312" height="236" rx="12" fill="#5a3f22"/>'
          '<rect x="666" y="112" width="248" height="178" rx="8" fill="#1d2529"/>'
          '<circle cx="930" cy="160" r="12" fill="#c9a86a"/><circle cx="930" cy="208" r="12" fill="#c9a86a"/>'
          '<path d="M760 80 L716 20 M760 80 L812 20" stroke="#8a7446" stroke-width="8"/></g>')
    fl = .10 + .08 * A.w(t, 0.21)
    s += (f'<g opacity="{fl:.2f}" fill="#cfe0ea"><rect x="672" y="120" width="236" height="20" rx="4"/>'
          '<rect x="672" y="250" width="236" height="16" rx="4"/></g>')
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


# ---------------- ЧАСТЬ 4: нрав Лошади против нрава Козы ----------------

def _garland(t, y=16):
    """Гирлянда через весь верх: провис, лампочки мигают вразнобой."""
    s = (f'<path d="M0 {y} Q160 {y+46} 320 {y+8} Q480 {y-30} 640 {y+8} Q800 {y+46} 960 {y}"'
         ' stroke="#4a3a22" stroke-width="5" fill="none"/>')
    pts = ((80, y+32), (160, y+38), (240, y+28), (320, y+8), (400, y-8), (480, y-16),
           (560, y-8), (640, y+8), (720, y+28), (800, y+38), (880, y+32))
    cols = ("#ffd45e", "#ff8c6b", "#9ae06a", "#7fd0ff")
    return s + A.lights([(x, yy, cols[i % 4]) for i, (x, yy) in enumerate(pts)], t)


def _silho(x, y, t, sc=1.0, ph=0.0):
    """Силуэт гостя в тёплом контровом свете: покачивается, живой."""
    a = A.sway(t, 6.0, ph, 1.2)
    return (f'<g transform="rotate({a:.2f} {x} {y+150}) translate({x},{y}) scale({sc})">'
            '<path d="M-98 180 C-98 76 -56 38 0 38 C56 38 98 76 98 180 Z" fill="#2a150c"/>'
            '<circle cx="0" cy="-12" r="48" fill="#2a150c"/>'
            '<path d="M-42 -40 C-26 -66 26 -66 42 -40 L42 -24 L-42 -24 Z" fill="#2a150c"/>'
            '<path d="M46 -28 C62 -4 64 36 50 64" stroke="#e08a3c" stroke-width="7" fill="none" opacity=".45"/>'
            '<path d="M-46 -28 C-62 -4 -64 36 -50 64" stroke="#e08a3c" stroke-width="5" fill="none" opacity=".25"/>'
            '</g>')


def _snowman(x, y, t, sc=1.0, ph=0.0):
    """Снеговик: три кома, ведро, морковка, шарф. Моргает и покачивается."""
    a = A.sway(t, 5.8, ph, 1.5)
    g = f'<g transform="rotate({a:.2f} {x} {y}) translate({x},{y}) scale({sc})">'
    g += '<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
    g += '<ellipse cx="0" cy="0" rx="92" ry="80" fill="#f4f7fa"/>'
    g += '<ellipse cx="0" cy="-116" rx="68" ry="60" fill="#f8fbfd"/>'
    g += '<ellipse cx="0" cy="-214" rx="50" ry="46" fill="#fdfeff"/>'
    g += ('<path d="M-104 -124 C-140 -150 -152 -186 -144 -210" stroke="#6b4320" stroke-width="11"'
          ' fill="none" stroke-linecap="round"/>'
          '<path d="M104 -124 C140 -150 152 -186 144 -210" stroke="#6b4320" stroke-width="11"'
          ' fill="none" stroke-linecap="round"/>')
    g += ('<path d="M-56 -248 L56 -248 L44 -318 L-44 -318 Z" fill="#8a9aa6"/>'
          '<rect x="-66" y="-258" width="132" height="18" rx="5" fill="#73838f"/></g>')
    g += ('<path d="M-54 -176 C-18 -192 20 -192 54 -176 C40 -156 -36 -156 -54 -176 Z" fill="#c22a24"'
          ' stroke="#1b1309" stroke-width="8" stroke-linejoin="round"/>'
          '<path d="M38 -172 C62 -156 70 -126 64 -102 L30 -108 C40 -130 40 -154 38 -172 Z" fill="#a8201c"'
          ' stroke="#1b1309" stroke-width="8" stroke-linejoin="round"/>')
    if A.blink(t, 4.7, ph + .3):
        g += ('<path d="M-32 -228 C-24 -236 -10 -236 -2 -228" stroke="#1b1309" stroke-width="7"'
              ' fill="none" stroke-linecap="round"/>'
              '<path d="M4 -228 C12 -236 26 -236 34 -228" stroke="#1b1309" stroke-width="7"'
              ' fill="none" stroke-linecap="round"/>')
    else:
        lk = 2.5 * A.w(t, 7.2, ph)
        g += (f'<circle cx="{-17 + lk:.1f}" cy="-230" r="9" fill="#1b1309"/>'
              f'<circle cx="{19 + lk:.1f}" cy="-230" r="9" fill="#1b1309"/>'
              f'<circle cx="{-20 + lk:.1f}" cy="-234" r="3.4" fill="#fff" opacity=".85"/>'
              f'<circle cx="{16 + lk:.1f}" cy="-234" r="3.4" fill="#fff" opacity=".85"/>')
    g += ('<path d="M0 -214 L52 -200 L0 -192 Z" fill="#e8721f" stroke="#1b1309" stroke-width="7"'
          ' stroke-linejoin="round"/>')
    g += '<g fill="#1b1309">'
    for bx, by in ((-26, -176), (0, -170), (26, -176)):
        g += f'<circle cx="{bx}" cy="{by}" r="5"/>'
    g += '</g><g fill="#2a2018">'
    for bx, by in ((-24, -122), (0, -112), (24, -122)):
        g += f'<circle cx="{bx}" cy="{by}" r="8"/>'
    return g + '</g></g>'


def _bunch(x, y, t, sc=1.0, ph=0.0):
    """Пучок зелени на бечёвке: висит и качается."""
    a = A.sway(t, 6.6, ph, 1.6)
    g = f'<g transform="rotate({a:.2f} {x} {y-150}) translate({x},{y}) scale({sc})">'
    g += '<path d="M0 -150 L0 -16" stroke="#8a7a58" stroke-width="5"/>'
    g += '<g stroke="#4e7a35" stroke-width="8" fill="none" stroke-linecap="round">'
    for dx, dy in ((-48, 86), (-26, 106), (0, 116), (26, 106), (48, 86), (-14, 112), (14, 112)):
        g += '<path d="M0 -10 C%d %d %d %d %d %d"/>' % (dx * 0.5, dy * 0.4, dx * 0.9, dy * 0.75, dx, dy)
    g += '</g><g fill="#3f6b2c" stroke="#1b1309" stroke-width="4">'
    for dx, dy, r in ((-50, 88, 13), (-28, 108, 12), (0, 118, 14), (28, 108, 12), (50, 88, 13),
                      (-14, 114, 10), (14, 114, 10), (-38, 70, 10), (38, 68, 10)):
        g += '<circle cx="%d" cy="%d" r="%d"/>' % (dx, dy, r)
    g += '</g>'
    g += ('<rect x="-17" y="-26" width="34" height="20" rx="5" fill="#c9922f"'
          ' stroke="#1b1309" stroke-width="5"/>')
    return g + '</g>'


def _bowl(cx, cy, rx, ry, col, heap=1.0, berry=None, bowl="#dccbab", rot=0.0):
    """Салатница с горкой: чаша, горка салата, вкрапления."""
    s = f'<g transform="rotate({rot} {cx} {cy})">' if rot else '<g>'
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          f'<path d="M{cx-rx} {cy} C{cx-rx} {cy+ry*1.6:.0f} {cx+rx} {cy+ry*1.6:.0f} {cx+rx} {cy} Z" fill="{bowl}"/>'
          f'<path d="M{cx-rx} {cy} C{cx-rx*0.62:.0f} {cy-ry*heap:.0f} {cx+rx*0.62:.0f} {cy-ry*heap:.0f} {cx+rx} {cy}'
          f' C{cx+rx*0.5:.0f} {cy+ry*0.34:.0f} {cx-rx*0.5:.0f} {cy+ry*0.34:.0f} {cx-rx} {cy} Z" fill="{col}"/></g>')
    if berry:
        for bx, by, rr in ((-rx*0.44, -ry*0.44, 9), (0, -ry*0.70, 10), (rx*0.40, -ry*0.38, 8)):
            s += (f'<circle cx="{cx+bx:.0f}" cy="{cy+by:.0f}" r="{rr}" fill="{berry}"'
                  ' stroke="#1b0f07" stroke-width="4"/>')
    return s + '</g>'


def _bottle(x, y, col, h=78, rot=0.0):
    s = f'<g transform="rotate({rot} {x} {y})">' if rot else '<g>'
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          f'<path d="M{x-22} {y} L{x-22} {y-h} C{x-22} {y-h-18} {x-9} {y-h-22} {x-9} {y-h-40}'
          f' L{x+9} {y-h-40} C{x+9} {y-h-22} {x+22} {y-h-18} {x+22} {y-h} L{x+22} {y} Z" fill="{col}"/>'
          f'<rect x="{x-11}" y="{y-h-62}" width="22" height="24" rx="3" fill="#c9922f"/>'
          f'<rect x="{x-20}" y="{y-h+12}" width="40" height="30" rx="3" fill="#e4d4b6"/></g>')
    return s + '</g>'


def _goblet(x, y, t, sc=1.0, ph=0.0, wine="#9b1b28"):
    """Бокал на ножке: вино в нём колышется, сам бокал чуть качается."""
    a = 1.7 * A.w(t, 3.4, ph)
    return (f'<g transform="rotate({a:.2f} {x} {y})"><g transform="translate({x},{y}) scale({sc})">'
            '<path d="M-26 -78 L26 -78 L20 -26 C18 -12 -18 -12 -20 -26 Z" fill="url(#glass)"'
            ' stroke="#1b1309" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M-23 -50 L23 -50 L19 -27 C17 -14 -17 -14 -19 -27 Z" fill="{wine}" opacity=".85"/>'
            '<path d="M0 -12 L0 8" stroke="#1b1309" stroke-width="7"/>'
            '<path d="M-17 10 L17 10" stroke="#1b1309" stroke-width="8" stroke-linecap="round"/>'
            '</g></g>')


def _roast(cx, cy, sc=1.0, dark="#8d3a12", light="#b4541c", bone=True, rot=0.0, cut=True):
    """Запечённое мясо: неровный бок, косая решётка надрезов, срез с мякотью, кость."""
    g = f'<g transform="rotate({rot} {cx} {cy}) translate({cx},{cy}) scale({sc})">'
    g += '<g stroke="#1b0806" stroke-width="9" stroke-linejoin="round">'
    if bone:
        g += ('<path d="M104 -2 C126 -14 148 -14 158 -4 C168 6 164 22 150 26 C136 30 118 24 106 14 Z"'
              ' fill="#efe6d2"/>'
              '<path d="M150 -8 C160 -14 170 -6 166 4 C174 8 174 22 162 24" fill="#efe6d2"/>')
    g += ('<path d="M-116 44 C-128 12 -112 -18 -84 -30 C-62 -40 -44 -26 -24 -36 C-4 -46 10 -34 28 -40'
          ' C52 -48 72 -34 90 -24 C114 -10 126 10 118 40 C114 58 62 56 0 56 C-62 56 -104 60 -116 44 Z"'
          f' fill="{dark}"/></g>')
    g += (f'<path d="M-92 20 C-98 -6 -78 -24 -54 -26 C-34 -28 -22 -16 -2 -22 C16 -27 30 -16 48 -14'
          f' C72 -11 90 2 92 22 C54 2 -56 2 -92 20 Z" fill="{light}"/>')
    d1 = "".join('<path d="M%d 34 L%d -14"/>' % (-78 + k * 30, -46 + k * 30) for k in range(7))
    d2 = "".join('<path d="M%d 34 L%d -14"/>' % (-46 + k * 30, -78 + k * 30) for k in range(7))
    g += ('<g stroke="#5c2208" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round">'
          + d1 + d2 + '</g>')
    if cut:
        g += ('<g stroke="#1b0806" stroke-width="8" stroke-linejoin="round">'
              '<path d="M-116 44 C-128 12 -112 -18 -84 -30 C-74 -16 -70 16 -78 48 C-92 50 -110 52 -116 44 Z"'
              ' fill="#f0ddc4"/>'
              '<path d="M-110 38 C-118 14 -108 -10 -88 -20 C-82 -8 -80 14 -86 40 C-96 42 -106 42 -110 38 Z"'
              ' fill="#c2563f"/></g>'
              '<path d="M-104 28 C-108 12 -102 -2 -94 -10" stroke="#e59a86" stroke-width="5"'
              ' fill="none" stroke-linecap="round" opacity=".8"/>')
    g += ('<path d="M-56 -14 C-18 -30 34 -28 66 -10" stroke="#f2c98a" stroke-width="7" fill="none"'
          ' stroke-linecap="round" opacity=".4"/>')
    return g + '</g>'


def _cutlery(x, y, fork=False):
    """Нож или вилка, лежит на столе."""
    s = '<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
    s += f'<rect x="{x}" y="{y}" width="58" height="18" rx="6" fill="#6b4320"/>'
    if fork:
        s += f'<path d="M{x+58} {y+2} L{x+112} {y+2} L{x+112} {y+16} L{x+58} {y+16} Z" fill="#cfd4d9"/>'
        s += (f'<g stroke="#1b0f07" stroke-width="6">'
              f'<path d="M{x+112} {y+2} L{x+150} {y-2} M{x+112} {y+7} L{x+152} {y+6}'
              f' M{x+112} {y+12} L{x+152} {y+13} M{x+112} {y+16} L{x+150} {y+20}"/></g>')
    else:
        s += (f'<path d="M{x+58} {y+2} L{x+150} {y+1} C{x+164} {y+1} {x+164} {y+15} {x+150} {y+16}'
              f' L{x+58} {y+16} Z" fill="#cfd4d9"/>')
    return s + '</g>'


def feast(t):
    """Застолье Лошади: мясо на открытом огне, поднятые бокалы, стол ломится."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    gl = .30 + .07 * A.w(t, 3.1)
    s += (f'<g opacity="{gl:.2f}"><ellipse cx="470" cy="330" rx="340" ry="190" fill="#d9601a"/>'
          '<ellipse cx="110" cy="240" rx="150" ry="110" fill="#b8320f"/></g>')
    s += window(34, 70, 140, 148, t)
    s += _garland(t, 20)
    s += tree(886, 338, t, 0.42, 0.8)
    s += _silho(228, 182, t, 0.92, .0) + _silho(866, 190, t, 0.88, .5)
    s += '<path d="M0 352 L960 352 L960 540 L0 540 Z" fill="url(#cloth)"/>'
    s += '<path d="M0 344 L960 344 L960 368 L0 368 Z" fill="#c6523a"/>'
    s += ('<g stroke="#1b0806" stroke-width="9" stroke-linejoin="round">'
          '<path d="M338 502 L622 502 L596 430 L364 430 Z" fill="#3a2a1d"/></g>')
    for i, (ex, ec) in enumerate(((396, "#e8701b"), (448, "#f7b740"), (500, "#e8701b"), (552, "#c23a0d"))):
        o = .5 + .5 * A.w(t, 1.3 + .21 * i, i * .3)
        s += f'<ellipse cx="{ex}" cy="464" rx="25" ry="10" fill="{ec}" opacity="{o:.2f}"/>'
    for i, fx in enumerate((386, 432, 478, 524, 570)):
        s += A.flame(fx, 448, t, .58, 26, i * .23)
    s += ('<g stroke="#2a1e14" stroke-width="7" stroke-linecap="round">'
          + "".join('<path d="M%d 418 L%d 434"/>' % (352 + i * 38, 352 + i * 38) for i in range(8))
          + '<path d="M344 418 L616 418"/></g>')
    s += _roast(484, 362, 1.0, "#7a2d0c", "#9c4414")
    s += A.smoke(484, 318, t, 3, 190, 1.1, .3)
    s += _bowl(148, 450, 86, 34, "#efe3c8", 1.0, "#c0203a")
    s += _bowl(816, 446, 80, 32, "#e8dcc0", 0.9, "#4e7a35")
    s += _bottle(256, 500, "#2c4a2a")
    s += _bottle(708, 496, "#5c1f16")
    s += _goblet(300, 404, t, 1.0, .1)
    s += _goblet(668, 398, t, 1.05, .55)
    s += A.candle(922, 470, t, 50, 40)
    s += A.confetti(t, 26, seed=14)
    return s


def heap(t):
    """Стол ломится: посуда налезает друг на друга, беспорядок, гонка за количеством."""
    s = '<rect width="960" height="540" fill="url(#cloth)"/>'
    s += '<g opacity=".16" stroke="#f0c98a" stroke-width="4" fill="none">'
    for i in range(6):
        for j in range(4):
            s += '<path d="M%d %d q18 24 0 48 q-18 -24 0 -48"/>' % (70 + i * 170, 50 + j * 140)
    s += '</g>'
    s += (f'<g opacity="{.22 + .05 * A.w(t, 3.7):.2f}">'
          '<ellipse cx="480" cy="250" rx="360" ry="220" fill="#e8701b"/></g>')
    s += ('<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round" opacity=".95">'
          '<g transform="rotate(-7 128 150)"><ellipse cx="128" cy="150" rx="88" ry="42" fill="#dccbab"/>'
          '<ellipse cx="128" cy="146" rx="58" ry="25" fill="#b8431f"/></g>'
          '<g transform="rotate(6 296 124)"><ellipse cx="296" cy="124" rx="82" ry="39" fill="#e8dac0"/>'
          '<ellipse cx="296" cy="120" rx="54" ry="23" fill="#8a6b3f"/></g>'
          '<g transform="rotate(-5 842 158)"><ellipse cx="842" cy="158" rx="88" ry="41" fill="#dccbab"/>'
          '<ellipse cx="842" cy="154" rx="58" ry="24" fill="#4e7a35"/></g>'
          '<g transform="rotate(9 712 120)"><ellipse cx="712" cy="120" rx="70" ry="34" fill="#e8dac0"/>'
          '<ellipse cx="712" cy="116" rx="44" ry="19" fill="#c0203a"/></g></g>')
    s += _bottle(466, 214, "#2c4a2a", 70, -6)
    s += _bottle(552, 204, "#5c1f16", 64, 4)
    s += _bottle(624, 216, "#2c4a2a", 58, -3)
    s += _bowl(168, 302, 104, 43, "#efe3c8", 1.05, "#c0203a", rot=-4)
    s += _bowl(348, 286, 92, 39, "#e9dfc2", 1.0, "#4e7a35", rot=5)
    s += _bowl(792, 300, 98, 40, "#efe3c8", 1.1, "#e07f23", rot=-6)
    s += _bowl(652, 268, 72, 30, "#e4d8bb", 0.95, "#c9922f", rot=7)
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round" transform="rotate(-3 520 400)">'
          '<ellipse cx="520" cy="402" rx="252" ry="58" fill="#c9b89a"/>'
          '<ellipse cx="520" cy="392" rx="218" ry="44" fill="#e8dac0"/></g>')
    s += _roast(520, 346, 1.18, rot=-3)
    s += A.smoke(520, 296, t, 3, 150, 1.0, .22)
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<g transform="rotate(5 128 488)"><ellipse cx="128" cy="488" rx="130" ry="53" fill="#e8dac0"/>'
          '<path d="M46 474 C42 430 82 402 134 402 C186 402 222 428 220 470 Z" fill="#9a4a14"/></g>'
          '<g transform="rotate(-6 846 492)"><ellipse cx="846" cy="492" rx="126" ry="51" fill="#dccbab"/>'
          '<path d="M784 480 L824 432 L864 480 Z" fill="#f0d98a"/>'
          '<rect x="866" y="452" width="46" height="30" rx="4" fill="#f6edd2"/></g></g>')
    s += _goblet(388, 502, t, 1.1, .2)
    s += _goblet(650, 508, t, 1.05, .7)
    s += A.confetti(t, 20, seed=18)
    return s


def pork(t):
    """Запечённая свинина крупно: тяжёлое блюдо, пар, нож и вилка."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    gl = .26 + .06 * A.w(t, 3.3)
    s += f'<g opacity="{gl:.2f}"><ellipse cx="480" cy="300" rx="330" ry="200" fill="#d9601a"/></g>'
    s += _garland(t, 18)
    s += ('<g opacity=".5" stroke="#10180c" stroke-width="6" stroke-linejoin="round">'
          '<path d="M842 118 L906 200 L878 200 L942 276 L766 276 L826 200 L798 200 Z" fill="#2f5c2a"/></g>')
    s += '<path d="M0 368 L960 368 L960 540 L0 540 Z" fill="url(#cloth)"/>'
    s += '<path d="M0 360 L960 360 L960 384 L0 384 Z" fill="#c6523a"/>'
    s += A.candle(92, 300, t, 68, 50)
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<ellipse cx="470" cy="452" rx="302" ry="64" fill="#c9b89a"/>'
          '<ellipse cx="470" cy="438" rx="266" ry="50" fill="#e8dac0"/></g>')
    s += ('<g fill="#4e7a35" stroke="#1b0f07" stroke-width="5">'
          '<ellipse cx="236" cy="446" rx="46" ry="15"/><ellipse cx="706" cy="446" rx="46" ry="15"/></g>')
    s += ('<g stroke="#1b0f07" stroke-width="5">'
          '<circle cx="292" cy="456" r="27" fill="#e8963a"/>'
          '<circle cx="292" cy="456" r="18" fill="#f6b85e"/>'
          '<circle cx="650" cy="456" r="25" fill="#e8963a"/>'
          '<circle cx="650" cy="456" r="16" fill="#f6b85e"/></g>')
    s += ('<g stroke="#43703a" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M178 452 L268 432"/>'
          '<path d="M196 442 L190 424 M216 438 L210 420 M236 434 L230 416"/>'
          '<path d="M700 450 L780 430"/>'
          '<path d="M716 440 L710 422 M736 436 L730 418 M756 432 L750 414"/></g>')
    s += _roast(470, 356, 1.62)
    s += A.smoke(470, 282, t, 3, 200, 1.3, .32)
    s += _cutlery(30, 484, fork=True)
    s += '<g transform="translate(960,0) scale(-1,1)">' + _cutlery(30, 488, fork=False) + '</g>'
    s += A.confetti(t, 14, seed=21)
    return s


def koza_door(t):
    """Гостья входит в дом: светлый проём, коза на пороге, впереди угол заваленного стола."""
    s = '<rect width="960" height="540" fill="#1d1309"/>'
    s += ('<g opacity=".18" stroke="#7a5a2a" stroke-width="3" fill="none">'
          + "".join('<path d="M%d %d q16 22 0 44 q-16 -22 0 -44"/>' % (556 + i * 104, 56 + (i % 2) * 92)
                    for i in range(4)) + '</g>')
    s += _garland(t, 10)
    s += ('<g stroke="#120b06" stroke-width="12" stroke-linejoin="round">'
          '<rect x="92" y="60" width="380" height="480" rx="4" fill="#31240f"/></g>')
    s += '<rect x="112" y="80" width="340" height="460" fill="url(#roomc)"/>'
    gl = .32 + .07 * A.w(t, 3.4)
    s += f'<ellipse cx="282" cy="280" rx="200" ry="250" fill="#e8a24a" opacity="{gl:.2f}"/>'
    s += ('<g transform="translate(564,0) scale(-1,1)">'
          '<g transform="translate(-96,128) scale(0.62)">' + _koza_head(t, blink_ph=.25) + '</g></g>')
    s += ('<g stroke="#120b06" stroke-width="10" stroke-linejoin="round">'
          '<path d="M472 44 L578 86 L578 526 L472 540 Z" fill="#4a3520"/>'
          '<path d="M492 96 L558 122 L558 300 L492 288 Z" fill="#5c4228"/>'
          '<circle cx="556" cy="330" r="10" fill="#c9922f"/></g>')
    s += '<path d="M112 512 L452 512 L560 540 L60 540 Z" fill="#e8a24a" opacity=".15"/>'
    s += ('<g stroke="#120b06" stroke-width="10" stroke-linejoin="round">'
          '<path d="M596 540 L628 386 L960 356 L960 540 Z" fill="#5a1f15"/></g>')
    s += '<path d="M628 386 L960 356 L960 380 L624 410 Z" fill="#8a2f20"/>'
    s += '<g opacity=".9">'
    s += ('<g stroke="#120b06" stroke-width="9" stroke-linejoin="round">'
          '<ellipse cx="886" cy="432" rx="120" ry="44" fill="#a99b80"/></g>')
    s += _roast(886, 392, 0.92, "#5e2a11", "#7c3a16", rot=-4)
    s += _bowl(690, 474, 80, 33, "#b8ab8e", 1.0, "#7d2030", bowl="#8e8169")
    s += _goblet(744, 520, t, 1.0, .35, "#6d1620")
    s += '</g>'
    s += A.confetti(t, 12, seed=24)
    return s


def greens(t):
    """Опора 1: зелень в стаканах и на доске — то, что ценит хозяйка года."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _garland(t, 14)
    s += ('<g opacity=".45" stroke="#10180c" stroke-width="6" stroke-linejoin="round">'
          '<path d="M828 108 L896 194 L866 194 L936 278 L720 278 L790 194 L760 194 Z" fill="#2f5c2a"/></g>')
    s += ('<g opacity=".5"><circle cx="806" cy="206" r="12" fill="#d6202f"/>'
          '<circle cx="866" cy="240" r="11" fill="#c9922f"/></g>')
    s += _bunch(632, 158, t, 1.15, .2)
    s += '<path d="M0 352 L960 352 L960 540 L0 540 Z" fill="url(#cloth)"/>'
    s += '<path d="M0 344 L960 344 L960 366 L0 366 Z" fill="#c6523a"/>'
    s += A.candle(70, 246, t, 98, 56)
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<rect x="520" y="396" width="330" height="86" rx="12" fill="#b07d3f"/>'
          '<circle cx="836" cy="420" r="11" fill="#8a5c2a"/></g>')
    s += ('<g stroke="#8a5c2a" stroke-width="4" opacity=".7">'
          '<path d="M540 420 L820 420 M540 448 L820 448"/></g>')
    s += ('<g stroke="#1b1309" stroke-width="5">'
          '<ellipse cx="586" cy="410" rx="46" ry="14" fill="#4e7a35"/>'
          '<ellipse cx="668" cy="416" rx="40" ry="12" fill="#5e9a4a"/>'
          '<circle cx="748" cy="412" r="27" fill="#f2d24a"/>'
          '<circle cx="748" cy="412" r="19" fill="#f8ea9e"/></g>'
          '<g stroke="#e0b62a" stroke-width="4" stroke-linecap="round">'
          '<path d="M748 393 L748 431 M731 403 L765 421 M731 421 L765 403"/></g>'
          '<g stroke="#1b1309" stroke-width="5">'
          '<circle cx="806" cy="440" r="24" fill="#c0203a"/>'
          '<path d="M806 416 L800 404 L812 404 Z" fill="#8c2130"/>'
          '<circle cx="778" cy="452" r="15" fill="#d6202f"/></g>')
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M96 374 L196 374 L186 492 C184 506 108 506 106 492 Z" fill="url(#glass)"/>'
          '<path d="M240 382 L332 382 L323 490 C321 503 251 503 249 490 Z" fill="url(#glass)"/>'
          '<path d="M372 376 L466 376 L457 488 C455 501 383 501 381 488 Z" fill="url(#glass)"/></g>')
    s += ('<g stroke="#2f5c2a" stroke-width="8" fill="none" stroke-linecap="round" opacity=".55">'
          '<path d="M120 420 L124 486 M160 420 L156 486 M268 428 L272 486 M300 428 L296 486'
          ' M400 422 L404 484 M436 422 L432 484"/></g>')
    # петрушка
    s += (f'<g transform="rotate({A.sway(t, 5.4, .0, 1.1):.2f} 146 374)'
          f' translate(146,374) scale(1.2) translate(-146,-374)">')
    s += ('<g stroke="#4e7a35" stroke-width="9" fill="none" stroke-linecap="round">'
          '<path d="M146 374 L140 262"/><path d="M140 290 C106 268 96 230 104 202"/>'
          '<path d="M140 318 C178 298 192 258 184 228"/><path d="M140 250 C116 232 110 206 116 186"/></g>'
          '<g fill="#3f6b2c" stroke="#1b1309" stroke-width="4">'
          '<circle cx="100" cy="196" r="18"/><circle cx="124" cy="178" r="15"/>'
          '<circle cx="188" cy="222" r="18"/><circle cx="170" cy="198" r="14"/>'
          '<circle cx="112" cy="178" r="13"/><circle cx="82" cy="214" r="13"/>'
          '<circle cx="152" cy="206" r="12"/><circle cx="200" cy="246" r="13"/>'
          '<circle cx="134" cy="170" r="12"/></g></g>')
    # укроп
    s += (f'<g transform="rotate({A.sway(t, 4.7, .35, 1.3):.2f} 286 382)'
          f' translate(286,382) scale(1.2) translate(-286,-382)">')
    s += ('<g stroke="#5c8f3a" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M286 382 L282 276"/><path d="M282 302 C256 286 248 258 254 236"/>'
          '<path d="M282 326 C312 310 322 280 316 256"/><path d="M282 290 C306 272 316 248 312 226"/>'
          '<path d="M282 314 C258 302 246 280 250 258"/></g>'
          '<g stroke="#79b34c" stroke-width="4" fill="none" stroke-linecap="round" opacity=".95">'
          '<path d="M254 236 L240 216 M254 236 L268 214 M254 236 L236 240 M316 256 L332 236'
          ' M316 256 L302 232 M316 256 L336 260 M282 276 L266 254 M282 276 L300 252'
          ' M312 226 L300 206 M312 226 L328 208 M282 258 L262 244 M282 258 L302 240'
          ' M268 268 L252 258 M296 268 L312 258 M250 258 L234 240 M250 258 L264 236'
          ' M250 258 L232 262 M266 286 L250 272 M298 286 L314 272 M254 248 L238 230'
          ' M312 240 L326 222 M300 218 L288 198 M312 226 L330 214"/></g></g>')
    # розмарин
    s += (f'<g transform="rotate({A.sway(t, 6.1, .6, 1.0):.2f} 418 376)'
          f' translate(418,376) scale(1.2) translate(-418,-376)">')
    s += ('<g stroke="#43703a" stroke-width="8" fill="none" stroke-linecap="round">'
          '<path d="M418 376 L412 254"/><path d="M412 300 C390 288 382 266 386 248"/>'
          '<path d="M412 330 C438 318 448 294 444 274"/><path d="M412 276 C434 262 442 240 438 222"/></g>'
          '<g stroke="#5e9a4a" stroke-width="4" stroke-linecap="round">'
          '<path d="M404 266 L386 258 M420 272 L438 262 M404 292 L384 284 M420 298 L440 288'
          ' M404 318 L386 312 M420 324 L440 316 M408 346 L390 340 M418 352 L438 344'
          ' M406 242 L388 234 M418 248 L436 238 M408 222 L392 212 M416 226 L432 216'
          ' M430 236 L444 226 M434 258 L450 250 M410 282 L392 274 M422 286 L440 276'
          ' M410 308 L390 300 M422 312 L442 302 M412 334 L394 328 M420 338 L440 330'
          ' M406 254 L390 246 M418 258 L434 248 M410 212 L396 200 M414 214 L428 202'
          ' M412 364 L396 358 M416 366 L432 360"/></g></g>')
    s += A.confetti(t, 14, seed=27)
    return s


# ======================= ЧАСТЬ 5: семь опор стола =======================
# Рисунки перенесены из РИСУНКИ.html и ОЖИВЛЕНЫ: свечи горят, пар идёт,
# огоньки ёлки мигают, зелень качается — статичный кадр здесь запрещён.

def _boke(pts, op=".3"):
    """Расфокусированные огни на заднем плане."""
    s = f'<g opacity="{op}">'
    for x, y, r, c in pts:
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
    return s + '</g>'


def _plate_oval(cx, cy, rx, ry, rim="#cfbf9f", inner="#ece0c6"):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{rim}"'
            ' stroke="#1b0f07" stroke-width="9"/>'
            f'<ellipse cx="{cx}" cy="{cy-12}" rx="{rx*0.89:.0f}" ry="{ry*0.81:.0f}" fill="{inner}"/>')


def cheese(t):
    """Опора 2: сырная доска с характером — три сыра и три сопровождения."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(840, 86, 18, "#ffd45e"), (740, 128, 14, "#ff8c6b"),
                (906, 162, 13, "#9ae06a"), (640, 78, 11, "#7fd0ff")])
    s += tree(120, 268, t, 0.52, 0.5, star=False)
    s += _garland(t, 10)
    s += table(300)
    s += A.candle(900, 258, t, 72, 46, phase=.3, s=.85)
    # доска
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M70 352 L812 352 C860 352 884 376 884 404 L884 452 C884 486 856 506 812 506'
          ' L70 506 C40 506 24 486 24 452 L24 404 C24 376 40 352 70 352 Z" fill="#b07d3f"/>'
          '<path d="M884 404 L930 404 C944 404 950 414 950 428 C950 442 944 452 930 452 L884 452 Z"'
          ' fill="#9a6a33"/></g>'
          '<g stroke="#8a5c2a" stroke-width="4" opacity=".55">'
          '<path d="M60 380 L840 380 M60 476 L840 476"/></g>')
    # козий сыр с белой корочкой
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<ellipse cx="166" cy="428" rx="98" ry="38" fill="#f6f1e4"/>'
          '<path d="M68 428 C68 406 112 390 166 390 C220 390 264 406 264 428" fill="#faf7ee"/>'
          '<path d="M130 416 L206 416 L222 448 L114 448 Z" fill="#f2e4c4"/></g>'
          '<g stroke="#ddd2b8" stroke-width="4" opacity=".8">'
          '<path d="M96 428 C120 418 212 418 236 428"/></g>')
    # фета кубиками
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M330 450 L330 400 L392 380 L392 430 Z" fill="#f8f5ee"/>'
          '<path d="M330 400 L392 380 L440 396 L378 418 Z" fill="#fffdf7"/>'
          '<path d="M378 418 L440 396 L440 446 L378 468 Z" fill="#ece6d8"/>'
          '<path d="M300 486 L300 450 L344 434 L344 470 Z" fill="#f8f5ee"/>'
          '<path d="M300 450 L344 434 L378 446 L334 462 Z" fill="#fffdf7"/></g>')
    # твёрдый сыр клином, кристаллики поблёскивают
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M498 462 L498 392 L664 420 L664 486 Z" fill="#e8c86a"/>'
          '<path d="M498 392 L664 420 L622 440 L482 414 Z" fill="#f2d87f"/></g>'
          '<g fill="#c9a23f"><circle cx="546" cy="442" r="7"/><circle cx="588" cy="456" r="5.5"/>'
          '<circle cx="628" cy="446" r="6"/></g>')
    for i, (gx, gy, gr) in enumerate(((562, 428, 2.6), (606, 436, 2.2), (530, 462, 2.4))):
        o = .35 + .45 * (0.5 + 0.5 * A.w(t, 2.3 + i * .6, i * .3))
        s += f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="#fff" opacity="{o:.2f}"/>'
    # мёд с орехами
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M712 410 C712 398 788 398 788 410 L782 462 C780 480 720 480 718 462 Z" fill="#dcccae"/>'
          '<path d="M716 424 C736 416 766 416 784 424 L780 460 C778 474 722 474 720 460 Z" fill="#d8982a"/></g>')
    dz = 4 * A.w(t, 5.2, .1)
    s += (f'<path d="M750 388 C750 374 {762+dz:.0f} 366 {772+dz:.0f} 372" stroke="#8a6a3a"'
          ' stroke-width="7" fill="none" stroke-linecap="round"/>')
    s += ('<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
          '<path d="M826 452 C812 444 810 424 822 414 C834 404 854 408 860 422 C866 436 856 452 840 456 Z"'
          ' fill="#c2914f"/>'
          '<path d="M834 418 C840 430 838 444 832 452 M824 432 L854 428" stroke="#8a6133"'
          ' stroke-width="4" fill="none"/>'
          '<path d="M880 484 C866 476 864 458 876 448 C888 438 906 442 912 456 C918 470 908 486 894 490 Z"'
          ' fill="#b8854a"/></g>')
    # инжир разрезанный
    s += ('<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          '<path d="M604 500 C590 482 596 456 618 448 C640 440 662 454 662 476 C662 496 640 510 620 506 Z"'
          ' fill="#7b4a6e"/>'
          '<path d="M614 492 C606 480 610 464 624 460 C638 456 650 466 650 478 C650 490 638 498 626 496 Z"'
          ' fill="#c4556a"/><circle cx="630" cy="478" r="7" fill="#e8a0a8"/></g>')
    # яблоко дольками
    s += ('<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          '<path d="M404 500 C416 478 448 470 466 484 C448 504 420 512 404 500 Z" fill="#f2e8d2"/>'
          '<path d="M440 508 C452 486 484 478 502 492 C484 512 456 520 440 508 Z" fill="#f2e8d2"/>'
          '<path d="M476 514 C488 492 520 484 538 498 C520 518 492 526 476 514 Z" fill="#f2e8d2"/></g>'
          '<g stroke="#c0203a" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M414 496 C428 482 448 478 462 484 M450 504 C464 490 484 486 498 492'
          ' M486 510 C500 496 520 492 534 498"/></g>')
    s += A.confetti(t, 12, seed=51)
    return s


def pumpkin(t):
    """Опора 3: запечённая тыква с козьим сыром и гранатом. Горячая — идёт пар."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(120, 80, 18, "#ffd45e"), (240, 122, 14, "#ff8c6b"), (52, 156, 13, "#9ae06a")])
    s += tree(846, 272, t, 0.54, 0.5, star=False)
    s += _garland(t, 12)
    s += table(316)
    s += _plate_oval(480, 438, 376, 86)
    # дольки веером
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<path d="M196 436 C190 378 224 334 272 330 C286 376 268 428 240 444 Z" fill="#d97119"/>'
          '<path d="M276 444 C266 376 302 326 356 322 C370 374 348 430 318 450 Z" fill="#ef9a2e"/>'
          '<path d="M356 450 C344 378 382 324 440 322 C454 378 430 436 398 456 Z" fill="#e08523"/>'
          '<path d="M440 452 C428 380 468 326 526 326 C540 382 516 438 484 458 Z" fill="#ef9a2e"/>'
          '<path d="M526 448 C514 378 554 326 610 328 C622 382 598 436 566 454 Z" fill="#d97119"/>'
          '<path d="M610 442 C600 380 638 332 690 336 C700 386 678 432 648 448 Z" fill="#ef9a2e"/></g>'
          '<g stroke="#9c4a12" stroke-width="6" fill="none" opacity=".75">'
          '<path d="M212 404 C224 376 248 356 268 348 M292 408 C306 374 334 350 352 342'
          ' M372 412 C386 376 416 350 436 342 M456 414 C470 378 500 352 522 346'
          ' M542 410 C556 376 584 352 606 348 M624 404 C636 376 662 356 684 352"/></g>')
    # раскрошенный козий сыр
    s += ('<g fill="#f8f4e8" stroke="#1b0f07" stroke-width="4">'
          '<circle cx="268" cy="384" r="13"/><circle cx="340" cy="372" r="11"/>'
          '<circle cx="420" cy="380" r="14"/><circle cx="498" cy="370" r="11"/>'
          '<circle cx="572" cy="382" r="13"/><circle cx="650" cy="388" r="10"/>'
          '<circle cx="306" cy="412" r="9"/><circle cx="462" cy="410" r="10"/>'
          '<circle cx="612" cy="408" r="9"/></g>')
    # гранат
    s += ('<g fill="#c0203a" stroke="#7a0f20" stroke-width="3">'
          '<circle cx="240" cy="416" r="8"/><circle cx="300" cy="392" r="7"/>'
          '<circle cx="366" cy="404" r="8"/><circle cx="394" cy="360" r="7"/>'
          '<circle cx="452" cy="394" r="8"/><circle cx="524" cy="402" r="7"/>'
          '<circle cx="548" cy="358" r="7"/><circle cx="606" cy="396" r="8"/>'
          '<circle cx="672" cy="412" r="7"/><circle cx="330" cy="440" r="7"/>'
          '<circle cx="492" cy="438" r="7"/><circle cx="636" cy="434" r="6"/></g>')
    for i, (gx, gy) in enumerate(((237, 412), (449, 390), (603, 392))):
        o = .35 + .4 * (0.5 + 0.5 * A.w(t, 2.9 + i * .5, i * .4))
        s += f'<circle cx="{gx}" cy="{gy}" r="2.6" fill="#ff8ea0" opacity="{o:.2f}"/>'
    # мята — качается
    for cxm, cym, per, ph, d in ((400, 310, 5.6, .0, 'M392 332 C376 316 380 294 400 288 C420 282 436 298 430 316 C426 330 408 340 392 332 Z'),
                                 (534, 302, 6.2, .4, 'M528 324 C512 308 516 288 534 282 C552 276 568 290 562 308 C558 322 542 332 528 324 Z')):
        a = A.sway(t, per, ph, 2.2)
        s += (f'<g transform="rotate({a:.2f} {cxm} {cym+30})">'
              f'<path d="{d}" fill="#3f8c3c" stroke="#1b0f07" stroke-width="5" stroke-linejoin="round"/></g>')
    s += ('<g stroke="#235a22" stroke-width="3" fill="none">'
          '<path d="M398 330 L418 294 M534 322 L552 288"/></g>')
    # мёд струйкой
    hz = 5 * A.w(t, 4.4, .2)
    s += (f'<path d="M480 300 C{486+hz:.0f} 322 {478+hz:.0f} 342 486 364" stroke="#d8982a"'
          ' stroke-width="9" fill="none" stroke-linecap="round" opacity=".9"/>')
    s += A.smoke(372, 318, t, 3, 150, .9, .26)
    s += A.smoke(584, 322, t * 1.13 + .7, 2, 130, .8, .2)
    s += A.confetti(t, 12, seed=63)
    return s


def pumpkin_goat(t):
    """Знак внимания: дольки тыквы выложены козьей головой, рога — зеленью.
    Форму держит контур головы, а дольки — мозаика внутри него: иначе
    веер долек читается просто как куча, а не как морда."""
    HEAD = ("M334 372 C334 320 392 300 470 300 C548 300 606 320 606 372"
            " C606 406 586 430 552 450 C524 466 500 502 470 502"
            " C440 502 416 466 388 450 C354 430 334 406 334 372 Z")
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(130, 88, 17, "#ffd45e"), (252, 126, 13, "#ff8c6b"), (60, 158, 12, "#9ae06a")])
    s += tree(858, 282, t, 0.5, 0.45, star=False)
    s += _garland(t, 12)
    s += table(326)
    s += _plate_oval(470, 436, 348, 104, "#d4c6a8", "#f2ead6")
    # уши — две дольки по бокам лба
    for ex, sgn in ((318, -1), (622, 1)):
        s += (f'<g transform="translate({ex},356) scale({sgn},1)">'
              '<path d="M0 -26 C44 -34 72 -6 64 26 C34 38 2 18 0 -26 Z" fill="#c9661a"'
              ' stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/></g>')
    # рога зеленью — из-за ушей вверх и наружу
    for sx, sgn, ph in ((374, -1, .0), (566, 1, .45)):
        a = A.sway(t, 6.4, ph, 1.6)
        s += f'<g transform="rotate({a:.2f} {sx} 316)">'
        s += (f'<path d="M{sx} 316 C{sx + sgn * 54} 274 {sx + sgn * 76} 216 {sx + sgn * 42} 174"'
              ' stroke="#43703a" stroke-width="13" fill="none" stroke-linecap="round"/>')
        s += '<g stroke="#5e9a4a" stroke-width="5" stroke-linecap="round">'
        for k in range(6):
            u = (k + 0.4) / 5.6
            xx = sx + sgn * (54 * 3 * u * (1 - u) ** 2 + 76 * 3 * u * u * (1 - u) + 42 * u ** 3)
            yy = 316 - (42 * 3 * u * (1 - u) ** 2 + 100 * 3 * u * u * (1 - u) + 142 * u ** 3)
            s += (f'<path d="M{xx:.0f} {yy:.0f} L{xx + sgn * 22:.0f} {yy - 13:.0f}'
                  f' M{xx:.0f} {yy:.0f} L{xx - sgn * 13:.0f} {yy - 18:.0f}"/>')
        s += '</g></g>'
    # сама голова, выложенная тыквой
    s += f'<path d="{HEAD}" fill="#e08523" stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
    s += f'<clipPath id="goathead"><path d="{HEAD}"/></clipPath>'
    s += '<g clip-path="url(#goathead)">'
    for i, x in enumerate((352, 400, 448, 496, 544, 592)):
        s += (f'<path d="M{x} 286 C{x + 16} 340 {x + 12} 408 {x - 10} 512 L{x + 34} 512'
              f' C{x + 56} 408 {x + 60} 340 {x + 44} 286 Z"'
              f' fill="{"#ef9a2e" if i % 2 == 0 else "#d97119"}" opacity=".95"/>')
    s += ('<g stroke="#9c4a12" stroke-width="6" fill="none" opacity=".75">'
          '<path d="M352 300 C368 356 364 420 342 512 M400 292 C416 348 412 414 390 512'
          ' M448 288 C464 344 460 410 438 512 M496 288 C512 344 508 410 486 512'
          ' M544 292 C560 348 556 414 534 512 M592 300 C608 356 604 420 582 512"/></g>'
          '<g stroke="#b4541c" stroke-width="5" fill="none" opacity=".5">'
          '<path d="M320 352 C400 338 540 338 620 352 M330 420 C410 408 530 408 610 420"/></g>')
    s += '</g>'
    # глаза из граната, нос, борода
    s += ('<g stroke="#7a0f20" stroke-width="4">'
          '<ellipse cx="418" cy="372" rx="21" ry="16" fill="#8c1026"/>'
          '<ellipse cx="522" cy="372" rx="21" ry="16" fill="#8c1026"/></g>'
          '<g fill="#c0203a"><circle cx="418" cy="372" r="9"/><circle cx="522" cy="372" r="9"/></g>'
          '<g fill="#f8f4e8" opacity=".9"><circle cx="412" cy="366" r="4"/>'
          '<circle cx="516" cy="366" r="4"/></g>')
    s += ('<path d="M450 452 C462 462 478 462 490 452" stroke="#7a0f20" stroke-width="7"'
          ' fill="none" stroke-linecap="round"/>'
          '<g fill="#7a0f20"><ellipse cx="470" cy="434" rx="15" ry="9"/></g>')
    a = A.sway(t, 5.0, .2, 2.6)
    s += (f'<g transform="rotate({a:.2f} 470 500)">'
          '<g stroke="#4e7a35" stroke-width="8" fill="none" stroke-linecap="round">'
          '<path d="M456 498 C450 516 454 528 464 536 M482 498 C488 518 486 530 476 538"/></g>'
          '<g fill="#3f6b2c" stroke="#1b0f07" stroke-width="4">'
          '<circle cx="458" cy="528" r="13"/><circle cx="480" cy="532" r="12"/>'
          '<circle cx="470" cy="514" r="11"/></g></g>')
    s += ('<g fill="#c0203a" stroke="#7a0f20" stroke-width="3">'
          '<circle cx="250" cy="456" r="8"/><circle cx="296" cy="484" r="7"/>'
          '<circle cx="658" cy="454" r="8"/><circle cx="704" cy="480" r="7"/>'
          '<circle cx="216" cy="420" r="6"/><circle cx="724" cy="418" r="6"/></g>')
    s += A.smoke(470, 300, t, 2, 120, .8, .16)
    s += A.confetti(t, 12, seed=71)
    return s


def _mushroom(cx, base, sc=1.0, cap="#9c6a3e", rim="#7d5128", tilt=0.0):
    """Гриб, который УЗНАЁТСЯ: купол шляпки с тёмным ободом, светлая ножка
    с юбочкой и пластинки под шляпкой. Без пластинок и юбочки коричневый
    купол читался как булка (его правка 02.11)."""
    g = (f'<g transform="translate({cx},{base}) rotate({tilt}) scale({sc})">'
         '<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
         '<path d="M-17 0 C-21 -34 -19 -54 -15 -62 L15 -62 C19 -54 21 -34 17 0 Z" fill="#efe0c2"/>'
         '<path d="M-58 -58 C-58 -98 -32 -124 0 -124 C32 -124 58 -98 58 -58'
         ' C58 -48 34 -42 0 -42 C-34 -42 -58 -48 -58 -58 Z" fill="' + cap + '"/></g>'
         '<path d="M-52 -62 C-40 -52 -16 -46 0 -46 C16 -46 40 -52 52 -62'
         ' C52 -52 30 -46 0 -46 C-30 -46 -52 -52 -52 -62 Z" fill="' + rim + '"/>'
         '<g stroke="' + rim + '" stroke-width="4" opacity=".85">'
         '<path d="M-36 -50 L-34 -62 M-18 -46 L-18 -60 M0 -45 L0 -60 M18 -46 L18 -60 M36 -50 L34 -62"/></g>'
         '<path d="M-44 -96 C-28 -108 -4 -112 12 -108" stroke="#ffffff" stroke-width="7"'
         ' fill="none" opacity=".22" stroke-linecap="round"/>'
         '<path d="M-19 -54 C-8 -48 8 -48 19 -54" stroke="#d9c7a2" stroke-width="6" fill="none"/>'
         '</g>')
    return g


def pate(t):
    """Опора 4: грибной паштет с грецкими орехами на поджаренном хлебе."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(836, 78, 17, "#ffd45e"), (736, 122, 13, "#ff8c6b"), (906, 152, 12, "#9ae06a")],
               ".32")
    s += tree(112, 276, t, 0.52, 0.45, star=False)
    s += _garland(t, 10)
    s += table(320)
    # доска
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<rect x="70" y="372" width="700" height="130" rx="16" fill="#a9762f"/>'
          '<path d="M770 400 L828 400 C844 400 852 412 852 428 C852 446 844 458 828 458 L770 458 Z"'
          ' fill="#8f6227"/></g>'
          '<g stroke="#7f5420" stroke-width="4" opacity=".6">'
          '<path d="M96 400 L744 400 M96 476 L744 476"/></g>')
    # три тоста с паштетом
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<rect x="112" y="396" width="178" height="86" rx="12" fill="#d8a85c"/>'
          '<rect x="318" y="396" width="178" height="86" rx="12" fill="#d8a85c"/>'
          '<rect x="524" y="396" width="178" height="86" rx="12" fill="#d8a85c"/></g>'
          '<g stroke="#a8782f" stroke-width="5" fill="none" opacity=".75">'
          '<path d="M128 420 L274 420 M128 456 L274 456 M334 420 L480 420 M334 456 L480 456'
          ' M540 420 L686 420 M540 456 L686 456"/></g>'
          '<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          '<path d="M136 404 C148 374 254 374 266 404 C272 420 254 430 202 430 C150 430 130 420 136 404 Z"'
          ' fill="#7a5433"/>'
          '<path d="M342 404 C354 374 460 374 472 404 C478 420 460 430 408 430 C356 430 336 420 342 404 Z"'
          ' fill="#8a6039"/>'
          '<path d="M548 404 C560 374 666 374 678 404 C684 420 666 430 614 430 C562 430 542 420 548 404 Z"'
          ' fill="#7a5433"/></g>'
          '<g stroke="#5e3f24" stroke-width="4" fill="none" opacity=".7">'
          '<path d="M158 400 C180 388 226 388 246 400 M364 400 C386 388 432 388 452 400'
          ' M570 400 C592 388 638 388 658 400"/></g>')
    # на каждом тосте лежит целый гриб: иначе коричневая масса не читается
    for i, bx in enumerate((198, 404, 610)):
        s += _mushroom(bx + 26, 412, .30, "#8a5c34" if i % 2 else "#a0693a",
                       "#6b4322", tilt=-8 + i * 8)
    # зелень на тостах качается
    for i, bx in enumerate((198, 404, 610)):
        a = A.sway(t, 5.2 + i * .5, i * .3, 2.6)
        s += (f'<g transform="rotate({a:.2f} {bx} 390)">'
              '<g stroke="#4e7a35" stroke-width="5" fill="none" stroke-linecap="round">'
              f'<path d="M{bx-8} 388 L{bx-18} 368 M{bx+8} 388 L{bx+18} 366"/></g>'
              '<g fill="#3f8c3c" stroke="#1b1309" stroke-width="3">'
              f'<circle cx="{bx-20}" cy="364" r="8"/><circle cx="{bx+22}" cy="362" r="7"/></g></g>')
    # ГРИБЫ, которые узнаются: три штуки целиком стоят на доске, крупно
    # и целиком в кадре (прежние были мелкие, у самого края — его правка 02.11)
    s += _mushroom(806, 516, .92)
    s += _mushroom(884, 522, .70, "#8a5c34", "#6b4322", tilt=7)
    s += _mushroom(742, 524, .58, "#b07c47", "#8a5c34", tilt=-9)
    # тимьян
    a = A.sway(t, 6.8, .25, 1.6)
    s += (f'<g transform="rotate({a:.2f} 740 528)">'
          '<g stroke="#43703a" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M740 528 L808 512"/><path d="M756 520 L750 504 M776 516 L770 500'
          ' M796 512 L792 496 M760 534 L766 548 M782 528 L788 542"/></g></g>')
    # грецкий орех
    s += ('<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
          '<path d="M232 510 C218 502 216 484 228 474 C240 464 258 468 264 482 C270 496 260 512 246 516 Z"'
          ' fill="#c2914f"/>'
          '<path d="M238 478 C244 490 242 504 236 512 M228 492 L258 488" stroke="#8a6133"'
          ' stroke-width="4" fill="none"/></g>')
    s += A.confetti(t, 12, seed=83)
    return s


def duck(t):
    """Опора 5: утка с апельсинами и имбирём. Это именно ПТИЦА: грудка,
    прижатое крыло, две связанные ножки с косточками, гузка — без них
    тушка читается как батон (его слово 01.11)."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(128, 76, 19, "#ffd45e"), (248, 118, 14, "#ff8c6b"),
                (56, 150, 13, "#9ae06a"), (352, 70, 11, "#7fd0ff")], ".32")
    s += tree(852, 262, t, 0.5, 0.45, star=False)
    s += _garland(t, 8)
    s += table(300)
    s += A.candle(90, 214, t, 78, 50, phase=.15)
    s += _plate_oval(500, 440, 386, 88, "#cbb79a", "#e8dac0")
    # тушка: высокая грудка слева, понижение к гузке справа,
    # выемка перед ножками — иначе силуэт читается как батон
    s += ('<g stroke="#1b0f07" stroke-width="10" stroke-linejoin="round">'
          '<path d="M286 428 C268 376 300 320 374 296 C452 270 556 282 616 318'
          ' C664 346 700 376 706 400 C710 424 650 438 566 442'
          ' C452 448 322 450 286 428 Z" fill="url(#duck)"/>'
          # культя шеи слева
          '<path d="M292 390 C250 366 216 368 204 390 C222 414 262 418 292 408 Z" fill="#a85318"/>'
          # гузка справа
          '<path d="M700 382 C742 368 772 376 780 398 C762 418 726 420 698 410 Z" fill="#8f4210"/></g>')
    # шов по грудке
    s += ('<path d="M372 306 C408 336 436 380 448 436" stroke="#8a3c10" stroke-width="7"'
          ' fill="none" opacity=".7"/>')
    # прижатое крыло — отдельной лопастью, темнее тушки
    s += ('<path d="M332 366 C372 330 442 318 498 332 C486 378 424 406 348 400 Z"'
          ' fill="#8f4210" stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
          '<g stroke="#5e2a08" stroke-width="5" fill="none" opacity=".8">'
          '<path d="M360 382 C392 376 424 362 448 342 M378 394 C410 386 442 372 466 350'
          ' M346 368 C376 358 404 346 426 332"/></g>')
    # две ножки: торчат вверх-вправо, перекрещены, с косточками
    for lx, ly, rot, col, sc in ((618, 398, -34, "#b4541c", 1.0), (640, 410, 2, "#a04a14", .92)):
        s += (f'<g transform="rotate({rot} {lx} {ly}) translate({lx},{ly}) scale({sc}) translate({-lx},{-ly})">'
              f'<path d="M{lx} {ly} C{lx+60} {ly-34} {lx+104} {ly-26} {lx+124} {ly-10}'
              f' C{lx+104} {ly+18} {lx+48} {ly+26} {lx} {ly+16} Z" fill="{col}"'
              ' stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
              f'<rect x="{lx+116}" y="{ly-26}" width="30" height="28" rx="10" fill="#f6f1e4"'
              ' stroke="#1b0f07" stroke-width="7"/>'
              f'<path d="M{lx+34} {ly-12} C{lx+62} {ly-6} {lx+86} {ly-4} {lx+106} {ly-10}"'
              ' stroke="#6d300b" stroke-width="5" fill="none" opacity=".7"/></g>')
    # верёвочка, которой ножки связаны
    s += ('<path d="M620 392 C640 378 668 380 682 396" stroke="#e4d4b6" stroke-width="7"'
          ' fill="none" stroke-linecap="round"/>')
    # блестящая корка и насечки
    s += ('<path d="M336 336 C410 300 560 294 644 328" stroke="#d98a30" stroke-width="15"'
          ' fill="none" stroke-linecap="round" opacity=".75"/>'
          '<g stroke="#6d300b" stroke-width="5" fill="none" opacity=".8">'
          '<path d="M332 362 L322 404 M386 386 L380 420 M452 396 L450 428'
          ' M520 398 L522 430 M586 392 L592 424"/></g>')
    for i, (ex, ey, erx, ery) in enumerate(((420, 300, 40, 12), (556, 308, 32, 10))):
        o = .4 + .28 * (0.5 + 0.5 * A.w(t, 3.4 + i * .7, i * .35))
        s += f'<ellipse cx="{ex}" cy="{ey}" rx="{erx}" ry="{ery}" fill="#f2c073" opacity="{o:.2f}"/>'
    # апельсины
    s += ('<g stroke="#1b0f07" stroke-width="8">'
          '<circle cx="214" cy="458" r="46" fill="#f0921f"/><circle cx="214" cy="458" r="31" fill="#ffb455"/>'
          '<circle cx="790" cy="454" r="44" fill="#f0921f"/><circle cx="790" cy="454" r="30" fill="#ffb455"/>'
          '<circle cx="500" cy="474" r="36" fill="#e8821a"/><circle cx="500" cy="474" r="24" fill="#ffab46"/></g>'
          '<g stroke="#e07f23" stroke-width="4" opacity=".9">'
          '<path d="M214 428 L214 488 M184 458 L244 458 M193 437 L235 479 M235 437 L193 479"/>'
          '<path d="M790 424 L790 484 M760 454 L820 454 M769 433 L811 475 M811 433 L769 475"/>'
          '<path d="M500 450 L500 498 M476 474 L524 474"/></g>')
    s += ('<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<path d="M318 472 C332 450 368 442 386 458 C368 480 336 488 318 472 Z" fill="#f2e8d2"/>'
          '<path d="M648 476 C662 454 698 446 716 462 C698 484 666 492 648 476 Z" fill="#f2e8d2"/></g>'
          '<g stroke="#c0203a" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M328 468 C342 454 364 450 380 458 M658 472 C672 458 694 454 710 462"/></g>')
    a = A.sway(t, 6.0, .3, 1.8)
    s += (f'<g transform="rotate({a:.2f} 394 496)">'
          '<g stroke="#43703a" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M394 496 L498 472"/><path d="M414 486 L408 466 M440 480 L434 460'
          ' M466 474 L462 454 M422 504 L428 522 M450 498 L456 516"/></g></g>')
    s += A.smoke(430, 272, t, 3, 170, 1.0, .3)
    s += A.smoke(596, 276, t * 1.17 + 1.2, 2, 150, .9, .22)
    s += A.confetti(t, 12, seed=97)
    return s


def fish(t):
    """Опора 5, запасной путь: рыба целиком на пару — с головой и хвостом."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(128, 82, 18, "#ffd45e"), (246, 122, 14, "#ff8c6b"), (58, 156, 12, "#9ae06a")])
    s += tree(848, 268, t, 0.5, 0.45, star=False)
    s += _garland(t, 10)
    s += table(308)
    s += _plate_oval(480, 442, 396, 84, "#cfc0a2", "#eee3cb")
    # рыба: тело, голова слева, хвост справа
    s += ('<g stroke="#1b0f07" stroke-width="10" stroke-linejoin="round">'
          '<path d="M176 412 C236 344 352 310 492 310 C632 310 724 344 772 404'
          ' C724 462 630 492 492 492 C352 492 234 470 176 412 Z" fill="#bcc6cc"/>'
          '<path d="M772 404 L876 344 L856 410 L884 470 L772 420 Z" fill="#9fb0b8"/>'
          '<path d="M176 412 C204 376 236 356 266 344 L274 470 C236 460 202 440 176 412 Z"'
          ' fill="#aab8c0"/></g>')
    # жаберная дуга, глаз, рот
    s += ('<path d="M266 344 C292 384 292 432 274 470" stroke="#6d7d86" stroke-width="7"'
          ' fill="none"/>'
          '<circle cx="228" cy="396" r="17" fill="#f4efe3" stroke="#1b0f07" stroke-width="6"/>'
          '<circle cx="228" cy="396" r="8" fill="#241208"/>'
          '<path d="M182 432 C200 442 220 444 238 440" stroke="#1b0f07" stroke-width="6"'
          ' fill="none" stroke-linecap="round"/>')
    # чешуя и плавник
    s += '<g stroke="#8d9ba3" stroke-width="4" fill="none" opacity=".75">'
    for k in range(5):
        xx = 330 + k * 92
        s += f'<path d="M{xx} 348 C{xx+26} 388 {xx+26} 420 {xx} 458"/>'
    s += '</g>'
    s += ('<path d="M420 310 C470 272 540 268 580 300" fill="#9fb0b8" stroke="#1b0f07"'
          ' stroke-width="8" stroke-linejoin="round"/>')
    # имбирь и зелёный лук внутри разреза
    s += ('<path d="M330 400 C420 376 560 376 672 398" stroke="#1b0f07" stroke-width="7"'
          ' fill="none"/>'
          '<g stroke="#1b0f07" stroke-width="5">'
          '<ellipse cx="392" cy="392" rx="30" ry="12" fill="#e9c98a" transform="rotate(-8 392 392)"/>'
          '<ellipse cx="500" cy="388" rx="28" ry="11" fill="#f0d9a4" transform="rotate(6 500 388)"/>'
          '<ellipse cx="604" cy="394" rx="26" ry="11" fill="#e9c98a" transform="rotate(-5 604 394)"/></g>')
    for i, lx in enumerate((440, 548, 648)):
        a = A.sway(t, 5.4 + i * .6, i * .3, 2.4)
        s += (f'<g transform="rotate({a:.2f} {lx} 390)">'
              '<g stroke="#5e9a4a" stroke-width="8" fill="none" stroke-linecap="round">'
              f'<path d="M{lx} 392 C{lx+14} 368 {lx+10} 344 {lx-6} 326"/></g>'
              f'<path d="M{lx-6} 326 L{lx-16} 306 M{lx-6} 326 L{lx+10} 308" stroke="#79b34c"'
              ' stroke-width="5" fill="none" stroke-linecap="round"/></g>')
    # лимон и соус
    s += ('<g stroke="#1b0f07" stroke-width="7">'
          '<circle cx="180" cy="492" r="36" fill="#f2d24a"/><circle cx="180" cy="492" r="24" fill="#f8ea9e"/></g>'
          '<g stroke="#e0b62a" stroke-width="4" stroke-linecap="round">'
          '<path d="M180 468 L180 516 M156 492 L204 492 M163 475 L197 509 M197 475 L163 509"/></g>'
          '<g stroke="#1b0f07" stroke-width="6"><ellipse cx="800" cy="492" rx="56" ry="20" fill="#5a3a1e"/></g>'
          '<ellipse cx="792" cy="488" rx="22" ry="7" fill="#7a5433" opacity=".8"/>')
    s += A.smoke(400, 300, t, 3, 180, 1.0, .32)
    s += A.smoke(580, 304, t * 1.21 + .9, 3, 160, .9, .24)
    s += A.confetti(t, 12, seed=103)
    return s


def apples(t):
    """Опора 6: печёные яблоки с творожным кремом и корзина фруктов."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(828, 84, 18, "#ffd45e"), (728, 126, 13, "#ff8c6b"), (902, 158, 12, "#9ae06a")])
    s += tree(118, 274, t, 0.5, 0.45, star=False)
    s += _garland(t, 12)
    s += table(318)
    s += _plate_oval(420, 448, 330, 78, "#d4c6a8", "#f2ead6")
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<path d="M196 420 C188 362 230 324 282 324 C334 324 376 362 368 420'
          ' C362 462 330 482 282 482 C234 482 202 462 196 420 Z" fill="#b8431f"/>'
          '<path d="M396 430 C388 376 428 340 478 340 C528 340 568 376 560 430'
          ' C554 468 524 486 478 486 C432 486 402 468 396 430 Z" fill="#c6512a"/></g>'
          '<g stroke="#8c2d12" stroke-width="5" fill="none" opacity=".7">'
          '<path d="M224 390 C248 372 316 372 340 390 M420 404 C442 388 514 388 536 404"/></g>'
          '<g fill="#e0763f" opacity=".6"><ellipse cx="240" cy="372" rx="30" ry="16"/>'
          '<ellipse cx="438" cy="386" rx="26" ry="14"/></g>'
          '<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<path d="M232 330 C240 300 324 300 332 330 C338 350 310 360 282 360 C254 360 226 350 232 330 Z"'
          ' fill="#f8f4ea"/>'
          '<path d="M432 346 C440 318 518 318 526 346 C532 364 506 374 478 374 C450 374 426 364 432 346 Z"'
          ' fill="#fbf8f0"/></g>')
    # веточки качаются
    for cxv, cyv, per, ph, d in ((282, 300, 5.8, .0, 'M278 276 C262 264 266 246 284 244 C300 242 310 256 304 268 C300 276 288 282 278 276 Z'),
                                 (478, 316, 6.4, .4, 'M474 294 C458 282 462 264 480 262 C496 260 506 274 500 286 C496 294 484 300 474 294 Z')):
        a = A.sway(t, per, ph, 2.0)
        s += (f'<g transform="rotate({a:.2f} {cxv} {cyv})">'
              f'<path d="M{cxv} {cyv} L{cxv-4} {cyv-28}" stroke="#6b3f1c" stroke-width="7"'
              ' fill="none" stroke-linecap="round"/>'
              f'<path d="{d}" fill="#3f8c3c" stroke="#1b0f07" stroke-width="4"/></g>')
    s += ('<g fill="#c0203a" stroke="#7a0f20" stroke-width="3">'
          '<circle cx="248" cy="330" r="8"/><circle cx="286" cy="322" r="7"/>'
          '<circle cx="318" cy="334" r="7"/><circle cx="450" cy="346" r="8"/>'
          '<circle cx="486" cy="338" r="7"/><circle cx="514" cy="350" r="7"/></g>'
          '<g stroke="#1b0f07" stroke-width="5" stroke-linejoin="round">'
          '<path d="M304 348 C296 342 296 330 304 324 C314 318 326 322 328 332 C330 342 320 352 310 352 Z"'
          ' fill="#c2914f"/>'
          '<path d="M506 362 C498 356 498 344 506 338 C516 332 528 336 530 346 C532 356 522 366 512 366 Z"'
          ' fill="#b8854a"/></g>')
    # корзина фруктов
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<path d="M762 404 C762 386 938 386 938 404 L924 488 C920 506 780 506 776 488 Z" fill="#a9762f"/>'
          '<path d="M770 430 L930 430" stroke="#7f5420" stroke-width="5"/></g>'
          '<g stroke="#1b0f07" stroke-width="7">'
          '<circle cx="800" cy="392" r="34" fill="#f0921f"/><circle cx="866" cy="384" r="32" fill="#ef9a2e"/>'
          '<circle cx="922" cy="398" r="28" fill="#f0921f"/><circle cx="836" cy="358" r="30" fill="#c0203a"/></g>'
          '<g stroke="#4e7a35" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M836 330 L832 312"/></g>'
          '<g fill="#ffb455" opacity=".55"><circle cx="792" cy="382" r="9"/>'
          '<circle cx="858" cy="374" r="8"/></g>')
    s += A.smoke(282, 318, t, 2, 120, .8, .2)
    s += A.smoke(478, 332, t * 1.14 + .6, 2, 110, .7, .16)
    s += A.confetti(t, 12, seed=113)
    return s


def mors(t):
    """Седьмое: гранатово-апельсиновый морс с корицей и бадьяном, подогретый."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(132, 80, 20, "#ffd45e"), (258, 124, 15, "#ff8c6b"),
                (54, 158, 13, "#9ae06a"), (364, 74, 12, "#7fd0ff")], ".35")
    s += tree(850, 272, t, 0.52, 0.45, star=False)
    s += _garland(t, 10)
    s += table(352)
    # бутылка игристого сзади
    s += ('<g opacity=".65" stroke="#1b0806" stroke-width="8" stroke-linejoin="round">'
          '<path d="M790 196 L826 196 L826 250 C854 266 866 292 866 326 L866 470'
          ' C866 486 786 486 786 470 L786 326 C786 292 790 266 790 250 Z" fill="#2f5c2a"/>'
          '<rect x="786" y="300" width="80" height="60" rx="4" fill="#c9922f"/>'
          '<rect x="788" y="176" width="40" height="26" rx="4" fill="#c9922f"/></g>')
    # три стакана
    s += ('<g stroke="#1b0806" stroke-width="9" stroke-linejoin="round">'
          '<path d="M158 282 L300 282 L284 492 C282 512 176 512 174 492 Z" fill="url(#glass)"/>'
          '<path d="M172 348 L288 348 L276 486 C274 502 184 502 182 486 Z" fill="#c0203a" opacity=".88"/>'
          '<path d="M374 302 L500 302 L486 492 C484 510 390 510 388 492 Z" fill="url(#glass)"/>'
          '<path d="M386 360 L490 360 L479 486 C477 500 397 500 395 486 Z" fill="#a8172c" opacity=".88"/>'
          '<path d="M566 290 L700 290 L686 492 C684 510 584 510 582 492 Z" fill="url(#glass)"/>'
          '<path d="M578 342 L690 342 L678 486 C676 502 592 502 590 486 Z" fill="#c0203a" opacity=".88"/></g>'
          '<g stroke="#fff" stroke-width="7" fill="none" opacity=".4" stroke-linecap="round">'
          '<path d="M192 300 L182 470 M402 320 L393 470 M598 308 L589 470"/></g>')
    # корица
    s += ('<g stroke="#1b0806" stroke-width="6" stroke-linejoin="round">'
          '<path d="M248 254 L286 254 L270 364 L240 364 Z" fill="#8a5a2a"/>'
          '<path d="M248 254 L286 254 L278 268 L252 268 Z" fill="#a8702f"/>'
          '<path d="M636 268 L670 268 L656 372 L628 372 Z" fill="#8a5a2a"/>'
          '<path d="M636 268 L670 268 L663 282 L640 282 Z" fill="#a8702f"/></g>')
    # бадьян — медленно поворачивается на поверхности
    ar = 6 * A.w(t, 9.0, .1)
    s += (f'<g transform="rotate({ar:.2f} 452 336)">'
          '<path d="M436 322 L452 290 L468 322 L502 326 L476 348 L484 382 L452 364 L420 382'
          ' L428 348 L402 326 Z" fill="#8a5a2a" stroke="#1b0806" stroke-width="5"'
          ' stroke-linejoin="round"/>'
          '<circle cx="452" cy="336" r="8" fill="#c08a4a"/></g>')
    # долька апельсина на краю
    s += ('<g stroke="#1b0806" stroke-width="7">'
          '<path d="M690 300 C690 266 718 244 748 244 C748 278 722 300 690 300 Z" fill="#f0921f"/>'
          '<path d="M698 294 C700 272 718 256 740 254 C738 276 720 292 698 294 Z" fill="#ffb455"/></g>')
    # гранат рядом
    s += ('<g stroke="#1b0806" stroke-width="8">'
          '<circle cx="80" cy="446" r="50" fill="#a8172c"/>'
          '<path d="M80 396 L72 376 L88 380 L80 396 Z" fill="#7a0f20"/></g>'
          '<g fill="#c0203a"><circle cx="64" cy="436" r="9"/><circle cx="94" cy="440" r="8"/>'
          '<circle cx="78" cy="462" r="8"/></g>')
    s += A.smoke(228, 272, t, 2, 150, .8, .3)
    s += A.smoke(434, 288, t * 1.19 + .5, 3, 170, .9, .26)
    s += A.smoke(632, 276, t * 0.91 + 1.4, 2, 140, .8, .24)
    s += A.confetti(t, 12, seed=127)
    return s


def lamb_no(t):
    """То самое мясо, которого в эту ночь не ставят ни в каком виде."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(120, 92, 16, "#ffd45e"), (236, 128, 13, "#ff8c6b"), (56, 166, 12, "#9ae06a")],
               ".35")
    s += tree(846, 298, t, 0.52, 0.55, star=False)
    s += _garland(t, 8)
    s += table(408)
    s += A.candle(102, 330, t, 78, 50, phase=.2)
    s += _plate_oval(470, 452, 300, 62, "#c9b89a", "#e8dac0")
    s += ('<g fill="#4e7a35" stroke="#1b0f07" stroke-width="5">'
          '<ellipse cx="236" cy="448" rx="44" ry="15"/><ellipse cx="704" cy="448" rx="44" ry="15"/></g>')
    # голова барана
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<path d="M352 426 C332 358 372 300 450 286 C534 271 598 306 610 366'
          ' C622 426 578 450 498 454 C436 457 374 452 352 426 Z" fill="#dbd0bd"/>'
          '<path d="M374 326 C312 310 276 262 290 212 C304 164 358 144 400 170'
          ' C362 174 336 198 336 230 C336 270 350 306 388 318 Z" fill="#9c7a4a"/>'
          '<path d="M588 338 C650 324 690 278 680 228 C670 180 618 156 574 180'
          ' C612 186 638 208 638 240 C638 280 624 314 588 326 Z" fill="#8a6b3f"/>'
          '<path d="M372 384 C338 380 310 392 302 412 C326 426 362 420 380 404 Z" fill="#c7bba7"/></g>'
          '<g stroke="#6e5230" stroke-width="5" fill="none" opacity=".8">'
          '<path d="M330 258 C348 238 370 224 390 218 M336 290 C356 268 380 252 400 246"/>'
          '<path d="M632 266 C616 244 596 230 576 224 M628 298 C610 276 590 260 572 254"/></g>')
    if A.blink(t, 5.2, .1):
        s += '<path d="M419 356 L449 356" stroke="#241208" stroke-width="7" stroke-linecap="round"/>'
    else:
        s += ('<ellipse cx="434" cy="356" rx="15" ry="13" fill="#241208"/>'
              '<circle cx="429" cy="352" r="4" fill="#fff" opacity=".6"/>')
    s += ('<path d="M402 410 C420 422 448 422 466 408" stroke="#1b0f07" stroke-width="7"'
          ' fill="none" stroke-linecap="round"/>')
    a = A.sway(t, 6.2, .3, 1.8)
    s += (f'<g transform="rotate({a:.2f} 604 414)">'
          '<g stroke="#4e7a35" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M604 414 L672 392"/><path d="M620 402 L614 382 M640 396 L634 376'
          ' M660 390 L656 370 M624 420 L630 438 M646 412 L652 430"/></g></g>')
    # запрещающий знак — чуть дышит
    k = 1.0 + .018 * A.w(t, 3.1)
    s += (f'<g transform="translate(470,330) scale({k:.4f}) translate(-470,-330)" opacity=".92">'
          '<circle cx="470" cy="340" r="158" fill="none" stroke="#e02a1c" stroke-width="22"/>'
          '<path d="M358 228 L582 452" stroke="#e02a1c" stroke-width="22" stroke-linecap="round"/></g>')
    s += A.snowfall(t, 10, seed=19)
    return s


# ===================== ЧАСТЬ 6: ошибки стола и Восток =====================

def _no_sign(cx, cy, r, t, w=22):
    """Запрещающий знак, который чуть дышит."""
    k = 1.0 + .018 * A.w(t, 3.1)
    return (f'<g transform="translate({cx},{cy}) scale({k:.4f}) translate({-cx},{-cy})" opacity=".92">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e02a1c" stroke-width="{w}"/>'
            f'<path d="M{cx-r*0.707:.0f} {cy-r*0.707:.0f} L{cx+r*0.707:.0f} {cy+r*0.707:.0f}"'
            f' stroke="#e02a1c" stroke-width="{w}" stroke-linecap="round"/></g>')


def salat_mayo(t):
    """Ошибка первая: тяжёлые слоёные салаты под майонезом."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(126, 84, 18, "#ffd45e"), (246, 124, 13, "#ff8c6b"), (54, 158, 12, "#9ae06a")])
    s += tree(856, 276, t, 0.48, 0.4, star=False)
    s += _garland(t, 12)
    s += table(330)
    # три салатницы, слоёные, с майонезной шапкой
    for i, (cx, rx, ry) in enumerate(((210, 140, 50), (470, 158, 56), (726, 132, 46))):
        base = 470 - i % 2 * 8
        s += (f'<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
              f'<path d="M{cx-rx} {base-70} L{cx+rx} {base-70} L{cx+rx-14} {base} L{cx-rx+14} {base} Z"'
              ' fill="#e4d4b6"/></g>')
        # слои
        for k, (col, dy) in enumerate((("#c0203a", 56), ("#e9c98a", 40), ("#6e8f3a", 24))):
            s += (f'<path d="M{cx-rx+6+k*4} {base-dy} L{cx+rx-6-k*4} {base-dy}'
                  f' L{cx+rx-10-k*4} {base-dy+14} L{cx-rx+10+k*4} {base-dy+14} Z" fill="{col}"'
                  ' stroke="#1b0f07" stroke-width="4"/>')
        # майонезная шапка с потёками
        s += (f'<path d="M{cx-rx} {base-70} C{cx-rx+10} {base-108} {cx+rx-10} {base-108} {cx+rx} {base-70}'
              f' C{cx+rx*0.5} {base-58} {cx-rx*0.5} {base-58} {cx-rx} {base-70} Z"'
              ' fill="#f8f5ee" stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>')
        d = 6 * A.w(t, 5.0 + i, i * .4)
        s += (f'<path d="M{cx-rx*0.5} {base-62} C{cx-rx*0.5+d} {base-44} {cx-rx*0.5-d} {base-30}'
              f' {cx-rx*0.5} {base-16}" stroke="#f8f5ee" stroke-width="10" fill="none"'
              ' stroke-linecap="round" opacity=".9"/>')
    # ложка воткнута
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<path d="M498 408 L546 318" stroke="#cfc8bd" stroke-width="13" fill="none"/>'
          '<ellipse cx="550" cy="306" rx="19" ry="26" fill="#cfc8bd" transform="rotate(20 550 306)"/></g>')
    s += A.confetti(t, 10, seed=131)
    return s


def two_floors(t):
    """Ошибка вторая: стол на количество — посуда в два этажа."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(840, 88, 17, "#ffd45e"), (734, 126, 13, "#ff8c6b"), (906, 158, 12, "#9ae06a")])
    s += tree(118, 282, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(300)
    # нижний ярус: тарелки впритык, налезают друг на друга
    for i, (cx, rx) in enumerate(((150, 104), (330, 110), (514, 106), (690, 100), (848, 92))):
        s += (f'<g stroke="#1b0f07" stroke-width="8">'
              f'<ellipse cx="{cx}" cy="482" rx="{rx}" ry="{rx*0.3:.0f}" fill="#dccbab"/>'
              f'<ellipse cx="{cx}" cy="476" rx="{rx*0.78:.0f}" ry="{rx*0.21:.0f}" fill="#f2ead6"/></g>')
        col = ("#b4541c", "#6e8f3a", "#c0203a", "#d8982a", "#7b4a6e")[i]
        s += (f'<path d="M{cx-rx*0.6:.0f} 474 C{cx-rx*0.4:.0f} 452 {cx+rx*0.4:.0f} 452'
              f' {cx+rx*0.6:.0f} 474 Z" fill="{col}" stroke="#1b0f07" stroke-width="6"/>')
    # второй ярус: миски стоят прямо на тарелках, криво
    for i, (cx, rx, rot) in enumerate(((236, 74, -5), (430, 80, 4), (612, 70, -6), (790, 64, 5))):
        s += _bowl(cx, 410, rx, int(rx * 0.34), ("#6e8f3a", "#c0203a", "#d8982a", "#b4541c")[i],
                   heap=1.0, rot=rot)
    # третий этаж: одинокая тарелка сверху, качается
    a = A.sway(t, 4.2, .0, 2.4)
    s += (f'<g transform="rotate({a:.2f} 470 352)">'
          '<g stroke="#1b0f07" stroke-width="8">'
          '<ellipse cx="470" cy="352" rx="86" ry="26" fill="#dccbab"/>'
          '<ellipse cx="470" cy="346" rx="66" ry="18" fill="#f2ead6"/></g>'
          '<path d="M424 344 C438 322 502 322 516 344 Z" fill="#c0203a" stroke="#1b0f07"'
          ' stroke-width="6"/></g>')
    # бокал, которому некуда встать — на самом краю
    s += _goblet(898, 430, t, .9, .3)
    s += A.confetti(t, 10, seed=137)
    return s


def meat_only(t):
    """Ошибка третья: стол, накрытый одним мясом."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(130, 80, 18, "#ffd45e"), (252, 122, 14, "#ff8c6b"), (58, 156, 12, "#9ae06a")], ".3")
    s += tree(850, 274, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(312)
    # блюдо с нарезками слева
    s += ('<g stroke="#1b0f07" stroke-width="8">'
          '<ellipse cx="176" cy="452" rx="150" ry="44" fill="#cfbf9f"/>'
          '<ellipse cx="176" cy="444" rx="126" ry="34" fill="#ece0c6"/></g>')
    for i in range(6):
        x = 78 + i * 38
        s += (f'<ellipse cx="{x}" cy="{432+(i%2)*10}" rx="30" ry="13" fill="#c4556a"'
              ' stroke="#1b0f07" stroke-width="5" transform="rotate(-12 %d %d)"/>' % (x, 432 + (i % 2) * 10))
        s += (f'<ellipse cx="{x}" cy="{432+(i%2)*10}" rx="18" ry="7" fill="#e08a96" opacity=".7"/>')
    # колбаса кругом в центре
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<path d="M372 436 C372 390 430 362 486 368 C544 374 580 410 572 448'
          ' C564 484 508 498 452 490 C404 483 374 464 372 436 Z" fill="#8c2130"/>'
          '<path d="M398 430 C402 400 446 382 490 388 C530 393 556 416 550 444"'
          ' stroke="#b03c4a" stroke-width="7" fill="none"/></g>')
    s += '<g fill="#e4d4b6" opacity=".75">'
    for cx, cy, r in ((420, 420, 7), (470, 406, 6), (516, 424, 7), (452, 452, 6), (512, 462, 6)):
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
    s += '</g>'
    # холодец справа
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<path d="M672 492 L672 400 C672 386 836 386 836 400 L836 492 Z" fill="#e9dfc4"'
          ' opacity=".9"/>'
          '<ellipse cx="754" cy="400" rx="82" ry="18" fill="#f3ecd8"/></g>'
          '<g fill="#b4541c" stroke="#1b0f07" stroke-width="4" opacity=".9">'
          '<ellipse cx="720" cy="440" rx="24" ry="12"/><ellipse cx="790" cy="458" rx="20" ry="10"/>'
          '<ellipse cx="752" cy="470" rx="18" ry="9"/></g>'
          '<g stroke="#4e7a35" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8">'
          '<path d="M700 420 L716 410 M800 428 L816 418"/></g>')
    # запечённое сзади по центру
    s += _roast(470, 350, .8, rot=-3)
    s += A.confetti(t, 10, seed=149)
    return s


def lamb_dishes(t):
    """То, чего в эту ночь не ставят: шашлык, плов, запечённая нога."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(120, 92, 16, "#ffd45e"), (236, 128, 13, "#ff8c6b"), (56, 166, 12, "#9ae06a")], ".3")
    s += tree(858, 292, t, 0.44, 0.4, star=False)
    s += _garland(t, 8)
    s += table(356)
    # шашлык: неровные куски с подпалинами, на шампуре с кольцом
    s += ('<path d="M60 436 L332 400" stroke="#cfc8bd" stroke-width="10" stroke-linecap="round"/>'
          '<circle cx="56" cy="437" r="13" fill="none" stroke="#cfc8bd" stroke-width="9"/>')
    for i in range(4):
        x = 116 + i * 60
        y = 430 - i * 8
        s += (f'<path d="M{x-30} {y-4} C{x-36} {y-34} {x-6} {y-44} {x+14} {y-38}'
              f' C{x+38} {y-32} {x+34} {y+6} {x+16} {y+18} C{x-6} {y+30} {x-26} {y+16} {x-30} {y-4} Z"'
              ' fill="#8d3a12" stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>')
        s += (f'<path d="M{x-18} {y-18} C{x-6} {y-26} {x+8} {y-24} {x+18} {y-14}"'
              ' stroke="#b4541c" stroke-width="5" fill="none" opacity=".85"/>'
              f'<path d="M{x-14} {y+4} C{x-2} {y-2} {x+12} {y} {x+20} {y+8}"'
              ' stroke="#5e2a08" stroke-width="4" fill="none" opacity=".7"/>')
        if i < 3:
            s += (f'<rect x="{x+26}" y="{y-14}" width="14" height="14" rx="4" fill="#e9c98a"'
                  ' stroke="#1b0f07" stroke-width="5"/>')
    # плов: горка риса с рисинками, морковь соломкой, куски мяса
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<path d="M352 498 C352 430 404 392 480 392 C556 392 608 430 608 498 Z" fill="#edd49c"/>'
          '<ellipse cx="480" cy="392" rx="128" ry="30" fill="#f4e3bb"/></g>')
    s += '<g stroke="#d9bd84" stroke-width="4" stroke-linecap="round" opacity=".9">'
    for k in range(16):
        rx = 372 + (k * 37) % 216
        ry = 410 + (k * 29) % 76
        s += f'<path d="M{rx} {ry} L{rx+13} {ry-5}"/>'
    s += '</g>'
    s += '<g fill="#e07f23" stroke="#1b0f07" stroke-width="3" opacity=".95">'
    for k, (cx, cy, rot) in enumerate(((414, 430, -18), (486, 418, 10), (546, 440, -8),
                                       (444, 466, 14), (520, 470, -14))):
        s += (f'<rect x="{cx-18}" y="{cy-5}" width="36" height="10" rx="4"'
              f' transform="rotate({rot} {cx} {cy})"/>')
    s += '</g>'
    s += ('<g fill="#8d3a12" stroke="#1b0f07" stroke-width="5">'
          '<path d="M430 390 C430 372 470 366 478 384 C484 398 456 408 440 402 Z"/>'
          '<path d="M506 386 C508 368 548 364 554 382 C558 396 530 404 516 398 Z"/></g>')
    # запечённая нога: мясистая, с костью и манжетой
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<ellipse cx="768" cy="492" rx="150" ry="34" fill="#cfbf9f"/>'
          '<path d="M650 470 C638 414 682 372 748 372 C808 372 848 404 850 442'
          ' C852 474 806 492 744 492 C698 492 660 486 650 470 Z" fill="#8d3a12"/>'
          '<path d="M838 420 C866 402 890 404 896 420 C890 440 862 448 840 440 Z" fill="#a84c18"/>'
          '<rect x="884" y="398" width="28" height="26" rx="9" fill="#f6f1e4"/></g>'
          '<g stroke="#5e2a08" stroke-width="5" fill="none" opacity=".8">'
          '<path d="M686 400 L676 460 M730 384 L726 476 M776 386 L780 478 M820 404 L828 462"/></g>'
          '<path d="M676 408 C716 388 790 386 830 406" stroke="#b4541c" stroke-width="9"'
          ' fill="none" opacity=".6"/>')
    s += A.smoke(190, 392, t, 2, 120, .8, .2)
    s += _no_sign(470, 330, 156, t, 22)
    s += A.snowfall(t, 10, seed=23)
    return s


def koza_head_table(t):
    """Гостья во главе стола, а на блюде перед ней — её родня."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(132, 86, 17, "#ffd45e"), (250, 124, 13, "#ff8c6b"), (60, 158, 12, "#9ae06a")])
    s += window(690, 92, 190, 150, t)
    s += tree(128, 286, t, 0.46, 0.5, star=True)
    s += _garland(t, 10)
    # стол уходит вглубь: трапеция
    s += ('<path d="M196 384 L764 384 L920 540 L40 540 Z" fill="url(#cloth)"'
          ' stroke="#8c2d12" stroke-width="6"/>'
          '<path d="M196 378 L764 378 L776 396 L184 396 Z" fill="#c6523a"/>')
    # коза во главе: голова над столом, чуть повёрнута
    s += f'<g transform="translate(480,214) scale(0.50) translate(-480,-214)">'
    s += _koza_head(t, fire=True)
    s += '</g>'
    # свечи по краям
    s += A.candle(132, 404, t, 62, 44, phase=.2, s=.8)
    s += A.candle(836, 410, t, 58, 42, phase=.6, s=.78)
    # блюдо перед ней — баранья голова
    s += ('<g stroke="#1b0f07" stroke-width="9">'
          '<ellipse cx="480" cy="486" rx="230" ry="52" fill="#c9b89a"/>'
          '<ellipse cx="480" cy="474" rx="196" ry="40" fill="#e8dac0"/></g>')
    s += ('<g transform="translate(480,448) scale(0.70) translate(-480,-448)">'
          '<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<path d="M362 452 C342 384 382 326 460 312 C544 297 608 332 620 392'
          ' C632 452 588 476 508 480 C446 483 384 478 362 452 Z" fill="#dbd0bd"/>'
          '<path d="M384 352 C322 336 286 288 300 238 C314 190 368 170 410 196'
          ' C372 200 346 224 346 256 C346 296 360 332 398 344 Z" fill="#9c7a4a"/>'
          '<path d="M598 364 C660 350 700 304 690 254 C680 206 628 182 584 206'
          ' C622 212 648 234 648 266 C648 306 634 340 598 352 Z" fill="#8a6b3f"/></g>'
          '<ellipse cx="444" cy="382" rx="15" ry="13" fill="#241208"/></g>')
    s += ('<g fill="#4e7a35" stroke="#1b0f07" stroke-width="5">'
          '<ellipse cx="292" cy="494" rx="44" ry="15"/><ellipse cx="668" cy="494" rx="44" ry="15"/></g>')
    s += A.confetti(t, 10, seed=151)
    return s


def round_fruits(t):
    """Восток любит круглые фрукты: апельсины, мандарины, яблоки."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(128, 86, 18, "#ffd45e"), (250, 124, 13, "#ff8c6b"), (56, 158, 12, "#9ae06a")])
    s += tree(852, 278, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(322)
    # большое плоское блюдо, фрукты выложены кругом
    s += ('<g stroke="#1b0f07" stroke-width="9">'
          '<ellipse cx="470" cy="452" rx="330" ry="86" fill="#cfbf9f"/>'
          '<ellipse cx="470" cy="440" rx="292" ry="70" fill="#f2ead6"/></g>')
    import math as _m
    for i in range(9):
        ang = _m.pi * (i / 8.0)
        cx = 470 + int(238 * _m.cos(_m.pi - ang))
        cy = 426 + int(44 * _m.sin(ang))
        kind = i % 3
        r = (40, 33, 37)[kind]
        col = ("#f0921f", "#ef9a2e", "#c0203a")[kind]
        inner = ("#ffb455", "#ffc06a", "#d8465c")[kind]
        s += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="#1b0f07" stroke-width="7"/>'
              f'<circle cx="{cx-r//4}" cy="{cy-r//3}" r="{r//3}" fill="{inner}" opacity=".75"/>')
        if kind == 2:
            s += (f'<path d="M{cx} {cy-r} L{cx-4} {cy-r-16} L{cx+8} {cy-r-12} Z" fill="#4e7a35"'
                  ' stroke="#1b0f07" stroke-width="4"/>')
        else:
            s += (f'<path d="M{cx+r//3} {cy-r+4} C{cx+r} {cy-r-14} {cx+r+16} {cy-r} {cx+r+6} {cy-r+12}"'
                  ' stroke="#4e7a35" stroke-width="6" fill="none" stroke-linecap="round"/>')
    # пара долек мандарина впереди
    s += ('<g stroke="#1b0f07" stroke-width="6">'
          '<path d="M398 496 C398 474 420 458 442 458 C442 482 422 496 398 496 Z" fill="#f0921f"/>'
          '<path d="M510 498 C510 476 532 460 554 460 C554 484 534 498 510 498 Z" fill="#ef9a2e"/></g>')
    s += A.confetti(t, 11, seed=163)
    return s


def pelmeni_gold(t):
    """Пельмени как старинные золотые слитки — пожелание богатства."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(840, 84, 17, "#ffd45e"), (736, 124, 13, "#ff8c6b"), (904, 156, 12, "#9ae06a")])
    s += tree(116, 280, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(330)
    s += ('<g stroke="#1b0f07" stroke-width="9">'
          '<ellipse cx="470" cy="456" rx="300" ry="76" fill="#cfbf9f"/>'
          '<ellipse cx="470" cy="444" rx="262" ry="62" fill="#f2ead6"/></g>')
    # ПЕЛЬМЕНИ: тесто, защип гребешком и загнутые уголки. Раньше здесь
    # лежали золотые слитки — слиток пельменем не читался (его правка 02.11)
    for i, (cx, cy, sc, rot, bright) in enumerate(((298, 438, 1.0, -6, False),
                                                   (418, 418, 1.06, 4, True),
                                                   (542, 428, 1.0, -3, True),
                                                   (656, 448, .94, 7, False),
                                                   (358, 480, .92, 5, True),
                                                   (486, 486, .96, -5, False),
                                                   (598, 482, .9, 3, True))):
        dough = "#f3e6c6" if bright else "#e8d8b2"
        edge = "#e0cb9e" if bright else "#d4bd8d"
        s += f'<g transform="translate({cx},{cy}) rotate({rot}) scale({sc})">'
        # брюшко с начинкой
        s += ('<path d="M-58 16 C-62 -14 -32 -34 0 -34 C32 -34 62 -14 58 16'
              ' C34 30 -34 30 -58 16 Z"'
              f' fill="{dough}" stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>')
        # загнутые уголки — пельмень, а не вареник
        s += ('<path d="M-58 16 C-74 10 -78 -8 -66 -18 C-56 -8 -58 4 -48 14 Z"'
              f' fill="{edge}" stroke="#1b0f07" stroke-width="7" stroke-linejoin="round"/>'
              '<path d="M58 16 C74 10 78 -8 66 -18 C56 -8 58 4 48 14 Z"'
              f' fill="{edge}" stroke="#1b0f07" stroke-width="7" stroke-linejoin="round"/>')
        # ЗАЩИП ГРЕБЕШКОМ по верхнему краю — главный признак пельменя
        s += f'<path d="M-50 -14 C-30 -30 30 -30 50 -14" stroke="{edge}" stroke-width="13" fill="none" stroke-linecap="round"/>'
        s += '<g stroke="#1b0f07" stroke-width="5" fill="none" stroke-linecap="round">'
        for k, (px, py) in enumerate(((-40, -20), (-24, -26), (-8, -29), (8, -29), (24, -26), (40, -20))):
            s += f'<path d="M{px} {py+12} L{px} {py+1}"/>'
        s += ('<path d="M-50 -14 C-30 -30 30 -30 50 -14"/></g>')
        # блик теста и тень на блюде
        s += ('<path d="M-34 2 C-18 -6 10 -8 28 -2" stroke="#fffaec" stroke-width="7"'
              ' fill="none" stroke-linecap="round" opacity=".6"/>'
              '<path d="M-48 18 C-24 26 24 26 48 18" stroke="#b9a075" stroke-width="5"'
              ' fill="none" opacity=".55"/>')
        s += '</g>'
        if bright:
            o = .25 + .35 * (0.5 + 0.5 * A.w(t, 2.6, i * .3))
            s += f'<circle cx="{cx-20}" cy="{cy-10}" r="7" fill="#fff6cf" opacity="{o:.2f}"/>'
    # два золотых слитка рядом с блюдом — та самая форма, о которой речь
    for gx, gy, gs in ((132, 498, .62), (826, 506, .56)):
        s += (f'<g transform="translate({gx},{gy}) scale({gs})">'
              '<path d="M-62 26 C-58 2 -30 -8 0 -8 C30 -8 58 2 62 26 C40 34 -40 34 -62 26 Z"'
              ' fill="#edc75c" stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
              '<path d="M-62 26 C-78 14 -80 -10 -64 -24 C-50 -14 -52 6 -44 20 Z"'
              ' fill="#f8e39a" stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
              '<path d="M62 26 C78 14 80 -10 64 -24 C50 -14 52 6 44 20 Z"'
              ' fill="#f8e39a" stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
              '<path d="M-38 6 C-18 -2 18 -2 38 6" stroke="#fdf2c6" stroke-width="7"'
              ' fill="none" stroke-linecap="round" opacity=".85"/></g>')
    s += A.smoke(470, 400, t, 3, 140, .9, .24)
    s += A.confetti(t, 11, seed=167)
    return s


def pear_no(t):
    """Груша на праздничном столе — слово звучит как «расставание»."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(126, 90, 16, "#ffd45e"), (240, 126, 13, "#ff8c6b"), (58, 164, 12, "#9ae06a")], ".3")
    s += tree(852, 286, t, 0.44, 0.4, star=False)
    s += _garland(t, 8)
    s += table(368)
    s += ('<g stroke="#1b0f07" stroke-width="9">'
          '<ellipse cx="470" cy="470" rx="236" ry="52" fill="#c9b89a"/>'
          '<ellipse cx="470" cy="458" rx="200" ry="40" fill="#e8dac0"/></g>')
    for cx, cy, sc in ((372, 402, .92), (470, 388, 1.0), (568, 404, .88)):
        s += (f'<g transform="translate({cx},{cy}) scale({sc})">'
              '<path d="M0 -64 C14 -64 18 -46 10 -34 C44 -22 60 14 40 42'
              ' C24 64 -24 64 -40 42 C-60 14 -44 -22 -10 -34 C-18 -46 -14 -64 0 -64 Z"'
              ' fill="#c9c84a" stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>'
              '<path d="M-22 10 C-14 -8 10 -14 24 -4" stroke="#e2e08a" stroke-width="7"'
              ' fill="none" stroke-linecap="round"/>'
              '<path d="M0 -64 C2 -82 14 -92 26 -90" stroke="#6b3f1c" stroke-width="8"'
              ' fill="none" stroke-linecap="round"/>'
              '<path d="M8 -80 C24 -94 44 -90 48 -76 C40 -66 18 -68 8 -80 Z" fill="#4e7a35"'
              ' stroke="#1b0f07" stroke-width="5"/></g>')
    s += _no_sign(470, 404, 172, t, 22)
    s += A.snowfall(t, 9, seed=29)
    return s


def white_no(t):
    """Совсем белое на столе — на Востоке цвет траура."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(840, 88, 16, "#ffd45e"), (730, 126, 12, "#ff8c6b")], ".26")
    s += tree(112, 286, t, 0.44, 0.4, star=False)
    s += _garland(t, 10)
    # белый островок посреди красной скатерти: иначе кадр читается как пустой
    s += table(352)
    s += ('<path d="M96 368 L864 368 L904 524 L56 524 Z" fill="#eceadf"'
          ' stroke="#b9b5a6" stroke-width="8"/>'
          '<path d="M96 368 L864 368 L870 390 L90 390 Z" fill="#f8f7f1"/>')
    s += ('<g stroke="#8d8a7e" stroke-width="7">'
          '<ellipse cx="268" cy="448" rx="124" ry="34" fill="#f6f5ef"/>'
          '<ellipse cx="268" cy="438" rx="98" ry="25" fill="#fdfdfa"/>'
          '<ellipse cx="676" cy="458" rx="132" ry="36" fill="#f6f5ef"/>'
          '<ellipse cx="676" cy="448" rx="104" ry="27" fill="#fdfdfa"/></g>')
    s += ('<g stroke="#8d8a7e" stroke-width="7" stroke-linejoin="round">'
          '<path d="M420 486 L420 410 C420 398 520 398 520 410 L520 486 Z" fill="#f8f7f1"/>'
          '<ellipse cx="470" cy="410" rx="50" ry="12" fill="#fdfdfa"/></g>')
    s += ('<g stroke="#8d8a7e" stroke-width="7">'
          '<rect x="150" y="318" width="22" height="84" rx="5" fill="#fbfaf4"/>'
          '<rect x="800" y="330" width="22" height="76" rx="5" fill="#fbfaf4"/></g>'
          '<g fill="#cfcabb" opacity=".8">'
          '<ellipse cx="268" cy="474" rx="118" ry="12"/><ellipse cx="676" cy="486" rx="126" ry="12"/></g>')
    s += _no_sign(470, 420, 182, t, 24)
    s += A.snowfall(t, 12, seed=31)
    return s


def calendar_feb(t):
    """Год хозяйки начинается не 31 декабря, а 6 февраля 2027-го."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(130, 84, 18, "#ffd45e"), (250, 124, 13, "#ff8c6b"), (58, 156, 12, "#9ae06a")])
    s += _garland(t, 10)
    s += table(462)
    # два листка календаря: зачёркнутый декабрь и горящий февраль
    for i, (cx, head, day, mon, warm) in enumerate(
            ((268, "#8a3c10", "31", "ДЕКАБРЯ", False), (686, "#c0203a", "6", "ФЕВРАЛЯ", True))):
        s += (f'<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
              f'<rect x="{cx-150}" y="150" width="300" height="300" rx="18" fill="#f4efe3"/>'
              f'<path d="M{cx-150} 150 L{cx+150} 150 L{cx+150} 226 L{cx-150} 226 Z" fill="{head}"/></g>')
        s += (f'<g stroke="#1b0f07" stroke-width="7">'
              f'<circle cx="{cx-92}" cy="150" r="11" fill="#c9922f"/>'
              f'<circle cx="{cx+92}" cy="150" r="11" fill="#c9922f"/></g>')
        s += (f'<text x="{cx}" y="{372}" font-family="DejaVu Serif" font-size="150"'
              f' font-weight="bold" fill="#1a140e" text-anchor="middle">{day}</text>')
        s += (f'<text x="{cx}" y="{424}" font-family="DejaVu Sans" font-size="32"'
              f' letter-spacing="6" fill="#6b6155" text-anchor="middle">{mon}</text>')
        if warm:
            g = .45 + .35 * (0.5 + 0.5 * A.w(t, 2.4))
            s += (f'<circle cx="{cx}" cy="300" r="210" fill="#e07f23" opacity="{g*0.18:.2f}"/>')
        else:
            s += (f'<path d="M{cx-120} 420 L{cx+120} 196" stroke="#8a3c10" stroke-width="14"'
                  ' stroke-linecap="round" opacity=".8"/>')
    s += A.confetti(t, 12, seed=173)
    return s


def lanterns(t):
    """Китайцы встречают её в феврале — с фонарями и фейерверками."""
    s = '<rect width="960" height="540" fill="url(#night)"/>'
    # фейерверк: лучи из двух точек, вспыхивают по очереди
    import math as _m
    for j, (fx, fy, per, col) in enumerate(((250, 150, 3.4, "#ffd45e"), (690, 118, 4.1, "#ff8c6b"))):
        ph = (t / per + j * .4) % 1.0
        rr = 40 + ph * 150
        op = max(0.0, 1.0 - ph) * .9
        s += f'<g stroke="{col}" stroke-width="5" opacity="{op:.2f}" stroke-linecap="round">'
        for k in range(12):
            a = 2 * _m.pi * k / 12
            s += (f'<path d="M{fx + _m.cos(a)*rr*0.45:.0f} {fy + _m.sin(a)*rr*0.45:.0f}'
                  f' L{fx + _m.cos(a)*rr:.0f} {fy + _m.sin(a)*rr:.0f}"/>')
        s += '</g>'
        s += f'<circle cx="{fx}" cy="{fy}" r="{6+8*(1-ph):.0f}" fill="{col}" opacity="{op:.2f}"/>'
    # ряд бумажных фонарей, качаются
    for i, (x, y, sc, ph) in enumerate(((140, 180, 1.0, .0), (330, 150, 1.16, .3),
                                        (520, 176, 1.04, .6), (700, 146, 1.2, .15),
                                        (860, 188, .94, .45))):
        a = A.sway(t, 5.6 + i * .4, ph, 2.2)
        s += (f'<g transform="rotate({a:.2f} {x} {y-80}) translate({x},{y}) scale({sc})">'
              '<path d="M0 -80 L0 -46" stroke="#8a6a3a" stroke-width="5"/>'
              '<ellipse cx="0" cy="0" rx="46" ry="54" fill="#d6202f" stroke="#1b0f07"'
              ' stroke-width="8"/>'
              '<rect x="-20" y="-60" width="40" height="16" rx="5" fill="#c9922f"'
              ' stroke="#1b0f07" stroke-width="6"/>'
              '<rect x="-20" y="46" width="40" height="16" rx="5" fill="#c9922f"'
              ' stroke="#1b0f07" stroke-width="6"/>'
              '<g stroke="#8c2130" stroke-width="4" opacity=".7">'
              '<path d="M-22 -44 C-28 0 -28 12 -22 44 M0 -50 L0 50 M22 -44 C28 0 28 12 22 44"/></g>'
              '<g stroke="#c9922f" stroke-width="5" stroke-linecap="round">'
              '<path d="M-14 62 L-16 86 M0 62 L0 92 M14 62 L16 86"/></g>'
              '<ellipse cx="0" cy="0" rx="70" ry="78" fill="#ffb43c" opacity=".16"/></g>')
    # крыша с изогнутым краем внизу — намёк на восточный город
    s += ('<path d="M0 470 C120 436 240 436 330 456 C420 476 540 476 630 456'
          ' C720 436 850 436 960 470 L960 540 L0 540 Z" fill="#2a150c"/>'
          '<path d="M0 470 C120 436 240 436 330 456 C420 476 540 476 630 456'
          ' C720 436 850 436 960 470" stroke="#1b0f07" stroke-width="9" fill="none"/>')
    s += A.snowfall(t, 14, seed=37)
    return s


def finale_2027(t):
    """Финал после озвучки: башенные часы бьют полночь, расходится звон,
    и цифра 2027 вырастает на весь кадр. Его просьба 02.11: пара секунд
    музыки с курантами в самом конце."""
    import math as _m
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(132, 92, 19, "#ffd45e"), (250, 128, 14, "#ff8c6b"),
                (58, 166, 13, "#9ae06a"), (820, 104, 16, "#ffd45e"),
                (900, 168, 12, "#ff8c6b")], ".34")
    s += _garland(t, 12)
    s += tree(110, 470, t, 0.62, 0.5, star=True)
    s += tree(852, 470, t, 0.58, 0.45, star=True)
    # часы: стрелки сходятся на двенадцати
    cx, cy, R = 480, 188, 116
    s += (f'<circle cx="{cx}" cy="{cy}" r="{R+18}" fill="#6b3f1c" stroke="#1b0f07" stroke-width="9"/>'
          f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#f4efe3" stroke="#1b0f07" stroke-width="8"/>')
    s += '<g stroke="#1a140e" stroke-width="6" stroke-linecap="round">'
    for k in range(12):
        a = 2 * _m.pi * k / 12
        r1 = R - (22 if k % 3 == 0 else 13)
        s += (f'<path d="M{cx + _m.cos(a)*r1:.0f} {cy + _m.sin(a)*r1:.0f}'
              f' L{cx + _m.cos(a)*(R-5):.0f} {cy + _m.sin(a)*(R-5):.0f}"/>')
    s += '</g>'
    # стрелки подходят к двенадцати слева и сходятся на ней
    k = min(1.0, t / 2.2)
    ang = _m.radians(-16.0 * (1 - k))
    for ln, wd in ((R - 38, 12), (R - 20, 8)):
        s += (f'<path d="M{cx} {cy} L{cx + _m.sin(ang)*ln:.0f} {cy - _m.cos(ang)*ln:.0f}"'
              f' stroke="#1a140e" stroke-width="{wd}" stroke-linecap="round"/>')
    s += (f'<path d="M{cx} {cy} L{cx + _m.sin(ang)*(R-26):.0f} {cy - _m.cos(ang)*(R-26):.0f}"'
          ' stroke="#c0203a" stroke-width="4" stroke-linecap="round"/>'
          f'<circle cx="{cx}" cy="{cy}" r="11" fill="#c0203a" stroke="#1a140e" stroke-width="5"/>')
    # звон расходится кругами
    for i in range(4):
        ph = (t / 1.5 + i * .25) % 1.0
        op = max(0.0, 1 - ph) * .45
        s += (f'<circle cx="{cx}" cy="{cy}" r="{R + 30 + ph * 150:.0f}" fill="none"'
              f' stroke="#f6c84e" stroke-width="4" opacity="{op:.2f}"/>')
    # ЦИФРА РАСТЁТ: от маленькой до полного кадра, с лёгким перелётом
    gk = min(1.0, t / 1.9)
    sc = 0.22 + 0.86 * (1 - (1 - gk) ** 3)
    if gk >= 1.0:
        sc = 1.08 + 0.02 * A.w(t, 3.0)
    gy = 452
    s += (f'<g transform="translate(480,{gy}) scale({sc:.3f})">'
          f'<ellipse cx="0" cy="-26" rx="300" ry="120" fill="#e07f23" opacity="{0.16*gk:.2f}"/>'
          '<text x="6" y="12" font-family="DejaVu Serif" font-size="176" font-weight="bold"'
          ' fill="#1b0f07" text-anchor="middle" opacity=".55">2027</text>'
          '<text x="0" y="0" font-family="DejaVu Serif" font-size="176" font-weight="bold"'
          ' fill="#f6c84e" text-anchor="middle">2027</text>'
          '<text x="0" y="0" font-family="DejaVu Serif" font-size="176" font-weight="bold"'
          ' fill="none" stroke="#1b0f07" stroke-width="7" text-anchor="middle">2027</text>'
          '</g>')
    s += A.confetti(t, 34, seed=2027)
    s += A.snowfall(t, 26, seed=77) if hasattr(A, "snowfall") else ""
    return s


def kuranty(t):
    """Куранты бьют: у нас свой праздник, тридцать первого."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(130, 96, 18, "#ffd45e"), (248, 130, 14, "#ff8c6b"), (60, 168, 12, "#9ae06a")])
    s += _garland(t, 10)
    s += tree(126, 318, t, 0.5, 0.5, star=True)
    s += table(430)
    # башенные часы крупно
    cx, cy, R = 560, 262, 150
    s += (f'<circle cx="{cx}" cy="{cy}" r="{R+22}" fill="#6b3f1c" stroke="#1b0f07" stroke-width="10"/>'
          f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#f4efe3" stroke="#1b0f07" stroke-width="9"/>')
    import math as _m
    s += '<g stroke="#1a140e" stroke-width="7" stroke-linecap="round">'
    for k in range(12):
        a = 2 * _m.pi * k / 12
        r1 = R - (26 if k % 3 == 0 else 16)
        s += (f'<path d="M{cx + _m.cos(a)*r1:.0f} {cy + _m.sin(a)*r1:.0f}'
              f' L{cx + _m.cos(a)*(R-6):.0f} {cy + _m.sin(a)*(R-6):.0f}"/>')
    s += '</g>'
    # ДО полуночи: все стрелки СЛЕВА от двенадцати и подходят к ней.
    # Раньше секундная уходила вправо — читалось, что полночь уже прошла
    # (его правка 02.11).
    ha = _m.radians(-6.0)
    ma = _m.radians(-3.0)
    s += (f'<path d="M{cx} {cy} L{cx + _m.sin(ha)*(R-44):.0f} {cy - _m.cos(ha)*(R-44):.0f}"'
          ' stroke="#1a140e" stroke-width="13" stroke-linecap="round"/>'
          f'<path d="M{cx} {cy} L{cx + _m.sin(ma)*(R-24):.0f} {cy - _m.cos(ma)*(R-24):.0f}"'
          ' stroke="#1a140e" stroke-width="9" stroke-linecap="round"/>')
    sa = _m.radians(max(-26.0 + 7.0 * t, -4.0))
    s += (f'<path d="M{cx} {cy} L{cx + _m.sin(sa)*(R-30):.0f} {cy - _m.cos(sa)*(R-30):.0f}"'
          ' stroke="#c0203a" stroke-width="5" stroke-linecap="round"/>'
          f'<circle cx="{cx}" cy="{cy}" r="12" fill="#c0203a" stroke="#1a140e" stroke-width="5"/>')
    # звон: расходящиеся дуги
    for k in range(3):
        ph = (t / 1.6 + k * .33) % 1.0
        op = max(0.0, (1 - ph)) * .4
        rr = R + 40 + ph * 90
        s += (f'<circle cx="{cx}" cy="{cy}" r="{rr:.0f}" fill="none" stroke="#f6c84e"'
              f' stroke-width="4" opacity="{op:.2f}"/>')
    # бокалы внизу
    s += _goblet(300, 500, t, 1.0, .0)
    s += _goblet(372, 508, t, .92, .4)
    s += _goblet(800, 504, t, .96, .7)
    s += A.confetti(t, 20, seed=179)
    return s


def koza_figure(t):
    """Деревянная фигурка козы между тарелками — знак внимания."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(132, 88, 17, "#ffd45e"), (252, 126, 13, "#ff8c6b"), (58, 160, 12, "#9ae06a")])
    s += tree(856, 282, t, 0.44, 0.4, star=False)
    s += _garland(t, 10)
    s += table(350)
    # две тарелки по краям, фигурка между ними
    s += ('<g stroke="#1b0f07" stroke-width="8">'
          '<ellipse cx="150" cy="470" rx="130" ry="36" fill="#dccbab"/>'
          '<ellipse cx="150" cy="462" rx="104" ry="26" fill="#f2ead6"/>'
          '<ellipse cx="820" cy="478" rx="136" ry="38" fill="#dccbab"/>'
          '<ellipse cx="820" cy="470" rx="108" ry="28" fill="#f2ead6"/></g>')
    s += _bunch(300, 300, t, .8, .25)
    # ФИГУРКА КОЗЫ, которая читается козой: тонкие прямые ноги, высокая
    # шея, клиновидная морда, рога назад, борода и короткий хвост торчком.
    # Прежняя была сплошным комом и козой не читалась (его правка 02.11).
    s += ('<g transform="translate(470,396)">'
          # подставка
          '<path d="M-110 92 L110 92 L94 114 L-94 114 Z" fill="#8a5c2a" stroke="#1b0f07"'
          ' stroke-width="8" stroke-linejoin="round"/>'
          # четыре тонкие прямые ноги с копытцами
          '<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<rect x="-62" y="26" width="16" height="66" rx="4" fill="#96631f"/>'
          '<rect x="-34" y="30" width="16" height="62" rx="4" fill="#8a5c2a"/>'
          '<rect x="34" y="28" width="16" height="64" rx="4" fill="#96631f"/>'
          '<rect x="60" y="32" width="16" height="60" rx="4" fill="#8a5c2a"/>'
          '<rect x="-64" y="80" width="20" height="14" rx="4" fill="#6f4718"/>'
          '<rect x="-36" y="80" width="20" height="14" rx="4" fill="#6f4718"/>'
          '<rect x="32" y="80" width="20" height="14" rx="4" fill="#6f4718"/>'
          '<rect x="58" y="80" width="20" height="14" rx="4" fill="#6f4718"/></g>'
          # вытянутое тело с прогнутой спиной и подтянутым животом
          '<path d="M-78 -2 C-72 -26 -40 -36 2 -36 C46 -36 74 -26 80 -4'
          ' C84 14 72 34 36 38 C0 42 -46 42 -68 32 C-82 26 -84 12 -78 -2 Z"'
          ' fill="#a8702f" stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
          # короткий хвост торчком
          '<path d="M-76 -14 C-94 -26 -102 -44 -96 -58" stroke="#8a5c2a" stroke-width="11"'
          ' fill="none" stroke-linecap="round"/>'
          # высокая шея
          '<path d="M52 -22 C58 -62 72 -88 92 -98 C108 -106 120 -96 114 -80'
          ' C106 -56 94 -34 80 -14 Z" fill="#b67d36" stroke="#1b0f07" stroke-width="9"'
          ' stroke-linejoin="round"/>'
          # КЛИНОВИДНАЯ МОРДА вперёд-вправо — главный признак козы
          '<path d="M86 -104 C86 -124 104 -134 124 -132 C150 -130 170 -116 168 -100'
          ' C166 -86 146 -78 120 -78 C98 -78 86 -88 86 -104 Z" fill="#c08a40"'
          ' stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
          # ухо назад
          '<path d="M96 -116 C78 -126 64 -122 62 -110 C70 -100 86 -102 96 -116 Z"'
          ' fill="#8a5c2a" stroke="#1b0f07" stroke-width="6" stroke-linejoin="round"/>'
          # РОГА дугой назад — две штуки, задний короче
          '<path d="M104 -128 C122 -156 114 -180 88 -188" stroke="#7a4e1f" stroke-width="13"'
          ' fill="none" stroke-linecap="round"/>'
          '<path d="M92 -126 C106 -150 100 -170 80 -178" stroke="#6f4718" stroke-width="10"'
          ' fill="none" stroke-linecap="round"/>'
          # БОРОДКА под мордой
          '<path d="M118 -80 C124 -58 118 -40 104 -32" stroke="#8a5c2a" stroke-width="11"'
          ' fill="none" stroke-linecap="round"/>'
          # глаз, ноздря и линия рта
          '<circle cx="134" cy="-110" r="7" fill="#241208"/>'
          '<circle cx="163" cy="-99" r="4" fill="#241208"/>'
          '<path d="M150 -88 C158 -90 164 -94 166 -98" stroke="#1b0f07" stroke-width="5"'
          ' fill="none" stroke-linecap="round"/>'
          # текстура дерева по телу
          '<g stroke="#8a5c2a" stroke-width="4" fill="none" opacity=".55">'
          '<path d="M-58 -12 C-24 -22 26 -22 60 -10 M-58 18 C-24 8 26 8 62 18"/></g></g>')
    g = .3 + .25 * (0.5 + 0.5 * A.w(t, 3.2))
    s += f'<ellipse cx="470" cy="350" rx="170" ry="130" fill="#e07f23" opacity="{g*0.12:.2f}"/>'
    s += A.candle(680, 330, t, 70, 46, phase=.35, s=.85)
    s += A.confetti(t, 11, seed=181)
    return s


def final_warm(t):
    """Финал: за столом тепло и никто никуда не спешит."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(126, 80, 19, "#ffd45e"), (246, 120, 14, "#ff8c6b"),
                (58, 154, 13, "#9ae06a"), (352, 70, 11, "#7fd0ff")], ".34")
    s += window(760, 70, 170, 134, t)
    s += tree(126, 322, t, 0.6, 0.72, star=True)
    s += _garland(t, 12)
    # силуэты гостей вокруг, спокойные
    for x, sc, ph in ((330, .72, .0), (470, .78, .35), (610, .74, .7)):
        s += _silho(x, 190, t, sc, ph)
    s += table(386)
    # накрытый стол: зелень, сыр, утка, морс — всё, о чём шла речь
    s += ('<g stroke="#1b0f07" stroke-width="8">'
          '<ellipse cx="470" cy="448" rx="190" ry="44" fill="#cbb79a"/>'
          '<ellipse cx="470" cy="438" rx="158" ry="34" fill="#e8dac0"/></g>')
    s += _roast(470, 408, .62, dark="#8d3a12", light="#b4541c", bone=False, cut=False)
    s += herbs_glass(196, 400, 46, 62)
    s += herbs_glass(262, 412, 42, 54)
    s += ('<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<rect x="676" y="412" width="190" height="52" rx="10" fill="#b07d3f"/></g>'
          '<g stroke="#1b0f07" stroke-width="5">'
          '<path d="M700 440 L700 418 L740 406 L740 428 Z" fill="#f8f5ee"/>'
          '<path d="M760 442 L760 414 L818 424 L818 450 Z" fill="#e8c86a"/></g>')
    s += _goblet(130, 470, t, .9, .2)
    s += _goblet(880, 476, t, .94, .55)
    s += A.candle(392, 498, t, 46, 46, phase=.1, s=.82)
    s += A.candle(566, 504, t, 40, 44, phase=.5, s=.8)
    s += A.smoke(470, 384, t, 3, 150, .9, .22)
    s += A.confetti(t, 14, seed=191)
    return s


# ---- варианты служебных кадров: чтобы одни и те же не шли через весь ролик ----

def guests_close(t):
    """Гости крупнее и ближе: тянутся к столу, в руках бокалы."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(126, 82, 18, "#ffd45e"), (246, 122, 13, "#ff8c6b"), (56, 154, 12, "#9ae06a")])
    s += window(726, 74, 176, 138, t)
    s += tree(120, 320, t, 0.52, 0.6, star=True)
    s += _garland(t, 10)
    for x, sc, ph, coat, skin in ((196, 1.18, .0, "#5e3f6b", "#e9c99c"),
                                  (420, 1.30, .35, "#2f5c6b", "#f0d4a8"),
                                  (646, 1.22, .7, "#8c4a2a", "#e4bf90")):
        a = A.sway(t, 5.8, ph, 1.0)
        s += (f'<g transform="rotate({a:.2f} {x} 470) translate({x},180) scale({sc})">'
              f'<path d="M-96 260 C-96 150 -54 108 0 108 C54 108 96 150 96 260 Z" fill="{coat}"'
              ' stroke="#1b0f07" stroke-width="9"/>'
              f'<circle cx="0" cy="54" r="52" fill="{skin}" stroke="#1b0f07" stroke-width="9"/>'
              + _eyes(-18, 18, 48, t, 7, ph)
              + '<path d="M-16 76 C-6 86 8 86 18 76" stroke="#1b0f07" stroke-width="6"'
              ' fill="none" stroke-linecap="round"/></g>')
    s += table(400)
    for gx, ph in ((268, .1), (470, .5), (672, .8)):
        s += _goblet(gx, 470, t, 1.05, ph)
    s += ('<g stroke="#1b0f07" stroke-width="8">'
          '<ellipse cx="130" cy="492" rx="104" ry="28" fill="#dccbab"/>'
          '<ellipse cx="830" cy="496" rx="110" ry="30" fill="#dccbab"/></g>')
    s += A.candle(570, 442, t, 58, 44, phase=.3, s=.78)
    s += A.confetti(t, 14, seed=193)
    return s


def koza_window(t):
    """Хозяйка года у окна: смотрит на снег, в комнате тепло."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(132, 92, 17, "#ffd45e"), (250, 128, 13, "#ff8c6b")])
    s += window(560, 60, 340, 262, t)
    s += _garland(t, 10)
    s += tree(116, 330, t, 0.5, 0.55, star=True)
    s += table(430)
    s += f'<g transform="translate(400,260) scale(0.86) translate(-400,-260)">'
    s += _koza_head(t, fire=True, blink_ph=.3)
    s += '</g>'
    s += A.candle(846, 394, t, 64, 46, phase=.2, s=.82)
    s += _goblet(160, 486, t, .95, .4)
    s += A.confetti(t, 10, seed=197)
    return s


def koza_bokal(t):
    """Коза поднимает бокал — тёплый кадр для тоста и финала."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(128, 86, 18, "#ffd45e"), (248, 124, 14, "#ff8c6b"), (58, 158, 12, "#9ae06a")])
    s += tree(846, 318, t, 0.54, 0.6, star=True)
    s += _garland(t, 10)
    s += table(420)
    s += f'<g transform="translate(368,250) scale(0.78) translate(-368,-250)">'
    s += _koza_head(t, fire=True, blink_ph=.6)
    s += '</g>'
    # бокал в кадре, с бликом
    a = A.sway(t, 5.2, .2, 1.4)
    s += (f'<g transform="rotate({a:.2f} 712 460)">'
          '<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<path d="M636 286 L800 286 L772 406 C766 436 670 436 664 406 Z" fill="url(#glass)"/>'
          '<path d="M650 332 L786 332 L764 404 C758 428 678 428 672 404 Z" fill="#9b1b28"/>'
          '<path d="M718 436 L718 498" stroke="#1b0f07" stroke-width="11"/>'
          '<ellipse cx="718" cy="504" rx="62" ry="16" fill="url(#glass)"/></g>'
          '<path d="M668 300 L658 396" stroke="#ffffff" stroke-width="8" opacity=".5"'
          ' stroke-linecap="round"/></g>')
    g = .35 + .3 * (0.5 + 0.5 * A.w(t, 2.8))
    s += f'<circle cx="718" cy="356" r="118" fill="#ffd45e" opacity="{g*0.12:.2f}"/>'
    s += A.candle(140, 384, t, 70, 48, phase=.45, s=.86)
    s += A.confetti(t, 16, seed=199)
    return s


def table_wide(t):
    """Стол общим планом с другой точки: ниже и шире, видны оба края."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(840, 86, 17, "#ffd45e"), (734, 124, 13, "#ff8c6b"), (904, 156, 12, "#9ae06a")])
    s += tree(112, 300, t, 0.5, 0.5, star=True)
    s += _garland(t, 10)
    s += ('<path d="M20 340 L940 340 L960 540 L0 540 Z" fill="url(#cloth)"/>'
          '<path d="M20 332 L940 332 L944 356 L16 356 Z" fill="#c6523a"/>')
    s += herbs_glass(120, 376, 44, 58)
    s += herbs_glass(806, 384, 42, 56)
    s += ('<g stroke="#1b0f07" stroke-width="8">'
          '<ellipse cx="300" cy="438" rx="120" ry="32" fill="#dccbab"/>'
          '<ellipse cx="300" cy="430" rx="96" ry="24" fill="#f2ead6"/>'
          '<ellipse cx="650" cy="446" rx="126" ry="34" fill="#dccbab"/>'
          '<ellipse cx="650" cy="438" rx="100" ry="25" fill="#f2ead6"/></g>')
    s += _roast(300, 410, .5, bone=False, cut=False)
    s += _bowl(650, 420, 76, 24, "#4e7a35", berry="#c0203a")
    s += ('<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<rect x="368" y="470" width="220" height="48" rx="10" fill="#b07d3f"/></g>'
          '<g stroke="#1b0f07" stroke-width="5">'
          '<path d="M396 506 L396 482 L438 470 L438 494 Z" fill="#f8f5ee"/>'
          '<path d="M468 508 L468 480 L530 490 L530 516 Z" fill="#e8c86a"/></g>')
    s += _goblet(196, 470, t, .9, .1)
    s += _goblet(486, 420, t, .82, .5)
    s += _goblet(790, 476, t, .92, .8)
    s += A.candle(900, 462, t, 56, 42, phase=.15, s=.76)
    s += A.smoke(300, 392, t, 2, 110, .7, .18)
    s += A.confetti(t, 12, seed=211)
    return s


def koza_profile(t):
    """Та же принятая коза, но развёрнута к столу и чуть наклонена:
    свой кадр, а не третья подача одного и того же плана."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(130, 88, 18, "#ffd45e"), (252, 126, 13, "#ff8c6b"), (60, 160, 12, "#9ae06a")])
    s += tree(126, 316, t, 0.5, 0.55, star=True)
    s += _garland(t, 10)
    s += window(700, 74, 190, 150, t)
    s += table(404)
    tilt = 4.0 + 2.0 * A.w(t, 7.2, .2)
    s += (f'<g transform="translate(520,268) rotate({tilt:.2f}) scale(-0.92,0.92)'
          ' translate(-480,-250)">')
    s += _koza_head(t, fire=True, blink_ph=.45)
    s += '</g>'
    s += _goblet(840, 468, t, .95, .3)
    s += A.candle(150, 372, t, 66, 46, phase=.25, s=.82)
    s += A.confetti(t, 10, seed=223)
    return s


def greens_board(t):
    """Зелень на доске: пучки лежат, рядом нож — другой план той же опоры."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(840, 84, 17, "#ffd45e"), (736, 122, 13, "#ff8c6b"), (906, 154, 12, "#9ae06a")])
    s += tree(112, 286, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(336)
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<rect x="60" y="384" width="690" height="130" rx="16" fill="#b07d3f"/>'
          '<path d="M750 412 L812 412 C828 412 836 424 836 440 C836 458 828 470 812 470'
          ' L750 470 Z" fill="#9a6a33"/></g>'
          '<g stroke="#8a5c2a" stroke-width="4" opacity=".55">'
          '<path d="M86 412 L724 412 M86 488 L724 488"/></g>')
    # три пучка лежат поперёк доски, чуть качаются от сквозняка
    for i, (x, col, dark, per) in enumerate(((190, "#4e7a35", "#3f6b2c", 5.4),
                                             (390, "#5e9a4a", "#43703a", 6.0),
                                             (590, "#79b34c", "#4e7a35", 5.1))):
        a = A.sway(t, per, i * .3, 1.0)
        s += f'<g transform="rotate({a:.2f} {x} 448)">'
        s += (f'<g stroke="{col}" stroke-width="10" fill="none" stroke-linecap="round">'
              f'<path d="M{x-110} 462 C{x-50} 436 {x+40} 436 {x+106} 458"/>'
              f'<path d="M{x-104} 440 C{x-44} 416 {x+44} 416 {x+100} 438"/>'
              f'<path d="M{x-100} 482 C{x-40} 460 {x+46} 460 {x+98} 480"/></g>')
        s += f'<g fill="{dark}" stroke="#1b1309" stroke-width="4">'
        for dx, dy, r in ((-96, 452, 15), (-50, 432, 13), (0, 428, 16), (52, 432, 13),
                          (96, 450, 15), (-24, 470, 12), (30, 470, 12)):
            s += f'<circle cx="{x+dx}" cy="{dy}" r="{r}"/>'
        s += '</g>'
        s += (f'<rect x="{x-22}" y="438" width="44" height="22" rx="7" fill="#c9922f"'
              ' stroke="#1b1309" stroke-width="6"/></g>')
    # нож рядом
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M786 506 L920 476 L924 500 L790 524 Z" fill="#cfc8bd"/>'
          '<rect x="752" y="500" width="48" height="26" rx="8" fill="#6b3f1c"'
          ' transform="rotate(-10 752 500)"/></g>')
    s += A.candle(880, 320, t, 66, 46, phase=.3, s=.82)
    s += A.confetti(t, 11, seed=227)
    return s


def duck_cut(t):
    """Утка разрезана: куски с хрустящей кожей, апельсин, соус."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(126, 80, 18, "#ffd45e"), (248, 120, 14, "#ff8c6b"), (56, 152, 12, "#9ae06a")], ".3")
    s += tree(852, 272, t, 0.48, 0.42, star=False)
    s += _garland(t, 10)
    s += table(318)
    s += _plate_oval(470, 452, 364, 82, "#cbb79a", "#e8dac0")
    # ломти веером, у каждого тёмная кожа сверху и светлая мякоть
    for i in range(6):
        x = 198 + i * 92
        y = 436 - (i % 2) * 10
        rot = -14 + i * 5
        s += (f'<g transform="rotate({rot} {x} {y})">'
              f'<path d="M{x-54} {y+30} C{x-60} {y-18} {x-26} {y-44} {x+16} {y-42}'
              f' C{x+56} {y-40} {x+66} {y-6} {x+52} {y+28} C{x+20} {y+40} {x-24} {y+40} {x-54} {y+30} Z"'
              ' fill="#e0b584" stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>'
              f'<path d="M{x-56} {y-2} C{x-40} {y-34} {x+30} {y-44} {x+58} {y-8}'
              f' C{x+30} {y-20} {x-28} {y-18} {x-56} {y-2} Z" fill="#8d3a12"'
              ' stroke="#1b0f07" stroke-width="7" stroke-linejoin="round"/>'
              f'<path d="M{x-30} {y+14} C{x-10} {y+6} {x+18} {y+6} {x+34} {y+16}"'
              ' stroke="#c99466" stroke-width="5" fill="none" opacity=".8"/></g>')
    # апельсиновые дольки и соус
    s += ('<g stroke="#1b0f07" stroke-width="7">'
          '<path d="M150 486 C150 450 180 426 214 426 C214 462 186 486 150 486 Z" fill="#f0921f"/>'
          '<path d="M160 480 C162 454 184 436 208 434 C206 460 186 478 160 480 Z" fill="#ffb455"/>'
          '<path d="M744 492 C744 456 774 432 808 432 C808 468 780 492 744 492 Z" fill="#f0921f"/>'
          '<path d="M754 486 C756 460 778 442 802 440 C800 466 780 484 754 486 Z" fill="#ffb455"/></g>')
    s += ('<g stroke="#1b0f07" stroke-width="6">'
          '<ellipse cx="470" cy="500" rx="86" ry="20" fill="#6b3414"/></g>'
          '<ellipse cx="456" cy="496" rx="34" ry="8" fill="#8d4a1c" opacity=".8"/>')
    a = A.sway(t, 5.6, .4, 1.6)
    s += (f'<g transform="rotate({a:.2f} 300 506)">'
          '<g stroke="#43703a" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M300 506 L392 486"/><path d="M318 498 L312 480 M344 492 L338 474'
          ' M368 486 L364 468"/></g></g>')
    s += A.smoke(380, 390, t, 3, 150, .9, .26)
    s += A.confetti(t, 11, seed=229)
    return s


def cheese_slice(t):
    """Сыр крупным планом: ломти, мёд стекает, орех расколот."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(132, 86, 18, "#ffd45e"), (252, 124, 13, "#ff8c6b"), (58, 158, 12, "#9ae06a")])
    s += tree(858, 280, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(330)
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M70 392 L870 392 C906 392 920 410 920 436 L920 470 C920 498 900 512 866 512'
          ' L70 512 C40 512 24 498 24 470 L24 436 C24 410 40 392 70 392 Z" fill="#a9762f"/></g>')
    # три ломтя разного сыра, крупно
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M110 492 L110 404 L286 428 L286 496 Z" fill="#f2d87f"/>'
          '<path d="M110 404 L286 428 L246 448 L96 422 Z" fill="#f8e7a6"/>'
          '<path d="M336 496 L336 418 L470 396 L470 486 Z" fill="#f6f1e4"/>'
          '<path d="M336 418 L470 396 L512 414 L376 438 Z" fill="#fbf8f0"/>'
          '<path d="M556 490 L556 420 L712 406 L712 482 Z" fill="#e8c86a"/>'
          '<path d="M556 420 L712 406 L746 424 L588 440 Z" fill="#f2d87f"/></g>'
          '<g fill="#c9a23f"><circle cx="612" cy="444" r="8"/><circle cx="668" cy="456" r="6"/>'
          '<circle cx="640" cy="470" r="7"/></g>')
    for i, (gx, gy) in enumerate(((160, 448), (214, 466), (396, 452))):
        o = .35 + .45 * (0.5 + 0.5 * A.w(t, 2.3 + i * .6, i * .3))
        s += f'<circle cx="{gx}" cy="{gy}" r="4" fill="#fff" opacity="{o:.2f}"/>'
    # мёд стекает с ложки
    dz = 7 * A.w(t, 4.6, .1)
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<ellipse cx="800" cy="330" rx="46" ry="26" fill="#d8982a"'
          ' transform="rotate(-14 800 330)"/>'
          '<path d="M832 318 L906 282" stroke="#8a6a3a" stroke-width="12" fill="none"'
          ' stroke-linecap="round"/></g>')
    s += (f'<path d="M790 352 C{796+dz:.0f} 382 {784+dz:.0f} 404 792 430" stroke="#d8982a"'
          ' stroke-width="12" fill="none" stroke-linecap="round" opacity=".92"/>')
    # расколотый орех
    s += ('<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          '<path d="M250 526 C230 514 228 486 246 472 C264 458 290 464 298 484'
          ' C306 504 290 528 268 532 Z" fill="#c2914f"/>'
          '<path d="M258 478 C268 494 266 514 258 526 M244 498 L290 492"'
          ' stroke="#8a6133" stroke-width="5" fill="none"/></g>')
    s += A.confetti(t, 11, seed=233)
    return s


def guests_toast(t):
    """Гости поднимают бокалы: третий вариант застолья, свой план."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(130, 84, 18, "#ffd45e"), (250, 124, 14, "#ff8c6b"), (58, 158, 12, "#9ae06a")])
    s += tree(846, 310, t, 0.5, 0.55, star=True)
    s += _garland(t, 10)
    for x, sc, ph, coat in ((170, .96, .0, "#5e3f6b"), (330, 1.04, .3, "#2f5c6b"),
                            (560, 1.0, .6, "#8c4a2a"), (706, .92, .85, "#4e6b3a")):
        a = A.sway(t, 6.2, ph, 1.4)
        s += (f'<g transform="rotate({a:.2f} {x} 430) translate({x},150) scale({sc})">'
              f'<path d="M-84 230 C-84 136 -48 100 0 100 C48 100 84 136 84 230 Z" fill="{coat}"'
              ' stroke="#1b0f07" stroke-width="9"/>'
              '<circle cx="0" cy="54" r="46" fill="#edcfa4" stroke="#1b0f07" stroke-width="9"/>'
              + _eyes(-16, 16, 48, t, 6, ph)
              + '<path d="M-14 74 C-5 84 7 84 16 74" stroke="#1b0f07" stroke-width="6"'
              ' fill="none" stroke-linecap="round"/>'
              # поднятая рука с бокалом
              '<path d="M56 150 C86 120 104 86 104 56" stroke="#1b0f07" stroke-width="16"'
              ' fill="none" stroke-linecap="round"/>'
              '<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
              '<path d="M80 10 L130 10 L122 48 C120 58 90 58 88 48 Z" fill="url(#glass)"/>'
              '<path d="M86 26 L124 26 L118 46 C116 54 94 54 92 46 Z" fill="#9b1b28"/>'
              '<path d="M105 58 L105 80" stroke="#1b0f07" stroke-width="7"/>'
              '<ellipse cx="105" cy="84" rx="20" ry="6" fill="url(#glass)"/></g></g>')
    s += table(416)
    s += ('<g stroke="#1b0f07" stroke-width="8">'
          '<ellipse cx="150" cy="492" rx="112" ry="30" fill="#dccbab"/>'
          '<ellipse cx="820" cy="498" rx="118" ry="32" fill="#dccbab"/></g>')
    s += A.candle(470, 420, t, 60, 44, phase=.25, s=.8)
    s += A.confetti(t, 20, seed=239)
    return s


def pumpkin_slice(t):
    """Тыкву режут: половина, долька на доске и нож — рабочий план рецепта."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(838, 86, 17, "#ffd45e"), (734, 124, 13, "#ff8c6b"), (904, 156, 12, "#9ae06a")])
    s += tree(118, 284, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(336)
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<rect x="80" y="396" width="700" height="120" rx="16" fill="#b07d3f"/>'
          '<path d="M780 422 L840 422 C856 422 864 434 864 450 C864 468 856 480 840 480'
          ' L780 480 Z" fill="#9a6a33"/></g>')
    # половина тыквы срезом к зрителю
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<path d="M150 466 C130 406 176 356 250 356 C324 356 372 406 352 466 Z" fill="#d97119"/>'
          '<path d="M172 452 C158 408 196 376 250 376 C304 376 342 408 328 452 Z" fill="#ef9a2e"/>'
          '<path d="M202 440 C194 414 220 398 250 398 C280 398 306 414 298 440'
          ' C282 452 218 452 202 440 Z" fill="#e9c98a"/></g>'
          '<g fill="#f4e3bb" stroke="#1b0f07" stroke-width="3">'
          '<ellipse cx="232" cy="424" rx="7" ry="10"/><ellipse cx="252" cy="418" rx="7" ry="10"/>'
          '<ellipse cx="272" cy="424" rx="7" ry="10"/></g>')
    # отрезанные дольки веером
    for i, (x, rot, col) in enumerate(((440, -16, "#ef9a2e"), (520, -4, "#d97119"),
                                       (600, 8, "#e08523"))):
        s += (f'<g transform="rotate({rot} {x} 450)">'
              f'<path d="M{x-46} 486 C{x-54} 430 {x-24} 398 {x+16} 396'
              f' C{x+28} 438 {x+12} 476 {x-16} 494 Z" fill="{col}"'
              ' stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>'
              f'<path d="M{x-34} 462 C{x-38} 428 {x-18} 410 {x+6} 406"'
              ' stroke="#9c4a12" stroke-width="6" fill="none" opacity=".75"/></g>')
    # нож
    a = A.sway(t, 7.0, .2, 1.2)
    s += (f'<g transform="rotate({a:.2f} 700 380)">'
          '<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M672 384 L860 344 L866 372 L678 414 Z" fill="#cfc8bd"/>'
          '<rect x="636" y="378" width="52" height="28" rx="9" fill="#6b3f1c"'
          ' transform="rotate(-12 636 378)"/></g></g>')
    s += A.candle(886, 320, t, 64, 44, phase=.4, s=.8)
    s += A.confetti(t, 11, seed=241)
    return s


def fish_serve(t):
    """ПОДАЧА: рыба целиком — с головой и хвостом, как положено на Востоке.
    Длинное блюдо наискосок, палочки, пиала соевого соуса, пар. Прежде
    здесь стоял объеденный хребет — а озвучка как раз про подачу целиком
    (его правка 02.11)."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(842, 80, 18, "#ffd45e"), (740, 120, 13, "#ff8c6b"), (906, 154, 12, "#9ae06a")],
               ".32")
    s += tree(96, 282, t, 0.44, 0.38, star=False)
    s += _garland(t, 10)
    s += table(318)
    # вся подача мельче и выше — иначе блюдо упирается в нижний край
    s += '<g transform="translate(470,404) scale(0.76) translate(-470,-440)">'
    # длинное блюдо наискосок
    s += ('<g transform="rotate(-6 470 440)">'
          '<g stroke="#1b0f07" stroke-width="10" stroke-linejoin="round">'
          '<rect x="126" y="376" width="716" height="136" rx="56" fill="#cfc0a2"/>'
          '<rect x="146" y="392" width="676" height="104" rx="46" fill="#eee3cb"/></g>'
          '</g>')
    # рыба целиком: голова слева с глазом, хвост справа веером
    s += '<g transform="rotate(-6 470 440)">'
    s += ('<g stroke="#1b0f07" stroke-width="10" stroke-linejoin="round">'
          '<path d="M186 440 C244 382 348 354 470 354 C592 354 684 382 730 436'
          ' C684 492 590 520 470 520 C348 520 244 496 186 440 Z" fill="#c3ccd2"/>'
          '<path d="M716 392 C772 404 806 356 846 336 C836 388 820 420 816 440'
          ' C822 462 840 494 852 544 C808 520 770 476 716 486 Z" fill="#a4b4bc"/>'
          '<path d="M186 440 C212 406 242 388 270 378 L278 500 C242 490 212 468 186 440 Z"'
          ' fill="#aab8c0"/></g>')
    s += ('<path d="M270 378 C296 416 296 462 278 500" stroke="#6d7d86" stroke-width="7"'
          ' fill="none"/>'
          '<circle cx="234" cy="424" r="17" fill="#f4efe3" stroke="#1b0f07" stroke-width="6"/>'
          '<circle cx="234" cy="424" r="8" fill="#241208"/>'
          '<path d="M190 460 C208 470 228 472 246 468" stroke="#1b0f07" stroke-width="6"'
          ' fill="none" stroke-linecap="round"/>')
    # спинной плавник — чтобы рыба читалась рыбой, а не батоном
    s += ('<path d="M366 366 C420 320 520 316 578 356 C512 344 430 346 366 366 Z" fill="#a4b4bc" stroke="#1b0f07"'
          ' stroke-width="8" stroke-linejoin="round"/>')
    s += '<g stroke="#8d9ba3" stroke-width="4" fill="none" opacity=".75">'
    for k in range(5):
        xx = 336 + k * 86
        s += f'<path d="M{xx} 390 C{xx+24} 428 {xx+24} 458 {xx} 494"/>'
    s += '</g>'
    # зелёный лук и ломтики имбиря сверху
    s += '<g stroke="#1b0f07" stroke-width="5">'
    for ex, ey, rot, col in ((382, 424, -8, "#e9c98a"), (486, 416, 6, "#f0d9a4"),
                             (596, 424, -5, "#e9c98a")):
        s += (f'<ellipse cx="{ex}" cy="{ey}" rx="30" ry="12" fill="{col}"'
              f' transform="rotate({rot} {ex} {ey})"/>')
    s += '</g>'
    for i, lx in enumerate((428, 534, 638)):
        a = A.sway(t, 5.4 + i * .6, i * .3, 2.2)
        s += (f'<g transform="rotate({a:.2f} {lx} 440)">'
              f'<path d="M{lx-34} 452 C{lx-10} 428 {lx+18} 428 {lx+42} 444" stroke="#5e9a4a"'
              ' stroke-width="9" fill="none" stroke-linecap="round"/>'
              f'<path d="M{lx-24} 468 C{lx-2} 448 {lx+22} 448 {lx+40} 462" stroke="#79b34c"'
              ' stroke-width="7" fill="none" stroke-linecap="round"/></g>')
    s += '</g>'
    # палочки и пиала соевого соуса — восточная подача
    s += ('<g stroke="#1b0f07" stroke-width="6" stroke-linejoin="round">'
          '<path d="M120 556 L306 512 L312 528 L126 572 Z" fill="#c98f46"/>'
          '<path d="M130 572 L314 536 L318 550 L134 586 Z" fill="#b87f3c"/></g>')
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<path d="M726 560 C726 518 838 518 838 560 Z" fill="#dccbab"/>'
          '<path d="M736 550 C740 528 824 528 828 550 Z" fill="#4a2f18"/></g>')
    s += '</g>'
    s += A.smoke(440, 346, t, 3, 110, .7, .2)
    s += A.smoke(584, 352, t, 2, 100, .6, .16)
    s += A.candle(886, 322, t, 62, 44, phase=.35, s=.76)
    s += A.confetti(t, 11, seed=457)
    return s


def fish_left(t):
    """Рыбу не доедают: часть съедена, хвост и голова остались на блюде."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(128, 84, 18, "#ffd45e"), (246, 124, 13, "#ff8c6b"), (58, 156, 12, "#9ae06a")])
    s += tree(850, 272, t, 0.48, 0.42, star=False)
    s += _garland(t, 10)
    s += table(312)
    s += _plate_oval(480, 444, 388, 84, "#cfc0a2", "#eee3cb")
    # голова и передняя треть
    s += ('<g stroke="#1b0f07" stroke-width="10" stroke-linejoin="round">'
          '<path d="M182 414 C238 348 330 318 404 316 C398 374 398 448 404 490'
          ' C330 486 240 468 182 414 Z" fill="#bcc6cc"/>'
          '<path d="M182 414 C208 380 238 360 266 348 L274 476 C238 464 206 442 182 414 Z"'
          ' fill="#aab8c0"/></g>'
          '<circle cx="230" cy="398" r="17" fill="#f4efe3" stroke="#1b0f07" stroke-width="6"/>'
          '<circle cx="230" cy="398" r="8" fill="#241208"/>'
          '<path d="M186 434 C204 444 224 446 242 442" stroke="#1b0f07" stroke-width="6"'
          ' fill="none" stroke-linecap="round"/>')
    # хребет и объеденная середина
    s += ('<path d="M404 400 L676 396" stroke="#e4ddd0" stroke-width="10"'
          ' stroke-linecap="round"/>')
    s += '<g stroke="#cfc6b6" stroke-width="6" stroke-linecap="round">'
    for k in range(9):
        x = 418 + k * 30
        s += f'<path d="M{x} 400 L{x-8} 356" /><path d="M{x} 400 L{x-8} 444"/>'
    s += '</g>'
    # хвост
    s += ('<g stroke="#1b0f07" stroke-width="10" stroke-linejoin="round">'
          '<path d="M676 396 L690 344 L724 392 L764 330 L744 396 L768 462 L724 408 L690 452 Z"'
          ' fill="#9fb0b8"/></g>')
    # лимон и зелень
    s += ('<g stroke="#1b0f07" stroke-width="7">'
          '<circle cx="190" cy="490" r="34" fill="#f2d24a"/><circle cx="190" cy="490" r="22" fill="#f8ea9e"/></g>'
          '<g stroke="#e0b62a" stroke-width="4" stroke-linecap="round">'
          '<path d="M190 468 L190 512 M168 490 L212 490 M174 474 L206 506 M206 474 L174 506"/></g>')
    a = A.sway(t, 5.8, .3, 2.0)
    s += (f'<g transform="rotate({a:.2f} 560 486)">'
          '<g stroke="#4e7a35" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M560 486 L652 468"/><path d="M578 478 L572 458 M604 472 L598 452"/></g></g>')
    s += A.confetti(t, 10, seed=251)
    return s


def fruit_basket(t):
    """Фруктовая корзина отдельным кадром: мандарины, яблоки, гранат."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(132, 88, 18, "#ffd45e"), (252, 126, 13, "#ff8c6b"), (60, 160, 12, "#9ae06a")])
    s += tree(118, 286, t, 0.46, 0.42, star=False)
    s += _garland(t, 10)
    s += table(348)
    # корзина крупно по центру
    s += ('<g stroke="#1b0f07" stroke-width="10" stroke-linejoin="round">'
          '<path d="M276 406 C276 384 684 384 684 406 L656 512 C650 532 310 532 304 512 Z"'
          ' fill="#a9762f"/></g>'
          '<g stroke="#7f5420" stroke-width="6" opacity=".8">'
          '<path d="M292 444 L668 444 M300 482 L660 482"/>'
          '<path d="M360 392 L348 524 M470 388 L470 528 M580 392 L592 524"/></g>'
          '<path d="M276 406 C340 352 620 352 684 406" stroke="#8a5c2a" stroke-width="12"'
          ' fill="none"/>')
    # фрукты горкой
    for cx, cy, r, col, inner in ((352, 384, 46, "#f0921f", "#ffb455"),
                                  (452, 364, 52, "#ef9a2e", "#ffc06a"),
                                  (560, 378, 48, "#f0921f", "#ffb455"),
                                  (650, 396, 42, "#ef9a2e", "#ffc06a"),
                                  (404, 330, 44, "#c0203a", "#d8465c"),
                                  (512, 322, 46, "#a8172c", "#c0203a")):
        s += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="#1b0f07" stroke-width="8"/>'
              f'<circle cx="{cx-r//4}" cy="{cy-r//3}" r="{r//3}" fill="{inner}" opacity=".75"/>')
    s += ('<g stroke="#4e7a35" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M404 286 L398 266"/><path d="M512 276 L518 256"/></g>'
          '<g fill="#3f8c3c" stroke="#1b0f07" stroke-width="5">'
          '<path d="M398 266 C382 254 386 236 404 234 C420 232 430 246 424 258 Z"/></g>')
    s += ('<g stroke="#1b0f07" stroke-width="7">'
          '<circle cx="786" cy="486" r="44" fill="#a8172c"/>'
          '<path d="M786 442 L778 422 L794 426 Z" fill="#7a0f20"/></g>'
          '<g fill="#c0203a"><circle cx="772" cy="478" r="8"/><circle cx="800" cy="482" r="7"/></g>')
    s += A.candle(140, 352, t, 66, 46, phase=.35, s=.82)
    s += A.confetti(t, 12, seed=257)
    return s


# ---------------- новые рисунки против сквозного повтора (02.11) ----------------

def basics_six(t):
    """Шесть основ стола гостьи: зелень, овощи, фрукты, крупа, орехи, сыр."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(846, 90, 17, "#ffd45e"), (742, 128, 13, "#ff8c6b"), (900, 160, 12, "#9ae06a")])
    s += tree(104, 290, t, 0.44, 0.38, star=False)
    s += _garland(t, 10)
    s += table(342)
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<rect x="34" y="392" width="892" height="124" rx="18" fill="#a8702f"/></g>'
          '<g stroke="#8a5c2a" stroke-width="4" opacity=".5">'
          '<path d="M60 420 L900 420 M60 492 L900 492"/></g>')
    # 1 зелень пучком
    a = A.sway(t, 5.6, .1, 1.4)
    s += (f'<g transform="rotate({a:.2f} 108 500)">'
          '<g stroke="#4e7a35" stroke-width="9" fill="none" stroke-linecap="round">'
          '<path d="M108 500 C86 464 84 436 96 410"/><path d="M108 500 C112 462 122 436 140 416"/>'
          '<path d="M108 500 C96 470 72 452 52 444"/></g>'
          '<g fill="#3f6b2c" stroke="#1b1309" stroke-width="4">'
          '<circle cx="96" cy="408" r="14"/><circle cx="142" cy="414" r="12"/>'
          '<circle cx="50" cy="442" r="12"/><circle cx="120" cy="438" r="11"/></g>'
          '<rect x="88" y="470" width="40" height="22" rx="7" fill="#c9922f"'
          ' stroke="#1b1309" stroke-width="6"/></g>')
    # 2 овощи: морковь и перец
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M210 490 C236 458 268 440 300 436 C292 466 266 486 232 496 Z" fill="#e07f23"'
          ' transform="rotate(-8 256 466)"/>'
          '<path d="M300 436 C312 424 322 420 330 424" stroke="#4e7a35" stroke-width="9" fill="none"/>'
          '<path d="M222 500 C206 474 216 446 244 440 C258 466 254 492 238 502 Z" fill="#d6202f"/>'
          '</g>')
    # 3 фрукты: яблоко и мандарин
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<circle cx="396" cy="470" r="38" fill="#c3281f"/>'
          '<path d="M396 432 C398 418 408 410 420 410" stroke="#4e7a35" stroke-width="8" fill="none"/>'
          '<circle cx="460" cy="486" r="28" fill="#f0921f"/></g>'
          '<path d="M378 452 C386 440 400 438 410 444" stroke="#f0a090" stroke-width="7"'
          ' fill="none" opacity=".6" stroke-linecap="round"/>')
    # 4 крупа в банке
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M520 500 L520 430 C520 418 532 412 548 412 C564 412 576 418 576 430 L576 500 Z"'
          ' fill="url(#glass)"/>'
          '<path d="M522 500 L522 448 L574 448 L574 500 Z" fill="#d8b06a"/>'
          '<rect x="516" y="404" width="64" height="16" rx="5" fill="#c9922f"/></g>'
          '<g fill="#b9913f" opacity=".8"><circle cx="534" cy="462" r="4"/><circle cx="552" cy="470" r="4"/>'
          '<circle cx="564" cy="458" r="4"/><circle cx="542" cy="484" r="4"/></g>')
    # 5 орехи горкой
    s += '<g stroke="#1b1309" stroke-width="7" fill="#b07d3f">'
    for nx, ny, rr in ((648, 486, 19), (686, 492, 17), (666, 462, 18), (704, 470, 16), (630, 464, 15)):
        s += f'<circle cx="{nx}" cy="{ny}" r="{rr}"/>'
    s += '</g><g stroke="#7a5324" stroke-width="4" fill="none" opacity=".8">'
    for nx, ny, rr in ((648, 486, 19), (686, 492, 17), (666, 462, 18), (704, 470, 16)):
        s += f'<path d="M{nx-rr+4} {ny} L{nx+rr-4} {ny}"/><path d="M{nx} {ny-rr+5} C{nx+6} {ny} {nx-6} {ny} {nx} {ny+rr-5}"/>'
    s += '</g>'
    # 6 клин сыра с кристалликами
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M784 496 L784 428 L906 408 L906 486 Z" fill="#f2d87f"/>'
          '<path d="M784 428 L906 408 L880 394 L762 414 Z" fill="#f8e7a6"/></g>')
    for i, (gx, gy) in enumerate(((812, 452), (856, 444), (838, 472), (880, 460))):
        o = .3 + .5 * (0.5 + 0.5 * A.w(t, 2.2 + i * .5, i * .3))
        s += f'<circle cx="{gx}" cy="{gy}" r="4" fill="#fff" opacity="{o:.2f}"/>'
    s += A.candle(898, 326, t, 64, 46, phase=.3, s=.8)
    s += A.confetti(t, 11, seed=301)
    return s


def empty_plate(t):
    """Пустой стол: огромная тарелка и два салатных листа — это бедность, не уважение."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += window(96, 56, 196, 212, t)
    s += '<ellipse cx="196" cy="300" rx="210" ry="150" fill="#9fc4e8" opacity=".10"/>'
    s += _garland(t, 10)
    s += tree(876, 300, t, 0.42, 0.26, star=False)
    s += table(352, top="#8e3b2c")
    # холодная полоса света из окна через стол
    s += ('<path d="M120 400 L300 360 L470 540 L170 540 Z" fill="#cfe0f2" opacity=".10"/>')
    s += '<ellipse cx="470" cy="506" rx="250" ry="34" fill="#1b0f07" opacity=".35"/>'
    s += _plate_oval(470, 452, 272, 72, "#dcd3c2", "#f1ece0")
    # два одиноких листа
    for i, (lx, ly, rot) in enumerate(((432, 444, -12), (512, 452, 14))):
        a = A.sway(t, 6.2, i * .4, 1.1)
        s += (f'<g transform="rotate({rot + a:.2f} {lx} {ly})">'
              f'<path d="M{lx-54} {ly+10} C{lx-40} {ly-26} {lx+6} {ly-34} {lx+48} {ly-14}'
              f' C{lx+22} {ly+18} {lx-22} {ly+22} {lx-54} {ly+10} Z" fill="#6f9c48"'
              ' stroke="#1b1309" stroke-width="7" stroke-linejoin="round"/>'
              f'<path d="M{lx-46} {ly+6} C{lx-16} {ly-8} {lx+16} {ly-10} {lx+42} {ly-12}"'
              ' stroke="#48702f" stroke-width="5" fill="none" opacity=".8"/></g>')
    s += _cutlery(690, 472, fork=True)
    s += _cutlery(170, 472)
    s += '<ellipse cx="470" cy="536" rx="300" ry="20" fill="#1b0f07" opacity=".25"/>'
    s += A.candle(846, 392, t, 62, 40, phase=.6, s=.72)
    return s


def seafood(t):
    """Морепродукты на льду: креветки, ракушки, лимон — сытно, но не грубо."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(128, 84, 18, "#ffd45e"), (248, 124, 13, "#ff8c6b"), (58, 156, 12, "#9ae06a")])
    s += tree(856, 282, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(330)
    s += _plate_oval(470, 452, 352, 84, "#cbd6d8", "#e7eef0")
    # лёд: осколки с мерцанием
    s += '<g stroke="#1b0f07" stroke-width="5" fill="#dceaf2" opacity=".9">'
    for ix, iy, r in ((330, 470, 20), (372, 492, 16), (560, 480, 18), (612, 466, 15),
                      (470, 496, 17), (280, 488, 14), (660, 490, 14)):
        s += f'<path d="M{ix-r} {iy} L{ix-r*0.3:.0f} {iy-r} L{ix+r*0.6:.0f} {iy-r*0.7:.0f} L{ix+r} {iy+r*0.4:.0f} L{ix-r*0.2:.0f} {iy+r*0.6:.0f} Z"/>'
    s += '</g>'
    for i, (gx, gy) in enumerate(((344, 462), (568, 472), (474, 488), (292, 480))):
        o = .25 + .6 * (0.5 + 0.5 * A.w(t, 2.0 + i * .6, i * .35))
        s += f'<circle cx="{gx}" cy="{gy}" r="5" fill="#fff" opacity="{o:.2f}"/>'
    # три креветки, чуть качаются
    for i, (x, y, sc, rot) in enumerate(((392, 440, 1.0, -10), (502, 426, .92, 8), (596, 448, .86, -16))):
        a = A.sway(t, 6.4, i * .3, .8)
        s += (f'<g transform="rotate({rot + a:.2f} {x} {y}) translate({x},{y}) scale({sc})">'
              '<path d="M-62 18 C-74 -14 -52 -44 -16 -48 C22 -52 52 -32 56 2 C58 24 44 38 26 36'
              ' C34 16 26 -8 2 -14 C-24 -20 -44 -6 -46 20 Z" fill="#e8734a"'
              ' stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>'
              '<g stroke="#b94526" stroke-width="5" fill="none" opacity=".75">'
              '<path d="M-44 4 C-32 -16 -10 -26 8 -24 M-30 18 C-16 -2 6 -12 24 -10"/></g>'
              '<g stroke="#1b0f07" stroke-width="5" fill="none" stroke-linecap="round">'
              '<path d="M-62 14 L-86 2 M-62 20 L-88 20 M-60 26 L-84 38"/></g>'
              '<circle cx="-50" cy="-4" r="5" fill="#1b0f07"/></g>')
    # две ракушки
    for x, y, rot in ((262, 442, -8), (700, 452, 12)):
        s += (f'<g transform="rotate({rot} {x} {y})">'
              f'<path d="M{x-44} {y+16} C{x-48} {y-22} {x-20} {y-44} {x+14} {y-42}'
              f' C{x+48} {y-40} {x+60} {y-12} {x+48} {y+16} Z" fill="#3c4a63"'
              ' stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>'
              f'<g stroke="#8795ad" stroke-width="4" fill="none" opacity=".8">'
              f'<path d="M{x-28} {y+12} C{x-24} {y-16} {x-10} {y-34} {x+6} {y-38}'
              f' M{x-8} {y+14} C{x-2} {y-14} {x+10} {y-30} {x+24} {y-34}'
              f' M{x+14} {y+14} C{x+22} {y-10} {x+34} {y-22} {x+44} {y-24}"/></g></g>')
    # лимон дольками и зелень
    s += ('<g stroke="#1b0f07" stroke-width="7">'
          '<path d="M150 494 C150 458 180 434 214 434 C214 470 186 494 150 494 Z" fill="#f2c73c"/>'
          '<path d="M160 488 C162 462 184 444 208 442 C206 468 186 486 160 488 Z" fill="#fbe9a8"/></g>')
    a = A.sway(t, 5.8, .4, 1.5)
    s += (f'<g transform="rotate({a:.2f} 790 500)">'
          '<g stroke="#43703a" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M790 500 L876 478"/><path d="M806 494 L800 476 M832 488 L826 470 M856 482 L852 464"/></g></g>')
    s += A.candle(140, 344, t, 62, 44, phase=.2, s=.78)
    s += A.confetti(t, 10, seed=303)
    return s


def herb_glasses(t):
    """Зелень в низких стаканах между тарелками: гости тянутся к ним руками."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(844, 88, 17, "#ffd45e"), (746, 126, 13, "#ff8c6b"), (902, 158, 12, "#9ae06a")])
    s += tree(100, 288, t, 0.44, 0.36, star=False)
    s += _garland(t, 10)
    s += table(336)
    # две тарелки по краям — стаканы стоят ПРЯМО МЕЖДУ блюдами
    s += _plate_oval(126, 470, 150, 44, "#cfbf9f", "#ece0c6")
    s += _plate_oval(820, 476, 152, 44, "#cfbf9f", "#ece0c6")
    s += '<ellipse cx="470" cy="506" rx="230" ry="26" fill="#1b0f07" opacity=".3"/>'
    for i, (x, w, h, col, dark) in enumerate(((300, 86, 104, "#4e7a35", "#3f6b2c"),
                                              (452, 96, 116, "#5e9a4a", "#43703a"),
                                              (616, 84, 100, "#79b34c", "#4e7a35"))):
        y = 516 - h
        a = A.sway(t, 5.4 + i * .5, i * .35, 1.3)
        s += (f'<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
              f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="url(#glass)"/>'
              f'<rect x="{x+6}" y="{y+h*0.46:.0f}" width="{w-12}" height="{h*0.5:.0f}" rx="4"'
              ' fill="#cfe6f2" opacity=".35"/></g>')
        cx = x + w / 2
        s += f'<g transform="rotate({a:.2f} {cx:.0f} {y})">'
        s += (f'<g stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round">'
              f'<path d="M{cx:.0f} {y+20} L{cx-10:.0f} {y-92}"/>'
              f'<path d="M{cx-8:.0f} {y-30} C{cx-44:.0f} {y-48} {cx-56:.0f} {y-86} {cx-48:.0f} {y-116}"/>'
              f'<path d="M{cx-4:.0f} {y-10} C{cx+34:.0f} {y-30} {cx+48:.0f} {y-68} {cx+40:.0f} {y-100}"/>'
              f'<path d="M{cx:.0f} {y-54} C{cx+16:.0f} {y-82} {cx+12:.0f} {y-110} {cx-2:.0f} {y-128}"/></g>')
        s += f'<g fill="{dark}" stroke="#1b1309" stroke-width="4">'
        for dx, dy, r in ((-48, -116, 14), (40, -100, 13), (-2, -128, 15), (-10, -92, 12),
                          (-30, -70, 11), (24, -62, 11)):
            s += f'<circle cx="{cx+dx:.0f}" cy="{y+dy}" r="{r}"/>'
        s += '</g></g>'
    # рядом хлеб и нож — чтобы было видно, что стаканы стоят МЕЖДУ едой
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M706 498 C700 462 730 438 772 438 C814 438 844 460 840 498 Z" fill="#c98f46"/>'
          '<path d="M716 474 C714 452 740 440 772 440 C804 440 828 452 826 474 Z" fill="#e0b069"/></g>')
    s += A.candle(886, 330, t, 62, 44, phase=.5, s=.78)
    s += A.confetti(t, 11, seed=305)
    return s


def herb_three(t):
    """Три стакана зелени В РЯД НА ЛИНИИ СТОЛА, у каждого СВОЯ трава,
    и каждая узнаётся по рисунку: розмарин — жёсткие иголки, кинза —
    веер резных листиков, базилик — крупные парные листья. Под стаканами
    деревянные бирки с названием (его правка 02.11)."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(846, 86, 17, "#ffd45e"), (742, 124, 13, "#ff8c6b"), (904, 156, 12, "#9ae06a")])
    s += tree(84, 292, t, 0.40, 0.32, star=False)
    s += _garland(t, 10)
    s += table(350)
    s += '<ellipse cx="470" cy="462" rx="300" ry="22" fill="#1b0f07" opacity=".28"/>'
    # --- три стакана: основания стоят на ОДНОЙ линии ------------------------
    for i, (x, name, col, dark) in enumerate(((150, "РОЗМАРИН", "#6f8a52", "#55703d"),
                                              (424, "КИНЗА", "#5e9a4a", "#3f6b2c"),
                                              (700, "БАЗИЛИК", "#46772f", "#2f5820"))):
        w, h = 112, 92
        y = 452 - h                      # верх стакана: бирка должна влезть ниже
        cx = x + w / 2
        a = A.sway(t, 5.2 + i * .7, i * .33, 1.4)
        s += f'<g transform="rotate({a:.2f} {cx:.0f} {y})">'
        if i == 0:
            # РОЗМАРИН: прямые ветки, на каждой частые короткие иголки
            for k, (dx, tip, lean) in enumerate(((-30, -150, -16), (-8, -186, -4),
                                                 (18, -170, 10), (38, -132, 22))):
                x0, y0 = cx + dx, y + 16
                x1, y1 = cx + dx + lean, y + tip
                s += (f'<path d="M{x0:.0f} {y0} L{x1:.0f} {y1}" stroke="{dark}"'
                      ' stroke-width="7" stroke-linecap="round"/>')
                n = 9
                for j in range(1, n + 1):
                    p = j / (n + 1.0)
                    px, py = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
                    L = 19 - 7 * p
                    s += (f'<path d="M{px:.0f} {py:.0f} L{px-L:.0f} {py-L*0.55:.0f}'
                          f' M{px:.0f} {py:.0f} L{px+L:.0f} {py-L*0.55:.0f}"'
                          f' stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
        elif i == 1:
            # КИНЗА: тонкие черешки веером, на конце — тройка резных листиков
            for dx, tip, lean in ((-34, -120, -34), (-12, -156, -14), (14, -150, 16), (36, -118, 34)):
                x0, y0 = cx + dx * .4, y + 16
                x1, y1 = cx + dx + lean, y + tip
                s += (f'<path d="M{x0:.0f} {y0} C{x0:.0f} {y0-40} {x1:.0f} {y1+46} {x1:.0f} {y1:.0f}"'
                      f' stroke="{dark}" stroke-width="6" fill="none" stroke-linecap="round"/>')
                for lx, ly, r in ((-20, -8, 17), (20, -8, 17), (0, -24, 18)):
                    ex, ey = x1 + lx, y1 + ly
                    s += (f'<path d="M{ex:.0f} {ey+r*0.9:.0f} C{ex-r*1.15:.0f} {ey+r*0.5:.0f}'
                          f' {ex-r*1.0:.0f} {ey-r*0.9:.0f} {ex:.0f} {ey-r*1.0:.0f}'
                          f' C{ex+r*1.0:.0f} {ey-r*0.9:.0f} {ex+r*1.15:.0f} {ey+r*0.5:.0f}'
                          f' {ex:.0f} {ey+r*0.9:.0f} Z" fill="{col}" stroke="#1b1309"'
                          ' stroke-width="4" stroke-linejoin="round"/>')
                    s += (f'<path d="M{ex:.0f} {ey+r*0.7:.0f} L{ex:.0f} {ey-r*0.8:.0f}"'
                          f' stroke="{dark}" stroke-width="3"/>')
        else:
            # БАЗИЛИК: толстые стебли, КРУПНЫЕ парные листья с прожилкой
            for dx, tip, lean in ((-26, -128, -26), (0, -166, 2), (26, -132, 26)):
                x0, y0 = cx + dx * .5, y + 16
                x1, y1 = cx + dx + lean, y + tip
                s += (f'<path d="M{x0:.0f} {y0} C{x0:.0f} {y0-50} {x1:.0f} {y1+50} {x1:.0f} {y1:.0f}"'
                      f' stroke="{dark}" stroke-width="8" fill="none" stroke-linecap="round"/>')
                for p, side, L in ((.42, -1, 40), (.42, 1, 40), (.74, -1, 33), (.74, 1, 33)):
                    bx = x0 + (x1 - x0) * p
                    by = y0 + (y1 - y0) * p
                    ex, ey = bx + side * L * 1.05, by - L * 0.72
                    s += (f'<path d="M{bx:.0f} {by:.0f} C{bx + side*L*0.25:.0f} {by - L*0.72:.0f}'
                          f' {ex - side*L*0.25:.0f} {ey - L*0.55:.0f} {ex:.0f} {ey:.0f}'
                          f' C{ex - side*L*0.45:.0f} {ey + L*0.42:.0f} {bx + side*L*0.4:.0f}'
                          f' {by + L*0.22:.0f} {bx:.0f} {by:.0f} Z" fill="{col}"'
                          ' stroke="#1b1309" stroke-width="5" stroke-linejoin="round"/>')
                    s += (f'<path d="M{bx:.0f} {by:.0f} C{bx + side*L*0.4:.0f} {by - L*0.38:.0f}'
                          f' {ex - side*L*0.3:.0f} {ey - L*0.1:.0f} {ex:.0f} {ey:.0f}"'
                          f' stroke="{dark}" stroke-width="4" fill="none"/>')
        s += '</g>'
        # стакан поверх стеблей — видно, что трава СТОИТ В НЁМ
        s += (f'<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
              f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="url(#glass)"/>'
              f'<rect x="{x+7}" y="{y+h*0.44:.0f}" width="{w-14}" height="{h*0.5:.0f}" rx="4"'
              ' fill="#cfe6f2" opacity=".38"/></g>')
        s += (f'<path d="M{x+16} {y+14} L{x+16} {y+h-14}" stroke="#ffffff"'
              ' stroke-width="6" opacity=".45" stroke-linecap="round"/>')
        # деревянная бирка с названием — чтобы трава ещё и ЧИТАЛАСЬ.
        # ширина МЕРЯЕТСЯ ШРИФТОМ (правило 3), а не прикидывается
        try:
            import overlays as _O
            bw = _O.wid(name, "DejaVu Sans", 23, True) + 46
        except Exception:
            bw = 150
        s += (f'<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
              f'<rect x="{cx-bw/2:.0f}" y="460" width="{bw}" height="34" rx="8" fill="#d8a85c"/></g>'
              f'<text x="{cx:.0f}" y="485" font-family="DejaVu Sans" font-size="23"'
              f' font-weight="bold" fill="#2a1a08" text-anchor="middle">{name}</text>')
    s += A.candle(898, 330, t, 62, 44, phase=.4, s=.78)
    s += A.confetti(t, 10, seed=317)
    return s

def cheese_trio(t):
    """Три сыра по отдельности: круг с белой корочкой, фета в рассоле, твёрдый клин."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(840, 86, 18, "#ffd45e"), (740, 126, 14, "#ff8c6b"), (904, 158, 12, "#9ae06a")])
    s += tree(98, 286, t, 0.44, 0.36, star=False)
    s += _garland(t, 10)
    s += table(332)
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<rect x="40" y="398" width="880" height="118" rx="16" fill="#9a6a33"/></g>'
          '<g stroke="#7d5425" stroke-width="4" opacity=".5"><path d="M66 426 L894 426 M66 492 L894 492"/></g>')
    # 1 козий: круг с белой корочкой, вырезан клин
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<ellipse cx="190" cy="462" rx="104" ry="52" fill="#f6f1e4"/>'
          '<path d="M190 462 L286 442 C290 462 276 482 250 492 Z" fill="#efe6d2"/>'
          '<ellipse cx="190" cy="448" rx="92" ry="42" fill="#fbf8f0"/></g>'
          '<g stroke="#ddd2bb" stroke-width="5" fill="none" opacity=".9">'
          '<path d="M120 440 C150 428 230 428 258 440 M136 460 C166 450 216 450 244 458"/></g>'
          '<path d="M190 448 L264 436 C268 450 256 462 236 468 Z" fill="#f0e3c2"'
          ' stroke="#1b1309" stroke-width="7" stroke-linejoin="round"/>')
    # 2 фета в рассоле: кубы в пиале с жидкостью
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M372 420 L578 420 C574 480 548 506 476 506 C404 506 378 480 372 420 Z" fill="#dccbab"/>'
          '<path d="M382 436 L568 436 C562 476 536 494 476 494 C416 494 390 476 382 436 Z"'
          ' fill="#e9f1f6" opacity=".9"/></g>')
    for i, (x, y, sz, rot) in enumerate(((422, 456, 38, -8), (476, 446, 42, 6), (528, 460, 34, -14))):
        q = 2.0 * A.w(t, 4.2, i * .4)
        s += (f'<g transform="rotate({rot + q:.2f} {x} {y})">'
              f'<rect x="{x-sz/2:.0f}" y="{y-sz/2:.0f}" width="{sz}" height="{sz}" rx="4" fill="#fdfcf8"'
              ' stroke="#1b1309" stroke-width="7"/>'
              f'<path d="M{x-sz/2+5:.0f} {y-sz/2+8:.0f} L{x+sz/2-6:.0f} {y-sz/2+8:.0f}" stroke="#e2dccd"'
              ' stroke-width="5"/></g>')
    s += ('<g stroke="#43703a" stroke-width="6" fill="none" stroke-linecap="round" opacity=".9">'
          '<path d="M400 480 C420 470 444 470 462 478 M500 482 C520 472 544 474 560 482"/></g>')
    # 3 твёрдый клин с кристалликами
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M672 500 L672 426 L886 400 L886 482 Z" fill="#e8c86a"/>'
          '<path d="M672 426 L886 400 L856 384 L644 410 Z" fill="#f2d87f"/></g>'
          '<g stroke="#c08f2c" stroke-width="4" fill="none" opacity=".5">'
          '<path d="M700 444 L700 496 M760 436 L760 492 M820 428 L820 488"/></g>')
    for i, (gx, gy) in enumerate(((708, 460), (762, 452), (812, 466), (840, 440), (736, 478))):
        o = .25 + .6 * (0.5 + 0.5 * A.w(t, 2.1 + i * .5, i * .3))
        s += f'<circle cx="{gx}" cy="{gy}" r="4.5" fill="#fff" opacity="{o:.2f}"/>'
    s += A.candle(900, 330, t, 64, 46, phase=.3, s=.8)
    s += A.confetti(t, 10, seed=307)
    return s


def honey_nuts(t):
    """Три сопровождения к сырам: мёд с грецкими орехами, инжир, яблоко веером."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(846, 90, 17, "#ffd45e"), (744, 130, 13, "#ff8c6b"), (900, 162, 12, "#9ae06a")])
    s += tree(96, 290, t, 0.42, 0.34, star=False)
    s += _garland(t, 10)
    s += table(336)
    s += '<ellipse cx="470" cy="512" rx="300" ry="26" fill="#1b0f07" opacity=".28"/>'
    # пиала мёда, мёд стекает с ложки
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M160 430 L352 430 C348 486 322 510 256 510 C190 510 164 486 160 430 Z" fill="#dccbab"/>'
          '<path d="M172 444 L340 444 C334 482 310 498 256 498 C202 498 178 482 172 444 Z" fill="#d8982a"/></g>')
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<ellipse cx="286" cy="382" rx="44" ry="25" fill="#c9922f" transform="rotate(-16 286 382)"/>'
          '<path d="M320 368 L392 330" stroke="#8a6a3a" stroke-width="12" fill="none" stroke-linecap="round"/></g>')
    dz = 8 * A.w(t, 4.4, .1)
    s += (f'<path d="M276 404 C{282+dz:.0f} 418 {272+dz:.0f} 432 280 446" stroke="#d8982a"'
          ' stroke-width="13" fill="none" stroke-linecap="round" opacity=".92"/>')
    # грецкие орехи: целый, расколотый
    s += '<g stroke="#1b1309" stroke-width="7" fill="#b07d3f">'
    for nx, ny, rr in ((392, 486, 22), (436, 498, 18), (414, 458, 19)):
        s += f'<circle cx="{nx}" cy="{ny}" r="{rr}"/>'
    s += '</g><g stroke="#7a5324" stroke-width="4" fill="none" opacity=".85">'
    for nx, ny, rr in ((392, 486, 22), (436, 498, 18), (414, 458, 19)):
        s += (f'<path d="M{nx-rr+4} {ny} L{nx+rr-4} {ny}"/>'
              f'<path d="M{nx} {ny-rr+5} C{nx+7} {ny} {nx-7} {ny} {nx} {ny+rr-5}"/>')
    s += '</g>'
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M342 470 C342 446 362 430 386 432 C380 456 362 470 342 470 Z" fill="#e8d6b4"/></g>')
    # инжир разрезанный и вяленые абрикосы
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M520 500 C496 484 492 452 512 432 C532 412 566 414 582 436 C598 458 590 490 564 502'
          ' C548 508 532 508 520 500 Z" fill="#6b3a63"/>'
          '<path d="M612 496 C592 480 590 452 608 436 C626 420 656 424 668 444 C680 464 672 490 648 500'
          ' C634 504 622 504 612 496 Z" fill="#8a4a7c"/></g>'
          '<path d="M620 490 C608 476 608 456 620 444 C634 432 654 436 662 450 C670 466 662 484 644 492'
          ' C634 495 626 495 620 490 Z" fill="#d6607a"/>'
          '<g stroke="#f2c0cc" stroke-width="4" fill="none" opacity=".9">'
          '<path d="M636 448 L636 486 M622 460 L652 476 M652 460 L622 476"/></g>')
    s += '<g stroke="#1b1309" stroke-width="7" fill="#e09440">'
    for ax, ay, rr in ((712, 492, 20), (754, 480, 18)):
        s += f'<ellipse cx="{ax}" cy="{ay}" rx="{rr}" ry="{rr-5}"/>'
    s += '</g>'
    # яблоко тонкими ломтиками веером
    for i in range(5):
        x = 790 + i * 26
        y = 456 + (i % 2) * 8
        s += (f'<g transform="rotate({-16 + i * 7} {x} {y})">'
              f'<path d="M{x-22} {y+30} C{x-28} {y-6} {x-10} {y-26} {x+8} {y-26}'
              f' C{x+26} {y-26} {x+36} {y-4} {x+30} {y+30} Z" fill="#f6ecd6"'
              ' stroke="#1b1309" stroke-width="7" stroke-linejoin="round"/>'
              f'<path d="M{x-16} {y+26} C{x-20} {y-2} {x-6} {y-18} {x+6} {y-18}" stroke="#c3281f"'
              ' stroke-width="5" fill="none" opacity=".75"/></g>')
    s += A.candle(130, 346, t, 62, 44, phase=.25, s=.76)
    s += A.confetti(t, 11, seed=309)
    return s


def goat_milk(t):
    """Молоко она отдаёт добровольно: коза рядом с кувшином и стаканом молока."""
    s = '<rect width="960" height="540" fill="url(#room)"/>'
    s += window(120, 54, 182, 206, t)
    s += '<ellipse cx="214" cy="190" rx="170" ry="140" fill="url(#candle)" opacity=".4"/>'
    s += tree(852, 300, t, 0.46, 0.4)
    s += _garland(t, 10)
    s += table(352)
    s += '<ellipse cx="520" cy="506" rx="300" ry="30" fill="#1b0f07" opacity=".3"/>'
    s += _goat_side(290, 318, t, .2)
    # кувшин и стакан — крупно, рядом с козой
    s += '<g transform="translate(-40,-26) scale(1.34) translate(-150,-120)">'
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M596 500 C576 476 574 432 590 406 C600 390 622 384 646 384 C670 384 692 390 702 406'
          ' C718 432 716 476 696 500 Z" fill="#b5622f"/>'
          '<path d="M590 406 C606 396 686 396 702 406 C686 416 606 416 590 406 Z" fill="#cf7a3e"/>'
          '<path d="M702 414 C734 418 744 448 728 470 C720 480 706 482 700 476" fill="none"/></g>'
          '<g stroke="#8a4520" stroke-width="5" fill="none" opacity=".6">'
          '<path d="M586 440 C620 432 672 432 706 440 M590 466 C622 460 670 460 702 466"/></g>')
    # стакан молока, молоко чуть колышется
    lv = 2.5 * A.w(t, 3.6, .3)
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M782 504 L772 414 L866 414 L856 504 Z" fill="url(#glass)"/></g>'
          f'<path d="M776 {450 + lv:.1f} L862 {446 - lv:.1f} L856 500 L782 500 Z" fill="#f6f2e8"/>')
    s += ('<path d="M782 462 L790 496" stroke="#fff" stroke-width="6" opacity=".5"/>')
    # капля молока падает
    p = (t / 2.6) % 1.0
    s += f'<circle cx="724" cy="{432 + 56 * p:.0f}" r="{6 * (1 - p * 0.4):.1f}" fill="#f6f2e8" opacity="{1 - p:.2f}"/>'
    s += '</g>'
    s += A.candle(176, 396, t, 72, 50)
    s += A.confetti(t, 11, seed=311)
    return s


def pumpkin_raw(t):
    """До готовки: тыква крупными дольками, масло, розмарин, нож."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(850, 92, 17, "#ffd45e"), (748, 130, 13, "#ff8c6b"), (902, 162, 12, "#9ae06a")])
    s += tree(98, 290, t, 0.44, 0.36, star=False)
    s += _garland(t, 10)
    s += table(338)
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<rect x="52" y="394" width="820" height="126" rx="18" fill="#b07d3f"/></g>'
          '<g stroke="#8a5c2a" stroke-width="4" opacity=".5"><path d="M78 422 L846 422 M78 496 L846 496"/></g>')
    # половина тыквы со срезом и семечками
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M98 486 C98 428 142 392 196 392 C250 392 294 428 294 486 Z" fill="#e07f23"/>'
          '<path d="M98 486 C98 442 142 414 196 414 C250 414 294 442 294 486 Z" fill="#f0a24a"/></g>'
          '<g fill="#f6e0bc" stroke="#1b1309" stroke-width="4">'
          '<ellipse cx="166" cy="452" rx="10" ry="14" transform="rotate(-16 166 452)"/>'
          '<ellipse cx="196" cy="442" rx="10" ry="14"/>'
          '<ellipse cx="226" cy="452" rx="10" ry="14" transform="rotate(16 226 452)"/>'
          '<ellipse cx="182" cy="474" rx="9" ry="13" transform="rotate(-8 182 474)"/>'
          '<ellipse cx="212" cy="474" rx="9" ry="13" transform="rotate(8 212 474)"/></g>'
          '<path d="M196 392 C198 374 208 364 222 362" stroke="#4e7a35" stroke-width="10"'
          ' fill="none" stroke-linecap="round"/>')
    # четыре крупные дольки в ряд, блестят от масла
    for i in range(4):
        x = 366 + i * 102
        y = 468 - (i % 2) * 8
        rot = -10 + i * 6
        s += (f'<g transform="rotate({rot} {x} {y})">'
              f'<path d="M{x-54} {y+26} C{x-62} {y-10} {x-30} {y-40} {x+6} {y-40}'
              f' C{x+42} {y-40} {x+62} {y-12} {x+52} {y+26} Z" fill="#e8933a"'
              ' stroke="#1b1309" stroke-width="8" stroke-linejoin="round"/>'
              f'<path d="M{x-44} {y+22} C{x-50} {y-6} {x-26} {y-28} {x+4} {y-28}'
              f' C{x+34} {y-28} {x+50} {y-8} {x+42} {y+22} Z" fill="#f2ad58"/>'
              f'<path d="M{x-50} {y+26} C{x-20} {y+18} {x+20} {y+18} {x+48} {y+26}" stroke="#2f6b2a"'
              ' stroke-width="8" fill="none"/>')
        o = .35 + .4 * (0.5 + 0.5 * A.w(t, 2.4 + i * .5, i * .3))
        s += f'<ellipse cx="{x-14}" cy="{y-14}" rx="14" ry="7" fill="#fff" opacity="{o*0.5:.2f}" transform="rotate(-24 {x-14} {y-14})"/></g>'
    # бутылочка масла и розмарин
    s += _bottle(810, 418, "#6b8f35", 64)
    a = A.sway(t, 5.8, .4, 1.6)
    s += (f'<g transform="rotate({a:.2f} 560 510)">'
          '<g stroke="#43703a" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M560 510 L676 486"/>'
          '<path d="M578 504 L570 486 M602 498 L594 480 M626 492 L620 474 M650 488 L646 470"/></g></g>')
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M696 516 L838 486 L842 508 L700 534 Z" fill="#cfc8bd"/></g>')
    s += A.candle(898, 332, t, 62, 44, phase=.35, s=.78)
    s += A.confetti(t, 10, seed=313)
    return s


def pumpkin_topping(t):
    """Подача: на дольках тыквы крошка козьего сыра, зёрна граната, мята, мёд."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(132, 86, 18, "#ffd45e"), (252, 126, 13, "#ff8c6b"), (58, 158, 12, "#9ae06a")])
    s += tree(858, 284, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(330)
    s += _plate_oval(470, 452, 356, 86, "#cbb79a", "#e8dac0")
    for i in range(3):
        x = 288 + i * 182
        y = 452 - (i % 2) * 10
        rot = -12 + i * 12
        s += f'<g transform="rotate({rot} {x} {y})">'
        s += (f'<path d="M{x-80} {y+36} C{x-90} {y-12} {x-44} {y-52} {x+8} {y-52}'
              f' C{x+60} {y-52} {x+90} {y-14} {x+76} {y+36} Z" fill="#d97a26"'
              ' stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
              f'<path d="M{x-66} {y+30} C{x-74} {y-6} {x-36} {y-38} {x+6} {y-38}'
              f' C{x+48} {y-38} {x+74} {y-10} {x+62} {y+30} Z" fill="#ef9b3c"/>'
              f'<path d="M{x-74} {y+36} C{x-34} {y+26} {x+30} {y+26} {x+70} {y+36}" stroke="#2f6b2a"'
              ' stroke-width="9" fill="none"/>')
        # крошка козьего сыра
        s += '<g fill="#fbf8f0" stroke="#1b0f07" stroke-width="4">'
        for dx, dy, rr in ((-40, -16, 11), (-8, -28, 13), (26, -14, 12), (6, 2, 10), (-24, 6, 9), (44, 4, 9)):
            s += f'<rect x="{x+dx-rr:.0f}" y="{y+dy-rr:.0f}" width="{rr*2}" height="{rr*1.6:.0f}" rx="4"/>'
        s += '</g>'
        # зёрна граната
        s += '<g fill="#b5102a" stroke="#1b0f07" stroke-width="3">'
        for dx, dy in ((-54, 2), (-20, -8), (14, -24), (40, -22), (56, 12), (-2, 16), (30, 16), (-38, -30)):
            s += f'<circle cx="{x+dx}" cy="{y+dy}" r="7"/>'
        s += '</g>'
        # листики мяты
        for k, (dx, dy, r2) in enumerate(((-30, -40, -20), (34, -42, 18))):
            a = A.sway(t, 6.0, k * .4 + i * .2, 1.6)
            s += (f'<g transform="rotate({r2 + a:.2f} {x+dx} {y+dy})">'
                  f'<path d="M{x+dx-22} {y+dy+8} C{x+dx-16} {y+dy-16} {x+dx+10} {y+dy-20} {x+dx+22} {y+dy-6}'
                  f' C{x+dx+8} {y+dy+12} {x+dx-10} {y+dy+14} {x+dx-22} {y+dy+8} Z" fill="#5e9a4a"'
                  ' stroke="#1b0f07" stroke-width="6" stroke-linejoin="round"/></g>')
        s += '</g>'
    # мёд стекает струйкой сверху
    dz = 9 * A.w(t, 4.0, .2)
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<ellipse cx="640" cy="318" rx="46" ry="26" fill="#d8982a" transform="rotate(16 640 318)"/>'
          '<path d="M604 306 L528 268" stroke="#8a6a3a" stroke-width="12" fill="none" stroke-linecap="round"/></g>')
    s += (f'<path d="M660 342 C{668+dz:.0f} 372 {654+dz:.0f} 394 664 416" stroke="#d8982a"'
          ' stroke-width="12" fill="none" stroke-linecap="round" opacity=".92"/>')
    s += A.smoke(300, 380, t, 3, 130, .8, .2)
    s += A.candle(136, 344, t, 62, 44, phase=.2, s=.78)
    s += A.confetti(t, 11, seed=315)
    return s


def mushrooms_pan(t):
    """Процесс: грибы с луком на сковороде, пар, чеснок, тимьян, грецкие орехи."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(846, 90, 17, "#ffd45e"), (744, 128, 13, "#ff8c6b"), (900, 160, 12, "#9ae06a")])
    s += tree(96, 288, t, 0.42, 0.34, star=False)
    s += _garland(t, 10)
    s += table(336)
    s += '<ellipse cx="430" cy="506" rx="290" ry="30" fill="#1b0f07" opacity=".3"/>'
    # чугунная сковорода с ручкой
    s += ('<g stroke="#1b1309" stroke-width="10" stroke-linejoin="round">'
          '<path d="M700 420 L884 388 L890 414 L706 448 Z" fill="#3a3028"/>'
          '<ellipse cx="420" cy="446" rx="270" ry="78" fill="#2e2620"/>'
          '<ellipse cx="420" cy="440" rx="244" ry="64" fill="#4a3c30"/></g>')
    # грибы: шляпки половинками и целые
    for i, (x, y, sc, rot) in enumerate(((268, 432, 1.0, -10), (360, 452, .9, 6), (452, 428, 1.05, 12),
                                         (548, 450, .92, -8), (632, 432, .85, 16), (320, 404, .78, -4),
                                         (500, 400, .72, 8))):
        s += (f'<g transform="rotate({rot} {x} {y}) translate({x},{y}) scale({sc})">'
              '<path d="M-44 6 C-48 -22 -24 -40 2 -40 C28 -40 50 -22 46 6 C28 16 -26 16 -44 6 Z"'
              ' fill="#c99a63" stroke="#1b1309" stroke-width="8" stroke-linejoin="round"/>'
              '<path d="M-34 2 C-36 -16 -18 -30 2 -30 C22 -30 38 -16 36 2 C22 8 -22 8 -34 2 Z" fill="#e0b584"/>'
              '<path d="M-14 8 C-14 24 -12 32 -4 36 L8 36 C14 30 14 22 14 8 Z" fill="#efe0c6"'
              ' stroke="#1b1309" stroke-width="7" stroke-linejoin="round"/></g>')
    # кольца лука
    for x, y, rx in ((308, 470, 44), (486, 476, 40), (596, 468, 36)):
        s += (f'<g stroke="#1b1309" stroke-width="7" fill="none">'
              f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*0.36:.0f}" fill="#f0e6d6" opacity=".95"/>'
              f'<ellipse cx="{x}" cy="{y}" rx="{rx*0.6:.0f}" ry="{rx*0.22:.0f}" fill="#4a3c30"/></g>')
    # масло шипит: блики
    for i, (gx, gy) in enumerate(((240, 470), (400, 480), (560, 486), (660, 462))):
        o = .2 + .5 * (0.5 + 0.5 * A.w(t, 1.6 + i * .4, i * .3))
        s += f'<ellipse cx="{gx}" cy="{gy}" rx="12" ry="5" fill="#ffd98a" opacity="{o:.2f}"/>'
    s += A.smoke(330, 380, t, 4, 180, 1.0, .26)
    s += A.smoke(520, 372, t, 3, 160, .9, .2)
    # чеснок, тимьян и орехи рядом
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M118 512 C98 492 100 462 120 448 C140 434 166 442 174 464 C182 488 164 512 140 516 Z"'
          ' fill="#f0e8dc"/>'
          '<path d="M140 448 C142 434 150 426 162 424" stroke="#9a8a6a" stroke-width="8" fill="none"/></g>'
          '<g stroke="#cfc4b2" stroke-width="4" fill="none" opacity=".9">'
          '<path d="M122 500 C130 480 134 462 142 452 M152 504 C154 482 152 464 146 452"/></g>')
    a = A.sway(t, 5.6, .3, 1.5)
    s += (f'<g transform="rotate({a:.2f} 166 520)">'
          '<g stroke="#43703a" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M166 520 L262 498"/><path d="M182 514 L176 498 M206 508 L200 492 M230 502 L226 486"/></g></g>')
    s += '<g stroke="#1b1309" stroke-width="7" fill="#b07d3f">'
    for nx, ny, rr in ((782, 490, 20), (826, 502, 17)):
        s += f'<circle cx="{nx}" cy="{ny}" r="{rr}"/>'
    s += '</g><g stroke="#7a5324" stroke-width="4" fill="none" opacity=".85">'
    for nx, ny, rr in ((782, 490, 20), (826, 502, 17)):
        s += f'<path d="M{nx-rr+4} {ny} L{nx+rr-4} {ny}"/><path d="M{nx} {ny-rr+5} C{nx+7} {ny} {nx-7} {ny} {nx} {ny+rr-5}"/>'
    s += '</g>'
    s += A.candle(886, 336, t, 60, 42, phase=.5, s=.74)
    s += A.confetti(t, 10, seed=317)
    return s


def pate_toast(t):
    """Подача: паштет на поджаренном хлебе с зеленью и каплей масла."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(130, 84, 18, "#ffd45e"), (250, 124, 13, "#ff8c6b"), (56, 156, 12, "#9ae06a")])
    s += tree(858, 282, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(330)
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M64 390 L864 390 C898 390 912 408 912 434 L912 466 C912 494 892 508 858 508'
          ' L64 508 C34 508 20 494 20 466 L20 434 C20 408 34 390 64 390 Z" fill="#a9762f"/></g>')
    # три тоста
    for i in range(3):
        x = 196 + i * 256
        y = 448 + (i % 2) * 6
        rot = -6 + i * 5
        s += f'<g transform="rotate({rot} {x} {y})">'
        s += (f'<path d="M{x-104} {y+42} C{x-112} {y-4} {x-72} {y-34} {x-6} {y-34}'
              f' C{x+62} {y-34} {x+104} {y-6} {x+96} {y+42} Z" fill="#c98f46"'
              ' stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
              f'<path d="M{x-94} {y+16} C{x-98} {y-10} {x-64} {y-26} {x-4} {y-26}'
              f' C{x+56} {y-26} {x+92} {y-8} {x+86} {y+16} Z" fill="#e0b069"/>')
        # паштет сверху, волной
        s += (f'<path d="M{x-88} {y+8} C{x-74} {y-20} {x-40} {y-16} {x-18} {y-26}'
              f' C{x+6} {y-36} {x+42} {y-22} {x+62} {y-18} C{x+78} {y-14} {x+86} {y-2} {x+82} {y+10}'
              f' C{x+40} {y+22} {x-50} {y+22} {x-88} {y+8} Z" fill="#8a6246"'
              ' stroke="#1b0f07" stroke-width="8" stroke-linejoin="round"/>'
              f'<path d="M{x-72} {y-2} C{x-52} {y-16} {x-16} {y-14} {x+10} {y-20}'
              f' C{x+38} {y-26} {x+60} {y-12} {x+70} {y-4}" stroke="#a3795a" stroke-width="6"'
              ' fill="none" opacity=".85"/>')
        # зелень и капля масла
        for k, (dx, dy, r2) in enumerate(((-40, -30, -22), (28, -34, 16))):
            a = A.sway(t, 6.2, k * .4 + i * .25, 1.5)
            s += (f'<g transform="rotate({r2 + a:.2f} {x+dx} {y+dy})">'
                  f'<path d="M{x+dx-20} {y+dy+6} C{x+dx-14} {y+dy-14} {x+dx+10} {y+dy-18} {x+dx+20} {y+dy-4}'
                  f' C{x+dx+6} {y+dy+12} {x+dx-10} {y+dy+12} {x+dx-20} {y+dy+6} Z" fill="#5e9a4a"'
                  ' stroke="#1b0f07" stroke-width="6" stroke-linejoin="round"/></g>')
        o = .4 + .4 * (0.5 + 0.5 * A.w(t, 2.6 + i * .5, i * .3))
        s += f'<ellipse cx="{x+8}" cy="{y-6}" rx="13" ry="7" fill="#ffd98a" opacity="{o*0.6:.2f}"/>'
        s += '</g>'
    # пиала паштета с ножом
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M368 372 L584 372 C580 404 556 420 476 420 C396 420 372 404 368 372 Z" fill="#dccbab"/>'
          '<path d="M380 380 L572 380 C566 400 544 410 476 410 C408 410 386 400 380 380 Z" fill="#8a6246"/></g>')
    s += A.smoke(476, 356, t, 3, 110, .7, .18)
    s += A.candle(124, 344, t, 62, 44, phase=.3, s=.76)
    s += A.confetti(t, 11, seed=319)
    return s


def duck_spices(t):
    """Добавим огня: соль, молотый имбирь, корица и апельсиновая цедра."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(846, 88, 17, "#ffd45e"), (744, 128, 13, "#ff8c6b"), (900, 160, 12, "#9ae06a")])
    s += tree(98, 286, t, 0.44, 0.36, star=False)
    s += _garland(t, 10)
    s += table(334)
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<rect x="46" y="396" width="868" height="124" rx="18" fill="#a8702f"/></g>'
          '<g stroke="#8a5c2a" stroke-width="4" opacity=".5"><path d="M72 424 L888 424 M72 496 L888 496"/></g>')
    # четыре блюдца со специями
    for i, (x, col, dark) in enumerate(((158, "#f2ece0", "#d8d2c4"), (334, "#d08a2a", "#b06f1c"),
                                        (510, "#8a4a22", "#6b3414"), (686, "#e07f23", "#c06a1e"))):
        s += (f'<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
              f'<ellipse cx="{x}" cy="{466}" rx="76" ry="32" fill="#dccbab"/>'
              f'<ellipse cx="{x}" cy="{460}" rx="64" ry="24" fill="{col}"/></g>')
        s += f'<g fill="{dark}" opacity=".8">'
        for dx, dy, rr in ((-28, 456, 7), (-6, 464, 6), (18, 454, 7), (36, 464, 5), (4, 450, 5)):
            s += f'<circle cx="{x+dx}" cy="{dy}" r="{rr}"/>'
        s += '</g>'
    # палочки корицы
    for x, y, rot in ((486, 418, -14), (534, 410, 8)):
        s += (f'<g transform="rotate({rot} {x} {y})">'
              f'<rect x="{x-14}" y="{y-44}" width="28" height="88" rx="12" fill="#8a4a22"'
              ' stroke="#1b1309" stroke-width="8"/>'
              f'<path d="M{x-6} {y-40} L{x-6} {y+40}" stroke="#6b3414" stroke-width="6" opacity=".8"/></g>')
    # апельсин разрезан и стружка цедры
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<circle cx="812" cy="440" r="62" fill="#f0921f"/>'
          '<circle cx="812" cy="440" r="48" fill="#ffb455"/></g>'
          '<g stroke="#f0921f" stroke-width="6" fill="none" opacity=".9">'
          '<path d="M812 394 L812 486 M770 414 L854 466 M770 466 L854 414"/></g>')
    for i, (x, y, rot) in enumerate(((228, 424, -20), (272, 412, 14), (196, 408, 8))):
        a = A.sway(t, 6.4, i * .3, 1.2)
        s += (f'<g transform="rotate({rot + a:.2f} {x} {y})">'
              f'<path d="M{x-30} {y} C{x-18} {y-18} {x+12} {y-20} {x+30} {y-6}'
              f' C{x+14} {y+6} {x-14} {y+10} {x-30} {y} Z" fill="#f0921f"'
              ' stroke="#1b1309" stroke-width="6" stroke-linejoin="round"/></g>')
    # утка силуэтом на заднем плане
    s += ('<g opacity=".5">'
          '<ellipse cx="620" cy="360" rx="150" ry="46" fill="#6d300b"/>'
          '<path d="M700 338 C716 318 742 312 756 322 C742 330 736 344 740 356 C724 362 706 356 700 346 Z"'
          ' fill="#6d300b"/></g>')
    s += A.candle(900, 334, t, 62, 44, phase=.4, s=.78)
    s += A.confetti(t, 11, seed=321)
    return s


def duck_glaze(t):
    """Кожа стала тёмной и блестящей: мёд с соевым соусом, кисточка, блеск."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(128, 82, 18, "#ffd45e"), (248, 122, 13, "#ff8c6b"), (56, 154, 12, "#9ae06a")])
    s += tree(856, 280, t, 0.46, 0.4, star=False)
    s += _garland(t, 10)
    s += table(328)
    s += _plate_oval(470, 456, 374, 88, "#cbb79a", "#e8dac0")
    # тушка: тёмная блестящая кожа
    s += ('<g stroke="#1b0806" stroke-width="10" stroke-linejoin="round">'
          '<path d="M196 456 C188 404 240 360 326 350 C412 340 514 346 590 366 C652 382 690 410 684 446'
          ' C678 478 588 494 450 496 C306 498 206 488 196 456 Z" fill="#5e2608"/>'
          # крыло прижато к боку
          '<path d="M300 408 C342 382 418 372 486 382 C452 404 388 420 320 424 Z" fill="#9a4a14"/>'
          # ножка с косточкой
          '<path d="M612 430 C656 414 702 414 722 428 C736 438 732 456 714 460 C690 466 640 458 612 448 Z"'
          ' fill="#8a3c10"/>'
          '<path d="M716 428 C738 418 760 424 762 438 C764 452 746 460 728 456" fill="#efe6d2"/></g>'
          '<path d="M244 424 C262 390 330 370 406 366 C486 362 568 376 630 396 C576 382 470 376 384 386'
          ' C312 394 266 406 244 424 Z" fill="#8a3c10"/>')
    # шея и голова с клювом — чтобы читалась птица, а не бурый холм
    s += ('<g stroke="#1b0806" stroke-width="10" stroke-linejoin="round">'
          '<path d="M238 368 C222 322 214 282 226 252 C206 246 186 272 190 308 C193 338 210 362 226 376 Z"'
          ' fill="#5e2608"/>'
          '<path d="M226 252 C208 232 182 230 168 244 C154 258 158 282 176 290 C196 298 220 284 226 266 Z"'
          ' fill="#6b2c08"/></g>'
          '<path d="M168 262 L120 272 L166 284 Z" fill="#c9922f" stroke="#1b0806" stroke-width="8"'
          ' stroke-linejoin="round"/>'
          '<circle cx="196" cy="258" r="7" fill="#1b0806"/>')
    # блеск бежит по коже
    ph = (t / 3.6) % 1.0
    gx = 230 + 420 * ph
    s += (f'<ellipse cx="{gx:.0f}" cy="410" rx="70" ry="22" fill="#ffd98a"'
          f' opacity="{0.34 * (1 - abs(ph - .5) * 1.2):.2f}" transform="rotate(-8 {gx:.0f} 410)"/>')
    for i, (bx, by, rr) in enumerate(((330, 396, 13), (452, 388, 15), (556, 402, 12), (248, 428, 10))):
        o = .25 + .45 * (0.5 + 0.5 * A.w(t, 2.2 + i * .5, i * .3))
        s += f'<ellipse cx="{bx}" cy="{by}" rx="{rr}" ry="{rr*0.5:.0f}" fill="#ffe3a8" opacity="{o:.2f}"/>'
    # кисточка смазывает
    br = 10 * A.w(t, 2.8, .1)
    s += (f'<g transform="translate({br:.1f},{-br*0.6:.1f})">'
          '<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<rect x="548" y="196" width="34" height="112" rx="10" fill="#6b4320"/>'
          '<path d="M546 306 L584 306 L590 362 L540 362 Z" fill="#c98f46"/></g>'
          '<g stroke="#a3703a" stroke-width="5" fill="none" opacity=".85">'
          '<path d="M552 318 L548 356 M566 318 L566 356 M580 318 L582 356"/></g></g>')
    dz = 7 * A.w(t, 4.2, .3)
    s += (f'<path d="M564 366 C{570+dz:.0f} 386 {558+dz:.0f} 400 566 414" stroke="#8a5a1c"'
          ' stroke-width="10" fill="none" stroke-linecap="round" opacity=".9"/>')
    # пиала соуса
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M726 462 L896 462 C892 506 868 524 810 524 C752 524 730 506 726 462 Z" fill="#dccbab"/>'
          '<path d="M738 474 L884 474 C878 504 856 514 810 514 C764 514 744 504 738 474 Z" fill="#3a2008"/></g>')
    s += A.smoke(420, 356, t, 3, 150, .9, .22)
    s += A.candle(126, 342, t, 62, 44, phase=.2, s=.78)
    s += A.confetti(t, 11, seed=323)
    return s


def fish_steam(t):
    """Рыба целиком на пару: бамбуковая пароварка, имбирь и зелёный лук, соус."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(848, 90, 17, "#ffd45e"), (746, 128, 13, "#ff8c6b"), (902, 160, 12, "#9ae06a")])
    s += tree(96, 288, t, 0.42, 0.34, star=False)
    s += _garland(t, 10)
    s += table(334)
    s += '<ellipse cx="450" cy="512" rx="300" ry="28" fill="#1b0f07" opacity=".3"/>'
    # круглая бамбуковая пароварка: плетёный борт
    s += ('<g stroke="#1b1309" stroke-width="10" stroke-linejoin="round">'
          '<ellipse cx="450" cy="462" rx="310" ry="76" fill="#b08a4a"/>'
          '<ellipse cx="450" cy="446" rx="290" ry="62" fill="#c99a5a"/>'
          '<ellipse cx="450" cy="448" rx="250" ry="48" fill="#e6dcc6"/></g>'
          '<g stroke="#8a6a32" stroke-width="5" fill="none" opacity=".7">')
    for i in range(13):
        x = 160 + i * 48
        s += f'<path d="M{x} 442 C{x+8} 470 {x+8} 490 {x} 506"/>'
    s += '</g>'
    # рыба целиком, с головой и хвостом
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M250 448 C300 406 420 394 520 404 C600 412 650 428 672 444 C650 462 600 476 520 484'
          ' C420 494 300 482 250 448 Z" fill="#cfd6d2"/>'
          '<path d="M250 448 C214 428 190 418 168 416 C178 436 178 462 168 482 C192 478 216 468 250 448 Z"'
          ' fill="#b8c0bc"/>'
          '<path d="M398 400 C420 376 446 370 462 380 C446 388 438 398 438 408 Z" fill="#b8c0bc"/></g>'
          '<circle cx="612" cy="436" r="13" fill="#f6f2e8" stroke="#1b1309" stroke-width="6"/>'
          '<circle cx="614" cy="437" r="6" fill="#1b1309"/>'
          '<path d="M576 424 C586 436 586 450 576 462" stroke="#1b1309" stroke-width="7" fill="none"/>'
          '<g stroke="#9aa6a0" stroke-width="5" fill="none" opacity=".85">'
          '<path d="M320 434 C360 424 420 420 470 424 M330 460 C370 468 430 470 480 464"/></g>')
    # ломтики имбиря и зелёный лук сверху
    for i, (x, y, rot) in enumerate(((360, 426, -14), (430, 418, 10), (496, 430, -6))):
        s += (f'<g transform="rotate({rot} {x} {y})">'
              f'<ellipse cx="{x}" cy="{y}" rx="26" ry="14" fill="#e8c88a"'
              ' stroke="#1b1309" stroke-width="6"/></g>')
    for i, (x, y) in enumerate(((330, 452), (420, 446), (510, 456), (470, 464))):
        a = A.sway(t, 5.8, i * .3, 1.4)
        s += (f'<g transform="rotate({a:.2f} {x} {y})">'
              f'<path d="M{x-46} {y+6} C{x-20} {y-8} {x+18} {y-10} {x+46} {y-2}" stroke="#4e9a3a"'
              ' stroke-width="9" fill="none" stroke-linecap="round"/></g>')
    # пар валит
    s += A.smoke(330, 390, t, 4, 220, 1.1, .3)
    s += A.smoke(470, 376, t, 4, 240, 1.2, .26)
    s += A.smoke(580, 396, t, 3, 200, 1.0, .22)
    # соус и кунжут
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M782 486 L910 486 C906 518 886 532 846 532 C806 532 786 518 782 486 Z" fill="#dccbab"/>'
          '<path d="M792 496 L900 496 C896 518 878 524 846 524 C814 524 796 518 792 496 Z" fill="#3a2008"/></g>'
          '<g fill="#f6ecd0" stroke="#1b1309" stroke-width="3">'
          '<ellipse cx="816" cy="500" rx="6" ry="4"/><ellipse cx="846" cy="506" rx="6" ry="4"/>'
          '<ellipse cx="872" cy="500" rx="6" ry="4"/></g>')
    s += A.candle(888, 336, t, 60, 42, phase=.45, s=.74)
    s += A.confetti(t, 10, seed=325)
    return s


def apple_cream(t):
    """Тёплое яблоко, холодный творожный крем, хруст граната."""
    s = '<rect width="960" height="540" fill="url(#roomc)"/>'
    s += _boke([(846, 88, 17, "#ffd45e"), (744, 126, 13, "#ff8c6b"), (900, 158, 12, "#9ae06a")])
    s += tree(98, 288, t, 0.44, 0.36, star=False)
    s += _garland(t, 10)
    s += table(332)
    s += _plate_oval(470, 456, 330, 82, "#cfbf9f", "#f1ece0")
    # два печёных яблока, слегка лопнувшие
    for i, (x, y, sc) in enumerate(((356, 432, 1.0), (574, 442, .9))):
        s += (f'<g transform="translate({x},{y}) scale({sc})">'
              '<path d="M-74 22 C-86 -14 -62 -48 -22 -52 C-6 -54 6 -48 20 -50 C58 -56 84 -26 76 14'
              ' C70 46 36 66 -4 66 C-44 66 -66 48 -74 22 Z" fill="#b8431f"'
              ' stroke="#1b0f07" stroke-width="9" stroke-linejoin="round"/>'
              '<path d="M-58 10 C-66 -14 -48 -38 -18 -40 C-4 -42 8 -36 20 -38 C48 -42 66 -22 60 6'
              ' C54 30 28 46 -2 46 C-32 46 -52 32 -58 10 Z" fill="#d8632c" opacity=".8"/>'
              '<path d="M-22 -50 C-20 -66 -10 -76 4 -78" stroke="#4e3a1c" stroke-width="9"'
              ' fill="none" stroke-linecap="round"/>'
              '<path d="M-30 -2 C-12 -12 10 -10 26 0 C10 8 -14 8 -30 -2 Z" fill="#8a2c12"/></g>')
    # творожный крем ложкой поверх
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<path d="M300 414 C310 386 348 374 382 384 C404 390 416 378 440 382 C470 388 480 414 464 430'
          ' C438 452 324 448 300 414 Z" fill="#fbf8f0"/>'
          '<path d="M520 424 C530 400 562 390 592 398 C614 404 626 396 644 402 C664 410 668 430 652 442'
          ' C626 460 540 452 520 424 Z" fill="#fbf8f0"/></g>'
          '<g stroke="#e4ddcc" stroke-width="5" fill="none" opacity=".9">'
          '<path d="M322 408 C346 394 382 396 406 406 M540 418 C564 404 598 406 620 416"/></g>')
    # гранатовые зёрна
    s += '<g fill="#b5102a" stroke="#1b0f07" stroke-width="3">'
    for px, py in ((330, 400), (368, 390), (406, 398), (438, 392), (548, 410), (586, 402),
                   (620, 410), (300, 466), (470, 486), (690, 470), (250, 478)):
        s += f'<circle cx="{px}" cy="{py}" r="8"/>'
    s += '</g>'
    # палочка ванили и мята
    s += ('<g stroke="#1b1309" stroke-width="7" stroke-linejoin="round">'
          '<path d="M700 496 C736 486 776 480 812 482 L810 500 C774 500 736 506 702 514 Z" fill="#3a2614"/></g>')
    for k, (x, y, rot) in enumerate(((228, 442, -18), (716, 436, 14))):
        a = A.sway(t, 6.0, k * .4, 1.6)
        s += (f'<g transform="rotate({rot + a:.2f} {x} {y})">'
              f'<path d="M{x-26} {y+8} C{x-18} {y-18} {x+12} {y-24} {x+26} {y-6}'
              f' C{x+10} {y+14} {x-12} {y+16} {x-26} {y+8} Z" fill="#5e9a4a"'
              ' stroke="#1b0f07" stroke-width="7" stroke-linejoin="round"/>'
              f'<path d="M{x-20} {y+4} C{x-6} {y-6} {x+8} {y-10} {x+20} {y-6}" stroke="#43703a"'
              ' stroke-width="5" fill="none"/></g>')
    s += A.smoke(356, 372, t, 3, 120, .7, .2)
    s += A.candle(126, 340, t, 62, 44, phase=.3, s=.76)
    s += A.confetti(t, 11, seed=327)
    return s


def koza_mane(t):
    """Огненная грива во весь кадр: вихрь пламени, искры, край рога и глаз."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    pulse = .22 + .1 * A.w(t, 1.7)
    s += f'<ellipse cx="480" cy="300" rx="620" ry="420" fill="#d9601a" opacity="{pulse:.2f}"/>'
    # три слоя языков пламени, каждый дышит в своём ритме
    for i, (cx, cy, sc, per, col) in enumerate(((300, 330, 1.00, 1.9, "url(#fl2)"),
                                                (520, 300, 1.18, 1.5, "url(#fl1)"),
                                                (740, 350, 0.92, 2.2, "url(#fl2)"))):
        p = 1 + .05 * A.w(t, per, i * .3)
        q = 1 + .08 * A.w(t, per * 1.3, i * .5)
        s += (f'<g transform="translate({cx},{cy}) scale({sc * p:.3f},{sc * q:.3f})">'
              '<g stroke="#2a1105" stroke-width="8" stroke-linejoin="round">'
              '<path d="M0 190 C70 60 30 -60 -70 -156 C80 -116 200 -20 206 126 C210 236 140 316 40 340 Z"'
              f' fill="{col}"/>'
              '<path d="M-120 200 C-60 100 -96 0 -170 -74 C-60 -42 20 36 18 142 C16 214 -40 266 -116 282 Z"'
              ' fill="url(#fl1)" opacity=".92"/></g></g>')
    # жар поднимается полосами — мягко, без чёрточек поперёк кадра
    for i in range(4):
        a = A.sway(t, 3.4 + i * .5, i * .3, 10.0)
        x0 = 150 + i * 220
        s += (f'<path d="M{x0} 560 C{x0 + 46 + a:.0f} 440 {x0 - 40 - a:.0f} 330 {x0 + 24:.0f} 210"'
              f' stroke="#ffd36e" stroke-width="{26 - i * 4}" fill="none"'
              f' opacity="{.16 - i * .02:.2f}" stroke-linecap="round"/>')
    # искры летят вверх
    for i in range(14):
        per = 2.2 + (i % 5) * .5
        p = ((t / per) + i * .137) % 1.0
        x = 60 + i * 66 + 24 * A.w(t, per * 1.6, i * .2)
        y = 540 - 540 * p
        r = 2.4 + (i % 4)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * (1 - p * .5):.1f}" fill="#ffd36e" opacity="{.85 * (1 - p):.2f}"/>'
    # край рога и жёлтый глаз в левом нижнем углу — чья это грива
    # чья это грива: морда уходит за левый край, видны рог и глаз
    s += ('<path d="M-60 540 C-20 430 70 356 190 320 C300 288 380 318 404 392'
          ' C428 466 372 532 268 540 Z" fill="#e9c99c" stroke="#2a1105" stroke-width="11"'
          ' stroke-linejoin="round"/>'
          '<path d="M118 332 C96 268 126 212 186 182 C216 166 244 178 248 200 C228 188 206 196 188 210'
          ' C146 244 132 288 140 338 Z" fill="#8e6436" stroke="#2a1105" stroke-width="10"'
          ' stroke-linejoin="round"/>'
          '<g stroke="#5c3d1c" stroke-width="6" fill="none" opacity=".85">'
          '<path d="M140 308 C158 292 176 280 192 270 M148 276 C166 260 184 248 200 242"/></g>')
    brow = 4 * A.w(t, 9.1, .4)
    s += (f'<path d="M150 {382+brow:.0f} C190 {360+brow:.0f} 250 {362+brow:.0f} 282 {384+brow:.0f}"'
          ' stroke="#2a1105" stroke-width="17" fill="none" stroke-linecap="round"/>')
    if A.blink(t, 4.3, .2):
        s += ('<path d="M156 432 C190 406 248 406 276 432" stroke="#2a1105" stroke-width="16"'
              ' fill="none" stroke-linecap="round"/>')
    else:
        look = 5 * A.w(t, 7.1, .3)
        s += ('<ellipse cx="216" cy="430" rx="62" ry="40" fill="#f7cb53" stroke="#2a1105" stroke-width="10"/>'
              f'<rect x="{182+look:.1f}" y="416" width="68" height="27" rx="12" fill="#2a1105"/>'
              f'<circle cx="{192+look:.1f}" cy="411" r="11" fill="#fff" opacity=".9"/>')
    s += A.confetti(t, 12, seed=329)
    return s


def cake_no(t):
    """Тяжёлый торт с жирным кремом — не в эту ночь."""
    s = '<rect width="960" height="540" fill="url(#roomb)"/>'
    s += _boke([(132, 86, 18, "#ffd45e"), (252, 126, 13, "#ff8c6b"), (58, 158, 12, "#9ae06a")])
    s += tree(862, 286, t, 0.44, 0.36, star=False)
    s += _garland(t, 10)
    s += table(336)
    s += '<ellipse cx="450" cy="512" rx="250" ry="26" fill="#1b0f07" opacity=".3"/>'
    # подставка
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M330 512 L570 512 L560 494 L340 494 Z" fill="#cfc8bd"/>'
          '<rect x="434" y="452" width="32" height="46" fill="#cfc8bd"/>'
          '<ellipse cx="450" cy="448" rx="200" ry="26" fill="#e4ddd2"/></g>')
    # три яруса с толстым кремом
    for i, (y, rx, col) in enumerate(((414, 176, "#e8c99a"), (354, 148, "#e8c99a"), (298, 118, "#e8c99a"))):
        s += (f'<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
              f'<rect x="{450-rx}" y="{y-6}" width="{rx*2}" height="52" rx="8" fill="{col}"/>'
              f'<rect x="{450-rx}" y="{y+16}" width="{rx*2}" height="16" fill="#a9743a"/></g>')
        # потёки крема
        s += f'<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round" fill="#fbf4e4">'
        for k in range(6):
            x = 450 - rx + 14 + k * (rx * 2 - 28) / 5
            d = 16 + (k % 3) * 10
            s += (f'<path d="M{x-22:.0f} {y-6} L{x+22:.0f} {y-6} L{x+22:.0f} {y+d} '
                  f'C{x+10:.0f} {y+d+14} {x-10:.0f} {y+d+14} {x-22:.0f} {y+d} Z"/>')
        s += '</g>'
    # розочки крема и вишни сверху
    s += '<g stroke="#1b1309" stroke-width="7" fill="#fbf4e4">'
    for rx2, ry2 in ((392, 290), (450, 282), (508, 290), (420, 300), (480, 300)):
        s += f'<circle cx="{rx2}" cy="{ry2}" r="20"/>'
    s += '</g><g stroke="#8a1020" stroke-width="5" fill="#c3281f">'
    for rx2, ry2 in ((392, 284), (450, 276), (508, 284)):
        s += f'<circle cx="{rx2}" cy="{ry2}" r="11"/>'
    s += '</g>'
    # жирный блик на креме
    o = .3 + .3 * (0.5 + 0.5 * A.w(t, 3.2, .2))
    s += f'<ellipse cx="408" cy="330" rx="40" ry="14" fill="#fff" opacity="{o*0.4:.2f}" transform="rotate(-12 408 330)"/>'
    s += _no_sign(450, 380, 176, t, 26)
    s += A.candle(136, 348, t, 60, 42, phase=.3, s=.74)
    s += A.confetti(t, 10, seed=331)
    return s


SCENES = {
    "open": open_newyear, "dish": dish, "table_top": table_top, "three": three_animals,
    "yang": yang, "cozy": cozy, "makers": makers, "koza": koza, "koza_fire": koza_fire,
    "koza_turn": koza_turn, "koza_table": koza_table, "koza_table_right": koza_table_right, "koza_eye": koza_eye,
    "koza_shadow": koza_shadow, "koza_far": koza_far,
    "guests": guests, "ded": ded, "horse": horse,
    "retro": retro, "retro_child": retro_child,
    "feast": feast, "heap": heap, "pork": pork, "koza_door": koza_door,
    "greens": greens,
    # часть 5 — семь опор стола
    "cheese": cheese, "pumpkin": pumpkin, "pumpkin_goat": pumpkin_goat, "pate": pate,
    "duck": duck, "fish": fish, "apples": apples, "mors": mors, "lamb_no": lamb_no,
    # часть 6 — ошибки стола и Восток
    "salat_mayo": salat_mayo, "two_floors": two_floors, "meat_only": meat_only,
    "lamb_dishes": lamb_dishes, "koza_head_table": koza_head_table,
    "round_fruits": round_fruits, "pelmeni_gold": pelmeni_gold, "pear_no": pear_no,
    "white_no": white_no, "calendar_feb": calendar_feb, "lanterns": lanterns,
    "kuranty": kuranty, "finale_2027": finale_2027, "koza_figure": koza_figure, "final_warm": final_warm,
    # варианты служебных кадров против сквозного повтора
    "guests_close": guests_close, "koza_window": koza_window, "koza_bokal": koza_bokal,
    "table_wide": table_wide, "koza_profile": koza_profile,
    "greens_board": greens_board, "duck_cut": duck_cut, "cheese_slice": cheese_slice,
    "guests_toast": guests_toast, "pumpkin_slice": pumpkin_slice,
    "fish_left": fish_left, "fish_serve": fish_serve, "fruit_basket": fruit_basket,
    # новые кадры против сквозного повтора (02.11)
    "basics_six": basics_six, "empty_plate": empty_plate, "seafood": seafood,
    "herb_glasses": herb_glasses, "herb_three": herb_three, "cheese_trio": cheese_trio, "honey_nuts": honey_nuts,
    "goat_milk": goat_milk, "pumpkin_raw": pumpkin_raw, "pumpkin_topping": pumpkin_topping,
    "mushrooms_pan": mushrooms_pan, "pate_toast": pate_toast, "duck_spices": duck_spices,
    "duck_glaze": duck_glaze, "fish_steam": fish_steam, "apple_cream": apple_cream,
    "koza_mane": koza_mane, "cake_no": cake_no,
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


# ---- второй ролик серии: новые персонажи и камера по глубине (art2.py) ----
try:
    import art2 as _a2
    SCENES.update(_a2.SCENES)
    NO_GLARE |= _a2.NO_GLARE
except Exception as _e:          # пробник не должен ронять уже принятые части
    print("art2 не подключён:", _e)

# ---- предметные кадры второго ролика, нарисованные заново (art3.py) ----
try:
    import art3 as _a3
    SCENES.update(_a3.SCENES)
    NO_GLARE |= _a3.NO_GLARE
except Exception as _e:
    print("art3 не подключён:", _e)

# ---- пробник рецепта: приготовление оливье (art4.py) ----
try:
    import art4 as _a4
    SCENES.update(_a4.SCENES)
    NO_GLARE |= _a4.NO_GLARE
except Exception as _e:
    print("art4 не подключён:", _e)
