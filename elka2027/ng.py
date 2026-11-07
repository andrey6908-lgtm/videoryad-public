# -*- coding: utf-8 -*-
"""Новогодние кирпичики для роликов про ёлку 2027: комната, ёлка, шары, банты,
гирлянда, подарки, камин, окно, коза-игрушка. Плоский вектор, толстый контур,
палитра «Года козы» — тёплая, а не ночная."""
K = "#17130f"
KRAS, VIN, GRAN = "#d6202f", "#7d1f2e", "#9c2740"
ORA, ZOL, SVET = "#e07f23", "#c9922f", "#ffd36e"
KREM, PERS, TERRA = "#e4d4b6", "#efb07a", "#a8512c"
ZEL, ZEL2, HVOYA = "#3f8a4a", "#2d6236", "#24512e"
STENA, STENA2, POL = "#4a3129", "#5c3d33", "#6b4634"
TEMN = "#2a1a18"


def o(w=7, col=None):
    return f'stroke="{col or K}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def defs():
    """Градиенты и тени: без них картинка плоская (его правка 20 и 22)."""
    g = ('<linearGradient id="plg" x1="0" y1="0" x2="1" y2="0">'
         f'<stop offset="0" stop-color="{ZOL}"/><stop offset="1" stop-color="{ORA}"/></linearGradient>'
         '<linearGradient id="stena" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{STENA2}"/><stop offset="1" stop-color="{STENA}"/></linearGradient>'
         '<radialGradient id="teplo" cx=".5" cy=".5" r=".5">'
         f'<stop offset="0" stop-color="{SVET}" stop-opacity=".55"/>'
         f'<stop offset="1" stop-color="{SVET}" stop-opacity="0"/></radialGradient>'
         # мягкая падающая тень
         '<radialGradient id="ten" cx=".5" cy=".5" r=".5">'
         '<stop offset="0" stop-color="#000000" stop-opacity=".55"/>'
         '<stop offset="1" stop-color="#000000" stop-opacity="0"/></radialGradient>'
         # снег с объёмом
         '<linearGradient id="snegg" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#c3d2e6"/></linearGradient>'
         # стекло бокала
         '<linearGradient id="steklo" x1="0" y1="0" x2="1" y2="0">'
         '<stop offset="0" stop-color="#ffffff" stop-opacity=".55"/>'
         '<stop offset=".35" stop-color="#ffffff" stop-opacity=".12"/>'
         '<stop offset="1" stop-color="#ffffff" stop-opacity=".4"/></linearGradient>'
         # вино
         '<linearGradient id="vino" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#a32a3f"/><stop offset="1" stop-color="#4e0f1c"/></linearGradient>'
         # воск свечи
         '<linearGradient id="vosk" x1="0" y1="0" x2="1" y2="0">'
         '<stop offset="0" stop-color="#fff6e0"/><stop offset=".45" stop-color="#e9dcc0"/>'
         '<stop offset="1" stop-color="#c8b08a"/></linearGradient>'
         # дерево
         '<linearGradient id="derevo" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="#9a6540"/><stop offset="1" stop-color="{TERRA}"/></linearGradient>'
         # хвоя с объёмом
         '<linearGradient id="hvoya" x1="0" y1="0" x2="1" y2="1">'
         f'<stop offset="0" stop-color="#4f9a56"/><stop offset=".5" stop-color="{ZEL2}"/>'
         f'<stop offset="1" stop-color="{HVOYA}"/></linearGradient>')
    # шары: у каждого цвета свой радиальный градиент с бликом
    for i, c in enumerate(SHAR_COLS):
        g += (f'<radialGradient id="sh{i}" cx=".34" cy=".3" r=".78">'
              f'<stop offset="0" stop-color="#ffffff" stop-opacity=".85"/>'
              f'<stop offset=".22" stop-color="{c}" stop-opacity=".95"/>'
              f'<stop offset="1" stop-color="{c}"/></radialGradient>')
    return g


SHAR_COLS = []


def shar_grad(col):
    """Возвращает id градиента для цвета шара, заводя его при первой встрече."""
    if col not in SHAR_COLS:
        SHAR_COLS.append(col)
    return "sh%d" % SHAR_COLS.index(col)


def ten(cx, cy, rx, ry, op=1.0):
    """Мягкая падающая тень под предметом."""
    return (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}"'
            f' fill="url(#ten)" opacity="{op:.2f}"/>')


def room(w, h, pol=.78):
    y = h * pol
    s = f'<rect width="{w}" height="{h}" fill="url(#stena)"/>'
    s += f'<rect y="{y:.0f}" width="{w}" height="{h-y:.0f}" fill="{POL}"/>'
    s += f'<rect y="{y-10:.0f}" width="{w}" height="14" fill="{TERRA}"/>'
    for i in range(0, int(w), 220):          # доски пола
        s += f'<path d="M{i},{y:.0f} L{i-90},{h}" stroke="#5a3a2c" stroke-width="5" opacity=".6"/>'
    return s


