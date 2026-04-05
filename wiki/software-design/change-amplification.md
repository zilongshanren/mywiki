---
tags: [软件设计, 复杂性症状, aposd]
date: 2026-04-05
sources: 1
---

# 变更放大（Change Amplification）

**变更放大**是 Ousterhout 列出的 [[complexity]] 三大症状之一：

> "A seemingly simple change requires code modifications in many different places."
> 一个看似简单的改动，需要在许多不同的地方修改代码。

经典例子是早期网页把背景色写死在每个页面里——换颜色就要改所有页面。等价的模式到处都是：散布在多个文件的 magic number、重复的业务规则、复制粘贴的序列化代码。

## 为什么会发生

变更放大是**设计决策被分散**的症状。当一份知识——一个伤害系数、一个文件格式、一个枚举布局——同时存在于多个地方时，修改它就需要同步多处。这本质上是 [[information-leakage]]：某个设计决策从它该待的地方泄漏了出去。

游戏开发中的典型例子：

- 基础伤害值 50 硬编码在 17 个地方。每次策划调整数值，工程师要全局搜索并祈祷没漏。
- UI 代码直接读战斗逻辑的枚举值，战斗系统任何重构都会向上级联。
- AI 代码依赖动画状态机的内部枚举，动画一变 AI 就挂。

## 成本曲线

变更放大的成本是**线性或超线性**：一份决策被分散到多少处，就得改多少处，每一处改动都有引入 bug 的风险。和 [[unknown-unknowns]] 不同，变更放大至少是**可见的**——你每次改动都会感到痛，所以你知道问题存在。

## 解药

把每个设计决策集中在一个模块里。[[information-hiding]] 是主要武器：确保「知识」（格式、系数、算法）只存在于一个地方。一个拥有这份决策的 [[deep-modules|深模块]]，不会暴露任何泄漏它的接口。

## 相关

- 根源：[[dependencies]]、[[information-leakage]]
- 对策：[[information-hiding]]、[[deep-modules]]
- 其他症状：[[cognitive-load]]、[[unknown-unknowns]]

## Sources

- [[sources/aposd-day02]]
