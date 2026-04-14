---
tags: [source, shader, shadergraph, 纹理, uv]
date: 2026-04-14
sources: 1
---

# UV-Based Nodes（Cyan）

[[cyanilux|Cyan]] 2020 年 1 月发表的 Shader Graph 教程，系统讲解了一组和 **UV 坐标**相关的节点：**Sample Texture 2D**、**Tiling And Offset**、**Rotate**、**Flipbook**、**Polar Coordinates**。它是 Shader Graph 新手圈里流传最广的几篇入门资料之一——因为它把几个看起来简单但非常容易被误解的节点讲透了。

## 摘要

文章先铺垫 **UV** 的基本概念：美术如何通过 UV 展开给每个顶点分配 `[0,1]` 范围的二维坐标，顶点之间如何线性插值，模型如何带多套 UV 通道（UV0/UV1/...），Particle System 的 Custom Vertex Streams 如何借用闲置的 UV 通道分量传数据。随后逐个讲解：

- **Sample Texture 2D** 的 Sampler State 参数（Filter 三档：Point / Linear / Trilinear，Wrap 四档：Repeat / Clamp / Mirror / Mirror Once），顺带澄清 "Linear/Bilinear/Trilinear" 命名混淆。
- **Tiling And Offset** 的公式 `UV * Tiling + Offset`——它只是缩放和平移，"平铺"效果来自采样器 Wrap Mode 设为 Repeat，不是这个节点在做。想在程序化图形上产生平铺效果，需要在后面接 `Fraction`。
- **Rotate** 节点是 2D 旋转（别和 Rotate About Axis 的 3D 旋转混淆），默认中心在原点，旋转纹理需要手动设中心到 `(0.5, 0.5)`。
- **Flipbook** 把 UV 映射到网格纹理的子区块，Invert Y 选项处理 sprite sheet 左上角起的习惯与 UV 左下角原点的冲突。
- **Polar Coordinates** 把笛卡尔坐标转成极坐标 `(distance, angle)`，做旋涡、辐射条纹、传送门的关键节点。

## 关键要点

- UV 是每个顶点的属性，在光栅化时线性插值到每个 fragment——这是 Shader Graph 预览里 UV 节点呈现"黑 → 红 → 黄 → 绿"渐变的原因。
- Sampler State 的 **Linear** 在 shader 里就是 **Bilinear**；**Trilinear** 指额外做一次 mipmap 轴上的线性插值，和 3D 纹理无关。
- Tiling And Offset 不是"平铺节点"，它只是缩放 + 偏移——程序化图形要平铺必须配 `Fraction`。
- Flipbook 节点只操作 UV，不负责采样；Tile 索引可以结合 Time + Floor 做逐格动画。
- Polar Coordinates 的输出 R 分量是半径、G 分量是角度，配合 Fraction+Step 能快速做旋涡和向心条纹。

## 链接到的概念

- [[uv-manipulation-nodes]]
- [[sampler-filter-wrap-modes]]
- [[particle-custom-vertex-streams]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2020/01/14/uv-based-nodes/
- 本地：`raw/articles/cyangamedev.wordpress.com/2020-01-14_uv-based-nodes.md`
