---
tags: [source, 渲染, 图形API, Vulkan, DirectX, Metal, WebGPU, OpenGL]
date: 2026-04-27
sources: 1
---

# A Comparison of Modern Graphics APIs（Alain Galvan / alain.xyz）

[[people/alain-galvan]] 发表于 2021 年 1 月的文章，对 Vulkan、DirectX 12/11、Metal、WebGPU、OpenGL 六个图形 API 的核心数据结构进行逐类对比。

## 摘要

文章按图形应用生命周期（初始化 → 加载资源 → 更新 → 呈现 → 销毁）逐一对比六个 API 的对应数据结构，涵盖：入口点、物理/逻辑设备、队列、命令池、Surface、Swapchain、帧缓冲、纹理、缓冲、着色器模块、绑定布局、Pipeline、命令缓冲、同步原语（Fence/Barrier/Semaphore）。核心结论是：现代 API（Vulkan、DX12、Metal）设计高度趋同，差异主要体现在抽象层次和职责划分——Metal 最简洁（物理/逻辑设备合一、Swapchain 委托给 OS），Vulkan 最显式（内存管理、队列族、信号量全暴露），DX11/OpenGL 是高层 API，大量工作由驱动完成。坐标系差异（Bottom Left 对 Top Left）在 UV `y` 翻转处处理即可。文章还列举了 Falcor、NVRHI、The Forge、bgfx 等跨平台图形抽象框架。

## 关键要点

- Vulkan 是唯一把 Semaphore 内置于 API 的；DX 和 Metal 委托 OS 调用
- Metal 的 `CAMetalLayer` 身兼 Surface + Swapchain 双重职责
- DX12/Vulkan 支持显式内存管理；AMD 为两者分别提供了内存分配器库
- DirectX 的像素空间原点在左上角，Vulkan/OpenGL/WebGPU 在左下角
- Vulkan Pipeline 要求在创建设备前就声明要使用的队列族
- 推荐工具：VMA（Vulkan Memory Allocator）、D3D12MA（D3D12 Memory Allocator）

## 链接到的概念

- [[rendering/graphics-api-history]]
- [[rendering/shader-ir-pipeline]]
- [[rendering/async-compute]]
- [[rendering/buffer-renaming]]

## 原文

- 链接：https://alain.xyz/blog/comparison-of-modern-graphics-apis
- 本地：`raw/articles/alain.xyz/2021-01-31_a-comparison-of-modern-graphics-apis.md`
