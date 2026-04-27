---
tags: [source, C++, 性能, noexcept, STL, vector-pessimization, benchmark, 16bpp.net]
date: 2026-04-27
sources: 1
---

# `noexcept` 有时有益有时有害（16BPP.net）

[[16bpp]] 发表于 2024 年 8 月的文章，延续 `final` 实验的方法论，对 `noexcept` 关键字的性能影响进行了 370 小时累计测试。

## 摘要

作者以相同的 PSRayTracing 项目构建 `NOEXCEPT` 宏，在 10 种芯片/OS/编译器配置下各运行 50 次全场景测试。整体结论：`noexcept` 对性能的影响基本可视为噪声（±1–2%），仅 AMD+Ubuntu+GCC 配置在 Book 1（顺序搜索 `std::vector` 场景）下观测到一致的 6–8% 提升，归因于 vector 在 move-noexcept 路径下的优化。文章还补充了一个最小化 `std::vector` 搜索基准，验证了跨 x86 配置的小幅加速；但在完整程序中这一效果无法重现（Apple Silicon 无加速），说明孤立组件的 microbenchmark 不能代表系统级性能。Intel+Windows+MSVC 的 Perlin Sphere 场景出现 -10% 退步，原因未解。文章附加了 Hacker News 评论区的"vector pessimization"讨论，以及 `noexcept` 通过 ABI 边界影响代码生成的进阶案例。

## 关键要点

- `noexcept` 主要性能杠杆是 `std::vector` 的 move-vs-copy 路径选择
- 孤立基准（microbenchmark）的加速不代表整体程序的真实收益
- 作者的最终决定：关闭 `noexcept`，保留其作为文档工具的价值
- 完整程序中唯一显著提升仅出现在一种特定配置，说明效果高度平台相关

## 链接到的概念

- [[programming-languages/cpp-noexcept-keyword-performance]]
- [[programming-languages/cpp-final-keyword-performance]]
- [[computer-systems/benchmark-methodology-end-to-end]]
- [[programming-languages/throwing-destructor-noexcept-terminate]]

## 原文

- 链接：https://16bpp.net/blog/post/noexcept-can-sometimes-help-or-hurt-performance/
- 本地：`raw/articles/16bpp.net/2024-08-05_https-16bpp-net-blog-post-noexcept-can-sometimes-help-or-hur.md`
