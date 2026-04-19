---
tags: [source, 渲染, shader, glsl, tanh]
date: 2026-04-19
sources: 1
---

# Functions: Tanh（Xor）

[[xor-shader-artist|Xor]] 2025 年 5 月「Functions」系列的第一篇，重启 Mini tutorial 日更。介绍双曲正切 `tanh` 作为 shader 工具函数的数学背景和 4 类用法。

## 摘要

`tanh(x)` 把 $(-\infty, +\infty)$ 光滑映射到 $(-1, +1)$，可以看作"无定边的 smoothstep"。Xor 列了四类用法：(1) **平滑 blend**：`mix(col_a, col_b, tanh(x*SPREAD)*0.5 + 0.5)`；(2) **tone mapping**：tweet shader 几乎每个都用它压 HDR 输出，"不是最好但极方便"；(3) **调试可视化**：任何可能越界的量 `tanh` 一下就能看大小趋势；(4) **神经网络激活**：GAN 用 tanh 把权重压到 $[-1, +1]$。数学背景给了三种视角：sigmoid、单位双曲线上的 x/y 比（类比于单位圆上的 tan）、指数形式 `tanh(x) = (e^x - e^{-x})/(e^x + e^{-x}) = -1 + 2/(1 + e^{-2x})`。后者给出 GLSL ES 1.00 / WebGL 1.0 手写实现（GLSL 1.30+ 已有 `tanh` 内建）。文章后半段（替代函数、性能对比）留给付费订阅。

## 关键要点

- $\tanh: (-\infty, \infty) \to (-1, +1)$ **平滑的 sigmoid**，用于 tonemap / blend / 调试。
- 手写版：`-1.0 + 2.0 / (1.0 + exp(-2.0*x))`——一次 exp。
- "不是最好的 tonemap，但够用又便宜"——实用主义哲学。
- 把不确定范围的变量 `tanh` 一下再可视化——debug 神器。

## 链接到的概念

- [[hyperbolic-tangent-shader]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/func-tanh
- 本地：`raw/articles/mini.gmshaders.com/2025-05-31_functions-tanh.md`
