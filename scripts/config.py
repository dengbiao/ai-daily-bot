#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 配置文件

# RSS源配置 - AI相关优质新闻源
RSS_FEEDS = [
    {
        "name": "MIT Technology Review AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
        "category": "news"
    },
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/feed",
        "category": "company"
    },
    {
        "name": "AI Trends",
        "url": "https://www.aitrends.com/feed/",
        "category": "news"
    },
    {
        "name": "KDnuggets",
        "url": "https://www.kdnuggets.com/feed",
        "category": "blog"
    }
]

# HuggingFace Daily Papers 配置
HF_DAILY_PAPERS_URL = "https://huggingface.co/papers/daily"
MAX_PAPERS = 10

# GitHub Trending 配置
GITHUB_TRENDING_URL = "https://api.github.com/search/repositories"
GITHUB_TRENDING_PARAMS = {
    "q": "topic:artificial-intelligence topic:machine-learning",
    "sort": "stars",
    "order": "desc",
    "per_page": 10
}
MAX_TRENDING_REPOS = 10

# 输出目录配置
POSTS_DIR = "_posts"

# 日期格式
DATE_FORMAT = "%Y-%m-%d"
POST_FILENAME_FORMAT = "%Y-%m-%d-ai-daily.md"
