# -*- coding: utf-8 -*-
"""Наложения ролика «13 ноября — Спиридон и Никодим»: плашки, титры, окно
вставки. Каждое — функция времени: приходит, живёт, уходит.
Кегли МЕРЯЮТСЯ ШРИФТОМ (мина 5 «Ёлки»: 86-й кегль лез под окно вставки)."""
import anim as A
from baza import *

SANS = "DejaVu Sans, Segoe UI, sans-serif"
SERIF = "DejaVu Serif, Georgia, serif"
# Ширину МЕРЯЕМ ШРИФТОМ, а не коэффициентом: правило 3 скилла. Коэффициент
# .54 обрезал «ЗАПРЕТ 1 — давать и брать в долг» на половине слова.
import functools
_FONTS = {"SERIF": "DejaVuSerif-Bold.ttf", "SANS": "DejaVuSans-Bold.ttf"}
_DIRS = ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu/",
         "/usr/share/fonts/TTF/")
try:
    from PIL import ImageFont as _IF
except Exception:
    _IF = None


@functools.lru_cache(maxsize=512)
def _font(name, size):
    if _IF is None:
        return None
    for d in _DIRS:
        try:
            return _IF.truetype(d + _FONTS[name], int(size))
        except Exception:
            continue
    return None


def wid(s, size, font="SERIF", ls=1):
    """Ширина строки в пикселях при данном кегле, с межбуквенным интервалом."""
    f = _font(font, size)
    if f is None:
        return len(s) * size * (.58 if font == "SANS" else .55) + len(s) * ls
    return f.getlength(s) + len(s) * ls


def kegl_pod(s, shir, font="SERIF", start=58, minim=22, ls=1):
    """Подобрать кегль, при котором строка влезает в заданную ширину."""
    k = start
    while k > minim and wid(s, k, font, ls) > shir:
        k -= 2
    return k


def txt(x, y, s, size=64, col="#fdf2dc", anchor="start", font=SERIF, ls=2,
        weight="bold", stroke=None, op=1.0):
    st = stroke if stroke is not None else max(3, size * .085)
    base = (f'font-family="{font}" font-size="{size:.1f}" font-weight="{weight}"'
            f' letter-spacing="{ls}" text-anchor="{anchor}" x="{x:.1f}" y="{y:.1f}"')
    out = ""
    if st:
        out += (f'<text {base} fill="none" stroke="{K}" stroke-width="{st:.1f}"'
                f' stroke-linejoin="round" opacity="{.9*op:.2f}">{s}</text>')
    return out + f'<text {base} fill="{col}" opacity="{op:.2f}">{s}</text>'


