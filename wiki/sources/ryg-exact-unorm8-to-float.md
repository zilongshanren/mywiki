---
tags: [source, 渲染, GPU, 数值精度]
date: 2026-04-14
sources: 1
---

# Exact UNORM8 to float（Fabian Giesen）

[[fabian-giesen|Fabian "ryg" Giesen]] 2024 年 11 月发表的短文，讨论一个被 D3D 规范明确「让步」掉的小问题：把 8-bit UNORM 整数 `x` 转成 float32 时，**怎样既不用真正的除法器、也不用 double，还能严格满足 round-to-nearest**。

## 摘要

数学定义是 `x / 255.f`，但 D3D11 功能规范明确写「要求 1/2 ULP 的精确转换被认为代价过高」。常见做法 `x * (1.f/255.f)` 因为 `1/255` 不是机器数，会在少数 `x` 上差 1 ULP——对图形通常无所谓，但作为**正确性问题**值得有干净解法。文章给了三条路线：
1. **double 中转**——可证明等价，但很多场合不愿引入 double。
2. **几何级数展开** `1/255 = ∑ 2⁻⁸ᵏ`——用 6 项加合并系数压成两次乘加，FMA 时只需 2 次浮点指令。
3. **Alexandre Mutel 的 `(3·x) ÷ (3·255)`**——`1/(255·3)` 在 float32 中恰好够精确，`3·x` 在 [0,255] 上无损可表示，最终只需两次乘法、不需要 FMA。这是目前最短的精确方案。

文章顺带讨论了 SNORM8/SNORM16 上类似的 `1/(31·127)`、`1/(73·32767)` 常数；UNORM16 至今没有同等干净的两乘法构造。

## 关键要点

- **「不能用真除法」≠「无法精确」**：在 IEEE 754 round-to-nearest 下可以严格用乘加构造正确舍入。
- **常数选择是数论问题**：找到「乘上 `x` 后是机器数 + 倒数也是机器数」的 `k` 是关键。
- **几何级数视角**：因为 `1/255 = 1/(2⁸ − 1) = ∑_{k≥1} 2⁻⁸ᵏ`，每项都是 2 的幂，自然落在 IEEE 754 的尾数槽里。
- 实践提醒：`(value + value + value) * (1.f / (3.f * 255.f))` 这种「先 ×3 再倒数」的微优化在产品代码里实测能比 `(float)x * (1.f/255.f)` 快约 10%。

## 链接到的概念

- [[unorm-float-conversion]]
- [[fabian-giesen]]
- [[color-space]]

## 原文

- 链接：https://fgiesen.wordpress.com/2024/11/06/exact-unorm8-to-float/
- 本地：`raw/articles/fgiesen.wordpress.com/2024-11-06_exact-unorm8-to-float.md`
