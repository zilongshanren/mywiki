---
tags: [渲染, 程序化, 草地, 几何着色器, LOD, 植被]
date: 2026-04-27
sources: 1
---

# 程序化草地渲染（Procedural Grass Rendering）

草地是实时渲染中最难平衡「密度感」与「性能预算」的对象：单片草叶的几何极其简单，但场景中动辄有数十万到数百万根，并且需要跨 LOD 级别保持视觉连续。程序化方案的核心思路是**在运行时生成叶片，而不是预存储每根草叶的顶点**——从而把内存压力换成 GPU 算力，同时把 LOD 降为生成算法的一个参数而非多套独立资产。

## 双阶段架构

Outerra 引擎在 2012 年展示了一套典型的双阶段方案：

**第一阶段：canopy 生成**
生成一张分辨率约 30 cm/texel 的高度掩码（canopy 贴图），用 fractal pattern 表达草的稀密分布与高度变化。这张贴图有两个用途：（1）驱动第二阶段的叶片生成；（2）直接作为远景地形的「矮植被信封」纹理——远处你看到的不是裸露地表而是这张程序化蒙版盖出来的植被轮廓，使近景草叶与远景纹理在视觉上无缝衔接。

**第二阶段：叶片生成**
几何着色器读取 canopy 贴图，为每个纹素生成若干草叶。每根草叶是一个 7 顶点 5 三角形的 triangle strip，带有 3 段弯曲以模拟自然形态。对矮草，将 3 段折叠成 V 形——顶点数不变，但等效翻倍了视觉上的草叶密度，因为矮草覆盖率低，需要更多「视觉存在感」。

## LOD 策略

LOD 直接映射为「每个 canopy 像素生成几根叶片」：最近处 4 根，每退一级减半、同时加倍叶片宽度，维持视觉覆盖率。宽度补偿使远处草地看起来仍然有足够的填充感，而不会出现稀疏的单线感。

相比之下，预烘焙方案需要为每个 LOD 级别单独维护一套网格资产，切换时有明显的几何跳变（pop-in）；程序化方案的 LOD 过渡是连续的，因为叶片密度和宽度可以随距离平滑调节。

## 几何着色器的局限

几何着色器生成叶片的方法在 2012 年是主流选择，但后来逐渐被更现代的方案替代：

- **顶点着色器 + instancing**：把草叶模板作为 instance mesh，用顶点着色器读取 canopy 数据做偏移；比 GS 路径在 AMD 等架构上有显著性能优势（参考 [[gpu-driven-grass-tiles]]）。
- **Compute shader + indirect draw**：先用 CS 剔除不可见草叶，再 indirect draw 剩余草叶；天然支持 GPU-driven culling。
- **Mesh shader（现代 API）**：meshlet 级别控制，更灵活地混合 LOD。

对于「几何着色器吞吐 vs instanced VS」的实测数据，Outerra 的另一篇 OpenGL 性能测试（[[sources/outerra-opengl-perf-grass]]）给出了跨 GPU 厂商的详细曲线：indexed triangle list + 5k-20k tri/instance 是跨厂最稳的甜点。

## 动画

草叶动画可以极简实现：直接采样一张预存的波纹纹理（如海浪纹理），把 UV 偏移映射到叶片顶点偏移。这比「基于物理的布料/弹性杆」便宜得多，在远中景下视觉质量足够。近景叶片如果需要与角色交互，通常需要额外的单独处理（如基于距离场的弯曲响应）。

## 相关

- [[gpu-driven-grass-tiles]] — GPU 驱动的草地 tile 渲染，instancing 路径
- [[waving-grass-shader-vertex-offset]] — 顶点偏移驱动草叶摆动
- [[vegetation-procedural-placement]] — 植被的程序化放置与分布
- [[deferred-grass-shader]] — 延迟渲染管线下的草地 shader
- [[outerra-team]]

## Sources

- [[sources/outerra-procedural-grass]]
