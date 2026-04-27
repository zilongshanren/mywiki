---
tags: [gpu, qualcomm, adreno, igpu, snapdragon, laptop, tiled-rendering, hpm, wave64]
date: 2026-04-27
sources: 2
---

# Adreno X2 iGPU 架构

Adreno X2 是高通为 [[snapdragon-x2-elite-soc]] 设计的集成 GPU，是 [[adreno-x1-igpu-architecture]] 的下一代。顶配型号 X2-90 配备 2048 FP32 ALU，最高 1.85 GHz，是高通迄今最大的 GPU。

## Slice-Based 架构

Adreno X2 采用 Slice-Based 分层结构（类比 AMD Shader Engine 或 Nvidia GPC），X2-90 有 4 个 Slice。每 Slice 包含：
- 1 个 Front-End（每周期可光栅化 4 个三角形）
- 2 个 Shader Processor（SP），每 SP 含 2 个 micro-Shader Processor（uSP）
- 每 uSP：128 KB 寄存器文件 + 128 FP32/FP16/BF16 ALU + Ray Tracing Unit（4 ray-tri 或 8 ray-box 交叉/cycle）
- 128 KB Cluster Cache（Slice 级），统一 2 MB L2，再溢出至 8 MB System Level Cache（SLC）

内存子系统：最高 228 GB/s，SLC 后接 LPDDR5X。

## High-Performance Memory（HPM / AHPM）

HPM 是 Adreno X2 最核心的新特性。X2-90 共 21 MB 片上 SRAM，物理上分布在各 Slice（5.25 MB/Slice），但通过全局 crossbar 以全带宽可跨 Slice 随机访问。

**用途划分（软件可配置）：**
- 最多 3 MB 配置为 cache（受 cache tag 面积限制，超过此大小命中率收益趋于平坦）
- 剩余 ~18 MB 作为软件管理 scratchpad（存储 render target、Z-buffer、纹理等）

**核心价值**：X2-90 可将 QHD+（1600p）分辨率的完整帧——color ROPs + Z-buffer——全部保留在片上完成，无需触碰 DRAM，从根本上降低帧渲染的内存带宽消耗，提升能效。这是移动端 [[hsr-tbdr]] 思想在桌面级分辨率上的延伸。

## Wave64 与双发射机制

X1 时代每个 uSP 发射 Wave128 指令。X2 改为 **Wave64 + 双发射**：每周期同时发射两个 Wave64，128 个 ALU 同样满载。

**优势**：Wave64 的分支发散（divergence）粒度更小，分支执行效率更高；更多 Wave 在途有助于隐藏内存延迟。代价是上下文状态翻倍，寄存器文件因此从 96 KB 扩展至 128 KB（+33%）。根据 Eric Demers 的说法，双发射几乎全时运行，只在极端 GPR 压力下才降为单发射。

## API 支持

- DirectX 12.2（含 DX12 Ultimate 全特性）、Shader Model 6.8
- 原生 Vulkan 1.4（与移动端 Adreno 共享代码库）
- 原生 OpenCL 3.0（同上）
- SYCL（计划 2026 Q1）

原生实现是相比 X1 的重要改进——X1 依赖 Windows 系统提供的兼容层。

## 与 Adreno X1 对比

| 特性 | X1 | X2 |
|---|---|---|
| Wave 模式 | Wave128 | Wave64 双发射 |
| 寄存器文件（uSP） | 96 KB | 128 KB |
| 片上 SRAM | GMEM（小） | HPM 21 MB（大） |
| Ray Tracing | 有 | 有（同规格） |
| 原生 Vulkan | 否（系统层） | 是 |

## Sources

- [[sources/chipsandcheese-snapdragon-x2]]
- [[sources/chipsandcheese-adreno-x2]]
