---
tags: [source, rendering, deferred-rendering, 性能优化, 游戏开发]
date: 2026-04-27
sources: 1
---

# Notes on optimizing a deferred renderer（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2012 年 10 月的文章，发布了一份内部 post-mortem 演示文稿：Relic Entertainment 的《Space Marine》在出货前六个月将渲染性能翻倍的经过。

## 摘要

文章内容很短，主要是对 Scribd 上一份演示文稿的介绍。这份 deck 原为 Relic 的内部 post-mortem，后经清洁（去掉实现细节、将截图替换为公开截图）发布到 Pesce 偶尔在温哥华组织的渲染工程师小聚上，再后来发到网上。

《Space Marine》是一款跨主机 3D TPS 游戏，由以 PC RTS 著称的 Relic 开发，Pesce 负责跨平台渲染性能监督。关键事实：出货前六个月性能翻倍，达到稳定 30 fps。主要工作包括：shadows / post effects / SSAO 从头重写、加入软件遮挡剔除、全面的 SIMD 和多线程化；Pesce 列出了超过 20 条每平台任务，出货时完成了 80% 以上。

技术亮点（文中提到，但在公开版 deck 中已部分删除）：Oren-Nayar diffuse 的实现方式、「world occlusion」、DOF/MB 滤波、头发光照技巧，以及「几乎零延迟」的帧流水线（参见 [[frame-pipeline-latency]]）。

## 关键要点

- 出货前六个月渲染性能翻倍是可能的：系统性优化（重写 + 软件遮挡 + SIMD/threading）而非单点 trick
- Pesce 的工作方式：制作横跨平台的任务列表（20+ 条/平台），驱动执行
- 延迟渲染「几乎零延迟」：参见 [[frame-pipeline-latency]] 中的讨论
- 软件遮挡剔除（software occlusion culling）在当时是不常见的优化手段
- Relic 的知识共享文化（openness to share）是发布这份 deck 的前提

## 链接到的概念

- [[deferred-rendering]]
- [[frame-pipeline-latency]]
- [[bottleneck-analysis]]

## 原文

- 链接：https://c0de517e.blogspot.com/2012/10/notes-on-optimizing-deferred-renderer.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-10-08_notes-on-optimizing-a-deferred-renderer.md`
