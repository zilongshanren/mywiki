---
tags: [cpu, 微架构, amd, zen2, 分支预测, 调度器, 缓存]
date: 2026-04-19
sources: 1
---

# AMD Zen 2 微架构分析

Zen 2 是 AMD 于 2019 年推出的 x86-64 微架构，基于台积电 7nm 工艺制造，首次在主流桌面平台实现了对同期 Intel Skylake 的全面性能超越。Chester Lam 以 Cinebench R15 单线程场景为切入点，通过性能计数器实测剖析了 Zen 2 领先的三条主要原因：分支预测精度更高、后端非调度 FP 队列设计独特、L2 缓存更大。

## 分支预测优势

[[branch-predictor-design|分支预测器]]的精度在 Zen 2 上达到 96% 平均准确率，超越 Skylake 的 94.9%。换算为 MPKI（每千指令误预测次数），Zen 2 为 5.15，Skylake 为 6.45——后者多出 25%。更高的误预测率意味着前端需要从错误路径取更多指令，Skylake 的前端带宽浪费比 Zen 2 高出约 17%。

每次误预测的惩罚在两代架构上相似（Zen 2 约 16 周期，Skylake 约 15–20 周期），因此 MPKI 的差异直接转化为吞吐量损失。这一差距在 CBR15 的分支密集代码段尤为突出。

## 非调度 FP 队列：后端吸收延迟的关键

传统上，微操作进入后端时需同时占用重排序缓冲（ROB）和调度队列（RS）条目。Skylake 采用统一调度队列，共 97 个条目。Zen 2 改为分布式调度器：每个 ALU 端口 16 个条目、三个 AGU 端口共 28 个条目、FP 单元 36 个条目，合计 128 个调度条目，另加一个 64 条目的**非调度 FP 溢出队列**。

非调度队列不参与每周期的就绪检查，因此实现成本远低于等规模的调度队列。有了它，Zen 2 的 FPU 侧可容纳最多 100 个微操作在等待，整个后端有效可见 192 个待执行微操作。实测中，Zen 2 后端受限周期占比为 15.1%，Skylake 为 20.1%，差距主要来自调度队列压力。

## L2 缓存容量翻倍

Zen 2 配备 512 KB 的 L2 缓存，而 Skylake 仅有 256 KB，但两者 L2 延迟均为 12 周期。更大的 L2 使 Zen 2 在 CBR15 数据访问端有更高的命中率，L3 访问频率相应降低，进一步减轻后端队列压力。同时，L2 也对指令缓存侧起到兜底作用——L1i 缺失时 L2 命中率越高，前端流水线的停顿越少。

Zen 2 的 L3 容量（最大 32 MB per CCD）也远超 Skylake，使 CBR15 场景下访问 DRAM 的频率不到 Skylake 的一半。

## 相对弱项

Skylake 的 store buffer 更大，在 store 密集型负载下具有优势。Skylake 的 op cache（DSB）命中率在 CBR15 中反而高于 Zen 2（69.1% vs 62.7%），可能源于更灵活的替换策略；但在 CBR15 这种 IPC 不高的场景下，op cache 命中率与 IPC 的相关性很弱。

## 参见
- [[branch-predictor-design]]
- [[cpu-scheduler-design]]
- [[cache-friendliness]]
- [[cpu-performance-formula]]
- [[benchmark-methodology-end-to-end]]
- [[op-cache-decoded-uop-cache]] — Zen 2 op cache 的性能与功耗实测
- [[isa-implementation-not-architecture]] — ARM/x86 ISA 无关论
- [[neoverse-n1-microarchitecture]] — 同代 ARM 服务器核横向对比
- [[dispatch-stall-breakdown]] — Zen 3 派发停顿分解（沿用分析方法）
- [[golden-cove-microarchitecture]] — 同期 Intel 大核对标
- [[non-scheduling-queue]] — Zen 2 FP 侧 64 项 NSQ 是此模式的代表实现
- [[move-elimination-zeroing-idioms]] — rename 阶段消除 MOV 与 zeroing idiom 的技巧

## Sources
- [[sources/chipsandcheese-zen2-cinebench-analysis]]
- [[sources/chipsandcheese-zen2-op-cache-performance]]
- [[sources/chipsandcheese-neoverse-n1-vs-zen2]]
