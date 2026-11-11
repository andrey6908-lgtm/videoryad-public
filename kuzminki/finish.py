# -*- coding: utf-8 -*-
"""Склейка частей в немой файл. Звук подмешивается на его машине."""
import os, sys, subprocess, glob

out = sys.argv[1] if len(sys.argv) > 1 else "out"
segs = sorted(glob.glob(os.path.join(out, "seg*.mp4")))
if not segs:
    raise SystemExit("частей нет")
lst = os.path.join(out, "spisok.txt")
with open(lst, "w") as f:
    for s in segs:
        f.write("file '%s'\n" % os.path.abspath(s))
fin = os.path.join(out, "kuzminki-nemoe.mp4")
r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c", "copy", fin], capture_output=True, text=True)
if r.returncode:
    print(r.stderr[-3000:]); raise SystemExit(1)
print("склеено %d частей → %s, %.1f МБ" % (len(segs), fin, os.path.getsize(fin) / 1e6))
