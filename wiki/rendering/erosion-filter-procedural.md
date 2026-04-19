---
tags: [rendering, terrain, procedural, shader, gpu-friendly, erosion]
date: 2026-04-19
sources: 1
---

# 过程化侵蚀滤波器（Erosion Filter）

一种"**看起来像被水侵蚀的地形**"的过程化噪声滤波器：不需要模拟任何水滴，每个点独立求值，GPU 友好、可分 chunk 生成，而且能**叠加到任意高度函数之上**。技术脉络从 2018 年 clayjohn 的 Shadertoy → 2023 年 Fewes 的抛光版 → 2025-2026 年 [[rune-skovbo-johansen]] 的 Advanced Terrain Erosion Filter 一路演进。

## 基本思想

1. **从高度函数取梯度**。水流沿 −∇h 方向。
2. **沿坡向生成条纹**（cos 波做高度偏移，sin 波做斜率分量）。条纹之间是 gully，之间是 ridge。条纹本身带有坡度，把 sin 乘以与梯度正交的向量即可得到新的梯度贡献。
3. **迭代多个 octave**：用叠加过前一 octave 的梯度来决定下一个更细尺度的条纹方向。条纹在 ridges/creases 处分叉，形成分形水道。
4. **用 cell 内 pivot 避免远距离失真**：rotation 围绕 pivot 会在远处把"第几条条纹"错开，所以把平面分成网格，每 cell 一 pivot，类似简化 Worley 噪声，然后在邻近 cell 间对条纹做 blending。

## 峰顶与河谷的保留：frequency vs. fade

坡度趋零（峰/谷）时条纹方向失定义，直接应用会产生混乱。两种方案：

- **Frequency approach**（clayjohn / Fewes）：让条纹频率正比于坡度，坡度为零时条纹"无限粗"——峰顶永远落在白条上。代价：河谷底部出现隆起，无法生成锋利 V 型谷。
- **Fade approach**（作者原创）：条纹宽度保持不变，坡度趋零时把 gully 淡出到用户提供的 `fadeTarget`（典型做法：取高度归一化到 [-1, 1]，−1 为谷 1 为峰）。再配合 shaping 函数 `1 − (1 − t)²` 代替 `sqrt(t)`，以消除峰谷附近的不连续折痕。优点：V 型谷和锋利峰可共存。

## 作者的三个关键增强

1. **Stacked fading**（层叠淡出）：把上一个 octave 的 gully 作为下一 octave 的 `fadeTarget`，同时把"坡度为 0"处的 mask 累乘到下一层；小 gully 不会再骑在大 ridge 上。通过 `combiMask = pow_inv(combiMask, detail) * newMask` 提供 *detail* 参数：值越小，高频 gully 越被限制在陡坡。
2. **Normalized gullies**（归一化 gully）：把插值后的 `(cos, sin)` 归一化——前提是做部分归一化（长度 × 2 再 clamp 到 1），以规避完全归一化在波完全抵消点处产生的"loopy" 尖刺伪影。这一步催生了 [[phacelle-noise]]。
3. **Straight gullies**（直 gully）：小尺度 gully 往往沿大 gully 弯曲而非干脆分叉。解法：计算 gully 方向时用 sin 的 *sign* 而非值本身，模拟"三角波斜率恒定"。然后并行维护两份导数——输出导数保留 fade，但用于下一 octave 方向计算的 `gullySlope` 不做 fade。

## 附加能力

- **Pointy peaks**：把 gully 权重乘 0.5、侵蚀强度乘 2.0，即可让归一化后变圆的山峰重新变尖。
- **Edge rounding**：通过在 shaping 函数后链式 ease-in，分别对 ridges / creases 做可调圆角；按 lacunarity 反向缩放，使各 octave 视觉一致。
- **Ridge map / 树枝状水系**：最终的 `fadeTarget` 本身就近似是"ridge+crease 图"。把它作为 albedo mask，就能在谷底画出 *dendritic drainage*（枝状水系）线条——但因为条纹是插值而成的，线条有时会中途断掉；不精确但视觉可用。

## 与模拟式侵蚀的对比

- 模拟式（水滴 / thermal / hydraulic）：物理正确，但慢、难分 chunk、难用 GPU 滤波形式叠到已有高度上。
- 此滤波器：纯过程化，**单 pass、O(cells × octaves) 常数复杂度**、可在 GPU 上批量处理。代价：解析导数本身不准（作者坦言最后放弃了对导数精度的追求）；fadeTarget 基于高度而非曲率，在"高谷比低峰还高"的地形里不够鲁棒——作者把 fadeTarget 的定义权交给用户。

## 社区反响

作者开源后（MPL v2），已有人把它移植到 Unity Burst、Unity ShaderGraph、Unreal Landmass、Godot、Houdini、Hytale Worldgen v2、球面地形、甚至 Desmos 3D 上。

## 相关

- [[phacelle-noise]] — 从该侵蚀滤波器中独立出来的方向性噪声
- [[directional-noise]]
- [[worley-voronoi-noise]]
- [[classic-shader-noise]]
- [[shaping-functions]]
- [[turbulence-domain-warping]]
- [[layered-grid-noise]]

## Sources

- [[sources/runevision-erosion-filter]]
