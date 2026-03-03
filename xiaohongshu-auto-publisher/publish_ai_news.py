# -*- coding: utf-8 -*-
"""
GitHub AI资讯自动发布
"""
import requests
import asyncio
import json
import random
import os
from datetime import datetime
from playwright.async_api import async_playwright

cookie_file = r"C:\Users\Administrator\.openclaw\agents\mofa\cookies\xiaohongshu.json"
IMAGE_DIR = r"C:\Users\Administrator\Pictures"

content_prefixes = ["Today Hot", "New Release", "Trending", "Recommended", "Tech"]

def get_github_ai_trending():
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "topic:ai created:>=" + datetime.now().strftime("%Y-%m-%d"),
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            repos = r.json().get("items", [])[:10]
            return [{"rank": i+1, "name": x.get("full_name"), "stars": x.get("stargazers_count", 0), "lang": x.get("language") or "?", "desc": (x.get("description") or "?")[:60]} for i, x in enumerate(repos)]
    except: pass
    return []

def gen_content(projects):
    titles = ["GitHub AI Trending Today", "Latest AI Projects", "Top AI Repos", "AI Projects Worth Attention"]
    lines = ["GitHub AI Projects Today:\n"]
    for p in projects[:5]:
        lines.append(f"{p['rank']}. {p['name'].split('/')[1]}")
        lines.append(f"   {p['stars']} stars | {p['lang']}")
        lines.append(f"   {p['desc']}")
        lines.append("")
    lines.append("\n#AI #GitHub #OpenSource #Tech")
    return random.choice(titles), "\n".join(lines), "#AI #GitHub #OpenSource"

async def publish():
    print("Fetching GitHub AI...")
    projects = get_github_ai_trending()
    if not projects:
        print("Fetch failed")
        return
    
    title, content, tags = gen_content(projects)
    title = title + str(random.randint(10, 99))
    prefix = random.choice(content_prefixes)
    content = f"{prefix}: {content}"
    
    # Image
    imgs = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_path = os.path.join(IMAGE_DIR, random.choice(imgs)) if imgs else ""
    
    print(f"Title: {title}")
    print(f"Image: {image_path}")
    
    # Load cookies
    with open(cookie_file) as f:
        cookies = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        ctx = await browser.new_context()
        page = await ctx.new_page()
        
        for c in cookies:
            c2 = {'name': c['name'], 'value': c['value'], 'domain': c.get('domain', '.xiaohongshu.com'), 'path': c.get('path', '/')}
            if 'expirationDate' in c:
                c2['expires'] = c['expirationDate']
            await ctx.add_cookies([c2])
        
        try:
            await page.goto("https://creator.xiaohongshu.com/publish/publish")
            await asyncio.sleep(4)
            
            if "login" in page.url:
                print("Cookie invalid")
                return
            
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            # Tab
            tabs = await page.query_selector_all(".creator-tab-item, .tab-item")
            for t in tabs:
                if "图文" in await t.text_content():
                    await t.click()
                    break
            await asyncio.sleep(1)
            
            # Image
            if image_path:
                fi = await page.query_selector("input[type='file']")
                if fi:
                    await fi.set_input_files(image_path)
                    await asyncio.sleep(3)
            
            # Title
            ti = await page.query_selector(".d-text")
            if ti:
                await ti.click()
                await asyncio.sleep(0.5)
                await ti.type(title, delay=100)
            
            await asyncio.sleep(0.5)
            
            # Content
            ci = await page.query_selector(".ql-editor")
            if ci:
                await ci.click()
                await asyncio.sleep(0.3)
                await ci.type(content, delay=50)
            
            await asyncio.sleep(2)
            
            # Publish
            await page.evaluate('''() => {
                const btns = document.querySelectorAll('button');
                for (const b of btns) { if (b.textContent.trim() === '发布') { b.click(); return; } }
            }''')
            await asyncio.sleep(3)
            
            # Confirm
            cb = await page.query_selector("button:has-text('确认发布')")
            if cb:
                await cb.click()
                await asyncio.sleep(5)
            
            print("Done!")
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(publish())
