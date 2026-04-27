---
tags: [cpu, intel, chiplet, packaging, foveros, cxl, igpu]
date: 2026-04-27
sources: 1
---

# Meteor Lake Chiplet 架构

Meteor Lake 是 Intel 首款面向客户端市场的 chiplet 设计，将单片 die 拆分为四个独立 tile，通过被动 base die（Foveros 封装）互联。这标志着 Intel 彻底改变了过去十年以不同单片 die 覆盖不同细分市场的策略。

## 四 Tile 结构

Meteor Lake 由四个 tile 组成：

- **CPU tile**：包含 P-core 与 E-core 集群及其 L3 缓存，与 AMD 的 CCD 类似
- **iGPU tile**：独立集成显卡 tile，首次与 CPU tile 分离
- **SoC tile**：包含系统代理功能（Thunderbolt、PCH 逻辑等）
- **IO Extender tile**：处理 PCIe 通道与 DisplayPort PHY

所有 tile 堆叠于被动 base die 之上，由 base die 负责互联与电源分配。

## Foveros Die Interconnect（FDI）

Intel 称其 die-to-die 互联方案为 Foveros Die Interconnect（FDI）。FDI 相比 AMD 的平面封装互联（IFOP）具有更高 IO 密度与更低功耗，适合超薄本对空间和功耗的严苛要求。但 Intel 公布的延迟数据（＜10 ns）与 AMD 的 Infinity Fabric 跨 die 延迟（＜9 ns）相近，并无明显优势。

FDI 主要服务于低带宽、高延迟路径（CPU tile ↔ SoC tile ↔ IO Extender tile），并不用于性能关键路径，因此 L3 缓存环总线完整保留在 CPU tile 内部——这使 Meteor Lake 的 L3 结构更接近 [[golden-cove-microarchitecture]] 时代的设计。

## iGPU 与 CPU L3 不再共享

最关键的架构变化在于 iGPU 从 Sandy Bridge 以来首次与 CPU L3 解耦：

- 旧设计：iGPU 作为 IDI（In-Die Interface）代理，通过环总线直接访问 CPU L3
- 新设计：iGPU tile 使用 **iCXL**（内部 CXL 实现，不含 PHY）与 SoC tile 通信

这一变化有多重动机：减少环总线 stop 数量（降低延迟）、允许 CPU tile 独立进入低功耗状态、以及 iGPU 对共享 L3 的命中率本身极低（实测仅 28% 左右，AMD 的 Infinity Cache 在 16 MB 以下同样命中率低下）。

## 与 AMD Chiplet 策略的对比

| 维度 | Intel Meteor Lake | AMD（Zen + IFOP） |
|------|------------------|-------------------|
| 目标市场 | 移动优先（低功耗） | 桌面 + 服务器优先 |
| Die-to-die 互联 | FDI（高密度、低功耗） | IFOP（低成本、更长距离） |
| iGPU 集成 | 独立 tile | 集成于 IOD |
| 解耦程度 | 更高（4 tile） | 较低（CCD + IOD） |
| 移动扩展 | 天然适合 | 当时仍用单片 die |

AMD 当时的 Dragon Range（55W+）复用了桌面 chiplet 架构，Phoenix Point（15~45W）也在规划 chiplet 路线，暗示双方在移动 chiplet 策略上可能趋于接近。

## 相关

- [[intel-hybrid-alder-lake]]
- [[golden-cove-microarchitecture]]
- [[gracemont-microarchitecture]]
- [[mcm-gpu-design]]
- [[chipset-pcie-latency]]

## Sources

- [[sources/chipsandcheese-meteor-lake-chiplets]]
- [[sources/chipsandcheese-meteor-lake-ces]] — CES 微基准：P/E/LP 三核缓存延迟与带宽数据
- [[sources/chipsandcheese-meteor-lake-igpu]]
- [[sources/chipsandcheese-meteor-lake-igpu-rt]]
- [[sources/chipsandcheese-meteor-lake-npu]]
