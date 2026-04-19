---
tags: [source, ecs, svelto, unity, 案例]
date: 2026-04-19
sources: 1
---

# The new Svelto.ECS Survival Mini Example（Sebastiano Mandalà / Seba's Lab）

[[sebastiano-mandala]] 2022 年末发布的 Svelto.ECS 入门参考示例重写版，是他 7 年前写的第一个 demo 的彻底改造。

## 摘要

Survival 是一个转自 Unity 老例子的打僵尸小游戏，但真正重要的是它把 Svelto 的最新范式全部串起来：[[ecs-abstraction-layers|ECS 抽象层]]用 asmdef 拆成 Hud / Enemy / Player / Camera / Damageable / OOP 六层，每层只管自己的 entity descriptor、engine、group tag。**implementors 模式被降级为 niche 用法**——Mandalà 认为这个旧模式太容易把用户拉回 OOP 思维，复杂 UI 用不动，cache 也不友好；**publisher/consumer 模式则被直接废掉**——它原本是为跨 EnginesRoot 通信设计的，后来被用来当 event bus，用户真正想要的是 "给我这一批处在某状态的 entity"，而 [[svelto-filters-api|Filter API]]能干净地表达这点。他还单独强调了 OOP Layer——Svelto 和 Unity 这类 OOP 框架的缝由一个专门的 asmdef 来缝，engine 顺序固定为 "Objects → Svelto engines → Entities sync to Objects → OOP code runs"，以后要换引擎只需要换这一层。Damageable 层给出抽象层的范例：Enemy 和 Player 都能受伤，就把 `HealthComponent` + `DamageableComponent` + `ApplyDamageToDamageableEntitiesEngine` 提升到抽象层，用 transient filter `DamagedEntitiesFilter` / `DeadEntitiesFilter` 筛出本帧状态子集。demo 可以在 WebGL 浏览器里跑，证明 Svelto 的兼容性。

## 关键要点

- 六层 asmdef：Hud / Enemy / Player / Camera / Damageable / OOP
- implementors 模式被降级为 niche 用法，新手用 OOP 抽象层模式
- publisher/consumer 被 filter 取代：transient filter 表达"本帧受伤"+"本帧死亡"两级筛选
- OOP Layer 的 sync 协议：OOP → Svelto（每帧开始）→ Svelto engines → Svelto → OOP（每帧结束）
- `GameObjectResourceManager`：给 Svelto entity 和 Unity GameObject 建立 1:1 映射
- Damageable 层给出 *"shared behaviour emerges → extract abstract layer"* 的模板

## 链接到的概念

- [[ecs-abstraction-layers]]
- [[svelto-filters-api]]
- [[svelto-ecs]]
- [[sebastiano-mandala]]

## 原文

- 链接：https://www.sebaslab.com/the-new-svelto-ecs-survival-mini-example/
- 本地：`raw/articles/sebaslab.com/2022-12-31_the-new-svelto-ecs-survival-mini-example-seba-s-lab.md`
