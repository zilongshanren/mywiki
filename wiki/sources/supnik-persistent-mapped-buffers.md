---
tags: [source, rendering, opengl, vbo, streaming, driver]
date: 2026-04-27
sources: 1
---

# Never Map Again: Persistent Memory, System Memory, and Nothing In Between（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2018 年 5 月发表的文章，总结了 X-Plane 在适配 GL 4.x / Vulkan / Metal 三后端过程中，针对流式几何（streaming geometry）上传的最新结论：一种是 persistent mapped buffer，另一种是直接用 client arrays 走系统内存，中间的各种 VBO 方案反而都不如这两端。

## 摘要

Supnik 多年来写了大量 VBO / map buffer 相关博文，2018 年重访这个问题时得到了更简洁的答案。第一选择是 `GL_ARB_buffer_storage` 提供的 persistent mapped buffer：驱动一次性给出可常驻的内存指针，CPU 直接写入，无需任何 map/unmap 往返，也没有多上下文同步的麻烦，是多核友好的零开销路径。第二选择（在不支持 persistent map 的平台如 macOS 上）是 client arrays（系统内存直接传顶点）：实测对中小批次比 VBO+glMapBuffer 更快，原因在于驱动在 draw call 时能一次性知道所有信息（数据大小、格式、着色器用量、位置都是系统内存），可以选最优的传输方式（大块走 DMA、中等走 AGP 内存、极小的直接塞命令缓冲区）；更关键的是 client arrays 在单个上下文内是严格 FIFO 的，驱动只需要一个 ring buffer 做内存分配，而 VBO orphaning 则需要复杂的堆管理。一旦确定只使用这两种路径，unmap/flush 开销就彻底为零，客户端代码可以大幅简化，无需缓冲命令再重放。

## 关键要点

- `GL_ARB_buffer_storage` persistent map 是流式几何的最快路径，驱动完全退出数据传输环节
- macOS 不支持 persistent map，此时 client arrays 比 VBO+map 更快（中小批次实测）
- client arrays 快的原因：draw call 时信息完整 → 驱动选最优传输；严格 FIFO → ring buffer 分配比 VBO heap 分配更廉价
- VBO orphaning 在不同驱动代价悬殊，client arrays 则行为更可预期
- 只用这两条路径后，可以删去 unmap/flush 路径分支，客户端逻辑收敛

## 链接到的概念

- [[opengl-pinned-memory-vbo-streaming]]
- [[glmapbuffer-threaded-driver-stall]]
- [[vbo-double-buffering-orphaning]]
- [[buffer-renaming]]
- [[ring-buffer-virtual-stream]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2018/05/never-map-again-persistent-memory.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2018-05-21_never-map-again-persistent-memory-system-memory-and-nothing.md`
