---
tags: [cpu, amd, infinity-fabric, memory-latency, zen, interconnect, qos]
date: 2026-04-27
sources: 1
---

# Infinity Fabric 带宽负载下的延迟特性

AMD 的 Infinity Fabric 是一套多层次互联结构，让 AMD 能够灵活组合 CCX（Core Complex）、CCD（Core Complex Die）和 IO Die，实现高核心数扩展。这套架构在追求扩展性的同时，也在高带宽负载下引入了多层叠加延迟的风险。

## 互联层次

自 Zen 2 起，AMD 桌面/服务器平台采用三层拓扑：

1. **CCX 内**：多核共享 L3，通过 **XI（eXternal Interface）** 模块与外部通信，XI 有固定大小的请求队列；
2. **CCD 到 IO Die**：通过 **IFOP（Infinity Fabric On-Package）** 链路，每 CCD 提供 32 B/cycle 读 + 16 B/cycle 写（以 FCLK 计）；
3. **IO Die 到 DRAM**：内存控制器，须应对 bank conflict、refresh、bus turnaround 等调度开销。

每一层都有固定队列容量，一旦上游核心产生的请求超过队列可吸收的速率，延迟会在各层叠加。

## Zen 各代的队列容量演进

| 架构 | CCX 结构 | XI 队列项（推算） |
|------|----------|-------------------|
| Zen 2 | 两个 4 核 CCX / CCD | 每 CCX 约 64 项，合计 ~128 |
| Zen 3 | 单个 8 核 CCX | 192 项（AMD Hot Chips 33 披露） |
| Zen 4 | 单个 8 核 CCX | 未公开，推测略高于 Zen 3 |
| Zen 5 | 单个 8 核 CCX，双 XI | 推测约 320 项（两块各 ~160） |

Zen 4 的问题在于：单核带宽能力跃升至约 50 GB/s，远超前代，少量核心即可把 XI 队列打满，导致延迟敏感线程遭受严重排队延迟（软件可见延迟可超过 700 ns）。

## CCD 隔离的 QoS 效应

将延迟敏感线程与带宽密集线程分置于不同 CCD 可显著降低竞争，原因是两个 CCD 各自拥有独立的 XI 和 IFOP 链路，不会直接共享队列资源。Zen 4 上实测：

- **同 CCD 场景**：5 个带宽线程可将延迟测试线程推至 400+ ns；
- **跨 CCD 场景**：即使对端 CCD 满载，延迟测试线程仍可维持在 100 ns 以下。

这一特性使 AMD 双 CCD 设计天然具备一定的软件 QoS 能力，调度器若能感知 CCD 拓扑并将延迟/带宽负载分开放置，可获得明显收益。

## 多层延迟叠加

一旦竞争同时发生在 CCX XI 和 IFOP 两个层次，延迟延迟是近似相加的。AMD 的 Zen 4 PPR 提供的 `XiSampledLatency` 性能计数器事件可独立观测 L3 miss 后到数据返回的 XI 层延迟（约 166~200 ns），与软件端 700+ ns 之间的差距正反映了请求在队列中等待的额外时间。

## 与 Intel 的对比

Intel 桌面平台（如 Comet Lake）采用环形或 mesh 总线直连所有核心与 LLC，无 CCD 级隔离层，加载所有核心时延迟约 234 ns——比 Zen 2 全载更差，但比 Zen 4 同 CCD 全载更好。Intel 平台的延迟行为整体更线性，缺少 AMD 多层结构带来的 QoS 隔离机会，也缺少其叠加延迟的风险。

## 实际影响

Chester Lam 在 Cyberpunk 2077、BG3、RawTherapee 等实际负载上的测试显示，典型游戏产生的 L3 miss 带宽（10~15 GB/s）远未达到触发 Infinity Fabric 排队的阈值，VCache 通过减少 L3 miss 进一步降低了 IFOP 负载。RawTherapee 等多线程高带宽任务可把内存子系统推至极限，此时与游戏并行运行会造成明显的延迟干扰。

## 相关

- [[amd-trinity-northbridge-interconnect]] — Infinity Fabric 前身：Trinity Northbridge Garlic/Onion 双链路设计

## Sources

- [[sources/chipsandcheese-infinity-fabric-limits]]
