---
tags: [source, metal, apple, 历史, api]
date: 2026-04-19
sources: 1
---

# A Decade of Metal: The Early Years (2014–2019)（Warren Moore / Metal by Example）

[[warren-moore|Warren Moore]] 发表于 2024 年 6 月 10 日，Metal 十周年的上半段回顾，把 Metal 1.0 到 Metal 2.2（iOS 13 / macOS 10.15）的关键 feature 按年铺开。

## 摘要

作者 2014 年 WWDC 后离开 Apple 开了这个博客，把 Metal 作为职业主线维持到现在。回溯第一个五年：

- **2014 / Metal 1.0**（iOS 8 独占）：fixed-function state（混合、顶点布局）必须在 draw 前确定以降驱动开销；multi-thread command recording；compute shader（A7 上性能一般但铺好了 MPS / ML 的路）；MSL 是 C++ 加 GPU 扩展。当时还缺 indirect draw、tessellation、dual-source blending
- **2015**：Metal 上 Mac，随 MetalKit（跨平台 `MTKView`、纹理加载、Model I/O）和 MetalPerformanceShaders（预编译 compute kernel 覆盖图像处理 / 线性代数，埋伏 ML 未来）一起发；加入 indirect dispatch / draw，追上 OpenGL 4.0
- **2016 / iOS 10**：加入 tessellation——Metal 走的路径和 OpenGL 不同，**用 compute shader 代替 TCS**（可自选频率生成 tessellation factors 写 buffer，固定功能 tessellator 消费，post-tessellation vertex function 做顶点属性插值）；加入 heap（资源从大块内存子分配，可 aliasable）；dual-source blending（Mac 先，iOS 后）
- **2017 / Metal 2**：GPU-driven rendering 的真正起点。A11 Bionic 解锁 imageblocks + tile shader（render/compute 在一个 encoder 里交错）；第一代 argument buffers（后来被淘汰，但开了 bindless 的门）；nonuniform threadgroup sizes（省掉 `(N+ts-1)/ts` 这种算术）
- **2018**：raytracing v1 —— `MPSRayIntersector` 提供层级+实例化加速结构；indirect command buffer（ICB）把命令录进 buffer 复用，类似 DX12 bundle / GL `glMultiDrawElementsIndirect`
- **2019 / Metal 2.2**（A13）：sparse heap（texture streaming 的关键但作者当时低估了）；GPU 端可在 argument buffer 里 set pipeline（CPU/GPU 工作彻底解耦）；rasterization rate map（可变速率光栅化——后来在 visionOS 做 foveated rendering 的基础）；vertex amplification（多 RT 一轮顶点处理——立方体 / AR/VR 多视口的基础）

贯穿第一个十年的主题：**从 OpenGL 附庸走向 GPU-driven 主力渲染路线**，每次 WWDC 加一块拼图，一批早期 feature（argument buffers v1、MPS raytracing）后来被更成熟的替代。

## 关键要点

- Metal 1 重点是 fixed state + multi-thread encoding 降驱动开销，一上来就支持 compute shader
- Metal 2 的 argument buffer / tile shader / imageblock 是 GPU-driven pipeline 的关键 enable
- Tessellation 用 compute shader 代替 TCS，灵活性 > 传统 pipeline
- Heap 是后续 argument buffer / manual hazard tracking 的地基
- ICB + argument buffer 加速 CPU 端 draw call 编排
- Rasterization rate map + vertex amplification 后来在 Vision Pro 起关键作用
- 一批早期 feature（argument buffer v1、MPS raytracing）后来被淘汰重做

## 链接到的概念

- [[metal-decade-history]]
- [[metal-api-overview]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/a-decade-of-metal-early-years/
- 本地：`raw/articles/metalbyexample.com/2024-06-10_a-decade-of-metal-the-early-years-2014-2019.md`
