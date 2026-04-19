---
tags: [source, rendering, culling, simd, ispc]
date: 2026-04-19
sources: 1
---

# More (Robust) Frustum Culling（bruop.github.io）

[[bruno-opsenica|Bruno Opsenica]] 2021 年 2 月的续篇，用分离轴定理（SAT）修掉上一篇顶点法的 false negative，并改用 [[ispc-simd-culling|ISPC]] 实现 SIMD 化。

## 摘要

作者首先举例说明旧测试的漏洞：OBB 比视锥大时 near plane 穿入其中、或边-边相交而所有顶点都落在对方之外，都会被误剔。正解是 [[obb-frustum-sat|分离轴定理]]：两凸体不相交则必存在一条分离轴让它们投影不重叠。对 OBB × frustum 需测试 26 根候选：两体各自面法向（OBB 3 + frustum 5）加上所有边向量两两叉积（3×6=18）。在 view space 中做数学上最简洁——frustum 原点在零、上右方向对齐 y/x 轴。OBB 投影用 `MoC ± Σ|M·axis_i|·extent_i`；frustum 投影用 David Eberly 给的 `τ_0, τ_1` 闭式。10k 物体在 i5 6600k 上 ~0.85 ms，比旧 SSE 版慢一倍多。用 Intel ISPC 重写（premake 配 SSE4/AVX2 双目标）、AABB 改 SoA、矩阵乘法留在 ISPC 外（避免 gather），最终 0.3 ms，与旧手写版同速但无 false negative。作者实测 99.9% 物体在第一组 frustum 法向测试就被剔，SIMD lane 散度问题不明显。

## 关键要点

- 旧顶点法的 false negative：OBB ⊃ near plane、边-边相交
- SAT 的 26 根轴：OBB 3 法向 + frustum 5 法向 + 3×6=18 叉积对
- view space 可消掉大量计算
- ISPC 用法与陷阱：AoS→SoA，否则编译器会警告 gather/scatter
- matrix-mul 留给手写 SSE，AABB 进 ISPC
- 统计：10,000 物体中第一组 frustum 法向剔 8,913 个，其他测试加起来 4 个——99.9% 早退
- 最终 0.3 ms / 10k，与旧法同速且健壮

## 链接到的概念

- [[obb-frustum-sat]]
- [[ispc-simd-culling]]
- [[culling]]

## 原文

- 链接：https://bruop.github.io/improved_frustum_culling/
- 本地：`raw/articles/bruop.github.io/2021-02-17_more-robust-frustum-culling.md`
