---
tags: [source, gpu, intel, battlemage, arc-b580, raytracing, bvh, xe2]
date: 2026-04-27
sources: 1
---

# Raytracing on Intel's Arc B580（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 3 月的文章，通过 Intel GPA 捕获的 Cyberpunk 2077 路径追踪帧和 3DMark Port Royal 帧，分析 Battlemage（Xe2-HPG）架构的光追实现。

## 摘要

Battlemage 的光追加速器（RTA）在 Alchemist 基础上将遍历管线从 2 条增至 3 条，专用 BVH 缓存从 8 KB 扩至 16 KB。在 Cyberpunk 2077 完整路径追踪模式下，B580 每秒处理约 4.68 亿条光线，平均每条光线需 39.5 次 BVH 遍历步骤。RTA 的盒测试与三角形测试利用率均低于 10%，主要瓶颈不在 BVH 遍历本身，而在 hit/miss 着色器阶段：着色器线程调度队列 80% 的时间处于满载或等待空闲 XVE 槽的状态。XVE 占用率虽高（93.8%），但实际 ALU 利用率低于 20%，主因是大量内存延迟与指令缓存缺失（命中率仅 92.7%）。Port Royal 因场景更简单、更缓存友好，ALU 利用率明显改善。Intel 的分层调度机制（hierarchical scheduling）是让 RTA 与 XVE 高效协作的关键。

## 关键要点

- RTA 增加第三条遍历管线，BVH 缓存翻倍至 16 KB，有效减少 L1 压力
- Cyberpunk 2077 路径追踪中 B580 的瓶颈在着色器执行而非 BVH 遍历
- XVE 高占用不等于高利用率：内存延迟和依赖链是真正限制因素
- Port Royal（混合光追）更适合 B580 的缓存容量，ALU 利用率更高
- Intel 仍使用与上一代相同的 64B box 和 triangle node 格式
- Xe3 将引入子三角形不透明度裁剪（sub-triangle opacity culling）及新数据结构

## 链接到的概念

- [[computer-systems/battlemage-architecture]]
- [[rendering/bvh-traversal-hardware]]
- [[rendering/xe-lpg-raytracing]]

## 原文

- 链接：https://chipsandcheese.com/p/raytracing-on-intels-arc-b580
- 本地：`raw/articles/chipsandcheese.com/2025-03-14_raytracing-on-intels-arc-b580.md`
