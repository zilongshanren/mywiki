---
tags: [gpu, 性能优化, 并行, 内存]
date: 2026-04-14
sources: 1
---

# GPU Latency Hiding（延迟隐藏）

GPU 的整个设计哲学就是**用并行度换延迟**：每一次内存访问都可能是几百个 cycle 的等待，但只要同一个硬件单元上还有别的工作可跑，延迟就被掩盖掉了。在 shader 程序员看到的层面，这表现为两条彼此对偶的机制，在 [[gcn-wave-occupancy|GCN wave occupancy]] 一文里被 Wronski 明确对举起来。

## 两条路径

### 1. Per-wave ILP — 寄存器换延迟

编译器对 shader 做激进的 loop unrolling，把后续多个样本的 fetch 统统提前发出，再把所有**不依赖这些 fetch 的 ALU** 插到 fetch 和第一次 use 之间。等真正用到数据时，寄存器已经就位，`wait` 指令直接通过。

- **代价**：[[register-spilling-avoidance|VGPR]] 用量飙高。寄存器寿命 = 从首次 fetch 到最后一次 use，越长越占。
- **适用**：fetch 之间互不依赖、单 wave 内就能凑够「足够的 ALU」来填延迟的场景。经典后效（blur、大采样数 AO、DOF）都属此类。
- **与 CPU 对照**：这就是编译器里的 software pipelining / scheduling，只是 GPU 的 VGPR 池大得多、编译器也更乐意激进展开。

### 2. Per-CU TLP — wave 换延迟

同一个硬件单元（CU/SM）上挂多个 wavefront/warp。当一个 wave 卡在 `wait` 时，调度器在 1 个 cycle 内切到另一个 wave 跑它的 ALU，第一个 wave 的数据回来后再切回去。

- **代价**：每个 wave 能用的 VGPR 上限更紧（寄存器总量除以同时存活 wave 数），shader 里的局部变量必须塞得下。
- **适用**：**data-dependent flow control**——fetch 的结果立刻被用于分支或下一次地址计算，单 wave 内根本凑不出独立 ALU 去填延迟。
- **别名**：GPU 世界的「occupancy」就是这个机制的度量——NVIDIA 叫 warp occupancy，AMD 叫 wave occupancy。

## 两条路对偶

```
         ↑ ILP (unroll, long VGPR lifetime)
         │
    ┌────┼────┐
    │    │    │
 后效 DOF │   SSR
 blur/AO  │   POM
    │    │    │
    └────┼────┘
         │
         ↓ TLP (high occupancy, low VGPR)
```

一条 shader 里的 VGPR 预算是零和博弈：要么留给 ILP 的中间结果，要么留给多 wave 的活跃状态。Wronski 的总结是「对简单采样后效走 ILP，对任何带 data-dependent flow control 的算法走 TLP」。

## 难点：判断自己落在哪一边

只凭源码难看，必须读 ISA disasm。两个信号：

- **VGPR 使用量**：被编译器压到了几个？对应 occupancy 上 CU 几个 wave？
- **`s_waitcnt` 之前有多少独立 ALU cycle**：够不够覆盖预期的 L1/L2 latency？

对不确定的场景，**动手跑 profiler** 比任何启发式都靠谱——Wronski 自己做过「强制退回循环换 occupancy」的实验，结论常常反直觉（cache thrashing、纹理单元上限、带宽饱和都可能让高 occupancy 变慢）。

## 什么时候两个都救不了你

- **多层 indirection table / 虚拟纹理**：每一跳都是一次依赖 fetch，`s_waitcnt` 深度比 wave 能隐藏的还要大。
- **bandwidth-bound shader**：VRAM 打满，换 wave 也等不到数据。
- **tex unit 打满**：TMU 是稀缺资源，高 occupancy 反而排队。

这类场景需要更高层的重构——把多层 fetch 合并、预计算、或者改用 LDS 做 tile 内共享。

## 相关
- [[gcn-wave-occupancy]]
- [[latency-vs-throughput]]
- [[cache-friendliness]]
- [[cuda-memory-hierarchy]]
- [[memory-hierarchy]]
- [[bartosz-wronski]]
- [[ampere-warp-stall-utilization]] — Nsight warp stall 实证 Ampere/Pascal 被 memory latency bound

## Sources

- [[sources/bartwronski-gcn-latency-hiding]]
