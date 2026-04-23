---
tags: [id-lookup, handle, packed-array, data-oriented, decoupling]
date: 2026-04-19
sources: 1
---

# ID 查找表：从 std::map 到 packed array 的三级演化

[[niklas-frykholm]] 在「Managing Decoupling Part 4」里给出了 Bitsquid 做「ID → Object」查找的三种实现，依次更好。所有方案都以「用 ID 而不是指针引用其他系统对象」为前提（理由参考 [[system-decoupling-patterns]]、[[id-based-lifetime-with-kill-flag]]）：POD、不悬空、允许持有方重排内存、不需要 refcount 线程同步。

## 1. STL：`std::map<ID, Object*>`

教科书写法：对象 heap 分配，ID 自增计数，`map` 做查找。问题是 cache 恶劣——对象单独 new 散布堆上，`map` 又是红黑树走指针。实测比后面方案慢 40 倍。除了性能，ID wrap around 到 4B 以后还会重复。

## 2. Array with holes + freelist

对象塞进 `std::vector<Object>` 线性排列，ID 变成 `{index, inner_id}` 复合结构：

- `index` 直接定位 vector 位置——查找退化为一次数组下标；
- `inner_id` 验证「这个槽位上的对象还是不是当初那个」，防止槽位重用后老 ID 还能命中。

删除留下 hole，用 **freelist 把 hole 串起来**——freelist 指针复用 hole 本身的内存（死对象占的内存反正不用了）。新对象优先填 hole。

代价：ID 从 32 位变 64 位。可以拆 `16+16`（`index` 和 `inner_id` 各占半），但要把 LIFO freelist 改成 FIFO 并保留最少 N 个空槽，这样 `inner_id` 冲突要等同一槽位轮 `N * 64K` 次才出现。

缺点：因为 `index` 暴露在外，对象**不能移动**。遍历时 hole 会被一并触碰，cache 利用率下降。

## 3. Packed array + 间接层

再加一级 index 数组换取对象的「可移动」：

```
ID → indices[ID & MASK].index → objects[index]
```

`indices` 数组保留 ID 语义，`objects` 紧密排布无洞。删除时做经典的「swap-and-pop」——把末尾对象搬到被删位置，然后修改那个对象对应的 `indices` 项使其指向新位置。

此时系统内部遍历（最频繁的操作）完全无洞、连续 cache 友好；外部 ID 查找多一跳但仍是 O(1)；ID 可以压回 32 位（`16` 位槽位 index + `16` 位 generation）。freelist 用 FIFO，每次分配给 index 一个新 `NEW_OBJECT_ID_ADD = 0x10000` 的 generation，旧 ID 的 `has()` 就会因为 `in.id != id` 而失败。

## 工程细节

评论区指出一个 bug：填满到 `MAX_OBJECTS` 后 `_freelist_dequeue` 指向越界；修复需在 `remove()` 里判断并回指 `_freelist_enqueue`。

另一个常被问的设计问题：如果多个子系统都要持有同一 entity 的「transform」，每个系统是否自己拷一份？作者回答是：**每个系统维护自己的数据顺序**（animation 按骨骼、scenegraph 按节点、renderer 按 texture 排序），高层把某系统的结果映射到另一系统（`for b in Bones: Node[bone_to_node[b.i]].tm = b.tm`）。局部随机访问在一个紧凑数组里仍然比跨堆指针好，参考 [[aos-vs-soa]]、[[cache-friendliness]]。

## 相关

- [[id-based-lifetime-with-kill-flag]]
- [[handle-based-resource-manager]]
- [[system-decoupling-patterns]]
- [[data-driven-architecture]]
- [[entity-index-reconstruction]]

## Sources

- [[sources/bitsquid-id-lookup-table]]
