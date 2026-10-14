#!/usr/bin/env bash
# One command: try the cloud, fall straight back to a local build if the
# cloud stalls, bans, errors or is just slow. The cloud is NEVER a single
# point of failure — a bad run here just means "build it the old way".
#
#   run.sh <project-dir> [queue-name] [--timeout MIN] [--fetch-only]   (default 55)
#
# Success  -> pulls the result with get.sh, prints where it is.
# --fetch-only -> the matrix fetches the web scenes + pop-up photos in parallel
#                 and the workflow STOPS before the build; this pulls the
#                 fetched project and prints the LOCAL dashboard command. Review
#                 the gate locally, then `ship.sh <dir> <name>` for the real
#                 build. The review-gate-safe way to use the cloud.
# Any snag -> prints a loud banner, kicks off the LOCAL fetch + dashboard
#             (old templates, old rules) and exits 2 so the session switches
#             over immediately.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
skill="$(cd "$here/.." && pwd)"
source "$here/config.sh"

fetch_only=0; pos=(); _t=0; tmin=""
for a in "$@"; do
  if [ "$_t" = 1 ]; then tmin="$a"; _t=0; continue; fi
  case "$a" in
    --timeout)    _t=1 ;;
    --fetch-only) fetch_only=1 ;;
    *)            pos+=("$a") ;;
  esac
done
set -- "${pos[@]}"

src="${1:?usage: run.sh <project-dir> [queue-name] [--timeout MIN] [--fetch-only]}"
src="$(cd "$src" && pwd)"
name="${2:-$(basename "$src")}"; name="${name%-cloud}"
[ -n "$tmin" ] || { tmin=55; [ "$fetch_only" = 1 ] && tmin=25; }

repo="${CLOUD_REPO_URL##*github.com[:/]}"; repo="${repo%.git}"

banner() {
  echo
  echo "================================================================"
  echo "  ОБЛАКО НЕ СПРАВИЛОСЬ — ПЕРЕХОДИМ НА ЛОКАЛЬНУЮ СБОРКУ"
  echo "  причина: $*"
  echo "================================================================"
  echo
}

