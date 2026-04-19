---
tags: [source, 复杂度理论, cs-theory, game-design, np-complete, co-np]
date: 2026-04-19
sources: 1
---

# The Computational Complexity of Patterna（Sebastian Schöner）

[[sebastian-schoener]] 于 2016 年 10 月的续篇，把 $\P/\NP/\coNP$ 理论套在 Patterna（HexCells、Minesweeper 同类逻辑消除游戏）之上，纠正一个在玩家圈里流传已久的错误说法。

## 摘要

流行观点说「Minesweeper 是 $\NP$-complete」，所以 Patterna 也是。作者指出这里混了两件事：Richard Kaye 证的是 **Minesweeper Consistency Problem (MCP)**——给一块已标注的棋盘，问「是否存在一种摆法与所有约束一致」。用类似思路，把 **3CNF-SAT** 归约进去，可以轻松证明 Patterna 的一致性问题 **PatPC** 也是 $\NP$-complete。**但这和玩家实际做的事情无关**：玩家不是去找「一个可能的解」，而是**根据当前约束证明某个格子的状态被唯一确定**。这是完全不同的复杂度问题。作者把玩家真正解的问题定义为 **PatProg**——给一块一致的棋盘，是否存在某个未知节点的状态被当前约束唯一确定？其补集 **PatStuck** 明显在 $\NP$ 里（证据就是每个未知节点的两种可行赋值），因此 **PatProg** 在 $\coNP$ 里。随后作者通过 **3CNF-UNSAT**（$\coNP$-hard）向 **PatProg** 的归约证明其 $\coNP$-complete，用 OR gadget 构造电路，让最终输出节点的状态当且仅当公式不可满足时才能被推出。把整个关卡的可解性 **PatSolv** 也论证在 $\coNP$ 中。结论是：**从玩家视角讲这类游戏是 $\coNP$-hard，不是 $\NP$-hard**——这是两件 long-running 被误解的事。

## 关键要点

- **Consistency 问题** ≠ **Progress 问题**：一致性只需存在一个可行摆法（$\NP$），推理只需证明「所有可行摆法上该节点状态一致」（$\coNP$）
- 这是「找答案 vs. 排除所有反例」在问题层面的体现——Minesweeper 现实玩法本质是**排除**而非**构造**
- Scott/Stege/van Rooij 2011 对 Minesweeper 的纠偏论文就是同样结论（Minesweeper is $\coNP$-complete, not NP-complete）
- OR-gadget 构造：用「pattern 节点连通数」约束模拟逻辑门，DeMorgan 定律把 AND 转成 NOR
- 已知 pattern 节点总数这一约束必须显式建模，否则归约不成立
- 整个关卡的可解性 **PatSolv**：用「obstruction（阻塞扩展）」作证据证明其 $\coNP$-complete 仍有技术细节未完全闭合

## 链接到的概念

- [[patterna-hexcells-np-vs-conp]]
- [[computational-complexity-theory-intro]]

## 原文

- 链接：https://blog.s-schoener.com/2016-10-10-computational-complexity-patterna/
- 本地：`raw/articles/blog.s-schoener.com/2016-10-10_the-computational-complexity-of-patterna-sebastian-schoner.md`
