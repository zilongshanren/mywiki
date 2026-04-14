---
tags: [渲染, 光栅化, GPU]
date: 2026-04-14
sources: 1
---

# Triangle Setup

[[pineda-edge-rasterization|Pineda 边方程算法]] 把光栅化变成了「每像素一次整数加法」——但这个加法的 **a/b/c** 系数从哪里来？答案是 **triangle setup**：在 [[rasterization|光栅化]] 真正开始之前，硬件用每个三角形顶点的屏幕坐标算出三条边方程 `aᵢ·x + bᵢ·y + cᵢ` 以及一些预置的步进、参考值。

## 它的输入

来自前一阶段（geometry processing 之后、viewport transform 之后）：三个顶点的 **fixed-point 子像素屏幕坐标**。snap 到栅格这一步本身不在 triangle setup 里，但 setup 依赖它的结果——只有在整数坐标下，后面的 Pineda 算法才能保证位级精确、watertight。

## 它产出的东西

1. **三条边方程的 `(a, b, c)`**——每条从两个相邻顶点的差直接算出，需要几次较大的整数乘法。
2. **每个 8×8 tile 步进时的 `Δ`**——`a · 8`、`b · 8` 等。这些其实就是上面的小常量乘法。
3. **「reference corner」**——根据 `a, b` 的符号，决定 [[hierarchical-rasterization|coarse rast]] 算 tile 上下界时该用 4 个角中的哪一个。
4. **第一个参考 tile 的 `Eᵢ` 初值**——为前面的 reference corner 算出来，已经把 [[fill-rule|top-left 填充规则]]里的 `−1` 修正包含进去，coarse rast 一接手就能直接用。
5. **要插值的属性的常数项**——Z、1/W、shading attribute 等（这部分 ryg 留给后续帖子讲）。

## 硬件代价

总的来说就是「几次大整数乘法 + 几次小整数乘法 + 一些组合逻辑」。乘法可以用 [[carry-save-adder|carry-save adder（3:2 reducer）]] 把多项加法合并，再用一次普通加法收尾——典型的硬件优化。和 vertex shader 的浮点开销比，setup 的成本几乎可以忽略；和 pixel shader 的开销比则更不值一提。

## 但它会成为小三角形的瓶颈

虽然单 setup 便宜，但是**每个三角形固定一次**：当三角形非常小（覆盖 0–1 个像素）、数量又非常多（典型场景：远处的细发丝、过度细分的 LOD），整个管线很容易卡在「triangle setup 或 coarse rasterization」上，而 pixel shader 反而吃不饱。Nanite 这一类基于软件光栅化的方案，相当大一部分动机就是**绕开硬件 triangle setup 在小三角形时的固定开销**。

## 与 attribute setup 的区别

注意 ryg 在原文里只讲了「rasterization 用的 setup」。还有另一类 setup 是为 **属性插值**（Z、color、UV）服务的——它和 [[perspective-correct-interpolation|透视校正插值]] 紧密相关，需要的是 1/W 项的预除和重心坐标的常数项。两者都叫 setup，但走的是不同的硬件单元。

## 相关

- [[pineda-edge-rasterization]]
- [[hierarchical-rasterization]]
- [[rasterization]]
- [[rendering-pipeline]]
- [[perspective-correct-interpolation]]
- [[fabian-giesen]]
- [[homogeneous-rasterization-transpose-bug]] — 齐次坐标 setup 矩阵的转置陷阱

## Sources

- [[sources/ryg-trip-through-graphics-pipeline-2011-part-6]]