go_local() {
  banner "$*"
  sc=$(ls "$src"/*.scenes.json 2>/dev/null | grep -v overlays_fetch | head -1 || true)
  if [ -n "$sc" ]; then
    echo "локальный поиск кадров (fetch_parallel, 6 потоков)…"
    python3 "$skill/template/fetch_parallel.py" "$sc" "$src/images" "$src/.env" 6 || true
    echo
    echo "открываю локальный дашборд — правь как всегда:"
    echo "  cd \"$src\" && python3 \"$skill/template/review.py\" --live \"$sc\" images 8790"
    echo "  -> http://localhost:8790/review.html"
  else
    echo "scenes.json ещё нет — классификация сценария делается в сессии по"
    echo "  $skill/СБОРКА-НОВОСТНОГО-РОЛИКА.md, дальше обычная локальная сборка."
  fi
  exit 2
}

# --- 0. cloud reachable at all? ---
command -v gh >/dev/null            || go_local "gh не установлен"
gh auth status >/dev/null 2>&1      || go_local "нет входа в GitHub (gh auth login)"

# --- 1. library scenes: fetch locally (fast disk read, no library in the cloud) ---
sc=$(ls "$src"/*.scenes.json 2>/dev/null | grep -v overlays_fetch | head -1 || true)
if [ -n "$sc" ]; then
  mkdir -p "$src/images"
  nlib=$(python3 - "$sc" "$src/images" <<'PY'
import json, sys, glob, os
d = json.load(open(sys.argv[1], encoding="utf-8"))
imgs = sys.argv[2]
todo = [s for s in d["scenes"] if str(s.get("source")) == "local_library"
        and not glob.glob(os.path.join(imgs, f"scene_{s['id']:03d}.*"))]
if todo:
    sub = {k: d[k] for k in d if k != "scenes"}
    sub["scenes"] = todo
    json.dump(sub, open(os.path.join(imgs, ".library_only.scenes.json"), "w"),
              ensure_ascii=False, indent=1)
print(len(todo))
PY
)
  if [ "${nlib:-0}" -gt 0 ]; then
    echo ">> ${nlib} библиотечных сцен — беру локально из медиатеки…"
    python3 "$skill/template/fetch_assets_news.py" \
      "$src/images/.library_only.scenes.json" "$src/images" "$src/.env" || \
      echo "   (часть библиотечных не нашлась — облако/дашборд подхватят)"
    rm -f "$src/images/.library_only.scenes.json"
  fi
fi

# --- 2. ship (library images ride along; cloud does only the web scenes) ---
if [ "$fetch_only" = 1 ]; then
  echo ">> отправляю в облако [FETCH-ONLY] — матрица наберёт кадры и остановится ДО сборки…"
  "$here/ship.sh" "$src" "$name" --fetch-only || go_local "ship.sh не смог запушить в репозиторий"
else
  echo ">> отправляю проект в облако (веб-сцены — параллельно на матрице)…"
  "$here/ship.sh" "$src" "$name"   || go_local "ship.sh не смог запушить в репозиторий"
fi

# --- 3. find the run the push kicked off ---
echo ">> жду, пока GitHub заведёт запуск…"
run_id=""
for _ in $(seq 1 20); do
  sleep 6
  run_id=$(gh run list -R "$repo" --workflow videoryad-cloud.yml \
            --json databaseId,event,status -q \
            '[.[] | select(.status=="in_progress" or .status=="queued")][0].databaseId' 2>/dev/null || true)
  [ -n "$run_id" ] && break
done
[ -n "$run_id" ] || go_local "запуск в GitHub Actions не появился за 2 минуты"
echo "   запуск #$run_id  —  https://github.com/$repo/actions/runs/$run_id"

# --- 4. watch it, with our own wall-clock timeout ---
( gh run watch "$run_id" -R "$repo" --exit-status >/dev/null 2>&1 ) &
watch_pid=$!
deadline=$(( $(date +%s) + tmin*60 ))
while kill -0 "$watch_pid" 2>/dev/null; do
  [ "$(date +%s)" -ge "$deadline" ] && { kill "$watch_pid" 2>/dev/null; go_local "облако не уложилось в ${tmin} мин"; }
  sleep 15
done
wait "$watch_pid"; rc=$?

concl=$(gh run view "$run_id" -R "$repo" --json conclusion -q .conclusion 2>/dev/null || echo unknown)
[ "$rc" -eq 0 ] && [ "$concl" = "success" ] || go_local "запуск завершился как '$concl'"

# --- 5. collect ---
echo ">> облако отработало успешно — забираю результат…"
"$here/get.sh" "$name" || go_local "не смог скачать Release (get.sh)"

dest="$HOME/projects/$name-cloud"

if [ "$fetch_only" = 1 ]; then
  echo
  echo "================================================================"
  echo "  КАДРЫ ИЗ ОБЛАКА (сборки ещё нет):  $dest"
  echo "================================================================"
  echo "  дашборд :  cd \"$dest\" && python3 \"$skill/template/review.py\" --live *.scenes.json images 8790"
  echo "  -> показать пользователю, дождаться «собирай»"
  echo "  сборка  :  $here/ship.sh \"$dest\" $name        (БЕЗ --fetch-only)"
  exit 0
fi

echo
echo "================================================================"
echo "  ГОТОВО (из облака):  $dest"
echo "================================================================"
echo "  QA-отчёт:  cat \"$dest/_cloud/QA-report.md\""
echo "  дашборд :  cd \"$dest\" && python3 \"$skill/template/review.py\" --live *.scenes.json images 8790"
echo "  правки  :  $here/ship.sh \"$dest\" $name   (тем же именем)"
