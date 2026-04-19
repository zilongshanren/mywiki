---
tags: [渲染, 图形api, webgpu, wgsl, zig, mach, sysgpu]
date: 2026-04-19
sources: 1
---

# sysgpu：Zig 写的 WebGPU 原生实现与"继任者"

`sysgpu` 是 [[mach-engine|Mach]] 在 2023-2024 年做的一次关键实验：用 Zig 从零写一个 WebGPU 的 native 实现，作为 Dawn（Chrome 的 WebGPU 实现）的替代品。到 Mach v0.3（2024-02）时它已接近一个完整可用的 WebGPU 原生后端——支持 D3D12/Vulkan/Metal/OpenGL 四个后端、自带 WGSL 编译器、nearly all mach-core examples 可以在其上跑，连第三方 Pixi pixel art editor 也开始用它。

## 从"另一个 WebGPU 实现"到"WebGPU 的继任者"

随着开发深入，Mach 团队发现 [[webgpu-intro|WebGPU]] 的 API 里有些选择在 native 语境下是可以翻修的，于是把 sysgpu 的定位从"又一个 WebGPU 实现"转成"WebGPU 的精简继任者/后代"——仍然基于 WebGPU 的设计思想，但不再保证 ABI 兼容，路线图里有这些计划：

- **削减 pipeline creation / descriptor boilerplate**：WebGPU 把所有状态打包进不可变 pipeline 的设计对小示例挺直白，但日常开发里 descriptor 代码量很烦。
- **把 push constants 当一等特性**，不走 extension 路径，用更好的 API 表达。
- **shader 与资源绑定更紧耦合**，保证类型正确性、减少错绑资源的运行时坑。
- **考虑用 Zig 本身作为 shading language**，并把 shader 编译完全离线作为可选流程。

上述修改在 v0.3 里大多还没实装，sysgpu 默认是关掉的。

## 为什么能做成

sysgpu 能绕开 Dawn 的核心原因是 Mach 肯接受一次离开 web 标准保证的 tradeoff：放弃 browser 级别的安全检查、放弃 ABI 兼容、也放弃和 Chrome 的 W3C 路线同步。换回来的是一个能完全自控的 pipeline，从 WGSL / 未来的 Zig-as-shader → 各个后端 IR（D3D12 对应 DXIL）→ 实际 GPU binary。为了让这条路径在 D3D12 那一端真的工作，Stephen 不得不顺手做了 [[mach-dxcompiler-static-build]]。

## 相关

- [[webgpu-intro]]
- [[mach-engine]]
- [[mach-dxcompiler-static-build]]
- [[stephen-gutekanst]]

## Sources

- [[sources/hexops-mach-v0-3-released]]
