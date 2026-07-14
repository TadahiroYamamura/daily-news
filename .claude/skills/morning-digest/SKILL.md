---
name: morning-digest
description: "毎朝のニュース収集とGitHub Pagesダイジェスト生成"
---

# 朝刊ダイジェスト収集

はてなブックマークIT人気エントリー・Hacker News・Reddit(13サブレディット)・追加セキュリティソースを収集し、`digests/YYYY-MM-DD.json` に保存した上で、GitHub Pages公開用のHTML(`docs/`)を生成してcommit+pushする。

## 実行手順

### 0. 興味プロファイル・収集ソース読み込み

`PROFILE.md`(興味領域・★評価基準)と`SOURCES.md`(収集ソース一覧)を読み込む。CLAUDE.mdは参照しない(これらのファイルが単一情報源)。

### 1. トレンド情報の収集

`SOURCES.md`に列挙された各URLをWebFetchツールで取得する。

**はてなブックマークIT**
- 各エントリーの**タイトル、元記事URL、ブックマーク数**を必ず取得する
- はてブのエントリーページURLではなく、リンク先の元記事URLを抽出する
- 重複エントリーは削除する

**Hacker News**
- 各記事の**タイトル、HNコメントページURL(`https://news.ycombinator.com/item?id=XXXXX`形式)、ポイント数**を取得する
- 元記事URLではなくHNのコメントページURLを使用する(コメントも確認できるようにするため)
- タイトルは日本語に翻訳する

**セキュリティ(追加ソース)**
- 最新1〜3記事をチェックし、興味度★★★のものがあれば含める

**Reddit**
- `scripts/get_all_reddit.sh` を**1回だけ**実行して全13サブレディットのデータを取得する(Bash承認プロンプトの摩擦を避けるため一括スクリプト化されている)
- 各記事の**タイトル、Redditコメントページの完全URL、投票数(ups)、コメント数**を取得する
- 英語のタイトルは日本語に翻訳する

```bash
bash scripts/get_all_reddit.sh
```

### 2. 分析・興味度評価

`PROFILE.md`の「興味度★評価基準」に従い、各記事を★1〜3で評価する。興味領域とのマッチングを最優先の観点とする。

### 3. JSON書き出し

`dev-docs/digest-schema.md`の「配信フィルタ基準」に従い、`interest_level >= 2`(★★以上)の記事のみを抽出し、`digests/YYYY-MM-DD.json`(実行日の日付)に以下の形式で書き出す。

```json
{
  "date": "YYYY-MM-DD",
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

- `id`: ソース名+URLベースのスラッグなど、安定した識別子(後の深掘り時にアーカイブファイル名として再利用する)
- `source`: `hatena_it` / `hacker_news` / `reddit_<subreddit>` / `security_blog` のいずれか
- `score_label`: はてブなら`XXX users`、HNなら`XXXpt`、Redditなら`XXX ups`

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

- WebFetchツールを使用して情報を取得する
- すべての記事にURLリンクを必ず含める(リンクなしは不可)
- はてブは元記事のURLを必ず取得する(はてブページURLではなく)
- Hacker NewsはHNコメントページURL(`item?id=`形式)を使用する(元記事URLではなく)
- 英語のタイトルは日本語に翻訳する
- RedditはRedditコメントページの完全URL(`https://www.reddit.com/r/subreddit/comments/...`形式)を使用する
- Reddit APIレート制限に注意(1分あたり60リクエスト程度)
- 投票数(ups)/コメント数/ポイント数が高い記事を優先する
- `digests/YYYY-MM-DD.json`のYYYY-MM-DDは実行日の日付を使用する
- 完了したら「ダイジェスト収集完了。」と一言メッセージを返す(Remote Control経由で確認しているユーザーに伝わるようにする)
