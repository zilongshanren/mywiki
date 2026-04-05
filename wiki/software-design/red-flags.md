---
tags: [软件设计, aposd, 工具]
date: 2026-04-05
sources: 1
---

# 红旗（Red Flags）

Ousterhout 在 APoSD 第一章提出的设计直觉训练工具：

> "One of the best ways to improve your design skills is to learn to recognize red flags: signs that a piece of code is probably more complicated than it needs to be."

**红旗是「代码比需要的更复杂」的信号**。全书的每一章都在扩展红旗的词汇表——变更放大、认知负荷、未知未知、信息泄漏、浅模块、虚假抽象等等。

## 正确使用红旗的姿势

> "When you see a red flag, stop and look for an alternate design that eliminates the problem. When you first try this approach, you may have to try several design alternatives before you find one that eliminates the red flag. Don't give up easily: the more alternatives you try before fixing the problem, the more you will learn."

关键是：**停下来、分析、系统地寻找替代方案**。经验丰富的工程师常常能「感觉到」代码有问题，但不会停下来分析，更不会刻意培养替代方案的能力。他们的默认解法是「找一个能工作的方案继续」——短期高效，长期错过设计能力的成长机会。

## APoSD 中的红旗词汇表

从本知识库抽取的红旗列表：

- **[[change-amplification]]**：改动需要触及许多地方。
- **[[cognitive-load]]**：需要大量前置知识才能理解。
- **[[unknown-unknowns]]**：改完之后会不会坏，你不确定。
- **[[information-leakage]]**：同一份知识存在于多个模块。
- **[[shallow-modules]]**：接口复杂度接近实现复杂度。
- **[[classitis]]**：系统充满小类，理解单个功能需要跨多个文件。
- **[[false-abstraction]]**：简洁外表下藏着必须知道的细节。
- **[[temporal-decomposition]]**：类名是流水线结构，相邻步骤共享格式知识。
- **过度文档**：需要大段注释才能使用 → [[obscurity]] 的伪装。

## 价值

当你能精确地说「这里有变更放大问题」而不是「这里看起来有点乱」，你就有了更清晰的改进方向。红旗词汇表把「感觉」升华成可以分析、交流、系统化解决的框架。

## 相关

- [[complexity]]——红旗们共同指向的敌人
- [[strategic-programming]]——识别红旗后应有的反应
- [[zero-tolerance]]——对红旗的处理纪律

## Sources

- [[sources/aposd-day01]]
