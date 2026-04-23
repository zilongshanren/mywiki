---
tags: [source, 构建系统, 解耦, 工程流程]
date: 2026-04-19
sources: 1
---

# Do You Have "Failed Builds"?（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2011 年 3 月的一篇极短 provocation——一页纸不到——对「build failed / game crashed」这类术语本身提出质疑。

## 摘要

Pesce 抛出一个反问：**一个 build「失败了」到底是什么意思？**整个产品编不出来？只有前端挂了？只有一张美术资源烂了？他把这类用法类比为「这辆车坏了——但其实只是空调」。

接下来是口号：**禁用「broken build」「game crashes」概念**。音频挂了——得到无音频但其余可跑的 build；渲染挂了——禁渲染、用 debug 模式跑骨架 + 碰撞 mesh 继续 iterate；前端挂了——gameplay 团队照常工作。

一句话主张：**Decouple, my friend.**

评论区长篇辩论（Pesce 亲自回应）：

- 「build failed 就是让你停下来修的」→ Pesce：**让需要修的人修，让不需要的人继续做事**，两件事不矛盾。
- 「依赖 bug 怎么办，昨天能跑今天炸」→ **那种 bug 是健康的 bug**，暴露了真实的耦合问题，修了让架构更健康。
- 「那 build passed 还有意义吗」→ 它应被理解为「各子系统各自绿」，而不是「clean checkout 就能跑整个产品」。需要那种信息另做 integration check。
- 「游戏引擎性能太紧耦合做不到」→ 确实难，但方向是对的；JRebel、Lisp / Erlang 的 runtime patching 是应用层参考，C++ 层要付出更高工程成本。

## 关键要点

- **术语会驱动设计选择**——「build failed」这种粗粒度状态会内生地强化系统耦合。
- **可降级构建 / partial build** 是去掉全员阻塞的关键——后来 Bazel / Buck / Unreal 的 optional subsystem / plugin 系统一定程度上落地了这条思路。
- **「让 bug 暴露」vs「让 bug 被盖住」**——和 [[crash-on-unexpected-errors]] 的「崩溃好过静默错误」是同构主张。
- **和 Pesce 同月《Surviving C++》的核心原则同构**——软件质量 = 可修改性 = 解耦面；这一篇把原则推到构建与部署层。
- 归档命名 `-2.md` 是对同一篇 URL 的重抓冗余——两份应视同一篇。

## 链接到的概念

- [[component-degradable-build]]
- [[system-decoupling-patterns]]
- [[cpp-decoupling-over-details]]
- [[crash-on-unexpected-errors]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/03/do-you-have-failed-builds.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-03-09_do-you-have-failed-builds-2.md`

## 备注

文件名 `do-you-have-failed-builds-2.md` 的 `-2` 是归档系统对同一 URL 的去重计数；2011-03-09 原文只有这一篇，并非续作。
