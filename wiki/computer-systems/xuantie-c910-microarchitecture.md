---
tags: [risc-v, t-head, alibaba, c910, xuantie, microarchitecture, out-of-order, vector, china]
date: 2026-04-27
sources: 2
---

# 阿里巴巴 T-HEAD 玄铁 C910 微架构

玄铁 C910 是阿里巴巴旗下 T-HEAD 半导体（平头哥）推出的第一款乱序执行 RISC-V 处理器核心，也是中国在高性能 RISC-V 领域最早的可量产实现之一。C910 既承载技术探索，也承载战略意图——阿里巴巴希望通过自主可控的 RISC-V 核心 IP，减少对美英企业 ISA（x86-64、Arm）的依赖。

## 总体概览

C910 是 3-wide 乱序核心，12 级流水线，目标工作频率 2~2.5 GHz（TSMC 12nm FinFET），量产搭载于 TH1520 SoC（1.85 GHz）。核心面积约 0.8 mm²（12nm），动态功耗约 0.2 W（2 GHz，不含静态与片外）。T-HEAD 支持最多四核簇构型，各簇共享 L2 缓存，最大 8 MB。C910 核心已部分开源，可从 RTL 读取部分实现细节。

## 前端

指令缓存为 64 KB、2-way 组相联，采用 FIFO 替换策略，原始存储量约 83.7 KB（含 4 bit/16-bit slot 预解码元数据）。取指阶段并行读取两路数据（256 bit 指令 + 64 bit 预解码），通过 16 slot 早期解码器进行 IP 阶段预处理，再经标签匹配丢弃未命中路。

分支预测采用 bi-mode 结构：1024 项选择表 + 两张 16384 项历史表（含 2-bit 计数器）+ 22-bit 全局历史寄存器，总存储约 17.3 KB。BTB 1024 项（4-way），前跳延迟 2 周期，BTB Miss 4 周期（L1i 命中）。返回栈 12 项，间接分支跳转表 256 项。这一规模对于低功耗核心是合理选择，但与现代高性能核心（Qualcomm Oryon 仅方向预测器即 80 KB）相比差距悬殊。

指令缓冲区含 32 项队列 + 16 项循环缓冲（loop buffer），功能类似 Pentium 4 trace cache，可在小循环场景减少前端气泡。

## 乱序执行引擎

C910 的 ROB 定义为 64 条目，但 T-HEAD 论文声明实际可持有 192 条指令，微基准测试结果与此吻合。这一 ROB 规模与 Intel Haswell（2013 年）相当，理论上优于 P550 和 Goldmont Plus。然而其他结构未能匹配：整数调度器仅 16 项（P550 为 40 项，Goldmont Plus 为 30 项），整数寄存器文件在 32 个体系结构寄存器保留之后仅剩 64 项乱序槽位（FP 侧仅剩 32 项），远小于 Haswell 的对应规模。这是 C910 乱序窗口在实测中常常无法填满的根本原因。

执行端口共 8 个：2 个标准整数 ALU 端口、1 个分支端口、3 个内存端口（含 AGU），以及 2 个 FP/向量端口。FP 执行延迟 3~5 周期，支持 128-bit 向量操作，向量 ISA 为 RVV 0.7.1（T-HEAD 后续 C920 升级至 RVV 1.0，其余不变）。

## 内存子系统（核心弱点）

L1 数据缓存 64 KB、2-way、3 周期延迟，分 4 字节 bank。非对齐访问有硬件支持，不跨 16B（load）或 8B（store）边界时几乎无额外开销——这一点优于 P550（P550 需 OS trap 软件模拟，耗费约 1062 周期）。

L2 缓存 1 MB（可配至 8 MB）、16-way、60 周期延迟，多核共享。这 60 周期的 L2 延迟是 C910 最严重的设计缺陷之一——甚至高于 P550 的 L3（4 MB，约 38 周期）。多核 L2 读带宽仅约 12.6 GB/s（四核合计），写带宽 23.81 GB/s，远低于 P550 L3 带宽。C910 没有 L3 缓存，L1 Miss 直接进入这个慢而窄的 L2，无任何中间缓冲。

DRAM（LPDDR4X-3733）实测带宽约 4.2 GB/s（多线程），延迟 133.9 ns。绝对延迟尚可，但带宽严重不足，即便是向量化应用也难以喂饱。

## 核间一致性

四核集群内核间传输延迟明显优于 P550（P550 四核集群内超过 300 ns），体现 T-HEAD 在 CIU（Cluster Interface Unit）实现上的一定功力。

## 性能定位

在 SPEC CPU2017 对比中，C910 在整数测试中无一能击败时钟更低的 P550，在浮点测试中赢得部分但无法保持整体领先。Cortex A55 在高频、低内存延迟配置下可追平两者。C910 的高 ROB 容量是纸面参数，实际执行中调度器容量和 L2 带宽/延迟才是真正瓶颈。

C910 展示了 T-HEAD 在乱序 RISC-V 设计上的初步成果，但也暴露出"基本功"的不扎实。非对齐访问处理和向量扩展支持是其相对 P550 的优点，但这些边界特性难以弥补内存子系统的系统性短板。

## 相关

- [[computer-systems/sifive-p550-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/memory-hierarchy]]
- [[computer-systems/cortex-a73-microarchitecture]]

## Sources

- [[sources/chipsandcheese-xuantie-c910]]
- [[sources/chipsandcheese-riscv-2025]]
