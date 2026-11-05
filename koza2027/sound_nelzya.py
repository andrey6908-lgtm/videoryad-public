# -*- coding: utf-8 -*-
"""Звук второго ролика «Что нельзя готовить на Новый год козы» — одним проходом.

Озвучка одним файлом, музыка одной дорожкой через весь ролик, эффекты по
абсолютному времени. «Дзинь» под каждый выскакивающий ярлык берётся прямо
из раскадровки (наложения с именем на n_tag), чтобы звон не разъехался
с картинкой.

    python3 sound_nelzya.py <куда.m4a>
"""
import os, subprocess, sys

KOZA = os.path.expanduser("~/projects/videoryad-cloud-rezerv/koza2027")
VOICE = os.path.expanduser("~/projects/koza-nelzya/narration.mp3")
SND = "/mnt/d/YouTube/СБОРЩИК ЖИВОТНЫЕ библиотека/ЗВУКИ/новогодние"
MUS = ("/mnt/d/YouTube/СБОРЩИК ЖИВОТНЫЕ библиотека/МУЗЫКА/"
       "Lotus Pond - Aakash Gandhi - лекое но слегка бодренькое.mp3")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sound_nelzya.m4a"
sys.path.insert(0, KOZA)
import nelzya

DUR = nelzya.TOTAL          # 855,6 с: озвучка 849,6 + 6 с финала

# (файл, абсолютное время, дБ, обрезка в секундах или None)
fx = [
    ("бубенцы-02.mp3",        0.40, -21, None),
    ("коза-блеяние-01.mp3",   9.60, -18, None),     # «седьмое» — про хозяйку
    ("треск-свечи-01.mp3",   57.90, -33, None),
    ("треск-камина-02.mp3",  64.60, -32, 8),        # «она ещё и огненная»
    ("колокол-удар-01.mp3",  74.00, -28, None),     # «просто отвернётся»
    ("гул-застолья-01.mp3",  91.70, -30, 7),        # застолья Лошади
    ("гул-застолья-02.mp3", 234.40, -31, 6),        # стол ломится
    ("коза-блеяние-02.mp3", 299.30, -17, None),     # седьмое: баранина
    ("коза-блеяние-01.mp3", 358.30, -18, None),     # «молоко она отдаёт сама»
    ("бокалы-01.mp3",       387.30, -22, None),
    ("куранты-01.mp3",      393.40, -27, None),     # «шампанское под куранты»
    ("треск-свечи-01.mp3",  406.80, -33, None),
    ("гул-застолья-01.mp3", 471.80, -30, 6),        # стол Лошади
    ("треск-свечи-01.mp3",  516.20, -33, None),     # «свечи красные»
    ("бокалы-02.mp3",       531.50, -24, None),
    ("треск-камина-02.mp3", 611.40, -33, 7),        # «заглянем в Китай»
    ("колокол-удар-01.mp3", 721.50, -28, None),
    ("куранты-01.mp3",      749.20, -25, None),     # стол к полуночи
    ("бубенцы-01.mp3",      795.50, -23, None),
    ("бокалы-01.mp3",       820.50, -23, None),
    ("куранты-01.mp3",      840.90, -15, None),     # «когда пробьют куранты»
    ("колокол-удар-01.mp3", 845.60, -22, None),
    ("бубенцы-02.mp3",      848.60, -20, None),     # финал
]

dzin = sorted(a for nm, _s, a, _b in nelzya.OVERLAYS if nm.startswith("n_tag"))
print("ярлыков со звоном:", len(dzin), "| эффектов:", len(fx))

inputs, fc, mixed = [], [], []
inputs += ["-i", VOICE]
fc.append("[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[g0]")
mixed.append("[g0]")
idx = 1

inputs += ["-stream_loop", "8", "-i", MUS]
fc.append("[%d:a]atrim=0:%.2f,asetpts=N/SR/TB,volume=-25dB,"
          "afade=t=in:st=0:d=3,afade=t=out:st=%.1f:d=4,aresample=48000[m]" % (idx, DUR, DUR - 4))
mixed.append("[m]"); idx += 1

for f, at, db, cut in fx:
    inputs += ["-i", os.path.join(SND, f)]
    pre = "atrim=0:%d," % cut if cut else ""
    fade = ("afade=t=in:st=0:d=1,afade=t=out:st=%d:d=2," % (cut - 2)) if cut else ""
    fc.append("[%d:a]%s%svolume=%ddB,adelay=%d|%d,aresample=48000[x%d]"
              % (idx, pre, fade, db, int(at * 1000), int(at * 1000), idx))
    mixed.append("[x%d]" % idx); idx += 1

for at in dzin:
    inputs += ["-i", os.path.join(SND, "бубенцы-01.mp3")]
    fc.append("[%d:a]atrim=0:0.45,volume=-24dB,afade=t=out:st=0.25:d=0.2,"
              "adelay=%d|%d,aresample=48000[z%d]" % (idx, int(at * 1000), int(at * 1000), idx))
    mixed.append("[z%d]" % idx); idx += 1

fc.append("%samix=inputs=%d:duration=longest:normalize=0,alimiter=limit=0.95[a]"
          % ("".join(mixed), len(mixed)))
cmd = (["nice", "-n", "19", "ionice", "-c3", "ffmpeg", "-v", "error", "-y"] + inputs +
       ["-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-ac", "2", "-t", "%.2f" % DUR, OUT])
print("входов:", idx, "— считаем")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode:
    print(r.stderr[-3000:]); raise SystemExit(1)
print("звук собран:", OUT)
m = subprocess.run(["ffmpeg", "-nostats", "-i", OUT, "-af", "ebur128", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
for ln in m.splitlines():
    if "I:" in ln and "LUFS" in ln:
        print("громкость:", ln.strip())
