---
tags: [procedural-generation, sampling, mathematics, infinite-world, poisson]
date: 2026-04-27
sources: 1
---

# 泊松点过程与无限均匀分布（Poisson Point Process）

在无限平面上生成均匀随机点分布时，最直觉的做法——**jittered grid（抖动网格）**——并不是真正的独立均匀分布。[[boris-the-brave]] 在 2024 年的文章中给出了理论上正确的模型：**泊松点过程（Poisson Point Process）**。

## Jittered Grid 的问题

Jittered grid 把平面切成等大格子，每格放一个点，点在格内随机偏移。这保证了密度均匀，但引入了隐性负相关：格子内已有一点，该格内任何其他位置的概率立刻降为零。真正的均匀独立分布里，某区域的稠密簇不影响邻近区域——这正是 jittered grid 无法复现的特性。

## 泊松点过程的数学依据

对面积为 A、密度为 ρ 的区域，其中点的数量应服从 **Poisson(ρ·A)** 分布，且任意不相交区域之间相互独立。推导路线是极限过程：在 N×N 矩形里均匀分布 ρN² 个点，取出 1×1 子矩形，其中的点数满足二项分布 B(ρN², 1/N²)；当 N→∞ 时，该二项分布收敛到 Poisson(ρ)。这种分布被称为**均匀泊松点过程（Homogeneous Poisson Point Process）**。

## 实现：Chunked Lazy Evaluation

和 [[rendering/poisson-rect-process]] 与 [[game-development/infinite-chunked-procedural-generation]] 的一般策略相同，把无限平面切成 chunk，每块独立生成：

1. 用 `(chunk_x, chunk_y)` 导出确定性种子
2. 从 Poisson(ρ·chunk_area) 采样得到点数 n
3. 在 chunk 内均匀散布 n 个点

推荐 chunk 大小取 1/√ρ，使每块平均点数恰好为 1——与 jittered grid 密度等效，但不再有「每格精确一点」的强约束，可以出现 0 个或多个点。泊松分布的采样可参考 Knuth 算法（文章中给出伪代码，注意对大参数 L 分段累乘避免浮点下溢）。

## 与相关概念的关系

- [[rendering/poisson-disk-sampling]]：Poisson disk 是另一种均匀点采样，加了最小间距约束，不是点过程意义下的独立均匀分布，但在渲染采样中更常用。
- [[rendering/poisson-rect-process]]：把点过程扩展为矩形，增加了非重叠过滤；依赖同样的 chunking 思路。
- Jittered grid 与本文方案的视觉差异微妙，但在稠密场景或需要真正独立性的统计应用中，差异会放大。

## Sources

- [[sources/boris-infinite-uniform-points]]
