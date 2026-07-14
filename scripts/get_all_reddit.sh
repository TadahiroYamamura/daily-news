#!/usr/bin/env bash
# 全サブレッドのホット記事を一括取得する
# 出力フォーマット: ===subreddit=== の後に "id | ups ups | cmts cmts | URL | タイトル" が続く
# id は fetch_sources.py の article_id() と同じ規則(sha1(url)の先頭8桁、source接頭辞つき)で
# このスクリプト自身が算出する。LLMに手計算させないことで決定論性を保つ。

ua="trend-collector/1.0 (trend analysis tool)"
subreddits=(netsec cybersecurity OpenAI LocalLLaMA ClaudeCode programming technology opensource indiehackers webdev javascript cscareerquestions productivity)

for sub in "${subreddits[@]}"; do
    echo "===${sub}==="
    curl -s -H "User-Agent: $ua" "https://old.reddit.com/r/${sub}/hot.json?t=day&limit=10" \
        | jq -r '.data.children[] | "\(.data.ups)\t\(.data.num_comments)\thttps://www.reddit.com\(.data.permalink)\t\(.data.title)"' \
        | while IFS=$'\t' read -r ups cmts url title; do
            id="reddit_${sub}-$(printf '%s' "$url" | sha1sum | cut -c1-8)"
            echo "${id} | ${ups} ups | ${cmts} cmts | ${url} | ${title}"
        done
    sleep 1.5
done
