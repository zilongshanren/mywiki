---
tags: [source, 渲染, 体积光, 框架, siggraph]
date: 2026-04-14
sources: 1
---

# CSharpRenderer framework update + volumetric fog code（Bart Wronski，2014-08）

[[bartosz-wronski|Bart Wronski]] 2014 年 8 月的更新说明：他把 Siggraph 2014 talk *Volumetric Fog*（《Assassin's Creed 4》里 Scimitar 引擎用的那套 froxel 体积雾，技术见 [[volumetric-fog-froxels]]）的 demo compute shader 代码发布到了开源的 **CSharpRenderer** C# / .NET / DX11 原型框架里。

## 摘要

这篇 post 是 CSharpRenderer 的一次 major update 发布公告，核心礼物是**随代码附带的 volumetric fog compute shader demo**——Wronski 明确说明这不是 shipping 代码（shipping 版包含 NDA 的 console 专属优化），而是 Siggraph 讲座配套的「快速写就的示例」。这是公开世界里早期可以直接读到的 froxel volumetric pipeline 实现之一，对于想照着 [[volumetric-fog-froxels|ROTR / Frostbite / Unity HDRP]] 同一套做法自己 prototype 的人非常有价值。其他更新包括：**Global Shader Define** 机制——shader 里带 `// GlobalDefine` 注释的 `#define` 能被 C# 代码直接通过 `ShaderManager.GetUIntShaderDefine(...)` 反射读取，消除 shader/CPU 常量重复；基于 Rory Driscoll 的 derivative maps（用普通 normal map 当 derivative map 近似，省掉 tangent frame 生成）；GPU Pro 的 Perlin noise 纹理生成器（体积雾用它做动画扰动）；基于 John Hable 优化的 GGX specular BRDF；以及 Black Ops 2 的 environment BRDF 近似、累积式 temporal AA、UI 动态重载等杂项改进。Wronski 保持框架定位——**不是生产级代码，而是「迭代时间逼近 0」的实验 playground**。后续计划包括 post-effect / tone mapping 重写、GPU 调试、screen-space reflection、面积光（会和体积雾联动得很好）和局部阴影。

## 关键要点

- **发布：** 开源 CSharpRenderer 框架配套的 froxel **volumetric fog compute shader 示范代码**，来源于 Wronski Siggraph 2014 talk，非 shipping 代码，不含 console NDA 优化。
- 这是 [[volumetric-fog-froxels|AC4/Scimitar → ROTR/Frostbite/UE/Unity HDRP]] 同一套 froxel 思路的早期公开参考实现。
- **Global Shader Define**：shader `#define` 带 `// GlobalDefine` 标签即可被 C# 反射读取，避免 shader 与 CPU 常量的重复定义与不同步。
- **Derivative maps**：借用 Rory Driscoll 的做法，用 normal map 直接当 derivative map，跳过 mesh 预处理里的 tangent 生成——对 prototype 足够。
- **GGX Specular**：用 John Hable 的 `dot(L,H)` 优化版 GGX；Black Ops 2 的 environment BRDF 2D LUT 近似。
- **Perlin noise generator**：GPU Pro 的做法，生成过后用来驱动体积雾的动画扰动。Wronski 回复读者说 demo 默认很 subtle、想看效果得去 `volumetric_fog.fx` 里自行调高。
- **其他工程改进**：累积式 temporal AA（参考 UE4 AA talk）、动态 UI 重载、LUA 脚本化常量缓冲、基础 particle 渲染（GPU buffer + vertex shader）、UI 清理、FPS clamp。
- **框架定位**：prototype playground，追求「迭代时间趋近于 0」，不追求代码美感或性能。
- **后续计划**：post / tonemap 重写、GPU 调试、SSR + env cube-map、面积光（与体积雾协同）、局部光源阴影。

## 链接到的概念

- [[volumetric-fog-froxels]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/08/20/major-c-net-graphics-framework-update-volumetric-fog-code/
- 本地：`raw/articles/bartwronski.com/2014-08-20_major-c-net-graphics-framework-update-volumetric-fog-code.md`
