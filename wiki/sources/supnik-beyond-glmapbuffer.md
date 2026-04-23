---
tags: [source, 渲染, opengl, vbo, amd, 性能, 驱动]
date: 2026-04-19
sources: 1
---

# Beyond glMapBuffer（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2012-04-04 的一篇硬核 OpenGL 性能排查文——X-Plane 的流式顶点（雨滴、车灯、云 index buffer）在 Windows 下 ATI Radeon HD 上比 NV 慢几 ms，最后靠 **`GL_AMD_pinned_memory`** 绕开 `glMapBuffer` 开销。

## 摘要

X-Plane 的 streaming VBO 管线用"orphan-and-map"：每帧先 `glBufferData(NULL)` 废弃旧内容、再 `glMapBuffer(WRITE)` 拿新块。理论上 CPU 非阻塞。但 i5-2500 + Radeon 7970 实测 100k 粒子云：sort 2 ms、**map 6 ms、write 1 ms、draw 1 ms**；同场景 GTX 580 是 sort 2 ms、其余几乎为 0。8 ms 全被 map 吃掉。Supnik 推断 ATI 驱动在 orphan 路径上走了保守路线——真分新 buffer（memory alloc + VM op 设 write-combined）、追踪老 buffer 的 command stream 状态、GC 浮游 orphan，每一步都不便宜。

尝试换 `glMapBufferRange` + `GL_MAP_INVALIDATE_BUFFER_BIT` 反而更慢——ATI 实现下必须**额外加** `GL_MAP_UNSYNCHRONIZED_BIT` 才能避免阻塞等 pending draw。加上后性能回到 orphan-and-map 水平。

真正的突破是 `GL_AMD_pinned_memory`：把一块页对齐的应用内存 pin 住、设 write-combined、通过 GART 映射给 GPU 看——VBO 的 backing store 就是这块指针本身，**完全不需要 map**。代价：内存永久占住（不适合大而稀少修改的 buffer），且驱动不再替你同步——Supnik 把 buffer 切 4 段当 ring，理想实现应该用 `glFence` 按需扩 ring。改造后 draw+sort 回落到 3 ms 左右，省 6-7 ms。

他还试了 `glCopyBuffer` 把 pinned AGP buffer blit 到 VRAM 静态 VBO。但云粒子 fill rate 重、每 vertex 用两次，实测**直接从 AGP 画更快**（省一次总线往返），copy 反而多 0.5 ms。

附带他顺手 profile 到 streaming light 的 batch 配小了（5000 次 map/s），**减 batch 数比换 API 更值**。最后对比 NVidia GDC 2012 [Efficient Buffer Management](http://developer.nvidia.com/sites/default/files/akamai/gamedev/files/gdc12/Efficient_Buffer_Management_McDonald.pdf)——用应用自建大 ring + 子窗口 + `MAP_UNSYNCHRONIZED | MAP_INVALIDATE_RANGE | MAP_WRITE`。这条在 NV 快、在 ATI 不快（仍然 map/unmap 成本高）。Supnik 留在 pinned 方案。

## 关键要点

- **orphan-and-map 不是"零成本"**——它要求驱动实现动态 FIFO，代价随驱动实现剧烈变化。
- **ATI 的 `glMapBufferRange` 默认会阻塞**——必须主动加 `GL_MAP_UNSYNCHRONIZED_BIT`，否则比 `glBufferData(NULL)` + `glMapBuffer` 更慢。
- **`GL_AMD_pinned_memory` 是 AGP/VAR 精神的回归**——应用内存直接当 VBO、跳过 map、自管同步。
- **pinned buffer 必须页对齐**——不对齐会崩显卡驱动。
- **应用层 ring buffer 要解决"环被吃满"**——理想用 `glFence` 按需扩环，worst case SLI/CrossFire 下 outstanding 帧数会翻倍。
- **直接从 AGP 画 vs 先 copy 到 VRAM**——fill rate 重 + vertex 复用次数低时，AGP 直取更快。
- **"最快的 API 是不调用"**——调 profile 时发现 batch 配小产生 5000 次/s map，减 batch 数胜过任何 API 技巧。
- **驱动不是懒，是抽象层太高**——Supnik 的元评论：OpenGL 看似低层，实际驱动路径非常多层、碰到慢 API 换调用方式比骂驱动更有效。

## 链接到的概念

- [[opengl-pinned-memory-vbo-streaming]]
- [[vbo-double-buffering-orphaning]]
- [[agp-vs-vram-streaming]]
- [[ring-buffer-virtual-stream]]
- [[buffer-renaming]]
- [[glbuffersubdata-serialization]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2012/04/beyond-glmapbuffer.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2012-04-04_beyond-glmapbuffer.md`
