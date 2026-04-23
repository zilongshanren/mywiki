---
tags: [source, rendering, opengl, driver, streaming]
date: 2026-04-19
sources: 1
---

# glMapBuffer No Longer Cool（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015 年 6 月发表的一篇"自我反转帖"——五年前他说 `glBufferSubData` 不可能打过 map buffer，现在修了 X-Plane 的性能 bug 发现恰恰相反，因为桌面 GL 驱动早已运行在独立线程上。

## 摘要

多线程驱动架构下 `glMapBuffer` 必须阻塞 app 线程等驱动算出真实指针，而 `glBufferSubData` 是单向 API——可以完整 marshal 进命令 FIFO 让驱动线程晚点跑。所以在 NVIDIA / AMD（DX11-capable） / Intel 现行驱动上，对全量替换的 case，`glBufferSubData` 与 `glMapBuffer+orphan` 持平或更快；尤其在流式 UBO 场景（每 draw call 前更新小量数据）显著占优。代价是两次 memcpy——marshal 一次再真落库一次——小 UBO 无所谓，大几何就不划算。Supnik 把结论推广到"GL 多线程模型从根本上不友好，**应该用 Vulkan/Metal 重写后端**而不是继续打补丁"。评论区与 NVIDIA 工程师补充了 `GL_MAP_PERSISTENT_BIT` / `COHERENT_BIT` 的正确组合（别加 READ bit，否则会掉进慢内存）、AMD Catalyst 13-9 在 pre-DX11 GPU 上不可接受、Intel Iris Pro 上 `glBufferData` 反而更快等实测数据。

## 关键要点

- `glMapBuffer` 在 threaded driver 下会阻塞 app 线程同步到驱动线程
- `glBufferSubData` 单向 API，可以作为 in-band update 排队执行（DMA 或 renaming）
- 多一次 marshal 阶段的 memcpy，小数据可忽略
- 流式 UBO 是最严苛 case——UBO 更新速度 = draw call rate
- Attribute 代替 uniform 在 OS X 上 2× loose uniforms，其他平台波动
- `MAP_PERSISTENT + COHERENT + 避开 READ_BIT` 是 GL 上最接近 Vulkan 内存模型的路径
- GL 的 implicit flush 是多线程敌对的根因——spot fix 治不了根

## 链接到的概念

- [[glmapbuffer-threaded-driver-stall]]
- [[glbuffersubdata-in-band-streaming]]
- [[buffer-renaming]]
- [[vbo-double-buffering-orphaning]]
- [[opengl-pinned-memory-vbo-streaming]]
- [[vulkan-explicit-performance]]
- [[api-fast-path-design]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2015/06/glmapbuffer-no-longer-cool.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-06-18_glmapbuffer-no-longer-cool.md`
