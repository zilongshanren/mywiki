---
tags: [品味, 学习, 元, 综合]
date: 2026-04-05
sources: 8
---

# 提升品味的实践指南

一份基于本 wiki 内容综合出的**品味训练方法**。核心洞察：**品味不是规则，是判断力**；判断力靠持续的"**停下来 → 分析 → 找替代**"练习积累。

## 什么是品味

[[john-ousterhout|Ousterhout]] 在 APoSD Day 1 埋了一条关键护栏：

> "Every rule has its exceptions... If you take any design idea to its extreme, you will probably end up in a bad place. Beautiful designs reflect a balance between competing ideas and approaches."

**所有原则都是工具，不是规则**。[[deep-modules|深模块]]推到极致也是坏设计，SRP 推到极致就是 [[classitis]]。**品味正是在相互竞争的原则之间做平衡的能力**——不是机械套用任一条。

品味和知识的区别：
- **知识**是"我知道深模块应该接口简单、实现复杂"。
- **品味**是"我能感觉到这个接口虽然只有 3 个方法，但隐性约定太多，实际上是浅的"。

前者靠阅读，后者靠**带着概念反复看真实代码**。

## 五条可执行的练习

### 1. 建立红旗词汇表——把感觉变成概念

[[red-flags]] 给出了最重要的训练方法：**当你精确地说「这里是变更放大」而不是「这里有点乱」，你就有了改进方向**。

wiki 收录的红旗词汇表：

| 红旗 | 信号 |
|---|---|
| [[change-amplification]] | 改动需要触及多处 |
| [[cognitive-load]] | 需要大量前置知识才能理解 |
| [[unknown-unknowns]] | 改完后会不会坏，你不确定 |
| [[information-leakage]] | 同一份知识存在于多个模块 |
| [[shallow-modules]] | 接口复杂度接近实现复杂度 |
| [[classitis]] | 系统充满小类，跨多文件理解一个功能 |
| [[false-abstraction]] | 简洁外表下藏着必须知道的细节 |
| [[temporal-decomposition]] | 类名是流水线结构，相邻步骤共享格式知识 |
| [[obscurity]] | 需要大段注释才能安全使用 |

**实操**：把这张表贴在工位旁。下次读代码时**强制自己点名一条红旗**——不说"这里乱"，说"这里是信息泄漏"或"这里是时序分解"。这一步让你从感觉层面升到分析层面。

### 2. 强制 3 个替代设计

Ousterhout 在 APoSD Day 1 说：

> "Don't give up easily: the more alternatives you try before fixing the problem, the more you will learn."

**每次遇到红旗，强制自己想 3 个替代设计，然后才选一个**。这是 [[strategic-programming]] 的 10-20% 投资时间预算的具体用法。

大多数经验丰富的工程师跳过这一步——他们能**感觉到**代码有问题，但默认"找一个能工作的方案继续"。短期高效，长期错过设计能力成长机会。

### 3. 用 [[complexity]] 的三问审代码

Code review 时，不问"能不能工作"，问三个读者视角的问题：

1. **「没我上下文的读者能在合理时间内读懂吗？」**——[[cognitive-load]] 的检查
2. **「如果实现改了，调用方要跟着改吗？」**——[[change-amplification]] 的检查
3. **「如果我改这里，会不会在别处爆炸？」**——[[unknown-unknowns]] 的检查

**把这三个问题变成条件反射**，比任何代码规范都更能塑造品味。

### 4. 背诵 wiki 里的「品味结晶」

几个可以随身携带的判断准则：

**关于接口与实现**（[[information-hiding]]）：

> 真正的信息隐藏是设计决策的结果，不是语言约束的副产品。

用 `public` 字段可以做到完美隐藏，用满 `private` 也能漏个干净。

**关于重复与抽象**（[[higher-order-functions]]）：

> 代码重复是思维还没到位的信号——三次复制同一个模式，你欠它一个名字。

