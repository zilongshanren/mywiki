---
tags: [软件设计, 编程心态, aposd]
date: 2026-04-05
sources: 1
---

# 战术编程（Tactical Programming）

**战术编程**是 Ousterhout 警告要避免的心态：

> "In the tactical approach, your main focus is to get something working, such as a new feature or a bug fix."
> 战术方式下，你的主要目标是让某样东西工作——一个新特性或一个 bug 修复。

目标听起来很合理：让东西工作不就是程序员的本职吗？问题出在视野的尺度：

> "The problem with tactical programming is that it is short-sighted."
> 战术编程的问题在于它是短视的。

战术程序员为当前任务优化。他们不会问「五个版本之后，这个设计还合理吗」，只会问「我怎么最快让这个 bug 消失」。

## 复利陷阱

每个战术决策在局部看都合理。临时 hardcode、多加一个参数绕过重构、用一个 flag 回避边缘情况……但：

> "Before long, some of the complexities will start causing problems, and you will begin to wish you hadn't taken those early shortcuts. But, you will tell yourself that it's more important to get the next feature working than to go back and refactor existing code."

重构永远在待办里，永远没有优先级。因为**在战术框架下，重构不产出功能，因此不产出价值**。每一次绕过都让下一次绕过更必要，[[complexity]] 开始复利增长。

## 不是个人问题，是系统激励

如果 KPI 是「每个 sprint 的特性数」，战术编程就是局部理性选择。解药通常不是「批判个人」，而是「改变被奖励的东西」。用外部指标衡量代码质量、让 review 严肃对待设计的团队，会自然漂移到 [[strategic-programming]]。

## 战略 vs 战术对照

| 维度 | 战术 | 战略 |
|---|---|---|
| 视野 | 当前 ticket | 月/年尺度的系统 |
| 目标 | 让它工作 | 一个优秀设计，恰好也能工作 |
| 遇到设计问题 | 绕过去 | 修掉它 |
| 生产力曲线 | 初期快，后期慢 | 初期慢，后期快 |

## 相关
- 极端形态：[[tactical-tornado]]
- 替代方案：[[strategic-programming]]
- 造成的陷阱：[[complexity]] 累积
- [[clean-code-critique]] — 游戏/图形视角下对 clean code 的系统批判
- [[vibe-coding-workflow]] — AI 辅助下的 tactical 循环

## Sources

- [[sources/aposd-day03]]
