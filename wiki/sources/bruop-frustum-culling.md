---
tags: [source, rendering, culling, simd]
date: 2026-04-19
sources: 1
---

# Frustum Culling（bruop.github.io）

[[bruno-opsenica|Bruno Opsenica]] 2020 年 12 月的视锥剔除实战，从朴素顶点 clip-space 测试到 AVX2 手写 intrinsics，演示 CPU 剔除对 GPU 帧时间的杠杆。

## 摘要

测试场景是 10,000 个 BoomBox 网格排成 3D 网格，相机居中只看见一小部分。不剔除时 GPU 执行 5.8 ms、CPU 命令 2.4 ms，GPU occupancy 图显示大量 VS 没有对应 PS 工作——纯浪费。作者选用 OBB 而非 sphere 作为 bounding volume（对细长物更紧），但剔除测试极简：把 AABB 八顶点用 MVP 变到 clip space，任一顶点满足 `-w≤x,y≤w`、`0≤z≤w` 就判定可见。加上这一步后 GPU 时间降到 1.5 ms，CPU 多 1.2 ms（剔除本身）。进一步用 AVX2：把 4×4 矩阵乘法按行广播 + FMA 重写，AABB 8 顶点用 `__m256` 一次变换、水平 OR 归约 lane。AoS→SoA 布局、Hammersley 式地按 256-bit 宽度批处理，把剔除时间从 1.2 ms 压到 0.3 ms。文末作者自曝该顶点法会产生 [[obb-frustum-sat|false negative]]，埋下续篇伏笔。

## 关键要点

- 未剔：10k 物体 GPU 5.8 ms + CPU 2.4 ms = 8.2 ms
- 顶点 clip-space 测试：GPU 降到 1.5 ms、总帧时间 4.2 ms
- AVX2 手写 intrinsics：剔除 1.2 → 0.3 ms
- SoA 数据布局是 SIMD 的前提（否则 gather 吃掉收益）
- `_mm256_extractf128_ps` + permute 做水平归约
- 已知缺陷：OBB 顶点都在外、但边相交时会漏剔（→ [[obb-frustum-sat|SAT 续篇]]）

## 链接到的概念

- [[obb-frustum-sat]]
- [[ispc-simd-culling]]
- [[culling]]

## 原文

- 链接：https://bruop.github.io/frustum_culling/
- 本地：`raw/articles/bruop.github.io/2020-12-24_frustum-culling.md`
