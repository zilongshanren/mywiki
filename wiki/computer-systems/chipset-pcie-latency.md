---
tags: [pcie, chipset, 互连, 延迟]
date: 2026-04-19
sources: 1
---

# 主板 chipset 对 PCIe 延迟与带宽的影响

过去二十年里，主板 chipset（南桥 / PCH / 北桥）在性能路径上的角色不断退化：Athlon 64 把内存控制器集成进 CPU，Sandy Bridge 把 PCIe 车道也挪进 CPU。今天 chipset 主要负责 SSD、USB、网卡这种延迟本就在 µs/ms 级别的 IO。但插在 chipset 下的 PCIe 槽接设备时，仍然会吃掉几百 ns 的额外延迟。

## 测法

Chester 用 Nemes 的 Vulkan GPU 基准，把 buffer 分配成 `HOST_COHERENT_BIT` 置位、`DEVICE_LOCAL_BIT` 清零——也就是 host 内存——然后让 GPU 走 pointer chasing。GPU 用 Nvidia T1000（单槽 PCIe Gen3 x16），插不同的槽（CPU 直连 vs chipset 下挂）测延迟差异。反向测（CPU 访问 GPU VRAM）遇到 page fault 干扰就回避了。

## 数字（GPU → host memory）

| 平台 | 基线（CPU 槽） | chipset 槽 | chipset 增量 |
|---|---|---|---|
| AMD AM5 / B650 (一级 PROM21) | 650 ns | 1221 ns | 569.7 ns |
| AMD AM5 / X670E (两级 PROM21) | 650 ns | ~1571 ns | 921.3 ns |
| Intel Arrow Lake / Z890 | 785 ns | ~1335 ns | ~550 ns |
| Intel Skylake / Z170 | 535.6 ns | ~874 ns | 338 ns |
| AMD AM3+ / 990X + SB950 | 769.7 ns | ~1372 ns | 602 ns |

结论：
- 每挂一级 chipset chip，大约多 500–600 ns
- X670E 因为串了两颗 PROM21 惩罚翻倍
- 老 Skylake Z170 单级 chipset 反而最优
- AM3+ 时代 CPU 直连其实走的是 5.3 GT/s HyperTransport 到外置 RD980 北桥，基线已经 770 ns，仍然体面

## 缓存 hit 带宽也会被 chipset 压住

T1000 因为 `HOST_COHERENT_BIT`，即使命中自己 L1 也会发出 probe 到 CPU 侧——probe 节流成了 cache hit 带宽的瓶颈。观测到：
- Zen 5 CPU 直连：T1000 L1 hit 带宽正常
- Zen 5 chipset 下挂：T1000 cache hit 带宽被压到 ~25 GB/s
- 990X 北桥：132 GB/s 上限（仍远超 HyperTransport 10.5 GB/s，说明 probe 预算即使富余也未必打得满 IO）
- 990X 南桥 SB950：~20 GB/s

probe 似乎每 512 B 一个、而非每 cache line（64 B）一个——一个未解谜题。

## 为什么 chipset 不再优化延迟

多 GPU 退场后，chipset 服务的设备（SSD、网卡）延迟本身就以 µs/ms 计，几百 ns 无关紧要。VRAM-backed buffer 的 cache hit 更不需要给 CPU 发 probe。所以未来 chipset 设计的方向是成本 + 连接性 + 更高带宽，而不是 latency/probe 路径优化。

## 相关

- [[memory-hierarchy]]
- [[latency-vs-throughput]]

## Sources

- [[sources/chipsandcheese-chipset-microbench]]
