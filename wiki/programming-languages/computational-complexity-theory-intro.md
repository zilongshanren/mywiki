---
tags: [cs-theory, 复杂度理论, np-complete, p-vs-np]
date: 2026-04-19
sources: 1
---

# 计算复杂度理论入门（P/NP/归约）

**计算复杂度理论（Computational Complexity Theory）** 研究「一个问题本身有多难」，不是某个具体算法跑多快。它把算法分析的焦点从「实现细节」推到「问题内禀性质」。

## 从函数到判定问题

理论先把任意函数 $f: A \to B$ 的计算简化成**判定问题（decision problem）**：输出仅为 0/1、yes/no。这不失一般性——任何输出可以按位逐个判定问出来。常见的判定问题：

- **Sorted**：输入一个整数序列，问它是否有序
- **Clique**：给定社交网络和 $k$，问是否存在 $k$ 个两两互为朋友的人
- **TravelingSalesPerson**：给定城市距离和上界 $d$，问是否存在总长 $\leq d$ 的环游路线

## 时间复杂度与 $\P$

一个算法的 **runtime** 是它处理规模为 $n$ 的输入所需的基本步数（作为 $n$ 的函数）。问题的**时间复杂度**是能解它的所有算法中 runtime 的下确界。

**$\P$（polynomial time）** 是所有能在 $O(n^k)$ 时间内解决的判定问题。这是「高效可解」的操作定义，即便 $n^{20}$ 并不真的快——参考 [[order-of-growth]]。

## $\NP$ 与验证

**$\NP$（nondeterministic polynomial time）** 的直观定义：若输入 $x$ 是 yes-instance，则存在一个**多项式长度的证据**，可以在多项式时间内**验证**它确实是 yes。Clique 和 TSP 都在 $\NP$ 里——给你一个团或一条路，你能快速验证其合法性，但自己找却似乎很慢。

显然 $\P \subseteq \NP$（算法运行痕迹本身就是证据）。**$\P = \NP$ 是否成立**是千禧年七大难题之一，等价于问：**找答案和验答案一样难吗？** 大多数研究者相信 $\P \neq \NP$，但没人证出来。

## $\coNP$：被忽略的另一半

**$\coNP$** 是补集在 $\NP$ 中的所有问题。注意 $\coNP$ **不是** $\NP$ 的补集——它是「no-instance 有短证据」的那类问题。举例：

- 「公式 $\varphi$ 是否可满足」在 $\NP$ 里（找到一个赋值即可验证）
- 「公式 $\varphi$ 是否**不**可满足」在 $\coNP$ 里（反证：一旦有任一满足赋值就推翻）

这个区分在 [[patterna-hexcells-np-vs-conp]] 里发挥关键作用：构造题（找存在）是 $\NP$，推理题（排除所有可能）是 $\coNP$。一般认为 $\NP \neq \coNP$。

## 归约与 $\NP$-complete

无法给出绝对下界时，理论学者退而求相对下界：**多项式时间归约**。若问题 $L$ 能在多项式时间内转换为问题 $M$，记 $L \leq_p M$，那么：

$M \in \P \Longrightarrow L \in \P$

$M$ 至少和 $L$ 一样难。**$\NP$-hard** 是 $\NP$ 中所有问题都能归约到它的问题；若它同时也在 $\NP$ 内则叫 **$\NP$-complete**。Clique、IndependentSet、TSP、3CNF-SAT 都是 $\NP$-complete。对应地，3CNF-UNSAT 是 $\coNP$-complete。

## 为什么这对工程师重要

- 看见「这问题是 $\NP$-complete」时，应理解为「极大概率没有多项式算法，别白花时间找了」——该去做近似、启发式或限制输入结构
- 但「$X$ 是 $\NP$-complete」的说法必须先问清楚：**是哪个版本的 $X$？** 游戏里的「可一致摆法」和「能否推出某格」是完全不同的问题（见 [[patterna-hexcells-np-vs-conp]]）
- 归约是程序员最常低估的工具：把新问题映射到已知 $\NP$-complete 问题是说明它难；反向映射是把它**降维**到已有求解器（SAT solver、ILP）上

## Sources

- [[sources/schoener-intro-computational-complexity]]
- [[sources/schoener-complexity-of-patterna]]
