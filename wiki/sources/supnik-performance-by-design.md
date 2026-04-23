---
tags: [source, performance, 方法论, knuth]
date: 2026-04-19
sources: 1
---

# High Performance Code Is Designed, Not Optimized（Ben Supnik）

[[ben-supnik]] 2015-01-04 发表，立场帖。

## 摘要

作者原本准备写一篇反驳"Knuth 的 premature optimization 被滥用"的长文，但 Joshua Barczak 已经先写了同题。于是他把自己的观点浓缩成一个口号：**High performance software is always high performance by design**。核心论点是性能不是后期 profile 调出来的——它是架构阶段就被决定的。他还给出一个反过来写的 Knuth 式俏皮话："Premature design without analyzing the performance characteristics of the problem is the root of all evil."。评论区对话进一步澄清：他不是反对 profile，也不是反对 hand tuning——他只是反对"用 profile + 局部 hand tuning 代替性能设计"。Hand tuning 本身有两种意义：按 profile 数据改内存布局，以及用汇编等劳动密集手段重写热点，两者都正当，都是必要补充。这篇是续篇 [[four-horsemen-performance]] 的立论起点。

## 关键要点

- 错引 Knuth 的代价：把"premature optimization"当"不要管性能"的借口
- 高性能软件的性能是**设计出来的**，后期救不回来
- Hand tuning 是设计的**补充**，不是替代
- profile + 优化是必要但不充分——没 profile 连代码是否正确都不知道

## 链接到的概念

- [[performance-by-design]]
- [[four-horsemen-performance]]
- [[strategic-programming]]
- [[pragmatic-performance-philosophy]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/01/high-performance-code-is-designed-not.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-01-04_high-performance-code-is-designed-not-optimized.md`
