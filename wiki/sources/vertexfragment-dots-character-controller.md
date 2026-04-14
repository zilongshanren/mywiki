---
tags: [source, game-development, unity, dots, ecs, character-controller, physics]
date: 2026-04-14
sources: 1
---

# Unity DOTS Character Controller（Steven Sell / Vertex Fragment）

[[steven-sell]] 2020 年 8 月写的长篇工程记录，用 Unity DOTS（Entities + Physics 包）从零搭一个 kinematic 角色控制器。起因是他的项目 Realms 之前用 rigidbody 控制器，但手感滑、上不去台阶，不得不重写。

## 摘要

文章是一份分段详尽的实现笔记。角色被拆成 `CharacterControllerComponent`（纯数据：输入、控制参数、内部状态）和 `CharacterControllerSystem`（`IJobChunk` 作业），系统挂在物理 group 内部，依赖 `BuildPhysicsWorld`/`ExportPhysicsWorld`/`EndFramePhysicsSystem`，通过 `JobHandle.CombineDependencies` 织进物理依赖链。核心循环 `HandleChunk` 对每个实体依次做：构造 epsilon 防止贴地误伤 → 计算 vertical velocity（重力 + 跳跃，grounded 时清重力防滑坡）→ collider cast 试探，有碰撞就用 `ColliderDistance` 查 penetration 沿 surface normal 推出并二次 cast → 水平位移先试 step-up（从 `targetPos + MaxStep` 朝 target 打垂直 cast，`Fraction != 0` 说明头顶有净空就抬起 target 爬梯）→ 不能 step 就 slide（对所有 penetration hit 累加 `normal * -distance` 投影速度沿墙滑）→ grounded 判定是 5 条向下 raycast（中心 + 四周，用 collider bounds 的 fraction 作为偏移，避开小坑误判与 wall-jump 误报）。作者还提供一组 PhysicsUtils 封装（`ColliderCast/All`、`ColliderDistance/All`、`TrimByFilter` + `PhysicsCollisionFilters.DynamicWithPhysical` 用来排除 trigger volume）。`PlayerControllerSystem` 是单独的主线程系统，只负责把 WASD + camera 朝向翻译成 controller 的 `CurrentDirection/Magnitude` + `Jump`。

## 关键要点

- kinematic 控制器靠自己查询碰撞并维护速度，彻底绕开 rigidbody 的"滑冰感"和"卡台阶"
- DOTS 下数据（component）与逻辑（system）严格分离，job 要通过 `ComponentTypeHandle<T>` + `chunk.GetNativeArray` 访问数据
- 水平与竖直速度分开处理比合并成一个向量更好维护
- 5 条 raycast 的 grounded 判定是简单但有效的折中，避免单中心 ray 的误判和 collider cast 的 wall-jump 漏洞
- step-up 的"上方垂直 cast 看有没有净空"是让角色爬楼梯的标准 trick
- 作者坦白的 edge case（不做 substep → 高速穿墙、不限坡度、移动平台失效）正是 kinematic 控制器的典型未竟之业

## 链接到的概念

- [[kinematic-character-controller]]
- [[ecs]]
- [[unity-complexity-patterns]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/unity-dots-character-controller/
- 本地：`raw/articles/vertexfragment.com/2020-08-27_unity-dots-character-controller.md`
