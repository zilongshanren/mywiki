---
tags: [source, rendering, gpu-driven, occlusion-culling, compute-shader, stream-compaction]
date: 2026-04-14
sources: 1
---

# Experiments in GPU-based occlusion culling（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2017 年 11 月发表的 GPU-driven occlusion culling 实验第一篇，基于 DX11 + compute shader 完整实现「HZB 查询 → parallel prefix scan 流压缩 → `DrawIndexedInstancedIndirect` 绘制」的 retrofit pipeline。

## 摘要

目标是**不改动既有内容管线**的前提下给一个工程外挂 GPU-driven 的实例级 occlusion。流程借鉴 Splinter Cell: Conviction 的 HZB 方案并替换成 compute shader：先渲染 occluder 到 occlusion buffer、compute shader 用 `max` 降采样建 [[hierarchical-z-buffer|HZB mip chain]]、再用一个 compute shader 遍历所有 instance——对 AABB 投影算屏幕矩形、根据矩形长宽选 HZB mip、读 4 个 corner texel 取 `max` 与 `minZ` 比较。朴素版用 AppendBuffer 写可见 instance，但**丢失 front-to-back 排序**且单次 draw 不能跨 mesh 类型（DX11 的 `DrawIndexedInstancedIndirect` 不支持从 buffer 读 offset）。为此作者换成 **stream compaction** 方案：compute shader 只写 predicate，Blelloch / Mark Harris 的 parallel prefix scan 算出每个 instance 的压缩写位置，scatter pass 保序地写出可见 instance，最后 patch `StartInstanceLocation`。由于 DX11 里 `StartInstanceLocation` 对 `SV_InstanceID` 路径无效，vertex shader 手动从 arguments buffer 读 offset 补偿。作者指出局限：parallel scan 受 1024-thread 限制（最多处理 2048 instance）、bank conflict、HZB 对带洞 occluder 的保守性退化、GPU-driven 让 CPU 无法用可见性跳过动画 / 骨骼。测试在 GTX 970 上把某个 exaggerated scenario 从 5+ ms 降到 1.5 ms，occlusion pass 自身只占 0.1 ms。

## 关键要点

- HZB 查询用 `mip = ceil(log2(max(size.x, size.y)))` 选最粗有效层，4 个 corner texel `max` 即可。
- Append buffer **顺序不保证**——会破坏 front-to-back sort 和 overdraw 优化。
- DX11 的 `DrawIndexedInstancedIndirect` 不允许 args offset 从 buffer 读，**单 draw 只能一种 mesh**。
- Parallel prefix scan (Blelloch) 把 predicate 数组转成「写位置数组」——典型 stream compaction 算法。
- DX11 的 `StartInstanceLocation` 对 `SV_InstanceID` 路径无效，需要 vertex shader 手动读 arguments buffer 补偿。
- Compute scan 单 group 上限 1024 threads × 2 instance/thread = **2048 instance**；更多需跨 group 聚合。
- 实测 GTX 970 上：5 ms → 1.5 ms，occlusion pass 本身 0.1 ms。
- Marco Giordano 的 GPU-driven grass 实践直接引用了本文。

## 链接到的概念

- [[gpu-based-occlusion-culling]]
- [[hierarchical-z-buffer]]
- [[occlusion-culling]]
- [[stream-compaction]]
- [[indirect-draw]]
- [[gpu-driven-grass-tiles]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2017-11-15_experiments-in-gpu-based-occlusion-culling.md`
