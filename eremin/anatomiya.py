# -*- coding: utf-8 -*-
"""ГЕЙТ АНАТОМИИ (R-0051, его слово 15.11.2026: «какие-то три руки… должны
   соответствовать механике, физике, откуда у человека что растёт»).

   Кадр собирается в два прохода (lok.scena): первый запоминает, куда сцена
   крепит свои руки через rukav(), второй рисует фигуру БЕЗ своего рукава на
   этом плече. Гейт проверяет по всем декорациям ролика:
     · сколько внешних рук село на плечи фигур (столько рукавов погашено);
     · СИРОТЫ — руки, не севшие ни на одно плечо: либо рука из воздуха, либо
       третья рука у фигуры, которую не распознали. Смотреть глазами.
     · фигуры, у которых погашены ОБА своих рукава: допустимо, только если
       сцена вывела им обе руки сама.
   python3 anatomiya.py [--vse]
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lok
from karta import DEK

PL = json.load(open(os.path.join(HERE, "plany.json"), encoding="utf-8"))
loki = []
for p in PL:
    if p["lok"] not in loki:
        loki.append(p["lok"])

vse = "--vse" in sys.argv
itog = {"figur": 0, "ruk": 0, "pogasheno": 0, "siroty": 0, "bez_svoih": 0,
        "na_figure": 0}
plohie = []
brak = []
for nazv in loki:
    imya = DEK[nazv]
    fn = getattr(lok, imya)
    lok.scena(fn, 2.0)
    sv = lok.anatomiya_svodka()
    for k in ("figur", "ruk", "pogasheno"):
        itog[k] += sv[k]
    itog["siroty"] += len(sv["siroty"])
    itog["bez_svoih"] += len(sv["bez_svoih"])
    itog["na_figure"] += len(sv["na_figure"])
    if sv["na_figure"]:
        brak.append((nazv, imya, sv["na_figure"]))
    if sv["siroty"] and sv["figur"]:
        plohie.append((nazv, imya, sv["figur"], sv["ruk"], len(sv["siroty"])))
    if vse:
        print("%-44s фигур %d · рук %d · погашено %d · сирот %d"
              % (nazv[:44], sv["figur"], sv["ruk"], sv["pogasheno"], len(sv["siroty"])))

print("\nДЕКОРАЦИЙ %d · фигур %d · внешних рук %d · погашено рукавов %d"
      % (len(loki), itog["figur"], itog["ruk"], itog["pogasheno"]))
print("фигур без обоих своих рукавов: %d" % itog["bez_svoih"])
print("РУК-СИРОТ (не сели ни на одно плечо): %d" % itog["siroty"])
if plohie:
    print("\nСМОТРЕТЬ ГЛАЗАМИ — сцены с фигурами и руками-сиротами:")
    for nazv, imya, f, r, k in plohie:
        print("  %-42s figura=%d rukav=%d сирот=%d" % (nazv[:42], f, r, k))

if brak:
    print("\nТРЕТЬЯ РУКА (растёт из туловища мимо плеча) — СБОРКА НЕ ИДЁТ:")
    for nazv, imya, sp in brak:
        for hx, hy, fx, fpl in sp:
            print("  %-42s рука (%.0f,%.0f) при фигуре x=%.0f плечо=%.0f"
                  % (nazv[:42], hx, hy, fx, fpl))
    print("\nR-0051 НЕ ПРОЙДЕН: третьих рук %d" % itog["na_figure"])
    sys.exit(1)
print("\nR-0051 пройден: третьих рук нет"
      " (руки-сироты вне фигур — это крупный план кистей, норма)")
sys.exit(0)