def ball(x, y, r, col=KRAS, shine=True):
    """Шар с объёмом: радиальный градиент, блик, отражённый свет снизу."""
    r = max(5.0, float(r))
    gid = shar_grad(col)
    s = (f'<rect x="{x-7:.0f}" y="{y-r-16:.0f}" width="14" height="14" rx="3"'
         f' fill="url(#plg)" {o(3)}/>'
         f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{gid})" {o(max(3, r*.1))}/>')
    if shine:
        s += (f'<ellipse cx="{x-r*.34:.0f}" cy="{y-r*.36:.0f}" rx="{r*.24:.0f}"'
              f' ry="{r*.16:.0f}" fill="#ffffff" opacity=".75"'
              f' transform="rotate(-28 {x-r*.34:.0f} {y-r*.36:.0f})"/>')
        s += (f'<path d="M{x-r*.7:.0f},{y+r*.45:.0f} a{r*.7:.0f},{r*.7:.0f} 0 0 0 {r*1.4:.0f},0"'
              f' fill="none" stroke="#ffffff" stroke-width="{max(1.5, r*.09):.1f}" opacity=".22"/>')
    return s


def bow(x, y, s=1.0, col=VIN):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M0,0 C-46,-34 -72,-6 -52,20 C-34,40 -10,20 0,0 Z" fill="{col}" {o(5)}/>'
            f'<path d="M0,0 C46,-34 72,-6 52,20 C34,40 10,20 0,0 Z" fill="{col}" {o(5)}/>'
            f'<path d="M-6,6 C-26,44 -34,60 -44,72" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M6,6 C26,44 34,60 44,72" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round"/>'
            f'<circle cx="0" cy="2" r="12" fill="{col}" {o(5)}/></g>')


def lights(x, y, w, n=9, r=9):
    s = f'<path d="M{x},{y} q{w*.25:.0f},34 {w*.5:.0f},0 q{w*.25:.0f},-34 {w*.5:.0f},0" fill="none" stroke="{ZOL}" stroke-width="4"/>'
    import math
    for i in range(n):
        t = i / (n - 1)
        px = x + w * t
        py = y + 30 * math.sin(2 * math.pi * t) * (1 if t < .5 else -1) * .7
        col = [SVET, KRAS, "#9ee07f", "#7fd0ff"][i % 4]
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r*2.4:.0f}" fill="{col}" opacity=".18"/>'
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r}" fill="{col}" {o(3)}/>'
    return s


def tree(cx, base, h, palette=None, bows_on=True, star=True, bare=False):
    """Ёлка ярусами. palette — цвета шаров."""
    palette = palette or [KRAS, ZOL, VIN]
    w = h * .80
    s = f'<ellipse cx="{cx}" cy="{base-h*.5:.0f}" rx="{w*.86:.0f}" ry="{h*.62:.0f}" fill="url(#teplo)" opacity=".5"/>'
    s += f'<rect x="{cx-26}" y="{base-40}" width="52" height="60" rx="8" fill="{TERRA}" {o(6)}/>'
    tiers = 5
    for i in range(tiers):
        t = i / tiers
        yy = base - h * t
        ww = w * (1 - t) * .5 + w * .12
        hh = h / tiers * 1.5
        s += (f'<path d="M{cx},{yy-hh:.0f} L{cx-ww:.0f},{yy:.0f} Q{cx},{yy+22:.0f} {cx+ww:.0f},{yy:.0f} Z"'
              f' fill="{HVOYA if i%2 else ZEL2}" {o(6)}/>')
    if not bare:
        import math
        k = 0
        for i in range(tiers):
            t = i / tiers
            yy = base - h * t - h * .06
            ww = w * (1 - t) * .5
            n = max(2, 5 - i)
            for j in range(n):
                px = cx - ww * .8 + (ww * 1.6) * (j / max(1, n - 1))
                s += ball(px, yy - 10, max(7, h * .055 - i * h * .008), palette[k % len(palette)])
                k += 1
        s += lights(cx - w * .46, base - h * .30, w * .92, 7, max(4, h * .016))
        s += lights(cx - w * .30, base - h * .58, w * .60, 5, max(3, h * .014))
        if bows_on:
            s += bow(cx - w * .26, base - h * .42, .55)
            s += bow(cx + w * .22, base - h * .70, .45)
    if star:
        s += zvezda(cx, base - h - 18, 34, SVET)
    return s


