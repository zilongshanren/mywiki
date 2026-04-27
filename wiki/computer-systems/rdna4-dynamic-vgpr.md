---
tags: [gpu, amd, rdna4, vgpr, register-allocation, occupancy, raytracing, dynamic]
date: 2026-04-27
sources: 1
---

# RDNA 4 动态 VGPR 分配

GPU 的占用率（同时活跃的线程数）和每线程寄存器数之间存在根本性的张力：寄存器文件容量有限，分给每个线程的寄存器越多，能同时运行的线程就越少，延迟隐藏能力也随之下降。RDNA 4 的动态 VGPR 分配机制是 AMD 针对这一矛盾的创新解法，核心目标是让光追着色器在需要大量寄存器的阶段与需要少量寄存器的阶段之间动态调整配额，而无需牺牲整体占用率。

## 设计动机

AMD 采用内联光追模型：光线生成、BVH 遍历、closest-hit/any-hit/miss 着色全部在同一线程中执行。不同阶段的 VGPR 需求差异悬殊——遍历阶段可能只需少量寄存器，而着色阶段可能需要大量。传统静态分配必须按峰值设置，导致整个生命周期都占据高 VGPR 配额，限制了并行线程数（即占用率）。

对比：RDNA 4 每个 SIMD 有 192 KB 寄存器文件，最大占用率为 16 个线程槽（wave32 模式）。若每线程需要 128 个 VGPR，静态分配只能跑 12 个线程；动态分配可以让所有 16 个槽都启动，在低 VGPR 阶段共享资源，高 VGPR 阶段轮流申请。

## 核心机制

**启动**：驱动通过 `SQ_DYN_VGPR` 寄存器直接设置每 SIMD 的活跃线程槽数，不再由 VGPR 配额隐式推算。每个启用的线程槽自动获得一个保留的最小 VGPR 块。

**运行中申请/释放**：线程通过 `s_alloc_vgpr` 指令请求新的 VGPR 配额（以 16 或 32 个寄存器为粒度，共最多 8 块）。指令通过 SCC（Scalar Condition Code）返回成功/失败。分配失败时，线程忙等重试——这是动态分配的主要性能代价。

**死锁避免模式**：可选模式，保留足够 7 个额外 VGPR 块（最大 8 块减去初始 1 块），确保任意时刻至少有一个线程能成功申请到最大配额并最终完成，逐步释放资源给其他线程。但此模式不能防范所有死锁场景（如生产者-消费者依赖链中的循环等待）。

## 使用限制与实践观察

- 仅支持 wave32 compute shader；图形 shader、wave64 不支持
- 同一 WGP 内动态与非动态线程不可混用
- 当前驱动只在 indirect 光追模式（带函数调用边界）中使用动态 VGPR，内联模式即使 VGPR 受限也未见使用

## 与 Nvidia setmaxnreg 的对比

Nvidia 在 Hopper 引入 `setmaxnreg` PTX 指令，表面相似但语义不同：

| 维度 | AMD s_alloc_vgpr | Nvidia setmaxnreg |
|------|----------------|-----------------|
| 寄存器来源 | GPU 全局自由池 | 当前 workgroup 的固定配额内转移 |
| 同步要求 | 无（线程间独立） | 整个 warpgroup 必须同步执行 |
| 混用常规线程 | 不可（同 WGP 互斥） | 可以 |
| 分配粒度 | 16 或 32 寄存器 | 更细（64 KB 寄存器文件） |
| 死锁风险 | 存在（需 deadlock avoidance mode）| 工作组内封闭，不会跨工作组死锁 |

Nvidia 的方案更适合在已知总量的工作组内协调线程，不适用于 AMD inline 光追场景中各 wave 独立推进的模式。Intel 则因每线程固定 128 或 256 寄存器（无中间选项），动态分配收益有限。

## Sources

- [[sources/chipsandcheese-rdna4-register-alloc]]
