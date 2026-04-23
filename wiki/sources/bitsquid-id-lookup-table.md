---
tags: [source, bitsquid, data-oriented, id-lookup, handle, decoupling]
date: 2026-04-19
sources: 1
---

# Managing Decoupling Part 4: The ID Lookup Table（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2011 年 9 月的博文，给出三种 ID→Object 查找实现的逐级优化。是 Bitsquid Managing Coupling 系列的续篇（参考 [[bitsquid-managing-coupling]]、[[bitsquid-managing-coupling-part-2]]）。

## 摘要

Bitsquid 用 ID 而非指针引用跨系统对象：ID 是 POD，不悬空，允许被引用系统随意重排、删除对象而无需 refcount 同步。问题在于「ID → Object」的查找数据结构如何高效。作者依次给出三种方案：

1. **STL**：`std::map<ID, Object*>`，heap 分配，cache 差，比后面慢 40×。
2. **Array with holes + freelist**：`vector<Object>` 线性排布，ID = `{index, inner_id}`，删除留洞并用 freelist 复用洞的内存串起来；查找一跳 O(1)，代价是对象暴露 index 不能移动、遍历会碰洞。
3. **Packed array**：加一层 `indices` 间接，`objects` 紧密无洞；删除用 swap-and-pop 并修对应 `indices`。查找两跳但遍历最优，ID 可压回 32 位（16+16 分 index 与 generation），配 FIFO freelist 防 generation 碰撞。

作者在评论里回答了多个子系统共享 transform 的问题：**每个系统自己排自己的数据**，高层做映射拷贝；这样局部随机访问仍然在紧凑数组里，比跨堆好。

## 关键要点

- ID 是 POD 的解耦契约，而不是性能工具。
- `inner_id` generation 位用来区分「同一槽位新旧对象」。
- freelist 指针复用 hole 内存——零额外分配。
- LIFO freelist + 小 inner_id 会快速生成碰撞，FIFO + 最少 N 空槽才安全。
- Packed array 的间接层是「外部 ID 语义稳定」和「内部遍历紧密」的折中。
- 代码有 corner case：`_freelist_dequeue == MAX_OBJECTS` 时需 wrap（评论指出并修复）。

## 链接到的概念

- [[id-lookup-table-packed]]
- [[id-based-lifetime-with-kill-flag]]
- [[handle-based-resource-manager]]
- [[system-decoupling-patterns]]
- [[entity-index-reconstruction]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/09/managing-decoupling-part-4-id-lookup.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-09-23_managing-decoupling-part-4-the-id-lookup-table.md`
