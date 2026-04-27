---
tags: [gpu, nvidia, h100, hopper, hbm, compute, datacenter]
date: 2026-04-27
sources: 1
---

# H100 Hopper 架构

H100 是 Nvidia Hopper 架构的旗舰计算 GPU，面向大规模 AI 训练与科学计算，代表了 Nvidia 计算与图形 GPU 路线进一步分化的产物。

## 规格概述

H100 基于 TSMC 4N 工艺，814 mm² 巨型单片 die，约 80 亿晶体管。完整规格包含 144 个 SM、60 MB L2 缓存、12 路 512-bit HBM 内存控制器。PCIe 版启用 114 SM、50 MB L2、10 路 HBM2e；SXM 版启用 132 SM 并使用 HBM3 内存，功耗高达 700W。

## 分裂 L2 缓存

H100 最显著的结构特征是其分裂 L2 设计，继承自 A100 并进化。50 MB L2 分为两个物理分区，任何线程均可访问全部 50 MB，但访问"远端"分区的延迟约为"近端"的两倍（约 350 ns，相当于 RX 6900 XT 的 VRAM 延迟）。因此，H100 的 L2 实质上是一个两层结构：

- 近端 L2 读取带宽 > 5.5 TB/s
- 全量 50 MB 访问时带宽降至 ~3.8 TB/s（相比 A100 的 ~4.5 TB/s 有所退步）

这与现代消费级 GPU 的低延迟单层大 L2 截然不同。Nvidia RTX 4090 的 72 MB L2 在近端带宽和延迟上均优于 H100，但 H100 的设计优先保证大容量和绝对吞吐，不针对单线程延迟优化。

## SM 级别设计

H100 每个 SM 拥有 256 KB 的 L1/Shared Memory 联合存储池，可灵活分配为 L1 缓存或软件管理的 Shared Memory（scratchpad）。偏向 L1 配置可获得约 208 KB 有效 L1 容量，为当前所有 GPU 中最高。Shared Memory 访问速度快于 L1（不需 tag 比较），H100 在 workgroup 内原子操作上表现合理，但跨 SM 的全局内存原子操作延迟远高于消费级 GPU（大尺寸 die 跨越距离的固有代价）。

H100 将每 SM 可跟踪的 warp 数从 A100 的 48 个提升至 64 个，以应对更高的 L1 miss 延迟。

## FP32 / FP64 / Tensor 吞吐

A100 的 SMs 只有 FP32 一半吞吐用于避免 FP64 占用：H100 修正了这一点，每个 SMSP 内 FP32 单元翻倍，FP64 吞吐相比 A100 也翻倍。配合 SM 数量增加和时钟提升，H100 的 FP32/FP64 整体算力对 A100 形成碾压。Tensor Core 吞吐同样翻倍，用于加速矩阵乘法（AI 推理/训练的核心操作）。

## HBM 带宽

H100 PCIe 版通过 5 栈 HBM2e 提供接近 2 TB/s 的 VRAM 带宽，大幅超越任何消费级 GPU 的 GDDR6 配置；SXM 版使用 HBM3，带宽更高。这与计算 GPU 的设计哲学一致：大型、长时间运行的任务倾向于使用不符合 cache 友好访问模式的超大数据集，因此 VRAM 带宽比缓存容量和延迟更关键。

## Distributed Shared Memory（DSMEM）

H100 新增 DSMEM 特性，允许同一 GPC（Graphics Processing Cluster）内的多个 SM 直接访问彼此的 Shared Memory 空间，无需通过全局内存中转。Nvidia 宣称 DSMEM 比全局内存数据交换快约 7 倍，对需要在超出单个 workgroup 范围内共享状态的算法（如 Flash Attention 的某些变体）有明显收益。

## 与消费级 GPU 的分化

H100 的设计哲学与消费级 GPU（[[rendering/rdna3-architecture]]、[[rendering/ada-lovelace-architecture]]）形成鲜明对比：

- 消费级 GPU 追求高时钟、低延迟缓存、响应小批量工作负载
- H100 牺牲单线程延迟和小工作负载响应，换取极高的并行吞吐和超大 VRAM 带宽
- Ada Lovelace（RTX 4090）时钟 >2.5 GHz；H100 PCIe 典型频率约 1.75 GHz

这种分化随着工艺节点进步放缓而日趋明显——在预算有限时，针对不同用途分别优化比做一款通用 GPU 更有效率。

## Sources

- [[sources/chipsandcheese-h100-l2-bandwidth]]
- [[sources/chipsandcheese-grace-hopper]] — GH200 中的 H100 GPU 实测，NVLink C2C 互联分析
