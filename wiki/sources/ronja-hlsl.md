---
tags: [source, rendering, shader, hlsl, 入门]
date: 2026-04-14
sources: 1
---

# HLSL（Ronja's Shader Tutorials 002）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 3 月发表的系列第二篇，速通 Unity shader 里用到的 **HLSL / CG 语法子集**：标量/向量/矩阵类型、swizzle、struct、函数、控制流。目标读者是已经会一门 C-like 语言的开发者。

## 摘要

Ronja 先澄清术语：Unity shader 官方标记是 CG（C for Graphics，2012 年已废弃），但语法几乎就是 HLSL，大家都统一叫 HLSL 更好搜。然后列出常用标量类型 `fixed / half / float / int / uint`，并指出移动端 GPU 下 `fixed`（[-2,2], 1/256 精度）、`half`（16 位浮点）、`float`（32 位）之间的真实精度差异——这在桌面 GPU 上被全部抹平为 32 位，所以桌面调试时优化空间被隐藏了。接着讲向量类型（`float2/3/4`），并系统介绍 [[shader-vector-math-primer|swizzle]] 语法：`vec.xy`、`vec.zyx`、`vec.xxxx`，以及 `.x/y/z/w` 与 `.r/g/b/a` 的别名。矩阵部分一句话带过（`float4x4`、`mul` 做向量变换）。最后讲自定义 struct、函数声明（没有类、全局作用域）、和控制流——她特意**反驳了"shader 不能用 if"的教条**：step 函数内部也有分支，写可读的 if 比强行用 step 堆乘法更好。

## 关键要点

- Unity CG ≈ HLSL，术语上统一叫 HLSL 更容易查资料。
- 移动端 `fixed/half/float` 有真实精度差；桌面端全是 32 位，优化空间隐藏。
- swizzle 是 shader 最强语法糖：`.xxxx` 广播、`.zyx` 反序、`.xy` 截断。
- HLSL 数据类型全是值类型，struct 不需要 `new`。
- 反教条：`if` 不是绝对禁区——`step` 内部也是分支，可读性优先。
- 向量变换统一通过 `mul(M, v)` 做，不是 `*` 操作符。

## 链接到的概念

- [[shaderlab-hlsl-basics]]
- [[shader-vector-math-primer]]
- [[fragment-shader]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/002-hlsl/>
- 本地：`raw/articles/ronja-tutorials.com/2018-03-21_hlsl.md`
