---
tags: [rendering, culling, collision]
date: 2026-04-19
sources: 2
---

# OBB × 视锥的分离轴测试

一种朴素的 OBB 视锥剔除做法：把 AABB 八个顶点用 MVP 变到 clip space，测试 `-w ≤ x,y ≤ w`、`0 ≤ z ≤ w` 是否有任意顶点满足。Bruop 2020 实现的版本在 10,000 个 BoomBox 的场景下把 GPU 帧时间从 5.8 ms 降到 1.5 ms，SIMD 化（AVX2、一次处理 8 顶点）后 CPU 剔除从 1.2 ms 降到 0.3 ms。

但这个测试有 **false negative**：当 OBB 比视锥大、且所有 8 顶点都在视锥外却两者边相交（边-边相交或 near plane 穿入 OBB 内部）时，物体会错误被剔，表现为视野切换时闪烁。正例（[[view-frustum-culling-ryg]] 家族）需要更健壮的方法。

2021 年 Bruop 改用**分离轴定理（SAT / Hyperplane Separation Theorem）**：两凸体若不相交，必存在一条分离轴让两者投影不重叠。对 OBB × frustum 共需测试 26 根候选轴——两边各自面的法向（OBB 3 根 + frustum 5 根，去掉反平行）+ 所有边向量的两两叉积（OBB 3 根 × frustum 6 根 = 18 根）。在 view space 中做可极大简化 frustum 几何。投影时 OBB 用 `center ± Σ|M·axis_i| · extent_i`；frustum 端用 David Eberly 给出的 `τ_0, τ_1` 闭式表达（按轴与视方向夹角决定是近平面还是远平面定界）。

实测 10,000 物体里 99.9% 在第一组 frustum 法向测试就被剔除，分支散度对 SIMD 影响很小。Bruop 用 [[ispc-simd-culling|ISPC]] 把 SAT 版本压回 0.3 ms，与顶点法同速但无 false negative。

## Sources

- [[sources/bruop-frustum-culling]]
- [[sources/bruop-more-robust-frustum-culling]]
