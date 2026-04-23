---
tags: [软件设计, 构建系统, 解耦, 工程流程, 团队协作]
date: 2026-04-19
sources: 1
---

# 「Build Failed」是个糟糕的术语——可降级构建

[[angelo-pesce|Pesce]] 2011 年的一条短文——《Do you have "failed builds"?》——对游戏行业的构建系统术语提出质疑：

> **一个 build「失败了」到底是什么意思？**整个 build catastrophically 崩了？连一个源文件都没编过？还是只有前端的一小段没过？还是一个美术资源烂了？这像说「这辆车坏了」却只是空调没反应。

这篇文章本身很短，几乎只是一个 provocation——但它指向的设计立场足够锋利，可以单列成页。

## 观察与主张

游戏是**复杂组件的集合**。如果音频系统编译失败——我们应该得到一个**没有音频但其它一切能跑**的 build；渲染挂了——禁用渲染，改用 debug 版（骨架 + 碰撞 mesh）；前端挂了——gameplay 侧工程师照样能跑、照样能 iterate。

**`broken build` / `game crashes` 是一种反模式术语**——把「某个子系统坏了」和「整个产品坏了」混为一谈，结果是：**一个子系统挂掉会锁死全团队**的 iteration。

口号：**Decouple, my friend.**

和 [[system-decoupling-patterns|Bitsquid 解耦四条]]、和 [[cpp-decoupling-over-details|C++ 活下来的关键是解耦]] 是同一条骨干原则的又一侧面——这次的切面是**构建与部署**。

## 评论区的反对与 Pesce 的回应

反对意见 #1：**「build failed」就是提醒大家停下来修问题**——你让它别叫了，你就永远不会修。

Pesce 的回应：**降级 != 无视**。某个子系统长期失败当然是问题，但「让正在修的人修，让不需要那块的人继续干活」并不矛盾。构建系统应该报**部件级状态**，而不是全 / 无。

反对意见 #2：「**依赖 bug**」——某人在「没有音频」版本上开发，等音频回来后才发现自己的改动和音频系统冲突——「昨天还行，今天就炸」。

Pesce 的回应：**那种 bug 是健康的 bug**。它们本来就存在，只是被「所有东西链在一起」掩盖了。让它们暴露出来 → 顺便暴露真正的 coupling 问题 → 修了它整个架构更健康。这条逻辑和 [[crash-on-unexpected-errors|崩溃比静默错误好]] 是同构的——**问题应当可见，而不是被盖住**。

反对意见 #3：「**那 build passed 还有什么意义？**没人能保证 clean checkout 跑得起来。」

Pesce 的回应：`build passed` 本来也不应当被当成「整个产品绿了」；它应当被理解为「每一个子系统各自绿了」。需要「整个 clean checkout 能跑」这种信息就另做一个 **integration check**。把两类问题分开，而不是塞进同一个灯。

## 工业落地的障碍与今天的样子

Pesce 没细说怎么落地，但暗示两点：

- **依赖关系必须在构建层级就声明清楚**——哪些组件是 optional、互相 fallback 方式是什么。
- **游戏引擎的模块化程度决定上限**——紧耦合（所有模块互相 include 头文件、互相持有指针）的 C++ 引擎想做这件事非常难。评论区有人提到 JRebel、Lisp / Erlang 的运行时热补丁——在应用层可行，C++ 层要付出巨额工程成本。

十几年后，这条主张的部分成果出现在：

- **Partial build / 模块化构建系统**（Bazel / Buck / 现代 CMake），能单独重建坏掉的 target 而不阻塞其余 target。
- **引擎的 optional subsystem** 设计（Unreal / Unity 的 plugin 系统、Bitsquid 的子系统隔离）——和 [[engine-plugin-c-abi-versioned-api]] 方向一致。
- **CI 的 matrix 报告**（各 target 单独亮灯）——现实落地的「部件级 build 状态」。

## 和《surviving C++》的关系

Pesce 在同月写的 [[cpp-decoupling-over-details]] 里把**可修改性**当作软件项目的唯一核心质量，并把模块边界视为实现路径。本文把同一条原则推到**构建与部署**层——如果你连一个子系统挂了都让全员停工，那就是耦合在组织流程上的外化。

## 备注

`2011-03-09_do-you-have-failed-builds-2.md` 与 `do-you-have-failed-builds.md`（如存在）是同一篇的重抓；URL 末尾编号差一位的归档冗余。

## 相关

- [[system-decoupling-patterns]]
- [[cpp-decoupling-over-details]]
- [[crash-on-unexpected-errors]]
- [[engine-plugin-c-abi-versioned-api]]
- [[ci-cost-optimization-asg]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-failed-builds]]
