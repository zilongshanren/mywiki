---
tags: [source, bitsquid, 场景图, data-oriented, 引擎架构]
date: 2026-04-19
sources: 1
---

# Practical Examples in Data Oriented Design（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 5 月的一篇 post——正文其实是一段 SIGGRAPH 风格 slideshare 的嵌入（本地抓取下来只剩 HTML 评论区），真正可读的技术内容全在 Frykholm 对评论提问的回复里。核心讨论是"data-oriented 场景图怎么做增删"。

## 摘要

读者问：如果场景图用数组排布，删一个节点是不是要把后面所有节点左移，很慢吧？而且 mesh 引用的 node index 也要跟着改，是不是要改 `remove_node` 去遍历所有 mesh 修 index？Frykholm 的回答把前提直接换掉：Bitsquid 的**场景图不覆盖整个场景，只覆盖一个 entity 内部**，所以增删节点本来就不常发生。添加通常是 append 到数组末尾；删除可以不做（留着也没事）；只有 relinking（改父子关系）才需要数组重排，而这又是"你不会把手挪到肩膀前面"那种罕见事。不是优化 `remove_node`，是让 `remove_node` 很少被调。

## 关键要点

- **场景图粒度**：Bitsquid 的场景图**只在 entity 内部**，不是全局大树；
- entity 内部节点数小、结构稳定，增删不是 hot path；
- **add as leaf**：append 到数组末尾，O(1)；
- **remove**：不做也行，entity 销毁时整个数组一起释放；
- **relink**：真要改父子关系确实需要移位，**但极少发生**，用慢路径处理；
- 这是典型的"把问题 reframe 掉"而不是"优化一个不存在的瓶颈"。

## 链接到的概念

- [[per-entity-scene-graph]]
- [[scene-graph-matrix-stack-visitor]]
- [[data-driven-architecture]]
- [[ecs-data-oriented-revert]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/05/practical-examples-in-data-oriented.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-05-28_practical-examples-in-data-oriented-design.md`
