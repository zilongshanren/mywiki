---
tags: [source, 渲染, frame-analysis, clustered-forward, megatexture, adriancourreges]
date: 2026-04-27
sources: 1
---

# DOOM (2016) – Graphics Study（Adrian Courrèges）

[[people/adrian-courreges]] 发表于 2016 年 9 月的帧分析文章，基于 Vulkan + RenderDoc，结合 Siggraph 2016 id Tech 6 演讲，全面解析《DOOM (2016)》的渲染管线。

## 摘要

DOOM 2016 采用 id Tech 6 引擎，使用 **Clustered Forward Rendering** 而非完整延迟管线。每帧开始先通过 `vkCmdCopyBufferToImage` 更新 Mega-Texture 虚拟纹理 tiles（16k×8k 物理纹理，128×128 分块）；静态光源的阴影贴图缓存复用上帧结果，仅重建动态部分，存于 8k×8k atlas；深度预通道同时输出速度缓冲区（用于 TAA 和 motion blur）；GPU 遮挡查询进一步剔除几何；前向渲染 pass 以 DEPTH_EQUAL 方式着色所有不透明体，并生成精简 G-Buffer（法线+高光）用于后续效果；SSAO、SSR、IBL 静态 cubemap 探针依次合成；GPU compute 粒子更新；透明物体渲染前预先生成多级模糊链，支持玻璃按像素级别动态调整折射模糊度；TAA + motion blur 联合处理；Uncharted 2 filmic tonemapping；UI 在独立渲染目标合成。全帧 1331 次 draw call，50 个渲染目标，16ms 内完成。

## 关键要点

- [[clustered-forward-rendering]]：3072 个 froxel（16×8×24），每 cluster 最多 256 灯/decals/探针，CPU 预计算替代延迟管线多 G-Buffer 的开销
- Mega-Texture 虚拟纹理系统：渲染时 feedback buffer 报告缺失 tile，驱动下帧流式加载
- 静态阴影缓存：静态光+静态几何的 depth map 直接跨帧复用，动态部分单独合成
- 速度缓冲区：动态物体逐顶点计算上下帧位移；静态像素速度可从深度+相机变换推导，无需预存
- 粒子光照解耦：不论渲染分辨率，粒子光照固定存入小尺寸 atlas tiles，避免高分辨率重算
- 玻璃折射：预生成多级高斯模糊链，像素级读取相邻模糊级别插值，实现每像素不同折射模糊

## 链接到的概念

- [[clustered-forward-rendering]]
- [[megatexture-virtual-texturing]]
- [[taa-history-rectification]]
- [[screenspace-reflections]]
- [[deferred-rendering]]

## 原文

- 链接：http://www.adriancourreges.com/blog/2016/09/09/doom-2016-graphics-study/
- 本地：`raw/articles/adriancourreges.com/2016-09-09_doom-2016-graphics-study-adrian-courreges.md`
