---
tags: [渲染, gpu, 同步, 图形api]
date: 2026-04-14
sources: 1
---

# GPU Hazard Tracking（自动危险追踪）

**Hazard tracking** 指图形驱动自动检测"同一资源被一个 pass 写、另一个 pass 读"这种顺序依赖，然后插入同步或禁止并行，从而保证正确性。OpenGL 和 Direct3D 11 时代全部由驱动兜底，D3D12 与 Vulkan 则把这件事交还给应用程序。Metal 保留了一种 *optional* 的自动追踪（`MTLHazardTrackingMode`），作为便利出口。

## 它要解决的问题

GPU 并行执行 draw call、pass、甚至多个 queue。如果 pass A 把内容写进某张 render target，pass B 把它作为 texture 采样，那么二者必须按顺序跑，否则 B 读到的内容未定义。驱动要么追踪每个 texture、render target 的"当前归属"并在必要处插 barrier，要么要求用户自己来做这件事。

## D3D11 / OpenGL 路线

驱动维护一份"谁现在正在使用每个资源"的台账，每次切换 render target 或绑定 texture 时交叉比对前面的 pass，推断是否需要等待。因为追踪粒度不可能做到逐字节（太贵），只能用相对粗的 granularity，结果就是**误报率偏高**：两个理论上可以并行的 pass 被驱动保守地串起来跑。类比：CPU 侧用 8MB chunk 粒度追踪内存依赖，只要两个 job 碰巧落到同一个 8MB 区间就判为冲突。

## D3D12 / Vulkan 路线

移除自动追踪，改为让用户显式声明 **barrier**：
"把这张 texture 从 `RENDER_TARGET` 转成 `SHADER_READ_ONLY`"、"把这块 buffer 从 copy 目的地转成 vertex buffer"。barrier 同时承担三件事：

1. **顺序同步**：告诉 GPU pass X 必须在 pass Y 前跑完。
2. **缓存刷新**：GPU 内的 L1/L2/color-cache 必须在资源"交棒"前清掉。
3. **布局转换**（仅 Vulkan）：[image layout](https://registry.khronos.org/vulkan/specs/1.3-extensions/man/html/VkImageLayout.html) 从 `COLOR_ATTACHMENT_OPTIMAL` 转成 `SHADER_READ_ONLY_OPTIMAL`，因为两种用途对内存排布的需求不同。

这对应用程序来说当然更复杂，但它开启了几个关键能力：**multi-threaded 命令录制、multi-queue、bindless、indirect draw**——这些都很难或无法在自动追踪框架里正确表达。Jasper St. Pierre 在《How to write a renderer》一文里强调，这正是 D3D12/Vulkan "看起来复杂"的真正动因。

## Metal 的折中

Metal 允许在资源上设 `trackingMode = tracked` 来恢复 D3D11 风格的自动追踪。这让新手好上手，但使用 argument buffer（Metal 的 bindless 机制）之类的新特性时必须切回 `untracked` 模式，也会把可能的 false positive 带回来。

## 实现上的常见陷阱：over-barriering

手写 barrier 时容易**保守过度**——每个 draw call 前都插 full barrier。这会把 GPU 的并行度彻底杀死。[[render-graph]] / FrameGraph / AMD RPS 之类的框架把 barrier 插入做成声明式工具，原因之一就是**减少 over-barrier 带来的 GPU 性能损失**。AMD 团队提到，把游戏切到 RPS 之后 over-barrier 下降，GPU 端性能整体提升。

## 与资源状态跟踪的关系

[[d3d12-resource-binding]] 里的 `ResourceStateTracker` 是同一问题在单引擎层的朴素实现：多线程录制命令列表时，局部状态就地记录，全局状态留到 `ExecuteCommandLists` 时一次性回填。这是"自己做 hazard tracking"的最小工程形态。

## 相关

- [[d3d12-resource-binding]]
- [[render-graph]]
- [[draw-call]]
- [[gpu-fence-timeline-semaphore]]
- [[rendering-api-depth]]

## Sources

- [[sources/jasper-how-to-write-a-renderer]]
