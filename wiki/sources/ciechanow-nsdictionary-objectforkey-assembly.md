---
tags: [source, objective-c, arm64, 逆向工程, 汇编]
date: 2026-04-14
sources: 1
---

# __NSDictionaryI objectForKey: 汇编分析（Bartosz Ciechanowski）

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 为主文 [[sources/ciechanow-exposing-nsdictionary|Exposing NSDictionary]] 准备的**汇编附录页**。整篇只做一件事：把 iOS 7.1 SDK 里 `__NSDictionaryI objectForKey:` 的 ARM64 反汇编（约 60 条指令）逐句翻译成 C 伪代码。

## 摘要

主文里给出的那段开放寻址线性探测 C 代码，实际上是这个页面一条条 `cmp/ccmp/csel/b.eq/msub/orr` 指令反推出来的。附录里可以学到几项 ARM64 特有的低层技巧：① **callee-saved 寄存器保存**——`x19-x24` 在函数序言里通过 `stp ... [sp, #0xfffffff0]!` 一次压两个；② **`ccmp` 条件比较**指令可以一条指令表达「如果上一个比较失败，就再比另一对值」，被用来实现 `if (fetchedKey == nil || fetchedKey == queryKey)` 的无分支融合版；③ **`udiv` + `msub` 组合**实现整数取模：先 `q = x8 / x22`，再 `x24 = x8 - q * x22`——这就是 `hash % size`；④ **lazy binding**：调用 `imp___stubs__object_getIndexedIvars` 而非 `object_getIndexedIvars` 本体，首次调用时才解析真正的函数地址；⑤ **位运算的小聪明**：`lsl x8, x24, #1` + `orr x8, x8, #1` 等价于 `2*index + 1`，用来从 key-object 交替数组里取 value 槽。作为主文的补充，这一页对想认真读一段非平凡 ARM64 的人是极好的练习材料——它让人看到**编译器为紧凑哈希查找写出的代码密度有多高**。

## 关键要点

- 纯汇编附录页，不独立引入新概念，读法是**与主文对照**。
- **`ccmp` 条件比较**：`cmp x0, #0x0; ccmp x0, x19, #0x4, ne; b.eq` = `if (x0 == 0 || x0 == x19)`——无分支融合。
- **`udiv/msub` 求模**：ARM64 没有硬件 `%` 指令，靠两条指令合成。
- **ARM64 函数序言**：callee-saved `x19-x24` 用 `stp` 成对压栈，`sp` 预减。
- **lazy binding**：`imp___stubs__*` 是 dyld 的短桩，首次命中触发符号解析。
- **主文引用**：与 [[sources/ciechanow-exposing-nsdictionary]] 配对阅读，对应 [[nsdictionary-linear-probing]] 概念页的算法段落。

## 链接到的概念

- [[nsdictionary-linear-probing]]
- [[calling-conventions-x86]]
- [[objc-runtime-internals]]
- [[bartosz-ciechanowski]]

## 原文

- 链接：https://ciechanow.ski/extra/objectforkeyassembly/
- 本地：`raw/articles/ciechanow.ski/2014-04-08_nsdictionaryi-objectforkey-bartosz-ciechanowski.md`
