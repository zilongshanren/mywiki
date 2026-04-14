---
tags: [cuda, gpu, 内存层次, 并行计算]
date: 2026-04-14
sources: 1
---

# CUDA 内存模型

CUDA kernel 可见的**五种内存**构成一个非常刻意的层次：片上（on-chip）与片外（off-chip），共享与私有，可写与只读，几乎每一维都有用来交易的资源。优化 CUDA kernel 的第一件事，就是把数据放到正确的内存类别里，让访问延迟差 100 倍左右。

## 五种内存一览

| 类型 | 位置 | 延迟 | 作用域 | 生命周期 | 读写 |
|---|---|---|---|---|---|
| **Register** | 片上 | 极低 | 单线程 | 线程 | R/W |
| **Local** | 设备内存 | 高（~100×） | 单线程 | 线程 | R/W |
| **Shared** | 片上 | 极低 | block | block | R/W（需同步） |
| **Global** | 设备内存 | 高 | 全部线程 | 应用 | R/W |
| **Constant** | 设备内存（有缓存） | 低（命中） | 全部线程 | 应用 | host W / kernel R |

要点：

- **Register** 是默认。kernel 里的标量和编译期可解的小数组都走寄存器；超过预算就 **spill 到 local**
- **Local memory 其实在 device memory 上**——名字误导：它"本地"只是作用域上的本地，物理上和 global 一样慢
- **Shared memory** 是 block 内广播/共享的快车道，地址空间小（16KB–48KB），但延迟接近 register
- **Constant memory** 只有 64KB，但有专门缓存，同一 warp 内读同一地址基本没开销
- **Global memory** 容量最大，跨 kernel 持久，是 CPU ↔ GPU 主要通道，但延迟决定性地高

## Tiling：把全局读搬到共享

典型优化是"分块（tiling）"——以矩阵乘 `C = A × B` 为例：
- 朴素版本每个元素让一个线程完整扫 A 的一行和 B 的一列，A/B 元素被重复读 N、M 次
- 优化版本把 A、B 切成 `BLOCK_SIZE × BLOCK_SIZE` 的瓦片，每个 block 把一对瓦片从 global 搬到 shared，`__syncthreads()` 保证都就位后在 shared 里做乘累加，再进入下一对瓦片

实测 512×512 矩阵乘，朴素版 45ms，tiled 版 15ms——3 倍收益，来源只是**把读次数从 O(N) 降到 O(N/BLOCK_SIZE)**。

## 占用率（Occupancy）与资源预算

SM 的 register 数与 shared memory 大小是硬上限：

- 一个 kernel 声明了多少 register × block 线程数 → SM 能同时跑几个 block
- 一个 block 用了多少 shared memory → 同样限制驻留 block 数
- 过度使用任一资源都会降低**活跃 warp 数**，进而掩盖不了 global memory 的延迟

这个 trade-off 把 [[latency-vs-throughput]] 的哲学推到极致：GPU 用大量驻留 warp 填满 memory latency，一个 warp stall 就切到另一个。如果 occupancy 不足，stall 就真的 stall 了。

## 相关

- [[memory-hierarchy]]
- [[latency-vs-throughput]]
- [[locality-principle]]
- [[cache-friendliness]]
- [[flynn-taxonomy]]

## Sources

- [[sources/3dgep-cuda-memory-model]]
