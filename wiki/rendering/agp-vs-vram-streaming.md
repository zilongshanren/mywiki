---
tags: [渲染, gpu, 内存, opengl, 驱动]
date: 2026-04-19
sources: 1
---

# AGP vs VRAM Streaming（流式几何为何常落在 AGP）

直觉说「VRAM wicked fast」，那么把动态 VBO 也放 VRAM、用 DMA 每帧推上去不就完事了？Ben Supnik 2010 年这篇笔记论证：**对于每帧重写一次的流式几何，AGP（system memory + GART）往往更好，不是 VRAM**。这是驱动在你标 `GL_STREAM_DRAW` 时常偷偷做的选择。

## 「GPU 落后」是好事

现代 OpenGL 实现让 GPU 落后 CPU 一帧甚至两帧——draw call issue 和 draw call 真正执行之间有个 FIFO。这个 FIFO 越长，CPU 和 GPU 短时间的速度失配越无所谓。只有四种情况会让 CPU 阻塞：

1. 吃满实现定义的 frame-ahead 上限（多半在 `SwapBuffers` 里睡）；
2. command buffer 内存耗尽；
3. 你查询 GPU 还没算完的东西（比如 occlusion query）；
4. 你尝试锁一个 GPU 还在读的资源（比如没 orphan 的 VBO map）。

FIFO 长度换来调度弹性——先画个占满屏幕的贵行星，再画一堆便宜房子，GPU 慢慢吃贵的那个时 CPU 已经提交完便宜的那堆。

## AGP 双缓冲的时序

假设 VBO 落在 AGP / system memory，每帧做两步：CPU 侧 `fill`（orphan map + 写 + unmap），GPU 侧 `draw`。每一步各取一次锁。若 driver 能给我们两块 buffer（orphan 的典型行为）：

- frame 3 的 fill 等 frame 1 的 draw；
- frame 4 的 fill 等 frame 2 的 draw；
- frame N 的 draw 总是等同帧的 fill。

也就是说 CPU 最多等「2 帧前的 draw」——按 FIFO 长度 1~2 帧的前提，这几乎不会真等到。

## VRAM 双缓冲的时序变糟了

如果目标是 VRAM，动作变三步：

1. `fill` system RAM 暂存；
2. `DMA` 从 system RAM 拷到 VRAM；
3. `draw` 从 VRAM 读。

三步间的依赖：`fill_N` 等 `DMA_(N-1)` 完成；`DMA_N` 等 `fill_N` 和 `draw_(N-1)` 完成；`draw_N` 等 `DMA_N` 完成。

考虑 DMA 发生的时机：

- **太早**（填完立即 DMA）：DMA 要等 frame N-1 draw 收尾——阻塞。
- **太晚**（刚好赶 draw 前）：填 frame N+1 的时候上一帧 DMA 还没做完——阻塞。
- **刚好**：driver 在 GPU 刚空出时立刻调度 DMA，勉强能不卡。

VRAM 路径的问题是 **DMA 同时需要两边都 available**，时序要求窄得多；AGP 路径只要锁两块 buffer，时序要求宽得多。因此驱动见到 `GL_STREAM_DRAW` 常把你放进 AGP。

## 反过来：什么情形下 VRAM 真赢

Supnik 举的最有力反例：**streaming ratio 不是 1:1**。每帧写一次 VBO，但画多次——env mapping、[[shadow-mapping-basics|shadow map]]、[[early-z-late-z|early Z pre-pass]] 都要把场景几何走多遍。AGP 意味着每次 draw 都拉 PCIe，VRAM 意味着 DMA 一次后 draw N 次本地读。draw-to-fill 比例越高，VRAM 越划算。

## 写 AGP 的工程小心

AGP 映射的 system memory 多半是 **write-combined, uncached**。正确写法：**线性大块写，绝不读，绝不乱序改**。任何 read-modify-write 模式都会被惩罚得极惨。这也是为什么 Supnik 在第三篇（[[glbuffersubdata-serialization]]）里强调 `glBufferSubData` 在 AGP VBO 上可能奇慢——驱动要先把你要覆盖的范围从 cache/buffer 里拉回来再写。

## 历史注脚

2010 年这篇的术语是 AGP / GART / system memory——现代（PCIe / Resizable BAR / Vulkan Memory Types）换了名字但底层权衡不变：`HOST_VISIBLE + DEVICE_LOCAL`（等价于 VRAM 直写）vs `HOST_VISIBLE + HOST_COHERENT`（等价于 AGP），流式几何仍然常落后者。

## 相关
- [[vbo-double-buffering-orphaning]]
- [[glbuffersubdata-serialization]]
- [[gpu-latency-hiding]]
- [[frames-in-flight]]
- [[streaming-staging-texture-upload]]
- [[virtual-memory]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-agp-vs-vram]]
