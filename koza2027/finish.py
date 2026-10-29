# -*- coding: utf-8 -*-
"""Склейка частей и наложения поверх. Запускается после всех шардов."""
import os, sys, json, subprocess
import cairosvg
import plan

SEG, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
segs = sorted(os.path.join(SEG, f) for f in os.listdir(SEG) if f.startswith("seg") and f.endswith(".mp4"))
print("частей найдено:", len(segs))
assert segs, "нет ни одной части"

with open("/tmp/list.txt", "w") as f:
    for p in segs:
        f.write("file '%s'\n" % os.path.abspath(p))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd[:12]), "...\n", r.stderr[-3000:]); raise SystemExit(1)


run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "/tmp/list.txt",
     "-c", "copy", "/tmp/base.mp4"])

for nm, svg_src, aa, bb in plan.OVERLAYS:
    cairosvg.svg2png(bytestring=svg_src.encode("utf-8"), write_to="/tmp/ov_%s.png" % nm,
                     output_width=1920, output_height=1080)

inputs, fc, cur = ["-i", "/tmp/base.mp4"], [], "0:v"
for k, (nm, _s, aa, bb) in enumerate(plan.OVERLAYS, start=1):
    d = bb - aa
    inputs += ["-loop", "1", "-framerate", str(plan.FPS), "-t", "%.4f" % d, "-i", "/tmp/ov_%s.png" % nm]
    fc.append("[%d:v]format=rgba,fade=in:st=0:d=0.35:alpha=1,"
              "fade=out:st=%.3f:d=0.55:alpha=1,setpts=PTS-STARTPTS+%.4f/TB[o%d]"
              % (k, max(0.0, d - 0.55), aa, k))
    fc.append("[%s][o%d]overlay=0:0:eof_action=pass:enable='between(t,%.3f,%.3f)'[v%d]"
              % (cur, k, aa, bb, k))
    cur = "v%d" % k

final = os.path.join(OUT, "koza2027_chasti1-3_nemoe.mp4")
run(["ffmpeg", "-v", "error", "-y"] + inputs +
    ["-filter_complex", ";".join(fc), "-map", "[%s]" % cur,
     "-c:v", "libx264", "-crf", "19", "-preset", "medium",
     "-pix_fmt", "yuv420p", "-r", str(plan.FPS), "-movflags", "+faststart", final])

dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", final], capture_output=True, text=True).stdout.strip()
print("ГОТОВО:", final, os.path.getsize(final) // 1024, "КБ,", dur, "с")
json.dump({"file": os.path.basename(final), "seconds": float(dur), "frames": plan.NFRAMES,
           "shots": len(plan.SHOTS), "arts": len(set(s[2] for s in plan.SHOTS)),
           "overlays": len(plan.OVERLAYS)},
          open(os.path.join(OUT, "report.json"), "w"), ensure_ascii=False, indent=1)
