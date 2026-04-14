---
tags: [source, shader, rendering-pipeline, allen-chou, 入门]
date: 2026-04-14
sources: 1
---

# Shader Primer（Allen Chou, 2011）

[[allen-chou|Allen Chou]] 2011 年 2 月为准备 Flash Molehill（Flash Player 11 的低级 GPU API）而写的一篇给队友/自己看的 shader 入门笔记。用伪代码跳过语言细节，只讲 shader 在渲染管线里的位置与最小可用的 VS/FS 对。

## 摘要

文章把 shader 类比为"驻留在 GPU 内存里的程序"：和 CPU 程序类似，但运行在专门硬件上，而且对每个顶点/每个像素**并行独立**执行——这意味着 shader 程序不能读其他顶点/像素的结果。接着作者给出顶点着色器和片元着色器的最小例子。VS 示例只做一件事：把输入的 4D 顶点乘以一个 4×4 [[mvp-transform|变换矩阵]]，输出裁剪空间坐标；这已经够把 3D 顶点投影到 2D 屏幕。FS 示例演示**插值变量**与**纹理采样**：UV 坐标在光栅化后自动被 GPU 以**透视正确**的方式插值（见 [[perspective-correct-interpolation]]），然后用 `sample(texture, uv)` 取颜色输出。评论区的读者追问到"透视正确"能否在 shader 里选择——作者补充说通常每个 shader 语言都提供插值修饰符，默认是透视正确。

## 关键要点

- Shader = 驻留 GPU 内存、被 GPU 硬件并行执行的小程序，对每个顶点/像素独立运行、不可互相访问。
- 最小管线：CPU 送顶点 → VS 变换到 clip space → 光栅化 → FS 决定每个像素颜色。
- VS 的标准职责就是 `clipPos = transform * vertex`；用 4×4 矩阵而非 3×3 是为了让平移也能塞进一次矩阵乘法。
- FS 读到的 UV 是被 GPU **透视正确插值**过的，而不是屏幕空间线性插值——这是远处三角形采样变稀疏的根本原因。
- Shader 语言通常允许用修饰符指定"透视正确 / 非透视 / 无插值"等插值方式。

## 链接到的概念

- [[rendering-pipeline]]
- [[fragment-shader]]
- [[mvp-transform]]
- [[perspective-correct-interpolation]]
- [[triangle-primitives]]
- [[shader-vector-math-primer]]

## 原文

- 链接：https://allenchou.net/2011/02/shader-primer/
- 本地：`raw/articles/allenchou.net/2011-02-17_shader-primer-ming-lun-allen-chou-zhou-ming-lun.md`
