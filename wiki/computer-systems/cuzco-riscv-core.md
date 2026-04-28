---
tags: [cpu, risc-v, condor, andes, cuzco, ooo, time-based-scheduling, hot-chips-2025, 微架构]
date: 2026-04-27
sources: 1
---

# Cuzco RISC-V 核心与时间调度

Cuzco 是 Condor Computing（Andes Technology 旗下子公司，成立于 2023 年）设计的可许可 RISC-V 高性能核心，于 Hot Chips 2025 公开展示。它定位于与 SiFive P870、Veyron V1 同一梯队，远超目前量产的 Alibaba T-HEAD C910 和 SiFive P550。Cuzco 的独特之处不在于 ISA——它完全兼容 RISC-V——而在于后端调度机制：将传统动态调度器的职责前移至重命名/分配阶段，以"时间调度（time-based scheduling）"取而代之。

## 时间资源矩阵（TRM）

在传统乱序核中，指令进入后端调度器（issue queue / reservation station）后，调度器每周期扫描所有等待指令，判断哪些指令的操作数已就绪并分配空闲执行单元。这个"唤醒-选择（wakeup-select）"逻辑是功耗与面积的主要来源之一，在宽核设计中尤为昂贵。

Cuzco 的重命名器在指令进入后端之前，就根据当前已知的执行计划预测每条指令将在哪个周期可以执行，并将这个时间槽记录进**时间资源矩阵（Time Resource Matrix, TRM）**。TRM 追踪未来 256 个周期内各执行资源（端口、功能单元、数据总线）的占用情况。后端调度器只需按照 TRM 写入的周期倒计时触发指令，完全无需动态依赖检查。

重命名器在为一条新指令寻找执行槽时，只在依赖就绪时间点之后的 **8 cycle 窗口**内搜索 TRM，找到空闲资源即填入。若窗口内资源满载，该指令会在 ID2 阶段停顿等待。Condor 测试表明，相比理想的"贪心"调度，这种受限搜索仅带来约数个百分点的性能下降。

这一思路与 Nvidia GPU 的静态 warp 调度（Kepler 架构后）有表面相似之处，但区别在于：GPU 的调度由编译器生成，依赖非标准 ISA；Cuzco 的 TRM 完全在硬件重命名级动态生成，对软件和编译器完全透明。

## 指令重放机制

静态时间调度有一个根本性问题：若预测的执行时间错误（例如预期 L1D 命中但实际缺失），后续指令已基于错误预期值开始执行，产生无效结果。Cuzco 通过**毒化位（poison bit）**处理此问题：被误执行指令的结果被标记为 poison，所有消费该结果的后继指令被强制重新执行。

Cuzco 对所有变延迟操作（包括 L1D miss 在内）统一以 L1D 命中延迟入 TRM；实际缺失由重放修复。以 L3 命中为例，一条 load 指令可能被重放三次：首次按 L1D 命中预测执行（失败）、二次按 L2 命中预测执行（失败）、第三次按 L3 命中预测执行（成功）。实测重放率约 **70.07 次/千指令**，约消耗 7% 额外执行资源，被认为可接受。

## 前端与执行资源

- **前端**：TAGE-SC-L 分支预测器（TAGE + Statistical Corrector + Loop Predictor），基础 bimodal 表 16K 条目；8K 两级 BTB（第一级命中产生单周期气泡）；32 条目 return stack
- **取指/解码**：每周期取 64B（一个 cacheline）存入 ICQ，再向解码器供应；最多 8-wide decode
- **流水线深度**：12 级；误预测惩罚约 10 周期
- **执行 slice 化**：执行资源按 slice 划分，每 slice 含一对流水线，可执行所有 RISC-V 指令；4 slice 配置下峰值吞吐 8 整数 ALU / 4 AGU / 4 FMA/cycle
- **向量**：256/512-bit VLEN 以多 µop 拆分，分发至各 slice 的 64-bit 原生执行单元；FP add 2 cycle，FP MUL/FMA 4 cycle

## 竞争格局与商业挑战

技术上，Cuzco 在 RISC-V 软件生态内提供高性能（TAGE-SC-L 预测器与 AMD Zen 2、Ampere AmpereOne、Qualcomm Oryon 同档），同时以时间调度降低实现复杂度。但高性能 RISC-V 核的商业挑战在于：无论 Graviton（AWS 内部消化）还是 Ampere（外部销售）都面临客户获取难题，RISC-V 更需要一个体量足够大的"锚点客户"（如腾讯、阿里巴巴）才能形成规模。

## Sources

- [[sources/chipsandcheese-condor-riscv]]
