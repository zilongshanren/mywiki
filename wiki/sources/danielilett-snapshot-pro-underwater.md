---
tags: [source, 渲染, unity, urp, 后处理, underwater]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Underwater（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Underwater 后处理的四个参数。

## 摘要

*Snapshot Shaders Pro* 的 Underwater 是一个轻量版水下后处理：用一张 bump map 驱动屏幕 UV 波纹扭曲、叠加一层随深度渐浓的水色雾。参数只有 `Bump Map`（控制扭曲方向与强度的纹理，需要手动指定，仓库提供 `Resources/Textures/UnderwaterNormals.png` 示例）、`Strength`（扭曲强度）、`Water Color`（远裁剪平面处的水色）、`Fog Strength`（雾浓度与起雾距离）。页面提示把相机远裁剪平面调小，让整个场景落在水雾范围内，否则远处雾效不自然。相比后续 *Snapshot Shaders 2* 的 Underwater（见 [[sources/danielilett-snapshot2-underwater]]），Pro 版没有 caustics、flow map 滚动、triplanar 投影等高级项，只保留最基础的 bump 扭曲 + depth fog 两层。

## 关键要点

- Bump Map 必须设置，否则 effect 不工作——Pro 版没有默认 fallback 纹理
- 远裁剪平面决定水色的"最深处"——调小让场景全部落在水雾里
- `Fog Strength` 同时控制**起雾距离**和**浓度**（一个参数控两个维度，简化了用法但也少了灵活度）
- 相比 Snapshot 2 Underwater：Pro 是 *bump + fog*，Snapshot 2 是 *flow map + caustics + triplanar*——产品定位从"基础工具"向"功能完整"迭代

## 链接到的概念

- [[underwater-post-effect]]
- [[urp-volume-post-processing]]
- [[fog-shader]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/underwater/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-underwater.md`
