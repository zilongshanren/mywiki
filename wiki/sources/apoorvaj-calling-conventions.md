---
tags: [source, 计算机系统, x86, abi]
date: 2026-04-14
sources: 1
---

# The experiment —— cdecl / stdcall / fastcall 三路 diff（Apoorva Joshi / apoorvaj.io）

[[apoorva-joshi]] 在 2016 年 9 月写的一篇短文。起因是他在给上一篇博客的 OpenGL loader 加函数指针时漏写了 `WINAPI` 宏，32 位编译挂掉。追下去发现 `WINAPI` 在 32 位 Windows 上展开成 `__stdcall`，于是顺手把 `cdecl` / `stdcall` / `fastcall` 三种调用约定在同一段 C 代码上做了一次汇编 diff。

## 摘要

作者写一段最小 C 程序，调用 `foo(88, 99)`，用 `gcc -S -m32 main.c` 编译三遍，每次把函数属性换成 `cdecl`、`stdcall`、`fastcall`，然后 diff 得到的 `.s` 文件。通过读 `main:` 块里 `%ebp` / `%esp` 栈帧建立、参数压栈、`call foo`、`addl` 栈清理这几步汇编，直观看出三种约定的差别：`cdecl` 参数压栈、**调用者**清理；`stdcall` 参数压栈、**被调用者**用 `ret $N` 清理；`fastcall` 前两个参数走 `%ecx` / `%edx`、其余压栈、被调用者清理。作者提醒：64 位时代调用约定已经大幅收敛，这篇主要是理解 x86 栈帧机制的小练习。

## 关键要点

- `pushl %ebp` + `movl %esp, %ebp` 是 x86 栈帧建立的标准序曲，`%ebp` 在函数内不动、`%esp` 随分配/释放移动。
- `cdecl` 把栈清理交给调用者，是为了支持可变参数函数——`printf` 这种调用点才知道到底压了几个参数。
- `stdcall` 的 `ret $N` 把栈清理编码到被调用者一侧，代码密度更高，是 Win32 API 的默认约定。忘写 `WINAPI` → 32 位编译下栈不平衡。
- `fastcall` 只能把两个整型参数塞进寄存器（`%ecx`、`%edx`），多余的还是 spill 到栈上。
- 文末给出 Agner Fog 的 *calling conventions* PDF 作为进阶阅读。

## 链接到的概念

- [[calling-conventions-x86]]
- [[sse-tricks]]
- [[register-spilling-avoidance]]

## 原文

- 链接：https://apoorvaj.io/exploring-calling-conventions
- 本地：`raw/articles/apoorvaj.io/2016-09-04_the-experiment.md`
