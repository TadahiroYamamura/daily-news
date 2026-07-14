---
name: morning-digest
description: "毎朝のニュース収集とGitHub Pagesダイジェスト生成"
---

# 朝刊ダイジェスト収集

Hacker News・Lobsters・はてなブックマークIT人気エントリー・Zenn・Qiita・追加セキュリティソースを収集し、`digests/YYYY-MM-DD.json` に保存した上で、GitHub Pages公開用のHTML(`docs/`)を生成してcommit+pushする。

## 実行手順

### 0. 興味プロファイル・収集ソース読み込み

`PROFILE.md`(興味領域・★評価基準)と`SOURCES.md`(収集ソース一覧)を読み込む。CLAUDE.mdは参照しない(これらのファイルが単一情報源)。

### 1. トレンド情報の収集

データ取得はLLMによるページ読解(WebFetch)に頼らず、構造化API/RSS(Atom含む)を決定論的にパースするスクリプトで行う。実行のたびに抽出結果がブレるのを防ぐため、**この手順以外の方法(WebFetchでのスクレイピング等)でタイトル・URL・スコアを抽出してはならない**。

- `scripts/fetch_sources.py` を**1回だけ**実行し、標準出力のJSON配列を取得する(`source` / `id` / `title` / `url` / `score_label` 等が構造化済み)

```bash
python3 scripts/fetch_sources.py
```

Hacker News・Lobsters・はてなブックマークIT・Zenn・Qiita・セキュリティブログ(aikido.dev/wiz.io)すべてがこの1回の実行に含まれる。この時点でタイトル・URL・スコアはすべて確定しており、LLMが行うのは以降の翻訳と評価のみである。

### 2. 翻訳・分析・興味度評価

- 英語のタイトル(Hacker News・セキュリティブログ)は日本語に翻訳する
- `PROFILE.md`の「興味度★評価基準」に従い、各記事を★1〜3で評価する。興味領域とのマッチングを最優先の観点とする
- `id`は`fetch_sources.py`の出力に既に含まれている値をそのまま使う。**LLMが新たにIDを考案・計算してはならない**(ハッシュの手計算は毎回結果がブレるため、決定論性が崩れる)

### 3. JSON書き出し

`dev-docs/digest-schema.md`の「配信フィルタ基準」に従い、`interest_level >= 2`(★★以上)の記事のみを抽出し、`digests/YYYY-MM-DD.json`(実行日の日付)に以下の形式で書き出す。

```json
{
  "date": "YYYY-MM-DD",
  "articles": [
    {
      "id": "hatena_it-a1b2c3d4",
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

- `id`・`source`・`url`・`score_label`は`fetch_sources.py`の出力をそのまま転記する(`id`はアーカイブファイル名にも再利用する)
- `interest_level`・`category`・`note`はこのステップでLLMが付与する

詳細なスキーマは `dev-docs/digest-schema.md` を参照。

### 4. HTML生成

```bash
python3 scripts/render_digest.py
```

`digests/*.json` すべてから `docs/YYYY-MM-DD.html` と `docs/index.html` を再生成する。

### 5. commit + push

```bash
git add digests/ docs/
git commit -m "docs: YYYY-MM-DDの朝刊ダイジェストを追加"
git push
```

**このリポジトリでは `digests/` と `docs/` 以外のGit履歴を操作してはならない。**

## 注意事項

- データ取得は`scripts/fetch_sources.py`のみを用いる。WebFetchでのページスクレイピングによる代替は行わない(決定論性が崩れるため)
- すべての記事にURLリンクを必ず含める(リンクなしは不可)
- 英語のタイトルは日本語に翻訳する
- 投票数(ups)/コメント数/ポイント数が高い記事を優先する
- `digests/YYYY-MM-DD.json`のYYYY-MM-DDは実行日の日付を使用する
- 完了したら「ダイジェスト収集完了。」と一言メッセージを返す(Remote Control経由で確認しているユーザーに伝わるようにする)
