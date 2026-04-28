---
tags: [cpu, arm, huawei, hisi, kunpeng, taishan, chiplet, numa, 微架构]
date: 2026-04-27
sources: 1
---

# 华为 Kunpeng 920 与 TaiShan v110 架构

Kunpeng 920 是华为 HiSilicon 自研的 chiplet 服务器 CPU，于 2019 年发布，针对云服务器、AI 加速和无线基站等企业应用。它是华为在先进制程和 chiplet 封装上的早期押注，也是 TaiShan v110——HiSilicon 第一代自研 AArch64 核心——的旗舰载体。

## 系统架构

Kunpeng 920 使用 TSMC 的 CoWoS（Chip on Wafer on Substrate）封装，将多种 die 集成在 65 nm 被动中介层上：

- **SCCL（Super CPU Cluster）计算 die**：TSMC 7 nm，最多 32 颗 TaiShan v110 核心 + DDR4 控制器。核心以 4 核一组的 **CCL（CPU Cluster）** 排列，通过双向 ring bus 将 CPU cluster、L3 数据 bank、内存控制器和跨 die 链路连接在一起
- **IO Die**：TSMC 16 nm，连接 PCIe、SATA 等低速 IO

与 Intel Sapphire Rapids 的高带宽跨 die 策略类似，Kunpeng 920 将内存控制器放置在计算 die 的边缘，使小型 SKU 也能直接访问 DRAM 而无需路由到其他 chiplet。但 Kunpeng 920 不支持跨 SCCL 的 L3 和 DRAM 透明共享——多 die 配置下各 SCCL 呈现为独立 NUMA 节点。Kunpeng 920 支持 "Hydra" 链路用于双路和四路配置，跨 die 带宽最高 400 GB/s（带一致性）。

## L3 缓存的独特设计

Kunpeng 920 最具特色的系统级特性是其三模式 L3 缓存策略：

| 模式 | 行为 |
|------|------|
| Shared | 所有 L3 bank 构成统一共享缓存，地址哈希分散到各 bank |
| Private | 每个 L3 bank 私属于最近的 CPU cluster |
| Partition（默认）| 动态调整，尽量将 L3 数据保持在使用它的 cluster 附近 |

另一个非常规设计是将 **L3 tag 放置在 CPU cluster** 而非 L3 数据 bank。正常设计（Intel、AMD、Arm）都是 tag 与数据同位。Huawei 的选择是将 tag 靠近核心，以更快地响应 hit/miss 判断，代价是 tag 与数据位于不同 ring stop，需额外一次互联传输。

Partition 模式下单核私有 L3 访问约 36 cycle，表现尚可。但一旦有数据共享，L3 即切换为 shared 模式，延迟升至 >90 cycle——即便是同 cluster 内两核共享也会触发这一行为，这被 Chester 指出是设计上的显著缺陷。

## TaiShan v110 核心

TaiShan v110 是 HiSilicon 第一代自研 AArch64 核心，4-wide 乱序执行，定位与 [[xuantie-c910-microarchitecture]] 的 C910 不同，主要服务于服务器场景。

核心主要参数：

- 4-wide 解码，支持寄存器重命名与移动消除
- ROB 容量与 Goldmont Plus 相近，整数寄存器文件略大
- 统一调度器：ALU / 内存 / FP-向量 各一个，每个约 33 项
- 4 整数端口（3 通用 ALU + 1 多周期），2 FPU 端口（128-bit 向量，FP32 FMA 5 cycle）
- 64 KB L1I + 64 KB L1D，512 KB 私有 L2
- 分支预测：双级动态预测器，64 项 BTB（1 cycle），31 项返回堆栈

与同时代竞争者的 SPEC CPU2017 整数比较：TaiShan v110 领先 Cortex A72 约 22.5%、Goldmont Plus 约 7%，但落后 Neoverse N1 约 34%，与 Zen 2 差距更大。Neoverse N1 优势来源：更大的 BTB（6K 项）、更平衡的后端资源、更大的 FP/向量寄存器堆，以及更大的 L2 缓存（使核心能更好地绕过 L3 延迟问题）。

## 总体评价

Kunpeng 920 集合了多项超前于同代的技术选择：早期 7 nm CoWoS chiplet、动态 L3 分区、服务器级 DRAM 控制器。然而这些特性的组合效益不尽如人意。CoWoS 高带宽似乎没有充分利用（缺少跨 die 透明共享）。动态 L3 分区在数据共享场景下退化为高延迟 shared 模式。TaiShan v110 的 7 nm 工艺密度优势被不够平衡的微架构设计消耗。

结论是：HiSilicon 的工程团队足够激进，愿意尝试大量非常规设计，为 Huawei 未来的自研 CPU 路线（TaiShan v200/v300 系列）积累了宝贵经验。Kunpeng 920 可以视为华为 CPU 自研能力的"验证平台"。

## Sources

- [[sources/chipsandcheese-kunpeng-920]]
