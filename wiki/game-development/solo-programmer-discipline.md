---
tags: [游戏开发, 工程哲学, 独立游戏, 小团队]
date: 2026-04-19
sources: 1
---

# 独行程序员的十条纪律

Swords & Soldiers 的 Wii 版是 Ronimo 的第一款主机游戏，全职程序员只有 [[joost-van-dongen|Joost van Dongen]] 一人，外加平均一名实习生。他在 2010 年 Festival of Games 的演讲里把生存经验压成了十条「瓷砖格言」（*tegeltjeswijsheden*，荷兰传统挂在墙上的箴言），主题是「只有一个程序员的团队该怎么分配精力」。这套原则不是 rocket science，但对初创工作室和学生项目特别契合。

## 十条

1. **最小可行版本先做完**。先让整套 loop 能跑，再加东西；别一开始就啃超出自己节奏的目标——**每个人都高估自己的编码速度**。
2. **不要替设计师调参**。走路速度、跳跃高度这些不是你的活。给设计师开个数据文件让他自己调（见 [[game-settings-hot-reload]]）。
3. **关卡工具要做但要最小**。重点在「能让关卡被设计出来」，不是「编辑器多漂亮」。Notepad 就是一个合格的关卡编辑器（[[level-design-without-editor]]）。
4. **代码一直保持干净**。哪怕赶 deadline 也别让它滑坡——代码一旦变 mess，之后加的每行也都是 mess。
5. **bug 立即修**。游戏自身 bug 越多，越分不清新加的功能是不是又坏了；反正早晚要修，现在修能保持开发可观测。
6. **不要追极致性能**。你不是在做 Uncharted 3；接受「有些机器跑不动」比把时间烧在优化上值得。
7. **不必照搬所有编程最佳实践**。自研内存管理器、杜绝运行时分配这类规则是给大项目的，小项目照搬只会拖慢自己。**做对自己有用的事**。
8. **让实习生做工具**。start-up 的实习生喜欢真实项目，把工具让他们做很合适，别不好意思。
9. **对几乎所有想法说「不」**。越接近 deadline 越要说不。游戏概念需要被保护住不被膨胀——真有时间再加。
10. **拉上美术和设计师一起做取舍**。问「我没时间做 A，B 或 C 能做，你要哪个？」——让他们参与决策比单方面说「no」能减少很多挫败感。

## 对解读的几点补充

- 这套纪律的共同精神是「**精力守恒**」：一个程序员的产能是有限常量，所有优化决策都在这个约束下做。把它和 [[tools-first-iteration-loop]]（工具优先于特性）、[[strategic-programming]] / [[tactical-programming]]（结构纪律）连起来看：小团队没有余粮做「未来可能用得上」的抽象。
- 「对想法说 no」和 Scope 控制是一回事；Joost 的做法是**把协作从单方否决升级为多选题**——设计师被拉进 triage 后不再把「做不了」当成程序员的傲慢。
- 「minimal tools」不是反工具链；是反「过度打磨工具反而吃掉开发时间」。Ronimo 本身还是把大量精力砸在 [[game-settings-hot-reload]] 这类**杠杆极高、实现极简**的工具上。

## 相关

- [[tools-first-iteration-loop]]
- [[indie-game-dev-rhythm]]
- [[pragmatic-performance-philosophy]]
- [[strategic-programming]]
- [[tactical-programming]]

## Sources

- [[sources/joostdevblog-lonely-programmer-tips]]
