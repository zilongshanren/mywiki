---
tags: [cpu, amd, hypertransport, magny-cours, opteron, numa, 互联, 多核扩展]
date: 2026-04-27
sources: 1
---

# AMD HyperTransport 与 Magny Cours 多核扩展

HyperTransport（HT）是 AMD 从 K8 时代开始用于多处理器互联的点对点高速总线协议，取代了此前的前端总线（FSB）。Magny Cours（Opteron 6000 系列，2010 年）则是 AMD 第一次将 HyperTransport 用于**同封装多 die 互联**的尝试，代表了 AMD 在 Infinity Fabric 诞生之前的高核心数扩展路线。

## Magny Cours 封装设计

Magny Cours 的核心策略是复用现有的 Phenom II X6（Shanghai，6 核）die，将两颗 die 通过 HyperTransport 链路封装在同一 G34 socket 中。这样做的好处显而易见：无需为高核心数 tape out 新 die，降低验证复杂度和掩模成本，同时改善良率。

两颗 die 的连接方式并不对称：一条 16-bit "ganged" HT 链路连接两颗 die（6.4 GT/s，提供约 12.8 GB/s 带宽），另有一条来自不同 HT 端口的 8-bit 子链路也横跨两颗 die，但 AMD 选择不使用这条链路。结果是封装内的 die 间带宽被限制在 12.8 GB/s，若使用 8-bit 链路可提升至 19.2 GB/s，但 AMD 判断其收益不足以抵消不均匀链路带来的复杂度。

每颗 die 有四个 HT 端口，封装内消耗 1.5 个端口，剩余 2.5 个端口用于外部连接——G34 接口因此可提供四个外部 HT 端口，分别用于 IO 和多路 socket 互联。

## NUMA 拓扑

一颗 Magny Cours（双 die）在双路系统中形成四个 NUMA 节点（每颗 die 有独立内存控制器），通过 HT 链路全互联：

- 同 socket 内的 16-bit 链路（快）
- 跨 socket 的 16-bit 链路（慢）
- 跨 socket 的 8-bit 对角线链路（最慢，约 4.4 GB/s）

跨节点内存延迟约 120–130 ns（本地 70–80 ns），与同期 Intel Westmere 双路相当，两者都比现代系统具有更低的跨节点延迟惩罚。

## HyperTransport 性能实测

跨节点内存带宽测试揭示了 Magny Cours 的一个关键弱点。从理论上，每个 NUMA 节点有 DDR3-1333 双通道，理论带宽 21.3 GB/s；但实测单 die 带宽仅约 10.4 GB/s，约为理论值的 49%。瓶颈在于 Northbridge 时钟频率（1.8 GHz）低以及内存控制器队列深度不足，无法充分吸收 DDR3 访问延迟产生的排队。

## 片上互联：Northbridge（SRI + XBAR）

Magny Cours 延续了 AMD K8 以来的两级 crossbar Northbridge 设计（与 [[amd-trinity-northbridge-interconnect]] 中描述的 Trinity 使用相同架构）：

- **SRI（System Request Interface）**：CPU 核心的接入点，含 32 项系统请求队列（较早期 K8 的 24 项提升）
- **XBAR**：连接 SRI 与内存控制器、HT 链路，含 56 项 XCS 调度队列

Crossbar 拓扑的优点是简单、有序、延迟低——基础内存延迟仅约 72 ns，在 2010 年的服务器 CPU 中属于优秀水准。现代服务器 CPU 的内存延迟常超过 100 ns。代价是跨节点和高带宽争用时延迟骤升（高负载下接近 400 ns）以及带宽利用率低下。

## 缓存一致性：HT Assist

Magny Cours 的内存控制器（MCT）负责全部缓存一致性工作。默认行为是广播探测（broadcast），每次内存请求都会探测所有节点。HT Assist 选项会从 L3 中划出 1 MB/die 用作探测过滤器（snoop filter），记录哪些缓存行被远端节点缓存及其状态，从而减少广播探测流量。Intel 同期设计（Westmere）在 L3 中使用 core valid bits 作为探测过滤器，可在同 die 内完成 cache-to-cache 传输而无需绕道远端 MCT。

## 历史意义与演进

Magny Cours 的策略——复用小 die、通过互联横向扩展核心数——在 AMD 后续产品中持续演进：

- **Bulldozer Opteron（Interlagos，2011）**：同样使用两 die 封装，但基于模块化 Bulldozer 核心
- **Zen 1 EPYC（Naples，2017）**：达到 4 die/socket，但以 Infinity Fabric 取代 HyperTransport，内存控制器仍在计算 die 上
- **Zen 2 及之后**：引入独立 IO Die，将内存控制器下沉到 IO Die，计算 die 专注计算

Infinity Fabric 在某种意义上是 HyperTransport + Northbridge 的合并与进化：它统一了片上 crossbar 和跨 die 互联协议，并引入了更完整的硬件 snoop filter（Coherent Slave），彻底替代了手动维护探测过滤器的需要。

## Sources

- [[sources/chipsandcheese-magny-cours]]
