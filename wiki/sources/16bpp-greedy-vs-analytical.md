---
tags: [source, benchmark, sampling, cpp, compiler, ray-tracing]
date: 2026-04-19
sources: 1
---

# When Greedy Algorithms Can Be Faster（16BPP.net）

[[16bpp]] 发表于 2025 年 1 月的长文，以 PSRayTracing 的单位圆盘 / 球内均匀采样为切入，测拒绝采样（rejection sampling）与解析解（polar coordinates + `sqrt`）的实际速度。作者自己承认标题取得糟糕（rejection 并不是严格意义上的 greedy algorithm，reddit 被吐槽），但内容本身是他性能系列里分量最重的一篇。

## 摘要

2D 拒绝采样命中率 ~78.54%，3D 只有 ~52.36%，直觉上解析方法必胜。作者做出解析实现并塞回 PSRayTracing，**结果渲染耗时反而从 105.9 秒涨到 118.4 秒**。剥离 ray tracer 做独立 C++ microbench，`-O0` 下解析 10~33% 更快，打开 `-O1` 后拒绝反超 50%+。作者跨 Intel i7 / AMD Ryzen 9 / Apple M1 × Windows/Linux/macOS × GCC/Clang/MSVC × 多 `-O` 共 48 组合做矩阵测试，并同时用 Rust 做横向验证（Debug 解析更快、Release 拒绝更快，与 C++ 一致）。结论：**拒绝采样在开优化后几乎全面胜出**，最后 PSRayTracing 保持拒绝采样不变。

## 关键要点

- **数学直觉与编译后性能无关**：解析方法指令略少，但 `sqrt` / `sincos` 是 libc 调用无法内联，`-O3` 下拒绝版 45 条指令 0 次 `call` 完爆 55 条指令 + 2 次 `call` 的解析版；
- **`-O0` 下的测量几乎无意义**——所有反例都在优化打开后反转；
- **Linux + GCC** 上拒绝采样全胜；**Linux + Clang** 多数情况解析更快；**Windows 两编译器**都拒绝胜；**Apple M1** GCC 拒绝胜、Clang 看维度；
- 真实场景测试（20 scene × 50 runs × 2 方法）证实端到端与 microbench 一致；少数非 BVH 场景是例外；
- **Rust + LLVM** 与 C++ + GCC 行为一致——结论不是 C++ 特有；
- 「**代码的秒表永远比数指令可靠**」——本系列一再强调。

## 链接到的概念

- [[rejection-vs-analytical-sampling]]
- [[benchmark-methodology-end-to-end]]
- [[inversion-sampling-prng]]
- [[psraytracing]]
- [[16bpp]]

## 原文

- 链接：<https://16bpp.net/blog/post/when-greedy-algorithms-can-be-faster>
- 本地：`raw/articles/16bpp.net/2025-01-28_16bpp-net-blog-when-greedy-algorithms-can-be-faster.md`
