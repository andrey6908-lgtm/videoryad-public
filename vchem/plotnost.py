# -*- coding: utf-8 -*-
"""ПЛОТНОСТЬ КАДРА ЧИСЛОМ — самопроверка художника.

    python3 plotnost.py                 # все декорации ролика
    python3 plotnost.py <имя> [<имя>…]  # выбранные
    python3 plotnost.py --modul chast1  # порция целиком

Что печатается на каждую сцену:
  пусто    — доля клеток 40x40 в центре кадра, которых не накрыл ни один
             предмет (фон, земля и стена во весь кадр предметом не считаются);
  слоёв    — сколько предметов в среднем приходится на клетку центра;
  крупный  — самый крупный ПРЕДМЕТ (без фона), должен быть от 420 px;
  средних  — предметов 100-420 px, это и есть «сопутствующие вещи».

ПЛАНКА (снята с принятого ролика 17-11): пусто ≤ 0,10 · слоёв ≥ 8 ·
крупный ≥ 600 · средних ≥ 15. ПОЛ, ниже которого гейт не пустит:
пусто ≤ 0,30 · слоёв ≥ 3,0 · крупный ≥ 420 · средних ≥ 8.
"""
import ast, importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bbox

modul = "lok"
argv = sys.argv[1:]
if "--modul" in argv:
    i = argv.index("--modul"); modul = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
M = importlib.import_module(modul)
lok = importlib.import_module("lok")
src = open(os.path.join(HERE, modul + ".py"), encoding="utf-8").read()
imena = argv or [n.name for n in ast.parse(src).body
                 if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]
print("%-36s %6s %6s %8s %8s" % ("сцена", "пусто", "слоёв", "крупный", "средних"))
hudo = 0
for f in imena:
    fn = getattr(M, f, None)
    if fn is None:
        continue
    try:
        s = lok.scena(fn, 2.2)
    except Exception as e:
        print("%-36s падает: %r" % (f, e)); hudo += 1; continue
    st, sv = bbox.setka(s), bbox.svodka(s)
    znak = ""
    if st["pusto_centr"] > .30 or st["sloev_sred"] < 3.0 or sv["krupnyy"] < 420 or sv["srednih"] < 8:
        znak = "  ← НИЖЕ ПОЛА"; hudo += 1
    elif st["pusto_centr"] > .10 or st["sloev_sred"] < 8 or sv["krupnyy"] < 600 or sv["srednih"] < 15:
        znak = "  ← ниже планки 17-11"
    print("%-36s %6.2f %6.1f %8d %8d%s"
          % (f, st["pusto_centr"], st["sloev_sred"], sv["krupnyy"], sv["srednih"], znak))
print("\nсцен: %d · ниже пола: %d" % (len(imena), hudo))
