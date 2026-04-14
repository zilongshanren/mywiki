---
tags: [source, 渲染, gpu, compute-shader, 性能]
date: 2026-04-14
sources: 1
---

# This many points is surely out of scope!（Aras Pranckevičius / aras-p.info）

[[aras-pranckevicius]] 发表于 2025 年 8 月的文章，记录他在为 Blender VSE 重写 waveform/vectorscope 示波器时，意外发现「**朴素 compute shader 比硬件点光栅化在所有 GPU 上都更快**」的过程。

## 摘要

故事从 HDR 视频示波器需要 GPU 化开始。把每像素映射成一个点 sprite、用 alpha blending 累加颜色，PC 上跑得很快——但 M4 Max 上 vectorscope 慢到 2 FPS。Aras 沿着 Fabian Giesen 的《A trip through the Graphics Pipeline》查根因，定位到三个隐藏瓶颈：

1. Vectorscope 把所有自然图像的点都堆在原点附近，造成 16 万次/像素的极端 [[overdraw]]。
2. 固定功能 alpha blending 必须 in-order，ROP 队列容量有限。
3. 单像素点会触发 2×2 quad overshading，每点 4 次 fragment shader 执行。

他写了一个 30+ 显卡的 WebGPU 跨平台基准，证实 Apple GPU 在「同点高密度」场景慢 12-19 倍，远超其他 vendor 的 2-5 倍。然后用最朴素的 compute shader（R/G/B `uint` 缓冲 + atomic add）重新实现，**所有 GPU 上比硬件路径快 1.5-10 倍**，AMD GPU 上接近 10×。最终的 PR 让 Blender 5.0 的示波器在 4K 视频上从 7.9 FPS 提升到 14.1 FPS，并且因为 resolve pass 自由可控，画质也更好。

## 关键要点

- **「GPU 一定比 CPU 快」是个未经验证的假设**。如果工作负载击中 ROP 队列、tile 缓冲、quad overshading 这些隐藏瓶颈，硬件路径会比 compute 路径慢得多。
- Apple GPU 没有专用的 ROP 硬件——alpha blending 在 fragment shader 内做 read-modify-write，整条 fragment 流水都得排成顺序队列才能保证语义正确。
- **Profiler 不一定能指出真凶**：Xcode 的 Metal frame capture 在这个例子里只会说「fragment shader 慢」，但真实瓶颈是 blending 队列。
- 朴素 atomic add 居然比 in-order blending 更快——因为 atomic 只需保证可交换的 RMW 原子性，没有 in-order 约束。
- 把 blending 拉出固定功能管线后，可以自由用任意非线性映射（log、tone curve、感知均匀），这是 Nanite/Dreams 这类 compute-based rendering 的次要动机。
- **教训**：对「点云」「粒子」「示波器」「直方图」这类极端密度的 fragment 写入工作负载，先尝试 compute 路径再说。

## 链接到的概念

- [[compute-vs-raster-points]]
- [[overdraw]]
- [[fragment-shader]]
- [[rasterization]]
- [[alpha-blending]]
- [[tbdr-vs-imr]]
- [[bottleneck-analysis]]
- [[unknown-unknowns]]

## 原文

- 链接：https://aras-p.info/blog/2025/08/24/This-many-points-is-surely-out-of-scope/
- 本地：`raw/articles/aras-p.info/2025-08-24_this-many-points-is-surely-out-of-scope-aras-website.md`
- 跨 GPU 基准 demo：https://aras-p.info/files/temp/webgpu/20250823_webgpu-point-raster.html
