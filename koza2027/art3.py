# -*- coding: utf-8 -*-
"""Предметные кадры ВТОРОГО ролика — нарисованы заново.

Повод (его слово 05.11): «очень много сцен ты притянул с прошлого видео,
я поставлю ссылку с прошлого ролика на это — какую разницу человек увидит?».
Поэтому вся еда и все предметы здесь свои, кадры из первого ролика больше
не используются. Камера, свет и персонажи — из art2.
"""
import anim as A
import art
import art2 as A2
from art2 import (W, H, OUT, RED, ORA, TER, PCH, CRM, GLD, GRN, HRB, NGT, SNOW, WOOL,
                  g, ST, dolly, plane, warm_light, side_dark, air, ground_shadow,
                  candles, no_sign, Z_WALL, Z_TREE, Z_HERO, Z_TABLE, Z_NEAR)

WIN = {"л": (70, 80, 200, 152), "п": (690, 80, 200, 152), "ц": (390, 70, 210, 160)}


def stage(t, dur, hero, *, bg="roomc", wins="п", tins=30, table=452, cloth=None,
          cand=((160, 0, 56, 1.0),), near=None, nearc=((120, 440, 76, 1.05),),
          z1=130, x0=-16, x1=14, light=(300, 360, 300, .32), dark=None, shadow=None,
          sign=None, tree=None, vig=".66"):
    """Один предметный кадр: стена с окном, стол, герой, передний план, свет.
    Камера одна и та же — медленный наезд планами по глубине."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=z1, x0=x0, x1=x1)
    s = f'<rect width="{W}" height="{H}" fill="url(#{bg})"/>'
    wall = "".join(art.window(*WIN[k], t) for k in wins) + art.tinsel(tins)
    s += plane(wall, Z_WALL, cx, cz)
    if tree:
        s += plane(A2.tree_new(t, tree[0], tree[1], tree[2]), Z_TREE, cx, cz)
    body = ""
    if shadow:
        body += ground_shadow(*shadow)
    body += hero
    s += plane(body, Z_HERO, cx, cz)
    if sign:
        s += plane(no_sign(*sign), Z_HERO - 120, cx, cz)
    tb = ""
    if table is not None:
        tb = art.table(table, cloth) if cloth else art.table(table)
        tb += candles([(c[0], table + c[1], c[2], c[3]) for c in cand], t)
    if tb:
        s += plane(tb, Z_TABLE, cx, cz)
    nr = near or ""
    if nearc:
        nr += candles(nearc, t)
    if nr:
        s += plane(nr, Z_NEAR, cx, cz)
    s += warm_light(*light) + air()
    if dark:
        s += side_dark(*dark)
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity="{vig}"/>'
    return s


# ------------------------- слоёные салаты -------------------------
def _layers(lay, w=150, top=SNOW):
    b = f'<path d="M{-w} -22 C{-w} 62 {-w*0.72} 102 0 102 C{w*0.72} 102 {w} 62 {w} -22 Z"' \
        f' fill="#cfe6f2" opacity=".32"{ST(8)}/>'
    for c, yy in lay:
        b += (f'<path d="M{-w+8} {yy} C{-w*0.68} {yy+22} {w*0.68} {yy+22} {w-8} {yy}'
              f' L{w-8} {yy+24} C{w*0.68} {yy+44} {-w*0.68} {yy+44} {-w+8} {yy+24} Z" fill="{c}"{ST(5)}/>')
    b += (f'<path d="M{-w+4} {lay[-1][1]} C{-w*0.8} {lay[-1][1]-44} {w*0.8} {lay[-1][1]-44} {w-4} {lay[-1][1]}'
          f' C{w*0.68} {lay[-1][1]+22} {-w*0.68} {lay[-1][1]+22} {-w+4} {lay[-1][1]} Z" fill="{top}"{ST(8)}/>')
    return b


def tazik_olivye(t, dur=8.0):
    """Таз оливье: горошек, морковь, картошка, майонезная шапка и ложка."""
    b = _layers([("#d9b86a", -14), ("#e8c87a", -36), ("#f2e3b8", -58)], 164)
    b += '<g>' + "".join(
        f'<circle cx="{-110+i*26}" cy="{-66-(i%3)*9}" r="{8-(i%2)}" fill="{["#6abf4b","#e07f23","#efe7d2"][i%3]}"'
        f' stroke="{OUT}" stroke-width="3"/>' for i in range(9)) + '</g>'
    b += (f'<path d="M126 -96 C176 -126 206 -116 214 -96 C206 -76 176 -70 128 -86 Z" fill="#d9d2c2"{ST(7)}/>'
          f'<path d="M212 -96 L268 -140" stroke="#d9d2c2" stroke-width="13" stroke-linecap="round"/>')
    return g(b, 420, 300, 1.0)


def sc_tazik(t, dur=8.0):
    return stage(t, dur, tazik_olivye(t), bg="roomr", cloth="#b8463f", table=396,
                 shadow=(420, 408, 180, 30, .42), light=(760, 360, 260, .3), dark=("left", .22))


def sc_shuba(t, dur=8.0):
    """Селёдка под шубой: свёкла сверху, слои видно сбоку, кусочек рыбы."""
    b = _layers([("#8e2b4a", -16), ("#efe7d2", -38), ("#d98b2a", -58), ("#9fb6c4", -78)], 150,
                top="#a32f58")
    b += (f'<path d="M-40 -108 C-16 -124 20 -124 44 -108 C20 -96 -16 -96 -40 -108 Z" fill="#7f94a4"{ST(6)}/>'
          + "".join(f'<circle cx="{-28+i*20}" cy="-112" r="4" fill="{SNOW}" opacity=".7"/>' for i in range(4)))
    return stage(t, dur, g(b, 470, 304, 1.0), bg="roomb", table=392, cloth="#a8512c",
                 shadow=(470, 404, 168, 28, .4), light=(220, 360, 280, .3), x0=14, x1=-12)


def sc_mimoza(t, dur=8.0):
    """Мимоза: жёлтая яичная крошка сверху, слои под ней."""
    b = _layers([("#efe7d2", -16), ("#f2d85a", -38), ("#e8e2d0", -58)], 142, top="#f4de6a")
    b += "".join(f'<circle cx="{-96+i*17}" cy="{-66-(i%4)*6}" r="4.6" fill="#f7e98a"'
                 f' stroke="#d9bd3c" stroke-width="2"/>' for i in range(12))
    return stage(t, dur, g(b, 450, 306, 1.0), bg="roomc", table=398, cloth="#b8463f",
                 shadow=(450, 406, 158, 26, .4), light=(740, 350, 250, .3))


def sc_tri_tazika(t, dur=8.0):
    """Три таза салатов подряд — «готовят тазиками»."""
    b = g(_layers([("#d9b86a", -10), ("#f2e3b8", -30)], 96), -230, 10, .9)
    b += g(_layers([("#8e2b4a", -10), ("#efe7d2", -30)], 96, top="#a32f58"), 0, 0, .95)
    b += g(_layers([("#f2d85a", -10), ("#e8e2d0", -30)], 96, top="#f4de6a"), 236, 12, .88)
    return stage(t, dur, g(b, 470, 320, 1.0), bg="roomr", table=408, cloth="#b8463f",
                 cand=((110, 0, 50, .9),), shadow=(470, 420, 290, 30, .38),
                 light=(480, 350, 340, .3), z1=110)


# ------------------------- мясо -------------------------
def _meat(w=150, h=74, cut=True):
    """Мясо: неровный верх, косая решётка надрезов, срез с мякотью."""
    b = (f'<path d="M{-w} {h*0.3} C{-w*0.92} {-h*0.5} {-w*0.4} {-h} {0} {-h*0.92}'
         f' C{w*0.46} {-h} {w*0.94} {-h*0.42} {w} {h*0.26}'
         f' C{w*0.6} {h*0.86} {-w*0.6} {h*0.86} {-w} {h*0.3} Z" fill="#8a4a24"{ST(8)}/>')
    b += f'<g stroke="#5d2f10" stroke-width="5" fill="none" opacity=".85">'
    for i in range(6):
        b += f'<path d="M{-w*0.72+i*w*0.26} {-h*0.62} L{-w*0.5+i*w*0.26} {h*0.42}"/>'
    for i in range(3):
        b += f'<path d="M{-w*0.8} {-h*0.2+i*h*0.3} L{w*0.8} {-h*0.34+i*h*0.3}"/>'
    b += '</g>'
    if cut:
        b += (f'<path d="M{w*0.42} {-h*0.5} C{w*0.86} {-h*0.34} {w*0.9} {h*0.2} {w*0.66} {h*0.52}'
              f' C{w*0.5} {h*0.3} {w*0.42} {-h*0.1} {w*0.42} {-h*0.5} Z" fill="{CRM}"{ST(6)}/>'
              f'<path d="M{w*0.48} {-h*0.34} C{w*0.76} {-h*0.2} {w*0.78} {h*0.16} {w*0.62} {h*0.36}'
              f' C{w*0.52} {h*0.2} {w*0.48} {-h*0.06} {w*0.48} {-h*0.34} Z" fill="#c05a4e"/>')
    return b


def sc_svinina(t, dur=8.0):
    """Запечённая буженина крупно, на блюде, с розмарином."""
    b = f'<ellipse cx="0" cy="56" rx="192" ry="48" fill="{CRM}"{ST(8)}/>'
    b += _meat(158, 78)
    b += "".join(f'<path d="M{-120+i*120} 44 q10 -30 26 -44" stroke="{HRB}" stroke-width="7" fill="none"/>'
                 for i in range(3))
    return stage(t, dur, g(b, 460, 296, 1.0), bg="roomr", table=392, cloth="#b8463f",
                 shadow=(460, 364, 196, 30, .42), light=(760, 350, 260, .3), dark=("left", .22))


def sc_rebra(t, dur=8.0):
    """Свиная рулька: круглый кусок на кости, кость торчит — узнаётся сразу."""
    b = f'<ellipse cx="0" cy="66" rx="186" ry="46" fill="{CRM}"{ST(8)}/>'
    b += (f'<path d="M-96 50 C-134 10 -120 -60 -40 -78 C40 -96 112 -52 108 10'
          f' C104 56 56 78 -10 78 C-48 78 -78 68 -96 50 Z" fill="#8a4a24"{ST(9)}/>')
    b += f'<g stroke="#5d2f10" stroke-width="5" fill="none" opacity=".85">'
    for i in range(4):
        b += f'<path d="M{-74+i*46} -62 C{-66+i*46} -16 {-70+i*46} 26 {-78+i*46} 58"/>'
    b += f'<path d="M-96 -16 C-30 -34 52 -36 106 -14"/></g>'
    b += (f'<path d="M96 -36 C132 -56 150 -70 150 -86 C150 -100 132 -106 120 -96'
          f' C108 -86 94 -66 78 -50 Z" fill="{SNOW}"{ST(8)}/>'
          f'<circle cx="140" cy="-96" r="18" fill="{SNOW}"{ST(7)}/>')
    b += (f'<path d="M-40 -78 C0 -92 44 -86 70 -62 C30 -66 -10 -64 -44 -54 Z" fill="{CRM}" opacity=".45"/>')
    b += "".join(f'<path d="M{-110+i*110} 56 q12 -26 28 -36" stroke="{HRB}" stroke-width="7" fill="none"/>'
                 for i in range(3))
    return stage(t, dur, g(b, 460, 300, 1.06), bg="roomb", table=404, cloth="#a8512c",
                 shadow=(460, 372, 196, 28, .4), light=(220, 360, 270, .3), x0=12, x1=-10)


def sc_myasnoy_stol(t, dur=8.0):
    """Стол из одного мяса: холодец, нарезка, жаркое, и так до края."""
    b = g(f'<ellipse cx="0" cy="0" rx="104" ry="30" fill="{CRM}"{ST(7)}/>'
          f'<path d="M-80 -8 C-60 -44 60 -44 80 -8 C56 8 -56 8 -80 -8 Z" fill="#c9a27a" opacity=".85"{ST(6)}/>'
          f'<path d="M-40 -18 q16 -10 34 -2" stroke="#8a4a24" stroke-width="7" fill="none"/>', -250, 18, .84)
    b += g(_meat(96, 48), 0, -6, 1.0)
    b += g(f'<ellipse cx="0" cy="0" rx="100" ry="28" fill="{CRM}"{ST(7)}/>' + A2.sausage_plate(0, -6, .54),
           250, 16, .9)
    b += g(_meat(72, 36), -130, 54, .8) + g(_meat(66, 32), 150, 58, .78)
    return stage(t, dur, g(b, 470, 300, 1.0), bg="roomr", table=392, cloth="#b8463f",
                 cand=((110, 0, 48, .9),), shadow=(470, 392, 320, 30, .4),
                 light=(480, 340, 340, .3), z1=110)


def sc_baranina(t, dur=8.0):
    """Баранья нога на блюде — главный запрет ролика."""
    b = f'<ellipse cx="0" cy="62" rx="196" ry="50" fill="{CRM}"{ST(8)}/>'
    b += (f'<path d="M-140 40 C-150 -30 -70 -86 10 -80 C92 -74 150 -22 140 36'
          f' C100 76 -100 80 -140 40 Z" fill="#8a4a24"{ST(9)}/>')
    b += f'<g stroke="#5d2f10" stroke-width="5" fill="none" opacity=".85">'
    for i in range(5):
        b += f'<path d="M{-96+i*44} -56 L{-74+i*44} 36"/>'
    b += '</g>'
    b += (f'<path d="M136 20 C190 6 214 -10 226 -28 C236 -42 224 -56 208 -48'
          f' C190 -38 162 -18 132 -6 Z" fill="{SNOW}"{ST(8)}/>')
    b += (f'<path d="M-130 -16 C-96 -44 -40 -56 6 -52 C-24 -30 -80 -16 -126 -2 Z" fill="{CRM}" opacity=".5"/>')
    return stage(t, dur, g(b, 460, 288, 1.0), bg="roomr", table=388, cloth="#b8463f",
                 shadow=(460, 358, 200, 32, .45), sign=(460, 276, 186, 30),
                 light=(760, 340, 250, .3), dark=("left", .22))


def sc_shashlyk(t, dur=8.0):
    """Шашлык, плов и рагу — всё из баранины."""
    b = g("".join(f'<g transform="translate({-20+i*46},0)">'
                  f'<path d="M0 -58 L0 48" stroke="#c9c4bb" stroke-width="7"/>'
                  + "".join(f'<rect x="-19" y="{-44+j*30}" width="38" height="26" rx="8" fill="#8a4a24"'
                            f' stroke="{OUT}" stroke-width="5"/>' for j in range(3)) + '</g>'
                  for i in range(3)), -220, -20, .92)
    b += g(f'<ellipse cx="0" cy="0" rx="118" ry="34" fill="{CRM}"{ST(7)}/>'
           f'<path d="M-92 -8 C-70 -48 70 -48 92 -8 C66 12 -66 12 -92 -8 Z" fill="#d9b86a"{ST(7)}/>'
           + "".join(f'<rect x="{-60+i*30}" y="-30" width="24" height="18" rx="6" fill="#8a4a24"'
                     f' stroke="{OUT}" stroke-width="4"/>' for i in range(4)), 200, 20, .95)
    return stage(t, dur, g(b, 470, 306, 1.0), bg="roomb", table=404, cloth="#a8512c",
                 shadow=(470, 400, 300, 28, .38), sign=(470, 294, 190, 30),
                 light=(480, 350, 320, .3), z1=110)


# ------------------------- сладкое -------------------------
def sc_tort(t, dur=8.0):
    """Жирный кремовый торт с розочками."""
    b = f'<ellipse cx="0" cy="64" rx="168" ry="42" fill="{CRM}"{ST(8)}/>'
    b += (f'<path d="M-130 56 L-130 -24 C-130 -46 130 -46 130 -24 L130 56 C96 76 -96 76 -130 56 Z"'
          f' fill="#f2e3c8"{ST(8)}/>')
    b += f'<path d="M-130 10 C-80 26 80 26 130 10 L130 26 C80 42 -80 42 -130 26 Z" fill="#d98b6a" opacity=".9"/>'
    b += f'<ellipse cx="0" cy="-26" rx="130" ry="30" fill="{SNOW}"{ST(7)}/>'
    for i, x in enumerate((-86, -30, 28, 84)):
        b += (f'<circle cx="{x}" cy="{-34-(i%2)*6}" r="19" fill="#e9a7b8"{ST(6)}/>'
              f'<circle cx="{x}" cy="{-34-(i%2)*6}" r="9" fill="#d98b9e"/>')
    b += f'<path d="M-104 -46 q22 -16 44 0 q22 -16 44 0 q22 -16 44 0" stroke="{SNOW}" stroke-width="10" fill="none"/>'
    return stage(t, dur, g(b, 460, 296, 1.0), bg="roomc", table=398, cloth="#b8463f",
                 shadow=(460, 368, 176, 28, .4), sign=(460, 282, 176, 28),
                 light=(760, 350, 250, .3), x0=12, x1=-10)


def sc_yabloki(t, dur=8.0):
    """Печёные яблоки с мёдом, орехами и творожным кремом."""
    b = f'<ellipse cx="0" cy="40" rx="176" ry="46" fill="{CRM}"{ST(8)}/>'
    for i, (x, sc) in enumerate(((-96, 1.0), (0, 1.12), (96, .96))):
        b += (f'<g transform="translate({x},{10-14*sc}) scale({sc})">'
              f'<path d="M0 36 C-42 36 -54 4 -46 -18 C-38 -40 -14 -46 0 -36'
              f' C14 -46 38 -40 46 -18 C54 4 42 36 0 36 Z" fill="#b8463f"{ST(7)}/>'
              f'<path d="M0 -36 L0 -50 M0 -50 q14 -8 20 2" stroke="#6b4a2c" stroke-width="5" fill="none"/>'
              f'<ellipse cx="0" cy="-22" rx="16" ry="8" fill="{SNOW}"{ST(5)}/>'
              f'<circle cx="-8" cy="-26" r="5" fill="#a8703a"{ST(3)}/>'
              f'<circle cx="7" cy="-24" r="4.4" fill="#8a5a2c"{ST(3)}/>'
              + A.smoke(0, -46, t, 2, 60, .5, .22) + '</g>')
    return stage(t, dur, g(b, 470, 318, 1.0), bg="roomc", table=412, cloth="#b8463f",
                 shadow=(470, 388, 186, 26, .38), light=(220, 360, 280, .32))


def sc_korzina(t, dur=8.0):
    """Корзина с мандаринами, яблоками и гранатами."""
    b = f'<path d="M-140 -14 C-140 54 -92 92 0 92 C92 92 140 54 140 -14 Z" fill="#9a6a34"{ST(9)}/>'
    for i in range(7):
        b += f'<path d="M{-128+i*42} -6 C{-120+i*42} 46 {-112+i*42} 70 {-104+i*42} 84" stroke="#7a5228" stroke-width="5" fill="none"/>'
    b += f'<path d="M-146 -14 L146 -14 L140 6 L-140 6 Z" fill="#a8703a"{ST(7)}/>'
    for x, y, r, c in ((-82, -44, 32, "#d8622a"), (-16, -60, 34, "#e2b23c"), (56, -46, 31, "#d8622a"),
                       (96, -16, 28, "#b8463f"), (-116, -12, 27, "#e2b23c"), (22, -16, 29, "#b8463f")):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"{ST(6)}/>'
        b += f'<circle cx="{x-r*.3:.0f}" cy="{y-r*.34:.0f}" r="{r*.22:.1f}" fill="#fff" opacity=".45"/>'
    b += f'<path d="M-16 -94 L-16 -108 M-10 -104 q10 -8 16 2" stroke="{HRB}" stroke-width="5" fill="none"/>'
    return stage(t, dur, g(b, 460, 300, 1.0), bg="roomc", table=404, cloth="#b8463f",
                 shadow=(460, 396, 170, 26, .4), light=(760, 350, 270, .3), x0=10, x1=-12)


# ------------------------- сыр, мёд, орехи -------------------------
def sc_doska(t, dur=8.0):
    """Сырная доска: три сыра, мёд в пиале, орехи, инжир."""
    b = f'<path d="M-200 -8 L200 -8 L184 34 L-184 34 Z" fill="#8a5a2c"{ST(8)}/>'
    b += f'<path d="M200 -8 C228 -8 236 6 224 14 L196 14 Z" fill="#8a5a2c"{ST(7)}/>'
    b += (f'<path d="M-170 -10 L-96 -10 L-108 -62 L-158 -62 Z" fill="#f2d85a"{ST(6)}/>'
          f'<circle cx="-146" cy="-36" r="8" fill="#d9bd3c"/><circle cx="-122" cy="-24" r="6" fill="#d9bd3c"/>')
    b += f'<path d="M-80 -10 L-4 -10 L-12 -56 L-72 -56 Z" fill="{SNOW}"{ST(6)}/>'
    b += f'<path d="M12 -10 L78 -10 L72 -46 L18 -46 Z" fill="{PCH}"{ST(6)}/>'
    b += (f'<path d="M100 -10 C100 -34 122 -44 140 -44 C158 -44 180 -34 180 -10 Z" fill="{CRM}"{ST(6)}/>'
          f'<path d="M108 -16 C120 -28 160 -28 172 -16 Z" fill="{GLD}"/>')
    for i, (x, y, r) in enumerate(((-30, -70, 11), (6, -66, 9), (40, -72, 10))):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#a8703a"{ST(4)}/>'
    for x in (-58, 86):
        b += (f'<path d="M{x} -58 C{x-16} -58 {x-22} -72 {x-16} -82 C{x-10} -92 {x+10} -92 {x+16} -82'
              f' C{x+22} -72 {x+16} -58 {x} -58 Z" fill="#7a3b63"{ST(5)}/>'
              f'<path d="M{x} -92 L{x} -100 M{x-7} -98 L{x+7} -98" stroke="{HRB}" stroke-width="4"/>')
    return stage(t, dur, g(b, 470, 312, 1.18), bg="roomb", table=424, cloth="#a8512c",
                 shadow=(470, 372, 236, 26, .36), light=(230, 360, 280, .32), x0=14, x1=-12)


def sc_med_orehi(t, dur=8.0):
    """Мёд течёт с ложки, рядом орехи и инжир — крупно."""
    b = (f'<path d="M-40 -10 C-40 -58 -16 -78 0 -78 C16 -78 40 -58 40 -10 Z" fill="{CRM}"{ST(8)}/>'
         f'<path d="M-34 -22 C-18 -46 18 -46 34 -22 Z" fill="{GLD}"/>')
    b += (f'<path d="M-96 -92 C-52 -116 -16 -112 4 -96" stroke="#d9d2c2" stroke-width="13" stroke-linecap="round"/>'
          f'<path d="M4 -96 C8 -70 6 -44 2 -24" stroke="{GLD}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    for x, y, r, c in ((96, -24, 25, "#a8703a"), (142, -6, 21, "#8a5a2c"), (72, 10, 19, "#a8703a")):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"{ST(6)}/>'
    b += (f'<path d="M-128 6 C-160 6 -172 -18 -160 -36 C-148 -54 -108 -54 -96 -36'
          f' C-84 -18 -96 6 -128 6 Z" fill="#7a3b63"{ST(7)}/>'
          f'<path d="M-128 -54 L-128 -70 M-142 -64 L-114 -64" stroke="{HRB}" stroke-width="6"/>')
    return stage(t, dur, g(b, 450, 318, 1.3), bg="roomc", table=420, cloth="#b8463f",
                 shadow=(450, 378, 200, 24, .34), light=(740, 350, 250, .3))


def sc_kozy_syr(t, dur=8.0):
    """Козий сыр поленом, кружки среза, рядом кубики феты и брынза."""
    b = f'<ellipse cx="0" cy="48" rx="186" ry="46" fill="{CRM}"{ST(8)}/>'
    b += (f'<path d="M-150 30 L-30 30 L-30 -34 L-150 -34 Z" fill="{SNOW}"{ST(8)}/>'
          f'<ellipse cx="-30" cy="-2" rx="16" ry="32" fill="#f6f2e8"{ST(7)}/>'
          f'<path d="M-150 -34 C-150 -16 -150 12 -150 30" stroke="#ddd2b8" stroke-width="5"/>')
    for i, (x, y) in enumerate(((10, 18), (56, 26), (34, -4))):
        b += (f'<ellipse cx="{x}" cy="{y}" rx="30" ry="12" fill="#f6f2e8"{ST(6)}/>'
              f'<ellipse cx="{x}" cy="{y-4}" rx="30" ry="12" fill="{SNOW}"{ST(6)}/>')
    for i, (x, y, sc) in enumerate(((112, 18, 1.0), (150, 4, .9), (132, 34, .86))):
        b += (f'<g transform="translate({x},{y}) scale({sc})">'
              f'<path d="M-22 18 L22 18 L22 -16 L-22 -16 Z" fill="#fbf7ee"{ST(6)}/>'
              f'<path d="M-22 -16 L-10 -26 L34 -26 L22 -16 Z" fill="#f2ead6"{ST(5)}/>'
              f'<path d="M22 -16 L34 -26 L34 8 L22 18 Z" fill="#e8e0cc"{ST(5)}/></g>')
    b += "".join(f'<path d="M{-120+i*80} 26 q10 -24 24 -32" stroke="{GRN}" stroke-width="6" fill="none"/>'
                 for i in range(4))
    return stage(t, dur, g(b, 460, 312, 1.12), bg="roomc", table=412, cloth="#b8463f",
                 shadow=(460, 374, 196, 24, .36), light=(240, 350, 270, .32))


# ------------------------- птица и горячее -------------------------
def sc_utka(t, dur=8.0):
    """Утка с апельсинами — чем заменить свинину."""
    b = f'<ellipse cx="0" cy="56" rx="198" ry="50" fill="{CRM}"{ST(8)}/>'
    b += (f'<path d="M-146 36 C-152 -30 -74 -84 6 -80 C86 -76 148 -26 142 34'
          f' C100 72 -104 76 -146 36 Z" fill="url(#duck)"{ST(9)}/>')
    b += (f'<path d="M-96 -22 C-50 -52 40 -56 96 -26" stroke="#5d2f0d" stroke-width="6" fill="none" opacity=".75"/>'
          f'<path d="M-70 10 C-20 -14 36 -16 84 6" stroke="#5d2f0d" stroke-width="5" fill="none" opacity=".6"/>')
    for i, x in enumerate((-116, -46, 36, 112)):
        b += (f'<circle cx="{x}" cy="{44-(i%2)*16}" r="26" fill="{ORA}"{ST(6)}/>'
              f'<path d="M{x-14} {36-(i%2)*16} q14 -10 28 0" stroke="#c0661a" stroke-width="4" fill="none"/>')
    b += "".join(f'<path d="M{-130+i*130} 40 q12 -28 28 -40" stroke="{HRB}" stroke-width="7" fill="none"/>'
                 for i in range(3))
    b += A.smoke(0, -74, t, 3, 90, .8, .22)
    return stage(t, dur, g(b, 460, 292, 1.0), bg="roomc", table=398, cloth="#b8463f",
                 shadow=(460, 360, 202, 30, .4), light=(760, 350, 260, .3), x0=12, x1=-10)


def sc_indeyka(t, dur=8.0):
    """Индейка с яблоками: чем заменить колбасу и свинину."""
    b = f'<ellipse cx="0" cy="54" rx="190" ry="48" fill="{CRM}"{ST(8)}/>'
    b += (f'<path d="M-134 34 C-140 -36 -60 -88 14 -82 C88 -76 142 -24 134 32'
          f' C94 70 -96 74 -134 34 Z" fill="#b07234"{ST(9)}/>')
    b += f'<path d="M-84 -34 C-30 -60 44 -58 92 -30" stroke="#75441a" stroke-width="6" fill="none" opacity=".7"/>'
    b += (f'<path d="M126 26 C170 14 190 0 200 -14 C208 -26 198 -38 184 -32'
          f' C168 -24 144 -8 120 2 Z" fill="{SNOW}"{ST(7)}/>')
    for x in (-120, 110):
        b += f'<circle cx="{x}" cy="42" r="24" fill="#b8463f"{ST(6)}/>'
    b += A.smoke(10, -76, t, 3, 86, .8, .22)
    return stage(t, dur, g(b, 470, 296, 1.0), bg="roomb", table=402, cloth="#a8512c",
                 shadow=(470, 362, 196, 28, .4), light=(230, 350, 270, .3))


def sc_protiven(t, dur=8.0):
    """Горячее несут прямо в противне — некрасивая подача."""
    b = (f'<path d="M-200 -16 L200 -16 L182 56 L-182 56 Z" fill="#5a544c"{ST(9)}/>'
         f'<path d="M-212 -24 L212 -24 L212 -6 L-212 -6 Z" fill="#6f6a60"{ST(7)}/>')
    b += g(_meat(120, 50), 0, 18, 1.0)
    b += (f'<path d="M-212 -16 C-240 -16 -248 2 -232 10 M212 -16 C240 -16 248 2 232 10"'
          f' stroke="{OUT}" stroke-width="9" fill="none"/>')
    b += A.smoke(0, -24, t, 3, 110, .9, .26)
    return stage(t, dur, g(b, 470, 306, 1.0), bg="roomb", table=416, cloth="#a8512c",
                 shadow=(470, 378, 210, 26, .4), light=(240, 350, 270, .3), x0=14, x1=-12)


def sc_podacha(t, dur=8.0):
    """То же блюдо, но подано красиво: порция, зелень, гранат."""
    b = f'<ellipse cx="0" cy="40" rx="176" ry="46" fill="{SNOW}"{ST(8)}/>'
    b += f'<ellipse cx="0" cy="30" rx="138" ry="34" fill="#efe7d2"/>'
    b += g(_meat(72, 34), -26, 2, 1.0)
    b += "".join(f'<path d="M{40+i*34} 16 q10 -28 24 -38" stroke="{GRN}" stroke-width="6" fill="none"/>'
                 for i in range(3))
    b += "".join(f'<circle cx="{-96+i*22}" cy="{30-(i%2)*8}" r="5.4" fill="#b8463f"{ST(3)}/>' for i in range(5))
    return stage(t, dur, g(b, 470, 320, 1.0), bg="roomc", table=412, cloth="#b8463f",
                 shadow=(470, 374, 182, 24, .34), light=(740, 350, 260, .3))


def sc_zelen(t, dur=8.0):
    """Пучки петрушки, базилика и розмарина в низких стаканах."""
    b = ""
    for i, (x, col, kind) in enumerate(((-150, GRN, "петрушка"), (0, "#5aa83c", "базилик"),
                                        (150, "#7fae58", "розмарин"))):
        sw = A.sway(t, 5.6, i * .3, 2.2)
        b += (f'<g transform="translate({x},0)">'
              f'<path d="M-44 10 L44 10 L38 74 L-38 74 Z" fill="#cfe6f2" opacity=".5"{ST(7)}/>'
              f'<g transform="rotate({sw:.2f} 0 10)">')
        if kind == "петрушка":
            for j in range(5):
                b += (f'<path d="M{-28+j*14} 8 C{-30+j*14} -22 {-22+j*14} -44 {-14+j*14} -58"'
                      f' stroke="{col}" stroke-width="5" fill="none"/>'
                      f'<circle cx="{-14+j*14}" cy="-62" r="10" fill="{col}"{ST(4)}/>')
        elif kind == "базилик":
            for j in range(4):
                b += (f'<path d="M{-22+j*15} 8 L{-18+j*15} -46" stroke="{col}" stroke-width="5"/>'
                      f'<ellipse cx="{-18+j*15}" cy="-54" rx="15" ry="11" fill="{col}"{ST(4)}/>')
        else:
            for j in range(4):
                b += (f'<path d="M{-20+j*14} 8 L{-16+j*14} -62" stroke="{col}" stroke-width="5"/>'
                      + "".join(f'<path d="M{-16+j*14} {-18-k*12} l-10 -6 M{-16+j*14} {-18-k*12} l10 -6"'
                                f' stroke="{col}" stroke-width="3.4"/>' for k in range(4)))
        b += '</g></g>'
    return stage(t, dur, g(b, 470, 300, 1.0), bg="roomc", table=382, cloth="#b8463f",
                 shadow=(470, 378, 230, 22, .3), light=(480, 340, 330, .32), z1=110)


def sc_tykva(t, dur=8.0):
    """Запечённая тыква дольками: оранжевая мякоть, тёмная корка по дуге."""
    b = f'<ellipse cx="0" cy="58" rx="196" ry="48" fill="{CRM}"{ST(8)}/>'
    for x, y, rot, sc in ((-120, 18, -12, 1.0), (-36, 6, -4, 1.12), (48, 12, 6, 1.06), (128, 26, 14, .94)):
        b += (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
              f'<path d="M-62 26 C-48 -30 48 -30 62 26 C30 42 -30 42 -62 26 Z" fill="{ORA}"{ST(7)}/>'
              f'<path d="M-62 26 C-30 42 30 42 62 26 C52 44 -52 44 -62 26 Z" fill="#4e6b2a"{ST(6)}/>'
              f'<path d="M-40 16 C-28 -12 28 -12 40 16" stroke="#c0661a" stroke-width="5" fill="none"/>'
              f'<path d="M-20 6 C-12 -10 12 -10 20 6" stroke="#d98b2a" stroke-width="4" fill="none"/></g>')
    for i in range(8):
        b += f'<circle cx="{-130+i*38}" cy="{-26-(i%3)*10}" r="6" fill="#b8463f"{ST(4)}/>'
    b += f'<path d="M-60 -44 q14 -26 32 -34 M40 -40 q12 -24 30 -32" stroke="{HRB}" stroke-width="7" fill="none"/>'
    b += A.smoke(0, -40, t, 2, 70, .7, .2)
    return stage(t, dur, g(b, 470, 306, 1.1), bg="roomc", table=412, cloth="#b8463f",
                 shadow=(470, 392, 220, 26, .36), light=(740, 350, 260, .3))


def sc_salat_tykva(t, dur=8.0):
    """Салат с тыквой, нутом и гранатом — вместо оливье."""
    b = f'<path d="M-140 -16 C-140 44 -96 78 0 78 C96 78 140 44 140 -16 Z" fill="{SNOW}"{ST(8)}/>'
    b += f'<path d="M-128 -14 C-108 18 108 18 128 -14 C100 -34 -100 -34 -128 -14 Z" fill="{HRB}"{ST(6)}/>'
    for i in range(7):
        b += (f'<path d="M{-96+i*32} -22 C{-92+i*32} -42 {-78+i*32} -52 {-66+i*32} -56"'
              f' stroke="{GRN}" stroke-width="5" fill="none"/>')
    for x, y in ((-72, -20), (-18, -28), (40, -22), (92, -14), (-44, -6), (20, -6)):
        b += f'<path d="M{x-16} {y} C{x-16} {y-14} {x} {y-22} {x+16} {y} Z" fill="{ORA}"{ST(5)}/>'
    for i in range(9):
        b += f'<circle cx="{-104+i*26}" cy="{-4-(i%3)*8}" r="5" fill="#d9b86a"{ST(3)}/>'
    for i in range(7):
        b += f'<circle cx="{-88+i*30}" cy="{10-(i%2)*8}" r="5.4" fill="#b8463f"{ST(3)}/>'
    return stage(t, dur, g(b, 460, 316, 1.0), bg="roomr", table=406, cloth="#b8463f",
                 shadow=(460, 396, 170, 24, .36), light=(760, 350, 250, .3), x0=12, x1=-12)


def sc_mors(t, dur=8.0):
    """Кувшин тёплого гранатового морса с корицей и бадьяном."""
    b = A2.jug_mors(-70, 10, 1.25)
    for x, y, sc in ((86, 26, 1.0), (148, 34, .9)):
        b += (f'<g transform="translate({x},{y}) scale({sc})">'
              f'<path d="M-30 -46 L30 -46 L24 42 C24 54 -24 54 -24 42 Z" fill="#cfe6f2" opacity=".55"{ST(7)}/>'
              f'<path d="M-27 -16 L27 -16 L22 42 C22 52 -22 52 -22 42 Z" fill="#a8302f" opacity=".9"/>'
              f'<path d="M-6 -58 L10 -22" stroke="#8a5a2c" stroke-width="7" stroke-linecap="round"/>'
              f'<path d="M22 -34 l12 -8 l-2 14 l12 2 l-10 10 l4 13 l-13 -6 l-10 8 l1 -14 Z"'
              f' fill="#8a5a2c"{ST(4)}/></g>')
    b += A.smoke(-70, -70, t, 2, 80, .7, .22)
    return stage(t, dur, g(b, 450, 300, 1.0), bg="roomb", table=404, cloth="#a8512c",
                 shadow=(450, 384, 190, 24, .34), light=(240, 350, 270, .32))


def sc_shampanskoe(t, dur=8.0):
    """Шампанское под куранты: бутылка и поднятые бокалы."""
    b = (f'<path d="M-24 -120 L24 -120 L24 -80 C44 -60 50 -30 50 20 C50 46 -50 46 -50 20'
         f' C-50 -30 -44 -60 -24 -80 Z" fill="#2f5c2a"{ST(8)}/>'
         f'<path d="M-24 -132 L24 -132 L24 -114 L-24 -114 Z" fill="{GLD}"{ST(6)}/>'
         f'<path d="M-40 -12 L40 -12 L40 18 L-40 18 Z" fill="{CRM}" opacity=".9"{ST(5)}/>')
    for x, y, sc in ((-150, 20, 1.0), (150, 12, 1.06)):
        b += (f'<g transform="translate({x},{y}) scale({sc})">'
              f'<path d="M-26 -58 L26 -58 L18 -2 L-18 -2 Z" fill="#cfe6f2" opacity=".7"{ST(6)}/>'
              f'<path d="M-24 -46 L24 -46 L17 -6 L-17 -6 Z" fill="{GLD}" opacity=".85"/>'
              f'<path d="M0 -2 L0 34 M-18 36 L18 36" stroke="{OUT}" stroke-width="7" fill="none"/>'
              + "".join(f'<circle cx="{-12+j*9}" cy="{-20-((t*32+j*17)%34):.0f}" r="2.6" fill="#fff" opacity=".7"/>'
                        for j in range(4)) + '</g>')
    return stage(t, dur, g(b, 470, 306, 1.0), bg="roomc", table=416, cloth="#b8463f",
                 shadow=(470, 388, 200, 24, .34), light=(480, 340, 330, .32), z1=110)


# ------------------------- китайский блок -------------------------
def sc_ryba(t, dur=8.0):
    """Рыба целиком — с головой и хвостом, как ставят на Востоке."""
    b = f'<ellipse cx="0" cy="40" rx="210" ry="48" fill="{SNOW}"{ST(8)}/>'
    b += f'<path d="M-150 12 C-110 -42 90 -46 140 6 C92 56 -108 58 -150 12 Z" fill="#9fb6c4"{ST(9)}/>'
    b += f'<path d="M140 6 L206 -30 L198 44 Z" fill="#9fb6c4"{ST(8)}/>'
    b += (f'<path d="M-150 12 C-170 2 -176 -8 -170 -18" stroke="{OUT}" stroke-width="7" fill="none"/>'
          f'<circle cx="-118" cy="2" r="11" fill="{SNOW}"{ST(5)}/><circle cx="-118" cy="2" r="5" fill="{OUT}"/>')
    b += f'<g stroke="#6f8696" stroke-width="4" fill="none" opacity=".8">'
    for i in range(5):
        b += f'<path d="M{-80+i*44} -22 C{-70+i*44} 2 {-74+i*44} 24 {-84+i*44} 40"/>'
    b += '</g>'
    b += f'<path d="M-24 -34 C14 -52 60 -48 86 -30" stroke="{HRB}" stroke-width="7" fill="none"/>'
    for i in range(4):
        b += f'<path d="M{-96+i*58} 46 q12 -22 28 -30" stroke="{GRN}" stroke-width="6" fill="none"/>'
    b += "".join(f'<circle cx="{-140+i*40}" cy="58" r="5" fill="#b8463f"{ST(3)}/>' for i in range(3))
    b += A.smoke(0, -40, t, 2, 70, .7, .2)
    return stage(t, dur, g(b, 470, 310, 1.0), bg="roomb", table=410, cloth="#a8512c",
                 shadow=(470, 376, 216, 24, .34), light=(240, 350, 280, .3))


def sc_beloe(t, dur=8.0):
    """Всё совсем белое: отварной рис и тофу — цвет траура на Востоке."""
    b = (f'<path d="M-170 -10 C-170 44 -130 72 -74 72 C-18 72 22 44 22 -10 Z" fill="{SNOW}"{ST(8)}/>'
         f'<path d="M-160 -12 C-140 -46 -8 -46 12 -12 C-10 4 -138 4 -160 -12 Z" fill="#f6f2e8"{ST(6)}/>')
    for i in range(14):
        b += f'<ellipse cx="{-140+i*11}" cy="{-24-(i%3)*7}" rx="6" ry="3.6" fill="#fff" opacity=".9"/>'
    b += (f'<path d="M58 44 L198 44 L198 -24 L58 -24 Z" fill="#fbf7ee"{ST(8)}/>'
          f'<path d="M86 -24 L86 44 M128 -24 L128 44 M170 -24 L170 44" stroke="#e4ded0" stroke-width="5"/>')
    b += f'<path d="M-180 -44 L-120 -74" stroke="#d9d2c2" stroke-width="9" stroke-linecap="round"/>'
    return stage(t, dur, g(b, 460, 312, 1.0), bg="roomb", table=408, cloth="#8a7a5e",
                 shadow=(460, 390, 200, 24, .3), sign=(460, 300, 180, 28), light=(240, 350, 260, .28))


def sc_grushi(t, dur=8.0):
    """Груши — «груша» звучит как «расставание»."""
    b = f'<ellipse cx="0" cy="60" rx="170" ry="44" fill="{CRM}"{ST(8)}/>'
    for x, sc in ((-82, 1.0), (6, 1.14), (90, .96)):
        b += (f'<g transform="translate({x},{16-16*sc}) scale({sc})">'
              f'<path d="M0 44 C-34 44 -46 20 -38 -2 C-32 -20 -18 -26 -16 -42'
              f' C-14 -56 -6 -62 0 -62 C6 -62 14 -56 16 -42 C18 -26 32 -20 38 -2'
              f' C46 20 34 44 0 44 Z" fill="#b2c04a"{ST(7)}/>'
              f'<path d="M0 -62 L2 -78 M2 -78 q14 -8 20 2" stroke="#6b4a2c" stroke-width="5" fill="none"/>'
              f'<path d="M-22 6 C-18 -8 -8 -16 0 -18" stroke="#9aa83c" stroke-width="4" fill="none"/></g>')
    return stage(t, dur, g(b, 460, 302, 1.0), bg="roomc", table=408, cloth="#b8463f",
                 shadow=(460, 396, 168, 24, .36), sign=(460, 288, 172, 28),
                 light=(760, 350, 250, .3), x0=12, x1=-10)


def sc_lapsha(t, dur=8.0):
    """Длинная лапша: нити тянутся, палочки поднимают прядь, нож под запретом."""
    b = f'<path d="M-150 -6 C-150 52 -106 84 0 84 C106 84 150 52 150 -6 Z" fill="{SNOW}"{ST(8)}/>'
    for i in range(11):
        x = -120 + i * 24
        b += (f'<path d="M{x} -8 C{x-14} 18 {x+14} 40 {x} 64" stroke="#e8d9a8" stroke-width="7"'
              f' fill="none" stroke-linecap="round"/>')
    b += f'<path d="M-140 -8 C-80 -30 80 -30 140 -8 C80 10 -80 10 -140 -8 Z" fill="#edd9a0"{ST(6)}/>'
    lift = 10 * A.w(t, 4.2)
    b += (f'<g transform="translate(96,{-96+lift:.1f})">'
          f'<path d="M-10 0 L34 -86 M10 2 L54 -84" stroke="#8a5a2c" stroke-width="9" stroke-linecap="round"/>'
          + "".join(f'<path d="M{-6+j*9} 6 C{-14+j*9} 46 {2+j*9} 76 {-6+j*9} 104"'
                    f' stroke="#e8d9a8" stroke-width="6" fill="none" stroke-linecap="round"/>' for j in range(3))
          + '</g>')
    b += (f'<g transform="translate(-170,-70) rotate(-18)">'
          f'<path d="M0 0 L104 -26 L112 -6 L8 20 Z" fill="#c9c4bb"{ST(6)}/>'
          f'<path d="M-6 2 L-56 14 L-52 34 L2 22 Z" fill="#6b4a2c"{ST(6)}/></g>')
    return stage(t, dur, g(b, 480, 316, 1.0), bg="roomb", table=414, cloth="#a8512c",
                 shadow=(480, 396, 178, 24, .34), sign=(380, 250, 128, 22), light=(760, 350, 250, .3))


def sc_kasha(t, dur=8.0):
    """Каша в миске: густая, ложка стоит, пар идёт — знак бедности."""
    b = (f'<path d="M-140 -10 C-140 52 -96 86 0 86 C96 86 140 52 140 -10 Z" fill="{CRM}"{ST(9)}/>'
         f'<path d="M-150 -10 L150 -10 L142 8 L-142 8 Z" fill="#d9cdb0"{ST(6)}/>')
    b += f'<path d="M-124 -12 C-108 -44 108 -44 124 -12 C92 8 -92 8 -124 -12 Z" fill="#e4d4b6"{ST(6)}/>'
    for i in range(9):
        b += f'<ellipse cx="{-96+i*24}" cy="{-26-(i%3)*6}" rx="11" ry="7" fill="#efe7d2" opacity=".9"/>'
    b += (f'<path d="M34 -30 C68 -40 92 -34 96 -22 C92 -12 64 -8 32 -18 Z" fill="#d9d2c2"{ST(6)}/>'
          f'<path d="M94 -24 L150 -86" stroke="#d9d2c2" stroke-width="12" stroke-linecap="round"/>')
    b += A.smoke(-20, -40, t, 3, 90, .8, .26)
    return stage(t, dur, g(b, 460, 306, 1.0), bg="roomb", table=408, cloth="#8a7a5e",
                 shadow=(460, 396, 170, 24, .34), sign=(460, 292, 170, 28), light=(240, 350, 260, .3))


def sc_pelmeni(t, dur=8.0):
    """Пельмени с защипом гребешком — «в форме слитков»."""
    b = f'<ellipse cx="0" cy="46" rx="186" ry="48" fill="{SNOW}"{ST(8)}/>'
    for x, y, sc in ((-110, 14, 1.0), (-36, 2, 1.06), (40, 12, 1.0), (112, 22, .94),
                     (-70, 44, .9), (10, 46, .92), (84, 50, .88)):
        b += (f'<g transform="translate({x},{y}) scale({sc})">'
              f'<path d="M-44 10 C-44 -16 -22 -30 0 -30 C22 -30 44 -16 44 10 C22 22 -22 22 -44 10 Z"'
              f' fill="#f2ead6"{ST(6)}/>'
              + "".join(f'<path d="M{-32+j*16} -16 q8 -10 16 -2" stroke="#d9cdb0" stroke-width="4" fill="none"/>'
                        for j in range(5)) + '</g>')
    for x in (-150, 150):
        b += (f'<path d="M{x-40} 44 L{x+40} 44 L{x+28} 10 L{x-28} 10 Z" fill="{GLD}"{ST(6)}/>'
              f'<path d="M{x-26} 14 L{x+26} 14" stroke="#e0b453" stroke-width="5"/>')
    b += A.smoke(0, -24, t, 2, 70, .7, .2)
    return stage(t, dur, g(b, 470, 316, 1.0), bg="roomc", table=412, cloth="#b8463f",
                 shadow=(470, 388, 196, 24, .34), light=(740, 350, 260, .3))


def sc_fonari(t, dur=8.0):
    """Китайские фонари: красные, качаются, свет тёплый."""
    b = ""
    for i, (x, y, sc) in enumerate(((-230, -40, 1.0), (-80, -84, 1.16), (80, -56, 1.04), (236, -96, .92))):
        sw = A.sway(t, 5.4 + i * .5, i * .3, 2.6)
        b += (f'<g transform="translate({x},{y}) rotate({sw:.2f}) scale({sc})">'
              f'<path d="M0 -92 L0 -62" stroke="{GLD}" stroke-width="5"/>'
              f'<path d="M-46 -30 C-46 -58 -26 -62 0 -62 C26 -62 46 -58 46 -30'
              f' C46 -2 26 4 0 4 C-26 4 -46 -2 -46 -30 Z" fill="{RED}"{ST(7)}/>'
              f'<path d="M-22 -58 C-30 -36 -30 -24 -22 0 M22 -58 C30 -36 30 -24 22 0"'
              f' stroke="#8d1420" stroke-width="4" fill="none"/>'
              f'<path d="M-30 -62 L30 -62 L30 -70 L-30 -70 Z" fill="{GLD}"{ST(5)}/>'
              f'<path d="M-26 4 L26 4 L26 12 L-26 12 Z" fill="{GLD}"{ST(5)}/>'
              + "".join(f'<path d="M{-18+j*9} 12 L{-20+j*9} 36" stroke="{GLD}" stroke-width="4"/>' for j in range(5))
              + '</g>')
    return stage(t, dur, g(b, 470, 240, 1.0), bg="roomr", table=440, cloth="#b8463f",
                 cand=((150, 0, 54, 1.0), (790, 0, 48, .9)), nearc=(),
                 light=(470, 220, 360, .36), z1=100, vig=".6")


def sc_kalendar(t, dur=8.0):
    """31 декабря и 17 февраля: мы встречаем раньше китайцев."""
    b = ""
    for x, big, small, col in ((-150, "31", "ДЕКАБРЯ", TER), (150, "17", "ФЕВРАЛЯ", RED)):
        b += (f'<g transform="translate({x},0)">'
              f'<rect x="-104" y="-104" width="208" height="208" rx="12" fill="{SNOW}"{ST(9)}/>'
              f'<rect x="-104" y="-104" width="208" height="54" rx="12" fill="{col}"{ST(7)}/>'
              f'<circle cx="-54" cy="-112" r="9" fill="{GLD}"{ST(5)}/><circle cx="54" cy="-112" r="9" fill="{GLD}"{ST(5)}/>'
              f'<text x="0" y="46" text-anchor="middle" font-family="DejaVu Serif" font-size="108"'
              f' font-weight="bold" fill="{OUT}">{big}</text>'
              f'<text x="0" y="86" text-anchor="middle" font-family="DejaVu Sans" font-size="26"'
              f' fill="#6b6256">{small}</text></g>')
    return stage(t, dur, g(b, 470, 272, 1.0), bg="roomb", table=452, cloth="#a8512c",
                 cand=((120, 0, 50, .9), (820, 0, 46, .85)), nearc=(),
                 light=(470, 250, 340, .32), z1=100)


# ------------------------- стол, подача, сравнение -------------------------
def sc_dva_etaza(t, dur=8.0):
    """Тарелки в два этажа: ставить бокал некуда."""
    b = (f'<ellipse cx="0" cy="92" rx="150" ry="40" fill="{CRM}"{ST(8)}/>'
         f'<ellipse cx="0" cy="40" rx="126" ry="34" fill="{SNOW}"{ST(8)}/>'
         f'<ellipse cx="4" cy="-8" rx="104" ry="28" fill="{CRM}"{ST(8)}/>')
    b += g(_meat(70, 32), 0, -36, .9)
    b += f'<path d="M-150 86 C-186 76 -196 48 -178 34" stroke="{OUT}" stroke-width="8" fill="none"/>'
    b += (f'<g transform="translate(176,40) rotate(14)">'
          f'<path d="M-24 -54 L24 -54 L16 0 L-16 0 Z" fill="#cfe6f2" opacity=".7"{ST(6)}/>'
          f'<path d="M0 0 L0 30 M-16 32 L16 32" stroke="{OUT}" stroke-width="7" fill="none"/></g>')
    return stage(t, dur, g(b, 450, 280, 1.0), bg="roomr", table=408, cloth="#b8463f",
                 shadow=(450, 376, 164, 26, .4), light=(760, 350, 250, .3), x0=12, x1=-10)


def sc_zavalen(t, dur=8.0):
    """Стол ломится: блюда внахлёст, места нет совсем."""
    b = ""
    items = ((-300, 10, .8, "sal"), (-150, -10, .9, "meat"), (0, 6, .95, "saus"),
             (150, -8, .88, "sal2"), (300, 8, .82, "meat2"), (-230, 60, .78, "saus2"),
             (-60, 66, .8, "sal3"), (120, 64, .8, "meat3"), (280, 68, .76, "sal4"))
    for x, y, sc, kind in items:
        if kind.startswith("sal"):
            inner = (f'<ellipse cx="0" cy="0" rx="92" ry="28" fill="{CRM}"{ST(6)}/>'
                     f'<path d="M-72 -8 C-50 -40 50 -40 72 -8 C48 8 -48 8 -72 -8 Z" fill="{SNOW}"{ST(5)}/>')
        elif kind.startswith("meat"):
            inner = f'<ellipse cx="0" cy="12" rx="94" ry="26" fill="{CRM}"{ST(6)}/>' + g(_meat(62, 28), 0, -10, 1.0)
        else:
            inner = A2.sausage_plate(0, 0, .52)
        b += g(inner, x, y, sc)
    b += (f'<g transform="translate(336,-58) rotate(16)">'
          f'<path d="M-22 -50 L22 -50 L15 0 L-15 0 Z" fill="#cfe6f2" opacity=".7"{ST(6)}/>'
          f'<path d="M0 0 L0 26 M-14 28 L14 28" stroke="{OUT}" stroke-width="6" fill="none"/></g>')
    return stage(t, dur, g(b, 470, 288, 1.0), bg="roomr", table=372, cloth="#b8463f",
                 cand=((86, 0, 44, .8),), nearc=(),
                 shadow=(470, 392, 400, 30, .34), light=(480, 330, 360, .3), z1=100)


def sc_pustoy_stol(t, dur=8.0):
    """Пустой стол в полночь: одна тарелка и крошки."""
    b = (f'<ellipse cx="0" cy="0" rx="118" ry="32" fill="{SNOW}"{ST(8)}/>'
         f'<ellipse cx="0" cy="-6" rx="92" ry="24" fill="#efe7d2"/>')
    b += "".join(f'<circle cx="{-40+i*26}" cy="{-8+(i%2)*6}" r="3.4" fill="#cdbfa2"/>' for i in range(4))
    b += (f'<g transform="translate(150,-10) rotate(-12)">'
          f'<path d="M-20 -44 L20 -44 L14 0 L-14 0 Z" fill="#cfe6f2" opacity=".55"{ST(6)}/>'
          f'<path d="M0 0 L0 24 M-13 26 L13 26" stroke="{OUT}" stroke-width="6" fill="none"/></g>')
    return stage(t, dur, g(b, 460, 344, 1.0), bg="roomb", table=420, cloth="#8a7a5e",
                 shadow=(460, 378, 140, 20, .3), light=(240, 360, 250, .26), vig=".72")


def sc_polufabrikaty(t, dur=8.0):
    """Покупные котлеты, наггетсы и пицца из коробки."""
    b = (f'<path d="M-200 30 L-30 30 L-30 -46 L-200 -46 Z" fill="#c9a27a"{ST(8)}/>'
         f'<path d="M-200 -46 L-116 -92 L-30 -46 Z" fill="#b08a62"{ST(7)}/>'
         f'<text x="-116" y="6" text-anchor="middle" font-family="DejaVu Sans" font-size="30"'
         f' fill="#6b5236">ПИЦЦА</text>')
    b += f'<path d="M10 34 L190 34 L178 -16 L22 -16 Z" fill="#d9d2c2"{ST(7)}/>'
    for i in range(5):
        b += (f'<path d="M{34+i*32} 24 C{30+i*32} 2 {44+i*32} -8 {58+i*32} -2'
              f' C{66+i*32} 6 {58+i*32} 24 {34+i*32} 24 Z" fill="#d1913f"{ST(5)}/>')
    b += (f'<ellipse cx="60" cy="-54" rx="54" ry="22" fill="#8a4a24"{ST(6)}/>'
          f'<ellipse cx="146" cy="-48" rx="48" ry="20" fill="#8a4a24"{ST(6)}/>')
    return stage(t, dur, g(b, 460, 306, 1.0), bg="roomb", table=406, cloth="#a8512c",
                 shadow=(460, 392, 210, 24, .34), sign=(460, 292, 186, 28), light=(760, 350, 250, .3))


def sc_sravnenie(t, dur=10.0):
    """ДВА СТОЛА РЯДОМ на разделённом экране: слева год Лошади (ломится),
    справа год Козы (воздух между тарелками). Его просьба 05.11."""
    cx, cz, _ = dolly(t, dur, z0=0, z1=70, x0=0, x1=0)
    u = A2.ease(min(1.0, t / max(.1, dur * .55)))
    s = f'<rect width="{W}" height="{H}" fill="url(#roomb)"/>'
    left = f'<rect x="0" y="0" width="480" height="540" fill="url(#roomr)"/>'
    left += art.table(392, "#b8463f")
    lefts = ((70, 348, .46), (180, 340, .5), (290, 346, .46), (390, 352, .42),
             (120, 392, .44), (240, 386, .46), (350, 392, .42), (60, 420, .4), (300, 428, .4))
    for i, (x, y, sc) in enumerate(lefts):
        if i / float(len(lefts)) > u:
            continue
        if i % 3 == 0:
            inner = A2.sausage_plate(0, 0, .5)
        elif i % 3 == 1:
            inner = (f'<ellipse cx="0" cy="0" rx="92" ry="28" fill="{CRM}"{ST(6)}/>'
                     f'<path d="M-70 -8 C-48 -38 48 -38 70 -8 C46 8 -46 8 -70 -8 Z" fill="{SNOW}"{ST(5)}/>')
        else:
            inner = f'<ellipse cx="0" cy="12" rx="90" ry="26" fill="{CRM}"{ST(6)}/>' + g(_meat(58, 26), 0, -8, 1.0)
        left += g(inner, x, y, sc)
    left += candles([(40, 392, 44, .8)], t)
    right = f'<rect x="480" y="0" width="480" height="540" fill="url(#roomc)"/>'
    right += f'<path d="M480 392 L960 392 L960 540 L480 540 Z" fill="url(#cloth)"/>'
    right += f'<path d="M480 384 L960 384 L960 404 L480 404 Z" fill="#b8463f"/>'
    for i, (x, y, sc, kind) in enumerate(((600, 350, .5, "g"), (775, 344, .54, "b"),
                                          (680, 414, .46, "c"), (880, 410, .44, "f"))):
        if i / 4.0 > u:
            continue
        inner = {"g": A2.dish_greens(0, 0, 1.0), "b": A2.dish_bird(0, 0, 1.0),
                 "c": A2.dish_cheese(0, 0, 1.0), "f": A2.dish_fruit(0, 0, 1.0)}[kind]
        right += g(inner, x, y, sc)
    right += candles([(560, 392, 46, .85), (930, 392, 40, .8)], t)
    s += plane(left + right, Z_HERO, cx, cz)
    s += f'<path d="M480 0 L480 540" stroke="{OUT}" stroke-width="10"/>'
    for x, txt, col in ((240, "ГОД ЛОШАДИ", "#d9d2c2"), (720, "ГОД КОЗЫ", GLD)):
        s += (f'<rect x="{x-176}" y="34" width="352" height="74" rx="10" fill="#0e0e0e" opacity=".88"/>'
              f'<rect x="{x-176}" y="34" width="352" height="6" rx="3" fill="{col}"/>'
              f'<text x="{x}" y="88" text-anchor="middle" font-family="DejaVu Sans" font-size="44"'
              f' font-weight="bold" fill="{col}">{txt}</text>')
    s += warm_light(240, 360, 260, .26) + warm_light(720, 356, 280, .3) + air()
    s += f'<rect width="{W}" height="{H}" fill="url(#vign)" opacity=".6"/>'
    return s


def sc_tri_zveri(t, dur=8.0):
    """Коза, овца и баран в ряд: «англичане пишут то овцу, то барана,
    то вообще козла» — спор об имени хозяйки года."""
    b = ""
    for i, (x, kind) in enumerate(((-300, "koza"), (0, "ovca"), (300, "baran"))):
        sw = A.sway(t, 5.8, i * .33, 1.6)
        g_ = f'<g transform="translate({x},0) rotate({sw:.2f} 0 60)">'
        # туловище
        g_ += (f'<path d="M-74 58 C-74 12 -44 -14 4 -14 C52 -14 82 12 82 58'
               f' C82 82 -74 82 -74 58 Z" fill="{WOOL if kind != "koza" else SNOW}"{ST(8)}/>')
        if kind == "ovca":
            for j in range(6):
                g_ += f'<circle cx="{-54+j*24}" cy="{8+(j%2)*14}" r="17" fill="{WOOL}"{ST(5)}/>'
        # ноги
        g_ += (f'<path d="M-44 76 L-44 124 M-10 78 L-10 124 M26 78 L26 124 M60 76 L60 124"'
               f' stroke="{OUT}" stroke-width="11" stroke-linecap="round"/>')
        # голова крупнее туловища по пропорции мультяшки
        head = (f'<path d="M0 0 C-30 -4 -52 -22 -54 -50 C-56 -76 -36 -94 -10 -92'
                f' C10 -90 22 -74 20 -52 C18 -28 14 -8 0 0 Z"'
                f' fill="{SNOW if kind == "koza" else "#e8dcc2"}"{ST(8)}/>'
                f'<circle cx="-30" cy="-58" r="7" fill="{OUT}"/>'
                f'<path d="M-46 -16 C-54 -8 -58 -2 -56 6" stroke="{OUT}" stroke-width="6" fill="none"/>')
        if kind == "koza":
            head += (f'<path d="M-14 -92 C-18 -126 -2 -148 26 -152 C10 -134 0 -114 -2 -94 Z"'
                     f' fill="#7a6246"{ST(7)}/>'
                     f'<path d="M-44 -6 C-50 16 -46 32 -38 42" stroke="{SNOW}" stroke-width="12"'
                     f' fill="none" stroke-linecap="round"/>'
                     f'<path d="M12 -70 C34 -78 54 -70 58 -56 C40 -46 18 -52 10 -62 Z" fill="#e2d6bc"{ST(6)}/>')
        elif kind == "baran":
            head += (f'<path d="M-18 -88 C-56 -98 -74 -70 -52 -50 C-36 -36 -14 -46 -16 -62"'
                     f' fill="none" stroke="#7a6246" stroke-width="13" stroke-linecap="round"/>'
                     f'<path d="M12 -66 C34 -74 54 -66 58 -52 C40 -42 18 -48 10 -58 Z" fill="#e2d6bc"{ST(6)}/>')
        else:
            head += (f'<path d="M-20 -90 C-38 -100 -48 -90 -42 -78" stroke="#7a6246" stroke-width="10"'
                     f' fill="none" stroke-linecap="round"/>'
                     f'<path d="M12 -68 C36 -76 56 -66 60 -52 C42 -42 18 -50 10 -60 Z" fill="#e2d6bc"{ST(6)}/>')
        g_ += f'<g transform="translate(-58,8) scale(1.25)">{head}</g>'
        q = 1 + .08 * A.w(t, 2.4, i * .3)
        g_ += (f'<g transform="translate(10,-140) scale({q:.3f})">'
               f'<text x="0" y="0" text-anchor="middle" font-family="DejaVu Serif" font-size="82"'
               f' font-weight="bold" fill="{GLD}" stroke="{OUT}" stroke-width="6">?</text></g>')
        b += g_ + '</g>'
    return stage(t, dur, g(b, 470, 276, .78), bg="roomb", table=456, cloth="#a8512c",
                 cand=((110, 0, 48, .9), (840, 0, 44, .85)), nearc=(),
                 light=(470, 280, 350, .32), z1=105)


SCENES = {n[3:]: f for n, f in list(globals().items()) if n.startswith("sc_")}
NO_GLARE = {"sravnenie"}
