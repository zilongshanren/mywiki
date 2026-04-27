---
tags: [cpu, amd, zen4, microarchitecture, x86, avx512, ryzen7000]
date: 2026-04-27
sources: 2
---

# Zen 4 微架构

Zen 4 是 AMD 2022 年推出的第四代 Zen 架构，面向 Ryzen 7000 系列（AM5 平台）。与 Zen 2 的节奏类似，Zen 4 同时完成了架构演进和制程迁移（从 7nm 升至 5nm），采用"演进而非革命"的策略规避风险。AMD 宣称 IPC 提升约 13%，但更大的性能增益来自于频率的显著提升（最高可达 5.7 GHz）。

## 前端

**分支预测器**：Zen 4 保留了 Zen 系列的双级覆盖结构（L1 快速、L2 精确覆盖）。L2 预测器大幅升级，可识别极长的分支模式，在分支密集场景下显著优于 Intel Golden Cove 的单级预测器。L1 BTB 容量从 1024 项扩大到约 1024-3072 项（依分支密度），延迟保持 1 cycle 不变；L2 BTB 从 6656 项增至 8192 项，且惩罚周期从 3 cycle 降至 1 cycle，这是重要改进。

**微操作缓存**：从 4K 增至 6.75K 项，带宽达到 9 ops/cycle（但受下游 6-wide 重命名级限制）。Zen 4 发现了 NOP 的双重融合行为（pairs → pairs），实测可达 12 NOP/cycle，属于特殊优化路径。从 L2/L3 获取代码时带宽约 16 bytes/cycle，与 Zen 3 和 Golden Cove 相当。

## 重命名与乱序资源

重命名级保持 6-wide（与 Zen 3 一致）。ROB 容量增加约 25%（至 320 项），整数寄存器文件和加载队列也有不同程度扩大；存储队列维持 64 项不变，这在 AVX-512 场景下会有压力（512-bit 存储消耗两个存储队列项）。

与 Intel Golden Cove 相比，Zen 4 的乱序资源规模较小，但物理整数寄存器的利用效率更高——Zen 4 有 202 个整数物理寄存器可用于投机结果（占 ROB 63%），而 Golden Cove 为 47.2%。Intel 需要更大的乱序资源来应对其更高的缓存延迟。

调度器布局与 Zen 3 完全一致（没有增大），AMD 选择用更高频率换取性能，而非扩大调度队列。

## 系统级：Infinity Fabric 与内存带宽

Zen 4 的每个 CCD 有一条 32B/cycle 读链路和 16B/cycle 写链路连接到 Infinity Fabric。在配合 DDR5-6000 的 Ryzen 7950X 上，单 CCD 的读链路成为内存读带宽上限。写链路（16B/cycle）限制更明显，与较低 FCLK 测试结果高度吻合。

一个反直觉现象：使用 4 线程（每 CCD 2 核）时写带宽高于 32 线程全满时，原因是更多线程令内存控制器访问调度难度上升，page hit 率下降。FCLK 降低 20% 时，写带宽对应下降，但读带宽仅降约 5.8%。

Raphael 平台是首个高性能 AMD 桌面平台集成 iGPU 的方案：RDNA2 架构，1 WGP，L1 64 KB（标准 128 KB 的一半），L2 256 KB，无 Infinity Cache。DRAM 延迟约 191 ns，优于桌面独立显卡 RDNA2 的 >250 ns，因为 iGPU 与内存控制器同在 IO die 上。

Zen 4 单核 DRAM 带宽能力约 50 GB/s，在高并发带宽测试中可使 CCD 内 XI 队列迅速饱和，引发软件可见延迟超过 700 ns。CCD 边界提供天然 QoS 隔离。详见 [[infinity-fabric-loaded-latency]] 与 [[sources/chipsandcheese-infinity-fabric-limits]]。

## AVX-512 实现

Zen 4 是 AMD 首款支持 AVX-512 的桌面架构。实现策略上走"平衡路线"：512-bit 指令在流水线中大部分阶段保持为单条微操作，进入 256-bit 执行管道前才分为两个 256-bit 半，即"double pumping"。主要特点：

