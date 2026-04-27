---
tags: [cpu, 微架构, centaur, via, x86, avx-512, 边缘计算]
date: 2026-04-27
sources: 3
---

# Centaur CNS：最后的第三条 x86 路线

CNS（Centaur Network Server 核）是 VIA 旗下 Centaur 设计团队在 2019 年前后披露的服务器级 x86 核，也是 Centaur 有史以来最雄心勃勃的微架构——它是**第一个非 Intel 实现 AVX-512 的 x86 核**，对标 Intel Haswell 级别的 IPC，但以极小的面积达成目标。2021 年 Intel 以 1.25 亿美元收购 Centaur 设计团队，CNS 的量产计划就此终结。

CHA 是搭载 CNS 的 SoC 芯片名称，集成了八颗 CNS 核、NCore 机器学习加速器、16 MB LLC、四通道 DDR4 控制器以及 44 条 PCIe 通道，采用台积电 16nm 工艺，die 面积仅 194 mm²。

## 前端

CNS 的分支预测器能处理最长 24 级的历史模式（Haswell 是 16 级），同时对 512 个以上的间接分支跳转目标不明显掉速，但受限于 7 级的 return stack（Haswell 16 级，Zen 31 级），深层调用树会遭遇显著惩罚。

取指带宽方面，在 L1i 命中的 2 KB 范围内可达 32 B/cycle，但超出后快速下降到约 16 B/cycle（L2 级别），与 Haswell 行为类似。CNS 加入了一个约 24 条目的指令队列兼 loop buffer——只要循环完全驻留其中，就能旁路预解码限制，以 5 IPC 运行。BTB 与 L1i 深度绑定：循环规模超过 32 KB 时会出现明显惩罚，分支间距开销约为 3 cycle/taken branch，略逊于 Haswell 的 2 cycle。

## 后端与执行单元

ROB、scheduler、FP 寄存器堆等关键结构与 Haswell 规模相当，但出彩的是执行单元的灵活性：

- **四条 ALU 管道**，rotate/shift/PDEP/PEXT 均可在全部或更多管道中执行，整数乘法两条，均优于 Haswell 的单一复杂整数管道配置
- **FP/vector**：2×256-bit FP add/mul（3 周期延迟），FMA 同 Haswell（5 周期），AVX-512 指令拆成两条 256-bit micro-op 执行，不提升吞吐但可受益于 mask 指令和专用 ISA
- **地址生成**：2 个 AGU（Haswell 3 个），但写带宽高达 64 B/cycle，理论峰值 L1D 读写混合可超 90 B/cycle

store forwarding 整体健壮，完全包含型 forwarding 为 7 周期，可支持 2 load + 2 store/cycle（Haswell 在此须等到 Sunny Cove 才实现）；但 partial overlap forwarding 代价较高（21 周期）。

## 缓存层次与互连

以 2.2 GHz 工程样片测量，L1D 延迟 5 周期（略高于 Haswell 的 4 周期），L2 也慢一周期，L3 以周期数计同样落后。但**L2 读带宽接近 64 B/cycle**，超过 Intel 同时期设计。环形总线每停 64 B/方向，带宽随核心数线性扩展，八核满载 L1 带宽超 1.6 TB/s、L2 约 1.1 TB/s。

NUMA/多路方面详见 [[numa-multi-socket-design]]。

## Die 面积哲学：密度优先

在 TSMC 16nm 上，194 mm² die 里 CNS 核+L3 仅占约三分之一，NCore 加速器占据等量面积，剩余为 IO/互连。相比之下，Intel 同核数的 Haswell-E 大一倍，其核心面积占比近 50%。CNS 核实现这一密度的核心选择：

1. 低频率目标（2.5 GHz 量产），使用高密度 cell library
2. AVX-512 以最小面积方案实现：mask 寄存器与 GPR 共用同一物理寄存器堆，256-bit 执行单元拆两条 micro-op 而非加宽至 512-bit
3. IPC 目标保守（Haswell 对标而非追赶 Skylake），避免出于 ROB/scheduler 边际收益而膨胀面积

仿真数据显示，即使是 Golden Cove 这样的高 L3 延迟芯片，ROB 超过 200 条目后也只有显著收益递减——CNS 的选择因此在目标场景下是理性的。

## 与同类的比较定位

- 对比 Haswell：IPC 大致相当，branch prediction 略弱，向量执行灵活性更强，整数内存吞吐落后（2 AGU vs 3 AGU）
- 对比 Zen 2 及之后：单线程性能差距大，无 SMT，时钟频率低；但在重度 AVX-512 scalar/vector 负载（如 Y-Cruncher）上受益于 ISA 扩展能短暂持平甚至领先
- 定位：边缘推理服务器，CNS 负责"足够的 CPU 算力"，NCore 提供核心 ML 吞吐（~6.8 TFLOPS bfloat16），两者共享片上低延迟互连

Intel 收购 Centaur 团队的原因众说纷纭（NCore IP、工程师资源、减少 x86 授权方……），官方从未说明。Zhaoxin 通过 VIA 于 2020 年获得了部分 CPU IP，后续是否会推出 CNS 派生核尚存疑。

## 参见

- [[via-x86-isaiah-lujiazui]] — Centaur 此前的低功耗 x86 路线
- [[numa-multi-socket-design]] — CHA 双路实现的瑕疵分析
- [[golden-cove-microarchitecture]] — 对应时期的 Intel P-Core
- [[gracemont-microarchitecture]] — Intel E-Core，密度目标与 CNS 类似
- [[dispatch-stall-breakdown]] — ROB 利用率与调度器容量的权衡

## Sources

- [[sources/chipsandcheese-via-centaur-cns]]
- [[sources/chipsandcheese-centaur-cha-dual-socket]]
- [[sources/chipsandcheese-centaur-cha-die]]
