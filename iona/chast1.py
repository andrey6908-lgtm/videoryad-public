# -*- coding: utf-8 -*-
"""ПОРЦИЯ 1: 35 декораций ролика «18 ноября — День Ионы».

Каждая функция — f(t) -> SVG (без внешнего <svg> и без <defs>). Рисуются
заново под текст этого ролика (R-0019): ни один кадр не взят из «13», «14»,
«15», «16 ноября». Люди — только `figura()` из `lok_obshchee`, руки — через
`rukav()` от плеча (R-0051). Источник: `zadaniya/porciya1.md`.
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


# ── общие помощники этой порции (не кирпичики baza, локальные для файла) ───













































































def moneta_na_tropinke(t):
    """Утоптанная тропинка в инее, медяк в четверть кадра, бабушка с бидоном
    останавливается над ним. Вокруг — живая деревня: избы, заборы, колея."""
    rnd = random.Random(101)
    gor = 500
    s = nebo("sumer", t, True, 11)
    s += oblaka(t, 150, 5, 7, .4)
    s += SL(Z_DAL, _derevnya_ryad(gor, t, 7, ((150, 330), (470, 270), (1760, 300))))
    s += SL(Z_DAL, goloe_derevo(760, gor + 30, 720, t, 4, 10, "#2a2b33", True)
            + goloe_derevo(1200, gor + 22, 560, t, 9, 9, "#2a2b33", True)
            + goloe_derevo(1480, gor + 14, 400, t, 14, 7, "#2a2b33", True))
    sta = ""
    for i in range(9):
        bx_ = 420 + i * 130 + 30 * math.sin(t * .5 + i)
        by_ = 210 + (i % 4) * 46 + 12 * A.w(t, 2.0, i * .3)
        sta += ptica(bx_, by_, t, .9, "#4a4a52", i * .2)
    s += SL(Z_DAL, sta)
    s += SL(Z_DAL, _zabor_dosok(-20, 356, 1040, 200, 5, 52)
            + _zabor_dosok(1180, 368, 760, 196, 8, 54))
    s += SL(Z_DAL, teplo(470, gor - 110, 230, 170, .42))

    zem = f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor}" fill="#4c3b2a"/>'
    zem += (f'<path d="M-40,{gor+70:.0f} Q500,{gor+20:.0f} 1020,{gor+96:.0f}'
            f' Q1520,{gor+170:.0f} 1960,{gor+120:.0f} L1960,1080 L-40,1080 Z"'
            f' fill="#5d4830" {o(0)}/>')
    zem += _koleya(gor + 180, 21, 2)
    zem += _listya(23, 34, gor + 90, 1060)
    zem += _trava(rnd, 16, gor + 60, 1050)
    zem += _inej(31, 48, gor + 60, 1060)
    zem += _podorozhnik(300, 960, 1.5, t, .2)
    zem += _podorozhnik(1640, 880, 1.1, t, .6)
    zem += kartoshka(1560, 1010, t, 5, 6, .9)
    s += SL(Z_SRED, zem)
    s += SL(Z_SRED, _dvorovaya_utvar(70, 700, 420, t, 9, ["korzina", "vedro", "korob"]))
    s += SL(Z_SRED, _polenica(1480, 620, 380, 190, 7, 24))
    # после того как монета ужалась до трети роста, в середине кадра
    # освободилось место — закрываю его вещами, а не пустотой
    s += SL(Z_SRED, _dvorovaya_utvar(880, 800, 380, t, 357,
                                     ["korzina", "vedro", "meshok"]))
    s += SL(Z_SRED, _kucha_listev(500, 906, 268, 359, 86)
            + kartoshka(1010, 944, t, 7, 361, 1.05)
            + _sledy(210, 1046, 606, 892, 6, 363, "#33281d", 1.1))

    # МОНЕТА — ТРЕТЬ РОСТА ФИГУРЫ (осмотр 15.11, второй заход: 428 px всё
    # ещё читались половиной роста). Диаметр 292 при росте 880 и голове 270 —
    # чуть больше головы, меньше трети человека.
    s += SL(Z_SRED, _moneta_krupno(706, 862, 146, t, .1))

    fx, fy, fh = 1400, 1076, 880
    stop = A.ease(A.seg(t, .4, 1.1))
    fig = figura(fx - 40 * (1 - stop), fy, fh, t, col="#30323e", kant="#cfe4f5",
                 platok=True, tulup=True, ph=.3)
    ruk, (rx2, ry2), (psx, psy) = _ruka(fx, fy, fh, 1, fh * .44, 74, t,
                                        "#30323e", "#cfe4f5", .3, 9.0)
    fig += ruk
    bid = 10 * A.w(t, 1.3, .2)
    fig += (f'<g transform="rotate({bid:.1f} {rx2:.0f} {ry2:.0f})">'
            f'<rect x="{rx2-42:.0f}" y="{ry2:.0f}" width="84" height="112" rx="10"'
            f' fill="url(#zhel)" {o(5)}/>'
            f'<rect x="{rx2-50:.0f}" y="{ry2-14:.0f}" width="100" height="22" rx="8"'
            f' fill="{ZHELEZ}" {o(4)}/>'
            f'<path d="M{rx2-30:.0f},{ry2-14:.0f} Q{rx2:.0f},{ry2-62:.0f}'
            f' {rx2+30:.0f},{ry2-14:.0f}" fill="none" stroke="{ZHELEZ}" stroke-width="8"/>'
            f'<line x1="{rx2-34:.0f}" y1="{ry2+56:.0f}" x2="{rx2+34:.0f}" y2="{ry2+56:.0f}"'
            f' stroke="#2f3337" stroke-width="6" opacity=".7"/></g>')
    ruk2, (lx2, ly2), (plx, ply) = _ruka(fx, fy, fh, -1, fh * .22, -52, t,
                                         "#30323e", "#cfe4f5", .7, 5.0)
    fig += ruk2
    fig += (f'<path d="M{lx2-18:.0f},{ly2-6:.0f} Q{lx2:.0f},{ly2+34:.0f}'
            f' {lx2+22:.0f},{ly2-4:.0f}" fill="none" stroke="#6d4a52" stroke-width="12"/>')
    fig += para_izo_rta(fx - 54, fy - fh * .80, t, .2, 1.1, .55)
    s += SL(Z_SRED, fig)
    s += SL(Z_SRED, ten(fx, fy + 8, 186, 30, .5))
    # НИЖНЯЯ ТРЕТЬ — НАСТОЯЩИМИ ВЕЩАМИ: следы к монете, лужа с отражением,
    # сгребённые листья, кот у поленницы. Счётчик низ не меряет, глаз меряет.
    s += SL(Z_SRED, _sledy(1760, 1070, 1180, 862, 7, 41, "#33281d", 1.25)
            + _luzha(430, 1012, 196, t, .3)
            + _kucha_listev(1066, 1062, 300, 43, 94)
            + _kot_zhivoy(206, 902, t, .86, "#2f2a26", .4))

    s += SL(Z_PERED, _vetka_pered(-60, 120, 820, 22, t, 3, "#241c16", 7))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 5, .5, .8))
    s += ramka_pp("levo")
    s += vinetka(.42)
    return s


def monety_do_samoy_kalitki(t):
    """Тропинка сверху: медяки лежат дорожкой, как крошки, и ведут к резной
    калитке. Между ними бусина, пуговица и колечко. Петух на заборе тянет шею."""
    rnd = random.Random(102)
    gor = 400
    s = nebo("rassv", t, False, 13)
    s += oblaka(t, 120, 5, 9, .42)
    s += SL(Z_DAL, _derevnya_ryad(gor, t, 11, ((170, 380), (520, 300), (1700, 420))))
    s += SL(Z_DAL, goloe_derevo(1340, gor + 10, 420, t, 6, 8, "#2a2b33", True)
            + goloe_derevo(230, gor + 20, 300, t, 16, 6, "#2a2b33", True))
    s += SL(Z_DAL, _zabor_dosok(-20, 272, 1060, 216, 4, 54)
            + _zabor_dosok(1180, 280, 780, 212, 6, 56))
    s += SL(Z_DAL, teplo(520, gor - 120, 220, 170, .40))

    zem = f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor}" fill="#4a3a29"/>'
    zem += (f'<path d="M-40,1080 Q420,{gor+300:.0f} 700,{gor+80:.0f}'
            f' L1180,{gor+80:.0f} Q1480,{gor+300:.0f} 1960,1080 Z" fill="#6a5236" {o(0)}/>')
    zem += _zemlya_faktura(gor + 90, 1060, 51, 18)
    zem += _koleya(880, 24, 2)
    zem += _listya(25, 34, gor + 80, 1060)
    zem += _trava(rnd, 16, gor + 60, 1050)
    zem += _inej(33, 48, gor + 70, 1060)
    zem += _podorozhnik(1790, 980, 1.6, t, .4)
    zem += _podorozhnik(110, 900, 1.3, t, .8)
    s += SL(Z_SRED, zem)

    kx, ky, kw, kh = 760, 250, 390, 360
    kach = 2.2 * A.w(t, 3.0, .1)
    kal = (f'<g transform="rotate({kach:.1f} {kx:.0f} {ky+kh:.0f})">'
           f'<rect x="{kx:.0f}" y="{ky:.0f}" width="{kw:.0f}" height="{kh:.0f}" rx="10"'
           f' fill="url(#derev)" {o(6)}/>')
    for i in range(6):
        bx = kx + 24 + i * (kw - 60) / 5.0
        kal += (f'<rect x="{bx:.0f}" y="{ky+14:.0f}" width="34" height="{kh-28:.0f}"'
                f' rx="6" fill="#6a5030" {o(3)}/>')
    kal += (f'<path d="M{kx:.0f},{ky+50:.0f} L{kx+kw:.0f},{ky+190:.0f}'
            f' M{kx+kw:.0f},{ky+50:.0f} L{kx:.0f},{ky+190:.0f}" fill="none"'
            f' stroke="#4a3522" stroke-width="16"/>')
    for i in range(8):
        gx = kx + 8 + i * (kw - 16) / 7.0
        kal += (f'<path d="M{gx:.0f},{ky:.0f} Q{gx+16:.0f},{ky-42:.0f}'
                f' {gx+32:.0f},{ky:.0f} Z" fill="#6a5030" {o(3)}/>')
    kal += (f'<circle cx="{kx+kw-46:.0f}" cy="{ky+kh*.5:.0f}" r="18" fill="{ZHELEZ}" {o(3)}/>'
            f'</g>')
    for bx in (kx - 54, kx + kw + 10):
        kal += (f'<rect x="{bx:.0f}" y="{ky-56:.0f}" width="54" height="{kh+150:.0f}"'
                f' rx="8" fill="#3f2d1c" {o(6)}/>'
                f'<path d="M{bx-18:.0f},{ky-56:.0f} L{bx+27:.0f},{ky-112:.0f}'
                f' L{bx+72:.0f},{ky-56:.0f} Z" fill="#4e3a24" {o(5)}/>')
    s += SL(Z_SRED, kal)
    s += SL(Z_SRED, teplo(kx + kw * .5, ky + kh * .5, 300, 230, .38))

    # дорожка медяков: лежат ПЛАШМЯ и сходятся к калитке по перспективе
    dor = ""
    for i in range(13):
        p = i / 12.0
        mx = 1430 + (kx + kw * .5 - 1430) * (p ** .80) + (330 - 390 * p) * math.sin(p * 6.1)
        my = 1066 - (1066 - (ky + kh + 24)) * (p ** .70)
        r = 98 - 76 * p
        vsp = max(.0, 1 - abs(((t * .9) % 1.0) - p) * 5.4)
        dor += _moneta_krupno(mx, my, r, t, i * .17, True, r > 44, .74)
        if vsp > 0:
            dor += (f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{r*1.8:.0f}"'
                    f' ry="{r*.8:.0f}" fill="#ffe9ac" opacity="{vsp*.34:.2f}"/>')
    dor += (f'<ellipse cx="560" cy="968" rx="32" ry="24" fill="#6fa0c4" {o(4)}/>'
            f'<circle cx="550" cy="958" r="10" fill="#cfe9fb" opacity=".8"/>'
            f'<ellipse cx="1420" cy="900" rx="40" ry="18" fill="#e8e2d2" {o(4)}/>'
            f'<ellipse cx="1420" cy="900" rx="17" ry="8" fill="none" stroke="#b9ae95"'
            f' stroke-width="5"/>'
            f'<ellipse cx="420" cy="804" rx="36" ry="16" fill="none" stroke="url(#med)"'
            f' stroke-width="12"/>')
    s += SL(Z_SRED, dor)
    s += SL(Z_SRED, _polenica(40, 620, 380, 270, 12, 26))
    s += SL(Z_SRED, _dvorovaya_utvar(1180, 1056, 420, t, 14,
                                     ["kadka", "vedro", "korzina"]))

    # ЖИВОЙ ЧЕЛОВЕК В КАДРЕ (осмотр 15.11: сцена была совсем без фигуры —
    # дорожка медяков вела к калитке, и подобрать их было некому) и НИЖНЯЯ
    # ТРЕТЬ настоящими вещами: следы по тропе, лужа с отражением калитки,
    # сгребённые листья у столба, кот у поленницы, ящики под забором.
    fx, fy, fh = 1636, 1058, 790
    sh_ = 26 * A.w(t, .7, .2)
    fig = figura(fx + sh_, fy, fh, t, col="#3b3446", kant="#cfe4f5",
                 platok=True, tulup=True, ph=.25)
    rk, (kzx, kzy), _ = _ruka(fx, fy, fh, -1, fh * .40, 72, t,
                              "#3b3446", "#cfe4f5", .2, 6)
    fig += rk
    kch = 7 * A.w(t, 1.2, .4)
    fig += (f'<g transform="rotate({kch:.1f} {kzx:.0f} {kzy:.0f})">'
            f'<path d="M{kzx-74:.0f},{kzy+10:.0f} L{kzx+74:.0f},{kzy+10:.0f}'
            f' L{kzx+56:.0f},{kzy+138:.0f} L{kzx-56:.0f},{kzy+138:.0f} Z"'
            f' fill="url(#derev)" {o(5)}/>')
    for i in range(5):
        fig += (f'<line x1="{kzx-70+i*6:.0f}" y1="{kzy+22+i*24:.0f}"'
                f' x2="{kzx+70-i*6:.0f}" y2="{kzy+22+i*24:.0f}"'
                f' stroke="#4e3a24" stroke-width="5" opacity=".7"/>')
    fig += (f'<path d="M{kzx-72:.0f},{kzy+12:.0f} Q{kzx:.0f},{kzy-66:.0f}'
            f' {kzx+72:.0f},{kzy+12:.0f}" fill="none" stroke="#5a4228"'
            f' stroke-width="11"/>'
            f'<ellipse cx="{kzx-24:.0f}" cy="{kzy+18:.0f}" rx="34" ry="18"'
            f' fill="#7d4a24" {o(3)}/>'
            f'<ellipse cx="{kzx+28:.0f}" cy="{kzy+14:.0f}" rx="30" ry="16"'
            f' fill="#9a5a28" {o(3)}/></g>')
    rk2, _, _ = _ruka(fx, fy, fh, 1, fh * .34, 86, t, "#3b3446", "#cfe4f5", .6, 5)
    fig += rk2
    fig += para_izo_rta(fx - 48, fy - fh * .80, t, .4, 1.0, .5)
    s += SL(Z_SRED, fig)
    s += SL(Z_SRED, ten(fx, fy + 8, 168, 28, .5))
    s += SL(Z_SRED, _sledy(1500, 1072, 1030, 666, 7, 57, "#2f2518", 1.2)
            + _luzha(300, 1016, 182, t, .5)
            + _kucha_listev(690, 1036, 272, 59, 86)
            + _kot_zhivoy(1010, 974, t, .78, "#4a423a", .6)
            + _yaschiki(1700, 790, t, 61, 2, .8))
    s += SL(Z_SRED, _dvorovaya_utvar(250, 744, 360, t, 345, ["korob", "meshok"]))
    s += SL(Z_SRED, _kadushki_i_grabli(60, 1072, t, 347))
    s += SL(Z_SRED, _listya(349, 30, 820, 1060))

    px, py = 1320, 292
    shea = 26 * A.ease(abs(A.w(t, 2.2, .0)))
    pet = (f'<ellipse cx="{px:.0f}" cy="{py-74:.0f}" rx="86" ry="62" fill="#8d4a2a" {o(5)}/>'
           f'<path d="M{px-78:.0f},{py-52:.0f} Q{px-140:.0f},{py-92:.0f}'
           f' {px-74:.0f},{py-150:.0f} Q{px-30:.0f},{py-120:.0f} {px-38:.0f},{py-64:.0f} Z"'
           f' fill="#5e2f1a" {o(4)}/>'
           f'<path d="M{px+52:.0f},{py-100:.0f} Q{px+92+shea:.0f},{py-128-shea:.0f}'
           f' {px+96+shea:.0f},{py-186-shea:.0f} L{px+58+shea:.0f},{py-188-shea:.0f}'
           f' Q{px+56:.0f},{py-134:.0f} {px+30:.0f},{py-94:.0f} Z" fill="#9c5630" {o(4)}/>'
           f'<circle cx="{px+80+shea:.0f}" cy="{py-202-shea:.0f}" r="34" fill="#a85c33"'
           f' {o(4)}/>'
           f'<circle cx="{px+94+shea:.0f}" cy="{py-210-shea:.0f}" r="6" fill="#120c08"/>'
           f'<path d="M{px+112+shea:.0f},{py-202-shea:.0f} L{px+156+shea:.0f},'
           f'{py-192-shea:.0f} L{px+112+shea:.0f},{py-182-shea:.0f} Z" fill="#d8a14a"'
           f' {o(3)}/>'
           f'<path d="M{px+60+shea:.0f},{py-234-shea:.0f} Q{px+76+shea:.0f},'
           f'{py-276-shea:.0f} {px+96+shea:.0f},{py-234-shea:.0f}'
           f' Q{px+112+shea:.0f},{py-268-shea:.0f} {px+124+shea:.0f},{py-228-shea:.0f} Z"'
           f' fill="{KRAS}" {o(3)}/>'
           f'<path d="M{px+74+shea:.0f},{py-178-shea:.0f} Q{px+86+shea:.0f},'
           f'{py-152-shea:.0f} {px+98+shea:.0f},{py-178-shea:.0f} Z" fill="{KRAS}" {o(2)}/>'
           f'<path d="M{px-70:.0f},{py-96:.0f} Q{px-10:.0f},{py-150:.0f}'
           f' {px+30:.0f},{py-104:.0f}" fill="none" stroke="#b5682f" stroke-width="10"'
           f' opacity=".8"/>'
           f'<line x1="{px-14:.0f}" y1="{py-18:.0f}" x2="{px-14:.0f}" y2="{py+30:.0f}"'
           f' stroke="#d8a14a" stroke-width="9"/>'
           f'<line x1="{px+28:.0f}" y1="{py-18:.0f}" x2="{px+28:.0f}" y2="{py+30:.0f}"'
           f' stroke="#d8a14a" stroke-width="9"/>')
    s += SL(Z_SRED, pet)
    s += SL(Z_DAL, dym(520, 250, t, 5, .26, 300, .36, "#d3dae2", .9)
            + dym(1700, 210, t, 4, .22, 260, .30, "#d3dae2", .8))
    s += SL(Z_PERED, _stolb_pered(-10, 110, "#1d1611", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 7, .45, .7))
    s += ramka_pp("pravo")
    s += vinetka(.42)
    return s


def kalitka_na_zare(t):
    """Распахнутая резная калитка справа, за ней настоящая заря. Девушка в
    тулупчике широким взмахом бросает за калитку горсть мелочи из плошки."""
    rnd = random.Random(103)
    gor = 600
    s = nebo("rassv", t, False, 5)
    s += oblaka(t, 110, 4, 3, .38)

    px_, py_, pw_, ph_ = 1150, 170, 770, 480
    put = kontur_proema(px_, py_, pw_, ph_, "arka")
    s += SL(Z_DAL, _vid_za_proemom(put, t, "zarya", 5, px_ + pw_ * .5)
            + mesto_stoka(px_, py_, pw_, ph_, "arka")
            + f'<path d="{put}" fill="none" stroke="#2a1d12" stroke-width="16"/>')

    ug = -22 + 3 * A.w(t, 4.0, .2)
    stv = (f'<g transform="rotate({ug:.1f} {px_-40:.0f} {py_+ph_:.0f})">'
           f'<rect x="{px_-300:.0f}" y="{py_+60:.0f}" width="270" height="{ph_-40:.0f}"'
           f' rx="10" fill="url(#derev)" {o(6)}/>')
    for i in range(4):
        stv += (f'<rect x="{px_-282+i*64:.0f}" y="{py_+78:.0f}" width="40"'
                f' height="{ph_-76:.0f}" rx="6" fill="#6a5030" {o(3)}/>')
    for i in range(6):
        gx = px_ - 296 + i * 46
        stv += (f'<path d="M{gx:.0f},{py_+60:.0f} Q{gx+12:.0f},{py_+20:.0f}'
                f' {gx+24:.0f},{py_+60:.0f} Z" fill="#6a5030" {o(3)}/>')
    stv += (f'<path d="M{px_-300:.0f},{py_+140:.0f} L{px_-30:.0f},{py_+320:.0f}'
            f' M{px_-30:.0f},{py_+140:.0f} L{px_-300:.0f},{py_+320:.0f}" fill="none"'
            f' stroke="#4a3522" stroke-width="16"/>'
            f'<circle cx="{px_-70:.0f}" cy="{py_+ph_*.52:.0f}" r="20" fill="{ZHELEZ}"'
            f' {o(3)}/></g>')
    for bx in (px_ - 60, px_ + pw_ + 6):
        stv += (f'<rect x="{bx:.0f}" y="{py_-60:.0f}" width="58" height="{ph_+200:.0f}"'
                f' rx="8" fill="#3b2a1a" {o(6)}/>'
                f'<path d="M{bx-18:.0f},{py_-60:.0f} L{bx+29:.0f},{py_-120:.0f}'
                f' L{bx+76:.0f},{py_-60:.0f} Z" fill="#4e3a24" {o(5)}/>')
    s += SL(Z_SRED, stv)

    s += SL(Z_DAL, brevna(-20, 60, 1000, 560, 92))
    s += SL(Z_DAL, okno_izby(110, 170, 310, 260, t, svet=True)
            + teplo(265, 300, 260, 210, .44))
    s += SL(Z_DAL, dver(520, 140, 290, 480, .0, "url(#derev)", True, False))
    s += SL(Z_DAL, podkova(664, 100, 1.6, t))
    s += SL(Z_DAL, _polka_s_utvaryu(70, 540, 400, t, 75, 3))
    s += SL(Z_DAL, ryabina(900, 560, t, 1.3, 5))

    zem = f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor}" fill="#4a3a29"/>'
    zem += (f'<path d="M-40,1080 Q440,{gor+230:.0f} 900,{gor+50:.0f}'
            f' L1500,{gor+50:.0f} Q1760,{gor+200:.0f} 1960,1080 Z" fill="#5e482f" {o(0)}/>')
    zem += _zemlya_faktura(gor + 70, 1060, 53, 16)
    zem += _listya(27, 30, gor + 50, 1060)
    zem += _trava(rnd, 12, gor + 40, 1050)
    zem += _inej(35, 36, gor + 50, 1060)
    s += SL(Z_SRED, zem)
    s += SL(Z_SRED, _kryl_co(40, 690, 500, 180, t, 3, True, False))
    s += SL(Z_SRED, _dvorovaya_utvar(50, 684, 460, t, 19, ["vedro", "vedro", "kadka"]))
    s += SL(Z_SRED, grozd_ryabiny(1880, 790, t, 1.6, 12, 4, .3))

    bx, by = 520, 1074
    vyg = 18 * A.ease(abs(A.w(t, 2.8, .3)))
    s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{by-250:.0f}" width="290" height="250" rx="10"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<path d="M{bx-24:.0f},{by-250:.0f} L{bx+145:.0f},{by-344:.0f}'
                    f' L{bx+314:.0f},{by-250:.0f} Z" fill="#4e3a24" {o(5)}/>'
                    f'<ellipse cx="{bx+145:.0f}" cy="{by-112:.0f}" rx="76" ry="92"'
                    f' fill="#20170f" {o(4)}/>'
                    f'<ellipse cx="{bx+145-vyg:.0f}" cy="{by-106:.0f}" rx="50" ry="46"'
                    f' fill="#6b5236" {o(4)}/>'
                    f'<circle cx="{bx+127-vyg:.0f}" cy="{by-114:.0f}" r="6" fill="#120c08"/>'
                    f'<circle cx="{bx+163-vyg:.0f}" cy="{by-114:.0f}" r="6" fill="#120c08"/>'
                    f'<ellipse cx="{bx+146-vyg:.0f}" cy="{by-78:.0f}" rx="16" ry="11"'
                    f' fill="#2a1d12"/>'
                    f'<path d="M{bx+104-vyg:.0f},{by-140:.0f} L{bx+90-vyg:.0f},{by-176:.0f}'
                    f' L{bx+124-vyg:.0f},{by-156:.0f} Z" fill="#4e3a24" {o(3)}/>')

    fx, fy, fh = 840, 1046, 720
    vzm = A.ease(A.seg(t, .35, 1.2))
    fig = figura(fx, fy, fh, t, col="#6a4a32", kant="#ffd98a", platok=False, ph=.2,
                 tulup=True, naklon=5 * vzm)
    ruk, (rx2, ry2), (psx, psy) = _ruka(fx, fy, fh, 1, fh * .50, -54 + 92 * vzm,
                                        t, "#6a4a32", "#ffd98a", .1, 6)
    fig += ruk
    ruk2, (lx2, ly2), (plx, ply) = _ruka(fx, fy, fh, -1, fh * .46, 46, t,
                                         "#6a4a32", "#ffd98a", .5, 5)
    fig += ruk2
    # ПЛОШКА С МЕЛОЧЬЮ, А НЕ ТЁМНЫЙ КРУГ (осмотр 15.11: предмет в руке читался
    # кошкой или горшком). Теперь это широкая низкая плошка на 430 px —
    # главный предмет сцены, и мелочь в ней лежит горкой и видна поштучно.
    bcx = lx2 + _predmet_naruzhu(fx, fh, lx2, 430)
    bry = ly2 - 18
    fig += (f'<path d="M{bcx-215:.0f},{bry:.0f} Q{bcx-204:.0f},{bry+116:.0f}'
            f' {bcx:.0f},{bry+128:.0f} Q{bcx+204:.0f},{bry+116:.0f}'
            f' {bcx+215:.0f},{bry:.0f} Z" fill="url(#glina)" {o(6)}/>'
            f'<path d="M{bcx-180:.0f},{bry+54:.0f} Q{bcx:.0f},{bry+96:.0f}'
            f' {bcx+180:.0f},{bry+54:.0f}" fill="none" stroke="#8a6a44"'
            f' stroke-width="9" opacity=".6"/>'
            f'<ellipse cx="{bcx:.0f}" cy="{bry:.0f}" rx="215" ry="58"'
            f' fill="#3a2a18" {o(5)}/>'
            f'<ellipse cx="{bcx:.0f}" cy="{bry+4:.0f}" rx="188" ry="46"'
            f' fill="#1f160e" opacity=".85"/>'
            f'<ellipse cx="{bcx:.0f}" cy="{bry:.0f}" rx="215" ry="58" fill="none"'
            f' stroke="#d8b878" stroke-width="7" opacity=".7"/>')
    for i, (mdx, mdy, mr) in enumerate(((-126, 10, 46), (-54, 22, 50), (16, 14, 44),
                                        (84, 24, 48), (142, 6, 40),
                                        (-88, -18, 42), (48, -22, 44))):
        fig += _moneta_krupno(bcx + mdx, bry + mdy, mr, t, i * .18, True, False, .66)
    fig += (f'<ellipse cx="{bcx-70:.0f}" cy="{bry-12:.0f}" rx="86" ry="20"'
            f' fill="#ffeab4" opacity="{.18+.14*A.w(t,1.6,.3):.2f}"/>'
            f'<path d="M{lx2-30:.0f},{bry+8:.0f} q{30:.0f},{34:.0f} {62:.0f},{2:.0f}"'
            f' fill="none" stroke="#6a4a32" stroke-width="22"'
            f' stroke-linecap="round" opacity=".95"/>')
    kosa = 30 * vzm
    fig += (f'<path d="M{fx-fh*.14:.0f},{fy-fh*.78:.0f}'
            f' Q{fx-fh*.30-kosa:.0f},{fy-fh*.58:.0f} {fx-fh*.22-kosa*1.4:.0f},{fy-fh*.32:.0f}"'
            f' fill="none" stroke="#6b4a26" stroke-width="26" stroke-linecap="round"/>'
            f'<path d="M{fx+fh*.22:.0f},{fy-fh*.52:.0f}'
            f' Q{fx+fh*.34+kosa:.0f},{fy-fh*.30:.0f} {fx+fh*.26+kosa:.0f},{fy-fh*.10:.0f}"'
            f' fill="none" stroke="#7a5438" stroke-width="20" opacity=".8"/>')
    fig += para_izo_rta(fx + 46, fy - fh * .80, t, .1, 1.1, .5)
    s += SL(Z_SRED, fig + ten(fx, fy + 8, 152, 26, .5))

    let = ""
    for i in range(10):
        p = max(.0, min(1.0, (t * .62 + i * .07) % 1.0))
        mx = rx2 + (1086 - rx2) * p
        my = ry2 - 150 * math.sin(math.pi * p) + 520 * p * p
        let += _moneta_krupno(mx, my, 34, t, i * .2, True, False, .55 * p)
    s += SL(Z_SRED, let)
    s += SL(Z_PERED, _vetka_pered(-40, 70, 700, 24, t, 8, "#241c16", 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 14, 9, .4, .7))
    s += ramka_pp("oba")
    s += vinetka(.40)
    return s


def prohozhiy_i_chuzhaya_prosba(t):
    """Дорога за калиткой: парень в картузе приседает на колено и поднимает
    монету, из неё вылетает светящееся письмо-голубок и садится ему на плечо.
    Девушки в окнах задёргивают занавески одна за другой."""
    rnd = random.Random(104)
    gor = 430
    s = nebo("sumer", t, True, 19)
    s += oblaka(t, 120, 5, 11, .4)
    s += SL(Z_DAL, _derevnya_ryad(gor, t, 21, ((140, 470), (620, 390), (1180, 340),
                                               (1700, 440))))
    s += SL(Z_DAL, goloe_derevo(960, gor + 12, 330, t, 3, 7, "#2a2b33", True))
    s += SL(Z_DAL, teplo(620, gor - 150, 230, 180, .40) + teplo(1180, gor - 130, 200, 150, .38))
    s += SL(Z_DAL, _zabor_dosok(-20, 342, 1020, 190, 23, 52)
            + _zabor_dosok(1140, 350, 820, 186, 25, 54))

    zem = f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor}" fill="#45382a"/>'
    zem += (f'<path d="M-40,1080 Q300,{gor+320:.0f} 660,{gor+56:.0f}'
            f' L1280,{gor+56:.0f} Q1640,{gor+320:.0f} 1960,1080 Z" fill="#5e4830" {o(0)}/>')
    zem += _zemlya_faktura(gor + 100, 1060, 59, 18)
    zem += _koleya(820, 26, 2)
    zem += _listya(29, 36, gor + 80, 1060)
    zem += _trava(rnd, 13, gor + 70, 1050)
    zem += _inej(37, 40, gor + 70, 1060)
    s += SL(Z_SRED, zem)

    # колодец-сруб и поленница по сторонам дороги
    kx, ky = 1700, 900
    kol = (f'<rect x="{kx-170:.0f}" y="{ky-220:.0f}" width="340" height="220" rx="8"'
           f' fill="url(#derev)" {o(6)}/>')
    for i in range(4):
        kol += (f'<rect x="{kx-170:.0f}" y="{ky-216+i*54:.0f}" width="340" height="48"'
                f' rx="8" fill="url(#brev)" {o(3)}/>')
    kol += (f'<rect x="{kx-192:.0f}" y="{ky-246:.0f}" width="384" height="30" rx="8"'
            f' fill="#5b4428" {o(5)}/>'
            f'<ellipse cx="{kx:.0f}" cy="{ky-246:.0f}" rx="150" ry="26" fill="#160f0a"'
            f' {o(3)}/>')
    s += SL(Z_SRED, kol)
    s += SL(Z_SRED, _polenica(80, 620, 420, 280, 27, 27))
    s += SL(Z_SRED, _dvorovaya_utvar(1180, 1064, 460, t, 29, ["kadka", "korzina", "meshok"]))

    # парень: приседает на левое колено, правой поднимает монету
    uh = A.ease(A.seg(t, 2.6, 1.8))
    fx = 820 + 420 * uh
    fy = 1040
    fh = 560 - 110 * (1 - uh)
    fig = figura(fx, fy, fh, t, col="#3b3346", kant="#ffd98a", ph=.2, shapka=True,
                 naklon=-14 * (1 - uh))
    # РУКИ ОТ ПЛЕЧА И НАРУЖУ: прежде левый рукав на подъёме доходил до угла
    # 74° и шёл прямой палкой через грудь — в кадре это читалось посохом,
    # проткнувшим корпус (осмотр 15.11).
    ruk, (rx2, ry2), (psx, psy) = _ruka(fx, fy, fh, 1, fh * .52, 76 - 44 * uh,
                                        t, "#3b3346", "#ffd98a", .1, 7)
    fig += ruk
    ruk2, _, (plx, ply) = _ruka(fx, fy, fh, -1, fh * .40, 96 - 26 * uh, t,
                                "#3b3346", "#ffd98a", .5, 5)
    fig += ruk2
    # колено на земле, пока не встал
    if uh < .9:
        fig += (f'<path d="M{fx-80:.0f},{fy-10:.0f} L{fx-10:.0f},{fy-170*(1-uh)-30:.0f}'
                f' L{fx+40:.0f},{fy-6:.0f} Z" fill="#3b3346" opacity="{1-uh:.2f}" {o(5)}/>')
    fig += para_izo_rta(fx + 50, fy - fh * .80, t, .3, 1.1, .5)
    s += SL(Z_SRED, fig + ten(fx, fy + 8, 120, 22, .45))
    s += SL(Z_SRED, _moneta_krupno(770, 990, 110, t, .3, True, True, .6))

    # письмо-голубок с сердечком садится на плечо
    gp = A.ease(A.seg(t, 1.3, 1.4))
    gx = 770 + (psx - 770) * gp
    gy = 990 + (psy - 50 - 990) * gp - 200 * math.sin(math.pi * gp)
    kr = 30 * A.w(t, .34, .0)
    gol = (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="80" fill="#ffe9ac" opacity=".30"/>'
           f'<path d="M{gx-54:.0f},{gy:.0f} L{gx+54:.0f},{gy-26:.0f}'
           f' L{gx+54:.0f},{gy+26:.0f} Z" fill="#f6ecd4" {o(3)}/>'
           f'<path d="M{gx-14:.0f},{gy-12:.0f} Q{gx+16:.0f},{gy-62-kr:.0f}'
           f' {gx+52:.0f},{gy-22:.0f} Z" fill="#fff6dd" {o(3)}/>'
           f'<path d="M{gx-14:.0f},{gy+12:.0f} Q{gx+16:.0f},{gy+62+kr:.0f}'
           f' {gx+52:.0f},{gy+22:.0f} Z" fill="#f0e2c4" {o(3)}/>'
           f'<path d="M{gx+6:.0f},{gy-36:.0f} Q{gx+20:.0f},{gy-58:.0f}'
           f' {gx+34:.0f},{gy-36:.0f} Q{gx+46:.0f},{gy-16:.0f} {gx+20:.0f},{gy-2:.0f}'
           f' Q{gx-6:.0f},{gy-16:.0f} {gx+6:.0f},{gy-36:.0f} Z" fill="{KRAS}" {o(2)}/>')
    s += SL(Z_SRED, gol)

    # занавески в окнах задёргиваются по очереди
    zan = ""
    for i, (ox, oy) in enumerate(((548, gor - 200), (1116, gor - 170), (1646, gor - 210))):
        z = A.ease(A.seg(t, 1.0 + i * .4, .6))
        zan += (f'<rect x="{ox-10:.0f}" y="{oy-10:.0f}" width="132" height="150" rx="6"'
                f' fill="#4a3522" {o(4)}/>'
                f'<rect x="{ox:.0f}" y="{oy:.0f}" width="112" height="130" rx="5"'
                f' fill="#f2d79a" opacity="{.88-.55*z:.2f}" {o(3)}/>'
                f'<rect x="{ox:.0f}" y="{oy:.0f}" width="{56*z:.0f}" height="130"'
                f' fill="{TKAN}" {o(2)}/>'
                f'<rect x="{ox+112-56*z:.0f}" y="{oy:.0f}" width="{56*z:.0f}" height="130"'
                f' fill="{TKAN}" {o(2)}/>'
                f'<line x1="{ox+56:.0f}" y1="{oy:.0f}" x2="{ox+56:.0f}" y2="{oy+130:.0f}"'
                f' stroke="#4a3522" stroke-width="6"/>'
                f'<rect x="{ox-22:.0f}" y="{oy-26:.0f}" width="156" height="22" rx="6"'
                f' fill="#6a5030" {o(3)}/>')
    s += SL(Z_SRED, zan)
    s += SL(Z_PERED, _stolb_pered(1860, 120, "#1d1611", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 11, .45, .8))
    s += ramka_pp("levo")
    s += vinetka(.42)
    return s


def muzh_zhena_i_moneta_u_kolodca(t):
    """Колодец с журавлём на пол-кадра: муж тянется к монете у сруба, жена
    держит его за рукав и показывает на ворону, севшую на журавль."""
    rnd = random.Random(105)
    gor = 460
    s = nebo("sumer", t, True, 29)
    s += oblaka(t, 120, 4, 13, .4)
    s += SL(Z_DAL, _derevnya_ryad(gor, t, 31, ((170, 420), (600, 330), (1800, 400))))
    s += SL(Z_DAL, goloe_derevo(420, gor + 14, 440, t, 5, 9, "#2a2b33", True)
            + goloe_derevo(1640, gor + 10, 300, t, 15, 7, "#2a2b33", True))
    s += SL(Z_DAL, _zabor_dosok(-20, 344, 1100, 200, 33, 52)
            + _zabor_dosok(1280, 352, 680, 196, 34, 54))
    s += SL(Z_DAL, teplo(600, gor - 130, 220, 170, .40))

    zem = f'<rect x="0" y="{gor:.0f}" width="{W}" height="{H-gor}" fill="#473626"/>'
    zem += (f'<path d="M-40,1080 Q420,{gor+300:.0f} 820,{gor+70:.0f}'
            f' L1160,{gor+70:.0f} Q1540,{gor+300:.0f} 1960,1080 Z" fill="#59452e" {o(0)}/>')
    zem += _zemlya_faktura(gor + 90, 1060, 55, 16)
    zem += _listya(39, 30, gor + 80, 1060)
    zem += _trava(rnd, 13, gor + 70, 1050)
    zem += _inej(41, 38, gor + 70, 1060)
    s += SL(Z_SRED, zem)

    # сруб колодца крупно
    kx, ky, kw = 900, 1010, 470
    kol = ""
    for i in range(6):
        kol += (f'<rect x="{kx-kw/2:.0f}" y="{ky-346+i*58:.0f}" width="{kw:.0f}"'
                f' height="54" rx="12" fill="url(#brev)" {o(5)}/>'
                f'<ellipse cx="{kx-kw/2+10:.0f}" cy="{ky-319+i*58:.0f}" rx="18" ry="26"'
                f' fill="#5e442a" {o(3)}/>'
                f'<ellipse cx="{kx+kw/2-10:.0f}" cy="{ky-319+i*58:.0f}" rx="18" ry="26"'
                f' fill="#5e442a" {o(3)}/>')
    kol += (f'<rect x="{kx-kw/2-30:.0f}" y="{ky-378:.0f}" width="{kw+60:.0f}" height="36"'
            f' rx="10" fill="#5b4428" {o(5)}/>'
            f'<ellipse cx="{kx:.0f}" cy="{ky-378:.0f}" rx="{kw*.44:.0f}" ry="42"'
            f' fill="#160f0a" {o(4)}/>'
            f'<ellipse cx="{kx:.0f}" cy="{ky-368:.0f}" rx="{kw*.34:.0f}" ry="30"'
            f' fill="#3b5560" opacity=".55"/>')
    s += SL(Z_SRED, kol)

    # журавль: столб, коромысло, шест, ведро на цепи
    jx, jy = 1420, 1020
    kach = 4.0 * A.w(t, 2.6, .1)
    jur = (f'<rect x="{jx-28:.0f}" y="{jy-620:.0f}" width="56" height="620" rx="10"'
           f' fill="#3f2d1c" {o(6)}/>'
           f'<path d="M{jx-70:.0f},{jy-40:.0f} L{jx-28:.0f},{jy-180:.0f}'
           f' M{jx+70:.0f},{jy-40:.0f} L{jx+28:.0f},{jy-180:.0f}" stroke="#3f2d1c"'
           f' stroke-width="20" fill="none"/>'
           f'<g transform="rotate({kach:.1f} {jx:.0f} {jy-620:.0f})">'
           f'<rect x="{jx-500:.0f}" y="{jy-652:.0f}" width="860" height="38" rx="12"'
           f' fill="#4e3a24" {o(5)}/>'
           f'<rect x="{jx+300:.0f}" y="{jy-680:.0f}" width="110" height="100" rx="14"'
           f' fill="#2f261c" {o(4)}/>'
           f'<line x1="{jx-472:.0f}" y1="{jy-614:.0f}" x2="{jx-458:.0f}" y2="{jy-360:.0f}"'
           f' stroke="{ZHELEZ}" stroke-width="8"/>'
           f'<path d="M{jx-512:.0f},{jy-360:.0f} L{jx-404:.0f},{jy-360:.0f}'
           f' L{jx-420:.0f},{jy-240:.0f} L{jx-496:.0f},{jy-240:.0f} Z" fill="url(#zhel)"'
           f' {o(5)}/>'
           f'<path d="M{jx-512:.0f},{jy-360:.0f} Q{jx-458:.0f},{jy-428:.0f}'
           f' {jx-404:.0f},{jy-360:.0f}" fill="none" stroke="{ZHELEZ}" stroke-width="8"/>'
           f'</g>')
    s += SL(Z_SRED, jur)

    # ворона садится на журавль
    vp = A.ease(A.seg(t, .6, 1.3))
    vx = 1900 - 440 * vp
    vy = 150 + (jy - 690 - 150) * vp
    kryl = 1 - vp
    vor = (f'<ellipse cx="{vx:.0f}" cy="{vy:.0f}" rx="72" ry="46" fill="#14110f" {o(3)}/>'
           f'<circle cx="{vx-62:.0f}" cy="{vy-24:.0f}" r="34" fill="#14110f" {o(3)}/>'
           f'<path d="M{vx-92:.0f},{vy-26:.0f} L{vx-150:.0f},{vy-12:.0f}'
           f' L{vx-92:.0f},{vy-2:.0f} Z" fill="#6a6258" {o(2)}/>'
           f'<circle cx="{vx-72:.0f}" cy="{vy-32:.0f}" r="5" fill="#d8cfbd"/>'
           f'<path d="M{vx+14:.0f},{vy-12:.0f} Q{vx+40:.0f},{vy-78-64*kryl:.0f}'
           f' {vx+112:.0f},{vy-34-38*kryl:.0f} Q{vx+64:.0f},{vy+6:.0f} {vx+14:.0f},{vy+8:.0f} Z"'
           f' fill="#1d1916" {o(2)}/>'
           f'<path d="M{vx+52:.0f},{vy+20:.0f} L{vx+146:.0f},{vy+52:.0f}'
           f' L{vx+58:.0f},{vy+44:.0f} Z" fill="#14110f" {o(2)}/>')
    s += SL(Z_SRED, vor)

    # муж тянется и выпрямляется
    mx, my, mh = 600, 1030, 560
    tyan = A.ease(abs(A.w(t, 2.4, .0)))
    muzh = figura(mx, my, mh, t, col="#2f2a38", kant="#cfe4f5", ph=.2, shapka=True,
                  naklon=-22 * tyan)
    # ОБЕ РУКИ ОТ ПЛЕЧА И НАРУЖУ. Было: правый рукав брусок, левый под 20°
    # шёл поперёк груди (осмотр 15.11 — «обе руки брусками, одна поперёк
    # груди»). Монета переехала к подножию сруба СПРАВА от мужа, чтобы
    # тянулся он наружу, а не через собственный корпус.
    ruk, (rx2, ry2), (mpx, mpy) = _ruka(mx, my, mh, 1, mh * .58, 52 + 26 * tyan,
                                        t, "#2f2a38", "#cfe4f5", .1, 7)
    muzh += ruk
    ruk2, _, (mlx, mly) = _ruka(mx, my, mh, -1, mh * .42, 82, t,
                                "#2f2a38", "#cfe4f5", .5, 5)
    muzh += ruk2
    muzh += para_izo_rta(mx + 48, my - mh * .80, t, .2, 1.1, .5)
    s += SL(Z_SRED, muzh)
    s += SL(Z_SRED, _moneta_krupno(886, 1032, 72, t, .4))

    # жена: правой показывает на ворону, левой держит ведро — за рукав мужа
    # она тянулась НАСКВОЗЬ своей груди, этого в кадре быть не должно
    zx, zy, zh = 260, 1050, 540
    zhena = figura(zx, zy, zh, t, col="#5a2f33", kant="#cfe4f5", platok=True, ph=.5)
    ruk3, (ux, uy), (zpx, zpy) = _ruka(zx, zy, zh, 1, zh * .54, -56, t,
                                       "#5a2f33", "#cfe4f5", .3, 6)
    zhena += ruk3
    ruk4, (vdx, vdy), (zlx, zly) = _ruka(zx, zy, zh, -1, zh * .46, 74, t,
                                         "#5a2f33", "#cfe4f5", .7, 5)
    zhena += ruk4
    vkach = 6 * A.w(t, 1.4, .3)
    zhena += (f'<g transform="rotate({vkach:.1f} {vdx:.0f} {vdy:.0f})">'
              f'<path d="M{vdx-62:.0f},{vdy+14:.0f} L{vdx+62:.0f},{vdy+14:.0f}'
              f' L{vdx+46:.0f},{vdy+136:.0f} L{vdx-46:.0f},{vdy+136:.0f} Z"'
              f' fill="url(#zhel)" {o(5)}/>'
              f'<rect x="{vdx-66:.0f}" y="{vdy+8:.0f}" width="132" height="20" rx="8"'
              f' fill="{ZHELEZ}" {o(3)}/>'
              f'<ellipse cx="{vdx:.0f}" cy="{vdy+30:.0f}" rx="48" ry="14"'
              f' fill="#3b5560" opacity=".6"/>'
              f'<path d="M{vdx-44:.0f},{vdy+10:.0f} Q{vdx:.0f},{vdy-54:.0f}'
              f' {vdx+44:.0f},{vdy+10:.0f}" fill="none" stroke="{ZHELEZ}"'
              f' stroke-width="9"/></g>')
    zhena += para_izo_rta(zx + 42, zy - zh * .80, t, .6, 1.1, .5)
    s += SL(Z_SRED, zhena)
    s += SL(Z_SRED, ten(mx, my + 8, 120, 22, .45) + ten(zx, zy + 8, 110, 20, .45))

    s += SL(Z_SRED, _dvorovaya_utvar(60, 1060, 320, t, 43, ["vedro", "vedro"]))
    kor = (f'<path d="M1020,700 Q1180,632 1360,702" fill="none" stroke="url(#derev)"'
           f' stroke-width="28" stroke-linecap="round"/>'
           f'<rect x="1006" y="688" width="36" height="52" rx="8" fill="#4a3522" {o(3)}/>'
           f'<rect x="1346" y="690" width="36" height="52" rx="8" fill="#4a3522" {o(3)}/>')
    s += SL(Z_SRED, kor)
    s += SL(Z_SRED, _polenica(1600, 540, 340, 260, 45, 26))
    s += SL(Z_DAL, izba_snaruzhi(1700, 700, 520, t, True, True, 46))
    s += SL(Z_SRED, _dvorovaya_utvar(760, 640, 300, t, 48, ["vedro", "krynka"]))
    s += SL(Z_SRED, _polka_s_utvaryu(1040, 560, 330, t, 49, 3))
    gr = ""
    for i, (gx_, gy_) in enumerate(((330, 352), (470, 350), (1560, 358))):
        kl = 6 * A.w(t, 2.4, i * .3)
        gr += (f'<ellipse cx="{gx_:.0f}" cy="{gy_-30:.0f}" rx="34" ry="22"'
               f' fill="#1b1714" {o(2)}/>'
               f'<circle cx="{gx_-28:.0f}" cy="{gy_-42:.0f}" r="16" fill="#1b1714" {o(2)}/>'
               f'<path d="M{gx_-42:.0f},{gy_-44:.0f} L{gx_-70:.0f},{gy_-38:.0f}'
               f' L{gx_-42:.0f},{gy_-32:.0f} Z" fill="#6a6258" {o(2)}/>'
               f'<path d="M{gx_+6:.0f},{gy_-36:.0f} Q{gx_+22:.0f},{gy_-62-kl:.0f}'
               f' {gx_+52:.0f},{gy_-42:.0f} Q{gx_+28:.0f},{gy_-22:.0f}'
               f' {gx_+6:.0f},{gy_-22:.0f} Z" fill="#241f1b" {o(2)}/>')
    s += SL(Z_SRED, gr)
    s += SL(Z_PERED, _vetka_pered(-40, 70, 760, 26, t, 47, "#241c16", 7))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 13, .45, .8))
    s += ramka_pp("oba")
    s += vinetka(.42)
    return s


def dva_venika_u_krylca(t):
    """Крыльцо избы и два веника НА ПОЛ-КАДРА: слева чужой, растрёпанный, с
    красной тряпицей, справа новенький жёлтый с биркой. Хозяйка тянется к
    обоим, отдёргивает руку и берёт из сеней свой, старый и тёмный."""
    rnd = random.Random(106)
    s = nebo("sumer", t, True, 23)
    s += oblaka(t, 120, 4, 15, .36)
    s += SL(Z_DAL, _derevnya_ryad(520, t, 51, ((120, 300), (1820, 280))))

    # стена избы за крыльцом
    s += SL(Z_DAL, brevna(240, 0, 1460, 700, 92)
            + f'<rect x="240" y="0" width="1460" height="700" fill="none" {o(10)}/>')
    s += SL(Z_DAL, okno_izby(1300, 120, 320, 270, t, svet=True)
            + teplo(1460, 256, 280, 230, .44))
    s += SL(Z_DAL, dver(420, 110, 300, 520, .22, "url(#derev)", True, False))
    s += SL(Z_DAL, podkova(570, 70, 1.6, t))
    s += SL(Z_DAL, _polka_s_utvaryu(800, 250, 440, t, 77, 3))

    zem = f'<rect x="0" y="760" width="{W}" height="320" fill="#473626"/>'
    zem += _zemlya_faktura(820, 1060, 61, 14)
    zem += _listya(55, 26, 820, 1060)
    zem += _inej(57, 32, 820, 1060)
    s += SL(Z_SRED, zem)
    s += SL(Z_SRED, _kryl_co(240, 700, 1200, 190, t, 3, True, False))

    def venik(vx, vy, h2, col, tryap, birka, rastr, ph, s_=1.0):
        kach = 3.4 * A.w(t, 2.2, ph)
        g = f'<g transform="rotate({kach:.1f} {vx:.0f} {vy:.0f})">'
        rr = random.Random(int(vx))
        n = 23
        for i in range(n):
            p = (i / (n - 1.0)) - .5
            raz = (1.0 + rastr * rr.uniform(0, 1.6))
            ex = vx + p * 180 * s_ * raz
            ey = vy - h2 + rr.uniform(-30, 20) * raz
            g += (f'<path d="M{vx+p*34*s_:.0f},{vy-h2*.40:.0f}'
                  f' Q{vx+p*118*s_:.0f},{vy-h2*.76:.0f} {ex:.0f},{ey:.0f}"'
                  f' fill="none" stroke="{col}" stroke-width="{9*s_:.0f}"'
                  f' stroke-linecap="round" opacity=".92"/>')
        g += (f'<rect x="{vx-28*s_:.0f}" y="{vy-h2*.42:.0f}" width="{56*s_:.0f}"'
              f' height="{h2*.46:.0f}" rx="18" fill="url(#derev)" {o(5)}/>'
              f'<rect x="{vx-44*s_:.0f}" y="{vy-h2*.50:.0f}" width="{88*s_:.0f}"'
              f' height="{34*s_:.0f}" rx="12" fill="{tryap}" {o(4)}/>'
              f'<rect x="{vx-40*s_:.0f}" y="{vy-h2*.28:.0f}" width="{80*s_:.0f}"'
              f' height="{24*s_:.0f}" rx="10" fill="#8a6a3c" {o(3)}/>')
        if tryap == "#b8352c":
            tr = 8 * A.w(t, 1.7, ph + .5)
            g += (f'<path d="M{vx+40*s_:.0f},{vy-h2*.48:.0f}'
                  f' Q{vx+86*s_+tr:.0f},{vy-h2*.42:.0f} {vx+70*s_:.0f},{vy-h2*.30:.0f} Z"'
                  f' fill="#b8352c" {o(3)}/>')
        if birka:
            bk = 4 * A.w(t, 1.8, ph + .3)
            g += (f'<g transform="rotate({bk:.1f} {vx+34*s_:.0f} {vy-h2*.28:.0f})">'
                  f'<line x1="{vx+34*s_:.0f}" y1="{vy-h2*.28:.0f}"'
                  f' x2="{vx+52*s_:.0f}" y2="{vy-h2*.14:.0f}" stroke="#cbbb98"'
                  f' stroke-width="4"/>'
                  f'<rect x="{vx+34*s_:.0f}" y="{vy-h2*.14:.0f}" width="{52*s_:.0f}"'
                  f' height="{68*s_:.0f}" rx="8" fill="#efe4c8" {o(4)}/>'
                  f'<path d="M{vx+44*s_:.0f},{vy-h2*.14+30*s_:.0f}'
                  f' Q{vx+58*s_:.0f},{vy-h2*.14+20*s_:.0f}'
                  f' {vx+74*s_:.0f},{vy-h2*.14+30*s_:.0f}" fill="none" stroke="#9a8a68"'
                  f' stroke-width="4"/></g>')
        g += "</g>"
        return g

    s += SL(Z_SRED, venik(560, 1000, 620, "#8a7246", "#b8352c", False, 1.0, .0, 1.25))
    s += SL(Z_SRED, venik(1080, 1000, 640, "url(#solom)", "#c8a24a", True, .0, .4, 1.25))
    s += SL(Z_SRED, f'<rect x="250" y="940" width="380" height="64" rx="10" fill="{RUSH}"'
                    f' {o(4)}/>'
                    f'<path d="M272,956 L612,956 M272,984 L612,984" stroke="{KRAS}"'
                    f' stroke-width="8" opacity=".7"/>')
    for i, lx in enumerate((760, 880)):
        s += SL(Z_SRED, f'<path d="M{lx:.0f},1030 Q{lx+48:.0f},974 {lx+96:.0f},1030'
                        f' Q{lx+48:.0f},1060 {lx:.0f},1030 Z" fill="url(#solom)" {o(4)}/>'
                        f'<path d="M{lx+16:.0f},1016 L{lx+80:.0f},1016" stroke="#8a6a3c"'
                        f' stroke-width="5"/>')
    s += SL(Z_SRED, _dvorovaya_utvar(1240, 1060, 330, t, 59, ["kadka", "vedro"]))
    s += SL(Z_SRED, _kucha_listev(1760, 1050, 300, 67, 96)
            + _luzha(960, 1058, 210, t, .2))
    s += SL(Z_SRED, _polenica(20, 760, 240, 220, 63, 25))

    # ФИГУРА ЦЕЛИКОМ В КАДРЕ И РУКИ НАРУЖУ. Было: хозяйка стояла у самого
    # правого края, указующая рука шла от ПРАВОГО плеча налево — прямым
    # бруском через подбородок и голову, а на дальней цели кисть уезжала за
    # холст. Теперь показывает ЛЕВАЯ рука (цели все слева), веник держит
    # правая, и обе уложены внутрь кадра (осмотр 15.11).
    fx, fy, fh = 1468, 1016, 620
    faza = (t * .55) % 1.0
    cel = 560 if faza < .34 else (1080 if faza < .68 else 300)
    otd = .5 + .5 * math.sin(faza * 3 * 2 * math.pi)
    fig = figura(fx, fy, fh, t, col="#4a3b2a", kant="#ffd98a", platok=True, ph=.2)
    lpx, lpy = _plecho(fx, fy, fh, -1)
    ang = math.degrees(math.atan2(820 - lpy, lpx - cel))
    ruk, _, _ = _ruka(fx, fy, fh, -1, fh * (.30 + .20 * otd), ang, t,
                      "#4a3b2a", "#ffd98a", .1, 6)
    fig += ruk
    ruk2, (bx, by), (rpx, rpy) = _ruka(fx, fy, fh, 1, fh * .34, 64, t,
                                       "#4a3b2a", "#ffd98a", .3, 5)
    fig += ruk2
    # веник держится ЗА ЧЕРЕНОК, прутья смотрят вниз-вперёд
    fig += (f'<g transform="rotate(168 {bx:.0f} {by:.0f})">'
            + venik(bx, by, 300, "#4b3f28", "#5a4a2e", False, .25, .7, .8) + "</g>")
    fig += para_izo_rta(fx - 48, fy - fh * .80, t, .4, 1.1, .5)
    s += SL(Z_SRED, fig + ten(fx, fy + 8, 140, 24, .45))
    s += SL(Z_PERED, _stolb_pered(-6, 100, "#1d1611", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 17, .4, .7))
    s += ramka_pp("pravo")
    s += vinetka(.42)
    return s


def tri_otlozhennyh_dela(t):
    """Горница: стол с фартуком, подносом и караваем, дед в жилетке за столом
    отодвигает дело за делом. Ходики, окно с занавеской, полки с утварью."""
    rnd = random.Random(107)
    pol = 740
    s = _stena_gornicy(t, 5, True, pol)
    s += SL(Z_DAL, f'<rect x="0" y="86" width="{W}" height="30" fill="#3b2a1a" opacity=".8"/>'
                   f'<rect x="880" y="0" width="34" height="{pol:.0f}" fill="#4e3220"'
                   f' opacity=".75"/>')
    s += SL(Z_DAL, okno_izby(1320, 190, 360, 300, t, svet=False, moroz=.5))
    s += SL(Z_DAL, zanaveska(1320, 180, 170, 130, TKAN, t, 1)
            + zanaveska(1680, 180, 170, 130, TKAN, t, -1))
    s += SL(Z_DAL, hodiki(300, 180, t, 1.7))
    s += SL(Z_DAL, _polka_s_utvaryu(520, 300, 560, t, 11, 4))
    s += SL(Z_DAL, utvar_izby(1140, 330, 420, t, 7))
    s += SL(Z_SRED, lampa(960, 230, t, 1.5, True) + teplo(960, 420, 420, 320, .44))
    s += SL(Z_SRED, _polka_s_utvaryu(1180, 560, 560, t, 379, 4))
    s += SL(Z_SRED, _dvorovaya_utvar(980, 1070, 520, t, 381,
                                     ["kadka", "vedro", "korzina"]))
    s += SL(Z_SRED, f'<rect x="620" y="620" width="300" height="140" rx="10"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<path d="M620,620 Q770,566 920,620 Z" fill="#5b4428" {o(5)}/>'
                    f'<rect x="610" y="658" width="320" height="18" rx="7"'
                    f' fill="{ZHELEZ}" {o(3)}/>')

    s += SL(Z_SRED, mebel_hlam(180, 900, 420, t, 13))
    s += SL(Z_SRED, lavka(1340, 930, 480))
    s += SL(Z_SRED, _kot_zhivoy(1500, 1040, t, 1.4, "#4a423c", .2, True, True))

    # стол во всю ширину кадра
    sx, sy, sw = 960, 880, 1320
    stl = (f'<rect x="{sx-sw/2:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="46" rx="10"'
           f' fill="url(#dosk)" {o(6)}/>'
           f'<rect x="{sx-sw/2:.0f}" y="{sy+46:.0f}" width="{sw:.0f}" height="20"'
           f' fill="#3a2a1a" opacity=".8"/>')
    for px in (sx - sw / 2 + 60, sx + sw / 2 - 100):
        stl += (f'<rect x="{px:.0f}" y="{sy+66:.0f}" width="44" height="180" rx="8"'
                f' fill="#4a3522" {o(4)}/>')
    s += SL(Z_SRED, stl)

    sd1 = A.ease(A.seg(t, .5, 1.0))
    sd2 = A.ease(A.seg(t, 1.9, 1.0))
    sd3 = A.ease(A.seg(t, 3.3, 1.0))

    # 1. рабочий фартук с рукавицами
    f1x = 470 - 260 * sd1
    far = (f'<path d="M{f1x-90:.0f},{sy-24:.0f} L{f1x-60:.0f},{sy-186:.0f}'
           f' L{f1x+60:.0f},{sy-186:.0f} L{f1x+90:.0f},{sy-24:.0f} Z"'
           f' fill="#6b5a3c" opacity="{1-sd1*.5:.2f}" {o(5)}/>'
           f'<line x1="{f1x-60:.0f}" y1="{sy-186:.0f}" x2="{f1x-150:.0f}" y2="{sy-120:.0f}"'
           f' stroke="#6b5a3c" stroke-width="12" opacity="{1-sd1*.5:.2f}"/>'
           f'<line x1="{f1x+60:.0f}" y1="{sy-186:.0f}" x2="{f1x+150:.0f}" y2="{sy-120:.0f}"'
           f' stroke="#6b5a3c" stroke-width="12" opacity="{1-sd1*.5:.2f}"/>'
           f'<rect x="{f1x-56:.0f}" y="{sy-110:.0f}" width="112" height="60" rx="8"'
           f' fill="#584a30" opacity="{1-sd1*.5:.2f}" {o(3)}/>')
    for i, gx in enumerate((f1x - 120, f1x + 120)):
        far += (f'<path d="M{gx-36:.0f},{sy-20:.0f} L{gx-30:.0f},{sy-96:.0f}'
                f' Q{gx:.0f},{sy-124:.0f} {gx+30:.0f},{sy-96:.0f} L{gx+36:.0f},{sy-20:.0f} Z"'
                f' fill="#7a6342" opacity="{1-sd1*.5:.2f}" {o(4)}/>'
                f'<path d="M{gx+30:.0f},{sy-86:.0f} L{gx+58:.0f},{sy-66:.0f}'
                f' L{gx+40:.0f},{sy-44:.0f} Z" fill="#7a6342"'
                f' opacity="{1-sd1*.5:.2f}" {o(3)}/>')
    s += SL(Z_SRED, far)

    # 2. поднос с рушником и караваем
    f2x = 960 + 300 * sd2
    pod = (f'<ellipse cx="{f2x:.0f}" cy="{sy-14:.0f}" rx="210" ry="48" fill="url(#zhel)"'
           f' opacity="{1-sd2*.5:.2f}" {o(5)}/>'
           f'<path d="M{f2x-250:.0f},{sy-34:.0f} Q{f2x:.0f},{sy-86:.0f}'
           f' {f2x+250:.0f},{sy-34:.0f} L{f2x+250:.0f},{sy+4:.0f}'
           f' Q{f2x:.0f},{sy-44:.0f} {f2x-250:.0f},{sy+4:.0f} Z" fill="{RUSH}"'
           f' opacity="{1-sd2*.5:.2f}" {o(4)}/>')
    for i in range(6):
        ux = f2x - 220 + i * 88
        pod += (f'<path d="M{ux:.0f},{sy-30:.0f} L{ux+18:.0f},{sy-50:.0f}'
                f' L{ux+36:.0f},{sy-30:.0f} Z" fill="{KRAS}" opacity="{(1-sd2*.5)*.8:.2f}"/>')
    pod += karavay(f2x, sy - 50, 1.6, False)
    s += SL(Z_SRED, pod)

    # 3. две руки над столом, готовые к рукопожатию
    rx_, ry_ = 1310, sy - 110
    ruk1, _ = rukav(rx_ + 230, ry_ + 60, 210, 196, t, "#3a3142", "#cfe4f5", .2, 4, True)
    ruk3 = ruk1
    s += SL(Z_SRED, ruk3 + f'<ellipse cx="{rx_+30:.0f}" cy="{ry_+10:.0f}" rx="56" ry="34"'
                           f' fill="#3a3142" opacity="{1-sd3*.75:.2f}" {o(4)}/>')

    fx, fy, fh = 700, 846, 470
    ded = figura(fx, fy, fh, t, col="#3c3326", kant="#ffd98a", ph=.2, boroda=True)
    # Показывает на дела ПРАВАЯ рука (дела все справа от деда), левая просто
    # висит наружу. Было: левый рукав под -10° шёл прямой палкой через бороду
    # и голову на 163 px за ось тела (осмотр 15.11).
    ang = -4 - 26 * (sd1 + sd2 + sd3) / 3.0
    ruk, _, (dpx, dpy) = _ruka(fx, fy, fh, 1, fh * .52, ang, t,
                               "#3c3326", "#ffd98a", .1, 5)
    ded += ruk
    ruk2, _, (dlx, dly) = _ruka(fx, fy, fh, -1, fh * .46, 70 - 18 * sd3, t,
                                "#3c3326", "#ffd98a", .5, 4)
    ded += ruk2
    s += SL(Z_SRED, ded)
    s += SL(Z_SRED, krynka(240, sy - 10, 1.3) + monety(1700, sy - 20, t, 4, 3, 1.2))
    s += SL(Z_SRED, f'<path d="M460,1004 L1460,1004 L1600,1076 L320,1076 Z"'
                    f' fill="{RUSH}" {o(5)}/>'
                    f'<path d="M486,1030 L1472,1030 M466,1056 L1540,1056"'
                    f' stroke="{KRAS}" stroke-width="9" opacity=".6"/>')
    s += SL(Z_SRED, _dvorovaya_utvar(560, 1070, 560, t, 375,
                                     ["korzina", "kadka", "korob"]))
    s += SL(Z_DAL, _polka_s_utvaryu(540, 520, 520, t, 81, 4))
    s += SL(Z_DAL, utvar_izby(180, 420, 300, t, 9))
    s += SL(Z_SRED, _dvorovaya_utvar(100, 1040, 420, t, 83, ["kadka", "korob", "korzina"]))
    s += SL(Z_SRED, lavka(120, 980, 420))
    uhv = ""
    for i, ux in enumerate((1760, 1820, 1876)):
        uhv += (f'<rect x="{ux:.0f}" y="{520+i*18:.0f}" width="16" height="420" rx="7"'
                f' fill="url(#derev)" {o(3)}/>')
    uhv += (f'<path d="M1748,520 Q1768,476 1792,520" fill="none" stroke="{ZHELEZ}"'
            f' stroke-width="12"/>'
            f'<rect x="1806" y="500" width="34" height="44" rx="8" fill="{CHUGUN}" {o(3)}/>')
    s += SL(Z_SRED, uhv)
    s += SL(Z_PERED, _stolb_pered(1840, 120, "#140f0b", 0, H))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def torgovyy_gorod_na_reke(t):
    """Старинный деревянный город над рекой: бревенчатые стены с башнями,
    пристань с ладьями, торг с навесами, дымы над крышами. В проёме ворот —
    настоящая река. У ворот один стоит маленький мальчик."""
    rnd = random.Random(108)
    s = nebo("den", t, False, 37)
    s += oblaka(t, 130, 6, 19, .5)

    px_, py_, pw_, ph_ = 1110, 258, 770, 400
    put = kontur_proema(px_, py_, pw_, ph_, "arka")
    s += SL(Z_DAL, _vid_za_proemom(put, t, "reka", 9)
            + mesto_stoka(px_, py_, pw_, ph_, "arka")
            + f'<path d="{put}" fill="none" stroke="#2a1d12" stroke-width="18"/>')

    sten = ""
    for bx, bw in ((-20, 900), (1880, 80)):
        sten += (f'<rect x="{bx:.0f}" y="250" width="{bw:.0f}" height="510" rx="6"'
                 f' fill="url(#brev)" {o(6)}/>')
        for i in range(9):
            sten += (f'<rect x="{bx:.0f}" y="{256+i*56:.0f}" width="{bw:.0f}" height="48"'
                     f' rx="8" fill="url(#brev)" {o(3)}/>')
        for i in range(int(bw // 76)):
            zx = bx + 8 + i * 76
            sten += (f'<rect x="{zx:.0f}" y="196" width="58" height="58" rx="6"'
                     f' fill="#5b4428" {o(4)}/>')
        for i in range(int(bw // 160)):
            zx = bx + 40 + i * 160
            sten += (f'<rect x="{zx:.0f}" y="330" width="34" height="76" rx="6"'
                     f' fill="#1a120c" {o(3)}/>')
    for bx in (280, 1000):
        sten += (f'<rect x="{bx-130:.0f}" y="120" width="260" height="640" rx="8"'
                 f' fill="url(#brev)" {o(6)}/>')
        for i in range(10):
            sten += (f'<rect x="{bx-130:.0f}" y="{126+i*62:.0f}" width="260" height="54"'
                     f' rx="8" fill="url(#brev)" {o(3)}/>')
        sten += (f'<path d="M{bx-190:.0f},120 L{bx:.0f},-40 L{bx+190:.0f},120 Z"'
                 f' fill="#4a3a28" {o(5)}/>'
                 f'<rect x="{bx-200:.0f}" y="112" width="400" height="24" rx="8"'
                 f' fill="#5c4830" {o(4)}/>'
                 f'<rect x="{bx-66:.0f}" y="220" width="58" height="92" rx="8"'
                 f' fill="#1a120c" {o(4)}/>'
                 f'<rect x="{bx+14:.0f}" y="220" width="58" height="92" rx="8"'
                 f' fill="#1a120c" {o(4)}/>'
                 f'<rect x="{bx-66:.0f}" y="430" width="58" height="92" rx="8"'
                 f' fill="#1a120c" {o(4)}/>'
                 f'<rect x="{bx+14:.0f}" y="430" width="58" height="92" rx="8"'
                 f' fill="#1a120c" {o(4)}/>')
    # надвратный сруб и косяки проёма вместо створок
    sten += (f'<rect x="{px_-70:.0f}" y="{py_-120:.0f}" width="{pw_+140:.0f}"'
             f' height="140" rx="10" fill="url(#brev)" {o(6)}/>')
    for i in range(2):
        sten += (f'<rect x="{px_-70:.0f}" y="{py_-114+i*62:.0f}" width="{pw_+140:.0f}"'
                 f' height="54" rx="9" fill="url(#brev)" {o(3)}/>')
    for i in range(int((pw_ + 140) // 78)):
        sten += (f'<rect x="{px_-62+i*78:.0f}" y="{py_-178:.0f}" width="56" height="58"'
                 f' rx="6" fill="#5b4428" {o(4)}/>')
    sten += (f'<rect x="{px_-74:.0f}" y="{py_+10:.0f}" width="74"'
             f' height="{ph_+120:.0f}" rx="8" fill="#3b2a1a" {o(6)}/>'
             f'<rect x="{px_+pw_:.0f}" y="{py_+10:.0f}" width="74"'
             f' height="{ph_+120:.0f}" rx="8" fill="#3b2a1a" {o(6)}/>'
             f'<rect x="{px_-74:.0f}" y="{py_+ph_+90:.0f}" width="{pw_+148:.0f}"'
             f' height="34" rx="10" fill="#4e3a24" {o(5)}/>')
    for i in range(5):
        sten += (f'<circle cx="{px_-38:.0f}" cy="{py_+70+i*86:.0f}" r="14"'
                 f' fill="{ZHELEZ}" {o(3)}/>'
                 f'<circle cx="{px_+pw_+36:.0f}" cy="{py_+70+i*86:.0f}" r="14"'
                 f' fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, sten)

    for i, dx in enumerate((280, 640, 1000, 1880)):
        s += SL(Z_SRED, dym(dx, 90 + (i % 2) * 50, t, 5, .24, 300, .34, "#d3dae2", .9))

    zem = f'<rect x="0" y="700" width="{W}" height="380" fill="#4e3f2c"/>'
    zem += f'<rect x="0" y="700" width="{W}" height="26" fill="#6a553a" opacity=".8"/>'
    zem += _zemlya_faktura(760, 1060, 57, 18)
    zem += _listya(61, 28, 740, 1060)
    s += SL(Z_SRED, zem)
    # торговый настил через всю середину: доски, бочки, короба, мешки
    nast = (f'<rect x="230" y="748" width="1460" height="54" rx="12"'
            f' fill="url(#dosk)" {o(7)}/>'
            f'<rect x="230" y="802" width="1460" height="26" fill="#3a2a1a"'
            f' opacity=".85"/>')
    for i in range(6):
        nast += (f'<rect x="{300+i*260:.0f}" y="828" width="48" height="160" rx="9"'
                 f' fill="#4a3522" {o(4)}/>')
    s += SL(Z_SRED, nast)
    s += SL(Z_SRED, _dvorovaya_utvar(300, 744, 560, t, 331,
                                     ["kadka", "korzina", "meshok"]))
    s += SL(Z_SRED, _dvorovaya_utvar(560, 744, 500, t, 333,
                                     ["korob", "kadka", "vedro"]))
    s += SL(Z_SRED, _polenica(260, 836, 300, 200, 335, 25))
    s += SL(Z_SRED, _polenica(1340, 836, 300, 200, 337, 25))

    pr = f'<rect x="-20" y="870" width="660" height="36" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(6):
        pr += (f'<rect x="{20+i*118:.0f}" y="906" width="32" height="150" rx="6"'
               f' fill="#4a3522" {o(4)}/>')
    for i, (lx, ly, lw) in enumerate(((100, 1000, 460), (420, 1060, 400))):
        kach = 5 * A.w(t, 3.0 + i, i * .4)
        pr += (f'<g transform="rotate({kach:.1f} {lx+lw/2:.0f} {ly:.0f})">'
               f'<path d="M{lx:.0f},{ly:.0f} Q{lx+lw/2:.0f},{ly+78:.0f} {lx+lw:.0f},{ly:.0f}'
               f' L{lx+lw-34:.0f},{ly-50:.0f} L{lx+34:.0f},{ly-50:.0f} Z"'
               f' fill="url(#derev)" {o(5)}/>'
               f'<path d="M{lx:.0f},{ly:.0f} L{lx-38:.0f},{ly-92:.0f}" stroke="#4a3522"'
               f' stroke-width="18" fill="none"/>'
               f'<path d="M{lx+lw:.0f},{ly:.0f} L{lx+lw+38:.0f},{ly-92:.0f}"'
               f' stroke="#4a3522" stroke-width="18" fill="none"/>'
               f'<rect x="{lx+lw/2-12:.0f}" y="{ly-280:.0f}" width="24" height="236"'
               f' fill="#4a3522" {o(3)}/>'
               f'<path d="M{lx+lw/2:.0f},{ly-270:.0f} L{lx+lw/2+120:.0f},{ly-200:.0f}'
               f' L{lx+lw/2:.0f},{ly-140:.0f} Z" fill="{KREM}" opacity=".5" {o(3)}/></g>')
    s += SL(Z_SRED, pr)

    trg = ""
    for i in range(2):
        tx = 420 + i * 300
        trg += (f'<path d="M{tx-124:.0f},820 L{tx:.0f},744 L{tx+124:.0f},820 Z"'
                f' fill="#8a6a3c" {o(5)}/>'
                f'<rect x="{tx-118:.0f}" y="816" width="236" height="22" rx="6"'
                f' fill="#5b4428" {o(4)}/>'
                f'<rect x="{tx-104:.0f}" y="838" width="28" height="170" rx="6"'
                f' fill="#4a3522" {o(3)}/>'
                f'<rect x="{tx+76:.0f}" y="838" width="28" height="170" rx="6"'
                f' fill="#4a3522" {o(3)}/>'
                f'<rect x="{tx-118:.0f}" y="948" width="236" height="32" rx="7"'
                f' fill="url(#dosk)" {o(4)}/>')
    s += SL(Z_SRED, trg)
    s += SL(Z_SRED, _dvorovaya_utvar(360, 1058, 760, t, 63))
    s += SL(Z_SRED, _polenica(40, 640, 280, 220, 65, 24))
    s += SL(Z_SRED, _polka_s_utvaryu(430, 950, 440, t, 67, 4))
    s += SL(Z_SRED, _dvorovaya_utvar(200, 904, 480, t, 407, ["korob", "meshok"]))
    s += SL(Z_SRED, _polka_s_utvaryu(620, 620, 420, t, 351, 4))
    s += SL(Z_SRED, _polka_s_utvaryu(560, 700, 420, t, 383, 4))
    s += SL(Z_SRED, _dvorovaya_utvar(620, 1062, 620, t, 385,
                                     ["kadka", "korob", "meshok"]))
    s += SL(Z_SRED, _polenica(900, 820, 260, 180, 387, 24))
    s += SL(Z_SRED, _kadushki_i_grabli(420, 1070, t, 157))
    s += SL(Z_SRED, _lavka_krupno(640, 1076, 420, t, 150))
    seti = ""
    for i in range(3):
        sx_ = 70 + i * 190
        seti += (f'<path d="M{sx_:.0f},880 L{sx_+150:.0f},880 L{sx_+120:.0f},1020'
                 f' L{sx_+30:.0f},1020 Z" fill="#6a6250" opacity=".55" {o(3)}/>')
        for k in range(5):
            seti += (f'<line x1="{sx_+12+k*32:.0f}" y1="884" x2="{sx_+30+k*22:.0f}"'
                     f' y2="1016" stroke="#8a8068" stroke-width="3" opacity=".7"/>'
                     f'<line x1="{sx_+4:.0f}" y1="{896+k*26:.0f}" x2="{sx_+146:.0f}"'
                     f' y2="{896+k*26:.0f}" stroke="#8a8068" stroke-width="3"'
                     f' opacity=".7"/>')
    s += SL(Z_SRED, seti)
    ptic = ""
    for i in range(7):
        bx_ = ((t * 26 + i * 290) % 2300) - 180
        by_ = 110 + (i % 3) * 54 + 12 * A.w(t, 2.0, i * .3)
        ptic += ptica(bx_, by_, t, .9, "#4a4a52", i * .2)
    s += SL(Z_DAL, ptic)
    s += SL(Z_SRED, teplo(640, 860, 280, 200, .34))

    fx, fy, fh = 1300, 1012, 340
    mal = figura(fx, fy, fh, t, col="#8e8068", kant="#cfe4f5", ph=.3)
    r1, _, (mpx, mpy) = _ruka_ekr(fx, fy, fh, 1, fh * .44, 84, t, "#8e8068", "#cfe4f5", .2, 4)
    r2, _, (mpx2, mpy2) = _ruka_ekr(fx, fy, fh, -1, fh * .44, 96, t, "#8e8068", "#cfe4f5", .6, 4)
    mal += r1 + r2
    mal += para_izo_rta(fx + 30, fy - fh * .80, t, .1, .9, .5)
    s += SL(Z_SRED, mal + ten(fx, fy + 6, 78, 15, .45))
    s += SL(Z_PERED, _stolb_pered(1870, 110, "#1d1611", 0, H))
    s += SL(Z_LETIT, sneg_letit(t, 16, 21, .4, .7))
    s += ramka_pp("oba")
    s += vinetka(.42)
    return s


def torg_i_malchik_ivan(t):
    """Торговый ряд: бочки с мёдом, связки мехов, весы с гирями, горшки,
    калачи на шесте. Купец кладёт гирю, покупательница с корзиной, мальчик
    прижимает берестяную грамотку."""
    rnd = random.Random(109)
    s = nebo("den", t, False, 41)
    s += oblaka(t, 140, 5, 23, .45)
    s += SL(Z_DAL, _derevnya_ryad(480, t, 67, ((170, 330), (1760, 310))))

    # навес торгового ряда во всю ширину
    nav = (f'<path d="M190,430 L960,248 L1730,430 Z" fill="#8a6a3c" {o(6)}/>'
           f'<rect x="200" y="416" width="1520" height="28" rx="9" fill="#5b4428" {o(5)}/>')
    for i in range(6):
        nx = 60 + i * 370
        nav += (f'<rect x="{nx:.0f}" y="436" width="34" height="380" rx="8"'
                f' fill="#4a3522" {o(4)}/>')
    s += SL(Z_DAL, nav)

    zem = f'<rect x="0" y="790" width="{W}" height="290" fill="#4e3f2c"/>'
    zem += _listya(69, 22, 820, 1060)
    zem += _inej(71, 26, 830, 1060)
    s += SL(Z_SRED, zem)

    # прилавок
    pr = (f'<rect x="210" y="818" width="1480" height="58" rx="12"'
          f' fill="url(#dosk)" {o(7)}/>'
          f'<rect x="210" y="876" width="1480" height="26" fill="#3a2a1a" opacity=".85"/>')
    for px in (260, 740, 1180, 1600):
        pr += (f'<rect x="{px:.0f}" y="898" width="46" height="160" rx="8" fill="#4a3522"'
               f' {o(4)}/>')
    s += SL(Z_SRED, pr)

    # бочки с мёдом слева
    boch = ""
    for i, (bx, by, bs) in enumerate(((160, 820, 1.0), (330, 824, .84), (250, 1050, 1.1))):
        bw, bh = 170 * bs, 200 * bs
        boch += (f'<path d="M{bx-bw/2:.0f},{by-bh:.0f} Q{bx-bw*.68:.0f},{by-bh*.5:.0f}'
                 f' {bx-bw/2:.0f},{by:.0f} L{bx+bw/2:.0f},{by:.0f}'
                 f' Q{bx+bw*.68:.0f},{by-bh*.5:.0f} {bx+bw/2:.0f},{by-bh:.0f} Z"'
                 f' fill="url(#derev)" {o(5)}/>'
                 f'<rect x="{bx-bw*.62:.0f}" y="{by-bh*.78:.0f}" width="{bw*1.24:.0f}"'
                 f' height="18" rx="6" fill="{ZHELEZ}" {o(3)}/>'
                 f'<rect x="{bx-bw*.62:.0f}" y="{by-bh*.30:.0f}" width="{bw*1.24:.0f}"'
                 f' height="18" rx="6" fill="{ZHELEZ}" {o(3)}/>'
                 f'<ellipse cx="{bx:.0f}" cy="{by-bh:.0f}" rx="{bw/2:.0f}" ry="{bw*.17:.0f}"'
                 f' fill="url(#med)" {o(4)}/>')
    s += SL(Z_SRED, boch)

    # связки мехов на жерди
    meh = (f'<rect x="420" y="470" width="520" height="20" rx="7" fill="#4a3522" {o(4)}/>')
    for i in range(5):
        mx = 460 + i * 106
        kach = 3.0 * A.w(t, 2.6 + i * .2, i * .3)
        meh += (f'<g transform="rotate({kach:.1f} {mx:.0f} 486)">'
                f'<path d="M{mx-44:.0f},490 Q{mx-56:.0f},620 {mx-20:.0f},720'
                f' Q{mx:.0f},760 {mx+20:.0f},720 Q{mx+56:.0f},620 {mx+44:.0f},490 Z"'
                f' fill="{["#6b4a2c","#8a6a46","#4e3a28","#7a5a3a","#5e4630"][i]}" {o(4)}/>'
                f'<ellipse cx="{mx:.0f}" cy="{492:.0f}" rx="44" ry="18" fill="#3a2a1a" {o(3)}/>'
                f'<path d="M{mx-18:.0f},700 L{mx:.0f},762 L{mx+18:.0f},700 Z"'
                f' fill="#2e2118" {o(2)}/></g>')
    s += SL(Z_SRED, meh)

    # весы с гирями
    vx_, vy_ = 1180, 560
    gir = A.ease(A.seg(t, .4, 1.0))
    nak = 11 * gir
    ves = (f'<rect x="{vx_-12:.0f}" y="{vy_:.0f}" width="24" height="300" rx="8"'
           f' fill="{ZHELEZ}" {o(4)}/>'
           f'<g transform="rotate({nak:.1f} {vx_:.0f} {vy_:.0f})">'
           f'<rect x="{vx_-210:.0f}" y="{vy_-12:.0f}" width="420" height="20" rx="8"'
           f' fill="{ZHELEZ}" {o(4)}/>'
           f'<line x1="{vx_-196:.0f}" y1="{vy_:.0f}" x2="{vx_-196:.0f}" y2="{vy_+96:.0f}"'
           f' stroke="{ZHELEZ}" stroke-width="5"/>'
           f'<line x1="{vx_+196:.0f}" y1="{vy_:.0f}" x2="{vx_+196:.0f}" y2="{vy_+96:.0f}"'
           f' stroke="{ZHELEZ}" stroke-width="5"/>'
           f'<path d="M{vx_-276:.0f},{vy_+96:.0f} Q{vx_-196:.0f},{vy_+170:.0f}'
           f' {vx_-116:.0f},{vy_+96:.0f} Z" fill="url(#zhel)" {o(4)}/>'
           f'<path d="M{vx_+116:.0f},{vy_+96:.0f} Q{vx_+196:.0f},{vy_+170:.0f}'
           f' {vx_+276:.0f},{vy_+96:.0f} Z" fill="url(#zhel)" {o(4)}/>'
           f'<path d="M{vx_-224:.0f},{vy_+94:.0f} L{vx_-208:.0f},{vy_+28:.0f}'
           f' L{vx_-184:.0f},{vy_+28:.0f} L{vx_-168:.0f},{vy_+94:.0f} Z"'
           f' fill="{CHUGUN}" opacity="{gir:.2f}" {o(3)}/></g>')
    s += SL(Z_SRED, ves)

    # калачи на шесте
    kal = (f'<rect x="1480" y="500" width="400" height="18" rx="6" fill="#4a3522" {o(4)}/>')
    for i in range(5):
        cx = 1520 + i * 86
        kch = 4.0 * A.w(t, 2.2 + i * .3, i * .25)
        kal += (f'<g transform="rotate({kch:.1f} {cx:.0f} 510)">'
                f'<circle cx="{cx:.0f}" cy="{586:.0f}" r="52" fill="url(#solom)" {o(4)}/>'
                f'<circle cx="{cx:.0f}" cy="{586:.0f}" r="20" fill="#5a4328" {o(3)}/>'
                f'<line x1="{cx:.0f}" y1="510" x2="{cx:.0f}" y2="{560:.0f}"'
                f' stroke="#8a7a58" stroke-width="4"/></g>')
    s += SL(Z_SRED, kal)
    s += SL(Z_SRED, _polka_s_utvaryu(1420, 800, 480, t, 73, 4))
    zherdi = ""
    zherdi += (f'<rect x="250" y="300" width="1420" height="22" rx="9"'
               f' fill="#5b4428" {o(5)}/>'
               f'<rect x="330" y="214" width="1260" height="20" rx="8"'
               f' fill="#6a5030" {o(4)}/>')
    for i in range(9):
        zx_ = 60 + i * 220
        zherdi += (f'<line x1="{zx_:.0f}" y1="{410+abs(zx_-960)*0.17:.0f}"'
                   f' x2="{zx_+60:.0f}" y2="250" stroke="#5b4428" stroke-width="10"'
                   f' opacity=".8"/>')
    for i in range(8):
        hx2 = 360 + i * 170
        kc2 = 2.6 * A.w(t, 3.1, i * .27)
        zherdi += (f'<g transform="rotate({kc2:.1f} {hx2:.0f} 322)">'
                   f'<path d="M{hx2-26:.0f},322 L{hx2+26:.0f},322'
                   f' L{hx2+18:.0f},{416:.0f} L{hx2-18:.0f},{416:.0f} Z"'
                   f' fill="{["#8a6a46","#6b4a2c","#7a6342","#5e4630"][i%4]}" {o(3)}/>'
                   f'<ellipse cx="{hx2:.0f}" cy="324" rx="26" ry="9" fill="#3a2a1a"'
                   f' {o(2)}/></g>')
    for i in range(7):
        hx = 220 + i * 250
        hy = 300 + abs(hx - 960) * .13
        kch = 3.0 * A.w(t, 2.8, i * .3)
        zherdi += (f'<g transform="rotate({kch:.1f} {hx:.0f} {hy:.0f})">'
                   f'<path d="M{hx-30:.0f},{hy:.0f} L{hx+30:.0f},{hy:.0f}'
                   f' L{hx+20:.0f},{hy+110:.0f} L{hx-20:.0f},{hy+110:.0f} Z"'
                   f' fill="{["#7a6342","#6b4a2c","#8a6a46"][i%3]}" {o(3)}/>'
                   f'<line x1="{hx:.0f}" y1="{hy-30:.0f}" x2="{hx:.0f}" y2="{hy:.0f}"'
                   f' stroke="#8a7a58" stroke-width="4"/></g>')
    s += SL(Z_DAL, zherdi)
    s += SL(Z_SRED, _dvorovaya_utvar(60, 1058, 420, t, 79, ["korob", "meshok", "korzina"]))
    s += SL(Z_SRED, _dvorovaya_utvar(700, 816, 560, t, 397,
                                     ["korzina", "korob", "kadka"]))

    # купец за прилавком
    kx, ky, kh = 1180, 1040, 500
    kup = figura(kx, ky, kh, t, col="#4b3550", kant="#ffd98a", ph=.2, boroda=True)
    r1, _, (kpx, kpy) = _ruka_ekr(kx, ky, kh, 1, kh * .46, -58 + 30 * gir, t, "#4b3550",
                                  "#ffd98a", .1, 5)
    r2, _, (klx, kly) = _ruka_ekr(kx, ky, kh, -1, kh * .36, 42, t, "#4b3550", "#ffd98a", .5, 4)
    s += SL(Z_SRED, kup + r1 + r2)

    # покупательница с корзиной
    bx_, by_, bh_ = 560, 1050, 470
    pok = figura(bx_, by_, bh_, t, col="#3d4a3a", kant="#cfe4f5", platok=True, ph=.6)
    r3, (c1x, c1y), (ppx, ppy) = _ruka_ekr(bx_, by_, bh_, 1, bh_ * .36, 62, t, "#3d4a3a",
                                           "#cfe4f5", .3, 4)
    r4, (c2x, c2y), (plx2, ply2) = _ruka_ekr(bx_, by_, bh_, -1, bh_ * .36, 118, t, "#3d4a3a",
                                             "#cfe4f5", .7, 4)
    kor_y = (c1y + c2y) / 2 + 40
    pok += r3 + r4
    pok += (f'<path d="M{bx_-96:.0f},{kor_y:.0f} L{bx_+96:.0f},{kor_y:.0f}'
            f' L{bx_+66:.0f},{kor_y+118:.0f} L{bx_-66:.0f},{kor_y+118:.0f} Z"'
            f' fill="url(#solom)" {o(5)}/>'
            f'<path d="M{bx_-80:.0f},{kor_y:.0f} Q{bx_:.0f},{kor_y-96:.0f}'
            f' {bx_+80:.0f},{kor_y:.0f}" fill="none" stroke="#8a6a3c" stroke-width="9"/>')
    s += SL(Z_SRED, pok)

    # мальчик Иван с берестяной грамоткой
    mx_, my_, mh_ = 830, 1056, 330
    prizh = 6 * A.w(t, 1.6, .2)
    mal = figura(mx_, my_, mh_, t, col="#9a8c70", kant="#cfe4f5", ph=.4)
    r5, _, (m1x, m1y) = _ruka_ekr(mx_, my_, mh_, 1, mh_ * .34, 128, t, "#9a8c70", "#cfe4f5", .2, 4)
    r6, _, (m2x, m2y) = _ruka_ekr(mx_, my_, mh_, -1, mh_ * .34, 52, t, "#9a8c70", "#cfe4f5", .6, 4)
    mal += r5 + r6
    gy = my_ - mh_ * .46 + prizh
    mal += (f'<rect x="{mx_-54:.0f}" y="{gy:.0f}" width="108" height="76" rx="8"'
            f' fill="#cdb183" {o(4)}/>'
            f'<path d="M{mx_-40:.0f},{gy+22:.0f} Q{mx_-10:.0f},{gy+12:.0f}'
            f' {mx_+20:.0f},{gy+24:.0f} Q{mx_+40:.0f},{gy+32:.0f} {mx_+44:.0f},{gy+22:.0f}"'
            f' fill="none" stroke="#7a6038" stroke-width="4"/>'
            f'<path d="M{mx_-40:.0f},{gy+48:.0f} Q{mx_-6:.0f},{gy+38:.0f}'
            f' {mx_+26:.0f},{gy+50:.0f}" fill="none" stroke="#7a6038" stroke-width="4"/>')
    mal += para_izo_rta(mx_ + 30, my_ - mh_ * .80, t, .5, .8, .5)
    s += SL(Z_SRED, mal + ten(mx_, my_ + 6, 72, 14, .45))
    s += SL(Z_SRED, teplo(1180, 700, 300, 220, .36))
    s += SL(Z_PERED, _stolb_pered(-6, 96, "#1d1611", 0, H))
    s += SL(Z_LETIT, sneg_letit(t, 14, 27, .36, .6))
    s += ramka_pp("oba")
    s += vinetka(.42)
    return s


def dve_pustye_lavki(t):
    """Горница: у стены две лавки — на первой платок и веретено, на второй
    шапка и топор. Между ними стол с одной миской и ложкой. Мальчик сидит за
    столом на табурете, ноги не достают до пола. Свет гаснет над лавками."""
    rnd = random.Random(110)
    pol = 760
    s = _stena_gornicy(t, 7, True, pol)
    s += SL(Z_DAL, f'<rect x="620" y="0" width="30" height="{pol:.0f}" fill="#4e3220"'
                   f' opacity=".7"/>'
                   f'<rect x="1300" y="0" width="30" height="{pol:.0f}" fill="#4e3220"'
                   f' opacity=".7"/>')
    s += SL(Z_DAL, okno_izby(820, 150, 330, 280, t, svet=False, moroz=.55))
    s += SL(Z_DAL, zanaveska(820, 140, 160, 120, TKAN, t, 1)
            + zanaveska(1150, 140, 160, 120, TKAN, t, -1))
    s += SL(Z_DAL, _polka_s_utvaryu(180, 330, 420, t, 85, 3))
    s += SL(Z_DAL, _polka_s_utvaryu(620, 560, 540, t, 147, 4))
    s += SL(Z_DAL, _polka_s_utvaryu(460, 420, 480, t, 389, 4))
    s += SL(Z_SRED, _dvorovaya_utvar(620, 700, 500, t, 391,
                                     ["kadka", "korzina", "korob"]))
    s += SL(Z_DAL, utvar_izby(1420, 320, 420, t, 11))
    # якорь был 1180 — пила (x+880) и серп уезжали за правый край холста,
    # и половина снасти в кадр не попадала (тот же класс, что в сцене
    # прищуренной соседки; правило «поймал один — проверь все»)
    s += SL(Z_DAL, _stennoe_hozyaystvo(760, 150, t, 149))
    s += SL(Z_DAL, hodiki(1760, 200, t, 1.4))

    # печь углом слева
    s += SL(Z_SRED, pech(-110, 180, 420, 560, t, True, True, True))
    s += SL(Z_SRED, ugli(10, 560, 250, t, 8, 2) + teplo(150, 540, 330, 280, .40))
    s += SL(Z_SRED, dym(140, 190, t, 4, .24, 220, .28, "#d3dae2", .8))

    g1 = A.ease(A.seg(t, .6, 1.0))
    g2 = A.ease(A.seg(t, 2.1, 1.0))
    s += SL(Z_SRED, luch(560, 420, 360, 420, t, .22 * (1 - g1))
            + luch(1180, 420, 360, 420, t, .22 * (1 - g2)))

    # две лавки
    s += SL(Z_SRED, _lavka_krupno(300, 1010, 640, t, 230, True))
    s += SL(Z_SRED, _lavka_krupno(1220, 1010, 640, t, 230, True))
    s += SL(Z_SRED, _kadushki_i_grabli(60, 1056, t, 135))

    # на первой — платок и веретено с недопряденной нитью
    prov = 26 * g1
    l1 = (f'<path d="M340,772 Q450,700 620,764 Q500,842 368,826 Z" fill="#6d4a52" {o(6)}/>'
          f'<path d="M372,784 Q482,730 598,776" fill="none" stroke="{KRAS}"'
          f' stroke-width="9" opacity=".7"/>'
          f'<path d="M386,812 Q470,766 570,802" fill="none" stroke="#b07a86"'
          f' stroke-width="6" opacity=".6"/>'
          f'<path d="M700,780 L736,660 L772,780 L736,890 Z" fill="url(#derev)" {o(5)}/>'
          f'<ellipse cx="736" cy="816" rx="54" ry="28" fill="url(#solom)" {o(5)}/>'
          f'<path d="M736,660 Q812,{640+prov:.0f} 884,{690+prov*1.8:.0f}" fill="none"'
          f' stroke="{KREM}" stroke-width="8"/>'
          f'<ellipse cx="900" cy="{706+prov*1.8:.0f}" rx="56" ry="70" fill="url(#solom)"'
          f' opacity=".9" {o(5)}/>')
    s += SL(Z_SRED, l1)

    # на второй — мужская шапка и плотницкий топор
    l2 = (f'<path d="M1262,782 Q1290,672 1384,668 Q1480,672 1508,782 Z" fill="#3a3040"'
          f' {o(6)}/>'
          f'<rect x="1246" y="768" width="280" height="44" rx="20" fill="#5e4a3a" {o(5)}/>'
          f'<path d="M1262,720 Q1384,690 1508,720" fill="none" stroke="#50465c"'
          f' stroke-width="7" opacity=".7"/>'
          f'<rect x="1596" y="762" width="300" height="32" rx="13" fill="url(#derev)"'
          f' {o(5)}/>'
          f'<path d="M1600,776 L1548,700 L1470,726 L1480,812 L1556,830 Z"'
          f' fill="url(#zhel)" {o(6)}/>'
          f'<path d="M1490,744 L1540,730" stroke="#e6eef6" stroke-width="10"'
          f' opacity=".75"/>'
          f'<path d="M1480,812 Q1520,826 1556,830" fill="none" stroke="#8c99a4"'
          f' stroke-width="6" opacity=".7"/>')
    s += SL(Z_SRED, l2)

    # стол между лавками, миска и ложка
    s += SL(Z_SRED, stol(960, 880, 520, 32))
    s += SL(Z_SRED, f'<path d="M882,866 Q960,924 1038,866 L1024,842 Q960,886 896,842 Z"'
                    f' fill="url(#glina)" {o(5)}/>'
                    f'<ellipse cx="960" cy="862" rx="78" ry="22" fill="#6d4e32" {o(3)}/>'
                    f'<ellipse cx="1092" cy="868" rx="34" ry="16" fill="url(#derev)"'
                    f' {o(3)}/>'
                    f'<rect x="1118" y="860" width="110" height="14" rx="7"'
                    f' fill="url(#derev)" {o(3)}/>')

    # мальчик на табурете, ноги не достают до пола
    fx, fy, fh = 960, 1000, 300
    gol = 10 * g2
    s += SL(Z_SRED, f'<rect x="{fx-80:.0f}" y="{fy-60:.0f}" width="160" height="22" rx="8"'
                    f' fill="url(#dosk)" {o(5)}/>'
                    f'<rect x="{fx-62:.0f}" y="{fy-38:.0f}" width="26" height="38" rx="7"'
                    f' fill="#4a3522" {o(3)}/>'
                    f'<rect x="{fx+36:.0f}" y="{fy-38:.0f}" width="26" height="38" rx="7"'
                    f' fill="#4a3522" {o(3)}/>')
    mal = figura(fx, fy - 60, fh, t, col="#6e6250", kant="#ffd98a", ph=.3,
                 naklon=6 * g2)
    r1, _, (m1x, m1y) = _ruka_ekr(fx, fy - 60, fh, 1, fh * .36, 104, t, "#6e6250", "#ffd98a", .2,
                                  3)
    r2, _, (m2x, m2y) = _ruka_ekr(fx, fy - 60, fh, -1, fh * .36, 76, t, "#6e6250", "#ffd98a", .6,
                                  3)
    mal += r1 + r2
    s += SL(Z_SRED, mal)
    s += SL(Z_SRED, _kot_zhivoy(250, 1046, t, 1.5, "#4a423c", .5, True, True))
    s += SL(Z_SRED, mebel_hlam(1560, 1056, 400, t, 17))
    s += SL(Z_SRED, krynka(120, 1030, 1.4) + kartoshka(600, 1056, t, 7, 6, 1.1))
    # половик во всю середину пола
    s += SL(Z_SRED, f'<path d="M560,1006 L1400,1006 L1520,1076 L440,1076 Z"'
                    f' fill="{RUSH}" {o(5)}/>'
                    f'<path d="M580,1026 L1392,1026 M566,1050 L1428,1050"'
                    f' stroke="{KRAS}" stroke-width="9" opacity=".65"/>'
                    f'<path d="M600,1038 L1372,1038" stroke="#6a7a8a" stroke-width="6"'
                    f' opacity=".5"/>')
    # прялка в углу: донце, гребень, веретено
    prx, pry = 1700, 1000
    pkach = 2.2 * A.w(t, 3.2, .3)
    s += SL(Z_SRED, f'<g transform="rotate({pkach:.1f} {prx:.0f} {pry:.0f})">'
                    f'<rect x="{prx-110:.0f}" y="{pry-40:.0f}" width="230" height="36"'
                    f' rx="10" fill="url(#dosk)" {o(5)}/>'
                    f'<rect x="{prx-16:.0f}" y="{pry-420:.0f}" width="34" height="382"'
                    f' rx="12" fill="url(#derev)" {o(5)}/>'
                    f'<path d="M{prx-80:.0f},{pry-420:.0f} L{prx+112:.0f},{pry-420:.0f}'
                    f' L{prx+96:.0f},{pry-500:.0f} L{prx-64:.0f},{pry-500:.0f} Z"'
                    f' fill="#6a5030" {o(5)}/>')
    for i in range(7):
        s += SL(Z_SRED, f'<line x1="{prx-62+i*28:.0f}" y1="{pry-500:.0f}"'
                        f' x2="{prx-56+i*28:.0f}" y2="{pry-556:.0f}" stroke="#5b4428"'
                        f' stroke-width="8"/>')
    s += SL(Z_SRED, f'<ellipse cx="{prx+20:.0f}" cy="{pry-540:.0f}" rx="74" ry="56"'
                    f' fill="url(#solom)" opacity=".92" {o(5)}/></g>')
    # сундук под окном
    s += SL(Z_SRED, f'<rect x="940" y="930" width="300" height="130" rx="10"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<path d="M940,930 Q1090,876 1240,930 Z" fill="#5b4428" {o(5)}/>'
                    f'<rect x="930" y="962" width="320" height="18" rx="7"'
                    f' fill="{ZHELEZ}" {o(3)}/>'
                    f'<rect x="1070" y="954" width="40" height="46" rx="8"'
                    f' fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, _dvorovaya_utvar(560, 1072, 820, t, 321,
                                     ["korzina", "korob", "kadka", "meshok"]))
    s += SL(Z_SRED, _listya(377, 22, 950, 1050))
    s += SL(Z_PERED, _stolb_pered(1846, 110, "#140f0b", 0, H))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def vdova_natalya_i_malchik(t):
    """Тёплая изба: Наталья ставит мальчику миску с кашей и набрасывает на
    плечи тулупчик, мальчик сидит на лавке с ложкой. Потом на столе доска с
    писалом, и он берёт писало. На полке горшки, у печи кот."""
    rnd = random.Random(111)
    pol = 770
    s = _stena_gornicy(t, 9, True, pol)
    s += SL(Z_DAL, f'<rect x="1180" y="0" width="30" height="{pol:.0f}" fill="#4e3220"'
                   f' opacity=".7"/>')
    s += SL(Z_DAL, _polka_s_utvaryu(1240, 300, 560, t, 87, 4))
    s += SL(Z_DAL, utvar_izby(1300, 520, 420, t, 13))
    s += SL(Z_DAL, okno_izby(980, 160, 260, 230, t, svet=False, moroz=.4))

    # печь крупно слева — главный предмет и единственное тёплое пятно
    s += SL(Z_SRED, pech(20, 90, 620, 740, t, True, True, False))
    s += SL(Z_SRED, teplo(330, 560, 420, 350, .46))
    s += SL(Z_SRED, iskra_let(t, 300, 600, 8, 4, 280, .5))
    s += SL(Z_SRED, dym(330, 150, t, 4, .3, 240, .3, "#d3dae2", .8))
    s += SL(Z_SRED, _kot_zhivoy(640, 1046, t, 1.4, "#554c44", .7, True, False))
    s += SL(Z_SRED, mebel_hlam(1660, 1050, 420, t, 19))

    s += SL(Z_SRED, stol(1180, 850, 1180, 40))
    s += SL(Z_SRED, _polka_s_utvaryu(760, 250, 520, t, 339, 4))
    s += SL(Z_SRED, _dvorovaya_utvar(700, 1070, 460, t, 341,
                                     ["kadka", "korzina", "korob"]))
    s += SL(Z_SRED, utvar_izby(820, 520, 360, t, 35))
    s += SL(Z_SRED, _polka_s_utvaryu(620, 440, 520, t, 353, 4))
    s += SL(Z_SRED, _stennoe_hozyaystvo(560, 320, t, 355))
    s += SL(Z_SRED, f'<rect x="1180" y="400" width="300" height="210" rx="10"'
                    f' fill="{RUSH}" {o(5)}/>'
                    f'<path d="M1196,452 L1464,452 M1196,502 L1464,502"'
                    f' stroke="{KRAS}" stroke-width="9" opacity=".65"/>')
    s += SL(Z_SRED, _lavka_krupno(1290, 1010, 480, t, 160))

    # миска с кашей ставится на стол
    st1 = A.ease(A.seg(t, .4, .9))
    bx_, by_ = 960, 836 - 140 * (1 - st1)
    s += SL(Z_SRED, f'<path d="M{bx_-88:.0f},{by_:.0f} Q{bx_:.0f},{by_+76:.0f}'
                    f' {bx_+88:.0f},{by_:.0f} L{bx_+72:.0f},{by_-26:.0f}'
                    f' Q{bx_:.0f},{by_+30:.0f} {bx_-72:.0f},{by_-26:.0f} Z"'
                    f' fill="url(#glina)" {o(5)}/>'
                    f'<ellipse cx="{bx_:.0f}" cy="{by_-24:.0f}" rx="80" ry="24"'
                    f' fill="url(#krem)" {o(3)}/>'
                    + par(bx_, by_ - 50, t, 4, .55, 170, .45, 1.1))

    # доска с писалом появляется на третьих словах
    st3 = A.ease(A.seg(t, 3.2, 1.0))
    dx_, dy_ = 1380, 830
    dos = (f'<rect x="{dx_-130:.0f}" y="{dy_-30:.0f}" width="260" height="36" rx="8"'
           f' fill="#6b5a3c" opacity="{st3:.2f}" {o(5)}/>'
           f'<rect x="{dx_-118:.0f}" y="{dy_-24:.0f}" width="236" height="24" rx="6"'
           f' fill="#2e2620" opacity="{st3*.9:.2f}"/>')
    vol = min(1.0, max(.0, (t - 3.6) * .8))
    dos += (f'<path d="M{dx_-96:.0f},{dy_-12:.0f} Q{dx_-70:.0f},{dy_-22:.0f}'
            f' {dx_-44:.0f},{dy_-12:.0f} Q{dx_-18:.0f},{dy_-2:.0f} {dx_+8:.0f},{dy_-12:.0f}"'
            f' fill="none" stroke="#d8c79a" stroke-width="5"'
            f' stroke-dasharray="{200*vol:.0f} 400" opacity="{st3:.2f}"/>')
    s += SL(Z_SRED, dos)

    # Наталья у стола
    nx, ny, nh = 760, 1030, 540
    nat = figura(nx, ny, nh, t, col="#39303c", kant="#ffd98a", platok=True, ph=.2)
    # было: один прямой рукав в 270 px по диагонали к полке — брусок
    r1, (hx, hy), (npx, npy) = _ruka_so_sgibom(nx, ny, nh, 1, nh * .25,
                                               16 + 14 * st1, nh * .22,
                                               72 - 16 * st1, t, "#39303c",
                                               "#ffd98a", .1, 5)
    r2, (tx2, ty2), (nlx, nly) = _ruka_ekr(nx, ny, nh, -1, nh * .40, -62, t, "#39303c",
                                           "#ffd98a", .5, 4)
    nat += r1 + r2
    s += SL(Z_SRED, nat)

    # мальчик на лавке
    mx_, my_, mh_ = 1420, 1010, 330
    ber = A.ease(A.seg(t, 3.8, .8))
    mal = figura(mx_, my_ - 150, mh_, t, col="#7a6a52", kant="#ffd98a", ph=.4,
                 naklon=-5 * ber)
    r3, (lx3, ly3), (p1x, p1y) = _ruka_ekr(mx_, my_ - 150, mh_, 1, mh_ * .46, 154 - 40 * ber, t,
                                           "#7a6a52", "#ffd98a", .2, 4)
    r4, _, (p2x, p2y) = _ruka_ekr(mx_, my_ - 150, mh_, -1, mh_ * .42, 170, t, "#7a6a52",
                                  "#ffd98a", .6, 4)
    mal += r3 + r4
    mal += (f'<rect x="{lx3-10:.0f}" y="{ly3-10:.0f}" width="16" height="96" rx="7"'
            f' fill="url(#derev)" opacity="{1-ber:.2f}" {o(3)}/>'
            f'<ellipse cx="{lx3-2:.0f}" cy="{ly3+96:.0f}" rx="26" ry="16"'
            f' fill="url(#derev)" opacity="{1-ber:.2f}" {o(3)}/>'
            f'<rect x="{lx3-8:.0f}" y="{ly3-16:.0f}" width="12" height="90" rx="6"'
            f' fill="{ZHELEZ}" opacity="{ber:.2f}" {o(3)}/>')
    s += SL(Z_SRED, mal)

    # тулупчик ложится на плечи
    tul = A.ease(A.seg(t, 1.5, 1.0))
    s += SL(Z_SRED, f'<path d="M{mx_-92:.0f},{my_-150-mh_*.62-40*(1-tul):.0f}'
                    f' Q{mx_:.0f},{my_-150-mh_*.80-70*(1-tul):.0f}'
                    f' {mx_+92:.0f},{my_-150-mh_*.62-40*(1-tul):.0f}'
                    f' L{mx_+76:.0f},{my_-150-mh_*.28:.0f}'
                    f' Q{mx_:.0f},{my_-150-mh_*.40:.0f}'
                    f' {mx_-76:.0f},{my_-150-mh_*.28:.0f} Z" fill="#7a5a36"'
                    f' opacity="{tul*.95:.2f}" {o(5)}/>')
    s += SL(Z_SRED, krynka(1800, 836, 1.2) + karavay(1640, 840, 1.1, True))
    s += SL(Z_PERED, _stolb_pered(-6, 96, "#140f0b", 0, H))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def malchik_u_steny(t):
    """Городская улица: бревенчатая стена амбара на пол-кадра. Четверо ребят
    играют в горелки, Иван стоит у стены, руки за спиной, и смотрит.
    У стены бочка, тележное колесо, лопухи, курица перебегает улицу."""
    rnd = random.Random(112)
    s = nebo("den", t, False, 43)
    s += oblaka(t, 130, 5, 25, .45)
    s += SL(Z_DAL, _derevnya_ryad(470, t, 71, ((130, 300), (1810, 280))))
    # НАД ГОЛОВОЙ РЕБЁНКА ПУСТО. Осмотр 15.11: «два взрослых держат
    # скрещённые шесты прямо над головой мальчика, у самого лица». Шестов
    # никто не держал — это крестовина ворот амбара (1010-1439 × 419-616) и
    # полотно пилы со стенной снасти (1240-1520 × 620-708) приходились ровно
    # на голову Ивана, стоявшего на 1480. Стена и снасть съехали влево,
    # правую часть держит дощатый забор, Иван отошёл в чистое поле кадра.
    s += SL(Z_SRED, _stena_ambara(230, 210, 1120, 580, t, True, 3))
    s += SL(Z_SRED, _stennoe_hozyaystvo(240, 300, t, 137))
    # забор и поленница стоят НИЖЕ и ПРАВЕЕ головы Ивана: горизонтальные
    # поперечины забора на уровне лица — та же беда, что и шесты
    s += SL(Z_SRED, _zabor_dosok(1366, 700, 574, 240, 85, 56))
    s += SL(Z_SRED, _polenica(1706, 420, 214, 180, 87, 22))
    s += SL(Z_DAL, dym(1810, 180, t, 4, .24, 240, .3, "#d3dae2", .8))

    zem = f'<rect x="0" y="780" width="{W}" height="300" fill="#4e3f2c"/>'
    zem += _zemlya_faktura(830, 1060, 73, 15)
    zem += _koleya(960, 75, 2)
    zem += _listya(77, 24, 830, 1060)
    zem += _trava(rnd, 10, 850, 1050)
    s += SL(Z_SRED, zem)

    # бочка, тележное колесо, лопухи у стены
    s += SL(Z_SRED, f'<path d="M80,1000 Q40,900 80,800 L250,800 Q290,900 250,1000 Z"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<rect x="56" y="836" width="218" height="20" rx="7" fill="{ZHELEZ}"'
                    f' {o(3)}/>'
                    f'<rect x="56" y="946" width="218" height="20" rx="7" fill="{ZHELEZ}"'
                    f' {o(3)}/>'
                    f'<ellipse cx="165" cy="800" rx="86" ry="24" fill="#5b4428" {o(4)}/>')
    # колесо ушло к бочке влево, чтобы не стоять там, где теперь Иван
    kol_a = 6 * A.w(t, 5.0, .2)
    kolo = (f'<g transform="rotate({kol_a:.1f} 340 972)">'
            f'<circle cx="340" cy="972" r="118" fill="none" stroke="url(#derev)"'
            f' stroke-width="24"/>'
            f'<circle cx="340" cy="972" r="31" fill="url(#derev)" {o(4)}/>')
    for i in range(8):
        a = math.radians(i * 45)
        kolo += (f'<line x1="{340+31*math.cos(a):.0f}" y1="{972+31*math.sin(a):.0f}"'
                 f' x2="{340+107*math.cos(a):.0f}" y2="{972+107*math.sin(a):.0f}"'
                 f' stroke="#5e442a" stroke-width="10"/>')
    kolo += "</g>"
    s += SL(Z_SRED, kolo)
    s += SL(Z_SRED, _podorozhnik(400, 1040, 2.0, t, .2, 6)
            + _podorozhnik(1480, 1056, 1.8, t, .7, 6))
    s += SL(Z_SRED, _yaschiki(1414, 962, t, 79, 2, .92))

    # четверо ребят в горелки: двое бегут, двое догоняют
    beg = (t * .5) % 1.0
    deti = ""
    # РОСТ, ГЛУБИНА, ШАГ И ПОВОРОТ У КАЖДОГО СВОИ (осмотр 15.11: четверо
    # ребят шли ровным рядом одного роста и читались орнаментом). Теперь
    # разброс роста 614-217 px, базы 1032-976, шаги 412-274-328 и у каждого
    # свой убор.
    for i, (bx0, bh, col, dg, dep) in enumerate(((330, 530, "#6b5a3c", 0, 1.16),
                                                 (742, 390, "#3f5466", 0, .78),
                                                 (1016, 470, "#6a4a52", 1, .98),
                                                 (1344, 330, "#4c5c3e", 1, .66))):
        bh = int(bh * dep)
        dx_ = bx0 + (150 if dg else 230) * beg
        yb = 1014 - (1 - dep) * 110
        pryg = (14 + 9 * i % 11) * abs(math.sin(beg * 6.283 * 2 + i * 1.7))
        d = figura(dx_, yb - pryg, bh, t, col=col, kant="#cfe4f5", ph=i * .31,
                   naklon=(14 if dg else -11) + (3 if i % 2 else -4),
                   platok=(i == 3), shapka=(i in (1, 2)), profil=(i % 2 == 0),
                   op=.78 + .22 * dep)
        # руки МАШУТ в противофазе: одна вверх-наружу, другая вниз-наружу,
        # и у чётных-нечётных по-разному — бег, а не стойка «руки по швам»
        rr1, _, (a1x, a1y) = _ruka(dx_, yb - pryg, bh, 1, bh * (.38 + .09 * (i % 2)),
                                   (-34 if dg else 52) + (14 if i % 2 else -16), t, col,
                                   "#cfe4f5", i * .2, 7)
        rr2, _, (a2x, a2y) = _ruka(dx_, yb - pryg, bh, -1, bh * (.34 + .11 * (i % 2)),
                                   (46 if dg else -30) + (11 if i % 2 else -13), t, col,
                                   "#cfe4f5", i * .2 + .4, 7)
        d += rr1 + rr2
        deti += d + ten(dx_, yb + 6, 60 * dep, 13 * dep, .4)
        # пыль из-под ног
        for k in range(3):
            pp = (beg + k / 3.0) % 1.0
            deti += (f'<ellipse cx="{dx_-40-pp*70:.0f}" cy="{yb-pp*16:.0f}"'
                     f' rx="{(18+pp*30)*dep:.0f}" ry="{(8+pp*12)*dep:.0f}"'
                     f' fill="#8a7a62" opacity="{(1-pp)*.35:.2f}"/>')
    s += SL(Z_SRED, deti)

    # Иван у стены: спиной к брёвнам, руки за спиной
    ix, iy, ih = 1600, 1026, 470
    iv = figura(ix, iy, ih, t, col="#8e8068", kant="#ffd98a", ph=.5)
    s += SL(Z_SRED, iv + ten(ix, iy + 6, 84, 16, .45))
    s += SL(Z_SRED, f'<path d="M{ix-66:.0f},{iy-ih*.52:.0f} Q{ix:.0f},{iy-ih*.40:.0f}'
                    f' {ix+66:.0f},{iy-ih*.52:.0f}" fill="none" stroke="#8e8068"'
                    f' stroke-width="26" stroke-linecap="round"/>')

    # курица перебегает улицу
    kx_ = ((t * 170) % 2300) - 200
    s += SL(Z_SRED, kura(kx_, 1056, t, 1.4, .2))
    s += SL(Z_SRED, _dvorovaya_utvar(560, 1066, 420, t, 81, ["korzina", "vedro"]))
    s += SL(Z_PERED, _vetka_pered(2000, 60, 760, 158, t, 83, "#241c16", 6))
    s += SL(Z_LETIT, sneg_letit(t, 12, 29, .3, .6))
    s += ramka_pp("oba")
    s += vinetka(.42)
    return s


def yurodivyy_na_vecherney_ulice(t):
    """Та же улица на закате, длинные тени: высокий худой странник идёт со
    спины, босой, подпоясан верёвкой, в правой руке посох. Четверо ребят
    сбились в кучку и хохочут. У забора лежит собака, над крышами звезда."""
    rnd = random.Random(113)
    s = nebo("zakat", t, False, 47) if "zakat" else nebo("sumer", t, True, 47)
    s += oblaka(t, 140, 5, 31, .5)
    s += SL(Z_DAL, _derevnya_ryad(460, t, 85, ((150, 380), (640, 320), (1780, 400))))
    s += SL(Z_SRED, _stena_ambara(620, 110, 1300, 660, t, False, 5))
    s += SL(Z_DAL, _zabor_dosok(-20, 380, 560, 190, 87, 54))
    s += SL(Z_DAL, teplo(640, 330, 230, 180, .40))
    s += SL(Z_DAL, dym(640, 210, t, 5, .26, 280, .34, "#d3dae2", .9))

    # первая звезда
    mig = .4 + .6 * abs(A.w(t, 1.6, .2))
    s += SL(Z_DAL, f'<circle cx="1480" cy="110" r="9" fill="#fff6dd"'
                   f' opacity="{mig:.2f}"/>'
                   f'<path d="M1480,86 L1484,106 L1504,110 L1484,114 L1480,134'
                   f' L1476,114 L1456,110 L1476,106 Z" fill="#fff6dd"'
                   f' opacity="{mig*.8:.2f}"/>')

    zem = f'<rect x="0" y="770" width="{W}" height="310" fill="#4a3c2a"/>'
    zem += _zemlya_faktura(820, 1060, 89, 15)
    zem += _koleya(950, 91, 2)
    zem += _listya(93, 26, 820, 1060)
    s += SL(Z_SRED, zem)

    # длинные тени поперёк улицы
    ten_ = ""
    for i, tx_ in enumerate((336, 742, 1046, 1532)):
        ten_ += (f'<path d="M{tx_:.0f},1010 L{tx_+330:.0f},1066 L{tx_+270:.0f},1076'
                 f' L{tx_-40:.0f},1016 Z" fill="#2c2318" opacity=".35"/>')
    s += SL(Z_SRED, ten_)
    s += SL(Z_SRED, _polenica(80, 700, 320, 260, 95, 26))
    # Якорь был 1060, и пила (x+880) уходила за холст на 1940 — половина
    # снасти просто не попадала в кадр, отчего правая стена и пустовала.
    s += SL(Z_SRED, _stennoe_hozyaystvo(700, 290, t, 139))
    s += SL(Z_SRED, _kadushki_i_grabli(1500, 1050, t, 141))
    s += SL(Z_SRED, _dvorovaya_utvar(1600, 1060, 320, t, 97, ["kadka", "korob"]))

    # странник идёт ровным шагом
    hod = (t * .3) % 1.0
    sx, sy, sh = 760 + 160 * hod, 1030, 620
    shag = 14 * math.sin(hod * 6.283 * 2)
    str_ = figura(sx, sy - abs(shag) * .3, sh, t, col="#4e4438", kant="#ffd98a",
                  ph=.2, boroda=True, naklon=2 * math.sin(hod * 12.6))
    r1, (px2, py2), (spx, spy) = _ruka_ekr(sx, sy, sh, 1, sh * .42, 72, t, "#4e4438", "#ffd98a",
                                           .1, 4)
    r2, _, (slx, sly) = _ruka_ekr(sx, sy, sh, -1, sh * .44, 96, t, "#4e4438", "#ffd98a", .5, 6)
    str_ += r1 + r2
    # посох стучит о землю
    stuk = 10 * abs(math.sin(hod * 6.283))
    str_ += (f'<line x1="{px2:.0f}" y1="{py2-180:.0f}" x2="{px2+16:.0f}"'
             f' y2="{sy+6-stuk:.0f}" stroke="url(#derev)" stroke-width="18"'
             f' stroke-linecap="round"/>'
             f'<circle cx="{px2:.0f}" cy="{py2-186:.0f}" r="18" fill="#5e442a" {o(3)}/>')
    # заплаты на длинной одежде и верёвка-пояс
    for i, (zx_, zy_) in enumerate(((-44, -.42), (36, -.30), (-20, -.16))):
        str_ += (f'<rect x="{sx+zx_:.0f}" y="{sy+sh*zy_:.0f}" width="54" height="46"'
                 f' rx="8" fill="#6a5a46" opacity=".8" {o(3)}/>')
    str_ += (f'<path d="M{sx-70:.0f},{sy-sh*.46:.0f} Q{sx:.0f},{sy-sh*.40:.0f}'
             f' {sx+70:.0f},{sy-sh*.46:.0f}" fill="none" stroke="#9a8a68"'
             f' stroke-width="12"/>'
             f'<path d="M{sx+58:.0f},{sy-sh*.45:.0f} L{sx+66:.0f},{sy-sh*.26:.0f}"'
             f' stroke="#9a8a68" stroke-width="8"/>')
    s += SL(Z_SRED, str_ + ten(sx, sy + 6, 110, 20, .5))

    # четверо ребят кучкой хохочут
    deti = ""
    # ростом и шагом разные: было 290-275-300-270 через ровные 90 px
    for i, (bx0, bh, col, gl) in enumerate(((268, 380, "#6b5a3c", 1.0),
                                            (404, 246, "#4a5a6a", .80),
                                            (512, 322, "#6a4a52", .94),
                                            (650, 196, "#52604a", .70))):
        tr = 10 * abs(A.w(t, 1.1, i * .3))
        yb3 = 1020 - tr * .3 - (1 - gl) * 86
        d = figura(bx0, yb3, bh, t, col=col,
                   kant="#cfe4f5", ph=i * .25, naklon=-9 + 6 * i,
                   profil=(i % 2 == 1), shapka=(i == 2), platok=(i == 3),
                   op=.80 + .20 * gl)
        ug = -64 if i == 0 else -100
        rr1, _, (a1x, a1y) = _ruka_ekr(bx0, yb3, bh, 1, bh * (.54 if i == 0 else .34),
                                       ug, t, col, "#cfe4f5", i * .2, 5)
        rr2, _, (a2x, a2y) = _ruka_ekr(bx0, yb3, bh, -1, bh * .32, -104, t, col,
                                       "#cfe4f5", i * .2 + .4, 5)
        d += rr1 + rr2
        deti += d + ten(bx0, yb3 + 6, 58 * gl, 12 * gl, .4)
    s += SL(Z_SRED, deti)

    # собака у забора поднимает голову
    sg = A.ease(A.seg(t, 1.6, .8))
    dx_, dy_ = 180, 1046
    s += SL(Z_SRED, f'<ellipse cx="{dx_:.0f}" cy="{dy_:.0f}" rx="106" ry="46"'
                    f' fill="#6b5236" {o(4)}/>'
                    f'<ellipse cx="{dx_-96:.0f}" cy="{dy_-30-44*sg:.0f}" rx="46" ry="38"'
                    f' fill="#6b5236" {o(4)}/>'
                    f'<path d="M{dx_-128:.0f},{dy_-50-44*sg:.0f}'
                    f' L{dx_-140:.0f},{dy_-92-44*sg:.0f}'
                    f' L{dx_-100:.0f},{dy_-66-44*sg:.0f} Z" fill="#54402a" {o(3)}/>'
                    f'<circle cx="{dx_-112:.0f}" cy="{dy_-36-44*sg:.0f}" r="5"'
                    f' fill="#120c08"/>'
                    f'<path d="M{dx_+96:.0f},{dy_-16:.0f} Q{dx_+150:.0f},'
                    f'{dy_-60-20*A.w(t,1.3,.2):.0f} {dx_+168:.0f},{dy_-10:.0f}"'
                    f' fill="none" stroke="#6b5236" stroke-width="16"'
                    f' stroke-linecap="round"/>')
    s += SL(Z_SRED, _lavka_krupno(1180, 1056, 480, t, 170))
    s += SL(Z_SRED, _polka_s_utvaryu(1100, 540, 420, t, 151, 3))
    # ПРАВАЯ СТЕНА ОБЖИТА (осмотр 15.11: от 1520 до края шло голое бревно на
    # две трети высоты кадра). Настоящие вещи: приставная лестница, второе
    # стенное хозяйство, поленница под стеной, штабель ящиков, связки трав.
    lest = (f'<g transform="rotate(-6 1720 1040)">'
            f'<rect x="1636" y="300" width="20" height="740" rx="8"'
            f' fill="url(#derev)" {o(4)}/>'
            f'<rect x="1792" y="300" width="20" height="740" rx="8"'
            f' fill="url(#derev)" {o(4)}/>')
    for i in range(8):
        lest += (f'<rect x="1640" y="{352+i*92:.0f}" width="168" height="16" rx="6"'
                 f' fill="#5b4428" {o(3)}/>')
    lest += "</g>"
    s += SL(Z_SRED, lest)
    s += SL(Z_SRED, _polenica(1178, 884, 268, 186, 153, 23))
    s += SL(Z_SRED, _yaschiki(1430, 1056, t, 155, 2, .84))
    trav = ""
    for i, (hx_, hl) in enumerate(((1538, 150), (1596, 120), (1876, 168))):
        kol = 3 * A.w(t, 2.2, i * .3)
        trav += (f'<g transform="rotate({kol:.1f} {hx_:.0f} 240)">'
                 f'<rect x="{hx_-7:.0f}" y="236" width="14" height="{hl*.3:.0f}"'
                 f' rx="5" fill="#6a5a3c" {o(3)}/>')
        for k in range(7):
            trav += (f'<path d="M{hx_:.0f},{236+hl*.3:.0f} q{-22+k*7:.0f},{hl*.4:.0f}'
                     f' {-30+k*10:.0f},{hl:.0f}" fill="none" stroke="#7e8a4e"'
                     f' stroke-width="7" opacity=".85"/>')
        trav += (f'<rect x="{hx_-20:.0f}" y="{236+hl*.3:.0f}" width="40" height="16"'
                 f' rx="6" fill="#a8683c" {o(2)}/>'
                 f'<circle cx="{hx_:.0f}" cy="230" r="9" fill="{ZHELEZ}" {o(2)}/></g>')
    s += SL(Z_SRED, trav)
    s += SL(Z_PERED, _stolb_pered(-6, 104, "#1d1611", 0, H))
    s += SL(Z_LETIT, sneg_letit(t, 12, 33, .28, .55))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def yurodivyy_podnimaet_malchika(t):
    """У стены амбара: странник стоит, расставив ноги, посох прислонён к
    стене, обеими руками он поднимает мальчика прямо над своей головой.
    Закатный луч падает на обоих, сорочка отлетает вверх."""
    rnd = random.Random(114)
    s = nebo("zakat", t, False, 51)
    s += oblaka(t, 120, 4, 35, .45)
    s += SL(Z_DAL, _derevnya_ryad(430, t, 99, ((120, 320), (1830, 300))))
    s += SL(Z_SRED, _stena_ambara(220, 40, 1480, 760, t, True, 7))
    s += SL(Z_DAL, dym(1830, 190, t, 4, .24, 240, .3, "#d3dae2", .8))

    zem = f'<rect x="0" y="800" width="{W}" height="280" fill="#4a3c2a"/>'
    zem += _zemlya_faktura(840, 1060, 101, 14)
    zem += _listya(103, 24, 840, 1060)
    zem += _trava(rnd, 9, 860, 1050)
    s += SL(Z_SRED, zem)
    s += SL(Z_SRED, _polenica(40, 740, 280, 220, 105, 25))
    s += SL(Z_SRED, _dvorovaya_utvar(1560, 1062, 380, t, 107, ["korzina", "vedro"]))

    # закатный луч падает на обоих
    s += SL(Z_SRED, luch(700, 60, 620, 900, t, .22))
    s += SL(Z_SRED, teplo(980, 560, 480, 420, .36))

    # посох прислонён к стене
    s += SL(Z_SRED, f'<line x1="520" y1="300" x2="466" y2="1010" stroke="url(#derev)"'
                    f' stroke-width="20" stroke-linecap="round"/>'
                    f'<circle cx="522" cy="294" r="20" fill="#5e442a" {o(3)}/>')

    pod = A.ease(A.seg(t, .4, 1.6))
    # бочка, на которую мальчик встаёт
    bo_x, bo_y, bo_h, bo_w = 1280, 1046, 330, 260
    boch = (f'<path d="M{bo_x-bo_w/2:.0f},{bo_y-bo_h:.0f}'
            f' Q{bo_x-bo_w*.66:.0f},{bo_y-bo_h*.5:.0f} {bo_x-bo_w/2:.0f},{bo_y:.0f}'
            f' L{bo_x+bo_w/2:.0f},{bo_y:.0f}'
            f' Q{bo_x+bo_w*.66:.0f},{bo_y-bo_h*.5:.0f} {bo_x+bo_w/2:.0f},{bo_y-bo_h:.0f} Z"'
            f' fill="url(#derev)" {o(6)}/>'
            f'<rect x="{bo_x-bo_w*.62:.0f}" y="{bo_y-bo_h*.80:.0f}"'
            f' width="{bo_w*1.24:.0f}" height="20" rx="7" fill="{ZHELEZ}" {o(4)}/>'
            f'<rect x="{bo_x-bo_w*.62:.0f}" y="{bo_y-bo_h*.30:.0f}"'
            f' width="{bo_w*1.24:.0f}" height="20" rx="7" fill="{ZHELEZ}" {o(4)}/>'
            f'<ellipse cx="{bo_x:.0f}" cy="{bo_y-bo_h:.0f}" rx="{bo_w/2:.0f}"'
            f' ry="{bo_w*.18:.0f}" fill="#5b4428" {o(5)}/>'
            + ten(bo_x, bo_y + 8, 150, 26, .5))
    s += SL(Z_SRED, boch)
    # странник
    sx, sy, sh = 860, 1046, 560
    str_ = figura(sx, sy, sh, t, col="#4e4438", kant="#ffd98a", ph=.2, boroda=True)
    spx, spy = _plecho(sx, sy, sh, 1)
    # правый рукав тянется к плечу мальчика на бочке и поддерживает его
    mal_pl_x, mal_pl_y = bo_x - 46, bo_y - bo_h - 290 * .62
    ang_p = math.degrees(math.atan2(mal_pl_y - spy, mal_pl_x - spx))
    dl_p = math.hypot(mal_pl_x - spx, mal_pl_y - spy)
    r1, (hx1, hy1), _ = _ruka_ekr(sx, sy, sh, 1, dl_p, ang_p, t,
                                  "#4e4438", "#ffd98a", .1, 2)
    r2, (hx2, hy2), (slx, sly) = _ruka_ekr(sx, sy, sh, -1, sh * .42, 104 - 10 * pod, t,
                                           "#4e4438", "#ffd98a", .5, 4)
    str_ += r1 + r2
    # расставленные ноги
    str_ += (f'<line x1="{sx-30:.0f}" y1="{sy-sh*.30:.0f}" x2="{sx-104:.0f}"'
             f' y2="{sy-4:.0f}" stroke="#4e4438" stroke-width="40" stroke-linecap="round"/>'
             f'<line x1="{sx+30:.0f}" y1="{sy-sh*.30:.0f}" x2="{sx+104:.0f}"'
             f' y2="{sy-4:.0f}" stroke="#4e4438" stroke-width="40" stroke-linecap="round"/>')
    for i, (zx_, zy_) in enumerate(((-56, -.44), (30, -.32), (-16, -.20))):
        str_ += (f'<rect x="{sx+zx_:.0f}" y="{sy+sh*zy_:.0f}" width="58" height="48"'
                 f' rx="8" fill="#6a5a46" opacity=".8" {o(3)}/>')
    str_ += (f'<path d="M{sx-76:.0f},{sy-sh*.46:.0f} Q{sx:.0f},{sy-sh*.40:.0f}'
             f' {sx+76:.0f},{sy-sh*.46:.0f}" fill="none" stroke="#9a8a68"'
             f' stroke-width="13"/>')
    s += SL(Z_SRED, str_ + ten(sx, sy + 8, 150, 26, .5))

    # мальчик поднимается над головой странника
    mh2 = 290
    sx_m = bo_x
    my_ = bo_y - bo_h - 6
    mal = figura(sx_m, my_, mh2, t, col="#d8cbab", kant="#ffd98a", ph=.4,
                 naklon=-3 + 2 * pod)
    r3, _, (m1x, m1y) = _ruka_ekr(sx_m, my_, mh2, 1, mh2 * .44, -28 - 10 * pod, t, "#d8cbab",
                                  "#ffd98a", .2, 5)
    r4, _, (m2x, m2y) = _ruka_ekr(sx_m, my_, mh2, -1, mh2 * .44, -152 + 10 * pod, t, "#d8cbab",
                                  "#ffd98a", .6, 5)
    mal += r3 + r4
    # сорочка отклоняется вверх по ходу подъёма
    mal += (f'<path d="M{sx_m-72:.0f},{my_-40:.0f} Q{sx_m:.0f},{my_-72-40*pod:.0f}'
            f' {sx_m+72:.0f},{my_-40:.0f} L{sx_m+58:.0f},{my_-96:.0f}'
            f' Q{sx_m:.0f},{my_-120:.0f} {sx_m-58:.0f},{my_-96:.0f} Z" fill="#e4d9bc"'
            f' opacity=".9" {o(4)}/>')
    s += SL(Z_SRED, mal)
    s += SL(Z_SRED, f'<circle cx="{sx_m:.0f}" cy="{my_-150:.0f}" r="{150+24*pod:.0f}"'
                    f' fill="#ffe9ac" opacity="{.08+.05*pod:.2f}"/>')
    s += SL(Z_SRED, iskra_let(t, sx_m, my_ - 120, 7, 6, 300, .40))
    s += SL(Z_SRED, _polka_s_utvaryu(420, 420, 420, t, 131, 3))
    s += SL(Z_SRED, _lavka_krupno(260, 1050, 440, t, 150))
    s += SL(Z_SRED, _kadushki_i_grabli(1180, 1046, t, 133))
    s += SL(Z_PERED, _vetka_pered(-40, 60, 700, 24, t, 109, "#241c16", 6))
    s += SL(Z_LETIT, sneg_letit(t, 12, 37, .28, .55))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def vorota_lesnoy_obiteli(t):
    """Бревенчатая ограда и тесовые ворота обители среди елей, ворота
    распахнуты, в проёме настоящий осенний лес. Юноша с котомкой идёт к
    воротам со спины. У ворот колода с топором, поленница, улей-борть."""
    rnd = random.Random(115)
    s = nebo("den", t, False, 53)
    s += oblaka(t, 130, 5, 39, .45)

    px_, py_, pw_, ph_ = 700, 230, 790, 500
    put = kontur_proema(px_, py_, pw_, ph_, "arka")
    s += SL(Z_DAL, _vid_za_proemom(put, t, "les", 13)
            + mesto_stoka(px_, py_, pw_, ph_, "arka")
            + f'<path d="{put}" fill="none" stroke="#2a1d12" stroke-width="18"/>')

    # ограда из брёвен по сторонам ворот
    ogr = ""
    for bx, bw in ((-20, 640), (1540, 420)):
        ogr += (f'<rect x="{bx:.0f}" y="300" width="{bw:.0f}" height="520" rx="6"'
                f' fill="url(#brev)" {o(6)}/>')
        for i in range(9):
            ogr += (f'<rect x="{bx:.0f}" y="{306+i*58:.0f}" width="{bw:.0f}" height="50"'
                    f' rx="8" fill="url(#brev)" {o(3)}/>')
        ogr += (f'<path d="M{bx-20:.0f},300 L{bx+bw/2:.0f},230 L{bx+bw+20:.0f},300 Z"'
                f' fill="#4a3a28" {o(5)}/>')
    for sgn, vx in ((-1, px_ - 210), (1, px_ + pw_ + 10)):
        ug = sgn * (-16 + 2 * A.w(t, 4.4, .2))
        ogr += (f'<g transform="rotate({ug:.1f} {vx+(200 if sgn<0 else 0):.0f} {py_+ph_:.0f})">'
                f'<rect x="{vx:.0f}" y="{py_+40:.0f}" width="200" height="{ph_-10:.0f}"'
                f' rx="8" fill="url(#derev)" {o(6)}/>')
        for i in range(4):
            ogr += (f'<rect x="{vx+12+i*48:.0f}" y="{py_+56:.0f}" width="34"'
                    f' height="{ph_-42:.0f}" rx="6" fill="#6a5030" {o(3)}/>')
        ogr += (f'<rect x="{vx+4:.0f}" y="{py_+120:.0f}" width="192" height="24"'
                f' fill="{ZHELEZ}" {o(3)}/>'
                f'<rect x="{vx+4:.0f}" y="{py_+380:.0f}" width="192" height="24"'
                f' fill="{ZHELEZ}" {o(3)}/></g>')
    ogr += (f'<path d="M{px_-80:.0f},{py_+20:.0f} L{px_+pw_*.5:.0f},{py_-80:.0f}'
            f' L{px_+pw_+80:.0f},{py_+20:.0f} Z" fill="#4e3a24" {o(6)}/>'
            f'<rect x="{px_-100:.0f}" y="{py_+14:.0f}" width="{pw_+200:.0f}" height="26"'
            f' rx="9" fill="#5c4830" {o(5)}/>')
    s += SL(Z_SRED, ogr)

    # ели по сторонам ограды
    el = ""
    for i, (ex, eb, eh) in enumerate(((100, 560, 700), (360, 480, 520), (1800, 580, 720),
                                      (1580, 470, 480))):
        kach = 1.4 * A.w(t, 5.0 + i, i * .3)
        el += f'<g transform="rotate({kach:.2f} {ex:.0f} {eb:.0f})">'
        for k in range(4):
            yy = eb - eh * (k / 4.0)
            ww = eh * .38 * (1 - k / 5.2)
            el += (f'<path d="M{ex-ww:.0f},{yy:.0f} L{ex:.0f},{yy-eh*.36:.0f}'
                   f' L{ex+ww:.0f},{yy:.0f} Z" fill="{["#3e4f3e","#35463a"][k%2]}"'
                   f' {o(4)}/>')
        el += (f'<rect x="{ex-14:.0f}" y="{eb-20:.0f}" width="28" height="90"'
               f' fill="#3b2a1a" {o(3)}/></g>')
    s += SL(Z_DAL, el)
    s += SL(Z_SRED, dym(430, 250, t, 5, .26, 300, .36, "#d3dae2", .9))

    zem = f'<rect x="0" y="810" width="{W}" height="270" fill="#4e3f2c"/>'
    zem += _zemlya_faktura(850, 1060, 111, 14)
    zem += _listya(113, 30, 840, 1060)
    zem += _trava(rnd, 10, 870, 1050)
    s += SL(Z_SRED, zem)

    # колода с топором
    s += SL(Z_SRED, f'<ellipse cx="340" cy="880" rx="120" ry="34" fill="#7b5c38" {o(5)}/>'
                    f'<rect x="220" y="880" width="240" height="170" rx="10"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<path d="M352,880 L330,790 L300,804 L306,874 Z" fill="url(#zhel)"'
                    f' {o(5)}/>'
                    f'<rect x="318" y="760" width="22" height="60" rx="8"'
                    f' fill="url(#derev)" {o(4)}/>'
                    f'<path d="M306,812 L328,804" stroke="#e6eef6" stroke-width="7"'
                    f' opacity=".7"/>')
    s += SL(Z_SRED, _polenica(20, 700, 190, 300, 115, 24))
    s += SL(Z_SRED, f'<path d="M620,1080 Q820,944 {px_+pw_*.34:.0f},{py_+ph_-8:.0f}'
                    f' L{px_+pw_*.70:.0f},{py_+ph_-8:.0f} Q1240,944 1440,1080 Z"'
                    f' fill="#6a5236" opacity=".85"/>'
                    f'<path d="M680,1078 Q860,952 {px_+pw_*.40:.0f},{py_+ph_-6:.0f}"'
                    f' fill="none" stroke="#7d6243" stroke-width="7" opacity=".6"/>')

    # улей-борть
    s += SL(Z_SRED, f'<path d="M1660,1050 L1640,820 Q1740,786 1840,820 L1820,1050 Z"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<ellipse cx="1740" cy="820" rx="100" ry="30" fill="#5b4428" {o(4)}/>'
                    f'<ellipse cx="1740" cy="930" rx="24" ry="16" fill="#2a1d12" {o(3)}/>'
                    f'<rect x="1636" y="880" width="208" height="18" rx="7" fill="#8a6a3c"'
                    f' {o(3)}/>')
    for i in range(5):
        pz = ((t * .7 + i * .2) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{1740+120*math.cos(pz*6.283+i):.0f}"'
                        f' cy="{900+60*math.sin(pz*6.283+i*1.7):.0f}" rx="9" ry="6"'
                        f' fill="#d8a14a" opacity=".85"/>')

    # юноша с котомкой идёт к воротам со спины
    vh = A.ease(A.seg(t, .4, 2.0))
    fx, fy, fh = 560 - 90 * vh, 1052 - 40 * vh, 660 - 60 * vh
    yun = figura(fx, fy, fh, t, col="#4a4254", kant="#ffd98a", ph=.2)
    r1, (px2, py2), (ypx, ypy) = _ruka_ekr(fx, fy, fh, 1, fh * .44, 78, t, "#4a4254", "#ffd98a",
                                           .1, 5)
    r2, _, (ylx, yly) = _ruka_ekr(fx, fy, fh, -1, fh * .30, 206, t, "#4a4254", "#ffd98a", .5, 4)
    yun += r1 + r2
    yun += (f'<line x1="{px2:.0f}" y1="{py2-150:.0f}" x2="{px2+10:.0f}" y2="{fy+4:.0f}"'
            f' stroke="url(#derev)" stroke-width="16" stroke-linecap="round"/>')
    # котомка за плечами
    yun += (f'<path d="M{fx-fh*.34:.0f},{fy-fh*.44:.0f}'
            f' Q{fx-fh*.44:.0f},{fy-fh*.30:.0f} {fx-fh*.34:.0f},{fy-fh*.16:.0f}'
            f' Q{fx-fh*.22:.0f},{fy-fh*.10:.0f} {fx-fh*.16:.0f},{fy-fh*.24:.0f}'
            f' Q{fx-fh*.16:.0f},{fy-fh*.38:.0f} {fx-fh*.34:.0f},{fy-fh*.44:.0f} Z"'
            f' fill="#7a6342" {o(5)}/>'
            f'<path d="M{fx-fh*.30:.0f},{fy-fh*.44:.0f} Q{fx-fh*.22:.0f},'
            f'{fy-fh*.56:.0f} {fx-fh*.12:.0f},{fy-fh*.52:.0f}" fill="none"'
            f' stroke="#8a7a58" stroke-width="9"/>'
            f'<path d="M{fx-fh*.30:.0f},{fy-fh*.32:.0f} L{fx-fh*.18:.0f},'
            f'{fy-fh*.28:.0f}" stroke="#5e4a2e" stroke-width="6"/>')
    s += SL(Z_SRED, yun + ten(fx, fy + 6, 110 - 20 * vh, 20, .45))
    s += SL(Z_SRED, _kadushki_i_grabli(560, 1064, t, 143))
    s += SL(Z_SRED, _polka_s_utvaryu(240, 700, 400, t, 153, 3))
    s += SL(Z_SRED, _polenica(1600, 740, 280, 230, 401, 24))
    s += SL(Z_SRED, _dvorovaya_utvar(880, 1072, 420, t, 403, ["korob", "meshok"]))
    s += SL(Z_SRED, _listya(155, 22, 880, 1060))
    s += SL(Z_SRED, _dvorovaya_utvar(1240, 1070, 360, t, 145, ["meshok", "korzina"]))
    s += SL(Z_PERED, _stolb_pered(1874, 106, "#1d1611", 0, H))
    s += SL(Z_LETIT, sneg_letit(t, 12, 41, .3, .6))
    s += ramka_pp("oba")
    s += vinetka(.42)
    return s


def gorozhane_zovut_ionu(t):
    """Городская площадь: толпа со спины — шапки, платки, посохи. Седобородый
    старец на крыльце, руки сложены на посохе; старшина подаёт ему на рушнике
    хлеб-соль. Над площадью летят вверх шапки. У крыльца бочки, сани, собака."""
    rnd = random.Random(116)
    s = nebo("den", t, False, 57)
    s += oblaka(t, 120, 6, 43, .5)
    s += SL(Z_DAL, _derevnya_ryad(400, t, 117, ((130, 400), (1800, 420))))
    # палаты за крыльцом
    s += SL(Z_DAL, brevna(420, 60, 1100, 560, 92)
            + f'<rect x="420" y="60" width="1100" height="560" fill="none" {o(9)}/>')
    s += SL(Z_DAL, okno_izby(520, 180, 260, 230, t, svet=True)
            + okno_izby(1180, 180, 260, 230, t, svet=True)
            + teplo(650, 300, 230, 190, .40) + teplo(1310, 300, 230, 190, .40))
    s += SL(Z_DAL, dver(860, 150, 300, 480, .0, "url(#derev)", True, False))
    s += SL(Z_DAL, dym(1800, 200, t, 5, .26, 280, .34, "#d3dae2", .9))

    zem = f'<rect x="0" y="700" width="{W}" height="380" fill="#4e3f2c"/>'
    zem += _zemlya_faktura(760, 1060, 119, 16)
    zem += _listya(121, 24, 760, 1060)
    s += SL(Z_SRED, zem)
    s += SL(Z_SRED, _kryl_co(620, 620, 700, 200, t, 4, True, True))

    # бочки, сани, собака у крыльца
    s += SL(Z_SRED, _dvorovaya_utvar(40, 880, 520, t, 123, ["kadka", "kadka", "korob"]))
    sani = (f'<path d="M1480,980 Q1560,936 1800,936 L1812,980 Z" fill="url(#derev)"'
            f' {o(5)}/>'
            f'<rect x="1500" y="880" width="300" height="60" rx="10" fill="#5b4428"'
            f' {o(5)}/>'
            f'<line x1="1530" y1="940" x2="1530" y2="980" stroke="#4a3522"'
            f' stroke-width="14"/>'
            f'<line x1="1740" y1="940" x2="1740" y2="980" stroke="#4a3522"'
            f' stroke-width="14"/>'
            f'<path d="M1470,984 Q1580,962 1824,962" fill="none" stroke="{ZHELEZ}"'
            f' stroke-width="10"/>')
    s += SL(Z_SRED, sani)
    s += SL(Z_SRED, f'<ellipse cx="1360" cy="1040" rx="94" ry="40" fill="#54402a"'
                    f' {o(4)}/>'
                    f'<ellipse cx="1278" cy="1012" rx="42" ry="35" fill="#54402a" {o(4)}/>'
                    f'<path d="M1248,994 L1238,956 L1274,974 Z" fill="#43321f" {o(3)}/>'
                    f'<circle cx="1262" cy="1008" r="5" fill="#120c08"/>'
                    f'<path d="M1448,1026 Q1498,{988-16*A.w(t,1.4,.2):.0f} 1512,1038"'
                    f' fill="none" stroke="#54402a" stroke-width="15"'
                    f' stroke-linecap="round"/>')

    # толпа со спины: шапки, платки, посохи
    # толпа: три глубины, рост и цвет у каждого свой, шаг неровный
    CVET = ["#39323f", "#4a3b2a", "#2f3a44", "#523340", "#3d4a3a", "#5a4a32",
            "#2e3a34", "#4a3346", "#3a4452", "#54412c"]
    # глубины разведены сильнее (0.54 / 0.80 / 1.10): иначе крупный из
    # дальнего ряда оказывался по соседству с крупным из ближнего и
    # кратность роста падала до 1.05
    ryady = ((1, 0.54, 936, 150), (0, 0.80, 1012, 196), (2, 1.10, 1074, 238))
    for sloy, msh, ty0, step in ryady:
        tol = ""
        x0 = 40 + sloy * 70
        i = 0
        while x0 < W + 80:
            # РОСТ СОСЕДЕЙ ОТЛИЧАЕТСЯ НЕ МЕНЬШЕ ЧЕМ В ПОЛТОРА РАЗА, ШАГ
            # РВАНЫЙ, ЧАСТЬ ФИГУР СО СПИНЫ И В ПРОФИЛЬ, ДВОЕ-ТРОЕ СТОЯТ
            # ВПЛОТНУЮ И ПЕРЕКРЫВАЮТ ДРУГ ДРУГА. Осмотр 15.11, второй заход:
            # «внизу снова читается ровный ряд одинаковых мелких фигур с
            # равным шагом» — прежнего разброса ±52 по росту и ±62 по базе
            # глазу не хватило, ряд всё равно складывался в орнамент.
            krup = (i % 2 == 0)              # строго через одного
            th = (362 if krup else 150) * msh * rnd.uniform(.92, 1.08)
            ty = ty0 - rnd.uniform(0, 70) - (0 if krup else 38)
            col = CVET[rnd.randrange(len(CVET))]
            pl = rnd.random() < .42
            d = figura(x0, ty, th, t, col=col, kant="#cfe4f5", platok=pl,
                       ph=rnd.uniform(0, 1), shapka=not pl,
                       profil=rnd.random() < .50,
                       lico=rnd.random() > .32,
                       naklon=rnd.uniform(-15, 15),
                       op=.72 + .28 * msh)
            if rnd.random() < .32:
                rr, (qx, qy), (a1x, a1y) = _ruka_ekr(x0, ty, th, 1, th * .36,
                                                     62 + rnd.uniform(-18, 18), t, col,
                                                     "#cfe4f5", rnd.uniform(0, 1), 4)
                d += rr + (f'<line x1="{qx:.0f}" y1="{qy-th*.58:.0f}"'
                           f' x2="{qx+8:.0f}" y2="{ty+4:.0f}" stroke="url(#derev)"'
                           f' stroke-width="{11*msh:.0f}" stroke-linecap="round"/>')
            tol += d
            # треть шагов — почти вплотную: фигуры заходят одна за другую
            x0 += step * (rnd.uniform(.24, .44) if rnd.random() < .34
                          else rnd.uniform(.78, 1.62))
            i += 1
        s += SL(Z_DAL if sloy == 1 else Z_SRED, tol)

    # шапки летят вверх
    # ШАПКИ ЛЕТЯТ ВРАЗНОБОЙ: было ровно девять штук через 200 px — ряд
    # одинаковых предметов равным шагом читается узором, а не радостью
    shap = ""
    for i, (hx_, hs_, hf_) in enumerate(((150, 1.14, .00), (372, .82, .37),
                                         (470, 1.04, .62), (690, .72, .18),
                                         (902, 1.22, .81), (1024, .88, .44),
                                         (1290, .96, .07), (1416, 1.10, .70),
                                         (1664, .78, .29), (1842, 1.02, .52))):
        p = ((t * .55 + hf_) % 1.0)
        hy_ = 1000 - (620 + 180 * hs_) * math.sin(math.pi * p * .9)
        rot = 240 * p + i * 47
        shap += (f'<g transform="rotate({rot:.0f} {hx_:.0f} {hy_:.0f})">'
                 f'<path d="M{hx_-44:.0f},{hy_:.0f} Q{hx_-30:.0f},{hy_-56:.0f}'
                 f' {hx_:.0f},{hy_-58:.0f} Q{hx_+30:.0f},{hy_-56:.0f}'
                 f' {hx_+44:.0f},{hy_:.0f} Z"'
                 f' fill="{["#3a3040","#5e4a3a","#4a3b2a","#4a3346"][i%4]}" {o(4)}/>'
                 f'<rect x="{hx_-54:.0f}" y="{hy_-10:.0f}" width="108" height="26" rx="12"'
                 f' fill="#6b5236" {o(3)}/></g>')
    s += SL(Z_SRED, shap)

    # старец на крыльце, руки сложены на посохе
    sk = A.ease(A.seg(t, 1.0, 1.2))
    sx, sy, sh = 1120, 636, 620
    star = figura(sx, sy, sh, t, col="#2e2a34", kant="#ffd98a", ph=.2, boroda=True,
                  naklon=7 * sk)
    r1, (hx1, hy1), (spx, spy) = _ruka_ekr(sx, sy, sh, 1, sh * .40, 62, t, "#2e2a34", "#ffd98a",
                                           .1, 3)
    r2, _, (slx, sly) = _ruka_ekr(sx, sy, sh, -1, sh * .40, 118, t, "#2e2a34", "#ffd98a", .5, 3)
    star += r1 + r2
    star += (f'<line x1="{sx+10:.0f}" y1="{sy-sh*.60:.0f}" x2="{sx+18:.0f}" y2="{sy+6:.0f}"'
             f' stroke="url(#derev)" stroke-width="18" stroke-linecap="round"/>'
             f'<circle cx="{sx+8:.0f}" cy="{sy-sh*.62:.0f}" r="20" fill="#5e442a" {o(3)}/>')
    # борода от подбородка, лежит на груди
    star += (f'<path d="M{sx-50:.0f},{sy-sh*.74:.0f} Q{sx:.0f},{sy-sh*.40+8*sk:.0f}'
             f' {sx+50:.0f},{sy-sh*.74:.0f} Q{sx:.0f},{sy-sh*.66:.0f}'
             f' {sx-50:.0f},{sy-sh*.74:.0f} Z" fill="#d8d2c4" opacity=".95" {o(4)}/>')
    s += SL(Z_SRED, star)

    # старшина подаёт хлеб-соль на рушнике
    ox, oy, oh = 700, 860, 520
    ost = figura(ox, oy, oh, t, col="#4b3550", kant="#ffd98a", ph=.5, boroda=True)
    r3, (q1x, q1y), (o1x, o1y) = _ruka_ekr(ox, oy, oh, 1, oh * .44, -48, t, "#4b3550", "#ffd98a",
                                           .2, 4)
    r4, (q2x, q2y), (o2x, o2y) = _ruka_ekr(ox, oy, oh, -1, oh * .44, -22, t, "#4b3550",
                                           "#ffd98a", .6, 4)
    ost += r3 + r4
    rx_, ry_ = (q1x + q2x) / 2, (q1y + q2y) / 2
    ost += (f'<path d="M{rx_-150:.0f},{ry_:.0f} Q{rx_:.0f},{ry_-50:.0f}'
            f' {rx_+150:.0f},{ry_:.0f} L{rx_+150:.0f},{ry_+40:.0f}'
            f' Q{rx_:.0f},{ry_-10:.0f} {rx_-150:.0f},{ry_+40:.0f} Z" fill="{RUSH}" {o(4)}/>')
    for i in range(5):
        ux = rx_ - 124 + i * 62
        ost += (f'<path d="M{ux:.0f},{ry_+8:.0f} L{ux+16:.0f},{ry_-12:.0f}'
                f' L{ux+32:.0f},{ry_+8:.0f} Z" fill="{KRAS}" opacity=".75"/>')
    ost += karavay(rx_, ry_ - 26, 1.5, False)
    s += SL(Z_SRED, ost)
    s += SL(Z_PERED, _stolb_pered(-6, 96, "#1d1611", 0, H))
    s += SL(Z_LETIT, sneg_letit(t, 12, 45, .28, .55))
    s += ramka_pp("oba")
    s += vinetka(.42)
    return s


def tri_dela_vladyki(t):
    """Три сцены по словам, старец везде со спины: держит весы над двумя
    спорщиками; заслоняет вдову с ребёнком от купца с долговой книгой;
    подаёт нищему каравай. Борода белеет от сцены к сцене."""
    rnd = random.Random(117)
    pol = 790
    s = _stena_gornicy(t, 11, True, pol)
    s += SL(Z_DAL, svody(t, "#4b443b", 3))
    for dx in (640, 1280):
        s += SL(Z_DAL, f'<rect x="{dx:.0f}" y="0" width="34" height="{pol:.0f}"'
                       f' fill="#4e3220" opacity=".7"/>')
    for i, ox in enumerate((250, 940, 1620)):
        s += SL(Z_DAL, okno_izby(ox - 110, 150, 230, 210, t, svet=False, moroz=.35))
        s += SL(Z_DAL, zanaveska(ox - 110, 140, 130, 100, TKAN, t, 1))
    s += SL(Z_DAL, _polka_s_utvaryu(420, 430, 420, t, 125, 3)
            + _polka_s_utvaryu(1380, 430, 420, t, 127, 3))

    # свечи в подсвечниках — по свече на каждую сцену
    for i, sx_ in enumerate((430, 1080, 1760)):
        s += SL(Z_SRED, f'<rect x="{sx_-34:.0f}" y="{pol-26:.0f}" width="68" height="26"'
                        f' rx="9" fill="{ZHELEZ}" {o(4)}/>'
                        f'<rect x="{sx_-12:.0f}" y="{pol-96:.0f}" width="24" height="76"'
                        f' rx="8" fill="{ZHELEZ}" {o(3)}/>'
                        + svecha(sx_, pol - 96, t, i * .3, 1.5))
    s += SL(Z_SRED, teplo(1080, 640, 520, 420, .36))

    for i, (lx, ly, lw) in enumerate(((96, 1046, 440), (806, 1056, 350),
                                      (1486, 1038, 480))):
        s += SL(Z_SRED, _lavka_krupno(lx, ly, lw, t, 120 + i * 14, i == 1))
    s += SL(Z_SRED, mebel_hlam(60, 900, 320, t, 23))

    prost = ""
    for dx2 in (650, 1300):
        prost += (f'<rect x="{dx2:.0f}" y="0" width="54" height="{pol+120:.0f}"'
                  f' fill="#2a1d12" {o(6)}/>'
                  f'<rect x="{dx2+10:.0f}" y="0" width="16" height="{pol+120:.0f}"'
                  f' fill="#3e2c1c" opacity=".8"/>'
                  f'<path d="M{dx2-34:.0f},84 L{dx2+88:.0f},84 L{dx2+74:.0f},130'
                  f' L{dx2-20:.0f},130 Z" fill="#4e3a24" {o(4)}/>')
    s += SL(Z_SRED, prost)
    pr = (t * .34) % 1.0
    # ── первая: старец на скамье держит весы, чаши ровные
    ax, ay, ah = 330, 920, 480
    rov = A.ease(A.seg(t, .4, 1.1))
    st1 = figura(ax, ay, ah, t, col="#2e2a34", kant="#ffd98a", ph=.2, boroda=True)
    r1, (v1x, v1y), (p1x, p1y) = _ruka_ekr(ax, ay, ah, 1, ah * .44, -28, t, "#2e2a34", "#ffd98a",
                                           .1, 4)
    r2, _, (p2x, p2y) = _ruka_ekr(ax, ay, ah, -1, ah * .40, 48, t, "#2e2a34", "#ffd98a", .5, 4)
    st1 += r1 + r2
    st1 += (f'<path d="M{ax-44:.0f},{ay-ah*.72:.0f} Q{ax:.0f},{ay-ah*.46:.0f}'
            f' {ax+44:.0f},{ay-ah*.72:.0f} Z" fill="#cfc8ba" opacity=".9" {o(3)}/>')
    nak = 14 * (1 - rov)
    ves = (f'<g transform="rotate({nak:.1f} {v1x:.0f} {v1y:.0f})">'
           f'<rect x="{v1x-130:.0f}" y="{v1y-9:.0f}" width="260" height="16" rx="7"'
           f' fill="{ZHELEZ}" {o(3)}/>'
           f'<line x1="{v1x-118:.0f}" y1="{v1y:.0f}" x2="{v1x-118:.0f}" y2="{v1y+62:.0f}"'
           f' stroke="{ZHELEZ}" stroke-width="4"/>'
           f'<line x1="{v1x+118:.0f}" y1="{v1y:.0f}" x2="{v1x+118:.0f}" y2="{v1y+62:.0f}"'
           f' stroke="{ZHELEZ}" stroke-width="4"/>'
           f'<path d="M{v1x-168:.0f},{v1y+62:.0f} Q{v1x-118:.0f},{v1y+112:.0f}'
           f' {v1x-68:.0f},{v1y+62:.0f} Z" fill="url(#zhel)" {o(4)}/>'
           f'<path d="M{v1x+68:.0f},{v1y+62:.0f} Q{v1x+118:.0f},{v1y+112:.0f}'
           f' {v1x+168:.0f},{v1y+62:.0f} Z" fill="url(#zhel)" {o(4)}/></g>')
    s += SL(Z_SRED, st1 + ves)
    # НИЖНИЙ РЯД ВРАЗНОБОЙ (осмотр 15.11, второй заход: «то же самое в нижнем
    # ряду»). Рост соседей 452 · 268 · 236 — каждый следующий в полтора-два
    # раза иной, базы 1046-1062-1030 разные, шаги 214 и 112 рваные, третий
    # зритель заходит на спорщика, двое из трёх даны со спины и в профиль.
    SPOR = (("#5a3340", 104, 1046, 452, -11, 0, 1, 1),
            ("#3d4a3a", 318, 1062, 268, 13, 1, 0, 0),
            ("#54412c", 430, 1030, 236, -6, 0, 0, 1))
    for i, (col2, sx_, sy2, sh2, nak2, shap2, bor2, prof2) in enumerate(SPOR):
        d = figura(sx_, sy2, sh2, t, col=col2, kant="#cfe4f5", ph=.3 + i * .2,
                   shapka=bool(shap2), boroda=bool(bor2), profil=bool(prof2),
                   lico=(i != 2), naklon=nak2)
        rr, _, (q1x, q1y) = _ruka(sx_, sy2, sh2, 1 if i == 1 else -1,
                                  sh2 * (.46 if i == 1 else .38), -34 + 66 * (i == 1),
                                  t, col2, "#cfe4f5", i * .3, 6)
        s += SL(Z_SRED, d + rr)

    # ── вторая: заслоняет вдову с ребёнком от купца с книгой
    bx_, by_, bh_ = 1000, 1016, 596
    zasl = A.ease(A.seg(t, 2.0, 1.1))
    st2 = figura(bx_, by_, bh_, t, col="#2e2a34", kant="#ffd98a", ph=.4, boroda=True,
                 naklon=-8 * zasl)
    r3, _, (p3x, p3y) = _ruka_ekr(bx_, by_, bh_, -1, bh_ * .52, -178 + 16 * zasl, t, "#2e2a34",
                                  "#ffd98a", .2, 4)
    r4, _, (p4x, p4y) = _ruka_ekr(bx_, by_, bh_, 1, bh_ * .38, 36, t, "#2e2a34", "#ffd98a", .6, 4)
    st2 += r3 + r4
    st2 += (f'<path d="M{bx_-48:.0f},{by_-bh_*.72:.0f} Q{bx_:.0f},{by_-bh_*.40:.0f}'
            f' {bx_+48:.0f},{by_-bh_*.72:.0f} Z" fill="#e2ded2" opacity=".95" {o(3)}/>')
    s += SL(Z_SRED, st2)
    vd = figura(798, 1044, 486, t, col="#4e3a50", kant="#cfe4f5", platok=True, ph=.7,
                naklon=6)
    s += SL(Z_SRED, vd + figura(700, 1058, 214, t, col="#8e8068", kant="#cfe4f5",
                                ph=.3, profil=True))
    kx_, ky_, kh_ = 1230, 1038, 470
    kup = figura(kx_, ky_, kh_, t, col="#4b3550", kant="#ffd98a", ph=.5, boroda=True,
                 profil=True, naklon=-7)
    r5, (bkx, bky), (p5x, p5y) = _ruka_ekr(kx_, ky_, kh_, -1, kh_ * .40, -156, t, "#4b3550",
                                           "#ffd98a", .3, 4)
    kup += r5
    kup += (f'<path d="M{bkx-70:.0f},{bky-56:.0f} L{bkx+70:.0f},{bky-56:.0f}'
            f' L{bkx+70:.0f},{bky+56:.0f} L{bkx-70:.0f},{bky+56:.0f} Z" fill="#6b4a2c"'
            f' {o(5)}/>'
            f'<rect x="{bkx-62:.0f}" y="{bky-48:.0f}" width="124" height="96" rx="5"'
            f' fill="#e4dcc4" {o(3)}/>')
    for i in range(4):
        kup += (f'<path d="M{bkx-46:.0f},{bky-28+i*24:.0f} Q{bkx-10:.0f},'
                f'{bky-38+i*24:.0f} {bkx+28:.0f},{bky-28+i*24:.0f}" fill="none"'
                f' stroke="#8a7a58" stroke-width="4"/>')
    s += SL(Z_SRED, kup)

    # ── третья: подаёт нищему каравай
    cx_, cy_, ch_ = 1626, 994, 524
    dat = A.ease(A.seg(t, 3.6, 1.1))
    st3 = figura(cx_, cy_, ch_, t, col="#2e2a34", kant="#ffd98a", ph=.6, boroda=True,
                 profil=True, naklon=9 * dat)
    r6, (k1x, k1y), (p6x, p6y) = _ruka_ekr(cx_, cy_, ch_, 1, ch_ * .44, 4 - 24 * dat, t,
                                           "#2e2a34", "#ffd98a", .1, 3)
    r7, (k2x, k2y), (p7x, p7y) = _ruka_ekr(cx_, cy_, ch_, -1, ch_ * .44, 30 - 24 * dat, t,
                                           "#2e2a34", "#ffd98a", .5, 3)
    st3 += r6 + r7
    st3 += (f'<path d="M{cx_-52:.0f},{cy_-ch_*.72:.0f} Q{cx_:.0f},{cy_-ch_*.36:.0f}'
            f' {cx_+52:.0f},{cy_-ch_*.72:.0f} Z" fill="#f2efe6" opacity=".95" {o(3)}/>')
    s += SL(Z_SRED, st3)
    # каравай идёт в ПРАВОЙ руке, наружу к нищему: от середины между кистями
    # он ложился старцу на грудь, когда левый рукав прижимался к телу
    kar_x = k1x + _predmet_naruzhu(cx_, ch_, k1x, 230) + 60 * dat
    s += SL(Z_SRED, karavay(kar_x, k1y + 24, 1.5, True))
    nx_, ny_, nh_ = 1786, 1066, 306
    nish = figura(nx_, ny_, nh_, t, col="#6a5a46", kant="#cfe4f5", ph=.8, boroda=True,
                  naklon=15, profil=True)
    r8, _, (p8x, p8y) = _ruka_ekr(nx_, ny_, nh_, -1, nh_ * .46, -164, t, "#6a5a46", "#cfe4f5",
                                  .4, 5)
    s += SL(Z_SRED, nish + r8)
    # третий зритель третьего пролёта: заходит на владыку и ломает линию
    zr = figura(1450, 1038, 240, t, col="#2e3a34", kant="#cfe4f5", ph=.8,
                shapka=True, lico=False, naklon=9)
    rz, _, _ = _ruka(1450, 1038, 240, -1, 240 * .42, 64, t, "#2e3a34",
                     "#cfe4f5", .8, 4)
    s += SL(Z_SRED, zr + rz + ten(1450, 1044, 56, 12, .4))
    s += SL(Z_PERED, _stolb_pered(-4, 84, "#140f0b", 0, H))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def tihiy_uchenik_v_shkolnom_klasse(t):
    """Школьный класс: парты с откидными крышками, чёрная доска, глобус,
    чернильницы, портфели на крючках. Трое на перемене дерутся портфелями,
    у стены за последней партой сидит тихий мальчик в очках; следующий миг —
    он у доски, в правой руке мел, в левой тряпка."""
    rnd = random.Random(118)
    pol = 820
    s = f'<rect width="{W}" height="{H}" fill="#3b3a36"/>'
    s += SL(Z_DAL, doski(0, 0, W, pol, 70, False, "dosk"))
    s += SL(Z_DAL, f'<rect x="0" y="{pol-130:.0f}" width="{W}" height="26"'
                   f' fill="#5b4428" opacity=".85"/>'
                   f'<rect x="0" y="{pol-20:.0f}" width="{W}" height="36"'
                   f' fill="#2f2a22" opacity=".85"/>')
    s += SL(Z_DAL, polovicy(pol + 20))

    # чёрная доска
    dx_, dy_, dw, dh = 250, 150, 1060, 430
    dos = (f'<rect x="{dx_-24:.0f}" y="{dy_-24:.0f}" width="{dw+48:.0f}"'
           f' height="{dh+48:.0f}" rx="10" fill="#6b5a3c" {o(6)}/>'
           f'<rect x="{dx_:.0f}" y="{dy_:.0f}" width="{dw:.0f}" height="{dh:.0f}"'
           f' rx="6" fill="#23302a" {o(4)}/>'
           f'<rect x="{dx_-30:.0f}" y="{dy_+dh+24:.0f}" width="{dw+60:.0f}" height="26"'
           f' rx="8" fill="#7a6342" {o(4)}/>')
    # решённая задача — волнистыми строками, букв не рисуем
    pis = min(1.0, max(.0, (t - 2.6) * .55))
    for i in range(5):
        ly = dy_ + 90 + i * 66
        dl = (dw - 160) * min(1.0, max(.0, pis * 5 - i))
        if dl > 4:
            dos += (f'<path d="M{dx_+70:.0f},{ly:.0f} Q{dx_+70+dl*.25:.0f},{ly-18:.0f}'
                    f' {dx_+70+dl*.5:.0f},{ly:.0f} Q{dx_+70+dl*.75:.0f},{ly+18:.0f}'
                    f' {dx_+70+dl:.0f},{ly:.0f}" fill="none" stroke="#e8ecd8"'
                    f' stroke-width="7" opacity=".9"/>')
    # ДОСКА НЕ ПУСТАЯ (осмотр 15.11: до 2,6 с это было ровное зелёное поле на
    # четверть кадра). На ней всегда есть прошлый урок: чертёж с прямым углом
    # и штриховкой, окружность с радиусом, два столбика палочек, уголок
    # деления, затёртые разводы от тряпки, лоток с мелом и указка.
    tri = (dx_ + 118, dy_ + 338)
    dos += (f'<path d="M{tri[0]:.0f},{tri[1]:.0f} L{tri[0]+250:.0f},{tri[1]:.0f}'
            f' L{tri[0]:.0f},{tri[1]-172:.0f} Z" fill="none" stroke="#dfe6cf"'
            f' stroke-width="6" opacity=".88"/>'
            f'<rect x="{tri[0]+4:.0f}" y="{tri[1]-34:.0f}" width="30" height="30"'
            f' fill="none" stroke="#dfe6cf" stroke-width="4" opacity=".8"/>')
    for i in range(7):
        dos += (f'<line x1="{tri[0]+26+i*30:.0f}" y1="{tri[1]:.0f}"'
                f' x2="{tri[0]+6+i*30:.0f}" y2="{tri[1]-24-i*6:.0f}"'
                f' stroke="#c8d2bc" stroke-width="3" opacity=".7"/>')
    okr = (dx_ + 560, dy_ + 262)
    dos += (f'<circle cx="{okr[0]:.0f}" cy="{okr[1]:.0f}" r="96" fill="none"'
            f' stroke="#dfe6cf" stroke-width="6" opacity=".88"/>'
            f'<line x1="{okr[0]:.0f}" y1="{okr[1]:.0f}" x2="{okr[0]+68:.0f}"'
            f' y2="{okr[1]-68:.0f}" stroke="#dfe6cf" stroke-width="5" opacity=".8"/>'
            f'<circle cx="{okr[0]:.0f}" cy="{okr[1]:.0f}" r="7" fill="#e8ecd8"'
            f' opacity=".9"/>')
    for st_ in (0, 1):
        for i in range(6):
            dos += (f'<line x1="{dx_+770+st_*86+i*13:.0f}" y1="{dy_+200:.0f}"'
                    f' x2="{dx_+766+st_*86+i*13:.0f}" y2="{dy_+268:.0f}"'
                    f' stroke="#dfe6cf" stroke-width="5" opacity=".82"/>')
    dos += (f'<path d="M{dx_+760:.0f},{dy_+300:.0f} h190 M{dx_+950:.0f},{dy_+300:.0f}'
            f' v76" fill="none" stroke="#dfe6cf" stroke-width="5" opacity=".85"/>'
            f'<path d="M{dx_+770:.0f},{dy_+348:.0f} q40,-20 86,2 q44,22 92,-6"'
            f' fill="none" stroke="#c8d2bc" stroke-width="6" opacity=".7"/>')
    for i, (ex_, ew) in enumerate(((dx_ + 300, 240), (dx_ + 690, 190),
                                   (dx_ + 120, 150))):
        dos += (f'<ellipse cx="{ex_:.0f}" cy="{dy_+56+i*34:.0f}" rx="{ew:.0f}"'
                f' ry="26" fill="#cfe0c8" opacity=".10"/>')
    dos += (f'<path d="M{dx_+60:.0f},{dy_+46:.0f} h420" stroke="#dfe6cf"'
            f' stroke-width="5" opacity=".55"/>')
    for i, mx_ in enumerate((dx_ + 70, dx_ + 118, dx_ + 158)):
        dos += (f'<rect x="{mx_:.0f}" y="{dy_+dh+26:.0f}" width="{34-i*5:.0f}"'
                f' height="18" rx="7" fill="#f2efe2" {o(2)}/>')
    dos += (f'<rect x="{dx_+230:.0f}" y="{dy_+dh+22:.0f}" width="86" height="26"'
            f' rx="9" fill="#5c87a8" {o(3)}/>'
            f'<rect x="{dx_+250:.0f}" y="{dy_+dh+16:.0f}" width="48" height="12"'
            f' rx="5" fill="#e4dcc4" opacity=".8"/>'
            f'<g transform="rotate(-72 {dx_+dw-40:.0f} {dy_+dh+40:.0f})">'
            f'<rect x="{dx_+dw-48:.0f}" y="{dy_+dh+40:.0f}" width="16" height="520"'
            f' rx="7" fill="url(#derev)" {o(3)}/>'
            f'<circle cx="{dx_+dw-40:.0f}" cy="{dy_+dh+44:.0f}" r="15"'
            f' fill="#5e442a" {o(2)}/></g>')
    s += SL(Z_SRED, dos)

    # глобус, чернильницы, портфели на крючках, карта-рейка
    gl = 8 * A.w(t, 4.0, .2)
    s += SL(Z_SRED, f'<rect x="1545" y="470" width="30" height="110" rx="9"'
                    f' fill="#5b4428" {o(4)}/>'
                    f'<ellipse cx="1560" cy="590" rx="66" ry="18" fill="#4a3522" {o(4)}/>'
                    f'<g transform="translate(335 0)">'
                    f'<g transform="rotate({gl:.1f} 1225 370)">'
                    f'<circle cx="1225" cy="370" r="104" fill="#5c87a8" {o(5)}/>'
                    f'<path d="M1150,330 Q1200,300 1256,336 Q1300,364 1270,404'
                    f' Q1220,430 1176,398 Z" fill="#6f9a5e" {o(3)}/>'
                    f'<path d="M1130,392 Q1180,420 1240,430" fill="none" stroke="#6f9a5e"'
                    f' stroke-width="18" opacity=".85"/>'
                    f'<path d="M1121,370 L1329,370" stroke="#2a3a46" stroke-width="4"'
                    f' opacity=".6"/>'
                    f'<path d="M1225,266 Q1310,370 1225,474" fill="none" stroke="{ZHELEZ}"'
                    f' stroke-width="11"/></g></g>')
    kr = ""
    for i in range(5):
        hx = 1230 + i * 92
        kch = 3.0 * A.w(t, 2.6, i * .3)
        kr += (f'<rect x="{hx-6:.0f}" y="188" width="12" height="36" fill="{ZHELEZ}"'
               f' {o(2)}/>'
               f'<g transform="rotate({kch:.1f} {hx:.0f} 220)">'
               f'<rect x="{hx-42:.0f}" y="220" width="84" height="104" rx="9"'
               f' fill="{["#4a3522","#5e3a2a","#3a4452","#5a4a2e","#4e3a50"][i]}" {o(4)}/>'
               f'<rect x="{hx-42:.0f}" y="254" width="84" height="16" fill="#2f2419"'
               f' opacity=".7"/>'
               f'<rect x="{hx-12:.0f}" y="212" width="24" height="18" rx="6"'
               f' fill="{ZHELEZ}" {o(2)}/></g>')
    s += SL(Z_SRED, kr)
    s += SL(Z_SRED, tusklaya_lampochka(980, 80, t, 1.8, True))
    s += SL(Z_SRED, _polka_s_utvaryu(1380, 700, 460, t, 343, 4))
    s += SL(Z_SRED, f'<rect x="300" y="624" width="900" height="30" rx="10"'
                    f' fill="url(#dosk)" {o(6)}/>'
                    f'<rect x="330" y="654" width="840" height="120" rx="8"'
                    f' fill="#5e4a3a" {o(5)}/>')
    PORTF = ["#3a4452", "#5a3340", "#4a3b2a", "#3d4a3a", "#4e3a50", "#5e3a2a"]
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{356+i*140:.0f}" y="668" width="110" height="92"'
                        f' rx="6" fill="{PORTF[i]}" {o(3)}/>')
    s += SL(Z_SRED, teplo(980, 300, 420, 320, .34))

    # парты рядами
    def parta(px, py, pw, ph2, col="url(#derev)"):
        g = (f'<path d="M{px:.0f},{py-ph2:.0f} L{px+pw:.0f},{py-ph2:.0f}'
             f' L{px+pw:.0f},{py-ph2+34:.0f} L{px:.0f},{py-ph2+46:.0f} Z"'
             f' fill="{col}" {o(5)}/>'
             f'<rect x="{px:.0f}" y="{py-ph2+46:.0f}" width="{pw:.0f}" height="20"'
             f' fill="#3a2a1a" opacity=".8"/>'
             f'<rect x="{px+16:.0f}" y="{py-ph2+66:.0f}" width="30"'
             f' height="{ph2-66:.0f}" rx="8" fill="#4a3522" {o(3)}/>'
             f'<rect x="{px+pw-46:.0f}" y="{py-ph2+66:.0f}" width="30"'
             f' height="{ph2-66:.0f}" rx="8" fill="#4a3522" {o(3)}/>'
             f'<rect x="{px:.0f}" y="{py-ph2*.46:.0f}" width="{pw:.0f}" height="24"'
             f' rx="8" fill="url(#dosk)" {o(4)}/>'
             f'<circle cx="{px+pw-70:.0f}" cy="{py-ph2+22:.0f}" r="18" fill="#2a3a46"'
             f' {o(3)}/>')
        return g
    s += SL(Z_SRED, parta(30, 1012, 490, 236) + parta(600, 1012, 490, 236)
            + parta(1170, 1012, 490, 236))
    s += SL(Z_SRED, parta(1390, 888, 470, 206))
    s += SL(Z_SRED, f'<rect x="1380" y="60" width="440" height="30" rx="10"'
                    f' fill="#5b4428" {o(5)}/>'
                    f'<rect x="1400" y="90" width="400" height="300" rx="8"'
                    f' fill="#cfd8d2" {o(5)}/>'
                    f'<path d="M1430,210 Q1520,160 1620,210 Q1710,260 1780,210"'
                    f' fill="none" stroke="#6f9a5e" stroke-width="14" opacity=".8"/>'
                    f'<path d="M1420,290 Q1540,250 1660,296 Q1740,324 1790,292"'
                    f' fill="none" stroke="#5c87a8" stroke-width="12" opacity=".75"/>')
    s += SL(Z_SRED, _dvorovaya_utvar(560, 840, 460, t, 393, ["korob", "korzina"]))
    s += SL(Z_SRED, f'<rect x="60" y="640" width="300" height="170" rx="10"'
                    f' fill="url(#derev)" {o(5)}/>'
                    f'<rect x="60" y="640" width="300" height="22" rx="7"'
                    f' fill="#5b4428" {o(4)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{84+i*70:.0f}" y="672" width="52" height="118"'
                        f' rx="6" fill="{["#5a3340","#3d4a3a","#4a3b2a","#3a4452"][i]}"'
                        f' {o(3)}/>')
    chrn = ""
    for i, cx_ in enumerate((700, 1270, 1600)):
        chrn += (f'<rect x="{cx_-24:.0f}" y="{(820 if i<2 else 696):.0f}" width="48"'
                 f' height="44" rx="9" fill="#2a3a46" {o(4)}/>'
                 f'<ellipse cx="{cx_:.0f}" cy="{(820 if i<2 else 696):.0f}" rx="24"'
                 f' ry="9" fill="#6a7a88" {o(3)}/>')
    s += SL(Z_SRED, chrn)

    # трое на перемене дерутся портфелями
    dr = ""
    # рост 412-286, базы 918-868, шаги 208-248 и у каждого свой убор: было
    # трое одного роста через ровные 200 px (осмотр 15.11)
    for i, (bx0, bh, col, gl2) in enumerate(((396, 412, "#3a4452", 1.0),
                                             (604, 286, "#2f3a44", .78),
                                             (852, 352, "#4a3346", .92))):
        pr_ = 22 * A.w(t, 1.2, i * .35)
        d = figura(bx0, 918 - (1 - gl2) * 50 - abs(pr_) * .4, bh, t, col=col,
                   kant="#cfe4f5", ph=i * .3, naklon=-14 + 13 * i,
                   shapka=(i == 1), profil=(i != 1), op=.80 + .20 * gl2)
        yb2 = 918 - (1 - gl2) * 50
        rr1, (q1x, q1y), (a1x, a1y) = _ruka(bx0, yb2, bh, 1, bh * .46,
                                            -52 + 34 * A.w(t, 1.2, i * .35), t,
                                            col, "#cfe4f5", i * .2, 9)
        rr2, _, (a2x, a2y) = _ruka(bx0, yb2, bh, -1, bh * .36, 48 - 22 * (i % 2), t,
                                   col, "#cfe4f5", i * .2 + .4, 7)
        d += rr1 + rr2
        d += (f'<g transform="rotate({26*A.w(t,1.2,i*.35):.0f} {q1x:.0f} {q1y:.0f})">'
              f'<rect x="{q1x-52:.0f}" y="{q1y-14:.0f}" width="104" height="80" rx="10"'
              f' fill="{["#4a3522","#5e3a2a","#3a4452"][i]}" {o(5)}/>'
              f'<rect x="{q1x-52:.0f}" y="{q1y+18:.0f}" width="104" height="16"'
              f' fill="#2f2419" opacity=".7"/>'
              f'<rect x="{q1x-16:.0f}" y="{q1y-30:.0f}" width="32" height="20" rx="8"'
              f' fill="{ZHELEZ}" {o(3)}/>'
              f'<rect x="{q1x+16:.0f}" y="{q1y+10:.0f}" width="22" height="18" rx="5"'
              f' fill="{ZHELEZ}" {o(2)}/></g>')
        dr += d + ten(bx0, yb2 + 6, 62 * gl2, 13 * gl2, .4)
    s += SL(Z_SRED, dr)

    # ТИХИЙ ВЫДЕЛЕН МЕСТОМ, ПОЗОЙ И СВЕТОМ (осмотр 15.11: «ученики
    # одинаковые, тихий не выделен»). Он один сидит, пригнувшись к тетради,
    # в профиль, в тёплом пятне своей свечи — а трое дерутся в холодной
    # половине класса.
    ux, uy, uh = 1620, 896, 346
    s += SL(Z_SRED, teplo(ux - 10, uy - 150, 330, 260, .46))
    s += SL(Z_SRED, f'<rect x="{ux+120:.0f}" y="{uy-24:.0f}" width="54" height="24"'
                    f' rx="8" fill="{ZHELEZ}" {o(3)}/>'
            + svecha(ux + 147, uy - 24, t, .4, 1.25))
    u = figura(ux, uy, uh, t, col="#6a4a32", kant="#ffd98a", ph=.6, naklon=14,
               profil=True)
    r1, (sh1x, sh1y), (u1x, u1y) = _ruka_ekr(ux, uy, uh, -1, uh * .40, -72, t, "#3d4a3a",
                                             "#ffd98a", .3, 3)
    r2, (pe_x, pe_y), (u2x, u2y) = _ruka_ekr(ux, uy, uh, 1, uh * .40, 10, t, "#3d4a3a",
                                             "#ffd98a", .7, 4)
    u += r1 + r2
    skr = 7 * A.w(t, 1.6, .2)
    u += (f'<line x1="{pe_x:.0f}" y1="{pe_y:.0f}" x2="{pe_x+34+skr:.0f}"'
          f' y2="{pe_y+56:.0f}" stroke="#e4dcc4" stroke-width="8"'
          f' stroke-linecap="round"/>'
          f'<rect x="{ux-66:.0f}" y="{uy-14:.0f}" width="150" height="20" rx="5"'
          f' fill="#f0ead6" {o(3)}/>'
          f'<path d="M{ux-56:.0f},{uy-6:.0f} Q{ux-20:.0f},{uy-16:.0f}'
          f' {ux+16:.0f},{uy-6:.0f}" fill="none" stroke="#7a8a9a" stroke-width="4"/>'
          f'<circle cx="{ux-18:.0f}" cy="{uy-uh*.80:.0f}" r="20" fill="none"'
          f' stroke="#cfe4f5" stroke-width="5" opacity=".9"/>'
          f'<circle cx="{ux+22:.0f}" cy="{uy-uh*.80:.0f}" r="20" fill="none"'
          f' stroke="#cfe4f5" stroke-width="5" opacity=".9"/>'
          f'<line x1="{ux-2:.0f}" y1="{uy-uh*.80:.0f}" x2="{ux+2:.0f}"'
          f' y2="{uy-uh*.80:.0f}" stroke="#cfe4f5" stroke-width="5"/>')
    s += SL(Z_SRED, u)
    s += SL(Z_SRED, _dvorovaya_utvar(60, 1076, 300, t, 129, ["korob", "korzina"]))
    s += SL(Z_PERED, _stolb_pered(1870, 92, "#140f0b", 0, H))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def pyat_monet_na_podzerkalnike(t):
    """Старое трюмо с тремя зеркалами, перед ним подзеркальник на пол-кадра:
    гребень, флакон, катушка ниток, фарфоровое блюдце. Бабушка на пуфе левой
    придерживает блюдце, правой выкладывает в ряд пять медных монет."""
    rnd = random.Random(119)
    pol = 840
    s = f'<rect width="{W}" height="{H}" fill="#2a2630"/>'
    s += SL(Z_DAL, doski(0, 0, W, pol, 180, True, "dosk"))
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{pol:.0f}" fill="#3b3a46"'
                   f' opacity=".55"/>'
                   f'<rect x="0" y="{pol-150:.0f}" width="{W}" height="26"'
                   f' fill="#2f2c38" opacity=".8"/>')
    s += SL(Z_DAL, polovicy(pol + 30))
    s += SL(Z_DAL, kvartira_veschi(1600, 760, 620, t, 11))

    # синий вечер за окном
    s += SL(Z_DAL, okno_izby(60, 150, 320, 380, t, svet=False, moroz=.0))
    s += SL(Z_DAL, f'<rect x="76" y="166" width="288" height="348" fill="#2b3a52"/>')
    for i in range(10):
        s += SL(Z_DAL, f'<rect x="{96+(i%3)*96:.0f}" y="{220+(i//3)*78:.0f}" width="44"'
                       f' height="40" rx="5" fill="#ffd98a"'
                       f' opacity="{.35+.25*abs(A.w(t,4.0,i*.2)):.2f}"/>')
    s += SL(Z_DAL, zanaveska(60, 140, 220, 150, TKAN, t, 1)
            + zanaveska(380, 140, 220, 150, TKAN, t, -1))

    # трюмо — главный предмет
    s += SL(Z_SRED, _tryumo(620, 700, 900, 600, t, 3))
    s += SL(Z_SRED, lampa(1420, 560, t, 1.5, True))
    s += SL(Z_SRED, teplo(1420, 700, 440, 340, .44))

    # вещи НА подзеркальнике
    pd = 700
    veshi = (f'<path d="M700,{pd-10:.0f} L860,{pd-10:.0f} L860,{pd-34:.0f}'
             f' L700,{pd-34:.0f} Z" fill="#c9b78e" {o(4)}/>')
    for i in range(14):
        veshi += (f'<line x1="{706+i*11:.0f}" y1="{pd-10:.0f}" x2="{706+i*11:.0f}"'
                  f' y2="{pd+22:.0f}" stroke="#c9b78e" stroke-width="5"/>')
    veshi += (f'<path d="M920,{pd-10:.0f} L920,{pd-96:.0f} Q952,{pd-120:.0f}'
              f' {984:.0f},{pd-96:.0f} L984,{pd-10:.0f} Z" fill="#8fb6c4"'
              f' opacity=".85" {o(4)}/>'
              f'<rect x="936" y="{pd-124:.0f}" width="32" height="28" rx="8"'
              f' fill="#d8c69a" {o(3)}/>'
              f'<rect x="1040" y="{pd-76:.0f}" width="86" height="66" rx="10"'
              f' fill="#b4762f" {o(4)}/>'
              f'<ellipse cx="1083" cy="{pd-76:.0f}" rx="43" ry="13" fill="#d09850"'
              f' {o(3)}/>'
              f'<line x1="1083" y1="{pd-76:.0f}" x2="1083" y2="{pd-16:.0f}"'
              f' stroke="#f0e6cc" stroke-width="4" opacity=".8"/>')
    s += SL(Z_SRED, veshi)

    # блюдце и пять монет в ряд
    bx_, by_ = 1300, pd - 14
    s += SL(Z_SRED, f'<path d="M{bx_-104:.0f},{by_-36:.0f} Q{bx_:.0f},{by_+30:.0f}'
                    f' {bx_+104:.0f},{by_-36:.0f} Z" fill="#eae4d6" {o(5)}/>'
                    f'<ellipse cx="{bx_:.0f}" cy="{by_-38:.0f}" rx="104" ry="26"'
                    f' fill="#f6f1e6" {o(3)}/>')
    mon = ""
    for i in range(5):
        vy = A.ease(A.seg(t, .5 + i * .35, .5))
        mx = 700 + i * 150
        my = by_ - 54 - 180 * (1 - vy)
        if vy > .02:
            mon += _moneta_krupno(mx, my, 66, t, i * .2, True, True, .80 * vy)
            nm = A.ease(A.seg(t, .9 + i * .35, .4))
            mon += (f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="{78*nm:.0f}" fill="none"'
                    f' stroke="#ffe9ac" stroke-width="5" opacity="{(1-nm)*.8:.2f}"/>'
                    f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="34" fill="#fff3cf"'
                    f' opacity="{nm*.30:.2f}"/>')
    s += SL(Z_SRED, mon)

    # бабушка на пуфе
    fx, fy, fh = 1620, 1040, 470
    s += SL(Z_SRED, f'<ellipse cx="{fx:.0f}" cy="{fy-60:.0f}" rx="120" ry="44"'
                    f' fill="#5a4a58" {o(5)}/>'
                    f'<rect x="{fx-110:.0f}" y="{fy-62:.0f}" width="220" height="56"'
                    f' rx="16" fill="#4a3c48" {o(4)}/>')
    bab = figura(fx, fy - 56, fh, t, col="#46404e", kant="#ffd98a", platok=True, ph=.3,
                 naklon=-6)
    # Руки лежат на колене и на пуфе. Было: правый рукав под 178° уходил
    # прямой палкой через полкадра влево и кончался в пустоте (осмотр 15.11).
    r1, _, (b1x, b1y) = _ruka(fx, fy - 56, fh, 1, fh * .34, 74, t,
                              "#46404e", "#ffd98a", .2, 5)
    r2, _, (b2x, b2y) = _ruka(fx, fy - 56, fh, -1, fh * .30, 82, t,
                              "#46404e", "#ffd98a", .6, 4)
    s += SL(Z_SRED, bab + r1 + r2)
    s += SL(Z_SRED, _kot_zhivoy(300, 1060, t, 1.6, "#4a423c", .3, True, True))
    s += SL(Z_SRED, mebel_hlam(120, 940, 380, t, 29))
    s += SL(Z_SRED, _lavka_krupno(520, 1070, 520, t, 190, True))
    s += SL(Z_SRED, kvartira_veschi(520, 380, 420, t, 31))
    s += SL(Z_SRED, f'<path d="M560,1010 L1500,1010 L1620,1076 L440,1076 Z"'
                    f' fill="#5a3f46" {o(5)}/>'
                    f'<path d="M580,1032 L1512,1032 M566,1056 L1560,1056"'
                    f' stroke="#8a6a3c" stroke-width="8" opacity=".55"/>')
    s += SL(Z_PERED, _stolb_pered(1884, 90, "#140f0b", 0, H))
    s += ramka_pp("oba")
    s += vinetka(.46)
    return s


def ruka_nad_monetoy(t):
    """Булыжная мостовая крупно: в щели между камнями ЛЕЖИТ ПЛАШМЯ крупная
    серебряная монета — профиль-чеканка, гурт насечкой, блик дугой, тень под
    ребром. Рядом жёлтый лист, оброненная пуговица, травинка. Сверху входит
    рука до локтя в рукаве пальто, зависает, сжимается в кулак и уходит."""
    rnd = random.Random(120)
    s = f'<rect width="{W}" height="{H}" fill="#2e2f33"/>'
    s += SL(Z_DAL, _bulyzhnik(60, 440, 13, 90, "#4a4740"))
    s += SL(Z_SRED, _bulyzhnik(400, 1080, 17, 150, "#5a5248"))
    s += SL(Z_SRED, _bulyzhnik(620, 1080, 19, 90, "#625a4e"))
    s += SL(Z_SRED, f'<rect x="0" y="40" width="{W}" height="80" fill="#3a3b40"'
                    f' opacity=".7"/>')
    s += SL(Z_DAL, tuman(t, 160, .30, "#aab4bc"))
    # ВЕРХ КАДРА — НЕ ПУСТОЙ СЕРЫЙ (осмотр 15.11). Та же мостовая дальше:
    # чугунная крышка люка, водосточный жёлоб, лужа с отражением, сгребённые
    # листья, ящик у бордюра, голубь. Вещи, а не полупрозрачные пятна.
    lyuk = (f'<ellipse cx="286" cy="176" rx="196" ry="112" fill="#2a2d31" {o(6)}/>'
            f'<ellipse cx="286" cy="166" rx="176" ry="98" fill="#4a4d52" {o(5)}/>'
            f'<ellipse cx="286" cy="166" rx="146" ry="80" fill="none" stroke="#2f3237"'
            f' stroke-width="9"/>')
    for i in range(8):
        a_ = math.radians(i * 45)
        lyuk += (f'<line x1="{286+36*math.cos(a_):.0f}" y1="{166+20*math.sin(a_):.0f}"'
                 f' x2="{286+142*math.cos(a_):.0f}" y2="{166+78*math.sin(a_):.0f}"'
                 f' stroke="#2f3237" stroke-width="11"/>')
    for i in range(6):
        lyuk += (f'<ellipse cx="{196+i*36:.0f}" cy="{150+(i%2)*26:.0f}" rx="13"'
                 f' ry="8" fill="#6a6f75" opacity=".7"/>')
    lyuk += (f'<ellipse cx="286" cy="166" rx="34" ry="19" fill="#23262a" {o(3)}/>'
             f'<path d="M240,120 Q286,96 332,120" fill="none" stroke="#7d848b"'
             f' stroke-width="7" opacity=".55"/>')
    s += SL(Z_SRED, lyuk)
    zhel = (f'<path d="M0,268 L{W},242 L{W},288 L0,314 Z" fill="#3a3d42" {o(4)}/>'
            f'<path d="M0,282 L{W},256" stroke="#22262a" stroke-width="12"'
            f' opacity=".85"/>')
    for i in range(14):
        zhel += (f'<rect x="{40+i*136:.0f}" y="{262-i*2:.0f}" width="54" height="16"'
                 f' rx="6" fill="#20242a" {o(2)}/>')
    s += SL(Z_SRED, zhel)
    s += SL(Z_SRED, _luzha(1420, 150, 240, t, .4, 92, "#8ea6bb"))
    s += SL(Z_SRED, _kucha_listev(830, 230, 330, 163, 118))
    s += SL(Z_SRED, _yaschiki(1700, 230, t, 167, 1, .92))
    s += SL(Z_SRED, f'<g transform="rotate(-18 620 206)">'
                    f'<path d="M556,206 Q556,142 596,136 Q604,100 640,118'
                    f' Q676,102 680,142 Q716,152 702,198 Q660,230 606,228 Z"'
                    f' fill="#4e3a44" {o(5)}/>'
                    f'<path d="M578,212 Q624,196 690,206" fill="none" stroke="#2f2029"'
                    f' stroke-width="7" opacity=".8"/></g>')
    s += SL(Z_SRED, ptica(1180, 330, t, 1.7, "#6a717a", .3, "#4a5058"))
    # бордюрный камень и решётка стока
    s += SL(Z_SRED, f'<rect x="0" y="300" width="{W}" height="56" rx="8"'
                    f' fill="#7a7c80" {o(5)}/>'
                    f'<rect x="0" y="356" width="{W}" height="30" fill="#5a5c60"'
                    f' opacity=".9"/>')
    resh = f'<rect x="1500" y="420" width="330" height="150" rx="10" fill="#3a3d42" {o(5)}/>'
    for i in range(7):
        resh += (f'<rect x="{1516+i*44:.0f}" y="432" width="26" height="126" rx="5"'
                 f' fill="#22262a" {o(2)}/>')
    s += SL(Z_SRED, resh)
    # крупные камни переднего плана
    for i, (gx_, gy_, gr) in enumerate(((180, 700, 130), (1600, 840, 150),
                                        (1180, 1040, 170), (300, 1020, 120))):
        s += SL(Z_SRED, f'<ellipse cx="{gx_:.0f}" cy="{gy_:.0f}" rx="{gr:.0f}"'
                        f' ry="{gr*.66:.0f}" fill="#5e5a52" {o(5)}/>'
                        f'<ellipse cx="{gx_-gr*.24:.0f}" cy="{gy_-gr*.20:.0f}"'
                        f' rx="{gr*.52:.0f}" ry="{gr*.30:.0f}" fill="#726d62"'
                        f' opacity=".6"/>')
    s += SL(Z_SRED, f'<ellipse cx="460" cy="1046" rx="330" ry="54" fill="#6d7f8c"'
                    f' opacity=".45"/>'
                    f'<path d="M250,1036 L680,1030" stroke="#c6dcea" stroke-width="6"'
                    f' opacity=".55"/>')

    # щель между камнями, в которой лежит монета
    mx, my = 860, 720
    s += SL(Z_SRED, f'<path d="M{mx-620:.0f},{my+56:.0f} Q{mx:.0f},{my-54:.0f}'
                    f' {mx+620:.0f},{my+86:.0f} L{mx+620:.0f},{my+150:.0f}'
                    f' Q{mx:.0f},{my+20:.0f} {mx-620:.0f},{my+120:.0f} Z"'
                    f' fill="#26262a" opacity=".85"/>')
    # МОНЕТА ЛЕЖИТ ПЛАШМЯ И КРУПНО
    s += SL(Z_SRED, _moneta_krupno(mx, my, 268, t, .1, False, True, .56))
    s += SL(Z_SRED, teplo(mx, my, 360, 260, .32))

    # жёлтый лист, пуговица, травинка
    lk = 5 * A.w(t, 1.9, .2)
    s += SL(Z_SRED, f'<g transform="rotate({lk:.1f} 340 1004)">'
                    f'<path d="M190,1004 Q340,890 490,1004 Q340,1090 190,1004 Z"'
                    f' fill="#c08a3a" {o(4)}/>'
                    f'<line x1="190" y1="1004" x2="490" y2="1004" stroke="#7a5420"'
                    f' stroke-width="6"/>'
                    f'<path d="M264,978 L304,1004 M340,966 L350,1004'
                    f' M416,978 L386,1004" stroke="#7a5420" stroke-width="4"'
                    f' opacity=".8"/></g>')
    s += SL(Z_SRED, f'<ellipse cx="1430" cy="980" rx="74" ry="30" fill="#e8e2d2" {o(5)}/>'
                    f'<ellipse cx="1430" cy="980" rx="30" ry="12" fill="none"'
                    f' stroke="#b9ae95" stroke-width="6"/>'
                    f'<circle cx="1412" cy="976" r="7" fill="#fff8e8" opacity=".9"/>'
                    f'<circle cx="1448" cy="976" r="7" fill="#fff8e8" opacity=".9"/>')
    s += SL(Z_SRED, _podorozhnik(1620, 1040, 1.8, t, .3, 5)
            + _trava(rnd, 10, 840, 1060, "#6f7a44"))
    s += SL(Z_SRED, _listya(161, 30, 480, 1060))
    s += SL(Z_SRED, svecha(1800, 760, t, .2, 1.6))
    s += SL(Z_SRED, _gorodskoy_hlam(1060, 1076, 460, t, 205, ["korobka", "yaschik"]))

    # рука до локтя в рукаве пальто: опускается, зависает, сжимается, уходит
    op_ = A.ease(A.seg(t, .2, 1.2))
    zh = A.ease(A.seg(t, 1.9, .6))
    uh = A.ease(A.seg(t, 2.8, .8))
    ky_ = -400 + 640 * op_ - 700 * uh
    ruk, (kx2, ky2) = rukav(mx + 310, ky_, 380, 112, t, "#2f3542", "#cfe4f5", .1, 3, True)
    kul = (f'<ellipse cx="{kx2:.0f}" cy="{ky2:.0f}" rx="{84-18*zh:.0f}"'
           f' ry="{74-12*zh:.0f}" fill="#2f3542" {o(6)}/>'
           f'<rect x="{mx+248:.0f}" y="{ky_-32:.0f}" width="132" height="58" rx="17"'
           f' fill="#232835" {o(5)}/>'
           f'<path d="M{kx2-52:.0f},{ky2-26+14*zh:.0f} Q{kx2:.0f},{ky2-48+20*zh:.0f}'
           f' {kx2+52:.0f},{ky2-26+14*zh:.0f}" fill="none" stroke="#1a1e28"'
           f' stroke-width="7" opacity=".8"/>'
           f'<ellipse cx="{kx2:.0f}" cy="{my+120:.0f}" rx="{110-20*zh:.0f}" ry="26"'
           f' fill="#1a1a1e" opacity="{.30*op_*(1-uh):.2f}"/>')
    s += SL(Z_PERED, ruk + kul)
    s += SL(Z_LETIT, mokryy_sneg(t, 14, 19, .4, .7))
    s += ramka_pp("oba")
    s += vinetka(.48)
    return s


def nadezhda_v_monete(t):
    """Монета во весь кадр: в её блестящем кружке, как в окошке, виден тёплый
    вид — изба с огоньком в окне, крыльцо, дымок над трубой, рябина. Девушка
    стоит СНАРУЖИ монеты и смотрит в неё. Сверху тянется та же рука и
    отдёргивается, по ободку бежит блик."""
    rnd = random.Random(121)
    s = f'<rect width="{W}" height="{H}" fill="#2a2a2e"/>'
    s += SL(Z_DAL, _bulyzhnik(500, 1080, 23, 90, "#4a4740"))
    s += SL(Z_DAL, tuman(t, 240, .26, "#aab4bc"))

    cx, cy, r = 760, 520, 496
    s += SL(Z_SRED, ten(cx, cy + r * .98, r * 1.04, r * .2, .5))
    s += SL(Z_SRED, f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#med)"'
                    f' {o(9)}/>'
                    f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.90:.0f}" fill="none"'
                    f' stroke="#8a5a22" stroke-width="12" opacity=".85"/>')
    gurt = ""
    for i in range(44):
        a = math.radians(i * 360 / 44.0)
        gurt += (f'<line x1="{cx+r*.91*math.cos(a):.0f}" y1="{cy+r*.91*math.sin(a):.0f}"'
                 f' x2="{cx+r*1.0*math.cos(a):.0f}" y2="{cy+r*1.0*math.sin(a):.0f}"'
                 f' stroke="#7a4d1c" stroke-width="7" opacity=".8"/>')
    for i in range(22):
        a = math.radians(i * 360 / 22.0 + 8)
        gurt += (f'<circle cx="{cx+r*.82*math.cos(a):.0f}" cy="{cy+r*.82*math.sin(a):.0f}"'
                 f' r="11" fill="#8a5a22" opacity=".85"/>')
    s += SL(Z_SRED, gurt)

    # ── в кружке монеты ТЁПЛЫЙ ВИД: изба с огоньком, крыльцо, дымок
    rr = r * .74
    vid = (f'<clipPath id="monok"><circle cx="{cx:.0f}" cy="{cy:.0f}"'
           f' r="{rr:.0f}"/></clipPath><g clip-path="url(#monok)">'
           f'<rect x="{cx-rr:.0f}" y="{cy-rr:.0f}" width="{rr*2:.0f}"'
           f' height="{rr*2:.0f}" fill="#d8a85c"/>'
           f'<rect x="{cx-rr:.0f}" y="{cy-rr:.0f}" width="{rr*2:.0f}"'
           f' height="{rr:.0f}" fill="#e6c488"/>'
           f'<rect x="{cx-rr:.0f}" y="{cy+rr*.42:.0f}" width="{rr*2:.0f}"'
           f' height="{rr:.0f}" fill="#a87a38"/>')
    # сруб избы
    ix, ib, iw = cx + rr * .14, cy + rr * .46, rr * 1.22
    for i in range(6):
        vid += (f'<rect x="{ix-iw/2:.0f}" y="{ib-28-i*30:.0f}" width="{iw:.0f}"'
                f' height="27" rx="9" fill="{["#b5813c","#a3722f"][i%2]}" {o(4)}/>')
    vid += (f'<path d="M{ix-iw*.62:.0f},{ib-180:.0f} L{ix:.0f},{ib-268:.0f}'
            f' L{ix+iw*.62:.0f},{ib-180:.0f} Z" fill="#8a5a22" {o(5)}/>'
            f'<rect x="{ix-iw*.66:.0f}" y="{ib-188:.0f}" width="{iw*1.32:.0f}"'
            f' height="18" rx="7" fill="#94651f" {o(4)}/>')
    # огонёк в окне
    og = .65 + .35 * abs(A.w(t, 2.0, .1))
    vid += (f'<rect x="{ix-44:.0f}" y="{ib-140:.0f}" width="88" height="80" rx="8"'
            f' fill="#6b4420" {o(4)}/>'
            f'<rect x="{ix-34:.0f}" y="{ib-130:.0f}" width="68" height="60" rx="5"'
            f' fill="#fff0bd" opacity="{og:.2f}"/>'
            f'<line x1="{ix:.0f}" y1="{ib-130:.0f}" x2="{ix:.0f}" y2="{ib-70:.0f}"'
            f' stroke="#6b4420" stroke-width="7"/>'
            f'<line x1="{ix-34:.0f}" y1="{ib-100:.0f}" x2="{ix+34:.0f}"'
            f' y2="{ib-100:.0f}" stroke="#6b4420" stroke-width="7"/>'
            f'<circle cx="{ix:.0f}" cy="{ib-100:.0f}" r="{74*og:.0f}" fill="#fff0bd"'
            f' opacity=".30"/>')
    # крыльцо
    vid += (f'<rect x="{ix-iw*.72:.0f}" y="{ib-54:.0f}" width="{iw*.46:.0f}"'
            f' height="20" rx="7" fill="#8a5a22" {o(4)}/>'
            f'<rect x="{ix-iw*.68:.0f}" y="{ib-34:.0f}" width="{iw*.38:.0f}"'
            f' height="18" rx="6" fill="#94651f" {o(3)}/>'
            f'<rect x="{ix-iw*.72:.0f}" y="{ib-120:.0f}" width="16" height="70"'
            f' rx="6" fill="#7a4d1c" {o(3)}/>'
            f'<rect x="{ix-iw*.32:.0f}" y="{ib-120:.0f}" width="16" height="70"'
            f' rx="6" fill="#7a4d1c" {o(3)}/>')
    # труба и дымок
    vid += (f'<rect x="{ix+iw*.26:.0f}" y="{ib-286:.0f}" width="36" height="60" rx="6"'
            f' fill="#94651f" {o(4)}/>')
    for i in range(4):
        p = ((t * .22 + i * .25) % 1.0)
        vid += (f'<ellipse cx="{ix+iw*.30+26*math.sin(p*5+i):.0f}"'
                f' cy="{ib-300-p*170:.0f}" rx="{20+p*34:.0f}" ry="{15+p*26:.0f}"'
                f' fill="#f0e0bc" opacity="{(1-p)*.5:.2f}"/>')
    # рябина у крыльца
    vid += (f'<line x1="{cx-rr*.64:.0f}" y1="{ib:.0f}" x2="{cx-rr*.60:.0f}"'
            f' y2="{ib-140:.0f}" stroke="#7a4d1c" stroke-width="12"/>')
    for i in range(9):
        a = math.radians(i * 40 + 10 * A.w(t, 3.0, i * .2))
        vid += (f'<circle cx="{cx-rr*.60+40*math.cos(a):.0f}"'
                f' cy="{ib-150+30*math.sin(a):.0f}" r="10" fill="#c8402c"'
                f' opacity=".95"/>')
    # тёплое пятно от окна на земле
    vid += (f'<ellipse cx="{ix:.0f}" cy="{ib+30:.0f}" rx="{rr*.72:.0f}"'
            f' ry="{rr*.18:.0f}" fill="#ffe9ac" opacity=".38"/>')
    vid += "</g>"
    s += SL(Z_SRED, vid)
    s += SL(Z_SRED, f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="none"'
                    f' stroke="#8a5a22" stroke-width="12" opacity=".9"/>')

    # блик бежит по ободку
    bp = (t * .35) % 1.0
    ba = bp * 6.283
    s += SL(Z_SRED, f'<path d="M{cx+r*.95*math.cos(ba-.5):.0f},'
                    f'{cy+r*.95*math.sin(ba-.5):.0f} A{r*.95:.0f},{r*.95:.0f} 0 0 1'
                    f' {cx+r*.95*math.cos(ba+.5):.0f},{cy+r*.95*math.sin(ba+.5):.0f}"'
                    f' fill="none" stroke="#fff3cf" stroke-width="26" opacity=".55"/>')
    s += SL(Z_SRED, teplo(cx, cy, 540, 480, .32))

    # девушка СНАРУЖИ монеты: стоит на мостовой и смотрит в кружок
    isp = A.ease(A.seg(t, 1.1, .5)) * (1 - A.ease(A.seg(t, 2.4, .6)))
    fx, fy, fh = 1560, 1030, 600
    dev = figura(fx, fy, fh, t, col="#4a3f52", kant="#ffd98a", platok=True, ph=.3,
                 naklon=-7 + 5 * isp)
    rr1, (c1x, c1y), (d1x, d1y) = _ruka_ekr(fx, fy, fh, 1, fh * .34, -150 + 24 * isp, t,
                                            "#4a3f52", "#ffd98a", .2, 4)
    rr2, (c2x, c2y), (d2x, d2y) = _ruka_ekr(fx, fy, fh, -1, fh * .34, -116 - 24 * isp, t,
                                            "#4a3f52", "#ffd98a", .6, 4)
    dev += rr1 + rr2
    # ладони сложены у груди, при испуге поднимаются к лицу
    for (hx_, hy_) in ((c1x, c1y), (c2x, c2y)):
        dev += (f'<ellipse cx="{hx_:.0f}" cy="{hy_-40*isp:.0f}" rx="34" ry="46"'
                f' fill="#4a3f52" {o(5)}/>')
    dev += para_izo_rta(fx - 48, fy - fh * .80, t, .2, 1.1, .5)
    s += SL(Z_SRED, dev + ten(fx, fy + 8, 120, 22, .5))

    # рука тянется к монете и отдёргивается
    tyn = A.ease(A.seg(t, .6, .9)) * (1 - A.ease(A.seg(t, 2.2, .7)))
    ruk, (kx2, ky2) = rukav(cx - 300, -340 + 500 * tyn, 420, 72, t, "#2f3542",
                            "#cfe4f5", .1, 3, True)
    s += SL(Z_PERED, ruk + f'<ellipse cx="{kx2:.0f}" cy="{ky2:.0f}" rx="82" ry="72"'
                           f' fill="#2f3542" {o(6)}/>'
                           f'<rect x="{cx-366:.0f}" y="{-370+500*tyn:.0f}" width="132"'
                           f' height="58" rx="17" fill="#232835" {o(5)}/>')
    s += SL(Z_SRED, _listya(167, 30, 620, 1060))
    s += SL(Z_SRED, _gorodskoy_hlam(40, 1056, 420, t, 187, ["stolbik", "yaschik"]))
    s += SL(Z_SRED, _gorodskoy_hlam(1760, 1070, 200, t, 189, ["korobka"]))
    for i, (gx_, gy_, gr) in enumerate(((240, 900, 120), (1320, 980, 140))):
        s += SL(Z_SRED, f'<ellipse cx="{gx_:.0f}" cy="{gy_:.0f}" rx="{gr:.0f}"'
                        f' ry="{gr*.66:.0f}" fill="#5e5a52" {o(5)}/>')
    s += SL(Z_SRED, _podorozhnik(300, 1040, 1.8, t, .4, 5)
            + _podorozhnik(1180, 1060, 1.6, t, .9, 5))
    s += SL(Z_SRED, svecha(120, 760, t, .3, 1.5))
    s += SL(Z_SRED, lampa(180, 300, t, 1.3, True) + teplo(180, 420, 240, 200, .36))
    s += SL(Z_LETIT, mokryy_sneg(t, 12, 21, .35, .65))
    s += ramka_pp("oba")
    s += vinetka(.48)
    return s


def nogi_pereshagivayut_nahodku(t):
    """Деревянные мостки, на доске лежит монета. КРУПНО — одна пара ног в
    валенках с подошвой, опора на доски настила: нога поднимается выше и
    перешагивает находку. Двое других идут следом в глубине кадра, видны
    целиком и мелко. Под мостками лужа со льдом, лопух, воробей."""
    rnd = random.Random(122)
    POL = 880
    s = f'<rect width="{W}" height="{H}" fill="#39342c"/>'
    s += SL(Z_DAL, f'<rect x="0" y="{POL+60:.0f}" width="{W}" height="{H-POL-60}"'
                   f' fill="#3b352c"/>'
                   f'<ellipse cx="620" cy="1020" rx="420" ry="60" fill="#6d7f8c"'
                   f' opacity=".55"/>'
                   f'<ellipse cx="620" cy="1008" rx="310" ry="38" fill="#c6dcea"'
                   f' opacity=".45"/>'
                   f'<path d="M380,1010 L860,998 M450,1034 L800,1024" stroke="#e4f1fa"'
                   f' stroke-width="5" opacity=".6"/>')
    s += SL(Z_DAL, _podorozhnik(1360, 1060, 2.6, t, .2, 6)
            + _podorozhnik(180, 1056, 2.0, t, .7, 5))
    vp = (t * .5) % 1.0
    s += SL(Z_DAL, ptica(1180 - 320 * vp, POL - 40 - 200 * max(.0, vp - .62) * 2.6, t,
                         1.5, "#7d6a52", .2))

    # дальний план: улица, заборы, дым, перила мостков
    s += SL(Z_DAL, _zabor_dosok(-20, POL - 560, 820, 300, 177, 56)
            + _zabor_dosok(1180, POL - 556, 780, 296, 179, 58))
    s += SL(Z_DAL, teplo(300, POL - 420, 260, 210, .34))
    s += SL(Z_DAL, dym(300, POL - 560, t, 5, .26, 280, .34, "#d3dae2", .9))
    s += SL(Z_DAL, goloe_derevo(1180, POL - 540, 620, t, 325, 10, "#2a2b33", True)
            + goloe_derevo(560, POL - 548, 520, t, 357, 9, "#2a2b33", True))
    s += SL(Z_DAL, _derevnya_ryad(POL - 560, t, 359, ((640, 380), (1240, 340))))
    sta2 = ""
    for i in range(7):
        bx_ = 460 + i * 160 + 26 * math.sin(t * .5 + i)
        sta2 += ptica(bx_, 214 + (i % 3) * 44, t, .9, "#4a4a52", i * .2)
    s += SL(Z_DAL, sta2)
    per = (f'<rect x="150" y="{POL-470:.0f}" width="1480" height="28" rx="10"'
           f' fill="url(#derev)" {o(6)}/>'
           f'<rect x="150" y="{POL-392:.0f}" width="1480" height="22" rx="9"'
           f' fill="#5b4428" {o(5)}/>')
    for i in range(8):
        px = 40 + i * 260
        per += (f'<rect x="{px:.0f}" y="{POL-478:.0f}" width="32" height="300" rx="9"'
                f' fill="#4a3522" {o(4)}/>')
    s += SL(Z_DAL, per)
    s += SL(Z_DAL, tuman(t, POL - 330, .26, "#aab4bc"))

    # двое других — целиком, мелко, в глубине
    sh = (t * .55) % 1.0
    glub = ""
    for i, (gx_, gh, col, pl, ph_) in enumerate(((1310, 290, "#3a3a44", False, .2),
                                                 (1470, 250, "#4a4a56", True, .6))):
        pryg = 10 * abs(math.sin((sh + i * .4) * 6.283))
        g = figura(gx_, POL - 12 - pryg * .3, gh, t, col=col, kant="#cfe4f5",
                   platok=pl, ph=ph_, shapka=not pl)
        rr1, (q1x, q1y), (a1x, a1y) = _ruka_ekr(gx_, POL - 12, gh, 1, gh * .40, 72, t, col,
                                                "#cfe4f5", ph_, 5)
        rr2, _, (a2x, a2y) = _ruka_ekr(gx_, POL - 12, gh, -1, gh * .38, 104, t, col, "#cfe4f5",
                                       ph_ + .3, 5)
        g += rr1 + rr2
        if i == 0:
            g += (f'<path d="M{q1x-46:.0f},{q1y:.0f} L{q1x+46:.0f},{q1y:.0f}'
                  f' L{q1x+34:.0f},{q1y+76:.0f} L{q1x-34:.0f},{q1y+76:.0f} Z"'
                  f' fill="url(#solom)" {o(4)}/>'
                  f'<path d="M{q1x-38:.0f},{q1y:.0f} Q{q1x:.0f},{q1y-50:.0f}'
                  f' {q1x+38:.0f},{q1y:.0f}" fill="none" stroke="#8a6a3c"'
                  f' stroke-width="7"/>')
        else:
            g += (f'<path d="M{q1x-30:.0f},{q1y:.0f} Q{q1x-44:.0f},{q1y+44:.0f}'
                  f' {q1x-30:.0f},{q1y+86:.0f} L{q1x+30:.0f},{q1y+86:.0f}'
                  f' Q{q1x+44:.0f},{q1y+44:.0f} {q1x+30:.0f},{q1y:.0f} Z"'
                  f' fill="url(#glina)" {o(4)}/>')
        glub += g + ten(gx_, POL + 4, 54, 12, .4)
    s += SL(Z_DAL, glub)

    # настил мостков
    nast = ""
    for i in range(6):
        dy = POL - 10 + i * 36
        nast += (f'<rect x="-30" y="{dy:.0f}" width="{W+60}" height="32" rx="6"'
                 f' fill="url(#dosk)" {o(4)}/>'
                 f'<line x1="-30" y1="{dy+32:.0f}" x2="{W+30}" y2="{dy+32:.0f}"'
                 f' stroke="#2f2419" stroke-width="5" opacity=".7"/>')
    for i in range(9):
        gx = 90 + i * 220
        nast += (f'<circle cx="{gx:.0f}" cy="{POL+6:.0f}" r="9" fill="#5e5146" {o(2)}/>'
                 f'<circle cx="{gx+110:.0f}" cy="{POL+78:.0f}" r="9" fill="#5e5146"'
                 f' {o(2)}/>')
    s += SL(Z_SRED, nast)
    s += SL(Z_SRED, _listya(169, 26, POL - 20, POL + 160))
    s += SL(Z_SRED, _inej(171, 30, POL - 10, POL + 160))

    # монета лежит на доске
    s += SL(Z_SRED, _moneta_krupno(1000, POL + 70, 96, t, .2, True, True, .86))
    s += SL(Z_SRED, teplo(1000, POL + 70, 300, 210, .30))

    # ── КРУПНО одна пара ног в валенках, опора на доски настила
    shag = sh
    bedr = 330
    col = "#5a3f46"
    nx = 620
    kr = ""
    for k, sgn in ((0, -1), (1, 1)):
        lift = max(.0, math.sin((shag + k * .5) * math.pi)) * 230
        bx2 = nx + sgn * 96
        fy2 = POL + 96 - lift
        # штанина/чулок
        kr += (f'<path d="M{bx2-38:.0f},{bedr:.0f} L{bx2+38:.0f},{bedr:.0f}'
               f' L{bx2+34:.0f},{fy2-150:.0f} L{bx2-34:.0f},{fy2-150:.0f} Z"'
               f' fill="#6e6252" {o(6)}/>')
        # валенок: голенище, след, подошва, строчка
        kr += (f'<path d="M{bx2-42:.0f},{fy2-262:.0f} L{bx2+42:.0f},{fy2-262:.0f}'
               f' L{bx2+52:.0f},{fy2-30:.0f} L{bx2-52:.0f},{fy2-30:.0f} Z"'
               f' fill="#9a8c70" {o(7)}/>'
               f'<path d="M{bx2-74:.0f},{fy2-30:.0f} Q{bx2+30:.0f},{fy2-10:.0f}'
               f' {bx2+128:.0f},{fy2-40:.0f} L{bx2+134:.0f},{fy2+16:.0f}'
               f' Q{bx2+20:.0f},{fy2+46:.0f} {bx2-78:.0f},{fy2+22:.0f} Z"'
               f' fill="#8b7d62" {o(7)}/>'
               f'<path d="M{bx2-78:.0f},{fy2+22:.0f} Q{bx2+20:.0f},{fy2+46:.0f}'
               f' {bx2+134:.0f},{fy2+16:.0f} L{bx2+136:.0f},{fy2+44:.0f}'
               f' Q{bx2+20:.0f},{fy2+76:.0f} {bx2-80:.0f},{fy2+50:.0f} Z"'
               f' fill="#4a4036" {o(6)}/>')
        for q in range(5):                                   # подошва-рифление
            kr += (f'<line x1="{bx2-56+q*44:.0f}" y1="{fy2+34+q*2:.0f}"'
                   f' x2="{bx2-50+q*44:.0f}" y2="{fy2+60+q*2:.0f}" stroke="#2e2820"'
                   f' stroke-width="6" opacity=".8"/>')
        kr += (f'<path d="M{bx2-60:.0f},{fy2-206:.0f} L{bx2+60:.0f},{fy2-206:.0f}"'
               f' stroke="#857757" stroke-width="7"/>'
               f'<path d="M{bx2-66:.0f},{fy2-96:.0f} Q{bx2:.0f},{fy2-76:.0f}'
               f' {bx2+70:.0f},{fy2-100:.0f}" fill="none" stroke="#857757"'
               f' stroke-width="6"/>')
        kr += ten(bx2 + 24, POL + 122, 86, 18, .40 * (1 - lift / 300.0))
    # подол и пояс крупно
    kr += (f'<path d="M{nx-104:.0f},-80 L{nx+104:.0f},-80'
           f' L{nx+174:.0f},{bedr+62:.0f} L{nx-174:.0f},{bedr+62:.0f} Z"'
           f' fill="{col}" {o(8)}/>'
           f'<path d="M{nx-174:.0f},{bedr+62:.0f} Q{nx-60:.0f},{bedr+118:.0f}'
           f' {nx+6:.0f},{bedr+74:.0f} Q{nx+80:.0f},{bedr+120:.0f}'
           f' {nx+174:.0f},{bedr+62:.0f}" fill="none" stroke="#2a1820"'
           f' stroke-width="10" opacity=".6"/>'
           f'<path d="M{nx+4:.0f},-80 L{nx+10:.0f},{bedr+72:.0f}" stroke="#2a1820"'
           f' stroke-width="9" opacity=".45"/>')
    for k in range(6):
        kr += (f'<line x1="{nx-86+k*36:.0f}" y1="-60"'
               f' x2="{nx-140+k*58:.0f}" y2="{bedr+54:.0f}" stroke="#2a1820"'
               f' stroke-width="6" opacity=".28"/>')
    s += SL(Z_SRED, kr)

    s += SL(Z_SRED, _dvorovaya_utvar(1180, POL + 180, 560, t, 181,
                                     ["korzina", "vedro", "korob"]))
    s += SL(Z_SRED, _polka_s_utvaryu(600, POL - 420, 420, t, 183, 3))
    s += SL(Z_SRED, _dvorovaya_utvar(760, POL - 380, 420, t, 323, ["kadka", "meshok"]))
    s += SL(Z_SRED, svecha(1840, POL - 420, t, .2, 1.4))
    s += SL(Z_PERED, _stolb_pered(-8, 86, "#1d1611", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 23, .4, .7))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def moneta_kupyura_i_perchatka_na_asfa(t):
    """Городской тротуар у бордюра, осенние листья. В ряд лежат монета,
    сложенная купюра и вязаная перчатка. Рядом урна, скамейка, колесо
    коляски. Женщина в пальто и берете проходит мимо, не сбавляя шага."""
    rnd = random.Random(123)
    s = f'<rect width="{W}" height="{H}" fill="#2d3038"/>'
    s += SL(Z_DAL, panelka(300, 470, 620, t, 5, True, 7)
            + panelka(1500, 450, 560, t, 5, True, 9))
    s += SL(Z_DAL, goloe_derevo(470, 482, 700, t, 13, 11, "#2a2b33", False)
            + goloe_derevo(1520, 476, 560, t, 361, 9, "#2a2b33", False))
    s += SL(Z_DAL, panelka(960, 470, 540, t, 6, True, 363))
    s += SL(Z_DAL, tusklaya_lampochka(300, 160, t, 2.0, False))
    s += SL(Z_DAL, teplo(300, 280, 260, 210, .36))
    s += SL(Z_SRED, _asfalt(470, 1080, 29, 34))
    s += SL(Z_SRED, f'<rect x="170" y="462" width="1440" height="46" rx="8"'
                    f' fill="#7a7c80" {o(5)}/>'
                    f'<rect x="0" y="508" width="{W}" height="26" fill="#5a5c60"'
                    f' opacity=".9"/>')

    # урна, скамейка, колесо коляски
    # урна ушла в правый край, скамейка стала МЕНЬШЕ и дальше, коляскино
    # колесо поднялось: находки были мельче скамейки и в кадре читались
    # мусором под ногами (осмотр 15.11)
    s += SL(Z_SRED, f'<path d="M1636,906 L1796,906 L1774,1060 L1658,1060 Z"'
                    f' fill="#4a5055" {o(6)}/>'
                    f'<rect x="1622" y="888" width="188" height="26" rx="10"'
                    f' fill="#5e656a" {o(4)}/>'
                    f'<rect x="1700" y="1060" width="22" height="20" fill="#3a4045"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<line x1="{1656+i*38:.0f}" y1="916" x2="{1666+i*36:.0f}"'
                        f' y2="1054" stroke="#333a3e" stroke-width="5" opacity=".7"/>')
    skam = (f'<rect x="1150" y="712" width="700" height="28" rx="11" fill="url(#dosk)"'
            f' {o(6)}/>'
            f'<rect x="1150" y="636" width="700" height="24" rx="10" fill="url(#dosk)"'
            f' {o(6)}/>'
            f'<rect x="1150" y="674" width="700" height="24" rx="10" fill="url(#dosk)"'
            f' {o(6)}/>')
    for px in (1196, 1784):
        skam += (f'<rect x="{px:.0f}" y="736" width="22" height="124" rx="8"'
                 f' fill="#4a5055" {o(4)}/>'
                 f'<rect x="{px-22:.0f}" y="616" width="22" height="132" rx="8"'
                 f' fill="#4a5055" {o(4)}/>')
    s += SL(Z_SRED, skam)
    ka = 10 * A.w(t, 4.6, .2)
    kolo = f'<g transform="rotate({ka:.1f} 1016 718)"><circle cx="1016" cy="718" r="72"' \
           f' fill="none" stroke="#3a4045" stroke-width="17"/>' \
           f'<circle cx="1016" cy="718" r="19" fill="#5e656a" {o(3)}/>'
    for i in range(10):
        a = math.radians(i * 36)
        kolo += (f'<line x1="{1016+19*math.cos(a):.0f}" y1="{718+19*math.sin(a):.0f}"'
                 f' x2="{1016+64*math.cos(a):.0f}" y2="{718+64*math.sin(a):.0f}"'
                 f' stroke="#767c82" stroke-width="6"/>')
    s += SL(Z_SRED, kolo + "</g>")

    # ТРИ НАХОДКИ — ГЛАВНЫЕ ПРЕДМЕТЫ КАДРА: монета 416 px (две головы
    # прохожей), купюра 540, перчатка 420 по длинной стороне
    s += SL(Z_SRED, _moneta_krupno(336, 936, 208, t, .2, True, True, .80))
    kp = A.ease(A.seg(t, 2.4, .8))
    s += SL(Z_SRED, f'<path d="M600,904 L1134,866 L1148,1000 L614,1038 Z"'
                    f' fill="#9aa07e" {o(6)}/>'
                    f'<path d="M600,904 L1148,1000" fill="none" stroke="#7c8463"'
                    f' stroke-width="7"/>'
                    f'<path d="M700,892 L716,1020 M1012,870 L1028,998"'
                    f' stroke="#7c8463" stroke-width="6" opacity=".8"/>'
                    f'<ellipse cx="872" cy="950" rx="86" ry="52" fill="none"'
                    f' stroke="#7c8463" stroke-width="7" opacity=".7"/>'
                    f'<path d="M622,{896+30*kp:.0f} Q880,{836+30*kp:.0f}'
                    f' {1160:.0f},{884+30*kp:.0f}" fill="none" stroke="#b4762f"'
                    f' stroke-width="26" opacity="{kp*.9:.2f}"/>')
    per = (f'<path d="M1280,980 L1270,880 Q1300,856 1330,878 L1340,960'
           f' L1410,944 Q1440,956 1430,984 L1360,1016 Q1310,1030 1280,1010 Z"'
           f' fill="#7a5a86" {o(6)}/>')
    for i in range(4):
        per += (f'<path d="M{1272+i*20:.0f},{884-i*4:.0f} L{1282+i*20:.0f},'
                f'{836-i*6:.0f} Q{1300+i*20:.0f},{824-i*6:.0f}'
                f' {1312+i*20:.0f},{842-i*6:.0f} L{1304+i*20:.0f},{890-i*4:.0f} Z"'
                f' fill="#8a6a96" {o(4)}/>')
    per += (f'<path d="M1286,948 Q1340,934 1400,946 M1290,976 Q1344,962 1406,974"'
            f' fill="none" stroke="#5e4068" stroke-width="6" opacity=".8"/>')
    s += SL(Z_SRED, f'<g transform="translate(-668 -542) scale(1.58)">{per}</g>')
    for i, (chx, chy) in enumerate(((336, 770), (872, 806), (1416, 758))):
        ch = A.ease(A.seg(t, .6 + i * .6, .5))
        s += SL(Z_SRED, f'<rect x="{chx-150*ch:.0f}" y="{chy:.0f}"'
                        f' width="{300*ch:.0f}" height="20" rx="10" fill="{KRAS}"'
                        f' opacity="{ch*.9:.2f}" {o(3)}/>')
    # лист накрывает купюру
    nl = A.ease(A.seg(t, 3.2, 1.0))
    s += SL(Z_SRED, f'<g transform="rotate({40*nl:.0f} 876 {690+240*nl:.0f})">'
                    f'<path d="M720,{690+240*nl:.0f} Q876,{586+240*nl:.0f}'
                    f' {1032:.0f},{690+240*nl:.0f} Q876,{776+240*nl:.0f}'
                    f' {720:.0f},{690+240*nl:.0f} Z" fill="#b4762f" {o(5)}/></g>')

    # женщина идёт мимо, не сбавляя шага
    hod = (t * .32) % 1.0
    fx, fy, fh = 460 + 900 * hod, 1062, 680
    zh = figura(fx, fy, fh, t, col="#3f3a46", kant="#cfe4f5", ph=.2)
    r1, (sx2, sy2), (z1x, z1y) = _ruka_ekr(fx, fy, fh, 1, fh * .44, 86, t, "#3f3a46", "#cfe4f5",
                                           .1, 8)
    r2, _, (z2x, z2y) = _ruka_ekr(fx, fy, fh, -1, fh * .34, 102, t, "#3f3a46", "#cfe4f5", .5, 4)
    zh += r1 + r2
    sk = 10 * A.w(t, 1.2, .2)
    zh += (f'<g transform="rotate({sk:.1f} {sx2:.0f} {sy2:.0f})">'
           f'<rect x="{sx2-58:.0f}" y="{sy2:.0f}" width="116" height="92" rx="12"'
           f' fill="#5a3f46" {o(5)}/>'
           f'<path d="M{sx2-30:.0f},{sy2:.0f} Q{sx2:.0f},{sy2-50:.0f}'
           f' {sx2+30:.0f},{sy2:.0f}" fill="none" stroke="#5a3f46" stroke-width="8"/></g>')
    # берет
    zh += (f'<path d="M{fx-54:.0f},{fy-fh*.88:.0f} Q{fx:.0f},{fy-fh*.99:.0f}'
           f' {fx+54:.0f},{fy-fh*.88:.0f} Q{fx:.0f},{fy-fh*.82:.0f}'
           f' {fx-54:.0f},{fy-fh*.88:.0f} Z" fill="#5a3f46" {o(4)}/>'
           f'<circle cx="{fx+6:.0f}" cy="{fy-fh*.99:.0f}" r="9" fill="#5a3f46"/>')
    zh += para_izo_rta(fx + 44, fy - fh * .80, t, .2, 1.0, .5)
    s += SL(Z_SRED, zh + ten(fx, fy + 8, 110, 20, .45))
    s += SL(Z_SRED, _gorodskoy_hlam(60, 700, 420, t, 191, ["stolbik", "kust"]))
    s += SL(Z_SRED, _gorodskoy_hlam(1180, 706, 460, t, 395, ["yaschik", "velik"]))
    s += SL(Z_SRED, _gorodskoy_hlam(1380, 1062, 520, t, 193,
                                   ["yaschik", "korobka", "stolbik"]))
    s += SL(Z_SRED, _zabor_dosok(540, 600, 560, 190, 195, 56, "#3f5a46"))
    s += SL(Z_SRED, _gorodskoy_hlam(700, 1070, 440, t, 317, ["kust", "stolbik"]))
    s += SL(Z_SRED, goloe_derevo(1500, 700, 360, t, 319, 7, "#2a2b33", False))
    s += SL(Z_LETIT, mokryy_sneg(t, 20, 25, .45, .8))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def perchatka_na_zabore(t):
    """Низкий заборчик палисадника у подъезда: на столбике НА ПОЛ-КАДРА
    надета вязаная перчатка пальцами вверх. На ветке сирени чьи-то ключи с
    брелоком, на скамейке забытый плюшевый заяц. Мужчина подбегает,
    снимает перчатку ЛЕВОЙ рукой и держит обе перед собой."""
    rnd = random.Random(124)
    s = f'<rect width="{W}" height="{H}" fill="#2d3038"/>'
    s += SL(Z_DAL, panelka(620, 520, 900, t, 5, True, 11))
    s += SL(Z_DAL, panelka(1740, 500, 520, t, 5, True, 13))
    s += SL(Z_DAL, tusklaya_lampochka(1140, 300, t, 1.8, False))
    s += SL(Z_DAL, teplo(1140, 410, 280, 230, .38))
    s += SL(Z_DAL, goloe_derevo(240, 540, 480, t, 15, 9, "#2a2b33", False))
    s += SL(Z_SRED, _asfalt(540, 1080, 31, 30))

    # козырёк подъезда и дверь
    s += SL(Z_SRED, f'<rect x="900" y="300" width="420" height="300" rx="8"'
                    f' fill="#3f4650" {o(6)}/>'
                    f'<rect x="950" y="340" width="150" height="260" rx="6"'
                    f' fill="#2a3038" {o(5)}/>'
                    f'<rect x="1120" y="340" width="150" height="260" rx="6"'
                    f' fill="#2a3038" {o(5)}/>'
                    f'<rect x="860" y="268" width="500" height="36" rx="10"'
                    f' fill="#5e656a" {o(5)}/>'
                    f'<rect x="1095" y="440" width="20" height="60" rx="8"'
                    f' fill="#9aa2a8" {o(3)}/>')

    # заборчик палисадника
    s += SL(Z_SRED, _zabor_dosok(60, 686, 1100, 290, 33, 58, "#3f5a46"))
    # столбик со вязаной перчаткой — главный предмет
    px, py = 500, 700
    kch = 3.0 * A.w(t, 2.4, .1)
    s += SL(Z_SRED, f'<rect x="{px-46:.0f}" y="{py:.0f}" width="92" height="330" rx="10"'
                    f' fill="#3f5a46" {o(6)}/>'
                    f'<rect x="{px-58:.0f}" y="{py-20:.0f}" width="116" height="26"'
                    f' rx="9" fill="#4e6b54" {o(4)}/>')
    snyal = A.ease(A.seg(t, 2.8, .9))
    perch = (f'<g transform="rotate({kch:.1f} {px:.0f} {py:.0f})" '
             f'opacity="{1-snyal:.2f}">'
             f'<path d="M{px-88:.0f},{py-20:.0f} L{px-78:.0f},{py-250:.0f}'
             f' Q{px-46:.0f},{py-300:.0f} {px-14:.0f},{py-252:.0f}'
             f' L{px-6:.0f},{py-130:.0f} L{px+10:.0f},{py-290:.0f}'
             f' Q{px+42:.0f},{py-330:.0f} {px+66:.0f},{py-284:.0f}'
             f' L{px+58:.0f},{py-120:.0f} L{px+88:.0f},{py-20:.0f} Z"'
             f' fill="#7a5a86" {o(7)}/>')
    for i in range(5):
        perch += (f'<path d="M{px-84+i*6:.0f},{py-60-i*34:.0f}'
                  f' Q{px:.0f},{py-96-i*34:.0f} {px+84-i*6:.0f},{py-60-i*34:.0f}"'
                  f' fill="none" stroke="#5e4068" stroke-width="7" opacity=".8"/>')
    perch += (f'<path d="M{px-52:.0f},{py-212:.0f} Q{px:.0f},{py-250:.0f}'
              f' {px+44:.0f},{py-216:.0f}" fill="none" stroke="#9a7aa6"'
              f' stroke-width="6" opacity=".8"/></g>')
    s += SL(Z_SRED, perch)

    # ветка сирени с ключами
    s += SL(Z_SRED, _vetka_pered(1500, 420, 420, 128, t, 35, "#3a2f28", 6))
    zv = 8 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<g transform="rotate({zv:.1f} 1680 620)">'
                    f'<line x1="1680" y1="620" x2="1680" y2="690" stroke="{ZHELEZ}"'
                    f' stroke-width="5"/>'
                    f'<circle cx="1680" cy="702" r="22" fill="none" stroke="{ZHELEZ}"'
                    f' stroke-width="7"/>'
                    f'<path d="M1668,716 L1660,790 L1676,790 L1670,760 L1684,760"'
                    f' fill="none" stroke="url(#zhel)" stroke-width="8"/>'
                    f'<path d="M1696,716 L1704,780 L1690,780" fill="none"'
                    f' stroke="url(#zhel)" stroke-width="8"/>'
                    f'<circle cx="1712" cy="712" r="26" fill="#8a6a46" {o(3)}/>'
                    f'<circle cx="1698" cy="692" r="12" fill="#8a6a46" {o(2)}/>'
                    f'<circle cx="1726" cy="692" r="12" fill="#8a6a46" {o(2)}/></g>')

    # скамейка с плюшевым зайцем
    s += SL(Z_SRED, f'<rect x="60" y="930" width="420" height="28" rx="10"'
                    f' fill="url(#dosk)" {o(5)}/>'
                    f'<rect x="60" y="848" width="420" height="24" rx="10"'
                    f' fill="url(#dosk)" {o(5)}/>'
                    f'<rect x="96" y="958" width="24" height="120" rx="8"'
                    f' fill="#4a5055" {o(4)}/>'
                    f'<rect x="416" y="958" width="24" height="120" rx="8"'
                    f' fill="#4a5055" {o(4)}/>')
    # ПЛЮШЕВЫЙ ЗАЯЦ УБРАН (осмотр 15.11: «сцена городская»). На скамейке —
    # городские забытые вещи: сложенный зонт и авоська с покупками.
    zk = 3 * A.w(t, 2.8, .4)
    s += SL(Z_SRED, f'<g transform="rotate({zk:.1f} 150 928)">'
                    f'<rect x="92" y="800" width="26" height="128" rx="10"'
                    f' fill="#3a4452" {o(4)}/>'
                    f'<path d="M86,800 Q105,748 124,800 Q134,836 105,844'
                    f' Q78,838 86,800 Z" fill="#46506a" {o(5)}/>'
                    f'<rect x="98" y="760" width="14" height="48" rx="6"'
                    f' fill="#6a7488" opacity=".8"/>'
                    f'<path d="M118,924 q26,22 44,-4" fill="none" stroke="#2a3038"'
                    f' stroke-width="9"/></g>')
    avos = (f'<path d="M250,932 Q238,1010 310,1022 Q384,1012 372,932 Z"'
            f' fill="#6a7a5e" opacity=".55" {o(5)}/>')
    for i in range(5):
        avos += (f'<line x1="{258+i*29:.0f}" y1="938" x2="{266+i*26:.0f}" y2="1018"'
                 f' stroke="#8a9a76" stroke-width="4" opacity=".8"/>'
                 f'<path d="M248,{950+i*16:.0f} Q310,{964+i*16:.0f}'
                 f' {374:.0f},{948+i*16:.0f}" fill="none" stroke="#8a9a76"'
                 f' stroke-width="4" opacity=".7"/>')
    avos += (f'<circle cx="286" cy="976" r="32" fill="#a8482f" {o(4)}/>'
             f'<circle cx="340" cy="986" r="27" fill="#8a9a3a" {o(4)}/>'
             f'<ellipse cx="312" cy="944" rx="38" ry="20" fill="#c8a24a" {o(3)}/>'
             f'<path d="M254,934 Q268,886 296,906 M366,934 Q352,886 324,906"'
             f' fill="none" stroke="#6a7a5e" stroke-width="9"/>')
    s += SL(Z_SRED, avos)

    # мужчина подбегает и прижимает перчатки к груди
    beg = A.ease(A.seg(t, .3, 1.6))
    fx, fy, fh = 1500 - 620 * beg, 1046, 560
    m = figura(fx, fy, fh, t, col="#3a4452", kant="#cfe4f5", ph=.2, naklon=-12 * (1 - beg))
    # СНИМАЕТ ЛЕВОЙ: столбик с перчаткой стоит СЛЕВА от него, и тянуться
    # туда правой рукой значило вести рукав бруском через голову на 206 px
    # за ось тела (осмотр 15.11). Обе перчатки он потом держит перед собой,
    # но не на груди: рукав без кисти, прижатый к груди, читается палкой.
    r2, (hx2, hy2), (m2x, m2y) = _ruka(fx, fy, fh, -1, fh * (.58 - .18 * snyal),
                                       -12 + 46 * snyal, t, "#3a4452", "#cfe4f5", .5, 5)
    r1, (hx1, hy1), (m1x, m1y) = _ruka(fx, fy, fh, 1, fh * (.34 + .08 * snyal),
                                       26 + 18 * snyal, t, "#3a4452", "#cfe4f5", .1, 7)
    m += r1 + r2
    # вторая перчатка в правой руке с самого начала
    m += (f'<path d="M{hx1-32:.0f},{hy1-46:.0f} L{hx1-24:.0f},{hy1-104:.0f}'
          f' Q{hx1-4:.0f},{hy1-130:.0f} {hx1+14:.0f},{hy1-102:.0f}'
          f' L{hx1+20:.0f},{hy1-44:.0f} L{hx1+32:.0f},{hy1+6:.0f}'
          f' Q{hx1:.0f},{hy1+22:.0f} {hx1-32:.0f},{hy1+6:.0f} Z" fill="#7a5a86"'
          f' {o(5)}/>')
    # снятая перчатка приходит в левую руку
    if snyal > .02:
        m += (f'<g opacity="{snyal:.2f}">'
              f'<path d="M{hx2-32:.0f},{hy2-46:.0f} L{hx2-24:.0f},{hy2-104:.0f}'
              f' Q{hx2-4:.0f},{hy2-130:.0f} {hx2+14:.0f},{hy2-102:.0f}'
              f' L{hx2+20:.0f},{hy2-44:.0f} L{hx2+32:.0f},{hy2+6:.0f}'
              f' Q{hx2:.0f},{hy2+22:.0f} {hx2-32:.0f},{hy2+6:.0f} Z"'
              f' fill="#8a6a96" {o(5)}/></g>')
    m += para_izo_rta(fx + 44, fy - fh * .80, t, .2, 1.0, .5)
    s += SL(Z_SRED, m + ten(fx, fy + 8, 110, 20, .45))
    s += SL(Z_SRED, _gorodskoy_hlam(1380, 1070, 520, t, 197,
                                   ["velik", "yaschik", "stolbik"]))
    s += SL(Z_SRED, _gorodskoy_hlam(640, 1074, 420, t, 199, ["korobka", "kust"]))
    s += SL(Z_SRED, _gorodskoy_hlam(300, 700, 380, t, 313, ["stolbik", "kust"]))
    s += SL(Z_SRED, _zabor_dosok(900, 780, 520, 200, 315, 56, "#3f5a46"))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 27, .45, .8))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def babushkin_shag_u_podezda(t):
    """Дорожка к подъезду, посреди неё блестит монета. Женщина в пальто идёт
    к подъезду и перешагивает монету; рядом полупрозрачным контуром тем же
    движением шагает бабушка в платке с бидоном. Клумба, скамейка, кот."""
    rnd = random.Random(125)
    s = f'<rect width="{W}" height="{H}" fill="#2d3038"/>'
    s += SL(Z_DAL, panelka(500, 500, 820, t, 5, True, 15)
            + panelka(1620, 480, 600, t, 5, True, 17))
    s += SL(Z_DAL, goloe_derevo(180, 510, 440, t, 19, 8, "#2a2b33", False))
    s += SL(Z_DAL, tusklaya_lampochka(960, 250, t, 1.8, False))
    s += SL(Z_DAL, teplo(960, 370, 300, 240, .38))
    s += SL(Z_SRED, _asfalt(520, 1080, 37, 32))
    s += SL(Z_SRED, f'<path d="M620,1080 Q780,820 900,600 L1120,600 Q1200,820'
                    f' 1360,1080 Z" fill="#62646a" opacity=".9"/>')

    # подъезд
    s += SL(Z_SRED, f'<rect x="840" y="320" width="340" height="300" rx="8"'
                    f' fill="#3f4650" {o(6)}/>'
                    f'<rect x="880" y="356" width="124" height="262" rx="6"'
                    f' fill="#2a3038" {o(5)}/>'
                    f'<rect x="1018" y="356" width="124" height="262" rx="6"'
                    f' fill="#2a3038" {o(5)}/>'
                    f'<rect x="806" y="292" width="408" height="34" rx="10"'
                    f' fill="#5e656a" {o(5)}/>')

    # клумба и скамейка
    klm = (f'<path d="M80,900 Q300,840 520,900 Q300,970 80,900 Z" fill="#4a3f33" {o(5)}/>')
    for i in range(9):
        cx_ = 120 + i * 48
        kk = 4 * A.w(t, 3.0, i * .2)
        klm += (f'<g transform="rotate({kk:.1f} {cx_:.0f} 900)">'
                f'<line x1="{cx_:.0f}" y1="900" x2="{cx_+6:.0f}" y2="{824:.0f}"'
                f' stroke="#5e6b42" stroke-width="6"/>'
                f'<circle cx="{cx_+6:.0f}" cy="816" r="18"'
                f' fill="{["#b4762f","#8a5a86","#9a5a28"][i%3]}" {o(2)}/></g>')
    s += SL(Z_SRED, klm)
    skam = (f'<rect x="1080" y="840" width="800" height="32" rx="12" fill="url(#dosk)"'
            f' {o(6)}/>'
            f'<rect x="1080" y="752" width="800" height="28" rx="11" fill="url(#dosk)"'
            f' {o(6)}/>'
            f'<rect x="1080" y="796" width="800" height="28" rx="11" fill="url(#dosk)"'
            f' {o(6)}/>'
            f'<rect x="1124" y="872" width="26" height="130" rx="9" fill="#4a5055" {o(4)}/>'
            f'<rect x="1810" y="872" width="26" height="130" rx="9" fill="#4a5055" {o(4)}/>'
            f'<rect x="160" y="620" width="1180" height="34" rx="12" fill="#7a7c80"'
            f' {o(5)}/>')
    s += SL(Z_SRED, skam)
    # КОТ ЧИТАЕТСЯ КОТОМ (осмотр 15.11: было чёрное пятно с двумя точками)
    s += SL(Z_SRED, _kot_zhivoy(1596, 840, t, 1.35, "#4a423c", .3))

    # монета на дорожке
    s += SL(Z_SRED, _moneta_krupno(960, 900, 88, t, .2, True, True, .84))

    hod = (t * .30) % 1.0
    pere = max(.0, math.sin(hod * math.pi)) * 120

    # сегодняшняя женщина
    fx, fy, fh = 500 + 820 * hod, 1046, 580
    zh = figura(fx, fy - pere * .12, fh, t, col="#3f3a46", kant="#cfe4f5", ph=.2)
    r1, (sx2, sy2), (z1x, z1y) = _ruka_ekr(fx, fy, fh, 1, fh * .44, 90, t, "#3f3a46", "#cfe4f5",
                                           .1, 7)
    r2, _, (z2x, z2y) = _ruka_ekr(fx, fy, fh, -1, fh * .30, 54, t, "#3f3a46", "#cfe4f5", .5, 4)
    zh += r1 + r2
    zh += (f'<rect x="{sx2-54:.0f}" y="{sy2:.0f}" width="108" height="104" rx="10"'
           f' fill="#8a7a58" {o(5)}/>'
           f'<path d="M{sx2-30:.0f},{sy2:.0f} Q{sx2:.0f},{sy2-44:.0f}'
           f' {sx2+30:.0f},{sy2:.0f}" fill="none" stroke="#8a7a58" stroke-width="8"/>'
           f'<ellipse cx="{sx2:.0f}" cy="{sy2+30:.0f}" rx="40" ry="24" fill="#c9a86a"'
           f' {o(3)}/>')
    # поднятая нога
    zh += (f'<line x1="{fx+20:.0f}" y1="{fy-fh*.30:.0f}" x2="{fx+78:.0f}"'
           f' y2="{fy-10-pere:.0f}" stroke="#3f3a46" stroke-width="40"'
           f' stroke-linecap="round"/>')
    zh += para_izo_rta(fx + 44, fy - fh * .80, t, .2, 1.0, .5)
    s += SL(Z_SRED, zh + ten(fx, fy + 8, 110, 20, .45))

    # бабушка полупрозрачным контуром, то же движение
    gx = fx - 230
    bab = figura(gx, fy - pere * .12, 560, t, col="#6a7a8a", kant="#cfe4f5",
                 platok=True, ph=.5, op=.42, tulup=True)
    r3, (bx2, by2), (g1x, g1y) = _ruka_ekr(gx, fy, 560, 1, 560 * .44, 78, t, "#6a7a8a",
                                           "#cfe4f5", .3, 7)
    r4, _, (g2x, g2y) = _ruka_ekr(gx, fy, 560, -1, 560 * .24, -100, t, "#6a7a8a", "#cfe4f5", .7, 4)
    bab += r3 + r4
    bid = 10 * A.w(t, 1.3, .2)
    bab += (f'<g transform="rotate({bid:.1f} {bx2:.0f} {by2:.0f})" opacity=".45">'
            f'<rect x="{bx2-42:.0f}" y="{by2:.0f}" width="84" height="110" rx="10"'
            f' fill="#8fa2b4" {o(4)}/>'
            f'<rect x="{bx2-50:.0f}" y="{by2-14:.0f}" width="100" height="22" rx="8"'
            f' fill="#8fa2b4" {o(3)}/>'
            f'<path d="M{bx2-30:.0f},{by2-14:.0f} Q{bx2:.0f},{by2-60:.0f}'
            f' {bx2+30:.0f},{by2-14:.0f}" fill="none" stroke="#8fa2b4"'
            f' stroke-width="8"/></g>')
    bab += (f'<line x1="{gx+20:.0f}" y1="{fy-560*.30:.0f}" x2="{gx+78:.0f}"'
            f' y2="{fy-10-pere:.0f}" stroke="#6a7a8a" stroke-width="40"'
            f' stroke-linecap="round" opacity=".42"/>')
    s += SL(Z_SRED, bab)
    s += SL(Z_SRED, _gorodskoy_hlam(60, 1072, 460, t, 201,
                                   ["yaschik", "stolbik", "korobka"]))
    s += SL(Z_SRED, _gorodskoy_hlam(1400, 1076, 480, t, 203, ["velik", "kust"]))
    s += SL(Z_SRED, _gorodskoy_hlam(300, 1078, 440, t, 399, ["yaschik", "korobka"]))
    # НИЖНЯЯ ТРЕТЬ ОБЖИТА: мокрая дорожка со следами, лужа с отражением
    # подъезда, сгребённые к бордюру листья (осмотр 15.11 — голый асфальт)
    s += SL(Z_SRED, _sledy(640, 1074, 912, 736, 7, 205, "#4a4b50", 1.35)
            + _luzha(1246, 992, 214, t, .4, 72, "#8ea6bb")
            + _kucha_listev(690, 1062, 290, 207, 88)
            + _kucha_listev(1664, 1074, 320, 211, 102))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 29, .45, .8))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def larek_s_iriskami(t):
    """Фанерный ларёк с навесом и окошком на пол-кадра: на полке за стеклом
    банки с леденцами, пряники, коробка ирисок, весы. В окошке — настоящие
    ириски. Мальчик на цыпочках протягивает монетку, продавщица в белом
    колпаке подаёт ему ириску."""
    rnd = random.Random(126)
    s = nebo("den", t, False, 59)
    s += oblaka(t, 120, 5, 47, .45)
    s += SL(Z_DAL, panelka(260, 520, 560, t, 4, True, 19)
            + panelka(1700, 500, 520, t, 4, True, 21))
    s += SL(Z_DAL, goloe_derevo(120, 560, 430, t, 23, 8, "#2a2b33", False))
    s += SL(Z_SRED, _asfalt(560, 1080, 41, 30))

    # корпус ларька
    lx, ly, lw, lh = 420, 230, 1120, 720
    lar = (f'<rect x="{lx:.0f}" y="{ly:.0f}" width="{lw:.0f}" height="{lh:.0f}" rx="10"'
           f' fill="url(#dosk)" {o(7)}/>')
    for i in range(9):
        lar += (f'<rect x="{lx+10+i*(lw-20)/9:.0f}" y="{ly+10:.0f}"'
                f' width="{(lw-20)/9-10:.0f}" height="{lh-20:.0f}" rx="6"'
                f' fill="#7d6a48" {o(3)}/>')
    # навес
    lar += (f'<path d="M{lx-70:.0f},{ly:.0f} L{lx+lw/2:.0f},{ly-130:.0f}'
            f' L{lx+lw+70:.0f},{ly:.0f} Z" fill="#8a4a4a" {o(6)}/>'
            f'<rect x="{lx-86:.0f}" y="{ly-10:.0f}" width="{lw+172:.0f}" height="30"'
            f' rx="10" fill="#6a3a3a" {o(5)}/>')
    for i in range(10):
        lar += (f'<rect x="{lx-60+i*(lw+120)/10:.0f}" y="{ly-6:.0f}"'
                f' width="{(lw+120)/20:.0f}" height="26" fill="#a85a5a"'
                f' opacity=".75"/>')
    s += SL(Z_SRED, lar)

    # полка за стеклом: банки, пряники, коробка ирисок, весы
    s += SL(Z_SRED, f'<rect x="{lx+60:.0f}" y="{ly+70:.0f}" width="{lw-120:.0f}"'
                    f' height="230" rx="8" fill="#2e3a40" {o(5)}/>'
                    f'<rect x="{lx+60:.0f}" y="{ly+290:.0f}" width="{lw-120:.0f}"'
                    f' height="22" rx="8" fill="#5b4428" {o(4)}/>')
    bank = ""
    for i in range(4):
        bx_ = lx + 150 + i * 150
        bank += (f'<rect x="{bx_-52:.0f}" y="{ly+140:.0f}" width="104" height="150"'
                 f' rx="12" fill="#9fc4da" opacity=".8" {o(4)}/>'
                 f'<rect x="{bx_-58:.0f}" y="{ly+122:.0f}" width="116" height="26"'
                 f' rx="9" fill="#c9c2ae" {o(3)}/>')
        for k in range(7):
            bank += (f'<circle cx="{bx_-34+(k%3)*34:.0f}" cy="{ly+200+(k//3)*32:.0f}"'
                     f' r="16" fill="{["#c84a3a","#d8a14a","#6f9a5e"][k%3]}"'
                     f' opacity=".95"/>')
    bank += (f'<rect x="{lx+760:.0f}" y="{ly+170:.0f}" width="190" height="120" rx="8"'
             f' fill="#b4762f" {o(5)}/>'
             f'<rect x="{lx+760:.0f}" y="{ly+170:.0f}" width="190" height="26" rx="7"'
             f' fill="#8a5a22" {o(3)}/>')
    for k in range(6):
        bank += _iriska(lx + 794 + (k % 3) * 60, ly + 224 + (k // 3) * 44,
                        .78, -18 + (k % 3) * 22, "#7d4f1c", "#e8dcc0")
    s += SL(Z_SRED, bank)

    # весы с качающейся чашей
    vx_, vy_ = lx + 1000, ly + 300
    nak = 8 * A.w(t, 1.6, .2)
    s += SL(Z_SRED, f'<rect x="{vx_-14:.0f}" y="{vy_-150:.0f}" width="28" height="150"'
                    f' rx="9" fill="{ZHELEZ}" {o(4)}/>'
                    f'<g transform="rotate({nak:.1f} {vx_:.0f} {vy_-150:.0f})">'
                    f'<rect x="{vx_-90:.0f}" y="{vy_-160:.0f}" width="180" height="16"'
                    f' rx="7" fill="{ZHELEZ}" {o(3)}/>'
                    f'<path d="M{vx_-120:.0f},{vy_-110:.0f} Q{vx_-80:.0f},{vy_-64:.0f}'
                    f' {vx_-40:.0f},{vy_-110:.0f} Z" fill="url(#zhel)" {o(4)}/>'
                    f'<path d="M{vx_+40:.0f},{vy_-110:.0f} Q{vx_+80:.0f},{vy_-64:.0f}'
                    f' {vx_+120:.0f},{vy_-110:.0f} Z" fill="url(#zhel)" {o(4)}/>'
                    f'<line x1="{vx_-80:.0f}" y1="{vy_-144:.0f}" x2="{vx_-80:.0f}"'
                    f' y2="{vy_-110:.0f}" stroke="{ZHELEZ}" stroke-width="4"/>'
                    f'<line x1="{vx_+80:.0f}" y1="{vy_-144:.0f}" x2="{vx_+80:.0f}"'
                    f' y2="{vy_-110:.0f}" stroke="{ZHELEZ}" stroke-width="4"/></g>')

    # окошко-витрина: нарисованный вид, метка, потом переплёт поверх
    px_, py_, pw_, ph_ = 560, 560, 800, 300
    put = kontur_proema(px_, py_, pw_, ph_, "pryam")
    vit = (f'<path d="{put}" fill="#6a4a28"/>')
    # В ОКОШКЕ — ИРИСКИ В ФАНТИКАХ (были жёлтые кружки = мелочь)
    for i in range(11):
        vit += _iriska(px_ + 70 + i * 66, py_ + ph_ * .5 + ((i % 3) - 1) * 60,
                       1.12, -26 + (i % 4) * 17, "#8a5a22", "#efe2c2")
    s += SL(Z_SRED, vit + mesto_stoka(px_, py_, pw_, ph_, "pryam")
            + f'<path d="{put}" fill="none" stroke="#5b4428" stroke-width="18"/>'
            + f'<rect x="{px_-20:.0f}" y="{py_+ph_-6:.0f}" width="{pw_+40:.0f}"'
              f' height="40" rx="10" fill="#8a7248" {o(5)}/>')
    s += SL(Z_SRED, lampa(960, 150, t, 1.3, True))
    s += SL(Z_SRED, teplo(960, 700, 460, 300, .36))

    # мальчик на цыпочках
    cyp = 24 * A.ease(abs(A.w(t, 2.0, .0)))
    mx_, my_, mh_ = 620, 1050 - cyp, 420
    mal = figura(mx_, my_, mh_, t, col="#3a4452", kant="#ffd98a", ph=.3)
    # ТЯНЕТСЯ ОДНОЙ РУКОЙ — к окошку, оно справа от него. Было: оба рукава
    # задраны вверх под -46° и -24°, в кадре это поза распятия (осмотр 15.11)
    r1, (hx1, hy1), (m1x, m1y) = _ruka(mx_, my_, mh_, 1, mh_ * .54, -44, t, "#3a4452",
                                       "#ffd98a", .2, 5)
    r2, _, (m2x, m2y) = _ruka(mx_, my_, mh_, -1, mh_ * .40, 64, t, "#3a4452",
                              "#ffd98a", .6, 4)
    mal += r1 + r2
    mal += _moneta_krupno(hx1, hy1 - 14, 26, t, .2, True, False, .9)
    # кепка
    mal += (f'<path d="M{mx_-50:.0f},{my_-mh_*.88:.0f} Q{mx_:.0f},{my_-mh_*1.0:.0f}'
            f' {mx_+50:.0f},{my_-mh_*.88:.0f} Z" fill="#2f3a44" {o(4)}/>'
            f'<rect x="{mx_+28:.0f}" y="{my_-mh_*.90:.0f}" width="54" height="16"'
            f' rx="7" fill="#2f3a44" {o(3)}/>')
    s += SL(Z_SRED, mal + ten(mx_, 1056, 78, 15, .45))

    # продавщица в белом колпаке
    px2, py2, ph2 = 1360, 1046, 470
    pro = figura(px2, py2, ph2, t, col="#e4e0d4", kant="#ffd98a", ph=.6)
    r3, _, (p1x, p1y) = _ruka_ekr(px2, py2, ph2, 1, ph2 * .40, -12, t, "#e4e0d4", "#ffd98a", .3, 4)
    r4, (hx2, hy2), (p2x, p2y) = _ruka_ekr(px2, py2, ph2, -1, ph2 * .54, -168, t, "#e4e0d4",
                                           "#ffd98a", .7, 5)
    pro += r3 + r4
    pro += (f'<rect x="{px2-46:.0f}" y="{py2-ph2*1.04:.0f}" width="92" height="76"'
            f' rx="12" fill="#f4f1e8" {o(4)}/>'
            f'<rect x="{px2-52:.0f}" y="{py2-ph2*.92:.0f}" width="104" height="22"'
            f' rx="9" fill="#e0dccc" {o(3)}/>')
    # ириска переходит из руки в руку
    ir = A.ease(A.seg(t, 1.4, 1.2))
    irx = hx2 + (hx1 - hx2) * ir
    iry = hy2 + (hy1 - 30 - hy2) * ir - 60 * math.sin(math.pi * ir)
    pro += _iriska(irx, iry, 1.45, 24 * ir, "#8a5a22", "#efe2c2")
    s += SL(Z_SRED, pro + ten(px2, 1052, 90, 17, .45))
    s += SL(Z_SRED, _gorodskoy_hlam(80, 1070, 320, t, 207, ["yaschik", "korobka"]))
    s += SL(Z_SRED, _gorodskoy_hlam(1620, 1074, 320, t, 209, ["stolbik", "kust"]))
    s += SL(Z_PERED, _stolb_pered(1880, 90, "#1d1611", 0, H))
    s += SL(Z_LETIT, sneg_letit(t, 12, 49, .28, .55))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def pyatak_v_tufle(t):
    """Школьный коридор, скамья у двери с табличкой без надписи. Школьница в
    форме с белым фартуком сидит на скамье: левая нога на полу, правая на
    левом колене. Левой держит снятую туфлю, правой кладёт под пятку пятак.
    Рядом портфель, зачётная книжка, букет астр."""
    rnd = random.Random(127)
    pol = 800
    s = f'<rect width="{W}" height="{H}" fill="#3a4442"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{pol:.0f}" fill="#54645e"/>'
                   f'<rect x="0" y="{pol-260:.0f}" width="{W}" height="260"'
                   f' fill="#6e7d74" opacity=".9"/>'
                   f'<rect x="0" y="{pol-274:.0f}" width="{W}" height="22"'
                   f' fill="#3e4a46" opacity=".9"/>'
                   f'<rect x="0" y="{pol-20:.0f}" width="{W}" height="34"'
                   f' fill="#2f3a36" opacity=".9"/>')
    # пол шашками
    sh = ""
    yy, ry = pol + 14, 0
    while yy < H:
        step = 120 + (yy - pol) * .5
        xx = -((ry % 2) * step / 2)
        while xx < W:
            sh += (f'<rect x="{xx:.0f}" y="{yy:.0f}" width="{step:.0f}"'
                   f' height="{step*.5:.0f}" fill="{["#6a5a4a","#4e4238"][ry%2]}"'
                   f' opacity=".85"/>')
            xx += step * 2
        yy += step * .5
        ry += 1
    s += SL(Z_DAL, sh)

    # две двери с табличками без надписи
    for i, dx in enumerate((160, 1500)):
        s += SL(Z_DAL, f'<rect x="{dx:.0f}" y="190" width="300" height="610" rx="8"'
                       f' fill="#6a5a3c" {o(6)}/>'
                       f'<rect x="{dx+24:.0f}" y="220" width="252" height="250" rx="6"'
                       f' fill="#7d6a48" {o(4)}/>'
                       f'<rect x="{dx+24:.0f}" y="500" width="252" height="270" rx="6"'
                       f' fill="#7d6a48" {o(4)}/>'
                       f'<rect x="{dx+250:.0f}" y="480" width="22" height="70" rx="9"'
                       f' fill="{ZHELEZ}" {o(3)}/>'
                       f'<rect x="{dx+90:.0f}" y="128" width="130" height="52" rx="7"'
                       f' fill="#e4dcc4" {o(4)}/>'
                       f'<path d="M{dx+104:.0f},154 Q{dx+140:.0f},142 {dx+178:.0f},156"'
                       f' fill="none" stroke="#9aa0a4" stroke-width="5"/>')
    # окно коридора и свет
    s += SL(Z_DAL, okno_izby(760, 150, 420, 330, t, svet=False, moroz=.0)
            + f'<rect x="780" y="168" width="382" height="296" fill="#aebfcc"'
              f' opacity=".9"/>')
    s += SL(Z_SRED, luch(700, 480, 520, 420, t, .20))
    s += SL(Z_SRED, tusklaya_lampochka(960, 70, t, 1.6, True))
    s += SL(Z_SRED, teplo(960, 300, 380, 280, .32))

    s += SL(Z_SRED, _gorodskoy_hlam(1500, 1076, 420, t, 211, ["yaschik", "kust"]))
    s += SL(Z_SRED, _gorodskoy_hlam(80, 1070, 360, t, 293, ["stolbik", "korobka"]))
    s += SL(Z_SRED, _kot_zhivoy(1760, 1062, t, 1.2, "#4a423c", .5))
    # батарея под окном
    bat = f'<rect x="700" y="560" width="540" height="140" rx="10" fill="#b9bcc0" {o(5)}/>'
    for i in range(11):
        bat += (f'<rect x="{716+i*48:.0f}" y="570" width="30" height="120" rx="9"'
                f' fill="#cdd1d4" {o(3)}/>')
    s += SL(Z_SRED, bat)
    # вешалка с пальто
    s += SL(Z_SRED, f'<rect x="1320" y="300" width="420" height="22" rx="9"'
                    f' fill="#5e4a3a" {o(5)}/>'
                    f'<rect x="1500" y="322" width="24" height="420" rx="9"'
                    f' fill="#5e4a3a" {o(4)}/>')
    for i in range(4):
        hx2 = 1360 + i * 108
        s += SL(Z_SRED, f'<rect x="{hx2-8:.0f}" y="308" width="16" height="40"'
                        f' fill="{ZHELEZ}" {o(2)}/>'
                        f'<path d="M{hx2-60:.0f},{360:.0f} Q{hx2:.0f},{330:.0f}'
                        f' {hx2+60:.0f},{360:.0f} L{hx2+74:.0f},{640:.0f}'
                        f' L{hx2-74:.0f},{640:.0f} Z"'
                        f' fill="{["#3a4452","#5a3340","#3d4a3a","#4a3b2a"][i]}"'
                        f' {o(5)}/>')
    # доска объявлений без текста
    s += SL(Z_SRED, f'<rect x="240" y="300" width="380" height="280" rx="10"'
                    f' fill="#6b5a3c" {o(5)}/>'
                    f'<rect x="262" y="322" width="336" height="236" rx="6"'
                    f' fill="#3a4a44" {o(3)}/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{286+i*110:.0f}" y="{348+(i%2)*90:.0f}" width="90"'
                        f' height="120" rx="5" fill="#e8e2d2" {o(2)}/>')
    # скамья
    s += SL(Z_SRED, _lavka_krupno(380, 1010, 1180, t, 216, True))
    # портфель, зачётка, астры НА скамье
    s += SL(Z_SRED, f'<rect x="1160" y="640" width="190" height="130" rx="10"'
                    f' fill="#5e3a2a" {o(5)}/>'
                    f'<rect x="1160" y="690" width="190" height="20" fill="#3a2419"'
                    f' opacity=".8"/>'
                    f'<rect x="1230" y="614" width="50" height="34" rx="12"'
                    f' fill="{ZHELEZ}" {o(3)}/>'
                    f'<rect x="1000" y="730" width="124" height="40" rx="5"'
                    f' fill="#8a3a3a" {o(4)}/>'
                    f'<rect x="1004" y="736" width="116" height="28" rx="4"'
                    f' fill="#e8e2d2" {o(2)}/>')
    ast = ""
    for i in range(7):
        ax = 250 + i * 32
        kk = 4 * A.w(t, 2.6, i * .25)
        ast += (f'<g transform="rotate({kk:.1f} {ax:.0f} 752)">'
                f'<line x1="{ax:.0f}" y1="752" x2="{ax+8:.0f}" y2="620"'
                f' stroke="#5e6b42" stroke-width="7"/>')
        for k in range(8):
            a = math.radians(k * 45)
            ast += (f'<ellipse cx="{ax+8+26*math.cos(a):.0f}"'
                    f' cy="{612+26*math.sin(a):.0f}" rx="16" ry="7"'
                    f' transform="rotate({k*45} {ax+8+26*math.cos(a):.0f}'
                    f' {612+26*math.sin(a):.0f})"'
                    f' fill="{["#b07ab0","#d4a0cc","#8a6aa6"][i%3]}" opacity=".95"/>')
        ast += (f'<circle cx="{ax+8:.0f}" cy="612" r="13" fill="#e8c86a"/></g>')
    s += SL(Z_SRED, ast)

    # школьница
    fx, fy, fh = 820, 790, 500
    put_ = A.ease(A.seg(t, .5, 1.0))
    vst = A.ease(A.seg(t, 2.6, .9))
    # пока сидит — короткий торс над скамьёй, встала — полный рост
    sit = 1 - vst
    fh_ = fh + 200 * vst
    fy_ = fy - 10 - 230 * vst
    shk = figura(fx, fy_, fh_, t, col="#3a3a46", kant="#ffd98a",
                 ph=.3, naklon=-8 * sit)
    r1, (hx1, hy1), (s1x, s1y) = _ruka_ekr(fx, fy_, fh_, 1, fh_ * .56, 64 - 40 * vst, t,
                                           "#3a3a46", "#ffd98a", .2, 5)
    r2, (hx2, hy2), (s2x, s2y) = _ruka_ekr(fx, fy_, fh_, -1, fh_ * .52, 108 - 30 * vst, t,
                                           "#3a3a46", "#ffd98a", .6, 4)
    shk += r1 + r2
    # белый фартук поверх формы
    byy = fy_
    shk += (f'<path d="M{fx-34:.0f},{byy-fh_*.56:.0f} L{fx+34:.0f},{byy-fh_*.56:.0f}'
            f' L{fx+48:.0f},{byy-fh_*.12:.0f} L{fx-48:.0f},{byy-fh_*.12:.0f} Z"'
            f' fill="#f2efe6" opacity=".95" {o(4)}/>'
            f'<path d="M{fx-26:.0f},{byy-fh_*.56:.0f} L{fx-16:.0f},{byy-fh_*.70:.0f}'
            f' M{fx+26:.0f},{byy-fh_*.56:.0f} L{fx+16:.0f},{byy-fh_*.70:.0f}"'
            f' stroke="#f2efe6" stroke-width="9"/>')
    # ТУФЛЯ И ПЯТАК — ГЛАВНЫЙ ПРЕДМЕТ КАДРА. Осмотр 15.11: «пятак и туфля не
    # опознаются» — туфля была 144 px безымянным пятном, пятак 60 px. Теперь
    # туфля 420 px с каблуком, подошвой, ремешком и стоптанным носком, пятак
    # 132 px ложится под пятку, и его видно поштучно.
    tx_, ty_ = hx2 - 36, hy2 + 24
    shk += (f'<ellipse cx="{tx_+10:.0f}" cy="{ty_+58:.0f}" rx="200" ry="30"'
            f' fill="#1f1714" opacity=".45"/>'
            f'<path d="M{tx_-206:.0f},{ty_+34:.0f} Q{tx_-196:.0f},{ty_-76:.0f}'
            f' {tx_-96:.0f},{ty_-104:.0f} Q{tx_+8:.0f},{ty_-122:.0f}'
            f' {tx_+104:.0f},{ty_-66:.0f} L{tx_+196:.0f},{ty_+8:.0f}'
            f' Q{tx_+210:.0f},{ty_+42:.0f} {tx_+150:.0f},{ty_+48:.0f}'
            f' L{tx_-196:.0f},{ty_+48:.0f} Z" fill="#4a2f2a" {o(7)}/>'
            f'<path d="M{tx_-196:.0f},{ty_+48:.0f} L{tx_+176:.0f},{ty_+24:.0f}'
            f' L{tx_+186:.0f},{ty_+54:.0f} L{tx_-194:.0f},{ty_+78:.0f} Z"'
            f' fill="#2a1a16" {o(5)}/>'
            f'<path d="M{tx_-196:.0f},{ty_+76:.0f} L{tx_-120:.0f},{ty_+72:.0f}'
            f' L{tx_-114:.0f},{ty_+146:.0f} L{tx_-186:.0f},{ty_+150:.0f} Z"'
            f' fill="#33211c" {o(5)}/>'
            f'<path d="M{tx_-176:.0f},{ty_-24:.0f} Q{tx_-86:.0f},{ty_-56:.0f}'
            f' {tx_+16:.0f},{ty_-62:.0f} Q{tx_+96:.0f},{ty_-54:.0f}'
            f' {tx_+150:.0f},{ty_-6:.0f}" fill="none" stroke="#6a443c"'
            f' stroke-width="10" opacity=".8"/>'
            f'<path d="M{tx_-118:.0f},{ty_-98:.0f} Q{tx_-20:.0f},{ty_-54:.0f}'
            f' {tx_+90:.0f},{ty_-70:.0f}" fill="none" stroke="#33211c"'
            f' stroke-width="16" opacity=".85"/>'
            f'<ellipse cx="{tx_+34:.0f}" cy="{ty_-74:.0f}" rx="20" ry="13"'
            f' fill="#c9a86a" {o(3)}/>'
            f'<path d="M{tx_+120:.0f},{ty_-44:.0f} Q{tx_+168:.0f},{ty_-26:.0f}'
            f' {tx_+188:.0f},{ty_+6:.0f}" fill="none" stroke="#8a6258"'
            f' stroke-width="9" opacity=".7"/>'
            f'<path d="M{tx_-178:.0f},{ty_-6:.0f} Q{tx_-90:.0f},{ty_+20:.0f}'
            f' {tx_+120:.0f},{ty_-2:.0f}" fill="none" stroke="#2a1a16"'
            f' stroke-width="7" opacity=".55"/>')
    px3 = hx1 + (tx_ - 150 - hx1) * put_
    py3 = hy1 + (ty_ + 6 - hy1) * put_
    shk += _moneta_krupno(px3, py3, 66, t, .2, True, True, .72)
    # нога на колене / обе на полу
    # сидит: левая нога на полу, правая закинута на левое колено
    bedr_x, bedr_y = fx - 40, byy - 6
    kol_x, kol_y = fx - 180 * sit, byy + 100 * sit
    shk += (f'<line x1="{bedr_x:.0f}" y1="{bedr_y:.0f}" x2="{kol_x:.0f}"'
            f' y2="{kol_y:.0f}" stroke="#3a3a46" stroke-width="46"'
            f' stroke-linecap="round" opacity="{sit:.2f}"/>'
            f'<line x1="{kol_x:.0f}" y1="{kol_y:.0f}" x2="{kol_x+8:.0f}"'
            f' y2="{1010:.0f}" stroke="#3a3a46" stroke-width="44"'
            f' stroke-linecap="round" opacity="{sit:.2f}"/>'
            f'<ellipse cx="{kol_x+2:.0f}" cy="{1024:.0f}" rx="56" ry="22"'
            f' fill="#4a2f2a" opacity="{sit:.2f}" {o(4)}/>'
            f'<line x1="{bedr_x+80:.0f}" y1="{bedr_y:.0f}" x2="{kol_x-30:.0f}"'
            f' y2="{kol_y-30:.0f}" stroke="#3a3a46" stroke-width="46"'
            f' stroke-linecap="round" opacity="{sit:.2f}"/>'
            f'<line x1="{kol_x-30:.0f}" y1="{kol_y-30:.0f}" x2="{kol_x+130:.0f}"'
            f' y2="{kol_y-110:.0f}" stroke="#3a3a46" stroke-width="44"'
            f' stroke-linecap="round" opacity="{sit:.2f}"/>')
    if vst > .02:
        shk += (f'<g opacity="{vst:.2f}">'
                f'<line x1="{fx-24:.0f}" y1="{byy-fh_*.24:.0f}" x2="{fx-50:.0f}"'
                f' y2="{1010:.0f}" stroke="#3a3a46" stroke-width="44"'
                f' stroke-linecap="round"/>'
                f'<line x1="{fx+24:.0f}" y1="{byy-fh_*.24:.0f}" x2="{fx+50:.0f}"'
                f' y2="{1010:.0f}" stroke="#3a3a46" stroke-width="44"'
                f' stroke-linecap="round"/>'
                f'<ellipse cx="{fx-54:.0f}" cy="{1026:.0f}" rx="54" ry="21"'
                f' fill="#4a2f2a" {o(4)}/>'
                f'<ellipse cx="{fx+54:.0f}" cy="{1026:.0f}" rx="54" ry="21"'
                f' fill="#4a2f2a" {o(4)}/></g>')
    s += SL(Z_SRED, shk)
    s += SL(Z_PERED, _stolb_pered(-6, 92, "#20262a", 0, H))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def babushka_i_moneta_v_ladoshke(t):
    """Двор у скамейки: внук лет пяти стоит на земле и гордо показывает на
    раскрытой ладошке найденную монету. Бабушка сидит на скамейке, правой
    берёт монету двумя пальцами и кладёт обратно на землю под скамейку.
    Рядом песочница, голуби, качели."""
    rnd = random.Random(128)
    s = f'<rect width="{W}" height="{H}" fill="#2d3038"/>'
    s += SL(Z_DAL, panelka(420, 500, 760, t, 5, True, 23)
            + panelka(1660, 480, 560, t, 5, True, 25))
    s += SL(Z_DAL, goloe_derevo(200, 540, 470, t, 27, 9, "#2a2b33", False))
    s += SL(Z_DAL, goloe_derevo(1260, 520, 380, t, 29, 8, "#2a2b33", False))
    s += SL(Z_DAL, tusklaya_lampochka(840, 220, t, 1.8, False))
    s += SL(Z_DAL, teplo(840, 340, 300, 240, .36))
    s += SL(Z_SRED, _asfalt(540, 1080, 43, 30))

    # качели
    kx, ky = 1540, 520
    kach = 9 * A.w(t, 2.6, .2)
    s += SL(Z_SRED, f'<path d="M{kx-200:.0f},1010 L{kx-110:.0f},{ky:.0f}'
                    f' L{kx+110:.0f},{ky:.0f} L{kx+200:.0f},1010" fill="none"'
                    f' stroke="#4a5055" stroke-width="22"/>'
                    f'<rect x="{kx-230:.0f}" y="{ky-16:.0f}" width="460" height="26"'
                    f' rx="10" fill="#5e656a" {o(4)}/>'
                    f'<g transform="rotate({kach:.1f} {kx:.0f} {ky:.0f})">'
                    f'<line x1="{kx-60:.0f}" y1="{ky:.0f}" x2="{kx-60:.0f}" y2="{ky+290:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="7"/>'
                    f'<line x1="{kx+60:.0f}" y1="{ky:.0f}" x2="{kx+60:.0f}" y2="{ky+290:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="7"/>'
                    f'<rect x="{kx-86:.0f}" y="{ky+290:.0f}" width="172" height="26"'
                    f' rx="9" fill="#8a4a4a" {o(4)}/></g>')

    # песочница
    s += SL(Z_SRED, f'<path d="M60,1010 L560,1010 L600,1076 L20,1076 Z"'
                    f' fill="#b09868" {o(5)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<rect x="{30+i*140:.0f}" y="984" width="150" height="34"'
                        f' rx="8" fill="#6b5a3c" {o(4)}/>')
    s += SL(Z_SRED, f'<rect x="150" y="930" width="70" height="58" rx="8"'
                    f' fill="#c84a3a" {o(4)}/>'
                    f'<path d="M150,930 Q185,900 220,930" fill="none" stroke="#c84a3a"'
                    f' stroke-width="7"/>'
                    f'<rect x="330" y="952" width="24" height="90" rx="8"'
                    f' fill="#4a5055" {o(3)}/>'
                    f'<path d="M318,952 L376,952 L364,992 L330,992 Z" fill="#d8a14a"'
                    f' {o(3)}/>')

    # скамейка
    s += SL(Z_SRED, f'<rect x="880" y="840" width="1020" height="34" rx="12"'
                    f' fill="url(#dosk)" {o(6)}/>'
                    f'<rect x="880" y="736" width="1020" height="28" rx="11"'
                    f' fill="url(#dosk)" {o(6)}/>'
                    f'<rect x="880" y="788" width="1020" height="28" rx="11"'
                    f' fill="url(#dosk)" {o(6)}/>'
                    f'<rect x="922" y="874" width="28" height="150" rx="9"'
                    f' fill="#4a5055" {o(4)}/>'
                    f'<rect x="1840" y="874" width="28" height="150" rx="9"'
                    f' fill="#4a5055" {o(4)}/>'
                    f'<rect x="896" y="676" width="28" height="172" rx="9"'
                    f' fill="#4a5055" {o(4)}/>'
                    f'<rect x="1856" y="676" width="28" height="172" rx="9"'
                    f' fill="#4a5055" {o(4)}/>')

    # бабушка на скамейке
    bx_, by_, bh_ = 1200, 840, 480
    vz = A.ease(A.seg(t, 1.2, 1.0))
    pol_ = A.ease(A.seg(t, 2.6, 1.0))
    bab = figura(bx_, by_, bh_, t, col="#46404e", kant="#ffd98a", platok=True, ph=.4,
                 naklon=10 * pol_)
    ug = 10 + 44 * vz + 36 * pol_
    r1, (hx1, hy1), (b1x, b1y) = _ruka_ekr(bx_, by_, bh_, 1, bh_ * (.50 + .14 * pol_),
                                           ug, t, "#46404e", "#ffd98a", .2, 5)
    r2, (hx2, hy2), (b2x, b2y) = _ruka_ekr(bx_, by_, bh_, -1, bh_ * .40, 56, t, "#46404e",
                                           "#ffd98a", .6, 4)
    bab += r1 + r2
    # сумка отодвинута НАРУЖУ: при опущенной вдоль тела руке её габарит
    # налезал бабушке на подол
    sum_x = hx2 + _predmet_naruzhu(bx_, bh_, hx2, 124)
    bab += (f'<rect x="{sum_x-62:.0f}" y="{hy2-40:.0f}" width="124" height="92" rx="12"'
            f' fill="#5a3f46" {o(5)}/>'
            f'<path d="M{sum_x-34:.0f},{hy2-40:.0f} Q{sum_x:.0f},{hy2-90:.0f}'
            f' {sum_x+34:.0f},{hy2-40:.0f}" fill="none" stroke="#5a3f46"'
            f' stroke-width="9"/>')
    # ноги на земле
    bab += (f'<line x1="{bx_-26:.0f}" y1="{by_-bh_*.24:.0f}" x2="{bx_-66:.0f}"'
            f' y2="{by_+176:.0f}" stroke="#46404e" stroke-width="40"'
            f' stroke-linecap="round"/>'
            f'<line x1="{bx_+26:.0f}" y1="{by_-bh_*.24:.0f}" x2="{bx_+8:.0f}"'
            f' y2="{by_+176:.0f}" stroke="#46404e" stroke-width="40"'
            f' stroke-linecap="round"/>')
    s += SL(Z_SRED, bab)

    # внук с монетой на ладошке
    vx_, vy_, vh_ = 740, 1030, 360
    vn = figura(vx_, vy_, vh_, t, col="#5a4a3a", kant="#ffd98a", ph=.7,
                naklon=8 * pol_)
    r3, (lx1, ly1), (v1x, v1y) = _ruka_ekr(vx_, vy_, vh_, 1, vh_ * .56, -28, t, "#5a4a3a",
                                           "#ffd98a", .3, 4)
    r4, _, (v2x, v2y) = _ruka_ekr(vx_, vy_, vh_, -1, vh_ * .44, 104, t, "#5a4a3a", "#ffd98a", .7,
                                  4)
    vn += r3 + r4
    s += SL(Z_SRED, vn + ten(vx_, vy_ + 6, 82, 16, .45))

    # МОНЕТУ В ЛАДОШКЕ ВИДНО (осмотр 15.11: было 88 px — пятнышко на рукаве).
    # Диаметр 196 px — почти две головы внука; под ней светлая оторочка
    # рукава вместо кисти (рук в кадре не рисуем) и тёплое пятно-подсветка.
    if pol_ < .02:
        mx_, my_ = lx1, ly1 - 26
        pl = .50
    else:
        mx_ = lx1 + (1240 - lx1) * pol_
        my_ = (ly1 - 26) + (1042 - (ly1 - 26)) * pol_
        pl = .50 + .40 * pol_
    s += SL(Z_SRED, f'<ellipse cx="{lx1:.0f}" cy="{ly1+10:.0f}" rx="104" ry="40"'
                    f' fill="#c9bfae" opacity="{(1-pol_)*.9:.2f}" {o(4)}/>'
                    f'<ellipse cx="{lx1:.0f}" cy="{ly1+2:.0f}" rx="84" ry="28"'
                    f' fill="#8a7a62" opacity="{(1-pol_)*.7:.2f}"/>'
            + teplo(mx_, my_, 210, 150, .34 * (1 - pol_ * .6))
            + _moneta_krupno(mx_, my_, 98, t, .2, True, True, pl))

    # голуби расходятся
    gol = ""
    for i in range(5):
        gp = ((t * .4 + i * .18) % 1.0)
        gx_ = 420 + i * 120 - 160 * gp
        gy_ = 1030 - 60 * max(.0, gp - .6) * 2.5
        gol += (f'<ellipse cx="{gx_:.0f}" cy="{gy_:.0f}" rx="42" ry="26"'
                f' fill="#6a7682" {o(3)}/>'
                f'<circle cx="{gx_-34:.0f}" cy="{gy_-20:.0f}" r="18" fill="#6a7682"'
                f' {o(3)}/>'
                f'<path d="M{gx_-50:.0f},{gy_-22:.0f} L{gx_-74:.0f},{gy_-16:.0f}'
                f' L{gx_-50:.0f},{gy_-10:.0f} Z" fill="#d8a14a" {o(2)}/>'
                f'<circle cx="{gx_-40:.0f}" cy="{gy_-24:.0f}" r="4" fill="#120c08"/>'
                f'<path d="M{gx_+6:.0f},{gy_-10:.0f} Q{gx_+26:.0f},'
                f'{gy_-44-20*max(.0,gp-.6)*2.5:.0f} {gx_+62:.0f},{gy_-16:.0f}'
                f' Q{gx_+34:.0f},{gy_+4:.0f} {gx_+6:.0f},{gy_+6:.0f} Z"'
                f' fill="#8a96a2" {o(2)}/>')
    s += SL(Z_SRED, gol)
    s += SL(Z_SRED, _gorodskoy_hlam(1660, 1076, 300, t, 213, ["stolbik", "kust"]))
    s += SL(Z_SRED, _gorodskoy_hlam(560, 700, 520, t, 365, ["kust", "stolbik", "kust"]))
    # НИЖНЯЯ ТРЕТЬ: лужа с отражением скамейки, сгребённые листья, авоська на
    # земле, следы к скамейке — вместо голого асфальта (осмотр 15.11)
    s += SL(Z_SRED, _luzha(1540, 1024, 230, t, .2, 76, "#8ea6bb")
            + _kucha_listev(380, 1060, 300, 215, 92)
            + _sledy(140, 1072, 640, 946, 6, 217, "#4a4b50", 1.2)
            + _yaschiki(930, 1056, t, 219, 1, .8))
    s += SL(Z_SRED, _zabor_dosok(420, 560, 1080, 180, 367, 58, "#3f5a46"))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 31, .4, .7))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def ostanovka_s_monetoy(t):
    """Стеклянный павильон остановки на пол-кадра, скамья, урна, расписание
    без текста. За стеклом — настоящая вечерняя улица в огнях. На плитке
    переднего плана крупно блестит монета. Мужчина в шляпе читает газету; женщина с
    зонтом-тростью проходит мимо, не наклоняясь."""
    rnd = random.Random(129)
    s = f'<rect width="{W}" height="{H}" fill="#20242e"/>'
    s += SL(Z_DAL, panelka(220, 480, 440, t, 6, True, 27)
            + panelka(1760, 460, 420, t, 6, True, 29))
    s += SL(Z_SRED, _asfalt(560, 1080, 45, 28))

    # нарисованный вид, метка, переплёт поверх
    px_, py_, pw_, ph_ = 300, 200, 790, 420
    put = kontur_proema(px_, py_, pw_, ph_, "pryam")
    s += SL(Z_SRED, _vid_za_proemom(put, t, "ulica", 17)
            + mesto_stoka(px_, py_, pw_, ph_, "pryam"))
    # переплёт павильона поверх кадра
    ram = (f'<path d="{put}" fill="none" stroke="#3f4650" stroke-width="26"/>'
           f'<rect x="{px_+pw_*.5-9:.0f}" y="{py_:.0f}" width="18" height="{ph_:.0f}"'
           f' fill="#3f4650" {o(3)}/>'
           f'<rect x="{px_:.0f}" y="{py_+ph_*.5-8:.0f}" width="{pw_:.0f}" height="16"'
           f' fill="#3f4650" {o(3)}/>'
           f'<path d="M{px_+40:.0f},{py_+ph_-40:.0f} L{px_+260:.0f},{py_+40:.0f}"'
           f' stroke="#cfe4f5" stroke-width="22" opacity=".16"/>'
           f'<path d="M{px_+150:.0f},{py_+ph_-40:.0f} L{px_+370:.0f},{py_+40:.0f}"'
           f' stroke="#cfe4f5" stroke-width="12" opacity=".12"/>')
    s += SL(Z_SRED, ram)
    # стойки и крыша павильона
    s += SL(Z_SRED, f'<rect x="{px_-150:.0f}" y="{py_-70:.0f}" width="{pw_+300:.0f}"'
                    f' height="48" rx="12" fill="#4a5560" {o(6)}/>'
                    f'<path d="M{px_-170:.0f},{py_-70:.0f} L{px_+pw_+170:.0f},{py_-70:.0f}'
                    f' L{px_+pw_+130:.0f},{py_-116:.0f} L{px_-130:.0f},{py_-116:.0f} Z"'
                    f' fill="#5e6a74" {o(5)}/>'
                    f'<rect x="{px_-70:.0f}" y="{py_-26:.0f}" width="40"'
                    f' height="{ph_+330:.0f}" rx="10" fill="#3f4650" {o(5)}/>'
                    f'<rect x="{px_+pw_+30:.0f}" y="{py_-26:.0f}" width="40"'
                    f' height="{ph_+330:.0f}" rx="10" fill="#3f4650" {o(5)}/>')
    # расписание без текста
    s += SL(Z_SRED, f'<rect x="1180" y="300" width="230" height="330" rx="10"'
                    f' fill="#2e3640" {o(5)}/>'
                    f'<rect x="1196" y="318" width="198" height="294" rx="6"'
                    f' fill="#e8e2d2" {o(3)}/>')
    for i in range(8):
        s += SL(Z_SRED, f'<path d="M1214,{350+i*34:.0f} Q1280,{338+i*34:.0f}'
                        f' 1376,{352+i*34:.0f}" fill="none" stroke="#8a929a"'
                        f' stroke-width="6"/>')
    s += SL(Z_SRED, tusklaya_lampochka(960, 120, t, 1.6, True))
    s += SL(Z_SRED, teplo(960, 320, 420, 300, .32))

    # скамья и урна
    s += SL(Z_SRED, f'<rect x="1060" y="800" width="840" height="34" rx="12"'
                    f' fill="url(#dosk)" {o(6)}/>'
                    f'<rect x="1060" y="698" width="840" height="28" rx="11"'
                    f' fill="url(#dosk)" {o(6)}/>'
                    f'<rect x="1060" y="748" width="840" height="28" rx="11"'
                    f' fill="url(#dosk)" {o(6)}/>'
                    f'<rect x="1104" y="834" width="28" height="170" rx="9"'
                    f' fill="#4a5055" {o(4)}/>'
                    f'<rect x="1832" y="834" width="28" height="170" rx="9"'
                    f' fill="#4a5055" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M250,860 L400,860 L376,1010 L274,1010 Z"'
                    f' fill="#4a5055" {o(6)}/>'
                    f'<rect x="236" y="842" width="178" height="26" rx="10"'
                    f' fill="#5e656a" {o(4)}/>')
    for i in range(4):
        s += SL(Z_SRED, f'<line x1="{272+i*36:.0f}" y1="872" x2="{280+i*34:.0f}"'
                        f' y2="1002" stroke="#333a3e" stroke-width="5" opacity=".7"/>')

    # МОНЕТА ЕСТЬ И ЕЁ ВИДНО (осмотр 15.11: «монеты в кадре НЕТ ВООБЩЕ» —
    # 144 px под скамьёй, да ещё за ногами мужчины и за проходящей женщиной).
    # Теперь 352 px на свободной плитке переднего плана, с бликом и
    # подсветкой, и ничем не перекрыта.
    s += SL(Z_SRED, f'<ellipse cx="700" cy="1024" rx="250" ry="56" fill="#1b1f26"'
                    f' opacity=".5"/>'
            + teplo(700, 992, 330, 180, .30)
            + _moneta_krupno(700, 992, 176, t, .2, True, True, .74)
            + f'<path d="M520,1056 Q700,1030 886,1058" fill="none"'
              f' stroke="#cfe4f5" stroke-width="7" opacity=".3"/>')

    # мужчина в шляпе с газетой
    mx_, my_, mh_ = 1480, 800, 500
    gz = 6 * A.w(t, 1.1, .2)
    muz = figura(mx_, my_, mh_, t, col="#3a3a46", kant="#ffd98a", ph=.3)
    r1, (g1x, g1y), (m1x, m1y) = _ruka_ekr(mx_, my_, mh_, 1, mh_ * .40, 46, t, "#3a3a46",
                                           "#ffd98a", .2, 4)
    r2, (g2x, g2y), (m2x, m2y) = _ruka_ekr(mx_, my_, mh_, -1, mh_ * .40, 134, t, "#3a3a46",
                                           "#ffd98a", .6, 4)
    muz += r1 + r2
    gcx = (g1x + g2x) / 2
    gcy = (g1y + g2y) / 2
    gcy += 46
    muz += (f'<g transform="rotate({gz:.1f} {gcx:.0f} {gcy:.0f})">'
            f'<path d="M{gcx-92:.0f},{gcy-70:.0f} L{gcx:.0f},{gcy-60:.0f}'
            f' L{gcx+92:.0f},{gcy-70:.0f} L{gcx+92:.0f},{gcy+62:.0f}'
            f' L{gcx:.0f},{gcy+72:.0f} L{gcx-92:.0f},{gcy+62:.0f} Z"'
            f' fill="#ddd8c8" {o(5)}/>'
            f'<line x1="{gcx:.0f}" y1="{gcy-60:.0f}" x2="{gcx:.0f}" y2="{gcy+72:.0f}"'
            f' stroke="#a8a294" stroke-width="5"/>')
    for i in range(5):
        muz += (f'<path d="M{gcx-78:.0f},{gcy-42+i*24:.0f}'
                f' Q{gcx-42:.0f},{gcy-50+i*24:.0f} {gcx-12:.0f},{gcy-40+i*24:.0f}'
                f' M{gcx+12:.0f},{gcy-40+i*24:.0f} Q{gcx+46:.0f},{gcy-50+i*24:.0f}'
                f' {gcx+78:.0f},{gcy-42+i*24:.0f}" fill="none" stroke="#9aa0a4"'
                f' stroke-width="4"/>')
    muz += "</g>"
    muz += (f'<path d="M{mx_-66:.0f},{my_-mh_*.88:.0f} Q{mx_:.0f},{my_-mh_*1.04:.0f}'
            f' {mx_+66:.0f},{my_-mh_*.88:.0f} Z" fill="#2a2a34" {o(5)}/>'
            f'<rect x="{mx_-96:.0f}" y="{my_-mh_*.90:.0f}" width="192" height="20"'
            f' rx="9" fill="#2a2a34" {o(4)}/>')
    muz += (f'<line x1="{mx_-26:.0f}" y1="{my_-mh_*.24:.0f}" x2="{mx_-70:.0f}"'
            f' y2="{my_+200:.0f}" stroke="#3a3a46" stroke-width="40"'
            f' stroke-linecap="round"/>'
            f'<line x1="{mx_+26:.0f}" y1="{my_-mh_*.24:.0f}" x2="{mx_+30:.0f}"'
            f' y2="{my_+200:.0f}" stroke="#3a3a46" stroke-width="40"'
            f' stroke-linecap="round"/>')
    s += SL(Z_SRED, muz)

    # женщина с зонтом-тростью проходит мимо
    hod = (t * .30) % 1.0
    fx, fy, fh = 1560 - 560 * hod, 1056, 580
    zh = figura(fx, fy, fh, t, col="#4a3f52", kant="#cfe4f5", platok=False, ph=.5)
    r3, (zx2, zy2), (z1x, z1y) = _ruka_ekr(fx, fy, fh, 1, fh * .42, 84, t, "#4a3f52", "#cfe4f5",
                                           .1, 6)
    r4, (sx3, sy3), (z2x, z2y) = _ruka_ekr(fx, fy, fh, -1, fh * .36, -46, t, "#4a3f52",
                                           "#cfe4f5", .5, 4)
    zh += r3 + r4
    stuk = 8 * abs(math.sin(hod * 6.283 * 2))
    zh += (f'<line x1="{zx2:.0f}" y1="{zy2:.0f}" x2="{zx2+14:.0f}"'
           f' y2="{fy+6-stuk:.0f}" stroke="#2e2a36" stroke-width="15"'
           f' stroke-linecap="round"/>'
           f'<path d="M{zx2-10:.0f},{zy2-6:.0f} Q{zx2-44:.0f},{zy2-30:.0f}'
           f' {zx2-40:.0f},{zy2+6:.0f}" fill="none" stroke="#2e2a36"'
           f' stroke-width="13"/>')
    # шарф
    zh += (f'<path d="M{fx-54:.0f},{fy-fh*.72:.0f} Q{fx:.0f},{fy-fh*.64:.0f}'
           f' {fx+54:.0f},{fy-fh*.72:.0f} L{fx+46:.0f},{fy-fh*.56:.0f}'
           f' Q{fx:.0f},{fy-fh*.48:.0f} {fx-46:.0f},{fy-fh*.56:.0f} Z"'
           f' fill="#8a4a4a" {o(4)}/>'
           f'<path d="M{fx+30:.0f},{fy-fh*.58:.0f} L{fx+54:.0f},{fy-fh*.30:.0f}'
           f' L{fx+16:.0f},{fy-fh*.32:.0f} Z" fill="#8a4a4a" {o(3)}/>')
    zh += para_izo_rta(fx + 44, fy - fh * .80, t, .2, 1.0, .5)
    s += SL(Z_SRED, zh + ten(fx, fy + 8, 110, 20, .45))
    s += SL(Z_SRED, _gorodskoy_hlam(60, 1076, 380, t, 215, ["stolbik", "yaschik"]))
    s += SL(Z_SRED, _gorodskoy_hlam(1560, 1076, 360, t, 217, ["kust", "stolbik"]))
    s += SL(Z_LETIT, mokryy_sneg(t, 18, 33, .45, .8))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def chuzhoy_venik_u_vhoda(t):
    """Порог избы снаружи: поперёк него лежит чужой веник НА ПОЛ-КАДРА —
    растрёпанный, с красной тряпицей на ручке. Рядом скребок для обуви,
    половик, кадка. Хозяйка стоит в дверях, держится за косяк, отдёргивает
    протянутую руку и отступает на шаг внутрь."""
    rnd = random.Random(130)
    s = nebo("sumer", t, True, 61)
    s += oblaka(t, 120, 4, 51, .36)
    s += SL(Z_DAL, _derevnya_ryad(470, t, 219, ((130, 300), (1830, 280))))
    s += SL(Z_DAL, brevna(230, 0, 1480, 760, 94)
            + f'<rect x="230" y="0" width="1480" height="760" fill="none" {o(10)}/>')
    s += SL(Z_DAL, okno_izby(1420, 120, 320, 270, t, svet=True)
            + teplo(1580, 256, 280, 230, .44))
    s += SL(Z_DAL, _polka_s_utvaryu(240, 180, 440, t, 221, 3))
    s += SL(Z_DAL, _stennoe_hozyaystvo(240, 330, t, 223))
    s += SL(Z_DAL, dym(1620, 140, t, 5, .26, 280, .34, "#d3dae2", .9))

    # дверной проём с косяком, внутри тепло
    dx_, dy_, dw, dh = 760, 200, 420, 560
    s += SL(Z_SRED, f'<rect x="{dx_-40:.0f}" y="{dy_-40:.0f}" width="{dw+80:.0f}"'
                    f' height="{dh+60:.0f}" rx="10" fill="#3b2a1a" {o(7)}/>'
                    f'<rect x="{dx_:.0f}" y="{dy_:.0f}" width="{dw:.0f}"'
                    f' height="{dh:.0f}" fill="#1c1510" {o(5)}/>'
                    f'<ellipse cx="{dx_+dw*.5:.0f}" cy="{dy_+dh*.62:.0f}" rx="200"'
                    f' ry="200" fill="#ffd98a" opacity=".16"/>')
    # ДВЕРЬ НА ПЕТЛЯХ, А КРЮК И ЦЕПОЧКА — НА ОПОРЕ. Осмотр 15.11: «синяя
    # дуга висит без опоры» — крюк и цепочка из `dver()` рисовались правее
    # полотна, по голым брёвнам, и читались дугой, подвешенной в воздухе.
    s += SL(Z_SRED, dver(dx_ + dw - 60, dy_, 380, dh, .0, "url(#derev)", False, False))
    petli = ""
    for py2 in (dy_ + 70, dy_ + dh * .5, dy_ + dh - 90):
        petli += (f'<rect x="{dx_+dw-96:.0f}" y="{py2:.0f}" width="104" height="30"'
                  f' rx="10" fill="{ZHELEZ}" {o(4)}/>'
                  f'<circle cx="{dx_+dw-88:.0f}" cy="{py2+15:.0f}" r="13"'
                  f' fill="#3a4045" {o(3)}/>'
                  f'<circle cx="{dx_+dw-14:.0f}" cy="{py2+15:.0f}" r="8"'
                  f' fill="#3a4045" {o(2)}/>')
    kolx, koly = dx_ + dw + 374, dy_ + dh * .40
    petli += (f'<rect x="{kolx-24:.0f}" y="{koly-30:.0f}" width="48" height="60"'
              f' rx="9" fill="#4a3522" {o(4)}/>'
              f'<circle cx="{kolx:.0f}" cy="{koly:.0f}" r="13" fill="{ZHELEZ}"'
              f' {o(3)}/>'
              f'<path d="M{dx_+dw+316:.0f},{koly-18:.0f} q30,30 {kolx-dx_-dw-316:.0f},18"'
              f' fill="none" stroke="{ZHELEZ}" stroke-width="9"'
              f' stroke-dasharray="5 9" stroke-linecap="round"/>'
              f'<rect x="{dx_+dw+300:.0f}" y="{koly-34:.0f}" width="30" height="34"'
              f' rx="8" fill="{ZHELEZ}" {o(3)}/>')
    s += SL(Z_SRED, petli)
    # подкова прибита к НАЩЕЛЬНИКУ над дверью, а не парит над проёмом
    s += SL(Z_SRED, f'<rect x="{dx_+dw*.5-120:.0f}" y="{dy_-104:.0f}" width="240"'
                    f' height="38" rx="9" fill="#5b4428" {o(5)}/>'
            + podkova(dx_ + dw * .5, dy_ - 74, 1.6, t))

    zem = f'<rect x="0" y="760" width="{W}" height="320" fill="#473626"/>'
    zem += _zemlya_faktura(820, 1060, 225, 14)
    zem += _listya(227, 26, 800, 1060)
    zem += _inej(229, 30, 800, 1060)
    s += SL(Z_SRED, zem)
    # порог и крыльцо
    s += SL(Z_SRED, f'<rect x="{dx_-80:.0f}" y="760" width="{dw+160:.0f}" height="46"'
                    f' rx="10" fill="#5b4428" {o(6)}/>'
                    f'<rect x="{dx_-120:.0f}" y="806" width="{dw+240:.0f}" height="36"'
                    f' rx="9" fill="url(#derev)" {o(5)}/>'
                    f'<rect x="{dx_-160:.0f}" y="842" width="{dw+320:.0f}" height="36"'
                    f' rx="9" fill="url(#derev)" {o(5)}/>')

    # ЧУЖОЙ ВЕНИК ЛЕЖИТ ПОПЕРЁК ПОРОГА — ПРУТЬЯМИ ВЕЕРОМ И С ПЕРЕВЯЗЬЮ.
    # Осмотр 15.11: «бесформенный жёлтый пучок» — разброс прутьев стоял на
    # 1.0 и веер рассыпался в пятно, а тон #8a7246 сливался с землёй.
    # Теперь разброс 0.24, прутья светлые по тёмному комлю, две перевязи.
    ven = (f'<g transform="rotate(-84 700 940)">'
           + _venik(700, 1104, 620, t, "#c2a45e", "#b8352c", False, .24, .0, 1.5, 231))
    for i, (ky2, kw2, kc) in enumerate(((.50, 104, "#b8352c"), (.40, 92, "#6a4a26"),
                                        (.30, 84, "#8a6a3c"))):
        ven += (f'<rect x="{700-kw2*.5:.0f}" y="{1104-620*ky2:.0f}" width="{kw2:.0f}"'
                f' height="26" rx="10" fill="{kc}" {o(4)}/>')
    ven += (f'<path d="M{700-150:.0f},{1104-620+28:.0f} Q700,{1104-620-34:.0f}'
            f' {700+150:.0f},{1104-620+28:.0f}" fill="none" stroke="#8a6a3c"'
            f' stroke-width="8" opacity=".55"/></g>')
    s += SL(Z_SRED, ven)
    # скребок, половик, кадка
    s += SL(Z_SRED, f'<path d="M520,900 L700,900 L700,870 L520,870 Z" fill="{ZHELEZ}"'
                    f' {o(5)}/>'
                    f'<rect x="508" y="896" width="30" height="80" rx="8"'
                    f' fill="#3a4045" {o(4)}/>'
                    f'<rect x="682" y="896" width="30" height="80" rx="8"'
                    f' fill="#3a4045" {o(4)}/>')
    s += SL(Z_SRED, f'<path d="M1240,906 L1660,906 L1720,992 L1180,992 Z" fill="{RUSH}"'
                    f' {o(5)}/>'
                    f'<path d="M1222,936 L1686,936 M1204,966 L1704,966" stroke="{KRAS}"'
                    f' stroke-width="9" opacity=".65"/>')
    s += SL(Z_SRED, _dvorovaya_utvar(220, 1056, 420, t, 233, ["kadka", "vedro"]))
    s += SL(Z_SRED, _kadushki_i_grabli(1480, 1070, t, 235))

    # хозяйка в дверях: левой за косяк, правую прижимает к груди, отступает
    otst = A.ease(A.seg(t, 1.4, 1.0))
    fx, fy, fh = 1040 + 70 * otst, 790, 560
    hoz = figura(fx, fy, fh, t, col="#4a3b2a", kant="#ffd98a", platok=True, ph=.2,
                 naklon=5 * otst)
    r1, _, (h1x, h1y) = _ruka_ekr(fx, fy, fh, 1, fh * (.46 - .22 * otst), 118 - 76 * otst, t,
                                  "#4a3b2a", "#ffd98a", .1, 6)
    r2, _, (h2x, h2y) = _ruka_ekr(fx, fy, fh, -1, fh * .40, -158, t, "#4a3b2a", "#ffd98a", .5, 4)
    hoz += r1 + r2
    hoz += (f'<path d="M{fx-56:.0f},{fy-fh*.62:.0f} L{fx+56:.0f},{fy-fh*.62:.0f}'
            f' L{fx+74:.0f},{fy-fh*.16:.0f} L{fx-74:.0f},{fy-fh*.16:.0f} Z"'
            f' fill="#9a8c70" opacity=".92" {o(4)}/>')
    hoz += para_izo_rta(fx + 46, fy - fh * .80, t, .3, 1.0, .5)
    s += SL(Z_SRED, hoz + ten(fx, fy + 8, 110, 20, .45))
    s += SL(Z_PERED, _stolb_pered(-6, 96, "#1d1611", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 35, .4, .7))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def svoy_venik_i_svoi_ugly(t):
    """Горница сверху, как план: четыре угла, печь, стол, лавки, прялка.
    Хозяйка держит свой тёмный веник обеими руками и метёт от угла к порогу,
    из каждого угла тянется дорожка сора. В дверь просовывается чужой веник,
    и с него сыплется чужой сор."""
    rnd = random.Random(131)
    s = f'<rect width="{W}" height="{H}" fill="#2a2018"/>'
    # план горницы: пол досками в перспективе «сверху»
    s += SL(Z_DAL, f'<path d="M260,120 L1660,120 L1880,1020 L40,1020 Z"'
                   f' fill="url(#pol)" {o(8)}/>')
    for i in range(13):
        p = i / 12.0
        s += SL(Z_DAL, f'<line x1="{260+1400*p:.0f}" y1="120"'
                       f' x2="{40+1840*p:.0f}" y2="1020" stroke="#4a3522"'
                       f' stroke-width="6" opacity=".55"/>')
    # стены по периметру
    s += SL(Z_DAL, f'<path d="M260,120 L1660,120 L1700,40 L220,40 Z" fill="url(#brev)"'
                   f' {o(6)}/>'
                   f'<path d="M260,120 L40,1020 L-40,1020 L160,60 Z" fill="url(#brev)"'
                   f' {o(6)}/>'
                   f'<path d="M1660,120 L1880,1020 L1960,1020 L1760,60 Z"'
                   f' fill="url(#brev)" {o(6)}/>')
    # печь в дальнем левом углу
    s += SL(Z_SRED, pech(250, 120, 330, 400, t, True, True, False))
    s += SL(Z_SRED, teplo(400, 380, 360, 300, .42))
    s += SL(Z_SRED, dym(400, 130, t, 4, .26, 230, .3, "#d3dae2", .8))
    # стол, лавки, прялка по углам
    s += SL(Z_SRED, stol(1180, 540, 460, 30))
    s += SL(Z_SRED, _lavka_krupno(760, 620, 420, t, 130))
    s += SL(Z_SRED, _lavka_krupno(1420, 760, 420, t, 140))
    s += SL(Z_SRED, krynka(1180, 520, 1.2) + karavay(1300, 522, 1.0, True))
    prx, pry = 1660, 420
    s += SL(Z_SRED, f'<rect x="{prx-90:.0f}" y="{pry-26:.0f}" width="190" height="30"'
                    f' rx="10" fill="url(#dosk)" {o(5)}/>'
                    f'<rect x="{prx-14:.0f}" y="{pry-320:.0f}" width="30" height="300"'
                    f' rx="11" fill="url(#derev)" {o(5)}/>'
                    f'<ellipse cx="{prx+10:.0f}" cy="{pry-360:.0f}" rx="66" ry="50"'
                    f' fill="url(#solom)" opacity=".92" {o(5)}/>')
    s += SL(Z_SRED, mebel_hlam(180, 980, 380, t, 31))
    s += SL(Z_SRED, _kot_zhivoy(1740, 960, t, 1.35, "#4a423c", .6, True, True))
    s += SL(Z_SRED, _polenica(300, 540, 260, 220, 295, 24))
    s += SL(Z_SRED, _dvorovaya_utvar(560, 900, 420, t, 297,
                                     ["kadka", "korzina", "vedro"]))
    s += SL(Z_SRED, _polka_s_utvaryu(760, 300, 420, t, 299, 4))
    s += SL(Z_SRED, _polka_s_utvaryu(1060, 380, 420, t, 369, 4))
    s += SL(Z_SRED, _lavka_krupno(560, 470, 420, t, 130))
    s += SL(Z_SRED, _dvorovaya_utvar(620, 960, 560, t, 371,
                                     ["korzina", "vedro", "korob"]))
    s += SL(Z_SRED, _listya(373, 24, 880, 1000))
    s += SL(Z_SRED, utvar_izby(1240, 260, 400, t, 33))
    s += SL(Z_SRED, f'<path d="M620,700 L1320,700 L1420,900 L520,900 Z" fill="{RUSH}"'
                    f' {o(5)}/>'
                    f'<path d="M600,760 L1350,760 M576,820 L1382,820" stroke="{KRAS}"'
                    f' stroke-width="9" opacity=".6"/>')
    s += SL(Z_SRED, f'<rect x="1440" y="200" width="300" height="140" rx="10"'
                    f' fill="url(#derev)" {o(6)}/>'
                    f'<path d="M1440,200 Q1590,146 1740,200 Z" fill="#5b4428" {o(5)}/>'
                    f'<rect x="1430" y="236" width="320" height="18" rx="7"'
                    f' fill="{ZHELEZ}" {o(3)}/>')

    # дорожки сора из каждого угла к порогу
    sor = ""
    uglov = ((300, 200), (1620, 200), (120, 960), (1820, 960))
    for i, (ux, uy) in enumerate(uglov):
        for k in range(11):
            p = k / 10.0
            sx_ = ux + (960 - ux) * p + 30 * math.sin(p * 6 + i)
            sy_ = uy + (1000 - uy) * p
            r = 7 + (1 - p) * 9
            sor += (f'<ellipse cx="{sx_:.0f}" cy="{sy_:.0f}" rx="{r:.0f}"'
                    f' ry="{r*.6:.0f}" fill="{["#8a7a58","#6b5a3c","#9a8c70"][k%3]}"'
                    f' opacity=".9"/>')
            if k % 3 == 0:
                sor += (f'<line x1="{sx_-16:.0f}" y1="{sy_-6:.0f}" x2="{sx_+14:.0f}"'
                        f' y2="{sy_+8:.0f}" stroke="#7a6a48" stroke-width="4"/>')
    s += SL(Z_SRED, sor)

    # хозяйка метёт от угла к порогу
    mah = A.ease(abs(A.w(t, 1.6, .0)))
    fx, fy, fh = 700, 900, 460
    hoz = figura(fx, fy, fh, t, col="#4a3b2a", kant="#ffd98a", platok=True, ph=.2,
                 naklon=14 * mah)
    r1, (v1x, v1y), (h1x, h1y) = _ruka_ekr(fx, fy, fh, 1, fh * .50, 36 + 30 * mah, t, "#4a3b2a",
                                           "#ffd98a", .1, 5)
    r2, _, (h2x, h2y) = _ruka_ekr(fx, fy, fh, -1, fh * .46, 56 + 26 * mah, t, "#4a3b2a",
                                  "#ffd98a", .5, 5)
    hoz += r1 + r2
    hoz += _venik_v_ruke(v1x, v1y, 280, t, "#4b3f28", "#5a4a2e",
                         104 - 30 * mah, .9, 237, .25, .7)
    # подол и платок отклоняются по ходу взмаха
    hoz += (f'<path d="M{fx-80:.0f},{fy-fh*.30:.0f} Q{fx+30*mah:.0f},{fy-fh*.10:.0f}'
            f' {fx+90:.0f},{fy-fh*.28:.0f} L{fx+74:.0f},{fy-4:.0f}'
            f' L{fx-74:.0f},{fy-4:.0f} Z" fill="#4a3b2a" {o(5)}/>')
    s += SL(Z_SRED, hoz)

    # чужой веник просовывается в дверь, сыплется чужой сор
    dv = A.ease(A.seg(t, 3.0, 1.2))
    s += SL(Z_SRED, f'<rect x="820" y="1004" width="300" height="76" rx="10"'
                    f' fill="#2a1d12" {o(6)}/>'
                    f'<rect x="800" y="986" width="340" height="26" rx="9"'
                    f' fill="#5b4428" {o(5)}/>')
    s += SL(Z_SRED, f'<g transform="rotate(176 970 1040)">'
                    + _venik(970, 1040 + 300 * (1 - dv), 360, t, "#8a7246", "#b8352c",
                             False, 1.0, .3, 1.0, 239) + "</g>")
    chuz = ""
    for i in range(10):
        p = ((t * .7 + i * .1) % 1.0)
        cx_ = 880 + i * 22
        cy_ = 960 + 110 * p
        if i % 4 == 0:                           # рассерженная рожица
            chuz += (f'<circle cx="{cx_:.0f}" cy="{cy_:.0f}" r="22" fill="#c86a4a"'
                     f' opacity="{(1-p)*dv:.2f}" {o(3)}/>'
                     f'<path d="M{cx_-10:.0f},{cy_+8:.0f} Q{cx_:.0f},{cy_-2:.0f}'
                     f' {cx_+10:.0f},{cy_+8:.0f}" fill="none" stroke="#3a1c14"'
                     f' stroke-width="4" opacity="{(1-p)*dv:.2f}"/>'
                     f'<path d="M{cx_-12:.0f},{cy_-10:.0f} L{cx_-2:.0f},{cy_-4:.0f}'
                     f' M{cx_+12:.0f},{cy_-10:.0f} L{cx_+2:.0f},{cy_-4:.0f}"'
                     f' stroke="#3a1c14" stroke-width="4"'
                     f' opacity="{(1-p)*dv:.2f}"/>')
        elif i % 4 == 1:                         # чужая пуговица
            chuz += (f'<circle cx="{cx_:.0f}" cy="{cy_:.0f}" r="14" fill="#e8e2d2"'
                     f' opacity="{(1-p)*dv:.2f}" {o(2)}/>')
        else:                                    # чужое письмо
            chuz += (f'<rect x="{cx_-16:.0f}" y="{cy_-12:.0f}" width="32" height="24"'
                     f' rx="4" fill="#f0e8d4" opacity="{(1-p)*dv:.2f}" {o(2)}/>')
    s += SL(Z_SRED, chuz)
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.46)
    return s


def prischurennaya_sosedka(t):
    """Двор и забор: у калитки на земле лежит чужой веник. Хозяйка метёт
    крыльцо своим старым веником, замечает чужой и замирает. Из-за забора
    выглядывает соседка, обе руки на жерди, от прищуренных глаз к венику
    тянется пунктир. Во дворе куры, корыто, поленница."""
    rnd = random.Random(132)
    s = nebo("sumer", t, True, 63)
    s += oblaka(t, 120, 4, 53, .36)
    s += SL(Z_DAL, _derevnya_ryad(430, t, 241, ((140, 330), (1820, 300))))
    s += SL(Z_DAL, brevna(-20, 40, 1040, 700, 92)
            + f'<rect x="-20" y="40" width="1040" height="700" fill="none" {o(9)}/>')
    s += SL(Z_DAL, okno_izby(120, 170, 300, 250, t, svet=True)
            + teplo(270, 296, 260, 210, .44))
    s += SL(Z_DAL, dver(520, 150, 280, 500, .0, "url(#derev)", True, False))
    s += SL(Z_DAL, dym(360, 100, t, 5, .26, 280, .34, "#d3dae2", .9))
    # СТЕННОЕ ХОЗЯЙСТВО ПОДНЯТО НА СТЕНУ. Осмотр 15.11: «белый вытянутый
    # предмет внизу не опознаётся» — это ПИЛА: `_stennoe_hozyaystvo` вешает её
    # на y+320, и при якоре 540 полотно (940-1220 × 860-948, сталь #7e848c)
    # оказывалось на 200 px НИЖЕ бревенчатой стены, прямо на земле, и читалось
    # светлым пятном ни на чём. Якорь 290 — вся снасть внутри стены (40-740).
    s += SL(Z_DAL, _stennoe_hozyaystvo(60, 290, t, 243))

    zem = f'<rect x="0" y="760" width="{W}" height="320" fill="#473626"/>'
    zem += _zemlya_faktura(820, 1060, 245, 14)
    zem += _listya(247, 26, 800, 1060)
    zem += _inej(249, 28, 800, 1060)
    s += SL(Z_SRED, zem)
    s += SL(Z_SRED, _kryl_co(60, 700, 620, 180, t, 3, True, False))

    # забор с соседкой
    s += SL(Z_SRED, _zabor_dosok(880, 470, 1080, 350, 251, 58))
    sx_, sy_ = 1480, 480
    pr = 4 * A.w(t, 2.2, .2)
    sos = (f'<path d="M{sx_-130:.0f},{sy_+40:.0f} Q{sx_-116:.0f},{sy_-70:.0f}'
           f' {sx_-48:.0f},{sy_-110:.0f} L{sx_+48:.0f},{sy_-110:.0f}'
           f' Q{sx_+116:.0f},{sy_-70:.0f} {sx_+130:.0f},{sy_+40:.0f} Z"'
           f' fill="#3d4a3a" {o(5)}/>'
           f'<ellipse cx="{sx_:.0f}" cy="{sy_-80+pr:.0f}" rx="86" ry="96"'
           f' fill="#e8c9a8" {o(5)}/>'
           f'<path d="M{sx_-92:.0f},{sy_-110+pr:.0f} Q{sx_:.0f},{sy_-230+pr:.0f}'
           f' {sx_+92:.0f},{sy_-110+pr:.0f} Q{sx_+70:.0f},{sy_-50+pr:.0f}'
           f' {sx_+86:.0f},{sy_+10+pr:.0f} L{sx_-86:.0f},{sy_+10+pr:.0f}'
           f' Q{sx_-70:.0f},{sy_-50+pr:.0f} {sx_-92:.0f},{sy_-110+pr:.0f} Z"'
           f' fill="#5a2f33" {o(5)}/>'
           f'<ellipse cx="{sx_:.0f}" cy="{sy_-80+pr:.0f}" rx="86" ry="96"'
           f' fill="#e8c9a8" {o(0)}/>'
           f'<path d="M{sx_-96:.0f},{sy_-96+pr:.0f} Q{sx_:.0f},{sy_-236+pr:.0f}'
           f' {sx_+96:.0f},{sy_-96+pr:.0f} Q{sx_+70:.0f},{sy_-132+pr:.0f}'
           f' {sx_:.0f},{sy_-142+pr:.0f} Q{sx_-70:.0f},{sy_-132+pr:.0f}'
           f' {sx_-96:.0f},{sy_-96+pr:.0f} Z" fill="#8a4a6a" {o(5)}/>'
           f'<path d="M{sx_-96:.0f},{sy_-96+pr:.0f} Q{sx_-120:.0f},{sy_-30+pr:.0f}'
           f' {sx_-60:.0f},{sy_+10+pr:.0f} L{sx_-74:.0f},{sy_-52+pr:.0f} Z"'
           f' fill="#8a4a6a" {o(4)}/>'
           f'<path d="M{sx_+96:.0f},{sy_-96+pr:.0f} Q{sx_+120:.0f},{sy_-30+pr:.0f}'
           f' {sx_+60:.0f},{sy_+10+pr:.0f} L{sx_+74:.0f},{sy_-52+pr:.0f} Z"'
           f' fill="#8a4a6a" {o(4)}/>'
           f'<path d="M{sx_-48:.0f},{sy_-96+pr:.0f} Q{sx_-28:.0f},{sy_-108+pr:.0f}'
           f' {sx_-8:.0f},{sy_-96+pr:.0f}" fill="none" stroke="#3a2a22"'
           f' stroke-width="9" stroke-linecap="round"/>'
           f'<path d="M{sx_+8:.0f},{sy_-96+pr:.0f} Q{sx_+28:.0f},{sy_-108+pr:.0f}'
           f' {sx_+48:.0f},{sy_-96+pr:.0f}" fill="none" stroke="#3a2a22"'
           f' stroke-width="9" stroke-linecap="round"/>'
           f'<path d="M{sx_-54:.0f},{sy_-124+pr:.0f} Q{sx_-28:.0f},{sy_-142+pr:.0f}'
           f' {sx_-4:.0f},{sy_-128+pr:.0f} M{sx_+4:.0f},{sy_-128+pr:.0f}'
           f' Q{sx_+28:.0f},{sy_-142+pr:.0f} {sx_+54:.0f},{sy_-124+pr:.0f}"'
           f' fill="none" stroke="#5a4030" stroke-width="7"/>'
           f'<path d="M{sx_-26:.0f},{sy_-44+pr:.0f} Q{sx_:.0f},{sy_-34+pr:.0f}'
           f' {sx_+26:.0f},{sy_-44+pr:.0f}" fill="none" stroke="#9c4a3c"'
           f' stroke-width="7" stroke-linecap="round"/>')
    # обе руки на верхней жерди
    sos += (f'<rect x="{sx_-140:.0f}" y="{sy_+6:.0f}" width="110" height="38" rx="16"'
            f' fill="#5a2f33" {o(4)}/>'
            f'<rect x="{sx_+30:.0f}" y="{sy_+6:.0f}" width="110" height="38" rx="16"'
            f' fill="#5a2f33" {o(4)}/>')
    s += SL(Z_SRED, sos)

    # чужой веник у калитки
    s += SL(Z_SRED, f'<g transform="rotate(96 1240 980)">'
                    + _venik(1240, 1250, 520, t, "#8a7246", "#b8352c", False, 1.0, .2,
                             1.1, 253) + "</g>")
    # пунктир взгляда от глаз к венику
    pun = ""
    for i in range(14):
        p = i / 13.0
        px_ = sx_ - 20 + (1240 - sx_ + 20) * p
        py_ = sy_ - 96 + (980 - sy_ + 96) * p
        mig = max(.0, 1 - abs(((t * .6) % 1.0) - p) * 4.0)
        pun += (f'<circle cx="{px_:.0f}" cy="{py_:.0f}" r="{8+6*mig:.0f}"'
                f' fill="#d8c0a0" opacity="{.30+mig*.5:.2f}"/>')
    s += SL(Z_SRED, pun)

    # хозяйка метёт крыльцо, потом обходит веник по дуге
    mah = A.ease(abs(A.w(t, 1.8, .0)))
    obh = A.ease(A.seg(t, 4.2, 2.0))
    fx, fy, fh = 420 + 420 * obh, 880 + 150 * obh, 540
    hoz = figura(fx, fy, fh, t, col="#4a3b2a", kant="#ffd98a", platok=True, ph=.2,
                 naklon=12 * mah * (1 - obh))
    r1, (v1x, v1y), (h1x, h1y) = _ruka_ekr(fx, fy, fh, 1, fh * .48,
                                           44 + 26 * mah * (1 - obh) - 60 * obh, t, "#4a3b2a",
                                           "#ffd98a", .1, 5)
    r2, _, (h2x, h2y) = _ruka_ekr(fx, fy, fh, -1, fh * .44, 62 - 40 * obh, t, "#4a3b2a",
                                  "#ffd98a", .5, 5)
    hoz += r1 + r2
    hoz += _venik_v_ruke(v1x, v1y, 300, t, "#4b3f28", "#5a4a2e",
                         102 - 26 * mah * (1 - obh) + 22 * obh, .95, 255, .25, .7)
    hoz += para_izo_rta(fx + 46, fy - fh * .80, t, .3, 1.0, .5)
    s += SL(Z_SRED, hoz + ten(fx, fy + 8, 110, 20, .45))

    # куры разбегаются, корыто, поленница
    # КУРЫ РЯБЫЕ, А НЕ БЕЛЫЕ: сливочный #e2d6c2 на буром дворе читался
    # батоном или костью (осмотр 15.11). Теперь у каждой свой тон и размер.
    for i, kcol in enumerate(("#b9a88c", "#8a7a62", "#c2a882", "#9a8468")):
        kp = ((t * .55 + i * .22) % 1.0)
        s += SL(Z_SRED, kura(300 + i * 150 + 220 * kp,
                             1050 - 30 * abs(A.w(t, 1.2, i * .3)),
                             t, 1.18 + .14 * (i % 2), i * .25, kcol))
    s += SL(Z_SRED, f'<path d="M700,1070 Q760,990 900,990 L1100,990 Q1180,1056'
                    f' 1140,1076 Z" fill="url(#derev)" {o(6)}/>'
                    f'<ellipse cx="920" cy="996" rx="200" ry="30" fill="#5b4428"'
                    f' {o(4)}/>')
    s += SL(Z_SRED, _polenica(1620, 780, 320, 270, 257, 26))
    s += SL(Z_SRED, _dvorovaya_utvar(700, 880, 420, t, 301, ["kadka", "korzina"]))
    s += SL(Z_SRED, goloe_derevo(1180, 800, 420, t, 303, 8, "#2a2b33", True))
    s += SL(Z_SRED, _kadushki_i_grabli(260, 1070, t, 305))
    s += SL(Z_PERED, _stolb_pered(1880, 90, "#1d1611", 0, H))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 37, .4, .7))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def venik_i_dlinnaya_palka(t):
    """Крыльцо современного дома с ковриком и фонарём, у нижней доски лежит
    чужой веник. Хозяин в куртке и резиновых сапогах стоит на земле и обеими
    руками держит длинную лыжную палку, как клюшку, и её концом отодвигает
    веник к калитке. Рядом лопата, лейка, собачья миска."""
    rnd = random.Random(133)
    s = nebo("sumer", t, True, 67)
    s += oblaka(t, 120, 4, 55, .36)
    s += SL(Z_DAL, goloe_derevo(1700, 560, 480, t, 33, 9, "#2a2b33", False)
            + goloe_derevo(240, 540, 380, t, 35, 7, "#2a2b33", False))
    # дом: сайдинг, окно со светом
    s += SL(Z_SRED, doski(300, 60, 1120, 660, 72, False, "dosk"))
    s += SL(Z_SRED, f'<rect x="300" y="60" width="1120" height="660" fill="none"'
                    f' {o(9)}/>')
    s += SL(Z_SRED, okno_izby(1060, 160, 300, 250, t, svet=True)
            + teplo(1210, 286, 270, 220, .44))
    s += SL(Z_SRED, f'<rect x="560" y="180" width="300" height="540" rx="8"'
                    f' fill="#5e4a3a" {o(6)}/>'
                    f'<rect x="586" y="210" width="248" height="230" rx="6"'
                    f' fill="#7d6a48" {o(4)}/>'
                    f'<rect x="586" y="470" width="248" height="230" rx="6"'
                    f' fill="#7d6a48" {o(4)}/>'
                    f'<rect x="812" y="430" width="22" height="70" rx="9"'
                    f' fill="{ZHELEZ}" {o(3)}/>')
    # фонарь у двери
    fg = .6 + .4 * abs(A.w(t, 2.4, .2))
    s += SL(Z_SRED, f'<rect x="900" y="200" width="22" height="80" fill="#3a4045"'
                    f' {o(3)}/>'
                    f'<path d="M880,280 L944,280 L930,370 L894,370 Z" fill="#3a4045"'
                    f' {o(5)}/>'
                    f'<path d="M888,288 L936,288 L924,362 L900,362 Z" fill="#ffd98a"'
                    f' opacity="{fg:.2f}"/>'
                    f'<circle cx="912" cy="326" r="90" fill="#ffd98a"'
                    f' opacity="{fg*.22:.2f}"/>')

    zem = f'<rect x="0" y="790" width="{W}" height="290" fill="#473626"/>'
    zem += _zemlya_faktura(840, 1060, 259, 14)
    zem += _listya(261, 26, 830, 1060)
    s += SL(Z_SRED, zem)
    s += SL(Z_SRED, _kryl_co(540, 720, 420, 150, t, 3, True, False))
    s += SL(Z_SRED, f'<rect x="590" y="690" width="320" height="42" rx="8"'
                    f' fill="#4a5055" {o(5)}/>')
    for i in range(9):
        s += SL(Z_SRED, f'<line x1="{600+i*35:.0f}" y1="694" x2="{600+i*35:.0f}"'
                        f' y2="728" stroke="#2f3338" stroke-width="7"/>')
    # калитка справа
    s += SL(Z_SRED, _zabor_dosok(1560, 640, 400, 300, 263, 58, "#3f5a46"))

    # чужой веник едет к калитке
    ed = A.ease(A.seg(t, .4, 2.2))
    vx_ = 980 + 520 * ed
    s += SL(Z_SRED, f'<g transform="rotate(92 {vx_:.0f} 940)">'
                    + _venik(vx_, 1200, 480, t, "#8a7246", "#b8352c", False, 1.0, .2,
                             1.0, 265) + "</g>")

    # хозяин с длинной палкой
    fx, fy, fh = 560, 1030, 580
    # ГАММА ТЁПЛАЯ, КАК ВЕСЬ ВЕЧЕР: фигура была бирюзовой (#2f4a52) и выпадала
    # из кадра, палка — холодной сталью (осмотр 15.11)
    hoz = figura(fx, fy, fh, t, col="#5a3f2e", kant="#ffd98a", ph=.2, shapka=True,
                 naklon=-8)
    # палка ОДНОЙ рукой, от правого плеча наружу; левая просто висит вниз —
    # прежде на её конце болтался кулак, которому палку взять было неоткуда
    r1, (p1x, p1y), (h1x, h1y) = _ruka(fx, fy, fh, 1, fh * .36, 26, t, "#5a3f2e",
                                       "#ffd98a", .1, 3)
    r2, (p2x, p2y), (h2x, h2y) = _ruka(fx, fy, fh, -1, fh * .30, 80, t, "#5a3f2e",
                                       "#ffd98a", .5, 3)
    hoz += r1 + r2
    # хват: ближний кулак на конце палки, дальний чуть выше по ней
    # палка начинается ОТСТУПИВ от кисти и светлее пальто: при тоне, близком
    # к одежде, рукав и палка сливались в один брусок «из груди» (осмотр 15.11)
    pal_x0, pal_y0 = p1x + 44, p1y + 16
    # длина палки ограничена 340 px: прежде она тянулась на 520 и доходила
    # почти до края кадра (осмотр 15.11)
    _pdx, _pdy = (vx_ - 90) - pal_x0, 968 - pal_y0
    _pk = min(1.0, 340.0 / max(1.0, math.hypot(_pdx, _pdy)))
    pal_x1, pal_y1 = pal_x0 + _pdx * _pk, pal_y0 + _pdy * _pk
    hoz += (f'<line x1="{pal_x0:.0f}" y1="{pal_y0:.0f}" x2="{pal_x1:.0f}"'
            f' y2="{pal_y1:.0f}" stroke="#b08a52" stroke-width="17"'
            f' stroke-linecap="round"/>'
            f'<line x1="{pal_x0:.0f}" y1="{pal_y0:.0f}" x2="{pal_x1:.0f}"'
            f' y2="{pal_y1:.0f}" stroke="#e8cf96" stroke-width="5" opacity=".55"/>'
            f'<circle cx="{pal_x1:.0f}" cy="{pal_y1:.0f}" r="25" fill="none"'
            f' stroke="#b08a52" stroke-width="9"/>'
            f'<rect x="{pal_x0-22:.0f}" y="{pal_y0-28:.0f}" width="44" height="56"'
            f' rx="15" fill="#3a2b20" {o(5)}/>'
            f'<path d="M{pal_x0-16:.0f},{pal_y0-14:.0f} l32,6'
            f' M{pal_x0-16:.0f},{pal_y0+2:.0f} l32,6'
            f' M{pal_x0-16:.0f},{pal_y0+18:.0f} l32,6" stroke="#6a5438"'
            f' stroke-width="5" opacity=".9"/>')
    # резиновые сапоги
    hoz += (f'<path d="M{fx-56:.0f},{fy-fh*.26:.0f} L{fx-10:.0f},{fy-fh*.26:.0f}'
            f' L{fx-10:.0f},{fy-6:.0f} L{fx-70:.0f},{fy-6:.0f} Z" fill="#3a2f26"'
            f' {o(5)}/>'
            f'<path d="M{fx+12:.0f},{fy-fh*.26:.0f} L{fx+58:.0f},{fy-fh*.26:.0f}'
            f' L{fx+72:.0f},{fy-6:.0f} L{fx+12:.0f},{fy-6:.0f} Z" fill="#3a2f26"'
            f' {o(5)}/>')
    hoz += para_izo_rta(fx + 46, fy - fh * .80, t, .2, 1.0, .5)
    s += SL(Z_SRED, hoz + ten(fx, fy + 8, 120, 22, .45))

    # лопата, лейка, собачья миска, пёс нюхает веник и отходит
    s += SL(Z_SRED, f'<line x1="200" y1="700" x2="236" y2="1020" stroke="url(#derev)"'
                    f' stroke-width="20" stroke-linecap="round"/>'
                    f'<path d="M206,1016 L280,1030 L264,1076 L190,1062 Z"'
                    f' fill="url(#zhel)" {o(5)}/>'
                    f'<path d="M340,1070 L340,956 L470,956 L470,1070 Z" fill="#4a7a6a"'
                    f' {o(5)}/>'
                    f'<path d="M470,990 L560,940 L566,966 L478,1014 Z" fill="#4a7a6a"'
                    f' {o(4)}/>'
                    f'<path d="M352,956 Q404,900 456,956" fill="none" stroke="#4a7a6a"'
                    f' stroke-width="11"/>'
                    f'<ellipse cx="1180" cy="1060" rx="78" ry="26" fill="#5e656a"'
                    f' {o(4)}/>')
    nn = (t * .34) % 1.0
    px3 = 1340 - 180 * max(.0, nn - .5) * 2
    s += SL(Z_SRED, f'<ellipse cx="{px3:.0f}" cy="1010" rx="98" ry="44"'
                    f' fill="#6b5236" {o(4)}/>'
                    f'<ellipse cx="{px3+86:.0f}" cy="986" rx="44" ry="38"'
                    f' fill="#6b5236" {o(4)}/>'
                    f'<path d="M{px3+112:.0f},966 L{px3+126:.0f},922'
                    f' L{px3+86:.0f},946 Z" fill="#54402a" {o(3)}/>'
                    f'<circle cx="{px3+100:.0f}" cy="982" r="5" fill="#120c08"/>'
                    f'<path d="M{px3-90:.0f},994 Q{px3-140:.0f},'
                    f'{950-16*A.w(t,1.3,.2):.0f} {px3-154:.0f},1004" fill="none"'
                    f' stroke="#6b5236" stroke-width="15" stroke-linecap="round"/>')
    s += SL(Z_SRED, _gorodskoy_hlam(1180, 1072, 420, t, 307, ["yaschik", "kust"]))
    s += SL(Z_SRED, _polenica(60, 700, 220, 260, 309, 24))
    s += SL(Z_SRED, _dvorovaya_utvar(700, 1072, 420, t, 311, ["kadka", "korob"]))
    s += SL(Z_PERED, _vetka_pered(2020, 60, 720, 160, t, 267, "#241c16", 6))
    s += SL(Z_LETIT, mokryy_sneg(t, 16, 39, .4, .7))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def lestnichnaya_ploschadka_s_dvumya_d(t):
    """Лестничная площадка, две двери, между ними велосипед, коврики, детская
    коляска. В проёме открытой двери соседки виден настоящий кадр: веник
    метёт пол. Соседка протягивает швабру и веник, хозяйка обеими ладонями
    показывает «нет». У неё за спиной новые веник и швабра в упаковке."""
    rnd = random.Random(134)
    pol = 860
    s = f'<rect width="{W}" height="{H}" fill="#3a4046"/>'
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="{pol:.0f}" fill="#58646a"/>'
                   f'<rect x="0" y="{pol-300:.0f}" width="{W}" height="300"'
                   f' fill="#6e7a80" opacity=".9"/>'
                   f'<rect x="0" y="{pol-314:.0f}" width="{W}" height="22"'
                   f' fill="#3e484e" opacity=".9"/>'
                   f'<rect x="0" y="{pol-20:.0f}" width="{W}" height="34"'
                   f' fill="#2f383c" opacity=".9"/>')
    # плитка пола
    sh = ""
    yy, ry = pol + 14, 0
    while yy < H:
        step = 130 + (yy - pol) * .5
        xx = -((ry % 2) * step / 2)
        while xx < W:
            sh += (f'<rect x="{xx:.0f}" y="{yy:.0f}" width="{step:.0f}"'
                   f' height="{step*.5:.0f}" fill="{["#6a6258","#4e4a42"][ry%2]}"'
                   f' opacity=".85"/>')
            xx += step * 2
        yy += step * .5
        ry += 1
    s += SL(Z_DAL, sh)
    s += SL(Z_SRED, tusklaya_lampochka(960, 60, t, 1.6, True))
    s += SL(Z_SRED, teplo(960, 280, 400, 300, .32))
    # перила лестницы справа
    s += SL(Z_SRED, f'<path d="M1700,520 L1960,400 L1960,440 L1700,560 Z"'
                    f' fill="#5e4a3a" {o(5)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="{1716+i*58:.0f}" y1="{548-i*26:.0f}"'
                        f' x2="{1716+i*58:.0f}" y2="{880-i*26:.0f}" stroke="{ZHELEZ}"'
                        f' stroke-width="9"/>')

    # закрытая дверь хозяйки слева
    s += SL(Z_SRED, f'<rect x="120" y="190" width="380" height="670" rx="8"'
                    f' fill="#5e4a3a" {o(7)}/>'
                    f'<rect x="150" y="224" width="320" height="270" rx="6"'
                    f' fill="#7d6a48" {o(4)}/>'
                    f'<rect x="150" y="524" width="320" height="300" rx="6"'
                    f' fill="#7d6a48" {o(4)}/>'
                    f'<rect x="440" y="500" width="24" height="76" rx="10"'
                    f' fill="{ZHELEZ}" {o(3)}/>'
                    f'<circle cx="300" cy="200" r="20" fill="#c9b78e" {o(3)}/>')

    # открытая дверь соседки: нарисованный вид, метка, косяк поверх
    px_, py_, pw_, ph_ = 980, 290, 900, 570
    put = kontur_proema(px_, py_, pw_, ph_, "pryam")
    vid = (f'<path d="{put}" fill="#4e4236"/>')
    for i in range(9):
        vid += (f'<rect x="{px_:.0f}" y="{py_+40+i*58:.0f}" width="{pw_:.0f}"'
                f' height="48" fill="url(#dosk)" opacity=".9"/>')
    s += SL(Z_SRED, vid + mesto_stoka(px_, py_, pw_, ph_, "pryam")
            + f'<rect x="{px_-46:.0f}" y="{py_-46:.0f}" width="{pw_+92:.0f}"'
              f' height="{ph_+66:.0f}" rx="8" fill="none" stroke="#5e4a3a"'
              f' stroke-width="46"/>')
    # распахнутая створка перед проёмом
    s += SL(Z_SRED, f'<g transform="rotate(-5 {px_-40:.0f} {py_+ph_:.0f})">'
                    f'<rect x="{px_-250:.0f}" y="{py_-20:.0f}" width="230"'
                    f' height="{ph_+20:.0f}" rx="8" fill="#5e4a3a" {o(6)}/>'
                    f'<rect x="{px_-224:.0f}" y="{py_+10:.0f}" width="178"'
                    f' height="230" rx="6" fill="#7d6a48" {o(4)}/>'
                    f'<rect x="{px_-224:.0f}" y="{py_+270:.0f}" width="178"'
                    f' height="250" rx="6" fill="#7d6a48" {o(4)}/></g>')

    # велосипед, коврики, коляска
    s += SL(Z_SRED, _gorodskoy_hlam(520, 1010, 420, t, 269, ["velik", "yaschik"]))
    s += SL(Z_SRED, _gorodskoy_hlam(80, 1074, 400, t, 405, ["korobka", "yaschik"]))
    for i, (kx_, ky_) in enumerate(((240, 950), (1260, 1000))):
        s += SL(Z_SRED, f'<path d="M{kx_-150:.0f},{ky_:.0f} L{kx_+150:.0f},{ky_:.0f}'
                        f' L{kx_+186:.0f},{ky_+76:.0f} L{kx_-186:.0f},{ky_+76:.0f} Z"'
                        f' fill="{["#8a4a4a","#4a6a5a"][i]}" {o(5)}/>'
                        f'<path d="M{kx_-160:.0f},{ky_+28:.0f}'
                        f' L{kx_+160:.0f},{ky_+28:.0f} M{kx_-174:.0f},{ky_+54:.0f}'
                        f' L{kx_+174:.0f},{ky_+54:.0f}" stroke="#e8dcc8"'
                        f' stroke-width="7" opacity=".55"/>')
    kol = (f'<path d="M1600,900 Q1620,790 1740,790 L1860,790 Q1900,880 1860,940'
           f' L1640,940 Z" fill="#3a4a5a" {o(6)}/>'
           f'<path d="M1620,860 Q1700,816 1820,824" fill="none" stroke="#5a6a7a"'
           f' stroke-width="9"/>'
           f'<circle cx="1660" cy="990" r="52" fill="none" stroke="#2f3338"'
           f' stroke-width="14"/>'
           f'<circle cx="1830" cy="990" r="52" fill="none" stroke="#2f3338"'
           f' stroke-width="14"/>'
           f'<path d="M1860,790 L1930,700" stroke="#5a6a7a" stroke-width="13"'
           f' fill="none"/>')
    s += SL(Z_SRED, kol)

    # новые веник и швабра в упаковке за спиной хозяйки, листок с числом
    # НОВЫЕ ВЕНИК И ШВАБРА ПРИСЛОНЕНЫ К СТЕНЕ И СТОЯТ НА ПОЛУ: раньше они
    # просто висели в воздухе, а насадка швабры была ярко-розовой (#8a5a86) и
    # выбивалась из всего кадра (осмотр 15.11)
    s += SL(Z_SRED, ten(300, 1016, 76, 17, .5) + ten(420, 1062, 84, 18, .5)
            + f'<g transform="rotate(7 300 1010)">'
            + _venik(300, 1010, 420, t, "url(#solom)", "#c8a24a", True, .0, .3,
                     .85, 271) + "</g>")
    s += SL(Z_SRED, f'<line x1="372" y1="606" x2="420" y2="1010" stroke="#6a5a4a"'
                    f' stroke-width="17"/>'
                    f'<path d="M352,1010 L488,1010 L482,1056 L358,1056 Z"'
                    f' fill="#5a6670" {o(5)}/>'
                    f'<path d="M360,1018 L480,1018 M362,1038 L478,1038"'
                    f' stroke="#8a949c" stroke-width="6" opacity=".6"/>'
                    f'<rect x="244" y="560" width="230" height="300" rx="10"'
                    f' fill="#cfe4f5" opacity=".30" {o(3)}/>')
    lst = 5 * A.w(t, 2.0, .3)
    s += SL(Z_SRED, f'<g transform="rotate({lst:.1f} 360 580)">'
                    f'<rect x="300" y="560" width="120" height="86" rx="7"'
                    f' fill="#f0ead6" {o(4)}/>'
                    f'<path d="M318,598 Q356,586 404,600" fill="none" stroke="#8a929a"'
                    f' stroke-width="6"/>'
                    f'<path d="M318,622 Q350,612 388,624" fill="none" stroke="#8a929a"'
                    f' stroke-width="5"/></g>')

    # соседка в дверях протягивает швабру и веник
    # СОСЕДКА ЦЕЛИКОМ В КАДРЕ: стояла на 1880 и обрезалась правым краем
    # (туловище 1771-1989 при холсте 1920). И протягивает она ЛЕВОЙ — хозяйка
    # стоит слева, а правый рукав под 176° уходил поперёк тела за холст.
    sx_, sy_, sh_ = 1676, 944, 540
    sos = figura(sx_, sy_, sh_, t, col="#8a4a6a", kant="#ffd98a", ph=.5, naklon=-5)
    r2, (q2x, q2y), (s2x, s2y) = _ruka(sx_, sy_, sh_, -1, sh_ * .56, 6, t, "#8a4a6a",
                                       "#ffd98a", .6, 5)
    r1, (q1x, q1y), (s1x, s1y) = _ruka(sx_, sy_, sh_, 1, sh_ * .34, 72, t, "#8a4a6a",
                                       "#ffd98a", .2, 5)
    sos += r1 + r2
    # швабра в протянутой левой: черенок от кисти, насадка на дальнем конце
    sos += (f'<line x1="{q2x:.0f}" y1="{q2y:.0f}" x2="{q2x-250:.0f}"'
            f' y2="{q2y+96:.0f}" stroke="#6a5a4a" stroke-width="15"/>'
            f'<path d="M{q2x-250:.0f},{q2y+74:.0f} L{q2x-164:.0f},{q2y+112:.0f}'
            f' L{q2x-178:.0f},{q2y+146:.0f} L{q2x-266:.0f},{q2y+108:.0f} Z"'
            f' fill="#5a6670" {o(4)}/>')
    # веник в правой, прутьями вниз-вперёд и ЗА черенок
    sos += _venik_v_ruke(q1x, q1y, 300, t, "#8a7246", "#b8352c", 92, .78, 273, .3, .4)
    s += SL(Z_SRED, sos + ten(sx_, sy_ + 6, 104, 19, .45))

    # хозяйка напротив: обе ладони вежливо показывают «нет»
    hx_, hy_, hh_ = 700, 1000, 560
    hoz = figura(hx_, hy_, hh_, t, col="#3d4a3a", kant="#ffd98a", ph=.2)
    r3, (n1x, n1y), (g1x, g1y) = _ruka_ekr(hx_, hy_, hh_, 1, hh_ * .40, -48, t, "#3d4a3a",
                                           "#ffd98a", .1, 4)
    r4, (n2x, n2y), (g2x, g2y) = _ruka_ekr(hx_, hy_, hh_, -1, hh_ * .40, -22, t, "#3d4a3a",
                                           "#ffd98a", .5, 4)
    hoz += r3 + r4
    for (nx_, ny_) in ((n1x, n1y), (n2x, n2y)):
        hoz += (f'<ellipse cx="{nx_:.0f}" cy="{ny_:.0f}" rx="40" ry="54"'
                f' fill="#3d4a3a" {o(5)}/>'
                f'<ellipse cx="{nx_:.0f}" cy="{ny_:.0f}" rx="26" ry="38"'
                f' fill="#4c5b48" opacity=".8"/>')
    # фартук
    hoz += (f'<path d="M{hx_-56:.0f},{hy_-hh_*.60:.0f} L{hx_+56:.0f},{hy_-hh_*.60:.0f}'
            f' L{hx_+76:.0f},{hy_-hh_*.16:.0f} L{hx_-76:.0f},{hy_-hh_*.16:.0f} Z"'
            f' fill="#e4dcc4" opacity=".92" {o(4)}/>')
    s += SL(Z_SRED, hoz + ten(hx_, hy_ + 8, 110, 20, .45))
    s += SL(Z_PERED, _stolb_pered(-6, 86, "#20262a", 0, H))
    s += ramka_pp("oba")
    s += vinetka(.44)
    return s


def tri_raboty_odnogo_venika(t):
    """Три сцены по словам, в каждой по одному человеку: женщина в косынке
    метёт крашеный пол обеими руками; во дворе она же бьёт веником половик
    на верёвке; на крыльце мальчик на одной ноге обметает веником снег с
    валенка."""
    rnd = random.Random(135)
    pol = 800
    s = f'<rect width="{W}" height="{H}" fill="#2a2118"/>'
    s += SL(Z_DAL, brevna(0, 0, 640, pol + 40, 92))
    s += SL(Z_DAL, f'<rect x="640" y="0" width="640" height="{pol+40:.0f}"'
                   f' fill="#51606a"/>')
    s += SL(Z_DAL, nebo("sumer", t, True, 69))
    s += SL(Z_DAL, f'<rect x="640" y="0" width="640" height="{pol+40:.0f}"'
                   f' fill="#2f3a46" opacity=".55"/>')
    s += SL(Z_DAL, brevna(1280, 0, 680, pol + 40, 92))
    s += SL(Z_DAL, f'<rect x="200" y="56" width="1520" height="62" rx="12"'
                   f' fill="#3b2a1a" {o(7)}/>'
                   f'<rect x="200" y="112" width="1520" height="18" fill="#2a1d12"'
                   f' opacity=".8"/>')
    # простенки между тремя сценами
    for dx2 in (620, 1260):
        s += SL(Z_SRED, f'<rect x="{dx2:.0f}" y="0" width="52" height="{H}"'
                        f' fill="#2a1d12" {o(6)}/>'
                        f'<rect x="{dx2+10:.0f}" y="0" width="16" height="{H}"'
                        f' fill="#3e2c1c" opacity=".8"/>')

    # ── 1: крашеный пол, женщина метёт обеими руками
    s += SL(Z_DAL, okno_izby(60, 150, 260, 230, t, svet=False, moroz=.4))
    s += SL(Z_DAL, _polka_s_utvaryu(300, 330, 300, t, 275, 3))
    s += SL(Z_SRED, f'<rect x="0" y="{pol:.0f}" width="620" height="{H-pol}"'
                    f' fill="#8a5a4a" {o(0)}/>')
    for i in range(5):
        s += SL(Z_SRED, f'<line x1="0" y1="{pol+40+i*60:.0f}" x2="620"'
                        f' y2="{pol+40+i*60:.0f}" stroke="#6e4438" stroke-width="6"'
                        f' opacity=".7"/>')
    s += SL(Z_SRED, lampa(320, 160, t, 1.2, True) + teplo(320, 300, 260, 220, .40))
    s += SL(Z_SRED, _lavka_krupno(40, 1046, 320, t, 140))
    m1 = A.ease(abs(A.w(t, 1.5, .0)))
    ax, ay, ah = 340, 1010, 500
    zh1 = figura(ax, ay, ah, t, col="#4a3b2a", kant="#ffd98a", platok=True, ph=.2,
                 naklon=14 * m1)
    r1, (w1x, w1y), (a1x, a1y) = _ruka_ekr(ax, ay, ah, 1, ah * .48, 40 + 30 * m1, t, "#4a3b2a",
                                           "#ffd98a", .1, 5)
    r2, _, (a2x, a2y) = _ruka_ekr(ax, ay, ah, -1, ah * .44, 62 + 24 * m1, t, "#4a3b2a",
                                  "#ffd98a", .5, 5)
    zh1 += r1 + r2
    zh1 += _venik_v_ruke(w1x, w1y, 290, t, "#4b3f28", "#5a4a2e",
                         100 - 24 * m1, .9, 277, .25, .7)
    s += SL(Z_SRED, zh1)
    pyl = ""
    for i in range(7):
        p = ((t * .8 + i * .14) % 1.0)
        pyl += (f'<ellipse cx="{200-p*120:.0f}" cy="{1010-p*60:.0f}"'
                f' rx="{14+p*26:.0f}" ry="{7+p*12:.0f}" fill="#8a7a62"'
                f' opacity="{(1-p)*.4:.2f}"/>')
    s += SL(Z_SRED, pyl)

    # ── 2: двор, половик на верёвке, удары веником
    s += SL(Z_DAL, _derevnya_ryad(430, t, 279, ((760, 260), (1180, 240))))
    s += SL(Z_SRED, f'<rect x="640" y="{pol+10:.0f}" width="620" height="{H-pol-10}"'
                    f' fill="#473626" {o(0)}/>')
    s += SL(Z_SRED, _zemlya_faktura(pol + 60, 1060, 281, 8))
    s += SL(Z_SRED, f'<line x1="660" y1="430" x2="1250" y2="400" stroke="#9a8a68"'
                    f' stroke-width="8"/>')
    ud = A.ease(abs(A.w(t, 1.3, .2)))
    s += SL(Z_SRED, f'<path d="M820,410 L1120,398 L{1126+16*ud:.0f},680'
                    f' L{814-16*ud:.0f},692 Z" fill="{RUSH}" {o(6)}/>'
                    f'<path d="M824,470 L1122,458 M820,540 L1124,528'
                    f' M818,610 L1126,598" stroke="{KRAS}" stroke-width="11"'
                    f' opacity=".65"/>')
    for i in range(6):
        for k in range(3):
            sp = ((t * .9 + i * .16 + k * .3) % 1.0)
            s += SL(Z_SRED, f'<ellipse cx="{1130+sp*170:.0f}"'
                            f' cy="{460+k*80-sp*70:.0f}" rx="{10+sp*24:.0f}"'
                            f' ry="{6+sp*14:.0f}" fill="#9a8c70"'
                            f' opacity="{(1-sp)*.45*ud:.2f}"/>')
    bx_, by_, bh_ = 686, 1046, 500
    zh2 = figura(bx_, by_, bh_, t, col="#5a3f46", kant="#ffd98a", platok=True, ph=.5,
                 naklon=-8 * ud)
    # Женщина встала ЛЕВЕЕ половика и бьёт по нему ПРАВОЙ, наружу: прежде она
    # стояла прямо перед половиком, рукав под -44° шёл поперёк её лица, а
    # прутья веника ложились ей на голову (осмотр 15.11)
    r3, (w2x, w2y), (b1x, b1y) = _ruka(bx_, by_, bh_, 1, bh_ * .50, -50 + 30 * ud, t,
                                       "#5a3f46", "#ffd98a", .3, 6)
    r4, _, (b2x, b2y) = _ruka(bx_, by_, bh_, -1, bh_ * .44, 74, t, "#5a3f46",
                              "#ffd98a", .7, 4)
    zh2 += r3 + r4
    zh2 += _venik_v_ruke(w2x, w2y, 320, t, "#4b3f28", "#5a4a2e",
                         -42 + 26 * ud, .85, 283, .25, .2)
    zh2 += para_izo_rta(bx_ + 44, by_ - bh_ * .80, t, .4, 1.0, .5)
    s += SL(Z_SRED, zh2 + ten(bx_, by_ + 6, 100, 18, .45))
    s += SL(Z_SRED, _dvorovaya_utvar(940, 1070, 310, t, 285, ["kadka", "vedro"]))

    # ── 3: крыльцо, мальчик на одной ноге обметает валенок
    s += SL(Z_DAL, okno_izby(1640, 150, 260, 230, t, svet=True)
            + teplo(1770, 270, 240, 200, .42))
    s += SL(Z_DAL, _polka_s_utvaryu(1320, 340, 300, t, 287, 3))
    s += SL(Z_SRED, f'<rect x="1312" y="{pol+10:.0f}" width="648" height="{H-pol-10}"'
                    f' fill="#473626" {o(0)}/>')
    s += SL(Z_SRED, _kryl_co(1340, 820, 540, 170, t, 3, True, False))
    sug = (f'<path d="M1320,900 Q1420,844 1540,862 Q1660,820 1780,856'
           f' Q1880,834 1956,868 L1956,1080 L1320,1080 Z" fill="url(#sneg)" {o(5)}/>'
           f'<path d="M1330,906 Q1440,866 1546,882 Q1664,846 1790,876"'
           f' fill="none" stroke="#f2f7fb" stroke-width="7" opacity=".7"/>')
    s += SL(Z_SRED, sug)
    kach2 = A.ease(abs(A.w(t, 1.4, .1)))
    cx_, cy_, ch_ = 1600, 820, 400
    mal = figura(cx_, cy_, ch_, t, col="#3a4452", kant="#ffd98a", ph=.3,
                 naklon=8 * kach2 - 4)
    r5, (w3x, w3y), (c1x, c1y) = _ruka_ekr(cx_, cy_, ch_, 1, ch_ * .52, 66, t, "#3a4452",
                                           "#ffd98a", .2, 7)
    r6, _, (c2x, c2y) = _ruka_ekr(cx_, cy_, ch_, -1, ch_ * .48, 152, t, "#3a4452", "#ffd98a", .6,
                                  4)
    mal += r5 + r6
    # опорная нога на крыльце, вторая поднята
    mal += (f'<line x1="{cx_-14:.0f}" y1="{cy_-ch_*.28:.0f}" x2="{cx_-30:.0f}"'
            f' y2="{cy_-6:.0f}" stroke="#3a4452" stroke-width="36"'
            f' stroke-linecap="round"/>'
            f'<line x1="{cx_+14:.0f}" y1="{cy_-ch_*.28:.0f}" x2="{cx_+160:.0f}"'
            f' y2="{cy_-142:.0f}" stroke="#3a4452" stroke-width="36"'
            f' stroke-linecap="round"/>'
            f'<path d="M{cx_+136:.0f},{cy_-190:.0f} L{cx_+212:.0f},{cy_-180:.0f}'
            f' L{cx_+218:.0f},{cy_-92:.0f} L{cx_+130:.0f},{cy_-102:.0f} Z"'
            f' fill="#9a8c70" {o(5)}/>'
            f'<ellipse cx="{cx_+174:.0f}" cy="{cy_-94:.0f}" rx="50" ry="19"'
            f' fill="#7a6c52" {o(4)}/>')
    mal += _venik_v_ruke(w3x, w3y, 230, t, "#4b3f28", "#5a4a2e",
                         -86 + 16 * kach2, .7, 289, .25, .5)
    for i in range(8):
        sp = ((t * 1.1 + i * .12) % 1.0)
        mal += (f'<circle cx="{cx_+130+sp*120:.0f}" cy="{cy_-110+sp*180:.0f}"'
                f' r="{7-sp*3:.0f}" fill="#e4f1fa" opacity="{(1-sp)*.8:.2f}"/>')
    mal += para_izo_rta(cx_ + 40, cy_ - ch_ * .80, t, .2, .9, .5)
    s += SL(Z_SRED, mal)
    s += SL(Z_SRED, _dvorovaya_utvar(1340, 1070, 320, t, 291, ["korzina", "vedro"]))
    s += SL(Z_PERED, ramka_pp("oba"))
    s += vinetka(.44)
    return s
