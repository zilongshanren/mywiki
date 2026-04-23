---
tags: [vulkan, opengl, 图形API, 显式性能, 线程, 资源管理]
date: 2026-04-19
sources: 1
---

# Vulkan（glNext）的显式性能承诺

[[ben-supnik|Ben Supnik]] 2015 年 3 月听完 Khronos 的 glNext + SPIR-V 讲座后的立场帖。当时 API 还叫 glNext，不久后被定名为 Vulkan。他的标题自嘲："glNext 既不是 OpenGL，也不是 'next'"——它是**替换**，不是 OpenGL 的延续。

## 两条已知事实

- **不是 OpenGL 的增量扩展**。没有 API 兼容。替换，不是升级。
- **位于图形栈更低的一层**。显式暴露了过去驱动替你做的事——命令缓冲、同步、内存分配、descriptor。

这两点都意味着**驱动层代码变少**——而这恰恰是好事。OpenGL 结合 `ARB_compatibility` 加上所有最新扩展之后，API 面积 Kafka 式膨胀，"谁能把这个全写好"成为笑话。

## 三个核心卖点

### 1. 线程：OpenGL 无药可救

OpenGL 线程不友好**写在骨子里**，加扩展救不了：

- 队列、命令缓冲、线程——OpenGL 锁死 1:1 对应（context），想要别的结构没有；
- 驱动**替你做线程同步**，即使你不想它做——driver 内有锁，你无法禁用。

Supnik 拿 X-Plane 的 scenery tile 后台加载举例：加载线程在生产一块"thread-local"的数据，与渲染线程没有共享，应当 **lock-free**。插入世界时只有一次同步点——通过 message queue 在帧间由渲染线程做。**整条路径理应无锁**——但 OpenGL 驱动不知道，每次 `glBufferSubData` 都要问"是不是有人在用？"。Vulkan 的回答是："我是 app，信我"。安全检查被拿掉，快的是**不做的那部分**。

### 2. 显式性能（Explicit Performance）

OpenGL 是"write once, performance-tune everywhere"——你不知道快路径在哪，API 组合爆炸大到**文档化 fast path 在数学上不可能**（即使所有 IHV 能达成一致）。Supnik 的笑话：新手发个 "我把 refrigerator state 设成 GL_FROZEN_CUSTARD 然后 glDrawGizmo(GL_ICECREAM)，为什么卡"——他只能在旁边看着，想写篇博客说"这不能一起用"。

Vulkan 直接把这件事公开：**这些函数快、这些函数慢。要快路径就不要调慢路径**。开发者第一次能看到"驱动眼里什么贵什么便宜"。这和他前几个月写 [[iphone-4-opengl-es-perf-gap|iPhone 4 性能断崖]] 时抱怨的正是同一个根本问题——规范只说 API 做什么，不说多快——在 Vulkan 这里被直接解决。

### 3. Shim 策略：旧代码库的迁移路径

反直觉的观察：**因为 Vulkan 不是 OpenGL**，把旧 GL 代码迁过去可能**反而更容易**。理由是历史经验：X-Plane 从 GLES 1.1 → 2.0 时他写过 shim，最麻烦的不是新 API，而是两边的 API**名字相同但行为不同**。Vulkan 完全不是 OpenGL，可以直接写一个**基于 Vulkan 的 OpenGL 实现**；大型 legacy CAD / 游戏代码库照常跑在 shim 上，然后选择性地**从 shim 钻洞**到 Vulkan 原生路径做关键 hot path。两个额外好处：

- 驱动代码量降低 → 跨平台时 bug 是**同样的 bug**（原文："像圣诞节一样"）；
- 可以做**渐进式迁移**而不是整体重写。

## Vulkan 不适合所有人

他自己点名的几类人用 Vulkan 会疼：

- **3D 教学入门**——太低层；
- **觉得 GLES 2.0 已经太麻烦的手机游戏**——Vulkan 只会更麻烦；
- **一亿行 OpenGL 的 CAD 代码库**——需要的是那个关键扩展，不是 rewrite。

对他所属的"全职、小团队、自有引擎"类型开发者，迁移成本**真实存在**。最大的未知是**资源管理**：大引擎在主机上本来就在做自己的显式资源管理，挪过来很省；小团队的"资源管理"其实就是 OpenGL 驱动在替他们做——**猜得不一定好，但有得用**。

Metal 示范了"非可变对象 + 命令队列 + 命令 buffer"的世界，但 Metal 的资源管理简单到作弊——因为 **iOS 是 unified memory**，buffer object = 一个指针。PC 上 GPU 没那么简单。**写一个 AMD/NVIDIA 级别的 Vulkan 资源管理器对小团队是真正的挑战**——这是 Supnik 写作当时（2015 Q1）最大的 open question。

## 相关

- [[iphone-4-opengl-es-perf-gap]]
- [[graphics-api-history]]
- [[metal-api-overview]]
- [[ray-tracing-api-debate]]
- [[api-fast-path-design]]
- [[vbo-double-buffering-orphaning]]
- [[opengl-ext-vs-arb-fast-path-leak]]

## Sources

- [[sources/supnik-glnext-vulkan-discuss]]
