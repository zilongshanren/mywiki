---
tags: [source, 渲染, frame-analysis, terrain, rts, adriancourreges]
date: 2026-04-27
sources: 1
---

# Supreme Commander – Graphics Study（Adrian Courrèges）

[[people/adrian-courreges]] 发表于 2015 年 6 月的帧分析文章，使用 PIX（RenderDoc 不支持 DX9）逐 pass 解析《Supreme Commander》（2007，Gas Powered Games，Moho 引擎）的渲染管线。

## 摘要

文章以地形系统为切入点：SupCom 先从 513×513 heightmap 生成地形网格，再通过 **Texture Splatting** 叠加多层 stratum（每层含 albedo + normal + splat mask），4 张 splat map 压缩进单张 RGBA 纹理。细节由 861 个 decal 实例补充。帧渲染流程：视锥剔除提取地形子网格；法线 pass 融合所有 stratum 法线（XY 两通道压缩）；LiSPSM 阴影，并尝试了 Variance Shadow Map（部分实现）进行模糊处理；带光照和阴影的地形渲染；水面反射图（场景垂直翻转渲染）；所有单位渲染（植被使用几何实例化）；粒子和血条；bloom（从 alpha 通道提取发光信息，LDR 工作流）；单 draw call 渲染整个 UI（1024×1024 纹理 atlas，动态重打包）。

## 关键要点

- [[terrain-splatmap-shader-graph]]：多层 stratum splat map 打包进 RGBA 通道，单 pass 融合
- 法线切线空间 XY 压缩：Z = sqrt(1 - X² - Y²)，存 RG 两通道即可重建完整法线
- LiSPSM 阴影 + 半 VSM：借助视角透视变换最大化阴影精度；高斯模糊 shadow map 但未完整实现 depth²
- 反射图：垂直轴缩放 -1 翻转场景，产生水面倒影
- 几何实例化用于大量相同植被树木，单 draw call 渲染数千棵
- UI 单 draw call：运行时打包 1024×1024 sprite atlas，切换选择单位时重新生成

## 链接到的概念

- [[terrain-splatmap-shader-graph]]
- [[shadow-mapping-basics]]
- [[deferred-rendering]]

## 原文

- 链接：http://www.adriancourreges.com/blog/2015/06/23/supreme-commander-graphics-study/
- 本地：`raw/articles/adriancourreges.com/2015-06-23_supreme-commander-graphics-study-adrian-courreges.md`
