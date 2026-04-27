---
tags: [gpu, amd, rdna4, 微架构, 光追, 渲染]
date: 2026-04-27
sources: 1
---

# RDNA4 架构

RDNA4 是 AMD 2025 年推出的消费级图形架构，搭载于 RX 9000 系列离散 GPU（如 RX 9070 / RX 9070 XT）。与 RDNA3 相比，RDNA4 的设计重心是效率提升而非旗舰规模竞争——RX 9070 相比 RX 7900 XT 在更低功耗和更少带宽下实现接近的光栅化性能，并大幅领先于后者的光线追踪性能。

## 计算架构变化

RDNA4 的 Workgroup Processor（WGP）保留了 RDNA 系历代的基本布局，但在光线追踪、动态寄存器分配和调度器层面做了重要改进（详见此前分析文章）。Hot Chips 2025 着重介绍了以下两点新特性：

**标量浮点指令**：RDNA4 的标量单元获得 FP32 加法、乘法、FMA、min/max 及整数/浮点转换指令，扩展了标量卸载的适用范围。该能力最初在 RDNA 3.5 中出现，RDNA4 将其带入独立 GPU。标量 FP32 加法/乘法延迟为 4 周期，快于向量侧的 5 周期基础延迟。

**分裂屏障（Split Barriers）**：传统 `s_barrier` 要求所有线程同时到达屏障点，产生等待开销。RDNA4 将屏障拆分为 `s_barrier_signal`（线程完成数据生产后即可发出信号）和 `s_barrier_wait`（需要消费数据时才等待），允许线程在产生数据后继续执行独立工作，只在真正需要同伴数据时才阻塞，有效减少屏障引起的空转。

## 内存子系统

RDNA4 最大规格配备 8 MB L2 缓存，是历代 RDNA L2 容量最高值（RDNA3 为 6 MB，RDNA2 为 4 MB）。L2 容量增大对光线追踪尤其有利——BVH 遍历是密集指针追踪场景，对 L2 命中率高度敏感，访问 Infinity Cache 会额外引入 50 ns 以上的延迟（约 >100 个时钟周期）。

RDNA4 **移除了**历代 RDNA 存在的 L1 Cache 层（介于 WGP L0 和 L2 之间的中间级）。Chester 推测这是有意为之：L1 在 RDNA1 上命中率往往低于 50%，将面积预算直接用于更大的 L2 可能比保留命中率不高的 L1 更划算。另一个可能是 L1 验证问题导致本代跳过。

与 [[blackwell-gb202-architecture|Blackwell]] 的策略对比鲜明：Nvidia 将 L2 作为 last-level cache（兼顾 AMD L2 + Infinity Cache 两个层级的功能），Blackwell GB202 的 L2 延迟约为 130 ns，处于 RDNA4 L2（更快）和 Infinity Cache（更慢）之间。

Infinity Fabric 内存侧子系统包含 16 个 CS（Coherent Station）模块，每个配套一个 UMC（Unified Memory Controller）。每个 CS 配备 4 MB Infinity Cache，合计 64 MB。Infinity Fabric 支持 1.5–2.5 GHz DVFS，理论带宽约 2.5 TB/s。

RDNA4 离散 GPU 采用 256-bit GDDR6 内存总线，通过更强的压缩和更大的 L2 弥补带宽不足。

## 透明压缩

RDNA4 在整个 SoC 中大量使用透明压缩，包括 Display Engine 和 Media Engine 端点。压缩数据可存入缓存，写回 DRAM 时解压，减少数据传输量，降低带宽需求和功耗。Delta Color Compression（DCC）已是历代 RDNA 的标配；RDNA4 将压缩范围进一步扩大至 Infinity Cache 层级。

RDNA4 得以在较小 die（356.5 mm²）和 256-bit GDDR6 配置下维持高性能，压缩提升是重要因素之一。

## 媒体引擎

高端 RDNA4（RX 9070 XT）配备两个媒体引擎，支持 H.264/H.265/AV1 硬件编解码。RDNA4 媒体引擎的改进集中在两点：更快的解码速度（racing to idle，省电）以及低延迟 VBR 编码的质量提升。与 RDNA3.5 相比，H.264 低延迟编码下 VMAF 分数提升明显，特别是高对比度轮廓和文字保留更佳，编码速度从约 190 FPS 提升至约 200 FPS。

## Display Engine

RDNA4 新增 Radeon Image Sharpening 滤镜，由 Display Engine 在硬件中以极低功耗完成，不影响游戏性能，也无需游戏开发者集成。

多显示器空闲功耗是 RDNA4 Display Engine 的另一个改进点。通过配合 FreeSync 显示器动态降低刷新率，RDNA4 可在屏幕内容不变时让内存总线进入低功耗状态，显著降低空闲功耗（RDNA2 在相同场景下更容易维持高内存时钟）。

## 单片设计

AMD 明确表示基于对性能目标、封装组装时间和成本的评估，为 RDNA4 选择了单片（monolithic）设计。这与 AMD 在 RDNA3 大 SKU 上使用 chiplet 的做法不同，体现了"没有万能方案"的工程取舍哲学。

## 相关

- [[blackwell-gb202-architecture]]
- [[rdna3-architecture]]
- [[rdna2-architecture]]
- [[infinity-cache-efficacy]]
- [[strix-halo-soc]]
- [[gpu-latency-hiding]]

## Sources

- [[sources/chipsandcheese-rdna4-hot-chips-2025]]
