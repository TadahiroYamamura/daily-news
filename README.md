# news

毎朝の技術ニュース収集 → GitHubのブラウザ表示で閲覧 → Remote Controlで深掘り・アーカイブ、を行うリポジトリ。

設計の経緯・全体構成は `/home/develop/.claude/plans/tingly-greeting-lecun.md` を参照。

## ディレクトリ構成

```
news/
├── .claude/skills/morning-digest/SKILL.md  # 収集・評価・JSON/Markdown生成・commit/push
├── PROFILE.md                    # 興味プロファイルの単一情報源(興味領域・★評価基準)
├── SOURCES.md                    # 収集ソース一覧(HN/Lobsters/はてブ/Zenn/Qiita/セキュリティブログ)
├── scripts/
│   ├── fetch_sources.py          # 全ソースを決定論的に取得(API/RSS/Atom)
│   └── render_digest.py          # digests/*.json → digests/*.md
├── digests/YYYY-MM-DD.{json,md}  # 収集結果(json)とGitHub表示用Markdown(md)
├── archive/YYYY/MM/DD-<slug>.md  # 深掘り要約のアーカイブ
├── tests/
│   ├── test_fetch_sources.py
│   └── test_render_digest.py
├── dev-docs/                     # 開発・運用ドキュメント
└── README.md
```

データ取得(HN/Lobsters/はてブ/Zenn/Qiita/セキュリティブログ)はすべてAPI/RSS/Atomを構造化パースするスクリプトで行い、LLMによるページスクレイピング(WebFetch)には頼らない。実行のたびに抽出結果がブレるのを防ぐための設計判断。LLMが担うのは翻訳・興味度評価・深掘り要約のみ。

なお、Redditは`old.reddit.com`のJSON APIが家庭用ISP経由でも`403 blocked by network security`で安定してブロックされることを確認したため、収集対象から除外している(代わりにLobstersを採用)。

## 閲覧方法

GitHub Pagesやカスタムのビューアは使わず、GitHubの標準ブラウザ表示(`https://github.com/<owner>/news/blob/main/digests/YYYY-MM-DD.md`)でそのまま読む。この程度の一覧表示にHTML化・専用サイト配信は過剰と判断した。

## 深掘り→アーカイブの規約

Remote Control経由で記事の深掘りを依頼された場合、担当するClaudeセッションは以下に従うこと。

1. 対象記事の`id`(`digests/YYYY-MM-DD.json`内、または会話で示されたURL)を特定する
2. `archive/YYYY/MM/DD-<slug>.md`(その記事が`digests/`に登場した日付ディレクトリ、`<slug>`は`id`と同じ値)が既に存在するか確認する
   - 存在すればその内容を提示するだけでよい(再度WebFetchして要約し直す必要はない)
   - 存在しなければ、記事URLをWebFetchし要約を作成する
3. 新規作成する場合は以下のフォーマットで保存する

   ```markdown
   # <記事タイトル>

   - URL: <元記事/コメントページURL>
   - 収集日: YYYY-MM-DD
   - カテゴリ: <category>

   ## 要約

   <深掘り要約本文>
   ```

4. `git add archive/ && git commit -m "archive: <記事タイトルの要約>" && git push` を実行する

## 開発

- `render_digest.py`のテストは `python3 -m pytest tests/` で実行する
- コードにはHow、テストにはWhat、コミットログにはWhy、コードコメントにはWhy notを書く
