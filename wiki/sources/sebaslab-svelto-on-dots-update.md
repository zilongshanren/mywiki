---
tags: [source, ecs, svelto, unity-dots, 集成]
date: 2026-04-19
sources: 1
---

# Svelto.ECS 3.4 – Svelto On DOTS ECS update（Sebastiano Mandalà / Seba's Lab）

[[sebastiano-mandala]] 2023 年 3 月发布的 Svelto.ECS 3.4 说明：解释为什么一个已有的 ECS 框架要和 Unity DOTS ECS 集成，以及他对 DOTS 1.0 的评价。

## 摘要

Svelto.ECS 3.4 的 *Svelto-On-DOTS* 集成把 DOTS ECS **当作 ECS 写的引擎库**而非游戏框架。Mandalà 的核心立场：ECS 做不了一整个引擎（引擎算法和 ECS 模型不匹配），但 DOTS 里被 Burst / Jobs 加速的库（Havok、rendering 后端等）拿出来当库用刚好。Svelto 接管整帧调度，world 由 Svelto 创建、`[DisableAutoCreation]` 关掉 DOTS 自动 bootstrap，DOTS world 的 `Update()` 也由 Svelto 手动调。帧流水线分八步：Svelto engine → sync point 等 DOTS job → Svelto→DOTS sync → Svelto submission → Add/Remove callback → structural engine post-submission → DOTS world update → DOTS→Svelto sync。升级到 DOTS 1.0 时他发现 EntityCommandBuffer 是性能陷阱——ECB 只排队 op、最后在主线程串行回放，他把 Svelto 里所有 ECB 用法删光、改用 DOTS 1.0 的 batched operations，500+ entity 结构性改变的耗时降到和纯 Svelto 同档。文末给了 DOTS 1.0 的详细评价。商业证据：*Robocraft 2* 是 Svelto 主体，DOTS ECS 只跑 Havok，渲染走 GPUInstancer、网络走 LiteNetLib。

## 关键要点

- Svelto-On-DOTS 帧流水线固定 8 步，Svelto 全程持有调度权
- 必须 `UNITY_DISABLE_AUTOMATIC_SYSTEM_BOOTSTRAP_RUNTIME_WORLD` + 所有 system 打 `[DisableAutoCreation]`
- Sync engine 两种模式：pool（不要求 1:1）+ 1:1（Havok 这类需要 DOTS 侧状态的场景）
- EntityCommandBuffer 被废：用 DOTS 1.0 的 batched operations 替代，性能提升显著
- DOTS 1.0 Pros：idiomatic for each、`ISystem` 弃继承、`EntityManager` 进 Burst、managed/unmanaged 分界清晰
- DOTS 1.0 Cons：`ISystem` 不能用户实例化、archetype 恐惧症、[[dots-enableable-components|IEnableableComponents]] 是 [[svelto-filters-api|filter]] 的弱化版、过度依赖 source generation、chunk 设计可能是过度工程
- 结论：Svelto 已 burst/job 就绪，是否用 DOTS 是工程偏好而非能力短板

## 链接到的概念

- [[svelto-on-dots]]
- [[svelto-filters-api]]
- [[svelto-ecs]]
- [[dots-enableable-components]]
- [[dots-ecs-programming-patterns]]
- [[sebastiano-mandala]]

## 原文

- 链接：https://www.sebaslab.com/svelto-ecs-3-4-svelto-on-dots-ecs-update/
- 本地：`raw/articles/sebaslab.com/2023-03-13_svelto-ecs-3-4-svelto-on-dots-ecs-update-seba-s-lab.md`
