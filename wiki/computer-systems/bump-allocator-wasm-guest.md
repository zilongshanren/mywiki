---
tags: [wasm, memory, arena]
date: 2026-04-19
sources: 1
---

# Wasm Guest 端的 Bump 分配器

把 C/C++ 代码编成 Wasm 供 host 调用时，host 需要向 guest 的线性内存申请空间来放入参数。一个自然的想法是让 guest 暴露 `malloc`/`free`，但 [[chris-wellons]] 指出这是过度工程：

- 把一个 general-purpose 分配器塞进 Wasm 只是为了做一次调用的参数生命周期管理，非常浪费
- guest 不会有多线程（host 会串行化 Wasm 实例）
- 绝大多数调用模式就是“拷入一批值、调一次、拷出结果”

最合适的方案是 **guest 里一个全局 [[linear-allocator|bump allocator]]**，覆盖 `__heap_base` 到 linear memory 高端：

```c
extern char __heap_base[];
static char *heap_used;
static char *heap_high;

void *bump_alloc(ptrdiff_t size) { ... }

void bump_reset() {
    ptrdiff_t len = heap_used - __heap_base;
    __builtin_memset(__heap_base, 0, len);  // 顺便擦除敏感数据
    heap_used = __heap_base;
}
```

Host 每次调用 Wasm 之前 rapid-fire 一串 alloc 把参数放好，调用结束 `bump_reset`，本质上是一个跨 host/guest 的“栈”。对于 [[monocypher-aead]] 这样的加密库还有额外好处：`bump_reset` 里的 `memset` 是对 Wasm linear memory 的外部可见写，不会被编译器当作死 store 消除——这是一般在 [[sources/nullprogram-python-wasmtime|Monocypher 例子]]里普通 C 程序里很难可靠做到的。

`__heap_base` 是 Clang Wasm target 的 ABI 约定符号，表示数据段末尾、可用堆起点。

## 相关

- [[linear-allocator]]
- [[wasmtime-py]]
- [[monocypher-aead]]

## Sources

- [[sources/nullprogram-python-wasmtime]]
