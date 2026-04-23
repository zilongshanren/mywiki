---
tags: [source, bitsquid, 软件设计, 重写, flow]
date: 2026-04-19
sources: 1
---

# Four Meditations on Bad Design Decisions（Bitsquid, 2012-12）

[[niklas-frykholm|Niklas Frykholm]] 2012 年 12 月的复盘：在把 Bitsquid 的可视化脚本系统 **Flow**（见 [[flow-graph-data-oriented-runtime]]）做大规模重写后，回头总结第一版留下的四条坏决策。

## 摘要

开场先声明一个反直觉的前提——**重写比新写更难**：新写能小步迭代、早期 release、用户反馈驱动演化；重写必须"至少和旧版一样好"才敢交付，否则用户会问"你怎么把它做烂了"。因此第一版的所有坏决定都要在重写时加倍偿还。接下来四条教训逐一出场：（1）不要把字符串当非文本用，要把 Id 和 DisplayName 拆开；（2）拿不准的特性宁愿不加，等想到漂亮解法再上；（3）能显式就别隐式——反射、魔法推导在长期来看都是负债；（4）复杂代码只在真正本质复杂或极致性能场景才合理，其它场景就是成本。评论区活跃——有人讨论 C# 的 Attribute 方案是否比 config file 更合理（Niklas 承认看法有分歧），还有人追问 Flow 在真实项目里的使用，作者答：Flow 是给美术/关卡的，不是给程序员的——程序员用 Lua，事件驱动而非主动循环，深度优先求值，race 用 sequence 节点解决。

## 关键要点

- 重写的退化式约束：必须"至少和旧版一样好"，等于退回瀑布流。
- **字符串 ≠ 标识符**：Id / DisplayName 分离；临时同名的 "rock / rock_small" 例子是经典反例。
- 不完美的特性宁愿砍：Flow 的 "Do First / Do Last" 右键菜单 → 换成显式 sequence 节点。
- 反射驱动的"隐式"便利在存档兼容、字段顺序等处反噬；应改用显式 config 定义节点。
- 折叠（fold）应做成**视觉操作**而非数据变换；一旦走复杂代码的不归路，下次重写还得把复杂度再造一遍。
- Flow 的 runtime 行为：**事件驱动，不 update**；多个下游默认并行（不确定序），要序就显式 sequence；深度优先求值；事件流易于推理，几乎不会陷入 race。

## 链接到的概念

- [[four-meditations-on-rewrites]]
- [[strings-as-identifiers-antipattern]]
- [[flow-graph-data-oriented-runtime]]
- [[no-magic-principle]]
- [[strategic-programming]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2012/12/four-meditations-on-bad-design-decisions.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2012-12-11_four-meditations-on-bad-design-decisions.md`
