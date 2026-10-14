#!/usr/bin/env bash
# Send a видеоряд project to the free cloud assembler (first build OR a rebuild
# after you've corrected some scenes).
#
#   ship.sh <project-dir> [queue-name] [--fetch-only]
#
# Modes (auto):
#   FULL AUTO  — project has only <srt> + <narration>: the cloud splits +
#                classifies + fetches + builds, search-only, no library.
#   FROM DASH  — project also has <name>.scenes.json + images/: the cloud
#                skips classification and builds YOUR dashboard as-is.
#   REBUILD    — same as FROM DASH but the cloud reuses last build's clips and
#                only re-renders scenes whose picture changed (keep the SAME
#                queue-name so the clip cache is reused).
#
#   --fetch-only — matrix fetches all web scenes + pop-up photos in parallel,
#                then STOPS before the build. The Release carries the fetched
#                project (images/ + overlays/ + manifest) but no video. Pull it
#                with get.sh, review the dashboard locally, and on «собирай»
#                re-run ship.sh WITHOUT --fetch-only for the actual build.
#                This is the review-gate-safe way to use the cloud (a plain
#                ship.sh runs straight through to a published video).
#
# Result comes back as a GitHub Release named <queue-name>:
#   get.sh <queue-name>            # video + dashboard + QA report + full project
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/config.sh"

fetch_only=0
args=()
for a in "$@"; do
  case "$a" in
    --fetch-only) fetch_only=1 ;;
    *) args+=("$a") ;;
  esac
done
set -- "${args[@]}"

src="${1:?usage: ship.sh <project-dir> [queue-name] [--fetch-only]}"
src="$(cd "$src" && pwd)"
name="${2:-$(basename "$src")}"
name="${name%-cloud}"                       # a pulled project is <name>-cloud

if [ ! -d "$CLOUD_REPO_DIR/.git" ]; then
  echo "cloning cloud repo -> $CLOUD_REPO_DIR"
  git clone "$CLOUD_REPO_URL" "$CLOUD_REPO_DIR"
fi
cd "$CLOUD_REPO_DIR"
git pull --quiet --ff-only || true

dest="queue/$name"
rm -rf "$dest"; mkdir -p "$dest"
shopt -s nullglob

