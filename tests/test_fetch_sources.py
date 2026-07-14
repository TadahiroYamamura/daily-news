import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from fetch_sources import (
    article_id,
    dedupe_by_url,
    fetch_hn,
    fetch_rss_source,
    hn_item_to_article,
    parse_rss_items,
)

HATENA_RSS_FIXTURE = b"""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns="http://purl.org/rss/1.0/"
 xmlns:hatena="http://www.hatena.ne.jp/info/xmlns#"
>
<channel rdf:about="https://b.hatena.ne.jp/hotentry/it">
<title>hotentry</title>
</channel>
<item rdf:about="https://example.com/a">
<title>\xe8\xa8\x98\xe4\xba\x8b1</title>
<link>https://example.com/a</link>
<hatena:bookmarkcount>312</hatena:bookmarkcount>
</item>
<item rdf:about="https://example.com/b">
<title>\xe8\xa8\x98\xe4\xba\x8b2</title>
<link>https://example.com/b</link>
<hatena:bookmarkcount>88</hatena:bookmarkcount>
</item>
</rdf:RDF>
"""

PLAIN_RSS2_FIXTURE = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
<title>Security Blog</title>
<item>
<title>Some vulnerability disclosed</title>
<link>https://example.com/blog/post-1</link>
</item>
<item>
<title>Another post</title>
<link>https://example.com/blog/post-2</link>
</item>
</channel>
</rss>
"""


def test_article_id_is_stable_and_source_prefixed():
    id1 = article_id("hatena_it", "https://example.com/a")
    id2 = article_id("hatena_it", "https://example.com/a")
    id3 = article_id("hatena_it", "https://example.com/b")

    assert id1 == id2
    assert id1 != id3
    assert id1.startswith("hatena_it-")


def test_parse_rss_items_handles_rss1_with_hatena_bookmarkcount():
    items = parse_rss_items(HATENA_RSS_FIXTURE)

    assert items == [
        {"title": "記事1", "url": "https://example.com/a", "bookmarkcount": "312"},
        {"title": "記事2", "url": "https://example.com/b", "bookmarkcount": "88"},
    ]


def test_parse_rss_items_handles_plain_rss2_without_bookmarkcount():
    items = parse_rss_items(PLAIN_RSS2_FIXTURE)

    assert items == [
        {"title": "Some vulnerability disclosed", "url": "https://example.com/blog/post-1", "bookmarkcount": None},
        {"title": "Another post", "url": "https://example.com/blog/post-2", "bookmarkcount": None},
    ]


def test_hn_item_to_article_uses_comments_page_as_url():
    # digest-schema.mdの規約: HNは元記事ではなくコメントページURLを使う(コメントも読めるようにするため)
    item = {"id": 123, "type": "story", "title": "Some Title", "url": "https://example.com/x", "score": 45, "descendants": 12}

    article = hn_item_to_article(item)

    assert article["source"] == "hacker_news"
    assert article["title"] == "Some Title"
    assert article["url"] == "https://news.ycombinator.com/item?id=123"
    assert article["score_label"] == "45pt"
    assert article["id"] == article_id("hacker_news", "https://news.ycombinator.com/item?id=123")


def test_hn_item_to_article_uses_comments_page_for_self_post_too():
    item = {"id": 999, "type": "story", "title": "Ask HN: something", "score": 10, "descendants": 3}

    article = hn_item_to_article(item)

    assert article["url"] == "https://news.ycombinator.com/item?id=999"


def test_hn_item_to_article_returns_none_for_non_story_type():
    item = {"id": 1, "type": "job", "title": "We are hiring"}

    assert hn_item_to_article(item) is None


def test_dedupe_by_url_keeps_first_occurrence():
    articles = [
        {"url": "https://example.com/a", "title": "first"},
        {"url": "https://example.com/b", "title": "b"},
        {"url": "https://example.com/a", "title": "duplicate"},
    ]

    result = dedupe_by_url(articles)

    assert len(result) == 2
    assert result[0]["title"] == "first"
    assert result[1]["title"] == "b"


def test_fetch_hn_orchestrates_topstories_and_items_via_injected_fetcher():
    topstories = [1, 2, 3]
    items_by_id = {
        1: {"id": 1, "type": "story", "title": "A", "url": "https://example.com/a", "score": 100, "descendants": 5},
        2: {"id": 2, "type": "job", "title": "job post"},
        3: {"id": 3, "type": "story", "title": "C", "url": "https://example.com/c", "score": 50, "descendants": 1},
    }

    def fake_fetch_json(url):
        if url.endswith("topstories.json"):
            return topstories
        story_id = int(url.rsplit("/", 1)[-1].removesuffix(".json"))
        return items_by_id[story_id]

    articles = fetch_hn(limit=3, fetch_json=fake_fetch_json)

    assert [a["title"] for a in articles] == ["A", "C"]


def test_fetch_rss_source_orchestrates_with_injected_fetcher_and_limit():
    def fake_fetch_bytes(url):
        return HATENA_RSS_FIXTURE

    articles = fetch_rss_source("hatena_it", "https://example.com/feed.rss", limit=1, fetch_bytes=fake_fetch_bytes)

    assert len(articles) == 1
    assert articles[0]["source"] == "hatena_it"
    assert articles[0]["title"] == "記事1"
    assert articles[0]["score_label"] == "312 users"
