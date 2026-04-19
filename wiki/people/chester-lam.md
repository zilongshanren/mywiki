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

## Sources

- [[sources/chipsandcheese-gb10-cpu-memory]]
- [[sources/chipsandcheese-gb10-gpu]]
- [[sources/chipsandcheese-chipset-microbench]]
- [[sources/chipsandcheese-ccc-april-fools]]
- [[sources/chipsandcheese-split-locks]]
