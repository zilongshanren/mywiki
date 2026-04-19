---
tags: [数据结构, C, 内存管理, 分配器]
date: 2026-04-19
sources: 1
---

# Segment Array（分段数组）

一种同时具备**常数时间随机访问、追加时指针稳定、不需连续内存**的增长型容器，多人独立发现、多名字并存：2001 年论文叫 *levelwise-allocated pile*，Zig 标准库叫 *Segmented List*，Per Vognsen 叫 *Segment Array*。C++ 的 `std::deque` 表面相似但内部结构不同。Daniel Hooper 在他的构建可视化工具里用它存「运行中未知数量的事件」。

## 结构

结构体里固定一个指针数组，每个指针指向一段（segment），**段大小按 2 的幂递增**：

```c
typedef struct {
    u32 count;
    int used_segments;
    u8 *segments[26];
} SegmentArrayInternal;
```

指针数组放在结构体内而非外部分配，意味着**索引时大概率只命中一次缓存行**。段为 2 的幂后，`log2(index)` 就能直接定位所在段，再一次减法得到段内偏移。

为什么是 26 段？推导链条是一组硬件 / 类型事实：64 位 CPU 仅能用 48 位虚拟地址 → 最多 48 段；用 `uint32_t` 索引 → 减到 32 段；最小的 6 段（1/2/4/8/16/32 元素）管理开销不值，去掉 → 剩 26 段，可容纳 `~4.29e9` 个元素，接近 `UINT32_MAX`。

## 寻址代码

```c
int segment = log2i((index >> SMALL_SEGMENTS_TO_SKIP) + 1);
u32 slot = index - capacity_for_segment_count(segment);
return sa->segments[segment] + item_size*slot;
```

`log2i` 用 `__builtin_clzll`（count-leading-zeros）计算。Clang `-O3` 下 `_sa_get` 编译为 **10 条 x86-64 指令**：`shr / inc / bsr / shl / add / add / imul / add [mem] / ret`。取数的真实耗时由内存加载而非地址算占主导，这一点和普通数组一致。顺序遍历连这 10 条都可以省——macro 直接嵌套双层 `for` 走段内连续内存。

## 增长操作

```c
if (sa->count >= capacity_for_segment_count(sa->used_segments)) {
    size_t slots_in_segment = (1 << SMALL_SEGMENTS_TO_SKIP) << sa->used_segments;
    sa->segments[sa->used_segments] = malloc(item_size * slots_in_segment);
    sa->used_segments++;
}
sa->count++;
```

**不 `realloc`、不搬旧数据、指针永不失效**。这也是它能和 [[linear-allocator|arena 分配器]] 无缝配合的原因——arena 最怕「把 10MB 大块扔在中间」这种洞，Segment Array 只追加不搬家，不产生洞。

## 何时选它

Hooper 列了六种常见选择的对比表：

|  | 可增长 | 指针稳定 | 随机访问 | 连续内存 |
|---|---|---|---|---|
| 固定数组 | × | ✓ | ✓ | ✓ |
| 动态数组 | ✓ | × | ✓ | ✓ |
| 分块链表 | ✓ | ✓ | × | × |
| 混合（初始化后变固定） | ✓（创建时）| ✓ | ✓（创建后）| ✓（创建后）|
| 虚拟内存数组 | ✓（预留上限）| ✓ | ✓ | ✓ |
| Segment Array | ✓ | ✓ | ✓ | × |

Hooper 自己**默认用固定数组或混合方案**；当「运行期生成数量未知、又用不了虚拟内存」时（手机、WASM、或不想预占地址空间）才上 Segment Array。它的 header 是 216 字节（vs 动态数组 24 字节），只适合存**程序的中心大数组**（所有 Entity、所有 Sample），不适合当小容器。

## 两个变体技巧

- **类型安全泛型**：用 `union { SegmentArrayInternal internal; T *payload; }` + `typeof(payload)` 宏，给 C 的泛型数据结构套上类型检查——这是 Hooper 上一篇文章的套路；
- **2 的幂容量**：令前两段同尺寸即可让整体容量永远是 2 的幂，方便作为 [[open-addressing-hashtable|open-addressing 哈希表]] 的后备存储，避免 50% 空间浪费。

## 相关

- [[linear-allocator]] — Segment Array 对 arena 友好的核心原因
- [[open-addressing-hashtable]] — 2 的幂容量变体的用法
- [[data-structure-invariants]] — 容器内部指针稳定性的另一篇讨论
- [[daniel-chase-hooper]]

## Sources

- [[sources/hooper-segment-array]]
