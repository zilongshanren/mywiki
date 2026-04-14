---
tags: [source, 计算机系统, 编译器, bug, C++, MSVC]
date: 2026-04-14
sources: 1
---

# A Compiler Bug（Max Slater）

[[max-slater|Max Slater]] 2021 年 12 月发表，记录他在写 path tracer **Dawn** 时遇到的一个 MSVC 2019 代码生成 bug——被确认为「interference analysis」问题，一年后在 cl 19.25 修复。文章把整个调试过程剥到汇编级别，是「只有 -O2 才出现的 bug 不一定是 UB」的一个经典反例。

## 摘要

Slater 在 Dawn 里实现一个包含 4 KB 随机数组的 Perlin noise 类，发现 path tracer 输出是乱的——**只在优化开启时**。一般 -O2 独有的 bug 是 UB 的症状，但他这次代码没有 UB。按经典方法逐步删简到能复现的最小代码：一个 `container{ uint8_t type = 1; data n; }`（`data` 含 4095 字节数组），经过 `container::make()` + 拷贝构造 + `func()` 调用，在 `-O2` 下 `ret.type` 在 `ret.n = data{};` 赋值后被清零。

用 **compiler explorer** 跨版本对比汇编，发现 19.24 → 19.25 的唯一差别是：**修复版本多分配 4 KB 栈空间**。坏版本把临时 `data{}`（记为 $T1$）和 `ret`（记为 $T2$）分配到了同一栈区间 `[32, 4128)`——**两者生命期重叠、且 memcpy 源目标还存在部分重叠（UB）**。修复版本把 $T2$ 挪到 `[4128, 8224)`，$T3$ 再往后。

文章推测根因：**RVO / copy elision + inlining 让编译器误判两个临时量的 live 区间不重叠**，进而合并栈槽。真正的原因官方说是 interference analysis 错误，但也只能靠猜——**发现 bug 的人看到什么、怎么走到修复差的**，是这篇文章真正的价值。

## 关键要点

- **只在 -O2 下出现的 bug 不一定是 UB**：这一次，用户代码 valid，是 MSVC 的 interference analysis 错了。
- **Minimal reproducer is king**：Slater 反复删简到 20 行代码触发 bug，外加四个「能让 bug 消失的改动」做特征列表——这种列表是 bug 报告的高价值素材。
- **Compiler Explorer / godbolt bisect**：用网页工具跨版本对比汇编输出是「看见」编译器内部状态的主要手段。
- **栈临时量有 live 区间分析**：它们不是简单按源代码顺序分配，而是和寄存器分配类似做图着色。错误的 live 分析会让两个活着的变量共享同一位置。
- **memcpy 的 UB 不能只看源码里的对象**：编译器有责任保证 memcpy 的源目标不重叠，否则就是 codegen bug。
- **RVO + inlining 让栈所有权变得模糊**：这是根因最可能的地方——Slater 自己也承认「我们可能永远不知道真正原因」。
- **数组大小的 sensitivity**（4095 对 4094）暗示是 page-size / chkstk 路径相关的 heuristic。

## 链接到的概念

- [[compiler-interference-analysis-bug]]
- [[compilation-pipeline]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Compiler-Bug/
- 最小 repro：https://godbolt.org/z/5a9v99988
- 本地：`raw/articles/thenumb.at/2021-12-26_a-compiler-bug.md`
