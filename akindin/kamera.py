# -*- coding: utf-8 -*-
"""КАМЕРА И ГЛУБИНА. Взято из лаборатории камеры (C1-C16) и «Года козы»
(K9, K13, K44-K55) один в один по параметрам: smoother на всех ходах,
панорама ±30°, удар push 0,6 с, дуга 32°, долли-зум.

Кадр собран из ПЛАНОВ ПО ГЛУБИНЕ (C1/K9). У каждого слоя своё z; смещение и
масштаб слоя считаются от хода камеры по множителю p(z) = F/(F+z):
небо почти стоит, передний план проносится. Это и есть наш объём —
без него «зум» остаётся плоским растягиванием картинки.
"""
import math, re
import anim as A
from baza import W, H

F = 1400.0                       # фокусное: чем меньше, тем сильнее расхождение планов

# глубины слоёв (размечены прямо в baza.py)
Z = {"nebo": 1500, "dal": 520, "sred": 420, "deystvie": 0, "pered": -230, "letit": -120}


def smoother(x):
    x = max(0.0, min(1.0, x))
    return x * x * x * (x * (x * 6 - 15) + 10)


def punch(u):
    """Кривая удара push: концы мягкие, середина стремительная (C9/K46)."""
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u) ** 2 if u < .5 else 1 - (1 - u) ** 3


def p_sloya(z):
    return F / (F + z)


# ── ХОДЫ КАМЕРЫ ────────────────────────────────────────────────────────────
# каждый возвращает (camx, camy, zoom, ugol) в момент k ∈ [0,1]
# Амплитуды подрезаны после сведения: при ходе ±300 по плану действия главный
# предмет уезжал за край и кадр оставался пустым (поймано на планах 2, 19, 48).
# Ход НАЧИНАЕТСЯ на главном (оно слева) и открывает второй план, а не бросает его.
def hod_naezd(k):      return 0, 0, 1.0 + .18 * smoother(k), 0
def hod_naezd_bystro(k): return 0, 0, 1.0 + .26 * punch(min(1, k * 1.6)), 0
def hod_otezd(k):      return 0, 0, 1.22 - .22 * smoother(k), 0
def hod_pan_lp(k):     return -40 + 150 * smoother(k), 0, 1.06, 0
def hod_pan_pl(k):     return 110 - 150 * smoother(k), 0, 1.06, 0
def hod_tilt_up(k):    return 0, 62 - 124 * smoother(k), 1.08, 0
def hod_tilt_down(k):  return 0, -62 + 124 * smoother(k), 1.08, 0
def hod_kran(k):       return 0, 80 - 160 * smoother(k), 1.16 - .10 * smoother(k), 0
def hod_snizhenie(k):  return 0, -70 + 140 * smoother(k), 1.05 + .10 * smoother(k), 0
def hod_provodka(k):   return -70 + 190 * smoother(k), 0, 1.10, 0
def hod_vertigo(k):    return 0, 0, 1.26 - .26 * smoother(k), 0   # мир наваливается на слои
def hod_dutch(k):      return 0, 0, 1.10, -3.0 * smoother(k)


def hod_duga(k):
    """Дуга 32° (C12/K49): ракурс едет вбок, кадр остаётся кадром."""
    a = math.radians(-16 + 32 * smoother(k))
    return math.sin(a) * 160, -math.cos(a) * 22 + 22, 1.08, math.degrees(a) * .14


def hod_push(k):
    """Три удара под слово (C9/K46): назад камера не отходит."""
    z = 1.0
    for t0, d, z0, z1 in ((.18, .09, 1.0, 1.09), (.46, .09, 1.09, 1.18), (.74, .09, 1.18, 1.27)):
        if k >= t0:
            z = z0 + (z1 - z0) * punch(min(1.0, (k - t0) / d))
    return 0, 0, z, 0


def hod_stat(k):
    """Статики не бывает (R-0009): еле заметное дыхание кадра."""
    return 12 * math.sin(k * math.pi), 7 * math.sin(k * math.pi * .7), 1.02 + .03 * k, 0


