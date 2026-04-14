---
tags: [objective-c, runtime, ios, ivar, 动态派发]
date: 2026-04-14
sources: 2
---

# Objective-C Runtime 内部机制

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2014 年逆向 `__NSArrayM` 和 `__NSDictionaryI` 时顺手把 modern Objective-C runtime 几个非常有用的底层机制都讲了一遍——这些机制解释了为什么 Foundation 里的 ivar 布局是可进化的、为什么子类能在对象末尾「偷偷」长出一段存储、以及为什么一条 `[obj method]` 调用背后会有那么多间接。

## Class Cluster：公开类是抽象基类

`NSMutableArray` 本身是抽象的——`+[NSMutableArray new]` 返回的是内部子类 `__NSArrayM`。用 LLDB 一行就能验证：

```
(lldb) po [[NSMutableArray new] class]
__NSArrayM
```

文档化的 `NSMutableArray` 只要求子类实现 7 个原语方法（`count / objectAtIndex: / insertObject:atIndex: / removeObjectAtIndex: / addObject: / removeLastObject / replaceObjectAtIndex:withObject:`），其余 20+ 方法都由抽象基类默认组合实现——这是教科书级别的 [[interface-vs-implementation|接口与实现分离]]，但它也意味着你 `subclass NSMutableArray` 时继承的大多数方法其实性能很差（循环调用原语），所以具体子类经常自己重写一部分。

## Non-fragile ivars：每次读字段都多一跳

逆向 `objectAtIndex:` 时会看到每次读取 ivar 都经过这个模式：

```
adrp  x8, #0x1d1000
ldrsw x8, [x8, #0x2c]    ; x8 = *(int *)(page + 0x2c) = 当前 _used 偏移
ldr   x8, [x0, x8]       ; x8 = *(self + offset)
```

为什么不直接 hardcode 偏移？因为 fragile base class——如果 Apple 未来给 `NSObject` 加一个 ivar，旧应用二进制里固化的偏移就全错了。**modern Obj-C runtime 的解法：把每个 ivar 的偏移存成一个全局变量 `_OBJC_IVAR_$_ClassName._ivarName`，加载时可以由 runtime 改写**。你的二进制每次读 ivar 都多一次内存 fetch，换来二进制与最新 Foundation 的前向兼容。

这条机制让 Apple 可以随版本迭代 `NSArray`、`NSDictionary` 的内部结构而不必重编译 App Store 上所有 app。

## Indexed Ivars：对象尾部的变长存储

```objc
id class_createInstance(Class cls, size_t extraBytes);
void *object_getIndexedIvars(id obj);
```

`class_createInstance` 可以在创建对象时要求 runtime 多分配 `extraBytes` 字节，这段内存紧跟在常规 ivars 末尾。`object_getIndexedIvars` 返回这段内存的起点。`__NSDictionaryI` 用这个机制把整张 hash 表直接塞在对象后面，见 [[nsdictionary-linear-probing|`__NSDictionaryI` 的线性探测]]。

Indexed ivars 的三项好处：

1. **变长**——每个实例可以要不同大小的尾巴。
2. **cache 友好**——紧挨对象头，调 method 时大概率已经在 L1。
3. **反 class-dump**——不是 ivar，class-dump 看不到存储层；当然对手只要看 `object_getIndexedIvars` 调用就能识破，所以只是 obfuscation 而非 security。

两个注意点：`class_createInstance` 不能在 ARC 代码里直接用（得 `-fno-objc-arc`）；runtime **不记录**你要了多少 extraBytes，你要用变长 indexed ivars 就得自己存个长度字段。

## Objective-C 方法 = C 函数 + 两个隐藏参数

每个 `- method:(T)arg` 最终都是 C 函数 `method(id self, SEL _cmd, T arg)`。调用时 `self` 在 x0、`_cmd` 在 x1、用户参数从 x2 开始——这就是逆向 `objectAtIndex:` 时能直接从寄存器认出「第一个在 x0 是 self、第二个在 x2 是 index」的原因。

## Lazy Binding：`imp___stubs__`

你看到的 `bl imp___stubs__object_getIndexedIvars` 不是真的直接调库函数，而是调一个短桩：

- 首次触发时，桩会把控制权交给 dyld 查找真正的符号地址，然后**把结果写回桩指向的函数指针变量**。
- 此后每次调用都直接跳到真地址，只多一次间接跳转。

这让 app 启动时不用一次性解析所有动态符号（**lazy** binding），启动速度更快，代价是稳态调用多一次 indirect jump。

## Fragile Base Class 的另一面：动态子类化

另一项经常被忽视的能力：**subclass 可以在 runtime 动态生成**，比如 KVO 就是这么干的——`addObserver:` 时 Foundation 会给目标实例偷偷换上一个 `NSKVONotifying_XXX` 子类。这套机制依赖的正是 indexed ivar 布局和 ivar 间接寻址——子类可以在不破坏既有 ivar 偏移的前提下增加新行为。

## 相关

- [[nsmutablearray-circular-buffer]]
- [[nsdictionary-linear-probing]]
- [[interface-vs-implementation]]
- [[cache-friendliness]]
- [[calling-conventions-x86]]

## Sources

- [[sources/ciechanow-exposing-nsmutablearray]]
- [[sources/ciechanow-exposing-nsdictionary]]
