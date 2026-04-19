---
tags: [source, bit-twiddling, bc7, oodle]
date: 2026-04-14
sources: 1
---

# Inserting a 0 bit in the middle of a value（fgiesen / Fabian Giesen）

[[fabian-giesen]] 在 Oodle Texture BC7 解码器里需要把 anchor pixel 被省略掉的 0 bit 重新插回去，顺手写下了这则 bit-twiddling 小品：从 5 条语句的朴素写法到 `value + (value & top_mask)` 的一行版本，再延伸到「移除已知为 0 的 bit」的对偶形式。

## 摘要

朴素做法把值拆成上下两段、高段左移 1 位再 or 回去，一共 5 条 C 语句，功能完全正确、也根本不是热点；但 ryg 觉得为一件"听起来很简单"的事花 5 条语句别扭。观察点有二：一是"最高若干位"的 mask 可以直接用 `~0 << pos` 写成一条常量左移，比 `(1 << pos) - 1` 省一条；二是"值加到自己身上就是左移 1 位"，把高位段挑出来再和原值相加，相当于把高位段 ×2、低位段原样保留——正好实现"在 pos 插入 0 bit"。对偶的"移除已知为 0 的 bit"则是同样逻辑的除法版本，并且 mask 可以从 pos 而非 pos+1 开始——因为被删的那一位本身就是 0，纳入 mask 等同无效。整篇是一次"用算术替代 mask 拼接"的思维体操。

## 关键要点

- 需要"高 N 位 mask"时，`~0 << N` 比 `(1 << N) - 1` 更便宜
- `x + (x & mask)` 相当于把被 mask 命中的位左移 1 位
- 一条算术指令就能完成"插入 0 bit"
- 对偶的"删 0 bit"用减法版本，前提是该位确实为 0
- 价值不在加速（BC7 anchor 只有 1–3 个），而在训练 bit 层面的代换直觉

## 链接到的概念

- [[insert-zero-bit-in-middle]]
- [[sign-extend-without-shift]]

## 原文

- 链接：<https://fgiesen.wordpress.com/2024/10/24/inserting-a-0-bit-in-the-middle-of-a-value/>
- 本地：`raw/articles/fgiesen.wordpress.com/2024-10-24_inserting-a-0-bit-in-the-middle-of-a-value.md`
