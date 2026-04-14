---
tags: [shader, shadergraph, uv, 纹理, 渲染]
date: 2026-04-14
sources: 1
---

# UV 操作节点（Tiling/Offset、Rotate、Flipbook、Polar）

在 Shader Graph 里，`Sample Texture 2D` 只是终点——真正决定画面结构的是它上游对 **UV 坐标**的一连串操作。Cyan 的 UV-Based Nodes 教程把 Shader Graph 里最常用的几个 UV 变换节点讲清楚，其中有几个容易被误解的点，值得抽出来沉淀。

## UV 是什么，它在管线的哪一环插值

一个模型在建模时通常会经过 **UV 展开**：把 3D 几何展平成 2D "net"，每个顶点分到一个 `(u, v)` 坐标，一般落在 `[0, 1]`。渲染时 UV 从 **顶点着色器**作为 varying 发到 **片段着色器**，在三角形内部逐像素**线性插值**——所以在一个四边形（quad）的 UV 预览里能看到 `(0,0)` 黑 → `(1,0)` 红 → `(0,1)` 绿 → `(1,1)` 黄的渐变，那正是插值的结果。模型可以有多套 UV 通道（UV0/UV1/...），Unity 内置球体就同时带两套——UV0 沿赤道缠绕，UV1 在底部安排 6 个方块按轴投影。

Shader Graph 里的 `UV` 节点直接吐出当前片段的 UV；`Sample Texture 2D` 的 UV 输入如果不连任何东西，默认用 UV0。

## Tiling And Offset：是"缩放"不是"平铺"

这个节点几乎是所有 Shader Graph 教程里被误解最深的一个。Cyan 强调：它的公式就是

```
Out = UV * Tiling + Offset
```

**它只是缩放 + 偏移 UV 坐标而已**。"平铺"效果之所以出现，是因为把这个输出喂给 `Sample Texture 2D`，而纹理的 Sampler State 的 Wrap Mode 被设成 **Repeat**——是**采样器**在重复，不是节点在重复。

后果：如果你不是采样纹理，而是用 `Rectangle`、`Ellipse` 这类程序化节点生成图形，`Tiling And Offset` 把坐标放大 3 倍，得到的只是**一个更大的矩形**，不会变成 3×3 网格。要真的拿到"重复"效果，必须在 `Tiling And Offset` 之后接一个 `Fraction` 节点，把坐标的整数部分扔掉，得到周期性的 `[0, 1)` 坐标空间。反过来，如果你在采样带 mipmap 的纹理时**也**插了 `Fraction`，会在 UV 从 1 跳回 0 的接缝处看到明显的 seam——因为 mipmap 筛选看到了相邻像素的剧烈跳变。

## Rotate、Flipbook、Polar Coordinates

- **Rotate** 绕一个 center 旋转 UV。注意它是 2D 的，不要和 `Rotate About Axis`（3D）混淆。配合 `Time` 节点就能做无成本的旋转纹理——但旋转中心默认是 `(0, 0)` 即左下角，通常需要设成 `(0.5, 0.5)` 才是可视化意义上的"绕中心转"。
- **Flipbook** 把 UV 映射到"从一张 N×M 网格纹理里抽第 k 格"的子区间，本身不做采样，只变换坐标。配合 `Time → Floor` 就是逐格跳的精灵动画。需要注意的是 UV 的 `(0, 0)` 在**左下角**，而美术准备的 sprite sheet 通常 tile 0 画在**左上角**——此时必须勾选 **Invert Y**。Tile index 越界（负数或超出总数）会自动回绕。
- **Polar Coordinates** 把笛卡尔坐标转成极坐标：输出 `R` 分量是离 center 的距离、`G` 分量是角度（单位是 `Length Scale` 乘上 `-0.5` 到 `0.5` 范围）。它是做**旋涡、虫洞、传送门、向心条纹、日芒**的基石——把极坐标的角度通道喂给 `Fraction + Step`，就得到辐射状光线。

## 和 Custom Vertex Streams 的交汇

Cyan 在文中顺带提到：Particle System 的 Custom Vertex Streams 会借用 UV 通道的额外分量（TEXCOORD0 的 `z/w`、TEXCOORD1、...）来传递 per-particle 数据——这是 [[particle-custom-vertex-streams]] 的话题。所以当你看到某个 Shader Graph 里 `UV` 节点的 channel 被设成 UV1 或者用 split 取它的 `z` 分量时，那多半是在读粒子系统塞进来的 AgePercent 或 StableRandom。

## 相关

- [[sampler-filter-wrap-modes]]
- [[planar-mapping]] —— 当模型 UV 不好用时用世界坐标算 UV
- [[particle-custom-vertex-streams]]
- [[fragment-shader]]
- [[shaping-functions]] —— 程序化图形的底层语法

## Sources

- [[sources/cyan-uv-based-nodes]]
