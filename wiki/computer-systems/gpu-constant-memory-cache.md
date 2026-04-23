---
tags: [gpu, nvidia, 缓存, constant-memory, 内存延迟]
date: 2026-04-19
sources: 1
---

# GPU Constant Memory 专用缓存层次

CPU 只有一种可读写的内存视图，GPU 不是——constant memory 是只读的、shader 从它读取 uniform 参数。Nvidia 为 constant memory 维护一套**独立于 global memory** 的缓存层次，而 AMD 则与 global memory 共用同一 cache 路径。这一差异在微基准里会显示成两种形态截然不同的延迟曲线。

## Nvidia 的三级 constant cache

Chester Lam 的实测显示 Nvidia 从 Fermi 一直到 Ampere 都有明确的 constant cache 层次：

- **L1 constant**：2 KB（Fermi 为 4 KB），延迟比 Ampere/Turing 的 global-memory L1 还略低——也许该叫 L0
- **L1.5 constant**：Fermi → Pascal 为 32 KB；Turing 升到 48 KB（论文说 46 KB，实测偏向 48）；Ampere 再升到至少 64 KB
- **L2**：超出上述容量后 constant 数据溢出到普通 L2

实验上有个局限：OpenCL 每 kernel 最多可分配 64 KB constant 数据，所以 Ampere 的 L1.5 实际上可能比 64 KB 更大，测不到。

## Pascal 的特殊点

Pascal 的 global memory L1 对 OpenCL 计算 workload 不可见（要回到 Fermi 才见），但 constant memory 仍然有完整的 L1 / L1.5 / L2 三级。这种"compute 走 L2，constant 走 L1"的分流设计在 Pascal 时代是一个有趣的工程选择。

## AMD 的对照

AMD GPU 测试 constant memory 时给出的延迟曲线与 global memory 几乎一致——没有独立的 constant cache 层次，只是标注 memory 类型而已。这与 AMD 统一使用 scalar unit 读取 SGPR 数据的架构思路一致：uniform-per-wave 的数据走 scalar path，不需要独立的数据 cache 层级。

## 实践含义

对 shader 作者而言：Nvidia 上把常量塞进 `__constant__`（或 OpenCL `constant` 地址空间）能命中比 global 更低延迟的 cache；AMD 上这种区分对延迟几乎无帮助，但仍有意义——它能让编译器决定是否走 SGPR path。跨厂的 uniform-heavy shader 性能画像并不对称。

此现象与 [[gpu-memory-hierarchy-latency]] 共同描绘 GPU 缓存的全景，也对 [[gpu-latency-microbench-methodology]] 提出额外要求——同一工具要能独立测 constant 和 global。

## Sources

- [[sources/chipsandcheese-gpu-memory-latency-impact]]
