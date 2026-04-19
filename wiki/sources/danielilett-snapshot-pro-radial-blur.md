---
tags: [source, 渲染, unity, urp, 后处理, blur, radial-blur]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Radial Blur（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Radial Blur 径向模糊后处理的两个参数。

## 摘要

Radial Blur 是 [[radial-blur-postfx|空间变化强度]]的高斯模糊：屏幕中心保留原样、越往边缘越糊。参数两个：`Strength` 控制 kernel 尺寸（每帧像素操作数随之增加），`Luminance Threshold`（命名稍误导，其实是**径向距离阈值**）设定保持锐利的中心区域比例。权重公式近似 `weight = saturate((r - threshold) / (1 - threshold))`，再按 weight lerp 到原图。产品面板锁死了方向/步长/kernel 形状，想做真正的 zoom blur（沿 `uv→center` 矢量方向加速）需要换 override。

## 关键要点

- 参数：`Strength`（kernel 大小）+ `Luminance Threshold`（中心清晰范围）
- 不是 zoom blur，是 kernel 半径随 `length(uv-0.5)` 线性拉伸的 gaussian
- 严格意义上 kernel 随像素变化会破坏 [[convolution-separability-blur|可分离性]]，实践上仍两 pass 近似
- 典型用途：加速 / 受击眩晕 / 焦点引导 / 隧道视觉
- 命名坑：`Luminance Threshold` 其实和亮度无关，是径向距离——产品文档本身写法易误导

## 链接到的概念

- [[radial-blur-postfx]]
- [[separable-gaussian-blur]]
- [[dual-kawase-blur]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/radial-blur/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-radial-blur.md`
