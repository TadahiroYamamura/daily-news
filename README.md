# news

毎朝の技術ニュース収集 → GitHub Issueでチェックボックス選択 → Remote Controlで深掘り・アーカイブ、を行うリポジトリ。

設計上の大きな方向転換の経緯と今後の改善計画は `dev-docs/design-history.md` を参照。

## ディレクトリ構成

```
news/
├── .claude/skills/morning-digest/SKILL.md  # 収集・評価・JSON保存・Issue投稿
├── PROFILE.md                    # 興味プロファイルの単一情報源(興味領域・★評価基準)
├── SOURCES.md                    # 収集ソース一覧(HN/Lobsters/はてブ/Zenn/Qiita/セキュリティブログ)
├── scripts/
│   ├── fetch_sources.py          # 全ソースを決定論的に取得(API/RSS/Atom)
│   ├── render_digest.py          # digests/*.json → GitHub Issue本文(チェックボックス付き)
│   ├── gh.sh                     # .envのGITHUB_TOKENを読み込むghラッパー(gh直接使用は禁止)
│   ├── post_digest_issue.sh      # render_digest.py + gh issue create をまとめた投稿スクリプト
│   └── archive_index.py          # 指定日のarchive/*.mdへのリンク一覧を生成(Issueコメント用)
├── digests/YYYY-MM-DD.json       # 収集結果(データソースそのもの)
├── archive/YYYY/MM/DD-<slug>.md  # 深掘り要約のアーカイブ
├── tests/
│   ├── test_fetch_sources.py
│   └── test_render_digest.py
├── dev-docs/                     # 開発・運用ドキュメント
└── README.md
```

データ取得(HN/Lobsters/はてブ/Zenn/Qiita/セキュリティブログ)はすべてAPI/RSS/Atomを構造化パースするスクリプトで行い、LLMによるページスクレイピング(WebFetch)には頼らない。実行のたびに抽出結果がブレるのを防ぐための設計判断。LLMが担うのは翻訳・興味度評価・深掘り要約のみ。

なお、Redditは`old.reddit.com`のJSON APIが家庭用ISP経由でも`403 blocked by network security`で安定してブロックされることを確認したため、収集対象から除外している(代わりにLobstersを採用)。

## 閲覧・興味記事の選択

毎朝、GitHub Issue(`digest`ラベル)としてダイジェストを投稿する。GitHubの通常のファイル表示(blobビュー)ではMarkdownのチェックボックスはクリックできず、Issue/PR本文でのみタップでトグルできるため、この形式にしている。スマホのGitHubアプリ/モバイルブラウザでIssueを開き、気になった記事のチェックボックスをタップする。

## 深掘り→アーカイブの規約

Remote Control経由で「今日のIssueをチェックして」等の依頼を受けた場合、担当するClaudeセッションは以下に従うこと。

1. `scripts/gh.sh issue list --label digest --state open --json number,title` 等で対象のIssueを特定する(通常は最新のもの)
2. `scripts/gh.sh issue view <number> --json body --jq .body` で本文を取得し、`scripts/render_digest.py`の`parse_checked_ids()`と同じルール(`- [x]`の直後に現れる`<!-- id:... -->`)でチェック済みの記事`id`を洗い出す
3. 各`id`について、`archive/YYYY/MM/DD-<slug>.md`(その記事が`digests/`に登場した日付、`<slug>`は`id`と同じ値)が既に存在するか確認する
   - 存在すればその内容を提示するだけでよい(再度WebFetchして要約し直す必要はない)
   - 存在しなければ、記事URLをWebFetchし要約を作成する
4. 新規作成する場合は以下のフォーマットで保存する

   ```markdown
   # <記事タイトル>

   - URL: <元記事/コメントページURL>
   - 収集日: YYYY-MM-DD
   - カテゴリ: <category>

   ## 要約

   <深掘り要約本文>
   ```

5. `git add archive/ && git commit -m "archive: <記事タイトルの要約>" && git push` を実行する
6. その回の深掘りが完了したら、`python3 scripts/archive_index.py YYYY-MM-DD | scripts/gh.sh issue comment <number> --body-file -` でアーカイブへのリンク一覧をIssueのコメントとして投稿する。Issue本文(チェックボックス)は書き換えず、コメントとして追記する形にすることで、後からarchive/配下を直接探さなくてもIssueから要約に辿れるようにする

## 開発

- `render_digest.py`のテストは `python3 -m pytest tests/` で実行する
- コードにはHow、テストにはWhat、コミットログにはWhy、コードコメントにはWhy notを書く
