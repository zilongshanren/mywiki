---
tags: [source, opengl, mesh, draw-call]
date: 2026-04-19
sources: 1
---

# To Strip or Not To Strip（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 1 月解释为什么性能优先的桌面 OpenGL 应用 X-Plane **不用** triangle strip。针对的是社区里新手查教程看到「strip 最快」、老手却都在说「indexed triangles 更好」、两边都不展开推导的困惑。

## 摘要

在纯 `glDrawArrays` 时代 strip 的卖点是：一条长 N 的带子只需 `N+2` 个顶点，远少于独立三角形的 `3N`，在几何受限时是 3× 胜利。但索引化（`glDrawElements`）引入后格局翻转：X-Plane 的 vertex 是 32 字节、index 是 4 字节，顶点比索引贵 8 倍，只要共享顶点占比 >1/8 索引就赚——对建模师做的 mesh 这几乎一定成立。一旦用了索引，strip 的 3× 压缩只作用在**索引列表**上，在 32:4 比例下只有原来收益的 1/8。更糟的是 strip 在真实 mesh 里往往很短，要么对每条 strip 独立 `glDrawElements`（CPU call 暴涨），要么依赖 `glMultiDrawElements`（驱动可能偷偷拆回）或 `NV_primitive_restart`（早年仅 NVidia，每次 restart 还要占一个索引）。结论：**为了压缩已经放在 VRAM 的 index buffer 而增加 CPU 调用，是方向搞反**。X-Plane 的方案是每块 mesh 一次 `glDrawElements` 画完，代码只处理一种情况。例外要认清——`GL_POINTS`、X-Plane 的「树」（每株独立 quad 无共享）关闭索引；PowerVR MBX（iPhone 1 代 ES 1.1）tile-based renderer 按 strip 桶化几何，移动端 strip-order 索引仍值得做。评论区还补充了 degenerate triangle「跳变」技巧和 ATI 从 GL 3.1 起支持 primitive restart 的情况。

## 关键要点

- strip 的 vertex 压缩 3× 在未索引时是大胜，在索引化后只压索引列表
- X-Plane 比例 32:4，索引化后 strip 节省只剩原先的 1/8
- 短 strip 下 `glDrawElements` per-strip / `glMultiDrawElements` / `primitive_restart` 都有坑
- 反模式：用额外 CPU draw call 去压 VRAM 中的 index buffer
- 桌面默认策略：有共享顶点就走 indexed triangles + 一次 draw call
- 移动端例外：PowerVR MBX tile-based 仍需 strip-order 索引

## 链接到的概念

- [[triangle-strips-vs-indexed-triangles]]
- [[draw-call]]
- [[opengl-draw-call-batching-sweet-spot]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/01/to-strip-or-not-to-strip.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-01-31_to-strip-or-not-to-strip.md`
