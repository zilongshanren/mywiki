---
tags: [软件设计, aposd, 核心概念]
date: 2026-04-05
sources: 1
---

# 接口 vs 实现

Ousterhout 对模块价值的核心比喻：

> "The benefit provided by a module is its functionality. The cost of a module (in terms of system complexity) is its interface."

**功能是收益，接口是成本。**

## 为什么接口是成本

通常接口被理解为「提供服务的入口」，是正面的东西。Ousterhout 颠倒了这个视角：**每一个接口方法都是一个负担**——调用者必须学习的东西、必须在脑子里维持的知识、可能出错的地方。

接口的成本包含两种：

**形式化（Formal）**：方法签名、参数类型、返回值、异常。编译器能检查。

**非形式化（Informal）**：

> "The informal parts of an interface include its high-level behavior, such as the fact that a function deletes the file named by one of its arguments. If there are constraints on the usage of a class (perhaps one method must be called before another), these are also part of the class's interface."

> "For most interfaces the informal aspects are larger and more complex than the formal aspects."

一个方法签名可能只有一行，但它隐含的使用约束、副作用、调用顺序要求、线程安全保证……往往比签名本身复杂得多。

## 设计的含义

- 减少接口面积不止是减少方法数量，更是减少调用者需要理解的隐性约定。
- 每增加一个接口方法，都要问「调用者真的需要控制这个吗，还是模块内部可以有合理默认值？」
- 把**常见情况**做简单——Unix I/O 默认顺序+缓冲，不要求调用者显式处理。
- 实现细节不应该泄漏（参见 [[information-leakage]]）——如果调用者必须理解实现才能正确使用接口，接口设计失败。

## 判断标准

**好的模块让你「不需要打开实现代码就能自信地使用它」。** 如果你经常需要看源码才知道怎么用一个 API，这个 API 的设计者欠你一个道歉。

## 相关

- 深度的源头：[[deep-modules]]
- 成本端：[[shallow-modules]]
- 核心工具：[[abstraction]]、[[information-hiding]]

## Sources

- [[sources/aposd-day04]]
