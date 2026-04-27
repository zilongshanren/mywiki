---
tags: [source, software-design, 架构, 模块化, 坏代码, 隔离]
date: 2026-04-27
sources: 1
---

# The Art and Joy of Well-Architected "Bad Code"（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2024 年 1 月（c0de517e.com）的文章，借个人静态网站的维护经历，论述"坏代码"与"好架构"并不矛盾——正确的模块隔离才是保证坏代码可以存活的前提条件。

## 摘要

Pesce 用自己的网站生成器举例：代码惨不忍睹（`exec(f.read())` 代替 `import`），但他完全不担心，因为内容数据格式极其简单，即便扔掉全部代码从头写也只需两天。这一直觉被他提炼为对"好架构"的定义：**关键组件在正确粒度上隔离，组件间 API 表面小且简单，"坏"就无法扩散**。

他认为好架构之所以稀缺，有两个互相强化的原因。第一，DRY 文化和 OOP 语言激励共享与复用，却没有任何机制强制反向的隔离——函数引用随手就能跨整个代码库，而不像 library 边界那样有物理阻隔。第二，好架构最重要的时刻恰好是它最难被追加的时刻：项目成功后代码库规模和团队规模都已超出控制，生产优先级又挤压重构空间。结论：适量技术债是正常的，关键是把债务限制在"皮肤病"而非"皮肤癌"的范围内。

## 关键要点

- 坏代码是否危险取决于它能否被隔离，而非代码本身有多糟糕
- "end-user programming"的生产力来自彻底的局部性：失去隔离就失去了这种生产力
- OOP 与 DRY 是依赖纠缠的主要推手；C/C++ 的 library 边界是语言外的隔离工具
- mock、TDD 的必要性本身就是缺乏真实隔离的征兆（为人造隔离写代码）
- 成功项目的好架构总是滞后于规模增长：这是宿命，不是失败

## 链接到的概念

- [[modular-design]]
- [[information-hiding]]
- [[clean-code-critique]]
- [[deep-modules]]
- [[tactical-programming]]

## 原文

- 链接：https://c0de517e.com/009_website_joy.htm
- 本地（blogspot 存根）：`raw/articles/c0de517e.blogspot.com/2024-01-17_the-art-and-joy-of-well-architected-bad-code.md`
- 本地（c0de517e.com 全文）：`raw/articles/c0de517e.com/2024-01-15_the-art-and-joy-of-well-architected-bad-code-and-a-website-u.md`
