---
tags: [rendering, ray-tracing, voxel, mobile, fallback]
date: 2026-04-19
sources: 1
---

# 混合体素软件光追

在没有硬件 RT 的设备上——MoltenVK 上的 Mac、大多数移动 GPU——如果还想保留 [[path-tracing]] 的世界观，就得有一套可接受的软件光追近似。直接在 compute shader 里跑完整 BVH 求交当然可以（tinybvh 已经给出现成数据结构），但"为什么显卡厂商还要专门做 RT Core？"——显然纯软件 BVH 不会比硬件 RT 快。所以工程意义是"在不支持硬件 RT 的设备上提供一个**够用**的近似"，而不是追求性能对等。

gameknife 的方案巧妙地复用了 [[ambient-cube-probe-pathtrace-exit|AmbientCube 探针]]：探针以 0.25 米为密度均匀分布全场景，每个探针会追踪若干条射线，**击中 mesh 背面记为距离 0，击中正面记录距离**——这样每个探针天然就存了一小段"到最近几何面的距离"信息，某种意义上把整个场景退化成了一个带方向的 sparse SDF 点云。

运行时的射线查询：沿 ray 方向遍历所经过的探针网格，根据探针里的"最大距离"决定跨多少步（类似 SDF sphere tracing）；遇到距离为 0 或 1 的探针，视作命中。这是一种密度严重不足但结构极简的 SDF 追踪——精度远低于硬件 BVH，但足以表达低频遮挡、漫反射间接光，对 SoftModern 这种"不追求物理精确，只要一个能动的 GI"的场景够用。

再往上套一层 voxel 数据结构——Voxel 层可由 CPU 实时生成（0.25 米格子），AmbientCube 层则在硬件或软件之间灵活选择——就得到了 gkNextEngine 的 hybrid context：**同一份探针数据在 4 种渲染模式（HardwarePT / SoftwarePT / SoftTracing / SoftModern）里都有意义**，这是整个引擎在桌面高端到移动低端都能跑的关键。

## Sources

- [[sources/gameknife-modern-rendering-how-modern]]
