---
tags: [source, 渲染, shader, 光栅化, 插值]
date: 2026-04-14
sources: 1
---

# Correctly interpolating view/light vectors on large triangles（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 5 月的短篇笔记：帮美术解一段 FX Composer 生成的 Blinn shader 在大三角形上出现的奇怪高光撕裂。

## 摘要

美术的 Blinn shader 在大三角形拼接的几何上出现了**沿某条边撕裂的高光分布**。Kostas 检查代码发现 view/light direction 是在顶点着色器里算好**再归一化**后下发到像素着色器的。原因是光栅化的 barycentric interpolation 在三角形**边**上退化为线性插值——两个共享这条边的三角形对角顶点属性差异大，共享边的插值结果完全由两个端点决定，边两侧的内部点向**不同对角**过渡，边线因此被「切开」。位置属性没事（它本身就有空间意义），但**归一化的方向向量**丢失了长度信息，线性插值出来的是弦上滑动而非方向平滑过渡。修复办法有两条：把方向计算搬进 pixel shader，或者在顶点阶段**不归一化**就下发、像素阶段再做 normalize——本质是利用「方向 = 两点之差」，位置差在屏幕空间经过 [[perspective-correct-interpolation|透视校正插值]] 后仍然正确。

## 关键要点

- Barycentric interpolation 在三角形边上退化为沿边的两顶点线性插值（对角顶点权重为零）
- 相邻三角形共享边 → 边上插值结果相同，但两侧内部从不同对角过渡，出现「切开」效果
- 只有**带空间语义**的属性（位置）能正确处理；归一化的方向向量没有空间语义
- 修法 1：方向计算全部放 pixel shader
- 修法 2（更省 ALU）：顶点阶段算出**未归一化**的 `Pw - CameraWS`、`Lamp0Pos - Pw`，像素阶段再 `normalize()`
- FX Composer 模板只归一化了 `WorldView`，但任意一个被归一化都会出问题——两个都必须未归一化
- 小三角形上几乎不可见；大三角形（地板 / 水面 / 美术快速原型）下立刻炸

## 链接到的概念

- [[vertex-vector-interpolation-artifact]]
- [[perspective-correct-interpolation]]
- [[rasterization]]
- [[diffuse-lighting-lambertian]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2013/05/17/correctly-interpolating-viewlight-vectors-on-large-triangles/
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-05-17_correctly-interpolating-view-light-vectors-on-large-triangle.md`
