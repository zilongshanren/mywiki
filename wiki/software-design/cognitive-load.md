---
tags: [软件设计, 复杂性症状, aposd]
date: 2026-04-05
sources: 1
---

# 认知负荷（Cognitive Load）

**认知负荷**是 Ousterhout 列出的第二种复杂性症状：

> "Cognitive load refers to how much a developer needs to know in order to complete a task."
> 认知负荷指的是开发者为完成一个任务需要知道多少东西。

认知负荷和代码行数不是同一件事。Ousterhout 明确反对把简洁等同于简短：

> "Sometimes an approach that requires more lines of code is actually simpler, because it reduces cognitive load."
> 有时候更长的方案反而更简单，因为它降低了认知负荷。

这戳破了「简洁就是短」这种肤浅理解。

## 常见来源

- **隐式所有权约定**。C++ 里一个函数返回指针但不说由谁 free。Rust 的所有权系统存在的部分意义，正是把这种负荷变成编译器强制的类型级契约。
- **没有生命周期绑定的协程**。Unity 的 `StartCoroutine` 让人不确定 GameObject 销毁时协程会怎样。UniTask 的价值在于把异步工作绑定到显式的 CancellationToken，显著降低这种负荷。
- **全局可变状态**。每一个 Singleton 都是认知负荷的发射源：读一个 static 字段，就要追查所有可能写入它的地方。
- **未文档化的副作用**。一个名为 `getX` 的函数同时修改了状态，读者要时刻记住这个陷阱。

## 为什么文档不是根本答案

> "The need for extensive documentation is often a red flag that the design isn't quite right."
> 需要大量文档本身就是设计不太对的红旗。

文档会过时，注释会失效。更深的方案是让设计自解释：用显式参数代替全局变量，用类型表达约束，用精确命名直接点明事物的身份。**好的设计通过结构转移知识，从而减少对文档的需求。**

## Code Review 的含义

Code review 的核心问题应该是：**「一个没有我这份上下文的读者，能否在合理时间内理解这段代码？」** 如果不能，这段代码就在施加认知负荷，review 要追问为什么——不止是「能不能工作」。

## 相关

- 姊妹症状：[[change-amplification]]、[[unknown-unknowns]]
- 根源：[[dependencies]]、[[obscurity]]
- 对策：[[deep-modules]]、[[information-hiding]]、[[abstraction]]

## Sources

- [[sources/aposd-day02]]
