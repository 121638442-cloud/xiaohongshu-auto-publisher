"""
小红书自动发布 - 智能配图版
"""
import sys
import asyncio
import json
import random
import os
from playwright.async_api import async_playwright

cookie_file = r"C:\Users\Administrator\.openclaw\agents\mofa\cookies\xiaohongshu.json"

# 本地图片库
IMAGE_DIR = r"C:\Users\Administrator\Pictures"

# 关键词对应图片
KEYWORD_IMAGES = {
    "ai": ["ai.png", "tech.png", "科技.png"],
    "科技": ["tech.png", "ai.png"],
    "智能": ["ai.png", "tech.png"],
    "未来": ["future.png", "科技.png"],
    "生活": ["life.png", "生活.png"],
    "美食": ["food.png", "美食.png"],
    "旅行": ["travel.png", "旅行.png"],
    "学习": ["study.png", "学习.png"],
    "工作": ["work.png", "工作.png"],
}

DEFAULT_IMAGE = "212721871.png"

def select_image(title: str, content: str = "") -> str:
    """根据标题内容选择合适的图片"""
    text = (title + " " + content).lower()
    
    # 查找匹配的关键词
    for keyword, images in KEYWORD_IMAGES.items():
        if keyword in text:
            for img in images:
                path = os.path.join(IMAGE_DIR, img)
                if os.path.exists(path):
                    print(f"选择图片: {img} (关键词: {keyword})")
                    return path
    
    # 返回默认图片
    default_path = os.path.join(IMAGE_DIR, DEFAULT_IMAGE)
    if os.path.exists(default_path):
        return default_path
    
    # 随机选择一张
    all_images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if all_images:
        choice = random.choice(all_images)
        return os.path.join(IMAGE_DIR, choice)
    
    return ""

# 多样化内容模板
content_prefixes = [
    "今天分享", "最新消息", "研究发现", "最新动态",
    "科技前沿", "行业观察", "深度分析", "最新资讯",
    "值得关注", "一起来看", "深入了解", "全面解读"
]

content_suffixes = [
    "值得关注！", "你怎么看？", "一起讨论！",
    "未来可期", "拭目以待", "一起来看",
    "深度好文", "推荐阅读"
]

async def publish(title: str, content: str, tags: str = "", image_path: str = ""):
    try:
        with open(cookie_file, 'r') as f:
            cookies_data = json.load(f)
    except:
        print("ERROR: Cookie文件不存在")
        return False
    
    # 自动选择图片
    if not image_path:
        image_path = select_image(title, content)
        print(f"自动选择图片: {image_path}")
    
    if not image_path or not os.path.exists(image_path):
        print("ERROR: 图片不存在")
        return False
    
    # 添加随机变化
    prefix = random.choice(content_prefixes)
    suffix = random.choice(content_suffixes)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        async def handle_dialog(dialog):
            print(f"Dialog: {dialog.message}")
            await dialog.accept()
        page.on("dialog", handle_dialog)
        
        for cookie in cookies_data:
            pc = {
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': cookie.get('domain', '.xiaohongshu.com'),
                'path': cookie.get('path', '/'),
            }
            if 'expirationDate' in cookie:
                pc['expires'] = cookie['expirationDate']
            await context.add_cookies([pc])
        
        try:
            await page.goto("https://creator.xiaohongshu.com/publish/publish")
            await asyncio.sleep(4)
            
            if "login" in page.url:
                print("ERROR: Cookie无效")
                await browser.close()
                return False
            
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            # Click 上传图文
            try:
                tabs = await page.query_selector_all(".creator-tab-item, .tab-item, [class*='tab']")
                for tab in tabs:
                    text = await tab.text_content()
                    if text and "图文" in text:
                        await tab.click()
                        print("点击上传图文")
                        await asyncio.sleep(1)
                        break
            except Exception as e:
                print(f"切换标签: {e}")
            
            # Upload image
            try:
                file_input = await page.query_selector("input[type='file']")
                if file_input:
                    await file_input.set_input_files(image_path)
                    print(f"已上传图片: {os.path.basename(image_path)}")
                    await asyncio.sleep(3)
            except Exception as e:
                print(f"上传图片: {e}")
            
            # Input title - 随机变化
            title = title[:16] + str(random.randint(10, 99))
            try:
                title_input = await page.query_selector(".d-text")
                if title_input:
                    await title_input.click()
                    await asyncio.sleep(0.5)
                    await title_input.type(title, delay=100)
            except Exception as e:
                print(f"标题: {e}")
            
            await asyncio.sleep(0.5)
            
            # Input content - 添加变化
            try:
                content_full = f"{prefix}，{content}，{suffix}\n\n{tags}"
                content_input = await page.query_selector(".ql-editor")
                if content_input:
                    await content_input.click()
                    await asyncio.sleep(0.3)
                    await content_input.type(content_full, delay=50)
            except Exception as e:
                print(f"内容: {e}")
            
            await asyncio.sleep(2)
            
            # Click 发布
            await page.evaluate('''
                () => {
                    const buttons = document.querySelectorAll('button');
                    for (const btn of buttons) {
                        if (btn.textContent.trim() === '发布') {
                            btn.click();
                            return;
                        }
                    }
                }
            ''')
            print("点击发布...")
            
            await asyncio.sleep(3)
            
            # Click 确认发布
            try:
                confirm_btn = await page.query_selector("button:has-text('确认发布')")
                if confirm_btn:
                    await confirm_btn.click()
                    print("点击确认发布")
                    await asyncio.sleep(5)
            except Exception as e:
                print(f"确认: {e}")
            
            print("完成")
            await browser.close()
            return True
                
        except Exception as e:
            print(f"ERROR: {e}")
            await browser.close()
            return False


if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "Test"
    content = sys.argv[2] if len(sys.argv) > 2 else "Test"  
    tags = sys.argv[3] if len(sys.argv) > 3 else ""
    image = sys.argv[4] if len(sys.argv) > 4 else ""
    
    result = asyncio.run(publish(title, content, tags, image))
