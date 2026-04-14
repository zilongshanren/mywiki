---
tags: [渲染, 可见性, 剔除, gpu-driven, compute-shader, stream-compaction]
date: 2026-04-14
sources: 1
---

# GPU 侧的实例级遮挡剔除实验

[[kostas-anagnostou|Kostas Anagnostou]] 2017 年在 DX11 上做的一个完整实验：**在不改动内容管线的前提下「外挂」一个 GPU 侧的遮挡剔除 + GPU-driven 实例绘制 pipeline**。文章的价值不在引入新技术——它的三大组件（[[hierarchical-z-buffer|HZB]] 查询、`DrawIndexedInstancedIndirect`、parallel prefix scan [[stream-compaction|流压缩]]）都是已知的——而在于把它们拼起来、落到「既有工程 retrofit」场景下，并列出每一个 **DX11 特有的约束**以及绕开的 trick。

## 背景：为什么 CPU roundtrip 是 OQ 的原罪

常规 [[occlusion-culling|遮挡剔除]] 方案里，不管是硬件 query 还是软件光栅，最后都要把 visibility 结果读回 CPU，再由 CPU 挑选性送 draw——一个同步点。[[hardware-occlusion-query|硬件 OQ]] 还有额外缺点：draw-call 粒度、instance 内不可见性合并、popping（需要延迟读结果）。本文的目标是**整条 visibility + draw issue 都留在 GPU 上**：visibility pass 和 draw 共享同一个 buffer，CPU 只需要发一个 `DrawIndexedInstancedIndirect`。

## Pipeline 骨架

四个步骤：

1. **Occlusion buffer**：把「大 occluder」的 depth 渲到一张 DepthStencil 纹理（可以低分辨率、可以 POT）。用 null pixel shader，仅顶点着色器写 depth，吞吐量翻倍。也可以把它 prime 成主渲染 z-buffer 来减主 pass overdraw。
2. **HZB mip chain**：用 compute shader，每层用 `max` 降采样构建金字塔——对应 [[hierarchical-z-buffer|HZB]] 经典结构。Anagnostou 用 `Gather` 一次取 4 个 texel，不过 `Gather` 不支持选 mip，所以得为每层 bind 一次不同的 RT view；或者退回到 4 次 `SampleLevel`。
3. **Prop visibility compute**：每个 thread 处理一个 instance——取 world-space AABB、把 8 个角点投到 NDC、算 `minXY / maxXY / minZ`；用屏幕矩形边长选 HZB mip（`mip = ceil(log2(max(size.x, size.y)))`），再算一下「下一层 texel 是否仍能被 2×2 覆盖」决定是否跳到更细的一层；读 4 个 corner depth 的 `max` 作为场景最近深度；`minZ <= maxDepth` 则保守判可见。
4. **渲染**：用 `DrawIndexedInstancedIndirect` 驱动渲染——arguments buffer 从 compute shader 里写。

## 朴素版的两个问题

把可见 instance 直接 `AppendStructuredBuffer` 往外写最快最简单，但会踩两个坑：

- **顺序丢失**：append buffer 不保证写入顺序，若 CPU 之前做过 front-to-back 排序（为 overdraw 减少），顺序没了。
- **单次 draw 不能跨 mesh 类型**：DX11 里 `DrawIndexedInstancedIndirect` 每次只能一个 mesh；理论上一 buffer 多段 arguments + 偏移 offset 的方案可行，但 **DX11 不允许 offset 从另一个 buffer 读**，必须 CPU 常量传进去——这排除了「一个 draw call 全场景」的理想。

## 流压缩 retrofit

为了**保持实例顺序 + 全场景批量**，改写成一个 stream compaction pipeline：

1. Compute shader **不写数据**，只输出一个 per-instance 的 `predicate`（0/1）到 flags buffer；同时 `InterlockedAdd` 一个 per-prop-type instance counter。
2. **Parallel prefix scan** compute shader（Blelloch / Mark Harris 方案）把 predicate 转成一个 exclusive prefix sum：`y[i] = sum(x[0..i-1])`——意思是「在 i 之前有多少个可见 instance」，也就是 i 在压缩后的写位置。
3. **Scatter** pass 用 `predicate[i] == true` 作 mask 把 `instanceDataIn[i]` 写到 `instanceDataOut[prefix[i]]`，顺序保留。
4. 最后 patch 每个 prop type 的 `StartInstanceLocation` 偏移——base index 是「前面所有 prop type 的可见 instance 数之和」。

**第二个 DX11 陷阱**：`StartInstanceLocation` 参数只在 instance data 走 input assembler vertex stream 时有效；如果像这里一样从 `SV_InstanceID` 加 `StructuredBuffer` 采 instance 数据，它会被静默忽略。Anagnostou 的绕法是：**自己在 VS 里读 arguments buffer 的 offset、手动加到 `SV_InstanceID`**——等价于手写一个 StartInstance。

## 局限

文章把自己的局限写得很诚实：

- **Prefix scan shader 规模受限**。一个 thread group 最多 1024 threads × 2 instance = 2048 实例；超过得拆到多个 group 再合。
- **Bank conflict**。共享内存里多线程访问相同 bank 被串行化，原文引了 Mark Harris 更高效的 padding 方案。
- **HZB 的 conservative 退化**。带大洞（如窗户）的 occluder 经过 max 降采样后洞会被填上，剔除率显著下降。
- **GPU-driven 的副作用**：CPU 拿不到可见性后无法跳过动画 / 骨骼 / 粒子更新等 gameplay 逻辑。趋势是这些也迁上 GPU（[[gpu-skinning]]、GPU 粒子），所以影响会越来越小；否则可以延迟一两帧读 visibility 回 CPU。

## 在 wiki 里的坐标

本文是 Anagnostou 整条 GPU-driven 系列的**第一篇**——后续 Part 2 引入 `MultiDrawIndexedInstancedIndirect`（DX11 外部扩展）解决「一次 draw 多 mesh」的问题，再之后移植到 bgfx、再到 Digital Dragons 大会分享，构成一条连续线索。[[gpu-driven-grass-tiles|Marco Giordano 的 GPU-driven grass]] 明确把本文列为直接参考。更广义的 GPU-driven rendering 请看 Ulrich Haar / Sebastian Aaltonen 的 *GPU-Driven Rendering Pipelines*（Siggraph 2015）和 Graham Wihlidal 的 *Optimizing the Graphics Pipeline with Compute*。

## 相关

- [[occlusion-culling]]
- [[hierarchical-z-buffer]]
- [[stream-compaction]] —— parallel prefix scan
- [[indirect-draw]] —— `DrawIndexedInstancedIndirect`
- [[gpu-driven-grass-tiles]] —— 引用本文的 GPU-driven grass 实践
- [[compute-shader]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-gpu-occlusion-culling]]
