---
tags: [source, 渲染, 法线贴图, derivative-map]
date: 2026-04-27
sources: 1
---

# Derivative Maps（Rory Driscoll / CodeItNow）

[[people/rory-driscoll]] 发表于 2012 年 1 月的文章，介绍基于 Morten Mikkelsen 论文的 derivative map 技术原理与实现，并比较两种实现方案的视觉质量。

## 摘要

文章从高度场梯度和表面梯度的概念出发，推导了将二维高度场梯度投影到三维曲面上扰动法线的公式。不同于 normal map，derivative map 无需预计算切线向量，只依赖屏幕空间的 `ddx`/`ddy` 指令或预计算的 UV 空间导数贴图。文章分两种方案实现：方案一直接用 `ddx`/`ddy` 取高度偏导，成本低但因双线性滤波造成块状感；方案二预先存储 UV 空间的高度导数，运行时用链式法则转换到屏幕空间，视觉质量大幅提升，接近 normal map 的效果。文章也指出 derivative map 在内存（省去切线向量）和混合便利性上的优势，但最终质量和性能的系统对比留到后续文章。

## 关键要点

- 核心公式：$\mathbf{n}' = \mathbf{n} - \nabla_s\beta$，表面梯度用 $\mathbf{p}$ 的偏导和高度偏导共同计算
- `ddx`/`ddy` 方案：最简单但近距离出现块状（双线性滤波导致梯度恒定）
- 预计算方案（PD map）：导数可正确插值，质量与 normal map 相当
- 链式法则：$\partial h/\partial x = (\partial h/\partial u)(\partial u/\partial x) + (\partial h/\partial v)(\partial v/\partial x)$
- 优势：不需切线向量、混合直接相加；劣势：多约 5 条 ALU 指令

## 链接到的概念

- [[rendering/derivative-map]]
- [[rendering/tangent-space-normal-mapping]]
- [[rendering/tangent-free-normal-mapping]]
- [[rendering/mipmap-generation-sampling]]

## 原文

- 链接：https://www.rorydriscoll.com/2012/01/11/derivative-maps/
- 本地：`raw/articles/rorydriscoll.com/2012-01-11_derivative-maps.md`
