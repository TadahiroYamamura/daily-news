---
name: morning-digest
description: "毎朝のニュース収集とダイジェスト生成"
---

# 朝刊ダイジェスト収集

Hacker News・Lobsters・はてなブックマークIT人気エントリー・Zenn・Qiita・追加セキュリティソースを収集し、`digests/YYYY-MM-DD.json` に保存してcommit+pushした上で、チェックボックス付きのGitHub Issueとして投稿する。GitHubの通常のファイル表示(blobビュー)ではMarkdownのチェックボックスはクリックできず、Issue/PR本文でのみタップでトグルできるため、この形式にしている。

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

`dev-docs/digest-schema.md`の「配信フィルタ基準」に従い、`interest_level >= 2`(★★以上)の記事のみを抽出し、`digests/YYYY-MM-DD.json`(実行日の日付)に以下の形式で書き出す。**中間ファイルやマージ用スクリプト(`python3 -c`等)を経由せず、Writeツールで最終形をそのまま1回で書き出す。** `fetch_sources.py`の出力は手順1の実行時点で会話コンテキスト上にあるため、そこから`id`・`source`・`url`・`score_label`を転記しつつ、`interest_level`・`category`・`note`(・英語記事の翻訳後`title`)をこのステップで直接付与すればよく、突き合わせのための別ファイルは不要。

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

### 3.5 スキーマ検証

commitする前に`scripts/validate_digest.py`で必須フィールド漏れ・id重複・配信フィルタ基準(`interest_level >= 2`)違反がないか機械的に検証する。引数無しで実行すると`digests/`内の最新ファイル(=今書き出したファイル)を自動検証する。

```bash
python3 scripts/validate_digest.py
```

エラーが出力された場合はJSONを修正してから再実行する。この検証は形式面のみを見るもので、★評価の妥当性そのもの(何が★3に値するか)はLLMの判断領域であり検証対象外。

### 4. commit + push

```bash
git add digests/
git commit -m "docs: YYYY-MM-DDの朝刊ダイジェストを追加"
git push
```

**このリポジトリでは `digests/` 以外のGit履歴を操作してはならない。**

### 5. GitHub Issueとして投稿

```bash
scripts/post_digest_issue.sh YYYY-MM-DD
```

`digests/YYYY-MM-DD.json` を元にチェックボックス付きのIssue本文を生成し、タイトル・ラベルを固定値で組み立てて`gh issue create`まで実行する(内部で`scripts/gh.sh`経由の`render_digest.py`+`gh issue create`を行う)。エージェント側は日付を渡すだけでよく、`--title`や`--label`等のオプションを都度組み立てる必要はない。各記事は`- [ ] [タイトル](URL) — ★評価 ・ カテゴリ ・ スコア`の1行(必要なら次行にメモ)、末尾に`<!-- id:記事id -->`というHTMLコメントで`digests/*.json`の`id`を埋め込む(表示はされないが、後で深掘り対象を特定するための機械可読な手がかりになる)。`digest`ラベルが存在しない場合は事前に`scripts/gh.sh label create digest`で作成しておく。

**`gh`コマンドは直接使わず、必ず`scripts/gh.sh`(`.env`の`GITHUB_TOKEN`を読み込んで`gh`を実行するラッパー)を経由すること。** `.env`を直接読む・sourceすることは禁止(`.claude/settings.json`のdenyルールでも制限している)。

## 注意事項

- データ取得は`scripts/fetch_sources.py`のみを用いる。WebFetchでのページスクレイピングによる代替は行わない(決定論性が崩れるため)
- `digests/YYYY-MM-DD.json`はWriteツールで直接書き出す。`python3 -c`等でのJSON組み立て・マージは行わない(承認プロンプトの増加要因になる上、判断を伴わない転記作業に外部プロセスは不要)
- Issue投稿は`scripts/post_digest_issue.sh`のみを用いる。深掘り時の`gh issue list`/`gh issue view`など読み取り系は`scripts/gh.sh`経由で行う
- すべての記事にURLリンクを必ず含める(リンクなしは不可)
- 英語のタイトルは日本語に翻訳する
- 投票数(ups)/コメント数/ポイント数が高い記事を優先する
- `digests/YYYY-MM-DD.json`のYYYY-MM-DDは実行日の日付を使用する
- 完了したら「ダイジェスト収集完了。」と一言メッセージを返す(Remote Control経由で確認しているユーザーに伝わるようにする)
- Issueのチェックボックスを見て深掘り・アーカイブする流れ(このスキルの対象外、Remote Control経由で別途依頼された時のみ行う)は`README.md`の「深掘り→アーカイブの規約」を参照
