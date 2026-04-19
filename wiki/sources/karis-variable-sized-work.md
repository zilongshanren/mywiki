---
tags: [source, GPU, 并行, wave-intrinsics, nanite]
date: 2026-04-19
sources: 1
---

# Variable sized work（Brian Karis / Graphic Rants）

[[brian-karis|Karis]] 2026-03-15 的第五篇，从 Nanite Tessellation 的 split/dice 实现里抽出一个**通用并行编程原语**：变长工作的 wave 内打包分发。

## 摘要

核心观察：GPU 编程里反复出现"生产者以常量成本排入变长工作、消费者完美打包到 wave"的需求，却没有被现有原语覆盖。类比 HW 光栅器（三角形 → 像素），但光栅器有 tile 亲和性和 overlap 串行化等像素专用约束，"rasterizer inception"（SW 里抽 HW 光栅器当 dispatcher）跑不过纯 SW 方案。更关键的是**数据移动成本**——Karis 顺便解释为什么 Nanite 软光栅比硬光栅快：不是因为 pixel quad、不是因为 transistor 规模，而是 HW 光栅器做 triangle setup → bin → tile list → 多级 mask → prefix sum 打包的整条链路，在 pixel 量足够大时摊销得开，对 micropoly 来说开销超过收益。

同理搬到 tessellation split/dice：把工作项写到 memory queue 再读回来带宽浪费，应当**就在 wave 内**分发。算法：每 lane 声明 `NumWorkItems`，`WavePrefixSum` 算出起始偏移；循环 pull，每条消费 lane 用 `WaveActiveBallot + firstbithigh` 做 bit-scan 找到源 lane，再 `WaveReadLaneAt` 直接读源 lane 的 register 状态（不经 groupshared 搬数据、不经 memory queue）。生产 lane 的 patch 状态（Tessellation Pattern 索引等）直接被消费 lane 读。Rune 优化：`NumWorkItems == 0` 路径不做 compaction。**代价**：只能 wave 内分发，总工作量要有上界（TessFactor 上限天然给出），否则"一个 wave 拖死整块机器"。Nanite Tessellation 用它三次：ClusterRasterize 就地 dice、ClusterRasterize 就地一步 split、PatchSplit 里 split 工作分发。

## 关键要点

- **核心需求**：`生产者常量成本产出变长工作 → 消费者完美打包到 wave`。
- **Nanite SW 光栅器 vs HW**：差别不在 pixel quad，在**数据移动**——HW 的 binning chain 对 micropoly 是净开销。
- **wave 内 pull-based 分发**：`WavePrefixSum` + `WaveActiveBallot` + `firstbithigh` + `WaveReadLaneAt`；数据留在生产 lane register 里。
- **边界**：只覆盖 wave 内；跨 threadgroup / 跨 dispatch 要 multipass 或 [[d3d12-work-graphs|work graphs]]。
- **三处应用**：ClusterRasterize 内就地 dicing / 就地一步 split / PatchSplit 的子 subpatch 分发。

## 链接到的概念

- [[variable-sized-work-pattern]]
- [[nanite-tessellation-approach]]
- [[d3d12-work-graphs]] —— 跨 wave 尺度的同类问题
- [[meshlets-and-mesh-shaders]] —— AS 剔除用同类 wave intrinsics 思路

## 原文

- 链接：<http://graphicrants.blogspot.com/2026/03/variable-sized-work.html>
- 本地：`raw/articles/graphicrants.blogspot.com/2026-03-15_variable-sized-work.md`
