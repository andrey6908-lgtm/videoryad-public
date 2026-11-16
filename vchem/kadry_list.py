# -*- coding: utf-8 -*-
"""Контактный лист ГОТОВЫХ кадров ролика (декорация + камера + окно + титры).
   python3 kadry_list.py <выход.jpg> <план> [план ...]"""
import io, sys, cairosvg
from PIL import Image, ImageDraw
import kadr, plan

out = sys.argv[1]
nums = [int(x) for x in sys.argv[2:]]
P = {p["n"]: (i, p) for i, p in enumerate(plan.PLANY)}
TW, TH = 470, 264
cols = 3
rows = (len(nums) + cols - 1) // cols
L = Image.new("RGB", (cols * TW, rows * (TH + 20)), (16, 16, 20))
d = ImageDraw.Draw(L)
for i, n in enumerate(nums):
    idx, pl = P[n]
    svg = kadr.body(pl, min(2.2, pl["sek"] * .5), .5, zaglushki=True)
    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf, output_width=TW, output_height=TH, unsafe=True)
    im = Image.open(buf).convert("RGB")
    x, y = (i % cols) * TW, (i // cols) * (TH + 20)
    L.paste(im, (x, y))
    d.text((x + 6, y + TH + 4), "%d · %s · %.1fс" % (n, pl["lok"][:40], pl["sek"]), fill=(226, 226, 236))
L.save(out, quality=88)
print(out, L.size)
