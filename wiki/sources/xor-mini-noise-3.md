---
tags: [source, 渲染, shader, 噪声, simplex, 程序纹理]
date: 2026-04-14
sources: 1
---

# GM Shaders: Noise 3（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2024 年 1 月 13 日的噪声第三集，填补第一、第二集没覆盖的一块：**Simplex noise、函数 vs 纹理的权衡、以及如何把噪声做成可 tile**。和 [[sources/xor-mini-noise]]、[[sources/xor-mini-noise-2]] 一起共同构成 [[classic-shader-noise]] 的源头。

## 摘要

**Simplex noise** 由 Perlin 本人发明，用来替代 Perlin noise 在高维下的采样爆炸：Perlin 在 2D 需要 4 次、3D 需要 8 次、N-D 需要 2^N 次哈希采样，而 Simplex 分别只要 3 / 4 / N+1 次。思路是**把方形 cell 倾斜成等边三角形的 rhombus**，再按 sub-cell 内部的对角关系选择相邻两个顶点共 3 个去采样。具体步骤：(1) 倾斜 `skew = p + F*(p.x+p.y)`，其中 `F = 0.366025`；(2) `floor(skew)` 得 cell，`sub = skew - cell`；(3) 按 `sub.x > sub.y` 决定走上三角还是下三角；(4) 把 3 个顶点到 `p` 的相对位移代入 `max(0.5 - d², 0)⁴` 作权重；(5) 对每个顶点 hash 出梯度方向，点乘位移后按权重求和。对比之下 Simplex 在 2D 未必比 Perlin 快（代码复杂度更高），**真正的收益在 3D/4D**。

第二块是**函数 vs 纹理的取舍**——函数版无限范围 / 动态 / 高精度但慢且跨硬件不一致，纹理版可复杂、便宜、一致但有限范围 / 动画不便 / 多 VRAM。Xor 把两张利弊表直接摆出来让读者自行决策。第三块是**tileable noise**：只要坚持方形 cell，让采样 hash 前 `mod(cell, s)`，value/Perlin/Worley/Voronoi 都能做成 s 的倍数内 tile 的。fractal 版为了不打破方形约束，把旋转换成 `p = p.yx*2 + 9`（x/y 互换 + 放大 + 平移），同样能达到 octave 去相干的效果。

## 关键要点

- **Simplex = 三角 cell 的 Perlin**：在 N 维只需 N+1 次哈希采样，相比 Perlin 的 2^N 在高维大幅节省。
- **魔数 F = 0.366025, G = 0.211325**：由 `(√(N+1) - 1)/N` 导出的倾斜 / 反倾斜因子，2D 场景下的固定常数。
- **权重 `(0.5 - d²)⁴`**：四次幂 falloff 使得 cell 边界处刚好归零，自然避免硬边。
- **2D 未必有收益**：2D Simplex 的节省被代码复杂度抵消；**3D/4D 才是主场**。
- **Functions vs Textures 是工程取舍**：纹理胜在跨设备一致和复杂噪声便宜，函数胜在无限范围、动态参数、精度高。
- **Tileable noise 的机制就一个 `mod`**：在 hash cell 坐标前 `mod(cell, s)`，让 s 等于纹理宽度即可 tile。
- **Fractal 的 tile 替代旋转方案**：用 `p = p.yx*2 + 9`——swap + scale + translate——达到和 143° 旋转一样的 octave 去对齐效果，但保留方形 cell 兼容 tile。
- **Simplex 是一类思想**：同一套「倾斜空间让 cell 顶点更少」的做法可以迁移到其他邻域密度问题。

## 链接到的概念

- [[classic-shader-noise]]
- [[worley-voronoi-noise]]
- [[layered-grid-noise]]
- [[fractal-texturing]]
- [[xor-shader-artist]]
- [[fragment-shader]]

## 原文

- 链接：https://mini.gmshaders.com/p/noise3
- 本地：`raw/articles/mini.gmshaders.com/2024-01-13_gm-shaders-noise-3.md`
