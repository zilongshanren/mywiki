---
tags: [程序化几何, mesh, 参数化曲面, limit-theory, 入门]
date: 2026-04-14
sources: 2
---

# 程序化几何基元：圆环、球、椭球

[[linden-reid]] 在 2017 年为 Limit Theory 写的一组"先懂数学再写代码"的几何教程。这条线的核心观点只有一句话：**3D 基元的顶点布局，本质上是把圆的参数方程层层嵌套**。一旦看穿这一点，torus、sphere、ellipsoid 就不再是三个独立的算法，而是同一个嵌套结构上调参数。这篇把这条主线整理出来，作为 [[unity-procedural-mesh]] 之上的下一级——后者讲的是"怎么把顶点/索引塞进 Unity Mesh API"，这里讲的是"顶点坐标从哪来"。

## 参数方程这一层心智模型

先从最朴素的圆开始：给一个角度 `t ∈ [0, 2π)`，`(x, y) = (cos t · r, sin t · r)` 就画出了所有点。要离散化，就把 `2π` 均分成 `n` 段（即 `dt = 2π/n`），每一步存一个顶点。Reid 反复强调"参数方程"的本质：**所有坐标都是某个角度的函数**，所以可以把 `cos/sin` 替换成任意其他参数函数，得到的仍然是一条闭合曲线。这个视角是后面所有基元的地基。

这也解释了为什么文章末尾能用一个 hypotrochoid（`x = a·cos³t, y = b·sin³t`）替换掉圆，得到一个"方形圆环"——算法骨架没变，只换了内层函数。

## 圆环（torus）= 两层嵌套的圆

圆环的直觉模型是一个甜甜圈：**沿着一个大圆的轨道，运动一个小圆**。大圆的半径叫 `outerR`（圆环主半径），小圆的半径叫 `innerR`（截面厚度）。用两个角度 `θ`（沿大圆走）和 `φ`（沿小圆走），顶点公式是：

```
x = cos(θ) · (outerR + cos(φ) · innerR)
y = sin(θ) · (outerR + cos(φ) · innerR)
z = sin(φ) · innerR
```

这里 `(outerR + cos(φ) · innerR)` 是"当前截面在 XY 平面上的投影半径"——当 `φ = 0` 时最大（`outerR + innerR`），`φ = π` 时最小（`outerR − innerR`）。外层的 `cos(θ), sin(θ)` 把这个投影半径旋转一圈就得到整个圆环。

索引生成采用 `stack × slice` 二维网格：相邻两个 stack 的同列和下列顶点组成一个 quad，拆成两个三角形。Reid 特别提到她这个实现**在接缝处存了重复顶点**——当 `slice = sl - 1` 时环绕回 0 的索引没做取模处理。后果是，如果你想算平滑法线或做其他需要顶点拓扑一致性的操作，要么先去重，要么算法里对坏三角形容错。这是一个"够用"而非"正确"的实现选择。

## UV 球（uv-sphere）= 半径随 y 变化的圆环层

UV 球的构造是圆环的降维版：**把环绕大圆的一圈换成从南极到北极的半圈**，同时每一圈（stack）的水平半径也随高度变化。形式化地，outer 角 `θ ∈ [0, π]` 控制南北，inner 角 `φ ∈ [0, 2π)` 控制经度：

```
stackRadius = sin(θ) · r         -- 当前 stack 在水平面上的半径
x = cos(φ) · stackRadius         -- 同 stack 内的 slice
y = cos(θ) · r                   -- 只取决于 stack
z = sin(φ) · stackRadius
```

注意 `θ` 只扫 `[0, π]` 而非 `[0, 2π)`——球是"半个周期的圆环"。南北两极是奇点：`sin(θ) = 0` 时所有 slice 都塌在同一点，所以 Reid 的实现**硬编码首尾两个极点**，让循环只扫 `stack = 1 .. n-1`。这与三角形索引的结构也配套——顶部 tris 是一组共享 index 0（顶极）的三角形扇，底部同理，中间层用 quad 网格。

共享顶点在接缝上的问题同样存在。和圆环一样，如果要算正确的法线，接缝处的顶点最好拆开。

## 椭球（ellipsoid）= 各向异性的球

从球到椭球只需要**把 `stackRadius` 和 `y` 半径分开**——分别用 `width`、`length`、`height` 三个参数替换原本统一的 `r`：

```
stackRadiusX = sin(θ) · width
stackRadiusZ = sin(θ) · length
x = cos(φ) · stackRadiusX
y = cos(θ) · height
z = sin(φ) · stackRadiusZ
```

索引结构和球完全一样——这也印证了最初的观点：**基元的拓扑是固定的，形状只是参数**。想做飞船的机舱、行星的扁椭球、或者任意比例的 capsule，这个参数化就够了。

## 这条线与其他基元生成方法的关系

Reid 在文章里明确提到这是 **UV-sphere** 方法，还有另一类 **icosahedron-sphere / icosasphere** 做法（先建正二十面体再细分）没覆盖。两者的区别体现在顶点分布的均匀性上：UV 球在两极密、赤道疏，icosasphere 全表面均匀——对需要做 [[mesh-warps-and-tessellation|per-face warp]] 或者 LOD 细分的场景后者通常更友好。

程序化生成出来的顶点流塞进 [[unity-procedural-mesh|Unity Mesh API]] 或任何其他 [[rendering-pipeline]] 入口都是一样的——参数函数是 CPU 侧的"顶点工厂"，不影响 GPU。真要优化吞吐，这种二维嵌套循环完全可以搬到 [[draw-procedural-gpu|compute shader]] 里跑。

## 相关

- [[unity-procedural-mesh]] —— Mesh API 侧的最小闭环
- [[mesh-warps-and-tessellation]] —— 有了基元之后怎么"让它变有趣"
- [[triangle-primitives]]
- [[rendering-pipeline]]
- [[linden-reid]]
- [[waving-grass-shader-vertex-offset]] —— 顶点动画对生成后 mesh 的运行时变形，和 CPU 侧的 warp / tessellation 是互补路线

## Sources

- [[sources/lindenreid-procedural-torus]]
- [[sources/lindenreid-procedural-sphere-ellipsoid]]
