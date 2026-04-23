---
tags: [游戏开发, 工具链, 热重载, 迭代速度, 引擎架构]
date: 2026-04-19
sources: 1
---

# 实时编辑方案分类（Pesce 2010 poll）

2010 年 4 月 [[angelo-pesce]] 在博客上发起一个小投票，问工业界开发者的游戏 / 引擎到底用哪种 live-editing。75 人答题，结果在 5 月公布。这张分类表不是学术划分，而是**站在图形程序员视角的吐槽版图谱**——每一档都附带「它解决了什么、留下了什么痛」。放在今天看，它仍然是一份理解「[[tools-first-iteration-loop|为什么工具优先]]」的精练坐标系。

## 八档阶梯（从最糟到最理想）

- **None（16%）**——每次改贴图 / shader 都要重启游戏。Pesce 的原话：「活在持续的痛苦里，没法解 bug、没法优化、注定完蛋。」
- **File hot-swapping（41%）**——贴图、mesh、也许 shader 可以热换。门槛低，只要文件系统集中管理资源、对象用 handle 而非指针就能做到。但**代码一改仍然要重来**，渲染工程师写完 shader 回到 C++ 就崩溃。不好导航场景、不好选对象、不好调参，而且主机内存碎片化下反复 reload 还会崩。
- **Script hot-swapping（41%）**——同上，但多了一套脚本（多半是 Lua），脚本文件也能换。
- **Tools partially replicating game functions（29%）**——shader editor / animation editor 这类独立工具。**反向陷阱**：它不解决原问题，反而创造一个平行的「好用但不是游戏」的环境，导致同一功能要写两份，艺术家在工具里爽、回到游戏里依然慢。
- **Tool + RPC live-update（21%）**——在上一档基础上加网络通道把改动推给运行中的游戏。与 [[runtime-editor-console-connection]] 是同一思路。
- **Engine-embedded-in-tool（18%）**——把游戏编译成 DLL / 静态库嵌入一个 PC 编辑器，编辑器提供 windowing、反射、调试服务。缺点：在 **PC** 上看，不是在**目标平台**上看；还要维护 PC 构建；代码迭代依然是 C++ 痛苦循环。
- **Tool ↔ Game via reflection / RPC（9%）**——编辑器用好语言（C#/脚本）写，通过反射把编辑动作发给主机游戏，鼠标输入也 forward 过去。Pesce 说这是「精英档」。
- **Pure in-game on-platform editing（10%）**——整个编辑器和游戏一起编进 build 里跑在主机上。主机内存是最大敌人。
- **Code hot-swapping（9%）**——关心「我们自己」的迭代速度。Pesce 的评价：「这一档拥有了它，其他一切都不重要。」

## Pesce 的结论

- **File-swap 最普及**（41%），因为最便宜最好写。
- **外部工具很多**（29% + 21%），但和游戏的耦合度参差。
- **真正关心 code iteration 的人极少**（9%），这是博客作者的主要吐槽点。
- 评论区也有读者反驳「194% 合计」是数学错——Pesce 回复指出 overlapping 和 mutually exclusive 不是对立面，poll 允许多选。

## Code hot-swap 的工程要点

评论里 Nicolas 问「代码热重载怎么做」，Pesce 给了一份**简短设计清单**，这份 checklist 在 16 年后仍然成立：

- 理论上 reload DLL 就行，技术本身不复杂。
- **实际问题是设计**：必须**从引擎立项起就把热重载当目标**，中途加几乎不可能。
- 需要条件：**模块有清晰接口、无静态 / 运行时隐式依赖**（参见 [[dependencies]]）。
- 必须能**序列化 / 反序列化模块状态**——流程是 serialize → unload → load → deserialize。
- **不要跨模块共享对象**，尤其是有 vtable 的非 POD——reload 后 vtable 地址会换。

这份清单与 [[binary-hot-reload]] 的设计约束几乎完全吻合。

## 为什么这张表值得保存

八档阶梯的价值不在于分类本身，而在于**每一档都标注了它遗留的痛**。这让今天的工程师评估自己项目的工具链时，能定位自己在哪一档、下一步要补哪个缺口——而不是在「我们有热重载」这个笼统答案里自满。_The Witcher 2_ 的 [[runtime-editor-console-connection]] 对应第 5–6 档之间，[[tools-first-iteration-loop|Evan Todd 的 tools-first]] 论证则贯穿整张表。

## 相关
- [[runtime-editor-console-connection]]
- [[tools-first-iteration-loop]]
- [[binary-hot-reload]]
- [[csharp-runtime-script-compilation]]
- [[decoupled-tool-engine-json-rpc]]
- [[dependencies]]
- [[angelo-pesce]]
- [[javascript-hot-reload-dom-script]] —— Niklas 用 30 行 JS 做出的 code hot-swap 最小实现

## Sources

- [[sources/c0de517e-live-editing-poll-results]]
