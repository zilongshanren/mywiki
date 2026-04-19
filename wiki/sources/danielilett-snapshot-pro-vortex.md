---
tags: [source, 渲染, unity, urp, 后处理, uv-distortion]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Vortex（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Vortex 漩涡扭曲后处理的三个参数。

## 摘要

Vortex 是围绕一个中心点做旋转式 UV 扭曲的后处理，视觉上把屏幕图像"卷入"中心。参数极简：`Strength`（卷曲强度，越高越剧烈）、`Center`（UV 空间的旋转中心，默认 `(0.5, 0.5)` 即屏幕中心）、`Offset`（在旋转之前给 UV 预加的偏移，可实现偏心漩涡或漩涡中心动态位移）。与 [[vortex-distortion]] 概念页讨论的一样，底层是极坐标空间下把 `theta` 按半径函数偏移——Pro 版把这个公式封装成了一个 Volume override，暴露最少的参数给用户。

## 关键要点

- `Strength` 控制极坐标下 `theta += strength * f(r)` 的乘数——`f(r)` 具体形式由 Pro 内部决定（未公开）
- `Center` 用 UV 空间坐标（0-1），不是屏幕像素坐标；默认 `(0.5, 0.5)` 中心对称
- `Offset` 在旋转前预位移 UV，等于把旋转中心在坐标系中前后平移——可以实现"漩涡中心本身在动"的效果
- 典型用法：传送门开启、受击镜头、boss 召唤、场景切换过渡
- 配合 HDR color separation 或 [[chromatic-aberration-post]] 能让漩涡视觉更强烈

## 链接到的概念

- [[vortex-distortion]]
- [[urp-volume-post-processing]]
- [[underwater-post-effect]]
- [[chromatic-aberration-post]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/vortex/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-vortex.md`
