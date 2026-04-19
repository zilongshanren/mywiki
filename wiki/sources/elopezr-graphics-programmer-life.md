---
tags: [source, software-design, graphics, career, cpp]
date: 2026-04-19
sources: 1
---

# Life and Death of a Graphics Programmer（Emilio López Ros）

[[emilio-lopez-ros]] 2024 年 5 月的意见长文。他写自己十多年图形程序员的日常——编译时间、模板陷阱、shader 爆炸、heap 碎片、虚函数、debug build、STL、工具、codebase 考古——其中几乎每一段都能直接拍在 *clean code* 信徒脸上。不谈炫酷渲染算法，只谈「为什么游戏引擎和银行后台用的是两种 C++」。

## 摘要

文章按主题分段。**硬需求**：游戏在平民硬件上 16 ms/帧塞进 I/O、网络、音频、物理、寻路、输入、渲染——**性能是正确性的一部分**。对比之下字处理器、浏览器是事件驱动、延迟宽松；HFT、航空软件有正确性硬约束但域窄。

**等编译器**：AAA 引擎全量 rebuild 10–40 分钟，shader 全量 rebuild 能到小时级；作者列举包括 C 头文件传递包含、Unity/PCH/incredibuild 等缓解手段都只是治标。

**模板与混乱**：他承认自己也曾过度用模板，但模板代码难读难调、编译慢、RTTI 与 SFINAE 难掌握；他亲眼见过 shader reflection 用 template magic 写到没人能 debug 的案例，反省后认为那种地方用**代码生成**更好。

**shader 爆炸**：从 DOOM 2016 的几百个 shader 到典型 UE 项目的一万个，取决于谁被允许写 shader（仅程序员 vs 全体艺术家）。作者顺便带出 PSO 编译和 `#stutterstruggle` 的来龙去脉。

**heap 与虚函数**：每帧分配 per-frame command / particle 会撕碎内存；游戏用 arena / pool / stack 替代。虚函数的问题不在 vtable 几条指令，而在数据布局被迫打散；文章给出「per-type 容器 + 批处理」的 DOD 演进三步。

**clean code 批判**：他直接点名 `std::transform` 比手写循环在 debug build 慢 57%、release 等价但更难读；他的立场是 code is a **tool not a painting**，命名、评论、一致性远比花式 STL 调用重要。

**debug build matters**：优化过度的 debug build 会逼程序员不用 debug build，这是自戕。放宽 inline、deep call stack、多层 accessor 来换 debug 速度通常值得。

**STL 抱怨**：编译慢、容器都堆分配、SSO 不标准、更新绑 C++ 版本、跨平台行为不一致——这是为什么 EASTL、游戏厂自研容器长期存在。

**工具**：VS 曾经领先所有人 20 年，现在在万行工程上卡顿；图形 debugger RenderDoc/PIX/NSight/Radeon 各有所长，没有一个覆盖全部；美术用的工具（烘焙、LOD、navmesh）同样关键，不该为了代码「干净」让它们跑一小时。

**考古**：熟悉新 codebase 是查找、符号搜索、书签、perforce/git time-lapse 的组合艺术。

## 关键要点

- 性能不是图形程序员的 nice-to-have，而是**职责的一部分**——这是游戏/嵌入式 vs 其它行业的根本分水岭。
- 过度 clean code（大量小函数、templated STL 算法、深继承）在 **debug build 代价** 非线性。
- **data-oriented design** 不是选择题——heap 分配、vtable、per-object 循环在大规模粒子/实体循环里是真的瓶颈。
- 工具友好度（美术的 UI、debug build 可用性、编辑器响应）是「对队友是否诚实」的一把尺子。

## 链接到的概念

- [[graphics-programmer-constraints]]
- [[shader-permutation-explosion]]
- [[clean-code-critique]]
- [[aos-vs-soa]]
- [[cache-friendliness]]

## 原文

- 链接：https://www.elopezr.com/life-and-death-of-a-graphics-programmer/
- 本地：`raw/articles/elopezr.com/2024-05-16_life-and-death-of-a-graphics-programmer.md`
