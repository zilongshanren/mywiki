---
tags: [source, 渲染, GPU, mesh-shader, 剔除, 几何管线]
date: 2026-04-14
sources: 1
---

# Meshlets and Mesh Shaders（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou]] 发表于 2025 年 5 月的实操笔记，在 toy engine 里加入 mesh shader 管线并通过 meshoptimizer 生成 meshlets，定量比较 vertex shader 管线与 mesh shader 管线在剔除前后的性能。

## 摘要

Kostas 把自己引擎里 St Miguel 和 Bistro 两个场景改造到 mesh shader + amplification shader 管线上，目标是量化：什么情况下 mesh shader 比传统 VS pipeline 快、meshlet 尺寸和 threadgroup 尺寸怎么选、amplification shader 里做 hi-z 遮挡剔除的真实收益多少。几个关键发现：**(1) 没有 AS 做剔除时 mesh shader 勉强持平 VS pipeline**——最优配置 64v/124tri/64thr 下 2.78 ms vs VS pipeline 2.87 ms，但 depth-only pass 里 mesh shader 反而全面落败；**(2) 加上 AS + frustum + hi-z 遮挡剔除后差距拉开**——St Miguel gbuffer 从 2.87 ms 降到 1.59 ms（−44%）、z-prepass 从 2.41 ms 降到 1.24 ms（−48%）；Bistro 30%；**(3) 用 `min()` clamp 越界而不是 `if` 分支是 1.76× 加速**（2.78 vs 3.36 ms），divergence 比重复计算更贵；**(4) 加了 occlusion 之后 meshlet 越小越好**——32v/64tri 配置由最差变成最优，因为小包围球更容易被 hi-z 剔除。NSight 分析证实 Primitive Distributor 被 bypass、VAF 完全闲置、VGT active warps/cycle 涨 6×、ZCULL 和 VPC 的工作量显著下降。最后点明 mesh shader 相对 Frostbite 那种 compute+ExecuteIndirect 的 compute-driven meshlet cull 管线，优势在于不需要 compaction / 不走 memory roundtrip / 不需要 UAV barrier——和 [[d3d12-work-graphs]] 想解决的是同一类问题。

## 关键要点

- **CPU mesh-level frustum 太粗**：St Miguel 里一棵树是一个 mesh，meshlet 切分后能剔掉半棵树的 canopy
- **meshoptimizer 给的三个 buffer**：mesh_vertices（去重顶点索引）、mesh_triangles（三角索引）、meshlets（offset+count）
- **meshoptimizer 的 vertex 优化本身也能加速 VS 管线**（St Miguel 3.28 → 2.87 ms），Bistro 几乎无效
- **最优 meshlet/threadgroup 高度依赖 GPU+内容**：3080 mobile + St Miguel 最佳 64v/124tri/64thr
- **NVidia 建议 64v/126tri，AMD 建议 128v/256tri**——两家不一样，没通用值
- **SetMeshOutputCounts 超限是 UB**：必须用 min clamp 或分支，分支成本 +21%
- **加 AS 剔除后，小 meshlet（32v/64tri）反超**：小包围球 → 更多被 hi-z 剔掉
- **Depth-only pass**（无 PS）里 mesh shader **全面输给 VS pipeline**，除非开启 AS occlusion
- **硬件证据**：PD 几乎零吞吐、VAF 完全闲置、VGT active warps 增 6×、ZCULL/VPC 工作量显著下降
- 最大改进来自 **hi-z occlusion**，不是 mesh shader 本身的通道改善

## 链接到的概念

- [[meshlets-and-mesh-shaders]]
- [[culling]]
- [[gpu-based-occlusion-culling]]
- [[hierarchical-z-buffer]]
- [[multidraw-indirect-occlusion-culling]]
- [[d3d12-work-graphs]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2025/05/05/meshlets-and-mesh-shaders/
- 本地：`raw/articles/interplayoflight.wordpress.com/2025-05-05_meshlets-and-mesh-shaders.md`