- 向量寄存器文件扩展至 512 位宽（最昂贵的改动）
- 新增掩码寄存器文件（约 52 项重命名，远小于服务端 Intel 的规模）
- L1D 带宽**未**增加，仍为 2×256-bit load / 1×256-bit store per cycle（与 Zen 2/3 相同）
- 512-bit 存储拆分为两条微操作，占用两个存储队列项
- 执行单元保持两个 256-bit FMA + 四个 256-bit ALU（自 Zen 2 起未变）

与 Intel 客户端架构相比：Golden Cove 无法在混合 hybrid 芯片上启用 AVX-512，Zen 4 因此在支持 AVX-512 的应用中具备明显优势。与服务端 Intel 相比，Zen 4 在 load/store 带宽和 FMA 单元数量上仍有差距。

## 内存子系统

**缓存层次（2MB 大页测试）**：
- L1D：4 cycle / ~0.7 ns（得益于高频）
- L2：14 cycle / ~2.44 ns，容量从 512 KB 倍增至 **1 MB**（仅多 2 cycle）
- L3：约 47 cycle / 8-9 ns，恢复至 Zen 2 水平但容量更大（32 MB）

Intel Golden Cove 在各级缓存上都比 Zen 4 延迟更高（L1 +1 cycle、L3 +~20 cycle），需要更大的乱序窗口和更大的 L2（1.25 MB）来掩盖延迟。

**TLB**：L1 DTLB 从 64 项增至 72 项，L2 TLB 从 2048 项增至 **3072 项**（覆盖 12 MB 地址空间仅需 7-8 cycle 额外延迟），这在大工作集场景下显著优于 Golden Cove 的 2048 项 L2 TLB。

**带宽**：L3 带宽（单核）提升至约 27 bytes/cycle（Zen 3 为 24）。Intel Golden Cove 在 L1/L2 带宽上有优势（尤其 AVX-512 场景下），但 L3 带宽急剧下降（约 20 bytes/cycle），AMD 在 L3 及 DRAM 带宽上保持领先。

**DDR5**：Zen 4 转向 DDR5，实测约 72.85 GB/s 读带宽（DDR5-6000，约为理论值的 76%）。DDR5 内存控制器的效率略低于旧 DDR4 控制器，但绝对带宽仍提升约 43%。单核 DRAM 峰值带宽超过 57 GB/s，暗示 L2 miss 追踪队列极深，内存级并行性显著提升。

## 结论

Zen 4 通过前端优化（更强分支预测、更大微操作缓存）和频率提升挖掘现有执行资源的利用率，而非直接扩大执行宽度或 L1D 带宽。核心是"喂饱执行单元"而非"添加执行单元"。AVX-512 的加入是关键亮点，在支持该指令集的应用中可拉开对缺乏 AVX-512 竞争对手的差距。

Zen 4 的 Loop Buffer（144 µop 容量）在 AGESA 1.2.0.2a 附近被 AMD 静默禁用，推测原因为硬件缺陷（类比 Intel Skylake LSD bug）。因 op cache 带宽已完全覆盖 6-wide 重命名级，性能影响 < 1%。见 [[sources/chipsandcheese-zen4-loop-buffer]]。

## 相关

- [[zen2-microarchitecture]]
- [[zen3-bottlenecks]]
- [[golden-cove-microarchitecture]]
- [[sunny-cove-microarchitecture]]
- [[skylake-microarchitecture]]
- [[branch-predictor-design]]
- [[op-cache-decoded-uop-cache]]
- [[memory-hierarchy]]
- [[littles-law-reorder-buffer]]
- [[intel-hybrid-alder-lake]]
- [[raptor-lake-l2-cache]]

## Sources

- [[sources/chipsandcheese-zen4-part1]]
- [[sources/chipsandcheese-zen4-part2]]
- [[sources/chipsandcheese-zen4-part3]]
- [[sources/chipsandcheese-7950x3d-vcache]]
- [[sources/chipsandcheese-zen4-gaming-workloads]] — 游戏 workload pipeline slot 级剖析
- [[sources/chipsandcheese-phoenix-soc]] — Phoenix APU CPU 侧测试
- [[sources/chipsandcheese-zen5-desktop]] — 桌面 Zen 5 对比参考
