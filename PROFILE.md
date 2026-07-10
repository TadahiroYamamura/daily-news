# 興味プロファイル

`morning-digest`スキルが記事の関連度を評価する際に参照する単一情報源。CLAUDE.mdではなくこのファイルを直接読み込むこと。

## 興味領域

- AI(開発とセキュリティへの応用)
- Webセキュリティ/ハッキング(OWASP、脆弱性、サプライチェーン攻撃)
- OSS開発/コミュニティ
- 個人開発/SaaS運営(Technical SEO、グロースハック、収益化)
- キャリア/人生哲学(経済的自由、外資転職、Build in Public)
- JavaScript/TypeScript技術スタック

## 収集ソース

### はてなブックマークIT(日本市場)

- https://b.hatena.ne.jp/hotentry/it
- https://b.hatena.ne.jp/hotentry/it/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0
- https://b.hatena.ne.jp/hotentry/it/AI%E3%83%BB%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92
- https://b.hatena.ne.jp/hotentry/it/%E3%81%AF%E3%81%A6%E3%81%AA%E3%83%96%E3%83%AD%E3%82%B0%EF%BC%88%E3%83%86%E3%82%AF%E3%83%8E%E3%83%AD%E3%82%B8%E3%83%BC%EF%BC%89
- https://b.hatena.ne.jp/hotentry/it/%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3%E6%8A%80%E8%A1%93
- https://b.hatena.ne.jp/hotentry/it/%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2

### Hacker News(グローバル)

- https://news.ycombinator.com/

### セキュリティ(追加ソース)

- https://www.aikido.dev/blog — セキュリティ研究開発者向けのセキュリティ情報
- https://www.wiz.io/blog — クラウドセキュリティ

最新1〜3記事をチェックし、興味度★★★のものがあれば注目トピックに含める。

### Reddit(13サブレディット)

`scripts/get_all_reddit.sh` で一括取得する。対象サブレディット:

netsec, cybersecurity, OpenAI, LocalLLaMA, ClaudeCode, programming, technology, opensource, indiehackers, webdev, javascript, cscareerquestions, productivity

- セキュリティ系: netsec, cybersecurity — 最新の脅威、実践的な攻撃・防御手法
- AI系: OpenAI, LocalLLaMA, ClaudeCode — OpenAI、ローカルLLM、Claude Code関連
- OSS/個人開発系: opensource, indiehackers, webdev, javascript — OSSプロジェクト、個人開発、Web開発
- キャリア/実践系: cscareerquestions, productivity — キャリア、生産性

## 興味度★評価基準

- ★★★: 興味領域に直接関連(AI×セキュリティ、OSS、個人開発、キャリアなど)
- ★★: 間接的に関連(技術トレンド全般、エンジニアリング文化)
- ★: 一般的なIT/技術ニュース

## 配信フィルタ基準

- `digests/YYYY-MM-DD.json`に書き出すのは `interest_level >= 2`(★★以上)の記事のみとする
- ★1件のみの記事はGitHub Pagesの一覧には出さず、収集ログとしても残さない(ノイズを増やさないため)

## 更新履歴

- 初版: `trend-daily`スキル(life リポジトリ)にハードコードされていた興味領域を、単一情報源として本ファイルに切り出した
