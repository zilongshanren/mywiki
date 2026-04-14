---
tags: [source, rust, 汇编, 编译器, 性能]
date: 2026-04-14
sources: 1
---

# Rust Disassembly: part 1（Marco Giordano / A programmer's cave）

[[marco-giordano]] 发表于 2020 年 5 月的文章，把 Rust 的几个常用语言特性丢进 Compiler Explorer 看它们到底编译成什么汇编，验证"零成本抽象"名副其实的程度。

## 摘要

文章以一个 C/C++ 性能控初次接触 Rust 的视角写成，挑了四个特性做汇编对照：`i128` 整数、元组解构 destructuring、定长数组 `[i32;N]` 索引、以及 `for var in slice.iter()` 式的迭代器循环。结论与作者最初的预期有偏差——**边界检查在单次访问里开销近乎零，而 iterator 写法反而比裸循环更容易被 LLVM 向量化**。`i128` 是用两个 64-bit word + `adc`/`mul` 软件实现的；元组解构和字段访问生成完全相同的汇编，都是静态偏移寻址；定长数组索引在编译期已知下标时零成本，运行期下标时会带一次 `cmp + ja` 边界检查并在越界分支触发 `panic_bounds_check` 加一条 `ud2`（invalid opcode 硬件陷阱）。最有意思的对比发生在循环：`while idx < b` + `a[idx]` 编译出 5 路循环展开但**没有** SIMD；`for var in a.iter()`、`a: &[i32;8]` 直接变成 `movdqu / paddd / pshufd` tree reduce 的 128-bit SIMD 加法，而且完全**没有**边界检查。作者借此指出 Rust 推崇 iterator 不是风格偏好，而是为了让编译器能证明访问安全。文章结尾补充了 `ud2` 指令的来源——LLVM 的 "trap after unreachable" 开关，由 Rust PR #45920 启用。

## 关键要点

- `i128` 是纯软件两 word 实现：`add128` 用 `add + adc`，`mul128` 用 `mul + imul` 拼接高低位
- 元组解构 `let (_,_,z) = a` 与字段访问 `a.2` 生成完全相同的汇编（`movss xmm0, [rdi+8]`）
- tuple 不支持运行期下标 `a.b`，因为字段类型可异构，编译期无法推断返回类型
- 定长数组编译期下标 → 单条 `mov` 指令；运行期下标 → `cmp + ja + panic_bounds_check + ud2` 一套边界检查
- `ud2` 是 LLVM 在不可达代码后插入的硬件陷阱指令，由 Rust PR #45920 启用
- `while + 索引` 循环虽被展开但每步都要做 `cmp` 边界检查，且没有向量化
- `for ... in slice.iter()` 让编译器看到访问范围，**自动 SIMD**、**完全消除边界检查**
- 这解释了为什么 Rust 社区推崇 iterator + zip/map/filter 链式写法——不是美学，是 vectorizer 的必要条件

## 链接到的概念

- [[rust-disassembly-tour]]
- [[fearless-simd]]
- [[compilation-pipeline]]
- [[marco-giordano]]

## 原文

- 链接：https://giordi91.github.io/post/disassemlbyrust1/
- Compiler Explorer：https://godbolt.org/z/Xbf-7u
- 本地：`raw/articles/giordi91.github.io/2020-05-23_rust-disassembly-part-1.md`
