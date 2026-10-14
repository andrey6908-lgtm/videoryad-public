# Cloud assembler — local config. Edit these two lines after you create the repo.
#
# CLOUD_REPO_URL  — the empty private repo you made on github.com
# CLOUD_REPO_DIR  — where a local working copy lives (ship.sh clones here once)

CLOUD_REPO_URL="${CLOUD_REPO_URL:-https://github.com/cptand-bot/videoryad-cloud.git}"
CLOUD_REPO_DIR="${CLOUD_REPO_DIR:-$HOME/projects/videoryad-cloud}"

# ── ПАРАЛЛЕЛЬНЫЙ РЕЖИМ (2026-10-11) ────────────────────────────────────────
# Если в окружении задан VIDEORYAD_ACCOUNT=<cptand|andiv|olga|andrey4>, эта
# вкладка работает со СВОИМ каталогом gh и СВОИМ репо, не трогая общие
# ~/.config/gh/hosts.yml и ~/.config/videoryad-cloud.local.sh. Четыре вкладки
# могут пушить в четыре аккаунта ОДНОВРЕМЕННО — switch_account.sh при этом
# не нужен вообще.
#
# Зачем: `gh` хранит активный аккаунт в ОДНОМ файле на всю машину, поэтому
# при четырёх вкладках переключатель один на всех, и вкладки встают в
# очередь друг за другом вместо параллельной работы. 2026-10-11 это стоило
# двух инцидентов за день: разъехавшееся окно переключения (пуш едва не
# ушёл в чужой репозиторий) и, как следствие общей же гонки за ресурсы,
# перепутанные порты дашбордов. GH_CONFIG_DIR убирает общий ресурс целиком.
#
# Использование в сессии (один раз в начале работы над роликом):
#   export VIDEORYAD_ACCOUNT=andrey4
# дальше run.sh / ship.sh / get.sh сами ходят в нужный аккаунт.
if [ -n "${VIDEORYAD_ACCOUNT:-}" ]; then
  case "$VIDEORYAD_ACCOUNT" in
    cptand|andiv|olga|andrey4) : ;;
    # rezerv — ПЯТЫЙ аккаунт, ПУБЛИЧНЫЙ репозиторий (решение 2026-10-13).
    # Включается только когда приватные три упёрлись в лимит минут: у
    # публичного репозитория минуты Actions не считаются вообще. Платой за это
    # является открытость: пока идёт сборка, в очереди видны найденные кадры, а
    # готовый видеоряд несколько минут висит в релизе (get.sh его сразу удаляет).
    # Ключей там нет — они в Secrets; озвучки нет — ship.sh её не отправляет.
    rezerv) export VIDEORYAD_PUBLIC=1 ;;
    *) echo "config.sh: неизвестный VIDEORYAD_ACCOUNT='$VIDEORYAD_ACCOUNT' (ожидается cptand|andiv|olga|andrey4|rezerv)" >&2; return 1 2>/dev/null || exit 1 ;;
  esac
  _va_dir="$HOME/.config/gh-$VIDEORYAD_ACCOUNT"
  _va_cfg="$HOME/.config/videoryad-cloud.$VIDEORYAD_ACCOUNT.sh"
  if [ ! -d "$_va_dir" ]; then
    echo "config.sh: нет каталога $_va_dir — создай его (см. README-CLOUD.md, раздел про параллельный режим)" >&2
    return 1 2>/dev/null || exit 1
  fi
  if [ ! -f "$_va_cfg" ]; then
    echo "config.sh: нет файла $_va_cfg" >&2
    return 1 2>/dev/null || exit 1
  fi
  export GH_CONFIG_DIR="$_va_dir"
  . "$_va_cfg"
  unset _va_dir _va_cfg
fi

# Local, untracked override — holds the active rotation account's repo URL
# (see switch_account.sh). Sourced last so it wins.
# ВНИМАНИЕ: читается ТОЛЬКО когда VIDEORYAD_ACCOUNT не задан (старый,
# последовательный режим с общим переключателем).
# `if [ -f ]; then . ; fi` on purpose, NOT `[ -f ] && .` — under this script's
# callers' `set -e` (ship.sh/run.sh), a bare `&&`-guard whose test is false
# (local.sh absent) makes the ENTIRE `source config.sh` line fail with no
# output, silently killing the caller before it prints anything (bit us
# 2026-10-01: a ship to the then-local.sh-less "default" account looked like
# it succeeded — exit 0 — but pushed nothing). `if/fi` has no such trap.
if [ -z "${VIDEORYAD_ACCOUNT:-}" ] && [ -f "$HOME/.config/videoryad-cloud.local.sh" ]; then . "$HOME/.config/videoryad-cloud.local.sh"; fi

# ASSEMBLER_REPO (a GitHub mirror of ~/.claude/skills/news-video) is referenced
# by the workflow as a repo variable `ASSEMBLER_REPO`, not here. See README-CLOUD.md.
