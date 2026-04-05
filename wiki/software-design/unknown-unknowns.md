---
tags: [软件设计, 复杂性症状, aposd]
date: 2026-04-05
sources: 1
---

# 未知的未知（Unknown Unknowns）

**未知的未知**是最危险的复杂性症状：

> "Of the three manifestations of complexity, unknown unknowns are the worst."
> 三种复杂性表现里，未知的未知是最糟糕的。

[[change-amplification|变更放大]]让工作更繁琐，[[cognitive-load|认知负荷]]让工作更费力——至少你知道问题存在。未知的未知则不一样：

> "Unknown unknown means that there is something you need to know, but there is no way for you to find out what it is, or even whether there is an issue. You won't find out about it until bugs appear after you make a change."
> 未知的未知是指你需要知道某件事，但无法得知它是什么，甚至不知道有没有问题。你只会在改动之后、bug 出现时才发现。

## 经典例子

一个网站把背景色存在中心变量里（好设计），但某些页面基于背景色手算了「强调色」并硬编码在各处（坏设计）。当你改背景色时，你更新了所有中心变量的引用，以为大功告成——结果上线就坏了，因为没人告诉你还有那些强调色的依赖。

## 游戏开发中的变体

- 新加一个 `PlayerState.Stunned` 枚举值。所有 `switch` 被正确更新——除了一个模块用硬编码整数值做判断（`if (playerState == 3)`）。三天后 QA 报 bug。
- 某个子系统默默假设了一个初始化顺序。这个假设没有出现在任何代码或文档里。换到新平台后，顺序变了，某个边缘场景触发崩溃，开发者连线索都找不到。

## 为什么这么危险

未知的未知无法通过「做改动时更仔细」来预防。它们只在 bug 出现时才浮现，反馈回路极长，根因和症状距离遥远。平均诊断时间极高，正是因为问题对搜索不可见。

## 战略应对

主要防御是**让依赖变显式**。每把一个隐式假设转成断言、类型约束或参数，就消除一个潜在的未知未知。强类型系统（Rust 所有权、可空引用类型、代数数据类型）的真正价值不仅仅是「帮你抓 bug」，更是**把隐式约定转成显式契约**。

[[information-hiding]] 同样有效：一个决策只存在于一处，第二处依赖就没有藏身之地。

## 相关

- 姊妹症状：[[change-amplification]]、[[cognitive-load]]
- 根源：[[obscurity]]、[[dependencies]]
- 对策：[[information-hiding]]、[[strategic-programming]]

## Sources

- [[sources/aposd-day02]]
