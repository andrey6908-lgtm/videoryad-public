# -*- coding: utf-8 -*-
"""Декорации планов 132-157 ролика «Как встречать год хозяйки года 2027»."""
import math, random
from baza import *
import baza
import anim as A
import obrazy as ob
OKNO = (860, 300, 980, 551)


# ═══════════════════ ОБЩИЕ КИРПИЧИКИ ЭТОГО БЛОКА ═══════════════════
# Ссора и слёзы идут БЕЗ лиц и без жести: силуэт со спины, тень на стене,
# разделённый стол. Рук не рисуем — работает сам предмет.

def _grad(idd, c1, c2, vert=True):
    x2, y2 = (0, 1) if vert else (1, 0)
    return (f'<linearGradient id="{idd}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def _fon(idd, c1, c2):
    """Полнокадровая заливка с запасом под оверскан камеры."""
    return (_grad(idd, c1, c2)
            + f'<rect x="-440" y="-340" width="{W+880}" height="{H+680}" fill="url(#{idd})"/>')


def _oboi(y0, h_, col, shag=124, op=.14):
    """Обои полосой: без них стена читается пустой заливкой."""
    s = ""
    for i in range(int((W + 880) / shag) + 1):
        x = -440 + i * shag
        s += (f'<rect x="{x:.0f}" y="{y0}" width="{shag*.40:.0f}" height="{h_}"'
              f' fill="{col}" opacity="{op:.2f}"/>')
    return s


def _pol(y, idd="b7pol", c1="#8d6440", c2="#432a18"):
    s = _grad(idd, c1, c2)
    s += f'<rect x="-440" y="{y}" width="{W+880}" height="{H+680-y}" fill="url(#{idd})"/>'
    for i in range(9):
        yy = y + 22 + i * (H + 240 - y) / 8.0
        s += (f'<line x1="-440" y1="{yy:.0f}" x2="{W+440}" y2="{yy:.0f}"'
              f' stroke="#36210f" stroke-width="3" opacity=".42"/>')
    return s


def _plintus(y, h_=36, col="#d9cdb8"):
    return (f'<rect x="-440" y="{y-h_}" width="{W+880}" height="{h_}" rx="6"'
            f' fill="{col}" {o(5)}/>')


def _plitka(x, y, w_, h_, step, idd, c1="#e2edf4", c2="#b4cad9"):
    """Кафель: ряды со сдвигом, шов холодный."""
    s = _grad(idd, c1, c2)
    for r in range(int(h_ / step) + 1):
        for c in range(int(w_ / step) + 2):
            xx = x + c * step - (step * .5 if r % 2 else 0)
            s += (f'<rect x="{xx:.0f}" y="{y+r*step:.0f}" width="{step-7}" height="{step-7}"'
                  f' rx="7" fill="url(#{idd})" stroke="#9db5c6" stroke-width="3"/>')
    return s


def _tuchka(x, y, s_, t, ph=0.0, hmuraya=True, op=.95, col="#8e98a6"):
    """Серая тучка-обида: дышит, губы поджаты. ЛЮДЯМ лиц не рисуем — складка
    рта есть только у тучки, это знак настроения, а не лицо."""
    dy = 8 * s_ * A.w(t, 2.6, ph)
    g = f'<g transform="translate({x:.0f},{y+dy:.1f}) scale({s_:.3f})" opacity="{op:.2f}">'
    g += ten(0, 104, 126, 22, .40)
    g += (f'<path d="M-146,44 q-44,-70 20,-96 q2,-74 80,-68 q52,-46 108,8'
          f' q70,-12 76,64 q10,58 -50,58 z" fill="{col}" {o(7)}/>')
    g += ('<path d="M-112,6 q62,-32 124,-6" fill="none" stroke="#b7c1cd"'
          ' stroke-width="13" stroke-linecap="round" opacity=".65"/>')
    if hmuraya:
        g += f'<path d="M-62,2 q28,-24 56,-4" fill="none" {o(8)} opacity=".85"/>'
        g += f'<path d="M14,0 q26,-22 52,0" fill="none" {o(8)} opacity=".85"/>'
        g += f'<path d="M-34,62 q34,-20 68,0" fill="none" {o(9)}/>'
    g += '</g>'
    return g


def _shkaf_stvorka(x, y, w_, h_, idd, otkr=0.0):
    """Дверца шкафа: при otkr=0 стоит на месте, при 1 — закрыта до конца."""
    s = _grad(idd, "#8a6039", "#4a2e18")
    s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="10"'
          f' fill="url(#{idd})" {o(8)}/>')
    s += (f'<rect x="{x+34:.0f}" y="{y+44:.0f}" width="{w_-68:.0f}" height="{h_-88:.0f}"'
          f' rx="8" fill="none" stroke="#3a2210" stroke-width="7" opacity=".7"/>')
    s += (f'<ellipse cx="{x+30:.0f}" cy="{y+h_*.52:.0f}" rx="15" ry="26"'
          f' fill="url(#zol)" {o(4)}/>')
    s += (f'<rect x="{x-90:.0f}" y="{y:.0f}" width="92" height="{h_:.0f}"'
          f' fill="#120d09" opacity="{.42*otkr:.2f}"/>')
    return s


def _vesh(x, y, w_, h_, col, t, ph=0.0, cvetochek=False, amp=6.0):
    """Платье на плечиках: крючок, плечики, подол качается."""
    kach = amp * A.w(t, 3.1, ph)
    g = f'<g transform="rotate({kach*.5:.2f} {x:.0f} {y:.0f})">'
    g += (f'<path d="M{x:.0f},{y:.0f} q-16,-22 0,-34 q16,12 0,34" fill="none"'
          f' stroke="#9aa3ab" stroke-width="7"/>')
    g += (f'<path d="M{x-w_*.46:.0f},{y+34:.0f} L{x:.0f},{y+4:.0f} L{x+w_*.46:.0f},{y+34:.0f}"'
          f' fill="none" stroke="#6f5436" stroke-width="12" stroke-linecap="round"/>')
    sl_, sr_ = x - w_ * .26, x + w_ * .26
    sy_ = y + 42
    wl_, wr_ = x - w_ * .21, x + w_ * .21
    wy_ = y + 42 + h_ * .34
    hl_, hr_ = x - w_ * .56 - kach * .3, x + w_ * .56 + kach * .3
    hy_ = y + 42 + h_
    for sgn in (-1, 1):
        g += (f'<ellipse cx="{x + sgn*w_*.27:.0f}" cy="{sy_+22:.0f}" rx="{w_*.09:.0f}"'
              f' ry="{h_*.07:.0f}" fill="{col}" {o(5)}/>')
    g += (f'<path d="M{sl_:.0f},{sy_:.0f} Q{x:.0f},{y+16:.0f} {sr_:.0f},{sy_:.0f}'
          f' L{wr_:.0f},{wy_:.0f} Q{x+w_*.40:.0f},{y+42+h_*.72:.0f} {hr_:.1f},{hy_:.0f}'
          f' Q{x:.0f},{hy_+38:.0f} {hl_:.1f},{hy_:.0f}'
          f' Q{x-w_*.40:.0f},{y+42+h_*.72:.0f} {wl_:.0f},{wy_:.0f} Z"'
          f' fill="{col}" {o(7)}/>')
    g += (f'<path d="M{wl_:.0f},{wy_:.0f} Q{x:.0f},{wy_+20:.0f} {wr_:.0f},{wy_:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="9" opacity=".38"/>')
    g += (f'<path d="M{x-w_*.14:.0f},{sy_+16:.0f} Q{x:.0f},{wy_-10:.0f} {x+w_*.14:.0f},{sy_+16:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="7" opacity=".26"/>')
    if cvetochek:
        r = random.Random(int(x) % 97)
        for i in range(11):
            cx = x + r.uniform(-w_ * .40, w_ * .40)
            cy = y + 120 + r.uniform(0, h_ * .76)
            g += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r.uniform(7,11):.0f}"'
                  f' fill="{ob.ALYJ}" opacity=".55"/>')
    g += '</g>'
    return g


def _nozhnicy(x, y, t, s_=1.0, ug=0.0, razvod=1.0, bl=True):
    """Ножницы предметом: лезвия и кольца. Рук нет — они работают сами."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ug:.2f}) scale({s_:.3f})">'
    g += ten(10, 230, 70, 14, .35)
    for sgn in (-1, 1):
        a = sgn * 11 * razvod
        g += (f'<g transform="rotate({a:.2f} 0 60)">'
              f'<path d="M{sgn*13},50 L{sgn*31},-168 q{sgn*13},-20 {sgn*21},2'
              f' L{sgn*32},56 z" fill="url(#zhel)" {o(5)}/>'
              f'<path d="M{sgn*17},40 L{sgn*31},-150" fill="none" stroke="#eef5fb"'
              f' stroke-width="5" opacity="{.75 if bl else .3:.2f}"/>'
              f'<path d="M{sgn*16},70 q{sgn*44},70 {sgn*10},128" fill="none"'
              f' stroke="#4b5159" stroke-width="13"/>'
              f'<ellipse cx="{sgn*30}" cy="226" rx="50" ry="42" fill="none"'
              f' stroke="#4b5159" stroke-width="18"/></g>')
    g += f'<circle cx="0" cy="60" r="13" fill="url(#zol)" {o(4)}/>'
    g += '</g>'
    return g


def _konvert(x, y, s_, znak, t, ph=0.0):
    """Конверт со значком: монета, сердечко с градусником, домик с ключом."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.3f})">'
    g += ten(8, 86, 118, 18, .38)
    g += f'<rect x="-130" y="-78" width="260" height="160" rx="10" fill="url(#list)" {o(7)}/>'
    g += (f'<path d="M-130,-78 L0,20 L130,-78" fill="none" stroke="#b6a784"'
          f' stroke-width="7"/>')
    if znak == "moneta":
        g += f'<circle cx="0" cy="34" r="36" fill="url(#zol)" {o(5)}/>'
        g += '<circle cx="-11" cy="24" r="11" fill="#fff0bc" opacity=".7"/>'
    elif znak == "serdce":
        g += (f'<path d="M0,66 q-62,-42 -62,-82 q0,-34 32,-34 q22,0 30,26'
              f' q8,-26 30,-26 q32,0 32,34 q0,40 -62,82 z" fill="{ob.ALYJ}" {o(5)}/>')
        g += ('<path d="M44,6 v-56 q0,-16 16,-16 q16,0 16,16 v56" fill="#eef5fb"'
              f' {o(4)}/><circle cx="60" cy="18" r="17" fill="{ob.ALYJ}" {o(4)}/>')
    else:
        g += (f'<path d="M-60,66 v-58 L0,-40 L60,8 v58 z" fill="{MED}" {o(5)}/>')
        g += f'<path d="M-72,10 L0,-52 L72,10" fill="none" stroke="{UGOL}" stroke-width="12" stroke-linecap="round"/>'
        g += (f'<circle cx="56" cy="44" r="15" fill="none" stroke="url(#zol)" stroke-width="8"/>'
              f'<path d="M56,58 v26 M56,74 h16" fill="none" stroke="url(#zol)" stroke-width="8"/>')
    g += '</g>'
    return g


def _svecha_stola(x, y, t, s_=1.0, ph=0.0):
    return baza.svecha(x, y, t, ph, s_, 96)


# ═══════════════════ 133. ШВАБРА ОТДЫХАЕТ В УГЛУ ═══════════════════

