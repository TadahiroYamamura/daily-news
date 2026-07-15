# digests/*.json スキーマ

`morning-digest`スキルが書き出し、`scripts/render_digest.py`が読み込むJSONの形式。

```json
{
  "date": "2026-07-10",
  "articles": [
    {
      "id": "hatena-abc123",
      "source": "hatena_it",
      "title": "記事タイトル",
      "url": "https://example.com/article",
      "score_label": "312 users",
      "interest_level": 3,
      "category": "AI",
      "note": "興味領域とのマッチング理由"
    }
  ]
}
```

## フィールド

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `date` | string | ○ | `YYYY-MM-DD`形式。ファイル名(`digests/YYYY-MM-DD.json`)と一致させる |
| `articles[].id` | string | ○ | ソース名+URLベースのスラッグ等、安定した識別子。`archive/YYYY/MM/DD-<slug>.md`のファイル名にも流用する |
| `articles[].source` | string | ○ | `hatena_it` / `hacker_news` / `lobsters` / `zenn` / `qiita` / `security_blog_aikido` / `security_blog_wiz` のいずれか |
| `articles[].title` | string | ○ | 日本語(英語記事は翻訳済み) |
| `articles[].url` | string | ○ | はてブ=元記事URL、HN/Lobsters=コメントページURL、Zenn/Qiita=記事URL |
| `articles[].score_label` | string | ○ | 表示用のスコア文字列(例: `312 users`, `120pt`)。Zenn/Qiita/セキュリティブログは件数指標がないため空文字列 |
| `articles[].interest_level` | number | 推奨 | 1〜3の★評価。欠損時は`render_digest.py`側で★1相当として扱う |
| `articles[].category` | string | ○ | `AI` / `Security` / `OSS` / `Career` 等の分類 |
| `articles[].note` | string | 任意 | 興味領域とのマッチング理由・発信への活用メモ |

## 配信フィルタ基準

- `digests/YYYY-MM-DD.json`に書き出すのは `interest_level >= 2`(★★以上、`PROFILE.md`の興味度★評価基準に基づく)の記事のみとする
- ★1件のみの記事はGitHub Issueの一覧には出さず、収集ログとしても残さない(ノイズを増やさないため)

## 契約上の注意

- `scripts/render_digest.py`はこのファイルの内容をそのままGitHub Issue本文(チェックボックス付き、末尾に`<!-- id:... -->`で`id`を埋め込む)に変換する。フィールド名を変更する場合は`render_digest.py`と`tests/test_render_digest.py`を同一コミットで更新すること
- `scripts/validate_digest.py`はcommit前に必須フィールド漏れ・id重複・配信フィルタ基準(`interest_level >= 2`)違反を検証する。フィールド名や必須/任意の区分を変更する場合は`validate_digest.py`と`tests/test_validate_digest.py`も同一コミットで更新すること
