---
tags: [source, hardware, qualcomm, snapdragon, cpu, gpu, oryon, adreno]
date: 2026-04-27
sources: 1
---

# Qualcomm's Snapdragon X2 Elite（George Cozma / Chips and Cheese）

[[george-cozma]] 发表于 2025 年 11 月的文章，介绍高通 Snapdragon X2 Elite（SDX2E）SoC 的架构细节，涵盖 Oryon Gen 3 CPU 核心、Adreno X2 GPU、Hexagon NPU 6 及功耗机制。

## 摘要

SDX2E 配备 18 个 CPU 核心（12 个 Prime + 6 个 Performance），Prime 核心基于 Oryon Gen 3 微架构，单簇 6 核共享 16 MB L2，最高 5.0 GHz。Oryon Gen 3 相比 Gen 1 主要升级：解码/重命名/退休宽度从 8 扩展到 9；Branch Unit 翻倍至 4 个；新增 SVE/SVE2 支持；每簇配备一个 SME 兼容 Matrix Engine（4096 位宽，支持 128 FP32 / 256 FP16 / 512 INT8 ops/cycle）。Performance 核心为较窄的低功耗变种，目标低于 2W 运行。

GPU 方面，Adreno X2 采用 Slice-Based 架构，顶配 X2-90 有 4 个 Slice，共 2048 FP32 ALU，最高 1.85 GHz。引入 21 MB AHPM（Adreno High Performance Memory），可在片上完成 QHD+ 分辨率的完整帧渲染，大幅降低对 DRAM 的带宽需求。Wave128 被移除，改为 Wave64 + 双发射机制。NPU 6 的 INT8 算力从 45 TOPS 提升到 80 TOPS，新增 FP8/BF16/INT2 支持，DMA 单元升级为 64 位虚拟寻址。

## 关键要点

- Oryon Gen 3 解码宽度 9-wide，Branch Unit ×4，新增 SVE/SVE2
- Matrix Engine 每簇一个，4096 位宽，独立时钟域
- Performance 核心≠效率核：命名与业界习惯相反（Qualcomm Prime ≈ 其他厂商 Performance）
- Adreno X2 AHPM：21 MB 片上 SRAM，可作为 scratchpad 或 cache，3 MB 可配置为 cache
- Wave128 → Wave64 + 双发射（dual-issue），ALU 利用率不变
- Hexagon NPU 6：80 TOPS INT8，64 位虚拟地址 DMA
- API 支持：DX12.2 / SM 6.8 / Vulkan 1.4 / OpenCL 3.0 / SYCL（2026 H1）

## 链接到的概念

- [[oryon-microarchitecture]]
- [[snapdragon-x2-elite-soc]]
- [[adreno-x2-igpu-architecture]]
- [[npu-accelerator-design]]

## 原文

- 链接：https://chipsandcheese.com/p/qualcomms-snapdragon-x2-elite
- 本地：`raw/articles/chipsandcheese.com/2025-11-19_qualcomms-snapdragon-x2-elite.md`
