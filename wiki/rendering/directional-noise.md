---
tags: [rendering, noise, procedural, shader]
date: 2026-04-19
sources: 1
---

# Directional Noise（方向性噪声）

"方向性噪声"是一族能生成沿**指定方向场**走向的条纹（stripes / gullies / anisotropic noise）的过程化噪声。典型用途包括：

- **地形侵蚀**：条纹沿地表坡度方向对齐，模拟出雨水冲刷形成的分形水道。例如 [[erosion-filter-procedural]]。
- **各向异性材质**：头发、金属拉丝、木纹、水流。
- **纹理合成**：依照输入向量场做方向性 Gabor/Phasor 合成。

## 家族谱系（作者视角）

根据 [[rune-skovbo-johansen]] 的考据，沿同一条脉络的代表作按时间排列：

1. **Voronoi Noise**（iq 的 Shadertoy）——引入"4×4 moving window of cells"思想，每个 cell 随机放置 pivot。
2. **Gabor Noise**——在随机位置上叠加有方向性的正弦核。
3. **Gavoronoise**（user *guil*）——把 Voronoi 的 moving-window 和 Gabor 的正弦核结合，但方向是**全局**的。
4. **clayjohn `erosion` 函数**（2018）——让条纹方向**每像素可变**，同时插值余弦和正弦以获得解析导数，用于分形地形。
5. **Fewes / Felix Westin 的 Terrain Erosion Noise**（2023）——抛光 clayjohn，简化了正弦前乘向量。
6. **Phasor Noise**（Tricard 等，2019）——同期的另一条学术脉络，Gabor Noise 的相位重构；强调频域控制与各向同性控制，但实现昂贵（每像素 144~400 次内循环）。
7. **[[phacelle-noise]]**（Johansen, 2026）——把"插值余弦+正弦 → 单位圆点 → 归一化恢复相位"这一步显式化，采样降到 16 次/像素，同时提供 API 友好的 `Simple` 变种（方向场做函数参数）。

## 核心技术要点

- **cells + moving window**：把无限空间切成网格，每 cell 一个随机 pivot，采样时只需看 3×3/4×4/5×5 近邻，保证"无限但局部可求值"。
- **cos+sin 双通道**：让插值结果既可视为标量条纹，也可归一化恢复相位/导数。
- **权重函数**：高斯（Phasor）或减去常数的指数（Phacelle）——后者在 cell 边界处归零，避免 grid-aligned 伪像。
- **方向场 vs. kernel 方向**：单 splat-direction / 多 splat-direction 的选择决定了输出平滑程度与链式调用可行性。

## 相关

- [[phacelle-noise]]
- [[erosion-filter-procedural]]
- [[worley-voronoi-noise]]
- [[classic-shader-noise]]
- [[turbulence-domain-warping]]
- [[layered-grid-noise]]

## Sources

- [[sources/runevision-phacelle-noise]]
- [[sources/runevision-erosion-filter]]
