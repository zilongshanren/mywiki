---
tags: [unity, dots, ecs, source-generator, burst]
date: 2026-04-19
sources: 1
---

# DOTS Enableable Components 的代码生成内幕

Unity DOTS 的 **Enableable Components** 在表层看起来"就是少敲几个 `if (myBool)`"——但背后藏着一套由 **Roslyn Source Generator** 生成的状态机，足以解释为什么这个功能是 Unity 能拿出 [[ecs|ECS]] 源码生成之后才真正可行。

## 表面 API vs 生成代码

用户写的 `IJobEntity.Execute(ref MyComp c) { c.Value += 1234; }` 在 Burst 编译后的汇编里出现了 **8 次** `1234`。Source generator 在 `partial` 的另一侧给同一个 Execute 生成了三条路径：

1. **`!useEnabledMask`**：组件没有 `IEnableableComponent`，朴素 for 循环，每个 entity 调一次。
2. **Use-ranges mode**：mask 里"连续的 1 片段"数量 ≤ 4（用 `countbits(mask ^ (mask << 1))` 统计变化边）。外层 `while` 用 `UnsafeTryGetNextEnabledBitRange` 跳到下一个连续片段，内层 `while` 在片段内批量处理。
3. **Per-bit loop**：变化边多（disable 得太碎）时，for 循环 64 bit + 64 bit 地检查每一位。

选择逻辑硬编码在生成代码里：**`edgeCount <= 4` 才走 range 模式**。这意味着"偶尔 disable 几个 / 整段 disable"是性能甜蜜点；"均匀穿插 disable"最贵。但**不要为这个特性做优化**——Unity 的建议是"把 enableable 当成随意 toggle，别去考虑范围连续性"。

## 为什么非 Source Generator 做不到

"是否执行 Execute"的判断依赖 query——同一个 `Execute` 被不同 System / query 调用时，判断的组件不同、mask 不同。动态 dispatch 用虚函数/委托都打断 Burst；写模板让用户每个组合各写一份太啰嗦。Source generator 的优势是**编译期展开**：针对每个 Job 类型生成专属代码，mask 的 128-bit 拆法、bit-scan 指令都能被 Burst 继续 inline 和 SIMD 化。

## 128 entity per chunk 的硬上限

enable mask 是 **`v128`**（128 bit），所以 `MaximumChunkCapacity = 128`。在有 enableable 之前，16 字节的组件一个 chunk 能装 1000 个 entity；有了 enableable 之后上限砍到 128。"optimal archetype size" 是 ~125 字节——刚好塞满 128 entity。作者的判断是 Unity 大概率对实际项目的 archetype 平均大小做过统计，128 是合理折中；担心 iteration cache miss 的人可以自己测，但先不要过早优化。

## Write permission 的传染

和手写 `bool` + `if (bool)` 的老套路一样：要改变组件的 enable 状态就需要**对该组件的 write access**。`ComponentLookup<T>` 提供 `SetComponentEnabled(entity, bool)`，把 lookup 传进 job 会自动把 write 依赖算到 scheduling 里，后续只读这个组件的 job 会被正确 gate 在之后。

几条可以改 enable 状态的 API 入口：
- **主线程**：`EntityManager` / idiomatic foreach + `EnabledRefRW<T>`。
- **Job 内**：`ComponentLookup<T>.SetComponentEnabled`、`EntityCommandBuffer`（延后执行）。
- **IJobChunk**：`ArchetypeChunk.SetComponentEnabled(typeHandle, index, value)`、`SetComponentEnabledForAll`（整 chunk 翻）。

## Execute 的 entity 范围 ≠ 实际工作的 entity

`matchingEntityCount` 是生成代码里一个看起来多余的计数器。作者没查到它为什么必须存在——猜测是某种 assert 或者帮助 Burst 做循环优化。无论哪种原因，用户写 `Execute` 时不能假设它会按遍历顺序连续运行；受 enableable 影响，它的"跳跃"是可见的。

## 与 IJobChunk 的对比

`IJobEntity` 能被 source generator "贴心地"包一层 `if`；`IJobChunk` 的 `Execute(chunk, ...)` 颗粒度本来就是 chunk，source generator 已经介入不了。Unity 只好把 mask / 辅助函数原样塞给用户，由用户自己在 `Execute` 里遍历 mask 决定哪些 entity 要处理——官方文档里专门有一节讲 `useEnabledMask` 和 `chunkEnabledMask` 的用法。

## 相关
- [[ecs]]
- [[dots-chunk-change-version]]
- [[dots-ecs-cache-iteration]]
- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[sirawat-pitaksarit]]
- [[svelto-filters-api]] — Sebastiano Mandalà 认为 IEnableableComponents 只是 filter 的弱化版，filter 还能表达 ownership relationship 而非仅状态

## Sources

- [[sources/gametorrahod-enableable-generated-code]]
