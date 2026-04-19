---
tags: [source, 渲染, shader, raymarching, 体积渲染]
date: 2026-04-19
sources: 1
---

# Volumetric Raymarching（Xor）

[[xor-shader-artist|Xor]] 2025 年 8 月的 mini tutorial，从 SDF raymarch 过渡到**密度场**（density field）驱动的体积渲染——云、烟、火、光柱。

## 摘要

SDF raymarch 用「距最近表面距离」做步长；volumetric raymarch 则换成「局部密度」——高密度区走小步采样多、低密度区大步快进。Xor 给出两类样本累积方式：**additive（发光）**——每步 `col += LIGHT_COLOR / vol` 自然产生距离衰减，最后 `tanh(K*col)` tonemap；**alpha blend（半透明介质）**——`color = mix(color, sample, (1-color.a)*sample.a)`，阈值 `color.a > 0.998` 提前退出。关键坑：密度函数可能产生 0（让步长归零死循环），解法是给密度公式加 **passthrough 项**（`+0.1`）或用 `abs(d)` 制造空心 SDF 让 ray 穿透。举例用的 density field 是 `3.5 - 0.25*|p.xy| + 0.5*dot(sin(p), cos(p*0.618).yzx)`——圆柱 + 廉价 [[dot-gyroid-noise|aperiodic gyroid noise]]。还有更花哨的八面体 density field 演示。文章后半段（更高级 demo、光线散射）留给付费订阅。

## 关键要点

- **SDF → density field**：距离换密度，步长按密度缩放。
- **Additive 累积**：`col += color / d`、最后 tanh tonemap。
- **Alpha blend**：从前往后 `mix`，阈值早退出。
- **防死循环**：密度加 passthrough 或 `abs` 空心化。
- **密度步长故意缩小**（比如 × 0.05）应对 SDF 被 warp 后的估计失真。

## 链接到的概念

- [[density-field-volumetric]]
- [[volumetric-raymarching-intro]]
- [[dot-gyroid-noise]]
- [[hyperbolic-tangent-shader]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/volumetric
- 本地：`raw/articles/mini.gmshaders.com/2025-08-23_volumetric-raymarching.md`
