---
tags: [source, bitsquid, hash, murmurhash]
date: 2026-04-19
sources: 1
---

# Code Snippet: Murmur hash inverse / pre-image（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2011 年 8 月的博文，直接给出 MurmurHash2 32 位与 64 位版本的 `murmur_hash_inverse()` C 代码。

## 摘要

MurmurHash2 在输入长度 ≤ bucket（32 位版 4 字节，64 位版 8 字节）且 seed 已知时是一一映射。Frykholm 给出完整实现：通过计算 `m` 在 mod 2^32（或 mod 2^64）下的乘法逆元 `minv`，并把 `h ^= h >> s` 这种异或移位也逆出来（`invert_shift_xor` 按字节高到低反推），就能从 hash 反算出原始 4/8 字节输入。典型用途是**在 watch window 或日志里把引擎内部的 4 字符资源 tag / 类型 ID 的 hash 反查回人类可读的字符串**。

## 关键要点

- `m = 0x5bd1e995` 的乘法逆元 `minv = 0xe59b19bd`（32 位），通过扩展欧几里得算。
- `invert_shift_xor(hs, s)` 处理 `8 <= s <= 16`，按字节从高字节开始重构。
- 64 位版常数 `m = 0xc6a4a7935bd1e995ULL`，`minv = 0x5f7a0ea7e59b19bdULL`，shift 47。
- 只对 ≤ bucket 长度的 pre-image 唯一；更长输入空间远大于 2^32，必须字典反查。
- 有人把这份 C 代码移植成 Lua 在 Steam Workshop 发布（评论链接）。

## 链接到的概念

- [[murmur-hash-inverse]]
- [[non-cryptographic-hash]]
- [[bitsquid-static-hash-values]]
- [[static-hash-value-debug-assert]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/08/code-snippet-murmur-hash-inverse-pre.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-08-25_code-snippet-murmur-hash-inverse-pre-image.md`
