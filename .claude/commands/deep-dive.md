---
description: ダイジェストIssueでチェック済みの記事を深掘り要約し、アーカイブしてIssueにコメントする
argument-hint: "[issue番号(省略時は最新のdigest Issue)]"
---

対象Issue: $ARGUMENTS (省略時は`scripts/gh.sh issue list --label digest --state open --json number,title`で最新のものを特定する)

`README.md`の「深掘り→アーカイブの規約」に定義された6ステップに厳密に従って、上記Issueでチェック済み(`- [x]`)の記事の深掘り要約・アーカイブ保存・Issueへのコメント投稿までを行う。手順・保存フォーマット・使用してよいスクリプトの詳細は同セクションを参照すること(このコマンド側では重複させない)。

完了したら「深掘り完了。」と一言メッセージを返す。
