---
tags: [source, software-design, file-format, serialization]
date: 2026-04-27
sources: 1
---

# When Not To Serialize（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2018 年 8 月发表的文章，以 WorldEditor（X-Plane 场景编辑器）的真实教训为例，论证了一条容易被忽视的设计原则：把内存数据结构直接序列化为文件格式，是一种隐患极深的"偷懒"。

## 摘要

WorldEditor 的数据模型用父子树（thing 树）来表示多边形，边（edge）是隐式的——每对相邻顶点定义一条边。这在内存中工作良好，但"导致 edge 无法被选中"的 UI 问题迫使团队要引入显式 edge 对象。然而旧文件里没有 edge，加载旧文件时就必须从顶点还原——而旧文件格式本身就是旧数据结构的镜像，毫无为演化预留的空间。这是"把内存数据结构序列化为文件格式"的典型代价：内存模型一旦改变，读取旧文件的代价就是保留一套旧代码或为新数据模型添加"可选字段"的兼容模式，两条路都很丑陋。文章的核心论点是：把内存格式翻译成独立的文件格式是一个**特性**而非负担——翻译层让文件格式和内存格式能独立演化，各自针对"持久化"和"运行性能"两个不同目标分别优化。X-Plane 从 v9 迁移到 v10 时正是因为 v9 文件是结构体的 memcpy，才不得不保留一整套旧 C 结构体做中间层；改为 key-value 格式后，v10 以后的迁移就轻松多了。

## 关键要点

- 把内存数据结构直接序列化为文件格式，等价于把两者的演化绑定在一起
- 文件格式的设计目标是持久化（长期可读、向前兼容），内存格式的目标是运行性能（局部性、快速查找）；两者目标不同，不该是同一个东西
- 显式翻译层（内存 ↔ 文件）虽然要写更多代码，但让两端可以独立变化
- 序列化直接用于 undo 栈等生命期只在单次运行内的场景是可以的，不需要跨版本兼容
- "现在不写翻译层"只是推迟了代价，下个版本的翻译对象将是一个从未为可读性设计的格式

## 链接到的概念

- [[file-format-vs-data-model]]
- [[temporal-decomposition]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2018/08/when-not-to-serialize.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2018-08-08_when-not-to-serialize.md`