规则：**两次等待，三次抽象**。

**关于接口成本**（[[deep-modules]]、[[interface-vs-implementation]]）：

> 接口是成本，不是"提供的服务"。每多一个参数都是对所有调用者的税。

**关于类的大小**（[[classitis]]）：

> 行数是假指标，认知负担才是真指标。

800 行的 PlayerController 可能比 10 个 80 行的 Manager 更简单。

**关于精确 vs 可行**（[[probabilistic-algorithms]]）：

> 当精确解不可行时，概率算法不是妥协而是唯一合理的工程选择。

**关于复杂性的分类**（[[complexity]]）：

区分**本质复杂性**（必须有，封装它）vs **不必要复杂性**（设计出来的，消除它）。这是每次评审代码时的第一道分界线。

**关于技术债**（[[engine-evolution]]、[[tactical-programming]] vs [[strategic-programming]]）：

> 每个架构选择都是对未来的借贷。问题不是"该不该借"，而是"是否理解代价并有偿还计划"。

### 5. 接受「节制」这条底线

**品味的最高形态是知道每条原则的边界**。

- [[deep-modules|深模块]]过度 → 一个函数做所有事的 1000 行混乱。
- [[classitis|SRP]]过度 → Manager 癌症。
- [[information-hiding|信息隐藏]]过度 → [[false-abstraction|虚假抽象]]。
- [[strategic-programming|战略编程]]过度 → 过度工程、永远不发货。

**Beautiful designs reflect a balance between competing ideas**——优秀设计反映了相互竞争的理念之间的平衡。品味就是这种平衡能力。

## 建议的 30 天练习

| 周 | 重点 | 可量化产出 |
|---|---|---|
| 1 | 读旧代码，**点名红旗**。不改任何东西。 | 10 条「这段代码是 X 问题」笔记 |
| 2 | 新代码**每次 PR 写 3 个替代设计**，选最深的。 | 3 份自己的 alternatives 日志 |
| 3 | 做 code review 时用 [[cognitive-load]] 三问。 | 5 次 review 加上这三个问题 |
| 4 | 找一处**信息泄漏**并修复；写下「X 改了，多少处要改」。 | 1 次真实重构 |

## 为什么"停下来"比"做什么"更重要

APoSD 反复强调的是让"感觉有问题"时**不要下意识绕过去**。

> 停下来、分析、系统地寻找替代方案。

经验丰富的工程师能**感觉**到代码有问题，但真正提升品味的工程师会**停下来**。这个停顿就是品味生长的地方。

## 跨领域的品味一致性

品味不是只在软件设计里。本 wiki 的五大主题共享同一种品味培育路径：

- **[[complexity|APoSD]]** 的品味：在深度 vs 大小、分割 vs 合并之间找平衡。
- **[[elements-of-programming|SICP]]** 的品味：识别重复模式，找到"等待被浮现出来的抽象"。
- **[[probabilistic-algorithms|算法]]** 的品味：精确 vs 可行的工程取舍。
- **[[rendering-pipeline|渲染]]** 的品味：在 ALU / 带宽 / 精度之间找当前瓶颈。
- **[[game-engine|引擎]]** 的品味：在工具（Unity）vs 框架（Unreal）之间看清权衡。

**共通的能力是**：不把任何原则推到极致，始终在竞争约束之间寻找当前最优。

## 相关

- [[complexity]]——品味要对抗的敌人
- [[red-flags]]——品味的词汇表
- [[strategic-programming]]——品味的时间预算
- [[zero-tolerance]]——品味的日常纪律
- [[continuous-design]]——品味是持续过程
- [[overview]]——整体视角

## Sources

- [[sources/aposd-day01]]
- [[sources/aposd-day02]]
- [[sources/aposd-day04]]
- [[sources/aposd-day05]]
- [[sources/aposd-day06]]
- [[sources/sicp-day01]]
- [[sources/sicp-day05]]
- [[sources/sicp-day06]]
