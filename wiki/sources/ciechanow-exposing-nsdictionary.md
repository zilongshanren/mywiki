---
tags: [source, objective-c, 数据结构, 哈希表, 逆向工程, ios]
date: 2026-04-14
sources: 1
---

# Exposing NSDictionary（Bartosz Ciechanowski）

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2014 年 4 月发表的逆向工程长文，是 [[sources/ciechanow-exposing-nsmutablearray|Exposing NSMutableArray]] 的姊妹篇——这次目标是 `__NSDictionaryI`，不可变字典的真实实现类。

## 摘要

`__NSDictionaryI` 的 ivar 清单短得惊人：只有 `_used:58` 和 `_szidx:6` 两个位域，**没有任何指向 key/value 存储的指针**。秘密在 Obj-C runtime 的 `object_getIndexedIvars` 机制：`class_createInstance(cls, extraBytes)` 会在对象末尾跟一段变长内存，通过访问器以指针方式暴露。`__NSDictionaryI` 就把 key-value 对直接摊在对象后面（key-object-key-object 交替），所以不仅 cache-friendly，还天然隐藏 ivar（class-dump 看不到）。`objectForKey:` 的汇编反推出的算法是**开放寻址线性探测**：`hash % size` 算初始槽，碰撞就顺序往下，遇到 nil 返回 nil，遇到 pointer 相等直接返回（绕过 `isEqual:`——这是 `NSString` literal、tagged `NSNumber` 的重要优化），否则再走 `isEqual:`。存储大小 `__NSDictionarySizes` 是一张 **64 个素数**表（0, 3, 7, 13, 23, 41, 71, 127…），相邻比值约 **1.637**——和 `NSMutableArray` 的 1.625 如出一辙；容量数组 `__NSDictionaryCapacities` 更小（0, 3, 6, 11, 19, 32, 52, 85），确保平均装载率不超过 **62%**，压制碰撞链长。文章末尾给出了两个陷阱：① 自定义 key 类若让 `isEqual: nil` 可能返回 YES，`objectForKey:nil` 就会错误命中（因为 `[nil hash] == 0`，查完第 0 槽接着线性探测）；② 若自定义 `hash` 的输出恰好**模 size 同余**，所有 key 会退化成 O(n) 链。两篇姊妹文的联合教训：Foundation 集合类的性能保证依赖你的 `hash/isEqual:` 写对。

## 关键要点

- **零显式指针存储**：`__NSDictionaryI` 用 `object_getIndexedIvars` 把 key/value 紧随对象尾部分配，一次 malloc、一段连续内存，极度 cache friendly。
- **key-object 交替布局**：`storage[2i]` 是 key，`storage[2i+1]` 是 value；作者猜测原始实现用 `struct { id key; id object; }` 数组。
- **线性探测开放寻址**：`hash % size` → 命中 nil 返 nil → 命中相同指针立即返回（省掉 `isEqual:`）→ 否则走 `isEqual:` → 否则 `(i+1) mod size`。
- **size 表是质数序列**：0, 3, 7, 13, 23, 41, 71, 127 … 相邻比 ≈1.637；`capacities` 更小，装载率上限 62%。
- **`objectForKey:nil` 陷阱**：`[nil hash]` 返回 0，接着用 nil 调 `isEqual:` 比较第 0 槽起的 key——你的自定义 `isEqual:` 必须 nil-safe。
- **tagged pointer 友好**：64-bit 上 `NSNumber`/`NSDate`/`NSIndexPath` 共享指针，命中时直接指针比较绕过 `isEqual:`。
- **逆向方法复盘**：`kCFAbsoluteTimeIntervalSince1904` 恰好排在 `__NSDictionarySizes` 前一个 qword，可以 `+8` 字节硬访问这张内部表——脏但有效。

## 链接到的概念

- [[nsdictionary-linear-probing]]
- [[objc-runtime-internals]]
- [[nsmutablearray-circular-buffer]]
- [[cache-friendliness]]
- [[non-cryptographic-hash]]
- [[bartosz-ciechanowski]]

## 原文

- 链接：https://ciechanow.ski/exposing-nsdictionary/
- 本地：`raw/articles/ciechanow.ski/2014-04-08_exposing-nsdictionary-bartosz-ciechanowski.md`