def plashka(x, y, s, t, t0, size=52, dur=.6, col="url(#zol)", tcol="#1a1208",
            pad=34, font=SERIF, maxw=760):
    """Золотая плашка: разворачивается слева направо, текст проявляется следом."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    fnt = "SERIF" if font == SERIF else "SANS"
    size = kegl_pod(s, maxw - pad * 2, fnt, size, 24)
    w_ = wid(s, size, fnt, 1) + pad * 2
    h_ = size * 1.62
    cid = "pl%d" % int(abs(x * 7 + y * 13 + size) % 99999)
    out = (f'<clipPath id="{cid}"><rect x="{x-4}" y="{y-6}" width="{w_*p+8:.0f}"'
           f' height="{h_+12:.0f}"/></clipPath><g clip-path="url(#{cid})">')
    out += ten(x + w_ / 2, y + h_ + 10, w_ * .45, 12, .4)
    out += f'<rect x="{x}" y="{y}" width="{w_:.0f}" height="{h_:.0f}" rx="10" fill="{col}" {o(6)}/>'
    out += (f'<text x="{x+pad:.0f}" y="{y+h_*.70:.0f}" font-family="{font}"'
            f' font-size="{size}" font-weight="bold" fill="{tcol}" letter-spacing="1">{s}</text>')
    out += "</g>"
    if p < 1:
        out += f'<rect x="{x+w_*p-6:.0f}" y="{y}" width="8" height="{h_:.0f}" fill="{SVET}" opacity=".9"/>'
    return out


def plashka_glavy(s, t, t0, y=470, dur=.9, shir=W):
    """Отбивка главы. Когда в кадре окно вставки, лента идёт ТОЛЬКО по левой
    полосе и не залезает на окно (мина 3 «Ёлки»)."""
    p = A.ease(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    h_ = 150
    kegl = kegl_pod(s, shir - 80, "SERIF", 76, 34, 6)
    out = (f'<rect x="0" y="{y}" width="{shir*p:.0f}" height="{h_}" fill="#1a1208" opacity=".9"/>'
           f'<rect x="0" y="{y}" width="{shir*p:.0f}" height="6" fill="{ZOL}"/>'
           f'<rect x="0" y="{y+h_-6}" width="{shir*p:.0f}" height="6" fill="{ZOL}"/>')
    if p > .5:
        q = A.ease((p - .5) / .5)
        out += txt(shir / 2, y + h_ * .68, s, kegl, SVET, "middle", SERIF, 6, op=q)
    return out


def plashka_zapreta(n, s, t, t0, x=90, y=170):
    """«ЗАПРЕТ N — ...»: номер в красном квадрате, текст на золоте."""
    p = A.out(A.seg(t, t0, .55))
    if p <= 0:
        return ""
    size = kegl_pod(s, 640, "SANS", 46, 22)
    w_ = wid(s, size, "SANS", 1) + 60
    out = ten(x + 60, y + 150, 90, 14, .45)
    out += (f'<g transform="scale({.6+.4*p:.3f}) translate({(x)*(1/(.6+.4*p)-1):.0f},'
            f'{(y)*(1/(.6+.4*p)-1):.0f})">')
    out += f'<rect x="{x}" y="{y}" width="120" height="120" rx="12" fill="{TKAN}" {o(7)}/>'
    out += txt(x + 60, y + 88, str(n), 74, "#fdf2dc", "middle", SERIF, 0)
    out += (f'<rect x="{x+132}" y="{y+18}" width="{w_:.0f}" height="84" rx="10"'
            f' fill="url(#zol)" {o(6)}/>')
    out += txt(x + 162, y + 76, s, size, "#1a1208", "start", SANS, 1, stroke=0)
    return out + "</g>"


def titr_obeshchanie(lines, t, t0, x=1010, y=300, dur=.5):
    """Первый кадр: три плашки одна под другой в свободной половине (R-0004)."""
    out = ""
    for i, (s, size) in enumerate(lines):
        out += plashka(x, y + i * (size * 1.62 + 26), s, t, t0 + i * dur * .8, size)
    return out


def nadpis(x, y, s, t, t0, size=40, col="#fdf2dc", anchor="middle", dur=.4):
    """Подпись на предмете: проявляется, не ездит."""
    p = A.ease(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    w_ = wid(s, size, "SANS", 1) + 36
    out = (f'<rect x="{x-w_/2 if anchor=="middle" else x-18:.0f}" y="{y-size*.95:.0f}"'
           f' width="{w_:.0f}" height="{size*1.42:.0f}" rx="8" fill="#140f0c" opacity="{.72*p:.2f}"/>')
    return out + txt(x, y, s, size, col, anchor, SANS, 1, op=p)


def kartochka(x, y, w_, h_, n, s, t, t0, dur=.5):
    """Карточка памятки: номер на красном, текст на креме."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    out = f'<g opacity="{p:.2f}" transform="translate({(1-p)*-50:.0f},0)">'
    out += ten(x + w_ / 2, y + h_ + 14, w_ * .42, 12, .35)
    out += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="14" fill="url(#krem)" {o(7)}/>'
    out += f'<rect x="{x}" y="{y}" width="92" height="{h_}" rx="14" fill="{TKAN}" {o(6)}/>'
    out += txt(x + 46, y + h_ * .68, str(n), 62, "#fdf2dc", "middle", SERIF, 0)
    size = 34
    if wid(s, size, "SANS", 0) > w_ - 140:
        sl = s.split()
        a_, b_ = "", ""
        for w in sl:
            if wid(a_ + " " + w, size, "SANS", 0) <= (w_ - 140) and not b_:
                a_ = (a_ + " " + w).strip()
            else:
                b_ = (b_ + " " + w).strip()
        size = kegl_pod(max(a_, b_, key=len), w_ - 140, "SANS", 32, 20)
        out += txt(x + 118, y + h_ * .46, a_, size, "#241a10", "start", SANS, 0, stroke=0)
        out += txt(x + 118, y + h_ * .80, b_, size, "#241a10", "start", SANS, 0, stroke=0)
    else:
        out += txt(x + 118, y + h_ * .62, s, size, "#241a10", "start", SANS, 0, stroke=0)
    return out + "</g>"