def shvabra_otdyhaet_v_uglu(t):
    """Вечерний угол с сухой шваброй и ведром, справа двумя листками назад —
    день с распахнутым окном. Живое: мишура на швабре блестит, два листка
    отлетают вправо, дневная швабра ходит по полу."""
    POL = 792
    s = SL(Z_NEBO, _fon("b7a_f", "#36465f", "#1b2434"))

    d = _oboi(60, POL - 60, "#4c5e78", 130, .20)
    d += (f'<rect x="-440" y="-340" width="{1320}" height="{POL+340}"'
          f' fill="#0d1523" opacity=".32"/>')
    d += f'<line x1="880" y1="-40" x2="880" y2="{POL}" stroke="#0e1725" stroke-width="8" opacity=".55"/>'
    # ДЕНЬ справа — единственное тёплое пятно кадра
    d += ('<linearGradient id="b7a_den" x1="0" y1="0" x2="1" y2="0">'
          '<stop offset="0" stop-color="#e8f1ff" stop-opacity="0"/>'
          '<stop offset=".40" stop-color="#eef4ff" stop-opacity=".55"/>'
          '<stop offset="1" stop-color="#fff0cf" stop-opacity=".92"/></linearGradient>'
          f'<rect x="880" y="-340" width="{W+440-880}" height="{H+680}" fill="url(#b7a_den)"/>')
    # распахнутое окно дневной половины
    ox, oy, ow, oh = 1210, 190, 420, 400
    d += f'<rect x="{ox-22}" y="{oy-22}" width="{ow+44}" height="{oh+44}" rx="8" fill="url(#derev)" {o(7)}/>'
    d += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#dceeff"/>'
    d += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#fff6dd" opacity=".55"/>'
    for sgn, bx in ((-1, ox), (1, ox + ow)):
        d += (f'<g transform="translate({bx},{oy}) skewY({sgn*8})">'
              f'<rect x="{-100 if sgn<0 else 0}" y="0" width="100" height="{oh}"'
              f' fill="url(#stekl)" opacity=".8" {o(6)}/></g>')
    d += baza.luch(ox + 80, oy + oh, 260, POL - oy - oh + 180, t, .26)
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    m = _pol(POL, "b7a_p")
    m += (f'<rect x="880" y="{POL}" width="{W+440-880}" height="{H+680-POL}"'
          f' fill="#ffe9bd" opacity=".30"/>')
    # ВЕДРО — сухое, дужка вверх
    bx, by = 492, POL
    m += ten(bx, by + 8, 104, 20, .5)
    m += (f'<path d="M{bx-92},{by-176} h184 l-26,176 h-132 z" fill="url(#zhel)" {o(8)}/>')
    m += (f'<ellipse cx="{bx}" cy="{by-176}" rx="92" ry="26" fill="#2b323a" {o(6)}/>'
          f'<ellipse cx="{bx}" cy="{by-176}" rx="74" ry="18" fill="#1a1f25"/>')
    m += (f'<path d="M{bx-86},{by-186} q86,-150 172,0" fill="none" stroke="#565e68"'
          f' stroke-width="12" stroke-linecap="round"/>')
    m += f'<path d="M{bx-62},{by-150} l-18,140" fill="none" stroke="#eef5fb" stroke-width="10" opacity=".35"/>'
    # ШВАБРА отдыхает: ручка в угол, насадка сухая
    hx1, hy1, hx2, hy2 = 300, POL - 6, 196, 150
    m += ten(hx1, POL + 8, 112, 18, .45)
    m += (f'<path d="M{hx1},{hy1} L{hx2},{hy2}" fill="none" stroke="url(#derev)"'
          f' stroke-width="24" stroke-linecap="round"/>')
    m += (f'<path d="M{hx1-4},{hy1-6} L{hx2-4},{hy2+8}" fill="none" stroke="#c9a173"'
          f' stroke-width="7" opacity=".5"/>')
    m += (f'<g transform="rotate(-7 {hx1} {hy1})">'
          f'<rect x="{hx1-150}" y="{hy1-64}" width="300" height="62" rx="16"'
          f' fill="url(#dosk)" {o(7)}/>'
          f'<path d="M{hx1-134},{hy1-44} h268" stroke="#c9a173" stroke-width="9" opacity=".6"/>')
    for i in range(14):
        lx = hx1 - 136 + i * 21
        m += (f'<path d="M{lx},{hy1-6} q{4*A.w(t,6.0,i*.11):.1f},20 1,34" fill="none"'
              f' stroke="#d8cdb2" stroke-width="15" stroke-linecap="round"/>')
    m += '</g>'
    # БАНТИК ИЗ МИШУРЫ — блестит
    mx, my = int(hx2 + (hx1 - hx2) * .34), int(hy2 + (hy1 - hy2) * .34)
    for sgn in (-1, 1):
        m += (f'<path d="M{mx},{my} q{sgn*96},-86 {sgn*122},10 q{-sgn*46},62 {-sgn*122},-10 z"'
              f' fill="url(#zol)" {o(6)}/>')
        m += (f'<path d="M{mx},{my+8} q{sgn*40},54 {sgn*76},92" fill="none"'
              f' stroke="{ob.ZOLOTO2}" stroke-width="13" stroke-linecap="round"/>')
    m += f'<circle cx="{mx}" cy="{my}" r="26" fill="{ob.ZOLOTO}" {o(6)}/>'
    for i in range(13):
        a = i * .62
        gx = mx + math.cos(a) * (36 + 54 * (i % 3))
        gy = my + math.sin(a) * (28 + 38 * (i % 2))
        bl = .20 + .80 * abs(A.w(t, 1.1 + i * .17, i * .21))
        m += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="{7.5 + 2.5*(i%2):.1f}"'
              f' fill="#fff3c4" opacity="{bl:.2f}"/>')
    # ДНЕВНАЯ ШВАБРА — ходит по полу под окном
    sx = 1340 + 250 * A.w(t, 3.4)
    nak = -6 + 7 * A.w(t, 3.4)
    m += f'<g transform="translate({sx:.0f},0) rotate({nak:.1f} 0 {POL})">'
    m += (f'<path d="M0,{POL} L52,{POL-470}" fill="none" stroke="url(#derev)"'
          f' stroke-width="20" stroke-linecap="round"/>')
    m += (f'<rect x="-120" y="{POL-52}" width="240" height="52" rx="14" fill="url(#dosk)" {o(6)}/>')
    for i in range(11):
        m += (f'<path d="M{-108+i*21},{POL} v26" stroke="#d8cdb2" stroke-width="13"'
              f' stroke-linecap="round" opacity=".9"/>')
    m += (f'<ellipse cx="0" cy="{POL+16}" rx="150" ry="22" fill="#bfe0f2" opacity=".55"/>')
    m += '</g>'
    for i in range(4):
        gx = 1180 + i * 170 + 40 * A.w(t, 4.0, i * .3)
        m += (f'<ellipse cx="{gx:.0f}" cy="{POL+54+i*22}" rx="{70-i*8}" ry="12"'
              f' fill="#ffffff" opacity="{.18+.22*abs(A.w(t,2.4,i*.2)):.2f}"/>')
    s += SL(Z_SRED, m)

    # ДВА ЛИСТКА — отлетают назад, в день
    f = f'<rect x="620" y="268" width="210" height="36" rx="8" fill="url(#zhel)" {o(5)}/>'
    f += f'<rect x="636" y="304" width="178" height="214" rx="8" fill="url(#list)" {o(6)}/>'
    f += '<path d="M652,330 h146 M652,372 h146" stroke="#c3b694" stroke-width="5"/>'
    for i, t0 in enumerate((.45, 1.25)):
        p = A.out(A.seg(t, t0, 1.55))
        if p <= 0:
            continue
        lx = 726 + 560 * p
        ly = 400 - 150 * p + 240 * p * p
        f += (f'<g transform="translate({lx:.0f},{ly:.0f}) rotate({-16-54*p:.1f})"'
              f' opacity="{1-.45*p:.2f}">'
              f'<rect x="-88" y="-108" width="176" height="212" rx="8" fill="url(#list)" {o(6)}/>'
              f'<path d="M-66,-62 h132 M-66,-18 h132" stroke="#c7baa0" stroke-width="5"/></g>')
    s += SL(Z_LETIT, f)

    p = baza._ramka_pp("levo", "#0b0f18", .78)
    s += SL(Z_PERED, p)
    s += SL(Z_FIX, baza._vinetka(.40))
    return s


# ═══════════════════ 134. МЁРЗЛУЮ ПРОСТЫНЮ ВНОСЯТ В ДОМ ═══════════════════

def merzluyu_prostynyu_vnosyat_v_dom(t):
    """Мостик в память: дверь из сеней в клубах пара, простыня стоит листом
    у стены, девочка прижалась к ней. Живое: пар клубится в дверях, простыня
    медленно обмякает, девочка дышит в неё и жмурится плечами."""
    POL = 836
    s = SL(Z_NEBO, _fon("b7b_f", "#3a3a50", "#201d2a"))

    d = _oboi(40, POL - 40, "#4e4a63", 118, .18)
    d += baza.brevna(960, 60, 980, POL - 60, 96)
    # дверь из сеней: распахнута, оттуда холодный синий свет
    dx, dy, dw, dh = 110, 180, 330, POL - 180
    d += f'<rect x="{dx-26}" y="{dy-26}" width="{dw+52}" height="{dh+26}" rx="8" fill="url(#derev)" {o(8)}/>'
    d += f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#16233c"/>'
    d += ('<linearGradient id="b7b_seni" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#93bedd" stop-opacity=".85"/>'
          '<stop offset="1" stop-color="#2c3f5e" stop-opacity=".9"/></linearGradient>'
          f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="url(#b7b_seni)"/>')
    d += baza.dver(dx + dw - 40, dy, dw, dh, .72, "url(#derev)", True)
    d += (f'<path d="M{dx},{POL} l{dw},0 l180,220 l-{dw+360},0 z" fill="#bcd6ea"'
          f' opacity=".22"/>')
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    m = _pol(POL, "b7b_p", "#8a6038", "#3f2715")
    # ПРОСТЫНЯ стоит листом и медленно обмякает
    ob_ = A.ease(A.seg(t, .9, 3.4))
    px, py = 1240, POL
    volna = 26 * ob_
    m += ten(px, py + 10, 190, 26, .5)
    m += (f'<g transform="rotate({-6 + 9*ob_:.2f} {px} {py})">'
          f'<path d="M{px-150},{py} L{px-134+volna*.4:.0f},{py-620}'
          f' q150,{-34-volna:.0f} 290,{6:.0f} L{px+156},{py} z"'
          f' fill="url(#list)" {o(7)}/>')
    for i in range(4):
        wx = px - 112 + i * 76
        m += (f'<path d="M{wx},{py-584} q{10+volna*.6:.1f},200 {-6:.0f},576"'
              f' fill="none" stroke="#cfd8e4" stroke-width="7" opacity=".7"/>')
    m += (f'<path d="M{px-130},{py-560} q140,{-26-volna:.0f} 280,0" fill="none"'
          f' stroke="{TKAN2}" stroke-width="12" opacity=".75"/>')
    m += (f'<path d="M{px-122},{py-520} l60,300" fill="none" stroke="#ffffff"'
          f' stroke-width="18" opacity=".28"/></g>')
    # иней с простыни — холодное облачко
    for i in range(5):
        k = ((t * .4 + i * .2) % 1.0)
        m += (f'<ellipse cx="{px-200-60*k:.0f}" cy="{py-430-120*k:.0f}"'
              f' rx="{26+54*k:.0f}" ry="{(26+54*k)*.7:.0f}" fill="#d7e8f6"'
              f' opacity="{.34*(1-k):.2f}"/>')
    # МАТЬ: вошла из сеней, идёт к стене
    hod = A.ease(A.seg(t, .2, 2.4))
    m += ob.figura(430 + 320 * hod, POL + 10, 470, t, "#2c2436", "#f0c070", True, ph=.1)
    # ДЕВОЧКА нюхает простыню: вдох поднимает плечи, жмурится всем телом
    vdoh = .5 + .5 * A.w(t, 1.9, .2)
    m += (f'<g transform="translate(0,{-9*vdoh:.1f})">'
          + ob.figura(px - 196, POL + 10, 340 + 10 * vdoh, t, "#352a3e", "#f3cf90",
                      False, ph=.55, profil=True) + '</g>')
    s += SL(Z_SRED, m)

    f = baza.par(dx + dw * .5, POL - 150, t, 6, .62, 430, .34, 1.5)
    f += baza.par(dx + dw * .8, POL - 70, t, 5, .5, 330, .4, 1.2)
    f += baza._ramka_pp("levo", "#0a0d14", .62)
    s += SL(Z_PERED, f)

    fix = f'<rect width="{W}" height="{H}" fill="#c2884a" opacity=".13"/>'
    fix += baza._vinetka(.46)
    s += SL(Z_FIX, fix)
    return s


# ═══════════════════ 135. СТОПКА БЕЛЬЯ СО СКАТЕРТЬЮ ═══════════════════

def stopka_belya_so_skatertyu(t):
    """Полка шкафа крупно: ровная стопка с синей каймой, сверху накрахмаленная
    скатерть. Живое: свет проводит по скатерти вместо ладони, уголок хрустит
    и встаёт, дверца шкафа закрывается справа."""
    s = SL(Z_NEBO, _fon("b7c_f", "#4a331f", "#190f07"))

    d = baza.doski(-40, -60, W + 120, 980, 108, True, "dosk")
    d += f'<rect x="-440" y="-340" width="{W+880}" height="{H+680}" fill="#17100a" opacity=".42"/>'
    d += baza.teplo(520, 120, 760, 460, .50)
    d += (f'<rect x="-440" y="-340" width="{W+880}" height="420" fill="#0b0705" opacity=".55"/>')
    s += SL(Z_DAL, d)

    m = ""
    # ПОЛКА
    m += f'<rect x="-40" y="828" width="{W+200}" height="46" rx="10" fill="url(#derev)" {o(8)}/>'
    m += f'<rect x="-40" y="874" width="{W+200}" height="26" fill="#3f2713" opacity=".8"/>'
    m += ten(760, 836, 620, 30, .55)
    # СТОПКА БЕЛЬЯ с синей каймой
    r = random.Random(4)
    for i in range(7):
        yy = 824 - i * 56
        dx = r.uniform(-14, 14)
        m += (f'<rect x="{250+dx:.0f}" y="{yy-54:.0f}" width="1000" height="56" rx="14"'
              f' fill="url(#list)" {o(6)}/>')
        m += (f'<rect x="{250+dx:.0f}" y="{yy-22:.0f}" width="1000" height="22" rx="8"'
              f' fill="{TKAN2}" opacity=".95"/>')
        m += (f'<rect x="{250+dx:.0f}" y="{yy-30:.0f}" width="1000" height="7"'
              f' fill="#2c4260" opacity=".7"/>')
        m += (f'<path d="M{262+dx:.0f},{yy-42:.0f} h976" stroke="#ffffff"'
              f' stroke-width="7" opacity=".30"/>')
    # СКАТЕРТЬ сверху — накрахмаленная, уголок встаёт
    ug = A.over(A.seg(t, .8, 1.4)) * 52
    m += (f'<path d="M258,352 h988 q16,56 0,110 h-988 q-16,-54 0,-110 z"'
          f' fill="#f7efdc" {o(7)}/>')
    m += (f'<path d="M258,430 h988 q16,80 0,156 h-988 q-16,-78 0,-156 z"'
          f' fill="url(#krem)" {o(7)}/>')
    m += '<path d="M268,436 h968" stroke="#ffffff" stroke-width="9" opacity=".45"/>'
    m += ('<path d="M300,470 q460,-26 900,0" fill="none" stroke="#d7c49c" stroke-width="7"/>'
          '<path d="M300,548 q460,26 900,0" fill="none" stroke="#d7c49c" stroke-width="7"/>')
    for i in range(9):
        cx = 330 + i * 112
        m += (f'<path d="M{cx},500 q16,-22 32,0 q-16,22 -32,0 z" fill="{TKAN2}" opacity=".55"/>')
    m += (f'<g transform="rotate({-ug:.1f} 1246 586)">'
          f'<path d="M1246,586 l-176,-30 q-10,-66 6,-126 l170,0 z" fill="url(#krem)" {o(6)}/>'
          f'<path d="M1246,470 l-160,8" stroke="#ffffff" stroke-width="9" opacity=".4"/></g>')
    # СВЕТ ВМЕСТО ЛАДОНИ: полоса проходит по скатерти
    bx = 180 + ((t * 340) % 1500)
    m += (f'<g opacity=".55"><path d="M{bx:.0f},412 l150,0 l-104,180 l-150,0 z"'
          f' fill="#fff8e4" opacity=".55"/>'
          f'<path d="M{bx+54:.0f},412 l44,0 l-104,180 l-44,0 z" fill="#ffffff" opacity=".6"/></g>')
    s += SL(Z_SRED, m)

    zakr = A.ease(A.seg(t, 2.6, 2.6))
    f = _shkaf_stvorka(1920 - 760 * zakr, -200, 820, H + 420, "b7c_dv", zakr)
    f += baza._ramka_pp("levo", "#090705", .70)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.44))
    return s


