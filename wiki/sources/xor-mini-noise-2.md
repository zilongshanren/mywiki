---
tags: [source, 渲染, shader, 噪声, 程序纹理]
date: 2026-04-14
sources: 1
---

# Mini: Noise 2（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 11 月 11 日的续篇，补齐 **Worley → Voronoi → fractal** 三个在第一集里被砍掉的噪声函数。和 [[sources/xor-mini-noise|Mini: Noise]] 一起构成 [[classic-shader-noise]] 这一页的源头。

## 摘要

**Worley noise** 不做插值，而是在每个整数 cell 里随机放一个特征点，取「当前像素到最近特征点的距离」作为输出。为了避免 cell 边界跳变，需要遍历 3×3（2D）或 3×3×3（3D）邻域取最小值。Xor 用 `hash2(cell) + cell - p` 构造相对位移，再 `length()` 算距离，初始值用 `dist = 9.0` 作为安全上界。**Voronoi** 是 Worley 的分支变种：循环内同时记录最近的 `sample_cell` 坐标，最后 `return hash1(voronoi_cell)`——每个 Voronoi 域内颜色是恒定的随机灰度，得到蜂窝状图案。**Fractal noise** 则是把任意噪声按 octave 叠加：每层权重 `weight *= 0.5`（persistence），坐标 `p *= mat2(1.6, 1.2, -1.2, 1.6)`——这个矩阵把坐标 scale 2 并旋转约 143°，用旋转角不是 90 倍数的关键动机是**打破相邻 octave 的对齐**（和 [[layered-grid-noise]] 黄金角旋转是一模一样的出发点）。最后做加权平均 `noise_sum / weight_sum` 拿到 fBm。作者鼓励把 fractal 作用到任何一种噪声上都可以，6 octave 是个常用默认值。

## 关键要点

- **Worley = 距离场**：`floor` 出 cell，`hash2` 出特征点，`length` 拿距离，`min` 合并 3×3 邻域。
- **Voronoi = 最近 cell hash**：多记一个 `voronoi_cell`，循环外再 `hash1(voronoi_cell)`，域内同色。
- **初始 dist 设 9**：安全上界，足够覆盖任何 2D/3D/4D 邻域的最远点。
- **Fractal = fBm 通用模板**：octave 循环 + persistence + scale/rotate 矩阵。
- **143° 旋转的意义**：旋转 90° 的倍数会让相邻 octave 对齐出网格；任意非对称角即可破坏周期。
- **加权平均而不是简单求和**：`noise_sum / weight_sum` 自动处理任意 persistence，不需要额外归一化。
- **Fractal 对谁都有效**：value、Perlin、Worley、Voronoi 都能 fBm，产物分别对应云/地形/岩石/马赛克。

## 链接到的概念

- [[classic-shader-noise]]
- [[worley-voronoi-noise]]
- [[layered-grid-noise]]
- [[fractal-texturing]]
- [[xor-shader-artist]]
- [[fragment-shader]]

## 原文

- 链接：https://mini.gmshaders.com/p/noise2
- 本地：`raw/articles/mini.gmshaders.com/2022-11-11_noise-2.md`
