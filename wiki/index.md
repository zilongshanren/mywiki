---
tags: [index]
date: 2026-04-05
sources: 7
---

# 知识库索引

本知识库目前聚焦两大主题：**软件设计哲学（A Philosophy of Software Design）** 与 **Unity 渲染/游戏引擎开发**。入口页：[[overview]]。

## 软件设计（wiki/software-design/）

核心概念与框架，源自 John Ousterhout 的 APoSD。

| 文章 | 一句话描述 |
|---|---|
| [[complexity]] | 复杂性的定义与整体框架，软件设计的核心敌人 |
| [[change-amplification]] | 复杂性症状之一：改动需要触及多处 |
| [[cognitive-load]] | 复杂性症状之二：需要知道太多东西 |
| [[unknown-unknowns]] | 复杂性症状之三：不知道自己不知道（最危险） |
| [[dependencies]] | 复杂性根源之一：代码间的相互牵连 |
| [[obscurity]] | 复杂性根源之二：重要信息不显而易见 |
| [[red-flags]] | 识别设计问题的信号集合 |
| [[tactical-programming]] | 短视的「让它工作」心态 |
| [[strategic-programming]] | 投资心态，优秀设计恰好也能工作 |
| [[tactical-tornado]] | 外部化成本的高产出工程师 |
| [[zero-tolerance]] | 对复杂性增量的日常纪律 |
| [[continuous-design]] | 软件设计是持续过程，不是一次性活动 |
| [[modular-design]] | 模块化的真正目标是认知隔离 |
| [[deep-modules]] | 强大功能 + 简单接口的设计理想 |
| [[shallow-modules]] | 接口复杂度接近实现复杂度的反模式 |
| [[classitis]] | 「类越多越好」的系统性设计疾病 |
| [[interface-vs-implementation]] | 接口是成本，功能是收益 |
| [[abstraction]] | 省略不重要细节的简化视图 |
| [[false-abstraction]] | 省略了重要细节的「简洁」陷阱 |
| [[information-hiding]] | 把设计决策藏进实现——深模块的引擎 |
| [[information-leakage]] | 同一份知识分散在多个模块 |
| [[temporal-decomposition]] | 按时间顺序切模块的陷阱 |

## 经典案例（wiki/examples/）

APoSD 中反复出现的标杆与反面案例。

| 文章 | 一句话描述 |
|---|---|
| [[unix-io]] | 5 个系统调用隐藏几十万行实现的深模块标杆 |
| [[java-io]] | 三件套 + 显式 buffering 的 classitis 病例 |
| [[garbage-collector]] | 接口为零的极限深模块 |

## 游戏开发（wiki/game-development/）

APoSD 框架在 Unity/游戏引擎开发中的应用。

| 文章 | 一句话描述 |
|---|---|
| [[unity-complexity-patterns]] | Unity 项目中的复杂性典型模式 |
| [[classitis-in-games]] | Manager 癌症与事件系统滥用 |
| [[resource-system-design]] | 资源系统的信息隐藏战场 |
| [[ecs]] | ECS 作为深模块与显式依赖的案例 |
| [[rendering-api-depth]] | 渲染 API 的浅 vs 深对照 |

## 渲染（wiki/rendering/）

Unity SRP 相关概念，主要来自 Custom SRP 6.1.0 教程。

| 文章 | 一句话描述 |
|---|---|
| [[custom-srp]] | Catlike Coding 的 Custom SRP 教程系列 |
| [[scriptable-render-pipeline]] | Unity 的可编程渲染管线概念 |
| [[render-graph]] | SRP 的声明式渲染编排系统 |
| [[color-lut]] | 用于 color grading 的查找纹理 |
| [[debug-visualization]] | Rendering Debugger 集成方式 |

## 人物（wiki/people/）

| 文章 | 一句话描述 |
|---|---|
| [[john-ousterhout]] | APoSD 作者，斯坦福 CS 教授 |
| [[jasper-flick]] | Catlike Coding 作者，Unity 教程作者 |

## 源摘要（wiki/sources/）

| 源 | 一句话描述 |
|---|---|
| [[sources/custom-srp-6-1-0]] | Custom SRP 6.1.0 教程摘要 |
| [[sources/aposd-day01]] | APoSD Day 1：Introduction |
| [[sources/aposd-day02]] | APoSD Day 2：复杂性的定义与症状 |
| [[sources/aposd-day03]] | APoSD Day 3：战术 vs 战略编程 |
| [[sources/aposd-day04]] | APoSD Day 4：深模块 |
| [[sources/aposd-day05]] | APoSD Day 5：浅模块之罪与 Classitis |
| [[sources/aposd-day06]] | APoSD Day 6：信息隐藏 |

## 特殊页面

- [[overview]] —— 综合叙事：把主题串起来
- [[log]] —— 所有操作的时间顺序记录
