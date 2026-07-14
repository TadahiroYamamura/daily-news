#!/usr/bin/env python3
"""指定日にアーカイブされたarchive/*.mdへのリンク一覧を生成する。

深掘り完了後、この出力をGitHub Issueのコメントとして投稿することで、
Issue本文(チェックボックス)を書き換えずに要約への導線を追加できる。
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = REPO_ROOT / "archive"


def _extract_title(path):
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    return first_line.removeprefix("# ").strip()


def render_archive_links(date, archive_dir=ARCHIVE_DIR, repo="", branch="main"):
    year, month, day = date.split("-")
    day_dir = archive_dir / year / month
    prefix = f"{day}-"

    files = sorted(
        p for p in day_dir.glob(f"{prefix}*.md") if p.is_file()
    ) if day_dir.exists() else []

    if not files:
        return f"{date} のアーカイブはまだありません。\n"

    lines = [f"# {date} の深掘りアーカイブ({len(files)}件)\n"]
    for path in files:
        title = _extract_title(path)
        rel_path = f"archive/{year}/{month}/{path.name}"
        url = f"https://github.com/{repo}/blob/{branch}/{rel_path}"
        lines.append(f"- [{title}]({url})")

    return "\n".join(lines) + "\n"


def _detect_repo():
    url = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    # git@github.com:owner/repo.git または https://github.com/owner/repo.git を owner/repo に変換
    tail = url.split("github.com")[-1].lstrip(":/").removesuffix(".git")
    return tail


def _detect_branch():
    return subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="対象日付(YYYY-MM-DD)")
    args = parser.parse_args()
    sys.stdout.write(render_archive_links(args.date, repo=_detect_repo(), branch=_detect_branch()))
