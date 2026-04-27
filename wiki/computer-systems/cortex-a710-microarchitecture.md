---
tags: [cpu, arm, cortex-a710, mobile, microarchitecture, dsu, snapdragon]
date: 2026-04-27
sources: 1
---

# Cortex-A710 微架构

Cortex-A710 是 ARM 在 A78 基础上的效率优先迭代，于 2022 年随 Armv9-A 指令集一同发布，主要出现在 Snapdragon 8 Gen 1 / 8+ Gen 1 和 Dimensity 9000 系列 SoC 中。

## 设计哲学：效率优先

A710 的核心主题是在保持竞争力的同时降低功耗，而非追求更高的原始性能。体现在：前端宽度从 A77/A78 的 6-wide 削减至 5-wide，µop cache 出口带宽从 6 降至 5 µop/cycle，renamer 随之收窄。ARM 认为这些精简对大多数工作负载的性能影响极小，却能节省可观的面积和功耗。

## 前端

A710 的 µop cache 设计与 [[computer-systems/sandy-bridge-microarchitecture]] 高度相似：均为 1536 entry 虚地址索引设计，ARM 声称命中率约 85%。从 op cache 取出时可达 5 µop/cycle，支持 NOP 融合（2 个 NOP 合并为 1 µop），进一步提升有效吞吐。

分支预测器配置强劲：

- 2048 entry L1 BTB（有效约 512–1024 branch），1–2 周期延迟
- 10K entry L2 BTB，1–3 周期延迟
- 间接分支预测：单分支 64 目标，或 8 目标 × 4K 个分支
- 14-entry RAS，超出时回退到间接预测器

## 乱序执行引擎

A710 拥有远超老一代 ARM 核的乱序执行容量，ROB 容量约为 A76 的两倍。整数 cluster scheduler 容量超过 AMD Zen 2 的同类结构，尽管 Zen 2 采用更集中的调度设计，在队列填满时不易停顿。

整数执行端口约 4 个，其中 3 个处理常见整数操作（第 4 个偏向多周期运算）；2 个向量/FP 端口，128-bit 宽度（不支持 256-bit SIMD）。标量 FP 指令可在 rename 阶段融合，节省向量寄存器文件 entry。

## 内存子系统

地址翻译是 A710 相对保守的领域：

- L1 DTLB 仅 32 entry（小于 Haswell 的 64 entry、Zen 4 的 72 entry）
- L2 TLB 1024 entry，与多年前的 A73 相同，Zen 4 为 3072 entry
- 物理地址空间限制在 40-bit（1 TB），节省功耗

Store forwarding 仅支持上半或下半 store 到 load 的简单转发，完整 store 包含 load 的情况无快速路径，惩罚超过 10 周期。这与 [[computer-systems/sandy-bridge-microarchitecture]] 或 AMD Zen 系列的更完备 forwarding 逻辑有明显差距。

缓存配置灵活，由 SoC 厂商选择：Snapdragon 8+ Gen 1 配置了 32 KB L1D（个别核心为 64 KB）、512 KB L2、6 MB L3。L3 延迟约 20–21 ns（50+ cycle at 2.2 GHz），LPDDR 内存延迟则接近 100 ns。

## DSU-110 互联

A710 通过 ARM DynamIQ Shared Unit（DSU-110）与 L3 缓存和内存控制器互联。DSU-110 采用双环形总线拓扑，L3 分 slice，地址条带分布在各 slice 上——与 [[computer-systems/sandy-bridge-microarchitecture]] 的环形总线 L3 行为相似，core-to-core 延迟因 cacheline 归属 slice 位置而变化。

## 市场定位与竞争格局

A710 在技术上更接近"不出错的迭代"而非革命性设计。Samsung 和 Qualcomm 已放弃自研竞争，Apple 的 Firestorm/Avalanche 处于封闭生态。ARM 的策略：以稳健的效率改进维持客户满意，避免风险。

文章暗示这种垄断地位可能促使 ARM 放缓步伐，而若 Qualcomm（Nuvia/Oryon）或 Ampere（Siryn）推出有竞争力的核心，可能会催生类似 Sandy Bridge 时代 Intel 面对 AMD 竞争时的大幅架构跃进。

## Sources

- [[sources/chipsandcheese-cortex-a710]]
