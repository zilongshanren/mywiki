---
tags: [source, 渲染, 数学, HLSL, GPU, 数值方法]
date: 2026-04-14
sources: 1
---

# How to Solve a Cubic Equation, Revisited（Peters，2016-09-10）

[[christoph-peters]] 2016 年 9 月发布的一篇短文，给出一段 ~30 行 HLSL 代码，是「在 fragment shader 里求解三个实根的一元三次方程」目前已知最快的方案之一。基于 Jim Blinn 的 *IEEE CG&A* 五部分专栏 "How to solve a cubic equation"，但**牺牲了一些数值稳健性，换来约 2× 的性能**。

## 摘要

文章以一段可直接复用的 HLSL `SolveCubic` 函数为主体，外加一段非正式说明。代码假定调用方已知方程**有三个实根**——这正是 [[moment-shadow-mapping|MSM]] 的"六阶矩 prefiltered single scattering"分支在重建步骤所需的精确条件。算法骨架是：先归一化、把中间系数除以 3、构造 Hessian 与判别式、化为 depressed cubic、然后用一次 `atan2 + sincos` 在复平面里取一个立方根，最后把这个复立方根分别旋转 0°、120°、240° 即得三个实根。

Peters 强调两点：第一，**Blinn 的"双分支求最大模根"策略**在今天的 GPU 上反而慢，因为 fragment shader 不再像旧 SIMD 时代那样把两条分支并行执行；他的版本直接一次算完三个根，把成本砍掉一半。第二，这段代码替换掉了"六矩 single scattering"原本用 Wikipedia 闭式公式 + 可选 Newton 修正的方案——既修复了三次系数趋零时的破图像素，又**又快又稳**。

## 关键要点

- **三实根专用**——是硬约束；只有一个实根时行为未定义，需要走 Blinn 的另一支公式。
- **零分支、零循环、零查表**——纯 mad/dot/sin/cos/atan2，编译器友好。
- **来源动机**：解决六阶矩 prefiltered single scattering 的破图，不是为了"做数学"。
- **比 Newton 后处理便宜**——Newton 修正会把成本顶上去；闭式 + 重新设计直接消灭根因。
- **Blinn 设计哲学的过期**：那种"用并行 SIMD 让重复变免费"的论证在现代 GPU 不再成立。

## 链接到的概念

- [[cubic-equation-solver-hlsl]]
- [[moment-shadow-mapping]]
- [[polynomial-root-finding-gpu]]
- [[christoph-peters]]

## 原文

- 链接：<http://momentsingraphics.de/CubicRoots.html>
- 本地：`raw/articles/momentsingraphics.de/2016-09-10_how-to-solve-a-cubic-equation-revisited.md`
