---
tags: [d3d12, gpu-memory, resource-allocation, alignment]
date: 2026-04-19
sources: 1
---

# D3D12 资源对齐的坑

在 Direct3D 12 里把资源（纹理、缓冲）摆进堆（`ID3D12Heap`）时，必须同时满足"资源自身的对齐"与"堆本身的对齐"两层约束，Adam Sawicki 把这一层叠的规则称作 D3D12 的一个"秘密"。

## 默认对齐与"small alignment"

D3D12 把常量对齐直接写进了头文件，和具体 GPU / 驱动无关，这点与 [[vulkan-memory-allocation]] 的 `vkGetBufferMemoryRequirements` 返回值不同：

| 类型 | 默认 | Small |
|------|------|------|
| Buffer | 64 KB | — |
| Texture | 64 KB | 4 KB |
| MSAA texture | 4 MB | 64 KB |

Buffer 永远是 64 KB 起步；只有纹理有"小资源对齐"路径，而且定义相当绕：必须是 `UNKNOWN` 布局、且不能是 `RENDER_TARGET` / `DEPTH_STENCIL`，还要满足一个像素数阈值。

## GetResourceAllocationInfo 的古怪行为

同一个 `D3D12_RESOURCE_DESC::Alignment` 字段既是输入也是输出：

- 输入 `Alignment = 0` → 总是返回默认（较大）对齐，即便该纹理其实有资格走 small。
- 输入 `Alignment = small` → 如果授予则返回同值；不授予则返回 `Alignment = 64KB` 且 `SizeInBytes = 0xFFFFFFFFFFFFFFFF`（一个明显无效的哨兵），需要再跑一次默认路径。

Microsoft 的 "Small Resources Sample" 就用第二套策略——先试小的，失败再退默认。副作用是早期 D3D12 Debug Layer 会报 `CREATERESOURCE_INVALIDALIGNMENT` (#721)，某些较新 Windows / SDK 已修。

## Heap 本身的对齐

`D3D12_HEAP_DESC::Alignment` 只能取 64 KB 或 4 MB。只要该堆将来可能放 MSAA 纹理，就必须选 4 MB，Vulkan 没有这个字段的对应物。

## 后续发展

2025 年 DirectX 12 Agility SDK 1.716.0-preview 引入 **Tight Alignment**，移除了 buffer 的 64 KB 硬约束，相当于在设计 5 年之后才补上 Vulkan 早就有的灵活度——详见 Adam 的 [[asawicki-dx12-gdc-2026-comments]] 系列。

[[d3d12-memory-allocator]] 作为 Adam 主导的开源库，已经把上面所有的 quirk 自动处理掉，两种 small alignment 策略都用预处理宏切换。

## Sources

- [[sources/asawicki-d3d12-resource-alignment]]
