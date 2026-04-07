---
tags: [编程语言, sicp, 抽象]
date: 2026-04-05
sources: 1
---

# 过程抽象（Procedural Abstraction）

**把"做什么"与"怎么做"分离**——调用者只需知道接口契约，不需知道实现。

## SICP 的陈述

> "The contrast between function and procedure is a reflection of the general distinction between describing properties of things and describing how to do things."

## 核心组件

- **绑定变量（Bound Variables）**：过程参数，作用域局限于过程内部。重命名不影响行为。
- **自由变量（Free Variables）**：来自外部环境的变量——是**隐式耦合**的来源。
- **块结构（Block Structure）**：函数内部定义辅助函数，隐藏实现。
- **词法作用域**：参见 [[lexical-scoping]]。

## 过程抽象屏障

调用者和实现之间有一道"屏障"，接口契约定义清楚后，实现可以自由演化而不影响调用者。这与 APoSD 的 [[information-hiding]] 是完全一致的思想。

## 品味

好的过程抽象：
1. **接口稳定，实现可替换**
2. **充分隐藏信息**
3. **名字有意义**
4. **避免过度抽象**——单次用的 helper 不必抽成函数

## 游戏开发案例

- Unity Surface Shader：黑盒隐藏渲染管线复杂性。
- 行为树节点：遵循 Tick 协议，每个节点是黑盒。
- ECS Component：纯数据黑盒。

## 相关

- [[information-hiding]]
- [[lexical-scoping]]
- [[closure]]
- [[higher-order-functions]]
- [[deep-modules]]

## Sources

- [[sources/sicp-day02]]
