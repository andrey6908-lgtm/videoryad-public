#!/usr/bin/env bash
# Выполнить ЛЮБУЮ команду от имени конкретного аккаунта ротации — одним
# вызовом, без всякого состояния в оболочке.
#
#     bash ~/.claude/skills/news-video/cloud/va.sh <аккаунт> <команда...>
#
# Примеры:
#     bash cloud/va.sh andrey4 gh run list -R andrey6908-lgtm/videoryad-cloud --workflow videoryad-cloud.yml
#     bash cloud/va.sh andrey4 bash ~/.claude/skills/news-video/cloud/ship.sh /mnt/c/videoryad-build/proj proj
#     bash cloud/va.sh cptand  bash ~/.claude/skills/news-video/cloud/get.sh ds-roll-1210
#     bash cloud/va.sh olga    gh api user --jq .login
#
# ПОЧЕМУ ИМЕННО ТАК, А НЕ `source use_account.sh` (2026-10-11, поймано
# соседней вкладкой уже после внедрения параллельного режима): в среде
# Claude Code состояние оболочки между вызовами инструмента Bash НЕ
# сохраняется. `source use_account.sh andiv` отдельной командой экспортирует
# переменные в оболочку, которая тут же умирает, и следующая команда снова
# работает с ОБЩИМ ~/.config/gh/hosts.yml, то есть с чужим активным
# аккаунтом. При этом ничего не падает — gh просто отвечает про другой
# аккаунт, и ошибку легко не заметить, пока пуш не уедет не в тот репозиторий.
#
# va.sh снимает проблему целиком: обе переменные выставляются внутри ОДНОГО
# процесса вместе с самой командой, поэтому помнить ничего не нужно и
# состояние между вызовами не требуется.
#
# `source use_account.sh` остаётся полезным только в живом интерактивном
# терминале, где оболочка живёт долго.
set -euo pipefail

name="${1:?usage: va.sh <cptand|andiv|olga|andrey4|rezerv> <команда...>}"
shift
[ "$#" -gt 0 ] || { echo "va.sh: не задана команда" >&2; exit 1; }

case "$name" in
  cptand|andiv|olga|andrey4|rezerv) : ;;
  *) echo "va.sh: неизвестный аккаунт '$name' (ожидается cptand|andiv|olga|andrey4|rezerv)" >&2; exit 1 ;;
esac

dir="$HOME/.config/gh-$name"
[ -d "$dir" ] || { echo "va.sh: нет каталога $dir" >&2; exit 1; }

export VIDEORYAD_ACCOUNT="$name"   # читают run.sh / ship.sh / get.sh через config.sh
export GH_CONFIG_DIR="$dir"        # читает сам бинарь gh

exec "$@"
