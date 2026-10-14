#!/usr/bin/env bash
# Session-priority flag. `busy.sh on` while Claude is working live in a session
# (push-triggered cloud runs then defer to the nightly schedule); `busy.sh off`
# when the session ends. The nightly cron run ignores this flag.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/config.sh"

[ -d "$CLOUD_REPO_DIR/.git" ] || { echo "run ship.sh once first (clones the repo)"; exit 1; }
cd "$CLOUD_REPO_DIR"
git pull --quiet --ff-only || true

case "${1:-}" in
  on)  date -u '+%Y-%m-%dT%H:%M:%SZ' > BUSY; git add BUSY
       git commit -q -m "session busy" && git push --quiet
       echo "BUSY set — cloud push-runs will defer" ;;
  off) rm -f BUSY; git add -A
       git commit -q -m "session free" && git push --quiet
       echo "BUSY cleared" ;;
  *)   echo "usage: busy.sh on|off"; exit 1 ;;
esac
