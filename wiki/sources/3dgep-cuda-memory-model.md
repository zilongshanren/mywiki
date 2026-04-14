---
tags: [source, cuda, gpu, 内存]
date: 2026-04-14
sources: 1
---

# CUDA Memory Model（Jeremiah van Oosten / 3dgep.com）

[[jeremiah-van-oosten]] 于 2011 年 11 月发表的 CUDA 系列文章，系统讲解 CUDA kernel 可见的五种内存及其使用策略，并用矩阵乘的 tiling 优化展示片上 shared memory 的收益。

## 摘要

CUDA 应用能看到 register、local、shared、global、constant 五种内存，区别来自物理位置（片上 cache vs 片外 device memory）、作用域（线程 / block / 应用）和可写性。register 和 shared 位于片上，延迟接近 1 个时钟；local、global、constant 位于 device memory，未命中缓存时延迟约慢 100 倍。作者强调一个反直觉点：local memory 的 "local" 只是作用域意义上的本地，物理上和 global 一样慢——当 kernel 声明的变量超过寄存器预算就会 register spill 到 local。文章用矩阵乘做案例：朴素实现里 A 的一行被重复读 M 次，B 的一列被读 N 次；tiling 版本让每个 block 把一对 `BLOCK_SIZE × BLOCK_SIZE` 瓦片先搬进 shared memory，`__syncthreads()` 同步后在 shared 里做乘累加——实测 512×512 矩阵从 45ms 降到 15ms。最后讨论占用率（occupancy）与 register / shared memory 预算的硬约束。

## 关键要点

- **五种内存 + 物理位置**：register/shared 在片上；local/global/constant 都在 device memory，但 constant 有专门缓存
- **Local memory 是假本地**：它只是"线程私有作用域"的名字，物理上和 global 一样慢，register spill 会落到这里
- **Shared memory 是程序员可控的片上 cache**：`__shared__` 声明，生命周期是 block，容量 16–48KB，需要 `__syncthreads()` 做 block 内同步
- **Tiling 模式**：把 global memory 读次数从 O(N) 降到 O(N/BLOCK_SIZE)，典型收益 3× 以上
- **Occupancy 权衡**：register 数 × 线程数、shared 内存 × block 数 都会限制驻留 block 的数量，进而影响 GPU 用 warp 切换掩盖 memory latency 的能力
- **指针不带位置信息**：`__constant__ float*` 中的 const 只修饰指针本身，不代表它指向 constant memory

## 链接到的概念

- [[cuda-memory-hierarchy]]
- [[memory-hierarchy]]
- [[latency-vs-throughput]]
- [[locality-principle]]
- [[flynn-taxonomy]]

## 原文

- 链接：https://www.3dgep.com/cuda-memory-model/
- 本地：`raw/articles/3dgep.com/2011-11-25_cuda-memory-model.md`
