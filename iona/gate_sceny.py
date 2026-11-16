# -*- coding: utf-8 -*-
"""ГЕЙТ СЦЕН РОЛИКА 2027: его правила 14.11 держит КОД, а не текст.

    python3 gate_sceny.py [имя_функции ...]            # пусто = все декорации плана
    python3 gate_sceny.py --modul chast1               # проверить порцию целиком

Что проверяется у каждой декорации (его слова этого дня):
  1. СТОК ИДЁТ ВНУТРИ СЦЕНЫ, А НЕ ПОВЕРХ (R-0007, R-0003, его слово 14.11:
     «не должны стоковые видео перекрывать наши мультяшные кадры, оно должно
     идти внутри»). Метка проёма обязана быть ВНУТРИ слоя сцены и занимать
     около половины кадра; поверх кадра настоящее видео не кладётся вообще —
     отдельно сверяется, что в kadr.py нет окна-рамки в углу.
  2. СЦЕНА НЕ ПУСТАЯ (R-0045): предметов в кадре много, а не один объект.
  3. ГЛАВНЫЙ ОБЪЕКТ КРУПНЫЙ (R-0047): есть предмет на пол-кадра — иначе он
     не опознаётся с первого взгляда.
  4. ДИНАМИКА И ЖИВОЙ ОГОНЁК (R-0006, его слово: «больше динамики, там дымок,
     где-то лампочка горит, где-то свеча горит»): кадр меняется во времени и
     в сцене есть живой источник — огонь, угли, свеча, лампа, лучина, дым, пар.
  5. СЛОИ ПО ГЛУБИНЕ: не меньше трёх, иначе камера даёт плоское растягивание.
  6. `random` только с семенем, иначе кадр дрожит между вызовами.
"""
import json, os, re, sys, importlib
import bbox

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ZHIVOE = ("ogon(", "ugli(", "svecha(", "lampa(", "luchina(", "dym(", "par(",
          "iskra_let(", "tusklaya_lampochka(", "blink(", "mokryy_sneg(",
          "sneg_letit(", "ptica(", "kot(", "kura(")
# Живой огонёк — именно ЖИВОЙ: `teplo(` отсюда убрано 14.11, это статичное
# пятно света, и сцена без единого язычка пламени проходила проверку.
OGON = ("ogon(", "ugli(", "svecha(", "lampa(", "luchina(", "dym(", "par(",
        "tusklaya_lampochka(", "iskra_let(", "para_izo_rta(", "izba_snaruzhi(",
        "kostyor(", "fonar(")
PREDMET = re.compile(r"<(rect|path|circle|ellipse|line|polygon|polyline|image|text)\b")
_CHISLA = re.compile(r"-?\d+\.?\d*")


def _габарит(svg):
    """Самый крупный предмет кадра по вертикали — грубо, по атрибутам."""
    mx = 0.0
    for m in re.finditer(r'height="(\d+\.?\d*)"', svg):
        mx = max(mx, float(m.group(1)))
    for m in re.finditer(r'ry="(\d+\.?\d*)"', svg):
        mx = max(mx, float(m.group(1)) * 2)
    for m in re.finditer(r'\br="(\d+\.?\d*)"', svg):
        mx = max(mx, float(m.group(1)) * 2)
    # вертикальный размах путей: по координатам после запятых
    for m in re.finditer(r'<path d="([^"]{40,})"', svg):
        ys = [float(v) for v in _CHISLA.findall(m.group(1))][1::2]
        if len(ys) > 2:
            mx = max(mx, max(ys) - min(ys))
    return mx


def сток_нужен():
    pl = json.load(open(os.path.join(HERE, "plany.json"), encoding="utf-8"))
    karta = importlib.import_module("karta").DEK
    out = {}
    for p in pl:
        s = (p.get("stok") or "").strip().lower()
        if s and s not in ("нет", "не нужно", "-", "убрано"):
            out.setdefault(karta[p["lok"]], []).append(p["n"])
    return out


