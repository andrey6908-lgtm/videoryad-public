# -*- coding: utf-8 -*-
"""Рисунки ролика «Год козы 2027». Всё векторное, никаких внешних картинок."""

W, H = 960, 540
SERIF = "DejaVu Serif"
SANS = "DejaVu Sans"

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
</defs>
"""

# ---------- кирпичики ----------

def window(x, y, w, h, frost=True):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="url(#night)" stroke="#120b06" stroke-width="9"/>'
    s += f'<path d="M{x+w/2} {y} L{x+w/2} {y+h} M{x} {y+h/2} L{x+w} {y+h/2}" stroke="#120b06" stroke-width="7"/>'
    s += '<g fill="#e8f2fb" opacity=".8">'
    for dx, dy, r in ((.22, .2, 4), (.74, .28, 3.4), (.3, .82, 3.8), (.82, .86, 3), (.56, .14, 2.6)):
        s += f'<circle cx="{x+w*dx:.0f}" cy="{y+h*dy:.0f}" r="{r}"/>'
    s += '</g>'
    if frost:
        s += (f'<path d="M{x+4} {y+h*0.9} C{x+w*0.2} {y+h*0.82} {x+w*0.36} {y+h*0.88} {x+w*0.56} {y+h*0.8}'
              f' C{x+w*0.74} {y+h*0.72} {x+w*0.9} {y+h*0.8} {x+w-4} {y+h*0.74} L{x+w-4} {y+h} L{x+4} {y+h} Z"'
              ' fill="#eef5fb" opacity=".3"/>')
    return s


def candle(x, y, hgt=78, glow=52):
    return (f'<g><rect x="{x-10}" y="{y}" width="20" height="{hgt}" rx="4" fill="#ecdfc2" stroke="#1b1309" stroke-width="7"/>'
            f'<path d="M{x} {y-40} C{x+16} {y-18} {x+16} {y-4} {x} {y} C{x-16} {y-4} {x-16} {y-18} {x} {y-40} Z" fill="#f9bb3e"/>'
            f'<ellipse cx="{x}" cy="{y-20}" rx="{glow*0.85:.0f}" ry="{glow}" fill="url(#candle)"/></g>')


def garland_bokeh(pts):
    s = '<g opacity=".32">'
    cols = ["#ffd45e", "#ff8c6b", "#9ae06a", "#7fd0ff"]
    for i, (x, y, r) in enumerate(pts):
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cols[i % 4]}"/>'
    return s + '</g>'


def tree(cx, base, scale=1.0, opacity=1.0, toys=True, star=True):
    """Ёлка с игрушками. base — низ кроны."""
    s = f'<g opacity="{opacity}" transform="translate({cx},{base}) scale({scale})">'
    s += '<g stroke="#10180c" stroke-width="7" stroke-linejoin="round">'
    s += '<rect x="-15" y="-6" width="30" height="44" fill="#6b3f1c"/>'
    s += ('<path d="M0 -318 L85 -204 L45 -204 L115 -100 L67 -100 L147 0 L-147 0'
          ' L-67 -100 L-115 -100 L-45 -204 L-85 -204 Z" fill="#2f5c2a"/></g>')
    s += ('<path d="M0 -292 L61 -208 L29 -208 L89 -110 L51 -110 L121 -6 L0 -6 Z"'
          ' fill="#3b7334" opacity=".85"/>')
    if toys:
        s += '<g stroke="#10180c" stroke-width="5">'
        for tx, ty, r, c in ((-29, -188, 15, "#d6202f"), (35, -164, 13, "#c9922f"),
                             (-61, -110, 14, "#e07f23"), (71, -80, 15, "#d6202f"),
                             (-1, -58, 13, "#efb07a"), (-77, -32, 14, "#c9922f"),
                             (93, -24, 13, "#d6202f"), (23, -236, 12, "#c9922f")):
            s += f'<circle cx="{tx}" cy="{ty}" r="{r}" fill="{c}"/>'
        s += '</g>'
        s += '<g><path d="M-77 -210 Q0 -178 79 -204 M-101 -128 Q0 -92 103 -122 M-123 -46 Q0 -10 125 -38" stroke="#8a6a3a" stroke-width="4" fill="none"/>'
        for gx, gy, c in ((-55, -196, "#ffd45e"), (0, -186, "#7fd0ff"), (55, -196, "#ff8c6b"),
                          (-73, -112, "#9ae06a"), (0, -100, "#ffd45e"), (75, -110, "#ff8c6b"),
                          (-91, -30, "#7fd0ff"), (0, -18, "#ffd45e"), (97, -28, "#9ae06a")):
            s += f'<circle cx="{gx}" cy="{gy}" r="7" fill="{c}"/><circle cx="{gx}" cy="{gy}" r="17" fill="{c}" opacity=".3"/>'
        s += '</g>'
    if star:
        s += ('<path d="M0 -356 L14 -320 L53 -318 L23 -293 L33 -255 L0 -277 L-33 -255'
              ' L-23 -293 L-53 -318 L-14 -320 Z" fill="#f6c84e" stroke="#10180c" stroke-width="6" stroke-linejoin="round"/>')
    return s + '</g>'


def tinsel(y=24):
    return (f'<path d="M0 {y-2} Q120 {y+38} 240 {y} Q360 {y-38} 480 {y} Q600 {y+38} 720 {y}'
            f' Q840 {y-38} 960 {y}" stroke="#c9922f" stroke-width="10" fill="none" opacity=".8"/>')


def snow(pts):
    s = '<g fill="#eef6ff" opacity=".45">'
    for x, y, r in pts:
        s += f'<circle cx="{x}" cy="{y}" r="{r}"/>'
    return s + '</g>'


def table(y=452, top="#c6523a"):
    return (f'<path d="M0 {y} L960 {y} L960 540 L0 540 Z" fill="url(#cloth)"/>'
            f'<path d="M0 {y-8} L960 {y-8} L960 {y+12} L0 {y+12} Z" fill="{top}"/>')


def herbs_glass(x, y, w=40, h=56):
    s = f'<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="url(#glass)"/></g>'
    s += '<g stroke="#4e7a35" stroke-width="6" fill="none" stroke-linecap="round">'
    cx = x + w / 2
    s += f'<path d="M{cx} {y} L{cx-4} {y-52}"/><path d="M{cx-4} {y-36} C{cx-22} {y-46} {cx-28} {y-66} {cx-24} {y-82}"/>'
    s += f'<path d="M{cx-4} {y-22} C{cx+18} {y-32} {cx+26} {y-52} {cx+22} {y-68}"/></g>'
    return s


# ---------- ПЕРСОНАЖИ ----------

def _koza_head(fire=True, eye="open", turn=False):
    """Голова козы. turn — отвёрнута (зеркально и глаз прикрыт)."""
    s = ""
    if fire:
        s += '<g stroke="#2a1105" stroke-width="7" stroke-linejoin="round">'
        s += '<path d="M596 236 C640 150 622 88 568 44 C646 68 706 124 710 206 C713 272 678 318 626 332 Z" fill="url(#fl2)"/>'
        s += '<path d="M664 286 C726 228 732 170 708 118 C780 166 806 240 778 306 C760 348 716 368 678 358 Z" fill="url(#fl1)"/>'
        s += '<path d="M548 206 C572 134 556 78 512 42 C578 52 626 110 620 184 C616 230 592 262 562 270 Z" fill="url(#fl1)"/>'
        s += '<path d="M726 356 C772 330 792 290 786 246 C832 288 836 348 800 384 C778 406 748 410 730 398 Z" fill="url(#fl2)"/></g>'
        s += ('<g fill="#ffd36e"><circle cx="820" cy="128" r="6"/><circle cx="866" cy="188" r="4"/>'
              '<circle cx="782" cy="80" r="4.5"/><circle cx="890" cy="300" r="3.6"/><circle cx="748" cy="38" r="3"/></g>')
    s += ('<path d="M498 196 C478 140 500 90 556 62 C588 46 616 56 620 78 C600 66 578 74 560 88'
          ' C518 122 504 158 512 202 Z" fill="#6d4a28" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>')
    s += ('<g stroke="#4a3018" stroke-width="5" fill="none" opacity=".8">'
          '<path d="M516 170 C532 158 548 148 562 142 M524 142 C540 128 556 118 570 112 M536 116 C552 102 570 94 584 90"/></g>')
    s += ('<path d="M556 190 C624 198 654 258 646 318 C638 382 602 434 540 452 C484 468 426 458 390 432'
          ' C354 406 350 362 380 316 C416 262 492 182 556 190 Z" fill="#e9c99c" stroke="#2a1105" stroke-width="9" stroke-linejoin="round"/>')
    s += ('<path d="M596 206 C640 226 658 274 648 322 C638 378 606 426 552 448 C580 408 596 360 596 310'
          ' C596 262 586 228 596 206 Z" fill="#c8a173" opacity=".55"/>')
    s += ('<path d="M372 302 C404 286 446 296 462 332 C478 370 456 406 414 412 C372 418 340 394 338 358'
          ' C336 328 350 312 372 302 Z" fill="#f6e0bc"/>')
    s += ('<g stroke="#c49b6c" stroke-width="5" fill="none" stroke-linecap="round" opacity=".85">'
          '<path d="M470 236 C486 244 492 258 490 272 M504 254 C520 262 526 276 524 290 M536 276 C552 284 558 298 556 312"/></g>')
    s += ('<path d="M554 188 C534 126 558 72 618 44 C652 28 682 40 686 62 C664 50 640 58 620 74'
          ' C576 110 562 150 570 196 Z" fill="#8e6436" stroke="#2a1105" stroke-width="9" stroke-linejoin="round"/>')
    s += ('<g stroke="#5c3d1c" stroke-width="6" fill="none" opacity=".85">'
          '<path d="M572 166 C590 152 608 142 624 134 M580 136 C598 120 616 110 632 104'
          ' M592 108 C610 94 630 84 646 80 M606 82 C622 68 644 58 660 56"/></g>')
    s += ('<path d="M636 254 C680 244 722 258 740 284 C720 304 674 306 636 284 Z" fill="#d8ad7c" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>'
          '<path d="M654 268 C684 262 710 270 722 282 C704 290 676 288 654 276 Z" fill="#b4825a"/>')
    if eye == "closed" or turn:
        s += '<path d="M512 268 C532 252 572 252 588 268" stroke="#2a1105" stroke-width="12" fill="none" stroke-linecap="round"/>'
    else:
        s += '<ellipse cx="548" cy="268" rx="38" ry="25" fill="#f7cb53" stroke="#2a1105" stroke-width="8"/>'
        s += '<rect x="528" y="260" width="42" height="16" rx="8" fill="#2a1105"/>'
        s += '<circle cx="534" cy="256" r="7" fill="#fff" opacity=".9"/>'
        s += '<path d="M512 246 C534 232 570 234 582 248" stroke="#2a1105" stroke-width="7" fill="none" stroke-linecap="round" opacity=".55"/>'
    s += '<path d="M506 230 C534 212 578 214 602 232" stroke="#2a1105" stroke-width="15" fill="none" stroke-linecap="round"/>'
    s += '<path d="M364 324 C372 314 388 314 394 326 C388 338 370 338 364 324 Z" fill="#2a1105"/>'
    s += '<path d="M358 368 C382 384 414 384 436 370" stroke="#2a1105" stroke-width="9" fill="none" stroke-linecap="round"/>'
    s += '<path d="M398 384 L398 398" stroke="#2a1105" stroke-width="7" stroke-linecap="round"/>'
    s += ('<path d="M424 452 C408 498 416 528 440 540 L392 540 C382 506 394 472 414 454 Z" fill="#e9c99c" stroke="#2a1105" stroke-width="8" stroke-linejoin="round"/>'
          '<g stroke="#c49b6c" stroke-width="5" fill="none" stroke-linecap="round"><path d="M414 476 L408 520 M428 474 L426 522"/></g>')
    s += ('<path d="M540 450 C562 498 594 522 648 540 L330 540 C352 506 404 470 540 450 Z" fill="#cfa473" stroke="#2a1105" stroke-width="9" stroke-linejoin="round"/>'
          '<g stroke="#a67c4e" stroke-width="6" fill="none" stroke-linecap="round">'
          '<path d="M470 486 C478 506 476 524 466 540 M520 472 C532 496 532 518 522 540 M572 476 C588 500 594 520 590 540"/></g>')
    return s


def _horse_head():
    s = '<g stroke="#1b0806" stroke-width="8" stroke-linejoin="round">'
    s += '<path d="M616 102 C700 106 772 166 790 254 C808 346 764 428 684 476 C736 394 744 310 704 236 C672 178 644 138 616 102 Z" fill="#9c2a12"/>'
    s += '<path d="M650 140 C726 152 780 212 788 284 C752 232 704 204 658 200 Z" fill="#c43c18"/>'
    s += '<path d="M600 78 C664 68 724 100 752 152 C708 122 660 112 624 124 Z" fill="#d9541f"/></g>'
    s += ('<g stroke="#7a1c0a" stroke-width="6" fill="none" opacity=".75">'
          '<path d="M660 150 C712 182 744 240 744 300 M688 196 C726 232 746 282 744 330 M632 122 C688 140 730 182 748 230"/></g>')
    s += '<path d="M578 96 C582 54 598 28 620 18 C632 48 628 84 612 110 Z" fill="#bc553c" stroke="#1b0806" stroke-width="8" stroke-linejoin="round"/>'
    s += '<path d="M642 108 C658 70 682 46 706 42 C706 78 690 114 666 134 Z" fill="#a0432e" stroke="#1b0806" stroke-width="8" stroke-linejoin="round"/>'
    s += ('<path d="M632 118 C692 146 704 218 680 286 C652 364 584 420 492 444 C420 462 364 440 336 400'
          ' C310 364 324 320 364 280 C432 212 540 96 632 118 Z" fill="#c95c3e" stroke="#1b0806" stroke-width="9" stroke-linejoin="round"/>')
    s += '<path d="M580 166 C608 186 612 234 588 286 C562 342 510 386 446 410 C426 390 430 358 458 322 C498 270 544 198 580 166 Z" fill="#e08157" opacity=".8"/>'
    s += '<path d="M676 240 C668 324 598 400 492 440 C560 396 614 330 640 254 Z" fill="#9c3c24" opacity=".6"/>'
    s += '<ellipse cx="596" cy="220" rx="26" ry="24" fill="#2e0f06" stroke="#1b0806" stroke-width="7"/><circle cx="588" cy="212" r="8" fill="#f6cf84"/>'
    s += '<path d="M560 188 C584 172 616 176 630 194" stroke="#1b0806" stroke-width="14" fill="none" stroke-linecap="round"/>'
    s += '<path d="M386 374 C400 362 424 366 430 384 C422 402 394 402 384 388 Z" fill="#1b0806"/>'
    s += '<path d="M352 404 C382 424 428 424 458 404" stroke="#1b0806" stroke-width="9" fill="none" stroke-linecap="round"/>'
    s += '<g fill="#f3d6b2" opacity=".32"><ellipse cx="330" cy="372" rx="30" ry="16"/><ellipse cx="282" cy="352" rx="22" ry="12"/><ellipse cx="244" cy="338" rx="14" ry="8"/></g>'
    s += ('<path d="M660 290 C692 376 724 436 782 500 L430 500 C488 450 584 362 660 290 Z" fill="#aa4630" stroke="#1b0806" stroke-width="9" stroke-linejoin="round"/>'
          '<g stroke="#7f3020" stroke-width="7" fill="none" stroke-linecap="round"><path d="M560 400 C586 430 604 464 610 500 M640 350 C668 392 688 444 692 500"/></g>')
    return s


def _guest(x, base, body, skin, hair, hw, scale=1.0, hat=False):
    """Один гость: плечи, голова, волосы, глаза, улыбка."""
    r = 50 * scale
    hy = base - 134 * scale
    s = f'<g stroke="#1b1309" stroke-width="{8*scale:.1f}" stroke-linejoin="round">'
    s += (f'<path d="M{x-90*scale} {base} C{x-86*scale} {base-56*scale} {x-46*scale} {base-88*scale} {x} {base-88*scale}'
          f' C{x+46*scale} {base-88*scale} {x+86*scale} {base-56*scale} {x+90*scale} {base} Z" fill="{body}"/>')
    s += f'<circle cx="{x}" cy="{hy}" r="{r}" fill="{skin}"/>'
    s += (f'<path d="M{x-r} {hy-4*scale} C{x-r-4*scale} {hy-50*scale} {x-26*scale} {hy-74*scale} {x} {hy-74*scale}'
          f' C{x+28*scale} {hy-74*scale} {x+r+4*scale} {hy-50*scale} {x+r} {hy-4*scale}'
          f' C{x+34*scale} {hy-30*scale} {x-34*scale} {hy-30*scale} {x-r} {hy-4*scale} Z" fill="{hair}"/></g>'
          if not hw else '</g>')
    if hw:
        s += (f'<path d="M{x-r} {hy-4*scale} C{x-r-4*scale} {hy-50*scale} {x-26*scale} {hy-74*scale} {x} {hy-74*scale}'
              f' C{x+28*scale} {hy-74*scale} {x+r+4*scale} {hy-50*scale} {x+r} {hy-4*scale}'
              f' C{x+34*scale} {hy-30*scale} {x-34*scale} {hy-30*scale} {x-r} {hy-4*scale} Z"'
              f' fill="{hair}" stroke="#1b1309" stroke-width="{8*scale:.1f}" stroke-linejoin="round"/>')
    if hat:
        s += (f'<g stroke="#1b1309" stroke-width="{7*scale:.1f}" stroke-linejoin="round">'
              f'<path d="M{x-36*scale} {hy-12*scale} C{x-32*scale} {hy-62*scale} {x-14*scale} {hy-84*scale} {x+4*scale} {hy-88*scale}'
              f' C{x+38*scale} {hy-96*scale} {x+56*scale} {hy-76*scale} {x+52*scale} {hy-46*scale} L{x+48*scale} {hy-14*scale}'
              f' C{x+30*scale} {hy-32*scale} {x-16*scale} {hy-30*scale} {x-36*scale} {hy-12*scale} Z" fill="#d6202f"/>'
              f'<circle cx="{x+56*scale}" cy="{hy-98*scale}" r="{14*scale:.0f}" fill="#f4efe3"/>'
              f'<path d="M{x-38*scale} {hy-14*scale} C{x-10*scale} {hy-32*scale} {x+30*scale} {hy-32*scale} {x+50*scale} {hy-14*scale}'
              f' C{x+32*scale} {hy-4*scale} {x-20*scale} {hy-4*scale} {x-38*scale} {hy-14*scale} Z" fill="#f4efe3"/></g>')
    e = 6 * scale
    s += (f'<circle cx="{x-16*scale}" cy="{hy+2*scale}" r="{e:.1f}" fill="#241208"/>'
          f'<circle cx="{x+18*scale}" cy="{hy+2*scale}" r="{e:.1f}" fill="#241208"/>'
          f'<path d="M{x-16*scale} {hy+30*scale} C{x-6*scale} {hy+40*scale} {x+10*scale} {hy+40*scale} {x+20*scale} {hy+28*scale}"'
          f' stroke="#1b1309" stroke-width="{7*scale:.1f}" fill="none" stroke-linecap="round"/>')
    return s


# ---------- СЦЕНЫ ----------

def homes():
    """Повтор до горизонта: много окон, в каждом накрытый стол."""
    s = '<rect width="960" height="540" fill="#141d30"/>'
    s += '<path d="M0 0 L960 0 L960 300 L0 300 Z" fill="#101a2c"/>'
    rows = [(0.30, 7, 56, 30), (0.52, 6, 76, 40), (0.80, 4, 112, 60)]
    for ri, (yy, n, ww, hh) in enumerate(rows):
        y = 96 + ri * 112
        op = 0.5 + ri * 0.25
        for i in range(n):
            x = 40 + i * (960 - 110) / (n - 1) if n > 1 else 480
            x += (ri % 2) * 24
            s += f'<g opacity="{op:.2f}" stroke="#0b0f18" stroke-width="7" stroke-linejoin="round">'
            s += f'<rect x="{x:.0f}" y="{y}" width="{ww}" height="{hh}" rx="4" fill="#5e2a18"/>'
            s += f'<rect x="{x+6:.0f}" y="{y+6}" width="{ww-12}" height="{hh-12}" rx="3" fill="#e8a23c"/></g>'
            s += f'<g opacity="{op*0.95:.2f}">'
            s += f'<ellipse cx="{x+ww/2:.0f}" cy="{y+hh*0.72:.0f}" rx="{ww*0.32:.0f}" ry="{hh*0.1:.0f}" fill="#b03c2d"/>'
            s += f'<circle cx="{x+ww*0.3:.0f}" cy="{y+hh*0.45:.0f}" r="{hh*0.12:.0f}" fill="#7a3a1a"/>'
            s += f'<circle cx="{x+ww*0.68:.0f}" cy="{y+hh*0.45:.0f}" r="{hh*0.1:.0f}" fill="#7a3a1a"/></g>'
    s += snow([(120, 60, 5), (300, 120, 4), (520, 46, 5), (700, 150, 4), (860, 80, 5),
               (200, 250, 4), (620, 280, 4), (420, 200, 3.4), (780, 330, 4)])
    s += '<path d="M0 448 L960 448 L960 540 L0 540 Z" fill="#0d1420"/>'
    s += '<g opacity=".5" fill="#2a3850"><path d="M0 448 L120 380 L240 448 Z M300 448 L420 368 L540 448 Z M600 448 L720 384 L840 448 Z"/></g>'
    return s


def dish():
    """Загадочное блюдо под крышкой — какое, не видно."""
    s = f'<rect width="960" height="540" fill="url(#roomc)"/>'
    s += tree(846, 262, 0.52, 0.42)
    s += garland_bokeh([(110, 86, 18), (232, 126, 14), (52, 160, 13), (330, 76, 11)])
    s += table(330)
    s += candle(96, 250, 78, 56)
    s += ('<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
          '<ellipse cx="480" cy="452" rx="300" ry="64" fill="#cbb79a"/>'
          '<ellipse cx="480" cy="438" rx="262" ry="50" fill="#e8dac0"/>'
          '<path d="M238 424 C238 320 346 258 480 258 C614 258 722 320 722 424 Z" fill="#b9bec4"/>'
          '<path d="M276 404 C280 332 368 288 480 288 C592 288 680 332 684 404 Z" fill="#d6dadf"/>'
          '<path d="M452 258 L508 258 L508 240 C508 226 452 226 452 240 Z" fill="#9aa0a6"/>'
          '<ellipse cx="480" cy="226" rx="34" ry="16" fill="#c2c7cc"/></g>')
    s += '<path d="M318 356 C356 318 426 296 480 296" stroke="#f2f5f8" stroke-width="16" fill="none" stroke-linecap="round" opacity=".55"/>'
    s += ('<g stroke="#f3d6b2" stroke-width="8" fill="none" opacity=".3" stroke-linecap="round">'
          '<path d="M700 230 C684 200 716 180 700 148 M760 258 C746 230 776 210 762 182"/></g>')
    s += ('<g stroke="#1b0f07" stroke-width="7" stroke-linejoin="round">'
          '<path d="M60 470 C64 436 96 414 142 414 C172 414 190 430 186 450 C182 470 158 478 134 480 C106 482 80 494 70 510 Z" fill="#eec194"/>'
          '<path d="M900 476 C896 442 866 420 822 420 C794 420 776 436 780 456 C784 476 806 484 830 486 C856 488 880 500 890 516 Z" fill="#eec194"/></g>')
    s += snow([(390, 100, 5), (560, 70, 4), (680, 150, 3.4)])
    return s


def table_top():
    """Стол сверху, разложен по зонам."""
    s = '<rect width="960" height="540" fill="#3a2214"/>'
    s += '<path d="M0 0 L960 0 L960 540 L0 540 Z" fill="url(#cloth)"/>'
    s += '<g opacity=".25" stroke="#f0c98a" stroke-width="4" fill="none">'
    for i in range(6):
        for j in range(4):
            s += f'<path d="M{70+i*170} {60+j*140} q18 24 0 48 q-18 -24 0 -48"/>'
    s += '</g>'
    s += '<g stroke="#1b0f07" stroke-width="9" stroke-linejoin="round">'
    s += '<ellipse cx="480" cy="270" rx="170" ry="92" fill="#e8dac0"/>'
    s += '<path d="M372 252 C370 206 418 178 480 178 C544 178 588 204 588 248 C588 268 552 266 486 266 C416 266 390 262 372 252 Z" fill="#9a4a14"/>'
    s += '<circle cx="382" cy="300" r="16" fill="#f0921f"/><circle cx="578" cy="296" r="16" fill="#f0921f"/>'
    s += '<ellipse cx="170" cy="180" rx="96" ry="52" fill="#dccbab"/><ellipse cx="170" cy="176" rx="70" ry="34" fill="#4e7a35"/>'
    s += '<ellipse cx="790" cy="178" rx="96" ry="52" fill="#dccbab"/>'
    s += '<path d="M734 168 L774 128 L814 168 Z" fill="#f0d98a"/><rect x="782" y="146" width="48" height="30" rx="4" fill="#f6edd2"/>'
    s += '<ellipse cx="180" cy="418" rx="100" ry="50" fill="#e8dac0"/>'
    s += '<path d="M126 404 C122 374 150 354 182 354 C214 354 238 372 236 400 Z" fill="#b8431f"/>'
    s += '<ellipse cx="790" cy="420" rx="100" ry="50" fill="#e8dac0"/>'
    s += '<rect x="742" y="382" width="42" height="34" rx="4" fill="#d8a85c"/><rect x="796" y="386" width="42" height="34" rx="4" fill="#d8a85c"/>'
    s += '<rect x="432" y="430" width="44" height="66" rx="5" fill="url(#glass)"/>'
    s += '<rect x="492" y="432" width="42" height="62" rx="5" fill="url(#glass)"/></g>'
    s += '<g stroke="#4e7a35" stroke-width="7" fill="none" stroke-linecap="round">'
    s += '<path d="M454 430 L450 372"/><path d="M450 388 C428 376 420 354 424 336"/><path d="M450 404 C476 394 488 370 484 350"/>'
    s += '<path d="M513 432 L509 384"/><path d="M509 398 C490 388 484 368 488 352"/></g>'
    s += candle(312, 60, 64, 48) + candle(650, 60, 64, 48)
    s += '<g fill="#c0203a" stroke="#1b0f07" stroke-width="5"><circle cx="300" cy="448" r="20"/><circle cx="662" cy="452" r="18"/></g>'
    return s


def three_animals():
    """Коза, овца, баран рядом — как её называют."""
    s = f'<rect width="960" height="540" fill="url(#roomb)"/>'
    s += garland_bokeh([(90, 70, 16), (430, 54, 12), (880, 76, 15)])
    s += '<path d="M0 452 L960 452 L960 540 L0 540 Z" fill="#4a3620"/>'
    s += '<path d="M0 446 L960 446 L960 460 L0 460 Z" fill="#6b4f2c"/>'
    bodies = [(168, "#e9c99c", "коза"), (480, "#efe6d6", "овца"), (792, "#d9c3a0", "баран")]
    for i, (cx, col, _) in enumerate(bodies):
        s += f'<g stroke="#2a1105" stroke-width="8" stroke-linejoin="round">'
        s += f'<ellipse cx="{cx}" cy="{396}" rx="118" ry="78" fill="{col}"/>'
        if i == 1:
            s += f'<g fill="{col}">'
            for a in range(8):
                s += f'<circle cx="{cx-100+a*28}" cy="{330+ (a%2)*12}" r="26"/>'
            s += '</g>'
        s += f'<path d="M{cx-72} 452 L{cx-72} 510 M{cx-20} 452 L{cx-20} 516 M{cx+30} 452 L{cx+30} 514 M{cx+78} 452 L{cx+78} 506" stroke="#2a1105" stroke-width="16" stroke-linecap="round"/>'
        s += '</g>'
    # головы
    for i, (cx, col, _) in enumerate(bodies):
        hx = cx - 92
        s += '<g stroke="#2a1105" stroke-width="8" stroke-linejoin="round">'
        if i == 0:   # коза — длинные прямые рога назад
            s += f'<path d="M{hx+22} 272 C{hx+10} 226 {hx+30} 196 {hx+70} 180 C{hx+84} 196 {hx+66} 236 {hx+48} 272 Z" fill="#8e6436"/>'
            s += f'<path d="M{hx+48} 268 C{hx+40} 222 {hx+62} 192 {hx+100} 178 C{hx+112} 196 {hx+92} 234 {hx+74} 270 Z" fill="#6d4a28"/>'
            s += f'<ellipse cx="{hx+40}" cy="318" rx="62" ry="48" fill="{col}"/>'
            s += f'<path d="M{hx+6} 352 C{hx-4} 388 {hx+4} 404 {hx+18} 410 C{hx+8} 390 {hx+4} 368 {hx+12} 352 Z" fill="{col}"/>'
        elif i == 1:  # овца — без рогов, шерсть на лбу
            s += f'<ellipse cx="{hx+40}" cy="318" rx="58" ry="50" fill="#f3ead8"/>'
            s += f'<g fill="#efe6d6"><circle cx="{hx+8}" cy="282" r="22"/><circle cx="{hx+40}" cy="272" r="24"/><circle cx="{hx+72}" cy="284" r="21"/></g>'
        else:        # баран — спиральные рога
            s += f'<ellipse cx="{hx+40}" cy="320" rx="60" ry="50" fill="{col}"/>'
            s += f'<path d="M{hx-6} 296 C{hx-52} 286 {hx-74} 248 {hx-60} 216 C{hx-46} 186 {hx-6} 180 {hx+10} 202 C{hx-18} 202 {hx-34} 220 {hx-32} 244 C{hx-30} 272 {hx-16} 288 {hx+6} 294 Z" fill="#9c7a4a"/>'
            s += f'<path d="M{hx+86} 300 C{hx+130} 288 {hx+150} 250 {hx+134} 220 C{hx+118} 192 {hx+82} 188 {hx+68} 208 C{hx+94} 208 {hx+110} 226 {hx+108} 250 C{hx+106} 276 {hx+96} 292 {hx+78} 298 Z" fill="#8a6b3f"/>'
        s += f'<path d="M{hx-14} 330 C{hx-40} 326 {hx-58} 336 {hx-62} 350 C{hx-44} 360 {hx-20} 354 {hx-8} 344 Z" fill="{col}"/>'
        s += '</g>'
        s += f'<circle cx="{hx+22}" cy="306" r="8" fill="#241208"/><circle cx="{hx+22-3}" cy="303" r="3" fill="#fff" opacity=".7"/>'
        s += f'<path d="M{hx-6} 348 C{hx+6} 356 {hx+22} 356 {hx+32} 346" stroke="#2a1105" stroke-width="7" fill="none" stroke-linecap="round"/>'
    s += snow([(260, 110, 5), (600, 86, 4), (760, 170, 3.6)])
    return s


def yang():
    """Иероглиф 羊 — одно слово на всех трёх."""
    s = f'<rect width="960" height="540" fill="url(#roomb)"/>'
    s += garland_bokeh([(110, 80, 18), (850, 96, 15), (240, 440, 13)])
    k = '<g fill="#f2e3c6" stroke="#2a1105" stroke-width="9" stroke-linejoin="round">'
    k += '<path d="M404 148 L368 96 L402 84 L428 142 Z"/>'
    k += '<path d="M556 148 L592 96 L558 84 L532 142 Z"/>'
    k += '<rect x="358" y="186" width="244" height="26" rx="6"/>'
    k += '<rect x="338" y="268" width="284" height="26" rx="6"/>'
    k += '<rect x="318" y="350" width="324" height="26" rx="6"/>'
    k += '<rect x="464" y="150" width="32" height="306" rx="8"/>'
    k += '</g>'
    s += k
    s += '<g fill="#d6202f" opacity=".18"><circle cx="480" cy="290" r="236"/></g>'
    s += snow([(170, 150, 5), (780, 210, 4), (300, 470, 4), (700, 460, 3.4)])
    return s


def cozy():
    """Уютная комната: дом, уют, красота и покой."""
    s = f'<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(44, 54, 196, 198)
    s += tinsel(26)
    s += tree(790, 452, 0.78, 1.0)
    s += '<ellipse cx="330" cy="150" rx="150" ry="118" fill="url(#candle)" opacity=".5"/>'
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
    s += candle(468, 350, 56, 48)
    s += herbs_glass(612, 356)
    s += snow([(300, 90, 5), (530, 58, 4), (620, 140, 3.6), (180, 300, 3.4)])
    return s


def makers():
    """Художник, музыкант, мастер."""
    s = f'<rect width="960" height="540" fill="url(#roomb)"/>'
    s += garland_bokeh([(96, 66, 16), (480, 48, 12), (880, 70, 15)])
    s += '<path d="M0 462 L960 462 L960 540 L0 540 Z" fill="#4a3620"/>'
    s += '<path d="M0 456 L960 456 L960 470 L0 470 Z" fill="#6b4f2c"/>'
    # художник — мольберт
    s += ('<g stroke="#1b1309" stroke-width="9" stroke-linejoin="round">'
          '<path d="M112 462 L168 240 L224 462 M132 380 L204 380" stroke="#8a5c2a" fill="none"/>'
          '<rect x="96" y="196" width="146" height="124" rx="5" fill="#f2ead6"/></g>'
          '<g stroke="#1b1309" stroke-width="5"><circle cx="140" cy="240" r="18" fill="#d6202f"/>'
          '<path d="M108 300 L170 248 L208 300 Z" fill="#4e7a35"/></g>')
    s += _guest(170, 462, "#9c5a3c", "#eec194", "#5e3718", True, 0.72)
    # музыкант — скрипка
    s += _guest(480, 462, "#53647a", "#e5b184", "#3e2a18", True, 0.78)
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round" transform="rotate(-18 480 400)">'
          '<path d="M434 376 C410 376 398 394 400 412 C402 430 418 440 438 438 C440 452 468 452 470 438'
          ' C490 440 506 430 508 412 C510 394 498 376 474 376 C470 362 438 362 434 376 Z" fill="#9c4a1e"/>'
          '<path d="M508 404 L566 384" stroke="#6b3214" stroke-width="12"/></g>')
    # мастер — верстак и дерево
    s += _guest(790, 462, "#7d8f6a", "#f0c79c", "#7a4a24", True, 0.72)
    s += ('<g stroke="#1b1309" stroke-width="8" stroke-linejoin="round">'
          '<rect x="692" y="398" width="196" height="26" rx="5" fill="#a9762f"/>'
          '<path d="M726 398 L726 462 M854 398 L854 462" stroke="#8a5c2a" stroke-width="12"/>'
          '<path d="M744 398 C744 362 772 344 800 344 C828 344 846 362 846 398 Z" fill="#c2914f"/></g>')
    s += snow([(300, 130, 5), (660, 100, 4), (560, 200, 3.4)])
    return s


def koza(fire=True, eye="open"):
    s = f'<rect width="960" height="540" fill="url(#room)"/>'
    s += window(748, 54, 186, 214)
    s += '<g opacity=".16" stroke="#f0c98a" stroke-width="3" fill="none">'
    s += '<path d="M70 70 q16 22 0 44 q-16 -22 0 -44 M70 170 q16 22 0 44 q-16 -22 0 -44 M150 120 q16 22 0 44 q-16 -22 0 -44 M150 220 q16 22 0 44 q-16 -22 0 -44"/></g>'
    s += '<ellipse cx="96" cy="150" rx="150" ry="130" fill="url(#candle)" opacity=".55"/>'
    s += tree(118, 470, 0.46, 0.4)
    s += table(470)
    s += '<g opacity=".45"><ellipse cx="860" cy="505" rx="64" ry="15" fill="#e4d4b6"/></g>'
    s += candle(206, 392, 78, 52)
    s += _koza_head(fire=fire, eye=eye)
    return s


def koza_fire():
    """Вспыхнула: пламя шире, искр больше, свет резче."""
    s = koza(fire=True)
    s = s.replace('<rect width="960" height="540" fill="url(#room)"/>',
                  '<rect width="960" height="540" fill="url(#roomr)"/>')
    extra = '<g opacity=".55">'
    extra += '<ellipse cx="640" cy="240" rx="330" ry="280" fill="#d9601a" opacity=".35"/>'
    extra += '</g><g fill="#ffd36e">'
    for x, y, r in ((96, 60, 5), (210, 120, 4), (330, 44, 5), (900, 60, 4),
                    (870, 420, 5), (150, 300, 4), (280, 220, 3.4), (60, 420, 4)):
        extra += f'<circle cx="{x}" cy="{y}" r="{r}"/>'
    extra += '</g>'
    return s + extra


def koza_turn():
    """Отвернулась: глаз прикрыт, пламя пригасло, свет холоднее."""
    s = f'<rect width="960" height="540" fill="#241a12"/>'
    s += window(748, 54, 186, 214)
    s += tree(118, 470, 0.46, 0.3)
    s += table(470, "#8c3a2a")
    s += candle(206, 392, 78, 34)
    s += '<g transform="translate(960,0) scale(-1,1)">' + _koza_head(fire=False, eye="closed") + '</g>'
    s += '<g fill="#22304a" opacity=".3"><rect width="960" height="540"/></g>'
    s += snow([(320, 90, 5), (520, 150, 4), (660, 70, 4)])
    return s


def koza_table():
    """Коза во главе накрытого стола — смотрит, что ей поставили."""
    s = f'<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(42, 48, 180, 190)
    s += tinsel(24)
    s += tree(820, 404, 0.62, 0.9)
    s += '<path d="M0 330 L960 330 L960 540 L0 540 Z" fill="url(#cloth)"/>'
    s += '<path d="M0 322 L960 322 L960 344 L0 344 Z" fill="#c6523a"/>'
    # коза мельче и по центру стола
    s += '<g transform="translate(222,-74) scale(0.56)">' + _koza_head(fire=True) + '</g>'
    s += ('<g stroke="#1b0f07" stroke-width="8" stroke-linejoin="round">'
          '<ellipse cx="236" cy="452" rx="150" ry="36" fill="#e4d4b6"/>'
          '<path d="M150 440 C148 404 188 382 240 382 C292 382 326 402 326 436 C326 452 294 450 244 450 C196 450 166 452 150 440 Z" fill="#9a4a14"/>'
          '<circle cx="160" cy="452" r="14" fill="#f0921f"/><circle cx="316" cy="450" r="14" fill="#f0921f"/>'
          '<ellipse cx="760" cy="466" rx="120" ry="30" fill="#dccbab"/>'
          '<path d="M706 456 L742 414 L778 456 Z" fill="#f0d98a"/><rect x="782" y="430" width="44" height="26" rx="4" fill="#f6edd2"/></g>')
    s += herbs_glass(452, 400, 44, 60)
    s += herbs_glass(528, 408, 40, 54)
    s += candle(640, 330, 62, 46)
    s += snow([(300, 100, 5), (560, 66, 4), (680, 140, 3.4)])
    return s


def guests():
    s = f'<rect width="960" height="540" fill="url(#roomc)"/>'
    s += window(24, 40, 168, 186)
    s += tree(777, 410, 1.0, 1.0)
    s += tinsel(22)
    s += ('<g stroke="#10180c" stroke-width="6" stroke-linejoin="round">'
          '<rect x="640" y="372" width="62" height="42" rx="4" fill="#a8512c"/><path d="M671 372 L671 414 M640 390 L702 390" stroke="#f6c84e" stroke-width="7"/>'
          '<rect x="866" y="382" width="54" height="34" rx="4" fill="#4e7a35"/><path d="M893 382 L893 416 M866 398 L920 398" stroke="#efb07a" stroke-width="6"/></g>')
    s += ('<g stroke="#120b06" stroke-width="7"><circle cx="330" cy="104" r="48" fill="#e4d4b6"/>'
          '<circle cx="330" cy="104" r="6" fill="#120b06"/>'
          '<path d="M330 104 L330 70 M330 104 L352 118" stroke="#120b06" stroke-width="7" stroke-linecap="round"/></g>')
    s += table(452)
    s += ('<g stroke="#1b1309" stroke-width="6" stroke-linejoin="round">'
          '<ellipse cx="430" cy="492" rx="92" ry="20" fill="#e4d4b6"/>'
          '<path d="M376 486 C374 462 404 448 436 448 C470 448 492 462 492 482 C492 492 468 491 440 491 C408 491 388 492 376 486 Z" fill="#9a4a14"/>'
          '<circle cx="382" cy="494" r="11" fill="#f0921f"/><circle cx="486" cy="492" r="11" fill="#f0921f"/></g>')
    s += herbs_glass(196, 466) + herbs_glass(596, 470, 38, 52)
    s += candle(309, 414, 52, 42)
    s += ('<g><path d="M690 470 L690 430" stroke="#8a8a8a" stroke-width="6" stroke-linecap="round"/>'
          '<g stroke="#ffe08a" stroke-width="4" stroke-linecap="round">'
          '<path d="M690 426 L690 396 M690 426 L668 402 M690 426 L712 402 M690 426 L660 420 M690 426 L720 420 M690 426 L674 448 M690 426 L706 448"/></g>'
          '<circle cx="690" cy="426" r="9" fill="#fff6d0"/></g>')
    s += _guest(148, 452, "#8a6b8e", "#eec194", "#d9d4cb", True, 1.0)
    s += _guest(340, 452, "#53647a", "#e5b184", "#3e2a18", True, 1.04)
    s += _guest(544, 452, "#9c5a3c", "#f0c79c", "#7a4a24", True, 0.92)
    s += _guest(698, 452, "#c9a23f", "#f3cfa6", "#a9712f", True, 0.72, hat=True)
    s += snow([(266, 120, 4), (470, 76, 3.4), (600, 140, 3)])
    return s


def ded():
    s = f'<rect width="960" height="540" fill="url(#roomr)"/>'
    s += window(690, 54, 214, 214)
    s += tinsel(26)
    s += ('<g stroke="#10180c" stroke-width="6" stroke-linejoin="round">'
          '<path d="M0 108 L96 136 L40 152 L140 186 L72 198 L176 236 L0 236 Z" fill="#2f5c2a"/></g>'
          '<g stroke="#10180c" stroke-width="5"><circle cx="64" cy="164" r="13" fill="#d6202f"/><circle cx="118" cy="206" r="12" fill="#c9922f"/></g>')
    s += table(470)
    s += '<g stroke="#1b0806" stroke-width="9" stroke-linejoin="round">'
    s += '<path d="M268 540 C274 440 340 376 450 372 C560 376 626 440 632 540 Z" fill="#c22a24"/>'
    s += '<path d="M268 512 C340 496 560 496 632 512 L632 540 L268 540 Z" fill="#f4efe8"/>'
    s += '<path d="M396 378 C410 452 418 500 414 540 L352 540 C352 466 366 408 396 378 Z" fill="#f4efe8"/>'
    s += '<path d="M504 378 C490 452 482 500 486 540 L548 540 C548 466 534 408 504 378 Z" fill="#f4efe8"/>'
    s += '<path d="M332 486 C390 470 510 470 568 486 L568 516 C510 500 390 500 332 516 Z" fill="#8a6a1e"/>'
    s += '<rect x="424" y="472" width="52" height="46" rx="6" fill="#f6c84e"/>'
    s += '<circle cx="450" cy="262" r="92" fill="#f3c9a0"/>'
    s += '<path d="M364 268 C356 356 394 420 450 436 C506 420 544 356 536 268 C512 318 476 334 450 334 C424 334 388 318 364 268 Z" fill="#f4efe8"/>'
    s += '<path d="M398 324 C410 300 490 300 502 324 C492 346 408 346 398 324 Z" fill="#e8ddd0"/>'
    s += '<path d="M384 290 C408 276 436 282 448 298 C460 282 488 276 512 290 C500 316 468 322 448 312 C428 322 396 316 384 290 Z" fill="#f8f4ee"/>'
    s += '<path d="M352 214 C348 136 392 92 452 92 C512 92 554 136 548 214 C512 182 388 182 352 214 Z" fill="#c22a24"/>'
    s += '<path d="M344 196 C388 170 514 170 558 196 C560 226 548 242 532 244 C492 222 410 222 370 244 C352 242 342 226 344 196 Z" fill="#f4efe8"/>'
    s += '<circle cx="560" cy="110" r="26" fill="#f4efe8"/>'
    s += '<path d="M452 92 C508 88 548 108 560 110 C538 118 504 118 480 112 Z" fill="#a8201c"/>'
    s += '<path d="M632 500 C640 436 616 396 578 388 C552 382 536 398 540 418 C544 440 568 450 586 456 C604 462 622 476 628 500 Z" fill="#c22a24"/>'
    s += '<path d="M600 396 C624 390 646 398 650 414 C642 426 614 428 596 420 Z" fill="#f3c9a0"/></g>'
    s += ('<g stroke="#1b0806" stroke-width="6" stroke-linejoin="round">'
          '<path d="M640 300 L700 300 L690 356 C686 372 654 372 650 356 Z" fill="url(#glass)"/>'
          '<path d="M670 372 L670 412 M646 412 L694 412" stroke="#1b0806" stroke-width="6" stroke-linecap="round"/>'
          '<path d="M646 338 L694 338 L690 356 C686 372 654 372 650 356 Z" fill="#f6c84e" opacity=".85"/></g>'
          '<g fill="#fff6d0" opacity=".8"><circle cx="658" cy="326" r="4"/><circle cx="678" cy="316" r="3"/><circle cx="688" cy="332" r="3.4"/></g>')
    s += ('<g><ellipse cx="416" cy="252" rx="17" ry="19" fill="#fff"/><circle cx="419" cy="254" r="10" fill="#2f4a6b"/><circle cx="415" cy="249" r="4" fill="#fff"/>'
          '<ellipse cx="486" cy="252" rx="17" ry="19" fill="#fff"/><circle cx="489" cy="254" r="10" fill="#2f4a6b"/><circle cx="485" cy="249" r="4" fill="#fff"/></g>')
    s += '<path d="M388 220 C404 206 436 206 448 218" stroke="#f4efe8" stroke-width="13" fill="none" stroke-linecap="round"/>'
    s += '<path d="M454 218 C468 206 498 207 514 221" stroke="#f4efe8" stroke-width="13" fill="none" stroke-linecap="round"/>'
    s += '<ellipse cx="450" cy="282" rx="20" ry="16" fill="#e4906c"/>'
    s += '<ellipse cx="380" cy="284" rx="24" ry="15" fill="#e4906c" opacity=".6"/><ellipse cx="520" cy="284" rx="24" ry="15" fill="#e4906c" opacity=".6"/>'
    s += snow([(212, 96, 5), (300, 166, 4), (162, 286, 4.4), (250, 340, 3.4), (688, 430, 4)])
    return s


def horse():
    s = f'<rect width="960" height="540" fill="url(#roomr)"/>'
    s += '<g opacity=".5"><ellipse cx="760" cy="420" rx="260" ry="150" fill="#d9601a"/><ellipse cx="200" cy="440" rx="200" ry="120" fill="#b8320f"/></g>'
    s += '<path d="M0 452 L960 452 L960 540 L0 540 Z" fill="#6b2318"/>'
    s += '<path d="M0 446 L960 446 L960 462 L0 462 Z" fill="#9a3524"/>'
    s += ('<g stroke="#1b0806" stroke-width="7" stroke-linejoin="round" opacity=".9">'
          '<ellipse cx="120" cy="490" rx="86" ry="20" fill="#d9c7a6"/>'
          '<path d="M62 486 C60 460 92 444 132 444 C172 444 198 458 198 480 C198 492 170 490 136 490 C100 490 76 492 62 486 Z" fill="#7d3a12"/>'
          '<ellipse cx="840" cy="496" rx="78" ry="18" fill="#d9c7a6"/>'
          '<path d="M790 492 C788 470 814 456 846 456 C878 456 898 468 898 486 C898 496 876 494 848 494 C818 494 802 496 790 492 Z" fill="#8a4414"/>'
          '<ellipse cx="470" cy="508" rx="96" ry="20" fill="#cbb79a"/></g>')
    s += _horse_head()
    return s


def retro(child=False):
    """Стол 1967 года — приглушённая гамма, другой свет."""
    s = f'<rect width="960" height="540" fill="url(#sepia)"/>'
    s += '<g opacity=".2" stroke="#d8c28a" stroke-width="3" fill="none">'
    for i in range(7):
        s += f'<path d="M{60+i*140} 60 q16 22 0 44 q-16 -22 0 -44 M{60+i*140} 160 q16 22 0 44 q-16 -22 0 -44"/>'
    s += '</g>'
    s += ('<g stroke="#1a1208" stroke-width="8" stroke-linejoin="round">'
          '<rect x="708" y="96" width="196" height="150" rx="10" fill="#5a3f22"/>'
          '<rect x="730" y="118" width="134" height="106" rx="6" fill="#8ea7b4"/>'
          '<circle cx="884" cy="150" r="10" fill="#c9a86a"/><circle cx="884" cy="186" r="10" fill="#c9a86a"/>'
          '<path d="M806 96 L770 44 M806 96 L848 44" stroke="#8a7446" stroke-width="7"/></g>')
    s += '<g opacity=".35" fill="#cfe0ea"><rect x="736" y="124" width="124" height="18" rx="4"/><rect x="736" y="178" width="124" height="14" rx="4"/></g>'
    s += ('<g stroke="#1a1208" stroke-width="7" stroke-linejoin="round">'
          '<path d="M60 152 L188 152 L176 96 L72 96 Z" fill="#9a8450"/>'
          '<path d="M124 152 L124 206" stroke="#1a1208" stroke-width="7"/></g>')
    s += tree(300, 408, 0.54, 0.75, toys=True, star=True)
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
    s += candle(600, 356, 58, 40)
    if child:
        s += _guest(248, 420, "#7a6a3e", "#e8c79c", "#6b5330", True, 0.62)
        s += _guest(700, 420, "#6b5a3a", "#dcbb8e", "#4a3a22", True, 0.58)
    s += '<g fill="#2a1f10" opacity=".22"><rect width="960" height="540"/></g>'
    return s


SCENES = {
    "homes": homes, "dish": dish, "table_top": table_top, "three": three_animals,
    "yang": yang, "cozy": cozy, "makers": makers, "koza": koza, "koza_fire": koza_fire,
    "koza_turn": koza_turn, "koza_table": koza_table, "guests": guests, "ded": ded,
    "horse": horse, "retro": retro, "retro_child": lambda: retro(child=True),
}


def svg(name):
    body = SCENES[name]()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{DEFS}{body}</svg>')
