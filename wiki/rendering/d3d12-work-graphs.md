---
tags: [渲染, GPU, D3D12, 工作图, GPU驱动渲染, 调度]
date: 2026-04-14
sources: 2
---

# D3D12 Work Graphs

**Work Graphs** 是 DirectX 12 在 2024 年加入的新管线，配合 NVidia 与 AMD 的硬件支持，让 GPU 可以**自己生产并消费任务**——不再需要 CPU 下发 dispatch。它的意图是把 [[gpu-based-occlusion-culling]] 里那条"GPU 决策、CPU 调度、回到 GPU"的老回路封闭在显卡内部。

## 心智模型

把一个 work graph 想成若干 **节点**（node）组成的图：每个节点是一段 shader（目前只支持 compute shader 和 inline raytracing），从 GPU 内存或其它节点收到 **record**（数据记录），跑一段计算，再把新的 record 写给下游节点。不需要全局 barrier，也不需要预先分配大 buffer 容纳 indirect args。

一个节点的声明不太像 `numthreads` 就结束的那种 compute shader，要多上几组注解：

```hlsl
[Shader("node")]
[NodeLaunch("broadcasting")]
[NodeIsProgramEntry]
[NodeDispatchGrid(1, 1, 1)]
[numthreads(8, 8, 1)]
void ClassifyPixels_Node(
    [MaxRecords(1)] NodeOutput<TileRecord> Shadows_Node
);
```

`NodeIsProgramEntry` 标记图的入口，`NodeDispatchGrid` 是个**占位**——在 CPU 端通过 `CreateBroadcastingLaunchNodeOverrides` 根据 RT 分辨率改写。`NodeOutput<T>` 声明一个下游节点以及允许发给它的最大 record 数 (`MaxRecords`)。

## 三种 launch 模式

节点的执行粒度由 `NodeLaunch` 决定：

- **broadcasting**：保留 threadgroup 概念，一个 record 被**整组**共享。适合 tile 分类这种一张 record 对应一整块像素的场景。由于仍有 threadgroup，可以用 **groupshared 内存** 和 Wave Intrinsics。
- **thread**：每个线程独享一条 record，不再有 threadgroup。**没有 groupshared，但 wave intrinsics 仍可用**。适合每像素不同的 ray origin / dir。
- **coalescing**：介于两者之间——声明一个 threadgroup 大小，GPU **尝试**（不保证）把零散的 worker 填进一个组里，于是又能用 groupshared 了。官方说"需要 groupshared 再用"，但 Kostas 在 SSSR 上发现：即便不用 shared memory，coalescing 相比 thread 也能提升 L1TEX 命中率，从而把整个 dispatch 从 2.18 ms 降到 1.81 ms。

## 记录的生命周期

产生输出 record 的 API 是 `GetGroupNodeOutputRecords(N)` / `GetThreadNodeOutputRecords(N)`：
一条**关键约束**是——这些调用必须 **threadgroup uniform**，不能放进 if 里、不能 thread-divergent。要表达"某个线程不需要输出"，就把 `N` 设成 0，而不是不调用。最后必须调用 `OutputComplete()` 来封装 record、交给下游。每个 threadgroup 请求的总记录数必须等于 `MaxRecords` 声明的上限，违反是 UB。

## CPU 端的 PSO

Work graph 的管线构建方式和 DXR 很像——走 `CD3DX12_STATE_OBJECT_DESC`，把一个 **global root signature**、一份编译好的 lib (`lib_6_8`) 和一个 `CD3DX12_WORK_GRAPH_SUBOBJECT` 组合进去；然后用 `IncludeAllAvailableNodes()` 把图里的节点全纳入。关键一步是 **backing memory**：这是 driver 在节点之间暂存 record 的 VRAM 缓冲，需要先调 `GetWorkGraphMemoryRequirements()` 查容量，再自己分配一块 UAV buffer 绑上去。执行用 `DispatchGraph()`，第一次调用时要带 `D3D12_SET_WORK_GRAPH_FLAG_INITIALIZE` 把 backing memory 初始化。

## 硬件实现线索

