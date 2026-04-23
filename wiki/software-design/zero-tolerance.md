---
tags: [软件设计, aposd, 哲学]
date: 2026-04-05
sources: 1
---

# 零容忍（Zero Tolerance）

**零容忍**是 Ousterhout 推荐用来减缓 [[complexity]] 增长的纪律：

> "In order to slow the growth of complexity, you must adopt a 'zero tolerance' philosophy."

因为 [[complexity]] 是以小增量的方式累积的——每次增量在局部都说得通——所以唯一有效的应对方式是每次出现时就拒绝它。如果容忍每次「小妥协」，复杂性指数增长；如果每次都付小修复成本，复杂性线性增长。

这不是完美主义，是**复利算术**应用在代码库上的结果。

## 拖延的滑坡

> "When you get in a crunch it will be tempting to put off cleanups until after the crunch is over. However, this is a slippery slope; after the current crunch there will almost certainly be another one, and another after that."

「crunch 之后」永远不会来。每次拖延的清理，都让下一次清理成本更高。最终重构成本会超过任何一个 sprint 的容量，债务变成结构性的。

## 和战略编程的关系

零容忍是 [[strategic-programming]] 的日常操作形态。10-20% 的设计投资配额让零容忍变得可负担：每个 PR 都带着一点预算去修当前面前的问题，而不是留给陌生人。

## 实操

- 工作中遇到设计问题时，修它而不是绕它。
- 看到小不一致、糟糕命名、重复常量时——现在就处理，即使这不在 ticket 描述里。
- 当 code review 暴露了一处异味时，把异味当成要交付的东西，而不是可选项。

## 相关
- [[strategic-programming]]——零容忍是它的操作化形式
- [[tactical-programming]]——零容忍要防范的对象
- [[complexity]]——被控制的目标
- [[warnings-as-errors-strategy]] — Bitsquid 对 warning 的治理：升格为 error 是主战术

## Sources

- [[sources/aposd-day03]]
