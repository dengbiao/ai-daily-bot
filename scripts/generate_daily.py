#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from typing import List, Dict

# 导入各个模块
from scripts.huggingface import get_daily_papers
from scripts.github_trending import get_trending_repos
from scripts.rss_parser import get_recent_news
from scripts.config import POSTS_DIR, POST_FILENAME_FORMAT, DATE_FORMAT

def ensure_dir():
    """确保posts目录存在"""
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

def generate_markdown(date: datetime, papers: List[Dict], repos: List[Dict], news: List[Dict]) -> str:
    """生成日报markdown内容"""
    date_str = date.strftime("%Y年%m月%d日")
    
    content = f"""---
title: 每日AI日报 - {date_str}
date: {date.strftime(DATE_FORMAT)}
categories: daily-ai-news
tags: AI, daily-news, paper, open-source
excerpt: {len(papers)}篇最新论文 · {len(repos)}个热门开源项目 · {len(news)}条行业新闻
---

这里是今天AI领域的最新进展，包含最新论文、热门开源项目和行业新闻，所有内容均可点击链接查看原始来源。

"""

    # 添加论文部分
    if papers:
        content += f"\n## 📄 最新AI论文\n\n"
        for paper in papers:
            abstract = paper['abstract'] if paper['abstract'] and paper['abstract'] != '无描述' else '暂无摘要'
            content += f"""<div class="post-item mb-4 p-3 border rounded">
### [{paper['title']}]({paper['url']}){{:target="_blank" rel="noopener"}}

| 信息 |  |
|------|------|
| 作者 | {paper['authors']} |
| 热度 | {paper['votes']} downloads |
| 来源 | [{paper['source']}]({paper['url']}){{:target="_blank" rel="noopener"}} |

{abstract}

[查看原文 →]({paper['url']}){{: .btn .btn-outline-primary .btn-sm target="_blank" rel="noopener"}}
</div>

"""

    # 添加热门仓库部分
    if repos:
        content += f"\n## ⭐ GitHub热门AI仓库\n\n"
        for repo in repos:
            desc = repo['description'] if repo['description'] else '暂无描述'
            lang = repo['language'] if repo['language'] and repo['language'] != '未知' else '多种语言'
            content += f"""<div class="post-item mb-4 p-3 border rounded">
### [{repo['name']}]({repo['url']}){{:target="_blank" rel="noopener"}}

| 信息 |  |
|------|------|
| 语言 | {lang} |
| Star/Fork | {repo['stars']} / {repo['forks']} |
| 描述 | {desc} |

[查看仓库 →]({repo['url']}){{: .btn .btn-outline-primary .btn-sm target="_blank" rel="noopener"}}
</div>

"""

    # 添加新闻部分
    if news:
        content += f"\n## 📰 AI领域新闻\n\n"
        for item in news:
            summary = item['summary'][:250] + '...' if len(item['summary']) > 250 else item['summary']
            content += f"""<div class="post-item mb-4 p-3 border rounded">
### [{item['title']}]({item['url']}){{:target="_blank" rel="noopener"}}

| 信息 |  |
|------|------|
| 发布时间 | {item['published']} |
| 来源 | {item['source_name']} |

{summary}

[阅读原文 →]({item['url']}){{: .btn .btn-outline-primary .btn-sm target="_blank" rel="noopener"}}
</div>

"""

    # 添加页脚
    content += """
---

*本日报由AI自动生成，数据来源于HuggingFace Daily Papers、GitHub Trending和各大AI媒体RSS源。*
"""

    return content

def save_post(content: str, date: datetime):
    """保存markdown文件到_posts目录"""
    filename = date.strftime(POST_FILENAME_FORMAT)
    filepath = os.path.join(POSTS_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"日报已保存到: {filepath}")
    return filepath

def main():
    """主函数"""
    print("开始生成今日AI日报...")
    
    # 确保目录存在
    ensure_dir()
    
    # 获取今天日期
    today = datetime.now()
    
    # 获取各个数据源
    print("正在抓取HuggingFace每日论文...")
    papers = get_daily_papers()
    print(f"获取到 {len(papers)} 篇论文")
    
    print("正在抓取GitHub热门AI仓库...")
    repos = get_trending_repos()
    print(f"获取到 {len(repos)} 个热门仓库")
    
    print("正在获取RSS新闻...")
    news = get_recent_news(days=7)
    print(f"获取到 {len(news)} 条新闻")
    
    # 生成markdown
    print("正在生成markdown...")
    content = generate_markdown(today, papers, repos, news)
    
    # 保存文件
    filepath = save_post(content, today)
    
    print("生成完成!")
    
    # 检查是否有内容
    total = len(papers) + len(repos) + len(news)
    if total == 0:
        print("警告: 没有获取到任何内容!")
        exit(1)

if __name__ == "__main__":
    main()
