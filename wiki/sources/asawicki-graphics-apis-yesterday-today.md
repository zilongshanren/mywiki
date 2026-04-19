---
tags: [source, 渲染, 图形API, 历史]
date: 2026-04-19
sources: 1
---

# Graphics APIs – Yesterday, Today, and Tomorrow（Adam Sawicki）

[[adam-sawicki]] 2026 年 1 月放出的文章公告，内容是一篇面向"玩过老游戏的普通人"的图形 API 科普长文，原为波兰《Programista》杂志 2025 年 4 期刊载，现以英语 + 波兰语同时免费开放。

## 摘要

文章走一遍 DirectX、OpenGL、Vulkan 的演进历史，同时并行穿插 GPU 硬件与商业游戏的发展线。定位不是教程（不会教怎么写代码），而是科普——解释从固定管线到可编程管线再到"现代低层"API 这 20 多年的结构性变化，以及为什么今天的 D3D12 学习曲线远比 DX9 陡。

## 关键要点

- 固定管线 → 可编程管线 → 现代低层 API 的三段式演进
- 每一代 API 都对应一批"什么问题从驱动甩给应用"——shader 编译、状态管理、内存、barrier、命令录制
- 文章同时出中英/波兰双语，作者保留商业刊物过期后的公开权
- 面向普通读者而非程序员，可作为向非技术同事解释"为什么 AAA 游戏引擎越来越复杂"的入门材料

## 链接到的概念

- [[graphics-api-history]]
- [[adam-sawicki]]

## 原文

- 链接：<https://asawicki.info/news_1798_graphics_apis_yesterday_today_and_tomorrow_-_a_new_article>
- 本地：`raw/articles/asawicki.info/2026-01-20_graphics-apis-yesterday-today-and-tomorrow-a-new-article.md`
