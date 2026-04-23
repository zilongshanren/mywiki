---
tags: [gpu, parallelism, command-buffer, dispatch]
date: 2026-04-19
sources: 1
---

# GPU 天生并行：为何无需并行命令派发

[[ben-supnik]] 曾向「圣诞老人」许愿：希望 OpenGL 支持并行命令派发，这样 8 核 CPU 就能同时向 GPU 塞入 8 条命令流，把 CSM 多级阴影图的独立渲染并行化。一位 CUDA 开发者点醒了他——并行内核（parallel kernel）在 CUDA 里的真正目的不是把工作分给更多「核心」，而是防止 GPU 在 batch 切换之间空闲。因为即便是数百个着色器单元，单个 kernel 覆盖的数据点也动辄成千上万，一次派发已足以喂饱整块卡。

把这套观察搬回图形管线，结论是：现代 GPU 的着色器数量（即使是几百个）仍远小于任何非平凡光栅化任务的 fragment 数。一张 256×256 的环境贴图就是 65536 个像素，加上 overdraw 更多；整块卡会很忙，只是很短时间。图形工作依然是「令人尴尬地并行」（embarrassingly parallel）的典型，所以在单卡场景下串行派发命令已经足够让 GPU 不空转，并行命令队列在架构上并不能带来额外带宽。

真正留下的问题是另一个维度：如果 batch 本身极其简单但每次都伴随显著的 CPU 侧驱动开销（shader 切换、状态变更判断），多 context / 多核填充命令缓冲区能否加速 CPU 侧而间接避免 GPU 饿死？Supnik 承认自己没能用实验回答——很难从应用层面分清 batch 成本里有多少是「判断是否要改配置」的决策开销、多少是「真正要改 GPU 程序」的硬件开销。这层区分直到后来的 [[gpu-queues-vs-dispatch-execution]] 与多队列显式 API 才系统化厘清。参见 [[gpu-latency-hiding]] 与 [[draw-call]]。

## 相关

- [[gpu-queues-vs-dispatch-execution]]
- [[gpu-latency-hiding]]
- [[draw-call]]
- [[async-compute]]
- [[cached-shadowmaps]]

## Sources

- [[sources/supnik-santa-youre-an-idiot]]
