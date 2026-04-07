---
tags: [算法, sicp]
date: 2026-04-05
sources: 1
---

# 概率算法（Probabilistic Algorithms）

**用概率正确性换取可行性**——当精确解太贵时的合理工程选择。

## SICP 的哲学立场

> "The Fermat test differs in character from most familiar algorithms, in which one computes an answer that is guaranteed to be correct. Here, the answer obtained is only probably correct."

概率算法不是妥协——**当精确解的计算成本使其不可行时，概率算法是唯一合理的工程选择**。

## Fermat 素性测试

基于费马小定理：若 n 是素数，对任何 a，`a^n ≡ a (mod n)`。

- 单次 Fermat 测试：合数时失败率 < 1/4。
- k 次独立测试：失败率 < (1/4)^k。
- 10 次：错误概率 < 10^-6。

**Carmichael 数**是反例（稀有但存在），**Miller-Rabin** 算法改进处理。

## 游戏开发中的概率算法

- **碰撞检测 Broad Phase + Narrow Phase**：粗检（AABB）降成本，精检（GJK）保精度。
- **蒙特卡洛全局光照**：随机采样路径，样本越多越精确。
- **AI 决策概率化**：70% 追击、30% 巡逻，打破机械感。
- **PRNG**：伪随机数生成是概率思维在代码里的常态化。

## 与密码学

现代密码学大量用概率算法：
- **素数生成**：Miller-Rabin 判断大素数候选。
- **哈希**：概率碰撞性是可接受的 trade-off。
- **RSA**：依赖高概率素数判定。

## 相关

- [[fast-exponentiation]]
- [[order-of-growth]]

## Sources

- [[sources/sicp-day05]]
