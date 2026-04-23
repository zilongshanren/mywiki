---
tags: [渲染, 性能, gpu]
date: 2026-04-05
sources: 2
---

# Draw Call

**CPU 向 GPU 发送的绘制命令**。它的真实成本不在 GPU 执行，而在 **CPU 侧的状态 setup 与驱动验证**。

## 为什么 Draw Call 贵

每一次 DrawCall 需要：
- 验证 pipeline state（shader、blend、depth、stencil）
- 绑定 vertex buffer / index buffer / textures / constant buffers
- 可能 flush GPU pipeline（状态切换时）
- 驱动在 CPU 侧做参数转换与命令封装

**主成本在 CPU，不在 GPU 执行**。

## 典型预算

- 中端 Android 在 200-300 DrawCall 就开始成为瓶颈。
- 桌面端 DX12/Vulkan 由于更薄的驱动，可以到几千。
- PS5/Xbox Series X 可以再高。

## 降 DrawCall 的手段

- **[[batching|批处理]]**：把多个对象合并成一个 mesh / 一次绘制。
- **GPU Instancing**：同一个 mesh 多个副本在一次 DrawCall 画完——真正减少 DrawCall 数量。
- **SRP Batcher**（Unity）：用持久化 Constant Buffer 减少**状态 setup 开销**（不减少 DrawCall 数量）。
- **Texture Atlas**：合并纹理避免纹理切换引起的 DrawCall 拆分。
- **GPU-Driven Rendering**（Nanite 等）：把决策全推给 GPU，DrawCall 接近 O(1)。

## Vulkan/Metal 的价值

移动端 Vulkan/Metal 的价值是**降低 CPU driver overhead**，不是 GPU 更快。

具体 Metal 对象模型见 [[metal-api-overview]]——command queue / command buffer / command encoder 这一套就是显式 API 共通的 CPU 侧成本下压机制。

## 相关
- [[rendering-pipeline]]
- [[batching]]
- [[bottleneck-analysis]]
- [[draw-call|SRP Batcher 相关见 Custom SRP 系列]]
- [[d3d12-resource-binding]] —— D3D12 里 draw call 前的 descriptor / barrier 对齐开销
- [[gpu-hazard-tracking]] —— 为什么 D3D12/Vulkan 要求你自己声明 barrier
- [[buffer-renaming]] —— 老驱动的隐式魔法与 D3D12/Vulkan 的显式化
- [[draw-procedural-gpu]] —— 把一次 draw call 打到极致：CPU 只发命令，vertex 数据全部由 GPU buffer 提供
- [[metal-api-overview]] —— iOS 上降 CPU 驱动开销的显式 API
- [[opengl-draw-call-batching-sweet-spot]] —— Outerra 实测：per-instance 5k-20k 三角形是跨厂吞吐甜点
- [[triangle-strips-vs-indexed-triangles]] — 为减小 VRAM 中的 index buffer 而增加 CPU 调用是反向优化

## Sources
- [[sources/rtr-day02]]
- [[sources/rtr-day06]]
- [[sources/aras-blender-vse-image-filtering]]
- [[sources/jasper-how-to-write-a-renderer]]
- [[sources/outerra-opengl-perf-grass]]
- [[sources/outerra-opengl-perf-blocks]]
