---
tags: [source, bitsquid, documentation, markup, ruby]
date: 2026-04-19
sources: 1
---

# A Simple Roll-Your-Own Documentation System（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2011 年 9 月的博文，展示如何用不到 200 行 Ruby 实现一个可控的自定义文档系统。

## 摘要

为什么不用 Word/Pages、HTML/LaTeX、Wiki 或 Markdown/ReST/DocBook？四类选型都有硬伤：Word 不能 diff；HTML 是表现层、不能重排；Wiki 无法与代码版本共 commit；Markdown 系列要么不够灵活要么太重。Frykholm 的方案是把文档管线拆成 **parser + generator** 两段：parser 把每行打成 `(type, text)` 扁平 line list——故意不用层级 AST；generator 维护当前打开的 HTML tag 栈，用一个 `context(tags)` 辅助方法自动开关标签，流式生成输出。嵌套列表用 `@li_li` 这种特殊 type marker 处理，拒绝通用层级。总代码量在 100 行量级。

## 关键要点

- 设计约束先于语法：想 plain-text diffable、可重排、与代码 co-commit、易扩展。
- 用 line list 代替 AST 是核心简化：写 parser 和 generator 都不需要前瞻。
- `context([tags])` 的双指针 prefix 比较是 generator 的优雅点。
- Lua 代码块用状态化 marker（`@lua … @endlua`）处理。
- TOC、交叉引用这类需要全局信息的功能，用 generator 后加 pass 解决。
- 评论质量很低（几乎都是 spam）。

## 链接到的概念

- [[minimal-markup-pipeline]]
- [[strategic-programming]]
- [[header-as-user-manual]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/09/simple-roll-your-own-documentation.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-09-08_a-simple-roll-your-own-documentation-system.md`
