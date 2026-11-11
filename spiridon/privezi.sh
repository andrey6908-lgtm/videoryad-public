#!/usr/bin/env bash
# Забрать немой видеоряд из облака, подмешать озвучку и положить в папку темы.
set -euo pipefail
RID="${1:?нужен номер сборки}"
REPO=andrey6908-lgtm/videoryad-public
PROJ="$HOME/projects/spiridon-1311"
DST="/mnt/d/YouTube/2022/Видео на Дзен/ПРИМЕТЫ/НОЯБРЬ/13 Ноября - Спиридон и Никодим/ГОТОВОЕ"
TMP=$(mktemp -d)
bash ~/.claude/skills/news-video/cloud/va.sh rezerv gh run download "$RID" -R "$REPO" -n spiridon-nemoe -D "$TMP"
NEM=$(ls "$TMP"/*.mp4 | head -1)
echo "немой: $(du -h "$NEM" | cut -f1), $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$NEM") с"
mkdir -p "$DST"
OUT="$DST/13-11 СПИРИДОН И НИКОДИМ${2:+ — $2}.mp4"
nice -n 19 ionice -c3 ffmpeg -v error -y -i "$NEM" -i "$PROJ/narration.mp3" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -threads 2 "$OUT"
echo "готово: $OUT  ($(du -h "$OUT" | cut -f1))"
rm -rf "$TMP"
