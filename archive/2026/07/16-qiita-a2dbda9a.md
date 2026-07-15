# Elixir製NotebookLMクローン「Notex」をDocker (Ubuntu 24.04) で動かす＆ai& Inference検証

- URL: https://qiita.com/torifukukaiou/items/78314be5a6db95b13286
- 収集日: 2026-07-16
- カテゴリ: AI

## 要約

Elixir/PhoenixとLiveViewで実装されたNotebookLMクローン「Notex」を、Ubuntu 24.04ベースのDockerイメージ上で動かし、動作検証を行った記事です。ffmpegやopen-jtalk、fonts-noto-cjkなどを追加インストールし、日本語音声合成を伴う動画生成にも対応できる環境を構築しています。

検証中には2つの問題に遭遇しています。1つは開発環境の設定でバインドアドレスがループバック(127.0.0.1)に固定されていたためホストからアクセスできない問題で、`config/dev.exs`を修正して0.0.0.0バインドに変更することで解決しました。もう1つはソース追加時にLiveViewがクラッシュする問題で、パラメータのネスト化オプション`as: :source`の指定漏れが原因と特定し、該当する4箇所の`to_form`呼び出しに追加して修正しています。

修正後はRAGによる引用付き質問応答、マインドマップ生成、スライド生成、動画生成（テキスト台本からopen-jtalkでナレーションを生成しffmpegで字幕合成）といった主要機能が正常に動作することを確認しています。

さらにOpenAI互換API経由でai& Inferenceの「deepseek-ai/deepseek-v4-flash」モデルを使った検証も実施しており、baseURLを変更するだけでRAG機能はほぼそのまま動作した一方、動画生成機能はエラーが発生したとのことです。全体として、いくつかのバグ修正を経ればElixir製NotebookLMクローンをローカルDocker環境で実用的に動かせること、また複数のAIモデル(OpenAI公式APIやai& Inference)に対応できるアーキテクチャであることが示された体験レポートとなっています。
