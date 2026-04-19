---
tags: [ecs, svelto, 框架]
date: 2026-04-19
sources: 5
---

# Svelto.ECS

[[sebastiano-mandala]] 开发的**平台无关 C# Entity-Component-System 框架**，用于 Unity / .NET / SDL / Stride 等环境。和 [[dots-ecs-programming-patterns|Unity DOTS ECS]] 的 archetype 模型不同，Svelto 用**群组（Group / GroupCompound）**做内存布局，而且从诞生之初就把 ECS 当作"多范式应用里的一层"而非"要吞掉整个引擎的终极模型"。

## 内存模型：Group 而非 Archetype

在 DOTS 里，entity 的 component 组合变了就要换 archetype，archetype chunk 是底层存储单位；在 Svelto 里，entity 一定属于且仅属于一个 group，group 就是存储单位。GroupCompound 把最多 4 个 tag 组合成 group，从而表达多维状态（例：`GameGroups.RED.ALIVE.FLYING`）。优点是——

- group 身份**显式**，程序员直接能看见状态维度
- 结构性改变 = "把 entity 从一个 group 挪到另一个 group"，语义清楚
- 不需要像 archetype 那样规避"frequent structural change"

缺点是 group 数量可能组合爆炸、内存碎片——[[svelto-filters-api|Filters API]] 就是为缓解这个而生。

## 核心 API 面

- **EntityDescriptor / ExtendibleEntityDescriptor** — 声明 entity 的 component 组合，支持继承扩展
- **Engine** — Svelto 的 System，实现 `IQueryingEntitiesEngine` 查询 DB、实现 `IStepEngine` / `IUpdateEngine` 定义 tick
- **EnginesRoot** — 容器，用户手动把 engine add 进去（**不自动 bootstrap**）
- **IReactOnAddEx / IReactOnRemoveEx** — 在 entity submission 时触发的回调
- **SveltoDictionary** — 核心存储结构，component 数据的实际 hashmap。其 `IBufferStrategy` 接口允许把存储换成任意后端（见 [[ecs-on-gpu-computesharp]]）

## 设计哲学

Mandalà 对 Svelto 有几个反复强调的立场：

- **非 100% ECS**：ECS-centric 应用而不是 ECS-only，和 OOP 库交互走 [[ecs-abstraction-layers|OOP 抽象层]]
- **显式优于魔法**：没有自动 bootstrap、没有 attribute 魔法、engine 和依赖都在 composition root 手动组装
- **框架就一个人写**：不要过度工程，实现"as simple as it can get"
- **模块化边界**：用 asmdef / assembly 强制层间依赖方向，见 [[ecs-abstraction-layers]]
- **ECS ≠ 引擎**：Svelto 不做渲染、不做物理、不做网络；这些需要专用库。DOTS ECS 想走的"把整个引擎迁到 ECS"他明确不认同

## 里程碑

- **3.0** — 大规模重构，确立现在的 group / compound / descriptor 模型
- **3.3**（2022-04）— [[svelto-filters-api|Filters API]] 重写，persistent filter + transient filter 两档
- **3.4**（2023-03）— [[svelto-on-dots]] 更新到 DOTS 1.0，废掉 EntityCommandBuffer 改用 batched operations
- **3.4 内部** — 通过 `IBufferStrategy` 演示 [[ecs-on-gpu-computesharp|ComputeSharp 后端]]，component 直接存在 GPU compute buffer

Mandalà 声明不会有 4.0——后续都是兼容的增量改进。

## 商业验证

*Robocraft 2*（Freejam）是 Svelto-centric 的商业作品：每个方块都是一个 Svelto entity，DOTS ECS 只被用来跑 Havok Physics，渲染走 GPUInstancer，网络走 LiteNetLib。这是"Svelto 主 + DOTS 当库用"模式的 ship 证据。

## 相关

- [[ecs-abstraction-layers]] — 用 assembly 强制的分层封装方法论
- [[svelto-filters-api]] — 跨 group 的子集索引
- [[svelto-on-dots]] — 与 Unity DOTS ECS 的集成模式
- [[ecs-on-gpu-computesharp]] — 把 component 存储接到 GPU
- [[ecs]] — 整体 ECS 范式入口
- [[dots-ecs-programming-patterns]] — 对照路线

## Sources

- [[sources/sebaslab-ecs-abstraction-layers]]
- [[sources/sebaslab-svelto-filters-api]]
- [[sources/sebaslab-survival-mini-example]]
- [[sources/sebaslab-svelto-on-dots-update]]
- [[sources/sebaslab-ecs-on-gpu-computesharp]]
