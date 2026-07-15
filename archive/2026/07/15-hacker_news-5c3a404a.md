# HTMXをGoでどう使っているか

- URL: https://news.ycombinator.com/item?id=48912175
- 収集日: 2026-07-15
- カテゴリ: エンジニアリング文化

## 要約

元記事: How I use HTMX with Go (https://www.alexedwards.net/blog/how-i-use-htmx-with-go)

Alex EdwardsによるブログでGo言語とHTMXを組み合わせた開発手法を解説した記事。JavaScriptフレームワークに頼らず、サーバーサイドでHTMLを返しHTMXで部分的に画面を更新するというシンプルな構成を志向している。

コメント欄では、Go・Unix・SQLiteを組み合わせた「GUSスタック」や、それにHTMXを加えた「HUGSスタック」といった呼称が挙がり、同様の構成を採用している開発者から支持する声が複数寄せられた。一方で、HTMXは生産性を高める一方「複雑性がコード量の2倍の速度で増加する」という懸念も示され、Mantineなど他のUIライブラリを代替案として挙げる意見もあった。

その他、よりシンプルで強力だとする「Datastar」への言及や、SvelteKitがハイパーテキスト志向の哲学に合致しているという評価もあった。またAlpineJSと組み合わせた場合のライブコラボレーション機能の限界を指摘し、より高度なインタラクションには追加の工夫が必要という指摘もあった。
