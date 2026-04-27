---
tags: [source, 渲染, frame-analysis, lod, reflections, adriancourreges]
date: 2026-04-27
sources: 1
---

# GTA V – Graphics Study Part 2（Adrian Courrèges）

[[people/adrian-courreges]] 发表于 2015 年 11 月的帧分析续篇，专注于《GTA V》的 LOD 系统与水面/镜面反射实现细节。

## 摘要

本文从两个角度深入分析 GTA V 的技术实现。LOD 部分：远处路灯全部以真实四边形（32×32 纹理）表示，重度批次化实例化；Vinewood Hills 整片区域仅 2500 三角形单 draw call 渲染；资产以流式加载实时进出内存，飞机速度被故意降低以配合流式系统带宽限制。反射部分：水面结合平面反射图（240×120 upside-down 场景）、折射图（含焦散和水深蓝移）和法线扰动（bump map）通过 Fresnel 方程混合；海洋网格顶点每帧更新模拟波浪；镜面与水面技术完全相同，仅省去折射；夜景中每盏路灯独立渲染贡献 GI——每个光源通过变形后的八面体网格触达受影响像素，在 [[deferred-rendering]] 管线中精确控制着色范围，避免对无关像素执行像素着色器。

## 关键要点

- LOD 极限：整座山丘（数平方公里）压缩为 2500 三角形单 draw call，3D 美术手动精调
- 流式加载约束：飞机速度被人为削减，以确保流式系统有足够带宽预加载前方资产
- 水面折射：先生成水深 opacity map（深水更蓝更不透明），再加焦散，最后与平面反射按 Fresnel 混合
- 延迟管线的光源优势：八面体形状 mesh 驱动像素着色器，只对真正受光像素执行计算
- 镜面实现：与水面同路径，距离过远/超出视口时 fallback 为黑色四边形，避免无效 pass

## 链接到的概念

- [[deferred-rendering]]
- [[fizzle-lod-fading]]
- [[reprojected-planar-reflection]]

## 原文

- 链接：http://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study-part-2/
- 本地：`raw/articles/adriancourreges.com/2015-11-02_gta-v-graphics-study-part-2-adrian-courreges.md`
