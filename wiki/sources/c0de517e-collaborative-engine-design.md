---
tags: [source, game-engines, engine-architecture, community-design]
date: 2026-04-19
sources: 1
---

# Collaborative Design Experiment（C0DE517E / Angelo Pesce）

[[angelo-pesce]] 2010 年 3 月发起的一次 etherpad 协作实验，邀请读者共建一份「理想游戏引擎的分层清单」，最终结果更接近 Pesce 本人的视角（他自承「是个 tyrant」），但汇聚了 2010 年前后工业界对引擎架构的主流共识。

## 摘要

Pesce 在博客开了一个共享 etherpad，让读者协作列出「一个引擎该有哪些层、每层该解决什么问题」。几天后他总结收官，承认「在人群里设计东西不太可能成功」，但仍把结果完整贴回博客。清单以 **分层 + Why + Proposal** 三段式展开：从 Layer -1 的前置工程（编码规范、构建系统、静态检查、Code Review）一路爬到 Layer 3 用户库与外部工具链。核心主张包括：抛弃 C++ OOP、数据为王、用模块服务系统替代全局依赖、用反射数据库（解析 PDB）替代模板魔法、用 job 调度器而非裸线程、渲染层走 DX11 风格的无状态 command buffer、STL 不适合引擎接口。2010 年的时代指纹很明显：引用 Intel TBB / Apple Grand Central / C# Parallel FX 作为多线程参考，对 GC vs 引用计数的讨论仍在纠结。文末留下一个未解 dilemma：引擎数据该基于反射+序列化，还是基于参数数据库+特定文件格式。

## 关键要点

- **Layer -1 前置**：编码规范（"Fuck C++ OOP. Data is the king. Keep compile times low."）、CI、静态检查、版本控制、Code Review——把工程流程摆到架构之前。
- **Layer 0 语言扩展**：编译器抽象（内存对齐、强制内联、分支提示）、栈回溯、模块/服务系统（模块注册接口到全局 hashmap，声明依赖、失败即拒载）、COM-like 根对象用于 RTTI + 生命周期。
- **内存分配器**：薄接口 + 对第三方 C/C++ 分配的 override + 可配置池策略 + 线程专属池（但跨线程共享指针时复杂）。
- **对象生命周期**：推崇智能指针，在 GC 与 RC 之间犹豫——RC 会泄漏循环、跨线程析构要排队；GC 难写。提出 refcount 内嵌到类、AddRef/Release 虚函数供反射/脚本用，模板静态派发保证性能。
- **Layer 1 核心库**：job scheduler（依赖分 normal / data / data-parallel / buffered / streamed 五种语义，SPU 友好）、资源层（handle 化以支持 hotload）、反射系统（**解析 PDB 生成反射 DB** 的路线，避免宏/模板魔法）、数学库（SRT 类避免 skew、SIMD 对齐但标量逻辑仍走 FPU）、自建容器（STL 对齐不友好、不适合接口、难调试、与反射冲突）、全局参数系统（分 external / shared / thread / threadmessage 四类 section）。
- **Layer 2 渲染基建**：**DX11 风格的 rendering device abstraction**——无单状态直写、块上传、支持多设备与 command buffer 录制；stateless 或支持 state flush/invalidate；debug 渲染走 immediate-mode + lockless queue；effect 系统类似 D3DXEffect / CgFx。
- **Layer 3 用户库 + 外部工具**：脚本绑定由反射数据自动生成；反射 inspector、自动化测试作为外部工具。
- **未解的设计张力**：引擎数据层到底该统一走「反射+序列化」，还是分裂成「参数数据库（材质、属性） + 专用文件格式（mesh、texture）」——Pesce 说两者都得写代码，但这仍是一个需要在架构里下判断的决定。
- **社区反馈**：评论区有读者分享自己在 vapor3d.org 尝试实现类似目标。Pesce 承认「人群设计」失败，计划后续用更聚焦的题目（比如 codepad 竞赛）再试。

## 链接到的概念

- [[angelo-pesce]]
- [[engine-layering]]
- [[game-engine]]
- [[data-driven-architecture]]
- [[cpp-runtime-reflection]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/03/collaborative-design-experiment.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-03-14_collaborative-design-experiment-2.md`
