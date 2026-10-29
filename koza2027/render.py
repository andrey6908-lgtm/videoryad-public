# -*- coding: utf-8 -*-
"""Рендер немого видео «Год козы 2027». Запускается на раннере GitHub.
Звук НЕ трогает: озвучка в облако не уезжает, она подмешивается на машине."""
import os, subprocess, sys, json
import cairosvg
import art, plan

OUT = sys.argv[1] if len(sys.argv) > 1 else "koza_out"
TMP = os.path.join(OUT, "tmp")
os.makedirs(TMP, exist_ok=True)
FPS = 30
SRC_W, SRC_H = 2880, 1620


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print("КОМАНДА УПАЛА:", " ".join(cmd[:14]), "...")
        print(r.stderr[-3000:])
        raise SystemExit(1)


print("1/4 рисую кадры")
used = sorted({s[2] for s in plan.SHOTS})
for nm in used:
    png = f"{TMP}/art_{nm}.png"
    cairosvg.svg2png(bytestring=art.svg(nm).encode("utf-8"),
                     write_to=png, output_width=SRC_W, output_height=SRC_H)
    print("   ", nm, os.path.getsize(png) // 1024, "КБ")

print("2/4 рисую наложения")
for nm, svg_src, a, b in plan.OVERLAYS:
    cairosvg.svg2png(bytestring=svg_src.encode("utf-8"),
                     write_to=f"{TMP}/ov_{nm}.png", output_width=1920, output_height=1080)
    print("   ", nm, "%.1f-%.1f с" % (a, b))

print("3/4 движение по сценам")
lst = []
for i, (a, b, nm, z0, z1, cx, cy) in enumerate(plan.SHOTS):
    dur = b - a
    nf = max(2, round(dur * FPS))
    out = f"{TMP}/sc{i:03d}.mp4"
    vf = (f"scale={SRC_W}:{SRC_H},"
          f"zoompan=z='{z0:.4f}+({z1 - z0:.4f})*on/{nf}'"
          f":x='(iw-iw/zoom)*{cx}':y='(ih-ih/zoom)*{cy}'"
          f":d=1:s=1920x1080:fps={FPS},format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS),
         "-t", f"{dur:.4f}", "-i", f"{TMP}/art_{nm}.png",
         "-vf", vf, "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", "-r", str(FPS), out])
    lst.append(out)
    print("   сцена %2d  %-12s %.2f с" % (i + 1, nm, dur))

with open(f"{TMP}/list.txt", "w") as f:
    for p in lst:
        f.write("file '%s'\n" % os.path.abspath(p))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
     "-i", f"{TMP}/list.txt", "-c", "copy", f"{TMP}/base.mp4"])

print("4/4 кладу наложения")
inputs, fc, cur = ["-i", f"{TMP}/base.mp4"], [], "0:v"
for k, (nm, _s, a, b) in enumerate(plan.OVERLAYS, start=1):
    d = b - a
    inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.4f}", "-i", f"{TMP}/ov_{nm}.png"]
    fc.append(f"[{k}:v]format=rgba,fade=in:st=0:d=0.35:alpha=1,"
              f"fade=out:st={max(0.0, d - 0.55):.3f}:d=0.55:alpha=1,"
              f"setpts=PTS-STARTPTS+{a:.4f}/TB[o{k}]")
    fc.append(f"[{cur}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[v{k}]")
    cur = f"v{k}"
final = os.path.join(OUT, "koza2027_chasti1-3_nemoe.mp4")
run(["ffmpeg", "-v", "error", "-y"] + inputs +
    ["-filter_complex", ";".join(fc), "-map", f"[{cur}]",
     "-c:v", "libx264", "-crf", "19", "-preset", "medium",
     "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", final])

dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", final], capture_output=True, text=True).stdout.strip()
sz = os.path.getsize(final) // 1024
print("ГОТОВО:", final, sz, "КБ,", dur, "с")
json.dump({"file": os.path.basename(final), "seconds": float(dur),
           "shots": len(plan.SHOTS), "overlays": len(plan.OVERLAYS)},
          open(os.path.join(OUT, "report.json"), "w"), ensure_ascii=False, indent=1)
for p in lst:
    os.remove(p)
