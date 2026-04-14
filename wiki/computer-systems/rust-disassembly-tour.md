---
tags: [rust, 汇编, 编译器, 性能]
date: 2026-04-14
sources: 1
---

# Rust 语言特性反汇编导览

把 Rust 的几个语言特性丢进 [compiler explorer](https://godbolt.org) 看它们编译成什么汇编，是理解「零成本抽象」到底是不是真的零成本的最直接办法。[[marco-giordano]] 在 2020 年的这篇文章里挑了四个对 C/C++ 出身的性能控来说最"可疑"的点：`i128` 整数、元组解构、定长数组索引、以及 `for var in slice.iter()` 式的迭代器循环。结论基本是两句话——**显式的边界检查没有想象中可怕，而 iterator 模式反而是最容易被编译器 SIMD 掉的写法**。

## i128：纯软件两 word 实现

`add128` 编译出来是一次 `add` 配一次 `adc`（add with carry）；`mul128` 是一次 `mul` 加几条 `imul`/`add` 做高低位拼接。没有魔法，也没有硬件 128-bit ALU，就是两个 64-bit word 拼起来跑。知道这一点，就知道 `i128` 不会比手写的 128-bit 结构慢，但也别期待它能比 64-bit 快。

## 元组解构：纯纯的偏移寻址

`let (_, _, z) = a` 和 `a.2` 生成的汇编完全一样，就是 `movss xmm0, [rdi + 8]` 一条指令。解构在语义上看起来像是在"拆"tuple，实际上编译器早就把它折叠成了静态偏移。唯一的限制是下标必须是编译期常量——`a.b` 这种运行期下标是语法上不合法的，因为 tuple 字段可以是异构类型，编译器没法在不知道 `b` 的情况下推断返回类型。

## 数组索引：Rust 边界检查的两种面貌

定长数组 `&[i32;5]`：
- 编译期常量下标 → `mov eax, [rdi + 16]` 一条指令，和 C 无异。
- 运行期下标 → 先 `cmp rsi, 4` / `ja .panic`，越界就直接跳进 `core::panicking::panic_bounds_check`，panic 之后 LLVM 还会插一条 `ud2`（invalid opcode）做硬件级陷阱，确保不可达代码真的执行不到。关于 `ud2` 的来源，作者特地追到 Rust 编译器打开 LLVM 的 "trap after unreachable" 选项那个 PR（#45920）。

边界检查的开销是一次比较 + 一次通常不跳转的条件跳。在单次访问里不可见，在热循环里就要注意了。

## 裸循环 vs iterator：iterator 才是 SIMD 友好的写法

作者拿"累加数组"做对比：
- `while idx < b { total += a[idx]; idx += 1; }`：编译器把循环**完全展开**成 5 个 `add eax, [rdi + k*4]`，每一步之前都有 `cmp rsi, k; je ...` 形式的边界检查，最后还是要兜到 panic 分支。展开了，但没向量化，也没消掉检查。
- `for var in a.iter() { total += var; }`，`a: &[i32;8]`：直接 `movdqu` + `paddd` + `pshufd` 做 tree reduce，一次就是 128-bit SIMD 加法，四条指令算完 8 个 i32。**完全没有边界检查**，因为 iterator 把访问包在自身内部，长度已经静态可知。
- 同样 iterator 写法，`a: &[i32;5]` 奇数长度：compiler 处理尾部用 `pshufd`/`paddd` 拼 4 个 + 一个标量 `add eax, [rdi]`。仍然没有边界检查。

结论：在 Rust 里，**"idiomatic"（iterator 写法）和"手动循环"编出来的代码有本质差异**。iterator 把"可达索引范围"这件事告诉了类型系统，编译器就敢 vectorize、敢把检查消光。裸 `while + 索引` 看起来更接近 C，但反而让编译器谨慎得多。

这也顺带解释了 Rust 为什么推崇各种链式 `zip / map / filter`：不是为了"好看"，是为了让边界检查可证伪。

## 相关

- [[fearless-simd]] —— Rust 端利用编译器 autovectorize 做 SIMD 的经验
- [[cpp-runtime-reflection]] —— 另一个"零成本抽象是否真的零成本"的案例
- [[compilation-pipeline]] —— 从源码到汇编的通用视角

## Sources

- [[sources/giordi91-rust-disassembly-part-1]]
