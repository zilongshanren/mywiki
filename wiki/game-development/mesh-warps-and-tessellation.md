---
tags: [程序化几何, mesh, tessellation, limit-theory, 算法]
date: 2026-04-14
sources: 3
---

# Mesh 变形与细分：stellation、extrusion、triangulation

[[linden-reid]] 2017 年 Limit Theory 教程的另一条线：**给定一个已经存在的 mesh，怎样在 CPU 侧对它做"有趣的"几何变换**。这些操作有两类：

1. **Warp（变形）**——在每个三角形上做手术，添加新的几何细节（stellation、extrusion）。
2. **Subdivision / triangulation（细分与三角化）**——在不改变形状的前提下增加多边形数量，或把高次多边形化成三角形（fan、centroid、triforce）。

两类操作是组合拳：先 tessellate 得到更密的三角形网，再 warp 才会看起来"丰富"；先把 n 边形 triangulate 成三角形，才能喂给假设输入全是三角形的 warp。[[procedural-mesh-primitives|程序化基元]] 提供原材料，这里的算法把原材料打成成品。

## Stellation：把三角形拱成金字塔

Stellation 的字面意思与 "star"（星）同源——对每个三角形拉出一个尖，整个 mesh 就变成多面星体。单个三角形的算法干净到不能再干净：

1. **重心**：`center = (v1 + v2 + v3) / 3`
2. **法线**：`normal = normalize(cross(v2 - v1, v3 - v2))`（注意对退化三角形要检查法线长度 > 0，否则会除零）
3. **新顶点**：`v4 = center + normal · h`，其中 `h` 是拉伸距离
4. **新三角形**：原三角形的三条边 × 新顶点 = 3 个新三角形，**原三角形本身被丢弃**（会被新的侧面盖住）

应用到整个 mesh 时要注意索引记账——先把所有旧顶点按原顺序塞进新 mesh，然后对每个旧三角形生成一个新顶点，索引就是 `vi = oldVertexCount + i`。重复 stellate 同一个 mesh 会得到越来越尖锐的分形星。

## Extrusion：把三角形拱成三棱柱

Extrusion 是 stellation 的"平移版"——不收束到一个点，而是把整个三角形沿法线推出去，产生一个三棱柱。区别主要在顶点数和拓扑：

- 新顶点 **3 个**：`v4 = v1 + n·h, v5 = v2 + n·h, v6 = v3 + n·h`
- 新三角形 **7 个**：顶面 1 + 三个侧面 × 2 = 7（顶面 1 个三角形、三条边各 2 个组成的 quad，各贡献 2 个三角形）

整个 mesh 循环时，每次迭代要把顶点索引计数器增加 3 而不是 stellation 的 1。Winding order 仍然要注意——Reid 默认 counter-clockwise，侧面三角形的顶点顺序必须对应。

## Triangulation：把 n 边形拆成三角形

渲染管线的三角形设置阶段（参见 [[triangle-setup]]）本质上只吃三角形，所以 mesh 数据结构如果允许高次多边形（Reid 的 Limit Theory 里是这样），在送给 GPU 之前必须先 triangulate。Reid 给了三个算法，**名字是她自己起的，不是教科书术语**——这是一个"审美实用派"的分类，不是计算几何的分类。

### Fan（扇形三角化）

最便宜：不加新顶点，从第一个顶点出发扇形地拉向其余每对相邻顶点。一个 5 边形 `[p0, p1, p2, p3, p4]` 拆成 `(p0, p1, p2)`, `(p0, p2, p3)`, `(p0, p3, p4)`。优点是**零额外顶点，零额外数据**——这是最后一步交给 renderer 时的理想选择。缺点是"基点"附近角度非常小、非常畸形，如果后续还要 warp，会得到难看的尖角。

### Centroid（质心三角化）

更"圆润"的拆法：在多边形中心（顶点位置平均值）加一个新顶点，然后从这个中心向每条边的两个端点连线，得到 n 个三角形。单个 5 边形变成 5 个三角形，顶点数 +1。角度比 fan 均匀很多，后续 warp 出来的结果也更可控。Limit Theory 在做"先 triangulate 再 extrude 整面"时用的就是这个——扇形 triangulation 后再 extrude 会得到一个所有尖都指向基点的畸形蘑菇，centroid 则是一个规整的金字塔。

### Triforce（Triforce 细分）

这是唯一一个**只在三角形上起作用**的算法，也是唯一一个 Reid 称之为 "tessellation" 的——因为它对等边三角形产生**正规镶嵌**（所有新三角形都是相似的等边三角形），对非等边三角形也**保角**。做法是：对每条边取中点 → 得到 3 个新顶点 → 连接 3 个中点把原三角形切成 4 个小三角形（3 个角上的 + 1 个中间反向的）。这就是塞尔达三力同形的样子。

实现关键是**去重**：相邻三角形共享边，共享边的中点必须是同一个顶点。Reid 用一个 `edgeMap`（以边的两个端点索引的最小值·顶点数 + 最大值为 key）来记录已经创建的边中点，避免重复。

这个算法是"加密"一个 mesh 最好的选择——几次 triforce 之后三角形数量按 4× 增长，但形状保持，是后续做 per-face warp（stellation、extrusion、displacement）的理想预处理。

## 组合使用的典型流程

Reid 在文章里反复示范的 pipeline 是：

1. 用 [[procedural-mesh-primitives|参数化基元]] 生成一个简单 mesh（cube、icosahedron、torus…）
2. 如果多边形不全是三角形，先跑 **centroid triangulation**（保角度比 fan 好）
3. 跑几轮 **triforce tessellation** 加密
4. 对每个三角形做 **stellation** 或 **extrusion**
5. 可选：再跑一轮 triforce → 再 warp，递归做出"多级分形星体"

Limit Theory 的程序化飞船和空间站就是这样逐层堆出来的。这套做法都在 CPU 侧、离线完成，对比 GPU 侧的 [[draw-procedural-gpu]] 或 compute-based 的 displacement 是两种正交的技术路线——前者得到真正的 mesh 数据（可以导出、可以打碰撞盒），后者只在 draw 时临时计算。

## 注意点与坑

- **Winding order** 决定正反面。Reid 全部使用 CCW，如果你的引擎是 CW 要全面翻转。
- **法线重算**。warp 之后顶点位置变了，原有的顶点法线完全失效，必须重算或让 [[unity-procedural-mesh|RecalculateNormals]] 接手。
- **接缝重复顶点**。像圆环那样有重复顶点的 mesh 做 triforce 时，`edgeMap` 的 key 可能会落到同一条"逻辑边"上——这是一个实际代码里要小心的陷阱，文章没讨论。
- **退化三角形**。stellation 对零面积三角形计算出的法线是 `(0,0,0)`，要么在入口过滤，要么容错。

## 相关

- [[procedural-mesh-primitives]]
- [[unity-procedural-mesh]]
- [[triangle-primitives]]
- [[triangle-setup]]
- [[linden-reid]]

## Sources

- [[sources/lindenreid-procedural-stellation]]
- [[sources/lindenreid-procedural-extrusion]]
- [[sources/lindenreid-mesh-tessellation-triangulation]]
