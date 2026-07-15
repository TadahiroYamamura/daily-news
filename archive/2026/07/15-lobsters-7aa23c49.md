# git historyコマンドはもっと評価されるべき

- URL: https://lobste.rs/s/tb3el5/git_history_command_deserves_more
- 収集日: 2026-07-15
- カテゴリ: OSS

## 要約

元記事: The git history command deserves more attention (https://lalitm.com/post/git-history/)

Git 2.54・2.55で導入された実験的コマンド「git history」を紹介する記事。著者のLalit Maganti氏は、このコマンドがGit代替ツールとして注目されている「jj (Jujutsu)」の利点の多くを、既存のワークフローを変えることなく取り込めると主張している。history配下には`fixup`（古いコミットの修正内容を反映し、依存する後続ブランチを自動で再構築する）、`reword`（古いコミットメッセージを書き換えてスタック全体を再構築する）、`split`（1つのコミットをインタラクティブに2つへ分割する）という3つのサブコマンドがあり、いずれも作業ツリーを中途半端に壊れた状態にしないアトミックな操作として設計されている点、また追加インストール不要でGit本体に組み込まれている点が評価されている。

Lobstersのコメント欄では、jade_氏がGitのコミットハッシュが変更のたびに変わり長く扱いにくいことを課題として指摘し、変更ID（change ID）のような恒久的な識別子の必要性を述べている。Forty-Bot氏は記事中で触れられているrebaseの危険性について、`git rebase --abort`で復旧できると反論した。iconara氏は複雑なgitエイリアス設定を`git history fix`で置き換えられることに満足しており、将来jjへ移行してもこの知見は無駄にならないとコメント。wrs氏はjjの利点として永続的な変更ID、ファーストクラスのコンフリクト対応、シンプルなCLI設計を挙げ、比較の文脈を補足している。

全体として、jjのような新しいVCSへの乗り換えを検討する前に、Git自体が同様の使い勝手を提供し始めている点が話題の中心となっている。
