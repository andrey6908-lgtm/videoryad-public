# -*- coding: utf-8 -*-
"""Смотреть кадры ГЛАЗАМИ до отправки в облако (правило №4 «Козы»).
python3 preview.py <куда> [секунда ...]"""
import os, sys
import cairosvg
import art, plan

out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/pl"
secs = [float(x) for x in sys.argv[2:]] or [1.0, 4.4, 6.2, 9.4, 10.6, 13.0, 14.3,
                                            17.0, 22.2, 24.4, 25.6, 29.0]
os.makedirs(out, exist_ok=True)
for s in secs:
    i = int(round(s * plan.FPS))
    cur, nxt, mix = plan.frame_info(i)
    nm, lt, z, cx, cy = cur
    p = os.path.join(out, "t%05.1f_%s.png" % (s, nm))
    cairosvg.svg2png(bytestring=art.svg(nm, lt, i / plan.FPS, z, cx, cy).encode("utf-8"),
                     write_to=p, output_width=1280, output_height=720)
    print("%6.1f с  %-7s зум %.3f  смесь %.2f  ->  %s" % (s, nm, z, mix, p))
