import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_digest import validate_digest


def _valid_article(**overrides):
    article = {
        "id": "hatena_it-a1b2c3d4",
        "source": "hatena_it",
        "title": "記事タイトル",
        "url": "https://example.com/article",
        "score_label": "312 users",
        "interest_level": 3,
        "category": "AI",
        "note": "興味領域とのマッチング理由",
    }
    article.update(overrides)
    return article


def test_validate_digest_returns_no_errors_for_valid_digest():
    digest = {"date": "2026-07-15", "articles": [_valid_article()]}

    assert validate_digest(digest) == []


def test_validate_digest_flags_missing_required_field():
    digest = {"date": "2026-07-15", "articles": [_valid_article(url="")]}

    errors = validate_digest(digest)

    assert any("url" in e for e in errors)


def test_validate_digest_flags_duplicate_ids():
    digest = {
        "date": "2026-07-15",
        "articles": [_valid_article(), _valid_article()],
    }

    errors = validate_digest(digest)

    assert any("重複" in e for e in errors)


def test_validate_digest_flags_invalid_source():
    digest = {"date": "2026-07-15", "articles": [_valid_article(source="reddit")]}

    errors = validate_digest(digest)

    assert any("source" in e for e in errors)


def test_validate_digest_flags_interest_level_below_filter_threshold():
    digest = {"date": "2026-07-15", "articles": [_valid_article(interest_level=1)]}

    errors = validate_digest(digest)

    assert any("interest_level" in e for e in errors)


def test_validate_digest_flags_missing_interest_level():
    article = _valid_article()
    del article["interest_level"]
    digest = {"date": "2026-07-15", "articles": [article]}

    errors = validate_digest(digest)

    assert any("interest_level" in e for e in errors)


def test_validate_digest_flags_missing_date():
    digest = {"articles": [_valid_article()]}

    errors = validate_digest(digest)

    assert any("date" in e for e in errors)


def test_validate_digest_flags_articles_not_a_list():
    digest = {"date": "2026-07-15", "articles": "not-a-list"}

    errors = validate_digest(digest)

    assert any("articles" in e for e in errors)


def test_validate_digest_allows_empty_score_label_for_sources_without_counts():
    digest = {
        "date": "2026-07-15",
        "articles": [_valid_article(source="zenn", score_label="")],
    }

    assert validate_digest(digest) == []
