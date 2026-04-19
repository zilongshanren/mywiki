---
tags: [source, 渲染, 同步, vulkan, d3d12]
date: 2026-04-19
sources: 1
---

# Simplified pipeline barriers（Panagiotis Charitos / anki3d.org）

[[people/panagiotis-charitos|Charitos]] 2025 年 2 月发的长文，完整讲清了 AnKi 如何把 Vulkan 的 25+ pipeline stage、30+ access flag、N 种 image layout 的同步 API 压缩成两个 enum。对想做引擎级 barrier 抽象的人几乎是一篇"实操 ADR"。

## 摘要

Vulkan/D3D12 的 barrier 细粒度设计初衷是未来兼容与极限性能，但工程上大多数团队既吃不下也用不上。Charitos 把 Vulkan 能区分同步的 stage 砍到 6 种（transfer / compute / geometry / fragment / traceRays / AS build），把 buffer 和 image 的 usage + access 合并成一个 `BufferUsageBit` / `TextureUsageBit` enum，让 barrier API 退化成 `{ view, previousUsage, nextUsage }` 三元组。代价是：`VkMemoryBarrier` 代替精确范围（Mali 上会顺带 flush texture cache）、全部 `VK_SHARING_MODE_CONCURRENT` 绕过 queue ownership（AMD 损失一点 exclusive 优化）、host access flag 全砍掉（现实里没人真 care）。indirect 作为独立 bit 保留（nVidia 漏掉会 hang），layout 仍精确计算（对 Mali/AMD 新硬件有微小收益）。作者还做了一份 Vulkan↔D3D12 Extended Barriers 对照表，说明这套思路同样适用于 D3D12。

## 关键要点

- **6 个 stage 就够**：transfer/compute/geometry/fragment/traceRays/AS-build。
- **access + usage 合一**：同一个 enum 同时推导 barrier stage、access mask、buffer/image usage flag。
- **buffer 精确 range 基本没人关心**；`VkMemoryBarrier` 全覆盖。
- **queue family ownership transfer 可以砍**，代价是 AMD 小损失，收益是消灭一大坨代码复杂度。D3D12 根本没这概念。
- **`VK_ACCESS_INDIRECT_COMMAND_READ_BIT` 不能漏**，nVidia 会间歇性 hang；所以 indirect 单列 bit。
- **Host access flag 无用**，Mali 早年按规范扣分，其他厂都不在乎。D3D12 干脆不要。
- **Image layout** 在 AMD/nVidia 近代硬件上近乎 no-op，但 Mali 新硬件还在乎——AnKi 保留精确计算。BC/ASTC/ETC 压缩纹理只用 UNDEFINED/GENERAL。
- Vulkan barrier 概念直接映射 D3D12 Extended Barriers（DX12 Agility SDK 之后）：`VkPipelineStageFlagBits`↔`D3D12_BARRIER_SYNC`、`VkAccessFlags`↔`D3D12_BARRIER_ACCESS`、`VkImageLayout`↔`D3D12_BARRIER_LAYOUT`。
- 代码参考：`AnKi/Gr/Vulkan/VkCommandBuffer.cpp::setPipelineBarrier`。

## 链接到的概念

- [[simplified-pipeline-barriers]]
- [[gpu-hazard-tracking]]
- [[render-graph]]
- [[async-compute]]
- [[d3d12-resource-binding]]

## 原文

- 链接：https://anki3d.org/simplified-pipeline-barriers/
- 本地：`raw/articles/anki3d.org/2025-02-04_simplified-pipeline-barriers.md`
