---
tags: [游戏引擎, 渲染, 架构, gui, cloudwu]
date: 2026-04-19
sources: 1
---

# 立即模式 vs 保留模式

渲染和 UI 领域有一对长期对立又长期共存的范式：**立即模式（Immediate Mode）**与**保留模式（Retained Mode）**。它们的差别不在于"能不能画出同样的画面"，而在于**谁来维护画面背后的对象列表**。[[cloudwu]] 在梳理自研 gameplay 架构时把它作为表现层对接数据模型的关键选型。

## 立即模式

每一帧，调用方（表现层）遍历游戏数据模型里的 Object 列表，取出各自的当前状态，直接提交给渲染器。引擎不保留跨帧对象列表，所有东西每帧重新声明一遍。Dear ImGui 是 GUI 侧最有名的立即模式实现，绝大多数游戏引擎的主循环也近似走这条路径（从 CPU 侧看，`DrawMesh` 每帧都要被调一次）。

优点：**调用方和显示内容始终一致**（没有"忘记同步"这种 bug），实现简单，对动态场景友好。

缺点：没有跨帧缓存意味着每帧都在重复做一些本可以摊销的工作；对象列表庞大时 CPU 开销可能显著。

## 保留模式

表现层为数据模型里的每个 Object 创建一个长期存在的 visual object（可以是 1:1、也可以是 1:n），数据层每个 tick 记录状态变化，**只把变化推到表现层**。表现层按消息更新 visual object，再交给引擎渲染。Unity 的 GameObject 树、浏览器的 DOM、Qt/WPF 的 widget tree 都是保留模式的样子。

优点：跨帧复用、引擎能做脏矩形优化、对静态场景极其高效。

缺点：**两套状态需要同步**（数据模型 vs visual object），忘同步就是 bug；创建销毁的配对关系成为复杂度来源。

## 混合是常态

真实引擎往往按渲染对象类型混合：粒子、debug 线、GUI 用立即模式；场景 mesh、灯光、骨骼角色用保留模式。云风的建议是让数据模型代码保持"两种模式都能支持"的姿态——**数据模型不直接调渲染 API，也不直接持有 visual object**——这样换引擎或混用模式都不影响上层。

## 与 gameplay 分层的关系

在 [[gameplay-layering-object-actor|三层 gameplay 架构]] 中，表现层对接的方式依据引擎选型而定：

- 引擎走立即模式：每帧 visual 层读 Object 状态，提交渲染。
- 引擎走保留模式：visual 层维护 visual object 池，订阅数据模型的变更消息，按消息差分更新 visual object。

不管哪条路径，**数据模型自身不感知到渲染的存在**，这是 cloudwu 对"gameplay 与引擎解耦"的核心要求。反过来，渲染层可以读 Object，但不能改 Object——若有物理反馈、UI 反馈要修改游戏状态，必须包装成消息发给对应的 Actor。

## 相关
- [[gameplay-layering-object-actor]] — 本模式的主要使用场景
- [[scriptable-render-pipeline]]
- [[render-graph]]
- [[cloudwu]]
- [[dual-mode-gui-bitsquid]] — Bitsquid 用同一 API / 同一实现同时支持两种模式的做法

## Sources
- [[sources/cloudwu-gameplay-architecture]]
- [[sources/bitsquid-dual-mode-guis]]
