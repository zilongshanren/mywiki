---
tags: [source, C++, 性能, final, devirtualization, benchmark, 16bpp.net]
date: 2026-04-27
sources: 1
---

# C++ `final` 关键字的性能影响（16BPP.net）

[[16bpp]] 发表于 2024 年 4 月的文章，以 PSRayTracing 光线追踪器为测试平台，对 `final` 关键字的性能影响进行了 125+ 小时的系统性实验。

## 摘要

多篇博客声称 `final` 可带来"免费"的去虚化提升，但无一提供量化数据。作者通过 CMake 宏控制开关，在 AMD Ryzen 9、Apple M1、Intel i7 三台机器，Linux/macOS/Windows 三个系统，GCC/Clang/MSVC 三款编译器上各运行了 1150+ 测试用例。结果表明：GCC 有时能获得 1–10% 的提升，Clang（尤其 Linux x86_64）超过 90% 的用例出现 5% 以上的退步，MSVC 表现混杂，Apple M1 变化极小。场景中虚对象数量与 `final` 的收益无显著相关性。移动端测试显示 Pixel 6 Pro（Clang 14）退步约 6%。作者个人决定不使用 `final`。

## 关键要点

- Clang 与 `final` 的组合在 x86 Linux 下几乎必然导致退步
- GCC 是最有可能从 `final` 受益的编译器，但也并不稳定
- Apple Silicon 对 `final` 基本免疫，增减均微乎其微
- "test & measure"是唯一可靠策略，不应盲信语言特性的性能声明

## 链接到的概念

- [[programming-languages/cpp-final-keyword-performance]]
- [[programming-languages/cpp-noexcept-keyword-performance]]
- [[computer-systems/benchmark-methodology-end-to-end]]

## 原文

- 链接：https://16bpp.net/blog/post/the-performance-impact-of-cpp-final-keyword/
- 本地：`raw/articles/16bpp.net/2024-04-22_16bpp-net-blog-the-performance-impact-of-c-s-final-keyword.md`
