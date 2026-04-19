---
tags: [source, unity, urp, shader, vfx, 顶点动画, explosion]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Mesh Explosion（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 撰写的 **Mesh Explosion** 参数手册——三角形炸开的 vertex-driven VFX。

## 摘要

Mesh Explosion 在 [[sources/danielilett-toolbox-urp-base-lit|Base Lit]] 的表面基础上用 vertex shader 把三角形向外扩散。*Expansion Mode* 三档：**Normal** 沿 vertex normal 扩散（不需要预处理但三角形会变形）、**Offset** 从 *Explosion Origin Point* 沿 `position - origin` 方向扩散（每顶点自算方向，三角形仍会变形）、**Colors** 每顶点的 vertex color 预烘入"所属三角形的中心坐标"，三个顶点收到相同方向——唯一能保持三角形形状的模式。为支持 Colors 模式，pack 附带 **BakeFaceColors.cs** 脚本：遍历 mesh triangle list 求每个三角形中心 `(v0 + v1 + v2) / 3`，写入三个顶点的 vertex color（需要本地空间 bounds → `[0,1]³` 的编码）。*Explosion Distance* 驱动总进度（外部脚本 lerp 或 `Time.time`）、*Debris Shrink Speed* 让三角形随距离缩小消失、*Gravity* 沿 y 负向叠加位移产生弧线、*Random Offset Range* 每顶点独立 hash 打散（过大会毁掉三角形形状）。适用一次性非交互爆炸，交互碎片得用 Rigidbody 方案。

## 关键要点

- **核心挑战**：shader 的最小执行单元是顶点，让"三角形作为整体移动"要求三顶点收到完全一致的数据——而 shader 无法直接访问"我属于哪个三角形"，必须预先烘到顶点属性里
- **Colors 模式 + BakeFaceColors.cs** 是行业里处理这个问题的标准套路——把 triangle-level 静态数据 bake 进 vertex color（或任意 unused vertex stream）
- **Normal vs. Offset vs. Colors 的几何效果差异**：
  - Normal：每顶点沿自己的法线移动——会把三角形拉扯变大/变形
  - Offset：每顶点算自己的 `pos - origin` 方向——接近 origin 处变形严重
  - Colors：三顶点收到同一个 `center - origin`——严格平移不变形
- *Debris Shrink Speed* 需要以三角形中心为原点缩放（而非世界原点），否则碎片缩小时会"漂开"而非"收缩"
- 这类 shader 适用于**一次性爆炸演出**；需要物理交互的碎片必须用 pre-fracture + Rigidbody 方案
- 和 [[texture-dissolve|dissolve]] 叠加可以做"炸开的同时溶解消失"

## 链接到的概念

- [[mesh-triangle-explosion]]
- [[compact-vertex-format]]
- [[vertex-shader-basics]]
- [[texture-dissolve]]
- [[fizzle-lod-fading]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/mesh-explosion/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-mesh-explosion.md`
