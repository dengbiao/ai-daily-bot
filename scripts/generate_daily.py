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
categories: AI日报
tags: AI,每日新闻,论文,开源项目
---

# 每日AI日报 - {date_str}

这里是今天AI领域的最新进展，包含最新论文、热门开源项目和行业新闻。

"""

    # 添加论文部分
    if papers:
        content += f"\n## 📄 最新AI论文\n\n"
        for i, paper in enumerate(papers, 1):
            content += f"### {i}. [{paper['title']}]({paper['url']})\n\n"
            content += f"**作者**: {paper['authors']}  \n"
            content += f"**票数**: {paper['votes']}  \n"
            content += f"**摘要**: {paper['abstract']}  \n"
            content += f"**来源**: [{paper['source']}]({paper['url']})\n\n"

    # 添加热门仓库部分
    if repos:
        content += f"\n## ⭐ GitHub热门AI仓库\n\n"
        for i, repo in enumerate(repos, 1):
            content += f"### {i}. [{repo['name']}]({repo['url']})\n\n"
            content += f"**描述**: {repo['description']}  \n"
            content += f"**语言**: {repo['language']}  \n"
            content += f"**Star数**: {repo['stars']} | Fork数**: {repo['forks']}  \n"
            content += f"**来源**: [{repo['source']}]({repo['url']})\n\n"

    # 添加新闻部分
    if news:
        content += f"\n## 📰 AI领域新闻\n\n"
        for i, item in enumerate(news, 1):
            content += f"### {i}. [{item['title']}]({item['url']})\n\n"
            content += f"**发布**: {item['published']}  \n"
            content += f"**摘要**: {item['summary']}  \n"
            content += f"**来源**: [{item['source_name']}]({item['url']})\n\n"

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