# ═══════════════════ 136. УТЮГ И ГОТОВЫЙ НАРЯД ═══════════════════

def utyug_i_gotovyy_naryad(t):
    """Гладильная доска в полосе 0-830: утюг делает последний проход по
    скатерти и встаёт на подставку, рядом наряд на спинке стула. Живое:
    утюг идёт, пар валит, наряд покачивается."""
    POL = 940
    s = SL(Z_NEBO, _fon("b7d_f", "#3c4a60", "#232a38"))

    d = _oboi(30, POL - 30, "#4d5d76", 116, .16)
    d += baza.teplo(400, 240, 620, 420, .40)
    d += f'<rect x="60" y="150" width="300" height="22" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(3):
        d += (f'<rect x="{96+i*92}" y="60" width="72" height="90" rx="10"'
              f' fill="url(#list)" {o(5)}/>')
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    m = _pol(POL, "b7d_p", "#8f6744", "#412918")
    # ДОСКА
    bx0, bx1, by = 40, 700, 612
    m += ten(380, POL - 6, 290, 26, .5)
    m += (f'<path d="M{bx0},{by+8} q40,-54 120,-54 h{bx1-bx0-180} q90,0 90,56'
          f' q0,52 -90,52 h{-(bx1-bx0-180)} q-80,0 -120,-54 z" fill="url(#krem)" {o(8)}/>')
    m += (f'<path d="M{bx0+30},{by-14} h{bx1-bx0-120}" stroke="#ffffff" stroke-width="10" opacity=".35"/>')
    for sgn, nx in ((1, 170), (-1, 560)):
        m += (f'<path d="M{nx},{by+54} l{sgn*150},{POL-by-56}" fill="none"'
              f' stroke="#6d757e" stroke-width="18" stroke-linecap="round"/>')
        m += (f'<path d="M{nx+sgn*150},{by+54} l{-sgn*150},{POL-by-56}" fill="none"'
              f' stroke="#565d66" stroke-width="18" stroke-linecap="round"/>')
    # СКАТЕРТЬ на доске
    m += (f'<path d="M{bx0+20},{by-16} h{bx1-bx0-90} q24,96 -40,180 h-{bx1-bx0-240}'
          f' q-60,-80 -40,-180 z" fill="url(#list)" {o(6)}/>')
    m += (f'<path d="M{bx0+60},{by+36} q250,22 500,0" fill="none" stroke="{TKAN2}"'
          f' stroke-width="9" opacity=".7"/>')
    # УТЮГ: проход и посадка на подставку
    hod = A.ease(A.seg(t, .15, 3.0))
    stav = A.out(A.seg(t, 3.3, 1.3))
    ux = 130 + 360 * hod + 80 * stav
    uy = by - 42 - 30 * stav
    m += (f'<g transform="translate({ux:.0f},{uy:.0f})">'
          f'{ten(6, 60, 104, 16, .45)}'
          f'<path d="M-150,22 q86,-26 180,-14 q50,8 54,24 q4,16 -36,18 l-186,0 z"'
          f' fill="#cfd8e2" {o(7)}/>'
          f'<path d="M-146,16 q-10,-66 60,-84 q88,-20 150,22 q22,16 10,42 q-16,26 -220,20 z"'
          f' fill="url(#zhel)" {o(8)}/>'
          f'<path d="M-128,-14 q94,-54 190,-22" fill="none" stroke="#eef5fb" stroke-width="10" opacity=".6"/>'
          f'<path d="M-78,-88 q70,-26 132,8 q22,14 14,40 l-168,0 q-14,-28 22,-48 z"'
          f' fill="{CHUGUN}" {o(6)}/>'
          f'<path d="M-64,-98 q66,-24 124,10" fill="none" stroke="#9aa1a9" stroke-width="11"/>'
          f'<circle cx="80" cy="-18" r="15" fill="url(#zol)" {o(4)}/></g>')
    # ПОДСТАВКА
    m += (f'<rect x="488" y="{by-22}" width="160" height="26" rx="10" fill="#4a5159" {o(5)}/>')
    s += SL(Z_SRED, m)

    f = baza.par(ux - 60, uy - 20, t, 6, .52, 340, .42, 1.1)
    # СТУЛ с нарядом
    sx, sb = 700, POL + 10
    f += ten(sx, sb, 140, 24, .5)
    f += (f'<rect x="{sx-96}" y="{sb-320}" width="192" height="30" rx="10" fill="url(#derev)" {o(7)}/>')
    f += (f'<rect x="{sx-86}" y="{sb-700}" width="26" height="382" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="{sx+62}" y="{sb-700}" width="26" height="382" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="{sx-86}" y="{sb-700}" width="174" height="28" rx="10" fill="url(#derev)" {o(6)}/>')
    f += (f'<rect x="{sx-86}" y="{sb-290}" width="24" height="290" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{sx+62}" y="{sb-290}" width="24" height="290" fill="url(#derev)" {o(5)}/>')
    f += _vesh(sx, sb - 712, 250, 400, ob.ALYJ, t, .2, False, 9.0)
    f += baza._ramka_pp("levo", "#0a0e16", .62)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


# ═══════════════════ 137. ТИХАЯ ВАННАЯ ═══════════════════

def tihaya_vannaya(t):
    """Ванная по трём предметам: пустой неподвижный барабан с табличкой-
    мандарином, сложенная сушилка у стены, тряпка на краю ведра. Живое:
    блик ползёт по стеклу, сушилка складывается, тряпка качается."""
    POL = 880
    s = SL(Z_NEBO, _fon("b7e_f", "#30465a", "#1a2733"))

    d = _plitka(-440, -120, W + 880, POL + 140, 128, "b7e_pl")
    d += f'<rect x="-440" y="-340" width="{W+880}" height="{H+680}" fill="#16222e" opacity=".34"/>'
    d += baza.teplo(980, 60, 820, 420, .34)
    d += f'<rect x="700" y="150" width="520" height="22" rx="8" fill="#c7d6e2" {o(5)}/>'
    for i in range(4):
        d += (f'<rect x="{740+i*110}" y="74" width="54" height="76" rx="10"'
              f' fill="{["#9fc4d8","#e2d2b0","#c0d8c2","#dcc0c6"][i]}" {o(5)}/>')
    s += SL(Z_DAL, d)

    m = _plitka(-440, POL, W + 880, 360, 150, "b7e_pol", "#c9d8e4", "#8fa6b6")
    # СТИРАЛЬНАЯ МАШИНА — барабан пуст и неподвижен
    mx, my = 120, POL
    m += ten(mx + 230, my + 10, 250, 26, .5)
    m += (f'<rect x="{mx}" y="{my-520}" width="460" height="520" rx="22"'
          f' fill="url(#krem)" {o(8)}/>')
    m += (f'<rect x="{mx+24}" y="{my-492}" width="412" height="64" rx="12" fill="#cfd9e2" {o(5)}/>')
    for i in range(3):
        m += f'<circle cx="{mx+70+i*58}" cy="{my-460}" r="15" fill="#8d9aa6" {o(4)}/>'
    m += f'<circle cx="{mx+340}" cy="{my-460}" r="30" fill="url(#zhel)" {o(5)}/>'
    m += f'<circle cx="{mx+230}" cy="{my-250}" r="178" fill="#aab8c4" {o(8)}/>'
    m += f'<circle cx="{mx+230}" cy="{my-250}" r="146" fill="url(#stekl)" opacity=".92" {o(6)}/>'
    m += f'<circle cx="{mx+230}" cy="{my-250}" r="112" fill="#263241" opacity=".82"/>'
    for i in range(8):
        a = i * math.pi / 4
        m += (f'<circle cx="{mx+230+math.cos(a)*74:.0f}" cy="{my-250+math.sin(a)*74:.0f}"'
              f' r="13" fill="#15202c" opacity=".7"/>')
    bl = ((t * .28) % 1.0)
    m += (f'<g opacity=".8"><path d="M{mx+110+230*bl:.0f},{my-396} l76,0 l-120,292 l-76,0 z"'
          f' fill="#ffffff" opacity=".35"/></g>')
    m += (f'<path d="M{mx+120},{my-330} q70,-62 150,-48" fill="none" stroke="#ffffff"'
          f' stroke-width="13" opacity=".45"/>')
    # ТАБЛИЧКА-МАНДАРИН на дверце
    kach = 4 * A.w(t, 3.6)
    m += (f'<g transform="rotate({kach:.2f} {mx+398} {my-390})">'
          f'<path d="M{mx+398},{my-390} l-10,96" stroke="#b9452c" stroke-width="7"/>'
          + ob.mandarin(mx + 388, my - 258, .9, .0, t) + '</g>')
    # СУШИЛКА складывается
    sl = A.ease(A.seg(t, .8, 2.6))
    sx, sy = 880, POL
    ug = 17 - 13 * sl
    m += ten(sx + 60, sy + 8, 200, 22, .45)
    for sgn in (-1, 1):
        m += f'<g transform="rotate({sgn*ug:.1f} {sx+60} {sy-430})">'
        for rx0 in (sx - 56, sx + 176):
            m += (f'<rect x="{rx0}" y="{sy-430}" width="26" height="430" rx="10"'
                  f' fill="#aeb9c4" {o(6)}/>')
        for i in range(6):
            yy = sy - 400 + i * 66
            m += (f'<line x1="{sx-46}" y1="{yy}" x2="{sx+190}" y2="{yy}"'
                  f' stroke="#cdd8e0" stroke-width="11" stroke-linecap="round"/>')
        m += '</g>'
    # ВЕДРО с тряпкой
    vx, vy = 1480, POL
    m += ten(vx, vy + 8, 120, 22, .5)
    m += f'<path d="M{vx-108},{vy-250} h216 l-30,250 h-156 z" fill="url(#zhel)" {o(8)}/>'
    m += (f'<ellipse cx="{vx}" cy="{vy-250}" rx="108" ry="30" fill="#2c343c" {o(6)}/>'
          f'<ellipse cx="{vx}" cy="{vy-250}" rx="86" ry="21" fill="#18202a"/>')
    m += f'<path d="M{vx-78},{vy-200} l-16,186" stroke="#eef5fb" stroke-width="10" opacity=".3"/>'
    tr = 9 * A.w(t, 3.0, .3)
    m += (f'<g transform="rotate({tr:.2f} {vx+60} {vy-256})">'
          f'<path d="M{vx-50},{vy-278} q130,-44 200,-6 q10,70 -34,180'
          f' q-70,22 -128,-14 q-54,-78 -38,-160 z" fill="#d7e3ec" {o(6)}/>'
          f'<path d="M{vx-20},{vy-240} q80,30 150,8" fill="none" stroke="#9fb6c6" stroke-width="8"/></g>')
    s += SL(Z_SRED, m)

    f = baza._ramka_pp("oba", "#0b1118", .55)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.40))
    return s


# ═══════════════════ 138. КУХНЯ В РАЗГАР ГОТОВКИ ═══════════════════

