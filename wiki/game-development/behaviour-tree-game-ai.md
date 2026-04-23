---
tags: [ai, behaviour-tree, rts, scripting, tools]
date: 2026-04-19
sources: 2
---

# 行为树 AI（Swords & Soldiers 两代迭代）

Joost van Dongen 从学院派 AI 走到业界后的顿悟：绝大多数游戏 AI 根本没有「智能」——所谓 AI 课教的是国际象棋那种简化问题或 pathfinding 这类工具算法，实时策略游戏里的真正复杂决策**业界做法就是长链 if-else 脚本**，顶多掺点随机。Black & White 的 Decision Trees 是少数例外。承认这个事实之后，剩下的问题就变成：**怎么把成百上千条 if-else 管理得不崩**。

## 三代演进

1. **纯 C++ if-else 链**（学校项目）：写起来慢、没有结构视图、bug 难查，弃。
2. **Lua 脚本**（Ronimo 早期取消掉的项目）：去掉了编译步骤，但 Lua 里写复杂 AI 的难度跟 C++ 几乎一样；还是得程序员写；而且把 C++ 数据暴露到 Lua 要大量胶水代码；复杂度上来后定位 bug 同样痛苦。弃。
3. **行为树 + 图形化编辑器**（受 Bungie Halo 2 GDC 论文启发）：实习生搭的 wxWidgets C++ 编辑器；设计师自己画树；程序员负责实现足够多的 **condition** 和 **action** 原子块，把 C++ 里的细节（比如「是否附近有敌方 Necromancer」里遍历全体单位算距离）藏在原子块里。这套用下来 Ronimo 一直沿用，并带到下一款不同类型的游戏。

## 行为树的具体工作方式

- **优先级驱动**：Swords & Soldiers 那一代的行为树本质是按优先级从上往下扫，**第一个条件满足的 action 就执行，不再往下看**。所以顶部动作必须挂强条件（例：「用雷电打 Necromancer」挂在最上，条件是附近有敌方 Necromancer 且法力足够），否则下面的永远轮不到。
- **示例层次**（典型 skirmish AI）：顶部 = useAbility 放雷电；中部 = createUnit 造工人，条件是 unitCount < 10 且 goldAmount 够且 timeSinceLastUnit > 10s；底部 = createUnit 造 Berserker（兜底，什么都没触发就一直压兵）。
- **可读性靠「够多且够聪明的积木」**：如果原子块粒度太粗或数量太少，设计师只能自己在树里重写复杂度，树会爆炸。Joost 承认 Swords & Soldiers 的 skirmish 树后期「太大太复杂」，如果当时有更丰富的 condition/action，树可以砍一半大小。

## 第二个意外用途：剧情脚本

Joost 起初坚决反对把 cutscene 触发器混进 AI 树，担心脏。设计师坚持试了——结果这套系统自带的「条件 + 动作」对剧情触发天然匹配（什么时候 pause、放对话、播动画），复用成本极低。**行为树无意中变成了 story event scripting 系统**。

## Secret New Game 的关键修改：去掉优先级

优先级模型的硬伤是 **AI 一次只能做一件事**。现实里 RTS AI 常需要同时造兵+放技能，在优先级树里要用很别扭的绕法。下一代产品直接把优先级扔掉，改成**大 if-else 树**：条件 + 动作结构几乎一样，但执行遇到一个成立的 action 后**不停，继续往下扫**。代价是不再有天然 fallback 语义，好处是可读性大增，还自然支持 if-then-else（Swords & Soldiers 实际只有 if-then）。

## 工程化要点

- 编辑器本体：wxWidgets + C++（评论区建议改 C# / .NET，更适合写工具）。
- AI 行为归属权从程序员转到**逻辑能力强的设计师**（Jasper、Fabian、Tom），程序员只维护原子块库；这是 Joost 回头看觉得最有价值的一步——「设计师做出来的东西经常超出我能想到的」。

## 相关
- [[determinism-vs-smart-ai-gameplay]] —— 强 AI 与确定性回放的矛盾
- [[a-star-pathfinding]] —— 行为树常见的 action 之一
- [[planning-over-rng-game-design]] —— 设计层面「可预测」vs「随机」的取舍

## Sources
- [[sources/joostdevblog-ai-swords-soldiers]]
