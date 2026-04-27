---
tags: [cpu, intel, skylake, microarchitecture, x86]
date: 2026-04-27
sources: 1
---

# Skylake 微架构

Skylake 是 Intel 于 2015 年推出的微架构，也是 Intel 近年来服役时间最长的架构——在 2021 年底 Alder Lake 全面铺开之前，它的衍生变体填满了 Intel 整条产品线长达六年。这一局面并非计划所致，而是 10nm 制程反复受挫的结果：原本应在 2016-2017 年接班的 Cannon Lake 和 Sunny Cove 相继延误，Skylake 被迫一再刷新延期。

## 前端

Skylake 的前端在 Haswell 基础上加宽加深：指令字节缓冲区从 20 项扩至 25 项，解码后微指令队列从 56 项扩至 64 项（SMT 模式下每线程 28 项）。微操作缓存带宽从每周期 4 条提升至 6 条，理论上使前端达到 6-wide，但后续重命名级（rename）只有 4-wide，因此多数情况下吞吐受重命名限制。

解码器可在某条指令展开为多条微操作时达到每周期 5 微操作，但因大多数指令为单微操作，这一提升实际效果有限。L2 TLB 从 1024 项扩大到 1536 项，减少了地址转换开销。

分支预测器行为与 Haswell 相似，方向预测精度无明显变化。L1 BTB 支持 128 个目标（零气泡），L2 BTB 支持 4096 个目标（1 cycle 惩罚）。与 Haswell 相比，密集分支需要 32 字节间距（Haswell 为 16 字节）才能获得零气泡，略有退步；但超出栈深度时可回退到间接预测器，减少惩罚。

## 后端

Skylake 彻底拆分了统一调度器：原先 Haswell 的 97 项统一调度器拆分为服务数学与存储端口的 58 项调度器和服务 AGU 端口的 39 项调度器。整数寄存器文件和存储队列均有所扩大，另单独引入了 x87/MMX 物理寄存器文件——这主要是为服务端 AVX-512 的掩码寄存器需求而设，客户端 Skylake 不支持 AVX-512，这部分逻辑在客户端属于"浪费"。

执行端口布局与 Haswell 基本一致（4 整数端口、2 通用 AGU、1 存储 AGU），但浮点和向量执行能力有所加强：FMA 单元延迟标准化为 4 cycle、吞吐 2/cycle；向量整数乘法器复制到 port 0 和 1；向量整数加法可在三个向量端口（0/1/5）上执行，减少了特定 SIMD 工作负载的端口压力。

存储转发（store-to-load forwarding）几乎总能在 5 cycle 内完成，略优于 Haswell 的 5-6 cycle。

## 缓存与内存层次

客户端 Skylake 的缓存层次几乎等同于 Haswell：32 KB L1D、256 KB L2（4-way，从 Haswell 的 8-way 降低以便服务端用于扩展 L2 容量）、环形总线拓扑的分片 L3。L2 和 L3 之间的队列从 16 项扩大至 32 项，改善了 L3 带宽和内存级并行性。

服务端变体 Skylake-X 切换到 mesh 互连，最多支持 28 核，并将 L2 扩大至 1 MB 用于隔离较高延迟的 mesh L3。服务端还支持完整的 AVX-512，带来了 512-bit 加载/存储带宽翻倍以及完整的掩码寄存器文件。

## 竞争历史

Skylake 在 2015 年面世时无任何竞争对手（AMD 的 Piledriver 落后显著），但随着 Zen 系列的推进，其优势被逐步蚕食：
- **Zen 1 (2017)**：多核数量超越，单核差距拉近，分支处理仍落后
- **Zen 2 (2019)**：全宽 256-bit 向量、更大 L3 带宽、更大微操作缓存，基本追平 Skylake 单核性能
- **Zen 3 (2020)**：在几乎所有方面超越 Skylake，包括分支处理

Intel 通过 14nm 工艺优化（Kaby Lake、Coffee Lake 等）不断提升频率和核心数，延缓了 Skylake 的过时，但终究是拖延而非解决。

## 相关

- [[sunny-cove-microarchitecture]]
- [[golden-cove-microarchitecture]]
- [[netburst-microarchitecture]]
- [[cannon-lake-microarchitecture]]
- [[zen2-microarchitecture]]
- [[intel-hybrid-alder-lake]]
- [[op-cache-decoded-uop-cache]]
- [[branch-predictor-design]]

## Sources

- [[sources/chipsandcheese-skylake-architecture]]
