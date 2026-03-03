# 小红书自动发布工具

自动化发布小红书笔记的工具，支持AI资讯自动采集发布。

## 功能

1. **手动发布笔记** - 指定标题、内容、标签发布
2. **自动发布AI资讯** - 自动获取GitHub热门AI项目并发布

## 环境要求

- Python 3.11+
- Chrome浏览器
- Playwright: `pip install playwright`

## 安装步骤

### 1. 安装依赖

```bash
pip install playwright requests
playwright install chromium
```

### 2. 配置Cookie

1. 用Chrome登录小红书创作者中心：https://creator.xiaohongshu.com
2. 按F12打开开发者工具
3. 切换到Application标签
4. 展开Cookies → https://creator.xiaohongshu.com
5. 右键Copy all as JSON
6. 保存到：`C:\Users\Administrator\.openclaw\agents\mofa\cookies\xiaohongshu.json`

### 3. 准备图片

在 `C:\Users\Administrator\Pictures\` 文件夹放一些图片，脚本会自动选择。

## 使用方法

### 方法1：手动发布

```bash
python xhs_publish.py "标题" "内容" "#标签"
```

示例：
```bash
python xhs_publish.py "AI新时代" "AI正在改变世界" "#AI#科技"
```

### 方法2：自动发布AI资讯

```bash
python publish_ai_news.py
```

会自动：
1. 获取GitHub今日AI热门项目
2. 生成小红书格式内容
3. 自动选图并发布

## OpenClaw集成

将技能文件复制到OpenClaw技能目录：

```
C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu-publisher\
E:\project\openclaw\openclaw-main\skills\xiaohongshu-publisher\
```

重启OpenClaw后可以说：
```
发布小红书，标题：xxx，内容：xxx，标签：#xxx
```

## 防封号建议

1. **内容多样化** - 每次发布内容要有变化
2. **图片更换** - 准备多张图片轮换使用
3. **控制频率** - 每天建议不超过5篇
4. **间隔时间** - 每篇间隔5分钟以上

## 文件说明

| 文件 | 说明 |
|------|------|
| xhs_publish.py | 手动发布脚本 |
| publish_ai_news.py | 自动发布AI资讯脚本 |
| github_trending.py | GitHub热门项目获取 |

## 常见问题

**Q: 提示Cookie无效**
A: 重新登录获取新Cookie

**Q: 发布失败**
A: 检查网络，确保Chrome能正常访问小红书

**Q: 被检测怎么办**
A: 暂停发布，等待账号恢复，内容要更加多样化
