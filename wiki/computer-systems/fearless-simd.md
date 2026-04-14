---
tags: [simd, rust, 性能, 运行时派发]
date: 2026-04-14
sources: 1
---

# Fearless SIMD：Rust 下的可移植 SIMD 愿景

**"Fearless SIMD"** 是 [[raph-linus]] 借用 Rust 社区"fearless concurrency"口号提出的目标：程序员用高层、可组合、**安全**的原语描述一次向量计算，编译器负责把它展开成目标架构上**近乎最优**的代码，运行时自动选出当前 CPU 支持的最佳档位。2018 年他写这篇文章时，Rust stable 刚刚让 SIMD 落地，但距离"fearless"还差很远——他发布了一个同名探索性 crate 来试水。

## 两层难题

写 SIMD 难有两个层次：

- **编译期选档**：Rust 的 `-C target-cpu` 配合 `#[cfg(target_feature = "...")]` 就能让代码为一个特定 CPU 编出最好的那版。缺点是 binary 只能在那台机器上跑。
- **运行时选档（真正难的那层）**：把多档（SSE / AVX / AVX2 / AVX-512、Neon …）编进同一个 binary，启动时检测 CPU 再挑。Rust 当时只给了原料：`#[target_feature(enable = "avx")]` 函数属性 + `is_x86_feature_detected!` 宏，**正确组合全靠程序员自己**，并且**被 target_feature 标注的函数必须声明为 `unsafe`**——编译器无法替你证明运行时真的具备这个 feature，直接调就是 UB。

结果一个典型 runtime 选档函数长这样：

```rust
#[target_feature(enable = "avx")]
unsafe fn foo_avx(...) { let ... = _mm256_add_ps(..., ...); }

fn foo(...) {
    if is_x86_feature_detected!("avx") {
        unsafe { foo_avx(...); }
    } else {
        foo_fallback(...);
    }
}
```

要写 AVX2、AVX-512、Neon、scalar fallback 四五个版本，每个都这样复制一份——显然不叫 fearless。

## inlining 的深渊

真正让人想掀桌子的是：一旦 SIMD 逻辑要跨多个函数组合，`#[cfg(target_feature)]` 就失效。原因是它在**编译早期**解析，看不到调用方是不是 `#[target_feature(enable=...)]`。换句话说，一个内联函数不知道自己被内联到的上下文里已经启用了什么 feature。Raph 认为这是**语言层面**的深度问题，不是靠补丁能解决的。叠加 rust-lang/rust#50154——不同 calling convention 之间 inline 的编译器 bug——写可组合 SIMD 在当时是雷区。

## 双层 trait 的方案

Raph 的 `fearless_simd` 用两层 trait 绕开这些坑：

- **底层 trait**：抽象某种 SIMD vector。`F32x4` 表示定宽四路，`SimdF32` 表示"原生宽度的 f32 vector"。实现是对 `__m256` / `__m128` 等 arch 类型的 **newtype**，运算符通过 `std::ops` 暴露，用户写 `a + b` 而不是 `a.add(b)`。
- **高层 trait**：表示一次用户计算（例如 `SimdFnF32` 是 `f32 -> f32` 的点式函数，`Thunk` 是任意随机访问的 compute block），**对底层 trait 泛型**。
- **Runner**：架构特定的入口，做 runtime 检测，调用对应的具体 `Simd` 类型——这里有一次 unsafe 但被安全地封装在 runner 里。

这套结构利用了 Rust 的 **monomorphization**：一个泛型计算会被**自动**单态化出每种 SIMD level 的一份代码，包括 scalar fallback。"创建一个具体 SIMD 类型"是 unsafe 动作（因为要断言 runtime 检测结果为真），但**使用**它是 safe。

## 性能证据

作者给了 sinewave 生成的 benchmark（i7-7700HQ，生成 64 个样本的耗时）：

| CPU | SIMD | 时间 |
|---|---|---|
| i7-7700HQ | AVX | 30 ns |
| " | SSE 4.2 | 49 ns |
| " | scalar fallback | 344 ns |
| " | `sin()` 标量 | 506 ns |

AVX 版本每样本约 **470 皮秒**——证明 Rust monomorphized 代码的 codegen 质量确实能吃到硬件上限。

## 与其他方案的对比

- **`packed_simd`**：提供架构无关的 `f32x4` 类型和运算——**但不解决 runtime 选档**
- **`faster`**：更高层、iterator 风格——同样不解决 runtime 选档
- **`simdeez`**：为 runtime 选档而设计，但把架构特定 shim 留给用户写，仍需大量 unsafe
- **Intel ISPC**：C 的 SIMD 方言语言扩展，可以同时做 SIMD + 多核并行，类似 rayon；思路比 Rust 当时任何 crate 都激进
- **Halide**：图像处理专用的 DSL，同时目标 SIMD 和 GPU compute；对音频 workload 不太合适

Raph 的判断：Rust 最终恐怕需要**语言级别**的增强（比如类似 GCC / Clang 的 function multi-versioning 语义，或把 `for<S: SimdF32>` 这种 higher-ranked generics 变成现实），才能让 fearless SIMD 真的 fearless。

## 历史评价

这篇文章成了后续 Rust SIMD 抽象的重要参照——`wide` crate、Rust 的 `std::simd`（portable_simd 提案）、以及 Raph 自己后来在 Vello / piet-gpu 里写的 GPU compute 代码，都继承了"让安全代码吃满硬件"的设计哲学。fearless_simd 本身停留在探索阶段，但它**把痛点清单列清楚**了，这个贡献比 crate 本身持久。

## 相关

- [[sse-tricks]]
- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[flynn-taxonomy]]
- [[raph-linus]]

## Sources

- [[sources/raphlinus-fearless-simd]]
