---
tags: [软件设计, 复杂性, aposd, 核心概念]
date: 2026-04-05
sources: 3
---

# 复杂性（Complexity）

**复杂性**是软件设计的核心敌人。Ousterhout 给出了精确定义：

> "Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system."
> 复杂性是软件系统结构中任何使系统难以理解和修改的东西。

注意这个定义的边界：复杂性与代码行数、功能多少无关，它关乎**理解和修改的难度**。这让复杂性从客观属性变成了读者脑中的主观体验。

## 读者视角

> "Complexity is more apparent to readers than writers."

写代码的人在当下脑子里装着完整上下文——所有隐式假设、设计决策都是鲜活的。但三个月后的读者看到的是一个被剥夺了上下文的代码壳。所以「我觉得挺清晰」从来不是有效的辩护，因为写作者永远是最有偏见的裁判。

## 复杂性公式

Ousterhout 给出一个粗糙但有用的表达：

**C = Σ(cp × tp)**

其中 `cp` 是某个组件的复杂度，`tp` 是开发者在这个组件上花费的时间比例。关键推论：**把复杂性隔离到不常触及的地方，几乎等同于消除它**。一个充满 GPU tricks 的渲染器，如果开发者从不触碰，它对整体系统的成本很低。

## 本质复杂性 vs 不必要复杂性

并非所有复杂性都是坏的。有些系统本质上复杂——碰撞检测、编译器优化、网络 lag compensation。Ousterhout 要对抗的是**不必要的复杂性**：那些本可以通过更好设计来消除或封装、但没有被处理的复杂性。

一个常见误区是把「性能关键代码本来就复杂」等同于「这种复杂性是合理的」。即使是本质复杂性，也应该被封装好，不让调用者直面它。

## 渐进累积

复杂性不是由某个灾难性错误造成的，而是通过成百上千个各自合理的小决定累积：

> "Complexity comes about because hundreds or thousands of small dependencies and obscurities build up over time."

每一次「这里先 hardcode」或「这个类再加一个方法」在局部都说得通。它们的总和则说不通。这就是温水煮青蛙的动力学，也是 [[zero-tolerance]] 哲学的依据：如果你容忍每一次小妥协，复杂性呈指数增长；如果你每次付出小修复成本，它保持线性。

## 对抗复杂性的两条路

1. **消除它**——去除特殊情况、统一标识符、简化逻辑。
2. **封装它**——把复杂行为藏在简单接口背后，让调用者不暴露在复杂性前。这就是模块化设计，产出的是 [[deep-modules]]。

## 相关

- 症状：[[change-amplification]]、[[cognitive-load]]、[[unknown-unknowns]]
- 根源：[[dependencies]]、[[obscurity]]
- 对策：[[tactical-programming]] vs [[strategic-programming]]、[[deep-modules]]、[[information-hiding]]

## Sources

- [[sources/aposd-day01]]
- [[sources/aposd-day02]]
- [[sources/aposd-day03]]
