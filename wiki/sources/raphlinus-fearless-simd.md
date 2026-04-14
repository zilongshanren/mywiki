---
tags: [source, rust, simd, 性能]
date: 2026-04-14
sources: 1
---

# Towards fearless SIMD（Raph Levien / raphlinus.github.io）

[[raph-linus]] 发表于 2018 年 10 月的文章，为 Rust 编写**可移植、运行时自动选档的 SIMD 代码**勾勒愿景，并发布了探索性 crate `fearless_simd`。

## 摘要

Raph 认为 Rust 有潜力成为写 SIMD 的首选语言，对标口号是「fearless SIMD」——呼应 Rust 的「fearless concurrency」。他先指出 SIMD 的难处来自两层：**编译期选档**（根据目标 CPU 的 feature 选最好的一版）和**运行时选档**（把多版本编进同一个 binary、启动后根据 CPU 再选）。前者靠 `target-cpu` + `#[cfg(target_feature=...)]` 能解；后者 Rust 当时只给了原料（`#[target_feature(enable="avx")]` 函数属性、`is_x86_feature_detected!` 宏），正确组合全靠程序员自己，并且**`target_feature` 函数必须是 unsafe**，因为编译器无法静态证明运行时真的具备该 feature。当逻辑要跨多个函数组合时就崩了：`#[cfg(target_feature)]` 在编译太早阶段解析，看不到调用方 `target_feature(enable)` 的上下文；rust-lang/rust#50154 等 inlining 调用约定 bug 进一步放大痛苦。

Raph 的 `fearless_simd` crate 用**双层 trait**做尝试：底层 trait 抽象 SIMD vector（比如 `F32x4`、原生宽度的 `SimdF32`），实现是对 `__m256` 等 arch 类型的 newtype，运算符通过 `std::ops` 暴露；上层 trait 表示用户的计算（generic over 实现），由 arch 特定的 runner 做 runtime 检测后 monomorphize 成多个版本，包括 scalar fallback。benchmark 里 sinewave 生成在 i7-7700HQ 上 AVX 比 scalar fallback 快 10 倍以上，单样本耗时约 470 皮秒。文章也批评 `packed_simd` 和 `faster` crate 都没解决 runtime 选档问题，并把 Intel ISPC、Halide 作为语言级别的参照物。

## 关键要点

- **SIMD 的两层难题**：编译期选档（能解）+ 运行时选档（Rust 当时只有原料没有组装）
- **`#[target_feature]` 必须 unsafe**：不加 runtime 检测直接调是 UB；编译器无法替你证明
- **inlining 与 target_feature 的冲突**：`#[cfg(target_feature)]` 解析过早，看不到调用方 enable 的上下文——作者认为这是深度语言问题
- **双层 trait 方案**：底层 trait 抽象硬件 SIMD 类型、高层 trait 抽象可被多版本单态化的计算
- **newtype + trait 的安全封装**：「创建 SIMD 类型」是 unsafe（需 runtime 检测），之后的使用是 safe
- **monomorphization 免费多版本**：Rust 的泛型单态化天然生成每种 SIMD level 的一份代码（含 scalar fallback）
- **性能证据**：AVX sinewave 生成 30ns / 64 样本，比 `sin()` 标量快 ~17×
- **竞品对比**：packed_simd 做抽象不做 runtime 选档；`faster` 提供 iterator 风格；`simdeez` 做 runtime 但仍要写 unsafe；ISPC / Halide 是语言级方案
- **周边 Rust 语言痛点**：runtime feature 检测与 target_feature 不完全对应（用户可能想手动降档）；`1.0 + x` 反向运算符、higher-ranked generics、generic associated types 都会让抽象更漂亮

## 链接到的概念

- [[fearless-simd]]
- [[sse-tricks]]
- [[flynn-taxonomy]]

## 原文

- 链接：https://raphlinus.github.io/rust/simd/2018/10/19/fearless-simd.html
- 本地：`raw/articles/raphlinus.github.io/2018-10-19_towards-fearless-simd.md`
