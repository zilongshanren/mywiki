---
tags: [cpp, software-design, performance, compiler-optimization]
date: 2026-04-19
sources: 1
---

# Free function vs 成员函数的性能差异（基本没有）

Klaus Iglberger 在 2017 年 CppCon 的 *"Free your Functions!"* 里说过一句 throwaway line：**「写成 free function 可能更有性能优势」**。这句话被一代 C++ 工程师反复引用，却从没有人做过 benchmark。16BPP.net 的作者 2025 年决定把它测一遍，并跟 Klaus 本人邮件确认过才发布。

## 什么是 Free Function

Free function 指**不属于任何 class / struct 的自由函数**。`std::sort`、`std::swap`、C 风格的 `glm::normalize(v)` 都是典型。它的对立面是成员函数（`v.normalize()`）。Free function 的设计优势是：

- 可以跨类型复用（[[higher-order-functions]] / generic programming）；
- 不污染 class 接口；
- 不需要 `friend`；
- 配合 [UFCS](https://en.wikipedia.org/wiki/Uniform_function_call_syntax)（Nim / D / Herb Sutter 的 Cpp2 里已有，C++ 几次提案都未通过）可以兼得两种调用语法。

## 三种写法

作者测的 `Vec4::normalize()` 有三种实现：

1. **成员函数**：`v.normalize()` — 用 `this` 访问数据；
2. **Free function 传 struct**：`normalize(Vec4& v)` — 函数自由，但仍需理解 struct；
3. **Free function 传所有标量**：`normalize(double& a, double& b, double& c, double& d)` — 这才是 Klaus 主张的「properly freed」。

## 小 benchmark：576 组合只有 8 组显著

1000 万个 Vec4 × 100 次迭代 × 3 CPU × 3 OS × 3 编译器 × 多个 `-O` flag × 4 个操作 = **576 组 benchmark 运行**。阈值定义为「必须比另外两种快 10ms 以上」（在 150~300ms 的 run 上相当于 3~6% 的显著差）。

**结果：只有 8 组有显著差异**，约 1.4%。并且集中在同一个子集——**clang / Linux / Intel / `normalize()` / 传标量版**。该子集下约有 15% 的速度提升（185→150ms）。其他 98% 的情况**完全没有差异**。

## 大应用 benchmark：Synfig 跑 78 小时

把小样本结论拉到一个真实的 C++ 图形应用里：选了 [Synfig](https://www.synfig.org/) 矢量动画引擎，用 [Callgrind](https://valgrind.org/docs/manual/cl-manual.html) + [KCachegrind](https://kcachegrind.sourceforge.net/) 在 680 个 `.sif` 测试上采 call graph，定位被调用最频繁的成员函数，选中 `synfig::Color::clamped()` 来「free 化」。

三种 free 化方式：

1. 改成 `friend` 函数；
2. 把数据成员 `public` 后从外部写 free function；
3. **重构函数签名把参数显式传入**——这是「真正的 free 化」。

跑 GCC 14.2 `-O3` / Ubuntu 24.04 / Intel + AMD，每个 `.sif` 10 次，总计 78 小时。结论：

- 基线 vs free 版本的累积耗时差异 **~0.5%**——完全在噪声范围内；
- `friend` 和 `public` 版本反而略慢一丢丢（也在噪声范围）；
- 做 Z-score 离群点剔除后，free 版本一致比 baseline 快 1.5~2.8%；
- 但如果取 best-case runtime，差异又掉回噪声；
- 作者坦承 Synfig 某些 `.sif` 的运行时间本身就非平稳（`164ms ⇄ 114ms` 的双峰分布），导致 Z-score 和 IQR 都无法彻底清洗数据。

**结论是「不拒绝也不接受」**：既没证明 free function 更快，也没证明一样快，但也没证据说它更慢。

## 最终立场

> **「如果你想把函数 free 化是出于架构 / 设计考虑，请去做；不要指望 free 化会带来性能提升，也不要担心它会带来性能下降。」**

顺带证明：`public` 数据成员 vs `private`、`friend` 函数 vs 普通成员，性能上都没有可测量的差别——这一点 C++ 社区常有模糊传言，这个实验也顺手杀掉了这些都市传说。

## 方法论启示

这篇把 [[benchmark-methodology-end-to-end]] 的几条规则都串了一遍：小 bench 里 2% 的亮点在整合测试里消失、Z-score 救不了 non-stationary 数据、原始 benchmark 必须挂出来让别人重跑。作者的更底层的态度是「**8 年前的性能主张今天可能早已不成立——编译器一直在偷偷变强**」。

## 相关

- [[benchmark-methodology-end-to-end]]
- [[psraytracing]]

## Sources

- [[sources/16bpp-free-functions-hypothesis]]