def kuhnya_v_razgar_gotovki(t):
    """Кухня: все конфорки заняты, на столе миски, противень и скалка,
    хозяйка со спины пробует с ложки. Живое: крышки подпрыгивают, пар стоит
    столбом, ложка идёт ко рту. Рук нет — ложка едет сама."""
    POL = 930
    s = SL(Z_NEBO, _fon("b7f_f", "#2f3f55", "#1a2330"))

    d = _plitka(600, 120, 900, 480, 120, "b7f_pl", "#dfe9ef", "#b2c6d2")
    d += _oboi(30, POL - 30, "#45566d", 120, .14)
    d += baza.okno_izby(120, 180, 330, 300, t, None, .55, False, True)
    d += f'<rect x="620" y="150" width="560" height="22" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(5):
        d += baza.krynka(680 + i * 110, 146, .52)
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    m = _pol(POL, "b7f_p", "#8b6341", "#3e2614")
    # ПЛИТА с четырьмя занятыми конфорками
    px, py, pw = 560, POL, 700
    m += ten(px + pw / 2, py + 8, pw * .5, 26, .5)
    m += f'<rect x="{px}" y="{py-430}" width="{pw}" height="430" rx="16" fill="url(#chug)" {o(8)}/>'
    m += f'<rect x="{px+18}" y="{py-250}" width="{pw-36}" height="200" rx="12" fill="#1b1917" {o(5)}/>'
    m += (f'<rect x="{px+40}" y="{py-230}" width="{pw-80}" height="150" rx="10"'
          f' fill="{ORA}" opacity="{.28+.16*abs(A.w(t,1.4)):.2f}"/>')
    m += f'<rect x="{px-12}" y="{py-452}" width="{pw+24}" height="34" rx="10" fill="url(#zhel)" {o(6)}/>'
    for i in range(4):
        cx = px + 110 + (i % 2) * 300
        cy = py - 400 + (i // 2) * 86
        m += baza.ogon(cx, cy + 26, t, .36, i * .23, 3)
        # кастрюля, крышка подпрыгивает
        pod = max(0.0, A.w(t, .9 + i * .17, i * .3)) ** 2 * 22
        m += (f'<path d="M{cx-104},{cy-130} h208 l-18,128 h-172 z" fill="url(#zhel)" {o(7)}/>')
        m += (f'<path d="M{cx-118},{cy-134} h236" stroke="#3e444c" stroke-width="12" stroke-linecap="round"/>')
        m += (f'<g transform="translate(0,{-pod:.1f})">'
              f'<ellipse cx="{cx}" cy="{cy-142}" rx="112" ry="26" fill="#c2cad2" {o(6)}/>'
              f'<circle cx="{cx}" cy="{cy-162}" r="17" fill="#4e555d" {o(4)}/></g>')
        m += baza.par(cx, cy - 170, t, 4, .46, 240, .4 + i * .05, .9)
    s += SL(Z_SRED, m)

    # СТОЛ с мисками, противнем и скалкой
    f = ""
    sx, sy = -40, 700
    f += ten(260, POL - 4, 330, 26, .5)
    f += f'<rect x="{sx}" y="{sy}" width="560" height="38" rx="10" fill="url(#derev)" {o(8)}/>'
    f += f'<rect x="{sx+360}" y="{sy+38}" width="34" height="{POL-sy-38}" fill="url(#derev)" {o(6)}/>'
    for i, (bx, rx_) in enumerate(((110, 100), (320, 72))):
        f += (f'<path d="M{bx-rx_},{sy-16} q{rx_*.1:.0f},{rx_*1.25:.0f} {rx_:.0f},{rx_*1.3:.0f}'
              f' q{rx_*.9:.0f},{-rx_*.05:.0f} {rx_:.0f},{-rx_*1.3:.0f} z"'
              f' fill="url(#glina)" {o(7)}/>')
        f += (f'<ellipse cx="{bx}" cy="{sy-16}" rx="{rx_}" ry="{rx_*.34:.0f}"'
              f' fill="#efe3c8" {o(6)}/>')
        f += (f'<ellipse cx="{bx}" cy="{sy-16}" rx="{rx_*.76:.0f}" ry="{rx_*.24:.0f}"'
              f' fill="#d9c8a4"/>')
    f += (f'<rect x="{sx+400}" y="{sy-24}" width="170" height="30" rx="8" fill="url(#zhel)" {o(6)}/>')
    f += (f'<rect x="{sx+120}" y="{sy-54}" width="300" height="22" rx="11" fill="url(#derev)" {o(5)}/>'
          f'<circle cx="{sx+112}" cy="{sy-43}" r="18" fill="url(#derev)" {o(4)}/>'
          f'<circle cx="{sx+428}" cy="{sy-43}" r="18" fill="url(#derev)" {o(4)}/>')
    # ХОЗЯЙКА со спины + ЛОЖКА идёт ко рту
    hx, hb = 1480, POL + 150
    f += ob.figura(hx, hb, 640, t, "#2a2231", "#f2c477", True, ph=.3)
    f += (f'<path d="M{hx-116},{hb-470} q110,-34 220,6 l-6,170 q-110,30 -212,-4 z"'
          f' fill="url(#krem)" opacity=".85" {o(5)}/>')
    lo = A.ease(A.seg(t, .5, 1.6))
    lx = hx - 240 + 190 * lo
    ly = hb - 300 - 180 * lo
    f += (f'<g transform="translate({lx:.0f},{ly:.0f}) rotate({-28+22*lo:.1f})">'
          f'<rect x="-13" y="0" width="26" height="230" rx="13" fill="url(#zhel)" {o(6)}/>'
          f'<ellipse cx="0" cy="-22" rx="62" ry="44" fill="url(#zhel)" {o(7)}/>'
          f'<ellipse cx="0" cy="-26" rx="46" ry="30" fill="#f2f7fb" opacity=".8"/>'
          f'<ellipse cx="-14" cy="-34" rx="20" ry="12" fill="#ffffff" opacity=".7"/></g>')
    f += baza.par(lx, ly - 46, t, 3, .4, 130, .5, .6)
    f += baza._ramka_pp("levo", "#090d14", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


# ═══════════════════ 139-140. НОЖНИЦЫ НАД ПРЯДЬЮ ═══════════════════

def nozhnicy_nad_pryadyu(t):
    """Крупно затылок под накинутой простынёй, ножницы зависли над прядью и
    опускаются, не щёлкнув. Живое: ножницы висят и уходят вниз, прядь
    качается, простыня на плечах подрагивает. Лица нет — только затылок."""
    s = SL(Z_NEBO, _fon("b7g_f", "#303b52", "#171d2a"))

    d = _oboi(-40, 1100, "#44506b", 132, .16)
    d += baza.teplo(1600, 240, 560, 480, .46)
    d += (f'<rect x="1500" y="180" width="300" height="420" rx="18" fill="url(#stekl)"'
          f' opacity=".45" {o(7)}/>')
    d += f'<rect x="120" y="190" width="320" height="24" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(4):
        d += baza.krynka(180 + i * 86, 186, .4, "url(#krem)")
    s += SL(Z_DAL, d)

    # ЗАТЫЛОК и ПРОСТЫНЯ
    drozh = 4 * A.w(t, 2.3, .2)
    m = ten(760, 1050, 520, 44, .5)
    m += (f'<g transform="translate(0,{drozh:.1f})">'
          f'<path d="M210,1120 q20,-224 150,-286 q120,-58 380,-58 q260,0 380,58'
          f' q130,62 150,286 z" fill="url(#list)" {o(8)}/>')
    m += ('<path d="M300,1100 q40,-212 170,-272" fill="none" stroke="#ffffff"'
          ' stroke-width="18" opacity=".30"/>')
    m += (f'<path d="M360,834 q380,-96 760,0" fill="none" stroke="{TKAN2}"'
          f' stroke-width="14" opacity=".55"/>')
    m += (f'<path d="M560,790 q180,-44 360,0 q-30,54 -180,54 q-150,0 -180,-54 z"'
          f' fill="#dfe6ef" {o(6)}/>'
          f'<circle cx="740" cy="828" r="22" fill="url(#zol)" {o(4)}/></g>')
    # голова со спины
    m += (f'<g transform="translate(0,{drozh*.5:.1f})">'
          f'<circle cx="740" cy="520" r="266" fill="#2a2029" {o(9)}/>')
    r = random.Random(7)
    for i in range(16):
        a = -2.5 + i * .19
        x0 = 740 + math.cos(a) * 250
        y0 = 520 + math.sin(a) * 250
        m += (f'<path d="M{x0:.0f},{y0:.0f} q{r.uniform(-40,40):.0f},120'
              f' {r.uniform(-26,26):.0f},230" fill="none" stroke="#3a2d36"'
              f' stroke-width="18" stroke-linecap="round"/>')
    m += ('<path d="M600,330 q140,-70 280,10" fill="none" stroke="#5a4650"'
          ' stroke-width="22" opacity=".65"/>')
    m += (f'<path d="M520,620 q-30,180 20,330" fill="none" stroke="#2a2029"'
          f' stroke-width="56" stroke-linecap="round"/></g>')
    # ПРЯДЬ качается
    pr = 20 * A.w(t, 2.0, .1)
    m += (f'<path d="M966,380 q{104+pr:.1f},180 {56+pr*1.7:.1f},392" fill="none"'
          f' stroke="#4a3a44" stroke-width="62" stroke-linecap="round"/>')
    m += (f'<path d="M974,402 q{92+pr:.1f},168 {50+pr*1.6:.1f},356" fill="none"'
          f' stroke="#7d6672" stroke-width="18" stroke-linecap="round" opacity=".8"/>')
    m += (f'<path d="M1010,430 q{86+pr:.1f},158 {44+pr*1.5:.1f},330" fill="none"'
          f' stroke="#5b4953" stroke-width="22" stroke-linecap="round" opacity=".9"/>')
    s += SL(Z_SRED, m)

    # НОЖНИЦЫ: зависли и опустились, не щёлкнув
    vis = A.ease(A.seg(t, .4, 1.5))
    niz = A.out(A.seg(t, 2.6, 2.0))
    ny = 230 + 130 * vis + 210 * niz + 14 * A.w(t, 2.4)
    f = baza.teplo(1180, ny + 120, 260, 220, .35)
    f += _nozhnicy(1180, ny, t, 1.34, 10 + 5 * A.w(t, 3.2) - 12 * niz, 1.0 - .15 * niz)
    f += baza._ramka_pp("levo", "#080c13", .6)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.46))
    return s


# ═══════════════════ 141. МАМА В БИГУДИ ═══════════════════

def mama_v_bigudi(t):
    """Мостик в память: вечер у трюмо, мама со спины докручивает последние
    бигуди и повязывает косынку, в зеркале дочка повторяет на кукле. Живое:
    бигуди появляются одна за другой, косынка опускается, прядь куклы
    наматывается."""
    POL = 960
    s = SL(Z_NEBO, _fon("b7h_f", "#4a4463", "#262337"))

    d = _oboi(-20, POL + 20, "#5b5579", 112, .20)
    r = random.Random(12)
    for i in range(26):
        cx, cy = r.uniform(-60, W + 60), r.uniform(0, POL - 60)
        d += (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="{ob.ALYJ}" opacity=".22"/>'
              f'<circle cx="{cx+22:.0f}" cy="{cy+16:.0f}" r="7" fill="{ob.ZOLOTO}" opacity=".18"/>')
    d += baza.zanaveska(1880, -20, 980, 260, TKAN, t, -1)
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    # ТРЮМО с зеркалом
    m = _pol(POL, "b7h_p", "#86603e", "#3b2414")
    tx, ty = 170, 770
    m += ten(tx + 330, POL - 4, 340, 26, .5)
    m += f'<rect x="{tx}" y="{ty}" width="660" height="34" rx="10" fill="url(#derev)" {o(8)}/>'
    m += (f'<rect x="{tx+30}" y="{ty+34}" width="250" height="{POL-ty-34}" rx="8"'
          f' fill="url(#derev)" {o(6)}/>')
    for i in range(2):
        m += (f'<rect x="{tx+52}" y="{ty+66+i*76}" width="206" height="56" rx="8"'
              f' fill="#6d492a" {o(5)}/>'
              f'<circle cx="{tx+155}" cy="{ty+94+i*76}" r="12" fill="url(#zol)" {o(3)}/>')
    m += (f'<rect x="{tx+420}" y="{ty+34}" width="200" height="{POL-ty-34}" rx="8"'
          f' fill="url(#derev)" {o(6)}/>')
    # зеркало
    mx, my, mrx, mry = tx + 330, 430, 265, 320
    m += (f'<ellipse cx="{mx}" cy="{my}" rx="{mrx+28}" ry="{mry+28}" fill="url(#med)" {o(8)}/>')
    m += (f'<ellipse cx="{mx}" cy="{my}" rx="{mrx}" ry="{mry}" fill="#243049" {o(5)}/>')
    m += (f'<clipPath id="b7h_zerk"><ellipse cx="{mx}" cy="{my}" rx="{mrx}" ry="{mry}"/></clipPath>'
          f'<g clip-path="url(#b7h_zerk)">')
    m += (f'<rect x="{mx-mrx}" y="{my-mry}" width="{mrx*2}" height="{mry*2}" fill="#3b4663"/>')
    m += baza.teplo(mx - 60, my + 60, 300, 280, .5)
    # отражение: дочка с куклой
    m += ob.figura(mx - 92, my + 320, 380, t, "#2b2436", "#ffd79a", False, ph=.4, profil=True)
    kx, ky = mx + 96, my + 150
    m += (f'<ellipse cx="{kx}" cy="{ky}" rx="56" ry="74" fill="{KREM}" {o(5)}/>'
          f'<circle cx="{kx}" cy="{ky-96}" r="60" fill="{KREM}" {o(5)}/>')
    vit = (t * 150) % 360
    m += (f'<g transform="rotate({vit:.0f} {kx+34} {ky-96})">'
          f'<path d="M{kx+34},{ky-96} q46,-24 52,26 q-40,36 -62,-6" fill="none"'
          f' stroke="{MED}" stroke-width="14" stroke-linecap="round"/></g>')
    m += (f'<path d="M{kx-46},{ky-110} q46,-44 92,0" fill="none" stroke="{MED}"'
          f' stroke-width="16"/>')
    m += '</g>'
    m += (f'<path d="M{mx-mrx*.7:.0f},{my-mry*.6:.0f} l{mrx*.8:.0f},{mry*1.1:.0f}"'
          f' stroke="#ffffff" stroke-width="26" opacity=".14"/>')
    # лампа трюмо — тёплое пятно
    m += baza.lampa(tx + 616, 700, t, .72, True)
    for i in range(3):
        m += baza.krynka(tx + 470 + i * 56, ty - 6, .34, "url(#stekl)")
    s += SL(Z_SRED, m)

    # МАМА со спины: бигуди и косынка
    f = baza.teplo(1420, 540, 420, 520, .40)
    hx, hb = 1420, POL + 130
    f += ob.figura(hx, hb, 690, t, "#4b3f5f", "#ffd79a", False, ph=.15)
    gy = hb - 690 * .80
    for i in range(8):
        p = A.out(A.seg(t, .3 + i * .22, .6))
        if p <= 0:
            continue
        ryad = i // 4
        a = -2.35 + (i % 4) * .62
        rr = 96 - ryad * 44
        bx = hx + math.cos(a) * rr
        by = gy + math.sin(a) * rr + ryad * 26
        f += (f'<g transform="translate({bx:.0f},{by:.0f}) rotate({a*57.3+90:.0f}) scale({p:.2f})">'
              f'<rect x="-44" y="-26" width="88" height="52" rx="24" fill="{ob.ALYJ}" {o(6)}/>'
              f'<path d="M-30,-26 v52 M0,-26 v52 M30,-26 v52" stroke="#8d1b1c" stroke-width="6"/>'
              f'<ellipse cx="-14" cy="-12" rx="16" ry="7" fill="#f4a89c" opacity=".7"/></g>')
    kos = A.out(A.seg(t, 3.9, 1.9))
    if kos > 0:
        ky2 = gy - 320 + 320 * kos
        f += (f'<g transform="translate({hx:.0f},{ky2:.0f})" opacity="{min(1,kos*1.6):.2f}">'
              f'<path d="M-120,-10 q120,-128 240,0 q10,140 -120,196 q-130,-56 -120,-196 z"'
              f' fill="{ob.ZOLOTO}" {o(6)}/>')
        for i in range(7):
            f += (f'<circle cx="{-92+i*30}" cy="{30+((i*37)%52)}" r="9" fill="{ob.ALYJ}"'
                  f' opacity=".6"/>')
        f += (f'<path d="M-24,182 q{26*kos:.0f},34 {62*kos:.0f},10" fill="none"'
              f' stroke="{ob.ZOLOTO}" stroke-width="18" stroke-linecap="round"/></g>')
    f += baza._ramka_pp("levo", "#0a0a12", .52)
    s += SL(Z_PERED, f)

    fix = f'<rect width="{W}" height="{H}" fill="#c08a4a" opacity=".12"/>' + baza._vinetka(.44)
    s += SL(Z_FIX, fix)
    return s


