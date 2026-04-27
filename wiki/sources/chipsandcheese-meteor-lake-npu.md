---
tags: [source, computer-systems, intel, npu, ai-accelerator, meteor-lake, movidius]
date: 2026-04-27
sources: 1
---

# Intel Meteor Lake's NPU（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2024 年 4 月的文章，对 Intel Core Ultra 7 155H（Meteor Lake）内置 NPU 3720 进行微基准测试与架构分析，给出了较为清醒的性价比评估。

## 摘要

NPU 3720 源自 Intel 2016 年收购的 Movidius DSP 平台，在其基础上添加了大规模 MAC 阵列。整颗 NPU 由两个 Neural Compute Engine（NCE）tile 构成，每 tile 512 个 MPE（每 MPE 4 INT8 MAC/cycle），合计 4096 INT8 MAC/cycle，峰值 9.5 TOPS @ 1.16 GHz。非 MAC 运算由 SHAVE（Streaming Hybrid Architecture Vector Engine）DSP 核心承担，支持 FP16/FP32，但不支持 FP64，导致 Stable Diffusion 等模型无法直接编译。内存层次上，NPU 不使用传统缓存，NCE 各有 2 MB 软件管理 SRAM；系统侧通过 IOMMU 接入 Scalable Fabric，但 DMA 带宽（~10 GB/s）明显逊于 iGPU（~19 GB/s）。实测 FP16 吞吐 1.35 TFLOPS，远低于 4.7 TFLOPS 理论值；Stable Diffusion 性能落后于 iGPU 62%（FP32）或 261%（INT8 对比）。作者结论：NPU 适合省电场景，但软件生态不成熟，"AI PC"营销言过其实。

## 关键要点

- NPU 3720：2×NCE tile，512 MPE/tile，4096 INT8 MAC/cycle，9.5 TOPS
- SHAVE DSP 处理 FP16/FP32，不支持 FP64，限制了模型兼容性
- LEON SPARC 微控制器（LeonRT + LeonNN）负责命令处理与任务调度
- 内存：NCE 各有 2 MB scratchpad SRAM（软件管理，非缓存），128 KB 快速本地存储（约 16 ns 延迟）
- DMA 带宽 <10 GB/s，落后 iGPU 的 19 GB/s
- Stable Diffusion 实测：iGPU FP32 比 NPU INT8 快 261%；离散 GPU（RX 6900 XT）快 6.7×
- 软件生态问题突出：ONNX、OpenVINO 兼容性差，FP64 缺失导致主流模型编译失败

## 链接到的概念

- [[computer-systems/npu-accelerator-design]]
- [[computer-systems/meteor-lake-chiplet-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/intel-meteor-lakes-npu
- 本地：`raw/articles/chipsandcheese.com/2024-04-22_intel-meteor-lakes-npu.md`