def main():
    import ast
    argv = sys.argv[1:]
    modul = "lok"
    if "--modul" in argv:
        i = argv.index("--modul")
        modul = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    lok = importlib.import_module(modul)
    src = open(os.path.join(HERE, modul + ".py"), encoding="utf-8").read()
    tela = {n.name: ast.get_source_segment(src, n) or ""
            for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}
    karta = importlib.import_module("karta").DEK
    pl = json.load(open(os.path.join(HERE, "plany.json"), encoding="utf-8"))
    vse = sorted({karta[p["lok"]] for p in pl})
    if argv:
        nado = argv
    elif modul == "lok":
        nado = vse
    else:                      # порция: проверяем только то, что в ней есть
        nado = [f for f in vse if getattr(lok, f, None) is not None
                and f in {n.name for n in ast.parse(src).body
                          if isinstance(n, ast.FunctionDef)}]
    so_stokom = сток_нужен()
    плохо = {}
    podskazki = []

    # общий гейт сборки: настоящее видео НЕ кладётся поверх сцены
    kadr_src = open(os.path.join(HERE, "kadr.py"), encoding="utf-8").read()
    _ = modul
    if "okno_foto" in kadr_src or "okno_ramka" in kadr_src:
        print("ГЕЙТ: kadr.py снова кладёт сток окном поверх сцены (R-0007)")
        return 1

    for imya in nado:
        bed = []
        fn = getattr(lok, imya, None)
        if fn is None:
            плохо[imya] = ["декорации нет в lok.py"]
            continue
        telo = tela.get(imya, "")
        try:
            a = fn(1.0)
            b = fn(2.4)
        except Exception as e:
            плохо[imya] = ["падает: %r" % (e,)]
            continue
        if len(a) < 1500:
            bed.append("пусто: %d символов (норма от 1500)" % len(a))
        n_pred = len(PREDMET.findall(a))
        if n_pred < 60:
            bed.append("предметов в кадре %d (норма от 60, R-0045)" % n_pred)
        # КРУПНЫЙ ПРЕДМЕТ СЧИТАЕМ БЕЗ ФОНА (15.11): полоса земли или стена во
        # весь кадр предметом не является — ею закрывали норму R-0047, и сцена
        # с фигуркой на пустом поле проходила гейт.
        sv = bbox.svodka(a)
        if sv["krupnyy"] < 520:
            bed.append("нет предмета на пол-кадра: самый крупный %d px без фона (пол 520, R-0047)"
                       % sv["krupnyy"])
        if sv["srednih"] < 30:
            bed.append("предметов среднего плана %d (пол 30, R-0045)" % sv["srednih"])
        # ПУСТОТА В ЦЕНТРЕ И ПЛОТНОСТЬ — пороги сняты с принятого ролика 17-11
        # (там медиана пусто 0,04 и слоёв 9,9; здесь порог с запасом).
        st = bbox.setka(a)
        # Пороги — это ПОЛ, а не планка: сняты с принятого ролика 17-11
        # ЧЕСТНЫМ замером (после починки габарита путей 15.11): медиана
        # пусто 0,12 · слоёв 3,4 · крупный 980 · средних 87; худшие сцены
        # 0,30 · 2,0 · 528 · 33 — они и стали полом. Планка в задании
        # художнику — медиана эталона.
        if st["pusto_centr"] > .30:
            bed.append("центр кадра пустой: %d%% клеток без предметов (пол 30%%, R-0045)"
                       % round(st["pusto_centr"] * 100))
        if st["sloev_sred"] < 2.0:
            bed.append("кадр жидкий: в центре %.1f предмета на клетку (пол 2,0, R-0045/R-0047)"
                       % st["sloev_sred"])
        # ДВОЙНАЯ ОБЁРТКА СЛОЯ: вложенный <g data-z> не разъезжается своей
        # глубиной — камера считает его частью родителя, и объём пропадает.
        # Ловится только счётом вложенности (часть 2 принесла 44 таких места).
        гл, maxгл = 0, 0
        for m in re.finditer(r'<g data-z="(?:-?\d+|fix)">|<!--/z-->', a):
            if m.group(0).startswith("<g"):
                гл += 1
                maxгл = max(maxгл, гл)
            else:
                гл = max(0, гл - 1)
        if maxгл > 1:
            bed.append("слой внутри слоя (SL в SL) — объём пропадает")
        сл = set(re.findall(r'<g data-z="(-?\d+|fix)">', a))
        if len(сл) < 3:
            bed.append("слоёв по глубине %d (норма от 3)" % len(сл))
        if a == b:
            bed.append("кадр НЕ ЖИВЁТ: вывод на 1,0 и 2,4 с одинаков (R-0006)")
        else:
            разн = sum(1 for x, y in zip(_CHISLA.findall(a), _CHISLA.findall(b)) if x != y)
            if разн < 8:
                bed.append("динамики мало: меняется %d чисел (норма от 8, R-0006)" % разн)
        if not any(k in telo for k in OGON):
            bed.append("нет живого огонька: ни огня, ни свечи, ни лампы, ни дыма (R-0006)")
        if not any(k in telo for k in ZHIVOE):
            bed.append("нет ни одного живого кирпичика (R-0006)")
        if "random.random()" in telo and "random.Random(" not in telo:
            bed.append("random без семени — кадр дрожит между вызовами")
        if imya in so_stokom:
            m = re.search(r'<g data-stok="([^"]*)"></g>', a)
            if not m:
                bed.append("СТОКА НЕГДЕ ПОСТАВИТЬ: нет метки mesto_stoka, планы %s"
                           % so_stokom[imya])
            else:
                ч = m.group(1).split(",")
                w_, h_, forma = float(ч[2]), float(ч[3]), (ч[4] if len(ч) > 4 else "pryam")
                порог = 360 if forma == "ellips" else 760
                if w_ < порог:
                    bed.append("проём под сток мал: %d px (норма от %d, R-0024)" % (w_, порог))
                if h_ < 300:
                    bed.append("проём под сток низкий: %d px (норма от 300)" % h_)
                x_, y_ = float(ч[0]), float(ч[1])
                if x_ < -40 or y_ < -40 or x_ + w_ > 1960 or y_ + h_ > 1120:
                    bed.append("проём под сток уехал за холст: %d,%d %dx%d"
                               % (x_, y_, w_, h_))
                до = a[:m.start()]
                if до.count('<g data-z="') <= до.count("<!--/z-->"):
                    bed.append("метка стока СНАРУЖИ слоя сцены — сток поедет "
                               "отдельно от кадра (R-0007/R-0016)")
                # НЕ ГЕЙТ, А ПОДСКАЗКА: передний план перед проёмом (створки,
                # колонны, ветки, огонь поверх клипа) — норма, его не убирают.
                # Машиной от «чашки в самом окне» не отличить, поэтому только
                # печатаем и смотрим глазами (прогон по 17-11: 10 из 15 проёмов
                # «грязные», и почти все ложные).
                svoi = bbox.v_proeme(a, (x_, y_, w_, h_))
                if svoi:
                    podskazki.append("%s: в двух третях проёма лежат наши предметы (%d шт) "
                                     "— посмотреть глазами, не спорят ли с кадром" % (imya, len(svoi)))
        elif 'data-stok' in a:
            bed.append("лишняя метка стока: по раскадровке стока в этой сцене нет")
        if bed:
            плохо[imya] = bed

    if podskazki:
        print("ПОСМОТРЕТЬ ГЛАЗАМИ (не брак, подсказка):")
        for p in podskazki:
            print("   · %s" % p)
    print("проверено декораций: %d" % len(nado))
    if not плохо:
        print("ВСЁ ЧИСТО: сток внутри сцены, сцены не пустые, динамика есть")
        return 0
    print("НЕ ПРОХОДЯТ %d декораций:" % len(плохо))
    for imya in sorted(плохо):
        print("  %s" % imya)
        for b in плохо[imya]:
            print("      · %s" % b)
    return 1


if __name__ == "__main__":
    sys.exit(main())
