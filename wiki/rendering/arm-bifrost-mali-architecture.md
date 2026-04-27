---
tags: [gpu, arm, mali, bifrost, 移动GPU, tile-rendering, compute, 低功耗]
date: 2026-04-27
sources: 1
---

# ARM Bifrost 架构与 Mali-G52

Bifrost 是 ARM 于 2016 年推出的第二代统一着色器 GPU 架构，取代了此前的 Midgard（VLIW4）设计。Chester Lam 以 Amlogic S922X 上的 Mali-G52 为对象，与 Snapdragon 670 的 Adreno 615 进行了详细的微基准对比分析。

## 业务模型的约束

Mali 作为独立授权 IP 块出售，ARM 对芯片级系统架构没有控制权。Mali 不含视频解码加速与显示输出，实现者可自由选配。这一业务模型要求 Bifrost 在尽可能宽泛的工作负载下保持合理性能，因为 ARM 无法假设芯片上存在其他加速器。这与 Qualcomm Adreno 的"专注图形光栅化"策略形成鲜明对比。

## 执行模型：SIMT 标量化

Bifrost 从 Midgard 的 VLIW4 切换为标量 + 双发射执行模型，与 AMD 从 Terascale 到 GCN 的转型思路平行。每个执行引擎（Execution Engine，EE）内，单线程寄存器宽度降为 32-bit，依赖多 API 线程填满 EE 的 4/8 条并行 lane。EE 内每 lane 仍有 FMA + FADD 两条流水线可在一条 78-bit 指令中打包两个操作，降低了编译器的发射压力。

## 架构层次

- **EE（Execution Engine）**：含 register file + FMA/FADD 流水线，4-wide 或 8-wide lane 可配置。
- **Shader Core（SC）**：1-3 个 EE + L1 纹理/load-store 缓存 + 像素后端（ROP），ROP 挂在 SC 级（桌面 GPU 通常挂在更高层级）。
- **GPU 级**：多 SC 共享 L2 缓存（Bifrost 推荐每 SC 64-128 KB），通过标准 ACE 总线连接系统。

Mali-G52（Amlogic S922X）是极小配置：2 个三 EE（8-wide）SC，800 MHz，峰值 96 GFLOP/s（FMA+FADD 双发）。

## 指令执行与 Clause-based ISA

Bifrost 使用分组执行的 clause-based ISA，类似 AMD Terascale：clause 内指令原子执行，跨 clause 依赖通过 6 项软件管理的记分板管理。"临时寄存器"（temporary registers）是软件控制的操作数转发路径，可绕过寄存器文件的带宽限制——寄存器文件仅有 4 个端口（2 读、1 写、1 读写），同时喂 FMA+FADD 原本需要 5 个输入。这些机制与 AMD Terascale 2 的 PV/PS 高度相似。

## 内存子系统

分离的纹理缓存（约 8 KB）与 load/store 缓存（16 KB），通过 SC 内部消息总线与 EE 通信。Mali 不为 compute shader 提供专用片上本地内存（Local Memory / Shared Memory）——所有本地内存访问均走 load/store 缓存并最终可能访问 DRAM，latency 明显高于 Adreno 的 GMEM。这是 Bifrost 面对 compute 工作负载的主要短板之一。

## Tile 渲染与带宽节省

Bifrost 采用层级式 tile 渲染（16×16 像素基础 tile，可升级为更大 power-of-two），将深度测试与 alpha 混合的中间结果保存在片上 tile memory，渲染完毕后才写回 DRAM。额外的"Transaction Elimination"功能对比当前 tile 与上一帧 CRC，相同则跳过写回，进一步节省带宽。Adreno 同样使用 tile 渲染，使用 512 KB 片上 GMEM 存储中间状态。

## FP16 与数据类型灵活性

EE 的执行流水线在 32/16/8-bit 数据类型间保持 256-bit 等效执行宽度（或 4-wide EE 的 128-bit），FP16/INT8 均有硬件快速路径。相比之下，Adreno 615 缺少硬件 FMA 快速路径（OpenCL `fma()` 需 600+ 周期/warp），且 INT8 无专用硬件。

## 与 Adreno 615 的对比

| 维度 | Mali-G52 (Bifrost) | Adreno 615 |
|---|---|---|
| 发散惩罚阈值 | 8 线程 | 64 线程 |
| FMA 硬件 | 有 | 无快速路径 |
| INT8 吞吐 | 优秀 | 接近 0 |
| 纹理吞吐 | 2 samples/SC/cycle | 4 samples/uSPTP/cycle |
| 本地内存 | DRAM 回退 | GMEM 片上 |
| 零拷贝支持 | 仅 coarse-grained | 支持零拷贝 |

## Sources

- [[sources/chipsandcheese-mali-g52-bifrost]]