# ═══════════════════ 142. ПАРИКМАХЕРСКАЯ ПЕРЕД ПРАЗДНИКОМ ═══════════════════

def parikmaherskaya_pered_prazdnikom(t):
    """Зал в полосе 0-830: три занятых кресла, дамы под колпаками-сушуарами с
    журналами, у двери очередь, на зеркале мишура. Живое: ножницы мастера
    мелькают, колпаки гудят светом, очередь листает журналы."""
    POL = 900
    s = SL(Z_NEBO, _fon("b7i_f", "#45506a", "#232a3a"))

    d = _oboi(20, POL - 20, "#525f7c", 110, .16)
    # зеркальная стена
    for i in range(3):
        zx = 40 + i * 268
        d += (f'<rect x="{zx}" y="150" width="226" height="330" rx="12" fill="url(#med)" {o(6)}/>'
              f'<rect x="{zx+16}" y="166" width="194" height="298" rx="8" fill="#5a6c88"'
              f' opacity=".9" {o(4)}/>'
              f'<path d="M{zx+36},{430} l120,-230" stroke="#ffffff" stroke-width="20" opacity=".17"/>')
    # мишура по верху зеркал
    for i in range(16):
        gx = 50 + i * 50
        gy = 136 + 18 * math.sin(i * .9)
        bl = .35 + .65 * abs(A.w(t, 1.4 + (i % 4) * .3, i * .13))
        d += (f'<circle cx="{gx}" cy="{gy:.0f}" r="17" fill="{[ob.ZOLOTO, ob.ALYJ][i%2]}"'
              f' opacity="{bl:.2f}"/>')
        d += (f'<circle cx="{gx}" cy="{gy:.0f}" r="30" fill="{ob.ZOLOTO}"'
              f' opacity="{bl*.2:.2f}"/>')
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    m = _pol(POL, "b7i_p", "#7e7367", "#3b352d")
    # ТРИ КРЕСЛА с колпаками-сушуарами
    for i, (cx, sc, ph) in enumerate(((150, 1.0, 0.0), (420, .88, .3), (660, .76, .6))):
        base = POL - 30 + 30 * (1 - sc)
        m += f'<g transform="translate({cx},{base}) scale({sc:.2f})">'
        m += ten(0, 10, 130, 22, .5)
        m += f'<rect x="-26" y="-180" width="52" height="180" rx="12" fill="#4b525b" {o(6)}/>'
        m += f'<ellipse cx="0" cy="0" rx="124" ry="26" fill="#3d444c" {o(5)}/>'
        m += f'<rect x="-116" y="-300" width="232" height="130" rx="22" fill="{TKAN}" {o(7)}/>'
        m += f'<rect x="-104" y="-560" width="208" height="270" rx="26" fill="{TKAN}" {o(7)}/>'
        m += (f'<path d="M-86,-540 q86,-30 172,0" fill="none" stroke="#e0756c"'
              f' stroke-width="12" opacity=".5"/>')
        # дама силуэтом со спины
        m += (f'<path d="M-82,-300 q-6,-180 82,-214 q88,34 82,214 z" fill="#4c4059"'
              f' stroke="#f0c070" stroke-width="4" stroke-opacity=".6"/>')
        m += (f'<circle cx="0" cy="-566" r="82" fill="#5e5073" stroke="#ffd79a"'
              f' stroke-width="5" stroke-opacity=".75"/>')
        # колпак-сушуар накрывает голову
        gor = .45 + .55 * abs(A.w(t, 1.7 + i * .4, i * .2))
        m += baza.teplo(0, -570, 210, 160, gor * .8)
        m += (f'<path d="M-128,-666 q128,-236 256,0 q-28,42 -128,42 q-100,0 -128,-42 z"'
              f' fill="#cfd8e2" {o(7)}/>')
        m += (f'<path d="M-104,-674 q104,-188 208,0 q-24,30 -104,30 q-80,0 -104,-30 z"'
              f' fill="{SVET}" opacity="{gor*.6:.2f}"/>')
        m += (f'<path d="M-90,-704 q90,-132 180,0" fill="none" stroke="#ffffff"'
              f' stroke-width="10" opacity="{gor*.5:.2f}"/>')
        m += f'<rect x="-18" y="-900" width="36" height="240" rx="10" fill="#8f98a3" {o(5)}/>'
        # журнал в руках не рисуем — журнал сам лежит на коленях и листается
        lst = ((t * .8 + i * .33) % 1.0)
        m += (f'<g transform="translate(60,-300)">'
              f'<rect x="-70" y="-30" width="140" height="100" rx="8" fill="url(#list)" {o(5)}/>'
              f'<g transform="translate(0,-30) scale({max(.05,1-2*abs(lst-.5)):.2f},1)">'
              f'<rect x="-66" y="0" width="132" height="96" rx="8" fill="#efe9d8" {o(4)}/></g></g>')
        m += '</g>'
    # НОЖНИЦЫ мастера мелькают у первого кресла
    mel = .55 + .45 * abs(A.w(t, .55))
    m += (f'<g opacity="{mel:.2f}">'
          + _nozhnicy(310, 330 + 26 * A.w(t, 1.1), t, .72, -48 + 30 * A.w(t, .55), .8)
          + '</g>')
    s += SL(Z_SRED, m)

    # ОЧЕРЕДЬ у двери — передний план
    f = ""
    for i, (qx, sc) in enumerate(((640, 1.0), (776, .94))):
        qb = POL + 110 - 20 * i
        f += f'<g transform="translate({qx},{qb}) scale({sc:.2f})">'
        f += ten(0, 8, 96, 18, .45)
        f += f'<rect x="-84" y="-40" width="168" height="34" rx="10" fill="url(#derev)" {o(6)}/>'
        f += (f'<rect x="-74" y="-6" width="22" height="90" fill="url(#derev)" {o(4)}/>'
              f'<rect x="52" y="-6" width="22" height="90" fill="url(#derev)" {o(4)}/>')
        f += (f'<path d="M-78,-44 q-8,-220 78,-252 q86,32 78,252 z" fill="#3a3148"'
              f' stroke="#e8b06a" stroke-width="4" stroke-opacity=".55"/>')
        f += (f'<circle cx="0" cy="-330" r="74" fill="#3a3148" stroke="#e8b06a"'
              f' stroke-width="4" stroke-opacity=".55"/>')
        lst = ((t * .7 + i * .5) % 1.0)
        f += (f'<g transform="translate(0,-170)">'
              f'<rect x="-82" y="-40" width="164" height="118" rx="8" fill="url(#list)" {o(5)}/>'
              f'<g transform="translate(0,-40) scale({max(.05,1-2*abs(lst-.5)):.2f},1)">'
              f'<rect x="-78" y="0" width="156" height="114" rx="8" fill="#f2ecdb" {o(4)}/></g></g>')
        f += '</g>'
    f += baza._ramka_pp("levo", "#090c14", .55)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.36))
    return s


# ═══════════════════ 143. ВНУК С ДЛИННОЙ ЧЁЛКОЙ ═══════════════════

