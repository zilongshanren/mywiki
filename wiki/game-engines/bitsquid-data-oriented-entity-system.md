---
tags: [游戏引擎, ecs, bitsquid, data-oriented, entity-system, transform, soa]
date: 2026-04-19
sources: 1
---

# Bitsquid 数据导向 Entity System

[[niklas-frykholm|Niklas Frykholm]] 2014 年的三篇连载（"Building a Data-Oriented Entity System" Part 1–3）是同时代公开文献里最完整的一份 [[ecs|数据导向 ECS]] 落地笔记。Bitsquid 原本没有 component 架构——因为 gameplay 都在 Lua 里写，[[lua-runtime-dynamism-tricks|Lua]] 已经把传统深继承的痛苦消化掉了。真正逼出 ECS 的，是 [[engine-plugin-c-abi-versioned-api|plugin 系统]]：C++ 插件要给 entity 动态加新能力，component 成了**最自然**的装配单位。

## Entity 只是一个整数

Bitsquid 的 `Entity` 是一个 32 位 id，其中 22 位 index + 8 位 generation——和 [[id-lookup-table-packed]]、[[id-based-lifetime-with-kill-flag]] 是同一套思路。`EntityManager` 只维护两个东西：`Array<unsigned char> _generation` 和 `Deque<unsigned> _free_indices`。`alive(e)` 就是 `_generation[e.index()] == e.generation()`，O(1) 而且 8 bit/entity 的 generation 表足够贴进 cache。

为防 generation 回绕，recycle 出来的 index 进 FIFO 队列，**至少累积 1024 个空闲 index 才能复用**——于是同一个 id 要想再次出现，至少需要先创建销毁 256 × 1024 ≈ 260 k 个 entity，工程上基本安全。30 位总宽度是被 Lua light userdata 的 32 位指针（去掉 2 位 tag）约束出来的——纯 64 位平台可以放宽。

## Component 由 Manager 集中管理

**没有 `Component` 基类，也没有 `entity.components` 列表。** 每类 component 由一个 `ComponentManager` 持有，manager 全权决定内存布局。`DebugNameComponentManager::debug_name(Entity e)`、`PointMassComponentManager::set_mass(Instance i, float m)`——想知道 entity 有没有某个 component，去问那个 manager。**entity 不知道自己有哪些 component**。

这样做的代价是 entity 死亡时需要把销毁通知广播出去；Bitsquid 的解法是两档：持有外部资源的 component 注册 destruction callback 立刻清理，轻量 component 走**惰性 GC**——每帧随机采样 4 个 instance，遇到 entity 已死就 swap-erase，连续 4 个都活着就停。这在"销毁率高时勤快、销毁率低时几乎零成本"之间做了自适应。

## SoA + 单块 buffer + HashMap 间接寻址

Manager 的数据布局是**结构数组 (Structure-of-Arrays)**，每个字段一条连续数组：`Entity *entity`、`float *mass`、`Vector3 *position`、`Vector3 *velocity`、`Vector3 *acceleration`。但这 5 条数组不是 5 次 `Array<T>` allocation——Niklas 直接 **一次 allocate 一个大 buffer**，五个指针分别指向 buffer 内部不同偏移。`allocate(sz)` 时一次 realloc + 五次 memcpy，从此和 5 条独立数组拜拜：**对 allocator 友好、对 cache 友好、对 debugger 也友好**（只有一块内存要盯）。

评论区有人提议把 `position/velocity/acceleration` 打包成 AoS 的 `SimData`，Niklas 的回应很关键：SoA 在 simulate 只碰 vel/pos/acc 时可以省 18.2% 的 cache 空间（不加载 mass/entity），对于 memory-bound 的典型 update 就是 18.2% 性能。**AoS 只在 "几乎每个字段都要碰" 的极少数场景才略胜**，所以默认走 SoA，等将来要上 SIMD 时也正好铺好了路。

Entity → Instance 的映射用 `HashMap<Entity, unsigned>` 而不是直接 index——除非 component 是"几乎所有 entity 都有"的那种（transform 可能是，debug-name 肯定不是），否则直接数组会留一堆空洞。API 上把 `Instance` 包成 `struct Instance { int i; }`——多一层类型让"拿到的 int 到底是 entity 还是 instance"在编译期就分得清。

`destroy(i)` 的实现是**swap-erase**：把末尾 element 移到被删位置，更新 `_map[last_entity] = i`，`--n`。和 [[handle-based-resource-manager]] 的对象池是同一套手法。

## 世界不止一个：World 和 Manager 的复数

Bitsquid 没有单一的全局 World——每个 `World` 有自己的一套 component manager。同一个 entity 可以在多个 world 里有不同的 `TransformComponent` 实例，也就是 **同一个 entity 在"主游戏世界"和"背包世界"里可以有不同位置、不同 mesh**。听起来玄，但对 pickaxe 这种同时要在世界里和在背包里显示的道具就很顺手。

## TransformComponent：entity scene graph 与 model scene graph 分离