def zvezda(x, y, r, col=SVET, k=5):
    import math
    pts = []
    for i in range(k * 2):
        rr = r if i % 2 == 0 else r * .45
        a = -math.pi / 2 + i * math.pi / k
        pts.append(f"{x+rr*math.cos(a):.1f},{y+rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{col}" {o(5)}/>'


def gift(x, y, w, h, col=KRAS, lent=ZOL):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{col}" {o(6)}/>'
            f'<rect x="{x+w*.42:.0f}" y="{y}" width="{w*.16:.0f}" height="{h}" fill="{lent}"/>'
            f'<rect x="{x}" y="{y+h*.4:.0f}" width="{w}" height="{h*.18:.0f}" fill="{lent}"/>'
            + bow(x + w * .5, y + 4, .34, lent))


def kamin(x, y, w=520, h=360):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{STENA2}" {o(7)}/>'
         f'<rect x="{x-26}" y="{y-34}" width="{w+52}" height="36" rx="8" fill="{TERRA}" {o(7)}/>'
         f'<rect x="{x+w*.14:.0f}" y="{y+h*.22:.0f}" width="{w*.72:.0f}" height="{h*.78:.0f}" rx="12" fill="{TEMN}" {o(7)}/>')
    s += f'<ellipse cx="{x+w*.5:.0f}" cy="{y+h*.78:.0f}" rx="{w*.26:.0f}" ry="{h*.2:.0f}" fill="url(#teplo)"/>'
    s += (f'<path d="M{x+w*.5:.0f},{y+h*.52:.0f} c40,36 26,70 -10,96 c-34,-16 -36,-50 -14,-70'
          f' c6,22 20,16 24,-26 Z" fill="{ORA}" {o(5)}/>')
    for i, dx in enumerate((-70, 10, 70)):
        s += (f'<rect x="{x+w*.5+dx:.0f}" y="{y+h*.84:.0f}" width="64" height="18" rx="8"'
              f' fill="{TERRA}" {o(5)}/>')
    return s


def okno(x, y, w, h):
    """Рама окна под живую вставку (само видео кладётся сверху из HTML)."""
    return (f'<rect x="{x-16}" y="{y-16}" width="{w+32}" height="{h+32}" rx="24" fill="#000" opacity=".4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#140d0b"/>'
            f'<rect x="{x-9}" y="{y-9}" width="{w+18}" height="{h+18}" rx="20" fill="none" {o(14)}/>'
            f'<rect x="{x-9}" y="{y-9}" width="{w+18}" height="{h+18}" rx="20" fill="none"'
            f' stroke="{ZOL}" stroke-width="5"/>')


def koza(cx, cy, s=1.0):
    """Коза-игрушка на ёлку: фетровая, в профиль, рога назад, золотой узор."""
    g = f'<g transform="translate({cx},{cy}) scale({s})">'
    # петелька
    g += f'<path d="M-6,-54 q6,-34 2,-56" fill="none" {o(5, ZOL)}/>'
    g += f'<circle cx="-4" cy="-116" r="13" fill="none" {o(5, ZOL)}/>'
    # ноги
    for x0, x1 in ((-44, -50), (-18, -22), (16, 20), (42, 48)):
        g += f'<path d="M{x0},26 L{x1},96" {o(13, TERRA)}/>'
        g += f'<path d="M{x1-7},96 h14" {o(9, K)}/>'
    # хвост
    g += f'<path d="M-66,-16 q-26,-6 -30,-28" fill="none" {o(11, KRAS)}/>'
    # тело
    g += f'<ellipse cx="0" cy="-6" rx="72" ry="46" fill="{KRAS}" {o(6)}/>'
    for dy in (-24, -6, 12):
        g += f'<path d="M-44,{dy} q44,14 88,0" fill="none" stroke="{ZOL}" stroke-width="5" opacity=".85"/>'
    # шея и голова
    g += f'<path d="M52,-28 L82,-56" {o(26, KRAS)}/>'
    g += f'<ellipse cx="92" cy="-64" rx="34" ry="26" fill="{KRAS}" {o(6)}'
    g += f' transform="rotate(-12 92 -64)"/>'
    # морда и бородка
    g += f'<path d="M112,-58 q22,2 24,14 q-16,8 -28,2 Z" fill="{KREM}" {o(5)}/>'
    g += f'<circle cx="131" cy="-48" r="4.5" fill="{K}"/>'
    g += f'<path d="M108,-36 q6,22 -8,30 q-6,-18 -2,-30 Z" fill="{KREM}" {o(5)}/>'
    g += f'<circle cx="100" cy="-72" r="5.5" fill="{K}"/>'
    # ухо и рога назад
    g += f'<ellipse cx="74" cy="-78" rx="16" ry="9" fill="{GRAN}" {o(5)}'
    g += f' transform="rotate(-28 74 -78)"/>'
    g += f'<path d="M86,-86 q-14,-30 -44,-40" fill="none" {o(8, KREM)}/>'
    g += f'<path d="M96,-88 q-6,-34 -32,-50" fill="none" {o(8, KREM)}/>'
    return g + '</g>'
