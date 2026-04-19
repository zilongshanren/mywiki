---
tags: [source, cpp, software-design, benchmark, compiler]
date: 2026-04-19
sources: 1
---

# The Hypothesis（16BPP.net）

[[16bpp]] 发表于 2025 年 11 月的长文，副标题其实就是博文的 slug：`free-functions-dont-change-performance-much`。这是作者性能系列的第 4 篇，跳出 PSRayTracing，改用 [Synfig](https://www.synfig.org/) 矢量动画引擎做 end-to-end 测试床。

## 摘要

Klaus Iglberger 2017 年 CppCon 演讲 *"Free your Functions!"* 留下一句「写成 free function 可能更有性能优势」，之后 8 年无人 benchmark。作者决定把它测一遍（并与 Klaus 邮件往来确认）。

**小 benchmark**：Vec4 的 `normalize` 等操作写成成员函数 / free-pass-struct / free-pass-args 三种，跨 3 CPU × 3 OS × 3 编译器 × 多 `-O` × 4 操作 × 1000 万次 × 100 次迭代 = 576 次 run。**98% 的情况下看不到 10ms 以上的差异**，仅 8 次显著差异全部集中在 Clang/Linux/Intel 的 `normalize(pass-args)` 上（+15%）。

**大 benchmark**：用 Callgrind + KCachegrind 在 680 个 `.sif` 测试文件上采 call graph，选出调用频繁的 `synfig::Color::clamped()` 做三种 free 化（`friend` / `public` 数据成员 / 重构参数），GCC 14.2 `-O3` 跑 **78 小时**。累积耗时差异 **0.5%**，属于噪声；用 Z-score 剔除 outlier 后 free 版本一致快 1.5~2.8%；但某些 `.sif` 文件本身运行时间双峰分布（`164ms ⇄ 114ms`），Z-score 和 IQR 都救不了。

**结论**：free function vs 成员函数**基本没有性能差别**；`public` vs `private` 数据、`friend` vs 成员同样没有差别。这个发现的价值是「没有性能惩罚」——想 free 就 free，别指望它带来速度。

## 关键要点

- 8 年前的性能主张今天未必成立——编译器在偷偷变强，老主张需要重测；
- 小 benchmark 的 15% 亮点在 end-to-end 里消失，这是 [[benchmark-methodology-end-to-end]] 的典型案例；
- Callgrind + KCachegrind 是选「该优化哪个函数」的标准工具；
- Synfig 某些测例**非平稳**，暴露了基准测试里常被忽视的 CPU 动态时钟 / OS 调度噪声；
- 作者顺手推荐 Herb Sutter 的 Cpp2 带 UFCS，能解决 member vs free 的语法分裂；
- 被 Synfig 项目维护者友好对待，鼓励 C++ 学习者去贡献这个被 Blender 掩盖的项目。

## 链接到的概念

- [[free-vs-member-functions-performance]]
- [[benchmark-methodology-end-to-end]]
- [[16bpp]]

## 原文

- 链接：<https://16bpp.net/blog/post/free-functions-dont-change-performance-much>
- 本地：`raw/articles/16bpp.net/2025-11-03_the-hypothesis.md`
