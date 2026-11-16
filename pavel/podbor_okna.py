# -*- coding: utf-8 -*-
"""ЭТАЛОН. Куда положить окно вставки В ЭТОЙ сцене — считается по картинке.

Копируется в папку кода ролика как `podbor_okna.py` и запускается оттуда
(ему нужны lok/kadr/kamera/plan этого ролика). Результат `okna.json`
коммитится вместе с кодом: шарды облака обязаны брать ОДНО И ТО ЖЕ окно,
иначе на стыке шардов окно прыгнет.

Его слово 14.11: «Почему оно у тебя всегда одинакового размера? Почему
всегда справа? Можно слева, если там пустая сцена. Можно выше, можно в
меньшем размере, можно чуть большим» (R-0048).

Как: кадр декорации рисуется в уменьшенном виде, по нему считается карта
ЗАНЯТОСТИ (градиент яркости — там, где нарисован предмет, он высокий, на
небе и снегу почти нулевой). Дальше перебираются варианты окна — две
стороны, три высоты, три размера — и берётся тот, под которым занятость
наименьшая, с предпочтением крупному окну (R-0024).

Результат кладётся в okna.json РЯДОМ С КОДОМ и коммитится: шарды облака
должны брать одно и то же окно, считать его на раннере нельзя.

    python3 podbor_okna.py            # посчитать и записать okna.json
"""
import io, json, os, sys
import numpy as np
from PIL import Image
import cairosvg

import baza, lok, kamera
from baza import W, H

HERE = os.path.dirname(os.path.abspath(__file__))
MAL = (480, 270)                 # в этом размере считаем занятость
POLE = 56                        # минимальное поле от края кадра
SHIRINY = (1120, 980, 860)       # крупное / обычное / поменьше
VERH = (140, 290, 430)


def _scena_png(pl, t, p):
    """Кадр БЕЗ окна и надписей — только рисованная сцена с ходом камеры."""
    from karta import DEK
    import kadr
    syr = getattr(lok, DEK[pl["lok"]])(t)
    if '<g data-z="-' not in syr:
        syr += baza.ramka_pp("levo", "#14110c", .30)
    scena = kamera.kadr(syr, kadr.hod_plana(pl), p)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
           f'<defs>{baza.defs()}</defs>{scena}</svg>')
    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf,
                     output_width=MAL[0], output_height=MAL[1], unsafe=True)
    im = Image.open(buf).convert("RGB")
    return (np.asarray(im.convert("L"), dtype=np.float32) / 255.0,
            np.asarray(im, dtype=np.float32) / 255.0)


