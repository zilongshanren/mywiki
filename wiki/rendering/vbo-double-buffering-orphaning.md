---
tags: [渲染, opengl, vbo, 驱动, 同步]
date: 2026-04-19
sources: 1
---

# VBO Double-Buffering / Orphaning（VBO 双缓冲与 orphan 写法）

**场景**：每帧都要重写一次 vertex buffer（动态骨骼蒙皮结果、粒子几何、UI 网格……），然后多次 draw。朴素写法就是 `glMapBuffer → 写 → Unmap → glDrawArrays`。PCIe 带宽并不小，但性能却很差——原因不是带宽，是**同步**。

## 锁从哪来

`glMapBuffer` 本质上是在申请一把 mutex，这把锁被 CPU 和 GPU 轮流持有。GPU 从 draw call issue 到 draw 真正完成的整段时间里都握着锁。当管线允许 GPU「落后」一两帧时（参见 [[agp-vs-vram-streaming]]、[[gpu-latency-hiding]]），CPU 想写下一帧的 VBO 时必然撞锁。锁之所以存在，是因为两种可能的内存布局：

- **AGP 布局**：VBO 在 system RAM 里、通过 GART 同时映射到 GPU 和 CPU——只有一份物理内存，CPU 写就会影响 GPU 读。
- **VRAM 布局**：VBO 在 VRAM 里，system RAM 只是 driver 的备份副本（相当于 D3D 的 managed 资源）。

不管哪种布局，只要物理位置只有一份「活」的拷贝，CPU 就只能等。

## 双缓冲：驱动层的解法

D3D 的 `D3DLOCK_DISCARD` 告诉驱动「我要从头改写整个 buffer」。驱动收到这个暗示就不等老 draw 了——它**给你一块新内存**让你填，旧那块挂在老 draw 上自生自灭，完事后回收。应用层逻辑上还是同一个 buffer，物理上已经悄悄 [[buffer-renaming|renaming]] 过了。这就是双缓冲。

OpenGL 里对应两种写法：

1. **orphaning**（经典）：写之前先 `glBufferData(target, size, NULL, usage)`——告诉驱动旧内容可以扔，按 `DiscardAndMapBuffer` 语义走（VBO 扩展 spec 明确承认这个幻术）。然后 `glMapBuffer` 拿到的就是新块。
2. **`GL_MAP_INVALIDATE_BUFFER_BIT`**（GL 3.0 / `ARB_map_buffer_range`）：直接用 flag 表达意图，比 `glBufferData(NULL)` 更精准。

注意 orphan 会**整块**换新——如果你只想覆盖一半、保留另一半，orphan 就不合适，要用 `GL_MAP_UNSYNCHRONIZED_BIT` + 自己用 [[gpu-fence-timeline-semaphore|fence]] 管理（参见 [[glbuffersubdata-serialization]]）。

## 手动半缓冲：只用一块但仔细切

Supnik 在第二篇中补了一笔：用 manual sync（`UNSYNCHRONIZED` + 自己保证不覆盖未完成的 draw）可以只用一块 buffer，每帧用其中一半。代价是**非常小心**——一旦写到 GPU 正在读的那半区，就是未定义行为。

## APPLE_flush_buffer_range 的早期解

Supnik 文中提到 MacOS 10.4.7 已经通过 `APPLE_flush_buffer_range` 提供两个关键能力：

- `BUFFER_SERIALIZED_MODIFY_APPLE`：关闭 map 时的阻塞（客户端自己管同步）；
- `BUFFER_FLUSHING_UNMAP_APPLE`：unmap 时不把整个 buffer 的 cache line flush 掉，而是客户端明确告诉驱动「我只改了这几个 range」。PowerPC 上收益巨大（没有自动 cache coherency），x86 上也有中等收益。

这两个能力后来被整合进 GL 3.0 的 `glMapBufferRange`。

## 驱动的「系统内存镜像」权衡

评论区 Rob（map-buffer-range 合著者）补充：很多驱动的 VBO 同时在 client 侧镜像一份 system memory copy，让 read-only map 便宜。但这条策略在不同实现上表现差异极大——某些实现下 read-only map 会走 uncached memory，CPU 性能反而崩盘。X-Plane 最后放弃依赖这个镜像，**自己在关键路径多存一份 RAM 副本，并明确告诉 GL「别管了，让数据待在 VRAM」**。这是「驱动替你扛复杂性换不可预测性」的典型案例，呼应了 [[rendering-api-depth|深/浅 API]] 的讨论。

## 相关
- [[buffer-renaming]] —— 同一幻象在 CB/UBO 上的形态
- [[agp-vs-vram-streaming]]
- [[glbuffersubdata-serialization]]
- [[gpu-fence-timeline-semaphore]]
- [[frames-in-flight]]
- [[streaming-staging-texture-upload]]
- [[ben-supnik]]
- [[opengl-pinned-memory-vbo-streaming]] —— orphan-and-map 在 ATI 驱动上慢到 6 ms 时的替代方案
- [[bricksmith-instancing-pipeline]] —— instance 数据合并成一条 giant STREAM_DRAW buffer 的实际设计
- [[streaming-quads-drawing-strategies]] —— 2D quad 每帧流式 VBO 的路线讨论

## Sources
- [[sources/supnik-double-buffering-vbos]]
- [[sources/supnik-vbo-really-double-buffered]] —— Supnik 用「如果是我写 driver」的视角重新整理了前三篇的结论
