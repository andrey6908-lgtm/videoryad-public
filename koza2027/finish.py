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

# ---- живые вставки: кусок настоящего видео внутри рисунка ----------------
# Клипы качает САМ раннер по прямым публичным ссылкам: ключ Pexels в облако
# не едет. Окно одного размера на весь ролик, поэтому маска скругления и
# рамка считаются по одному разу, а не на каждую вставку.
STOCK = list(getattr(plan, "STOCK", []))
stock_files = {}
if STOCK:
    import urllib.request
    bw, bh = STOCK[0][3][2], STOCK[0][3][3]
    R = 44
    cairosvg.svg2png(bytestring=(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="{bh}">'
        f'<rect x="0" y="0" width="{bw}" height="{bh}" rx="{R}" fill="#ffffff"/></svg>'
    ).encode(), write_to="/tmp/sv_mask.png", output_width=bw, output_height=bh)
    PAD = 30
    cairosvg.svg2png(bytestring=(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw+PAD*2}" height="{bh+PAD*2}">'
        f'<rect x="{PAD-9}" y="{PAD-3}" width="{bw+18}" height="{bh+18}" rx="{R+9}"'
        ' fill="#000000" opacity=".38"/>'
        f'<rect x="{PAD-6}" y="{PAD-6}" width="{bw+12}" height="{bh+12}" rx="{R+6}"'
        ' fill="none" stroke="#17130f" stroke-width="15"/></svg>'
    ).encode(), write_to="/tmp/sv_frame.png", output_width=bw+PAD*2, output_height=bh+PAD*2)
    for k, (aa, bb, url, box) in enumerate(STOCK):
        if url in stock_files:
            continue
        dst = "/tmp/sv_%02d.mp4" % len(stock_files)
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=90) as r, open(dst, "wb") as f:
                    f.write(r.read())
                break
            except Exception as e:
                print("   вставка %s: попытка %d не вышла (%s)" % (url[-28:], attempt + 1, e))
        if not os.path.exists(dst) or os.path.getsize(dst) < 100000:
            raise SystemExit("вставка не скачалась: %s" % url)
        stock_files[url] = dst
        print("   вставка: %s -> %d КБ" % (url[-28:], os.path.getsize(dst) // 1024))

# Сборка идёт ЭТАПАМИ, и каждый слой едет СВОИМ проходом с -itsoffset.
# Почему не одним фильтром: сдвиг слоя через setpts=PTS-STARTPTS+t/TB
# заставляет ffmpeg копить кадры слоя до его начала — на вставке, которая
# появляется на 283-й секунде, это гигабайты, и раннер убивает процесс
# (exit 143, поймано дважды 01.11). -itsoffset двигает метки на ВХОДЕ,
# ничего не накапливая.
CUR = "/tmp/base.mp4"
STAGE = 0


def stage_out():
    global STAGE
    STAGE += 1
    return "/tmp/stage%d.mp4" % STAGE


def encode(last):
    if last:
        return ["-c:v", "libx264", "-crf", "19", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-r", str(plan.FPS), "-movflags", "+faststart"]
    return ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-r", str(plan.FPS)]


FINAL = os.path.join(OUT, "koza2027_%s_nemoe.mp4" % plan.TAG)
total_layers = len(STOCK) + len(plan.OVERLAYS)
done_layers = 0

for i, (aa, bb, url, box) in enumerate(STOCK):
    x, y, w, h = box
    d = bb - aa
    done_layers += 1
    out = FINAL if done_layers == total_layers else stage_out()
    inputs = ["-i", CUR,
              "-loop", "1", "-framerate", str(plan.FPS), "-t", "%.3f" % plan.TOTAL,
              "-i", "/tmp/sv_mask.png",
              "-loop", "1", "-framerate", str(plan.FPS), "-t", "%.3f" % plan.TOTAL,
              "-i", "/tmp/sv_frame.png",
              "-itsoffset", "%.4f" % aa, "-stream_loop", "-1", "-t", "%.3f" % d,
              "-i", stock_files[url]]
    fc = [
        "[3:v]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,setsar=1,fps=%d,"
        "colorbalance=rm=.07:gm=.01:bm=-.06,eq=saturation=.94:contrast=1.03:brightness=-.02,"
        "format=rgba,fade=in:st=%.3f:d=0.25:alpha=1,fade=out:st=%.3f:d=0.35:alpha=1[sv]"
        % (w, h, w, h, plan.FPS, aa, max(aa, bb - 0.35)),
        "[1:v]format=gray,setsar=1[m]",
        "[sv][m]alphamerge[svm]",
        "[0:v][svm]overlay=%d:%d:eof_action=pass:enable='between(t,%.3f,%.3f)'[o1]"
        % (x, y, aa, bb),
        "[2:v]format=rgba,setsar=1,fade=in:st=%.3f:d=0.25:alpha=1,"
        "fade=out:st=%.3f:d=0.35:alpha=1[fr]" % (aa, max(aa, bb - 0.35)),
        "[o1][fr]overlay=%d:%d:eof_action=pass:enable='between(t,%.3f,%.3f)'[v]"
        % (x - 30, y - 30, aa, bb),
    ]
    print("слой %d/%d: живая вставка %.0f-%.0f с" % (done_layers, total_layers, aa, bb), flush=True)
    run(["ffmpeg", "-v", "error", "-y"] + inputs +
        ["-filter_complex", ";".join(fc), "-map", "[v]"] +
        encode(done_layers == total_layers) + [out])
    if CUR.startswith("/tmp/stage"):
        os.remove(CUR)
    CUR = out

GROUP = 6
ovs = list(plan.OVERLAYS)
for g0 in range(0, len(ovs), GROUP):
    chunk = ovs[g0:g0 + GROUP]
    inputs, fc, cur = ["-i", CUR], [], "0:v"
    for k, (nm, _s, aa, bb) in enumerate(chunk, start=1):
        d = bb - aa
        fi, fo = (0.07, 0.22) if nm.startswith("tag") else (0.35, 0.55)
        inputs += ["-itsoffset", "%.4f" % aa,
                   "-loop", "1", "-framerate", str(plan.FPS), "-t", "%.4f" % d,
                   "-i", "/tmp/ov_%s.png" % nm]
        fc.append("[%d:v]format=rgba,fade=in:st=%.3f:d=%.2f:alpha=1,"
                  "fade=out:st=%.3f:d=%.2f:alpha=1[o%d]"
                  % (k, aa, fi, max(aa, bb - fo), fo, k))
        fc.append("[%s][o%d]overlay=0:0:eof_action=pass:enable='between(t,%.3f,%.3f)'[v%d]"
                  % (cur, k, aa, bb, k))
        cur = "v%d" % k
    done_layers += len(chunk)
    last = (done_layers == total_layers)
    out = FINAL if last else stage_out()
    print("слои %d/%d: наложения" % (done_layers, total_layers), flush=True)
    run(["ffmpeg", "-v", "error", "-y"] + inputs +
        ["-filter_complex", ";".join(fc), "-map", "[%s]" % cur] + encode(last) + [out])
    if CUR.startswith("/tmp/stage"):
        os.remove(CUR)
    CUR = out

final = FINAL

dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", final], capture_output=True, text=True).stdout.strip()
print("ГОТОВО:", final, os.path.getsize(final) // 1024, "КБ,", dur, "с")
json.dump({"file": os.path.basename(final), "seconds": float(dur), "frames": plan.NFRAMES,
           "shots": len(plan.SHOTS), "arts": len(set(s[2] for s in plan.SHOTS)),
           "overlays": len(plan.OVERLAYS), "stock": len(STOCK)},
          open(os.path.join(OUT, "report.json"), "w"), ensure_ascii=False, indent=1)
