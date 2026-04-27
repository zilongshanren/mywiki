---
tags: [C++, 性能, final, 去虚化, 编译器优化, benchmark]
date: 2026-04-27
sources: 1
---

# C++ `final` 关键字的性能影响

`final` 关键字用于阻止类被继承，理论上允许编译器对虚函数调用做**去虚化（devirtualization）**优化，直接生成静态调用以省去虚表查找。多篇博客声称它是"几乎免费的性能提升"，但均缺乏实测数据。

## 实测结论（16bpp PSRayTracing 项目）

经过跨三台机器、三个操作系统、三款编译器的 125+ 小时累计测试，结论与宣传出入很大：

- **GCC（Linux/macOS）**：在部分场景有 1–10% 的可重现提升，Apple M1 上收益极为微小
- **Clang（Linux x86_64）**：**超过 90% 的测试用例** 在开启 `final` 后慢了至少 5%，某些场景退步达 17%
- **MSVC（Windows）**：结果混杂，部分场景有提升，部分场景有明显损失
- **Android（Clang 14）**：Pixel 6 Pro 观测到约 6% 的退步；iPhone 12 基本无变化

**核心结论：`final` 对性能的影响与场景中虚对象数量无明显相关性，编译器和平台差异才是主导因素。**

## 为何 Clang 表现差

作者推测 Clang 的去虚化启发式在该场景下未能触发，或反而妨碍了某些内联决策。由于 Clang 也是 iOS / Android 平台的唯一编译器，这对移动端高性能 C++ 应用具有实际意义。同样的问题可能波及 Rust 和 Swift（均基于 LLVM 后端）。

## 与 `noexcept` 的对比

与 [[cpp-noexcept-keyword-performance]] 所记录的结论相似：两个关键字在理论上有性能好处，但实测均表现出高度依赖编译器 + 平台的不稳定特性，难以作为通用优化建议。

## 操作建议

- 除非在目标平台 + 编译器组合上实测验证，否则**不建议将 `final` 作为通用性能技巧**
- 使用 `final` 作为语义标记（禁止继承）是合理的，但不应寄望于性能收益
- 始终通过 A/B 测试量化，而不是相信"就是更快"的断言——参见 [[benchmark-methodology-end-to-end]]

## Sources

- [[sources/16bpp-cpp-final-keyword]]
