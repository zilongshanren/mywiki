---
tags: [source, rendering, intel, raytracing, xe-lpg, igpu]
date: 2026-04-27
sources: 1
---

# Raytracing on Meteor Lake's iGPU（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 4 月的文章，深入分析 Meteor Lake iGPU 的硬件光线追踪实现（Xe-LPG RTA），并与 AMD RDNA 2/3 的光追方案做对比。

## 摘要

Xe-LPG 的光追加速单元（RTA）位于每个 Xe Core 内部，负责全程处理 BVH 遍历；XVE 仅负责发起光线和处理 hit/miss 着色器，在 RTA 工作期间占用率极低。RTA 使用 "restart trail"（29 个 3-bit 条目）+ 4 条目 short stack 管理遍历状态，全部保存在寄存器中，延迟远低于 AMD 将遍历栈放在 LDS 的方案（实测 Cyberpunk 2077 下 RDNA 3 有 46 cycle LDS 等待）。代价是需要更多遍历步骤（比深度优先搜索多约 16%）。Meteor Lake 每个 Xe Core 有独立 Thread Dispatcher，每秒可启动超 4100 万个着色器程序。实测 Cyberpunk 2077 路径追踪（7 FPS）与 3DMark Port Royal（8 FPS），iGPU 的 192 KB L1 承担超 1 TB/s 内部带宽，4 MB L2 有效拦截绝大多数 L1 miss。整体结论：光追技术实现扎实，但对 iGPU 这类本就难以流畅运行游戏的产品而言实用价值存疑。

## 关键要点

- RTA 独立处理 BVH 遍历，遍历状态全在寄存器（<16 B），延迟优于 AMD LDS 方案
- Restart trail 替代深度优先栈，多约 16% 遍历步骤，但每步极快
- 每 Xe Core 独立 Thread Dispatcher；每秒 >4100 万着色器启动
- L1（192 KB）命中率 87.9%，承担 >1 TB/s 带宽；L2（4 MB）有效拦截 L1 miss
- DXR 1.0 对应 Intel RTA 流程；DXR 1.1 RayQuery 跳过线程排序阶段
- Port Royal 测试中存在轻度 DRAM 带宽瓶颈（内存请求队列满载率 43.1%）
- 作者认为 iGPU 光追不实用，XMX 矩阵单元（AI 超分）价值更高

## 链接到的概念

- [[rendering/xe-hpg-architecture]]
- [[computer-systems/xe-lpg-igpu-architecture]]
- [[computer-systems/meteor-lake-chiplet-architecture]]
- [[rendering/bvh-traversal-hardware]]
- [[rendering/xe-lpg-raytracing]]

## 原文

- 链接：https://chipsandcheese.com/p/raytracing-on-meteor-lakes-igpu
- 本地：`raw/articles/chipsandcheese.com/2024-04-15_raytracing-on-meteor-lakes-igpu.md`
