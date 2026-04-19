---
tags: [渲染, 噪声, 程序纹理, shader, gyroid]
date: 2026-04-19
sources: 1
---

# Dot Noise：基于 Gyroid 的廉价 3D 噪声

[[xor-shader-artist|Xor]] 在「Dot Noise」里提出的是一条性能友好的 3D 噪声方案，专门用于**每像素采样次数极高**（如 [[density-field-volumetric|volumetric raymarching]]）的场景。它不需要 hash 函数、不需要插值、也不需要 gradient——只是两层旋转过的正弦波做点积。

## 从 Gyroid 起步

Gyroid 是一类三周期极小曲面，GLSL 里一行就能写出：

```glsl
float gyroid = dot(cos(p), sin(p.yzx));
// 展开即 cos(p.x)*sin(p.y) + cos(p.y)*sin(p.z) + cos(p.z)*sin(p.x)
```

它很漂亮、但**周期太规整**：每 $\tau \approx 6.28$ 就完美重复，作为噪声马上露馅。

## 用 phi 打破周期

如果给其中一条正弦波的频率乘一个**无理数**，两层波永远不完全对齐。黄金比 $\phi$ 是最"无理"的——连分数展开收敛最慢。加上 phi：

```glsl
dot(cos(p), sin(PHI * p))
```

已经可观不再完美周期，但**大尺度上仍然有视觉可辨的条纹**：两层波共用同一组轴线，结构太像。

## 用黄金角度做旋转

解法：给两层波用**不同的旋转**。Xor 选了**黄金角绕 `(1, phi, phi²)` 轴**，得到一个常量 3×3 矩阵：

```glsl
const mat3 GOLD = mat3(
    -0.571464913, +0.814921382, +0.096597072,
    -0.278044873, -0.303026659, +0.911518454,
    +0.772087367, +0.494042493, +0.399753815);

float dot_noise(vec3 p) {
    return dot(cos(GOLD * p), sin(PHI * p * GOLD));
    // 范围 [-3, +3]
}
```

「最无理方向」的直觉是：轴线向量本身用 phi 构造，再旋转最无理角度——两组采样轴线最大程度互不对齐。不是严格数学证明，但视觉上确实显著降低可辨模式。

## 对比分析

- **Value / Perlin / Simplex Noise**：需要 hash、梯度、多次插值——通常 $\mathcal{O}(30)$ 条 ALU 指令才能出一个 3D 样本。
- **Dot Noise**：`cos + sin + dot + 9 mul`——大约 5–7 条 ALU。**快一个量级**。
- **代价**：大尺度下仍然能看到 underlying 正弦波结构。单 octave 不适合需要 isotropic 噪声的地方；但**分层做 fractal 之后**短板被有效掩盖。

## 什么时候用

- **Volumetric raymarch 的密度场扰动**——每条射线采样 50–100 次。
- **廉价云、湍流、液体**——叠 3–5 层 fractal 就能做大体积。
- **流体模拟的湍流** - 结合 [[turbulence-domain-warping|Xor 的湍流 domain warp]]，用 `a += sin(a*d + t).yzx / d` 迭代，可以做出[[sources/xor-decoding-phosphor|Phosphor]] 那种荧光粒子轨迹。

## 什么时候不用

- 平面大面积**地形高度图**——结构化瑕疵暴露无遗；仍然是 Simplex/Perlin 的地盘。
- 需要**确定性 tileable** 的场景——dot noise 本质是连续函数，不是离散 hash 网格。

## 相关

- [[xor-shader-artist]]
- [[classic-shader-noise]]
- [[layered-grid-noise]]
- [[turbulence-domain-warping]]
- [[density-field-volumetric]]
- [[worley-voronoi-noise]]

## Sources

- [[sources/xor-dot-noise]]
