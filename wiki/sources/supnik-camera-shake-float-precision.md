---
tags: [source, rendering, float-precision, x-plane, large-world]
date: 2026-04-27
sources: 1
---

# Fixing Camera Shake on Single Precision GPUs（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2018 年 1 月的文章，讲述 X-Plane 11.10 如何在不依赖 64-bit GPU 浮点的前提下，彻底消除大世界场景中的相机抖动。

## 摘要

X-Plane 的地形 tile 达 100 km × 100 km，摄像机距 origin 可达 50 km。在 32-bit 坐标精度下，1 cm 精度足以导致接近地面时顶点以超过 1 像素的幅度「跳跃」——即相机抖动（camera shake / jitter）。文章的核心贡献是一个两步方案：首先让 CPU 端变换栈升级为 double precision（GPU 侧不变）；再引入一个额外的「世界坐标预平移」步骤（pre-offset），以 4 km 粒度对齐摄像机位置，使顶点与摄像机的大偏移量相互抵消后产生的只是小量——从而把「大世界引擎」的抖动问题化归为「小世界引擎」的量级，无需移动 mesh 数据本身。

## 关键要点

- 抖动的本质是 MVP 变换中两个大量相减时的浮点取消误差（cancellation error），而非单纯的精度不足。
- CPU double + GPU float 的混合方案：变换矩阵的平移分量在 CPU 上以 double 计算，最终结果截断为 float 送 shader；不要求 GPU 有 fp64 支持。
- Pre-offset 算法：将摄像机位置在**世界坐标**（而非 camera 空间）中网格对齐，减去 offset 后代入变换；Shader 里 `v_eye = (v_world - O) * modelview_matrix`。
- Hardware instancing 同样需要在实例变换的平移分量中减去 camera offset，否则实例仍会抖动。
- GPU 端运算顺序对结果至关重要——精确按 pre-offset-then-transform 的顺序写才能生效，`precise`/`invariant` qualifier 不足以保证。

## 链接到的概念

- [[huge-world-coordinate-precision]]
- [[single-precision-float-world-offset]]
- [[gpu-latency-microbench-methodology]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2018/01/fixing-camera-shake-on-single-precision.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2018-01-13_fixing-camera-shake-on-single-precision-gpus.md`
