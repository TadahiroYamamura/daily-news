import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from render_digest import render_digest_html, render_index_html


def test_render_digest_html_includes_each_article_title_and_link():
    digest = {
        "date": "2026-07-10",
        "articles": [
            {
                "id": "hatena-abc123",
                "source": "hatena_it",
                "title": "記事タイトルその1",
                "url": "https://example.com/article1",
                "score_label": "312 users",
                "interest_level": 3,
                "category": "AI",
                "note": "興味領域とのマッチング理由",
            },
            {
                "id": "hn-999",
                "source": "hacker_news",
                "title": "Article Title 2",
                "url": "https://news.ycombinator.com/item?id=999",
                "score_label": "120pt",
                "interest_level": 2,
                "category": "Security",
                "note": "",
            },
        ],
    }

    html = render_digest_html(digest)

    assert "記事タイトルその1" in html
    assert 'href="https://example.com/article1"' in html
    assert "Article Title 2" in html
    assert 'href="https://news.ycombinator.com/item?id=999"' in html
    assert "2026-07-10" in html
    assert "2件" in html


def test_render_digest_html_with_no_articles_shows_empty_state():
    digest = {"date": "2026-07-11", "articles": []}

    html = render_digest_html(digest)

    assert "0件" in html
    assert "該当する記事はありませんでした" in html


def test_render_digest_html_escapes_special_characters_in_title():
    digest = {
        "date": "2026-07-10",
        "articles": [
            {
                "id": "x-1",
                "source": "hatena_it",
                "title": "<script>alert('xss')</script> & \"quoted\"",
                "url": "https://example.com/a",
                "score_label": "1 users",
                "interest_level": 2,
                "category": "AI",
                "note": "",
            }
        ],
    }

    html = render_digest_html(digest)

    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html
    assert "&amp;" in html


def test_render_digest_html_treats_missing_interest_level_as_lowest():
    digest = {
        "date": "2026-07-10",
        "articles": [
            {
                "id": "x-1",
                "source": "hatena_it",
                "title": "評価欠損記事",
                "url": "https://example.com/a",
                "score_label": "1 users",
                "category": "AI",
                "note": "",
            }
        ],
    }

    html = render_digest_html(digest)

    assert "評価欠損記事" in html
    assert "1件" in html


def test_render_index_html_lists_dates_in_descending_order_with_links():
    html = render_index_html(["2026-07-08", "2026-07-10", "2026-07-09"])

    assert html.index("2026-07-10") < html.index("2026-07-09") < html.index("2026-07-08")
    assert 'href="2026-07-10.html"' in html


def test_render_index_html_with_no_dates_shows_empty_state():
    html = render_index_html([])

    assert "まだダイジェストがありません" in html
