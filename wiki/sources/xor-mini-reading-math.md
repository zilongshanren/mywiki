---
tags: [source, math, notation, shader, reference]
date: 2026-04-19
sources: 1
---

# Reading Math Papers（Xor / GM Shaders Mini）

[[xor-shader-artist|Xor]] 发表于 2025-04-10 的一篇**数学记号扫盲**，面向自学出身、想啃渲染论文（rendering equation、BRDF、SH 等）却被符号劝退的 shader 作者。

## 摘要

Xor 自己也是自学 + 自教出身，文章明确写给「上次数学课是几年前」的读者。内容覆盖：标量/向量/矩阵/张量记法（bold、右箭头、帽子、下标），运算符号（`·` vs `×`、`|x|` vs `‖v‖`、Σ 与 ∏），函数记号（`f(x)`、`f⁻¹`、inline `↦` vs 集合映射 `→`），集合论基础（ℕ/ℤ/ℚ/ℝ/ℂ 与 GLSL 数值类型的对应），以及区间 `[a, b]` / `(a, b)` 的开闭端点—顺带用 `fract(x) ∈ [0, 1)` 给一个程序员能秒懂的例子。布尔运算里顺嘴解释了 XOR 就是他的 ID 来源。文末以 sign 函数的 `ℝ → {-1, 0, +1}` 作为把「集合映射 + arrow notation + if-else」串起来的收尾样例（本地 raw 到此截断，文章在 Substack 是 paywall）。

## 关键要点

- 不是教数学，是一份**查表式**记号字典，配对 GLSL 语义。
- 强调记号不是数学本身——看不懂符号不等于不懂概念。
- 对 shader 作者最常见有用的部分是集合与区间——说明 `fract` 为什么值域是左闭右开。
- 补充了 `uint` 对应 `ℕ₀`、`int` 对应 `ℤ`、`float` 近似 `ℚ` 的映射关系。

## 链接到的概念

- [[reading-math-notation-for-shaders]]
- [[vector-dot-product]]
- [[faster-math-functions]]

## 原文

- 链接：https://mini.gmshaders.com/p/readingmath
- 本地：`raw/articles/mini.gmshaders.com/2025-04-10_reading-math-papers.md`
- 注：Substack 原文为付费续读，本地仅存免费前半。
