---
tags: [source, 程序化纹理, 噪声, 优化]
date: 2026-04-14
sources: 1
---

# How to generate cellular textures 2（Fabian Giesen）

[[fabian-giesen|ryg]] 2010 年 3 月 29 日的续篇，给上一篇文章的 tiles 算法修了一个距离下界 bug，并且真的写出了对 all-nearest-neighbors 结构的空间递归细分算法——比所有之前的方案再快 3–5×。

## 摘要

第一个发现是尴尬的：tiles 版本的 `distanceBound` 从 Werkkzeug3 抄过来带了一个 bug，让下界估得过大，剪枝失效。修正版以后单纯的 tiles SSE 已经比 sort-by-y SSE 快 1.5–2×。但真正的突破是把 **像素网格结构** 用起来：对输出图像做 quadtree 风格递归细分——从整图开始分成 4 个子矩形 `S`。对每个 `S`，算一个「扩展矩形」`S'`：以 `S` 为中心、边长为 `S` 的三倍。ryg 的关键观察是：**如果 `S` 内至少有两个散点，那么所有可能成为 `S` 内某像素最近两点的候选点都必然落在 `S'` 内**。把 `S'` 外的点永久丢掉后继续递归，直到矩形足够小再回落到 tiles 算法实际着色。没有显式树、没有动态分配，全用调用栈完成。1024 点 / 1024×1024 图像下的实测只需 41ms，几乎和 64 点持平——因为剪枝把点集规模问题彻底摊平了。

## 关键要点

- **扩展矩形 3× 结论的推导**：设 `S` 内有一点 `C`、任意像素 `P ∈ S`。若另一点 `D` 比 `C` 更近 `P`，则 `|PD| < |PC| ≤ diam(S)`；因此 `D` 到 `S` 的距离小于 `diam(S)`，即 `D` 必在 `S` 的 `diam(S)` 扩展内。对最近两点成立同理。
- **空间递归细分几乎对点数不敏感**：64 点 22ms、1024 点 41ms；tree 版同等条件要 5.6 秒。对于大量 cell 的纹理，spatial subd 把算法复杂度近似推到 `O(|G|)` 而非 `O(|G| log |C|)`。
- **与 metaballs 等值面的联系**：评论区有 Casey / Chris Hecker 的老同事指出，Definition Six 时代的 metaball 等值面提取也是按空间八叉树递归 + 距离下界剔除的，思路同构。
- **代码量**：spatial subd 版本含 KeyedPoint 辅助共 138 行，还比 tree 的 185 行短。
- **元教训**：`Keep it simple, stupid! Look at the problem you're trying to solve. And don't just use trees for everything :)`——文章结尾两句被大量转引。

## 链接到的概念

- [[cellular-texture-generation]]
- [[worley-voronoi-noise]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/03/29/how-to-generate-cellular-textures-2/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-03-29_how-to-generate-cellular-textures-2.md`
