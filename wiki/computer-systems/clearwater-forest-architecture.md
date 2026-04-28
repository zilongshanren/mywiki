---
tags: [cpu, intel, clearwater-forest, skymont, e-core, server, hot-chips-2025, chiplet]
date: 2026-04-27
sources: 1
---

# Clearwater Forest 架构

Clearwater Forest 是 Intel 面向高密度服务器市场的 E-Core 专用 CPU，首次在 Hot Chips 2025 上展示完整技术细节。它是上一代 [[computer-systems/crestmont-microarchitecture|Sierra Forest]]（Crestmont E-Core）的继任者，核心升级为性能大幅提升的 [[computer-systems/skymont-microarchitecture|Skymont]]，并采用更激进的 3D 封装策略实现 288 核总量与 576 MB L3 缓存。

## 封装与物理结构

Clearwater Forest 采用分离 die 的 3D 堆叠设计：

- **计算 die（Intel 18A 工艺）**：每块包含 6 个 Skymont 四核簇（共 24 核），核心逻辑受益于 Intel 18A 的密度和功耗改善。Intel 同期将 Skymont 用于 Arrow Lake 客户端平台（TSMC 3nm），这一跨工艺使用展示了其"工艺中立"能力。
- **基础 die（Intel 3 工艺）**：承载片上 Mesh 互联和 8 MB L3 切片。IO 接口等不依赖先进工艺的逻辑不适合放在昂贵的先进节点上，因此单独放于此层。
- **IO die（Intel 7 工艺）**：直接复用 Sierra Forest 的 IO die，位于芯片顶部和底部，提供 PCIe Gen5 / CXL 接口。

三块基础 die 通过嵌入式硅桥（embedded silicon bridge，pitch 约 45 µm）横向互联，计算 die 与基础 die 之间采用更密集的 9 µm pitch 互联。整个封装最终实现 **288 核（3 × 4 × 24）** 和 **576 MB L3**，是 Sierra Forest 144 核的两倍。

## 互联与内存子系统

片上 Mesh 可视为垂直与水平两方向的环形结构。垂直方向跨越基础 die 边界、贯通全芯片；水平方向将 L3 切片与最近的内存控制器关联，有助于降低延迟并便于划分 NUMA 域。

集群内 Skymont 的 L2 带宽为 256 B/cycle（聚合，四核合计），向系统 Mesh 输出 35 GB/s 带宽（估计受高 L3 延迟制约，并非物理接口极限）。Arrow Lake 桌面平台测试中，Skymont 集群实测 L3 读带宽可达 80 GB/s 以上，说明高 L3 延迟而非接口宽度是瓶颈。

DRAM 侧最高支持 **DDR5-8000**，理论读带宽约 1.3 TB/s；双路 UPI 跨 socket 带宽 576 GB/s，远超同级多路设计中常见水平。IO 方面每芯片 **96 条 PCIe Gen5**，其中 64 条支持 CXL，聚合 IO 带宽约 1 TB/s。

## 性能定位与竞争

Intel 以 SPEC CPU2017 整数速率基准宣称"20 台 CWF 机架替代 70 台旧 P-Core 机架"，侧面说明其密度效率提升。同为高密度路线的竞品包括 Ampere AmpereOne（192 核）和 AMD Bergamo（128 核 Zen 4c）；Clearwater Forest 的 288 核在原始核数上更具优势，但实际性能仍取决于 L3/DRAM 延迟实测数据。

Skymont 在桌面平台（Arrow Lake）上已展示接近 P-Core 的单核性能，这使得 Clearwater Forest 有别于以往 E-Core 产品"仅靠核数堆量"的印象，而是兼具密度与单核竞争力。正如 Chester Lam 所指出，"E-Core 团队在过去十年里将核心从截然不同的性能星球带到了接近 P-Core 的位置。"

## 与 Sierra Forest 对比

| 维度 | Sierra Forest（Crestmont）| Clearwater Forest（Skymont）|
|------|--------------------------|------------------------------|
| 核心数 | 144 核（最高 SKU 未量产）| 288 核 |
| L3 容量 | — | 576 MB |
| 工艺节点 | Intel 4 + Intel 7 IO | Intel 18A + Intel 3 + Intel 7 IO |
| 单核性能 | Crestmont 级 | Skymont 级（接近 P-Core）|
| 封装 | Tile-based | 3D 堆叠 |

## Sources

- [[sources/chipsandcheese-clearwater-forest]]
