---
tags: [source, gpu, amd, cdna3, mi300x, hpc, ai, benchmark, hbm3]
date: 2026-04-27
sources: 1
---

# Testing AMD's Giant MI300X（Chips and Cheese）

[[chester-lam]] 等人发表于 2024 年 6 月的实测文章，通过微基准测试与实际应用负载全面评估 MI300X 相对于 NVIDIA H100 PCIe 的硬件能力。

## 摘要

文章从缓存延迟、各层带宽、局部内存、全局原子操作、计算吞吐量、PCIe 链路带宽到 LLM 推理延迟，对 MI300X 进行系统性实测。总体结论是：MI300X 在几乎所有纯硬件维度上均优于 H100 PCIe——其 256 MB Infinity Cache 实测带宽约 11.9 TB/s，L2 带宽与 H100 的 L1 同量级，HBM3 提供超过 2.6× 的 DRAM 带宽优势。计算吞吐方面，INT16 packed 执行和 FP16 均有显著领先，FP64 受功耗限制未能满载运行。LLM 推理（Mistral 7B / LLaMA3-70B）方面，单卡 MI300X 的吞吐与延迟优于单卡或双卡 H100。然而文章也明确指出，ROCm 软件生态仍是 AMD 最大短板：flash-attention 的 CDNA3 实现尚不完整，ROCm 覆盖范围远不如 CUDA 普及。

## 关键要点

- MI300X Infinity Cache 实测带宽约 11.9 TB/s，超 H100 PCIe L2 带宽 4× 以上
- 每 XCD 的 TLB 容量约 16384 条目（4K 页），TLB miss 惩罚约 47.1 ns
- 局部内存（LDS）延迟优于 RDNA 2 消费卡，但不及 H100；轮询 atomic 延迟 MI300X 反超 H100
- FP64 算力约为 H100 PCIe 的 3×，但两者均受功耗限制无法维持最高频
- ROCm 缺乏统一覆盖是制约商业推广的核心障碍

## 链接到的概念

- [[cdna3-mi300x-architecture]]
- [[cdna2-mi200-architecture]]
- [[h100-hopper-architecture]]
- [[cuda-memory-hierarchy]]
- [[gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/testing-amds-giant-mi300x
- 本地：`raw/articles/chipsandcheese.com/2024-06-25_testing-amds-giant-mi300x.md`
