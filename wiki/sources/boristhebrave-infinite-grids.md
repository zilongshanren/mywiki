---
tags: [source, procedural-generation, infinite-world, sylves]
date: 2026-04-19
sources: 1
---

# Dealing With Infinite Grids（Boris The Brave）

[[boris-the-brave]] 发表于 2026 年 1 月的一篇指针式短文，宣布在 Sylves 的官方文档里新增了专门讨论**无限尺寸程序化生成**处理手法的一章，并注明这些技术对博客读者普遍有用，不限于 Sylves 用户。

## 摘要

博客正文本身只有一段，指向 Sylves 文档 `concepts/infinity.html`。它在知识库里的主要价值是把「无限网格上的程序化生成」这个**话题**正式立起来——和同系列的 [[poisson-rect-process]]、「Infinite Uniform Point Distributions」、「Infinite Modifying in Blocks」呼应，构成一组方法族：通过相位化（phase）+ 局部有界依赖，把全局约束降维成 chunk 可并行的规则。具体算法细节需要到 Sylves 文档查看，本条目作为入口记录。

## 关键要点

- 提示读者 Sylves 文档里有系统整理过的无限程序化生成方法论。
- 本站已就同一技术家族展开讨论，详见 [[infinite-chunked-procedural-generation]]。

## 链接到的概念

- [[infinite-chunked-procedural-generation]]
- [[poisson-rect-process]]

## 原文

- 链接：https://www.boristhebrave.com/2026/01/03/dealing-with-infinite-grids/
- 本地：`raw/articles/boristhebrave.com/2026-01-03_dealing-with-infinite-grids.md`
- Sylves 文档：https://www.boristhebrave.com/docs/sylves/1/articles/concepts/infinity.html
