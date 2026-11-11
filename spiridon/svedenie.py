# -*- coding: utf-8 -*-
"""СВЕДЁННАЯ РАСКАДРОВКА: 99 планов картинками + страница для просмотра.
Видео не собирается — это предпросмотр, по которому он правит до сборки."""
import os, sys, json, html
import cairosvg
import kadr, baza

HERE = os.path.dirname(os.path.abspath(__file__))


def risuy(out_dir, shir=960, tolko=None):
    os.makedirs(os.path.join(out_dir, "kadry"), exist_ok=True)
    P = kadr.plany()
    for pl in P:
        if tolko and pl["n"] not in tolko:
            continue
        t = min(pl["sek"] * .62, 3.2)
        svg = kadr.body(pl, t, .62)
        cairosvg.svg2png(bytestring=svg.encode(),
                         write_to=os.path.join(out_dir, "kadry", f"{pl['n']:03d}.png"),
                         output_width=shir, output_height=int(shir * baza.H / baza.W),
                         unsafe=True)
    return P


def mmss(x):
    return f"{int(x)//60}:{x-60*(int(x)//60):04.1f}"


def stranica(out_dir, P):
    blocks = {}
    for pl in P:
        blocks.setdefault(pl["blok"], []).append(pl)
    e = html.escape
    total = P[-1]["tab"] + P[-1]["sek"]
    okon = sum(1 for p in P if kadr.nado_okno(p))
    h = f"""<!doctype html><meta charset="utf-8">
<title>13 ноября — Спиридон и Никодим · сведённая раскадровка</title>
<style>
:root{{--fon:#17140f;--kart:#221d16;--ram:#3b3127;--zol:#d6a63f;--krem:#efe3c8;--sero:#9a9182}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--fon);color:var(--krem);
 font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}
header{{position:sticky;top:0;z-index:9;background:#0f0d0a;border-bottom:3px solid var(--zol);
 padding:14px 24px;display:flex;gap:28px;align-items:baseline;flex-wrap:wrap}}
h1{{font:700 22px/1.2 Georgia,serif;margin:0;color:var(--zol)}}
.svod{{color:var(--sero);font-size:13px}}
.svod b{{color:var(--krem)}}
nav{{padding:10px 24px;background:#1b1813;display:flex;gap:10px;flex-wrap:wrap}}
nav a{{color:var(--krem);text-decoration:none;border:1px solid var(--ram);
 padding:4px 12px;border-radius:14px;font-size:13px}}
nav a:hover{{border-color:var(--zol);color:var(--zol)}}
h2{{margin:36px 24px 10px;font:700 19px/1.2 Georgia,serif;color:var(--zol);
 border-bottom:1px solid var(--ram);padding-bottom:8px}}
.setka{{display:grid;grid-template-columns:repeat(auto-fill,minmax(440px,1fr));
 gap:18px;padding:0 24px}}
.plan{{background:var(--kart);border:1px solid var(--ram);border-radius:12px;overflow:hidden}}
.plan img{{width:100%;display:block;background:#000}}
.shapka{{display:flex;gap:10px;align-items:baseline;padding:10px 14px 6px}}
.nom{{background:var(--zol);color:#1a1208;font-weight:700;border-radius:6px;
 padding:1px 9px;font-size:14px}}
.vrem{{color:var(--sero);font-size:13px;font-variant-numeric:tabular-nums}}
.rech{{padding:0 14px 10px;font-size:14px;color:#fff}}
.rech i{{color:var(--zol);font-style:normal}}
dl{{margin:0;padding:0 14px 14px;font-size:13px;color:var(--sero)}}
dt{{color:#c3b79c;font-weight:600;margin-top:7px;font-size:12px;letter-spacing:.4px;
 text-transform:uppercase}}
dd{{margin:2px 0 0}}
.sred{{color:#9fc48f;font-size:12px}}
.okno{{color:#8fd0e8}} .titr{{color:#f0c96a}} .prav{{color:#7fa87f;font-size:12px}}
@media(max-width:560px){{.setka{{grid-template-columns:1fr;padding:0 12px}}
 header{{padding:10px 12px}} h2{{margin:24px 12px 8px}}}}
</style>
<header><h1>13 ноября — Спиридон и Никодим</h1>
<div class="svod">сведённая раскадровка · <b>{len(P)}</b> планов ·
 хронометраж <b>{mmss(total)}</b> · озвучка <b>10:51.5</b> ·
 окно вставки в <b>{okon}</b> планах · декораций <b>{len({p['lok'] for p in P})}</b></div>
<div class="svod">кадр рисованный, сток и портреты — только в окне справа</div></header>
<nav>""" + "".join(
        f'<a href="#b{i}">{e(b)}</a>' for i, b in enumerate(blocks)) + "</nav>"

    for i, (b, pls) in enumerate(blocks.items()):
        h += f'<h2 id="b{i}">{e(b)} · {len(pls)} планов</h2><div class="setka">'
        for pl in pls:
            okno = (f'<dt>окно справа</dt><dd class="okno">{e(pl["okno"])}<br>'
                    f'<small>запрос: {e(pl["najti"])}</small></dd>'
                    if kadr.nado_okno(pl) else '<dt>окно</dt><dd>убрано</dd>')
            titr = (f'<dt>надписи</dt><dd class="titr">{e(pl["titr"])}</dd>'
                    if pl["titr"].strip() and pl["titr"] != "нет" else "")
            h += f"""<div class="plan" id="p{pl['n']}">
<img src="kadry/{pl['n']:03d}.png" loading="lazy" alt="план {pl['n']}">
<div class="shapka"><span class="nom">{pl['n']}</span>
<span class="vrem">{mmss(pl['tab'])} → {mmss(pl['tab']+pl['sek'])} · {pl['sek']:.1f} с</span></div>
<div class="rech"><i>«{e(pl['yakor'])}…»</i> {e(pl['text'][len(pl['yakor']):].strip())}</div>
<dl><dt>декорация</dt><dd>{e(pl['lok'])}</dd>
<dt>в кадре</dt><dd>{e(pl['kadr'])}</dd>
<dt>живое</dt><dd>{e(pl['zhiv'])}</dd>
<dt>камера</dt><dd>{e(pl['kam'])}</dd>
<dt>средства библиотеки</dt><dd class="sred">{e(" · ".join(kadr.sredstva(pl)))}</dd>
{okno}{titr}
<dt>звук</dt><dd>{e(pl['zvuk'])}</dd>
<dd class="prav">{e(pl['prav'])}</dd></dl></div>"""
        h += "</div>"
    h += '<div style="height:60px"></div>'
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(h)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    P = risuy(out)
    stranica(out, P)
    print("готово:", os.path.join(out, "index.html"))
