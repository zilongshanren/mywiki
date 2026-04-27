---
tags: [hex-grid, math, procedural-generation, game-development, grid]
date: 2026-04-27
sources: 1
---

# 六边形绕回网格（Wraparound Hex Grid）

六边形绕回网格是一个有限的六边形单元格集合，其整体形状也是六边形，且具有环面拓扑：从任意一侧越过边界会从对面重新进入，类似于方形网格的圆环面推广到六边形坐标系。这一数学主题在 RedBlobGames 的六边形参考文档中尚未覆盖，由 [[people/boris-the-brave]] 通过 Sylves 库的实现需求独立推导。

## 数学原理

基础思路是将无限六边形平面划分为等尺寸的六边形"大块（chunk）"，再计算每个大块到中心块的平移偏移量。任意坐标通过这一映射折叠回中心块内的等价坐标，从而实现绕回。

使用轴坐标系（cube coordinates，满足 x+y+z=0）时，半径为 r 的绕回网格的关键参数：

```
shift = 3*r + 2
area  = r * shift + r + 1   // 即 3r²+3r+1 个单元格
```

计算步骤：
1. 用 Sander Evers 的公式确定坐标 (x,y,z) 所在的大块 (xh,yh,zh)
2. 从大块坐标推算整数偏移量 (i,j)：`i = floor((1+xh-yh)/3)`, `j = floor((1+yh-zh)/3)`
3. 平移回中心：`x -= (2r+1)*i + r*j`，`y -= -r*i + (r+1)*j`，`z = -x-y`

完整 Python 实现约 20 行，Boris 以「感觉不够优雅」的态度发布，欢迎更简洁的替代方案。

## 实现背景

该功能作为 Sylves（[[people/boris-the-brave]] 维护的 .NET 几何/网格库）的 `WrappingHexGrid` 类实现。用户请求此功能是触发推导的直接原因。六边形切片分块的数学来自 Sander Evers 的 Observable notebook，Boris 的贡献是将分块映射与绕回坐标折叠组合为完整算法。

## 与其他网格概念的关系

- 方形网格的绕回（toroidal）版本实现简单，模运算即可，六边形因坐标系的倾斜性而复杂得多
- [[game-development/triangle-grid]] 和 [[game-development/rotation-graphs]] 是 Sylves 覆盖的其他非标网格形态
- 六边形坐标系（cube/axial/offset coordinates）的基础可参考 RedBlobGames 的教程

## Sources

- [[sources/boris-wraparound-hex-grids]]
