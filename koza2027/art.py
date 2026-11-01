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
    s += _ded(392, 252, t, 0.92)
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
    s += A.candle(900, 420, t, 56, 42)
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
    # зелень на тостах качается
    for i, bx in enumerate((198, 404, 610)):
        a = A.sway(t, 5.2 + i * .5, i * .3, 2.6)
        s += (f'<g transform="rotate({a:.2f} {bx} 390)">'
              '<g stroke="#4e7a35" stroke-width="5" fill="none" stroke-linecap="round">'
              f'<path d="M{bx-8} 388 L{bx-18} 368 M{bx+8} 388 L{bx+18} 366"/></g>'
              '<g fill="#3f8c3c" stroke="#1b1309" stroke-width="3">'
              f'<circle cx="{bx-20}" cy="364" r="8"/><circle cx="{bx+22}" cy="362" r="7"/></g></g>')
    # грибы
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<path d="M772 500 L772 462 L812 462 L812 500 Z" fill="#cfae7e"/>'
          '<path d="M746 462 C746 424 768 404 792 404 C816 404 838 424 838 462 Z" fill="#9c6a3e"/>'
          '<path d="M858 504 L858 474 L888 474 L888 504 Z" fill="#cfae7e"/>'
          '<path d="M838 474 C838 444 856 428 874 428 C892 428 910 444 910 474 Z" fill="#8a5c34"/></g>'
          '<g stroke="#6e4a26" stroke-width="4" fill="none" opacity=".7">'
          '<path d="M762 440 C782 430 804 430 822 440 M848 456 C862 448 884 448 898 456"/></g>')
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
    """Опора 5: утка с апельсинами и имбирём. Кожа тёмная и блестящая, идёт пар."""
    s = '<rect width="960" height="540" fill="url(#roomr)"/>'
    s += _boke([(128, 76, 19, "#ffd45e"), (248, 118, 14, "#ff8c6b"),
                (56, 150, 13, "#9ae06a"), (352, 70, 11, "#7fd0ff")], ".32")
    s += tree(852, 262, t, 0.5, 0.45, star=False)
    s += _garland(t, 8)
    s += table(300)
    s += A.candle(90, 214, t, 78, 50, phase=.15)
    s += _plate_oval(500, 440, 386, 88, "#cbb79a", "#e8dac0")
    s += ('<g stroke="#1b0f07" stroke-width="10" stroke-linejoin="round">'
          '<path d="M248 418 C240 334 324 272 476 266 C640 260 748 312 756 390'
          ' C760 432 692 436 568 438 C416 440 282 446 248 418 Z" fill="url(#duck)"/>'
          '<path d="M744 362 C790 342 824 348 834 370 C820 388 784 392 752 384 Z" fill="#8f4210"/>'
          '<path d="M256 400 C222 388 200 396 196 414 C214 428 244 426 262 416 Z" fill="#8f4210"/></g>'
          '<path d="M320 320 C400 288 580 284 688 318" stroke="#d98a30" stroke-width="16"'
          ' fill="none" stroke-linecap="round" opacity=".8"/>'
          '<path d="M352 352 C440 326 596 324 676 352" stroke="#e8a44a" stroke-width="9"'
          ' fill="none" stroke-linecap="round" opacity=".6"/>')
    for i, (ex, ey, erx, ery) in enumerate(((420, 312, 44, 13), (572, 308, 38, 11))):
        o = .4 + .28 * (0.5 + 0.5 * A.w(t, 3.4 + i * .7, i * .35))
        s += f'<ellipse cx="{ex}" cy="{ey}" rx="{erx}" ry="{ery}" fill="#f2c073" opacity="{o:.2f}"/>'
    s += ('<g stroke="#6d300b" stroke-width="5" fill="none" opacity=".8">'
          '<path d="M360 300 L344 352 M420 288 L406 346 M484 282 L472 342'
          ' M548 284 L540 344 M612 294 L608 352"/></g>')
    # апельсины
    s += ('<g stroke="#1b0f07" stroke-width="8">'
          '<circle cx="214" cy="458" r="46" fill="#f0921f"/><circle cx="214" cy="458" r="31" fill="#ffb455"/>'
          '<circle cx="790" cy="454" r="44" fill="#f0921f"/><circle cx="790" cy="454" r="30" fill="#ffb455"/>'
          '<circle cx="560" cy="470" r="38" fill="#e8821a"/><circle cx="560" cy="470" r="25" fill="#ffab46"/></g>'
          '<g stroke="#e07f23" stroke-width="4" opacity=".9">'
          '<path d="M214 428 L214 488 M184 458 L244 458 M193 437 L235 479 M235 437 L193 479"/>'
          '<path d="M790 424 L790 484 M760 454 L820 454 M769 433 L811 475 M811 433 L769 475"/>'
          '<path d="M560 445 L560 495 M535 470 L585 470"/></g>')
    s += ('<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<path d="M330 470 C344 448 380 440 398 456 C380 478 348 486 330 470 Z" fill="#f2e8d2"/>'
          '<path d="M660 474 C674 452 710 444 728 460 C710 482 678 490 660 474 Z" fill="#f2e8d2"/></g>'
          '<g stroke="#c0203a" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M340 466 C354 452 376 448 392 456 M670 470 C684 456 706 452 722 460"/></g>')
    a = A.sway(t, 6.0, .3, 1.8)
    s += (f'<g transform="rotate({a:.2f} 406 490)">'
          '<g stroke="#43703a" stroke-width="7" fill="none" stroke-linecap="round">'
          '<path d="M406 490 L510 466"/><path d="M426 480 L420 460 M452 474 L446 454'
          ' M478 468 L474 448 M434 498 L440 516 M462 492 L468 510"/></g></g>')
    s += A.smoke(430, 262, t, 3, 170, 1.0, .3)
    s += A.smoke(596, 268, t * 1.17 + 1.2, 2, 150, .9, .22)
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


SCENES = {
    "open": open_newyear, "dish": dish, "table_top": table_top, "three": three_animals,
    "yang": yang, "cozy": cozy, "makers": makers, "koza": koza, "koza_fire": koza_fire,
    "koza_turn": koza_turn, "koza_table": koza_table, "koza_eye": koza_eye,
    "koza_shadow": koza_shadow, "koza_far": koza_far,
    "guests": guests, "ded": ded, "horse": horse,
    "retro": retro, "retro_child": retro_child,
    "feast": feast, "heap": heap, "pork": pork, "koza_door": koza_door,
    "greens": greens,
    # часть 5 — семь опор стола
    "cheese": cheese, "pumpkin": pumpkin, "pumpkin_goat": pumpkin_goat, "pate": pate,
    "duck": duck, "fish": fish, "apples": apples, "mors": mors, "lamb_no": lamb_no,
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
