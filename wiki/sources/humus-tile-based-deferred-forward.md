---
tags: [source, rendering, tiled-rendering, deferred-rendering, forward-rendering, shadow, dx11]
date: 2026-04-27
sources: 1
---

# Tile-based Deferred and Forward Lighting（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 发表于 2012 年 4 月的短文，分析分块光照的内存带宽收益，并指出当全部光源都投射阴影时这一优势被抵消。

## 摘要

Engel 在 DirectCompute 可用之后对分块延迟和分块前向光照的权衡进行了务实分析。纯光照成本来看，Tiled 方案最优情况下只读写 G-Buffer 各一次，相比 DX9/10 延迟光照（每光源一次读写）是量级级改善；但一旦加入阴影，分块方案必须在光照前把所有阴影数据准备好，导致含阴影的 pass 要对每个投影光源各读写一次 G-Buffer——收益因此归零，老式延迟反而因为光照与阴影合并 pass、共享算术指令而更优。Engel 认为 Tiled Forward 的真正价值不在于光源数扩展，而在于**为半透明物体提供了一条与不透明物体统一的多光源光照路径**，替代过去那套简化的独立透明光照系统。

## 关键要点

- 无阴影时 Tiled 读写 G-Buffer 各一次，内存带宽远低于 per-light pass 的延迟渲染
- 有阴影时每个投影光源仍需独立读写 G-Buffer，Tiled 带宽优势被抵消
- 老式延迟渲染（DX9/10 风格）在全阴影场景下是更一致的跨平台回退路径
- **Tiled Forward 的核心价值**：给半透明物体提供与不透明物体对等的多光源光照
- DX11 / DirectCompute 的并行能力使 Tiled 实现更自然，但 OpenGL 3.3 同样可实现（评论者 Ola Olsson 亲测）

## 链接到的概念

- [[rendering/tiled-light-culling]]
- [[rendering/forward-plus-rendering]]
- [[rendering/deferred-rendering]]
- [[rendering/tiled-light-prepass]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2012/04/tile-based-deferred-and-forward.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2012-04-15_tile-based-deferred-and-forward-lighting.md`
