---
tags: [source, 2d渲染, sprite, instance-draw, storage-buffer, sokol, cloudwu]
date: 2026-04-19
sources: 1
---

# Soluna 2D 渲染管线的一点优化（云风的 BLOG）

[[cloudwu]] 发表于 2025 年 2 月的一篇开发笔记。独立做策略向游戏不需要炫技画面，前几年的 3D 移动端引擎对需求来说太重，他起了个新坑 **Soluna**——纯 2D 游戏框架，并顺手把 GPU 时代的 sprite 绘制做了一次从头推导。

## 摘要

云风从"最朴素的 2D pipeline = 把 sprite 当作两个三角形塞进 VB"出发，逐步加码：加 UV 采样 atlas → 加 2×3 变换支持旋转缩放 → 发现顶点数据里的 mat2 在 4 个顶点间完全重复，于是把唯一的 SR 矩阵搬进 storage buffer，顶点只保留 index → 再发现 index 和 translation 也在 4 顶点间重复，改用 [[draw-procedural-gpu|instance draw]] 解决。继续观察：2D sprite 矩形是轴对齐的，四个顶点只需对角两个；offset 矩形和 UV 矩形形状一致，可以共用。再把坐标压缩为 int16 像素值。最终每个 sprite 12 字节（6 个 int16）塞进 storage buffer，外加 draw primitive 中每实例 3 个 float（x, y, index）= 26 字节/sprite。CPU 侧用 sokol（单线程限制），多线程填 batch 结构，渲染线程统一翻译成图形指令，对默认材质走专门路径，sprite id 为负表示下一条是非默认材质的参数。

## 关键要点

- sprite 批渲染的每一次"让顶点数据瘦身"都对应一个几何观察：SR 重复、轴对齐、offset/uv 同形
- storage buffer + instance draw 是压缩 per-vertex 重复信息的标准组合
- 顶点坐标用 int16 像素值表达足够，节省带宽
- sokol 单线程约束 → 中间层 batch，任意线程填、渲染线程 drain
- sprite id 负数位作 material 调度位，省下 tag 字段
- 比早年 [[draw-procedural-gpu|ejoy2d]] 在 CPU 算 2×3 定点数矩阵的方案更适配现代 GPU

## 链接到的概念

- [[soluna-2d-engine]]
- [[sprite-batch-instance-draw]]
- [[draw-procedural-gpu]]
- [[compact-vertex-format]]
- [[batching]]
- [[vertex-shader-basics]]

## 原文

- 链接：<https://blog.codingnow.com/2025/02/>（2025-02-20）
- GitHub 讨论：<https://github.com/cloudwu/soluna/discussions/1>
- 本地：`raw/articles/blog.codingnow.com/2025-02-20_yun-feng-de-blog.md`
