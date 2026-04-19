---
tags: [cs-theory, np-complete, co-np, game-design, puzzle]
date: 2026-04-19
sources: 1
---

# Patterna / HexCells / Minesweeper：$\NP$ 还是 $\coNP$？

一个在玩家社区广为流传的说法是「Minesweeper 是 $\NP$-complete」，因此 HexCells、Patterna 这类同构游戏也都 $\NP$-complete。[[sebastian-schoener]] 指出这**混淆了两个完全不同的问题**。

## 一致性问题 vs. 推理问题

**Consistency Problem（MCP / PatPC）**：给一块已标注的棋盘，**是否存在**一种摆法与约束一致？

**Progress Problem（PatProg）**：给一块一致的棋盘，**是否某个未知格的状态被约束唯一确定**？即能否作出下一步推理？

这两个问题的结构完全相反：

| 维度 | Consistency | Progress |
|---|---|---|
| 问法 | 存在一个摆法 | 所有摆法都一致 |
| 证据 | 给出一个摆法（yes 证据短） | 无法给短 yes 证据，但给反例否定容易 |
| 所属类 | $\NP$（→ $\NP$-complete） | $\coNP$（→ $\coNP$-complete） |
| 玩家做的 | ❌ 不是这个 | ✅ 就是这个 |

## 为什么玩家做的是 $\coNP$

点开一个方格前，玩家不是在问「有没有可能摆法」。他实际在证：**在当前所有约束允许的摆法里，这个格子都是同一状态**——只要能举出两种摆法让它一次是雷一次不是，这个格子就不能点。

「所有模型上都为真」是**逻辑有效性（validity）**，和「存在模型使之为真」（**可满足性，SAT**）对偶。SAT 是 $\NP$-complete，validity of propositional formulas 是 $\coNP$-complete。

## 归约：3CNF-UNSAT → PatProg

PatPC 的 $\NP$-completeness 用 3CNF-SAT 归约；PatProg 的 $\coNP$-completeness 用 **3CNF-UNSAT** 归约。核心构造：把布尔公式 $\varphi$ 编码成一块 Patterna 棋盘，让输出节点**当且仅当公式不可满足时**被唯一确定为 non-pattern。

- **变量 gadget**：每个变量 $A$ 用两个未知节点 + 一个一致性节点，保证 $A$ 和 $\lnot A$ 恰有一个是 pattern
- **OR gadget**：利用「4 连通 pattern 节点」约束，构造当且仅当 $X \lor Y \lor Z$ 为真时 OR 节点为 pattern 的结构
- **DeMorgan**：AND 用 $\lnot \bigvee \lnot$ 组合出来
- **总 pattern 数约束**：Patterna 总是显示剩余 pattern 节点数，必须显式算准（$2v + 4n + n + 1$），否则归约破缺

## 值得记下的教训

- **先问问题定义再套结论**：「这个游戏是 NP-complete」几乎一定是口头简化；严谨结论对应的是哪个判定问题？
- **游戏机制的"玩法语义"决定复杂度类别**：同一张棋盘，问"可以摆吗"和"必须摆什么"是两个不同的计算问题
- Scott、Stege、van Rooij 在 2011 年的 *Minesweeper May Not Be NP-Complete but Is Hard Nonetheless* 得到同样修正——Minesweeper 的**推理**问题是 $\coNP$-complete
- 关卡整体可解性 **PatSolv**（所有步骤一路能推到底）上界在 $\coNP$，用「obstruction」作反例证据；但 $\coNP$-complete 的 hardness 比单步难证，因为需要输入是"完整关卡"而非一致棋盘

## 相关

- [[computational-complexity-theory-intro]]

## Sources

- [[sources/schoener-complexity-of-patterna]]
