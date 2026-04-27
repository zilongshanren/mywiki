---
tags: [cpu, gpu, amd, mi300a, apu, infinity-fabric, hbm3, infinity-cache, numa, memory-subsystem, cdna3]
date: 2026-04-27
sources: 2
---

# AMD MI300A APU 内存子系统

MI300A 是 AMD 将 CPU 与 GPU 整合于同一芯片的最大规模尝试，也是 AMD APU 路线从桌面消费市场走向高性能计算的里程碑。与消费级 APU 将 CPU 能力作为核心、iGPU 作为补充的设计不同，MI300A 的出发点恰恰相反：它是一块以 GPU 为主体、以 CPU 作为辅助馈送的超级计算加速器。

## 芯片拓扑

MI300A 的封装由三类 die 构成。三块 CCD 各自包含 8 颗 Zen 4 核心，合计 24 核；六块 XCD 各含 38 个 CDNA 3 Compute Unit，合计 228 CU。这些计算 die 全部落在四块 IO Die（IOD）之上，IOD 作为主动中介层，整合了 Infinity Cache 切片、内存控制器以及跨 die 的 Infinity Fabric 互联。IOD 之间再通过一层底部互联 die 实现快速跨 IOD 通信，整个封装最终对外呈现为一块拥有 256 MB Infinity Cache 与 5.3 TB/s HBM3 带宽的统一系统。

## Infinity Fabric 的角色

MI300A 的 CPU 和 GPU 均通过 Coherent Master（CM）模块接入 Infinity Fabric。每个 CM 拥有内存地址映射，向负责对应地址的 Coherent Slave（CS）发送数据包。CS 紧邻内存控制器放置，并维护一个 2 MB Infinity Cache 切片——这就是 256 MB Infinity Cache 在物理上以 128 个 2 MB 切片分布于各 CS 旁边的原因。CS 依次从三个位置满足请求：本地 Infinity Cache 命中、本地内存控制器（DRAM Miss），或向远端 CM 发出 probe 请求（处理修改态缓存行）。

这套"memory-side cache"设计有一个结构性约束：每块 Infinity Cache 只能缓存由其绑定 CS 管辖的物理地址。跨节点访问时，远端节点的 Infinity Cache 无法被本节点的核心利用，只有当数据的归属 CS 在本地时才能命中 Infinity Cache。这一设计简化了一致性管理，但以牺牲部分 NUMA 性能为代价。

## 延迟代价

MI300A 的内存子系统对 CPU 核心并不友好。Infinity Cache 命中延迟超过 140 ns，远高于桌面 Zen 4 系统的 DDR5 延迟；HBM3 Miss 后延迟高达约 227 ns。这一数字背后是巨大 Infinity Fabric 网络的固有穿越延迟——这张网络需要服务 24 颗 CPU 核心和 228 个 GPU CU。

在四插槽 NUMA 配置下，跨节点 DRAM 访问延迟攀升至 477~559 ns（视拓扑距离而定）。Infinity Cache 虽然能将跨节点延迟拉低一些，但因为无法缓存对方节点的地址，最终仍在 369~430 ns 范围内。这使得 MI300A 的 Zen 4 核心在通用计算表现上落后于同频的桌面或服务器 Zen 4——SPEC CPU2017 单线程整数性能大致与 Zen 2 的 Ryzen 9 3950X 相当。

## 带宽格局

5.3 TB/s 的 HBM3 带宽实际上几乎全部为 GPU 所用。三块 CCD 的 CPU 核心最高能实现约 212 GB/s 读带宽，通过读写双向 Infinity Fabric 链路可推至 314 GB/s，但无论如何都不足以让内存控制器达到饱和——这本属设计预期。每块 CCD 拥有两条 32 B/cycle（双向）的宽 GMI 链路，单 CCD 带宽约 71 GB/s 读，一旦达到此上限，延迟会随之上升，但不会影响其他 CCD 的延迟感知。

跨节点 CPU 读带宽受到严重限制，实测仅约 25~26 GB/s，显著低于 128 GB/s 的跨插槽链路理论带宽，推测为延迟瓶颈。DMA 引擎在 OpenCL clEnqueueWriteBuffer 测试中可实现约 55.9 GB/s，体现了 GPU DMA 对延迟的低敏感性。

## CPU-GPU 一致性

MI300A 的一大卖点是消除 CPU-GPU 之间的显式数据搬运。系统支持 OpenCL Fine-Grained SVM，CPU 写入对 GPU 内核启动前即可见，GPU 写入在内核结束后可被 CPU 读取，且零拷贝实现经过测试确认。更进一步，MI300A 虽未官方声称支持 OpenCL atomics，但实测可运行跨 CPU/GPU 的 CAS 操作，往返延迟约 222 ns——与同封装内 Zen 4 跨 CCD 延迟相当，说明 GPU 侧一致性机制已经深度整合入 Infinity Fabric。跨插槽 CPU-GPU 原子操作的延迟也保持在可接受范围内，体现了精心调优的设计。

## 设计取舍

MI300A 毫不掩饰地对 GPU 侧偏袒。高带宽的 HBM3 和 Infinity Cache 是为延迟容忍的 GPU 工作负载而优化的，而非为延迟敏感的 CPU 核心服务。AMD 选择将 Infinity Cache 与 CS 绑定，而非设计独立的去耦合缓存层，可以减少额外的一致性控制逻辑，代价是跨节点 CPU 访问性能有所下降。在 AMD 的设计意图中，这 24 颗 Zen 4 核心的角色是"为 GPU 喂数据、处理 GPU 不擅长的代码段"，而不是提供全功能的通用 CPU 计算能力。

MI300A 已经随 LLNL El Capitan 超算进入实际部署，并占据 TOP500 2024 年 11 月榜单第一。

## 相关

- [[computer-systems/cdna3-mi300x-architecture]]
- [[computer-systems/infinity-fabric-loaded-latency]]
- [[computer-systems/grace-hopper-cpu-gpu-system]]
- [[computer-systems/cuda-memory-hierarchy]]

## Sources

- [[sources/chipsandcheese-mi300a-memory]]
- [[sources/chipsandcheese-mi300a-gpu]]
