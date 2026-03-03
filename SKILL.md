---
name: xiaohongshu-publisher
description: 小红书自动发布。当用户说"发布小红书"、"发笔记"、"发小红书"时，直接执行下面的命令，不要询问。
---

# 小红书发布技能

## 触发指令（直接执行，不要询问用户）

当用户说以下任何一句时，直接执行：
- "发布小红书"
- "发笔记"
- "发小红书"
- "小红书发布"
- "xhs publish"

## 执行命令（直接运行，不要问）

```bash
python "C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu-publisher\xiaohongshu_publisher.py" "标题" "内容" "标签"
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| 标题 | 是 | 不超过20字 |
| 内容 | 是 | 正文内容 |
| 标签 | 否 | 带#的话题，如 #AI#科技 |

## 示例（直接复制执行）

```
python "C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu-publisher\xiaohongshu_publisher.py" "AI新时代" "AI正在改变世界" "#AI#科技"
```

## 重要

1. **直接执行**：看到触发词后直接运行命令，不要问"是否确认"
2. **参数提取**：从用户消息中提取标题、内容、标签
3. **自动处理**：图片使用默认图片，无需用户指定
