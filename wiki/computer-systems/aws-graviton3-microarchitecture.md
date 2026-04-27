---
tags: [cpu, arm, aws, cloud, server, microarchitecture, sve]
date: 2026-04-27
sources: 1
---

# AWS Graviton 3 微架构

Graviton 3 是 Amazon AWS 于 2022 年 5 月面向公众正式开放的 ARM 服务器处理器，基于 TSMC 5nm 工艺，采用 64 核配置，主频 2.6 GHz。TheNextPlatform 的分析认为其核心基于 Neoverse V1，AWS 对架构细节有所定制（如将解码宽度从 V1 的 5-wide 裁剪至 4-wide）。Graviton 3 是 2022 年中期云计算市场中性能最强、覆盖最广的 ARM 服务器 CPU。

## 与 Neoverse N1 的代际飞跃

Graviton 2 基于 Neoverse N1（64 核，2.5 GHz），Graviton 3 在核心微架构上实现了质的跳跃。

**分支预测器**：从 N1 的平庸实现跃升至可与 Ice Lake / Zen 3 媲美的水平。单级快速预测器可识别极长模式（无 Zen 2 式双级叠加的额外延迟）。BTB 配置：micro-BTB（容量大于 Golden Cove 的 32 条目）支持每周期处理两次跳转，主 BTB 约 4K 条目，L2 BTB 可达 10K 条目。

**前端**：保持 4-wide 解码器，但新增约 3K 条目的微操作缓存，支持多种指令融合（包括 x86 风格跳转融合和 CNS 风格 NOP 融合）。重命名阶段 6-wide，与 Zen 3 同宽。

**乱序结构**：ROB 约 512 条目（超过 Zen 3 和 Ice Lake），调度器规模与 Zen 3/Ice Lake 大致相当。加载队列容量尤为突出。

**执行单元**：4 个整数 ALU（N1 为 3 个），3 个内存流水线（N1 为 2 个），向量/浮点侧大幅强化——可视为 N1 向量资源翻倍，两个 256-bit SVE FP 加法器 + 两个乘法器，FP 加法延迟 2 周期，与 Golden Cove 相当。

**缓存**：64 KB L1D（4 周期），L2 延迟比 Graviton 2 低 2 周期，L3 延迟比 Ampere Altra 大幅改善。DDR5 带来内存带宽大幅领先，但延迟略有回退。

## SVE 指令集的战略意义与局限

Graviton 3 是第一款面向通用云场景的 ARM SVE CPU（Fujitsu A64FX 是 HPC 专用）。256-bit SVE 可将 L1D/L2 带宽推上 Zen 3 之上，但：

- 截至 2022 年中，几乎无软件原生支持 SVE（GCC 默认不发射 SVE 指令，需用 Clang）
- SVE 市场渗透率远低于 AVX(2)，类似 Skylake-X 时代的 AVX-512
- SVE2 已发布，若软件针对 SVE2 特有指令优化，Graviton 3 将无法受益

## 云计算定位与功耗策略

AWS 的设计目标是**最大化云端计算密度**，而非追求单核性能峰值。主频仅 2.6 GHz（比 Graviton 2 高 100 MHz），近乎所有性能增益来自 IPC 提升。5nm 工艺极低功耗使 AWS 可在单节点塞入三颗 Graviton 3，以此降低每核成本、提高计算密度。

## 与 x86 竞品的定位

各架构取舍各异：Zen 3 和 Ice Lake 同时服务于客户端（可跑到 4+ GHz），而 Graviton 3 只针对服务器低频高密度场景。在实际时间延迟上，Graviton 3 因主频差距，绝对性能仍落后于 Zen 3（Milan）和 Ice Lake SP（Xeon）。但每美元性价比和内存带宽上，Graviton 3 具有竞争力。

## Sources

- [[sources/chipsandcheese-graviton3-first-impressions]]
