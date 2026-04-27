---
tags: [nvidia, gpu, microarchitecture, kepler, 28nm, compute, gaming]
date: 2026-04-27
sources: 1
---

# Kepler 架构

Kepler 是 Nvidia 第一款量产 28 nm GPU 架构，2012 年随 GTX 680（GK104）发布，此后扩展到 GTX 700 系列（包含 GK210 的 Tesla K80 等数据中心产品）。其设计目标是在 Fermi 的计算能力基础上大幅提升功耗效率，与 AMD 的 GCN 正面竞争。

## 动机：从 Fermi 到 Kepler

Fermi 在 40/28 nm 过渡期的功耗问题暴露了"运行两倍时钟的执行单元"方案的代价。Kepler 放弃热时钟，改为**更多执行单元 + 正常时钟**，用面积换功耗效率。于是一个 GK104 的"96 CUDA 核"等效于 GF104 同频的 48 个计算单元。

另一个重大决策是将调度从硬件（Fermi 的记分板）移交给**编译器静态调度**。

## SMX 结构

Kepler 的基本构件是 SMX（Streaming Multiprocessor X），每个 SMX 含 4 个调度分区（SMSP）。每个 SMSP：
- 跟踪至多 16 个 warp（32 宽向量线程）
- 每周期可选择 1 个 warp，最多发射 2 条指令（dual issue）
- 共享 8 KB 指令缓存

## 静态调度（编译器控制码）

Kepler 最具特色的设计：每 7 条指令前置一个 64-bit 控制字，编译器在其中编码每条指令的停顿周期数和 dual issue 标志。硬件无条件信任控制码，消除了 Fermi 那套多端口寄存器记分板，大幅简化了硬件并降低功耗。FMA 延迟固定为 9 cycle，编译器据此安排调度。

## 执行单元

每个 SMSP 有 64 KB 寄存器文件（GK210 为 128 KB），4 个单端口 bank。双发射 FMA 需要最多 6 个寄存器输入，因此引入了操作数收集器（operand collector）缓存最近读取的寄存器值。

整数操作走独占端口（2/3 FP32 速率），特殊函数（倒数、平方根）为 1/4 整数速率。

## 缓存层次

- **L1 / 共享内存**：从同一 64 KB 存储动态划分，GK210 扩至 128 KB
- **纹理缓存**：每 SMSP 12 KB，SMX 合计 48 KB（4 个分区）；纹理访问延迟优于 AMD GCN 向量缓存
- **常量缓存**：2 KB 第一级 + 32 KB 第二级；相比 Fermi 有所退步（4 KB 降至 2 KB，延迟升高）
- **共享内存（Local Memory）**：延迟低于 L1，优于 Fermi，更远优于 GCN LDS

**L2**：GK104 为 512 KB（8 个切片），GK210 为 1.5 MB；理论 L2 带宽 541 GB/s（GK104 @ 1058 MHz），但实测远低于此，GCN 的 L2 带宽更宽。

**DRAM 带宽**：GK104 实测 ~142 GB/s（256-bit GDDR5），GCN HD 7950 为 ~204 GB/s（384-bit）；GK210 获 384-bit 总线，但 AMD Hawaii 的 512-bit 仍更宽。

## 与 GCN 的对比

| 维度 | Kepler | GCN |
|------|--------|-----|
| FP32 吞吐 | 较低 | 较高 |
| DRAM 带宽 | 较低 | 较高 |
| 单线程指令发射 | 最快（同 warp 连续 cycle 可发射） | 每 4 cycle 发射一次 |
| 本地内存延迟 | 低 | 高 |
| 全局内存原子延迟 | 低于 Fermi，略低于 GCN | 较高 |

Kepler 的竞争力在于：小 kernel 场景（延迟少、利用率高），以及每线程能聚合更多资源。

## 遗产

Kepler 的静态调度方案被 Maxwell、Pascal、Volta 等后续所有 Nvidia 架构延续（控制码格式演进，但核心策略不变）。SMX 内 4 个调度分区的划分也延续至后续架构。Tesla K20x 系列凭借强大的软件生态在超算（Oak Ridge Titan）上取得成功。

## Sources

- [[sources/chipsandcheese-kepler-architecture]]
