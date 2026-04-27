---
tags: [渲染, 几何处理, meshlet, 压缩, mesh-shader, 带宽]
date: 2026-04-27
sources: 1
---

# Meshlet 压缩

[[meshlets-and-mesh-shaders|Meshlet 管线]]将几何体切分为约 64–128 顶点的小簇（meshlet），在 mesh shader 内独立处理。这一设计对剔除友好，但引入了新的存储问题：每个 meshlet 独立维护索引缓冲和顶点属性，传统顶点管线能共享的数据在 meshlet 间无法复用，总存储量可能反而膨胀。

## 压缩目标

Meshlet 压缩的目标是**在 mesh shader kernel 内进行数据并行 GPU 解压**，而不是在 CPU 或单独 compute pass 中预解压。这要求压缩格式能以 meshlet 为粒度独立解码，且解码逻辑简单到可以嵌入 mesh shader 执行。

## Chajdas 等的方案

[[matthaeus-chajdas|Chajdas]] 等设计的 codec 分两个子问题：

**索引缓冲压缩**：将 meshlet 内的三角形排列为**最优广义三角带（Generalized Triangle Strip，GTS）**，在条带内相邻三角形共享两个顶点，索引重复率高，压缩效果好。GTS 的最优排列通过**混合整数线性规划（MILP）**建模求解——这是离线预处理步骤，不影响运行时速度。最终索引缓冲压缩率达 **16:1**（相对于传统顶点管线的未压缩索引缓冲）。

**顶点属性量化**：采用 crack-free 量化——相邻 meshlet 边界上的顶点属性在量化后不产生裂缝，量化精度由用户按属性类型配置。

## 实测性能

在 AMD Radeon RX 7900 XTX 上，1550 万三角形解压 + 渲染耗时 **0.59ms**，与同硬件上的 [[catmull-clark-subdivision|Edge-Friend 细分曲面渲染]]（290 万三角形 0.58ms）数量级相当。

## 相关

- [[meshlets-and-mesh-shaders]]
- [[catmull-clark-subdivision]]
- [[matthaeus-chajdas]]

## Sources

- [[sources/anteru-meshlet-compression]]
