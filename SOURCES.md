# 収集ソース

`morning-digest`スキルが収集対象とする情報源の一覧。興味関心の中身は`PROFILE.md`を参照。

`scripts/fetch_sources.py`が下記すべてを1回の実行で決定論的に取得する(API/RSSを構造化データとしてパースするため、実行のたびに抽出結果がブレない)。Reddit(13サブレディット)は別途`scripts/get_all_reddit.sh`で取得する。

## はてなブックマークIT(日本市場)

- https://b.hatena.ne.jp/hotentry/it.rss(総合IT、30件)

IT配下の詳細カテゴリ(プログラミング/AI・機械学習/セキュリティ技術/エンジニア等)には専用RSSが存在しないため、この総合フィードから`morning-digest`スキルの興味度評価ステップでカテゴリ・関連度を判定する。

## Hacker News(グローバル)

- https://hacker-news.firebaseio.com/v0/topstories.json 経由、上位30件(Firebase API)

## セキュリティ(追加ソース、各最新3件)

- https://www.aikido.dev/blog/rss.xml — セキュリティ研究開発者向けのセキュリティ情報
- https://www.wiz.io/feed/rss.xml — クラウドセキュリティ

## Reddit(13サブレディット)

`scripts/get_all_reddit.sh` で一括取得する。対象サブレディット:

netsec, cybersecurity, OpenAI, LocalLLaMA, ClaudeCode, programming, technology, opensource, indiehackers, webdev, javascript, cscareerquestions, productivity

- セキュリティ系: netsec, cybersecurity — 最新の脅威、実践的な攻撃・防御手法
- AI系: OpenAI, LocalLLaMA, ClaudeCode — OpenAI、ローカルLLM、Claude Code関連
- OSS/個人開発系: opensource, indiehackers, webdev, javascript — OSSプロジェクト、個人開発、Web開発
- キャリア/実践系: cscareerquestions, productivity — キャリア、生産性
