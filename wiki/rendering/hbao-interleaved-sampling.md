---
tags: [渲染, 环境光遮蔽, ssao, hbao]
date: 2026-04-14
sources: 1
---

# HBAO 与 Interleaved Sampling

**Horizon-Based Ambient Occlusion（HBAO）** 是 NVIDIA 在 2008 年左右提出的屏幕空间环境光遮蔽算法，其 HBAO+ 变体在大量 AAA 游戏中被采用。Rise of the Tomb Raider 使用的是 HBAO+ 的一种实现，值得记录的是它所采用的 **interleaved sampling** 技术——这是一个把单 pass 重 shader 拆成多 pass 轻 shader 的巧妙工程 trick，作者是 Louis Bavoil。

## 为什么不直接多采样

一个像素要估计环境遮蔽，理论上需要在半球上多次采样深度 buffer 并做计算。单像素做 **32 次采样**已经相当重；如果想获得非常平滑的结果，比如等效 **512 次采样**，在 GPU 上直接跑是不可接受的。

## 4×4 交织拆分

Interleaved sampling 的做法是：

1. **把深度 buffer 按 4×4 块切成 16 张小图**。第一张图只取每个 4×4 块中位置 (0,0) 的像素，第二张取 (1,0)，依此类推。16 张图一起覆盖了原深度 buffer 的所有像素。
2. **对每张小图独立做 HBAO，使用不同的采样方向**。每一张小图的 32 次采样负责讲述这 4×4 块内的一部分故事。
3. **把 16 张 AO 结果织回成一张全分辨率图**——这张图非常 noisy，因为每个 4×4 块内四个相邻像素来自不同的采样集。
4. **做一个 full-screen blur**，把噪声磨平——blur 既是去噪，也是把 16 个采样集的结果**事实上平均**成等效 512 采样的结果。

## 为什么这样更快

直接单 pass 做 512 次采样不仅指令数量多，而且对缓存非常不友好——采样位置散布在半球上，命中率差。拆成 16 个小 pass 之后，**每个 pass 只采样 32 次，命中的内存区域小而密集**，GPU 的纹理缓存利用率大幅提升。Louis Bavoil 在一篇论文里专门讲过这个 cache-efficient post 的思路。

这是一个典型的「**把 latency-bound 算法改写成 throughput-bound**」的例子——算术工作量差不多，但访存模式完全变了。

## 与 depth-aware upsampling 的配合

ROTR 里 AO 通常是半分辨率计算的，最终要 upscale 回全分辨率——简单的 bilinear 在深度不连续处会糊。这里 Foundation 使用了 [[depth-aware-upsampling]] 的 stencil 技巧：把不连续像素 mark 进 stencil buffer，用一个简单 shader 处理连续区域、用一个复杂 shader 处理不连续区域，早期 stencil discard 保证每个区域只付它该付的成本。

## 相关

- [[deferred-rendering]]
- [[depth-aware-upsampling]]
- [[z-buffer]]
- [[cache-friendliness]]
- [[prebaked-corner-occlusion]] —— SSAO 时代之前的 lightmap / 顶点色烘焙 AO，以及 Sims 4 的手贴 AO mesh 补丁方案

## Sources

- [[sources/elopezr-rotr-rendering]]
