---
tags: [source, 游戏引擎, 软件设计, web工程, 编程语言]
date: 2026-04-27
sources: 1
---

# Engine Architecture, Web Engineering and Languages（Angelo Pesce / c0de517e）

[[angelo-pesce]] 发表于 2024 年 3 月的文章，论述游戏引擎工程师能从 web 工程领域学到什么，以及编程语言设计长期在错误粒度层面思考模块化问题。

## 摘要

Pesce 首先驳斥了游戏开发者鄙视 web 工程的习惯性姿态，指出才能与垃圾代码在任何领域都普遍存在，差距只来自需求压力与市场激励的不同。随后他从三个角度论述跨领域学习的价值：

第一，"拥抱糟糕代码"——任何为产品服务的代码都必须承担丑陋，工程质量的本质不是代码"完美"，而是让技术债处于可控位置、让"糟糕"不暴露在用户体验与长期可维护性上。第二，计算机科学的大多数核心原则与规模无关——磁带时代为存储优化设计的算法今天同样适用于 CPU 缓存；Hadoop 的 map/reduce 和 GPU 的数据并行如出一辙；REST 本质上是不可变数据结构加引用透明，SOAP 则可理解为 Actor 模型。第三，web 服务在模块化、热重载、API 设计、测试方面已经远超游戏引擎实践，因为它们天然运行在分布式机器上，隔离是物理强制的，不是设计选择。

最后他指出编程语言的主流范式都优先考虑"代码复用"而非"运行时隔离"，从根本上错过了控制复杂度的最有效手段——Erlang 的进程隔离模型是极少数例外。

## 关键要点

- 工程质量 = 管理技术债让它不暴露在终端，而非追求代码"完美"
- 计算机科学的核心规律与规模无关（磁带/缓存/GPU/分布式是同一套模式在不同尺度的投影）
- Web 服务因物理分布而天然拥有模块化、热重载、API 契约设计实践，游戏引擎应学习
- REST = 不可变数据结构 + 引用透明（缓存/记忆化的理论基础）；SOAP ≈ Actor 模型
- 大多数编程语言把"代码复用"置于"运行时隔离"之上，这是系统复杂度失控的根源
- Erlang 进程模型是目前极少数以运行时隔离为一等公民的语言设计

## 链接到的概念

- [[game-engine-web-engineering-lessons]]
- [[engine-evolution]]
- [[engine-layering]]
- [[peaked-technology]]
- [[data-driven-architecture]]

## 原文

- 链接：https://c0de517e.com/013_web.htm
- 本地：`raw/articles/c0de517e.com/2024-03-24_engine-architecture-web-engineering-and-languages-what-game.md`
