---
tags: [source, gpu, amd, rdna4, memory, wave, vmcnt, out-of-order]
date: 2026-04-27
sources: 1
---

# RDNA 4's "Out-of-Order" Memory Accesses（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 3 月的文章，通过实验验证了 RDNA 4 中跨 wave 内存伪依赖消除的实际效果，并将其与 Intel、Nvidia 的历史实现作对比。

## 摘要

AMD 的 RDNA 3 及更早架构存在一个隐蔽的性能缺陷：不同 wave 的内存访问必须按全局顺序返回，导致某个 wave 的缓存未命中可以阻塞另一个 wave 的缓存命中数据的消费。作者通过一对 wave（一个指针追逐 1 GB 大数组触发缓存缺失，另一个高频读取小数据集触发命中）验证了这一现象：在 RDNA 3 上，快 wave 的访问量与慢 wave 完全按循环展开比例锁定。RDNA 4 彻底消除了这种跨 wave 等待，两个 wave 的执行完全解耦。此外，RDNA 4 还将 `vmcnt` 拆分为多个独立计数器（全局内存、纹理采样、光线相交测试各自独立），让编译器可以只等待特定类型的访问完成，减少无谓的同步停顿。Intel（至少 Gen 9 起）和 Nvidia（Turing 起）历来没有这一跨 wave 伪依赖问题。

## 关键要点

- RDNA 3 的共享内存访问队列按序返回，波前间形成伪依赖
- RDNA 4 引入每 wave 独立队列（或乱序释放机制），消除跨 wave 等待
- `vmcnt` 拆分为全局内存、纹理采样、光线相交测试三类独立计数器
- `lgkmcnt` 同样拆分为标量内存（`kmcnt`）和 LDS 访问（`dscnt`）
- Intel Xe-LPG、Xe2 及 Nvidia Turing+ 无此跨 wave 伪依赖问题
- Nvidia Pascal 在同一 SM sub-partition 内的 wave 之间存在类似问题

## 链接到的概念

- [[computer-systems/rdna4-ooo-memory]]
- [[computer-systems/rdna4-architecture]]
- [[computer-systems/gpu-latency-hiding]]

## 原文

- 链接：https://chipsandcheese.com/p/rdna-4s-out-of-order-memory-accesses
- 本地：`raw/articles/chipsandcheese.com/2025-03-23_rdna-4-s-out-of-order-memory-accesses.md`
