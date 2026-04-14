---
tags: [objective-c, 数据结构, hash-table, linear-probing, ios, 逆向工程]
date: 2026-04-14
sources: 2
---

# `__NSDictionaryI` 的线性探测哈希表

`NSDictionary` 是 Foundation 里最常用的关联容器，但官方对其内部不做任何承诺。[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2014 年逆向 iOS 7.1 SDK 发现：真实不可变子类 `__NSDictionaryI` 其实是一个**开放寻址 + 线性探测**的哈希表，而且整个 key-value 存储就**紧跟在对象末尾**——靠 Obj-C runtime 的 indexed ivars 一次 malloc 搞定。

## Ivar 布局（看起来不像哈希表）

```objc
@interface __NSDictionaryI : NSDictionary {
  NSUInteger _used:58;
  NSUInteger _szidx:6;
}
```

**仅此而已。**没有 bucket 数组指针、没有 keys/values 分离数组。秘密在 `class_createInstance(cls, extraBytes)`：Obj-C runtime 可以在对象后面追加变长内存，通过 `object_getIndexedIvars()` 取得起始指针：

![indexed ivars](../../raw/assets/a0edb9b695310840.jpg)

`__NSDictionaryI` 把 key-value 对交替排成一段连续区域 `key₀, val₀, key₁, val₁, …`——作者猜测原始源码大概是 `struct { id key; id object; }` 的数组。这么做有三个好处：

1. **cache 友好**：紧跟对象尾部的内存最可能已经在缓存里，见 [[cache-friendliness]]。
2. **一次分配**：对象 + 存储只调一次 `calloc`。
3. **class-dump 抗性**：外部工具看不到指向存储的 ivar，反倒成了一种 obfuscation。

代价是**大小固定**——不可变字典天然适合这个模型，可变字典 `NSMutableDictionary` 处理复杂得多。

## 算法：`objectForKey:`

逆向出的等价代码：

```objc
- (id)objectForKey:(id)aKey {
  NSUInteger sizeIndex = _szidx;
  NSUInteger size = __NSDictionarySizes[sizeIndex];
  id *storage = (id *)object_getIndexedIvars(self);
  NSUInteger i = [aKey hash] % size;
  for (int probe = 0; probe < size; probe++) {
    id fetchedKey = storage[2 * i];
    if (fetchedKey == nil) return nil;              // 空槽→ miss
    if (fetchedKey == aKey || [fetchedKey isEqual:aKey]) {
      return storage[2 * i + 1];                    // 命中
    }
    i = (i + 1) % size;                             // 线性探测
  }
  return nil;
}
```

三个关键点：

- **开放寻址 / 线性探测**：碰撞时走下一个槽，遇到 nil 立即终止——这就是 nil 作为「空槽标记」的前提，也是为什么不能把 nil 当 value。
- **指针优先比较**：`fetchedKey == aKey` 在 `isEqual:` 之前测——这让 `NSString` literal、tagged `NSNumber`/`NSDate`/`NSIndexPath` 几乎永远零成本命中。
- **`objectForKey:nil` 不检查**：作者认为这其实是正确设计——派发器不应该为每次调用加这个分支。

## size 表：64 个精心挑的质数

`__NSDictionarySizes` 是一张 64 个 `NSUInteger` 的静态表：

```
0, 3, 7, 13, 23, 41, 71, 127, ...
```

每个都是质数（减少某些 hash 分布下的聚集），但**不是连续质数**——相邻比约 **1.637**，和 [[nsmutablearray-circular-buffer|`__NSArrayM` 的 1.625]] 非常接近，都在 φ ≈ 1.618 附近以便旧内存能被回收。

## capacity 表：装载率 62% 的上限

与 sizes 配对还有 `__NSDictionaryCapacities`：

```
0, 3, 6, 11, 19, 32, 52, 85, ...
```

注意比 sizes 小。`+ __new:::::` 初始化时线性找第一个 `capacities[i] ≥ count` 的 `i` 作为 `_szidx`。这意味着哪怕你塞 41 个元素，实际分配的 bucket 数是 **71**——作者换算为**装载率永远不超过 62%**。这是作者认为最干净的工程决策之一：以空间换碰撞链长的下降曲线。

（trivia：表里最后一个非零项是 0x11089481C742 ≈ 18.7 万亿，你在 64 位机上几乎不可能撑爆。）

## 实战陷阱 1：`objectForKey:nil` 可能误命中

```objc
NSDictionary *d = @{ [BC3DIndex new(2,8,5)] : @"A black hole!",
                     [BC3DIndex new(0,0,0)] : @"Asteroids!",
                     [BC3DIndex new(4,3,4)] : @"A planet!" };
[d objectForKey:nil];   // → @"Asteroids!"  ❌
```

为什么？`[nil hash]` 返回 0，线性探测从第 0 槽开始找，遇到 `BC3DIndex(2,8,5)`；这个 key 的 `isEqual:nil` 经过 `objc_msgSend` 的 nil 短路会把 `other.i/j/k` 读成 0——和 nil 的三个属性相等——返回 YES。**经验法则：自定义 key 的 `isEqual:` 必须 nil-safe。**

## 实战陷阱 2：hash 模同余退化成 O(n)

作者造了一组 key，hash 分别是 1, 8, 15, 22, 29, 36——都 mod 7 = 1（7 是 size）。查 36 时所有 key 都要走 `isEqual:`：

```
Key #36 asked for hash
Key #1  isEqual: #36 → NO
Key #8  isEqual: #36 → NO
Key #15 isEqual: #36 → NO
Key #22 isEqual: #36 → NO
Key #29 isEqual: #36 → NO
Result: 6
```

线性探测最怕的就是这种「模 size 同余」的对抗性输入。正常随机 hash 很难触发，写坏 `hash` 函数可以轻易触发——**hash 分布是字典性能的第一前提**。

## 附：ARM64 汇编层的小技巧

作者另有一篇[[sources/ciechanow-nsdictionary-objectforkey-assembly|ARM64 汇编附录页]]逐条翻译了 `objectForKey:` 的 60 条指令，里面几个值得学习的低层招数：

- **`cmp + ccmp + b.eq`**：一条条件比较指令实现 `if (x == 0 || x == y)` 的无分支融合。
- **`udiv + msub`**：ARM64 没有硬件取模指令，靠这两条合成 `hash % size`。
- **`lsl, #1` + `orr, #1`**：`2*i + 1`——从 key-object 交替数组里取 value 槽。
- **lazy binding**：调用的是 `imp___stubs__object_getIndexedIvars` 而非本体函数，首次命中才解析。

## Sources

- [[sources/ciechanow-exposing-nsdictionary]]
- [[sources/ciechanow-nsdictionary-objectforkey-assembly]]
