# -*- coding: utf-8 -*-
"""Раскадровка пробника ПОЛНОЛУНИЕ: 30 секунд, четыре сцены, восемь эффектов
текста. Время абсолютное, в секундах. Зум задаётся окном просмотра.
Наложений отдельным слоем НЕТ: весь текст рисуется внутри кадра, покадрово."""
import anim as A

FPS = 25
TRANS = 0.35             # перекрытие между сценами

# (начало, конец, сцена, зум от, зум до, якорь x, якорь y)
SHOTS = [
    (0.00,  8.60, "hook",   1.00, 1.07, .50, .52),
    (8.60, 11.60, "bump",   1.03, 1.09, .46, .50),
    (11.60, 21.40, "nelzya", 1.00, 1.08, .44, .50),
    (21.40, 30.00, "fact",   1.04, 1.13, .54, .46),
]

TOTAL = SHOTS[-1][1]
NFRAMES = int(round(TOTAL * FPS))
TAG = "probnik30"

# что показывает пробник — печатается в отчёт, чтобы смотреть по списку
EFFECTS = ["лунный налив", "печать", "плашка-маска", "падение слов",
           "зачёркивание", "росчерк", "штамп", "лента-разделитель"]


def _zoom(sh, gt):
    a, b, nm, z0, z1, cx, cy = sh
    p = A.clamp((gt - a) / (b - a))
    return z0 + (z1 - z0) * A.ease(p)


def frame_info(i):
    """Кадр → (сцена, локальное время, зум, якорь), сцена перехода и доля смеси."""
    gt = i / FPS
    k = 0
    for j, sh in enumerate(SHOTS):
        if sh[0] <= gt < sh[1]:
            k = j
            break
    else:
        k = len(SHOTS) - 1
    a, b, nm, z0, z1, cx, cy = SHOTS[k]
    lt = gt - a + (TRANS if k > 0 else 0.0)
    cur = (nm, lt, _zoom(SHOTS[k], gt), cx, cy)
    nxt, mix = None, 0.0
    if k + 1 < len(SHOTS) and gt > b - TRANS:
        sh2 = SHOTS[k + 1]
        mix = A.clamp((gt - (b - TRANS)) / TRANS)
        nxt = (sh2[2], gt - (sh2[0] - TRANS), _zoom(sh2, gt), sh2[5], sh2[6])
    return cur, nxt, mix
