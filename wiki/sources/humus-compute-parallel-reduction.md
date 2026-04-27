---
tags: [source, compute-shader, 性能优化, gpu, amd, 并行算法]
date: 2026-04-27
sources: 1
---

# Compute Shader Optimizations for AMD GPUs: Parallel Reduction（Wolfgang Engel）

[[people/wolfgang-engel]] 于 2014 年 3 月发表，并同期在 GDC 2014 Sony 展台演讲，一句话主题：针对 AMD GCN GPU 对并行归约 compute shader 进行系统性优化，覆盖 TGSM bank 布局、循环展开、屏障消除与多值预取四个维度。

## 摘要

文章以 Mark Harris 经典的 CUDA 并行归约讲稿为起点，针对 AMD RADEON HD 6770/7750/7850 给出详细的测量数据和对应优化策略。从树形归约的基本结构出发，依次讨论了：顺序访问 TGSM 减少 bank conflict（但实测现代 AMD 驱动已消除差异）；展开 for 循环减少地址算术开销并裁掉 warp/wavefront 宽度以下的不必要屏障；在第一次加载阶段预取 2 个、4 个颜色值以提升初始线程利用率；以及通过同时增大线程组尺寸和减小 dispatch grid 来让每个 dispatch 做更多有效工作。最终最优配置（256 线程 + 预取 4 值）将 1080p→30×17 归约的 frame time 降至原始方案的约 1/10。

## 关键要点

- AMD/NVIDIA 均为 32 bank TGSM；顺序访问优于交叉访问，但现代驱动可能已自动处理
- wavefront（AMD=64）/warp（NVIDIA=32）宽度以下无需内存屏障，手动展开可明确利用此点
- 预取多个值是最有效的单点优化；2 值 → 4 值接近线性提升
- "每 dispatch 做更多工作"（缩小 grid）优于"工作量不变但拆分更多 dispatch"
- 旧 GPU（HD 6770）从优化中收益更大；新 GPU 编译器/驱动已有部分优化

## 链接到的概念

- [[compute-parallel-reduction]]
- [[async-compute]]
- [[gcn-wave-occupancy]]
- [[register-spilling-avoidance]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2014/03/compute-shader-optimizations-for-amd.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2014-03-26_compute-shader-optimizations-for-amd-gpus-parallel-reduction.md`
