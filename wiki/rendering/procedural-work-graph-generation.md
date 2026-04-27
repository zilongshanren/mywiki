---
tags: [渲染, GPU, work-graphs, 程序化生成, 网格着色器, 实时]
date: 2026-04-27
sources: 1
---

# GPU Work Graphs 程序化内容生成

**GPU Work Graphs** 的动态任务生成能力与递归式程序化算法天然匹配：程序化内容生成（PCG）本质上是递归展开——一颗树展开成枝干，枝干展开成叶片，每一层都可能产生不等量的下游工作。传统上这要么在 CPU 上递归（GPU 等待），要么用 Compute + ExecuteIndirect 在 GPU 上多轮迭代（每轮要出入驱动）。[[d3d12-work-graphs]] 把"节点产生新工作"的能力直接放进 GPU 调度器，完全消除 CPU 往返。

## 工作结构

一个典型的 PCG work graph 有三类节点：

- **展开节点**（Expansion）：读入"种子" record（位置、参数），根据规则生成若干子 record 写给下游，相当于一次递归展开。
- **几何节点**（Mesh Shader 或 Geometry Emit）：接收展开后的 record，生成实际三角形或实例矩阵。
- **可见性节点**（Ray Tracing / Hi-Z Cull）：对生成的实例做可见性测试，只保留可见实体的 record 传给渲染节点。

这三者在图里串联，GPU 内部接力，没有 barrier，也不需要保守地预分配"最多可能有多少实例"的 buffer——[[d3d12-work-graphs]] 的 backing memory 由 driver 按需管理。

## 与 Mesh Shaders 的组合

[[mesh-shader-pipeline|Mesh Shader]] 管线本身已经能在 GPU 上生成任意几何，但它的 dispatch size 还是由 CPU 决定。Work Graphs + Mesh Shaders 的组合让 dispatch size 本身也变成 GPU 决策：上游节点数出"需要多少个 mesh shader 工作组"，直接写入 record，Mesh Shader 节点消费。这是目前让程序化内容完全驻留 GPU 的最干净的方案。

## 性能数据点

Chajdas 等人的演示在 AMD Radeon RX 7900 XTX 上，**3.74 ms** 内向场景中放置 **79,710 个实例**，并支持实时编辑预览。这一数字说明动态实例化的调度开销已经降到可接受范围，尽管 [[d3d12-work-graphs]] 页面记录的 SSSR 对照实验显示 work graph 当前对"已有 compute 优化好的 pass"仍有 2–3× 开销。程序化生成场景属于"GPU 决策量大、中间产物不确定"的类型，这里 work graph 的结构优势比纯 compute 场景更能体现。

## 已知约束

- 当前只支持 Compute Shader 节点和 Inline Ray Tracing——不支持完整的 VS/PS 管线节点，几何发射仍需通过 Mesh Shader 或实例化的方式绕行。
- backing memory 必须保守预分配（调用 `GetWorkGraphMemoryRequirements()`），大量递归展开仍需合理估计最大展开量。
- Driver 对 work graph 的 profiling 支持仍不完整（NSight 暂时看不到 SASS 级别追踪），生产调试成本较高。

## 相关

- [[d3d12-work-graphs]] — 机制详解与性能分析
- [[mesh-shader-pipeline]] — 几何生成节点
- [[infinite-chunked-procedural-generation]] — CPU 端无限程序化地形
- [[draw-procedural-gpu]] — 早期 GPU-driven 程序化绘制

## Sources

- [[sources/anteru-procedural-work-graphs]]
