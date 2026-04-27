---
tags: [gpu, register-file, occupancy, rdna3, ada-lovelace, latency-hiding, wave]
date: 2026-04-27
sources: 1
---

# GPU 寄存器文件与占用率

GPU 没有乱序执行引擎，依靠线程级并行（TLP）来隐藏缓存和内存延迟：当一个线程停在等待数据时，调度器切换到另一个就绪线程。能同时跟踪的线程数——即占用率（occupancy）——因此直接影响延迟隐藏能力。而占用率的主要限制因素往往是寄存器文件容量。

## 寄存器文件是瓶颈

与 CPU 的固定逻辑寄存器数量不同，GPU 在 SIMD/SMSP 粒度上动态分配寄存器文件给活跃线程。一个线程用的寄存器越多，能同时运行的线程就越少：

> 可同时运行线程数 ≈ 寄存器文件容量 / 每线程寄存器用量

这意味着编译器的寄存器分配决策直接影响运行时占用率，而占用率又影响延迟隐藏效果，最终体现在吞吐率上。

## RDNA 3 vs Ada Lovelace

以 Starfield 分析帧为例：

| 指标 | RDNA 3（7900 XTX）| Ada Lovelace（RTX 4090）|
|------|------------------|------------------------|
| SIMD 向量寄存器文件 | 192 KB | 64 KB |
| 编译器分配（Shader 1）| 132 → 144 寄存器/wave | ~128 寄存器/wave |
| 理论最大 wave 数 | 10 waves/SIMD | ~4-5 waves/SMSP |
| 实测占用率（Shader 1）| ~10 waves | ~4-5 warps |

RDNA 3 的 192 KB 寄存器文件是 Nvidia SMSP 64 KB 的三倍，允许在同等寄存器分配下保持更高占用率。对于 texture sampling 密集的 shader（L1 cache 延迟仍有数百 clock），更高占用率能隐藏更多延迟。

值得注意的是，[[rendering/rdna3-architecture|RDNA 3]] 分配寄存器的粒度为 24 个寄存器（即 132 向上取整至 144）。编译器会在寄存器压力与占用率之间权衡；某些 shader 可能精确使用到 192 KB 的上限（如以 96 寄存器×2KB/wave = 正好填满）。

## Wave64 与寄存器加倍

RDNA 3 支持 wave64 模式（64-wide 向量，double-pump 通过 32-wide 执行单元）。Wave64 下每线程等效消耗双倍寄存器文件容量，占用率下降。若 shader 被编译器选择以 wave64 运行，即使每线程名义寄存器数不变，SIMD 可同时活跃的 wave 数也减半。在某些以 L2 带宽为瓶颈的 shader 中，更多占用率无法提升带宽利用率，wave64 模式不会带来额外损失，有时反而因更宽的 SIMD 执行获益。

## 高占用率不总是关键

占用率是工具而非目标。在带宽受限（L2 bandwidth bound）的 shader 中，堆叠更多线程不增加带宽，只会增加队列压力。在延迟受限、工作集适合 L1 cache 的 shader 中，甚至一个线程也能填满执行单元。高占用率最有用的场景：延迟高（texture sampler、L2 miss）且执行单元容量相对于延迟"空着跑"。

## Nvidia 的设计取舍

Nvidia 削减单 SMSP 的寄存器文件容量，以允许在相同 die 面积内放更多 SM。更多 SM 在寄存器需求少的 shader 下可获得接近线性的吞吐提升。这一策略在 Starfield 整帧层面仍使 RTX 4090 领先（128 SM vs 48 WGP），但对寄存器需求较高或 L2 带宽受限的 shader 失去优势。详见 [[rendering/gcn-wave-occupancy]]。

## Sources

- [[sources/chipsandcheese-starfield-gpu]]
