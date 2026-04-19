---
tags: [source, gpu, workgraphs, hpc, spmv]
date: 2026-04-19
sources: 1
---

# GPUs All Grown-Up: Fully Device-Driven SpMV Using GPU Work Graphs（ISCA 2025）

[[matthaeus-chajdas|Matthäus Chajdas]] 等（AMD + THI + DFKI + Intel）发表于 **ISCA 2025** 的论文，把 **Work Graphs**（原本为图形管线设计的 GPU 程序模型，见 [[d3d12-work-graphs]]）**移植到 HPC 领域的稀疏矩阵向量乘（SpMV）**，证明 GPU 端动态自调度在纯 compute 场景同样能带来显著收益。

## 摘要

SpMV 是高性能计算、图分析等领域的核心算子。不同矩阵（每行非零元分布差异大）对应的最优算法不同，因此 GPU SpMV 通常依赖**昂贵的 preprocessing** 来选择每行的算法。本论文把 preprocessing 和后续 per-row 处理**都放进 work graph**：利用 work graph 在 GPU 硬件/固件上支持的 **细粒度 dataflow 自调度**，workgroup 可以在 preprocessing 产生足够工作后立刻被下游消费，不同 kernel 的 workgroup 交错执行，提升 cache locality 并**彻底消除 host 交互**。

## 关键结果

- 59 个稀疏矩阵测试集中，最佳 Work Graphs SpMV 实现相比 rocSPARSE **LRB 单次 SpMV 加速最多 7.19×**（均值 3.35×，标准差 1.89）。
- 相比 rocSPARSE CSR-General 在不同稀疏模式下性能更**稳定**；即便与先进的 CSR-Adaptive 相比，也能在连续 92 次 SpMV 的场景下胜出。
- 代码复杂度比 rocSPARSE LRB 降低 **75%**。
- 支持数据结构的**内存开销固定 ~25 MiB**，不随矩阵规模增长；rocSPARSE LRB 随矩阵规模涨到几百 MiB。

## 意义

这是第一批证明 work graph **在图形管线之外**也有实质收益的论文。前文 [[d3d12-work-graphs]] 里 Kostas 的渲染场景基准显示 work graph 在 2024 年的 driver 下比 compute + ExecuteIndirect 慢 2.8–3.3×；本论文则展示**当 preprocessing 的输出量随输入矩阵变化极大、保守分配完全不可行**时，work graph 的 "不需要预分配 + 省掉 pipeline drain + 取消 CPU 回合" 三重优势反而能压倒静态 compute 方案。这和 Kostas 的"不是立刻更快，是往后看"的判断一致——**work graph 的收益场景是动态输出密集、host 往返敏感的工作负载**。

## 链接到的概念

- [[d3d12-work-graphs]]
- [[matthaeus-chajdas]]

## 原文

- 链接：<https://anteru.net/research/gpus-all-grown-up>
- 本地：`raw/articles/anteru.net/2025-02-16_gpus-all-grown-up-fully-device-driven-spmv-using-gpu-work-gr.md`
