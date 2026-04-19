---
tags: [source, 渲染, unity, urp, 后处理, world-space, grid, synthwave]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Synthwave（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Synthwave 世界空间网格后处理的九个参数。

## 摘要

Synthwave 把每个屏幕像素**反推到世界空间坐标**，判断它是否落在三组正交平面（沿 X / Y / Z 轴）附近，落在线上画线色、落在外画背景色或保留原场景色——最终得到一张可以穿透物体、随相机运动保持透视正确的"无限数字网格"。概念细节见 [[synthwave-grid-postfx]]。Pro 版暴露完整的参数：`Background Color`、`Line Colors 1 & 2`（HDR 渐变顶底两色）、`Line Color Mix`（渐变混合比）、`Line Width`（硬边半宽）、`Line Falloff`（软边过渡距离）、`Gap Width`（各轴线间距）、`Offset`（全局平移）、`Axis Mask`（三个轴开关）、`Use Scene Color`（背景是纯色还是叠在原画面上）。典型搭配：HDR 线色 + [[bloom-threshold-blur-composite|Bloom]] 得到霓虹灯视觉。

## 关键要点

- 线色是 **HDR 色**——暗示期望下游接 Bloom
- Axis Mask 关掉某轴就省一组平面的判定，纯 XZ 地板格关 Y 最常见
- `Use Scene Color` 决定"虚空数字场景" vs "现实 + 叠加格子" 两种视觉分支
- 反投影需要 [[depth-texture-silhouette|`_CameraDepthTexture`]]——URP 下必须显式勾选 Depth Texture
- 世界空间判定使得网格随相机运动透视正确——区别于 UV-space grid 和 triplanar grid
- 典型用法：synthwave 美术风、vaporwave、关卡加载前的"matrix 状态"、debug 世界刻度可视化

## 链接到的概念

- [[synthwave-grid-postfx]]
- [[depth-texture-silhouette]]
- [[coordinate-spaces]]
- [[bloom-threshold-blur-composite]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/synthwave/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-synthwave.md`
