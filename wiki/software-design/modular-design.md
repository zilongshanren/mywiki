---
tags: [软件设计, 模块化, aposd]
date: 2026-04-05
sources: 1
---

# 模块化设计（Modular Design）

Ousterhout 对模块化的核心陈述：

> "In modular design, a software system is decomposed into a collection of modules that are relatively independent. Modules can take many forms, such as classes, subsystems, or services. In an ideal world, each module would be completely independent of the others: a developer could work in any of the modules without knowing anything about any of the other modules."

注意核心陈述：**开发者在任意一个模块里工作时，不需要了解其他模块**。

但这个理想是无法完全实现的：

> "Unfortunately, this ideal is not achievable. Modules must work together by calling each others's functions or methods. As a result, modules must know something about each other."

所以现实目标是：**最小化模块之间的依赖**。

## 核心认知转变

大多数程序员把模块化理解为「怎么拆分系统」，Ousterhout 把它理解为「**怎么控制认知成本**」。两种理解导致完全不同的设计决策：

- 按「怎么拆分」思考：根据功能边界切割——用户管理、订单处理、支付……再进一步细拆。
- 按「怎么控制认知成本」思考：问「当我在写 A 模块时，需要在脑子里同时装着哪些其他东西？」——这些「其他东西」就是认知成本。

好的模块设计让认知成本最小化。这就是 [[deep-modules]] 的追求。

## 衡量标准

真正的标准不是模块的数量或大小，而是：

- 使用这个模块需要知道多少其他东西？
- 改动它会影响多少其他模块？
- 实现换了，调用者受影响吗？

这些问题分别对应 [[cognitive-load]]、[[change-amplification]]、[[interface-vs-implementation]]。

## 相关

- 模块的理想形态：[[deep-modules]]
- 模块化失败的形态：[[shallow-modules]]、[[classitis]]
- 实现工具：[[information-hiding]]、[[abstraction]]

## Sources

- [[sources/aposd-day04]]
