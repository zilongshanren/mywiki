---
tags: [source, sicp, 算法]
date: 2026-04-05
sources: 1
---

# SICP Day 5 —— 素数判定与概率算法

SICP 学习推送第 5 天。

## 摘要

从朴素素数判定 Θ(√n) 到 **Fermat 素性测试** Θ(log n) 的概率算法转向。介绍 Carmichael 数（Fermat 测试的骗子）、Miller-Rabin 改进算法。讨论概率算法作为工程选择的正当性。

## 关键要点

- **Fermat 测试**：基于费马小定理，Θ(log n)，大概率正确。
- **Carmichael 数**：极罕见但存在的反例。
- **Miller-Rabin**：k 次测试失败率 < (1/4)^k；10 次 < 10^-6。
- **品味**：当精确解成本使其不可行时，概率算法不是妥协而是唯一合理的工程选择。
- 游戏类比：
  - 物理碰撞的 Broad Phase + Narrow Phase
  - 蒙特卡洛全局光照
  - AI 决策概率

## 链接到的概念

- [[probabilistic-algorithms]]
- [[fast-exponentiation]]

## 原文

- 链接到：[[raw/articles/sicp/day05]]
