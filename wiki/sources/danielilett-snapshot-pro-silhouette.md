---
tags: [source, 渲染, unity, urp, 后处理, silhouette, depth]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Silhouette（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Silhouette 深度剪影后处理的三个参数。

## 摘要

Silhouette 把场景按到相机的距离染成两色：近处是 `Near Color`、远处是 `Far Color`，中间用线性深度做 lerp。底层数学和 [[depth-texture-silhouette|image effects 版 Silhouette 教程]] 完全一致——读 [[depth-texture-silhouette|`_CameraDepthTexture`]]、`Linear01Depth` 归一化、再 `lerp(near, far, depth)`——Pro 版只是把它做成一个可在 Volume 里混合的 override。参数极简：`Enabled`（开关）、`Near Color`、`Far Color`，连教程里 `pow(depth, 0.75)` 的 remap 都不暴露。适合做受击 X 光、气氛切镜、Mario Odyssey 式剪影远景等视觉。

## 关键要点

- 只有三个参数，**不暴露深度 remap**——想要非线性分布只能 hack
- 背后用的是 Unity 的 Camera Depth Texture（URP 需要管线 asset 勾选）
- 后处理阶段的深度不包含半透明——符合 [[depth-texture-silhouette|image effect 深度缺失]]的行为
- `Near/Far Color` 是普通 Color（非 HDR），想做发光剪影要接 [[bloom-threshold-blur-composite|Bloom]]
- 典型用法：X 光切换、隐身相机、关卡过渡、受击闪切

## 链接到的概念

- [[depth-texture-silhouette]]
- [[z-buffer]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/silhouette/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-silhouette.md`
