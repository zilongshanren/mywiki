---
tags: [cpu, 微架构, intel, dunnington, penryn, merom, core2, server, p6, uncore, fsb]
date: 2026-04-27
sources: 1
---

# Dunnington 与 Penryn：Intel 的六核服务器尝试

Dunnington 是 Intel 2008 年推出的六核服务器处理器，将三个 Penryn（Core 2 的 45nm 版本）双核模块集成在一块 503 mm² 的大芯片上，并配备 16 MB L3 缓存。它代表了 Intel 从纯 FSB 架构向现代多核 uncore 过渡的关键节点。

## Merom / Penryn 微架构

Penryn 是 Merom 的 45nm 版本，本质上是 P6 架构的大幅进化版（同时保留了部分 P6 特征如 ROB+RRF）：

**前端**：4-wide 解码（较 Pentium M 的 3-wide 扩宽），2048 条目 BTB，可连续处理 4 个 taken 分支而无停顿。这点胜过 K8/K10，但弱于后来的 Sandy Bridge（8 个 taken 分支无气泡）。

**乱序执行**：96 条目 ROB，配合 ROB+RRF 方案（每条指令结果写入 ROB 条目，退休时复制到 RRF）。在 PRF 方案出现前，这套设计意味着不可能在 ROB 耗尽前先耗尽重命名寄存器，使调优相对简单。

**执行单元**：向量单元原生支持 128-bit 操作（K8 需两次 64-bit 操作），FP 加法延迟 1 周期（K10 为 2 周期）。整数 ALU 三条，比 K10 多一条。

**Load/Store**：一 load AGU + 一 store AGU 的非对称配置，而 AMD K8/K10 有三条均可处理 load/store 的 AGU。L1D 32 KB 8-way，3 周期延迟。

**致命弱点**：4K 页边界惩罚极重（load 越边界 163 周期，store 218 周期），而 K10 几乎无此罚则。推测 Intel 将物理地址比较延后到流水线末端（也与 Meltdown 漏洞有关）。

**L2 缓存**是 Penryn 的核心竞争力：3–6 MB 低延迟（~15 周期）L2，让 Intel 只用两级缓存就能覆盖 AMD 三级缓存的容量，且访问延迟更低。

## Dunnington 的 Uncore

Dunnington 的 uncore 架构直接继承自 Tulsa（基于 Netburst 的前辈六核芯片）：

- **CBC（Cache Bridge Controller）**：中心化 hub，连接三个 Penryn 模块、16 MB L3 以及 FSB 接口
- **SDI（Simple Direct Interface）**：替代 Penryn 模块的 FSB 端口，连接至 CBC
- **16 MB L3**：16-way，含 core-valid bits 作为片上 snoop filter，inclusive 设计
- L3 延迟约 **37 ns**（vs AMD K10 ~16 ns，Sandy Bridge <10 ns）

关键问题：L3 是中心化访问，所有核心请求都要排队通过 CBC，这比 AMD 的 Northbridge 也好不了多少。多核扩展性很差——在 libx264 测试中，加载两个 Penryn 模块仅带来 53% 性能提升，六核全开也只略好于四核，指向明显的 L3 或 FSB 带宽瓶颈。

## 7300 芯片组

为支持四路 socket，Intel 配套了 7300 MCH（Memory Controller Hub）：
- 四路独立 FSB 链接（每 socket 一条）
- DDR2 四通道内存控制器，Fully Buffered DIMMs，最高 667 MT/s
- **1M 条目 128-way snoop filter**，覆盖四个 socket 共 64 MB 的缓存内容
- 跨 socket 延迟约 178–190 ns（vs AMD HyperTransport ~100 ns）

尽管 snoop filter 设计颇为精巧（4 周期查找延迟，按物理地址索引），但 DDR2-667 的内存带宽极低——单 socket 仅约 2.3 GB/s，四 socket 共约 8.6 GB/s，远不及同期 AMD 单 socket 的带宽。

## 历史定位

Dunnington 证明了把更多核心堆到一个芯片上并不能自然解决服务器扩展性问题——你需要好的 L3 架构和好的互联设计。Intel 从 Tulsa/Dunnington 的失败中汲取教训：Nehalem 引入了全局队列和片上内存控制器，Sandy Bridge 进一步引入 ring bus，彻底解决了 L3 带宽问题。Dunnington 的 inclusive L3 + core-valid bits + SDI 等概念在演化中延续，只是更换了连接方式。

## 参见

- [[netburst-microarchitecture]] — Tulsa 的前身，Dunnington 的设计参照
- [[skylake-microarchitecture]] — Intel ring bus 成熟期的代表
- [[numa-multi-socket-design]] — 多 socket 一致性设计通论
- [[core-to-core-latency-lock-test]] — 核间延迟测量方法

## Sources

- [[sources/chipsandcheese-dunnington]]
