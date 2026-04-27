---
tags: [cpu, arm, china, phytium, ftc663, cortex-a72, microarchitecture]
date: 2026-04-27
sources: 1
---

# Phytium FTC663 微架构

飞腾（Phytium）D2000 处理器内含 8 颗 FTC663 ARM 核心，运行于 2.3 GHz，双核聚合为一个 cluster，面向桌面、笔记本与工业应用。从微架构实测数据来看，FTC663 与 ARM Cortex-A72 存在大量无法用巧合解释的相似之处，强烈暗示该设计并非真正独立研发。

## 性能定位

与同期竞品的真实对比极为惨烈：D2000 在几乎所有基准测试中输给 **2015 年的四核 Intel Core i5-6600K**（Skylake），尽管后者核心数量只有一半。与 Ampere Altra（Neoverse N1）的四核实例相比，D2000 也只能勉强持平。

- **7-Zip 压缩**：8 核 D2000 落后四核 Skylake，刚刚超过四核 Neoverse N1 云实例
- **Gem5 编译**：同样被四核 Skylake 碾压
- **libx264 编码**：向量执行短板暴露无遗，Skylake 因 AVX2 支持遥遥领先
- **Minecraft JVM 启动**：高 IPC 场景，D2000 再次落败

## 分支预测：最大弱点

FTC663 号称使用类 TAGE 预测器，但实测表明其在分支密集场景下甚至**弱于 Cortex-A72**——A72 本身已是现代 OoO 核心里预测最差的设计之一：

- 方向预测精度不如 A72（分支密集时）
- BTB（Branch Target Buffer）速度慢：64 项 L1 BTB 无法做到 zero-bubble taken branch，跳转后至少浪费 1-2 个周期；而 Skylake 和 Neoverse N1 均支持从小容量 L1 BTB 的 zero-bubble 分支
- 间接分支跟踪能力低于 Skylake 和 N1

分支预测退步直接抵消了 FTC663 相对 A72 扩大的重排序缓冲区带来的潜力。

## 与 Cortex-A72 的相似性

以下特征在两者身上完全一致，且都不是"自然选择"的结果：

| 特征 | FTC663 | Cortex-A72 |
|------|--------|-----------|
| NOP 吞吐量上限 | 1/cycle（3-wide 核） | 1/cycle |
| NOP 消耗额外 OoO 资源 | 是 | 是 |
| 128-bit NEON 寄存器分配低效 | 是 | 是 |
| L1 指令缓存大小 | 48 KB | 48 KB |
| BTB 结构（64 项 L1 + 4096 项主） | 完全一致 | 完全一致 |
| 4KB 页下 L1D 内的延迟抖动 | 相同 | 相同 |
| 负载队列大小 | 未扩容，同 A72 比例 | 25% ROB 覆盖率 |

A72 已知问题（如 load queue 占 ROB 比例过低）在 FTC663 中原样保留，而 ARM 自己在 Neoverse N1 中早已修复。

## 执行引擎

FTC663 是 3-wide OoO 设计，ROB 和向量寄存器文件比 A72 更大，store queue 扩至 28 项（A72 仅 15 项）。但 FP/向量单元性能与 A72 相同：大多数单元仅 64 位宽，128-bit NEON 指令分两次执行。N1 则有全宽（128-bit）FP 执行单元，每周期可完成两条 128-bit 指令。

## 内存子系统

- L1D：32 KB（4 周期延迟）
- L2：2 MB 每 cluster（22 周期）——实际延迟接近 Skylake 的大容量 L3
- L3：4 MB 全共享（>50 周期，>20 ns）——接近服务器级 Cascade Lake 的 L3 延迟
- DRAM：**164 ns**，高于双路 Xeon X5650 的 NUMA 远端内存延迟（~120 ns）

## 政治背景与评价

飞腾与中国军工有合作关系，研发受国家资金支持，目标是构建国产芯片设计能力，而非真正商业竞争。从技术能力积累角度看，FTC663 相比 A72 的改进极为有限——一进一退，且保留了 A72 的全部核心弱点。对比同样以 A72 为起点的 ARM Neoverse N1，N1 实现了彻底的技术跨越（快速分支、去耦 BTB、低延迟 L2、内存依赖推测）。

## 相关

- [[neoverse-n1-microarchitecture]]
- [[golden-cove-microarchitecture]]
- [[via-x86-isaiah-lujiazui]]
- [[branch-predictor-design]]
- [[cache-size-vs-latency-tradeoff]]

## Sources

- [[sources/chipsandcheese-phytium-d2000]]
