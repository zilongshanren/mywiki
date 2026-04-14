---
tags: [source, 渲染, metal, apple, 教程]
date: 2026-04-14
sources: 1
---

# Up and Running with Metal, Part 1: Clearing the Screen（Warren Moore）

[[warren-moore|Warren Moore]] 2014 年 8 月在 *Metal by Example* 发表的系列首篇，目标只有一个——**把屏幕清成纯红色**。文章逐步引入 Metal 与 UIKit 的胶合层 [[cametal-layer-drawable|CAMetalLayer]]、`MTLDevice`、`MTLCommandQueue` / `MTLCommandBuffer` / `MTLRenderCommandEncoder`、`MTLRenderPassDescriptor`，是理解 Metal「显式对象图」心智模型的最短路径。

## 摘要

文章从 Xcode 新建 Single View 项目开始，链接 `Metal.framework` 与 `QuartzCore.framework`，然后把一个自定义 `UIView` 的 backing layer 通过覆写 `+layerClass` 改成 `CAMetalLayer`。拿到 metal layer 之后先给它设 `device` 和 `pixelFormat`（`BGRA8Unorm`），接着在 `-redraw` 里走一次完整的 Metal 命令链：向 layer 问 `nextDrawable` 拿到 framebuffer texture，填一个 render pass descriptor（`loadAction=Clear`、`storeAction=Store`、`clearColor=红色`），从 device 开 command queue，从 queue 开 command buffer，从 command buffer 开 render command encoder、立即 `endEncoding`（因为不需要画任何几何），最后 `presentDrawable:` + `commit`。整个 redraw 方法只有二十几行，但覆盖了后续所有 Metal 程序的骨架。Warren 顺便强调两件事：Metal API **大量使用 Objective-C 协议**（`id<MTLDevice>`）而非具体类；Metal 尽管 low-level，仍然**保留了抽象层**，比如 command encoder 和 library。

## 关键要点

- **`+layerClass`** 是 UIKit → Core Animation → Metal 的三级粘合点；在 macOS 上要改用 `setWantsLayer:` + `makeBackingLayer`。
- **Device 是工厂**：command queue、library、pipeline state 全由它创建。
- **Render pass descriptor** 描述一次 pass 的 load / store 行为和 attachment；在 [[hsr-tbdr|TBDR 架构]] 上 load / store action 直接决定 tile memory 与 DRAM 的往返。
- **命令三件套 queue / buffer / encoder** 是显式 API 的共通结构——Metal、D3D12、Vulkan 都是一样的。
- **CAMetalDrawable** 是一张「临时」2D texture 的 handle，它的生命周期由 Core Animation 管；`presentDrawable:` 是「我画完了」的信号而不是立即上屏。
- **没有状态机**：清屏动作是通过 render pass descriptor 的 clearColor 实现的，而不是 `glClearColor` + `glClear`。这种「描述性」而非「命令性」的风格是 Metal 的核心性格。

## 链接到的概念

- [[metal-api-overview]]
- [[cametal-layer-drawable]]
- [[rendering-pipeline]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/up-and-running-1/
- 本地：`raw/articles/metalbyexample.com/2014-08-25_up-and-running-with-metal-part-1-clearing-the-screen.md`
