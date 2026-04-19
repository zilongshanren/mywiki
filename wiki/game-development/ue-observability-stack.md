---
tags: [ue, unreal, 物理, 调试, 工具, 观测性]
date: 2026-04-19
sources: 1
---

# UE 里的可观测性工具栈

[[thomas-poulet]] 在 [[sources/thomas-poulet-physics-tools-ue5|The tools we use to develop our physics game in UE5]] 里整理了他团队做物理驱动游戏时，沿着「观测性（observability）」这条轴一路升级的五种 UE 工具。主张是：**物理角色控制器的调优痛感来自输入多、内部状态多、耦合深——解药不是更好的模型，而是把系统内部状态最大程度地暴露给设计师，让他们能无需打扰工程师就自行迭代。**

| 工具 | 开箱程度 | 最适合的数据 | 实时/历史 | 接入层 |
|---|---|---|---|---|
| On-screen logging (`AddOnScreenDebugMessage` / BP `Print String`) | 立刻 | 偶发事件、低频值 | 实时 | Blueprint + C++ |
| Gameplay Debugger (GDT) | 需要 C++ 配 PreDefault 模块 | 中频变量，分类切换 | 实时 | C++ |
| Visual Logger | 中等接入 | 历史时序、空间可视化 | 历史 | C++ |
| ImGui plugin | 自由 | 任意，但工程量大 | 任意 | C++ |
| 自研 Ariadne | 高前期建设 | 全量、跨 session | 实时 + 历史 | Blueprint + C++ |

## 1. On-Screen Debug Message

最轻量。关键**小心：要用 *unique key*** 才能让消息固定替换而不是叠加：Poulet 团队按 `(ModuleKey << 32) | ValueKey` 构造，ModuleKey 一个模块一个、ValueKey 一个值一个，能避开跨模块撞 key。shipping build 下宏隔离。

BP 版本叫 `Print String`，连一下就能跑。

## 2. Gameplay Debugger Tool (GDT)

Epic 的分类层叠调试器，像 Photoshop 的图层——Epic 自己占了几类，剩下 **93 类留给项目**。按 `'` 键呼出，可以独立打开/关闭每一类。
接入需要 `PreDefault` 阶段加载的模块（如果游戏模块在 `PostConfigInit` 因为自定义 shader 需要晚加载，就必须另起一个 debug 模块），`Build.cs` 里 `SetupGameplayDebuggerSupport(Target)`，然后写 `FGameplayDebuggerCategory` 的子类实现 `CollectData` / `DrawData`。还能挂一个 `FDebugRenderSceneProxy` 在 viewport 里画 3D 可视化（箭头、框等），以及自定义 keyboard shortcut 给这一 category。

## 3. Visual Logger

历史录制 + 回放。actor 继承 `IVisualLoggerDebugSnapshotInterface`，覆盖 `GrabDebugSnapshot` 就能被自动抓快照。提供 `UE_VLOG_*` 宏（文本、线段、箭头、直方图）。

痛点：只能在主 viewport 里显示、图表的时间窗上限 0.5s、API 只支持 C++、高频数据不好看。

## 4. ImGui

Poulet 团队用 [Network ImGui plugin](https://github.com/sammyfreg/netImgui) 远程（从目标设备推回 PC）显示 ImGui 窗口，远程调试 console 游戏时很香。但**每个变量都要手工从 actor 里拿出来、每种可视化都要手写 C++** —— 工程师瓶颈拖慢设计师，最终不够好。

## 5. Ariadne（自研）

问题模型：工程团队介入成本高是铁律。Poulet 设计 Ariadne 的出发点是**把工程师从回路里拿掉**：
- 一台 server 接收所有开发会话的数据
- actor 只要打一个 tag，**所有属性自动被反射上报**，不需要再逐个变量接入
- 前端接 Grafana —— 一个工业标准的 observability dashboard，设计师 WYSIWYG 拖面板，自己搭 bug 专属 dashboard
- 附带自定义面板（地图、矢量视图）用于游戏场景

每次游戏都录、每个变量都存。工程师做一次基础接入后就从 observability 回路里退出。他们甚至拿 Ariadne 做 Forza 的比赛实况分析。目前内部工具，有 [mailing list](http://mightyariadne.substack.com) 招试用。

## 启示

Poulet 归纳的挑选依据：**rate of change / data type / update frequency / live-or-historical**。五档工具不是替代关系，是按场景选的光谱——on-screen 处理事件，GDT 处理分类变量，Visual Logger 处理历史时序，Ariadne 处理跨 session 的大规模录制。

相关：[[unreal-insights-counters-traces]] 做的是性能 / trace 的另一种观测性；[[runtime-editor-console-connection]] 解决另一种「拿到游戏内部状态」的问题。

## Sources

- [[sources/thomas-poulet-physics-tools-ue5]]
