import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from render_digest import render_digest_markdown


def test_render_digest_markdown_includes_each_article_title_and_link():
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

    md = render_digest_markdown(digest)

    assert "[記事タイトルその1](https://example.com/article1)" in md
    assert "[Article Title 2](https://news.ycombinator.com/item?id=999)" in md
    assert "2026-07-10" in md
    assert "2件" in md
    assert "★★★" in md
    assert "興味領域とのマッチング理由" in md


def test_render_digest_markdown_with_no_articles_shows_empty_state():
    digest = {"date": "2026-07-11", "articles": []}

    md = render_digest_markdown(digest)

    assert "0件" in md
    assert "該当する記事はありませんでした" in md


def test_render_digest_markdown_escapes_link_breaking_characters_in_title():
    digest = {
        "date": "2026-07-10",
        "articles": [
            {
                "id": "x-1",
                "source": "hatena_it",
                "title": "[速報] あなたの<script>を破壊する方法",
                "url": "https://example.com/a",
                "score_label": "1 users",
                "interest_level": 2,
                "category": "AI",
                "note": "",
            }
        ],
    }

    md = render_digest_markdown(digest)

    # 生の "]" "<script>" がリンク記法やHTMLタグとして解釈されないよう、エスケープされていること
    assert "[速報] あなたの<script>を破壊する方法" not in md
    assert r"\[速報\]" in md
    assert r"\<script\>" in md
    # リンク自体は壊れず、URLへの単一のリンクとして成立していること
    assert md.count("](https://example.com/a)") == 1


def test_render_digest_markdown_treats_missing_interest_level_as_lowest():
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

    md = render_digest_markdown(digest)

    assert "評価欠損記事" in md
    assert "1件" in md
    assert "★" in md
