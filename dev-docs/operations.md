# 運用手順

## 初回セットアップ

1. このリポジトリをGitHubにpushする(例: `TadahiroYamamura/news`)
2. リポジトリの公開範囲(public/private)を決める。GitHub Pagesの設定は不要(ダイジェストはGitHub Issueとして投稿するため)
3. リポジトリ直下に`.env`を作成し、`GITHUB_TOKEN=<fine-grained PAT等>`を設定する(`.gitignore`済み)。`gh`コマンドの認証には`gh auth login`のkeyringではなく、この`.env`を`scripts/gh.sh`経由で読み込む方式を使う(keyringのアカウント状態に依存しないため)
4. `scripts/gh.sh label create digest`で`digest`ラベルを作成する(未作成の場合)
5. この端末でRemote Controlを有効化する
   - 対話セッション内で `/remote-control` を実行、またはターミナルで `claude remote-control`
   - スマホのClaudeアプリでQRコードをスキャンしてペアリングする
6. 毎朝7時の収集を`/loop`で設定する(下記「`/loop`の再設定」を参照)

## `/loop`の再設定(毎週必要)

`/loop`は最大7日で自動失効する。以下を目安に再設定する。

```
/loop 毎朝7:00にmorning-digestスキルを実行して
```

- 失効に気づかず放置すると、その日から収集が止まる。カレンダーリマインダー等で「週1回`/loop`を確認する」運用をユーザー側で持つこと
- セッションがidleでない(何か別の作業中)場合、`/loop`の発火はスキップまたは遅延する

## Remote Controlでの深掘り

1. スマホのGitHubアプリ/モバイルブラウザで`digest`ラベルのIssueを開き、気になった記事のチェックボックスをタップする(この時点ではClaudeへの依頼は不要、後でまとめて処理する)
2. 都合の良いタイミングでClaudeアプリを開き、Remote Controlでこの端末のセッションに接続して「今日のIssueをチェックして」等と依頼する
3. Claudeがチェック済みの記事を洗い出し、それぞれ取得・要約して`archive/YYYY/MM/DD-<slug>.md`として保存・commit・pushする(規約は`README.md`を参照)
4. ネットワークが10分以上不通になるとRemote Control接続はタイムアウトする。再接続すれば復帰する

## トラブルシューティング

| 症状 | 確認ポイント |
|---|---|
| 朝になってもIssueが作成されていない | `/loop`が失効していないか、この端末が起動・ネットワーク接続されているかを確認。`scripts/gh.sh auth status`で`.env`の`GITHUB_TOKEN`が有効か確認 |
| Remote Controlから接続できない | この端末でClaude Codeプロセスが動作中か確認。プロセスが落ちていれば`claude remote-control`を再実行 |
| 深掘りの要約が返ってこない | ネットワーク切断によるタイムアウトの可能性。再接続して再度依頼する |
