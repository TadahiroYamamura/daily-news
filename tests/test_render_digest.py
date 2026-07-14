import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from render_digest import parse_checked_ids, render_digest_issue_body


def test_render_digest_issue_body_includes_each_article_as_checkbox_with_id():
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

    body = render_digest_issue_body(digest)

    assert "- [ ] [記事タイトルその1](https://example.com/article1)" in body
    assert "<!-- id:hatena-abc123 -->" in body
    assert "- [ ] [Article Title 2](https://news.ycombinator.com/item?id=999)" in body
    assert "<!-- id:hn-999 -->" in body
    assert "2026-07-10" in body
    assert "2件" in body
    assert "★★★" in body
    assert "興味領域とのマッチング理由" in body


def test_render_digest_issue_body_with_no_articles_shows_empty_state():
    digest = {"date": "2026-07-11", "articles": []}

    body = render_digest_issue_body(digest)

    assert "0件" in body
    assert "該当する記事はありませんでした" in body


def test_render_digest_issue_body_escapes_link_breaking_characters_in_title():
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

    body = render_digest_issue_body(digest)

    assert "[速報] あなたの<script>を破壊する方法" not in body
    assert r"\[速報\]" in body
    assert r"\<script\>" in body
    assert body.count("](https://example.com/a)") == 1


def test_render_digest_issue_body_treats_missing_interest_level_as_lowest():
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

    body = render_digest_issue_body(digest)

    assert "評価欠損記事" in body
    assert "1件" in body
    assert "★" in body


def test_parse_checked_ids_returns_only_checked_article_ids():
    body = """# 朝刊ダイジェスト 2026-07-10

2件

- [x] [記事1](https://example.com/a) — ★★★ ・ AI ・ 10 users
  メモ
  <!-- id:aaa-111 -->
- [ ] [記事2](https://example.com/b) — ★★ ・ Security ・ 5 users
  <!-- id:bbb-222 -->
"""

    checked = parse_checked_ids(body)

    assert checked == ["aaa-111"]


def test_parse_checked_ids_returns_empty_list_when_nothing_checked():
    body = "- [ ] [記事1](https://example.com/a)\n  <!-- id:aaa-111 -->\n"

    assert parse_checked_ids(body) == []
