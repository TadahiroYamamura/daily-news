import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_digest import build, validate_digest


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


def _write_digest(path, date, articles):
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"date": date, "articles": articles}), encoding="utf-8")


def test_build_validates_the_file_for_the_given_date(tmp_path):
    _write_digest(tmp_path / "2026-07-14.json", "2026-07-14", [_valid_article(url="")])

    errors = build("2026-07-14", digests_dir=tmp_path)

    assert any("url" in e for e in errors)


def test_build_defaults_to_the_most_recent_digest_file_when_date_omitted(tmp_path):
    _write_digest(tmp_path / "2026-07-14.json", "2026-07-14", [_valid_article()])
    _write_digest(tmp_path / "2026-07-15.json", "2026-07-15", [_valid_article(url="")])

    errors = build(digests_dir=tmp_path)

    assert any("url" in e for e in errors)