HODY = {
    "наезд": hod_naezd, "наезд_быстро": hod_naezd_bystro, "отъезд": hod_otezd,
    "панорама_лп": hod_pan_lp, "панорама_пл": hod_pan_pl,
    "наклон_вверх": hod_tilt_up, "наклон_вниз": hod_tilt_down,
    "кран": hod_kran, "снижение": hod_snizhenie, "проводка": hod_provodka,
    "дуга": hod_duga, "долли_зум": hod_vertigo, "наклон_горизонта": hod_dutch,
    "push": hod_push, "дыхание": hod_stat,
}


def _odin(s):
    """Одна фраза описания → имя хода."""
    if "резк" in s and "наезд" in s:
        return "наезд_быстро"
    if "долли" in s or "вертиго" in s:
        return "долли_зум"
    if "кран" in s or "подъем-кран" in s:
        return "кран"
    if "дуг" in s or "облет" in s or "вокруг" in s:
        return "дуга"
    if ("проезд за" in s or "проводк" in s or "идет за" in s or "за героем" in s
            or "за путником" in s or "за тачкой" in s or "за огоньком" in s
            or "за ней" in s or "привязана" in s):
        return "проводка"
    if "наклон" in s or "взгляд" in s or "бросок" in s:
        i = s.find("наклон")
        hvost = s[i:] if i >= 0 else s
        if "вверх" in hvost and ("вниз" not in hvost or hvost.find("вверх") < hvost.find("вниз")):
            return "наклон_вверх"
        if "вниз" in hvost:
            return "наклон_вниз"
    if "наклон от" in s or "от тучи" in s or "от солнца к" in s:
        return "наклон_вниз"                    # «наклон от X к Y»: ведёт сверху вниз
    if "подъем в небо" in s or "подъем к небу" in s or "уход в небо" in s:
        return "кран"
    if "вращен" in s or "облёт" in s:
        return "дуга"
    if "сдвиг к" in s or "сдвиг на" in s:
        return "панорама_лп"
    if "снижен" in s:
        return "снижение"
    if "вверх за" in s or "снизу вверх" in s or "до крыши" in s or "до звезды" in s:
        return "наклон_вверх"
    if "сверху вниз" in s or "вниз на" in s or "вниз к" in s:
        return "наклон_вниз"
    if "справа налево" in s:
        return "панорама_пл"
    if "панорам" in s or "слева направо" in s or "вдоль" in s or "сдвиг впр" in s or "по ряду" in s:
        return "панорама_лп"
    if "отъезд" in s or "отъезжа" in s or "отъехать" in s:
        return "отъезд"
    if "тряск" in s or "трях" in s or "удар" in s:
        return "push"
    if "наезд" in s or "наплыв" in s or "приближ" in s or "push" in s:
        return "наезд"
    return None


_SKLEYKA = re.compile(r"\s*(?:,?\s*(?:затем|потом|после|далее|в конце|и обратно|и снова)\b|;)\s*")


def razobrat(opisanie):
    """Колонка «Камера» → ход или ПАРА ходов. Камера делает ТО, ЧТО НАПИСАНО
    в раскадровке, а не случайный зум: «наезд, затем сдвиг вправо» — это два
    движения подряд, и в кадре их видно именно два."""
    s = (opisanie or "").lower().replace("ё", "е")
    kuski = [k for k in _SKLEYKA.split(s) if k.strip()]
    hody = []
    for k in kuski:
        h = _odin(k)
        if h and (not hody or hody[-1] != h):
            hody.append(h)
    if not hody:
        return "дыхание"
    if len(hody) == 1:
        return hody[0]
    return (hody[0], hody[1])


