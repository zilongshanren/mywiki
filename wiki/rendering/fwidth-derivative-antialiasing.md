---
tags: [渲染, 反走样, shader, sdf, 导数]
date: 2026-04-19
sources: 1
---

# 用 fwidth 做 shader 解析抗锯齿

Xor 的 *Anti-Aliasing* 教程给出了一个在 shader 日常里极其实用的三级递进模板：**从"完美 SDF"到"任意连续函数"再到"手动采样导数"**。核心思路与 [[analytical-antialiasing]] 一致——**在边缘上按像素尺度做一个 1 像素宽的线性淡出**——但重心放在「你**不**知道准确距离时怎么办」。

## Level 1：完美 SDF

如果已经有 [[sdf-2d-primitives|signed distance field]]，直接除以 texel 尺度即可：

```glsl
float gradient = clamp((radius - dist) / texel + 0.5, 0.0, 1.0);
```

`dist` 从负到正跨越 0 的那一像素，`gradient` 刚好从 1 淡到 0。这个写法适用于所有严格 SDF——圆、胶囊、星形、字体 MSDF……只要你能把距离正确归一化到 pixel unit。

## Level 2：fwidth 近似

噪声、层叠扭曲、procedural 渐变——它们不是严格 SDF，梯度不恒定，有的地方陡、有的地方缓。一个固定 scale 做不到处处一像素。

解决办法是**让 GPU 告诉你该像素里函数变化了多少**，也就是 `fwidth()`：

```glsl
float antialias_l1(float d) {
    return clamp(0.5 + d / fwidth(d), 0.0, 1.0);
}
```

`fwidth(d) = |dFdx(d)| + |dFdy(d)|` 是 L1 范数近似，便宜但对角方向会**过估**——小圆会被压成菱形（Freya Holmér 的 Shapes 把它叫 **Fast Local AA**）。Xor 更常用 L2 版本，手算 length 稍贵但各向同性：

```glsl
float antialias_l2(float d) {
    vec2  dxy   = vec2(dFdx(d), dFdy(d));
    float width = length(dxy);
    float scale = width > 0.0 ? 1.0 / width : 1e7;
    return clamp(0.5 + 0.7 * scale * d, 0.0, 1.0);
}
```

两个细节：

- **除零保护**：`width == 0` 时 `1/width` 爆炸，用一个大的常数（`1e7`）代替即可。
- **0.7 系数**：约 `1/√2`。GPU 的偏导数是按 2×2 quad 计算的，最坏情况（对角方向）下 `length(dxy)` 会比真实 per-pixel 梯度宽度大一个 `√2` 因子；乘 0.7 把平均边缘回拉到接近 1 像素的过渡。这是经验系数，Xor 在他自己的 Shadertoy 上做 A/B 得出来的。

## Level 3：手动偏导数

上面的办法对**不连续函数**会崩——`floor(x/10)` 的 `dFdx` 永远是 0 或爆炸峰值，`fract(x)` 在周期边界处有跳跃。另一种失败场景：2×2 quad 粒度太粗，细条纹上导数拿到错误邻居。

Xor 的方案是**放弃 GPU 的硬件导数，自己采样三次**：

```glsl
float antialias_l2_dxy(float d, vec2 dxy) {
    float width = length(dxy);
    float scale = width > 0.0 ? 1.0 / width : 1e7;
    return clamp(0.5 + 0.7 * scale * d, 0.0, 1.0);
}

float grad00 = grad(pos);
float grad10 = grad(pos + vec2(1, 0));
float grad01 = grad(pos + vec2(0, 1));
vec2  dxy    = vec2(grad10, grad01) - grad00;
```

有一个关键 insight：**做导数的那个函数可以和做阈值的函数不同**。比如要在 `fract(grad) - 0.5` 上画多条条纹，`fract` 把梯度打碎——那就**只在 `grad` 上算 dxy**，再代入 `antialias_l2_dxy`，因为整条纹方向上 `grad` 的变化率是连续的。判断和感知只需要**相同量纲的 dxy**，不需要逐点值严格相等。

代价：三次 `grad(pos)` 采样 vs 硬件导数几乎免费，所以只在高频率场景或导数失真时才启用。

## 和 [[analytical-antialiasing]] / [[hlsl-derivation-correctness]] 的关系

- 它是 Frost Kiwi AAA 在「通用 procedural shader」下的推广：AAA 假设你有 SDF；Level 2/3 让你**在不知道距离的情况下就地估计**。
- `divergent gradient` 问题（分支中调用 `dFdx` 导致结果不定）和这里手算 dxy 的出发点是一致的：当硬件导数不可信，就自己采样。

## 相关

- [[analytical-antialiasing]]
- [[sdf-2d-primitives]]
- [[hlsl-derivation-correctness]]
- [[divergent-gradient-in-branches]]
- [[aliasing]]
- [[msaa-ssaa]]
- [[temporal-antialiasing]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-anti-aliasing]]