# THE scene file = the *.scenes.json with the most scenes. An audit loop leaves
# scratch files (retry5.scenes.json, r2.scenes.json, fresh.scenes.json …) in the
# project dir; shipping them made the cloud pick a 2-scene retry file and build
# an 8-second stub (2026-09-08). Ship ONLY the real one + overlays_fetch.
scenes_src=""
best=-1
for f in "$src"/*.scenes.json; do
  case "$(basename "$f")" in *overlays_fetch*|*-дашборд*) continue;; esac
  n=$(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1])).get('scenes',[])))" "$f" 2>/dev/null || echo -1)
  if [ "$n" -gt "$best" ]; then best="$n"; scenes_src="$f"; fi
done
[ -n "$scenes_src" ] || { echo "ship.sh: no <niche>.scenes.json in $src"; exit 1; }
echo "scene file: $(basename "$scenes_src")  ($best scenes)"

# inputs the cloud needs — NEVER ship regenerated output or scratch scene files
{ cp "$scenes_src" "$dest/"; }
for f in "$src"/*.srt "$src"/overlays.json \
         "$src"/overlays_fetch.scenes.json "$src"/needs_upload.json; do
  [ -e "$f" ] || continue
  case "$(basename "$f")" in *-дашборд*) continue;; esac
  cp "$f" "$dest/"
done
# ОЗВУЧКА НЕ ОТПРАВЛЯЕТСЯ — НИКОГДА (user, 2026-10-12: «Я озвучку здесь
# накладываю у себя», «если она тебе там не нужна, мне там точно она не
# нужна»). Облаку она не нужна ни для чего: длительность берётся из
# scenes.json, куда scenes_from_srt.py записывает её точно по SRT
# (gap-inclusive, конец последней сцены = конец последней реплики), см.
# narration_duration()/scenes_total_duration() в cloud_pipeline.py. Имя
# выходного файла при отсутствии аудио берётся из SRT.
#
# ПОЧЕМУ ЭТО ВАЖНО, А НЕ ПРОСТО ЭКОНОМИЯ: всё, что попадает в queue/,
# остаётся в ИСТОРИИ git навсегда, даже после «Clear the queue slot».
# Проверено 2026-10-12: в истории облачного репозитория лежат 144 файла
# mp3/wav — голос пользователя ко всем прошлым роликам, включая
# невыпущенные. Если репозиторий когда-нибудь сделают публичным ради
# безлимитных минут Actions, всё это станет общедоступным, и удаление
# релиза задним числом не поможет. Не возвращать этот блок.
# dashboard-picked frames + overlay photos (FROM DASH / REBUILD)
if compgen -G "$src/images/scene_*" >/dev/null; then
  mkdir -p "$dest/images"; cp "$src/images"/scene_* "$dest/images/"
  [ -f "$src/images/.built.json" ] && cp "$src/images/.built.json" "$dest/images/"
  # GitHub рубит файлы >100 МБ и предупреждает на >50. Пиннутый целиком не-
  # индексированный длинный библиотечный клип копируется entire (60-160 МБ).
  # Обрезаем такие до длины сцены прямо в очереди (3-й раз, см. память
  # feedback_ship_to_github_asap). Только видео, только >45 МБ.
  ffm="$(command -v ffmpeg || echo ~/.local/bin/ffmpeg)"
  sc="$scenes_src"
  if [ -n "$sc" ] && [ -x "$ffm" ]; then
    for big in $(find "$dest/images" -name 'scene_*.mp4' -size +45M 2>/dev/null); do
      sid=$(basename "$big" | sed 's/scene_0*//;s/\.mp4//')
      dur=$(python3 -c "import json,sys;d=json.load(open('$sc'));print(next((s['duration_sec'] for s in d['scenes'] if s['id']==$sid),8))" 2>/dev/null || echo 8)
      t=$(python3 -c "print(max(3.0,$dur+1.0))" 2>/dev/null || echo 9)
      "$ffm" -y -ss 1 -i "$big" -t "$t" -an \
        -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30" \
        -c:v libx264 -preset veryfast -crf 22 "$big.trim.mp4" -loglevel error \
        && mv "$big.trim.mp4" "$big" \
        && echo "  обрезал большой клип scene_$sid -> $(du -h "$big" | cut -f1)"
    done
  fi
fi
if compgen -G "$src/overlays/scene_*" >/dev/null; then
  mkdir -p "$dest/overlays"; cp "$src/overlays"/scene_* "$dest/overlays/"
  # НИКОГДА не чинить расхождение overlays.json <-> overlays/*.* здесь
  # молча — раньше (до 2026-09-16) этот блок САМ дописывал "забытые" записи,
  # найдя файл-сироту на диске. Один раз файл-сирота оказался НЕ забытой
  # записью, а всплывашкой, которую пользователь сознательно убрал ✕ на
  # дашборде (drop_overlay чистил JSON, но не удалял фото) — ship.sh увидел
  # сироту и молча вернул её в шипуемый overlays.json, отменив решение
  # пользователя прямо в момент отправки. Баг всплыл только на этапе
  # сборки на GitHub — пользователь в ярости запретил ЛЮБЫЕ проверки/фиксы
  # после ship.sh: "тройную перепроверку делай перед тем как пошлёшь".
  # Теперь: расхождение = ЖЁСТКИЙ СТОП здесь, до пуша, а не тихий патч.
  # (Корень бага уже отдельно починен: drop_overlay в review.py теперь
  # удаляет и сам файл, так что при исправном review.py сирот быть не
  # должно вообще — эта проверка чисто defense-in-depth.)
  if [ -f "$dest/overlays.json" ]; then
    python3 - "$dest" <<'PY'
