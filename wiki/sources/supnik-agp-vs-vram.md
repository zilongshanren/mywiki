---
tags: [source, 渲染, opengl, gpu, 内存]
date: 2026-04-19
sources: 1
---

# Double-Buffering Part 2 — Why AGP Might Be Your Friend（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 2 月的续篇——前一篇推出了 orphan 写法，这篇推测「为什么告诉 GL 我要 stream draw 时驱动会把我放 AGP system memory 而不是 VRAM」，并给出直觉上的时序论证。

## 摘要

前提：现代 OpenGL 让 GPU 落后 CPU 一到两帧有好处——FIFO 长度缓冲 CPU/GPU 速度失配。双缓冲 AGP 路径每帧两步（fill on CPU、draw on GPU），锁冲突只可能在「GPU 落后超过 2 帧」的罕见情况下发生。切成 VRAM 路径多出一个 DMA 步骤：fill system RAM → DMA to VRAM → draw from VRAM，三步间的依赖链让 DMA 时机变得苛刻——早了 DMA 撞上一帧 draw，晚了下一帧 fill 撞上一帧 DMA，只有 driver 在 GPU 刚空出瞬间调度 DMA 才能勉强不卡。因此驱动对 `GL_STREAM_DRAW` 常选 AGP。反例是 streaming ratio 非 1:1 的工作负载——shadow map、env map、early-Z pre-pass 都让同一 VBO 每帧被 draw 多次，这时 VRAM 的 DMA 分摊就划算了。作者提醒：写 AGP 的 write-combined uncached memory 必须**线性大块写、不读、不乱序改**，否则性能崩。

## 关键要点

- GPU「落后 1-2 帧」是设计上的好事，拉长 FIFO 换调度弹性。
- AGP 双缓冲的时序宽松；VRAM 三步路径（fill/DMA/draw）时序窄。
- stream draw 默认落 AGP 是驱动的保守选择，多半对。
- `streaming ratio != 1:1`（多次 draw 同一帧数据）才让 VRAM 划算。
- AGP 写入必须迎合 write-combined 语义：线性、只写、不 read-modify-write。

## 链接到的概念

- [[agp-vs-vram-streaming]]
- [[vbo-double-buffering-orphaning]]
- [[gpu-latency-hiding]]
- [[frames-in-flight]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2010/02/double-buffering-part-2-why-agp-might.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-28_double-buffering-part-2-why-agp-might-be-your-friend.md`
