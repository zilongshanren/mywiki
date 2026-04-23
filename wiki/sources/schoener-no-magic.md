---
tags: [source, software-design, debugging, mental-model]
date: 2026-04-19
sources: 1
---

# The No Magic Principle（Sebastian Schöner）

[[sebastian-schoener]] 于 2017 年 11 月发表的短篇信条文：**计算机里没有魔法**，由此推出几条针对学习、debug 和教学的推论。

## 摘要

作者把自己对编程的基本态度浓缩为一句：计算机里发生的一切都遵循可被理解、可被推理的规则，没有魔法可言。大多数日常开发可以舒服地停留在「数学化」的抽象层，但当你必须下钻到物理层（cache 一致性、clock rate）时，这个原则依旧成立——只是层次更深。作者列了五条推论：*You can build it*（看到的都是别人写出来的）、*Pick your fights*（想不出慢算法就别找快算法，看似不可能多半就是不可能）、*It's probably your fault*（99% 的 bug 是自己写的，不是 OS、硬件或库）、*Be rational*（debug 不能靠拉杠杆碰运气，建立理论并验证）、*You can understand it*（抽象可以下钻，"不能亲手编译的代码都值得怀疑"）。文章短、观点明确，读来像教学宣言。

## 关键要点

- **No magic** 是工程态度，不是算法
- 看似不可能 ≈ 确实不可能；除非给问题加限制（呼应 P/NP 的世界观）
- 把 bug 的根因找出来，不要靠"换个 flag 试试"这种祈祷式 debug
- 抽象层可选，但不要装作下层不存在
- 对不能亲手重建的工具链保持怀疑

## 链接到的概念

- [[no-magic-principle]]
- [[red-flags]]
- [[zero-tolerance]]
- [[strategic-programming]]
- [[computational-complexity-theory-intro]]

## 原文

- 链接：https://blog.s-schoener.com/2017-11-29-no-magic/
- 本地：`raw/articles/blog.s-schoener.com/2017-11-29_the-no-magic-principle-sebastian-schoner.md`
