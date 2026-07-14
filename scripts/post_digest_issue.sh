#!/usr/bin/env bash
# digests/<date>.json をもとにGitHub Issueを作成する。
# タイトル・ラベル・gh呼び出しの詳細をここに閉じ込め、
# エージェントには日付だけを渡してもらう(gh issue createの組み立てをさせない)。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE="${1:?usage: post_digest_issue.sh YYYY-MM-DD}"

python3 "$SCRIPT_DIR/render_digest.py" "$DATE" | "$SCRIPT_DIR/gh.sh" issue create \
  --title "朝刊ダイジェスト $DATE" \
  --body-file - \
  --label digest
