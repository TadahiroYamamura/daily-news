#!/usr/bin/env python3
"""digests/*.json を docs/*.html (GitHub Pages 公開対象) に変換する。"""

import argparse
import json
import sys
from html import escape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIGESTS_DIR = REPO_ROOT / "digests"
DOCS_DIR = REPO_ROOT / "docs"

STAR_LABELS = {3: "★★★", 2: "★★", 1: "★"}


def _star_label(interest_level):
    return STAR_LABELS.get(interest_level, "★")


def _article_item_html(article):
    title = escape(article.get("title", ""))
    url = escape(article.get("url", ""), quote=True)
    score_label = escape(article.get("score_label", ""))
    category = escape(article.get("category", ""))
    note = escape(article.get("note", ""))
    star = _star_label(article.get("interest_level"))
    return f"""    <li class="article">
      <a href="{url}">{title}</a>
      <div class="meta">{star} ・ {category} ・ {score_label}</div>
      <div class="note">{note}</div>
    </li>"""


def render_digest_html(digest):
    date = escape(digest.get("date", ""))
    articles = digest.get("articles", [])
    count = len(articles)

    if count == 0:
        body = '  <p class="empty">該当する記事はありませんでした。</p>'
    else:
        items = "\n".join(_article_item_html(a) for a in articles)
        body = f"  <ul class=\"articles\">\n{items}\n  </ul>"

    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>朝刊ダイジェスト {date}</title>
</head>
<body>
  <h1>朝刊ダイジェスト {date}</h1>
  <p class="count">{count}件</p>
{body}
  <p><a href="index.html">一覧へ戻る</a></p>
</body>
</html>
"""


def render_index_html(dates):
    sorted_dates = sorted(dates, reverse=True)

    if not sorted_dates:
        body = '  <p class="empty">まだダイジェストがありません。</p>'
    else:
        items = "\n".join(
            f'    <li><a href="{escape(d, quote=True)}.html">{escape(d)}</a></li>'
            for d in sorted_dates
        )
        body = f"  <ul class=\"dates\">\n{items}\n  </ul>"

    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>朝刊ダイジェスト一覧</title>
</head>
<body>
  <h1>朝刊ダイジェスト一覧</h1>
{body}
</body>
</html>
"""


def build(digests_dir=DIGESTS_DIR, docs_dir=DOCS_DIR):
    docs_dir.mkdir(parents=True, exist_ok=True)
    dates = []

    for digest_path in sorted(digests_dir.glob("*.json")):
        digest = json.loads(digest_path.read_text(encoding="utf-8"))
        date = digest.get("date", digest_path.stem)
        dates.append(date)
        (docs_dir / f"{date}.html").write_text(
            render_digest_html(digest), encoding="utf-8"
        )

    (docs_dir / "index.html").write_text(render_index_html(dates), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    build()
    sys.exit(0)
