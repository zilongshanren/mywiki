---
tags: [procedural-generation, tileset, autotile, game-development, classification]
date: 2026-04-27
sources: 2
---

# 瓦片集形式化分类框架

瓦片集分类框架由 Boris The Brave 提出，旨在为各类自动切片方案建立统一的「短代码」描述语言，使不同方案之间可以直接比较，并系统性地探索设计空间。

## 四维代码体系

每个瓦片集可以用四个维度的组合来描述：

**单元类型（Cell type）** 标识网格拓扑，代码为 S（方格）、C（立方体）、H（六边形）、T（三角形）。这决定了每个单元有几个邻居、每个顶点/边对应几个单元。

**瓦片识别方式（Tile identification）** 是最核心的维度，回答「唯一标识一张瓦片最少需要在哪些部位存储多少种不同的值？」。可以在顶点（V）、边（E）、面（F，仅 3D）或单元本身（C）上存值，后跟取值数量。例如 V2 表示每个顶点存一个二值布尔；E3 表示每条边存一个三值枚举；多个部位可叠加，如 V2E2 表示顶点和边都各有二值。

**对称性（Symmetry）** 表示美术师允许的旋转（R）与镜像（M）操作，可附加轴向修饰符。引入对称性可大幅减少需要绘制的瓦片数量——例如 S-V2 需要 16 片，而 S-V2-RM 只需 6 片。

**限制条件（Restrictions）** 描述哪些值组合是非法的（对应不存在的瓦片）。最常见的是 `-Blob`：Blob 模式要求「如果一个角的两条相邻边都为空，则该角也必须为空」。这类限制减少了必要瓦片数量，但需要自动切片系统正确处理不合法的查表结果。

## 常见瓦片集的代码

| 常见名称 | 代码 | 瓦片数（无对称）| 瓦片数（带 RM）|
|---------|------|-------------|-------------|
| Marching Squares | S-V2 | 16 | 6 |
| Blob | S-V2E2-Blob | 47 | 16 |
| Wang Tiles（2 色） | S-E2 | 16 | — |
| Minecraft 方块 | C-C*n* | n | — |
| 三角格 Marching | T-V2 | 16 | 4 |

## 框架的意义

相同分类代码的瓦片集视觉风格可以截然不同——CR31 的 Blob Gallery 展示了同一套 S-V2E2-Blob 既可以画成沟渠、也可以画成城墙或水面。分类代码捕捉的是信息结构，而非美术表达。

框架的另一个价值是**发现新方案**：将 Blob 的分类应用到三角网格或六边形网格，可以机械地推导出新瓦片集；改变对称性假设可以探索介于 Marching Squares 和 Blob 之间的中间方案。

这与[[game-development/autotile-tileset-layouts]]的关系是：autotile-tileset-layouts 侧重于具体方案的美术量和视觉效果对比，而分类框架提供了跨方案比较的形式化语言。两者互补。

## Sources

- [[sources/boris-classification-of-tilesets]]
- [[sources/boris-beyond-basic-autotiling]]
