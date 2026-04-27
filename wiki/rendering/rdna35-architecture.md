---
tags: [gpu, amd, rdna35, igpu, strix-point, rdna3, mobile]
date: 2026-04-27
sources: 1
---

# RDNA 3.5 架构

RDNA 3.5 是 AMD 为移动 iGPU 优化的半代演进架构，介于 [[rendering/rdna3-architecture|RDNA 3]] 与下一代之间。它首次出现在 Strix Point APU 的 Radeon 890M（GFX1150）上，是目前移动端最强 AMD iGPU。主要变化相对保守：在继承 RDNA 3 双发射（dual-issue）机制的基础上，扩大了 WGP 数量，并对 LDS 延迟进行了优化。

## 与 RDNA 3 的差异

RDNA 3.5 的架构变化集中在以下几点：

- **WGP 规模提升**：Strix Point 采用 8 WGP（对比 Phoenix 的 6 WGP），Shader Array 划分为两个，各含 4 WGP 和 256 KB 中间层 L1 缓存（每个 L1 实例现在服务 4 个 WGP，而非 Phoenix 的 3 个）
- **LDS 延迟改善**：Local Data Share（每 WGP 128 KB）的访问延迟显著降低，不仅高于时钟频率的提升所能解释；LDS 的 thread-to-thread 延迟（用于 workgroup 内数据交换）与单线程 pointer chasing 延迟基本一致，说明 atomic 操作同样受益
- **Global Atomics 改善**：尽管 GPU 规模更大，跨 WGP 的全局内存 atomic 延迟仍有改善
- **寄存器堆**：GFX1150（Strix Point 的削减版 RDNA 3.5）使用 128 KB 向量寄存器堆；GFX1151（"Strix Halo"变体，更高端）据 LLVM 提交显示将使用更大的寄存器堆

## 内存子系统

RDNA 3.5 沿用 RDNA 3 的多级缓存策略：L0 向量缓存（16 KB，per-WGP）+ 标量缓存（16 KB）+ 中间层 L1（256 KB per Shader Array）+ 全局 L2（2 MB）。L2 带宽约 1.7 TB/s，总 LDS 带宽接近 5 TB/s。

GPU 通过 4×32 bytes/cycle Infinity Fabric 端口连接系统内存，Infinity Fabric 可运行在较低频率（约 1.6 GHz）而仍能满足满 LPDDR5 带宽需求，有助于节省功耗。实测 Vulkan 带宽约 96 GB/s（LPDDR5-7500 配置），与 Qualcomm Snapdragon X Elite 的 97.82 GB/s 相当。

对比 Intel Meteor Lake iGPU：AMD 缓存层级更多，Intel 则用更大的 L2（约 4 MB）弥补层级的不足。实际性能上，AMD 的缓存带宽全面领先。

## 计算能力

8 WGP × 2 CU/WGP × 2 SIMD32/CU × 32 lanes = 1024 个 FP32 流处理器（wave32 模式）。加上 RDNA 3 遗传的 dual-issue 机制（一个 wavefront 每周期可发射 64 个 FP 操作），Radeon 890M 峰值约 5.1 TFLOPS（或约 10 TFLOPS 若将 FMA 算作两次操作）。

相对前代 Phoenix（Radeon 780M，6 WGP）的提升约 33% 来自规模，加上更高时钟和 LDS 延迟优化，整体性能提升显著。Steam Deck 的 Van Gogh APU（RDNA 2，8 CU，1.6 GHz）在此对比中被远远甩开。

## 游戏表现

在 Cyberpunk 2077 1080P 低画质测试中，Radeon 890M 明显领先 Phoenix 和 Intel Meteor Lake iGPU，功耗约 50W（系统整体）。降功耗至 15W TDP 时，平均帧率约 30 FPS，仍与 Meteor Lake 接近。

AMD 将高端 iGPU 作为差异化战略的核心：Strix Point 是历史上首次 AMD 移动 iGPU 采用比桌面离散 GPU 更新的架构（RDNA 3.5 vs RDNA 3），标志着 AMD 将低功耗游戏作为未来的重点赛道。

## Sources

- [[sources/chipsandcheese-radeon-890m]]
