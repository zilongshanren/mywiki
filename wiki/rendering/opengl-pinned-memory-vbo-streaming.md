---
tags: [渲染, opengl, vbo, 驱动, 同步, 流式上传, amd]
date: 2026-04-19
sources: 1
---

# OpenGL Pinned Memory 与流式 VBO 上传

Ben Supnik 2012 年在 X-Plane 上排查过一个让人意外的性能差异：在 Windows 下 ATI Radeon HD 上推"每帧全新"的流式顶点时，**`glMapBuffer` 本身**就要吃 6 ms，同等负载下 NV GTX 580 几乎为 0。研究完才发现 [[vbo-double-buffering-orphaning|orphan-and-map]] 这条"让驱动替你做 FIFO"的路子，在不同驱动里代价差异极大——于是他换了一个 AMD 特有但效果明显的方案：**`GL_AMD_pinned_memory`**。

## 为什么 orphan 在 ATI 上慢

`glBufferData(NULL)` + `glMapBuffer` 让驱动动态提供一块"新的"后备内存，这背后理论上是一条 FIFO，深度取决于 GPU 落后几帧、SLI/CrossFire 有几张卡。假如 orphan 路径顺利，对 CPU 是无阻塞的。但"顺利"里隐藏着一堆潜在开销：

- 真要分新 buffer 就是一次内存分配；
- 新内存需要 VM 操作把 caching mode 改成 uncached / write-combined；
- 如果驱动想省地址空间，可能把 VBO 从 process 地址空间里 unmap 过，map 回来又一次 VM 操作；
- 驱动要自己 GC 浮游的 orphan buffer。

ATI 当时对这些路径没做激进优化，累积起来就是 6 ms。**更奇怪的是 `glMapBufferRange` + `GL_MAP_INVALIDATE_BUFFER_BIT` 反而更慢**——Supnik 发现必须同时带 `GL_MAP_UNSYNCHRONIZED_BIT`，否则 map 调用会阻塞等待待定 draw call 完成；GPU 落后越多阻塞越久，帧率直接腰斩。他认为"invalidate 明明会分新内存、根本不该等"是保守过头的驱动实现，但调用方带上 unsynchronized bit 就没代价。

## GL_AMD_pinned_memory：应用内存直接当 VBO

`GL_AMD_pinned_memory` 把一块**应用自己持有的、页对齐的内存**锁定为 VBO backing store——物理上仍在 system RAM 里，被 pin 住、设成 write-combined、通过 GART 给 GPU 看到。形态上就像老式 [VAR 扩展](http://www.opengl.org/registry/specs/NV/vertex_array_range.txt)：一块 AGP 风格的 buffer。关键是：

- **VBO 的存储就是你的指针本身**——VBO 生存期内不能 free 这块内存；
- 驱动替你设 write-combined，非页对齐会"壮观地失败"（含崩显卡驱动）；
- 因为 VBO = 你的指针，**根本不需要 map**——直接写内存地址即可，没有 lock 语义、没有 FIFO 判定。

代价对等：由于 VBO 永久占物理内存和地址空间，它只适合**总量可控的流式小数据**，不适合经常改但也常用的大型静态数据。

## 同步：应用自己排 ring

没有 map 就没有驱动给你的同步，所以要自己保证"GPU 还在读老数据时，不要覆盖写"。Supnik 采用了最简单的做法：把 pinned buffer 切成 **4 段**当环形队列，允许 CPU 领先 GPU 最多 4 帧。理想实现应该用 `glFence` 检测"环被吃满"事件、按需再追加一段 ring——因为 SLI / CrossFire 下 outstanding 帧数可能翻倍或更多。但在命中率极低的 worst case 上预留容量对所有用户都是浪费。

## 拷到 VRAM 还是直接画？

管线第二段是用 `glCopyBuffer` 把 pinned buffer 的内容异步"blit"到 VRAM 里的 `STATIC_DRAW` 目标 VBO。这是 **in-band 拷贝**——在 GPU 命中这条命令时才真正发生，不会阻塞后续 API 调用。但实测结果反直觉：对 X-Plane 的云粒子（每顶点**只用两次**、但 fill rate 极重），**跳过 copy 直接从 AGP 拉**更快——省去一次总线带宽往返，约快 0.5 ms。

## 对照 NVidia 的 GDC 2012 方案

同年 NVidia [GDC 方案](http://developer.nvidia.com/sites/default/files/akamai/gamedev/files/gdc12/Efficient_Buffer_Management_McDonald.pdf) 提倡的是：**应用层自建一个更大的 ring buffer，用 `MAP_UNSYNCHRONIZED | MAP_INVALIDATE_RANGE_BIT | MAP_WRITE` 映射一个子窗口**。好处是每批数据尺寸任意，驱动只管一个 buffer、可以做"先给你 scratch 内存，回头 DMA 合并写入"等优化。但这条路的 map/unmap 成本得靠驱动的 map 快速路径兜底——ATI 当时不满足这个前提，所以 Supnik 仍旧留在 pinned 方案上。

## 工程教训

Supnik 写下三条给自己：

1. **最快的 API 是不调用的 API**。排 pinned 方案的同时他顺手 profile 到 X-Plane 的 light/spill 流式管线 batch size 配错，每秒 5000 次 map——减 batch 数比换 API 更值。
2. **"驱动写得差"这种结论多半是错的**——OpenGL API 抽象层级比外人看起来高得多，驱动要在一个 API call 里穿很多层。正确的应对是**换调用方式**，不是在互联网上喊驱动作者偷懒。
3. **Orphaning 本质是让驱动帮你实现动态 FIFO**。这在 NV 驱动里便宜，在 ATI 不便宜——应用层能控制的东西（pinned ring / 应用自管子窗口），在驱动差异大的时代反而稳定。

## 相关

- [[vbo-double-buffering-orphaning]] —— orphan-and-map 的早期推导
- [[agp-vs-vram-streaming]] —— 两种 VBO 布局的带宽/同步权衡
- [[glbuffersubdata-serialization]]
- [[buffer-renaming]]
- [[ring-buffer-virtual-stream]]
- [[streaming-staging-texture-upload]]
- [[gpu-fence-timeline-semaphore]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-beyond-glmapbuffer]]
