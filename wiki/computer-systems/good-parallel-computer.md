---
tags: [computer-systems, gpu, parallel, architecture, opinion]
date: 2026-04-19
sources: 1
---

# 好的并行计算机（宣言）

Raph Levien 的这篇《I Want a Good Parallel Computer》是一份对现代 GPU 执行模型的系统批评。他的基本判断是：现在的 GPU 比 CPU 强 10–100 倍算力，但被两件事卡住，无法成为"真正的通用并行计算机"——**一是贫瘠的执行模型**（处理规则大块数据很行，但动态工作负载困难），**二是语言和工具不到位**（并行编程就是比串行难很多）。Mesh shader、[[d3d12-work-graphs|work graphs]] 这些新特性"前进两步、后退一步"——每加一个新能力，就发现一件基本的事还没被正确支持。

具体的工程痛点来自他的 [[vello-gpu-2d-renderer|Vello]] 项目：一个 GPU 上跑的 2D 矢量渲染器，compute shader 里做 path geometry、binning、tile compiler 等等一连串 stage，中间结果的大小**依赖输入且不可预测**——改一个 transform 可能让渲染计划彻底不同。于是所有中间 buffer 都得在 CPU 端提前分配最大尺寸，要么浪费、要么失败重试。他想要的是 [[gpu-queues-vs-dispatch-execution|队列式 stage-to-stage]]——stages 之间用有限大小的队列相连，保持在飞工作量够大就好——而不是现在这种 dispatch + pipeline barrier 的栅栏模型。

他对历史上的三条"走对过的岔路"做了致敬：

- **Connection Machine**（1985）：64k 处理器、超立方连接，推动了 prefix sum 等并行算法研究。
- **Cell**（PS3, 2006）：8 核 SIMD + 每核 256KB SRAM + 全局 job queue，在他看来"基本满足了好并行计算机的定义"，但编程模型太粗糙（手工 DMA、没有高层工具），最终被放弃。
- **Larrabee**（2008）：标准 x86 + 512 位 SIMD + 极少硬件固化。Tom Forsyth 认为它没失败，只是以 Xeon Phi / AVX10 / ISPC 的形式延续了遗产。

四条前进路径（任何一条都可能成事）：**Cell reborn**（一颗芯片上几百个 RISC-V + SIMD，Tenstorrent / Esperanto 已在做 AI 版本）；**GPU 端运行 Vulkan 命令**（command processor 暴露给用户代码，CUDA 12 的 device graph launch 已经是半步）；**work graphs**（但目前缺 join、缺顺序保证、缺变长 element）；**CPU 演化**（E-cores 越来越多直到追上 GPU，但 perf-per-watt 差一个数量级）。他倾向"也许硬件已经在那里了，只是被软件锁住"——GPU 里那个藏起来的 command processor 如果对用户代码开放，大概率能直接给出答案。

这篇文章也是对 [[d3d12-work-graphs|D3D12 Work Graphs]] 的一次落地评价：Raph 认真研究过能不能把 Vello 改成 work graphs 执行，发现三个 blocker——不能表达 join、没有 ordering guarantee（2D 画老虎，胡须必须画在脸上面——Z-order 必须保留）、不支持变长元素。所以他的结论是"两步前进、一步后退"。

## Sources

- [[sources/raphlinus-good-parallel-computer]]
