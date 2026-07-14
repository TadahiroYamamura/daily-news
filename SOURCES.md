# 収集ソース

`morning-digest`スキルが収集対象とする情報源の一覧。興味関心の中身は`PROFILE.md`を参照。

`scripts/fetch_sources.py`が下記すべてを1回の実行で決定論的に取得する(API/RSS/Atomを構造化データとしてパースするため、実行のたびに抽出結果がブレない)。

## Hacker News(グローバル)

- https://hacker-news.firebaseio.com/v0/topstories.json 経由、上位30件(Firebase API)

## Lobsters(グローバル)

- https://lobste.rs/hottest.json (公開JSON API、上位25件)

プログラミング・セキュリティ・AI関連のタグが充実したコミュニティ投票型のリンク集積サイト。Reddit(旧`old.reddit.com`のJSON API)は、家庭用ISP経由でも`403 blocked by network security`で安定してブロックされることを確認したため収集対象から外し、Lobstersに置き換えた。

## はてなブックマークIT(日本市場)

- https://b.hatena.ne.jp/hotentry/it.rss(総合IT、30件)

IT配下の詳細カテゴリ(プログラミング/AI・機械学習/セキュリティ技術/エンジニア等)には専用RSSが存在しないため、この総合フィードから`morning-digest`スキルの興味度評価ステップでカテゴリ・関連度を判定する。

## Zenn(日本語)

- https://zenn.dev/feed(トレンド、20件)

## Qiita(日本語)

- https://qiita.com/popular-items/feed(人気の記事、Atom形式、30件)

## セキュリティ(追加ソース、各最新3件)

- https://www.aikido.dev/blog/rss.xml — セキュリティ研究開発者向けのセキュリティ情報
- https://www.wiz.io/feed/rss.xml — クラウドセキュリティ
