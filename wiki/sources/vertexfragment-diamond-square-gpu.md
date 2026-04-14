---
tags: [source, rendering, noise, compute-shader, procedural, unity]
date: 2026-04-14
sources: 1
---

# GPU Accelerated Diamond-Square Generation（Steven Sell / Vertex Fragment）

[[steven-sell]] 2022 年 10 月发布的技术记录，给出 Diamond-Square 噪声的三种 Unity 实现（单线程 C#、多线程 C#、GPU compute shader）并横向测速，同时复盘为什么前两次 GPU 化尝试失败。

## 摘要

文章先把 Diamond-Square 的性质重新梳理一遍：边长 `2^n+1`、有界、需要状态、用户控制性强。它适合做地形的基础高度图而不是逐帧噪声。作者把它写成标准 FBM 外循环：步长从 `Dimensions/2` 开始逐次减半，每次先跑 diamond（对角四邻居平均 + 随机偏移）再跑 square（边四邻居平均 + 随机偏移），振幅随 persistence 衰减。CPU 版用自制 ThreadPool 把 diamond/square 步拆成 job，GPU 版用 Unity compute shader 在 structured buffer 上精确写入。性能表（8192²）：单线程 C# 13042 ms，多线程 C# 3121 ms，compute shader 778 ms。作者之前两次 GPU 化的失败很有启发：ShaderToy fragment shader 版因为无法维持跨 iteration 的可写状态而死；Unity 双 render target 版因为 fragment shader 里「精确像素寻址 vs 插值浮点」总差一点点，出来的值和 CPU 永远差一根丝；compute shader 一上就解决了这两个问题。有意思的是 GPU 版约一半时间耗在把 buffer 从 GPU 拉回 CPU——算法本身很快，瓶颈转到了 readback。配套仓库：github.com/ssell/GPU-Accelerated-Diamond-Square。

## 关键要点

- Diamond-Square 必须有状态、尺寸受 `2^n+1` 约束，不适合 shadertoy 式无状态 fragment 实现
- compute shader 是正确的 GPU 承载体：既能精确索引也能跨 iteration 持久化 buffer
- GPU 版相比单线程 C# 提速约 17 倍，相比多线程 C# 约 4 倍
- GPU→CPU readback 可占 GPU 版总耗时的一半，典型的「算得快但传不动」
- 适合"一次性生成地形基底"，再在上面叠 erosion、风化等效果

## 链接到的概念

- [[diamond-square-noise]]
- [[layered-grid-noise]]
- [[cuda-memory-hierarchy]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/diamond-square/
- 本地：`raw/articles/vertexfragment.com/2022-10-31_gpu-accelerated-diamond-square-generation.md`
