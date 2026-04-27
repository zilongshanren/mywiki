---
tags: [source, programming-languages, prng, determinism]
date: 2026-04-19
sources: 1
---

# Mulberry32: A Tiny, Fast, Deterministic RNG（Nikos Papadopoulos / 4rknova.com）

[[nikos-papadopoulos]] 发表于 2026 年 3 月的文章，用几十行 JavaScript 把一个可嵌入任何项目的 32-bit 确定性 PRNG 拆解到每个 bit 操作的原理。

## 摘要

文章从「为什么 `Math.random()` 不够用」切入：它不能 seed、实现不由语言规范规定，一旦需要可复现的随机性，必须自带 PRNG。作者给出 Mulberry32 的完整实现——一个 Weyl 序列驱动的 uint32 状态 + 两轮 xor-shift-multiply 输出 mixer，解释 `>>> 0` 强制 uint32、`Math.imul` 保证 32-bit wrap、`| 1` 保证奇数乘子等每个细节的作用。随后扩展出实用 wrapper（`float / int / range / bool / pick / shuffle / getState`），示范两个同 seed 实例字节对齐，用 FNV-1a 把字符串 seed 折成 uint32，并明确 Mulberry32 的适用范围：游戏程序化生成、测试 fixture、轻量 Monte Carlo；**不适用**：密码学、合规赌博、高统计严谨度的仿真。

## 关键要点

- Mulberry32 = Weyl 序列 state step（`t += 0x6D2B79F5`）+ 两轮 xor-shift + `Math.imul` 输出 mixer
- `Math.imul` 是 PRNG 在 JS 里的关键——普通 `*` 用 64-bit float 会丢掉 32-bit overflow 语义
- `t | 1`、`x | 61` 强制奇数乘子，奇数在模 2³² 乘法里保持位信息
- `x ^ (x >>> k)` 是典型 avalanche pattern，PRNG 和非加密 hash 的通用零件
- 用 FNV-1a 把用户输入的字符串 seed 折成 uint32
- 调用顺序就是 API——混用 `Math.random()` 或代码路径改变调用次数，都会破坏确定性
- 明确 **不适用密码学**：状态空间只有 2³²，可穷举

## 链接到的概念

- [[mulberry32-rng]]
- [[non-cryptographic-hash]]
- [[inversion-sampling-prng]]
- [[pcg3d-hash]]

## 原文

- 链接：https://www.4rknova.com/blog/2026/03/01/mulberry32-rng
- 本地：`raw/articles/4rknova.com/2026-03-01_mulberry32-a-tiny-fast-deterministic-rng.md`