def vnuk_s_dlinnoy_chelkoy(t):
    """Мальчик на стуле сдувает чёлку, бабушка убирает ножницы в карман
    фартука и закалывает чёлку заколкой. Живое: чёлка взлетает от выдоха,
    ножницы уходят в карман, заколка защёлкивается. Лиц нет — профиль."""
    POL = 940
    s = SL(Z_NEBO, _fon("b7j_f", "#3a4259", "#1f2531"))

    d = _oboi(10, POL - 10, "#4a556f", 122, .16)
    d += (f'<rect x="1100" y="150" width="620" height="420" rx="12" fill="{TKAN}" opacity=".8" {o(6)}/>')
    for i in range(4):
        d += (f'<path d="M1130,{200+i*98} q290,52 580,0" fill="none" stroke="{ob.ZOLOTO}"'
              f' stroke-width="8" opacity=".6"/>')
    d += baza.okno_izby(170, 170, 330, 290, t, None, .4, True, True)
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    # СТУЛ и МАЛЬЧИК в профиль
    m = _pol(POL, "b7j_p", "#8a6340", "#3d2616")
    sx, sb = 700, POL + 20
    m += ten(sx, sb, 140, 24, .5)
    m += f'<rect x="{sx-100}" y="{sb-270}" width="200" height="32" rx="10" fill="url(#derev)" {o(7)}/>'
    m += (f'<rect x="{sx-92}" y="{sb-240}" width="24" height="240" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{sx+68}" y="{sb-240}" width="24" height="240" fill="url(#derev)" {o(5)}/>')
    m += (f'<rect x="{sx+72}" y="{sb-620}" width="26" height="370" rx="10" fill="url(#derev)" {o(6)}/>'
          f'<rect x="{sx-20}" y="{sb-636}" width="120" height="26" rx="10" fill="url(#derev)" {o(5)}/>')
    # тело и голова в профиль
    m += (f'<path d="M{sx-96},{sb-272} q-10,-200 96,-228 q104,28 94,228 z"'
          f' fill="#2b2434" stroke="#f0c070" stroke-width="4" stroke-opacity=".7"/>')
    hy = sb - 580
    m += (f'<circle cx="{sx+16}" cy="{hy}" r="92" fill="#2b2434" stroke="#f0c070"'
          f' stroke-width="4" stroke-opacity=".7"/>')
    m += (f'<path d="M{sx-66},{hy-24} q70,-96 164,-30" fill="none" stroke="#3b3042"'
          f' stroke-width="34" stroke-linecap="round"/>')
    # ЧЁЛКА: мальчик её сдувает
    sdv = max(0.0, A.w(t, 1.5)) ** 3
    for i in range(6):
        cx0 = sx - 14 + i * 24
        m += (f'<path d="M{cx0},{hy-84} q{30+66*sdv:.0f},{104-56*sdv:.0f}'
              f' {16+96*sdv:.0f},{192-92*sdv:.0f}" fill="none" stroke="#453750"'
              f' stroke-width="26" stroke-linecap="round"/>')
        m += (f'<path d="M{cx0+8},{hy-78} q{28+62*sdv:.0f},{96-52*sdv:.0f}'
              f' {14+90*sdv:.0f},{178-86*sdv:.0f}" fill="none" stroke="#7a6684"'
              f' stroke-width="7" stroke-linecap="round" opacity=".55"/>')
    for i in range(3):
        k = ((t * 1.1 + i * .33) % 1.0)
        m += (f'<ellipse cx="{sx+112+70*k:.0f}" cy="{hy+28-22*k:.0f}" rx="{10+30*k:.0f}"'
              f' ry="{(10+30*k)*.5:.0f}" fill="#dbe7f2" opacity="{.3*(1-k)*sdv:.2f}"/>')
    # ЗАКОЛКА защёлкивается
    zp = A.over(A.seg(t, 2.5, 1.0))
    if zp > .02:
        m += (f'<g transform="translate({sx-18},{hy-84}) rotate({-18+10*zp:.1f}) scale({zp:.2f})">'
              f'<rect x="-52" y="-13" width="104" height="26" rx="13" fill="url(#zol)" {o(5)}/>'
              f'<path d="M-40,0 h80" stroke="#8a6414" stroke-width="7"/>'
              f'<circle cx="46" cy="0" r="12" fill="#fff3c4" opacity=".8"/></g>')
    s += SL(Z_SRED, m)

    # БАБУШКА с фартуком, ножницы уходят в карман
    f = ""
    bx, bb = 1500, POL + 170
    f += ob.figura(bx, bb, 700, t, "#2a2231", "#f2c477", True, ph=.4)
    f += (f'<path d="M{bx-130},{bb-500} q130,-40 258,6 l-10,266 q-124,34 -240,-6 z"'
          f' fill="url(#krem)" opacity=".9" {o(6)}/>')
    f += (f'<rect x="{bx-74}" y="{bb-370}" width="152" height="112" rx="12"'
          f' fill="#ded0b2" {o(6)}/>')
    kar = A.ease(A.seg(t, 1.0, 1.5))
    nx = bx - 240 + 244 * kar
    ny = bb - 560 + 142 * kar
    f += (f'<g opacity="{1-.15*kar:.2f}">'
          + _nozhnicy(nx, ny, t, .62 - .1 * kar, -24 + 30 * kar, .5) + '</g>')
    f += (f'<rect x="{bx-74}" y="{bb-370}" width="152" height="60" rx="12"'
          f' fill="#cfbf9c" {o(5)}/>')
    f += baza._ramka_pp("levo", "#090c13", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


# ═══════════════════ 144. СЛЕЗА НАД ПРАЗДНИЧНОЙ ТАРЕЛКОЙ ═══════════════════

def sleza_nad_prazdnichnoy_tarelkoy(t):
    """Крупно пустая праздничная тарелка, на её край падает одна слеза, рядом
    хлеб, разломленный пополам. Живое: слеза падает и расходится кругом,
    огонёк свечи вздрагивает, половинки хлеба расходятся. Без лиц."""
    s = SL(Z_NEBO, _fon("b7k_f", "#2b3146", "#14161f"))

    d = f'<rect x="-440" y="-340" width="{W+880}" height="620" fill="#10131c" opacity=".7"/>'
    d += baza.teplo(1560, 340, 540, 430, .42)
    rg = random.Random(31)
    d += (f'<path d="M1300,470 q190,-130 420,-90 q-150,70 -420,90 z" fill="{ob.HVOYA2}"'
          f' opacity=".85" {o(5)}/>')
    for i in range(14):
        gx = 1310 + rg.uniform(0, 420)
        gy = 300 + rg.uniform(0, 170)
        gor = .3 + .7 * abs(A.w(t, 1.6 + rg.uniform(0, 1.4), i * .17))
        d += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="13" fill="{[SVET, ob.ALYJ, ob.ZOLOTO][i%3]}"'
              f' opacity="{gor:.2f}"/>')
        d += (f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="30" fill="{SVET}"'
              f' opacity="{gor*.16:.2f}"/>')
    d += (f'<path d="M-440,470 q560,-46 1160,-10 q520,30 1200,-16 L{W+440},620 L-440,620 z"'
          f' fill="url(#rush)" {o(7)}/>')
    d += (f'<path d="M-440,540 q600,40 1200,6 q500,-30 1160,8" fill="none"'
          f' stroke="{ob.ALYJ}" stroke-width="9" opacity=".6"/>')
    d += _svecha_stola(1700, 300, t, 1.5, .2)
    s += SL(Z_DAL, d)

    m = (f'<rect x="-440" y="560" width="{W+880}" height="{H+340}" fill="url(#rush)"/>')
    for i in range(5):
        m += (f'<path d="M-440,{640+i*120} q620,34 1240,0 q480,-26 1120,14" fill="none"'
              f' stroke="#d9c79f" stroke-width="5" opacity=".5"/>')
    # ТАРЕЛКА крупно
    px, py = 720, 790
    m += ten(px, py + 130, 460, 54, .55)
    m += f'<ellipse cx="{px}" cy="{py}" rx="470" ry="186" fill="url(#krem)" {o(9)}/>'
    m += f'<ellipse cx="{px}" cy="{py+12}" rx="470" ry="186" fill="#c8b894" opacity=".45"/>'
    m += f'<ellipse cx="{px}" cy="{py-10}" rx="468" ry="184" fill="url(#krem)" {o(8)}/>'
    m += (f'<ellipse cx="{px}" cy="{py-10}" rx="368" ry="140" fill="none"'
          f' stroke="url(#zol)" stroke-width="12"/>')
    m += (f'<ellipse cx="{px}" cy="{py-10}" rx="250" ry="92" fill="#efe6cd" {o(5)}/>')
    m += (f'<path d="M{px-370},{py-60} q130,-78 300,-72" fill="none" stroke="#ffffff"'
          f' stroke-width="22" opacity=".45"/>')
    # ХЛЕБ разломлен пополам — половинки расходятся
    razh = 34 * A.ease(A.seg(t, .25, 1.6))
    for sgn in (-1, 1):
        hx = 1480 + sgn * (70 + razh)
        m += ten(hx, 965, 130, 24, .45)
        m += (f'<g transform="translate({hx:.0f},880) rotate({sgn*5:.0f})">'
              f'<path d="M{-sgn*6},78 q-110,-10 -118,-86 q-6,-80 110,-92 l{sgn*14},0'
              f' q10,94 0,178 z" fill="url(#med)" {o(7)}/>'
              f'<path d="M{-sgn*10},-96 q-80,10 -96,76" fill="none" stroke="#f0cf90"'
              f' stroke-width="12" opacity=".6"/>'
              f'<path d="M{-sgn*2},-98 q{sgn*16},92 0,178" fill="none" stroke="{KREM}"'
              f' stroke-width="16"/></g>')
    s += SL(Z_SRED, m)

    # СЛЕЗА падает на край тарелки
    k = ((t + .2) % 1.9) / 1.9
    f = ""
    if k < .62:
        u = k / .62
        ty = 230 + (py - 150 - 230) * (u * u)
        f += (f'<g transform="translate(400,{ty:.0f})">'
              f'{baza.teplo(0, 50, 110, 110, .3)}'
              f'<path d="M0,-78 q56,66 56,116 q0,56 -56,56 q-56,0 -56,-56 q0,-50 56,-116 z"'
              f' fill="#cfe6f6" opacity=".92" {o(5)}/>'
              f'<ellipse cx="-18" cy="76" rx="15" ry="24" fill="#ffffff" opacity=".85"/></g>')
    else:
        u = (k - .62) / .38
        f += (f'<ellipse cx="400" cy="{py-84}" rx="{50+190*u:.0f}" ry="{16+58*u:.0f}"'
              f' fill="none" stroke="#dcefff" stroke-width="{14*(1-u):.1f}"'
              f' opacity="{(1-u)*.9:.2f}"/>')
        f += (f'<ellipse cx="400" cy="{py-84}" rx="{18+70*u:.0f}" ry="{6+22*u:.0f}"'
              f' fill="#dcefff" opacity="{(1-u)*.35:.2f}"/>')
    f += baza._ramka_pp("levo", "#070910", .5)
    s += SL(Z_LETIT, f)
    s += SL(Z_FIX, baza._vinetka(.50))
    return s


# ═══════════════════ 145. ССОРА ТЯНЕТСЯ ЧЕРЕЗ ГОД ═══════════════════

def ssora_tyanetsya_cherez_god(t):
    """От тарелки со слезой ползёт серая дорожка: за ней ковыляют градусник с
    грелкой и унылая тучка, а трещина от разломленного хлеба бежит через
    двенадцать плиток-месяцев. Живое: дорожка ползёт, предметы ковыляют,
    трещина бежит."""
    s = SL(Z_NEBO, _fon("b7l_f", "#333d54", "#171c27"))

    # ДВЕНАДЦАТЬ ПЛИТОК-МЕСЯЦЕВ
    d = ""
    for i in range(12):
        px = 44 + i * 153
        d += ten(px + 66, 842, 72, 16, .4)
        d += (f'<rect x="{px}" y="650" width="134" height="190" rx="14"'
              f' fill="url(#krem)" {o(6)}/>')
        d += (f'<rect x="{px+10}" y="660" width="114" height="34" rx="8"'
              f' fill="{ob.ALYJ if i in (0, 11) else "#c3b595"}" opacity=".8"/>')
        for r_ in range(3):
            d += (f'<path d="M{px+18},{714+r_*34} h98" stroke="#c6b794"'
                  f' stroke-width="6" opacity=".7"/>')
    d += baza.teplo(140, 330, 420, 360, .34)
    s += SL(Z_DAL, d)

    # ТАРЕЛКА СО СЛЕЗОЙ и СЕРАЯ ДОРОЖКА
    m = ""
    m += ten(210, 520, 190, 28, .5)
    m += f'<ellipse cx="200" cy="470" rx="196" ry="74" fill="url(#krem)" {o(7)}/>'
    m += (f'<ellipse cx="200" cy="462" rx="146" ry="54" fill="none" stroke="url(#zol)"'
          f' stroke-width="9"/>')
    kap = ((t * .7) % 1.0)
    m += (f'<ellipse cx="268" cy="{400+70*kap:.0f}" rx="13" ry="19" fill="#cfe6f6"'
          f' opacity="{1-kap:.2f}"/>')
    hod = (t * 46) % 72
    m += (f'<path d="M300,492 q320,70 640,22 q360,-52 700,40 q180,54 300,10"'
          f' fill="none" stroke="#7c8694" stroke-width="56" stroke-linecap="round"'
          f' opacity=".75"/>')
    m += (f'<path d="M300,492 q320,70 640,22 q360,-52 700,40 q180,54 300,10"'
          f' fill="none" stroke="#9aa5b2" stroke-width="16" stroke-dasharray="46 26"'
          f' stroke-dashoffset="{-hod:.0f}" stroke-linecap="round" opacity=".9"/>')
    # ГРАДУСНИК и ГРЕЛКА ковыляют по дорожке
    sh = (t * 78) % 1560
    gx = 600 + sh
    kov = 18 * abs(A.w(t, .62))
    m += (f'<g transform="translate({gx:.0f},{470-kov:.1f}) rotate({9*A.w(t,.62):.1f})">'
          f'{ten(0, 112, 54, 13, .4)}'
          f'<rect x="-22" y="-150" width="44" height="236" rx="22" fill="url(#stekl)" {o(6)}/>'
          f'<rect x="-9" y="-120" width="18" height="186" rx="9" fill="{ob.ALYJ}"/>'
          f'<circle cx="0" cy="96" r="34" fill="{ob.ALYJ}" {o(5)}/>'
          f'<path d="M-22,-110 h14 M-22,-74 h14 M-22,-38 h14" stroke="{K}" stroke-width="5"/></g>')
    gx2 = 470 + sh
    kov2 = 16 * abs(A.w(t, .62, .35))
    m += (f'<g transform="translate({gx2:.0f},{486-kov2:.1f}) rotate({-8*A.w(t,.62,.35):.1f})">'
          f'{ten(0, 104, 76, 15, .4)}'
          f'<path d="M-82,80 q-26,-130 20,-168 q-30,-44 18,-56 q62,-12 70,40'
          f' q56,46 32,184 q-70,26 -140,0 z" fill="#b8564c" {o(7)}/>'
          f'<path d="M-40,-96 q34,-18 66,0" fill="none" stroke="#e08b80" stroke-width="12"/>'
          f'<path d="M-50,20 q56,22 112,-6" fill="none" stroke="#8d2f28" stroke-width="9"/></g>')
    s += SL(Z_SRED, m)

    # УНЫЛАЯ ТУЧКА позади них и ТРЕЩИНА по плиткам
    f = _tuchka(370 + sh * .92, 290, .86, t, .2)
    for i in range(4):
        dq = ((t * .6 + i * .25) % 1.0)
        f += (f'<line x1="{370+sh*.92-60+i*42:.0f}" y1="{366+120*dq:.0f}"'
              f' x2="{370+sh*.92-74+i*42:.0f}" y2="{400+120*dq:.0f}"'
              f' stroke="#9fc0d8" stroke-width="7" stroke-linecap="round"'
              f' opacity="{(1-dq)*.75:.2f}"/>')
    tre = A.ease(A.seg(t, 3.4, 4.2))
    pts = []
    for i in range(25):
        u = i / 24.0
        pts.append((44 + u * 1836, 744 + 34 * math.sin(u * 13.0) + (18 if i % 2 else -18)))
    dd = "M%.0f,%.0f " % pts[0] + " ".join("L%.0f,%.0f" % p for p in pts[1:])
    f += (f'<path d="{dd}" fill="none" stroke="#2a1f1a" stroke-width="13"'
          f' stroke-linecap="round" stroke-dasharray="2000"'
          f' stroke-dashoffset="{2000*(1-tre):.0f}" opacity=".9"/>')
    f += (f'<path d="{dd}" fill="none" stroke="#6d5b4a" stroke-width="5"'
          f' stroke-dasharray="2000" stroke-dashoffset="{2000*(1-tre):.0f}" opacity=".8"/>')
    f += baza._ramka_pp("levo", "#090c13", .45)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.42))
    return s


# ═══════════════════ 147. ОБИДА САДИТСЯ ЗА СТОЛ ═══════════════════

