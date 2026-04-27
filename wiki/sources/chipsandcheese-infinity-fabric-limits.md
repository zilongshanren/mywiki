---
tags: [source, computer-systems, amd, infinity-fabric, memory-latency, zen4, zen5, zen2]
date: 2026-04-27
sources: 1
---

# Pushing AMD's Infinity Fabric to its Limits（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2024 年 11 月的文章，通过在带宽压力下测量内存延迟，系统剖析 AMD Infinity Fabric 多层互联的排队竞争机制。

## 摘要

作者编写了一套"带宽施压下的延迟观测"工具：一个线程持续做指针追踪（latency-sensitive），同时逐步增加生成带宽负载的线程数，记录延迟随并发线程数的变化曲线。测试覆盖 Zen 2（两 CCX/CCD）、Zen 4（Ryzen 9 7950X3D）、Zen 5（Ryzen 9 9950X + DDR5-8000）三代平台。

核心发现：Zen 4 在单 CCD 内带宽竞争时延迟上升最剧烈（可超过 700 ns），根本原因在于 Zen 4 单核每秒可消耗约 50 GB/s DRAM 带宽，远超前代，导致 XI 队列（L3 与 Infinity Fabric 之间的接口模块）迅速打满。Zen 5 对同一场景的处理明显改善，推测原因是每 CCX 配备两个 XI 模块（共约 320 个请求队列项）、以及 DDR5-8000 配置令 IFOP 负载率降低。CCD 边界天然形成 QoS 隔离——将延迟敏感线程与带宽密集线程分置于不同 CCD 可显著降低竞争。Zen 2 由于单核带宽能力弱，即使 DRAM 利用率更高也不易把 XI 队列打满，延迟反而更可控。

文章还利用 Zen 4 L3 性能计数器的"XiSampledLatency"事件，验证了 XI 层观测到的平均延迟（约 166~200 ns）远低于软件测量的端到端延迟（700+ ns），说明延迟在 XI → IFOP → DRAM 各层级叠加，对少数请求而言尤为严重。实际游戏测试（Cyberpunk 2077、BG3）表明，典型桌面负载远未压到这些极限，VCache 通过减少 L3 miss 间接降低了对 Infinity Fabric 的压力。

## 关键要点

- Zen 4 单核 DRAM 带宽能力约 50 GB/s，极易在 CCD 内引发 XI 队列竞争
- CCD 隔离（latency/bandwidth 线程分 CCD 运行）是天然 QoS，Zen 2/4/5 均受益
- Zen 5 每 CCX 推测有两个 XI，队列项总数约 320，显著降低竞争烈度
- Zen 4 多层排队延迟可叠加：XI + IFOP + DRAM 合计可见 700+ ns 软件端延迟
- 典型游戏/生产力负载（BG3、视频编码混跑）在 VCache 帮助下远未触及带宽上限

## 链接到的概念

- [[infinity-fabric-loaded-latency]]
- [[zen4-microarchitecture]]
- [[vcache-3d-die-stacking]]
- [[numa-multi-socket-design]]
- [[memory-hierarchy]]
- [[gpu-latency-microbench-methodology]]

## 原文

- 链接：https://chipsandcheese.com/p/pushing-amds-infinity-fabric-to-its
- 本地：`raw/articles/chipsandcheese.com/2024-11-24_pushing-amds-infinity-fabric-to-its-limits.md`
