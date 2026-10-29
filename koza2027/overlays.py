# -*- coding: utf-8 -*-
"""Наложения ролика — приёмы исходника. Прозрачный PNG 1920x1080.
Тень рисуется вторым слоем текста, а не SVG-фильтром: cairosvg фильтры не умеет.
ШИРИНА ТЕКСТА МЕРЯЕТСЯ ШРИФТОМ, а не прикидывается: прикидка и была причиной
того, что текст вылезал за плашку."""
from PIL import ImageFont

W, H = 1920, 1080
SER, SAN = "DejaVu Serif", "DejaVu Sans"
GREEN = "#6abf4b"
_TTF = {("DejaVu Sans", 0): "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ("DejaVu Sans", 1): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ("DejaVu Serif", 0): "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ("DejaVu Serif", 1): "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"}
_cache = {}


def wid(text, font=SAN, size=30, bold=False, ls=0):
    """Ширина строки в пикселях. Межбуквенный интервал учитывается."""
    k = (font, 1 if bold else 0, size)
    if k not in _cache:
        try:
            _cache[k] = ImageFont.truetype(_TTF[(font, 1 if bold else 0)], size)
        except Exception:
            _cache[k] = None
    f = _cache[k]
    if f is None:
        return int(len(text) * size * 0.58) + ls * len(text)
    return int(f.getlength(text)) + ls * max(0, len(text) - 1)


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
                    f' xml:space="preserve" fill="#000000" opacity="{o}">{s}</text>')
    out += (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}"{w}{i}{l}'
            f' xml:space="preserve" fill="{fill}" opacity="{op}">{s}</text>')
    return out


def name(pre, big_lines, post, x=110, y=560):
    s = _t(x, y, pre, SAN, 30, "#ffffff", ls=11)
    yy = y + 92
    for ln in big_lines:
        s += _t(x - 4, yy, ln, SER, 104, "#ffffff", bold=True)
        yy += 104
    rw = max(wid(l, SER, 104, True) for l in big_lines)
    s += f'<rect x="{x}" y="{yy-44}" width="{int(rw*0.72)}" height="6" fill="{GREEN}"/>'
    s += f'<rect x="{x+int(rw*0.72)}" y="{yy-44}" width="{int(rw*0.28)}" height="6" fill="{GREEN}" opacity=".35"/>'
    s += _t(x, yy + 20, post, SAN, 30, "#f2ead8", ls=11)
    return _wrap(s)


def plate(head_lines, sub_lines, x=110, y=170, w=None):
    """Плашка: ширина ПОДБИРАЕТСЯ под текст, поля сверху и снизу."""
    PT, HL, RG, SL, PB, PAD = 50, 64, 26, 42, 36, 38
    need = max([wid(l, SER, 58, True) for l in head_lines] +
               [wid(l, SAN, 30, True) for l in sub_lines]) + PAD * 2
    w = max(900, min(1560, need)) if w is None else w
    hh = PT + HL * len(head_lines) + RG + SL * len(sub_lines) + PB
    s = (f'<rect x="{x+5}" y="{y+8}" width="{w}" height="{hh}" rx="14" fill="#000000" opacity=".35"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="14" fill="#0e0e0e" opacity=".88"/>')
    yy = y + PT + 48
    for ln in head_lines:
        s += _t(x + PAD, yy, ln, SER, 58, "#ffffff", bold=True, shadow=False)
        yy += HL
    ry = y + PT + HL * len(head_lines) + 8
    s += f'<rect x="{x+PAD}" y="{ry}" width="96" height="6" fill="{GREEN}"/>'
    s += f'<rect x="{x+PAD}" y="{ry+4}" width="{w-PAD*2}" height="2" fill="#ffffff" opacity=".2"/>'
    yy = ry + RG + 34
    for ln in sub_lines:
        s += _t(x + PAD, yy, ln, SAN, 30, "#efe8dc", bold=True, shadow=False)
        yy += SL
    return _wrap(s)


def myth_fact(myth, fact_lines, x=110, y=150, w=None):
    PAD = 38
    mw = wid(myth, SAN, 33)
    need = max([mw] + [wid(l, SAN, 38, True) for l in fact_lines]) + PAD * 2 + 20
    w = max(900, min(1620, need)) if w is None else w
    hh = 150 + 48 * len(fact_lines)
    s = (f'<rect x="{x+5}" y="{y+8}" width="{w}" height="{hh}" rx="14" fill="#000000" opacity=".35"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="14" fill="#0e0e0e" opacity=".9"/>')
    cx, cy = x + 56, y + 52
    s += f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" stroke="#8b857b" stroke-width="3"/>'
    s += (f'<path d="M{cx-7} {cy-7} L{cx+7} {cy+7} M{cx+7} {cy-7} L{cx-7} {cy+7}"'
          ' stroke="#8b857b" stroke-width="3" stroke-linecap="round"/>')
    s += _t(cx + 32, cy + 9, "МИФ", SAN, 22, "#9a948a", ls=9, shadow=False)
    s += _t(x + PAD, y + 108, myth, SAN, 33, "#9a948a", shadow=False)
    s += f'<rect x="{x+PAD-2}" y="{y+96}" width="{mw+4}" height="3" fill="#9a948a"/>'
    s += f'<rect x="{x+PAD}" y="{y+134}" width="{w-PAD*2}" height="2" fill="#ffffff" opacity=".14"/>'
    cy2 = y + 186
    s += f'<circle cx="{cx}" cy="{cy2}" r="17" fill="#2f9e3f"/>'
    s += (f'<path d="M{cx-8} {cy2} L{cx-2} {cy2+7} L{cx+9} {cy2-7}" stroke="#ffffff" stroke-width="4"'
          ' fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    s += _t(cx + 32, cy2 + 9, "ФАКТ", SAN, 22, "#cfc8bd", ls=9, shadow=False)
    yy = y + 244
    for ln in fact_lines:
        s += _t(x + PAD, yy, ln, SAN, 38, "#ffffff", bold=True, shadow=False)
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
        wpx = wid(txt, SAN, fs, True) + 60
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
