---
tags: [source, 渲染, GPU, D3D12, workgraphs, 性能]
date: 2026-04-14
sources: 1
---

# An introduction to workgraphs part 2: Performance（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou]] 发表于 2024 年 9 月的续篇，专注比较 [[d3d12-work-graphs]] 与 compute shader + ExecuteIndirect 方案在 FidelityFX SSSR 场景下的性能差异。

## 摘要

Kostas 把 FidelityFX SSSR 的 classification + raymarching 两个 pass 改成等价的 2-node work graph，在 RTX 3080 mobile / 1080p 上做对比。结果出人意料——work graph 版本 **2.18 ms**，compute shader 版本只有 **0.65 ms**。作者用 NSight GPU Trace + Real-Time Shader Profiler 细挖，发现 work graph 的理论 occupancy 从 32 掉到 16（raymarching 节点）、实际 warp occupancy 只有 18-27%、并出现了 compute shader 不会有的 **Sync Q Waiting** 前端 stall。把 classification 节点改成空函数仍然保留 0.38 ms 的固定开销，说明**大头是节点启动成本而非 shader 本体**。NSight 显示的 warp/threadgroup 数字和理论值对不上，作者推测 driver 在内部用不同方式重打包 launch。最后尝试把 raymarching 节点从 thread launch 改到 coalescing launch，吃到 L1TEX 命中率提升带来的 **2.18 → 1.81 ms**。文章引用一位读者推测 NVidia 的实现可能是"while loop 轮询 → launch → atomic join → 下一批"，而 AMD HPG 透露的实现是每节点一条 VRAM ring buffer，由 SIMD 直接写入、Micro Engine Scheduler 派发。

## 关键要点

- **Work graph 在 SSSR 场景慢 3×**（RTX 3080 mobile，1080p），主要原因是调度固定开销 + 低 occupancy
- **空 shader 节点仍保留 0.38 ms 开销**——确认是 launch overhead 而非 shader 计算
- **NSight 报告的 threadgroup/warp 数字不符合理论**（80,000 → 40,516），driver 在内部重打包
- **Sync Q Waiting 指标**是 work graph 独有的 stall，暗示 front-end 在等待节点调度
- **Coalescing launch 比 thread launch 好** ~17%：意外地提升了 L1TEX 吞吐，即便不用 groupshared 也值得试
- **AMD 实现细节**：每节点一条 VRAM ring buffer，SIMD 写入，Micro Engine Scheduler 派发，用 `MaxRecords` 约束避免死锁
- 作者结论是"技术很酷、目前性能还没优势、等 driver 和 profiler 成熟"

## 链接到的概念

- [[d3d12-work-graphs]]
- [[screenspace-reflections]]
- [[bottleneck-analysis]]
- [[gcn-wave-occupancy]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2024/09/09/an-introduction-to-workgraphs-part-2-performance/
- 本地：`raw/articles/interplayoflight.wordpress.com/2024-09-09_an-introduction-to-workgraphs-part-2-performance.md`
