---
tags: [人物, 作者]
date: 2026-04-19
sources: 5
---

# Chester Lam

[[chips-and-cheese]] 的主笔之一，长期从事 CPU 与 GPU 微架构的实测分析。本 wiki 收录的五篇文章均出自其手：GB10（Nvidia/Mediatek）CPU 与 GPU 两侧的内存子系统剖析、主板 chipset 对 PCIe 延迟/带宽的影响、x86-64 上的 split lock 跨平台横测，以及一篇以"Claude 写的 C 编译器"为切入点的 April Fools 风格但包含真实 top-down 分析的杂谈。

方法学偏好：Nemes 的 Vulkan 微基准、pointer chasing 测延迟、per-thread / shared array 双路测带宽、厂商 performance counter（AMD BKDG、Intel VTune、Arm STALL_BACKEND_MEMBOUND 等）交叉验证。

## 相关
- [[chips-and-cheese]]
- [[gb10-memory-subsystem]]
- [[gb10-gpu-blackwell-igpu]]
- [[chipset-pcie-latency]]
- [[split-lock-x86]]
- [[llm-generated-c-compiler-perf]]
- [[mcm-gpu-design]]
- [[zen2-microarchitecture]] — Zen 2 分支预测器与调度器的性能优势分析
- [[gpu-memory-hierarchy-latency]] — GPU 多级缓存延迟实测
- [[ampere-warp-stall-utilization]] — Ampere warp stall 与 shader 利用率实测
- [[gpu-latency-microbench-methodology]] — GPU 延迟微基准的方法学修正（Sattolo 随机置换）
- [[gpu-constant-memory-cache]] — GPU constant memory 专用缓存层次
- [[op-cache-decoded-uop-cache]] — Zen 2 op cache 对性能与功耗的影响
- [[isa-implementation-not-architecture]] — ISA 无关论的实测支撑
- [[neoverse-n1-microarchitecture]] — Neoverse N1 vs Zen 2 实测对比
- [[cache-size-vs-latency-tradeoff]] — 用 ChampSim 仿真比较 IBM 256 MB L3 与 AMD V-Cache 的延迟/容量取舍

## Sources
- [[sources/chipsandcheese-gb10-cpu-memory]]
- [[sources/chipsandcheese-gb10-gpu]]
- [[sources/chipsandcheese-chipset-microbench]]
- [[sources/chipsandcheese-ccc-april-fools]]
- [[sources/chipsandcheese-split-locks]]
- [[sources/chipsandcheese-nvidia-mcm-gpu]]
- [[sources/chipsandcheese-zen2-cinebench-analysis]]
- [[sources/chipsandcheese-gpu-memory-latency]]
- [[sources/chipsandcheese-gpu-memory-latency-impact]]
- [[sources/chipsandcheese-zen2-op-cache-performance]]
- [[sources/chipsandcheese-isa-doesnt-matter]]
- [[sources/chipsandcheese-neoverse-n1-vs-zen2]]
- [[sources/chipsandcheese-gigabyte-zen4-leak]]
- [[sources/chipsandcheese-ibm-l3-v-cache-future]]
- [[sources/chipsandcheese-neoverse-n1-deep-dive]]
- [[sources/chipsandcheese-zhaoxin-lujiazui]]
