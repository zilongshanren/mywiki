---
tags: [source, hardware, nvidia, blackwell, b200, gpu, datacenter, cuda]
date: 2026-04-27
sources: 1
---

# Nvidia's B200: Keeping the CUDA Juggernaut Rolling（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2025 年 12 月的文章，在 Verda 提供的含 8 块 B200 GPU 实例上，对 Nvidia Blackwell B200 服务器 GPU 进行缓存层次、带宽、计算吞吐量及机器学习特性的系统实测，并与 H100、A100、AMD MI300X 横向比较。

## 摘要

B200 是 Nvidia 首款 Chiplet GPU，由两块 reticle-size die 组成，软件侧视为单一 GPU，共 148 个 SM（各 die 启用 74 SM），使用 TSMC 4NP。L1/Shared Memory 维持 256 KB 不变；L2 大幅扩展至 126 MB（H100 为 50 MB），分两个分区对应两块 die，跨分区延迟略高但尚可接受（约 190-220 ns vs 单分区 90-100 ns）。HBM3E 带来 VRAM 带宽优势，超过 MI300X 的 HBM3。

Tensor Memory（TMEM）是 Blackwell 最重要的架构创新：每 SM 512 列 × 128 行的 32-bit 专用矩阵寄存器文件，支持动态分配（32~512 列），类比 AMD CDNA 的 Acc VGPRs 但更灵活——支持从 Shared Memory 直接加载、4/6-bit 解压、CTA 级矩阵指令。由此 Blackwell 可在不扩展主向量寄存器文件的前提下提供更大的 AI 专用存储，实现自 Kepler 以来首次有效的寄存器容量扩展。

FP16 向量算力反常地低于 H100（不再支持双倍速 FP16），重点转移到 Tensor Core。MI300X 在原始向量算力上仍领先，但 B200 在带宽敏感型（FluidX3D）工作负载中超越 MI300X。驱动层面存在可重现的 GPU hang 死锁问题（nvidia_uvm 锁未释放），需要重启系统。

## 关键要点

- B200：双 die chiplet GPU，148 SM，TSMC 4NP
- L2 126 MB（双分区），单分区 vs 跨分区延迟约 90-100 ns vs 190-220 ns
- Tensor Memory（TMEM）：动态分配的 AI 专用寄存器文件，每 SM 64 KB
- FP16 向量算力不再双倍速，聚焦 Tensor Core 处理 FP16/BF16
- HBM3E VRAM 带宽超越 MI300X（HBM3）
- MI300X 在原始算力、Local Memory 带宽上仍有领先
- CUDA 生态护城河是 Nvidia 保守设计策略背后的核心逻辑

## 链接到的概念

- [[blackwell-gb202-architecture]]
- [[h100-hopper-architecture]]
- [[cuda-memory-hierarchy]]
- [[mcm-gpu-design]]

## 原文

- 链接：https://chipsandcheese.com/p/nvidias-b200-keeping-the-cuda-juggernaut-rolling
- 本地：`raw/articles/chipsandcheese.com/2025-12-15_nvidias-b200-keeping-the-cuda-juggernaut-rolling-ft-verda-fo.md`
