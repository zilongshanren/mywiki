---
tags: [source, rendering, game-development, curriculum, graphics-programmer, deferred-rendering, global-illumination]
date: 2026-04-27
sources: 1
---

# Thoughts on the Knowledge of an Up-to-date Graphics Programmer（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 发表于 2011 年 3 月，梳理其在 UCSD 开设的图形编程课程大纲，反映 2011 年前后工业界图形程序员的知识图谱。

## 摘要

Engel 列出了他认为一名跟上时代的图形程序员应掌握的核心模块：DirectX 11 API、延迟光照与 MSAA、Order-Independent Transparency（OIT）、阴影（Cascaded/Cube/Soft）、PostFX 管线、GPU 粒子系统、实时动态全局光照以及 CUDA/DirectCompute。他的立场是 API 无关论——掌握一套 API 的概念后其他都能自学，只是暴露硬件功能的完整度不同。对延迟光照他指出当前最大问题是透明物体的光照与阴影；对全局光照他强调必须完全动态（无查找表/光照贴图），Reflective Shadow Maps + Light Propagation Volumes 是可行起点。CUDA 被推荐作为理解 GPU 内存层次和执行模型的入门路径，比 DirectCompute/OpenCL 更透明。

## 关键要点

- 2011 年工业级图形程序员的标准技能树：延迟光照 + MSAA + OIT + 阴影系统 + PostFX + GPU 粒子 + 动态 GI + GPGPU
- Deferred Lighting 已是标准管线，主要挑战是半透明和 OIT
- 目标光源密度：不透明物体 1000+ 灯可实现，阴影更难，透明物体暂无通用解
- GI 首选方案：Reflective Shadow Maps → Light Propagation Volume，约 1.5–2.5 MB 内存
- CUDA 作为 GPU 架构理解的入门首选，DirectCompute/OpenCL 抽象层更高但可移植性更好
- MSAA 在延迟下昂贵：边缘 per-sample，内部 per-pixel，MLAA 补充但不适用运动物体

## 链接到的概念

- [[rendering/deferred-rendering]]
- [[rendering/msaa-ssaa]]
- [[rendering/tiled-light-culling]]
- [[rendering/tessellation-approaches-overview]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2011/03/thoughts-on-knowledge-of-up-to-date.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2011-03-15_thoughts-on-the-knowledge-of-an-up-to-date-graphics-programm.md`
