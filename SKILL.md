# xiaohongshu-publisher

小红书自动发布技能

## 触发

当用户说"发布小红书"、"发笔记"时使用此技能。

## 执行

直接执行：

```
python "E:\project\xhs_publish.py" "标题" "内容" "标签"
```

示例：
```
python "E:\project\xhs_publish.py" "AI新时代" "AI正在改变世界" "#AI#科技"
```

## 自动发布AI资讯

```
python "E:\project\publish_ai_news.py"
```

会自动获取GitHub热门AI项目并发布。

## 注意事项

- 图片使用默认路径
- 发布间隔建议5分钟以上
- 每天建议不超过5篇
