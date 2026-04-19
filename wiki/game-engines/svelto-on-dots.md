---
tags: [ecs, svelto, unity-dots, 集成]
date: 2026-04-19
sources: 1
---

# Svelto-On-DOTS

Svelto.ECS 3.4 提供的 *Svelto-On-DOTS* 集成把 Unity DOTS ECS **当作 ECS 写的引擎库**来用，而不是"游戏框架"。[[sebastiano-mandala]] 的立场很明确：ECS 做不了一整个引擎（引擎的数据结构、算法和 ECS 模型经常不匹配），但 DOTS ECS 里那些 burstified 的渲染 / 物理库拿来当库用刚好合适。于是 Svelto 接管生命周期与调度，DOTS ECS 退化成一个可以 jobify / burstify 的 component 仓库。

## 帧流水线

Svelto-On-DOTS 把一帧切成下面的同步步骤：

1. Svelto（游戏逻辑）engines 先跑
2. 进入 integration：sync point — 等所有影响 DOTS entity 的 job 结束
3. Svelto → DOTS 的同步 engines 执行
4. Svelto entity submission（本帧的 add / remove / move group 生效）
5. Svelto 的 Add / Remove 回调（`ISveltoOnDOTSStructuralEngine` 在这里创建 / 改 DOTS entity）
6. `SveltoOnDOTSStructural` 的 post-submission
7. 纯 DOTS ECS 的 world 更新（Svelto 控制 `World.Update()`）
8. DOTS → Svelto 的同步 engines

## 打破的 DOTS 约定

要让 DOTS 服从 Svelto 的节拍，必须关掉 DOTS 的自动化：

- 在项目定义里开 `UNITY_DISABLE_AUTOMATIC_SYSTEM_BOOTSTRAP_RUNTIME_WORLD`
- DOTS world 由 Svelto 创建和持有
- 所有 sync engine / 纯 DOTS system 打 `[DisableAutoCreation]`，由用户在 composition root 里手动加到 Svelto 的 DOTS world
- Svelto 手动调 world update，不再让 PlayerLoop 驱动

Mandalà 认为 DOTS 1.0 的自动 bootstrapping 和 `ISystem` 把实例化权限从用户手里夺走，代价是丧失了 composition root 的可视性和 DI 灵活性——Svelto-On-DOTS 正是要把这点拿回来。

## Sync 策略

两种典型模式：

- **Pool 模式**：DOTS entity 集合被当作"尺寸和 Svelto 集合对齐的池子"，通过 `SharedComponentFilter` 过滤出与当前 Svelto group 对应的子集，然后 burstified `Entities.ForEach` 写 `Translation`。适合渲染这种不需要 1:1 的场景。
- **1:1 模式**：每个 Svelto entity 精确配对一个 DOTS entity。Havok Physics 这种需要保留 DOTS 侧状态的子系统必须走这条。

靠 Burst + Job + cache-aligned 数据结构，sync engine 的开销通常很小。Mandalà 强调 sync engine **只应触碰 DOTS 库组件**（Translation、PhysicsVelocity、RenderMeshArray 之类），不要用用户自定义 DOTS component——那样就又把逻辑切回 DOTS 侧了。

## EntityCommandBuffer 被废

升级到 DOTS 1.0 时 Mandalà 发现 ECB 不是"在 job 里安全应用结构性改变"，而是**把 op 排队、之后在主线程一条条重放**，性能极差。他干脆从 Svelto.ECS 里把 ECB 使用整个删掉，改用 DOTS 1.0 的 *batched operations*；500+ entity 的结构性改变走 batched op 后 Svelto-On-DOTS 的 submission 成本降到和纯 Svelto 同档。

## 对 DOTS 1.0 的评价

Pros：
- idiomatic for each 与 Svelto 多年的 API 一致
- `ISystem` 从继承转向接口
- 大量 API 已经预先 burstified，`EntityManager` 可以直接进 job
- 更清晰的 managed vs unmanaged component 分界

Cons：
- `ISystem` 不能由用户实例化，与依赖注入冲突
- archetype 模型鼓励"避免结构性改变"，但结构性改变恰恰是 ECS 表达状态的核心手段
- [[dots-enableable-components|IEnableableComponents]] 是 [[svelto-filters-api|Svelto filter]] 的弱化版
- `Aspect` 看起来没必要
- 过度依赖 source generation 让调试变难
- 他怀疑 chunk 的基础设计本身是过度工程，限制了 API 能简化到的下限

## 到底要不要 DOTS？

Mandalà 的结论：Svelto.ECS 自己已经兼容 Burst / Job 很多年，DOTS ECS 主要的卖点（jobify / burstify）并非 DOTS 独占。DOTS 对大公司意义在于官方支持与生态；*Robocraft 2* 作为 Svelto-centric 商业项目，只用 DOTS ECS 跑 Havok，渲染用 GPUInstancer、网络用 LiteNetLib——这反过来佐证了"DOTS 当库用"的思路能 ship。

## Sources

- [[sources/sebaslab-svelto-on-dots-update]]
