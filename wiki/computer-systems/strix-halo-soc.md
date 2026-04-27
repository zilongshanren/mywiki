---
tags: [amd, soc, apу, igpu, zen5, rdna3-5, strix-halo, chiplet]
date: 2026-04-27
sources: 1
---

# Strix Halo SoC（AMD Ryzen AI Max）

Strix Halo 是 AMD 历经四代迭代后首款将旗舰级 CPU 与高性能 iGPU 整合于单一封装的 SoC，以 Ryzen AI Max 系列面向市场。Mahesh Subramony（AMD Senior Fellow）将其比作"能握在手心的 Threadripper"。

## 核心架构

Strix Halo 由两个主要 die 组成：一个搭载 Zen 5 CPU 核心的 CCD，以及一个包含 RDNA 3.5 iGPU（40 CU）、NPU、视频编解码器（VCN）和 Infinity Cache 的 SoC tile。两者通过扇出封装（fan-out）层上的"海量导线"（sea of wires）直连，而非桌面平台惯用的串行 GMI SERDES 接口。

这一互连方式具有决定性意义：GMI SERDES 需在约 20 GHz 频率下工作，存在功耗高、有重训延迟、低功耗状态切换慢等缺点。扇出直连则将互连时钟降至与 Data Fabric 匹配的 1-2 GHz，无状态、即开即关，带宽维持 32 byte/cycle 双向不变，功耗却显著降低。

## CPU

Strix Halo 的 Zen 5 核心配备完整 512-bit FPU 数据路径（与桌面 Granite Ridge 相同，不同于精简版的 Strix Point），但通过 binning 筛选选取功耗曲线更低的管芯，峰值频率低于桌面版以换取移动端效率。

## iGPU 与 MALL

40 个 RDNA 3.5 Compute Unit 配合 32 MB MALL（Memory Access Last Level）缓存。MALL 的主要用途是放大图形带宽：GPU 的写入会安装到 MALL，后续读取命中 MALL 可在某些场景下将有效带宽翻倍。

MALL 架构上支持灵活的分区配置，可通过固件划分一部分给 NPU、VCN 或 Display，但当前默认配置仅 GPU 写入安装。MALL 纳入 coherent fabric，所有 CPU 访问也会查询 MALL 以维护一致性，但 CPU 写入不安装到 MALL。

一致性管理点位于 Data Fabric 与内存控制器之间，而非 MALL 本身。

## 内存子系统

Strix Halo 使用 LPDDR5，不支持标准 DDR5 超频。仅需 1-2 个 CPU 线程即可在 streaming 场景下打满 DRAM 带宽，说明 CPU 侧带宽充裕，瓶颈在 GPU/NPU 侧。AMD 的目标是在低到中等 CPU 负载（15-20%）下维持低且稳定的内存延迟，避免出现"延迟曲棍球效应"。

## 意义与局限

Strix Halo 标志着 AMD 真正实现了 ATi 收购以来的"大 APU"愿景，将桌面级 GPU 计算能力带入轻薄移动平台。主要限制在于 LPDDR5 的固有带宽上限（相比 GDDR 离散 GPU）以及 MALL 容量对 GPU workload 的缓冲效果有限。

## Sources

- [[sources/chipsandcheese-strix-halo-interview]]
