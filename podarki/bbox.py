# -*- coding: utf-8 -*-
"""Габариты предметов кадра — чтобы гейт считал ПРЕДМЕТЫ, а не фон.

Поймано 15.11 на первой порции «Дня Ионы»: исполнитель закрывал норму
«крупный предмет от 420 px» полосой земли во весь низ кадра, и сцена с
фигуркой на пустом поле проходила гейт. Фон, небо, земля и стена шириной
почти во весь холст предметом не считаются.
"""
import re

W, H = 1920, 1080
_NUM = re.compile(r"-?\d+\.?\d*")
_TAG = re.compile(r"<(rect|circle|ellipse|line|polygon|polyline|path|image|text)\b([^>]*)>")


def _at(s, name):
    m = re.search(r'\b%s="(-?\d+\.?\d*)"' % name, s)
    return float(m.group(1)) if m else None


_KOM = re.compile(r"([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)")


def _put_gabarit(d):
    """Габарит пути с учётом ОТНОСИТЕЛЬНЫХ команд.

    Прежде все числа из `d` читались как абсолютные координаты, и кирпичики
    baza.py (они написаны относительными `q 14,-8 …`) «весили» в замере
    больше, чем занимают в кадре: крупный предмет и пустота считались
    неверно. Поймано 15.11 на разборе первой порции «Дня Ионы»."""
    x = y = 0.0
    sx = sy = None
    xs, ys = [], []
    for kom, hvost in _KOM.findall(d):
        ch = [float(v) for v in _NUM.findall(hvost)]
        otn = kom.islower()
        k = kom.upper()
        if k == "Z":
            if sx is not None:
                x, y = sx, sy
            continue
        i = 0
        while i < len(ch) or (k in "MLHVCSQTA" and i == 0 and not ch):
            if k == "M" or k == "L" or k == "T":
                if i + 1 >= len(ch):
                    break
                nx, ny = ch[i], ch[i + 1]; i += 2
                x, y = (x + nx, y + ny) if otn else (nx, ny)
                if k == "M" and sx is None:
                    sx, sy = x, y
            elif k == "H":
                nx = ch[i]; i += 1
                x = x + nx if otn else nx
            elif k == "V":
                ny = ch[i]; i += 1
                y = y + ny if otn else ny
            elif k in ("C", "S", "Q"):
                n = {"C": 6, "S": 4, "Q": 4}[k]
                if i + n > len(ch):
                    break
                tochki = ch[i:i + n]; i += n
                for j in range(0, n, 2):
                    px = x + tochki[j] if otn else tochki[j]
                    py = y + tochki[j + 1] if otn else tochki[j + 1]
                    xs.append(px); ys.append(py)
                x = x + tochki[-2] if otn else tochki[-2]
                y = y + tochki[-1] if otn else tochki[-1]
            elif k == "A":
                if i + 7 > len(ch):
                    break
                tochki = ch[i:i + 7]; i += 7
                x = x + tochki[5] if otn else tochki[5]
                y = y + tochki[6] if otn else tochki[6]
            else:
                break
            xs.append(x); ys.append(y)
            if sx is None:
                sx, sy = x, y
    if not xs or not ys:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def predmety(svg):
    """[(x0, y0, x1, y1, тег, строка)] — габариты всех нарисованных кусков."""
    out = []
    for m in _TAG.finditer(svg):
        tag, at = m.group(1), m.group(2)
        try:
            if tag == "rect" or tag == "image":
                x, y = _at(at, "x") or 0, _at(at, "y") or 0
                w, h = _at(at, "width") or 0, _at(at, "height") or 0
                box = (x, y, x + w, y + h)
            elif tag == "circle":
                cx, cy, r = _at(at, "cx") or 0, _at(at, "cy") or 0, _at(at, "r") or 0
                box = (cx - r, cy - r, cx + r, cy + r)
            elif tag == "ellipse":
                cx, cy = _at(at, "cx") or 0, _at(at, "cy") or 0
                rx, ry = _at(at, "rx") or 0, _at(at, "ry") or 0
                box = (cx - rx, cy - ry, cx + rx, cy + ry)
            elif tag == "line":
                x1, y1 = _at(at, "x1") or 0, _at(at, "y1") or 0
                x2, y2 = _at(at, "x2") or 0, _at(at, "y2") or 0
                box = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            elif tag in ("polygon", "polyline"):
                d = re.search(r'\bpoints="([^"]*)"', at)
                if not d:
                    continue
                ch = [float(v) for v in _NUM.findall(d.group(1))]
                xs, ys = ch[0::2], ch[1::2]
                if not xs or not ys:
                    continue
                box = (min(xs), min(ys), max(xs), max(ys))
            elif tag == "path":
                d = re.search(r'\bd="([^"]*)"', at)
                if not d:
                    continue
                box = _put_gabarit(d.group(1))
                if box is None:
                    continue
            else:
                continue
        except Exception:
            continue
        out.append((box[0], box[1], box[2], box[3], tag, at))
    return out