def obida_saditsya_za_stol(t):
    """Праздничный стол: на свободный стул рядом с хмурым человеком взбирается
    надутая серая тучка, придвигает тарелку и заправляет салфетку. Живое:
    тучка взбирается, тарелка едет, салфетка встаёт. Человек — силуэт со
    спины, лица нет."""
    POL = 1000
    s = SL(Z_NEBO, _fon("b7m_f", "#36405c", "#1d2330"))

    d = _oboi(0, POL, "#47536f", 126, .15)
    d += ob.elka(1620, 880, 520, t)
    d += ob.girlyanda(-40, 180, 1180, 150, t, 12, 120)
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    m = _pol(POL, "b7m_p", "#89613d", "#3b2414")
    STY = 690
    m += ob.stol_prazdnik(60, STY, 1480, t)
    for i, px in enumerate((340, 760, 1180)):
        m += (f'<ellipse cx="{px}" cy="{STY-14}" rx="112" ry="40" fill="url(#krem)" {o(6)}/>'
              f'<ellipse cx="{px}" cy="{STY-18}" rx="78" ry="26" fill="#efe6cd" {o(4)}/>')
    m += ob.bokal(560, STY - 10, t, .8, .2)
    m += ob.bokal(980, STY - 10, t, .76, .5)
    m += _svecha_stola(1340, STY - 110, t, 1.0, .1)
    m += ob.mandarin(200, STY - 46, .9, .0, t)
    # ХМУРЫЙ ЧЕЛОВЕК на своём стуле — со спины
    cx, cb = 420, POL + 40
    m += ten(cx, cb, 130, 22, .5)
    m += f'<rect x="{cx-100}" y="{cb-640}" width="200" height="300" rx="16" fill="url(#derev)" {o(7)}/>'
    m += (f'<rect x="{cx-92}" y="{cb-250}" width="22" height="250" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{cx+70}" y="{cb-250}" width="22" height="250" fill="url(#derev)" {o(5)}/>')
    m += ob.figura(cx, cb - 150, 470, t, "#272034", "#e8b06a", False, ph=.7)
    s += SL(Z_SRED, m)

    # СВОБОДНЫЙ СТУЛ и ТУЧКА, которая на него взбирается
    f = ""
    sx, sb = 860, POL + 60
    f += ten(sx, sb, 140, 24, .5)
    f += f'<rect x="{sx-106}" y="{sb-680}" width="212" height="320" rx="16" fill="url(#derev)" {o(7)}/>'
    f += f'<rect x="{sx-110}" y="{sb-300}" width="220" height="34" rx="10" fill="url(#derev)" {o(7)}/>'
    f += (f'<rect x="{sx-98}" y="{sb-268}" width="24" height="268" fill="url(#derev)" {o(5)}/>'
          f'<rect x="{sx+74}" y="{sb-268}" width="24" height="268" fill="url(#derev)" {o(5)}/>')
    vz = A.out(A.seg(t, .25, 1.7))
    tx = sx - 150 + 150 * vz
    ty = sb - 110 - 430 * vz - 90 * math.sin(math.pi * vz)
    f += _tuchka(tx, ty, 1.02, t, .1)
    # ТАРЕЛКА придвигается к тучке
    pr = A.ease(A.seg(t, 1.9, 1.2))
    ppx = sx + 150 - 110 * pr
    f += (f'<ellipse cx="{ppx:.0f}" cy="{STY-14}" rx="110" ry="40" fill="url(#krem)" {o(6)}/>'
          f'<ellipse cx="{ppx:.0f}" cy="{STY-18}" rx="76" ry="26" fill="#e7dcc0" {o(4)}/>')
    # САЛФЕТКА заправляется
    sl = A.over(A.seg(t, 2.6, 1.1))
    if sl > .02:
        f += (f'<g transform="translate({tx:.0f},{ty+124:.0f}) rotate({-14*sl:.1f}) scale({sl:.2f})">'
              f'<path d="M-62,0 l124,0 l-40,150 l-44,0 z" fill="url(#list)" {o(6)}/>'
              f'<path d="M-40,40 h92" stroke="{ob.ALYJ}" stroke-width="9" opacity=".7"/></g>')
    f += baza._ramka_pp("levo", "#090c14", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


# ═══════════════════ 148. МИР НА КУХНЕ ═══════════════════

def mir_na_kuhne(t):
    """Кухня перед праздником: в комнате за дверью накрывают, у окна одна
    стоит отвернувшись, вторая подходит — и они обнимаются, тучка-обида
    улетает за окно. Живое: фигура подходит, двое сходятся в одно пятно,
    тучка уплывает. Без лиц, только силуэты."""
    POL = 960
    s = SL(Z_NEBO, _fon("b7n_f", "#333f58", "#1b2330"))

    d = _plitka(60, 140, 780, 420, 118, "b7n_pl", "#dde8ef", "#b0c5d2")
    d += _oboi(0, POL, "#46526c", 128, .14)
    # дверь в комнату — тёплое пятно кадра
    dx, dy, dw, dh = 1330, 180, 470, POL - 180
    d += f'<rect x="{dx-28}" y="{dy-28}" width="{dw+56}" height="{dh+28}" rx="10" fill="url(#derev)" {o(8)}/>'
    d += f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#2a2236"/>'
    d += baza.teplo(dx + dw / 2, dy + dh * .45, 330, 330, .9)
    d += (f'<rect x="{dx+40}" y="{dy+330}" width="{dw-80}" height="30" rx="8"'
          f' fill="url(#derev)" {o(6)}/>')
    d += (f'<path d="M{dx+30},{dy+330} h{dw-60} v34 q{-(dw-60)/2:.0f},34 {-(dw-60):.0f},0 z"'
          f' fill="url(#rush)" {o(5)}/>')
    for i in range(3):
        d += (f'<ellipse cx="{dx+110+i*120}" cy="{dy+324}" rx="44" ry="15"'
              f' fill="url(#krem)" {o(4)}/>')
    d += ob.figura(dx + 120, dy + 318, 230, t, "#2b2436", "#f2c477", True, ph=.3)
    d += ob.figura(dx + 340, dy + 322, 220, t, "#2b2436", "#f2c477", False, ph=.75)
    for i in range(7):
        gx = dx + 40 + i * 64
        gor = .3 + .7 * abs(A.w(t, 2.0 + (i % 3) * .4, i * .2))
        d += f'<circle cx="{gx}" cy="{dy+60}" r="13" fill="{[SVET, ob.ALYJ][i%2]}" opacity="{gor:.2f}"/>'
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    m = _pol(POL, "b7n_p", "#8a6240", "#3c2515")
    # ОКНО кухни, за ним улетает тучка
    ox, oy, ow, oh = 120, 190, 470, 400
    uley = A.ease(A.seg(t, 2.6, 3.6))
    vid = (f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#24344e"/>'
           + baza._sneg_letit(t, 26, 5, .55, .7)
           + _tuchka(ox + 150 + 330 * uley, oy + 240 - 170 * uley,
                     .52 - .22 * uley, t, .4, True, .9 - .8 * uley))
    m += baza.okno_izby(ox, oy, ow, oh, t, vid, .35, False, True)
    m += (f'<rect x="40" y="{POL-250}" width="560" height="34" rx="10" fill="url(#derev)" {o(7)}/>')
    m += (f'<rect x="66" y="{POL-216}" width="510" height="216" rx="10" fill="#6d4a2b" {o(6)}/>')
    for i in range(2):
        m += baza.krynka(170 + i * 190, POL - 262, .72)
    s += SL(Z_SRED, m)

    # ДВОЕ У ОКНА: подходит и обнимает
    f = ""
    pod = A.ease(A.seg(t, .6, 2.2))
    obn = A.ease(A.seg(t, 2.8, 1.6))
    ax = 680
    bx = 1240 - 370 * pod
    f += ob.figura(ax, POL + 60, 640, t, "#2a2235", "#f0bf78", False, ph=.2, profil=obn > .3)
    f += ob.figura(bx, POL + 60, 640, t, "#312839", "#f2c477", True, ph=.6, profil=True)
    if obn > .02:
        f += baza.teplo((ax + bx) / 2, POL - 320, 300 * obn, 260 * obn, .55 * obn)
        f += (f'<path d="M{ax-10:.0f},{POL-330:.0f} q{(bx-ax)/2:.0f},{-70*obn:.0f}'
              f' {bx-ax:.0f},0" fill="none" stroke="#f0c070" stroke-width="{10*obn:.1f}"'
              f' stroke-linecap="round" opacity="{.8*obn:.2f}"/>')
        f += (f'<ellipse cx="{(ax+bx)/2:.0f}" cy="{POL-300:.0f}" rx="{150*obn:.0f}"'
              f' ry="{210*obn:.0f}" fill="none" stroke="#f0c070" stroke-width="7"'
              f' opacity="{.35*obn:.2f}"/>')
    f += baza._ramka_pp("levo", "#090c14", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


# ═══════════════════ 149. ТРИ КОНВЕРТА В ЯЩИК КОМОДА ═══════════════════

def tri_konverta_v_yaschik_komoda(t):
    """Три конверта со значками — монета, сердечко с градусником, домик с
    ключом — сами ложатся в ящик комода, ящик задвигается, листок на нём
    покачивается. Живое: конверты падают, ящик едет, листок качается."""
    POL = 980
    s = SL(Z_NEBO, _fon("b7o_f", "#3a3d55", "#1e2029"))

    d = _oboi(-10, POL + 10, "#4b4e6a", 118, .16)
    d += (f'<rect x="660" y="90" width="620" height="300" rx="14" fill="url(#med)" {o(7)}/>'
          f'<rect x="686" y="116" width="568" height="248" rx="10" fill="#54607e" {o(5)}/>'
          f'<path d="M716,352 l200,-210" stroke="#ffffff" stroke-width="26" opacity=".15"/>')
    d += baza.lampa(1620, 460, t, .78, True)
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    # КОМОД
    m = _pol(POL, "b7o_p", "#87603d", "#3a2313")
    kx, ky, kw = 420, 560, 1040
    m += ten(kx + kw / 2, POL + 6, kw * .5, 28, .55)
    m += f'<rect x="{kx}" y="{ky}" width="{kw}" height="{POL-ky}" rx="12" fill="url(#derev)" {o(9)}/>'
    m += f'<rect x="{kx-24}" y="{ky-34}" width="{kw+48}" height="40" rx="12" fill="url(#med)" {o(7)}/>'
    for i in range(2):
        yy = ky + 190 + i * 150
        m += (f'<rect x="{kx+30}" y="{yy}" width="{kw-60}" height="130" rx="10"'
              f' fill="#70492a" {o(6)}/>')
        for xx in (kx + 300, kx + kw - 300):
            m += f'<ellipse cx="{xx}" cy="{yy+66}" rx="30" ry="15" fill="url(#zol)" {o(4)}/>'
    # ВЕРХНИЙ ЯЩИК выдвинут и задвигается
    zad = A.ease(A.seg(t, 2.9, 1.7))
    vy = ky + 30 + 36 * (1 - zad)
    vh = 150
    m += (f'<path d="M{kx+40},{vy} h{kw-80} l-64,{vh*.5:.0f} h{-(kw-208):.0f} z"'
          f' fill="#2b1b0e" opacity="{.9-.3*zad:.2f}"/>')
    m += (f'<g transform="translate(0,{90*(1-zad):.0f})">'
          f'<rect x="{kx+20}" y="{vy+60}" width="{kw-40}" height="{vh}" rx="10"'
          f' fill="url(#dosk)" {o(8)}/>'
          f'<rect x="{kx+54}" y="{vy+88}" width="{kw-108}" height="{vh-56}" rx="8"'
          f' fill="none" stroke="#6d4a2a" stroke-width="7" opacity=".8"/>'
          f'<ellipse cx="{kx+kw/2:.0f}" cy="{vy+134}" rx="42" ry="18" fill="url(#zol)" {o(5)}/>')
    # ЛИСТОК на ящике — текст кладёт over
    kach = 5 * A.w(t, 3.2)
    m += (f'<g transform="rotate({kach:.2f} {kx+180} {vy+74})">'
          f'<rect x="{kx+118}" y="{vy+74}" width="150" height="178" rx="8"'
          f' fill="url(#list)" {o(6)}/>'
          f'<rect x="{kx+118}" y="{vy+74}" width="150" height="34" rx="8"'
          f' fill="{ob.ALYJ}" opacity=".85"/></g>')
    m += '</g>'
    s += SL(Z_SRED, m)

    # ТРИ КОНВЕРТА ложатся в ящик сами
    vidno = 1.0 - A.ease(A.seg(t, 2.9, .9))
    f = f'<g opacity="{vidno:.2f}">'
    for i, (zn, t0) in enumerate((("moneta", .2), ("serdce", .9), ("domik", 1.6))):
        p = A.ease(A.seg(t, t0, 1.1))
        if p <= .001:
            continue
        x0 = 560 + i * 400
        y0 = -160
        x1 = kx + 230 + i * 300
        y1 = vy + 110
        f += _konvert(x0 + (x1 - x0) * p, y0 + (y1 - y0) * (p * p * .6 + p * .4),
                      .92 - .18 * p, zn, t, i * .2)
    f += '</g>'
    f += baza._ramka_pp("levo", "#090b12", .48)
    s += SL(Z_LETIT, f)
    s += SL(Z_FIX, baza._vinetka(.38))
    return s


# ═══════════════════ 150-151. ПРИГОРЕВШИЙ ПИРОГ ═══════════════════

def prigorevshiy_pirog(t):
    """Из духовки выезжает пирог с чёрным краем, на полу две половинки
    блюдца, хозяйка со спины смеётся. Живое: дымок от пирога, половинки
    блюдца качаются, плечи трясутся от смеха. Без жести и без лиц."""
    POL = 1000
    s = SL(Z_NEBO, _fon("b7p_f", "#37455c", "#1d2633"))

    d = _plitka(560, 140, 820, 420, 122, "b7p_pl", "#e0ebf1", "#b3c7d4")
    d += _oboi(0, POL, "#48556e", 124, .14)
    d += f'<rect x="620" y="200" width="560" height="22" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(4):
        d += baza.krynka(690 + i * 128, 196, .56)
    d += baza.okno_izby(1400, 150, 360, 270, t, None, .45, True, True)
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    # ПЛИТА С ДУХОВКОЙ
    m = _pol(POL, "b7p_p", "#8b6341", "#3d2615")
    px, pw = 160, 700
    m += ten(px + pw / 2, POL + 6, pw * .5, 28, .55)
    m += f'<rect x="{px}" y="{POL-620}" width="{pw}" height="620" rx="16" fill="url(#chug)" {o(9)}/>'
    m += f'<rect x="{px-14}" y="{POL-646}" width="{pw+28}" height="36" rx="12" fill="url(#zhel)" {o(6)}/>'
    for i in range(4):
        m += (f'<circle cx="{px+130+(i%2)*300}" cy="{POL-560+(i//2)*62}" r="44"'
              f' fill="#1b1917" {o(5)}/>')
    # откинутая дверца и противень с пирогом
    m += (f'<path d="M{px+40},{POL-330} h{pw-80} l140,230 h{-(pw-80)-140:.0f} z"'
          f' fill="url(#zhel)" {o(7)}/>')
    m += (f'<rect x="{px+40}" y="{POL-350}" width="{pw-80}" height="30" rx="10"'
          f' fill="#4a5159" {o(5)}/>')
    m += (f'<rect x="{px+60}" y="{POL-560}" width="{pw-120}" height="220" rx="10"'
          f' fill="#120f0d" opacity=".9"/>')
    m += baza.teplo(px + pw / 2, POL - 430, 260, 150, .45)
    vy = A.out(A.seg(t, .2, 1.5))
    prx = px + pw / 2 + 70 * vy
    pry = POL - 430 + 110 * vy
    m += (f'<g transform="translate({prx:.0f},{pry:.0f})">'
          f'{ten(0, 54, 230, 26, .45)}'
          f'<ellipse cx="0" cy="0" rx="250" ry="76" fill="#55585e" {o(6)}/>'
          f'<ellipse cx="0" cy="-16" rx="206" ry="62" fill="url(#med)" {o(6)}/>'
          f'<path d="M-206,-16 q0,-60 206,-60 q206,0 206,60" fill="none" stroke="#1d1410"'
          f' stroke-width="28" opacity=".95"/>'
          f'<path d="M-206,-16 q0,62 206,62 q206,0 206,-62" fill="none" stroke="#2d2017"'
          f' stroke-width="18" opacity=".8"/>'
          f'<path d="M-170,-34 q82,-30 170,-24" fill="none" stroke="#f0cf90"'
          f' stroke-width="14" opacity=".6"/>'
          f'<path d="M-120,-40 q40,26 86,0 q40,26 86,-4" fill="none" stroke="#7d4a20"'
          f' stroke-width="9" opacity=".8"/></g>')
    s += SL(Z_SRED, m)

    # ДЫМОК, БЛЮДЦЕ и ХОЗЯЙКА
    f = baza.dym(prx, pry - 60, t, 6, .32, 420, .42, "#b8bfc8", 1.1)
    for sgn in (-1, 1):
        bx = 1180 + sgn * 140
        kach = 8 * A.w(t, 2.2, .25 if sgn > 0 else .0)
        f += ten(bx, POL + 64, 130, 18, .45)
        f += (f'<g transform="rotate({kach*sgn:.2f} {bx} {POL+46})">'
              f'<path d="M{bx-sgn*140},{POL+50} q{sgn*78},-98 {sgn*140},-6'
              f' q{-sgn*64},50 {-sgn*140},6 z" fill="url(#krem)" {o(7)}/>'
              f'<path d="M{bx-sgn*108},{POL+34} q{sgn*64},-50 {sgn*104},-10" fill="none"'
              f' stroke="{TKAN2}" stroke-width="9" opacity=".75"/></g>')
    tr = 5 * A.w(t, .33) + 7 * A.w(t, 7.4)
    hx, hb = 1560, POL + 170
    f += (f'<g transform="rotate({tr*.3:.2f} {hx} {hb})" >'
          + ob.figura(hx, hb + 4 * abs(A.w(t, 7.4)), 700, t, "#2b2334", "#f2c477", True, ph=.5)
          + f'<path d="M{hx-132},{hb-500} q132,-40 262,6 l-12,268 q-126,34 -244,-6 z"'
            f' fill="url(#krem)" opacity=".88" {o(6)}/></g>')
    f += baza._ramka_pp("levo", "#090c13", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.40))
    return s


# ═══════════════════ 153. СВЕТЛЫЕ ПЛАТЬЯ ВЫХОДЯТ ИЗ ШКАФА ═══════════════════

def svetlye_platya_vyhodyat_iz_shkafa(t):
    """Из шкафа одно за другим выплывают платья — белое в цветочек, голубое,
    жёлтое, красное — и кружатся по комнате. Живое: платья выплывают, подолы
    кружатся, свет в комнате теплеет."""
    POL = 980
    s = SL(Z_NEBO, _fon("b7q_f", "#3b4258", "#20242f"))

    teplee = A.ease(A.seg(t, .2, 2.4))
    d = _oboi(-10, POL + 10, "#4c5572", 120, .16)
    d += baza.teplo(1180, 420, 900, 700, .22 + .40 * teplee)
    d += (f'<rect x="-440" y="-340" width="{W+880}" height="{H+680}" fill="#ffd79a"'
          f' opacity="{.05+.13*teplee:.2f}"/>')
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    # ШКАФ слева, дверца открыта
    m = _pol(POL, "b7q_p", "#8b6340", "#3c2515")
    sx, sy, sw = 60, 140, 520
    m += ten(sx + sw / 2, POL + 6, sw * .5, 26, .55)
    m += f'<rect x="{sx}" y="{sy}" width="{sw}" height="{POL-sy}" rx="12" fill="url(#derev)" {o(9)}/>'
    m += f'<rect x="{sx+28}" y="{sy+30}" width="{sw-56}" height="{POL-sy-80}" rx="10" fill="#241508" {o(6)}/>'
    m += (f'<line x1="{sx+50}" y1="{sy+110}" x2="{sx+sw-50}" y2="{sy+110}"'
          f' stroke="#9aa3ab" stroke-width="12"/>')
    for i in range(4):
        m += (f'<path d="M{sx+90+i*80},{sy+110} q-26,70 -16,210" fill="none"'
              f' stroke="#4b3a47" stroke-width="30" opacity=".6"/>')
    m += _shkaf_stvorka(sx + sw - 20, sy, 300, POL - sy, "b7q_dv", .0)
    m += (f'<g transform="translate({sx+sw+300},{sy}) skewY(-6)">'
          f'<rect x="0" y="0" width="30" height="{POL-sy}" fill="#3d2615" opacity=".5"/></g>')
    # ПЛАТЬЯ выплывают и кружатся
    plat = (("#f4efe4", True), ("#9fc9e4", False), ("#efcf72", False), (ob.ALYJ, False))
    for i, (col, cvet) in enumerate(plat):
        p = A.out(A.seg(t, .15 + i * .42, 1.5))
        if p <= 0:
            continue
        a = -1.9 + i * 1.15 + t * .9
        cx = sx + sw + 70 + (390 + i * 205) * p
        cy = 300 + 190 * math.sin(a) - 60 * p + i * 34
        m += (f'<g transform="rotate({22*math.sin(a+i):.1f} {cx:.0f} {cy:.0f})">'
              + _vesh(cx, cy, 300 - i * 12, 430 - i * 18, col, t, i * .27, cvet, 20.0)
              + '</g>')
    s += SL(Z_SRED, m)

    f = _vesh(1560, 240, 400, 560, ob.ALYJ, t, .5, False, 22.0)
    f += baza._ramka_pp("levo", "#0a0d14", .45)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.34))
    return s


