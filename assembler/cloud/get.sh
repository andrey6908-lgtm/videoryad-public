#!/usr/bin/env bash
# Collect a finished видеоряд from the cloud + unpack the full project so you
# can review it locally (review.py) and, if something's off, correct scenes
# and re-ship for a fast partial rebuild.
#
#   get.sh <queue-name> [dest-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/config.sh"

name="${1:?usage: get.sh <queue-name> [dest-dir]}"
dest="${2:-$HOME/projects/$name-cloud}"
repo="${CLOUD_REPO_URL##*github.com[:/]}"; repo="${repo%.git}"

mkdir -p "$dest"
gh release download "$name" -R "$repo" -D "$dest" --clobber

# unpack the full project (scenes.json + images/ + overlays/ + sfx/ + narration)
if [ -f "$dest/$name-project.tgz" ]; then
  tar xzf "$dest/$name-project.tgz" -C "$dest" --strip-components=1
  rm -f "$dest/$name-project.tgz"
  # the loose Release assets are a fallback; the tgz has them all with proper
  # (non-mangled) names, so drop the duplicates GitHub renamed on upload
  rm -f "$dest"/*.-.-.mp4 "$dest"/*.scenes-.html \
        "$dest/QA-report.md" "$dest/pipeline.log" "$dest/report.json" \
        "$dest/classify_report.md"
fi

vid=$(ls "$dest"/*ВИДЕОРЯД.mp4 2>/dev/null | head -1 || true)
[ -n "$vid" ] && echo "видео: $vid"

# ПУБЛИЧНЫЙ репозиторий (аккаунт rezerv): релиз открыт всему интернету, поэтому
# удаляем его сразу, как только видеоряд скачан — ссылка живёт минуты, а не
# навсегда. У приватных аккаунтов релиз остаётся как страховка на случай, если
# скачивание оборвалось. Проект при этом уже распакован в $dest.
if [ "${VIDEORYAD_PUBLIC:-0}" = 1 ] && [ -n "$vid" ] && [ -s "$vid" ]; then
  gh release delete "$name" -R "$repo" -y --cleanup-tag >/dev/null 2>&1 \
    && echo "релиз удалён с публичного репозитория (видеоряд уже здесь)" \
    || echo "ВНИМАНИЕ: релиз $name на публичном репозитории удалить не удалось — убери вручную"
fi

if [ -f "$dest/.fetch-only" ]; then
  rm -f "$dest/.fetch-only"
  n_img=$(ls "$dest"/images/scene_* 2>/dev/null | wc -l || true)
  n_ov=$(ls "$dest"/overlays/scene_* 2>/dev/null | wc -l || true)
  echo
  echo "================================================================"
  echo "  FETCH-ONLY: кадры с матрицы получены (сцен $n_img, всплывашек $n_ov)"
  echo "  видео ещё НЕТ — сборка не запускалась (ревью-гейт)"
  echo "================================================================"
  echo "  дашборд:  cd \"$dest\" && python3 $here/../template/review.py --live *.scenes.json images 8790"
  echo "  «собирай» -> $here/ship.sh \"$dest\" $name        (без --fetch-only)"
  echo
  exit 0
fi

echo
echo "готово: $dest"
echo
echo "== посмотреть QA-отчёт (что могло пойти не так) =="
echo "   cat \"$dest/_cloud/QA-report.md\""
echo
echo "== открыть дашборд для правок (как всегда) =="
echo "   cd \"$dest\" && python3 $here/../template/review.py --live *.scenes.json images 8790"
echo "   -> http://localhost:8790/review.html"
echo
echo "== поправил сцены -> отправить на пересборку (тем же именем!) =="
echo "   $here/ship.sh \"$dest\" $name"
