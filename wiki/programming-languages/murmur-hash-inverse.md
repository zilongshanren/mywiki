---
tags: [hash, murmurhash, reverse-engineering, bitwise]
date: 2026-04-19
sources: 1
---

# MurmurHash2 的逆运算：从 hash 恢复 pre-image

MurmurHash2 的 32 位版本看起来是单向的，但只要输入长度 `<= 4 字节` 且 seed 已知，哈希函数其实是一一映射——因为 `*m` 在 mod 2^32 下可逆（存在乘法逆元 `minv = 0xe59b19bd`），而 `h ^= h >> s`（`8 <= s <= 16`）也是可逆的。[[niklas-frykholm]] 给了一份可直接嵌引擎的 C 代码。

## 核心原理

MurmurHash2 的末尾 finalization 是：

```
h ^= h >> 13;
h *= m;
h ^= h >> 15;
```

逆过程按反向序依次撤销：

1. 逆 `h ^= h >> 15`——因为右移 15 位后只影响低 17 位，高 15 位不变，可按字节从高往低反推；这就是 `invert_shift_xor(h, s)`。
2. 逆 `h *= m`——用 `h *= minv`，其中 `minv = 0xe59b19bd` 满足 `m * minv ≡ 1 (mod 2^32)`，通过扩展欧几里得算出。
3. 逆 `h ^= h >> 13`——再次 `invert_shift_xor`。

然后把 seed 的初始混合 `seed ^ 4` 也 `*m` 拿出来 XOR 掉，得到当时的 `k = *(unsigned*)data * m ^ (k>>24) ^ …`。再对 `k` 做对应逆操作就还原出 4 字节的原始输入。

64 位版本同理，只是常数 `m = 0xc6a4a7935bd1e995ULL`，`minv = 0x5f7a0ea7e59b19bdULL`，shift 是 47。

## 用途

一句话：**用来在运行期反查 static string hash**。引擎里把字符串替换成 32 位 hash（参考 [[bitsquid-static-hash-values]]、[[string-handling-game-runtime]]）能省内存省比较开销，但调试时只能看到 hex。做一个 inverse 函数，对 ≤4 字符的资源类型（`"tex"`、`"mat"`、`"lua"`）直接反解 pre-image，就能在 watch window 里打印人类可读的 tag。

对超过 4 字节的字符串这招没用——pre-image 空间远大于 32 位 hash，必须暴力字典反查。但工程上大量引擎内部类型 tag 本来就是 2–4 字符，所以这招覆盖率很高。

## 相关

- [[non-cryptographic-hash]]
- [[static-hash-value-debug-assert]]
- [[bitsquid-static-hash-values]]
- [[string-handling-game-runtime]]

## Sources

- [[sources/bitsquid-murmur-hash-inverse]]
