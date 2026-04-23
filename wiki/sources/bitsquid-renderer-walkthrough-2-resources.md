---
tags: [source, 渲染, 资源系统, api抽象, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray Renderer Walkthrough #2: Resources & Resource Contexts（Tobias Persson / bitsquid 博客）

[[tobias-persson]] 发表于 2017-02-01 的博客，Stingray Renderer Walkthrough 系列第二篇，详述**GPU 资源的跨 API 抽象**和它的创建/销毁机制。

## 摘要

所有图形 API 专用代码（D3D / OGL / GNM / Metal）都封在 `RenderDevice` 背后。引擎侧用一个 POD `RenderResource` 做跨 API 表示，内部只有一个 `render_resource_handle`：高 8 位 type 枚举、低 24 位 type 专属数组 index。支持的资源种类覆盖完整 PSO 组件：Texture / RenderTarget / DependentRenderTarget / BackBufferWrapper / ShaderConstantBuffer / VertexStream / IndexStream / VertexDeclaration / RawBuffer / BatchInfo / Shader。大多数 buffer 类资源有 `STATIC / UPDATABLE / DYNAMIC` 三档 validity。

`RenderResourceContext` (RRC) 是创建/销毁资源的接口。它不是 thread-safe，但可以同时开多个实例——线程安全下放到调用方。RRC 本质是一条 command buffer，`alloc(resource)` / `dealloc(resource)` 压变长 "package"。RRC 还能持有平台专属 allocator，让 immutable 资源（贴图等）直接 stream 到 GPU 映射内存。录完后通过 `RenderDevice::dispatch` 在控制线程上提交，或通过 `RenderInterface::dispatch` 从其他线程提交（`RenderInterface` 是向 renderer 派数据的 thread-safe ring buffer）。

把 alloc/dealloc 从 `RenderDevice` 直接接口拆出来的好处：调度灵活、RRC 不用 thread-safe、可批量。文末预告下一篇讲 `RenderJobs` 和 `RenderContexts`——draw call / state change 的录制与调度。

## 关键要点

- `render_resource_handle` 把 type 和 index 压进 32 bit——`RenderDevice` 里按 type 切数组做 O(1) lookup。
- Validity 三档反映"谁更新、多频繁"：DCC 资产多为 STATIC，粒子系统为 DYNAMIC。
- RRC 的 command-buffer 化是 Stingray 跨子系统一致的 pattern（和 [[main-render-thread-state-reflection|state reflection]] 的 `StateStream` 思路一致）。
- 评论区问出关键技术悬念：handle 何时填值？作者没直接答，读者给出"本地 handle + dispatch 时平移到全局"的合理解决方案。
- `BackBufferWrapper` 是引擎创建 swap chain 时唯一自己造出来的 RT，其他 RT 都是用户显式创建。

## 链接到的概念

- [[stingray-render-resource-context]]
- [[stingray-renderer-three-stage-pipeline]]
- [[main-render-thread-state-reflection]]
- [[d3d12-resource-binding]]
- [[bindless-rendering]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-2.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-02-01_stingray-renderer-walkthrough-2-resources-resource-contexts.md`
