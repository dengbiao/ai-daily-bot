#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
from typing import List, Dict
import sys
sys.path.append('..')
from scripts.config import MAX_TRENDING_REPOS, GITHUB_TRENDING_URL, GITHUB_TRENDING_PARAMS

def get_trending_repos() -> List[Dict]:
    """获取GitHub热门AI仓库"""
    repos = []
    
    # 计算30天前的日期
    one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    query = f"{GITHUB_TRENDING_PARAMS['q']} created:>{one_month_ago}"
    
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": MAX_TRENDING_REPOS
    }
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'AI-Daily-Bot'
    }
    
    try:
        response = requests.get(GITHUB_TRENDING_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('items', []):
            repo = {
                "name": item['full_name'],
                "description": item['description'] or "无描述",
                "url": item['html_url'],
                "stars": item['stargazers_count'],
                "forks": item['forks_count'],
                "language": item['language'] or "未知",
                "created_at": item['created_at'],
                "source": "GitHub Trending"
            }
            repos.append(repo)
            
    except Exception as e:
        print(f"获取GitHub Trending出错: {e}")
    
    return repos

if __name__ == "__main__":
    repos = get_trending_repos()
    print(f"获取到 {len(repos)} 个热门仓库")
    for r in repos:
        print(f"{r['name']} - {r['stars']} stars - {r['url']}")
