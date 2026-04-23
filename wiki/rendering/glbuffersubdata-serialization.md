---
tags: [渲染, opengl, vbo, 同步, 驱动]
date: 2026-04-19
sources: 1
---

# glBufferSubData 的串行化陷阱

**症状**：用 `glBufferSubData` 轮流填一个 VBO 的左右两半、每半填完立刻 draw，性能远比想象差。本来指望两半互不干扰、可以并发，结果每次 SubData 都阻塞直到上一次 draw 完成。Ben Supnik 2010 年这篇小结给出驱动端的推理。

## 为什么驱动必须串行化

假设 VBO 在 AGP / system memory（[[agp-vs-vram-streaming|流式几何的常见落点]]），前一次 draw 还在 pipe 里没跑完时，你就要 SubData 覆盖它：

- 如果驱动让你直接写——GPU 可能会读到一半旧一半新的顶点，画面爆炸。
- 正确处理必须知道 **待 draw 的 range** 和 **你要写的 range** 是否相交。

理论上驱动可以精确算交集，但实践上做不到：

1. `glDrawElements` 的实际读取 range 由 index buffer 决定，要判断得扫一遍所有 index——治病比病还贵。任何清醒的驱动都保守假设「整个 VBO 都可能被用」。
2. 即使你改用 `glDrawRangeElements` 明确告诉驱动 range，驱动还是得为每个 VBO 维护一个「哪些区段还 pending」的动态结构，替换本来简单的时间戳锁。对所有 VBO 都付这代价不划算。

结论：SubData 在有 pending draw 时**必然等**。这是保守但合理的实现。

## 正确姿势：orphan 或精确 map

两条出路：

- **Orphan**（参见 [[vbo-double-buffering-orphaning]]）：整块换新，让老 buffer 跟着老 draw 一起退休。
- **精确 map**：用 `GL_MAP_UNSYNCHRONIZED_BIT`（GL 3.0 `glMapBufferRange`）或 `APPLE_flush_buffer_range`——告诉驱动「我自己保证不写进 pending 区段」，拿到一块无锁的 map 直接写想写的范围，再用 `FlushMappedBufferRange` 发出 dirty 标记。

两种方式的本质都是把「会不会冲突」的判断从驱动挪回应用。

## Ring buffer 模式（Rob Barris 评论）

评论区 Rob 给出他们（OpenGL 大厂 codebase）的实际做法，和 D3D 的 dynamic buffer 策略同构：

1. 开一块 2~4 MB 的 VBO 当 ring；
2. 维护一个 **递增 cursor**；
3. 每个 batch 从 cursor 往后拿一段写、draw、cursor 前进；
4. cursor 撞到 buffer 尾部时，orphan 一次（申请新块），cursor 归零。

只要工作负载是**纯追加写**（batch 写完不再回头修改），`map/write/unmap` 事件数和 orphan 事件数可以达到 **100:1** 以上——即绝大多数 map 都是 unsynchronized 的便宜操作，只有极少数（ring 满了）付一次 orphan 代价。**完全不需要 fence**，orphan 本身就是同步点。

仅当你**想原地回改已写入的数据**时，才需要显式 [[gpu-fence-timeline-semaphore|fence]]——用 fence 等到相关 draw 完成再改。

## 为什么 MapBufferRange 存在：SubData 的另一条死路

Rob 补充了一个不常被提到的动机：**SubData 假设源数据已经是可 memcpy 的形态**。如果 CPU 是从压缩 / 打包形式展开出来（例如 WoW 的 heightfield terrain 解码），SubData 要求先展到一个临时 buffer 再 SubData 拷走——污染 L1/L2 cache。`glMapBufferRange` 允许把展开直接写进 VBO 映射的 AGP 页，避免这次多余的拷贝。这和 [[streaming-staging-texture-upload]] 里 staging ring 的动机一致。

## 相关
- [[vbo-double-buffering-orphaning]]
- [[agp-vs-vram-streaming]]
- [[buffer-renaming]]
- [[gpu-fence-timeline-semaphore]]
- [[streaming-staging-texture-upload]]
- [[frames-in-flight]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-glbuffersubdata]]
