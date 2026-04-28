---
tags: [source, cpu, intel, clearwater-forest, skymont, e-core, server, hot-chips-2025]
date: 2026-04-27
sources: 1
---

# Intel's Clearwater Forest E-Core Server Chip at Hot Chips 2025（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 8 月的文章，报道 Intel 在 Hot Chips 2025 上发布的 Clearwater Forest 服务器 CPU，该芯片以 [[computer-systems/skymont-microarchitecture|Skymont]] E-Core 为核心，是 Intel 进军高密度服务器市场的主要产品。

## 摘要

Clearwater Forest 是 Intel 用于高密度服务器领域的 E-Core 芯片，使用 Intel 18A 节点生产的计算 die 搭载 Skymont 四核簇，通过 3D 堆叠方式叠于 Intel 3 工艺的基础 die（包含 Mesh 互联和大容量 L3 切片）上。三块基础 die 合计支持 288 核，是上一代 Sierra Forest（144 核）的两倍；576 MB 的 L3 缓存在同级竞品中同样领先。文章指出 Skymont 单核性能已接近 Intel P-Core，使其有能力与 AMD Bergamo 等高密度竞品正面竞争。

## 关键要点

- Skymont 集群（4 核 + 4 MB L2）封装在 Intel 18A 工艺计算 die 上，每块计算 die 含 6 簇（24 核）
- 3D 堆叠：计算 die 叠于 Intel 3 工艺基础 die，后者承载 Mesh 互联和 8 MB L3 切片
- 三块基础 die 通过嵌入式硅桥（45 µm pitch）互联，合计 288 核、576 MB L3
- 内存带宽约 1.3 TB/s（DDR5-8000），双路 UPI 跨 socket 带宽 576 GB/s
- L3 延迟较高，L2 hitrate 对性能至关重要；Skymont 4 MB L2 在此场景下不可或缺
- IO die 复用 Sierra Forest 旧设计（Intel 7 工艺），节省开发成本
- 每芯片 96 条 PCIe Gen5，其中 64 条支持 CXL；聚合 IO 带宽约 1 TB/s
- Intel 宣称 20 台 CWF 机架可替代 70 台旧 P-Core 服务器机架（SPEC CPU2017 整数速率测试）

## 链接到的概念

- [[computer-systems/clearwater-forest-architecture]]
- [[computer-systems/skymont-microarchitecture]]
- [[computer-systems/crestmont-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/intels-clearwater-forest-e-core-server
- 本地：`raw/articles/chipsandcheese.com/2025-08-25_intel-s-clearwater-forest-e-core-server-chip-at-hot-chips-20.md`
