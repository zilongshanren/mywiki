---
tags: [渲染, gpu, 驱动, 图形api]
date: 2026-04-14
sources: 1
---

# Buffer Renaming（缓冲区改名）

**Buffer renaming** 是 Direct3D 8 / OpenGL / Direct3D 11 时代图形驱动的一种隐式优化：应用程序在两次 draw call 之间对同一个 buffer（vertex buffer、constant buffer 等）写入新数据，驱动察觉 buffer 此刻还被之前的 draw call 引用，就**偷偷分配一块新的显存**，把旧内容拷过去，再把应用层的 handle 指向新块。应用感知不到，draw call A 读到旧内容，draw call B 读到新内容，"buffer 可以在用着的时候被更新"这个幻象就是这样维持的。

## 为什么要有这套魔法

老一代 API 允许应用"随时更新 buffer"。GPU 的真实约束是：一段正在被 in-flight draw call 读的内存如果被 CPU 重写，读回的内容未定义。驱动必须在下面三种方案里选一种：

1. **stall**：CPU 阻塞，等 GPU 读完。帧率杀手。
2. **rename**：新分一块，旧块留给还没跑完的 draw call。延迟 0，代价是显存碎片与分配压力。
3. **硬件 versioning**：非常老的 GPU 用过，现代 GPU 早已放弃。

## OpenGL 里的"buffer orphaning"

OpenGL 把这件事外包给了应用层的"暗示"：`glBufferData` 的 usage flag（`GL_STATIC_DRAW` / `GL_DYNAMIC_DRAW`）原本是希望驱动按这个暗示选 stall 或 rename，但实践中不同驱动解读不一致，很多 OpenGL 应用干脆养成了 **"buffer orphaning"** 的迷信操作：在写入前先 `glBufferData(size, NULL, ...)` 一次把整个 buffer 的内容"废弃"，强制驱动按 rename 路径走。这是 [Khronos wiki](https://www.khronos.org/opengl/wiki/Buffer_Object_Streaming) 明确推荐过的。

## Constant buffer 是 renaming 的重灾区

Vertex buffer 的更新相对稀疏，真正每帧都高频变的是 [[d3d12-resource-binding|constant buffer]]（D3D 术语）/ uniform buffer（GL 术语）——几乎每个对象、每个 draw call 都要换一次 per-object uniforms（世界矩阵、材质参数）。如果驱动不会 renaming，每次更新都 stall，那 GPU 基本就闲置了。因此驱动里的 renaming 对 constant buffer 尤其激进。

## 现代 API 把责任还给你

Vulkan / D3D12 / Metal 直接取消了 renaming 幻象：**你不能在 buffer 仍被 in-flight draw call 读时写它**。应用必须自己：

- 准备足量的 buffer 副本（例如每个 in-flight 帧一份，或每个 draw 一份），
- 用 [[gpu-fence-timeline-semaphore|fence / timeline semaphore]] 判断何时可复用，
- 小改动通过 **push constants**（Vulkan）/ **root constants**（D3D12）直接塞进 command list，绕过 buffer。

Jasper St. Pierre 给新手的建议是：**把整帧 uniform 数据打包进一个 [[linear-allocator|线性分配器]]，帧首一次性上传，每个 draw call 用 dynamic offset 取子区段**。这样把 renaming 这件事集中成一次上传、一次 fence tick，远比"每次 draw 都 rename"的代价可控。

## 历史意义

Buffer renaming 是一个典型的"驱动替你扛复杂性，代价是性能不可预测"的例子。它在 [[rendering-api-depth|深/浅 API 对比]] 里站的是深模块一侧——接口很简单（"写就行了"），实现非常复杂。Vulkan/D3D12 拆掉这层深模块的决定把复杂性前置到应用层，换来可预测性。

## 相关
- [[gpu-fence-timeline-semaphore]]
- [[gpu-hazard-tracking]]
- [[d3d12-resource-binding]]
- [[linear-allocator]]
- [[rendering-api-depth]]
- [[streaming-staging-texture-upload]] —— 显式 API 下自己做的 staging ring
- [[frames-in-flight]]
- [[vbo-double-buffering-orphaning]] —— Ben Supnik 2010 年从 OpenGL 应用端视角对 orphaning 的推导
- [[glbuffersubdata-serialization]] —— SubData 为什么必然与 in-flight draw 串行化
- [[agp-vs-vram-streaming]] —— 流式几何为什么驱动经常把你放进 AGP/system memory 而不是 VRAM

## Sources

- [[sources/jasper-how-to-write-a-renderer]]
