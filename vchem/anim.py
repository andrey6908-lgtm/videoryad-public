# -*- coding: utf-8 -*-
"""Движение от времени: сглаживания и колебания."""
import math


def clamp(p): return max(0.0, min(1.0, p))
def seg(t, t0, d): return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def ease(p):
    p = clamp(p); return p * p * (3 - 2 * p)
def out(p):
    p = clamp(p); return 1 - (1 - p) ** 3
def over(p, k=1.7):
    p = clamp(p); return 1 + (k + 1) * (p - 1) ** 3 + k * (p - 1) ** 2
def w(t, period, phase=0.0): return math.sin(2 * math.pi * (t / period + phase))
def blink(t, period=4.3, phase=0.0, d=0.15): return ((t / period) + phase) % 1.0 < d / period
