---
tags: [source, 游戏引擎, game-engine-architecture]
date: 2026-04-05
sources: 1
---

# Game Engine Architecture Day 2 —— 引擎演化史

Game Engine Architecture 学习推送第 2 天。

## 摘要

从 BSP Tree → Portal+PVS → 可编程 Shader → Deferred Rendering → Dynamic GI（Lumen/Nanite）的引擎技术演化史。**技术决定游戏设计**（BSP 限制导致第一代 FPS 必须室内）。**游戏引擎作为商品诞生于 Quake（1996）**——id 的授权决策塑造了整个行业。

## 关键要点

- **Quake（1996）** 的引擎授权开创了独立引擎市场。
- **BSP Tree**：第一代可见性解，O(log n)，自动后到前排序。
- **Portal + PVS**：预计算房间可见性，运行时 O(1) 查找。
- **技术决定设计**：BSP 限制导致 FPS 室内化，不是设计师选择。
- **Material Editor (UE3, 2004)** 民主化 shader 创建——Unity 到 2018 才有 Shader Graph（12 年差距）。
- **延迟渲染**：G-Buffer + 统一光照 pass，支持 10-100× 光源。
- **Lumen**：UE5 动态 GI = Screen Space GI（近）+ World Space SDF GI（远）。
- **Nanite**：软件光栅化 sub-pixel triangles。
- **性能预算内的最优近似是游戏引擎的本质**。
- **技术债的历史周期**：每个架构选择都是对未来的借贷。
- **Unity 移动端优势**是系统性的：URP SRP Batcher、GPU Instancing、TBDR 定向优化、ecosystem。
- **工具比运行时性能更重要**（Unreal Engine 1 的真正革命是 UnrealEd）。

## 链接到的概念

- [[game-engine]]
- [[unity-vs-unreal]]
- [[engine-evolution]]
- [[deferred-rendering]]
- [[rendering-pipeline]]

## 原文

- 链接到：[[raw/articles/game engine architecture/day02]]
