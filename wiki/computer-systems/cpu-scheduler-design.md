---
tags: [cpu, 微架构, 调度器, 后端, 乱序执行]
date: 2026-04-19
sources: 1
---

# CPU 后端调度器设计

调度器（Reservation Station / Scheduler）是乱序执行 CPU 后端的核心结构。它保存已派发但尚未执行的微操作，每个周期检查哪些微操作的操作数已就绪，并将它们发送到对应的执行单元。调度器的容量和组织方式直接决定了 CPU 对长延迟操作（如缓存缺失、除法）的容忍能力。

## 统一调度器 vs 分布式调度器

调度器在设计上存在两种主要范式：

**统一调度器（Unified RS）**：所有类型的微操作共享一个调度队列。优点是灵活——整数操作多时可把空位给整数端口，反之亦然。Intel Skylake 采用此方案，调度器共 97 个条目。

**分布式调度器（Distributed RS）**：为不同端口或执行单元分配独立的小队列。可以为每种功能单元单独调优；但按 Henry Wong 的论文，相同总条目数下，统一调度器的 IPC 通常更高，因为分布式方案存在某些端口满而其他端口空的结构性浪费。Zen 2 采用分布式方案：每个 ALU 端口 16 条目、AGU 端口共 28 条目、FP 单元 36 条目，合计 128 个调度条目。

## 非调度溢出队列（Non-Scheduling Buffer）

[[zen2-microarchitecture|Zen 2]] 的 FPU 侧引入了一个 64 条目的**非调度溢出队列**，这是统一 vs 分布式之外的第三个维度。非调度队列的条目不参与每周期的就绪检查扫描，因此其实现成本远低于等规模的调度队列。微操作可以在此等待，直到 FP 调度队列出现空位再移入正式调度。

有了这个溢出缓冲，Zen 2 FPU 侧可容纳 36（调度）+ 64（非调度）= 100 个微操作而无需阻断派发，整个后端实际可见深度达 192 个微操作。AMD 的 K10（Phenom）架构同样拥有 36 条目 FP 调度器但无溢出缓冲，实测中 FPU 资源引发的后端阻塞远多于 Zen 2，印证了溢出缓冲的价值。Intel 的 Tremont 也独立引入了类似思路（micro-op overflow buffers），进一步表明这是一种业界认可的有效设计。

## 调度器满导致的派发阻塞

当调度器全满时，CPU 前端必须停止向后端派发新微操作，称为 dispatch stall。Skylake 在 CBR15 场景下后端受限周期占比为 20.1%，Zen 2 仅 15.1%。Skylake 的统一调度器满是主要原因（占其后端阻塞的一半以上），而 Zen 2 的调度器引发的阻塞不足后端阻塞的三分之一。

## 参见

- [[zen2-microarchitecture]]
- [[branch-predictor-design]]
- [[cpu-performance-formula]]
- [[latency-vs-throughput]]

## Sources

- [[sources/chipsandcheese-zen2-cinebench-analysis]]
- [[sources/chipsandcheese-zen5-hot-chips]]
