---
tags: [source, rendering, fp64, map-projection, glsl, planet-engine, outerra]
date: 2026-04-27
sources: 1
---

# Double Precision Approximations for Map Projections in OpenGL（Outerra）

[[people/outerra-team]] 发表于 2014 年 5 月的文章，讲述在 GPU shader 中用纯 fp64 基本运算（加/乘/sqrt）近似实现地图投影所需三角与对数函数的方法。

## 摘要

`ARB_gpu_shader_fp64` 扩展为 GLSL 引入了双精度基本运算，但**故意不包含** `sin`、`cos`、`atan`、`ln` 等超越函数——规范如此规定，部分厂商甚至主动阉割以拉大消费级与专业显卡的差距。对于处理真实地理数据或实现地图投影（等经纬投影、墨卡托投影）的工具来说，fp32 精度不足，又不想为了一个函数引入 OpenCL 互操作。

文章的核心贡献是两段推导：一是用 lolremez 工具生成的 9 阶 minimax 多项式实现 `atan2`（误差 < 5×10⁻⁹，对应地球表面约 3 cm）；二是对墨卡托投影的 y 轴公式 `ln(tan(π/4 + φ/2))` 进行代数变形，将其展开为仅含 ECEF 坐标的 sqrt 与除法，最终把唯一剩余的 `ln` 归结为相对于 CPU 预计算参考值的差值，使用单精度 `ln` 计算极小增量，或直接用 `ln(x) ≈ 2x/(2+x)` 近似（在 x 接近 1 时误差可接受）。

## 关键要点

- `ARB_gpu_shader_fp64` 仅保证加/减/乘/除/sqrt，超越函数需自行实现
- `atan2` minimax 9 阶近似：10 个系数，Horner+FMA 求值，5e-9 绝对误差
- 墨卡托 y 公式通过 ECEF 坐标代换消去 `tan(φ)`，再通过对数差值技巧消去 `ln`
- 消费 GPU 的 fp64 吞吐量普遍被人为压低，避免在热路径滥用

## 链接到的概念

- [[fp64-map-projections]]
- [[fp64-sincos-minimax]]
- [[huge-world-coordinate-precision]]
- [[planet-terrain-dem-pipeline]]

## 原文

- 链接：https://outerra.blogspot.com/2014/05/double-precision-approximations-for-map.html
- 本地：`raw/articles/outerra.blogspot.com/2014-05-11_double-precision-approximations-for-map-projections-in-openg.md`
