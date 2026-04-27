---
tags: [source, rendering, ibl, cubemap, 环境光遮蔽, 光泄漏, diffuse-probe]
date: 2026-04-27
sources: 1
---

# From the Archive: Notes on Environment Lighting Occlusion（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2023 年 10 月（c0de517e.com 首篇图形文章），继续 2023 年 4 月 GGX 视差修正笔记的线索，专门讨论 specular 光泄漏与基于 diffuse probe 的 clamping 方案。

## 摘要

parallax-corrected specular probe 在着色点偏离 probe 中心时，标准 renormalization（用 diffuse probe 比值乘以 specular）只能给出全局亮度缩放，无法处理小立体角方向的能量集中——因而在阴影区域仍会出现高光泄漏，Fresnel 边缘处尤为明显。

Pesce 的方案：为每个方向构建一个"最大允许 specular"上界，然后对实际 specular probe 做 soft-min clamping。上界的推导假设 diffuse probe 的辐照度全部来自于"使当前视角 specular 响应最大的方向"（即 N·V = N·L），并进一步假设该能量来自一个有限尺寸的面光源（以"粗糙度修改"方式近似）。将上述假设串联，可得出一个以 roughness、diffuse 散射值和 N·V 为输入的解析上界公式，经多次近似化简后变成可在 shader 中执行的 HLSL 片段（但已完全失去物理意义可读性）。

关键调参：面光源"尺寸"参数决定上界松紧，作者承认最终以眼睛调参而非数值拟合确定，是一个显式 hack。

## 关键要点

- 标准 renormalization 不足以处理方向性强的高频能量，只能整体缩放
- 基于 diffuse probe 推导 specular 上界是一种退而求其次的保守估计，方向假设简化是核心近似
- "面光源作为代理"的技巧同样出现在 area light 近似中（cosine-lobe 等效粗糙度变换）
- 结论：parallax-corrected GGX 管线是一系列近似的叠加，连接处全是无法公开发表细节的 hack；作者鼓励从真值路径追踪器出发去校准

## 链接到的概念

- [[parallax-corrected-cubemap]]
- [[ibl-multiple-scattering]]
- [[envmap-ibl-approximation-errors]]
- [[split-sum-approximation]]
- [[ground-truth-ambient-occlusion]]

## 原文

- 链接：https://c0de517e.com/006_cubemap_occlusion.htm
- 本地（blogspot 存根）：`raw/articles/c0de517e.blogspot.com/2023-10-03_from-the-archive-notes-on-environment-lighting-occlusion.md`
- 本地（c0de517e.com 全文）：`raw/articles/c0de517e.com/2023-10-03_from-the-archive-notes-on-environment-lighting-occlusion.md`
