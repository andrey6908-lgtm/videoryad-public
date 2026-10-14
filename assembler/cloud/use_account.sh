# Выбор аккаунта для ЭТОЙ вкладки. Файл предназначен для `source`, не для
# запуска: он экспортирует переменные в твою текущую оболочку.
#
#     source ~/.claude/skills/news-video/cloud/use_account.sh andrey4
#
# После этого работают ОБА пути сразу:
#   • скрипты сборщика  — run.sh / ship.sh / get.sh (читают VIDEORYAD_ACCOUNT)
#   • прямые вызовы gh  — gh run list / gh release view (читают GH_CONFIG_DIR)
#
# ЗАЧЕМ ОТДЕЛЬНЫЙ ФАЙЛ (2026-10-11, поймано соседней вкладкой сразу после
# внедрения параллельного режима): сам бинарь `gh` про VIDEORYAD_ACCOUNT НИЧЕГО
# не знает — эту переменную читает только наш config.sh внутри скриптов
# сборщика. Поэтому `VIDEORYAD_ACCOUNT=cptand gh api user` молча уходит в ОБЩИЙ
# ~/.config/gh/hosts.yml и возвращает чужой, случайно активный сейчас аккаунт.
# Выглядит это особенно подло: команда не падает, а отвечает — просто про
# другой аккаунт. Экспортировать нужно ИМЕННО ОБЕ переменные, что этот файл и
# делает одной строкой.

_va_name="${1:-}"
case "$_va_name" in
  cptand|andiv|olga|andrey4|rezerv) ;;
  *)
    echo "usage: source use_account.sh <cptand|andiv|olga|andrey4|rezerv>" >&2
    unset _va_name
    return 1 2>/dev/null || exit 1
    ;;
esac

if [ ! -d "$HOME/.config/gh-$_va_name" ]; then
  echo "нет каталога ~/.config/gh-$_va_name — см. CLAUDE.md, раздел про ротацию" >&2
  unset _va_name
  return 1 2>/dev/null || exit 1
fi

export VIDEORYAD_ACCOUNT="$_va_name"
export GH_CONFIG_DIR="$HOME/.config/gh-$_va_name"
unset _va_name

echo "аккаунт этой вкладки: $VIDEORYAD_ACCOUNT ($(gh api user --jq .login 2>/dev/null || echo '?'))"
