---
tags: [游戏引擎, 脚本系统, 数据导向, 可视化编程, bitsquid]
date: 2026-04-19
sources: 1
---

# Flow：可视化脚本的数据导向运行时

大多数引擎的节点图脚本（UE Blueprint、Unity Bolt、VisualScript 之类）都是拿"OO 节点树"直接跑——每个节点是一个堆分配的派生类实例，虚函数 `tick / execute` 逐个调用。对**关卡脚本级**（barrel 爆炸序列、level trigger、UI 交互）这种数量成千、逻辑琐碎但访问极频的场景，这套做法在内存、指针追逐和 cache miss 上都很不划算。

[[niklas-frykholm|Niklas Frykholm]] 在 Bitsquid 里把可视化脚本叫做 **Flow**，并坚持用**数据导向**的办法来做它的 runtime：一张 Flow graph 在 runtime 里是**一整块连续 blob** —— 节点数据顺序拼接，每个节点以 type id 开头；用 `switch(type_id)` 分派动作；节点之间的指针全部变成**相对 blob 起点的 offset**。

## 关键做法
- **Editor vs runtime 分离**：编辑器里 Flow 是 OO、可改版本、跨平台的 source 数据（JSON）；runtime 是 platform-specific、只读、编译产物。想改 runtime 格式？从 source 重编就行，不需要版本兼容。
- **Switch dispatch over virtual**：有人在评论区问"换成 jump table 如何"。作者承认 `switch` 在 release 里一般会编成跳转表，但 vtable 仍值得考虑——收益主要是代码整洁，不是性能。
- **单次分配 / 单次 memcpy / 单次 DMA**：因为 blob 里没有真指针，能直接 `memcpy` 拷贝、DMA 到 PS3 SPU、或落盘再读回，都不需要指针修补。
- **静态 blob + 动态 blob**：静态部分是多实例共享的"编译出的 graph"；动态部分（counter 节点的 int、碰撞事件的 actor 引用，即图里的 blue links）在 compile 时各节点就"预约"一个 offset。**实例化 = 克隆一份动态 blob**；死亡 = 整块 free，近似零成本 GC。
- **不 update，只事件驱动**：Flow 没有 per-frame tick——所有实时节奏都交给底层系统（AnimationPlayer / AnimationBlender / AnimationStateMachine），Flow 只在事件来时触发。
- **不多线程**：Flow 自己不算数，只是路由器。真正的重算在底层系统，那才是该多线程的地方。评论里有人问能不能把 Flow 推到 SPU，作者回答理论可以（让它生成动作消息列表）但不值得——PPU 消费消息的时间和直接执行 Flow 几乎一样。
- **分层分组与 query 节点（2011-05 Q&A 补充）**：Flow 支持 hierarchical grouping（把一组节点折叠进子图，像可视化脚本版的 LOD）与 copy-paste 复用（改动不会在副本间传播）。紫色 query 节点是**按需取值**的——比如 `Particle Effect.Create` 被触发时，连着它的 Position Query 才现场抓一次 unit 位置，避免每帧采样。编辑器可以开多个 tab 把功能按门/钥匙/电梯等关卡主题切开。

## 和 Bitsquid 其他设计的呼应

- 和 [[offset-based-resource-blobs|offset-based blob 资源]] 同构：都是"file format for memory"，runtime 数据的不变量是"可 memcpy、可落盘、可 DMA"。
- 和 [[static-hash-value-debug-assert|静态 hash]] 呼应：Flow → animation state machine 通信用 32-bit string hash 当事件名，比较是编译期常量。
- 和 [[lua-design-philosophy|Lua 分工]] 互补：Lua 给程序员写 gameplay，Flow 给美术/关卡做"挂特效和反应"——两者不是替代，是工作流分层。
- 和 [[data-driven-architecture|数据驱动架构]]一致：行为由 graph 数据而非硬编码决定；runtime 代码只是 `switch(type)` 的 ISA。

## Sources
- [[sources/bitsquid-visual-scripting-data-oriented]]
- [[sources/bitsquid-flow-followup-qa]]
