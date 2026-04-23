---
tags: [source, bitsquid, matrix, transform, floating-point]
date: 2026-04-19
sources: 1
---

# Matrices, Rotation, Scale and Drifting — bitsquid: development blog

[[niklas-frykholm|Niklas Frykholm]] 2012 年 7 月的文章，写 `Matrix4x4` 存 transform 时 scale 在长时间旋转下会线性漂移的老问题，给出四条修复方案并比较其利弊。

## 摘要

在 `Matrix4x4` 中 rotation 和 scale 共享同一 3×3 块；"只改旋转不改缩放"的实现必须先取 scale 再写回，浮点 round-trip 每帧引入一点误差。实测 28 分钟 0.1% 的放大——可感知。文章分析误差线性增长而非 random walk，说明背后有**系统性偏差**而非随机 round-off。四条解法：(1) pose 拆成 translation + `Matrix3x3` rotation + `Vector3` scale（推荐；总内存略小于 `Matrix4x4`；估算 scene-graph 局部到世界变换变慢约 12%，对整体 ~0.2%）；(2) 强制 rotation + scale 一起设，把 scale 维护推给用户（Bitsquid 临时方案，但用户容易复刻反馈回路）；(3) `scale()` 返回时 snap 到离散网格（hack 但 work，动画不受影响因为 animator 直接 `set_scale`）；(4) 深入 floating-point 分析消除系统偏差（最漂亮但最难）。Bitsquid 最终倾向 #1。评论里还有一个实用 trick：把 scale 塞进 `Matrix4x4` 最后一行前三列（本就恒 0），取 scale 直接返回不做 decomposition。

## 关键要点

- scale 漂移的根因：rotation 与 scale 共享 3×3 存储 + `scale()` round-trip。
- 误差 `e·N` 不是 `e·sqrt(N)` → 有系统性偏差。
- translation + rotation 不漂——因为 translation 在独立列里。
- 首推方案：pose 分存。代价 ~0.2% 总帧时间。
- 临时方案：`set_rotation_and_scale` 原子设置，把 scale 维护推给调用者。
- 量化方案：`scale()` 返回离散值，切断反馈回路且不影响动画。
- 评论 trick：scale 塞 `Matrix4x4` 最后一行前三列。

## 链接到的概念

- [[matrix-scale-drift]]
- [[3d-rotation-math]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/07/matrices-rotation-scale-and-drifting.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-07-03_matrices-rotation-scale-and-drifting.md`
