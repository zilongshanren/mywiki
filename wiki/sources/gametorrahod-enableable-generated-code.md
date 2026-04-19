---
tags: [source, unity, dots, ecs, source-generator]
date: 2026-04-19
sources: 1
---

# Enableable Components Generated Code（Sirawat Pitaksarit / Game Torrahod）

[[sirawat-pitaksarit]] 2024 年 5 月的博客，解剖 Unity DOTS `IEnableableComponent` 背后 Roslyn Source Generator 生成的代码。

## 摘要

作者写一个最简单的 `IJobEntity.Execute(ref Counter c) { c.Value += 1234; }`，在 Burst 汇编里搜到 `1234` 出现 **8 次**——`Execute` 被不同分支的代码复用编译了多份。翻开 Source Generator 生成的 partial half，里面是一个三路状态机：(1) **`!useEnabledMask`**——组件无 `IEnableableComponent`，朴素 for；(2) **Use-ranges mode**——`edgeCount = countbits(mask ^ (mask << 1)) <= 4` 时，把 128-bit mask 按"连续 1 片段"跳着扫，`UnsafeTryGetNextEnabledBitRange` 找下一段，内层 while 在段内全扫；(3) **Per-bit loop**——变化边过多时，64-bit + 64-bit 一位一位测 `(mask & 1)`。

为什么非 Source Generator 做不到：判断是否 execute 依赖 query 的具体组件，在编译期展开才能保留 Burst inline 和 SIMD 友好。mask 是 `v128` → `MaximumChunkCapacity = 128`——原本 16 B 组件一 chunk 能装 1000 entity，有 enableable 后硬上限 128。"最佳 archetype 尺寸" ~125 B 正好塞满 128 entity。

作者给的工程建议："不要为 enableable 做性能优化"——该 toggle 就 toggle，相信 Unity 团队做过实测权衡；要写的 `ComponentLookup<T>.SetComponentEnabled` / `EntityCommandBuffer` 会自动把 write 依赖算进 scheduling。

## 关键要点

- Source Generator 给同一 `Execute` 生成 3 条路径，编译期展开保留 Burst 的向量化和 inline。
- `edgeCount <= 4` 才走 range 模式——偶尔 disable 或整段 disable 是甜蜜点，均匀穿插最贵。
- `v128` mask 把 chunk 容量从可变上限钉死到 128 entity（配套 `MaximumChunkCapacity = 128`）。
- 改 enable 状态需要**该组件 write 权限**，传 `ComponentLookup<T>` 进 job 会把写依赖加进 scheduling。
- `IJobChunk` 粒度是 chunk，Source Generator 无法"帮你包 if"——需要自己遍历 mask。

## 链接到的概念

- [[dots-enableable-components]]
- [[ecs]]
- [[dots-chunk-change-version]]
- [[dots-ecs-cache-iteration]]

## 原文

- 链接：https://gametorrahod.com/enableable-generated-code/
- 本地：`raw/articles/gametorrahod.com/2024-05-03_enableable-components-generated-code.md`