AMD 在 2024 年 HPG 上透露了一小段实现细节：每个节点在 VRAM 里有一条专属 **ring buffer** 存待执行的 command，上游节点的 SIMD unit 直接写进这个 ring buffer，下游节点由 **Micro Engine Scheduler** 的 Compute Unit 轮询、派发 warp。依靠每个节点声明的 `MaxRecords`，调度器能确保 ring buffer 不会溢出，从而避免死锁。NVidia 的实现目前没有公开资料，社区推测是"while loop 轮询 → 发射 → join 同步 → 下一批"的结构，同步靠 atomic——如果属实，可以解释观察到的寄存器压力偏高、 occupancy 被拖低的现象。

## 性能现状：不是立刻更快

Kostas 把 FidelityFX SSSR 的 **classification + raymarching** 两个 compute pass 改成 work graph 做对照：

| 实现 | 成本（1080p / RTX 3080 laptop） |
|---|---|
| compute shader + ExecuteIndirect | **0.65 ms** |
| work graph (thread launch) | 2.18 ms |
| work graph (coalescing launch) | 1.81 ms |

**慢了 2.8–3.3 倍**。GPU Trace 显示 work graph 版本的 SM utilisation、warp occupancy 都显著更低。进一步分离 classification 单独跑：compute shader 0.15 ms，work graph 0.49 ms——而且更诡异的是，**把 classification shader 改成空函数只节省 0.11 ms**，大头是节点生成/调度本身的固定开销。NSight 报告的 threadgroup/warp 数字和理论值对不上（80,000 → 40,516），暗示 driver/硬件正以一种"非单一 8×8 组"的方式重新打包工作。GPU Trace 里还能看到 **"Sync Q Waiting"** 高企，即 front-end 在等待 dispatcher——这是 compute shader 版本里没有的。

## 什么时候仍值得用

尽管当下比 compute + ExecuteIndirect 慢，work graph 解决的是后者的几个结构性痛点：

- **不需要保守分配 buffer**：GPU 写多少 record 就多少，不必预估最坏情况；
- **省掉 compaction/批处理 pass**：当前做法得跑额外的 shader 把稀疏 indirect args 压紧；
- **省掉 pipeline drain**：原来在 classification 和 consumer 之间必须插 UAV barrier，造成流水线 drain；work graph 由每个节点的 ring buffer 直接接力。

Kostas 演示的 "shadowmask 三级分类"（[[culling]] → hi-z raymarch → 加速结构 raytrace）是典型受益场景：GPU 自行决定"这一块只需要 classify、那一块需要 hi-z、还有一小块真的要追射线"，而三级之间没有 CPU 或 barrier 介入。

短期内，shipping 代码里的 classification pipeline 还得继续用 compute + indirect；**work graph 是往后看的机制**，等 driver 成熟、profiler 支持增强（目前 NSight 还看不到 SASS）之后才有机会追平甚至反超。

## 相关
- [[gpu-based-occlusion-culling]] — work graph 取代的旧式"GPU fill indirect args + CPU dispatch" 回路
- [[multidraw-indirect-occlusion-culling]] — 同样 Kostas 的 GPU-driven rendering 系列
- [[gpu-hazard-tracking]] — work graph 消除的正是大量 UAV barrier
- [[hybrid-raytraced-shadows-reflections]] — 他把这种三级分类用到 shadow 追踪
- [[bottleneck-analysis]] — 理解 Sync Q Waiting / SM occupancy 等指标
- [[async-compute]] — 另一个改善 GPU 利用率的手段，Kostas 的读者在评论区问"work graph 内部是不是在做 async compute？"
- [[sources/anteru-workgraph-spmv]] —— Chajdas 等 ISCA 2025，把 work graph 从图形管线移植到 SpMV，证明"动态输出 + host 往返敏感"的 HPC 场景 work graph 有实质收益（比 rocSPARSE LRB 快 3.35×，内存固定 25 MiB）
- [[variable-sized-work-pattern]] —— 同类问题的 wave 内尺度解法，和 work graphs 互补（work graphs 跨 threadgroup / 跨 dispatch）
- [[dxr-tier-2-clas-ptlas]] — DXR Tier 2.0 在光追侧做的三层加速结构拆分，思路与 Work Graphs 对应

## Sources

- [[sources/interplay-workgraphs-intro]]
- [[sources/interplay-workgraphs-performance]]
- [[sources/anteru-workgraph-spmv]]
