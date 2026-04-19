---
tags: [软件设计, 性能, 特化, 反通用]
date: 2026-04-19
sources: 1
---

# 打败专家的"作弊"术：只解更小的问题

Ben Supnik 有一篇标题党意味浓厚的博文——*This One Weird Trick Let's You Beat the Experts*。骨架只有一句话：

> 你打不过 `malloc` 的作者。但你可以不做他做的事情。

新人常在 StackOverflow 上问"怎么写一个比系统分配器还快的自定义 allocator"，被资深程序员劝退："系统 `malloc` 是黑胡子大神在藏传佛寺用沙子 IDE 花十年写的，你写不过的。"表面上这是对的——**同样功能集**下你写不过专家。Supnik 给的反击是：**改变功能集**。

## 作弊例 1：世界上最烂的 allocator

```cpp
static char s_buffer[1024];
void* cheat_malloc(size_t bytes) { return s_buffer; }
void  cheat_free (void* block)   { }
```

无可否认的事实：**它比 `malloc` 快**。只要你不要求它能分配多次、能处理 >1K、能真的 free——它就成立。这种「世界最烂」的 allocator 不是用来用的，而是一个极端例子，说明**问题规格决定性能上限**。

## 作弊例 2：Bump Allocator（[[linear-allocator|线性分配器]]）

游戏程序员都会的一招：一块大 buffer + 一个 offset 指针，分配就是加法，free 是 no-op，帧末把 offset 清零整体回收；多线程就每线程各一块。

- 单次分配：一条加法
- free：零操作
- 锁：无
- cache 命中：连续分配 → 连续内存

代价是你**必须**接受它的规格：所有当帧内存统一生命期；不支持任意顺序 free；容量必须是前算好的峰值。对游戏的 per-frame 数据，这些约束几乎天然成立——于是 bump allocator 在游戏引擎里无处不在，性能吊打 `malloc`。

## 抽象公式

Supnik 把这件事抽成三问：

1. 我是否**确实需要**比标准实现更快？
2. 我的**抽象需求是否比完全通用的情形更简单/更特别**？
3. 我能否**用这些不同的/有限的需求**写出更快的实现？

三条全 YES，自己动手才是合理的。只要有一条不成立——比如"其实 `malloc` 够快"、或"我的用法就是完全通用"——就用系统实现。

## 适用面远不止分配器

- **网络协议**：`TCP` 保证"网线不丢数据"，代价是确认重传和拥塞控制的一大堆开销。游戏/媒体流经常自研 UDP 协议，因为它们的丢包策略不是"重传"而是"丢弃后插值/跳帧"。
- **数据结构**：哈希表满足了"任意键、动态扩容、删除"，但当键空间小且固定时，[[non-cryptographic-hash|完美哈希]] / 紧凑位图能跑到它的数倍以上。
- **字符串处理**：标准 `strcpy` / UTF-8 解析要处理所有 Unicode 细节，但数值解析专用代码可以用 SIMD 一次扫一块。
- **压缩**：`zlib` 是通用通吃，但 [[oodle-compression-suite|Oodle]] 等领域特化编解码针对游戏纹理/动画能跑出完全不同的曲线。
- **渲染**：[[shader-permutation-explosion|shader 变体]]本身就是"只解当前材质需要的那部分"的极端例子。

## 核心教训

**通用实现 = 通用代价**。工程师的第一本能是"用别人写好的库"——这通常是对的。但当库里的通用性不是你的需求时，它就是纯开销。

> 专家在下象棋。你通过下井字棋赢他们。

这和 [[future-proofing-tests|别做未验证的 future-proofing]] 是同一枚硬币的两面：都是 **"少做，做得更好"**；都反对把想象中的灵活性烙进今天的代码。Ousterhout 的 [[deep-modules|深模块]] 与 [[false-abstraction|虚假抽象]] 讨论的是「抽象粒度对了没」；Supnik 这里补的是「抽象**范围**对了没」——接口里多一个不需要的自由度，就是一条要背的性能账。

## 什么时候不能作弊

- 你在写**库**，无法预设调用方的限制。这时候通用性本身就是需求。
- 你的数据规模真的是任意的——比如一个文本编辑器的 buffer，不能假设大小。
- 团队里会有新人接手，限制条件难以文档化。这时 **overhead 换 predictability** 是合理的。

Supnik 自己也加了一句："你可能需要一个更快版本的完全通用实现——那是另一篇博文，你得有一把长胡子。"

## 相关

- [[linear-allocator]] — Bump allocator，本文的主例
- [[future-proofing-tests]]
- [[graphics-programmer-constraints]]
- [[deep-modules]]
- [[false-abstraction]]
- [[oodle-compression-suite]]
- [[shader-permutation-explosion]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-beat-the-experts]]
