---
tags: [source, sicp, 算法]
date: 2026-04-05
sources: 1
---

# SICP Day 4 —— 增长的代价

SICP 学习推送第 4 天。

## 摘要

增长阶（Order of Growth）分析工具。引入 Θ 记法表示上下界兼有的粗描述。**快速幂 O(log n)** 的分治思想；**欧几里得算法** 与 Lamé 定理。警告常见错误：忽略常数系数、不考虑缓存行为、优化错位。

## 关键要点

- Θ 记法只提供对过程行为的**粗描述**。
- 快速幂：每多一次乘法，可计算的指数大约翻倍。
- **Lamé 定理**：GCD 步数与斐波那契的联系，最坏 O(log n)。
- **品味**：
  - 错误一：忽略常数系数（O(log n) 不总快于 O(n)）。
  - 错误二：不考虑缓存行为——ECS 的缓存友好性重要。
  - 错误三：优化错误的地方，用 profiler 确认热点。
- 游戏开发应用：矩阵快速幂（骨骼动画程序化计算）、模幂（密码学/PRNG）。

## 链接到的概念

- [[order-of-growth]]
- [[fast-exponentiation]]
- [[cache-friendliness]]

## 原文

- 链接到：[[raw/articles/sicp/day4]]
