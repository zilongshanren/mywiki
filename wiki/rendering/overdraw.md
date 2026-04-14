---
tags: [渲染, 性能]
date: 2026-04-05
sources: 2
---

# Overdraw（过度绘制）

**同一个像素被多次 fragment shader 执行**——直接的带宽和 ALU 浪费。

## 来源

- 多个不透明三角形重叠（没有合理剔除）。
- 多个半透明物体叠加。
- 全屏覆盖的后处理 pass（技术上不叫 overdraw，但效果类似）。

## 度量

- **Overdraw = 总 fragment 处理次数 / 屏幕像素数**。
- 典型桌面场景：3-10×。
- 病态场景（alpha particles）可以到 100+。

## 降低 overdraw 的手段

- **从前往后**排序渲染不透明物体。
- **Depth Pre-Pass**：先只写 depth，后续 fragment shader 因 [[early-z-late-z|Early-Z]] 大量剔除。
- **避免 alpha test / discard**——破坏 [[hsr-tbdr|HSR]]。
- **Occlusion Culling**：CPU 端不发可被遮挡的 DrawCall。
- **移动端**：避免全屏 post-processing 链过长。

## TBDR 的特殊对待

TBDR 架构的 HSR 可在 tile 粒度上**完全消除 overdraw**——若不被 `discard` 破坏。详见 [[hsr-tbdr]]。

## 相关

- [[hsr-tbdr]]
- [[early-z-late-z]]
- [[fragment-shader]]
- [[culling]]
- [[compute-vs-raster-points]] —— 高密度点云用 compute shader 比硬件光栅化更快

## Sources

- [[sources/rtr-day05]]
- [[sources/rtr-day06]]
