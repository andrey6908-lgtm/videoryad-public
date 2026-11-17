# -*- coding: utf-8 -*-
"""СКЛЕЙКА lok.py из частей.

Декорации пишутся порциями (`chast1.py`, `chast2.py`, `chast3.py`), сквозные
образы ролика лежат в `lok_obshchee.py`. Здесь всё сводится в ОДИН `lok.py`:
так гейт заимствований (`svoi_kadry.py`) видит настоящие тела функций, а не
звёздочный импорт, и Питон не берёт «последнее определение» из двух файлов.

    python3 sobrat_lok.py            # собрать и проверить запуском
"""
import ast, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHASTI = ["lok_obshchee.py", "chast1.py", "chast2.py", "chast3.py"]
SHAPKA = '''# -*- coding: utf-8 -*-
"""100 декораций ролика «Что дарить на Новый год 2027».

Каждая — функция времени f(t) -> svg. Все нарисованы ЗАНОВО под этот текст
(R-0019): ни один кадр не взят у прошлых роликов проекта 2027.
Его правила 15.11 (вечерняя редакция): настоящий кадр лежит ВНУТРИ сцены (метка mesto_stoka),
сцены не пустые, предметы узнаваемые, в каждой сцене живой огонёк.

СОБИРАЕТСЯ sobrat_lok.py из частей — руками этот файл не правят.
"""
import math, random
from baza import *
import anim as A

'''
# где в кадре горит источник: блик в объектив ставим только туда
ISTOCHNIK = re.compile(r"\b(ogon|svecha|lampa|luchina|ugli|kostyor|tusklaya_lampochka)"
                       r"\(\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)")


def telo_bez_shapki(put):
    src = open(put, encoding="utf-8").read()
    derevo = ast.parse(src)
    defs = [n for n in derevo.body if isinstance(n, (ast.FunctionDef, ast.Assign))]
    if not defs:
        return "", []
    stroki = src.split("\n")
    nach = defs[0].lineno - 1
    # декоратор или комментарий-шапка над первой функцией
    kus = "\n".join(stroki[nach:]).rstrip() + "\n"
    imena = [n.name for n in derevo.body if isinstance(n, ast.FunctionDef)]
    return kus, imena


def main():
    kuski, vse = [], []
    for ch in CHASTI:
        p = os.path.join(HERE, ch)
        if not os.path.exists(p):
            print("нет части: %s — собираю из того, что есть" % ch)
            continue
        k, imena = telo_bez_shapki(p)
        kuski.append("# ═══ из %s ═══\n%s" % (ch, k))
        vse += imena
    dubl = sorted({i for i in vse if vse.count(i) > 1})
    if dubl:
        print("ОДНО ИМЯ В ДВУХ ЧАСТЯХ (Питон возьмёт последнее): %s" % ", ".join(dubl))
        return 1
    src = SHAPKA + "\n\n".join(kuski)
    # блики в объектив — по первому источнику света каждой сцены
    bl = {}
    for n in ast.parse(src).body:
        if not isinstance(n, ast.FunctionDef):
            continue
        kus = ast.get_source_segment(src, n) or ""
        m = ISTOCHNIK.search(kus)
        if m:
            bl[n.name] = (int(float(m.group(2))), int(float(m.group(3))))
    src += "\n\n# источники света сцен: сюда ставится блик в объектив (C16/K17)\nBLIKI = {\n"
    for k in sorted(bl):
        src += '    "%s": (%d, %d),\n' % (k, bl[k][0], bl[k][1])
    src += "}\n"
    open(os.path.join(HERE, "lok.py"), "w", encoding="utf-8").write(src)
    print("lok.py собран: %d функций, из них декораций с бликом %d, %d КБ"
          % (len(vse), len(bl), len(src) // 1024))
    # проверка запуском
    sys.path.insert(0, HERE)
    import importlib
    lok = importlib.import_module("lok")
    plohо = []
    for imya in vse:
        try:
            s = getattr(lok, imya)(2.2)
            if not isinstance(s, str):
                plohо.append((imya, "вернула не строку"))
        except TypeError:
            pass                      # кирпичик с другими ключами — не декорация
        except Exception as e:
            plohо.append((imya, repr(e)))
    if plohо:
        print("ПАДАЮТ %d функций:" % len(plohо))
        for i, e in plohо[:20]:
            print("   %-28s %s" % (i, e))
        return 1
    print("все функции считаются")
    return 0


if __name__ == "__main__":
    sys.exit(main())
