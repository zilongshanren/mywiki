---
tags: [source, game-development, ai, behaviour-tree, rts]
date: 2026-04-19
sources: 2
---

# AI in Swords & Soldiers（Joost van Dongen，2010-12-31 / 2011-01-08 两部分合并）

[[joost-van-dongen]] 2010 年末到 2011 年初的两篇连载，写 Swords & Soldiers（Ronimo 的 2D 侧向 RTS）是怎么一步步把 AI 做出来的，同时把 Ronimo 从学院 AI 幻想里拉出来的过程拍给新人看。

## 摘要（Part 1：三代演进）

Joost 在大学里期待 AI 课上是聪明的学习算法，上了课才发现**业界 AI = 长链 if-else 脚本**，真正的决策问题在学界都没解掉。于是问题变成「怎么把几百条 if-else 管住」。Ronimo 试了三代：第一代纯 C++ if-else 链，**结构不可见，bug 难查**；第二代上 Lua，**免编译了但逻辑复杂度没变，胶水代码反而多**；第三代看到 Bungie 关于 Halo 2 行为树的 GDC 论文（2005），实习生用 wxWidgets 搭了图形化行为树编辑器，这一代成了公司长期方案，跨到下一款不同类型的游戏继续用。

## 摘要（Part 2：具体机制与演进）

Swords & Soldiers 的行为树是**优先级树**：从上往下扫，第一个条件满足的 action 就执行、停止。顶部 action 必须挂强条件，否则下面永远跑不到（示例：顶部「放雷电」仅在有敌 Necromancer 且法力足够时触发；中部「造工人」有 unitCount/goldAmount/timeSinceLastUnit 三重条件；底部「造 Berserker」兜底）。**原子块（condition/action）的粒度**是这套系统的关键：例如 `unitNear` 内部扫全体敌方 Necromancer 算距离，复杂度藏在 C++ 里，设计师不感知。Joost 事后承认 Swords & Soldiers 的 skirmish 树太大，如果当年积木更丰富，树能砍一半。这套系统**意外地同时变成了 story event 脚本系统**，触发 cutscene 跟触发 action 是一类问题。到 Secret New Game，Joost 把优先级模型整个扔掉改成**大 if-else 树**：执行完一个 action 不停、继续往下——这样天然支持 AI 同时造兵+放技能，可读性大增，还自然获得 if-then-else。最终结论：AI 行为归设计师写，程序员只维护原子块库。

## 关键要点

- 承认「游戏 AI 本质是脚本」是第一步，剩下的是可维护性。
- C++ 与 Lua 都无法解决「结构视图」问题，图形化才行。
- 优先级树适合「一次做一件事」；需要并行行为时换成 if-else 树。
- 原子块库的粒度和数量决定树能不能被设计师驾驭。
- 同一套触发/动作机制可一鱼两吃做 AI + cutscene scripting。
- 工具 UI 早期 wxWidgets + C++，Joost 事后建议改 C# / .NET。

## 链接到的概念

- [[behaviour-tree-game-ai]]
- [[determinism-vs-smart-ai-gameplay]]
- [[planning-over-rng-game-design]]

## 原文

- Part 1：http://joostdevblog.blogspot.com/2010/12/ai-in-swords-soldiers-part-1.html
- Part 2：http://joostdevblog.blogspot.com/2011/01/ai-in-swords-soldiers-part-2.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-12-31_ai-in-swords-soldiers-part-1.md`
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-01-08_ai-in-swords-soldiers-part-2.md`
