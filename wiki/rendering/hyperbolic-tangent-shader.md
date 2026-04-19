---
tags: [渲染, shader, 数学, tonemap, glsl]
date: 2026-04-19
sources: 2
---

# tanh 在 Shader 里的用法

`tanh`（双曲正切）在 shader 里最常被当作「**把任意实数无损映射到 (-1, +1)** 的可微 sigmoid」来用。[[xor-shader-artist|Xor]] 在教程里把它定位为一种**廉价、便利、常忘**的工具函数。

## 数学与实现

数学定义三种等价视角：

- **双曲三角**：$\tanh(\theta) = \sinh(\theta) / \cosh(\theta)$，单位双曲线上的斜率。
- **指数**：$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}} = 1 - \frac{2}{1 + e^{2x}}$。
- **Sigmoid**：对称的 S 形曲线，范围 (-1, +1)。

GLSL 1.30 起有 `tanh` 内建函数。WebGL 1.0 / GameMaker（GLSL ES 1.00）要手写：

```glsl
float tanh(float x) {
    float e = exp(-2.0 * x);
    return -1.0 + 2.0 / (1.0 + e);
}
```

## 用场景

### Tone mapping（最常见）

Xor 写 tweet shader 时几乎每个都用 `tanh` 压回显示范围：

```glsl
o = tanh(col / EXPOSURE);   // (−1, 1)，再裁到 [0, 1]
```

好处：**免配置**、只一条指令、所有 HDR 亮度都能"软上限"。缺点：不像 ACES 或 Reinhard 那样考虑色调色域。「够用」级别。

### 无定边的混合

想让两段颜色"慢慢开始、慢慢结束"但又不想设具体 start / end 坐标：

```glsl
mix(col_a, col_b, tanh(x * SPREAD) * 0.5 + 0.5)
```

`SPREAD` 控制过渡陡峭度，`x` 可以是任意坐标/时间变量。

### 调试可视化

把某个可能越界的变量 `tanh(v)` 一下就能看到它的大小趋势，**不关心绝对值**。负数显暗、正数显亮、溢出也不会爆屏。

### 神经网络激活

GAN 最后一层出 RGB 时常用 `tanh`——把 `[-∞, +∞]` 限在 $[-1, +1]$，再线性映射到 $[0, 1]$ 作为像素。

## 与其它 sigmoid 的对比

- **smoothstep**：有明确起点终点，能内插边缘。
- **sigmoid (logistic)**：范围 $[0, 1]$，多一次加减。
- **tanh**：范围 $[-1, 1]$，天生带正负、多一次减 1。

在 shader 里三者代价相近，选择主要看语义。

## 性能

现代 GPU 上 `tanh`、`exp`、`log` 都用同一套专门硬件（transcendental unit）：通常 4 cycle、吞吐 1/4。和 `sin`/`cos` 同一量级。移动端有时 ALU 实现不那么划算，手写 `exp(-2x)` 版本更可控。

## 在 raymarch 色彩累积里常见的模式

```glsl
for (int i = 0; i < N; i++) {
    ...
    col += L / d;     // 不断累加，最终可能很大
}
col = tanh(K * col);  // 无论 K·col 多大，输出 (-1, 1)
```

这是 Xor 压缩 tweet 的招牌搭配——raymarch 累积进 `col`，最后一条 `tanh` 一把压回可显示范围。

## 相关

- [[xor-shader-artist]]
- [[glsl-mix-function]]
- [[density-field-volumetric]]
- [[shader-code-golfing]]
- [[separable-gaussian-blur]]

## Sources

- [[sources/xor-functions-tanh]]
- [[sources/xor-decoding-phosphor]]
