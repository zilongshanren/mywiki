---
tags: [wasm, security, c]
date: 2026-04-19
sources: 1
---

# Wasm 指针有符号陷阱

Wasm 的接口里不区分指针和整数，所有整数一律当作有符号解释。于是当 guest 端的 `malloc` 等函数返回一个 32 位地址，而它的最高位恰好是 1（发生在内存使用超过 2GiB 空间下半部分，或 linear memory 大到足以把分配器推进“高位”时），host 端拿到的是一个 **负数指针**。

后果：

- `ctypes`/buffer 的边界检查只拦截 `> len`，不拦截负数——因为负数在通常 Python API 里表示“从末尾倒数”，**绕过检查默默写到错误地址**
- wasmtime-py 的 `write/read` 方法采用 Python 负索引惯例，触发的是一次静默的 memory corruption
- `data_ptr` 返回的原始 ctypes 指针甚至能越过 Wasm 线性内存，写进 Python 进程的内存空间（buffer overflow）

修法极简，从 Wasm 出来的每个指针都要 **截断成无符号**：

```python
pointer = malloc(...) & 0xffffffff     # wasm32
```

JavaScript 里对应写法：

```js
let pointer = malloc(...) >>> 0
```

64 位 Wasm 要用 64 位掩码，但实际上不会出现合法的负指针。Wasm 运行时无法代劳——它本身也不知道哪个 i32 是指针。[[chris-wellons]] 指出这大概是 Wasm 设计层面的一个根本缺陷，知道之后就会在各种项目里发现同样的 bug。

## 相关

- [[wasmtime-py]]
- [[avoid-unsigned-types]] — 作者的一般 C 风格建议相反，但 Wasm 接口是例外
- [[bump-allocator-wasm-guest]]

## Sources

- [[sources/nullprogram-python-wasmtime]]
