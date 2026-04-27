---
tags: [source, 渲染, frame-analysis, deferred-rendering, gbuffer, adriancourreges]
date: 2026-04-27
sources: 1
---

# GTA V – Graphics Study Part 1（Adrian Courrèges）

[[people/adrian-courreges]] 发表于 2015 年 11 月的帧分析文章，解剖《Grand Theft Auto V》PC 版（DX11，Rockstar Games）的完整延迟渲染管线。

## 摘要

GTA V 使用完整的 **延迟渲染**管线配合多张 HDR G-Buffer。流程如下：实时渲染环境 cubemap（6 面×128×128），随后转换为双抛物面反射图（dual-paraboloid map）以优化采样；compute shader 进行 LOD 和视锥剔除；G-Buffer 生成阶段输出 5 个渲染目标（漫反射、法线、高光、辐照度、深度/模板）共约 1900 次 draw call；CSM（4 级联阴影）另需约 1000 次 draw call；SSAO 在半分辨率下计算；G-Buffer 合并后对 Michael 皮肤执行 SSS；水面结合平面反射+折射+法线扰动；大气 light-shaft 和云天渲染；最后透明对象、LOD 抖动修复、tone mapping（Uncharted 2 filmic 算子）、bloom、FXAA、镜头畸变、色差、UI。全帧共 4155 次 draw call，113 张纹理，88 个渲染目标。

## 关键要点

- 对数 Z-buffer（反转 Z）大幅改善远距离 Z-fighting
- Alpha stippling：稀疏像素化（棋盘格丢弃 1/2 像素）实现不透明物体 LOD 渐变，后期单 pass 修复
- 双抛物面反射图相比 cubemap 减少 edge seam 且 mipmap 无缝
- G-Buffer 模板区分像素类型（玩家角色 0x89、载具 0x82、NPC 0x01 等），驱动 SSS 等针对性 pass
- Uncharted 2 filmic tonemapper：`(x(Ax+BC)+DE)/(x(Ax+B)+DF)-E/F`，GTA V 与 DOOM 2016 共用
- 动态曝光适应模拟人眼：由暗到亮比由亮到暗调整更快

## 链接到的概念

- [[deferred-rendering]]
- [[cascaded-shadow-maps]]
- [[alpha-stippling-lod-dithering]]
- [[screenspace-reflections]]

## 原文

- 链接：http://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study/
- 本地：`raw/articles/adriancourreges.com/2015-11-02_gta-v-graphics-study-adrian-courreges.md`
