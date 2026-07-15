# AIにコードを書かせるなら技術スタックは何がいい？たどり着いたのはTypeScript中心＋必要な部分だけPython/Go

- URL: https://qiita.com/nogataka/items/3be907bb38b545cf4a9e
- 収集日: 2026-07-15
- カテゴリ: JS/TS

## 要約

本記事は、Claude CodeやCursorなどのAIエージェントにコードを書かせる際に最適な技術スタックをどう選ぶかを論じている。著者はAI駆動開発との相性を「LLMの言語理解度 × 型・LSPによる意味解析 × コンパイラ／テストの検証能力 × 規約の明確さ」という複合要因で捉え、生成後の誤りを機械的に検出できるかどうかがLLMの言語知識と同等以上に重要だと指摘する。

言語別の評価では、TypeScriptを最高評価とし、フロントエンド/バックエンドを統一言語で書けること、型情報とLSPの成熟により修正直後に機械が誤りを検出できる検証ループの速さを理由に挙げている。PythonはS-評価で「詳しいが壊れやすい」とし、型ヒント・Pydantic・Pyright(strict)・Ruff・pytestをセットで運用することを推奨。Goも同じくS-評価で、言語仕様がシンプルでLLMが読みやすく、コンパイルが速く単一バイナリ化しやすいため、Gateway・MCPサーバー・常駐サービスに適するとしている。

用途別には、Web/SaaSはNext.js/Vite + React + PostgreSQL + Drizzle/Prisma + Zodを中心としたTypeScript構成、AI・データ処理にはFastAPI + Pydantic + Pyright(strict)のPythonを追加、LLM Gatewayや常駐サービスにはnet/http + pgx + OpenTelemetryのGoを使うという段階的拡張を提案している。

技術選定以上に重要なのはリポジトリ設計の一貫性であり、`make check`によるformat→lint→typecheck→test→buildの検証コマンド固定、役割別のディレクトリ整理、OpenAPIによる言語間API契約の明示が実装上の一貫性を担保するとする。逆に、最初から複数言語を全部導入すること、新しすぎるフレームワーク、独自DSLやメタプログラミング、初期段階でのマイクロサービス化は避けるべきとし、計測結果に基づき必要な箇所だけ言語を分離する段階的アプローチを結論としている。
