---
tags: [source, aposd, 软件设计]
date: 2026-04-05
sources: 1
---

# APoSD Day 5 —— 浅模块之罪 & Classitis

APoSD 学习推送系列第 5 天，对应第 4 章 Modules Should Be Deep（后半部分）。

## 摘要

详述 **[[shallow-modules|浅模块]]** 的病理：接口复杂度接近实现复杂度，提供的抽象为零。**[[classitis]]**（类炎症）是系统性的设计疾病——「类越多越好」的教条式理解导致系统级接口复杂度爆炸。**Java I/O vs Unix I/O** 对照展示两种设计哲学。游戏引擎里的 **Manager 癌**和 **Event System 滥用**是 Classitis 的典型。合理的浅模块场景：边界层、框架强制、测试隔离——都需要**有意识**的权衡。

## 关键要点

- 浅模块定义：**interface 的复杂度相对于功能过于复杂**。
- `addNullValueForAttribute` 案例：interface 复杂度 = 实现复杂度，发现/记忆成本额外为正——**负数价值**。
- Classitis 的危害：**「These interfaces accumulate to create tremendous complexity at the system level」**。
- Java I/O 三件套 + buffering 的「annoying → error-prone」链条。
- Unix I/O「**为最常见用例优化，把复杂度内化在实现里**」。
- 游戏的 PlayerXXXManager 群：十个 Manager 的系统级接口远比一个 800 行的 PlayerController 复杂。
- Event System 的隐性 Classitis：每个 Manager 接口看起来简洁，**系统整体接口是极度复杂的且隐性的**。
- **显式耦合比隐式耦合好管理**——显式能看到、追踪、测试。
- 合理浅模块：有意识的、知道代价的。

## 链接到的概念

- [[shallow-modules]]
- [[classitis]]
- [[deep-modules]]
- [[java-io]]
- [[unix-io]]
- [[classitis-in-games]]
- [[john-ousterhout]]

## 原文

- 链接到：[[raw/articles/a-philosophy-of-software-design/day05]]
