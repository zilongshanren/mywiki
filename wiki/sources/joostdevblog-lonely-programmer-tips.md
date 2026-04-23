---
tags: [source, game-development, 独立游戏, 工程哲学, 小团队]
date: 2026-04-19
sources: 1
---

# 10 Tips for the lonely programmer（Joost van Dongen，2011-02-10）

[[joost-van-dongen]] 2011 年 2 月的文章，基于他在 2010 年 4 月 Festival of Games 的一次演讲。Swords & Soldiers Wii 版开发时 Ronimo 只有他一个全职程序员（平均外加一名实习生），这十条是他给学生项目和初创小团队的生存箴言（荷兰语 *tegeltjeswijsheden*，瓷砖格言）。

## 摘要

十条核心纪律涵盖：**最小可行版本先做通**（所有人都高估自己的编码速度）、**不要替设计师调参**（给他一个配置文件）、**工具做最小但必须做**（Notepad 就是一个合格关卡编辑器）、**一直保持代码干净**（接近 deadline 也不能滑坡）、**bug 立刻修**（积压 bug 会污染新功能的可观测性）、**不追极致性能**（你不是在做 Uncharted 3）、**不盲从所有最佳实践**（自研内存管理器对小项目没意义，允许运行时分配）、**让实习生做工具**（别不好意思）、**对几乎所有想法说「不」**（靠近 deadline 尤其要说）、**拉设计师/美术进 triage**（把单方否决变多选题）。Joost 自认这套东西「不是 rocket science」，但对 young game-dev 公司和学生项目很有用。文后彩蛋：有读者以为这是「给程序员的恋爱建议」。

## 关键要点

- 「精力守恒」视角——一个程序员的产能是常量，所有优化都在这个约束下做。
- 工具链要做最小但不能不做（见 [[tools-first-iteration-loop]]）。
- bug 的成本随时间累积而非线性增长，**立即修**是省时间而非花时间。
- 「对想法说 no」不是傲慢，而是对游戏概念的保护；关键是**把否决变成对话**（「我没时间做 A，B 或 C 能做，你要哪个？」）。
- 「不必照搬所有编程最佳实践」是给小项目的校准：自研内存管理器、零分配等规则只有在规模够大时才值得。

## 链接到的概念

- [[solo-programmer-discipline]]
- [[tools-first-iteration-loop]]
- [[indie-game-dev-rhythm]]
- [[pragmatic-performance-philosophy]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/02/10-tips-for-lonely-programmer.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-02-10_10-tips-for-the-lonely-programmer.md`
