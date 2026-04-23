---
tags: [source, software-design, dependencies, tooling]
date: 2026-04-19
sources: 1
---

# Homework 2（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2010 年 3 月发的一则「给自己 / 读者的作业」：选一个小而隔离的系统（例如相机系统），列出依赖它的模块、它依赖的模块，然后用**依赖矩阵工具**（NDepend、Understand、Lattix、JDepend、Structure 101、DTangler、VS2010 Team System 等）把图画出来。接着**逐条审视**每条依赖：

- 能砍掉的砍掉（根本用不上）。
- 躲在清晰接口后面的（不依赖实现，不要求静态链接目标文件）也划掉。
- **剩下的，就是真正的问题**。

## 摘要

一篇短得像便签的动手练习，但论点锋利：如果你在一个**故意挑小、挑隔离**的系统上都能剩下一堆硬依赖，那整个代码库其他部分会糟到什么程度？编译和链接时间高、想推倒重写子系统却牵一发动全身，本质都是**坏依赖**的症状——Pesce 把这种情况形容为「长成无法切除的癌」。他建议把 DSM（Dependency Structure Matrix）工具纳入日常流程。

## 关键要点

- 挑**小而隔离**的系统做实验，因为它的依赖数量应该是下限。
- 两个角度都要看：**谁依赖我** + **我依赖谁**。
- 判定「坏依赖」的两条过滤：可删除的 / 藏在稳定接口后的都排除，剩下的才是真问题。
- 长编译 / 长链接 / 子系统难重写 = 依赖问题的可观测症状。
- 工具清单：NDepend（商业，.NET）、Understand（SciTools）、Lattix、JDepend、Structure 101、DTangler、VS2010 Team System、.NET Reflector。

## 链接到的概念

- [[dependencies]]
- [[dependency-checker-tool]]
- [[modular-design]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/03/homework-2.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-03-18_homework-2.md`
