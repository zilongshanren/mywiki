---
tags: [source, 渲染, 环境探针, 视差映射, 重投影, 反射]
date: 2026-04-27
sources: 1
---

# Half-Baked: Probe Warping（Angelo Pesce）

[[people/angelo-pesce]] 发表于 2025 年 8 月的文章，记录了一次将探针数据从烘焙位置重投影到新位置的半成品尝试，最终发现该算法是视差映射的球面变体。

## 摘要

Pesce 想解决的问题：一个在位置 A 烘焙的深度感知探针（存储了每个方向的场景深度），如何近似出在位置 B 看到的结果？最直接的方案（scatter 点云或 raymarch）过慢。他在 GeoGebra 上涂鸦推导出一个迭代几何算法：沿查询方向在 A 探针中采样得到交点 S1，在 S1 处构造垂直平面，从 B 与该平面求交得到 I，再在 A 探针中从 A 向 I 采样得到 S2，将 S2 投影到 B 的射线上作为近似交点。多次迭代可收敛。然而他意识到这正是**视差映射（parallax mapping）**的球面类比——单次迭代对应"offset mapping"，多次对应"steep parallax mapping"。Pesce 在 Shadertoy 上用 Gemini 辅助构建测试框架后验证了该方法，在单步情况下效果不错，两步反而因过度扭曲变差。对于预卷积 specular 探针仍需谨慎，Jacobian 变化会在高光中明显。

## 关键要点

- 深度感知探针可类比点云，但 scatter/raymarch 开销太高；"warp 采样方向"是更轻量的替代
- 推导出的迭代算法本质是视差映射在三维球面探针上的推广：单步≈offset mapping，多步≈steep parallax
- 球面的深度应低分辨率存储并用 mip 平滑以减少不连续性对 warp 稳定性的影响
- 与传统[[rendering/parallax-corrected-cubemap]]（代理形体解析求交）相比，此方法数学更简单，无需分析型代理
- 论文 "Approximate Ray-Tracing on the GPU with Distance Impostors"（Szirmay-Kalos 等）独立发现了相同方法

## 链接到的概念

- [[rendering/probe-warping]]
- [[rendering/parallax-corrected-cubemap]]
- [[rendering/environment-probe-placement]]

## 原文

- 链接：https://c0de517e.com/025_cubeproj.htm
- 本地：`raw/articles/c0de517e.com/2025-08-04_half-baked-probe-warping-reinventing-the-obvious-in-a-contri.md`
