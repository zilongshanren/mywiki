---
tags: [软件设计, 编程心态, aposd, 组织]
date: 2026-04-05
sources: 1
---

# 战术龙卷风（Tactical Tornado）

Ousterhout 用来描述把 [[tactical-programming]] 发挥到极致的工程师的词：

> "Almost every software development organization has at least one developer who takes tactical programming to the extreme: a tactical tornado. The tactical tornado is a prolific programmer who pumps out code far faster than others but works in a totally tactical fashion."

## 管理视角的幻觉

战术龙卷风通常被视为明星：

- 交付特性速度惊人。
- 总能赶上 deadline。
- Sprint velocity 最高。

从短视野的管理视角看，他们是英雄。从代码库视角看，他们是负债：

> "Tactical tornadoes leave behind a wake of destruction. They are rarely considered heroes by the engineers who must work with their code in the future. Typically, other engineers must clean up the messes left behind by the tactical tornado, which makes it appear that those engineers (who are the real heroes) are making slower progress than the tactical tornado."

## 经济学

战术龙卷风的速度是**真实的**，但成本是**外部化的**——甩给其他工程师、甩给后续版本、甩给维护预算。如果衡量系统只看这周的吞吐量，龙卷风赢；如果衡量系统健康和总拥有成本，那些安静擦屁股的工程师才是真英雄。

## 游戏行业的温床

战术龙卷风在以下环境里如鱼得水：

- **原型到生产的漂移**——demo 代码一字不改地进了正式版。
- **Game Jam 文化**——速度被奖励，结构被推迟。
- **Crunch 周期**——里程碑前的速度胜过长期可维护性。

一个龙卷风可以三天做出一个漂亮的连击系统原型：输入缓冲硬编码、时间窗口写死在七个地方、特效用 `GameObject.Find("Effect_001")` 实时查找。Demo 很美。两个月后，没人能安全地加第 8 种连击。

## 不是道德问题

战术龙卷风模式是激励结构造成的。如果团队奖励特性数量而不是系统健康，龙卷风做的正是系统要求他做的事。要改变结果，就得改变被测量和被赞许的东西。

## 相关

- [[tactical-programming]]——基础心态
- [[strategic-programming]]——替代方案
- [[complexity]]——累积的成本

## Sources

- [[sources/aposd-day03]]
