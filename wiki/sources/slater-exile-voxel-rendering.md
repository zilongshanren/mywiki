---
tags: [source, 渲染, 体素, 网格生成, 游戏引擎]
date: 2026-04-14
sources: 1
---

# Exile: Voxel Rendering Pipeline（Max Slater）

[[max-slater|Max Slater]] 2018 年 8 月发表，记录他自研体素引擎 **Exile**（GitHub: `TheNumbat/exile`）的渲染管线设计。Exile 是「Minecraft 风格」的方块渲染引擎——不是 ray marching 的 SDF voxel——从零开始用 C 风格 C++ 写。

## 摘要

文章先交代体素世界的优缺点：交互性、系统性（自然的网格基础）、性能（很多优化可用）、美学（远距离紧凑）；缺点是不适合写实、没有天然的 LOD。Exile 的世界是 $\mathrm{UINT32\_MAX}^2 \times 511$ 的方块场，按 $31 \times 31$ chunks 按需生成 / 加载（hash map）。

渲染技术上 Slater 比较了三条路：**instancing**（每方块一个 mesh 实例，容易，但 overdraw 极重）、**geometry shader**（紧凑但 GS 性能差）、**meshing**（把方块转成静态 mesh——最快）。最终选择 [[greedy-voxel-meshing|贪心 meshing]]：每 chunk 生成一个优化过的 quad mesh，每个 quad 4 个紧凑顶点，通过 instanced 四顶点三角带提交——`gl_VertexID` 选本顶点数据，vertex shader 解包然后输出。

[[voxel-ambient-occlusion|AO]] 在 mesh 阶段就烘进顶点：每顶点 0~3 级 AO，由三个相邻 voxel 决定；但要**在每个顶点里存所有 4 个顶点的 AO 值**，让 fragment shader 用 $u/v$ 做双线性插值（否则 GPU 重心插值会暴露对角线接缝）。

[[compact-vertex-format|紧凑顶点格式]] 是 8 字节 / 顶点（`uvec2`）：$x, z, u, v$ 各 8 bit（乘以 8 支持 1/8 格捕捉，所以 chunk 选 31 而不是 32）；$y$ 12 bit、tex_id 12 bit、4 × 2 bit AO。

## 关键要点

- **Minecraft 风 voxel 的瓶颈是几何量而非 shading**——把 $O(N^3)$ 的方块压成 $O(N^2)$ 的四边形是头等大事。
- **greedy meshing 合并面 + 剔除内表面**：同方向 / 同材质 / 同 AO 的连续面合成一个大 quad。
- **AO 信息的四顶点广播 trick**：避免 GPU 三角形重心插值在对角线上出伪影。
- **chunk 大小 = 31** 的选择完全被 8-bit 顶点字段的位宽反推出来——[[information-leakage|信息泄漏]] 的硬件版本。
- **实例化四顶点 triangle strip** 是把 quad mesh 喂 GPU 的便捷方法；vertex shader 里同时读 4 个顶点算法线，省了一个 normal attribute。
- **静态 mesh 永远是 GPU 最爱的路径**，所以 Exile 最终放弃了 geometry shader 的紧凑方案。

## 链接到的概念

- [[greedy-voxel-meshing]]
- [[voxel-ambient-occlusion]]
- [[compact-vertex-format]]
- [[max-slater]]
- [[perspective-correct-interpolation]]

## 原文

- 链接：https://thenumb.at/Voxel-Meshing-in-Exile/
- 仓库：https://github.com/TheNumbat/exile
- 本地：`raw/articles/thenumb.at/2018-08-26_exile-voxel-rendering-pipeline.md`
