# xiaohongshu-publisher

小红书自动发布技能

## 触发

当用户说"发布小红书"、"发笔记"时使用此技能。

## 执行

直接执行发布命令：
```
python "C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu-publisher\xiaohongshu_publisher.py" "标题" "内容" "标签" "图片路径"
```

## 本地图片管理

建议在 C:\Users\Administrator\Pictures\ 下准备多张图片：
- tech.png (科技类)
- ai.png (AI类) 
- life.png (生活类)
- nature.png (自然类)
- default.png (默认)

## 示例

```
python "C:\Users\Administrator\.openclaw\workspace\skills\xiaohongshu-publisher\xiaohongshu_publisher.py" "AI新时代" "AI正在改变世界" "#AI#科技"
```

## 注意事项

- 使用Chrome用户配置文件，无需调试模式
- 发布间隔建议5分钟以上
- 每天建议不超过3篇
