#!/usr/bin/env python3
"""Hacker News・Lobsters・はてなブックマーク・Zenn・Qiita・セキュリティブログを決定論的に取得する。

LLMによるページ読解に頼っていた抽出を、構造化API/RSS(Atom含む)の
パースに置き換えることで、実行のたびに結果がブレるのを防ぐ。
"""

import hashlib
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET

HN_TOPSTORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HN_LIMIT = 30

LOBSTERS_URL = "https://lobste.rs/hottest.json"
LOBSTERS_LIMIT = 25

HATENA_FEEDS = {
    # IT配下の詳細カテゴリ(プログラミング/AI・機械学習 等)には専用RSSが存在しない(404を確認済み)。
    # 総合IT枠(30件)から、興味度評価ステップ(LLM)でカテゴリ・関連度を判定する。
    "hatena_it": "https://b.hatena.ne.jp/hotentry/it.rss",
}

JAPANESE_TECH_FEEDS = {
    "zenn": "https://zenn.dev/feed",
    "qiita": "https://qiita.com/popular-items/feed",
}

SECURITY_BLOG_FEEDS = {
    "security_blog_aikido": "https://www.aikido.dev/blog/rss.xml",
    "security_blog_wiz": "https://www.wiz.io/feed/rss.xml",
}
SECURITY_BLOG_LIMIT = 3


def article_id(source, url):
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return f"{source}-{digest}"


def _local_name(tag):
    return tag.rsplit("}", 1)[-1]


def _child_text(elem, name):
    for child in elem:
        if _local_name(child.tag) == name:
            return (child.text or "").strip()
    return None


def _child_link(elem):
    # RSS(1.0/2.0): <link>テキストURL</link>。Atom(Qiita等): <link href="..." rel="alternate"/>
    links = [c for c in elem if _local_name(c.tag) == "link"]
    if not links:
        return None
    for link in links:
        if link.get("rel") in (None, "alternate") and link.get("href"):
            return link.get("href")
    text = (links[0].text or "").strip()
    return text or links[0].get("href")


def parse_rss_items(raw_bytes):
    """RSS 1.0(はてな)・RSS 2.0(一般ブログ)・Atom(Qiita等)から title/link/bookmarkcount を抽出する。"""
    root = ET.fromstring(raw_bytes)
    items = []
    for elem in root.iter():
        if _local_name(elem.tag) not in ("item", "entry"):
            continue
        items.append(
            {
                "title": _child_text(elem, "title") or "",
                "url": _child_link(elem) or "",
                "bookmarkcount": _child_text(elem, "bookmarkcount"),
            }
        )
    return items


def hn_item_to_article(item):
    if item.get("type") != "story":
        return None

    # 元記事ではなくコメントページURLを使う(コメントも確認できるようにするため。
    # dev-docs/digest-schema.md の規約)
    story_id = item["id"]
    url = f"https://news.ycombinator.com/item?id={story_id}"

    return {
        "source": "hacker_news",
        "id": article_id("hacker_news", url),
        "title": item.get("title", ""),
        "url": url,
        "score_label": f"{item.get('score', 0)}pt",
        "comment_count": item.get("descendants", 0),
    }


def lobsters_item_to_article(item):
    # 元記事ではなくコメントページURLを使う(HNと同じ規約。dev-docs/digest-schema.md参照)
    url = item["comments_url"]
    return {
        "source": "lobsters",
        "id": article_id("lobsters", url),
        "title": item.get("title", ""),
        "url": url,
        "score_label": f"{item.get('score', 0)}pt",
        "comment_count": item.get("comment_count", 0),
    }


def dedupe_by_url(articles):
    seen = set()
    result = []
    for article in articles:
        url = article["url"]
        if url in seen:
            continue
        seen.add(url)
        result.append(article)
    return result


def _default_fetch_json(url):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.load(resp)


def _default_fetch_bytes(url):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.read()


def fetch_hn(limit=HN_LIMIT, fetch_json=_default_fetch_json):
    story_ids = fetch_json(HN_TOPSTORIES_URL)[:limit]
    articles = []
    for story_id in story_ids:
        item = fetch_json(HN_ITEM_URL.format(story_id))
        article = hn_item_to_article(item)
        if article is not None:
            articles.append(article)
    return articles


def fetch_lobsters(limit=LOBSTERS_LIMIT, fetch_json=_default_fetch_json):
    items = fetch_json(LOBSTERS_URL)[:limit]
    return [lobsters_item_to_article(item) for item in items]


def fetch_rss_source(source, url, limit=None, fetch_bytes=_default_fetch_bytes):
    raw = fetch_bytes(url)
    entries = parse_rss_items(raw)
    if limit is not None:
        entries = entries[:limit]

    articles = []
    for entry in entries:
        bookmarkcount = entry["bookmarkcount"]
        score_label = f"{bookmarkcount} users" if bookmarkcount is not None else ""
        articles.append(
            {
                "source": source,
                "id": article_id(source, entry["url"]),
                "title": entry["title"],
                "url": entry["url"],
                "score_label": score_label,
            }
        )
    return articles


def fetch_all():
    articles = fetch_hn()
    articles.extend(fetch_lobsters())

    hatena_articles = []
    for source, url in HATENA_FEEDS.items():
        hatena_articles.extend(fetch_rss_source(source, url))
    articles.extend(dedupe_by_url(hatena_articles))

    for source, url in JAPANESE_TECH_FEEDS.items():
        articles.extend(fetch_rss_source(source, url))

    for source, url in SECURITY_BLOG_FEEDS.items():
        articles.extend(fetch_rss_source(source, url, limit=SECURITY_BLOG_LIMIT))

    return articles


if __name__ == "__main__":
    json.dump(fetch_all(), sys.stdout, ensure_ascii=False, indent=2)
    print()
