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

ПЛАНКА — медиана принятого ролика 17-11 честным замером: пусто ≤ 0,12 ·
слоёв ≥ 3,4 · крупный ≥ 980 · средних ≥ 87. ПОЛ (худшие сцены эталона),
ниже него гейт не пустит: пусто ≤ 0,30 · слоёв ≥ 2,0 · крупный ≥ 520 ·
средних ≥ 30.
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
print("%-36s %6s %6s %8s %8s %6s" % ("сцена", "пусто", "слоёв", "крупный", "средних", "пятен"))
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
    if st["pusto_centr"] > .30 or st["sloev_sred"] < 2.0 or sv["krupnyy"] < 520 or sv["srednih"] < 30:
        znak = "  ← НИЖЕ ПОЛА"; hudo += 1
    elif st["pusto_centr"] > .12 or st["sloev_sred"] < 3.4 or sv["krupnyy"] < 980 or sv["srednih"] < 87:
        znak = "  ← ниже планки 17-11"
    print("%-36s %6.2f %6.1f %8d %8d %6d%s"
          % (f, st["pusto_centr"], st["sloev_sred"], sv["krupnyy"], sv["srednih"],
             bbox.pyatna(s), znak))
print("\nсцен: %d · ниже пола: %d" % (len(imena), hudo))
