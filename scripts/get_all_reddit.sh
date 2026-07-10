#!/usr/bin/env bash
# 全サブレッドのホット記事を一括取得する
# 出力フォーマット: ===subreddit=== の後に "ups | cmts | URL | タイトル" が続く

ua="trend-collector/1.0 (trend analysis tool)"
subreddits=(netsec cybersecurity OpenAI LocalLLaMA ClaudeCode programming technology opensource indiehackers webdev javascript cscareerquestions productivity)

for sub in "${subreddits[@]}"; do
    echo "===${sub}==="
    curl -s -H "User-Agent: $ua" "https://old.reddit.com/r/${sub}/hot.json?t=day&limit=10" \
        | jq -r '.data.children[] | "\(.data.ups) ups | \(.data.num_comments) cmts | https://www.reddit.com\(.data.permalink) | \(.data.title)"'
    sleep 1.5
done
