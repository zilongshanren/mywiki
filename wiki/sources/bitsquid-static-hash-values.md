---
tags: [source, bitsquid, 哈希, 编译期, cpp]
date: 2026-04-19
sources: 1
---

# Static Hash Values（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 10 月的文章，讨论运行时如何与编译期预先算好的字符串哈希值比较——他给出的选择是 `static_hash("str", 0x...)` + debug assert。

## 摘要

Bitsquid 内部大量使用 MurmurHash 把字符串键"压成" 32-bit id（事件名、资源名、属性名）。要把代码里出现的比较写成零开销，方案有三：build 前用代码生成工具 patch hash；用预处理器硬算；或者**手写 hash 值 + debug 校验**。预处理器路线（`HASH_STR_10('r','o','o','t','_','p','o','i','n','t')`）能做，但作者觉得 macro 体积太大、不优雅。最终他选的是最平凡的一种：把十六进制 hash 值直接写在代码里，但用一个 wrapper `static_hash("root_point", 0x5e43bd96)`——debug 构建里跑真正的 MurmurHash 和传入值比对并 `assert`；release 里直接宏展开成常量。这么一来常量是源码里看得见的、hash 算法改了 assert 会炸、grep `static_hash(` 还能批量找到所有硬编码。评论区讨论了 template meta-programming、constexpr、preparser 改源码等替代，但在 2010 年编译器不行、constexpr 还没普及时，debug-assert 方案是"简单得恰到好处"。

## 关键要点

- 目标：`if (name() == HASH_OF("root_point"))` 在 release build 里是**零成本常量比较**；
- 朴素 `static unsigned id = hash(...)` 要付第一次 hash 成本 + 之后每次的 init-once 分支；
- **三条路线**：代码生成 / preprocessor / 手写常量；
- 作者选手写 + `static_hash(str, val)` debug 断言 —— 其他团队（Julien, Phil）更倾向 pre-parser（源码里用 `H("str", 0)`，工具把第二参数替换成真值；CI 校验）；
- template meta-programming 能把 MurmurHash 折成 immediate，但（2010 的）编译器 ≤ 23 字符才肯折叠、还不能用在 `switch case`（因为 `"hello"[0]` 不是常量表达式）；
- constexpr 是"未来的解法"——2013 年有人贴出 constexpr 版；
- static initializer 也有人提，作者明确**避免 static init**，不仅是初始化顺序问题，也为了 startup profiling 可控；
- **运行期校验 vs. release 命中**：作者认为 hash mismatch 会在 release 里也炸（行为不一致），所以 debug assert 只是防沾衣；Phil 反对——debug 不保证覆盖，他更信 pre-parser。

## 链接到的概念

- [[static-hash-value-debug-assert]]
- [[non-cryptographic-hash]]
- [[flow-graph-data-oriented-runtime]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/10/static-hash-values.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-10-01_static-hash-values.md`
