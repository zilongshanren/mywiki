---
tags: [shader, 程序化纹理, 数学, 图案, 渲染]
date: 2026-04-14
sources: 1
---

# 程序化棋盘图案（procedural checkerboard）

在 shader 里零纹理生成一张棋盘图案，是程序化图形最经典的「麻雀虽小五脏俱全」的例子：它同时用到 **整数域的奇偶判定**、**`floor` / `frac` 技巧**、**多维坐标求和** 和 **`lerp` 颜色插值**，而且可以干净地推广到 2D 和 3D。

## 一维：黑白条纹

从 1D 开始。给定位置 `p`：

```hlsl
float c = floor(p);       // 向下取整到整数
c = frac(c * 0.5);        // 偶数 → 0, 奇数 → 0.5
c *= 2;                   // 奇数 → 1
```

`floor` 保证每个整数单元格内常量；`c * 0.5` 把偶数留在整数位、把奇数变成 `.5`；`frac` 取小数部分；最后乘 2 归一到 0/1。每一步都可以在纸上一眼验证。

## 二维 / 三维：分量求和

这个构造的妙处在于 **换维几乎不要代价**：

```hlsl
float c = floor(p.x) + floor(p.y) + floor(p.z);
c = frac(c * 0.5) * 2;
```

原理是「加 1 改变奇偶性」——相邻网格在任何一根轴上移动一个单元，`floor` 和改变 1，整体奇偶翻转，颜色跟着翻。这就是为什么必须先 `floor` 再相加、而不是 `floor(p.x + p.y)`：后者只在对角线方向翻转，画出来是斜条纹。

```
(0,0)=黑  (1,0)=白  (2,0)=黑 ...
(0,1)=白  (1,1)=黑  (2,1)=白 ...
```

## 世界坐标 vs 物体坐标

和 [[planar-mapping|平面映射]] 一样，选哪个坐标系决定了图案的行为：

- **世界坐标** `mul(unity_ObjectToWorld, v.vertex).xyz`：图案钉在世界上，物体移动/旋转时贴图保持不动——适合地板、棋盘桌面。
- **物体坐标** `v.vertex.xyz`：图案跟着物体走。

## 缩放、着色、扩展

`_Scale` 在 `floor` 之前做除法就能控制单元格大小（`_Scale < 1` 变密、`> 1` 变稀疏）。两个 `_EvenColor` / `_OddColor` 属性配合 `lerp(_Even, _Odd, c)` 就得到彩色棋盘——因为 `c` 只会是 0 或 1，`lerp` 在这里实际上是「二选一」的选择器，参见 [[shader-color-interpolation]]。

这个「`floor + frac*2` → 0/1 mask → `lerp` 取色」的套路可以推广成 **条纹**、**网格线**、**色块噪声**——所有周期性二值图案都能从这里出发。从表达能力上讲，棋盘是 [[worley-voronoi-noise|Voronoi]]、[[diamond-square-noise|diamond-square]] 这类更复杂程序化纹理的「Hello World」。

## 相关

- [[planar-mapping]] — 决定图案贴到世界还是贴到物体
- [[shader-color-interpolation]] — `lerp` 的数学
- [[coordinate-spaces]]
- [[worley-voronoi-noise]] — 下一级程序化图案
- [[fragment-shader]]

## Sources

- [[sources/ronja-checkerboard-pattern]]
