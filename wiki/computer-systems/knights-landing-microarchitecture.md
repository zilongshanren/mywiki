---
tags: [cpu, intel, xeon-phi, hpc, avx512, many-core, smt4, mcdram]
date: 2026-04-27
sources: 1
---

# Knight's Landing 微架构

Knight's Landing（KNL）是 Intel Xeon Phi 第二代产品，于 2016 年以 Intel 14nm 工艺推出，集成 76 个基于改造版 [[computer-systems/clustered-decode-atom|Silvermont]] 的核心（消费级 SKU 启用 64 个），每核支持 SMT4。其设计目标是高性能计算（HPC），在 GPU 与传统服务器 CPU 之间填补空白。

## 核心架构

KNL 核心可被描述为"围绕喂饱巨大向量单元而构建的小型乱序核心"：

- **前端**：2-wide，32 KB 8-way L1i；分支预测器极小（仅 256 entry BTB），无法背靠背执行 taken branch（单线程）；SMT 可部分掩盖 BTB 延迟
- **重命名**：不支持 zeroing idiom 消除依赖，不支持 move elimination；ROB 72 entry，寄存器文件完整覆盖 ROB 容量（包含 mask 和 AVX-512 向量寄存器）
- **整数执行**：2 ALU，2×12-entry 调度器；64-bit 整数乘法仅单路半速，延迟 5 周期
- **SMT4 资源划分**：4 线程时每线程 ROB 缩至 18 entry，store queue 仅剩 4 entry

## AVX-512 执行

向量单元占核心面积约 39%，是 KNL 的核心竞争力：

- 每周期 2×512-bit FMA，吞吐与 Skylake-X 持平
- FMA 延迟 6 周期（Skylake-X 为 4 周期）；向量整数加法延迟 2 周期
- 向量调度器不持有操作数（节省面积），输入操作数宽达 512-bit 时这是必要妥协
- 向量寄存器文件物理上分为两部分：推测寄存器文件约 72 entry（4.6 KB）+ 架构寄存器文件（8 KB，存储 4 线程非推测状态）

## 存储子系统

- L1D 32 KB，延迟 4 周期；每周期可发 2 个内存操作（2 load 或 1 load + 1 store）
- L2 1 MB per 双核 tile，延迟 17 周期；无 L3
- 每核仅 1 MB on-die 缓存，HPC 场景下有限的局部性是设计妥协
- store-to-load forwarding 延迟 6–7 周期（精确地址匹配）；跨 64B cacheline 边界的 load 需 2 周期，store 需 4 周期

## MCDRAM

KNL 集成 16 GB 片上 MCDRAM，类似 HBM 但无需 interposer：

- **Flat 模式**：MCDRAM 映射至地址空间高端，直接寻址，延迟约 176 ns（DDR4 约 147 ns）
- **Cache 模式**：MCDRAM 作为 DDR4 的直接映射 LLC，带宽效率约 85.6%，实测约 350 GB/s
- **Hybrid 模式**：一半 flat、一半 cache
- Quadrant+SNC4 模式可将 DDR4 延迟降至 143 ns，但对 MCDRAM 带宽影响很小（mesh 带宽充裕）

## SMT4 收益

KNL 的 SMT4 效果优于典型评估：

- 高 FP 延迟（6 周期 FMA）、高 L2 延迟（17 周期）、taken branch 不能背靠背——这些都是 SMT 可掩盖的空泡
- Y-Cruncher（高带宽 + 高向量化）下，256 线程版本超越 Ryzen 3950X
- 缺点：分支密集型代码（libx264）BTB miss 率在 SMT4 下急剧上升；内存带宽受限时 SMT 会加剧 cache thrashing

## 设计谱系

KNL 核心血统：Larrabee → P54C+512-bit FPU+SMT4 → Knight's Ferry（32核+GDDR3）→ Knight's Corner（22nm，62核）→ Knight's Landing（14nm，76核，Silvermont基）。Larrabee 原本目标是 GPU，但最终演变为 HPC 专用产品。

## Sources

- [[sources/chipsandcheese-knights-landing]]
