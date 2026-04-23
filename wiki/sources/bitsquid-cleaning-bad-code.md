---
tags: [source, bitsquid, refactoring, legacy-code, yagni]
date: 2026-04-19
sources: 1
---

# Cleaning bad code — bitsquid: development blog

[[niklas-frykholm|Niklas Frykholm]] 2012 年 8 月的一篇重构实操清单——九条（0 到 8）加一个收尾"9. That is all"，把"如何清理继承来的烂代码"写成一本小手册。

## 摘要

第一条（第 0 条）最重要：**先决定清不清**。要么认领它、彻底清干净；要么当成"别人的"、只做最小改动。骑墙最糟。判断因子：改动频次、是否要跟上游、工作量（每天 100~10000 行，取 1000 估算）、是否核心功能、到底多烂。认领后的纪律：(1) 先拿到测试（unit 最好、不行用 integration），发现漏网就补入测试。(2) 用好 source control；公司系统太烂就本地 hg/git 仓库套一层。(3) 一次只改一小步——想顺手重构 API 就先别，等继承链拆完。(4) 不要一边清一边加功能——方向相反。(5) 砍未使用的功能——它在历史里。(6) 删大多数注释——多数是 pointless / incomprehensible / sowing FUD / downright lying；dead code 也删，refactor 后老注释多半错。好代码靠清晰命名、小函数、assert 文档化自己。(7) 干掉 shared mutable state——全局变量、对象大口袋、megafunction 的局部变量、非 const 指针参数，都是；切手段：拆函数拆对象、成员 private、方法 const 或 static、尽量纯函数、加 const。(8) 干掉不必要复杂度——YAGNI，去除序列化 / 虚接口 / 工厂 / visitor 等"骨架比实现还厚"的过度工程。

## 关键要点

- "karate do yes / karate do no"——清理代码没有中间态度。
- 改良派（reform）优于革命派（revolution），但承认有时候 rewrite 确实必要。
- 一天清 ~1000 行，按此估算时间。
- 测试不必每次改都跑；每 5 commit 一次 + revert 二分。
- 改动最小化 + 频繁 commit 是所有纪律的肌肉。
- shared mutable state 是理解代码最大的障碍，不是并发本身。
- 过度工程通常来自"设计模式崇拜"，结果反而不适应真实变化。

## 链接到的概念

- [[cleaning-bad-code]]
- [[tactical-programming]]
- [[strategic-programming]]
- [[clean-code-critique]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/08/cleaning-bad-code.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-08-18_cleaning-bad-code.md`
