---
tags: [unreal-engine, cpp, roguelike, action-system, data-oriented-design, object-pool]
date: 2026-04-19
sources: 1
---

# Project Orion：UE5 合作 Roguelike 示例项目

**Project Orion**（简称 Orion）是 [[tom-looman]] 在 UE5 下用纯 C++ 搭建的合作动作 Roguelike 示例，设计参考以 Risk of Rain 2 为对标，源码托管于 [GitHub: tomlooman/ActionRoguelike](https://github.com/tomlooman/ActionRoguelike)。它起源于 Tom 的 "Professional Game Development in C++ and Unreal Engine 5" 课程，后续不断加入新特性，目前已经是一份覆盖 Ability 系统、AI、存档、性能优化的综合模板。实验性开关集中在 `ActionRoguelike.h` 的 `#define` 里，改成 1 重编即可启用。

## Action 系统（Abilities / Buffs / Attributes）

项目自带一套仿 GAS 的 "Action System"：

- **Action** —— 表示技能/能力，例如冲刺、投射物、闪现，Player 和 Monster 都通过 Action 驱动行为。
- **ActionEffect** —— 即 Buff/Debuff，挂载到 Actor 身上的临时效果，可驱动属性、施加伤害、附加修正。
- **Attribute** —— 生命、体力、移动速度等数值，分 Base（永久，升级时改）与 Modifier（临时，Buff 施加）两层，Action 和 ActionEffect 都通过它来读写。

## 近战战斗

敌方 Monster 的近战攻击与 Behavior Tree + AnimMontage + AnimNotify 结合：BT 检查距离决定是否进入近战序列，`RogueAction_MinionMeleeAttack` 起停攻击并播放 AnimMontage，`RogueAnimNotifyState_Melee` 在 AnimNotify 生命周期内跑 `OverlapMultiByChannel` 并广播 `OnMeleeOverlap` 给 Action，由 Action 统一走伤害流程。`game.drawdebugmelee 1` 可视化重叠形状。

## 存档系统

项目内置了世界状态 + 玩家信息的存档框架，Tom 有专门博客 ([Unreal Engine CPP Save System](https://tomlooman.com/unreal-engine-cpp-save-system)) 拆解实现。

## 性能优化实践

这是 Orion 最核心的一块学习材料，给出几种在 UE 中不那么 "Actor-first" 的做法：

- **Data-Oriented Projectiles** —— 投射物既可以是 Actor，也可以用 struct 数组驱动（见 `URogueProjectileSubsystem`）。通过宏 `USE_DATA_ORIENTED_PROJECTILES 1` 切换，开启后玩家和敌人都用 struct 投射物，能轻松支撑上千弹幕。
- **Data-Oriented Lootables** —— 击杀敌人时喷射千枚金币，全部以 DoD 驱动，用单个 `InstancedStaticMeshComponent` 渲染（也可替换为 Niagara），逻辑见 `URoguePickupSubsystem`。
- **Object Pooling** —— `URogueActorPoolingSubsystem` 提供 Actor 池化，在 load screen 预生成固定数量的实例（如怪物尸体 `ARogueMonsterCorpse`），通过 `AcquireFromPool` / `ReleaseToPool` 复用。目的是避开 Actor Spawn 的高 CPU 成本、减少内存碎片、降低 GC 销毁开销。
- **Significance Manager** —— UE 自带的 "桶 + 容量" 框架，用来按重要度节流/裁剪游戏逻辑、动画和 VFX。示例以 MinionRanged 为载体做动画与 VFX 的分级节流，Fortnite 用它保证同一时刻只有 X 个玩家跑满帧质量，其余 LOD 和 VFX 被降级。
- **Animation Budget Allocator** —— UE 的动画预算插件，用在敌方 Monster 上，目标是把动画帧时间压在阈值内。可通过 `a.Budget.BudgetMs` 控制预算，`a.Budget.Debug.Enabled` 和 `stat AnimationBudgetAllocator` 查调试信息；`ARogueAICharacter` 可重写 `OnReduceAnimationWork` 插入自定义节流逻辑。

## 相关

- [[unreal-insights-counters-traces]]
- [[unity-vs-unreal]]

## Sources

- [[sources/tomlooman-project-orion]]
