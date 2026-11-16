# -*- coding: utf-8 -*-
"""ПОРЦИЯ 3: 35 декораций ролика «18 ноября — День Ионы».

Каждая функция — f(t) -> SVG (без внешнего <svg> и без <defs>). Рисуются
заново под текст этого ролика (R-0019): ни одно тело функции не повторяет
порции 1 и 2 и ни один кадр не взят у соседних роликов. Люди — только
`figura()` из `lok_obshchee`, руки — только `_ruka`/`_ruka_so_sgibom` от
плеча, а где в кадре больше одной фигуры — `_ruka_mimo`/`_ruka_sgib_mimo`
с реестром `_figury_kadra` (R-0051). Источник: `zadaniya/porciya3.md`.

Что держится здесь по итогам осмотра двух принятых порций:
· главный предмет назван в имени сцены, стоит 420-700 px и читается со
  стоп-кадра: у него детали, а не условная геометрия (R-0047);
· рука не пересекает ЧУЖУЮ фигуру, предмет не ложится ни на одно лицо;
· варежка ставится ТОЛЬКО там, где перекрывает предмет на четверть,
  иначе рукав остаётся без кисти; пальцев не рисуем;
· фигуры непрозрачные (op >= .9), иначе читаются призраком;
· группы: рост через одного крупный/мелкий, шаг рваный, треть в профиль и
  треть со спины, наклон ±15°;
· нижняя треть кадра занята НАСТОЯЩИМИ вещами (следы, лужа, листья, ящики,
  вёдра, поленница, кот, сугроб), а не полупрозрачными пятнами;
· своих букв не рисуем вовсе — вместо текста волнистая строка.
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
    _iriska,
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
# Реестр чужих фигур и руки, которые его обходят, уже написаны и проверены
# глазами в порции 2 — заново их не изобретаем, берём оттуда вместе с
# варежкой, световым конусом и фактурой пола. Предметы, которые в этой
# порции встречаются те же (редька, тёрка, кровать, численник), тоже
# берутся готовыми: второй раз один предмет не рисуется.
from chast2 import (
    _banka_krupy,
    _butyl_masla,
    _chaynik,
    _chislennik,
    _cvetok_v_gorshke,
    _figury_kadra,
    _golub,
    _kadushka_kapusty,
    _kafel,
    _kastryulya,
    _konus_sveta,
    _kover_na_stene,
    _kovrik_s_olenyami,
    _kreslo,
    _krovat,
    _kruzhka,
    _knizhnaya_polka,
    _ochki,
    _pol_shvy,
    _polki_otkrytye,
    _polotence,
    _polovik,
    _podushka,
    _ploshka_s_meloch,
    _ramki_na_stene,
    _redka,
    _romashka,
    _ruka_mimo,
    _ruka_sgib_mimo,
    _samovar,
    _sani,
    _skameyka_podezda,
    _snegovik,
    _stog,
    _stolik,
    _sumka_hozyaystvennaya,
    _tabyret,
    _tarelka,
    _terka,
    _ugol_pechnoy_utvari,
    _valenki_u_dveri,
    _varezhka,
    _vaza_s_yablokami,
    _veshalka_s_paltom,
    _venskiy_stul,
    _vesy,
    _vorona,
    _zavalinka,
    _zmeyka_zavisti,
    _zont_v_podstavke)


# ── ПОМОЩНИКИ ЭТОЙ ПОРЦИИ (в baza, lok_obshchee и порции 2 их нет) ─────────

def _repka(x, y, s_=1.0, t=0.0, ph=.0, par_=True):
    """ПАРЕНАЯ РЕПКА: жёлтый шар с поперечными поясками, срез-плечико,
    корешок-хвостик книзу, два листа-обрубка сверху и пар над ней. Шар без
    пояска и хвостика читается просто кружком (R-0047)."""
    r = 54 * s_
    s = (f'{ten(x, y + r * .86, r * .92, r * .22, .45)}'
         f'<path d="M{x-r:.0f},{y-r*.18:.0f}'
         f' q{r*.06:.0f},{-r*.86:.0f} {r*1.0:.0f},{-r*.80:.0f}'
         f' q{r*.94:.0f},{-r*.06:.0f} {r*1.0:.0f},{r*.80:.0f}'
         f' q{r*.04:.0f},{r*.92:.0f} {-r*1.0:.0f},{r*.96:.0f}'
         f' q{-r*1.04:.0f},{-r*.04:.0f} {-r*1.0:.0f},{-r*.96:.0f} Z"'
         f' fill="#e8c64e" {o(6)}/>')
    for i in range(3):
        s += (f'<path d="M{x-r*.84:.0f},{y-r*.46+i*r*.44:.0f}'
              f' q{r*.84:.0f},{r*.22:.0f} {r*1.68:.0f},0" fill="none"'
              f' stroke="#c9a331" stroke-width="{max(3, 6 * s_):.0f}" opacity=".7"/>')
    s += (f'<path d="M{x-r*.70:.0f},{y-r*.56:.0f} q{r*.42:.0f},{-r*.28:.0f}'
          f' {r*.86:.0f},{-r*.08:.0f}" fill="none" stroke="#fdf0b4"'
          f' stroke-width="{max(3, 9 * s_):.0f}" opacity=".6"/>'
          f'<path d="M{x+r*.10:.0f},{y+r*.92:.0f} q{r*.16:.0f},{r*.40:.0f}'
          f' {-r*.06:.0f},{r*.66:.0f}" fill="none" stroke="#d8c08a"'
          f' stroke-width="{max(2, 6 * s_):.0f}" stroke-linecap="round"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*r*.22:.0f},{y-r*.92:.0f}'
              f' q{i*r*.34:.0f},{-r*.42:.0f} {i*r*.62:.0f},{-r*.22:.0f}'
              f' q{-i*r*.22:.0f},{r*.34:.0f} {-i*r*.62:.0f},{r*.22:.0f} Z"'
              f' fill="#5c8a40" {o(4)}/>')
    if par_:
        s += par(x, y - r * 1.5, t, 3, .42, 120, .5)
    return s


def _chugunok(x, y, s_=1.0, t=0.0, vyezd=.0, repok=5):
    """ЧУГУНОК С ПАРЕНОЙ РЕПОЙ — главный предмет сцены: пузатое чёрное
    тулово с обручем по плечу, две литые ушки, отблеск огня по боку, горка
    жёлтых репок через край. `vyezd` 0..1 — насколько он выехал из устья."""
    dx = 150 * vyezd
    r = 118 * s_
    s = (f'<g transform="translate({dx:.0f},0)">'
         f'{ten(x, y + r * .30, r * 1.02, r * .24, .55)}'
         f'<path d="M{x-r*.62:.0f},{y-r*1.26:.0f}'
         f' q{-r*.56:.0f},{r*.52:.0f} {-r*.26:.0f},{r*.96:.0f}'
         f' q{r*.40:.0f},{r*.46:.0f} {r*1.76:.0f},0'
         f' q{r*.30:.0f},{-r*.44:.0f} {-r*.26:.0f},{-r*.96:.0f} Z"'
         f' fill="url(#chug)" {o(8)}/>'
         f'<rect x="{x-r*.70:.0f}" y="{y-r*1.30:.0f}" width="{r*1.40:.0f}"'
         f' height="{r*.20:.0f}" rx="{r*.09:.0f}" fill="#4a4442" {o(5)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-r*1.28:.0f}" rx="{r*.66:.0f}"'
         f' ry="{r*.16:.0f}" fill="#1f1d1c" {o(4)}/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*r*.70:.0f},{y-r*1.18:.0f} q{i*r*.30:.0f},{r*.04:.0f}'
              f' {i*r*.24:.0f},{r*.28:.0f}" fill="none" stroke="#3a3634"'
              f' stroke-width="{max(5, 13 * s_):.0f}"/>')
    s += (f'<path d="M{x-r*.54:.0f},{y-r*.84:.0f} q{-r*.18:.0f},{r*.46:.0f}'
          f' {r*.04:.0f},{r*.76:.0f}" fill="none" stroke="#ffb45a"'
          f' stroke-width="{max(4, 12 * s_):.0f}" opacity="{.42+.28*abs(A.w(t,1.3,.2)):.2f}"/>'
          f'<path d="M{x+r*.46:.0f},{y-r*.92:.0f} q{r*.20:.0f},{r*.40:.0f}'
          f' {r*.02:.0f},{r*.70:.0f}" fill="none" stroke="#ffd98a"'
          f' stroke-width="{max(3, 8 * s_):.0f}" opacity=".35"/>')
    rnd = random.Random(301 + repok)
    for i in range(repok):
        a = -2.4 + i * (2.0 / max(1, repok - 1))
        rx_ = x + math.cos(a) * r * .50
        ry_ = y - r * 1.34 - abs(math.sin(a)) * r * .22 + rnd.uniform(-6, 6)
        s += _repka(rx_, ry_, s_ * .62, t, i * .3, i % 2 == 0)
    return s + "</g>"


def _uhvat_rogi(cx, cy, dl, ug, t, kach=1.0):
    """УХВАТ: короткий черенок (<= 340 px) и железные рога полукольцом,
    которые обхватывают тулово чугунка. Рога крупные — при мелком масштабе
    ухват читается скобой (грабли 14.11, пункт 6)."""
    a = math.radians(ug + 1.4 * kach * A.w(t, 2.4, .2))
    ex, ey = cx + dl * math.cos(a), cy + dl * math.sin(a)
    nx, ny = math.cos(a + 1.5708), math.sin(a + 1.5708)
    s = (f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}"'
         f' stroke="url(#derev)" stroke-width="20" stroke-linecap="round"/>'
         f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}"'
         f' stroke="#3a2a1a" stroke-width="5" opacity=".5"/>'
         f'<path d="M{ex-nx*86:.0f},{ey-ny*86:.0f}'
         f' Q{ex+math.cos(a)*96:.0f},{ey+math.sin(a)*96:.0f}'
         f' {ex+nx*86:.0f},{ey+ny*86:.0f}" fill="none" stroke="{ZHELEZ}"'
         f' stroke-width="19" stroke-linecap="round"/>'
         f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="13" fill="#6f767c" {o(4)}/>'
         f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="15" fill="none"'
         f' stroke="#5b4428" stroke-width="7"/>')
    return s, (ex, ey)


def _zaslonka_pechi(x, y, w_, h_, t, kach=1.0):
    """Заслонка устья, прислонённая рядом: лист с клёпками, дуга-ручка,
    нагар по низу. Покачивается на пятке, а не ездит целиком."""
    ug = 2.6 * kach * A.w(t, 2.9, .4)
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'{ten(x, y + 8, w_ * .52, 14, .5)}'
            f'<path d="M{x-w_*.5:.0f},{y:.0f} L{x-w_*.44:.0f},{y-h_:.0f}'
            f' Q{x:.0f},{y-h_*1.12:.0f} {x+w_*.44:.0f},{y-h_:.0f}'
            f' L{x+w_*.5:.0f},{y:.0f} Z" fill="#4e4a47" {o(7)}/>'
            f'<path d="M{x-w_*.34:.0f},{y-h_*.18:.0f} L{x-w_*.30:.0f},{y-h_*.82:.0f}'
            f' Q{x:.0f},{y-h_*.94:.0f} {x+w_*.30:.0f},{y-h_*.82:.0f}'
            f' L{x+w_*.34:.0f},{y-h_*.18:.0f} Z" fill="#5f5a56" opacity=".8"/>'
            f'<path d="M{x-w_*.22:.0f},{y-h_*.96:.0f} q{w_*.22:.0f},{-h_*.30:.0f}'
            f' {w_*.44:.0f},0" fill="none" stroke="{ZHELEZ}" stroke-width="17"/>'
            + "".join(f'<circle cx="{x-w_*.36+i*w_*.18:.0f}" cy="{y-h_*.10:.0f}"'
                      f' r="7" fill="#8f979d"/>' for i in range(5))
            + f'<path d="M{x-w_*.46:.0f},{y-h_*.08:.0f} q{w_*.46:.0f},{h_*.10:.0f}'
              f' {w_*.92:.0f},0" fill="none" stroke="#1d1a18" stroke-width="12"'
              f' opacity=".7"/></g>')


def _lozhka_derev(x, y, s_=1.0, ug=0.0, kovsh=1.0):
    """Деревянная ложка: черпак-лопатка с ободком, перехват и ручка с
    расписной насечкой. Без ободка черпак читается пятном."""
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{40*s_*kovsh:.0f}"'
            f' ry="{30*s_*kovsh:.0f}" fill="url(#derev)" {o(5)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y+3*s_:.0f}" rx="{28*s_*kovsh:.0f}"'
            f' ry="{20*s_*kovsh:.0f}" fill="#8a6038" opacity=".9"/>'
            f'<rect x="{x-9*s_:.0f}" y="{y+22*s_:.0f}" width="{18*s_:.0f}"'
            f' height="{120*s_:.0f}" rx="{8*s_:.0f}" fill="url(#derev)" {o(4)}/>'
            f'<circle cx="{x:.0f}" cy="{y+140*s_:.0f}" r="{12*s_:.0f}"'
            f' fill="#9c7049" {o(3)}/>'
            + "".join(f'<line x1="{x-8*s_:.0f}" y1="{y+(48+i*22)*s_:.0f}"'
                      f' x2="{x+8*s_:.0f}" y2="{y+(48+i*22)*s_:.0f}"'
                      f' stroke="{KRAS}" stroke-width="{max(2,4*s_):.0f}"'
                      f' opacity=".7"/>' for i in range(3))
            + "</g>")


def _rushnik_vyshityy(x, y, w_, h_=96, t=0.0, seed=5):
    """Длинный вышитый рушник: полотно со складками, две красные полосы
    узора (ромбы и петушиные гребешки), бахрома по концам. Узор — геометрия,
    своих букв не рисуем."""
    rnd = random.Random(seed)
    s = (f'<path d="M{x:.0f},{y:.0f} L{x+w_:.0f},{y-6:.0f} L{x+w_:.0f},{y+h_-4:.0f}'
         f' L{x:.0f},{y+h_:.0f} Z" fill="{RUSH}" {o(5)}/>')
    for p in (.26, .72):
        yy = y + h_ * p
        s += (f'<rect x="{x+10:.0f}" y="{yy:.0f}" width="{w_-20:.0f}"'
              f' height="{h_*.14:.0f}" fill="{TKAN}" opacity=".9"/>')
        for i in range(int(w_ / 76)):
            cx = x + 36 + i * 76
            s += (f'<path d="M{cx:.0f},{yy-h_*.11:.0f} l{18:.0f},{h_*.11:.0f}'
                  f' l{-18:.0f},{h_*.11:.0f} l{-18:.0f},{-h_*.11:.0f} Z"'
                  f' fill="{TKAN}" opacity=".85"/>')
    for i in range(int(w_ / 54)):
        cx = x + 20 + i * 54
        s += (f'<path d="M{cx:.0f},{y+4:.0f} q{6:.0f},{h_*.5:.0f} {-2:.0f},{h_-6:.0f}"'
              f' fill="none" stroke="#d3c3a0" stroke-width="5" opacity=".8"/>')
    for e in (x + 4, x + w_ - 4):
        for i in range(7):
            s += (f'<line x1="{e:.0f}" y1="{y+10+i*(h_-18)/7.0:.0f}"'
                  f' x2="{e+(-26 if e < x + w_ / 2 else 26):.0f}"'
                  f' y2="{y+16+i*(h_-18)/7.0+rnd.uniform(-5,5):.0f}"'
                  f' stroke="#d9cbaa" stroke-width="5"/>')
    return s


def _blyudo_pirogov(x, y, w_, t, razlom=.0, n=5, seed=7):
    """БЛЮДО РУМЯНЫХ ПИРОГОВ — главный предмет: овальное блюдо с бортом,
    пироги защипом вверх, подпалины на корочке. Верхний пирог разламывается:
    из разлома идёт пар и видна оранжевая начинка."""
    rnd = random.Random(seed)
    s = (f'{ten(x, y + 18, w_ * .54, 24, .5)}'
         f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_*.5:.0f}" ry="{w_*.17:.0f}"'
         f' fill="#eae2d2" {o(7)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-4:.0f}" rx="{w_*.42:.0f}"'
         f' ry="{w_*.13:.0f}" fill="#d8ccb6" opacity=".9"/>'
         f'<path d="M{x-w_*.46:.0f},{y-w_*.05:.0f} q{w_*.20:.0f},{-w_*.10:.0f}'
         f' {w_*.46:.0f},{-w_*.07:.0f}" fill="none" stroke="#fffaf0"'
         f' stroke-width="9" opacity=".55"/>')
    for i in range(n):
        px = x - w_ * .32 + i * (w_ * .64 / max(1, n - 1))
        py = y - 22 - (i % 2) * 16
        pw = w_ * .20 * rnd.uniform(.9, 1.1)
        s += (f'<path d="M{px-pw*.5:.0f},{py:.0f} q{pw*.10:.0f},{-pw*.52:.0f}'
              f' {pw*.5:.0f},{-pw*.50:.0f} q{pw*.40:.0f},{-pw*.02:.0f}'
              f' {pw*.5:.0f},{pw*.50:.0f} q{-pw*.5:.0f},{pw*.26:.0f}'
              f' {-pw*1.0:.0f},0 Z" fill="#d79b4e" {o(5)}/>'
              f'<path d="M{px-pw*.34:.0f},{py-pw*.30:.0f} q{pw*.34:.0f},{-pw*.14:.0f}'
              f' {pw*.68:.0f},0" fill="none" stroke="#b5752f" stroke-width="7"'
              f' opacity=".85"/>')
        for j in range(4):
            s += (f'<circle cx="{px-pw*.26+j*pw*.17:.0f}" cy="{py-pw*.18:.0f}"'
                  f' r="{5+rnd.random()*4:.0f}" fill="#9c5a24" opacity=".7"/>')
    # ВЕРХНИЙ ПИРОГ: разламывается на две половинки, начинка наружу
    tx, ty = x - w_ * .06, y - w_ * .30
    rz = 46 * razlom
    for sgn in (-1, 1):
        s += (f'<path d="M{tx+sgn*rz:.0f},{ty:.0f}'
              f' q{sgn*14:.0f},{-70:.0f} {sgn*86:.0f},{-62:.0f}'
              f' q{sgn*22:.0f},{34:.0f} {sgn*10:.0f},{66:.0f} Z"'
              f' fill="#dca254" {o(6)}/>'
              f'<path d="M{tx+sgn*rz:.0f},{ty-4:.0f} q{sgn*18:.0f},{-30:.0f}'
              f' {sgn*16:.0f},{-56:.0f}" fill="none" stroke="{ORA}"'
              f' stroke-width="{10+12*razlom:.0f}" opacity=".95"/>')
    if razlom > .05:
        s += (f'<ellipse cx="{tx:.0f}" cy="{ty-26:.0f}" rx="{16+30*razlom:.0f}"'
              f' ry="{10+18*razlom:.0f}" fill="{ORA}" opacity=".9"/>')
        for i in range(4):
            s += (f'<circle cx="{tx-20+i*14:.0f}" cy="{ty-24-i*4:.0f}"'
                  f' r="{6+i:.0f}" fill="#f0a93c" opacity=".85"/>')
        s += par(tx, ty - 52, t, 4, .5, 150, .5)
    return s


def _morkov_botva(x, y, s_=1.0, t=0.0, ph=.0):
    """Морковь с ботвой: конус с поперечными насечками и перистая зелень,
    которая поводит от тепла."""
    sway = 4.0 * A.w(t, 2.6, ph)
    s = (f'<path d="M{x-26*s_:.0f},{y-86*s_:.0f} L{x+26*s_:.0f},{y-86*s_:.0f}'
         f' Q{x+10*s_:.0f},{y+30*s_:.0f} {x:.0f},{y+54*s_:.0f}'
         f' Q{x-10*s_:.0f},{y+30*s_:.0f} {x-26*s_:.0f},{y-86*s_:.0f} Z"'
         f' fill="{ORA}" {o(5)}/>')
    for i in range(5):
        s += (f'<path d="M{x-22*s_+i*2:.0f},{y-(70-i*26)*s_:.0f}'
              f' q{20*s_:.0f},{7*s_:.0f} {40*s_-i*4:.0f},0" fill="none"'
              f' stroke="#b85c18" stroke-width="{max(2,4*s_):.0f}" opacity=".7"/>')
    s += f'<g transform="rotate({sway:.1f} {x:.0f} {y-86*s_:.0f})">'
    for i in range(5):
        a = math.radians(-150 + i * 30)
        ex = x + 70 * s_ * math.cos(a)
        ey = y - 86 * s_ + 70 * s_ * math.sin(a)
        s += (f'<line x1="{x:.0f}" y1="{y-86*s_:.0f}" x2="{ex:.0f}" y2="{ey:.0f}"'
              f' stroke="#4e7a3c" stroke-width="{max(3,6*s_):.0f}"/>')
        for j in range(3):
            s += (f'<ellipse cx="{x+(ex-x)*(.4+j*.26):.0f}"'
                  f' cy="{y-86*s_+(ey-(y-86*s_))*(.4+j*.26):.0f}"'
                  f' rx="{11*s_:.0f}" ry="{6*s_:.0f}" fill="#5c8a40"'
                  f' opacity=".9"/>')
    return s + "</g>"


def _lukovica(x, y, s_=1.0, t=0.0, ph=.0):
    """Луковица: золотая шелуха дольками, сухой хвостик и корешки."""
    r = 46 * s_
    s = (f'{ten(x, y + r * .80, r * .86, r * .20, .4)}'
         f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r*.88:.0f}"'
         f' fill="{ZOL}" {o(5)}/>')
    for i in (-1, 0, 1):
        s += (f'<path d="M{x+i*r*.40:.0f},{y-r*.84:.0f} q{i*r*.22:.0f},{r*.84:.0f}'
              f' {i*r*.10:.0f},{r*1.66:.0f}" fill="none" stroke="#b5803a"'
              f' stroke-width="{max(2,5*s_):.0f}" opacity=".75"/>')
    s += (f'<path d="M{x-r*.10:.0f},{y-r*.86:.0f} q{r*.14:.0f},{-r*.52:.0f}'
          f' {r*.34:.0f},{-r*.66:.0f}" fill="none" stroke="#c9b06a"'
          f' stroke-width="{max(3,8*s_):.0f}" stroke-linecap="round"/>'
          f'<ellipse cx="{x-r*.34:.0f}" cy="{y-r*.34:.0f}" rx="{r*.22:.0f}"'
          f' ry="{r*.14:.0f}" fill="#f0dca0" opacity=".5"/>')
    for i in range(4):
        s += (f'<line x1="{x-r*.22+i*r*.15:.0f}" y1="{y+r*.82:.0f}"'
              f' x2="{x-r*.30+i*r*.20:.0f}" y2="{y+r*1.10:.0f}"'
              f' stroke="#c4a870" stroke-width="{max(2,3*s_):.0f}"/>')
    return s


def _skalka(x, y, s_=1.0, ug=0.0):
    """Скалка: валик с двумя ручками и прожилиной по дереву."""
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'{ten(x, y + 18 * s_, 110 * s_, 12 * s_, .4)}'
            f'<rect x="{x-100*s_:.0f}" y="{y-20*s_:.0f}" width="{200*s_:.0f}"'
            f' height="{40*s_:.0f}" rx="{19*s_:.0f}" fill="url(#derev)" {o(5)}/>'
            f'<rect x="{x-146*s_:.0f}" y="{y-10*s_:.0f}" width="{48*s_:.0f}"'
            f' height="{20*s_:.0f}" rx="{10*s_:.0f}" fill="#9c7049" {o(4)}/>'
            f'<rect x="{x+98*s_:.0f}" y="{y-10*s_:.0f}" width="{48*s_:.0f}"'
            f' height="{20*s_:.0f}" rx="{10*s_:.0f}" fill="#9c7049" {o(4)}/>'
            f'<path d="M{x-84*s_:.0f},{y-8*s_:.0f} q{84*s_:.0f},{-8*s_:.0f}'
            f' {168*s_:.0f},0" fill="none" stroke="#c9a47a" stroke-width="{5*s_:.0f}"'
            f' opacity=".6"/></g>')


def _miska_nachinki(x, y, s_=1.0, t=0.0, col=ORA):
    """Глиняная миска с начинкой: борт, полоска поливы, горка начинки и
    деревянная ложка поперёк борта."""
    r = 78 * s_
    s = (f'{ten(x, y + r * .26, r * .96, r * .20, .45)}'
         f'<path d="M{x-r:.0f},{y-r*.34:.0f} q{r*.14:.0f},{r*.76:.0f}'
         f' {r*1.0:.0f},{r*.76:.0f} q{r*.86:.0f},0 {r*1.0:.0f},{-r*.76:.0f} Z"'
         f' fill="url(#glina)" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-r*.34:.0f}" rx="{r:.0f}" ry="{r*.26:.0f}"'
         f' fill="#b08050" {o(5)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-r*.32:.0f}" rx="{r*.82:.0f}"'
         f' ry="{r*.19:.0f}" fill="{col}" opacity=".95"/>')
    rnd = random.Random(int(x) + 17)
    for i in range(7):
        s += (f'<circle cx="{x+rnd.uniform(-r*.6,r*.6):.0f}"'
              f' cy="{y-r*.40+rnd.uniform(-r*.08,r*.10):.0f}"'
              f' r="{rnd.uniform(7,13)*s_:.0f}" fill="#f0a93c" opacity=".9"/>')
    s += (f'<path d="M{x-r*.92:.0f},{y-r*.10:.0f} q{r*.92:.0f},{r*.18:.0f}'
          f' {r*1.84:.0f},0" fill="none" stroke="{KREM}" stroke-width="{8*s_:.0f}"'
          f' opacity=".7"/>')
    s += _lozhka_derev(x + r * .62, y - r * .52, s_ * .6, 118 + 4 * A.w(t, 2.2, .3))
    return s


def _muka_sypletsya(x, y, t, n=10, seed=3, R=120):
    """Мука сыплется с рук: мелкие крупинки падают и редеют книзу."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        p = ((t * .7 + i / float(n)) % 1.0)
        px = x + rnd.uniform(-40, 40) + 12 * math.sin(p * 6 + i)
        py = y + p * R
        s += (f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(3,7):.0f}"'
              f' fill="#f4efe2" opacity="{1 - p:.2f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y+R:.0f}" rx="{R*.5:.0f}" ry="{R*.12:.0f}"'
          f' fill="#efe8d8" opacity=".55"/>')
    return s


def _yaschik_peska(x, y, w_, h_, t, vyhod=.0, seed=9):
    """ЯЩИК С ПЕСКОМ — главный предмет погреба: дощатый короб с угловыми
    стойками и скобой, песок горкой с бороздками, из песка торчат чёрные
    макушки редьки и рыжие морковки, по краю сыплется струйка песка."""
    rnd = random.Random(seed)
    s = (f'{ten(x + w_ * .5, y + 14, w_ * .54, 22, .55)}'
         f'<path d="M{x:.0f},{y-h_:.0f} L{x+w_:.0f},{y-h_:.0f} L{x+w_-24:.0f},{y:.0f}'
         f' L{x+24:.0f},{y:.0f} Z" fill="url(#dosk)" {o(8)}/>')
    for i in range(4):
        yy = y - h_ + 26 + i * (h_ - 30) / 4.0
        s += (f'<line x1="{x+10:.0f}" y1="{yy:.0f}" x2="{x+w_-10:.0f}"'
              f' y2="{yy:.0f}" stroke="#5b4428" stroke-width="7" opacity=".8"/>')
    for bx in (x + 6, x + w_ - 36):
        s += (f'<rect x="{bx:.0f}" y="{y-h_-6:.0f}" width="30" height="{h_+8:.0f}"'
              f' rx="7" fill="#7d5636" {o(5)}/>')
    s += (f'<rect x="{x+w_*.44:.0f}" y="{y-h_*.56:.0f}" width="86" height="26"'
          f' rx="9" fill="{ZHELEZ}" {o(4)}/>')
    # ПЕСОК: горка с бороздками и ямкой, откуда вынимают редьку
    s += (f'<path d="M{x+16:.0f},{y-h_+42:.0f} Q{x+w_*.3:.0f},{y-h_+4:.0f}'
          f' {x+w_*.52:.0f},{y-h_+30:.0f} Q{x+w_*.8:.0f},{y-h_+56:.0f}'
          f' {x+w_-16:.0f},{y-h_+34:.0f} L{x+w_-16:.0f},{y-20:.0f}'
          f' L{x+16:.0f},{y-20:.0f} Z" fill="#c9a97a" {o(5)}/>')
    for i in range(6):
        yy = y - h_ + 70 + i * 24
        s += (f'<path d="M{x+30:.0f},{yy:.0f} Q{x+w_*.5:.0f},{yy-12:.0f}'
              f' {x+w_-30:.0f},{yy+6:.0f}" fill="none" stroke="#b08f62"'
              f' stroke-width="6" opacity=".6"/>')
    yam = 18 + 26 * vyhod
    s += (f'<ellipse cx="{x+w_*.36:.0f}" cy="{y-h_+44:.0f}" rx="{64+22*vyhod:.0f}"'
          f' ry="{yam:.0f}" fill="#a98a5e" opacity=".9"/>')
    for i in range(4):
        mx = x + w_ * (.56 + i * .10)
        s += _morkov_botva(mx, y - h_ + 30 - (i % 2) * 10, .58, t, i * .4)
    for i in range(3):
        bx = x + w_ * (.14 + i * .09)
        s += (f'<path d="M{bx-34:.0f},{y-h_+40:.0f} q{34:.0f},{-44:.0f}'
              f' {68:.0f},0 q{-34:.0f},{20:.0f} {-68:.0f},0 Z" fill="#2e2b2a" {o(5)}/>'
              f'<line x1="{bx:.0f}" y1="{y-h_+16:.0f}" x2="{bx+6:.0f}"'
              f' y2="{y-h_-12:.0f}" stroke="#5c8a40" stroke-width="7"/>')
    for i in range(9):
        p = ((t * .9 + i / 9.0) % 1.0)
        s += (f'<circle cx="{x+w_*.30+rnd.uniform(-26,26):.0f}"'
              f' cy="{y-h_+50+p*110:.0f}" r="{rnd.uniform(2.5,5):.0f}"'
              f' fill="#e2c898" opacity="{1-p:.2f}"/>')
    return s


def _lestnica(x, y, h_, t, stup=5, ug=-6.0):
    """Приставная лестница погреба: две тетивы и ступени на шипах, нижняя
    ступень стёрта светлее. Чуть покачивается."""
    k = .6 * A.w(t, 3.6, .3)
    s = f'<g transform="rotate({ug + k:.1f} {x:.0f} {y:.0f})">'
    for i in (-1, 1):
        s += (f'<rect x="{x+i*64-11:.0f}" y="{y-h_:.0f}" width="22"'
              f' height="{h_:.0f}" rx="8" fill="#8a6038" {o(5)}/>')
    for i in range(stup):
        yy = y - 30 - i * (h_ - 50) / max(1, stup - 1.0)
        col = "#c9a47a" if i == 0 else "url(#derev)"
        s += (f'<rect x="{x-62:.0f}" y="{yy:.0f}" width="124" height="20"'
              f' rx="7" fill="{col}" {o(4)}/>'
              f'<line x1="{x-56:.0f}" y1="{yy+16:.0f}" x2="{x+56:.0f}"'
              f' y2="{yy+16:.0f}" stroke="#5b4428" stroke-width="4" opacity=".7"/>')
    return s + "</g>"


def _fonar_ruchnoy(x, y, t, s_=1.0, kach=1.0, ph=.0):
    """Ручной фонарь-керосинка: скоба, стекло с язычком огня, донце с
    гайкой, пятно света под ним. Качается на скобе."""
    ug = 6.0 * kach * A.w(t, 2.1, ph)
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y-110*s_:.0f})">'
            f'<path d="M{x-30*s_:.0f},{y-104*s_:.0f} q{30*s_:.0f},{-46*s_:.0f}'
            f' {60*s_:.0f},0" fill="none" stroke="{ZHELEZ}"'
            f' stroke-width="{9*s_:.0f}"/>'
            f'<rect x="{x-34*s_:.0f}" y="{y-104*s_:.0f}" width="{68*s_:.0f}"'
            f' height="{18*s_:.0f}" rx="{7*s_:.0f}" fill="#6f767c" {o(4)}/>'
            f'<path d="M{x-30*s_:.0f},{y-86*s_:.0f} L{x+30*s_:.0f},{y-86*s_:.0f}'
            f' L{x+26*s_:.0f},{y-18*s_:.0f} L{x-26*s_:.0f},{y-18*s_:.0f} Z"'
            f' fill="url(#stekl)" opacity=".85" {o(4)}/>'
            f'<rect x="{x-32*s_:.0f}" y="{y-18*s_:.0f}" width="{64*s_:.0f}"'
            f' height="{22*s_:.0f}" rx="{8*s_:.0f}" fill="{ZHELEZ}" {o(4)}/>'
            f'<circle cx="{x:.0f}" cy="{y+2*s_:.0f}" r="{8*s_:.0f}"'
            f' fill="#8f979d" {o(3)}/>'
            f'{svecha(x, y - 30 * s_, t, ph, s_ * .72, 46 * s_)}'
            f'{teplo(x, y - 54 * s_, 150 * s_, 130 * s_, .45)}</g>')


def _banki_v_pogrebe(x, y, w_, t, seed=11, n=5):
    """Полка с банками закруток: стекло, цветное содержимое слоями, жестяные
    крышки, пара банок с мутным блеском и паутинка в углу."""
    rnd = random.Random(seed)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="26" rx="7"'
         f' fill="url(#dosk)" {o(6)}/>'
         f'<rect x="{x+16:.0f}" y="{y+26:.0f}" width="26" height="54" rx="6"'
         f' fill="#5b4428" {o(4)}/>'
         f'<rect x="{x+w_-42:.0f}" y="{y+26:.0f}" width="26" height="54" rx="6"'
         f' fill="#5b4428" {o(4)}/>')
    cols = ["#9c3a2a", "#6f8c4a", "#c9a331", "#8a4a5c", "#4e7a3c"]
    for i in range(n):
        bx = x + 44 + i * (w_ - 88) / max(1, n - 1.0)
        bh = rnd.uniform(118, 158)
        bw = rnd.uniform(66, 86)
        s += (f'<rect x="{bx-bw/2:.0f}" y="{y-bh:.0f}" width="{bw:.0f}"'
              f' height="{bh:.0f}" rx="10" fill="url(#stekl)" opacity=".88" {o(5)}/>'
              f'<rect x="{bx-bw/2+7:.0f}" y="{y-bh*.70:.0f}" width="{bw-14:.0f}"'
              f' height="{bh*.64:.0f}" rx="7" fill="{cols[i % 5]}" opacity=".92"/>'
              f'<rect x="{bx-bw/2-5:.0f}" y="{y-bh-16:.0f}" width="{bw+10:.0f}"'
              f' height="20" rx="7" fill="{ZHELEZ}" {o(4)}/>'
              f'<path d="M{bx-bw*.30:.0f},{y-bh*.86:.0f} q{bw*.08:.0f},{bh*.34:.0f}'
              f' {0:.0f},{bh*.62:.0f}" fill="none" stroke="#ffffff"'
              f' stroke-width="7" opacity="{.22+.18*abs(A.w(t,2.6,i*.3)):.2f}"/>')
    s += (f'<path d="M{x+w_-30:.0f},{y-26:.0f} q{-40:.0f},{-30:.0f} {-74:.0f},{-6:.0f}"'
          f' fill="none" stroke="#cfd6de" stroke-width="3" opacity=".4"/>')
    return s


def _naves_polosatyy(x, y, w_, t, h_=120, seed=5):
    """Полосатый навес рынка: зубчатый подзор, красно-белые полосы, две
    стойки с растяжками. Колышется волной, а не целиком."""
    s = (f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_*.56:.0f}"'
         f' rx="10" fill="#efe8d8" {o(6)}/>')
    n = int(w_ / 86)
    for i in range(n):
        if i % 2 == 0:
            s += (f'<rect x="{x+i*86:.0f}" y="{y-h_:.0f}" width="86"'
                  f' height="{h_*.56:.0f}" fill="{TKAN}" opacity=".92"/>')
    for i in range(n):
        kol = 10 * math.sin(t * 1.6 + i * .7)
        s += (f'<path d="M{x+i*86:.0f},{y-h_*.44:.0f} q{43:.0f},{54+kol:.0f}'
              f' {86:.0f},0 Z" fill="{TKAN if i % 2 == 0 else "#efe8d8"}" {o(4)}/>')
    for sx in (x + 26, x + w_ - 26):
        s += (f'<rect x="{sx-10:.0f}" y="{y-h_:.0f}" width="20" height="{h_+130:.0f}"'
              f' rx="8" fill="{ZHELEZ}" {o(4)}/>')
    s += (f'<line x1="{x+30:.0f}" y1="{y-h_+10:.0f}" x2="{x+w_-30:.0f}"'
          f' y2="{y-h_+10:.0f}" stroke="#6f767c" stroke-width="7"/>')
    return s


def _cenniki_bez_cifr(x, y, n=4, t=0.0, seed=3):
    """Ценники на спицах: картонка с волнистой строкой вместо букв и цифр
    (своих букв в декорации не рисуем — ряд палочек читается надписью)."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        cx = x + i * 112
        ug = 4.0 * A.w(t, 2.8, i * .4)
        s += (f'<g transform="rotate({ug:.1f} {cx:.0f} {y:.0f})">'
              f'<line x1="{cx:.0f}" y1="{y:.0f}" x2="{cx:.0f}" y2="{y-62:.0f}"'
              f' stroke="{ZHELEZ}" stroke-width="6"/>'
              f'<rect x="{cx-40:.0f}" y="{y-116:.0f}" width="80" height="56"'
              f' rx="7" fill="#f4eedc" {o(4)}/>')
        for j in range(2):
            s += (f'<path d="M{cx-28:.0f},{y-98+j*22:.0f} q{14:.0f},{-8:.0f}'
                  f' {28:.0f},0 q{14:.0f},{8:.0f} {28:.0f},0" fill="none"'
                  f' stroke="#8a7a5c" stroke-width="5"/>')
        s += "</g>"
    return s


def _puchki_zeleni(x, y, w_, t, seed=7, n=4):
    """Пучки зелени, перевязанные нитью: перья лука и укроп веером."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        px = x + i * (w_ / max(1, n - 1.0))
        sway = 3.4 * A.w(t, 2.4, i * .5)
        s += f'<g transform="rotate({sway:.1f} {px:.0f} {y:.0f})">'
        for j in range(7):
            a = math.radians(-152 + j * 24 + rnd.uniform(-6, 6))
            dl = rnd.uniform(86, 136)
            s += (f'<path d="M{px:.0f},{y:.0f} Q{px+dl*.6*math.cos(a):.0f},'
                  f'{y+dl*.6*math.sin(a)-14:.0f} {px+dl*math.cos(a):.0f},'
                  f'{y+dl*math.sin(a):.0f}" fill="none" stroke="#4e7a3c"'
                  f' stroke-width="{rnd.uniform(6,11):.0f}" stroke-linecap="round"/>')
        s += (f'<rect x="{px-18:.0f}" y="{y-16:.0f}" width="36" height="22"'
              f' rx="8" fill="#b8a86a" {o(3)}/>'
              f'<line x1="{px-18:.0f}" y1="{y-5:.0f}" x2="{px+18:.0f}"'
              f' y2="{y-5:.0f}" stroke="#8a7a46" stroke-width="5"/></g>')
    return s


def _svekla(x, y, s_=1.0, t=0.0, ph=.0):
    """Свёкла: бордовый шар с пояском, хвостик и две ножки ботвы."""
    r = 48 * s_
    s = (f'{ten(x, y + r * .80, r * .86, r * .18, .4)}'
         f'<path d="M{x-r:.0f},{y-r*.20:.0f} q{r*.08:.0f},{-r*.82:.0f}'
         f' {r*1.0:.0f},{-r*.76:.0f} q{r*.92:.0f},{-r*.06:.0f} {r*1.0:.0f},{r*.76:.0f}'
         f' q{r*.04:.0f},{r*.92:.0f} {-r*1.0:.0f},{r*.94:.0f}'
         f' q{-r*1.04:.0f},{-r*.02:.0f} {-r*1.0:.0f},{-r*.94:.0f} Z"'
         f' fill="#7a2338" {o(5)}/>'
         f'<path d="M{x-r*.80:.0f},{y-r*.10:.0f} q{r*.80:.0f},{r*.26:.0f}'
         f' {r*1.60:.0f},0" fill="none" stroke="#5a1626" stroke-width="{6*s_:.0f}"'
         f' opacity=".7"/>'
         f'<ellipse cx="{x-r*.32:.0f}" cy="{y-r*.42:.0f}" rx="{r*.22:.0f}"'
         f' ry="{r*.12:.0f}" fill="#b05a74" opacity=".45"/>'
         f'<path d="M{x+r*.12:.0f},{y+r*.86:.0f} q{r*.16:.0f},{r*.40:.0f}'
         f' {-r*.04:.0f},{r*.62:.0f}" fill="none" stroke="#8a4a5c"'
         f' stroke-width="{max(2,5*s_):.0f}" stroke-linecap="round"/>')
    sway = 4.0 * A.w(t, 2.3, ph)
    s += f'<g transform="rotate({sway:.1f} {x:.0f} {y-r*.80:.0f})">'
    for i in (-1, 1):
        s += (f'<path d="M{x+i*r*.16:.0f},{y-r*.80:.0f}'
              f' Q{x+i*r*.56:.0f},{y-r*1.56:.0f} {x+i*r*.30:.0f},{y-r*2.00:.0f}'
              f' Q{x+i*r*.06:.0f},{y-r*1.50:.0f} {x+i*r*.16:.0f},{y-r*.80:.0f} Z"'
              f' fill="#4e5a2c" {o(4)}/>'
              f'<line x1="{x+i*r*.16:.0f}" y1="{y-r*.80:.0f}"'
              f' x2="{x+i*r*.30:.0f}" y2="{y-r*1.96:.0f}" stroke="#9c3a2a"'
              f' stroke-width="{max(2,5*s_):.0f}"/>')
    return s + "</g>"


def _kapusta(x, y, s_=1.0, t=0.0):
    """Кочан капусты: плотная голова, отогнутые верхние листья с
    прожилками, срез кочерыжки внизу."""
    r = 62 * s_
    s = (f'{ten(x, y + r * .72, r * .96, r * .20, .45)}'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#b8c99a" {o(6)}/>')
    for i in range(4):
        s += (f'<path d="M{x-r*.80+i*r*.18:.0f},{y-r*.70:.0f}'
              f' q{r*.28:.0f},{r*.70:.0f} {r*.04:.0f},{r*1.44:.0f}" fill="none"'
              f' stroke="#8fa36e" stroke-width="{max(3,7*s_):.0f}" opacity=".8"/>')
    for i in (-1, 1):
        sway = 3.0 * A.w(t, 2.7, .2 + (0 if i < 0 else .4))
        s += (f'<g transform="rotate({sway*i:.1f} {x:.0f} {y+r*.4:.0f})">'
              f'<path d="M{x+i*r*.56:.0f},{y+r*.30:.0f}'
              f' Q{x+i*r*1.30:.0f},{y-r*.20:.0f} {x+i*r*1.12:.0f},{y+r*.60:.0f}'
              f' Q{x+i*r*.80:.0f},{y+r*.84:.0f} {x+i*r*.56:.0f},{y+r*.30:.0f} Z"'
              f' fill="#9cb47a" {o(4)}/>'
              f'<line x1="{x+i*r*.60:.0f}" y1="{y+r*.36:.0f}"'
              f' x2="{x+i*r*1.08:.0f}" y2="{y+r*.56:.0f}" stroke="#e2ecd0"'
              f' stroke-width="{max(2,5*s_):.0f}" opacity=".8"/></g>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y+r*.86:.0f}" rx="{r*.20:.0f}"'
          f' ry="{r*.10:.0f}" fill="#efe8d8" {o(3)}/>')
    return s


def _glubokaya_miska(x, y, s_=1.0, t=0.0, napoln=.0):
    """Глубокая миска под тёркой: высокий борт с поливой, в ней горка белой
    стружки редьки, которая растёт по ходу сцены."""
    r = 112 * s_
    s = (f'{ten(x, y + r * .22, r * 1.0, r * .20, .5)}'
         f'<path d="M{x-r:.0f},{y-r*.56:.0f} q{r*.10:.0f},{r*.98:.0f}'
         f' {r*1.0:.0f},{r*.98:.0f} q{r*.90:.0f},0 {r*1.0:.0f},{-r*.98:.0f} Z"'
         f' fill="#e7edf0" {o(7)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-r*.56:.0f}" rx="{r:.0f}" ry="{r*.28:.0f}"'
         f' fill="#cfd8dc" {o(5)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-r*.54:.0f}" rx="{r*.86:.0f}"'
         f' ry="{r*.22:.0f}" fill="#b9c6cc" opacity=".9"/>'
         f'<rect x="{x-r*.96:.0f}" y="{y-r*.26:.0f}" width="{r*1.92:.0f}"'
         f' height="{r*.12:.0f}" fill="{TKAN2}" opacity=".65"/>')
    rnd = random.Random(int(x) + 29)
    m = int(4 + 16 * napoln)
    for i in range(m):
        a = rnd.uniform(0, 6.28)
        rr = rnd.uniform(.1, .86)
        px = x + math.cos(a) * r * .74 * rr
        py = y - r * .52 - abs(math.sin(a)) * r * .20 * rr - napoln * 14
        s += (f'<path d="M{px-22:.0f},{py:.0f} q{22:.0f},{-9:.0f} {44:.0f},{2:.0f}"'
              f' fill="none" stroke="#f8f6ee" stroke-width="{rnd.uniform(6,11):.0f}"'
              f' stroke-linecap="round"/>')
    s += (f'<path d="M{x-r*.70:.0f},{y+r*.18:.0f} q{r*.30:.0f},{r*.22:.0f}'
          f' {r*.66:.0f},{r*.10:.0f}" fill="none" stroke="#ffffff"'
          f' stroke-width="{9*s_:.0f}" opacity=".4"/>')
    return s


def _struzhka_letit(x, y, t, n=8, seed=5, R=130):
    """Стружка редьки падает с тёрки в миску: белые завитки, часть с тёмной
    кожурой по кромке."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        p = ((t * 1.1 + i / float(n)) % 1.0)
        px = x + rnd.uniform(-34, 34) + 16 * math.sin(p * 5 + i)
        py = y + p * R
        ug = rnd.uniform(-40, 40) + p * 90
        s += (f'<g transform="rotate({ug:.0f} {px:.0f} {py:.0f})">'
              f'<path d="M{px-18:.0f},{py:.0f} q{18:.0f},{-11:.0f} {36:.0f},{2:.0f}"'
              f' fill="none" stroke="#f8f6ee" stroke-width="9"'
              f' stroke-linecap="round" opacity="{1-p*.5:.2f}"/>'
              f'<path d="M{px-16:.0f},{py+5:.0f} q{16:.0f},{-9:.0f} {32:.0f},{2:.0f}"'
              f' fill="none" stroke="#5a5450" stroke-width="3" opacity="{.7-p*.4:.2f}"/>'
              f'</g>')
    return s


def _solonka(x, y, s_=1.0, t=0.0, tryaska=.0):
    """Солонка-деревянный шалашик с крышечкой и щепоткой соли, которая
    сыплется, когда её трясут."""
    ug = 9.0 * tryaska * A.w(t, 9.0, .1)
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'{ten(x, y + 6 * s_, 40 * s_, 10 * s_, .4)}'
         f'<path d="M{x-36*s_:.0f},{y:.0f} L{x+36*s_:.0f},{y:.0f}'
         f' L{x+28*s_:.0f},{y-64*s_:.0f} L{x-28*s_:.0f},{y-64*s_:.0f} Z"'
         f' fill="url(#derev)" {o(5)}/>'
         f'<path d="M{x-34*s_:.0f},{y-64*s_:.0f} L{x:.0f},{y-98*s_:.0f}'
         f' L{x+34*s_:.0f},{y-64*s_:.0f} Z" fill="#9c7049" {o(4)}/>'
         f'<circle cx="{x:.0f}" cy="{y-100*s_:.0f}" r="{8*s_:.0f}"'
         f' fill="#7d5636" {o(3)}/>'
         f'<rect x="{x-30*s_:.0f}" y="{y-40*s_:.0f}" width="{60*s_:.0f}"'
         f' height="{10*s_:.0f}" fill="#8a6038" opacity=".8"/></g>')
    if tryaska > .05:
        rnd = random.Random(31)
        for i in range(9):
            p = ((t * 1.6 + i / 9.0) % 1.0)
            s += (f'<circle cx="{x+rnd.uniform(-20,20):.0f}"'
                  f' cy="{y+10*s_+p*120:.0f}" r="{rnd.uniform(2.5,4.5):.0f}"'
                  f' fill="#ffffff" opacity="{(1-p)*tryaska:.2f}"/>')
    return s


def _blyudce(x, y, s_=1.0, sok=.0, t=0.0):
    """Блюдце с бортиком и кольцом дна; по мере сцены в нём набегает
    янтарный сок с бликом."""
    r = 96 * s_
    s = (f'{ten(x, y + r * .20, r * 1.0, r * .18, .45)}'
         f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r*.30:.0f}"'
         f' fill="#eef2f4" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-2*s_:.0f}" rx="{r*.80:.0f}"'
         f' ry="{r*.22:.0f}" fill="#dde6ea" {o(4)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y+r*.12:.0f}" rx="{r*.44:.0f}"'
         f' ry="{r*.11:.0f}" fill="#e7edf0" opacity=".9"/>')
    if sok > .02:
        s += (f'<ellipse cx="{x:.0f}" cy="{y-1*s_:.0f}" rx="{r*(.46+.32*sok):.0f}"'
              f' ry="{r*(.13+.08*sok):.0f}" fill="#d6a63f" opacity=".95"/>'
              f'<ellipse cx="{x-r*.20:.0f}" cy="{y-r*.05:.0f}"'
              f' rx="{r*.18*sok:.0f}" ry="{r*.05*sok:.0f}" fill="#f2d78a"'
              f' opacity="{.5+.3*abs(A.w(t,2.2,.2)):.2f}"/>')
    s += (f'<path d="M{x-r*.74:.0f},{y-r*.10:.0f} q{r*.30:.0f},{-r*.16:.0f}'
          f' {r*.62:.0f},{-r*.04:.0f}" fill="none" stroke="#ffffff"'
          f' stroke-width="{8*s_:.0f}" opacity=".5"/>')
    return s


def _redka_s_yamkoy(x, y, s_=1.0, t=0.0, yamka=.0, med=.0):
    """Чёрная редька на блюдце с СРЕЗАННОЙ ВЕРХУШКОЙ-крышечкой: в тулове
    выбрана ямка, в ямку кладут мёд. Сам корень берём готовым (`_redka`),
    чтобы один предмет не рисовать дважды; здесь — срез, ямка и мёд."""
    r = 86 * s_
    s = _redka(x, y, s_, t, 0.0, .18, "#2e2b2a")
    s += (f'<ellipse cx="{x:.0f}" cy="{y-r*.86:.0f}" rx="{r*.62:.0f}"'
          f' ry="{r*.20:.0f}" fill="#4a4644" {o(5)}/>'
          f'<ellipse cx="{x:.0f}" cy="{y-r*.88:.0f}" rx="{r*.52:.0f}"'
          f' ry="{r*.15:.0f}" fill="#efe8d8" opacity=".95"/>')
    gl = r * (.10 + .34 * yamka)
    s += (f'<ellipse cx="{x:.0f}" cy="{y-r*.84:.0f}" rx="{r*(.20+.20*yamka):.0f}"'
          f' ry="{gl*.42:.0f}" fill="#2b2826" opacity=".95"/>')
    if med > .02:
        s += (f'<ellipse cx="{x:.0f}" cy="{y-r*.82:.0f}"'
              f' rx="{r*(.16+.18*yamka)*med:.0f}" ry="{gl*.34*med:.0f}"'
              f' fill="{ZOL}" opacity=".95"/>'
              f'<ellipse cx="{x-r*.08:.0f}" cy="{y-r*.84:.0f}" rx="{r*.07*med:.0f}"'
              f' ry="{r*.03*med:.0f}" fill="#f6e2a0" opacity=".8"/>')
    # СРЕЗАННАЯ ВЕРХУШКА лежит рядом крышечкой, срезом вверх
    s += (f'<g transform="rotate(-14 {x+r*1.40:.0f} {y+r*.20:.0f})">'
          f'{ten(x + r * 1.40, y + r * .38, r * .52, r * .14, .4)}'
          f'<path d="M{x+r*.94:.0f},{y+r*.20:.0f} q{r*.46:.0f},{-r*.52:.0f}'
          f' {r*.92:.0f},0 q{-r*.46:.0f},{r*.26:.0f} {-r*.92:.0f},0 Z"'
          f' fill="#2e2b2a" {o(5)}/>'
          f'<ellipse cx="{x+r*1.40:.0f}" cy="{y+r*.20:.0f}" rx="{r*.46:.0f}"'
          f' ry="{r*.12:.0f}" fill="#efe8d8" opacity=".9"/></g>')
    return s


def _banka_meda(x, y, s_=1.0, t=0.0, lozhka=True):
    """Банка мёда: стекло, густой мёд с медленной волной, жестяная крышка
    рядом, ложка с тянущейся струйкой."""
    w2, h2 = 92 * s_, 136 * s_
    s = (f'{ten(x, y + 8 * s_, w2 * .56, 12 * s_, .45)}'
         f'<rect x="{x-w2/2:.0f}" y="{y-h2:.0f}" width="{w2:.0f}" height="{h2:.0f}"'
         f' rx="12" fill="url(#stekl)" opacity=".9" {o(6)}/>'
         f'<path d="M{x-w2/2+8:.0f},{y-h2*.70:.0f}'
         f' q{w2*.24:.0f},{-10 - 6 * A.w(t, 3.0, .2):.0f} {w2*.46:.0f},0'
         f' q{w2*.24:.0f},{10:.0f} {w2*.38:.0f},{-2:.0f} L{x+w2/2-8:.0f},{y-10:.0f}'
         f' L{x-w2/2+8:.0f},{y-10:.0f} Z" fill="{ZOL}" opacity=".95"/>'
         f'<rect x="{x-w2/2-6:.0f}" y="{y-h2-18:.0f}" width="{w2+12:.0f}"'
         f' height="24" rx="9" fill="{ZHELEZ}" {o(4)}/>'
         f'<path d="M{x-w2*.28:.0f},{y-h2*.86:.0f} q{w2*.06:.0f},{h2*.30:.0f}'
         f' {0:.0f},{h2*.56:.0f}" fill="none" stroke="#ffffff" stroke-width="8"'
         f' opacity=".3"/>')
    if lozhka:
        kap = (t * .55) % 1.0
        s += (f'<g transform="rotate(26 {x+w2*.84:.0f} {y-h2*.86:.0f})">'
              f'<ellipse cx="{x+w2*.84:.0f}" cy="{y-h2*.86:.0f}" rx="{30*s_:.0f}"'
              f' ry="{20*s_:.0f}" fill="#cfd8dc" {o(4)}/>'
              f'<rect x="{x+w2*.84-7:.0f}" y="{y-h2*.86:.0f}" width="{14*s_:.0f}"'
              f' height="{96*s_:.0f}" rx="6" fill="#b9c6cc" {o(3)}/></g>'
              f'<path d="M{x+w2*.70:.0f},{y-h2*.76:.0f} q{6:.0f},{40+40*kap:.0f}'
              f' {-2:.0f},{70+50*kap:.0f}" fill="none" stroke="{ZOL}"'
              f' stroke-width="{13-5*kap:.0f}" stroke-linecap="round"/>')
    return s


def _nozh(x, y, s_=1.0, ug=0.0):
    """Нож: клинок с обушком и светлой фаской, деревянная рукоять с
    заклёпками."""
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'{ten(x + 40 * s_, y + 8 * s_, 90 * s_, 8 * s_, .35)}'
            f'<path d="M{x:.0f},{y:.0f} L{x+156*s_:.0f},{y-10*s_:.0f}'
            f' L{x+162*s_:.0f},{y+2*s_:.0f} L{x:.0f},{y+16*s_:.0f} Z"'
            f' fill="#c9d2d8" {o(4)}/>'
            f'<path d="M{x+6*s_:.0f},{y+2*s_:.0f} L{x+150*s_:.0f},{y-6*s_:.0f}"'
            f' fill="none" stroke="#ffffff" stroke-width="{4*s_:.0f}" opacity=".6"/>'
            f'<rect x="{x-86*s_:.0f}" y="{y-4*s_:.0f}" width="{88*s_:.0f}"'
            f' height="{26*s_:.0f}" rx="{9*s_:.0f}" fill="#7d5636" {o(4)}/>'
            f'<circle cx="{x-62*s_:.0f}" cy="{y+9*s_:.0f}" r="{4*s_:.0f}"'
            f' fill="#9aa3aa"/>'
            f'<circle cx="{x-24*s_:.0f}" cy="{y+9*s_:.0f}" r="{4*s_:.0f}"'
            f' fill="#9aa3aa"/></g>')


def _batareya_s_noskom(x, y, w_, t, nosok=True, seed=3):
    """Чугунная батарея под подоконником: секции с перехватами, вентиль,
    на ней шерстяной носок, над ней дрожит тёплый воздух."""
    n = int(w_ / 46)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="26" rx="8"'
         f' fill="#b6bcc2" {o(5)}/>'
         f'<rect x="{x:.0f}" y="{y+150:.0f}" width="{w_:.0f}" height="26" rx="8"'
         f' fill="#b6bcc2" {o(5)}/>')
    for i in range(n):
        bx = x + 8 + i * 46
        s += (f'<rect x="{bx:.0f}" y="{y+18:.0f}" width="30" height="138" rx="13"'
              f' fill="#cfd5da" {o(4)}/>'
              f'<rect x="{bx+6:.0f}" y="{y+30:.0f}" width="9" height="112" rx="4"'
              f' fill="#eef2f4" opacity=".7"/>')
    s += (f'<circle cx="{x+w_+12:.0f}" cy="{y+22:.0f}" r="20" fill="{ZHELEZ}" {o(4)}/>'
          f'<rect x="{x+w_-4:.0f}" y="{y+16:.0f}" width="30" height="14" rx="6"'
          f' fill="#8f979d"/>')
    if nosok:
        kach = 2.4 * A.w(t, 3.2, .3)
        s += (f'<g transform="rotate({kach:.1f} {x+w_*.42:.0f} {y+10:.0f})">'
              f'<path d="M{x+w_*.30:.0f},{y-6:.0f} L{x+w_*.54:.0f},{y-6:.0f}'
              f' L{x+w_*.56:.0f},{y+96:.0f} Q{x+w_*.56:.0f},{y+128:.0f}'
              f' {x+w_*.74:.0f},{y+128:.0f} L{x+w_*.76:.0f},{y+154:.0f}'
              f' L{x+w_*.30:.0f},{y+150:.0f} Z" fill="#b8323a" {o(5)}/>'
              f'<rect x="{x+w_*.30:.0f}" y="{y-8:.0f}" width="{w_*.25:.0f}"'
              f' height="24" rx="8" fill="#efe3c8" opacity=".9"/>'
              + "".join(f'<line x1="{x+w_*.32+i*14:.0f}" y1="{y+20:.0f}"'
                        f' x2="{x+w_*.33+i*14:.0f}" y2="{y+140:.0f}"'
                        f' stroke="#9c2a32" stroke-width="4" opacity=".7"/>'
                        for i in range(6))
              + "</g>")
    s += vozduh(x + w_ * .5, y + 40, t, 420, .1)
    return s


def _mishka_plyush(x, y, s_=1.0, t=0.0, szhat=.0):
    """Плюшевый мишка: голова с круглыми ушами, мордочка со швом, лапы в
    стороны, на шее лоскут. Когда его сжимают, лапы прижимаются к тулову."""
    r = 44 * s_
    pr = 1.0 - .34 * szhat
    s = (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r*1.10:.0f}" ry="{r*1.26:.0f}"'
         f' fill="#a87a4a" {o(5)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y+r*.26:.0f}" rx="{r*.68:.0f}"'
         f' ry="{r*.78:.0f}" fill="#c99c68" opacity=".9"/>')
    for i in (-1, 1):
        s += (f'<ellipse cx="{x+i*r*1.26*pr:.0f}" cy="{y+r*.10:.0f}"'
              f' rx="{r*.40:.0f}" ry="{r*.26:.0f}" fill="#a87a4a" {o(4)}/>'
              f'<ellipse cx="{x+i*r*.56:.0f}" cy="{y+r*1.34:.0f}"'
              f' rx="{r*.34:.0f}" ry="{r*.42:.0f}" fill="#a87a4a" {o(4)}/>')
    s += (f'<circle cx="{x:.0f}" cy="{y-r*1.42:.0f}" r="{r*.76:.0f}"'
          f' fill="#a87a4a" {o(5)}/>')
    for i in (-1, 1):
        s += (f'<circle cx="{x+i*r*.62:.0f}" cy="{y-r*1.96:.0f}" r="{r*.26:.0f}"'
              f' fill="#8a6038" {o(4)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-r*1.22:.0f}" rx="{r*.40:.0f}"'
          f' ry="{r*.30:.0f}" fill="#e2c898" opacity=".95"/>'
          f'<ellipse cx="{x:.0f}" cy="{y-r*1.26:.0f}" rx="{r*.12:.0f}"'
          f' ry="{r*.09:.0f}" fill="{K}"/>'
          f'<circle cx="{x-r*.26:.0f}" cy="{y-r*1.58:.0f}" r="{r*.09:.0f}" fill="{K}"/>'
          f'<circle cx="{x+r*.26:.0f}" cy="{y-r*1.58:.0f}" r="{r*.09:.0f}" fill="{K}"/>'
          f'<path d="M{x:.0f},{y-r*1.16:.0f} q{r*.14:.0f},{r*.16:.0f}'
          f' {r*.26:.0f},{r*.02:.0f}" fill="none" stroke="{K}"'
          f' stroke-width="{max(2,3.4*s_):.0f}"/>'
          f'<path d="M{x-r*.90:.0f},{y-r*.76:.0f} q{r*.90:.0f},{r*.26:.0f}'
          f' {r*1.80:.0f},0" fill="none" stroke="{TKAN}"'
          f' stroke-width="{max(4,11*s_):.0f}"/>')
    return s


def _tumbochka_veschi(x, y, w_, t, h_=190):
    """Тумбочка у кровати и что на ней: градусник в стакане, стакан воды с
    блеском, книжка с закладкой, пузырёк. Ящик с ручкой-скобой."""
    s = (f'{ten(x + w_ * .5, y + 8, w_ * .54, 16, .5)}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="10" fill="url(#dosk)" {o(7)}/>'
         f'<rect x="{x+12:.0f}" y="{y-h_+16:.0f}" width="{w_-24:.0f}" height="58"'
         f' rx="7" fill="#8a6038" {o(4)}/>'
         f'<rect x="{x+w_*.36:.0f}" y="{y-h_+40:.0f}" width="{w_*.28:.0f}"'
         f' height="12" rx="6" fill="{ZHELEZ}" {o(3)}/>'
         f'<rect x="{x-10:.0f}" y="{y-h_-14:.0f}" width="{w_+20:.0f}" height="18"'
         f' rx="7" fill="#9c7049" {o(5)}/>')
    gx = x + w_ * .24
    s += (f'<path d="M{gx-26:.0f},{y-h_-14:.0f} L{gx+26:.0f},{y-h_-14:.0f}'
          f' L{gx+20:.0f},{y-h_-94:.0f} L{gx-20:.0f},{y-h_-94:.0f} Z"'
          f' fill="url(#stekl)" opacity=".86" {o(4)}/>'
          f'<path d="M{gx-18:.0f},{y-h_-20:.0f} L{gx+18:.0f},{y-h_-20:.0f}'
          f' L{gx+15:.0f},{y-h_-64:.0f} L{gx-15:.0f},{y-h_-64:.0f} Z"'
          f' fill="{VODA}" opacity=".55"/>'
          f'<line x1="{gx+6:.0f}" y1="{y-h_-20:.0f}" x2="{gx+16:.0f}"'
          f' y2="{y-h_-116:.0f}" stroke="#eef2f4" stroke-width="8"/>'
          f'<circle cx="{gx+16:.0f}" cy="{y-h_-118:.0f}" r="6" fill="#d6452a"/>'
          f'<path d="M{gx-14:.0f},{y-h_-30:.0f} q{6:.0f},{-20:.0f} {2:.0f},{-34:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="5"'
          f' opacity="{.3+.25*abs(A.w(t,2.4,.2)):.2f}"/>')
    kx = x + w_ * .70
    s += (f'<path d="M{kx-54:.0f},{y-h_-16:.0f} L{kx+54:.0f},{y-h_-16:.0f}'
          f' L{kx+54:.0f},{y-h_-44:.0f} L{kx-54:.0f},{y-h_-38:.0f} Z"'
          f' fill="#8a4a5c" {o(4)}/>'
          f'<rect x="{kx-50:.0f}" y="{y-h_-38:.0f}" width="100" height="8"'
          f' fill="#efe8d8"/>'
          f'<rect x="{kx+18:.0f}" y="{y-h_-44:.0f}" width="14" height="42"'
          f' rx="4" fill="{ZOL}" {o(3)}/>')
    s += (f'<rect x="{x+w_*.50:.0f}" y="{y-h_-62:.0f}" width="34" height="46"'
          f' rx="8" fill="#6f8c4a" opacity=".9" {o(3)}/>')
    return s


def _odeyalo_kray(x, y, w_, h_, t, scep=.0, col=TKAN2):
    """Край одеяла, в который вцепились руками: лоскутные квадраты, светлая
    подкладка отворотом и две складки, которые стягиваются при хвате."""
    rnd = random.Random(53)
    sg = 16 * scep
    s = (f'<path d="M{x:.0f},{y:.0f} Q{x+w_*.5:.0f},{y-26-sg:.0f} {x+w_:.0f},{y:.0f}'
         f' L{x+w_:.0f},{y+h_:.0f} L{x:.0f},{y+h_:.0f} Z" fill="{col}" {o(7)}/>')
    for r in range(3):
        for c in range(int(w_ / 120)):
            if (r + c) % 2:
                continue
            s += (f'<rect x="{x+10+c*120:.0f}" y="{y+30+r*110:.0f}" width="108"'
                  f' height="98" rx="8" fill="#5a7a9c" opacity=".55"/>')
    s += (f'<path d="M{x:.0f},{y:.0f} Q{x+w_*.5:.0f},{y-26-sg:.0f} {x+w_:.0f},{y:.0f}'
          f' L{x+w_:.0f},{y+34:.0f} Q{x+w_*.5:.0f},{y+8-sg:.0f} {x:.0f},{y+34:.0f} Z"'
          f' fill="{KREM}" {o(5)}/>')
    for i in range(4):
        px = x + w_ * (.18 + i * .22)
        s += (f'<path d="M{px:.0f},{y+18:.0f} q{10 + sg:.0f},{h_*.4:.0f}'
              f' {-4:.0f},{h_*.8:.0f}" fill="none" stroke="#2f4a66"'
              f' stroke-width="8" opacity=".6"/>')
    return s


def _banya_srub(x, base, w_, t, seed=7, dver=.0):
    """БАНЬКА НА ОГОРОДЕ — главный предмет: низкий сруб в пять венцов,
    двускатная крыша с тёсом и снегом, кирпичная труба с дымом, стреха с
    вениками, маленькое окошко с тёплым светом, дверь на пяте."""
    rnd = random.Random(seed)
    h_ = w_ * .74
    s = (f'{ten(x + w_ * .5, base + 12, w_ * .56, 26, .5)}'
         f'<rect x="{x:.0f}" y="{base-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' fill="url(#brev)" {o(8)}/>')
    for i in range(6):
        yy = base - h_ + 18 + i * (h_ - 20) / 6.0
        s += (f'<rect x="{x:.0f}" y="{yy:.0f}" width="{w_:.0f}" height="{(h_-20)/6.0-6:.0f}"'
              f' rx="14" fill="{BREVNO if i % 2 == 0 else BREVNO2}" {o(5)}/>'
              f'<path d="M{x+16:.0f},{yy+(h_-20)/9.0:.0f} q{w_*.44:.0f},{8:.0f}'
              f' {w_-32:.0f},0" fill="none" stroke="#a97a4e" stroke-width="5"'
              f' opacity=".55"/>')
    # крыша
    s += (f'<path d="M{x-40:.0f},{base-h_+10:.0f} L{x+w_*.5:.0f},{base-h_-170:.0f}'
          f' L{x+w_+40:.0f},{base-h_+10:.0f} Z" fill="#6b5340" {o(7)}/>'
          f'<path d="M{x-40:.0f},{base-h_+10:.0f} L{x+w_*.5:.0f},{base-h_-170:.0f}'
          f' L{x+w_*.5:.0f},{base-h_-140:.0f} L{x-10:.0f},{base-h_+4:.0f} Z"'
          f' fill="{SNEG}" opacity=".92"/>')
    for i in range(7):
        s += (f'<line x1="{x-30+i*(w_+50)/7.0:.0f}" y1="{base-h_+8:.0f}"'
              f' x2="{x+w_*.5:.0f}" y2="{base-h_-166:.0f}" stroke="#4e3c2c"'
              f' stroke-width="5" opacity=".6"/>')
    # труба с дымом
    tx = x + w_ * .70
    s += (f'<rect x="{tx:.0f}" y="{base-h_-230:.0f}" width="76" height="120"'
          f' rx="6" fill="{KAMEN}" {o(5)}/>'
          + kladka(tx, base - h_ - 230, 76, 120, 34, KAMEN)
          + f'<rect x="{tx-12:.0f}" y="{base-h_-244:.0f}" width="100" height="22"'
            f' rx="7" fill="{KAMEN2}" {o(4)}/>')
    s += dym(tx + 38, base - h_ - 252, t, 6, .30, 340, .42, "#d6dde4", 1.5)
    # окошко с тёплым светом
    ox = x + w_ * .20
    s += (f'<rect x="{ox:.0f}" y="{base-h_*.74:.0f}" width="120" height="104"'
          f' rx="8" fill="#2a1d12" {o(6)}/>'
          f'<rect x="{ox+8:.0f}" y="{base-h_*.74+8:.0f}" width="104" height="88"'
          f' fill="{SVET}" opacity="{.74+.16*abs(A.w(t,2.4,.3)):.2f}"/>'
          f'<line x1="{ox+60:.0f}" y1="{base-h_*.74:.0f}" x2="{ox+60:.0f}"'
          f' y2="{base-h_*.74+104:.0f}" stroke="#4e3c2c" stroke-width="9"/>'
          f'<rect x="{ox-14:.0f}" y="{base-h_*.74-22:.0f}" width="148" height="20"'
          f' rx="7" fill="#7d5636" {o(4)}/>')
    # веники под стрехой
    for i in range(4):
        vx = x + w_ * .40 + i * 58
        s += _venik(vx, base - h_ - 36, 150, t, "#b8a86a", "#5a4a2e", False,
                    .10, i * .3, .52, 71 + i)
    s += (f'<rect x="{x+w_*.34:.0f}" y="{base-h_-58:.0f}" width="260" height="14"'
          f' rx="6" fill="{ZHELEZ}" {o(3)}/>')
    return s


def _hvor(x, y, s_=1.0, t=0.0, ph=.0, beg=.0):
    """ХВОРЬ — серый комок с красным носом, тремя космами, кривыми ножками
    и кислой гримасой: выкатывается из бани и убегает в сугроб. Не человек и
    не лицо в горе — рисованная нежить, по образцу комка радости из порции 2,
    но своя: серая, с носом и ножками."""
    r = 38 * s_
    pryg = abs(math.sin(t * 5.0 + ph)) * 16 * s_ * (0.3 + beg)
    s = (f'<g transform="translate({beg * 240 * s_:.0f},{-pryg:.0f})">'
         f'{ten(x, y + r * .36 + pryg, r * .86, r * .18, .4)}'
         f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r*.88:.0f}"'
         f' fill="#8d939a" {o(5)}/>'
         f'<ellipse cx="{x-r*.26:.0f}" cy="{y-r*.26:.0f}" rx="{r*.26:.0f}"'
         f' ry="{r*.18:.0f}" fill="#aab1b8" opacity=".6"/>')
    for i in (-1, 0, 1):
        s += (f'<path d="M{x+i*r*.30:.0f},{y-r*.82:.0f} q{i*r*.20:.0f},{-r*.44:.0f}'
              f' {i*r*.44:.0f},{-r*.30:.0f}" fill="none" stroke="#6f767c"'
              f' stroke-width="{max(3,7*s_):.0f}" stroke-linecap="round"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*r*.40:.0f},{y+r*.72:.0f} q{i*r*.24:.0f},{r*.30:.0f}'
              f' {i*r*.10:.0f},{r*.52:.0f}" fill="none" stroke="#6f767c"'
              f' stroke-width="{max(4,9*s_):.0f}" stroke-linecap="round"/>'
              f'<ellipse cx="{x+i*r*.50:.0f}" cy="{y+r*1.26:.0f}" rx="{r*.20:.0f}"'
              f' ry="{r*.10:.0f}" fill="#5b6168" {o(3)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y+r*.06:.0f}" rx="{r*.22:.0f}"'
          f' ry="{r*.18:.0f}" fill="{KRAS}" {o(3)}/>'
          f'<circle cx="{x-r*.34:.0f}" cy="{y-r*.22:.0f}" r="{r*.12:.0f}" fill="{K}"/>'
          f'<circle cx="{x+r*.34:.0f}" cy="{y-r*.22:.0f}" r="{r*.12:.0f}" fill="{K}"/>'
          f'<path d="M{x-r*.30:.0f},{y+r*.46:.0f} q{r*.30:.0f},{-r*.20:.0f}'
          f' {r*.60:.0f},0" fill="none" stroke="{K}"'
          f' stroke-width="{max(2,4*s_):.0f}"/></g>')
    return s


def _taz_i_svertok(x, y, s_=1.0, t=0.0, ug=0.0):
    """Таз под рукой и свёрток чистого белья, перевязанный тесьмой: таз —
    жестяной с обручем и бликом, свёрток — скатка с узлом."""
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x-96*s_:.0f},{y-60*s_:.0f} q{10*s_:.0f},{84*s_:.0f}'
         f' {96*s_:.0f},{84*s_:.0f} q{86*s_:.0f},0 {96*s_:.0f},{-84*s_:.0f} Z"'
         f' fill="#b6bcc2" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-60*s_:.0f}" rx="{96*s_:.0f}"'
         f' ry="{24*s_:.0f}" fill="#cfd5da" {o(5)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-58*s_:.0f}" rx="{80*s_:.0f}"'
         f' ry="{17*s_:.0f}" fill="#8f979d" opacity=".8"/>'
         f'<path d="M{x-70*s_:.0f},{y-20*s_:.0f} q{18*s_:.0f},{34*s_:.0f}'
         f' {44*s_:.0f},{44*s_:.0f}" fill="none" stroke="#eef2f4"'
         f' stroke-width="{9*s_:.0f}" opacity=".5"/></g>')
    return s


def _svertok_belya(x, y, s_=1.0, t=0.0, ug=-8.0):
    """Свёрток чистого белья: скатка полотна со складками и крест-накрест
    тесьма с узлом."""
    w2, h2 = 150 * s_, 96 * s_
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'{ten(x, y + h2 * .54, w2 * .54, 12 * s_, .4)}'
         f'<rect x="{x-w2/2:.0f}" y="{y-h2/2:.0f}" width="{w2:.0f}" height="{h2:.0f}"'
         f' rx="{22*s_:.0f}" fill="{KREM}" {o(6)}/>')
    for i in range(4):
        s += (f'<path d="M{x-w2*.42+i*w2*.24:.0f},{y-h2*.44:.0f}'
              f' q{8*s_:.0f},{h2*.44:.0f} {-2*s_:.0f},{h2*.86:.0f}" fill="none"'
              f' stroke="#d6cbb0" stroke-width="{max(3,6*s_):.0f}"/>')
    s += (f'<rect x="{x-w2*.08:.0f}" y="{y-h2*.56:.0f}" width="{w2*.16:.0f}"'
          f' height="{h2*1.12:.0f}" fill="{TKAN}" opacity=".9"/>'
          f'<rect x="{x-w2*.54:.0f}" y="{y-h2*.10:.0f}" width="{w2*1.08:.0f}"'
          f' height="{h2*.16:.0f}" fill="{TKAN}" opacity=".9"/>'
          f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{13*s_:.0f}" fill="{TKAN}" {o(3)}/></g>')
    return s


def _bochka_vody(x, y, s_=1.0, t=0.0, ledok=True):
    """Бочка с водой: клёпки, два обруча, вода с ледком и отражением,
    по краю наледь."""
    w2, h2 = 150 * s_, 170 * s_
    s = (f'{ten(x, y + 10 * s_, w2 * .56, 16 * s_, .5)}'
         f'<path d="M{x-w2/2:.0f},{y-h2:.0f} q{-12*s_:.0f},{h2*.5:.0f} 0,{h2:.0f}'
         f' L{x+w2/2:.0f},{y:.0f} q{12*s_:.0f},{-h2*.5:.0f} 0,{-h2:.0f} Z"'
         f' fill="url(#derev)" {o(7)}/>')
    for i in range(6):
        s += (f'<line x1="{x-w2*.42+i*w2*.17:.0f}" y1="{y-h2+8*s_:.0f}"'
              f' x2="{x-w2*.46+i*w2*.19:.0f}" y2="{y-6*s_:.0f}" stroke="#5b4428"'
              f' stroke-width="{max(3,5*s_):.0f}" opacity=".8"/>')
    for p in (.22, .74):
        s += (f'<rect x="{x-w2*.54:.0f}" y="{y-h2+h2*p:.0f}" width="{w2*1.08:.0f}"'
              f' height="{16*s_:.0f}" rx="{6*s_:.0f}" fill="{ZHELEZ}" {o(4)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h2:.0f}" rx="{w2*.5:.0f}" ry="{w2*.17:.0f}"'
          f' fill="{VODA2}" {o(5)}/>'
          f'<ellipse cx="{x:.0f}" cy="{y-h2+4*s_:.0f}" rx="{w2*.42:.0f}"'
          f' ry="{w2*.12:.0f}" fill="{VODA}" opacity=".9"/>'
          f'<ellipse cx="{x-w2*.14:.0f}" cy="{y-h2:.0f}" rx="{w2*.16:.0f}"'
          f' ry="{w2*.05:.0f}" fill="#9fc4d8"'
          f' opacity="{.4+.3*abs(A.w(t,2.6,.2)):.2f}"/>')
    if ledok:
        s += (f'<path d="M{x-w2*.40:.0f},{y-h2-2*s_:.0f} q{w2*.20:.0f},{-10*s_:.0f}'
              f' {w2*.40:.0f},{2*s_:.0f} q{w2*.20:.0f},{8*s_:.0f} {w2*.38:.0f},{-4*s_:.0f}"'
              f' fill="none" stroke="{LED}" stroke-width="{10*s_:.0f}" opacity=".8"/>')
    return s


def _kovsh_na_gvozde(x, y, s_=1.0, t=0.0, ph=.0):
    """Ковш на гвозде: долблёный черпак с ручкой-уткой, качается на гвозде."""
    ug = 5.0 * A.w(t, 2.5, ph)
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{6*s_:.0f}" fill="{ZHELEZ}"/>'
            f'<path d="M{x:.0f},{y:.0f} q{18*s_:.0f},{38*s_:.0f} {8*s_:.0f},{66*s_:.0f}"'
            f' fill="none" stroke="url(#derev)" stroke-width="{14*s_:.0f}"/>'
            f'<path d="M{x-54*s_:.0f},{y+66*s_:.0f} q{10*s_:.0f},{62*s_:.0f}'
            f' {62*s_:.0f},{62*s_:.0f} q{52*s_:.0f},0 {62*s_:.0f},{-62*s_:.0f} Z"'
            f' fill="url(#derev)" {o(6)}/>'
            f'<ellipse cx="{x+8*s_:.0f}" cy="{y+66*s_:.0f}" rx="{62*s_:.0f}"'
            f' ry="{17*s_:.0f}" fill="#8a6038" {o(4)}/>'
            f'<path d="M{x-28*s_:.0f},{y+96*s_:.0f} q{30*s_:.0f},{18*s_:.0f}'
            f' {62*s_:.0f},{-4*s_:.0f}" fill="none" stroke="#c9a47a"'
            f' stroke-width="{6*s_:.0f}" opacity=".6"/></g>')


# ── ДЕКОРАЦИИ ──────────────────────────────────────────────────────────────

def parenaya_repa_iz_pechi(t):
    """Устье печи и шесток крупно: хозяйка ухватом вынимает на шесток
    чугунок с пареной репой, малыш на лавке держится за печь и тянется к
    репке, дуя на пальцы. Рядом заслонка, деревянная ложка, печная утварь."""
    rnd = random.Random(331)
    pol = 1010
    s = f'<rect width="{W}" height="{H}" fill="#241a12"/>'
    # задник: бревенчатая стена справа, где стоит хозяйка, и полка с утварью
    s += SL(Z_DAL, brevna(1180, 40, 740, pol - 40, 96))
    s += SL(Z_DAL, _polka_s_utvaryu(1250, 250, 580, t, 331, 5))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-20:.0f}" width="{W}" height="34"'
                   f' fill="#3b2a1a" opacity=".9"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 18, 1074, 333, 6, "#4a3824"))
    # ПЕЧЬ слева и в центре: массив, кладка, устье рамкой, огонь в глубине
    s += SL(Z_SRED, pech(-60, 20, 1240, 880, t, True, True, False))
    s += SL(Z_SRED, kladka(20, 60, 1060, 340, 76, PECH2))
    put = kontur_proema(430, 470, 620, 400, "ustie")
    s += SL(Z_SRED, f'<path d="{put}" fill="#190c05"/>'
            + ogon(740, 820, t, 1.5, .2, 8) + ugli(560, 846, 420, t, 9, 2)
            + iskra_let(t, 740, 790, 9, 4, 240, .6)
            + f'<path d="{put}" fill="none" stroke="#2a1a0e" stroke-width="10"/>')
    s += SL(Z_SRED, kirpich_ustya(430, 470, 620, 400, t, True))
    # ШЕСТОК — полка перед устьем, на неё и выезжает чугунок
    s += SL(Z_SRED, f'{ten(740, 902, 330, 22, .5)}'
                    f'<rect x="360" y="864" width="770" height="40" rx="10"'
                    f' fill="{PECH2}" {o(7)}/>'
            + f'<rect x="388" y="904" width="714" height="22" rx="8"'
              f' fill="#c2b393" {o(4)}/>'
            + kladka(360, 926, 770, 84, 42, PECH2))
    # ГЛАВНЫЙ ПРЕДМЕТ: чугунок с репой выезжает из устья на шесток
    vyezd = A.ease(A.seg(t, .35, 1.5))
    s += SL(Z_SRED, dym(700, 700, t, 4, .22, 220, .26, "#d6dde4", 1.1))
    s += SL(Z_SRED, _chugunok(690, 862, 1.0, t, vyezd, 5))
    # заслонка у края устья и деревянная ложка на шестке
    s += SL(Z_SRED, _zaslonka_pechi(1180, 900, 230, 300, t, 1.0))
    s += SL(Z_SRED, _lozhka_derev(980, 846, 1.1, 104))
    # ДВЕ ФИГУРЫ: реестр объявляется до первой руки
    hx, hy, hh = 1370, pol, 730
    mx, my, mh = 330, 872, 420
    _figury_kadra((hx, hy, hh), (mx, my, mh))
    tyan = A.ease(A.seg(t, .4, 1.1))
    duet = A.ease(A.seg(t, 1.8, .9))
    # хозяйка: ОБЕ руки на черенке ухвата, обе наружу влево
    hoz = figura(hx, hy, hh, t, col="#54505e", kant="#ffd98a", platok=True,
                 ph=.3, naklon=3.0)
    h1, (u1x, u1y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .44, 16 + 10 * vyezd, t,
                                   "#54505e", "#ffd98a", .2, 5.0)
    h2, (u2x, u2y), _ = _ruka_sgib_mimo(hx, hy, hh, -1, hh * .26, 34,
                                        hh * .24, 20 + 8 * vyezd, t,
                                        "#54505e", "#ffd98a", .6, 4.0)
    hoz += h1 + h2
    # малыш на лавке: левая держится за печь, правая тянется к репке
    mal = figura(mx, my, mh, t, col="#b8a86a", kant="#ffd98a", ph=.7,
                 naklon=5.0)
    m1, (p1x, p1y), _ = _ruka_mimo(mx, my, mh, -1, mh * .46, 10, t,
                                   "#b8a86a", "#ffd98a", .1, 4.0)
    m2, (p2x, p2y), _ = _ruka_mimo(mx, my, mh, 1, mh * .50, 4 - 26 * tyan, t,
                                   "#b8a86a", "#ffd98a", .5, 7.0)
    mal += m1 + m2
    s += SL(Z_SRED, _lavka_krupno(340, my + 4, 420, t, 150, False))
    s += SL(Z_SRED, hoz)
    s += SL(Z_SRED, mal)
    # УХВАТ: черенок приходит ровно в кисти хозяйки, рога обхватывают чугунок
    uh, (rx_, ry_) = _uhvat_rogi(min(u1x, u2x) + 24, (u1y + u2y) * .5,
                                 250 - 30 * vyezd, 182, t, 1.0)
    s += SL(Z_SRED, uh)
    # варежки ПОВЕРХ черенка — хват читается перекрытием, а не соседством
    s += SL(Z_SRED, _varezhka(u1x, u1y + 2, hh, t, .2)
            + _varezhka(u2x, u2y + 2, hh, t, .5))
    # малыш дует на пальцы: пар у его правой кисти, варежки нет (нечего брать)
    s += SL(Z_SRED, par(p2x + 26, p2y - 10, t, 3, .40 + .3 * duet, 90, .7))
    s += SL(Z_SRED, _repka(p2x + 92, 846, .64, t, .4, True))
    # нижняя треть: вещи, а не пустой пол
    s += SL(Z_SRED, _ugol_pechnoy_utvari(1300, pol + 10, t, 3))
    s += SL(Z_SRED, _polenica(60, pol + 70, 300, 170, 337, 25)
            + _dvorovaya_utvar(620, pol + 72, 320, t, 339, ["kadka", "vedro"])
            + kartoshka(1080, pol + 60, t, 7, 341, 1.0)
            + _polovik(1420, pol + 40, 440, 110)
            + _valenki_u_dveri(1740, pol + 30, 1.05, t))
    s += SL(Z_SRED, _kot_zhivoy(1010, pol + 56, t, 1.1, "#38332e", .3))
    s += SL(Z_SRED, teplo(740, 800, 560, 420, .42))
    s += SL(Z_PERED, _stolb_pered(1890, 120, "#1a120c", 0, H))
    s += vinetka(.42)
    return s


def pirogi_na_rushnike(t):
    """Стол под длинным вышитым рушником: блюдо румяных пирогов крупно,
    морковь с ботвой, луковицы, скалка, миска с начинкой. Бабушка в переднике
    левой рукой держит блюдо, правой разламывает верхний пирог — из разлома
    идёт пар, с рук сыплется мука."""
    rnd = random.Random(347)
    pol = 1012
    s = f'<rect width="{W}" height="{H}" fill="#2a2018"/>'
    s += SL(Z_DAL, _stena_gornicy(t, 349, True, 700, True))
    s += SL(Z_DAL, _polka_s_utvaryu(80, 190, 560, t, 351, 5)
            + _polka_s_utvaryu(1230, 170, 560, t, 353, 4))
    s += SL(Z_DAL, utvar_pekarni(620, 196, 560, t, 355))
    # жердь над столом: связка лука, пучки зелени, рушник на стене — иначе
    # простенок между полками остаётся голым (замер пустоты центра)
    s += SL(Z_DAL, f'<rect x="660" y="300" width="560" height="18" rx="7"'
                   f' fill="#5b4428" {o(5)}/>')
    for i in range(6):
        s += SL(Z_DAL, _lukovica(700 + i * 92, 420 + (i % 2) * 34, .78, t,
                                 i * .3)
                + f'<line x1="{700+i*92:.0f}" y1="318" x2="{700+i*92:.0f}"'
                  f' y2="{388+(i%2)*34:.0f}" stroke="#b8a86a" stroke-width="6"/>')
    s += SL(Z_DAL, _puchki_zeleni(760, 520, 400, t, 371, 4))
    s += SL(Z_DAL, _rushnik_vyshityy(690, 92, 500, 84, t, 373))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="32"'
                   f' fill="#3f2d1d" opacity=".9"/>' + polovicy(pol + 16)
            + _pol_shvy(pol + 20, 1076, 357, 6, "#4a3824"))
    # печной угол справа — одно тёплое пятно кадра
    s += SL(Z_SRED, kladka(1660, 420, 260, 300, 70, PECH2)
            + f'<path d="{kontur_proema(1700, 560, 180, 150, "ustie")}"'
              f' fill="#190c05"/>' + ogon(1790, 686, t, .9, .4, 5))
    # СТОЛ и рушник
    s += SL(Z_SRED, f'{ten(840, pol + 18, 640, 26, .5)}'
                    f'<rect x="90" y="700" width="1500" height="56" rx="12"'
                    f' fill="url(#derev)" {o(8)}/>'
            + f'<rect x="124" y="756" width="1432" height="28" rx="9"'
              f' fill="#5b4428" {o(5)}/>')
    for px in (200, 1420):
        s += SL(Z_SRED, f'<rect x="{px:.0f}" y="784" width="74"'
                        f' height="{pol-784:.0f}" rx="12" fill="#5b4428" {o(6)}/>')
    s += SL(Z_SRED, _rushnik_vyshityy(120, 684, 1440, 100, t, 359))
    # ГЛАВНЫЙ ПРЕДМЕТ: блюдо пирогов, верхний разламывается
    razlom = A.ease(A.seg(t, .45, 1.3))
    s += SL(Z_SRED, _blyudo_pirogov(830, 666, 560, t, razlom, 5, 361))
    # сопутствующие вещи НА столе
    s += SL(Z_SRED, _morkov_botva(300, 660, 1.05, t, .2)
            + _morkov_botva(382, 666, .92, t, .6)
            + _lukovica(470, 660, 1.0, t, .3)
            + _lukovica(552, 664, .86, t, .7)
            + _skalka(1280, 652, 1.0, -8)
            + _miska_nachinki(1480, 668, 1.0, t, ORA))
    s += SL(Z_SRED, lampa(170, 640, t, 1.0, True))
    # ОДНА ФИГУРА: обе руки наружу влево, к блюду
    bx, by_, bh = 1330, pol, 750
    bab = figura(bx, by_, bh, t, col="#6a5a4a", kant="#ffd98a", platok=True,
                 ph=.4, naklon=4.0)
    r1, (k1x, k1y), _ = _ruka_so_sgibom(bx, by_, bh, -1, bh * .24, 30,
                                        bh * .26, 46, t, "#6a5a4a", "#ffd98a",
                                        .2, 5.0)
    r2, (k2x, k2y), _ = _ruka_so_sgibom(bx, by_, bh, -1, bh * .28, 12,
                                        bh * .30, 30 - 14 * razlom, t,
                                        "#6a5a4a", "#ffd98a", .6, 6.0)
    bab += r1 + r2
    # передник поверх одежды — роль видна с кадра
    s += SL(Z_SRED, f'<path d="M{bx-bh*.14:.0f},{by_-bh*.58:.0f}'
                    f' L{bx+bh*.14:.0f},{by_-bh*.58:.0f}'
                    f' L{bx+bh*.18:.0f},{by_-bh*.16:.0f}'
                    f' L{bx-bh*.18:.0f},{by_-bh*.16:.0f} Z" fill="{KREM}"'
                    f' {o(5)}/>'
            + f'<path d="M{bx-bh*.18:.0f},{by_-bh*.28:.0f} q{bh*.18:.0f},{bh*.03:.0f}'
              f' {bh*.36:.0f},0" fill="none" stroke="{TKAN}" stroke-width="9"'
              f' opacity=".8"/>')
    s += SL(Z_SRED, bab)
    # мука сыплется с рук, варежек нет: пирог держат пальцами, перекрытия нет
    s += SL(Z_SRED, _muka_sypletsya(k1x, k1y + 10, t, 11, 363, 120)
            + _muka_sypletsya(k2x, k2y + 8, t, 8, 365, 100))
    # нижняя треть
    s += SL(Z_SRED, _dvorovaya_utvar(70, pol + 76, 330, t, 367,
                                     ["korzina", "meshok"])
            + _yaschiki(620, pol + 10, t, 375, 3, .92)
            + _dvorovaya_utvar(880, pol + 70, 300, t, 377, ["vedro", "kadka"])
            + kartoshka(640, pol + 64, t, 8, 369, 1.05)
            + _kadushka_kapusty(1700, pol + 50, t, .9)
            + _polovik(900, pol + 48, 520, 120))
    s += SL(Z_SRED, _kot_zhivoy(1120, pol + 58, t, 1.05, "#4a3f36", .5))
    s += SL(Z_SRED, teplo(1790, 660, 420, 360, .34))
    s += SL(Z_PERED, _stolb_pered(-6, 112, "#1a120c", 0, H))
    s += vinetka(.42)
    return s


def yaschik_s_peskom_v_pogrebe(t):
    """Погреб со светом из люка: дощатый ящик с песком крупно, из песка
    торчат чёрные макушки редьки и рыжие морковки. Хозяин в телогрейке
    присел у ящика, левой держит фонарь, правой разгребает песок и тянет
    редьку за хвост. Рядом кадка, полка с банками, приставная лестница."""
    rnd = random.Random(379)
    pol = 1008
    s = f'<rect width="{W}" height="{H}" fill="#1b150f"/>'
    # земляные стены и своды — каменная кладка даёт сетку, а не обои
    s += SL(Z_DAL, svody(t, "#3b332a", 3))
    s += SL(Z_DAL, kladka(0, 120, 760, 620, 78, "#6a5c4c")
            + kladka(1180, 120, 740, 620, 78, "#6a5c4c"))
    s += SL(Z_DAL, kladka(760, 300, 420, 440, 72, "#5e5244"))
    # матица и подпорный столб погреба: длинная балка держит крупную
    # вертикаль кадра, а главный предмет остаётся в коридоре 420-700 px
    s += SL(Z_DAL, f'<rect x="-20" y="132" width="1120" height="52" rx="10"'
                   f' fill="#5a4530" {o(7)}/>'
            + f'<rect x="-20" y="184" width="1120" height="16" rx="6"'
              f' fill="#3f2d1d" opacity=".8"/>'
            + f'<rect x="300" y="184" width="54" height="{pol-184:.0f}" rx="10"'
              f' fill="#6b5340" {o(6)}/>'
            + f'<rect x="286" y="170" width="84" height="24" rx="8"'
              f' fill="#5a4530" {o(4)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="{pol-24:.0f}" width="{W}" height="{H-pol+24:.0f}"'
                   f' fill="#3f3326"/>'
            + _zemlya_faktura(pol - 10, 1072, 381, 18, "#342a1e"))
    # ЛЮК В ПОТОЛКЕ и косой столб света из него
    s += SL(Z_DAL, f'<rect x="700" y="60" width="520" height="34" rx="8"'
                   f' fill="#2a2118" {o(6)}/>'
            + f'<path d="M740,94 L1180,94 L1120,34 L800,34 Z" fill="#5a4a36"'
              f' {o(5)}/>'
            + f'<rect x="1140" y="30" width="180" height="24" rx="8"'
              f' fill="#6b5340" {o(4)}/>')
    s += SL(Z_SRED, _konus_sveta(960, 96, 440, 820, 0.0, .38))
    s += SL(Z_SRED, luch(700, 94, 520, 820, t, .18))
    # ПОЛКА С БАНКАМИ и лестница — обстановка погреба
    s += SL(Z_SRED, _banki_v_pogrebe(1380, 520, 480, t, 383, 5))
    # огарок на полке: живой огонёк погреба, кроме фонаря в руке
    s += SL(Z_SRED, svecha(1670, 512, t, .3, 1.15, 104)
            + teplo(1670, 470, 220, 190, .38))
    s += SL(Z_SRED, _banki_v_pogrebe(60, 470, 420, t, 385, 4))
    s += SL(Z_SRED, _lestnica(1700, pol, 760, t, 6, -7.0))
    # ГЛАВНЫЙ ПРЕДМЕТ: ящик с песком на пол-кадра
    vyhod = A.ease(A.seg(t, .4, 1.6))
    s += SL(Z_SRED, _yaschik_peska(560, pol - 10, 690, 290, t, vyhod, 387))
    # ОДНА ФИГУРА: присел у ящика, корпус наклонён к песку
    gx, gy, gh = 1230, pol, 640
    goz = figura(gx, gy, gh, t, col="#4e5a46", kant="#ffd98a", ph=.3,
                 shapka=True, tulup=True, naklon=7.0)
    g1, (f1x, f1y), _ = _ruka_so_sgibom(gx, gy, gh, 1, gh * .26, 6,
                                        gh * .24, 30, t, "#4e5a46", "#ffd98a",
                                        .1, 4.0)
    g2, (f2x, f2y), _ = _ruka_so_sgibom(gx, gy, gh, -1, gh * .30, 22,
                                        gh * .32, 56 - 12 * vyhod, t,
                                        "#4e5a46", "#ffd98a", .5, 6.0)
    goz += g1 + g2
    s += SL(Z_SRED, goz)
    # ФОНАРЬ в левой кисти: живой огонёк кадра, варежка перекрывает скобу
    s += SL(Z_SRED, _fonar_ruchnoy(f1x + 20, f1y + 150, t, 1.0, 1.0, .2))
    s += SL(Z_SRED, _varezhka(f1x, f1y + 4, gh, t, .1))
    # РЕДЬКА, которую вынимают за хвост: идёт вверх из песка вслед за кистью
    s += SL(Z_SRED, _redka(f2x - 30, f2y + 78 - 40 * vyhod, .92, t,
                           -12 + 8 * vyhod, .5, "#2e2b2a"))
    s += SL(Z_SRED, _varezhka(f2x, f2y + 6, gh, t, .5))
    # нижняя треть: земляной пол с вещами
    s += SL(Z_SRED, _kadushka_kapusty(240, pol + 54, t, 1.0)
            + _yaschiki(1560, pol + 20, t, 389, 3, 1.0)
            + kartoshka(800, pol + 56, t, 9, 391, 1.1)
            + _luzha(1120, pol + 62, 160, t, .3)
            + _dvorovaya_utvar(1300, pol + 70, 260, t, 393, ["vedro"]))
    s += SL(Z_SRED, _kot_zhivoy(520, pol + 58, t, .95, "#2f2a26", .6, True, True))
    s += SL(Z_PERED, _stolb_pered(-8, 126, "#120d08", 0, H))
    s += SL(Z_PERED, _stolb_pered(1884, 126, "#120d08", 0, H))
    s += vinetka(.46)
    return s


def rynochnyy_prilavok_s_redkoy(t):
    """Городской рынок: погребной ящик стал прилавком под полосатым навесом.
    В витрине прилавка — настоящая чёрная редька; на прилавке весы, ценники
    без цифр, пучки зелени, свёкла, капуста. Продавщица кладёт редьку на
    весы и придерживает чашу, покупательница держит раскрытую сумку и
    показывает на редьку."""
    rnd = random.Random(397)
    pol = 1014
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 41)
    s += oblaka(t, 150, 5, 43, .40, "#cdd7e4", 13.0)
    s += SL(Z_DAL, _derevnya_ryad(560, t, 47, ((160, 330), (1700, 300))))
    s += SL(Z_DAL, _zabor_dosok(-30, 420, 540, 170, 49, 56))
    s += SL(Z_DAL, goloe_derevo(1560, 580, 460, t, 51, 8, "#3a3b43", True))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-26:.0f}" width="{W}" height="{H-pol+26:.0f}"'
                   f' fill="#55504a"/>' + _bulyzhnik(pol - 16, 1074, 53, 86))
    # ПРИЛАВОК: тумба из того же дощатого короба, что был ящиком в погребе
    px, py, pw, ph_ = 440, 470, 800, 420
    s += SL(Z_SRED, _naves_polosatyy(360, 430, 1340, t, 130, 55))
    s += SL(Z_SRED, f'{ten(960, pol + 16, 520, 24, .5)}'
                    f'<rect x="380" y="890" width="1280" height="40" rx="10"'
                    f' fill="url(#dosk)" {o(8)}/>'
            + f'<rect x="402" y="930" width="1236" height="{pol-930+16:.0f}"'
              f' rx="8" fill="#7d5636" {o(6)}/>'
            + "".join(f'<line x1="{424+i*72:.0f}" y1="940" x2="{424+i*72:.0f}"'
                      f' y2="{pol+10:.0f}" stroke="#5b4428" stroke-width="7"'
                      f' opacity=".8"/>' for i in range(17)))
    # НАСТОЯЩИЙ КАДР в витрине прилавка: сначала рисованный вид, потом метка,
    # потом обвязка поверх — переплёт витрины и бортик
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#2b2622"/>'
            + _vid_za_proemom(put, t, "lavka", 57, px + pw * .5)
            + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#5f4a34"'
                    f' stroke-width="30"/>'
            + f'<rect x="{px-40:.0f}" y="{py-44:.0f}" width="{pw+80:.0f}"'
              f' height="38" rx="10" fill="#6b5340" {o(5)}/>'
            + f'<rect x="{px-26:.0f}" y="{py+ph_-12:.0f}" width="{pw+52:.0f}"'
              f' height="34" rx="10" fill="url(#dosk)" {o(6)}/>'
            + f'<line x1="{px:.0f}" y1="{py+ph_*.5:.0f}" x2="{px+pw:.0f}"'
              f' y2="{py+ph_*.5:.0f}" stroke="#5f4a34" stroke-width="16"/>'
            + f'<path d="M{px+40:.0f},{py+ph_*.18:.0f} L{px+pw*.42:.0f},'
              f'{py+ph_*.06:.0f}" fill="none" stroke="#ffffff" stroke-width="12"'
              f' opacity="{.16+.10*abs(A.w(t,3.4,.2)):.2f}"/>')
    # ВЕСЫ, ценники и товар на прилавке
    klad = A.ease(A.seg(t, .5, 1.2))
    s += SL(Z_SRED, _vesy(1500, 886, t, .62, .22 * klad, .5, 240))
    s += SL(Z_SRED, _cenniki_bez_cifr(1250, 886, 3, t, 59))
    s += SL(Z_SRED, _puchki_zeleni(1310, 878, 220, t, 61, 3)
            + _svekla(1600, 862, .9, t, .3)
            + _svekla(1648, 872, .74, t, .7)
            + _kapusta(1420, 856, .86, t))
    # редька горкой на левом краю прилавка — на неё и показывает покупательница
    for i, (rx0, ry0, rs) in enumerate(((410, 862, .54), (466, 872, .44),
                                        (372, 878, .40))):
        s += SL(Z_SRED, _redka(rx0, ry0, rs, t, -8 + i * 11, .22))
    # ДВЕ ФИГУРЫ: реестр до первой руки
    prx, pry, prh = 1790, pol, 730
    pux, puy, puh = 250, pol, 700
    _figury_kadra((prx, pry, prh), (pux, puy, puh))
    pok = A.ease(A.seg(t, .4, 1.0))
    # продавщица: обе руки влево, к весам
    prod = figura(prx, pry, prh, t, col="#3f5c7a", kant="#cfe4f5", platok=True,
                  ph=.2, naklon=3.0)
    a1, (v1x, v1y), _ = _ruka_mimo(prx, pry, prh, -1, prh * .40, 20 + 10 * klad, t,
                                   "#3f5c7a", "#cfe4f5", .1, 5.0)
    a2, (v2x, v2y), _ = _ruka_sgib_mimo(prx, pry, prh, -1, prh * .22, 40,
                                        prh * .22, 56, t, "#3f5c7a",
                                        "#cfe4f5", .5, 4.0)
    prod += a1 + a2
    # нарукавники и фартук — роль читается со стоп-кадра
    s += SL(Z_SRED, f'<path d="M{prx-prh*.13:.0f},{pry-prh*.56:.0f}'
                    f' L{prx+prh*.13:.0f},{pry-prh*.56:.0f}'
                    f' L{prx+prh*.17:.0f},{pry-prh*.14:.0f}'
                    f' L{prx-prh*.17:.0f},{pry-prh*.14:.0f} Z" fill="#dfd6c0"'
                    f' {o(5)}/>')
    s += SL(Z_SRED, prod)
    s += SL(Z_SRED, f'<ellipse cx="{v1x+16:.0f}" cy="{v1y:.0f}" rx="26"'
                    f' ry="20" fill="#efe8d8" {o(4)}/>')
    # редька в кисти продавщицы ложится на чашу весов
    s += SL(Z_SRED, _redka(v1x - 54, v1y + 44 + 26 * klad, .64, t, 14, .3))
    s += SL(Z_SRED, _varezhka(v1x, v1y + 4, prh, t, .1))
    # покупательница: левая с раскрытой сумкой, правая показывает на редьку
    pokup = figura(pux, puy, puh, t, col="#54505e", kant="#cfe4f5", ph=.6,
                   platok=True, naklon=4.0)
    b1, (s1x, s1y), _ = _ruka_mimo(pux, puy, puh, -1, puh * .34, 54, t,
                                   "#54505e", "#cfe4f5", .2, 5.0)
    b2, (s2x, s2y), _ = _ruka_mimo(pux, puy, puh, 1, puh * .34, 58 - 10 * pok, t,
                                   "#54505e", "#cfe4f5", .6, 6.0)
    pokup += b1 + b2
    s += SL(Z_SRED, pokup)
    s += SL(Z_SRED, _sumka_hozyaystvennaya(s1x - 10, s1y + 118, t, 1.0, pok))
    s += SL(Z_SRED, _varezhka(s1x, s1y + 6, puh, t, .2))
    s += SL(Z_SRED, para_izo_rta(pux + 40, puy - puh * .80, t, .3, 1.0, .5)
            + para_izo_rta(prx - 44, pry - prh * .80, t, .7, 1.0, .45))
    # нижняя треть: городская мостовая с вещами
    s += SL(Z_SRED, _yaschiki(170, pol + 16, t, 63, 3, 1.0)
            + _yaschiki(1500, pol + 24, t, 65, 2, .9)
            + _kucha_listev(760, pol + 56, 300, 67, 70)
            + _luzha(1120, pol + 58, 190, t, .4)
            + _golub(620, pol + 50, t, 1.0, .2, True)
            + _golub(690, pol + 58, t, .86, .6, False))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 69, .54, .9))
    s += SL(Z_PERED, _stolb_pered(1892, 118, "#171310", 0, H))
    s += vinetka(.42)
    return s


def salat_iz_redki_za_tri_shaga(t):
    """Городская кухня у окна: тёрка над глубокой миской крупно, рядом
    бутылка масла без этикетки, солонка, ложка, полотенце. Женщина левой
    рукой держит тёрку за ручку, правой водит по ней редькой, потом льёт
    масло ложкой, потом трясёт солонкой — три шага подряд."""
    rnd = random.Random(401)
    pol = 1016
    s = f'<rect width="{W}" height="{H}" fill="#2e3334"/>'
    s += SL(Z_DAL, _kafel(0, 90, 1920, 640, t, 403))
    # окно кухни: вечер за стеклом, огоньки в домах напротив
    s += SL(Z_DAL, okno_izby(1320, 150, 520, 420, t,
                             f'<rect x="1320" y="150" width="520" height="420"'
                             f' fill="#2b3550"/>'
                             + "".join(f'<rect x="{1360+i*96:.0f}"'
                                       f' y="{300+(i%3)*54:.0f}" width="62"'
                                       f' height="46" rx="5" fill="{SVET}"'
                                       f' opacity="{.5+.3*abs(A.w(t,2.6,i*.4)):.2f}"/>'
                                       for i in range(5)),
                             .14, False, True))
    s += SL(Z_DAL, _polki_otkrytye(60, 170, 520, t, 405, 3, True, .0))
    s += SL(Z_DAL, _kover_na_stene(640, 150, 1, 1, t, 407)
            if False else _knizhnaya_polka(640, 210, 560, t, 409, 2, 170))
    s += SL(Z_DAL, tusklaya_lampochka(960, 40, t, 1.1, True))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-20:.0f}" width="{W}" height="{H-pol+20:.0f}"'
                   f' fill="#6a615a"/>' + _pol_shvy(pol - 10, 1074, 411, 6, "#4e463f"))
    # СТОЛ-столешница на тумбах
    s += SL(Z_SRED, f'{ten(900, pol + 14, 620, 24, .5)}'
                    f'<rect x="80" y="720" width="1500" height="46" rx="10"'
                    f' fill="#b9b2a4" {o(7)}/>'
            + f'<rect x="110" y="766" width="1440" height="{pol-766+10:.0f}"'
              f' rx="8" fill="#7e6c56" {o(6)}/>'
            + "".join(f'<rect x="{160+i*300:.0f}" y="800" width="250"'
                      f' height="180" rx="9" fill="#8f7b61" {o(4)}/>'
                      f'<circle cx="{280+i*300:.0f}" cy="890" r="13"'
                      f' fill="{ZHELEZ}" {o(3)}/>' for i in range(5)))
    # ТРИ ШАГА ПОДРЯД: тёрка, масло, соль
    sh1 = A.seg(t, .3, 1.2)
    sh2 = A.seg(t, 1.5, 1.1)
    sh3 = A.seg(t, 2.6, 1.0)
    napoln = min(1.0, A.ease(sh1) * .7 + A.ease(sh2) * .3)
    # ГЛАВНЫЙ ПРЕДМЕТ: тёрка над глубокой миской
    s += SL(Z_SRED, _glubokaya_miska(780, 712, 1.1, t, napoln))
    s += SL(Z_SRED, _terka(780, 580 - 14 * A.w(t, .9, .2), t, 1.25, -9.0))
    if sh1 < 1.0:
        s += SL(Z_SRED, _redka(790 + 30 * A.w(t, .7, .1),
                               470 + 120 * A.ease(sh1), .66, t, 18, .4))
        s += SL(Z_SRED, _struzhka_letit(780, 640, t, 9, 413, 120))
    # сопутствующие вещи
    s += SL(Z_SRED, _butyl_masla(1180, 718, 1.15, t, .3 * A.ease(sh2),
                                 A.ease(sh2)))
    s += SL(Z_SRED, _lozhka_derev(1040, 660 - 40 * A.ease(sh2), 1.0,
                                  128 - 40 * A.ease(sh2)))
    s += SL(Z_SRED, _solonka(1340, 716, 1.15, t, A.ease(sh3)))
    s += SL(Z_SRED, _polotence(1660, 700, 230, t, .3, "#e3ddc6", True))
    s += SL(Z_SRED, _kruzhka(240, 716, 1.0, 0, "#e8eef0", 1)
            + _banka_krupy(380, 716, 1.0, "#d8c08a")
            + _tarelka(500, 690, 66, t, .3, False, 0, "#eef2f4"))
    # ОДНА ФИГУРА: обе руки наружу, к тёрке и к миске
    zx, zy, zh = 1520, pol, 740
    zhen = figura(zx, zy, zh, t, col="#8a4a5c", kant="#cfe4f5", ph=.3,
                  naklon=4.0)
    q1, (w1x, w1y), _ = _ruka_so_sgibom(zx, zy, zh, -1, zh * .24, 24,
                                        zh * .28, 48, t, "#8a4a5c",
                                        "#cfe4f5", .2, 5.0)
    q2, (w2x, w2y), _ = _ruka_so_sgibom(zx, zy, zh, -1, zh * .26, 8,
                                        zh * .30, 26 + 10 * A.ease(sh3), t,
                                        "#8a4a5c", "#cfe4f5", .6, 7.0)
    zhen += q1 + q2
    s += SL(Z_SRED, zhen)
    # варежка только там, где кисть перекрывает ручку тёрки
    s += SL(Z_SRED, _varezhka(w1x, w1y + 4, zh, t, .2))
    s += SL(Z_SRED, f'<rect x="{w1x-60:.0f}" y="{w1y-8:.0f}" width="90"'
                    f' height="22" rx="10" fill="#9aa3aa" {o(4)}/>')
    # нижняя треть
    s += SL(Z_SRED, _gorodskoy_hlam(120, pol + 46, 300, t, 415,
                                    ["yaschik", "paket"])
            + _polovik(820, pol + 38, 520, 110, "#6a7a8c", "#3f5c7a")
            + _kot_zhivoy(1240, pol + 48, t, 1.05, "#4a4440", .4)
            + _dvorovaya_utvar(1660, pol + 48, 240, t, 417, ["vedro"]))
    s += SL(Z_SRED, teplo(960, 140, 460, 300, .30))
    s += SL(Z_PERED, _stolb_pered(-8, 104, "#1c1a18", 0, H))
    s += vinetka(.40)
    return s


def redka_s_medom_na_blyudce(t):
    """Кухонный подоконник: чёрная редька на блюдце крупно, срезанная
    верхушка лежит рядом крышечкой. В стекле окна за редькой — настоящий
    кадр, где мёд стекает с ложки. Видны руки до локтя: одна придерживает
    редьку, другая чайной ложкой выбирает ямку и кладёт в неё мёд. Рядом
    банка мёда, нож, шерстяной носок на батарее."""
    rnd = random.Random(419)
    pod = 760
    s = f'<rect width="{W}" height="{H}" fill="#2b2f31"/>'
    s += SL(Z_DAL, _kafel(0, 60, 1920, 600, t, 421, "#cfd8d4", "#a4b0ac"))
    s += SL(Z_DAL, _polki_otkrytye(1480, 120, 420, t, 423, 2, False, .0))
    s += SL(Z_DAL, tusklaya_lampochka(300, 30, t, .95, True))
    # НАСТОЯЩИЙ КАДР в стекле окна: вид, метка, переплёт и наличник поверх
    px, py, pw, ph_ = 480, 150, 900, 470
    put = kontur_proema(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1d2630"/>'
            + _vid_za_proemom(put, t, "dvor", 425, px + pw * .5)
            + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#6f6a60"'
                    f' stroke-width="34"/>'
            + f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#6f6a60" stroke-width="22"/>'
            + f'<line x1="{px:.0f}" y1="{py+ph_*.46:.0f}" x2="{px+pw:.0f}"'
              f' y2="{py+ph_*.46:.0f}" stroke="#6f6a60" stroke-width="18"/>'
            + f'<path d="M{px+60:.0f},{py+ph_*.30:.0f} L{px+pw*.34:.0f},'
              f'{py+ph_*.10:.0f}" fill="none" stroke="#ffffff" stroke-width="14"'
              f' opacity="{.14+.10*abs(A.w(t,3.2,.3)):.2f}"/>'
            + f'<rect x="{px-54:.0f}" y="{py-46:.0f}" width="{pw+108:.0f}"'
              f' height="40" rx="10" fill="#7e776c" {o(5)}/>')
    # ПОДОКОННИК — широкая доска, на ней всё и стоит
    s += SL(Z_SRED, f'{ten(930, pod + 16, 560, 22, .5)}'
                    f'<rect x="300" y="{pod-34:.0f}" width="1320" height="48"'
                    f' rx="12" fill="#cfc9bc" {o(7)}/>'
            + f'<rect x="330" y="{pod+14:.0f}" width="1260" height="22" rx="8"'
              f' fill="#a8a299" {o(4)}/>')
    # БАТАРЕЯ с шерстяным носком под подоконником
    s += SL(Z_SRED, _batareya_s_noskom(620, pod + 60, 560, t, True, 427))
    # ГЛАВНЫЙ ПРЕДМЕТ: редька с выбранной ямкой и мёдом
    yamka = A.ease(A.seg(t, .5, 2.0))
    med = A.ease(A.seg(t, 2.8, 1.6))
    s += SL(Z_SRED, _blyudce(900, pod - 30, 1.0, med, t))
    s += SL(Z_SRED, _redka_s_yamkoy(880, pod - 46, 1.0, t, yamka, med))
    # сопутствующие вещи подоконника
    s += SL(Z_SRED, _banka_meda(1330, pod - 34, 1.0, t, True))
    s += SL(Z_SRED, _nozh(1120, pod - 36, 1.0, -6))
    s += SL(Z_SRED, _kruzhka(420, pod - 34, 1.05, 0, "#e8eef0", -1)
            + _banka_krupy(540, pod - 34, .92, "#e2d6a8")
            + _cvetok_v_gorshke(1540, pod - 32, t, .9, .2))
    # РУКИ ДО ЛОКТЯ, без человека: nichya=True — такая кисть не гасит
    # рукав соседней фигуры и браком не считается
    lx, ly = 700, 1072
    r1, (e1x, e1y) = rukav(lx, ly, 300, -74, t, "#c2a07a", "#e8d8c0", .2, 4.0,
                           True)
    rx2, ry2 = 1140, 1074
    hod = A.w(t, 1.6, .1)
    r2, (e2x, e2y) = rukav(rx2, ry2, 318, -104 + 5 * hod, t, "#c2a07a",
                           "#e8d8c0", .6, 5.0, True)
    s += SL(Z_SRED, r1 + r2)
    # варежки ставим: обе кисти перекрывают предмет — редьку и черенок ложки
    s += SL(Z_SRED, _varezhka(e1x, e1y, 760, t, .2, "#e8d8c0", "#b89a74"))
    s += SL(Z_SRED, f'<g transform="rotate(-38 {e2x:.0f} {e2y:.0f})">'
                    f'<ellipse cx="{e2x-22:.0f}" cy="{e2y-46:.0f}" rx="26"'
                    f' ry="18" fill="#cfd8dc" {o(4)}/>'
                    f'<rect x="{e2x-6:.0f}" y="{e2y-46:.0f}" width="13"'
                    f' height="76" rx="6" fill="#b9c6cc" {o(3)}/></g>')
    s += SL(Z_SRED, _varezhka(e2x, e2y, 760, t, .6, "#e8d8c0", "#b89a74"))
    if med > .05:
        s += SL(Z_SRED, f'<path d="M{e2x-26:.0f},{e2y-52:.0f} q{6:.0f},'
                        f'{30+26*med:.0f} {-10:.0f},{54+30*med:.0f}" fill="none"'
                        f' stroke="{ZOL}" stroke-width="{12-4*med:.0f}"'
                        f' stroke-linecap="round"/>')
    # нижняя треть: кухонный низ занят вещами
    s += SL(Z_SRED, _gorodskoy_hlam(170, 1020, 260, t, 429, ["yaschik"])
            + _dvorovaya_utvar(1700, 1026, 210, t, 431, ["vedro"])
            + _polovik(1420, 1016, 400, 96, "#6a7a8c", "#3f5c7a"))
    s += SL(Z_SRED, teplo(900, pod + 80, 520, 260, .26))
    s += SL(Z_PERED, _stolb_pered(1896, 96, "#1a1816", 0, H))
    s += vinetka(.40)
    return s


def sok_redki_k_utru(t):
    """Та же редька на блюдце у окна, за которым ночь сменяется утром, и
    блюдце наполняется янтарным соком. Малыш с завязанным шарфом горлом
    сидит в кровати среди подушек и обеими руками держит плюшевого мишку.
    Мать на краю кровати: левой держит блюдце, правой подносит ложку с
    соком. На тумбочке градусник, стакан, книжка."""
    rnd = random.Random(433)
    pol = 1018
    utro = A.ease(A.seg(t, .6, 2.6))
    s = f'<rect width="{W}" height="{H}" fill="#242a33"/>'
    s += SL(Z_DAL, _stena_gornicy(t, 435, True, 720, True))
    s += SL(Z_DAL, _kover_na_stene(1140, 150, 700, 400, t, 437))
    # окно: ночь светлеет до рассвета, за стеклом огоньки и первый снег
    s += SL(Z_DAL, okno_izby(120, 170, 560, 440, t,
                             f'<rect x="120" y="170" width="560" height="440"'
                             f' fill="{SUMER}" opacity="{1-utro*.7:.2f}"/>'
                             f'<rect x="120" y="170" width="560" height="440"'
                             f' fill="{RASSV}" opacity="{utro*.8:.2f}"/>'
                             + f'<circle cx="300" cy="300" r="{54:.0f}"'
                               f' fill="#e8eef6" opacity="{1-utro:.2f}"/>'
                             + f'<circle cx="560" cy="330" r="{70:.0f}"'
                               f' fill="{SVET}" opacity="{utro*.7:.2f}"/>'
                             + "".join(f'<rect x="{170+i*96:.0f}" y="440"'
                                       f' width="56" height="44" rx="5"'
                                       f' fill="{SVET}"'
                                       f' opacity="{(1-utro)*(.4+.3*abs(A.w(t,2.4,i*.3))):.2f}"/>'
                                       for i in range(5))
                             + f'<rect x="120" y="500" width="560" height="110"'
                               f' fill="{SNEG}" opacity=".7"/>',
                             .22, True, True))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#5e4a34"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1074, 439, 6, "#4a3824"))
    # ПОДОКОННИК с блюдцем: сок набегает к утру
    s += SL(Z_SRED, f'<rect x="90" y="614" width="640" height="40" rx="10"'
                    f' fill="#cfc9bc" {o(6)}/>')
    s += SL(Z_SRED, _blyudce(300, 606, .92, utro, t))
    s += SL(Z_SRED, _redka_s_yamkoy(290, 594, .80, t, 1.0, .9 - .5 * utro))
    s += SL(Z_SRED, _banka_meda(560, 610, .7, t, False))
    # КРОВАТЬ с подушками — обстановка плана
    s += SL(Z_SRED, _krovat(800, pol, 1000, t, 441, True, 330))
    s += SL(Z_SRED, _podushka(1000, 700, 320, 190, t, .2, .3, .0)
            + _podushka(1250, 684, 290, 180, t, .6, .2, .0))
    s += SL(Z_SRED, _odeyalo_kray(830, 814, 820, 200, t, .2, TKAN2))
    s += SL(Z_SRED, _tumbochka_veschi(1600, pol, 270, t, 200))
    s += SL(Z_SRED, lampa(1700, pol - 212, t, .9, True))
    # ДВЕ ФИГУРЫ: малыш в кровати и мать на краю
    mx, my, mh = 1120, 806, 440
    mtx, mty, mth = 660, pol, 720
    _figury_kadra((mx, my, mh), (mtx, mty, mth))
    nes = A.ease(A.seg(t, 1.1, 1.3))
    # малыш: обе руки обнимают мишку, шарф на горле
    mal = figura(mx, my, mh, t, col="#e2d6c2", kant="#ffd98a", ph=.4,
                 naklon=3.0)
    d1, (c1x, c1y), _ = _ruka_mimo(mx, my, mh, -1, mh * .36, 44, t,
                                   "#e2d6c2", "#ffd98a", .2, 4.0)
    d2, (c2x, c2y), _ = _ruka_mimo(mx, my, mh, 1, mh * .36, 42, t,
                                   "#e2d6c2", "#ffd98a", .6, 4.0)
    mal += d1 + d2
    s += SL(Z_SRED, mal)
    s += SL(Z_SRED, f'<path d="M{mx-mh*.14:.0f},{my-mh*.70:.0f}'
                    f' q{mh*.14:.0f},{mh*.07:.0f} {mh*.28:.0f},0'
                    f' q{-mh*.04:.0f},{mh*.07:.0f} {-mh*.28:.0f},{mh*.02:.0f} Z"'
                    f' fill="{TKAN}" {o(4)}/>'
            + f'<path d="M{mx+mh*.10:.0f},{my-mh*.64:.0f} q{mh*.10:.0f},'
              f'{mh*.14:.0f} {mh*.02:.0f},{mh*.24:.0f}" fill="none"'
              f' stroke="{TKAN}" stroke-width="{mh*.05:.0f}"/>')
    # МИШКА — ровно между кистями малыша, видно, что его держат
    s += SL(Z_SRED, _mishka_plyush((c1x + c2x) * .5, (c1y + c2y) * .5 + 24,
                                   1.0, t, .3 + .5 * abs(A.w(t, 2.0, .2))))
    # мать: левая с блюдцем, правая с ложкой — обе наружу вправо, к малышу
    mat = figura(mtx, mty, mth, t, col="#54505e", kant="#ffd98a", platok=True,
                 ph=.7, naklon=5.0)
    e1, (g1x, g1y), _ = _ruka_mimo(mtx, mty, mth, 1, mth * .40, 34, t,
                                   "#54505e", "#ffd98a", .3, 5.0)
    e2, (g2x, g2y), _ = _ruka_sgib_mimo(mtx, mty, mth, 1, mth * .26, 16,
                                        mth * .26, 4 - 14 * nes, t,
                                        "#54505e", "#ffd98a", .8, 5.0)
    mat += e1 + e2
    s += SL(Z_SRED, mat)
    # блюдце в левой кисти, ложка в правой: варежки перекрывают оба предмета
    s += SL(Z_SRED, _blyudce(g1x + 40, g1y + 16, .62, utro * .8, t))
    s += SL(Z_SRED, _varezhka(g1x, g1y + 2, mth, t, .3))
    s += SL(Z_SRED, f'<g transform="rotate({12 + 8 * nes:.1f} {g2x:.0f} {g2y:.0f})">'
                    f'<rect x="{g2x:.0f}" y="{g2y-7:.0f}" width="96" height="14"'
                    f' rx="7" fill="#b9c6cc" {o(3)}/>'
                    f'<ellipse cx="{g2x+116:.0f}" cy="{g2y:.0f}" rx="30"'
                    f' ry="21" fill="#cfd8dc" {o(4)}/>'
                    f'<ellipse cx="{g2x+116:.0f}" cy="{g2y-2:.0f}" rx="21"'
                    f' ry="13" fill="{ZOL}" opacity=".95"/></g>')
    s += SL(Z_SRED, _varezhka(g2x + 16, g2y + 2, mth, t, .8))
    # нижняя треть
    s += SL(Z_SRED, _polovik(900, pol + 40, 620, 120)
            + _valenki_u_dveri(300, pol + 32, 1.0, t)
            + _kot_zhivoy(1480, pol + 52, t, 1.05, "#3b3430", .4, True, True)
            + _dvorovaya_utvar(1760, pol + 54, 190, t, 443, ["korzina"]))
    s += SL(Z_SRED, teplo(1700, pol - 240, 440, 340, .34))
    s += SL(Z_PERED, _stolb_pered(-8, 110, "#1a120c", 0, H))
    s += vinetka(.42)
    return s


def babushka_s_lozhkoy(t):
    """Мальчик лет шести крупно: зажмурился, плечи подняты, обе руки
    вцепились в край одеяла. Бабушка в очках наклонилась у кровати: в правой
    руке чайная ложка у самых его губ, левую держит ковшиком под ложкой,
    потом гладит его по голове. Ложка подходит к губам СБОКУ — лицо остаётся
    видно целиком (правило «предмет не ложится на лицо»)."""
    rnd = random.Random(447)
    pol = 1022
    s = f'<rect width="{W}" height="{H}" fill="#282019"/>'
    s += SL(Z_DAL, _stena_gornicy(t, 449, True, 740, True))
    s += SL(Z_DAL, _ramki_na_stene(140, 180, 520, t, 451, 4))
    s += SL(Z_DAL, _polka_s_utvaryu(1420, 170, 440, t, 453, 4))
    # простенок над кроватью занят вещами: без них центр кадра жидкий
    s += SL(Z_DAL, _polka_s_utvaryu(940, 180, 380, t, 459, 4)
            + _kover_na_stene(700, 300, 560, 330, t, 461))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#5e4a34"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1078, 455, 6, "#4a3824"))
    s += SL(Z_SRED, _krovat(240, pol, 1120, t, 457, True, 340))
    s += SL(Z_SRED, _podushka(420, 686, 360, 210, t, .3, .4, .0))
    s += SL(Z_SRED, lampa(1760, pol - 30, t, 1.1, True))
    # МАЛЬЧИК КРУПНО: рост взят так, что в кадр входят голова и плечи, а
    # опора (кровать) остаётся под ним — ноги уходят за нижний край
    bx, by_, bh = 700, 1620, 1340
    gx, gy, gh = 1430, pol, 760
    _figury_kadra((bx, by_, bh), (gx, gy, gh))
    glot = A.ease(A.seg(t, 2.6, .8))
    glad = A.ease(A.seg(t, 4.4, 1.2))
    drozh = 7.0 * glot * A.w(t, 11.0, .2)
    s += SL(Z_SRED, f'<g transform="translate({drozh:.1f},0)">')
    mal = figura(bx, by_, bh, t, col="#e2d6c2", kant="#ffd98a", ph=.2,
                 naklon=2.0)
    b1, (y1x, y1y), _ = _ruka_mimo(bx, by_, bh, -1, bh * .22, 58, t,
                                   "#e2d6c2", "#ffd98a", .1, 3.0)
    b2, (y2x, y2y), _ = _ruka_mimo(bx, by_, bh, 1, bh * .22, 56, t,
                                   "#e2d6c2", "#ffd98a", .5, 3.0)
    mal += b1 + b2
    s += SL(Z_SRED, mal + "</g>")
    # одеяло, в которое вцепились обе руки: край стягивается при хвате
    s += SL(Z_SRED, _odeyalo_kray(240, max(y1y, y2y) + 10, 1020, 240, t,
                                  .4 + .5 * abs(A.w(t, 2.2, .1)), TKAN2))
    # БАБУШКА В ОЧКАХ: обе руки наружу влево, к губам мальчика
    bab = figura(gx, gy, gh, t, col="#6a5a4a", kant="#ffd98a", platok=True,
                 ph=.6, naklon=9.0)
    k1, (z1x, z1y), _ = _ruka_sgib_mimo(gx, gy, gh, -1, gh * .24, 18,
                                        gh * .26, 34 - 10 * glot, t,
                                        "#6a5a4a", "#ffd98a", .2, 4.0)
    k2, (z2x, z2y), _ = _ruka_sgib_mimo(gx, gy, gh, -1, gh * .24, 34,
                                        gh * .24, 54 - 46 * glad, t,
                                        "#6a5a4a", "#ffd98a", .7, 5.0)
    bab += k1 + k2
    s += SL(Z_SRED, bab)
    s += SL(Z_SRED, _ochki(gx - 6, gy - gh * .845, 1.15, t))
    # ЛОЖКА у губ: черенок от кисти, черпак останавливается у края лица
    hh_ = bh * .145
    cel_x = bx + hh_ * .98
    cel_y = by_ - bh * .845 + hh_ * .42
    ug_l = math.degrees(math.atan2(cel_y - z1y, cel_x - z1x))
    dl_l = min(150.0, max(70.0, math.hypot(cel_x - z1x, cel_y - z1y) - 26))
    lx2 = z1x + dl_l * math.cos(math.radians(ug_l))
    ly2 = z1y + dl_l * math.sin(math.radians(ug_l))
    s += SL(Z_SRED, f'<line x1="{z1x:.0f}" y1="{z1y:.0f}" x2="{lx2:.0f}"'
                    f' y2="{ly2:.0f}" stroke="#b9c6cc" stroke-width="15"'
                    f' stroke-linecap="round"/>'
            + f'<ellipse cx="{lx2:.0f}" cy="{ly2:.0f}" rx="32" ry="22"'
              f' fill="#cfd8dc" {o(4)}/>'
            + f'<ellipse cx="{lx2:.0f}" cy="{ly2-2:.0f}" rx="22" ry="13"'
              f' fill="{ZOL}" opacity="{.95-.7*glot:.2f}"/>')
    s += SL(Z_SRED, _varezhka(z1x, z1y + 2, gh, t, .2))
    # левая ладонь ковшиком ПОД ложкой, пока не гладит по голове
    if glad < .2:
        s += SL(Z_SRED, f'<path d="M{z2x-34:.0f},{z2y:.0f} q{34:.0f},{40:.0f}'
                        f' {68:.0f},0 q{-34:.0f},{14:.0f} {-68:.0f},0 Z"'
                        f' fill="#e8d8c0" {o(4)}/>')
    else:
        s += SL(Z_SRED, _varezhka(z2x, z2y + 2, gh, t, .7))
    # передёргивание и «бр-р»: капля с ложки и дрожь плеч уже заданы
    if glot > .1:
        for i in range(3):
            s += SL(Z_LETIT, f'<circle cx="{lx2+10+i*14:.0f}"'
                             f' cy="{ly2+28+i*22+40*glot:.0f}"'
                             f' r="{7-i:.0f}" fill="{ZOL}"'
                             f' opacity="{(1-glot)*.8:.2f}"/>')
    # нижняя треть
    s += SL(Z_SRED, _yaschiki(110, pol + 16, t, 463, 3, 1.0)
            + _dvorovaya_utvar(1560, pol + 60, 230, t, 465, ["kadka"]))
    s += SL(Z_SRED, _tabyret(1180, pol + 8, t, 160, 180)
            + _kruzhka(1180, pol - 150, 1.0, 0, "#e8eef0", 1)
            + _polovik(900, pol + 40, 560, 120)
            + _valenki_u_dveri(1680, pol + 34, 1.05, t)
            + _kot_zhivoy(1310, pol + 54, t, 1.05, "#3b3430", .5))
    s += SL(Z_SRED, teplo(1760, pol - 60, 420, 320, .32))
    s += SL(Z_PERED, _stolb_pered(1898, 96, "#1a120c", 0, H))
    s += vinetka(.42)
    return s


def banya_na_ogorode(t):
    """Бревенчатая банька на краю огорода: дым валит из трубы, бочка с
    водой, ковш на гвозде, веники под стрехой, тропинка в снегу. Дверь
    приоткрыта, в проёме клубится пар и стоит берёзовый веник. Мужик в
    тулупе идёт по тропинке: под левой рукой таз, в правой свёрток чистого
    белья. Из двери выкатываются и убегают в сугроб три серые хвори."""
    rnd = random.Random(467)
    gor = 700
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, True, 71)
    s += oblaka(t, 150, 5, 73, .42, "#cdd7e4", 13.0)
    s += SL(Z_DAL, _derevnya_ryad(gor - 150, t, 75, ((140, 300), (1760, 260))))
    s += SL(Z_DAL, goloe_derevo(360, gor - 40, 520, t, 77, 9, "#3a3b43", True)
            + goloe_derevo(1700, gor - 10, 460, t, 79, 8, "#3a3b43", True))
    s += SL(Z_DAL, pleten(-20, gor - 190, 620, 180, 9)
            + _zabor_dosok(1480, gor - 180, 460, 170, 81, 56))
    s += SL(Z_DAL, _stog(220, gor + 40, .9, t, True))
    s += SL(Z_DAL, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                   f' fill="#55564e"/>' + sneg_lezhit(gor + 20, 28)
            + _zemlya_faktura(gor + 70, 1070, 83, 16, "#3f4238"))
    # ГЛАВНЫЙ ПРЕДМЕТ: банька с трубой, дымом, окошком и вениками
    s += SL(Z_SRED, _banya_srub(700, gor + 80, 660, t, 85, .0))
    # ДВЕРЬ ПРИОТКРЫТА: нарисованный пар и берёзовый веник в самом проёме —
    # настоящего кадра здесь НЕ ставим: в раскадровке по этому плану сток
    # помечен «убрано», а лишняя метка — брак гейта
    dx_, dy_, dw, dh = 860, gor - 300, 230, 380
    putd = kontur_proema(dx_, dy_, dw, dh, "arka")
    s += SL(Z_SRED, f'<path d="{putd}" fill="#140d08"/>'
            + f'<path d="{putd}" fill="{SVET}" opacity=".16"/>')
    s += SL(Z_SRED, par(dx_ + dw * .5, dy_ + dh * .72, t, 5, .62, 220, .55, 1.6))
    s += SL(Z_SRED, _venik(dx_ + dw * .62, dy_ + dh - 20, 260, t, "#cdbf9c",
                           "#b8352c", True, .14, .2, .86, 87))
    s += SL(Z_SRED, f'<path d="{putd}" fill="none" stroke="#4e3c2c"'
                    f' stroke-width="26"/>'
            + dver(dx_ - 210, dy_ + 20, 200, dh - 20, .55, "url(#derev)",
                   True, False))
    s += SL(Z_SRED, par(dx_ + dw * .5, dy_ + dh * .40, t, 4, .46, 180, .4, 1.3))
    # бочка, ковш на гвозде, поленница — обстановка двора
    s += SL(Z_SRED, _bochka_vody(1430, gor + 150, 1.0, t, True))
    s += SL(Z_SRED, _kovsh_na_gvozde(1330, gor - 120, 1.0, t, .3))
    s += SL(Z_SRED, _polenica(1500, gor + 230, 380, 210, 89, 26))
    s += SL(Z_SRED, _kadushki_i_grabli(360, gor + 250, t, 91))
    # ТРОПИНКА В СНЕГУ и следы по ней
    s += SL(Z_SRED, f'<path d="M120,1070 Q520,920 {dx_+dw*.5:.0f},{gor+90:.0f}'
                    f' L{dx_+dw*.5+150:.0f},{gor+90:.0f} Q700,940 460,1072 Z"'
                    f' fill="#6b6a60" {o(5)}/>'
            + f'<path d="M150,1064 Q540,916 {dx_+dw*.5+20:.0f},{gor+100:.0f}"'
              f' fill="none" stroke="#7d7c70" stroke-width="22" opacity=".8"/>')
    s += SL(Z_SRED, _sledy(300, 1040, dx_ + dw * .5, gor + 110, 9, 93,
                           "#43423a", 1.1))
    # ОДНА ФИГУРА: мужик в тулупе на тропинке, таз под левой, свёрток в правой
    shag = A.ease(A.seg(t, .3, 2.4))
    ux = 560 + 170 * shag
    uy = 1010 - 120 * shag
    uh = 760 - 150 * shag
    _figury_kadra((ux, uy, uh))
    muzh = figura(ux, uy, uh, t, col="#4e4036", kant="#cfe4f5", ph=.3,
                  shapka=True, tulup=True, naklon=4.0)
    n1, (t1x, t1y), _ = _ruka_mimo(ux, uy, uh, -1, uh * .30, 56, t,
                                   "#4e4036", "#cfe4f5", .2, 4.0)
    n2, (t2x, t2y), _ = _ruka_mimo(ux, uy, uh, 1, uh * .34, 60, t,
                                   "#4e4036", "#cfe4f5", .6, 5.0)
    muzh += n1 + n2
    s += SL(Z_SRED, muzh)
    s += SL(Z_SRED, _taz_i_svertok(t1x - 46, t1y + 60, .62 * uh / 760.0, t, -12))
    s += SL(Z_SRED, _varezhka(t1x, t1y + 4, uh, t, .2))
    s += SL(Z_SRED, _svertok_belya(t2x + 36, t2y + 42, .62 * uh / 760.0, t, -10))
    s += SL(Z_SRED, _varezhka(t2x, t2y + 6, uh, t, .6))
    s += SL(Z_SRED, para_izo_rta(ux + 40, uy - uh * .80, t, .4, 1.1, .55))
    # ТРИ ХВОРИ: рост через одного крупная/мелкая, шаг рваный, разбег < 0,4 с
    for i, (hx_, hs, hp) in enumerate(((1030, 1.30, .0), (1130, .64, .22),
                                       (1230, 1.08, .40))):
        beg = A.ease(A.seg(t, .5 + i * .32, 1.6))
        s += SL(Z_SRED, _hvor(hx_, gor + 120 + i * 26, hs, t, hp, beg))
    s += SL(Z_SRED, f'<path d="M1560,1052 q120,-60 250,-8" fill="none"'
                    f' stroke="{SNEG}" stroke-width="40" opacity=".8"/>')
    s += SL(Z_SRED, _snegovik(1800, gor + 320, .74, t))
    s += SL(Z_SRED, teplo(900, gor - 180, 480, 380, .30))
    s += SL(Z_LETIT, mokryy_sneg(t, 30, 95, .6, 1.0))
    s += SL(Z_PERED, _vetka_pered(-40, 150, 620, 26, t, 97, "#241c16", 7))
    s += vinetka(.44)
    return s


# ── ПОМОЩНИКИ ВТОРОЙ ПАРТИИ ───────────────────────────────────────────────

def _dverca_pechi(x, y, w_, h_, t, otkr=.0, seed=3):
    """ЧУГУННАЯ ДВЕРЦА БАННОЙ ПЕЧИ — главный предмет: литая рама с
    завитками по углам, решётчатая отдушина, ручка-завёртка, а за открытой
    створкой видна топка с углями. Створка ходит на петлях, не ездит целиком."""
    ug = -82.0 * otkr
    s = (f'{kladka(x - 40, y - h_ - 50, w_ + 80, h_ + 70, 54, "#6a5c4c")}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="14" fill="#1b1512" {o(8)}/>'
         f'{ugli(x + 20, y - 26, w_ - 40, t, 8, seed)}'
         f'{ogon(x + w_ * .5, y - h_ * .40, t, 1.25, .2, 7)}')
    s += (f'<rect x="{x-26:.0f}" y="{y-h_-26:.0f}" width="{w_+52:.0f}"'
          f' height="{h_+40:.0f}" rx="16" fill="none" stroke="#3d3a38"'
          f' stroke-width="26"/>')
    for i in (-1, 1):
        for j in (-1, 1):
            cx = x + w_ * .5 + i * (w_ * .5 + 10)
            cy = y - h_ * .5 + j * (h_ * .5 + 6)
            s += (f'<path d="M{cx:.0f},{cy:.0f} q{i*30:.0f},{j*6:.0f}'
                  f' {i*26:.0f},{j*30:.0f}" fill="none" stroke="#4e4a47"'
                  f' stroke-width="11"/>')
    # створка
    s += (f'<g transform="rotate({ug:.1f} {x:.0f} {y-h_*.5:.0f})">'
          f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' rx="12" fill="#4e4a47" {o(7)}/>'
          f'<rect x="{x+18:.0f}" y="{y-h_+18:.0f}" width="{w_-36:.0f}"'
          f' height="{h_-36:.0f}" rx="9" fill="#5f5a56" opacity=".9"/>')
    for i in range(5):
        s += (f'<rect x="{x+w_*.26:.0f}" y="{y-h_*.74+i*h_*.09:.0f}"'
              f' width="{w_*.48:.0f}" height="{h_*.045:.0f}" rx="5"'
              f' fill="#2a2726"/>')
    s += (f'<circle cx="{x+w_*.84:.0f}" cy="{y-h_*.5:.0f}" r="{h_*.09:.0f}"'
          f' fill="#8f979d" {o(5)}/>'
          f'<rect x="{x+w_*.80:.0f}" y="{y-h_*.56:.0f}" width="{w_*.22:.0f}"'
          f' height="{h_*.055:.0f}" rx="6" fill="#6f767c" {o(3)}/>')
    for j in (-1, 1):
        s += (f'<rect x="{x-14:.0f}" y="{y-h_*.5+j*h_*.34:.0f}" width="30"'
              f' height="{h_*.14:.0f}" rx="7" fill="#3d3a38" {o(4)}/>')
    s += "</g>"
    s += (f'<ellipse cx="{x+w_*.5:.0f}" cy="{y+16:.0f}" rx="{w_*.56:.0f}"'
          f' ry="22" fill="#2a2118" opacity=".6"/>')
    return s


def _poleno(x, y, s_=1.0, ug=0.0, bereza=True):
    """Берёзовое полено: колотая плашка, торец с годовыми кольцами и
    трещиной, белая кора с чёрными штрихами."""
    w2, h2 = 190 * s_, 56 * s_
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<rect x="{x-w2/2:.0f}" y="{y-h2/2:.0f}" width="{w2:.0f}"'
         f' height="{h2:.0f}" rx="{10*s_:.0f}"'
         f' fill="{"#e8e2d6" if bereza else "url(#derev)"}" {o(5)}/>')
    if bereza:
        for i in range(5):
            s += (f'<path d="M{x-w2*.40+i*w2*.19:.0f},{y-h2*.44:.0f}'
                  f' q{6*s_:.0f},{h2*.30:.0f} {-2*s_:.0f},{h2*.50:.0f}"'
                  f' fill="none" stroke="#3a352e" stroke-width="{max(2,5*s_):.0f}"'
                  f' opacity=".8"/>')
    s += (f'<ellipse cx="{x+w2/2:.0f}" cy="{y:.0f}" rx="{10*s_:.0f}"'
          f' ry="{h2/2:.0f}" fill="#c9a47a" {o(4)}/>')
    for i in range(3):
        s += (f'<ellipse cx="{x+w2/2:.0f}" cy="{y:.0f}" rx="{(7-i*2)*s_:.0f}"'
              f' ry="{h2*(.36-i*.10):.0f}" fill="none" stroke="#a98a5e"'
              f' stroke-width="{max(2,3*s_):.0f}"/>')
    s += (f'<line x1="{x+w2/2:.0f}" y1="{y-h2*.34:.0f}" x2="{x+w2/2:.0f}"'
          f' y2="{y+h2*.34:.0f}" stroke="#8a6038" stroke-width="{max(2,4*s_):.0f}"/>'
          f'</g>')
    return s


def _vanna(x, y, w_, t, h_=250):
    """БЕЛАЯ ВАННА — главный предмет: чугунный борт с заворотом, четыре
    ножки-лапы, смеситель с душевой лейкой, вода с рябью и густой пар."""
    s = (f'{ten(x + w_ * .5, y + 22, w_ * .52, 24, .5)}'
         f'<path d="M{x:.0f},{y-h_:.0f} q{-26:.0f},{h_*.56:.0f} {30:.0f},{h_:.0f}'
         f' L{x+w_-30:.0f},{y:.0f} q{56:.0f},{-h_*.44:.0f} {30:.0f},{-h_:.0f} Z"'
         f' fill="#eef2f4" {o(8)}/>'
         f'<ellipse cx="{x+w_*.5:.0f}" cy="{y-h_:.0f}" rx="{w_*.5:.0f}"'
         f' ry="{w_*.09:.0f}" fill="#dde6ea" {o(6)}/>'
         f'<ellipse cx="{x+w_*.5:.0f}" cy="{y-h_+10:.0f}" rx="{w_*.44:.0f}"'
         f' ry="{w_*.07:.0f}" fill="#b9c6cc" opacity=".9"/>'
         f'<ellipse cx="{x+w_*.5:.0f}" cy="{y-h_+16:.0f}" rx="{w_*.40:.0f}"'
         f' ry="{w_*.055:.0f}" fill="{VODA}" opacity=".55"/>')
    for i in range(4):
        s += (f'<path d="M{x+w_*(.18+i*.18):.0f},{y-h_+16:.0f}'
              f' q{w_*.05:.0f},{-7 - 4 * A.w(t, 2.0, i * .3):.0f} {w_*.10:.0f},0"'
              f' fill="none" stroke="#dff0fa" stroke-width="7" opacity=".7"/>')
    for i in (0, 1):
        for j in (0, 1):
            lx = x + 40 + i * (w_ - 80)
            s += (f'<path d="M{lx-16:.0f},{y:.0f} q{4:.0f},{34:.0f} {-10:.0f},{46:.0f}'
                  f' q{26:.0f},{10:.0f} {46:.0f},{-4:.0f} q{-16:.0f},{-14:.0f}'
                  f' {-12:.0f},{-42:.0f} Z" fill="#cfd5da" {o(5)}/>')
            break
    s += (f'<rect x="{x+w_*.84:.0f}" y="{y-h_-150:.0f}" width="24" height="160"'
          f' rx="10" fill="#9aa3aa" {o(4)}/>'
          f'<path d="M{x+w_*.86:.0f},{y-h_-150:.0f} q{-10:.0f},{-54:.0f}'
          f' {-86:.0f},{-46:.0f}" fill="none" stroke="#9aa3aa" stroke-width="20"/>'
          f'<ellipse cx="{x+w_*.80-86:.0f}" cy="{y-h_-192:.0f}" rx="34" ry="14"'
          f' fill="#8f979d" {o(4)}/>')
    kap = (t * .7) % 1.0
    s += (f'<ellipse cx="{x+w_*.80-86:.0f}" cy="{y-h_-176+kap*120:.0f}" rx="7"'
          f' ry="{11+6*kap:.0f}" fill="#d6e8f4" opacity="{1-kap:.2f}"/>')
    s += par(x + w_ * .44, y - h_ - 10, t, 6, .62, 300, .45, 1.9)
    s += par(x + w_ * .66, y - h_ - 20, t, 5, .5, 260, .55, 1.6)
    return s


def _mochalka(x, y, s_=1.0, t=0.0, ph=.0):
    """Лыковая мочалка: жгут из светлого лыка с распушёнными концами и
    верёвочной петлёй."""
    sway = 3.0 * A.w(t, 2.6, ph)
    s = f'<g transform="rotate({sway:.1f} {x:.0f} {y:.0f})">'
    for i in range(7):
        s += (f'<path d="M{x-72*s_+i*10*s_:.0f},{y:.0f}'
              f' q{40*s_:.0f},{(-26+i*5)*s_:.0f} {120*s_:.0f},{(4-i*2)*s_:.0f}"'
              f' fill="none" stroke="{"#d8c08a" if i % 2 else "#c9ad74"}"'
              f' stroke-width="{max(4,11*s_):.0f}" stroke-linecap="round"/>')
    for e in (-1, 1):
        for j in range(5):
            s += (f'<line x1="{x+e*58*s_:.0f}" y1="{y+(-16+j*8)*s_:.0f}"'
                  f' x2="{x+e*92*s_:.0f}" y2="{y+(-24+j*12)*s_:.0f}"'
                  f' stroke="#b89a6a" stroke-width="{max(2,4*s_):.0f}"/>')
    s += (f'<circle cx="{x:.0f}" cy="{y-30*s_:.0f}" r="{18*s_:.0f}" fill="none"'
          f' stroke="#9c8a62" stroke-width="{max(3,6*s_):.0f}"/></g>')
    return s


def _mylo_v_mylnice(x, y, s_=1.0, t=0.0):
    """Мыло в мыльнице: пластмассовая ванночка с рёбрами, брусок мыла с
    фаской и мокрый блик."""
    return (f'{ten(x, y + 8 * s_, 58 * s_, 10 * s_, .4)}'
            f'<path d="M{x-62*s_:.0f},{y-26*s_:.0f} q{8*s_:.0f},{34*s_:.0f}'
            f' {62*s_:.0f},{34*s_:.0f} q{54*s_:.0f},0 {62*s_:.0f},{-34*s_:.0f} Z"'
            f' fill="#6a9cc2" {o(5)}/>'
            + "".join(f'<line x1="{x-40*s_+i*20*s_:.0f}" y1="{y-16*s_:.0f}"'
                      f' x2="{x-40*s_+i*20*s_:.0f}" y2="{y+4*s_:.0f}"'
                      f' stroke="#4e7a9c" stroke-width="{max(2,4*s_):.0f}"/>'
                      for i in range(5))
            + f'<path d="M{x-46*s_:.0f},{y-30*s_:.0f} q{8*s_:.0f},{-26*s_:.0f}'
              f' {46*s_:.0f},{-26*s_:.0f} q{40*s_:.0f},0 {46*s_:.0f},{26*s_:.0f} Z"'
              f' fill="#efe3c8" {o(4)}/>'
            + f'<path d="M{x-28*s_:.0f},{y-44*s_:.0f} q{18*s_:.0f},{-10*s_:.0f}'
              f' {40*s_:.0f},{-4*s_:.0f}" fill="none" stroke="#ffffff"'
              f' stroke-width="{7*s_:.0f}"'
              f' opacity="{.4+.3*abs(A.w(t,2.4,.3)):.2f}"/>')


def _utochka(x, y, s_=1.0, t=0.0, ph=.0):
    """Резиновая уточка: жёлтое тулово, клюв оранжевым, глаз точкой,
    покачивается на воде."""
    kol = 4.0 * A.w(t, 1.9, ph)
    r = 30 * s_
    return (f'<g transform="rotate({kol:.1f} {x:.0f} {y:.0f})">'
            f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r*1.30:.0f}" ry="{r*.80:.0f}"'
            f' fill="#e8c64e" {o(4)}/>'
            f'<path d="M{x+r*.80:.0f},{y-r*.20:.0f} q{r*.60:.0f},{-r*.50:.0f}'
            f' {r*.30:.0f},{-r*.90:.0f}" fill="none" stroke="#e8c64e"'
            f' stroke-width="{r*.46:.0f}"/>'
            f'<circle cx="{x+r*1.02:.0f}" cy="{y-r*1.08:.0f}" r="{r*.46:.0f}"'
            f' fill="#e8c64e" {o(3)}/>'
            f'<path d="M{x+r*1.40:.0f},{y-r*1.06:.0f} l{r*.46:.0f},{r*.14:.0f}'
            f' l{-r*.44:.0f},{r*.20:.0f} Z" fill="{ORA}" {o(3)}/>'
            f'<circle cx="{x+r*1.02:.0f}" cy="{y-r*1.20:.0f}" r="{r*.09:.0f}"'
            f' fill="{K}"/>'
            f'<path d="M{x-r*1.20:.0f},{y-r*.30:.0f} q{r*.40:.0f},{-r*.40:.0f}'
            f' {r*.70:.0f},{-r*.06:.0f}" fill="none" stroke="#c9a331"'
            f' stroke-width="{max(2,5*s_):.0f}"/></g>')


def _halat_na_dveri(x, y, h_, t, ph=.0, col="#e3ddc6"):
    """Махровый халат на крючке двери: плечи, пояс висит петлёй, махровая
    фактура точками, чуть качается."""
    kach = 1.8 * A.w(t, 3.4, ph)
    s = (f'<g transform="rotate({kach:.1f} {x:.0f} {y:.0f})">'
         f'<path d="M{x-16:.0f},{y-24:.0f} q{16:.0f},{-22:.0f} {32:.0f},{-4:.0f}"'
         f' fill="none" stroke="{ZHELEZ}" stroke-width="10"/>'
         f'<path d="M{x:.0f},{y:.0f} q{-80:.0f},{20:.0f} {-96:.0f},{90:.0f}'
         f' L{x-78:.0f},{y+h_:.0f} L{x+78:.0f},{y+h_:.0f} L{x+96:.0f},{y+90:.0f}'
         f' q{-16:.0f},{-70:.0f} {-96:.0f},{-90:.0f} Z" fill="{col}" {o(6)}/>'
         f'<path d="M{x:.0f},{y+6:.0f} L{x-24:.0f},{y+h_:.0f}" fill="none"'
         f' stroke="#c9c1a6" stroke-width="12"/>'
         f'<path d="M{x:.0f},{y+6:.0f} L{x+24:.0f},{y+h_:.0f}" fill="none"'
         f' stroke="#c9c1a6" stroke-width="12"/>'
         f'<path d="M{x-70:.0f},{y+h_*.52:.0f} q{70:.0f},{18:.0f} {140:.0f},0"'
         f' fill="none" stroke="{TKAN2}" stroke-width="16"/>'
         f'<path d="M{x+60:.0f},{y+h_*.56:.0f} q{30:.0f},{70:.0f} {-10:.0f},{110:.0f}"'
         f' fill="none" stroke="{TKAN2}" stroke-width="13"/>')
    rnd = random.Random(int(x) + 7)
    for i in range(26):
        s += (f'<circle cx="{x+rnd.uniform(-82,82):.0f}"'
              f' cy="{y+rnd.uniform(30,h_-10):.0f}" r="{rnd.uniform(3,6):.0f}"'
              f' fill="#cfc7ad" opacity=".7"/>')
    return s + "</g>"


def _zerkalo_zapot(x, y, w_, h_, t, zapot=.0):
    """Зеркало над раковиной: рама, отражение кафеля полосами, запотевание
    от низа вверх и протёртая полоса пальцем — без буквы, дугой."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="10" fill="#cfe0e8" {o(7)}/>'
         f'<rect x="{x+14:.0f}" y="{y+14:.0f}" width="{w_-28:.0f}"'
         f' height="{h_-28:.0f}" rx="7" fill="#b9d6e8" opacity=".92"/>')
    for i in range(4):
        s += (f'<rect x="{x+24:.0f}" y="{y+30+i*(h_-56)/4.0:.0f}"'
              f' width="{w_-48:.0f}" height="{(h_-56)/6.0:.0f}" rx="5"'
              f' fill="#a4c4d8" opacity=".55"/>')
    s += (f'<path d="M{x+30:.0f},{y+40:.0f} L{x+w_*.5:.0f},{y+h_*.3:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="12" opacity=".4"/>')
    if zapot > .02:
        s += (f'<rect x="{x+14:.0f}" y="{y+h_-14-(h_-28)*zapot:.0f}"'
              f' width="{w_-28:.0f}" height="{(h_-28)*zapot:.0f}" rx="6"'
              f' fill="#e8f1f6" opacity="{.50+.30*zapot:.2f}"/>')
        if zapot > .5:
            s += (f'<path d="M{x+w_*.26:.0f},{y+h_*.62:.0f}'
                  f' q{w_*.22:.0f},{-h_*.20:.0f} {w_*.46:.0f},{h_*.04:.0f}"'
                  f' fill="none" stroke="#9fc4d8" stroke-width="22"'
                  f' opacity=".8"/>')
    s += (f'<rect x="{x-10:.0f}" y="{y-12:.0f}" width="{w_+20:.0f}" height="20"'
          f' rx="8" fill="#9aa3aa" {o(4)}/>')
    return s


def _stopka_belya(x, y, w_, t, zavitki=True, seed=5):
    """СТОПКА ЧИСТОГО БЕЛЬЯ — главный предмет: сорочка сложенная квадратом,
    поверх неё полотенце с каймой, сверху скатанные носки клубком. От стопки
    поднимаются рисованные завитки свежести."""
    rnd = random.Random(seed)
    h2 = 0
    s = f'{ten(x + w_ * .5, y + 14, w_ * .52, 20, .45)}'
    cols = ["#efe8d8", "#e3ddc6", "#f4eedc", "#dfd6c0"]
    for i in range(4):
        hh = 44 - i * 4
        yy = y - h2 - hh
        dx = rnd.uniform(-10, 10)
        s += (f'<rect x="{x+dx+i*8:.0f}" y="{yy:.0f}" width="{w_-i*16:.0f}"'
              f' height="{hh:.0f}" rx="9" fill="{cols[i]}" {o(5)}/>'
              f'<line x1="{x+dx+i*8+14:.0f}" y1="{yy+hh*.5:.0f}"'
              f' x2="{x+dx+w_-i*16-14:.0f}" y2="{yy+hh*.5:.0f}"'
              f' stroke="#cfc7ad" stroke-width="5" opacity=".8"/>')
        h2 += hh + 4
    # полотенце с каймой поверх стопки
    s += (f'<rect x="{x+16:.0f}" y="{y-h2-50:.0f}" width="{w_-40:.0f}"'
          f' height="54" rx="10" fill="{RUSH}" {o(5)}/>'
          f'<rect x="{x+24:.0f}" y="{y-h2-34:.0f}" width="{w_-56:.0f}"'
          f' height="14" fill="{TKAN}" opacity=".85"/>'
          f'<rect x="{x+24:.0f}" y="{y-h2-50:.0f}" width="{w_-56:.0f}"'
          f' height="8" fill="{TKAN2}" opacity=".7"/>')
    # скатанные носки клубком — две шайбы с резинкой
    for i in (0, 1):
        nx = x + w_ * (.30 + i * .38)
        s += (f'<ellipse cx="{nx:.0f}" cy="{y-h2-76:.0f}" rx="44" ry="28"'
              f' fill="#8fa3c2" {o(5)}/>'
              f'<ellipse cx="{nx:.0f}" cy="{y-h2-82:.0f}" rx="32" ry="17"'
              f' fill="#a4b8d2" opacity=".9"/>')
        for j in range(3):
            s += (f'<path d="M{nx-34:.0f},{y-h2-82+j*9:.0f} q{34:.0f},{-8:.0f}'
                  f' {68:.0f},0" fill="none" stroke="#7288a8"'
                  f' stroke-width="4" opacity=".8"/>')
    if zavitki:
        for i in range(5):
            p = ((t * .5 + i / 5.0) % 1.0)
            zx = x + w_ * (.18 + i * .17)
            zy = y - h2 - 110 - p * 190
            s += (f'<path d="M{zx:.0f},{zy:.0f} q{22:.0f},{-26:.0f} {2:.0f},{-48:.0f}'
                  f' q{-22:.0f},{-22:.0f} {6:.0f},{-44:.0f}" fill="none"'
                  f' stroke="#cfe4f5" stroke-width="{8-3*p:.0f}"'
                  f' stroke-linecap="round" opacity="{(1-p)*.85:.2f}"/>')
    return s


def _shkafchiki_bani(x, y, w_, h_, t, n=5, seed=7):
    """Шкафчики раздевалки: дверцы с филёнкой, вентиляционные прорези,
    кольцо-ручка и жестяной номерок на гвоздике — номер не рисуем, на
    номерке волнистая насечка."""
    rnd = random.Random(seed)
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' fill="#8a6038" {o(7)}/>')
    dw = w_ / float(n)
    for i in range(n):
        dx = x + i * dw
        s += (f'<rect x="{dx+8:.0f}" y="{y+10:.0f}" width="{dw-16:.0f}"'
              f' height="{h_-20:.0f}" rx="9" fill="url(#dosk)" {o(5)}/>'
              f'<rect x="{dx+28:.0f}" y="{y+36:.0f}" width="{dw-56:.0f}"'
              f' height="{h_-80:.0f}" rx="7" fill="#9c7049" opacity=".85"/>')
        for j in range(3):
            s += (f'<rect x="{dx+dw*.3:.0f}" y="{y+52+j*22:.0f}"'
                  f' width="{dw*.4:.0f}" height="9" rx="4" fill="#5b4428"/>')
        s += (f'<circle cx="{dx+dw-34:.0f}" cy="{y+h_*.52:.0f}" r="13"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="8"/>')
        kol = 6.0 * A.w(t, 2.4, i * .4)
        s += (f'<g transform="rotate({kol:.1f} {dx+dw*.5:.0f} {y+h_*.18:.0f})">'
              f'<line x1="{dx+dw*.5:.0f}" y1="{y+h_*.18:.0f}"'
              f' x2="{dx+dw*.5:.0f}" y2="{y+h_*.18+30:.0f}" stroke="#8f979d"'
              f' stroke-width="4"/>'
              f'<circle cx="{dx+dw*.5:.0f}" cy="{y+h_*.18+46:.0f}" r="19"'
              f' fill="#c9ad74" {o(4)}/>'
              f'<path d="M{dx+dw*.5-10:.0f},{y+h_*.18+46:.0f} q{5:.0f},{-6:.0f}'
              f' {10:.0f},0 q{5:.0f},{6:.0f} {10:.0f},0" fill="none"'
              f' stroke="#8a7a46" stroke-width="4"/></g>')
    return s


def _taz_bannyy(x, y, s_=1.0, t=0.0, soderzh=True):
    """ОЦИНКОВАННЫЙ ТАЗ — главный предмет: конусное тулово с обручем и
    двумя ушками, оцинковка пятнами и блик дугой. Внутри лыковая мочалка,
    кусок мыла и берёзовый веник через край."""
    w2, h2 = 300 * s_, 128 * s_
    s = (f'{ten(x, y + 12 * s_, w2 * .56, 18 * s_, .5)}'
         f'<path d="M{x-w2*.5:.0f},{y-h2:.0f} q{6*s_:.0f},{h2*1.08:.0f}'
         f' {w2*.5:.0f},{h2*1.02:.0f} q{w2*.44:.0f},{2*s_:.0f}'
         f' {w2*.5:.0f},{-h2*1.02:.0f} Z" fill="#b6bcc2" {o(8)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-h2:.0f}" rx="{w2*.5:.0f}"'
         f' ry="{w2*.14:.0f}" fill="#cfd5da" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-h2+8*s_:.0f}" rx="{w2*.43:.0f}"'
         f' ry="{w2*.11:.0f}" fill="#8f979d" opacity=".9"/>')
    rnd = random.Random(int(x) + 11)
    for i in range(9):
        s += (f'<ellipse cx="{x+rnd.uniform(-w2*.4,w2*.4):.0f}"'
              f' cy="{y+rnd.uniform(-h2*.8,-h2*.1):.0f}"'
              f' rx="{rnd.uniform(12,26)*s_:.0f}" ry="{rnd.uniform(7,15)*s_:.0f}"'
              f' fill="#c9ced4" opacity=".55"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*w2*.50:.0f},{y-h2+4*s_:.0f} q{i*42*s_:.0f},'
              f'{6*s_:.0f} {i*34*s_:.0f},{38*s_:.0f}" fill="none"'
              f' stroke="{ZHELEZ}" stroke-width="{13*s_:.0f}"/>')
    s += (f'<path d="M{x-w2*.36:.0f},{y-h2*.52:.0f} q{w2*.14:.0f},{h2*.40:.0f}'
          f' {w2*.30:.0f},{h2*.44:.0f}" fill="none" stroke="#eef2f4"'
          f' stroke-width="{12*s_:.0f}" opacity=".55"/>')
    if soderzh:
        s += _mochalka(x - w2 * .18, y - h2 - 6 * s_, s_ * .74, t, .2)
        s += _mylo_v_mylnice(x + w2 * .24, y - h2 + 4 * s_, s_ * .62, t)
        s += _venik(x + w2 * .40, y - h2 - 10 * s_, 230 * s_, t, "#cdbf9c",
                    "#b8352c", False, .12, .3, s_ * .72, 113)
    return s


def _stakan_podstakannik(x, y, s_=1.0, t=0.0, chay=.8, lozhka=True):
    """Гранёный стакан в подстаканнике: грани вертикальными блеснами,
    мельхиоровый подстаканник с завитком-ручкой, чай с ободком и ложечка."""
    w2, h2 = 72 * s_, 112 * s_
    s = (f'{ten(x, y + 6 * s_, w2 * .6, 9 * s_, .4)}'
         f'<path d="M{x-w2/2:.0f},{y-h2:.0f} L{x+w2/2:.0f},{y-h2:.0f}'
         f' L{x+w2*.42:.0f},{y:.0f} L{x-w2*.42:.0f},{y:.0f} Z"'
         f' fill="url(#stekl)" opacity=".9" {o(5)}/>'
         f'<path d="M{x-w2*.44:.0f},{y-h2*chay:.0f} L{x+w2*.44:.0f},{y-h2*chay:.0f}'
         f' L{x+w2*.42:.0f},{y-4*s_:.0f} L{x-w2*.42:.0f},{y-4*s_:.0f} Z"'
         f' fill="#8a4a1c" opacity=".88"/>'
         f'<ellipse cx="{x:.0f}" cy="{y-h2*chay:.0f}" rx="{w2*.44:.0f}"'
         f' ry="{w2*.11:.0f}" fill="#b5803a" opacity=".9"/>')
    for i in range(4):
        s += (f'<line x1="{x-w2*.30+i*w2*.20:.0f}" y1="{y-h2+6*s_:.0f}"'
              f' x2="{x-w2*.27+i*w2*.18:.0f}" y2="{y-6*s_:.0f}"'
              f' stroke="#ffffff" stroke-width="{max(2,4*s_):.0f}" opacity=".35"/>')
    s += (f'<path d="M{x-w2*.52:.0f},{y-h2*.70:.0f} L{x+w2*.52:.0f},{y-h2*.70:.0f}'
          f' L{x+w2*.46:.0f},{y+4*s_:.0f} L{x-w2*.46:.0f},{y+4*s_:.0f} Z"'
          f' fill="none" stroke="#b9c6cc" stroke-width="{11*s_:.0f}"/>'
          f'<path d="M{x+w2*.52:.0f},{y-h2*.54:.0f} q{44*s_:.0f},{10*s_:.0f}'
          f' {4*s_:.0f},{46*s_:.0f}" fill="none" stroke="#b9c6cc"'
          f' stroke-width="{10*s_:.0f}"/>')
    for i in range(3):
        s += (f'<circle cx="{x-w2*.30+i*w2*.30:.0f}" cy="{y-h2*.44:.0f}"'
              f' r="{6*s_:.0f}" fill="#cfd8dc" opacity=".9"/>')
    if lozhka:
        ug = 14 + 4 * A.w(t, 1.8, .2)
        s += (f'<g transform="rotate({ug:.1f} {x+w2*.2:.0f} {y-h2:.0f})">'
              f'<rect x="{x+w2*.14:.0f}" y="{y-h2-56*s_:.0f}" width="{8*s_:.0f}"'
              f' height="{78*s_:.0f}" rx="4" fill="#cfd8dc" {o(3)}/>'
              f'<ellipse cx="{x+w2*.18:.0f}" cy="{y-h2-62*s_:.0f}"'
              f' rx="{13*s_:.0f}" ry="{9*s_:.0f}" fill="#dde6ea" {o(3)}/></g>')
    s += par(x, y - h2 - 30 * s_, t, 3, .45, 120 * s_, .5)
    return s


def _sushka_odna(x, y, s_=1.0, t=0.0, makaet=.0, ug=0.0):
    """Сушка: твёрдое кольцо с маковой крошкой и блеском; когда её макают,
    низ кольца темнеет от чая и с него срывается капля."""
    r = 34 * s_
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="none"'
         f' stroke="#d7a860" stroke-width="{r*.52:.0f}"/>'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="none"'
         f' stroke="{K}" stroke-width="{max(2,3.6*s_):.0f}" opacity=".9"/>'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*.74:.0f}" fill="none"'
         f' stroke="{K}" stroke-width="{max(2,3*s_):.0f}" opacity=".7"/>')
    rnd = random.Random(int(x) + 13)
    for i in range(8):
        a = rnd.uniform(0, 6.28)
        s += (f'<circle cx="{x+math.cos(a)*r*.88:.0f}" cy="{y+math.sin(a)*r*.88:.0f}"'
              f' r="{2.6*s_:.0f}" fill="#5a3a18"/>')
    if makaet > .05:
        s += (f'<path d="M{x-r*.9:.0f},{y+r*.5:.0f} a{r:.0f},{r:.0f} 0 0 0'
              f' {r*1.8:.0f},0" fill="none" stroke="#8a4a1c"'
              f' stroke-width="{r*.44:.0f}" opacity="{makaet:.2f}"/>'
              f'<ellipse cx="{x:.0f}" cy="{y+r*1.5+18*makaet:.0f}" rx="{5*s_:.0f}"'
              f' ry="{9*s_:.0f}" fill="#8a4a1c" opacity="{makaet*.8:.2f}"/>')
    s += (f'<path d="M{x-r*.5:.0f},{y-r*.8:.0f} q{r*.4:.0f},{-r*.2:.0f}'
          f' {r*.9:.0f},{r*.1:.0f}" fill="none" stroke="#f0d8a0"'
          f' stroke-width="{max(2,5*s_):.0f}" opacity=".6"/></g>')
    return s


def _nogi_v_noskah(x, y, s_=1.0, t=0.0):
    """ДВЕ НОГИ В ПОЛОСАТЫХ НОСКАХ из-под одеяла — главный предмет: у каждой
    видно пятку, подъём, бугорок пальцев и рубчик резинки, носки в полоску
    двух цветов. Шевелятся во сне по очереди, а не вместе (иначе читаются
    цветными колбасками — R-0047)."""
    s = ""
    for i, (dx, ph) in enumerate(((-96 * s_, .0), (96 * s_, .5))):
        kol = 5.0 * A.w(t, 2.2, ph)
        nx = x + dx
        s += (f'<g transform="rotate({kol:.1f} {nx:.0f} {y-150*s_:.0f})">'
              f'{ten(nx + 20 * s_, y + 10 * s_, 86 * s_, 14 * s_, .45)}'
              f'<path d="M{nx-56*s_:.0f},{y-168*s_:.0f}'
              f' L{nx+56*s_:.0f},{y-168*s_:.0f} L{nx+60*s_:.0f},{y-40*s_:.0f}'
              f' Q{nx+66*s_:.0f},{y:.0f} {nx+116*s_:.0f},{y-6*s_:.0f}'
              f' Q{nx+140*s_:.0f},{y-14*s_:.0f} {nx+134*s_:.0f},{y-44*s_:.0f}'
              f' Q{nx+120*s_:.0f},{y-78*s_:.0f} {nx+60*s_:.0f},{y-86*s_:.0f}'
              f' L{nx-56*s_:.0f},{y-86*s_:.0f} Z" fill="#8fa3c2" {o(6)}/>')
        for j in range(7):
            yy = y - 160 * s_ + j * 22 * s_
            if yy > y - 86 * s_:
                break
            s += (f'<rect x="{nx-56*s_:.0f}" y="{yy:.0f}" width="{116*s_:.0f}"'
                  f' height="{11*s_:.0f}" fill="{"#b8323a" if j % 2 else "#efe3c8"}"'
                  f' opacity=".9"/>')
        s += (f'<path d="M{nx+58*s_:.0f},{y-76*s_:.0f} q{40*s_:.0f},{10*s_:.0f}'
              f' {72*s_:.0f},{34*s_:.0f}" fill="none" stroke="#efe3c8"'
              f' stroke-width="{12*s_:.0f}" opacity=".9"/>'
              f'<rect x="{nx-60*s_:.0f}" y="{y-176*s_:.0f}" width="{124*s_:.0f}"'
              f' height="{26*s_:.0f}" rx="{10*s_:.0f}" fill="#7288a8" {o(4)}/>')
        for j in range(5):
            s += (f'<line x1="{nx-52*s_+j*26*s_:.0f}" y1="{y-174*s_:.0f}"'
                  f' x2="{nx-52*s_+j*26*s_:.0f}" y2="{y-154*s_:.0f}"'
                  f' stroke="#5e7294" stroke-width="{max(2,4*s_):.0f}"/>')
        for j in range(3):
            s += (f'<ellipse cx="{nx+(100+j*14)*s_:.0f}" cy="{y-(26-j*6)*s_:.0f}"'
                  f' rx="{13*s_:.0f}" ry="{10*s_:.0f}" fill="#a4b8d2"'
                  f' opacity=".9"/>')
        s += "</g>"
    return s


def _oblachko_sna(x, y, s_=1.0, t=0.0, seed=3):
    """Облачко сна с банным паром: пухлая гряда пузырей, три пузырька-хвоста
    к спящему и внутри — веник с паром. Плывёт по кругу, не стоит."""
    rnd = random.Random(seed)
    hod = 26 * s_ * math.sin(t * .6)
    s = f'<g transform="translate({hod:.0f},{-8 * s_ * math.sin(t * .9):.0f})">'
    for i, (dx, dy, rr) in enumerate(((-150, 10, 74), (-60, -24, 96),
                                      (52, -14, 86), (140, 16, 66))):
        s += (f'<circle cx="{x+dx*s_:.0f}" cy="{y+dy*s_:.0f}" r="{rr*s_:.0f}"'
              f' fill="#e8f1f6" {o(5)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y+30*s_:.0f}" rx="{190*s_:.0f}"'
          f' ry="{54*s_:.0f}" fill="#e8f1f6" {o(5)}/>')
    s += _venik(x + 10 * s_, y + 54 * s_, 150 * s_, t, "#b8a86a", "#5a4a2e",
                False, .16, .2, s_ * .5, 117)
    s += par(x - 50 * s_, y + 10 * s_, t, 3, .5, 110 * s_, .6)
    s += "</g>"
    for i in range(3):
        s += (f'<circle cx="{x-200*s_-i*44*s_:.0f}" cy="{y+96*s_+i*40*s_:.0f}"'
              f' r="{(22-i*6)*s_:.0f}" fill="#e8f1f6" {o(3)}/>')
    return s


def _budilnik(x, y, s_=1.0, t=0.0):
    """Будильник: круглый корпус на ножках, две чашки-звонка, молоточек,
    циферблат БЕЗ цифр (своих букв не рисуем) со стрелками и секундной,
    которая идёт."""
    r = 62 * s_
    sek = (t * 60.0) % 60.0
    a_s = math.radians(sek * 6 - 90)
    s = (f'{ten(x, y + 8 * s_, r * .9, 11 * s_, .45)}'
         f'<circle cx="{x:.0f}" cy="{y-r*.9:.0f}" r="{r:.0f}" fill="#9c3a2a" {o(6)}/>'
         f'<circle cx="{x:.0f}" cy="{y-r*.9:.0f}" r="{r*.80:.0f}"'
         f' fill="#efe8d8" {o(4)}/>')
    for i in range(12):
        a = math.radians(i * 30)
        s += (f'<line x1="{x+math.cos(a)*r*.66:.0f}" y1="{y-r*.9+math.sin(a)*r*.66:.0f}"'
              f' x2="{x+math.cos(a)*r*.74:.0f}" y2="{y-r*.9+math.sin(a)*r*.74:.0f}"'
              f' stroke="{K}" stroke-width="{max(2,4*s_):.0f}"/>')
    s += (f'<line x1="{x:.0f}" y1="{y-r*.9:.0f}" x2="{x+r*.40:.0f}"'
          f' y2="{y-r*1.22:.0f}" stroke="{K}" stroke-width="{max(3,7*s_):.0f}"/>'
          f'<line x1="{x:.0f}" y1="{y-r*.9:.0f}" x2="{x-r*.16:.0f}"'
          f' y2="{y-r*1.50:.0f}" stroke="{K}" stroke-width="{max(3,6*s_):.0f}"/>'
          f'<line x1="{x:.0f}" y1="{y-r*.9:.0f}"'
          f' x2="{x+math.cos(a_s)*r*.64:.0f}"'
          f' y2="{y-r*.9+math.sin(a_s)*r*.64:.0f}" stroke="{KRAS}"'
          f' stroke-width="{max(2,4*s_):.0f}"/>'
          f'<circle cx="{x:.0f}" cy="{y-r*.9:.0f}" r="{6*s_:.0f}" fill="{K}"/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*r*.72:.0f},{y-r*1.52:.0f} q{i*r*.34:.0f},'
              f'{-r*.30:.0f} {i*r*.10:.0f},{-r*.44:.0f}" fill="none"'
              f' stroke="#8f979d" stroke-width="{max(3,7*s_):.0f}"/>'
              f'<ellipse cx="{x+i*r*.76:.0f}" cy="{y-r*1.92:.0f}" rx="{r*.34:.0f}"'
              f' ry="{r*.22:.0f}" fill="#b9c6cc" {o(4)}/>')
    s += (f'<rect x="{x-r*.10:.0f}" y="{y-r*2.02:.0f}" width="{r*.20:.0f}"'
          f' height="{r*.30:.0f}" rx="{r*.08:.0f}" fill="#8f979d" {o(3)}/>')
    for i in (-1, 1):
        s += (f'<path d="M{x+i*r*.52:.0f},{y-r*.18:.0f} q{i*r*.14:.0f},'
              f'{r*.22:.0f} {i*r*.04:.0f},{r*.26:.0f}" fill="none"'
              f' stroke="#8f979d" stroke-width="{max(3,8*s_):.0f}"/>')
    return s


def _staya_vetra(t, n=22, seed=5, y0=120, y1=520):
    """ВЕТЕР НАРИСОВАН СТАЕЙ ВОРОБЬЁВ ИЗ ЗАВИТКОВ: у каждого тельце-запятая,
    крыло росчерком и хвост вилкой; стая несётся слева направо рваным
    строем, часть птиц мелкая, часть крупная (через одного)."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        ph = rnd.uniform(0, 1)
        p = ((t * .42 + ph) % 1.0)
        px = -220 + p * (W + 440)
        py = y0 + (y1 - y0) * rnd.random() + 22 * math.sin(t * 3 + i)
        sc = (1.5 if i % 2 == 0 else .62) * rnd.uniform(.8, 1.15)
        kr = 16 * sc * A.w(t, .36, ph)
        s += (f'<path d="M{px:.0f},{py:.0f} q{22*sc:.0f},{-12*sc:.0f}'
              f' {40*sc:.0f},{2*sc:.0f} q{-14*sc:.0f},{12*sc:.0f}'
              f' {-40*sc:.0f},{-2*sc:.0f} Z" fill="#8e9ab0" {o(3)}/>'
              f'<path d="M{px+14*sc:.0f},{py-2*sc:.0f} q{14*sc:.0f},'
              f'{-20*sc-kr:.0f} {34*sc:.0f},{-6*sc:.0f}" fill="none"'
              f' stroke="#a8b4c6" stroke-width="{max(2,4*sc):.0f}"/>'
              f'<path d="M{px:.0f},{py:.0f} l{-18*sc:.0f},{-7*sc:.0f}'
              f' l{4*sc:.0f},{7*sc:.0f} l{-16*sc:.0f},{6*sc:.0f}" fill="none"'
              f' stroke="#8e9ab0" stroke-width="{max(2,3.4*sc):.0f}"/>')
    return s


def _bereza_sognuta(x, base, h_, t, seed=3, storona=1, vetok=7):
    """Берёза, согнутая ветром в одну сторону: белый ствол с чёрными
    чечевичками, ветки свисают по ходу ветра и хлещут все вместе."""
    rnd = random.Random(seed)
    gib = (.26 + .10 * abs(A.w(t, 1.3, .2))) * storona
    vx = x + h_ * gib
    s = (f'<path d="M{x-h_*.030:.0f},{base:.0f} Q{x+h_*gib*.4:.0f},'
         f'{base-h_*.55:.0f} {vx:.0f},{base-h_:.0f}'
         f' L{vx+h_*.026:.0f},{base-h_:.0f} Q{x+h_*gib*.4+h_*.034:.0f},'
         f'{base-h_*.55:.0f} {x+h_*.030:.0f},{base:.0f} Z"'
         f' fill="#e6e2d8" {o(5)}/>')
    for i in range(9):
        yy = base - h_ * (.08 + i * .10)
        xx = x + h_ * gib * ((i + 1) / 10.0) ** 1.4
        s += (f'<path d="M{xx-h_*.022:.0f},{yy:.0f} q{h_*.014:.0f},{4:.0f}'
              f' {h_*.030:.0f},{-2:.0f}" fill="none" stroke="#2f2b26"'
              f' stroke-width="{max(2, h_*.011):.0f}" opacity=".85"/>')
    for i in range(vetok):
        p = .40 + i * (.56 / max(1, vetok - 1.0))
        bx = x + h_ * gib * p ** 1.4
        by = base - h_ * p
        dl = h_ * (.30 - .02 * i)
        hl = 14 * storona * A.w(t, .9, i * .2)
        s += (f'<path d="M{bx:.0f},{by:.0f} Q{bx+storona*dl*.6:.0f},'
              f'{by+dl*.12:.0f} {bx+storona*dl+hl:.0f},{by+dl*.52:.0f}"'
              f' fill="none" stroke="#5a564e"'
              f' stroke-width="{max(2, h_*.010):.0f}"/>')
        for j in range(4):
            s += (f'<path d="M{bx+storona*dl*(.3+j*.18):.0f},'
                  f'{by+dl*(.16+j*.10):.0f} q{storona*dl*.14:.0f},{dl*.14:.0f}'
                  f' {storona*dl*.10:.0f},{dl*.28:.0f}" fill="none"'
                  f' stroke="#4e4a44" stroke-width="{max(2, h_*.006):.0f}"/>')
    return s


def _kalitka_hlopaet(x, y, w_, h_, t, stolby=True):
    """Калитка, которая хлопает на ветру: дощатое полотнище на двух петлях,
    косина-подкос, кольцо-ручка, два столба с набалдашниками."""
    hlop = abs(math.sin(t * 2.2)) ** 2
    ug = -58.0 * hlop
    s = ""
    if stolby:
        for sx in (x - 26, x + w_ + 26):
            s += (f'<rect x="{sx-20:.0f}" y="{y-h_-30:.0f}" width="40"'
                  f' height="{h_+40:.0f}" rx="9" fill="#5a4530" {o(5)}/>'
                  f'<path d="M{sx-26:.0f},{y-h_-30:.0f} q{26:.0f},{-26:.0f}'
                  f' {52:.0f},0 Z" fill="#6b5340" {o(4)}/>')
    s += f'<g transform="rotate({ug:.1f} {x:.0f} {y-h_*.5:.0f})">'
    for i in range(5):
        s += (f'<rect x="{x+6+i*(w_-12)/5.0:.0f}" y="{y-h_:.0f}"'
              f' width="{(w_-12)/5.0-7:.0f}" height="{h_:.0f}" rx="6"'
              f' fill="url(#derev)" {o(4)}/>')
    for p in (.22, .78):
        s += (f'<rect x="{x:.0f}" y="{y-h_+h_*p:.0f}" width="{w_:.0f}"'
              f' height="16" rx="6" fill="#7d5636" {o(4)}/>')
    s += (f'<line x1="{x+4:.0f}" y1="{y-10:.0f}" x2="{x+w_-4:.0f}"'
          f' y2="{y-h_+20:.0f}" stroke="#7d5636" stroke-width="16"/>'
          f'<circle cx="{x+w_-24:.0f}" cy="{y-h_*.52:.0f}" r="14" fill="none"'
          f' stroke="{ZHELEZ}" stroke-width="7"/>'
          f'<rect x="{x-10:.0f}" y="{y-h_*.80:.0f}" width="34" height="16"'
          f' rx="6" fill="{ZHELEZ}" {o(3)}/>'
          f'<rect x="{x-10:.0f}" y="{y-h_*.24:.0f}" width="34" height="16"'
          f' rx="6" fill="{ZHELEZ}" {o(3)}/></g>')
    return s


def _gorshok_letit(x, y, t, s_=1.0, k=.0, seed=5):
    """Глиняный горшок, слетающий с забора: тулово с венчиком и поливой,
    летит по дуге и кувыркается; за ним пыль с кола."""
    px = x + k * 420
    py = y - math.sin(k * 3.14) * 170 + k * 60
    ug = k * 420
    r = 44 * s_
    s = (f'<g transform="rotate({ug:.0f} {px:.0f} {py:.0f})">'
         f'<path d="M{px-r:.0f},{py-r*.30:.0f} q{r*.10:.0f},{r*1.00:.0f}'
         f' {r*1.0:.0f},{r*1.00:.0f} q{r*.90:.0f},0 {r*1.0:.0f},{-r*1.00:.0f} Z"'
         f' fill="url(#glina)" {o(6)}/>'
         f'<ellipse cx="{px:.0f}" cy="{py-r*.30:.0f}" rx="{r:.0f}"'
         f' ry="{r*.28:.0f}" fill="#b08050" {o(5)}/>'
         f'<ellipse cx="{px:.0f}" cy="{py-r*.26:.0f}" rx="{r*.78:.0f}"'
         f' ry="{r*.20:.0f}" fill="#4a3a2a" opacity=".9"/>'
         f'<path d="M{px-r*.92:.0f},{py+r*.14:.0f} q{r*.92:.0f},{r*.26:.0f}'
         f' {r*1.84:.0f},0" fill="none" stroke="{KREM}"'
         f' stroke-width="{8*s_:.0f}" opacity=".7"/></g>')
    if k < .3:
        for i in range(5):
            s += (f'<circle cx="{x+i*12:.0f}" cy="{y+16+i*6:.0f}"'
                  f' r="{7-i:.0f}" fill="#cfd6de" opacity="{(.3-k)*2:.2f}"/>')
    return s


def _tulup_na_gvozde(x, y, h_, t, ph=.0, shapka=True):
    """Тулуп и шапка на гвозде: овчинная опушка по вороту, запах полой,
    рукава висят, подол вздрагивает от сквозняка."""
    drog = 2.6 * A.w(t, 2.2, ph) + 1.4 * A.w(t, 7.0, ph)
    s = (f'<g transform="rotate({drog:.1f} {x:.0f} {y:.0f})">'
         f'<rect x="{x-20:.0f}" y="{y-22:.0f}" width="40" height="14" rx="6"'
         f' fill="{ZHELEZ}" {o(3)}/>'
         f'<path d="M{x:.0f},{y:.0f} q{-96:.0f},{26:.0f} {-110:.0f},{110:.0f}'
         f' L{x-96:.0f},{y+h_:.0f} L{x+96:.0f},{y+h_:.0f} L{x+110:.0f},{y+110:.0f}'
         f' q{-14:.0f},{-84:.0f} {-110:.0f},{-110:.0f} Z" fill="#6b5340" {o(7)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y+8:.0f}" rx="64" ry="24" fill="#cfc1a4"'
         f' {o(5)}/>'
         f'<path d="M{x:.0f},{y+22:.0f} L{x+22:.0f},{y+h_:.0f}" fill="none"'
         f' stroke="#4e3c2c" stroke-width="12"/>'
         f'<path d="M{x-104:.0f},{y+96:.0f} q{-26:.0f},{86:.0f} {-6:.0f},{140:.0f}'
         f' q{30:.0f},{16:.0f} {46:.0f},{-14:.0f}" fill="#5e4a38" {o(5)}/>'
         f'<path d="M{x+104:.0f},{y+96:.0f} q{26:.0f},{86:.0f} {6:.0f},{140:.0f}'
         f' q{-30:.0f},{16:.0f} {-46:.0f},{-14:.0f}" fill="#5e4a38" {o(5)}/>'
         f'<rect x="{x-96:.0f}" y="{y+h_-30:.0f}" width="192" height="26"'
         f' rx="9" fill="#cfc1a4" opacity=".85"/></g>')
    if shapka:
        s += (f'<g transform="rotate({-drog:.1f} {x+170:.0f} {y-10:.0f})">'
              f'<rect x="{x+150:.0f}" y="{y-28:.0f}" width="40" height="14"'
              f' rx="6" fill="{ZHELEZ}" {o(3)}/>'
              f'<path d="M{x+118:.0f},{y+48:.0f} q{52:.0f},{-72:.0f}'
              f' {104:.0f},0 q{-20:.0f},{26:.0f} {-104:.0f},0 Z" fill="#4a3f36"'
              f' {o(5)}/>'
              f'<ellipse cx="{x+170:.0f}" cy="{y+50:.0f}" rx="56" ry="20"'
              f' fill="#cfc1a4" {o(4)}/></g>')
    return s


def _volny_zvuka(x, y, t, n=4, ug=0.0, dl=260, col="#cfe4f5"):
    """Волны звука от стены к уху: три-четыре дуги разного радиуса бегут
    одна за другой и гаснут на подходе."""
    s = ""
    for i in range(n):
        p = ((t * 1.3 + i / float(n)) % 1.0)
        r = dl * (.22 + .78 * p)
        s += (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
              f'<path d="M{x:.0f},{y-r*.62:.0f} A{r:.0f},{r*.62:.0f} 0 0 1'
              f' {x:.0f},{y+r*.62:.0f}" fill="none" stroke="{col}"'
              f' stroke-width="{11-6*p:.0f}" opacity="{(1-p)*.8:.2f}"/></g>')
    return s


def _pryalka(x, y, t, s_=1.0, kruzh=True):
    """Прялка с колесом: станина на трёх ножках, большое колесо со спицами,
    стойка с куделью и шнур привода. Колесо медленно крутится."""
    r = 110 * s_
    ug = (t * 40.0) % 360.0
    s = (f'{ten(x, y + 8 * s_, 110 * s_, 14 * s_, .45)}'
         f'<rect x="{x-110*s_:.0f}" y="{y-40*s_:.0f}" width="{230*s_:.0f}"'
         f' height="{26*s_:.0f}" rx="{10*s_:.0f}" fill="url(#dosk)" {o(6)}/>')
    for i in (-1, 0, 1):
        s += (f'<rect x="{x+i*92*s_-9*s_:.0f}" y="{y-16*s_:.0f}"'
              f' width="{18*s_:.0f}" height="{22*s_:.0f}" rx="{7*s_:.0f}"'
              f' fill="#5b4428" {o(4)}/>')
    if kruzh:
        s += f'<g transform="rotate({ug:.1f} {x-40*s_:.0f} {y-r-24*s_:.0f})">'
        s += (f'<circle cx="{x-40*s_:.0f}" cy="{y-r-24*s_:.0f}" r="{r:.0f}"'
              f' fill="none" stroke="#8a6038" stroke-width="{14*s_:.0f}"/>'
              f'<circle cx="{x-40*s_:.0f}" cy="{y-r-24*s_:.0f}" r="{r*.14:.0f}"'
              f' fill="#7d5636" {o(4)}/>')
        for i in range(8):
            a = math.radians(i * 45)
            s += (f'<line x1="{x-40*s_:.0f}" y1="{y-r-24*s_:.0f}"'
                  f' x2="{x-40*s_+math.cos(a)*r*.92:.0f}"'
                  f' y2="{y-r-24*s_+math.sin(a)*r*.92:.0f}" stroke="#9c7049"'
                  f' stroke-width="{max(3,7*s_):.0f}"/>')
        s += "</g>"
    s += (f'<rect x="{x+76*s_:.0f}" y="{y-240*s_:.0f}" width="{18*s_:.0f}"'
          f' height="{212*s_:.0f}" rx="{8*s_:.0f}" fill="#8a6038" {o(5)}/>'
          f'<path d="M{x+86*s_:.0f},{y-240*s_:.0f} q{-46*s_:.0f},{-50*s_:.0f}'
          f' {-10*s_:.0f},{-96*s_:.0f} q{46*s_:.0f},{34*s_:.0f} {10*s_:.0f},{96*s_:.0f} Z"'
          f' fill="#e2d6c2" {o(4)}/>')
    for i in range(5):
        s += (f'<path d="M{x+72*s_+i*6*s_:.0f},{y-290*s_:.0f} q{-14*s_:.0f},'
              f'{-30*s_:.0f} {-4*s_:.0f},{-56*s_:.0f}" fill="none"'
              f' stroke="#cfc7ad" stroke-width="{max(2,4*s_):.0f}"/>')
    s += (f'<line x1="{x-40*s_:.0f}" y1="{y-r-24*s_:.0f}" x2="{x+84*s_:.0f}"'
          f' y2="{y-200*s_:.0f}" stroke="#4e4a44" stroke-width="{max(2,4*s_):.0f}"/>')
    return s


def _lar_kovanyy(x, y, w_, h_, t, seed=3):
    """Кованый ларь: толстые доски, железные полосы с заклёпками, накладной
    замок с пробоем и кольцо-ручка по боку."""
    s = (f'{ten(x + w_ * .5, y + 10, w_ * .52, 18, .5)}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="10" fill="url(#dosk)" {o(8)}/>'
         f'<path d="M{x-10:.0f},{y-h_:.0f} q{w_*.5:.0f},{-54:.0f} {w_+20:.0f},0 Z"'
         f' fill="#8a6038" {o(6)}/>')
    for i in range(4):
        s += (f'<line x1="{x+10:.0f}" y1="{y-h_+28+i*(h_-34)/4.0:.0f}"'
              f' x2="{x+w_-10:.0f}" y2="{y-h_+28+i*(h_-34)/4.0:.0f}"'
              f' stroke="#5b4428" stroke-width="6" opacity=".8"/>')
    for i in range(3):
        bx = x + 30 + i * (w_ - 90) / 2.0
        s += (f'<rect x="{bx:.0f}" y="{y-h_-18:.0f}" width="34"'
              f' height="{h_+22:.0f}" rx="7" fill="#4e4a47" {o(4)}/>')
        for j in range(4):
            s += (f'<circle cx="{bx+17:.0f}" cy="{y-h_+16+j*(h_-26)/3.0:.0f}"'
                  f' r="6" fill="#8f979d"/>')
    s += (f'<rect x="{x+w_*.46:.0f}" y="{y-h_*.56:.0f}" width="{w_*.14:.0f}"'
          f' height="{h_*.26:.0f}" rx="8" fill="#5f5a56" {o(5)}/>'
          f'<path d="M{x+w_*.50:.0f},{y-h_*.56:.0f} q{w_*.03:.0f},{-28:.0f}'
          f' {w_*.06:.0f},0" fill="none" stroke="#8f979d" stroke-width="11"/>'
          f'<circle cx="{x+w_*.53:.0f}" cy="{y-h_*.44:.0f}" r="7" fill="#2a2726"/>'
          f'<circle cx="{x+w_-26:.0f}" cy="{y-h_*.52:.0f}" r="16" fill="none"'
          f' stroke="{ZHELEZ}" stroke-width="8"/>')
    return s


def _kadka_kvashni(x, y, s_=1.0, t=0.0):
    """Кадка с квашнёй: клёпки с обручами, тесто подошло горбом и дышит,
    поверх марля и деревянный гнёт-кружок рядом."""
    w2, h2 = 170 * s_, 150 * s_
    dysh = 10 * s_ * abs(A.w(t, 1.5, .2))
    s = (f'{ten(x, y + 10 * s_, w2 * .56, 15 * s_, .5)}'
         f'<path d="M{x-w2/2:.0f},{y-h2:.0f} q{-10*s_:.0f},{h2*.5:.0f}'
         f' {4*s_:.0f},{h2:.0f} L{x+w2/2-4*s_:.0f},{y:.0f}'
         f' q{14*s_:.0f},{-h2*.5:.0f} {4*s_:.0f},{-h2:.0f} Z"'
         f' fill="url(#derev)" {o(7)}/>')
    for i in range(6):
        s += (f'<line x1="{x-w2*.44+i*w2*.18:.0f}" y1="{y-h2+6*s_:.0f}"'
              f' x2="{x-w2*.46+i*w2*.19:.0f}" y2="{y-6*s_:.0f}"'
              f' stroke="#5b4428" stroke-width="{max(3,5*s_):.0f}" opacity=".8"/>')
    for p in (.26, .78):
        s += (f'<rect x="{x-w2*.54:.0f}" y="{y-h2+h2*p:.0f}" width="{w2*1.08:.0f}"'
              f' height="{15*s_:.0f}" rx="6" fill="{ZHELEZ}" {o(4)}/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h2:.0f}" rx="{w2*.5:.0f}"'
          f' ry="{w2*.16:.0f}" fill="#8a6038" {o(5)}/>'
          f'<path d="M{x-w2*.46:.0f},{y-h2:.0f} q{w2*.24:.0f},{-56*s_-dysh:.0f}'
          f' {w2*.92:.0f},0 Z" fill="#efe3c8" {o(5)}/>'
          f'<path d="M{x-w2*.30:.0f},{y-h2-28*s_-dysh*.6:.0f} q{w2*.14:.0f},'
          f'{-14*s_:.0f} {w2*.30:.0f},{-2*s_:.0f}" fill="none" stroke="#fffaf0"'
          f' stroke-width="{8*s_:.0f}" opacity=".6"/>'
          f'<path d="M{x-w2*.52:.0f},{y-h2+6*s_:.0f} q{w2*.26:.0f},{-34*s_:.0f}'
          f' {w2*1.04:.0f},{2*s_:.0f}" fill="none" stroke="#e8f1f6"'
          f' stroke-width="{7*s_:.0f}" opacity=".5"/>'
          f'<ellipse cx="{x+w2*.72:.0f}" cy="{y-18*s_:.0f}" rx="{w2*.22:.0f}"'
          f' ry="{w2*.07:.0f}" fill="url(#dosk)" {o(4)}/>')
    return s


def _puchki_trav(x, y, n=4, t=0.0, seed=5, step=108):
    """Пучки сушёных трав на стене: перевязь, стебли вниз, сухие соцветия,
    пара листьев отпала. Шевелятся от сквозняка."""
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        px = x + i * step
        kach = 2.4 * A.w(t, 2.6, i * .4)
        s += (f'<g transform="rotate({kach:.1f} {px:.0f} {y:.0f})">'
              f'<rect x="{px-6:.0f}" y="{y-16:.0f}" width="12" height="14"'
              f' rx="4" fill="{ZHELEZ}"/>'
              f'<rect x="{px-22:.0f}" y="{y-6:.0f}" width="44" height="22"'
              f' rx="8" fill="#b8a86a" {o(3)}/>')
        for j in range(7):
            a = math.radians(66 + (j - 3) * 11)
            dl = rnd.uniform(96, 150)
            s += (f'<path d="M{px:.0f},{y+14:.0f} Q{px+dl*.5*math.cos(a)+8:.0f},'
                  f'{y+14+dl*.5*math.sin(a):.0f} {px+dl*math.cos(a):.0f},'
                  f'{y+14+dl*math.sin(a):.0f}" fill="none" stroke="#7b8450"'
                  f' stroke-width="{rnd.uniform(4,7):.0f}"/>'
                  f'<ellipse cx="{px+dl*math.cos(a):.0f}"'
                  f' cy="{y+14+dl*math.sin(a):.0f}" rx="9" ry="13"'
                  f' fill="#9ca86a" opacity=".9"/>')
        s += "</g>"
    return s


def _kontur_televizora(x, y, w_, h_, t, prost=.0, diktor=True):
    """Прозрачный КОНТУР телевизора, который проступает на миг и тает: сам
    ящик нарисован ЛИНИЯМИ (не мутным пятном), внутри — контур диктора в
    галстуке, рот открывается. Плотность кадра держат настоящие вещи, этот
    контур только проступает."""
    op = prost
    if op <= .01:
        return ""
    s = (f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="16" fill="none" stroke="#9fd8f0" stroke-width="9"'
         f' opacity="{op*.9:.2f}"/>'
         f'<rect x="{x+22:.0f}" y="{y-h_+22:.0f}" width="{w_-100:.0f}"'
         f' height="{h_-44:.0f}" rx="22" fill="none" stroke="#9fd8f0"'
         f' stroke-width="7" opacity="{op*.8:.2f}"/>')
    for i in range(2):
        s += (f'<circle cx="{x+w_-40:.0f}" cy="{y-h_+60+i*54:.0f}" r="15"'
              f' fill="none" stroke="#9fd8f0" stroke-width="6"'
              f' opacity="{op*.8:.2f}"/>')
    for i in (0, 1):
        s += (f'<line x1="{x+w_*(.26+i*.4):.0f}" y1="{y:.0f}"'
              f' x2="{x+w_*(.22+i*.44):.0f}" y2="{y+44:.0f}" stroke="#9fd8f0"'
              f' stroke-width="7" opacity="{op*.8:.2f}"/>')
    s += (f'<line x1="{x+w_*.78:.0f}" y1="{y-h_:.0f}" x2="{x+w_*.92:.0f}"'
          f' y2="{y-h_-120:.0f}" stroke="#9fd8f0" stroke-width="6"'
          f' opacity="{op*.7:.2f}"/>'
          f'<line x1="{x+w_*.78:.0f}" y1="{y-h_:.0f}" x2="{x+w_*.62:.0f}"'
          f' y2="{y-h_-108:.0f}" stroke="#9fd8f0" stroke-width="6"'
          f' opacity="{op*.7:.2f}"/>')
    if diktor:
        cx, cy = x + w_ * .38, y - h_ * .52
        rot = 6 + 12 * abs(A.w(t, 1.1, .2))
        s += (f'<circle cx="{cx:.0f}" cy="{cy-56:.0f}" r="40" fill="none"'
              f' stroke="#9fd8f0" stroke-width="7" opacity="{op*.9:.2f}"/>'
              f'<path d="M{cx-66:.0f},{y-h_*.12:.0f} q{10:.0f},{-86:.0f}'
              f' {66:.0f},{-92:.0f} q{56:.0f},{6:.0f} {66:.0f},{92:.0f}"'
              f' fill="none" stroke="#9fd8f0" stroke-width="7"'
              f' opacity="{op*.9:.2f}"/>'
              f'<path d="M{cx-16:.0f},{cy-20:.0f} L{cx:.0f},{cy+6:.0f}'
              f' L{cx+16:.0f},{cy-20:.0f}" fill="none" stroke="#9fd8f0"'
              f' stroke-width="6" opacity="{op*.9:.2f}"/>'
              f'<path d="M{cx:.0f},{cy+6:.0f} l{-11:.0f},{44:.0f} l{11:.0f},{18:.0f}'
              f' l{11:.0f},{-18:.0f} Z" fill="none" stroke="#9fd8f0"'
              f' stroke-width="6" opacity="{op*.9:.2f}"/>'
              f'<ellipse cx="{cx:.0f}" cy="{cy-42:.0f}" rx="13" ry="{rot:.0f}"'
              f' fill="none" stroke="#9fd8f0" stroke-width="5"'
              f' opacity="{op*.9:.2f}"/>'
              f'<circle cx="{cx-16:.0f}" cy="{cy-68:.0f}" r="5" fill="#9fd8f0"'
              f' opacity="{op*.9:.2f}"/>'
              f'<circle cx="{cx+16:.0f}" cy="{cy-68:.0f}" r="5" fill="#9fd8f0"'
              f' opacity="{op*.9:.2f}"/>')
    return s


# ── ДЕКОРАЦИИ, ВТОРАЯ ПАРТИЯ ──────────────────────────────────────────────

def drova_v_bannoy_pechi(t):
    """Предбанник: чугунная дверца банной печи крупно, рядом поленница,
    кочерга, ведро, лавка с вениками. Хозяин в вязаной шапке присел у печи:
    левой рукой в рукавице придерживает открытую створку, правой закладывает
    в топку берёзовое полено, отблеск огня ложится на лицо и бороду."""
    rnd = random.Random(503)
    pol = 1010
    s = f'<rect width="{W}" height="{H}" fill="#1e1510"/>'
    s += SL(Z_DAL, brevna(0, 40, 980, pol - 40, 92)
            + brevna(980, 40, 940, pol - 40, 92))
    s += SL(Z_DAL, _stennoe_hozyaystvo(1600, 240, t, 505))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-20:.0f}" width="{W}" height="{H-pol+20:.0f}"'
                   f' fill="#4a3a2a"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1074, 507, 6, "#3a2c1e"))
    # ГЛАВНЫЙ ПРЕДМЕТ: чугунная дверца с топкой, створка открыта и закрывается
    otkr = 1.0 - A.ease(A.seg(t, 1.5, .9))
    s += SL(Z_SRED, _dverca_pechi(360, 790, 440, 420, t, otkr, 509))
    s += SL(Z_SRED, dym(520, 330, t, 4, .24, 230, .26, "#cfd6de", 1.2))
    s += SL(Z_SRED, iskra_let(t, 560, 650, 8, 511, 240, .6))
    # обстановка предбанника
    s += SL(Z_SRED, _polenica(880, pol - 8, 420, 300, 513, 27))
    s += SL(Z_SRED, _ugol_pechnoy_utvari(1340, pol, t, 515))
    s += SL(Z_SRED, _lavka_krupno(1620, pol, 400, t, 160, True))
    for i in range(3):
        s += SL(Z_SRED, _venik(1520 + i * 92, pol - 162, 210, t, "#cdbf9c",
                               "#b8352c", False, .12, i * .3, .7, 517 + i))
    s += SL(Z_SRED, _dvorovaya_utvar(1180, pol + 46, 240, t, 519, ["vedro"]))
    # ОДНА ФИГУРА: присел у печи, обе руки наружу влево
    gx, gy, gh = 980, pol, 660
    zak = A.ease(A.seg(t, .3, 1.1))
    hoz = figura(gx, gy, gh, t, col="#4e4036", kant="#ffd98a", ph=.3,
                 shapka=True, boroda=True, naklon=8.0)
    r1, (a1x, a1y), _ = _ruka_so_sgibom(gx, gy, gh, -1, gh * .24, 10,
                                        gh * .26, 28, t, "#4e4036",
                                        "#ffd98a", .2, 4.0)
    r2, (a2x, a2y), _ = _ruka_so_sgibom(gx, gy, gh, -1, gh * .24, 34,
                                        gh * .26, 52 - 16 * zak, t,
                                        "#4e4036", "#ffd98a", .7, 5.0)
    hoz += r1 + r2
    s += SL(Z_SRED, hoz)
    # РУКАВИЦА на левой кисти придерживает створку: перекрытие по кромке
    s += SL(Z_SRED, _varezhka(a1x, a1y + 2, gh, t, .2, "#c9ad74", "#8a7a46"))
    # ПОЛЕНО уходит в топку из правой кисти
    plx = a2x - 60 - 180 * zak
    s += SL(Z_SRED, _poleno(plx, a2y + 26, 1.0, -8 + 14 * zak, True))
    s += SL(Z_SRED, _varezhka(a2x, a2y + 4, gh, t, .7, "#c9ad74", "#8a7a46"))
    # ОТБЛЕСК ОГНЯ на лице и бороде — тёплое пятно одно, от печи
    s += SL(Z_SRED, teplo(gx - gh * .22, gy - gh * .82, 180, 150,
                          .32 + .22 * abs(A.w(t, 1.1, .2))))
    s += SL(Z_SRED, teplo(580, 700, 560, 440, .44))
    # нижняя треть
    s += SL(Z_SRED, _polovik(1060, pol + 40, 480, 110, "#cdbf9c", "#b8352c")
            + _sledy(1880, 1066, 1240, pol + 30, 7, 521, "#3a2c1e", 1.1)
            + _kot_zhivoy(1480, pol + 54, t, 1.0, "#3b3430", .4)
            + _valenki_u_dveri(240, pol + 40, 1.1, t))
    s += SL(Z_PERED, _stolb_pered(1892, 118, "#150f0a", 0, H))
    s += vinetka(.44)
    return s


def vanna_s_parom(t):
    """Городская ванная: белая ванна крупно, над ней густой пар, на бортике
    мочалка, мыло в мыльнице, резиновая уточка, на двери махровый халат.
    Видна одна рука до локтя: пробует ладонью пар над ванной и вешает на
    крючок полотенце. Зеркало над раковиной запотевает."""
    rnd = random.Random(523)
    pol = 1012
    zapot = A.ease(A.seg(t, .5, 2.4))
    s = f'<rect width="{W}" height="{H}" fill="#39434a"/>'
    s += SL(Z_DAL, _kafel(0, 40, 1920, 720, t, 525, "#cfdcdc", "#a0b0b0"))
    s += SL(Z_DAL, tusklaya_lampochka(640, 20, t, 1.0, True))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#8f9c9c"/>' + _kafel(0, pol - 10, 1920, 110, t, 527,
                                                 "#b8c4c4", "#8f9c9c"))
    # дверь с махровым халатом и раковина с зеркалом
    s += SL(Z_DAL, dver(1540, 180, 360, 790, .0, "#cfd8dc", True, False))
    s += SL(Z_SRED, _halat_na_dveri(1700, 300, 420, t, .2, "#e3ddc6"))
    s += SL(Z_SRED, f'<rect x="100" y="640" width="330" height="48" rx="14"'
                    f' fill="#eef2f4" {o(6)}/>'
            + f'<ellipse cx="265" cy="664" rx="120" ry="32" fill="#dde6ea" {o(4)}/>'
            + f'<ellipse cx="265" cy="668" rx="96" ry="22" fill="#b9c6cc"'
              f' opacity=".9"/>'
            + f'<rect x="240" y="688" width="50" height="{pol-688:.0f}" rx="12"'
              f' fill="#cfd5da" {o(4)}/>'
            + f'<rect x="248" y="560" width="22" height="86" rx="10"'
              f' fill="#9aa3aa" {o(4)}/>'
            + f'<path d="M258,560 q0,-40 56,-36" fill="none" stroke="#9aa3aa"'
              f' stroke-width="20"/>')
    s += SL(Z_SRED, _zerkalo_zapot(110, 180, 330, 360, t, zapot))
    # ГЛАВНЫЙ ПРЕДМЕТ: ванна с водой и паром
    s += SL(Z_SRED, _vanna(520, pol - 6, 900, t, 260))
    # на бортике: мочалка, мыло, уточка
    s += SL(Z_SRED, _mochalka(640, pol - 272, 1.0, t, .2))
    s += SL(Z_SRED, _mylo_v_mylnice(870, pol - 262, 1.05, t))
    s += SL(Z_SRED, _utochka(1120, pol - 250, 1.15, t, .4))
    s += SL(Z_SRED, _polotence(1430, 420, 300, t, .4, "#e3ddc6", True))
    # РУКА ДО ЛОКТЯ над бортиком, без человека (nichya=True)
    ves = A.ease(A.seg(t, 1.6, 1.3))
    rk, (ex, ey) = rukav(1400, 1074, 330, -104 + 16 * ves, t, "#c2a07a",
                         "#e8d8c0", .3, 5.0, True)
    s += SL(Z_SRED, rk)
    # ладонь пробует пар: варежка перекрывает полотенце, когда вешает
    s += SL(Z_SRED, _polotence(ex - 28, ey - 10, 210 + 60 * ves, t, .2,
                               "#efe3c8", False))
    s += SL(Z_SRED, _varezhka(ex, ey, 760, t, .3, "#e8d8c0", "#b89a74"))
    s += SL(Z_SRED, par(ex - 20, ey - 40, t, 4, .52, 170, .6, 1.3))
    # нижняя треть
    s += SL(Z_SRED, _polovik(760, pol + 44, 520, 110, "#6a9cc2", "#3f5c7a")
            + _dvorovaya_utvar(1300, pol + 50, 230, t, 529, ["vedro"])
            + _gorodskoy_hlam(170, pol + 42, 260, t, 531, ["yaschik"])
            + _utochka(980, pol + 34, .9, t, .7))
    s += SL(Z_SRED, teplo(900, pol - 280, 520, 300, .28))
    s += SL(Z_LETIT, par(760, 560, t, 5, .40, 320, .35, 2.1))
    s += SL(Z_PERED, _stolb_pered(-8, 100, "#20262a", 0, H))
    s += vinetka(.40)
    return s


def chistoe_bele_i_pervyy_sneg(t):
    """Спальня: на кровати стопка чистого белья крупно — сорочка, носки,
    полотенце, от стопки поднимаются завитки свежести. Женщина в халате с
    полотенцем-тюрбаном левой рукой придерживает тюрбан, правой открывает
    створку окна, за которым падает первый снег. Рядом трюмо, гребень,
    флакон."""
    rnd = random.Random(533)
    pol = 1014
    s = f'<rect width="{W}" height="{H}" fill="#2d3238"/>'
    s += SL(Z_DAL, _stena_gornicy(t, 535, True, 740, True))
    s += SL(Z_DAL, _ramki_na_stene(700, 130, 420, t, 537, 3))
    s += SL(Z_DAL, _polka_s_utvaryu(150, 170, 500, t, 551, 5)
            + _knizhnaya_polka(700, 400, 480, t, 553, 2, 150))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#5e4a34"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1074, 539, 6, "#4a3824"))
    # ОКНО со створкой, которая открывается, и первым снегом за ним
    stv = A.ease(A.seg(t, 1.4, 1.6))
    s += SL(Z_DAL, okno_izby(1260, 160, 560, 470, t,
                             f'<rect x="1260" y="160" width="560" height="470"'
                             f' fill="{SUMER}"/>'
                             + "".join(f'<rect x="{1300+i*104:.0f}" y="440"'
                                       f' width="60" height="48" rx="5"'
                                       f' fill="{SVET}"'
                                       f' opacity="{.4+.25*abs(A.w(t,2.2,i*.4)):.2f}"/>'
                                       for i in range(5))
                             + f'<rect x="1260" y="500" width="560" height="130"'
                               f' fill="{SNEG}" opacity=".72"/>',
                             .12, False, True))
    s += SL(Z_SRED, f'<g transform="rotate({-36 * stv:.1f} 1540 400)">'
                    f'<rect x="1540" y="180" width="270" height="430" rx="8"'
                    f' fill="none" stroke="#6a5030" stroke-width="26"/>'
                    f'<rect x="1548" y="188" width="254" height="414" rx="6"'
                    f' fill="{STEKLO}" opacity="{.30-.18*stv:.2f}"/>'
                    f'<line x1="1675" y1="188" x2="1675" y2="602"'
                    f' stroke="#6a5030" stroke-width="16"/></g>')
    s += SL(Z_LETIT, mokryy_sneg(t, 30, 541, .62, .9))
    # КРОВАТЬ и ГЛАВНЫЙ ПРЕДМЕТ: стопка чистого белья
    s += SL(Z_SRED, _krovat(90, pol, 1010, t, 543, True, 320))
    s += SL(Z_SRED, _podushka(300, 710, 320, 190, t, .3, .2, .0))
    s += SL(Z_SRED, _stopka_belya(440, 700, 460, t, True, 545))
    # трюмо с гребнем и флаконом
    s += SL(Z_SRED, _tryumo(990, pol, 420, 560, t, 547))
    s += SL(Z_SRED, f'<path d="M1046,{pol-566:.0f} l96,0 l0,24 l-96,0 Z"'
                    f' fill="#c9ad74" {o(4)}/>'
            + "".join(f'<line x1="{1052+i*11:.0f}" y1="{pol-542:.0f}"'
                      f' x2="{1052+i*11:.0f}" y2="{pol-520:.0f}"'
                      f' stroke="#c9ad74" stroke-width="5"/>' for i in range(9))
            + f'<rect x="1180" y="{pol-592:.0f}" width="52" height="66" rx="10"'
              f' fill="#b8323a" opacity=".9" {o(4)}/>'
            + f'<rect x="1196" y="{pol-606:.0f}" width="20" height="18" rx="6"'
              f' fill="{ZOL}" {o(3)}/>')
    s += SL(Z_SRED, svecha(900, pol - 580, t, .2, 1.2, 108)
            + teplo(900, pol - 640, 230, 200, .36))
    # ОДНА ФИГУРА: левая держит тюрбан, правая открывает створку
    zx, zy, zh = 1430, pol, 760
    plech_r = A.ease(A.seg(t, 2.6, 1.0))
    zhen = figura(zx, zy, zh, t, col="#b8323a", kant="#cfe4f5", ph=.4,
                  naklon=3.0 - 2.0 * plech_r)
    r1, (b1x, b1y), _ = _ruka_so_sgibom(zx, zy, zh, -1, zh * .20, -28,
                                        zh * .20, -52, t, "#b8323a",
                                        "#cfe4f5", .2, 4.0)
    r2, (b2x, b2y), _ = _ruka_mimo(zx, zy, zh, 1, zh * .42, -14 - 20 * stv, t,
                                   "#b8323a", "#cfe4f5", .7, 5.0)
    zhen += r1 + r2
    s += SL(Z_SRED, zhen)
    # ТЮРБАН из полотенца на голове — отдельный виток поверх убора
    gy_ = zy - zh * .845
    s += SL(Z_SRED, f'<path d="M{zx-zh*.105:.0f},{gy_-zh*.095:.0f}'
                    f' q{zh*.105:.0f},{-zh*.105:.0f} {zh*.21:.0f},0'
                    f' q{-zh*.02:.0f},{zh*.042:.0f} {-zh*.21:.0f},{zh*.008:.0f} Z"'
                    f' fill="{RUSH}" {o(5)}/>'
            + f'<path d="M{zx-zh*.10:.0f},{gy_-zh*.12:.0f} q{zh*.10:.0f},'
              f'{-zh*.06:.0f} {zh*.20:.0f},{-zh*.01:.0f}" fill="none"'
              f' stroke="{TKAN}" stroke-width="{zh*.013:.0f}"/>'
            + f'<path d="M{zx+zh*.10:.0f},{gy_-zh*.105:.0f} q{zh*.07:.0f},'
              f'{zh*.03:.0f} {zh*.04:.0f},{zh*.09:.0f}" fill="none"'
              f' stroke="{RUSH}" stroke-width="{zh*.026:.0f}"/>')
    s += SL(Z_SRED, _varezhka(b1x, b1y, zh, t, .2))
    s += SL(Z_SRED, para_izo_rta(zx + 30, gy_ + 10, t, .5, .9, .4))
    # нижняя треть
    s += SL(Z_SRED, _polovik(820, pol + 42, 540, 118, "#6a7a8c", "#3f5c7a")
            + _valenki_u_dveri(1760, pol + 36, 1.05, t)
            + _dvorovaya_utvar(140, pol + 52, 230, t, 549, ["korzina"])
            + _kot_zhivoy(700, pol + 52, t, 1.05, "#3b3430", .3))
    s += SL(Z_PERED, _stolb_pered(-8, 110, "#1a120c", 0, H))
    s += vinetka(.42)
    return s


def bannyy_den_taz_i_mochalka(t):
    """Раздевалка городской бани: деревянные шкафчики с номерками, длинная
    лавка, на ней оцинкованный таз крупно — в тазу лыковая мочалка, кусок
    мыла, берёзовый веник. Отец в простыне сидит на лавке и обеими руками
    держит гранёный стакан чая в подстаканнике. Сын рядом болтает ногами,
    левой держит свой стакан, правой макает в него сушку."""
    rnd = random.Random(557)
    pol = 1016
    lav = 806
    s = f'<rect width="{W}" height="{H}" fill="#2f2a24"/>'
    s += SL(Z_DAL, _kafel(0, 40, 1920, 230, t, 559, "#c4ccc8", "#98a49e"))
    s += SL(Z_SRED, _shkafchiki_bani(0, 250, 1340, 540, t, 6, 561))
    s += SL(Z_DAL, _shkafchiki_bani(1340, 250, 580, 540, t, 3, 563))
    s += SL(Z_DAL, tusklaya_lampochka(1700, 40, t, 1.0, True))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-20:.0f}" width="{W}" height="{H-pol+20:.0f}"'
                   f' fill="#7a6a58"/>' + _kafel(0, pol - 12, 1920, 110, t, 565,
                                                 "#a89c8c", "#80745f"))
    # ЛАВКА во всю ширину — опора обеих фигур
    s += SL(Z_SRED, f'{ten(960, pol + 12, 720, 22, .5)}'
                    f'<rect x="60" y="{lav:.0f}" width="1800" height="54" rx="12"'
                    f' fill="url(#dosk)" {o(8)}/>'
            + f'<rect x="90" y="{lav+54:.0f}" width="1740" height="26" rx="9"'
              f' fill="#5b4428" {o(5)}/>')
    for px in (180, 900, 1700):
        s += SL(Z_SRED, f'<rect x="{px:.0f}" y="{lav+80:.0f}" width="68"'
                        f' height="{pol-lav-80+12:.0f}" rx="12" fill="#5b4428"'
                        f' {o(6)}/>')
    # ГЛАВНЫЙ ПРЕДМЕТ: оцинкованный таз с мочалкой, мылом и веником
    s += SL(Z_SRED, _taz_bannyy(420, lav - 4, 1.0, t, True))
    # ДВЕ ФИГУРЫ сидят на лавке: уровень пола у них — сама лавка
    ox, oy, oh = 1080, lav + 6, 560
    sx_, sy_, sh = 1480, lav + 6, 420
    _figury_kadra((ox, oy, oh), (sx_, sy_, sh))
    mak = A.ease(A.seg(t, .6, 1.2)) * (1 - A.ease(A.seg(t, 2.6, 1.0)))
    otec = figura(ox, oy, oh, t, col="#efe8d8", kant="#ffd98a", ph=.3,
                  naklon=3.0)
    o1, (c1x, c1y), _ = _ruka_mimo(ox, oy, oh, -1, oh * .32, 52, t,
                                   "#efe8d8", "#ffd98a", .2, 4.0)
    o2, (c2x, c2y), _ = _ruka_mimo(ox, oy, oh, 1, oh * .30, 54, t,
                                   "#efe8d8", "#ffd98a", .6, 4.0)
    otec += o1 + o2
    syn = figura(sx_, sy_, sh, t, col="#efe8d8", kant="#ffd98a", ph=.7,
                 naklon=4.0)
    p1, (d1x, d1y), _ = _ruka_mimo(sx_, sy_, sh, 1, sh * .34, 50, t,
                                   "#efe8d8", "#ffd98a", .1, 4.0)
    p2, (d2x, d2y), _ = _ruka_sgib_mimo(sx_, sy_, sh, 1, sh * .22, 24,
                                        sh * .22, 44 + 14 * mak, t,
                                        "#efe8d8", "#ffd98a", .5, 5.0)
    syn += p1 + p2
    s += SL(Z_SRED, otec)
    # ПРОСТЫНЯ, в которую завёрнут отец: распаренное лицо и пар от плеч
    s += SL(Z_SRED, f'<path d="M{ox-oh*.22:.0f},{oy-oh*.60:.0f}'
                    f' q{oh*.22:.0f},{-oh*.06:.0f} {oh*.44:.0f},0'
                    f' L{ox+oh*.26:.0f},{oy-oh*.08:.0f}'
                    f' L{ox-oh*.26:.0f},{oy-oh*.08:.0f} Z" fill="#f4eedc"'
                    f' {o(5)}/>'
            + f'<path d="M{ox-oh*.24:.0f},{oy-oh*.34:.0f} q{oh*.24:.0f},'
              f'{oh*.04:.0f} {oh*.48:.0f},0" fill="none" stroke="#d9d0b8"'
              f' stroke-width="9"/>'
            + "".join(f'<ellipse cx="{ox+i*oh*.085:.0f}"'
                      f' cy="{oy-oh*.825:.0f}" rx="{oh*.038:.0f}"'
                      f' ry="{oh*.026:.0f}" fill="#d9705a" opacity=".45"/>'
                      for i in (-1, 1)))
    s += SL(Z_SRED, par(ox - oh * .22, oy - oh * .66, t, 4, .50, 170, .5)
            + par(ox + oh * .22, oy - oh * .62, t, 3, .44, 150, .6))
    s += SL(Z_SRED, syn)
    s += SL(Z_SRED, f'<path d="M{sx_-sh*.22:.0f},{sy_-oh*.44:.0f}'
                    f' q{sh*.22:.0f},{-sh*.08:.0f} {sh*.44:.0f},0'
                    f' L{sx_+sh*.26:.0f},{sy_-sh*.10:.0f}'
                    f' L{sx_-sh*.26:.0f},{sy_-sh*.10:.0f} Z" fill="#f4eedc"'
                    f' {o(5)}/>')
    # БОЛТАЮЩИЕСЯ НОГИ сына: ступни над полом, качаются в противофазе
    for i, ph in ((-1, .0), (1, .5)):
        kol = 16 * A.w(t, 1.3, ph)
        nx = sx_ + i * sh * .14
        s += SL(Z_SRED, f'<g transform="rotate({kol:.1f} {nx:.0f} {sy_-sh*.08:.0f})">'
                        f'<rect x="{nx-18:.0f}" y="{sy_-sh*.08:.0f}" width="36"'
                        f' height="130" rx="15" fill="#e2d6c2" {o(5)}/>'
                        f'<path d="M{nx-20:.0f},{sy_-sh*.08+130:.0f}'
                        f' q{20:.0f},{26:.0f} {58:.0f},{14:.0f}'
                        f' q{8:.0f},{-20:.0f} {-18:.0f},{-28:.0f} Z"'
                        f' fill="#8fa3c2" {o(4)}/></g>')
    # СТАКАНЫ В ПОДСТАКАННИКАХ: ровно в кистях, варежки перекрывают их
    sta_x = (c1x + c2x) * .5
    s += SL(Z_SRED, _stakan_podstakannik(sta_x, c1y + 56, 1.0, t, .78, True))
    s += SL(Z_SRED, _varezhka(c1x, c1y + 4, oh, t, .2)
            + _varezhka(c2x, c2y + 4, oh, t, .6))
    s += SL(Z_SRED, _stakan_podstakannik(d1x + 30, d1y + 48, .84, t, .72, False))
    s += SL(Z_SRED, _varezhka(d1x, d1y + 4, sh, t, .1))
    s += SL(Z_SRED, _sushka_odna(d2x + 20, d2y + 36 + 26 * mak, .92, t, mak, 10))
    s += SL(Z_SRED, _varezhka(d2x, d2y + 4, sh, t, .5))
    # нижняя треть
    s += SL(Z_SRED, _taz_bannyy(1760, pol + 8, .62, t, False)
            + _valenki_u_dveri(300, pol + 36, 1.15, t)
            + _polovik(960, pol + 40, 560, 110, "#cdbf9c", "#b8352c")
            + _dvorovaya_utvar(680, pol + 46, 230, t, 567, ["vedro"]))
    s += SL(Z_SRED, teplo(1700, 180, 420, 300, .26))
    s += SL(Z_PERED, _stolb_pered(1894, 104, "#1c1710", 0, H))
    s += vinetka(.42)
    return s


def suhie_noski_i_krepkiy_son(t):
    """Кровать с железными шишечками, толстое ватное одеяло, из-под одеяла
    торчат две ноги в полосатых шерстяных носках. Мальчик спит на правом
    боку, правая ладонь под щекой, левая рука поверх одеяла. На стуле
    простыня и веник, на стене коврик, на тумбочке будильник, над мальчиком
    плывёт облачко сна с банным паром."""
    rnd = random.Random(571)
    pol = 1020
    s = f'<rect width="{W}" height="{H}" fill="#241c16"/>'
    s += SL(Z_DAL, _stena_gornicy(t, 573, True, 760, True))
    s += SL(Z_DAL, _kovrik_s_olenyami(900, 120, 700, 400, t))
    s += SL(Z_DAL, _polka_s_utvaryu(120, 150, 480, t, 575, 4))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#5e4a34"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1078, 577, 6, "#4a3824"))
    # КРОВАТЬ с железными шишечками на спинках
    s += SL(Z_SRED, _krovat(300, pol, 1180, t, 579, True, 330))
    for i, (bx, n) in enumerate(((330, 3), (1430, 3))):
        s += SL(Z_SRED, f'<rect x="{bx-16:.0f}" y="{pol-430:.0f}" width="32"'
                        f' height="430" rx="14" fill="#8f979d" {o(5)}/>')
        for j in range(n):
            s += SL(Z_SRED, f'<circle cx="{bx:.0f}" cy="{pol-446-j*4:.0f}"'
                            f' r="{26-j*6:.0f}" fill="#b9c6cc" {o(4)}/>')
        s += SL(Z_SRED, f'<rect x="{bx-10:.0f}" y="{pol-300:.0f}" width="{(1430-330) if i == 0 else 10:.0f}"'
                        f' height="22" rx="9" fill="#9aa3aa" {o(4)}/>')
    s += SL(Z_SRED, _podushka(560, 716, 360, 200, t, .3, .5, .0))
    # ВАТНОЕ ОДЕЯЛО дышит
    s += SL(Z_SRED, _odeyalo_kray(360, 780, 1060, 240, t,
                                  .2 + .3 * abs(A.w(t, 1.7, .1)), "#8a4a5c"))
    # ГЛАВНЫЙ ПРЕДМЕТ: две ноги в полосатых носках из-под одеяла
    s += SL(Z_SRED, _nogi_v_noskah(1300, 1010, 1.15, t))
    # МАЛЬЧИК спит на правом боку: рост мал, голова на подушке
    bx_, by_, bh = 700, 806, 420
    _figury_kadra((bx_, by_, bh))
    mal = figura(bx_, by_, bh, t, col="#e2d6c2", kant="#ffd98a", ph=.3,
                 naklon=10.0)
    m1, (h1x, h1y), _ = _ruka_mimo(bx_, by_, bh, -1, bh * .28, -34, t,
                                   "#e2d6c2", "#ffd98a", .2, 3.0)
    m2, (h2x, h2y), _ = _ruka_mimo(bx_, by_, bh, 1, bh * .40, 58, t,
                                   "#e2d6c2", "#ffd98a", .6, 3.0)
    mal += m1 + m2
    s += SL(Z_SRED, mal)
    # ладонь под щекой: варежка перекрывает край подушки (хват читается)
    s += SL(Z_SRED, _varezhka(h1x, h1y + 4, bh, t, .2))
    # ОБЛАЧКО СНА с банным паром над мальчиком
    s += SL(Z_SRED, _oblachko_sna(900, 330, 1.0, t, 581))
    # стул с простынёй и веником, тумбочка с будильником
    s += SL(Z_SRED, _venskiy_stul(1640, pol, 420, t, -6, False))
    s += SL(Z_SRED, f'<path d="M1540,{pol-390:.0f} q110,-46 220,0'
                    f' q{-20:.0f},{70:.0f} {-110:.0f},{96:.0f}'
                    f' q{-90:.0f},{-26:.0f} {-110:.0f},{-96:.0f} Z"'
                    f' fill="#f4eedc" {o(5)}/>')
    s += SL(Z_SRED, _venik(1700, pol - 300, 260, t, "#cdbf9c", "#b8352c",
                           False, .12, .3, .8, 583))
    s += SL(Z_SRED, _tumbochka_veschi(130, pol, 250, t, 210))
    s += SL(Z_SRED, _budilnik(255, pol - 224, 1.0, t))
    s += SL(Z_SRED, svecha(190, pol - 226, t, .4, 1.0, 96)
            + teplo(200, pol - 280, 230, 200, .34))
    # нижняя треть
    s += SL(Z_SRED, _polovik(900, pol + 42, 540, 118, "#cdbf9c", "#b8352c")
            + _valenki_u_dveri(1860, pol + 38, 1.0, t)
            + _kot_zhivoy(640, pol + 52, t, 1.1, "#3b3430", .3, True, True)
            + _dvorovaya_utvar(420, pol + 48, 220, t, 585, ["korzina"]))
    s += SL(Z_PERED, _stolb_pered(-8, 110, "#1a120c", 0, H))
    s += vinetka(.44)
    return s


def vorobinaya_noch_nad_derevney(t):
    """Тёмно-синяя ночь под луной: деревня пригнулась под ветром — дым из
    труб лежит вбок, берёзы согнуты в одну сторону, калитка хлопает, с
    забора летит горшок. Ветер нарисован огромной стаей воробьёв из
    завитков, она несётся над крышами слева направо. Людей нет, во всех
    избах темно, в одном окне горит огонёк."""
    rnd = random.Random(587)
    gor = 720
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 83)
    s += oblaka(t, 140, 6, 85, .36, "#8e9ab0", 5.0)
    s += SL(Z_NEBO, f'<circle cx="1560" cy="190" r="104" fill="#e8eef6"'
                    f' opacity=".92"/>'
            + f'<circle cx="1560" cy="190" r="150" fill="#cfe4f5" opacity=".16"/>'
            + f'<circle cx="1596" cy="162" r="22" fill="#cfd6de" opacity=".5"/>'
            + f'<circle cx="1528" cy="216" r="15" fill="#cfd6de" opacity=".45"/>')
    # ДЕРЕВНЯ: избы в три плана, свет только в одном окне
    s += SL(Z_DAL, _derevnya_ryad(gor - 170, t, 87,
                                  ((120, 300), (520, 260), (1120, 280),
                                   (1700, 240))))
    for i, (bx, bw, sv_) in enumerate(((200, 470, False), (660, 790, True),
                                       (1400, 450, False))):
        s += SL(Z_SRED, izba_snaruzhi(bx, gor + 40 + i * 12, bw, t, sv_, True,
                                      89 + i * 4))
    # дым из труб ЛЕЖИТ ВБОК: сдвиг по ходу ветра
    for i, (dx_, dy_) in enumerate(((330, gor - 330), (860, gor - 366),
                                    (1440, gor - 342))):
        s += SL(Z_SRED, f'<g transform="translate({120 + 40 * i:.0f},0)'
                        f' rotate(62 {dx_:.0f} {dy_:.0f})">'
                        + dym(dx_, dy_, t, 6, .40, 420, .40, "#8e9ab0", 2.2)
                        + "</g>")
    # БЕРЁЗЫ согнуты в одну сторону
    for i, (bx, bh) in enumerate(((120, 560), (640, 480), (1180, 520),
                                  (1820, 440))):
        s += SL(Z_DAL, _bereza_sognuta(bx, gor + 60, bh, t, 93 + i, 1, 7))
    # ЗАБОР, КАЛИТКА и летящий горшок
    s += SL(Z_SRED, _zabor_dosok(1480, gor - 100, 440, 170, 97, 54))
    s += SL(Z_SRED, _kalitka_hlopaet(1060, gor + 110, 210, 280, t, True))
    for i, (gx_, gy_, gs) in enumerate(((1560, gor - 118, 1.0),
                                        (1700, gor - 110, .74))):
        k = A.ease(A.seg(t, .4 + i * .34, 2.2))
        s += SL(Z_SRED, _gorshok_letit(gx_, gy_, t, gs, k, 99 + i))
    # ЗЕМЛЯ и нижняя треть — настоящие вещи, а не пустое поле
    s += SL(Z_SRED, f'<rect x="0" y="{gor+60:.0f}" width="{W}"'
                    f' height="{H-gor-60:.0f}" fill="#2b3038"/>'
            + sneg_lezhit(gor + 90, 30)
            + _zemlya_faktura(gor + 130, 1072, 101, 16, "#232830"))
    s += SL(Z_SRED, _polenica(80, 1040, 380, 210, 103, 26)
            + _sani(560, 1040, .86, t, True)
            + _kucha_listev(1360, 1052, 320, 105, 76)
            + _dvorovaya_utvar(1660, 1046, 240, t, 107, ["kadka", "vedro"])
            + _sledy(300, 1070, 1020, gor + 150, 8, 109, "#1d2128", 1.1))
    s += SL(Z_SRED, _stog(1860, 1010, .76, t, True))
    s += SL(Z_SRED, _vorona(420, gor - 420, t, 1.0, .2, .6)
            + _vorona(1240, gor - 470, t, .74, .6, .4))
    # ВЕТЕР СТАЕЙ: два яруса, над крышами и чуть выше
    s += SL(Z_LETIT, _staya_vetra(t, 20, 111, 180, 420))
    s += SL(Z_LETIT, _staya_vetra(t, 14, 113, 440, 640))
    s += SL(Z_LETIT, mokryy_sneg(t, 34, 115, .46, 2.1))
    s += SL(Z_SRED, teplo(900, gor - 180, 420, 300, .30))
    s += SL(Z_PERED, _vetka_pered(1960, 170, 640, 154, t, 117, "#141017", 7))
    s += vinetka(.48)
    return s


def uho_u_steny(t):
    """Бревенчатая стена избы изнутри, пакля между брёвнами, на гвозде тулуп
    и шапка. Дед в исподнем стоит босиком на половике боком к стене: ухо
    прижал к бревну, ладонь приложил к уху раковиной, второй рукой держит
    кальсоны. От стены к уху бегут рисованные волны звука, в плошке мечется
    огонёк."""
    rnd = random.Random(601)
    pol = 1012
    s = f'<rect width="{W}" height="{H}" fill="#241a12"/>'
    # СТЕНА КРУПНО: брёвна в полкадра и пакля между венцами
    s += SL(Z_DAL, brevna(0, 0, 1100, pol, 118))
    s += SL(Z_DAL, brevna(1100, 0, 820, pol, 118, 40))
    for i in range(9):
        yy = 116 + i * 118
        s += SL(Z_DAL, "".join(
            f'<path d="M{20+j*96:.0f},{yy:.0f} q{22:.0f},{-11:.0f} {46:.0f},{2:.0f}"'
            f' fill="none" stroke="#c9b48a" stroke-width="{rnd.uniform(7,13):.0f}"'
            f' opacity=".8"/>' for j in range(19)))
    s += SL(Z_DAL, _polka_s_utvaryu(1420, 170, 440, t, 603, 4)
            + _polka_s_utvaryu(60, 200, 460, t, 611, 5))
    # стенное хозяйство и подкова-оберег: без них стена читается обоями
    s += SL(Z_DAL, _stennoe_hozyaystvo(230, 520, t, 613))
    s += SL(Z_DAL, podkova(1020, 150, 1.5, t))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#5e4a34"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1074, 605, 6, "#4a3824"))
    # ТУЛУП И ШАПКА НА ГВОЗДЕ — вздрагивают от сквозняка
    s += SL(Z_SRED, _tulup_na_gvozde(1180, 210, 480, t, .3, True))
    # плошка с лучиной: огонёк мечется
    s += SL(Z_SRED, f'<rect x="1560" y="{pol-330:.0f}" width="300" height="26"'
                    f' rx="9" fill="url(#dosk)" {o(5)}/>'
            + f'<path d="M1660,{pol-330:.0f} q50,-34 100,0 Z" fill="#b08050"'
              f' {o(4)}/>')
    s += SL(Z_SRED, luchina(1710, pol - 338, t, 1.25, .2)
            + teplo(1710, pol - 380, 300, 250, .40))
    # ОДНА ФИГУРА: дед в исподнем, босиком, в профиль к стене
    dx_, dy_, dh = 700, pol, 780
    _figury_kadra((dx_, dy_, dh))
    brov = A.w(t, 1.6, .2)
    ded = figura(dx_, dy_, dh, t, col="#efe8d8", kant="#ffd98a", ph=.3,
                 profil=True, boroda=True, naklon=4.0)
    # ПРАВАЯ рука идёт ВВЕРХ и НАРУЖУ к уху: `_ruka` не пускает кисть в свою
    # же голову, поэтому ладонь встаёт РЯДОМ с ухом, у самого его края —
    # это и есть «ладонь раковиной», коридор угла держит код
    r1, (u1x, u1y), _ = _ruka_so_sgibom(dx_, dy_, dh, 1, dh * .18, -38,
                                        dh * .14, -56, t, "#efe8d8",
                                        "#ffd98a", .2, 3.0)
    r2, (u2x, u2y), _ = _ruka_mimo(dx_, dy_, dh, -1, dh * .26, 62, t,
                                   "#efe8d8", "#ffd98a", .7, 4.0)
    ded += r1 + r2
    s += SL(Z_SRED, ded)
    # ЛАДОНЬ РАКОВИНОЙ у уха: полукольцо от кисти к голове, пальцев нет
    s += SL(Z_SRED, f'<path d="M{u1x-10:.0f},{u1y-40:.0f}'
                    f' q{44:.0f},{-14:.0f} {52:.0f},{40:.0f}'
                    f' q{6:.0f},{44:.0f} {-40:.0f},{54:.0f}"'
                    f' fill="none" stroke="#e8d8c0" stroke-width="30"'
                    f' stroke-linecap="round"/>')
    # ВОЛНЫ ЗВУКА от стены к уху
    s += SL(Z_SRED, _volny_zvuka(u1x - 180, u1y + 10, t, 4, 0.0, 240))
    s += SL(Z_SRED, _volny_zvuka(u1x - 130, u1y - 90, t, 3, -14.0, 190))
    # БРОВИ ходят вверх-вниз: короткий штрих над глазом, поверх лица
    gy_ = dy_ - dh * .845
    for i in (-1, 1):
        s += SL(Z_SRED, f'<path d="M{dx_+i*dh*.045-dh*.022:.0f},'
                        f'{gy_-dh*.052+brov*dh*.008:.0f}'
                        f' q{dh*.022:.0f},{-dh*.014:.0f} {dh*.044:.0f},0"'
                        f' fill="none" stroke="{K}"'
                        f' stroke-width="{dh*.009:.0f}" stroke-linecap="round"/>')
    # КАЛЬСОНЫ, которые он придерживает второй рукой
    s += SL(Z_SRED, f'<path d="M{dx_-dh*.15:.0f},{dy_-dh*.40:.0f}'
                    f' q{dh*.15:.0f},{dh*.03:.0f} {dh*.30:.0f},0'
                    f' L{dh*.015+dx_+dh*.14:.0f},{dy_-dh*.08:.0f}'
                    f' L{dx_-dh*.16:.0f},{dy_-dh*.08:.0f} Z" fill="#e2dccc"'
                    f' {o(5)}/>'
            + f'<path d="M{dx_-dh*.16:.0f},{dy_-dh*.36:.0f} q{dh*.16:.0f},'
              f'{dh*.03:.0f} {dh*.32:.0f},0" fill="none" stroke="#c4bba6"'
              f' stroke-width="{dh*.016:.0f}"/>')
    s += SL(Z_SRED, _varezhka(u2x, u2y + 2, dh, t, .7))
    # БОСЫЕ НОГИ НА ПОЛОВИКЕ — опора названа
    s += SL(Z_SRED, _polovik(dx_ - 250, pol + 16, 520, 120, "#cdbf9c", "#b8352c"))
    # нижняя треть
    s += SL(Z_SRED, _valenki_u_dveri(1860, pol + 36, 1.05, t)
            + _dvorovaya_utvar(120, pol + 52, 240, t, 607, ["korzina", "vedro"])
            + _kot_zhivoy(1240, pol + 54, t, 1.1, "#3b3430", .4)
            + _yaschiki(1500, pol + 16, t, 609, 2, .9)
            + _polenica(300, pol + 60, 300, 170, 615, 25)
            + kartoshka(1020, pol + 58, t, 8, 617, 1.05))
    s += SL(Z_SRED, _kadushki_i_grabli(1680, pol + 44, t, 619))
    s += SL(Z_PERED, _stolb_pered(-8, 124, "#140e09", 0, H))
    s += vinetka(.44)
    return s


def pustoy_ugol_bez_televizora(t):
    """Красный угол старой избы, где сегодня стоял бы телевизор: вместо него
    прялка, кованый ларь, кадка с квашнёй, на стене ходики и пучки трав. На
    ларе на миг проступает прозрачный контур телевизора с диктором в
    галстуке, диктор открывает рот — и контур тает. Дед сидит на лавке
    рядом: правой рукой машет на контур, левая лежит на колене."""
    rnd = random.Random(623)
    pol = 1014
    s = f'<rect width="{W}" height="{H}" fill="#26190f"/>'
    s += SL(Z_DAL, brevna(0, 0, 1180, pol, 104)
            + brevna(1180, 0, 740, pol, 104, 52))
    s += SL(Z_DAL, _polka_s_utvaryu(100, 150, 500, t, 625, 5))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#5e4a34"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1074, 627, 6, "#4a3824"))
    # ХОДИКИ и пучки трав на стене
    s += SL(Z_SRED, hodiki(1000, 190, t, 1.5))
    s += SL(Z_SRED, _puchki_trav(620, 200, 4, t, 629, 108))
    # ПРЯЛКА, КОВАНЫЙ ЛАРЬ, КАДКА С КВАШНЁЙ — то, что стоит вместо экрана
    s += SL(Z_SRED, _pryalka(300, pol, t, 1.0, True))
    s += SL(Z_SRED, _lar_kovanyy(760, pol, 560, 300, t, 631))
    s += SL(Z_SRED, _kadka_kvashni(1480, pol, 1.15, t))
    s += SL(Z_SRED, svecha(1320, pol - 8, t, .3, 1.35, 120)
            + teplo(1320, pol - 70, 300, 260, .40))
    # КОНТУР ТЕЛЕВИЗОРА проступает на ларе и тает
    prost = A.ease(A.seg(t, .6, .9)) * (1 - A.ease(A.seg(t, 2.0, 1.2)))
    s += SL(Z_SRED, _kontur_televizora(840, pol - 310, 420, 320, t, prost, True))
    # ОДНА ФИГУРА: дед на лавке, правая машет, левая на колене
    s += SL(Z_SRED, _lavka_krupno(1640, pol, 470, t, 170, True))
    dx_, dy_, dh = 1660, pol - 160, 560
    _figury_kadra((dx_, dy_, dh))
    mash = A.w(t, 1.1, .2)
    ded = figura(dx_, dy_, dh, t, col="#54505e", kant="#ffd98a", ph=.4,
                 boroda=True, naklon=5.0)
    r1, (m1x, m1y), _ = _ruka_mimo(dx_, dy_, dh, -1, dh * .46,
                                   -4 + 22 * mash, t, "#54505e", "#ffd98a",
                                   .2, 9.0)
    r2, (m2x, m2y), _ = _ruka_so_sgibom(dx_, dy_, dh, 1, dh * .22, 30,
                                        dh * .22, 62, t, "#54505e",
                                        "#ffd98a", .7, 3.0)
    ded += r1 + r2
    s += SL(Z_SRED, ded)
    # машущая кисть: предмета в ней нет, значит варежки НЕТ — рукав без кисти
    s += SL(Z_SRED, f'<path d="M{m1x-26:.0f},{m1y-20:.0f} q{30:.0f},{-16:.0f}'
                    f' {52:.0f},{10:.0f}" fill="none" stroke="#ffd98a"'
                    f' stroke-width="7" opacity="{.25+.3*abs(mash):.2f}"/>')
    # нижняя треть
    s += SL(Z_SRED, _polovik(900, pol + 40, 560, 118, "#cdbf9c", "#b8352c")
            + _dvorovaya_utvar(120, pol + 52, 240, t, 633, ["kadka", "vedro"])
            + _kot_zhivoy(1180, pol + 54, t, 1.1, "#3b3430", .3)
            + kartoshka(640, pol + 60, t, 8, 635, 1.0)
            + _valenki_u_dveri(1870, pol + 36, 1.0, t))
    s += SL(Z_SRED, _yaschiki(420, pol + 14, t, 637, 2, .86))
    s += SL(Z_PERED, _stolb_pered(-8, 118, "#150e08", 0, H))
    s += vinetka(.44)
    return s


def stariki_slushayut_noch(t):
    """Деревянная кровать с горой подушек под окном, окно на пол-кадра — в
    нём настоящая луна в бегущих облаках. Дед лежит на спине, обе руки
    поверх одеяла, смотрит в потолок и слушает. Бабка на правом боку лицом
    к нему, левую руку высунула из-под одеяла и подняла: тише. На второй
    половине фразы в окне утро, и дед сидит на кровати, уверенно показывая
    рукой на небо."""
    rnd = random.Random(641)
    pol = 1016
    utro = A.ease(A.seg(t, 2.0, 1.1))
    sel = A.ease(A.seg(t, 2.2, 1.0))
    s = f'<rect width="{W}" height="{H}" fill="#1e2430"/>'
    s += SL(Z_DAL, _stena_gornicy(t, 643, True, 700, True))
    s += SL(Z_DAL, _polka_s_utvaryu(80, 150, 420, t, 645, 4)
            + _ramki_na_stene(1560, 170, 320, t, 647, 3))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#5e4a34"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1074, 649, 6, "#4a3824"))
    # НАСТОЯЩИЙ КАДР в окне над кроватью: вид, метка, переплёт поверх
    px, py, pw, ph_ = 540, 110, 860, 420
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<path d="{put}" fill="{NOCH}" opacity="{1-utro*.75:.2f}"/>'
           f'<path d="{put}" fill="{RASSV}" opacity="{utro*.85:.2f}"/>'
           f'<circle cx="{px+pw*.56:.0f}" cy="{py+ph_*.40:.0f}" r="86"'
           f' fill="#e8eef6" opacity="{1-utro*.8:.2f}"/>'
           f'<circle cx="{px+pw*.30:.0f}" cy="{py+ph_*.32:.0f}" r="94"'
           f' fill="{SVET}" opacity="{utro*.7:.2f}"/>')
    for i in range(4):
        ox_ = px + ((t * 40 + i * 260) % (pw + 300)) - 150
        vid += (f'<ellipse cx="{ox_:.0f}" cy="{py+ph_*(.30+i*.14):.0f}"'
                f' rx="{130-i*16:.0f}" ry="{40-i*5:.0f}" fill="#8e9ab0"'
                f' opacity="{.44-utro*.2:.2f}"/>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#6a5030"'
                    f' stroke-width="34"/>'
            + f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#6a5030" stroke-width="24"/>'
            + f'<line x1="{px:.0f}" y1="{py+ph_*.48:.0f}" x2="{px+pw:.0f}"'
              f' y2="{py+ph_*.48:.0f}" stroke="#6a5030" stroke-width="20"/>'
            + f'<rect x="{px-56:.0f}" y="{py-52:.0f}" width="{pw+112:.0f}"'
              f' height="44" rx="12" fill="#7d5a3c" {o(5)}/>'
            + f'<rect x="{px-40:.0f}" y="{py+ph_-10:.0f}" width="{pw+80:.0f}"'
              f' height="42" rx="12" fill="url(#dosk)" {o(6)}/>'
            + zanaveska(px + 30, py + 10, 230, 130, None, t, 1)
            + zanaveska(px + pw - 30, py + 10, 230, 130, None, t, -1))
    # КРОВАТЬ с горой подушек
    s += SL(Z_SRED, _krovat(360, pol, 1180, t, 651, True, 340))
    s += SL(Z_SRED, _podushka(560, 700, 330, 200, t, .2, .4, .0)
            + _podushka(820, 672, 300, 190, t, .5, .3, .0)
            + _podushka(1070, 694, 310, 190, t, .8, .35, .0))
    # ОДЕЯЛО ДЫШИТ — лоскутное, одно на двоих
    s += SL(Z_SRED, _odeyalo_kray(400, 800, 1100, 230, t,
                                  .2 + .3 * abs(A.w(t, 1.9, .2)), TKAN2))
    s += SL(Z_SRED, _tumbochka_veschi(1680, pol, 230, t, 200))
    s += SL(Z_SRED, lampa(1780, pol - 206, t, .85, True))
    s += SL(Z_SRED, hodiki(170, 300, t, 1.2))
    # ДВЕ ФИГУРЫ лежат, к утру дед садится
    dx_, dy_, dh = 760, 812 - 180 * sel, 430 + 190 * sel
    bx_, by_, bh = 1180, 806, 400
    _figury_kadra((dx_, dy_, dh), (bx_, by_, bh))
    ded = figura(dx_, dy_, dh, t, col="#e2d6c2", kant="#ffd98a", ph=.3,
                 boroda=True, naklon=4.0 - 3.0 * sel)
    g1, (n1x, n1y), _ = _ruka_mimo(dx_, dy_, dh, -1, dh * .34, 52 - 26 * sel, t,
                                   "#e2d6c2", "#ffd98a", .2, 4.0)
    g2, (n2x, n2y), _ = _ruka_mimo(dx_, dy_, dh, 1, dh * .40,
                                   50 - 96 * sel, t, "#e2d6c2", "#ffd98a",
                                   .6, 4.0)
    ded += g1 + g2
    bab = figura(bx_, by_, bh, t, col="#e2d6c2", kant="#ffd98a", platok=True,
                 ph=.7, profil=True, naklon=9.0)
    b1, (q1x, q1y), _ = _ruka_mimo(bx_, by_, bh, 1, bh * .34, 48, t,
                                   "#e2d6c2", "#ffd98a", .1, 3.0)
    b2, (q2x, q2y), _ = _ruka_so_sgibom(bx_, by_, bh, -1, bh * .22, 20,
                                        bh * .22, -40, t, "#e2d6c2",
                                        "#ffd98a", .5, 3.0)
    bab += b1 + b2
    s += SL(Z_SRED, ded)
    s += SL(Z_SRED, bab)
    # ПОДНЯТАЯ РУКА БАБКИ «тише»: кисть варежкой, пальцев не рисуем — хват
    # читается по вертикальному рукаву и светлому овалу на его конце
    s += SL(Z_SRED, f'<ellipse cx="{q2x:.0f}" cy="{q2y-26:.0f}" rx="13"'
                    f' ry="30" fill="#e8d8c0" {o(4)}/>')
    s += SL(Z_SRED, _varezhka(q2x, q2y + 6, bh, t, .5))
    # УВЕРЕННЫЙ ЖЕСТ деда на небо к утру — рукав вверх и наружу, без предмета
    if sel > .3:
        s += SL(Z_SRED, f'<path d="M{n2x-14:.0f},{n2y+16:.0f} q{22:.0f},{-20:.0f}'
                        f' {44:.0f},{-6:.0f}" fill="none" stroke="#ffd98a"'
                        f' stroke-width="8" opacity="{sel*.6:.2f}"/>')
    # нижняя треть
    s += SL(Z_SRED, _polovik(900, pol + 40, 560, 118, "#cdbf9c", "#b8352c")
            + _valenki_u_dveri(300, pol + 36, 1.1, t)
            + _kot_zhivoy(1480, pol + 52, t, 1.1, "#3b3430", .4, True, True)
            + _dvorovaya_utvar(130, pol + 52, 230, t, 653, ["korzina"])
            + _yaschiki(1860, pol + 14, t, 655, 2, .8))
    s += SL(Z_SRED, teplo(1780, pol - 240, 420, 320, .32))
    s += SL(Z_PERED, _stolb_pered(-8, 110, "#150f0c", 0, H))
    s += vinetka(.44)
    return s


# ── ПОМОЩНИКИ ТРЕТЬЕЙ ПАРТИИ ──────────────────────────────────────────────

def _flyuger_petuh(x, y, s_=1.0, t=0.0, ug=0.0, roza=True):
    """КОВАНЫЙ ФЛЮГЕР-ПЕТУХ — главный предмет: тело с прорезным хвостом,
    гребень зубцами, бородка, клюв, лапы на штыре. Поворачивается на штыре
    целиком, со скрипом-дрожью. Роза ветров под ним — ЧЕТЫРЕ СТРЕЛЫ, север
    отмечен двойным наконечником: СВОИХ БУКВ НЕ РИСУЕМ ВООБЩЕ, поэтому ни
    «С», ни «Ю» на розе нет (правило ролика сильнее буквы задания)."""
    drozh = 1.6 * A.w(t, 7.0, .2)
    s = (f'<rect x="{x-9*s_:.0f}" y="{y:.0f}" width="{18*s_:.0f}"'
         f' height="{150*s_:.0f}" rx="{8*s_:.0f}" fill="{ZHELEZ}" {o(5)}/>')
    if roza:
        s += (f'<circle cx="{x:.0f}" cy="{y+40*s_:.0f}" r="{70*s_:.0f}"'
              f' fill="none" stroke="#4e4a47" stroke-width="{7*s_:.0f}"/>')
        for i in range(4):
            a = math.radians(i * 90)
            ex = x + math.cos(a) * 92 * s_
            ey = y + 40 * s_ + math.sin(a) * 92 * s_
            s += (f'<line x1="{x:.0f}" y1="{y+40*s_:.0f}" x2="{ex:.0f}"'
                  f' y2="{ey:.0f}" stroke="#4e4a47" stroke-width="{9*s_:.0f}"/>'
                  f'<path d="M{ex:.0f},{ey:.0f} l{-math.cos(a)*22*s_-math.sin(a)*11*s_:.0f},'
                  f'{-math.sin(a)*22*s_+math.cos(a)*11*s_:.0f}'
                  f' l{0:.0f},{0:.0f} l{-math.cos(a)*22*s_+math.sin(a)*11*s_:.0f},'
                  f'{-math.sin(a)*22*s_-math.cos(a)*11*s_:.0f} Z" fill="#5f5a56"'
                  f' {o(3)}/>')
        # север отмечен не буквой, а двойным наконечником и звездой
        s += (f'<path d="M{x:.0f},{y-76*s_:.0f} l{14*s_:.0f},{26*s_:.0f}'
              f' l{-28*s_:.0f},0 Z" fill="#cfe4f5" {o(3)}/>'
              f'<path d="M{x:.0f},{y-108*s_:.0f} l{7*s_:.0f},{18*s_:.0f}'
              f' l{19*s_:.0f},{3*s_:.0f} l{-15*s_:.0f},{13*s_:.0f}'
              f' l{5*s_:.0f},{19*s_:.0f} l{-16*s_:.0f},{-10*s_:.0f}'
              f' l{-16*s_:.0f},{10*s_:.0f} l{5*s_:.0f},{-19*s_:.0f}'
              f' l{-15*s_:.0f},{-13*s_:.0f} l{19*s_:.0f},{-3*s_:.0f} Z"'
              f' fill="#cfe4f5" {o(3)}/>')
    s += f'<g transform="rotate({ug + drozh:.1f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x-120*s_:.0f},{y-10*s_:.0f}'
          f' q{30*s_:.0f},{-64*s_:.0f} {104*s_:.0f},{-58*s_:.0f}'
          f' q{46*s_:.0f},{6*s_:.0f} {58*s_:.0f},{34*s_:.0f}'
          f' q{10*s_:.0f},{34*s_:.0f} {-38*s_:.0f},{48*s_:.0f}'
          f' q{-66*s_:.0f},{16*s_:.0f} {-124*s_:.0f},{-24*s_:.0f} Z"'
          f' fill="#3d3a38" {o(7)}/>')
    for i in range(5):
        s += (f'<path d="M{x-118*s_+i*6*s_:.0f},{y-14*s_:.0f}'
              f' q{-48*s_:.0f},{(-34+i*18)*s_:.0f} {-86*s_:.0f},{(-52+i*26)*s_:.0f}'
              f' q{40*s_:.0f},{8*s_:.0f} {86*s_:.0f},{10*s_:.0f} Z"'
              f' fill="#4e4a47" {o(4)}/>')
    s += (f'<circle cx="{x+118*s_:.0f}" cy="{y-56*s_:.0f}" r="{30*s_:.0f}"'
          f' fill="#3d3a38" {o(5)}/>'
          f'<path d="M{x+146*s_:.0f},{y-56*s_:.0f} l{42*s_:.0f},{10*s_:.0f}'
          f' l{-40*s_:.0f},{16*s_:.0f} Z" fill="{ORA}" {o(4)}/>'
          f'<circle cx="{x+124*s_:.0f}" cy="{y-64*s_:.0f}" r="{6*s_:.0f}"'
          f' fill="#ffd98a"/>')
    for i in range(4):
        s += (f'<path d="M{x+100*s_+i*12*s_:.0f},{y-84*s_:.0f}'
              f' l{6*s_:.0f},{-22*s_:.0f} l{8*s_:.0f},{20*s_:.0f} Z"'
              f' fill="{KRAS}" {o(3)}/>')
    s += (f'<path d="M{x+134*s_:.0f},{y-30*s_:.0f} q{10*s_:.0f},{22*s_:.0f}'
          f' {-6*s_:.0f},{30*s_:.0f}" fill="none" stroke="{KRAS}"'
          f' stroke-width="{12*s_:.0f}"/>')
    for i in (-1, 1):
        s += (f'<line x1="{x+i*18*s_:.0f}" y1="{y+10*s_:.0f}"'
              f' x2="{x+i*26*s_:.0f}" y2="{y+46*s_:.0f}" stroke="#3d3a38"'
              f' stroke-width="{max(3,7*s_):.0f}"/>')
    return s + "</g>"


def _konek_kryshi(x, y, w_, t, seed=3, sneg=True):
    """Конёк крыши крупно: тёс в два скатa, охлупень по гребню, снеговая
    подушка и стропильные выпуски."""
    rnd = random.Random(seed)
    s = (f'<path d="M{x:.0f},{y+200:.0f} L{x+w_*.5:.0f},{y:.0f}'
         f' L{x+w_:.0f},{y+200:.0f} L{x+w_:.0f},{y+440:.0f} L{x:.0f},{y+440:.0f} Z"'
         f' fill="#6b5340" {o(8)}/>')
    for i in range(14):
        s += (f'<line x1="{x+i*(w_/14.0):.0f}" y1="{y+440:.0f}"'
              f' x2="{x+w_*.5:.0f}" y2="{y+4:.0f}" stroke="#4e3c2c"'
              f' stroke-width="6" opacity=".6"/>')
    s += (f'<path d="M{x+w_*.5-30:.0f},{y-16:.0f} q{30:.0f},{-22:.0f} {60:.0f},0'
          f' L{x+w_*.5+26:.0f},{y+42:.0f} L{x+w_*.5-26:.0f},{y+42:.0f} Z"'
          f' fill="#5a4530" {o(6)}/>')
    if sneg:
        s += (f'<path d="M{x-20:.0f},{y+214:.0f} Q{x+w_*.5:.0f},{y-18:.0f}'
              f' {x+w_+20:.0f},{y+214:.0f} Q{x+w_*.5:.0f},{y+150:.0f}'
              f' {x-20:.0f},{y+214:.0f} Z" fill="url(#sneg)" opacity=".92"/>')
    for i in range(5):
        bx = x + 60 + i * (w_ - 120) / 4.0
        s += (f'<rect x="{bx:.0f}" y="{y+430:.0f}" width="34" height="56"'
              f' rx="8" fill="#5a4530" {o(4)}/>')
    return s


def _bele_na_verevke(x, y, w_, t, veter=1.0, n=4, seed=5, derev=.0):
    """Бельё на верёвке: рубаха, простыня, полотенце, наволочка. `veter`
    сносит все вещи в ОДНУ сторону, `derev` — бельё деревенеет на морозе и
    висит коробом, почти не шевелясь."""
    rnd = random.Random(seed)
    s = (f'<path d="M{x:.0f},{y:.0f} Q{x+w_*.5:.0f},{y+26-20*derev:.0f}'
         f' {x+w_:.0f},{y:.0f}" fill="none" stroke="#c9b48a" stroke-width="7"/>')
    for i in range(n):
        px = x + 40 + i * (w_ - 80) / max(1, n - 1.0)
        py = y + 18 - 14 * derev
        hh = rnd.uniform(150, 230)
        ww = rnd.uniform(110, 170)
        sn = (26 * veter + 16 * veter * A.w(t, 1.6, i * .3)) * (1 - .82 * derev)
        s += (f'<path d="M{px-ww*.5:.0f},{py:.0f} L{px+ww*.5:.0f},{py:.0f}'
              f' Q{px+ww*.5+sn:.0f},{py+hh*.5:.0f} {px+ww*.46+sn:.0f},{py+hh:.0f}'
              f' Q{px:.0f},{py+hh+18:.0f} {px-ww*.46+sn*.5:.0f},{py+hh:.0f}'
              f' Q{px-ww*.5:.0f},{py+hh*.5:.0f} {px-ww*.5:.0f},{py:.0f} Z"'
              f' fill="{["#f4eedc", "#e8eef0", "#efe3c8", "#dde6ea"][i % 4]}"'
              f' {o(5)}/>')
        for j in range(3):
            s += (f'<path d="M{px-ww*.3+j*ww*.3:.0f},{py+12:.0f}'
                  f' q{6+sn*.2:.0f},{hh*.4:.0f} {sn*.4:.0f},{hh*.86:.0f}"'
                  f' fill="none" stroke="#cfc7ad" stroke-width="5" opacity=".8"/>')
        if derev > .4:
            s += (f'<path d="M{px-ww*.5:.0f},{py+hh:.0f} L{px+ww*.5:.0f},{py+hh:.0f}"'
                  f' fill="none" stroke="{INEY}" stroke-width="11" opacity=".8"/>')
        for e in (-1, 1):
            s += (f'<rect x="{px+e*ww*.34-7:.0f}" y="{py-14:.0f}" width="14"'
                  f' height="30" rx="5" fill="#c9a47a" {o(3)}/>')
    return s


def _luzha_so_ldom(x, y, rx, t, led=.0, ph=.0):
    """Лужа, которая схватывается льдом: вода с отражением (берём готовую
    `_luzha`), поверх растут ледяные перья и матовая корка, по кромке иней."""
    s = _luzha(x, y, rx, t, ph, rx * .34, "#7e97ad")
    if led > .02:
        s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx*led*.96:.0f}"'
              f' ry="{rx*.33*led:.0f}" fill="{LED}" opacity="{.42+.38*led:.2f}"/>')
        for i in range(9):
            a = math.radians(i * 40)
            s += (f'<path d="M{x:.0f},{y:.0f} L{x+math.cos(a)*rx*led*.9:.0f},'
                  f'{y+math.sin(a)*rx*.30*led:.0f}" fill="none" stroke="#e8f1f6"'
                  f' stroke-width="{5*led:.0f}" opacity=".8"/>')
        s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx*1.02:.0f}"'
              f' ry="{rx*.35:.0f}" fill="none" stroke="{INEY}"'
              f' stroke-width="{9*led:.0f}" opacity=".8"/>')
    return s


def _kolodec(x, y, w_, t, h_=330, vorot=True):
    """КОЛОДЕЦ С ВОРОТОМ — главный предмет: сруб в венцы, стойки, вал с
    рукоятью, цепь с ведром, двускатная кровелька. Середина сруба остаётся
    ТЁМНЫМ ПРОЁМОМ — там и стоит настоящий кадр."""
    s = (f'{ten(x + w_ * .5, y + 14, w_ * .54, 22, .55)}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="10" fill="url(#brev)" {o(8)}/>')
    for i in range(4):
        yy = y - h_ + 20 + i * (h_ - 26) / 4.0
        s += (f'<rect x="{x-14:.0f}" y="{yy:.0f}" width="{w_+28:.0f}"'
              f' height="{(h_-26)/4.0-8:.0f}" rx="14"'
              f' fill="{BREVNO if i % 2 == 0 else BREVNO2}" {o(5)}/>')
    for i in (0, 1):
        sx = x + 30 + i * (w_ - 86)
        s += (f'<rect x="{sx:.0f}" y="{y-h_-300:.0f}" width="56" height="320"'
              f' rx="10" fill="#6b5340" {o(6)}/>')
    s += (f'<path d="M{x-30:.0f},{y-h_-290:.0f} L{x+w_*.5:.0f},{y-h_-396:.0f}'
          f' L{x+w_+30:.0f},{y-h_-290:.0f} Z" fill="#5a4530" {o(6)}/>'
          f'<path d="M{x-30:.0f},{y-h_-290:.0f} L{x+w_*.5:.0f},{y-h_-396:.0f}'
          f' L{x+w_*.5:.0f},{y-h_-370:.0f} L{x+10:.0f},{y-h_-294:.0f} Z"'
          f' fill="{SNEG}" opacity=".9"/>')
    if vorot:
        kr = (t * 26.0) % 360.0
        s += (f'<rect x="{x+40:.0f}" y="{y-h_-160:.0f}" width="{w_-74:.0f}"'
              f' height="52" rx="24" fill="url(#derev)" {o(6)}/>')
        for i in range(5):
            s += (f'<line x1="{x+60+i*(w_-120)/4.0:.0f}" y1="{y-h_-158:.0f}"'
                  f' x2="{x+60+i*(w_-120)/4.0:.0f}" y2="{y-h_-112:.0f}"'
                  f' stroke="#5b4428" stroke-width="5" opacity=".8"/>')
        s += (f'<g transform="rotate({kr:.0f} {x+w_-30:.0f} {y-h_-134:.0f})">'
              f'<rect x="{x+w_-34:.0f}" y="{y-h_-140:.0f}" width="86" height="16"'
              f' rx="7" fill="{ZHELEZ}" {o(4)}/>'
              f'<rect x="{x+w_+42:.0f}" y="{y-h_-144:.0f}" width="18" height="46"'
              f' rx="8" fill="#8a6038" {o(4)}/></g>')
        for i in range(7):
            s += (f'<circle cx="{x+w_*.5+3*math.sin(t+i):.0f}"'
                  f' cy="{y-h_-100+i*17:.0f}" r="9" fill="none"'
                  f' stroke="{ZHELEZ}" stroke-width="5"/>')
    return s


def _koromyslo(x, y, s_=1.0, t=0.0, vedra=True):
    """Коромысло с двумя вёдрами, прислонённое к срубу: дуга с зарубками,
    крючья, вёдра покачиваются."""
    s = (f'<path d="M{x-150*s_:.0f},{y:.0f} Q{x:.0f},{y-70*s_:.0f}'
         f' {x+150*s_:.0f},{y:.0f}" fill="none" stroke="url(#derev)"'
         f' stroke-width="{24*s_:.0f}" stroke-linecap="round"/>'
         f'<path d="M{x-140*s_:.0f},{y-6*s_:.0f} Q{x:.0f},{y-64*s_:.0f}'
         f' {x+140*s_:.0f},{y-6*s_:.0f}" fill="none" stroke="#c9a47a"'
         f' stroke-width="{6*s_:.0f}" opacity=".6"/>')
    if vedra:
        for i in (-1, 1):
            kol = 4.0 * A.w(t, 2.3, .2 + (0 if i < 0 else .4))
            vx = x + i * 150 * s_
            s += (f'<g transform="rotate({kol:.1f} {vx:.0f} {y:.0f})">'
                  f'<path d="M{vx-10*s_:.0f},{y:.0f} q{2*s_:.0f},{34*s_:.0f}'
                  f' {10*s_:.0f},{40*s_:.0f}" fill="none" stroke="{ZHELEZ}"'
                  f' stroke-width="{7*s_:.0f}"/>'
                  f'<path d="M{vx-44*s_:.0f},{y+40*s_:.0f} q{6*s_:.0f},{78*s_:.0f}'
                  f' {44*s_:.0f},{78*s_:.0f} q{38*s_:.0f},0 {44*s_:.0f},{-78*s_:.0f} Z"'
                  f' fill="#b6bcc2" {o(5)}/>'
                  f'<ellipse cx="{vx:.0f}" cy="{y+40*s_:.0f}" rx="{44*s_:.0f}"'
                  f' ry="{13*s_:.0f}" fill="#cfd5da" {o(4)}/>'
                  f'<ellipse cx="{vx:.0f}" cy="{y+44*s_:.0f}" rx="{34*s_:.0f}"'
                  f' ry="{9*s_:.0f}" fill="{VODA}" opacity=".7"/></g>')
    return s


def _rogozha(x, y, w_, t, h_=120, seed=5):
    """Рогожа, которой накрывают поленницу: плетёное полотно с бахромой,
    углы прихвачены камнями, край хлопает на ветру."""
    rnd = random.Random(seed)
    hlop = 10 * A.w(t, 1.7, .2)
    s = (f'<path d="M{x:.0f},{y:.0f} Q{x+w_*.5:.0f},{y-30:.0f} {x+w_:.0f},{y:.0f}'
         f' L{x+w_-10:.0f},{y+h_+hlop:.0f} Q{x+w_*.5:.0f},{y+h_+20:.0f}'
         f' {x+10:.0f},{y+h_:.0f} Z" fill="#9c8a62" {o(6)}/>')
    for i in range(int(w_ / 48)):
        s += (f'<line x1="{x+10+i*48:.0f}" y1="{y-6:.0f}" x2="{x+14+i*48:.0f}"'
              f' y2="{y+h_+8:.0f}" stroke="#8a7a46" stroke-width="5"'
              f' opacity=".7"/>')
    for i in range(3):
        s += (f'<path d="M{x+6:.0f},{y+18+i*(h_-30)/3.0:.0f}'
              f' Q{x+w_*.5:.0f},{y+6+i*(h_-30)/3.0:.0f}'
              f' {x+w_-6:.0f},{y+20+i*(h_-30)/3.0:.0f}" fill="none"'
              f' stroke="#b8a86a" stroke-width="6" opacity=".7"/>')
    for ex in (x + 14, x + w_ - 14):
        s += (f'<ellipse cx="{ex:.0f}" cy="{y+4:.0f}" rx="26" ry="18"'
              f' fill="{KAMEN}" {o(4)}/>')
    for i in range(int(w_ / 36)):
        s += (f'<line x1="{x+12+i*36:.0f}" y1="{y+h_+6:.0f}"'
              f' x2="{x+10+i*36+rnd.uniform(-6,6):.0f}" y2="{y+h_+26:.0f}"'
              f' stroke="#8a7a46" stroke-width="4"/>')
    return s


def _zont_mokryy(x, y, t, s_=1.0, ph=.0):
    """Мокрый зонт на гвозде: сложенный купол клиньями, спицы наружу,
    крючковатая ручка, с кончика срывается капля."""
    kap = (t * .6 + ph) % 1.0
    s = (f'<rect x="{x-16:.0f}" y="{y-22:.0f}" width="32" height="14" rx="6"'
         f' fill="{ZHELEZ}" {o(3)}/>'
         f'<path d="M{x-26:.0f},{y:.0f} q{26:.0f},{-30:.0f} {52:.0f},0'
         f' L{x+30:.0f},{y+230*s_:.0f} q{-30:.0f},{26:.0f} {-60:.0f},0 Z"'
         f' fill="#3f5c7a" {o(6)}/>')
    for i in range(4):
        s += (f'<path d="M{x-20+i*14:.0f},{y+8:.0f} q{6:.0f},{110*s_:.0f}'
              f' {2:.0f},{216*s_:.0f}" fill="none" stroke="#2f4a66"'
              f' stroke-width="6" opacity=".85"/>')
    s += (f'<path d="M{x:.0f},{y+230*s_:.0f} l{-16:.0f},{34*s_:.0f}'
          f' l{10:.0f},{4*s_:.0f} l{8:.0f},{-20*s_:.0f} l{8:.0f},{20*s_:.0f}'
          f' l{10:.0f},{-4*s_:.0f} Z" fill="#2f4a66" {o(4)}/>'
          f'<path d="M{x-2:.0f},{y+266*s_:.0f} q{2:.0f},{40*s_:.0f}'
          f' {-30:.0f},{40*s_:.0f}" fill="none" stroke="#7d5636"'
          f' stroke-width="{14*s_:.0f}"/>'
          f'<ellipse cx="{x+2:.0f}" cy="{y+272*s_+kap*90:.0f}" rx="7"'
          f' ry="{11+5*kap:.0f}" fill="#9fc4d8" opacity="{1-kap:.2f}"/>')
    return s


def _plasch_na_gvozde(x, y, h_, t, ph=.0, col="#4e5a46"):
    """Мокрый плащ на гвозде: брезентовые полы, капюшон, пояс болтается,
    по подолу стекают капли."""
    kach = 1.6 * A.w(t, 3.0, ph)
    s = (f'<g transform="rotate({kach:.1f} {x:.0f} {y:.0f})">'
         f'<rect x="{x-18:.0f}" y="{y-24:.0f}" width="36" height="14" rx="6"'
         f' fill="{ZHELEZ}" {o(3)}/>'
         f'<path d="M{x:.0f},{y:.0f} q{-78:.0f},{22:.0f} {-92:.0f},{96:.0f}'
         f' L{x-82:.0f},{y+h_:.0f} L{x+82:.0f},{y+h_:.0f} L{x+92:.0f},{y+96:.0f}'
         f' q{-14:.0f},{-74:.0f} {-92:.0f},{-96:.0f} Z" fill="{col}" {o(6)}/>'
         f'<path d="M{x-44:.0f},{y+6:.0f} q{44:.0f},{-46:.0f} {88:.0f},0'
         f' q{-20:.0f},{30:.0f} {-88:.0f},0 Z" fill="#3f4a38" {o(5)}/>'
         f'<path d="M{x:.0f},{y+30:.0f} L{x+14:.0f},{y+h_:.0f}" fill="none"'
         f' stroke="#2f3a2a" stroke-width="11"/>'
         f'<path d="M{x+70:.0f},{y+h_*.52:.0f} q{34:.0f},{54:.0f} {-6:.0f},{96:.0f}"'
         f' fill="none" stroke="#3f4a38" stroke-width="13"/></g>')
    for i in range(4):
        kap = ((t * .7 + i / 4.0) % 1.0)
        s += (f'<ellipse cx="{x-58+i*38:.0f}" cy="{y+h_+8+kap*70:.0f}" rx="6"'
              f' ry="{10+5*kap:.0f}" fill="#9fc4d8" opacity="{1-kap:.2f}"/>')
    return s


def _kaloshi(x, y, s_=1.0, t=0.0, luzhica=True):
    """Калоши в лужице: два блестящих резиновых башмака с бортиком, носки
    врозь, под ними растекается вода с кругами."""
    s = ""
    if luzhica:
        s += _luzha(x + 10 * s_, y + 16 * s_, 130 * s_, t, .3, 34 * s_, "#6a8296")
    for i, (dx, ug) in enumerate(((-56 * s_, -8), (58 * s_, 10))):
        s += (f'<g transform="rotate({ug:.0f} {x+dx:.0f} {y:.0f})">'
              f'<path d="M{x+dx-50*s_:.0f},{y:.0f} q{4*s_:.0f},{-52*s_:.0f}'
              f' {40*s_:.0f},{-56*s_:.0f} q{40*s_:.0f},{2*s_:.0f}'
              f' {56*s_:.0f},{34*s_:.0f} q{10*s_:.0f},{22*s_:.0f}'
              f' {-16*s_:.0f},{24*s_:.0f} Z" fill="#2a2726" {o(5)}/>'
              f'<path d="M{x+dx-50*s_:.0f},{y-8*s_:.0f} q{50*s_:.0f},{-12*s_:.0f}'
              f' {96*s_:.0f},{14*s_:.0f}" fill="none" stroke="#5f5a56"'
              f' stroke-width="{8*s_:.0f}"/>'
              f'<path d="M{x+dx-26*s_:.0f},{y-44*s_:.0f} q{22*s_:.0f},{-14*s_:.0f}'
              f' {44*s_:.0f},{-4*s_:.0f}" fill="none" stroke="#8f979d"'
              f' stroke-width="{7*s_:.0f}"'
              f' opacity="{.4+.3*abs(A.w(t,2.6,i*.4)):.2f}"/>'
              f'<ellipse cx="{x+dx:.0f}" cy="{y+4*s_:.0f}" rx="{52*s_:.0f}"'
              f' ry="{10*s_:.0f}" fill="#1d1a18" opacity=".8"/></g>')
    return s


def _listki_tuchki(x, y, w_, t, otgib=.0, n=6, seed=7):
    """Отогнутые листки численника: каждый лист отходит веером, и на каждом
    нарисована тучка с каплями — значит сырость до конца месяца. Цифр и букв
    на листках НЕТ, только тучка."""
    s = ""
    for i in range(n):
        p = max(0.0, min(1.0, otgib * n - i))
        ug = -8 - 74 * p
        px = x + i * 6
        s += (f'<g transform="rotate({ug:.1f} {px:.0f} {y:.0f})">'
              f'<rect x="{px-w_*.5:.0f}" y="{y:.0f}" width="{w_:.0f}"'
              f' height="{w_*1.06:.0f}" rx="8" fill="#f4eedc" {o(5)}/>'
              f'<rect x="{px-w_*.5:.0f}" y="{y:.0f}" width="{w_:.0f}"'
              f' height="{w_*.14:.0f}" fill="{TKAN}" opacity=".85"/>')
        cx, cy = px, y + w_ * .52
        s += (f'<path d="M{cx-w_*.26:.0f},{cy:.0f} q{-w_*.08:.0f},{-w_*.22:.0f}'
              f' {w_*.14:.0f},{-w_*.24:.0f} q{w_*.08:.0f},{-w_*.18:.0f}'
              f' {w_*.30:.0f},{-w_*.06:.0f} q{w_*.22:.0f},{-w_*.04:.0f}'
              f' {w_*.24:.0f},{w_*.18:.0f} q{w_*.12:.0f},{w_*.06:.0f}'
              f' {w_*.02:.0f},{w_*.16:.0f} Z" fill="#8e9ab0" {o(4)}/>')
        for j in range(3):
            kap = ((t * .9 + j / 3.0 + i * .1) % 1.0)
            s += (f'<ellipse cx="{cx-w_*.14+j*w_*.14:.0f}"'
                  f' cy="{cy+w_*.10+kap*w_*.30:.0f}" rx="{w_*.026:.0f}"'
                  f' ry="{w_*.046:.0f}" fill="#9fc4d8"'
                  f' opacity="{1-kap:.2f}"/>')
        s += "</g>"
    return s


def _perila_balkona(x, y, w_, t, h_=190, reshetka=True):
    """Перила балкона: бетонный поручень, решётка из прутьев с косыми
    вставками, плита снизу и облупленная краска."""
    s = (f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="34" rx="12"'
         f' fill="{BETON}" {o(6)}/>'
         f'<rect x="{x:.0f}" y="{y-h_+34:.0f}" width="{w_:.0f}" height="12"'
         f' fill="{BETON2}" opacity=".85"/>')
    if reshetka:
        for i in range(int(w_ / 54) + 1):
            px = x + 10 + i * 54
            if px > x + w_ - 10:
                break
            s += (f'<rect x="{px:.0f}" y="{y-h_+46:.0f}" width="12"'
                  f' height="{h_-46:.0f}" rx="5" fill="#7a8288" {o(3)}/>')
        for i in range(int(w_ / 108) + 1):
            px = x + 14 + i * 108
            s += (f'<line x1="{px:.0f}" y1="{y-6:.0f}" x2="{px+96:.0f}"'
                  f' y2="{y-h_+50:.0f}" stroke="#8f979d" stroke-width="8"'
                  f' opacity=".8"/>')
    s += (f'<rect x="{x-14:.0f}" y="{y:.0f}" width="{w_+28:.0f}" height="46"'
          f' rx="10" fill="{BETON2}" {o(6)}/>')
    rnd = random.Random(int(x) + 3)
    for i in range(7):
        s += (f'<ellipse cx="{x+rnd.uniform(20,w_-20):.0f}"'
              f' cy="{y-h_+rnd.uniform(6,28):.0f}" rx="{rnd.uniform(14,30):.0f}"'
              f' ry="{rnd.uniform(5,11):.0f}" fill="#8a9298" opacity=".6"/>')
    return s


def _yaschik_barhatcev(x, y, w_, t, seed=5):
    """Ящик с засохшими бархатцами: деревянный короб, сухая земля комьями,
    бурые стебли с пустыми головками, пара листьев ещё держится."""
    rnd = random.Random(seed)
    s = (f'{ten(x + w_ * .5, y + 8, w_ * .52, 14, .45)}'
         f'<rect x="{x:.0f}" y="{y-110:.0f}" width="{w_:.0f}" height="110"'
         f' rx="8" fill="url(#dosk)" {o(6)}/>'
         f'<rect x="{x-8:.0f}" y="{y-118:.0f}" width="{w_+16:.0f}" height="20"'
         f' rx="7" fill="#8a6038" {o(4)}/>'
         f'<rect x="{x+10:.0f}" y="{y-98:.0f}" width="{w_-20:.0f}" height="26"'
         f' rx="6" fill="#4a3a2a"/>')
    for i in range(8):
        s += (f'<ellipse cx="{x+16+i*(w_-32)/7.0:.0f}" cy="{y-96:.0f}"'
              f' rx="{rnd.uniform(12,22):.0f}" ry="{rnd.uniform(6,11):.0f}"'
              f' fill="#3f3326"/>')
    for i in range(6):
        px = x + 24 + i * (w_ - 48) / 5.0
        ug = rnd.uniform(-26, 26)
        hh = rnd.uniform(90, 150)
        s += (f'<g transform="rotate({ug + 2 * A.w(t, 2.4, i * .3):.1f}'
              f' {px:.0f} {y-96:.0f})">'
              f'<path d="M{px:.0f},{y-96:.0f} q{8:.0f},{-hh*.5:.0f}'
              f' {-4:.0f},{-hh:.0f}" fill="none" stroke="#7a6a4a"'
              f' stroke-width="8"/>'
              f'<ellipse cx="{px-4:.0f}" cy="{y-96-hh:.0f}" rx="16" ry="12"'
              f' fill="#8a6a3c" {o(3)}/>')
        for j in range(2):
            s += (f'<path d="M{px+2:.0f},{y-96-hh*.5:.0f}'
                  f' q{18-j*36:.0f},{-14:.0f} {26-j*52:.0f},{4:.0f}'
                  f' q{-18+j*36:.0f},{10:.0f} {-26+j*52:.0f},{-4:.0f} Z"'
                  f' fill="#6f7a44" opacity=".85" {o(3)}/>')
        s += "</g>"
    return s


def _prischepki(x, y, w_, t, n=6, seed=3):
    """Прищепки на верёвке: деревянные с пружинкой, часть качается, часть
    висит криво; верёвка чуть провисает."""
    rnd = random.Random(seed)
    s = (f'<path d="M{x:.0f},{y:.0f} Q{x+w_*.5:.0f},{y+28:.0f} {x+w_:.0f},{y:.0f}"'
         f' fill="none" stroke="#c9b48a" stroke-width="7"/>')
    for i in range(n):
        p = i / max(1, n - 1.0)
        px = x + w_ * p
        py = y + 28 * (1 - (2 * p - 1) ** 2)
        kol = 10 * A.w(t, 1.9, i * .35)
        s += (f'<g transform="rotate({kol:.1f} {px:.0f} {py:.0f})">'
              f'<rect x="{px-11:.0f}" y="{py-4:.0f}" width="22" height="58"'
              f' rx="7" fill="#c9a47a" {o(4)}/>'
              f'<line x1="{px:.0f}" y1="{py+8:.0f}" x2="{px:.0f}" y2="{py+52:.0f}"'
              f' stroke="#8a6038" stroke-width="4"/>'
              f'<rect x="{px-13:.0f}" y="{py+16:.0f}" width="26" height="8"'
              f' rx="4" fill="#9aa3aa" {o(3)}/></g>')
    return s


def _strelka_vetra(x, y, dl, ug, t, col="#4e8ad0", n=3):
    """Синяя стрелка ветра: древко с пунктиром и наконечник, за ней ещё две
    короткие — ветер виден направлением, а не пятном."""
    s = ""
    for i in range(n):
        p = ((t * .9 + i / float(n)) % 1.0)
        d2 = dl * (.5 + .5 * p)
        a = math.radians(ug)
        ex, ey = x + d2 * math.cos(a), y + d2 * math.sin(a)
        s += (f'<line x1="{x:.0f}" y1="{y + i * 22 - 22:.0f}" x2="{ex:.0f}"'
              f' y2="{ey + i * 22 - 22:.0f}" stroke="{col}"'
              f' stroke-width="{11-3*i:.0f}" stroke-linecap="round"'
              f' opacity="{(1-p)*.9:.2f}"/>'
              f'<path d="M{ex:.0f},{ey+i*22-22:.0f}'
              f' l{-26*math.cos(a)+13*math.sin(a):.0f},'
              f'{-26*math.sin(a)-13*math.cos(a):.0f}'
              f' l{0:.0f},{26:.0f} Z" fill="{col}"'
              f' opacity="{(1-p)*.9:.2f}"/>')
    return s


def _sharf_otletaet(x, y, dl, t, ug=0.0, col=TKAN):
    """Шарф, который относит ветром: два конца летят в одну сторону волной,
    на концах бахрома."""
    s = ""
    for i, (sm, w_) in enumerate(((0, 34), (26, 26))):
        vol = 20 * A.w(t, 1.4, i * .4)
        s += (f'<path d="M{x:.0f},{y+sm:.0f}'
              f' Q{x+dl*.4:.0f},{y+sm-40+vol:.0f} {x+dl*.72:.0f},{y+sm+10:.0f}'
              f' Q{x+dl*.9:.0f},{y+sm+40+vol:.0f} {x+dl:.0f},{y+sm-6:.0f}"'
              f' fill="none" stroke="{col}" stroke-width="{w_:.0f}"'
              f' stroke-linecap="round"/>')
        for j in range(4):
            s += (f'<line x1="{x+dl:.0f}" y1="{y+sm-20+j*11:.0f}"'
                  f' x2="{x+dl+26:.0f}" y2="{y+sm-24+j*14:.0f}" stroke="{col}"'
                  f' stroke-width="5"/>')
    s += (f'<path d="M{x-20:.0f},{y+4:.0f} q{22:.0f},{18:.0f} {44:.0f},{2:.0f}"'
          f' fill="none" stroke="{col}" stroke-width="30"/>')
    return s


def _buda_s_psom(x, y, s_=1.0, t=0.0, ph=.0):
    """Будка и пёс: двускатная конура с круглым лазом и жестяной кромкой,
    пёс лежит у входа — голова на лапах, ухо поводит, хвост постукивает,
    на колышке цепь."""
    w2, h2 = 220 * s_, 190 * s_
    s = (f'{ten(x, y + 10 * s_, w2 * .56, 16 * s_, .5)}'
         f'<rect x="{x-w2/2:.0f}" y="{y-h2:.0f}" width="{w2:.0f}"'
         f' height="{h2:.0f}" rx="8" fill="url(#dosk)" {o(7)}/>'
         f'<path d="M{x-w2*.60:.0f},{y-h2:.0f} L{x:.0f},{y-h2-80*s_:.0f}'
         f' L{x+w2*.60:.0f},{y-h2:.0f} Z" fill="#6b5340" {o(6)}/>'
         f'<circle cx="{x:.0f}" cy="{y-h2*.46:.0f}" r="{w2*.26:.0f}"'
         f' fill="#241a12" {o(5)}/>'
         f'<circle cx="{x:.0f}" cy="{y-h2*.46:.0f}" r="{w2*.26:.0f}"'
         f' fill="none" stroke="#8f979d" stroke-width="{7*s_:.0f}"/>')
    for i in range(5):
        s += (f'<line x1="{x-w2*.44+i*w2*.22:.0f}" y1="{y-h2+8*s_:.0f}"'
              f' x2="{x-w2*.44+i*w2*.22:.0f}" y2="{y-6*s_:.0f}"'
              f' stroke="#5b4428" stroke-width="{max(3,5*s_):.0f}" opacity=".7"/>')
    # пёс лежит у входа
    px = x + w2 * .72
    hv = 22 * s_ * A.w(t, 1.5, ph)
    uho = 8 * s_ * A.w(t, 2.6, ph + .3)
    s += (f'{ten(px, y + 6 * s_, 96 * s_, 16 * s_, .45)}'
          f'<ellipse cx="{px:.0f}" cy="{y-36*s_:.0f}" rx="{104*s_:.0f}"'
          f' ry="{40*s_:.0f}" fill="#8a6a4a" {o(5)}/>'
          f'<path d="M{px-104*s_:.0f},{y-30*s_:.0f} q{-40*s_:.0f},{10*s_:.0f}'
          f' {-54*s_:.0f},{hv:.0f}" fill="none" stroke="#8a6a4a"'
          f' stroke-width="{18*s_:.0f}" stroke-linecap="round"/>'
          f'<circle cx="{px+92*s_:.0f}" cy="{y-56*s_:.0f}" r="{42*s_:.0f}"'
          f' fill="#9c7a56" {o(5)}/>'
          f'<path d="M{px+120*s_:.0f},{y-44*s_:.0f} q{36*s_:.0f},{4*s_:.0f}'
          f' {38*s_:.0f},{20*s_:.0f} q{-24*s_:.0f},{12*s_:.0f}'
          f' {-44*s_:.0f},{4*s_:.0f} Z" fill="#9c7a56" {o(4)}/>'
          f'<circle cx="{px+156*s_:.0f}" cy="{y-30*s_:.0f}" r="{9*s_:.0f}"'
          f' fill="{K}"/>'
          f'<path d="M{px+64*s_:.0f},{y-86*s_:.0f} q{-10*s_:.0f},{-34*s_-uho:.0f}'
          f' {18*s_:.0f},{-40*s_:.0f} q{10*s_:.0f},{22*s_:.0f} {2*s_:.0f},{44*s_:.0f} Z"'
          f' fill="#7a5a3c" {o(4)}/>'
          f'<circle cx="{px+104*s_:.0f}" cy="{y-66*s_:.0f}" r="{7*s_:.0f}"'
          f' fill="{K}"/>'
          f'<path d="M{px+40*s_:.0f},{y-8*s_:.0f} q{30*s_:.0f},{10*s_:.0f}'
          f' {64*s_:.0f},{2*s_:.0f}" fill="none" stroke="#7a5a3c"'
          f' stroke-width="{16*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<rect x="{x-w2*.74:.0f}" y="{y-40*s_:.0f}" width="{14*s_:.0f}"'
          f' height="{44*s_:.0f}" rx="6" fill="{ZHELEZ}" {o(3)}/>')
    for i in range(6):
        s += (f'<circle cx="{x-w2*.70+i*20*s_:.0f}"'
              f' cy="{y-20*s_+6*s_*math.sin(i+t):.0f}" r="{8*s_:.0f}"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="{4*s_:.0f}"/>')
    return s


def _miska_zerna(x, y, s_=1.0, t=0.0, syplet=.0):
    """Миска с зерном для кур: эмалированная чашка со сколом, зерно горкой,
    пара зёрен летит вниз, когда её наклоняют."""
    r = 76 * s_
    s = (f'{ten(x, y + 8 * s_, r * .9, 12 * s_, .45)}'
         f'<path d="M{x-r:.0f},{y-r*.40:.0f} q{r*.12:.0f},{r*.82:.0f}'
         f' {r*1.0:.0f},{r*.82:.0f} q{r*.88:.0f},0 {r*1.0:.0f},{-r*.82:.0f} Z"'
         f' fill="#e7edf0" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-r*.40:.0f}" rx="{r:.0f}"'
         f' ry="{r*.26:.0f}" fill="#cfd8dc" {o(4)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-r*.38:.0f}" rx="{r*.84:.0f}"'
         f' ry="{r*.20:.0f}" fill="#c9a331" opacity=".95"/>'
         f'<path d="M{x+r*.84:.0f},{y-r*.46:.0f} l{r*.12:.0f},{r*.08:.0f}'
         f' l{-r*.12:.0f},{r*.10:.0f} Z" fill="#9aa3aa" {o(3)}/>')
    rnd = random.Random(int(x) + 19)
    for i in range(14):
        s += (f'<ellipse cx="{x+rnd.uniform(-r*.7,r*.7):.0f}"'
              f' cy="{y-r*.44+rnd.uniform(-r*.08,r*.06):.0f}" rx="{5*s_:.0f}"'
              f' ry="{3.4*s_:.0f}" fill="#d8c08a" opacity=".9"/>')
    if syplet > .05:
        for i in range(7):
            p = ((t * 1.4 + i / 7.0) % 1.0)
            s += (f'<ellipse cx="{x+r*.6+rnd.uniform(-14,14):.0f}"'
                  f' cy="{y-r*.3+p*140:.0f}" rx="{4*s_:.0f}" ry="{3*s_:.0f}"'
                  f' fill="#d8c08a" opacity="{(1-p)*syplet:.2f}"/>')
    return s


def _balkon_plita(x, y, w_, t, h_=40, verevki=2):
    """Балконная плита соседнего балкона: бетонная консоль, экран-отбортовка
    и верёвки с бельём — этажи повторяются, двор читается колодцем."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="8" fill="{BETON2}" {o(5)}/>'
         f'<rect x="{x:.0f}" y="{y-150:.0f}" width="{w_:.0f}" height="150"'
         f' rx="6" fill="{BETON}" opacity=".9" {o(4)}/>')
    for i in range(int(w_ / 46)):
        s += (f'<line x1="{x+10+i*46:.0f}" y1="{y-148:.0f}"'
              f' x2="{x+10+i*46:.0f}" y2="{y-4:.0f}" stroke="#8a9298"'
              f' stroke-width="6" opacity=".7"/>')
    return s


def _navolochka_parus(x, y, w_, t, k=1.0, col="#f4eedc"):
    """Наволочка, надувающаяся парусом: полотнище выгибается по ветру, угол
    приколот прищепкой, по кромке строчка."""
    puz = (40 + 30 * A.w(t, 1.5, .2)) * k
    s = (f'<path d="M{x:.0f},{y:.0f} L{x+w_:.0f},{y-14:.0f}'
         f' Q{x+w_+puz:.0f},{y+w_*.5:.0f} {x+w_*.92:.0f},{y+w_*1.02:.0f}'
         f' Q{x+w_*.4:.0f},{y+w_*1.14:.0f} {x+8:.0f},{y+w_*.98:.0f}'
         f' Q{x-10:.0f},{y+w_*.5:.0f} {x:.0f},{y:.0f} Z" fill="{col}" {o(6)}/>')
    for i in range(3):
        s += (f'<path d="M{x+w_*(.22+i*.26):.0f},{y-8:.0f}'
              f' q{puz*.4:.0f},{w_*.5:.0f} {puz*.2:.0f},{w_*1.0:.0f}"'
              f' fill="none" stroke="#dcd3bb" stroke-width="6" opacity=".85"/>')
    s += (f'<path d="M{x+6:.0f},{y+w_*.96:.0f} Q{x+w_*.5:.0f},{y+w_*1.10:.0f}'
          f' {x+w_*.90:.0f},{y+w_*.98:.0f}" fill="none" stroke="{TKAN2}"'
          f' stroke-width="7" opacity=".7"/>')
    return s


def _kresla_ryad(x, y, w_, t, n=3, h_=300, col="#7a2338", krupno=False):
    """Ряд бархатных кресел кинозала: спинка валиком с пуговицами, сиденье
    откинуто, подлокотники с деревянной накладкой, литые боковины на полу."""
    s = ""
    dw = w_ / float(n)
    for i in range(n):
        bx = x + i * dw
        s += (f'{ten(bx + dw * .5, y + 8, dw * .46, 14, .5)}'
              f'<path d="M{bx+10:.0f},{y-h_:.0f} q{dw*.5-10:.0f},{-40:.0f}'
              f' {dw-20:.0f},0 L{bx+dw-14:.0f},{y-h_*.40:.0f}'
              f' L{bx+14:.0f},{y-h_*.40:.0f} Z" fill="{col}" {o(6)}/>')
        for j in range(3):
            s += (f'<circle cx="{bx+dw*(.26+j*.24):.0f}" cy="{y-h_*.70:.0f}"'
                  f' r="{9 if krupno else 6:.0f}" fill="#5a1626" {o(3)}/>')
        s += (f'<rect x="{bx+8:.0f}" y="{y-h_*.42:.0f}" width="{dw-16:.0f}"'
              f' height="{h_*.16:.0f}" rx="12" fill="#8a2a40" {o(5)}/>'
              f'<rect x="{bx+4:.0f}" y="{y-h_*.28:.0f}" width="{dw-8:.0f}"'
              f' height="{h_*.10:.0f}" rx="10" fill="#6a1c30" {o(4)}/>')
        for e in (bx + 2, bx + dw - 26):
            s += (f'<rect x="{e:.0f}" y="{y-h_*.46:.0f}" width="24"'
                  f' height="{h_*.46:.0f}" rx="9" fill="#5a4530" {o(4)}/>'
                  f'<rect x="{e-4:.0f}" y="{y-h_*.50:.0f}" width="32"'
                  f' height="18" rx="8" fill="#7d5636" {o(3)}/>')
    return s


def _kepka_i_rupor(x, y, s_=1.0, t=0.0):
    """Режиссёрская кепка на рупоре: кепка с козырьком и пуговкой лежит
    поверх жестяного рупора с ремешком."""
    s = (f'<path d="M{x-96*s_:.0f},{y:.0f} L{x+10*s_:.0f},{y-54*s_:.0f}'
         f' L{x+20*s_:.0f},{y+54*s_:.0f} Z" fill="#8f979d" {o(6)}/>'
         f'<ellipse cx="{x-96*s_:.0f}" cy="{y:.0f}" rx="{14*s_:.0f}"'
         f' ry="{26*s_:.0f}" fill="#6f767c" {o(4)}/>'
         f'<ellipse cx="{x+16*s_:.0f}" cy="{y:.0f}" rx="{16*s_:.0f}"'
         f' ry="{56*s_:.0f}" fill="#b9c6cc" {o(5)}/>'
         f'<path d="M{x-60*s_:.0f},{y+30*s_:.0f} q{30*s_:.0f},{34*s_:.0f}'
         f' {66*s_:.0f},{18*s_:.0f}" fill="none" stroke="#7d5636"'
         f' stroke-width="{9*s_:.0f}"/>')
    s += (f'<path d="M{x-40*s_:.0f},{y-56*s_:.0f} q{60*s_:.0f},{-56*s_:.0f}'
          f' {120*s_:.0f},{-6*s_:.0f} q{6*s_:.0f},{30*s_:.0f}'
          f' {-50*s_:.0f},{34*s_:.0f} q{-54*s_:.0f},{4*s_:.0f}'
          f' {-70*s_:.0f},{-28*s_:.0f} Z" fill="#4a4036" {o(5)}/>'
          f'<path d="M{x+70*s_:.0f},{y-62*s_:.0f} q{54*s_:.0f},{6*s_:.0f}'
          f' {62*s_:.0f},{26*s_:.0f} q{-30*s_:.0f},{14*s_:.0f}'
          f' {-66*s_:.0f},{2*s_:.0f} Z" fill="#3d352c" {o(4)}/>'
          f'<circle cx="{x+20*s_:.0f}" cy="{y-84*s_:.0f}" r="{9*s_:.0f}"'
          f' fill="#5e5347" {o(3)}/>'
          f'<path d="M{x-24*s_:.0f},{y-70*s_:.0f} q{50*s_:.0f},{-26*s_:.0f}'
          f' {100*s_:.0f},{-10*s_:.0f}" fill="none" stroke="#6a5f52"'
          f' stroke-width="{7*s_:.0f}" opacity=".8"/>')
    return s


def _korobka_katushki(x, y, s_=1.0, t=0.0, perchatki=True):
    """Жестяная коробка с киноплёночной катушкой и пара белых перчаток:
    круглая банка с ободом, катушка с сердечником и витками плёнки, блик по
    ободу ходит."""
    r = 92 * s_
    bl = .3 + .5 * abs(A.w(t, 2.2, .2))
    s = (f'{ten(x, y + 10 * s_, r * .96, 14 * s_, .5)}'
         f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r*.30:.0f}"'
         f' fill="#8f979d" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-18*s_:.0f}" rx="{r:.0f}"'
         f' ry="{r*.30:.0f}" fill="#b9c6cc" {o(5)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-20*s_:.0f}" rx="{r*.86:.0f}"'
         f' ry="{r*.24:.0f}" fill="#9aa3aa" opacity=".9"/>')
    s += (f'<g transform="translate({r*.30:.0f},{-r*.52:.0f})">'
          f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r*.74:.0f}" ry="{r*.24:.0f}"'
          f' fill="#3d3a38" {o(5)}/>')
    for i in range(3):
        s += (f'<ellipse cx="{x:.0f}" cy="{y-i*7*s_:.0f}" rx="{r*(.70-i*.10):.0f}"'
              f' ry="{r*(.22-i*.03):.0f}" fill="none" stroke="#2a2726"'
              f' stroke-width="{max(2,4*s_):.0f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-24*s_:.0f}" rx="{r*.22:.0f}"'
          f' ry="{r*.08:.0f}" fill="#8f979d" {o(3)}/>'
          f'<path d="M{x-r*.62:.0f},{y-r*.10:.0f} q{r*.30:.0f},{-r*.16:.0f}'
          f' {r*.60:.0f},{-r*.02:.0f}" fill="none" stroke="#eef2f4"'
          f' stroke-width="{9*s_:.0f}" opacity="{bl:.2f}"/></g>')
    if perchatki:
        for i, (dx, ug) in enumerate(((-r * 1.10, -16), (-r * .64, 12))):
            s += (f'<g transform="rotate({ug:.0f} {x+dx:.0f} {y+r*.18:.0f})">'
                  f'<path d="M{x+dx-40*s_:.0f},{y+r*.18:.0f}'
                  f' q{6*s_:.0f},{-44*s_:.0f} {40*s_:.0f},{-46*s_:.0f}'
                  f' q{34*s_:.0f},{2*s_:.0f} {40*s_:.0f},{30*s_:.0f}'
                  f' q{4*s_:.0f},{18*s_:.0f} {-16*s_:.0f},{18*s_:.0f} Z"'
                  f' fill="#f4f8fa" {o(5)}/>'
                  f'<path d="M{x+dx-34*s_:.0f},{y+r*.10:.0f} q{34*s_:.0f},'
                  f'{-14*s_:.0f} {66*s_:.0f},{-2*s_:.0f}" fill="none"'
                  f' stroke="#cfd8dc" stroke-width="{6*s_:.0f}"/></g>')
    return s


def _ekran_kino(x, y, w_, h_, t, luch=.0):
    """Белый экран кинозала: полотно в рамке с заклёпками, по краям тёмные
    кулисы со складками, в середине слабое дежурное свечение."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="6" fill="#d8d2c4" {o(8)}/>'
         f'<rect x="{x+18:.0f}" y="{y+18:.0f}" width="{w_-36:.0f}"'
         f' height="{h_-36:.0f}" rx="4" fill="#e8e2d4"/>'
         f'<ellipse cx="{x+w_*.5:.0f}" cy="{y+h_*.5:.0f}" rx="{w_*.34:.0f}"'
         f' ry="{h_*.34:.0f}" fill="#f4f0e4" opacity="{.30+.30*luch:.2f}"/>')
    for i in range(14):
        s += (f'<circle cx="{x+20+i*(w_-40)/13.0:.0f}" cy="{y+9:.0f}" r="5"'
              f' fill="#9aa3aa"/>'
              f'<circle cx="{x+20+i*(w_-40)/13.0:.0f}" cy="{y+h_-9:.0f}" r="5"'
              f' fill="#9aa3aa"/>')
    for e, sg in ((x - 14, -1), (x + w_ + 14, 1)):
        for i in range(5):
            s += (f'<path d="M{e+sg*i*34:.0f},{y-30:.0f}'
                  f' q{sg*26:.0f},{h_*.5:.0f} {sg*4:.0f},{h_+40:.0f}'
                  f' l{sg*32:.0f},0 q{sg*20:.0f},{-h_*.5:.0f}'
                  f' {-sg*2:.0f},{-h_-40:.0f} Z" fill="#3a1e26"'
                  f' opacity="{.9-i*.09:.2f}" {o(3)}/>')
    return s


# ── ДЕКОРАЦИИ, ТРЕТЬЯ ПАРТИЯ ──────────────────────────────────────────────

def flyuger_na_sever(t):
    """Конёк крыши и кованый флюгер-петух крупно на ясном звёздном небе:
    флюгер разворачивается клювом на север. Хозяин в тулупе стоит на
    приставной лестнице, левой держится за тетиву, правой послюнявленным
    пальцем проверяет ветер. Внизу во дворе лужа схватывается льдом, бельё
    на верёвке деревенеет."""
    rnd = random.Random(701)
    gor = 860
    pov = A.ease(A.seg(t, .4, 1.8))
    led = A.ease(A.seg(t, 1.0, 2.2))
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 121)
    for i in range(16):
        bx, by_ = rnd.uniform(60, W - 60), rnd.uniform(40, 420)
        mig = .4 + .6 * abs(A.w(t, 1.1 + i * .07, i * .3))
        s += SL(Z_NEBO, f'<path d="M{bx:.0f},{by_-16:.0f} l{4:.0f},{12:.0f}'
                        f' l{12:.0f},{4:.0f} l{-12:.0f},{4:.0f} l{-4:.0f},{12:.0f}'
                        f' l{-4:.0f},{-12:.0f} l{-12:.0f},{-4:.0f} l{12:.0f},{-4:.0f} Z"'
                        f' fill="#e8eef6" opacity="{mig:.2f}"/>')
    s += SL(Z_DAL, _derevnya_ryad(gor - 120, t, 123, ((120, 300), (1740, 260))))
    # КОНЁК КРЫШИ и ГЛАВНЫЙ ПРЕДМЕТ: флюгер-петух
    # сруб ПОД коньком: крыша не висит в воздухе, а стоит на стене, и центр
    # кадра занят брёвнами, а не пустым небом (замер пустоты)
    s += SL(Z_SRED, brevna(540, 740, 860, gor - 700, 88)
            + f'<rect x="520" y="726" width="900" height="26" rx="9"'
              f' fill="#5a4530" {o(5)}/>')
    s += SL(Z_SRED, okno_izby(760, 790, 290, 200, t, None, .34, True, True))
    s += SL(Z_SRED, _konek_kryshi(560, 300, 820, t, 125, True))
    s += SL(Z_SRED, _flyuger_petuh(970, 290, 1.25, t, -34 + 112 * pov, True))
    # хозяин на приставной лестнице у крыши
    s += SL(Z_SRED, _lestnica(1360, gor + 40, 700, t, 6, 9.0))
    hx, hy, hh = 1300, gor - 290, 540
    _figury_kadra((hx, hy, hh))
    hoz = figura(hx, hy, hh, t, col="#4e4036", kant="#cfe4f5", ph=.3,
                 shapka=True, tulup=True, boroda=True, naklon=4.0)
    r1, (a1x, a1y), _ = _ruka_mimo(hx, hy, hh, 1, hh * .34, 28, t,
                                   "#4e4036", "#cfe4f5", .2, 4.0)
    r2, (a2x, a2y), _ = _ruka_so_sgibom(hx, hy, hh, -1, hh * .22, -22,
                                        hh * .20, -52, t, "#4e4036",
                                        "#cfe4f5", .7, 4.0)
    hoz += r1 + r2
    s += SL(Z_SRED, hoz)
    # варежка держит тетиву лестницы (перекрытие по стойке), второй кисти нет:
    # поднятый палец читается самим рукавом, пальцев мы не рисуем
    s += SL(Z_SRED, _varezhka(a1x, a1y + 2, hh, t, .2))
    s += SL(Z_SRED, f'<ellipse cx="{a2x:.0f}" cy="{a2y-22:.0f}" rx="12"'
                    f' ry="28" fill="#e8d8c0" {o(4)}/>')
    s += SL(Z_SRED, _strelka_vetra(a2x + 40, a2y - 30, 150, 14, t, "#4e8ad0", 3))
    s += SL(Z_SRED, para_izo_rta(hx + 32, hy - hh * .80, t, .4, 1.0, .55))
    # ДВОР ВНИЗУ: земля, лужа со льдом, бельё деревенеет
    s += SL(Z_SRED, f'<rect x="0" y="{gor+40:.0f}" width="{W}"'
                    f' height="{H-gor-40:.0f}" fill="#3f4238"/>'
            + sneg_lezhit(gor + 70, 26)
            + _zemlya_faktura(gor + 100, 1072, 127, 16, "#2f3228")
            + _inej(129, 26, gor + 90, 1070))
    s += SL(Z_SRED, _luzha_so_ldom(540, 1010, 230, t, led, .2))
    s += SL(Z_SRED, _bele_na_verevke(60, 740, 520, t, .25, 4, 131, led))
    s += SL(Z_SRED, _polenica(1620, 1040, 300, 200, 133, 26)
            + _sani(1120, 1046, .8, t, True)
            + _dvorovaya_utvar(820, 1046, 240, t, 135, ["kadka", "vedro"])
            + _sledy(300, 1070, 1180, gor + 110, 7, 137, "#2a2d24", 1.0))
    s += SL(Z_SRED, dym(220, gor - 260, t, 4, .26, 260, .3, "#8e9ab0", 1.3))
    s += SL(Z_SRED, _vorona(1700, gor - 180, t, .8, .3, .4))
    s += SL(Z_LETIT, _inej(139, 20, 300, 760))
    s += SL(Z_PERED, _stolb_pered(-8, 110, "#121018", 0, H))
    s += vinetka(.46)
    return s


def flyuger_na_yug(t):
    """Тот же флюгер-петух разворачивается клювом на юг, небо затягивает
    мягкими облаками. Хозяин внизу во дворе правой рукой снимает шапку,
    левой расстёгивает верхний крючок тулупа. Лёд на луже подтаивает, с
    крыши падает капля, воробьи купаются в луже."""
    rnd = random.Random(743)
    gor = 850
    pov = A.ease(A.seg(t, .3, 1.5))
    tay = A.ease(A.seg(t, .6, 1.6))
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 141)
    s += oblaka(t, 150, 7, 143, .56, "#d6dde4", 9.0)
    s += oblaka(t, 300, 5, 145, .44, "#c4cdd8", 13.0)
    s += SL(Z_DAL, _derevnya_ryad(gor - 110, t, 147, ((140, 320), (1720, 280))))
    s += SL(Z_SRED, brevna(440, 700, 960, gor - 660, 88)
            + f'<rect x="420" y="686" width="1000" height="26" rx="9"'
              f' fill="#5a4530" {o(5)}/>')
    s += SL(Z_SRED, okno_izby(700, 750, 300, 210, t, None, .10, True, True))
    # сарай справа с дворовым хозяйством на стене — вещи, а не пустое небо
    s += SL(Z_SRED, _stena_ambara(1460, 420, 460, 470, t, False, 163))
    s += SL(Z_SRED, _stennoe_hozyaystvo(1560, 520, t, 165))
    s += SL(Z_SRED, _konek_kryshi(440, 240, 980, t, 149, False))
    s += SL(Z_SRED, _flyuger_petuh(930, 230, 1.15, t, 146 - 128 * pov, True))
    # капля с крыши
    for i in range(3):
        kap = ((t * .8 + i / 3.0) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{620+i*180:.0f}"'
                        f' cy="{706+kap*260:.0f}" rx="8"'
                        f' ry="{13+7*kap:.0f}" fill="#9fc4d8"'
                        f' opacity="{(1-kap)*.9:.2f}"/>')
    # ДВОР: земля, лужа подтаивает, воробьи купаются
    s += SL(Z_SRED, f'<rect x="0" y="{gor+30:.0f}" width="{W}"'
                    f' height="{H-gor-30:.0f}" fill="#4a4a40"/>'
            + sneg_lezhit(gor + 60, 22)
            + _zemlya_faktura(gor + 96, 1072, 151, 16, "#3a3a30"))
    s += SL(Z_SRED, _luzha_so_ldom(1200, 1000, 260, t, 1.0 - tay, .3))
    for i, (bx, bs, bp) in enumerate(((1090, 1.3, .0), (1200, .68, .3),
                                      (1320, 1.1, .6))):
        s += SL(Z_SRED, ptica(bx, 960 - 30 * abs(A.w(t, 2.2, bp)), t, bs,
                              "#8a7a5c", bp, "#6b7a88"))
    s += SL(Z_SRED, _bele_na_verevke(60, 700, 480, t, 1.0, 4, 153, .0))
    # ОДНА ФИГУРА во дворе: снимает шапку, расстёгивает крючок
    hx, hy, hh = 620, 1018, 730
    _figury_kadra((hx, hy, hh))
    snim = A.ease(A.seg(t, .5, 1.1))
    hoz = figura(hx, hy, hh, t, col="#4e4036", kant="#cfe4f5", ph=.3,
                 tulup=True, boroda=True, naklon=4.0)
    r1, (b1x, b1y), _ = _ruka_so_sgibom(hx, hy, hh, 1, hh * .22, -30 - 20 * snim,
                                        hh * .20, -54, t, "#4e4036",
                                        "#cfe4f5", .2, 4.0)
    r2, (b2x, b2y), _ = _ruka_so_sgibom(hx, hy, hh, -1, hh * .20, -24,
                                        hh * .18, -44, t, "#4e4036",
                                        "#cfe4f5", .7, 4.0)
    hoz += r1 + r2
    s += SL(Z_SRED, hoz)
    # ШАПКА, снятая с головы: лежит в кисти, варежка перекрывает её околыш
    s += SL(Z_SRED, f'<g transform="rotate({-14 + 10 * snim:.1f} {b1x:.0f} {b1y:.0f})">'
                    f'<path d="M{b1x-54:.0f},{b1y+10:.0f} q{54:.0f},{-72:.0f}'
                    f' {108:.0f},0 q{-20:.0f},{26:.0f} {-108:.0f},0 Z"'
                    f' fill="#4a3f36" {o(5)}/>'
                    f'<ellipse cx="{b1x:.0f}" cy="{b1y+12:.0f}" rx="58"'
                    f' ry="20" fill="#cfc1a4" {o(4)}/></g>')
    s += SL(Z_SRED, _varezhka(b1x, b1y + 4, hh, t, .2))
    # РАССТЁГНУТЫЙ КРЮЧОК ворота: петля отходит в сторону
    s += SL(Z_SRED, f'<path d="M{hx-hh*.08:.0f},{hy-hh*.64:.0f}'
                    f' q{hh*.03:.0f},{hh*.03:.0f} {hh*.02+hh*.03*snim:.0f},'
                    f'{hh*.06:.0f}" fill="none" stroke="{ZHELEZ}"'
                    f' stroke-width="{hh*.012:.0f}"/>'
            + f'<path d="M{hx+hh*.04:.0f},{hy-hh*.64:.0f} q{hh*.02:.0f},'
              f'{hh*.03:.0f} {-hh*.01-hh*.03*snim:.0f},{hh*.06:.0f}"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="{hh*.012:.0f}"/>')
    s += SL(Z_SRED, _varezhka(b2x, b2y + 4, hh, t, .7))
    s += SL(Z_SRED, dym(240, gor - 240, t, 5, .30, 300, .34, "#cfd6de", 1.6))
    s += SL(Z_SRED, _polenica(80, 1046, 320, 200, 155, 26)
            + _dvorovaya_utvar(1600, 1046, 260, t, 157, ["kadka", "vedro"])
            + _kucha_listev(900, 1052, 300, 159, 74)
            + _sani(1700, 1040, .76, t, False))
    s += SL(Z_SRED, _kot_zhivoy(400, 1040, t, 1.1, "#4a4440", .3))
    s += SL(Z_PERED, _vetka_pered(1960, 160, 560, 156, t, 161, "#2a2318", 6))
    s += vinetka(.42)
    return s


def luna_v_dymke_nad_kolodcem(t):
    """Ночной двор: колодец с воротом крупно, в небе круглая луна в мутном
    кольце. В тёмном проёме колодезного сруба, как в зеркале, стоит настоящая
    луна в дымке. Бабка в шали обеими руками держит ворот, смотрит то на
    небо, то в колодец и качает головой. У колодца ведро, коромысло, кот на
    срубе, рядом поленница под рогожей."""
    rnd = random.Random(769)
    gor = 760
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 167)
    s += oblaka(t, 180, 5, 169, .32, "#6f7f8c", 16.0)
    # ЛУНА В МУТНОМ КОЛЬЦЕ — мерцает
    mig = .78 + .18 * abs(A.w(t, 1.3, .2))
    s += SL(Z_NEBO, f'<circle cx="1480" cy="190" r="200" fill="#8e9ab0"'
                    f' opacity="{.16*mig:.2f}"/>'
            + f'<circle cx="1480" cy="190" r="140" fill="#cfe4f5"'
              f' opacity="{.22*mig:.2f}"/>'
            + f'<circle cx="1480" cy="190" r="92" fill="#e8eef6"'
              f' opacity="{mig:.2f}"/>'
            + f'<circle cx="1510" cy="164" r="20" fill="#cfd6de" opacity=".5"/>'
            + f'<circle cx="1452" cy="212" r="14" fill="#cfd6de" opacity=".45"/>'
            + f'<circle cx="1480" cy="190" r="168" fill="none" stroke="#cfe4f5"'
              f' stroke-width="9" opacity="{.26*mig:.2f}"/>')
    s += SL(Z_DAL, _derevnya_ryad(gor - 150, t, 171, ((140, 300), (1760, 250))))
    s += SL(Z_DAL, _zabor_dosok(-30, gor - 200, 1010, 200, 173, 54))
    s += SL(Z_DAL, goloe_derevo(1700, gor + 20, 480, t, 175, 8, "#2f3038", True))
    s += SL(Z_SRED, f'<rect x="0" y="{gor+20:.0f}" width="{W}"'
                    f' height="{H-gor-20:.0f}" fill="#2f3228"/>'
            + sneg_lezhit(gor + 50, 24)
            + _zemlya_faktura(gor + 90, 1072, 177, 16, "#262a22"))
    # ГЛАВНЫЙ ПРЕДМЕТ: колодец, в его срубе — проём под настоящий кадр
    s += SL(Z_SRED, _kolodec(560, gor + 170, 660, t, 330, True))
    px, py, pw, ph_ = 580, gor - 148, 620, 300
    # проём колодца узок по срубу, поэтому кадр ставим в ПЛОСКОСТИ воды:
    # широкий прямоугольник по горлу сруба, гейт требует от 760 px
    px, py, pw, ph_ = 500, gor - 142, 780, 310
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<path d="{put}" fill="#101620"/>'
           f'<ellipse cx="{px+pw*.5:.0f}" cy="{py+ph_*.5:.0f}"'
           f' rx="{pw*.34:.0f}" ry="{ph_*.30:.0f}" fill="#2b3550" opacity=".9"/>'
           f'<ellipse cx="{px+pw*.5:.0f}" cy="{py+ph_*.48:.0f}"'
           f' rx="{pw*.17:.0f}" ry="{ph_*.15:.0f}" fill="#cfe4f5"'
           f' opacity="{.5+.3*abs(A.w(t,1.7,.3)):.2f}"/>')
    for i in range(4):
        vid += (f'<path d="M{px+60:.0f},{py+ph_*(.30+i*.16):.0f}'
                f' q{pw*.24:.0f},{-10 - 8 * A.w(t, 1.9, i * .3):.0f}'
                f' {pw*.46:.0f},0 q{pw*.22:.0f},{10:.0f} {pw*.42:.0f},{-4:.0f}"'
                f' fill="none" stroke="#9fc4d8" stroke-width="7" opacity=".5"/>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#4e3c2c"'
                    f' stroke-width="34"/>'
            + f'<rect x="{px-24:.0f}" y="{py-34:.0f}" width="{pw+48:.0f}"'
              f' height="40" rx="14" fill="{BREVNO}" {o(6)}/>'
            + f'<rect x="{px-24:.0f}" y="{py+ph_-8:.0f}" width="{pw+48:.0f}"'
              f' height="36" rx="14" fill="{BREVNO2}" {o(6)}/>')
    # ведро, коромысло, кот на срубе
    s += SL(Z_SRED, _koromyslo(1480, gor + 40, 1.0, t, True))
    s += SL(Z_SRED, _kot_zhivoy(1180, py - 40, t, 1.15, "#2f2a26", .3))
    # ОДНА ФИГУРА: бабка в шали, ОБЕ руки на вороте
    bx, by_, bh = 1400, gor + 250, 700
    _figury_kadra((bx, by_, bh))
    kach = A.w(t, 1.2, .2)
    bab = figura(bx, by_, bh, t, col="#54505e", kant="#cfe4f5", platok=True,
                 ph=.4, naklon=6.0)
    r1, (c1x, c1y), _ = _ruka_mimo(bx, by_, bh, -1, bh * .40, -12 + 8 * kach, t,
                                   "#54505e", "#cfe4f5", .2, 5.0)
    r2, (c2x, c2y), _ = _ruka_sgib_mimo(bx, by_, bh, -1, bh * .24, 10,
                                        bh * .24, -22, t, "#54505e",
                                        "#cfe4f5", .7, 4.0)
    bab += r1 + r2
    s += SL(Z_SRED, bab)
    # ШАЛЬ поверх платка — бахрома по плечам, узел на груди
    s += SL(Z_SRED, f'<path d="M{bx-bh*.17:.0f},{by_-bh*.62:.0f}'
                    f' q{bh*.17:.0f},{-bh*.05:.0f} {bh*.34:.0f},0'
                    f' L{bx+bh*.10:.0f},{by_-bh*.34:.0f}'
                    f' L{bx-bh*.10:.0f},{by_-bh*.34:.0f} Z" fill="#8a4a5c"'
                    f' {o(5)}/>'
            + "".join(f'<line x1="{bx-bh*.09+i*bh*.03:.0f}"'
                      f' y1="{by_-bh*.34:.0f}" x2="{bx-bh*.095+i*bh*.03:.0f}"'
                      f' y2="{by_-bh*.30:.0f}" stroke="#8a4a5c"'
                      f' stroke-width="{bh*.009:.0f}"/>' for i in range(7)))
    s += SL(Z_SRED, _varezhka(c1x, c1y + 2, bh, t, .2)
            + _varezhka(c2x, c2y + 2, bh, t, .7))
    s += SL(Z_SRED, para_izo_rta(bx - 40, by_ - bh * .80, t, .3, 1.0, .5))
    # поленница под рогожей, которую она идёт накрывать
    s += SL(Z_SRED, _polenica(120, 1040, 400, 220, 179, 27))
    s += SL(Z_SRED, _rogozha(110, 854, 420, t, 130, 181))
    s += SL(Z_SRED, _dvorovaya_utvar(760, 1046, 280, t, 183, ["vedro", "kadka"])
            + _sledy(1700, 1070, 1320, gor + 110, 7, 185, "#1f231c", 1.0)
            + _kucha_listev(1060, 1050, 280, 187, 72))
    s += SL(Z_SRED, dym(300, gor - 240, t, 4, .26, 260, .3, "#8e9ab0", 1.4))
    s += SL(Z_SRED, luchina(1240, py - 86, t, 1.0, .4)
            + teplo(1240, py - 120, 240, 200, .34))
    s += SL(Z_LETIT, tuman(t, 900, .34, "#9fb0bc"))
    s += SL(Z_PERED, _stolb_pered(1892, 118, "#10141a", 0, H))
    s += vinetka(.48)
    return s


def listki_chislennika_pod_zontom(t):
    """Стена сеней: отрывной численник крупно, на гвозде рядом мокрый зонт и
    плащ, под ними калоши в лужице. Дед в мокрой кепке правой рукой отгибает
    листки один за другим — на каждом тучка с каплями, — левой выжимает
    кепку над калошами."""
    rnd = random.Random(787)
    pol = 1012
    s = f'<rect width="{W}" height="{H}" fill="#282018"/>'
    s += SL(Z_DAL, doski(0, 0, 1920, pol, 72, True, "dosk"))
    for i in range(13):
        s += SL(Z_DAL, f'<line x1="{30+i*150:.0f}" y1="0" x2="{30+i*150:.0f}"'
                       f' y2="{pol:.0f}" stroke="#5b4428" stroke-width="7"'
                       f' opacity=".7"/>')
    s += SL(Z_DAL, _polka_s_utvaryu(1520, 170, 380, t, 189, 4)
            + _polka_s_utvaryu(60, 150, 420, t, 199, 4))
    # стенное хозяйство и лавка сеней: без них левый простенок стоит голым
    s += SL(Z_SRED, f'<rect x="120" y="226" width="1080" height="40" rx="12"'
                    f' fill="#6b5340" {o(7)}/>'
            + "".join(f'<path d="M{200+i*150:.0f},266 q{10:.0f},{26:.0f}'
                      f' {-14:.0f},{38:.0f}" fill="none" stroke="{ZHELEZ}"'
                      f' stroke-width="9"/>' for i in range(7)))
    s += SL(Z_SRED, _stennoe_hozyaystvo(300, 420, t, 201))
    s += SL(Z_SRED, _lavka_krupno(260, 1012, 420, t, 170, False))
    s += SL(Z_SRED, _venik(170, 1008, 330, t, "#b8a86a", "#5a4a2e", True,
                           .12, .2, .92, 203))
    s += SL(Z_DAL, tusklaya_lampochka(300, 30, t, .95, False))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#5a4a3a"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1074, 191, 6, "#463828"))
    # ГЛАВНЫЙ ПРЕДМЕТ: отрывной численник, листки отгибаются с тучками
    otgib = A.ease(A.seg(t, .4, 2.4))
    s += SL(Z_SRED, _chislennik(520, 250, 360, 480, t, .0))
    s += SL(Z_SRED, _listki_tuchki(700, 330, 300, t, otgib, 6, 193))
    # зонт, плащ, калоши в лужице
    s += SL(Z_SRED, _plasch_na_gvozde(1240, 230, 480, t, .3, "#4e5a46"))
    s += SL(Z_SRED, _zont_mokryy(1530, 240, t, 1.0, .2))
    s += SL(Z_SRED, _kaloshi(1380, pol + 10, 1.1, t, True))
    # ОДНА ФИГУРА: дед в мокрой кепке
    dx_, dy_, dh = 1080, pol, 740
    _figury_kadra((dx_, dy_, dh))
    vyzh = A.w(t, 1.6, .2)
    ded = figura(dx_, dy_, dh, t, col="#4e4a44", kant="#cfe4f5", ph=.3,
                 boroda=True, naklon=4.0)
    r1, (e1x, e1y), _ = _ruka_mimo(dx_, dy_, dh, -1, dh * .44,
                                   -26 + 28 * otgib, t, "#4e4a44",
                                   "#cfe4f5", .2, 5.0)
    r2, (e2x, e2y), _ = _ruka_so_sgibom(dx_, dy_, dh, 1, dh * .22, 24,
                                        dh * .24, 56, t, "#4e4a44",
                                        "#cfe4f5", .7, 4.0)
    ded += r1 + r2
    s += SL(Z_SRED, ded)
    # МОКРАЯ КЕПКА, которую он выжимает: лежит в кисти, из неё текут капли
    gy_ = dy_ - dh * .845
    s += SL(Z_SRED, f'<path d="M{dx_-dh*.10:.0f},{gy_-dh*.09:.0f}'
                    f' q{dh*.10:.0f},{-dh*.07:.0f} {dh*.20:.0f},{-dh*.01:.0f}'
                    f' q{-dh*.02:.0f},{dh*.035:.0f} {-dh*.20:.0f},{dh*.008:.0f} Z"'
                    f' fill="#5e5a52" {o(5)}/>')
    s += SL(Z_SRED, f'<g transform="rotate({16 + 10 * vyzh:.1f} {e2x:.0f} {e2y:.0f})">'
                    f'<path d="M{e2x-50:.0f},{e2y+6:.0f} q{50:.0f},{-56:.0f}'
                    f' {100:.0f},{-6:.0f} q{-16:.0f},{30:.0f} {-100:.0f},{6:.0f} Z"'
                    f' fill="#5e5a52" {o(5)}/>'
                    f'<path d="M{e2x+38:.0f},{e2y:.0f} q{34:.0f},{4:.0f}'
                    f' {40:.0f},{18:.0f} q{-22:.0f},{10:.0f} {-46:.0f},{2:.0f} Z"'
                    f' fill="#4e4a44" {o(4)}/></g>')
    s += SL(Z_SRED, _varezhka(e2x, e2y + 4, dh, t, .7))
    for i in range(5):
        kap = ((t * 1.1 + i / 5.0) % 1.0)
        s += SL(Z_LETIT, f'<ellipse cx="{e2x-20+i*20:.0f}"'
                         f' cy="{e2y+40+kap*(pol-e2y-30):.0f}" rx="6"'
                         f' ry="{10+5*kap:.0f}" fill="#9fc4d8"'
                         f' opacity="{(1-kap)*.9:.2f}"/>')
    # варежки на отгибающей кисти НЕТ: листок тонкий, перекрытия не даёт
    s += SL(Z_SRED, f'<path d="M{e1x-20:.0f},{e1y-14:.0f} q{24:.0f},{-12:.0f}'
                    f' {44:.0f},{6:.0f}" fill="none" stroke="#cfe4f5"'
                    f' stroke-width="7" opacity=".3"/>')
    # нижняя треть
    s += SL(Z_SRED, _polovik(700, pol + 42, 500, 110, "#cdbf9c", "#b8352c")
            + _valenki_u_dveri(240, pol + 38, 1.1, t)
            + _dvorovaya_utvar(1700, pol + 50, 210, t, 195, ["vedro"])
            + _yaschiki(160, pol + 14, t, 197, 2, .9)
            + _kot_zhivoy(900, pol + 52, t, 1.05, "#3b3430", .4))
    s += SL(Z_SRED, _luzha(1380, pol + 60, 200, t, .3))
    s += SL(Z_SRED, teplo(300, 140, 320, 240, .28))
    s += SL(Z_PERED, _stolb_pered(-8, 116, "#171107", 0, H))
    s += vinetka(.44)
    return s


def mokryy_palec_na_vetru(t):
    """Балкон городской квартиры: перила, ящик с засохшими бархатцами,
    табурет, прищепки на верёвке. Мужчина в домашней куртке держит
    послюнявленный палец вверх над головой, левой держится за перила. С
    одной стороны палец холодеет — на ней синяя стрелка ветра, шарф
    отлетает в ту же сторону."""
    rnd = random.Random(809)
    plita = 1010
    s = f'<rect width="{W}" height="{H}" fill="#39424a"/>'
    s += nebo("sumer", t, False, 205)
    s += oblaka(t, 170, 6, 207, .42, "#c4cdd8", 11.0)
    # двор за перилами: панельные дома и дальние балконы
    s += SL(Z_DAL, panelka(60, 760, 620, t, 5, True, 209)
            + panelka(1320, 740, 580, t, 5, True, 211))
    s += SL(Z_DAL, _balkon_plita(180, 560, 300, t, 36, 2)
            + _balkon_plita(1480, 530, 290, t, 36, 2))
    s += SL(Z_DAL, _bele_na_verevke(200, 430, 260, t, 1.0, 2, 213, .0)
            + _bele_na_verevke(1500, 400, 250, t, 1.0, 2, 215, .0))
    # стена квартиры и балконная плита
    s += SL(Z_SRED, f'<rect x="0" y="0" width="420" height="{H}"'
                    f' fill="{BETON2}" {o(6)}/>'
            + _kafel(0, 120, 400, 560, t, 217, "#b0bcc0", "#8a9298"))
    s += SL(Z_SRED, dver(60, 230, 300, 740, .18, "#cfd8dc", True, False))
    s += SL(Z_SRED, tusklaya_lampochka(220, 60, t, .9, False))
    s += SL(Z_SRED, f'<rect x="0" y="{plita:.0f}" width="{W}" height="{H-plita:.0f}"'
                    f' fill="#8a9298"/>' + _asfalt(plita - 6, 1076, 219, 10))
    # ПЕРИЛА БАЛКОНА — главная конструкция плана
    s += SL(Z_SRED, _perila_balkona(420, plita, 1500, t, 210, True))
    s += SL(Z_SRED, _yaschik_barhatcev(470, plita - 6, 340, t, 221))
    s += SL(Z_SRED, _tabyret(980, plita - 4, t, 160, 180))
    s += SL(Z_SRED, _prischepki(620, 300, 900, t, 7, 223))
    s += SL(Z_SRED, _gorodskoy_hlam(1700, plita - 6, 200, t, 225,
                                    ["yaschik", "korobka"]))
    # ОДНА ФИГУРА: правая рука с поднятым пальцем, левая на перилах
    mx, my, mh = 1240, plita - 6, 780
    _figury_kadra((mx, my, mh))
    pod = A.ease(A.seg(t, .25, .9))
    muzh = figura(mx, my, mh, t, col="#3f5c7a", kant="#cfe4f5", ph=.3,
                  naklon=3.0)
    r1, (f1x, f1y), _ = _ruka_so_sgibom(mx, my, mh, 1, mh * .22,
                                        -30 - 24 * pod, mh * .22, -56, t,
                                        "#3f5c7a", "#cfe4f5", .2, 3.0)
    r2, (f2x, f2y), _ = _ruka_mimo(mx, my, mh, -1, mh * .38, 46, t,
                                   "#3f5c7a", "#cfe4f5", .7, 4.0)
    muzh += r1 + r2
    s += SL(Z_SRED, muzh)
    # ПАЛЕЦ ВВЕРХ: кисть рукавом, на конце узкий овал — пальцев не рисуем,
    # жест читается вертикалью и стрелкой ветра рядом
    s += SL(Z_SRED, f'<ellipse cx="{f1x:.0f}" cy="{f1y-30:.0f}" rx="14"'
                    f' ry="{34+10*pod:.0f}" fill="#e8d8c0" {o(4)}/>'
            + f'<ellipse cx="{f1x-5:.0f}" cy="{f1y-54-8*pod:.0f}" rx="7"'
              f' ry="12" fill="#cfe4f5" opacity=".55"/>')
    # СИНЯЯ СТРЕЛКА ветра ложится на холодеющую сторону пальца
    s += SL(Z_SRED, _strelka_vetra(f1x + 36, f1y - 36, 210, 8, t, "#4e8ad0", 3))
    s += SL(Z_SRED, f'<path d="M{f1x+8:.0f},{f1y-62:.0f} q{10:.0f},{30:.0f}'
                    f' {2:.0f},{58:.0f}" fill="none" stroke="#4e8ad0"'
                    f' stroke-width="9" opacity=".7"/>')
    # ШАРФ отлетает в ту же сторону
    s += SL(Z_SRED, _sharf_otletaet(mx + 26, my - mh * .66, 330, t, 0.0, TKAN))
    s += SL(Z_SRED, _varezhka(f2x, f2y + 2, mh, t, .7))
    s += SL(Z_SRED, para_izo_rta(mx + 40, my - mh * .80, t, .4, 1.1, .55))
    # нижняя треть
    s += SL(Z_SRED, _kucha_listev(760, plita + 46, 300, 227, 66)
            + _luzha(1460, plita + 52, 190, t, .3)
            + _dvorovaya_utvar(560, plita + 48, 200, t, 229, ["vedro"])
            + _kot_zhivoy(1060, plita + 46, t, 1.05, "#4a4440", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 26, 231, .5, 1.6))
    s += SL(Z_PERED, _stolb_pered(1894, 104, "#20262a", 0, H))
    s += vinetka(.42)
    return s


def dym_nad_pechnoy_truboy(t):
    """Двор частного дома: крыша с кирпичной трубой, чердачное окно-проём
    крупно показывает настоящий дым из трубы на ветру. Хозяйка в пуховом
    платке приложила правую ладонь козырьком ко лбу, в левой держит миску с
    зерном, смотрит на дым и кивает. Куры клюют у её ног, пёс лежит у
    будки."""
    rnd = random.Random(821)
    gor = 880
    s = f'<rect width="{W}" height="{H}" fill="url(#nden)"/>'
    s += nebo("den", t, False, 233)
    s += oblaka(t, 150, 6, 235, .46, "#c4cdd8", 12.0)
    s += SL(Z_DAL, _derevnya_ryad(gor - 140, t, 237, ((130, 280), (1800, 250))))
    s += SL(Z_DAL, _zabor_dosok(-30, gor - 180, 480, 170, 239, 54))
    # ДОМ: сруб, крыша, кирпичная труба с дымом
    s += SL(Z_SRED, brevna(360, 520, 1200, gor - 480, 92)
            + f'<rect x="340" y="506" width="1240" height="28" rx="9"'
              f' fill="#5a4530" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M300,520 L960,250 L1620,520 Z" fill="#6b5340"'
                    f' {o(8)}/>'
            + f'<path d="M300,520 L960,250 L960,286 L360,524 Z" fill="{SNEG}"'
              f' opacity=".88"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<line x1="{320+i*110:.0f}" y1="518" x2="960"'
                        f' y2="254" stroke="#4e3c2c" stroke-width="6"'
                        f' opacity=".6"/>')
    s += SL(Z_SRED, f'<rect x="1230" y="150" width="130" height="200" rx="8"'
                    f' fill="{KAMEN}" {o(6)}/>' + kladka(1230, 150, 130, 200, 40, KAMEN)
            + f'<rect x="1206" y="128" width="178" height="32" rx="9"'
              f' fill="{KAMEN2}" {o(5)}/>')
    s += SL(Z_SRED, f'<g transform="rotate(54 1295 120)">'
                    + dym(1295, 120, t, 6, .34, 420, .42, "#cfd6de", 2.0)
                    + "</g>")
    # НАСТОЯЩИЙ КАДР в чердачном окне: вид, метка, наличник и переплёт поверх
    px, py, pw, ph_ = 580, 330, 780, 320
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<path d="{put}" fill="#4a5a68"/>'
           + _vid_za_proemom(put, t, "nebo", 241, px + pw * .5))
    for i in range(4):
        vid += (f'<path d="M{px+90+i*60:.0f},{py+ph_*.80:.0f}'
                f' q{90:.0f},{-80 - 20 * A.w(t, 1.6, i * .3):.0f}'
                f' {220:.0f},{-120:.0f}" fill="none" stroke="#cfd6de"'
                f' stroke-width="{22-i*4:.0f}" opacity=".5"/>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#5f4a34"'
                    f' stroke-width="32"/>'
            + f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#5f4a34" stroke-width="22"/>'
            + f'<rect x="{px-46:.0f}" y="{py-48:.0f}" width="{pw+92:.0f}"'
              f' height="42" rx="12" fill="#7d5a3c" {o(5)}/>'
            + f'<rect x="{px-34:.0f}" y="{py+ph_-10:.0f}" width="{pw+68:.0f}"'
              f' height="40" rx="12" fill="url(#dosk)" {o(6)}/>'
            + f'<path d="M{px-46:.0f},{py-48:.0f} l{-28:.0f},{-30:.0f}'
              f' l{pw+148:.0f},0 l{-28:.0f},{30:.0f} Z" fill="#6b5340" {o(5)}/>')
    # ДВОР: земля, будка с псом, куры
    s += SL(Z_SRED, f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor:.0f}"'
                    f' fill="#55564e"/>' + sneg_lezhit(gor + 30, 24)
            + _zemlya_faktura(gor + 70, 1072, 243, 16, "#43443c"))
    s += SL(Z_SRED, _buda_s_psom(1560, 1040, .92, t, .3))
    for i, (kx, ks, kp) in enumerate(((760, 1.45, .0), (900, .74, .3),
                                      (1030, 1.25, .6), (1150, .66, .85))):
        s += SL(Z_SRED, kura(kx, 1040 - i * 6, t, ks, kp, "#e2d6c2", True))
    # ОДНА ФИГУРА: хозяйка в пуховом платке
    hx, hy, hh = 420, 1018, 760
    _figury_kadra((hx, hy, hh))
    kiv = A.w(t, 1.3, .2)
    hoz = figura(hx, hy, hh, t, col="#8a4a5c", kant="#cfe4f5", platok=True,
                 ph=.3, naklon=3.0 + 2.0 * kiv)
    r1, (g1x, g1y), _ = _ruka_so_sgibom(hx, hy, hh, 1, hh * .22, -34,
                                        hh * .18, -56, t, "#8a4a5c",
                                        "#cfe4f5", .2, 3.0)
    r2, (g2x, g2y), _ = _ruka_mimo(hx, hy, hh, -1, hh * .34, 50, t,
                                   "#8a4a5c", "#cfe4f5", .7, 4.0)
    hoz += r1 + r2
    s += SL(Z_SRED, hoz)
    # ЛАДОНЬ КОЗЫРЬКОМ у лба: горизонтальная накладка от кисти, лицо открыто
    s += SL(Z_SRED, f'<path d="M{g1x-14:.0f},{g1y:.0f} q{40:.0f},{-20:.0f}'
                    f' {76:.0f},{-4:.0f} q{-6:.0f},{20:.0f} {-76:.0f},{16:.0f} Z"'
                    f' fill="#e8d8c0" {o(4)}/>')
    # ПУХОВЫЙ ПЛАТОК: пушистая кромка поверх убора
    gy_ = hy - hh * .845
    s += SL(Z_SRED, "".join(
        f'<circle cx="{hx+math.cos(math.radians(a)) * hh * .165:.0f}"'
        f' cy="{gy_+math.sin(math.radians(a)) * hh * .165:.0f}"'
        f' r="{hh*.022:.0f}" fill="#e8e2d6" opacity=".9"/>'
        for a in range(150, 391, 24)))
    # МИСКА С ЗЕРНОМ в левой кисти, варежка перекрывает борт
    s += SL(Z_SRED, _miska_zerna(g2x - 36, g2y + 64, .92, t, .3))
    s += SL(Z_SRED, _varezhka(g2x, g2y + 4, hh, t, .7))
    s += SL(Z_SRED, para_izo_rta(hx + 38, gy_ + 14, t, .5, 1.0, .5))
    # нижняя треть
    s += SL(Z_SRED, _polenica(80, 1046, 300, 200, 245, 26)
            + _dvorovaya_utvar(620, 1046, 240, t, 247, ["kadka", "vedro"])
            + _sani(1300, 1042, .74, t, True)
            + _sledy(240, 1070, 760, gor + 90, 7, 249, "#3a3b33", 1.0))
    s += SL(Z_SRED, teplo(1295, 200, 360, 300, .26))
    s += SL(Z_PERED, _vetka_pered(-40, 150, 540, 24, t, 251, "#2a2318", 6))
    s += vinetka(.42)
    return s


def bele_na_balkonnoy_verevke(t):
    """Двор-колодец из панельных стен: балкон крупно, верёвки. В проёме
    балконной двери — настоящий кадр, где бельё полощется на ветру. Женщина
    в халате левой рукой держит таз у бедра, правой прищепляет наволочку.
    Наволочку и халат относит в одну сторону, на соседних балконах бельё
    летит туда же."""
    rnd = random.Random(853)
    plita = 1004
    s = f'<rect width="{W}" height="{H}" fill="#4a535a"/>'
    s += nebo("den", t, False, 253)
    # ДВОР-КОЛОДЕЦ: панельные стены по трём сторонам
    s += SL(Z_DAL, panelka(-40, 820, 560, t, 6, True, 255)
            + panelka(1420, 800, 560, t, 6, True, 257))
    s += SL(Z_DAL, panelka(500, 560, 420, t, 4, True, 259)
            + panelka(940, 560, 420, t, 4, True, 261))
    # соседние балконы: бельё летит в ту же сторону
    for i, (bx, by_, bw) in enumerate(((120, 520, 320), (1500, 490, 300),
                                       (640, 330, 280), (1060, 300, 280))):
        s += SL(Z_DAL, _balkon_plita(bx, by_, bw, t, 34, 2))
        s += SL(Z_DAL, _bele_na_verevke(bx + 20, by_ - 130, bw - 40, t, 1.0,
                                        2, 263 + i * 2, .0))
    # СТЕНА КВАРТИРЫ и проём балконной двери с настоящим кадром
    s += SL(Z_SRED, f'<rect x="0" y="0" width="520" height="{H}"'
                    f' fill="{BETON2}" {o(6)}/>'
            + _kafel(0, 100, 500, 620, t, 271, "#b0bcc0", "#8a9298"))
    px, py, pw, ph_ = 60, 190, 780, 700
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<path d="{put}" fill="#5e6a72"/>'
           + _vid_za_proemom(put, t, "dvor", 273, px + pw * .5))
    for i in range(3):
        sn = 30 * A.w(t, 1.5, i * .3)
        vid += (f'<path d="M{px+90+i*220:.0f},{py+120:.0f}'
                f' q{40+sn:.0f},{ph_*.3:.0f} {18+sn:.0f},{ph_*.56:.0f}'
                f' q{-40:.0f},{30:.0f} {-110:.0f},{10:.0f}'
                f' q{-10:.0f},{-ph_*.3:.0f} {18:.0f},{-ph_*.56:.0f} Z"'
                f' fill="#f4eedc" opacity=".92" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#cfd8dc"'
                    f' stroke-width="34"/>'
            + f'<line x1="{px+pw*.52:.0f}" y1="{py:.0f}" x2="{px+pw*.52:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#cfd8dc" stroke-width="26"/>'
            + f'<line x1="{px:.0f}" y1="{py+ph_*.30:.0f}" x2="{px+pw:.0f}"'
              f' y2="{py+ph_*.30:.0f}" stroke="#cfd8dc" stroke-width="20"/>'
            + f'<circle cx="{px+pw*.52+40:.0f}" cy="{py+ph_*.56:.0f}" r="16"'
              f' fill="#9aa3aa" {o(4)}/>'
            + f'<path d="M{px+120:.0f},{py+ph_*.18:.0f} L{px+pw*.42:.0f},'
              f'{py+70:.0f}" fill="none" stroke="#ffffff" stroke-width="14"'
              f' opacity="{.14+.10*abs(A.w(t,3.0,.2)):.2f}"/>')
    # БАЛКОН: плита, перила, верёвки
    s += SL(Z_SRED, f'<rect x="0" y="{plita:.0f}" width="{W}" height="{H-plita:.0f}"'
                    f' fill="{BETON}"/>' + _asfalt(plita - 4, 1076, 275, 8))
    s += SL(Z_SRED, _perila_balkona(560, plita, 1340, t, 220, True))
    s += SL(Z_SRED, _prischepki(620, 300, 1200, t, 8, 277))
    s += SL(Z_SRED, _bele_na_verevke(640, 316, 560, t, 1.0, 3, 279, .0))
    s += SL(Z_SRED, _yaschik_barhatcev(1640, plita - 6, 250, t, 281))
    # ОДНА ФИГУРА: левая держит таз у бедра, правая прищепляет наволочку
    zx, zy, zh = 1180, plita - 6, 780
    _figury_kadra((zx, zy, zh))
    prisch = A.ease(A.seg(t, .5, 1.3))
    zhen = figura(zx, zy, zh, t, col="#b8323a", kant="#cfe4f5", ph=.3,
                  naklon=4.0)
    r1, (h1x, h1y), _ = _ruka_so_sgibom(zx, zy, zh, 1, zh * .22,
                                        -34 - 16 * prisch, zh * .20, -58, t,
                                        "#b8323a", "#cfe4f5", .2, 4.0)
    r2, (h2x, h2y), _ = _ruka_mimo(zx, zy, zh, -1, zh * .30, 44, t,
                                   "#b8323a", "#cfe4f5", .7, 4.0)
    zhen += r1 + r2
    s += SL(Z_SRED, zhen)
    # ХАЛАТ относит в ту же сторону, что и бельё
    sn = 26 + 18 * A.w(t, 1.5, .2)
    s += SL(Z_SRED, f'<path d="M{zx-zh*.14:.0f},{zy-zh*.60:.0f}'
                    f' q{zh*.14:.0f},{-zh*.04:.0f} {zh*.28:.0f},0'
                    f' L{zx+zh*.20+sn:.0f},{zy-zh*.10:.0f}'
                    f' L{zx-zh*.14+sn*.4:.0f},{zy-zh*.10:.0f} Z"'
                    f' fill="#d9444c" {o(5)}/>'
            + f'<path d="M{zx-zh*.15:.0f},{zy-zh*.38:.0f} q{zh*.15:.0f},'
              f'{zh*.03:.0f} {zh*.30:.0f},0" fill="none" stroke="{TKAN2}"'
              f' stroke-width="{zh*.018:.0f}"/>')
    # НАВОЛОЧКА парусом — ровно в кисти, прищепка поверх
    s += SL(Z_SRED, _navolochka_parus(h1x - 20, h1y + 10, 230, t,
                                      .5 + .5 * prisch, "#f4eedc"))
    s += SL(Z_SRED, f'<rect x="{h1x-30:.0f}" y="{h1y-10:.0f}" width="22"'
                    f' height="56" rx="7" fill="#c9a47a" {o(4)}/>')
    s += SL(Z_SRED, _varezhka(h1x, h1y + 4, zh, t, .2))
    # ТАЗ У БЕДРА в левой кисти
    s += SL(Z_SRED, _taz_i_svertok(h2x - 40, h2y + 70, .72, t, -14))
    s += SL(Z_SRED, _varezhka(h2x, h2y + 6, zh, t, .7))
    # нижняя треть
    s += SL(Z_SRED, _gorodskoy_hlam(620, plita + 46, 280, t, 283,
                                    ["yaschik", "paket"])
            + _kucha_listev(980, plita + 50, 280, 285, 64)
            + _luzha(1500, plita + 54, 200, t, .3)
            + _kot_zhivoy(1300, plita + 46, t, 1.05, "#4a4440", .4))
    s += SL(Z_SRED, tusklaya_lampochka(300, 70, t, .9, False))
    s += SL(Z_LETIT, mokryy_sneg(t, 24, 287, .44, 1.8))
    s += SL(Z_PERED, _stolb_pered(1896, 108, "#20262a", 0, H))
    s += vinetka(.42)
    return s


def kinozal_i_dva_kresla(t):
    """Старый кинозал: ряды бархатных кресел, белый экран, из окошка будки
    бьёт тёплый луч. В первом ряду два кресла крупно — на левом режиссёрская
    кепка на рупоре, на правом жестяная коробка с катушкой и пара белых
    перчаток. Людей нет, луч скользит с одного кресла на другое, в нём
    пляшут пылинки."""
    rnd = random.Random(877)
    pol = 1010
    sk = A.ease(A.seg(t, .6, 2.0))
    s = f'<rect width="{W}" height="{H}" fill="#170f12"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{pol:.0f}"'
                   f' fill="#2a1820"/>'
            + kladka(0, 40, 520, 620, 76, "#4a2a34")
            + kladka(1400, 40, 520, 620, 76, "#4a2a34"))
    s += SL(Z_DAL, _ekran_kino(560, 110, 800, 430, t, sk))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#3a2028"/>'
            + _pol_shvy(pol - 6, 1074, 289, 6, "#2a151c"))
    # БУДКА КИНОМЕХАНИКА с окошком — источник луча
    s += SL(Z_DAL, f'<rect x="1660" y="150" width="260" height="330" rx="10"'
                   f' fill="#3d2a30" {o(6)}/>'
            + f'<rect x="1700" y="210" width="150" height="120" rx="8"'
              f' fill="#1a1012" {o(5)}/>'
            + f'<rect x="1718" y="228" width="114" height="84" rx="6"'
              f' fill="{SVET}" opacity="{.7+.2*abs(A.w(t,2.2,.2)):.2f}"/>'
            + f'<circle cx="1775" cy="400" r="34" fill="none" stroke="#6f767c"'
              f' stroke-width="9"/>'
            + f'<circle cx="1860" cy="400" r="24" fill="none" stroke="#6f767c"'
              f' stroke-width="8"/>')
    # ТЁПЛЫЙ ЛУЧ скользит с кресла на кресло
    lx = 1760 - 760 * sk
    s += SL(Z_SRED, f'<g transform="rotate({10 - 16 * sk:.1f} 1775 270)">'
            + _konus_sveta(1775, 270, 560, 760, 0.0, .34, "#ffd98a") + "</g>")
    s += SL(Z_SRED, luch(900, 240, 820, 720, t, .22))
    rnd2 = random.Random(291)
    for i in range(28):
        p = ((t * .22 + rnd2.random()) % 1.0)
        pxx = 1700 - p * 900 + rnd2.uniform(-60, 60)
        pyy = 300 + p * 420 + rnd2.uniform(-70, 70)
        s += SL(Z_LETIT, f'<circle cx="{pxx:.0f}" cy="{pyy:.0f}"'
                         f' r="{rnd2.uniform(2.5,6):.0f}" fill="#ffeec2"'
                         f' opacity="{.25+.5*abs(A.w(t,1.6,i*.2)):.2f}"/>')
    # РЯДЫ КРЕСЕЛ в глубину
    s += SL(Z_DAL, _kresla_ryad(160, 700, 1600, t, 7, 200, "#6a1c30", False))
    s += SL(Z_SRED, _kresla_ryad(100, 800, 1740, t, 6, 250, "#7a2338", False))
    # ДВА КРЕСЛА ПЕРВОГО РЯДА — главный предмет плана
    s += SL(Z_SRED, _kresla_ryad(360, pol, 1240, t, 2, 420, "#8a2a40", True))
    # на левом кресле кепка на рупоре, на правом коробка с катушкой
    s += SL(Z_SRED, _kepka_i_rupor(640, pol - 300, 1.15, t))
    s += SL(Z_SRED, _korobka_katushki(1320, pol - 268, 1.0, t, True))
    # нижняя треть: проход, ковровая дорожка, урна, оброненный билетик-лоскут
    s += SL(Z_SRED, _polovik(960, pol + 40, 760, 120, "#8a2a40", "#5a1626"))
    s += SL(Z_SRED, _dvorovaya_utvar(140, pol + 48, 220, t, 293, ["vedro"])
            + _yaschiki(1740, pol + 16, t, 295, 2, .82)
            + _kucha_listev(540, pol + 52, 240, 297, 58))
    s += SL(Z_SRED, _kot_zhivoy(1540, pol + 48, t, 1.05, "#2f2a26", .3))
    s += SL(Z_SRED, svecha(120, pol - 150, t, .3, 1.2, 104)
            + teplo(130, pol - 210, 240, 200, .34))
    s += SL(Z_SRED, blik(1775, 270, t, 1.3, "#bcd8ff", "#ffd98a", .5))
    s += SL(Z_PERED, _stolb_pered(-8, 120, "#140a0e", 0, H))
    s += vinetka(.50)
    return s


# ── ПОМОЩНИКИ ЧЕТВЁРТОЙ ПАРТИИ ────────────────────────────────────────────

def _televizor_nozhki(x, y, w_, t, h_=430, ekran=None):
    """ТЕЛЕВИЗОР НА ТОНКИХ НОЖКАХ — главный предмет: деревянный корпус с
    выпуклым экраном в скруглённой рамке, решётка динамика, две круглые
    крутилки, тонкие косые ножки с латунными наконечниками. На корпусе
    салфетка. Середина экрана остаётся ВАМ — туда встаёт настоящий кадр."""
    s = (f'{ten(x + w_ * .5, y + 10, w_ * .48, 18, .5)}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="22" fill="#7d5636" {o(8)}/>'
         f'<rect x="{x+14:.0f}" y="{y-h_+14:.0f}" width="{w_-28:.0f}"'
         f' height="{h_-28:.0f}" rx="18" fill="#8a6038" opacity=".9"/>')
    # решётка динамика и крутилки справа
    gx = x + w_ - 118
    for i in range(7):
        s += (f'<rect x="{gx:.0f}" y="{y-h_*.86+i*22:.0f}" width="86"'
              f' height="11" rx="5" fill="#5b4428" opacity=".9"/>')
    for i in (0, 1):
        s += (f'<circle cx="{gx+44:.0f}" cy="{y-h_*.34+i*70:.0f}" r="26"'
              f' fill="#c9a47a" {o(5)}/>'
              f'<circle cx="{gx+44:.0f}" cy="{y-h_*.34+i*70:.0f}" r="9"'
              f' fill="#5b4428"/>')
    for i in (0, 1):
        nx = x + 60 + i * (w_ - 150)
        s += (f'<line x1="{nx:.0f}" y1="{y-6:.0f}" x2="{nx+(-34 if i == 0 else 34):.0f}"'
              f' y2="{y+150:.0f}" stroke="#5b4428" stroke-width="18"'
              f' stroke-linecap="round"/>'
              f'<ellipse cx="{nx+(-34 if i == 0 else 34):.0f}" cy="{y+152:.0f}"'
              f' rx="16" ry="8" fill="{ZOL}" {o(3)}/>')
    s += (f'<path d="M{x-10:.0f},{y-h_-6:.0f} q{w_*.5:.0f},{-26:.0f}'
          f' {w_+20:.0f},0 l{-14:.0f},{30:.0f} q{-w_*.5:.0f},{-18:.0f}'
          f' {-(w_-8):.0f},0 Z" fill="{KREM}" {o(5)}/>')
    for i in range(int(w_ / 46)):
        s += (f'<path d="M{x+12+i*46:.0f},{y-h_+8:.0f} q{11:.0f},{14:.0f}'
              f' {22:.0f},0" fill="none" stroke="#d9d0b8" stroke-width="5"/>')
    return s


def _torsher(x, y, t, s_=1.0, h_=620):
    """Торшер: трёхлапая стойка, витая нога, тканевый абажур с бахромой и
    тёплый свет из-под него."""
    s = (f'{ten(x, y + 8 * s_, 72 * s_, 14 * s_, .45)}')
    for i in (-1, 0, 1):
        s += (f'<path d="M{x:.0f},{y-14*s_:.0f} q{i*44*s_:.0f},{10*s_:.0f}'
              f' {i*62*s_:.0f},{16*s_:.0f}" fill="none" stroke="#5b4428"'
              f' stroke-width="{12*s_:.0f}" stroke-linecap="round"/>')
    s += (f'<rect x="{x-9*s_:.0f}" y="{y-h_:.0f}" width="{18*s_:.0f}"'
          f' height="{h_:.0f}" rx="{8*s_:.0f}" fill="#7d5636" {o(5)}/>')
    for i in range(5):
        s += (f'<ellipse cx="{x:.0f}" cy="{y-h_*.22-i*h_*.13:.0f}"'
              f' rx="{16*s_:.0f}" ry="{7*s_:.0f}" fill="#9c7049" {o(3)}/>')
    s += (f'<path d="M{x-96*s_:.0f},{y-h_:.0f} L{x+96*s_:.0f},{y-h_:.0f}'
          f' L{x+66*s_:.0f},{y-h_-120*s_:.0f} L{x-66*s_:.0f},{y-h_-120*s_:.0f} Z"'
          f' fill="{RUSH}" {o(6)}/>'
          f'<path d="M{x-66*s_:.0f},{y-h_-120*s_:.0f} q{66*s_:.0f},{-16*s_:.0f}'
          f' {132*s_:.0f},0" fill="none" stroke="#c9b48a"'
          f' stroke-width="{8*s_:.0f}"/>')
    for i in range(10):
        s += (f'<line x1="{x-92*s_+i*20*s_:.0f}" y1="{y-h_:.0f}"'
              f' x2="{x-94*s_+i*21*s_:.0f}" y2="{y-h_+22*s_:.0f}"'
              f' stroke="#c9b48a" stroke-width="{max(2,4*s_):.0f}"/>')
    s += (f'<ellipse cx="{x:.0f}" cy="{y-h_+14*s_:.0f}" rx="{86*s_:.0f}"'
          f' ry="{18*s_:.0f}" fill="{SVET}"'
          f' opacity="{.6+.2*abs(A.w(t,2.4,.2)):.2f}"/>'
          f'{teplo(x, y - h_ + 40 * s_, 300 * s_, 260 * s_, .36)}')
    return s


def _vyazanie(x, y, s_=1.0, t=0.0, ph=.0):
    """Вязание со спицами: начатое полотно резинкой, две спицы наперекрест
    (мелькают), клубок на нитке рядом."""
    mel = 9.0 * A.w(t, .7, ph)
    s = (f'<path d="M{x-76*s_:.0f},{y:.0f} L{x+76*s_:.0f},{y:.0f}'
         f' L{x+66*s_:.0f},{y+96*s_:.0f} L{x-66*s_:.0f},{y+96*s_:.0f} Z"'
         f' fill="#8a4a5c" {o(5)}/>')
    for i in range(6):
        s += (f'<line x1="{x-62*s_+i*25*s_:.0f}" y1="{y+6*s_:.0f}"'
              f' x2="{x-58*s_+i*23*s_:.0f}" y2="{y+90*s_:.0f}"'
              f' stroke="#6a2c3c" stroke-width="{max(2,5*s_):.0f}"/>')
    for i in (-1, 1):
        s += (f'<g transform="rotate({i*mel:.1f} {x:.0f} {y:.0f})">'
              f'<line x1="{x+i*70*s_:.0f}" y1="{y+10*s_:.0f}"'
              f' x2="{x+i*140*s_:.0f}" y2="{y-54*s_:.0f}" stroke="#cfd8dc"'
              f' stroke-width="{max(3,7*s_):.0f}" stroke-linecap="round"/>'
              f'<circle cx="{x+i*142*s_:.0f}" cy="{y-56*s_:.0f}" r="{7*s_:.0f}"'
              f' fill="#9aa3aa"/></g>')
    s += (f'<circle cx="{x+40*s_:.0f}" cy="{y+150*s_:.0f}" r="{44*s_:.0f}"'
          f' fill="#8a4a5c" {o(5)}/>')
    for i in range(4):
        s += (f'<path d="M{x+4*s_+i*6*s_:.0f},{y+150*s_:.0f}'
              f' q{40*s_:.0f},{-26*s_+i*14*s_:.0f} {76*s_:.0f},{6*s_:.0f}"'
              f' fill="none" stroke="#6a2c3c" stroke-width="{max(2,4*s_):.0f}"/>')
    s += (f'<path d="M{x+40*s_:.0f},{y+106*s_:.0f} q{-16*s_:.0f},{-30*s_:.0f}'
          f' {-50*s_:.0f},{-20*s_:.0f}" fill="none" stroke="#8a4a5c"'
          f' stroke-width="{max(2,4*s_):.0f}"/>')
    return s


def _elovaya_vetka_v_banke(x, y, s_=1.0, t=0.0, ph=.0):
    """Ёлочная ветка в банке: стеклянная банка с водой, лапа с иглами в три
    яруса и одна игрушка-шар на нитке. Ветка покачивается целиком."""
    kach = 2.6 * A.w(t, 2.2, ph)
    s = (f'{ten(x, y + 6 * s_, 44 * s_, 10 * s_, .4)}'
         f'<rect x="{x-40*s_:.0f}" y="{y-120*s_:.0f}" width="{80*s_:.0f}"'
         f' height="{120*s_:.0f}" rx="10" fill="url(#stekl)" opacity=".88" {o(5)}/>'
         f'<rect x="{x-34*s_:.0f}" y="{y-70*s_:.0f}" width="{68*s_:.0f}"'
         f' height="{64*s_:.0f}" rx="7" fill="{VODA}" opacity=".5"/>')
    s += f'<g transform="rotate({kach:.1f} {x:.0f} {y-120*s_:.0f})">'
    s += (f'<line x1="{x:.0f}" y1="{y-110*s_:.0f}" x2="{x+16*s_:.0f}"'
          f' y2="{y-330*s_:.0f}" stroke="#4e3c2c"'
          f' stroke-width="{max(3,9*s_):.0f}"/>')
    for i in range(4):
        yy = y - (150 + i * 56) * s_
        dl = (120 - i * 20) * s_
        for sg in (-1, 1):
            s += (f'<path d="M{x+i*4*s_:.0f},{yy:.0f} q{sg*dl*.5:.0f},'
                  f'{-10*s_:.0f} {sg*dl:.0f},{-26*s_:.0f}" fill="none"'
                  f' stroke="#2f5a34" stroke-width="{max(3,8*s_):.0f}"/>')
            for j in range(5):
                s += (f'<line x1="{x+i*4*s_+sg*dl*(.2+j*.18):.0f}"'
                      f' y1="{yy-6*s_-j*4*s_:.0f}"'
                      f' x2="{x+i*4*s_+sg*dl*(.2+j*.18)+sg*16*s_:.0f}"'
                      f' y2="{yy-24*s_-j*5*s_:.0f}" stroke="#3f7a44"'
                      f' stroke-width="{max(2,4*s_):.0f}"/>')
    s += (f'<line x1="{x+10*s_:.0f}" y1="{y-250*s_:.0f}" x2="{x+32*s_:.0f}"'
          f' y2="{y-212*s_:.0f}" stroke="#c9b48a" stroke-width="{max(2,3*s_):.0f}"/>'
          f'<circle cx="{x+34*s_:.0f}" cy="{y-196*s_:.0f}" r="{22*s_:.0f}"'
          f' fill="{KRAS}" {o(4)}/>'
          f'<ellipse cx="{x+26*s_:.0f}" cy="{y-206*s_:.0f}" rx="{8*s_:.0f}"'
          f' ry="{5*s_:.0f}" fill="#ffd1c0" opacity=".7"/></g>')
    return s


def _afisha(x, y, w_, h_, t, vid="chasy", podsvet=.0, seed=3):
    """РИСОВАННАЯ АФИША: рамка-планка, фон, КРУПНЫЙ ПРЕДМЕТ вместо лиц и
    пустая полоса сверху под название. Букв не рисуем вовсе — вместо текста
    волнистая строка, настоящее название кладёт `kadr.py` поверх."""
    rnd = random.Random(seed)
    fon = {"chasy": "#8a2a40", "mashinka": "#2f5a6a",
           "sakvoyazhi": "#5a4a2e", "venik": "#3f5a3a"}[vid]
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="8" fill="{fon}" {o(7)}/>'
         f'<rect x="{x+12:.0f}" y="{y+12:.0f}" width="{w_-24:.0f}"'
         f' height="{h_-24:.0f}" rx="6" fill="none" stroke="{KREM}"'
         f' stroke-width="7" opacity=".7"/>'
         f'<rect x="{x+24:.0f}" y="{y+26:.0f}" width="{w_-48:.0f}"'
         f' height="{h_*.14:.0f}" rx="6" fill="{KREM}" opacity=".9"/>')
    for i in range(2):
        s += (f'<path d="M{x+44:.0f},{y+40+i*22:.0f} q{(w_-88)*.25:.0f},{-10:.0f}'
              f' {(w_-88)*.5:.0f},0 q{(w_-88)*.25:.0f},{10:.0f}'
              f' {(w_-88)*.5:.0f},0" fill="none" stroke="#8a7a5c"'
              f' stroke-width="6"/>')
    cx, cy = x + w_ * .5, y + h_ * .60
    if vid == "chasy":
        s += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{w_*.30:.0f}"'
              f' fill="{ZOL}" {o(6)}/>'
              f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{w_*.24:.0f}"'
              f' fill="{KREM}" {o(4)}/>'
              f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{cx+w_*.14:.0f}"'
              f' y2="{cy-w_*.10:.0f}" stroke="{K}" stroke-width="8"/>'
              f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{cx-w_*.04:.0f}"'
              f' y2="{cy-w_*.19:.0f}" stroke="{K}" stroke-width="7"/>')
        for i in range(10):
            p = ((t * .5 + i / 10.0) % 1.0)
            s += (f'<path d="M{cx-w_*.34+i*w_*.075:.0f},{cy-w_*.36:.0f}'
                  f' q{10:.0f},{30+14*math.sin(t*3+i):.0f} {-4:.0f},{60:.0f}"'
                  f' fill="none" stroke="{["#e8c64e", "#cfe4f5", "#d6452a"][i % 3]}"'
                  f' stroke-width="7" opacity=".9"/>'
                  f'<circle cx="{cx-w_*.30+i*w_*.07:.0f}"'
                  f' cy="{cy+w_*.30+p*w_*.20:.0f}" r="7"'
                  f' fill="{["#e8c64e", "#cfe4f5", "#d6452a"][i % 3]}"'
                  f' opacity="{1-p:.2f}"/>')
    elif vid == "mashinka":
        s += (f'<path d="M{cx-w_*.32:.0f},{cy+w_*.16:.0f}'
              f' L{cx+w_*.32:.0f},{cy+w_*.16:.0f} L{cx+w_*.26:.0f},{cy-w_*.10:.0f}'
              f' L{cx-w_*.26:.0f},{cy-w_*.10:.0f} Z" fill="#3d3a38" {o(6)}/>'
              f'<rect x="{cx-w_*.22:.0f}" y="{cy-w_*.26:.0f}"'
              f' width="{w_*.44:.0f}" height="{w_*.16:.0f}" rx="6"'
              f' fill="#4e4a47" {o(4)}/>')
        for r in range(3):
            for c in range(8):
                s += (f'<circle cx="{cx-w_*.24+c*w_*.068+r*6:.0f}"'
                      f' cy="{cy+w_*.02+r*w_*.045:.0f}" r="{w_*.020:.0f}"'
                      f' fill="{KREM}" opacity=".9"/>')
        s += (f'<circle cx="{cx-w_*.20:.0f}" cy="{cy-w_*.34:.0f}"'
              f' r="{w_*.085:.0f}" fill="none" stroke="{ZOL}" stroke-width="7"/>'
              f'<circle cx="{cx-w_*.02:.0f}" cy="{cy-w_*.34:.0f}"'
              f' r="{w_*.085:.0f}" fill="none" stroke="{ZOL}" stroke-width="7"/>'
              f'<line x1="{cx-w_*.12:.0f}" y1="{cy-w_*.34:.0f}"'
              f' x2="{cx-w_*.10:.0f}" y2="{cy-w_*.34:.0f}" stroke="{ZOL}"'
              f' stroke-width="7"/>')
    elif vid == "sakvoyazhi":
        s += (f'<rect x="{x+16:.0f}" y="{cy+w_*.16:.0f}" width="{w_-32:.0f}"'
              f' height="{h_*.10:.0f}" fill="#4a4036" {o(4)}/>'
              f'<circle cx="{cx:.0f}" cy="{y+h_*.30:.0f}" r="{w_*.13:.0f}"'
              f' fill="{KREM}" {o(5)}/>'
              f'<line x1="{cx:.0f}" y1="{y+h_*.30:.0f}" x2="{cx+w_*.07:.0f}"'
              f' y2="{y+h_*.24:.0f}" stroke="{K}" stroke-width="6"/>')
        for i, (dx, sc) in enumerate(((-w_ * .18, 1.0), (w_ * .18, .78))):
            s += (f'<path d="M{cx+dx-w_*.15*sc:.0f},{cy+w_*.16:.0f}'
                  f' q{-w_*.02:.0f},{-w_*.20*sc:.0f} {w_*.15*sc:.0f},{-w_*.21*sc:.0f}'
                  f' q{w_*.16*sc:.0f},{w_*.01*sc:.0f} {w_*.15*sc:.0f},{w_*.21*sc:.0f} Z"'
                  f' fill="#7d5636" {o(5)}/>'
                  f'<path d="M{cx+dx-w_*.07*sc:.0f},{cy-w_*.06*sc:.0f}'
                  f' q{w_*.07*sc:.0f},{-w_*.09*sc:.0f} {w_*.14*sc:.0f},0"'
                  f' fill="none" stroke="#4a3522" stroke-width="7"/>')
    else:
        s += _venik(cx - w_ * .12, cy + w_ * .22, w_ * .52, t, "#cdbf9c",
                    "#b8352c", False, .14, .2, w_ * .0016, seed + 1)
        s += (f'<line x1="{cx+w_*.20:.0f}" y1="{y+h_*.26:.0f}"'
              f' x2="{cx+w_*.20:.0f}" y2="{cy-w_*.06:.0f}" stroke="{KREM}"'
              f' stroke-width="5"/>'
              f'<circle cx="{cx+w_*.20:.0f}" cy="{cy+w_*.03:.0f}"'
              f' r="{w_*.10:.0f}" fill="{KRAS}" {o(5)}/>'
              f'<ellipse cx="{cx+w_*.16:.0f}" cy="{cy-w_*.01:.0f}"'
              f' rx="{w_*.035:.0f}" ry="{w_*.022:.0f}" fill="#ffd1c0"'
              f' opacity=".75"/>')
    s += (f'<rect x="{x-10:.0f}" y="{y-16:.0f}" width="{w_+20:.0f}" height="22"'
          f' rx="8" fill="#5a4530" {o(5)}/>'
          f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
          f' rx="8" fill="{SVET}" opacity="{.26*podsvet:.2f}"/>')
    return s


def _stremyanka(x, y, h_, t, stup=4):
    """Стремянка расклейщика: две стойки под углом, ступени, распорка и
    крючок с ведёрком. Чуть переступает под весом."""
    k = .5 * A.w(t, 3.4, .2)
    s = f'<g transform="rotate({k:.1f} {x:.0f} {y:.0f})">'
    for i, sg in ((0, -1), (1, 1)):
        s += (f'<line x1="{x+sg*20:.0f}" y1="{y:.0f}" x2="{x+sg*90:.0f}"'
              f' y2="{y+h_:.0f}" stroke="#8a6038" stroke-width="22"'
              f' stroke-linecap="round"/>')
    for i in range(stup):
        p = (i + 1) / float(stup + 1)
        yy = y + h_ * p
        ww = 40 + 150 * p
        s += (f'<rect x="{x-ww*.5:.0f}" y="{yy:.0f}" width="{ww:.0f}"'
              f' height="18" rx="7" fill="url(#dosk)" {o(4)}/>')
    s += (f'<line x1="{x-70:.0f}" y1="{y+h_*.62:.0f}" x2="{x+70:.0f}"'
          f' y2="{y+h_*.62:.0f}" stroke="#5b4428" stroke-width="12"/>'
          f'<path d="M{x+24:.0f},{y+20:.0f} q{26:.0f},{-14:.0f} {30:.0f},{14:.0f}"'
          f' fill="none" stroke="{ZHELEZ}" stroke-width="8"/></g>')
    return s


def _vederko_kleya(x, y, s_=1.0, t=0.0, kist=True):
    """Ведёрко с клеем и кисть: жестяное ведро с дугой-ручкой, мутный клей,
    на борту лежит широкая кисть с деревянной ручкой."""
    s = (f'{ten(x, y + 8 * s_, 60 * s_, 12 * s_, .45)}'
         f'<path d="M{x-56*s_:.0f},{y-110*s_:.0f} q{6*s_:.0f},{110*s_:.0f}'
         f' {56*s_:.0f},{110*s_:.0f} q{50*s_:.0f},0 {56*s_:.0f},{-110*s_:.0f} Z"'
         f' fill="#9aa3aa" {o(6)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-110*s_:.0f}" rx="{56*s_:.0f}"'
         f' ry="{16*s_:.0f}" fill="#b9c6cc" {o(4)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-104*s_:.0f}" rx="{44*s_:.0f}"'
         f' ry="{11*s_:.0f}" fill="#d9d0b8" opacity=".9"/>'
         f'<path d="M{x-56*s_:.0f},{y-104*s_:.0f} q{56*s_:.0f},{-54*s_:.0f}'
         f' {112*s_:.0f},0" fill="none" stroke="{ZHELEZ}"'
         f' stroke-width="{8*s_:.0f}"/>')
    if kist:
        s += (f'<g transform="rotate(-24 {x+40*s_:.0f} {y-110*s_:.0f})">'
              f'<rect x="{x+30*s_:.0f}" y="{y-200*s_:.0f}" width="{22*s_:.0f}"'
              f' height="{90*s_:.0f}" rx="8" fill="#8a6038" {o(4)}/>'
              f'<rect x="{x+22*s_:.0f}" y="{y-116*s_:.0f}" width="{38*s_:.0f}"'
              f' height="{36*s_:.0f}" rx="6" fill="#c9b48a" {o(4)}/></g>')
    return s


def _schetka_oboynaya(x, y, s_=1.0, ug=0.0, t=0.0):
    """Щётка для афиш: деревянная колодка с ворсом и скобой-ручкой; ворс
    приминается по ходу разглаживания."""
    pr = 4 * s_ * A.w(t, 1.3, .2)
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'<rect x="{x-62*s_:.0f}" y="{y-26*s_:.0f}" width="{124*s_:.0f}"'
            f' height="{26*s_:.0f}" rx="{9*s_:.0f}" fill="#8a6038" {o(5)}/>'
            f'<path d="M{x-40*s_:.0f},{y-26*s_:.0f} q{40*s_:.0f},{-30*s_:.0f}'
            f' {80*s_:.0f},0" fill="none" stroke="{ZHELEZ}"'
            f' stroke-width="{11*s_:.0f}"/>'
            + "".join(f'<line x1="{x-56*s_+i*14*s_:.0f}" y1="{y:.0f}"'
                      f' x2="{x-56*s_+i*14*s_+pr:.0f}" y2="{y+30*s_:.0f}"'
                      f' stroke="#c9b48a" stroke-width="{max(2,5*s_):.0f}"/>'
                      for i in range(9))
            + "</g>")


def _setka_mandarinov(x, y, s_=1.0, t=0.0, ph=.0, n=7):
    """Сетка с мандаринами: ячейки сетки, оранжевые плоды с пупком и
    листиком, сетка оттягивается вниз и качается в руке."""
    rnd = random.Random(int(x) + 23)
    kol = 5.0 * A.w(t, 1.6, ph)
    s = f'<g transform="rotate({kol:.1f} {x:.0f} {y:.0f})">'
    s += (f'<path d="M{x-8*s_:.0f},{y:.0f} q{-54*s_:.0f},{44*s_:.0f}'
          f' {-40*s_:.0f},{110*s_:.0f} q{48*s_:.0f},{44*s_:.0f}'
          f' {100*s_:.0f},0 q{14*s_:.0f},{-66*s_:.0f} {-40*s_:.0f},{-110*s_:.0f} Z"'
          f' fill="#c24a2a" opacity=".32" {o(4)}/>')
    for i in range(n):
        a = rnd.uniform(0, 6.28)
        rr = rnd.uniform(.25, .9)
        mx = x + 8 * s_ + math.cos(a) * 42 * s_ * rr
        my = y + 60 * s_ + abs(math.sin(a)) * 54 * s_ * rr
        r = rnd.uniform(22, 30) * s_
        s += (f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="{r:.0f}" fill="{ORA}"'
              f' {o(4)}/>'
              f'<circle cx="{mx:.0f}" cy="{my-r*.78:.0f}" r="{r*.17:.0f}"'
              f' fill="#8a4a1c"/>'
              f'<ellipse cx="{mx-r*.34:.0f}" cy="{my-r*.34:.0f}"'
              f' rx="{r*.22:.0f}" ry="{r*.13:.0f}" fill="#f8c27a" opacity=".6"/>')
    for i in range(6):
        s += (f'<path d="M{x-42*s_+i*18*s_:.0f},{y+10*s_:.0f}'
              f' q{8*s_:.0f},{60*s_:.0f} {2*s_:.0f},{112*s_:.0f}" fill="none"'
              f' stroke="#8a2a18" stroke-width="{max(2,3*s_):.0f}" opacity=".85"/>')
    for i in range(4):
        s += (f'<path d="M{x-44*s_:.0f},{y+30*s_+i*28*s_:.0f}'
              f' q{50*s_:.0f},{14*s_:.0f} {100*s_:.0f},{-4*s_:.0f}" fill="none"'
              f' stroke="#8a2a18" stroke-width="{max(2,3*s_):.0f}" opacity=".85"/>')
    s += (f'<ellipse cx="{x+8*s_:.0f}" cy="{y+4*s_:.0f}" rx="{22*s_:.0f}"'
          f' ry="{9*s_:.0f}" fill="#8a2a18" {o(3)}/></g>')
    return s


def _portfel(x, y, s_=1.0, t=0.0, ug=0.0):
    """Портфель: кожаный корпус со швами, два ремешка с пряжками, скобяной
    замок и ручка дугой."""
    w2, h2 = 150 * s_, 180 * s_
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'{ten(x, y + 8 * s_, w2 * .54, 12 * s_, .45)}'
            f'<rect x="{x-w2/2:.0f}" y="{y-h2:.0f}" width="{w2:.0f}"'
            f' height="{h2:.0f}" rx="{14*s_:.0f}" fill="#6b4a2c" {o(6)}/>'
            f'<path d="M{x-w2/2:.0f},{y-h2*.70:.0f} L{x+w2/2:.0f},{y-h2*.70:.0f}'
            f' L{x+w2*.44:.0f},{y-h2*.40:.0f} L{x-w2*.44:.0f},{y-h2*.40:.0f} Z"'
            f' fill="#7d5636" {o(5)}/>'
            + "".join(f'<g><rect x="{x+i*w2*.26-8*s_:.0f}" y="{y-h2*.52:.0f}"'
                      f' width="{16*s_:.0f}" height="{h2*.30:.0f}" rx="5"'
                      f' fill="#4a3522" {o(3)}/>'
                      f'<rect x="{x+i*w2*.26-11*s_:.0f}" y="{y-h2*.36:.0f}"'
                      f' width="{22*s_:.0f}" height="{12*s_:.0f}" rx="4"'
                      f' fill="{ZOL}" {o(3)}/></g>' for i in (-1, 1))
            + f'<rect x="{x-14*s_:.0f}" y="{y-h2*.60:.0f}" width="{28*s_:.0f}"'
              f' height="{20*s_:.0f}" rx="5" fill="{ZHELEZ}" {o(3)}/>'
            + f'<path d="M{x-42*s_:.0f},{y-h2:.0f} q{42*s_:.0f},{-56*s_:.0f}'
              f' {84*s_:.0f},0" fill="none" stroke="#4a3522"'
              f' stroke-width="{13*s_:.0f}"/>'
            + f'<path d="M{x-w2*.42:.0f},{y-h2*.16:.0f} q{w2*.42:.0f},{10*s_:.0f}'
              f' {w2*.84:.0f},0" fill="none" stroke="#4a3522"'
              f' stroke-width="{max(2,4*s_):.0f}" opacity=".8"/></g>')


def _fonar_dvorovoy(x, y, t, s_=1.0, h_=620):
    """Дворовый фонарь: чугунный столб с хомутами, кронштейн, жестяной
    колпак и лампа с живым дрожанием света; конус света на снег."""
    mig = .78 + .18 * abs(A.w(t, 2.6, .2))
    s = (f'{ten(x, y + 8 * s_, 44 * s_, 12 * s_, .45)}'
         f'<path d="M{x-30*s_:.0f},{y:.0f} q{30*s_:.0f},{-20*s_:.0f}'
         f' {60*s_:.0f},0 Z" fill="#3d3a38" {o(4)}/>'
         f'<rect x="{x-11*s_:.0f}" y="{y-h_:.0f}" width="{22*s_:.0f}"'
         f' height="{h_:.0f}" rx="{9*s_:.0f}" fill="#4e4a47" {o(5)}/>')
    for i in range(3):
        s += (f'<rect x="{x-16*s_:.0f}" y="{y-h_*(.26+i*.26):.0f}"'
              f' width="{32*s_:.0f}" height="{12*s_:.0f}" rx="5"'
              f' fill="#5f5a56" {o(3)}/>')
    s += (f'<path d="M{x:.0f},{y-h_:.0f} q{10*s_:.0f},{-54*s_:.0f}'
          f' {66*s_:.0f},{-56*s_:.0f}" fill="none" stroke="#4e4a47"'
          f' stroke-width="{14*s_:.0f}"/>'
          f'<path d="M{x+36*s_:.0f},{y-h_-56*s_:.0f} L{x+96*s_:.0f},{y-h_-56*s_:.0f}'
          f' L{x+82*s_:.0f},{y-h_-96*s_:.0f} L{x+50*s_:.0f},{y-h_-96*s_:.0f} Z"'
          f' fill="#3d3a38" {o(5)}/>'
          f'<ellipse cx="{x+66*s_:.0f}" cy="{y-h_-42*s_:.0f}" rx="{34*s_:.0f}"'
          f' ry="{24*s_:.0f}" fill="{SVET}" opacity="{mig:.2f}" {o(4)}/>'
          f'{teplo(x + 66 * s_, y - h_ - 30 * s_, 320 * s_, 280 * s_, .40)}'
          + _konus_sveta(x + 66 * s_, y - h_ - 20 * s_, 220 * s_,
                         h_ + 40 * s_, 0.0, .26))
    return s


def _okoshko_kassy(x, y, w_, h_, t, otryv=.0):
    """ОКОШКО КАССЫ — главный предмет: полукруглое окно в деревянной
    обвязке, латунная решётка, мраморный подоконничек, блюдце для монет и
    рулон билетов с отрывающимся билетом."""
    put = kontur_proema(x, y, w_, h_, "arka")
    s = (f'<path d="{put}" fill="#2a1d14"/>'
         f'<path d="{put}" fill="{SVET}" opacity=".20"/>'
         f'<path d="{put}" fill="none" stroke="#7d5636" stroke-width="34"/>')
    for i in range(7):
        s += (f'<line x1="{x+30+i*(w_-60)/6.0:.0f}" y1="{y+h_*.30:.0f}"'
              f' x2="{x+30+i*(w_-60)/6.0:.0f}" y2="{y+h_-14:.0f}"'
              f' stroke="{ZOL}" stroke-width="9" opacity=".85"/>')
    for i in range(3):
        s += (f'<path d="M{x+20:.0f},{y+h_*(.34+i*.20):.0f}'
              f' q{w_*.5:.0f},{-14:.0f} {w_-40:.0f},0" fill="none" stroke="{ZOL}"'
              f' stroke-width="8" opacity=".8"/>')
    s += (f'<rect x="{x-40:.0f}" y="{y+h_-16:.0f}" width="{w_+80:.0f}"'
          f' height="44" rx="12" fill="#cfc9bc" {o(6)}/>'
          f'<rect x="{x-40:.0f}" y="{y+h_+28:.0f}" width="{w_+80:.0f}"'
          f' height="18" rx="7" fill="#a8a299" {o(4)}/>')
    # блюдце для монет и рулон билетов
    s += (f'<ellipse cx="{x+w_*.26:.0f}" cy="{y+h_+2:.0f}" rx="64" ry="20"'
          f' fill="#dde6ea" {o(5)}/>'
          f'<ellipse cx="{x+w_*.26:.0f}" cy="{y+h_-2:.0f}" rx="50" ry="13"'
          f' fill="#b9c6cc" opacity=".9"/>')
    rx_ = x + w_ * .74
    s += (f'<circle cx="{rx_:.0f}" cy="{y+h_*.70:.0f}" r="52" fill="#e8c64e"'
          f' {o(5)}/>'
          f'<circle cx="{rx_:.0f}" cy="{y+h_*.70:.0f}" r="16" fill="#8a6038"'
          f' {o(3)}/>')
    for i in range(4):
        s += (f'<circle cx="{rx_:.0f}" cy="{y+h_*.70:.0f}" r="{46-i*10:.0f}"'
              f' fill="none" stroke="#c9a331" stroke-width="4" opacity=".8"/>')
    s += (f'<path d="M{rx_+50:.0f},{y+h_*.70:.0f} l{70+60*otryv:.0f},{-8:.0f}'
          f' l{2:.0f},{40:.0f} l{-(70+60*otryv):.0f},{8:.0f} Z"'
          f' fill="#f4eedc" {o(4)}/>'
          f'<path d="M{rx_+88+30*otryv:.0f},{y+h_*.70-6:.0f}'
          f' q{10:.0f},{20:.0f} {0:.0f},{38:.0f}" fill="none" stroke="#c9b48a"'
          f' stroke-width="5"/>')
    return s


def _naves_lampochki(x, y, w_, t, n=12, h_=70):
    """Навес кинотеатра двадцатых с бегущими лампочками: жестяной карниз,
    кронштейны и два ряда лампочек, которые загораются бегом."""
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="10" fill="#4e4a47" {o(7)}/>'
         f'<rect x="{x-16:.0f}" y="{y-16:.0f}" width="{w_+32:.0f}" height="24"'
         f' rx="9" fill="#5f5a56" {o(5)}/>')
    for i in (0, 1):
        for j in range(n):
            faza = ((t * 2.2 + j * .18 + i * .4) % 1.0)
            яр = .35 + .65 * (1 - abs(faza - .5) * 2)
            s += (f'<circle cx="{x+30+j*(w_-60)/(n-1.0):.0f}"'
                  f' cy="{y+20+i*(h_-34):.0f}" r="13" fill="{SVET}"'
                  f' opacity="{яр:.2f}" stroke="#8a7a46" stroke-width="4"/>')
    for i in range(4):
        bx = x + 60 + i * (w_ - 120) / 3.0
        s += (f'<path d="M{bx:.0f},{y+h_:.0f} q{10:.0f},{46:.0f} {-26:.0f},{64:.0f}'
              f' l{30:.0f},{6:.0f} q{16:.0f},{-30:.0f} {12:.0f},{-70:.0f} Z"'
              f' fill="#5f5a56" {o(4)}/>')
    s += (f'{teplo(x + w_ * .5, y + h_ + 40, w_ * .56, 180, .30)}')
    return s


def _tablichka_bez_cifr(x, y, w_, h_, t, ph=.0):
    """Табличка на двух крючках: жестяное поле с кромкой и ВОЛНИСТАЯ строка
    вместо года — свои буквы и цифры в декорации не рисуются, настоящий
    «1928» кладёт `kadr.py` поверх."""
    kach = 2.2 * A.w(t, 2.8, ph)
    s = (f'<g transform="rotate({kach:.1f} {x+w_*.5:.0f} {y:.0f})">'
         f'<line x1="{x+18:.0f}" y1="{y:.0f}" x2="{x+22:.0f}" y2="{y+26:.0f}"'
         f' stroke="{ZHELEZ}" stroke-width="5"/>'
         f'<line x1="{x+w_-18:.0f}" y1="{y:.0f}" x2="{x+w_-22:.0f}"'
         f' y2="{y+26:.0f}" stroke="{ZHELEZ}" stroke-width="5"/>'
         f'<rect x="{x:.0f}" y="{y+26:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="9" fill="#efe8d8" {o(5)}/>'
         f'<rect x="{x+10:.0f}" y="{y+36:.0f}" width="{w_-20:.0f}"'
         f' height="{h_-20:.0f}" rx="6" fill="none" stroke="#b8a86a"'
         f' stroke-width="5"/>'
         f'<path d="M{x+30:.0f},{y+26+h_*.5:.0f} q{(w_-60)*.25:.0f},{-14:.0f}'
         f' {(w_-60)*.5:.0f},0 q{(w_-60)*.25:.0f},{14:.0f} {(w_-60)*.5:.0f},0"'
         f' fill="none" stroke="#8a7a5c" stroke-width="8"/></g>')
    return s


def _ledenec(x, y, s_=1.0, t=0.0, ph=.0):
    """Леденец на палочке: спираль двух цветов, обёртка фантиком и блик,
    который ходит по спирали."""
    r = 34 * s_
    s = (f'<rect x="{x-5*s_:.0f}" y="{y:.0f}" width="{10*s_:.0f}"'
         f' height="{86*s_:.0f}" rx="4" fill="#efe8d8" {o(3)}/>'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#f4eedc" {o(5)}/>')
    for i in range(4):
        a0 = i * 90 + 14 * A.w(t, 2.2, ph)
        s += (f'<path d="M{x:.0f},{y:.0f} A{r:.0f},{r:.0f} 0 0 1'
              f' {x+r*math.cos(math.radians(a0+60)):.0f},'
              f'{y+r*math.sin(math.radians(a0+60)):.0f} L{x:.0f},{y:.0f} Z"'
              f' fill="{KRAS}" opacity=".9"/>')
    s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="none"'
          f' stroke="{K}" stroke-width="{max(2,4*s_):.0f}"/>'
          f'<ellipse cx="{x-r*.34:.0f}" cy="{y-r*.34:.0f}" rx="{r*.22:.0f}"'
          f' ry="{r*.13:.0f}" fill="#ffffff"'
          f' opacity="{.35+.35*abs(A.w(t,1.9,ph)):.2f}"/>')
    return s


def _pianino(x, y, w_, t, h_=330, taper_igra=.0):
    """Пианино тапёра: лакированный корпус, откинутая крышка, два ряда
    клавиш с чёрными, подсвечники по бокам и педали. Клавиши проваливаются
    по ходу игры."""
    s = (f'{ten(x + w_ * .5, y + 10, w_ * .50, 18, .5)}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="10" fill="#2e2320" {o(8)}/>'
         f'<rect x="{x-14:.0f}" y="{y-h_-22:.0f}" width="{w_+28:.0f}"'
         f' height="26" rx="9" fill="#3d2f2a" {o(5)}/>'
         f'<rect x="{x+16:.0f}" y="{y-h_*.76:.0f}" width="{w_-32:.0f}"'
         f' height="{h_*.26:.0f}" rx="8" fill="#241b18" opacity=".9"/>')
    s += (f'<rect x="{x+10:.0f}" y="{y-h_*.46:.0f}" width="{w_-20:.0f}"'
          f' height="{h_*.16:.0f}" rx="6" fill="#efe8d8" {o(5)}/>')
    nk = int((w_ - 20) / 26)
    for i in range(nk):
        pr = 5 if (math.sin(t * 7 + i) > .7 and taper_igra > .3) else 0
        s += (f'<rect x="{x+12+i*26:.0f}" y="{y-h_*.46+pr:.0f}" width="22"'
              f' height="{h_*.16:.0f}" rx="3" fill="#f8f6ee" stroke="#b9b2a4"'
              f' stroke-width="3"/>')
    for i in range(nk):
        if i % 7 in (2, 6):
            continue
        s += (f'<rect x="{x+26+i*26:.0f}" y="{y-h_*.46:.0f}" width="14"'
              f' height="{h_*.10:.0f}" rx="3" fill="#1d1a18"/>')
    for i in (0, 1):
        sx = x + 40 + i * (w_ - 110)
        s += (f'<rect x="{sx:.0f}" y="{y-h_*.72:.0f}" width="18" height="34"'
              f' rx="6" fill="{ZOL}" {o(3)}/>'
              + svecha(sx + 9, y - h_ * .72, t, i * .4, .7, 60))
    for i in (0, 1):
        s += (f'<rect x="{x+w_*.40+i*60:.0f}" y="{y-34:.0f}" width="34"'
              f' height="18" rx="7" fill="{ZOL}" {o(3)}/>')
    return s


def _zatylki_ryad(x, y, w_, t, n=7, seed=5, h_baz=260, ryad=0):
    """РЯД ДЕТСКИХ ЗАТЫЛКОВ: фигуры СО СПИНЫ (lico=False) — кепки и банты.
    Рост СТРОГО ЧЕРЕЗ ОДНОГО крупный/мелкий (разница около двух раз), шаг
    рваный с перекрытиями, часть в профиль, наклон ±15°, и дети
    подпрыгивают на местах вразнобой."""
    rnd = random.Random(seed)
    s = ""
    poz = []
    for i in range(n):
        dx = x + (w_ / float(n)) * (i + rnd.uniform(-.14, .14))
        krup = (i % 2 == 0)
        hh = h_baz * (1.0 if krup else .52) * rnd.uniform(.92, 1.08)
        pryg = 14 * abs(math.sin(t * 3.4 + i * 1.1))
        pr = (i % 3 == 1)
        nak = rnd.uniform(-13, 13)
        poz.append((dx, y - pryg, hh))
        col = ["#4a5a72", "#6a5a4a", "#54505e", "#3f5c7a"][i % 4]
        s += figura(dx, y - pryg, hh, t, col=col, kant="#ffd98a",
                    platok=(i % 4 == 1), ph=i * .23, profil=pr, naklon=nak,
                    shapka=(i % 4 == 2), lico=False)
        # кепка или бант поверх затылка
        gy = y - pryg - hh * .845
        if i % 2 == 0:
            s += (f'<path d="M{dx-hh*.15:.0f},{gy:.0f} q{hh*.15:.0f},'
                  f'{-hh*.10:.0f} {hh*.30:.0f},{-hh*.01:.0f}'
                  f' q{-hh*.03:.0f},{hh*.045:.0f} {-hh*.30:.0f},{hh*.01:.0f} Z"'
                  f' fill="#3d352c" {o(4)}/>'
                  f'<path d="M{dx+hh*.13:.0f},{gy-hh*.01:.0f} q{hh*.09:.0f},'
                  f'{hh*.012:.0f} {hh*.10:.0f},{hh*.035:.0f}'
                  f' q{-hh*.06:.0f},{hh*.02:.0f} {-hh*.12:.0f},{hh*.005:.0f} Z"'
                  f' fill="#2f291f" {o(3)}/>')
        else:
            for sg in (-1, 1):
                s += (f'<path d="M{dx+sg*hh*.10:.0f},{gy-hh*.08:.0f}'
                      f' q{sg*hh*.13:.0f},{-hh*.09:.0f} {sg*hh*.15:.0f},{hh*.01:.0f}'
                      f' q{-sg*hh*.06:.0f},{hh*.05:.0f} {-sg*hh*.15:.0f},{-hh*.01:.0f} Z"'
                      f' fill="{KRAS}" {o(3)}/>')
            s += (f'<circle cx="{dx:.0f}" cy="{gy-hh*.07:.0f}" r="{hh*.03:.0f}"'
                  f' fill="{KRAS}" {o(3)}/>')
    return s, poz


def _tort_svechi(x, y, w_, t, gasnet=.0, yarusov=3):
    """ОГРОМНЫЙ ИМЕНИННЫЙ ТОРТ — главный предмет: три яруса с кремовыми
    розетками и подтёками глазури, по верхнему ярусу ЛЕС СВЕЧЕЙ, которые
    гаснут рядами и курятся дымком. Цифры на торте НЕ рисуем — её кладёт
    `kadr.py` поверх, здесь под неё оставлено чистое поле."""
    s = f'{ten(x, y + 16, w_ * .56, 26, .55)}'
    yb = y
    for i in range(yarusov):
        ww = w_ * (1.0 - i * .22)
        hh = 96 - i * 10
        s += (f'<rect x="{x-ww*.5:.0f}" y="{yb-hh:.0f}" width="{ww:.0f}"'
              f' height="{hh:.0f}" rx="16" fill="#f4e4c8" {o(7)}/>'
              f'<ellipse cx="{x:.0f}" cy="{yb-hh:.0f}" rx="{ww*.5:.0f}"'
              f' ry="{ww*.09:.0f}" fill="#fbf2de" {o(5)}/>')
        # подтёки глазури
        for j in range(int(ww / 56)):
            dx = x - ww * .5 + 24 + j * 56
            s += (f'<path d="M{dx:.0f},{yb-hh+4:.0f} q{6:.0f},{30:.0f}'
                  f' {-2:.0f},{48:.0f} q{12:.0f},{8:.0f} {18:.0f},{-6:.0f}'
                  f' q{-6:.0f},{-22:.0f} {4:.0f},{-44:.0f} Z"'
                  f' fill="#d9789c" opacity=".9" {o(3)}/>')
        # кремовые розетки по кромке
        for j in range(int(ww / 44)):
            dx = x - ww * .5 + 20 + j * 44
            s += (f'<circle cx="{dx:.0f}" cy="{yb-4:.0f}" r="13"'
                  f' fill="#fffaf0" {o(3)}/>')
        yb -= hh
    # ЛЕС СВЕЧЕЙ на верхнем ярусе, гаснут рядами
    rnd = random.Random(299)
    for r in range(3):
        for c in range(9):
            cx = x - w_ * .26 + c * (w_ * .52 / 8.0) + rnd.uniform(-6, 6)
            cy = yb + 4 + r * 16
            gor = (gasnet * 3.0) < (r + c / 9.0)
            s += (f'<rect x="{cx-5:.0f}" y="{cy-58:.0f}" width="10" height="58"'
                  f' rx="4" fill="{["#e8c64e", "#d9789c", "#8fa3c2"][c % 3]}"'
                  f' {o(3)}/>')
            if gor:
                s += (f'<ellipse cx="{cx:.0f}" cy="{cy-68:.0f}" rx="6"'
                      f' ry="{12+3*A.w(t, 1.3, c*.2):.0f}" fill="{SVET}"/>'
                      f'<ellipse cx="{cx:.0f}" cy="{cy-66:.0f}" rx="3"'
                      f' ry="7" fill="#fff6dc"/>')
            else:
                s += (f'<path d="M{cx:.0f},{cy-62:.0f} q{8:.0f},{-20:.0f}'
                      f' {-2:.0f},{-38:.0f}" fill="none" stroke="#cfd6de"'
                      f' stroke-width="5" opacity=".6"/>')
    s += teplo(x, yb - 60, 420, 300, .34)
    return s


def _kolpak_imeninnika(x, y, s_=1.0, t=0.0, ph=.0):
    """Колпак именинника на стуле: конус в полоску с кисточкой и резинкой,
    покачивается на кисточке."""
    kach = 3.0 * A.w(t, 2.4, ph)
    s = (f'<g transform="rotate({kach:.1f} {x:.0f} {y:.0f})">'
         f'{ten(x, y + 6 * s_, 54 * s_, 11 * s_, .4)}'
         f'<path d="M{x-54*s_:.0f},{y:.0f} L{x+54*s_:.0f},{y:.0f}'
         f' L{x+6*s_:.0f},{y-150*s_:.0f} Z" fill="#d9789c" {o(5)}/>')
    for i in range(4):
        s += (f'<path d="M{x-46*s_+i*8*s_:.0f},{y-i*34*s_:.0f}'
              f' L{x+46*s_-i*10*s_:.0f},{y-i*34*s_-8*s_:.0f}" fill="none"'
              f' stroke="#f4eedc" stroke-width="{max(3,8*s_):.0f}" opacity=".9"/>')
    s += (f'<circle cx="{x+6*s_:.0f}" cy="{y-158*s_:.0f}" r="{16*s_:.0f}"'
          f' fill="#e8c64e" {o(4)}/>'
          f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{54*s_:.0f}" ry="{13*s_:.0f}"'
          f' fill="#c05a80" {o(4)}/></g>')
    return s


def _shturval(x, y, s_=1.0, t=0.0):
    """Маленький рисованный штурвал: обод с восемью рукоятями, спицы,
    латунная ступица; медленно поворачивается."""
    r = 68 * s_
    ug = 10 * A.w(t, 3.2, .2)
    s = (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="none"'
         f' stroke="#8a6038" stroke-width="{16*s_:.0f}"/>'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*.22:.0f}" fill="{ZOL}"'
         f' {o(4)}/>')
    for i in range(8):
        a = math.radians(i * 45)
        s += (f'<line x1="{x+math.cos(a)*r*.2:.0f}" y1="{y+math.sin(a)*r*.2:.0f}"'
              f' x2="{x+math.cos(a)*r*.92:.0f}" y2="{y+math.sin(a)*r*.92:.0f}"'
              f' stroke="#9c7049" stroke-width="{max(3,8*s_):.0f}"/>'
              f'<path d="M{x+math.cos(a)*r*1.0:.0f},{y+math.sin(a)*r*1.0:.0f}'
              f' l{math.cos(a)*26*s_:.0f},{math.sin(a)*26*s_:.0f}" fill="none"'
              f' stroke="#7d5636" stroke-width="{max(3,11*s_):.0f}"'
              f' stroke-linecap="round"/>')
    return s + "</g>"


def _trost_nabaldashnik(x, y, s_=1.0, t=0.0, h_=300):
    """Трость с набалдашником: гнутая палка с кольцом и шаровым
    набалдашником, резиновый наконечник."""
    return (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+14*s_:.0f}"'
            f' y2="{y-h_*s_:.0f}" stroke="url(#derev)"'
            f' stroke-width="{16*s_:.0f}" stroke-linecap="round"/>'
            f'<circle cx="{x+16*s_:.0f}" cy="{y-h_*s_-14*s_:.0f}"'
            f' r="{26*s_:.0f}" fill="{ZOL}" {o(5)}/>'
            f'<ellipse cx="{x+8*s_:.0f}" cy="{y-h_*s_-22*s_:.0f}"'
            f' rx="{9*s_:.0f}" ry="{6*s_:.0f}" fill="#f2e2a0" opacity=".7"/>'
            f'<rect x="{x+4*s_:.0f}" y="{y-h_*s_+34*s_:.0f}" width="{20*s_:.0f}"'
            f' height="{12*s_:.0f}" rx="5" fill="{ZHELEZ}" {o(3)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y+4*s_:.0f}" rx="{12*s_:.0f}"'
            f' ry="{7*s_:.0f}" fill="#2a2726" {o(3)}/>')


def _meshok_zabota(x, y, s_=1.0, t=0.0, hmur=.0):
    """Серый мешок-забота: холщовый куль с завязкой и ХМУРОЙ рожицей —
    две брови вниз и опущенный рот. Рожица хмурится вслед, когда мимо
    проходят. Это нарисованный образ, а не человек."""
    w2, h2 = 120 * s_, 150 * s_
    dysh = 4 * s_ * A.w(t, 1.7, .2)
    s = (f'{ten(x, y + 8 * s_, w2 * .58, 13 * s_, .5)}'
         f'<path d="M{x-w2*.5:.0f},{y:.0f} q{-10*s_:.0f},{-h2*.72:.0f}'
         f' {w2*.26:.0f},{-h2*.86-dysh:.0f} q{w2*.24:.0f},{-14*s_:.0f}'
         f' {w2*.48:.0f},0 q{w2*.36:.0f},{h2*.16:.0f} {w2*.26:.0f},{h2*.86+dysh:.0f} Z"'
         f' fill="#8d939a" {o(7)}/>')
    for i in range(4):
        s += (f'<path d="M{x-w2*.36+i*w2*.24:.0f},{y-h2*.72:.0f}'
              f' q{8*s_:.0f},{h2*.34:.0f} {-2*s_:.0f},{h2*.64:.0f}" fill="none"'
              f' stroke="#767c82" stroke-width="{max(2,5*s_):.0f}" opacity=".8"/>')
    s += (f'<path d="M{x-w2*.24:.0f},{y-h2*.86-dysh:.0f} q{w2*.24:.0f},'
          f'{-20*s_:.0f} {w2*.48:.0f},0" fill="none" stroke="#5f656b"'
          f' stroke-width="{14*s_:.0f}"/>'
          f'<path d="M{x-w2*.14:.0f},{y-h2*.94-dysh:.0f} q{w2*.08:.0f},'
          f'{-30*s_:.0f} {w2*.10:.0f},{-44*s_:.0f}" fill="none"'
          f' stroke="#767c82" stroke-width="{max(3,9*s_):.0f}"/>')
    # ХМУРАЯ РОЖИЦА
    cy = y - h2 * .50
    for i in (-1, 1):
        s += (f'<path d="M{x+i*w2*.22-w2*.10:.0f},{cy-18*s_-10*s_*hmur:.0f}'
              f' q{w2*.10:.0f},{-10*s_-8*s_*hmur:.0f} {w2*.20:.0f},{4*s_:.0f}"'
              f' fill="none" stroke="{K}" stroke-width="{max(3,7*s_):.0f}"'
              f' stroke-linecap="round"/>')
        s += (f'<circle cx="{x+i*w2*.18:.0f}" cy="{cy:.0f}" r="{9*s_:.0f}"'
              f' fill="{K}"/>')
    s += (f'<path d="M{x-w2*.20:.0f},{cy+44*s_+8*s_*hmur:.0f}'
          f' q{w2*.20:.0f},{-20*s_-12*s_*hmur:.0f} {w2*.40:.0f},0"'
          f' fill="none" stroke="{K}" stroke-width="{max(3,8*s_):.0f}"'
          f' stroke-linecap="round"/>')
    return s


def _bidon(x, y, s_=1.0, t=0.0, ug=0.0):
    """Бидон: конусное тулово с обручем, крышка с бортиком, дуга-ручка на
    двух ушках, вмятина и блик по боку."""
    w2, h2 = 120 * s_, 170 * s_
    return (f'<g transform="rotate({ug:.1f} {x:.0f} {y:.0f})">'
            f'{ten(x, y + 8 * s_, w2 * .54, 12 * s_, .45)}'
            f'<path d="M{x-w2*.5:.0f},{y:.0f} L{x+w2*.5:.0f},{y:.0f}'
            f' L{x+w2*.34:.0f},{y-h2*.70:.0f} L{x-w2*.34:.0f},{y-h2*.70:.0f} Z"'
            f' fill="#b6bcc2" {o(6)}/>'
            f'<rect x="{x-w2*.36:.0f}" y="{y-h2*.76:.0f}" width="{w2*.72:.0f}"'
            f' height="{h2*.10:.0f}" rx="{7*s_:.0f}" fill="#9aa3aa" {o(4)}/>'
            f'<ellipse cx="{x:.0f}" cy="{y-h2*.80:.0f}" rx="{w2*.30:.0f}"'
            f' ry="{h2*.06:.0f}" fill="#cfd5da" {o(4)}/>'
            f'<circle cx="{x:.0f}" cy="{y-h2*.86:.0f}" r="{10*s_:.0f}"'
            f' fill="{ZHELEZ}" {o(3)}/>'
            f'<path d="M{x-w2*.30:.0f},{y-h2*.74:.0f} q{w2*.30:.0f},{-h2*.26:.0f}'
            f' {w2*.60:.0f},0" fill="none" stroke="{ZHELEZ}"'
            f' stroke-width="{10*s_:.0f}"/>'
            f'<rect x="{x-w2*.5:.0f}" y="{y-h2*.34:.0f}" width="{w2:.0f}"'
            f' height="{h2*.07:.0f}" fill="#8f979d" opacity=".8"/>'
            f'<path d="M{x-w2*.26:.0f},{y-h2*.58:.0f} q{10*s_:.0f},{h2*.22:.0f}'
            f' {2*s_:.0f},{h2*.42:.0f}" fill="none" stroke="#eef2f4"'
            f' stroke-width="{10*s_:.0f}" opacity=".5"/>'
            f'<ellipse cx="{x+w2*.22:.0f}" cy="{y-h2*.40:.0f}" rx="{14*s_:.0f}"'
            f' ry="{9*s_:.0f}" fill="#9aa3aa" opacity=".7"/></g>')


def _shapka_s_bumazhkami(x, y, s_=1.0, t=0.0, tyanet=.0, n=9, seed=5):
    """Шапка, полная свёрнутых бумажек: меховая шапка тульей вверх, в ней
    трубочки бумажек с нитяной перевязью; одна бумажка тянется наружу."""
    rnd = random.Random(seed)
    s = (f'{ten(x, y + 8 * s_, 96 * s_, 14 * s_, .45)}'
         f'<path d="M{x-96*s_:.0f},{y:.0f} q{6*s_:.0f},{-104*s_:.0f}'
         f' {96*s_:.0f},{-104*s_:.0f} q{90*s_:.0f},0 {96*s_:.0f},{104*s_:.0f} Z"'
         f' fill="#4a3f36" {o(7)}/>'
         f'<ellipse cx="{x:.0f}" cy="{y-100*s_:.0f}" rx="{86*s_:.0f}"'
         f' ry="{24*s_:.0f}" fill="#2f2924" {o(5)}/>'
         f'<path d="M{x-100*s_:.0f},{y-8*s_:.0f} q{100*s_:.0f},{34*s_:.0f}'
         f' {200*s_:.0f},0" fill="none" stroke="#cfc1a4"'
         f' stroke-width="{26*s_:.0f}"/>')
    for i in range(n):
        a = -2.7 + i * (2.3 / max(1, n - 1))
        bx = x + math.cos(a) * 62 * s_
        by = y - 104 * s_ - abs(math.sin(a)) * 18 * s_
        ug = math.degrees(a) + 90 + rnd.uniform(-10, 10)
        s += (f'<g transform="rotate({ug:.0f} {bx:.0f} {by:.0f})">'
              f'<rect x="{bx-9*s_:.0f}" y="{by-48*s_:.0f}" width="{18*s_:.0f}"'
              f' height="{54*s_:.0f}" rx="{8*s_:.0f}" fill="#f4eedc" {o(3)}/>'
              f'<line x1="{bx-9*s_:.0f}" y1="{by-26*s_:.0f}" x2="{bx+9*s_:.0f}"'
              f' y2="{by-26*s_:.0f}" stroke="#c9b48a"'
              f' stroke-width="{max(2,4*s_):.0f}"/></g>')
    if tyanet > .02:
        ty = y - 120 * s_ - 90 * s_ * tyanet
        s += (f'<g transform="rotate({-12:.0f} {x+20*s_:.0f} {ty:.0f})">'
              f'<rect x="{x+10*s_:.0f}" y="{ty-56*s_:.0f}" width="{22*s_:.0f}"'
              f' height="{62*s_:.0f}" rx="{9*s_:.0f}" fill="#fbf6e6" {o(4)}/>'
              f'<line x1="{x+10*s_:.0f}" y1="{ty-30*s_:.0f}"'
              f' x2="{x+32*s_:.0f}" y2="{ty-30*s_:.0f}" stroke="#c9b48a"'
              f' stroke-width="{max(2,5*s_):.0f}"/>'
              f'<path d="M{x+14*s_:.0f},{ty-14*s_:.0f} q{11*s_:.0f},{-8*s_:.0f}'
              f' {22*s_:.0f},0" fill="none" stroke="#8a7a5c"'
              f' stroke-width="{max(2,4*s_):.0f}"/></g>')
    return s


def _romashka_v_stakane(x, y, s_=1.0, t=0.0, opali=.0):
    """Ромашка в стакане с облетевшими лепестками: гранёный стакан с водой,
    стебель, цветок (берём готовую `_romashka`), а лепестки лежат на столе
    и один ещё падает."""
    s = (f'{ten(x, y + 6 * s_, 44 * s_, 10 * s_, .4)}'
         f'<path d="M{x-40*s_:.0f},{y-130*s_:.0f} L{x+40*s_:.0f},{y-130*s_:.0f}'
         f' L{x+32*s_:.0f},{y:.0f} L{x-32*s_:.0f},{y:.0f} Z"'
         f' fill="url(#stekl)" opacity=".9" {o(5)}/>'
         f'<path d="M{x-36*s_:.0f},{y-70*s_:.0f} L{x+36*s_:.0f},{y-70*s_:.0f}'
         f' L{x+32*s_:.0f},{y-4*s_:.0f} L{x-32*s_:.0f},{y-4*s_:.0f} Z"'
         f' fill="{VODA}" opacity=".45"/>')
    for i in range(3):
        s += (f'<line x1="{x-24*s_+i*24*s_:.0f}" y1="{y-126*s_:.0f}"'
              f' x2="{x-22*s_+i*22*s_:.0f}" y2="{y-8*s_:.0f}" stroke="#ffffff"'
              f' stroke-width="{max(2,4*s_):.0f}" opacity=".35"/>')
    s += (f'<line x1="{x+4*s_:.0f}" y1="{y-120*s_:.0f}" x2="{x+12*s_:.0f}"'
          f' y2="{y-240*s_:.0f}" stroke="#56763f"'
          f' stroke-width="{max(3,9*s_):.0f}"/>')
    s += _romashka(x + 12 * s_, y - 250 * s_, t, s_ * .9,
                   max(3, int(round(8 - 5 * opali))), opali, 6.0)
    rnd = random.Random(int(x) + 31)
    for i in range(6):
        lx = x + rnd.uniform(-150, 180) * s_
        ly = y + rnd.uniform(6, 26) * s_
        s += (f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{26*s_:.0f}"'
              f' ry="{11*s_:.0f}" fill="#f8f6ee"'
              f' transform="rotate({rnd.uniform(-40,40):.0f} {lx:.0f} {ly:.0f})"'
              f' {o(3)}/>')
    p = (t * .45) % 1.0
    s += (f'<ellipse cx="{x+70*s_+40*s_*p:.0f}" cy="{y-220*s_+p*210*s_:.0f}"'
          f' rx="{24*s_:.0f}" ry="{10*s_:.0f}" fill="#f8f6ee" {o(3)}'
          f' transform="rotate({p*160:.0f} {x+70*s_:.0f} {y-220*s_:.0f})"/>')
    return s


def _svadebnaya_kartochka(x, y, w_, t, prost=.0, h_=None):
    """Свадебная карточка в рамке, которая ПРОСТУПАЕТ к концу плана: резная
    рамка, карточка с двумя фигурками в профиль (невеста с фатой, он в
    пиджаке), она уже седая и улыбается; по стеклу блик дугой. Лиц крупно
    нет — только силуэты в профиль нашим же стилем."""
    if prost <= .02:
        return ""
    h_ = h_ if h_ else int(w_ * 1.22)
    op = prost
    s = (f'<g opacity="{op:.2f}">'
         f'{ten(x + w_ * .5, y + 10, w_ * .46, 14, .4)}'
         f'<rect x="{x:.0f}" y="{y-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}"'
         f' rx="10" fill="#8a6038" {o(6)}/>'
         f'<rect x="{x+20:.0f}" y="{y-h_+20:.0f}" width="{w_-40:.0f}"'
         f' height="{h_-40:.0f}" rx="6" fill="#efe8d8" {o(4)}/>')
    for i in range(4):
        s += (f'<path d="M{x+8:.0f},{y-h_+22+i*(h_-44)/4.0:.0f}'
              f' q{14:.0f},{-12:.0f} {0:.0f},{-24:.0f}" fill="none"'
              f' stroke="#a97a4e" stroke-width="5" opacity=".8"/>')
    cx = x + w_ * .5
    by = y - 40
    for i, (dx, hh, fata) in enumerate(((-w_ * .16, h_ * .60, True),
                                        (w_ * .16, h_ * .66, False))):
        col = "#cfc9bc" if fata else "#3f4a58"
        s += (f'<path d="M{cx+dx-hh*.14:.0f},{by:.0f}'
              f' q{hh*.14:.0f},{-hh*.10:.0f} {hh*.28:.0f},0'
              f' L{cx+dx+hh*.17:.0f},{by-hh*.56:.0f}'
              f' L{cx+dx-hh*.17:.0f},{by-hh*.56:.0f} Z" fill="{col}" {o(4)}/>'
              f'<circle cx="{cx+dx:.0f}" cy="{by-hh*.70:.0f}" r="{hh*.13:.0f}"'
              f' fill="#e8d8c0" {o(4)}/>')
        if fata:
            s += (f'<path d="M{cx+dx-hh*.16:.0f},{by-hh*.72:.0f}'
                  f' q{hh*.16:.0f},{-hh*.22:.0f} {hh*.32:.0f},0'
                  f' q{hh*.06:.0f},{hh*.40:.0f} {-hh*.04:.0f},{hh*.52:.0f}'
                  f' q{-hh*.28:.0f},{-hh*.10:.0f} {-hh*.28:.0f},{-hh*.52:.0f} Z"'
                  f' fill="#f4f8fa" opacity=".82" {o(3)}/>'
                  f'<path d="M{cx+dx-hh*.11:.0f},{by-hh*.78:.0f}'
                  f' q{hh*.11:.0f},{-hh*.07:.0f} {hh*.22:.0f},0" fill="none"'
                  f' stroke="#e8eef6" stroke-width="{hh*.030:.0f}"/>')
        else:
            s += (f'<path d="M{cx+dx-hh*.12:.0f},{by-hh*.80:.0f}'
                  f' q{hh*.12:.0f},{-hh*.08:.0f} {hh*.24:.0f},0" fill="none"'
                  f' stroke="#9aa3aa" stroke-width="{hh*.034:.0f}"/>')
        # улыбка в профиль — короткая дуга, без лица крупно
        s += (f'<path d="M{cx+dx+hh*.04:.0f},{by-hh*.66:.0f}'
              f' q{hh*.05:.0f},{hh*.035:.0f} {hh*.085:.0f},{-hh*.005:.0f}"'
              f' fill="none" stroke="{K}" stroke-width="{hh*.018:.0f}"'
              f' stroke-linecap="round"/>')
    s += (f'<path d="M{x+36:.0f},{y-h_*.74:.0f} L{x+w_*.56:.0f},{y-h_*.94:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="16" opacity=".3"/>'
          f'<path d="M{x+20:.0f},{y-30:.0f} q{w_*.5-20:.0f},{-18:.0f}'
          f' {w_-40:.0f},0" fill="none" stroke="#c9b48a" stroke-width="6"/>'
          f'</g>')
    return s


# ── ДЕКОРАЦИИ, ЧЕТВЁРТАЯ ПАРТИЯ ───────────────────────────────────────────

def televizor_na_nozhkah_i_portret(t):
    """Комната: телевизор на тонких ножках с выпуклым экраном крупно, на нём
    салфетка и ваза, рядом торшер, кресло, ёлочная ветка в банке. На экране
    настоящий портрет. Бабушка сидит в кресле и обеими руками держит
    вязание, внучка на ковре у телевизора правой рукой показывает на экран,
    левой опирается о ковёр."""
    rnd = random.Random(907)
    pol = 1012
    s = f'<rect width="{W}" height="{H}" fill="#2b241e"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{pol:.0f}"'
                   f' fill="#6a5a46"/>'
            + "".join(f'<line x1="{40+i*86:.0f}" y1="0" x2="{40+i*86:.0f}"'
                      f' y2="{pol:.0f}" stroke="#5a4a38" stroke-width="7"'
                      f' opacity=".6"/>' for i in range(23)))
    s += SL(Z_DAL, kvartira_veschi(1300, 170, 600, t, 909))
    s += SL(Z_DAL, _kover_na_stene(80, 150, 620, 380, t, 911))
    s += SL(Z_DAL, _ramki_na_stene(760, 130, 420, t, 913, 3))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}" height="{H-pol+18:.0f}"'
                   f' fill="#7a6248"/>' + polovicy(pol + 14)
            + _pol_shvy(pol + 16, 1074, 915, 6, "#5e4a34"))
    s += SL(Z_SRED, _polovik(820, pol + 36, 980, 150, "#8a4a5c", "#5a2c3c"))
    # ГЛАВНЫЙ ПРЕДМЕТ: телевизор на ножках, на экране настоящий портрет
    tx, ty, tw = 620, pol - 150, 680
    s += SL(Z_SRED, _televizor_nozhki(tx, ty, tw, t, 430))
    px, py, pw, ph_ = tx + 44, ty - 400, 780, 330
    px, py = tx - 10, ty - 400
    pw, ph_ = 780, 330
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<path d="{put}" fill="#2a3038"/>'
           f'<ellipse cx="{px+pw*.5:.0f}" cy="{py+ph_*.52:.0f}"'
           f' rx="{pw*.30:.0f}" ry="{ph_*.34:.0f}" fill="#54606a" opacity=".9"/>'
           f'<ellipse cx="{px+pw*.5:.0f}" cy="{py+ph_*.34:.0f}"'
           f' rx="{pw*.13:.0f}" ry="{ph_*.17:.0f}" fill="#8a929a" opacity=".85"/>')
    for i in range(6):
        vid += (f'<rect x="{px+20:.0f}" y="{py+30+i*48:.0f}" width="{pw-40:.0f}"'
                f' height="{14:.0f}" fill="#cfd6de"'
                f' opacity="{.10+.08*abs(A.w(t,1.7,i*.3)):.2f}"/>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    # обвязка поверх: выпуклое стекло и скруглённая рамка кинескопа
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#5b4428"'
                    f' stroke-width="44"/>'
            + f'<path d="{put}" fill="none" stroke="#8a6038" stroke-width="16"/>'
            + f'<path d="M{px+70:.0f},{py+60:.0f} Q{px+pw*.34:.0f},{py+20:.0f}'
              f' {px+pw*.56:.0f},{py+52:.0f}" fill="none" stroke="#ffffff"'
              f' stroke-width="22" opacity="{.14+.08*abs(A.w(t,3.0,.2)):.2f}"/>'
            + f'<ellipse cx="{px+pw*.5:.0f}" cy="{py+ph_*.5:.0f}"'
              f' rx="{pw*.52:.0f}" ry="{ph_*.60:.0f}" fill="none"'
              f' stroke="#4a3522" stroke-width="18" opacity=".55"/>')
    # салфетка и ваза на телевизоре
    s += SL(Z_SRED, f'<ellipse cx="{tx+tw*.72:.0f}" cy="{ty-446:.0f}" rx="96"'
                    f' ry="22" fill="{KREM}" {o(5)}/>'
            + _vaza_s_yablokami(tx + tw * .72, ty - 450, 1.0, t, 917, 5))
    s += SL(Z_DAL, tusklaya_lampochka(900, 40, t, 1.05, True))
    s += SL(Z_SRED, _torsher(1480, pol, t, 1.0, 620))
    s += SL(Z_SRED, _elovaya_vetka_v_banke(240, pol - 6, 1.1, t, .3))
    s += SL(Z_SRED, _kreslo(1620, pol, 400, t, 440, "#6c5a4a"))
    s += SL(Z_SRED, _stolik(1300, pol, 260, t, 200, True))
    # ДВЕ ФИГУРЫ: бабушка в кресле и внучка на ковре
    bx, by_, bh = 1680, pol - 170, 560
    vx, vy, vh = 1060, pol + 20, 400
    _figury_kadra((bx, by_, bh), (vx, vy, vh))
    pok = A.ease(A.seg(t, .6, 1.2))
    bab = figura(bx, by_, bh, t, col="#54505e", kant="#ffd98a", platok=True,
                 ph=.3, naklon=3.0)
    r1, (k1x, k1y), _ = _ruka_mimo(bx, by_, bh, -1, bh * .34, 44, t,
                                   "#54505e", "#ffd98a", .2, 4.0)
    r2, (k2x, k2y), _ = _ruka_sgib_mimo(bx, by_, bh, -1, bh * .22, 20,
                                        bh * .22, 50, t, "#54505e",
                                        "#ffd98a", .7, 4.0)
    bab += r1 + r2
    s += SL(Z_SRED, bab)
    s += SL(Z_SRED, _vyazanie((k1x + k2x) * .5 - 30, k1y + 16, .9, t, .2))
    s += SL(Z_SRED, _varezhka(k1x, k1y + 2, bh, t, .2)
            + _varezhka(k2x, k2y + 2, bh, t, .7))
    vnu = figura(vx, vy, vh, t, col="#b8323a", kant="#ffd98a", ph=.7,
                 naklon=5.0)
    p1, (m1x, m1y), _ = _ruka_mimo(vx, vy, vh, -1, vh * .48, 6 - 18 * pok, t,
                                   "#b8323a", "#ffd98a", .1, 5.0)
    p2, (m2x, m2y), _ = _ruka_mimo(vx, vy, vh, 1, vh * .40, 56, t,
                                   "#b8323a", "#ffd98a", .5, 3.0)
    vnu += p1 + p2
    s += SL(Z_SRED, vnu)
    # поджатые ноги на ковре: опора названа, ступни видны из-под подола
    s += SL(Z_SRED, f'<path d="M{vx-vh*.22:.0f},{vy-vh*.05:.0f}'
                    f' q{vh*.22:.0f},{vh*.06:.0f} {vh*.44:.0f},0'
                    f' q{-vh*.10:.0f},{vh*.05:.0f} {-vh*.44:.0f},0 Z"'
                    f' fill="#8fa3c2" {o(4)}/>')
    # показывающая кисть: предмета нет, варежки нет — рукав без кисти
    s += SL(Z_SRED, f'<path d="M{m1x-22:.0f},{m1y-14:.0f} q{26:.0f},{-12:.0f}'
                    f' {46:.0f},{6:.0f}" fill="none" stroke="#ffd98a"'
                    f' stroke-width="7" opacity=".3"/>')
    s += SL(Z_SRED, _varezhka(m2x, m2y + 2, vh, t, .5))
    # нижняя треть
    s += SL(Z_SRED, _kot_zhivoy(400, pol + 54, t, 1.1, "#3b3430", .3, True, True)
            + _dvorovaya_utvar(120, pol + 52, 210, t, 919, ["korzina"])
            + _yaschiki(1880, pol + 16, t, 921, 2, .76)
            + _ploshka_s_meloch(1320, pol - 196, t, .9, 6, 923))
    s += SL(Z_SRED, teplo(1480, pol - 600, 460, 380, .34))
    s += SL(Z_PERED, _stolb_pered(-8, 104, "#1a140e", 0, H))
    s += vinetka(.44)
    return s


def chetyre_afishi_u_kinoteatra(t):
    """Афишная стена кинотеатра: четыре рисованные афиши в ряд, на каждой
    крупный предмет вместо лиц — часы с лентами и конфетти, пишущая машинка
    с очками, два саквояжа на перроне под вокзальными часами, банный веник с
    ёлочной игрушкой. Расклейщик в кепке на стремянке левой рукой держит
    край четвёртой афиши, правой разглаживает её щёткой. Внизу ведёрко с
    клеем, урна, голуби. СВОИХ БУКВ НЕТ: названия кладёт `kadr.py`."""
    rnd = random.Random(929)
    pol = 1010
    s = f'<rect width="{W}" height="{H}" fill="#3a3630"/>'
    s += SL(Z_DAL, kladka(0, 0, 1920, 820, 82, "#6a5c4c"))
    s += SL(Z_DAL, f'<rect x="0" y="820" width="{W}" height="42" rx="8"'
                   f' fill="#5e5244" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}"'
                   f' height="{H-pol+18:.0f}" fill="#7a7268"/>'
            + _asfalt(pol - 10, 1076, 931, 12))
    # ЧЕТЫРЕ АФИШИ, подсвечиваются по очереди
    vidy = ("chasy", "mashinka", "sakvoyazhi", "venik")
    for i, vid in enumerate(vidy):
        faza = ((t * .45 + i * .25) % 1.0)
        podsvet = max(0.0, 1.0 - abs(faza - .5) * 4)
        s += SL(Z_SRED, _afisha(60 + i * 460, 180, 420, 600, t, vid,
                                podsvet, 933 + i * 2))
    s += SL(Z_SRED, _naves_lampochki(210, 80, 1500, t, 14, 64))
    # РАСКЛЕЙЩИК на стремянке у четвёртой афиши
    s += SL(Z_SRED, _stremyanka(1560, 640, 380, t, 4))
    rx_, ry_, rh = 1560, 690, 560
    _figury_kadra((rx_, ry_, rh))
    gl = A.w(t, 1.1, .2)
    rask = figura(rx_, ry_, rh, t, col="#4e5a46", kant="#ffd98a", ph=.3,
                  naklon=4.0)
    a1, (c1x, c1y), _ = _ruka_mimo(rx_, ry_, rh, -1, rh * .40, -18, t,
                                   "#4e5a46", "#ffd98a", .2, 4.0)
    a2, (c2x, c2y), _ = _ruka_mimo(rx_, ry_, rh, -1, rh * .34,
                                   16 + 26 * gl, t, "#4e5a46", "#ffd98a",
                                   .7, 7.0)
    rask += a1 + a2
    s += SL(Z_SRED, rask)
    # КЕПКА расклейщика поверх убора
    gy_ = ry_ - rh * .845
    s += SL(Z_SRED, f'<path d="M{rx_-rh*.10:.0f},{gy_-rh*.085:.0f}'
                    f' q{rh*.10:.0f},{-rh*.075:.0f} {rh*.20:.0f},{-rh*.008:.0f}'
                    f' q{-rh*.02:.0f},{rh*.04:.0f} {-rh*.20:.0f},{rh*.008:.0f} Z"'
                    f' fill="#3d352c" {o(5)}/>'
            + f'<path d="M{rx_-rh*.12:.0f},{gy_-rh*.078:.0f} q{-rh*.05:.0f},'
              f'{rh*.012:.0f} {-rh*.055:.0f},{rh*.032:.0f}'
              f' q{rh*.05:.0f},{rh*.006:.0f} {rh*.08:.0f},{-rh*.014:.0f} Z"'
              f' fill="#2f291f" {o(3)}/>')
    # край афиши в левой кисти и ЩЁТКА в правой
    s += SL(Z_SRED, f'<path d="M{c1x:.0f},{c1y-40:.0f} L{c1x-90:.0f},{c1y-60:.0f}'
                    f' L{c1x-86:.0f},{c1y+40:.0f} L{c1x+4:.0f},{c1y+28:.0f} Z"'
                    f' fill="#3f5a3a" {o(4)}/>')
    s += SL(Z_SRED, _varezhka(c1x, c1y + 2, rh, t, .2))
    s += SL(Z_SRED, para_izo_rta(rx_ - 40, gy_ + 12, t, .4, 1.0, .5))
    s += SL(Z_SRED, _schetka_oboynaya(c2x - 40, c2y + 10, 1.0, -74, t))
    s += SL(Z_SRED, _varezhka(c2x, c2y + 4, rh, t, .7))
    # внизу ведёрко с клеем, урна, голуби
    s += SL(Z_SRED, _vederko_kleya(1420, pol + 6, 1.05, t, True))
    s += SL(Z_SRED, _gorodskoy_hlam(240, pol + 6, 300, t, 941,
                                    ["urna", "yaschik"]))
    for i, (gx_, gs, gp, hod) in enumerate(((700, 1.3, .0, True),
                                            (820, .68, .3, False),
                                            (960, 1.15, .6, True))):
        s += SL(Z_SRED, _golub(gx_, pol + 46 - i * 4, t, gs, gp, hod))
    s += SL(Z_SRED, _kucha_listev(1180, pol + 50, 260, 943, 62)
            + _luzha(520, pol + 56, 210, t, .3)
            + _skameyka_podezda(1700, pol + 6, 240, t, 150))
    s += SL(Z_SRED, teplo(960, 160, 820, 260, .26))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 945, .40, 1.3))
    s += SL(Z_PERED, _stolb_pered(-8, 112, "#241f18", 0, H))
    s += vinetka(.42)
    return s


def zhenschina_s_mandarinami_i_sneg(t):
    """Зимний вечер, двор у подъезда: фонарь, скамейка в снегу, новогодние
    огоньки в окнах. Женщина в пальто и пуховом платке идёт к подъезду — в
    правой руке сетка с мандаринами, левой поправляет платок. У подъезда
    мужчина в шапке-пирожке: в левой портфель, правой неловко протягивает
    ей оброненную варежку. Она останавливается и улыбается, у калитки позади
    блестит монетка."""
    rnd = random.Random(947)
    pol = 1016
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 949)
    # панельные дома с новогодними огоньками
    s += SL(Z_DAL, panelka(-60, 740, 1010, t, 6, True, 951)
            + panelka(1060, 720, 920, t, 6, True, 953))
    for i in range(16):
        ox_ = 60 + (i % 8) * 230
        oy_ = 300 + (i // 8) * 160
        mig = .3 + .7 * abs(A.w(t, 1.2 + i * .06, i * .4))
        s += SL(Z_DAL, "".join(
            f'<circle cx="{ox_+j*26:.0f}" cy="{oy_+8*math.sin(j+i):.0f}" r="8"'
            f' fill="{["#e8c64e", "#d6452a", "#56763f", "#cfe4f5"][j % 4]}"'
            f' opacity="{mig:.2f}"/>' for j in range(6)))
    # подъезд с козырьком
    s += SL(Z_SRED, f'<rect x="1300" y="470" width="520" height="{pol-470:.0f}"'
                    f' rx="10" fill="{BETON2}" {o(6)}/>'
            + f'<rect x="1260" y="430" width="600" height="56" rx="12"'
              f' fill="{BETON}" {o(5)}/>'
            + dver(1420, 560, 300, pol - 560, .0, "#5a4530", True, False)
            + f'<rect x="1500" y="470" width="140" height="70" rx="10"'
              f' fill="{SVET}" opacity="{.6+.2*abs(A.w(t,2.6,.2)):.2f}"/>')
    s += SL(Z_SRED, _fonar_dvorovoy(880, pol - 10, t, 1.0, 620))
    # земля в снегу, скамейка, следы
    s += SL(Z_SRED, f'<rect x="0" y="{pol-20:.0f}" width="{W}"'
                    f' height="{H-pol+20:.0f}" fill="#6a7280"/>'
            + sneg_lezhit(pol + 10, 30)
            + _inej(955, 26, pol + 20, 1070))
    s += SL(Z_SRED, _skameyka_podezda(380, pol + 4, 330, t, 160))
    s += SL(Z_SRED, f'<path d="M370,{pol-110:.0f} q170,-34 330,-6'
                    f' q-10,36 -330,30 Z" fill="url(#sneg)" opacity=".92"/>')
    s += SL(Z_SRED, _sledy(200, 1070, 1160, pol - 10, 8, 957, "#4e5664", 1.1))
    # МОНЕТКА у калитки далеко позади
    s += SL(Z_SRED, _zabor_dosok(-30, pol - 230, 360, 210, 959, 54))
    s += SL(Z_SRED, _moneta_krupno(150, pol - 44, 34, t, .2, True, False, .8))
    s += SL(Z_SRED, f'<circle cx="150" cy="{pol-44:.0f}" r="56" fill="{SVET}"'
                    f' opacity="{.14+.14*abs(A.w(t,1.6,.3)):.2f}"/>')
    # ДВЕ ФИГУРЫ: женщина идёт, мужчина протягивает варежку
    hod = A.ease(A.seg(t, .3, 3.0))
    zx = 620 + 180 * hod
    zy, zh = pol + 2, 760
    mx, my, mh = 1340, pol + 2, 780
    _figury_kadra((zx, zy, zh), (mx, my, mh))
    prot = A.ease(A.seg(t, 1.6, 1.6))
    ulyb = A.ease(A.seg(t, 3.4, 1.2))
    zhen = figura(zx, zy, zh, t, col="#54505e", kant="#cfe4f5", platok=True,
                  ph=.3, naklon=3.0 - 1.5 * ulyb)
    r1, (n1x, n1y), _ = _ruka_mimo(zx, zy, zh, 1, zh * .34, 48, t,
                                   "#54505e", "#cfe4f5", .2, 5.0)
    r2, (n2x, n2y), _ = _ruka_so_sgibom(zx, zy, zh, -1, zh * .20, -30,
                                        zh * .18, -52, t, "#54505e",
                                        "#cfe4f5", .7, 4.0)
    zhen += r1 + r2
    s += SL(Z_SRED, zhen)
    # ПУХОВЫЙ ПЛАТОК пушистой кромкой и улыбка уголком
    gyz = zy - zh * .845
    s += SL(Z_SRED, "".join(
        f'<circle cx="{zx+math.cos(math.radians(a)) * zh * .160:.0f}"'
        f' cy="{gyz+math.sin(math.radians(a)) * zh * .160:.0f}"'
        f' r="{zh*.020:.0f}" fill="#e8e2d6" opacity=".9"/>'
        for a in range(150, 391, 22)))
    s += SL(Z_SRED, f'<path d="M{zx-zh*.03:.0f},{gyz+zh*.040:.0f}'
                    f' q{zh*.03:.0f},{zh*.012+zh*.012*ulyb:.0f}'
                    f' {zh*.06:.0f},{-zh*.004*ulyb:.0f}" fill="none"'
                    f' stroke="{K}" stroke-width="{zh*.009:.0f}"'
                    f' stroke-linecap="round"/>')
    s += SL(Z_SRED, _setka_mandarinov(n1x + 20, n1y + 30, 1.0, t, .3, 7))
    s += SL(Z_SRED, _varezhka(n1x, n1y + 4, zh, t, .2))
    s += SL(Z_SRED, para_izo_rta(zx + 36, gyz + 12, t, .4, 1.0, .55))
    muzh = figura(mx, my, mh, t, col="#3f4a58", kant="#cfe4f5", ph=.7,
                  naklon=4.0)
    p1, (q1x, q1y), _ = _ruka_mimo(mx, my, mh, -1, mh * .30, 50, t,
                                   "#3f4a58", "#cfe4f5", .1, 4.0)
    p2, (q2x, q2y), _ = _ruka_mimo(mx, my, mh, -1, mh * .42,
                                   34 - 30 * prot, t, "#3f4a58",
                                   "#cfe4f5", .6, 5.0)
    muzh += p1 + p2
    s += SL(Z_SRED, muzh)
    # ШАПКА-ПИРОЖОК поверх убора
    gym = my - mh * .845
    s += SL(Z_SRED, f'<path d="M{mx-mh*.105:.0f},{gym-mh*.055:.0f}'
                    f' L{mx+mh*.105:.0f},{gym-mh*.055:.0f}'
                    f' L{mx+mh*.095:.0f},{gym-mh*.135:.0f}'
                    f' L{mx-mh*.095:.0f},{gym-mh*.135:.0f} Z" fill="#3d352c"'
                    f' {o(5)}/>'
            + f'<ellipse cx="{mx:.0f}" cy="{gym-mh*.135:.0f}"'
              f' rx="{mh*.095:.0f}" ry="{mh*.020:.0f}" fill="#4a4036" {o(3)}/>')
    s += SL(Z_SRED, _portfel(q1x - 40, q1y + 110, .82, t, -8))
    s += SL(Z_SRED, _varezhka(q1x, q1y + 6, mh, t, .1))
    # ОБРОНЕННАЯ ВАРЕЖКА, которую он протягивает: лежит в кисти внахлёст
    s += SL(Z_SRED, f'<g transform="rotate({-18 + 10 * prot:.1f} {q2x:.0f} {q2y:.0f})">'
                    f'<path d="M{q2x-54:.0f},{q2y-6:.0f} q{-8:.0f},{-46:.0f}'
                    f' {30:.0f},{-52:.0f} q{44:.0f},{-4:.0f} {52:.0f},{34:.0f}'
                    f' q{6:.0f},{26:.0f} {-16:.0f},{30:.0f} Z" fill="#b8323a"'
                    f' {o(5)}/>'
                    f'<path d="M{q2x-50:.0f},{q2y-16:.0f} q{52:.0f},{-16:.0f}'
                    f' {96:.0f},{6:.0f}" fill="none" stroke="#efe3c8"'
                    f' stroke-width="11"/>'
                    f'<path d="M{q2x+36:.0f},{q2y-40:.0f} q{26:.0f},{-6:.0f}'
                    f' {30:.0f},{14:.0f} q{-16:.0f},{14:.0f} {-34:.0f},{6:.0f} Z"'
                    f' fill="#b8323a" {o(4)}/></g>')
    s += SL(Z_SRED, _varezhka(q2x, q2y + 4, mh, t, .6))
    s += SL(Z_SRED, para_izo_rta(mx - 38, gym + 12, t, .8, 1.0, .5))
    # нижняя треть
    s += SL(Z_SRED, _gorodskoy_hlam(1760, pol + 6, 160, t, 961, ["urna"])
            + _snegovik(240, pol + 20, .66, t)
            + _kot_zhivoy(1060, pol + 46, t, 1.0, "#3b3430", .4))
    s += SL(Z_LETIT, mokryy_sneg(t, 44, 963, .78, .7))
    s += SL(Z_SRED, teplo(946, pol - 640, 420, 360, .36))
    s += SL(Z_PERED, _vetka_pered(-40, 140, 520, 22, t, 965, "#141017", 6))
    s += vinetka(.46)
    return s


def kassa_starogo_kinoteatra(t):
    """Фасад кинотеатра двадцатых: навес с бегущими лампочками, окошко кассы
    крупно, рулон билетов, табличка с годом (поле под год пустое — цифры
    кладёт `kadr.py`). Кассирша в шляпке-колоколе правой рукой отрывает
    билет, левой придерживает рулон. Мальчик в кепке-восьмиклинке стоит на
    цыпочках и правой кладёт на блюдце монетку, левой держит леденец."""
    rnd = random.Random(967)
    pol = 1012
    s = f'<rect width="{W}" height="{H}" fill="#2a2420"/>'
    s += SL(Z_DAL, kladka(0, 0, 1920, 860, 84, "#7a6a56"))
    s += SL(Z_DAL, f'<rect x="0" y="856" width="{W}" height="40" rx="8"'
                   f' fill="#6a5c4c" {o(5)}/>')
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}"'
                   f' height="{H-pol+18:.0f}" fill="#8a7f70"/>'
            + _bulyzhnik(pol - 10, 1076, 969, 84))
    s += SL(Z_SRED, _naves_lampochki(200, 110, 1520, t, 14, 66))
    # пилястры фасада по краям — ближний объём
    for px in (60, 1740):
        s += SL(Z_SRED, f'<rect x="{px:.0f}" y="190" width="120"'
                        f' height="{pol-190:.0f}" rx="8" fill="#8a7a66" {o(6)}/>'
                + "".join(f'<line x1="{px+22+i*26:.0f}" y1="220"'
                          f' x2="{px+22+i*26:.0f}" y2="{pol-20:.0f}"'
                          f' stroke="#6a5c4c" stroke-width="7" opacity=".7"/>'
                          for i in range(4)))
    # ГЛАВНЫЙ ПРЕДМЕТ: окошко кассы
    otryv = A.ease(A.seg(t, .5, 1.2))
    s += SL(Z_SRED, _okoshko_kassy(620, 330, 620, 400, t, otryv))
    s += SL(Z_SRED, _tablichka_bez_cifr(1340, 330, 300, 150, t, .2))
    s += SL(Z_SRED, _afisha(220, 330, 330, 470, t, "chasy", .4, 971))
    # ДВЕ ФИГУРЫ: кассирша в окошке и мальчик перед ним
    kx, ky, kh = 980, 1050, 620
    bx, by_, bh = 1480, pol, 430
    _figury_kadra((kx, ky, kh), (bx, by_, bh))
    cyp = A.ease(A.seg(t, .8, 1.0))
    kass = figura(kx, ky, kh, t, col="#8a4a5c", kant="#ffd98a", ph=.3,
                  naklon=3.0)
    a1, (d1x, d1y), _ = _ruka_mimo(kx, ky, kh, 1, kh * .34, 42 - 14 * otryv, t,
                                   "#8a4a5c", "#ffd98a", .2, 4.0)
    a2, (d2x, d2y), _ = _ruka_mimo(kx, ky, kh, -1, kh * .30, 48, t,
                                   "#8a4a5c", "#ffd98a", .7, 4.0)
    kass += a1 + a2
    s += SL(Z_SRED, kass)
    # ШЛЯПКА-КОЛОКОЛ поверх убора
    gyk = ky - kh * .845
    s += SL(Z_SRED, f'<path d="M{kx-kh*.11:.0f},{gyk+kh*.012:.0f}'
                    f' q{-kh*.012:.0f},{-kh*.13:.0f} {kh*.11:.0f},{-kh*.14:.0f}'
                    f' q{kh*.12:.0f},{kh*.01:.0f} {kh*.11:.0f},{kh*.14:.0f}'
                    f' q{-kh*.11:.0f},{kh*.03:.0f} {-kh*.22:.0f},0 Z"'
                    f' fill="#5a2c3c" {o(5)}/>'
            + f'<path d="M{kx-kh*.085:.0f},{gyk-kh*.055:.0f} q{kh*.085:.0f},'
              f'{kh*.016:.0f} {kh*.17:.0f},0" fill="none" stroke="{ZOL}"'
              f' stroke-width="{kh*.016:.0f}"/>')
    s += SL(Z_SRED, _varezhka(d1x, d1y + 2, kh, t, .2)
            + _varezhka(d2x, d2y + 2, kh, t, .7))
    # мальчик на цыпочках
    mal = figura(bx, by_ - 16 * cyp, bh, t, col="#4a5a72", kant="#ffd98a",
                 ph=.7, naklon=4.0)
    p1, (e1x, e1y), _ = _ruka_mimo(bx, by_ - 16 * cyp, bh, -1, bh * .46,
                                   -16 - 14 * cyp, t, "#4a5a72",
                                   "#ffd98a", .1, 5.0)
    p2, (e2x, e2y), _ = _ruka_mimo(bx, by_ - 16 * cyp, bh, 1, bh * .34, 46, t,
                                   "#4a5a72", "#ffd98a", .6, 4.0)
    mal += p1 + p2
    s += SL(Z_SRED, mal)
    # КЕПКА-ВОСЬМИКЛИНКА поверх убора: клинья сходятся к пуговке
    gyb = by_ - 16 * cyp - bh * .845
    s += SL(Z_SRED, f'<path d="M{bx-bh*.115:.0f},{gyb-bh*.055:.0f}'
                    f' q{bh*.115:.0f},{-bh*.10:.0f} {bh*.23:.0f},{-bh*.008:.0f}'
                    f' q{-bh*.02:.0f},{bh*.05:.0f} {-bh*.23:.0f},{bh*.008:.0f} Z"'
                    f' fill="#3f4a58" {o(5)}/>'
            + "".join(f'<line x1="{bx:.0f}" y1="{gyb-bh*.095:.0f}"'
                      f' x2="{bx+bh*.115*math.cos(math.radians(a)):.0f}"'
                      f' y2="{gyb-bh*.05+bh*.03*math.sin(math.radians(a)):.0f}"'
                      f' stroke="#2f3a48" stroke-width="{bh*.009:.0f}"/>'
                      for a in range(160, 381, 28))
            + f'<circle cx="{bx:.0f}" cy="{gyb-bh*.098:.0f}" r="{bh*.015:.0f}"'
              f' fill="#2f3a48" {o(3)}/>')
    # ЦЫПОЧКИ: пятки приподняты, носки на мостовой — опора названа
    s += SL(Z_SRED, "".join(
        f'<path d="M{bx+i*bh*.09-bh*.045:.0f},{by_-bh*.02:.0f}'
        f' q{bh*.045:.0f},{bh*.03:.0f} {bh*.09:.0f},{-bh*.005:.0f}'
        f' l{0:.0f},{bh*.02:.0f} l{-bh*.09:.0f},0 Z" fill="#3b2f26" {o(3)}/>'
        for i in (-1, 1)))
    # МОНЕТКА ложится на блюдце, ЛЕДЕНЕЦ в другой кисти
    s += SL(Z_SRED, _moneta_krupno(e1x - 10, e1y + 24 + 18 * cyp, 26, t, .3,
                                   True, True, .5))
    s += SL(Z_SRED, _varezhka(e1x, e1y + 4, bh, t, .1))
    s += SL(Z_SRED, para_izo_rta(bx + 34, gyb + 14, t, .5, .9, .5))
    s += SL(Z_SRED, _ledenec(e2x + 26, e2y - 36, .92, t, .4))
    s += SL(Z_SRED, _varezhka(e2x, e2y + 4, bh, t, .6))
    # нижняя треть
    s += SL(Z_SRED, _gorodskoy_hlam(300, pol + 6, 280, t, 973,
                                    ["urna", "yaschik"])
            + _golub(760, pol + 46, t, 1.2, .2, True)
            + _golub(860, pol + 52, t, .66, .6, False)
            + _kucha_listev(1700, pol + 48, 240, 975, 60)
            + _luzha(1180, pol + 54, 200, t, .3))
    s += SL(Z_SRED, teplo(960, 190, 820, 280, .30))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 977, .40, 1.2))
    s += SL(Z_PERED, _stolb_pered(1898, 108, "#1d1812", 0, H))
    s += vinetka(.44)
    return s


def ekran_s_parohodom(t):
    """Зал того же кинотеатра: белый экран крупно, на нём настоящий кадр со
    старинным колёсным пароходом. Перед экраном тапёр за пианино — обе руки
    на клавишах, — и ряды детских затылков в кепках и бантах: дети
    подпрыгивают на местах. Самого персонажа в кадре нет."""
    rnd = random.Random(977)
    pol = 1014
    s = f'<rect width="{W}" height="{H}" fill="#170f12"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{pol:.0f}"'
                   f' fill="#2a1820"/>'
            + kladka(0, 30, 420, 640, 74, "#4a2a34")
            + kladka(1500, 30, 420, 640, 74, "#4a2a34"))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-16:.0f}" width="{W}"'
                   f' height="{H-pol+16:.0f}" fill="#3a2028"/>'
            + _pol_shvy(pol - 6, 1074, 979, 6, "#2a151c"))
    # НАСТОЯЩИЙ КАДР на экране: рисованный вид, метка, обвязка поверх
    px, py, pw, ph_ = 500, 110, 920, 430
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<path d="{put}" fill="#8a8f92"/>'
           f'<rect x="{px:.0f}" y="{py+ph_*.60:.0f}" width="{pw:.0f}"'
           f' height="{ph_*.40:.0f}" fill="#6a7276"/>')
    hod = (t * 36.0) % (pw + 300) - 150
    vid += (f'<path d="M{px+hod:.0f},{py+ph_*.70:.0f} l{300:.0f},0'
            f' l{-30:.0f},{70:.0f} l{-240:.0f},0 Z" fill="#3d4246" {o(5)}/>'
            f'<rect x="{px+hod+60:.0f}" y="{py+ph_*.48:.0f}" width="{180:.0f}"'
            f' height="{ph_*.22:.0f}" rx="6" fill="#55595c" {o(4)}/>'
            f'<circle cx="{px+hod+150:.0f}" cy="{py+ph_*.78:.0f}" r="42"'
            f' fill="none" stroke="#2f3336" stroke-width="12"/>')
    for i in (0, 1):
        vid += (f'<rect x="{px+hod+90+i*70:.0f}" y="{py+ph_*.22:.0f}"'
                f' width="26" height="{ph_*.28:.0f}" rx="5" fill="#2f3336"/>')
        vid += dym(px + hod + 103 + i * 70, py + ph_ * .20, t, 4, .30, 200,
                   .34, "#b9c0c4", 1.2)
    for i in range(5):
        vid += (f'<path d="M{px+40:.0f},{py+ph_*(.84+i*.03):.0f}'
                f' q{pw*.25:.0f},{-8 - 5 * A.w(t, 1.6, i * .3):.0f}'
                f' {pw*.46:.0f},0 q{pw*.22:.0f},{8:.0f} {pw*.42:.0f},{-4:.0f}"'
                f' fill="none" stroke="#9aa3a8" stroke-width="7" opacity=".6"/>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#d8d2c4"'
                    f' stroke-width="30"/>'
            + "".join(f'<circle cx="{px+24+i*(pw-48)/13.0:.0f}" cy="{py+6:.0f}"'
                      f' r="6" fill="#9aa3aa"/>' for i in range(14))
            + "".join(f'<circle cx="{px+24+i*(pw-48)/13.0:.0f}"'
                      f' cy="{py+ph_-6:.0f}" r="6" fill="#9aa3aa"/>'
                      for i in range(14)))
    for e, sg in ((px - 20, -1), (px + pw + 20, 1)):
        for i in range(5):
            s += SL(Z_SRED, f'<path d="M{e+sg*i*36:.0f},{py-40:.0f}'
                            f' q{sg*28:.0f},{ph_*.5:.0f} {sg*4:.0f},{ph_+60:.0f}'
                            f' l{sg*34:.0f},0 q{sg*22:.0f},{-ph_*.5:.0f}'
                            f' {-sg*2:.0f},{-ph_-60:.0f} Z" fill="#3a1e26"'
                            f' opacity="{.9-i*.09:.2f}" {o(3)}/>')
    # ЛУЧ ПРОЕКТОРА дрожит
    s += SL(Z_LETIT, f'<g transform="rotate({8 + .8 * A.w(t, 9.0, .2):.1f}'
                     f' 1820 240)">'
            + _konus_sveta(1820, 240, 520, 740, 0.0, .26, "#ffd98a") + "</g>")
    rnd2 = random.Random(981)
    for i in range(22):
        p = ((t * .24 + rnd2.random()) % 1.0)
        s += SL(Z_LETIT, f'<circle cx="{1760-p*900+rnd2.uniform(-60,60):.0f}"'
                         f' cy="{300+p*380+rnd2.uniform(-60,60):.0f}"'
                         f' r="{rnd2.uniform(2.5,5.5):.0f}" fill="#ffeec2"'
                         f' opacity="{.22+.4*abs(A.w(t,1.6,i*.2)):.2f}"/>')
    # ПИАНИНО и ТАПЁР — главный человек плана, обе руки на клавишах
    s += SL(Z_SRED, _pianino(180, 980, 520, t, 330, 1.0))
    tx_, ty_, th = 450, 952, 520
    deti = []
    s_zat, poz = _zatylki_ryad(620, pol + 10, 1200, t, 7, 983, 300, 0)
    _figury_kadra(*([(tx_, ty_, th)] + [(p[0], p[1], p[2]) for p in poz]))
    s_zat, poz = _zatylki_ryad(620, pol + 10, 1200, t, 7, 983, 300, 0)
    s += SL(Z_SRED, _tabyret(tx_ + 30, ty_ + 6, t, 150, 160))
    tap = figura(tx_, ty_, th, t, col="#3d352c", kant="#ffd98a", ph=.3,
                 profil=True, naklon=5.0)
    r1, (f1x, f1y), _ = _ruka_mimo(tx_, ty_, th, -1, th * .34, 40, t,
                                   "#3d352c", "#ffd98a", .2, 7.0)
    r2, (f2x, f2y), _ = _ruka_mimo(tx_, ty_, th, -1, th * .28, 56, t,
                                   "#3d352c", "#ffd98a", .7, 8.0)
    tap += r1 + r2
    s += SL(Z_SRED, tap)
    # кисти тапёра на клавишах: варежки перекрывают клавиатуру внахлёст
    s += SL(Z_SRED, _varezhka(f1x, f1y + 2, th, t, .2)
            + _varezhka(f2x, f2y + 2, th, t, .7))
    # РЯДЫ ДЕТСКИХ ЗАТЫЛКОВ: со спины, рост через одного, шаг рваный
    s += SL(Z_SRED, s_zat)
    s_zat2, _ = _zatylki_ryad(520, pol + 70, 1400, t, 8, 985, 230, 1)
    s += SL(Z_SRED, s_zat2)
    # нижняя треть
    s += SL(Z_SRED, _polovik(1000, pol + 46, 720, 120, "#8a2a40", "#5a1626")
            + _kucha_listev(1780, pol + 50, 220, 987, 56)
            + _dvorovaya_utvar(100, pol + 48, 190, t, 989, ["vedro"]))
    s += SL(Z_SRED, svecha(120, pol - 230, t, .4, 1.1, 100)
            + teplo(130, pol - 290, 230, 200, .32))
    s += SL(Z_SRED, blik(1820, 240, t, 1.2, "#bcd8ff", "#ffd98a", .45))
    s += SL(Z_PERED, _stolb_pered(-8, 118, "#140a0e", 0, H))
    s += vinetka(.50)
    return s


def imeninnyy_tort_na_sto_svechey(t):
    """Стол с огромным именинным тортом крупно: лес свечек гаснет рядами, на
    стуле у торта колпак именинника и маленький рисованный штурвал. Дед в
    очках сидит за столом, обе руки на набалдашнике трости. Внук стоит на
    стуле коленями, обеими руками упирается в стол и дует на свечи. Цифры на
    торте не рисуем — их кладёт `kadr.py`."""
    rnd = random.Random(991)
    pol = 1014
    s = f'<rect width="{W}" height="{H}" fill="#2b2218"/>'
    s += SL(Z_DAL, _stena_gornicy(t, 993, True, 720, True))
    s += SL(Z_DAL, _ramki_na_stene(140, 140, 440, t, 995, 3)
            + _polka_s_utvaryu(1400, 160, 460, t, 997, 4))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}"'
                   f' height="{H-pol+18:.0f}" fill="#5e4a34"/>'
            + polovicy(pol + 14) + _pol_shvy(pol + 16, 1074, 999, 6, "#4a3824"))
    # СТОЛ с тортом
    s += SL(Z_SRED, f'{ten(960, pol + 16, 640, 26, .5)}'
                    f'<rect x="140" y="760" width="1500" height="54" rx="12"'
                    f' fill="url(#derev)" {o(8)}/>'
            + f'<rect x="170" y="814" width="1440" height="26" rx="9"'
              f' fill="#5b4428" {o(5)}/>')
    for px in (250, 1480):
        s += SL(Z_SRED, f'<rect x="{px:.0f}" y="840" width="70"'
                        f' height="{pol-840:.0f}" rx="12" fill="#5b4428"'
                        f' {o(6)}/>')
    s += SL(Z_SRED, _rushnik_vyshityy(160, 744, 900, 84, t, 1001))
    # ГЛАВНЫЙ ПРЕДМЕТ: торт со свечами, они гаснут рядами
    gasnet = A.ease(A.seg(t, 1.2, 2.2))
    s += SL(Z_SRED, _tort_svechi(700, 752, 560, t, gasnet, 3))
    # стул с колпаком и штурвалом вместо персонажа
    s += SL(Z_SRED, _venskiy_stul(1230, pol, 430, t, -6, False))
    s += SL(Z_SRED, _kolpak_imeninnika(1180, pol - 250, 1.0, t, .2))
    s += SL(Z_SRED, _shturval(1300, pol - 300, .9, t))
    # сопутствующие вещи стола
    s += SL(Z_SRED, _kruzhka(370, 752, 1.05, 0, "#e8eef0", 1)
            + _tarelka(1420, 730, 70, t, .3, False, 0, "#eef2f4")
            + _samovar(1560, 752, t, .82))
    s += SL(Z_SRED, svecha(1380, 748, t, .4, 1.15, 110)
            + teplo(1380, 690, 260, 220, .34))
    # ДВЕ ФИГУРЫ: дед за столом и внук на стуле коленями
    dx_, dy_, dh = 1680, pol - 150, 580
    vx, vy, vh = 420, pol - 180, 430
    _figury_kadra((dx_, dy_, dh), (vx, vy, vh))
    duet = A.ease(A.seg(t, .5, 1.0))
    razv = A.ease(A.seg(t, 3.4, 1.2))
    ded = figura(dx_, dy_, dh, t, col="#54505e", kant="#ffd98a", ph=.3,
                 boroda=True, naklon=4.0)
    r1, (k1x, k1y), _ = _ruka_mimo(dx_, dy_, dh, -1, dh * .32,
                                   44 - 46 * razv, t, "#54505e",
                                   "#ffd98a", .2, 4.0)
    r2, (k2x, k2y), _ = _ruka_sgib_mimo(dx_, dy_, dh, -1, dh * .22, 22,
                                        dh * .22, 48 - 40 * razv, t,
                                        "#54505e", "#ffd98a", .7, 4.0)
    ded += r1 + r2
    s += SL(Z_SRED, ded)
    s += SL(Z_SRED, _ochki(dx_ - 4, dy_ - dh * .845, 1.1, t))
    # ТРОСТЬ: обе кисти на набалдашнике, пока дед не развёл руками
    if razv < .3:
        s += SL(Z_SRED, _trost_nabaldashnik((k1x + k2x) * .5 - 10,
                                            pol - 4, .9, t, 280))
        s += SL(Z_SRED, _varezhka(k1x, k1y + 2, dh, t, .2)
                + _varezhka(k2x, k2y + 2, dh, t, .7))
    else:
        s += SL(Z_SRED, _trost_nabaldashnik(1560, pol - 4, .9, t, 280))
    vnuk = figura(vx, vy, vh, t, col="#4a5a72", kant="#ffd98a", ph=.7,
                  naklon=7.0)
    p1, (m1x, m1y), _ = _ruka_mimo(vx, vy, vh, 1, vh * .44, 28 + 14 * duet, t,
                                   "#4a5a72", "#ffd98a", .1, 4.0)
    p2, (m2x, m2y), _ = _ruka_mimo(vx, vy, vh, 1, vh * .38, 48 + 10 * duet, t,
                                   "#4a5a72", "#ffd98a", .6, 4.0)
    vnuk += p1 + p2
    s += SL(Z_SRED, _venskiy_stul(400, pol, 420, t, 4, True))
    s += SL(Z_SRED, vnuk)
    # колени на сиденье стула — опора названа
    s += SL(Z_SRED, f'<path d="M{vx-vh*.18:.0f},{vy-vh*.04:.0f}'
                    f' q{vh*.18:.0f},{vh*.07:.0f} {vh*.36:.0f},0'
                    f' q{-vh*.09:.0f},{vh*.05:.0f} {-vh*.36:.0f},0 Z"'
                    f' fill="#3f5c7a" {o(4)}/>')
    # ДУНОВЕНИЕ: струи воздуха от лица внука к свечам
    gyv = vy - vh * .845
    for i in range(3):
        p = ((t * 1.5 + i / 3.0) % 1.0)
        s += SL(Z_LETIT, f'<path d="M{vx+vh*.14:.0f},{gyv+vh*.05+i*16:.0f}'
                         f' q{120+p*120:.0f},{-20+i*14:.0f}'
                         f' {240+p*200:.0f},{-6+i*10:.0f}" fill="none"'
                         f' stroke="#cfe4f5" stroke-width="{9-3*i:.0f}"'
                         f' opacity="{(1-p)*.6*duet:.2f}"/>')
    s += SL(Z_SRED, _varezhka(m1x, m1y + 2, vh, t, .1)
            + _varezhka(m2x, m2y + 2, vh, t, .6))
    # нижняя треть
    s += SL(Z_SRED, _polovik(960, pol + 42, 620, 120, "#cdbf9c", "#b8352c")
            + _dvorovaya_utvar(130, pol + 50, 220, t, 1003, ["korzina"])
            + _kot_zhivoy(1060, pol + 54, t, 1.1, "#3b3430", .3)
            + _yaschiki(1840, pol + 14, t, 1005, 2, .78)
            + kartoshka(700, pol + 58, t, 7, 1007, 1.0))
    s += SL(Z_SRED, teplo(700, 640, 520, 380, .40))
    s += SL(Z_PERED, _stolb_pered(-8, 110, "#1a120c", 0, H))
    s += vinetka(.44)
    return s


def chetyre_chuzhih_veschi_na_doroge(t):
    """Осенняя дорога к дому: в ряд лежат четыре вещи — блестящая монета,
    растрёпанный веник с красной тряпицей, серый мешок-забота с хмурой
    рожицей и зелёная змейка-зависть кольцом. Бабушка в платке идёт по
    дороге: в правой руке бидон, левой придерживает платок. Она по очереди
    перешагивает или обходит все четыре и идёт к своей калитке, не
    оглядываясь."""
    rnd = random.Random(1009)
    gor = 700
    s = f'<rect width="{W}" height="{H}" fill="url(#nsumer)"/>'
    s += nebo("sumer", t, False, 1011)
    s += oblaka(t, 160, 6, 1013, .42, "#cdd7e4", 12.0)
    s += SL(Z_DAL, _derevnya_ryad(gor - 140, t, 1015, ((150, 300), (1700, 330))))
    s += SL(Z_DAL, goloe_derevo(420, gor - 30, 520, t, 1017, 9, "#3a3b43", True)
            + goloe_derevo(1280, gor - 10, 460, t, 1019, 8, "#3a3b43", True))
    s += SL(Z_DAL, pleten(-20, gor - 190, 560, 180, 9))
    # КАЛИТКА своего двора, к которой она идёт
    s += SL(Z_SRED, _zabor_dosok(1120, gor - 180, 800, 180, 1021, 54))
    s += SL(Z_SRED, _stena_ambara(100, gor - 300, 560, 320, t, True, 1043))
    s += SL(Z_SRED, _stennoe_hozyaystvo(200, gor - 240, t, 1045))
    s += SL(Z_DAL, izba_snaruzhi(900, gor + 20, 640, t, True, True, 1047))
    s += SL(Z_SRED, _stog(700, gor + 80, .82, t, True))
    s += SL(Z_SRED, _kalitka_hlopaet(1700, gor + 130, 200, 270, t, True))
    s += SL(Z_DAL, izba_snaruzhi(1760, gor + 60, 420, t, True, True, 1023))
    # ЗЕМЛЯ и ДОРОГА, уходящая к калитке
    s += SL(Z_SRED, f'<rect x="0" y="{gor+40:.0f}" width="{W}"'
                    f' height="{H-gor-40:.0f}" fill="#4e4638"/>'
            + _zemlya_faktura(gor + 80, 1072, 1025, 18, "#3c3529")
            + _listya(1027, 40, gor + 90, 1070))
    s += SL(Z_SRED, f'<path d="M-40,1072 Q560,900 1680,{gor+120:.0f}'
                    f' L1860,{gor+150:.0f} Q700,960 420,1076 Z"'
                    f' fill="#6a6050" {o(5)}/>'
            + _koleya(1000, 1029, 2))
    # ЧЕТЫРЕ ЧУЖИЕ ВЕЩИ в ряд по дороге
    s += SL(Z_SRED, _moneta_krupno(300, 1016, 56, t, .2, True, True, .78))
    s += SL(Z_SRED, f'<circle cx="300" cy="1016" r="92" fill="{SVET}"'
                    f' opacity="{.12+.14*abs(A.w(t,1.5,.2)):.2f}"/>')
    s += SL(Z_SRED, _venik(700, 978, 300, t, "#9c8a62", "#b8352c", True,
                           .82, .3, .92, 1031))
    s += SL(Z_SRED, _meshok_zabota(1090, 952, .96, t,
                                   A.ease(A.seg(t, 2.6, 1.2))))
    s += SL(Z_SRED, _zmeyka_zavisti(1420, 912, t, 1.25,
                                    A.ease(A.seg(t, 3.6, 1.4))))
    # ОДНА ФИГУРА: бабушка идёт мимо, перешагивая вещи
    hod = A.ease(A.seg(t, .3, 4.4))
    bx = 240 + 980 * hod
    by_ = 1040 - 160 * hod
    bh = 790 - 190 * hod
    shag = 16 * A.w(t, 1.1, .2)
    _figury_kadra((bx, by_, bh))
    bab = figura(bx, by_ - abs(shag) * .5, bh, t, col="#54505e",
                 kant="#cfe4f5", platok=True, ph=.3, naklon=4.0)
    r1, (n1x, n1y), _ = _ruka_mimo(bx, by_ - abs(shag) * .5, bh, 1,
                                   bh * .34, 50, t, "#54505e", "#cfe4f5",
                                   .2, 5.0)
    r2, (n2x, n2y), _ = _ruka_so_sgibom(bx, by_ - abs(shag) * .5, bh, -1,
                                        bh * .20, -28, bh * .18, -50, t,
                                        "#54505e", "#cfe4f5", .7, 4.0)
    bab += r1 + r2
    s += SL(Z_SRED, bab)
    s += SL(Z_SRED, _bidon(n1x + 24, n1y + 110, .68 * bh / 790.0, t, 4))
    s += SL(Z_SRED, _varezhka(n1x, n1y + 4, bh, t, .2))
    s += SL(Z_SRED, _varezhka(n2x, n2y + 2, bh, t, .7))
    s += SL(Z_SRED, para_izo_rta(bx + 34, by_ - bh * .80, t, .4, 1.0, .5))
    # нижняя треть
    s += SL(Z_SRED, _sledy(180, 1072, bx - 90, by_ + 10, 7, 1033,
                           "#352f24", 1.1)
            + _kucha_listev(900, 1056, 300, 1035, 72)
            + _luzha(520, 1050, 220, t, .3)
            + _polenica(60, 1046, 260, 190, 1037, 25)
            + _podorozhnik(1240, 1058, 1.1, t, .3, 5, "#6f7a44"))
    s += SL(Z_SRED, dym(1860, gor - 180, t, 5, .28, 300, .34, "#cfd6de", 1.5))
    s += SL(Z_SRED, _vorona(1120, gor - 300, t, .82, .3, .5))
    s += SL(Z_LETIT, mokryy_sneg(t, 22, 1039, .44, 1.1))
    s += SL(Z_PERED, _vetka_pered(-40, 150, 580, 26, t, 1041, "#241c16", 7))
    s += vinetka(.44)
    return s


def tri_devichih_gadaniya(t):
    """Девичья комната, стол у окна и три гадания: ромашка в стакане с
    облетевшими лепестками; шапка, полная свёрнутых бумажек с именами —
    девушка правой рукой тянет одну, левой держит шапку; окно, в котором
    виден первый встречный прохожий в шляпе. К концу на столе проступает
    свадебная карточка в рамке, где она уже седая и улыбается."""
    rnd = random.Random(1049)
    pol = 1014
    s = f'<rect width="{W}" height="{H}" fill="#2a2320"/>'
    s += SL(Z_DAL, _stena_gornicy(t, 1051, True, 720, True))
    s += SL(Z_DAL, _polka_s_utvaryu(100, 150, 440, t, 1053, 4)
            + _ramki_na_stene(600, 130, 380, t, 1055, 3))
    # девичья комната обжита: коврик на стене, полка с мелочью, сундук
    s += SL(Z_DAL, _kover_na_stene(420, 330, 560, 340, t, 1067))
    s += SL(Z_DAL, _polka_s_utvaryu(1020, 200, 420, t, 1091, 5))
    s += SL(Z_SRED, _yaschiki(200, 1014, t, 1093, 3, .96))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-18:.0f}" width="{W}"'
                   f' height="{H-pol+18:.0f}" fill="#5e4a34"/>'
            + polovicy(pol + 14) + _pol_shvy(pol + 16, 1074, 1057, 6, "#4a3824"))
    # ОКНО с первым встречным прохожим в шляпе
    pro = ((t * .14) % 1.0)
    vid = (f'<rect x="1300" y="180" width="540" height="440" fill="{SUMER}"/>'
           + "".join(f'<rect x="{1340+i*110:.0f}" y="420" width="62"'
                     f' height="50" rx="5" fill="{SVET}"'
                     f' opacity="{.4+.25*abs(A.w(t,2.4,i*.4)):.2f}"/>'
                     for i in range(4))
           + f'<rect x="1300" y="470" width="540" height="150" fill="{SNEG}"'
             f' opacity=".7"/>')
    ppx = 1320 + pro * 480
    vid += (f'<path d="M{ppx-34:.0f},{600:.0f} q{34:.0f},{-14:.0f} {68:.0f},0'
            f' L{ppx+22:.0f},{470:.0f} L{ppx-22:.0f},{470:.0f} Z"'
            f' fill="#3f4a58" {o(5)}/>'
            f'<circle cx="{ppx:.0f}" cy="{448:.0f}" r="26" fill="#e8d8c0"'
            f' {o(4)}/>'
            f'<path d="M{ppx-36:.0f},{432:.0f} q{36:.0f},{-14:.0f} {72:.0f},0'
            f' q{-10:.0f},{10:.0f} {-72:.0f},0 Z" fill="#2f3a48" {o(4)}/>'
            f'<rect x="{ppx-20:.0f}" y="{400:.0f}" width="40" height="34"'
            f' rx="6" fill="#2f3a48" {o(4)}/>')
    s += SL(Z_DAL, okno_izby(1300, 180, 540, 440, t, vid, .16, False, True))
    s += SL(Z_SRED, zanaveska(1320, 190, 240, 130, None, t, 1)
            + zanaveska(1820, 190, 240, 130, None, t, -1))
    # СТОЛ У ОКНА
    s += SL(Z_SRED, f'{ten(760, pol + 16, 540, 24, .5)}'
                    f'<rect x="200" y="760" width="1180" height="52" rx="12"'
                    f' fill="url(#derev)" {o(8)}/>'
            + f'<rect x="230" y="812" width="1120" height="26" rx="9"'
              f' fill="#5b4428" {o(5)}/>')
    for px in (300, 1230):
        s += SL(Z_SRED, f'<rect x="{px:.0f}" y="838" width="68"'
                        f' height="{pol-838:.0f}" rx="12" fill="#5b4428"'
                        f' {o(6)}/>')
    s += SL(Z_SRED, _rushnik_vyshityy(220, 744, 700, 80, t, 1059))
    # ГАДАНИЕ ПЕРВОЕ: ромашка в стакане с облетевшими лепестками
    s += SL(Z_SRED, _romashka_v_stakane(370, 752, 1.05, t,
                                        A.ease(A.seg(t, .4, 3.0))))
    # ГАДАНИЕ ВТОРОЕ: шапка с бумажками, одна тянется наружу
    tyan = A.ease(A.seg(t, 1.4, 1.8))
    s += SL(Z_SRED, _shapka_s_bumazhkami(820, 752, 1.0, t, tyan, 9, 1061))
    # ГАДАНИЕ ТРЕТЬЕ — само окно с прохожим (выше), плюс свеча у стекла
    s += SL(Z_SRED, svecha(1180, 752, t, .3, 1.3, 118)
            + teplo(1180, 690, 300, 260, .40))
    # СВАДЕБНАЯ КАРТОЧКА проступает к концу плана
    s += SL(Z_SRED, _svadebnaya_kartochka(540, 748, 300, t,
                                          A.ease(A.seg(t, 6.6, 2.0))))
    # ОДНА ФИГУРА: девушка у стола
    dx_, dy_, dh = 1020, pol, 770
    _figury_kadra((dx_, dy_, dh))
    dev = figura(dx_, dy_, dh, t, col="#8a4a5c", kant="#ffd98a", ph=.4,
                 naklon=4.0)
    r1, (c1x, c1y), _ = _ruka_so_sgibom(dx_, dy_, dh, -1, dh * .22, 10,
                                        dh * .24, 34 - 26 * tyan, t,
                                        "#8a4a5c", "#ffd98a", .2, 5.0)
    r2, (c2x, c2y), _ = _ruka_so_sgibom(dx_, dy_, dh, -1, dh * .24, 32,
                                        dh * .24, 56, t, "#8a4a5c",
                                        "#ffd98a", .7, 4.0)
    dev += r1 + r2
    s += SL(Z_SRED, dev)
    # КОСА девушки через плечо — роль читается со стоп-кадра
    gy_ = dy_ - dh * .845
    s += SL(Z_SRED, f'<path d="M{dx_+dh*.11:.0f},{gy_+dh*.02:.0f}'
                    f' q{dh*.06:.0f},{dh*.10:.0f} {dh*.015:.0f},{dh*.22:.0f}"'
                    f' fill="none" stroke="#8a6038" stroke-width="{dh*.045:.0f}"'
                    f' stroke-linecap="round"/>'
            + "".join(f'<circle cx="{dx_+dh*(.115-i*.004):.0f}"'
                      f' cy="{gy_+dh*(.06+i*.05):.0f}" r="{dh*.020:.0f}"'
                      f' fill="#9c7049" {o(3)}/>' for i in range(4))
            + f'<path d="M{dx_+dh*.11:.0f},{gy_+dh*.245:.0f} q{dh*.03:.0f},'
              f'{dh*.03:.0f} {-dh*.01:.0f},{dh*.05:.0f}" fill="none"'
              f' stroke="{TKAN}" stroke-width="{dh*.020:.0f}"/>')
    s += SL(Z_SRED, _varezhka(c1x, c1y + 2, dh, t, .2)
            + _varezhka(c2x, c2y + 2, dh, t, .7))
    # нижняя треть
    s += SL(Z_SRED, _venskiy_stul(1420, pol, 420, t, 6, False)
            + _polovik(760, pol + 42, 560, 118, "#cdbf9c", "#b8352c")
            + _dvorovaya_utvar(130, pol + 50, 220, t, 1063, ["korzina"])
            + _kot_zhivoy(620, pol + 54, t, 1.1, "#3b3430", .3, True, True)
            + _yaschiki(1800, pol + 14, t, 1065, 2, .8))
    s += SL(Z_PERED, _stolb_pered(-8, 110, "#1a120c", 0, H))
    s += vinetka(.44)
    return s


def vecher_dnya_iony(t):
    """Вечерний двор одним кадром, четыре места по словам: монета блестит на
    тропинке у калитки, на подоконнике кухни редька на блюдце с ложкой мёда,
    над банькой дым и свет в окошке, чердачное окно дома крупно показывает
    настоящую яркую луну. Бабушка в чистом платке стоит на крыльце после
    бани, обеими руками держит кружку чая, от плеч идёт пар, смотрит на
    луну."""
    rnd = random.Random(1069)
    gor = 820
    s = f'<rect width="{W}" height="{H}" fill="url(#nnoch)"/>'
    s += nebo("noch", t, True, 1071)
    s += oblaka(t, 170, 4, 1073, .26, "#6f7f8c", 18.0)
    s += SL(Z_DAL, _derevnya_ryad(gor - 160, t, 1075, ((120, 280), (1840, 240))))
    # ДОМ с чердачным окном — в нём настоящая луна
    s += SL(Z_SRED, brevna(760, 430, 900, gor - 390, 92)
            + f'<rect x="740" y="416" width="940" height="26" rx="9"'
              f' fill="#5a4530" {o(5)}/>')
    s += SL(Z_SRED, f'<path d="M700,434 L1210,196 L1720,434 Z" fill="#6b5340"'
                    f' {o(8)}/>'
            + f'<path d="M700,434 L1210,196 L1210,228 L756,438 Z"'
              f' fill="{SNEG}" opacity=".88"/>')
    px, py, pw, ph_ = 820, 440, 780, 310
    put = kontur_proema(px, py, pw, ph_, "pryam")
    vid = (f'<path d="{put}" fill="{NOCH}"/>'
           f'<circle cx="{px+pw*.56:.0f}" cy="{py+ph_*.42:.0f}" r="96"'
           f' fill="#f2f6fa" opacity="{.88+.1*abs(A.w(t,1.9,.2)):.2f}"/>'
           f'<circle cx="{px+pw*.56:.0f}" cy="{py+ph_*.42:.0f}" r="150"'
           f' fill="#cfe4f5" opacity=".16"/>'
           f'<circle cx="{px+pw*.60:.0f}" cy="{py+ph_*.34:.0f}" r="20"'
           f' fill="#cfd6de" opacity=".45"/>')
    for i in range(14):
        sx_ = px + rnd.uniform(26, pw - 26)
        sy_ = py + rnd.uniform(24, ph_ - 24)
        vid += (f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}"'
                f' r="{rnd.uniform(2.5,5):.0f}" fill="#e8eef6"'
                f' opacity="{.4+.5*abs(A.w(t,1.2+i*.08,i*.3)):.2f}"/>')
    s += SL(Z_SRED, vid + mesto_stoka(px, py, pw, ph_, "pryam"))
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#5f4a34"'
                    f' stroke-width="32"/>'
            + f'<line x1="{px+pw*.5:.0f}" y1="{py:.0f}" x2="{px+pw*.5:.0f}"'
              f' y2="{py+ph_:.0f}" stroke="#5f4a34" stroke-width="22"/>'
            + f'<rect x="{px-44:.0f}" y="{py-46:.0f}" width="{pw+88:.0f}"'
              f' height="40" rx="12" fill="#7d5a3c" {o(5)}/>'
            + f'<rect x="{px-32:.0f}" y="{py+ph_-10:.0f}" width="{pw+64:.0f}"'
              f' height="38" rx="12" fill="url(#dosk)" {o(6)}/>')
    # ПОДОКОННИК КУХНИ с редькой на блюдце
    s += SL(Z_SRED, okno_izby(300, 470, 380, 300, t,
                              f'<rect x="300" y="470" width="380" height="300"'
                              f' fill="#2a1d12"/>'
                              f'<rect x="312" y="482" width="356" height="276"'
                              f' fill="{SVET}"'
                              f' opacity="{.66+.14*abs(A.w(t,2.4,.3)):.2f}"/>',
                              .14, True, True))
    s += SL(Z_SRED, f'<rect x="250" y="762" width="480" height="40" rx="12"'
                    f' fill="#cfc9bc" {o(6)}/>')
    s += SL(Z_SRED, _blyudce(430, 756, .72, .5, t))
    s += SL(Z_SRED, _redka_s_yamkoy(420, 744, .68, t, 1.0, .9))
    s += SL(Z_SRED, f'<g transform="rotate(-34 540 740)">'
                    f'<ellipse cx="540" cy="740" rx="24" ry="17"'
                    f' fill="#cfd8dc" {o(4)}/>'
                    f'<ellipse cx="540" cy="738" rx="16" ry="10" fill="{ZOL}"'
                    f' opacity=".95"/>'
                    f'<rect x="552" y="733" width="76" height="12" rx="6"'
                    f' fill="#b9c6cc" {o(3)}/></g>')
    # БАНЬКА на огороде: дым и свет в окошке
    s += SL(Z_DAL, _banya_srub(50, gor + 30, 420, t, 1077, .0))
    # ЗЕМЛЯ, тропинка и монета у калитки
    s += SL(Z_SRED, f'<rect x="0" y="{gor+40:.0f}" width="{W}"'
                    f' height="{H-gor-40:.0f}" fill="#45483e"/>'
            + sneg_lezhit(gor + 70, 26)
            + _zemlya_faktura(gor + 100, 1072, 1079, 16, "#353830"))
    s += SL(Z_SRED, f'<path d="M-40,1072 Q420,940 1180,{gor+110:.0f}'
                    f' L1340,{gor+140:.0f} Q640,1000 360,1076 Z"'
                    f' fill="#6a6a5c" {o(5)}/>')
    s += SL(Z_SRED, _zabor_dosok(1480, gor - 90, 440, 180, 1081, 54))
    s += SL(Z_SRED, _kalitka_hlopaet(1700, gor + 150, 200, 260, t, True))
    s += SL(Z_SRED, _moneta_krupno(1540, 1000, 50, t, .2, True, True, .76))
    s += SL(Z_SRED, f'<circle cx="1540" cy="1000" r="86" fill="{SVET}"'
                    f' opacity="{.12+.16*abs(A.w(t,1.4,.2)):.2f}"/>')
    # КРЫЛЬЦО и ОДНА ФИГУРА: бабушка после бани с кружкой чая
    s += SL(Z_SRED, _kryl_co(640, gor + 150, 420, 180, t, 3, True, False))
    bx, by_, bh = 820, gor + 10, 700
    _figury_kadra((bx, by_, bh))
    bab = figura(bx, by_, bh, t, col="#efe8d8", kant="#ffd98a", platok=True,
                 ph=.3, naklon=3.0)
    r1, (k1x, k1y), _ = _ruka_mimo(bx, by_, bh, -1, bh * .30, 42, t,
                                   "#efe8d8", "#ffd98a", .2, 4.0)
    r2, (k2x, k2y), _ = _ruka_mimo(bx, by_, bh, 1, bh * .28, 44, t,
                                   "#efe8d8", "#ffd98a", .7, 4.0)
    bab += r1 + r2
    s += SL(Z_SRED, bab)
    # КРУЖКА ЧАЯ в обеих кистях, от неё и от плеч идёт пар
    kx_ = (k1x + k2x) * .5
    s += SL(Z_SRED, _kruzhka(kx_, k1y + 52, 1.15, 0, "#e8eef0", 1))
    s += SL(Z_SRED, par(kx_, k1y - 12, t, 4, .56, 170, .5, 1.2))
    s += SL(Z_SRED, _varezhka(k1x, k1y + 4, bh, t, .2)
            + _varezhka(k2x, k2y + 4, bh, t, .7))
    s += SL(Z_SRED, par(bx - bh * .20, by_ - bh * .66, t, 3, .46, 150, .55)
            + par(bx + bh * .20, by_ - bh * .64, t, 3, .42, 140, .62))
    # нижняя треть
    s += SL(Z_SRED, _polenica(230, 1046, 320, 200, 1083, 26)
            + _dvorovaya_utvar(560, 1050, 230, t, 1085, ["kadka", "vedro"])
            + _sledy(1420, 1070, 900, gor + 160, 7, 1087, "#2d302a", 1.0)
            + _kot_zhivoy(1180, 1042, t, 1.1, "#3b3430", .3))
    s += SL(Z_SRED, teplo(260, gor - 120, 420, 340, .32))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 1089, .40, .9))
    s += SL(Z_PERED, _stolb_pered(-8, 112, "#121018", 0, H))
    s += vinetka(.46)
    return s
