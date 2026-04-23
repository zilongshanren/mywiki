---
tags: [gpu, 内存, 缓存, 延迟, rdna2, ampere, 微基准]
date: 2026-04-19
sources: 1
---

# GPU 多级缓存延迟实测

CPU 的缓存延迟测量已是惯例，GPU 也同样构建了多级缓存层次来弥补 GDDR/HBM 的高延迟。Chester Lam 利用 OpenCL pointer chasing 微基准，对多代 AMD 和 Nvidia GPU 的各级缓存延迟进行了系统实测，揭示了截然不同的设计哲学。

## RDNA 2 vs Ampere

AMD RDNA 2（RX 6800 XT）构建了三级缓存：SM 私有 L0、共享 L1、以及大容量的 Infinity Cache（L2）。实测显示，从 L0 出发到达 Infinity Cache 的延迟仅约 86 ns（+20 ns over L1），而 Nvidia Ampere（RTX 3090）从 SM 私有 L1 到达 L2 就需要超过 100 ns。

令人意外的是，RDNA 2 穿越三级缓存到达 VRAM 的总延迟（约 226 ns）与 Ampere 的两级缓存到 VRAM 的延迟大致相当——RDNA 2 在途中多了两次缓存检查却没有付出更高的最终内存延迟。这源于 Infinity Cache 极低的增量延迟（~20 ns over L1 hit）：它像一个快速的 L3，而非传统意义上的大延迟末级缓存。

对于低分辨率或小工作集的场景，RDNA 2 的缓存层次优势更加突出：小数据集可在低延迟的 L1/Infinity Cache 中命中，Ampere 的高 L2 延迟此时就成为瓶颈。

## GPU 与 CPU 的延迟鸿沟

将同一 OpenCL 程序在 CPU 上运行（Intel i7-4770 Haswell + DDR3-1600 CL9），结果令人印象深刻：Haswell 访问 DRAM 的往返时延仅 63 ns，而 RDNA 2 的 GDDR6 访问需要 226 ns。这一差距源于两个原因：

1. GPU 的内存控制器到 GDDR6 本身延迟更高（GDDR6 频率更高但 I/O 往返代价大）。
2. CPU 的缓存层次距离内存控制器更近，访问路径更短。

若将 GDDR6 理论上接上 CPU 内存控制器（以 Haswell L3 miss delta + GDDR6 raw delta 估算），等效延迟约 133 ns，仍高于 DDR 服务器内存的典型值，但差距并非不可接受。

## 历代 Nvidia 架构对比

Maxwell 与 Pascal 延迟特性相近（Nvidia 未对 OpenCL 开放 L1 texture cache，所以测量从 L2 开始）。Turing 开始出现与 Ampere 类似的结构：相对低延迟的 L1 + L2 两级体系。GTX 980 Ti 因较大的 die 和较低的时钟频率，L2 延迟偏高，暗示片上信号传播路径也是延迟的组成部分。

## 历代 AMD 架构对比

从 Terascale → GCN → RDNA 2，AMD 各级缓存的延迟呈现出明显的逐代下降趋势。GCN 与 RDNA 2 的行为符合预期，Terascale 的异常低延迟现象（小于 32 KB 时）可能源于 vertex reuse cache 的干扰，原因尚不明确。

## 方法学

测试以 OpenCL pointer chasing 实现：在大数组中随机游走，每次加载取下一个地址，强制串行访问，排除预取和并行度的干扰。不同数组大小对应不同缓存层次的命中。这一方法与 CPU 端的 pointer chasing 缓存延迟测量完全类比，便于跨平台对比。

## 参见

- [[memory-hierarchy]]
- [[gpu-latency-hiding]]
- [[cache-friendliness]]
- [[cuda-memory-hierarchy]]
- [[zen2-microarchitecture]]

## Sources

- [[sources/chipsandcheese-gpu-memory-latency]]
