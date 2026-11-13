# -*- coding: utf-8 -*-
"""Контактный лист декораций: смотреть кадры глазами до облака (правило №4).
   python3 list_dek.py <выход.jpg> <func> [func ...]"""
import io, sys, cairosvg
from PIL import Image, ImageDraw
import lok
from baza import defs, W, H

out = sys.argv[1]
names = sys.argv[2:]
TW, TH = 470, 264
cols = 3
rows = (len(names) + cols - 1) // cols
L = Image.new("RGB", (cols * TW, rows * (TH + 20)), (18, 18, 22))
d = ImageDraw.Draw(L)
for i, nm in enumerate(names):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d"><defs>%s</defs>%s</svg>'
           % (W, H, defs(), getattr(lok, nm)(2.2)))
    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf, output_width=TW, output_height=TH, unsafe=True)
    im = Image.open(buf).convert("RGB")
    x, y = (i % cols) * TW, (i // cols) * (TH + 20)
    L.paste(im, (x, y))
    d.text((x + 6, y + TH + 4), "%d %s" % (i + 1, nm[:46]), fill=(228, 228, 236))
L.save(out, quality=88)
print(out, L.size)
