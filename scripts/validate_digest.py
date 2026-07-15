#!/usr/bin/env python3
"""digests/*.json がdev-docs/digest-schema.mdのスキーマを満たしているか検証する。

LLMが直接digests/YYYY-MM-DD.jsonを書き出した後、commitする前に
機械的なフィールド漏れ・不整合を検出するためのチェックのみを行う。
興味度評価そのもの(interest_levelの妥当性の中身)はLLMの判断領域であり、
ここでは形式面(必須フィールド・重複id・配信フィルタ基準の逸脱)のみ検証する。
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIGESTS_DIR = REPO_ROOT / "digests"

REQUIRED_NON_EMPTY_FIELDS = ["id", "source", "title", "url", "category"]
# score_label はZenn/Qiita/セキュリティブログで件数指標が無いため空文字列を許容する(必須なのはキーの存在のみ)
REQUIRED_PRESENT_FIELDS = ["score_label"]
VALID_SOURCES = {
    "hatena_it",
    "hacker_news",
    "lobsters",
    "zenn",
    "qiita",
    "security_blog_aikido",
    "security_blog_wiz",
}
MIN_INTEREST_LEVEL = 2
VALID_INTEREST_LEVELS = (1, 2, 3)


def validate_digest(digest):
    errors = []

    if not digest.get("date"):
        errors.append("dateフィールドがありません")

    articles = digest.get("articles")
    if not isinstance(articles, list):
        errors.append("articlesが配列ではありません")
        return errors

    seen_ids = set()
    for index, article in enumerate(articles):
        label = article.get("id") or f"(id無し, {index}番目)"

        for field in REQUIRED_NON_EMPTY_FIELDS:
            if not article.get(field):
                errors.append(f"{label}: 必須フィールド'{field}'が空です")
        for field in REQUIRED_PRESENT_FIELDS:
            if field not in article:
                errors.append(f"{label}: 必須フィールド'{field}'がありません")

        article_id = article.get("id")
        if article_id:
            if article_id in seen_ids:
                errors.append(f"{label}: idが重複しています")
            seen_ids.add(article_id)

        source = article.get("source")
        if source and source not in VALID_SOURCES:
            errors.append(f"{label}: 不正なsource '{source}'")

        interest_level = article.get("interest_level")
        if interest_level is None:
            errors.append(f"{label}: interest_levelがありません")
        elif interest_level not in VALID_INTEREST_LEVELS:
            errors.append(f"{label}: interest_levelが不正な値です({interest_level})")
        elif interest_level < MIN_INTEREST_LEVEL:
            errors.append(
                f"{label}: interest_levelが{MIN_INTEREST_LEVEL}未満です(配信フィルタ基準違反)"
            )

    return errors


def _resolve_digest_path(date, digests_dir):
    if date:
        return digests_dir / f"{date}.json"

    files = sorted(digests_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"{digests_dir} にdigestファイルがありません")
    return files[-1]


def build(date=None, digests_dir=DIGESTS_DIR):
    digest_path = _resolve_digest_path(date, digests_dir)
    digest = json.loads(digest_path.read_text(encoding="utf-8"))
    return validate_digest(digest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="対象日付(YYYY-MM-DD)。省略時はdigests/内の最新ファイルを検証する",
    )
    args = parser.parse_args()

    errors = build(args.date)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)

    validated_path = _resolve_digest_path(args.date, DIGESTS_DIR)
    print(f"{validated_path.relative_to(REPO_ROOT)} は妥当です")
