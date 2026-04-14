---
tags: [source, objective-c, 数据结构, 逆向工程, ios]
date: 2026-04-14
sources: 1
---

# Exposing NSMutableArray（Bartosz Ciechanowski）

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2014 年 3 月发表的硬核逆向工程长文——用 `class-dump` + Hopper + 手写 ARM64 分析把 Apple 闭源的 `__NSArrayM` 实现从汇编里抠出来。这是他早期「低层系统挖坟」风格的代表作之一。

## 摘要

出发点是一个日常问题：`NSMutableArray` 内部到底长什么样？作者先用 LLDB 发现真实子类是 `__NSArrayM`，再用 `class-dump` 拿到 ivar 布局（`_used / _size / _offset / _list / _mutations`），然后逐条翻译 `objectAtIndex:` 的 ARM64 汇编——顺带科普了 ARM64 的 PC 相对寻址、modern Obj-C runtime 为何要**通过全局 ivar 偏移变量**间接寻址来解决 fragile base class 问题、以及 `csel` 条件选择指令如何用无分支代码实现 modulo。汇编反推出的 C 等价只有三行：`fetchOffset = _offset + index; realOffset = fetchOffset - (_size > fetchOffset ? 0 : _size); return _list[realOffset]`——这是**循环缓冲区** (circular buffer) 的典型代码。作者再用 runtime 注入一个 `BCExploredMutableArray` 影子类，观察到：两端 insert/remove 真的 O(1)、buffer 按 **1.625×**（不是 2×）增长、**永不收缩**、从中间删除会朝两端中近的那一端移动（最多搬一半元素）、清空后旧指针不抹（所以调试代码必须用 `void**` 绕开 ARC）。最后对比了 `CFArray` 的实现——同样是 deque，但 CF 用两端填零的 padded buffer 而非 circular buffer，两套逻辑各干各的。

## 关键要点

- **`__NSArrayM` = 循环缓冲区 deque**：两端 O(1)，中间插删搬最多一半元素，完美替代「array or linked list?」的二选一。
- **非 2× 扩容**：growth factor 是 **1.625**，理由是 Facebook folly fbvector 同款——2× 下旧内存永远无法被后续分配复用。
- **初始容量参数近乎被忽略**：`initWithCapacity:` 大部分值直接映射到 size=16，Apple 显然不信任调用者给的 hint。
- **永不收缩**：清空一个装过 14336 元素的数组后，buffer 仍保持 14336。
- **modern runtime 的 ivar 间接寻址**：每条 `ldrsw x8, [page, #offset]` 背后是 Apple 解决 fragile base class 的运行时 ivar 修正机制——旧二进制在新 Foundation 下仍能工作。
- **`__NSArrayM` 与 `CFArray` 毫无共享代码**：作者原以为 Foundation 是 CF 的壳，事实相反；两套 deque 实现长期共存。
- **`NSMutableArray` 抽象基类**：子类只需实现 7 个原语方法，其余 21 个组合方法由基类默认转发。

## 链接到的概念

- [[nsmutablearray-circular-buffer]]
- [[objc-runtime-internals]]
- [[cache-friendliness]]
- [[aos-vs-soa]]
- [[bartosz-ciechanowski]]

## 原文

- 链接：https://ciechanow.ski/exposing-nsmutablearray/
- 本地：`raw/articles/ciechanow.ski/2014-03-05_exposing-nsmutablearray-bartosz-ciechanowski.md`
