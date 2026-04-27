---
tags: [source, 渲染, 帧分析, 光线追踪, 去噪, dlss, northlight, remedy]
date: 2026-04-27
sources: 1
---

# Frame Analysis: Control（Alain Galvan / alain.xyz）

[[people/alain-galvan]] 发表于 2021 年 6 月的文章，对 Remedy Entertainment 的 Control 游戏在 4K + DLSS 最高画质下的单帧渲染过程进行逐通道分析。

## 摘要

文章拆解了基于 Northlight 引擎的混合光追管线，按时序描述 9 个主要渲染阶段：BVH 加速结构构建、16384×2048 纹理图集阴影深度通道（光追+光栅双路阴影）、法线/粗糙度预通道、NDC 速度通道、弯曲法线 Dispatch、光追反射（全分辨率 GGX + SVGF 去噪变体）、半分辨率光追 GI（预计算体素 GI + 近场 BRDF）、接触阴影（灯光索引编码）、Fluid Smoke 屏幕空间流体效果（速度/散度/压力反馈回路）、DLSS 1080p→4K 超分、UI（Gameface HTML5 渲染器）。技术亮点是 Fluid Smoke 通道——用多 Compute 缓冲区实现的屏幕空间彩色气体效果，以及光追与光栅阴影并存的务实策略。

## 关键要点

- 光追阴影只用于接触阴影，主要阴影仍走光栅化图集方案
- 光追反射基于 GGX，远处/低粗糙度表面使用近似减少光线数量
- GI 在半分辨率下渲染，结合预计算体素 GI 处理远景
- SVGF 变体：含 Firefly Filter + 4 像素邻域空间滤波；偶有亮度不均匀问题但与美术风格契合
- Fluid Smoke 维护 velocity/pressure/divergence 三个流体缓冲区，帧间反馈扭曲产生气体流动效果
- DLSS 将 1080p 输入超分至 4K，让 RTX 2070 Super 在 4K 下均帧率 >30fps

## 链接到的概念

- [[rendering/northlight-frame-analysis]]
- [[rendering/hybrid-raytracing-pipeline]]
- [[rendering/rt-denoising]]
- [[rendering/svgf]]
- [[rendering/bvh-traversal-hardware]]

## 原文

- 链接：https://alain.xyz/blog/frame-analysis-control
- 本地：`raw/articles/alain.xyz/2021-06-11_frame-analysis-control.md`
