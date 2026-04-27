---
tags: [cpu, intel, broadwell, edram, cache, l4, crystal-well, history, packaging]
date: 2026-04-27
sources: 1
---

# Broadwell eDRAM L4（Crystal Well）

Broadwell 桌面版（2015 年）是首个在消费级处理器上提供大容量片上 L4 缓存的产品，比 AMD Ryzen 7 5800X3D（2022 年）早约七年。其 128 MB eDRAM 由独立的 77 mm² Crystal Well die（22 nm）实现，通过 OPIO 接口连接 CPU die，是 [[vcache-3d-die-stacking|AMD V-Cache]] 在历史上的精神前驱。

## Crystal Well 技术原理

eDRAM（Embedded DRAM）以电容+晶体管存储一位，相比 SRAM 的 6T 结构密度更高，但需要刷新且读操作具有破坏性（读后需恢复）。Crystal Well 针对高性能低功耗场景进行了特殊设计：

- **128 bank**：远超 DDR3（8 bank）和 DDR5（32 bank），bank 并发度高，随机访问冲突概率低
- **6 array cycle bank 恢复**：相比主内存 DDR 的数十 cycle 恢复时间大幅缩短
- **独立读/写 64-bit 总线**（OPIO 接口）：避免 DDR 的 bus turnaround，可在相邻周期内交替服务读/写请求
- 工作电压 <1.1V，OPIO 接口总功耗仅约 1W（102 GB/s 双向）

理论性能：1.6 GHz eDRAM 时钟，等效 DDR-3200，最大单向带宽约 50 GB/s，延迟约 36.6 ns（~140 cycle @ 3.8 GHz）。

## 作为 L4 缓存的架构实现

Broadwell 将 eDRAM tag 嵌入 CPU die 的 L3 切片（L3 因此从 8 MB 缩至 6 MB），tag 检查与 L3 检查并行进行。这意味着：

- **L4 命中**：L3 miss 与 eDRAM tag 命中同时发现，由 L3 控制逻辑直接从 eDRAM 取数，不额外绕行 ring bus
- **L4 miss**：L3 miss + eDRAM miss，才发出到 System Agent 的内存请求
- eDRAM 作为非包含型（non-inclusive）受害者缓存，只缓存从 L3 驱逐的行

这一设计在延迟上非常克制，使 eDRAM 能在需要时直接补充 L3 容量，而不引入额外 ring bus 往返。

## Skylake 变体的退化

Skylake 重新设计将 eDRAM 控制器移至 System Agent：tag 检查延后至 L3 miss 触发后才开始，且与主内存请求串行，L4 延迟大幅上升（接近 DDR3 直接访问延迟）。CPU 端的性能益处被严重削弱，eDRAM 主要惠及 iGPU 和 display engine（显示刷新流量）。随着 DDR4/DDR5 带宽持续提升，Crystal Well 的带宽优势逐渐消失，Intel 最终放弃了 eDRAM 路线。

## 性能局限

尽管设计精巧，eDRAM L4 存在根本性限制：

- **带宽不随核数扩展**：单 OPIO 接口约 50 GB/s，4 核 CPU 即可饱和；Broadwell L3 因分切片设计可线性扩展
- **延迟对 CPU 偏高**：~140 cycle 延迟只适合作 L4，不能替代 L3
- 只有少数 SPEC CPU2017 工作负载（如 520.omnetpp）能从 L4 命中率获得可感知提升

## 与 AMD V-Cache 的对比

| 方案 | 延迟 | 带宽 | 工艺 | 结合方式 |
|------|------|------|------|----------|
| Crystal Well eDRAM（Broadwell） | ~140 cycle / 36.6 ns | ~50 GB/s | 22 nm，独立 die | OPIO 封装走线 |
| AMD V-Cache（Zen 3/4） | L3+约 4 cycle / 1.6 ns | 与 L3 一致 | TSV 堆叠 SRAM | 3D TSV 键合 |

TSV SRAM 从根本上解决了 eDRAM 的延迟问题，带宽与 L3 一致，性价比远优。Crystal Well 是 eDRAM 性能的极限展示，也是迫使业界转向 TSV SRAM 堆叠的历史证明。

## Sources

- [[sources/chipsandcheese-broadwell-edram]]
