---
tags: [source, 渲染, DirectX9, MSAA, 深度缓冲, 方差]
date: 2026-04-27
sources: 1
---

# DirectX9 vs Depth Resolve（C0DE517E）

[[angelo-pesce]] 发表于 2012 年 3 月的文章，展示如何借助方差阴影贴图（VSM）的思想解决 DX9 MSAA 深度缓冲 resolve 精度丢失问题。

## 摘要

在 DirectX 9 下，MSAA 深度缓冲不可直接读取，只能写入 R32F 渲染目标；resolve 时多个 MSAA 采样被平均，导致深度边界处出现中间值，用于 SSAO、软粒子等深度相关效果时产生明显的错误边缘。Pesce 从 Donnelly 和 Lauritzen 的 VSM 论文获得灵感：除了均值，还可以存储方差（用 16bit ARGB 的第二个通道），然后用方差对深度做偏移，近似还原 min/max 信息，将平均值行为纠正为"前景优先"或两端均值，效果显著优于直接使用平均深度。

## 关键要点

- **DX9 深度限制**：MSAA 深度不可采样，R32F 深度目标 resolve = 平均，在物体边界产生幽灵深度值。
- **VSM 元技术迁移**：VSM 的核心思想是用均值+方差来统计描述一批样本，可以迁移到任何"有一堆样本但只能访问其均值"的场景。
- **实现**：把深度写入 16bit ARGB（mean, variance 分两通道），在深度相关效果中用 `mean ± f(variance)` 偏移后再做比较，可模拟前景深度或双端平均。
- **局限与结论**：这是 GDC 之前几小时内写的原型，演示"元技术"比具体实现更重要——Variance Shadow Map 论文的真正价值不在于 VSM 本身，而在于它教会了统计方法在图形中的通用运用。
- **历史背景**：Aras Pranckevičius 的 D3D9 GPU Hacks 页面记录了另一种方案（INTZ 格式可以直接采样深度 buffer），但 MSAA 深度在 DX9 仍是痛点。

## 链接到的概念

- [[moment-shadow-mapping]]
- [[msaa-ssaa]]
- [[z-buffer]]
- [[depth-aware-gaussian-blur]]

## 原文

- 链接：https://c0de517e.blogspot.com/2012/03/directx9-vs-depth-resolve.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-03-17_directx9-vs-depth-resolve.md`
