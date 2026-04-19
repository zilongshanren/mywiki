---
tags: [ecs, 架构, 模块化, svelto]
date: 2026-04-19
sources: 2
---

# ECS 抽象层与模块封装

[[sebastiano-mandala]] 把*依赖倒置原则*（高层不依赖低层实现）与 *Hollywood Principle*（"Don't call us, we'll call you"）搬到 ECS 世界后得到的一套工程化组织方法。核心主张：**ECS 不仅要把代码拆成 system / component，还要进一步按职责抽象程度拆到独立的 assembly / dll / asmdef，让依赖关系严格单向分层**。

## 问题

主流游戏引擎把"框架 vs 用户代码"做成非黑即白：Unity 的 MonoBehaviour 完全由框架 new 和调度，用户代码不能充当框架。*IoC 容器*（ZenInject、StrangeIoC）反过来走极端，鼓励对象互相知道，最终变成谁都能随时调用谁的意大利面。ECS 如果只停留在"一堆 system 平铺"的阶段，同样会退化——尤其当代码量上来之后。

## 抽象层规则

Mandalà 建议把 ECS 代码按行为抽象度切成层，用物理边界（assembly）而不是命名约定来强制封装：

- **高层 = 抽象的"框架"模块**：提供 Component（相当于 OOP 的接口）、通用 Engine（System）、group tag。这些模块不知道有哪些具体实体会用它们。
- **低层 = 专门化模块**：用高层的 ExtendibleEntityDescriptor 把自己的 component 拼上去，从而被高层 engine 自动处理。
- 依赖方向由 asmdef 强制——**禁止循环依赖**，高层永远不知道低层。
- 通用 engine 用 `entitiesDB.FindGroups<T>()` 查询（不预设哪些组会带这些 component）；专门化 engine 用 group compound tag 查询（代码里能看见用在哪些组上）。

在 Svelto 术语里这就是：*Projectile Layer* 提供 ProjectileComponent + ProjectileEntityDescriptor + 通用 ProjectileEngine；*Weapon Layer* 引用 *Projectile Layer* 并用它的 descriptor 去 spawn 子弹；反过来 *Projectile Layer* 绝不知道 Weapon 的存在。

## Composition Root

每一层都是 `static class`，只暴露一个 `Compose(Action<IEngine> addEngine, …)`，把自己内部的 engine 注册到 EnginesRoot 里。engine 一律 `internal`——这是"只有边界，没有门"的封装手段。最终 Game 层的 composition root 把所有 context 串起来：

```csharp
TransformableContext.Compose(AddEngine);
SimplePhysicContext.Compose(AddEngine);
PlayerContext.Compose(AddEngine, input, entityManager, enginesRoot, sceneSystem);
BulletContext.Compose(AddEngine, entityManager, enginesRoot, sceneSystem);
EnemyContext.Compose(AddEngine, entityManager, enginesRoot);
```

每个 context 都可以有自己的 *Mock Composition Root* 用于单独测试。

## 抽象层的副产品

- 符合 Robert Martin 的 *Granularity* / *Stability* 原则：改一个行为只影响一两个 assembly
- 通用层（如 Damageable / Transformable / Physic）可以跨项目复用，游戏层只管组合
- 强制的单向依赖让重构代价线性而非组合爆炸

Mandalà 一再强调：**"Early abstraction is the root of all evil"**——不要提前画层，而是先写能跑的代码，等共享行为自然浮现再重新打包。

## 与 [[svelto-ecs]] 的关系

这套思想直接驱动了 Svelto.ECS 的 API 设计：ExtendibleEntityDescriptor、ReactOn callback、group compound 都是为抽象层服务的。2022 年重写的 Survival Mini Example（见 [[sources/sebaslab-survival-mini-example]]）就是把这套范式拆成 Player / Enemy / Camera / HUD / Damageable / OOP 六个 asmdef 的参考实现。

## Sources

- [[sources/sebaslab-ecs-abstraction-layers]]
- [[sources/sebaslab-survival-mini-example]]