场景图有两张。**entity scene graph**：child entity 跟着 parent entity 动（车轮跟着车）。**model scene graph**：单个 entity 内部的骨骼层级（角色几百个骨头）。以前 Bitsquid 把两张图接到一张上——model 算世界空间、要先等 entity scene graph 算完，**更新顺序被锁死**，并行化空间极窄。

Part 3 的关键决策是**解耦两张图**：model scene graph 只算**相对 entity 的局部姿态**，entity transform 完全不管。要拿 model node 的世界坐标？拿到 entity world transform 自己乘一下。代价换来了两张图可独立、可并行、可异步。

## Immediate vs Deferred 更新

`TransformComponent` 的 world 矩阵更新策略有两档：

- **Deferred**：改 local 只置 dirty，后面统一扫 dirty 列表算 world。对 n 层嵌套的 chain，即使每层都动，也只要 O(n) 次矩阵乘。但**查询 world 时拿到的是上一帧的值**——bug 温床。
- **Immediate**：改 local 立刻把自己和所有子孙的 world 重算。最坏情况 O(n²)（每层都动一次），但永远不会读到陈旧值。

Niklas 的选择是 **immediate**，理由也很 Bitsquid：entity scene graph 里的 chain 一般 ≤ 5 层，且不太会同时整条 chain 都在动（不像 model 的鞭子动画），O(n²) 的最坏场景在 entity 层基本不出现。并且**"世界坐标永远准确"这件事值得多付一点 CPU**——bug 少于性能。如果真撞上性能问题，再开一个"批量改 local、最后触发一次 transform"的 API 就能回到 O(n)。

### Deferred 也有工程技巧

如果选 deferred，Niklas 顺手给出两条优化：

1. **dirty 段集中在数组尾部**。每帧可能只有 1% 的 entity 在动，扫全数组都是浪费。用 swap 把 dirty 的搬到尾部，循环只走 `[first_dirty, n)`。
2. **数组按"parent 永远在 child 之前"排序**。这样 `for (i = first_dirty; i < n; ++i) transform(i)` 一遍跑下去，child 算 world 时 parent 的 world 一定是新的。保持这个不变式靠 swap——发现 child 在 parent 前面就交换。

### swap 三步法

Transform component 数据里不光 `local/world`，还有 `parent/first_child/next_sibling/prev_sibling` 四条 Instance 引用数组。swap 两个 element 时，既要搬 element 也要修所有引用。Niklas 的办法是用末尾 `[size]` 做中转：`[size]←[A]`、`[A]←[B]`、`[B]←[size]`，每一步都保证被搬的 element **没人引用**，避免"改引用时还走链表"的互相纠缠。

## 为什么这套值得被当作业界标杆

2014 年 ECS 还远不是主流（Unity DOTS 要到 2018 才公开预览），Niklas 这份笔记把**"entity 只是 id"、"manager 拥有布局"、"SoA 默认"、"惰性 GC"、"handle + generation 防悬垂"、"两张 scene graph 分离"、"immediate 与 deferred 的取舍"、"dirty 段末端排序"** 全部摊开讲清楚——每一条后来都能在 DOTS / bgfx / Our Machinery / stingray 后续演进里看到对应。

和 [[component-entity-data-binding|Todd 的端口绑定]] 比，Bitsquid 的 manager 方案更接近数据库视角（System 查询一堆 entity 一次性批处理）；和 [[ecs|DOTS 的 Archetype/Chunk]] 比，Bitsquid 保留了"每类 component 管自己"的分散权力，没有把所有 component 塞进统一 chunk。[[ecs-data-oriented-revert|云风]] 近年对 Ant ECS 的"回归原始"反思——少加封装、保留数据视角——精神上和 Bitsquid 这份 2014 年的设计接近。

## 相关

- [[ecs]] — Unity DOTS 代表的后继 ECS，把 SoA/Archetype 做到了编译器+运行时层
- [[component-entity-data-binding]] — Todd 的"端口"方案，组件间不互相引用
- [[ecs-data-oriented-revert]] — 云风反思：不要给 ECS 加太多辅助模块
- [[ecs-particle-system-c]] — 纯 C 实现的 ECS 粒子系统
- [[aos-vs-soa]] — SoA 在 memory-bound 场景的 18% 经验优势
- [[id-lookup-table-packed]] — Bitsquid 同作者的另一个 id + generation 版本
- [[id-based-lifetime-with-kill-flag]] — id + kill flag 管理对象生命周期
- [[handle-based-resource-manager]] — swap-erase 式 packed 对象池
- [[per-entity-scene-graph]] — per-entity scene graph 的一般讨论
- [[scene-graph-matrix-stack-visitor]] — 场景图的 matrix stack 访问者模式
- [[scene-graph-unnecessary-in-engine]] — 场景图是否该从引擎下放到游戏层的讨论
- [[engine-plugin-c-abi-versioned-api]] — 逼出 Bitsquid ECS 的 plugin 系统
- [[custom-allocator-interface]] — manager 分配"一大块 buffer 自己切"的前提
- [[entity-index-reconstruction]] — Stingray 后来对 entity index 的原型链式重构

## Sources

- [[sources/bitsquid-data-oriented-entity-system]]
