---
tags: [source, 软件设计, yagni, x-plane]
date: 2026-04-19
sources: 1
---

# Is It Ever Okay to Future Proof?（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 的工程方法论笔记，讨论「为未来预留设计」在什么情况下不是浪费。

## 摘要

文章起于作者之前一篇「解领域特定问题、别解通用问题」的主张，读者反馈里一部分引用 YAGNI 完全同意，另一部分认为 YAGNI 被拿来当借口糊死技术债。作者提出三问测试：(1) 你是否**确知**未来那个特性会被商业需要？(2) 你是否**知道怎么用今天的代码高效实现**它？(3) 两个特性合并做的**总成本是否确实更低**？一条答不上就别 future-proof；全通过了还得看排期是否允许。关键认识是：写代码本身是学习过程——写完 A 才会真正了解 B 的约束，因此过早合并设计常常注定失败。作者用 X-Plane 粒子系统作正例（明确知道要扩展到场景，实现路径已知，二次改造成本小于单独做）说明测试通过时的 future-proofing 是合算的。

## 关键要点

- "YAGNI 是默认态，三问都通过才能打破"——给了一个可操作的判断流程。
- 代码本身承载了对问题空间的学习——Ousterhout [[strategic-programming|战略编程]] 的同源观察。
- 典型陷阱：大量预留 virtual hook、配置项、接口扩展点，其中绝大多数永远不会被用到。
- 要素：业务确认、实现路径清晰、总工程量可算。

## 链接到的概念

- [[future-proofing-tests]]
- [[cheat-by-solving-less]]
- [[strategic-programming]]
- [[tactical-programming]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2018/10/is-it-ever-okay-to-future-proof.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2021-10-16_is-it-ever-okay-to-future-proof.md`