# ═══════════════════ 157. ГЛОБУС С ДВУМЯ ОГОНЬКАМИ ═══════════════════

def globus_s_dvumya_ogonkami(t):
    """Школьный глобус на подставке: на двух сторонах горят огоньки, от них
    тянутся красные нитки, глобус поворачивается, нитки встречаются и
    завязываются в бант. Живое: глобус вращается, нитки тянутся, бант
    затягивается."""
    POL = 1010
    s = SL(Z_NEBO, _fon("b7r_f", "#32405c", "#181f2b"))

    d = _oboi(0, POL, "#45526e", 126, .15)
    d += baza.okno_izby(120, 190, 380, 330, t, None, .45, False, True)
    d += f'<rect x="1340" y="250" width="500" height="24" rx="8" fill="url(#derev)" {o(5)}/>'
    for i in range(7):
        d += (f'<rect x="{1370+i*64}" y="{140+(i%3)*14}" width="48" height="{110-(i%3)*14}"'
              f' rx="6" fill="{[TKAN, ZEL2, MED, TKAN2, "#6b4428", ob.ALYJ, "#51607a"][i]}" {o(4)}/>')
    d += baza.teplo(960, 520, 640, 560, .34)
    d += _plintus(POL)
    s += SL(Z_DAL, d)

    # СТОЛ и ГЛОБУС
    m = _pol(POL, "b7r_p", "#8a6240", "#3b2414")
    STY = 860
    m += ten(960, STY + 110, 520, 34, .5)
    m += f'<rect x="300" y="{STY}" width="1340" height="40" rx="12" fill="url(#derev)" {o(8)}/>'
    m += f'<rect x="400" y="{STY+40}" width="40" height="{POL-STY-40}" fill="url(#derev)" {o(6)}/>'
    m += f'<rect x="1500" y="{STY+40}" width="40" height="{POL-STY-40}" fill="url(#derev)" {o(6)}/>'
    # подставка
    gx, gy, gr = 940, 520, 290
    m += f'<ellipse cx="{gx}" cy="{STY-6}" rx="150" ry="34" fill="url(#med)" {o(7)}/>'
    m += f'<rect x="{gx-22}" y="{gy+gr-40}" width="44" height="{STY-gy-gr+40}" fill="url(#med)" {o(6)}/>'
    m += (f'<path d="M{gx-gr-40},{gy-60} q{gr+40},{gr*1.5:.0f} {gr*2+80:.0f},0"'
          f' fill="none" stroke="url(#med)" stroke-width="26"/>')
    # шар
    m += f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="url(#voda)" {o(9)}/>'
    faza = t * .55
    m += f'<clipPath id="b7r_sh"><circle cx="{gx}" cy="{gy}" r="{gr-6}"/></clipPath>'
    m += f'<g clip-path="url(#b7r_sh)">'
    r = random.Random(21)
    for i in range(7):
        u = (i / 7.0 + faza * .5) % 1.0
        cx0 = gx - gr + u * gr * 2
        sc = max(.12, math.sin(math.pi * u))
        cy0 = gy + r.uniform(-160, 160)
        ww = r.uniform(70, 140) * sc
        hh = r.uniform(50, 100)
        m += (f'<path d="M{cx0-ww:.0f},{cy0:.0f}'
              f' q{ww*.3:.0f},{-hh*1.1:.0f} {ww*.9:.0f},{-hh*.7:.0f}'
              f' q{ww*.5:.0f},{hh*.2:.0f} {ww*1.1:.0f},{hh*.5:.0f}'
              f' q{-ww*.2:.0f},{hh*.9:.0f} {-ww*.8:.0f},{hh*.6:.0f}'
              f' q{-ww*.7:.0f},{-hh*.1:.0f} {-ww*1.2:.0f},{-hh*.4:.0f} z"'
              f' fill="{[ZEL2, TRAVA, "#6f8c4a", ZEL][i%4]}" opacity=".95" {o(4)}/>')
    for i in range(7):
        u = (i / 7.0 + faza) % 1.0
        rx_ = abs(math.cos(math.pi * u)) * gr
        m += (f'<ellipse cx="{gx}" cy="{gy}" rx="{rx_:.0f}" ry="{gr:.0f}" fill="none"'
              f' stroke="#cfe6f2" stroke-width="3" opacity=".30"/>')
    for yy in (-170, -60, 60, 170):
        m += (f'<ellipse cx="{gx}" cy="{gy+yy}" rx="{math.sqrt(max(1,gr*gr-yy*yy)):.0f}"'
              f' ry="18" fill="none" stroke="#cfe6f2" stroke-width="3" opacity=".25"/>')
    m += '</g>'
    m += (f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="none" {o(9)}/>')
    m += (f'<path d="M{gx-gr*.72:.0f},{gy-gr*.6:.0f} q{gr*.5:.0f},{-gr*.3:.0f} {gr*.86:.0f},{gr*.1:.0f}"'
          f' fill="none" stroke="#ffffff" stroke-width="26" opacity=".18"/>')
    s += SL(Z_SRED, m)

    # ДВА ОГОНЬКА и НИТКИ, которые завязываются бантом
    f = ""
    ax, ay = gx - 196, gy - 40
    bx2, by2 = gx + 196, gy + 10
    for i, (ox_, oy_) in enumerate(((ax, ay), (bx2, by2))):
        pul = .6 + .4 * abs(A.w(t, 1.3, i * .4))
        f += baza.teplo(ox_, oy_, 120 * pul, 110 * pul, .8)
        f += f'<circle cx="{ox_}" cy="{oy_}" r="{16*pul:.0f}" fill="{SVET}" {o(3)}/>'
        f += f'<circle cx="{ox_}" cy="{oy_}" r="{34*pul:.0f}" fill="{SVET}" opacity=".35"/>'
    tyan = A.ease(A.seg(t, .25, 1.6))
    mxp, myp = gx, gy - 330
    for sgn, (ox_, oy_) in ((-1, (ax, ay)), (1, (bx2, by2))):
        ex = ox_ + (mxp - ox_) * tyan
        ey = oy_ + (myp - oy_) * tyan
        f += (f'<path d="M{ox_},{oy_} Q{ox_ + sgn*120:.0f},{(oy_+myp)/2 - 120:.0f} {ex:.0f},{ey:.0f}"'
              f' fill="none" stroke="{ob.ALYJ}" stroke-width="11" stroke-linecap="round"/>')
    ban = A.over(A.seg(t, 1.8, 1.2))
    if ban > .02:
        f += (f'<g transform="translate({mxp},{myp}) scale({ban:.2f})">')
        for sgn in (-1, 1):
            f += (f'<path d="M0,0 q{sgn*120},-88 {sgn*138},10 q{-sgn*44},72 {-sgn*138},-10 z"'
                  f' fill="{ob.ALYJ}" {o(6)}/>')
            f += (f'<path d="M0,4 q{sgn*52},62 {sgn*96},110" fill="none" stroke="{ob.ALYJ2}"'
                  f' stroke-width="12" stroke-linecap="round"/>')
        f += f'<circle cx="0" cy="0" r="24" fill="{ob.ALYJ2}" {o(5)}/>'
        f += '<circle cx="-8" cy="-8" r="8" fill="#f4a89c" opacity=".7"/>'
        f += '</g>'
    f += baza._ramka_pp("oba", "#090c13", .5)
    s += SL(Z_PERED, f)
    s += SL(Z_FIX, baza._vinetka(.40))
    return s
