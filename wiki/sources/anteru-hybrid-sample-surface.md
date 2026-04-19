---
tags: [source, 渲染, 光线投射, 光栅化, 大规模几何]
date: 2026-04-19
sources: 1
---

# Hybrid Sample-based Surface Rendering（VMV 2012）

Reichl、[[matthaeus-chajdas|Chajdas]]、Bürger、Westermann（TUM）发表于 **VMV 2012** 的论文。针对"三角形小于像素时光栅化崩溃"和"大模型 overdraw 代价高"两个经典病症，提出**在每帧内同时使用光栅化和光线投射**的混合管线。

## 摘要

现代 GPU 的光栅化性能**强烈依赖于能否避免 overdraw 和避免渲染小于像素的三角形**——否则高分辨率多边形模型的显示帧率会被严重拖垮。本论文不试图把这两件事塞回光栅化管线，而是提出一条备选管线：**每帧同时用光栅化和光线投射**确定视线-表面交点。

为让光线投射与光栅化可比，作者提出**内存高效的 sample-based 数据结构**，支持高效 ray traversal。结合模型的**规则划分**，**在运行时为每一部分选择最优渲染技术**。对超大三角形 mesh，本方法在性能上可以超过纯光栅化，且 GPU 内存占用明显更小。该数据结构可从任何 renderable 表面表示构造，也可用于标量体数据的 isosurface。当替代方法需要大量 paging 时，本方法仍能从 GPU memory 直接渲染。

## 关键要点

- **分而治之**：模型规则划分，每一块按当前视角特征选择光栅化 or ray-cast。
- **sample-based 表示**紧凑，能从 GPU memory 直接渲染；传统方法此时已需大量 paging。
- 同一份数据结构可同时服务 triangle mesh 的屏幕渲染和体数据的 isosurface 提取——泛化性好。

## 链接到的概念

- [[matthaeus-chajdas]]

## 备注

这是 Chajdas 博士期间的论文，问题与 Gigavoxels、SVO 路线并列（2012 年前后 large-model 渲染的几种学术探索）。没有直接延伸到今天的产品线，但"光栅化 + 光线投射混合 + runtime 选择"的框架思想后来在 UE5 Nanite（rasterizer vs. compute raster 的二选一）和 Lumen（SDF trace vs. mesh SDF trace vs. HW RT 的三选一）里都能看到类似结构。

## 原文

- 链接：<https://anteru.net/research/hybrid-sample-based-surface-rendering>
- 项目页：<https://www.in.tum.de/cg/research/publications/2012/hybrid-sample-based-surface-rendering/>
- 本地：`raw/articles/anteru.net/2025-02-16_hybrid-sample-based-surface-rendering.md`
