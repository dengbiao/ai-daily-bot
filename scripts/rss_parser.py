#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import sys
sys.path.append('..')
from scripts.config import RSS_FEEDS

def get_recent_news(days: int = 7) -> List[Dict]:
    """从RSS源获取最近几天的AI新闻"""
    news = []
    cutoff_date = datetime.now() - timedelta(days=days)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for feed_info in RSS_FEEDS:
        try:
            print(f"正在获取 {feed_info['name']}...")
            # 使用requests获取内容
            import requests
            response = requests.get(feed_info["url"], headers=headers, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            
            if not feed.entries:
                print(f"{feed_info['name']} 没有条目")
                continue
                
            for entry in feed.entries:
                # 获取发布时间
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])
                else:
                    pub_date = datetime.now()
                
                # 只保留最近几天的新闻
                if pub_date >= cutoff_date:
                    summary = ""
                    if hasattr(entry, 'summary'):
                        summary = entry.summary
                    elif hasattr(entry, 'description'):
                        summary = entry.description
                    else:
                        summary = "无摘要"
                        
                    news_item = {
                        "title": entry.title,
                        "summary": summary,
                        "url": entry.link,
                        "published": pub_date.strftime("%Y-%m-%d"),
                        "source_name": feed_info["name"],
                        "source": f"{feed_info['name']} RSS"
                    }
                    # 清理HTML标签
                    from bs4 import BeautifulSoup
                    if news_item["summary"]:
                        soup = BeautifulSoup(news_item["summary"], 'html.parser')
                        news_item["summary"] = soup.get_text(strip=True)
                        if len(news_item["summary"]) > 300:
                            news_item["summary"] = news_item["summary"][:297] + "..."
                    
                    news.append(news_item)
            print(f"{feed_info['name']}: 找到 {len(feed.entries)} 条条目")
                    
        except Exception as e:
            print(f"解析RSS源 {feed_info['name']} 出错: {e}")
            continue
    
    # 按发布日期排序
    news.sort(key=lambda x: x["published"], reverse=True)
    return news

if __name__ == "__main__":
    news = get_recent_news(days=7)
    print(f"获取到 {len(news)} 条新闻")
    for n in news:
        print(f"{n['published']} - {n['title']} - {n['url']}")
