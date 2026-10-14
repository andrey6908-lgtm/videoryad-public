#!/usr/bin/env bash
# Push the current assembler (this skill) into the cloud repo under assembler/,
# so the GitHub runner builds with the same code we run locally.
# Run this once at setup, and again whenever the engine changes
# (same moment you'd update СБОРКА-НОВОСТНОГО-РОЛИКА.md).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
skill="$(cd "$here/.." && pwd)"
source "$here/config.sh"

[ -d "$CLOUD_REPO_DIR/.git" ] || git clone "$CLOUD_REPO_URL" "$CLOUD_REPO_DIR"
cd "$CLOUD_REPO_DIR"
git pull --quiet --ff-only || true

mkdir -p assembler
# ВАЖНО: .env НИКОГДА не уезжает в репозиторий (проверено 2026-10-14 — он
# лежал в assembler/template/.env всех четырёх репозиториев, то есть ключ
# Pexels остался в истории git навсегда). Ключи раннер получает из GitHub
# Secrets; .yml собирает из них .env прямо в джобе. Резервные копии *.bak*
# тоже не нужны — это мои локальные черновики.
rsync -a --delete --delete-excluded \
  --exclude '__pycache__' --exclude '.git' --exclude 'scripts/' \
  --exclude '.env' --exclude '.env.local' \
  --exclude '*.bak' --exclude '*.bak-*' --exclude '*.bak[0-9]*' \
  "$skill/template"  "$skill/cloud"  assembler/
# SKILL.md и СБОРКА-*.md — это рабочие заметки пользователя: цитаты, пути на
# D:, названия каналов, стратегия. В ПУБЛИЧНЫЙ репозиторий они не едут
# (2026-10-14). Облаку они и не нужны: сцены классифицируются локально, а
# шаг Claude в workflow включается только при секрете CLAUDE_CODE_OAUTH_TOKEN,
# которого на публичном аккаунте нет и не будет.
if [ "${VIDEORYAD_PUBLIC:-0}" = 1 ]; then
  rm -f assembler/SKILL.md "assembler/СБОРКА-НОВОСТНОГО-РОЛИКА.md"
else
  cp "$skill/SKILL.md" "$skill/СБОРКА-НОВОСТНОГО-РОЛИКА.md" assembler/ 2>/dev/null || true
fi

# first run also installs the workflow
mkdir -p .github/workflows
cp "$here/workflows/videoryad-cloud.yml" .github/workflows/
mkdir -p queue output && touch queue/.keep output/.keep
cat > .gitignore <<'IGN'
# ключи — только в GitHub Secrets, в репозитории их быть не должно
.env
.env.local
# озвучка пользователя в облако не отправляется (ship.sh, 2026-10-12)
*.mp3
*.wav
*.m4a
# локальные черновики-бэкапы
*.bak
*.bak-*
__pycache__/
IGN
# --delete-excluded выше сам убирает из рабочей копии всё исключённое
# (.env, *.bak*, __pycache__), поэтому git add -A снимает это и с учёта.

git add -A
if git diff --cached --quiet; then echo "assembler already up to date"; exit 0; fi
git commit -q -m "sync assembler $(date -u '+%Y-%m-%d %H:%M')"
git push --quiet
echo "assembler synced to cloud repo"
