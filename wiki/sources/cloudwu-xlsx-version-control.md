---
tags: [source, xlsx, 版本控制, 工具链, 策划协作]
date: 2026-04-19
sources: 1
---

# xlsx 与版本管理（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2025 年 9 月的一篇工程笔记，记录了他花一周时间解决"策划的 Excel 表格无法走 git 工作流"这个老问题时踩的坑。

## 摘要

起点是一个非常普遍的困境：项目里的策划把一切都记在 xlsx 表格里，刚从 svn 迁到 git 后频繁冲突，因为 Excel 文件"打开再保存就会变成一个完全不同的文件"——里面带着最后修改时间、激活单元格这类与内容无关但会导致差异的字段。作者的解法是把 xlsx 规范化成一个可 diff 的纯文本格式：xlsx 本质是 zip + 一堆 xml，写 Lua 小程序解压、按文件名排序、拼接、对二进制做 base64、给 xml 标签加换行，并剔除"最后修改时间"这类无语义字段。为了让 Excel / WPS 继续能编辑，把自定义格式关联到一个十几行的 Lua 脚本：双击时转成临时 xlsx 打开，监控文件锁释放后再反向转回。作者评价这次工作"不算成功也不算失败"——方案能跑，但 xlsx 格式细节里还藏着很多对版本控制不友好的点，需要继续打磨。

## 关键要点

- xlsx 对版本管理的敌意主要来自元数据字段（mtime、激活单元格）而非内容
- xlsx 本质是 zip + xml，规范化解压 + 排序 + base64 图片即可变成文本
- 剔除无语义字段后，"空打开再保存"不再产生差异
- 不写 Excel 插件也能让用户无缝编辑：文件关联 + 临时文件 + 文件锁检测结束
- 方案是"弯路"而非"最佳实践"，踩坑记录性质大于方法论

## 链接到的概念

- [[xlsx-text-versioning]]
- [[game-resource-pack-format]]
- [[c-serialization-metadata]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/cat4/cat33/
- 本地：`raw/articles/blog.codingnow.com/2025-09-16_yun-feng-de-blog-2.md`
