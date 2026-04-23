---
tags: [source, 渲染, opengl, vbo, 同步]
date: 2026-04-19
sources: 1
---

# One More On VBOs — glBufferSubData（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 2 月 VBO 三连的收尾，集中回答「为什么 `glBufferSubData` 也会阻塞」。

## 摘要

朴素写法：SubData 填 VBO 左半 → draw 左半 → SubData 填右半 → draw 右半。预期两半互不干扰，实际每次 SubData 都等上一次 draw 完成。原因在驱动实现的保守性：要让 SubData 不阻塞，驱动必须判断「你要写的 range 与 pending draw 读的 range 不相交」。`glDrawElements` 的真正读 range 由 index buffer 决定，扫 index 的代价比病本身更大；`glDrawRangeElements` 能告诉驱动一个上界，但维护「哪些段 pending」的动态结构要替换简单的时间戳锁，对所有 VBO 都付这代价不划算。任何清醒驱动保守假设「整个 VBO 都可能被读」，于是 SubData 必等。两条出路：整块 orphan（见 [[vbo-double-buffering-orphaning]]），或用 `ARB_map_buffer_range` / `APPLE_flush_buffer_range` 的 `UNSYNCHRONIZED` + `FlushMappedBufferRange` 自己负责 sync。评论区 Rob Barris（map-buffer-range 合著者）给出实战模板：ring buffer + 递增 cursor + 追加写 + 撞尾 orphan，map/write/unmap : orphan ≈ 100:1，纯追加场景下**完全不需要 fence**。fence 只在想原地改已写数据时才必要。Rob 还提到 SubData 另一个死点：它假设源数据已是可 memcpy 形态，遇到 CPU 解压/解码（如 WoW 地形高度场）必须先展到临时 buffer 再 SubData——污染 cache；MapBufferRange 允许直接写进 AGP 映射页，绕过这次拷贝。

## 关键要点

- SubData 保守等 pending draw，因为驱动不愿为所有 VBO 维护精确的 range 锁。
- `glDrawRangeElements` 理论上能救，但驱动不为它设计数据结构。
- Orphan = 整块换；`UNSYNCHRONIZED` + flush = 局部精确写（客户端自管同步）。
- Ring buffer + 追加写 + 撞尾 orphan 是 D3D/GL 通用的高命中模式。
- SubData 强制源数据可直接 memcpy，遇到解压/展开场景必然多一次 cache 污染拷贝。
- 纯追加 + 恰当 orphan 频率下，fence 非必需。

## 链接到的概念

- [[glbuffersubdata-serialization]]
- [[vbo-double-buffering-orphaning]]
- [[agp-vs-vram-streaming]]
- [[gpu-fence-timeline-semaphore]]
- [[streaming-staging-texture-upload]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2010/02/one-more-on-vbos-glbuffersubdata.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-28_one-more-on-vbos-glbuffersubdata.md`
