---
tags: [source, 渲染, DirectX12, 图形API, HLSL, 命令队列, alain.xyz]
date: 2026-04-27
sources: 1
---

# Raw DirectX 12（Alain Galvan / alain.xyz）

[[alain-galvan]] 发表于 2021 年 10 月的文章，以 Hello Triangle 程序为蓝本系统拆解 DirectX 12 的核心对象和渲染循环。

## 摘要

文章从 Debug Controller 启用方式开始，依次介绍 Factory → Adapter（软件与硬件适配器区分）→ Device → CommandQueue → CommandAllocator → CommandList 的创建链；Fence 和 Barrier 的同步语义；SwapChain 与 DescriptorHeap（RTV）的配合；Upload Heap 和 Readback Heap 的内存管理；Root Signature 的资源绑定声明；以及 PSO 的完整描述（Input Assembly、Root Signature、VS/PS bytecode、Rasterizer、Blend、Depth/Stencil、RTV 格式）。最后演示了帧循环中的命令录制、提交与围栏等待流程。文章末尾提及 DirectML、DXR（光线追踪）、Mesh Shaders 等进阶方向。

## 关键要点

- DX12 将命令录制与提交解耦，天然支持多线程录制和异步 compute
- ResourceBarrier 是显式声明资源用途转变的机制，驱动据此排查访问冲突
- DescriptorHeap 集中管理 CBV/SRV/UAV 描述符，避免每次绑定时驱动分配内存
- Root Signature 在 PSO 构建前定义着色器可见资源布局；bindless 是其自然演进
- `ComPtr<T>` 可替代手动 `Release()`，但显式资源生命周期管理仍是最佳实践

## 链接到的概念

- [[rendering/directx12-api-overview]]
- [[rendering/d3d12-root-signature]]
- [[rendering/d3d12-resource-binding]]
- [[rendering/d3d12-resource-alignment]]
- [[rendering/gpu-hazard-tracking]]
- [[rendering/async-compute]]
- [[rendering/frames-in-flight]]
- [[rendering/bvh-traversal-hardware]]

## 原文

- 链接：https://alain.xyz/blog/raw-directx12
- 本地：`raw/articles/alain.xyz/2021-10-24_raw-directx-12.md`
