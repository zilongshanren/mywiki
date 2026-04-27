---
tags: [cpu, cache, power, efficiency, memory-hierarchy, alder-lake]
date: 2026-04-27
sources: 1
---

# 缓存层次与功耗效率

现代 CPU 的功耗不只取决于核心结构的复杂度，数据搬运的距离（即从哪一级缓存/内存获取数据）对功耗的影响同样巨大。Chips and Cheese 在 Alder Lake 上通过 Intel 的 RAPL 功耗计数器（MSR 0x611）对各级缓存的数据传输能量进行了直接测量。

## 基本规律

测量结果确认了一条贯穿所有平台的经验规律：

- **L2 命中比 L1 命中能耗约高 2 倍**
- **L3 命中比 L2 命中能耗高 2 倍以上**
- **DRAM 访问比 L3 命中能耗高约 4-5 倍**

此规律在 Golden Cove、Gracemont、Skylake、Haswell、Zen 2、Zen 3 上均成立，仅数值有差异。

"race-to-sleep"效应补充说明：部分 CPU 在测试 DRAM 大小的区域时报告了更低的瞬时功率（因执行单元大量等待），但 DRAM 带宽极低意味着等待时间极长，**每字节总能耗依然远高于缓存命中**。

## Golden Cove（Alder Lake P 核）

- 从 DRAM 获取数据的能耗约为 L3 的 5 倍（仅 package 功耗，不含 DRAM 本身功耗）
- L1 命中与微操作缓存命中能耗极为接近（< 6.5% 差距），说明微操作缓存对低功耗设计的价值有限——相同面积直接用于扩大 L1i 效果更佳
- L2 效率优于 Skylake，且带宽更高、容量更大；L3 因环形总线更长、切片更多，效率略低于 Skylake

## Gracemont（Alder Lake E 核）

- Gracemont **不具备**整体功耗效率优势：DRAM 效率略好（执行引擎更小），但 L1D/L2 效率反而低于 Golden Cove
- L2 共享（4 核共用 2 MB）使访问路径更复杂，能耗更高
- 由于缺乏真正的 256-bit AVX（拆分为两次 128-bit），L1D 数据粒度更小，能耗相对更高
- 与 Tremont 对比：10nm 低频 Tremont 在每一级缓存上均比 Gracemont 省电，但带宽也更低；Gracemont 更接近 14nm Goldmont Plus 的效率水平，本质上是面积效率设计而非纯功耗效率设计

## Intel 与 AMD 的策略差异

| 维度 | Intel（Golden Cove）| AMD（Zen 2/3）|
|------|---------------------|----------------|
| 核私有缓存效率 | 接近 | 接近 |
| L3 效率 | 较低（长环形总线）| 较高（4核+L3 slice，核频运行）|
| 向量带宽 | 强（256-bit AVX 每核私有）| L3 弥补 L1/L2 不足 |
| DRAM 效率 | Zen 2 ≈ Skylake，Golden Cove 略差（大 OoO 等待时仍耗电）| 略好 |

Intel 的应对策略是：用**大 L2**（Golden Cove 1280 KB，Raptor Lake 传闻增至 2 MB）拦截更多访问，减少 L3 流量；AMD 则依赖优秀的 L3 设计（低延迟、核频运行）。

## 对设计决策的启示

1. **缓存对功耗不只是"节省"，更是"避免浪费"**：减少 DRAM 访问对功耗的影响远超缩小核心结构
2. **微操作缓存的功耗价值主要在性能，而非节能**：L1 与 uop cache 命中能耗相近；若设计目标是省电，直接加大 L1i 可能更有效
3. **Gracemont 的定位是面积效率，而非功耗效率**：在 Alder Lake 的 i9-12900K 功耗预算下，整体效率受 uncore 功耗主导

## Sources

- [[sources/chipsandcheese-alder-lake-caching-power]]
- [[sources/chipsandcheese-cache-efficiency-mobile-avx512]]
