---
tags: [source, unity, dots, ecs, cache, simd, burst]
date: 2026-04-19
sources: 1
---

# Thinking in Cache（Sirawat Pitaksarit / Game Torrahod）

[[sirawat-pitaksarit]] 2024 年 5 月写的 DOTS 性能心智模型入门：把 chunk 画成并排的三条连续数组、把 `RefRO`/`RefRW` 的作用解释清楚、用 Burst Inspector 看自动向量化。

## 摘要

一个 chunk 里每个 `IComponentData` 各占一段连续原生数组：`[a,a,a,...][b,b,b,...][c,c,c,...]`——[[aos-vs-soa|SoA]] 的直接实现。`foreach` 第 i 次 iteration 拿到的三个 ref 都指向"各自轨道的第 i 元素"。`int` 组件 4 B，一条 64 B cache line 装 16 个；第一次 Execute 在 A/B/C 各一次 miss，之后 15 次全 hit——"小 component + 多 system" 自动拿到的红利。

`in`/`ref`（`IJobEntity`）和 `RefRO<T>.ValueRO` / `RefRW<T>.ValueRW`（idiomatic `foreach`）在语义上等价：按引用传、用户代码第一次 touch 时才碰 cache。直接按值传意味着 Source Generator 在调你之前就解引用、dirty cache——分支里没用到的组件白占带宽。

Burst + AVX2 的自动向量化：对 `b += a + c + 1234`，Burst 广播 `1234` 到 256-bit `ymm0`（8 个 int），双路用 `ymm1`/`ymm2`，一次 iteration 覆盖 16 个 int（正好一条 64 B cache line）；不足 16 的尾巴自动生成 `add/cmp/jne` 标量 fallback。作者用 "Coloured With Full Debug Information" 模式在 Burst Inspector 里对着粉色（`v` 前缀 = vector 指令）确认。

GameObject 数组为什么拿不到同样的红利：它是**指针数组**，一次 dereference 得到 `GameObject`，它的各个组件又散在堆上——cache line 的邻居是下一个指针，不是下一个 `ScriptA`。访问一个组件 = 一次 miss；访问多个 = 多次 miss。DOTS 的内存模型是对这个包袱的彻底替换。

## 关键要点

- Chunk = 多条并排的连续 native array，`IJobEntity` 的每个 ref 指向独立轨道的 i 号元素。
- `in` / `ref` / `RefRO.ValueRO` / `RefRW.ValueRW` 的 property 实现是"按引用、触达时才读"——节省未使用组件的 cache 污染。
- Burst + AVX2 自动把 scalar loop 改写成 SIMD，256-bit 双路一次覆盖 16 int + 标量 tail handling。
- 复杂大组件（含 bool / 引用 / 嵌套 struct）不用强行拆小——Unity 内部做了 struct alignment，性能仍优于 GameObject。
- 与 [[amdahls-law|Amdahl 定律]]关系：DOTS 的贡献是**提高可并行部分 p 的比例**，靠 cache-friendly + Burst + Job System 三层叠加。

## 链接到的概念

- [[dots-ecs-cache-iteration]]
- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[fearless-simd]]
- [[amdahls-law]]

## 原文

- 链接：https://gametorrahod.com/thinking-in-cache/
- 本地：`raw/articles/gametorrahod.com/2024-05-14_thinking-in-cache.md`
