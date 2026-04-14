---
tags: [source, md5, 骨骼动画, opengl, 模型加载]
date: 2026-04-14
sources: 1
---

# Loading and Animating MD5 Models with OpenGL（Jeremiah van Oosten）

[[jeremiah-van-oosten]] 2011 年的一篇长文，从零讲透 [[md5-model-format|MD5 模型格式]]的解析与运行时动画播放，使用 OpenGL + GLM + SOIL + boost::filesystem 实现，是 *Doom 3* 时代骨骼动画的"考古级"参考实现。

## 摘要

文章分两半。前半是格式说明：`.md5mesh` 的 header / joints / mesh 段每一个字段都给了语法和样例，并解释为什么 MD5 把方向四元数只存 3 个分量、`w` 为何要在加载时由 `w = -sqrt(1-x²-y²-z²)` 现算补回；mesh 段里 vert / tri / weight 三层结构以及"顶点位置 = Σ joint.pos + (joint.orient · weight.pos) × bias"的合成公式被反复强调。`.md5anim` 部分讲清楚 hierarchy 段的 `flags` 位掩码如何决定每个关节哪些自由度从 baseframe 拷、哪些从 frame data 覆盖。后半是 C++ 实现：`MD5Model` 类负责解析与渲染，`MD5Animation` 类负责帧插值，CPU 端每帧重新计算所有顶点位置和法线，再用 `glDrawElements` 提交。

## 关键要点

- MD5 的"权重"绑定的是**关节本地空间中的位置**，不是 bind-pose 顶点；最终位置是这些位置在各关节当前姿态下的加权求和。
- baseframe + frame data + flags 三者结合的紧凑表示：未被动画驱动的自由度从 baseframe 取，省掉了大量冗余。
- 文章用的是 **CPU 蒙皮**——所有顶点变换都在 C++ 里完成，每帧重新上传顶点缓存。后续的 [[sources/3dgep-md5-gpu-skinning|GPU 蒙皮版本]] 会把这一步搬到 vertex shader。
- 实现细节里频繁出现的 `glm::toMat4(quat)`、`glm::translate`、`glm::inverse` 等调用，是理解 [[gpu-skinning-matrix-palette|矩阵调色板]] 算法的前置。

## 链接到的概念

- [[md5-model-format]]
- [[gpu-skinning-matrix-palette]]
- [[3d-rotation-math]]
- [[mvp-transform]]

## 原文

- 链接：https://www.3dgep.com/loading-and-animating-md5-models-with-opengl/
- 本地：`raw/articles/3dgep.com/2011-03-14_loading-and-animating-md5-models-with-opengl.md`
