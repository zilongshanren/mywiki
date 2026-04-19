---
tags: [source, rendering, engine-architecture, 反思, blog]
date: 2026-04-19
sources: 1
---

# The pitfalls of experience（Angelo Pesce / C0DE517E）

[[angelo-pesce|Angelo Pesce]] 2010 年 2 月在博客 C0DE517E 发表的随笔，表面上是一篇关于"经验为什么既是优势也是陷阱"的工程文化反思，底下却藏了两块很硬的技术内容——Crysis 深度缓冲 SSAO 的反向推导故事，以及他对 **3D 引擎是否需要场景图** 的完整态度。

## 摘要

Pesce 的核心论点分两半。**前半**：AAA 行业的生存条件（两三年周期、硬 deadline、恶心的遗留代码、残酷竞争）让"经验"成为最被推崇的美德，因为它是一种高效的**噪声过滤器**——能快速砍掉烂点子、估算可行性、选择安全路径。但代价是：**那些"看起来不可能"的革命性点子也同时被过滤掉了**。他借 Alice in Wonderland "before breakfast believe six impossible things" 的对白做隐喻：天才之所以是天才，就是因为他们愿意去相信那些经验告诉你"不可能"的事。

**后半**是 Crysis 故事：同事用 3DRipper 抓了一帧 Crysis，发现一张动态生成的类 AO 贴图。Pesce 当时完全想不到怎么做，但**一旦知道它可能**，他几天内就靠"在深度缓冲上做简化 raymarching"复现出来——这就是今天 SSAO/HBAO/GTAO 整条技术脉络的祖师爷雏形。结论：*"All it took was to know it was possible."*

文章解药也很朴素：保持好奇心大于专业、多给外行讲自己的工作（新点子往往在 presentation 写稿时出现）、珍惜 preproduction 阶段；而**迭代速度**是决定创造力能否贯穿整个项目的关键变量。

## 关键要点

- **经验是噪声过滤器**——筛掉 99 个平庸点子的同时也筛掉那 1 个革命性的点子。
- Crysis 的 SSAO 反推是"unknown unknowns 变成 known knowns"的经典案例：技术不难，难的是打破先验。
- **好奇心 vs 经验** 的平衡是工程文化的核心问题之一；知识是可被重组的噪声，经验会把它压成"只能这么做"。
- 讲给别人听（甚至讲给自己听）是最便宜的创造力激发手段——洞见通常出现在写 slides 的过程里。
- 评论区讨论延伸出两个额外话题：**Preproduction 才是真正能创新的窗口**（但工具链够好时可以延长这个窗口）、**3D 引擎不应以场景图为核心**（Pesce 详细回应读者 Rob 的提问，给出按 renderable 类型特化的替代设计）。

## 链接到的概念

- [[experience-as-noise-filter]] —— 正文主论点
- [[scene-graph-unnecessary-in-engine]] —— 从评论区提炼的设计观点
- [[hbao-interleaved-sampling]] / [[ground-truth-ambient-occlusion]] —— 故事里深度缓冲 SSAO 的后代
- [[z-buffer]]
- [[unknown-unknowns]]
- [[taste-development]]
- [[strategic-programming]] / [[tactical-programming]]

## 原文

- 链接：<https://c0de517e.blogspot.com/2010/02/pitfalls-of-experience.html>
- 本地：`raw/articles/c0de517e.blogspot.com/2010-02-05_the-pitfalls-of-experience-2.md`
