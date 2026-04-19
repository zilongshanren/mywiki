---
tags: [unity, dots, ecs, cache, simd, burst]
date: 2026-04-19
sources: 1
---

# DOTS 的 Cache 视角：RefRO/RefRW 与 Burst 向量化

理解 DOTS 性能最实用的入口是**脑子里画出 chunk 的线性内存布局**，然后看 `foreach`/`IJobEntity` 的每一步实际上在 cache line 里摸到什么。Sirawat 的 "Thinking in Cache" 沿着一个简单的 `b.Data += a.Data + c.Data` 例子把这层思维展开。

## Chunk 的三条轨道

一个 chunk 里不同 component 各占一段**连续原生数组**：

```
[a, a, a, ..., a][b, b, b, ..., b][c, c, c, ..., c]
```

Iteration 的第 i 次拿到三个 ref，都指向**各自轨道的第 i 个元素**。这是 [[aos-vs-soa|SoA]] 的直接实现。`int` 组件 4 B × 16 个正好占一条 64 B cache line——第一次 Execute 在 A/B/C 各触发一次 miss，第二到第十六次都是全 hit，这就是"小 component + 多 system"在 DOTS 里自动拿到的性能红利。

## `in` / `ref` / `RefRO` / `RefRW` 的真实含义

`IJobEntity`：
```csharp
public void Execute(in ComponentA a, ref ComponentB b, in ComponentC c) {
    b.Data += a.Data + c.Data;
}
```

`in` ≈ `readonly ref`，`ref` 就是 ref——两者都**按引用**传而不是按值。直接按值传意味着调用方就要做解引用 / 拷贝，即便分支里根本没读这个 component，cache 已经被 dirty 过了。用 `in`/`ref` 延迟到用户代码第一次 touch 时再碰 cache，多组件 query 里没实际用的那几个就不浪费带宽。

Idiomatic `foreach` 不允许加 `ref`/`in`，所以用 `RefRO<T>` / `RefRW<T>` 包装——它们的 `.ValueRO` / `.ValueRW` 是 property，property body 里做解引用，语义上等价于 `in`/`ref`。多打两个点、不改语义。

## Burst 的自动向量化

Burst 看到循环体 `b += a + c + 1234` 会尝试重写成"一次 iteration 做 16 个元素"的 vector code。作者用 AVX2 target 看 Burst Inspector：编译器把 `1234` broadcast 到 256-bit 的 `ymm0`（8 个 int），然后同时用 `ymm1` 和 `ymm2` 双路处理——一次 loop iteration 实际覆盖 16 个 int、跨 64 B cache line 恰好吻合。

剩下不足 16 的尾巴 Burst 自动生成标量 fallback——`add / cmp / jne` 一次处理一个 int。手写这种 tail handling 在每个循环都要重复一遍，机器做比人做稳。

## 为什么 GameObject 拿不到这个红利

GameObject 数组 = **指针数组**。iteration 第 i 次 dereference 一次拿到一个 `GameObject`，它的 `Transform` / `ScriptA` / `ScriptB` 又各自是堆上不知何处的对象。cache line 的"邻居"是下一个 **指针**，不是下一个 `ScriptA`。访问一个 component 多半是一次 miss，访问多个 component 是多次 miss——GameObject 的 layout 天生和 cache 不兼容，DOTS 的内存模型是对这个历史包袱的彻底替换。

## 大 component 也不是灾难

真实项目的组件不会都是 `int`——字段可能掺 `bool`、引用、嵌套 struct。Sirawat 的看法是**不用强行追求组件 <= cache line**：复杂组件在 cache 上表现退化，但 Unity 在内部对 struct alignment / 字段顺序做了不少优化，"通常仍然比 GameObject 好"。真正意识到 cache 的场景是"某个 hot 循环只碰大组件的一两个字段"——那时可以把这些字段拆出来做独立组件（小 component 原则的另一个来源）。

## 与 Amdahl / 并行的关系

在 [[amdahls-law|Amdahl 定律]]里，DOTS 的核心贡献是**让更多代码能并行**（提高 p 值），不是单纯加核。Cache-friendly 内存 → Burst 向量化 → Job System 多线程调度，三层都依赖同一个前提：**数据按 component 列连续存放**。缺了它，后两层都打折。

## 相关

- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[ecs]]
- [[dots-chunk-change-version]]
- [[dots-enableable-components]]
- [[amdahls-law]]
- [[fearless-simd]] — 另一条 SIMD 视角
- [[sirawat-pitaksarit]]

## Sources

- [[sources/gametorrahod-thinking-in-cache]]
