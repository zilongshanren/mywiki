---
tags: [ray-tracing, cpp, project, benchmark]
date: 2026-04-19
sources: 3
---

# PSRayTracing

[PSRayTracing](https://github.com/define-private-public/PSRayTracing)（下称 PSRT）是 [[16bpp]] 基于 Peter Shirley 的 *Ray Tracing in One Weekend* / *Ray Tracing: The Next Week* 书系写的 C++ 重写版，从 2020 开始维护。它本身是一个标准的 CPU 路径追踪器（与 [[path-tracing-basics]] / [[path-tracing-monte-carlo]] 是同一条路线），但在作者手里真正的用途是**性能实验的测试床**——作者连续几年在它上面测 C++ 关键字、编译器选项、采样算法、数学函数近似。

## 与原书的差别

- **C++17**，大量用 `constexpr`、`std::variant`；
- 默认用 **[PCG](https://www.pcg-random.org/)** 随机数引擎（比 libstdc++ 的 Mersenne Twister 快且不易耗尽），见 [[inversion-sampling-prng]]；
- 场景拆成 20 个独立 benchmark scene（`book1::final_scene`、`book2::bouncing_spheres`、各种 `with_bvh` 变体）；
- 三角函数默认用近似版（参见 [[asin-cg-approximation]]），精度敏感时可编译开关切换；
- 标配 CMake Release / RelWithDebInfo / `Callgrind` 一键测评脚本。

## 在这里测过的结论

- **`final` 关键字对性能基本没有影响**（第一篇文章）；
- **`noexcept` 有时帮忙、有时伤害**（第二篇）；
- **[[rejection-vs-analytical-sampling]]**：拒绝采样在打开 `-O1` 后一律胜过解析方法；
- **[[free-vs-member-functions-performance]]**：在 Synfig 上也证伪「free function 更快」的流传；
- **[[asin-cg-approximation]]**：Nvidia Cg 的 Minimax 公式比自己搓的 Taylor / Padé 都快；
- **[[estrin-scheme]]**：把 Horner 改成 Estrin 再吃 +17%。

每一篇的原始 benchmark 数据（Google Sheet、Jupyter notebook、CSV）都随文章挂出来。

## 方法论共性

作者的测法见 [[benchmark-methodology-end-to-end]]：矩阵测试（3 CPU × 3 OS × 3 编译器 × 多 `-O`）、最终必须回到端到端渲染而非 microbench、至少 25 次样本取中位数、小于 2% 的差异视为噪声。

## 相关

- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[16bpp]]
- [[rejection-vs-analytical-sampling]]
- [[asin-cg-approximation]]
- [[estrin-scheme]]
- [[free-vs-member-functions-performance]]
- [[benchmark-methodology-end-to-end]]

## Sources

- [[sources/16bpp-greedy-vs-analytical]]
- [[sources/16bpp-free-functions-hypothesis]]
- [[sources/16bpp-quicker-trig-asin-cg]]
