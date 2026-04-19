---
tags: [source, software-design, agent-coding, code-smell]
date: 2026-04-19
sources: 1
---

# Good Software Doesn't Double Check（Boris The Brave）

[[boris-the-brave]] 发表于 2026 年 4 月的文章，从自己在「vibe coding ↔ 精雕细琢」之间拉锯的体验出发，提出需要为 agent 辅助编程建立一套**新的代码气味清单**。

## 摘要

传统代码气味（code smell）是「快速识别典型代码问题」的工具，针对的是人的典型错误：思路混乱、结构不合理、技术债。但 agent 犯的错误和人类不同，最具代表性的一类是**过度防御式编程**——入口塞满冗长的类型/存在性检查。作者认为这是强化学习训练过程的副产物：代码跑通有奖励，但代码长度和质量基本不扣分，agent 因而学会了「多检查就稳」。他进一步论证这不是单纯的冗余，而是把「假设」在多处重复声明，**使假设之间随演化漂移**，最终在调用栈中部出现莫名其妙的失败（类 TOCTOU 问题）。作者列举同源的坏味道（ad-hoc 类型校验、无意义 try/catch、乘性 retry 等），并给出替代姿势：用严格静态类型 + 文档化不变量代替重复检查；一次建立，后续信任。

## 关键要点

- Agent 倾向写过度防御式代码，来源是 RL 的奖励信号不惩罚冗长。
- 重复检查 ≠ 更鲁棒，它制造了假设之间漂移的空间（代码版 TOCTOU）。
- 乘性 retry 会把跨服务故障暴露时间延迟一个数量级。
- 替代做法是把假设升级为类型系统或文档化的不变量，信任一次就够。
- 识别并压制「agent 时代的新气味」，是工程师在 agent 辅助开发中必须培养的新直觉。

## 链接到的概念

- [[good-software-no-double-check]]
- [[type-safety-vs-simplicity]]
- [[data-structure-invariants]]

## 原文

- 链接：https://www.boristhebrave.com/2026/04/17/good-software-doesnt-double-check/
- 本地：`raw/articles/boristhebrave.com/2026-04-17_good-software-doesnt-double-check.md`
