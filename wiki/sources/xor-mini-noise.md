---
tags: [source, 渲染, shader, 噪声, 程序纹理]
date: 2026-04-14
sources: 1
---

# Mini: Noise（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 11 月 4 日的一篇，是 Mini 系列里关于**程序噪声**的第一集，手写展开 **hash → value noise → Perlin noise** 三个函数。一周后的 [[sources/xor-mini-noise-2|Noise 2]] 续写 Worley / Voronoi / fractal，两篇共同构成 [[classic-shader-noise]] 这一页。

## 摘要

作者从最基础的 sine-fract 哈希开始——`fract(sin(p.x*0.129898 + p.y*0.78233) * 43758.5453)`——强调 magic number 要避免明显的整数比，否则会出现对角条纹；向量版本可以用 `mat2` 把两组魔数打包。随后按 **round → sample corners → interpolate** 三步描述 **value noise**：像素落到整数 cell，采样四角 hash 值，做 `sub*sub*(3-2*sub)` 的 cubic 插值再 lerp，得到带一点平滑的格子随机场。**Perlin noise** 的区别只在角点存的不是标量而是单位向量，每个角贡献 `dot(dir, offset-sub)`，然后套上 quintic 曲线 `sub³(10 - 15*sub + 6*sub²)` 做更平滑的插值——由于输出范围是 `[-√2, +√2]`，归一化时乘 0.7 加 0.5。作者把 cubic / quintic 和 [[sources/xor-mini-interpolation|Mini: Interpolation]] 串起来：同一个多项式出现在滤波、噪声、smoothstep 中。文章结尾指向完整的 ShaderToy demo，并预告续篇会讲 Worley / Voronoi / fractal。

## 关键要点

- **sine-fract 哈希**：教学够用，但对 cross-vendor 精度敏感；魔数要随维度选不同的一套。
- **Value noise 三步走**：floor 出 cell → 四角哈希 → 双线性 + cubic 预处理 sub-pixel。
- **Perlin 的差异**：存「方向向量」而非「标量」，每个角点贡献是方向 · 相对坐标的点积。
- **Cubic vs quintic**：value noise 用 `3x²-2x³` 够，Perlin 推荐更光滑的 `6x⁵-15x⁴+10x³`，因为需要 C² 连续。
- **维数代价指数级**：3D value noise 要 8 次哈希 + 7 次 lerp；高维别硬刚。
- **Perlin 归一化**：乘 0.7（≈√0.5）加 0.5 把 `[-√2, √2]` 压到 `[0, 1]`。
- **信道复用**：同一份 `hash2` 后面 Worley、Voronoi 都要用，算基础 utility。

## 链接到的概念

- [[classic-shader-noise]]
- [[shader-color-interpolation]]
- [[non-cryptographic-hash]]
- [[xor-shader-artist]]
- [[fragment-shader]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-noise-1437243
- 本地：`raw/articles/mini.gmshaders.com/2022-11-04_noise.md`
