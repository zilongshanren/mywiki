---
tags: [unity, dots, ecs, tween, animation, performance]
date: 2026-04-19
sources: 1
---

# Unity DOTS Tween 系统

[[Ted Sie]] 在 DOTS 学习路线上的第二个案例（第一个是砖块破坏游戏）：把传统 MonoBehaviour 版 Tween 迁移到 ECS。测试数据是关键——**50 万物体同时 tween，CPU 耗时从 614.5ms 降到 64.3ms，约 89.5% 的提升**。作为案例也暴露了 ECS 在实际工程里的几个摩擦点。

## 拆解 MonoBehaviour 版 Tween

传统 Tween 在 `Update` 里做三件事：

1. 累加时间 → 得到归一化 `t`。
2. 把 `t` 过一个 Ease 函数 → 得到插值系数 `lerp`。
3. 用 `lerp` 在 `from / to` 之间求值 → 写回 Transform。

## DOTS 化的五层分解

分成 Entity + 多个 System 的拆分方式：

- **TweenBase (Component)**：`loop / pingpong / duration / time / lerp`，所有 Tween 共用。
- **TweenBaseSystem**：用 `Entities.ForEach` 处理 `TweenBase`，累加 time、计算归一 lerp。
- **TweenFloat3 / TweenFloat4 (Component)**：承载 `from / to / result` 的类型化数据。
- **TweenInterpolationSystem**：过滤 `TweenBase + TweenFloat3` 的 Entity，`math.lerp(from, to, tweenBase.lerp)` 写入 `result`。
- **应用 System（TweenLocalRotationSystem 等）**：用 `TransformAccessArray` + `IJobParallelForTransform` + `BurstCompile` 把 result 写回 Transform。这一层才真正享受到 Job + Burst 的 SIMD 收益。

## Ease Function 的 DOTS 化

Ease 通过**标签 Component + UpdateAfter** 的组合实现：

- 每种 Ease（如 `EaseInOutQuadratic`）就是一个空 Component。
- 对应的 System 用 `[UpdateAfter(typeof(TweenInterpolationSystem))]` 保证执行顺序在 lerp 计算之后（其实是之前，用于 warp lerp 值）。
- 系统按 `WithAll<EaseInOutQuadratic>()` 过滤，对该类 Entity 的 lerp 做函数变换。

这种"用标签 Component 开关代码路径"的写法是 DOTS 里的核心 idiom。

## Transform 之外：和 MonoBehaviour 通信

`IJobParallelForTransform` 是 Unity 黑盒对 Transform 的特殊并行化。对其他 MonoBehaviour（如 `Light`），作者示范了退路：

- 用 `Entities.WithoutBurst().WithAll<TweenLightColor>().ForEach((Light light, in TweenFloat4 data) => ...)` 直接访问托管对象。
- 必须 `inputDeps.Complete()` 显式等待上游 Job 完成，且放弃 Burst。
- 代价是**失去并行 + SIMD**——是能通但不快的下策。

## 生命期管理：EntityCommandBuffer

Tween 播放完毕要清理 Entity，不能让它永远留在 Chunk 里。做法：

1. `TweenBase` 里多存一个 `Entity` 自引用。
2. 结束时通过 `EntityCommandBuffer.Concurrent.AddComponent<TweenComplete>(entityInQueryIndex, entity)` 打标签——注意 `entityInQueryIndex` 是 DOTS 的保留参数名。
3. `TweenCompleteSystem` 扫 `TweenComplete`，触发 Complete 回调，加 `TweenDestroy`。
4. `TweenDestroySystem` 扫 `TweenDestroy`，`ecb.DestroyEntity(...)`。

把"删除"拆成三个 System 而非一步到位，是为了配合 ECB 的**延迟执行**与帧边界之间的安全点。

## 工程启示

- **ECS 不是免费午餐**：Transform 用 `IJobParallelForTransform`，但 Light 就只能 WithoutBurst，说明引擎托管对象的集成仍是 leaky abstraction。
- **标签 Component** 是 DOTS 的控制流——不是多态，是位图过滤。
- **Burst 的收益只在纯 blittable 数据路径上**——只要沾染 managed object，就退化。
- 文末评论"Tween 是 UI 用得多，不太需要 DOTS 化"切中要害：**DOTS 的收益和数据规模强相关**，UI Tween 几十个 entity 时 MonoBehaviour 够用。这也呼应了 [[ecs]] 页中"方向正确但引入新复杂性"的结论。

## 相关

- [[ecs]]
- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[unity-complexity-patterns]]
- [[shaping-functions]]

## Sources

- [[sources/tedsie-dots-tween-system]]
