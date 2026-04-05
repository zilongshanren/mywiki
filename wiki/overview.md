---
tags: [overview, synthesis]
date: 2026-04-05
sources: 7
---

# 知识库综述

本知识库目前包含两组看起来不相干、实际高度呼应的源材料：

- **[[john-ousterhout|John Ousterhout]] 的 A Philosophy of Software Design（APoSD）前 5 章的学习笔记（Day 1–6）**——一个以[[complexity|复杂性]]为敌的软件设计哲学框架。
- **[[jasper-flick|Jasper Flick]] 的 Unity Custom SRP 6.1.0 教程**——一次对具体渲染管线的微型重构与调试可视化添加。

它们共享同一个核心主题：**复杂性管理**。APoSD 给出原理与框架，Custom SRP 给出一份在真实引擎代码里实践这些原理的微观样本。

## 主题一：复杂性是首要敌人

Ousterhout 开宗明义——**软件开发的最大限制是理解系统的能力，不是技术**。这把软件设计的议题从「怎么写代码」翻转到「怎么管理认知负荷」。[[complexity|复杂性]]被精确定义为「任何使系统难以理解和修改的东西」——**读者视角**，不是写者视角。

复杂性以三种症状出现：
- **[[change-amplification]]**：改一个决策要改多个地方
- **[[cognitive-load]]**：需要知道太多
- **[[unknown-unknowns]]**：不知道自己不知道（最危险）

有两个根源：**[[dependencies]]**（依赖）和 **[[obscurity]]**（模糊性）。

复杂性**渐进累积**——没有灾难性错误，只有无数个局部合理的小妥协。**[[zero-tolerance|零容忍]]**是唯一能让复杂性从指数增长降到线性增长的纪律。

## 主题二：深模块是正面构造

Ousterhout 最核心的正面构造是 **[[deep-modules|深模块]]**：**强大功能 + 简单接口**。接口被重新定义为**成本**——调用者必须承担的认知负担——而功能是收益。这颠覆了「接口是提供服务」的通常直觉。

深度的标杆：**[[unix-io|Unix I/O]]** 的 5 个系统调用隐藏几十万行实现；**[[garbage-collector|垃圾回收器]]**是零接口的极限深模块。

对立面是 **[[shallow-modules|浅模块]]**——接口复杂度接近实现复杂度，抽象为零。当浅模块成为系统性倾向，就是 **[[classitis]]**——「类越多越好」的教条。**[[java-io|Java I/O]]** 的三件套是经典病例。

**核心认知转变**：**好的抽象不是把代码分割成更小块，而是让调用者理解更少的东西**。分割是手段，不是目的。

## 主题三：信息隐藏是深度的引擎

**[[information-hiding|信息隐藏]]**是达成深度的技术——每个模块封装代表设计决策的「知识」，让它们活在实现里、不出现在接口上。

关键区分：**`private` ≠ 信息隐藏**。`private` 是访问控制；信息隐藏是设计哲学。一个用 public 字段的类可以做到完美信息隐藏；满屏 private 的类也可能通过 getter 把一切漏个干净。

信息隐藏的反面是 **[[information-leakage|信息泄漏]]**——同一份知识存在于多个模块。**[[temporal-decomposition|时序分解]]** 是常见制造者：按时间顺序切模块，而不是按知识归属。

反直觉推论：**有时让类稍微大一点反而改善信息隐藏**——Clean Code 的「小类优先」教条在此失效。

## 主题四：战术 vs 战略

面对复杂性，有两种编程心态的对立：

- **[[tactical-programming|战术编程]]**：目标是让东西工作。短视，制造复利陷阱。极端形态是**[[tactical-tornado|战术龙卷风]]**——高速产出但成本外部化。
- **[[strategic-programming|战略编程]]**：目标是「一个优秀的设计，恰好也能工作」。需要**投资心态**，建议 **10–20% 时间花在设计投资**。

战略编程**不是完美主义，是复利**。每个工程师、持续、小投资——战略编程是**文化**，不是项目。

## 具象化：Custom SRP 6.1.0 作为原理实践

[[custom-srp|Custom SRP 6.1.0]] 教程本身是一次小规模但干净的战略编程样本：

- **消除 [[change-amplification]]**：把「相机目标的选择」集中到 `SetupPass.Record` 一处，其他 Pass 只通过 `textures.cameraTarget` 使用。
- **[[deep-modules|深模块]]思想的体现**：[[render-graph|Render Graph]] API 让 Pass 作者只声明资源依赖和执行函数，隐藏资源生命周期、Pass 排序、内存 aliasing 等复杂性。
- **[[debug-visualization|调试可视化]]作为小型深模块**：调用者只需 `showColorLUT = true`，底层处理所有状态与绘制。

## 游戏开发中的应用

Ousterhout 的框架特别适合游戏开发，因为游戏项目有几个放大复杂性的特征：需求高速变化、跨学科协作、实时系统的隐式顺序。典型问题与对策收录在：

- [[classitis-in-games]]——Manager 癌症、事件系统滥用
- [[resource-system-design]]——信息隐藏与虚假抽象的典型战场
- [[ecs]]——把隐式依赖变显式的例证
- [[rendering-api-depth]]——接口深度在渲染 API 中的体现
- [[unity-complexity-patterns]]——综合的复杂性观察

## 开放问题 / 张力

- **深度 vs SRP**：Ousterhout 和 Clean Code 在「类应该多大」上直接冲突。本知识库目前只收录了 APoSD 的视角，Clean Code 的反驳未独立成文。
- **合理的浅模块**：Ousterhout 承认存在合理场景（边界适配、框架强制、测试隔离），但没有给出清晰的判断边界。
- **GC 的边界**：[[garbage-collector]] 作为极限深模块的例子，在对暂停时间敏感的游戏场景下会失效——深度抽象的边界在哪里？
- **战略编程的度量**：10-20% 投资、深度公式（实现行数/接口行数）都是启发式，没有严格的工程度量方法。

## 待补充的来源

- APoSD 后续章节（第 5 章 Information Hiding 之后的部分、General-Purpose Modules、Define Errors Out of Existence、Design It Twice 等）。
- Clean Code 和设计模式的第一手资料，用于补全对照。
- 更多游戏引擎代码实践案例（目前只有 Custom SRP 这一个）。
