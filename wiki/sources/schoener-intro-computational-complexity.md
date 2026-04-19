---
tags: [source, 复杂度理论, cs-theory, np-complete]
date: 2026-04-19
sources: 1
---

# A Short Introduction to Computational Complexity Theory（Sebastian Schöner）

[[sebastian-schoener]] 于 2016 年 10 月发表的入门短文，为随后一篇「Patterna 游戏的计算复杂度」做理论铺垫。

## 摘要

作者把「一个问题难不难」这件事，一步一步从直觉推向形式化。先把任意函数通过「判定问题（decision problem）」简化成 0/1 输出，然后用「算法所需步数随输入规模增长的函数」定义**时间复杂度**。以多项式时间 $n^k$ 作为「高效可解」的分界，由此引出两大类别：$\P$ 是所有高效可解的判定问题；$\NP$ 是**答案为 yes 的情况下可以在多项式时间内验证证据**的判定问题。Clique、TravelingSalesPerson 是 $\NP$ 里经典但暂无多项式算法的例子。$\P \subseteq \NP$ 显然成立，但 $\P = \NP$ 是否成立仍是未解之谜——要证 $\P \neq \NP$ 等于要给出某个问题的「下界对所有算法都成立」，极难。作为比较难度的工具，作者引入**多项式时间归约**：若 $L$ 能高效归约到 $M$，则 $M$ 高效可解意味着 $L$ 也高效可解。$\NP$-hard 表示 $\NP$ 中所有问题都能归约到它；既 $\NP$-hard 又在 $\NP$ 内的问题叫 $\NP$-complete（Clique、IndependentSet、TSP 都是）。证明一个问题 $\NP$-complete 被视为它**几乎不可能有多项式算法**的强证据。

## 关键要点

- 从「计算一个函数」→「判定问题（yes/no）」的简化路径
- 时间复杂度的定义必须以**输入编码的比特数**为基准，否则 pseudo-polynomial 陷阱会让人误判
- 多项式即「高效」是业界惯例，但 $n^{20}$ 并不真的高效——这是抽象选择的代价
- $\P = \NP$ 等价于「找答案和验答案一样难」，绝大多数研究者倾向不等
- 归约是比较问题难度的核心工具，把绝对下界替换成相对下界
- 证 $\NP$-complete 的常见套路：先证在 $\NP$ 里（给验证器），再从一个已知 $\NP$-complete 问题归约过来

## 链接到的概念

- [[computational-complexity-theory-intro]]
- [[order-of-growth]]
- [[probabilistic-algorithms]]

## 原文

- 链接：https://blog.s-schoener.com/2016-10-03-intro-to-computational-complexity/
- 本地：`raw/articles/blog.s-schoener.com/2016-10-03_a-short-introduction-to-computational-complexity-theory-seba.md`
