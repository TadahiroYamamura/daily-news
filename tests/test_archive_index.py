import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from archive_index import render_archive_links


def _write(path, title, body="本文"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n- URL: https://example.com\n\n## 要約\n\n{body}\n", encoding="utf-8")


def test_render_archive_links_lists_titles_with_github_blob_urls(tmp_path):
    _write(tmp_path / "2026" / "07" / "14-hatena_it-aaa.md", "記事タイトル1")
    _write(tmp_path / "2026" / "07" / "14-hacker_news-bbb.md", "記事タイトル2")
    _write(tmp_path / "2026" / "07" / "15-hatena_it-ccc.md", "別の日の記事")  # 対象外の日付

    body = render_archive_links(
        "2026-07-14",
        archive_dir=tmp_path,
        repo="TadahiroYamamura/daily-news",
        branch="develop",
    )

    assert "記事タイトル1" in body
    assert "記事タイトル2" in body
    assert "別の日の記事" not in body
    assert (
        "https://github.com/TadahiroYamamura/daily-news/blob/develop/archive/2026/07/14-hatena_it-aaa.md"
        in body
    )
    assert (
        "https://github.com/TadahiroYamamura/daily-news/blob/develop/archive/2026/07/14-hacker_news-bbb.md"
        in body
    )


def test_render_archive_links_returns_empty_state_when_no_files(tmp_path):
    body = render_archive_links(
        "2026-07-14",
        archive_dir=tmp_path,
        repo="TadahiroYamamura/daily-news",
        branch="develop",
    )

    assert "アーカイブはまだありません" in body


def test_render_archive_links_sorts_alphabetically_by_filename(tmp_path):
    _write(tmp_path / "2026" / "07" / "14-zzz.md", "後の記事")
    _write(tmp_path / "2026" / "07" / "14-aaa.md", "先の記事")

    body = render_archive_links(
        "2026-07-14",
        archive_dir=tmp_path,
        repo="TadahiroYamamura/daily-news",
        branch="develop",
    )

    assert body.index("先の記事") < body.index("後の記事")
