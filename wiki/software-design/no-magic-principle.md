---
tags: [software-design, debugging, mental-model, first-principles]
date: 2026-04-19
sources: 1
---

# No Magic Principle

Sebastian Schöner 在 2017 年总结的一条个人信条：**计算机里没有魔法**。所有发生在机器内部的行为都遵循可以被理解、可以被推理的规则。大多数日常编程可以停留在这层「数学式」的抽象上，但当你不得不贴近物理实现时，这条原则也不应被放弃——只是层次更深了而已。

它本身不是一条算法，而是一种**debug 与学习时的姿态**，可以拆成几条推论：

- **You can build it.**——你看到的任何酷炫 shader、webapp、小功能，都是别人用同样可被理解的规则拼出来的，理论上你也可以拆解并重建。反过来：*If it is there, it must have been built*，每一个理所当然的 undo 系统、每一个 StarCraft 的小地图背后都是工程师一行行写出来的。
- **Pick your fights.**——如果你连一个「又慢又笨又蠢」的算法都想不出来，就别指望找到高效算法。看似不可能的事多半确实不可能，除非你能给问题加上合适的限制（类似 [[computational-complexity-theory-intro]] 的思路）。
- **It's probably your fault.**——程序崩溃 99% 的情况是你自己的 bug，不是 OS、不是硬件、不是 million-users 跑过的库函数。接受这一点是学会编程的必经之路。
- **Be rational.**——debug 时不要「拉杠杆碰运气」：*要不我把 flag 开一下？要不我把矩阵转置一下？*。既然系统无魔法，**崩溃必有因**，建立假设、验证、定位、修复，不要被人脑天生的巫术思维带偏。
- **You can understand it.**——抽象是有代价的，但底层永远可以下钻。作者的截断线是「物理域之前」：cache 一致性值得学，晶体管工作机制则不值（对应用工程师而言）。任何你不能大致亲手编译出来的代码，都应该被怀疑。

这条原则与 [[red-flags]]、[[zero-tolerance]]、[[strategic-programming]] 同族，都是在抵抗「靠直觉过日子」的工程反面。也和 Ousterhout 在 APoSD 里强调的**理解系统本身**一致：把复杂度当成可被拆解的对象而不是不可抗力。

## Sources

- [[sources/schoener-no-magic]]