def _hod_f(hod):
    if isinstance(hod, tuple):
        a, b = HODY.get(hod[0], hod_stat), HODY.get(hod[1], hod_stat)

        def para(k, _a=a, _b=b):
            """Два движения подряд: первое до 55%, второе — остаток, стык сшит."""
            if k < .55:
                return _a(k / .55)
            x0, y0, z0, u0 = _a(1.0)
            x1, y1, z1, u1 = _b((k - .55) / .45)
            x2, y2, z2, u2 = _b(0.0)
            return (x0 + x1 - x2, y0 + y1 - y2, z0 * (z1 / z2 if z2 else 1), u0 + u1 - u2)
        return para
    return HODY.get(hod, hod_stat)


# ── СБОРКА КАДРА ПО СЛОЯМ ──────────────────────────────────────────────────
_OTKR = re.compile(r'<g data-z="(-?\d+|fix)">')
_ZAKR = '</g><!--/z-->'


def sloi(svg):
    """Разбить вывод декорации на слои по глубине.
    Вложенный слой (например небо ВНУТРИ окна избы) остаётся частью родителя:
    содержимое окна не должно уезжать своей глубиной."""
    out, poz = [], 0
    while True:
        m = _OTKR.search(svg, poz)
        if not m:
            break
        if m.start() > poz:
            out.append((Z["deystvie"], svg[poz:m.start()]))
        gl, i = 1, m.end()
        while gl:
            nx = _OTKR.search(svg, i)
            zk = svg.find(_ZAKR, i)
            if zk < 0:
                zk = len(svg)
            if nx and nx.start() < zk:
                gl += 1
                i = nx.end()
            else:
                gl -= 1
                i = zk + len(_ZAKR)
        z = m.group(1)
        out.append((z if z == "fix" else int(z), svg[m.end():i - len(_ZAKR)]))
        poz = i
    if poz < len(svg):
        out.append((Z["deystvie"], svg[poz:]))
    return out


def haze(z, k=1.0):
    """Воздушная перспектива (fog из лаборатории): дальний план чуть выцветает.
    Размытия рендер не умеет, глубину даёт вуаль. Сильная вуаль читается как
    туман на весь кадр — поэтому потолок 0,16 и только от z=500."""
    if z < 500:
        return ""
    op = min(.16, .16 * (z / 1500.0)) * k
    if op < .02:
        return ""
    return (f'<rect x="-400" y="-300" width="{W+800}" height="{H+600}"'
            f' fill="#8fa3bd" opacity="{op:.3f}"/>')


SHIROKIE = ("панорама_лп", "панорама_пл", "проводка", "дуга", "кран",
            "наклон_вверх", "наклон_вниз", "снижение")


def overscan_dlya(hod):
    """Запас кадра: при сдвиге слоёв у краёв иначе обнажаются дыры."""
    h = hod if isinstance(hod, tuple) else (hod,)
    return 1.09 if any(x in SHIROKIE for x in h) else 1.05


def kadr(svg_dekoracii, hod, k, overscan=None):
    """Кадр: слои разъезжаются по глубине под ход камеры."""
    overscan = overscan or overscan_dlya(hod)
    camx, camy, zoom, ug = _hod_f(hod)(k)
    sl = sloi(svg_dekoracii)
    fix = "".join(telo for z, telo in sl if z == "fix")
    out = (f'<g transform="translate({W/2:.0f},{H/2:.0f}) rotate({ug:.3f})'
           f' scale({overscan:.3f}) translate({-W/2:.0f},{-H/2:.0f})">')
    for z, telo in sl:
        if z == "fix":
            continue
        p = p_sloya(z)
        s = 1.0 + (zoom - 1.0) * p
        dx = -camx * p
        dy = -camy * p
        if z < 0:                  # передний план не уносим за край кадра
            dx = max(-330, min(330, dx))
            dy = max(-210, min(210, dy))
        out += (f'<g transform="translate({W/2+dx:.2f},{H/2+dy:.2f}) scale({s:.4f})'
                f' translate({-W/2:.2f},{-H/2:.2f})">{telo}{haze(z)}</g>')
    return out + "</g>" + fix
