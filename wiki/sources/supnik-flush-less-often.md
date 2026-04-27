---
tags: [source, rendering, opengl, command-buffer, vbo, streaming]
date: 2026-04-27
sources: 1
---

# Flush Less Often（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2018 年 1 月的文章，解释 OpenGL 隐式命令缓冲区的「冲刷」（flush）问题如何在大量小 batch 场景中拖垮性能，以及两种实用修复路线。

## 摘要

现代 GPU 通过命令缓冲区工作：CPU 把绘制指令写进缓冲区，缓冲区满或显式触发时才真正发给 GPU。Vulkan/Metal/DX12 里命令缓冲区是显式对象；OpenGL 里则是隐式的，在 `glFlush`、`glFinish`、`glSwapBuffers` 以及缓冲区写满时自动冲刷。问题在于，当代码结构是「写数据 → draw → 写数据 → draw …」循环时，每次 `glMapBufferRange` 的 unmap 都必须在 draw 之前完成，防止命令缓冲区在 buffer 还没准备好时意外发出。这迫使 CPU 频繁进行不必要的同步，尤其对小 batch 性能极差。解决方案有两条：一是用**持久一致性缓冲区**（persistent coherent buffer），写完无需 flush，GPU 随时可见；二是**推迟所有 draw 调用**，先把全部 buffer 填好再统一发出——这是 Supnik 在不支持持久缓冲区的老 OpenGL 上的实际做法，同时还可以顺手去掉冗余的状态切换。

## 关键要点

- OpenGL 命令缓冲区冲刷时机：`glFlush`、`glFinish`、`glSwapBuffers`、缓冲区满、以及某些 sync 操作。
- 即便使用 `glMapBufferRange` + `GL_MAP_UNSYNCHRONIZED_BIT`，unmap 时仍需要对**数据缓冲区**做 flush，以确保数据在 draw 触发前可见。
- 持久一致性缓冲区（persistent coherent buffer）是现代 GL 的推荐方案，适合 UBO，尤其在 Windows 上效果好。
- 延迟所有 state change + draw call（Supnik 在 X-Plane 里的实际做法）适用范围更广，但需要封装整个绘制 API，不适合大型脚印的代码库。
- Supnik 的附注：在不支持持久缓冲区的情况下，**不应使用 UBO**——每 draw 冲刷成本极高，反而不如 loose uniforms（驱动对后者有多年专项优化）。

## 链接到的概念

- [[opengl-gl-command-buffer-flush]]
- [[glbuffersubdata-serialization]]
- [[opengl-pinned-memory-vbo-streaming]]
- [[gl-draw-accumulator-batching]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2018/01/flush-less-often.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2018-01-29_flush-less-often.md`