def fon(b):
    """Фон, земля, небо, стена во весь кадр — это НЕ предмет."""
    x0, y0, x1, y1 = b[:4]
    return (x1 - x0) >= .80 * W or (y1 - y0) >= .80 * H


def svodka(svg):
    """Числа кадра: крупный предмет, предметы среднего плана, плотность центра."""
    p = [b for b in predmety(svg)]
    svoi = [b for b in p if not fon(b)]
    krupn = max(((b[3] - b[1]) for b in svoi), default=0)
    krupn_w = max(((b[2] - b[0]) for b in svoi), default=0)
    sredn = [b for b in svoi if 100 <= max(b[2] - b[0], b[3] - b[1]) <= 420]
    centr = [b for b in svoi
             if 400 <= (b[0] + b[2]) / 2 <= 1520 and 220 <= (b[1] + b[3]) / 2 <= 1000]
    return {"vsego": len(p), "predmetov": len(svoi), "fona": len(p) - len(svoi),
            "krupnyy": max(krupn, krupn_w), "krupnyy_v": krupn, "srednih": len(sredn),
            "v_centre": len(centr)}


def v_proeme(svg, proem):
    """ПОДСКАЗКА «посмотреть глазами», а не гейт: что из нашего нарисовано
    после метки и лежит ЦЕЛИКОМ во внутренних двух третях проёма.

    Поправлено 15.11 после прогона по 17-11: там из 15 проёмов «грязными»
    вышли 10, и почти все — ложные. Намеренный передний план (колонны перед
    аркой, створки ворот, ветки рябины перед дверью, огонь и искры поверх
    клипа в устье печи) попадает в габарит проёма и убирать его нельзя —
    это и есть «кадр внутри сцены». Настоящий брак другой: предмет стоит В
    САМОМ проёме и спорит с кадром (чашка на подоконнике, сеятель в окне).
    Поэтому считаем только то, что целиком внутри двух третей, а решение
    всегда за глазами."""
    x, y, w, h = proem
    vx0, vy0 = x + w / 6.0, y + h / 6.0
    vx1, vy1 = x + w * 5 / 6.0, y + h * 5 / 6.0
    met = svg.find('data-stok')
    if met < 0:
        return []
    out = []
    for b in predmety(svg[met:]):
        if b[0] >= vx0 and b[1] >= vy0 and b[2] <= vx1 and b[3] <= vy1:
            if 'fill="none"' in b[5]:
                continue
            out.append(b)
    return out


def setka(svg, cell=40):
    """Покрытие кадра ПРЕДМЕТАМИ по клеткам 40x40 (фон не в счёт).
    Пустая клетка — та, которую не накрыл ни один предмет."""
    nx, ny = W // cell, H // cell
    pole = [[0] * nx for _ in range(ny)]
    for b in predmety(svg):
        if fon(b):
            continue
        x0 = max(0, int(b[0] // cell)); x1 = min(nx - 1, int(b[2] // cell))
        y0 = max(0, int(b[1] // cell)); y1 = min(ny - 1, int(b[3] // cell))
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                pole[yy][xx] += 1
    vsego = nx * ny
    pusto = sum(1 for r in pole for c in r if c == 0)
    cx0, cx1 = 400 // cell, 1520 // cell
    cy0, cy1 = 220 // cell, 1000 // cell
    centr = [pole[y][x] for y in range(cy0, cy1) for x in range(cx0, cx1)]
    pusto_c = sum(1 for c in centr if c == 0)
    return {"pusto_dolya": round(pusto / vsego, 3),
            "pusto_centr": round(pusto_c / max(1, len(centr)), 3),
            "sloev_sred": round(sum(centr) / max(1, len(centr)), 1)}


_OP = re.compile(r'opacity="(\.\d+|0\.\d+|1(?:\.0)?)"')


def pyatna(svg):
    """Крупные полупрозрачные пятна: свет и дымка — норма, но ИМИ ЖЕ набивают
    плотность, когда рисовать лень (поймано 15.11 на доводке первой порции
    «Дня Ионы»: пятнадцать прозрачных прямоугольников подняли число слоёв,
    а кадр стал мутным). Гейтом не отбиваем — у принятого 17-11 их до 14 в
    сцене честно, на свет и воздух; просто показываем число глазам."""
    n = 0
    for b_ in predmety(svg):
        if fon(b_):
            continue
        m = _OP.search(b_[5])
        op = float(m.group(1)) if m else 1.0
        if op <= .35 and (b_[2] - b_[0]) >= 300 and (b_[3] - b_[1]) >= 120:
            n += 1
    return n
