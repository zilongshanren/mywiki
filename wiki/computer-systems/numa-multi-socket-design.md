---
tags: [cpu, numa, 多路, 缓存一致性, 服务器, 内存]
date: 2026-04-27
sources: 1
---

# NUMA 多路设计：延迟、带宽与一致性的三角困境

现代服务器 CPU 将内存控制器集成到 die 上，每个 socket 有自己的本地内存池，跨路访问必须借助 socket 间互联（cross-socket link）。这形成了 **Non-Uniform Memory Access（NUMA）** 架构：本地访问延迟低、带宽高；远端访问延迟高、带宽受限于互联带宽。

## 跨路延迟

典型跨路延迟增量数据（pointer chasing，1 GB 测试大小，2 MB 大页）：

| 平台 | 本地延迟 | 跨路增量 | 倍数 |
|------|---------|---------|------|
| Centaur CHA（2.2 GHz，DDR4-3200）| ~100 ns | +92 ns | ~1.9× |
| Intel Xeon E5-2660 v4（Broadwell）| ~81 ns | +42 ns | ~1.5× |
| Intel Xeon X5650（Westmere）| 70.3 ns | +50.8 ns | ~1.7× |
| AMD EPYC Milan-X（NPS2 同路跨节点）| | +14 ns | 极小 |
| AMD EPYC Milan-X（跨路）| | +70–80 ns | |

Centaur CHA 的跨路延迟增量几乎是本地延迟的等量——这表明其 cross-socket link 并未针对低延迟优化，带宽表现更为惨烈（见下节）。

## 跨路带宽的差距

跨路带宽是 NUMA 实现成熟度的更直观指标。CHA 的跨路读带宽仅约 **1.3 GB/s**，而其本地内存带宽可达 50+ GB/s。对比：

- Intel Westmere X5650（十年前）：跨路 11.2 GB/s
- Intel Broadwell（DDR4-2400）：跨路约 21 GB/s
- AMD Milan-X（每 NPS2 节点）：跨路仍可超 40 GB/s

1.3 GB/s 甚至低于高端 NVMe SSD 的顺序读带宽——这基本宣告了 CHA 的双路配置在任何 NUMA-unaware 负载下都会产生严重性能退化，也无法使用将内存交错（interleave）跨路分布的方式规避 NUMA 问题。

Chester Lam 的推断是：Centaur 实现了 cross-socket 协议和 coherency directory，但负责缓冲请求的队列从未完成验证——这是一个未完成的 work in progress，而 Centaur 被收购后自然无法续工。

## Broadwell Cluster-on-Die 的教训

Intel Broadwell 支持 cluster-on-die（CoD）模式，将一个 die 划分成两个 NUMA 节点，每个节点控制一半 DDR4 通道。启用后本地延迟略降，但跨 die 内节点的延迟惩罚接近跨路，说明**目录协议的查询层数**是延迟主因，而非物理距离。这也解释了为什么 AMD 的 NPS2 模式中同 die 跨节点开销仅 14 ns——AMD 有更快的 directory 机制。

## 核间一致性延迟（Contested Atomics）

跨路 CAS（compare-and-exchange）操作的延迟往往比"干净"内存访问展示更好的相对表现，因为一致性协议会选择将 cache line 的 home 节点直接参与仲裁，不一定要绕到远端内存。CHA 在这一测试中与 Intel/AMD 持平甚至略好（90–130 ns 范围），因为它的拓扑更简单、核数更少，绕路成本小。

然而，Contested Atomics 在真实多线程代码中极少见——这个维度上的优势几乎没有实用价值。

## 设计含义

良好的 NUMA 实现需要几个协同要素：

1. **高带宽 cross-socket link**（或片间 fabric），避免带宽成为瓶颈
2. **完备的请求队列**，能堆叠足够多的 outstanding request 以隐藏高延迟
3. **快速 coherency directory**，减少跨节点 cache miss 的仲裁开销
4. **NUMA-aware 调度与内存分配**（OS 层面），尽可能让访问落在本地节点

从 CHA 的失败案例可以看出，仅实现协议状态机是不够的，实际的带宽交付能力需要对互联 buffer 和 flow control 做完整的性能工程验证。

## 参见

- [[centaur-cns-microarchitecture]] — CNS 核心架构及 CHA SoC 整体设计
- [[cache-coherence-cross-cluster]] — 同 die 内跨 cluster 的一致性设计
- [[core-to-core-latency-lock-test]] — 核间 lock 延迟的测量方法
- [[littles-law-reorder-buffer]] — 延迟与 outstanding requests 的 Little's Law 分析

## Sources

- [[sources/chipsandcheese-centaur-cha-dual-socket]]
