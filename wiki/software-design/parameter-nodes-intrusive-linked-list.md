---
tags: [data-oriented, memory-layout, linked-list, bitsquid]
date: 2026-04-19
sources: 1
---

# 池化数组上的 intrusive 链表

Bitsquid 用"声音实例的参数集合"做案例展示的一种经典 DOD 容器：**把链表节点全部放在一个固定大数组里，SoundInstance 只存一个头指针**，用索引/指针在数组内部串起来。既保留了链表"每实例可变长度、总量可控"的灵活性，又拿到了数组"物理相邻、cache 友好"的访问性。

## 演化路径

起点是 `std::map<std::string, ParameterValue>` + 每实例一个堆上 map，五步改造：

1. **字符串哈希化**——`IdString32` 替掉 `std::string`。只有给终端用户看的字符串才该是 string；
2. **union 吃掉 type tag**——`union { IdString32; float; }`，8 字节 POD。访问时上下文已知类型，放弃 assert 换密度；
3. **`std::map` → `std::vector` + 线性搜索**——典型 <10 个参数，线性扫比二叉树快也简单；
4. **vectors-of-vectors 警报**——512 实例就是 512 次堆分配；换成每实例固定数组 `Parameter p[MAX]` 但浪费内存；
5. **array-embedded intrusive linked list**——全局 `ParameterNode nodes[MAX_PARAMETERS]`，SoundInstance 只存 `ParameterNode* head`，`node.next` 也是指向同一数组的指针。

## 分配策略

```
last_allocated = (last_allocated + 1) % MAX_PARAMETERS
if nodes[last_allocated].key == 0: break
```

从上次分配位置往前扫找空槽。**同一个 sound 的参数都是同一帧前后分配的**，所以它们自然落在数组相邻几格——既保住链表语义又拿到数组局部性。当 `last_allocated` 绕一圈回来时大多数短命 sound 早已停止，只有少数长命 loop 占位，整体仍然"大致相邻"。

## 适用前提

- **N 小**（典型 <10）：线性遍历链表不付性能代价；
- **寿命同期**：一起分配、一起释放的数据才能享受这套分配策略的局部性；
- **容量封顶可接受**：`MAX_PARAMETERS` 超了就拒绝；如果不能封顶，用 `std::vector<ParameterNode>` + index 替代指针（指针会随 realloc 失效）。

## 和其他容器的关系

这是 [[cache-friendliness]] 在变长结构上的一般答案：**凡是变长小集合，先考虑能否池化**。思路与 [[animation-stream-cache-layout]] 的 active 数组一致——都是"按访问局部性选布局"。也是 Frykholm 在多篇文里反复出现的主题：**避免 vectors-of-vectors**、**避免 std::map**，这些都是 [[red-flags]]。

## 相关

- [[animation-stream-cache-layout]]
- [[cache-friendliness]]
- [[aos-vs-soa]]
- [[pragmatic-performance-philosophy]]
- [[non-cryptographic-hash]]
- [[red-flags]]

## Sources

- [[sources/bitsquid-dod-sound-parameters]]
