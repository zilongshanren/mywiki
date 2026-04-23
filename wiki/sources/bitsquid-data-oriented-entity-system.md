---
tags: [source, 游戏引擎, ecs, entity-system, transform, soa, bitsquid]
date: 2026-04-19
sources: 3
---

# Building a Data-Oriented Entity System, Part 1–3（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2014 年 8 月 27 日到 10 月 3 日连载的三篇文章，是同时代最完整的公开 [[ecs|ECS]] 落地笔记。本条 source 合并 Part 1（EntityManager）、Part 2（Component Managers）、Part 3（Transform Component）——它们逻辑上是一个整体。

## 摘要

Bitsquid 原本没有 component 架构，因为 gameplay 都在 [[lua-runtime-dynamism-tricks|Lua]] 里——深继承的痛苦被脚本层消化掉了。真正逼出 ECS 的是 [[engine-plugin-c-abi-versioned-api|plugin 系统]]：C++ plugin 要动态给 entity 加能力，component 是最自然的装配单位。

**Part 1**：`Entity` 就是一个 32 位整数（22 index + 8 generation，被 Lua light userdata 的 2-tag 约束到 30 bit 有效宽度）。`EntityManager` 只持 `Array<unsigned char> _generation` 和 `Deque<unsigned> _free_indices`——`alive()` O(1)。generation 防 id 回绕靠 `MINIMUM_FREE_INDICES = 1024` 缓冲，要复用同一个 id 至少需要 256 × 1024 ≈ 260 k 次创建销毁。

**Part 2**：**没有 Component 基类**，每类 component 由 `ComponentManager` 集中管理，manager 决定布局。默认 **SoA**——每字段一条数组。但不是 5 次 `Array<T>` allocation，而是**一次 allocate 一个大 buffer，五个指针分指不同偏移**，对 allocator / cache / debugger 都友好。Entity → Instance 的映射用 `HashMap<Entity, unsigned>`。`Instance { int i; }` wrap 一下让类型系统帮忙分清 entity 和 instance。删除走 swap-erase 保持数据紧密。Entity 死亡的 component 清理分两档：持外部资源的注册 destruction callback 立刻清，轻量 component 走**惰性 GC**（每帧随机采样 4 个，连续 4 个活着就停）。SoA vs AoS 的回应很关键——simulate 只碰 vel/pos/acc 时 SoA 省 18.2% cache 空间，memory-bound 就是 18.2% 性能；AoS 只在几乎碰所有字段时才略胜。

**Part 3**：`TransformComponent` 掌管 entity scene graph（child entity 跟 parent entity 动）。**不强制每个 entity 都有 transform**——纯逻辑 entity 不配坐标。Bitsquid 没有全局 world，每个 World 有自己的一套 component manager，同一 entity 可以在多个 world 有不同 transform。**关键决策：entity scene graph 与 model scene graph 解耦**——model 只算相对 entity 的局部姿态，两张图可独立并行。**immediate 更新**（改 local 立刻算 world 及子孙）而非 deferred，理由是 entity 层 chain 短（≤ 5）、少整条同时动，O(n²) 坏场景罕见，**世界坐标永远准确值多付一点 CPU**。deferred 也给出两条工程优化：dirty 段搬到数组尾部扫描、数组按 parent-before-child 排序让一遍 for 循环就正确。swap 时用 `[size]` 当中转三步法避免引用改写时走链表纠缠。

这份设计里后来能在 DOTS / bgfx / Our Machinery 的演进中看到对应的每一条：entity=id、manager 拥布局、SoA 默认、惰性 GC、handle+generation 防悬垂、两张 scene graph 分离、immediate/deferred 取舍、dirty 末端排序。

## 关键要点

### Part 1 — EntityManager
- `Entity` = 30 位 id = 22 index + 8 generation（Lua light userdata 约束）
- `EntityManager._generation` 数组 + `_free_indices` FIFO 队列
- `MINIMUM_FREE_INDICES = 1024`——id 要复用需 256×1024 次创建销毁
- `alive(e)` 就是 `_generation[e.index()] == e.generation()`，O(1) 且 8 bit/entity
- weak reference 必须走 alive 检查——避免强引用的销毁广播

### Part 2 — Components
- **没有 Component 基类**，每类由 ComponentManager 拥有
- Entity 不知道自己有哪些 component——manager 说了算
- SoA 为默认：**单次大 allocation + 多指针 alias**，不要 5 条 `Array<T>`
- Entity → Instance 走 `HashMap<Entity, unsigned>`（除非 component 几乎全 entity 有）
- `Instance { int i; }` wrap 一下让类型系统分清 entity / instance
- 删除走 **swap-erase** 保持紧密
- 两档 component 销毁：destruction callback（紧急）+ 惰性 GC（每帧采样 4）
- **SoA 18.2% 优势**：simulate 只用 vel/pos/acc 时可以不加载 mass/entity
- 作者讨厌 `update()` 这个名字——inheritance-based 的坏习惯

### Part 3 — Transform
- 不强制每 entity 有 transform——纯逻辑 entity 可以没坐标
- 多 World 架构：同一 entity 在多个 world 有不同 transform
- **entity scene graph 与 model scene graph 解耦**——并行化前提
- **immediate 优于 deferred**：chain 短、O(n²) 罕见、世界坐标永远准确
- deferred 优化：dirty 段集中末端 + parent-before-child 排序
- swap 三步法：`[size]←[A]; [A]←[B]; [B]←[size]`，每步被搬者无引用

## 链接到的概念

- [[bitsquid-data-oriented-entity-system]]
- [[ecs]]
- [[engine-plugin-c-abi-versioned-api]]
- [[component-entity-data-binding]]
- [[aos-vs-soa]]
- [[id-lookup-table-packed]]
- [[handle-based-resource-manager]]
- [[per-entity-scene-graph]]
- [[custom-allocator-interface]]

## 原文

- 链接：
  - https://bitsquid.blogspot.com/2014/08/building-data-oriented-entity-system.html
  - https://bitsquid.blogspot.com/2014/09/building-data-oriented-entity-system.html
  - https://bitsquid.blogspot.com/2014/10/building-data-oriented-entity-system.html
- 本地：
  - `raw/articles/bitsquid.blogspot.com/2014-08-27_building-a-data-oriented-entity-system-part-1.md`
  - `raw/articles/bitsquid.blogspot.com/2014-09-08_building-a-data-oriented-entity-system-part-2-components.md`
  - `raw/articles/bitsquid.blogspot.com/2014-10-03_building-a-data-oriented-entity-system-part-3-the-transform.md`
