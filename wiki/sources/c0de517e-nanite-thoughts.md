---
tags: [source, rendering, nanite, software-rasterization, visibility-buffer, geometry]
date: 2026-04-27
sources: 1
---

# Some Thoughts on Unreal 5's Nanite（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2020 年 5 月的文章，以推测性分析探讨 UE5 Nanite 的可能实现机制。

## 摘要

文章并非正式逆向工程，而是从第一原理出发推理 Nanite 的构造：作者先指出硬件光栅器针对像素级三角形极度低效（四边形浪费达 75%），因此 Nanite 必然绕开固定功能光栅器，转向纯 compute 的软件光栅方案。核心链路是：compute 侧剔除（cluster culling） → 软件光栅（compute shader 逐三角形写像素） → [[rendering/visibility-buffer]]（写 draw/triangle ID + barycentrics）→ 延迟着色。文章还讨论了 LOD、流式压缩和梯度计算等挑战，并提到 REYES/几何图像作为历史参照。整体预判与 Brian Karis 后来公开的真实实现高度吻合，是社区最早的系统性思辨文章之一。

## 关键要点

- 硬件光栅器在像素级三角形上因 2×2 quad 规则损失 75% 效率，必须被绕开
- 软件光栅 + compute 侧剔除是替代路径；Karis 自己的表述印证了这一点
- [[rendering/visibility-buffer]] 是软件光栅与延迟着色之间的衔接层
- LOD 切换不依赖拓扑变化，配合时序抗锯齿可隐藏误差
- REYES 思路（规则网格、世界空间着色）是重要参照，但 Nanite 并未采用其着色策略
- 压缩与流式传输是系统中最难评估的部分，作者承认无从推断

## 链接到的概念

- [[rendering/visibility-buffer]]
- [[rendering/nanite-reyes-comparison]]
- [[rendering/nanite-tessellation-approach]]
- [[rendering/software-rasterization-compute]]
- [[rendering/culling]]
- [[rendering/temporal-antialiasing]]

## 原文

- 链接：https://c0de517e.blogspot.com/2020/05/some-thoughts-on-unreal-5s-nanite-in.html
- 本地：`raw/articles/c0de517e.blogspot.com/2020-05-15_some-thoughts-on-unreal-5-s-nanite-in-way-too-many-words.md`
