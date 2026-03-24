#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import sys
sys.path.append('..')
from scripts.config import MAX_PAPERS, HF_DAILY_PAPERS_URL

def get_daily_papers() -> List[Dict]:
    """获取HuggingFace每日热门论文"""
    papers = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }
    
    # 使用HuggingFace搜索API获取最新热门AI论文
    try:
        print("正在通过API获取HuggingFace热门论文...")
        api_url = "https://huggingface.co/api/search/papers"
        params = {
            "limit": MAX_PAPERS,
            "sort": "last_modified",
            "direction": -1
        }
        api_response = requests.get(api_url, params=params, headers=headers, timeout=10)
        api_response.raise_for_status()
        data = api_response.json()
        
        for item in data:
            try:
                paper = {
                    "title": item.get("title", "无标题"),
                    "abstract": item.get("summary", "无摘要"),
                    "authors": item.get("authors", "未知作者"),
                    "url": f"https://huggingface.co/papers/{item.get('id', '')}",
                    "votes": f"{item.get('upvotes', 0)} votes",
                    "source": "HuggingFace Papers"
                }
                if isinstance(paper["authors"], list):
                    paper["authors"] = ", ".join([a.get("name", "") if isinstance(a, dict) else str(a) for a in paper["authors"]])
                if len(paper["abstract"]) > 300:
                    paper["abstract"] = paper["abstract"][:297] + "..."
                papers.append(paper)
            except Exception as e:
                print(f"解析单篇论文出错: {e}")
                continue
                
    except Exception as e:
        print(f"获取HuggingFace论文出错: {e}")
        
        # 尝试备用方式 - 获取最近热门论文
        try:
            print("尝试备用方式获取...")
            api_url = "https://huggingface.co/api/models"
            params = {
                "search": "ai paper",
                "limit": MAX_PAPERS,
                "sort": "downloads",
                "direction": -1
            }
            api_response = requests.get(api_url, params=params, headers=headers, timeout=10)
            if api_response.status_code == 200:
                data = api_response.json()
                for item in data[:MAX_PAPERS]:
                    paper = {
                        "title": item.get("modelId", "无标题"),
                        "abstract": item.get("description", "无描述"),
                        "authors": "未知作者",
                        "url": f"https://huggingface.co/{item.get('modelId', '')}",
                        "votes": f"{item.get('downloads', 0)} downloads",
                        "source": "HuggingFace Models"
                    }
                    if len(paper["abstract"]) > 300:
                        paper["abstract"] = paper["abstract"][:297] + "..."
                    papers.append(paper)
        except Exception as e2:
            print(f"备用方式也失败了: {e2}")
    
    return papers

if __name__ == "__main__":
    papers = get_daily_papers()
    print(f"获取到 {len(papers)} 篇论文")
    for p in papers:
        print(f"{p['title']} - {p['url']}")
