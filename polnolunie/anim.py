# -*- coding: utf-8 -*-
"""Кирпичики движения формата ПОЛНОЛУНИЕ: всё считается от времени.
Кадр рисуется заново каждые 1/FPS секунды, поэтому ничего не стоит
«оживить» — это параметр, а не новый рисунок."""
import math


def w(t, period, phase=0.0):
    """Колебание −1..1."""
    return math.sin(2 * math.pi * (t / period + phase))


def ease(p):
    """Плавный вход-выход 0..1."""
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def out(p):
    """Быстро начал, мягко встал."""
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


def over(p, k=1.7):
    """С перелётом: доезжает выше цели и возвращается."""
    p = max(0.0, min(1.0, p))
    return 1 + (k + 1) * (p - 1) ** 3 + k * (p - 1) ** 2


def clamp(p):
    return max(0.0, min(1.0, p))


def seg(t, t0, dur):
    """Доля прохождения отрезка [t0, t0+dur]."""
    return clamp((t - t0) / dur) if dur > 0 else (1.0 if t >= t0 else 0.0)


def blink(t, period=4.3, phase=0.0, dur=0.15):
    """True, пока глаз закрыт."""
    return ((t / period) + phase) % 1.0 < dur / period
