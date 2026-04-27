---
tags: [raytracing, bvh, amd, nvidia, rdna2, rdna3, turing, pascal, 加速结构, hardware-rt]
date: 2026-04-27
sources: 2
---

# BVH 遍历的硬件策略对比

BVH（Bounding Volume Hierarchy，层次包围体）是光线追踪加速结构的标准形式，决定了光追性能的两个核心变量：相交测试**次数**（与树的宽度正相关）和内存访问**跳数**（与树的深度正相关）。AMD 与 Nvidia 在面对同样的 GPU 约束（高带宽、高延迟、大规模并行）时，选择了截然不同的 BVH 策略，反映了两家公司对"GPU 瓶颈在哪里"的不同判断。

## AMD 的窄树策略

AMD 的 BVH 格式是固定宽度的：box node 包含 **4 个子节点**，triangle node 包含 **4 个三角形**。这是一个偏向"CPU 风格"的设计——通过增加树深度来减少每层的计算量。

在《赛博朋克 2077》中，TLAS 覆盖整个夜之城区域：70,720 个节点，总占用 11 MB，从根节点到叶子需要 **19 次跳转**（包含一次 TLAS→BLAS 的转换）。单棵游戏内树木的 BLAS 平均深度 7 层，最深 11 层。

这一策略的代价是**延迟敏感**。每次跳转都依赖上一步的相交结果，形成长链式依赖。GPU L2 cache 的延迟约 80 ns，而 TLAS 本身就有 11 MB，很难整体驻留在低延迟缓存中。

[[rendering/rdna3-architecture|RDNA 3]] 的针对性优化方向：
- L0/L1 缓存容量翻倍（降低平均访问延迟）
- 新增 LDS 专用 BVH 栈指令（减少 BVH 遍历栈访问延迟）
- 向量寄存器文件扩大（占用率从 10/16 提升至 12/16，允许更多 ray 同时 in-flight）

## Nvidia 的宽树策略

Nvidia 的 BVH 采用极宽的非固定宽度节点。据 Nsight Graphics 呈现，顶层节点展开后**直接指向数千个 BLAS**，单个 triangle node 可包含数百至数千个三角形——仅需 **3 次跳转**即可到达叶子几何体。

这一策略的逻辑：GPU 的延迟隐藏能力依赖同时保持大量 warp in-flight，**减少跳数就是减少指针追逐的串行依赖链**，让并行计算单元不必等待。代价是每步的相交测试计算量大幅增加，需要高吞吐的专用 RT Core。

Nvidia 架构的迭代方向完全符合这一逻辑：
- **Turing（第一代）**：部署 RT Core，但 INT32/FP32 路径静态分离，SM 利用率仅 11%
- **Ampere（第二代）**：三角形测试吞吐翻倍，修复 INT32/FP32 分裂，SM 更高效
- **Ada（第三代）**：更高 SM 数、再次翻倍三角形测试吞吐，超大 L2（72 MB）进一步降低节点访问延迟

## Pascal 的教训

Pascal 无专用 RT 硬件，但 Nvidia 仍让其使用宽树策略，以纯 compute shader 遍历。结果是性能灾难：SM 平均 IPC 仅 1.09，占用率极低（13.23/64 warps），主要瓶颈为 long scoreboard（全局内存延迟）和 no-instructions（指令缓存缺失）。Pascal SM 的 L1 无法绕过纹理单元路由，延迟不可优化，注定是第一代光追实现的性能底线。

## 两种策略的本质权衡

| 维度 | AMD（窄树） | Nvidia（宽树） |
|------|------------|--------------|
| 跳转深度 | ~19 跳 | ~3 跳 |
| 每步计算量 | 少（4 个子节点） | 大（数百三角形）|
| 延迟敏感度 | 高（长串行依赖） | 低 |
| 所需硬件 | 简单（借纹理单元）| 专用高吞吐 RT Core |
| 优化方向 | 增大缓存，增加 occupancy | 增加 RT 吞吐，减少 L2 延迟 |

没有绝对正确的答案。AMD 的方案在架构代价上更低，且其改进路径（缓存扩容、更多 wavefront）会同时惠及所有其他工作负载。Nvidia 的方案更激进，但在 Ada 时代借助巨大的 SM 规模和 L2 容量已能很好弥补早期 Turing 的短板。

## 参见

- [[rendering/rdna2-architecture]] — AMD RDNA 2 光追实现细节
- [[rendering/rdna3-architecture]] — RDNA 3 的针对性改进
- [[rendering/ada-lovelace-architecture]] — Nvidia Ada 架构
- [[rendering/hybrid-raytracing-pipeline]] — 混合光追管线实践
- [[rendering/raytracing-vs-rasterization]] — 光追与光栅化对比
- [[computer-systems/gpu-latency-hiding]] — GPU 延迟隐藏机制

## Sources

- [[sources/chipsandcheese-rt-rdna-turing]]
- [[sources/chipsandcheese-rdna2-architecture]]
