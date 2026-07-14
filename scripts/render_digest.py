#!/usr/bin/env python3
"""digests/*.json を digests/*.md (GitHubのブラウザ表示でそのまま読める形式) に変換する。"""

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


def _escape_markdown(text):
    return _MARKDOWN_ESCAPE_RE.sub(r"\\\1", text)


def _star_label(interest_level):
    return STAR_LABELS.get(interest_level, "★")


def _article_line(article):
    title = _escape_markdown(article.get("title", ""))
    url = article.get("url", "")
    score_label = article.get("score_label", "")
    category = article.get("category", "")
    note = article.get("note", "")
    star = _star_label(article.get("interest_level"))

    line = f"- [{title}]({url}) — {star} ・ {category} ・ {score_label}"
    if note:
        line += f"\n  {note}"
    return line


def render_digest_markdown(digest):
    date = digest.get("date", "")
    articles = digest.get("articles", [])
    count = len(articles)

    if count == 0:
        body = "該当する記事はありませんでした。"
    else:
        body = "\n".join(_article_line(a) for a in articles)

    return f"# 朝刊ダイジェスト {date}\n\n{count}件\n\n{body}\n"


def build(digests_dir=DIGESTS_DIR):
    for digest_path in sorted(digests_dir.glob("*.json")):
        digest = json.loads(digest_path.read_text(encoding="utf-8"))
        date = digest.get("date", digest_path.stem)
        (digests_dir / f"{date}.md").write_text(
            render_digest_markdown(digest), encoding="utf-8"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    build()
    sys.exit(0)
