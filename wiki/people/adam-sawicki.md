---
tags: [人物, 作者, D3D12, Vulkan, GPU内存]
date: 2026-04-19
sources: 7
---

# Adam Sawicki

波兰图形程序员，博客 [asawicki.info](https://asawicki.info/)。**AMD D3D12 Memory Allocator（D3D12MA）** 与 **Vulkan Memory Allocator（VMA）** 两大开源库的作者，曾在 AMD GPUOpen 任职多年，专攻 DX12/Vulkan 低层内存与资源管理。2025 年起离开 AMD，加入小型游戏工作室 **Plastic**，视角从 IHV 转到应用端，博客风格也变得更敢说话（他自称"brutal honesty"）。

## 关注方向

- **D3D12 的角落与坑**：资源对齐、root signature、`ClearUnorderedAccessView` 行为、文档分散等"秘密"系列
- **GPU 内存分配器**：子块分配、碎片度量，见 [[a-metric-for-memory-fragmentation]]（2022）
- **小工具与数值**：系统级数学问题 + 交互式 demo，见 [[system-load-formula]]
- **GDC / Agility SDK 跟踪**：以应用端视角评注 Microsoft 每年的 DX12 公告，见 [[pix-api-and-dxdmp]]、[[dxr-tier-2-clas-ptlas]]、[[advanced-shader-delivery]]
- **图形 API 的历史与未来**：把 DirectX/OpenGL/Vulkan 的演进线写成面向初学者的科普，见 [[graphics-api-history]]
- **Total Commander 与 C++ 工具**：老派 Windows 工具的插件开发

## 风格

- 底层、诚实、不绕弯。从 AMD 出来以后敢直接点名 Microsoft 文档乱、DirectSR 被悄悄砍掉、Render Pipeline Shaders 基本死了
- 喜欢做"math puzzle + 可交互 demo"，把数值问题做成可玩的网页
- 同时写英语与波兰语版本，英语博客文章常先在波兰《Programista》杂志上发表

## 相关
- [[graphics-api-history]]
- [[system-load-formula]]
- [[pix-api-and-dxdmp]]
- [[dxr-tier-2-clas-ptlas]]
- [[advanced-shader-delivery]]
- [[hlsl-cooperative-vectors-tensor-cores]]
- [[d3d12-work-graphs]]
- [[d3d12-resource-binding]]
- [[d3d12-resource-alignment]]
- [[compute-shader-dispatch-ids]]

## Sources
- [[sources/asawicki-graphics-apis-yesterday-today]]
- [[sources/asawicki-system-load-formula]]
- [[sources/asawicki-dx12-gdc-2026-comments]]
- [[sources/asawicki-d3d12-resource-alignment]]
- [[sources/asawicki-compute-shader-sv-cheat-sheet]]
- [[sources/asawicki-memory-fragmentation-metric]]
