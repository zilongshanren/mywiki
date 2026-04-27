---
tags: [渲染, 球谐, 光线追踪, 科学可视化, 多项式求根]
date: 2026-04-27
sources: 1
---

# 球谐字形的光线追踪（SH Glyphs Ray Tracing）

球谐字形（SH glyph）是医学和神经科学可视化中常用的图元——将单位球表面各点按某个球谐展开的函数值**径向拉伸**，得到一个能直观展示方向分布函数（ODF）的三维形状。Christoph Peters 等人在 VMV 2023 上提出了一种高效的**光线追踪**渲染方法。

## 问题的代数结构

设光线 $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$，字形表面由函数 $f(\hat{\omega}) = \sum_{\ell,m} c_{\ell}^{m} Y_{\ell}^{m}(\hat{\omega})$ 定义（只含偶次带 $\ell = 0, 2, \ldots, k$）。光线-字形求交的条件是：

$$\|\mathbf{r}(t)\| = f\!\left(\frac{\mathbf{r}(t)}{\|\mathbf{r}(t)\|}\right)$$

对两边平方并展开，可以化归为一个关于 $t$ 的**多项式方程**，阶数为 $2k+2$。例如：
- 只用 L0–L2（$k=2$）：4 次多项式
- 用到 L4（$k=4$）：6 次多项式

## 关键设计

**完整根查找**：使用数值稳定的多项式求根算法找出全部实根，而非仅求最近交点。这使得凹陷字形、自遮挡、以及透明/不确定性效果都能正确处理。

**法向量公式**：字形表面法向量可由隐函数定理直接导出解析表达式，无需数值差分，精度和效率均优于之前方法。

**紧密 AABB**：论文还推导了字形的近似严格包围盒，减少了光线遍历阶段的无效求交。

## 与图形渲染的联系

虽然 SH glyph 的主要应用场景在科学可视化（diffusion MRI、HARDI），但文章的核心技术——**将球面函数求交化归为多项式求根**——与 [[polynomial-root-finding-gpu]] 一脉相承。Peters 此前研究 GPU 上的高次多项式求根，本文是同一代数工具链在另一个渲染问题上的自然应用。

## 相关

- [[spherical-harmonics]] — SH 理论基础
- [[polynomial-root-finding-gpu]] — GPU 上的多项式求根
- [[sh-glyphs-ray-tracing]] — 本页自身
- [[christoph-peters]]

## Sources

- [[sources/peters-rt-sh-glyphs]]
