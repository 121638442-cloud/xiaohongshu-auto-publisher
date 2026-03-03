# -*- coding: utf-8 -*-
import requests
import sys
from datetime import datetime

def get_github_ai_trending():
    url = "https://api.github.com/search/repositories"
    
    params = {
        "q": "topic:ai created:>=" + datetime.now().strftime("%Y-%m-%d"),
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            repos = data.get("items", [])
            
            results = []
            for i, repo in enumerate(repos[:10], 1):
                desc = repo.get("description") or "No description"
                results.append({
                    "rank": i,
                    "name": repo.get("full_name"),
                    "desc": desc[:80] if len(desc) > 80 else desc,
                    "stars": repo.get("stargazers_count", 0),
                    "lang": repo.get("language") or "Unknown",
                    "url": repo.get("html_url")
                })
            return results
        return []
    except:
        return []

if __name__ == "__main__":
    projects = get_github_ai_trending()
    
    if projects:
        for p in projects:
            print(f"{p['rank']}|{p['name']}|{p['stars']}|{p['lang']}|{p['desc']}|{p['url']}")
    else:
        print("ERROR:Failed to fetch")
