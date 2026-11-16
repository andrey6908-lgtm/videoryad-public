# -*- coding: utf-8 -*-
"""ПОРЦИЯ 2: 35 декораций ролика «18 ноября — День Ионы».

Каждая функция — f(t) -> SVG (без внешнего <svg> и без <defs>). Рисуются
заново под текст этого ролика (R-0019): ни один кадр не взят из «13», «14»,
«15», «16 ноября» и ни одно тело функции не повторяет порцию 1. Люди —
только `figura()` из `lok_obshchee`, руки — только `_ruka()` от плеча
(R-0051). Источник: `zadaniya/porciya2.md`.

Чему научила первая порция и что держится здесь:
· веник, ухват, кочерга держатся ЗА ЧЕРЕНОК концом рукава, палка ≤ 340 px;
· главный предмет 420-700 px и с деталями, читается со стоп-кадра (R-0047);
· нижняя треть кадра занята настоящими вещами, а не пустым полом;
· в группах рост СТРОГО ЧЕРЕЗ ОДНОГО крупный/мелкий, шаг рваный, треть
  фигур в профиль и со спины, наклон ±15°;
· плотность набирается ВЕЩАМИ, полупрозрачными пятнами — нельзя.
"""
import math, random
from baza import *
import anim as A
from lok_obshchee import *
# ЗВЁЗДОЧКА НЕ ТАЩИТ ИМЕНА С ПОДЧЁРКИВАНИЯ — общие кирпичики берём явно
from lok_obshchee import (
    _asfalt,
    _bulyzhnik,
    _derevnya_ryad,
    _dvorovaya_utvar,
    _gorodskoy_hlam,
    _inej,
    _kadushki_i_grabli,
    _koleya,
    _kot_zhivoy,
    _kryl_co,
    _kucha_listev,
    _lavka_krupno,
    _listya,
    _luzha,
    _moneta_krupno,
    _plecho,
    _podorozhnik,
    _polenica,
    _polka_s_utvaryu,
    _predmet_naruzhu,
    _ruka,
    _ruka_ekr,
    _ruka_so_sgibom,
    _sledy,
    _stena_ambara,
    _stena_gornicy,
    _stennoe_hozyaystvo,
    _stolb_pered,
    _trava,
    _tryumo,
    _venik,
    _venik_v_ruke,
    _vetka_pered,
    _vid_za_proemom,
    _yaschiki,
    _zabor_dosok,
    _zemlya,
    _zemlya_faktura)


# ── ПОМОЩНИКИ ЭТОЙ ПОРЦИИ (локальные, в baza и lok_obshchee их нет) ────────

def _varezhka(x, y, h_=800.0, t=0.0, ph=.0, col="#e8d8c0", kant="#b89a74"):
    """ВАРЕЖКА НА КОНЦЕ РУКАВА — ХВАТ ЧИТАЕТСЯ ПЕРЕКРЫТИЕМ.

    Разбор принятого ролика 17-11 глазами: там рука — ОДИН сегмент рукава,
    на конце светлый овал-варежка, и предмет лежит ПОД варежкой внахлёст.
    Поэтому видно, что предмет держат. В первой порции «Дня Ионы» рукав
    обрывался в пустоту во всех 17 осмотренных кадрах, и предмет примыкал
    встык или висел с зазором («веник висит в воздухе без руки»).
    Пальцев не рисуем — их нет и в образце: овал, большой палец отдельной
    долькой, тёмный кант по нижней кромке, светлый блик сверху.

    Ставится ПОСЛЕ предмета: овал ложится поверх черенка.

    ПРАВИЛО (решение по осмотру порции 2): варежка ставится ТОЛЬКО там, где
    она перекрывает предмет не меньше чем на ЧЕТВЕРТЬ своей площади. Где
    перекрытия нет — варежку не ставим вовсе, рукав остаётся без кисти, как
    в первой порции: иначе она читается отдельным светлым пятном и обещает
    хват, которого нет. Проверяется числом: `varezhki_proverka.py`.
    """
    s_ = max(.42, h_ / 800.0)
    rx_, ry_ = 34 * s_, 27 * s_
    kol = 3 * s_ * A.w(t, 1.7, ph)
    return (f'<g transform="translate({kol:.1f},0)">'
            f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx_:.0f}" ry="{ry_:.0f}"'
            f' fill="{col}" stroke="{K}" stroke-width="{max(2, 4 * s_):.1f}"/>'
            f'<ellipse cx="{x-rx_*.62:.0f}" cy="{y+ry_*.30:.0f}" rx="{rx_*.34:.0f}"'
            f' ry="{ry_*.46:.0f}" fill="{col}" stroke="{K}"'
            f' stroke-width="{max(2, 3 * s_):.1f}"/>'
            f'<path d="M{x-rx_*.84:.0f},{y+ry_*.42:.0f}'
            f' q{rx_*.84:.0f},{ry_*.68:.0f} {rx_*1.68:.0f},{-ry_*.16:.0f}"'
            f' fill="none" stroke="{kant}" stroke-width="{max(2, 5 * s_):.1f}"'
            f' opacity=".8"/>'
            f'<path d="M{x-rx_*.56:.0f},{y-ry_*.44:.0f}'
            f' q{rx_*.46:.0f},{-ry_*.34:.0f} {rx_*1.02:.0f},{-ry_*.06:.0f}"'
            f' fill="none" stroke="#fff4e2" stroke-width="{max(2, 4 * s_):.1f}"'
            f' opacity=".55"/></g>')


def _konus_sveta(x, y, w_, h_, ug=0.0, op=.40, col="#ffd98a"):
    """Световой конус от источника на стену или пол: у принятого 17-11 он
    есть в каждом кадре, и именно от него кадр читается ОСВЕЩЁННЫМ, а не
    просто светлым. Прозрачность держим выше .35 — мутных пятен не плодим."""
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'<path d="M{x-w_*.14:.0f},{y:.0f} L{x+w_*.14:.0f},{y:.0f}'
            f' L{x+w_*.5:.0f},{y+h_:.0f} L{x-w_*.5:.0f},{y+h_:.0f} Z"'
            f' fill="{col}" opacity="{op:.2f}"/>'
            f'<path d="M{x-w_*.07:.0f},{y:.0f} L{x+w_*.07:.0f},{y:.0f}'
            f' L{x+w_*.26:.0f},{y+h_:.0f} L{x-w_*.26:.0f},{y+h_:.0f} Z"'
            f' fill="#fff2d2" opacity="{op*.7:.2f}"/></g>')


def _pol_shvy(y0, y1, seed=3, n=5, col="#3f3326"):
    """Фактура пола и земли вблизи: швы половиц сходятся к точке схода,
    поперечные трещины, пара сучков. Разбор 17-11: у них деталь у земли
    втрое густее, чем в небе, у нас была ровная заливка."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n + 1):
        p = i / float(n)
        x0 = 960 + (p - .5) * 1120
        x1 = 960 + (p - .5) * 2600
        s += (f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}"'
              f' stroke="{col}" stroke-width="7" opacity=".55"/>')
    for i in range(4):
        yy = y0 + (y1 - y0) * (.22 + i * .22)
        s += (f'<path d="M-20,{yy:.0f} Q480,{yy-14:.0f} 980,{yy+8:.0f}'
              f' Q1480,{yy+20:.0f} 1940,{yy-6:.0f}" fill="none" stroke="{col}"'
              f' stroke-width="5" opacity=".42"/>')
    for i in range(5):
        sx = rnd.uniform(80, W - 80)
        sy = rnd.uniform(y0 + 20, y1 - 20)
        s += (f'<ellipse cx="{sx:.0f}" cy="{sy:.0f}" rx="{rnd.uniform(16, 30):.0f}"'
              f' ry="{rnd.uniform(7, 13):.0f}" fill="{col}" opacity=".5"/>')
    return s


def _kafel(x, y, w_, h_, t, seed=3, col="#d4dcdc", shov="#a8b4b4"):
    """Кафельная стена кухни: плитка в перевязку, затирка, пара плиток с
    рисунком и мокрый блик по нижнему ряду у мойки."""
    rnd = random.Random(seed)
    s = ""
    kh = 74
    for r in range(int(h_ / kh) + 1):
        yy = y + r * kh
        off = 0 if r % 2 == 0 else 86
        for c in range(int(w_ / 172) + 2):
            xx = x - 86 + off + c * 172
            if xx + 166 < x or xx > x + w_:
                continue
            tn = col if rnd.random() < .82 else "#c2cdcd"
            s += (f'<rect x="{xx:.0f}" y="{yy:.0f}" width="166" height="{kh-7}"'
                  f' rx="6" fill="{tn}" stroke="{shov}" stroke-width="4"/>')
            if rnd.random() < .16:
                s += (f'<path d="M{xx+40:.0f},{yy+44:.0f} q{42:.0f},{-30:.0f}'
                      f' {84:.0f},0" fill="none" stroke="#8fa3a8"'
                      f' stroke-width="6" opacity=".7"/>')
    s += (f'<rect x="{x:.0f}" y="{y+h_-14:.0f}" width="{w_:.0f}" height="14"'
          f' fill="#8f9c9c" opacity=".7"/>')
    return s


def _tarelka(cx, cy, r, t, ph=.0, pena=True, ug=0.0, col="#eef2f4"):
    """Тарелка, которую видно со стоп-кадра: борт, кольцо дна, глазурный
    блик дугой, скол на борту и пена по краю."""
    bl = .4 + .6 * abs(A.w(t, 2.2, ph))
    s = (f'<g transform="rotate({ug:.1f} {cx:.0f} {cy:.0f})">'
         f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r:.0f}" ry="{r*.86:.0f}"'
         f' fill="{col}" {o(6)}/>'
         f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r*.80:.0f}" ry="{r*.68:.0f}"'
         f' fill="none" stroke="#b9c6cc" stroke-width="7"/>'
         f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r*.46:.0f}" ry="{r*.39:.0f}"'
         f' fill="#e2e9ec" {o(4)}/>'
         f'<path d="M{cx-r*.72:.0f},{cy-r*.30:.0f} Q{cx-r*.10:.0f},{cy-r*.78:.0f}'
         f' {cx+r*.56:.0f},{cy-r*.44:.0f}" fill="none" stroke="#ffffff"'
         f' stroke-width="{max(5, r*.11):.0f}" opacity="{.32+bl*.40:.2f}"/>'
         f'<path d="M{cx+r*.86:.0f},{cy-r*.14:.0f} l{r*.12:.0f},{r*.08:.0f}'
         f' l{-r*.12:.0f},{r*.10:.0f} Z" fill="#c6d0d4" {o(3)}/>')
    if pena:
        rnd = random.Random(int(cx) + int(r))
        for i in range(9):
            a = math.radians(i * 40 + 12 * A.w(t, 2.8, ph + i * .1))
            px = cx + r * .93 * math.cos(a)
            py = cy + r * .80 * math.sin(a)
            rr = rnd.uniform(13, 27)
            s += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr:.0f}" fill="#f6fbff"'
                  f' stroke="#c8d8e2" stroke-width="3"/>')
    return s + "</g>"


def _stopka_tarelok(x, y, n, t, seed=5, shir=190):
    """Гора тарелок: каждая своя, с бортом и щербинкой, стопка чуть ведёт
    в сторону — ровный столбик читается трубой."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        dx = rnd.uniform(-13, 13) + 3 * A.w(t, 3.4, i * .2)
        yy = y - i * 23
        w2 = shir * rnd.uniform(.88, 1.06)
        s += (f'<ellipse cx="{x+dx:.0f}" cy="{yy:.0f}" rx="{w2*.5:.0f}" ry="{w2*.15:.0f}"'
              f' fill="#e7edf0" {o(4)}/>'
              f'<ellipse cx="{x+dx:.0f}" cy="{yy-5:.0f}" rx="{w2*.44:.0f}"'
              f' ry="{w2*.11:.0f}" fill="#fbfdfe" opacity=".8"/>')
    return s


def _pena_gorka(cx, cy, rx, t, seed=7, n=16, osadka=.0):
    """Мыльная пена кучей: пузыри разного калибра, часть с радужным бликом.
    osadka 0..1 — пена оседает, горка становится ниже."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        a = rnd.uniform(0, 6.28)
        rr = rnd.uniform(.2, 1.0)
        px = cx + math.cos(a) * rx * rr
        py = cy - abs(math.sin(a)) * rx * .34 * rr * (1 - .55 * osadka)
        b = rnd.uniform(16, 44) * (1 - .25 * osadka)
        s += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{b:.0f}" fill="#f4fafe"'
              f' stroke="#cadbe6" stroke-width="3" opacity=".92"/>')
        if i % 3 == 0:
            s += (f'<circle cx="{px-b*.3:.0f}" cy="{py-b*.3:.0f}" r="{b*.26:.0f}"'
                  f' fill="#ffffff" opacity="{.5+.4*abs(A.w(t,2.0,i*.2)):.2f}"/>')
    return s


def _moyka(x, y, w_, t, seed=5, kran=True, osadka=.0):
    """Мойка с тумбой: столешница, врезанная чаша, смеситель с каплей,
    дверцы тумбы, пена в чаше, бутылка и губка на борту."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="40" rx="10"'
         f' fill="#b9b2a4" {o(6)}/>'
         f'<rect x="{x+6:.0f}" y="{y+40:.0f}" width="{w_-12:.0f}" height="{H-y-40:.0f}"'
         f' fill="#7e6c56" {o(5)}/>')
    for i in range(3):
        dx = x + 26 + i * (w_ - 70) / 3.0
        s += (f'<rect x="{dx:.0f}" y="{y+66:.0f}" width="{(w_-120)/3.2:.0f}"'
              f' height="260" rx="8" fill="#8f7b61" {o(4)}/>'
              f'<rect x="{dx+20:.0f}" y="{y+96:.0f}" width="{(w_-120)/4.4:.0f}"'
              f' height="200" rx="6" fill="#9c886c" opacity=".75"/>'
              f'<circle cx="{dx+(w_-120)/6.6:.0f}" cy="{y+300:.0f}" r="12"'
              f' fill="{ZHELEZ}" {o(3)}/>')
    cx = x + w_ * .42
    s += (f'<rect x="{cx-230:.0f}" y="{y+6:.0f}" width="460" height="30" rx="12"'
          f' fill="#6f767c" {o(5)}/>'
          f'<path d="M{cx-212:.0f},{y+28:.0f} L{cx-182:.0f},{y+176:.0f}'
          f' L{cx+182:.0f},{y+176:.0f} L{cx+212:.0f},{y+28:.0f} Z"'
          f' fill="#5a6168" {o(5)}/>'
          f'<ellipse cx="{cx:.0f}" cy="{y+172:.0f}" rx="56" ry="16" fill="#3e4348" {o(3)}/>')
    if kran:
        kx = x + w_ * .14
        s += (f'<rect x="{kx-14:.0f}" y="{y-150:.0f}" width="28" height="160" rx="12"'
              f' fill="#9aa3aa" {o(4)}/>'
              f'<path d="M{kx:.0f},{y-150:.0f} q0,{-64:.0f} {92:.0f},{-60:.0f}'
              f' q{36:.0f},{4:.0f} {32:.0f},{48:.0f}" fill="none" stroke="#9aa3aa"'
              f' stroke-width="26" stroke-linecap="round"/>'
              f'<rect x="{kx-54:.0f}" y="{y-176:.0f}" width="44" height="18" rx="8"'
              f' fill="#7d868d" {o(3)}/>')
        kap = ((t * .8) % 1.0)
        s += (f'<ellipse cx="{kx+124:.0f}" cy="{y-96+kap*86:.0f}" rx="7"'
              f' ry="{10+6*kap:.0f}" fill="#d6e8f4" opacity="{1-kap:.2f}"/>')
    s += _pena_gorka(cx, y + 150, 190, t, seed + 3, 18, osadka)
    s += (f'<rect x="{x+w_-150:.0f}" y="{y-96:.0f}" width="62" height="100" rx="14"'
          f' fill="#4e7a52" {o(4)}/>'
          f'<rect x="{x+w_-144:.0f}" y="{y-78:.0f}" width="48" height="44" rx="6"'
          f' fill="#e9f0d8" opacity=".85"/>'
          f'<rect x="{x+w_-74:.0f}" y="{y-40:.0f}" width="66" height="44" rx="12"'
          f' fill="#e4c85a" {o(4)}/>')
    return s


def _chaynik(x, y, s_=1.0, t=0.0, parok=False):
    """Чайник: тулово, носик, дуга-ручка, свисток и блик на боку."""
    s = (ten(x, y + 8 * s_, 74 * s_, 14 * s_, .45)
         + f'<path d="M{x-72*s_:.0f},{y:.0f} q{-16*s_:.0f},{-82*s_:.0f} {18*s_:.0f},{-104*s_:.0f}'
           f' q{54*s_:.0f},{-18*s_:.0f} {108*s_:.0f},0 q{34*s_:.0f},{22*s_:.0f}'
           f' {18*s_:.0f},{104*s_:.0f} Z" fill="url(#zhel)" {o(6)}/>'
         + f'<path d="M{x+58*s_:.0f},{y-82*s_:.0f} l{46*s_:.0f},{-38*s_:.0f}'
           f' l{14*s_:.0f},{20*s_:.0f} l{-44*s_:.0f},{36*s_:.0f} Z"'
           f' fill="url(#zhel)" {o(5)}/>'
         + f'<path d="M{x-40*s_:.0f},{y-104*s_:.0f} q{40*s_:.0f},{-58*s_:.0f}'
           f' {80*s_:.0f},0" fill="none" stroke="{ZHELEZ}" stroke-width="{13*s_:.0f}"/>'
         + f'<ellipse cx="{x:.0f}" cy="{y-104*s_:.0f}" rx="{44*s_:.0f}" ry="{13*s_:.0f}"'
           f' fill="#6f767c" {o(4)}/>'
         + f'<path d="M{x-44*s_:.0f},{y-56*s_:.0f} q{10*s_:.0f},{-28*s_:.0f}'
           f' {4*s_:.0f},{-44*s_:.0f}" fill="none" stroke="#fff0c8"'
           f' stroke-width="{9*s_:.0f}" opacity=".5"/>')
    return s


def _kastryulya(x, y, s_=1.0, t=0.0, kryshka=True):
    """Кастрюля: бок с обручем, две ушные ручки, крышка с пуговкой."""
    s = (ten(x, y + 6 * s_, 68 * s_, 12 * s_, .4)
         + f'<path d="M{x-62*s_:.0f},{y-104*s_:.0f} L{x+62*s_:.0f},{y-104*s_:.0f}'
           f' L{x+54*s_:.0f},{y:.0f} L{x-54*s_:.0f},{y:.0f} Z" fill="#b6bcc2" {o(6)}/>'
         + f'<rect x="{x-62*s_:.0f}" y="{y-66*s_:.0f}" width="{124*s_:.0f}"'
           f' height="{12*s_:.0f}" fill="#8b9299" opacity=".8"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*62*s_:.0f},{y-96*s_:.0f} q{i*30*s_:.0f},{4*s_:.0f}'
              f' {i*26*s_:.0f},{26*s_:.0f}" fill="none" stroke="{CHUGUN}"'
              f' stroke-width="{11*s_:.0f}"/>')
    if kryshka:
        s += (f'<ellipse cx="{x:.0f}" cy="{y-104*s_:.0f}" rx="{66*s_:.0f}"'
              f' ry="{15*s_:.0f}" fill="#cfd5da" {o(5)}/>'
              f'<circle cx="{x:.0f}" cy="{y-118*s_:.0f}" r="{11*s_:.0f}"'
              f' fill="{CHUGUN}" {o(3)}/>')
    return s


def _kruzhka(x, y, s_=1.0, ug=0.0, col="#e8eef0", uho=1):
    """Кружка: тулово, ручка кольцом, пояс рисунка, блик."""
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'{ten(x, y + 6 * s_, 34 * s_, 9 * s_, .4)}'
            f'<path d="M{x-34*s_:.0f},{y-78*s_:.0f} L{x+34*s_:.0f},{y-78*s_:.0f}'
            f' L{x+28*s_:.0f},{y:.0f} L{x-28*s_:.0f},{y:.0f} Z" fill="{col}" {o(5)}/>'
            f'<path d="M{x+uho*34*s_:.0f},{y-62*s_:.0f} q{uho*42*s_:.0f},{10*s_:.0f}'
            f' {uho*2*s_:.0f},{44*s_:.0f}" fill="none" stroke="{col}"'
            f' stroke-width="{11*s_:.0f}"/>'
            f'<rect x="{x-32*s_:.0f}" y="{y-54*s_:.0f}" width="{64*s_:.0f}"'
            f' height="{12*s_:.0f}" fill="{TKAN2}" opacity=".7"/>'
            f'<ellipse cx="{x:.0f}" cy="{y-78*s_:.0f}" rx="{34*s_:.0f}" ry="{9*s_:.0f}"'
            f' fill="#cfd8dc" {o(4)}/></g>')


def _banka_krupy(x, y, s_=1.0, col="#d8c08a"):
    """Банка крупы: стекло, крупа до плеча, жестяная крышка, бумажный ярлык
    с волнистой строкой (своих букв в декорации не рисуем)."""
    h2, w2 = 128 * s_, 84 * s_
    return (f'{ten(x, y + 6 * s_, w2 * .5, 10 * s_, .4)}'
            f'<rect x="{x-w2/2:.0f}" y="{y-h2:.0f}" width="{w2:.0f}" height="{h2:.0f}"'
            f' rx="10" fill="url(#stekl)" opacity=".9" {o(5)}/>'
            f'<rect x="{x-w2/2+7:.0f}" y="{y-h2*.62:.0f}" width="{w2-14:.0f}"'
            f' height="{h2*.58:.0f}" rx="7" fill="{col}"/>'
            f'<rect x="{x-w2/2-5:.0f}" y="{y-h2-16:.0f}" width="{w2+10:.0f}"'
            f' height="22" rx="8" fill="{ZHELEZ}" {o(4)}/>'
            f'<rect x="{x-w2*.32:.0f}" y="{y-h2*.46:.0f}" width="{w2*.64:.0f}"'
            f' height="{h2*.26:.0f}" rx="5" fill="#f2ead6" {o(3)}/>'
            f'<path d="M{x-w2*.24:.0f},{y-h2*.34:.0f} q{w2*.12:.0f},{-9:.0f}'
            f' {w2*.24:.0f},0 q{w2*.12:.0f},{9:.0f} {w2*.24:.0f},0" fill="none"'
            f' stroke="#9a8a68" stroke-width="4"/>')


def _polotence(x, y, h_, t, ph=.0, col="#e3ddc6", kryuk=True):
    """Полотенце на крючке: складки, кант по низу, слабое качание."""
    kach = 2.2 * A.w(t, 3.0, ph)
    s = ""
    if kryuk:
        s += (f'<path d="M{x:.0f},{y-26:.0f} q{14:.0f},{-20:.0f} {28:.0f},{-4:.0f}"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="9"/>')
    s += (f'<g transform="rotate({kach:.1f} {x+14:.0f} {y:.0f})">'
          f'<path d="M{x-6:.0f},{y:.0f} L{x+56:.0f},{y:.0f} L{x+66:.0f},{y+h_:.0f}'
          f' L{x-18:.0f},{y+h_:.0f} Z" fill="{col}" {o(5)}/>')
    for i in range(3):
        s += (f'<line x1="{x+6+i*18:.0f}" y1="{y+10:.0f}" x2="{x+2+i*20:.0f}"'
              f' y2="{y+h_-12:.0f}" stroke="#c9c1a6" stroke-width="5" opacity=".8"/>')
    s += (f'<rect x="{x-16:.0f}" y="{y+h_-28:.0f}" width="82" height="16"'
          f' fill="{TKAN}" opacity=".75"/></g>')
    return s


def _tabyret(x, y, t, h_=150, w_=160):
    """Табурет: толстое сиденье, четыре ножки с проножкой."""
    s = (f'{ten(x, y + 6, w_ * .54, 14, .45)}'
         f'<rect x="{x-w_/2:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="26" rx="9"'
         f' fill="url(#dosk)" {o(6)}/>')
    for i in (-1, 1):
        s += (f'<rect x="{x+i*(w_*.36)-13:.0f}" y="{y-h_+26:.0f}" width="26"'
              f' height="{h_-26:.0f}" rx="8" fill="#4a3522" {o(4)}/>'
              f'<rect x="{x+i*(w_*.22)-11:.0f}" y="{y-h_+30:.0f}" width="22"'
              f' height="{h_-32:.0f}" rx="7" fill="#3f2d1d" {o(3)}/>')
    s += (f'<rect x="{x-w_*.34:.0f}" y="{y-h_*.42:.0f}" width="{w_*.68:.0f}"'
          f' height="16" rx="7" fill="#4a3522" {o(3)}/>')
    return s


def _ugol_pechnoy_utvari(x, y, t, seed=3):
    """Угол у печи: кочерга, ухват и совок стоят в железном ведре-держалке,
    черенки короткие (≤340 px), на стене скоба с рукавицей."""
    s = (f'<path d="M{x-62:.0f},{y:.0f} L{x+62:.0f},{y:.0f} L{x+50:.0f},{y-108:.0f}'
         f' L{x-50:.0f},{y-108:.0f} Z" fill="#59606a" {o(5)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-108:.0f}" rx="50" ry="14" fill="#3d434b" {o(4)}/>')
    # кочерга
    k1 = 1.6 * A.w(t, 2.6, .1)
    s += (f'<g transform="rotate({k1:.1f} {x-20:.0f} {y-60:.0f})">'
          f'<line x1="{x-20:.0f}" y1="{y-60:.0f}" x2="{x-56:.0f}" y2="{y-392:.0f}"'
          f' stroke="{CHUGUN}" stroke-width="15" stroke-linecap="round"/>'
          f'<path d="M{x-20:.0f},{y-60:.0f} q{-30:.0f},{18:.0f} {-58:.0f},{10:.0f}"'
          f' fill="none" stroke="{CHUGUN}" stroke-width="15"/>'
          f'<circle cx="{x-58:.0f}" cy="{y-396:.0f}" r="13" fill="none"'
          f' stroke="{CHUGUN}" stroke-width="8"/></g>')
    # ухват
    k2 = 1.9 * A.w(t, 3.1, .5)
    s += (f'<g transform="rotate({k2:.1f} {x+6:.0f} {y-60:.0f})">'
          f'<line x1="{x+6:.0f}" y1="{y-60:.0f}" x2="{x+30:.0f}" y2="{y-378:.0f}"'
          f' stroke="url(#derev)" stroke-width="17" stroke-linecap="round"/>'
          f'<path d="M{x+14:.0f},{y-330:.0f} q{-36:.0f},{-54:.0f} {4:.0f},{-74:.0f}'
          f' q{44:.0f},{18:.0f} {40:.0f},{74:.0f}" fill="none" stroke="{ZHELEZ}"'
          f' stroke-width="14"/></g>')
    # совок
    s += (f'<g transform="rotate({-4 + 1.4 * A.w(t, 2.2, .8):.1f} {x+44:.0f} {y-70:.0f})">'
          f'<line x1="{x+44:.0f}" y1="{y-70:.0f}" x2="{x+78:.0f}" y2="{y-300:.0f}"'
          f' stroke="url(#derev)" stroke-width="14" stroke-linecap="round"/>'
          f'<path d="M{x+30:.0f},{y-66:.0f} L{x+96:.0f},{y-54:.0f} L{x+88:.0f},{y+4:.0f}'
          f' L{x+22:.0f},{y-8:.0f} Z" fill="#6e757c" {o(5)}/></g>')
    # скоба с рукавицей на стене
    s += (f'<rect x="{x+128:.0f}" y="{y-382:.0f}" width="34" height="18" rx="7"'
          f' fill="{ZHELEZ}" {o(3)}/>'
          f'<path d="M{x+136:.0f},{y-364:.0f} q{-22:.0f},{56:.0f} {4:.0f},{96:.0f}'
          f' q{34:.0f},{14:.0f} {44:.0f},{-18:.0f} q{10:.0f},{-54:.0f} {-10:.0f},{-78:.0f} Z"'
          f' fill="#8c6a4a" {o(4)}/>'
          f'<path d="M{x+178:.0f},{y-320:.0f} q{26:.0f},{12:.0f} {16:.0f},{40:.0f}"'
          f' fill="none" stroke="#8c6a4a" stroke-width="16"/>')
    return s


def _kreslo(x, y, w_, t, h_=430, col="#6c5a4a"):
    """Мягкое кресло: спинка валиком, два подлокотника, подушка на сиденье,
    короткие ножки и тень под ними."""
    s = (f'{ten(x, y + 8, w_ * .52, 20, .5)}'
         f'<path d="M{x-w_/2:.0f},{y-h_*.42:.0f} q0,{-h_*.62:.0f} {w_*.5:.0f},{-h_*.58:.0f}'
         f' q{w_*.5:.0f},{-h_*.04:.0f} {w_*.5:.0f},{h_*.58:.0f} Z"'
         f' fill="{col}" {o(7)}/>'
         f'<rect x="{x-w_/2:.0f}" y="{y-h_*.46:.0f}" width="{w_:.0f}"'
         f' height="{h_*.30:.0f}" rx="22" fill="#7d6a58" {o(6)}/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*w_*.5:.0f},{y-h_*.46:.0f} q{i*w_*.10:.0f},{-h_*.22:.0f}'
              f' {-i*w_*.02:.0f},{-h_*.30:.0f} q{-i*w_*.14:.0f},{-h_*.04:.0f}'
              f' {-i*w_*.16:.0f},{h_*.14:.0f} Z" fill="#7d6a58" {o(5)}/>'
              f'<rect x="{x+i*w_*.42-26:.0f}" y="{y-h_*.14:.0f}" width="34"'
              f' height="{h_*.16:.0f}" rx="10" fill="#4a3c30" {o(4)}/>')
    s += (f'<path d="M{x-w_*.40:.0f},{y-h_*.30:.0f} q{w_*.40:.0f},{-h_*.14:.0f}'
          f' {w_*.80:.0f},0 q{-w_*.06:.0f},{h_*.12:.0f} {-w_*.80:.0f},0 Z"'
          f' fill="#8c7260" {o(5)}/>')
    for i in range(4):
        s += (f'<line x1="{x-w_*.30+i*w_*.20:.0f}" y1="{y-h_*.86:.0f}"'
              f' x2="{x-w_*.30+i*w_*.20:.0f}" y2="{y-h_*.48:.0f}" stroke="#5a4a3c"'
              f' stroke-width="7" opacity=".7"/>')
    return s


def _stolik(x, y, w_, t, h_=190, kruzhev=False):
    """Журнальный столик: столешница, точёные ножки, кружевная салфетка."""
    s = (f'{ten(x, y + 6, w_ * .5, 16, .45)}'
         f'<rect x="{x-w_/2:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="24" rx="10"'
         f' fill="url(#derev)" {o(6)}/>')
    for i in (-1, 1):
        s += (f'<rect x="{x+i*w_*.38-12:.0f}" y="{y-h_+24:.0f}" width="24"'
              f' height="{h_-24:.0f}" rx="9" fill="#5b4428" {o(4)}/>'
              f'<ellipse cx="{x+i*w_*.38:.0f}" cy="{y-h_*.52:.0f}" rx="22" ry="14"'
              f' fill="#6a5030" {o(3)}/>')
    if kruzhev:
        s += (f'<path d="M{x-w_*.42:.0f},{y-h_:.0f} h{w_*.84:.0f} l-10,26 h{-w_*.84+20:.0f} Z"'
              f' fill="#f4efe0" {o(4)}/>')
        for i in range(9):
            s += (f'<circle cx="{x-w_*.40+i*w_*.10:.0f}" cy="{y-h_+30:.0f}" r="11"'
                  f' fill="none" stroke="#e2d8bf" stroke-width="4"/>')
    return s


def _pirog(x, y, s_=1.0, t=0.0, nadrez=True):
    """Пирог на блюде: корж, защип по краю, косые надрезы, блюдо с каймой."""
    s = (f'{ten(x, y + 10 * s_, 118 * s_, 16 * s_, .45)}'
         f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{124*s_:.0f}" ry="{30*s_:.0f}"'
         f' fill="#eae2cf" {o(5)}/>'
         f'<path d="M{x-104*s_:.0f},{y-6*s_:.0f} q{14*s_:.0f},{-66*s_:.0f}'
         f' {104*s_:.0f},{-64*s_:.0f} q{90*s_:.0f},{-2*s_:.0f} {104*s_:.0f},{64*s_:.0f} Z"'
         f' fill="url(#med)" {o(6)}/>')
    if nadrez:
        for i in range(4):
            s += (f'<path d="M{x-66*s_+i*44*s_:.0f},{y-18*s_:.0f}'
                  f' l{26*s_:.0f},{-34*s_:.0f}" fill="none" stroke="#8a5a22"'
                  f' stroke-width="{7*s_:.0f}" opacity=".8"/>')
    for i in range(7):
        s += (f'<circle cx="{x-96*s_+i*32*s_:.0f}" cy="{y-10*s_:.0f}" r="{11*s_:.0f}"'
              f' fill="#c99a52" {o(2)}/>')
    s += (f'<path d="M{x-70*s_:.0f},{y-54*s_:.0f} q{30*s_:.0f},{-14*s_:.0f}'
          f' {62*s_:.0f},{-6*s_:.0f}" fill="none" stroke="#fff0c8"'
          f' stroke-width="{8*s_:.0f}" opacity="{.3+.3*abs(A.w(t,2.6)):.2f}"/>')
    return s


def _vaza_s_yablokami(x, y, s_=1.0, t=0.0, seed=9, n=6):
    """Ваза-фруктовница на ножке и яблоки горкой: у каждого черешок и блик."""
    rnd = random.Random(seed)
    s = (f'{ten(x, y + 8 * s_, 80 * s_, 13 * s_, .4)}'
         f'<path d="M{x-28*s_:.0f},{y:.0f} L{x+28*s_:.0f},{y:.0f}'
         f' L{x+16*s_:.0f},{y-44*s_:.0f} L{x-16*s_:.0f},{y-44*s_:.0f} Z"'
         f' fill="url(#stekl)" opacity=".9" {o(4)}/>'
         f'<path d="M{x-92*s_:.0f},{y-48*s_:.0f} q{92*s_:.0f},{58*s_:.0f}'
         f' {184*s_:.0f},0 Z" fill="url(#stekl)" opacity=".85" {o(5)}/>')
    for i in range(n):
        ax = x + rnd.uniform(-72, 72) * s_
        ay = y - 58 * s_ - abs(rnd.uniform(0, 42)) * s_
        rr = rnd.uniform(26, 34) * s_
        col = "#b8352c" if i % 2 else "#c9772c"
        s += (f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="{rr:.0f}" fill="{col}" {o(4)}/>'
              f'<path d="M{ax+2*s_:.0f},{ay-rr:.0f} q{6*s_:.0f},{-16*s_:.0f}'
              f' {18*s_:.0f},{-18*s_:.0f}" fill="none" stroke="#4e3418"'
              f' stroke-width="{5*s_:.0f}"/>'
              f'<circle cx="{ax-rr*.32:.0f}" cy="{ay-rr*.34:.0f}" r="{rr*.22:.0f}"'
              f' fill="#ffe6c8" opacity=".55"/>')
    return s


def _servant_hrustal(x, y, w_, h_, t, seed=3):
    """Сервант шестидесятых: цоколь, застеклённая верхняя часть, рюмки и
    вазы за стеклом, нижние глухие дверцы с латунными ручками."""
    rnd = random.Random(seed)
    s = (f'{ten(x + w_ / 2, y + 10, w_ * .46, 18, .45)}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10"'
         f' fill="url(#derev)" {o(7)}/>'
         f'<rect x="{x-14:.0f}" y="{y-h_-22:.0f}" width="{w_+28:.0f}" height="26" rx="9"'
         f' fill="#6a5030" {o(5)}/>')
    st_y = y - h_ + 40
    st_h = h_ * .46
    s += (f'<rect x="{x+20:.0f}" y="{st_y:.0f}" width="{w_-40:.0f}" height="{st_h:.0f}"'
          f' rx="8" fill="url(#stekl)" opacity=".7" {o(5)}/>')
    for p in range(2):
        py = st_y + st_h * (.52 + .44 * p)
        s += (f'<rect x="{x+22:.0f}" y="{py:.0f}" width="{w_-44:.0f}" height="12"'
              f' fill="#5b4428" opacity=".85"/>')
        for i in range(6):
            gx = x + 54 + i * (w_ - 110) / 5.0
            hh = rnd.uniform(44, 76)
            bl = .35 + .4 * abs(A.w(t, 2.4 + i * .3, i * .2))
            s += (f'<path d="M{gx-18:.0f},{py:.0f} L{gx+18:.0f},{py:.0f}'
                  f' L{gx+12:.0f},{py-hh*.52:.0f} L{gx+16:.0f},{py-hh:.0f}'
                  f' L{gx-16:.0f},{py-hh:.0f} L{gx-12:.0f},{py-hh*.52:.0f} Z"'
                  f' fill="#dbeaf4" opacity=".9" {o(3)}/>'
                  f'<circle cx="{gx-6:.0f}" cy="{py-hh*.8:.0f}" r="5"'
                  f' fill="#ffffff" opacity="{bl:.2f}"/>')
    s += (f'<line x1="{x+w_/2:.0f}" y1="{st_y:.0f}" x2="{x+w_/2:.0f}"'
          f' y2="{st_y+st_h:.0f}" stroke="#4a3522" stroke-width="10"/>')
    for i in (0, 1):
        dx = x + 24 + i * (w_ - 48) / 2.0
        s += (f'<rect x="{dx:.0f}" y="{y-h_*.44:.0f}" width="{(w_-66)/2:.0f}"'
              f' height="{h_*.36:.0f}" rx="8" fill="#8a6a44" {o(5)}/>'
              f'<rect x="{dx+18:.0f}" y="{y-h_*.40:.0f}" width="{(w_-66)/2-36:.0f}"'
              f' height="{h_*.28:.0f}" rx="6" fill="#7b5c38" opacity=".8"/>'
              f'<rect x="{dx+(w_-66)/4-22:.0f}" y="{y-h_*.26:.0f}" width="44"'
              f' height="14" rx="7" fill="url(#zol)" {o(3)}/>')
    return s


def _venskiy_stul(x, y, h_, t, ug=0.0, sidit=False):
    """Венский стул: круглое сиденье, гнутая спинка с кольцом, четыре
    расходящиеся ножки и проножка."""
    sy = y - h_ * .52
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'{ten(x, y + 6, h_ * .22, 13, .45)}'
         f'<ellipse cx="{x:.0f}" cy="{sy:.0f}" rx="{h_*.24:.0f}" ry="{h_*.072:.0f}"'
         f' fill="url(#derev)" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{sy-h_*.016:.0f}" rx="{h_*.20:.0f}"'
         f' ry="{h_*.052:.0f}" fill="#8a6a44" opacity=".8"/>')
    for i, dx in enumerate((-.20, -.08, .08, .20)):
        s += (f'<line x1="{x+h_*dx:.0f}" y1="{sy+h_*.03:.0f}"'
              f' x2="{x+h_*dx*1.5:.0f}" y2="{y:.0f}" stroke="#5b4428"'
              f' stroke-width="{13 if abs(dx) > .1 else 10}" stroke-linecap="round"/>')
    s += (f'<path d="M{x-h_*.26:.0f},{sy-h_*.02:.0f} q{h_*.02:.0f},{-h_*.46:.0f}'
          f' {h_*.26:.0f},{-h_*.48:.0f} q{h_*.24:.0f},{h_*.02:.0f}'
          f' {h_*.26:.0f},{h_*.48:.0f}" fill="none" stroke="#6a5030"'
          f' stroke-width="16"/>'
          f'<ellipse cx="{x:.0f}" cy="{sy-h_*.26:.0f}" rx="{h_*.13:.0f}"'
          f' ry="{h_*.14:.0f}" fill="none" stroke="#6a5030" stroke-width="12"/>'
          f'<path d="M{x-h_*.22:.0f},{y-h_*.18:.0f} q{h_*.22:.0f},{h_*.05:.0f}'
          f' {h_*.44:.0f},0" fill="none" stroke="#5b4428" stroke-width="9"/></g>')
    return s


def _supnica(x, y, s_=1.0, t=0.0):
    """Супница: пузатое тулово, две ручки, крышка с хватком, золотая кайма."""
    return (f'{ten(x, y + 8 * s_, 96 * s_, 14 * s_, .45)}'
            f'<path d="M{x-96*s_:.0f},{y-54*s_:.0f} q{18*s_:.0f},{58*s_:.0f}'
            f' {96*s_:.0f},{56*s_:.0f} q{78*s_:.0f},{2*s_:.0f} {96*s_:.0f},{-56*s_:.0f} Z"'
            f' fill="#f0ece0" {o(6)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y-56*s_:.0f}" rx="{98*s_:.0f}"'
            f' ry="{20*s_:.0f}" fill="#e4dfd0" {o(5)}/>'
            f'<path d="M{x-98*s_:.0f},{y-60*s_:.0f} q{98*s_:.0f},{-56*s_:.0f}'
            f' {196*s_:.0f},0 q{-98*s_:.0f},{26*s_:.0f} {-196*s_:.0f},0 Z"'
            f' fill="#f6f2e8" {o(5)}/>'
            f'<circle cx="{x:.0f}" cy="{y-96*s_:.0f}" r="{15*s_:.0f}" fill="url(#zol)"'
            f' {o(4)}/>'
            f'<path d="M{x-96*s_:.0f},{y-44*s_:.0f} q{-36*s_:.0f},{10*s_:.0f}'
            f' {-28*s_:.0f},{34*s_:.0f}" fill="none" stroke="#f0ece0"'
            f' stroke-width="{15*s_:.0f}"/>'
            f'<path d="M{x+96*s_:.0f},{y-44*s_:.0f} q{36*s_:.0f},{10*s_:.0f}'
            f' {28*s_:.0f},{34*s_:.0f}" fill="none" stroke="#f0ece0"'
            f' stroke-width="{15*s_:.0f}"/>'
            f'<path d="M{x-88*s_:.0f},{y-28*s_:.0f} q{88*s_:.0f},{22*s_:.0f}'
            f' {176*s_:.0f},0" fill="none" stroke="url(#zol)" stroke-width="{6*s_:.0f}"/>')


def _kover_na_stene(x, y, w_, h_, t, seed=5):
    """Ковёр на стене: кайма, медальон в середине, бахрома по низу."""
    rnd = random.Random(seed)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8"'
         f' fill="#7a2f33" {o(6)}/>'
         f'<rect x="{x+26:.0f}" y="{y+26:.0f}" width="{w_-52:.0f}" height="{h_-52:.0f}"'
         f' rx="6" fill="none" stroke="#c9a05a" stroke-width="10"/>'
         f'<path d="M{x+w_*.5:.0f},{y+h_*.22:.0f} L{x+w_*.76:.0f},{y+h_*.5:.0f}'
         f' L{x+w_*.5:.0f},{y+h_*.78:.0f} L{x+w_*.24:.0f},{y+h_*.5:.0f} Z"'
         f' fill="#9c4b40" stroke="#e0c084" stroke-width="7"/>')
    for i in range(6):
        px = x + w_ * (.18 + .13 * i)
        s += (f'<circle cx="{px:.0f}" cy="{y+h_*(.36 if i % 2 else .64):.0f}" r="18"'
              f' fill="#d8b070" opacity=".8"/>')
    for i in range(int(w_ / 26)):
        fx = x + 10 + i * 26
        s += (f'<line x1="{fx:.0f}" y1="{y+h_:.0f}" x2="{fx+2*A.w(t,4.0,i*.1):.0f}"'
              f' y2="{y+h_+24:.0f}" stroke="#d8c08a" stroke-width="5" opacity=".85"/>')
    return s


def _pismennyy_stol(x, y, w_, t, h_=250):
    """Письменный стол конторы: толстая столешница с сукном, два тумбовых
    ящика с ручками, царга и чернильный развод на сукне."""
    s = (f'{ten(x + w_ / 2, y + 10, w_ * .46, 20, .5)}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="38" rx="9"'
         f' fill="url(#derev)" {o(7)}/>'
         f'<rect x="{x+16:.0f}" y="{y-h_+8:.0f}" width="{w_-32:.0f}" height="22" rx="6"'
         f' fill="#2f4a3c" opacity=".9"/>'
         f'<ellipse cx="{x+w_*.72:.0f}" cy="{y-h_+20:.0f}" rx="56" ry="9"'
         f' fill="#1d3028" opacity=".7"/>')
    for i in (0, 1):
        bx = x + (26 if i == 0 else w_ - 250)
        s += (f'<rect x="{bx:.0f}" y="{y-h_+38:.0f}" width="224"'
              f' height="{h_-38:.0f}" rx="8" fill="#7b5c38" {o(5)}/>')
        for k in range(2):
            s += (f'<rect x="{bx+16:.0f}" y="{y-h_+58+k*86:.0f}" width="192"'
                  f' height="72" rx="6" fill="#8a6a44" {o(4)}/>'
                  f'<rect x="{bx+86:.0f}" y="{y-h_+88+k*86:.0f}" width="52"'
                  f' height="14" rx="7" fill="url(#zhel)" {o(3)}/>')
    s += (f'<rect x="{x+250:.0f}" y="{y-h_+44:.0f}" width="{w_-500:.0f}" height="18"'
          f' rx="7" fill="#6a5030" {o(4)}/>')
    return s


def _chernilnica(x, y, s_=1.0, t=0.0):
    """Чернильница: стеклянный куб с чернилами, бронзовая крышка на шарнире,
    блик на граненом боку."""
    w2, h2 = 76 * s_, 70 * s_
    return (f'{ten(x, y + 6 * s_, w2 * .56, 10 * s_, .45)}'
            f'<rect x="{x-w2/2:.0f}" y="{y-h2:.0f}" width="{w2:.0f}" height="{h2:.0f}"'
            f' rx="8" fill="url(#stekl)" opacity=".92" {o(5)}/>'
            f'<rect x="{x-w2/2+6:.0f}" y="{y-h2*.52:.0f}" width="{w2-12:.0f}"'
            f' height="{h2*.46:.0f}" rx="5" fill="#1b2434"/>'
            f'<ellipse cx="{x:.0f}" cy="{y-h2:.0f}" rx="{w2*.42:.0f}" ry="{9*s_:.0f}"'
            f' fill="#8a6a3c" {o(4)}/>'
            f'<path d="M{x-w2*.42:.0f},{y-h2-4*s_:.0f} q{w2*.42:.0f},{-26*s_:.0f}'
            f' {w2*.84:.0f},{-2*s_:.0f} l0,{10*s_:.0f} q{-w2*.42:.0f},{-14*s_:.0f}'
            f' {-w2*.84:.0f},{2*s_:.0f} Z" fill="url(#zhel)" {o(4)}/>'
            f'<line x1="{x-w2*.28:.0f}" y1="{y-h2*.86:.0f}" x2="{x-w2*.28:.0f}"'
            f' y2="{y-h2*.12:.0f}" stroke="#eaf4ff" stroke-width="{5*s_:.0f}"'
            f' opacity="{.3+.25*abs(A.w(t,2.8)):.2f}"/>')


def _pero_pisma(ex, ey, t, s_=1.0, ug=-28.0, kaplya=.0):
    """Гусиное перо: стержень, бородка с прорезями, металлический кончик и
    набухающая капля чернил на острие."""
    s = (f'<g transform="rotate({ug:.1f} {ex:.0f} {ey:.0f})">'
         f'<path d="M{ex:.0f},{ey:.0f} L{ex-16*s_:.0f},{ey-176*s_:.0f}'
         f' L{ex+6*s_:.0f},{ey-184*s_:.0f} L{ex+14*s_:.0f},{ey-8*s_:.0f} Z"'
         f' fill="#efe8da" {o(4)}/>')
    for i in range(7):
        yy = ey - 44 * s_ - i * 20 * s_
        s += (f'<line x1="{ex-12*s_+i*s_:.0f}" y1="{yy:.0f}"'
              f' x2="{ex-54*s_+i*3*s_:.0f}" y2="{yy-16*s_:.0f}" stroke="#d8cfbd"'
              f' stroke-width="{6*s_:.0f}" opacity=".9"/>'
              f'<line x1="{ex+12*s_:.0f}" y1="{yy:.0f}" x2="{ex+48*s_:.0f}"'
              f' y2="{yy-14*s_:.0f}" stroke="#e6ded0" stroke-width="{6*s_:.0f}"'
              f' opacity=".85"/>')
    s += (f'<path d="M{ex-8*s_:.0f},{ey-16*s_:.0f} L{ex+10*s_:.0f},{ey-18*s_:.0f}'
          f' L{ex+2*s_:.0f},{ey+16*s_:.0f} Z" fill="{ZHELEZ}" {o(3)}/></g>')
    if kaplya > 0:
        s += (f'<ellipse cx="{ex+4*s_:.0f}" cy="{ey+22*s_+10*kaplya:.0f}"'
              f' rx="{(5+7*kaplya)*s_:.0f}" ry="{(7+11*kaplya)*s_:.0f}"'
              f' fill="#1b2434" {o(2)}/>')
    return s


def _list_bumagi(x, y, w_, h_, t, ug=0.0, stroki=5, pustaya_stroka=True):
    """Лист бумаги: загнутый угол, волнистые строки (букв не рисуем!),
    пустая строка под подпись внизу и тень под листом."""
    s = (f'<g transform="rotate({ug:.1f} {x+w_/2:.0f} {y+h_/2:.0f})">'
         f'{ten(x + w_ / 2, y + h_ + 8, w_ * .46, 12, .4)}'
         f'<path d="M{x:.0f},{y:.0f} L{x+w_-34:.0f},{y:.0f} L{x+w_:.0f},{y+34:.0f}'
         f' L{x+w_:.0f},{y+h_:.0f} L{x:.0f},{y+h_:.0f} Z" fill="#f4efe0" {o(5)}/>'
         f'<path d="M{x+w_-34:.0f},{y:.0f} L{x+w_:.0f},{y+34:.0f} L{x+w_-34:.0f},{y+34:.0f} Z"'
         f' fill="#ddd5c2" {o(3)}/>')
    for i in range(stroki):
        yy = y + h_ * .22 + i * (h_ * .50 / max(1, stroki))
        dl = w_ * (.66 if i % 2 else .78)
        s += (f'<path d="M{x+w_*.10:.0f},{yy:.0f} q{dl*.25:.0f},{-7:.0f} {dl*.5:.0f},0'
              f' q{dl*.25:.0f},{7:.0f} {dl*.5:.0f},0" fill="none" stroke="#6b6354"'
              f' stroke-width="6" opacity=".75"/>')
    if pustaya_stroka:
        mig = .5 + .5 * abs(A.w(t, 1.6))
        s += (f'<line x1="{x+w_*.12:.0f}" y1="{y+h_*.84:.0f}" x2="{x+w_*.66:.0f}"'
              f' y2="{y+h_*.84:.0f}" stroke="#3f4a58" stroke-width="7"'
              f' opacity="{.4+.5*mig:.2f}"/>')
    return s + "</g>"


def _ochki(x, y, s_=1.0, t=0.0):
    """Очки: два стекла в тонкой оправе, переносица, заушники и блик."""
    bl = .3 + .4 * abs(A.w(t, 2.2))
    s = ""
    for i in (-1, 1):
        s += (f'<ellipse cx="{x+i*44*s_:.0f}" cy="{y:.0f}" rx="{38*s_:.0f}"'
              f' ry="{30*s_:.0f}" fill="#cfe0ea" opacity=".5" stroke="#8a6a3c"'
              f' stroke-width="{7*s_:.0f}"/>'
              f'<path d="M{x+i*76*s_:.0f},{y-12*s_:.0f} q{i*40*s_:.0f},{-10*s_:.0f}'
              f' {i*52*s_:.0f},{10*s_:.0f}" fill="none" stroke="#8a6a3c"'
              f' stroke-width="{6*s_:.0f}"/>')
    s += (f'<path d="M{x-8*s_:.0f},{y-6*s_:.0f} q{8*s_:.0f},{-12*s_:.0f}'
          f' {16*s_:.0f},0" fill="none" stroke="#8a6a3c" stroke-width="{6*s_:.0f}"/>'
          f'<line x1="{x-56*s_:.0f}" y1="{y-14*s_:.0f}" x2="{x-34*s_:.0f}"'
          f' y2="{y+10*s_:.0f}" stroke="#ffffff" stroke-width="{5*s_:.0f}"'
          f' opacity="{bl:.2f}"/>')
    return s


def _klyaksa_grust(x, y, s_=1.0, t=0.0, ph=.0):
    """Клякса-несчастье: серая капля с подтёками, грустные глаза и рот
    дугой вниз. Шевелится, как живая."""
    dr = 1.0 + .07 * A.w(t, 1.3, ph)
    s = (f'<g transform="translate({x:.0f} {y:.0f}) scale({dr:.3f})'
         f' translate({-x:.0f} {-y:.0f})">'
         f'<path d="M{x-44*s_:.0f},{y:.0f} q{-10*s_:.0f},{-48*s_:.0f} {30*s_:.0f},{-58*s_:.0f}'
         f' q{44*s_:.0f},{-10*s_:.0f} {56*s_:.0f},{26*s_:.0f}'
         f' q{14*s_:.0f},{40*s_:.0f} {-16*s_:.0f},{50*s_:.0f}'
         f' q{-36*s_:.0f},{10*s_:.0f} {-70*s_:.0f},{-18*s_:.0f} Z"'
         f' fill="#6f7680" {o(4)}/>')
    for i in range(3):
        s += (f'<path d="M{x-28*s_+i*28*s_:.0f},{y+6*s_:.0f} q{4*s_:.0f},{22*s_:.0f}'
              f' {-2*s_:.0f},{34*s_:.0f}" fill="none" stroke="#6f7680"'
              f' stroke-width="{11*s_:.0f}" stroke-linecap="round"/>')
    for i in (-1, 1):
        s += (f'<ellipse cx="{x+i*17*s_:.0f}" cy="{y-26*s_:.0f}" rx="{9*s_:.0f}"'
              f' ry="{11*s_:.0f}" fill="#f2f6fa"/>'
              f'<circle cx="{x+i*17*s_:.0f}" cy="{y-22*s_:.0f}" r="{5*s_:.0f}"'
              f' fill="#23282f"/>'
              f'<path d="M{x+i*28*s_:.0f},{y-42*s_:.0f} q{-i*11*s_:.0f},{-7*s_:.0f}'
              f' {-i*22*s_:.0f},{2*s_:.0f}" fill="none" stroke="#3a4049"'
              f' stroke-width="{5*s_:.0f}"/>')
    s += (f'<path d="M{x-14*s_:.0f},{y+2*s_:.0f} q{14*s_:.0f},{-14*s_:.0f}'
          f' {28*s_:.0f},0" fill="none" stroke="#3a4049" stroke-width="{6*s_:.0f}"'
          f' stroke-linecap="round"/></g>')
    return s


def _polki_otkrytye(x, y, w_, t, seed=11, n=3, ruchki_vlevo=True, sdvig=.0):
    """Открытые кухонные полки: три доски на кронштейнах, чашки на крючках
    ручками в одну сторону, тарелки по росту ребром, банки крупы."""
    rnd = random.Random(seed)
    s = ""
    for p in range(n):
        py = y + p * 170
        s += (f'<rect x="{x:.0f}" y="{py:.0f}" width="{w_:.0f}" height="22" rx="7"'
              f' fill="url(#dosk)" {o(5)}/>')
        for k in (x + 60, x + w_ - 90):
            s += (f'<path d="M{k:.0f},{py+22:.0f} l26,38 l-26,0 Z" fill="{ZHELEZ}" {o(3)}/>')
        if p == 0:
            for i in range(5):
                cx = x + 90 + i * (w_ - 180) / 4.0
                sg = -1 if ruchki_vlevo else 1
                sg = sg if i % 2 or sdvig < .5 else -sg
                s += _kruzhka(cx, py - 6, .92, 0, "#eceff0", sg)
        elif p == 1:
            for i in range(6):
                r = 54 + i * 11
                s += (f'<ellipse cx="{x+80+i*(w_-170)/5.0:.0f}" cy="{py-r*.5:.0f}"'
                      f' rx="{r*.28:.0f}" ry="{r*.5:.0f}" fill="#e7edf0" {o(4)}/>'
                      f'<ellipse cx="{x+80+i*(w_-170)/5.0:.0f}" cy="{py-r*.5:.0f}"'
                      f' rx="{r*.12:.0f}" ry="{r*.34:.0f}" fill="#cfd8dc" opacity=".8"/>')
        else:
            for i in range(4):
                s += _banka_krupy(x + 110 + i * (w_ - 220) / 3.0, py - 6,
                                  rnd.uniform(.86, 1.04),
                                  ["#d8c08a", "#b8a068", "#e0d2a8", "#c0a878"][i])
    return s


def _okno_razdachi(x, y, w_, h_, t):
    """Окно-раздача между кухней и комнатой: широкий подоконник-полка,
    наличник в четверть, два крюка створок и блик по верхней кромке."""
    return (f'<rect x="{x-26:.0f}" y="{y-26:.0f}" width="{w_+52:.0f}"'
            f' height="{h_+52:.0f}" rx="10" fill="none" stroke="#8a7254"'
            f' stroke-width="26"/>'
            f'<rect x="{x-54:.0f}" y="{y+h_-6:.0f}" width="{w_+108:.0f}" height="40"'
            f' rx="10" fill="url(#dosk)" {o(6)}/>'
            f'<rect x="{x-40:.0f}" y="{y-48:.0f}" width="{w_+80:.0f}" height="30"'
            f' rx="9" fill="#9c8464" {o(5)}/>'
            f'<path d="M{x+20:.0f},{y-4:.0f} L{x+w_-20:.0f},{y-4:.0f}" fill="none"'
            f' stroke="#eaf4ff" stroke-width="7"'
            f' opacity="{.25+.2*abs(A.w(t,3.2)):.2f}"/>'
            f'<circle cx="{x-30:.0f}" cy="{y+h_*.5:.0f}" r="11" fill="{ZHELEZ}" {o(3)}/>'
            f'<circle cx="{x+w_+30:.0f}" cy="{y+h_*.5:.0f}" r="11" fill="{ZHELEZ}" {o(3)}/>')


def _polovik(x, y, w_, h_, col=RUSH, pol=KRAS):
    """Половик-дорожка: перспективная трапеция, две цветные полосы, бахрома."""
    s = (f'<path d="M{x:.0f},{y:.0f} L{x+w_:.0f},{y:.0f} L{x+w_+h_*.3:.0f},{y+h_:.0f}'
         f' L{x-h_*.3:.0f},{y+h_:.0f} Z" fill="{col}" {o(5)}/>'
         f'<path d="M{x+16:.0f},{y+h_*.34:.0f} L{x+w_-16:.0f},{y+h_*.34:.0f}"'
         f' stroke="{pol}" stroke-width="12" opacity=".7"/>'
         f'<path d="M{x+2:.0f},{y+h_*.70:.0f} L{x+w_-2:.0f},{y+h_*.70:.0f}"'
         f' stroke="{TKAN2}" stroke-width="9" opacity=".6"/>')
    for i in range(int(w_ / 44)):
        s += (f'<line x1="{x-h_*.3+i*48:.0f}" y1="{y+h_:.0f}"'
              f' x2="{x-h_*.3+i*48-6:.0f}" y2="{y+h_+20:.0f}" stroke="#d8c8a8"'
              f' stroke-width="5" opacity=".8"/>')
    return s


def _knizhnaya_polka(x, y, w_, t, seed=7, polok=2, step=180):
    """Полка с книгами: корешки разной высоты и толщины, пара книг лежит
    плашмя, одна наклонена. Держит средний план там, где стена пустая."""
    rnd = random.Random(seed)
    cols = ["#7a3a32", "#3f5c7a", "#4a6a48", "#8a6a2c", "#5a4a62", "#9c6a3c"]
    s = ""
    for p in range(polok):
        py = y + p * step
        s += (f'<rect x="{x:.0f}" y="{py:.0f}" width="{w_:.0f}" height="22" rx="7"'
              f' fill="url(#dosk)" {o(5)}/>'
              f'<rect x="{x+10:.0f}" y="{py+22:.0f}" width="20" height="30"'
              f' fill="#4a3522" {o(3)}/>'
              f'<rect x="{x+w_-30:.0f}" y="{py+22:.0f}" width="20" height="30"'
              f' fill="#4a3522" {o(3)}/>')
        bx = x + 18
        while bx < x + w_ - 90:
            tol = rnd.uniform(26, 50)
            hh = rnd.uniform(118, 168)
            nak = rnd.uniform(-9, 9) if rnd.random() < .22 else 0.0
            col = cols[rnd.randrange(len(cols))]
            s += (f'<g transform="rotate({nak:.1f} {bx:.0f} {py:.0f})">'
                  f'<rect x="{bx:.0f}" y="{py-hh:.0f}" width="{tol:.0f}"'
                  f' height="{hh:.0f}" rx="4" fill="{col}" {o(4)}/>'
                  f'<rect x="{bx+4:.0f}" y="{py-hh*.82:.0f}" width="{tol-8:.0f}"'
                  f' height="12" fill="#e8d8a8" opacity=".7"/>'
                  f'<rect x="{bx+4:.0f}" y="{py-hh*.34:.0f}" width="{tol-8:.0f}"'
                  f' height="8" fill="#e8d8a8" opacity=".5"/></g>')
            bx += tol + 6
        s += (f'<rect x="{x+w_-96:.0f}" y="{py-54:.0f}" width="86" height="26" rx="5"'
              f' fill="{cols[(seed + p) % len(cols)]}" {o(4)}/>'
              f'<rect x="{x+w_-92:.0f}" y="{py-28:.0f}" width="80" height="24" rx="5"'
              f' fill="{cols[(seed + p + 2) % len(cols)]}" {o(4)}/>')
    return s


def _ramki_na_stene(x, y, w_, t, seed=5, n=4):
    """Рамки на стене: фотографии и вышивки за стеклом, у каждой паспарту,
    блик по углу и гвоздик. Вместо лиц — предметы (афиши рисованные)."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        rw = rnd.uniform(150, 230)
        rh = rw * rnd.uniform(.62, .86)
        rx_ = x + i * (w_ / max(1, n)) + rnd.uniform(-10, 10)
        ry_ = y + (0 if i % 2 else 54)
        ug = rnd.uniform(-3, 3)
        s += (f'<g transform="rotate({ug:.1f} {rx_:.0f} {ry_:.0f})">'
              f'<rect x="{rx_:.0f}" y="{ry_:.0f}" width="{rw:.0f}" height="{rh:.0f}"'
              f' rx="6" fill="#6a5030" {o(5)}/>'
              f'<rect x="{rx_+16:.0f}" y="{ry_+16:.0f}" width="{rw-32:.0f}"'
              f' height="{rh-32:.0f}" rx="4" fill="#efe8d6" {o(3)}/>')
        if i % 2:
            s += (f'<path d="M{rx_+rw*.26:.0f},{ry_+rh*.74:.0f}'
                  f' q{rw*.24:.0f},{-rh*.46:.0f} {rw*.48:.0f},0 Z"'
                  f' fill="#8a9a58" opacity=".85"/>')
        else:
            s += (f'<circle cx="{rx_+rw*.5:.0f}" cy="{ry_+rh*.5:.0f}"'
                  f' r="{rh*.22:.0f}" fill="#b9a071" opacity=".85"/>')
        s += (f'<path d="M{rx_+18:.0f},{ry_+rh-20:.0f} L{rx_+rw*.5:.0f},{ry_+20:.0f}'
              f' L{rx_+rw*.66:.0f},{ry_+20:.0f} L{rx_+rw*.32:.0f},{ry_+rh-20:.0f} Z"'
              f' fill="#ffffff" opacity="{.10+.10*abs(A.w(t,3.0,i*.2)):.2f}"/>'
              f'<circle cx="{rx_+rw*.5:.0f}" cy="{ry_-10:.0f}" r="7"'
              f' fill="{ZHELEZ}"/></g>')
    return s


def _sushilka_posudy(x, y, w_, t, seed=3):
    """Сушилка над мойкой: решётка, тарелки ребром, кружки дном вверх,
    поддон с каплями. Сопутствующие вещи среднего плана у самой мойки."""
    rnd = random.Random(seed)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="20" rx="7"'
         f' fill="#8f979c" {o(5)}/>'
         f'<rect x="{x:.0f}" y="{y+176:.0f}" width="{w_:.0f}" height="26" rx="8"'
         f' fill="#7d868c" {o(5)}/>')
    for i in range(int(w_ / 42)):
        s += (f'<line x1="{x+14+i*42:.0f}" y1="{y+20:.0f}" x2="{x+14+i*42:.0f}"'
              f' y2="{y+176:.0f}" stroke="#a7b0b6" stroke-width="7"/>')
    for i in range(5):
        r = 148 + (i % 3) * 22
        px = x + 54 + i * (w_ - 120) / 4.0
        s += (f'<ellipse cx="{px:.0f}" cy="{y+104:.0f}" rx="{r*.11:.0f}"'
              f' ry="{r*.5:.0f}" fill="#e7edf0" {o(4)}/>'
              f'<ellipse cx="{px:.0f}" cy="{y+104:.0f}" rx="{r*.05:.0f}"'
              f' ry="{r*.34:.0f}" fill="#cfd8dc" opacity=".8"/>')
    for i in range(3):
        cx = x + 90 + i * (w_ - 190) / 2.0
        s += (f'<path d="M{cx-40:.0f},{y+200:.0f} L{cx+40:.0f},{y+200:.0f}'
              f' L{cx+32:.0f},{y+126:.0f} L{cx-32:.0f},{y+126:.0f} Z"'
              f' fill="#eceff0" {o(4)}/>')
    for i in range(6):
        s += (f'<ellipse cx="{x+30+i*64:.0f}" cy="{y+214:.0f}" rx="9"'
              f' ry="{6+4*abs(A.w(t,1.8,i*.2)):.1f}" fill="#cfe0ea" opacity=".8"/>')
    return s


def _svitki_i_papki(x, y, t, seed=5, n=5):
    """Свитки и папки конторы: трубки с печатями и тесьмой, пара папок
    стоймя. Строки на свитках — волнистые, своих букв не рисуем."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        sx = x + i * 92
        hh = rnd.uniform(130, 190)
        ug = rnd.uniform(-7, 7)
        s += (f'<g transform="rotate({ug:.1f} {sx:.0f} {y:.0f})">'
              f'<rect x="{sx-26:.0f}" y="{y-hh:.0f}" width="52" height="{hh:.0f}"'
              f' rx="20" fill="#e8dcc0" {o(5)}/>'
              f'<ellipse cx="{sx:.0f}" cy="{y-hh:.0f}" rx="26" ry="10"'
              f' fill="#d4c6a4" {o(3)}/>'
              f'<rect x="{sx-30:.0f}" y="{y-hh*.56:.0f}" width="60" height="14" rx="6"'
              f' fill="{TKAN}" opacity=".85"/>'
              f'<circle cx="{sx+22:.0f}" cy="{y-hh*.46:.0f}" r="13" fill="#9c2f28"'
              f' {o(2)}/></g>')
    for i in range(2):
        px = x + n * 92 + 30 + i * 74
        s += (f'<rect x="{px:.0f}" y="{y-200:.0f}" width="64" height="200" rx="7"'
              f' fill="#8a6a44" {o(5)}/>'
              f'<rect x="{px+8:.0f}" y="{y-186:.0f}" width="48" height="172" rx="5"'
              f' fill="#efe8d6" opacity=".85"/>'
              f'<path d="M{px+16:.0f},{y-150:.0f} q16,-8 32,0" fill="none"'
              f' stroke="#9a8a68" stroke-width="5"/>')
    return s


def _valenki_u_dveri(x, y, s_=1.0, t=0.0):
    """Пара валенок у двери: голенища разной высоты, подшитая подошва."""
    s = ""
    for i, dx in enumerate((-46, 42)):
        hh = (150 if i == 0 else 138) * s_
        s += (f'{ten(x + dx * s_, y + 6 * s_, 44 * s_, 11 * s_, .4)}'
              f'<path d="M{x+dx*s_-36*s_:.0f},{y:.0f} L{x+dx*s_+36*s_:.0f},{y:.0f}'
              f' L{x+dx*s_+28*s_:.0f},{y-hh:.0f} L{x+dx*s_-24*s_:.0f},{y-hh:.0f} Z"'
              f' fill="#6b6256" {o(5)}/>'
              f'<rect x="{x+dx*s_-38*s_:.0f}" y="{y-12*s_:.0f}" width="{76*s_:.0f}"'
              f' height="{14*s_:.0f}" rx="6" fill="#3f3a33" {o(3)}/>'
              f'<path d="M{x+dx*s_-22*s_:.0f},{y-hh+10*s_:.0f}'
              f' q{22*s_:.0f},{10*s_:.0f} {48*s_:.0f},0" fill="none" stroke="#8a8274"'
              f' stroke-width="{6*s_:.0f}" opacity=".8"/>')
    return s


# ── РУКА МИМО ЧУЖОЙ ФИГУРЫ (блокер осмотра порции 2) ───────────────────────
# `_ruka` обещает только одно: рука не попадёт в СВОЮ голову и грудь. Соседей
# она не знает — и в кадре рукав шёл сквозь голову и платок соседней фигуры,
# а жердь проходила сквозь лицо. Числами это не ловится: гейт анатомии считает
# только свои фигуры. Лечение правилом, а не поштучно: сцена объявляет, где
# стоят ВСЕ её фигуры, а рука сама укорачивается и доворачивается, пока
# отрезок плечо→кисть не разойдётся с чужими головами и корпусами.
_CHUZHIE = []


def _figury_kadra(*tochki):
    """Объявить фигуры сцены как (x, уровень пола, рост). Зовётся ОДИН раз в
    начале сцены, до первой руки; дальше `_ruka_mimo` обходит их сама."""
    global _CHUZHIE
    _CHUZHIE = [(float(a), float(b), float(c)) for a, b, c in tochki]
    return ""


def _gabarit_figury(fx, fy, fh):
    """Прямоугольники головы и корпуса фигуры — по размерам `figura()`."""
    hh = fh * .145
    gy = fy - fh * .845
    w_ = fh * .42
    return ((fx - hh * 1.2, gy - hh * 1.3, fx + hh * 1.2, gy + hh * 1.3),
            (fx - w_ * .44, fy - fh * .68, fx + w_ * .44, fy - fh * .10))


def _otrezok_v_pryam(x1, y1, x2, y2, r):
    """Пересекает ли отрезок прямоугольник (отсечение Лианга — Барски)."""
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for q_, p_ in ((x1 - r[0], -dx), (r[2] - x1, dx), (y1 - r[1], -dy), (r[3] - y1, dy)):
        if abs(p_) < 1e-9:
            if q_ < 0:
                return False
            continue
        rr = q_ / p_
        if p_ < 0:
            if rr > t1:
                return False
            t0 = max(t0, rr)
        else:
            if rr < t0:
                return False
            t1 = min(t1, rr)
    return t0 <= t1


def _chisto_ot_chuzhih(fx, fy, fh, px, py, ex, ey, zapas=1.0):
    """Отрезок плечо→кисть не задевает ни одну ЧУЖУЮ фигуру кадра."""
    for cx, cy, ch in _CHUZHIE:
        if abs(cx - fx) < 24.0 and abs(ch - fh) < 24.0:
            continue                      # это я сам (идущая фигура смещается)
        gol, kor = _gabarit_figury(cx, cy, ch)
        gol = (gol[0] - zapas * 6, gol[1] - zapas * 6,
               gol[2] + zapas * 6, gol[3] + zapas * 6)
        if _otrezok_v_pryam(px, py, ex, ey, gol):
            return False
        if _otrezok_v_pryam(px, py, ex, ey, kor):
            return False
    return True


def _ruka_mimo(fx, fy, fh, storona, dl, ug, t, col="#2a2430", kant="#cfe4f5",
               ph=.0, amp=6.0):
    """Тот же `_ruka`, но рука не доходит до чужой фигуры: сначала пробуем
    укоротить (кисть останавливается перед соседом), потом довернуть вниз —
    и только если не вышло, отдаём как есть. Возвращает то же, что `_ruka`."""
    px, py = _plecho(fx, fy, fh, storona)
    for dovorot in (0.0, 10.0, 20.0, 32.0, -12.0, -24.0):
        u = max(-58.0, min(88.0, float(ug) + dovorot))
        for k in (1.0, .92, .84, .76, .68, .60, .52, .44, .36, .30):
            a = u if storona > 0 else 180.0 - u
            rad = math.radians(a + amp * A.w(t, .9, ph))
            ex = px + dl * k * math.cos(rad)
            ey = py + dl * k * math.sin(rad)
            if _chisto_ot_chuzhih(fx, fy, fh, px, py, ex, ey):
                return _ruka(fx, fy, fh, storona, dl * k, u, t, col, kant, ph, amp)
    return _ruka(fx, fy, fh, storona, dl * .34, ug, t, col, kant, ph, amp)


def _ruka_sgib_mimo(fx, fy, fh, storona, dl1, ug1, dl2, ug2, t,
                    col="#2a2430", kant="#cfe4f5", ph=.0, amp=6.0):
    """Рука со сгибом, которая так же обходит чужие фигуры: укорачиваются
    оба звена сразу, предплечье остаётся наружу."""
    px, py = _plecho(fx, fy, fh, storona)
    for dovorot in (0.0, 12.0, 24.0, -14.0):
        u1 = max(-58.0, min(88.0, float(ug1) + dovorot))
        u2 = max(-58.0, min(88.0, float(ug2) + dovorot))
        for k in (1.0, .90, .80, .70, .60, .50, .40, .32):
            a1 = u1 if storona > 0 else 180.0 - u1
            r1 = math.radians(a1 + amp * A.w(t, .9, ph))
            lx = px + dl1 * k * math.cos(r1)
            ly = py + dl1 * k * math.sin(r1)
            a2 = u2 if storona > 0 else 180.0 - u2
            r2 = math.radians(a2 + amp * .7 * A.w(t, .9, ph + .3))
            ex = lx + dl2 * k * math.cos(r2)
            ey = ly + dl2 * k * math.sin(r2)
            if (_chisto_ot_chuzhih(fx, fy, fh, px, py, lx, ly)
                    and _chisto_ot_chuzhih(fx, fy, fh, lx, ly, ex, ey)):
                return _ruka_so_sgibom(fx, fy, fh, storona, dl1 * k, u1,
                                       dl2 * k, u2, t, col, kant, ph, amp)
    return _ruka_so_sgibom(fx, fy, fh, storona, dl1 * .4, ug1, dl2 * .4, ug2,
                           t, col, kant, ph, amp)


# ── ДЕКОРАЦИИ ──────────────────────────────────────────────────────────────

def babushkin_venik_v_uglu(t):
    """Угол деревенской кухни у печи: сточенный веник в пол-кадра среди
    кочерги, ухвата и совка. Внучка протягивает новый пышный веник, бабушка
    на табурете отводит его левой рукой и гладит ручку старого правой."""
    rnd = random.Random(201)
    pol = 902
    s = f'<rect width="{W}" height="{H}" fill="#2a2119"/>'
    # задник: бревенчатая стена двумя простенками (не фон — держит сетку)
    s += SL(Z_DAL, brevna(0, 60, 1040, pol - 60, 96)
            + brevna(1040, 60, 880, pol - 60, 96))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="30"'
                   f' fill="#3b2a1a" opacity=".9"/>' + polovicy(pol + 12))
    s += SL(Z_DAL, _polka_s_utvaryu(96, 300, 520, t, 11, 4))
    # печь справа: массив, устье с огнём, шесток
    s += SL(Z_SRED, pech(1430, 268, 490, 634, t, True, True, False))
    s += SL(Z_SRED, kirpich_ustya(1520, 646, 300, 200, t, True))
    s += SL(Z_SRED, ogon(1670, 804, t, 1.35, .2, 7))
    s += SL(Z_SRED, ugli(1540, 836, 260, t, 7, 2))
    s += SL(Z_SRED, dym(1480, 240, t, 4, .22, 260, .3, "#cfd6de", 1.2))
    # угол с печной утварью
    s += SL(Z_SRED, _ugol_pechnoy_utvari(1320, pol, t, 3))
    # где в кадре стоят ОБЕ фигуры — рука внучки обходит бабушку
    dx, dy_, dh = 330, pol + 26, 690
    bx, by_, bh = 860, pol + 10, 452
    _figury_kadra((dx, dy_, dh), (bx, by_ - 168, bh))
    otv = A.ease(A.seg(t, .5, 1.3))
    glad = A.w(t, 1.5, .1)
    # РУКИ СЧИТАЮТСЯ ДО РИСОВАНИЯ: веник ставится РОВНО В КИСТЬ, иначе
    # черенок и варежка расходятся на сотню пикселей и хват не читается
    # (осмотр порции 2).
    dev = figura(dx, dy_, dh, t, col="#4a5a72", kant="#ffd98a", ph=.2)
    r1, (h1x, h1y), _ = _ruka_mimo(dx, dy_, dh, 1, dh * .40, 16 + 10 * otv, t,
                                   "#4a5a72", "#ffd98a", .2, 5.0)
    r2, (h2x, h2y), _ = _ruka_mimo(dx, dy_, dh, -1, dh * .26, 34, t,
                                   "#4a5a72", "#ffd98a", .6, 4.0)
    dev += r1 + r2
    bab = figura(bx, by_ - 168, bh, t, col="#54505e", kant="#ffd98a",
                 platok=True, ph=.5, naklon=4.0)
    rb1, (b1x, b1y), _ = _ruka_mimo(bx, by_ - 168, bh, -1, bh * .50,
                                    10 + 16 * otv, t,
                                    "#54505e", "#ffd98a", .5, 6.0)
    rb2, (b2x, b2y), _ = _ruka_sgib_mimo(bx, by_ - 168, bh, 1, bh * .44, 26,
                                         bh * .44, 44 + 8 * glad, t,
                                         "#54505e", "#ffd98a", .1, 5.0)
    bab += rb1 + rb2
    # СТАРЫЙ ВЕНИК — главный предмет: ручкой вниз, веер КОРОЧЕ черенка
    # («сточенный»), прутья СВЕТЛЫЕ — #8a7340 на срубе #8e6337 давал разницу
    # 16/255 и веер растворялся в бревне. Черенок приходит ровно в кисть.
    vx, vy, vh = b2x - 4, pol + 4, 430
    s += SL(Z_SRED, _venik(vx, vy, vh, t, "#d8c48a", "#b8352c", True, .22, .1,
                           1.12, 211))
    s += SL(Z_SRED, f'<ellipse cx="{vx+2:.0f}" cy="{vy-vh*.20:.0f}" rx="34"'
                    f' ry="22" fill="#c9a463"'
                    f' opacity="{.30+.18*abs(glad):.2f}"/>')
    # НОВЫЙ веник — в кисти внучки, прутьями от неё
    s += SL(Z_SRED, _venik_v_ruke(h1x, h1y + 6, 320, t, "#b8a86a", "#5a4a2e",
                                  76 - 26 * otv, .88, 213, .34, .3))
    s += SL(Z_SRED, _tabyret(bx + 16, by_, t, 168, 182))
    s += SL(Z_SRED, dev)
    s += SL(Z_SRED, bab)
    # варежки ПОВЕРХ черенков: хват читается перекрытием, а не соседством
    s += SL(Z_SRED, _varezhka(h1x, h1y + 2, dh, t, .2)
            + _varezhka(b2x, b2y + 2, bh, t, .1))
    s += SL(Z_SRED, ten(bx + 10, by_ + 6, 150, 24, .5))
    # кот трётся о веник, нижняя треть занята вещами
    kot_x = vx - 230 + 30 * A.w(t, 4.0, .2)
    s += SL(Z_SRED, _kot_zhivoy(kot_x, pol + 58, t, 1.05, "#38332e", .3))
    s += SL(Z_SRED, _dvorovaya_utvar(96, pol + 96, 330, t, 29,
                                     ["korzina", "vedro"])
            + _polovik(560, pol + 70, 540, 118)
            + kartoshka(1180, pol + 92, t, 6, 6, 1.0)
            + _valenki_u_dveri(248, pol + 54, 1.0, t))
    s += SL(Z_SRED, teplo(1660, 790, 520, 420, .40))
    s += SL(Z_PERED, _stolb_pered(-10, 118, "#1a120c", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 1670, 790, 8, 4, 260, .42))
    s += vinetka(.42)
    return s


def gostya_s_chuzhoy_tryapkoy(t):
    """Чужая кухня: мойка с горой тарелок на пол-кадра. Гостья в бусах уже
    закатала рукав и берёт тряпку, хозяйка в фартуке обеими руками мягко
    забирает её. Пена оседает, бусы качаются."""
    rnd = random.Random(203)
    pol = 980
    s = f'<rect width="{W}" height="{H}" fill="#2f3338"/>'
    s += SL(Z_DAL, _kafel(0, 40, 1180, 540, t, 3, "#d4dcdc"))
    s += SL(Z_DAL, _kafel(1180, 40, 740, 540, t, 9, "#c8d2d4"))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-6:.0f}" width="{W}" height="{H-pol+6:.0f}"'
                   f' fill="#564b40"/>'
            + _polovik(430, pol + 24, 700, 86, "#cfc3a8", "#7a6a52"))
    s += SL(Z_DAL, _polki_otkrytye(1240, 150, 620, t, 17, 2, True, .0))
    # мойка — главный предмет кадра
    osd = A.ease(A.seg(t, 1.2, 1.6))
    s += SL(Z_SRED, _moyka(300, 590, 1240, t, 5, True, osd))
    # ГОРА ТАРЕЛОК на борту мойки
    s += SL(Z_SRED, _stopka_tarelok(1310, 576, 8, t, 23, 196))
    s += SL(Z_SRED, _tarelka(1176, 548, 92, t, .3, True, -16))
    s += SL(Z_SRED, _kastryulya(1448, 586, 1.0, t, True)
            + _chaynik(246, 584, 1.05, t)
            + _kruzhka(560, 580, .9, 0, "#e8eef0", 1)
            + _kruzhka(640, 578, .86, 0, "#ecdfd0", -1))
    s += SL(Z_SRED, par(620, 520, t, 4, .42, 180, .36, 1.0))
    s += SL(Z_SRED, _polotence(1600, 388, 230, t, .2, "#e3ddc6", True))
    _figury_kadra((700, pol + 36, 742), (1240, pol + 44, 860))
    # гостья: правый рукав закатан, правой берёт тряпку, левой тянется к тарелке
    gx, gy, gh = 700, pol + 36, 742
    ber = A.ease(A.seg(t, .3, .9))
    otdal = A.ease(A.seg(t, 1.5, 1.0))
    gost = figura(gx, gy, gh, t, col="#7a3a52", kant="#ffd98a", ph=.2,
                  naklon=5.0)
    g1, (t1x, t1y), _ = _ruka_mimo(gx, gy, gh, 1, gh * .40, 26 + 18 * ber - 26 * otdal, t,
                              "#7a3a52", "#ffd98a", .2, 5.0)
    g2, (t2x, t2y), _ = _ruka_mimo(gx, gy, gh, -1, gh * .34, 36 - 20 * otdal, t,
                              "#e8d8c0", "#ffd98a", .6, 4.0)
    gost += g1 + g2
    # бусы: качаются от наклона
    kach = 9 * A.w(t, 1.7, .3)
    for i in range(11):
        a = math.radians(-74 + i * 15)
        gost += (f'<circle cx="{gx+74*math.cos(a)+kach*.3:.0f}"'
                 f' cy="{gy-gh*.60+52*abs(math.sin(a))+kach*.4:.0f}" r="9"'
                 f' fill="#e2c76a" stroke="{K}" stroke-width="2"/>')
    s += SL(Z_SRED, gost)
    # тряпка переходит из рук в руки
    # ТРЯПКА крупная и своего цвета: раньше её путали с фартуком хозяйки
    tr = (f'<path d="M{t1x-96:.0f},{t1y-44:.0f} q{56:.0f},{-50:.0f} {152:.0f},{-18:.0f}'
          f' q{44:.0f},{68:.0f} {2:.0f},{130:.0f} q{-92:.0f},{28:.0f}'
          f' {-154:.0f},{-34:.0f} Z" fill="#6f93a4" {o(6)}/>')
    for q_ in range(3):
        tr += (f'<path d="M{t1x-56+q_*36:.0f},{t1y-34:.0f} q{10:.0f},{52:.0f}'
               f' {-4:.0f},{92:.0f}" fill="none" stroke="#587a8c"'
               f' stroke-width="7" opacity=".9"/>')
    tr += (f'<path d="M{t1x-70:.0f},{t1y+54:.0f} q{60:.0f},{26:.0f} {120:.0f},{4:.0f}"'
           f' fill="none" stroke="#9ab4c0" stroke-width="9"/>'
           f'<path d="M{t1x-30:.0f},{t1y+16:.0f} q{30:.0f},{-18:.0f} {62:.0f},{2:.0f}"'
           f' fill="none" stroke="#86a6b6" stroke-width="6"/>')
    # (тряпка рисуется ПОСЛЕ хозяйки, ниже: её корпус закрывал 65% —
    # осмотр порции 2)
    # хозяйка в фартуке: обе руки забирают тряпку
    hx, hy, hh = 1240, pol + 44, 860
    hoz = figura(hx, hy, hh, t, col="#3f4a58", kant="#ffd98a", platok=True,
                 ph=.7, profil=False)
    h1, (q1x, q1y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .38, 22 + 14 * otdal, t,
                              "#3f4a58", "#ffd98a", .7, 5.0)
    h2, (q2x, q2y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .30, 48 + 10 * otdal, t,
                              "#3f4a58", "#ffd98a", .3, 4.0)
    hoz += h1 + h2
    hoz += (f'<path d="M{hx-60:.0f},{hy-hh*.56:.0f} L{hx+60:.0f},{hy-hh*.56:.0f}'
            f' L{hx+78:.0f},{hy-hh*.10:.0f} L{hx-78:.0f},{hy-hh*.10:.0f} Z"'
            f' fill="#e4dcc8" {o(5)}/>'
            f'<path d="M{hx-78:.0f},{hy-hh*.36:.0f} q{78:.0f},{16:.0f} {156:.0f},0"'
            f' fill="none" stroke="#c4b79c" stroke-width="7"/>')
    s += SL(Z_SRED, hoz)
    s += SL(Z_SRED, tr)
    s += SL(Z_SRED, ten(gx, gy + 8, 170, 26, .45) + ten(hx, hy + 8, 180, 26, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(t1x, t1y, gh, t, .2) + ""
            + _varezhka(q1x, q1y, hh, t, .7) + _varezhka(q2x, q2y, hh, t, .3))
    s += SL(Z_SRED, _pol_shvy(pol + 10, 1078, 11, 6, "#413528"))
    # низ кадра: ведро, таз, ящик с луком, кот у тумбы
    s += SL(Z_SRED, _dvorovaya_utvar(96, pol + 72, 300, t, 31, ["vedro", "korob"])
            + _yaschiki(1560, pol + 70, t, 7, 2, .82)
            + _kot_zhivoy(1402, pol + 60, t, .92, "#4a423c", .6))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += SL(Z_LETIT, _pena_gorka(660, 560, 90, t, 41, 7, 1 - osd))
    s += vinetka(.40)
    return s


def tarelka_s_chuzhimi_neschastyami(t):
    """Чужая тарелка в мыльной пене во весь кадр, вокруг ложки, губка,
    кружка. Видны только руки до локтя: левая держит тарелку за край,
    правая трёт её по кругу, и по правой руке лезут три кляксы."""
    rnd = random.Random(207)
    s = f'<rect width="{W}" height="{H}" fill="#2b3338"/>'
    s += SL(Z_DAL, _kafel(0, 0, 1120, 520, t, 5, "#cdd7d8"))
    s += SL(Z_DAL, _kafel(1120, 0, 800, 520, t, 13, "#c2cccd"))
    s += SL(Z_DAL, _sushilka_posudy(100, 60, 640, t, 3))
    s += SL(Z_DAL, _polka_s_utvaryu(1180, 300, 620, t, 67, 5))
    s += SL(Z_DAL, f'<rect x="0" y="446" width="{W}" height="120" rx="8"'
                   f' fill="#a9a194" {o(6)}/>')
    # чаша мойки крупно: борт, дно, вода
    s += SL(Z_SRED, f'<path d="M160,500 L1760,500 L1660,1040 L260,1040 Z"'
                    f' fill="#5e676e" {o(7)}/>'
            + f'<path d="M226,560 L1694,560 L1612,980 L308,980 Z"'
              f' fill="#49535b" {o(5)}/>'
            + f'<ellipse cx="960" cy="986" rx="150" ry="34" fill="#333c43" {o(4)}/>')
    s += SL(Z_SRED, _pena_gorka(520, 930, 300, t, 19, 20, .3)
            + _pena_gorka(1420, 920, 250, t, 23, 16, .2))
    # ГЛАВНЫЙ ПРЕДМЕТ: тарелка, её роняют в пену
    pad = A.out(A.seg(t, 3.6, 1.0))
    tcx, tcy = 930, 606 + 230 * pad
    s += SL(Z_SRED, _tarelka(tcx, tcy, 300, t, .0, True, -6 + 14 * pad))
    # тряпка трёт по кругу
    a = t * 2.1
    rx_, ry_ = tcx + 150 * math.cos(a), tcy + 112 * math.sin(a)
    s += SL(Z_SRED, f'<path d="M{rx_-78:.0f},{ry_-40:.0f} q{52:.0f},{-34:.0f}'
                    f' {122:.0f},{-10:.0f} q{22:.0f},{54:.0f} {-16:.0f},{90:.0f}'
                    f' q{-74:.0f},{16:.0f} {-106:.0f},{-70:.0f} Z"'
                    f' fill="#9ab4c0" {o(5)}/>'
            + f'<path d="M{rx_-50:.0f},{ry_-16:.0f} q{44:.0f},{22:.0f} {80:.0f},{10:.0f}"'
              f' fill="none" stroke="#7e97a6" stroke-width="8"/>')
    # ЛЕВАЯ РУКА до локтя — ничья (крупный план кистей, человека в кадре нет)
    lruk, (lx2, ly2) = rukav(118, 1062, 440, -56, t, "#e8d8c0", "#ffd98a", .2,
                             4.0, True)
    s += SL(Z_SRED, lruk)
    s += SL(Z_SRED, f'<ellipse cx="{lx2:.0f}" cy="{ly2:.0f}" rx="56" ry="40"'
                    f' fill="#e8d8c0" {o(5)}/>'
            + f'<rect x="{lx2-92:.0f}" y="{ly2+30:.0f}" width="150" height="40" rx="16"'
              f' fill="#7a3a52" {o(5)}/>')
    # ПРАВАЯ РУКА до локтя — тоже ничья, по ней лезут кляксы
    rruk, (rx2, ry2) = rukav(1848, 1066, 470, -122, t, "#e8d8c0", "#ffd98a", .5,
                             4.0, True)
    s += SL(Z_SRED, rruk)
    s += SL(Z_SRED, f'<ellipse cx="{rx2:.0f}" cy="{ry2:.0f}" rx="58" ry="42"'
                    f' fill="#e8d8c0" {o(5)}/>'
            + f'<rect x="{rx2-30:.0f}" y="{ry2+34:.0f}" width="156" height="42" rx="16"'
              f' fill="#7a3a52" {o(5)}/>')
    # три кляксы лезут по правой руке к локтю и стряхиваются в мойку
    stry = A.ease(A.seg(t, 4.6, .9))
    for i in range(3):
        p = min(1.0, max(.0, A.seg(t, .6 + i * .35, 1.6)))
        kx = rx2 + (1848 - rx2) * p * .82 + 120 * stry
        ky = ry2 + (1066 - ry2) * p * .82 + 230 * stry * (1 + i * .2)
        s += SL(Z_SRED, _klyaksa_grust(kx, ky, .92 + .1 * i, t, i * .3))
    # ложки, губка, кружка вокруг
    for i in range(4):
        lxx = 300 + i * 118
        s += SL(Z_SRED, f'<ellipse cx="{lxx:.0f}" cy="{530+(i%2)*14:.0f}" rx="40"'
                        f' ry="26" fill="#cfd8dc" {o(4)}/>'
                f'<path d="M{lxx+30:.0f},{532+(i%2)*14:.0f} l{112:.0f},{26:.0f}'
                f' l{-8:.0f},{18:.0f} l{-112:.0f},{-26:.0f} Z" fill="#b9c4c9" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1560" y="478" width="150" height="76" rx="22"'
                    f' fill="#e4c85a" {o(5)}/>'
            + f'<path d="M1572,510 h126 M1572,534 h126" stroke="#c9a93c"'
              f' stroke-width="8"/>')
    s += SL(Z_SRED, _kruzhka(1800, 560, 1.2, 6, "#e8eef0", -1))
    # сопутствующие вещи по борту мойки: бутыли, щётка, доска, миски
    for i in range(4):
        bx = 300 + i * 150
        s += SL(Z_SRED, f'<rect x="{bx-34:.0f}" y="{430-i*16:.0f}" width="68"'
                        f' height="{150+i*18:.0f}" rx="16"'
                        f' fill="{["#4e7a52", "#7a5a2c", "#3f5c7a", "#8a4a3c"][i]}"'
                        f' {o(5)}/>'
                f'<rect x="{bx-26:.0f}" y="{454-i*16:.0f}" width="52" height="56"'
                f' rx="6" fill="#efe8d6" opacity=".85"/>')
    s += SL(Z_SRED, f'<path d="M1180,560 L1330,560 L1312,420 L1198,420 Z"'
                    f' fill="url(#dosk)" {o(5)}/>'
            + f'<circle cx="1255" cy="436" r="14" fill="none" stroke="#5b4428"'
              f' stroke-width="7"/>'
            + f'<rect x="1372" y="450" width="58" height="160" rx="12"'
              f' fill="#8a6a44" {o(5)}/>'
            + f'<rect x="1360" y="424" width="82" height="34" rx="10"'
              f' fill="#cfc3a0" {o(4)}/>')
    for i in range(3):
        s += SL(Z_SRED, _tarelka(1500 + i * 130, 980 - i * 26, 104, t, i * .3,
                                 True, 8 - i * 7))
    s += SL(Z_SRED, par(560, 470, t, 4, .4, 190, .34, 1.1))
    s += SL(Z_SRED, _polotence(1716, 120, 250, t, .4, "#dcd4bd", True))
    s += SL(Z_PERED, _stolb_pered(1846, 84, "#19140f", 0, H))
    s += SL(Z_LETIT, _pena_gorka(tcx, tcy - 40, 220, t, 29, 9, 1 - pad))
    s += vinetka(.44)
    return s


def chuzhoy_poryadok_na_polkah(t):
    """Открытые кухонные полки на пол-кадра: чашки ручками влево, тарелки по
    росту, крупы в банках. Гостья с табурета ставит чашки как попало,
    хозяйка смотрит исподлобья. В окне-раздаче настоящее мытьё тарелок."""
    rnd = random.Random(211)
    pol = 962
    s = f'<rect width="{W}" height="{H}" fill="#2d3236"/>'
    s += SL(Z_DAL, _kafel(0, 30, 1020, 520, t, 7, "#d2dadb"))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-8:.0f}" width="{W}" height="{H-pol+8:.0f}"'
                   f' fill="#5a4e42"/>' + _polovik(360, pol + 20, 620, 92))
    # НАСТОЯЩИЙ КАДР в окне-раздаче: сначала рисованный вид, потом метка,
    # потом обвязка поверх (порядок обязателен)
    px, py, pw, ph_ = 1020, 236, 820, 440
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<clipPath id="razd2"><path d="{put}"/></clipPath>'
           f'<g clip-path="url(#razd2)">'
           f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
           f' fill="#4a5258"/>'
           f'<rect x="{px:.0f}" y="{py+ph_*.62:.0f}" width="{pw:.0f}"'
           f' height="{ph_*.38:.0f}" fill="#8a8274"/>')
    for i in range(5):
        vid += (f'<ellipse cx="{px+140+i*140:.0f}" cy="{py+ph_*.58:.0f}" rx="64"'
                f' ry="20" fill="#e7edf0" opacity=".9"/>')
    vid += (f'<circle cx="{px+pw*.5:.0f}" cy="{py+ph_*.3:.0f}" r="86"'
            f' fill="#ffd98a" opacity=".22"/></g>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam")
            + _okno_razdachi(px, py, pw, ph_, t))
    # ПОЛКИ — главный предмет: три доски во всю левую половину
    sdv = A.ease(A.seg(t, .4, 1.2))
    s += SL(Z_SRED, _polki_otkrytye(70, 180, 880, t, 11, 3, True, sdv))
    # чашки, которые гостья уже поставила ручками ВПРАВО
    for i in range(3):
        s += SL(Z_SRED, _kruzhka(250 + i * 150, 174, 1.0, 3 * A.w(t, 2.4, i * .3),
                                 "#efe3d4", 1))
    s += SL(Z_SRED, _banka_krupy(900, 520, 1.1, "#cdb27c")
            + _chaynik(986, 940, 1.1, t))
    # после разведения фигур в середине кадра открылась дыра — закрываю
    # настоящими вещами: рабочий столик с посудой, ящики и связка лука
    s += SL(Z_SRED, _stolik(700, pol - 10, 420, t, 300, False))
    s += SL(Z_SRED, _stopka_tarelok(640, pol - 316, 5, t, 197, 180)
            + _kruzhka(790, pol - 308, 1.0, 0, "#efe3d4", 1)
            + _kastryulya(880, pol - 306, .92, t, True))
    s += SL(Z_SRED, _yaschiki(560, pol + 6, t, 199, 2, .9))
    for i in range(4):
        s += SL(Z_SRED, f'<circle cx="{600+i*52:.0f}" cy="{pol-60:.0f}" r="26"'
                        f' fill="#c9a05a" {o(4)}/>'
                f'<path d="M{600+i*52:.0f},{pol-86:.0f} q8,-18 20,-22"'
                f' fill="none" stroke="#8a7a46" stroke-width="6"/>')
    s += SL(Z_SRED, par(986, 836, t, 4, .4, 170, .34, 1.0))
    # гостья на табурете
    gx, gy, gh = 390, pol + 2, 686
    slez = A.ease(A.seg(t, 2.7, 1.1))
    s += SL(Z_SRED, _tabyret(gx + 8, gy, t, 196, 190))
    _figury_kadra((gx, gy - 196 + 120 * slez, gh), (960, pol + 46, 840))
    gost = figura(gx, gy - 196 + 120 * slez, gh, t, col="#6e4a62",
                  kant="#ffd98a", ph=.3, naklon=-6 + 10 * slez)
    g1, (c1x, c1y), _ = _ruka_mimo(gx, gy - 196 + 120 * slez, gh, 1, gh * .40,
                              -34 + 46 * slez, t, "#6e4a62", "#ffd98a", .3, 5.0)
    g2, (c2x, c2y), _ = _ruka_mimo(gx, gy - 196 + 120 * slez, gh, -1, gh * .36,
                              -26 + 42 * slez, t, "#6e4a62", "#ffd98a", .7, 5.0)
    gost += g1 + g2
    s += SL(Z_SRED, gost)
    s += SL(Z_SRED, _kruzhka(c1x + 20, c1y + 8, .96, 8 * A.w(t, 1.6, .2),
                             "#efe3d4", 1)
            + _kruzhka(c2x - 18, c2y + 10, .9, -6 * A.w(t, 1.9, .5),
                       "#e8eef0", -1))
    # хозяйка: руки скрещены на груди, брови сдвинуты — стоит на полу
    hx, hy, hh = 960, pol + 46, 840
    hoz = figura(hx, hy, hh, t, col="#3a4452", kant="#ffd98a", platok=True,
                 ph=.8, naklon=3.0)
    h1, (d1x, d1y), _ = _ruka_sgib_mimo(hx, hy, hh, 1, hh * .22, 48,
                                        hh * .26, -4, t, "#3a4452", "#ffd98a", .2, 3.0)
    h2, (d2x, d2y), _ = _ruka_sgib_mimo(hx, hy, hh, -1, hh * .22, 52,
                                        hh * .26, -8, t, "#3a4452", "#ffd98a", .6, 3.0)
    hoz += h1 + h2
    hoz += (f'<path d="M{hx-66:.0f},{hy-hh*.54:.0f} L{hx+66:.0f},{hy-hh*.54:.0f}'
            f' L{hx+80:.0f},{hy-hh*.08:.0f} L{hx-80:.0f},{hy-hh*.08:.0f} Z"'
            f' fill="#ded6c0" {o(5)}/>')
    s += SL(Z_SRED, hoz)
    s += SL(Z_SRED, ten(hx, hy + 8, 176, 26, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(c1x, c1y, gh, t, .3) + _varezhka(c2x, c2y, gh, t, .7)
            + _varezhka(d2x, d2y, hh, t, .6))
    s += SL(Z_SRED, _pol_shvy(pol + 10, 1078, 13, 6, "#44382a"))
    # низ кадра
    s += SL(Z_SRED, _dvorovaya_utvar(1180, pol + 86, 420, t, 37,
                                     ["vedro", "korzina", "korob"])
            + _yaschiki(96, pol + 78, t, 9, 2, .76)
            + _kot_zhivoy(1686, pol + 66, t, .98, "#3f3a34", .2)
            + kartoshka(1000, pol + 96, t, 7, 6, 1.0))
    s += SL(Z_PERED, _stolb_pered(1874, 72, "#191410", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 0, 5, .0, .0) + _pena_gorka(1380, 700, 60, t, 43, 4, .5))
    s += vinetka(.42)
    return s


def gostya_v_kresle(t):
    """Комната хозяйки: мягкое кресло на пол-кадра, торшер, столик с пирогом
    и чашками, ковёр. Гостья упёрлась руками в подлокотники и порывается
    встать, хозяйка усаживает её и подаёт чашку на блюдце."""
    rnd = random.Random(213)
    pol = 952
    s = f'<rect width="{W}" height="{H}" fill="#2b2622"/>'
    s += SL(Z_DAL, doski(0, 0, 1180, pol, 96, True, "dosk"))
    s += SL(Z_DAL, doski(1180, 0, 740, pol, 96, True, "dosk"))
    s += SL(Z_DAL, _kover_na_stene(1040, 128, 1060, 520, t, 5))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-14:.0f}" width="{W}" height="{H-pol+14:.0f}"'
                   f' fill="#6a5440"/>' + _polovik(520, pol + 16, 860, 118))
    s += SL(Z_DAL, _polka_s_utvaryu(80, 268, 540, t, 23, 4))
    s += SL(Z_DAL, _knizhnaya_polka(96, 440, 560, t, 19, 2, 196))
    s += SL(Z_DAL, _ramki_na_stene(640, 150, 420, t, 11, 3))
    # торшер — тёплое пятно сцены
    s += SL(Z_SRED, lampa(1468, 712, t, 1.25, True))
    s += SL(Z_SRED, f'<rect x="1452" y="712" width="32" height="236" rx="12"'
                    f' fill="#4a3c30" {o(5)}/>'
            + f'<ellipse cx="1468" cy="950" rx="88" ry="22" fill="#3f342a" {o(4)}/>')
    # КРЕСЛО — главный предмет
    # КРЕСЛО, А НЕ ДИВАН: 580 px ширины читались диваном — ставим 400 при
    # более высокой спинке
    # 400 px всё ещё читались диваном (ширина 2,9 подола сидящей) — 270
    s += SL(Z_SRED, _kreslo(700, pol, 270, t, 520, "#6c5a4a"))
    # столик с пирогом и чашками
    s += SL(Z_SRED, _stolik(1210, pol, 420, t, 220, False))
    s += SL(Z_SRED, _pirog(1178, pol - 224, .92, t, True)
            + _kruzhka(1346, pol - 216, 1.0, 0, "#f0eade", 1)
            + _kruzhka(1414, pol - 214, .92, 0, "#e8dcc8", -1))
    s += SL(Z_SRED, par(1352, pol - 300, t, 4, .46, 160, .4, .9))
    # гостья в кресле: привстаёт и садится обратно
    vst = A.ease(A.seg(t, .3, .9)) * (1 - A.ease(A.seg(t, 1.6, 1.0)))
    gx, gy, gh = 712, pol - 150 - 58 * vst, 430 + 60 * vst
    _figury_kadra((gx, gy, gh), (1046, pol + 30, 800))
    gost = figura(gx, gy, gh, t, col="#6a3a4a", kant="#ffd98a", platok=True,
                  ph=.3, naklon=-5 + 7 * vst)
    g1, (a1x, a1y), _ = _ruka_mimo(gx, gy, gh, 1, gh * .50, 56 - 22 * vst, t,
                              "#6a3a4a", "#ffd98a", .3, 4.0)
    g2, (a2x, a2y), _ = _ruka_mimo(gx, gy, gh, -1, gh * .50, 58 - 20 * vst, t,
                              "#6a3a4a", "#ffd98a", .7, 4.0)
    gost += g1 + g2
    s += SL(Z_SRED, gost)
    # подушка под спину ложится по ходу плана
    pod = A.ease(A.seg(t, 1.9, .8))
    s += SL(Z_SRED, f'<path d="M{gx-120:.0f},{gy-gh*.56-30*pod:.0f}'
                    f' q{120:.0f},{-54:.0f} {240:.0f},0 q{20:.0f},{70:.0f}'
                    f' {-10:.0f},{104:.0f} q{-116:.0f},{34:.0f} {-230:.0f},0'
                    f' q{-26:.0f},{-44:.0f} {0:.0f},{-104:.0f} Z"'
                    f' fill="#c9a05a" {o(5)} opacity="{.2+.8*pod:.2f}"/>')
    # хозяйка перед гостьей: обе ладони на плечах, потом чашка на блюдце
    hx, hy, hh = 1046, pol + 30, 800
    hoz = figura(hx, hy, hh, t, col="#3f4a58", kant="#ffd98a", ph=.8, naklon=-4.0)
    h1, (p1x, p1y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .40, 24 + 12 * pod, t,
                              "#3f4a58", "#ffd98a", .8, 4.0)
    h2, (p2x, p2y), _ = _ruka_sgib_mimo(hx, hy, hh, -1, hh * .24, 44,
                                        hh * .24, 8, t, "#3f4a58", "#ffd98a", .2, 4.0)
    hoz += h1 + h2
    s += SL(Z_SRED, hoz)
    # чашка на блюдце переходит в руки гостьи
    per = A.ease(A.seg(t, 2.6, 1.1))
    # чашка доходит ДО САМОЙ РУКИ гостьи и остаётся в ней
    chx = p1x + (a1x - p1x) * per
    chy = p1y + (a1y - p1y) * per
    s += SL(Z_SRED, f'<ellipse cx="{chx:.0f}" cy="{chy+56:.0f}" rx="52" ry="16"'
                    f' fill="#f2ece0" {o(4)}/>'
            + _kruzhka(chx, chy + 50, .86, 4 * A.w(t, 1.8, .2), "#f6f0e4", 1))
    s += SL(Z_SRED, par(chx, chy - 20, t, 3, .4, 120, .44, .8))
    s += SL(Z_SRED, ten(hx, hy + 8, 180, 26, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(a1x, a1y, gh, t, .3) + ""
            + _varezhka(p2x, p2y, hh, t, .2))
    s += SL(Z_SRED, _konus_sveta(1468, 700, 560, 300, -12, .38))
    s += SL(Z_SRED, _pol_shvy(pol + 14, 1078, 17, 6, "#4a3a28"))
    # низ кадра: тапки, корзина с клубками, кот на половике
    s += SL(Z_SRED, _valenki_u_dveri(360, pol + 70, .9, t)
            + _dvorovaya_utvar(120, pol + 92, 420, t, 41,
                               ["korzina", "korob", "vedro"])
            + _kot_zhivoy(1690, pol + 74, t, 1.1, "#4a423c", .4, True, True)
            + kartoshka(1540, pol + 96, t, 5, 6, .9))
    # пуфик, корзина с клубками и фикус в кадке у кресла
    s += SL(Z_SRED, f'<ellipse cx="420" cy="{pol-70:.0f}" rx="118" ry="74"'
                    f' fill="#7a5a4a" {o(6)}/>'
            + f'<ellipse cx="420" cy="{pol-96:.0f}" rx="104" ry="52"'
              f' fill="#8c6a56" opacity=".9"/>'
            + f'<rect x="402" y="{pol-30:.0f}" width="36" height="34" rx="10"'
              f' fill="#4a3c30" {o(4)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{232+i*42:.0f}" cy="{pol-44-(i%2)*30:.0f}"'
                        f' r="{30+(i%3)*8:.0f}"'
                        f' fill="{["#7a3a42", "#3f5c7a", "#8a6a2c", "#4a6a48", "#9c5a3c"][i]}"'
                        f' {o(4)}/>'
                f'<path d="M{232+i*42:.0f},{pol-44-(i%2)*30:.0f} q22,-14 40,4"'
                f' fill="none" stroke="#efe8d6" stroke-width="5" opacity=".7"/>')
    s += SL(Z_SRED, teplo(1468, 740, 560, 460, .44))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += SL(Z_LETIT, iskra_let(t, 1468, 712, 5, 7, 180, .3))
    s += vinetka(.42)
    return s


def za_stolom_u_docheri(t):
    """Современная кухня-столовая после обеда: круглый стол, пустые тарелки,
    салатник, хлебница, ваза с яблоками. Мать сидит с руками на коленях,
    дочь собирает тарелки в стопку, внук протягивает бабушке яблоко."""
    rnd = random.Random(217)
    pol = 968
    s = f'<rect width="{W}" height="{H}" fill="#2e3338"/>'
    s += SL(Z_DAL, _kafel(0, 20, 980, 420, t, 11, "#d8dedd"))
    s += SL(Z_DAL, f'<rect x="980" y="20" width="940" height="560" rx="10"'
                   f' fill="#9aa3a8" {o(6)}/>')
    s += SL(Z_DAL, _polki_otkrytye(1040, 120, 760, t, 29, 2, True, .0))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-10:.0f}" width="{W}" height="{H-pol+10:.0f}"'
                   f' fill="#7a6a56"/>' + _polovik(500, pol + 22, 900, 96,
                                                   "#cfc0a4", "#8a7a5c"))
    s += SL(Z_DAL, tusklaya_lampochka(960, 180, t, 1.25, True))
    # КРУГЛЫЙ СТОЛ — главный предмет
    sx, sy, sw = 960, pol - 258, 1180
    s += SL(Z_SRED, f'{ten(sx, pol + 4, 440, 26, .5)}'
                    f'<ellipse cx="{sx:.0f}" cy="{sy:.0f}" rx="{sw/2:.0f}" ry="162"'
                    f' fill="url(#derev)" {o(7)}/>'
            + f'<ellipse cx="{sx:.0f}" cy="{sy-18:.0f}" rx="{sw/2-26:.0f}" ry="138"'
              f' fill="#a9825a" opacity=".85"/>'
            + f'<rect x="{sx-58:.0f}" y="{sy+120:.0f}" width="116" height="150" rx="14"'
              f' fill="#6a5030" {o(5)}/>'
            + f'<ellipse cx="{sx:.0f}" cy="{pol-6:.0f}" rx="210" ry="40"'
              f' fill="#5b4428" {o(5)}/>')
    # посуда на столе: пустые тарелки, салатник, хлебница
    for i in range(4):
        s += SL(Z_SRED, _tarelka(600 + i * 208, sy - 24 + (i % 2) * 18, 86, t,
                                 i * .2, False, -8 + i * 5))
    s += SL(Z_SRED, f'<path d="M1180,{sy-40:.0f} q86,-30 172,0 q-16,70 -86,76'
                    f' q-70,-6 -86,-76 Z" fill="url(#stekl)" opacity=".9" {o(5)}/>'
            + f'<ellipse cx="1266" cy="{sy-44:.0f}" rx="86" ry="22" fill="#9cc06a"'
              f' opacity=".85"/>')
    s += SL(Z_SRED, f'<rect x="420" y="{sy-96:.0f}" width="230" height="86" rx="18"'
                    f' fill="url(#solom)" {o(5)}/>'
            + f'<path d="M430,{sy-96:.0f} q114,-44 210,0" fill="none"'
              f' stroke="#8a6a3c" stroke-width="9"/>'
            + karavay(530, sy - 92, .54, False))
    s += SL(Z_SRED, _vaza_s_yablokami(930, sy - 40, 1.0, t, 9, 7))
    # дочь слева: обеими руками собирает тарелки в стопку
    dx, dy_, dh = 408, pol + 40, 804
    sob = A.ease(A.seg(t, .4, 1.4))
    _figury_kadra((408, pol + 40, 804), (1390, pol - 118, 470),
                  (1680, pol - 92, 420))
    doch = figura(dx, dy_, dh, t, col="#46586a", kant="#ffd98a", ph=.2, naklon=6.0)
    d1, (e1x, e1y), _ = _ruka_mimo(dx, dy_, dh, 1, dh * .42, 40 - 16 * sob, t,
                              "#46586a", "#ffd98a", .2, 5.0)
    d2, (e2x, e2y), _ = _ruka_mimo(dx, dy_, dh, 1, dh * .34, 62 - 14 * sob, t,
                              "#46586a", "#ffd98a", .6, 4.0)
    doch += d1 + d2
    s += SL(Z_SRED, doch)
    s += SL(Z_SRED, _stopka_tarelok(e1x + 44, e1y - 10 - 40 * sob,
                                    2 + int(4 * sob), t, 53, 172))
    # мать в нарядной кофте: сидит, обе руки на коленях
    mx, my, mh = 1390, pol - 118, 470
    s += SL(Z_SRED, _venskiy_stul(1404, pol + 6, 520, t, 2.0, True))
    mat = figura(mx, my, mh, t, col="#7a4a5e", kant="#ffd98a", platok=True,
                 ph=.6, naklon=-3.0)
    m1, (f1x, f1y), _ = _ruka_mimo(mx, my, mh, -1, mh * .46, 64, t,
                              "#7a4a5e", "#ffd98a", .6, 3.0)
    m2, (f2x, f2y), _ = _ruka_mimo(mx, my, mh, 1, mh * .44, 68, t,
                              "#7a4a5e", "#ffd98a", .2, 3.0)
    mat += m1 + m2
    s += SL(Z_SRED, mat)
    # внук рядом: правой протягивает яблоко бабушке, левой держит своё
    vx, vy, vh = 1680, pol - 92, 420
    s += SL(Z_SRED, _tabyret(1694, pol + 8, t, 190, 170))
    vnuk = figura(vx, vy, vh, t, col="#4a6a58", kant="#ffd98a", ph=.9, naklon=5.0)
    v1, (y1x, y1y), _ = _ruka_mimo(vx, vy, vh, -1, vh * .52, 18, t,
                              "#4a6a58", "#ffd98a", .9, 5.0)
    v2, (y2x, y2y), _ = _ruka_mimo(vx, vy, vh, 1, vh * .34, 54, t,
                              "#4a6a58", "#ffd98a", .4, 4.0)
    vnuk += v1 + v2
    s += SL(Z_SRED, vnuk)
    per = A.ease(A.seg(t, 2.2, 1.3))
    ayx = y1x + (f1x - y1x) * per
    ayy = y1y + (f1y - y1y) * per
    s += SL(Z_SRED, f'<circle cx="{ayx:.0f}" cy="{ayy:.0f}" r="34"'
                    f' fill="#b8352c" {o(5)}/>'
            + f'<path d="M{ayx+4:.0f},{ayy-34:.0f} q8,-18 22,-20" fill="none"'
              f' stroke="#4e3418" stroke-width="6"/>'
            + f'<circle cx="{ayx-12:.0f}" cy="{ayy-12:.0f}" r="8" fill="#ffe6c8"'
              f' opacity=".55"/>')
    s += SL(Z_SRED, f'<circle cx="{y2x+10:.0f}" cy="{y2y+14:.0f}" r="30"'
                    f' fill="#c9772c" {o(5)}/>'
            + f'<path d="M{y2x+68:.0f},{y2y-6:.0f} a30,30 0 0 0 -56,8"'
              f' fill="none" stroke="#e8c8a0" stroke-width="7"/>')
    s += SL(Z_SRED, ten(dx, dy_ + 8, 176, 26, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(e1x, e1y, dh, t, .2) + ""
            + _varezhka(f1x, f1y, mh, t, .6) + ""
            + _varezhka(y1x, y1y, vh, t, .9) + _varezhka(y2x, y2y, vh, t, .4))
    s += SL(Z_SRED, _pol_shvy(pol + 10, 1078, 19, 6, "#5a4a36"))
    # низ кадра
    s += SL(Z_SRED, _gorodskoy_hlam(120, pol + 96, 340, t, 7, ["yaschik", "korobka"])
            + _kot_zhivoy(1010, pol + 84, t, 1.05, "#453e38", .7)
            + _valenki_u_dveri(1860, pol + 72, .8, t))
    s += SL(Z_PERED, _stolb_pered(-6, 96, "#1b1612", 0, H))
    s += SL(Z_LETIT, par(1266, sy - 130, t, 3, .3, 130, .3, .9))
    s += vinetka(.40)
    return s


def babushka_na_kraeshke_stula(t):
    """Гостиная шестидесятых: сервант с хрусталём, стол под кружевной
    скатертью, венский стул на пол-кадра. Бабушка сидит на самом краешке
    с сумочкой на коленях, хозяйка выносит супницу и приглашает к столу."""
    rnd = random.Random(223)
    pol = 958
    s = f'<rect width="{W}" height="{H}" fill="#2c2722"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="1100" height="{pol:.0f}"'
                   f' fill="#8a7a62"/>')
    for i in range(11):
        s += SL(Z_DAL, f'<rect x="{i*100:.0f}" y="0" width="54" height="{pol:.0f}"'
                       f' fill="#9a8a70" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect x="1100" y="0" width="820" height="{pol:.0f}"'
                   f' fill="#7e6f58"/>')
    s += SL(Z_DAL, _kover_na_stene(1120, 128, 660, 430, t, 13))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}" height="{H-pol+16:.0f}"'
                   f' fill="#6e5640"/>' + _polovik(430, pol + 18, 1000, 120))
    s += SL(Z_DAL, hodiki(190, 300, t, 1.3))
    s += SL(Z_DAL, _knizhnaya_polka(60, 560, 520, t, 23, 2, 200))
    s += SL(Z_DAL, _ramki_na_stene(520, 150, 540, t, 29, 4))
    s += SL(Z_DAL, tusklaya_lampochka(960, 150, t, 1.15, True))
    # СЕРВАНТ С ХРУСТАЛЁМ — главный предмет
    s += SL(Z_SRED, _servant_hrustal(1140, pol, 660, 700, t, 3))
    # стол под кружевной скатертью
    s += SL(Z_SRED, f'{ten(760, pol + 6, 330, 22, .5)}'
                    f'<rect x="430" y="{pol-268:.0f}" width="680" height="34" rx="10"'
                    f' fill="url(#derev)" {o(7)}/>'
            + f'<path d="M444,{pol-234:.0f} L1096,{pol-234:.0f} L1056,{pol-96:.0f}'
              f' L484,{pol-96:.0f} Z" fill="#f2ece0" {o(5)}/>')
    for i in range(12):
        s += SL(Z_SRED, f'<circle cx="{486+i*52:.0f}" cy="{pol-92:.0f}" r="15"'
                        f' fill="none" stroke="#e0d6bd" stroke-width="5"/>')
    for i in (0, 1):
        s += SL(Z_SRED, f'<rect x="{480+i*560:.0f}" y="{pol-234:.0f}" width="30"'
                        f' height="138" fill="url(#derev)" {o(5)}/>')
    # супница встаёт на стол
    pst = A.ease(A.seg(t, 1.1, 1.0))
    s += SL(Z_SRED, _supnica(770, pol - 244 - 120 * (1 - pst), 1.05, t))
    s += SL(Z_SRED, par(770, pol - 330 - 120 * (1 - pst), t, 4, .5, 170, .42, 1.0))
    for i in range(3):
        s += SL(Z_SRED, _kruzhka(560 + i * 150, pol - 246, .8, 0, "#f2ece0", 1))
    # венский стул и бабушка на самом краешке
    sx2 = 380
    s += SL(Z_SRED, _venskiy_stul(sx2, pol + 4, 560, t, -2.0, True))
    bst = A.ease(A.seg(t, 3.4, 1.1))
    # САЖАЕМ НА СИДЕНЬЕ: уровень сиденья венского стула = pol+4 - 560*.52
    bx, by_, bh = sx2 - 50, pol - 287 + 36 - 112 * bst, 430 + 330 * bst
    _figury_kadra((bx, by_, bh), (1004, pol + 40, 800))
    bab = figura(bx, by_, bh, t, col="#4e4a58", kant="#ffd98a", platok=True,
                 ph=.4, naklon=-2.0)
    b1, (s1x, s1y), _ = _ruka_mimo(bx, by_, bh, 1, bh * .40, 62 - 20 * bst, t,
                              "#4e4a58", "#ffd98a", .4, 3.0)
    b2, (s2x, s2y), _ = _ruka_mimo(bx, by_, bh, -1, bh * .40, 64 - 18 * bst, t,
                              "#4e4a58", "#ffd98a", .8, 3.0)
    bab += b1 + b2
    # брошь на груди
    bab += (f'<circle cx="{bx+36:.0f}" cy="{by_-bh*.56:.0f}" r="15"'
            f' fill="url(#zol)" {o(3)}/>'
            f'<circle cx="{bx+36:.0f}" cy="{by_-bh*.56:.0f}" r="6" fill="#d6452a"/>')
    s += SL(Z_SRED, bab)
    # сумочка на коленях
    # СУМОЧКА НОРМАЛЬНОГО РАЗМЕРА В ОДНОЙ РУКЕ. Задание просит «обе руки
    # держат сумочку», но `_ruka` разводит кисти наружу от оси тела, и на
    # 316 px между кистями сумочка превращалась в чемодан. Держит левая
    # (её варежка перекрывает сумочку), правая лежит на колене без кисти.
    sux, suy, sw_ = s2x + 26, s2y + 10, 178.0
    s += SL(Z_SRED, f'<rect x="{sux-sw_/2:.0f}" y="{suy-30:.0f}"'
                    f' width="{sw_:.0f}" height="104" rx="14" fill="#5a3a2c" {o(5)}/>'
            + f'<path d="M{sux-sw_*.28:.0f},{suy-30:.0f}'
              f' q{sw_*.28:.0f},-54 {sw_*.56:.0f},0" fill="none" stroke="#5a3a2c"'
              f' stroke-width="11"/>'
            + f'<rect x="{sux-18:.0f}" y="{suy-16:.0f}" width="36"'
              f' height="22" rx="6" fill="url(#zol)" {o(2)}/>'
            + f'<path d="M{sux-sw_*.42:.0f},{suy+30:.0f} q{sw_*.42:.0f},18'
              f' {sw_*.84:.0f},0" fill="none" stroke="#7d5a3c" stroke-width="7"/>')
    # хозяйка в переднике: приглашающий жест правой рукой
    hx, hy, hh = 1004, pol + 40, 800
    hoz = figura(hx, hy, hh, t, col="#3a4a44", kant="#ffd98a", ph=.9, naklon=4.0)
    zh = A.ease(A.seg(t, 2.4, 1.0))
    h1, (g1x, g1y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .44, 34 - 54 * zh, t,
                              "#3a4a44", "#ffd98a", .9, 5.0)
    h2, (g2x, g2y), _ = _ruka_mimo(hx, hy, hh, 1, hh * .30, 56, t,
                              "#3a4a44", "#ffd98a", .3, 4.0)
    hoz += h1 + h2
    hoz += (f'<path d="M{hx-62:.0f},{hy-hh*.52:.0f} L{hx+62:.0f},{hy-hh*.52:.0f}'
            f' L{hx+76:.0f},{hy-hh*.08:.0f} L{hx-76:.0f},{hy-hh*.08:.0f} Z"'
            f' fill="#e8e0ca" {o(5)}/>')
    s += SL(Z_SRED, hoz)
    s += SL(Z_SRED, ten(hx, hy + 8, 178, 26, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(s2x + 20, s2y + 6, bh, t, .8)
            + _varezhka(g1x, g1y, hh, t, .9))
    s += SL(Z_SRED, _pol_shvy(pol + 16, 1078, 23, 6, "#503c28"))
    # низ кадра
    s += SL(Z_SRED, _gorodskoy_hlam(96, pol + 92, 460, t, 11,
                                    ["korobka", "kust", "yaschik"])
            + _kot_zhivoy(1760, pol + 78, t, 1.05, "#3e3934", .5)
            + _valenki_u_dveri(1480, pol + 86, .82, t)
            + kartoshka(1230, pol + 96, t, 5, 6, .85))
    # ещё хрусталь: ваза с конфетами на столе, рюмки, графин и этажерка
    s += SL(Z_SRED, f'<path d="M620,{pol-246:.0f} q46,46 92,0 l-10,-56 h-72 Z"'
                    f' fill="#dbeaf4" opacity=".9" {o(4)}/>'
            + f'<ellipse cx="666" cy="{pol-300:.0f}" rx="52" ry="16"'
              f' fill="#cfe0ea" {o(3)}/>'
            + f'<path d="M940,{pol-240:.0f} q-16,-96 34,-130 q50,34 34,130 Z"'
              f' fill="#e2eef6" opacity=".92" {o(5)}/>'
            + f'<rect x="952" y="{pol-394:.0f}" width="44" height="30" rx="8"'
              f' fill="#cfe0ea" {o(3)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{846+i*54:.0f},{pol-240:.0f}'
                        f' l24,0 l-4,-34 l6,-30 l-28,0 l6,30 Z"'
                        f' fill="#dbeaf4" opacity=".9" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1832" y="{pol-520:.0f}" width="88" height="520"'
                    f' rx="8" fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="1826" y="{pol-460+i*160:.0f}" width="100"'
                        f' height="18" rx="6" fill="#6a5030" {o(4)}/>'
                f'<circle cx="1876" cy="{pol-480+i*160:.0f}" r="26"'
                f' fill="#8a9a58" opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, teplo(960, 240, 520, 340, .46))
    s += SL(Z_PERED, ramka_pp("pravo"))
    s += SL(Z_LETIT, iskra_let(t, 960, 190, 5, 9, 160, .26))
    s += vinetka(.42)
    return s


def syad_ya_sama(t):
    """Кухня у мойки: гость в жилете вскочил из-за стола с тарелкой и
    прибором, хозяйка забирает у него тарелку левой рукой и указывает
    правой на стул. На столе чайник, варенье, сахарница."""
    rnd = random.Random(227)
    pol = 972
    s = f'<rect width="{W}" height="{H}" fill="#2d3135"/>'
    s += SL(Z_DAL, _kafel(760, 40, 1160, 520, t, 17, "#d0d9d9"))
    s += SL(Z_DAL, doski(0, 0, 760, pol, 92, True, "dosk"))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-8:.0f}" width="{W}" height="{H-pol+8:.0f}"'
                   f' fill="#60513f"/>' + _polovik(640, pol + 20, 760, 92))
    s += SL(Z_DAL, _polka_s_utvaryu(70, 244, 600, t, 31, 5))
    s += SL(Z_DAL, tusklaya_lampochka(1340, 170, t, 1.1, True))
    # мойка справа — главный предмет
    s += SL(Z_SRED, _moyka(900, 600, 1000, t, 19, True, .4))
    s += SL(Z_SRED, _stopka_tarelok(1760, 588, 5, t, 59, 176))
    s += SL(Z_SRED, _polotence(1858, 400, 210, t, .6, "#ded6bd", True))
    # стол слева: чайник, варенье в розетке, сахарница
    s += SL(Z_SRED, stol(70, pol - 300, 700, 36, True))
    s += SL(Z_SRED, _chaynik(220, pol - 302, 1.15, t)
            + _kruzhka(400, pol - 300, .95, 0, "#efe3d4", 1)
            + f'<path d="M520,{pol-302:.0f} q44,-26 88,0 q-10,44 -44,48'
              f' q-34,-4 -44,-48 Z" fill="#9c2f28" {o(5)}/>'
            + f'<ellipse cx="564" cy="{pol-302:.0f}" rx="44" ry="13"'
              f' fill="#c24a3a" opacity=".9"/>'
            + f'<rect x="640" y="{pol-358:.0f}" width="96" height="60" rx="12"'
              f' fill="#f0eade" {o(5)}/>'
            + f'<ellipse cx="688" cy="{pol-358:.0f}" rx="48" ry="14"'
              f' fill="#dcd4c4" {o(4)}/>')
    s += SL(Z_SRED, par(220, pol - 410, t, 4, .46, 180, .4, 1.0))
    # гость вскочил: правая нога шагнула к мойке
    sht = A.ease(A.seg(t, .3, 1.0))
    sad = A.ease(A.seg(t, 2.6, 1.2))
    gx = 620 + 150 * sht - 130 * sad
    gy, gh = pol + 36 - 80 * (1 - sad) * 0, 790 - 240 * sad
    _figury_kadra((gx, pol + 36 - 150 * sad, gh), (1180, pol + 44, 814))
    gost = figura(gx, pol + 36 - 150 * sad, gh, t, col="#4a4a56", kant="#ffd98a",
                  boroda=True, ph=.2, naklon=7 - 10 * sad)
    g1, (t1x, t1y), _ = _ruka_mimo(gx, pol + 36 - 150 * sad, gh, 1, gh * .44,
                              22 + 24 * sad, t, "#4a4a56", "#ffd98a", .2, 5.0)
    g2, (t2x, t2y), _ = _ruka_mimo(gx, pol + 36 - 150 * sad, gh, -1, gh * .36,
                              34 + 20 * sad, t, "#4a4a56", "#ffd98a", .6, 5.0)
    gost += g1 + g2
    # жилет поверх рубахи
    gost += (f'<path d="M{gx-54:.0f},{pol+36-150*sad-gh*.58:.0f}'
             f' L{gx-18:.0f},{pol+36-150*sad-gh*.56:.0f}'
             f' L{gx-24:.0f},{pol+36-150*sad-gh*.18:.0f}'
             f' L{gx-62:.0f},{pol+36-150*sad-gh*.20:.0f} Z" fill="#33333d" {o(4)}/>'
             f'<path d="M{gx+54:.0f},{pol+36-150*sad-gh*.58:.0f}'
             f' L{gx+18:.0f},{pol+36-150*sad-gh*.56:.0f}'
             f' L{gx+24:.0f},{pol+36-150*sad-gh*.18:.0f}'
             f' L{gx+62:.0f},{pol+36-150*sad-gh*.20:.0f} Z" fill="#33333d" {o(4)}/>')
    s += SL(Z_SRED, gost)
    # хозяйка у мойки: левая забирает тарелку, правая указывает на стул
    hx, hy, hh = 1180, pol + 44, 814
    hoz = figura(hx, hy, hh, t, col="#3f4a58", kant="#ffd98a", platok=True,
                 ph=.7, naklon=-3.0)
    h1, (z1x, z1y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .44, 30, t,
                              "#3f4a58", "#ffd98a", .7, 5.0)
    h2, (z2x, z2y), _ = _ruka_mimo(hx, hy, hh, 1, hh * .42, 18 + 34 * sad, t,
                              "#3f4a58", "#ffd98a", .3, 4.0)
    hoz += h1 + h2
    s += SL(Z_SRED, hoz)
    # тарелка переходит из руки гостя в руку хозяйки
    per = A.ease(A.seg(t, 1.5, 1.1))
    pxx = t1x + (z1x - t1x) * per
    pyy = t1y + (z1y - t1y) * per
    s += SL(Z_SRED, _tarelka(pxx, pyy, 78, t, .2, False, -10 + 12 * per))
    # вилка и нож в левой руке гостя
    s += SL(Z_SRED, f'<g transform="rotate({-18 + 4 * A.w(t, 2.0, .3):.1f}'
                    f' {t2x:.0f} {t2y:.0f})">'
                    f'<rect x="{t2x-8:.0f}" y="{t2y-96:.0f}" width="16" height="106"'
                    f' rx="6" fill="#b9c4c9" {o(3)}/>'
            + f'<rect x="{t2x+18:.0f}" y="{t2y-88:.0f}" width="14" height="98" rx="6"'
              f' fill="#cfd8dc" {o(3)}/></g>')
    # стул, на который указывают и куда гость садится
    s += SL(Z_SRED, _venskiy_stul(448, pol + 6, 540, t, 1.5, False))
    s += SL(Z_SRED, ten(hx, hy + 8, 180, 26, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(t2x, t2y, gh, t, .6)
            + _varezhka(z1x, z1y, hh, t, .7) + _varezhka(z2x, z2y, hh, t, .3))
    s += SL(Z_SRED, _pol_shvy(pol + 10, 1078, 29, 6, "#463a2c"))
    # низ кадра
    s += SL(Z_SRED, _dvorovaya_utvar(1560, pol + 84, 340, t, 43, ["vedro", "korob"])
            + _yaschiki(70, pol + 80, t, 13, 2, .78)
            + _kot_zhivoy(880, pol + 70, t, 1.0, "#423b35", .9)
            + kartoshka(1400, pol + 96, t, 6, 6, .95))
    s += SL(Z_PERED, _stolb_pered(1870, 76, "#191310", 0, H))
    s += SL(Z_LETIT, _pena_gorka(1260, 700, 70, t, 61, 5, .4))
    s += vinetka(.42)
    return s


def pero_nad_bumagoy(t):
    """Письменный стол: лист с пустой строкой внизу, чернильница,
    пресс-папье, очки, свеча. Видна правая рука до локтя: держит перо над
    строкой, капля набухает на кончике, потом перо уходит в чернильницу."""
    rnd = random.Random(229)
    s = f'<rect width="{W}" height="{H}" fill="#1d1a16"/>'
    s += SL(Z_DAL, doski(0, 0, 1240, 690, 104, True, "dosk"))
    s += SL(Z_DAL, doski(1240, 0, 680, 690, 104, True, "dosk"))
    s += SL(Z_DAL, _polka_s_utvaryu(1300, 232, 560, t, 37, 4))
    s += SL(Z_DAL, _knizhnaya_polka(130, 300, 740, t, 41, 2, 206))
    s += SL(Z_DAL, _ramki_na_stene(950, 120, 330, t, 43, 2))
    s += SL(Z_DAL, f'<rect x="0" y="672" width="{W}" height="36" rx="8"'
                   f' fill="#4a3522" {o(5)}/>')
    # СТОЛ — главный предмет
    s += SL(Z_SRED, _pismennyy_stol(300, H + 60, 1340, t, 420))
    stol_y = H + 60 - 420
    # свеча — единственное тёплое пятно
    s += SL(Z_SRED, f'<rect x="1398" y="{stol_y-34:.0f}" width="86" height="34"'
                    f' rx="12" fill="url(#zhel)" {o(5)}/>')
    s += SL(Z_SRED, svecha(1440, stol_y - 150, t, .2, 1.5, 120))
    # лист бумаги с пустой строкой
    s += SL(Z_SRED, _list_bumagi(620, stol_y - 26, 560, 330, t, -3.0, 5, True))
    # чернильница, пресс-папье, очки, песочница
    s += SL(Z_SRED, _chernilnica(1260, stol_y - 10, 1.5, t))
    s += SL(Z_SRED, f'<path d="M418,{stol_y-10:.0f} q86,-74 172,0 Z"'
                    f' fill="#6a5030" {o(6)}/>'
            + f'<rect x="400" y="{stol_y-16:.0f}" width="208" height="22" rx="8"'
              f' fill="#8a6a44" {o(5)}/>'
            + f'<rect x="478" y="{stol_y-106:.0f}" width="52" height="40" rx="10"'
              f' fill="url(#zhel)" {o(4)}/>')
    s += SL(Z_SRED, _ochki(390, stol_y - 148, 1.25, t))
    # свитки, папки и стакан с ручками — обжитой стол конторщика
    s += SL(Z_SRED, _svitki_i_papki(640, stol_y - 14, t, 5, 4))
    s += SL(Z_SRED, f'<path d="M1556,{stol_y-10:.0f} L1664,{stol_y-10:.0f}'
                    f' L1652,{stol_y-128:.0f} L1568,{stol_y-128:.0f} Z"'
                    f' fill="#5e676e" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{1584+i*20:.0f}" y1="{stol_y-120:.0f}"'
                        f' x2="{1572+i*26:.0f}" y2="{stol_y-250-i*14:.0f}"'
                        f' stroke="{["#8a6a44","#6a5030","#9c7a4c","#7b5c38","#5b4428"][i]}"'
                        f' stroke-width="13" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<ellipse cx="1140" cy="{stol_y-16:.0f}" rx="72" ry="20"'
                    f' fill="#b9a988" {o(4)}/>'
            + f'<path d="M1082,{stol_y-24:.0f} q58,-40 116,0" fill="none"'
              f' stroke="#cdbf9c" stroke-width="10"/>')
    # ПРАВАЯ РУКА ДО ЛОКТЯ — ничья: человека в кадре нет
    otv = A.ease(A.seg(t, 1.3, 1.2))
    kist_x = 980 + (1260 - 980) * otv
    kist_y = stol_y - 230 + 180 * otv
    # предплечье лежит НА СТОЛЕШНИЦЕ: от правого края кадра к листу, и
    # опора видна — манжета на доске (осмотр порции 2: перо висело в воздухе)
    ruk, (ex, ey) = rukav(1900, stol_y + 120, 700, -168 + 14 * otv, t,
                          "#4a4450", "#ffd98a", .2, 3.0, True)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<rect x="{ex+30:.0f}" y="{ey+6:.0f}" width="170" height="52"'
                    f' rx="20" fill="#4a4450" {o(5)}/>'
            + f'<path d="M{ex+40:.0f},{ey+16:.0f} q80,18 150,6" fill="none"'
              f' stroke="#f2e4d0" stroke-width="9" opacity=".7"/>'
            + ten(ex + 90, stol_y - 8, 130, 18, .45))
    # перо в кисти: висит над пустой строкой, капля набухает
    kap = .3 + .7 * abs(A.w(t, 1.9, .1)) * (1 - otv)
    # перо: кончик стоит над пустой строкой листа, потом уходит в чернильницу
    perx = ex + 6 + (1260 - ex - 6) * otv
    pery = ey + 6 + (stol_y - 60 - ey - 6) * otv
    s += SL(Z_SRED, _pero_pisma(perx, pery, t, 1.3, -26 + 22 * otv, kap))
    s += SL(Z_SRED, _varezhka(perx - 4, pery - 8, 760, t, .2))
    s += SL(Z_SRED, ten(perx + 10, stol_y - 14, 110, 20, .4))
    s += SL(Z_SRED, _konus_sveta(1440, stol_y - 180, 620, 330, 8, .42))
    s += SL(Z_SRED, _pol_shvy(730, 1070, 31, 6, "#3a2a1a"))
    # нижняя треть: сундучок, корзина с бумагами, кот, ведро для бумаг
    s += SL(Z_PERED, _yaschiki(96, 1072, t, 17, 2, .92)
            + _dvorovaya_utvar(1560, 1066, 340, t, 47, ["korzina", "korob"])
            + _kot_zhivoy(1340, 1060, t, 1.15, "#3a332e", .4, True, True))
    s += SL(Z_SRED, teplo(1440, stol_y - 180, 520, 430, .42))
    s += SL(Z_PERED, _stolb_pered(-8, 104, "#140f0c", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 1440, stol_y - 230, 6, 3, 220, .4))
    s += vinetka(.44)
    return s


# ── ПОМОЩНИКИ ВТОРОЙ ПАРТИИ ────────────────────────────────────────────────

def _stolb_pogranichnyy(x, y, h_, t, w_=96):
    """Полосатый пограничный столб: косые полосы, железная шляпка, скоба,
    у основания насыпь камней. Качается от ветра самую малость."""
    kach = .8 * A.w(t, 5.2, .1)
    s = (f'<g transform="rotate({kach:.2f} {x:.0f} {y:.0f})">'
         f'{ten(x, y + 8, w_ * .9, 20, .5)}'
         f'<rect x="{x-w_/2:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="10" fill="#efe8da" {o(7)}/>')
    n = int(h_ / 92)
    for i in range(n):
        if i % 2 == 0:
            continue
        yy = y - h_ + i * 92
        s += (f'<path d="M{x-w_/2:.0f},{yy+76:.0f} L{x-w_/2:.0f},{yy+16:.0f}'
              f' L{x+w_/2:.0f},{yy-28:.0f} L{x+w_/2:.0f},{yy+32:.0f} Z"'
              f' fill="#b8352c" opacity=".92"/>')
    s += (f'<path d="M{x-w_*.72:.0f},{y-h_:.0f} L{x+w_*.72:.0f},{y-h_:.0f}'
          f' L{x+w_*.5:.0f},{y-h_-34:.0f} L{x-w_*.5:.0f},{y-h_-34:.0f} Z"'
          f' fill="{ZHELEZ}" {o(5)}/>'
          f'<rect x="{x-w_*.56:.0f}" y="{y-h_*.52:.0f}" width="{w_*1.12:.0f}"'
          f' height="22" rx="8" fill="#6a7278" {o(4)}/></g>')
    rnd = random.Random(int(x))
    for i in range(7):
        rr = rnd.uniform(22, 44)
        s += (f'<ellipse cx="{x+rnd.uniform(-110, 110):.0f}" cy="{y+rnd.uniform(-6, 22):.0f}"'
              f' rx="{rr:.0f}" ry="{rr*.6:.0f}" fill="#6a6256" {o(3)}/>')
    return s


def _stog(x, y, s_=1.0, t=0.0, kol=True):
    """Стог сена: шапка из соломы прядями, жердь по центру, подпорки и
    растрёпанный низ. Рыжая осень в кадре."""
    h2, w2 = 330 * s_, 400 * s_
    s = (f'{ten(x, y + 10, w2 * .52, 24, .45)}'
         f'<path d="M{x-w2/2:.0f},{y:.0f} q{w2*.10:.0f},{-h2*.82:.0f}'
         f' {w2*.5:.0f},{-h2:.0f} q{w2*.40:.0f},{h2*.18:.0f} {w2*.5:.0f},{h2:.0f} Z"'
         f' fill="url(#solom)" {o(6)}/>')
    rnd = random.Random(int(x) + 3)
    for i in range(22):
        px = x + rnd.uniform(-w2 * .46, w2 * .46)
        py = y - rnd.uniform(0, h2 * .86)
        dl = rnd.uniform(40, 96) * s_
        s += (f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{px+dl*.5:.0f}"'
              f' y2="{py+dl*.4:.0f}" stroke="#b08a3c" stroke-width="5"'
              f' opacity=".8"/>')
    if kol:
        s += (f'<line x1="{x:.0f}" y1="{y-h2-50*s_:.0f}" x2="{x:.0f}" y2="{y:.0f}"'
              f' stroke="url(#derev)" stroke-width="{16*s_:.0f}"/>'
              f'<line x1="{x-w2*.42:.0f}" y1="{y:.0f}" x2="{x-w2*.18:.0f}"'
              f' y2="{y-h2*.52:.0f}" stroke="#5e472e" stroke-width="{11*s_:.0f}"/>')
    return s


def _snegovik(x, y, s_=1.0, t=0.0):
    """Снеговик: три кома с инеем, ведро на голове, угольки, морковь,
    веточки-руки и шарф, который чуть шевелится."""
    kach = 3.0 * A.w(t, 3.6, .2)
    r1, r2, r3 = 104 * s_, 76 * s_, 54 * s_
    y1 = y - r1
    y2 = y1 - r1 * .76 - r2 * .5
    y3 = y2 - r2 * .72 - r3 * .5
    s = (f'{ten(x, y + 6, r1 * 1.1, 20, .45)}'
         f'<circle cx="{x:.0f}" cy="{y1:.0f}" r="{r1:.0f}" fill="url(#sneg)" {o(6)}/>'
         f'<circle cx="{x:.0f}" cy="{y2:.0f}" r="{r2:.0f}" fill="url(#sneg)" {o(6)}/>'
         f'<circle cx="{x:.0f}" cy="{y3:.0f}" r="{r3:.0f}" fill="url(#sneg)" {o(6)}/>')
    for i in range(3):
        s += (f'<circle cx="{x:.0f}" cy="{y2-r2*.3+i*r2*.4:.0f}" r="{9*s_:.0f}"'
              f' fill="{CHUGUN}"/>')
    for i in (-1, 1):
        s += (f'<circle cx="{x+i*r3*.38:.0f}" cy="{y3-r3*.18:.0f}" r="{8*s_:.0f}"'
              f' fill="{CHUGUN}"/>')
    s += (f'<path d="M{x+r3*.1:.0f},{y3+r3*.06:.0f} l{54*s_:.0f},{14*s_:.0f}'
          f' l{-50*s_:.0f},{14*s_:.0f} Z" fill="#d87a2c" {o(3)}/>'
          f'<path d="M{x-r3*.9:.0f},{y3-r3*.62:.0f} L{x+r3*.9:.0f},{y3-r3*.62:.0f}'
          f' L{x+r3*.72:.0f},{y3-r3*1.5:.0f} L{x-r3*.72:.0f},{y3-r3*1.5:.0f} Z"'
          f' fill="#5e676e" {o(5)}/>'
          f'<ellipse cx="{x:.0f}" cy="{y3-r3*1.5:.0f}" rx="{r3*.74:.0f}"'
          f' ry="{r3*.16:.0f}" fill="#49535b" {o(4)}/>')
    for i in (-1, 1):
        s += (f'<line x1="{x+i*r2*.9:.0f}" y1="{y2:.0f}" x2="{x+i*(r2*.9+78*s_):.0f}"'
              f' y2="{y2-54*s_:.0f}" stroke="#4e3a26" stroke-width="{10*s_:.0f}"'
              f' stroke-linecap="round"/>'
              f'<line x1="{x+i*(r2*.9+46*s_):.0f}" y1="{y2-28*s_:.0f}"'
              f' x2="{x+i*(r2*.9+68*s_):.0f}" y2="{y2-72*s_:.0f}" stroke="#4e3a26"'
              f' stroke-width="{7*s_:.0f}"/>')
    s += (f'<g transform="rotate({kach:.1f} {x:.0f} {y3+r3*.8:.0f})">'
          f'<rect x="{x-r3*1.0:.0f}" y="{y3+r3*.7:.0f}" width="{r3*2.0:.0f}"'
          f' height="{22*s_:.0f}" rx="9" fill="{TKAN}" {o(4)}/>'
          f'<path d="M{x+r3*.7:.0f},{y3+r3*.9:.0f} q{22*s_:.0f},{44*s_:.0f}'
          f' {4*s_:.0f},{78*s_:.0f} l{-28*s_:.0f},{-8*s_:.0f}'
          f' q{14*s_:.0f},{-34*s_:.0f} {-4*s_:.0f},{-64*s_:.0f} Z"'
          f' fill="{TKAN}" {o(3)}/></g>')
    return s


def _sani(x, y, s_=1.0, t=0.0, gruz=True):
    """Сани-розвальни: два полоза с загибом, вязки, борт из прутьев,
    охапка сена и верёвка. Стоят на снегу."""
    s = (f'{ten(x, y + 8, 180 * s_, 18, .4)}')
    for i, dy in enumerate((0, -26 * s_)):
        s += (f'<path d="M{x-180*s_:.0f},{y+dy:.0f} L{x+140*s_:.0f},{y+dy:.0f}'
              f' q{50*s_:.0f},{-4*s_:.0f} {56*s_:.0f},{-48*s_:.0f}"'
              f' fill="none" stroke="#5b4428" stroke-width="{16*s_:.0f}"'
              f' stroke-linecap="round"/>')
    for i in range(4):
        px = x - 150 * s_ + i * 96 * s_
        s += (f'<line x1="{px:.0f}" y1="{y:.0f}" x2="{px:.0f}" y2="{y-82*s_:.0f}"'
              f' stroke="#6a5030" stroke-width="{13*s_:.0f}"/>')
    s += (f'<rect x="{x-174*s_:.0f}" y="{y-96*s_:.0f}" width="{330*s_:.0f}"'
          f' height="{22*s_:.0f}" rx="9" fill="url(#derev)" {o(4)}/>')
    for i in range(7):
        px = x - 160 * s_ + i * 52 * s_
        s += (f'<path d="M{px:.0f},{y-96*s_:.0f} q{-10*s_:.0f},{-44*s_:.0f}'
              f' {6*s_:.0f},{-76*s_:.0f}" fill="none" stroke="#6a5030"'
              f' stroke-width="{8*s_:.0f}"/>')
    if gruz:
        s += (f'<path d="M{x-150*s_:.0f},{y-168*s_:.0f} q{80*s_:.0f},{-60*s_:.0f}'
              f' {160*s_:.0f},{-20*s_:.0f} q{70*s_:.0f},{26*s_:.0f}'
              f' {60*s_:.0f},{54*s_:.0f} Z" fill="url(#solom)" {o(5)}/>')
        for i in range(9):
            s += (f'<line x1="{x-130*s_+i*34*s_:.0f}" y1="{y-170*s_:.0f}"'
                  f' x2="{x-110*s_+i*34*s_:.0f}" y2="{y-214*s_:.0f}"'
                  f' stroke="#b08a3c" stroke-width="{5*s_:.0f}" opacity=".85"/>')
        s += (f'<path d="M{x-150*s_:.0f},{y-150*s_:.0f} q{150*s_:.0f},{40*s_:.0f}'
              f' {300*s_:.0f},{-16*s_:.0f}" fill="none" stroke="#8a7a58"'
              f' stroke-width="{7*s_:.0f}"/>')
    return s


def _svyazka_klyuchey(x, y, t, s_=1.0, ph=.0, n=4):
    """Связка ключей на кольце: кольцо, бородки разной формы, качается."""
    kach = 10 * A.w(t, 1.5, ph)
    s = (f'<g transform="rotate({kach:.1f} {x:.0f} {y:.0f})">'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{30*s_:.0f}" fill="none"'
         f' stroke="url(#zhel)" stroke-width="{11*s_:.0f}"/>')
    for i in range(n):
        a = math.radians(58 + i * (64.0 / max(1, n - 1)))
        kx = x + 26 * s_ * math.cos(a)
        ky = y + 26 * s_ * math.sin(a)
        dl = (96 + i * 16) * s_
        ex = kx + dl * math.cos(a)
        ey = ky + dl * math.sin(a)
        s += (f'<line x1="{kx:.0f}" y1="{ky:.0f}" x2="{ex:.0f}" y2="{ey:.0f}"'
              f' stroke="url(#zhel)" stroke-width="{10*s_:.0f}"'
              f' stroke-linecap="round"/>'
              f'<rect x="{ex-16*s_:.0f}" y="{ey-6*s_:.0f}" width="{30*s_:.0f}"'
              f' height="{26*s_:.0f}" rx="4" fill="url(#zhel)" {o(3)}/>'
              f'<rect x="{ex-6*s_:.0f}" y="{ey+4*s_:.0f}" width="{14*s_:.0f}"'
              f' height="{10*s_:.0f}" fill="#7a4d1c"/>'
              f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="{12*s_:.0f}" fill="none"'
              f' stroke="url(#zhel)" stroke-width="{6*s_:.0f}"/>')
    return s + "</g>"


def _krovat(x, y, w_, t, seed=5, loskut=True, h_=300):
    """Кровать: высокая спинка с шишечками, лоскутное покрывало квадратами,
    подзор по низу и тень под ней."""
    rnd = random.Random(seed)
    s = (f'{ten(x + w_ / 2, y + 10, w_ * .46, 22, .5)}'
         f'<rect x="{x:.0f}" y="{y-h_-170:.0f}" width="40" height="{h_+170:.0f}"'
         f' rx="12" fill="#5b4428" {o(5)}/>'
         f'<rect x="{x+w_-40:.0f}" y="{y-h_-110:.0f}" width="40" height="{h_+110:.0f}"'
         f' rx="12" fill="#5b4428" {o(5)}/>'
         f'<rect x="{x:.0f}" y="{y-h_-170:.0f}" width="{w_*.34:.0f}" height="30"'
         f' rx="11" fill="#6a5030" {o(4)}/>'
         f'<circle cx="{x+20:.0f}" cy="{y-h_-182:.0f}" r="22" fill="url(#zhel)" {o(4)}/>'
         f'<circle cx="{x+w_-20:.0f}" cy="{y-h_-122:.0f}" r="20" fill="url(#zhel)" {o(4)}/>'
         f'<rect x="{x+16:.0f}" y="{y-h_:.0f}" width="{w_-32:.0f}" height="{h_*.52:.0f}"'
         f' rx="16" fill="#cdbfa4" {o(6)}/>')
    if loskut:
        cols = ["#8a4a44", "#3f5c7a", "#8a6a2c", "#4a6a48", "#7a5a62", "#b0864a"]
        kk = 86
        for r in range(int(h_ * .50 / kk) + 1):
            for c in range(int((w_ - 40) / kk)):
                s += (f'<rect x="{x+24+c*kk:.0f}" y="{y-h_+8+r*kk:.0f}"'
                      f' width="{kk-8}" height="{kk-8}" rx="6"'
                      f' fill="{cols[(r*3+c) % len(cols)]}" stroke="{K}"'
                      f' stroke-width="3" opacity=".92"/>')
    s += (f'<path d="M{x+16:.0f},{y-h_+h_*.52:.0f} L{x+w_-16:.0f},{y-h_+h_*.52:.0f}'
          f' L{x+w_-26:.0f},{y:.0f} L{x+26:.0f},{y:.0f} Z" fill="#e8e0ca" {o(5)}/>')
    for i in range(int((w_ - 60) / 54)):
        s += (f'<path d="M{x+40+i*54:.0f},{y-h_*.30:.0f} q{14:.0f},{30:.0f}'
              f' {0:.0f},{h_*.26:.0f}" fill="none" stroke="#cdc5ae"'
              f' stroke-width="6" opacity=".85"/>')
    return s


def _podushka(x, y, w_, h_, t, ph=.0, pod=.0, hlop=.0):
    """Пуховая подушка: наволочка с мережкой, вдавленный угол, приподнятый
    край (pod 0..1) и хлопок ладонями (hlop 0..1 сплющивает)."""
    lift = 54 * pod
    sq = 1.0 - .14 * hlop
    return (f'<g transform="translate(0,{lift * .2:.1f})">'
            f'{ten(x, y + h_ * .5 + 10, w_ * .46, 16, .4)}'
            f'<path d="M{x-w_/2:.0f},{y+h_*sq*.5:.0f}'
            f' q{-28:.0f},{-h_*sq*.62:.0f} {46:.0f},{-h_*sq*.86:.0f}'
            f' q{w_*.44:.0f},{-26-lift:.0f} {w_*.86:.0f},{4-lift*.4:.0f}'
            f' q{70:.0f},{h_*sq*.26:.0f} {38:.0f},{h_*sq*.82:.0f}'
            f' q{-w_*.44:.0f},{36:.0f} {-w_*.92:.0f},0 Z"'
            f' fill="#f2ece0" {o(6)}/>'
            f'<path d="M{x-w_*.38:.0f},{y+h_*sq*.34:.0f}'
            f' q{w_*.38:.0f},{26:.0f} {w_*.76:.0f},{-6:.0f}" fill="none"'
            f' stroke="#d8d0bc" stroke-width="7"/>'
            f'<path d="M{x-w_*.34:.0f},{y-h_*sq*.28:.0f}'
            f' q{w_*.18:.0f},{-20:.0f} {w_*.36:.0f},{-4:.0f}" fill="none"'
            f' stroke="#e4dcc8" stroke-width="9" opacity=".9"/>'
            f'<path d="M{x+w_*.20:.0f},{y-h_*sq*.42:.0f}'
            f' q{w_*.12:.0f},{16:.0f} {w_*.04:.0f},{34:.0f}" fill="none"'
            f' stroke="#ddd5c2" stroke-width="6"/></g>')


def _bumaga_znachok(x, y, s_=1.0, vid="ruka", ug=0.0):
    """Бумага со значком вместо текста (своих букв не рисуем): рукопожатие,
    галочка, черта-отказ, перо. Лист с уголком и печатью."""
    w2, h2 = 150 * s_, 196 * s_
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x-w2/2:.0f},{y-h2:.0f} L{x+w2/2-22*s_:.0f},{y-h2:.0f}'
         f' L{x+w2/2:.0f},{y-h2+22*s_:.0f} L{x+w2/2:.0f},{y:.0f}'
         f' L{x-w2/2:.0f},{y:.0f} Z" fill="#f4efe0" {o(5)}/>'
         f'<path d="M{x+w2/2-22*s_:.0f},{y-h2:.0f} L{x+w2/2:.0f},{y-h2+22*s_:.0f}'
         f' L{x+w2/2-22*s_:.0f},{y-h2+22*s_:.0f} Z" fill="#ddd5c2" {o(2)}/>')
    cx, cy = x, y - h2 * .54
    if vid == "ruka":
        s += (f'<path d="M{cx-44*s_:.0f},{cy+12*s_:.0f} l{40*s_:.0f},{-26*s_:.0f}'
              f' l{48*s_:.0f},{10*s_:.0f} l{-40*s_:.0f},{28*s_:.0f} Z"'
              f' fill="#8a6a44" {o(4)}/>'
              f'<rect x="{cx-62*s_:.0f}" y="{cy+6*s_:.0f}" width="{34*s_:.0f}"'
              f' height="{18*s_:.0f}" rx="8" fill="#6a5030" {o(3)}/>'
              f'<rect x="{cx+34*s_:.0f}" y="{cy-22*s_:.0f}" width="{34*s_:.0f}"'
              f' height="{18*s_:.0f}" rx="8" fill="#6a5030" {o(3)}/>')
    elif vid == "galka":
        s += (f'<path d="M{cx-40*s_:.0f},{cy:.0f} L{cx-10*s_:.0f},{cy+32*s_:.0f}'
              f' L{cx+46*s_:.0f},{cy-40*s_:.0f}" fill="none" stroke="#3f7a44"'
              f' stroke-width="{16*s_:.0f}" stroke-linecap="round"/>')
    elif vid == "cherta":
        s += (f'<line x1="{cx-46*s_:.0f}" y1="{cy:.0f}" x2="{cx+46*s_:.0f}"'
              f' y2="{cy:.0f}" stroke="#9c2f28" stroke-width="{17*s_:.0f}"'
              f' stroke-linecap="round"/>')
    else:
        s += (f'<path d="M{cx+18*s_:.0f},{cy+34*s_:.0f} L{cx-12*s_:.0f},{cy-40*s_:.0f}'
              f' L{cx+4*s_:.0f},{cy-44*s_:.0f} L{cx+32*s_:.0f},{cy+30*s_:.0f} Z"'
              f' fill="#efe8da" {o(4)}/>'
              f'<line x1="{cx-6*s_:.0f}" y1="{cy-26*s_:.0f}" x2="{cx-34*s_:.0f}"'
              f' y2="{cy-36*s_:.0f}" stroke="#d8cfbd" stroke-width="{6*s_:.0f}"/>')
    s += (f'<circle cx="{x+w2*.26:.0f}" cy="{y-h2*.16:.0f}" r="{20*s_:.0f}"'
          f' fill="#9c2f28" opacity=".85" {o(2)}/>'
          f'<path d="M{x-w2*.32:.0f},{y-h2*.18:.0f} q{w2*.14:.0f},{-8*s_:.0f}'
          f' {w2*.28:.0f},0" fill="none" stroke="#6b6354" stroke-width="{5*s_:.0f}"/></g>')
    return s


def _vesy(x, y, t, s_=1.0, levo=.0, dreb=.0, h_=300):
    """Чашечные весы: чугунное основание, колонка, коромысло со стрелкой,
    две чаши на тройных цепях. levo −1..1 — перекос, dreb 0..1 — дрожь."""
    kren = levo * 11 + dreb * 7 * A.w(t, .22, .1)
    bal = 300 * s_
    s = (f'{ten(x, y + 8, 150 * s_, 20, .5)}'
         f'<path d="M{x-120*s_:.0f},{y:.0f} L{x+120*s_:.0f},{y:.0f}'
         f' L{x+86*s_:.0f},{y-34*s_:.0f} L{x-86*s_:.0f},{y-34*s_:.0f} Z"'
         f' fill="{CHUGUN}" {o(6)}/>'
         f'<rect x="{x-22*s_:.0f}" y="{y-h_*s_:.0f}" width="{44*s_:.0f}"'
         f' height="{h_*s_:.0f}" rx="14" fill="#5e676e" {o(6)}/>'
         f'<circle cx="{x:.0f}" cy="{y-h_*s_:.0f}" r="{30*s_:.0f}"'
         f' fill="url(#zhel)" {o(5)}/>')
    s += (f'<g transform="rotate({kren:.2f} {x:.0f} {y-h_*s_:.0f})">'
          f'<rect x="{x-bal:.0f}" y="{y-h_*s_-13*s_:.0f}" width="{bal*2:.0f}"'
          f' height="{26*s_:.0f}" rx="12" fill="url(#zhel)" {o(5)}/>'
          f'<path d="M{x:.0f},{y-h_*s_:.0f} l{-16*s_:.0f},{-76*s_:.0f}'
          f' l{32*s_:.0f},0 Z" fill="#8a5a22" {o(4)}/>')
    for sgn in (-1, 1):
        px = x + sgn * bal
        for k in (-.5, 0, .5):
            s += (f'<line x1="{px:.0f}" y1="{y-h_*s_:.0f}"'
                  f' x2="{px+k*76*s_:.0f}" y2="{y-h_*s_+112*s_:.0f}"'
                  f' stroke="#8a6a3c" stroke-width="{5*s_:.0f}"/>')
        s += (f'<path d="M{px-88*s_:.0f},{y-h_*s_+112*s_:.0f}'
              f' q{88*s_:.0f},{68*s_:.0f} {176*s_:.0f},0 Z" fill="url(#zhel)" {o(5)}/>'
              f'<ellipse cx="{px:.0f}" cy="{y-h_*s_+112*s_:.0f}" rx="{88*s_:.0f}"'
              f' ry="{18*s_:.0f}" fill="#d6a358" opacity=".85"/>')
    return s + "</g>"


def _veshalka_s_paltom(x, y, w_, t, seed=3):
    """Вешалка прихожей: планка с крючками, два пальто и плащ складками,
    шапка на верхней полке, зонт на крайнем крюке."""
    rnd = random.Random(seed)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="34" rx="10"'
         f' fill="url(#dosk)" {o(6)}/>'
         f'<rect x="{x+10:.0f}" y="{y-56:.0f}" width="{w_-20:.0f}" height="26" rx="9"'
         f' fill="#6a5030" {o(5)}/>')
    for i in range(5):
        hx = x + 56 + i * (w_ - 120) / 4.0
        s += (f'<path d="M{hx:.0f},{y+34:.0f} q{6:.0f},{26:.0f} {-16:.0f},{30:.0f}"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="10"/>')
    cols = ["#3f4a58", "#5a3a2c", "#4a5a46"]
    for i in range(3):
        px = x + 110 + i * (w_ - 240) / 2.0
        hh = rnd.uniform(390, 470)
        s += (f'<path d="M{px-78:.0f},{y+70:.0f} q{78:.0f},{-44:.0f} {156:.0f},0'
              f' L{px+96:.0f},{y+hh:.0f} q{-96:.0f},{34:.0f} {-192:.0f},0 Z"'
              f' fill="{cols[i]}" {o(6)}/>'
              f'<line x1="{px:.0f}" y1="{y+84:.0f}" x2="{px:.0f}" y2="{y+hh:.0f}"'
              f' stroke="{K}" stroke-width="5" opacity=".6"/>')
        for k in range(3):
            s += (f'<circle cx="{px+14:.0f}" cy="{y+150+k*78:.0f}" r="11"'
                  f' fill="#d8c08a" {o(2)}/>')
    s += (f'<ellipse cx="{x+w_-80:.0f}" cy="{y-70:.0f}" rx="62" ry="28"'
          f' fill="#4a3a2c" {o(5)}/>'
          f'<path d="M{x+w_-130:.0f},{y-74:.0f} q{50:.0f},{-44:.0f} {100:.0f},0 Z"'
          f' fill="#5a4636" {o(4)}/>')
    return s


def _zont_v_podstavke(x, y, t, s_=1.0):
    """Зонт в подставке: тулья сложена, спицы, ручка крюком, латунное
    ведёрко с каплями на дне."""
    kach = 1.6 * A.w(t, 4.4, .3)
    return (f'<g transform="rotate({kach:.2f} {x:.0f} {y:.0f})">'
            f'{ten(x, y + 6, 46 * s_, 11, .4)}'
            f'<path d="M{x-44*s_:.0f},{y:.0f} L{x+44*s_:.0f},{y:.0f}'
            f' L{x+38*s_:.0f},{y-130*s_:.0f} L{x-38*s_:.0f},{y-130*s_:.0f} Z"'
            f' fill="url(#zhel)" {o(5)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y-130*s_:.0f}" rx="{38*s_:.0f}"'
            f' ry="{11*s_:.0f}" fill="#8a5a22" {o(3)}/>'
            f'<path d="M{x-16*s_:.0f},{y-126*s_:.0f} q{-10*s_:.0f},{-150*s_:.0f}'
            f' {16*s_:.0f},{-230*s_:.0f} q{28*s_:.0f},{78*s_:.0f} {18*s_:.0f},{230*s_:.0f} Z"'
            f' fill="#3f4a58" {o(5)}/>'
            f'<line x1="{x+2*s_:.0f}" y1="{y-356*s_:.0f}" x2="{x+2*s_:.0f}"'
            f' y2="{y-120*s_:.0f}" stroke="#6a7278" stroke-width="{7*s_:.0f}"/>'
            f'<path d="M{x+2*s_:.0f},{y-356*s_:.0f} q{30*s_:.0f},{-34*s_:.0f}'
            f' {44*s_:.0f},{4*s_:.0f}" fill="none" stroke="#5b4428"'
            f' stroke-width="{13*s_:.0f}"/>'
            f'<ellipse cx="{x-10*s_:.0f}" cy="{y-10*s_:.0f}" rx="{20*s_:.0f}"'
            f' ry="{7*s_:.0f}" fill="#7e97ad" opacity=".7"/></g>')


def _chislennik(x, y, w_, h_, t, otryv=.0):
    """Отрывной численник: щиток с жестяной шапкой, толстый блок листков
    торцом, верхний листок пустой (цифру кладёт надпись поверх) и
    волнистая строка под ним. Листок шевелится."""
    kach = 1.8 * A.w(t, 2.6, .2)
    s = (f'{ten(x + w_ / 2, y + h_ + 14, w_ * .4, 14, .35)}'
         f'<rect x="{x-18:.0f}" y="{y-18:.0f}" width="{w_+36:.0f}"'
         f' height="{h_+36:.0f}" rx="12" fill="#6a5030" {o(6)}/>'
         f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8"'
         f' fill="#b8352c" {o(5)}/>'
         f'<rect x="{x-24:.0f}" y="{y-46:.0f}" width="{w_+48:.0f}" height="40" rx="12"'
         f' fill="{ZHELEZ}" {o(5)}/>'
         f'<circle cx="{x+w_/2:.0f}" cy="{y-26:.0f}" r="13" fill="#3e4348" {o(3)}/>')
    for i in range(7):
        s += (f'<rect x="{x+16:.0f}" y="{y+h_*.22+i*5:.0f}" width="{w_-32:.0f}"'
              f' height="{h_*.70:.0f}" rx="6" fill="#efe8da" opacity=".55"/>')
    s += (f'<g transform="rotate({kach + 8 * otryv:.1f} {x+22:.0f} {y+h_*.24:.0f})">'
          f'<rect x="{x+12:.0f}" y="{y+h_*.20:.0f}" width="{w_-24:.0f}"'
          f' height="{h_*.72:.0f}" rx="7" fill="#f6f1e4" {o(5)}/>'
          f'<path d="M{x+w_*.22:.0f},{y+h_*.80:.0f} q{w_*.14:.0f},{-12:.0f}'
          f' {w_*.28:.0f},0 q{w_*.14:.0f},{12:.0f} {w_*.28:.0f},0" fill="none"'
          f' stroke="#9a8a68" stroke-width="7"/>'
          f'<rect x="{x+w_*.14:.0f}" y="{y+h_*.26:.0f}" width="{w_*.72:.0f}"'
          f' height="10" rx="5" fill="#c9b79c" opacity=".8"/></g>')
    return s


def _zavalinka(x, y, w_, t, h_=170):
    """Завалинка у избы: земляная присыпка вдоль сруба, тёсаная доска
    сверху, подпорные колья и палая листва у подножия."""
    rnd = random.Random(int(x) + 7)
    s = (f'<path d="M{x:.0f},{y:.0f} L{x+w_:.0f},{y:.0f} L{x+w_-36:.0f},{y-h_:.0f}'
         f' L{x+36:.0f},{y-h_:.0f} Z" fill="#6b5a44" {o(6)}/>'
         f'<rect x="{x+18:.0f}" y="{y-h_-26:.0f}" width="{w_-36:.0f}" height="34"'
         f' rx="10" fill="url(#dosk)" {o(6)}/>')
    for i in range(int(w_ / 150)):
        px = x + 60 + i * 150
        s += (f'<line x1="{px:.0f}" y1="{y:.0f}" x2="{px+8:.0f}" y2="{y-h_:.0f}"'
              f' stroke="#4e3a26" stroke-width="15"/>')
    for i in range(14):
        rr = rnd.uniform(18, 34)
        s += (f'<ellipse cx="{x+rnd.uniform(0, w_):.0f}" cy="{y+rnd.uniform(-8, 26):.0f}"'
              f' rx="{rr:.0f}" ry="{rr*.5:.0f}"'
              f' fill="{["#9a5a28", "#b4762f", "#7d4a24"][i % 3]}" opacity=".9"/>')
    return s


def _sglaz(x, y, t, s_=1.0, ph=.0, op=.92):
    """Сглаз: серое облачко с ОДНИМ прищуренным глазом, клубится по краю,
    снизу тянется дымный хвостик. Рисованный персонаж, не пятно."""
    dr = 1.0 + .05 * A.w(t, 1.6, ph)
    s = (f'<g transform="translate({x:.0f} {y:.0f}) scale({dr:.3f})'
         f' translate({-x:.0f} {-y:.0f})" opacity="{op:.2f}">')
    rnd = random.Random(int(ph * 100) + 5)
    for i in range(7):
        a = math.radians(i * 51)
        s += (f'<circle cx="{x+math.cos(a)*62*s_:.0f}" cy="{y+math.sin(a)*34*s_:.0f}"'
              f' r="{(38+rnd.uniform(0, 16))*s_:.0f}" fill="#7a818a" {o(4)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{96*s_:.0f}" ry="{58*s_:.0f}"'
          f' fill="#8a919a" {o(5)}/>'
          f'<ellipse cx="{x:.0f}" cy="{y-4*s_:.0f}" rx="{40*s_:.0f}"'
          f' ry="{27*s_:.0f}" fill="#f2f6fa" {o(4)}/>'
          f'<circle cx="{x+8*s_:.0f}" cy="{y-2*s_:.0f}" r="{17*s_:.0f}"'
          f' fill="#2b3f52"/>'
          f'<circle cx="{x+14*s_:.0f}" cy="{y-8*s_:.0f}" r="{6*s_:.0f}"'
          f' fill="#eaf4ff" opacity=".9"/>'
          f'<path d="M{x-44*s_:.0f},{y-18*s_:.0f} q{44*s_:.0f},{-26*s_:.0f}'
          f' {88*s_:.0f},{-4*s_:.0f}" fill="none" stroke="#3c434a"'
          f' stroke-width="{10*s_:.0f}" stroke-linecap="round"/>'
          f'<path d="M{x-40*s_:.0f},{y+14*s_:.0f} q{40*s_:.0f},{20*s_:.0f}'
          f' {80*s_:.0f},{-2*s_:.0f}" fill="none" stroke="#5c646c"'
          f' stroke-width="{8*s_:.0f}"/>')
    for i in range(3):
        k = (t * .5 + ph + i * .33) % 1.0
        s += (f'<circle cx="{x-70*s_-40*k*s_:.0f}" cy="{y+40*s_+30*k*s_:.0f}"'
              f' r="{(20-10*k)*s_:.0f}" fill="#8a919a"'
              f' opacity="{.6*(1-k):.2f}"/>')
    return s + "</g>"


def _sapogi_novye(x, y, s_=1.0, t=0.0, blesk=1.0):
    """Новые сапоги: голенище гармошкой, скошенный каблук, подкова на
    подошве и бегущий блик по голенищу."""
    bl = .3 + .5 * abs(A.w(t, 1.8, .2)) * blesk
    s = ""
    for i, dx in enumerate((-52, 46)):
        hh = (168 if i == 0 else 158) * s_
        s += (f'{ten(x + dx * s_, y + 6 * s_, 46 * s_, 11 * s_, .45)}'
              f'<path d="M{x+dx*s_-38*s_:.0f},{y:.0f} L{x+dx*s_+42*s_:.0f},{y:.0f}'
              f' L{x+dx*s_+30*s_:.0f},{y-hh:.0f} L{x+dx*s_-26*s_:.0f},{y-hh:.0f} Z"'
              f' fill="#2e2620" {o(5)}/>')
        for k in range(4):
            s += (f'<path d="M{x+dx*s_-28*s_:.0f},{y-hh*.30-k*26*s_:.0f}'
                  f' q{30*s_:.0f},{10*s_:.0f} {60*s_:.0f},{-2*s_:.0f}" fill="none"'
                  f' stroke="#4a3f36" stroke-width="{7*s_:.0f}" opacity=".9"/>')
        s += (f'<rect x="{x+dx*s_-40*s_:.0f}" y="{y-16*s_:.0f}" width="{84*s_:.0f}"'
              f' height="{18*s_:.0f}" rx="5" fill="#1d1812" {o(3)}/>'
              f'<path d="M{x+dx*s_-22*s_:.0f},{y-hh*.84:.0f}'
              f' L{x+dx*s_-14*s_:.0f},{y-hh*.18:.0f}" fill="none" stroke="#cfe4f5"'
              f' stroke-width="{8*s_:.0f}" opacity="{bl:.2f}"/>')
    return s


def _ambar_s_meshkami(x, y, w_, h_, t, otkr=.0, seed=5):
    """Амбар с распахнутыми воротами: бревенчатые щиты створок на кованых
    петлях, внутри мешки горой, над дверью скоба и рябиновая гроздь."""
    rnd = random.Random(seed)
    s = brevna(x, y, w_, h_, 92)
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' fill="none" {o(9)}/>')
    pw = w_ * .34
    px = x + w_ * .33
    s += (f'<rect x="{px:.0f}" y="{y+h_*.18:.0f}" width="{pw:.0f}"'
          f' height="{h_*.82:.0f}" rx="6" fill="#2a2018"/>')
    for i in range(6):
        mx = px + 40 + rnd.uniform(0, pw - 110)
        my = y + h_ - 20 - (i % 3) * 86
        s += (f'<path d="M{mx-54:.0f},{my:.0f} q{-14:.0f},{-80:.0f} {24:.0f},{-104:.0f}'
              f' q{32:.0f},{-12:.0f} {58:.0f},{8:.0f} q{30:.0f},{34:.0f}'
              f' {20:.0f},{96:.0f} Z" fill="#d8c8a4" {o(5)}/>'
              f'<path d="M{mx-18:.0f},{my-102:.0f} q{20:.0f},{-14:.0f} {42:.0f},{4:.0f}"'
              f' fill="none" stroke="{TKAN}" stroke-width="8"/>')
    for sgn, ug in ((-1, -62 * otkr), (1, 62 * otkr)):
        vx = px + (0 if sgn < 0 else pw)
        s += (f'<g transform="rotate({ug:.1f} {vx:.0f} {y+h_*.2:.0f})">'
              f'<rect x="{vx - (pw * .5 if sgn < 0 else 0):.0f}" y="{y+h_*.18:.0f}"'
              f' width="{pw*.5:.0f}" height="{h_*.82:.0f}" rx="6"'
              f' fill="url(#derev)" {o(6)}/>')
        for k in range(4):
            s += (f'<rect x="{vx - (pw * .5 if sgn < 0 else 0) + 10 + k * (pw * .5 - 24) / 4:.0f}"'
                  f' y="{y+h_*.21:.0f}" width="{(pw*.5-30)/4.6:.0f}"'
                  f' height="{h_*.76:.0f}" rx="5" fill="#6a5030" {o(3)}/>')
        s += (f'<rect x="{vx - (pw * .5 if sgn < 0 else 0):.0f}" y="{y+h_*.42:.0f}"'
              f' width="{pw*.5:.0f}" height="24" rx="8" fill="{ZHELEZ}" {o(4)}/></g>')
    s += (f'<rect x="{px-26:.0f}" y="{y+h_*.10:.0f}" width="{pw+52:.0f}" height="34"'
          f' rx="10" fill="#4a3522" {o(5)}/>')
    s += grozd_ryabiny(px + pw + 70, y + h_ * .22, t, 1.1, 13, 7, .3)
    return s


def _rog_izobiliya(x, y, t, s_=1.0, ph=.0):
    """Рог изобилия: плетёный рог витком, из него сыплются яблоки, колосья
    и калач. Его держат обеими руками у груди."""
    s = (f'<path d="M{x:.0f},{y:.0f} q{-80*s_:.0f},{-30*s_:.0f} {-116*s_:.0f},{-96*s_:.0f}'
         f' q{-24*s_:.0f},{-54*s_:.0f} {26*s_:.0f},{-66*s_:.0f}'
         f' q{40*s_:.0f},{-8*s_:.0f} {48*s_:.0f},{32*s_:.0f}'
         f' q{10*s_:.0f},{48*s_:.0f} {60*s_:.0f},{72*s_:.0f} Z"'
         f' fill="url(#solom)" {o(6)}/>')
    for i in range(5):
        s += (f'<path d="M{x-24*s_-i*20*s_:.0f},{y-18*s_-i*14*s_:.0f}'
              f' q{-14*s_:.0f},{-26*s_:.0f} {6*s_:.0f},{-44*s_:.0f}" fill="none"'
              f' stroke="#8a6a3c" stroke-width="{6*s_:.0f}" opacity=".85"/>')
    rnd = random.Random(int(ph * 50) + 11)
    for i in range(6):
        k = ((t * .4 + ph + i * .17) % 1.0)
        ax = x + 30 * s_ + i * 26 * s_ + 40 * k * s_
        ay = y - 20 * s_ + 120 * k * s_
        if i % 3 == 2:
            s += (f'<path d="M{ax:.0f},{ay:.0f} q{10*s_:.0f},{-34*s_:.0f}'
                  f' {2*s_:.0f},{-58*s_:.0f}" fill="none" stroke="#c9a05a"'
                  f' stroke-width="{7*s_:.0f}" opacity="{1-k*.5:.2f}"/>')
        else:
            s += (f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="{22*s_:.0f}"'
                  f' fill="{"#b8352c" if i % 2 else "#c9772c"}" {o(3)}/>')
    s += (f'<path d="M{x+56*s_:.0f},{y+16*s_:.0f} a{34*s_:.0f},{34*s_:.0f} 0 1 0'
          f' {2*s_:.0f},0 Z" fill="url(#med)" {o(5)}/>')
    return s


def _vorota_dvora(x, y, w_, h_, t, otkr=.0):
    """Створчатые ворота двора: две плахи на кованых полосах, столбы с
    шапками, кольцо-ручка. Одна створка отведена (otkr 0..1)."""
    s = ""
    for sgn in (-1, 1):
        sx = x + (0 if sgn < 0 else w_ * .5)
        ug = sgn * 46 * otkr
        ax = x if sgn < 0 else x + w_
        s += (f'<g transform="rotate({ug:.1f} {ax:.0f} {y:.0f})">'
              f'<rect x="{sx:.0f}" y="{y-h_:.0f}" width="{w_*.5:.0f}" height="{h_:.0f}"'
              f' rx="6" fill="url(#derev)" {o(7)}/>')
        for k in range(5):
            s += (f'<rect x="{sx+12+k*(w_*.5-30)/5:.0f}" y="{y-h_+10:.0f}"'
                  f' width="{(w_*.5-40)/5.4:.0f}" height="{h_-20:.0f}" rx="5"'
                  f' fill="#6a5030" {o(3)}/>')
        s += (f'<rect x="{sx:.0f}" y="{y-h_*.72:.0f}" width="{w_*.5:.0f}" height="22"'
              f' rx="8" fill="{ZHELEZ}" {o(4)}/>'
              f'<rect x="{sx:.0f}" y="{y-h_*.28:.0f}" width="{w_*.5:.0f}" height="22"'
              f' rx="8" fill="{ZHELEZ}" {o(4)}/>'
              f'<circle cx="{sx + (w_ * .46 if sgn < 0 else w_ * .04):.0f}"'
              f' cy="{y-h_*.5:.0f}" r="20" fill="none" stroke="{ZHELEZ}"'
              f' stroke-width="9"/></g>')
    for px in (x - 30, x + w_ - 20):
        s += (f'<rect x="{px:.0f}" y="{y-h_-40:.0f}" width="52" height="{h_+40:.0f}"'
              f' rx="8" fill="#4e3a26" {o(6)}/>'
              f'<path d="M{px-14:.0f},{y-h_-40:.0f} L{px+26:.0f},{y-h_-78:.0f}'
              f' L{px+66:.0f},{y-h_-40:.0f} Z" fill="#5b4428" {o(4)}/>')
    return s


# ── ДЕКОРАЦИИ, ВТОРАЯ ПАРТИЯ ───────────────────────────────────────────────

def granica_oseni_i_zimy(t):
    """Поле, разделённое надвое полосатым пограничным столбом: слева рыжая
    осень со стогом и лужей, справа белая зима с сугробом, снеговиком и
    санями. Осень передаёт зиме связку ключей через столб."""
    rnd = random.Random(233)
    gor = 560
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 19)
    s += oblaka(t, 150, 5, 23, .42, "#cdd7e4", 14.0)
    # дальний план: слева бурая деревня с дымком, справа белый лес
    s += SL(Z_DAL, izba_snaruzhi(250, gor - 10, 330, t, True, True, 5)
            + izba_snaruzhi(560, gor - 24, 250, t, True, True, 11))
    s += SL(Z_DAL, goloe_derevo(130, gor + 10, 520, t, 7, 9, "#3a3b43", False)
            + goloe_derevo(820, gor + 4, 400, t, 13, 8, "#3a3b43", False))
    for i in range(5):
        s += SL(Z_DAL, f'<path d="M{1180+i*170:.0f},{gor:.0f}'
                       f' l{-72:.0f},0 l{72:.0f},{-230-i*26:.0f}'
                       f' l{72:.0f},{230+i*26:.0f} Z" fill="#cfd8e6"'
                       f' opacity=".92" {o(4)}/>')
    s += SL(Z_DAL, _zabor_dosok(-30, gor - 170, 860, 180, 5, 54))
    # земля: слева мёрзлая рыжая, справа снег. Два щита, не фон
    s += SL(Z_SRED, f'<path d="M-20,{gor:.0f} L960,{gor:.0f} L960,1080 L-20,1080 Z"'
                    f' fill="#5a4630"/>'
            + _zemlya_faktura(gor + 40, 1050, 3, 15, "#46382a")
            + _listya(27, 46, gor + 50, 1060)
            + _trava(rnd, 14, gor + 60, 1040))
    s += SL(Z_SRED, f'<path d="M960,{gor:.0f} L1940,{gor:.0f} L1940,1080 L960,1080 Z"'
                    f' fill="#d8e2ee"/>'
            + f'<path d="M980,{gor+80:.0f} q240,-56 480,-8 q240,46 460,-24'
              f' L1940,1080 L980,1080 Z" fill="url(#sneg)" {o(0)}/>'
            + _inej(37, 54, gor + 60, 1060))
    s += SL(Z_SRED, _stog(300, 1010, 1.12, t, True))
    s += SL(Z_SRED, _luzha(690, 1012, 196, t, .2))
    s += SL(Z_SRED, _kucha_listev(96, 1050, 320, 41, 92))
    s += SL(Z_SRED, _snegovik(1660, 1010, 1.18, t))
    s += SL(Z_SRED, _sani(1290, 1040, 1.0, t, True))
    s += SL(Z_SRED, _sledy(1880, 1066, 1480, 900, 7, 43, "#8fa3b4", 1.3))
    # великаны по пояс над горизонтом: сначала фигуры, потом полоса земли
    kl = A.ease(A.seg(t, 1.0, 2.2))
    ox, oy, oh = 560, gor + 300, 760
    osen = figura(ox, oy, oh, t, col="#9c5a28", kant="#ffd98a", platok=True,
                  ph=.2, naklon=4.0)
    o1, (k1x, k1y), _ = _ruka(ox, oy, oh, 1, oh * .44, 10, t,
                              "#9c5a28", "#ffd98a", .2, 5.0)
    o2, (k2x, k2y), _ = _ruka(ox, oy, oh, 1, oh * .34, 30, t,
                              "#b4762f", "#ffd98a", .6, 4.0)
    osen += o1 + o2
    # платок из листьев
    for i in range(9):
        a = math.radians(-168 + i * 21)
        osen += (f'<path d="M{ox+126*math.cos(a):.0f},{oy-oh*.86+96*math.sin(a):.0f}'
                 f' q{22:.0f},{-20:.0f} {44:.0f},{4:.0f} q{-20:.0f},{22:.0f}'
                 f' {-44:.0f},{-4:.0f} Z"'
                 f' fill="{["#b4762f", "#9a5a28", "#c08a3a"][i % 3]}" {o(3)}/>')
    s += SL(Z_SRED, osen)
    zx, zy, zh = 1360, gor + 300, 790
    zima = figura(zx, zy, zh, t, col="#e4eaf2", kant="#8fb0c4", tulup=True,
                  boroda=True, ph=.7, naklon=-3.0)
    z1, (p1x, p1y), _ = _ruka(zx, zy, zh, -1, zh * .42, 8, t,
                              "#e4eaf2", "#8fb0c4", .7, 5.0)
    z2, (p2x, p2y), _ = _ruka(zx, zy, zh, 1, zh * .46, 56, t,
                              "#e4eaf2", "#8fb0c4", .3, 4.0)
    zima += z1 + z2
    s += SL(Z_SRED, zima)
    # ледяной посох под правой рукой зимы
    s += SL(Z_SRED, f'<line x1="{p2x:.0f}" y1="{p2y-30:.0f}" x2="{p2x+30:.0f}"'
                    f' y2="{p2y+330:.0f}" stroke="#9fc4d8" stroke-width="22"'
                    f' stroke-linecap="round"/>'
            + f'<circle cx="{p2x-2:.0f}" cy="{p2y-48:.0f}" r="30" fill="#cfe4f5"'
              f' {o(5)}/>')
    # связка ключей идёт из рук осени в руку зимы
    kx = k1x + (p1x - k1x) * kl
    ky = k1y + (p1y - k1y) * kl
    s += SL(Z_SRED, _svyazka_klyuchey(kx, ky + 16, t, 1.25, .2, 4))
    s += SL(Z_SRED, para_izo_rta(ox + 96, oy - oh * .80, t, .2, 1.3, .5)
            + para_izo_rta(zx - 96, zy - zh * .80, t, .6, 1.4, .55))
    # СТОЛБ — главный предмет, ровно по стыку половин
    s += SL(Z_SRED, _stolb_pogranichnyy(960, 1016, 660, t, 104))
    # мужичок с топором и бревном на плече: подходит и уходит
    sh = A.seg(t, .2, 6.0)
    mx = 240 + 1340 * sh
    mh = 300
    muz = figura(mx, 1046, mh, t, col="#4a4a56", kant="#cfe4f5", shapka=True,
                 ph=.5, profil=True, naklon=5.0)
    m1, (b1x, b1y), _ = _ruka(mx, 1046, mh, 1, mh * .40, -32, t,
                              "#4a4a56", "#cfe4f5", .5, 6.0)
    m2, (b2x, b2y), _ = _ruka(mx, 1046, mh, -1, mh * .36, 44, t,
                              "#4a4a56", "#cfe4f5", .1, 6.0)
    muz += m1 + m2
    muz += (f'<line x1="{b1x-130:.0f}" y1="{b1y-56:.0f}" x2="{b1x+140:.0f}"'
            f' y2="{b1y+22:.0f}" stroke="url(#derev)" stroke-width="40"'
            f' stroke-linecap="round"/>'
            f'<line x1="{b2x:.0f}" y1="{b2y:.0f}" x2="{b2x+10:.0f}"'
            f' y2="{b2y+86:.0f}" stroke="url(#derev)" stroke-width="13"/>'
            f'<path d="M{b2x+4:.0f},{b2y+86:.0f} l{44:.0f},{-14:.0f} l{8:.0f},{40:.0f}'
            f' l{-48:.0f},{10:.0f} Z" fill="{ZHELEZ}" {o(4)}/>')
    s += SL(Z_SRED, muz)
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(k2x, k2y, oh, t, .6, "#f0d8b0")
            + _varezhka(p1x, p1y, zh, t, .7, "#dfe8f0")
            + _varezhka(p2x, p2y, zh, t, .3, "#dfe8f0")
            + _varezhka(kx, ky + 16, oh * .7, t, .2, "#f0d8b0"))
    s += SL(Z_PERED, _vetka_pered(-70, 110, 760, 26, t, 7, "#241c16", 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 5, .55, .9))
    s += ramka_pp("pravo")
    s += vinetka(.42)
    return s


def okno_noch_i_utro(t):
    """Спальня: кровать с высокими подушками, тумбочка с будильником и
    стаканом, окно на пол-кадра — за ним настоящий рассвет над городом.
    Мужчина в пижаме кладёт лист под будильник и гасит ночник."""
    rnd = random.Random(239)
    pol = 962
    s = f'<rect width="{W}" height="{H}" fill="#1b2130"/>'
    s += SL(Z_DAL, doski(0, 0, 820, pol, 102, True, "dosk"))
    s += SL(Z_DAL, f'<rect x="820" y="0" width="1100" height="{pol:.0f}"'
                   f' fill="#3c4556"/>')
    for i in range(11):
        s += SL(Z_DAL, f'<rect x="{830+i*100:.0f}" y="0" width="52"'
                       f' height="{pol:.0f}" fill="#465063" opacity=".6"/>')
    s += SL(Z_DAL, _ramki_na_stene(140, 180, 560, t, 17, 3))
    s += SL(Z_DAL, _knizhnaya_polka(96, 630, 620, t, 139, 1, 180))
    # комод с ящиками, графин и обувная полка — вещи спальни среднего плана
    s += SL(Z_DAL, f'<rect x="96" y="700" width="560" height="250" rx="10"'
                   f' fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_DAL, f'<rect x="{116+i*180:.0f}" y="724" width="166"'
                       f' height="100" rx="7" fill="#8a6a44" {o(4)}/>'
                f'<rect x="{116+i*180:.0f}" y="836" width="166" height="96"'
                f' rx="7" fill="#9c7a4c" {o(4)}/>'
                f'<rect x="{176+i*180:.0f}" y="766" width="48" height="14" rx="7"'
                f' fill="url(#zhel)" {o(3)}/>'
                f'<rect x="{176+i*180:.0f}" y="876" width="48" height="14" rx="7"'
                f' fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="{pol-12:.0f}" width="{W}"'
                   f' height="{H-pol+12:.0f}" fill="#4e4336"/>'
            + _polovik(560, pol + 24, 760, 104, "#b9a888", "#6a5a44"))
    # ОКНО: сначала рисованный вид, потом метка, потом переплёт поверх
    px, py, pw, ph_ = 940, 130, 900, 470
    put = kontur_proema(px, py, pw, ph_, "pryam")
    zar = A.ease(A.seg(t, .2, 1.8))
    s += SL(Z_SRED, _vid_za_proemom(put, t, "zarya", 5, px + pw * .5)
            + mesto_stoka(px, py, pw, ph_, "pryam"))
    # переплёт и наличники ПОВЕРХ кадра — это и есть «кадр внутри сцены»
    ram = (f'<path d="{put}" fill="none" stroke="#6a5a46" stroke-width="30"/>'
           f'<rect x="{px-34:.0f}" y="{py-42:.0f}" width="{pw+68:.0f}" height="36"'
           f' rx="10" fill="#7d6a52" {o(5)}/>'
           f'<rect x="{px-50:.0f}" y="{py+ph_-10:.0f}" width="{pw+100:.0f}"'
           f' height="44" rx="10" fill="url(#dosk)" {o(6)}/>'
           f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
           f' y2="{py+ph_:.0f}" stroke="#6a5a46" stroke-width="22"/>'
           f'<line x1="{px:.0f}" y1="{py+ph_*.46:.0f}" x2="{px+pw:.0f}"'
           f' y2="{py+ph_*.46:.0f}" stroke="#6a5a46" stroke-width="20"/>'
           f'<path d="M{px+40:.0f},{py+ph_*.40:.0f} L{px+pw*.44:.0f},{py+30:.0f}"'
           f' fill="none" stroke="#eaf4ff" stroke-width="12"'
           f' opacity="{.12+.22*zar:.2f}"/>')
    s += SL(Z_SRED, ram)
    s += SL(Z_SRED, zanaveska(px - 30, py - 20, 560, 150, "#c9bca0", t, 1)
            + zanaveska(px + pw + 30, py - 20, 560, 150, "#c9bca0", t, -1))
    # КРОВАТЬ — главный предмет
    s += SL(Z_SRED, _krovat(90, pol, 980, t, 7, True, 330))
    s += SL(Z_SRED, _podushka(300, pol - 420, 320, 180, t, .2, .0, .0)
            + _podushka(560, pol - 452, 300, 170, t, .5, .0, .0))
    # тумбочка, будильник, стакан, ночник
    tx = 1240
    s += SL(Z_SRED, f'{ten(tx + 70, pol + 6, 110, 18, .45)}'
                    f'<rect x="{tx:.0f}" y="{pol-290:.0f}" width="250" height="290"'
                    f' rx="10" fill="url(#derev)" {o(6)}/>'
            + f'<rect x="{tx+18:.0f}" y="{pol-262:.0f}" width="214" height="110"'
              f' rx="7" fill="#8a6a44" {o(4)}/>'
            + f'<rect x="{tx+100:.0f}" y="{pol-214:.0f}" width="54" height="16"'
              f' rx="7" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, f'<circle cx="{tx+86:.0f}" cy="{pol-346:.0f}" r="56"'
                    f' fill="#e8e0cc" {o(6)}/>'
            + f'<circle cx="{tx+86:.0f}" cy="{pol-346:.0f}" r="42"'
              f' fill="#f6f2e4" {o(3)}/>'
            + f'<line x1="{tx+86:.0f}" y1="{pol-346:.0f}"'
              f' x2="{tx+86+30*math.cos(t*1.1):.0f}"'
              f' y2="{pol-346+30*math.sin(t*1.1):.0f}" stroke="{K}" stroke-width="6"/>'
            + f'<line x1="{tx+86:.0f}" y1="{pol-346:.0f}"'
              f' x2="{tx+86+18*math.cos(t*.2):.0f}"'
              f' y2="{pol-346+18*math.sin(t*.2):.0f}" stroke="{K}" stroke-width="8"/>'
            + f'<circle cx="{tx+50:.0f}" cy="{pol-392:.0f}" r="17" fill="{ZHELEZ}" {o(3)}/>'
            + f'<circle cx="{tx+122:.0f}" cy="{pol-392:.0f}" r="17" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M{tx+180:.0f},{pol-294:.0f} L{tx+244:.0f},{pol-294:.0f}'
                    f' L{tx+236:.0f},{pol-384:.0f} L{tx+188:.0f},{pol-384:.0f} Z"'
                    f' fill="url(#stekl)" opacity=".9" {o(4)}/>'
            + f'<ellipse cx="{tx+212:.0f}" cy="{pol-340:.0f}" rx="22" ry="8"'
              f' fill="#8fb6cc" opacity=".8"/>')
    # ночник гаснет к концу плана
    gas = 1 - A.ease(A.seg(t, 1.1, .8))
    s += SL(Z_SRED, lampa(1596, pol - 300, t, .92, True))
    if gas > .25:
        s += SL(Z_SRED, teplo(1596, pol - 400, 420, 330, .50 * gas))
    # стул с брошенной одеждой и пара книг на нём
    s += SL(Z_SRED, _venskiy_stul(1760, pol + 2, 500, t, 2.0, False)
            + f'<path d="M1690,{pol-250:.0f} q70,-40 140,0 l-16,150 q-56,24 -112,0 Z"'
              f' fill="#5a6a7a" {o(5)}/>'
            + f'<rect x="1704" y="{pol-110:.0f}" width="120" height="34" rx="6"'
              f' fill="#7a3a42" {o(4)}/>')
    # мужчина в пижаме на краю кровати, ноги в тапках
    fx, fy, fh = 880, pol - 8, 540
    lozh = A.ease(A.seg(t, .2, .9))
    muz = figura(fx, fy - 236, fh, t, col="#5a6a7a", kant="#ffd98a", ph=.4,
                 naklon=6.0)
    m1, (r1x, r1y), _ = _ruka(fx, fy - 236, fh, 1, fh * .52, 40 + 14 * lozh, t,
                              "#5a6a7a", "#ffd98a", .4, 4.0)
    m2, (r2x, r2y), _ = _ruka(fx, fy - 236, fh, -1, fh * .40, 22, t,
                              "#5a6a7a", "#ffd98a", .8, 4.0)
    muz += m1 + m2
    for i in range(4):
        muz += (f'<line x1="{fx-50+i*28:.0f}" y1="{fy-236-fh*.58:.0f}"'
                f' x2="{fx-54+i*28:.0f}" y2="{fy-236-fh*.14:.0f}"'
                f' stroke="#6e8294" stroke-width="7" opacity=".8"/>')
    s += SL(Z_SRED, muz)
    s += SL(Z_SRED, f'<ellipse cx="{fx-60:.0f}" cy="{fy-4:.0f}" rx="62" ry="22"'
                    f' fill="#6a4a3c" {o(5)}/>'
            + f'<ellipse cx="{fx+66:.0f}" cy="{fy-2:.0f}" rx="62" ry="22"'
              f' fill="#6a4a3c" {o(5)}/>')
    # лист ложится под будильник
    lk = A.ease(A.seg(t, .9, .9))
    # пока рука не донесла — лист В РУКЕ (варежка его перекрывает), после —
    # ЛЕЖИТ на тумбочке под будильником. В воздухе он не висит.
    lx = r1x + (tx + 86 - r1x) * lk
    ly = r1y + (pol - 296 - r1y) * lk
    s += SL(Z_SRED, f'<g transform="rotate({-16 + 10 * lk:.1f} {lx:.0f} {ly:.0f})">'
                    f'<rect x="{lx-66:.0f}" y="{ly-46:.0f}" width="132" height="92"'
                    f' rx="6" fill="#f4efe0" {o(5)}/>'
            + f'<path d="M{lx-50:.0f},{ly-14:.0f} q32,-10 64,0" fill="none"'
              f' stroke="#9a8a68" stroke-width="6"/>'
            + f'<line x1="{lx-66:.0f}" y1="{ly:.0f}" x2="{lx+66:.0f}" y2="{ly+4:.0f}"'
              f' stroke="#d8cfbd" stroke-width="5"/></g>')
    if lk < .98:
        s += SL(Z_SRED, _varezhka(lx + 40, ly + 18, fh, t, .4))
    else:
        s += SL(Z_SRED, ten(lx, ly + 48, 70, 12, .4))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _konus_sveta(1596, pol - 400, 460, 300, -8, .40))
    s += SL(Z_SRED, _pol_shvy(pol + 14, 1078, 37, 6, "#3c3228"))
    # низ кадра: коврик, тапки второй пары, книга, корзина с бельём
    s += SL(Z_SRED, _valenki_u_dveri(430, pol + 86, .86, t)
            + _dvorovaya_utvar(1520, pol + 84, 360, t, 53, ["korzina", "korob"])
            + _kot_zhivoy(1180, pol + 72, t, 1.05, "#3a342e", .6, True, True))
    s += SL(Z_SRED, _knizhnaya_polka(70, 420, 420, t, 59, 1, 180))
    s += SL(Z_PERED, _stolb_pered(-6, 92, "#140f0c", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 1596, pol - 340, 5, 11, 170, .3))
    s += vinetka(.44)
    return s


def slovo_kotoroe_ne_vzyat_nazad(t):
    """Стол в конторе: папки, печать, календарь без года, стакан с ручками.
    Женщина в очках с ручкой, напротив мужчина в костюме. Изо рта вылетают
    слова-птички, она промахивается, и они улетают в окно."""
    rnd = random.Random(241)
    s = f'<rect width="{W}" height="{H}" fill="#242a30"/>'
    s += SL(Z_DAL, doski(0, 0, 1060, 700, 98, True, "dosk"))
    s += SL(Z_DAL, f'<rect x="1060" y="0" width="860" height="700"'
                   f' fill="#5a6470"/>')
    # окно конторы, куда улетают птички (без стока — просто окно)
    s += SL(Z_DAL, okno_izby(1420, 120, 420, 420, t, None, .0, False, True))
    s += SL(Z_DAL, f'<rect x="1400" y="100" width="460" height="40" rx="10"'
                   f' fill="#6a5a46" {o(5)}/>')
    s += SL(Z_DAL, _knizhnaya_polka(96, 320, 760, t, 61, 2, 200))
    s += SL(Z_DAL, _ramki_na_stene(880, 130, 300, t, 67, 2))
    s += SL(Z_DAL, f'<rect x="0" y="686" width="{W}" height="394"'
                   f' fill="#4a4036"/>' + _polovik(520, 760, 900, 130,
                                                   "#a89880", "#6a5a44"))
    # СТОЛ — главный предмет
    s += SL(Z_SRED, _pismennyy_stol(300, 1070, 1340, t, 400))
    sy = 1070 - 400
    # настольная лампа — живой огонёк конторы
    s += SL(Z_SRED, tusklaya_lampochka(1480, sy - 150, t, 1.3, True))
    # папки, печать, календарь, стакан с ручками
    s += SL(Z_SRED, _svitki_i_papki(360, sy - 10, t, 7, 3))
    s += SL(Z_SRED, f'<rect x="1150" y="{sy-124:.0f}" width="150" height="124"'
                    f' rx="10" fill="#6a5030" {o(6)}/>'
            + f'<rect x="1162" y="{sy-108:.0f}" width="126" height="88" rx="6"'
              f' fill="#f2ece0" {o(4)}/>'
            + f'<path d="M1180,{sy-74:.0f} q44,-14 88,0" fill="none"'
              f' stroke="#9a8a68" stroke-width="6"/>'
            + f'<rect x="1150" y="{sy-140:.0f}" width="150" height="22" rx="8"'
              f' fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="1328" y="{sy-96:.0f}" width="72" height="96" rx="10"'
                    f' fill="#5e676e" {o(5)}/>'
            + f'<rect x="1314" y="{sy-116:.0f}" width="100" height="26" rx="9"'
              f' fill="#49535b" {o(4)}/>'
            + f'<circle cx="1364" cy="{sy-14:.0f}" r="26" fill="#9c2f28"'
              f' opacity=".85" {o(3)}/>')
    s += SL(Z_SRED, f'<path d="M1046,{sy-10:.0f} L1118,{sy-10:.0f}'
                    f' L1106,{sy-130:.0f} L1058,{sy-130:.0f} Z" fill="#6e757c" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{1066+i*12:.0f}" y1="{sy-124:.0f}"'
                        f' x2="{1056+i*18:.0f}" y2="{sy-244-i*12:.0f}"'
                        f' stroke="{["#3f5c7a", "#8a4a3c", "#4a6a48", "#8a6a2c", "#5a4a62"][i]}"'
                        f' stroke-width="12" stroke-linecap="round"/>')
    # лист с мигающей строкой под подпись
    s += SL(Z_SRED, _list_bumagi(700, sy - 20, 420, 270, t, 2.0, 4, True))
    # женщина в очках за столом
    jx, jy, jh = 560, sy + 300, 560
    s += SL(Z_SRED, _venskiy_stul(jx - 40, sy + 310, 540, t, -2.0, True))
    jen = figura(jx, jy - 230, jh, t, col="#5a4a62", kant="#ffd98a", ph=.3,
                 naklon=5.0)
    j1, (w1x, w1y), _ = _ruka(jx, jy - 230, jh, 1, jh * .48,
                              30 - 44 * abs(A.w(t, 2.4, .1)), t,
                              "#5a4a62", "#ffd98a", .3, 6.0)
    j2, (w2x, w2y), _ = _ruka(jx, jy - 230, jh, 1, jh * .36, 56, t,
                              "#5a4a62", "#ffd98a", .7, 4.0)
    jen += j1 + j2
    jen += _ochki(jx, jy - 230 - jh * .845, .78, t)
    s += SL(Z_SRED, jen)
    s += SL(Z_SRED, f'<line x1="{w1x:.0f}" y1="{w1y:.0f}" x2="{w1x+64:.0f}"'
                    f' y2="{w1y-44:.0f}" stroke="#2b3038" stroke-width="13"'
                    f' stroke-linecap="round"/>')
    # мужчина в костюме напротив, обе руки сложены на столе
    mx, my, mh = 1316, sy + 320, 600
    muz = figura(mx, my - 250, mh, t, col="#2f3540", kant="#ffd98a", ph=.8,
                 naklon=-3.0)
    m1, (v1x, v1y), _ = _ruka(mx, my - 250, mh, -1, mh * .42, 58, t,
                              "#2f3540", "#ffd98a", .8, 3.0)
    m2, (v2x, v2y), _ = _ruka(mx, my - 250, mh, -1, mh * .34, 72, t,
                              "#2f3540", "#ffd98a", .2, 3.0)
    muz += m1 + m2
    muz += (f'<path d="M{mx-22:.0f},{my-250-mh*.60:.0f} L{mx+22:.0f},{my-250-mh*.60:.0f}'
            f' L{mx+10:.0f},{my-250-mh*.40:.0f} L{mx-10:.0f},{my-250-mh*.40:.0f} Z"'
            f' fill="#9c2f28" {o(3)}/>')
    s += SL(Z_SRED, muz)
    # СЛОВА-ПТИЧКИ: вылетают изо рта, рука промахивается, уходят в окно
    for i in range(4):
        k = A.seg(t, .5 + i * .55, 2.6)
        # старт дальше от лица: первая птица стояла у самого глаза
        bx = jx + 190 + (1560 - jx - 130) * A.ease(k)
        by = jy - 230 - jh * .78 - 90 - 240 * math.sin(math.pi * k) - 30 * k
        kr = 26 * A.w(t * 2.4, 1.0, i * .3)
        s += SL(Z_SRED, f'<g transform="translate({bx:.0f} {by:.0f})">'
                        f'<ellipse cx="0" cy="0" rx="40" ry="24" fill="#e8dcc0" {o(4)}/>'
                f'<circle cx="32" cy="-14" r="18" fill="#efe6d2" {o(3)}/>'
                f'<path d="M48,-16 l24,8 l-24,8 Z" fill="#d8a53c" {o(2)}/>'
                f'<circle cx="38" cy="-18" r="4" fill="{K}"/>'
                f'<path d="M-6,-6 q24,{-30 - kr:.0f} 54,{-14 - kr * .4:.0f}'
                f' q-26,{26 + kr * .5:.0f} -56,{12:.0f} Z" fill="#cfc3a4" {o(3)}/>'
                f'<path d="M-36,4 l-40,{10 + kr * .3:.0f} l34,{6:.0f} Z"'
                f' fill="#d8cfbd" {o(2)}/></g>')
    s += SL(Z_SRED, ten(jx, sy + 306, 150, 22, .4))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(w2x, w2y, jh, t, .7)
            + _varezhka(v1x, v1y, mh, t, .8))
    s += SL(Z_SRED, _konus_sveta(1480, sy - 150, 520, 300, 10, .40))
    s += SL(Z_SRED, _pol_shvy(760, 1078, 41, 6, "#3a3228"))
    # низ кадра
    s += SL(Z_PERED, _yaschiki(96, 1072, t, 23, 2, .88)
            + _dvorovaya_utvar(1560, 1068, 340, t, 71, ["korzina", "korob"])
            + _kot_zhivoy(1240, 1058, t, 1.1, "#3e3833", .3))
    s += SL(Z_PERED, _stolb_pered(1862, 86, "#191410", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 1480, sy - 190, 5, 13, 160, .26))
    s += vinetka(.42)
    return s


def chetyre_bumagi_pod_podushkoy(t):
    """Кровать с лоскутным покрывалом, большая пуховая подушка на пол-кадра,
    на тумбочке лампа, очки, клубок. Бабушка в сорочке и чепце приподнимает
    подушку и кладёт под неё по одной четыре бумаги со значками."""
    rnd = random.Random(251)
    pol = 972
    s = f'<rect width="{W}" height="{H}" fill="#201a16"/>'
    s += SL(Z_DAL, brevna(0, 40, 1120, pol - 40, 98)
            + brevna(1120, 40, 800, pol - 40, 98))
    s += SL(Z_DAL, _kover_na_stene(120, 130, 880, 430, t, 19))
    s += SL(Z_DAL, _polka_s_utvaryu(1180, 250, 620, t, 73, 5))
    s += SL(Z_DAL, _polka_s_utvaryu(100, 600, 580, t, 149, 5))
    s += SL(Z_DAL, _knizhnaya_polka(760, 250, 380, t, 151, 1, 180))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-14:.0f}" width="{W}"'
                   f' height="{H-pol+14:.0f}" fill="#5e4a34"/>'
            + polovicy(pol + 16))
    s += SL(Z_DAL, _polovik(620, pol + 30, 700, 96))
    # КРОВАТЬ и ПОДУШКА — главный предмет
    s += SL(Z_SRED, _krovat(360, pol, 1180, t, 11, True, 320))
    pod = A.ease(A.seg(t, .5, 1.1)) * (1 - A.ease(A.seg(t, 4.4, .7)))
    hlop = A.ease(A.seg(t, 4.9, .5)) * (1 - A.ease(A.seg(t, 5.5, .5)))
    s += SL(Z_SRED, _podushka(700, pol - 440, 520, 250, t, .2, pod, hlop))
    # бумаги уходят под подушку по одной
    vidy = ("ruka", "galka", "cherta", "pero")
    for i in range(4):
        k = A.ease(A.seg(t, 1.0 + i * .75, .7))
        bx = 1140 - 300 * k
        by = pol - 520 + 150 * k
        if k < 1.0:
            s += SL(Z_SRED, _bumaga_znachok(bx, by, .92, vidy[i],
                                            -14 + 20 * k + 6 * A.w(t, 2.0, i * .2)))
        else:
            s += SL(Z_SRED, _bumaga_znachok(760 + i * 34, pol - 356, .74,
                                            vidy[i], -8 + i * 5))
    # тумбочка: лампа, очки, клубок
    tx = 150
    s += SL(Z_SRED, f'{ten(tx + 110, pol + 6, 120, 18, .45)}'
                    f'<rect x="{tx:.0f}" y="{pol-300:.0f}" width="230" height="300"'
                    f' rx="10" fill="url(#derev)" {o(6)}/>'
            + f'<rect x="{tx+16:.0f}" y="{pol-272:.0f}" width="198" height="116"'
              f' rx="7" fill="#8a6a44" {o(4)}/>'
            + f'<rect x="{tx+88:.0f}" y="{pol-220:.0f}" width="54" height="16"'
              f' rx="7" fill="url(#zhel)" {o(3)}/>')
    gas = 1 - A.ease(A.seg(t, 5.8, .7))
    s += SL(Z_SRED, lampa(tx + 110, pol - 306, t, 1.05, False))
    s += SL(Z_SRED, teplo(tx + 110, pol - 430, 480, 380, .50 * gas))
    s += SL(Z_SRED, _ochki(tx + 196, pol - 318, 1.0, t))
    s += SL(Z_SRED, f'<circle cx="{tx+40:.0f}" cy="{pol-330:.0f}" r="44"'
                    f' fill="#8a4a52" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{tx+4:.0f},{pol-352+i*14:.0f}'
                        f' q{40:.0f},{-14:.0f} {76:.0f},{6:.0f}" fill="none"'
                        f' stroke="#a35a62" stroke-width="5" opacity=".85"/>')
    s += SL(Z_SRED, f'<line x1="{tx+84:.0f}" y1="{pol-320:.0f}" x2="{tx+150:.0f}"'
                    f' y2="{pol-284:.0f}" stroke="#8a4a52" stroke-width="6"/>')
    # бабушка у кровати: ложится к концу плана
    lozh = A.ease(A.seg(t, 5.4, 1.2))
    bx, by_, bh = 1380, pol + 18, 760 - 300 * lozh
    bab = figura(bx + 90 * lozh, by_ - 240 * lozh, bh, t, col="#e4dcc8",
                 kant="#ffd98a", platok=True, ph=.4, naklon=8 - 24 * lozh)
    b1, (q1x, q1y), _ = _ruka(bx + 90 * lozh, by_ - 240 * lozh, bh, -1,
                              bh * .48, 24 - 30 * pod, t,
                              "#e4dcc8", "#ffd98a", .4, 4.0)
    b2, (q2x, q2y), _ = _ruka(bx + 90 * lozh, by_ - 240 * lozh, bh, -1,
                              bh * .38, 48 - 20 * pod, t,
                              "#e4dcc8", "#ffd98a", .8, 4.0)
    bab += b1 + b2
    # чепец с рюшем поверх платка
    bab += (f'<path d="M{bx+90*lozh-96:.0f},{by_-240*lozh-bh*.90:.0f}'
            f' q{96:.0f},{-54:.0f} {192:.0f},0 q{-20:.0f},{26:.0f} {-192:.0f},0 Z"'
            f' fill="#f2ece0" {o(4)}/>')
    s += SL(Z_SRED, bab)
    s += SL(Z_SRED, ten(bx + 90 * lozh, by_ + 6, 160, 24, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(q1x, q1y, bh, t, .4))
    s += SL(Z_SRED, _konus_sveta(tx + 110, pol - 330, 560, 330, -14, .42))
    s += SL(Z_SRED, _pol_shvy(pol + 16, 1078, 43, 6, "#4a3824"))
    # лавка с крынками у стены и вязанки лука — обжитой средний план
    s += SL(Z_SRED, _lavka_krupno(96, pol - 10, 620, t, 130, False))
    for i in range(5):
        s += SL(Z_SRED, krynka(150 + i * 120, pol - 140, 1.42 + (i % 3) * .18))
    # два сундука с кованой полосой и прялка в углу
    for i in (0, 1):
        cx_ = 1540 + i * 250
        s += SL(Z_SRED, f'<rect x="{cx_-110:.0f}" y="{pol-180:.0f}" width="220"'
                        f' height="180" rx="10" fill="url(#derev)" {o(6)}/>'
                f'<path d="M{cx_-110:.0f},{pol-180:.0f} q{110:.0f},{-60:.0f}'
                f' {220:.0f},0 Z" fill="url(#med)" {o(5)}/>'
                f'<rect x="{cx_-116:.0f}" y="{pol-126:.0f}" width="232" height="20"'
                f' rx="7" fill="{ZHELEZ}" {o(3)}/>'
                f'<rect x="{cx_-22:.0f}" y="{pol-104:.0f}" width="44" height="34"'
                f' rx="8" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="100" y="{pol-430:.0f}" width="40" height="430"'
                    f' rx="12" fill="url(#derev)" {o(6)}/>'
            + f'<path d="M80,{pol-430:.0f} q40,-70 80,0 Z" fill="#6a5030" {o(5)}/>'
            + f'<ellipse cx="120" cy="{pol-150:.0f}" rx="86" ry="30"'
              f' fill="url(#dosk)" {o(5)}/>')
    # рушники на жерди под потолком
    for i in range(4):
        rx_ = 860 + i * 150
        kach = 2.4 * A.w(t, 3.6, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {rx_:.0f} 150)">'
                        f'<rect x="{rx_-44:.0f}" y="150" width="88" height="270"'
                        f' rx="8" fill="url(#rush)" {o(5)}/>'
                f'<rect x="{rx_-44:.0f}" y="300" width="88" height="16"'
                f' fill="{TKAN}" opacity=".8"/>'
                f'<rect x="{rx_-44:.0f}" y="386" width="88" height="16"'
                f' fill="{TKAN2}" opacity=".7"/></g>')
    s += SL(Z_SRED, f'<rect x="820" y="132" width="700" height="22" rx="9"'
                    f' fill="url(#derev)" {o(5)}/>')
    # ушат, короб с шерстью и подсвечник у лавки
    s += SL(Z_SRED, _dvorovaya_utvar(760, pol - 8, 420, t, 181,
                                     ["kadka", "korob", "korzina"]))
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{1700+i*74:.0f},240 q{-26:.0f},{80:.0f}'
                        f' {4:.0f},{150:.0f} q{30:.0f},{20:.0f} {44:.0f},{-14:.0f}'
                        f' q{14:.0f},{-76:.0f} {-18:.0f},{-136:.0f} Z"'
                        f' fill="#c9a05a" {o(5)}/>'
                f'<line x1="{1708+i*74:.0f}" y1="240" x2="{1724+i*74:.0f}"'
                f' y2="200" stroke="#8a7a46" stroke-width="7"/>')
    # низ кадра: сундук, валенки, кот, корзина с клубками
    s += SL(Z_SRED, _yaschiki(1600, pol + 86, t, 29, 2, .9)
            + _valenki_u_dveri(1300, pol + 96, .92, t)
            + _kot_zhivoy(560, pol + 76, t, 1.15, "#3b342f", .5, True, True)
            + _dvorovaya_utvar(96, pol + 96, 280, t, 79, ["korzina"]))
    s += SL(Z_PERED, _stolb_pered(1874, 70, "#17120e", 0, H))
    s += SL(Z_LETIT, iskra_let(t, tx + 110, pol - 360, 6, 17, 180, .34))
    s += vinetka(.44)
    return s


def chashi_vesov_segodnya_i_zavtra(t):
    """Кухонный стол: старые чашечные весы на пол-кадра, рядом чайник,
    записная книжка и карандаш. Женщина подпирает щёку левой ладонью,
    правой перекладывает листок с чаши «сегодня» на чашу «завтра»."""
    rnd = random.Random(257)
    pol = 980
    s = f'<rect width="{W}" height="{H}" fill="#2a2a2e"/>'
    s += SL(Z_DAL, _kafel(0, 30, 1060, 630, t, 23, "#d0d8d8"))
    s += SL(Z_DAL, doski(1060, 0, 860, 840, 92, True, "dosk"))
    s += SL(Z_DAL, doski(1060, 840, 860, 140, 92, True, "dosk"))
    # правая стена: полка с банками и связка сушёных травок в центре кадра
    s += SL(Z_DAL, _polka_s_utvaryu(1200, 420, 600, t, 173, 4))
    s += SL(Z_DAL, _polki_otkrytye(1120, 120, 740, t, 83, 2, True, .0))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-10:.0f}" width="{W}"'
                   f' height="{H-pol+10:.0f}" fill="#5a4c3c"/>'
            + _polovik(560, pol + 22, 820, 92, "#c0b094", "#7a6a52"))
    s += SL(Z_DAL, tusklaya_lampochka(620, 150, t, 1.2, True))
    # навесной шкафчик и полка в середине стены: центр кадра не пустует
    # ШКАФЧИК УХОДИТ ВЛЕВО: он стоял ровно за весами, и чашечные весы
    # пропадали в его тёмной дверце (осмотр порции 2)
    s += SL(Z_DAL, f'<rect x="60" y="240" width="520" height="300" rx="10"'
                   f' fill="url(#derev)" {o(6)}/>')
    for i in (0, 1):
        s += SL(Z_DAL, f'<rect x="{80+i*256:.0f}" y="262" width="236"'
                       f' height="256" rx="8" fill="#8a6a44" {o(5)}/>'
                f'<rect x="{102+i*256:.0f}" y="286" width="192" height="208"'
                f' rx="6" fill="url(#stekl)" opacity=".62" {o(3)}/>'
                f'<rect x="{186+i*256:.0f}" y="376" width="44" height="14" rx="7"'
                f' fill="url(#zhel)" {o(3)}/>')
    for i in range(4):
        s += SL(Z_DAL, _kruzhka(110 + i * 130, 530, .86, 0, "#eceff0", 1))
    s += SL(Z_DAL, _polki_otkrytye(70, 560, 460, t, 157, 1, True, .0))
    # за весами — светлый кафель и тёмная полоса под ними: латунь читается
    s += SL(Z_DAL, _kafel(620, 180, 700, 460, t, 191, "#e2e8e8"))
    # СТОЛ — крупный предмет
    s += SL(Z_SRED, stol(260, pol - 330, 1240, 40, True))
    sy = pol - 330
    # ВЕСЫ: чаша «сегодня» ходит ходуном, потом встают ровно
    per = A.ease(A.seg(t, 3.0, 1.4))
    dreb = (1 - per) * (1 - A.ease(A.seg(t, 2.6, .5)))
    # ВЕСЫ КРУПНЕЕ И ВЫШЕ: главный предмет сцены читается со стоп-кадра
    # ВЕСЫ ПРАВЕЕ: при x=960 левая чаша стояла ровно за фигурой (осмотр)
    s += SL(Z_SRED, _vesy(1180, sy - 8, t, 1.26, -.55 * (1 - per) + .04 * per,
                          dreb, 340))
    # листок перекладывается с левой чаши на правую
    lk = per
    lx = 1180 - 378 + 756 * lk
    ly = sy - 420 + 140 - 60 * math.sin(math.pi * lk)
    s += SL(Z_SRED, f'<g transform="rotate({-8 + 16 * lk:.1f} {lx:.0f} {ly:.0f})">'
                    f'<rect x="{lx-56:.0f}" y="{ly-40:.0f}" width="112" height="76"'
                    f' rx="6" fill="#f4efe0" {o(5)}/>'
            + f'<path d="M{lx-40:.0f},{ly-12:.0f} q26,-10 52,0" fill="none"'
              f' stroke="#9a8a68" stroke-width="6"/>'
            + f'<path d="M{lx-40:.0f},{ly+10:.0f} q26,-8 52,2" fill="none"'
              f' stroke="#b8a888" stroke-width="5"/></g>')
    # чайник, записная книжка, карандаш, чашка
    s += SL(Z_SRED, _chaynik(400, sy - 8, 1.2, t))
    s += SL(Z_SRED, par(400, sy - 140, t, 5, .5, 200, .44, 1.1))
    s += SL(Z_SRED, f'<rect x="1320" y="{sy-66:.0f}" width="190" height="66"'
                    f' rx="8" fill="#7a3a42" {o(6)}/>'
            + f'<rect x="1332" y="{sy-54:.0f}" width="166" height="48" rx="5"'
              f' fill="#f2ece0" {o(3)}/>'
            + f'<path d="M1350,{sy-30:.0f} q40,-12 80,2" fill="none"'
              f' stroke="#9a8a68" stroke-width="5"/>'
            + f'<line x1="1540" y1="{sy-16:.0f}" x2="1680" y2="{sy-40:.0f}"'
              f' stroke="#c9a05a" stroke-width="14" stroke-linecap="round"/>'
            + f'<path d="M1680,{sy-40:.0f} l26,-6 l-8,20 Z" fill="#3a3a42" {o(2)}/>')
    s += SL(Z_SRED, _kruzhka(1210, sy - 6, 1.05, 0, "#efe3d4", 1))
    # под столом и справа от него: корзина, вёдра, ящики, хлебница
    s += SL(Z_SRED, _dvorovaya_utvar(1080, pol - 4, 420, t, 167,
                                     ["korzina", "vedro", "korob"]))
    s += SL(Z_SRED, _yaschiki(1560, pol - 6, t, 169, 2, .96))
    # под столом: корзина с клубками, кадушка и кошачья плошка
    s += SL(Z_SRED, _dvorovaya_utvar(620, pol - 10, 420, t, 179,
                                     ["kadka", "korzina", "vedro"]))
    s += SL(Z_SRED, f'<ellipse cx="1040" cy="{pol-24:.0f}" rx="56" ry="20"'
                    f' fill="url(#glina)" {o(5)}/>'
            + f'<ellipse cx="1040" cy="{pol-30:.0f}" rx="42" ry="13"'
              f' fill="#8a5a30" opacity=".9"/>')
    s += SL(Z_SRED, f'<rect x="1120" y="{sy-96:.0f}" width="210" height="86"'
                    f' rx="18" fill="url(#solom)" {o(5)}/>'
            + f'<path d="M1130,{sy-96:.0f} q104,-42 190,0" fill="none"'
              f' stroke="#8a6a3c" stroke-width="9"/>'
            + karavay(1226, sy - 92, .5, False))
    # женщина за столом: подбородок на левой ладони, правая работает
    fx, fy, fh = 500, pol + 20, 640
    s += SL(Z_SRED, _venskiy_stul(430, pol + 10, 560, t, -2.0, True))
    jen = figura(fx, fy - 250, fh, t, col="#6a5a4a", kant="#ffd98a", ph=.3,
                 naklon=-6.0)
    j1, (n1x, n1y), _ = _ruka_so_sgibom(fx, fy - 250, fh, -1, fh * .26, 34,
                                        fh * .30, -48, t, "#6a5a4a",
                                        "#ffd98a", .3, 3.0)
    j2, (n2x, n2y), _ = _ruka(fx, fy - 250, fh, 1, fh * .56, 30 + 16 * lk, t,
                              "#6a5a4a", "#ffd98a", .7, 5.0)
    jen += j1 + j2
    # кардиган: borта и пуговицы
    jen += (f'<path d="M{fx-56:.0f},{fy-250-fh*.60:.0f} L{fx-20:.0f},{fy-250-fh*.58:.0f}'
            f' L{fx-26:.0f},{fy-250-fh*.16:.0f} L{fx-66:.0f},{fy-250-fh*.18:.0f} Z"'
            f' fill="#55473a" {o(4)}/>'
            f'<path d="M{fx+56:.0f},{fy-250-fh*.60:.0f} L{fx+20:.0f},{fy-250-fh*.58:.0f}'
            f' L{fx+26:.0f},{fy-250-fh*.16:.0f} L{fx+66:.0f},{fy-250-fh*.18:.0f} Z"'
            f' fill="#55473a" {o(4)}/>')
    s += SL(Z_SRED, jen)
    s += SL(Z_SRED, ten(fx, pol + 10, 150, 22, .4))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(n1x, n1y, fh, t, .3) + _varezhka(n2x, n2y, fh, t, .7))
    s += SL(Z_SRED, _pol_shvy(pol + 10, 1078, 47, 6, "#443828"))
    # низ кадра
    s += SL(Z_SRED, _dvorovaya_utvar(1540, pol + 86, 360, t, 89,
                                     ["vedro", "korzina"])
            + _yaschiki(96, pol + 80, t, 31, 2, .8)
            + _kot_zhivoy(1000, pol + 70, t, 1.0, "#443d37", .8)
            + kartoshka(1300, pol + 96, t, 6, 6, .95))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += SL(Z_LETIT, par(1180, sy - 520, t, 3, .26, 150, .28, 1.2))
    s += vinetka(.42)
    return s


def toroplivyy_gost_v_dveryah(t):
    """Прихожая: вешалка с пальто, зеркало, зонт в подставке, коврик.
    Напористый мужчина в плаще тычет ручкой в бумагу, хозяйка спокойно
    выставила ладонь и держится за ручку двери."""
    rnd = random.Random(263)
    pol = 968
    s = f'<rect width="{W}" height="{H}" fill="#262a2e"/>'
    s += SL(Z_DAL, doski(0, 0, 1180, pol, 96, True, "dosk"))
    s += SL(Z_DAL, f'<rect x="1180" y="0" width="740" height="{pol:.0f}"'
                   f' fill="#3f4650"/>')
    s += SL(Z_DAL, f'<rect x="0" y="{pol-12:.0f}" width="{W}"'
                   f' height="{H-pol+12:.0f}" fill="#4a4136"/>')
    s += SL(Z_DAL, tusklaya_lampochka(520, 140, t, 1.15, True))
    # ВЕШАЛКА С ПАЛЬТО — крупный предмет
    s += SL(Z_SRED, _veshalka_s_paltom(120, 230, 1020, t, 3))
    # зеркало и зонт
    s += SL(Z_SRED, f'<rect x="1176" y="250" width="34" height="520" rx="12"'
                    f' fill="#6a5030" {o(6)}/>'
            + f'<path d="M1210,270 L1210,740 Q1210,760 1230,760 L1340,760'
              f' Q1360,760 1360,740 L1360,270 Q1360,250 1340,250 L1230,250'
              f' Q1210,250 1210,270 Z" fill="#6a5030" {o(6)}/>'
            + f'<rect x="1226" y="266" width="118" height="478" rx="10"'
              f' fill="#4a5a66" opacity=".92" {o(3)}/>'
            + f'<path d="M1240,700 L1300,300 L1330,300 L1264,700 Z"'
              f' fill="#9fc0d4" opacity="{.18+.1*abs(A.w(t,3.4)):.2f}"/>')
    s += SL(Z_SRED, _zont_v_podstavke(1420, pol - 10, t, 1.15))
    # обувная полка во всю вешалку и комод прихожей
    s += SL(Z_SRED, f'<rect x="150" y="{pol-240:.0f}" width="940" height="26"'
                    f' rx="8" fill="url(#dosk)" {o(5)}/>'
            + f'<rect x="150" y="{pol-130:.0f}" width="940" height="26" rx="8"'
              f' fill="url(#dosk)" {o(5)}/>')
    for i in range(6):
        bx = 200 + i * 150
        s += SL(Z_SRED, f'<path d="M{bx-54:.0f},{pol-240:.0f}'
                        f' q{20:.0f},{-70:.0f} {60:.0f},{-66:.0f}'
                        f' q{44:.0f},{10:.0f} {46:.0f},{66:.0f} Z"'
                        f' fill="{["#3a2e26", "#5a3a2c", "#2e3540"][i % 3]}" {o(5)}/>'
                f'<path d="M{bx-30:.0f},{pol-130:.0f} l{86:.0f},0 l{-10:.0f},{-80:.0f}'
                f' l{-62:.0f},0 Z" fill="{["#4a3a2c", "#3f4650"][i % 2]}" {o(4)}/>')
    s += SL(Z_SRED, _dvorovaya_utvar(1140, pol - 6, 400, t, 163,
                                     ["korzina", "korob"]))
    # дверь, которую хозяйка плавно закрывает
    zak = A.ease(A.seg(t, 2.8, 1.5))
    s += SL(Z_SRED, dver(1560, pol - 840, 360, 840, .55 - .5 * zak,
                         "url(#derev)", True, True))
    s += SL(Z_SRED, f'<rect x="1532" y="{pol-872:.0f}" width="416" height="40"'
                    f' rx="10" fill="#5b4428" {o(6)}/>')
    # мужчина в плаще в дверях
    gx, gy, gh = 1476, pol + 18, 790
    hlop = A.ease(A.seg(t, 2.1, .6))
    _figury_kadra((1476, pol + 18, 790), (940, pol + 44, 820))
    muz = figura(gx, gy, gh, t, col="#4a4e46", kant="#cfe4f5", shapka=True,
                 ph=.2, naklon=-5.0)
    g1, (t1x, t1y), _ = _ruka_mimo(gx, gy, gh, -1, gh * .40,
                              18 + 12 * A.w(t, .5, .1) * (1 - hlop), t,
                              "#4a4e46", "#cfe4f5", .2, 7.0)
    g2, (t2x, t2y), _ = _ruka_mimo(gx, gy, gh, -1, gh * .30, 44, t,
                              "#4a4e46", "#cfe4f5", .6, 5.0)
    muz += g1 + g2
    muz += (f'<path d="M{gx-70:.0f},{gy-gh*.60:.0f} q{70:.0f},{-28:.0f} {140:.0f},0'
            f' L{gx+86:.0f},{gy-gh*.10:.0f} q{-86:.0f},{26:.0f} {-172:.0f},0 Z"'
            f' fill="#565a50" {o(6)}/>'
            f'<path d="M{gx:.0f},{gy-gh*.58:.0f} L{gx+14:.0f},{gy-gh*.12:.0f}"'
            f' fill="none" stroke="{K}" stroke-width="5" opacity=".6"/>')
    s += SL(Z_SRED, muz)
    # раскрытая папка в левой руке: захлопывается
    s += SL(Z_SRED, f'<g transform="rotate({-10 + 8 * hlop:.1f} {t2x:.0f} {t2y:.0f})">'
                    f'<path d="M{t2x-130:.0f},{t2y-70:.0f} L{t2x+8:.0f},{t2y-86:.0f}'
                    f' L{t2x+8:.0f},{t2y+54:.0f} L{t2x-130:.0f},{t2y+70:.0f} Z"'
                    f' fill="#7a4a3c" {o(5)}/>'
            + f'<path d="M{t2x+8:.0f},{t2y-86:.0f}'
              f' L{t2x+8+130*(1-hlop):.0f},{t2y-70-16*(1-hlop):.0f}'
              f' L{t2x+8+130*(1-hlop):.0f},{t2y+70-16*(1-hlop):.0f}'
              f' L{t2x+8:.0f},{t2y+54:.0f} Z" fill="#f2ece0" {o(5)}/>'
            + f'<path d="M{t2x+30:.0f},{t2y-40:.0f} q{40*(1-hlop):.0f},{-12:.0f}'
              f' {80*(1-hlop):.0f},{2:.0f}" fill="none" stroke="#9a8a68"'
              f' stroke-width="6"/></g>')
    # ручка тычет в бумагу
    tyk = 16 * A.w(t, .45, .2) * (1 - hlop)
    s += SL(Z_SRED, f'<line x1="{t1x:.0f}" y1="{t1y:.0f}" x2="{t1x-70-tyk:.0f}"'
                    f' y2="{t1y+26:.0f}" stroke="#2b3038" stroke-width="13"'
                    f' stroke-linecap="round"/>')
    # хозяйка на коврике: правая ладонь вперёд, левая на ручке двери
    hx, hy, hh = 940, pol + 44, 820
    hoz = figura(hx, hy, hh, t, col="#6a4a52", kant="#ffd98a", platok=False,
                 ph=.7, naklon=2.0)
    h1, (d1x, d1y), _ = _ruka_mimo(hx, hy, hh, 1, hh * .44, 4, t,
                              "#6a4a52", "#ffd98a", .7, 3.0)
    h2, (d2x, d2y), _ = _ruka_mimo(hx, hy, hh, 1, hh * .30, 40, t,
                              "#6a4a52", "#ffd98a", .3, 3.0)
    hoz += h1 + h2
    s += SL(Z_SRED, hoz)
    # ладонь-стоп: раскрытая кисть рукавицей (пальцев не рисуем)
    s += SL(Z_SRED, f'<ellipse cx="{d1x+34:.0f}" cy="{d1y:.0f}" rx="46" ry="58"'
                    f' fill="#e8d8c0" {o(6)}/>'
            + f'<path d="M{d1x+54:.0f},{d1y-30:.0f} q24,16 0,40" fill="none"'
              f' stroke="#e8d8c0" stroke-width="22" stroke-linecap="round"/>')
    s += SL(Z_SRED, _polovik(820, pol + 20, 420, 110, "#8a5a52", "#c9a05a"))
    s += SL(Z_SRED, ten(hx, hy + 8, 176, 26, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(t1x, t1y, gh, t, .2, "#dcd0bc")
            + _varezhka(t2x, t2y, gh, t, .6, "#dcd0bc")
            + _varezhka(d2x, d2y, hh, t, .3))
    s += SL(Z_SRED, _pol_shvy(pol + 12, 1078, 53, 6, "#3e3428"))
    # низ кадра
    s += SL(Z_SRED, _valenki_u_dveri(680, pol + 96, 1.0, t)
            + _gorodskoy_hlam(96, pol + 92, 420, t, 37,
                              ["korobka", "yaschik", "kust"])
            + _kot_zhivoy(1260, pol + 80, t, 1.0, "#423b35", .4))
    s += SL(Z_PERED, _stolb_pered(-8, 96, "#171210", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 520, 190, 5, 19, 150, .24))
    s += vinetka(.42)
    return s


def listok_chislennika_za_hozyayku(t):
    """Стена прихожей: отрывной численник на пол-кадра, под ним полочка с
    ключами, щётка для обуви, варежки. Хозяйка показывает на сегодняшний
    листок, за её плечом полупрозрачным контуром кивает бабушка."""
    rnd = random.Random(269)
    pol = 960
    s = f'<rect width="{W}" height="{H}" fill="#282c30"/>'
    s += SL(Z_DAL, doski(0, 0, 1080, pol, 100, True, "dosk"))
    s += SL(Z_DAL, f'<rect x="1080" y="0" width="840" height="{pol:.0f}"'
                   f' fill="#454c56"/>')
    for i in range(9):
        s += SL(Z_DAL, f'<rect x="{1090+i*94:.0f}" y="0" width="46"'
                       f' height="{pol:.0f}" fill="#4e5660" opacity=".6"/>')
    s += SL(Z_DAL, _ramki_na_stene(1150, 160, 700, t, 97, 4))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-12:.0f}" width="{W}"'
                   f' height="{H-pol+12:.0f}" fill="#4e4234"/>'
            + _polovik(640, pol + 26, 700, 96))
    s += SL(Z_DAL, tusklaya_lampochka(1480, 130, t, 1.1, True))
    # ПОЛКА во всю стену — крупный предмет, на ней хозяйство прихожей
    s += SL(Z_SRED, f'<rect x="60" y="640" width="1020" height="34" rx="10"'
                    f' fill="url(#dosk)" {o(6)}/>'
            + f'<rect x="60" y="674" width="1020" height="18" rx="7"'
              f' fill="#5b4428" {o(4)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{130+i*220:.0f},692 l26,44 l-30,0 Z"'
                        f' fill="{ZHELEZ}" {o(3)}/>')
    # ЧИСЛЕННИК — главный предмет (листок пустой: цифру кладёт надпись)
    s += SL(Z_SRED, _chislennik(300, 160, 390, 460, t, .0))
    # ключи на крючках покачиваются
    for i in range(3):
        s += SL(Z_SRED, _svyazka_klyuchey(760 + i * 110, 730 + (i % 2) * 24, t,
                                          .96, i * .3, 3))
    # щётка для обуви и варежки на полке
    s += SL(Z_SRED, f'<rect x="150" y="588" width="230" height="52" rx="16"'
                    f' fill="#6a5030" {o(6)}/>')
    for i in range(14):
        s += SL(Z_SRED, f'<line x1="{162+i*16:.0f}" y1="640" x2="{162+i*16:.0f}"'
                        f' y2="672" stroke="#2e2620" stroke-width="7"/>')
    for i in (0, 1):
        mx = 470 + i * 150
        s += SL(Z_SRED, f'<path d="M{mx:.0f},590 q{-34:.0f},{34:.0f} {-18:.0f},{50:.0f}'
                        f' q{40:.0f},{14:.0f} {64:.0f},{-4:.0f}'
                        f' q{12:.0f},{-34:.0f} {-10:.0f},{-48:.0f} Z"'
                        f' fill="{["#8a4a52", "#3f5c7a"][i]}" {o(5)}/>'
                f'<path d="M{mx+54:.0f},612 q{30:.0f},{10:.0f} {18:.0f},{32:.0f}"'
                f' fill="none" stroke="{["#8a4a52", "#3f5c7a"][i]}" stroke-width="18"/>')
    s += SL(Z_SRED, _polka_s_utvaryu(1180, 400, 620, t, 101, 4))
    # контур бабушки за плечом: полупрозрачная фигура, кивает
    kiv = 7 * A.w(t, 1.7, .2)
    kx, ky, kh = 1230, pol + 30, 700
    _figury_kadra((1230, pol + 30, 700), (880, pol + 46, 828))
    kon = figura(kx, ky, kh, t, col="#9fb4c8", kant="#eaf4ff", platok=True,
                 ph=.5, op=.95, naklon=kiv * .3)
    k1, (u1x, u1y), _ = _ruka_mimo(kx, ky, kh, -1, kh * .34, 56, t,
                              "#9fb4c8", "#eaf4ff", .5, 3.0)
    k2, (u2x, u2y), _ = _ruka_mimo(kx, ky, kh, 1, kh * .32, 60, t,
                              "#9fb4c8", "#eaf4ff", .1, 3.0)
    kon += k1 + k2
    # ФИГУРА НЕПРОЗРАЧНАЯ (op не ниже 0,9): сквозь «контур бабушки» была
    # видна мебель, и фигура читалась дырой. Память показана ХОЛОДНЫМ
    # цветом и светлым кантом, а не прозрачностью.
    s += SL(Z_SRED, f'<g opacity=".92">{kon}</g>')
    # хозяйка: правая показывает на листок, левая на груди
    hx, hy, hh = 880, pol + 46, 828
    pok = A.ease(A.seg(t, .3, .9))
    hoz = figura(hx, hy, hh, t, col="#4a5a6a", kant="#ffd98a", ph=.8,
                 naklon=-4.0)
    h1, (y1x, y1y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .48, -26 - 22 * pok, t,
                              "#4a5a6a", "#ffd98a", .8, 4.0)
    h2, (y2x, y2y), _ = _ruka_sgib_mimo(hx, hy, hh, 1, hh * .22, 50,
                                        hh * .24, -6, t, "#4a5a6a",
                                        "#ffd98a", .2, 3.0)
    hoz += h1 + h2
    s += SL(Z_SRED, hoz)
    s += SL(Z_SRED, f'<ellipse cx="{y1x-20:.0f}" cy="{y1y-14:.0f}" rx="40" ry="30"'
                    f' fill="#e8d8c0" {o(5)}/>'
            + f'<path d="M{y1x-44:.0f},{y1y-22:.0f} l-70,-26" fill="none"'
              f' stroke="#e8d8c0" stroke-width="20" stroke-linecap="round"/>')
    s += SL(Z_SRED, ten(hx, hy + 8, 178, 26, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, _varezhka(y2x, y2y, hh, t, .2))
    s += SL(Z_SRED, _pol_shvy(pol + 12, 1078, 59, 6, "#413528"))
    # низ кадра
    s += SL(Z_SRED, _valenki_u_dveri(400, pol + 92, 1.05, t)
            + _gorodskoy_hlam(1480, pol + 90, 420, t, 41,
                              ["korobka", "kust", "yaschik"])
            + _kot_zhivoy(1080, pol + 76, t, 1.1, "#3f3933", .7)
            + _dvorovaya_utvar(96, pol + 96, 260, t, 103, ["korzina"]))
    s += SL(Z_PERED, ramka_pp("levo"))
    s += SL(Z_LETIT, iskra_let(t, 1480, 180, 5, 23, 140, .22))
    s += vinetka(.42)
    return s


def hvastun_na_zavalinke(t):
    """Завалинка у избы: трое мужиков. Средний в новой шапке встал, бьёт себя
    в грудь и показывает на новые сапоги, двое по бокам сидят. Из-за угла
    избы на хвастуна смотрит прищуренный Сглаз."""
    rnd = random.Random(271)
    gor = 700
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 29)
    s += oblaka(t, 170, 4, 31, .4, "#cdd7e4", 13.0)
    # ИЗБА — крупный предмет, с дымком из трубы
    s += SL(Z_DAL, izba_snaruzhi(640, gor - 40, 1040, t, True, True, 7))
    s += SL(Z_DAL, _derevnya_ryad(gor - 110, t, 13, ((1560, 330), (1860, 270))))
    s += SL(Z_DAL, goloe_derevo(1330, gor - 20, 520, t, 17, 9, "#3a3b43", True))
    s += SL(Z_DAL, _zabor_dosok(1180, gor - 180, 740, 190, 11, 56))
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#4e4030"/>'
            + _zemlya_faktura(gor + 40, 1050, 7, 16, "#3f3326")
            + _listya(53, 44, gor + 50, 1060)
            + _inej(59, 40, gor + 60, 1060))
    # ЗАВАЛИНКА
    s += SL(Z_SRED, _zavalinka(170, gor + 160, 1180, t, 180))
    zav_y = gor + 160 - 180 - 26
    # трое мужиков: рост через одного крупный/мелкий, наклон разный
    # сидящий слева — чешет затылок правой рукой
    ax, ay, ah = 380, zav_y + 30, 420
    _figury_kadra((380, zav_y + 30, 420), (1120, zav_y + 34, 390),
                  (740, zav_y + 48, 760))
    sid1 = figura(ax, ay, ah, t, col="#4e4a46", kant="#cfe4f5", shapka=True,
                  ph=.2, naklon=-7.0, profil=False)
    a1, (c1x, c1y), _ = _ruka_mimo(ax, ay, ah, 1, ah * .44, -48, t,
                              "#4e4a46", "#cfe4f5", .2, 8.0)
    a2, (c2x, c2y), _ = _ruka_mimo(ax, ay, ah, -1, ah * .34, 58, t,
                              "#4e4a46", "#cfe4f5", .6, 4.0)
    sid1 += a1 + a2
    s += SL(Z_SRED, sid1)
    # сидящий справа — обеими руками держит шапку на коленях, в профиль
    bx, by_, bh = 1120, zav_y + 34, 390
    sid2 = figura(bx, by_, bh, t, col="#5a5248", kant="#cfe4f5", boroda=True,
                  ph=.7, naklon=9.0, profil=True)
    b1, (e1x, e1y), _ = _ruka_mimo(bx, by_, bh, -1, bh * .40, 62, t,
                              "#5a5248", "#cfe4f5", .7, 4.0)
    b2, (e2x, e2y), _ = _ruka_mimo(bx, by_, bh, -1, bh * .32, 76, t,
                              "#5a5248", "#cfe4f5", .3, 4.0)
    sid2 += b1 + b2
    s += SL(Z_SRED, sid2)
    s += SL(Z_SRED, f'<ellipse cx="{(e1x+e2x)/2-16:.0f}" cy="{(e1y+e2y)/2:.0f}"'
                    f' rx="68" ry="34" fill="#4a3a2c" {o(5)}/>'
            + f'<path d="M{(e1x+e2x)/2-74:.0f},{(e1y+e2y)/2-6:.0f}'
              f' q{58:.0f},{-54:.0f} {116:.0f},{0:.0f} Z" fill="#5a4636" {o(4)}/>')
    # ХВАСТУН встал в середине — вдвое выше сидящих
    hx, hy, hh = 740, zav_y + 48, 760
    bit = 18 * A.w(t, .7, .1)
    hva = figura(hx, hy, hh, t, col="#3f5a6a", kant="#ffd98a", shapka=True,
                 ph=.4, naklon=3.0)
    h1, (g1x, g1y), _ = _ruka_sgib_mimo(hx, hy, hh, 1, hh * .24, 40,
                                        hh * .24, -14 + bit * .4, t,
                                        "#3f5a6a", "#ffd98a", .4, 6.0)
    h2, (g2x, g2y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .46, 60, t,
                              "#3f5a6a", "#ffd98a", .8, 5.0)
    hva += h1 + h2
    s += SL(Z_SRED, hva)
    # новые сапоги, на которые он показывает
    s += SL(Z_SRED, _sapogi_novye(hx + 10, hy + 6, 1.18, t, 1.0))
    s += SL(Z_SRED, para_izo_rta(hx + 64, hy - hh * .80, t, .3, 1.2, .5)
            + para_izo_rta(ax + 50, ay - ah * .80, t, .7, .8, .4))
    # СГЛАЗ выглядывает из-за угла избы
    sg = A.ease(A.seg(t, .6, 1.2))
    s += SL(Z_SRED, _sglaz(1380 - 120 * sg, gor - 250, t, 1.15, .2, .92))
    s += SL(Z_SRED, ten(hx, hy + 8, 160, 24, .45))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    s += SL(Z_SRED, ""
            + ""
            + _varezhka(e1x, e1y, bh, t, .7, "#dcd0bc")
            + ""
            + _varezhka(g1x, g1y, hh, t, .4, "#dcd0bc")
            + _varezhka(g2x, g2y, hh, t, .8, "#dcd0bc"))
    # низ кадра: поленница, кадушка, кот, корзина, следы
    s += SL(Z_SRED, _polenica(1480, gor + 150, 400, 200, 7, 60)
            + _dvorovaya_utvar(96, gor + 330, 300, t, 107, ["kadka", "vedro"])
            + _kucha_listev(1320, 1050, 320, 109, 94)
            + _kot_zhivoy(560, gor + 340, t, 1.0, "#3b342f", .2)
            + _sledy(300, 1060, 740, 900, 6, 113, "#33281d", 1.2))
    # НИЗ КАДРА ОБЖИТ: корзина с репой, кадка, ведро, сани-волокуши,
    # охапка хвороста и грабли у завалинки (осмотр: низ пустовал)
    s += SL(Z_SRED, _kadushki_i_grabli(700, gor + 420, t, 151)
            + _dvorovaya_utvar(1060, gor + 400, 420, t, 157,
                               ["korzina", "meshok", "korob"])
            + _yaschiki(380, gor + 420, t, 163, 2, .92)
            + _luzha(1180, 1030, 170, t, .3))
    s += SL(Z_PERED, _vetka_pered(1980, 130, 780, 158, t, 11, "#241c16", 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 5, .5, .85))
    s += ramka_pp("levo")
    s += vinetka(.42)
    return s


def udacha_otvorachivaetsya(t):
    """Двор в три сцены по словам: та же хвастунья распахивает амбар с
    мешками, показывает силу, выставляет вперёд мужа и детей. Над каждой
    сценой проплывает Сглаз, а Удача с рогом изобилия уходит за ворота."""
    rnd = random.Random(277)
    gor = 640
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 37)
    s += oblaka(t, 150, 5, 41, .4, "#cdd7e4", 15.0)
    s += SL(Z_DAL, izba_snaruzhi(1700, gor - 30, 420, t, True, True, 19))
    s += SL(Z_DAL, goloe_derevo(120, gor, 560, t, 23, 9, "#3a3b43", True))
    s += SL(Z_DAL, _zabor_dosok(-20, gor - 150, 560, 160, 13, 54))
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#52412f"/>'
            + _zemlya_faktura(gor + 50, 1050, 11, 16, "#43362a")
            + _koleya(gor + 300, 127, 2)
            + _listya(61, 40, gor + 60, 1060)
            + _inej(67, 36, gor + 70, 1060))
    # АМБАР С МЕШКАМИ — крупный предмет, створки распахиваются
    rsk = A.ease(A.seg(t, .3, 1.1))
    s += SL(Z_SRED, _ambar_s_meshkami(40, gor - 430, 1020, 470, t, rsk, 5))
    # ПЕРВАЯ СЦЕНА: распахивает амбар обеими руками
    f1x, f1y, f1h = 430, gor + 340, 700
    _figury_kadra((430, gor + 340, 700), (960, gor + 210, 420),
                  (1430, gor + 400, 680), (1700, gor + 350, 580),
                  (1210, gor + 356, 290), (1596, gor + 362, 230))
    hv1 = figura(f1x, f1y, f1h, t, col="#8a3a42", kant="#ffd98a", platok=True,
                 ph=.2, naklon=-4.0)
    a1, (i1x, i1y), _ = _ruka_mimo(f1x, f1y, f1h, 1, f1h * .44, 10 - 26 * rsk, t,
                              "#8a3a42", "#ffd98a", .2, 5.0)
    a2, (i2x, i2y), _ = _ruka_mimo(f1x, f1y, f1h, -1, f1h * .44, 12 - 24 * rsk, t,
                              "#8a3a42", "#ffd98a", .6, 5.0)
    hv1 += a1 + a2
    s += SL(Z_SRED, hv1)
    # ВТОРАЯ СЦЕНА: сгибает правую руку, левая на поясе
    f2x, f2y, f2h = 960, gor + 210, 420
    sil = .5 + .5 * abs(A.w(t, 1.1, .2))
    hv2 = figura(f2x, f2y, f2h, t, col="#8a3a42", kant="#ffd98a", platok=True,
                 ph=.5, naklon=3.0)
    b1, (j1x, j1y), _ = _ruka_sgib_mimo(f2x, f2y, f2h, 1, f2h * .26, 6,
                                        f2h * .28, -52 + 10 * sil, t,
                                        "#8a3a42", "#ffd98a", .5, 5.0)
    b2, (j2x, j2y), _ = _ruka_sgib_mimo(f2x, f2y, f2h, -1, f2h * .20, 36,
                                        f2h * .22, 4, t, "#8a3a42",
                                        "#ffd98a", .9, 3.0)
    hv2 += b1 + b2
    s += SL(Z_SRED, hv2)
    # ТРЕТЬЯ СЦЕНА: обнимает мужа и детей, выставляя их вперёд.
    # Рост через одного: муж крупный, дети мелкие, один ребёнок со спины
    f3x, f3y, f3h = 1430, gor + 400, 680
    hv3 = figura(f3x, f3y, f3h, t, col="#8a3a42", kant="#ffd98a", platok=True,
                 ph=.8, naklon=-3.0)
    # ОБЪЯТИЕ БЕЗ НАРУЖНЫХ РУК: муж и дети стоят ВПЕРЕДИ и перекрывают её,
    # свои рукава фигуры видны по сторонам. Наружная рука здесь шла сквозь
    # голову Удачи — осмотр порции 2.
    s += SL(Z_SRED, hv3)
    # муж крупный, дети мелкие и РАЗНЫЕ: 580 / 290 / 230 — через одного,
    # один со спины, двое в профиль, наклон ±11°
    s += SL(Z_SRED, figura(1700, gor + 350, 580, t, col="#46506a",
                           kant="#cfe4f5", shapka=True, ph=.3, naklon=4.0,
                           profil=True))
    s += SL(Z_SRED, figura(1210, gor + 356, 290, t, col="#5a6a52",
                           kant="#cfe4f5", ph=.6, naklon=-11.0, lico=False))
    s += SL(Z_SRED, figura(1596, gor + 362, 230, t, col="#6a5a46",
                           kant="#cfe4f5", ph=.9, naklon=11.0, profil=True))
    s += SL(Z_SRED, para_izo_rta(f2x + 70, f2y - f2h * .80, t, .3, 1.1, .45)
            + para_izo_rta(f3x + 66, f3y - f3h * .80, t, .8, 1.0, .4))
    # СГЛАЗ над каждой сценой
    for i, sx in enumerate((430, 920, 1410)):
        pl = ((t * .22 + i * .33) % 1.0)
        s += SL(Z_SRED, _sglaz(sx + 160 * pl - 80, gor - 290 - 30 * math.sin(pl * 6.28),
                               t, .88, i * .3, .88))
    # УДАЧА поворачивается спиной и уходит за ворота
    # Удача уходит ПЕРЕДНИМ планом, ниже и крупнее: её рука больше не
    # проходит сквозь голову хвастуньи
    ux = 1060 + 420 * A.ease(A.seg(t, 2.6, 3.4))
    uh = 680
    spin = A.ease(A.seg(t, 2.2, .8))
    uda = figura(ux, gor + 470, uh, t, col="#c9a05a", kant="#ffd98a",
                 platok=True, ph=.1, naklon=2.0, lico=(spin < .5))
    s += SL(Z_SRED, uda)
    # рог изобилия прижат к груди СБОКУ, своими рукавами фигуры: наружная
    # рука отсюда шла сквозь голову ребёнка (осмотр порции 2)
    s += SL(Z_SRED, _rog_izobiliya(ux - uh * .34, gor + 470 - uh * .46,
                                   t, 1.0, .2))
    # ВОРОТА, за которые она уходит
    s += SL(Z_SRED, _vorota_dvora(1620, gor + 300, 360, 440, t,
                                  A.ease(A.seg(t, 2.4, 1.6))))
    # варежки на концах рукавов: предмет уже нарисован, хват ложится поверх
    # ВАРЕЖКИ СНЯТЫ: здесь руки ничего не держат (распахнутый амбар, показ
    # силы, объятие) — варежка без предмета читается светлым пятном и обещает
    # хват, которого нет (решение по осмотру порции 2).
    # низ кадра
    s += SL(Z_SRED, _kadushki_i_grabli(300, gor + 400, t, 11)
            + _polenica(840, gor + 250, 300, 180, 13, 58)
            + _kot_zhivoy(1080, gor + 420, t, 1.05, "#3b342f", .4)
            + _sledy(1880, 1060, 1300, 880, 7, 131, "#33281d", 1.2)
            + _kucha_listev(620, 1056, 300, 137, 90))
    s += SL(Z_PERED, _stolb_pered(-10, 110, "#1a120c", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 5, .5, .9))
    s += vinetka(.42)
    return s


# ── ПОМОЩНИКИ ТРЕТЬЕЙ ПАРТИИ ───────────────────────────────────────────────

def _zmeyka_zavisti(x0, y0, x1, y1, t, ph=.0, s_=1.0):
    """Змейка зависти: зелёное тело волной, светлое брюшко, голова с глазом
    и раздвоенный язычок. Ползёт от окна к чужому дому."""
    k = ((t * .34 + ph) % 1.0)
    cx = x0 + (x1 - x0) * k
    cy = y0 + (y1 - y0) * k
    ug = math.degrees(math.atan2(y1 - y0, x1 - x0))
    s = (f'<g transform="rotate({ug:.1f} {cx:.0f} {cy:.0f})">'
         f'<path d="M{cx-140*s_:.0f},{cy:.0f}'
         f' q{35*s_:.0f},{-30*s_ + 12 * A.w(t, .9, ph):.0f} {70*s_:.0f},0'
         f' q{35*s_:.0f},{30*s_:.0f} {70*s_:.0f},0'
         f' q{35*s_:.0f},{-26*s_:.0f} {60*s_:.0f},{-6*s_:.0f}"'
         f' fill="none" stroke="#4e7a3c" stroke-width="{19*s_:.0f}"'
         f' stroke-linecap="round"/>'
         f'<path d="M{cx-140*s_:.0f},{cy+6*s_:.0f}'
         f' q{35*s_:.0f},{-30*s_:.0f} {70*s_:.0f},0'
         f' q{35*s_:.0f},{30*s_:.0f} {70*s_:.0f},0" fill="none"'
         f' stroke="#8fae5c" stroke-width="{7*s_:.0f}" opacity=".8"/>'
         f'<ellipse cx="{cx+66*s_:.0f}" cy="{cy-8*s_:.0f}" rx="{26*s_:.0f}"'
         f' ry="{17*s_:.0f}" fill="#4e7a3c" {o(4)}/>'
         f'<circle cx="{cx+74*s_:.0f}" cy="{cy-14*s_:.0f}" r="{6*s_:.0f}"'
         f' fill="#f4e06a"/>'
         f'<circle cx="{cx+76*s_:.0f}" cy="{cy-14*s_:.0f}" r="{2.6*s_:.0f}"'
         f' fill="{K}"/>'
         f'<path d="M{cx+90*s_:.0f},{cy-4*s_:.0f} l{20*s_:.0f},{-6*s_:.0f}'
         f' m{-20*s_:.0f},{6*s_:.0f} l{20*s_:.0f},{6*s_:.0f}" fill="none"'
         f' stroke="#b8352c" stroke-width="{5*s_:.0f}"/></g>')
    return s


def _korova(x, y, s_=1.0, t=0.0, otvorot=.0):
    """Корова в профиль: тулово с пятнами, рога, вымя, хвост с кистью.
    otvorot 0..1 — отворачивает голову от ведра."""
    gol = -26 * otvorot
    hv = 12 * A.w(t, 2.2, .1)
    s = (f'{ten(x, y + 8 * s_, 150 * s_, 24 * s_, .45)}'
         f'<ellipse cx="{x:.0f}" cy="{y-150*s_:.0f}" rx="{168*s_:.0f}"'
         f' ry="{104*s_:.0f}" fill="#e8e2d6" {o(7)}/>')
    for i, (dx, dy, rr) in enumerate(((-70, -30, 46), (40, -60, 38), (90, 10, 30))):
        s += (f'<ellipse cx="{x+dx*s_:.0f}" cy="{y-150*s_+dy*s_:.0f}"'
              f' rx="{rr*s_:.0f}" ry="{rr*.74*s_:.0f}" fill="#4a3e34"'
              f' opacity=".9"/>')
    for dx in (-120, -70, 70, 120):
        s += (f'<rect x="{x+dx*s_-17*s_:.0f}" y="{y-66*s_:.0f}" width="{34*s_:.0f}"'
              f' height="{66*s_:.0f}" rx="{10*s_:.0f}" fill="#e0d8ca" {o(5)}/>'
              f'<rect x="{x+dx*s_-19*s_:.0f}" y="{y-16*s_:.0f}" width="{38*s_:.0f}"'
              f' height="{18*s_:.0f}" rx="6" fill="#3a332c" {o(3)}/>')
    s += (f'<ellipse cx="{x+20*s_:.0f}" cy="{y-58*s_:.0f}" rx="{44*s_:.0f}"'
          f' ry="{32*s_:.0f}" fill="#f0c8c0" {o(4)}/>')
    s += (f'<g transform="rotate({gol:.1f} {x+160*s_:.0f} {y-200*s_:.0f})">'
          f'<ellipse cx="{x+216*s_:.0f}" cy="{y-176*s_:.0f}" rx="{74*s_:.0f}"'
          f' ry="{58*s_:.0f}" fill="#e8e2d6" {o(6)}/>'
          f'<ellipse cx="{x+268*s_:.0f}" cy="{y-150*s_:.0f}" rx="{40*s_:.0f}"'
          f' ry="{30*s_:.0f}" fill="#d8b0a8" {o(5)}/>'
          f'<circle cx="{x+278*s_:.0f}" cy="{y-156*s_:.0f}" r="{7*s_:.0f}"'
          f' fill="#5a4a42"/>'
          f'<circle cx="{x+252*s_:.0f}" cy="{y-144*s_:.0f}" r="{7*s_:.0f}"'
          f' fill="#5a4a42"/>'
          f'<ellipse cx="{x+232*s_:.0f}" cy="{y-204*s_:.0f}" rx="{12*s_:.0f}"'
          f' ry="{15*s_:.0f}" fill="{K}"/>'
          f'<path d="M{x+192*s_:.0f},{y-218*s_:.0f} q{-30*s_:.0f},{-34*s_:.0f}'
          f' {-8*s_:.0f},{-56*s_:.0f}" fill="none" stroke="#cdbf9c"'
          f' stroke-width="{15*s_:.0f}" stroke-linecap="round"/>'
          f'<path d="M{x+252*s_:.0f},{y-220*s_:.0f} q{28*s_:.0f},{-32*s_:.0f}'
          f' {8*s_:.0f},{-54*s_:.0f}" fill="none" stroke="#cdbf9c"'
          f' stroke-width="{15*s_:.0f}" stroke-linecap="round"/>'
          f'<path d="M{x+170*s_:.0f},{y-190*s_:.0f} q{-40*s_:.0f},{4*s_:.0f}'
          f' {-50*s_:.0f},{30*s_:.0f}" fill="none" stroke="#e0d8ca"'
          f' stroke-width="{22*s_:.0f}"/></g>')
    s += (f'<g transform="rotate({hv:.1f} {x-166*s_:.0f} {y-200*s_:.0f})">'
          f'<line x1="{x-166*s_:.0f}" y1="{y-200*s_:.0f}" x2="{x-186*s_:.0f}"'
          f' y2="{y-50*s_:.0f}" stroke="#d8d0c2" stroke-width="{11*s_:.0f}"/>'
          f'<ellipse cx="{x-188*s_:.0f}" cy="{y-34*s_:.0f}" rx="{13*s_:.0f}"'
          f' ry="{24*s_:.0f}" fill="#4a3e34" {o(3)}/></g>')
    return s


def _cvetok_v_gorshke(x, y, t, s_=1.0, vyanet=.0):
    """Цветок в глиняном горшке: поддон, земля, три листа и бутон. vyanet
    0..1 — листья опускаются и бледнеют, лепестки осыпаются."""
    s = (f'{ten(x, y + 6 * s_, 54 * s_, 11 * s_, .4)}'
         f'<path d="M{x-50*s_:.0f},{y-96*s_:.0f} L{x+50*s_:.0f},{y-96*s_:.0f}'
         f' L{x+38*s_:.0f},{y:.0f} L{x-38*s_:.0f},{y:.0f} Z"'
         f' fill="url(#glina)" {o(5)}/>'
         f'<rect x="{x-56*s_:.0f}" y="{y-110*s_:.0f}" width="{112*s_:.0f}"'
         f' height="{20*s_:.0f}" rx="7" fill="#9c6a44" {o(4)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-100*s_:.0f}" rx="{44*s_:.0f}"'
         f' ry="{11*s_:.0f}" fill="#4a3a28"/>')
    for i, a0 in enumerate((-150, -90, -30)):
        a = math.radians(a0 + 54 * vyanet + 5 * A.w(t, 3.0, i * .3))
        dl = 110 * s_
        ex = x + dl * math.cos(a)
        ey = y - 100 * s_ + dl * math.sin(a)
        col = "#6f8c4a" if vyanet < .5 else "#8a8a54"
        s += (f'<path d="M{x:.0f},{y-100*s_:.0f}'
              f' Q{(x+ex)/2+20*s_:.0f},{(y-100*s_+ey)/2-30*s_:.0f} {ex:.0f},{ey:.0f}'
              f' Q{(x+ex)/2-14*s_:.0f},{(y-100*s_+ey)/2+24*s_:.0f} {x:.0f},{y-100*s_:.0f} Z"'
              f' fill="{col}" {o(4)}/>')
    s += (f'<line x1="{x:.0f}" y1="{y-100*s_:.0f}" x2="{x+8*s_:.0f}"'
          f' y2="{y-200*s_+30*s_*vyanet:.0f}" stroke="#6f8c4a"'
          f' stroke-width="{8*s_:.0f}"/>')
    for i in range(5):
        a = math.radians(i * 72)
        pd = 1 - vyanet
        s += (f'<ellipse cx="{x+8*s_+22*s_*math.cos(a)*pd:.0f}"'
              f' cy="{y-200*s_+30*s_*vyanet+20*s_*math.sin(a)*pd:.0f}"'
              f' rx="{17*s_:.0f}" ry="{12*s_:.0f}" fill="#d6452a"'
              f' opacity="{.4+.6*pd:.2f}" {o(3)}/>')
    return s


def _sumka_hozyaystvennaya(x, y, t, s_=1.0, zast=.0):
    """Хозяйственная сумка: кожаные боковины, две дуги ручек, застёжка
    на замке и выпирающий бок. zast 0..1 — застёгивается."""
    return (f'{ten(x, y + 6 * s_, 86 * s_, 13 * s_, .45)}'
            f'<path d="M{x-96*s_:.0f},{y-130*s_:.0f} L{x+96*s_:.0f},{y-130*s_:.0f}'
            f' L{x+84*s_:.0f},{y:.0f} L{x-84*s_:.0f},{y:.0f} Z"'
            f' fill="#6a4a32" {o(6)}/>'
            f'<path d="M{x-96*s_:.0f},{y-130*s_:.0f} q{96*s_:.0f},{-34*s_*(1-zast):.0f}'
            f' {192*s_:.0f},0 l0,{18*s_:.0f} q{-96*s_:.0f},{-14*s_*(1-zast):.0f}'
            f' {-192*s_:.0f},0 Z" fill="#7d5a3c" {o(4)}/>'
            f'<path d="M{x-54*s_:.0f},{y-132*s_:.0f} q{18*s_:.0f},{-72*s_:.0f}'
            f' {52*s_:.0f},{-70*s_:.0f}" fill="none" stroke="#5a3a28"'
            f' stroke-width="{13*s_:.0f}"/>'
            f'<path d="M{x+54*s_:.0f},{y-132*s_:.0f} q{-18*s_:.0f},{-72*s_:.0f}'
            f' {-52*s_:.0f},{-70*s_:.0f}" fill="none" stroke="#5a3a28"'
            f' stroke-width="{13*s_:.0f}"/>'
            f'<rect x="{x-24*s_:.0f}" y="{y-128*s_:.0f}" width="{48*s_:.0f}"'
            f' height="{30*s_:.0f}" rx="8" fill="url(#zhel)" {o(4)}/>'
            f'<rect x="{x-34*s_:.0f}" y="{y-80*s_:.0f}" width="{68*s_:.0f}"'
            f' height="{14*s_:.0f}" rx="6" fill="#4a3222" opacity=".8"/>')


def _skameyka_podezda(x, y, w_, t, h_=150):
    """Скамейка у подъезда: две бетонные тумбы, три крашеные доски сиденья,
    облупившаяся краска и доска спинки."""
    s = (f'{ten(x + w_ / 2, y + 8, w_ * .44, 18, .45)}')
    for i in (0, 1):
        bx = x + 40 + i * (w_ - 150)
        s += (f'<rect x="{bx:.0f}" y="{y-h_:.0f}" width="110" height="{h_:.0f}"'
              f' rx="8" fill="{BETON}" {o(6)}/>'
              f'<rect x="{bx+12:.0f}" y="{y-h_+16:.0f}" width="86" height="{h_-40:.0f}"'
              f' rx="6" fill="{BETON2}" opacity=".7"/>')
    for i in range(3):
        s += (f'<rect x="{x:.0f}" y="{y-h_-28+i*2:.0f}" width="{w_:.0f}" height="26"'
              f' rx="8" fill="#4e7a52" {o(5)}/>'
              f'<rect x="{x+60+i*180:.0f}" y="{y-h_-26+i*2:.0f}" width="120"'
              f' height="12" rx="5" fill="#6b9a6e" opacity=".8"/>')
        y -= 0
    s += (f'<rect x="{x+20:.0f}" y="{y-h_-190:.0f}" width="{w_-40:.0f}" height="28"'
          f' rx="9" fill="#4e7a52" {o(5)}/>')
    for i in (0, 1):
        s += (f'<rect x="{x+60+i*(w_-180):.0f}" y="{y-h_-190:.0f}" width="26"'
              f' height="166" rx="8" fill="{BETON2}" {o(4)}/>')
    return s


def _golub(x, y, t, s_=1.0, ph=.0, hodit=True):
    """Голубь у скамейки: сизое тело, зелёная шейка, красные лапки, клюёт и
    переступает. Живая мелочь нижней трети."""
    sh = 16 * s_ * A.w(t, 1.9, ph) if hodit else 0
    kl = 14 * s_ * max(.0, A.w(t, 1.3, ph))
    return (f'<g transform="translate({sh:.1f},0)">'
            f'{ten(x, y + 4 * s_, 34 * s_, 8 * s_, .4)}'
            f'<ellipse cx="{x:.0f}" cy="{y-34*s_:.0f}" rx="{44*s_:.0f}"'
            f' ry="{28*s_:.0f}" fill="#8694a4" {o(4)}/>'
            f'<path d="M{x-40*s_:.0f},{y-40*s_:.0f} q{30*s_:.0f},{-18*s_:.0f}'
            f' {62*s_:.0f},{2*s_:.0f} q{-26*s_:.0f},{22*s_:.0f} {-62*s_:.0f},{-2*s_:.0f} Z"'
            f' fill="#6e7c8c" {o(3)}/>'
            f'<path d="M{x-44*s_:.0f},{y-30*s_:.0f} l{-28*s_:.0f},{8*s_:.0f}'
            f' l{26*s_:.0f},{10*s_:.0f} Z" fill="#7a8898" {o(3)}/>'
            f'<circle cx="{x+36*s_:.0f}" cy="{y-56*s_+kl:.0f}" r="{17*s_:.0f}"'
            f' fill="#9aa8b8" {o(3)}/>'
            f'<ellipse cx="{x+32*s_:.0f}" cy="{y-46*s_+kl:.0f}" rx="{13*s_:.0f}"'
            f' ry="{9*s_:.0f}" fill="#5c8a72" opacity=".9"/>'
            f'<path d="M{x+50*s_:.0f},{y-54*s_+kl:.0f} l{16*s_:.0f},{4*s_:.0f}'
            f' l{-16*s_:.0f},{5*s_:.0f} Z" fill="#3a3a42" {o(2)}/>'
            f'<circle cx="{x+42*s_:.0f}" cy="{y-60*s_+kl:.0f}" r="{3.4*s_:.0f}"'
            f' fill="{K}"/>'
            f'<line x1="{x-6*s_:.0f}" y1="{y-10*s_:.0f}" x2="{x-10*s_:.0f}"'
            f' y2="{y:.0f}" stroke="#b8503c" stroke-width="{5*s_:.0f}"/>'
            f'<line x1="{x+14*s_:.0f}" y1="{y-10*s_:.0f}" x2="{x+20*s_:.0f}"'
            f' y2="{y:.0f}" stroke="#b8503c" stroke-width="{5*s_:.0f}"/></g>')


def _komochek_radosti(x, y, t, s_=1.0, ph=.0):
    """Комочек-радость: тёплый светящийся шарик с улыбкой, щёчками и
    лучиками. Светится в сложенных лодочкой ладонях."""
    puls = 1.0 + .07 * A.w(t, 1.1, ph)
    s = (f'<g transform="translate({x:.0f} {y:.0f}) scale({puls:.3f})'
         f' translate({-x:.0f} {-y:.0f})">')
    for i in range(8):
        a = math.radians(i * 45 + 14 * A.w(t, 2.4, ph))
        s += (f'<line x1="{x+56*s_*math.cos(a):.0f}" y1="{y+56*s_*math.sin(a):.0f}"'
              f' x2="{x+(84+10*math.sin(t*2+i))*s_*math.cos(a):.0f}"'
              f' y2="{y+(84+10*math.sin(t*2+i))*s_*math.sin(a):.0f}"'
              f' stroke="#ffd98a" stroke-width="{7*s_:.0f}" opacity=".8"'
              f' stroke-linecap="round"/>')
    s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{48*s_:.0f}" fill="#ffd98a"'
          f' {o(4)}/>'
          f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{34*s_:.0f}" fill="#fff0c4"'
          f' opacity=".9"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*17*s_-7*s_:.0f},{y-8*s_:.0f}'
              f' q{7*s_:.0f},{-9*s_:.0f} {14*s_:.0f},0" fill="none" stroke="#8a5a22"'
              f' stroke-width="{5*s_:.0f}" stroke-linecap="round"/>'
              f'<circle cx="{x+i*26*s_:.0f}" cy="{y+9*s_:.0f}" r="{8*s_:.0f}"'
              f' fill="#e08a74" opacity=".55"/>')
    s += (f'<path d="M{x-14*s_:.0f},{y+10*s_:.0f} q{14*s_:.0f},{14*s_:.0f}'
          f' {28*s_:.0f},0" fill="none" stroke="#8a5a22" stroke-width="{6*s_:.0f}"'
          f' stroke-linecap="round"/>'
          f'{teplo(x, y, 210 * s_, 190 * s_, .5)}</g>')
    return s


def _samovar(x, y, t, s_=1.0):
    """Самовар: пузатое тулово на поддоне, труба с коленом, краник с
    вентилем, две ручки и блик дугой. Пускает пар."""
    return (f'{ten(x, y + 8 * s_, 86 * s_, 15 * s_, .5)}'
            f'<path d="M{x-74*s_:.0f},{y-34*s_:.0f} L{x+74*s_:.0f},{y-34*s_:.0f}'
            f' L{x+54*s_:.0f},{y:.0f} L{x-54*s_:.0f},{y:.0f} Z"'
            f' fill="url(#med)" {o(5)}/>'
            f'<path d="M{x-88*s_:.0f},{y-150*s_:.0f}'
            f' q{-16*s_:.0f},{-80*s_:.0f} {30*s_:.0f},{-104*s_:.0f}'
            f' q{58*s_:.0f},{-18*s_:.0f} {116*s_:.0f},0'
            f' q{46*s_:.0f},{24*s_:.0f} {30*s_:.0f},{104*s_:.0f}'
            f' q{-10*s_:.0f},{36*s_:.0f} {-88*s_:.0f},{34*s_:.0f}'
            f' q{-78*s_:.0f},{2*s_:.0f} {-88*s_:.0f},{-34*s_:.0f} Z"'
            f' fill="url(#zol)" {o(7)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y-254*s_:.0f}" rx="{74*s_:.0f}"'
            f' ry="{20*s_:.0f}" fill="#b5803a" {o(5)}/>'
            f'<rect x="{x-26*s_:.0f}" y="{y-330*s_:.0f}" width="{52*s_:.0f}"'
            f' height="{80*s_:.0f}" rx="8" fill="{ZHELEZ}" {o(5)}/>'
            f'<path d="M{x-26*s_:.0f},{y-330*s_:.0f} l{-40*s_:.0f},{-30*s_:.0f}'
            f' l{18*s_:.0f},{-26*s_:.0f} l{48*s_:.0f},{32*s_:.0f} Z"'
            f' fill="{ZHELEZ}" {o(4)}/>'
            f'<path d="M{x-96*s_:.0f},{y-190*s_:.0f} q{-44*s_:.0f},{20*s_:.0f}'
            f' {-6*s_:.0f},{54*s_:.0f}" fill="none" stroke="#8a5a22"'
            f' stroke-width="{15*s_:.0f}"/>'
            f'<path d="M{x+96*s_:.0f},{y-190*s_:.0f} q{44*s_:.0f},{20*s_:.0f}'
            f' {6*s_:.0f},{54*s_:.0f}" fill="none" stroke="#8a5a22"'
            f' stroke-width="{15*s_:.0f}"/>'
            f'<path d="M{x+56*s_:.0f},{y-112*s_:.0f} l{44*s_:.0f},{10*s_:.0f}'
            f' l{-6*s_:.0f},{26*s_:.0f} l{-42*s_:.0f},{-10*s_:.0f} Z"'
            f' fill="#b5803a" {o(4)}/>'
            f'<circle cx="{x+104*s_:.0f}" cy="{y-120*s_:.0f}" r="{14*s_:.0f}"'
            f' fill="url(#zhel)" {o(3)}/>'
            f'<path d="M{x-54*s_:.0f},{y-220*s_:.0f} q{20*s_:.0f},{-44*s_:.0f}'
            f' {10*s_:.0f},{-66*s_:.0f}" fill="none" stroke="#fff0c8"'
            f' stroke-width="{11*s_:.0f}" opacity="{.35+.3*abs(A.w(t,2.4)):.2f}"/>')


def _baranki(x, y, t, n=5, s_=1.0, svyazka=True):
    """Связка баранок: кольца с маковой обсыпкой на бечёвке, пара лежит
    рядом на столе. Качается, если висит."""
    rnd = random.Random(int(x) + n)
    kach = 2.6 * A.w(t, 2.8, .2)
    s = f'<g transform="rotate({kach:.1f} {x:.0f} {y:.0f})">'
    if svyazka:
        s += (f'<path d="M{x-120*s_:.0f},{y:.0f} q{120*s_:.0f},{54*s_:.0f}'
              f' {240*s_:.0f},0" fill="none" stroke="#cbbb98"'
              f' stroke-width="{6*s_:.0f}"/>')
    for i in range(n):
        p = i / max(1, n - 1.0)
        bx = x - 120 * s_ + 240 * s_ * p
        by = y + 54 * s_ * (1 - (2 * p - 1) ** 2) * .9
        rr = (30 + rnd.uniform(0, 7)) * s_
        s += (f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{rr:.0f}" fill="url(#med)"'
              f' {o(4)}/>'
              f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{rr*.36:.0f}" fill="none"'
              f' stroke="{K}" stroke-width="4"/>')
        for k in range(4):
            a = math.radians(k * 90 + 20)
            s += (f'<circle cx="{bx+rr*.66*math.cos(a):.0f}"'
                  f' cy="{by+rr*.66*math.sin(a):.0f}" r="{2.6*s_:.0f}"'
                  f' fill="#4a3522"/>')
    return s + "</g>"


def _kulak(x, y, s_=1.0, t=0.0, ph=.0, col="#e8d8c0"):
    """КУЛАК КОСТЯШКАМИ ВНИЗ: овал кисти, три бугра костяшек, тёмная тень
    под ними и светлый блик сверху. Ставится там, где рука стучит по столу
    и держать ей нечего — варежка-перекрытие тут неуместна."""
    s_ = max(.5, s_)
    return (f'{ten(x, y + 26 * s_, 40 * s_, 10 * s_, .45)}'
            f'<path d="M{x-40*s_:.0f},{y:.0f} q{-6*s_:.0f},{-34*s_:.0f}'
            f' {26*s_:.0f},{-38*s_:.0f} q{34*s_:.0f},{-6*s_:.0f}'
            f' {56*s_:.0f},{10*s_:.0f} q{14*s_:.0f},{28*s_:.0f}'
            f' {-6*s_:.0f},{44*s_:.0f} q{-38*s_:.0f},{14*s_:.0f}'
            f' {-76*s_:.0f},{-16*s_:.0f} Z" fill="{col}" {o(5)}/>'
            + "".join(
                f'<path d="M{x-26*s_+i*26*s_:.0f},{y+16*s_:.0f}'
                f' q{10*s_:.0f},{-14*s_:.0f} {22*s_:.0f},{-2*s_:.0f}"'
                f' fill="none" stroke="#c9a884" stroke-width="{max(2, 5 * s_):.0f}"/>'
                for i in range(3))
            + f'<path d="M{x-28*s_:.0f},{y-24*s_:.0f} q{26*s_:.0f},{-14*s_:.0f}'
              f' {54*s_:.0f},{-2*s_:.0f}" fill="none" stroke="#fff4e2"'
              f' stroke-width="{max(2, 5 * s_):.0f}" opacity=".6"/>')


def _krugi_po_stolu(cx, cy, t, n=3, ph=.0, rmax=260):
    """Круги, расходящиеся по столешнице от стука: три кольца догоняют друг
    друга, у каждого свой возраст и толщина."""
    s = ""
    for i in range(n):
        k = ((t * .9 + ph + i * .33) % 1.0)
        rr = rmax * k
        s += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rr:.0f}"'
              f' ry="{rr*.32:.0f}" fill="none" stroke="#f6ead0"'
              f' stroke-width="{max(5, 14 - 8 * k):.0f}"'
              f' opacity="{.85*(1-k):.2f}"/>')
    return s


def _ploshka_s_meloch(x, y, t, s_=1.0, n=7, seed=5):
    """Глиняная плошка с безделушками: монетки, бусины, ленточка, глиняная
    свистулька и тряпичная куколка. Позвякивает, когда её несут."""
    rnd = random.Random(seed)
    dr = 2.4 * A.w(t, 1.4, .2)
    s = (f'<g transform="translate({dr:.1f},0)">'
         f'{ten(x, y + 8 * s_, 76 * s_, 13 * s_, .4)}'
         f'<path d="M{x-88*s_:.0f},{y-56*s_:.0f} q{16*s_:.0f},{62*s_:.0f}'
         f' {88*s_:.0f},{58*s_:.0f} q{72*s_:.0f},{4*s_:.0f} {88*s_:.0f},{-58*s_:.0f} Z"'
         f' fill="url(#glina)" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-56*s_:.0f}" rx="{88*s_:.0f}"'
         f' ry="{20*s_:.0f}" fill="#8a5a30" {o(4)}/>')
    for i in range(n):
        mx = x + rnd.uniform(-62, 62) * s_
        my = y - 58 * s_ + rnd.uniform(-10, 6) * s_
        vid = i % 4
        if vid == 0:
            s += (f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{17*s_:.0f}"'
                  f' ry="{9*s_:.0f}" fill="url(#med)" {o(3)}/>'
                  f'<ellipse cx="{mx-4*s_:.0f}" cy="{my-2*s_:.0f}" rx="{6*s_:.0f}"'
                  f' ry="{3*s_:.0f}" fill="#fff0c4"'
                  f' opacity="{.4+.4*abs(A.w(t,2.2,i*.2)):.2f}"/>')
        elif vid == 1:
            s += (f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="{11*s_:.0f}"'
                  f' fill="{["#3f5c7a", "#8a4a52", "#4a6a48"][i % 3]}" {o(3)}/>'
                  f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="{3.4*s_:.0f}"'
                  f' fill="{K}"/>')
        elif vid == 2:
            s += (f'<path d="M{mx-24*s_:.0f},{my:.0f} q{12*s_:.0f},{-14*s_:.0f}'
                  f' {24*s_:.0f},0 q{12*s_:.0f},{14*s_:.0f} {24*s_:.0f},0"'
                  f' fill="none" stroke="{TKAN}" stroke-width="{8*s_:.0f}"/>')
        else:
            s += (f'<path d="M{mx-14*s_:.0f},{my+6*s_:.0f} l{26*s_:.0f},{-8*s_:.0f}'
                  f' l{10*s_:.0f},{14*s_:.0f} l{-30*s_:.0f},{6*s_:.0f} Z"'
                  f' fill="#9c6a44" {o(3)}/>')
    s += (f'<path d="M{x+30*s_:.0f},{y-70*s_:.0f} q{14*s_:.0f},{-26*s_:.0f}'
          f' {34*s_:.0f},{-18*s_:.0f} q{-8*s_:.0f},{22*s_:.0f} {-18*s_:.0f},{28*s_:.0f} Z"'
          f' fill="#cfa0a8" {o(3)}/>'
          f'<circle cx="{x+54*s_:.0f}" cy="{y-96*s_:.0f}" r="{13*s_:.0f}"'
          f' fill="#e8d8c0" {o(3)}/></g>')
    return s



def _polati(x, y, w_, t, seed=3):
    """Полати над входом: настил на брусьях, свесившаяся рука, край одеяла,
    которое «дышит», и детская пятка. Спящие домашние, без лиц."""
    dyh = 5 * A.w(t, 3.4, .2)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="34" rx="8"'
         f' fill="url(#dosk)" {o(6)}/>'
         f'<rect x="{x:.0f}" y="{y-26:.0f}" width="{w_:.0f}" height="30" rx="7"'
         f' fill="#5b4428" {o(5)}/>')
    for i in range(4):
        s += (f'<rect x="{x+30+i*(w_-100)/3:.0f}" y="{y+34:.0f}" width="26"'
              f' height="50" rx="7" fill="#4a3522" {o(4)}/>')
    s += (f'<g transform="translate(0,{dyh:.1f})">'
          f'<path d="M{x+80:.0f},{y-26:.0f} q{w_*.2:.0f},{-56:.0f} {w_*.44:.0f},{-20:.0f}'
          f' q{w_*.18:.0f},{30:.0f} {w_*.30:.0f},{20:.0f} l0,{26:.0f}'
          f' l{-w_*.74:.0f},0 Z" fill="#8a4a52" {o(5)}/>')
    for i in range(5):
        s += (f'<path d="M{x+120+i*90:.0f},{y-30:.0f} q{18:.0f},{-20:.0f}'
              f' {38:.0f},{-6:.0f}" fill="none" stroke="#a35a62"'
              f' stroke-width="7" opacity=".85"/>')
    s += "</g>"
    s += (f'<path d="M{x+w_*.72:.0f},{y+24:.0f} q{26:.0f},{64:.0f} {6:.0f},{104:.0f}"'
          f' fill="none" stroke="#e8d8c0" stroke-width="30" stroke-linecap="round"/>'
          f'<ellipse cx="{x+w_*.76:.0f}" cy="{y+140:.0f}" rx="26" ry="20"'
          f' fill="#e8d8c0" {o(4)}/>'
          f'<ellipse cx="{x+w_*.30:.0f}" cy="{y+40:.0f}" rx="30" ry="22"'
          f' fill="#f0cfae" {o(4)}/>'
          f'<ellipse cx="{x+w_*.38:.0f}" cy="{y+40:.0f}" rx="30" ry="22"'
          f' fill="#f0cfae" {o(4)}/>')
    return s


def _redka(cx, cy, s_=1.0, t=0.0, ug=0.0, kach=.0, cvet="#2e2b2a"):
    """ЧЁРНАЯ РЕДЬКА, КОТОРУЮ ВИДНО СО СТОП-КАДРА (R-0047): тёмное тулово
    каплей с продольными бороздами и светлыми чечевичками, срез кожуры,
    хвостик-корешок с волосками и пучок зелёной ботвы с прожилками.
    kach 0..1 — насколько сильно качается ботва."""
    rnd = random.Random(int(cx) + int(s_ * 100))
    sway = (3.0 + 7.0 * kach) * A.w(t, 2.2, .2)
    r = 86 * s_
    s = (f'<g transform="rotate({ug:.1f} {cx:.0f} {cy:.0f})">'
         f'{ten(cx, cy + r * .92, r * 1.0, r * .22, .5)}'
         f'<path d="M{cx-r:.0f},{cy-r*.34:.0f}'
         f' q{r*.10:.0f},{-r*.76:.0f} {r*1.0:.0f},{-r*.70:.0f}'
         f' q{r*.90:.0f},{r*.02:.0f} {r*1.0:.0f},{r*.70:.0f}'
         f' q{r*.06:.0f},{r*.84:.0f} {-r*1.0:.0f},{r*1.10:.0f}'
         f' q{-r*1.06:.0f},{-r*.26:.0f} {-r*1.0:.0f},{-r*1.10:.0f} Z"'
         f' fill="{cvet}" {o(7)}/>')
    for i in range(5):
        dx = -r * .62 + i * r * .32
        s += (f'<path d="M{cx+dx:.0f},{cy-r*.92:.0f}'
              f' q{r*.10:.0f},{r*.84:.0f} {dx*.14:.0f},{r*1.60:.0f}"'
              f' fill="none" stroke="#4a4644" stroke-width="{max(3, 7 * s_):.0f}"'
              f' opacity=".75"/>')
    for i in range(7):
        lx = cx + rnd.uniform(-r * .72, r * .72)
        ly = cy + rnd.uniform(-r * .70, r * .80)
        s += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{7 * s_:.0f}"'
              f' ry="{3.4 * s_:.0f}" fill="#8f8a84" opacity=".7"/>')
    s += (f'<path d="M{cx-r*.70:.0f},{cy-r*.52:.0f}'
          f' q{r*.40:.0f},{-r*.30:.0f} {r*.84:.0f},{-r*.12:.0f}" fill="none"'
          f' stroke="#cfc9c2" stroke-width="{max(3, 10 * s_):.0f}" opacity=".45"/>'
          f'<path d="M{cx+r*.30:.0f},{cy+r*.96:.0f}'
          f' q{r*.16:.0f},{r*.46:.0f} {-r*.04:.0f},{r*.78:.0f}" fill="none"'
          f' stroke="#cdbf9c" stroke-width="{max(3, 9 * s_):.0f}"'
          f' stroke-linecap="round"/>')
    for i in range(4):
        s += (f'<line x1="{cx+r*(.30+i*.04):.0f}" y1="{cy+r*(1.10+i*.16):.0f}"'
              f' x2="{cx+r*(.44+i*.05):.0f}" y2="{cy+r*(1.22+i*.16):.0f}"'
              f' stroke="#cdbf9c" stroke-width="{max(2, 4 * s_):.0f}"'
              f' opacity=".8"/>')
    # БОТВА: пять резных листьев веером, с прожилкой у каждого
    s += f'<g transform="rotate({sway:.1f} {cx:.0f} {cy - r * .96:.0f})">'
    for i in range(5):
        a = math.radians(-150 + i * 30)
        dl = (140 + (i % 2) * 44) * s_
        ex = cx + dl * math.cos(a)
        ey = cy - r * .96 + dl * math.sin(a)
        s += (f'<path d="M{cx:.0f},{cy-r*.96:.0f}'
              f' Q{(cx+ex)/2+30*s_:.0f},{(cy-r*.96+ey)/2-28*s_:.0f} {ex:.0f},{ey:.0f}'
              f' Q{(cx+ex)/2-24*s_:.0f},{(cy-r*.96+ey)/2+30*s_:.0f}'
              f' {cx:.0f},{cy-r*.96:.0f} Z" fill="{["#4e7a3c", "#5c8a40", "#3f6a34"][i % 3]}"'
              f' {o(4)}/>'
              f'<line x1="{cx:.0f}" y1="{cy-r*.96:.0f}" x2="{ex:.0f}" y2="{ey:.0f}"'
              f' stroke="#8fae5c" stroke-width="{max(2, 5 * s_):.0f}" opacity=".8"/>')
    s += "</g></g>"
    return s


# ── ДЕКОРАЦИИ, ТРЕТЬЯ ПАРТИЯ ───────────────────────────────────────────────

def zavist_v_chuzhih_oknah(t):
    """Деревенская улица, три избы в ряд: в каждом окне по соседу, руки на
    подоконниках, глаза позеленели. От окон к нарядному дому хвастуньи
    ползут зелёные змейки зависти, во дворе вянет цветок."""
    rnd = random.Random(281)
    gor = 690
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 43)
    s += oblaka(t, 160, 5, 47, .42, "#cdd7e4", 14.0)
    # три избы в ряд — средний план, у каждой своё окно с соседом
    mesta = ((190, 400), (620, 380), (1030, 420))
    for i, (bx, bw) in enumerate(mesta):
        s += SL(Z_DAL, izba_snaruzhi(bx, gor - 120 + i * 14, bw, t, True, True,
                                     7 + i * 5))
    s += SL(Z_DAL, goloe_derevo(1500, gor - 40, 520, t, 53, 9, "#3a3b43", True))
    s += SL(Z_DAL, _zabor_dosok(-30, gor - 210, 1300, 190, 17, 56))
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#4e4030"/>'
            + _zemlya_faktura(gor + 40, 1050, 19, 16, "#3f3326")
            + _koleya(gor + 230, 283, 2)
            + _listya(71, 44, gor + 50, 1060)
            + _inej(73, 40, gor + 60, 1060)
            + _pol_shvy(gor + 40, 1070, 79, 5, "#3a2c20"))
    # НАРЯДНЫЙ ДОМ ХВАСТУНЬИ справа — крупный предмет кадра
    s += SL(Z_SRED, izba_snaruzhi(1620, gor + 30, 1000, t, True, True, 23))
    s += SL(Z_SRED, _kryl_co(1450, gor + 60, 320, 120, t, 3, True, True))
    # три соседа в окнах: рост через одного, один в профиль, один со спины
    for i, (bx, bw) in enumerate(mesta):
        ox = bx + bw * .5
        oy = gor - 120 + i * 14 - bw * .30
        s += SL(Z_SRED, f'<rect x="{ox-96:.0f}" y="{oy-110:.0f}" width="192"'
                        f' height="150" rx="8" fill="#1b2029" {o(6)}/>'
                f'<rect x="{ox-110:.0f}" y="{oy+36:.0f}" width="220" height="26"'
                f' rx="8" fill="url(#dosk)" {o(5)}/>')
        fh = (270, 150, 230)[i]
        _figury_kadra((ox, oy + 42 + fh * .52, fh))
        sos = figura(ox, oy + 42 + fh * .52, fh, t,
                     col=("#4a4a56", "#5a5248", "#46506a")[i],
                     kant="#cfe4f5", platok=(i == 1), shapka=(i == 0),
                     boroda=(i == 2), ph=.2 + i * .3,
                     profil=(i == 2), lico=(i != 1), naklon=(-8, 12, -5)[i])
        r1, (s1x, s1y), _ = _ruka_mimo(ox, oy + 42 + fh * .52, fh, 1, fh * .42, 66, t,
                                  ("#4a4a56", "#5a5248", "#46506a")[i],
                                  "#cfe4f5", .2 + i * .2, 3.0)
        r2, (s2x, s2y), _ = _ruka_mimo(ox, oy + 42 + fh * .52, fh, -1, fh * .42, 70, t,
                                  ("#4a4a56", "#5a5248", "#46506a")[i],
                                  "#cfe4f5", .6 + i * .2, 3.0)
        sos += r1 + r2
        s += SL(Z_SRED, sos)
        s += SL(Z_SRED, ""
               )
        # позеленевшие глаза: зелёный отсвет поверх лица
        zel = .4 + .5 * abs(A.w(t, 1.6, i * .3))
        for sgn in (-1, 1):
            s += SL(Z_SRED, f'<circle cx="{ox+sgn*fh*.044:.0f}"'
                            f' cy="{oy+42+fh*.52-fh*.86:.0f}" r="{fh*.030:.0f}"'
                            f' fill="#6fae4c" opacity="{zel:.2f}"/>')
        s += SL(Z_SRED, para_izo_rta(ox + fh * .14, oy + 42 + fh * .52 - fh * .80,
                                     t, i * .3, .7, .4))
    # ЗМЕЙКИ ЗАВИСТИ ползут через улицу к дому
    for i, (bx, bw) in enumerate(mesta):
        s += SL(Z_SRED, _zmeyka_zavisti(bx + bw * .5, gor + 120 + i * 40,
                                        1540, gor + 230, t, i * .33, 1.05))
    # во дворе: цветок вянет, корова отворачивается от ведра
    vyan = A.ease(A.seg(t, .8, 2.4))
    s += SL(Z_SRED, _cvetok_v_gorshke(1420, gor + 64, t, 1.15, vyan))
    s += SL(Z_SRED, _korova(1080, 1052, .78, t, A.ease(A.seg(t, 1.6, 1.6))))
    s += SL(Z_SRED, _dvorovaya_utvar(1180, 1058, 180, t, 191, ["vedro"]))
    # пыль на новой шапке мужа: шапка на колу у крыльца
    s += SL(Z_SRED, f'<line x1="1760" y1="{gor+40:.0f}" x2="1764" y2="{gor-130:.0f}"'
                    f' stroke="url(#derev)" stroke-width="15"/>'
            + f'<ellipse cx="1764" cy="{gor-150:.0f}" rx="58" ry="30"'
              f' fill="#4a3a2c" {o(5)}/>'
            + f'<path d="M1710,{gor-154:.0f} q54,-50 108,0 Z" fill="#5a4636" {o(4)}/>')
    for i in range(7):
        k = ((t * .3 + i * .14) % 1.0)
        s += SL(Z_LETIT, f'<circle cx="{1740+i*12:.0f}"'
                         f' cy="{gor-210+40*k:.0f}" r="{4+2*i%4:.0f}"'
                         f' fill="#b9b2a4" opacity="{.5*(1-k):.2f}"/>')
    # низ кадра
    s += SL(Z_SRED, _polenica(130, gor + 220, 360, 190, 29, 58)
            + _kucha_listev(700, 1054, 330, 193, 92)
            + _kot_zhivoy(480, gor + 330, t, 1.0, "#3b342f", .6)
            + _sledy(1880, 1066, 1420, 880, 6, 197, "#33281d", 1.2))
    # НИЗ КАДРА ОБЖИТ: вёдра у колодезной лавки, кадка, корзина, лужа и
    # грабли поперёк улицы (осмотр: низ пустовал)
    s += SL(Z_SRED, _kadushki_i_grabli(300, 1040, t, 173)
            + _dvorovaya_utvar(860, 1046, 460, t, 179,
                               ["vedro", "korzina", "korob"])
            + _luzha(1560, 1020, 190, t, .5)
            + _yaschiki(1640, 1060, t, 181, 2, .86))
    s += SL(Z_PERED, _stolb_pered(-10, 108, "#1a120c", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 5, .5, .85))
    s += vinetka(.40)
    return s


def tri_novosti_pri_sebe(t):
    """Скамейка у подъезда, три соседки. Средняя в берете по словам убирает
    в сумку коробку, дневник внука и тонометр, застёгивает её и кладёт на
    неё обе ладони. Вместо новостей показывает на небо."""
    rnd = random.Random(283)
    pol = 920
    s = f'<rect width="{W}" height="{H}" fill="#3a4048"/>'
    s += SL(Z_DAL, panelka(60, 620, 900, t, 5, True, 7))
    s += SL(Z_DAL, panelka(1020, 600, 860, t, 5, True, 13))
    s += SL(Z_DAL, goloe_derevo(960, 640, 520, t, 59, 9, "#3a3b43", False))
    s += SL(Z_SRED, _asfalt(pol - 40, 1080, 7, 30))
    s += SL(Z_SRED, _pol_shvy(pol + 20, 1070, 83, 6, "#3c3d40"))
    # подъезд: крыльцо с навесом, дверь, урна, столбики — крупный предмет
    s += SL(Z_SRED, f'<rect x="60" y="{pol-560:.0f}" width="520" height="560"'
                    f' rx="8" fill="{BETON2}" {o(7)}/>'
            + f'<rect x="100" y="{pol-500:.0f}" width="440" height="460" rx="8"'
              f' fill="#3f4650" {o(6)}/>'
            + f'<rect x="120" y="{pol-470:.0f}" width="190" height="430" rx="6"'
              f' fill="url(#derev)" {o(5)}/>'
            + f'<rect x="330" y="{pol-470:.0f}" width="190" height="430" rx="6"'
              f' fill="url(#derev)" {o(5)}/>'
            + f'<rect x="40" y="{pol-600:.0f}" width="580" height="46" rx="10"'
              f' fill="#6a7278" {o(6)}/>')
    s += SL(Z_SRED, tusklaya_lampochka(320, pol - 548, t, 1.1, False))
    s += SL(Z_SRED, _konus_sveta(320, pol - 520, 520, 460, 0, .38))
    # СКАМЕЙКА
    s += SL(Z_SRED, _skameyka_podezda(700, pol + 10, 1020, t, 160))
    # три соседки: рост через одного, одна в профиль, одна со спины
    ros = (470, 300, 450)
    cvet = ("#6a4a52", "#4a5a6a", "#5a4a62")
    tochki = []
    for i in range(3):
        fx = 830 + i * 320
        fh = ros[i]
        fig = figura(fx, pol - 90, fh, t, col=cvet[i], kant="#ffd98a",
                     platok=(i != 1), ph=.2 + i * .35,
                     profil=(i == 2), lico=(i != 0),
                     naklon=(-6, 4, 9)[i])
        u1 = (58, 30 - 26 * A.ease(A.seg(t, 3.6, 1.0)), 62)[i]
        r1, (p1x, p1y), _ = _ruka(fx, pol - 90, fh, 1, fh * .46, u1, t,
                                  cvet[i], "#ffd98a", .2 + i * .2, 4.0)
        r2, (p2x, p2y), _ = _ruka(fx, pol - 90, fh, -1, fh * .44, 62, t,
                                  cvet[i], "#ffd98a", .6 + i * .2, 4.0)
        fig += r1 + r2
        if i == 1:
            # БЕРЕТ НА ТЕМЕНИ, А НЕ НА ГЛАЗАХ: на .90 роста он садился ровно
            # на лицо (осмотр порции 2). Верх головы = рост × .99.
            fig += (f'<ellipse cx="{fx:.0f}" cy="{pol-90-fh*.985:.0f}"'
                    f' rx="{fh*.17:.0f}" ry="{fh*.055:.0f}" fill="#8a4a52" {o(4)}/>'
                    f'<path d="M{fx-fh*.17:.0f},{pol-90-fh*.985:.0f}'
                    f' q{fh*.17:.0f},{-fh*.075:.0f} {fh*.34:.0f},0 Z"'
                    f' fill="#9c5a62" {o(3)}/>'
                    f'<circle cx="{fx+fh*.05:.0f}" cy="{pol-90-fh*1.045:.0f}"'
                    f' r="{fh*.026:.0f}" fill="#8a4a52" {o(2)}/>')
        s += SL(Z_SRED, fig)
        tochki.append((p1x, p1y, p2x, p2y, fh, i))
    # СУМКА на коленях средней: вещи уходят в неё по одной
    # сумка НА КОЛЕНЯХ: при pol-180 она ложилась ровно на лицо средней
    # соседки (осмотр порции 2 — закрыто 100%)
    sx = 1150
    zast = A.ease(A.seg(t, 3.2, .8))
    veschi = ("korobka", "dnevnik", "tonometr")
    for i, v in enumerate(veschi):
        k = A.ease(A.seg(t, .4 + i * .85, .7))
        vx = 1480 - 190 * k
        vy = pol - 300 + 190 * k
        if k >= 1.0:
            # вещь уже в сумке, но ВИДНА: торчит над её краем, а не исчезает
            vx, vy = sx - 120 + i * 120, pol - 140
        if v == "korobka":
            s += SL(Z_SRED, f'<rect x="{vx-66:.0f}" y="{vy-56:.0f}" width="132"'
                            f' height="100" rx="8" fill="#c9b79c" {o(5)}/>'
                    f'<path d="M{vx-66:.0f},{vy-20:.0f} h132" stroke="#9a8a68"'
                    f' stroke-width="6"/>'
                    f'<path d="M{vx-70:.0f},{vy-56:.0f} q{70:.0f},{-34:.0f}'
                    f' {140:.0f},0" fill="none" stroke="#b8352c" stroke-width="8"/>')
        elif v == "dnevnik":
            s += SL(Z_SRED, f'<rect x="{vx-50:.0f}" y="{vy-62:.0f}" width="100"'
                            f' height="126" rx="7" fill="#3f5c7a" {o(5)}/>'
                    f'<rect x="{vx-40:.0f}" y="{vy-50:.0f}" width="80" height="102"'
                    f' rx="5" fill="#f2ece0" opacity=".9"/>'
                    f'<path d="M{vx-28:.0f},{vy-20:.0f} q26,-10 52,2" fill="none"'
                    f' stroke="#9a8a68" stroke-width="5"/>')
        else:
            s += SL(Z_SRED, f'<rect x="{vx-56:.0f}" y="{vy-40:.0f}" width="112"'
                            f' height="80" rx="12" fill="#5e676e" {o(5)}/>'
                    f'<circle cx="{vx-16:.0f}" cy="{vy:.0f}" r="22"'
                    f' fill="#eaf0f4" {o(3)}/>'
                    f'<path d="M{vx+20:.0f},{vy-16:.0f} q{30:.0f},{18:.0f}'
                    f' {8:.0f},{44:.0f}" fill="none" stroke="#3a4049"'
                    f' stroke-width="9"/>')
    s += SL(Z_SRED, _sumka_hozyaystvennaya(sx, pol - 50, t, .78, zast))
    # варежки поверх вещей и сумки
    for p1x, p1y, p2x, p2y, fh, i in tochki:
        s += SL(Z_SRED, ""
               )
    # голуби у скамейки и урна
    for i in range(4):
        s += SL(Z_SRED, _golub(620 + i * 230, 1050 + (i % 2) * 20, t,
                               1.05 + (i % 3) * .12, i * .3, True))
    s += SL(Z_SRED, f'<path d="M1800,{pol+10:.0f} L1900,{pol+10:.0f}'
                    f' L1884,{pol-170:.0f} L1816,{pol-170:.0f} Z"'
                    f' fill="#5e676e" {o(6)}/>'
            + f'<ellipse cx="1850" cy="{pol-170:.0f}" rx="34" ry="12"'
              f' fill="#3e4348" {o(4)}/>')
    # низ кадра
    s += SL(Z_SRED, _gorodskoy_hlam(170, pol + 40, 420, t, 43,
                                    ["stolbik", "korobka", "kust"])
            + _kot_zhivoy(1660, 1056, t, 1.1, "#423b35", .5)
            + _kucha_listev(520, 1062, 300, 199, 86))
    s += SL(Z_PERED, _vetka_pered(1980, 120, 740, 160, t, 19, "#241c16", 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 5, .45, .8))
    s += vinetka(.40)
    return s


def radost_v_ladonyah(t):
    """Окно дома снаружи: на подоконнике цветы, занавеска. Женщина в комнате
    держит в сложенных лодочкой ладонях светящийся комочек-радость и
    задёргивает занавеску локтем. Сглаз заглядывает и летит дальше."""
    rnd = random.Random(293)
    gor = 760
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 61)
    s += oblaka(t, 150, 4, 67, .38, "#cdd7e4", 15.0)
    # СТЕНА ДОМА с наличниками — крупный предмет, окно в середине
    s += SL(Z_DAL, brevna(120, 60, 1100, gor - 60, 96)
            + brevna(1220, 110, 700, gor - 110, 96))
    s += SL(Z_DAL, f'<path d="M80,80 L700,-40 L1320,80 Z" fill="#4a3a28" {o(7)}/>'
            + f'<rect x="60" y="60" width="1280" height="44" rx="10"'
              f' fill="#5b4428" {o(6)}/>')
    # окно: рама, наличники с резьбой, подоконник с цветами
    ox, oy, ow, oh = 420, 230, 620, 420
    s += SL(Z_SRED, f'<rect x="{ox-40:.0f}" y="{oy-40:.0f}" width="{ow+80:.0f}"'
                    f' height="{oh+80:.0f}" rx="10" fill="#6a5030" {o(7)}/>'
            + f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
              f' fill="#2b3550" opacity=".95"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{ox-46+i*106:.0f},{oy-46:.0f} l34,-44 l34,44 Z"'
                        f' fill="#7d5a3c" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{ox-70:.0f}" y="{oy+oh:.0f}" width="{ow+140:.0f}"'
                    f' height="44" rx="10" fill="url(#dosk)" {o(6)}/>')
    # ЗАНАВЕСКА задёргивается
    zad = A.ease(A.seg(t, .8, 1.5))
    s += SL(Z_SRED, zanaveska(ox + 10, oy + 10, oh - 20, 180 + 220 * zad,
                              "#e8dcc0", t, 1)
            + zanaveska(ox + ow - 10, oy + 10, oh - 20, 180 + 220 * zad,
                        "#e8dcc0", t, -1))
    # женщина в комнате у окна: обе ладони лодочкой у груди
    fx, fy, fh = 730, oy + oh + 110, 520
    jen = figura(fx, fy, fh, t, col="#5a4a62", kant="#ffd98a", platok=True,
                 ph=.3, naklon=-4.0)
    j1, (l1x, l1y), _ = _ruka_so_sgibom(fx, fy, fh, 1, fh * .22, 42,
                                        fh * .24, -18, t, "#5a4a62",
                                        "#ffd98a", .3, 3.0)
    j2, (l2x, l2y), _ = _ruka_so_sgibom(fx, fy, fh, -1, fh * .22, 46,
                                        fh * .24, -14, t, "#5a4a62",
                                        "#ffd98a", .7, 3.0)
    jen += j1 + j2
    s += SL(Z_SRED, f'<g clip-path="none">{jen}</g>')
    # КОМОЧЕК-РАДОСТЬ светится между ладонями
    # КОМОЧЕК НИЖЕ И МЕЛЬЧЕ: у груди, а не под подбородком. С мимикой и в
    # размер головы он читался ВТОРЫМ ЛИЦОМ под лицом фигуры (осмотр).
    kx, ky = (l1x + l2x) / 2, (l1y + l2y) / 2 + 58
    s += SL(Z_SRED, _komochek_radosti(kx, ky, t, .62, .1))
    s += SL(Z_SRED, "")
    # комочек живой: от него летят искорки — это и есть тёплое пятно сцены
    s += SL(Z_SRED, iskra_let(t, kx, ky, 9, 103, 150, .5))
    # цветы на подоконнике покачиваются
    for i in range(4):
        s += SL(Z_SRED, _cvetok_v_gorshke(ox + 70 + i * 160, oy + oh + 44, t,
                                          .92 + (i % 3) * .1, .0))
    # СГЛАЗ пролетает мимо окна и ничего не видит
    pl = A.seg(t, .2, 3.0)
    s += SL(Z_PERED, _sglaz(-120 + 2200 * pl, oy - 60 + 60 * math.sin(pl * 6.0),
                            t, .8, .2, .9))
    # земля под окном: завалинка, поленница, кадушка, следы, кот
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#4e4030"/>'
            + _zemlya_faktura(gor + 30, 1050, 23, 15, "#3f3326")
            + _listya(101, 42, gor + 40, 1060)
            + _inej(103, 36, gor + 50, 1060)
            + _pol_shvy(gor + 30, 1070, 107, 5, "#3a2c20"))
    s += SL(Z_SRED, _zavalinka(140, gor + 150, 1060, t, 160))
    s += SL(Z_SRED, _polenica(1300, gor + 120, 420, 200, 31, 60)
            + _kadushki_i_grabli(170, gor + 330, t, 13)
            + _kucha_listev(900, 1056, 320, 109, 90)
            + _kot_zhivoy(700, gor + 330, t, 1.05, "#3b342f", .3)
            + _sledy(1880, 1066, 1360, 900, 6, 113, "#33281d", 1.2))
    s += SL(Z_SRED, teplo(730, oy + oh * .5, 520, 420, .40))
    s += SL(Z_PERED, _vetka_pered(-70, 130, 700, 24, t, 23, "#241c16", 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 5, .5, .85))
    s += vinetka(.40)
    return s


def babushka_shepchet_na_uho(t):
    """Кухня, стол с самоваром, баранки, варенье в розетках. Бабушка
    наклонилась к дочери и прикрывает рот ладонью, как ширмой; дочь слушает
    с чашкой, а за окном соседка идёт с вёдрами на коромысле."""
    rnd = random.Random(307)
    pol = 964
    s = f'<rect width="{W}" height="{H}" fill="#2a241c"/>'
    s += SL(Z_DAL, brevna(0, 40, 1060, pol - 40, 96)
            + brevna(1060, 40, 860, pol - 40, 96))
    s += SL(Z_DAL, _polka_s_utvaryu(80, 230, 620, t, 109, 5))
    s += SL(Z_DAL, _polka_s_utvaryu(96, 520, 560, t, 113, 4))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#5e4a34"/>'
            + polovicy(pol + 18) + _pol_shvy(pol + 20, 1070, 127, 6, "#4a3824"))
    # ОКНО: за ним улица, по ней идёт соседка с коромыслом
    wx, wy, ww, wh = 1180, 210, 620, 400
    s += SL(Z_DAL, f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}"'
                   f' height="{wh:.0f}" fill="#46536b"/>')
    s += SL(Z_DAL, ulica_dal(wx, wy + wh - 40, ww, t, False, 29))
    kx = wx - 160 + 940 * A.seg(t, .2, 4.6)
    kh2 = 210
    sos = figura(kx, wy + wh - 30, kh2, t, col="#46506a", kant="#cfe4f5",
                 platok=True, ph=.4, profil=True, naklon=4.0)
    # она в слое Z_DAL за стеклом — обычная `_ruka`, обходить фигуры
    # другого плана ей не нужно
    c1, (m1x, m1y), _ = _ruka(kx, wy + wh - 30, kh2, 1, kh2 * .34, -30, t,
                              "#46506a", "#cfe4f5", .4, 4.0)
    c2, (m2x, m2y), _ = _ruka(kx, wy + wh - 30, kh2, -1, kh2 * .34, -26, t,
                              "#46506a", "#cfe4f5", .8, 4.0)
    sos += c1 + c2
    # коромысло с вёдрами — палка 300 px, держится обеими руками
    sos += (f'<line x1="{m2x-26:.0f}" y1="{m2y-16:.0f}" x2="{m1x+26:.0f}"'
            f' y2="{m1y-16:.0f}" stroke="url(#derev)" stroke-width="15"'
            f' stroke-linecap="round"/>')
    for ex in (m2x - 14, m1x + 14):
        sos += (f'<line x1="{ex:.0f}" y1="{m1y-12:.0f}" x2="{ex:.0f}"'
                f' y2="{m1y+40:.0f}" stroke="#8a6a3c" stroke-width="5"/>'
                f'<path d="M{ex-26:.0f},{m1y+40:.0f} L{ex+26:.0f},{m1y+40:.0f}'
                f' L{ex+18:.0f},{m1y+94:.0f} L{ex-18:.0f},{m1y+94:.0f} Z"'
                f' fill="url(#zhel)" {o(4)}/>')
    sos += _varezhka(m1x, m1y, kh2, t, .4, "#dcd0bc")
    sos += ""
    s += SL(Z_DAL, f'<g clip-path="none">{sos}</g>')
    s += SL(Z_SRED, f'<rect x="{wx-34:.0f}" y="{wy-34:.0f}" width="{ww+68:.0f}"'
                    f' height="{wh+68:.0f}" rx="10" fill="none" stroke="#6a5030"'
                    f' stroke-width="30"/>'
            + f'<line x1="{wx+ww*.5:.0f}" y1="{wy:.0f}" x2="{wx+ww*.5:.0f}"'
              f' y2="{wy+wh:.0f}" stroke="#6a5030" stroke-width="20"/>'
            + f'<line x1="{wx:.0f}" y1="{wy+wh*.5:.0f}" x2="{wx+ww:.0f}"'
              f' y2="{wy+wh*.5:.0f}" stroke="#6a5030" stroke-width="18"/>'
            + f'<rect x="{wx-54:.0f}" y="{wy+wh+30:.0f}" width="{ww+108:.0f}"'
              f' height="42" rx="10" fill="url(#dosk)" {o(6)}/>')
    # СТОЛ — крупный предмет, на нём самовар, баранки, варенье
    s += SL(Z_SRED, stol(180, pol - 320, 1180, 40, True))
    sy = pol - 320
    s += SL(Z_SRED, _samovar(500, sy - 6, t, 1.0))
    s += SL(Z_SRED, par(500, sy - 350, t, 5, .5, 210, .42, 1.2))
    s += SL(Z_SRED, _baranki(880, sy - 60, t, 5, 1.0, True))
    s += SL(Z_SRED, _baranki(1180, sy - 10, t, 3, .92, False))
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{700+i*120:.0f},{sy-8:.0f}'
                        f' q{40:.0f},{40:.0f} {80:.0f},0 Z" fill="#f0ece0" {o(5)}/>'
                f'<ellipse cx="{740+i*120:.0f}" cy="{sy-10:.0f}" rx="40" ry="13"'
                f' fill="#9c2f28" opacity=".9"/>')
    s += SL(Z_SRED, _kruzhka(1300, sy - 6, 1.0, 0, "#efe3d4", 1))
    # бабушка наклонилась к дочери: ладонь ширмой у рта
    bx, by_, bh = 660, pol + 10, 540
    s += SL(Z_SRED, _tabyret(bx - 30, pol + 6, t, 180, 180))
    _figury_kadra((660, pol + 10 - 180, 540), (1180, pol + 16 - 190, 620))
    bab = figura(bx, by_ - 180, bh, t, col="#54505e", kant="#ffd98a",
                 platok=True, ph=.4, naklon=10.0, profil=True)
    b1, (h1x, h1y), _ = _ruka_sgib_mimo(bx, by_ - 180, bh, 1, bh * .20, 30,
                                        bh * .22, -34, t, "#54505e",
                                        "#ffd98a", .4, 4.0)
    b2, (h2x, h2y), _ = _ruka_mimo(bx, by_ - 180, bh, -1, bh * .44, 62, t,
                              "#54505e", "#ffd98a", .8, 3.0)
    bab += b1 + b2
    s += SL(Z_SRED, bab)
    # ладонь-ширма у рта и шёпот волной
    s += SL(Z_SRED, f'<ellipse cx="{h1x:.0f}" cy="{h1y:.0f}" rx="40" ry="52"'
                    f' fill="#e8d8c0" {o(6)}/>')
    for i in range(3):
        k = ((t * .7 + i * .33) % 1.0)
        s += SL(Z_SRED, f'<path d="M{h1x+30:.0f},{h1y-10:.0f}'
                        f' q{30+40*k:.0f},{-18:.0f} {60+80*k:.0f},{4:.0f}"'
                        f' fill="none" stroke="#eaf4ff" stroke-width="6"'
                        f' opacity="{.6*(1-k):.2f}"/>')
    # дочь слушает: обе руки на чашке, глаза округляются
    dx, dy_, dh = 1180, pol + 16, 620
    s += SL(Z_SRED, _venskiy_stul(1232, pol + 8, 600, t, 2.0, True))
    doch = figura(dx, dy_ - 190, dh, t, col="#6a4a52", kant="#ffd98a",
                  ph=.9, naklon=-6.0)
    d1, (g1x, g1y), _ = _ruka_mimo(dx, dy_ - 190, dh, -1, dh * .40, 36, t,
                              "#6a4a52", "#ffd98a", .9, 3.0)
    d2, (g2x, g2y), _ = _ruka_mimo(dx, dy_ - 190, dh, -1, dh * .32, 56, t,
                              "#6a4a52", "#ffd98a", .5, 3.0)
    doch += d1 + d2
    s += SL(Z_SRED, doch)
    s += SL(Z_SRED, _kruzhka((g1x + g2x) / 2 - 10, (g1y + g2y) / 2 + 20, 1.0,
                             4 * A.w(t, 1.9, .3), "#f0eade", 1))
    s += SL(Z_SRED, _varezhka(g1x, g1y, dh, t, .9) + _varezhka(g2x, g2y, dh, t, .5))
    # округлившиеся глаза дочери
    for sgn in (-1, 1):
        s += SL(Z_SRED, f'<circle cx="{dx+sgn*dh*.044:.0f}"'
                        f' cy="{dy_-190-dh*.86:.0f}" r="{dh*.026:.0f}"'
                        f' fill="#f2f6fa" opacity=".8"/>')
    s += SL(Z_SRED, par(dx, dy_ - 190 - dh * .70, t, 3, .3, 110, .3, .8))
    # низ кадра
    s += SL(Z_SRED, _polovik(640, pol + 30, 620, 104)
            + _dvorovaya_utvar(96, pol + 92, 320, t, 211, ["kadka", "korzina"])
            + _yaschiki(1600, pol + 86, t, 223, 2, .86)
            + _kot_zhivoy(1420, pol + 70, t, 1.1, "#3b342f", .7, True, True)
            + kartoshka(430, pol + 96, t, 6, 6, .95))
    s += SL(Z_SRED, teplo(500, sy - 240, 520, 420, .40))
    s += SL(Z_PERED, _stolb_pered(-8, 96, "#181209", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 500, sy - 320, 6, 29, 190, .3))
    s += vinetka(.40)
    return s


def tri_stuka_po_stolu(t):
    """Край деревянного кухонного стола на пол-кадра: хлебница, солонка,
    чашка. Мужчина трижды стучит костяшками по столешнице, от каждого стука
    расходится круг, и Сглаз над его левым плечом лопается."""
    rnd = random.Random(311)
    pol = 1000
    s = f'<rect width="{W}" height="{H}" fill="#2c2620"/>'
    s += SL(Z_DAL, doski(0, 0, 1140, 760, 98, True, "dosk"))
    s += SL(Z_DAL, doski(1140, 0, 780, 760, 98, True, "dosk"))
    s += SL(Z_DAL, _polka_s_utvaryu(1180, 250, 640, t, 127, 5))
    s += SL(Z_DAL, _knizhnaya_polka(120, 300, 600, t, 131, 2, 196))
    s += SL(Z_DAL, f'<rect x="0" y="744" width="{W}" height="40" rx="8"'
                   f' fill="#4a3522" {o(5)}/>')
    s += SL(Z_DAL, tusklaya_lampochka(960, 130, t, 1.3, True))
    s += SL(Z_DAL, _konus_sveta(960, 180, 760, 560, 0, .38))
    s += SL(Z_DAL, _polka_s_utvaryu(760, 300, 420, t, 383, 3))
    s += SL(Z_DAL, _polki_otkrytye(760, 480, 420, t, 389, 1, True, .0))
    # вязанки лука и сушёных травок на гвоздях, рушник и сито на стене
    for i in range(4):
        s += SL(Z_DAL, f'<path d="M{1620+i*76:.0f},200 q{-26:.0f},{80:.0f}'
                       f' {4:.0f},{148:.0f} q{30:.0f},{20:.0f} {44:.0f},{-14:.0f}'
                       f' q{14:.0f},{-74:.0f} {-18:.0f},{-134:.0f} Z"'
                       f' fill="#c9a05a" {o(5)}/>'
                f'<line x1="{1628+i*76:.0f}" y1="200" x2="{1644+i*76:.0f}"'
                f' y2="162" stroke="#8a7a46" stroke-width="7"/>')
    s += SL(Z_DAL, f'<circle cx="300" cy="620" r="86" fill="none" stroke="#6a5030"'
                   f' stroke-width="22"/>'
            + f'<circle cx="300" cy="620" r="70" fill="#cdbf9c" opacity=".7"/>')
    for i in range(7):
        s += SL(Z_DAL, f'<line x1="{238+i*18:.0f}" y1="556" x2="{238+i*18:.0f}"'
                       f' y2="684" stroke="#9a8a68" stroke-width="4"'
                       f' opacity=".8"/>')
    s += SL(Z_DAL, f'<rect x="520" y="560" width="110" height="280" rx="9"'
                   f' fill="url(#rush)" {o(5)}/>'
            + f'<rect x="520" y="660" width="110" height="18" fill="{TKAN}"'
              f' opacity=".8"/>'
            + f'<rect x="520" y="760" width="110" height="18" fill="{TKAN2}"'
              f' opacity=".7"/>')
    # СТОЛ КРУПНО: край столешницы во всю ширину кадра
    sy = 700
    s += SL(Z_SRED, f'{ten(960, pol + 40, 640, 30, .5)}'
                    f'<path d="M-20,{sy:.0f} L1940,{sy:.0f} L1940,{sy+86:.0f}'
                    f' L-20,{sy+86:.0f} Z" fill="url(#derev)" {o(8)}/>'
            + f'<rect x="60" y="{sy+86:.0f}" width="1400" height="28" rx="8"'
              f' fill="#5b4428" {o(5)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{-20+i*230:.0f},{sy+10:.0f}'
                        f' q{60:.0f},{24:.0f} {120:.0f},{6:.0f}" fill="none"'
                        f' stroke="#8a6a44" stroke-width="6" opacity=".6"/>')
    for i in (0, 1):
        s += SL(Z_SRED, f'<rect x="{200+i*1300:.0f}" y="{sy+114:.0f}" width="80"'
                        f' height="{pol+70-sy-114:.0f}" rx="12"'
                        f' fill="#5b4428" {o(6)}/>')
    # КРУГИ от стуков по столешнице
    # (круги и кулак ставятся НИЖЕ, по фактической точке кисти: жёсткие
    # 870 расходились в 153 px от руки — осмотр порции 2)
    # хлебница, солонка, чашка — вздрагивает от стука
    drog = 6 * math.sin(t * 22) * max(.0, 1 - abs(((t - .5) % .7) * 6))
    s += SL(Z_SRED, f'<rect x="1180" y="{sy-96:.0f}" width="260" height="96"'
                    f' rx="20" fill="url(#solom)" {o(6)}/>'
            + f'<path d="M1192,{sy-96:.0f} q128,-54 236,0" fill="none"'
              f' stroke="#8a6a3c" stroke-width="10"/>'
            + karavay(1310, sy - 92, .58, False))
    s += SL(Z_SRED, f'<path d="M1520,{sy-6:.0f} L1596,{sy-6:.0f}'
                    f' L1584,{sy-78:.0f} L1532,{sy-78:.0f} Z" fill="#f0ece0" {o(5)}/>'
            + f'<ellipse cx="1558" cy="{sy-78:.0f}" rx="26" ry="9"'
              f' fill="#dcd4c4" {o(3)}/>')
    s += SL(Z_SRED, f'<g transform="translate({drog:.1f},0)">'
                    f'{_kruzhka(1700, sy - 6, 1.15, 0, "#e8eef0", -1)}</g>')
    s += SL(Z_SRED, par(1700, sy - 110, t, 3, .36, 130, .34, .9))
    # мужчина за столом: левая держит чашку, правая стучит костяшками
    fx, fy, fh = 700, pol + 150, 700
    pov = A.ease(A.seg(t, 2.6, .9))
    muz = figura(fx, fy - 230, fh, t, col="#4a5a52", kant="#ffd98a", ph=.3,
                 naklon=-4 + 6 * pov, profil=(pov > .5))
    m1, (r1x, r1y), _ = _ruka(fx, fy - 230, fh, 1, fh * .44,
                              44 + 10 * math.sin(t * 9), t,
                              "#4a5a52", "#ffd98a", .3, 4.0)
    m2, (r2x, r2y), _ = _ruka(fx, fy - 230, fh, -1, fh * .40, 50, t,
                              "#4a5a52", "#ffd98a", .7, 3.0)
    muz += m1 + m2
    s += SL(Z_SRED, muz)
    s += SL(Z_SRED, _kruzhka(r2x - 10, r2y + 20, 1.0, 0, "#f0eade", -1))
    s += SL(Z_SRED, _varezhka(r2x, r2y, fh, t, .7))
    # КУЛАК РОВНО НА КОНЦЕ РУКАВА, круги расходятся от него
    kulx, kuly = r1x, r1y + 10
    udar = 14 * max(.0, math.sin(t * 9))
    s += SL(Z_SRED, _krugi_po_stolu(kulx, kuly + 18, t, 3, .0, 300))
    s += SL(Z_SRED, _kulak(kulx, kuly - udar, 1.3, t, .2))
    # СГЛАЗ над левым плечом лопается, как мыльный шарик
    lop = A.ease(A.seg(t, 2.1, .5))
    if lop < 1.0:
        s += SL(Z_SRED, _sglaz(fx - 230, fy - 230 - fh * .92, t, .92 + .3 * lop,
                               .3, .92 * (1 - lop)))
    for i in range(7):
        if lop > 0:
            a = math.radians(i * 51)
            rr = 120 * lop
            s += SL(Z_SRED, f'<circle cx="{fx-230+rr*math.cos(a):.0f}"'
                            f' cy="{fy-230-fh*.92+rr*math.sin(a):.0f}"'
                            f' r="{14*(1-lop):.0f}" fill="#8a919a"'
                            f' opacity="{.8*(1-lop):.2f}"/>')
    # низ кадра: табурет, половик, валенки, кот, ящик
    s += SL(Z_PERED, _polovik(560, pol + 40, 760, 110)
            + _valenki_u_dveri(300, pol + 70, 1.0, t)
            + _kot_zhivoy(1480, pol + 60, t, 1.2, "#3b342f", .4)
            + _yaschiki(96, pol + 60, t, 137, 2, .9))
    # НИЗ КАДРА: кадка, вёдра, корзина и кошачья плошка под столом
    s += SL(Z_SRED, _dvorovaya_utvar(620, pol + 30, 520, t, 167,
                                     ["kadka", "vedro", "korzina", "korob"])
            + f'<ellipse cx="1360" cy="{pol+36:.0f}" rx="58" ry="21"'
              f' fill="url(#glina)" {o(5)}/>'
            + f'<ellipse cx="1360" cy="{pol+30:.0f}" rx="44" ry="14"'
              f' fill="#8a5a30" opacity=".9"/>')
    s += SL(Z_PERED, _stolb_pered(1860, 88, "#171209", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 960, 180, 6, 31, 170, .24))
    s += vinetka(.40)
    return s


def dvor_s_tremya_zabotami(t):
    """Яркий морозный день: деревенский двор одним кадром. У калитки девушка
    бросает монету, на крыльце мать держит чёрную редьку, справа отец несёт
    дрова к баньке. В окне избы — настоящая редька в корзине."""
    rnd = random.Random(313)
    gor = 640
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, False, 71)
    s += oblaka(t, 140, 5, 73, .5, "#eef4fa", 16.0)
    s += SL(Z_DAL, _derevnya_ryad(gor - 90, t, 31, ((120, 300), (430, 250))))
    s += SL(Z_DAL, goloe_derevo(760, gor - 30, 480, t, 79, 8, "#4a4b53", True))
    s += SL(Z_DAL, _zabor_dosok(-30, gor - 170, 820, 180, 41, 56))
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#c8cfd8"/>'
            + f'<path d="M-20,{gor+70:.0f} Q480,{gor+20:.0f} 980,{gor+86:.0f}'
              f' Q1480,{gor+150:.0f} 1940,{gor+96:.0f} L1940,1080 L-20,1080 Z"'
              f' fill="url(#sneg)" {o(0)}/>'
            + _inej(139, 60, gor + 60, 1060)
            + _pol_shvy(gor + 60, 1070, 149, 5, "#9fb0c0"))
    # ИЗБА С КРЫЛЬЦОМ — крупный предмет; в окне настоящий кадр
    s += SL(Z_SRED, f'{ten(1020, gor + 120, 400, 30, .4)}'
                    f'<rect x="620" y="{gor-420:.0f}" width="1020" height="500"'
                    f' rx="10" fill="url(#brev)" {o(8)}/>')
    s += SL(Z_SRED, brevna(620, gor - 420, 1020, 500, 92))
    s += SL(Z_SRED, f'<path d="M580,{gor-420:.0f} L1130,{gor-610:.0f}'
                    f' L1680,{gor-420:.0f} Z" fill="#5a4636" {o(7)}/>'
            + f'<path d="M580,{gor-420:.0f} L1130,{gor-610:.0f} L1680,{gor-420:.0f}'
              f' l-40,0 L1130,{gor-566:.0f} L620,{gor-420:.0f} Z"'
              f' fill="url(#sneg)" opacity=".92"/>')
    # НАСТОЯЩИЙ КАДР в окне над крыльцом: вид, метка, наличник поверх
    px, py, pw, ph_ = 760, gor - 390, 800, 330
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<clipPath id="okn3"><path d="{put}"/></clipPath>'
           f'<g clip-path="url(#okn3)">'
           f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
           f' fill="#4a4034"/>'
           f'<path d="M{px:.0f},{py+ph_*.58:.0f} L{px+pw:.0f},{py+ph_*.58:.0f}'
           f' L{px+pw:.0f},{py+ph_:.0f} L{px:.0f},{py+ph_:.0f} Z"'
           f' fill="url(#solom)"/>')
    for i in range(5):
        vid += (f'<ellipse cx="{px+150+i*130:.0f}" cy="{py+ph_*.62:.0f}" rx="58"'
                f' ry="36" fill="#2e2b2a" opacity=".9"/>'
                f'<path d="M{px+150+i*130:.0f},{py+ph_*.52:.0f}'
                f' q{20:.0f},{-54:.0f} {48:.0f},{-70:.0f}" fill="none"'
                f' stroke="#5c7a40" stroke-width="10"/>')
    vid += "</g>"
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#6a5030"'
                    f' stroke-width="30"/>'
            + f'<rect x="{px-40:.0f}" y="{py-48:.0f}" width="{pw+80:.0f}"'
              f' height="40" rx="10" fill="#7d5a3c" {o(5)}/>'
            + f'<rect x="{px-54:.0f}" y="{py+ph_-10:.0f}" width="{pw+108:.0f}"'
              f' height="42" rx="10" fill="url(#dosk)" {o(6)}/>'
            + f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#6a5030" stroke-width="22"/>')
    s += SL(Z_SRED, _kryl_co(430, gor + 60, 420, 130, t, 3, True, True))
    # БАНЬКА справа с дымом из трубы
    s += SL(Z_SRED, izba_snaruzhi(1640, gor - 40, 330, t, True, True, 43))
    s += SL(Z_SRED, dym(1690, gor - 240, t, 6, .3, 340, .42, "#e2e8ee", 1.4))
    # КАЛИТКА слева, девушка бросает монету за неё
    s += SL(Z_SRED, _vorota_dvora(120, gor + 180, 300, 330, t, .25))
    dvx, dvy, dvh = 340, gor + 300, 560
    bros = A.ease(A.seg(t, .4, .8))
    _figury_kadra((340, gor + 300, 560), (590, gor - 50, 470),
                  (1810, gor + 330, 660))
    dev = figura(dvx, dvy, dvh, t, col="#6a4a62", kant="#ffd98a", platok=True,
                 ph=.2, naklon=5.0)
    d1, (a1x, a1y), _ = _ruka_mimo(dvx, dvy, dvh, 1, dvh * .44, 20 - 62 * bros, t,
                              "#6a4a62", "#ffd98a", .2, 5.0)
    d2, (a2x, a2y), _ = _ruka_mimo(dvx, dvy, dvh, -1, dvh * .36, 44, t,
                              "#6a4a62", "#ffd98a", .6, 4.0)
    dev += d1 + d2
    s += SL(Z_SRED, dev)
    s += SL(Z_SRED, _ploshka_s_meloch(a2x - 30, a2y + 30, t, .78, 6, 151))
    s += SL(Z_SRED, _varezhka(a1x, a1y, dvh, t, .2) + _varezhka(a2x, a2y, dvh, t, .6))
    # монета летит за калитку
    mk = A.seg(t, 1.0, 1.6)
    s += SL(Z_SRED, _moneta_krupno(a1x - 220 * mk, a1y - 120 * math.sin(math.pi * mk) + 200 * mk,
                                   46, t, .2, True, True, .3))
    # МАТЬ на крыльце с чёрной редькой в обеих руках
    mx, my, mh = 590, gor + 70, 470
    s += SL(Z_SRED, _lavka_krupno(430, gor + 76, 420, t, 120, False))
    mat = figura(mx, my - 120, mh, t, col="#4a5a6a", kant="#ffd98a",
                 platok=True, ph=.5, naklon=-3.0)
    m1, (b1x, b1y), _ = _ruka_mimo(mx, my - 120, mh, 1, mh * .40, 28, t,
                              "#4a5a6a", "#ffd98a", .5, 3.0)
    m2, (b2x, b2y), _ = _ruka_mimo(mx, my - 120, mh, -1, mh * .40, 30, t,
                              "#4a5a6a", "#ffd98a", .9, 3.0)
    mat += m1 + m2
    s += SL(Z_SRED, mat)
    # РЕДЬКА НА КОЛЕНЯХ, А НЕ НА ЛИЦЕ: при s_=1,35 её ботва вставала ровно
    # в лицо матери и читалась кадкой с растением (осмотр порции 2)
    s += SL(Z_SRED, _redka((b1x + b2x) / 2, (b1y + b2y) / 2 + 142, .78, t, -14, .3))
    s += SL(Z_SRED, "")
    # ОТЕЦ несёт дрова в обеих руках — крупнее матери, в профиль
    ox2, oy2, oh2 = 1810, gor + 330, 660
    shag = A.seg(t, .2, 5.0)
    otec = figura(ox2 - 120 + 120 * shag, oy2, oh2, t, col="#46506a",
                  kant="#cfe4f5", shapka=True, boroda=True, ph=.8,
                  profil=True, naklon=6.0)
    o1, (c1x, c1y), _ = _ruka_mimo(ox2 - 120 + 120 * shag, oy2, oh2, -1, oh2 * .34,
                              28, t, "#46506a", "#cfe4f5", .8, 4.0)
    o2, (c2x, c2y), _ = _ruka_mimo(ox2 - 120 + 120 * shag, oy2, oh2, -1, oh2 * .28,
                              52, t, "#46506a", "#cfe4f5", .4, 4.0)
    otec += o1 + o2
    s += SL(Z_SRED, otec)
    # охапка поленьев в руках
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{c1x-120+ (i % 3) * 56:.0f}"'
                        f' y="{c1y-30+(i//3)*40:.0f}" width="130" height="36"'
                        f' rx="16" fill="url(#derev)" {o(5)}/>'
                f'<ellipse cx="{c1x-120+(i % 3) * 56:.0f}"'
                f' cy="{c1y-12+(i//3)*40:.0f}" rx="12" ry="17"'
                f' fill="#8a6a44" {o(3)}/>')
    s += SL(Z_SRED, _varezhka(c1x, c1y, oh2, t, .8, "#dcd0bc")
           )
    s += SL(Z_SRED, para_izo_rta(ox2 - 80 + 120 * shag, oy2 - oh2 * .80, t,
                                 .2, 1.3, .5))
    # низ кадра
    s += SL(Z_SRED, _polenica(1700, gor + 330, 300, 190, 47, 58)
            + _dvorovaya_utvar(540, gor + 400, 420, t, 229,
                               ["korzina", "vedro", "korob"])
            + _kot_zhivoy(820, gor + 420, t, 1.05, "#3b342f", .5)
            + _sledy(300, 1066, 900, 860, 7, 233, "#8fa3b4", 1.3)
            + _kucha_listev(1360, 1058, 300, 239, 84))
    # ветка поднята: её контур резал лицо матери слева (осмотр)
    s += SL(Z_PERED, _vetka_pered(-70, 40, 560, 16, t, 29, "#241c16", 5))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 5, .4, .8))
    s += vinetka(.34)
    return s


def devushka_kradetsya_iz_spyaschey_iz(t):
    """Сени спящей избы в синих сумерках перед зарёй: на лавке храпит дед,
    на печи детские пятки, на гвозде тулупы. Девушка в сорочке крадётся на
    цыпочках к двери, прижимая к груди плошку с безделушками."""
    rnd = random.Random(317)
    pol = 980
    s = f'<rect width="{W}" height="{H}" fill="#1a2238"/>'
    s += SL(Z_DAL, brevna(0, 30, 1080, pol - 30, 96)
            + brevna(1080, 30, 840, pol - 30, 96))
    s += SL(Z_DAL, _polka_s_utvaryu(96, 240, 540, t, 241, 4))
    s += SL(Z_DAL, _polka_s_utvaryu(100, 540, 500, t, 397, 4))
    s += SL(Z_DAL, _polati(640, 180, 620, t, 3))
    # кадки, вёдра и короба вдоль стены сеней
    s += SL(Z_SRED, _dvorovaya_utvar(500, pol - 6, 520, t, 401,
                                     ["kadka", "vedro", "korob", "korzina"]))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#4a3c2c"/>'
            + polovicy(pol + 16) + _pol_shvy(pol + 20, 1070, 251, 6, "#3a2c1e"))
    # ПЕЧЬ с детскими пятками на лежанке — крупный предмет
    s += SL(Z_SRED, pech(1300, 300, 600, 600, t, True, True, True))
    s += SL(Z_SRED, ugli(1430, 790, 300, t, 7, 3))
    s += SL(Z_SRED, teplo(1560, 800, 480, 380, .40))
    for i in (0, 1):
        s += SL(Z_SRED, f'<ellipse cx="{1420+i*86:.0f}" cy="330" rx="40" ry="30"'
                        f' fill="#f0cfae" {o(5)}/>'
                f'<path d="M{1392+i*86:.0f},316 q28,-14 56,0" fill="none"'
                f' stroke="#e0bb98" stroke-width="7"/>')
    s += SL(Z_SRED, f'<path d="M1360,352 q140,-40 280,0 l0,40 q-140,34 -280,0 Z"'
                    f' fill="#8a4a52" {o(5)}/>')
    # ЛАВКА с храпящим дедом
    s += SL(Z_SRED, _lavka_krupno(120, pol - 6, 620, t, 150, False))
    ded = figura(300, pol - 150, 330, t, col="#5a5248", kant="#ffd98a",
                 boroda=True, ph=.6, naklon=-4.0, lico=True)
    s += SL(Z_SRED, f'<g transform="rotate(78 300 {pol-150:.0f})">{ded}</g>')
    for i in range(3):
        k = ((t * .45 + i * .33) % 1.0)
        s += SL(Z_SRED, f'<path d="M{600+60*k:.0f},{pol-250-30*k:.0f}'
                        f' q{20:.0f},{-20:.0f} {44:.0f},{-6:.0f}" fill="none"'
                        f' stroke="#cfe4f5" stroke-width="7"'
                        f' opacity="{.6*(1-k):.2f}"/>')
    # ТУЛУПЫ на гвозде
    for i in range(3):
        tx = 760 + i * 150
        kach = 1.4 * A.w(t, 4.2, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} {tx:.0f} 250)">'
                        f'<circle cx="{tx:.0f}" cy="244" r="11" fill="{ZHELEZ}"/>'
                f'<path d="M{tx-80:.0f},300 q{80:.0f},{-56:.0f} {160:.0f},0'
                f' l{16:.0f},{330:.0f} q{-96:.0f},{34:.0f} {-192:.0f},0 Z"'
                f' fill="{["#5a4636", "#4a4e46", "#6a5a46"][i]}" {o(6)}/>'
                f'<ellipse cx="{tx:.0f}" cy="306" rx="60" ry="22"'
                f' fill="#cdbf9c" opacity=".8"/></g>')
    # ДВЕРЬ приоткрывается от локтя
    otkr = A.ease(A.seg(t, 2.6, 2.0))
    s += SL(Z_SRED, dver(60, pol - 820, 330, 820, .2 + .5 * otkr,
                         "url(#derev)", True, False))
    s += SL(Z_SRED, f'<rect x="30" y="{pol-852:.0f}" width="390" height="40"'
                    f' rx="10" fill="#5b4428" {o(6)}/>')
    # ДЕВУШКА крадётся на цыпочках: обе руки прижимают плошку
    shag = A.ease(A.seg(t, .2, 4.0))
    fx = 1020 - 480 * shag
    fy, fh = pol + 10, 740
    zam = max(.0, A.w(t, 3.2, .2))
    # дед лежит на лавке головой вправо: в реестр идёт точка его разворота
    _figury_kadra((300, pol - 150, 330), (fx, fy - 26 * zam, fh))
    dev = figura(fx, fy - 26 * zam, fh, t, col="#e8dcc8", kant="#ffd98a",
                 platok=True, ph=.3, naklon=7.0, profil=True)
    d1, (p1x, p1y), _ = _ruka_sgib_mimo(fx, fy - 26 * zam, fh, -1, fh * .20, 34,
                                        fh * .22, -10, t, "#e8dcc8",
                                        "#ffd98a", .3, 3.0)
    d2, (p2x, p2y), _ = _ruka_sgib_mimo(fx, fy - 26 * zam, fh, 1, fh * .20, 38,
                                        fh * .22, -6, t, "#e8dcc8",
                                        "#ffd98a", .7, 3.0)
    dev += d1 + d2
    s += SL(Z_SRED, dev)
    s += SL(Z_SRED, _ploshka_s_meloch((p1x + p2x) / 2, (p1y + p2y) / 2 + 24, t,
                                      1.05, 7, 257))
    s += SL(Z_SRED, "")
    # скрипнувшая половица под её ногой
    s += SL(Z_SRED, f'<path d="M{fx-120:.0f},{pol+30:.0f} L{fx+140:.0f},{pol+30:.0f}'
                    f' L{fx+170:.0f},{pol+80:.0f} L{fx-150:.0f},{pol+80:.0f} Z"'
                    f' fill="#5e4a34" {o(5)}/>')
    s += SL(Z_SRED, luchina(760, pol - 6, t, 1.2, .2))
    # сени холодные: кадушка с водой, вёдра, лопата и корзины у стены
    s += SL(Z_SRED, _kadushki_i_grabli(1060, pol - 4, t, 419))
    for i in range(3):
        s += SL(Z_SRED, krynka(150 + i * 120, 232, 1.35 + (i % 2) * .2))
    # низ кадра
    s += SL(Z_SRED, _valenki_u_dveri(300, pol + 76, 1.05, t)
            + _dvorovaya_utvar(1180, pol + 90, 380, t, 263, ["kadka", "vedro"])
            + _kot_zhivoy(640, pol + 70, t, 1.1, "#2f2a26", .6, True, True)
            + _yaschiki(1620, pol + 84, t, 269, 2, .84)
            + kartoshka(900, pol + 96, t, 6, 6, .9))
    s += SL(Z_PERED, _stolb_pered(1870, 76, "#140f0c", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 1560, 790, 7, 37, 240, .34))
    s += vinetka(.44)
    return s


def zhenihi_idut_na_blesk(t):
    """Дорога перед калиткой сплошь усыпана блестящей мелочью. По ней один за
    другим шагают три жениха — с гармонью, с пряником в платке и долговязый
    с букетом рябины. Девушка выглядывает из-за калитки и считает."""
    rnd = random.Random(331)
    gor = 620
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, False, 83)
    s += oblaka(t, 150, 5, 89, .44, "#e4e8f0", 15.0)
    s += SL(Z_DAL, _derevnya_ryad(gor - 60, t, 37, ((230, 320), (640, 260),
                                                    (1560, 300))))
    s += SL(Z_DAL, goloe_derevo(1080, gor - 10, 520, t, 97, 9, "#3a3b43", True))
    s += SL(Z_DAL, _zabor_dosok(620, gor - 190, 1300, 200, 53, 58))
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#5a4a36"/>'
            + _zemlya_faktura(gor + 40, 1050, 29, 16, "#473a2c")
            + _koleya(gor + 250, 337, 2)
            + _pol_shvy(gor + 40, 1070, 347, 6, "#3e3226")
            + _listya(349, 40, gor + 50, 1060))
    # ДОРОГА, УСЫПАННАЯ МЕЛОЧЬЮ: монетки блестят по всей полосе
    for i in range(54):
        mx = rnd.uniform(60, W - 60)
        my = rnd.uniform(gor + 120, 1060)
        rr = 13 + (my - gor - 120) * .022
        bl = .4 + .6 * abs(A.w(t, 1.6 + (i % 5) * .3, i * .11))
        s += SL(Z_SRED, f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{rr:.0f}"'
                        f' ry="{rr*.48:.0f}" fill="url(#med)" {o(3)}/>'
                f'<ellipse cx="{mx-rr*.26:.0f}" cy="{my-rr*.12:.0f}"'
                f' rx="{rr*.38:.0f}" ry="{rr*.17:.0f}" fill="#fff0c4"'
                f' opacity="{bl:.2f}"/>')
    # КАЛИТКА — крупный предмет; за ней девушка
    s += SL(Z_SRED, _vorota_dvora(90, gor + 250, 420, 420, t, .12))
    s += SL(Z_SRED, _zabor_dosok(-30, gor + 60, 560, 210, 59, 56))
    dvh = 560
    dev = figura(230, gor + 300, dvh, t, col="#6a4a62", kant="#ffd98a",
                 platok=True, ph=.3, naklon=-5.0)
    # 16.11: было -8/-6 (обе горизонтально, поза распятия) — вниз-наружу на 28°/34°
    d1, (v1x, v1y), _ = _ruka_mimo(230, gor + 300, dvh, 1, dvh * .24, 28, t,
                              "#6a4a62", "#ffd98a", .3, 4.0)
    d2, (v2x, v2y), _ = _ruka_mimo(230, gor + 300, dvh, -1, dvh * .24, 34, t,
                              "#6a4a62", "#ffd98a", .7, 4.0)
    dev += d1 + d2
    s += SL(Z_SRED, dev)
    s += SL(Z_SRED, _varezhka(v1x, v1y, dvh, t, .3))
    # ТРИ ЖЕНИХА вереницей: рост через одного, шаг рваный, заходят друг за друга
    shag = A.seg(t, .2, 3.6)
    # рост СТРОГО через одного: 760 / 440 / 700 — разница 1,7× и 1,6×;
    # шаг рваный (0.0 / 0.52 / 0.16), средний со спины, третий в профиль
    zhen = ((0, 760, "#4a5a72", 0.0, "garmon", 4.0, False),
            (1, 440, "#5a4636", 0.52, "pryanik", -9.0, False),
            (2, 700, "#46506a", 0.16, "ryabina", 12.0, True))
    _figury_kadra((230, gor + 300, 560),
                  *[(760 + j * 430 - 120 * shag * (1 - o_ * .55),
                     gor + 330 + j * 46, h_) for j, h_, _c, o_, _p, _n, _pr in zhen])
    for i, fh, col, ot, pred, nak, prof in zhen:
        fx = 760 + i * 430 - 120 * shag * (1 - ot * .55)
        fy = gor + 330 + i * 46
        fig = figura(fx, fy, fh, t, col=col, kant="#cfe4f5", shapka=(i != 2),
                     ph=.2 + i * .33, profil=prof, naklon=nak,
                     lico=(i != 1))        # средний — СО СПИНЫ
        r1, (w1x, w1y), _ = _ruka_mimo(fx, fy, fh, 1, fh * .40,
                                  (24, 30, -46)[i], t, col, "#cfe4f5",
                                  .2 + i * .2, 6.0)
        r2, (w2x, w2y), _ = _ruka_mimo(fx, fy, fh, -1, fh * .36,
                                  (46, 34, 30)[i], t, col, "#cfe4f5",
                                  .6 + i * .2, 5.0)
        fig += r1 + r2
        s += SL(Z_SRED, fig)
        if pred == "garmon":
            rast = 30 * abs(A.w(t, 1.3, .2))
            s += SL(Z_SRED, f'<rect x="{w1x-10:.0f}" y="{w1y-20:.0f}" width="54"'
                            f' height="110" rx="10" fill="#8a3a32" {o(5)}/>'
                    f'<rect x="{w1x+44+rast:.0f}" y="{w1y-20:.0f}" width="54"'
                    f' height="110" rx="10" fill="#8a3a32" {o(5)}/>')
            for k in range(6):
                s += SL(Z_SRED, f'<path d="M{w1x+44:.0f},{w1y-14+k*18:.0f}'
                                f' l{14+rast*.5:.0f},{-6:.0f} l{14+rast*.5:.0f},{6:.0f}"'
                                f' fill="none" stroke="#efe2c2" stroke-width="5"/>')
            for k in range(4):
                s += SL(Z_SRED, f'<circle cx="{w1x+16:.0f}"'
                                f' cy="{w1y+4+k*24:.0f}" r="7"'
                                f' fill="#efe2c2" {o(2)}/>')
        elif pred == "pryanik":
            s += SL(Z_SRED, f'<path d="M{w1x-80:.0f},{w1y+10:.0f}'
                            f' q{80:.0f},{-54:.0f} {160:.0f},0'
                            f' q{-80:.0f},{40:.0f} {-160:.0f},0 Z" fill="{RUSH}"'
                            f' {o(5)}/>'
                    f'<ellipse cx="{w1x:.0f}" cy="{w1y-6:.0f}" rx="56" ry="34"'
                    f' fill="url(#med)" {o(5)}/>'
                    f'<path d="M{w1x-30:.0f},{w1y-14:.0f} q30,-16 60,2"'
                    f' fill="none" stroke="#efe2c2" stroke-width="6"/>'
                    f'<path d="M{w1x-70:.0f},{w1y+16:.0f} l-26,40 M{w1x+70:.0f},'
                    f'{w1y+16:.0f} l26,40" stroke="{TKAN}" stroke-width="9"'
                    f' fill="none"/>')
        else:
            s += SL(Z_SRED, grozd_ryabiny(w2x + 20, w2y + 40, t, 1.2, 15, 101, .3)
                    + f'<line x1="{w2x+16:.0f}" y1="{w2y+10:.0f}"'
                      f' x2="{w2x+24:.0f}" y2="{w2y+80:.0f}" stroke="{ZEL}"'
                      f' stroke-width="9"/>')
            # приглаживает чуб правой рукой
            s += SL(Z_SRED, f'<path d="M{w1x-10:.0f},{w1y-16:.0f}'
                            f' q{26:.0f},{-26:.0f} {58:.0f},{-10:.0f}" fill="none"'
                            f' stroke="#4a3526" stroke-width="14"/>')
        # варежка — только на той руке, где предмет: у первых двух это
        # правая (гармонь, пряник), у долговязого левая (букет рябины),
        # а чуб он приглаживает рукавом без кисти
        if i != 2:
            s += SL(Z_SRED, _varezhka(w1x, w1y, fh, t, .2 + i * .2, "#dcd0bc"))
        else:
            s += SL(Z_SRED, _varezhka(w2x, w2y, fh, t, .6 + i * .2, "#dcd0bc"))
        s += SL(Z_SRED, para_izo_rta(fx + fh * .10, fy - fh * .80, t,
                                     i * .3, 1.0, .42))
    # низ кадра
    s += SL(Z_SRED, _kucha_listev(620, 1060, 320, 353, 88)
            + _luzha(1500, 1020, 180, t, .4)
            + _kot_zhivoy(140, 1050, t, 1.0, "#3b342f", .2)
            + _sledy(1880, 1066, 1240, 880, 6, 359, "#33281d", 1.2)
            + _dvorovaya_utvar(1680, gor + 280, 240, t, 367, ["korzina"]))
    s += SL(Z_PERED, _stolb_pered(-10, 100, "#1a120c", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 5, .4, .75))
    s += vinetka(.38)
    return s


def blyudce_s_melochyu_u_zerkala(t):
    """Прихожая шестидесятых: подзеркальник у круглого зеркала, фарфоровое
    блюдце с мелочью на пол-кадра, расчёска, ключи, коробок спичек. Рука до
    локтя раскладывает монеты в три кучки, над ними встают значки."""
    rnd = random.Random(337)
    s = f'<rect width="{W}" height="{H}" fill="#2a262a"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="1080" height="820" fill="#8a7a62"/>')
    for i in range(11):
        s += SL(Z_DAL, f'<rect x="{i*100:.0f}" y="0" width="52" height="820"'
                       f' fill="#9a8a70" opacity=".55"/>')
    s += SL(Z_DAL, f'<rect x="1080" y="0" width="840" height="820"'
                   f' fill="#7e6f58"/>')
    s += SL(Z_DAL, _ramki_na_stene(1140, 120, 700, t, 373, 4))
    s += SL(Z_DAL, _veshalka_s_paltom(60, 150, 820, t, 409))
    # полка с обувью под вешалкой и две шляпные коробки сверху
    s += SL(Z_DAL, f'<rect x="80" y="640" width="780" height="26" rx="8"'
                   f' fill="url(#dosk)" {o(5)}/>')
    for i in range(5):
        bx = 150 + i * 150
        s += SL(Z_DAL, f'<path d="M{bx-70:.0f},640 q{24:.0f},{-80:.0f}'
                       f' {74:.0f},{-74:.0f} q{54:.0f},{12:.0f} {58:.0f},{74:.0f} Z"'
                       f' fill="{["#3a2e26", "#5a3a2c", "#2e3540"][i % 3]}" {o(5)}/>'
                f'<rect x="{bx-74:.0f}" y="628" width="140" height="16" rx="6"'
                f' fill="#1d1812" {o(3)}/>')
    for i in (0, 1):
        s += SL(Z_DAL, f'<ellipse cx="{300+i*220:.0f}" cy="96" rx="96" ry="34"'
                       f' fill="#c9b79c" {o(5)}/>'
                f'<rect x="{204+i*220:.0f}" y="96" width="192" height="76" rx="12"'
                f' fill="#b8a68c" {o(5)}/>'
                f'<path d="M{216+i*220:.0f},130 h168" stroke="#9a8a68"'
                f' stroke-width="6"/>')
    s += SL(Z_DAL, tusklaya_lampochka(540, 120, t, 1.2, True))
    s += SL(Z_DAL, _konus_sveta(540, 170, 360, 480, 0, .38))
    # ПОДЗЕРКАЛЬНИК и круглое зеркало — крупный предмет
    s += SL(Z_SRED, f'{ten(760, 946, 420, 26, .5)}'
                    f'<rect x="300" y="700" width="1100" height="48" rx="12"'
                    f' fill="url(#derev)" {o(7)}/>'
            + f'<rect x="330" y="748" width="1040" height="30" rx="8"'
              f' fill="#5b4428" {o(5)}/>')
    for i in (0, 1):
        s += SL(Z_SRED, f'<rect x="{400+i*880:.0f}" y="778" width="46"'
                        f' height="170" rx="14" fill="#4a3522" {o(5)}/>'
                f'<ellipse cx="{423+i*880:.0f}" cy="860" rx="34" ry="20"'
                f' fill="#5e442a" {o(3)}/>')
    s += SL(Z_SRED, f'<rect x="520" y="778" width="660" height="150" rx="10"'
                    f' fill="url(#dosk)" {o(5)}/>'
            + f'<line x1="520" y1="850" x2="1180" y2="850" stroke="#3a2a1a"'
              f' stroke-width="8" opacity=".7"/>'
            + f'<circle cx="700" cy="818" r="16" fill="url(#zhel)" {o(3)}/>'
            + f'<circle cx="1000" cy="818" r="16" fill="url(#zhel)" {o(3)}/>')
    # круглое зеркало с отражением руки
    s += SL(Z_SRED, f'<circle cx="860" cy="400" r="280" fill="#6a5030" {o(8)}/>'
            + f'<circle cx="860" cy="400" r="246" fill="#4a5a66" opacity=".95"'
              f' {o(4)}/>'
            + f'<path d="M700,560 L900,230 L960,230 L760,560 Z" fill="#9fc0d4"'
              f' opacity="{.16+.1*abs(A.w(t,3.2)):.2f}"/>')
    # отражение руки в зеркале
    otr, (orx, ory) = rukav(1120, 620, 300, -140, t, "#6a4a52", "#eaf4ff", .4,
                            3.0, True)
    s += SL(Z_SRED, f'<g opacity=".55" clip-path="none">{otr}'
                    f'<ellipse cx="{orx:.0f}" cy="{ory:.0f}" rx="42" ry="32"'
                    f' fill="#d8c8b0" {o(4)}/></g>')
    # БЛЮДЦЕ С МЕЛОЧЬЮ на пол-кадра
    # БЛЮДЦЕ 260 px, а не 500: при rx=250 оно занимало четверть кадра и
    # наезжало на раму зеркала (осмотр порции 2)
    s += SL(Z_SRED, f'<ellipse cx="700" cy="692" rx="130" ry="44"'
                    f' fill="#f2ece0" {o(6)}/>'
            + f'<ellipse cx="700" cy="684" rx="110" ry="34" fill="#e4dfd0" {o(4)}/>'
            + f'<ellipse cx="700" cy="678" rx="88" ry="25" fill="#f6f2e8"'
              f' opacity=".9"/>'
            + f'<path d="M570,692 q130,40 260,0" fill="none" stroke="url(#zol)"'
              f' stroke-width="7"/>')
    ost = 1 - A.ease(A.seg(t, .4, 3.2))
    for i in range(9):
        a = math.radians(i * 40)
        rr = 62 * ost
        s += SL(Z_SRED, f'<ellipse cx="{700+rr*math.cos(a):.0f}"'
                        f' cy="{672+rr*.3*math.sin(a):.0f}" rx="22" ry="10"'
                        f' fill="url(#med)" {o(3)}/>'
                f'<ellipse cx="{694+rr*math.cos(a):.0f}"'
                f' cy="{668+rr*.3*math.sin(a):.0f}" rx="8" ry="4"'
                f' fill="#fff0c4" opacity="{.4+.5*abs(A.w(t,2.0,i*.2)):.2f}"/>')
    # ТРИ КУЧКИ монет и значки над ними
    znaki = ("buhanka", "tramvay", "korobok")
    for i, zn in enumerate(znaki):
        k = A.ease(A.seg(t, .8 + i * .8, .7))
        cx = 1020 + i * 190
        # КУЧКА, А НЕ ДВЕ МОНЕТЫ: семь монет горкой, с гуртом и бликом
        for m in range(7):
            s += SL(Z_SRED, f'<ellipse cx="{cx+rnd.uniform(-24, 24):.0f}"'
                            f' cy="{702-m*13*k:.0f}" rx="44" ry="19"'
                            f' fill="url(#med)" opacity="{k:.2f}" {o(3)}/>'
                    f'<ellipse cx="{cx-8+rnd.uniform(-18, 18):.0f}"'
                    f' cy="{698-m*13*k:.0f}" rx="12" ry="5" fill="#fff0c4"'
                    f' opacity="{k*(.35+.5*abs(A.w(t,2.2,m*.2))):.2f}"/>')
        if k > .3:
            zy = 480 - 60 * k
            if zn == "buhanka":
                s += SL(Z_SRED, f'<path d="M{cx-66:.0f},{zy:.0f}'
                                f' q{66:.0f},{-60:.0f} {132:.0f},0 Z"'
                                f' fill="url(#med)" opacity="{k:.2f}" {o(5)}/>'
                        f'<path d="M{cx-40:.0f},{zy-24:.0f} l14,-20 M{cx:.0f},'
                        f'{zy-34:.0f} l14,-20" stroke="#8a5a22" stroke-width="6"'
                        f' fill="none" opacity="{k:.2f}"/>')
            elif zn == "tramvay":
                s += SL(Z_SRED, f'<rect x="{cx-70:.0f}" y="{zy-70:.0f}"'
                                f' width="140" height="76" rx="12" fill="#8a4a3c"'
                                f' opacity="{k:.2f}" {o(5)}/>'
                        f'<rect x="{cx-56:.0f}" y="{zy-58:.0f}" width="42"'
                        f' height="34" rx="5" fill="#cfe0ea" opacity="{k:.2f}"/>'
                        f'<rect x="{cx+8:.0f}" y="{zy-58:.0f}" width="42"'
                        f' height="34" rx="5" fill="#cfe0ea" opacity="{k:.2f}"/>'
                        f'<path d="M{cx:.0f},{zy-70:.0f} l0,-40 l40,-16"'
                        f' fill="none" stroke="{ZHELEZ}" stroke-width="6"'
                        f' opacity="{k:.2f}"/>'
                        f'<circle cx="{cx-40:.0f}" cy="{zy+4:.0f}" r="13"'
                        f' fill="{CHUGUN}" opacity="{k:.2f}"/>'
                        f'<circle cx="{cx+40:.0f}" cy="{zy+4:.0f}" r="13"'
                        f' fill="{CHUGUN}" opacity="{k:.2f}"/>')
            else:
                s += SL(Z_SRED, f'<rect x="{cx-58:.0f}" y="{zy-54:.0f}"'
                                f' width="116" height="68" rx="8" fill="#c9b79c"'
                                f' opacity="{k:.2f}" {o(5)}/>'
                        f'<rect x="{cx-46:.0f}" y="{zy-42:.0f}" width="92"'
                        f' height="44" rx="5" fill="#8a4a3c" opacity="{k:.2f}"/>'
                        f'<path d="M{cx-30:.0f},{zy-20:.0f} h60" stroke="#efe2c2"'
                        f' stroke-width="6" opacity="{k:.2f}"/>')
    # РУКА ДО ЛОКТЯ — ничья, с варежкой на конце
    ruk, (ex, ey) = rukav(1880, 1050, 760, -148, t, "#6a4a52", "#ffd98a", .2,
                          3.0, True)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, f'<rect x="{ex+40:.0f}" y="{ey+10:.0f}" width="170" height="46"'
                    f' rx="18" fill="#6a4a52" {o(5)}/>')
    s += SL(Z_SRED, _varezhka(ex, ey, 900, t, .2))
    # расчёска, ключи, коробок спичек на подзеркальнике
    s += SL(Z_SRED, f'<rect x="1240" y="664" width="190" height="36" rx="10"'
                    f' fill="#3f4650" {o(5)}/>')
    for i in range(14):
        s += SL(Z_SRED, f'<line x1="{1252+i*13:.0f}" y1="664" x2="{1252+i*13:.0f}"'
                        f' y2="634" stroke="#3f4650" stroke-width="6"/>')
    s += SL(Z_SRED, _svyazka_klyuchey(1520, 640, t, 1.15, .3, 3))
    s += SL(Z_SRED, _zont_v_podstavke(1840, 980, t, 1.1))
    s += SL(Z_SRED, _sumka_hozyaystvennaya(1700, 976, t, .92, 1.0))
    s += SL(Z_SRED, f'<rect x="200" y="840" width="230" height="160" rx="12"'
                    f' fill="#5a3a2c" {o(6)}/>'
            + f'<rect x="216" y="860" width="198" height="42" rx="8"'
              f' fill="#6a4a38" {o(4)}/>'
            + f'<path d="M270,840 q46,-56 92,0" fill="none" stroke="#4a2e22"'
              f' stroke-width="13"/>'
            + f'<rect x="286" y="910" width="60" height="22" rx="8"'
              f' fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, f'<line x1="1460" y1="990" x2="1488" y2="770" stroke="#5b4428"'
                    f' stroke-width="15" stroke-linecap="round"/>'
            + f'<path d="M1488,770 q30,-32 46,2" fill="none" stroke="#3a2a1a"'
              f' stroke-width="15"/>')
    s += SL(Z_SRED, f'<path d="M1296,700 q46,-40 92,0 q-10,66 -46,74'
                    f' q-36,-8 -46,-74 Z" fill="#dbeaf4" opacity=".9" {o(5)}/>'
            + f'<ellipse cx="1342" cy="640" rx="46" ry="15" fill="#cfe0ea" {o(3)}/>')
    # галошница под подзеркальником: три полки обуви парами
    for p_ in range(2):
        py_ = 834 + p_ * 56
        s += SL(Z_SRED, f'<rect x="540" y="{py_:.0f}" width="620" height="20"'
                        f' rx="7" fill="#5b4428" {o(4)}/>')
        for i in range(4):
            bx = 600 + i * 150
            s += SL(Z_SRED, f'<path d="M{bx-64:.0f},{py_:.0f} q{22:.0f},{-56:.0f}'
                            f' {66:.0f},{-54:.0f} q{48:.0f},{10:.0f} {52:.0f},{54:.0f} Z"'
                            f' fill="{["#3a2e26", "#5a3a2c", "#2e3540", "#6a4a3c"][i]}"'
                            f' {o(4)}/>'
                    f'<rect x="{bx-68:.0f}" y="{py_-12:.0f}" width="128"'
                    f' height="14" rx="5" fill="#1d1812" {o(3)}/>')
    # телефон с диском и записная книжка рядом с блюдцем
    s += SL(Z_SRED, f'<path d="M1060,700 L1250,700 L1232,614 L1078,614 Z"'
                    f' fill="#3f4650" {o(6)}/>'
            + f'<circle cx="1155" cy="658" r="42" fill="#5a6168" {o(4)}/>'
            + f'<circle cx="1155" cy="658" r="18" fill="#2b3038" {o(3)}/>'
            + f'<rect x="1066" y="586" width="180" height="40" rx="18"'
              f' fill="#2b3038" {o(5)}/>'
            + f'<ellipse cx="1080" cy="606" rx="30" ry="22" fill="#3f4650" {o(3)}/>'
            + f'<ellipse cx="1232" cy="606" rx="30" ry="22" fill="#3f4650" {o(3)}/>')
    for i in range(8):
        a = math.radians(i * 45 + 12)
        s += SL(Z_SRED, f'<circle cx="{1155+32*math.cos(a):.0f}"'
                        f' cy="{658+32*math.sin(a):.0f}" r="7" fill="#eaf0f4"'
                        f' opacity=".85"/>')
    s += SL(Z_SRED, f'<rect x="1300" y="700" width="150" height="46" rx="7"'
                    f' fill="#7a3a42" {o(5)}/>'
            + f'<rect x="1310" y="710" width="130" height="30" rx="4"'
              f' fill="#f2ece0" opacity=".9"/>')
    s += SL(Z_SRED, f'<rect x="1660" y="650" width="130" height="50" rx="8"'
                    f' fill="#8a4a3c" {o(5)}/>'
            + f'<rect x="1672" y="662" width="106" height="28" rx="4"'
              f' fill="#efe2c2" opacity=".9"/>'
            + f'<path d="M1690,676 h70" stroke="#8a5a22" stroke-width="5"/>')
    # низ кадра
    s += SL(Z_PERED, _polovik(520, 982, 820, 98, "#8a5a52", "#c9a05a")
            + _valenki_u_dveri(300, 1050, 1.0, t)
            + _gorodskoy_hlam(1560, 1060, 360, t, 379, ["korobka", "yaschik"])
            + _kot_zhivoy(1180, 1046, t, 1.1, "#423b35", .5))
    s += SL(Z_PERED, _stolb_pered(-8, 92, "#181310", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 540, 170, 5, 41, 150, .22))
    s += vinetka(.38)
    return s


# ── ПОМОЩНИКИ ЧЕТВЁРТОЙ ПАРТИИ ─────────────────────────────────────────────

def _terka(x, y, t, s_=1.0, ug=-8.0):
    """Тёрка: жестяное полотно рядами пробитых зубцов, деревянная ручка,
    загнутый борт и блик по кромке."""
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'{ten(x, y + 10 * s_, 54 * s_, 11 * s_, .4)}'
         f'<rect x="{x-56*s_:.0f}" y="{y-250*s_:.0f}" width="{112*s_:.0f}"'
         f' height="{250*s_:.0f}" rx="{10*s_:.0f}" fill="#b6bcc2" {o(5)}/>'
         f'<rect x="{x-56*s_:.0f}" y="{y-250*s_:.0f}" width="{112*s_:.0f}"'
         f' height="{16*s_:.0f}" fill="#8b9299" opacity=".85"/>')
    for r in range(8):
        for c in range(4):
            zx = x - 40 * s_ + c * 27 * s_
            zy = y - 230 * s_ + r * 26 * s_
            s += (f'<path d="M{zx:.0f},{zy:.0f} l{9*s_:.0f},{-11*s_:.0f}'
                  f' l{9*s_:.0f},{11*s_:.0f} Z" fill="#e4e9ec" opacity=".9"/>')
    s += (f'<rect x="{x-30*s_:.0f}" y="{y-20*s_:.0f}" width="{60*s_:.0f}"'
          f' height="{76*s_:.0f}" rx="{14*s_:.0f}" fill="url(#derev)" {o(5)}/>'
          f'<line x1="{x-46*s_:.0f}" y1="{y-240*s_:.0f}" x2="{x-46*s_:.0f}"'
          f' y2="{y-40*s_:.0f}" stroke="#eaf4ff" stroke-width="{7*s_:.0f}"'
          f' opacity="{.3+.25*abs(A.w(t,2.6)):.2f}"/></g>')
    return s


def _butyl_masla(x, y, s_=1.0, t=0.0, naklon=.0, lej=.0):
    """Бутыль с маслом: тёмное стекло, масло до плеча, пробка, бумажный
    хомутик. lej 0..1 — наклоняется и льёт струйку."""
    ug = -naklon * 62
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'{ten(x, y + 6 * s_, 44 * s_, 10 * s_, .4)}'
         f'<path d="M{x-44*s_:.0f},{y:.0f} L{x+44*s_:.0f},{y:.0f}'
         f' L{x+44*s_:.0f},{y-140*s_:.0f} q{-10*s_:.0f},{-40*s_:.0f}'
         f' {-30*s_:.0f},{-54*s_:.0f} L{x+14*s_:.0f},{y-248*s_:.0f}'
         f' L{x-14*s_:.0f},{y-248*s_:.0f} L{x-14*s_:.0f},{y-194*s_:.0f}'
         f' q{-20*s_:.0f},{14*s_:.0f} {-30*s_:.0f},{54*s_:.0f} Z"'
         f' fill="#7a6a3c" opacity=".9" {o(5)}/>'
         f'<path d="M{x-40*s_:.0f},{y-6*s_:.0f} L{x+40*s_:.0f},{y-6*s_:.0f}'
         f' L{x+40*s_:.0f},{y-120*s_:.0f} q{-40*s_:.0f},{10*s_:.0f}'
         f' {-80*s_:.0f},0 Z" fill="#d8a53c" opacity=".92"/>'
         f'<rect x="{x-18*s_:.0f}" y="{y-266*s_:.0f}" width="{36*s_:.0f}"'
         f' height="{22*s_:.0f}" rx="6" fill="#8a6a3c" {o(4)}/>'
         f'<rect x="{x-30*s_:.0f}" y="{y-176*s_:.0f}" width="{60*s_:.0f}"'
         f' height="{40*s_:.0f}" rx="5" fill="#f2ead6" {o(3)}/>'
         f'<line x1="{x-30*s_:.0f}" y1="{y-110*s_:.0f}" x2="{x-30*s_:.0f}"'
         f' y2="{y-30*s_:.0f}" stroke="#fff0c8" stroke-width="{7*s_:.0f}"'
         f' opacity=".45"/></g>')
    if lej > 0:
        s += (f'<path d="M{x+36*s_:.0f},{y-230*s_:.0f}'
              f' q{30*s_:.0f},{80*s_*lej:.0f} {20*s_:.0f},{190*s_*lej:.0f}"'
              f' fill="none" stroke="#e8b84c" stroke-width="{11*s_:.0f}"'
              f' stroke-linecap="round" opacity=".92"/>')
    return s


def _kadushka_kapusty(x, y, t, s_=1.0):
    """Кадушка с квашеной капустой: клёпки, два обруча, деревянный круг с
    гнётом-камнем, рассол и выбившийся капустный лист."""
    h2, w2 = 190 * s_, 180 * s_
    return (f'{ten(x, y + 8 * s_, w2 * .52, 14 * s_, .45)}'
            f'<path d="M{x-w2/2:.0f},{y-h2:.0f} L{x+w2/2:.0f},{y-h2:.0f}'
            f' L{x+w2*.40:.0f},{y:.0f} L{x-w2*.40:.0f},{y:.0f} Z"'
            f' fill="url(#derev)" {o(6)}/>'
            f'<rect x="{x-w2/2-5:.0f}" y="{y-h2*.86:.0f}" width="{w2+10:.0f}"'
            f' height="{16*s_:.0f}" rx="6" fill="{ZHELEZ}" {o(3)}/>'
            f'<rect x="{x-w2*.44:.0f}" y="{y-h2*.26:.0f}" width="{w2*.88:.0f}"'
            f' height="{16*s_:.0f}" rx="6" fill="{ZHELEZ}" {o(3)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y-h2:.0f}" rx="{w2/2:.0f}"'
            f' ry="{w2*.15:.0f}" fill="#3e3228" {o(4)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y-h2+8*s_:.0f}" rx="{w2*.42:.0f}"'
            f' ry="{w2*.12:.0f}" fill="#cdbf9c" opacity=".9"/>'
            f'<ellipse cx="{x+w2*.10:.0f}" cy="{y-h2-16*s_:.0f}"'
            f' rx="{w2*.20:.0f}" ry="{w2*.16:.0f}" fill="#6a6256" {o(4)}/>'
            f'<path d="M{x-w2*.34:.0f},{y-h2-4*s_:.0f}'
            f' q{w2*.16:.0f},{-30*s_:.0f} {w2*.34:.0f},{-8*s_:.0f}'
            f' q{-w2*.12:.0f},{22*s_:.0f} {-w2*.34:.0f},{8*s_:.0f} Z"'
            f' fill="#cfd8a8" {o(3)}/>')


def _pugalo(x, y, t, s_=1.0):
    """Пугало: крестовина из жердей, мешковина рубахой, ведро вместо головы,
    солома из рукавов и тряпица, которая хлопает на ветру."""
    kach = 2.6 * A.w(t, 3.2, .2)
    s = (f'<g transform="rotate({kach:.1f} {x:.0f} {y:.0f})">'
         f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+6*s_:.0f}" y2="{y-420*s_:.0f}"'
         f' stroke="url(#derev)" stroke-width="{20*s_:.0f}"/>'
         f'<line x1="{x-150*s_:.0f}" y1="{y-300*s_:.0f}" x2="{x+156*s_:.0f}"'
         f' y2="{y-310*s_:.0f}" stroke="url(#derev)" stroke-width="{16*s_:.0f}"/>'
         f'<path d="M{x-120*s_:.0f},{y-300*s_:.0f} L{x+126*s_:.0f},{y-306*s_:.0f}'
         f' L{x+90*s_:.0f},{y-110*s_:.0f} L{x-84*s_:.0f},{y-104*s_:.0f} Z"'
         f' fill="#b9a883" {o(6)}/>')
    for i in range(5):
        s += (f'<path d="M{x-110*s_+i*54*s_:.0f},{y-110*s_:.0f}'
              f' q{8*s_:.0f},{40*s_:.0f} {-6*s_:.0f},{70*s_:.0f}" fill="none"'
              f' stroke="#c9a05a" stroke-width="{7*s_:.0f}"/>')
    for sgn in (-1, 1):
        for i in range(4):
            a = math.radians(-20 + i * 18) * sgn
            s += (f'<line x1="{x+sgn*140*s_:.0f}" y1="{y-302*s_:.0f}"'
                  f' x2="{x+sgn*140*s_+sgn*60*s_*math.cos(a):.0f}"'
                  f' y2="{y-302*s_+60*s_*math.sin(a):.0f}" stroke="#c9a05a"'
                  f' stroke-width="{6*s_:.0f}"/>')
    s += (f'<path d="M{x-54*s_:.0f},{y-316*s_:.0f} L{x+60*s_:.0f},{y-320*s_:.0f}'
          f' L{x+48*s_:.0f},{y-424*s_:.0f} L{x-42*s_:.0f},{y-420*s_:.0f} Z"'
          f' fill="#6a7278" {o(6)}/>'
          f'<ellipse cx="{x+4*s_:.0f}" cy="{y-424*s_:.0f}" rx="{52*s_:.0f}"'
          f' ry="{15*s_:.0f}" fill="#49535b" {o(4)}/>'
          f'<path d="M{x+60*s_:.0f},{y-290*s_:.0f}'
          f' q{40*s_+14*s_*A.w(t, 1.1, .3):.0f},{30*s_:.0f} {30*s_:.0f},{76*s_:.0f}'
          f' l{-30*s_:.0f},{-10*s_:.0f} q{16*s_:.0f},{-34*s_:.0f}'
          f' {-14*s_:.0f},{-62*s_:.0f} Z" fill="{TKAN}" {o(3)}/></g>')
    return s


def _vorona(x, y, t, s_=1.0, ph=.0, letit=.0):
    """Ворона: чёрное тело с сизым отливом, крупный клюв, лапы с когтями.
    letit 0..1 — слетает, крылья раскрываются."""
    kr = 40 * s_ * letit + 7 * s_ * A.w(t, 1.1, ph)
    pod = -180 * s_ * letit
    s = (f'<g transform="translate({120 * s_ * letit:.1f},{pod:.1f})">'
         f'<ellipse cx="{x:.0f}" cy="{y-40*s_:.0f}" rx="{54*s_:.0f}"'
         f' ry="{32*s_:.0f}" fill="#23262c" {o(4)}/>'
         f'<path d="M{x-50*s_:.0f},{y-48*s_:.0f} q{36*s_:.0f},{-24*s_-kr:.0f}'
         f' {80*s_:.0f},{-4*s_:.0f} q{-32*s_:.0f},{28*s_+kr*.4:.0f}'
         f' {-80*s_:.0f},{4*s_:.0f} Z" fill="#33373f" {o(3)}/>'
         f'<path d="M{x-54*s_:.0f},{y-34*s_:.0f} l{-40*s_:.0f},{10*s_:.0f}'
         f' l{36*s_:.0f},{14*s_:.0f} Z" fill="#2a2e35" {o(3)}/>'
         f'<circle cx="{x+40*s_:.0f}" cy="{y-70*s_:.0f}" r="{21*s_:.0f}"'
         f' fill="#23262c" {o(3)}/>'
         f'<path d="M{x+58*s_:.0f},{y-70*s_:.0f} l{34*s_:.0f},{7*s_:.0f}'
         f' l{-32*s_:.0f},{10*s_:.0f} Z" fill="#5e676e" {o(2)}/>'
         f'<circle cx="{x+44*s_:.0f}" cy="{y-76*s_:.0f}" r="{4.4*s_:.0f}"'
         f' fill="#e4e9ec"/>'
         f'<circle cx="{x+45*s_:.0f}" cy="{y-76*s_:.0f}" r="{2.2*s_:.0f}"'
         f' fill="{K}"/>')
    if letit < .5:
        for dx in (-10, 12):
            s += (f'<line x1="{x+dx*s_:.0f}" y1="{y-12*s_:.0f}"'
                  f' x2="{x+dx*s_-4*s_:.0f}" y2="{y:.0f}" stroke="#5e676e"'
                  f' stroke-width="{5*s_:.0f}"/>')
    return s + "</g>"


def _gryadka_redki(x, y, w_, t, seed=5, n=6, vyrvana=-1, vyh=.0):
    """Грядка редьки: земляной гребень, из него торчат чёрные макушки с
    ботвой. vyrvana — номер редьки, которая выскакивает (vyh 0..1)."""
    rnd = random.Random(seed)
    s = (f'<path d="M{x:.0f},{y:.0f} q{w_*.25:.0f},{-54:.0f} {w_*.5:.0f},{-20:.0f}'
         f' q{w_*.25:.0f},{34:.0f} {w_*.5:.0f},{-14:.0f} L{x+w_:.0f},{y+120:.0f}'
         f' L{x:.0f},{y+120:.0f} Z" fill="#4a3c2c" {o(5)}/>')
    for i in range(16):
        s += (f'<ellipse cx="{x+rnd.uniform(20, w_-20):.0f}"'
              f' cy="{y+rnd.uniform(10, 100):.0f}" rx="{rnd.uniform(26, 56):.0f}"'
              f' ry="{rnd.uniform(9, 17):.0f}" fill="#3b3024" opacity=".8"/>')
    for i in range(n):
        gx = x + (i + .5) * w_ / n + rnd.uniform(-16, 16)
        gy = y - 10 + rnd.uniform(-14, 14)
        if i == vyrvana:
            gy -= 320 * vyh
        s += _redka(gx, gy, .62 + (i % 3) * .07, t, rnd.uniform(-12, 12),
                    .3 + (.7 if i == vyrvana else .0) * vyh)
    return s


def _kladovaya_polka(x, y, w_, t, seed=7):
    """Полка зимней кладовой: толстая доска на кронштейнах, связки лука,
    банка мёда с деревянной лопаткой, мешочек сушёной малины с завязкой и
    градусник в деревянном футляре."""
    rnd = random.Random(seed)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="34" rx="10"'
         f' fill="url(#dosk)" {o(6)}/>'
         f'<rect x="{x:.0f}" y="{y+34:.0f}" width="{w_:.0f}" height="18" rx="7"'
         f' fill="#5b4428" {o(4)}/>')
    for k in (x + 90, x + w_ * .5, x + w_ - 120):
        s += (f'<path d="M{k:.0f},{y+52:.0f} l34,56 l-38,0 Z" fill="{ZHELEZ}" {o(4)}/>')
    # связки лука под полкой
    for i in range(3):
        lx = x + 150 + i * 160
        kach = 2.2 * A.w(t, 3.4, i * .3)
        s += (f'<g transform="rotate({kach:.1f} {lx:.0f} {y+52:.0f})">')
        for k in range(5):
            s += (f'<ellipse cx="{lx-34+k*17:.0f}" cy="{y+120+(k%2)*26:.0f}"'
                  f' rx="26" ry="32" fill="#c9a05a" {o(4)}/>'
                  f'<line x1="{lx-34+k*17:.0f}" y1="{y+88+(k%2)*26:.0f}"'
                  f' x2="{lx-28+k*17:.0f}" y2="{y+54:.0f}" stroke="#8a7a46"'
                  f' stroke-width="6"/>')
        s += "</g>"
    # банка мёда с лопаткой
    bx = x + w_ - 300
    s += (f'<rect x="{bx:.0f}" y="{y-150:.0f}" width="150" height="150" rx="12"'
          f' fill="url(#stekl)" opacity=".92" {o(5)}/>'
          f'<rect x="{bx+8:.0f}" y="{y-104:.0f}" width="134" height="104" rx="8"'
          f' fill="#d8a53c"/>'
          f'<rect x="{bx-6:.0f}" y="{y-168:.0f}" width="162" height="24" rx="9"'
          f' fill="{ZHELEZ}" {o(4)}/>'
          f'<line x1="{bx+112:.0f}" y1="{y-160:.0f}" x2="{bx+128:.0f}"'
          f' y2="{y-250:.0f}" stroke="url(#derev)" stroke-width="15"/>'
          f'<ellipse cx="{bx+130:.0f}" cy="{y-262:.0f}" rx="24" ry="16"'
          f' fill="url(#derev)" {o(4)}/>')
    # мешочек сушёной малины
    mx = x + 140
    s += (f'<path d="M{mx-60:.0f},{y-8:.0f} q{-16:.0f},{-104:.0f} {28:.0f},{-130:.0f}'
          f' q{34:.0f},{-12:.0f} {64:.0f},{8:.0f} q{34:.0f},{34:.0f}'
          f' {24:.0f},{122:.0f} Z" fill="#cdbf9c" {o(6)}/>'
          f'<path d="M{mx-28:.0f},{y-134:.0f} q{30:.0f},{-18:.0f} {58:.0f},{4:.0f}"'
          f' fill="none" stroke="{TKAN}" stroke-width="10"/>')
    for i in range(5):
        s += (f'<circle cx="{mx-30+i*22:.0f}" cy="{y-78+(i%2)*20:.0f}" r="13"'
              f' fill="#9c2f3c" opacity=".9" {o(2)}/>')
    # градусник в футляре
    gx = x + 420
    s += (f'<rect x="{gx:.0f}" y="{y-190:.0f}" width="54" height="190" rx="10"'
          f' fill="url(#derev)" {o(5)}/>'
          f'<rect x="{gx+16:.0f}" y="{y-174:.0f}" width="22" height="160" rx="8"'
          f' fill="#efe8da" {o(3)}/>'
          f'<rect x="{gx+22:.0f}" y="{y-94:.0f}" width="10" height="76" rx="5"'
          f' fill="#b8352c"/>')
    for i in range(7):
        s += (f'<line x1="{gx+16:.0f}" y1="{y-166+i*22:.0f}" x2="{gx+28:.0f}"'
              f' y2="{y-166+i*22:.0f}" stroke="#8a8274" stroke-width="3"/>')
    return s


def _romashka(x, y, t, s_=1.0, lep=8, oborvan=.0, ug=0.0):
    """Ромашка: жёлтая сердцевина с точками, белые лепестки веером, стебель
    с резными листьями. oborvan 0..1 — последний лепесток отрывается."""
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x:.0f},{y:.0f} q{-16*s_:.0f},{120*s_:.0f} {4*s_:.0f},{250*s_:.0f}"'
         f' fill="none" stroke="#5c8a40" stroke-width="{11*s_:.0f}"/>')
    for i in (0, 1):
        yy = y + 110 * s_ + i * 70 * s_
        sgn = 1 if i % 2 == 0 else -1
        s += (f'<path d="M{x-8*s_+i*4*s_:.0f},{yy:.0f}'
              f' q{sgn*44*s_:.0f},{-26*s_:.0f} {sgn*76*s_:.0f},{10*s_:.0f}'
              f' q{-sgn*40*s_:.0f},{22*s_:.0f} {-sgn*76*s_:.0f},{-10*s_:.0f} Z"'
              f' fill="#4e7a3c" {o(3)}/>')
    for i in range(lep):
        a = math.radians(i * 360.0 / lep + 8 * A.w(t, 3.2, .2))
        dl = 74 * s_
        ex, ey = x + dl * math.cos(a), y + dl * math.sin(a)
        op = 1.0
        if i == lep - 1:
            ex += 90 * s_ * oborvan
            ey -= 40 * s_ * oborvan
            op = 1 - oborvan * .5
        s += (f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{36*s_:.0f}"'
              f' ry="{17*s_:.0f}" transform="rotate({math.degrees(a):.0f}'
              f' {ex:.0f} {ey:.0f})" fill="#f8f6ee" opacity="{op:.2f}"'
              f' stroke="{K}" stroke-width="{max(2, 4 * s_):.1f}"/>')
    s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{34*s_:.0f}" fill="#e8b84c"'
          f' {o(4)}/>')
    rnd = random.Random(int(x))
    for i in range(9):
        a = rnd.uniform(0, 6.28)
        rr = rnd.uniform(0, 26) * s_
        s += (f'<circle cx="{x+rr*math.cos(a):.0f}" cy="{y+rr*math.sin(a):.0f}"'
              f' r="{3.4*s_:.0f}" fill="#b5803a" opacity=".85"/>')
    return s + "</g>"


def _troyka(x, y, t, s_=1.0, k=.0):
    """Тройка с бубенцами: дуга с колокольцем, три коня в упряжке (ноги в
    беге), розвальни, ямщик на облучке. k 0..1 — проезд мимо окна."""
    nog = lambda f: 26 * s_ * math.sin(t * 9 + f)
    s = f'<g transform="translate({x:.0f},{y:.0f})">'
    # КОНИ ВРОЗЬ: при шаге 150 px тулова по 208 px слипались в кучу
    for i, (dx, sc, col) in enumerate(((-280, .88, "#6a4a32"),
                                       (0, 1.0, "#3e3630"),
                                       (280, .94, "#7d5a3c"))):
        hx = dx * s_
        s += (f'<ellipse cx="{hx:.0f}" cy="{-150*sc*s_:.0f}" rx="{104*sc*s_:.0f}"'
              f' ry="{56*sc*s_:.0f}" fill="{col}" {o(5)}/>'
              # шея: от тулова к голове, короткая и толстая
              f'<path d="M{hx+74*sc*s_:.0f},{-180*sc*s_:.0f}'
              f' q{40*sc*s_:.0f},{-20*sc*s_:.0f} {52*sc*s_:.0f},{-58*sc*s_:.0f}'
              f' l{44*sc*s_:.0f},{16*sc*s_:.0f}'
              f' q{-16*sc*s_:.0f},{56*sc*s_:.0f} {-56*sc*s_:.0f},{70*sc*s_:.0f} Z"'
              f' fill="{col}" {o(5)}/>'
              # ГОЛОВА КРУПНАЯ И БЛИЖЕ (была 74×52 с выносом 138 — читалась
              # котом): 110×68 при выносе 85
              f'<ellipse cx="{hx+128*sc*s_:.0f}" cy="{-256*sc*s_:.0f}"'
              f' rx="{55*sc*s_:.0f}" ry="{34*sc*s_:.0f}" fill="{col}" {o(5)}/>'
              f'<path d="M{hx+160*sc*s_:.0f},{-236*sc*s_:.0f}'
              f' q{30*sc*s_:.0f},{6*sc*s_:.0f} {34*sc*s_:.0f},{26*sc*s_:.0f}'
              f' q{-26*sc*s_:.0f},{10*sc*s_:.0f} {-44*sc*s_:.0f},{-6*sc*s_:.0f} Z"'
              f' fill="#2e2620" {o(3)}/>'
              f'<circle cx="{hx+150*sc*s_:.0f}" cy="{-268*sc*s_:.0f}"'
              f' r="{7*s_:.0f}" fill="{K}"/>'
              f'<circle cx="{hx+152*sc*s_:.0f}" cy="{-270*sc*s_:.0f}"'
              f' r="{2.6*s_:.0f}" fill="#eaf4ff"/>'
              # уши парой
              f'<path d="M{hx+112*sc*s_:.0f},{-286*sc*s_:.0f} l{-4*s_:.0f},{-30*s_:.0f}'
              f' l{22*s_:.0f},{18*s_:.0f} Z" fill="{col}" {o(2)}/>'
              f'<path d="M{hx+142*sc*s_:.0f},{-288*sc*s_:.0f} l{6*s_:.0f},{-28*s_:.0f}'
              f' l{18*s_:.0f},{22*s_:.0f} Z" fill="{col}" {o(2)}/>')
        # ГРИВА прядями по шее и хвост метёлкой
        for j in range(6):
            s += (f'<path d="M{hx+86*sc*s_+j*12*sc*s_:.0f},{-212*sc*s_-j*8*sc*s_:.0f}'
                  f' q{-18*sc*s_:.0f},{22*sc*s_:.0f} {-26*sc*s_:.0f},{48*sc*s_:.0f}"'
                  f' fill="none" stroke="#2e2620" stroke-width="{7*sc*s_:.0f}"'
                  f' opacity=".8"/>')
        s += (f'<path d="M{hx-104*sc*s_:.0f},{-186*sc*s_:.0f}'
              f' q{-50*sc*s_:.0f},{50*sc*s_:.0f} {-30*sc*s_:.0f},{124*sc*s_:.0f}"'
              f' fill="none" stroke="#2e2620" stroke-width="{16*sc*s_:.0f}"'
              f' stroke-linecap="round"/>')
        for j, fz in enumerate((0, 1.6, 3.1, 4.6)):
            lx = hx - 70 * sc * s_ + j * 48 * sc * s_
            s += (f'<line x1="{lx:.0f}" y1="{-120*sc*s_:.0f}"'
                  f' x2="{lx+nog(fz):.0f}" y2="{-6*s_:.0f}" stroke="{col}"'
                  f' stroke-width="{19*sc*s_:.0f}" stroke-linecap="round"/>'
                  # КОПЫТО: без него нога читалась палкой
                  f'<rect x="{lx+nog(fz)-11*sc*s_:.0f}" y="{-20*s_:.0f}"'
                  f' width="{22*sc*s_:.0f}" height="{20*s_:.0f}" rx="{5*s_:.0f}"'
                  f' fill="#1d1812" {o(2)}/>')
        s += (f'<path d="M{hx-104*sc*s_:.0f},{-200*sc*s_:.0f}'
              f' q{-40*sc*s_:.0f},{40*sc*s_:.0f} {-16*sc*s_:.0f},{100*sc*s_:.0f}"'
              f' fill="none" stroke="#2e2620" stroke-width="{9*s_:.0f}"/>')
    # дуга с бубенцами
    s += (f'<path d="M{-90*s_:.0f},{-230*s_:.0f} q{90*s_:.0f},{-150*s_:.0f}'
          f' {180*s_:.0f},0" fill="none" stroke="#b8352c"'
          f' stroke-width="{20*s_:.0f}"/>')
    for i in range(3):
        bx = -50 * s_ + i * 50 * s_
        s += (f'<circle cx="{bx:.0f}" cy="{-320*s_+10*s_*math.sin(t*8+i):.0f}"'
              f' r="{15*s_:.0f}" fill="url(#zhel)" {o(3)}/>'
              f'<circle cx="{bx:.0f}" cy="{-316*s_:.0f}" r="{5*s_:.0f}"'
              f' fill="#7a4d1c"/>')
    # розвальни и ямщик
    s += (f'<path d="M{-430*s_:.0f},{-30*s_:.0f} L{-130*s_:.0f},{-30*s_:.0f}'
          f' q{40*s_:.0f},{-4*s_:.0f} {46*s_:.0f},{-44*s_:.0f}" fill="none"'
          f' stroke="#5b4428" stroke-width="{15*s_:.0f}" stroke-linecap="round"/>'
          f'<rect x="{-420*s_:.0f}" y="{-140*s_:.0f}" width="{300*s_:.0f}"'
          f' height="{110*s_:.0f}" rx="{14*s_:.0f}" fill="url(#derev)" {o(6)}/>')
    for i in range(6):
        s += (f'<line x1="{-400*s_+i*54*s_:.0f}" y1="{-140*s_:.0f}"'
              f' x2="{-400*s_+i*54*s_:.0f}" y2="{-30*s_:.0f}" stroke="#6a5030"'
              f' stroke-width="{8*s_:.0f}"/>')
    return s + "</g>"


def _zayac(x, y, t, s_=1.0, k=.0):
    """Заяц перебегает дорогу: серо-белое тело, длинные уши прижаты, прыжок
    дугой. k 0..1 — доля перебега."""
    sk = abs(math.sin(k * math.pi * 3)) * 70 * s_
    xx = x + (1920 - x) * k * .5
    return (f'<g transform="translate({xx-x:.0f},{-sk:.1f})">'
            f'{ten(x, y + 6 * s_, 44 * s_, 10 * s_, .35)}'
            f'<ellipse cx="{x:.0f}" cy="{y-40*s_:.0f}" rx="{58*s_:.0f}"'
            f' ry="{34*s_:.0f}" fill="#cdc6bb" {o(4)}/>'
            f'<ellipse cx="{x+52*s_:.0f}" cy="{y-66*s_:.0f}" rx="{28*s_:.0f}"'
            f' ry="{22*s_:.0f}" fill="#d8d2c8" {o(3)}/>'
            f'<path d="M{x+46*s_:.0f},{y-84*s_:.0f} q{30*s_:.0f},{-54*s_:.0f}'
            f' {52*s_:.0f},{-44*s_:.0f} q{-14*s_:.0f},{40*s_:.0f}'
            f' {-38*s_:.0f},{54*s_:.0f} Z" fill="#cdc6bb" {o(3)}/>'
            f'<path d="M{x+34*s_:.0f},{y-86*s_:.0f} q{18*s_:.0f},{-56*s_:.0f}'
            f' {36*s_:.0f},{-52*s_:.0f} q{-6*s_:.0f},{42*s_:.0f}'
            f' {-26*s_:.0f},{56*s_:.0f} Z" fill="#b9b2a8" {o(3)}/>'
            f'<circle cx="{x+62*s_:.0f}" cy="{y-70*s_:.0f}" r="{5*s_:.0f}"'
            f' fill="{K}"/>'
            f'<ellipse cx="{x-54*s_:.0f}" cy="{y-48*s_:.0f}" rx="{16*s_:.0f}"'
            f' ry="{13*s_:.0f}" fill="#f2efe8" {o(2)}/>'
            f'<line x1="{x-20*s_:.0f}" y1="{y-16*s_:.0f}" x2="{x-34*s_:.0f}"'
            f' y2="{y:.0f}" stroke="#b9b2a8" stroke-width="{10*s_:.0f}"/>'
            f'<line x1="{x+22*s_:.0f}" y1="{y-16*s_:.0f}" x2="{x+34*s_:.0f}"'
            f' y2="{y:.0f}" stroke="#b9b2a8" stroke-width="{10*s_:.0f}"/></g>')


def _gitara_na_stene(x, y, t, s_=1.0):
    """Гитара на стене: корпус восьмёркой, розетка, гриф с ладами, шесть
    струн и лента-подвес."""
    s = (f'<path d="M{x:.0f},{y:.0f} q{-78*s_:.0f},{10*s_:.0f} {-80*s_:.0f},{96*s_:.0f}'
         f' q{-2*s_:.0f},{86*s_:.0f} {80*s_:.0f},{92*s_:.0f}'
         f' q{82*s_:.0f},{-6*s_:.0f} {80*s_:.0f},{-92*s_:.0f}'
         f' q{-2*s_:.0f},{-86*s_:.0f} {-80*s_:.0f},{-96*s_:.0f} Z"'
         f' fill="url(#med)" {o(6)}/>'
         f'<path d="M{x-62*s_:.0f},{y+76*s_:.0f} q{62*s_:.0f},{-34*s_:.0f}'
         f' {124*s_:.0f},0" fill="none" stroke="#8a5a22" stroke-width="{7*s_:.0f}"/>'
         f'<circle cx="{x:.0f}" cy="{y+118*s_:.0f}" r="{34*s_:.0f}" fill="#2e2620"'
         f' {o(4)}/>'
         f'<circle cx="{x:.0f}" cy="{y+118*s_:.0f}" r="{42*s_:.0f}" fill="none"'
         f' stroke="#8a5a22" stroke-width="{6*s_:.0f}"/>'
         f'<rect x="{x-20*s_:.0f}" y="{y-180*s_:.0f}" width="{40*s_:.0f}"'
         f' height="{190*s_:.0f}" rx="{8*s_:.0f}" fill="#5b4428" {o(5)}/>'
         f'<rect x="{x-26*s_:.0f}" y="{y-216*s_:.0f}" width="{52*s_:.0f}"'
         f' height="{44*s_:.0f}" rx="{8*s_:.0f}" fill="#4a3522" {o(4)}/>')
    for i in range(6):
        s += (f'<line x1="{x-18*s_:.0f}" y1="{y-150*s_+i*26*s_:.0f}"'
              f' x2="{x+18*s_:.0f}" y2="{y-150*s_+i*26*s_:.0f}" stroke="#cdbf9c"'
              f' stroke-width="{4*s_:.0f}" opacity=".8"/>')
    for i in range(6):
        s += (f'<line x1="{x-15*s_+i*6*s_:.0f}" y1="{y-196*s_:.0f}"'
              f' x2="{x-15*s_+i*6*s_:.0f}" y2="{y+172*s_:.0f}" stroke="#efe8da"'
              f' stroke-width="{2.4*s_:.0f}" opacity=".9"/>')
    s += (f'<path d="M{x-10*s_:.0f},{y-212*s_:.0f} q{-70*s_:.0f},{-50*s_:.0f}'
          f' {-110*s_:.0f},{-6*s_:.0f}" fill="none" stroke="{TKAN}"'
          f' stroke-width="{10*s_:.0f}"/>')
    return s


def _kovrik_s_olenyami(x, y, w_, h_, t):
    """Коврик с оленями над кроватью: бордовое поле, кайма зигзагом, два
    оленя с рогами у ёлочки — рисованный ковёр шестидесятых."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="8"'
         f' fill="#7a2f33" {o(6)}/>'
         f'<rect x="{x+24:.0f}" y="{y+24:.0f}" width="{w_-48:.0f}"'
         f' height="{h_-48:.0f}" rx="6" fill="none" stroke="#c9a05a"'
         f' stroke-width="9"/>')
    for i in range(int((w_ - 60) / 40)):
        s += (f'<path d="M{x+34+i*40:.0f},{y+h_-34:.0f} l20,-22 l20,22"'
              f' fill="none" stroke="#d8b070" stroke-width="6" opacity=".85"/>')
    for sgn, ox_ in ((-1, x + w_ * .32), (1, x + w_ * .68)):
        s += (f'<g transform="translate({ox_:.0f},{y+h_*.58:.0f}) scale({sgn},1)">'
              f'<ellipse cx="0" cy="0" rx="74" ry="40" fill="#c9a05a" {o(4)}/>'
              f'<path d="M50,-26 q40,-16 46,-70" fill="none" stroke="#c9a05a"'
              f' stroke-width="15"/>'
              f'<ellipse cx="100" cy="-104" rx="28" ry="20" fill="#c9a05a" {o(3)}/>'
              f'<path d="M86,-124 q-12,-54 -46,-70 M112,-124 q14,-56 50,-66"'
              f' fill="none" stroke="#d8b070" stroke-width="8"/>'
              f'<path d="M60,-134 l-16,-30 M130,-130 l20,-28" fill="none"'
              f' stroke="#d8b070" stroke-width="6"/>')
        for dx in (-50, -14, 22, 54):
            s += (f'<line x1="{dx}" y1="30" x2="{dx - 8}" y2="104"'
                  f' stroke="#c9a05a" stroke-width="11"/>')
        s += "</g>"
    s += (f'<path d="M{x+w_*.5:.0f},{y+h_*.26:.0f} l-54,96 l108,0 Z"'
          f' fill="#4e7a3c" {o(4)}/>'
          f'<path d="M{x+w_*.5:.0f},{y+h_*.40:.0f} l-70,110 l140,0 Z"'
          f' fill="#3f6a34" {o(4)}/>')
    return s


# ── ДЕКОРАЦИИ, ЧЕТВЁРТАЯ ПАРТИЯ ────────────────────────────────────────────

def gorstka_protiv_buhanki(t):
    """Стол в избе: чашечные весы на пол-кадра, крынка, нож, полотенце.
    Девушка кладёт на левую чашу горстку монет, на правую — круглый каравай
    и крынку молока. Чаши встают ровно, кулак с монетами сжимается."""
    rnd = random.Random(401)
    pol = 980
    s = f'<rect width="{W}" height="{H}" fill="#2a241c"/>'
    s += SL(Z_DAL, brevna(0, 40, 1060, pol - 40, 96)
            + brevna(1060, 40, 860, pol - 40, 96))
    s += SL(Z_DAL, _polka_s_utvaryu(90, 240, 600, t, 421, 5))
    s += SL(Z_DAL, _polka_s_utvaryu(1180, 260, 620, t, 431, 5))
    # ЗА ВЕСАМИ НЕ ГОЛАЯ СТЕНА: полка с утварью ровно за чашами
    s += SL(Z_DAL, _polka_s_utvaryu(700, 330, 560, t, 193, 4))
    s += SL(Z_DAL, _polka_s_utvaryu(100, 540, 560, t, 433, 4))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#5e4a34"/>'
            + polovicy(pol + 16) + _pol_shvy(pol + 20, 1070, 439, 6, "#4a3824"))
    s += SL(Z_SRED, svecha(1700, pol - 420, t, .2, 1.7, 130))
    s += SL(Z_SRED, _konus_sveta(1700, pol - 540, 520, 360, 12, .40))
    # СТОЛ и ВЕСЫ — главный предмет
    s += SL(Z_SRED, stol(240, pol - 330, 1200, 40, True))
    sy = pol - 330
    rov = A.ease(A.seg(t, 1.6, 1.2))
    # ВЕСЫ ПРАВЕЕ: левая чаша с горсткой стояла прямо за головой девушки
    s += SL(Z_SRED, _vesy(1160, sy - 8, t, 1.2, -.5 * (1 - rov), (1 - rov) * .5, 300))
    # монеты на левую чашу, каравай и крынка — на правую
    mk = A.ease(A.seg(t, .3, .8))
    # ГОРСТКА МЕЛОЧИ — настоящая горка из двенадцати монет с гуртом и бликом
    for i in range(12):
        a = math.radians(i * 30 + 12)
        rr = 16 + (i % 3) * 22
        s += SL(Z_SRED, f'<ellipse cx="{1160-310+rr*math.cos(a):.0f}"'
                        f' cy="{sy-312+100-7*(i%4)*mk+rr*.34*math.sin(a):.0f}"'
                        f' rx="30" ry="14" fill="url(#med)" opacity="{mk:.2f}"'
                        f' {o(3)}/>'
                f'<ellipse cx="{1160-316+rr*math.cos(a):.0f}"'
                f' cy="{sy-316+100-7*(i%4)*mk+rr*.34*math.sin(a):.0f}" rx="11"'
                f' ry="5" fill="#fff0c4" opacity="{mk*(.4+.5*abs(A.w(t,2.0,i*.2))):.2f}"/>')
    # КАРАВАЙ и КРЫНКА на другой чаше — крупно, с рушником
    s += SL(Z_SRED, karavay(1160 + 310, sy - 312 + 86, 1.34, True))
    s += SL(Z_SRED, krynka(1160 + 420, sy - 312 + 100, 1.4))
    # крынка, нож, полотенце на столе
    s += SL(Z_SRED, krynka(400, sy - 8, 1.5)
            + f'<line x1="520" y1="{sy-16:.0f}" x2="690" y2="{sy-40:.0f}"'
              f' stroke="#cfd8dc" stroke-width="16" stroke-linecap="round"/>'
            + f'<rect x="490" y="{sy-30:.0f}" width="70" height="26" rx="10"'
              f' fill="url(#derev)" {o(4)}/>'
            + f'<path d="M1180,{sy-10:.0f} L1400,{sy-10:.0f} L1384,{sy+70:.0f}'
              f' L1196,{sy+70:.0f} Z" fill="url(#rush)" {o(5)}/>'
            + f'<rect x="1196" y="{sy+30:.0f}" width="188" height="14"'
              f' fill="{TKAN}" opacity=".8"/>')
    # девушка у стола
    fx, fy, fh = 540, pol + 20, 800
    kul = A.ease(A.seg(t, 3.0, 1.0))
    dev = figura(fx, fy, fh, t, col="#6a4a62", kant="#ffd98a", platok=True,
                 ph=.3, naklon=5 - 8 * kul)
    d1, (a1x, a1y), _ = _ruka(fx, fy, fh, 1, fh * .44, 22 + 18 * kul, t,
                              "#6a4a62", "#ffd98a", .3, 5.0)
    d2, (a2x, a2y), _ = _ruka(fx, fy, fh, 1, fh * .34, 48, t,
                              "#6a4a62", "#ffd98a", .7, 4.0)
    dev += d1 + d2
    s += SL(Z_SRED, dev)
    # кулак с монетами: монеты уходят в ладонь и варежка сжимается
    if kul > .2:
        for i in range(4):
            s += SL(Z_SRED, f'<ellipse cx="{a1x+(i-2)*8:.0f}" cy="{a1y-6:.0f}"'
                            f' rx="22" ry="10" fill="url(#med)"'
                            f' opacity="{kul:.2f}" {o(3)}/>')
    s += SL(Z_SRED, "")
    s += SL(Z_SRED, ten(fx, fy + 8, 170, 26, .45))
    # низ кадра
    s += SL(Z_SRED, _polovik(640, pol + 34, 640, 106)
            + _dvorovaya_utvar(96, pol + 92, 420, t, 443,
                               ["kadka", "korzina", "vedro"])
            + _yaschiki(1600, pol + 86, t, 449, 2, .88)
            + _kot_zhivoy(1380, pol + 70, t, 1.1, "#3b342f", .4)
            + kartoshka(430, pol + 96, t, 6, 6, .95))
    # лавка с крынками, вязанки лука и короба — обжитой средний план
    s += SL(Z_SRED, _lavka_krupno(1180, pol - 8, 600, t, 140, False))
    for i in range(4):
        s += SL(Z_SRED, krynka(1250 + i * 150, pol - 150, 1.3 + (i % 2) * .2))
    # вязанки лука подняты: висели ровно на лице девушки (осмотр)
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{760+i*86:.0f},70 q{-28:.0f},{70:.0f}'
                        f' {4:.0f},{128:.0f} q{32:.0f},{18:.0f} {46:.0f},{-12:.0f}'
                        f' q{14:.0f},{-64:.0f} {-18:.0f},{-116:.0f} Z"'
                        f' fill="#c9a05a" {o(5)}/>'
                f'<line x1="{768+i*86:.0f}" y1="70" x2="{784+i*86:.0f}"'
                f' y2="34" stroke="#8a7a46" stroke-width="7"/>')
    s += SL(Z_SRED, _kadushka_kapusty(1860, pol - 6, t, .9))
    # ряд мисок унесён вправо: две из четырёх висели на лице (осмотр)
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{1180+i*150:.0f},232 q{54:.0f},{44:.0f}'
                        f' {108:.0f},0 l{-12:.0f},{-54:.0f} l{-84:.0f},0 Z"'
                        f' fill="#e7edf0" {o(5)}/>'
                f'<ellipse cx="{1234+i*150:.0f}" cy="178" rx="54" ry="16"'
                f' fill="#cfd8dc" {o(3)}/>')
    s += SL(Z_SRED, teplo(1700, pol - 480, 480, 400, .40))
    s += SL(Z_PERED, _stolb_pered(-8, 96, "#181209", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 1700, pol - 500, 6, 53, 190, .3))
    s += vinetka(.40)
    return s


def okoshko_devushki(t):
    """Окошко избы изнутри на пол-кадра, наличник, на подоконнике свеча в
    плошке и клубок. За стеклом настоящая ночная зимняя дорога под луной.
    Девушка подпирает щёку локтем и протирает стекло рукавом."""
    rnd = random.Random(409)
    pol = 1000
    s = f'<rect width="{W}" height="{H}" fill="#161d2e"/>'
    s += SL(Z_DAL, brevna(0, 30, 1040, pol - 30, 96)
            + brevna(1040, 30, 880, pol - 30, 96))
    s += SL(Z_DAL, _polka_s_utvaryu(96, 250, 520, t, 457, 4))
    s += SL(Z_DAL, _polka_s_utvaryu(100, 560, 480, t, 659, 4))
    s += SL(Z_DAL, _knizhnaya_polka(1420, 640, 440, t, 661, 1, 180))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#4a3c2c"/>'
            + polovicy(pol + 16) + _pol_shvy(pol + 20, 1070, 461, 6, "#3a2c1e"))
    # ПОЛАТИ за спиной: спят домашние
    s += SL(Z_DAL, _polati(1240, 180, 660, t, 5))
    # ОКОШКО: сначала нарисованный вид, потом метка, потом наличник поверх
    px, py, pw, ph_ = 310, 300, 900, 480
    put = kontur_proema(px, py, pw, ph_, "pryam")
    # СТОКА ЗДЕСЬ НЕТ: в plany.json у плана 70 столбец «сток» = «убрано»
    # (в задании porciya2.md он ещё описан — расхождение, гейт свежее текста).
    # Поэтому за стеклом только наш рисованный вид: ночная зимняя дорога.
    s += SL(Z_SRED, _vid_za_proemom(put, t, "les", 11, px + pw * .5))
    s += SL(Z_SRED, f'<clipPath id="dor4"><path d="{put}"/></clipPath>'
            + f'<g clip-path="url(#dor4)">'
            + f'<path d="M{px+pw*.18:.0f},{py+ph_:.0f} L{px+pw*.44:.0f},'
              f'{py+ph_*.52:.0f} L{px+pw*.58:.0f},{py+ph_*.52:.0f}'
              f' L{px+pw*.86:.0f},{py+ph_:.0f} Z" fill="#dbe6f2" opacity=".92"/>'
            + f'<circle cx="{px+pw*.74:.0f}" cy="{py+ph_*.24:.0f}" r="52"'
              f' fill="#f2f6fa" opacity=".95"/>'
            + f'<circle cx="{px+pw*.74:.0f}" cy="{py+ph_*.24:.0f}" r="96"'
              f' fill="#cfe4f5" opacity=".24"/></g>')
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#6a5030"'
                    f' stroke-width="34"/>'
            + f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#6a5030" stroke-width="24"/>'
            + f'<line x1="{px:.0f}" y1="{py+ph_*.46:.0f}" x2="{px+pw:.0f}"'
              f' y2="{py+ph_*.46:.0f}" stroke="#6a5030" stroke-width="22"/>')
    # наличник с резьбой и подоконник
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{px-52+i*112:.0f},{py-54:.0f} l36,-48 l36,48 Z"'
                        f' fill="#7d5a3c" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{px-60:.0f}" y="{py-58:.0f}" width="{pw+120:.0f}"'
                    f' height="36" rx="10" fill="#8a6a44" {o(6)}/>'
            + f'<rect x="{px-74:.0f}" y="{py+ph_-10:.0f}" width="{pw+148:.0f}"'
              f' height="50" rx="12" fill="url(#dosk)" {o(7)}/>')
    # свеча в плошке и клубок на подоконнике — не в самом проёме, а на борту
    s += SL(Z_SRED, f'<ellipse cx="{px+90:.0f}" cy="{py+ph_+40:.0f}" rx="58"'
                    f' ry="20" fill="url(#glina)" {o(5)}/>')
    s += SL(Z_SRED, svecha(px + 90, py + ph_ - 70, t, .1, 1.45, 110))
    s += SL(Z_SRED, f'<circle cx="{px+pw-80:.0f}" cy="{py+ph_+10:.0f}" r="48"'
                    f' fill="#8a4a52" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{px+pw-124:.0f},{py+ph_-14+i*16:.0f}'
                        f' q{44:.0f},{-16:.0f} {86:.0f},{6:.0f}" fill="none"'
                        f' stroke="#a35a62" stroke-width="5" opacity=".85"/>')
    # ДЕВУШКА на лавке боком к окну
    s += SL(Z_SRED, _lavka_krupno(560, pol - 6, 620, t, 150, False))
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{150+i*130:.0f},288 q{50:.0f},{40:.0f}'
                        f' {100:.0f},0 l{-10:.0f},{-50:.0f} l{-80:.0f},0 Z"'
                        f' fill="url(#glina)" {o(5)}/>'
                f'<ellipse cx="{200+i*130:.0f}" cy="238" rx="50" ry="15"'
                f' fill="#8a5a30" {o(3)}/>')
    s += SL(Z_SRED, _sapogi_novye(1420, pol + 4, 1.0, t, .4))
    fx, fy, fh = 840, pol - 150, 620
    prot = A.w(t, 1.6, .2)
    dev = figura(fx, fy, fh, t, col="#e4dcc8", kant="#ffd98a", platok=True,
                 ph=.3, profil=True, naklon=-7.0)
    d1, (s1x, s1y), _ = _ruka_so_sgibom(fx, fy, fh, -1, fh * .22, 30,
                                        fh * .24, -46, t, "#e4dcc8",
                                        "#ffd98a", .3, 3.0)
    d2, (s2x, s2y), _ = _ruka(fx, fy, fh, -1, fh * .46, -24 + 10 * prot, t,
                              "#e4dcc8", "#ffd98a", .7, 5.0)
    dev += d1 + d2
    s += SL(Z_SRED, dev)
    # рукав протирает стекло: светлый след по стеклу
    s += SL(Z_SRED, f'<path d="M{s2x-30:.0f},{s2y-40:.0f}'
                    f' q{60:.0f},{-50+20*prot:.0f} {130:.0f},{-20:.0f}"'
                    f' fill="none" stroke="#eaf4ff" stroke-width="26"'
                    f' opacity=".30" stroke-linecap="round"/>')
    s += SL(Z_SRED, _varezhka(s1x, s1y, fh, t, .3) + _varezhka(s2x, s2y, fh, t, .7))
    # крынки и короба на лавке, вязанки травы у наличника
    for i in range(4):
        s += SL(Z_SRED, krynka(620 + i * 130, pol - 160, 1.25 + (i % 2) * .2))
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{1300+i*80:.0f},240 q{-26:.0f},{78:.0f}'
                        f' {4:.0f},{146:.0f} q{30:.0f},{18:.0f} {44:.0f},{-14:.0f}'
                        f' q{14:.0f},{-72:.0f} {-18:.0f},{-132:.0f} Z"'
                        f' fill="#8a9a58" {o(5)}/>'
                f'<line x1="{1308+i*80:.0f}" y1="240" x2="{1324+i*80:.0f}"'
                f' y2="204" stroke="#6f7a44" stroke-width="7"/>')
    s += SL(Z_SRED, teplo(px + 90, py + ph_ - 110, 460, 380, .42))
    # низ кадра
    s += SL(Z_SRED, _valenki_u_dveri(400, pol + 70, 1.05, t)
            + _dvorovaya_utvar(1180, pol + 90, 420, t, 463,
                               ["kadka", "korzina", "vedro"])
            + _kot_zhivoy(700, pol + 66, t, 1.15, "#2f2a26", .5, True, True)
            + _yaschiki(96, pol + 84, t, 467, 2, .82))
    s += SL(Z_PERED, _stolb_pered(1874, 76, "#140f0c", 0, H))
    s += SL(Z_LETIT, iskra_let(t, px + 90, py + ph_ - 150, 6, 59, 170, .3))
    s += vinetka(.42)
    return s


def troyka_pod_oknom(t):
    """То же окошко снаружи, в нём силуэт девушки с ладонями на стекле. Мимо
    летит тройка с бубенцами: ямщик на облучке, в санях трое гуляк. Потом
    дорога пустеет, и только заяц перебегает её."""
    rnd = random.Random(419)
    gor = 700
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 97)
    s += oblaka(t, 150, 4, 101, .3, "#9fb0c4", 18.0)
    s += SL(Z_DAL, f'<circle cx="1560" cy="200" r="86" fill="#f2f6fa"'
                   f' opacity=".92"/>'
            + f'<circle cx="1560" cy="200" r="150" fill="#cfe4f5" opacity=".22"/>')
    s += SL(Z_DAL, _derevnya_ryad(gor - 90, t, 61, ((1480, 300), (1820, 260))))
    s += SL(Z_DAL, goloe_derevo(1180, gor - 30, 540, t, 103, 9, "#2a2b33", True))
    # СТЕНА ИЗБЫ С ОКОШКОМ — крупный предмет
    s += SL(Z_DAL, brevna(60, 120, 1040, gor - 120, 94))
    s += SL(Z_DAL, f'<path d="M20,140 L580,-10 L1140,140 Z" fill="#3a2e24" {o(7)}/>'
            + f'<rect x="20" y="120" width="1120" height="44" rx="10"'
              f' fill="#4a3a28" {o(6)}/>')
    ox, oy, ow, oh = 330, 260, 520, 360
    s += SL(Z_SRED, f'<rect x="{ox-40:.0f}" y="{oy-40:.0f}" width="{ow+80:.0f}"'
                    f' height="{oh+80:.0f}" rx="10" fill="#6a5030" {o(7)}/>'
            + f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
              f' fill="#2b3550"/>'
            + f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{ow:.0f}" height="{oh:.0f}"'
              f' fill="#ffd98a" opacity=".30"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{ox-46+i*126:.0f},{oy-46:.0f} l40,-46 l40,46 Z"'
                        f' fill="#7d5a3c" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="{ox-64:.0f}" y="{oy+oh-6:.0f}" width="{ow+128:.0f}"'
                    f' height="44" rx="10" fill="url(#dosk)" {o(6)}/>'
            + f'<line x1="{ox+ow*.5:.0f}" y1="{oy:.0f}" x2="{ox+ow*.5:.0f}"'
              f' y2="{oy+oh:.0f}" stroke="#6a5030" stroke-width="20"/>'
            + f'<line x1="{ox:.0f}" y1="{oy+oh*.48:.0f}" x2="{ox+ow:.0f}"'
              f' y2="{oy+oh*.48:.0f}" stroke="#6a5030" stroke-width="18"/>')
    # ДЕВУШКА в окне: обе ладони прижаты к стеклу, потом опускает
    opu = A.ease(A.seg(t, 2.8, 1.0))
    dvh = 420
    dev = figura(ox + ow * .5, oy + oh - 10, dvh, t, col="#3a3448",
                 kant="#ffd98a", platok=True, ph=.4, naklon=-3.0)
    v1, (g1x, g1y), _ = _ruka_mimo(ox + ow * .5, oy + oh - 10, dvh, 1, dvh * .34,
                              -36 + 70 * opu, t, "#3a3448", "#ffd98a", .4, 3.0)
    v2, (g2x, g2y), _ = _ruka_mimo(ox + ow * .5, oy + oh - 10, dvh, -1, dvh * .34,
                              -34 + 68 * opu, t, "#3a3448", "#ffd98a", .8, 3.0)
    dev += v1 + v2
    s += SL(Z_SRED, dev)
    s += SL(Z_SRED, "")
    s += SL(Z_SRED, teplo(ox + ow * .5, oy + oh * .5, 460, 360, .40))
    # ДОРОГА и снег
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#c2cedc"/>'
            + f'<path d="M-20,{gor+80:.0f} Q480,{gor+30:.0f} 980,{gor+96:.0f}'
              f' Q1480,{gor+160:.0f} 1940,{gor+106:.0f} L1940,1080 L-20,1080 Z"'
              f' fill="url(#sneg)" {o(0)}/>'
            + _koleya(gor + 230, 467, 2)
            + _inej(479, 58, gor + 60, 1060)
            + _pol_shvy(gor + 60, 1070, 487, 5, "#9fb0c0"))
    # ТРОЙКА летит мимо окна, потом дорога пустеет
    pr = A.seg(t, .2, 2.6)
    if pr < 1.0:
        tx = -520 + 2600 * pr
        s += SL(Z_SRED, _troyka(tx, gor + 300, t, .92, pr))
        # ямщик на облучке и трое гуляк в санях
        yh = 330
        _figury_kadra((ox + ow * .5, oy + oh - 10, 420),
                      (tx - 160, gor + 268, 330), (tx - 330, gor + 236, 310),
                      (tx - 470, gor + 250, 190), (tx - 600, gor + 240, 290))
        yam = figura(tx - 160, gor + 268, yh, t, col="#4a4e46",
                     kant="#cfe4f5", shapka=True, ph=.2, profil=True,
                     naklon=6.0)
        y1, (q1x, q1y), _ = _ruka_mimo(tx - 160, gor + 268, yh, 1, yh * .40, -14, t,
                                  "#4a4e46", "#cfe4f5", .2, 6.0)
        y2, (q2x, q2y), _ = _ruka_mimo(tx - 160, gor + 268, yh, 1, yh * .32, 4, t,
                                  "#4a4e46", "#cfe4f5", .6, 6.0)
        yam += y1 + y2
        yam += (f'<path d="M{q1x:.0f},{q1y:.0f} Q{q1x+180:.0f},{q1y-40:.0f}'
                f' {q1x+330:.0f},{q1y-120:.0f}" fill="none" stroke="#2e2620"'
                f' stroke-width="7"/>')
        yam += ""
        yam += ""
        s += SL(Z_SRED, yam)
        # трое гуляк: рост через одного, один машет шапкой, двое обнялись
        # трое гуляк: рост через одного 310 / 190 / 290, шаг рваный,
        # один в профиль, один со спины
        for i, (dx, fh2, nak, prof, dy_) in enumerate(((-330, 310, -9, False, -4),
                                                       (-470, 190, 13, True, 10),
                                                       (-600, 290, -6, False, 0))):
            gx = tx + dx
            gul = figura(gx, gor + 240 + dy_, fh2, t,
                         col=("#5a4636", "#46506a", "#6a5a46")[i],
                         kant="#cfe4f5", shapka=(i != 1), boroda=(i == 2),
                         ph=.2 + i * .3, profil=prof, naklon=nak,
                         lico=(i != 2))
            # НАРУЖНЫЕ РУКИ ТОЛЬКО У ТОГО, КТО МАШЕТ ШАПКОЙ, и его рука
            # идёт ВВЕРХ, от соседей. У двоих поющих — свои рукава фигуры:
            # объятие читается перекрытием и наклоном, а не рукой сквозь
            # корпус соседа (осмотр порции 2).
            z1x, z1y, z2x, z2y = gx, gor + 240 + dy_, gx, gor + 240 + dy_
            if i == 0:
                r1, (z1x, z1y), _ = _ruka_mimo(gx, gor + 240 + dy_, fh2, 1,
                                          fh2 * .46, -52, t,
                                          "#5a4636", "#cfe4f5", .2, 8.0)
                gul += r1
            if i == 0:
                # шапка ЛЕЖИТ ПОД варежкой: хват читается перекрытием
                gul += (f'<ellipse cx="{z1x:.0f}" cy="{z1y-16:.0f}" rx="56"'
                        f' ry="30" fill="#4a3a2c" {o(5)}/>'
                        f'<path d="M{z1x-48:.0f},{z1y-20:.0f} q48,-50 96,0 Z"'
                        f' fill="#5a4636" {o(4)}/>')
                gul += _varezhka(z1x, z1y, fh2, t, .2, "#dcd0bc")
            gul += para_izo_rta(gx + fh2 * .12, gor + 240 + dy_ - fh2 * .80, t,
                                i * .3, 1.0, .5)
            s += SL(Z_SRED, gul)
    else:
        # дорога опустела, заяц перебегает
        s += SL(Z_SRED, _zayac(620, gor + 330, t, 1.25,
                               A.seg(t, 2.8, 2.4)))
    s += SL(Z_SRED, dym(620, 110, t, 5, .26, 300, .36, "#cfd6de", 1.2))
    # низ кадра
    s += SL(Z_DAL, _zavalinka(90, gor + 120, 980, t, 150))
    s += SL(Z_SRED, (
            _polenica(1240, gor + 120, 420, 200, 67, 60)
            + _sledy(1880, 1066, 1240, 880, 7, 491, "#8fa3b4", 1.25)
            + _dvorovaya_utvar(140, gor + 300, 420, t, 499,
                               ["kadka", "vedro", "korzina"])
            + _kot_zhivoy(1680, gor + 320, t, 1.0, "#2f2a26", .3)))
    s += SL(Z_PERED, _vetka_pered(1980, 130, 740, 156, t, 31, "#241c16", 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 5, .55, .9))
    s += vinetka(.42)
    return s


def romashka_v_devichih_palcah(t):
    """Летнее окно с распахнутыми створками на пол-кадра, за ним настоящий
    ромашковый луг. Девушка сидит на подоконнике боком, ноги свесила в
    комнату: в левой руке ромашка, правой обрывает лепесток."""
    rnd = random.Random(421)
    pol = 1010
    s = f'<rect width="{W}" height="{H}" fill="#2e2a24"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="1920" height="{pol:.0f}"'
                   f' fill="#9a8a70"/>')
    for i in range(19):
        s += SL(Z_DAL, f'<rect x="{i*101:.0f}" y="0" width="54"'
                       f' height="{pol:.0f}" fill="#a89a80" opacity=".5"/>')
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#7a6a52"/>'
            + _pol_shvy(pol + 20, 1070, 503, 6, "#5a4a36"))
    # ОКНО: вид-луг, метка, створки и переплёт поверх
    px, py, pw, ph_ = 240, 180, 900, 540
    put = kontur_proema(px, py, pw, ph_, "pryam")
    lug = (f'<clipPath id="lug4"><path d="{put}"/></clipPath>'
           f'<g clip-path="url(#lug4)">'
           f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
           f' fill="#9fc0d4"/>'
           f'<rect x="{px:.0f}" y="{py+ph_*.42:.0f}" width="{pw:.0f}"'
           f' height="{ph_*.58:.0f}" fill="#8fae5c"/>')
    for i in range(26):
        lx = px + rnd.uniform(10, pw - 10)
        ly = py + ph_ * .46 + rnd.uniform(0, ph_ * .52)
        rr = 14 + (ly - py - ph_ * .46) * .05
        lug += (f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{rr:.0f}"'
                f' fill="#f8f6ee" opacity=".92"/>'
                f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{rr*.42:.0f}"'
                f' fill="#e8b84c"/>')
    lug += "</g>"
    s += SL(Z_SRED, lug + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#efe8da"'
                    f' stroke-width="34"/>'
            + f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#efe8da" stroke-width="22"/>'
            + f'<rect x="{px-70:.0f}" y="{py+ph_-10:.0f}" width="{pw+140:.0f}"'
              f' height="52" rx="12" fill="#e4dcc8" {o(6)}/>'
            + f'<rect x="{px-56:.0f}" y="{py-54:.0f}" width="{pw+112:.0f}"'
              f' height="40" rx="10" fill="#d8cfbd" {o(5)}/>')
    # распахнутые створки по сторонам — передний план перед проёмом
    for sgn, sx in ((-1, px), (1, px + pw)):
        s += SL(Z_SRED, f'<g transform="rotate({sgn*24:.1f} {sx:.0f} {py:.0f})">'
                        f'<rect x="{sx - (240 if sgn < 0 else 0):.0f}"'
                        f' y="{py:.0f}" width="240" height="{ph_:.0f}" rx="8"'
                        f' fill="#efe8da" {o(6)}/>'
                f'<rect x="{sx - (210 if sgn < 0 else -30):.0f}"'
                f' y="{py+30:.0f}" width="180" height="{ph_*.42:.0f}" rx="6"'
                f' fill="#cfe0ea" opacity=".5" {o(4)}/>'
                f'<rect x="{sx - (210 if sgn < 0 else -30):.0f}"'
                f' y="{py+ph_*.52:.0f}" width="180" height="{ph_*.40:.0f}" rx="6"'
                f' fill="#cfe0ea" opacity=".5" {o(4)}/></g>')
    # комната: кровать с подзорами, коврик с оленями, гитара, лампа
    s += SL(Z_SRED, _krovat(1240, pol, 640, t, 13, True, 300))
    s += SL(Z_SRED, _kovrik_s_olenyami(1300, 180, 540, 360, t))
    s += SL(Z_SRED, _gitara_na_stene(1760, 300, t, .92))
    # комод с ящиками, стул, этажерка с книгами и подушки на кровати
    s += SL(Z_SRED, f'<rect x="1180" y="620" width="520" height="280" rx="10"'
                    f' fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="1200" y="{644+i*86:.0f}" width="480"'
                        f' height="74" rx="7" fill="#8a6a44" {o(4)}/>'
                f'<rect x="1400" y="{672+i*86:.0f}" width="80" height="16" rx="7"'
                f' fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, _podushka(1340, 720, 300, 160, t, .2, .0, .0)
            + _podushka(1560, 700, 260, 150, t, .6, .0, .0))
    s += SL(Z_SRED, _venskiy_stul(1080, pol + 4, 520, t, -2.0, False))
    s += SL(Z_SRED, _knizhnaya_polka(1740, 620, 170, t, 673, 2, 180))
    s += SL(Z_SRED, _ramki_na_stene(1200, 110, 520, t, 677, 3))
    s += SL(Z_SRED, krynka(1240, 616, 1.5) + krynka(1360, 616, 1.2))
    s += SL(Z_SRED, _kruzhka(1470, 612, 1.3, 0, "#efe3d4", 1)
            + _kruzhka(1570, 614, 1.15, 0, "#e8dcc8", -1))
    s += SL(Z_SRED, lampa(1180, 560, t, .9, True))
    s += SL(Z_SRED, _konus_sveta(1180, 600, 420, 300, 0, .38))
    # ДЕВУШКА на подоконнике боком, ноги в комнату
    fx, fy, fh = 700, py + ph_ + 40, 620
    obr = A.ease(A.seg(t, .6, 1.1))
    dev = figura(fx, fy, fh, t, col="#6a7a98", kant="#ffd98a", ph=.3,
                 profil=True, naklon=-6.0)
    d1, (r1x, r1y), _ = _ruka(fx, fy, fh, -1, fh * .40, -22, t,
                              "#6a7a98", "#ffd98a", .3, 4.0)
    d2, (r2x, r2y), _ = _ruka(fx, fy, fh, 1, fh * .34, -30 + 16 * obr, t,
                              "#6a7a98", "#ffd98a", .7, 5.0)
    dev += d1 + d2
    # коса на плече
    dev += (f'<path d="M{fx+fh*.10:.0f},{fy-fh*.76:.0f}'
            f' q{fh*.08:.0f},{fh*.16:.0f} {fh*.02:.0f},{fh*.30:.0f}"'
            f' fill="none" stroke="#8a6a3c" stroke-width="{fh*.044:.0f}"'
            f' stroke-linecap="round"/>'
            f'<path d="M{fx+fh*.12:.0f},{fy-fh*.46:.0f} l{fh*.03:.0f},{fh*.05:.0f}'
            f' l{-fh*.04:.0f},{fh*.02:.0f} Z" fill="{TKAN}" {o(2)}/>')
    s += SL(Z_SRED, dev)
    # РОМАШКА в левой руке, лепесток отрывается правой
    # цветок МЕЛЬЧЕ ГОЛОВЫ девушки (голова 180 px, ромашка 130): было
    # крупнее головы и перетягивала кадр на себя
    s += SL(Z_SRED, _romashka(r1x + 14, r1y - 26, t, .62, 8, obr, -12))
    # варежка только на той руке, что держит стебель; правая обрывает
    # лепесток рукавом без кисти — ей перекрывать нечего
    s += SL(Z_SRED, _varezhka(r1x + 8, r1y - 18, fh, t, .3))
    # оторванный лепесток падает
    if obr > .5:
        pk = A.seg(t, 1.7, 1.8)
        s += SL(Z_LETIT, f'<ellipse cx="{r1x+50+30*pk:.0f}"'
                         f' cy="{r1y-10+260*pk:.0f}" rx="22" ry="11"'
                         f' transform="rotate({40+200*pk:.0f} {r1x+70+40*pk:.0f}'
                         f' {r1y-20+260*pk:.0f})" fill="#f8f6ee"'
                         f' opacity="{1-pk*.5:.2f}" {o(3)}/>')
    s += SL(Z_SRED, ten(fx, py + ph_ + 50, 150, 22, .4))
    # низ кадра
    s += SL(Z_SRED, _polovik(520, pol + 30, 760, 110, "#8a5a52", "#c9a05a")
            + _valenki_u_dveri(300, pol + 76, .92, t)
            + _gorodskoy_hlam(1540, pol + 70, 380, t, 509,
                              ["korobka", "yaschik"])
            + _kot_zhivoy(1000, pol + 64, t, 1.15, "#423b35", .6, True, True))
    s += SL(Z_PERED, _stolb_pered(-8, 92, "#1b1612", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 1180, 600, 5, 61, 140, .2))
    s += vinetka(.34)
    return s


def babushka_podglyadyvaet_v_schelku(t):
    """Дверной проём в ту же комнату, дверь приоткрыта на ладонь. Бабушка в
    фартуке с полотенцем в левой руке прикрывает улыбку правой и заглядывает
    в щель, где внучка с ромашкой. Потом скрещивает пальцы и отходит."""
    rnd = random.Random(431)
    pol = 1000
    s = f'<rect width="{W}" height="{H}" fill="#2a2620"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="1920" height="{pol:.0f}"'
                   f' fill="#8a7a62"/>')
    for i in range(19):
        s += SL(Z_DAL, f'<rect x="{i*101:.0f}" y="0" width="52"'
                       f' height="{pol:.0f}" fill="#9a8a70" opacity=".5"/>')
    # рамки левее и выше: третья садилась на правый край лица бабушки
    s += SL(Z_DAL, _ramki_na_stene(40, 140, 430, t, 521, 2))
    s += SL(Z_DAL, _veshalka_s_paltom(60, 420, 1040, t, 523))
    # полка с обувью и две шляпные коробки в коридоре
    s += SL(Z_DAL, f'<rect x="80" y="900" width="760" height="26" rx="8"'
                   f' fill="url(#dosk)" {o(5)}/>')
    for i in range(5):
        bx = 150 + i * 150
        s += SL(Z_DAL, f'<path d="M{bx-66:.0f},900 q{22:.0f},{-74:.0f}'
                       f' {70:.0f},{-70:.0f} q{50:.0f},{12:.0f} {54:.0f},{70:.0f} Z"'
                       f' fill="{["#3a2e26", "#5a3a2c", "#2e3540"][i % 3]}" {o(5)}/>'
                f'<rect x="{bx-70:.0f}" y="888" width="134" height="16" rx="6"'
                f' fill="#1d1812" {o(3)}/>')
    for i in (0, 1):
        s += SL(Z_DAL, f'<ellipse cx="{200+i*230:.0f}" cy="370" rx="92" ry="32"'
                       f' fill="#c9b79c" {o(5)}/>'
                f'<rect x="{108+i*230:.0f}" y="370" width="184" height="72" rx="12"'
                f' fill="#b8a68c" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="{pol-14:.0f}" width="{W}"'
                   f' height="{H-pol+14:.0f}" fill="#6a5440"/>'
            + _pol_shvy(pol + 18, 1070, 541, 6, "#4e3e2c"))
    s += SL(Z_DAL, tusklaya_lampochka(420, 130, t, 1.15, True))
    s += SL(Z_DAL, _konus_sveta(420, 180, 560, 480, 0, .38))
    # ДВЕРНОЙ ПРОЁМ — крупный предмет; дверь приоткрыта на ладонь
    dx0, dy0, dw, dh = 900, 140, 760, 860
    s += SL(Z_SRED, f'<rect x="{dx0-50:.0f}" y="{dy0-50:.0f}" width="{dw+100:.0f}"'
                    f' height="{dh+50:.0f}" rx="10" fill="#6a5030" {o(8)}/>'
            + f'<rect x="{dx0:.0f}" y="{dy0:.0f}" width="{dw:.0f}"'
              f' height="{dh:.0f}" fill="#1b2029"/>')
    # в щели видна внучка на подоконнике с ромашкой
    sch = 190
    s += SL(Z_SRED, f'<clipPath id="schel4"><rect x="{dx0:.0f}" y="{dy0:.0f}"'
                    f' width="{sch:.0f}" height="{dh:.0f}"/></clipPath>'
            + f'<g clip-path="url(#schel4)">'
            + f'<rect x="{dx0:.0f}" y="{dy0:.0f}" width="{sch:.0f}"'
              f' height="{dh:.0f}" fill="#9fc0d4"/>'
            + f'<rect x="{dx0:.0f}" y="{dy0+360:.0f}" width="{sch:.0f}"'
              f' height="{dh-360:.0f}" fill="#a89a80"/>'
            + f'<rect x="{dx0+20:.0f}" y="{dy0+560:.0f}" width="{sch:.0f}"'
              f' height="60" rx="10" fill="#e4dcc8" {o(5)}/>'
            # внучка ВИДНА ЦЕЛИКОМ, с головой: на dy0+300 её голова уходила
            # выше щели, и в щели оставалась фигура без лица (осмотр порции 2)
            + figura(dx0 + 110, dy0 + 560, 400, t, col="#6a7a98",
                     kant="#ffd98a", ph=.4, profil=True, naklon=-6.0)
            + _romashka(dx0 + 150, dy0 + 300, t, .5, 8, .4, -10)
            + "</g>")
    # створка двери поверх, приоткрыта
    s += SL(Z_SRED, f'<g transform="translate({sch:.0f},0)">'
                    f'{dver(dx0, dy0, dw - sch, dh, .0, "url(#derev)", True, False)}'
                    f'</g>')
    s += SL(Z_SRED, f'<rect x="{dx0-50:.0f}" y="{dy0-86:.0f}" width="{dw+100:.0f}"'
                    f' height="46" rx="12" fill="#7d5a3c" {o(6)}/>')
    # БАБУШКА в коридоре у двери
    ott = A.ease(A.seg(t, 2.4, 1.2))
    # в коридоре у двери стоит ОДНА фигура: внучка видна в щели, но она за
    # дверью, в другом плане, и обходить её рукой не нужно
    _figury_kadra((700 - 120 * ott, pol + 24, 790))
    fx, fy, fh = 700 - 120 * ott, pol + 24, 790
    bab = figura(fx, fy, fh, t, col="#4a5a6a", kant="#ffd98a", platok=True,
                 ph=.5, naklon=8 - 4 * ott)
    b1, (p1x, p1y), _ = _ruka_so_sgibom(fx, fy, fh, 1, fh * .22, 22,
                                        fh * .22, -40, t, "#4a5a6a",
                                        "#ffd98a", .5, 3.0)
    b2, (p2x, p2y), _ = _ruka(fx, fy, fh, -1, fh * .42, 50, t,
                              "#4a5a6a", "#ffd98a", .9, 4.0)
    bab += b1 + b2
    bab += (f'<path d="M{fx-62:.0f},{fy-fh*.52:.0f} L{fx+62:.0f},{fy-fh*.52:.0f}'
            f' L{fx+76:.0f},{fy-fh*.08:.0f} L{fx-76:.0f},{fy-fh*.08:.0f} Z"'
            f' fill="#e8e0ca" {o(5)}/>'
            f'<path d="M{fx-76:.0f},{fy-fh*.32:.0f} q{76:.0f},{16:.0f} {152:.0f},0"'
            f' fill="none" stroke="#c4b79c" stroke-width="7"/>')
    s += SL(Z_SRED, bab)
    # полотенце в левой руке
    s += SL(Z_SRED, f'<path d="M{p2x-36:.0f},{p2y:.0f} L{p2x+36:.0f},{p2y-10:.0f}'
                    f' L{p2x+46:.0f},{p2y+180:.0f} L{p2x-28:.0f},{p2y+190:.0f} Z"'
                    f' fill="url(#rush)" {o(5)}/>'
            + f'<rect x="{p2x-30:.0f}" y="{p2y+100:.0f}" width="74" height="16"'
              f' fill="{TKAN}" opacity=".8"/>')
    # правая ладонь прикрывает улыбку; к концу — скрещённые пальцы на удачу
    s += SL(Z_SRED, _varezhka(p2x, p2y, fh, t, .9))
    if ott > .3:
        s += SL(Z_SRED, f'<g transform="rotate(-16 {p1x:.0f} {p1y:.0f})">'
                        f'<rect x="{p1x-10:.0f}" y="{p1y-66:.0f}" width="20"'
                        f' height="70" rx="10" fill="#e8d8c0" {o(4)}/>'
                f'<rect x="{p1x+6:.0f}" y="{p1y-62:.0f}" width="20" height="66"'
                f' rx="10" fill="#e8d8c0" {o(4)}/>'
                f'<path d="M{p1x-14:.0f},{p1y-44:.0f} l48,-14" fill="none"'
                f' stroke="#b89a74" stroke-width="7"/></g>')
    s += SL(Z_SRED, ten(fx, fy + 8, 176, 26, .45))
    # кошка идёт за бабушкой
    s += SL(Z_SRED, _kot_zhivoy(fx - 230, pol + 60, t, 1.2, "#423b35", .4))
    # комод коридора, зонт и сумка — вещи среднего плана
    s += SL(Z_SRED, f'<rect x="60" y="{pol-300:.0f}" width="460" height="300"'
                    f' rx="10" fill="url(#derev)" {o(6)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{80+i*150:.0f}" y="{pol-274:.0f}" width="134"'
                        f' height="120" rx="7" fill="#8a6a44" {o(4)}/>'
                f'<rect x="{80+i*150:.0f}" y="{pol-140:.0f}" width="134"'
                f' height="110" rx="7" fill="#9c7a4c" {o(4)}/>'
                f'<rect x="{126+i*150:.0f}" y="{pol-224:.0f}" width="46"'
                f' height="14" rx="7" fill="url(#zhel)" {o(3)}/>')
    s += SL(Z_SRED, _zont_v_podstavke(640, pol - 6, t, 1.1))
    s += SL(Z_SRED, _sumka_hozyaystvennaya(790, pol - 10, t, .86, 1.0))
    s += SL(Z_SRED, _ramki_na_stene(740, 150, 180, t, 683, 1))
    # низ кадра
    s += SL(Z_SRED, _polovik(420, pol + 30, 720, 110, "#8a5a52", "#c9a05a")
            + _valenki_u_dveri(200, pol + 80, 1.0, t)
            + _gorodskoy_hlam(1680, pol + 70, 240, t, 547, ["korobka"])
            + _dvorovaya_utvar(1180, pol + 90, 300, t, 557, ["korzina"]))
    s += SL(Z_PERED, _stolb_pered(1876, 76, "#171209", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 420, 180, 5, 67, 140, .2))
    s += vinetka(.38)
    return s


def poslednyaya_gryadka_redki(t):
    """Огород в первом инее: последняя грядка, из земли торчат чёрные макушки
    редьки с ботвой. Отец обеими руками тянет за ботву огромную редьку, сын
    на корточках укладывает корзину. Рядом лопата, пугало, ворона."""
    rnd = random.Random(433)
    gor = 600
    s = f'<rect width="{W}" height="{H}" fill="url(#nrassv)"/>'
    s += nebo("rassv", t, False, 107)
    s += oblaka(t, 150, 5, 109, .44, "#e4e8f0", 15.0)
    s += SL(Z_DAL, _derevnya_ryad(gor - 70, t, 71, ((180, 300), (520, 250))))
    s += SL(Z_DAL, goloe_derevo(1700, gor - 20, 520, t, 113, 9, "#3a3b43", True))
    s += SL(Z_DAL, _zabor_dosok(820, gor - 180, 1100, 190, 73, 56))
    s += SL(Z_DAL, dym(260, gor - 290, t, 5, .26, 300, .4, "#cfd6de", 1.2))
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#5a4a36"/>'
            + _zemlya_faktura(gor + 40, 1050, 31, 16, "#473a2c")
            + _inej(569, 62, gor + 50, 1060)
            + _pol_shvy(gor + 40, 1070, 571, 6, "#3e3226"))
    # ГРЯДКИ РЕДЬКИ — крупный предмет кадра, одна редька выскакивает
    vyh = A.ease(A.seg(t, 1.4, 1.0))
    s += SL(Z_SRED, _gryadka_redki(60, gor + 300, 1040, t, 577, 6, 3, vyh))
    s += SL(Z_SRED, _gryadka_redki(1120, gor + 200, 760, t, 587, 4, -1, .0))
    # ПУГАЛО и ворона, которая слетает
    s += SL(Z_SRED, _pugalo(1480, gor + 190, t, 1.05))
    s += SL(Z_SRED, _vorona(1480, gor - 240, t, 1.1, .2,
                            A.ease(A.seg(t, 2.2, 1.0))))
    # лопата воткнута в грядку
    s += SL(Z_SRED, f'<line x1="300" y1="{gor+120:.0f}" x2="322"'
                    f' y2="{gor+330:.0f}" stroke="url(#derev)" stroke-width="19"'
                    f' stroke-linecap="round"/>'
            + f'<path d="M300,{gor+322:.0f} L376,{gor+338:.0f} L364,{gor+426:.0f}'
              f' L288,{gor+410:.0f} Z" fill="url(#zhel)" {o(5)}/>'
            + f'<path d="M290,{gor+120:.0f} l12,-34 l26,32 Z" fill="#5b4428" {o(3)}/>')
    # ОТЕЦ тянет редьку обеими руками, откинувшись назад
    sad = A.ease(A.seg(t, 2.4, .9))
    ox2, oy2, oh2 = 700, gor + 420 + 110 * sad, 800 - 240 * sad
    otec = figura(ox2, oy2, oh2, t, col="#46506a", kant="#cfe4f5",
                  shapka=True, boroda=True, ph=.3, naklon=-16 + 24 * sad)
    o1, (a1x, a1y), _ = _ruka(ox2, oy2, oh2, 1, oh2 * .44, -30 + 50 * sad, t,
                              "#46506a", "#cfe4f5", .3, 6.0)
    o2, (a2x, a2y), _ = _ruka(ox2, oy2, oh2, 1, oh2 * .36, -12 + 46 * sad, t,
                              "#46506a", "#cfe4f5", .7, 6.0)
    otec += o1 + o2
    s += SL(Z_SRED, otec)
    # ОГРОМНАЯ РЕДЬКА в руках: выскакивает из земли
    s += SL(Z_SRED, _redka(a1x + 70, a1y + 40 - 60 * vyh, 1.5, t, 14 - 20 * vyh,
                           .6 + .4 * vyh))
    s += SL(Z_SRED, _varezhka(a1x, a1y, oh2, t, .3, "#dcd0bc")
            + _varezhka(a2x, a2y, oh2, t, .7, "#dcd0bc"))
    s += SL(Z_SRED, para_izo_rta(ox2 + 70, oy2 - oh2 * .80, t, .3, 1.3, .55))
    # СЫН на корточках у корзины — вдвое меньше отца, в профиль
    syx, syy, syh = 1130, gor + 430, 340
    syn = figura(syx, syy, syh, t, col="#5a6a52", kant="#cfe4f5", ph=.8,
                 profil=True, naklon=12.0)
    s1, (b1x, b1y), _ = _ruka(syx, syy, syh, -1, syh * .44, 46, t,
                              "#5a6a52", "#cfe4f5", .8, 5.0)
    s2, (b2x, b2y), _ = _ruka(syx, syy, syh, -1, syh * .36, 64, t,
                              "#5a6a52", "#cfe4f5", .4, 5.0)
    syn += s1 + s2
    s += SL(Z_SRED, syn)
    # корзина с уже выдернутыми редьками
    s += SL(Z_SRED, _dvorovaya_utvar(900, gor + 440, 240, t, 593, ["korzina"]))
    for i in range(4):
        s += SL(Z_SRED, _redka(960 + i * 44, gor + 350 + (i % 2) * 20, .54, t,
                               -18 + i * 12, .2))
    s += SL(Z_SRED, _varezhka(b1x, b1y, syh, t, .8, "#dcd0bc")
            + _varezhka(b2x, b2y, syh, t, .4, "#dcd0bc"))
    s += SL(Z_SRED, para_izo_rta(syx + 50, syy - syh * .80, t, .8, .9, .45))
    # низ кадра
    s += SL(Z_SRED, _kucha_listev(400, 1058, 320, 599, 86)
            + _luzha(1660, 1030, 180, t, .3)
            + _kot_zhivoy(180, 1046, t, 1.0, "#3b342f", .2)
            + _sledy(1880, 1066, 1300, 900, 6, 601, "#33281d", 1.2)
            + _dvorovaya_utvar(1700, gor + 430, 220, t, 607, ["vedro"]))
    s += SL(Z_PERED, _vetka_pered(-70, 120, 700, 24, t, 37, "#241c16", 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 5, .4, .75))
    s += vinetka(.36)
    return s


def chernaya_redka_na_stole(t):
    """Кухонный стол на пол-кадра: доска, тёрка, миска, бутыль масла,
    луковица, солонка, кадушка с капустой. В окне кухни — настоящий кадр, где
    редьку трут на тёрке. Хозяйка режет, льёт масло и сыплет соль."""
    rnd = random.Random(439)
    pol = 1000
    s = f'<rect width="{W}" height="{H}" fill="#2a241c"/>'
    s += SL(Z_DAL, brevna(0, 40, 1020, 700, 96)
            + brevna(1020, 40, 900, 700, 96))
    s += SL(Z_DAL, _polka_s_utvaryu(70, 240, 580, t, 613, 5))
    s += SL(Z_DAL, _polka_s_utvaryu(80, 520, 540, t, 617, 4))
    s += SL(Z_DAL, f'<rect x="0" y="684" width="{W}" height="40" rx="8"'
                   f' fill="#4a3522" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#5e4a34"/>'
            + polovicy(pol + 16) + _pol_shvy(pol + 20, 1070, 619, 6, "#4a3824"))
    # НАСТОЯЩИЙ КАДР в окне над столом: вид, метка, наличник поверх
    px, py, pw, ph_ = 1020, 170, 820, 400
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<clipPath id="ter4"><path d="{put}"/></clipPath>'
           f'<g clip-path="url(#ter4)">'
           f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
           f' fill="#8a9aa8"/>'
           f'<rect x="{px:.0f}" y="{py+ph_*.56:.0f}" width="{pw:.0f}"'
           f' height="{ph_*.44:.0f}" fill="#a89a80"/>')
    for i in range(7):
        vid += (f'<ellipse cx="{px+90+i*110:.0f}" cy="{py+ph_*.70:.0f}" rx="44"'
                f' ry="16" fill="#f2efe8" opacity=".9"/>')
    vid += (f'<circle cx="{px+pw*.5:.0f}" cy="{py+ph_*.3:.0f}" r="92"'
            f' fill="#ffd98a" opacity=".2"/></g>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#6a5030"'
                    f' stroke-width="32"/>'
            + f'<rect x="{px-42:.0f}" y="{py-50:.0f}" width="{pw+84:.0f}"'
              f' height="40" rx="10" fill="#7d5a3c" {o(5)}/>'
            + f'<rect x="{px-56:.0f}" y="{py+ph_-10:.0f}" width="{pw+112:.0f}"'
              f' height="46" rx="10" fill="url(#dosk)" {o(6)}/>'
            + f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#6a5030" stroke-width="22"/>')
    # СТОЛ — крупный предмет
    s += SL(Z_SRED, f'{ten(960, pol + 20, 600, 28, .5)}'
                    f'<rect x="120" y="700" width="1420" height="54" rx="12"'
                    f' fill="url(#derev)" {o(8)}/>'
            + f'<rect x="150" y="754" width="1360" height="26" rx="8"'
              f' fill="#5b4428" {o(5)}/>')
    for px2 in (220, 1380):
        s += SL(Z_SRED, f'<rect x="{px2:.0f}" y="780" width="70"'
                        f' height="{pol-780:.0f}" rx="12" fill="#5b4428" {o(6)}/>')
    # доска с ломтиками, тёрка, миска, бутыль, луковица, солонка
    s += SL(Z_SRED, f'<path d="M300,700 L720,700 L700,620 L320,620 Z"'
                    f' fill="url(#dosk)" {o(6)}/>'
            + f'<circle cx="326" cy="636" r="15" fill="none" stroke="#5b4428"'
              f' stroke-width="7"/>')
    # (редька рисуется ПОСЛЕ фигуры, ниже по сцене: корпус хозяйки
    # закрывал её на 57-81% — осмотр порции 2)
    rez = A.ease(A.seg(t, .4, 1.2))
    for i in range(5):
        if rez > i * .2:
            s += SL(Z_SRED, f'<ellipse cx="{560+i*44:.0f}" cy="{668-i*4:.0f}"'
                            f' rx="30" ry="12" fill="#efe8da" {o(4)}/>'
                    f'<ellipse cx="{560+i*44:.0f}" cy="{664-i*4:.0f}" rx="22"'
                    f' ry="8" fill="#f8f6ee" opacity=".9"/>')
    s += SL(Z_SRED, _terka(900, 700, t, 1.0, -10))
    s += SL(Z_SRED, f'<path d="M1010,700 q90,54 180,0 q-14,-74 -90,-78'
                    f' q-76,4 -90,78 Z" fill="#e7edf0" {o(6)}/>'
            + f'<ellipse cx="1100" cy="630" rx="90" ry="26" fill="#f6fbff"'
              f' opacity=".92"/>')
    lej = A.ease(A.seg(t, 2.2, 1.0)) * (1 - A.ease(A.seg(t, 3.6, .8)))
    s += SL(Z_SRED, _butyl_masla(980, 700, 1.05, t, lej, lej))
    s += SL(Z_SRED, f'<ellipse cx="800" cy="676" rx="54" ry="44"'
                    f' fill="#d8b070" {o(5)}/>'
            + f'<path d="M800,634 q10,-26 26,-32" fill="none" stroke="#8a7a46"'
              f' stroke-width="7"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{760+i*26:.0f},676 q{14:.0f},{-34:.0f}'
                        f' {6:.0f},{-40:.0f}" fill="none" stroke="#c9a05a"'
                        f' stroke-width="4" opacity=".7"/>')
    s += SL(Z_SRED, f'<path d="M1420,700 L1500,700 L1488,624 L1432,624 Z"'
                    f' fill="url(#derev)" {o(5)}/>'
            + f'<ellipse cx="1460" cy="624" rx="30" ry="11" fill="#efe8da" {o(3)}/>')
    s += SL(Z_SRED, _kadushka_kapusty(1700, pol - 6, t, 1.05))
    # ХОЗЯЙКА у стола
    fx, fy, fh = 600, pol + 24, 830
    sol = A.ease(A.seg(t, 4.2, .9))
    hoz = figura(fx, fy, fh, t, col="#4a5a6a", kant="#ffd98a", platok=True,
                 ph=.4, naklon=7.0)
    h1, (c1x, c1y), _ = _ruka(fx, fy, fh, 1, fh * .46,
                              34 - 30 * lej - 20 * sol, t,
                              "#4a5a6a", "#ffd98a", .4, 5.0)
    h2, (c2x, c2y), _ = _ruka(fx, fy, fh, 1, fh * .36, 52, t,
                              "#4a5a6a", "#ffd98a", .8, 4.0)
    hoz += h1 + h2
    hoz += (f'<path d="M{fx-64:.0f},{fy-fh*.54:.0f} L{fx+64:.0f},{fy-fh*.54:.0f}'
            f' L{fx+78:.0f},{fy-fh*.08:.0f} L{fx-78:.0f},{fy-fh*.08:.0f} Z"'
            f' fill="#e4dcc8" {o(5)}/>')
    s += SL(Z_SRED, hoz)
    # нож в правой руке и щепоть соли
    if lej < .2 and sol < .2:
        # НОЖ: широкое полотно с обухом, пята и деревянная рукоять с
        # заклёпками — раньше читался серой палкой
        s += SL(Z_SRED, f'<g transform="rotate({34 - 20 * rez:.1f} {c1x:.0f}'
                        f' {c1y:.0f})">'
                        f'<path d="M{c1x+8:.0f},{c1y-16:.0f} L{c1x+186:.0f},'
                        f'{c1y-6:.0f} L{c1x+196:.0f},{c1y+12:.0f} L{c1x+8:.0f},'
                        f'{c1y+22:.0f} Z" fill="#dce4e8" {o(5)}/>'
                f'<path d="M{c1x+14:.0f},{c1y-12:.0f} L{c1x+180:.0f},{c1y-4:.0f}"'
                f' stroke="#a8b4ba" stroke-width="6" fill="none"/>'
                f'<rect x="{c1x-72:.0f}" y="{c1y-18:.0f}" width="84" height="40"'
                f' rx="12" fill="url(#derev)" {o(5)}/>'
                f'<circle cx="{c1x-46:.0f}" cy="{c1y+2:.0f}" r="5"'
                f' fill="{ZHELEZ}"/>'
                f'<circle cx="{c1x-18:.0f}" cy="{c1y+2:.0f}" r="5"'
                f' fill="{ZHELEZ}"/></g>')
    if sol > .1:
        for i in range(7):
            k = ((t * 1.3 + i * .14) % 1.0)
            s += SL(Z_SRED, f'<circle cx="{c1x+20+i*6+10*k:.0f}"'
                            f' cy="{c1y+30+140*k:.0f}" r="4"'
                            f' fill="#f8f6ee" opacity="{.9*(1-k):.2f}"/>')
    s += SL(Z_SRED, _varezhka(c1x, c1y, fh, t, .4) + _varezhka(c2x, c2y, fh, t, .8))
    # РЕДЬКА — ГЛАВНЫЙ ПРЕДМЕТ, поверх всего и крупно: половина на доске
    # и целая на свободном правом краю стола
    s += SL(Z_SRED, _redka(1280, 646, 1.6, t, -12, .35))
    s += SL(Z_SRED, _redka(1020, 676, 1.15, t, 24, .25))
    s += SL(Z_SRED, lampa(300, 560, t, .95, True))
    s += SL(Z_SRED, _konus_sveta(300, 600, 480, 340, 0, .40))
    s += SL(Z_SRED, ten(fx, fy + 8, 176, 26, .45))
    # низ кадра
    s += SL(Z_SRED, _dvorovaya_utvar(820, pol + 90, 420, t, 631,
                                     ["kadka", "korzina", "vedro"])
            + _yaschiki(96, pol + 84, t, 641, 2, .86)
            + _kot_zhivoy(1420, pol + 70, t, 1.15, "#3b342f", .5)
            + kartoshka(600, pol + 96, t, 7, 6, 1.0))
    s += SL(Z_PERED, _stolb_pered(1874, 80, "#181209", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 300, 600, 5, 71, 150, .22))
    s += vinetka(.38)
    return s


def redka_v_zimney_kladovoy(t):
    """Полка кладовой на пол-кадра: в ряд чёрные редьки, связки лука, банка
    мёда, сушёная малина в мешочке, градусник в футляре. Мать перекладывает
    редьки из корзины, одна редька чихает и получает от соседней шарф."""
    rnd = random.Random(443)
    pol = 1010
    s = f'<rect width="{W}" height="{H}" fill="#1f1a14"/>'
    s += SL(Z_DAL, kladka(0, 0, 1060, 760, 78, "#6e6256"))
    s += SL(Z_DAL, kladka(1060, 0, 860, 760, 78, "#655c50"))
    s += SL(Z_DAL, svody(t, "#4b443b", 3))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#4a4036"/>'
            + _pol_shvy(pol + 20, 1070, 643, 6, "#3a3028"))
    s += SL(Z_SRED, svecha(1740, 520, t, .2, 1.6, 120))
    s += SL(Z_SRED, _konus_sveta(1740, 420, 520, 420, -10, .40))
    # ПОЛКА КЛАДОВОЙ — крупный предмет
    s += SL(Z_SRED, _kladovaya_polka(120, 560, 1400, t, 7))
    # РЕДЬКИ в ряд на полке; одна чихает, соседняя повязывает ей шарф
    chih = A.ease(A.seg(t, 1.0, .5)) * (1 - A.ease(A.seg(t, 1.8, .5)))
    shrf = A.ease(A.seg(t, 2.0, .9))
    for i in range(6):
        rx_ = 250 + i * 190
        ry_ = 540 - (14 if i % 2 else 0)
        s += SL(Z_SRED, _redka(rx_, ry_, .86, t, -14 + i * 6,
                               .2 + (.8 * chih if i == 2 else .0)))
        if i == 2:
            # облачко чиха
            for k in range(4):
                kk = ((t * .9 + k * .25) % 1.0)
                s += SL(Z_SRED, f'<circle cx="{rx_-90-50*kk:.0f}"'
                                f' cy="{ry_-30-30*kk:.0f}" r="{(16+16*kk):.0f}"'
                                f' fill="#eaf4ff"'
                                f' opacity="{.55*chih*(1-kk):.2f}"/>')
            # шарф от соседки
            if shrf > .1:
                s += SL(Z_SRED, f'<rect x="{rx_-58:.0f}" y="{ry_+34:.0f}"'
                                f' width="116" height="26" rx="10"'
                                f' fill="{TKAN}" opacity="{shrf:.2f}" {o(4)}/>'
                        f'<path d="M{rx_+40:.0f},{ry_+56:.0f} q{18:.0f},{40:.0f}'
                        f' {2:.0f},{70:.0f} l{-26:.0f},{-8:.0f}'
                        f' q{12:.0f},{-30:.0f} {-2:.0f},{-56:.0f} Z"'
                        f' fill="{TKAN}" opacity="{shrf:.2f}" {o(3)}/>')
    # МАТЬ перед полкой: левая держит корзину у бедра, правая кладёт редьку
    fx, fy, fh = 1300, pol + 30, 820
    per = A.ease(A.seg(t, .4, 1.0))
    mat = figura(fx, fy, fh, t, col="#4a5a6a", kant="#ffd98a", platok=True,
                 ph=.4, naklon=-5.0)
    m1, (a1x, a1y), _ = _ruka(fx, fy, fh, -1, fh * .46, -24 + 48 * (1 - per), t,
                              "#4a5a6a", "#ffd98a", .4, 5.0)
    m2, (a2x, a2y), _ = _ruka(fx, fy, fh, 1, fh * .36, 54, t,
                              "#4a5a6a", "#ffd98a", .8, 4.0)
    mat += m1 + m2
    s += SL(Z_SRED, mat)
    # корзина с редьками у бедра
    s += SL(Z_SRED, f'<path d="M{a2x-14:.0f},{a2y+30:.0f}'
                    f' L{a2x+180:.0f},{a2y+30:.0f} L{a2x+152:.0f},{a2y+170:.0f}'
                    f' L{a2x+14:.0f},{a2y+170:.0f} Z" fill="url(#solom)" {o(6)}/>')
    for k in range(3):
        s += SL(Z_SRED, f'<path d="M{a2x-6:.0f},{a2y+60+k*38:.0f}'
                        f' q{90:.0f},{18:.0f} {178:.0f},0" fill="none"'
                        f' stroke="#8a6a3c" stroke-width="6"/>')
    for k in range(3):
        s += SL(Z_SRED, _redka(a2x + 40 + k * 56, a2y + 36, .46, t,
                               -10 + k * 14, .2))
    # редька едет из корзины на полку
    rx2 = a2x + 80 + (560 - a2x - 80 + 240) * per
    ry2 = a2y + 20 - (a2y + 20 - 540) * per
    s += SL(Z_SRED, _redka(rx2, ry2, .78, t, 20 - 30 * per, .4))
    s += SL(Z_SRED, _varezhka(a1x, a1y, fh, t, .4) + _varezhka(a2x, a2y, fh, t, .8))
    s += SL(Z_SRED, para_izo_rta(fx - 80, fy - fh * .80, t, .4, 1.1, .45))
    s += SL(Z_SRED, ten(fx, fy + 8, 176, 26, .45))
    # низ кадра: кадки, мешки, корзины, кот
    s += SL(Z_SRED, _dvorovaya_utvar(130, pol - 4, 520, t, 647,
                                     ["kadka", "meshok", "korzina", "korob"])
            + _yaschiki(760, pol - 6, t, 653, 3, .92)
            + _kot_zhivoy(1680, pol + 50, t, 1.1, "#2f2a26", .6, True, True)
            + kartoshka(1100, pol + 60, t, 8, 6, 1.1))
    s += SL(Z_SRED, teplo(1740, 470, 480, 400, .40))
    s += SL(Z_PERED, _stolb_pered(-8, 100, "#140f0c", 0, H))
    s += SL(Z_LETIT, iskra_let(t, 1740, 470, 6, 79, 180, .3))
    s += vinetka(.42)
    return s
