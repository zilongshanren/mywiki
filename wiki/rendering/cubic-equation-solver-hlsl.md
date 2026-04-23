---
tags: [渲染, 数学, GPU, HLSL, 数值方法]
date: 2026-04-14
sources: 1
---

# 三次方程的 HLSL 快速求解（三实根情形）

**Christoph Peters** 在 2016 年 9 月放出的一段 ~30 行 HLSL 代码，是「在 fragment shader 里稳定求解一元三次方程」这一基础任务上目前已知最快的方案之一。它假定方程**有三个实根**——这正是 [[moment-shadow-mapping|矩阴影贴图]] 与「六阶矩 prefiltered single scattering」在重建阶段所需的精确条件——并以一次 `atan2 / sincos` 的代价同时返回三个根。代码基于 Jim Blinn 在 *IEEE CG&A* 上那篇五部分专栏 "How to solve a cubic equation"，但**牺牲了一点稳健性来换取约 2× 的速度**。

## 为什么 Blinn 的写法在今天反而慢

Blinn 的目标是数值稳定性。他的策略是分别求最大模根和最小模根：通过代换 \(y := x^{-1}\) 把多项式翻转，让两条分支都只需要算「最大模那一支」，避开除以小数。第三个根可以由 Vieta 关系廉价补出。这个设计在那个 SIMD 指令能让两条分支并行的年代是合理的——并行计算让"重复 2×"变成几乎免费。

但今天的 GPU 不再有这种结构上的 SIMD 红利：fragment shader 里的两条逻辑分支不会被自动并行，反而会真的把工作量翻倍。Peters 的做法是**直接一次算出三个根**，丢掉那一半分支，换来翻倍的速度。

## 代码结构

算法骨架（对应 `Coefficient[0..3]` 是从常数项到三次项的系数）：

1. **归一化**：除以三次项系数；
2. **「除以 3」trick**：把一次和二次项系数除以 3，使后续 Hessian / discriminant 表达式形式更整齐；
3. **凑出 depressed cubic**：把方程化为 \(t^3 + pt + q = 0\) 的形式；
4. **复平面里取立方根**：用 `atan2(sqrt(D), -q)/3` 求出辐角，再用 `sincos` 一次拿到 cos/sin；
5. **三个根**就是把这一个复立方根分别旋转 0°、120°、240°，然后逆 depression 平移加回 \(-c_2\)。

整段代码没有循环、没有分支、没有查表，完全是 mad/dot 表达式构成的「单次直通」shader，编译器可以充分流水化。

## 它的来历：六矩 prefiltered single scattering

这段代码不是为了好玩而写的——Peters 当时在做 [[christoph-peters|moment shadow mapping]] 的「六阶矩 prefiltered single scattering」分支（[[volumetric-fog-froxels|参与介质]]里的体积阴影），原始实现用 Wikipedia 上的标准闭式公式，但是当三次项系数趋零时会在某些像素返回错误结果。一种廉价的修复方法是事后跑一次 Newton 迭代，但这又把成本顶起来了。Peters 花了几天读完 Blinn 的五部分专栏，最后总结出一个「比闭式更稳、比 Newton 更快」的折中方案——即上述代码。

## 适用边界

- **三实根**是硬约束。如果传入只有一个实根的方程，行为未定义。Blinn 的专栏给出了那种情况的对应公式；如果一段着色器需要同时处理两类，可以用 discriminant 做分支。
- **数值稳定性**比 Blinn 的双分支版本略弱，但据 Peters 实验，在他试过的所有近似方案（其它闭式、各种迭代、混合方案）里依然是**最稳的那一个**。
- 不依赖任何特殊扩展，原生 SM 5.0 HLSL 即可，移植到 GLSL 也只是改一下函数名。

## 与 GPU 求根工具箱的关系

它和 [[polynomial-root-finding-gpu|高阶多项式 bracketed Newton bisection]] 处在工具箱的两端：

- 三次方程：直接闭式、O(1) 表达式、零分支；
- 度 ≥ 5：必须迭代，要操心区间维护、寄存器溢出、稳定性；
- 度 4：通常先解 resolvent cubic（用本页这段代码），再二次公式。

也就是说，Peters 的"三次快算"在他自己的工具栈里既是终点（六矩 single scattering 直接就用），也是上层算法的子例程（对四矩 MSM 的解码、对 Hausdorff 矩闭式解）。

## 相关

- [[moment-shadow-mapping]] — 解码阶段需要的核心数学
- [[polynomial-root-finding-gpu]] — 度 ≥ 5 的对照方案
- [[christoph-peters]]

## Sources
- [[sources/peters-cubic-equation-revisited]]
- [[sources/supnik-joys-of-bezier-curves]]
