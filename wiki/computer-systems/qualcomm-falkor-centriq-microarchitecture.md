---
tags: [cpu, qualcomm, arm, 服务器, 微架构, 乱序执行, aarch64, 云计算]
date: 2026-04-27
sources: 1
---

# Qualcomm Falkor 微架构与 Centriq 2400

Falkor 是 Qualcomm 专为云计算服务器设计的第一款 AArch64 CPU 核心，于 2017 年随 Centriq 2400 SoC 发布。Chester Lam 在 Chips and Cheese 对测试系统 Centriq 2452 进行了完整的微基准分析。

## 背景

Qualcomm 以 10nm FinFET（Samsung）工艺切入云服务器市场，目标是用低功耗与高密度挑战 Intel Skylake-X 在 mainstream cloud 工作负载（web 服务、容器、轻量数据库）中的主导地位。Centriq 2452 支持最高 48 核，TDP 120W，约 2.5W/核。

## 前端

Falkor 采用双级指令缓存：24 KB 3-way L0（低功耗低延迟）+ 64 KB 8-way L1，共计 88 KB 有效指令缓存容量，在当时领先于同期主流设计（Apple M1 发布后才被超越）。两级 I-cache 均集成分支目标，分支目标查找与指令取值共用一次 cache 访问——优点是访问效率高，缺点是 I-cache miss 时无法超前预取分支路径。

16 项 BTIC（Branch Target Instruction Cache）缓存分支目标处的指令，实现 L0 内的零泡沫 taken branch。方向预测使用多历史长度表结构，概念上类似 TAGE，在 branch-heavy 工作负载下优于 Cortex A72。

## 重命名与乱序执行

4-wide 解码器，但第四槽仅支持直接分支及少数特化指令（cbz/cbnz 不能进第四槽），实际有效宽度接近 3-wide。256 项重命名缓冲，约 190 条指令的有效乱序窗口，资源释放可乱序进行。

Falkor 将执行管线平衡向内存侧倾斜，相对于前代 Kryo 削减了执行资源：3 条 ALU + 1 专用直接分支端口，FP/向量侧 2 条对称管线（各 11 项调度器），128-bit 向量指令拆为 2 条 micro-op（调度器、寄存器文件、完成缓冲均双占）。

## 内存子系统

L1D 32 KB 8-way，16 bytes/cycle，3 周期 load-to-use。L1D 同时带 virtual tag 和 physical tag（VIVT），某些负载可直接跳过 TLB 查询。写穿（write-through）L1D，配合类似 Bulldozer WCC 的侧边写合并结构提供写回等效性能，并以 parity 替代 ECC 保护 L1D。

L2 512 KB，8-way，15-17 周期延迟，含多 interleave（每 interleave 32 bytes/cycle），带宽明显优于 Kryo 和 A72 的 L2。

## 系统架构

Falkor 双核组成 duplex，共享 512 KB L2。通过专有 QSB（Qualcomm System Bus）协议连接片上环形总线（segmented ring bus）。环总线连接最多 24 个 duplex、12 个 L3 切片、6 个 DDR4 控制器（支持 128 GB/s）及 PCIe/IO 控制器。

L3 共 60 MB（12 × 5 MB 切片，20-way），对 Graviton 1 有巨大带宽优势。L3 延迟高（>40 ns / >100 核心周期），在高带宽负载下可恶化至 90 ns，不含 L2 内容（non-inclusive），利用 L2 snoop filter 维护一致性。

内存控制器延迟约 121 ns，高带宽负载下 latency 可超 500 ns（Intel 同等条件下可控制在 200 ns 以内）。不支持多路 NUMA，最高 48 核单 socket。

## SPEC CPU2017 性能

Falkor 整数套件领先 Cortex A72 21.6%，浮点套件领先 53.4%。在内存亲和型工作负载（505.mcf、503.bwaves）上优势明显；高 IPC 但向量不友好的测试（548.exchange2 等）中优势缩小，暴露出 4-wide 宽度受限的问题。

## 历史评价

Centriq 是当时 Arm 服务器市场中对 Graviton 1 压倒性的竞争者，但面对 Skylake 仍有明显差距（L2 更小、L3 延迟更高、向量能力弱）。Qualcomm 缺乏对 Linux/ARM 生态系统的长期承诺被认为是商业失败的关键因素之一。Arm 服务器真正立足要等到 2020 年后 Ampere Altra（基于 [[neoverse-n1-microarchitecture]]）出现。

Qualcomm 宣布了 2025 年后向服务器领域的再入局计划（供应 HUMAIN + Nvidia NVLink Fusion 生态），延续 Falkor 时代的经验。

## Sources

- [[sources/chipsandcheese-centriq-falkor]]
