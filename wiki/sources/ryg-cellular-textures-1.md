---
tags: [source, 程序化纹理, 噪声, 优化]
date: 2026-04-14
sources: 1
---

# How to generate cellular textures（Fabian Giesen）

[[fabian-giesen|Fabian "ryg" Giesen]] 2010 年 3 月 28 日的长文，记录了他在 Werkkzeug3（Farbrausch 的 demoscene 纹理生成器）里对[[worley-voronoi-noise|Worley / 细胞纹理]]生成算法的多年迭代，同时用实测数据打脸了 Jim Scott 最早推广的「用 tree 来加速」思路。

## 摘要

离线细胞纹理生成的真正问题是 _all-nearest-neighbors_：在规则的像素网格 `G` 上，对每个像素找到散点集 `C` 里最近的两个点。教材直觉是把 `C` 塞进 kd-tree，为每个像素下降一次；但这条路径忽略了**查询端本身是有结构的**——相邻像素的最近邻差异极小，每次从头走树完全浪费。ryg 对比了四种非树算法：brute force、sort-by-y（每扫描线把点按 y-距离插入排序，距离超过 best2 时中断）、tiles（按 32×32 像素分块、算点到 tile 的下界作排序 key）、以及 SSE 版本。在 1024×1024 / 64–512 点 / Core 2 Duo 2.2GHz 的实测下，sort-by-y 已经比暴力法快 5×、比 tree 快 10×，tiles SSE 版比 tree 快 50–80×。代码量也远小——tree 版 185 行，sort-by-y 只有 60 行。顺便给出一条着色配方 `(d2 - d1) / (d2 + d1)` 避免远离散点 cell 的整体变暗。

## 关键要点

- **用树反而最慢**：对点集做空间索引忽略了像素网格的规则性；每个像素独立下降一次树，cache miss 和冗余工作压过任何剪枝收益。
- **sort-by-y 几乎免费**：相邻行点集顺序变化极小，插入排序接近 O(n)；一旦 `best2 < dy²` 整行尾部直接剪掉。四像素并行时也不会像 tree 那样分岔。
- **tiles 对称处理 x/y**：sort-by-y 只能用 y 剪枝；切块 + 距离下界能同时剪 x 和 y，也更适配非均匀距离权重（Werkkzeug3 允许各向异性距离）。
- **配色 trick**：`(dist2 - dist1) / (dist1 + dist2) = 1 - 2·dist1/(dist1+dist2)` 避免整体亮度随 cell 尺寸剧变，比纯 `d2 - d1` 漂亮。
- ryg 在 update 里直接承认这些算法仍只是「单向对称」优化，真正对称的 _all-NN_ 算法他还没实现——为第二篇文章留下钩子。

## 链接到的概念

- [[cellular-texture-generation]]
- [[worley-voronoi-noise]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/03/28/how-to-generate-cellular-textures/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-03-28_how-to-generate-cellular-textures.md`
