---
tags: [source, cpu, amd, zen5, 游戏负载, 微架构]
date: 2026-04-27
sources: 1
---

# Running Gaming Workloads through AMD's Zen 5（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 8 月的文章，以 Ryzen 9 9900X（DDR5-5600）为测试平台，使用 AMD 性能计数器对 Palworld、COD Cold War 和 Cyberpunk 2077 做 top-down 分析，与同系列 Lion Cove 游戏文章形成对照。

## 摘要

与 Lion Cove 相比，Zen 5 的游戏瓶颈呈现互补格局：前端延迟（Frontend Latency Bound slots）占主导地位，而后端内存延迟次之。Zen 5 的 6K entry op cache 覆盖率高，但单线程 op cache 吞吐约 6 µop/cycle，低于 8-wide 重命名器额定值；分支预测准确率略低于 Lion Cove（跨三款游戏一致）。后端侧，整数寄存器堆容量是最常见的资源瓶颈，ROB 利用率较高。L3 和 DRAM 延迟低于 Arrow Lake 平台（在大多数游戏中），但前端延迟问题掩盖了这一优势。文章还通过强制跨 CCX affinity 实测发现 7% 的性能下降，量化了跨 CCX 流量对游戏的边际影响。

## 关键要点

- Zen 5 游戏瓶颈：前端延迟 > 后端内存延迟，与 Lion Cove 相反
- Op cache 命中率高但单线程吞吐约 6 µop/cycle，低于额定 12 µop/cycle 和 8-wide renamer 速率
- 前端停顿平均约 11–12 个周期，接近 L2 延迟，暗示 op cache miss 是主因
- 整数 RF 容量是后端资源停顿的主要原因；FP RF 停顿已被 NSQ 设计消除
- 后端 DRAM 延迟（Palworld/Cyberpunk）比 Arrow Lake 略好，COD Cold War 稍差
- 跨 CCX（Ryzen 9900X 双 CCX）强制分配时，Cyberpunk 性能下降约 7%；正常游戏几乎不产生跨 CCX 流量
- L3/DRAM 命中率：Zen 5 L3 命中率 55–68%，大多数 miss 到 DRAM，跨 CCX 流量可忽略不计
- 分支预测准确率高但略低于 Lion Cove，mispredicts per instruction 更多（原因不明）

## 链接到的概念

- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/lion-cove-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/memory-hierarchy]]
- [[computer-systems/infinity-fabric-loaded-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/running-gaming-workloads-through
- 本地：`raw/articles/chipsandcheese.com/2025-08-02_running-gaming-workloads-through-amds-zen-5.md`
