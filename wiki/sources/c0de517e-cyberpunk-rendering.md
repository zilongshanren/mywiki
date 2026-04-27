---
tags: [source, rendering, deferred-rendering, cyberpunk-2077, shadows, screen-space, gi, frame-analysis]
date: 2026-04-27
sources: 1
---

# Hallucinations Re: the Rendering of Cyberpunk 2077（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2020 年 12 月的文章，通过 RenderDoc 捕帧对 CP2077 渲染管线进行推测性逆向分析。

## 摘要

作者在高画质（无 RTX/DLSS）设置下逐步拆解 Cyberpunk 2077 的一帧。管线骨架是经典 [[rendering/deferred-rendering]]：G-Buffer 布局为 10.10.10.2 法线 + 10.10.10.2 Albedo + 8.8.8.8 金属度/粗糙度/半透/自发光，外加深度前置通道减少 overdraw。光照分两层：解析光以 32×32 froxel 聚类光源做 tiled compute，并行输出漫反射/高光两张 RGBA16；阴影系统混合 CSM（跨帧更新静态物体）、VSM（多帧增量）和屏幕空间 contact shadows。间接光依赖三条路径：HBAO/GTAO 级别的 bent normals + 锥体 AO、增量更新的探针数组（推测 GGX 预滤波）和一组 64×64×64 体积纹理（推测 SH 辐照度，可能是动态 GI）。SSR 全分辨率运行并使用前帧颜色做重投影。作者特别强调：场景主要照明来自间接光而非解析光，时域重投影质量极高，即便在大量透明表面的赛博朋克世界中也几乎无破绽。

## 关键要点

- G-Buffer 布局紧凑，法线用 10.10.10.2，mesh decal 使用自定义法线混合而非硬件 blend
- 剔除全在 CPU 侧（无 GPU depth pyramid），绑定式贴图（静态几何 bindless，动态物体非 bindless）
- CSM 跨帧增量更新；VSM 以 512/256 分辨率阵列存储，单帧仅更新少量切片
- 间接 GI 以体积纹理为主，均匀覆盖动静物体，避免漏光
- SSR 全分辨率但噪声明显，依赖时域抗锯齿做降噪
- 时域重投影是整帧画质稳定性的核心支柱

## 链接到的概念

- [[rendering/deferred-rendering]]
- [[rendering/cascaded-shadow-maps]]
- [[rendering/screenspace-reflections]]
- [[rendering/ground-truth-ambient-occlusion]]
- [[rendering/temporal-antialiasing]]
- [[rendering/volumetric-fog-froxels]]
- [[rendering/tiled-light-culling]]
- [[rendering/bindless-rendering]]

## 原文

- 链接：https://c0de517e.blogspot.com/2020/12/hallucinations-re-rendering-of.html
- 本地：`raw/articles/c0de517e.blogspot.com/2020-12-17_hallucinations-re-the-rendering-of-cyberpunk-2077.md`
