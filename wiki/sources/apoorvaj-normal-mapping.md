---
tags: [source, 渲染, 法线贴图, 视差贴图]
date: 2026-04-14
sources: 1
---

# Normal Mapping（Apoorva Joshi / apoorvaj.io）

[[apoorva-joshi|Apoorva Joshi]] 2017 年 3 月发表的一篇带 WebGL demo 的凹凸贴图教程。文章实现了一个可交互的旋转立方体，让读者在 normal mapping、parallax mapping、steep parallax 和 parallax occlusion mapping 之间切换并调参。

## 摘要

文章先定义凹凸贴图作为「中尺度细节」的统称——既不大到要做几何、又不小到能被 BRDF 隐含——再把焦点缩到四种**不修改几何**的方案。法线贴图部分用大量篇幅推切线空间：法线为什么不能存在世界空间（旋转 / mesh 共享会失效），怎么用每顶点的 T、B 加 N 构造 TBN 矩阵，怎么用矩阵 / 转置在切线空间和世界空间之间换基，以及为什么把光位置和相机位置在 vertex shader 里搬到切线空间比在 fragment shader 里把法线搬到世界空间更便宜。然后是视差家族：simple parallax 用一阶近似 $\Delta uv = h\,v_{xy}/v_z$；steep parallax 把深度切层、沿 view ray 线性搜索；POM 在交点前后做插值修正 steep 的台阶状 artefact。文末给出完整 vertex / fragment shader 源码，配三张贴图（diffuse / normal / depth）来自 learnopengl.com。

## 关键要点

- Bump mapping 是一族技术的统称；displacement mapping 不在内（那一类要改几何）。
- 法线贴图必须用切线空间，否则 mesh 旋转或共享时贴图都会失效。
- TBN 由 T = ∂p/∂u、B = ∂p/∂v、N = T×B 构成，正交时**逆 = 转置**。
- 光照空间选择：把 vector 从世界空间搬到切线空间通常更便宜，因为只发生在 vertex shader。
- Simple parallax / steep parallax / POM 是同一思路下精度递增的三步：闭式近似 → 离散搜索 → 离散搜索 + 段间插值。
- POM 假定相邻深度层之间高度场可被线性近似，所以步数必须够大。

## 链接到的概念

- [[tangent-space-normal-mapping]]
- [[normal-map-blending]]
- [[tangent-free-normal-mapping]]
- [[coordinate-spaces]]
- [[apoorva-joshi]]

## 原文

- 链接：<https://apoorvaj.io/exploring-bump-mapping-with-webgl>
- 本地：`raw/articles/apoorvaj.io/2017-03-04_normal-mapping.md`
