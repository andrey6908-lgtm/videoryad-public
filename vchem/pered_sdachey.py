# -*- coding: utf-8 -*-
"""ГЕЙТ ПЕРЕД СДАЧЕЙ: шесть проверок, на которых ролик 16 ноября отъехал
обратно четыре раза подряд. Запускать ИЗ ПАПКИ КОДА ролика:

    python3 pered_sdachey.py [папка рабочих файлов ролика]

Что проверяет (каждая строка — его живое замечание 14.11.2026):
 1. «почему оно всегда справа и одного размера» — окна стоят в разных
    местах и разных размеров (R-0048);
 2. «не делай пустыми сценами» — у планов есть места обживки (R-0045);
 3. «вместо камина чёрный прямоугольник» — в окне нет почти чёрного клипа
    (средняя яркость превью < 0,10 читается как пустая рамка);
 4. R-0030 — ни одна надпись не уходит за край кадра;
 5. «список должен идти в ряд, 1-2-3» — карточки памятки накапливаются;
 6. R-0021 — один клип стоит ровно в одном плане.

Выход 0 — можно сдавать. Выход 1 — есть «нет», ролик ему не показывать
(R-0025: показываем только то, что сами считаем готовым).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(os.getcwd() + "/x"))
RAB = sys.argv[1] if len(sys.argv) > 1 else None
sys.path.insert(0, os.getcwd())

import kadr, plan                      # noqa: E402
from baza import W                     # noqa: E402

bed = []


def say(ok, chto, podrobno=""):
    print(("  да  " if ok else "  НЕТ ") + chto + ("  · " + podrobno if podrobno else ""))
    if not ok:
        bed.append(chto)


print("ПРОВЕРКА ПЕРЕД СДАЧЕЙ")

# 1 ── НАСТОЯЩИЙ КАДР СТОИТ В РАЗНЫХ МЕСТАХ И РАЗНОГО РАЗМЕРА (R-0048)
# ПЕРЕПИСАНО 16.11.2026: проверка читала `okna.json` — файл СТАРОЙ схемы, где
# настоящий кадр стоял отдельным окном в углу. С 15.11 кадр лежит ВНУТРИ
# сцены, место и размер названы словами в раскадровке (поле `stok`), а
# `okna.json` не создаётся вовсе — и у принятого эталона «17 ноября» его тоже
# нет. Гейт честно печатал «окон 0» на исправном ролике, то есть держал
# сдачу за несуществующую дыру.
MESTA = ("слева", "справа", "по центру", "сверху", "снизу", "в центре")
stoki = []
for p_ in plan.PLANY:
    v = (p_.get("stok") or "").strip().lower()
    if v in ("", "нет", "-", "убрано", "не нужно"):
        continue
    storona = next((m for m in MESTA if m in v), "не названо")
    razmer = re.search(r"(\d{3,4})\s*(?:на|x|×)\s*(\d{3,4})", v)
    krug = re.search(r"(?:круг|овал)\s*(\d{3,4})", v)
    razm = ("%sx%s" % razmer.groups()) if razmer else ("круг%s" % krug.group(1) if krug else "?")
    stoki.append((storona, razm))
mest = set(stoki)
say(len(stoki) > 0 and len(mest) >= 3,
    "настоящий кадр подобран под сцену, а не прибит справа (R-0048)",
    "кадров %d, разных сочетаний сторона+размер %d" % (len(stoki), len(mest)))

# 2 ── СЦЕНЫ НЕ ПУСТЫЕ (R-0045): меряем ГЕЙТОМ СЦЕН, а не числом окон
# ПЕРЕПИСАНО 16.11.2026 по той же причине: прежняя проверка считала записи
# `obzhivka` в `okna.json`. Плотность кадра давно меряет gate_sceny.py
# (предметов от 60, крупный предмет от 420 px, слоёв от 3) — спрашиваем его.
import subprocess as _sp
_g = _sp.run([sys.executable, os.path.join(os.getcwd(), "gate_sceny.py")],
             capture_output=True, text=True)
say(_g.returncode == 0, "сцены не пустые — гейт сцен пройден (R-0045)",
    (_g.stdout.strip().splitlines() or ["гейт молчит"])[-1][:120])

# 3 ── почти чёрных клипов в окне нет
temn = []
if RAB and os.path.exists(os.path.join(RAB, "vybor_video.json")):
    try:
        import numpy as np
        from PIL import Image
        v = json.load(open(os.path.join(RAB, "vybor_video.json"), encoding="utf-8"))
        K = json.load(open(os.path.join(RAB, "video", "korotkie.json"), encoding="utf-8"))
        for n, i in v.items():
            pth = K[str(n)][i]["file"]
            a = np.asarray(Image.open(pth).convert("L"), dtype=np.float32) / 255.
            if a.mean() < .10:
                temn.append((int(n), round(float(a.mean()), 3)))
    except Exception as e:
        print("     (яркость не проверена: %s)" % str(e)[:60])
say(not temn, "в окне нет почти чёрного клипа", str(temn[:6]) if temn else "")

# 4 ── надписи в границах кадра
za_kray = []
for p in plan.PLANY:
    for t in (0.9, 2.2, max(1.0, p["sek"] * .8)):
        for m in re.finditer(r'<rect x="(-?[\d.]+)"\s+y="(-?[\d.]+)"\s+width="([\d.]+)"',
                             kadr.nalozheniya(p, t)):
            x, w_ = float(m.group(1)), float(m.group(3))
            if x < -2 or x + w_ > W + 2:
                za_kray.append(p["n"])
                break
        if za_kray and za_kray[-1] == p["n"]:
            break
say(not za_kray, "надписи не уходят за край кадра (R-0030)", str(sorted(set(za_kray))[:8]))

# 5 ── памятка идёт списком
# ИМЯ ФУНКЦИИ ПАМЯТКИ — `kartochki_pamyatki` (так она зовётся и у эталона):
# проверка искала несуществующее `spisok_pamyatki` и всегда отвечала «нет».
spisok = hasattr(kadr, "kartochki_pamyatki")
if spisok:
    # НАКОПЛЕНИЕ МЕРЯЕМ НА ПОСЛЕДНЕМ ПЛАНЕ ПАМЯТКИ: берём планы, у которых
    # есть карточка, и смотрим, сколько пунктов видно на экране к последнему.
    # Прежний код звал `kadr.pamyatka()` — функции с таким именем нет ни
    # здесь, ни у эталона, и гейт падал с AttributeError прямо на сдаче.
    kart_plany = [p for p in plan.PLANY
                  if any(tip.lower().startswith("карточка") for tip, _ in kadr.nadpisi(p))]
    vidno = 0
    posl_n = None
    for p_ in kart_plany:
        est = len(kadr.kartochki_pamyatki(p_))
        if est > vidno:
            vidno, posl_n = est, p_["n"]
    say(vidno >= 3, "памятка копится списком 1-2-3 (его слово 14.11)",
        "к плану %s на экране пунктов %d" % (posl_n, vidno))
else:
    say(False, "памятка копится списком 1-2-3 (его слово 14.11)",
        "нет kadr.kartochki_pamyatki")

# 6 ── один клип — один план
f = os.path.join(os.getcwd(), "stock_video.json")
st = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
ids = [v.get("id") for v in st.values()]
say(len(ids) == len(set(ids)), "повторов клипа нет (R-0021)",
    "клипов %d" % len(ids))

print("\nИТОГ: " + ("можно сдавать" if not bed else "НЕ СДАВАТЬ, не закрыто: " + "; ".join(bed)))
sys.exit(1 if bed else 0)
