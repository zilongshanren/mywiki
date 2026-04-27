---
tags: [渲染, compute-shader, 性能优化, gpu, amd]
date: 2026-04-27
sources: 2
---

# Compute Shader 并行归约优化

并行归约（Parallel Reduction）是后处理管线中的基础操作：把一帧像素数据逐级折叠为单个标量（典型用途：计算亮度直方图、平均曝光、全屏求和）。算法本质是树形结构——每一轮折叠把工作组内的活跃线程数减半，直至剩下 1 个线程写出结果。由于无法在 GPU 上运行真正的递归核，通常用 for 循环模拟这棵树。

## TGSM 银行冲突

Thread Group Shared Memory（TGSM）在 AMD 和 NVIDIA 硬件上都采用 32 个内存 bank 的布局，地址以 DWORD 为粒度连续排列。当多个线程同时访问地址相差 32 DWORD 倍数的元素时，会命中**同一 bank**，产生串行化的 bank conflict。

[[angelo-pesce|Nicolas Thibieroz]] 总结的经验规则：让 32 个线程分别命中 32 个不同 bank，即按"行优先"顺序访问二维共享数组，而非"列优先"。交叉访问（interleaved）模式与顺序访问（sequential）模式在现代 AMD 卡（HD 6770/7750/7850）上差异已经缩小——驱动或硬件可能已在内部重排。

## 展开循环消除内存屏障

NVIDIA Warp 宽度为 32，AMD Wavefront 宽度为 64。在同一 Warp/Wavefront 内部，指令是 SIMD 同步执行的，因此**当活跃线程数降至 Warp/Wavefront 宽度以下，`GroupMemoryBarrierWithGroupSync` 不再必要**。

手动展开（`[unroll]`）for 循环有两重收益：一是减少地址运算与循环控制指令的 overhead；二是可在代码中明确标注从哪一步起进入 warp/wavefront 内同步安全区，从而裁掉多余的 barrier。实测数据显示旧型号 GPU（HD 6770）收益更明显，新型号已基本持平——编译器或驱动早有类似优化。

## 预取多个颜色值

标准实现中，线程组第一次从设备内存加载数据时才利用了所有可用线程；归约开始后线程利用率立即折半。通过**在加载阶段每个线程预取 2 个或 4 个像素值并预加法**，可以：

- 将线程组大小从 256 缩减至 64（预取 2 值）或 16（预取 4 值），彻底避免内存屏障；
- 同时减少 Dispatch 的 grid 大小，降低调度开销。

实测中预取 4 值（16 线程，无 barrier）的性能接近线性叠加。但若进一步增加线程组至 64 同时预取 4 值，则一次 Dispatch 做的工作量更大（结果图更小），吞吐反而更高。Engel 给出的最终最优点是：256 线程 + 预取 4 值，1080p → 30×17，frame time 降至原始基准的约 1/10（HD 6770）。

## 关键结论

1. 现代 AMD GPU（HD 7000 系列起）对 sequential vs interleaved TGSM 访问已无显著差异；
2. 展开循环减少 barrier 对旧 GPU 帮助显著，新 GPU 提升有限；
3. 预取多个值是目前最有效的优化手段，且效果随值数线性增长；
4. "每 dispatch 做更多工作"（减少 grid size）优于"更少工作 + 更多 dispatch"。

## 相关

- [[async-compute]] — compute shader 在渲染管线中与光栅化并行执行
- [[gcn-wave-occupancy]] — AMD GCN wavefront 占用率与延迟隐藏
- [[register-spilling-avoidance]] — 线程减少后寄存器压力相关优化
- [[cuda-memory-hierarchy]] — CUDA 中类似的共享内存模型

## Sources

- [[sources/humus-compute-parallel-reduction]]
- [[sources/humus-compute-reloaded]] — 2015 年再版：补充 HD 6770/290X 实测、确认带宽为最终瓶颈
