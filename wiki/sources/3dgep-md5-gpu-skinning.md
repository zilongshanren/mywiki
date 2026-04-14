---
tags: [source, md5, 骨骼动画, gpu-skinning, vertex-shader, cg]
date: 2026-04-14
sources: 1
---

# GPU Skinning of MD5 Models in OpenGL and Cg（Jeremiah van Oosten）

[[jeremiah-van-oosten]] 2011 年的续篇，把上一篇里在 CPU 上完成的 [[md5-model-format|MD5 蒙皮]]搬到 GPU vertex shader，演示**矩阵调色板蒙皮（matrix palette skinning）**的标准做法。使用 OpenGL + Cg/CgFX 着色器语言。

## 摘要

文章先解释为什么 GPU 蒙皮值得做：CPU 路径每帧都要把成千上万个变换后的顶点 re-upload；GPU 路径只在加载时把 bind-pose 顶点上传一次，每帧只需要更新一小束骨骼矩阵 palette。然后给出新的数据布局：顶点新增 `boneIndices : vec4` 与 `boneWeights : vec4` 两个 stream，把"4 根骨骼影响一个顶点"的工业惯例直接编码进顶点格式。接下来是核心算法：`BuildBindPose` 为每根骨骼算出 bind-pose 矩阵和 inverse-bind-pose 矩阵；运行时每帧拿当前动画的关节矩阵乘上 inverse bind pose，得到 `skinMatrix[i] = animatedBone[i] · inverseBindPose[i]`，整组矩阵作为 uniform 上传到 GPU；vertex shader 用 4 个 weight 加权 4 次 `mul(palette[idx], pos)` 得到 skinned 位置，法线同理。文章还讨论了老 vertex profile 96 个 constant 的限制、CPU 蒙皮路径的保留意义（调试 / 物理 / 服务器端命中），以及把 inverse bind pose 提前烘进动画帧的算力 ↔ 内存折中。

## 关键要点

- `inverseBindPose` 的数学作用是"先把顶点从 bind pose 撤回关节本地空间，再用当前帧的关节矩阵推到目标位置"，让同一动画可以驱动不同体型的骨架。
- 4 个权重塞 `vec4` 是工业惯例；MD5 demo 里用 `assert(weightCount < 4)` 守住这个上限。
- 老 vertex profile 的 constant 上限 `96 × float4 = 24 矩阵` 是早期 GPU 蒙皮的硬约束，现在已被 constant buffer / SSBO / texture buffer 化解。
- demo 同时实现 CPU 与 GPU 两条路径，由 enum 在运行时切换——这是引擎里常见的双轨策略。

## 链接到的概念

- [[gpu-skinning-matrix-palette]]
- [[md5-model-format]]
- [[3d-rotation-math]]
- [[mvp-transform]]
- [[fragment-shader]]

## 原文

- 链接：https://www.3dgep.com/gpu-skinning-of-md5-models-in-opengl-and-cg/
- 本地：`raw/articles/3dgep.com/2011-05-14_gpu-skinning-of-md5-models-in-opengl-and-cg.md`
