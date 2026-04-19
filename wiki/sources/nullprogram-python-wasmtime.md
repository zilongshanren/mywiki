---
tags: [source, computer-systems, wasm, python]
date: 2026-04-19
sources: 1
---

# Extending Python with WebAssembly via wasmtime-py（Chris Wellons / nullprogram）

[[chris-wellons]] 发表于 2026 年 1 月的文章，讨论在 Python 中以 Wasm 取代 C 扩展的动机、陷阱与两个实用案例。

## 摘要

作者主张用 Wasm 来扩展 Python，以替代传统的 C 扩展——Wasm blob 是架构无关的，部署时不需要 C 工具链。比较 pywasm3（源码分发，需工具链）与 [[wasmtime-py]]（附带 x86-64/ARM64 Windows/macOS/Linux 二进制），选择后者。详细讲解几个关键陷阱：`Store` 需反复回传（作者用 `functools.partial` 解决）、struct 只能通过指针拷贝、Wasm 把所有整数当有符号解释导致 **返回的指针在高地址段会是负数并绕过边界检查**，规避方法是 `pointer & 0xffffffff` 掩码。又指出 `data_ptr` 返回非边界检查的 ctypes 指针会直接写入 Python 地址空间。两个案例：把 Python 热点函数改写成 C→Wasm 获得约 10x 加速；用 Wasm 封装 [[monocypher-aead]] 加密库，利用 [[bump-allocator-wasm-guest|guest 端 bump 分配器]] 实现密钥擦除。

## 关键要点

- wasmtime-py 当前 ~18MiB，API 月度变动，但免工具链分发值回票价
- Wasm 签名/无符号指针陷阱：`malloc(...) & 0xffffffff`（JS 里是 `>>> 0`）
- `struct.pack_into` 填补类似 JS `DataView` 的空缺；多值写入用拼接格式串
- 不要把 general-purpose malloc 塞进 Wasm guest——用 bump allocator + 全局 arena
- wasmtime Store 的耦合使得 compile/instantiate 必须同一 Store；解决办法是 `serialize`/`deserialize`
- Monocypher AEAD 示例：`finally` + `bump_reset` 保证密钥不留痕

## 链接到的概念

- [[wasmtime-py]]
- [[wasm-pointer-sign-trap]]
- [[bump-allocator-wasm-guest]]
- [[monocypher-aead]]
- [[linear-allocator]]

## 原文

- 链接：https://nullprogram.com/blog/2026/01/01/
- 本地：`raw/articles/nullprogram.com/2026-01-01_null-program.md`
