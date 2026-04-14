---
tags: [渲染, gpu, 同步, 图形api]
date: 2026-04-14
sources: 1
---

# GPU Fence 与 Timeline Semaphore

**Fence**（Direct3D 12 术语）/ **Timeline semaphore**（Vulkan 术语）是现代图形 API 暴露出的 GPU→CPU 单向计数器：GPU 每完成一段工作就往某个共享内存位写一个单调递增的 integer，CPU 随时可读。用它可以廉价地回答一个在 [[rendering-api-depth|显式 API]] 时代每帧都会反复出现的问题——**这块 buffer 现在还在 GPU 手里吗？**

## 为什么必要

D3D11 / OpenGL 时代，驱动用 buffer renaming、copy、stall 等隐式手段替你解决"buffer 正在被 draw call 用，能不能写新数据"的问题（见 [[buffer-renaming]]）。Vulkan / D3D12 把这块的 magic 全部拿走：**你不能在一个 buffer 还被 in-flight draw call 读的时候往里写东西**，否则行为未定义。于是你需要一个廉价的"in-flight 还是闲置"的判定机制。

## 工作方式

1. CPU 维护一个单调递增的 `frameIndex`。
2. 每帧提交所有 command list / queue submit 之后，CPU 调用 `ID3D12CommandQueue::Signal(fence, frameIndex)` 或 `vkQueueSubmit2` 带上 timeline semaphore 信号值。
3. GPU 跑完这一帧的所有工作之后，把 `frameIndex` 的值写进 fence 指向的那个内存位。
4. CPU 想判断"某个 buffer 上次使用是第 63 帧，现在用得上吗？"就读 fence 的当前值，只要 ≥ 63 就可以安全复用。

这个机制同时给了你**轮询**和**阻塞等待**两种 API（`ID3D12Fence::SetEventOnCompletion` 触发 Win32 event；`vkWaitSemaphores` 阻塞线程），因而也是**帧 pacing**、**CPU-GPU frame pipelining**、**资源回收**、**异步 compute 之间的跨队列同步**的基础设施。

## 与 binary semaphore 的差别

Vulkan 1.0 最初只提供二元 semaphore（signaled / unsignaled），同一个对象不能表达顺序——第二次 signal 必须等别人 wait 一次才能再次用。timeline semaphore（Vulkan 1.2 核心化）把它变成 integer counter，可以 signal 得比 wait 快、可以被多个等待方同时比较、可以做跨进程传递。这和 D3D12 自开始就用的 fence 概念在语义上对齐了。

## 典型用法：frames-in-flight + ring buffer

与 [[linear-allocator]] 结合：上传堆按"每帧一段"切分，帧 N 写入第 N%K 段（K 是 in-flight 帧数，常见 2 或 3）。提交前在 fence 上 signal `N`，当 CPU 要开始帧 `N+K` 时就等待 fence ≥ `N`，从而保证帧 N 的上传段已被 GPU 读完。这是 [[d3d12-resource-binding|D3D12 资源绑定]] 里 `UploadBuffer` 的核心节奏。

## 和 draw call 结构的耦合

Jasper St. Pierre 在《How to write a renderer》里建议"把所有数据上传集中到帧首"，这个建议看似是组织方式，其实是 fence 直接驱动的：**只有把同一帧内所有写入都 pin 到一个 fence 值上，生命周期才干净**。零散地在 draw call 之间插上传，就不得不为每段数据单独追踪 fence 值，很快失控。

## 相关

- [[buffer-renaming]]
- [[gpu-hazard-tracking]]
- [[d3d12-resource-binding]]
- [[linear-allocator]]
- [[draw-call]]

## Sources

- [[sources/jasper-how-to-write-a-renderer]]
