---
tags: [objective-c, 数据结构, circular-buffer, deque, ios, 逆向工程]
date: 2026-04-14
sources: 1
---

# `__NSArrayM` 的循环缓冲区实现

`NSMutableArray` 是 Foundation 里最常见的可变容器。很多 Obj-C 程序员以为它是 `std::vector` 的 Obj-C 壳，因此会本能地回避「在前端 insert / removeFirst」的写法。**事实并非如此。**[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2014 年用 `class-dump` + Hopper 逆向出 iOS 7.0 SDK 里的真实实现类 `__NSArrayM`，发现它其实是一个**循环缓冲区 (circular buffer)**——两端插入删除都是 O(1)，本质上是一个 deque。

## Ivar 布局

```objc
@interface __NSArrayM : NSMutableArray {
  unsigned long long _used;             // 当前元素数（count）
  unsigned long long _doHardRetain:1;
  unsigned long long _doWeakAccess:1;
  unsigned long long _size:62;          // buffer 容量
  unsigned long long _hasObjects:1;
  unsigned long long _hasStrongReferences:1;
  unsigned long long _offset:62;        // 首元素在 buffer 中的偏移
  unsigned long long _mutations;        // 快速枚举失效戳
  id *_list;                            // 实际存储指针
}
```

`_size` 是 buffer 容量，`_used` 是逻辑元素数，`_offset` 是首元素在 buffer 里的起始位置。

## `objectAtIndex:` 的逻辑

逆向出的汇编翻译成 C 只有三行：

```objc
- (id)objectAtIndex:(NSUInteger)index {
  if (_used <= index) { /* throw */ }
  NSUInteger fetchOffset = _offset + index;
  NSUInteger realOffset  = fetchOffset - (_size > fetchOffset ? 0 : _size);
  return _list[realOffset];
}
```

这就是教科书循环缓冲区的取值公式——用一个条件减法代替 `%` 实现环绕。ARM64 下靠 `csel` 无分支实现，比 modulo 便宜。

## 为什么两端都是 O(1)

- **在末尾 append**：直接写 `_list[(_offset + _used) mod _size]`，`_used++`，无搬运。
- **在头部 insert**：不往后搬，而是把 `_offset` **往左绕一位**（变成 `_size - 1`），然后写入那个槽位。
- **头部 remove**：清掉 `_list[_offset]`、`_offset = (_offset + 1) mod _size`。
- **尾部 removeLast**：`_used--`。

因此把 `NSMutableArray` 当队列用不再有顾虑——push 前后都是 O(1)，不需要引入 `NSMutableDeque`（Foundation 里也根本没有这个类）。

## 中间 insert/remove 的搬运策略

`__NSArrayM` 从中间删除时**不是永远往前搬**——它会判断删除点距离哪一端更近，朝较近的一端搬运。这保证最坏情况只搬 `n/2` 个元素（普通数组是固定搬 n 个）。这个设计让循环缓冲区在非极端操作模式下也依然有优势。

## 容量增长 = 1.625×

每次 buffer 满了就按 **1.625** 倍扩容。这个非整数系数并非随意——Facebook folly 的 `fbvector` 文档证明 2× 扩容下**旧内存永远不能被未来的分配复用**（因为 2ⁿ > 2⁰+2¹+…+2ⁿ⁻¹），而 φ ≈ 1.618 附近的系数可以在若干次扩容后回收旧空间。1.625 是 13/8，大概率是为了整数运算方便的工程取整。

## 非收缩性

**`__NSArrayM` 永不收缩。**装过 14336 元素再全部清空，buffer 仍保留 14336 槽位。如果你用 `NSMutableArray` 临时装很大一批数据再清空想释放内存——不行，必须整个数组 release 掉重建。

## `initWithCapacity:` 的 hint 基本被忽略

```
Size: 2    // capacity 1
Size: 2    // capacity 2
Size: 4    // capacity 4
Size: 8    // capacity 8
Size: 16   // capacity 16
Size: 16   // capacity 32
Size: 16   // capacity 64
...        // 所有更大的都是 16
```

小容量走一条类似 `max(capacity, 某下限)` 的路径，然后截断到 16——作者的解读是 Apple 并不信任调用者给的容量 hint，反正 1.625× 扩容会快速调整。

## 和 `CFArray` 没有任何共享

最让作者震惊的发现：`CFArray` 和 `__NSArrayM` **没有代码共享**。`CFArray` 也是 deque，但实现用的是**两端填零的 padded buffer**——预留空闲槽放在 buffer 左右两侧，添加元素时直接吃掉 padding，不用绕环。两套实现各有取舍长期共存。这也顺带打破了「Foundation = CoreFoundation 壳」的常见误解。

## 相关机制

背后真正使逆向成为可能的是 [[objc-runtime-internals|modern Obj-C runtime]] 的 ivar 间接寻址：每条读 ivar 的 ARM64 汇编都得先从 `_OBJC_IVAR_$___NSArrayM._used` 这样的全局变量读偏移，再加到 `self` 上。这是 Apple 解决 fragile base class 的方式——旧二进制在新 Foundation 下仍然能对齐 ivar。

类似的紧凑存储思路也可参见 [[nsdictionary-linear-probing|`__NSDictionaryI` 的 indexed ivars]]——那是更极端的版本，把整段 hash 表直接塞进对象尾部。

## Sources

- [[sources/ciechanow-exposing-nsmutablearray]]
