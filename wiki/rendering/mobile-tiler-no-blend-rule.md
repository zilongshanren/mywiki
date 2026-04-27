---
tags: [mobile, gpu, tbdr, blending, 性能, x-plane, iphone]
date: 2026-04-27
sources: 1
---

# 移动 GPU 的"禁止混合"性能规则

当代 Apple Silicon 移动 GPU 的性能建议可以压缩成一句话：**不要混合（don't blend）**。

## 背景：瓦片化 GPU 的隐藏优化

移动 GPU 普遍采用 [[hsr-tbdr|TBDR（Tile-Based Deferred Rendering）]] 架构，其核心优势之一是 HSR（Hidden Surface Removal）：GPU 在执行 fragment shader 之前，先在片上对整个 tile 做可见性排序，将被遮挡的像素彻底剔除掉，不做着色计算。这让填充率压力大幅降低。

然而，**一旦开启 alpha 混合，HSR 就失效了**。混合需要读回当前 framebuffer 的内容，GPU 无法预先知道哪些像素最终会暴露出来，因此不得不对所有重叠的片元都调用 fragment shader，变成和桌面 GPU 类似的前向多次着色。

## 2019 年的实测数据

[[ben-supnik|Supnik]] 在 2019 年整理 X-Plane Mobile 的性能瓶颈时观察到：

- **过去**：瓶颈分散于顶点数量、CPU 端非图形代码、填充率与着色成本三者之间
- **2019 年**：瓶颈几乎只剩着色成本

根本原因是 Apple 移动芯片的单核 CPU 性能已经大幅追平桌面。iPhone X 的 Geekbench 4 单核得分为 4245，而 2019 年带 i5-8500 的 iMac 仅为 5187——差距不到 20%。这意味着以往只在移动端暴露的 CPU 端瓶颈（内存访问模式不理想、数据依赖较深的代码）在新设备上已经"够快了"，无需专门手调。

着色成本成为剩下的唯一战场——而这个战场，实时图形领域本来就有大量成熟方案。

## 桌面 GPU 的对称问题

与移动端相反，桌面 GPU 的主要性能问题往往是**利用率（utilization）**：

- 桌面 GPU 的物理 ALU 和带宽完全可以应付多次 overdraw
- 但一帧由许多细碎的 draw call 拼成，GPU 在相邻 batch 之间需要等待，无法将整张卡始终喂饱
- 即使开着混合，只要 GPU 使用率本来就上不去，混合的额外开销也不是主要矛盾

Supnik 还记录了一次失败的优化尝试：把多个 shader 合并成带 GPU 端条件分支的"超级 shader"，期待减少 batch 切换。结果并未改善利用率（只要 batch 不能合并到完全相同就无法真正减少切换），反而增加了 ALU 成本。

## 实践原则

- **移动端**：优先消除混合，将不透明物体严格分离到不开混合的 pass；只有必须半透明的内容才接受混合代价
- **桌面端**：关注 GPU 利用率，合并 draw call、使用 indirect draw、减少 state 切换

## 相关

- [[hsr-tbdr]] — TBDR 的 HSR 机制详解
- [[iphone-4-opengl-es-perf-gap]] — 早期 iPhone 的性能断崖背景
- [[physically-based-shading]] — PBR 在移动端可以全量运行的前提正是 no-blend 规则
- [[overdraw]] — 过度绘制问题综述
- [[batching]] — 批次合并策略

## Sources

- [[sources/supnik-iphone-pc-hardware-performance]]
