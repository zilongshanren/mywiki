---
tags: [source, 压缩, 几何, 索引缓冲, 网格]
date: 2026-04-27
sources: 1
---

# How to Compress an Index Buffer（Jon Olick）

[[jon-olick]] 发表于 2021 年 1 月的文章，详细讲解其 2007-2008 年演讲中提出的索引缓冲无损压缩技术。

## 摘要

索引缓冲中相邻三角形通常共享大量顶点，triangle strip/fan 优化器会进一步加剧这种重复性。文章提出一个四阶段压缩管线：首先用 cache-coherency 优化器排序并按顺序重排顶点缓冲；其次用 2-bit repeat table 编码每个三角形相对前一个三角形的两个重复索引（四种模式，第四种为逃逸），将大多数新索引从 3 个缩减为 1 个；再用 1-bit sequential table 标记是否连续递增，进一步消除顺序索引；最后对剩余"混沌索引"做 delta 编码 + 正值偏移。最终数据可直接定宽打包，或交由 Kraken/zip 做熵编码（后者压缩比更高但解压开销更大）。

## 关键要点

- 前提：cache-coherency 优化器质量直接决定压缩效果
- 2-bit repeat table：四种相邻三角形重复模式 + 逃逸
- 1-bit sequential table：利用重排后顶点下标递增的特性
- delta encode + min shift：将混沌索引差值归零后打包
- 可选 Kraken/zip 进行最终熵编码；高字节几乎全零时建议分离存储
- 解码是编码的逆序操作，文章留为读者练习

## 链接到的概念

- [[index-buffer-compression]]
- [[triangle-strips-vs-indexed-triangles]]
- [[meshoptimizer-vertex-codec]]

## 原文

- 链接：https://www.jonolick.com/home/how-to-compress-an-index-buffer
- 本地：`raw/articles/jonolick.com/2021-01-26_how-to-compress-an-index-buffer.md`
