---
tags: [source, 渲染, shader, GLSL, 导数, 浮点精度]
date: 2026-04-19
sources: 1
---

# Derivatives III: I Ran Out of Rez（Ben Supnik / hacksoflife）

[[ben-supnik|Supnik]] 2011-01-20 的 Derivatives 连载第三篇，承接 [[sources/supnik-derivatives-two-parts]]（Part I/II）与 [[sources/supnik-running-out-of-derivative-res]]（2010 原始观察），把**「GLSL 内建导数本身会因浮点精度不足而崩」**这个情况讲得更系统。

## 摘要

内建 `dFdx/dFdy` 本质上是对 **相邻两像素**的 UV（或其他插值量）做实际差分。这意味着导数的精度上限 = 两像素间 UV 差值的浮点可表示精度，**远低于 UV 自身的精度**。举例：把一张 1024×1024 纹理铺到 5 km 游戏距离、再把 5 m 范围放大占满 1024 宽屏幕——选 texel 本身要 10 bit、在 1024 像素上插值又要 10 bit，UV 已消耗掉 20 bit，剩下只有约 3 bit 给「相邻像素间的差值」。差值低到某个阈值，**相邻像素的 UV 变成相同值，导数恒为 0**（或大幅抖动），用这个烂导数去重建切线基底（per-pixel normal mapping 依赖 `dFdx(uv)` 反推 TBN——见 [[tangent-free-normal-mapping]]）则是灾难。

texture 采样本身不怎么怕这种精度耗尽（相邻像素采同一 texel 只是填同一个颜色，视觉 256 级灰度看不出），**但导数会把它放大成几何与光照异常**。Supnik 给的唯一可行解：既然这种极端 UV 通常是在 vertex shader 里**按公式生成**的（比如从世界坐标直接投影），那就**用对应的解析公式算出 `dFdx/dFdy`**，彻底绕开内建差分。这正是「投影参数已知就别用差分反推」的再次应用（与 [[uv-precision-derivative-loss]] 的第二条出路一脉相承）。

## 关键要点

- **内建导数的精度 ≠ UV 的精度**：前者是两像素差值的精度，是后者余下的低位——UV 越大、精度越稀。
- **10 bit texel + 10 bit 插值 = 20 bit**，在 fp32 仅剩 ~3 bit 给差分——屏幕稍放大就爆。
- 用坏导数做**切线基底重建**（per-pixel normal mapping 无预存 TBN）会 total train wreck。
- 解法：**算法式导数替换内建导数**——UV 由公式生成时，对应公式可直接求导。
- 对 texture 采样本身来说，这个精度问题几乎无影响（perceptual 灰度掩盖）。
- 与 Part I/II 的根本区别：Part I/II 讲**差分不适用的控制流场景**，Part III 讲**差分可用但浮点输光了**。

## 链接到的概念

- [[uv-precision-derivative-loss]]
- [[texture2dgrad-explicit-derivatives]]
- [[huge-world-coordinate-precision]]
- [[tangent-free-normal-mapping]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/01/derivatives-iii-i-ran-out-of-rez.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-01-20_derivatives-iii-i-ran-out-of-rez.md`
