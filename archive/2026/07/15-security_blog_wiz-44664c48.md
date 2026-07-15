# M-Red-Team：GitHub Actions経由のAsyncAPIサプライチェーン侵害

- URL: https://www.wiz.io/blog/m-red-team-asyncapi-supply-chain-compromise-via-github-actions
- 収集日: 2026-07-15
- カテゴリ: Security

## 要約

攻撃者は「pwn request」と呼ばれる手法でAsyncAPIのGitHub Actionsを悪用した。asyncapi/generatorリポジトリのワークフローが`pull_request_target`を使いながらプルリクエスト側のコードをそのままチェックアウトして実行していたため、ベースリポジトリのシークレットにアクセスできる状態になっていた。2026年7月14日05:08 UTCに攻撃者は37個のPRを作成し、うち36個は偽の寄付ページを表示するカモフラージュ、残り1個に空白文字で難読化したJavaScriptペイロードを仕込んだ。自動レビューでは検出されたものの、ワークフローの実行自体は完了してしまい、ランナー環境をスキャンして`asyncapi-bot`サービスアカウントのPersonal Access Tokenを窃取し、rentry.co上のデッドドロップに外部送信された。

窃取したトークンを使い攻撃者は06:58 UTCに悪意あるコミットをプッシュし、07:10 UTCに@asyncapi/generator v3.3.1、@asyncapi/generator-helpers v1.1.1、@asyncapi/generator-components v0.7.1をnpmに公開、さらに07:51〜08:28 UTCにspec-json-schemasリポジトリへ11件のコミットを行い@asyncapi/specsのv6.11.2およびv6.11.2-alpha.1も公開した。これら侵害パッケージは合計で週300万ダウンロード規模の利用があり、影響範囲は大きい。マルウェアは多段構成で、パッケージのインポート時に第1ステージが実行され、IPFS経由で8.25MBの暗号化バンドル（第2ステージ）をダウンロード、最終的に約9万2千行に及ぶ第3ステージのマルウェアフレームワークがsystemdサービスとして永続化される。窃取対象はブラウザ保存パスワード（Chrome、Firefox、Edgeなど）、SSH鍵、npm/GitHubトークン、AWS認証情報、macOS Keychain、暗号資産ウォレットと多岐にわたる。

なお、悪用された脆弱性自体は4月29日に既に報告され、5月17日には修正PRも提出されていたが、58日間マージされずに放置されていたことが判明している。

対策として、開発者のワークステーションやCI/CD環境、リポジトリに侵害の痕跡がないか直ちに調査すること、GitHubトークン・SSH鍵・クラウド認証情報・CI/CDシークレットを一律ローテーションすることが推奨される。中長期的には、依存関係のホワイトリスト化、SBOM（ソフトウェア部品表）の生成、パッケージ検証の導入、ビルド環境の監視強化など、サプライチェーン全体の防御強化が求められる。
