---
tags: [sampling, monte-carlo, ray-tracing, benchmark, compiler-optimization]
date: 2026-04-19
sources: 1
---

# 拒绝采样 vs 解析采样：谁更快不取决于数学

在单位圆盘 / 单位球内均匀采样是 [[path-tracing-basics]] 和 [[inversion-sampling-prng]] 里反复出现的子问题。*Ray Tracing in One Weekend* 的原版实现是拒绝采样（rejection sampling）：在 $[-1, 1]^n$ 立方体里均匀撒点，落在单位球外的扔掉重来。这个写法有几个让人直觉不适的地方——理论上的无限循环、分支预测失败、「浪费掉的随机数」。

于是就有了直觉上的解析解：在极坐标下生成 $r$ 和 $\theta$，再用三角函数变到笛卡尔。这路子看上去优雅、没有循环、不浪费随机数，按[[inversion-sampling-prng]]的框架也是标准答案。

## 数学上的命中率

- **2D**：$\pi r^2 / (2r)^2 = \pi / 4 \approx 78.54\%$，约 22% 点要扔掉。
- **3D**：$\tfrac{4}{3}\pi r^3 / (2r)^3 = \pi / 6 \approx 52.36\%$，接近一半要扔掉。

3D 的情况尤其糟糕，看似是解析解必胜的铁证。

## 解析 2D 正确写法

关键坑：$r \sim U(0, 1)$ 会让点朝圆心堆积（圆周上 $dr$ 对应的环面积 $\propto r$），必须 $r = \sqrt{U(0,1)}$；3D 对应 $r = \sqrt[3]{U(0,1)}$。忘带这个 Jacobian 就得到「中心偏亮」的非均匀分布。

## 然后测一下——结果完全反直觉

16BPP.net 的作者在 PSRayTracing 中把原来的拒绝采样改成解析方法，默认场景的渲染时间从 **105.9s 涨到 118.4s**——解析方法反而更慢。

进一步做独立的 C++ microbench，`-O0` 下解析方法确实快 10~33%；**一旦打开 `-O1` 及以上，拒绝采样反超 50% 甚至更多**。在 10 机型 × 多编译器 × 多 `-O` 级别 共 48 个组合的全矩阵下，结论大致是：

- **Linux + GCC**：拒绝采样几乎全胜，`-O1` 就够；
- **Linux + Clang**：大多数情况解析更快，`-Ofast` 例外；
- **Windows + GCC / MSVC**：拒绝采样稳胜，2D 常见 +150% 速度；
- **macOS + Apple M1 + GCC**：拒绝采样全胜（除 `-O0`）；
- **macOS + Apple M1 + Clang**：2D 拒绝更快、3D 解析更快。
- **AMD** 与 Intel 行为一致。

然后再把这两种实现插回 PSRayTracing，用 20 个场景 × 50 次各两种实现的实际渲染作验证（总计几百小时机时），结论是**拒绝采样整体更快，有时差距悬殊**；解析方法占优的场景恰好是那些不带 [[bvh]] 的 baseline 场景，一旦打开 BVH（即真实 ray tracer 的使用方式），拒绝采样就重新胜出。

## 为什么？`-O3` 下的汇编

- **拒绝版本**在 `-O3` 下被内联成约 45 条指令、0 次 `call`，配合 CPU 的分支预测器，22% 的重采样几乎是白嫖。
- **解析版本**则无法内联 `sqrt()`、`sin()`、`cos()`、`sincos()`——这些是 libc 调用，每次都有真实的 `call` 开销。约 55 条指令 + 2 次 `call`，还没算 `sqrt`。

用「指令条数更少」「不调用库函数」这种纸上优化来判断性能，在打开优化器之后完全失效——这是本篇最大的教训。

## Rust 的横向验证

作者第一次写 Rust 也把同一个 benchmark 移过来，`rustc --release` 的行为与 C++/GCC 一致：Debug 下解析更快，Release 下拒绝更快，数量级也接近。这说明这不是 C++ 或特定编译器的特殊现象，而是**LLVM/GCC 优化器 + 现代 CPU 对短循环+分支预测的普遍偏好**。

## 工程结论

- **PSRayTracing 最终保留拒绝采样**。
- 「看上去更优雅的数学」并不一定更快，编译器会把简单循环 + 分支预测器用到极致。
- 再次印证 [[benchmark-methodology-end-to-end]]：microbench 换到真实应用可能完全反转；`-O0` 下的测量几乎没有参考价值。
- 和[[inversion-sampling-prng]]的对比：理论上 inversion 是 100% 命中的最优方案，但「理论最优」并未转化为「运行时最快」。图形里真正决定速度的是超越函数调用、内联能力和分支预测。

## 相关

- [[inversion-sampling-prng]]
- [[path-tracing-basics]]
- [[benchmark-methodology-end-to-end]]
- [[psraytracing]]
- [[faster-math-functions]]

## Sources

- [[sources/16bpp-greedy-vs-analytical]]
