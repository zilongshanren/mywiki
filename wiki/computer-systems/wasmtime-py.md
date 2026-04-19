---
tags: [wasm, python, tooling]
date: 2026-04-19
sources: 1
---

# wasmtime-py

wasmtime-py 是 bytecodealliance 提供的 wasmtime Python 绑定。相比另一个选项 pywasm3（纯 C、仅源码分发，部署需要 C 工具链），wasmtime-py **附带 Windows/macOS/Linux × x86-64/ARM64 的二进制**，因此可以直接作为 Python 库分发一个 Wasm blob 而不要求宿主机有 C 工具链。速度是 wasm3 的 3–10 倍。

[[chris-wellons]] 在 2026 年 1 月的博文（基于版本 40）中总结的使用要点：

- **Store 的设计很啰嗦**：所有对象都要再把 `store` 回传——作者用 `functools.partial` 把它绑定掉
- **get_buffer_ptr 是 buffer protocol 对象**，移动 bytes 首选 `memory.read/write`；内存 grow 后要重新拿 buffer
- **multi-value 尚处实验阶段**，复杂参数只能用指针 + 拷贝
- **[[wasm-pointer-sign-trap|指针必须掩码]]**：`malloc(...) & 0xffffffff`
- **Store 耦合 compile/instantiate**：一度以为是 fatal flaw，更新补充可以用 `serialize/deserialize` 分离
- 包大小 ~18MiB 且 API 月度 breaking，要为升级留心

典型搭配：host 一侧用 Python 做业务，guest 一侧 C 代码 + 全局 [[bump-allocator-wasm-guest|bump allocator]]，每次调用前 alloc、之后 reset。

## 相关

- [[wasm-pointer-sign-trap]]
- [[bump-allocator-wasm-guest]]
- [[monocypher-aead]]

## Sources

- [[sources/nullprogram-python-wasmtime]]
