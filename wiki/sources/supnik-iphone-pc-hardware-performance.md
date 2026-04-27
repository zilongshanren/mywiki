---
tags: [source, hacksoflife, mobile, gpu, 性能, iphone, tbdr]
date: 2026-04-27
sources: 1
---

# Hardware Performance: Old and New iPhones and PCs（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2019 年 9 月的文章，分析 X-Plane Mobile 新版本性能瓶颈的根本性转变，以及 2019 年 Apple 移动芯片追平桌面的实测数据。

## 摘要

X-Plane Mobile 以往的性能瓶颈来自多方：顶点数量、CPU 端业务代码、填充率/着色三者并重。2019 年版本的情况完全不同——瓶颈几乎只剩着色成本。Supnik 认为根本原因是 Apple 移动芯片的单核 CPU 性能已追平桌面（iPhone X 单核 Geekbench 4 得分 4245，2019 iMac i5-8500 为 5187，差距仅 20%），过去需要手动调优才能在移动端跑顺的代码，现在"够快了"。

着色成本剩下，但这是好事：实时图形领域针对着色成本有大量成熟方案。核心建议是**不要混合（don't blend）**：移动 GPU 的 TBDR 架构在混合关闭时会自动 HSR 剔除不可见片元，一旦混合打开，HSR 失效，填充代价暴涨。桌面 GPU 则相反——真正的瓶颈是利用率（utilization），物理算力足够多次 overdraw，但细碎 draw call 让 GPU 始终无法吃饱。

Supnik 还记录了一次失败的优化：把多 shader 合并成带条件分支的"超级 shader"以减少 batch 切换，结果利用率没改善，ALU 成本反而上升。

## 关键要点

- iPhone X vs 2019 iMac i5：单核性能差距仅约 20%，移动 CPU 已基本追平桌面
- 移动端最重要的性能规则：关混合，让 TBDR 的 HSR 自动剔除遮挡片元
- PBR 全效果在移动端完全可行，前提是不做全屏多次着色
- 桌面端主要矛盾是 GPU 利用率，不是填充率
- 合并 shader 为"超级 shader"加条件分支是一次失败的优化，教训是只有完全相同的 batch 才能真正合并

## 链接到的概念

- [[mobile-tiler-no-blend-rule]]
- [[hsr-tbdr]]
- [[iphone-4-opengl-es-perf-gap]]
- [[physically-based-shading]]
- [[overdraw]]
- [[batching]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2019/09/hardware-performance-old-and-new.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2019-09-14_hardware-performance-old-and-new-iphones-and-pcs.md`
