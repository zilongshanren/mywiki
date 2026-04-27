---
tags: [cpu, 微架构, amd, bulldozer, cmt, smt, x86, 32nm]
date: 2026-04-27
sources: 2
---

# Bulldozer：AMD 的激进现代化尝试

Bulldozer（微架构代号 Komodo，产品线 AMD FX，2011 年发布）是 AMD 彻底抛弃 Athlon/K10 架构、从头设计的全新微架构。它几乎在所有层面都引入了新技术，但最终以单线程性能低于前辈 Phenom II 而告终，并导致 AMD 陷入数年财务困难。

## 核心创新：CMT 模块结构

与 Intel SMT 将一个物理核虚拟化为两个逻辑核不同，Bulldozer 采用**集群多线程（CMT, Cluster Multithreading）**：每个"模块"包含：
- **共享**：fetch/decode 前端、FPU、L2 cache
- **各线程私有**：整数执行核（40 条目统一调度器 + 2 × ALU）、load/store 单元、L1D cache

这在面积效率上比 SMT 有优势——前端和 FPU 是高面积开销的组件，但实际利用率通常不足 100%。然而带来的代价是每线程可用的整数执行资源和重排序缓冲容量各自只有模块总量的一半。

## 前端与分支预测

Bulldozer 对 K10 的分支预测器做了大幅升级：更大容量的两级 BTB，并将分支预测器从 L1i fetch 级解耦，通过 fetch target queue 提前预填目标。然而，L2 BTB 每次命中需要 **5 周期**，导致不能背靠背执行 taken 分支——循环展开在 Bulldozer 上依然重要。相比之下，Sandy Bridge 的 4096 条目 L1 BTB 可以连续处理 8 个 taken 分支而不停顿。

指令缓存保留了 K10 的 64 KB 大容量，这是 Bulldozer 相对 Sandy Bridge 少有的优势点——Sandy Bridge 的 1536 条目 micro-op cache 在小代码足迹时更高效，但超出后 Bulldozer 的大 L1i 占优。

## 乱序执行引擎

AMD 在 Bulldozer 中全面切换为**物理寄存器文件（PRF）方案**，放弃了 K10 整数侧的 ROB+RRF 设计，Intel 也在同年的 Sandy Bridge 中做了同样的转变。PRF 方案下 ROB 只保存指向 RF 的指针，退休时仅需复制指针而不是数据，大向量寄存器场景下效率明显更高。Bulldozer 的 ROB 较 K10 扩大 **77%**，寄存器重命名快照（mapper checkpoint array）支持分支误预测后快速恢复，无需等待误预测分支退休。

整数执行侧：40 条目统一调度器，但**仅 2 条 ALU**——4-wide 前端却只有两条整数执行管道，执行资源明显偏弱。FPU 侧则是另一个极端：**60 条目统一调度器**（比 Sandy Bridge 的 54 条目还大）、**160 条目 FP 寄存器文件**，原生 FMA4 支持，两线程竞争共享而非固定分区。

## 缓存子系统（最大弱点）

| 层级 | Bulldozer | Sandy Bridge |
|------|-----------|--------------|
| L1D  | 16 KB write-through + 4 KB WCC | 32 KB write-back |
| L2   | 2 MB @ ~20 周期，16-way | 256 KB @ ~10 周期 |
| L3   | 8 MB @ >18 ns，中心化 Northbridge | ~10 MB @ <10 ns，ring bus |

L1D 从 K10 的 64 KB 骤降到 16 KB 是最惨烈的妥协，根因是 **32nm SOI 工艺**的时序困难：AMD 被迫从 6T SRAM 换到更低密度的 8T SRAM，并将 bitline 从 16 cells 缩到 8 cells。Write-through 的 L1D 配上 4 KB WCC 是"小降落伞"——比完全直写好，但写带宽仍仅 ~10 B/cycle（Sandy Bridge 16 B/cycle）。

L3 维持 K10 时代的中心化 Northbridge 架构，而 Sandy Bridge 已换用 ring bus。L3 延迟超过 18 ns 甚至比 K10 回退，带宽因 victim cache 操作（所有 L2 eviction 均写回 L3）实际翻倍承压，单线程实际可用带宽甚至接近 DRAM 带宽。

## 为何失败

Bulldozer 的失败是多因素叠加，而非单一原因：
1. 32nm SOI 工艺挑战比预期严重，迫使多处架构折中
2. 单线程 OoO 资源被模块对半分割，整数 ALU 数量也被削减
3. 小 L1D + write-through + 高惩罚 + L3 带宽差，缓存子系统全面拖后腿
4. Sandy Bridge 在同期做出了异常出色的设计，是强劲的比较对象

## 历史意义

Bulldozer 为 AMD 带来了 PRF 方案、先进分支预测器、FMA 等一批新技术的实战经验。正如 Netburst 的探索积累后来成就了 Sandy Bridge，Bulldozer 的技术积累后来在 [[zen2-microarchitecture|Zen]] 中成功复用——后者在相似的架构思路下用更成熟的工程实现取得了竞争力。

## 参见

- [[zen2-microarchitecture]] — Zen 继承了 Bulldozer 的 PRF 方案和先进分支预测器，但成功实现
- [[netburst-microarchitecture]] — 同样是"必要的失败"，为后来成功奠基
- [[non-scheduling-queue]] — AMD 的调度器设计历史
- [[amd-k8-microarchitecture]] — Bulldozer 的前辈架构

## Sources

- [[sources/chipsandcheese-bulldozer-part1]]
- [[sources/chipsandcheese-bulldozer-part2]]
