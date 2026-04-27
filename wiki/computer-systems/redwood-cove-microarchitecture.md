---
tags: [cpu, intel, redwood-cove, meteor-lake, microarchitecture, x86, p-core]
date: 2026-04-27
sources: 1
---

# Redwood Cove 微架构

Redwood Cove 是 Intel 2023 年 Meteor Lake SoC 中的 P-Core 架构，是 [[computer-systems/golden-cove-microarchitecture|Golden Cove]] 的直系后继（经由 Raptor Cove）。整体上属于小幅迭代——Intel 的 "tick"——主要结构容量未变，重点在前端改善和预取器扩充。对应关系：Golden Cove（Alder Lake 2021）→ Raptor Cove（Raptor Lake 2022，+2 MB L2、更高频率）→ Redwood Cove（Meteor Lake 2023）。

## 前端改进

**分支预测**：相对 Golden Cove 有小幅提升，Redwood Cove 的一级快速预测器可识别稍长的分支模式（pattern length 超过 16 时出现延迟跳变，Golden Cove 约在 8 跳变）。BTB 容量继承 Golden Cove 的 12K 项，但延迟从 3 周期降至 2 周期。奇特之处：单线程只能看到约 6K BTB 项，两个 SMT 线程合起来才能利用全部 12K 项，暗示 micro-op 缓存可能在 Golden Cove 时就已按线程永久分区。

**Branch Hint 重新启用**：Redwood Cove 恢复了 Pentium 4 时代引入、之后被多代忽略的 0x3E taken hint 前缀。当分支预测器对某个分支毫无先验信息时，解码器发现该前缀后会主动重定向前端，减少冷分支的惩罚周期。

**L1 指令缓存翻倍**：从 32 KB 增至 64 KB，是 Redwood Cove 最直观的前端变化。实测带宽 32 bytes/cycle，单线程与双线程均可达到（双线程略好）。

**Micro-op 队列（IDQ）扩容**：从 144 项增至 192 项（单线程）；双 SMT 激活时各分 96 项。更大的 IDQ 可吸收前端与后端之间的速率差，减少单次流水线气泡的放大效应。同时 Loop Stream Detector（LSD）覆盖范围提升，在 xalancbmk、gcc、x264 等测试中能让核心以低功耗的 LSD 模式处理相当比例的指令流。

**更多宏融合**：新增 MOV+OP 和 LD+OP 宏融合（load-then-op、move-then-op 可融合为单个 micro-op），减少后端资源压力，并使 6-wide 核心在融合指令频繁出现时效率接近 7 wide。

## 后端

后端与 Golden Cove/Raptor Cove 完全一致，所有主要结构（ROB、调度器、寄存器文件、Load/Store Queue）容量无变化。唯一记录在册的执行单元改进是 FP 乘法延迟从 4 周期降至 3 周期（追平了 Broadwell 2015 年短暂达到后又退步的水平；AMD Zen 系列自 Zen 1 起就是 3 周期）。

SMT 资源分配上，Redwood Cove 对部分结构采用高水位标记（watermark），例如单线程可占用约 3/4 的整数寄存器文件，比 AMD Zen 4 的约 58% 更激进，有助于单线程性能。实测 SPEC CPU2017 rate（双线程绑单核）：整数套件 +17.6%，浮点套件仅 +4.2%，逊于 Zen 4（整数 +20%+，浮点 +20%+）。

## 预取器新增

**LLC 页预取器（LLC Page Prefetcher）**：检测到访问接近当前 4 KB 页末尾时，提前将后续 8 KB（两页）数据预取进 L3（24 MB）。预取仅入 L3 以免污染 L1/L2，并通过 IDI 机会性发包（不占用 L2 miss 追踪槽，避免与正常需求访问竞争），在高 IDI 流量时自动节流。

**数组指针预取（AOP Prefetcher）**：识别通过指针数组进行间接访问的模式（pointer chasing through array of pointers），提前发起地址翻译与缓存填充。Apple Silicon 自 M1 起已有此功能，研究人员亦曾在 Raptor Cove 中发现类似机制。

## 内存层次

Redwood Cove 在 Meteor Lake 封装内使用 LPDDR5-7467 配置。L3 约 12 MB，L3 延迟约 75+ 周期（比 Zen 4 移动版的约 50 周期高约 50%），成为 Meteor Lake 在延迟敏感场景下的弱项。L2 miss 追踪队列从 48 增至 64 项，理论上有助于带宽，但 Meteor Lake 整体 clock-for-clock 带宽仍不及 AMD 的移动版。DRAM 延迟约 148 ns，高于 Strix Point 的约 128 ns。

## 定位与后继

Redwood Cove 是 Intel 在 Meteor Lake 系统级大变动（chiplet 转型）下刻意保守的 P-Core 选择，尽量降低新品风险。相比之下，Alder Lake 到 Raptor Lake 再到 Meteor Lake 的 P-Core 进化幅度远小于 AMD 同期从 Zen 3 到 Zen 4 再到 Zen 5 的演进。Redwood Cove 的后继是 [[computer-systems/lion-cove-microarchitecture|Lion Cove]]（Lunar Lake，弃用 SMT、大幅重设计），代表 Intel 真正的 "tock"。

## Sources

- [[sources/chipsandcheese-redwood-cove]]
