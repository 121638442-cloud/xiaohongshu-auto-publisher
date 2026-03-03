"""
小红书发布技能 - 连接到已运行的Chrome
"""

import os
import json
import time

chromedriver_path = r'E:\project\chromedriver\win64-145.0.7632.117\chromedriver-win64'

def publish_note(title: str, content: str, tags: str = ""):
    """发布小红书笔记"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    
    # Connect to existing Chrome with debugger
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    service = Service(os.path.join(chromedriver_path, 'chromedriver.exe'))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Go to publish page
        driver.get("https://creator.xiaohongshu.com/publish/publish")
        time.sleep(3)
        
        print(f"当前页面: {driver.current_url}")
        
        # Click on 图文 (image/text) tab
        try:
            tabs = driver.find_elements(By.CSS_SELECTOR, ".creator-tab-item, .tab-item")
            for tab in tabs:
                if "图文" in tab.text:
                    tab.click()
                    print("点击图文")
                    break
            time.sleep(2)
        except Exception as e:
            print(f"切换标签: {e}")
        
        # Input title
        title = title[:20]
        try:
            title_input = driver.find_element(By.CSS_SELECTOR, ".d-text, input[placeholder*='标题']")
            title_input.send_keys(title)
            print(f"标题: {title}")
        except Exception as e:
            print(f"输入标题: {e}")
        
        time.sleep(1)
        
        # Input content
        try:
            content_full = content + "\n\n" + tags
            content_input = driver.find_element(By.CSS_SELECTOR, ".ql-editor")
            content_input.send_keys(content_full)
            print(f"内容: {content_full[:50]}...")
        except Exception as e:
            print(f"输入内容: {e}")
        
        time.sleep(2)
        
        # Click publish
        try:
            publish_btn = driver.find_element(By.CSS_SELECTOR, ".publishBtn, button.primary")
            publish_btn.click()
            print("已点击发布")
            time.sleep(3)
            return {"success": True, "message": "发布成功！"}
        except Exception as e:
            print(f"发布按钮: {e}")
            return {"success": False, "error": str(e)}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    result = publish_note(
        title="测试AI",
        content="这是一篇测试笔记",
        tags="#AI#测试"
    )
    print(json.dumps(result, ensure_ascii=False))
    input("\n完成，按回车退出...")
