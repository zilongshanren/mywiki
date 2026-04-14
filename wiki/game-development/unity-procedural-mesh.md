---
tags: [unity, 程序化几何, mesh, 入门]
date: 2026-04-14
sources: 1
---

# Unity 程序化 Mesh 构造

Unity `Mesh` API 的最小契约：给它一个 `Vector3[] vertices`（顶点坐标列表）和一个 `int[] triangles`（顶点索引列表，每 3 个为一组构成一个三角形），再调 `RecalculateNormals` 算法线，就能从零生成几何体。Linden Reid 的 *Intro to Procedural Geometry Part 2* 用一个 2×2×2 cube 把这套流程讲透。

## 顶点布局

- cube 有 8 个角顶点，居中在原点时每个分量就是 ±1。
- `vertices` 数组里的**顺序无所谓**，但顺序决定了"索引号"，三角形只能通过索引引用顶点。
- 比 cube 更复杂的是共享顶点问题：几何上一个角有 3 个面相遇，但因为每个面需要**不同的法线和 UV**，实际上通常需要拆成 3 个不同的顶点（同位置但不同属性）。Reid 的教程先忽略这点，直接用共享顶点 + `RecalculateNormals`，所以得到的是"每顶点平均法线"而不是硬边。

## 三角形索引与 winding order

`triangles` 数组长度必须是 3 的倍数。cube 的 6 面 × 每面 2 三角 × 每三角 3 顶点 = **36**。

Unity（以及大多数现代图形 API 的默认状态）使用**顺时针 winding order** 来判定"正面"：

- 从你希望**可见的那一面**看过去，三个顶点顺序是顺时针 → 正面。
- 顺序写错了，三角形会被 [[culling|背面剔除]] 掉，出现"面缺了"的现象。

这意味着立方体的 6 个面不能盲目复制粘贴索引——每个面要根据**观察方向**重新判断 winding。实操里有个手动技巧：对每个面画张小图，标出希望看到的那一侧，再顺时针列顶点。

## 与 shader 阶段的关系

构造 mesh 只是到 [[rendering-pipeline|rendering pipeline]] 的入口：Unity 会把 `mesh.vertices` 作为 vertex buffer 上传，把 `mesh.triangles` 作为 index buffer 上传，后续由 [[triangle-setup]] 和 [[rasterization]] 处理。新手经常忽略的一件事是：**程序化 mesh 并不比导入的 FBX 便宜**——它们在 GPU 眼里完全是同一种东西，区别只在 CPU 侧谁在填 buffer。

## 教程没讲但很重要的坑

- **没有法线的 mesh 会漆黑一片**：必须调 `RecalculateNormals` 或手写法线，否则光照全 0。
- **没有 UV 的 mesh 无法贴图**：`RecalculateNormals` 不生成 UV。
- **频繁重建 mesh 很慢**：Reid 的教程每帧 `new Mesh()` 只是演示，生产环境要复用对象并用 `Mesh.SetVertices` / `SetTriangles`。
- **硬边/软边取决于是否共享顶点**：`RecalculateNormals` 对共享顶点会取平均，得到软边；需要硬边就必须把共享顶点拆开。

## 相关

- [[rendering-pipeline]]
- [[triangle-primitives]]
- [[triangle-setup]]
- [[culling]]
- [[compact-vertex-format]]
- [[greedy-voxel-meshing]] —— 运行时程序化 mesh 的另一个常见场景
- [[linden-reid]]

## Sources

- [[sources/lindenreid-procedural-geometry-part2]]
