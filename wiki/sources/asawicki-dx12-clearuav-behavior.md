---
tags: [source, D3D12, UAV, 缓冲区, 跨厂商行为]
date: 2026-04-27
sources: 1
---

# Secrets of D3D12: ClearUnorderedAccessViewUint/Float 的行为（Adam Sawicki）

[[adam-sawicki]] 发表于 2025 年 12 月的文章，通过在 Nvidia RTX 4090、AMD RX 9060 XT、Intel Arc B580 三张卡上的实验，揭示了 `ClearUnorderedAccessViewUint/Float` 在不同格式下跨厂商行为的不一致性。

## 摘要

`ClearUnorderedAccessViewUint` 和 `ClearUnorderedAccessViewFloat` 是 D3D12 中清零或填充 UAV 缓冲区的两个函数，相当于 GPU 端的 `memset`。文章先说明其接口：必须同时提供 GPU 可见堆的 GPU handle 和非 GPU 可见堆的 CPU handle，这一双重描述符要求来自早期固定功能硬件对 WRITE_COMBINE 内存的访问限制。随后，Sawicki 通过详细实验记录了在不同 `DXGI_FORMAT` 下（UINT/FLOAT/UNORM/SNORM/SINT 等）两个函数的实际写入行为：Uint 版本对非 UINT 格式和越界值的行为不可靠且跨厂商不一致；Float 版本对 FLOAT/UNORM/SNORM 格式的转换和截断行为更为规范一致。文章还对比了与 DX11 行为的差异，指出官方文档对此几乎没有说明。

## 关键要点

- 两个函数都要求缓冲区处于 `D3D12_RESOURCE_STATE_UNORDERED_ACCESS` 状态，与 compute shader 写入相同，与 `ClearRenderTargetView` 不同
- 双重描述符的设计动机：部分旧硬件将 shader-visible heap 分配在 WRITE_COMBINE 内存，固定功能 clear 单元无法从那里读取
- `ClearUnorderedAccessViewUint` 对 UINT 格式最安全，其余格式截断/溢出行为厂商各异
- `ClearUnorderedAccessViewFloat` 对 FLOAT/UNORM/SNORM 格式行为一致，对 UINT/SINT 格式不应依赖
- 部分行为在 RTX 4090 上正常但 D3D Debug Layer 报错——不能以 Nvidia 行为作为标准
- 官方文档对格式转换规则几乎没有说明，是 D3D12 文档混乱的一个缩影
- 限制清零范围可通过 UAV desc 的 `FirstElement/NumElements` 或通过 rect 参数两种等价方式实现

## 链接到的概念

- [[d3d12-resource-binding]]
- [[d3d12-resource-alignment]]

## 原文

- 链接：https://asawicki.info/news_1795_secrets_of_direct3d_12_the_behavior_of_clearunorderedaccessviewuintfloat
- 本地：`raw/articles/asawicki.info/2025-12-17_secrets-of-direct3d-12-the-behavior-of-clearunorderedaccessv.md`
