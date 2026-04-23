---
tags: [gpu, gcn, 性能优化, 并行, shader]
date: 2026-04-14
sources: 1
---

# GCN Wave Occupancy（波前占用率）

在 AMD **GCN（Graphics Core Next）** 架构上，每个 Compute Unit（CU）有 4 个 SIMD，每个 SIMD 可同时持有最多 **10 个活动 wavefront**（每个 wave = 64 线程）。**Wave occupancy** 就是一个 shader 在 CU 上实际能装下的 wavefront 数——由 VGPR（vector register）预算、LDS 预算、barrier 等因素共同决定。Wronski 2014 年的 GDC 后续博客把 wave occupancy 与「寄存器换延迟」摆到同一张天平上讲，是主机时代 shader 调优最被广泛引用的心智模型之一。

## 为什么重要：作为延迟隐藏的 TLP 分量

GPU 把内存延迟藏在两个互斥的机制里：

- **Per-wave ILP**：编译器把一堆 fetch 提前发出，再插入大量独立 ALU 把 fetch 到 use 的距离拉开，让 `s_waitcnt` 到来前数据已经回来。代价是 VGPR 占用膨胀——VGPR 寿命 = fetch 发出到最后一次 use。
- **Per-CU TLP（线程级并行）**：同一 SIMD 上挂多个 wave，当一个 wave 卡在 `s_waitcnt` 时切到别的 wave 跑它的 ALU。代价是每个 wave 能用的 VGPR 上限更紧——整个 SIMD 只有 256 个 VGPR。

两条路是方向相反的：ILP 要「低 occupancy + 深 unroll」，TLP 要「低 VGPR + 高 occupancy」。[[gpu-latency-hiding|GPU latency hiding]] 在 GCN 上就是在这两者之间二选一（或折中）的艺术。

## VGPR 与 occupancy 的数字关系

GCN 每个 SIMD 有 256 个 VGPR，如果一个 shader 使用 X 个 VGPR，则每个 SIMD 能装 `floor(256 / X)` 个 wave：

| VGPR/wave | Wave/SIMD | Wave/CU (4 SIMD) |
|---|---|---|
| 24 | 10 | 40（硬件上限） |
| 32 | 8 | 32 |
| 48 | 5 | 20 |
| 64 | 4 | 16 |
| 84 | 3 | 12 |
| 128 | 2 | 8 |

（硬件占用率最高为 10 waves/SIMD，即使 VGPR 用得极少也不会更多。）

## 何时 occupancy 不重要

一个反直觉的结论：**对很多 shader，提升 occupancy 甚至会降低性能**。Wronski 用一个老式 Poisson DOF 作例子——编译器默认展开整个采样循环，把所有样本坐标、depth/CoC、color 预取到大量 VGPR 里，occupancy 被压得很低，但：

- 采样之间彼此无依赖，ALU 可以紧贴在 fetch 之间。
- 中心像素的 depth/CoC 早就在 L1/L2 里。
- `s_waitcnt` 来到时数据几乎都已经就位。

强行压回循环、逼编译器减少 VGPR 用量，occupancy 虽然翻倍，但实测**性能持平甚至更差**——因为额外的 wave 会互相 thrashing [[cache-friendliness|cache]]（GCN L1 = 16KB 4-way，容量极小），还要和纹理单元抢吞吐。这类场景包括：老式后效、大量独立样本的 blur / AO、规则 taps 的 filter。

## 何时 occupancy 是救命稻草

反过来，当 shader 的控制流无法在 wave 内拉开 fetch 与 use 的距离时，唯一的办法就是让别的 wave 顶上。Wronski 列出的典型「吃 occupancy 的算法」：

- **Ray tracing / ray marching**（SSR、POM、volumetric）
- **多层 indirection table / 虚拟纹理**——最狠的性能杀手
- **延迟着色里的 BRDF 类型分支**
- **Forward 光照里的灯光类型分支**
- **data-dependent flow control**——循环早退出条件依赖 fetch 结果

Wronski 明确说，AC4 的 [[screenspace-reflections|SSR]] 和 parallax occlusion mapping 都属于这一类，必须死命压 VGPR 才能把 occupancy 顶上来。

## LGKM vs VM

GCN 有两类 `s_waitcnt` counter：`LGKM_CNT`（LDS / GDS / 常量 cache / 消息）和 `VMCNT`（vector memory fetch）。常量 cache 有独立的 scalar unit、延迟很低，LGKM 很少是瓶颈。真正要盯的是 **VMCNT**——它是 L1/L2 miss 的延迟暴露点。读 ISA disasm 时第一件事就是定位 `s_waitcnt vmcnt(n)` 的位置和它之前的独立 ALU 数量。

## 实践法则

Wronski 总结的经验：

- **简单多样本后效 → 低 occupancy + 高 unroll**；别去干扰编译器。
- **next-gen 算法 → 尽量压 VGPR 争 occupancy**；必要时手动重排变量生命周期。
- **验证手段 → 读 ISA**。不存在「只写高层不关心硬件」的实时渲染程序员。
- **工具 → CodeXL、AMD Shader Analyzer、PS4/Xbox One 厂商的私有 profiler**。

## 相关
- [[gpu-latency-hiding]]
- [[latency-vs-throughput]]
- [[cache-friendliness]]
- [[cuda-memory-hierarchy]]
- [[register-spilling-avoidance]]
- [[screenspace-reflections]]
- [[bartosz-wronski]]
- [[ampere-warp-stall-utilization]] — Ampere/Pascal 的 warp stall 与 occupancy 差异
- [[gpu-driver-support-lifecycle]] — GCN 2/3 硬件 EOL 话题

## Sources

- [[sources/bartwronski-gcn-latency-hiding]]
