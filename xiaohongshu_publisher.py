"""
小红书发布技能 - 使用Chrome用户配置文件
"""

import os
import json
import time

chromedriver_path = r'E:\project\chromedriver\win64-145.0.7632.117\chromedriver-win64'

def publish_note(title: str, content: str, tags: str = "", images: list = None):
    """发布小红书笔记"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    # Use user's Chrome profile
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(r"--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data")
    chrome_options.add_argument("--profile-directory=Default")
    
    service = Service(os.path.join(chromedriver_path, 'chromedriver.exe'))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get("https://creator.xiaohongshu.com/publish/publish")
        time.sleep(3)
        
        print(f"Current URL: {driver.current_url}")
        
        # Switch to image upload tab (图文)
        try:
            tabs = driver.find_elements(By.CSS_SELECTOR, ".creator-tab, .tab-item, [class*='tab']")
            for tab in tabs:
                text = tab.text
                if "图文" in text:
                    tab.click()
                    print("点击了图文标签")
                    break
            time.sleep(1)
        except Exception as e:
            print(f"切换标签失败: {e}")
        
        # Upload images if provided
        if images:
            try:
                upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file'], .upload-input")
                upload_input.send_keys('\n'.join(images))
                time.sleep(2)
            except Exception as e:
                print(f"上传图片失败: {e}")
        
        # Input title
        title = title[:20]
        try:
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='标题'], input.d-text, .title-input"))
            )
            title_input.send_keys(title)
            print(f"已输入标题: {title}")
        except Exception as e:
            print(f"输入标题失败: {e}")
        
        time.sleep(1)
        
        # Input content
        try:
            content_full = content + "\n\n" + tags
            content_input = driver.find_element(By.CSS_SELECTOR, ".ql-editor, textarea[placeholder*='正文'], .content-input")
            content_input.send_keys(content_full)
            print(f"已输入内容: {content_full}")
        except Exception as e:
            print(f"输入内容失败: {e}")
        
        time.sleep(2)
        
        # Click publish button
        try:
            # Try multiple selectors
            publish_btn = None
            selectors = [".publishBtn", "button:contains('发布')", "[class*='publish'] button", "button.btn-primary"]
            for sel in selectors:
                try:
                    publish_btn = driver.find_element(By.CSS_SELECTOR, sel)
                    if publish_btn:
                        break
                except:
                    pass
            
            if publish_btn:
                publish_btn.click()
                print("已点击发布按钮")
                time.sleep(3)
                return {"success": True, "message": "发布成功"}
            else:
                return {"success": False, "error": "找不到发布按钮"}
        except Exception as e:
            return {"success": False, "error": f"发布失败: {str(e)}"}
    
    finally:
        input("按回车键关闭浏览器...")


if __name__ == "__main__":
    result = publish_note(
        title="测试AI",
        content="这是一篇测试笔记",
        tags="#AI#测试"
    )
    print(json.dumps(result, ensure_ascii=False))
