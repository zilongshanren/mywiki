---
tags: [渲染, gpu, 同步, vulkan, d3d12, 引擎抽象]
date: 2026-04-19
sources: 1
---

# 简化版 Pipeline Barrier 抽象

Vulkan 的 `vkCmdPipelineBarrier` 和 D3D12 Extended Barriers 都想让应用精确描述三件事：**哪些 pipeline stage 之间要排序**、**哪些 GPU cache 要失效**、**image 要在哪两种 layout 之间转换**。Vulkan 提供 25+ 个 stage flag 和 30+ 个 access flag。对大多数引擎来说这太多了——[[people/panagiotis-charitos|Charitos]] 在 AnKi 里做了一次"激进裁剪"，把它压成两个 enum，换来一些"可以忽略的"性能代价。

## 关键观察

### Stage 只需要 6 种

不管 Vulkan 列了多少 stage flag，PC/console 硬件真正能独立同步的大致是：

1. **Transfer**（copy）
2. **Compute**（dispatch、AS build、ray tracing 底层都走 compute，但某些硬件能单独调度 AS build 和 dispatch）
3. **Geometry**（vertex input 到 geometry shader，包含 task/mesh shader）
4. **Fragment**
5. **TraceRays**
6. **Build acceleration structures**

移动端稍微细一点：Arm 有 transfer/compute/geometry/fragment 四个 stage；Adreno 能把 binning 和 fragment 并行跑。Turnip 驱动保守地合并了很多 stage，所以实操里不用为它们再细分。

### Access flag 与 usage flag 可以合并

Access flag 很难映射到具体的 cache，而且硬件变了还不保真。AnKi 的做法是**把 access 和 buffer/image usage 一次性写进同一个 enum**，因为两者大部分位本来就能共享：

```cpp
enum class BufferUsageBit : U64 {
    kConstantGeometry,  kConstantPixel,  kConstantCompute,  kConstantTraceRays,
    kSrvGeometry,       kSrvPixel,       kSrvCompute,       kSrvTraceRays,
    kUavGeometry,       kUavPixel,       kUavCompute,       kUavTraceRays,
    kVertexOrIndex,
    kIndirectCompute,   kIndirectDraw,   kIndirectTraceRays,
    kCopySource,        kCopyDestination,
    kAccelerationStructureBuild,   kShaderBindingTable,
    kAccelerationStructureBuildScratch,
    // + kAll* 组合
};
```

同一套 enum 同时承担三职：**推导 Vulkan barrier stage**、**推导 access mask**、**推导 buffer usage flag**。Texture 的版本更简单（13 个 bit），多了 RTV/DSV 和 ShadingRate 两类。

插 barrier 就是填一个 `BufferBarrierInfo { bufferView, previousUsage, nextUsage }`——引擎再反推 Vulkan 的具体 flag。

## 被故意忽略的细节

### 精确 buffer range 用不上

AnKi 把所有 `VkBufferMemoryBarrier` 折成一次 `VkMemoryBarrier`。观察到：**没有驱动真的在乎 buffer offset+range**，给整内存做一次 barrier 对 PC/console 来说几乎免费。唯一代价：Mali 上某些情况下 `VkMemoryBarrier` 会顺带触发 texture cache flush——可接受的 tradeoff。

### 队列归属转换可省略

`VK_SHARING_MODE_EXCLUSIVE` 配 queue family ownership transfer 是 AMD（尤其 GCN 时代）独有的真实需求。看 RADV 现状 AMD 仍在乎一点点；但看 VKD3D 和 D3D12 本身——**D3D12 根本没有 queue ownership 概念**，游戏照跑。所以 AnKi 选择对所有可能跨队列的 image 一律 `VK_SHARING_MODE_CONCURRENT`，彻底消灭 ownership transfer 这类代码。

### Indirect 的小陷阱

`VK_ACCESS_INDIRECT_COMMAND_READ_BIT` 在 nVidia 上不能漏——漏掉会间歇性 hang。所以 indirect 作为独立 bit 保留在 enum 里（`kIndirectCompute/Draw/TraceRays`），不和 SRV 合并。

### Host access flag 砍掉

`VK_ACCESS_HOST_*` 在 srcAccessMask 里几乎没用（submit 本身就有隐含 barrier）；在 dstAccessMask 里规范要求，但几乎所有驱动在 submit 结束时都会顺便 flush。Mali 早年按规范办事所以 CTS 失败过，其他厂商都没事。D3D12 Extended Barriers 干脆不包含 host 位——AnKi 也不保留。

### Image layout 几乎无感

AMD RDNA2 之后 layout 几乎变成 no-op；nVidia 从来不在乎；Mali 新硬件有一点点影响。AnKi 除了 BC/ASTC/ETC（只有 UNDEFINED/GENERAL 两态）之外，仍然精确计算每张 texture 的最优 layout——几乎免费，却保留了移植到 Mali 的正确性。

## 代价

- 一次 `VkMemoryBarrier` 覆盖整个 buffer 空间——Mali 上可能带出一次 texture cache flush；
- 全 `CONCURRENT` 模式下 AMD 可能错失一点点 queue-family-exclusive 的优化；
- `kAllRead` / `kAllWrite` 组合出来的 barrier 偶尔会比手写的精确版多刷一次 cache。

总体 Charitos 认为这些都是"minor performance concession"。实现见 AnKi 的 [`CommandBuffer::setPipelineBarrier`](https://github.com/godlikepanos/anki-3d-engine/blob/master/AnKi/Gr/Vulkan/VkCommandBuffer.cpp)。

## 相关

- [[gpu-hazard-tracking]] —— 这一代 API 为什么把同步责任丢回给应用
- [[render-graph]] —— 另一类减轻 barrier 负担的上层抽象（在 pass 级别自动推导）
- [[d3d12-resource-binding]] —— 引擎里同样问题的局部实现
- [[async-compute]] —— queue ownership 讨论的主场景

## Sources

- [[sources/anki-simplified-pipeline-barriers]]