import json, glob, os, re, sys
dest = sys.argv[1]
ovp = os.path.join(dest, "overlays.json")
ov = json.load(open(ovp, encoding="utf-8"))
have = {k for k in ov if str(k).isdigit() and (ov[k] or {}).get("photo")}
# Файла требуют ТОЛЬКО записи с непустым "photo". Чисто ТЕКСТОВАЯ всплывашка
# ({"text": {...}} без "photo") — штатная фича канала «5 МИНУТ», файл ей не
# нужен; до 2026-10-11 такая запись валила ship.sh как ложную сироту
# (5min-tramp-zelya-1210: 19 текстовых всплывашек -> STOP перед пушем).
on_disk = set()
for f in sorted(glob.glob(os.path.join(dest, "overlays", "scene_*.*"))):
    bn = os.path.basename(f)
    if ".ovthumb." in bn or ".text." in bn:   # review.py's own preview caches
        continue            # (video-thumb + text-overlay render) — not real
                             # overlay assets, false orphan otherwise. .text.
                             # added 2026-10-10 (cross-session report) — only
                             # .ovthumb. was excluded here, same gap selfcheck.py's
                             # own dedup pass already closed for this exact reason.
    m = re.search(r"scene_0*(\d+)\.", bn)
    if m:
        on_disk.add(m.group(1))
orphan_files = sorted(on_disk - have, key=int)   # file exists, no JSON entry
orphan_entries = sorted(have - on_disk, key=int)  # JSON entry, no file
if orphan_files or orphan_entries:
    print("STOP: overlays.json и overlays/*.* разошлись — ship ОТМЕНЁН.")
    if orphan_files:
        print(f"  файлы без записи в overlays.json (сироты): {orphan_files}")
        print("  -> либо это забытая запись (дописать в overlays.json руками),")
        print("     либо пользователь удалил эту всплывашку ✕ и файл просто не")
        print("     удалился (проверить review.py drop_overlay) — удалить файл.")
    if orphan_entries:
        print(f"  записи в overlays.json без файла: {orphan_entries}")
        print("  -> дофетчить фото или убрать запись.")
    print("  Почини в $src (НЕ в очереди), перезапусти ship.sh. Никогда не")
    print("  патчить расхождение здесь и уж тем более после push.")
    sys.exit(1)
PY
  fi
fi
# pop-up sounds — WITHOUT these the sfx step finds nothing and the видеоряд
# ships silent (chernaya-zima, 2026-09-06: had to bake sfx locally after)
if compgen -G "$src/sfx/*" >/dev/null; then
  mkdir -p "$dest/sfx"; cp "$src/sfx"/* "$dest/sfx/" 2>/dev/null || true
fi
# Куда класть готовый видеоряд — помним ЛОКАЛЬНО, в очередь это не отправляем.
# В .source_dir лежит путь к папке пользователя на D: вместе с названием темы
# ролика; в публичном репозитории он уехал бы в релиз и в историю git навсегда.
if [ -f "$src/.source_dir" ]; then
  mkdir -p "$HOME/.cache/videoryad"
  cp "$src/.source_dir" "$HOME/.cache/videoryad/$name.source_dir"
fi
rm -f "$dest/.source_dir"

# catch video-lead drift BEFORE it ships, not after the cloud's QA report —
# a scene approved on the dashboard as video can silently end up a photo on
# disk (source_query asked for video, the fetcher fell back to a photo and
# nobody re-ran the checker). Warn loudly here; not fatal (frozen-dashboard
# rule — don't block a ship over it once the user approved), just visible.
if [ "$fetch_only" != 1 ] && [ -n "$scenes_src" ] && [ -d "$dest/images" ]; then
  python3 "$HOME/.claude/skills/news-video/template/check_lead.py" "$scenes_src" "$dest/images" 2>&1 \
    | sed 's/^/  [видео-лид] /' || true
fi

# review-gate mode: matrix fetches, then stops before the build
if [ "$fetch_only" = 1 ]; then
  echo "fetch-only: облако наберёт кадры на матрице и остановится ДО сборки" > "$dest/.fetch-only"
fi

git add -A "$dest"
if [ "$fetch_only" = 1 ]; then _fo=" (fetch-only)"; else _fo=""; fi
git commit -q --allow-empty -m "queue: $name$_fo"
git push --quiet

repo="${CLOUD_REPO_URL##*github.com[:/]}"; repo="${repo%.git}"
echo
if [ "$fetch_only" = 1 ]; then
  echo "queued: $name  [FETCH-ONLY — сборки не будет, только кадры]"
else
  echo "queued: $name  [FULL BUILD -> видео]"
fi
echo "watch:   gh run list -R $repo --workflow videoryad-cloud.yml"
echo "collect: $here/get.sh $name"
