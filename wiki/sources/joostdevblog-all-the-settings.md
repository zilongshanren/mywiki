---
tags: [source, game-development, tools, designer-workflow]
date: 2026-04-19
sources: 1
---

# All the settings（Joost van Dongen，2010-12-11）

[[joost-van-dongen]] 2010 年 12 月的短文，讲 Ronimo 的「gameplay 数值统一集中、运行时 F5 热重载」这一套工具——Ronimo 内部认为这是他们做过最重要、却又最便宜的设计师工具。

## 摘要

Swords & Soldiers 里约 600 个 gameplay 数值（单位血量、售价、移速、武器射程……）全部写进一个纯文本设置文件。程序员负责定义字段，设计师负责调参。运行期间 alt+tab 回到文本改值、切回游戏按 F5，解析后直接覆盖内存里的 struct 字段；所有代码因为拿的是指针而不是值拷贝，下一帧就生效。实现成本极低，但是「设计师迭代速度」的杠杆极高。早年 De Blob 试过做游戏内 slider UI 来调参，在几百项规模下 slider 方案反而比纯文本更费劲，最后 Ronimo 把 slider 砍掉回归 Notepad。Proun 没做 F5 但做了「每关覆盖一组参数」，同一机制的变形用法。评论区指出 Unity 通过 C# 反射自动暴露 public 字段实现类似效果；HLSL UI annotation 能把 min/max 范围和分组写进数据。Joost 的结论很硬：**这套工具哪怕是学生项目也该第一天就做**。

## 关键要点

- 集中化的 struct + pointer 访问模式是关键纪律，**禁止拷贝字段**。
- 可调参数数量爆炸时，纯文本比 GUI slider 更耐扩展。
- Proun 把「每关覆盖一组参数」做成分层扩展，有助于关卡特化。
- 同样问题在 Unity / .NET 里用反射可以零代码做到，但纯文本方案在没有反射的 C++ 引擎里依然是最短路径。

## 链接到的概念

- [[game-settings-hot-reload]]
- [[binary-hot-reload]]
- [[tools-first-iteration-loop]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/12/all-settings.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-12-11_all-the-settings.md`
