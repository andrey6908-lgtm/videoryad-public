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
               [wid(l, SAN, 30, True) for l in sub_lines]) + PAD * 2 + 44
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
    need = max([mw] + [wid(l, SAN, 38, True) for l in fact_lines]) + PAD * 2 + 56
    w = max(900, min(1620, need)) if w is None else w
    # высота считается ОТ ПОСЛЕДНЕЙ БАЗОВОЙ ЛИНИИ, а не на глаз:
    # первая строка факта лежит на y+244, шаг 48, снизу поле 44
    hh = 288 + 48 * (len(fact_lines) - 1)
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
        wpx = wid(txt, SAN, fs, True) + 76
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

def tag(title, sub="", x=110, y=250, idx=0):
    """Ярлычок-подпись: выскакивает в столбик по мере того, как название
    звучит в озвучке. Ширина МЕРЯЕТСЯ ШРИФТОМ, не прикидывается.
    idx — номер в столбике: ярлыки накапливаются, а не сменяют друг друга."""
    TS, SS, PAD = 44, 26, 26
    h = 92 if sub else 64
    yy = y + idx * (h + 12)
    w = max(wid(title, SAN, TS, True), wid(sub, SAN, SS)) + PAD * 2 + 22
    w = max(300, w)
    s = (f'<rect x="{x+5}" y="{yy+7}" width="{w}" height="{h}" rx="9" fill="#000000" opacity=".4"/>'
         f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="9" fill="#0e0e0e" opacity=".9"/>'
         f'<rect x="{x}" y="{yy}" width="8" height="{h}" rx="4" fill="{GREEN}"/>')
    s += _t(x + PAD, yy + (46 if sub else 44), title, SAN, TS, "#ffffff", bold=True, shadow=False)
    if sub:
        s += _t(x + PAD, yy + 78, sub, SAN, SS, "#cfc8bd", shadow=False)
    return _wrap(s)

def recipe(title, steps, active=0, x=None, y=150):
    """Карточка рецепта: шаги списком, активный подсвечен. Висит, пока
    озвучка ведёт по шагам, — голый кадр блюда сам по себе пустоват.
    Ширина и высота МЕРЯЮТСЯ ШРИФТОМ."""
    TS, SS, PAD, LH = 40, 29, 32, 52
    w = max([wid(title, SAN, TS, True)] + [wid(t, SAN, SS, True) for t in steps]) + PAD * 2 + 56
    w = max(520, min(760, w))
    h = PAD + 54 + 22 + LH * len(steps) + PAD - 6
    if x is None:
        x = W - w - 90
    s = (f'<rect x="{x+6}" y="{y+8}" width="{w}" height="{h}" rx="14" fill="#000000" opacity=".4"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#0e0e0e" opacity=".9"/>')
    s += _t(x + PAD, y + PAD + 40, title, SAN, TS, "#ffffff", bold=True, shadow=False)
    ry = y + PAD + 58
    s += f'<rect x="{x+PAD}" y="{ry}" width="86" height="6" fill="{GREEN}"/>'
    s += f'<rect x="{x+PAD}" y="{ry+4}" width="{w-PAD*2}" height="2" fill="#ffffff" opacity=".18"/>'
    yy = ry + 46
    for i, t in enumerate(steps):
        on = (i == active)
        s += (f'<circle cx="{x+PAD+10}" cy="{yy-9}" r="{9 if on else 6}"'
              f' fill="{GREEN if on else "#5a5349"}"/>')
        if i < active:
            s += (f'<path d="M{x+PAD+5} {yy-9} L{x+PAD+9} {yy-5} L{x+PAD+16} {yy-14}"'
                  ' stroke="#0e0e0e" stroke-width="3" fill="none" stroke-linecap="round"/>')
        s += _t(x + PAD + 34, yy, t, SAN, SS, "#ffffff" if on else "#8e877c",
                bold=on, shadow=False)
        yy += LH
    return _wrap(s)

_CHIP_ICONS = {
    "апельсин": ('<circle cx="0" cy="0" r="30" fill="#f0921f" stroke="#1b0f07" stroke-width="7"/>'
                 '<circle cx="0" cy="0" r="20" fill="#ffb455" stroke="#1b0f07" stroke-width="4"/>'
                 '<g stroke="#e07f23" stroke-width="4" stroke-linecap="round">'
                 '<path d="M0 -18 L0 18 M-18 0 L18 0 M-13 -13 L13 13 M13 -13 L-13 13"/></g>'),
    "имбирь":   ('<path d="M-30 6 C-34 -10 -22 -20 -8 -18 C-2 -30 14 -30 18 -18'
                 ' C32 -18 36 -4 28 6 C32 16 22 26 10 22 C2 32 -14 30 -18 18'
                 ' C-30 18 -34 12 -30 6 Z" fill="#e9c98a" stroke="#1b0f07" stroke-width="7"'
                 ' stroke-linejoin="round"/>'
                 '<g stroke="#c49a56" stroke-width="4" fill="none" stroke-linecap="round">'
                 '<path d="M-14 -6 C-4 -2 6 -4 14 -10 M-10 8 C0 12 12 10 20 4"/></g>'),
    "мёд":      ('<path d="M-22 -16 C-22 -26 22 -26 22 -16 L18 16 C16 28 -16 28 -18 16 Z"'
                 ' fill="#d8982a" stroke="#1b0f07" stroke-width="7" stroke-linejoin="round"/>'
                 '<path d="M-16 -8 C-6 -13 8 -13 16 -8" stroke="#f3c75a" stroke-width="5" fill="none"/>'),
    "гранат":   ('<circle cx="0" cy="2" r="28" fill="#a8172c" stroke="#1b0f07" stroke-width="7"/>'
                 '<path d="M0 -26 L-8 -40 L8 -36 Z" fill="#7a0f20" stroke="#1b0f07" stroke-width="5"'
                 ' stroke-linejoin="round"/>'
                 '<g fill="#c0203a"><circle cx="-11" cy="-4" r="7"/><circle cx="10" cy="0" r="6"/>'
                 '<circle cx="-2" cy="13" r="6"/></g>'),
}


def chip(kind, text, x=110, y=760, idx=0):
    """Предмет выскакивает кружком с подписью: «апельсин», «имбирь».
    Рисунок тот же, что в сценах, поэтому вставка читается как часть кадра."""
    h, gap = 96, 14
    yy = y + idx * (h + gap)
    tw = wid(text, SAN, 38, True)
    w = 96 + tw + 44
    s = (f'<rect x="{x+5}" y="{yy+7}" width="{w}" height="{h}" rx="48" fill="#000000" opacity=".4"/>'
         f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="48" fill="#0e0e0e" opacity=".9"/>')
    s += f'<g transform="translate({x+50},{yy+h//2}) scale(1.12)">{_CHIP_ICONS[kind]}</g>'
    s += _t(x + 96, yy + 62, text, SAN, 38, "#ffffff", bold=True, shadow=False)
    return _wrap(s)
