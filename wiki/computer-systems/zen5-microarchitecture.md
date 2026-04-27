---
tags: [cpu, amd, zen5, microarchitecture, x86, avx512, ryzen9000]
date: 2026-04-27
sources: 4
---

# Zen 5 微架构

Zen 5 是 AMD 2024 年推出的第五代 Zen 架构，首发于 Strix Point 移动 APU（Ryzen AI 9 HX 370）和 Granite Ridge 桌面（Ryzen 9 9950X）。Zen 5 的 CPUID Family 为 1Ah，与 Zen 3/4 的 19h 不同，标志着架构发生了系统性的演进。从 IPC 角度看，AMD 官方宣称平均约 16% 的提升，但在重 AVX-512 工作负载下实测超过 22%。Zen 5 的设计哲学是：更宽的乱序窗口、更大的缓存容量、更强的 SMT 吞吐，而非追求极致频率提升。

## 前端

**分支预测器**：Zen 5 在 Zen 4 已经领先 Intel 的基础上继续升级。L1 BTB 从约 1024 项扩大至 16384 项，并支持每周期两次 taken branch（比肩 Rocket Lake 与 Cortex X2），但覆盖范围更大。更具创新性的是引入了 BTB 受害者缓存机制：16384 项的 L1 BTB 会将被驱逐的目标写入更慢的 L2 BTB（约 8K 项），净效果是系统合计可追踪约 24K 个分支目标。Return Stack 从 32 项增至 52 项，并为两个 SMT 线程各设一份独立副本。

**集群式前端**：Zen 5 首次采用双路 Fetch-Decode 集群。每个集群独立处理一个 SMT 线程，各自每周期可取 32 字节并解码 4 条指令，合计 8-wide decode。这与 Intel E-Core（Tremont/Gracemont）的集群解码在形式上相似，但机制不同——Intel 用多集群加速单线程；Zen 5 则是将两个集群专属于两个 SMT 线程，单线程活跃时无法使用两个集群合力。因此 Zen 5 单线程运行时 decode 带宽不如双线程场景，这是 AMD 为 SMT 优化的有意取舍。

**微操作缓存**：6K 项（比 Zen 4 的 6.75K 略缩，但关联度从 8-way 升至 16-way），支持每周期两条 6-wide fetch，单线程与双线程均可使用两路 fetch pipe。高命中率下 µOp Cache 是主要指令来源，spill-to-decoder 仅是补充。

## 重命名与后端乱序资源

重命名级从 6-wide 扩展至 8-wide，是 Zen 5 "更宽"最直接的体现。ROB、FP 寄存器堆、Load Queue 容量均明显增大，趋近 [[computer-systems/golden-cove-microarchitecture|Golden Cove]] 的水平。存储队列从 64 项增至 104 项（桌面版），条目仍为 256 位宽，512-bit 存储仍需两个条目。

**向量/FP 寄存器堆**：Zen 5 在移动版上采用混合宽度寄存器堆（部分 256-bit、部分 512-bit），共 384 项；桌面版则全部为 512-bit 宽。AMD 将向量重命名阶段移至 Non-Scheduling Queue（NSQ）之后，从而消除了 Zen 4 中频繁出现的 FP 寄存器堆容量派发停顿。

**整数调度器**：Zen 5 将整数侧改为单一统一 88 项调度器（对比 Zen 4 的分布式多个队列），每周期可向 6 个整数执行端口选发。这与 Intel Golden Cove 的单一 96 项整数调度器形成类比。分布式调度可降低每个队列选发的压力，但统一调度在端口利用率和移动微指令分配上更灵活。实测中，Zen 5 整数寄存器堆容量是新的瓶颈，在部分工作负载（如内核编译）中造成明显停顿。

**AGU**：4 个地址生成单元，由独立的 58 项统一调度器供给（不再与整数 ALU 共享），可持续每周期 4 次标量内存访问。

## 执行单元

**FP/向量（移动版）**：4 个 FP 执行端口，全部 256-bit 宽。FP 加法 3 周期延迟，FMA 4 周期延迟，执行速率同 Zen 4。向量整数加法延迟从 1 升至 2 周期，128/256-bit 吞吐从 4 条/周期降至 2 条/周期，需要用 AVX-512 才能恢复 1024 位/周期的计算量。

**FP/向量（桌面版）**：FP 单元升至 512-bit 全宽，FP 加法延迟降至 2 周期（快于移动版及 Zen 4 的 3 周期）。L1D 支持每周期两次 512-bit 向量加载，这是 Golden Cove 最初的优势，桌面版 Zen 5 将其追平并超越（Intel 自 Alder Lake 起在客户端禁用了 AVX-512）。

## 缓存与内存

L1 数据缓存从 32 KB 增至 48 KB，延迟保持 4 周期不变；L1D 带宽（存储方向）增至 64 bytes/cycle，与加载方向对称。L2 读写带宽均为 64 bytes/cycle，读写混合可达约 85 bytes/cycle。TLB 全面扩容：L2 iTLB 四倍于 Zen 4，L2 dTLB 增加 33%，且 L2 dTLB 延迟维持 7 周期不变。

移动版与桌面版在缓存容量上存在差异：Strix Point 高性能集群 L3 为 16 MB，桌面版每 CCD 为 32 MB。桌面版还受益于 DDR5（约 70 ns 延迟），显著优于移动版 LPDDR5（约 128 ns）。

## SMT 策略

Zen 5 的设计重心明显偏向 SMT。集群解码、NSQ 后向量重命名、8-wide 重命名中部分操作仅在双线程时满速等，均体现出 AMD 的 SMT 优先取向。与 Intel Lunar Lake（弃用 SMT）形成鲜明对比，AMD 通过"密度优化物理实现 + SMT"维持多线程竞争力，而非像 Intel 那样用不同核心架构实现异构混搭。

## Strix Point 移动配置

Strix Point APU 实现了 12 核 Zen 5，分为两个集群：高性能集群（4 颗标准 Zen 5，16 MB L3，最高 5.15 GHz）和密度优化集群（8 颗 Zen 5c，8 MB L3，最高 3.3 GHz）。Zen 5c 与标准 Zen 5 架构相同，仅是面积优化的物理实现，保留 AVX-512 支持。两个集群间的 core-to-core 延迟异常偏高（接近 200 ns，接近跨插槽服务器延迟），原因不明。详见 [[computer-systems/strix-point-soc]]。

## 与前代的比较

相比 [[computer-systems/zen4-microarchitecture|Zen 4]]，Zen 5 在分支预测准确率、BTB 容量、乱序窗口、FP 寄存器堆、缓存带宽等方面全面提升，但时钟频率几乎没有增长（Strix Point 仅比 Phoenix 略高），这导致在频率主导的测试中优势被部分稀释。整数寄存器堆容量是 Zen 5 最明显的遗留约束。

## Sources

- [[sources/chipsandcheese-strix-point-zen5]]
- [[sources/chipsandcheese-zen5-desktop]]
- [[sources/chipsandcheese-zen5-variants]]
- [[sources/chipsandcheese-zen5-clustered-decode]]
- [[sources/chipsandcheese-zen5-avx512-freq]]
- [[sources/chipsandcheese-zen5-gaming]]
- [[sources/chipsandcheese-zen5-hot-chips]]
