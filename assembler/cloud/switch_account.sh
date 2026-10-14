#!/usr/bin/env bash
# ⚠️  УСТАРЕЛО ДЛЯ ПАРАЛЛЕЛЬНОЙ РАБОТЫ (2026-10-11). НЕ ЗВАТЬ ЕГО, ЕСЛИ НА
# МАШИНЕ РАБОТАЕТ БОЛЬШЕ ОДНОЙ ВКЛАДКИ.
#
# Этот скрипт меняет ОБЩИЙ на всю машину файл ~/.config/gh/hosts.yml, то есть
# переключает аккаунт сразу ВСЕМ сессиям. Именно поэтому четыре вкладки
# выстраивались в очередь друг за другом («не трогай gh, я пушу») вместо того
# чтобы работать параллельно, и дважды за 2026-10-11 едва не отправили сборку
# в чужой репозиторий.
#
# ПРАВИЛЬНЫЙ СПОСОБ — у каждой вкладки свой каталог gh, общий файл не трогаем:
#
#     export VIDEORYAD_ACCOUNT=andrey4      # один раз в начале работы
#     bash cloud/run.sh  <proj> <name> --fetch-only
#     bash cloud/ship.sh <proj> <name>
#     bash cloud/get.sh  <name>
#
# Допустимые значения: cptand | andiv | olga | andrey4. Каталоги
# ~/.config/gh-<имя> уже созданы и закреплены за своими аккаунтами.
# Четыре вкладки с четырьмя разными VIDEORYAD_ACCOUNT пушат ОДНОВРЕМЕННО,
# никакой координации между ними не требуется. Подробности — в config.sh.
#
# Этот скрипт оставлен только для одиночной работы и для аварийного
# восстановления общего файла.
#
# Switch the active GitHub account (gh + git credential helper) AND the
# videoryad-cloud repo config to one of the rotation accounts, atomically.
# Usage: switch_account.sh <cptand|andiv|olga|andrey4>
#
# Do this INSTEAD of manually running `gh auth switch` + editing
# ~/.config/videoryad-cloud.local.sh separately — doing those two steps apart
# is exactly what caused a cross-session race on 2026-09-21 (one session's
# gh-auth-switch landed between another session's config-read and its
# git push, sending it to the wrong account's repo).
set -euo pipefail

name="${1:?usage: switch_account.sh <cptand|andiv|olga|andrey4>}"

case "$name" in
  cptand)
    gh auth switch -u cptand-bot
    # NOT `rm -f local.sh` (old behavior) — config.sh does
    # `[ -f local.sh ] && . local.sh` which, under this script's
    # `set -e` (inherited by ship.sh/run.sh via `source config.sh`),
    # makes the whole `source config.sh` line fail with ZERO output
    # whenever local.sh is absent, silently killing ship.sh before it
    # prints anything (found 2026-10-01 — a ship to cptand looked like
    # it succeeded, exit 0, nothing pushed). Always keep local.sh
    # present, even for the "default" account.
    cp "$HOME/.config/videoryad-cloud.cptand.sh" "$HOME/.config/videoryad-cloud.local.sh"
    ;;
  andiv)
    gh auth switch -u andiv1969cher-droid
    cp "$HOME/.config/videoryad-cloud.andiv.sh" "$HOME/.config/videoryad-cloud.local.sh"
    ;;
  olga)
    gh auth switch -u 19olga78gr-rgb
    cp "$HOME/.config/videoryad-cloud.olga.sh" "$HOME/.config/videoryad-cloud.local.sh"
    ;;
  andrey4)
    gh auth switch -u andrey6908-lgtm
    cp "$HOME/.config/videoryad-cloud.andrey4.sh" "$HOME/.config/videoryad-cloud.local.sh"
    ;;
  *)
    echo "unknown account: $name (expected cptand|andiv|olga|andrey4)" >&2
    exit 1
    ;;
esac

echo "active account -> $name"
gh auth status 2>&1 | grep -A1 "Active account: true" || true
