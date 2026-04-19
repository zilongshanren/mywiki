---
tags: [cryptography, wasm, c]
date: 2026-04-19
sources: 1
---

# Monocypher AEAD（via Wasm）

Monocypher 是 Loup Vaillant 的精简密码学库，单文件、无 libc/无运行时，非常适合编译到 Wasm。[[chris-wellons]] 在其 Python + Wasm 博文里以 AEAD 接口为例演示了如何把它当作一个从 Python 访问的“嵌入能力”。

AEAD 接口设计：

```c
void crypto_aead_lock(uint8_t *cipher_text, uint8_t mac[16],
                      const uint8_t key[32], const uint8_t nonce[24],
                      const uint8_t *ad, size_t ad_size,
                      const uint8_t *plain_text, size_t text_size);
int  crypto_aead_unlock(uint8_t *plain_text, const uint8_t mac[16],
                        const uint8_t key[32], const uint8_t nonce[24],
                        const uint8_t *ad, size_t ad_size,
                        const uint8_t *cipher_text, size_t text_size);
```

“锁”和“解锁”的对称设计：额外的 `ad`（associated data）是明文但会被认证。`mac` 承担完整性，任何一方被篡改都会 unlock 失败。

编译到 Wasm 的关键点：

```
clang --target=wasm32 -nostdlib -O2 -Wl,--no-entry -Wl,--export-all \
      -o monocypher.wasm monocypher.c
```

- `-nostdlib` 没有 libc 也没关系——Monocypher 自给
- `--export-all` 暴露所有外部链接符号作为 Wasm 接口
- 还要额外提供一个 [[bump-allocator-wasm-guest|bump allocator]] 供 host 申请临时缓冲

Python 侧用 `try/finally + bump_reset` 保证每次调用结束后 Wasm 线性内存里的 key/nonce/明文被擦除——这是传统 C 代码里不容易做到的事。CSPRNG 用 Python 自带的 `secrets.SystemRandom`。

## 相关

- [[bump-allocator-wasm-guest]]
- [[wasmtime-py]]

## Sources

- [[sources/nullprogram-python-wasmtime]]
