#!/usr/bin/env python3
"""digests/*.json をGitHub Issue本文(チェックボックス付き)に変換する。

通常のリポジトリファイル(blobビュー)ではMarkdownのチェックボックスは
クリックできない。Issue/PR本文でのみタップで状態をトグルできるため、
Issueとして投稿する形式にしている。
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIGESTS_DIR = REPO_ROOT / "digests"

STAR_LABELS = {3: "★★★", 2: "★★", 1: "★"}

# Markdownのリンク記法(`[...]  (...)`)やインラインHTMLタグ解釈を壊す文字をエスケープする
_MARKDOWN_ESCAPE_RE = re.compile(r"([\\`*_\[\]<>])")

_TASK_ITEM_RE = re.compile(r"^- \[( |x|X)\]")
_ID_COMMENT_RE = re.compile(r"<!-- id:(\S+) -->")


def _escape_markdown(text):
    return _MARKDOWN_ESCAPE_RE.sub(r"\\\1", text)


def _star_label(interest_level):
    return STAR_LABELS.get(interest_level, "★")


def _article_item(article):
    title = _escape_markdown(article.get("title", ""))
    url = article.get("url", "")
    score_label = article.get("score_label", "")
    category = article.get("category", "")
    note = article.get("note", "")
    star = _star_label(article.get("interest_level"))
    article_id = article.get("id", "")

    lines = [f"- [ ] [{title}]({url}) — {star} ・ {category} ・ {score_label}"]
    if note:
        lines.append(f"  {note}")
    lines.append(f"  <!-- id:{article_id} -->")
    return "\n".join(lines)


def render_digest_issue_body(digest):
    date = digest.get("date", "")
    articles = digest.get("articles", [])
    count = len(articles)

    if count == 0:
        body = "該当する記事はありませんでした。"
    else:
        body = "\n".join(_article_item(a) for a in articles)

    return f"# 朝刊ダイジェスト {date}\n\n{count}件\n\n{body}\n"


def parse_checked_ids(body):
    """Issue本文からチェック済み(- [x])の記事idを抽出する。"""
    checked_ids = []
    current_checked = False

    for line in body.splitlines():
        task_match = _TASK_ITEM_RE.match(line)
        if task_match:
            current_checked = task_match.group(1) in ("x", "X")
            continue

        id_match = _ID_COMMENT_RE.search(line)
        if id_match and current_checked:
            checked_ids.append(id_match.group(1))

    return checked_ids


def build(date, digests_dir=DIGESTS_DIR):
    digest_path = digests_dir / f"{date}.json"
    digest = json.loads(digest_path.read_text(encoding="utf-8"))
    return render_digest_issue_body(digest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="対象日付(YYYY-MM-DD)。digests/<date>.jsonを読み込む")
    args = parser.parse_args()
    sys.stdout.write(build(args.date))
