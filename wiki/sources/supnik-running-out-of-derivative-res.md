---
tags: [source, 渲染, shader, 浮点精度, normal-mapping]
date: 2026-04-19
sources: 1
---

# Running Out of Derivative Res（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 2 月的短文，描述 X-Plane 地形上 GF 8800 特有的 per-pixel tangent space 噪声。

## 摘要

X-Plane 地形 tile 尺寸 300 × 300 km，vertex shader 从世界空间位置投影出 UV。per-pixel normal-map 用 `dFdx(UV)` / `dFdy(UV)` 反推 tangent 基底（见 [[tangent-free-normal-mapping]]），避免顶点上编码 tangent。问题在于：在 NVIDIA 8800 上，UV 被投影到足够大的数值后，**插值出的 UV 每像素差值低于 fp32 的稳定精度**，差分结果退化为噪声，tangent 基底整张图逐像素抖动，法线贴图在屏幕上表现成 per-pixel 高频噪点。ATI 4870 没有复现，应该是两家在内部 interpolator/差分器精度上的差异。Supnik 给出两条 work-around：提高 UV 生成的精度，或者干脆在投影已知的场合直接传投影轴作为 tangent 基底，绕开差分。

## 关键要点

- 300 km 级 mesh + vertex-shader-projected UV ⇒ UV 数值大，per-pixel 差值被精度吞掉。
- 坏导数让 tangent 基底逐像素噪声 ⇒ 法线采样方向噪声 ⇒ 屏幕高频噪点。
- 同样的代码在 HD 4870 上不出错，驱动/硬件精度差异会掩盖问题但不是根治。
- 对策 1：把 UV 生成改成不丢精度的形式。
- 对策 2：投影已知时直接把投影轴当 tangent 基底，不用差分。
- 这是和「不连续 UV」并列的另一类导数失效。

## 链接到的概念

- [[uv-precision-derivative-loss]]
- [[tangent-free-normal-mapping]]
- [[texture2dgrad-explicit-derivatives]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/02/running-out-of-derivative-res.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-10_running-out-of-derivative-res.md`