def okno_ramka(x, y, w_, h_):
    """Неподвижный контейнер вставки: тень, чёрный контур, золотая рамка."""
    return (f'<rect x="{x-18}" y="{y-18}" width="{w_+36}" height="{h_+36}" rx="26"'
            f' fill="#000" opacity=".45"/>'
            f'<rect x="{x-10}" y="{y-10}" width="{w_+20}" height="{h_+20}" rx="22"'
            f' fill="none" {o(14)}/>'
            f'<rect x="{x-10}" y="{y-10}" width="{w_+20}" height="{h_+20}" rx="22"'
            f' fill="none" stroke="{ZOL}" stroke-width="5"/>')


import base64, functools


@functools.lru_cache(maxsize=96)
def _vstroit(path):
    """Картинка ВСТРАИВАЕТСЯ в SVG, а не читается по ссылке: битый или
    недокачанный файл иначе валит рендер (ExpatError на раннере 11.11)."""
    try:
        d = open(path, "rb").read()
        if len(d) < 1200 or d[:2] != b"\xff\xd8":      # не JPEG — не рисуем
            return None
        return "data:image/jpeg;base64," + base64.b64encode(d).decode()
    except Exception:
        return None


def okno_foto(x, y, w_, h_, path, t, dur=6.0, faza=0, zhivoj=False):
    """Настоящий кадр ВНУТРИ окна (K30). Окно неподвижно (R-0014), кадр
    заполняет его целиком с обрезом по краям (R-0012), внутри идёт медленный
    Ken Burns — фотография не висит мёртвой (R-0006)."""
    k = min(1.0, max(0.0, t / max(.001, dur)))
    if zhivoj:
        z0 = z1 = 1.0       # клип движется сам
    else:
        z0, z1 = ((1.00, 1.12), (1.12, 1.00), (1.05, 1.15), (1.15, 1.05))[faza % 4]
    z = z0 + (z1 - z0) * A.ease(k)
    dx = 0.0 if zhivoj else (-1 if faza % 2 else 1) * 26 * A.ease(k)
    dy = 0.0 if zhivoj else (1 if faza % 3 else -1) * 18 * A.ease(k)
    src = _vstroit(path)
    if not src:
        return okno_ramka(x, y, w_, h_)
    cid = "ok%d" % (abs(hash((x, y, path))) % 99999)
    w2, h2 = w_ * z, h_ * z
    s = f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="12"/></clipPath>'
    s += (f'<g clip-path="url(#{cid})"><image href="{src}" x="{x-(w2-w_)/2+dx:.1f}"'
          f' y="{y-(h2-h_)/2+dy:.1f}" width="{w2:.1f}" height="{h2:.1f}"'
          f' preserveAspectRatio="xMidYMid slice"/></g>')
    return s + okno_ramka(x, y, w_, h_)


