---
tags: [gpu, amd, rdna4, isa, llvm, gfx12, matrix, sparse, prefetch, coherence]
date: 2026-04-27
sources: 1
---

# AMD RDNA 4 架构（预发布分析）

RDNA 4 在 LLVM 中以 GFX12（gfx1200、gfx1201）标识，预计对应两款不同 die。以下信息来自 Chester Lam 对 LLVM 提交的分析，属于预发布内容，以实际产品为准。

RDNA 4 是 [[rdna3-architecture]] 的继任，在 ISA 层面做出了四大改动方向，整体趋势是：**更 CPU 化的内存访问控制、更精细的 AI/矩阵加速、更主动的指令流管理**。

## 更细粒度的内存依赖等待

GCN 以来，AMD GPU 用 `s_waitcnt` 系列指令等待特定类别的内存访问完成（如所有 vector load、所有 export 等）。RDNA 4 将这些分类拆分得更细，使 shader 程序可以针对更小范围的访问集合等待，减少因粗分类产生的伪依赖停顿，理论上提升线程级指令并行度。

对比：Nvidia Maxwell+ 使用 6 个可灵活分配的 barrier，更灵活但数量有限（仅 6 个）。

## 更灵活的缓存一致性控制

RDNA 3 及之前：三位 GLC/SLC/DLC 控制缓存 bypass 与时序 hint（非临时访问隐含于 bit 组合中）。

RDNA 4 改为四位方案：
- 两位 **scope**（Compute Unit / Shader Engine / 全设备），可精确选择在哪一级 cache 保持 temporal 性
- 三位独立 **temporal hint**（low / normal / high temporal），与 scope 正交

新增的 SE 级 scope 允许同一 Shader Engine 内的线程通过共享 L1 传递数据，而不必下沉到 GPU-wide L2，有望提升依赖数据的 L1 命中率。

## 更强的矩阵与 AI 指令

RDNA 3 引入 WMMA（Wave Matrix Multiply Accumulate）指令，RDNA 4 在此基础上：

- 新增 **FP8 / BF8** 格式支持，跟进低精度 AI 推理趋势
- 引入 **SWMMAC**（Sparse WMMA）：A 矩阵以稀疏压缩格式存储（实际只存一半元素），通过稀疏索引参数展开，理论可获 **2× 矩阵吞吐**

稀疏矩阵指令的实际效益取决于权重稀疏度，与 Nvidia Ampere 的 2:4 sparsity 类似。

## 更主动的指令与数据预取

### 指令预取改进
- 初始内核预取窗口：8 KB（RDNA 3）→ **32 KB**（RDNA 4），涵盖更大代码体积
- 新增 `s_prefetch_inst` 指令：可将预取指向推测分支目标，改善大型 shader 的指令缓存效率

### 数据侧软件预取（首次引入）
RDNA 4 首次为 AMD GPU 引入数据侧软件预取指令。传统 GPU 依靠宽访问+线程级并行隐藏 latency，数据预取是 CPU 域的工具。RDNA 4 的引入意味着 AMD 承认某些 GPU workload（如 BVH 遍历、稀疏访问）存在 latency 受限场景，预取可以补足带宽换延迟的机会。

## ISA 演进的启示

GPU ISA 与 CPU ISA 不同：GPU 驱动在用户机器上运行时编译 shader，不存在二进制兼容压力，因此可以大幅改动 ISA。RDNA 4 的改动方向（标量化、软件预取、更细一致性控制）清晰呈现出 GPU 向通用计算/AI 加速器演进的路径，与 [[gcn-architecture]] 当年从固定函数图形管线向通用计算迈出的一步一脉相承。

## Sources

- [[sources/chipsandcheese-rdna4-llvm]]
- [[sources/chipsandcheese-rdna4-ooo-memory]]
- [[sources/chipsandcheese-rdna4-register-alloc]]
- [[sources/chipsandcheese-rdna4-raytracing]]
- [[sources/chipsandcheese-rdna4-hot-chips-2025]]
