---
tags: [编程语言, sicp, 算法]
date: 2026-04-05
sources: 1
---

# 增长阶（Order of Growth）

**算法行为的粗描述**——输入规模变化时资源消耗如何变化。

## SICP 的定位

> "Orders of growth provide only a crude description of the behavior of a process."

**关键词：粗描述（crude）**。Θ 记法只告诉你趋势，不告诉你实际性能。

## 常见增长阶

| 增长阶 | 问题翻倍时 | 例子 |
|---|---|---|
| Θ(1) | 不变 | 哈希表查找 |
| Θ(log n) | +常数 | 二分、快速幂 |
| Θ(n) | 翻倍 | 线性扫描 |
| Θ(n log n) | 略多于 2× | 归并排序 |
| Θ(n²) | 4× | 冒泡 |
| Θ(2ⁿ) | 平方 | 朴素 Fibonacci |

## 常见错误

1. **忽略常数系数**：O(log n) 不总是比 O(n) 快——当 n 很小或常数很大时。
2. **不考虑缓存行为**：列表遍历在 cache 友好的数据布局下可能吊打哈希表（O(n) 胜 O(1)）。
3. **优化错位**：profile 不确认就盲目替换算法——用 profiler 找真正热点。

## 与 [[aos-vs-soa]] 的联系

ECS 的缓存友好性用增长阶完全表达不出来——但这恰恰是 SoA 性能优势的真正来源。**增长阶 + 常数 + 缓存**共同决定实际性能。

## 相关

- [[fast-exponentiation]]
- [[cache-friendliness]]
- [[recursive-vs-iterative-process]]

## Sources

- [[sources/sicp-day04]]
