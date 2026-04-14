---
tags: [x86, abi, 汇编, 函数调用]
date: 2026-04-14
sources: 1
---

# x86 32 位调用约定：cdecl / stdcall / fastcall

**调用约定（calling convention）**规定了函数调用时**谁负责把参数放到哪里、谁负责清理栈**，以及寄存器在调用前后的保留规则。Windows 32 位世界里常见的三种——`cdecl`、`stdcall`、`fastcall`——来自同一段汇编做三路 diff 就能讲清楚。

## 栈帧基础

任何一个 x86 函数进入时都会做两件事来建立栈帧：

```
pushl %ebp            ; 保存调用者的 base pointer
movl  %esp, %ebp      ; 新的 base pointer = 当前栈顶
```

此后 `%ebp` 在本函数生命周期内不动，用来相对寻址参数和局部变量；`%esp` 随 push/pop 移动。返回时 `popl %ebp` 或 `leave` 恢复调用者栈帧。x86 的栈向低地址增长，`subl $16, %esp` 就是「分配 16 字节局部空间」。

## 三种约定的差异

| 约定 | 参数传递 | 栈清理 |
|---|---|---|
| `cdecl` | 全部压栈 | **调用者**清理（`addl` 抵消 push） |
| `stdcall` | 全部压栈 | **被调用者**清理（`ret $N` 一次带走） |
| `fastcall` | 前两个整数参数走 `%ecx` / `%edx`，其余压栈 | 被调用者清理 |

`cdecl` 把清理交给调用者是为了支持**可变参数函数**——只有调用点才知道真的压了几个参数进去。`stdcall` 少一条 `addl`、代码密度更高，是 Win32 API（`WINAPI` 宏展开为 `__stdcall`）的默认选择；一旦忘写 `WINAPI`，32 位编译就会在栈清理上两边不一致，直接崩。`fastcall` 省掉两次内存 push，但能走寄存器的参数只有 `ecx`/`edx` 两个。

## 为什么现在没那么重要

64 位时代调用约定基本收敛：Windows x64 把前四个整型放 `RCX/RDX/R8/R9`、前四个浮点放 `XMM0~3`；System V AMD64 ABI 把前六个整型放 `RDI/RSI/RDX/RCX/R8/R9`。两种都由**被调用者保留部分寄存器**，清理也不再纠结。32 位那套 zoo 主要留作理解参数压栈、`%ebp`/`%esp` 栈帧机制的教学样本。

## 相关

- [[memory-hierarchy]]
- [[sse-tricks]]
- [[register-spilling-avoidance]]
- [[x64-platform-tidbits]] —— x86-64 上 C 整数提升规则导致地址计算被迫多一条指令；以及 32 位写入隐式清零高 32 位的设计

## Sources

- [[sources/apoorvaj-calling-conventions]]
