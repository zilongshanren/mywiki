---
tags: [source, graphics, d3d12, gpu-memory]
date: 2026-04-19
sources: 1
---

# Secrets of Direct3D 12: Resource Alignment（Adam Sawicki）

[[adam-sawicki]] 发表于 2020 年 4 月的文章，把 D3D12 `CreatePlacedResource` 背后那套资源对齐规则一次讲清——为什么 small alignment 既不自动授予、还会触发 debug layer 误报，以及 heap 对齐也是个独立的第三层约束。

## 摘要

D3D12 建议用大内存块 + `CreatePlacedResource` 而不是每个资源独立 committed。摆放时需要满足该资源的大小与对齐。D3D12 的对齐值是硬编码常量（而非 Vulkan 那种驱动依赖值）：buffer 总是 64 KB；texture 默认 64 KB 但"小纹理"可降到 4 KB；MSAA 默认 4 MB 但小 MSAA 可到 64 KB。问题是 `GetResourceAllocationInfo` 永远不会主动给你小对齐——你必须显式把 `D3D12_RESOURCE_DESC::Alignment` 设成候选小值再调，授予就返回同值，不授予就返回 `(64KB, 0xFFFF..FF)` 这种哨兵。Microsoft 官方示例走"先试小再退默认"策略，但老版 SDK 会触发 debug layer 错误 #721。再叠一层：`ID3D12Heap` 自身的 `Alignment` 只能选 64 KB 或 4 MB，准备放 MSAA 必须选 4 MB。2025 年 Agility SDK 1.716.0-preview 的 Tight Alignment 终于放开了 buffer 的 64 KB 下限。

## 关键要点

- D3D12 对齐常量是平台固定值，不随 GPU / 驱动变；`D3D12_DEFAULT_RESOURCE_PLACEMENT_ALIGNMENT` 等。
- "Small alignment" 只适用于 `UNKNOWN` 布局、非 RT/DS 的纹理，且有像素数量阈值。
- `GetResourceAllocationInfo` 把输入 `Alignment = 0` 当作"给我默认值"——不会主动优化。
- 堆本身还有 `D3D12_HEAP_DESC::Alignment`（64 KB 或 4 MB），Vulkan 无对应概念。
- [[d3d12-memory-allocator]] 把这些 quirk 自动化。
- Tight Alignment（2025）是这篇文章 5 年后的续集。

## 链接到的概念

- [[d3d12-resource-alignment]]
- [[d3d12-memory-allocator]]
- [[vulkan-memory-allocation]]

## 原文

- 链接：https://asawicki.info/news_1726_secrets_of_direct3d_12_resource_alignment
- 本地：`raw/articles/asawicki.info/2020-04-19_secrets-of-direct3d-12-resource-alignment.md`
