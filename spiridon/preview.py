# -*- coding: utf-8 -*-
"""Кадр декорации в PNG — смотреть глазами ДО облака (правило 4 скилла)."""
import sys, os, io
import cairosvg
import lok, baza

HERE = os.path.dirname(os.path.abspath(__file__))


def svg_doc(body, w=baza.W, h=baza.H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"'
            f' viewBox="0 0 {baza.W} {baza.H}"><defs>{baza.defs()}</defs>{body}</svg>')


def png(name, t, out, w=640):
    body = getattr(lok, name)(t)
    cairosvg.svg2png(bytestring=svg_doc(body).encode(), write_to=out,
                     output_width=w, output_height=int(w * baza.H / baza.W))


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    names = sys.argv[2:] or [n for n in dir(lok) if not n.startswith("_")]
    import inspect
    names = [n for n in names if inspect.isfunction(getattr(lok, n, None))
             and getattr(lok, n).__module__ == "lok"]
    for n in names:
        png(n, 2.4, os.path.join(out, n + ".png"))
        print(n)
