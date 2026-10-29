# -*- coding: utf-8 -*-
"""Наложения ролика — приёмы исходника. Прозрачный PNG 1920x1080.
Тень рисуется вторым слоем текста, а не SVG-фильтром: cairosvg фильтры не умеет."""
W, H = 1920, 1080
SER, SAN = "DejaVu Serif", "DejaVu Sans"
GREEN = "#6abf4b"


def _wrap(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{body}</svg>')


def _t(x, y, s, font, size, fill, *, bold=False, ital=False, ls=0, shadow=True, op=1.0):
    w = ' font-weight="bold"' if bold else ''
    i = ' font-style="italic"' if ital else ''
    l = f' letter-spacing="{ls}"' if ls else ''
    out = ""
    if shadow:
        for dx, dy, o in ((0, 5, .5), (3, 4, .35)):
            out += (f'<text x="{x+dx}" y="{y+dy}" font-family="{font}" font-size="{size}"{w}{i}{l}'
                    f' fill="#000000" opacity="{o}">{s}</text>')
    out += (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}"{w}{i}{l}'
            f' fill="{fill}" opacity="{op}">{s}</text>')
    return out


def name(pre, big_lines, post, x=130, y=430):
    s = _t(x, y, pre, SAN, 25, "#ffffff", ls=13)
    yy = y + 92
    for ln in big_lines:
        s += _t(x - 4, yy, ln, SER, 104, "#ffffff", bold=True)
        yy += 104
    s += f'<rect x="{x}" y="{yy-44}" width="430" height="6" fill="{GREEN}"/>'
    s += f'<rect x="{x+430}" y="{yy-44}" width="200" height="6" fill="{GREEN}" opacity=".35"/>'
    s += _t(x, yy + 16, post, SAN, 27, "#e8e0d2", ls=11)
    return _wrap(s)


def plate(head_lines, sub_lines, x=110, y=170, w=940):
    hh = 76 + 66 * len(head_lines) + 44 * len(sub_lines)
    s = (f'<rect x="{x+5}" y="{y+8}" width="{w}" height="{hh}" rx="14" fill="#000000" opacity=".35"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="14" fill="#0e0e0e" opacity=".88"/>')
    yy = y + 76
    for ln in head_lines:
        s += _t(x + 38, yy, ln, SER, 60, "#ffffff", bold=True, shadow=False)
        yy += 66
    s += f'<rect x="{x+38}" y="{yy-20}" width="96" height="6" fill="{GREEN}"/>'
    s += f'<rect x="{x+38}" y="{yy-16}" width="{w-76}" height="2" fill="#ffffff" opacity=".2"/>'
    yy += 42
    for ln in sub_lines:
        s += _t(x + 38, yy, ln, SAN, 31, "#efe8dc", bold=True, shadow=False)
        yy += 44
    return _wrap(s)


def myth_fact(myth, fact_lines, x=110, y=150, w=1210):
    hh = 150 + 48 * len(fact_lines)
    s = (f'<rect x="{x+5}" y="{y+8}" width="{w}" height="{hh}" rx="14" fill="#000000" opacity=".35"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="14" fill="#0e0e0e" opacity=".9"/>')
    cx, cy = x + 56, y + 52
    s += f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" stroke="#8b857b" stroke-width="3"/>'
    s += (f'<path d="M{cx-7} {cy-7} L{cx+7} {cy+7} M{cx+7} {cy-7} L{cx-7} {cy+7}"'
          ' stroke="#8b857b" stroke-width="3" stroke-linecap="round"/>')
    s += _t(cx + 32, cy + 9, "МИФ", SAN, 22, "#9a948a", ls=9, shadow=False)
    s += _t(x + 38, y + 108, myth, SAN, 33, "#9a948a", shadow=False)
    s += f'<rect x="{x+36}" y="{y+96}" width="{int(len(myth)*16.4)}" height="3" fill="#9a948a"/>'
    s += f'<rect x="{x+38}" y="{y+134}" width="{w-76}" height="2" fill="#ffffff" opacity=".14"/>'
    cy2 = y + 186
    s += f'<circle cx="{cx}" cy="{cy2}" r="17" fill="#2f9e3f"/>'
    s += (f'<path d="M{cx-8} {cy2} L{cx-2} {cy2+7} L{cx+9} {cy2-7}" stroke="#ffffff" stroke-width="4"'
          ' fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    s += _t(cx + 32, cy2 + 9, "ФАКТ", SAN, 22, "#cfc8bd", ls=9, shadow=False)
    yy = y + 244
    for ln in fact_lines:
        s += _t(x + 38, yy, ln, SAN, 38, "#ffffff", bold=True, shadow=False)
        yy += 48
    return _wrap(s)


def badge(q_lines, x=140, y=380):
    s = f'<circle cx="{x+20}" cy="{y}" r="20" fill="#2f9e3f"/>'
    s += _t(x + 11, y + 10, "?", SAN, 26, "#ffffff", bold=True, shadow=False)
    s += _t(x + 56, y + 9, "ВОПРОС", SAN, 22, "#ded5c7", ls=10)
    yy = y + 86
    for ln in q_lines:
        s += _t(x, yy, ln, SER, 68, "#ffffff")
        yy += 78
    return _wrap(s)


def slab(a, b, c, x=140, y=300):
    def blk(tx, ty, txt, bg, fg, fs, rot, ital=False):
        wpx = int(len(txt) * fs * 0.64) + 60
        hpx = int(fs * 1.42)
        return (f'<g transform="rotate({rot} {tx} {ty})">'
                f'<rect x="{tx+5}" y="{ty+7}" width="{wpx}" height="{hpx}" fill="#000000" opacity=".4"/>'
                f'<rect x="{tx}" y="{ty}" width="{wpx}" height="{hpx}" fill="{bg}"/>'
                + _t(tx + 30, ty + int(fs * 1.06), txt, SAN, fs, fg, bold=True, ital=ital, shadow=False)
                + '</g>')
    return _wrap(blk(x, y, a, "#79c04b", "#ffffff", 76, -1.6)
                 + blk(x + 96, y + 126, b, "#15120e", "#ffffff", 50, 1.4, True)
                 + blk(x + 36, y + 226, c, "#f4efe3", "#1a140e", 76, -1.0))


def anchor(year, x=1540, y=110):
    s = (f'<rect x="{x+5}" y="{y+7}" width="248" height="104" rx="8" fill="#000000" opacity=".4"/>'
         f'<rect x="{x}" y="{y}" width="248" height="104" rx="8" fill="#0e0e0e" opacity=".84"/>')
    s += _t(x + 30, y + 76, year, SAN, 62, "#ffffff", bold=True, ls=4, shadow=False)
    return _wrap(s)
