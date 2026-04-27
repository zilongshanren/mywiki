---
tags: [source, math, approximation, instruction-level-parallelism, cpp]
date: 2026-04-27
sources: 1
---

# Gotta Go Fast（16BPP.net）

[[people/16bpp]] 发表于 2026 年 3 月的文章，是 [[asin-cg-approximation]] 系列的直接续篇——把 Horner 求值写法改写为 [[estrin-scheme]]，在 Intel 平台再榨出 +17–20% 性能。

## 摘要

上一篇文章发现了 Nvidia Cg 的 Minimax `asin()` 近似；这篇发现该实现的 Horner 多项式展开可以用 Estrin's Scheme 重写，从而缩短依赖链长度。具体操作：把 `p = ((a3*x+a2)*x+a1)*x+a0`（依赖链长度 3）改写为 `p = (a3*x+a2)*x² + (a1*x+a0)`（依赖链长度 2），CPU 可以并行计算两个括号里的 FMA。作者在 Intel i7-10750H、AMD Ryzen 9 6900HX、Apple M4 三种硬件，Ubuntu/Windows 两个 OS，GCC/Clang/MSVC 三种编译器下做了 250 次 × 1000 万次调用的矩阵测评：Intel 端 +17–25%，AMD 端几乎无差（Ryzen OoO 窗口已能隐藏 Horner 的串行），M4 Clang +11%。在端到端 PSRayTracing 1920×1080 渲染中，Intel 上多得 +3%，M4 上差异被噪声淹没。结论：收益与 CPU 的乱序执行窗口负相关；AMD/Arm 不必改，Intel 老芯片改一行值得。

## 关键要点

- 将 Horner 3 阶多项式改为 Estrin 形式只需两行代码改写
- Intel 微基准测试 +17–25%，端到端渲染 +3%（asin 只占渲染时间的一小部分）
- AMD Ryzen 几乎无额外收益——说明 Estrin 的价值与目标 CPU 的 OoO 能力直接挂钩
- LUT 方案被尝试后放弃：误差更大且不比公式快
- 关键方法论：microbench + 端到端 double-check，小差异（<2 秒）视为噪声

## 链接到的概念

- [[estrin-scheme]]
- [[asin-cg-approximation]]
- [[faster-math-functions]]
- [[psraytracing]]

## 原文

- 链接：https://16bpp.net/blog/post/even-faster-asin-was-staring-right-at-me
- 本地：`raw/articles/16bpp.net/2026-03-16_gotta-go-fast.md`
