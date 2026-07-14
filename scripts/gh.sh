#!/usr/bin/env bash
# .envのGITHUB_TOKENを読み込んでghコマンドを実行するラッパー。
# エージェント(Claude)が.envを直接読む/sourceする必要をなくし、
# トークンが会話の透明性(tool result)に露出しないようにするための仲介。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -f "$SCRIPT_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/.env"
  set +a
fi

exec gh "$@"
