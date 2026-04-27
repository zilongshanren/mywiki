---
tags: [source, 渲染, 材质混合, screen-space, ssao, 基于屏幕空间]
date: 2026-04-27
sources: 1
---

# Fun with MeshBlend! Let's Learn from an Amazing Unreal Plugin（Angelo Pesce）

[[people/angelo-pesce]] 发表于 2025 年 7 月的文章，通过推理 Tore Lervik 的 MeshBlend 插件工作原理，讲述了如何从"存在性证明"出发独立推导技术方案。

## 摘要

MeshBlend 是一款 Unreal 插件，能让两个相交网格在接触处材质平滑过渡，视觉上消除独立建模拼接的边界。Pesce 在未接触插件实现的情况下独立推导其可能原理：关键约束是效果与摄像机无关、双向渐变、小混合半径、视觉稳定、需要 Deferred Rendering。他先排除了基于距离场和几何衬裙的方案，然后意识到——用 SSAO 风格的屏幕空间采样来判断何时采样邻近网格的材质属性，当采样命中率高（即表面接近）时就混合材质，这正是可行方案。Crysis 发布 SSAO 时他曾独立推导出一个基于深度缓冲 raymarching 的 AO 变体；同样的"已存在"知识解锁了此次推理。文章也坦承：真正困难的是实现细节（时序积累、分辨率分离、Z 不连续拒绝等），最终实现可能与 Tore 的完全不同。

## 关键要点

- MeshBlend 利用 Deferred Rendering 的 G-buffer：无需生成新几何，在延迟光照阶段混合材质参数
- 类 SSAO 的屏幕空间深度采样确定两表面接近程度，用命中率驱动混合权重
- 混合半径小是关键优势：短半径下视差伪影最小，接近早期 SSAO 的"角落晕圈"效果
- 时序积累（temporal amortization）可能用于稳定混合权重，而材质属性本身需全分辨率
- "存在性证明"对创意推导的价值：知道"它能做到"往往是打破自我设限的唯一前提

## 链接到的概念

- [[rendering/meshblend-ssao-material-blend]]
- [[rendering/hbao-interleaved-sampling]]
- [[rendering/deferred-rendering]]
- [[rendering/ground-truth-ambient-occlusion]]

## 原文

- 链接：https://c0de517e.com/024_meshblend.htm
- 本地：`raw/articles/c0de517e.com/2025-07-29_fun-with-meshblend-let-s-learn-from-an-amazing-unreal-plugin.md`
