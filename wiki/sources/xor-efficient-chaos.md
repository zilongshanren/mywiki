---
tags: [source, 渲染, 噪声, shader, 程序纹理]
date: 2026-04-14
sources: 1
---

# Efficient Chaos（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2025 年 7 月的一篇，介绍**在像素 shader 里做廉价伪随机散布**的技术。目标是星空、雨、雪、落叶、粒子等需要「看起来是随机散点」但又要便宜到 3D 也能用的场景。

## 摘要

文章的核心观察是：**伪随机感不必靠 hash，只要打破规则网格的周期性就够了**。经典 Worley noise 要做 `3^N` 邻域采样——2D 需要 9 次、3D 需要 27 次、4D 需要 81 次——在实时 3D 场景里很快就成瓶颈。Xor 的方案是从最简单的规则网格出发（`mod(coord, 2)` 每格放一个点光源），然后用三板斧叠多层：每层**平移**一个非整数偏移、**缩放**一点点、用**黄金角**（≈137.5°）对应的 `mat2` 旋转——黄金角的无理性质保证了任意多层都不会对齐到同一个网格。5 层左右肉眼就看不出格子感。为了保留「原始方向」以便做视差或定向光照，单独维护一个累积旋转矩阵，原始坐标不动。更顽固的对齐条纹可以用 `p += amp * sin(p.yx)` 的正弦 warp 或在每层按廉价阈值打洞来破。最漂亮的性质：整套流程从不做邻域采样，3D 下代价和 2D 完全一样。

## 关键要点

- **Worley 的维数诅咒**：`3^N` 邻域，3D 以上不划算。
- **基础单元**：`mod(coord, 2) - 1` 得到 cell-center 坐标，`length` 算到中心的距离，做点光源衰减。
- **三板斧**：shift（错开格子）、scale（打破周期）、rotate by 黄金角（最不容易对齐的无理角）。
- **黄金角 `mat2`**：`mat2(0.2225, -0.9749, 0.9749, 0.2225)`。在自然界里就是向日葵种子、松果鳞片的最优排布。
- **保留原始方向**：用单独的累积 `orient` 矩阵，需要时乘一次，保留 parallax / 定向光能力。
- **修补条纹**：`p += 0.2 * sin(p.yx)` 的正弦 warp 便宜好用。
- **层间打洞**：远看时叠加层过于均质，随机裁掉一部分 cell 可破。
- **3D 免费扩展**：没有邻域采样就没有维数依赖；`vec2 → vec3` 即可。
- 完整 demo 在 [Shadertoy tX3GW2](https://www.shadertoy.com/view/tX3GW2)。

## 链接到的概念

- [[layered-grid-noise]]
- [[fragment-shader]]
- [[poisson-disk-sampling]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/chaos
- Shadertoy demo：https://www.shadertoy.com/view/tX3GW2
- 本地：`raw/articles/mini.gmshaders.com/2025-07-10_efficient-chaos.md`
