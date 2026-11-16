# -*- coding: utf-8 -*-
"""ПОРЦИЯ 3: декорации ролика «19 ноября — Павел Ледостав».

Заботы дня (коньки, чай, калина), приметы погоды, поморский блок про
Ломоносова и финал с памяткой. Сцены рисуются заново под текст ЭТОГО дня
(R-0019), люди — figura() из lok_obshchee, руки — _ruka() от плеча, кистей и
пальцев не рисуем (R-0051). Задание — zadaniya/porciya3.md.
"""
import math, random
from baza import *
import anim as A
from lok_obshchee import *
from lok_obshchee import (
    _plecho, _predmet_naruzhu, _ruka, _ruka_ekr, _ruka_so_sgibom)
from chast1 import (_merzlaya_zemlya, _trava_suhaya, _petuh, _ramka_lubok,
                    _cherta_zapreta, _valenok)


def krepkiy_led_i_peshnya(t):
    """Река под толстым белым льдом в морозный день: мужик обеими руками бьёт
    пешнёй — она отскакивает, лёд не поддаётся, летит белая крошка. Он топает
    ногой и довольно кивает."""
    rnd = random.Random(3001)
    s = nebo("den", t, False, 373)
    s += oblaka(t, 150, 5, 179, .38)
    s += SL(Z_DAL, ulica_dal(60, 330, 820, t, True, 139))
    s += SL(Z_DAL, izba_snaruzhi(1500, 350, 300, t, True, True, 97)
            + dym_stolbom(1534, 200, t, 300, .5, .4, 7))
    s += SL(Z_DAL, f'<rect x="980" y="300" width="520" height="22" fill="#6b4428"'
                   f' stroke="{K}" stroke-width="4"/>')
    for i in range(4):
        s += SL(Z_DAL, f'<rect x="{1020+i*130:.0f}" y="322" width="18" height="90"'
                       f' fill="#54351f" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<rect x="0" y="420" width="{W}" height="660" fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(960, 760, 860, 220, t, .2, .0, .95))
    for i in range(9):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(60,1860):.0f}"'
                        f' cy="{rnd.uniform(560,1040):.0f}" rx="{rnd.uniform(80,220):.0f}"'
                        f' ry="{rnd.uniform(16,40):.0f}" fill="url(#sneg)"'
                        f' opacity="{rnd.uniform(.5,.9):.2f}"/>')
    # МУЖИК бьёт пешнёй
    ud = abs(A.w(t, 1.0, .0))
    mx, my, mh = 760, 900, 700
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f4a3a", kant="#cfe4f5",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -10 + 40 * ud, t,
                              "#3f4a3a", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .28, -6 + 36 * ud, t,
                              "#3f4a3a", "#cfe4f5", .5, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<g transform="rotate({-30+34*ud:.1f} {e1x:.0f} {e1y:.0f})">'
            + peshnya(e1x, e1y + 120, 1.3, 0, t, .1) + '</g>')
    # белая крошка от удара
    for i in range(9):
        d = ((t * 1.6 + i / 9.0) % 1.0)
        s += SL(Z_SRED, f'<path d="M{e1x+40+((i*37)%120)-60+120*d*math.cos(i):.0f},'
                        f'{e1y+220-180*d+120*d*d:.0f} l{10:.0f},{-8:.0f} l{4:.0f},{10:.0f} Z"'
                        f' fill="#ffffff" opacity="{(1-d)*.9:.2f}"/>')
    s += SL(Z_SRED, para_izo_rta(mx - 36, my - mh * .80, t, .3, 1.1, .55))
    s += SL(Z_SRED, ten(mx, my + 6, 140, 24, .4))
    # сани на берегу, лошадь под попоной
    s += SL(Z_SRED, sani_s_rogozhey(1480, 980, 1.0, t, .3, True))
    kiv = 8 * A.w(t, 1.8, .2)
    s += SL(Z_SRED, f'<ellipse cx="1760" cy="900" rx="150" ry="80" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1630,860 q{140:.0f},{-40:.0f} {270:.0f},{-10:.0f}'
                    f' l{-20:.0f},{90:.0f} q{-120:.0f},{20:.0f} {-240:.0f},0 Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>'
                    f'<circle cx="{1636+kiv:.0f}" cy="{830+kiv:.0f}" r="46"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{1612+kiv:.0f},{794+kiv:.0f} l{-10:.0f},{-34:.0f}'
                    f' l{26:.0f},{24:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3"/>'
                    f'<path d="M1680,980 l-10,60 M1760,984 l0,56 M1840,978 l10,62"'
                    f' stroke="#54351f" stroke-width="14"/>')
    s += SL(Z_SRED, goloe_derevo_ld(240, 1020, 520, t, 373, 7, True)
            + goloe_derevo_ld(420, 1050, 420, t, 379, 6, True))
    s += SL(Z_SRED, kamysh(80, 1000, 220, t, 7, 383, True))
    s += SL(Z_SRED, par(1760, 820, t, 4, .5, 170, .45, 1.0))
    s += SL(Z_SRED, inej_mel(373, 46, 900, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def sani_cherez_reku_i_konki(t):
    """Та же река, лёд крепкий: по льду едут сани, ближе к берегу двое детей
    на коньках, привязанных к валенкам. Листки численника перелистывают годы:
    в одном лёд белый, в других на этот день тёмная вода."""
    rnd = random.Random(3002)
    s = nebo("den", t, False, 379)
    s += oblaka(t, 140, 5, 181, .40)
    s += SL(Z_DAL, ulica_dal(1120, 320, 800, t, True, 149))
    s += SL(Z_DAL, izba_snaruzhi(300, 340, 280, t, True, True, 101)
            + dym_stolbom(330, 200, t, 280, .48, .4, 6))
    s += SL(Z_SRED, f'<rect x="0" y="420" width="{W}" height="660" fill="url(#led)"/>')
    s += SL(Z_SRED, korka_lda(960, 720, 880, 200, t, .3, .0, .9))
    s += SL(Z_SRED, mostki(1480, 520, 420, t, True, 160))
    # САНИ едут по льду
    edet = A.ease(A.seg(t, .3, 3.4))
    lx = 300 + 500 * edet
    s += SL(Z_SRED, sani_s_rogozhey(lx - 260, 700, .95, t, .2, False))
    kiv = 9 * A.w(t, 1.5, .1)
    s += SL(Z_SRED, f'<ellipse cx="{lx:.0f}" cy="640" rx="130" ry="70" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="{lx+116:.0f}" cy="{594+kiv:.0f}" r="42" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{lx+138:.0f},{560+kiv:.0f} l{12:.0f},{-40:.0f}'
                    f' l{18:.0f},{36:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3.4"/>'
                    f'<path d="M{lx-70:.0f},720 l-10,56 M{lx:.0f},724 l0,52'
                    f' M{lx+70:.0f},718 l10,58" stroke="#54351f" stroke-width="13"/>')
    mx, my, mh = lx - 230, 660, 460
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f4a3a", kant="#cfe4f5",
                           tulup=True, shapka=True, boroda=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -4, t, "#3f4a3a", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .28, 0, t, "#3f4a3a", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2
            + f'<path d="M{e1x:.0f},{e1y:.0f} L{lx+90:.0f},{600+kiv:.0f}"'
              f' stroke="#6b4428" stroke-width="5"/>'
              f'<path d="M{e2x:.0f},{e2y:.0f} L{lx+80:.0f},{620+kiv:.0f}"'
              f' stroke="#6b4428" stroke-width="5"/>')
    # ДВОЕ ДЕТЕЙ на коньках
    kat = A.ease(A.seg(t, .5, 3.0))
    dx, dy, dh = 760 + 260 * kat, 1010, 440
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#3f5a6a", kant="#cfe4f5",
                           shapka=True, ph=.2, naklon=4.0))
    r3, (e3x, e3y), _ = _ruka(dx, dy, dh, 1, dh * .30, -34, t, "#3f5a6a", "#cfe4f5", .2, 7)
    r4, (e4x, e4y), _ = _ruka(dx, dy, dh, -1, dh * .30, -30, t, "#3f5a6a", "#cfe4f5", .6, 7)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, konki_snegurki(dx - 30, dy, .68, 0, True, t, .1)
            + konki_snegurki(dx + 40, dy + 4, .68, 0, True, t, .5))
    gx, gy, gh = dx - 220, 1020, 400
    s += SL(Z_SRED, figura(gx, gy, gh, t, col="#8a2f22", kant="#cfe4f5",
                           platok=True, ph=.7, naklon=4.0))
    r5, (e5x, e5y), _ = _ruka(gx, gy, gh, 1, gh * .34, -16, t, "#8a2f22", "#cfe4f5", .3, 5)
    r6, (e6x, e6y), _ = _ruka(gx, gy, gh, -1, gh * .30, -12, t, "#8a2f22", "#cfe4f5", .8, 5)
    s += SL(Z_SRED, r5 + r6)
    s += SL(Z_SRED, f'<path d="M{e5x:.0f},{e5y:.0f} q{60:.0f},{-20:.0f} {130:.0f},{-30:.0f}"'
                    f' fill="none" stroke="{TKAN}" stroke-width="16"/>')
    s += SL(Z_SRED, konki_snegurki(gx - 26, gy, .62, 0, True, t, .3)
            + konki_snegurki(gx + 36, gy + 4, .62, 0, True, t, .8))
    s += SL(Z_SRED, para_izo_rta(dx - 26, dy - dh * .80, t, .3, .9, .45)
            + para_izo_rta(gx - 24, gy - gh * .80, t, .8, .8, .45))
    # ЛИСТКИ ЧИСЛЕННИКА перелистывают годы
    s += SL(Z_SRED, f'<rect x="120" y="200" width="200" height="260" rx="10"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="120" y="200" width="200" height="50" rx="10"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="5"/>')
    god = int((t * .7) % 3)
    s += SL(Z_SRED, f'<rect x="150" y="280" width="140" height="140" rx="8"'
                    f' fill="{"#dcecf8" if god == 0 else "#2f4a52"}" stroke="{K}"'
                    f' stroke-width="4"/>')
    for i in range(3):
        d = ((t * .7 + i * .33) % 1.0)
        s += SL(Z_LETIT, f'<rect x="{140+260*d:.0f}" y="{280+300*d*d:.0f}" width="120"'
                         f' height="140" rx="6" fill="#f2ead6" opacity="{(1-d)*.85:.2f}"'
                         f' transform="rotate({d*150:.0f} {200+260*d:.0f}'
                         f' {350+300*d*d:.0f})" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, goloe_derevo_ld(1800, 1000, 460, t, 389, 7, True))
    s += SL(Z_SRED, kamysh(60, 1020, 200, t, 6, 397, True))
    # СЕРЕДИНА ЛЬДА НЕ ПУСТАЯ: вешки, наметённые гряды, прорубь, санный след
    for i, vx_ in enumerate((620, 900, 1180, 1420)):
        kch = 3.0 * A.w(t, 3.2, i * .3)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {vx_:.0f} {620:.0f})">'
                        f'<rect x="{vx_:.0f}" y="430" width="12" height="190"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="3"/>'
                        f'<path d="M{vx_-20:.0f},430 q{26:.0f},{-28:.0f} {52:.0f},{-4:.0f}'
                        f' q{-24:.0f},{20:.0f} {-52:.0f},{4:.0f} Z" fill="#8a7a52"'
                        f' stroke="{K}" stroke-width="3"/></g>')
    for i in range(8):
        s += SL(Z_SRED, f'<ellipse cx="{320+i*210:.0f}" cy="{520+((i*7)%4)*40:.0f}"'
                        f' rx="{90+((i*5)%3)*40:.0f}" ry="{18+((i*3)%2)*10:.0f}"'
                        f' fill="url(#sneg)" opacity=".85"/>')
    s += SL(Z_SRED, prorub(1640, 760, 120, t, .3, True))
    s += SL(Z_SRED, sledy_valenok(1880, 900, 1200, 700, 7, 401, "#9fc4d8", 1.1))
    s += SL(Z_SRED, par(lx + 150, 580, t, 4, .5, 160, .45, 1.0))
    s += SL(Z_SRED, inej_mel(379, 44, 940, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def konki_na_valenkah(t):
    """Валенок на пол-кадра, к нему верёвкой и палочкой-закруткой прикручен
    конёк-«снегурка». Мальчик на лавочке у катка затягивает верёвку; рядом
    самодельная клюшка из гнутой ветки и консервная крышка вместо шайбы."""
    rnd = random.Random(3003)
    s = nebo("noch", t, True, 383)
    s += SL(Z_NEBO, luna_v_gorode(300, 160, t, .7, True))
    s += SL(Z_DAL, panelka(1180, 540, 740, t, 5, True, 47))
    s += SL(Z_DAL, zabor_shtaket(-40, 420, 1100, 200, 383, 62))
    s += SL(Z_SRED, f'<rect x="0" y="620" width="{W}" height="460" fill="#dce7f2"/>')
    s += SL(Z_SRED, sneg_lezhit(640, 34, "url(#sneg)"))
    # ФОНАРЬ
    s += SL(Z_SRED, f'<rect x="1520" y="260" width="22" height="560" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(1531, 260, t, 1.4, True) + teplo(1531, 280, 320, 270, .42))
    # ЛАВОЧКА и мальчик
    s += SL(Z_SRED, f'<rect x="900" y="800" width="700" height="26" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="900" y="740" width="700" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="930" y="826" width="24" height="140" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1550" y="826" width="24" height="140" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    mx, my, mh = 1240, 800, 520
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f5a6a", kant="#cfe4f5",
                           shapka=True, tulup=True, ph=.3, naklon=3.0))
    zakr = A.ease(A.seg(t, .6, 2.0))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, -1, mh * .38, 40 + 10 * zakr, t,
                              "#3f5a6a", "#cfe4f5", .2, 6)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, 1, mh * .36, 44 + 10 * zakr, t,
                              "#3f5a6a", "#cfe4f5", .6, 6)
    s += SL(Z_SRED, r1 + varezhka(e1x - 8, e1y + 10, .9, -14, TKAN, t, .2)
            + r2 + varezhka(e2x + 8, e2y + 10, .9, 14, TKAN, t, .6))
    s += SL(Z_SRED, para_izo_rta(mx - 28, my - mh * .78, t, .4, .9, .5))
    # ВАЛЕНОК С КОНЬКОМ на пол-кадра
    vx, vy = 540, 980
    s += SL(Z_SRED, f'<g transform="rotate(-6 {vx:.0f} {vy:.0f})">'
            + _valenok(vx, vy, 3.6, 0, "#c9bfa6") + '</g>')
    s += SL(Z_SRED, teplo(vx, vy - 140, 420, 340, .30))
    s += SL(Z_SRED, konki_snegurki(vx + 10, vy + 24, 2.8, -6, False, t, .2))
    # верёвка и палочка-закрутка
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{vx-130:.0f},{vy-90-i*46:.0f} q{130:.0f},{-26:.0f}'
                        f' {270:.0f},{6:.0f}" fill="none" stroke="#b9a37a"'
                        f' stroke-width="9"/>')
    s += SL(Z_SRED, f'<g transform="rotate({zakr*220:.0f} {vx+80:.0f} {vy-136:.0f})">'
                    f'<rect x="{vx+56:.0f}" y="{vy-150:.0f}" width="48" height="24"'
                    f' rx="8" fill="#7d5636" stroke="{K}" stroke-width="4"/></g>')
    # КЛЮШКА и крышка вместо шайбы
    s += SL(Z_SRED, f'<g transform="rotate(14 1760 1000)">'
                    f'<path d="M1754,520 q{20:.0f},{240:.0f} {-10:.0f},{420:.0f}'
                    f' q{-6:.0f},{60:.0f} {70:.0f},{60:.0f}" fill="none"'
                    f' stroke="#8a6342" stroke-width="18" stroke-linecap="round"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{1744+i*3:.0f},{600+i*54:.0f} q{16:.0f},{10:.0f}'
                        f' {26:.0f},{2:.0f}" fill="none" stroke="{TKAN}"'
                        f' stroke-width="7" opacity=".9"/>')
    s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, f'<ellipse cx="1500" cy="1040" rx="46" ry="16" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="1500" cy="1034" rx="36" ry="11" fill="#8f979f"/>')
    s += SL(Z_SRED, _valenok(960, 1050, 1.5, 6))
    s += SL(Z_SRED, konki_snegurki(980, 1066, 1.1, 4, False, t, .7))
    s += SL(Z_SRED, inej_mel(389, 50, 940, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 26, 101, .5, .6))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def tochilschik_s_tochilnym_krugom(t):
    """Двор, точильный станок с ножным приводом на пол-кадра: точильщик качает
    педаль и прижимает конёк к вращающемуся кругу, трое мальчишек ждут
    очереди со своими коньками. Над двором расходятся звуковые кольца."""
    rnd = random.Random(3004)
    s = nebo("den", t, False, 397)
    s += oblaka(t, 140, 5, 191, .40)
    s += SL(Z_DAL, panelka(60, 560, 860, t, 4, True, 53))
    s += SL(Z_DAL, panelka(1240, 540, 680, t, 5, True, 59))
    s += SL(Z_SRED, f'<rect x="0" y="640" width="{W}" height="440" fill="#dce7f2"/>')
    s += SL(Z_SRED, sneg_lezhit(660, 32, "url(#sneg)"))
    # САРАЙ и поленница
    s += SL(Z_SRED, f'<rect x="1480" y="420" width="440" height="300" rx="8"'
                    f' fill="#5e4430" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1450,420 l230,-110 l250,110 Z" fill="#4a3526"'
                    f' stroke="{K}" stroke-width="5.5"/>'
                    f'<path d="M1450,420 l230,-110 l250,110" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="16" opacity=".9"/>')
    s += SL(Z_SRED, f'<rect x="80" y="520" width="280" height="190" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(15):
        s += SL(Z_SRED, f'<circle cx="{104+(i%5)*56:.0f}" cy="{550+(i//5)*58:.0f}" r="26"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    # ТОЧИЛЬНЫЙ СТАНОК на пол-кадра
    sx_, sy_ = 820, 980
    s += SL(Z_SRED, f'<rect x="{sx_-220:.0f}" y="{sy_-80:.0f}" width="440" height="40"'
                    f' rx="8" fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="{sx_-190:.0f}" y="{sy_-40:.0f}" width="40" height="80"'
                    f' fill="#54351f" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{sx_+150:.0f}" y="{sy_-40:.0f}" width="40" height="80"'
                    f' fill="#54351f" stroke="{K}" stroke-width="4"/>')
    for i in (-1, 1):
        s += SL(Z_SRED, f'<rect x="{sx_+i*150-14:.0f}" y="{sy_-440:.0f}" width="28"'
                        f' height="360" fill="#7d5636" stroke="{K}" stroke-width="4"/>')
    ug = (t * 520) % 360
    s += SL(Z_SRED, f'<g transform="rotate({ug:.0f} {sx_:.0f} {sy_-430:.0f})">'
                    f'<circle cx="{sx_:.0f}" cy="{sy_-430:.0f}" r="130" fill="#9aa3a8"'
                    f' stroke="{K}" stroke-width="6"/>')
    for i in range(6):
        a = i * 1.05
        s += SL(Z_SRED, f'<line x1="{sx_:.0f}" y1="{sy_-430:.0f}"'
                        f' x2="{sx_+120*math.cos(a):.0f}" y2="{sy_-430+120*math.sin(a):.0f}"'
                        f' stroke="#8a8078" stroke-width="5" opacity=".8"/>')
    s += SL(Z_SRED, f'<circle cx="{sx_:.0f}" cy="{sy_-430:.0f}" r="30" fill="#6f7a84"'
                    f' stroke="{K}" stroke-width="4"/></g>')
    ped = 16 * A.w(t, .9, .0)
    s += SL(Z_SRED, f'<path d="M{sx_-170:.0f},{sy_+30+ped:.0f} h200 l0,20 h-200 Z"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{sx_-70:.0f},{sy_+30+ped:.0f} L{sx_-30:.0f},{sy_-380:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="7"/>')
    # искры от круга
    for i in range(8):
        d = ((t * 1.8 + i / 8.0) % 1.0)
        s += SL(Z_SRED, f'<path d="M{sx_+120+200*d:.0f},{sy_-440+120*d*d:.0f}'
                        f' l{12:.0f},{4:.0f}" stroke="#ffd98a" stroke-width="4"'
                        f' opacity="{(1-d)*.9:.2f}"/>')
    # ТОЧИЛЬЩИК
    tx, ty, th = 620, 1046, 700
    s += SL(Z_SRED, figura(tx, ty, th, t, col="#3f4a3a", kant="#ffd9a8",
                           shapka=True, ph=.2, naklon=2.0))
    s += SL(Z_SRED, f'<path d="M{tx-90:.0f},{ty-th*.52:.0f} q{90:.0f},{-20:.0f}'
                    f' {180:.0f},0 l{10:.0f},{th*.34:.0f} q{-100:.0f},{24:.0f}'
                    f' {-200:.0f},0 Z" fill="#8a7a62" stroke="{K}" stroke-width="4.5"/>')
    r1, (e1x, e1y), _ = _ruka(tx, ty, th, 1, th * .32, -16, t, "#3f4a3a", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(tx, ty, th, -1, th * .30, -12, t, "#3f4a3a", "#ffd9a8", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, konki_snegurki((e1x + e2x) * .5 + 40, e1y + 10, .9, -24, False, t, .2))
    s += SL(Z_SRED, para_izo_rta(tx - 34, ty - th * .80, t, .3, 1.0, .5))
    # ЗВУКОВЫЕ КОЛЬЦА над двором
    for i in range(4):
        d = ((t * .7 + i * .25) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="{sy_-430:.0f}"'
                        f' rx="{180+620*d:.0f}" ry="{70+240*d:.0f}" fill="none"'
                        f' stroke="#cfe4f5" stroke-width="{6-3*d:.1f}"'
                        f' opacity="{(1-d)*.5:.2f}"/>')
    # ТРОЕ МАЛЬЧИШЕК в очереди
    for i, (bx_, by_, bh_, col) in enumerate(((1200, 1050, 470, "#3f5a6a"),
                                              (1390, 1060, 440, "#8a2f22"),
                                              (1570, 1046, 490, "#4a6a3a"))):
        s += SL(Z_SRED, figura(bx_, by_, bh_, t, col=col, kant="#ffd9a8",
                               shapka=True, ph=i * .35))
        rk, (ex, ey), _ = _ruka(bx_, by_, bh_, 1, bh_ * .26, 40, t, col, "#ffd9a8", i * .3, 4)
        rk2, (e2x_, e2y_), _ = _ruka(bx_, by_, bh_, -1, bh_ * .26, 44, t, col,
                                     "#ffd9a8", i * .3 + .4, 4)
        s += SL(Z_SRED, rk + rk2
                + konki_snegurki((ex + e2x_) * .5, ey + 70, .6, 10, False, t, i * .3))
        s += SL(Z_SRED, para_izo_rta(bx_ - 24, by_ - bh_ * .80, t, i * .3, .8, .45))
    s += SL(Z_SRED, kot(1700, 400, t, 1.4, "#4a423a", False))
    s += SL(Z_SRED, dym_stolbom(1680, 300, t, 260, .45, .4, 6))
    s += SL(Z_SRED, inej_mel(397, 46, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def katok_vo_dvore(t):
    """Двор между домами: вечером отец широким взмахом выплёскивает ведро на
    тёмную площадку, утром она становится блестящим катком, и со всех
    подъездов сбегаются дети. В окне над катком — настоящие коньки на льду."""
    rnd = random.Random(3005)
    utro = A.ease(A.seg(t, 1.6, 1.8))
    s = nebo("noch" if utro < .5 else "rassv", t, utro < .5, 401)
    s += SL(Z_DAL, panelka(40, 620, 860, t, 5, True, 61))
    s += SL(Z_DAL, panelka(1180, 600, 740, t, 5, True, 67))
    # ОКНО-ПРОЁМ над катком (сверху справа)
    px, py, pw, ph_ = 1120, 180, 780, 320
    okno = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
            f' fill="#9fc4d8"/>')
    okno += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.4:.0f}"'
             f' fill="#c4d8e8"/>')
    okno += mesto_stoka(px, py, pw, ph_, "pryam")
    okno += (f'<rect x="{px-18:.0f}" y="{py-18:.0f}" width="{pw+36:.0f}"'
             f' height="{ph_+36:.0f}" rx="6" fill="none" stroke="#d8cbb0"'
             f' stroke-width="26"/>')
    okno += (f'<path d="M{px+pw*.5:.0f},{py:.0f} v{ph_:.0f} M{px:.0f},{py+ph_*.5:.0f}'
             f' h{pw:.0f}" stroke="#e4d8bd" stroke-width="16"/>')
    s += SL(Z_DAL, okno)
    s += SL(Z_SRED, _merzlaya_zemlya(700, 401, False))
    s += SL(Z_SRED, sneg_lezhit(720, 30, "url(#sneg)"))
    # ПЛОЩАДКА: тёмная вечером, каток утром
    s += SL(Z_SRED, f'<ellipse cx="900" cy="880" rx="620" ry="180" fill="#3f4a56"/>')
    s += SL(Z_SRED, f'<ellipse cx="900" cy="880" rx="620" ry="180" fill="url(#led)"'
                    f' opacity="{utro:.2f}"/>')
    if utro > .3:
        s += SL(Z_SRED, korka_lda(900, 876, 580, 160, t, .2, .0, utro * .85))
    # бортики из снега
    for i in range(14):
        a = 3.14 + i * .25
        s += SL(Z_SRED, f'<ellipse cx="{900+640*math.cos(a):.0f}"'
                        f' cy="{880+190*math.sin(a):.0f}" rx="70" ry="26"'
                        f' fill="url(#sneg)" opacity=".92"/>')
    # ВЕЧЕР: отец выплёскивает ведро
    if utro < .75:
        ox, oy, oh = 420, 1040, 700
        vzmah = A.ease(A.seg(t, .4, .8))
        s += SL(Z_SRED, f'<g opacity="{1-utro:.2f}">'
                + figura(ox, oy, oh, t, col="#3f4a3a", kant="#ffd9a8",
                         tulup=True, shapka=True, ph=.2) + '</g>')
        r1, (e1x, e1y), _ = _ruka(ox, oy, oh, 1, oh * .32, -40 + 50 * vzmah, t,
                                  "#3f4a3a", "#ffd9a8", .2, 6)
        r2, (e2x, e2y), _ = _ruka(ox, oy, oh, -1, oh * .28, -36 + 46 * vzmah, t,
                                  "#3f4a3a", "#ffd9a8", .6, 6)
        s += SL(Z_SRED, f'<g opacity="{1-utro:.2f}">' + r1 + r2
                + f'<g transform="rotate({-40+90*vzmah:.0f} {e1x:.0f} {e1y:.0f})">'
                  f'<path d="M{e1x-44:.0f},{e1y:.0f} h88 l-10,92 h-68 Z"'
                  f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4.5"/>'
                  f'<ellipse cx="{e1x:.0f}" cy="{e1y:.0f}" rx="44" ry="13"'
                  f' fill="#8f979f" stroke="{K}" stroke-width="3.6"/></g></g>')
        for i in range(12):
            d = ((t * 1.2 + i / 12.0) % 1.0)
            s += SL(Z_SRED, f'<ellipse cx="{e1x+80+500*d:.0f}"'
                            f' cy="{e1y+40+260*d*d-120*d:.0f}" rx="{20+26*d:.0f}"'
                            f' ry="{10+14*d:.0f}" fill="#9fd0e4"'
                            f' opacity="{(1-d)*.6*(1-utro):.2f}"/>')
        for i in range(6):
            s += SL(Z_SRED, par(700 + i * 140, 900, t, 3, .4 * (1 - utro), 150, .4, 1.0))
    # УТРО: дети сбегаются на каток
    if utro > .25:
        for i, (dx_, dy_, dh_, col) in enumerate(((700, 1000, 420, "#8a2f22"),
                                                  (1020, 1020, 440, "#3f5a6a"),
                                                  (1300, 990, 400, "#4a6a3a"),
                                                  (480, 1030, 380, "#6b3a6a"))):
            beg = A.ease(A.seg(t, 1.8 + i * .2, 1.4))
            px_ = dx_ + (900 - dx_) * .4 * beg
            s += SL(Z_SRED, f'<g opacity="{min(1.0, (utro-.25)*3):.2f}">'
                    + figura(px_, dy_, dh_, t, col=col, kant="#ffd9a8",
                             shapka=True, ph=i * .3, naklon=4.0) + '</g>')
            rk, (ex, ey), _ = _ruka(px_, dy_, dh_, 1 if i % 2 else -1, dh_ * .28,
                                    -30, t, col, "#ffd9a8", i * .25, 7)
            s += SL(Z_SRED, f'<g opacity="{min(1.0, (utro-.25)*3):.2f}">' + rk + '</g>')
            s += SL(Z_SRED, konki_snegurki(px_, dy_, .6, 0, True, t, i * .3))
    # фонарь, скамейка, санки, собака
    s += SL(Z_SRED, f'<rect x="300" y="420" width="22" height="420" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(311, 420, t, 1.3, True) + teplo(311, 440, 300, 250, .40))
    s += SL(Z_SRED, f'<rect x="1560" y="880" width="300" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1580" y="902" width="22" height="110" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="1810" y="902" width="22" height="110" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, sanki_derev(180, 1040, .9, t, .5, True))
    s += SL(Z_SRED, f'<ellipse cx="1700" cy="1020" rx="74" ry="36" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="1766" cy="986" r="30" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3.6"/>'
                    f'<path d="M1784,962 l{12:.0f},{-30:.0f} l{14:.0f},{28:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="3"/>'
                    f'<path d="M1636,1010 q{-38:.0f},{-28:.0f} {-54:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#6b5230" stroke-width="9"/>')
    s += SL(Z_SRED, inej_mel(401, 44, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def primerka_konkov_v_prihozhey(t):
    """Прихожая, коробка с коньками: внучка на пуфе вставляет ногу в белый
    ботинок и тянет шнурки, дед на корточках придерживает ботинок и
    проверяет рукавицей лезвие. На стене карта: пруд перечёркнут, каток обведён."""
    rnd = random.Random(3006)
    s = (f'<rect width="{W}" height="{H}" fill="#c3ab8a"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="760" fill="#cbb492"/>')
    for i in range(14):
        s += SL(Z_DAL, f'<path d="M{70+i*140:.0f},0 v760" stroke="#b9a082"'
                       f' stroke-width="4" opacity=".5"/>')
    s += SL(Z_DAL, polovicy(760, "#8a6342"))
    # ВЕШАЛКА с шапками
    s += SL(Z_SRED, f'<rect x="120" y="180" width="440" height="20" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{170+i*110:.0f},200 l0,30" stroke="{ZHELEZ}"'
                        f' stroke-width="7"/>')
    for i, (hx_, col) in enumerate(((180, "#3f4a7a"), (290, "#6b3a2a"), (400, "#4a6a3a"))):
        s += SL(Z_SRED, f'<path d="M{hx_:.0f},240 q{44:.0f},{-24:.0f} {88:.0f},0'
                        f' l{8:.0f},{150:.0f} q{-50:.0f},{20:.0f} {-104:.0f},0 Z"'
                        f' fill="{col}" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<ellipse cx="520" cy="250" rx="54" ry="30" fill="#4a3a2c"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="520" cy="236" rx="54" ry="20" fill="#8a6a4a"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    # КАРТА на стене: пруд перечёркнут, каток обведён
    s += SL(Z_SRED, f'<rect x="1180" y="160" width="620" height="420" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, f'<ellipse cx="1380" cy="330" rx="130" ry="80" fill="#9fc4d8"'
                    f' stroke="#6f7a84" stroke-width="5"/>')
    s += SL(Z_SRED, _cherta_zapreta(1380, 330, 130, t, .0, 14))
    obv = A.out(A.seg(t, 1.0, .8))
    s += SL(Z_SRED, f'<rect x="1560" y="380" width="200" height="130" rx="10"'
                    f' fill="#dce7f2" stroke="#6f7a84" stroke-width="5"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1590+i*60:.0f}" y="350" width="10" height="36"'
                        f' fill="{BETON2}"/>'
                        f'<circle cx="{1595+i*60:.0f}" cy="346" r="11" fill="#ffd98a"'
                        f' opacity=".9"/>')
    if obv > .02:
        s += SL(Z_SRED, f'<ellipse cx="1660" cy="444" rx="{170*obv:.0f}"'
                        f' ry="{110*obv:.0f}" fill="none" stroke="#3f8a4a"'
                        f' stroke-width="12" opacity="{obv:.2f}"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{1220+i*80:.0f},520 q{30:.0f},{-14:.0f} {60:.0f},0"'
                        f' fill="none" stroke="#b9a082" stroke-width="4"/>')
    # КОРОБКА с коньками
    s += SL(Z_SRED, f'<rect x="760" y="880" width="320" height="180" rx="10"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5.5"/>'
                    f'<path d="M760,930 h320" stroke="#6b4428" stroke-width="7"/>')
    s += SL(Z_SRED, konki_snegurki(900, 880, 1.0, -12, False, t, .2))
    # ВНУЧКА на пуфе
    vx, vy, vh = 420, 900, 520
    s += SL(Z_SRED, f'<ellipse cx="{vx:.0f}" cy="{vy:.0f}" rx="130" ry="56"'
                    f' fill="#8a2f8a" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="{vx:.0f}" cy="{vy-20:.0f}" rx="130" ry="50"'
                    f' fill="#a03aa0" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(vx, vy - 20, vh, t, col="#c8301f", kant="#ffd98a",
                           ph=.3, naklon=3.0))
    tyan = A.ease(A.seg(t, .6, 1.6))
    r1, (e1x, e1y), _ = _ruka(vx, vy - 20, vh, 1, vh * .38, 40 - 14 * tyan, t,
                              "#c8301f", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(vx, vy - 20, vh, -1, vh * .38, 44 - 12 * tyan, t,
                              "#c8301f", "#ffd98a", .6, 5)
    s += SL(Z_SRED, r1 + r2)
    # БЕЛЫЙ БОТИНОК конька на ноге
    bx_, by_ = vx + 150, vy + 60
    s += SL(Z_SRED, f'<path d="M{vx+40:.0f},{vy-40:.0f} q{60:.0f},{40:.0f}'
                    f' {110:.0f},{70:.0f}" fill="none" stroke="#c8301f"'
                    f' stroke-width="30" stroke-linecap="round"/>')
    s += SL(Z_SRED, f'<path d="M{bx_-50:.0f},{by_-110:.0f} h{90:.0f} q{20:.0f},{60:.0f}'
                    f' {10:.0f},{110:.0f} l{-100:.0f},0 q{-16:.0f},{-56:.0f}'
                    f' {0:.0f},{-110:.0f} Z" fill="#f4f1e8" stroke="{K}"'
                    f' stroke-width="5"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{bx_-44+i*4:.0f},{by_-96+i*20:.0f}'
                        f' l{76-i*8:.0f},{6:.0f}" stroke="#c9bfa6"'
                        f' stroke-width="{4-tyan:.1f}"/>')
    s += SL(Z_SRED, konki_snegurki(bx_ - 4, by_ + 10, 1.0, 0, False, t, .4))
    # ДЕД на корточках
    dx, dy, dh = 760, 1056, 470
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, ph=.6, naklon=2.0))
    kch = 3.0 * A.w(t, 1.8, .2)
    r3, (e3x, e3y), _ = _ruka(dx, dy, dh, -1, dh * .40, 6, t, "#4a4038", "#ffd98a", .3, 4)
    r4, (e4x, e4y), _ = _ruka(dx, dy, dh, 1, dh * .34, 20, t, "#4a4038", "#ffd98a", .8, 4)
    s += SL(Z_SRED, r3 + r4 + varezhka(e4x + 8, e4y + 8, 1.0, 16 + kch, "#6b4428", t, .3))
    s += SL(Z_SRED, f'<rect x="1020" y="1020" width="130" height="44" rx="8"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, sanki_derev(1500, 1050, .8, t, .4, True))
    s += SL(Z_SRED, f'<rect x="1660" y="900" width="220" height="160" rx="10"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, kot(1770, 900, t, 1.4, "#3b3430", True))
    s += SL(Z_SRED, lampa(960, 100, t, 1.3, True) + teplo(960, 120, 320, 260, .42))
    s += SL(Z_SRED, ten(dx, dy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def chaynik_i_travy_pod_potolkom(t):
    """Деревенская кухня: под потолком на жерди сушатся пучки трав, на столе
    пузатый фарфоровый чайник на пол-кадра. Стеклянная дверца буфета — проём
    с настоящим травяным чаем. Хозяйка кладёт в чайник щепоть травы."""
    rnd = random.Random(3007)
    s = stena_gornicy_19(t, 37, 840, True, True)
    s += SL(Z_SRED, pech(60, 260, 460, 580, t, True, True, False))
    s += SL(Z_SRED, ogon(200, 700, t, 1.3, .1, 6) + teplo(200, 680, 360, 300, .5))
    # ЖЕРДЬ с пучками трав
    s += SL(Z_SRED, f'<path d="M520,220 h1100" stroke="#8a6342" stroke-width="13"/>')
    for i, (px_, ph2, sc) in enumerate(((620, .1, 1.0), (780, .4, .9), (940, .7, 1.1),
                                        (1100, .2, .85), (1260, .6, 1.0),
                                        (1420, .9, .9))):
        s += SL(Z_SRED, puchok_trav(px_, 230, sc, t, ph2, 67 + i, "#8a7a4a"))
    # БУФЕТ со стеклянной дверцей — проём
    bx, by, bw, bh = 1180, 420, 760, 440
    s += SL(Z_SRED, f'<rect x="{bx-40:.0f}" y="{by-40:.0f}" width="{bw+80:.0f}"'
                    f' height="{bh+120:.0f}" rx="10" fill="url(#derev)" stroke="{K}"'
                    f' stroke-width="7"/>')
    put = kontur_proema(bx, by, bw, 320, "pryam")
    buf = (f'<path d="{put}" fill="#b9a082"/>')
    buf += (f'<path d="{put}" fill="#dce7f2" opacity=".35"/>')
    buf += mesto_stoka(bx, by, bw, 320, "pryam")
    buf += (f'<path d="{put}" fill="none" stroke="#6b4428" stroke-width="22"/>')
    buf += (f'<path d="M{bx+bw*.5:.0f},{by:.0f} v320" stroke="#6b4428"'
            f' stroke-width="14"/>')
    buf += (f'<path d="M{bx+30:.0f},{by+290:.0f} q{bw*.2:.0f},{-40:.0f}'
            f' {bw*.42:.0f},{-16:.0f}" fill="none" stroke="#ffffff" stroke-width="9"'
            f' opacity=".28"/>')
    s += SL(Z_SRED, buf)
    s += SL(Z_SRED, f'<rect x="{bx-20:.0f}" y="{by+340:.0f}" width="{bw+40:.0f}"'
                    f' height="26" rx="6" fill="{DOSKA}" stroke="{K}" stroke-width="5"/>')
    for i in range(4):
        s += SL(Z_SRED, banka_moloka(bx + 110 + i * 180, by + 340, .58, t, True, .78,
                                     ["#8a2f22", "#d6a63f", "#6b3a6a", "#b5803a"][i]))
    # СТОЛ и ЧАЙНИК на пол-кадра
    s += SL(Z_SRED, stol(120, 800, 900, 44, True))
    s += SL(Z_SRED, chaynik_s_parom(520, 800, 2.3, t, .1, True))
    # розетки мёда и варенья, ложка, полотенце
    s += SL(Z_SRED, f'<ellipse cx="880" cy="796" rx="76" ry="24" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="880" cy="788" rx="58" ry="17" fill="#d6a63f"'
                    f' stroke="#b5803a" stroke-width="3"/>')
    s += SL(Z_SRED, f'<ellipse cx="1030" cy="800" rx="70" ry="22" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="1030" cy="792" rx="54" ry="15" fill="#8a2f22"'
                    f' stroke="#6b2419" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M960,790 l{70:.0f},{-36:.0f}" stroke="#c9ccd1"'
                    f' stroke-width="7"/>'
                    f'<ellipse cx="1040" cy="748" rx="24" ry="14" fill="#dde3e8"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="140" y="860" width="90" height="170" rx="6"'
                    f' fill="{RUSH}" stroke="{K}" stroke-width="4"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M150,{900+i*44:.0f} h70" stroke="{TKAN}"'
                        f' stroke-width="7" opacity=".9"/>')
    # ХОЗЯЙКА кладёт щепоть травы
    hx, hy, hh = 860, 1050, 680
    syp = ((t * 1.1) % 1.0)
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.3))
    s += SL(Z_SRED, f'<path d="M{hx-110:.0f},{hy-hh*.46:.0f} q{110:.0f},{-24:.0f}'
                    f' {220:.0f},0 l0,{hh*.32:.0f} q{-110:.0f},{24:.0f} {-220:.0f},0 Z"'
                    f' fill="{RUSH}" opacity=".9" stroke="{K}" stroke-width="4"/>')
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .34, -24, t, "#8a2f22", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .24, 20, t, "#8a2f22", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    for i in range(6):
        d = ((syp + i / 6.0) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{e1x-40+i*7:.0f}" cy="{e1y+30+150*d:.0f}"'
                        f' rx="5" ry="8" fill="#7d7040" opacity="{1-d:.2f}"'
                        f' transform="rotate({d*120:.0f} {e1x-40+i*7:.0f}'
                        f' {e1y+30+150*d:.0f})"/>')
    s += SL(Z_SRED, kot(1280, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, polka_s_bankami(560, 380, 520, t, 71, 4, False))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def puchok_s_cherdaka_korobka_i_meshoc(t):
    """Развилка из трёх частей: слева чердак — хозяин на стремянке снимает с
    жерди пучок мяты; в середине городская кухня — рукав достаёт с полки
    коробку с нарисованной ромашкой; справа посылка с полотняным мешочком."""
    rnd = random.Random(3008)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    # ЛЕВАЯ ЧАСТЬ: чердак
    s += SL(Z_DAL, f'<rect x="0" y="0" width="640" height="{H}" fill="#3f3122"/>')
    s += SL(Z_DAL, doski(0, 0, 640, H, 66, True, "dosk"))
    s += SL(Z_SRED, f'<path d="M0,180 L320,20 L640,180" fill="none" stroke="#5e4430"'
                    f' stroke-width="22"/>'
                    f'<path d="M100,240 h440" stroke="#8a6342" stroke-width="12"/>')
    for i, (px_, ph2) in enumerate(((180, .2), (300, .5), (420, .8))):
        s += SL(Z_SRED, puchok_trav(px_, 250, .9, t, ph2, 73 + i, "#6f8c4a"))
    s += SL(Z_SRED, f'<path d="M140,1070 l60,-520 M300,1070 l-20,-520" stroke="#7d5636"'
                    f' stroke-width="14"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{150+i*6:.0f},{620+i*100:.0f} h{130-i*8:.0f}"'
                        f' stroke="#8a6342" stroke-width="13"/>')
    hx, hy, hh = 300, 760, 560
    snyat = A.ease(A.seg(t, .5, 1.4))
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a3a", kant="#ffd98a",
                           boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .36, -40 - 14 * snyat, t,
                              "#3f4a3a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .28, -34, t, "#3f4a3a", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, puchok_trav(e1x, e1y + 10, .8, t, .3, 79, "#6f8c4a"))
    s += SL(Z_SRED, lampa(540, 200, t, 1.1, False) + teplo(540, 210, 240, 200, .40))
    # СРЕДНЯЯ ЧАСТЬ: городская кухня, рукав достаёт коробку
    s += SL(Z_DAL, f'<rect x="640" y="0" width="640" height="{H}" fill="#cbb492"/>')
    for i in range(6):
        s += SL(Z_DAL, f'<path d="M{660+i*110:.0f},0 v{H}" stroke="#b9a082"'
                       f' stroke-width="4" opacity=".5"/>')
    s += SL(Z_SRED, f'<rect x="680" y="420" width="560" height="22" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="680" y="640" width="560" height="22" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4.5"/>')
    for i in range(4):
        s += SL(Z_SRED, banka_moloka(740 + i * 130, 640, .56, t, True, .75,
                                     ["#8a2f22", "#d6a63f", "#6b3a6a", "#b5803a"][i]))
    dost = A.ease(A.seg(t, 1.0, 1.4))
    s += SL(Z_SRED, f'<rect x="{900+60*dost:.0f}" y="{300+40*dost:.0f}" width="170"'
                    f' height="120" rx="8" fill="#f2ead6" stroke="{K}"'
                    f' stroke-width="5"/>')
    s += SL(Z_SRED, f'<circle cx="{985+60*dost:.0f}" cy="{356+40*dost:.0f}" r="32"'
                    f' fill="#f8f4e8" stroke="#c9bfa6" stroke-width="3"/>')
    for i in range(8):
        a = i * .785
        s += SL(Z_SRED, f'<ellipse cx="{985+60*dost+26*math.cos(a):.0f}"'
                        f' cy="{356+40*dost+26*math.sin(a):.0f}" rx="12" ry="7"'
                        f' fill="#ffffff" stroke="#d8cbb0" stroke-width="2.4"'
                        f' transform="rotate({math.degrees(a):.0f}'
                        f' {985+60*dost+26*math.cos(a):.0f}'
                        f' {356+40*dost+26*math.sin(a):.0f})"/>')
    s += SL(Z_SRED, f'<circle cx="{985+60*dost:.0f}" cy="{356+40*dost:.0f}" r="12"'
                    f' fill="#d6a63f"/>')
    ruk, (kx_, ky_) = rukav(1270, 240, 300, 150, t, "#6b3a6a", "#ffd98a", .3, 4, True)
    s += SL(Z_SRED, ruk)
    s += SL(Z_SRED, chaynik_s_parom(760, 900, .9, t, .4, True))
    s += SL(Z_SRED, f'<rect x="640" y="900" width="640" height="24" fill="#8a7a62"'
                    f' stroke="{K}" stroke-width="4"/>')
    # ПРАВАЯ ЧАСТЬ: посылка с мешочком
    s += SL(Z_DAL, f'<rect x="1280" y="0" width="640" height="{H}" fill="#b9a082"/>')
    s += SL(Z_SRED, stol(1300, 760, 600, 40, True))
    s += SL(Z_SRED, f'<rect x="1400" y="520" width="420" height="240" rx="8"'
                    f' fill="#c9a05a" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1400,600 h420 M1610,520 v240" stroke="#a8824a"'
                    f' stroke-width="9"/>'
                    f'<path d="M1400,520 q{210:.0f},{-60:.0f} {420:.0f},0 l0,{40:.0f}'
                    f' q{-210:.0f},{-54:.0f} {-420:.0f},0 Z" fill="#b08a52"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    vyn = A.ease(A.seg(t, 1.6, 1.4))
    mx_, my_ = 1620, 520 - 120 * vyn
    s += SL(Z_SRED, f'<path d="M{mx_-60:.0f},{my_:.0f} q{60:.0f},{-30:.0f} {120:.0f},0'
                    f' q{14:.0f},{90:.0f} {-10:.0f},{150:.0f} q{-50:.0f},{20:.0f}'
                    f' {-100:.0f},0 q{-24:.0f},{-60:.0f} {-10:.0f},{-150:.0f} Z"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{mx_-50:.0f},{my_+10:.0f} q{50:.0f},{20:.0f} {100:.0f},0"'
                    f' fill="none" stroke="#b9a37a" stroke-width="7"/>')
    s += SL(Z_SRED, f'<rect x="{mx_+40:.0f}" y="{my_+40:.0f}" width="80" height="54"'
                    f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="3.6"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{mx_+50:.0f},{my_+58+i*14:.0f} q{24:.0f},{-6:.0f}'
                        f' {52:.0f},0" fill="none" stroke="#8a7a62" stroke-width="3"/>')
    ruk2, (k2x, k2y) = rukav(1900, 420, 280, 160, t, "#4a4450", "#ffd98a", .6, 4, True)
    s += SL(Z_SRED, ruk2)
    s += SL(Z_SRED, lampa(1600, 180, t, 1.2, True) + teplo(1600, 200, 280, 230, .40))
    # ВСЕ ТРИ ЧАСТИ ОБЖИТЫ: на чердаке короба и связки, на кухне полка с посудой,
    # на почтовом столе бумаги, бечёвка и вторая посылка
    for i, (kx2, ky2, ks2) in enumerate(((120, 980, 1.0), (430, 1000, .85),
                                         (520, 880, .7))):
        s += SL(Z_SRED, f'<rect x="{kx2-70*ks2:.0f}" y="{ky2-90*ks2:.0f}"'
                        f' width="{140*ks2:.0f}" height="{90*ks2:.0f}" rx="8"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="{4*ks2:.1f}"/>'
                        f'<path d="M{kx2-70*ks2:.0f},{ky2-60*ks2:.0f} h{140*ks2:.0f}"'
                        f' stroke="#6b4428" stroke-width="{5*ks2:.1f}"/>')
    for i, (lx2, ly2) in enumerate(((180, 520), (380, 560))):
        for k in range(4):
            s += SL(Z_SRED, f'<ellipse cx="{lx2+((k*7)%3-1)*24:.0f}"'
                            f' cy="{ly2+k*48:.0f}" rx="24" ry="30" fill="#c9a05a"'
                            f' stroke="{K}" stroke-width="3.2"/>')
    s += SL(Z_SRED, polka_s_bankami(700, 500, 520, t, 83, 4, False))
    s += SL(Z_SRED, hodiki(1180, 520, t, 1.1))
    s += SL(Z_SRED, f'<rect x="660" y="300" width="240" height="170" rx="10"'
                    f' fill="#b9c2c8" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M660,380 h240" stroke="#8a98a8" stroke-width="7"/>'
                    f'<circle cx="876" cy="340" r="10" fill="{MED}"/>')
    for i, (bx2, by2) in enumerate(((960, 760), (1120, 770), (820, 764))):
        s += SL(Z_SRED, kruzhka_moloka(bx2, by2, .8, t, False, i * .3, "#e8e2d6"))
    s += SL(Z_SRED, f'<rect x="1140" y="700" width="120" height="200" rx="10"'
                    f' fill="#dde3e8" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1140,790 h120" stroke="#b9c2c8" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="420" y="420" width="160" height="240" rx="8"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M420,540 h160" stroke="#54351f" stroke-width="6"/>')
    s += SL(Z_SRED, puchok_trav(560, 250, .8, t, .9, 89, "#6f8c4a"))
    s += SL(Z_SRED, f'<rect x="1300" y="300" width="200" height="150" rx="8"'
                    f' fill="#8a7a62" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1300,370 h200" stroke="#6f6256" stroke-width="6"/>')
    s += SL(Z_SRED, f'<rect x="700" y="1000" width="180" height="70" rx="8"'
                    f' fill="#b9a082" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="920" y="1010" width="150" height="60" rx="8"'
                    f' fill="#8a7a62" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<rect x="1320" y="620" width="180" height="120" rx="8"'
                    f' fill="#c9a05a" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M1320,680 h180 M1410,620 v120" stroke="#a8824a"'
                    f' stroke-width="7"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="{1340+i*90:.0f}" y="{780+((i*5)%3)*16:.0f}"'
                        f' width="76" height="54" rx="5" fill="#f2ead6" stroke="{K}"'
                        f' stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<circle cx="1860" cy="760" r="46" fill="#b9a37a" stroke="{K}"'
                    f' stroke-width="4.5"/>'
                    f'<circle cx="1860" cy="760" r="18" fill="#8a7a52"/>')
    s += SL(Z_PERED, f'<rect x="634" y="0" width="12" height="{H}" fill="#1d1611"'
                     f' opacity=".9"/>'
                     f'<rect x="1274" y="0" width="12" height="{H}" fill="#1d1611"'
                     f' opacity=".9"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def paketik_otdyhaet_chaynik_rabotaet(t):
    """Современная кухня: рукав опускает чайный пакетик обратно в коробку, а
    на стол ставят заварочный чайник — в него по словам ложатся липовый цвет,
    мята и зверобой. Женщина сыплет травы из трёх баночек."""
    rnd = random.Random(3009)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="660" fill="#d8cbb0"/>')
    for i in range(16):
        s += SL(Z_DAL, f'<rect x="{-10+i*124:.0f}" y="0" width="112" height="660"'
                       f' fill="#cfc2a8" opacity=".45"/>')
    s += SL(Z_DAL, okno_izby(1500, 130, 380, 380, t, None, .2, False, True))
    s += SL(Z_SRED, f'<rect x="0" y="660" width="{W}" height="40" fill="#8a7a62"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<rect x="0" y="700" width="{W}" height="380" fill="#b9a082"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{30+i*270:.0f}" y="720" width="230" height="340"'
                        f' rx="8" fill="#a8956f" stroke="{K}" stroke-width="4"/>'
                        f'<circle cx="{145+i*270:.0f}" cy="760" r="12" fill="{MED}"/>')
    # ЗАВАРОЧНЫЙ ЧАЙНИК на столе
    s += SL(Z_SRED, chaynik_s_parom(820, 660, 1.9, t, .1, True))
    # ТРИ БАНОЧКИ с травами, травы ложатся по словам
    for i, (bx_, col, nm) in enumerate(((1180, "#d6a63f", "липа"),
                                        (1320, "#56763f", "мята"),
                                        (1460, "#e4c46a", "зверобой"))):
        s += SL(Z_SRED, banka_moloka(bx_, 660, .62, t, True, .68, col))
        syp = A.ease(A.seg(t, .7 + i * .6, .6))
        if syp > .02:
            for k in range(5):
                d = ((t * 1.3 + k / 5.0) % 1.0)
                s += SL(Z_SRED, f'<ellipse cx="{bx_-(bx_-860)*d:.0f}"'
                                f' cy="{560+120*d*d:.0f}" rx="6" ry="9" fill="{col}"'
                                f' opacity="{syp*(1-d)*.95:.2f}"'
                                f' transform="rotate({d*160:.0f} {bx_-(bx_-860)*d:.0f}'
                                f' {560+120*d*d:.0f})"/>')
    # ПАКЕТИК возвращается в коробку
    vern = A.ease(A.seg(t, .3, 1.0))
    px_, py_ = 420 + 120 * vern, 520 + 80 * vern
    s += SL(Z_SRED, f'<rect x="500" y="600" width="150" height="100" rx="6"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M500,640 h150" stroke="#c9bfa6" stroke-width="5"/>')
    s += SL(Z_SRED, f'<path d="M{px_:.0f},{py_-120:.0f} l{4:.0f},{90:.0f}"'
                    f' stroke="#c9bfa6" stroke-width="3"/>'
                    f'<path d="M{px_-24:.0f},{py_-30:.0f} h48 l-6,56 h-36 Z"'
                    f' fill="#c9a05a" stroke="{K}" stroke-width="3.6"/>'
                    f'<rect x="{px_-14:.0f}" y="{py_-136:.0f}" width="28" height="20"'
                    f' rx="4" fill="#e8e2d6" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<path d="M300,660 h120 l-10,-96 h-100 Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="360" cy="564" rx="50" ry="14" fill="#f2ead6"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    # ЖЕНЩИНА у стола
    zx, zy, zh = 1020, 1050, 700
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#6b3a6a", kant="#ffd98a", ph=.3))
    s += SL(Z_SRED, f'<path d="M{zx-120:.0f},{zy-zh*.60:.0f} q{120:.0f},{-24:.0f}'
                    f' {240:.0f},0 l{14:.0f},{zh*.34:.0f} q{-134:.0f},{26:.0f}'
                    f' {-268:.0f},0 Z" fill="#8a5a8a" opacity=".9" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    r1, (e1x, e1y), _ = _ruka(zx, zy, zh, -1, zh * .30, -26, t, "#6b3a6a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(zx, zy, zh, 1, zh * .26, -18, t, "#6b3a6a", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    # электрочайник без названия, мёд, ложка, полотенце
    s += SL(Z_SRED, f'<path d="M1660,660 q{-10:.0f},{-120:.0f} {70:.0f},{-130:.0f}'
                    f' q{80:.0f},{10:.0f} {70:.0f},{130:.0f} Z" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1690" y="518" width="80" height="18" rx="5"'
                    f' fill="#9aa3a8" stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1800,580 q{40:.0f},{30:.0f} {0:.0f},{60:.0f}"'
                    f' fill="none" stroke="#8a98a8" stroke-width="11"/>')
    s += SL(Z_SRED, banka_moloka(220, 660, .78, t, True, .8, "#d6a63f"))
    s += SL(Z_SRED, f'<rect x="1880" y="700" width="40" height="160" rx="6"'
                    f' fill="{TKAN2}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, polka_s_bankami(440, 240, 520, t, 97, 5, False))
    s += SL(Z_SRED, hodiki(1180, 250, t, 1.2))
    s += SL(Z_SRED, lampa(960, 70, t, 1.3, True) + teplo(960, 90, 320, 260, .40))
    s += SL(Z_SRED, ten(zx, zy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.40)
    return s


def chay_nastaivaetsya(t):
    """Стол под абажуром: заварник с отбитым носиком под вязаной
    грелкой-курицей на пол-кадра, четыре блюдца с вареньем, сушки. Семья
    сидит вокруг, никто не тянется к чашкам, по циферблату ползёт улитка."""
    rnd = random.Random(3010)
    s = (f'<rect width="{W}" height="{H}" fill="#3f3122"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="700" fill="#5f4a32"/>')
    s += SL(Z_DAL, brevna(0, 0, W, 700, 84, 3))
    s += SL(Z_DAL, okno_izby(1560, 180, 320, 300, t, None, .6, False, True))
    s += SL(Z_SRED, polovicy(820, "#6b4428"))
    # ПЛИТА с большим чайником за столом
    s += SL(Z_SRED, f'<rect x="80" y="520" width="340" height="300" rx="8"'
                    f' fill="#8a8078" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="100" y="546" width="300" height="60" rx="6"'
                    f' fill="#6f6256" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, chaynik_s_parom(250, 540, 1.3, t, .2, True))
    # СТОЛ со скатертью
    s += SL(Z_SRED, f'<rect x="420" y="760" width="1180" height="40" rx="8"'
                    f' fill="#e8e2d6" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M420,800 q{590:.0f},{36:.0f} {1180:.0f},0 l0,{90:.0f}'
                    f' q{-590:.0f},{36:.0f} {-1180:.0f},0 Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<path d="M{450+i*100:.0f},800 l{-10:.0f},{90:.0f}"'
                        f' stroke="#d8cbb0" stroke-width="5"/>')
    # ЗАВАРНИК под грелкой-курицей
    gx, gy = 960, 760
    s += SL(Z_SRED, f'<path d="M{gx-120:.0f},{gy:.0f} q{-20:.0f},{-130:.0f}'
                    f' {120:.0f},{-150:.0f} q{140:.0f},{20:.0f} {120:.0f},{150:.0f} Z"'
                    f' fill="#c8301f" stroke="{K}" stroke-width="6"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{gx-110+i*36:.0f},{gy-10:.0f} q{10:.0f},{-70:.0f}'
                        f' {2:.0f},{-120:.0f}" fill="none" stroke="#a8321c"'
                        f' stroke-width="5" opacity=".85"/>')
    s += SL(Z_SRED, f'<circle cx="{gx+86:.0f}" cy="{gy-146:.0f}" r="44" fill="#c8301f"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{gx+112:.0f},{gy-168:.0f} q{26:.0f},{-14:.0f}'
                    f' {40:.0f},{6:.0f} l{-34:.0f},{22:.0f} Z" fill="{ZOL}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="{gx+100:.0f}" cy="{gy-156:.0f}" r="5" fill="{K}"/>'
                    f'<path d="M{gx+70:.0f},{gy-186:.0f} q{14:.0f},{-20:.0f}'
                    f' {28:.0f},{-2:.0f} q{-6:.0f},{16:.0f} {-28:.0f},{2:.0f} Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M{gx-140:.0f},{gy-30:.0f} q{-44:.0f},{-12:.0f}'
                    f' {-56:.0f},{-36:.0f} l{18:.0f},{-12:.0f} q{12:.0f},{22:.0f}'
                    f' {44:.0f},{30:.0f} Z" fill="#b5803a" stroke="{K}"'
                    f' stroke-width="4"/>')
    # блюдца с вареньем, сахарница, сушки
    for i, bx_ in enumerate((560, 740, 1180, 1360)):
        s += SL(Z_SRED, f'<ellipse cx="{bx_:.0f}" cy="760" rx="72" ry="22"'
                        f' fill="#e8e2d6" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{bx_:.0f}" cy="752" rx="54" ry="15"'
                        f' fill="#8a2f22" stroke="#6b2419" stroke-width="3"/>')
    s += SL(Z_SRED, f'<path d="M1480,760 q{-6:.0f},{-70:.0f} {58:.0f},{-74:.0f}'
                    f' q{64:.0f},{4:.0f} {58:.0f},{74:.0f} Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{480+i*34:.0f}" cy="{730-((i*5)%3)*16:.0f}" r="26"'
                        f' fill="none" stroke="#c9a05a" stroke-width="13"/>')
    # ЧЕТВЕРО за столом
    for i, (fx_, fy_, fh_, col, pl) in enumerate(((620, 1060, 560, "#4a4038", False),
                                                  (820, 1070, 520, "#8a2f22", True),
                                                  (1180, 1066, 480, "#3f5a6a", False),
                                                  (1400, 1056, 500, "#6b3a6a", True))):
        s += SL(Z_SRED, figura(fx_, fy_, fh_, t, col=col, kant="#ffd98a",
                               platok=pl, boroda=(i == 0), ph=i * .3))
        rk, (ex, ey), _ = _ruka(fx_, fy_, fh_, 1, fh_ * .24, 46, t, col, "#ffd98a", i * .25, 3)
        rk2, (e2x_, e2y_), _ = _ruka(fx_, fy_, fh_, -1, fh_ * .24, 50, t, col,
                                     "#ffd98a", i * .25 + .4, 3)
        s += SL(Z_SRED, rk + rk2)
    # АБАЖУР и ходики с улиткой
    s += SL(Z_SRED, f'<path d="M700,0 v120" stroke="#6b4428" stroke-width="7"/>')
    s += SL(Z_SRED, lampa(700, 120, t, 2.0, True) + teplo(700, 170, 520, 420, .55))
    s += SL(Z_SRED, hodiki(1760, 560, t, 1.8))
    ulit = ((t * .12) % 1.0)
    a = -1.57 + ulit * 6.283
    s += SL(Z_SRED, f'<ellipse cx="{1760+54*math.cos(a):.0f}"'
                    f' cy="{560+54*math.sin(a)+40:.0f}" rx="18" ry="11" fill="#9a7c45"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<circle cx="{1760+54*math.cos(a)+6:.0f}"'
                    f' cy="{560+54*math.sin(a)+34:.0f}" r="11" fill="#b08a52"'
                    f' stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, kot(500, 1050, t, 1.5, "#3b3430", True))
    s += SL(Z_SRED, polka_s_bankami(1180, 300, 420, t, 101, 4, False))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def kust_kaliny_v_inee(t):
    """Куст калины у забора на пол-кадра, красные кисти в белом инее; просвет
    между досками расширен до окна — в нём настоящая калина. Рисованный Мороз
    дышит на куст, ягоды разгораются, горечь улетает зелёными рожицами."""
    rnd = random.Random(3011)
    s = nebo("rassv", t, False, 409)
    s += oblaka(t, 150, 4, 193, .34, "#ffe9c8")
    s += SL(Z_DAL, ulica_dal(1180, 360, 740, t, True, 151))
    s += SL(Z_DAL, izba_snaruzhi(1560, 380, 280, t, True, True, 103)
            + dym_stolbom(1588, 240, t, 260, .45, .4, 6))
    s += SL(Z_SRED, _merzlaya_zemlya(560, 409, False))
    s += SL(Z_SRED, sneg_lezhit(600, 30, "url(#sneg)"))
    # ЗАБОР с дорисованным окном-просветом
    s += SL(Z_SRED, zabor_shtaket(-40, 300, 1060, 420, 409, 64))
    px, py, pw, ph_ = 120, 340, 780, 320
    pr = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
          f' fill="#8aa8b4"/>')
    pr += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.4:.0f}"'
           f' fill="#c4d8e8"/>')
    pr += mesto_stoka(px, py, pw, ph_, "pryam")
    pr += (f'<rect x="{px-16:.0f}" y="{py-16:.0f}" width="{pw+32:.0f}"'
           f' height="{ph_+32:.0f}" rx="6" fill="none" stroke="#7d5636"'
           f' stroke-width="24"/>')
    s += SL(Z_SRED, pr)
    # КУСТ КАЛИНЫ на пол-кадра
    kx, kb = 1180, 1010
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{kb:.0f} q{-20:.0f},{-200:.0f} {-80:.0f},{-360:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{10:.0f},{-220:.0f} {70:.0f},{-380:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{40:.0f},{-180:.0f} {170:.0f},{-300:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{-60:.0f},{-160:.0f} {-190:.0f},{-250:.0f}"'
                    f' fill="none" stroke="#5e4430" stroke-width="14"/>')
    razg = A.ease(A.seg(t, 1.0, 1.6))
    for i, (gx_, gy_, gs) in enumerate(((1100, 660, 1.5), (1250, 630, 1.3),
                                        (1350, 720, 1.2), (990, 760, 1.25),
                                        (1180, 790, 1.4), (1430, 660, 1.0))):
        s += SL(Z_SRED, kalina_grozd(gx_, gy_, t, gs * (1 + .06 * razg), 13,
                                     409 + i, i * .2, True))
    for i in range(8):
        s += SL(Z_SRED, f'<path d="M{980+i*70:.0f},{600+((i*7)%4)*60:.0f}'
                        f' q{30:.0f},{-20:.0f} {60:.0f},{4:.0f}" fill="none"'
                        f' stroke="{INEY}" stroke-width="5" opacity=".7"/>')
    # МОРОЗ дышит на куст
    s += SL(Z_SRED, moroz_ded(1700, 1040, t, 1.0, .3))
    dyh = ((t * .7) % 1.0)
    for i in range(6):
        d = ((dyh + i / 6.0) % 1.0)
        s += SL(Z_SRED, f'<ellipse cx="{1640-320*d:.0f}" cy="{760+30*math.sin(i+d*4):.0f}"'
                        f' rx="{24+50*d:.0f}" ry="{16+30*d:.0f}" fill="#eaf6ff"'
                        f' opacity="{(1-d)*.5:.2f}"/>')
    # РОЖИЦЫ-ГОРЕЧИ улетают
    for i in range(5):
        d = ((t * .5 + i / 5.0) % 1.0)
        rx_ = 1180 + 300 * d
        ry_ = 700 - 320 * d
        s += SL(Z_LETIT, f'<g opacity="{(1-d)*.85:.2f}">'
                         f'<circle cx="{rx_:.0f}" cy="{ry_:.0f}" r="22" fill="#6f8c4a"'
                         f' stroke="{K}" stroke-width="3.4"/>'
                         f'<circle cx="{rx_-7:.0f}" cy="{ry_-5:.0f}" r="4" fill="{K}"/>'
                         f'<circle cx="{rx_+7:.0f}" cy="{ry_-5:.0f}" r="4" fill="{K}"/>'
                         f'<path d="M{rx_-9:.0f},{ry_+9:.0f} q{9:.0f},{-8:.0f} {18:.0f},0"'
                         f' fill="none" stroke="{K}" stroke-width="3"/></g>')
    # ХОЗЯЙКА с корзиной тянется к кисти
    hx, hy, hh = 760, 1056, 660
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a3a52", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.3))
    tyan = A.ease(A.seg(t, .8, 1.4))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * (.28 + .08 * tyan), -34, t,
                              "#4a3a52", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .26, 40, t, "#4a3a52", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x + 8, e1y + 6, 1.0, 16, "#8a2f22", t, .2) + r2)
    s += SL(Z_SRED, f'<path d="M{e2x-54:.0f},{e2y+10:.0f} q{54:.0f},{20:.0f} {108:.0f},0'
                    f' l{-12:.0f},{76:.0f} h{-84:.0f} Z" fill="#b08a52" stroke="{K}"'
                    f' stroke-width="4.5"/>')
    s += SL(Z_SRED, para_izo_rta(hx - 32, hy - hh * .80, t, .4, 1.0, .5))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    # синицы и калитка
    for i, (sx_, sy_) in enumerate(((1320, 560), (1460, 620))):
        s += SL(Z_SRED, ptica(sx_, sy_, t, 1.5, "#d6a63f", i * .4, "#4a6a78"))
    s += SL(Z_SRED, kalitka_rez(1760, 620, 180, 280, t, .12, True))
    s += SL(Z_SRED, inej_mel(409, 50, 960, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 16, 103, .34, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def vetka_s_kusta_i_puchok_s_rynka(t):
    """Кадр надвое: слева свой куст — хозяин секатором срезает ветку с тремя
    кистями; справа рыночный прилавок под навесом — продавщица протягивает
    покупательнице пучок калины, перевязанный ниткой."""
    rnd = random.Random(3012)
    s = nebo("den", t, False, 419)
    s += oblaka(t, 140, 5, 197, .40)
    # ЛЕВАЯ ПОЛОВИНА: свой куст
    s += SL(Z_DAL, ulica_dal(40, 420, 820, t, True, 157))
    s += SL(Z_SRED, _merzlaya_zemlya(600, 419, False))
    s += SL(Z_SRED, sneg_lezhit(640, 30, "url(#sneg)"))
    s += SL(Z_SRED, zabor_shtaket(-40, 420, 940, 220, 419, 62))
    kx, kb = 420, 1000
    s += SL(Z_SRED, f'<path d="M{kx:.0f},{kb:.0f} q{-20:.0f},{-180:.0f} {-70:.0f},{-320:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{14:.0f},{-200:.0f} {80:.0f},{-340:.0f}'
                    f' M{kx:.0f},{kb:.0f} q{50:.0f},{-150:.0f} {160:.0f},{-250:.0f}"'
                    f' fill="none" stroke="#5e4430" stroke-width="13"/>')
    srez = A.ease(A.seg(t, .8, .8))
    for i, (gx_, gy_, gs) in enumerate(((330, 700, 1.3), (470, 660, 1.2),
                                        (560, 760, 1.1))):
        dy_ = 180 * srez if i == 2 else 0
        s += SL(Z_SRED, kalina_grozd(gx_, gy_ + dy_, t, gs, 12, 419 + i, i * .25, True))
    hx, hy, hh = 700, 1056, 680
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a3a", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .34, -30, t, "#3f4a3a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .26, -22, t, "#3f4a3a", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x - 8, e1y + 8, 1.0, -16, "#6b4428", t, .2) + r2)
    rask = 26 * (1 - srez)
    s += SL(Z_SRED, f'<g transform="rotate(-24 {e1x:.0f} {e1y:.0f})">'
                    f'<path d="M{e1x-10:.0f},{e1y-10:.0f} l{-70:.0f},{-30-rask:.0f}'
                    f' M{e1x-10:.0f},{e1y+6:.0f} l{-70:.0f},{14+rask:.0f}"'
                    f' stroke="#c9ccd1" stroke-width="9"/>'
                    f'<circle cx="{e1x-6:.0f}" cy="{e1y-2:.0f}" r="9" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="3"/></g>')
    s += SL(Z_SRED, para_izo_rta(hx - 34, hy - hh * .80, t, .3, 1.0, .5))
    # ПРАВАЯ ПОЛОВИНА: рыночный прилавок
    s += SL(Z_DAL, f'<rect x="{W*.5:.0f}" y="0" width="{W*.5:.0f}" height="{H}"'
                   f' fill="#8a98a8" opacity=".25"/>')
    nav = 4.0 * A.w(t, 3.0, .2)
    s += SL(Z_SRED, f'<g transform="rotate({nav:.1f} 1440 420)">'
                    f'<path d="M1020,420 q{420:.0f},{-80:.0f} {840:.0f},0 l{-20:.0f},{44:.0f}'
                    f' q{-400:.0f},{-70:.0f} {-800:.0f},0 Z" fill="#8a2f22"'
                    f' stroke="{K}" stroke-width="5.5"/></g>'
                    f'<rect x="1030" y="440" width="18" height="300" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="1840" y="440" width="18" height="300" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="1000" y="740" width="900" height="50" rx="8"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="1020" y="790" width="860" height="26" rx="5"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="4"/>')
    # весы, банки с мёдом, клюква в лотке
    s += SL(Z_SRED, f'<path d="M1120,740 l0,-120" stroke="{ZHELEZ}" stroke-width="9"/>'
                    f'<path d="M1040,620 h160" stroke="{ZHELEZ}" stroke-width="7"/>'
                    f'<path d="M1050,620 q{10:.0f},{50:.0f} {-6:.0f},{64:.0f}'
                    f' M1190,620 q{-10:.0f},{50:.0f} {6:.0f},{64:.0f}" fill="none"'
                    f' stroke="#9aa3a8" stroke-width="3.4"/>'
                    f'<ellipse cx="1046" cy="690" rx="46" ry="14" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<ellipse cx="1196" cy="690" rx="46" ry="14" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="3.6"/>')
    for i in range(3):
        s += SL(Z_SRED, banka_moloka(1280 + i * 100, 740, .66, t, True, .82, "#d6a63f"))
    s += SL(Z_SRED, f'<rect x="1600" y="672" width="260" height="68" rx="8"'
                    f' fill="#b08a52" stroke="{K}" stroke-width="4.5"/>')
    for i in range(22):
        s += SL(Z_SRED, f'<circle cx="{1620+((i*53)%230):.0f}" cy="{690+((i*31)%40):.0f}"'
                        f' r="9" fill="#c8301f" stroke="#7d1b11" stroke-width="2"/>')
    # ПРОДАВЩИЦА и ПОКУПАТЕЛЬНИЦА
    per = A.ease(A.seg(t, 1.0, 1.6))
    px_, py_, ph_ = 1200, 1050, 640
    s += SL(Z_SRED, figura(px_, py_, ph_, t, col="#3f4a3a", kant="#ffd9a8",
                           platok=True, tulup=True, ph=.4))
    r3, (e3x, e3y), _ = _ruka(px_, py_, ph_, 1, ph_ * .30, -10, t, "#3f4a3a", "#ffd9a8", .3, 4)
    s += SL(Z_SRED, r3)
    zx_, zy_, zh_ = 1680, 1056, 650
    s += SL(Z_SRED, figura(zx_, zy_, zh_, t, col="#6b3a6a", kant="#ffd9a8", ph=.8))
    r4, (e4x, e4y), _ = _ruka(zx_, zy_, zh_, -1, zh_ * .30, -6, t, "#6b3a6a", "#ffd9a8", .5, 4)
    r5, (e5x, e5y), _ = _ruka(zx_, zy_, zh_, 1, zh_ * .24, 52, t, "#6b3a6a", "#ffd9a8", .9, 4)
    s += SL(Z_SRED, r4 + r5)
    s += SL(Z_SRED, f'<path d="M{e5x-40:.0f},{e5y+12:.0f} h80 l-8,72 h-64 Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    bx_ = e3x + (e4x - e3x) * per
    by_ = e3y + (e4y - e3y) * per
    s += SL(Z_SRED, kalina_grozd(bx_, by_ + 60, t, 1.1, 12, 431, .3, True)
            + f'<path d="M{bx_-24:.0f},{by_+18:.0f} h48" stroke="#b9a37a"'
              f' stroke-width="7"/>')
    s += SL(Z_SRED, para_izo_rta(px_ - 32, py_ - ph_ * .80, t, .3, .9, .45)
            + para_izo_rta(zx_ - 30, zy_ - zh_ * .80, t, .8, .9, .45))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45) + ten(px_, py_ + 6, 120, 20, .4)
            + ten(zx_, zy_ + 6, 120, 20, .4))
    s += SL(Z_PERED, f'<rect x="{W*.5-7:.0f}" y="0" width="14" height="{H}"'
                     f' fill="#dcecf8" opacity=".45"/>')
    s += SL(Z_SRED, dym_stolbom(240, 420, t, 280, .45, .4, 6))
    s += SL(Z_SRED, par(1240, 1000, t, 4, .5, 160, .45, 1.0))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def kalina_s_saharom_v_banke(t):
    """Кухонный стол: миска с калиной, деревянная толкушка, сахар в совке и
    чистая банка на пол-кадра. Хозяйка давит ягоды и перекладывает красное с
    прослойками сахара в банку; листки численника отлетают."""
    rnd = random.Random(3013)
    s = stena_gornicy_19(t, 41, 820, True, True)
    s += SL(Z_DAL, okno_izby(1500, 180, 360, 320, t, None, .7, False, True))
    s += SL(Z_SRED, stol(120, 760, 1120, 46, True))
    # МИСКА с калиной и толкушка
    s += SL(Z_SRED, f'<path d="M260,760 q{-16:.0f},{-110:.0f} {150:.0f},{-120:.0f}'
                    f' q{170:.0f},{10:.0f} {150:.0f},{120:.0f} Z" fill="#b9a082"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<ellipse cx="410" cy="648" rx="152" ry="38" fill="#8a2f22"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    davl = abs(A.w(t, 1.1, .0))
    for i in range(14):
        a = i * .45
        s += SL(Z_SRED, f'<circle cx="{410+110*math.cos(a)*.9:.0f}"'
                        f' cy="{644+26*math.sin(a):.0f}" r="{12-4*davl:.0f}"'
                        f' fill="#c8301f" stroke="#7d1b11" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<rect x="{392:.0f}" y="{420+60*davl:.0f}" width="36" height="200"'
                    f' rx="12" fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="410" cy="{620+60*davl:.0f}" rx="56" ry="22"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="4.5"/>')
    # САХАР в совке
    s += SL(Z_SRED, f'<path d="M700,760 h190 l-14,-80 h-162 Z" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="795" cy="680" rx="81" ry="20" fill="#f8f4e8"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M880,700 l{70:.0f},{-40:.0f}" stroke="#9aa3a8"'
                    f' stroke-width="9"/>')
    # БАНКА на пол-кадра, наполняется прослойками
    nap = A.ease(A.seg(t, .8, 3.2))
    bx, by = 1180, 780
    s += SL(Z_SRED, f'<path d="M{bx-110:.0f},{by-420:.0f} q0,{-50:.0f} {30:.0f},{-60:.0f}'
                    f' h{160:.0f} q{30:.0f},{10:.0f} {30:.0f},{60:.0f} l0,{420:.0f}'
                    f' q{-110:.0f},{30:.0f} {-220:.0f},0 Z" fill="{STEKLO}"'
                    f' opacity=".55" stroke="{K}" stroke-width="6"/>')
    for i in range(6):
        if nap * 6 < i:
            break
        yy = by - 30 - i * 64
        s += SL(Z_SRED, f'<rect x="{bx-104:.0f}" y="{yy-40:.0f}" width="208" height="44"'
                        f' rx="6" fill="#8a2f22" opacity=".95"/>'
                        f'<rect x="{bx-104:.0f}" y="{yy-56:.0f}" width="208" height="18"'
                        f' rx="4" fill="#f8f4e8" opacity=".9"/>')
    s += SL(Z_SRED, f'<path d="M{bx-86:.0f},{by-400:.0f} q{-10:.0f},{200:.0f}'
                    f' {4:.0f},{340:.0f}" fill="none" stroke="#ffffff"'
                    f' stroke-width="12" opacity=".4"/>')
    # ЛИСТКИ численника отлетают
    s += SL(Z_SRED, f'<rect x="1560" y="560" width="170" height="220" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1560" y="560" width="170" height="44" rx="8"'
                    f' fill="#3f6b7a" stroke="{K}" stroke-width="4"/>')
    for i in range(3):
        d = ((t * .55 + i * .33) % 1.0)
        s += SL(Z_LETIT, f'<rect x="{1580-240*d:.0f}" y="{620+280*d*d:.0f}" width="110"'
                         f' height="140" rx="6" fill="#f2ead6" opacity="{(1-d)*.85:.2f}"'
                         f' transform="rotate({-d*150:.0f} {1635-240*d:.0f}'
                         f' {690+280*d*d:.0f})" stroke="{K}" stroke-width="3"/>')
    # ХОЗЯЙКА
    hx, hy, hh = 700, 1050, 680
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#8a2f22", kant="#ffd98a",
                           platok=True, ph=.3))
    s += SL(Z_SRED, f'<path d="M{hx-110:.0f},{hy-hh*.46:.0f} q{110:.0f},{-24:.0f}'
                    f' {220:.0f},0 l0,{hh*.32:.0f} q{-110:.0f},{24:.0f} {-220:.0f},0 Z"'
                    f' fill="{RUSH}" opacity=".9" stroke="{K}" stroke-width="4"/>')
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .34, -24 + 12 * davl, t,
                              "#8a2f22", "#ffd98a", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .24, 6, t, "#8a2f22", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, kot(1480, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, polka_s_bankami(180, 400, 520, t, 103, 5, False))
    s += SL(Z_SRED, f'<rect x="900" y="820" width="90" height="170" rx="6"'
                    f' fill="{RUSH}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(960, 120, t, 1.3, True) + teplo(960, 150, 340, 280, .45))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def pirog_s_kalinoy(t):
    """Стол: на доске большой закрытый пирог на пол-кадра, в прорезях сверху
    видна тёмно-красная начинка, идёт пар. Бабушка держит край доски
    прихватками, двое внуков подняли носы и принюхиваются."""
    rnd = random.Random(3014)
    s = stena_gornicy_19(t, 43, 820, True, True)
    s += SL(Z_SRED, pech(1500, 280, 420, 540, t, True, True, False))
    s += SL(Z_SRED, ogon(1660, 700, t, 1.2, .2, 6) + teplo(1660, 680, 360, 300, .5))
    s += SL(Z_SRED, stol(160, 780, 1120, 46, True))
    # ДОСКА и ПИРОГ на пол-кадра
    s += SL(Z_SRED, f'<rect x="300" y="740" width="840" height="46" rx="10"'
                    f' fill="#b9a082" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1140,760 q{70:.0f},{4:.0f} {90:.0f},{-14:.0f}'
                    f' l0,{34:.0f} q{-30:.0f},{20:.0f} {-90:.0f},{10:.0f} Z"'
                    f' fill="#a8956f" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<path d="M360,740 q{360:.0f},{-230:.0f} {720:.0f},0'
                    f' q{-40:.0f},{40:.0f} {-360:.0f},{40:.0f} q{-320:.0f},0'
                    f' {-360:.0f},{-40:.0f} Z" fill="#d6a63f" stroke="{K}"'
                    f' stroke-width="7"/>')
    for i in range(5):
        px_ = 520 + i * 90
        s += SL(Z_SRED, f'<path d="M{px_:.0f},{640+((i*5)%3)*18:.0f}'
                        f' q{30:.0f},{-26:.0f} {60:.0f},{-2:.0f} q{-26:.0f},{22:.0f}'
                        f' {-60:.0f},{2:.0f} Z" fill="#8a2f22" stroke="#6b2419"'
                        f' stroke-width="3.4"/>')
        s += SL(Z_SRED, par(px_ + 30, 600 + ((i * 5) % 3) * 18, t, 3, .5, 150, .4, .9))
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{420+i*110:.0f},720 q{30:.0f},{-20:.0f} {56:.0f},{-2:.0f}"'
                        f' fill="none" stroke="#c09a3a" stroke-width="5" opacity=".8"/>')
    # струйка запаха
    for i in range(6):
        d = ((t * .5 + i / 6.0) % 1.0)
        s += SL(Z_SRED, f'<path d="M{700+40*math.sin(i+d*5):.0f},{560-220*d:.0f}'
                        f' q{40:.0f},{-40:.0f} {4:.0f},{-80:.0f}" fill="none"'
                        f' stroke="#d89a90" stroke-width="{7-3*d:.1f}"'
                        f' opacity="{(1-d)*.55:.2f}"/>')
    # БАБУШКА держит край доски
    bx, by, bh = 1240, 1050, 680
    s += SL(Z_SRED, figura(bx, by, bh, t, col="#4a3a52", kant="#ffd98a",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(bx, by, bh, -1, bh * .34, -12, t, "#4a3a52", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(bx, by, bh, 1, bh * .26, 22, t, "#4a3a52", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x - 10, e1y + 8, 1.2, -14, "#8a2f22", t, .2)
            + r2 + varezhka(e2x + 10, e2y + 10, 1.2, 14, "#8a2f22", t, .7))
    # ДВОЕ ВНУКОВ принюхиваются
    for i, (vx_, vy_, vh_, col) in enumerate(((620, 1066, 440, "#3f5a6a"),
                                              (860, 1056, 420, "#c8301f"))):
        nos = 6 * A.w(t, 1.6, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({-10-nos:.1f} {vx_:.0f} {vy_-vh_*.5:.0f})">'
                + figura(vx_, vy_, vh_, t, col=col, kant="#ffd98a", ph=i * .4) + '</g>')
        rk, (ex, ey), _ = _ruka(vx_, vy_, vh_, 1, vh_ * .24, 52, t, col, "#ffd98a", i * .3, 4)
        s += SL(Z_SRED, rk)
    # нож, полотенце, чайник, кот
    s += SL(Z_SRED, f'<path d="M200,780 l{150:.0f},{-26:.0f} l{14:.0f},{20:.0f}'
                    f' l{-160:.0f},{30:.0f} Z" fill="#c9ccd1" stroke="{K}"'
                    f' stroke-width="4"/>'
                    f'<rect x="348" y="736" width="64" height="22" rx="6"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<rect x="180" y="840" width="90" height="170" rx="6"'
                    f' fill="{RUSH}" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, chaynik_s_parom(1440, 780, 1.0, t, .4, True))
    kot_ = A.ease(A.seg(t, 1.4, 1.2))
    s += SL(Z_SRED, f'<g transform="translate(0,{-60*kot_:.0f})">'
            + kot(1060, 1060, t, 1.6, "#3b3430", False) + '</g>')
    s += SL(Z_SRED, polka_s_bankami(240, 380, 500, t, 107, 4, False))
    s += SL(Z_SRED, ten(bx, by + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def kalinovoe_varene_v_rozetke(t):
    """Стол с чаем, две розетки калинового варенья: дед подносит ложку ко рту
    и крякает от горчинки, внучка высунула язык от старания и вылавливает
    ягоды по одной на край блюдца."""
    rnd = random.Random(3015)
    s = stena_gornicy_19(t, 47, 840, True, True)
    s += SL(Z_DAL, okno_izby(1540, 200, 340, 300, t, None, .5, False, True))
    s += SL(Z_SRED, stol(200, 780, 1180, 46, True))
    # ДВЕ РОЗЕТКИ варенья на треть кадра
    for i, rx_ in enumerate((620, 1120)):
        s += SL(Z_SRED, f'<ellipse cx="{rx_:.0f}" cy="780" rx="170" ry="54"'
                        f' fill="#e8e2d6" stroke="{K}" stroke-width="6"/>'
                        f'<ellipse cx="{rx_:.0f}" cy="762" rx="140" ry="42"'
                        f' fill="#f2ead6" stroke="{K}" stroke-width="4"/>'
                        f'<ellipse cx="{rx_:.0f}" cy="758" rx="112" ry="32"'
                        f' fill="#8a2f22" stroke="#6b2419" stroke-width="4"/>')
        for k in range(7):
            a = k * .9
            s += SL(Z_SRED, f'<circle cx="{rx_+72*math.cos(a)*.9:.0f}"'
                            f' cy="{756+18*math.sin(a):.0f}" r="12" fill="#c8301f"'
                            f' stroke="#7d1b11" stroke-width="2.6"/>')
    # ДЕД с ложкой и стаканом в подстаканнике
    dx, dy, dh = 420, 1050, 660
    lozh = A.ease(A.seg(t, .6, 1.2))
    s += SL(Z_SRED, f'<rect x="{dx-90:.0f}" y="{dy-20:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(dx, dy - 10, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, ph=.2))
    s += SL(Z_SRED, f'<path d="M{dx-80:.0f},{dy-dh*.62:.0f} q{80:.0f},{-20:.0f}'
                    f' {160:.0f},0 l{10:.0f},{dh*.30:.0f} q{-90:.0f},{24:.0f}'
                    f' {-180:.0f},0 Z" fill="#3f4a3a" stroke="{K}" stroke-width="4.5"/>')
    r1, (e1x, e1y), _ = _ruka(dx, dy - 10, dh, 1, dh * .30, -34 - 16 * lozh, t,
                              "#4a4038", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy - 10, dh, -1, dh * .26, 20, t,
                              "#4a4038", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{50:.0f},{-20:.0f}"'
                    f' stroke="#c9ccd1" stroke-width="6"/>'
                    f'<ellipse cx="{e1x+62:.0f}" cy="{e1y-24:.0f}" rx="22" ry="13"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<path d="M{e2x-30:.0f},{e2y+10:.0f} h60 l-6,74 h-48 Z"'
                    f' fill="{STEKLO}" opacity=".6" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e2x-34:.0f},{e2y+6:.0f} h68 l-8,86 h-52 Z"'
                    f' fill="none" stroke="{MED}" stroke-width="6"/>'
                    f'<path d="M{e2x+34:.0f},{e2y+30:.0f} q{28:.0f},{16:.0f} {0:.0f},{34:.0f}"'
                    f' fill="none" stroke="{MED}" stroke-width="6"/>')
    s += SL(Z_SRED, par(e2x, e2y - 10, t, 3, .45, 130, .4, .8))
    # ВНУЧКА вылавливает ягоды
    vx, vy, vh = 1320, 1056, 520
    vyl = A.ease(A.seg(t, 1.0, 1.4))
    s += SL(Z_SRED, f'<rect x="{vx-80:.0f}" y="{vy-20:.0f}" width="160" height="24"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(vx, vy - 10, vh, t, col="#c8301f", kant="#ffd98a",
                           ph=.6, naklon=2.0))
    r3, (e3x, e3y), _ = _ruka(vx, vy - 10, vh, -1, vh * .34, -16 + 14 * vyl, t,
                              "#c8301f", "#ffd98a", .3, 5)
    r4, (e4x, e4y), _ = _ruka(vx, vy - 10, vh, 1, vh * .24, 36, t,
                              "#c8301f", "#ffd98a", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    s += SL(Z_SRED, f'<path d="M{e3x:.0f},{e3y:.0f} l{-54:.0f},{-16:.0f}"'
                    f' stroke="#c9ccd1" stroke-width="6"/>'
                    f'<ellipse cx="{e3x-66:.0f}" cy="{e3y-20:.0f}" rx="20" ry="12"'
                    f' fill="#dde3e8" stroke="{K}" stroke-width="3.2"/>'
                    f'<circle cx="{e3x-66:.0f}" cy="{e3y-24:.0f}" r="9" fill="#c8301f"'
                    f' opacity="{vyl:.2f}"/>')
    # ягоды, сложенные на край блюдца
    for i in range(4):
        if vyl * 4 < i:
            break
        s += SL(Z_SRED, f'<circle cx="{1240+i*26:.0f}" cy="742" r="11" fill="#c8301f"'
                        f' stroke="#7d1b11" stroke-width="2.6"/>')
    # сушки, чайник, сахарница, кот
    for i in range(5):
        s += SL(Z_SRED, f'<circle cx="{880+i*30:.0f}" cy="{740-((i*5)%3)*14:.0f}" r="24"'
                        f' fill="none" stroke="#c9a05a" stroke-width="12"/>')
    s += SL(Z_SRED, chaynik_s_parom(1600, 780, 1.0, t, .3, True))
    s += SL(Z_SRED, f'<path d="M260,780 q{-6:.0f},{-66:.0f} {56:.0f},{-70:.0f}'
                    f' q{62:.0f},{4:.0f} {56:.0f},{70:.0f} Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="316" cy="706" rx="52" ry="14" fill="#d8cbb0"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, kot(900, 1056, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, polka_s_bankami(240, 400, 480, t, 109, 4, False))
    s += SL(Z_SRED, lampa(960, 130, t, 1.4, True) + teplo(960, 160, 360, 300, .46))
    s += SL(Z_SRED, ten(dx, dy + 20, 130, 22, .45) + ten(vx, vy + 20, 110, 19, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def obuh_po_uglam_doma(t):
    """Угол бревенчатого дома зимним днём: хозяин обухом топора стучит по
    углу сруба, по косяку, по перилам и воротам — и от каждого удара из щелей
    выскакивают мелкие рисованные чертенята и улепётывают за забор."""
    rnd = random.Random(3016)
    s = nebo("den", t, False, 431)
    s += oblaka(t, 140, 5, 199, .40)
    s += SL(Z_DAL, ulica_dal(1240, 420, 700, t, True, 163))
    # УГОЛ ДОМА на пол-кадра
    s += SL(Z_SRED, f'<rect x="0" y="120" width="980" height="760" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, brevna(0, 120, 980, 760, 86, 1))
    s += SL(Z_SRED, f'<path d="M980,120 l340,120 l0,760 l-340,-120 Z" fill="#5e4430"'
                    f' stroke="{K}" stroke-width="6"/>')
    for i in range(8):
        s += SL(Z_SRED, f'<path d="M980,{160+i*86:.0f} l340,120" stroke="#4a3526"'
                        f' stroke-width="7" opacity=".8"/>')
    s += SL(Z_SRED, f'<path d="M-20,120 l500,-110 l860,230 l0,60 l-860,-220 l-500,110 Z"'
                    f' fill="#4a3526" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-20,110 l500,-112 l860,232" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="20" opacity=".92"/>')
    # крыльцо с перилами, дверь с косяком
    s += SL(Z_SRED, f'<rect x="200" y="620" width="300" height="260" rx="6"'
                    f' fill="#3f2d1c" stroke="{K}" stroke-width="6"/>'
                    f'<rect x="170" y="590" width="360" height="36" rx="6"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, f'<rect x="120" y="880" width="520" height="30" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="140" y="910" width="480" height="26" rx="5"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M150,880 l0,-120 M600,880 l0,-120" stroke="#7d5636"'
                    f' stroke-width="14"/>'
                    f'<path d="M150,790 h450" stroke="#8a6342" stroke-width="11"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(920, 431, False))
    s += SL(Z_SRED, sneg_lezhit(940, 28, "url(#sneg)"))
    # ХОЗЯИН с топором
    ud = abs(A.w(t, .9, .0))
    hx, hy, hh = 1180, 1050, 700
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a3a", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, -1, hh * .32, -14 + 30 * ud, t,
                              "#3f4a3a", "#ffd9a8", .2, 5)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, 1, hh * .28, -8 + 26 * ud, t,
                              "#3f4a3a", "#ffd9a8", .5, 5)
    s += SL(Z_SRED, r1 + varezhka(e1x - 8, e1y + 8, 1.0, -14, "#6b4428", t, .2) + r2)
    s += SL(Z_SRED, f'<g transform="rotate({-26+30*ud:.1f} {e1x:.0f} {e1y:.0f})">'
                    f'<rect x="{e1x-120:.0f}" y="{e1y-10:.0f}" width="150" height="20"'
                    f' rx="8" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M{e1x-160:.0f},{e1y-56:.0f} q{-38:.0f},{56:.0f}'
                    f' {0:.0f},{112:.0f} l{44:.0f},{-14:.0f} l0,{-86:.0f} Z"'
                    f' fill="#c9ccd1" stroke="{K}" stroke-width="6"/></g>')
    s += SL(Z_SRED, para_izo_rta(hx - 34, hy - hh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    # ЧЕРТЕНЯТА выскакивают из щелей и улепётывают за забор
    for i in range(5):
        d = ((t * .55 + i / 5.0) % 1.0)
        cx_ = 900 + 760 * d
        cy_ = 940 - 120 * math.sin(d * 3.14)
        s += SL(Z_SRED, f'<g opacity="{.95*(1-d*.35):.2f}">'
                + chertenok(cx_, cy_, t, 1.15, i * .3, "#5e3a6a") + '</g>')
    s += SL(Z_SRED, zabor_shtaket(1560, 700, 420, 240, 431, 58))
    # поленница, сани, собака, ворона на крыше
    s += SL(Z_SRED, f'<rect x="700" y="940" width="240" height="130" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4.5"/>')
    for i in range(10):
        s += SL(Z_SRED, f'<circle cx="{722+(i%5)*48:.0f}" cy="{968+(i//5)*52:.0f}" r="22"'
                        f' fill="#8a6342" stroke="{K}" stroke-width="3"/>')
    s += SL(Z_SRED, sani_s_rogozhey(1700, 1040, .72, t, .3, False))
    lay = 8 * A.w(t, 1.2, .2)
    s += SL(Z_SRED, f'<ellipse cx="1480" cy="1010" rx="70" ry="34" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{1544+lay:.0f}" cy="976" r="28" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M{1566+lay:.0f},{962:.0f} l{14:.0f},{-26:.0f}'
                    f' l{10:.0f},{26:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3"/>'
                    f'<path d="M{1570+lay:.0f},{988:.0f} q{16:.0f},{10:.0f} {-2:.0f},{18:.0f}"'
                    f' fill="none" stroke="{K}" stroke-width="4"/>')
    vor = 6 * A.w(t, 2.0, .4)
    s += SL(Z_SRED, f'<ellipse cx="{520+vor:.0f}" cy="40" rx="46" ry="30"'
                    f' fill="#23242a" stroke="{K}" stroke-width="3.6"/>'
                    f'<circle cx="{554+vor:.0f}" cy="10" r="21" fill="#23242a"'
                    f' stroke="{K}" stroke-width="3.2"/>'
                    f'<path d="M{574+vor:.0f},8 l26,6 l-26,7 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="2.4"/>')
    s += SL(Z_SRED, dym_stolbom(320, 100, t, 240, .42, .4, 6))
    s += SL(Z_SRED, par(1480, 960, t, 3, .45, 140, .4, .9))
    s += SL(Z_SRED, inej_mel(431, 44, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def meteoploschadka(t):
    """Смена главы: метеоплощадка в поле — белая будка на ножках с жалюзи на
    пол-кадра, мачта с флюгером и вертушкой, дождемер, сетчатая ограда, без
    флагов и надписей. Наблюдатель открывает дверцу и пишет в журнал."""
    rnd = random.Random(3017)
    s = nebo("den", t, False, 433)
    s += oblaka(t, 130, 6, 211, .45)
    s += SL(Z_DAL, ulica_dal(60, 480, 700, t, True, 167))
    s += SL(Z_DAL, f'<rect x="1500" y="420" width="380" height="200" rx="8"'
                   f' fill="#d8cbb0" stroke="{K}" stroke-width="6"/>'
                   f'<path d="M1470,420 l210,-110 l230,110 Z" fill="#8a7a62"'
                   f' stroke="{K}" stroke-width="5.5"/>'
                   f'<rect x="1560" y="480" width="90" height="90" rx="5"'
                   f' fill="#8aa8b4" stroke="{K}" stroke-width="4"'
                   f' opacity="{.7+.25*A.w(t,4.0,.3):.2f}"/>')
    s += SL(Z_DAL, dym_stolbom(1700, 300, t, 260, .45, .4, 6))
    s += SL(Z_SRED, f'<rect x="0" y="620" width="{W}" height="460" fill="#dce7f2"/>')
    s += SL(Z_SRED, sneg_lezhit(650, 32, "url(#sneg)"))
    # СЕТЧАТАЯ ОГРАДА
    for i in range(16):
        s += SL(Z_SRED, f'<path d="M{40+i*126:.0f},700 v220" stroke="#9aa3a8"'
                        f' stroke-width="4" opacity=".75"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M0,{710+i*56:.0f} h{W}" stroke="#9aa3a8"'
                        f' stroke-width="4" opacity=".75"/>')
    for i in range(5):
        s += SL(Z_SRED, f'<rect x="{80+i*440:.0f}" y="680" width="20" height="260"'
                        f' fill="{BETON2}" stroke="{K}" stroke-width="3.6"/>')
    # БУДКА на ножках
    bx, by, bw, bh = 540, 420, 520, 360
    s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}"'
                    f' rx="8" fill="#f2ead6" stroke="{K}" stroke-width="7"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{bx+14:.0f},{by+30+i*36:.0f} h{bw-28:.0f}"'
                        f' stroke="#d8cbb0" stroke-width="12"/>')
    otkr = A.ease(A.seg(t, .8, 1.2))
    s += SL(Z_SRED, f'<g transform="rotate({-46*otkr:.1f} {bx+bw:.0f} {by:.0f})">'
                    f'<rect x="{bx+bw*.5:.0f}" y="{by:.0f}" width="{bw*.5:.0f}"'
                    f' height="{bh:.0f}" rx="6" fill="#f8f4e8" stroke="{K}"'
                    f' stroke-width="6"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<path d="M{bx+bw*.5+12:.0f},{by+30+i*36:.0f} h{bw*.5-24:.0f}"'
                        f' stroke="#dde3e8" stroke-width="10"/>')
    s += SL(Z_SRED, '</g>')
    s += SL(Z_SRED, f'<path d="M{bx-30:.0f},{by:.0f} l{bw*.5+30:.0f},{-70:.0f}'
                    f' l{bw*.5+30:.0f},{70:.0f} Z" fill="#c9ccd1" stroke="{K}"'
                    f' stroke-width="6"/>')
    for i in (-1, 1):
        s += SL(Z_SRED, f'<rect x="{bx+bw*.5+i*bw*.38-12:.0f}" y="{by+bh:.0f}"'
                        f' width="24" height="300" fill="#c9ccd1" stroke="{K}"'
                        f' stroke-width="4.5"/>')
    # МАЧТА с флюгером и вертушкой
    s += SL(Z_SRED, f'<rect x="1230" y="240" width="20" height="700" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    fl = 12 * A.w(t, 3.0, .2)
    s += SL(Z_SRED, f'<g transform="rotate({fl:.1f} 1240 260)">'
                    f'<path d="M1240,260 l{130:.0f},{30:.0f} l{-130:.0f},{30:.0f} Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1240,260 l{-80:.0f},{30:.0f} l{80:.0f},{30:.0f}"'
                    f' fill="none" stroke="{ZHELEZ}" stroke-width="7"/></g>')
    vert = (t * 400) % 360
    s += SL(Z_SRED, f'<g transform="rotate({vert:.0f} 1240 420)">')
    for i in range(4):
        a = i * 1.57
        s += SL(Z_SRED, f'<ellipse cx="{1240+60*math.cos(a):.0f}"'
                        f' cy="{420+60*math.sin(a):.0f}" rx="26" ry="18" fill="#dde3e8"'
                        f' stroke="{K}" stroke-width="3.4"'
                        f' transform="rotate({math.degrees(a):.0f}'
                        f' {1240+60*math.cos(a):.0f} {420+60*math.sin(a):.0f})"/>')
    s += SL(Z_SRED, '</g>')
    # ДОЖДЕМЕР и столбик со шкалой без цифр
    s += SL(Z_SRED, f'<path d="M1500,940 h120 l-14,-200 h-92 Z" fill="#c9ccd1"'
                    f' stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="1560" cy="740" rx="46" ry="14" fill="#dde3e8"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<rect x="1550" y="700" width="20" height="44" fill="{BETON2}"/>')
    s += SL(Z_SRED, f'<rect x="1780" y="620" width="30" height="330" fill="#f2ead6"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(12):
        s += SL(Z_SRED, f'<path d="M1784,{650+i*26:.0f} h{16 if i%3 else 24:.0f}"'
                        f' stroke="#5f5a4e" stroke-width="3"/>')
    # НАБЛЮДАТЕЛЬ
    nx, ny, nh = 1000, 1000, 680
    s += SL(Z_SRED, figura(nx, ny, nh, t, col="#3f4a56", kant="#ffd9a8",
                           tulup=True, shapka=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(nx, ny, nh, -1, nh * .32, -22, t, "#3f4a56", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(nx, ny, nh, 1, nh * .26, 10, t, "#3f4a56", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<rect x="{e2x-50:.0f}" y="{e2y:.0f}" width="110" height="80"'
                    f' rx="6" fill="#f2ead6" stroke="{K}" stroke-width="4"/>')
    for i in range(4):
        s += SL(Z_SRED, f'<path d="M{e2x-40:.0f},{e2y+18+i*16:.0f} q{28:.0f},{-5:.0f}'
                        f' {56:.0f},0" fill="none" stroke="#8a7a62" stroke-width="3"/>')
    pish = 5 * A.w(t, 1.4, .1)
    s += SL(Z_SRED, f'<path d="M{e2x+30+pish:.0f},{e2y+10:.0f} l{26:.0f},{-54:.0f}"'
                    f' stroke="#d6a63f" stroke-width="7"/>')
    s += SL(Z_SRED, para_izo_rta(nx - 34, ny - nh * .80, t, .3, 1.0, .5))
    s += SL(Z_SRED, ten(nx, ny + 6, 130, 22, .45))
    vor = 6 * A.w(t, 2.2, .4)
    s += SL(Z_SRED, f'<ellipse cx="{300+vor:.0f}" cy="700" rx="44" ry="28"'
                    f' fill="#23242a" stroke="{K}" stroke-width="3.6"/>'
                    f'<circle cx="{332+vor:.0f}" cy="672" r="20" fill="#23242a"'
                    f' stroke="{K}" stroke-width="3.2"/>'
                    f'<path d="M{352+vor:.0f},670 l26,6 l-26,7 Z" fill="#6f6256"'
                    f' stroke="{K}" stroke-width="2.4"/>')
    s += SL(Z_SRED, inej_mel(433, 46, 960, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 14, 107, .3, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def tulup_naraspashku_u_peril(t):
    """Крыльцо избы утром: хозяин в тулупе нараспашку поднял рукавицу вверх,
    держась за столб. Вокруг него по словам встают три значка — струя ветра,
    воробей на ветке, огонёк в печной заслонке."""
    rnd = random.Random(3018)
    s = nebo("rassv", t, False, 439)
    s += oblaka(t, 150, 5, 223, .38)
    s += SL(Z_DAL, ulica_dal(1180, 460, 740, t, True, 173))
    s += SL(Z_DAL, goloe_derevo_ld(1420, 560, 420, t, 439, 7, True))
    # ИЗБА и КРЫЛЬЦО
    s += SL(Z_SRED, f'<rect x="0" y="120" width="1060" height="700" fill="#6b4428"'
                    f' stroke="{K}" stroke-width="6"/>')
    s += SL(Z_SRED, brevna(0, 120, 1060, 700, 88, 2))
    s += SL(Z_SRED, f'<path d="M-20,120 l540,-120 l560,120 l0,50 l-560,-116 l-540,120 Z"'
                    f' fill="#4a3526" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M-20,110 l540,-122 l560,122" fill="none"'
                    f' stroke="url(#sneg)" stroke-width="20" opacity=".92"/>')
    s += SL(Z_SRED, dver(220, 340, 300, 480, .0, "url(#derev)", True, False))
    s += SL(Z_SRED, okno_izby(640, 340, 300, 260, t, None, .4, True, True))
    s += SL(Z_SRED, f'<rect x="60" y="820" width="900" height="34" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="80" y="854" width="860" height="26" rx="5"'
                    f' fill="{DOSKA2}" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="100" y="880" width="820" height="26" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<rect x="120" y="500" width="30" height="330" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="900" y="500" width="30" height="330" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M135,620 h780" stroke="#8a6342" stroke-width="13"/>')
    s += SL(Z_SRED, _merzlaya_zemlya(900, 439, False))
    s += SL(Z_SRED, sneg_lezhit(920, 28, "url(#sneg)"))
    # ХОЗЯИН в тулупе нараспашку
    hx, hy, hh = 560, 820, 700
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a4038", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    s += SL(Z_SRED, f'<path d="M{hx-120:.0f},{hy-hh*.64:.0f} q{30:.0f},{200:.0f}'
                    f' {10:.0f},{380:.0f} l{-70:.0f},{-10:.0f} q{10:.0f},{-200:.0f}'
                    f' {-10:.0f},{-380:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="5"/>'
                    f'<path d="M{hx+120:.0f},{hy-hh*.64:.0f} q{-30:.0f},{200:.0f}'
                    f' {-10:.0f},{380:.0f} l{70:.0f},{-10:.0f} q{-10:.0f},{-200:.0f}'
                    f' {10:.0f},{-380:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="5"/>')
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .34, -52, t, "#4a4038", "#ffd9a8", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .26, -34, t, "#4a4038", "#ffd9a8", .7, 4)
    s += SL(Z_SRED, r1 + varezhka(e1x + 6, e1y - 10, 1.1, 10, "#6b4428", t, .2) + r2)
    s += SL(Z_SRED, para_izo_rta(hx - 36, hy - hh * .80, t, .3, 1.1, .55))
    # ТРИ ЗНАЧКА по словам
    for i, (zx_, zy_) in enumerate(((1300, 300), (1520, 450), (1700, 640))):
        vst = A.out(A.seg(t, .6 + i * .5, .6))
        if vst < .02:
            continue
        s += SL(Z_SRED, f'<g opacity="{vst:.2f}" transform="translate(0,{50*(1-vst):.0f})">'
                        f'<circle cx="{zx_:.0f}" cy="{zy_:.0f}" r="90" fill="#f2ead6"'
                        f' stroke="{K}" stroke-width="5"/>')
        if i == 0:
            for k in range(3):
                s += SL(Z_SRED, f'<path d="M{zx_-60:.0f},{zy_-20+k*22:.0f}'
                                f' q{50:.0f},{-14:.0f} {100:.0f},{4:.0f}" fill="none"'
                                f' stroke="#6f7a84" stroke-width="7"/>')
        elif i == 1:
            s += SL(Z_SRED, ptica(zx_, zy_ + 10, t, 1.6, "#8a7a62", .2, "#6f6256"))
        else:
            s += SL(Z_SRED, f'<path d="M{zx_-54:.0f},{zy_+40:.0f} h108 l-10,-80 h-88 Z"'
                            f' fill="#3f2d1c" stroke="{K}" stroke-width="4"/>'
                    + ogon(zx_, zy_ + 30, t, .8, i * .2, 5))
        s += SL(Z_SRED, '</g>')
    # веник, вёдра, рябина, собака, дым
    s += SL(Z_SRED, dvorovye_veschi(180, 900, 320, t, 439, ["metla", "vedro"]))
    s += SL(Z_SRED, ryabina(1120, 980, t, 1.5, 6)
            + kalina_grozd(1160, 900, t, 1.0, 11, 443, .3))
    zev = A.ease(A.seg(t, 1.2, .8))
    s += SL(Z_SRED, f'<ellipse cx="1000" cy="1020" rx="72" ry="34" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="1064" cy="988" r="28" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3.6"/>'
                    f'<path d="M1086,{968:.0f} l{12:.0f},{-26:.0f} l{12:.0f},{26:.0f} Z"'
                    f' fill="#6b5230" stroke="{K}" stroke-width="3"/>'
                    f'<ellipse cx="1086" cy="{1000+6*zev:.0f}" rx="{10:.0f}"'
                    f' ry="{6+10*zev:.0f}" fill="#4a2a1e"/>')
    s += SL(Z_SRED, dym_stolbom(400, 60, t, 220, .45, .4, 6))
    s += SL(Z_SRED, ten(hx, hy + 6, 140, 24, .4))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def dym_stolbom_nad_derevney(t):
    """Деревня в тихий день: из каждой трубы дым стоит ровным столбом, бельё
    на верёвке висит не шелохнувшись, флюгер замер. Дед держит послюнявленную
    рукавицу над головой, а из-за леса выглядывает Мороз и потирает руки."""
    rnd = random.Random(3019)
    s = nebo("den", t, False, 443)
    s += oblaka(t, 110, 3, 227, .28)
    # ЛЕС на горизонте
    for i in range(22):
        ex_ = -40 + i * 92
        eh = rnd.uniform(140, 260)
        s += SL(Z_DAL, f'<path d="M{ex_:.0f},520 l{36:.0f},{-eh:.0f} l{36:.0f},{eh:.0f} Z"'
                       f' fill="#2f4a3a" stroke="{K}" stroke-width="4"/>')
    # ДОМА с дымами столбом
    for i, (ix, iw, sd) in enumerate(((120, 300, 109), (560, 340, 113),
                                      (1060, 320, 127), (1520, 360, 131))):
        s += SL(Z_SRED, izba_snaruzhi(ix, 640 + (i % 2) * 20, iw, t, True, True, sd))
        s += SL(Z_SRED, dym_stolbom(ix + iw * .12, 640 - iw * .62, t, 480, .55, .38, 8))
    s += SL(Z_SRED, _merzlaya_zemlya(700, 443, False))
    s += SL(Z_SRED, sneg_lezhit(740, 34, "url(#sneg)"))
    s += SL(Z_SRED, zabor_shtaket(-40, 740, 2000, 160, 443, 64))
    # БЕЛЬЁ не шелохнётся
    s += SL(Z_SRED, f'<path d="M400,660 h420" stroke="#b9a37a" stroke-width="5"/>')
    for i, (px_, pw_, col) in enumerate(((430, 90, "#e8e2d6"), (560, 76, "#8aa8b4"),
                                         (680, 84, "#d6a63f"))):
        s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="660" width="{pw_:.0f}" height="150"'
                        f' rx="6" fill="{col}" stroke="{K}" stroke-width="4"/>')
    # ФЛЮГЕР замер
    s += SL(Z_SRED, f'<rect x="1360" y="400" width="14" height="300" fill="{ZHELEZ}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<path d="M1367,400 l{90:.0f},{26:.0f} l{-90:.0f},{26:.0f} Z"'
                    f' fill="#8a2f22" stroke="{K}" stroke-width="4"/>')
    # ДЕД с рукавицей над головой
    dx, dy, dh = 880, 1040, 700
    s += SL(Z_SRED, figura(dx, dy, dh, t, col="#4a4038", kant="#ffd9a8",
                           tulup=True, shapka=True, boroda=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(dx, dy, dh, 1, dh * .34, -56, t, "#4a4038", "#ffd9a8", .2, 3)
    r2, (e2x, e2y), _ = _ruka(dx, dy, dh, -1, dh * .28, 44, t, "#4a4038", "#ffd9a8", .7, 3)
    s += SL(Z_SRED, r1 + varezhka(e1x + 4, e1y - 14, 1.2, 6, "#6b4428", t, .1) + r2)
    s += SL(Z_SRED, f'<path d="M{e2x:.0f},{e2y:.0f} l{20:.0f},{dy-e2y-10:.0f}"'
                    f' stroke="#7d5636" stroke-width="12" stroke-linecap="round"/>')
    s += SL(Z_SRED, para_izo_rta(dx - 36, dy - dh * .80, t, .3, 1.1, .55))
    s += SL(Z_SRED, ten(dx, dy + 6, 134, 23, .45))
    # МОРОЗ выглядывает из-за леса и потирает руки
    vygl = A.ease(A.seg(t, .8, 1.6))
    s += SL(Z_SRED, f'<g transform="translate(0,{200-140*vygl:.0f})">'
            + moroz_ded(1760, 640, t, .9, .2) + '</g>')
    # колодец, сани, воробьи
    s += SL(Z_SRED, f'<rect x="300" y="880" width="220" height="110" rx="8"'
                    f' fill="{KAMEN}" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="410" cy="880" rx="110" ry="24" fill="{KAMEN2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M330,880 l-8,-140 h176 l-8,140" fill="none"'
                    f' stroke="#6b4428" stroke-width="12"/>'
                    f'<path d="M322,740 h190" stroke="#54351f" stroke-width="13"/>')
    s += SL(Z_SRED, sani_s_rogozhey(620, 1040, .8, t, .4, True))
    for i, (vx_, vy_) in enumerate(((1200, 900), (1280, 930), (1360, 890))):
        s += SL(Z_SRED, ptica(vx_, vy_, t, 1.4, "#8a7a62", i * .4, "#6f6256"))
    s += SL(Z_SRED, inej_mel(443, 48, 960, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def alaya_zarya_za_oknom(t):
    """Окно избы на пол-кадра: за стеклом настоящая алая заря. Хозяйка
    отодвигает занавеску, снимает с гвоздя зонт и ставит рядом валенки с
    галошами; на подоконнике горшок с луком и чашка."""
    rnd = random.Random(3020)
    s = stena_gornicy_19(t, 53, 860, True, True)
    # ОКНО-ПРОЁМ по центру
    px, py, pw, ph_ = 520, 200, 780, 320
    okno = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
            f' fill="#c8604a"/>')
    okno += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.45:.0f}"'
             f' fill="#e08a5a"/>')
    okno += mesto_stoka(px, py, pw, ph_, "pryam")
    okno += (f'<rect x="{px-18:.0f}" y="{py-18:.0f}" width="{pw+36:.0f}"'
             f' height="{ph_+36:.0f}" rx="6" fill="none" stroke="#6b4428"'
             f' stroke-width="26"/>')
    okno += (f'<path d="M{px+pw*.5:.0f},{py:.0f} v{ph_:.0f} M{px:.0f},{py+ph_*.5:.0f}'
             f' h{pw:.0f}" stroke="#6b4428" stroke-width="16"/>')
    okno += (f'<rect x="{px-50:.0f}" y="{py+ph_+18:.0f}" width="{pw+100:.0f}"'
             f' height="32" rx="6" fill="{DOSKA}" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, okno)
    s += SL(Z_SRED, teplo(px + pw * .5, py + ph_ * .5, 520, 420, .35))
    # ЗАНАВЕСКА отодвигается
    otod = A.ease(A.seg(t, .5, 1.2))
    for i in (0, 1):
        sdv = (-1 if i == 0 else 1) * 120 * otod
        s += SL(Z_SRED, f'<path d="M{px+i*(pw-180)+sdv:.0f},{py-20:.0f}'
                        f' q{80:.0f},{40:.0f} {70:.0f},{ph_*.9:.0f} q{-50:.0f},{26:.0f}'
                        f' {-120:.0f},{10:.0f} Z" fill="{RUSH}" opacity=".95"'
                        f' stroke="{K}" stroke-width="4.5"/>')
    # ГОРШОК С ЛУКОМ и чашка на подоконнике
    s += SL(Z_SRED, f'<path d="M560,{py+ph_+18:.0f} h120 l-14,-80 h-92 Z"'
                    f' fill="#a8743c" stroke="{K}" stroke-width="4.5"/>')
    for i in range(5):
        a = -1.1 + i * .55
        s += SL(Z_SRED, f'<path d="M620,{py+ph_-62:.0f} q{40*math.sin(a):.0f},{-60:.0f}'
                        f' {64*math.sin(a):.0f},{-130:.0f} q{16:.0f},{34:.0f}'
                        f' {-30*math.sin(a):.0f},{130:.0f} Z" fill="#6f8c4a"'
                        f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, kruzhka_moloka(1240, py + ph_ + 18, .8, t, False, .3, "#d8cbb0"))
    # ХОЗЯЙКА снимает зонт с гвоздя
    hx, hy, hh = 1560, 1050, 700
    snyat = A.ease(A.seg(t, 1.2, 1.4))
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#4a3a52", kant="#ffd98a",
                           platok=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .34, -40 + 16 * snyat, t,
                              "#4a3a52", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .30, -24, t, "#4a3a52", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    zx_, zy_ = e1x + 10, e1y + 40 * snyat
    s += SL(Z_SRED, f'<path d="M{zx_-14:.0f},{zy_:.0f} l{12:.0f},{220:.0f}"'
                    f' stroke="#3f3a33" stroke-width="10"/>'
                    f'<path d="M{zx_-90:.0f},{zy_:.0f} q{90:.0f},{-80:.0f} {180:.0f},0 Z"'
                    f' fill="#3f5a6a" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M{zx_:.0f},{zy_+220:.0f} q{26:.0f},{16:.0f} {30:.0f},{-14:.0f}"'
                    f' fill="none" stroke="#3f3a33" stroke-width="8"/>')
    s += SL(Z_SRED, f'<rect x="{zx_-30:.0f}" y="{zy_-60:.0f}" width="16" height="30"'
                    f' rx="4" fill="{ZHELEZ}" stroke="{K}" stroke-width="3"/>')
    # ВАЛЕНКИ с галошами у двери
    s += SL(Z_SRED, _valenok(1180, 1050, 1.2, -4) + _valenok(1290, 1056, 1.2, 5)
            + f'<ellipse cx="1180" cy="1056" rx="40" ry="14" fill="#23242a"'
              f' stroke="{K}" stroke-width="3.4"/>'
              f'<ellipse cx="1290" cy="1062" rx="40" ry="14" fill="#23242a"'
              f' stroke="{K}" stroke-width="3.4"/>')
    # лавка, ходики, кот, печь
    s += SL(Z_SRED, lavka(220, 940, 420))
    s += SL(Z_SRED, hodiki(220, 300, t, 1.4))
    s += SL(Z_SRED, kot(420, 940, t, 1.5, "#3b3430", True))
    s += SL(Z_SRED, pech(1680, 320, 260, 420, t, True, True, False))
    s += SL(Z_SRED, ogon(1760, 640, t, .9, .3, 5) + teplo(1760, 620, 260, 210, .42))
    s += SL(Z_SRED, polka_s_bankami(140, 500, 400, t, 113, 4, False))
    s += SL(Z_SRED, ten(hx, hy + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def nahohlennye_pticy_na_vetke(t):
    """Ветка рябины за окном, а чердачное окошко дома рядом — круглый проём с
    настоящими нахохленными воробьями. На рисованной ветке сидят пять
    воробьёв-шариков; мальчик прижался к стеклу, бабушка несёт вторую шаль."""
    rnd = random.Random(3021)
    s = stena_gornicy_19(t, 59, 880, True, True)
    # ОКНО комнаты
    s += SL(Z_SRED, f'<rect x="200" y="160" width="900" height="620" rx="8"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="7"/>'
                    f'<rect x="230" y="190" width="840" height="560" fill="#9fc4d8"'
                    f' opacity=".55"/>'
                    f'<path d="M650,160 v620 M200,470 h900" stroke="#e4d8bd"'
                    f' stroke-width="18"/>'
                    f'<rect x="170" y="780" width="960" height="34" rx="6"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="5"/>')
    # ВЕТКА РЯБИНЫ с пятью воробьями-шариками
    s += SL(Z_SRED, f'<path d="M230,330 q{220:.0f},{60:.0f} {460:.0f},{20:.0f}'
                    f' q{200:.0f},{-20:.0f} {380:.0f},{40:.0f}" fill="none"'
                    f' stroke="#5e4430" stroke-width="16"/>')
    for i in range(5):
        vx_ = 300 + i * 160
        vy_ = 330 + (20 if i % 2 else -10)
        puh = 1.0 + .05 * A.w(t, 2.4, i * .3)
        s += SL(Z_SRED, f'<ellipse cx="{vx_:.0f}" cy="{vy_-34:.0f}" rx="{44*puh:.0f}"'
                        f' ry="{40*puh:.0f}" fill="#8a7a62" stroke="{K}"'
                        f' stroke-width="4"/>'
                        f'<circle cx="{vx_+26:.0f}" cy="{vy_-54:.0f}" r="{20*puh:.0f}"'
                        f' fill="#9a8a6a" stroke="{K}" stroke-width="3.4"/>'
                        f'<path d="M{vx_+44:.0f},{vy_-56:.0f} l20,5 l-20,6 Z"'
                        f' fill="#5f5a4e"/>'
                        f'<circle cx="{vx_+32:.0f}" cy="{vy_-60:.0f}" r="4" fill="{K}"/>'
                        f'<path d="M{vx_-40:.0f},{vy_-20:.0f} l{-26:.0f},{16:.0f}'
                        f' l{26:.0f},{6:.0f} Z" fill="#6f6256" stroke="{K}"'
                        f' stroke-width="2.6"/>')
    for i in range(4):
        s += SL(Z_SRED, kalina_grozd(360 + i * 190, 380, t, .9, 10, 59 + i, i * .25, True))
    # ЧЕРДАЧНОЕ ОКОШКО — круглый проём
    ox, oy, od = 1360, 200, 400
    put = kontur_proema(ox, oy, od, od, "ellips")
    cher = (f'<path d="{put}" fill="#8aa8b4"/>')
    cher += (f'<path d="{put}" fill="#cfe4f5" opacity=".35"/>')
    cher += mesto_stoka(ox, oy, od, od, "ellips")
    cher += (f'<circle cx="{ox+od*.5:.0f}" cy="{oy+od*.5:.0f}" r="{od*.5:.0f}"'
             f' fill="none" stroke="#6b4428" stroke-width="24"/>')
    for i in range(4):
        a = i * 1.57 + .78
        cher += (f'<path d="M{ox+od*.5:.0f},{oy+od*.5:.0f}'
                 f' l{od*.5*math.cos(a):.0f},{od*.5*math.sin(a):.0f}" stroke="#6b4428"'
                 f' stroke-width="10"/>')
    s += SL(Z_SRED, cher)
    s += SL(Z_SRED, f'<rect x="{ox-60:.0f}" y="{oy+od+20:.0f}" width="{od+120:.0f}"'
                    f' height="28" rx="6" fill="{DOSKA2}" stroke="{K}" stroke-width="5"/>')
    # МАЛЬЧИК на табурете у окна
    mx, my, mh = 760, 980, 480
    s += SL(Z_SRED, f'<rect x="{mx-80:.0f}" y="{my:.0f}" width="160" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="{mx-60:.0f}" y="{my+26:.0f}" width="18" height="80"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>'
                    f'<rect x="{mx+42:.0f}" y="{my+26:.0f}" width="18" height="80"'
                    f' fill="#7d5636" stroke="{K}" stroke-width="3.2"/>')
    s += SL(Z_SRED, figura(mx, my, mh, t, col="#3f5a6a", kant="#ffd98a", ph=.3))
    r1, (e1x, e1y), _ = _ruka(mx, my, mh, 1, mh * .30, -40, t, "#3f5a6a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(mx, my, mh, -1, mh * .30, -36, t, "#3f5a6a", "#ffd98a", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    # БАБУШКА со второй шалью
    bx, by, bh = 1680, 1056, 660
    idt = A.ease(A.seg(t, 1.0, 1.6))
    s += SL(Z_SRED, f'<g opacity=".95">'
            + figura(bx - 140 * idt, by, bh, t, col="#4a3a52", kant="#ffd98a",
                     platok=True, ph=.7) + '</g>')
    r3, (e3x, e3y), _ = _ruka(bx - 140 * idt, by, bh, -1, bh * .28, -14, t,
                              "#4a3a52", "#ffd98a", .4, 4)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x-70:.0f},{e3y:.0f} q{70:.0f},{-30:.0f}'
                         f' {140:.0f},0 l{10:.0f},{120:.0f} q{-80:.0f},{26:.0f}'
                         f' {-160:.0f},0 Z" fill="#8a2f8a" stroke="{K}"'
                         f' stroke-width="4.5"/>')
    # кактус, кот на подоконнике, занавеска
    s += SL(Z_SRED, f'<path d="M300,812 h110 l-12,-70 h-86 Z" fill="#a8743c"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M332,742 q{24:.0f},{-90:.0f} {46:.0f},{-4:.0f}'
                    f' q{-6:.0f},{80:.0f} {-46:.0f},{4:.0f} Z" fill="#4a6a3a"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(1700, 420, t, 1.3, True) + teplo(1700, 440, 280, 230, .42))
    s += SL(Z_SRED, kot(1060, 812, t, 1.5, "#3b3430", False))
    kch = 5 * A.w(t, 2.6, .3)
    s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} 1180 160)">'
                    f'<path d="M1120,160 q{70:.0f},{40:.0f} {140:.0f},0 l0,{380:.0f}'
                    f' q{-70:.0f},{34:.0f} {-140:.0f},0 Z" fill="{RUSH}" opacity=".9"'
                    f' stroke="{K}" stroke-width="4.5"/></g>')
    s += SL(Z_SRED, ten(bx - 140 * idt, by + 6, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def drova_progoreli_do_zoly(t):
    """Устье печи: охапка поленьев вспыхивает и на глазах оседает в кучку
    серой золы, а рисованные песочные часы над устьем пересыпаются слишком
    быстро. Дед с кочергой чешет затылок и идёт за второй охапкой."""
    rnd = random.Random(3022)
    s = (f'<rect width="{W}" height="{H}" fill="#241c16"/>')
    s += SL(Z_DAL, brevna(0, 0, W, 900, 86, 3))
    s += SL(Z_SRED, polovicy(900, "#6b4428"))
    # ПЕЧЬ с устьем на пол-кадра
    s += SL(Z_SRED, pech(240, 120, 1000, 780, t, True, True, False))
    ux, uy, uw, uh = 520, 480, 460, 330
    put = kontur_proema(ux, uy, uw, uh, "ustie")
    s += SL(Z_SRED, f'<path d="{put}" fill="#1a0d06" stroke="{K}" stroke-width="7"/>')
    # ПОЛЕНЬЯ оседают в золу
    osad = A.ease(A.seg(t, .4, 2.2))
    for i in range(6):
        px_ = ux + 80 + i * 56
        py_ = uy + 250 - 30 * (1 - osad) * ((i % 3) + 1)
        s += SL(Z_SRED, f'<rect x="{px_:.0f}" y="{py_:.0f}" width="{44*(1-osad*.6):.0f}"'
                        f' height="{90*(1-osad*.75):.0f}" rx="10" fill="#7d5636"'
                        f' opacity="{1-osad*.7:.2f}" stroke="{K}" stroke-width="3.6"/>')
    s += SL(Z_SRED, ogon(ux + uw * .5, uy + 230, t, 1.5 * (1 - osad * .55), .1, 7))
    s += SL(Z_SRED, ugli(ux + 70, uy + 280, uw - 140, t, 8, 2))
    s += SL(Z_SRED, f'<ellipse cx="{ux+uw*.5:.0f}" cy="{uy+292:.0f}"'
                    f' rx="{160*osad:.0f}" ry="{30*osad:.0f}" fill="#9aa3a8"'
                    f' opacity="{.85*osad:.2f}"/>')
    s += SL(Z_SRED, teplo(ux + uw * .5, uy + 220, 520, 420, .55))
    s += SL(Z_SRED, iskra_let(t, ux + uw * .5, uy + 200, 8, 4, 300, .5))
    # ПЕСОЧНЫЕ ЧАСЫ над устьем
    pes = ((t * .9) % 1.0)
    s += SL(Z_SRED, f'<path d="M{ux+uw*.5-70:.0f},{uy-230:.0f} h140 l-60,{100:.0f}'
                    f' l60,{100:.0f} h-140 l60,{-100:.0f} Z" fill="#dce7f2"'
                    f' opacity=".5" stroke="{K}" stroke-width="5"/>'
                    f'<path d="M{ux+uw*.5-54:.0f},{uy-222:.0f} h108 l-54,{90:.0f} Z"'
                    f' fill="#d6a63f" opacity="{1-pes:.2f}"/>'
                    f'<path d="M{ux+uw*.5-54:.0f},{uy-32:.0f} h108 l-54,{-90:.0f} Z"'
                    f' fill="#d6a63f" opacity="{pes:.2f}"/>'
                    f'<path d="M{ux+uw*.5:.0f},{uy-132:.0f} l0,{60:.0f}"'
                    f' stroke="#d6a63f" stroke-width="5"/>')
    # ДЕД на скамеечке с кочергой
    dx, dy, dh = 1420, 1050, 560
    vst = A.ease(A.seg(t, 1.8, 1.0))
    s += SL(Z_SRED, f'<rect x="{dx-90:.0f}" y="{dy-20:.0f}" width="180" height="26"'
                    f' rx="5" fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, figura(dx, dy - 10 - 40 * vst, dh, t, col="#4a4038", kant="#ffd98a",
                           boroda=True, shapka=True, ph=.3))
    r1, (e1x, e1y), _ = _ruka(dx, dy - 10 - 40 * vst, dh, -1, dh * .34, -4, t,
                              "#4a4038", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(dx, dy - 10 - 40 * vst, dh, 1, dh * .30, -44, t,
                              "#4a4038", "#ffd98a", .7, 5)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{-240:.0f},{80:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="9"/>'
                    f'<path d="M{e1x-240:.0f},{e1y+80:.0f} l{-40:.0f},{-26:.0f}"'
                    f' stroke="{ZHELEZ}" stroke-width="9"/>')
    # заслонка, ухват, чугунок, кот, вязанка дров
    s += SL(Z_SRED, f'<rect x="1020" y="520" width="160" height="240" rx="8"'
                    f' fill="{CHUGUN}" stroke="{K}" stroke-width="5"/>'
                    f'<circle cx="1100" cy="640" r="20" fill="#5d6168" stroke="{K}"'
                    f' stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M180,1060 l{26:.0f},{-420:.0f}" stroke="#8a6342"'
                    f' stroke-width="12"/>'
                    f'<path d="M194,650 q{-36:.0f},{-46:.0f} {8:.0f},{-74:.0f}'
                    f' M232,644 q{36:.0f},{-46:.0f} {-6:.0f},{-76:.0f}" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="10"/>')
    s += SL(Z_SRED, f'<path d="M340,1040 q{-18:.0f},{-66:.0f} {52:.0f},{-70:.0f}'
                    f' q{70:.0f},{4:.0f} {52:.0f},{70:.0f} Z" fill="{CHUGUN}"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, kot(1700 + 60 * vst, 1050, t, 1.5, "#3b3430", False))
    s += SL(Z_SRED, f'<g transform="rotate(-10 1840 940)">')
    for i in range(7):
        s += SL(Z_SRED, f'<rect x="{1790+i*9:.0f}" y="{780:.0f}" width="26" height="170"'
                        f' rx="8" fill="#7d5636" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<path d="M1788,860 h110" stroke="#b9a37a" stroke-width="9"/></g>')
    s += SL(Z_SRED, ten(dx, dy + 20, 130, 22, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.46)
    return s


def pticy_na_dereve_u_doma(t):
    """Городской двор утром: берёза у подъезда и забор детской площадки. На
    ветках сидят рисованные синицы — одни распушились шариками, другие
    прыгают. На перилах балкона встают две карточки-подсказки."""
    rnd = random.Random(3023)
    s = nebo("rassv", t, False, 449)
    s += oblaka(t, 150, 5, 229, .36, "#ffe9c8")
    s += SL(Z_DAL, panelka(1180, 760, 740, t, 5, True, 71))
    # БЕРЁЗА у подъезда
    bx, bb = 700, 1000
    s += SL(Z_SRED, f'<path d="M{bx-26:.0f},{bb:.0f} q{6:.0f},{-400:.0f} {16:.0f},{-820:.0f}'
                    f' l{32:.0f},0 q{12:.0f},{420:.0f} {18:.0f},{820:.0f} Z"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>')
    for i in range(16):
        yy = bb - 60 - i * 50
        s += SL(Z_SRED, f'<path d="M{bx-22+((i*7)%10):.0f},{yy:.0f} h{16+((i*5)%14):.0f}"'
                        f' stroke="#3f3a33" stroke-width="{4+((i*3)%3):.0f}"'
                        f' opacity=".85"/>')
    for i in range(8):
        p = .32 + .66 * i / 7.0
        sgn = 1 if i % 2 else -1
        y0 = bb - 820 * p
        dl = 320 * (1.1 - p)
        s += SL(Z_SRED, f'<path d="M{bx:.0f},{y0:.0f} q{sgn*dl*.5:.0f},{-dl*.2:.0f}'
                        f' {sgn*dl:.0f},{-dl*.1:.0f}" fill="none" stroke="#c9bfa6"'
                        f' stroke-width="{max(3, 11-i):.0f}"/>')
    # СИНИЦЫ: часть шариками, часть прыгают
    for i in range(7):
        sgn = 1 if i % 2 else -1
        vx_ = bx + sgn * (120 + (i % 4) * 90)
        vy_ = bb - 300 - i * 70
        if i % 3 == 0:
            puh = 1.0 + .06 * A.w(t, 2.2, i * .3)
            s += SL(Z_SRED, f'<ellipse cx="{vx_:.0f}" cy="{vy_:.0f}" rx="{36*puh:.0f}"'
                            f' ry="{34*puh:.0f}" fill="#d6a63f" stroke="{K}"'
                            f' stroke-width="4"/>'
                            f'<circle cx="{vx_+20:.0f}" cy="{vy_-20:.0f}" r="16"'
                            f' fill="#4a5664" stroke="{K}" stroke-width="3.2"/>'
                            f'<path d="M{vx_+34:.0f},{vy_-22:.0f} l16,4 l-16,5 Z"'
                            f' fill="#5f5a4e"/>')
        else:
            pr = 16 * abs(A.w(t, 1.2, i * .25))
            s += SL(Z_SRED, f'<g transform="translate(0,{-pr:.0f})">'
                    + ptica(vx_, vy_, t, 1.5, "#d6a63f", i * .2, "#4a6a78") + '</g>')
    # БАЛКОН с женщиной и карточками-подсказками
    s += SL(Z_SRED, f'<rect x="1240" y="520" width="520" height="34" rx="6"'
                    f' fill="{BETON2}" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1240" y="554" width="520" height="190" rx="6"'
                    f' fill="#b9b2a6" stroke="{K}" stroke-width="5"/>')
    for i in range(9):
        s += SL(Z_SRED, f'<rect x="{1260+i*56:.0f}" y="560" width="12" height="180"'
                        f' fill="#9aa3a8"/>')
    zx, zy, zh = 1480, 520, 520
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#8a2f8a", kant="#ffd98a", ph=.3))
    r1, (e1x, e1y), _ = _ruka(zx, zy, zh, 1, zh * .26, 40, t, "#8a2f8a", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(zx, zy, zh, -1, zh * .24, 44, t, "#8a2f8a", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2 + kruzhka_moloka(e1x + 10, e1y + 50, .8, t, False, .2))
    s += SL(Z_SRED, par(e1x + 10, e1y + 10, t, 3, .45, 130, .4, .8))
    for i, (kx_, ky_) in enumerate(((1300, 420), (1620, 430))):
        vst = A.out(A.seg(t, .8 + i * .6, .6))
        if vst < .02:
            continue
        s += SL(Z_SRED, f'<g opacity="{vst:.2f}">'
                        f'<rect x="{kx_-80:.0f}" y="{ky_-70:.0f}" width="160"'
                        f' height="140" rx="12" fill="#f2ead6" stroke="{K}"'
                        f' stroke-width="5"/>')
        if i == 0:
            s += SL(Z_SRED, f'<circle cx="{kx_:.0f}" cy="{ky_+6:.0f}" r="40"'
                            f' fill="#d6a63f" stroke="{K}" stroke-width="3.6"/>'
                            f'<path d="M{kx_-40:.0f},{ky_-40:.0f} h{80:.0f}'
                            f' M{kx_:.0f},{ky_-60:.0f} v{40:.0f}" stroke="#4a6a78"'
                            f' stroke-width="5"/>')
        else:
            s += SL(Z_SRED, ptica(kx_, ky_ + 20, t, 1.3, "#d6a63f", .3, "#4a6a78")
                    + f'<circle cx="{kx_+46:.0f}" cy="{ky_-40:.0f}" r="20"'
                      f' fill="#ffe9ac" opacity=".9"/>')
        s += SL(Z_SRED, '</g>')
    # бельевая верёвка, лыжи, ящик для цветов, кот
    s += SL(Z_SRED, f'<path d="M1260,600 h480" stroke="#b9a37a" stroke-width="4"/>')
    for i, (px_, pw_, col) in enumerate(((1300, 70, "#e8e2d6"), (1420, 60, "#8aa8b4"))):
        kch = 5 * A.w(t, 2.4, i * .5)
        s += SL(Z_SRED, f'<g transform="rotate({kch:.1f} {px_+pw_*.5:.0f} 612)">'
                        f'<rect x="{px_:.0f}" y="612" width="{pw_:.0f}" height="110"'
                        f' rx="5" fill="{col}" stroke="{K}" stroke-width="3.4"/></g>')
    s += SL(Z_SRED, f'<path d="M1700,560 l{10:.0f},{-180:.0f} M1740,560 l{10:.0f},{-180:.0f}"'
                    f' stroke="#8a2f22" stroke-width="12"/>')
    s += SL(Z_SRED, f'<rect x="1260" y="690" width="160" height="56" rx="6"'
                    f' fill="#6b4428" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, kot(1660, 744, t, 1.3, "#3b3430", False))
    # двор: забор площадки, скамейка, сугробы
    s += SL(Z_SRED, _merzlaya_zemlya(940, 449, False))
    s += SL(Z_SRED, sneg_lezhit(960, 28, "url(#sneg)"))
    s += SL(Z_SRED, zabor_shtaket(-40, 860, 620, 180, 449, 58))
    s += SL(Z_SRED, f'<rect x="120" y="980" width="280" height="20" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="140" y="1000" width="20" height="70" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="360" y="1000" width="20" height="70" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    # ДВОР ОБЖИТ: второй дом, качели, песочница, фонарь, кусты, сугробы
    s += SL(Z_DAL, panelka(40, 720, 560, t, 5, True, 73))
    s += SL(Z_SRED, f'<rect x="300" y="620" width="22" height="420" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(311, 620, t, 1.1, True) + teplo(311, 640, 220, 180, .34))
    s += SL(Z_SRED, f'<rect x="900" y="700" width="20" height="300" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1120" y="700" width="20" height="300" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="880" y="690" width="280" height="20" rx="5"'
                    f' fill="{ZHELEZ}" stroke="{K}" stroke-width="4"/>')
    kach = 7 * A.w(t, 2.6, .2)
    s += SL(Z_SRED, f'<g transform="rotate({kach:.1f} 1020 700)">'
                    f'<path d="M960,710 l{10:.0f},{170:.0f} M1080,710 l{-10:.0f},{170:.0f}"'
                    f' stroke="#b9a37a" stroke-width="5"/>'
                    f'<rect x="950" y="878" width="140" height="22" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/></g>')
    s += SL(Z_SRED, f'<rect x="420" y="880" width="300" height="120" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="440" y="860" width="260" height="26" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<ellipse cx="570" cy="912" rx="120" ry="30" fill="url(#sneg)"'
                    f' opacity=".9"/>')
    for i, (kx2, kb2, kh2) in enumerate(((240, 1000, 220), (1180, 1010, 200),
                                         (1400, 990, 240))):
        s += SL(Z_SRED, goloe_derevo_ld(kx2, kb2, kh2, t, 457 + i, 5, True))
    for i in range(7):
        s += SL(Z_SRED, f'<ellipse cx="{160+i*260:.0f}" cy="{1020+((i*5)%3)*16:.0f}"'
                        f' rx="{90+((i*7)%4)*26:.0f}" ry="{26+((i*3)%2)*10:.0f}"'
                        f' fill="url(#sneg)" opacity=".92"/>')
    s += SL(Z_SRED, inej_mel(449, 44, 980, 1070))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.40)
    return s


def shkolnaya_parta_s_uchebnikom(t):
    """Школьная парта с раскрытым учебником: на правой странице в овальном
    медальоне — настоящий портрет Ломоносова, гравюра XVIII века. Рядом
    чернильница, ручка, мел; за партой сидит ученик."""
    rnd = random.Random(3024)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="560" fill="#d8cbb0"/>'
                   f'<rect x="0" y="560" width="{W}" height="56" fill="#8a7a52"'
                   f' opacity=".85"/>')
    s += SL(Z_DAL, klassnaya_doska(120, 90, 700, 380, t, 11))
    s += SL(Z_DAL, okno_izby(1500, 110, 380, 380, t, None, .3, False, True))
    s += SL(Z_DAL, f'<rect x="1020" y="200" width="200" height="260" rx="8"'
                   f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                   f'<circle cx="1120" cy="300" r="76" fill="#3f6b7a" stroke="{K}"'
                   f' stroke-width="5"/>'
                   f'<path d="M1046,286 q{74:.0f},{44:.0f} {148:.0f},0" fill="none"'
                   f' stroke="#56763f" stroke-width="8"/>')
    s += SL(Z_SRED, polovicy(700, "#8a6342"))
    # ПАРТА и УЧЕБНИК
    s += SL(Z_SRED, parta_shkolnaya(260, 1010, 1300, t, 13, True))
    ux, uy, uw, uh = 420, 620, 1000, 420
    s += SL(Z_SRED, uchebnik_razvorot(ux, uy, uw, uh, t, True, .2))
    # ОВАЛЬНЫЙ МЕДАЛЬОН на правой странице — проём с портретом
    ox, oy, ow, oh2 = ux + uw * .54, uy + 36, 420, 330
    put = kontur_proema(ox, oy, ow, oh2, "ellips")
    med = (f'<path d="{put}" fill="#e4d8bd"/>')
    med += (f'<path d="{put}" fill="#d8cbb0" opacity=".5"/>')
    med += mesto_stoka(ox, oy, ow, oh2, "ellips")
    med += (f'<ellipse cx="{ox+ow*.5:.0f}" cy="{oy+oh2*.5:.0f}" rx="{ow*.5:.0f}"'
            f' ry="{oh2*.5:.0f}" fill="none" stroke="#8a6342" stroke-width="18"/>')
    med += (f'<ellipse cx="{ox+ow*.5:.0f}" cy="{oy+oh2*.5:.0f}" rx="{ow*.5+14:.0f}"'
            f' ry="{oh2*.5+14:.0f}" fill="none" stroke="#c9a05a" stroke-width="6"'
            f' opacity=".9"/>')
    s += SL(Z_SRED, med)
    for i in range(5):
        s += SL(Z_SRED, f'<path d="M{ox-10:.0f},{oy+oh2+30+i*26:.0f} q{90:.0f},{-6:.0f}'
                        f' {180:.0f},0 q{70:.0f},{6:.0f} {120:.0f},{-2:.0f}" fill="none"'
                        f' stroke="#6f6354" stroke-width="3.4" opacity=".75"/>')
    # УЧЕНИК за партой
    px_, py_, ph_ = 1600, 1066, 560
    s += SL(Z_SRED, figura(px_, py_, ph_, t, col="#3f3a4a", kant="#ffd98a", ph=.3))
    r1, (e1x, e1y), _ = _ruka(px_, py_, ph_, -1, ph_ * .30, 10, t, "#3f3a4a", "#ffd98a", .2, 4)
    s += SL(Z_SRED, r1)
    # мел, чернильница, ручка уже в parta_shkolnaya; добавим стопку тетрадей
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1380+i*6:.0f}" y="{620-i*16:.0f}" width="150"'
                        f' height="18" rx="4" fill="#f2ead6" stroke="{K}"'
                        f' stroke-width="3.2"/>')
    s += SL(Z_SRED, lampa(960, 60, t, 1.3, True) + teplo(960, 80, 300, 250, .40))
    s += SL(Z_SRED, ten(px_, py_ + 6, 120, 20, .4))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def pomorskaya_derevnya_u_morya(t):
    """Северный берег: серое море, дома на высоких подклетах, карбас на
    берегу, сети на шестах. Распахнутые ворота лодочного сарая — проём с
    настоящим северным морем. Помор поднимает свёрток с младенцем к небу."""
    rnd = random.Random(3025)
    s = nebo("sumer", t, False, 457)
    s += oblaka(t, 140, 6, 233, .44)
    s += SL(Z_DAL, f'<rect x="0" y="420" width="{W}" height="240" fill="#4a5664"/>')
    for i in range(12):
        yy = 440 + i * 18
        s += SL(Z_DAL, f'<path d="M{rnd.uniform(-60,200):.0f},{yy:.0f}'
                       f' q{rnd.uniform(300,700):.0f},{rnd.uniform(-8,8):.0f}'
                       f' {rnd.uniform(1200,1960):.0f},{rnd.uniform(-6,6):.0f}"'
                       f' fill="none" stroke="#5e6a78" stroke-width="{rnd.uniform(2,5):.1f}"'
                       f' opacity=".6"/>')
    # ДОМА на высоких подклетах
    for i, (ix, iw) in enumerate(((60, 320), (1480, 360))):
        s += SL(Z_SRED, f'<rect x="{ix:.0f}" y="{600-i*20:.0f}" width="{iw:.0f}"'
                        f' height="200" fill="#5e4430" stroke="{K}" stroke-width="6"/>')
        s += SL(Z_SRED, brevna(ix, 600 - i * 20, iw, 200, 54, i))
        s += SL(Z_SRED, f'<path d="M{ix-40:.0f},{600-i*20:.0f} l{iw*.5+40:.0f},{-130:.0f}'
                        f' l{iw*.5+40:.0f},{130:.0f} Z" fill="#4a3526" stroke="{K}"'
                        f' stroke-width="5.5"/>'
                        f'<path d="M{ix-40:.0f},{600-i*20:.0f} l{iw*.5+40:.0f},{-130:.0f}'
                        f' l{iw*.5+40:.0f},{130:.0f}" fill="none" stroke="url(#sneg)"'
                        f' stroke-width="16" opacity=".9"/>')
        for k in range(4):
            s += SL(Z_SRED, f'<rect x="{ix+30+k*(iw-80)/3:.0f}" y="800" width="26"'
                            f' height="200" fill="#54351f" stroke="{K}"'
                            f' stroke-width="4"/>')
        s += SL(Z_SRED, f'<rect x="{ix+iw*.3:.0f}" y="{650-i*20:.0f}" width="90"'
                        f' height="80" rx="5" fill="#ffd98a"'
                        f' opacity="{.7+.2*A.w(t,4.0,i*.4):.2f}" stroke="{K}"'
                        f' stroke-width="4"/>')
        s += SL(Z_SRED, dym_stolbom(ix + iw * .18, 460 - i * 20, t, 300, .45, .4, 6))
    # ЛОДОЧНЫЙ САРАЙ с проёмом
    sx, sy, sw, sh_ = 920, 480, 820, 420
    s += SL(Z_SRED, f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="{sh_:.0f}"'
                    f' fill="#5e4430" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M{sx-50:.0f},{sy:.0f} l{sw*.5+50:.0f},{-150:.0f}'
                    f' l{sw*.5+50:.0f},{150:.0f} Z" fill="#4a3526" stroke="{K}"'
                    f' stroke-width="5.5"/>')
    px, py, pw, ph_ = sx + 20, sy + 60, 780, 320
    pr = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
          f' fill="#6f7a84"/>')
    pr += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.4:.0f}"'
           f' fill="#8a98a8"/>')
    pr += mesto_stoka(px, py, pw, ph_, "pryam")
    pr += (f'<rect x="{px-14:.0f}" y="{py-14:.0f}" width="{pw+28:.0f}"'
           f' height="{ph_+28:.0f}" fill="none" stroke="#3f2d1c" stroke-width="22"/>')
    s += SL(Z_SRED, pr)
    for i in (-1, 1):
        s += SL(Z_SRED, f'<g transform="rotate({i*22} {px + (0 if i<0 else pw):.0f}'
                        f' {py:.0f})">'
                        f'<rect x="{px + (0 if i<0 else pw) - (70 if i>0 else 0):.0f}"'
                        f' y="{py-10:.0f}" width="70" height="{ph_+30:.0f}"'
                        f' fill="url(#derev)" stroke="{K}" stroke-width="5"/></g>')
    # БЕРЕГ, карбас, сети на шестах, бочки, якорь
    s += SL(Z_SRED, f'<path d="M-40,1080 Q500,900 1080,870 L1920,850 L1920,1080 Z"'
                    f' fill="#6f6256" stroke="{K}" stroke-width="5"/>')
    for i in range(24):
        s += SL(Z_SRED, f'<ellipse cx="{rnd.uniform(-20,1940):.0f}"'
                        f' cy="{rnd.uniform(890,1070):.0f}" rx="{rnd.uniform(14,46):.0f}"'
                        f' ry="{rnd.uniform(6,16):.0f}" fill="#8a8078" opacity=".7"/>')
    s += SL(Z_SRED, karbas_pod_parusom(420, 960, 420, t, .2))
    for i, nx_ in enumerate((200, 420, 640)):
        s += SL(Z_SRED, f'<rect x="{nx_:.0f}" y="640" width="14" height="300"'
                        f' fill="#7d5636" stroke="{K}" stroke-width="3.4"/>')
        kch = 6 * A.w(t, 3.0, i * .4)
        for k in range(6):
            s += SL(Z_SRED, f'<path d="M{nx_+7:.0f},{680+k*40:.0f}'
                            f' q{100+kch:.0f},{20:.0f} {210:.0f},{-6:.0f}" fill="none"'
                            f' stroke="#b9a37a" stroke-width="2.6" opacity=".85"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<path d="M{1500+i*110:.0f},1050 q{-14:.0f},{-80:.0f}'
                        f' {40:.0f},{-86:.0f} q{54:.0f},{6:.0f} {40:.0f},{86:.0f} Z"'
                        f' fill="url(#derev)" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<path d="M1300,1000 l0,-120 M1240,900 h120 M1300,1000'
                    f' q{-60:.0f},{-10:.0f} {-70:.0f},{-60:.0f} M1300,1000'
                    f' q{60:.0f},{-10:.0f} {70:.0f},{-60:.0f}" fill="none"'
                    f' stroke="{ZHELEZ}" stroke-width="12"/>')
    # ПОМОР поднимает свёрток, ЖЕНА на крыльце
    pod = A.ease(A.seg(t, .6, 1.6))
    hx, hy, hh = 940, 1050, 720
    s += SL(Z_SRED, figura(hx, hy, hh, t, col="#3f4a56", kant="#cfe4f5",
                           boroda=True, shapka=True, tulup=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(hx, hy, hh, 1, hh * .30, -30 - 24 * pod, t,
                              "#3f4a56", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(hx, hy, hh, -1, hh * .30, -28 - 22 * pod, t,
                              "#3f4a56", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<ellipse cx="{(e1x+e2x)*.5:.0f}" cy="{e1y-20:.0f}" rx="86"'
                    f' ry="44" fill="{RUSH}" stroke="{K}" stroke-width="5"'
                    f' transform="rotate(-14 {(e1x+e2x)*.5:.0f} {e1y-20:.0f})"/>'
                    f'<circle cx="{(e1x+e2x)*.5+60:.0f}" cy="{e1y-34:.0f}" r="26"'
                    f' fill="#f0cfae" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, para_izo_rta(hx - 36, hy - hh * .80, t, .3, 1.1, .5))
    zx, zy, zh = 1660, 800, 560
    s += SL(Z_SRED, figura(zx, zy, zh, t, col="#4a3a52", kant="#cfe4f5",
                           platok=True, ph=.7))
    r3, (e3x, e3y), _ = _ruka(zx, zy, zh, -1, zh * .26, 50, t, "#4a3a52", "#cfe4f5", .4, 4)
    s += SL(Z_SRED, r3)
    for i in range(5):
        a = (t * .22 + i * .2) % 1.0
        s += SL(Z_LETIT, f'<path d="M{200+1400*a:.0f},{260+70*math.sin(a*6+i):.0f}'
                         f' q{16:.0f},{-14:.0f} {32:.0f},0 q{16:.0f},{-14:.0f} {32:.0f},0"'
                         f' fill="none" stroke="#f4f1e8" stroke-width="4" opacity=".9"/>')
    s += SL(Z_SRED, par(1400, 1000, t, 4, .5, 160, .45, 1.0))
    s += SL(Z_SRED, ten(hx, hy + 6, 140, 24, .45))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.44)
    return s


def malchik_s_knigoy_na_karbase(t):
    """Карбас под парусом в море, корма на пол-кадра: отец-помор у рулевого
    весла, мальчик в тулупчике сидит на бочонке с рыбой и читает толстую
    книгу, губы шевелятся; рядом в коробе ещё две книги."""
    rnd = random.Random(3026)
    s = nebo("rassv", t, False, 461)
    s += oblaka(t, 150, 5, 239, .40, "#ffe9c8")
    s += SL(Z_DAL, f'<rect x="0" y="480" width="{W}" height="600" fill="#4a6a78"/>')
    for i in range(16):
        yy = 500 + i * 36
        s += SL(Z_DAL, f'<path d="M{rnd.uniform(-60,200):.0f},{yy:.0f}'
                       f' q{rnd.uniform(200,500):.0f},{rnd.uniform(-16,16):.0f}'
                       f' {rnd.uniform(900,1960):.0f},{rnd.uniform(-10,10):.0f}"'
                       f' fill="none" stroke="#5f8a98" stroke-width="{rnd.uniform(3,8):.1f}"'
                       f' opacity=".6"/>')
    # берег вдали
    s += SL(Z_DAL, f'<path d="M0,470 q{300:.0f},{-40:.0f} {600:.0f},{-6:.0f}'
                   f' q{400:.0f},{30:.0f} {1320:.0f},{-10:.0f} l0,{40:.0f} l{-1920:.0f},0 Z"'
                   f' fill="#4a5664" opacity=".9"/>')
    # КАРБАС на пол-кадра
    s += SL(Z_SRED, karbas_pod_parusom(900, 820, 1180, t, .1))
    # ОТЕЦ у рулевого весла
    ox, oy, oh = 1420, 800, 600
    s += SL(Z_SRED, figura(ox, oy, oh, t, col="#3f4a56", kant="#cfe4f5",
                           boroda=True, shapka=True, tulup=True, ph=.2))
    r1, (e1x, e1y), _ = _ruka(ox, oy, oh, 1, oh * .30, 20, t, "#3f4a56", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ox, oy, oh, -1, oh * .26, 26, t, "#3f4a56", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x:.0f},{e1y:.0f} l{200:.0f},{180:.0f}"'
                    f' stroke="#7d5636" stroke-width="14" stroke-linecap="round"/>'
                    f'<path d="M{e1x+200:.0f},{e1y+180:.0f} l{60:.0f},{60:.0f}'
                    f' l{-30:.0f},{30:.0f} Z" fill="#6b4428" stroke="{K}"'
                    f' stroke-width="4"/>')
    bor = 10 * A.w(t, 1.8, .2)
    s += SL(Z_SRED, f'<path d="M{ox-20:.0f},{oy-oh*.80:.0f} q{-60-bor:.0f},{40:.0f}'
                    f' {-110-bor:.0f},{70:.0f}" fill="none" stroke="#ded3c4"'
                    f' stroke-width="18" stroke-linecap="round"/>')
    # МАЛЬЧИК на бочонке с книгой
    mx, my, mh = 760, 880, 440
    s += SL(Z_SRED, f'<path d="M{mx-70:.0f},{my:.0f} h140 l-10,-110 h-120 Z"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="5"/>'
                    f'<ellipse cx="{mx:.0f}" cy="{my-110:.0f}" rx="60" ry="18"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="4"/>')
    for k in (.3, .7):
        s += SL(Z_SRED, f'<rect x="{mx-68:.0f}" y="{my-110+110*k:.0f}" width="136"'
                        f' height="10" fill="{ZHELEZ}" opacity=".9"/>')
    s += SL(Z_SRED, figura(mx, my - 110, mh, t, col="#8a7a62", kant="#cfe4f5",
                           ph=.5, naklon=2.0))
    r3, (e3x, e3y), _ = _ruka(mx, my - 110, mh, 1, mh * .30, 14, t,
                              "#8a7a62", "#cfe4f5", .3, 4)
    r4, (e4x, e4y), _ = _ruka(mx, my - 110, mh, -1, mh * .30, 18, t,
                              "#8a7a62", "#cfe4f5", .8, 4)
    s += SL(Z_SRED, r3 + r4)
    kn_x, kn_y = (e3x + e4x) * .5 - 90, e3y - 20
    s += SL(Z_SRED, uchebnik_razvorot(kn_x, kn_y, 180, 130, t, False, .3))
    s += SL(Z_SRED, f'<path d="M{kn_x-14:.0f},{kn_y-10:.0f} q{100:.0f},{-26:.0f}'
                    f' {208:.0f},0 l0,{18:.0f} q{-104:.0f},{-20:.0f} {-208:.0f},0 Z"'
                    f' fill="#6b3a2a" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, para_izo_rta(mx - 24, my - 110 - mh * .78, t, .4, .8, .45))
    # КОРОБ с двумя книгами, сети, бочки
    s += SL(Z_SRED, f'<rect x="420" y="880" width="200" height="120" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>')
    for i in range(2):
        s += SL(Z_SRED, f'<rect x="{440+i*18:.0f}" y="{850-i*20:.0f}" width="150"'
                        f' height="36" rx="5" fill="#6b3a2a" stroke="{K}"'
                        f' stroke-width="4"/>')
    for i, nx_ in enumerate((300, 560)):
        for k in range(5):
            s += SL(Z_SRED, f'<path d="M{nx_:.0f},{720+k*34:.0f} q{90:.0f},{24:.0f}'
                            f' {180:.0f},{-6:.0f}" fill="none" stroke="#b9a37a"'
                            f' stroke-width="2.6" opacity=".8"/>')
    # ЧАЙКА садится на борт
    sad = A.ease(A.seg(t, 1.2, 1.6))
    cx_, cy_ = 1180 - 180 * sad, 420 + 280 * sad
    s += SL(Z_SRED, f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="34" ry="20"'
                    f' fill="#f4f1e8" stroke="{K}" stroke-width="3.6"/>'
                    f'<circle cx="{cx_+26:.0f}" cy="{cy_-16:.0f}" r="14" fill="#f4f1e8"'
                    f' stroke="{K}" stroke-width="3"/>'
                    f'<path d="M{cx_+40:.0f},{cy_-18:.0f} l20,5 l-20,6 Z" fill="{ZOL}"/>'
                    f'<path d="M{cx_-10:.0f},{cy_-8:.0f} q{20:.0f},{-30*(1-sad)-10:.0f}'
                    f' {50:.0f},{-14:.0f}" fill="none" stroke="#dde3e8"'
                    f' stroke-width="11"/>')
    for i in range(4):
        a = (t * .25 + i * .25) % 1.0
        s += SL(Z_LETIT, f'<path d="M{300+1300*a:.0f},{220+60*math.sin(a*6+i):.0f}'
                         f' q{16:.0f},{-14:.0f} {32:.0f},0 q{16:.0f},{-14:.0f} {32:.0f},0"'
                         f' fill="none" stroke="#f4f1e8" stroke-width="4" opacity=".85"/>')
    s += SL(Z_SRED, par(1420, 760, t, 4, .5, 160, .45, 1.0))
    s += SL(Z_PERED, f'<path d="M-40,1080 q{300:.0f},{-120:.0f} {700:.0f},{-60:.0f}'
                     f' l0,200 l{-740:.0f},0 Z" fill="#2f4a52" opacity=".85"/>')
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def oboz_na_zimney_doroge(t):
    """Зимняя ночная дорога через лес под луной: впереди тянется обоз с
    мороженой рыбой, за последними санями идёт рослый парень с книгами у
    груди. В глубине дорога уходит в просвет между елями — настоящий кадр."""
    rnd = random.Random(3027)
    s = nebo("noch", t, True, 463)
    s += SL(Z_NEBO, luna_v_gorode(1560, 170, t, .9, True))
    # ПРОЁМ: дорога уходит в просвет между елями (по центру чуть выше середины)
    px, py, pw, ph_ = 560, 330, 800, 340
    pr = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
          f' fill="#2b3550"/>')
    pr += (f'<rect x="{px:.0f}" y="{py+ph_*.5:.0f}" width="{pw:.0f}"'
           f' height="{ph_*.5:.0f}" fill="#dce7f2" opacity=".55"/>')
    pr += mesto_stoka(px, py, pw, ph_, "pryam")
    s += SL(Z_SRED, pr)
    # ЕЛИ по сторонам — ПОВЕРХ проёма (передний план)
    for i, (ex_, eb, eh) in enumerate(((60, 980, 620), (260, 1010, 540),
                                       (420, 940, 460), (1500, 990, 580),
                                       (1700, 1020, 640), (1860, 960, 500))):
        s += SL(Z_SRED, f'<path d="M{ex_:.0f},{eb:.0f} l{eh*.26:.0f},{-eh*.34:.0f}'
                        f' l{-eh*.10:.0f},0 l{eh*.20:.0f},{-eh*.30:.0f}'
                        f' l{-eh*.08:.0f},0 l{eh*.16:.0f},{-eh*.36:.0f}'
                        f' l{eh*.16:.0f},{eh*.36:.0f} l{-eh*.08:.0f},0'
                        f' l{eh*.20:.0f},{eh*.30:.0f} l{-eh*.10:.0f},0'
                        f' l{eh*.26:.0f},{eh*.34:.0f} Z" fill="#2f4a3a"'
                        f' stroke="{K}" stroke-width="5"/>')
        s += SL(Z_SRED, f'<path d="M{ex_+eh*.20:.0f},{eb-eh*.40:.0f}'
                        f' q{eh*.14:.0f},{-eh*.06:.0f} {eh*.28:.0f},0" fill="none"'
                        f' stroke="url(#sneg)" stroke-width="12" opacity=".9"/>')
    # ДОРОГА с санным следом
    s += SL(Z_SRED, f'<path d="M-40,1080 Q560,780 860,672 L1060,672 Q1400,790 1960,1080 Z"'
                    f' fill="#dce7f2" stroke="{K}" stroke-width="5"/>')
    for i in (-1, 1):
        s += SL(Z_SRED, f'<path d="M{960+i*300:.0f},1080 Q{960+i*120:.0f},820'
                        f' {960+i*40:.0f},690" fill="none" stroke="#9fb0c0"'
                        f' stroke-width="26" opacity=".8"/>')
    s += SL(Z_SRED, inej_mel(463, 60, 700, 1070))
    # ОБОЗ уходит вперёд
    uh = A.ease(A.seg(t, .3, 4.0))
    for i in range(3):
        sx_ = 1060 - i * 230 + 160 * uh
        sy_ = 760 + i * 90
        s += SL(Z_SRED, sani_s_rogozhey(sx_, sy_, .5 + i * .18, t, i * .3, True))
        s += SL(Z_SRED, f'<ellipse cx="{sx_-150-i*40:.0f}" cy="{sy_-60-i*20:.0f}"'
                        f' rx="{40+i*12:.0f}" ry="{70+i*20:.0f}" fill="#2b2419"'
                        f' opacity=".92" stroke="{K}" stroke-width="4"/>')
    # ПАРЕНЬ с книгами у груди
    px_, py_, ph2 = 760, 1050, 700
    shag = A.ease(A.seg(t, .4, 3.4))
    s += SL(Z_SRED, figura(px_ + 120 * shag, py_, ph2, t, col="#5e4430",
                           kant="#cfe4f5", tulup=True, shapka=True, ph=.2,
                           naklon=2.0))
    r1, (e1x, e1y), _ = _ruka(px_ + 120 * shag, py_, ph2, 1, ph2 * .24, 24, t,
                              "#5e4430", "#cfe4f5", .2, 4)
    r2, (e2x, e2y), _ = _ruka(px_ + 120 * shag, py_, ph2, -1, ph2 * .24, 28, t,
                              "#5e4430", "#cfe4f5", .6, 4)
    s += SL(Z_SRED, r1 + r2)
    kx_, ky_ = px_ + 120 * shag, py_ - ph2 * .48
    s += SL(Z_SRED, f'<rect x="{kx_-80:.0f}" y="{ky_-20:.0f}" width="160" height="44"'
                    f' rx="6" fill="#6b3a2a" stroke="{K}" stroke-width="4.5"/>'
                    f'<rect x="{kx_-72:.0f}" y="{ky_+24:.0f}" width="150" height="40"'
                    f' rx="6" fill="#8a2f22" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, f'<path d="M{kx_-100:.0f},{ky_-60:.0f} q{-50:.0f},{80:.0f}'
                    f' {-20:.0f},{170:.0f} q{50:.0f},{20:.0f} {80:.0f},{-20:.0f} Z"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="4.5"/>')
    s += SL(Z_SRED, para_izo_rta(kx_ - 40, py_ - ph2 * .80, t, .3, 1.2, .6))
    s += SL(Z_SRED, f'<path d="M{kx_-40:.0f},{py_-ph2*.84:.0f} h{80:.0f}"'
                    f' stroke="{INEY}" stroke-width="7" opacity=".8"/>')
    s += SL(Z_SRED, ten(kx_, py_ + 6, 130, 22, .4))
    # СЧЁТЧИК ВЁРСТ растёт (палочки, без цифр)
    n = 1 + int((t * 1.2) % 6)
    for i in range(n):
        s += SL(Z_SRED, f'<rect x="{1180+i*46:.0f}" y="200" width="16" height="70"'
                        f' rx="6" fill="#d6a63f" opacity=".9"/>')
    # деревня позади: гаснущее окно
    gas = max(.0, 1 - A.ease(A.seg(t, 1.6, 1.6)))
    s += SL(Z_DAL, izba_snaruzhi(120, 700, 220, t, gas > .4, True, 107))
    s += SL(Z_SRED, f'<rect x="160" y="620" width="80" height="60" rx="5"'
                    f' fill="#ffd98a" opacity="{gas:.2f}"/>')
    # верстовой столб и заячий след
    s += SL(Z_SRED, verstovoy_stolb(1420, 940, 300, t, 1.0, .2))
    for i in range(6):
        sx2 = 300 + i * 90
        sy2 = 980 + ((i * 7) % 3) * 22
        s += SL(Z_SRED, f'<ellipse cx="{sx2:.0f}" cy="{sy2:.0f}" rx="13" ry="20"'
                        f' fill="#9fb0c0" opacity=".8"/>'
                        f'<ellipse cx="{sx2+22:.0f}" cy="{sy2-10:.0f}" rx="11" ry="17"'
                        f' fill="#9fb0c0" opacity=".8"/>')
    s += SL(Z_LETIT, sneg_letit(t, 28, 109, .45, .6))
    s += ramka_pp("oba", "#0e0c0b", .55)
    s += vinetka(.46)
    return s


def sannyy_sled_do_vorot(t):
    """Вид сверху: два ровных санных следа тянутся от деревни у моря через
    леса и поля до городских ворот с башнями. По следу идёт фигурка с
    котомкой и книгами; над деревней значок-рыба, над воротами значок-книга."""
    rnd = random.Random(3028)
    s = (f'<rect width="{W}" height="{H}" fill="#dce7f2"/>')
    s += SL(Z_NEBO, f'<rect width="{W}" height="{H}" fill="#cfe0ee" opacity=".6"/>')
    # ПОЛЯ и ЛЕСА сверху
    for i in range(9):
        s += SL(Z_DAL, f'<path d="M{rnd.uniform(-100,400):.0f},{80+i*120:.0f}'
                       f' q{rnd.uniform(400,900):.0f},{rnd.uniform(-50,50):.0f}'
                       f' {rnd.uniform(1400,2000):.0f},{rnd.uniform(-30,30):.0f}"'
                       f' fill="none" stroke="#c4d8e8" stroke-width="{rnd.uniform(14,40):.0f}"'
                       f' opacity=".8"/>')
    for i in range(34):
        ex_ = rnd.uniform(-20, 1900)
        ey_ = rnd.uniform(120, 1040)
        eh = rnd.uniform(40, 90)
        s += SL(Z_DAL, f'<path d="M{ex_:.0f},{ey_:.0f} l{eh*.4:.0f},{-eh:.0f}'
                       f' l{eh*.4:.0f},{eh:.0f} Z" fill="#2f4a3a" opacity=".92"'
                       f' stroke="{K}" stroke-width="3"/>')
    # РЕКИ подо льдом
    for i in range(2):
        s += SL(Z_SRED, f'<path d="M{-40+i*700:.0f},{1080:.0f}'
                        f' Q{400+i*500:.0f},{700-i*200:.0f} {900+i*600:.0f},{120:.0f}"'
                        f' fill="none" stroke="#9fc4d8" stroke-width="46"'
                        f' opacity=".85"/>')
    # ДЕРЕВНЯ у моря (слева внизу) и ГОРОД с воротами (справа вверху)
    s += SL(Z_SRED, f'<path d="M-40,1080 q{200:.0f},{-120:.0f} {420:.0f},{-80:.0f}'
                    f' l0,{200:.0f} l{-440:.0f},0 Z" fill="#6f7a84" opacity=".8"/>')
    for i, (ix, iy) in enumerate(((120, 960), (240, 1010), (330, 940))):
        s += SL(Z_SRED, izba_snaruzhi(ix, iy, 120, t, True, True, 113 + i)
                + dym_stolbom(ix + 14, iy - 76, t, 160, .4, .35, 5))
    s += SL(Z_SRED, f'<rect x="1480" y="120" width="380" height="240" rx="8"'
                    f' fill="#c3ab8a" stroke="{K}" stroke-width="6"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<rect x="{1490+i*62:.0f}" y="100" width="32" height="24"'
                        f' fill="#c3ab8a" stroke="{K}" stroke-width="3"/>')
    for bx in (1460, 1820):
        s += SL(Z_SRED, f'<rect x="{bx:.0f}" y="60" width="80" height="300"'
                        f' fill="#cbb492" stroke="{K}" stroke-width="5"/>'
                        f'<path d="M{bx-14:.0f},60 l{47:.0f},{-44:.0f} l{47:.0f},{44:.0f} Z"'
                        f' fill="#a8552f" stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M1600,360 l0,-110 q{70:.0f},{-60:.0f} {140:.0f},0 l0,110 Z"'
                    f' fill="#3f2d1c" stroke="{K}" stroke-width="5"/>')
    # САННЫЙ СЛЕД: две ровные колеи через весь кадр
    put = "M300,1000 Q700,860 980,620 Q1240,420 1600,330"
    for i, off in enumerate((-16, 16)):
        s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#9fb0c0"'
                        f' stroke-width="14" opacity=".9"'
                        f' transform="translate({off},{off*.5:.0f})"/>')
    s += SL(Z_SRED, f'<path d="{put}" fill="none" stroke="#eaf6ff" stroke-width="46"'
                    f' opacity=".35"/>')
    # ФИГУРКА идёт по следу
    idt = A.ease(A.seg(t, .3, 3.6))
    fx = 300 + (1600 - 300) * idt
    fy = 1000 - 670 * (idt ** .92)
    s += SL(Z_SRED, figura(fx, fy, 170, t, col="#5e4430", kant="#cfe4f5",
                           shapka=True, tulup=True, ph=.3))
    s += SL(Z_SRED, f'<rect x="{fx-26:.0f}" y="{fy-100:.0f}" width="52" height="30"'
                    f' rx="5" fill="#6b3a2a" stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, f'<path d="M{fx-34:.0f},{fy-120:.0f} q{-20:.0f},{30:.0f}'
                    f' {-8:.0f},{60:.0f} q{20:.0f},{8:.0f} {30:.0f},{-8:.0f} Z"'
                    f' fill="#b9a37a" stroke="{K}" stroke-width="3.4"/>')
    # ЗНАЧКИ: рыба над деревней, книга над воротами
    s += SL(Z_SRED, f'<g opacity="{1-idt*.7:.2f}">'
                    f'<ellipse cx="260" cy="860" rx="56" ry="30" fill="#8aa8b4"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M316,860 l{30:.0f},{-20:.0f} l0,{40:.0f} Z"'
                    f' fill="#6f7a84" stroke="{K}" stroke-width="3.4"/>'
                    f'<circle cx="236" cy="854" r="5" fill="{K}"/></g>')
    gor_ = A.ease(A.seg(t, 2.4, 1.2))
    s += SL(Z_SRED, f'<g opacity="{gor_:.2f}">'
                    f'<rect x="1600" y="180" width="120" height="86" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="4.5"/>'
                    f'<path d="M1660,180 v86" stroke="#c9bfa6" stroke-width="6"/>'
                    f'<circle cx="1660" cy="222" r="{70*gor_:.0f}" fill="#ffe9ac"'
                    f' opacity="{.35*gor_:.2f}"/></g>')
    # верстовые столбы вдоль следа
    for i, (vx_, vy_) in enumerate(((520, 920), (820, 760), (1120, 560), (1400, 420))):
        s += SL(Z_SRED, verstovoy_stolb(vx_, vy_, 90, t, .5, i * .2))
    s += SL(Z_LETIT, sneg_letit(t, 22, 113, .4, .5))
    s += ramka_pp("oba", "#0e0c0b", .45)
    s += vinetka(.42)
    return s


def kabinet_uchenogo(t):
    """Кабинет восемнадцатого века: стол с колбами, телескоп на треноге,
    глобус, стопы книг, мозаичное панно без сюжета, гусиные перья. Учёный в
    камзоле стоит со спины и держит колбу на свету."""
    rnd = random.Random(3029)
    s = (f'<rect width="{W}" height="{H}" fill="#2b2419"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="840" fill="#5e4430"/>')
    for i in range(14):
        s += SL(Z_DAL, f'<rect x="{-10+i*140:.0f}" y="0" width="118" height="840"'
                       f' fill="#6b4c32" opacity=".55"/>')
    s += SL(Z_DAL, svody(t, "#4b443b", 3))
    s += SL(Z_SRED, polovicy(840, "#7a5436"))
    # ОКНО и ПЕЧЬ с изразцами
    s += SL(Z_SRED, f'<rect x="1480" y="140" width="380" height="440" rx="10"'
                    f' fill="#2b3550" stroke="{K}" stroke-width="7"/>'
                    f'<rect x="1510" y="170" width="320" height="380" fill="#8aa8b4"'
                    f' opacity=".5"/>'
                    f'<path d="M1670,140 v440 M1480,360 h380" stroke="#e4d8bd"'
                    f' stroke-width="16"/>')
    s += SL(Z_SRED, f'<rect x="60" y="180" width="300" height="660" rx="8"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="6"/>')
    for i in range(18):
        s += SL(Z_SRED, f'<rect x="{80+(i%3)*94:.0f}" y="{210+(i//3)*100:.0f}"'
                        f' width="84" height="88" rx="6" fill="#dce7f2" stroke="#9fc4d8"'
                        f' stroke-width="4"/>'
                        f'<path d="M{96+(i%3)*94:.0f},{250+(i//3)*100:.0f}'
                        f' q{26:.0f},{-26:.0f} {52:.0f},0" fill="none" stroke="#6f8ca8"'
                        f' stroke-width="4"/>')
    # СТОЛ с колбами, перьями, стопами книг
    s += SL(Z_SRED, stol(420, 760, 1000, 46, True))
    for i, (kx_, ks) in enumerate(((560, 1.0), (680, .78), (780, .9))):
        s += SL(Z_SRED, f'<path d="M{kx_-40*ks:.0f},{760:.0f} q{-20*ks:.0f},{-80*ks:.0f}'
                        f' {30*ks:.0f},{-110*ks:.0f} l0,{-50*ks:.0f} h{20*ks:.0f}'
                        f' l0,{50*ks:.0f} q{50*ks:.0f},{30*ks:.0f} {30*ks:.0f},{110*ks:.0f} Z"'
                        f' fill="{STEKLO}" opacity=".55" stroke="{K}"'
                        f' stroke-width="{4*ks:.1f}"/>'
                        f'<path d="M{kx_-30*ks:.0f},{740:.0f} q{30*ks:.0f},{14*ks:.0f}'
                        f' {60*ks:.0f},0 l0,{20*ks:.0f} h{-60*ks:.0f} Z"'
                        f' fill="{["#6f8c4a","#8a2f22","#3f6b7a"][i]}" opacity=".85"/>')
    for i in range(3):
        s += SL(Z_SRED, f'<rect x="{1180+i*10:.0f}" y="{700-i*26:.0f}" width="170"'
                        f' height="26" rx="5" fill="#6b3a2a" stroke="{K}"'
                        f' stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M1420,760 h90 l-10,-50 h-70 Z" fill="#3f3a33"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<path d="M1470,712 l{60:.0f},{-120:.0f}" stroke="#e8e2d6"'
                    f' stroke-width="8"/>'
                    f'<path d="M1524,596 q{24:.0f},{-36:.0f} {36:.0f},{-8:.0f}'
                    f' q{-16:.0f},{24:.0f} {-30:.0f},{28:.0f} Z" fill="#f4f1e8"'
                    f' stroke="{K}" stroke-width="3"/>')
    # ГЛОБУС с бегущими лучами
    gx, gy = 980, 640
    s += SL(Z_SRED, f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="110" fill="#8aa8b4"'
                    f' stroke="{K}" stroke-width="6"/>'
                    f'<path d="M{gx-110:.0f},{gy:.0f} q{110:.0f},{-50:.0f} {220:.0f},0'
                    f' q{-110:.0f},{50:.0f} {-220:.0f},0 Z" fill="#6f8c4a" opacity=".8"/>'
                    f'<path d="M{gx-70:.0f},{gy-70:.0f} q{70:.0f},{30:.0f} {140:.0f},{10:.0f}"'
                    f' fill="none" stroke="#56763f" stroke-width="12" opacity=".85"/>'
                    f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="110" ry="40" fill="none"'
                    f' stroke="#c9bfa6" stroke-width="4"/>'
                    f'<path d="M{gx:.0f},{gy+110:.0f} l0,{50:.0f} h{-40:.0f} h{80:.0f}"'
                    f' fill="none" stroke="#6b4428" stroke-width="9"/>')
    for i in range(5):
        d = ((t * .6 + i / 5.0) % 1.0)
        a = -2.2 + i * .7
        s += SL(Z_SRED, f'<path d="M{gx:.0f},{gy:.0f} l{(110+120*d)*math.cos(a):.0f},'
                        f'{(110+120*d)*math.sin(a):.0f}" stroke="#ffd98a"'
                        f' stroke-width="{6-3*d:.1f}" opacity="{(1-d)*.8:.2f}"/>')
    # ТЕЛЕСКОП на треноге
    s += SL(Z_SRED, f'<g transform="rotate(-24 1600 820)">'
                    f'<rect x="1500" y="520" width="220" height="60" rx="26"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1700" y="534" width="70" height="34" rx="14"'
                    f' fill="{MED}" stroke="{K}" stroke-width="4"/></g>'
                    f'<path d="M1600,820 l{-80:.0f},{220:.0f} M1600,820 l{10:.0f},{230:.0f}'
                    f' M1600,820 l{90:.0f},{210:.0f}" stroke="#6b4428" stroke-width="11"/>')
    bl = .5 + .5 * A.w(t, 2.6, .2)
    s += SL(Z_SRED, f'<circle cx="1772" cy="548" r="14" fill="#cfe4f5"'
                    f' opacity="{bl:.2f}"/>')
    # УЧЁНЫЙ со спины и вполоборота
    ux, uy, uh = 760, 1050, 720
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#4a3a52", kant="#ffd98a",
                           ph=.2, profil=True))
    s += SL(Z_SRED, f'<path d="M{ux-110:.0f},{uy-uh*.62:.0f} q{110:.0f},{-24:.0f}'
                    f' {220:.0f},0 l{20:.0f},{uh*.40:.0f} q{-130:.0f},{30:.0f}'
                    f' {-260:.0f},0 Z" fill="#6b4a6a" stroke="{K}" stroke-width="5"/>')
    for i in range(6):
        s += SL(Z_SRED, f'<circle cx="{ux-10:.0f}" cy="{uy-uh*.56+i*44:.0f}" r="9"'
                        f' fill="{ZOL}" stroke="{K}" stroke-width="2.6"/>')
    s += SL(Z_SRED, f'<path d="M{ux-70:.0f},{uy-uh*.84:.0f} q{70:.0f},{-40:.0f}'
                    f' {140:.0f},0 q{-10:.0f},{80:.0f} {-70:.0f},{86:.0f}'
                    f' q{-60:.0f},{-6:.0f} {-70:.0f},{-86:.0f} Z" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>')
    r1, (e1x, e1y), _ = _ruka(ux, uy, uh, 1, uh * .30, -34, t, "#4a3a52", "#ffd98a", .2, 4)
    r2, (e2x, e2y), _ = _ruka(ux, uy, uh, -1, uh * .26, 30, t, "#4a3a52", "#ffd98a", .7, 4)
    s += SL(Z_SRED, r1 + r2)
    s += SL(Z_SRED, f'<path d="M{e1x-26:.0f},{e1y:.0f} q{-10:.0f},{-60:.0f}'
                    f' {26:.0f},{-80:.0f} q{36:.0f},{20:.0f} {26:.0f},{80:.0f} Z"'
                    f' fill="{STEKLO}" opacity=".6" stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{e1x:.0f}" cy="{e1y-60:.0f}" r="{24+8*bl:.0f}"'
                    f' fill="#ffe9ac" opacity="{.3+.3*bl:.2f}"/>')
    s += SL(Z_SRED, svecha(1300, 760, t, .2, 1.4, 100) + teplo(1300, 700, 300, 250, .45))
    s += SL(Z_SRED, hodiki(1180, 240, t, 1.4))
    s += SL(Z_SRED, ten(ux, uy + 6, 140, 24, .45))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s


def klass_uchit_naizust(t):
    """Школьный класс: ученица с косичками читает наизусть у доски, над ней
    всплывают строчки-завитки; учительница водит ручкой по журналу, двое за
    первой партой подсказывают из-за учебника."""
    rnd = random.Random(3030)
    s = (f'<rect width="{W}" height="{H}" fill="#cbb492"/>')
    s += SL(Z_DAL, f'<rect x="0" y="0" width="{W}" height="600" fill="#d8cbb0"/>'
                   f'<rect x="0" y="600" width="{W}" height="56" fill="#8a7a52"'
                   f' opacity=".85"/>')
    s += SL(Z_DAL, klassnaya_doska(300, 140, 760, 400, t, 17))
    s += SL(Z_DAL, okno_izby(1560, 130, 320, 340, t, None, .25, False, True))
    s += SL(Z_SRED, polovicy(740, "#8a6342"))
    # ПОРТРЕТНАЯ РАМА над доской — нарисованная контуром
    s += SL(Z_SRED, f'<rect x="560" y="20" width="240" height="110" rx="8"'
                    f' fill="#8a6342" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="580" y="36" width="200" height="78" rx="5"'
                    f' fill="#e4d8bd" stroke="{K}" stroke-width="3.6"/>'
                    f'<ellipse cx="680" cy="86" rx="40" ry="34" fill="none"'
                    f' stroke="#8a7a62" stroke-width="5"/>'
                    f'<path d="M652,110 q{28:.0f},{-20:.0f} {56:.0f},0" fill="none"'
                    f' stroke="#8a7a62" stroke-width="5"/>')
    # УЧЕНИЦА у доски
    ux, uy, uh = 1180, 1000, 560
    s += SL(Z_SRED, figura(ux, uy, uh, t, col="#3f3a4a", kant="#ffd98a", ph=.2))
    s += SL(Z_SRED, f'<path d="M{ux-26:.0f},{uy-uh*.84:.0f} q{26:.0f},{80:.0f}'
                    f' {10:.0f},{150:.0f}" fill="none" stroke="#6b4428"'
                    f' stroke-width="16"/>'
                    f'<path d="M{ux+26:.0f},{uy-uh*.84:.0f} q{-20:.0f},{80:.0f}'
                    f' {-6:.0f},{150:.0f}" fill="none" stroke="#6b4428"'
                    f' stroke-width="16"/>')
    r1, (e1x, e1y), _ = _ruka(ux, uy, uh, 1, uh * .26, 64, t, "#3f3a4a", "#ffd98a", .2, 3)
    r2, (e2x, e2y), _ = _ruka(ux, uy, uh, -1, uh * .26, 66, t, "#3f3a4a", "#ffd98a", .6, 3)
    s += SL(Z_SRED, r1 + r2)
    # СТРОЧКИ-ЗАВИТКИ всплывают
    for i in range(5):
        d = ((t * .45 + i / 5.0) % 1.0)
        s += SL(Z_SRED, f'<path d="M{ux-130+30*math.sin(i+d*4):.0f},{uy-uh-40-200*d:.0f}'
                        f' q{50:.0f},{-16:.0f} {100:.0f},0 q{40:.0f},{14:.0f}'
                        f' {80:.0f},{-4:.0f}" fill="none" stroke="#6f6354"'
                        f' stroke-width="{5-2*d:.1f}" opacity="{(1-d)*.8:.2f}"/>')
    # УЧИТЕЛЬНИЦА за столом
    s += SL(Z_SRED, f'<rect x="1480" y="820" width="380" height="40" rx="8"'
                    f' fill="url(#derev)" stroke="{K}" stroke-width="5"/>'
                    f'<rect x="1500" y="860" width="30" height="180" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<rect x="1810" y="860" width="30" height="180" fill="#7d5636"'
                    f' stroke="{K}" stroke-width="4"/>')
    ux2, uy2, uh2 = 1700, 820, 520
    s += SL(Z_SRED, figura(ux2, uy2, uh2, t, col="#6b3a6a", kant="#ffd98a", ph=.6))
    pish = 6 * A.w(t, 1.3, .2)
    r3, (e3x, e3y), _ = _ruka(ux2, uy2, uh2, -1, uh2 * .32, 20 + 6 * pish, t,
                              "#6b3a6a", "#ffd98a", .3, 5)
    s += SL(Z_SRED, r3 + f'<path d="M{e3x:.0f},{e3y:.0f} l{-40:.0f},{-26:.0f}"'
                         f' stroke="#8a6342" stroke-width="7"/>'
                         f'<rect x="{e3x-160:.0f}" y="{e3y-10:.0f}" width="150"'
                         f' height="60" rx="6" fill="#f2ead6" stroke="{K}"'
                         f' stroke-width="4"/>')
    # ДВОЕ за первой партой, один прикрыл рот учебником
    s += SL(Z_SRED, parta_shkolnaya(380, 1040, 460, t, 19, True))
    for i, (px_, ph_) in enumerate(((480, 440), (700, 460))):
        s += SL(Z_SRED, figura(px_, 880, ph_, t, col=["#3f5a6a", "#4a6a3a"][i],
                               kant="#ffd98a", ph=i * .4))
        rk, (ex, ey), _ = _ruka(px_, 880, ph_, 1, ph_ * .28, 10, t,
                                ["#3f5a6a", "#4a6a3a"][i], "#ffd98a", i * .3, 4)
        rk2, (e2x_, e2y_), _ = _ruka(px_, 880, ph_, -1, ph_ * .28, 14, t,
                                     ["#3f5a6a", "#4a6a3a"][i], "#ffd98a", i * .3 + .4, 4)
        s += SL(Z_SRED, rk + rk2)
        if i == 1:
            s += SL(Z_SRED, f'<rect x="{px_-80:.0f}" y="{880-ph_*.86:.0f}" width="160"'
                            f' height="110" rx="8" fill="#6b3a2a" stroke="{K}"'
                            f' stroke-width="4.5"/>'
                            f'<path d="M{px_:.0f},{880-ph_*.86:.0f} v110" stroke="#54351f"'
                            f' stroke-width="6"/>')
    # глобус, карта, цветы
    s += SL(Z_SRED, f'<circle cx="1320" cy="640" r="60" fill="#3f6b7a" stroke="{K}"'
                    f' stroke-width="5"/>'
                    f'<path d="M1262,626 q{58:.0f},{34:.0f} {116:.0f},0" fill="none"'
                    f' stroke="#56763f" stroke-width="7"/>'
                    f'<path d="M1320,700 l0,40 h-30 h60" fill="none" stroke="#6b4428"'
                    f' stroke-width="7"/>')
    s += SL(Z_SRED, f'<rect x="120" y="160" width="140" height="380" rx="6"'
                    f' fill="#f2ead6" stroke="{K}" stroke-width="5"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M140,{200+i*50:.0f} q{34:.0f},{-10:.0f} {68:.0f},0'
                        f' q{20:.0f},{10:.0f} {32:.0f},{-4:.0f}" fill="none"'
                        f' stroke="#9fc4d8" stroke-width="4"/>')
    s += SL(Z_SRED, f'<path d="M1600,500 h110 l-12,-60 h-86 Z" fill="#a8743c"'
                    f' stroke="{K}" stroke-width="4"/>')
    for i in range(5):
        a = -1.1 + i * .55
        s += SL(Z_SRED, f'<path d="M1655,440 q{40*math.sin(a):.0f},{-50:.0f}'
                        f' {62*math.sin(a):.0f},{-110:.0f} q{14:.0f},{30:.0f}'
                        f' {-30*math.sin(a):.0f},{110:.0f} Z" fill="#56763f"'
                        f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, lampa(960, 60, t, 1.3, True) + teplo(960, 80, 300, 250, .40))
    s += SL(Z_SRED, ten(ux, uy + 6, 120, 20, .4))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .45))
    s += vinetka(.42)
    return s


def gorka_vo_dvore(t):
    """Ледяная горка во дворе на пол-кадра в зимних сумерках под фонарём:
    трое съезжают один за другим — на коньках, на санках со спинкой и верхом
    на школьном портфеле. Внизу куча-мала из валенок и варежек."""
    rnd = random.Random(3031)
    s = nebo("sumer", t, True, 467)
    s += SL(Z_DAL, panelka(60, 620, 760, t, 5, True, 79))
    s += SL(Z_DAL, panelka(1420, 600, 500, t, 5, True, 83))
    s += SL(Z_SRED, _merzlaya_zemlya(760, 467, False))
    s += SL(Z_SRED, sneg_lezhit(790, 32, "url(#sneg)"))
    # ГОРКА на пол-кадра
    s += SL(Z_SRED, f'<path d="M420,980 L820,380 L1020,380 L1020,980 Z"'
                    f' fill="#dce7f2" stroke="{K}" stroke-width="6"/>'
                    f'<path d="M1020,380 L1020,980 L1560,1000 Q1300,740 1020,380 Z"'
                    f' fill="url(#led)" stroke="{K}" stroke-width="6"/>')
    for i in range(7):
        s += SL(Z_SRED, f'<path d="M{1040+i*16:.0f},{420+i*76:.0f}'
                        f' q{120:.0f},{100:.0f} {260:.0f},{180:.0f}" fill="none"'
                        f' stroke="#eaf6ff" stroke-width="5" opacity=".6"/>')
    for i in range(6):                 # ступени с другой стороны
        s += SL(Z_SRED, f'<rect x="{480+i*58:.0f}" y="{900-i*88:.0f}" width="80"'
                        f' height="22" rx="5" fill="{DOSKA}" stroke="{K}"'
                        f' stroke-width="3.6"/>')
    s += SL(Z_SRED, f'<path d="M420,980 l0,-120 M820,380 l0,-60" stroke="#8a6342"'
                    f' stroke-width="11"/>'
                    f'<rect x="800" y="300" width="240" height="22" rx="6"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>')
    # ТРОЕ съезжают один за другим
    for i, (vid, col) in enumerate((("konki", "#3f5a6a"), ("sanki", "#8a2f22"),
                                    ("portfel", "#4a6a3a"))):
        d = A.ease(A.seg(t, .4 + i * .9, 1.6))
        if d <= .01:
            continue
        gx_ = 1020 + 520 * d
        gy_ = 400 + 580 * (d ** 1.6)
        if vid == "konki":
            s += SL(Z_SRED, figura(gx_, gy_, 400, t, col=col, kant="#cfe4f5",
                                   shapka=True, ph=.2, naklon=4.0))
            rk, (ex, ey), _ = _ruka(gx_, gy_, 400, 1, 400 * .30, -34, t,
                                    col, "#cfe4f5", .2, 7)
            rk2, (e2x_, e2y_), _ = _ruka(gx_, gy_, 400, -1, 400 * .30, -30, t,
                                         col, "#cfe4f5", .6, 7)
            s += SL(Z_SRED, rk + rk2)
            s += SL(Z_SRED, konki_snegurki(gx_ - 24, gy_, .6, 0, True, t, .2)
                    + konki_snegurki(gx_ + 34, gy_ + 4, .6, 0, True, t, .6))
        elif vid == "sanki":
            s += SL(Z_SRED, sanki_derev(gx_, gy_ + 20, .9, t, .3, True))
            s += SL(Z_SRED, figura(gx_, gy_ - 40, 380, t, col=col, kant="#cfe4f5",
                                   platok=True, ph=.5, naklon=3.0))
            rk, (ex, ey), _ = _ruka(gx_, gy_ - 40, 380, 1, 380 * .28, -12, t,
                                    col, "#cfe4f5", .3, 5)
            rk2, (e2x_, e2y_), _ = _ruka(gx_, gy_ - 40, 380, -1, 380 * .28, -8, t,
                                         col, "#cfe4f5", .8, 5)
            s += SL(Z_SRED, rk + rk2)
            s += SL(Z_SRED, f'<path d="M{gx_+70:.0f},{gy_-120:.0f} q{90:.0f},{-20:.0f}'
                            f' {170:.0f},{-50:.0f} l{8:.0f},{34:.0f} q{-84:.0f},{30:.0f}'
                            f' {-176:.0f},{50:.0f} Z" fill="{TKAN}" stroke="{K}"'
                            f' stroke-width="4"/>')
        else:
            s += SL(Z_SRED, f'<rect x="{gx_-70:.0f}" y="{gy_-20:.0f}" width="140"'
                            f' height="90" rx="10" fill="#6b4428" stroke="{K}"'
                            f' stroke-width="4.5"/>'
                            f'<path d="M{gx_-70:.0f},{gy_+14:.0f} h140" stroke="#54351f"'
                            f' stroke-width="6"/>')
            s += SL(Z_SRED, figura(gx_, gy_ - 20, 370, t, col=col, kant="#cfe4f5",
                                   shapka=True, ph=.8, naklon=5.0))
            rk, (ex, ey), _ = _ruka(gx_, gy_ - 20, 370, 1, 370 * .32, -54, t,
                                    col, "#cfe4f5", .4, 8)
            rk2, (e2x_, e2y_), _ = _ruka(gx_, gy_ - 20, 370, -1, 370 * .32, -50, t,
                                         col, "#cfe4f5", .9, 8)
            s += SL(Z_SRED, rk + rk2)
            s += SL(Z_SRED, f'<ellipse cx="{gx_:.0f}" cy="{gy_-20-370*.80:.0f}" rx="52"'
                            f' ry="26" fill="#4a3a2c" stroke="{K}" stroke-width="4"/>')
    # КУЧА-МАЛА из валенок и варежек внизу
    for i in range(5):
        s += SL(Z_SRED, _valenok(1500 + i * 60, 1050 - ((i * 7) % 3) * 12,
                                 .72, -20 + i * 12))
    for i in range(4):
        s += SL(Z_SRED, varezhka(1480 + i * 80, 990 - ((i * 5) % 3) * 16, .9,
                                 -30 + i * 22, TKAN, t, i * .25))
    # фонарь, собака, дома с жёлтыми окнами
    s += SL(Z_SRED, f'<rect x="300" y="400" width="24" height="520" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="4"/>')
    s += SL(Z_SRED, lampa(312, 400, t, 1.5, True) + teplo(312, 430, 360, 300, .45))
    beg = ((t * .6) % 1.0)
    sx_ = 1740 - 400 * beg
    s += SL(Z_SRED, f'<ellipse cx="{sx_:.0f}" cy="1010" rx="70" ry="34" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="4"/>'
                    f'<circle cx="{sx_-62:.0f}" cy="976" r="28" fill="#6b5230"'
                    f' stroke="{K}" stroke-width="3.6"/>'
                    f'<path d="M{sx_-80:.0f},{956:.0f} l{-12:.0f},{-26:.0f}'
                    f' l{-10:.0f},{26:.0f} Z" fill="#6b5230" stroke="{K}"'
                    f' stroke-width="3"/>'
                    f'<path d="M{sx_+66:.0f},1000 q{36:.0f},{-28:.0f} {52:.0f},{-4:.0f}"'
                    f' fill="none" stroke="#6b5230" stroke-width="9"/>')
    # ДВОР У ГОРКИ: бортики, скамейка, санки у забора, ёлочки, сугробы
    for i in range(9):
        s += SL(Z_SRED, f'<ellipse cx="{120+i*210:.0f}" cy="{1010+((i*5)%3)*18:.0f}"'
                        f' rx="{80+((i*7)%4)*22:.0f}" ry="{24+((i*3)%2)*10:.0f}"'
                        f' fill="url(#sneg)" opacity=".92"/>')
    s += SL(Z_SRED, zabor_shtaket(-40, 820, 460, 180, 467, 58))
    s += SL(Z_SRED, f'<rect x="120" y="940" width="280" height="20" rx="5"'
                    f' fill="{DOSKA}" stroke="{K}" stroke-width="4"/>'
                    f'<rect x="140" y="960" width="20" height="80" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>'
                    f'<rect x="360" y="960" width="20" height="80" fill="{BETON2}"'
                    f' stroke="{K}" stroke-width="3.4"/>')
    s += SL(Z_SRED, sanki_derev(220, 1050, .8, t, .4, True))
    for i, (ex_, eb_, eh_) in enumerate(((1760, 1000, 300), (1880, 1030, 260))):
        s += SL(Z_SRED, f'<path d="M{ex_:.0f},{eb_:.0f} l{eh_*.26:.0f},{-eh_*.36:.0f}'
                        f' l{-eh_*.10:.0f},0 l{eh_*.20:.0f},{-eh_*.32:.0f}'
                        f' l{-eh_*.08:.0f},0 l{eh_*.16:.0f},{-eh_*.32:.0f}'
                        f' l{eh_*.16:.0f},{eh_*.32:.0f} l{-eh_*.08:.0f},0'
                        f' l{eh_*.20:.0f},{eh_*.32:.0f} l{-eh_*.10:.0f},0'
                        f' l{eh_*.26:.0f},{eh_*.36:.0f} Z" fill="#2f4a3a"'
                        f' stroke="{K}" stroke-width="4.5"/>')
    for i in range(6):
        s += SL(Z_SRED, varezhka(560 + i * 90, 1056 - ((i * 5) % 3) * 14, .7,
                                 -24 + i * 16, TKAN2, t, i * .2))
    s += SL(Z_SRED, inej_mel(467, 44, 980, 1070))
    s += SL(Z_LETIT, sneg_letit(t, 26, 127, .45, .6))
    s += ramka_pp("oba", "#0e0c0b", .5)
    s += vinetka(.42)
    return s


def vecherniy_stol_u_okna_na_prud(t):
    """Вечерний стол у окна на пруд: липовый чай с мёдом, калина в розетке,
    тёплая лампа. В проёме окна над столом — настоящий замёрзший пруд на
    закате; за столом хозяйка и хозяин, кот спит на лавке."""
    rnd = random.Random(3032)
    s = stena_gornicy_19(t, 61, 860, True, True)
    # ОКНО-ПРОЁМ над столом (сверху)
    px, py, pw, ph_ = 560, 140, 780, 320
    okno = (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_:.0f}"'
            f' fill="#c88a6a"/>')
    okno += (f'<rect x="{px:.0f}" y="{py:.0f}" width="{pw:.0f}" height="{ph_*.45:.0f}"'
             f' fill="#e0a07a"/>')
    okno += mesto_stoka(px, py, pw, ph_, "pryam")
    okno += (f'<rect x="{px-18:.0f}" y="{py-18:.0f}" width="{pw+36:.0f}"'
             f' height="{ph_+36:.0f}" rx="6" fill="none" stroke="#6b4428"'
             f' stroke-width="26"/>')
    okno += (f'<path d="M{px+pw*.5:.0f},{py:.0f} v{ph_:.0f} M{px:.0f},{py+ph_*.5:.0f}'
             f' h{pw:.0f}" stroke="#6b4428" stroke-width="16"/>')
    okno += (f'<rect x="{px-50:.0f}" y="{py+ph_+18:.0f}" width="{pw+100:.0f}"'
             f' height="32" rx="6" fill="{DOSKA}" stroke="{K}" stroke-width="5"/>')
    s += SL(Z_SRED, okno)
    s += SL(Z_SRED, teplo(px + pw * .5, py + ph_ * .5, 520, 420, .30))
    kch = 5 * A.w(t, 2.8, .3)
    for i in (0, 1):
        sdv = (-1 if i == 0 else 1) * 10
        s += SL(Z_SRED, f'<g transform="rotate({kch*(1 if i else -1):.1f}'
                        f' {px+i*(pw-160):.0f} {py-10:.0f})">'
                        f'<path d="M{px+i*(pw-160)+sdv:.0f},{py-16:.0f}'
                        f' q{80:.0f},{40:.0f} {80:.0f},{ph_*.88:.0f} q{-50:.0f},{20:.0f}'
                        f' {-120:.0f},{10:.0f} Z" fill="{RUSH}" opacity=".95"'
                        f' stroke="{K}" stroke-width="4.5"/></g>')
    # СТОЛ: чайник, мёд, калина в розетке, кружки
    s += SL(Z_SRED, stol(240, 780, 1200, 46, True))
    s += SL(Z_SRED, chaynik_s_parom(560, 780, 1.5, t, .1, True))
    s += SL(Z_SRED, banka_moloka(820, 780, .8, t, True, .78, "#d6a63f"))
    s += SL(Z_SRED, f'<ellipse cx="1020" cy="776" rx="92" ry="28" fill="#e8e2d6"'
                    f' stroke="{K}" stroke-width="4.5"/>'
                    f'<ellipse cx="1020" cy="766" rx="72" ry="20" fill="#8a2f22"'
                    f' stroke="#6b2419" stroke-width="3.4"/>')
    for i in range(6):
        a = i * 1.05
        s += SL(Z_SRED, f'<circle cx="{1020+46*math.cos(a):.0f}"'
                        f' cy="{764+12*math.sin(a):.0f}" r="11" fill="#c8301f"'
                        f' stroke="#7d1b11" stroke-width="2.6"/>')
    s += SL(Z_SRED, kruzhka_moloka(1220, 780, 1.0, t, False, .2, "#e8e2d6")
            + kruzhka_moloka(1380, 780, 1.0, t, False, .6, "#dce4ea"))
    s += SL(Z_SRED, karavay(340, 776, .9, True))
    # ХОЗЯЙКА и ХОЗЯИН за столом
    for i, (fx_, fy_, fh_, col, pl, bor) in enumerate(
            ((760, 1050, 660, "#4a3a52", True, False),
             (1300, 1056, 680, "#4a4038", False, True))):
        s += SL(Z_SRED, figura(fx_, fy_, fh_, t, col=col, kant="#ffd98a",
                               platok=pl, boroda=bor, ph=i * .4))
        rk, (ex, ey), _ = _ruka(fx_, fy_, fh_, 1, fh_ * .24, 44, t, col, "#ffd98a", i * .3, 3)
        rk2, (e2x_, e2y_), _ = _ruka(fx_, fy_, fh_, -1, fh_ * .24, 48, t, col,
                                     "#ffd98a", i * .3 + .4, 3)
        s += SL(Z_SRED, rk + rk2)
        s += SL(Z_SRED, ten(fx_, fy_ + 6, 128, 22, .45))
    # лавка с котом, печь, полка, ходики
    s += SL(Z_SRED, lavka(1580, 980, 320))
    s += SL(Z_SRED, kot(1700, 980, t, 1.6, "#3b3430", True))
    s += SL(Z_SRED, pech(60, 300, 300, 520, t, True, True, False))
    s += SL(Z_SRED, ogon(150, 700, t, 1.1, .2, 6) + teplo(150, 680, 300, 250, .45))
    s += SL(Z_SRED, polka_s_bankami(1480, 380, 400, t, 127, 4, False))
    s += SL(Z_SRED, hodiki(420, 260, t, 1.3))
    s += SL(Z_SRED, lampa(960, 540, t, 1.6, True) + teplo(960, 580, 460, 380, .5))
    s += SL(Z_PERED, ramka_pp("oba", "#0e0c0b", .5))
    s += vinetka(.44)
    return s
