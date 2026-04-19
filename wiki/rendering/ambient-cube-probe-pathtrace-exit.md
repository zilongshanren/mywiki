---
tags: [rendering, path-tracing, global-illumination, probe]
date: 2026-04-19
sources: 1
---

# AmbientCube 探针作为 Path Tracing 提前退出缓存

gkNextEngine 的 [[path-tracing]] 加速核心不是降噪器、不是 ReSTIR，而是一个很朴素的东西：**在场景里离散分布的 [[valve-ambient-cube|AmbientCube]] 探针作为 path tracing 的"提前退出"缓存**。每个探针位置会向 6 个 cube 朝向各自追踪多条射线，把周围光照信息烘焙成 6 个方向的 HDR 值，存在一个类似体素的空间结构里。

运行时的 PathTracing 走这样一条路：从相机发射 ray，按某个概率（`ExitProbability`，gameknife 默认 0.5）**提前退出**；退出时在命中点插值附近若干个 AmbientCube 的 6 面光照，作为这条 path 的"后续光路贡献"。这相当于把 path 后 k 次 bounce 的蒙特卡洛估计替换成了一次对预计算辐射度的采样——思路上和 **NEE（Next Event Estimation）** 有一点像，但 NEE 是朝光源方向解析采样，这里是朝"已知光照缓存"采样。概率 `ExitProbability` 直接控制渲染预算与方差的 tradeoff：越接近 1 越快但越偏；0 则退化成朴素 PathTracing。

AmbientCube 数据自身是怎么来的？可以由硬件 RT 实时更新（类似 DDGI），也可以由 CPU 在 tinybvh 上软件追踪生成。这就让它成了一个**混合渲染上下文（hybrid context）**：同一份探针数据在 PathTracing 模式里作 exit cache、在 [[hybrid-voxel-software-raytracing|SoftTracing]] 模式里既作 exit cache 又作软件光追的加速结构、在 SoftModern 模式里作为漫反射光源和镜面反射遮挡的来源——一套数据结构复用在多种渲染器里，是 gkNextEngine 伸缩性的关键。

配合 [[taa-history-rectification|时域累积]]——每帧 8 spp、累积 16 帧就相当于 128 spp——AmbientCube 提前退出方案即使不带降噪器也能给出可接受的画质。

## Sources

- [[sources/gameknife-modern-rendering-how-modern]]
