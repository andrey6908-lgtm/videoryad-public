#!/usr/bin/env bash
# Разовая настройка ПЯТОГО аккаунта GitHub — публичного резервного (rezerv).
#
#   setup_rezerv.sh <github-логин> [имя-репозитория]
#
# Имя репозитория по умолчанию videoryad-cloud. Второй аргумент нужен, если
# публичный репозиторий заводится на аккаунте, где приватный videoryad-cloud
# уже есть (например videoryad-public на cptand-bot) — публичные репозитории
# не расходуют минуты Actions ВООБЩЕ, на любом аккаунте, поэтому пятый
# аккаунт для этого пути не обязателен.
#
# Зачем он нужен: у публичного репозитория минуты Actions не считаются вообще,
# поэтому он работает как аварийный бак, когда три приватных аккаунта
# (cptand/andiv/olga) выбрали свои 2000 минут и до обнуления 1-го числа ещё
# далеко. Постоянным путём он НЕ является: пока идёт сборка, в очереди видны
# найденные кадры, а готовый видеоряд несколько минут висит в релизе.
#
# Чего в публичном репозитории нет и не будет:
#   • ключей      — только в GitHub Secrets, .env собирается в джобе (workflow)
#   • озвучки     — ship.sh её не отправляет с 2026-10-12
#   • пути на D:  — .source_dir остаётся локально (ship.sh, 2026-10-14)
#
# ПЕРЕД запуском нужно один раз войти в аккаунт (это интерактивно, скрипт
# такого не умеет):
#   GH_CONFIG_DIR=~/.config/gh-rezerv gh auth login
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
login="${1:?usage: setup_rezerv.sh <github-логин> [имя-репозитория]}"
reponame="${2:-videoryad-cloud}"
cfgdir="$HOME/.config/gh-rezerv"
repo="$login/$reponame"

export GH_CONFIG_DIR="$cfgdir"
mkdir -p "$cfgdir"

who=$(gh api user --jq .login 2>/dev/null || true)
if [ "$who" != "$login" ]; then
  echo "Нет входа в аккаунт '$login' внутри $cfgdir (сейчас там: '${who:-никого}')."
  echo "Войди один раз вручную и запусти скрипт снова:"
  echo "    GH_CONFIG_DIR=$cfgdir gh auth login"
  exit 1
fi
echo "аккаунт: $who"

# 1. локальный конфиг аккаунта (его читает config.sh по VIDEORYAD_ACCOUNT=rezerv)
cat > "$HOME/.config/videoryad-cloud.rezerv.sh" <<CFG
CLOUD_REPO_URL="https://github.com/$login/$reponame.git"
CLOUD_REPO_DIR="\$HOME/projects/videoryad-cloud-rezerv"
CFG
echo "конфиг: ~/.config/videoryad-cloud.rezerv.sh"

# 2. ПУБЛИЧНЫЙ репозиторий с нуля — историю старых репозиториев не переносим
#    (в ней лежат ключ Pexels и 338 файлов озвучки; наружу это нельзя)
if gh repo view "$repo" >/dev/null 2>&1; then
  echo "репозиторий $repo уже есть"
else
  gh repo create "$repo" --public --description "видеоряд: облачная сборка (резервный, публичный)"
  echo "репозиторий $repo создан ПУБЛИЧНЫМ"
fi
vis=$(gh repo view "$repo" --json visibility --jq .visibility)
echo "видимость: $vis"

# 3. ключи — в Secrets, а не в репозиторий
key=$(grep '^PEXELS_API_KEY=' "$here/../template/.env" | cut -d= -f2- || true)
if [ -n "$key" ]; then
  printf '%s' "$key" | gh secret set PEXELS_API_KEY -R "$repo"
  echo "секрет PEXELS_API_KEY залит"
else
  echo "ВНИМАНИЕ: PEXELS_API_KEY в template/.env пуст — секрет не залит"
fi

# 4. защита, которой нет у приватных: чужие форки не должны запускать наши
#    прогоны и тем более трогать секреты
gh api -X PUT "repos/$repo/actions/permissions" \
  -F enabled=true -f allowed_actions=all >/dev/null
gh api -X PUT "repos/$repo/actions/permissions/workflow" \
  -f default_workflow_permissions=write -F can_approve_pull_request_reviews=false >/dev/null
gh api -X PUT "repos/$repo/actions/permissions/fork-pr-contributor-approval" \
  -f approval_policy=all_external_contributors >/dev/null 2>&1 \
  || echo "(политику форков задать через API не вышло — проверь в Settings → Actions → Fork pull request workflows)"
echo "форки: прогоны сторонних требуют ручного одобрения"

# 5. код сборщика — тем же sync_assembler.sh, что и у остальных четырёх
VIDEORYAD_ACCOUNT=rezerv bash "$here/sync_assembler.sh"

echo
echo "================================================================"
echo "  Пятый аккаунт готов: VIDEORYAD_ACCOUNT=rezerv -> $repo (публичный)"
echo "  Работать так же, как с остальными:"
echo "    bash $here/va.sh rezerv bash $here/ship.sh <проект> <имя>"
echo "    bash $here/va.sh rezerv bash $here/get.sh <имя>"
echo "  get.sh удалит релиз сразу после скачивания — ссылка публичная."
echo "  ОСТАЛОСЬ: один тестовый прогон целиком, прежде чем полагаться на резерв."
echo "================================================================"