def okno_zaglushka(x, y, w_, h_, podpis, zapros=""):
    """Пустое окно с подписью — только для СВЕДЁННОЙ РАСКАДРОВКИ,
    чтобы видеть, что и когда встанет внутрь. В ролик не идёт."""
    s = f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="14" fill="#1d2630"/>'
    for i in range(14):
        s += (f'<line x1="{x+i*90-200}" y1="{y}" x2="{x+i*90}" y2="{y+h_}"'
              f' stroke="#2a3744" stroke-width="22"/>')
    s += okno_ramka(x, y, w_, h_)
    s += txt(x + w_ / 2, y + h_ * .44, podpis, 38, SVET, "middle", SANS, 1)
    if zapros:
        words = zapros.split()
        line, lines = "", []
        for w in words:
            if wid(line + " " + w, 26, "SANS") > w_ - 90:
                lines.append(line); line = w
            else:
                line = (line + " " + w).strip()
        lines.append(line)
        for i, ln in enumerate(lines[:4]):
            s += txt(x + w_ / 2, y + h_ * .56 + i * 34, ln, 26, "#cfd8e2", "middle", SANS, 0, stroke=2)
    return s


def vopros_plashka(s, t, t0, y=820):
    p = A.out(A.seg(t, t0, .6))
    if p <= 0:
        return ""
    size = 58
    w_ = wid(s, size, "SERIF", 2) + 90
    x = (W - w_) / 2
    out = f'<g opacity="{p:.2f}">'
    out += ten(W / 2, y + 120, w_ * .45, 14, .45)
    out += f'<rect x="{x:.0f}" y="{y}" width="{w_:.0f}" height="{size*1.75:.0f}" rx="14" fill="#1a1208" opacity=".9" {o(6)}/>'
    out += txt(W / 2, y + size * 1.2, s, size, SVET, "middle", SERIF, 2)
    return out + "</g>"


def kartochka_daty(x, y, w_, h_, s_, t, t0=.4, dur=.6):
    """Дата рисуется НАШЕЙ карточкой, не окном со стоком: «XII век», «1889»."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    sc = .82 + .18 * p
    out = (f'<g opacity="{p:.2f}" transform="translate({x+w_/2:.0f},{y+h_/2:.0f})'
           f' scale({sc:.3f}) translate({-(x+w_/2):.0f},{-(y+h_/2):.0f})">')
    out += ten(x + w_ / 2, y + h_ + 16, w_ * .42, 14, .45)
    out += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="18" fill="#1a1208" opacity=".92" {o(8)}/>'
    out += (f'<rect x="{x+14}" y="{y+14}" width="{w_-28}" height="{h_-28}" rx="12"'
            f' fill="none" stroke="{ZOL}" stroke-width="5"/>')
    kegl = kegl_pod(s_, w_ - 120, "SERIF", 130, 40, 4)
    out += txt(x + w_ / 2, y + h_ / 2 + kegl * .34, s_, kegl, SVET, "middle", SERIF, 4)
    return out + "</g>"


def plashka_vniz(s_, t, t0, y=900, dur=.6, maxw=1700):
    """Длинная плашка (поговорка, пословица) — лентой внизу, под окном вставки."""
    p = A.out(A.seg(t, t0, dur))
    if p <= 0:
        return ""
    kegl = kegl_pod(s_, maxw - 90, "SERIF", 56, 28, 1)
    w_ = wid(s_, kegl, "SERIF", 1) + 90
    x = (W - w_) / 2
    out = f'<g opacity="{p:.2f}">' + ten(W / 2, y + kegl * 1.9, w_ * .45, 13, .4)
    out += f'<rect x="{x:.0f}" y="{y}" width="{w_:.0f}" height="{kegl*1.7:.0f}" rx="12" fill="url(#zol)" {o(6)}/>'
    out += txt(W / 2, y + kegl * 1.18, s_, kegl, "#1a1208", "middle", SERIF, 1, stroke=0)
    return out + "</g>"