def zanyatost(pl):
    """Карта занятости: среднее по трём моментам плана, чтобы учесть ход камеры."""
    karta = np.zeros(MAL[::-1], dtype=np.float32)
    sek = pl["sek"]
    cvet = None
    for t, p in ((0.2, .05), (sek * .5, .5), (max(0.4, sek - .3), .95)):
        a, rgb = _scena_png(pl, t, p)
        if cvet is None:
            cvet = rgb
        gx = np.abs(np.diff(a, axis=1, prepend=a[:, :1]))
        gy = np.abs(np.diff(a, axis=0, prepend=a[:1, :]))
        karta += gx + gy
    karta /= 3.0
    # мягкое размытие, чтобы тонкая линия не весила как целый предмет
    k = np.ones((5, 5), dtype=np.float32) / 25.0
    pad = np.pad(karta, 2, mode="edge")
    out = np.zeros_like(karta)
    for i in range(5):
        for j in range(5):
            out += pad[i:i + karta.shape[0], j:j + karta.shape[1]] * k[i, j]
    m = out.max()
    verh = cvet[: cvet.shape[0] // 3]
    r_, g_, b_ = verh[..., 0].mean(), verh[..., 1].mean(), verh[..., 2].mean()
    # верх кадра синее красного — это небо, значит сцена уличная;
    # в избе верх кадра тёплый, дерево и бревно (красный выше синего)
    tip = "ulica" if b_ > r_ + .02 else "komnata"
    return (out / m if m > 1e-6 else out), tip


def varianty():
    for w in SHIRINY:
        h = int(round(w * 551 / 980))
        for x in (POLE, W - POLE - w):
            for y in VERH:
                if y + h <= H - POLE:
                    yield (x, y, w, h)


def vybrat(pl, karta):
    sx, sy = MAL[0] / W, MAL[1] / H
    luchshe, ball_l = None, 1e9
    for (x, y, w, h) in varianty():
        x0, y0 = int(x * sx), int(y * sy)
        x1, y1 = int((x + w) * sx), int((y + h) * sy)
        kus = karta[y0:y1, x0:x1]
        if kus.size == 0:
            continue
        # занятость под окном. Среднего мало: мелкий предмет (буханка на доске,
        # фигура у проруби) тонет в среднем и всё равно уходит под окно —
        # поймано глазами 14.11. Поэтому к среднему добавляется ПИК.
        ball = (float(kus.mean()) + .9 * float(np.quantile(kus, .97))
                + .055 * (1 - w / SHIRINY[0]))
        # поля вокруг: окно не должно вставать вплотную к плотному месту
        if ball < ball_l:
            luchshe, ball_l = (x, y, w, h), ball
    return luchshe, ball_l


ZONY = ((620, 340), (470, 300))        # размеры мест под обживку


def mesta_obzhivki(pl, karta, okno, tip):
    """Два самых пустых места ВНЕ окна — туда ставится обжитый план
    (изба с огоньком и дымом на улице, полка с утварью в избе). Если пусто
    нигде нет, место не выдаётся: лепить поверх предмета нельзя (R-0007)."""
    # Зона ВСЕГДА прижата к низу кадра: изба и полка должны стоять на земле,
    # а не висеть посреди кадра (поймано глазами 14.11 на первом же листе).
    sx, sy = MAL[0] / W, MAL[1] / H
    ox, oy, ow, oh = okno
    out = []
    skolko = 1 if tip == "ulica" else 2      # на улице одной избы довольно
    for (zw, zh) in ZONY[:skolko]:
        y = H - zh - 8
        luchshe, ball_l = None, 1e9
        for x in range(POLE, W - POLE - zw + 1, 40):
            if not (x + zw < ox or x > ox + ow or y + zh < oy or y > oy + oh):
                continue
            if any(not (x + zw < bx or x > bx + bw) for bx, by, bw, bh in out):
                continue
            kus = karta[int(y * sy):, int(x * sx):int((x + zw) * sx)]
            if kus.size == 0:
                continue
            b = float(kus.mean())
            if b < ball_l:
                luchshe, ball_l = (x, y, zw, zh), b
        if luchshe and ball_l < .060:
            out.append(luchshe)
    return out


if __name__ == "__main__":
    import kadr, plan
    st = json.load(open(os.path.join(HERE, "stock_video.json"), encoding="utf-8"))
    ph = json.load(open(os.path.join(HERE, "stock.json"), encoding="utf-8"))
    out = {"okna": {}, "obzhivka": {}, "tip": {}}
    for p in plan.PLANY:
        karta, tip = zanyatost(p)
        out["tip"][str(p["n"])] = tip
        est = kadr.nado_okno(p) or kadr.data_kartochka(p)
        if est:
            okno, ball = vybrat(p, karta)
            out["okna"][str(p["n"])] = list(okno)
        else:
            okno, ball = (-9999, -9999, 0, 0), 0.0
        mesta = mesta_obzhivki(p, karta, okno, tip)
        if mesta:
            out["obzhivka"][str(p["n"])] = [list(m) for m in mesta]
        storona = "—" if not est else ("слева" if okno[0] < W / 2 else "справа")
        print("план %3d  %-32s %-8s окно %-6s %4dx%-3d  обживка %d"
              % (p["n"], p["lok"][:32], tip, storona, okno[2], okno[3], len(mesta)),
              flush=True)
    json.dump(out, open(os.path.join(HERE, "okna.json"), "w"),
              ensure_ascii=False, indent=1)
    print("окон:", len(out["okna"]), "· мест под обживку:",
          sum(len(v) for v in out["obzhivka"].values()))
