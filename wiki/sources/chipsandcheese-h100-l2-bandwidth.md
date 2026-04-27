---
tags: [source, gpu, nvidia, h100, hopper, hbm, cache, compute]
date: 2026-04-27
sources: 1
---

# Nvidia's H100: Funny L2, and Tons of Bandwidth（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 7 月的文章，通过微基准测试全面测量 H100 PCIe 版的 L1/L2/HBM 缓存层次、计算吞吐与特殊功能（Distributed Shared Memory、constant cache），并与 A100 及消费级 GPU 横向对比。

## 摘要

H100 是 Nvidia 基于 Hopper 架构的旗舰计算 GPU，814 mm²，TSMC 4N 工艺，80 亿晶体管。测试对象为 PCIe 版（114 SM、50 MB L2、10 HBM2e 控制器）。H100 最突出的特征是其"分裂 L2"——50 MB L2 分为两个分区，跨分区访问延迟接近消费级 GPU 的 VRAM 延迟（约 350 ns），带宽也明显低于近端分区。这使 H100 的 L2 实质上像一个两级结构而非单层缓存。另一方面，H100 的 HBM2e 带宽接近 2 TB/s，与 RDNA 2 Infinity Cache 相当；L1/Shared Memory 上升至 256 KB/SM（可配置偏向 L1 时为 208 KB 有效 L1）。FP32 和 FP64 吞吐相比 A100 均翻倍，Tensor Core 吞吐也翻倍。

## 关键要点

- H100 的 L2 分两个分区，跨分区延迟约 350 ns（相当于 RX 6900 XT 的 VRAM 延迟），带宽也大幅下降
- 近端 L2 读取带宽超过 5.5 TB/s，与 RX 7900 XTX L2 相当；远端分区带宽降至约 3.8 TB/s
- 每 SM 256 KB L1/Shared Memory 池，偏 L1 配置可得 208 KB 有效 L1，为当前最大
- HBM2e 带宽接近 2 TB/s，大幅超越消费级 GPU 的 VRAM；HBM3 SXM 版更高
- Constant cache 改由 L1 承担，消除了独立 constant cache 层次的延迟跳变
- FP32 和 FP64 吞吐相比 A100 均翻倍，配合 SM 数量和频率提升，整体算力大幅增加
- Distributed Shared Memory（DSMEM）允许 GPC 内 SM 间低延迟数据共享，Nvidia 宣称比全局内存快 7×

## 链接到的概念

- [[computer-systems/h100-hopper-architecture]]
- [[computer-systems/cuda-memory-hierarchy]]
- [[computer-systems/gpu-memory-hierarchy-latency]]
- [[rendering/rdna3-architecture]]
- [[rendering/rdna2-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/nvidias-h100-funny-l2-and-tons-of-bandwidth
- 本地：`raw/articles/chipsandcheese.com/2023-07-03_nvidias-h100-funny-l2-and-tons-of-bandwidth.md`
