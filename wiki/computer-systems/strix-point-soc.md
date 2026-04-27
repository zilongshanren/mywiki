---
tags: [cpu, gpu, amd, strix-point, soc, apu, mobile, rdna35, zen5, lpddr5]
date: 2026-04-27
sources: 2
---

# AMD Strix Point SoC

Strix Point 是 AMD 2024 年推出的移动 APU，搭载 [[computer-systems/zen5-microarchitecture|Zen 5]] CPU 与 [[rendering/rdna35-architecture|RDNA 3.5]] iGPU，面向高性能轻薄本市场。代表性型号为 Ryzen AI 9 HX 370，率先在 AMD 移动产品中引入 Zen 5 核心，打破了历史上移动版晚于桌面版发布的惯例。

## CPU 集群配置

Strix Point 实现了双集群混合 CPU 设计，但与 Intel 异构混搭策略不同，AMD 两个集群均使用同一架构：

- **高性能集群**：4 颗标准 Zen 5 核，16 MB L3 缓存，最高 boost 5.15 GHz
- **密度优化集群**：8 颗 Zen 5c 核，8 MB L3 缓存，最高 boost 3.3 GHz

Zen 5c 是同一微架构的面积优化物理实现，保留完整 AVX-512 支持，与 Intel Crestmont（不支持 AVX-512）形成对比。每个集群内所有核心时钟上限相同，简化了操作系统调度；集群间响应速度均极快，密度核也可在不到 2 ms 内达到 3.3 GHz 最高频率。

## 跨集群延迟异常

一个值得关注的问题：Strix Point 的跨集群 core-to-core 延迟高达约 200 ns，接近服务器跨插槽延迟，明显高于 Zen 4 移动版（Ryzen 9 3950X 跨集群约 80-90 ns）。考虑到 Strix Point 是单片设计（非 chiplet），这一现象令人意外。原因推测与 Infinity Fabric 路由或集群间互联拓扑有关，但尚无官方说明。

## 内存子系统

LPDDR5 内存控制器支持最高 LPDDR5-7500（Asus ProArt PX13 测试配置），128-bit 总线，理论带宽 120 GB/s，实测约 80 GB/s（单集群），96 GB/s（双集群均压）。每个 CPU 集群通过 32 bytes/cycle 读/写对称端口连接 Infinity Fabric（区别于桌面版写路径仅 16 bytes/cycle）。Infinity Fabric 运行频率最高 2 GHz。实测 DRAM 延迟约 128 ns，低于 Intel Meteor Lake（148 ns），但远高于桌面 DDR5。

## GPU 侧

iGPU 为 Radeon 890M，基于 RDNA 3.5 架构，8 个 WGP，较上代 Phoenix（6 WGP）扩大约 33%。详见 [[rendering/rdna35-architecture]] 和 [[sources/chipsandcheese-radeon-890m]]。Infinity Fabric 提供 4×32B/cycle 的 GPU 接入端口。

## 与 Intel Meteor Lake 的比较

Strix Point 与 Intel [[computer-systems/meteor-lake-chiplet-architecture|Meteor Lake]]（Core Ultra 7 155H）的直接竞争是本代最值得关注的对比。在时钟主导的现实性能测试（如 libx264）中，Strix Point 以明显优势胜出，AVX-512 支持差异是重要因素。内存带宽相当，但 AMD 获得更低的 DRAM 延迟。Intel Meteor Lake 则受益于更大的 CPU tile 内存带宽，以及可将单核访问至 24 MB L3 的不分区架构（AMD 将 L3 分散在两个集群中）。

## Sources

- [[sources/chipsandcheese-strix-point-zen5]]
- [[sources/chipsandcheese-radeon-890m]]
