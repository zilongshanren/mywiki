---
tags: [source, 图形, metal, powervr, tbdr, apple]
date: 2026-04-19
sources: 1
---

# Underestanding PowerVR GPUs via Metal（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015-05 的文章，用 Metal API 面作「反向望远镜」理解 PowerVR 的实际硬件行为。

## 摘要

新一代「贴近硬件」的 API（Metal / Mantle / Vulkan / D3D12）给了我们一种新工具——**通过 API 推断硬件**：如果 GL 被重写以匹配今天的 GPU，API 形状会变成什么样？作者从 Metal 三个设计点推 PowerVR 的内部结构。**Mutability Is Expensive**：`MTLTexture` 没有改尺寸 API，要变就造新对象——因为驱动一旦认定一份 texture 的硬件资源和 shader 引用，不愿意承担「下次还 valid 吗」的反复检查；GL 的 texture bind 可以把 2D 变 cube map，驱动被迫每 draw 重新验证。**Command Buffers + Queues**：`MTLCommandBuffer` / `MTLCommandQueue` / `MTLCommandEncoder` 直接暴露「填 command buffer → 排队给 GPU」这条真实管线，GL 上下文其实是把 encoder 藏在 thread 里自动 flush。**Entire Pipeline Grafted Onto Your Shader**：在 PowerVR 上 blend 和 framebuffer 写出都在 shader 内（tile 在片上 cache 里），加上 vertex fetch 的前置——一个 GLSL program 实际变成「前置 vertex + 你的 VS + 你的 FS + 后置 blend/write」的组合 shader；`MTLRenderPipelineState` 把这四段一起打包成 immutable 对象。另外，**GPU 在 render pass 起止时做大量工作**（tile 的 load/clear、save/discard），Metal 用 `MTLRenderPassDescriptor` 显式要求你回答 load/store action，GL ES 只能推断。评论里 Rys（Imagination）确认 tile size **32×32**，vertex fetch 仍是硬件块但**受 shader 驱动**（近似 fixed-function）。

## 关键要点

- **TBDR 核心**：32×32 tile 在片上 cache 做 raster+shade，pass 结束写回 DRAM——为了省带宽 = 省功耗。
- **Render pass descriptor 是强制问题**：load（load/clear/dontCare）+ store（store/discard/resolve）——给驱动完整意图。
- **Pipeline = shader + 前置 vertex fetch + 后置 blend/write**——PowerVR 上 blend 在 shader 里（不是 ROP），所以 color mask / blend 变更 = 新 PSO。
- **Mutability 的代价**：GL 的可变 texture / buffer 迫使驱动每次 draw 重验证；Metal immutable → 绑了就 valid。
- **Command encoder 暴露**：GL 的「为什么调完函数没执行」= 驱动在等 buffer 填满或 flush。
- **X-Plane 实践**：blending 永远绑 shader，shader 和 PSO 自然 1:1，迁移 Metal 成本低。
- 评论：**vertex fetch 在 PowerVR 仍是硬件块**（Rys 确认），但由 shader 驱动，可看作近乎 programmable。

## 链接到的概念

- [[mtl-render-pipeline-state]]
- [[mtl-render-pass-descriptor]]
- [[metal-api-overview]]
- [[hsr-tbdr]]
- [[tbdr-vs-imr]]
- [[opengl-hardware-impedance-mismatch]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/05/underestanding-powervr-gpus-via-metal.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-05-22_underestanding-powervr-gpus-via-metal.md`
