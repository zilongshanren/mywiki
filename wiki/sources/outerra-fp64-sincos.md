---
tags: [source, graphics, glsl, fp64, minimax, remez, 数学库]
date: 2026-04-19
sources: 1
---

# fp64 approximations for sin/cos for OpenGL（Outerra Blog）

[[outerra-team]] 2017 年 6 月的一篇代码贴文，补齐 GLSL 在 `double` 支持后仍**缺失的 fp64 `sin`/`cos`**。给出两组用 [Remez exchange](http://lolengine.net/wiki/doc/maths/remez) 生成的 minimax 多项式系数与完整 range reduction 代码。

## 摘要

在 $[0, \pi/2]$ 上用奇次多项式（$t + a_3 t^3 + a_5 t^5 + \ldots$）逼近 `sin`，再用 $\text{floor}(|x|\cdot 2/\pi)$ 做象限判定、奇象限做 $1-y+q$ 反向折叠、最后根据象限位 2 和输入符号翻号。所有多项式求值通过嵌套 `fma` 实现。9 阶版 < 5e-9 绝对误差（地球半径上约 3cm 位移），11 阶版 < 2e-11（约 0.13mm）。`cos` 通过 `sin(x + π/2)` 直接派生。文章最后指向作者 2014 年另一篇 *Double precision approximations for map projections in OpenGL*，两篇共同构成 Outerra 的行星坐标 fp64 管线。

## 关键要点

- **GLSL 不提供 fp64 超越函数**——任何 planet 引擎自行补齐是行业常态。
- **Remez Minimax 优于 Taylor**：同阶精度高数量级，与 [[faster-math-functions]] 一致。
- **FMA-only 多项式评估**：整条链用 `fma`，一次舍入，GPU 指令级最优。
- **Range reduction 用 $1 - y + q$ 折叠**：避免大数 `x mod 2π` 的灾难性相减。
- **精度可换阶**：9 阶 cm 级、11 阶 sub-mm 级。

## 链接到的概念

- [[fp64-sincos-minimax]]
- [[faster-math-functions]]
- [[robin-green]]
- [[planet-terrain-dem-pipeline]]

## 原文

- 链接：https://outerra.blogspot.com/2017/06/fp64-approximations-for-sincos-for.html
- 本地：`raw/articles/outerra.blogspot.com/2017-06-13_fp64-approximations-for-sin-cos-for-opengl.md`
