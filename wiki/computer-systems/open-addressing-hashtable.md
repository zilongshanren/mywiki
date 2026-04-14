---
tags: [数据结构, 哈希表, 性能, 缓存, SIMD]
date: 2026-04-14
sources: 1
---

# 开放寻址哈希表（Robin Hood 线性探测）

**经验法则**：你默认的哈希表应该是开放寻址 + Robin Hood 线性探测 + backward-shift 删除；当内存不是瓶颈而查询延迟必须确定时，two-way chaining 是同样好的备选。`std::unordered_map` 用了分离链式，在 C++ 界已被视作标准库的历史失误——它违背了「不为未请求的特性付代价」的原则。

## 为什么 flat 胜过 chained

分离链式把每个桶实现成链表，逻辑简单、好分析，但**所有操作都要追指针**，没法让 CPU 预取。开放寻址把所有条目放进同一块 flat 数组，冲突时就地往后探测，访问模式更连续。常见的「链式好处」在实践里都站不住脚：

- 「不需要线性时间操作」—— 分离链式同样需要 amortized 扩容。开放寻址同样可以增量扩容。
- 「条目地址稳定」—— 加一层 pointer-to-entry 间接即可。
- 「内存更省」—— 只有在堆分配器开销被忽略时才成立，现实里 flat + 高装载因子反而更省。

真正「只能用链式」的场景只有一种：不能分配、条目不能移动（例如 [[c-interface-oop|intrusive 链表]] 这种内核常见模式）。

## 探测策略谱系

**Linear probing**：冲突时线性往后走。`h(k)+n` 简单、缓存友好，但**聚集**问题严重——90% 装载下最大探测长度能飙到上千。

**Quadratic probing**：探测序列是 $h(k) + \frac{n(n+1)}{2}$，可以用递推求下一个 index 不用真正做平方。均值和最大长度都明显改善，但没有朴素的删除算法。

**Double hashing**：探测步长由第二个哈希决定：$h_1(k) + n \cdot h_2(k)$。2 的幂表下只要让 $h_2$ 永远返回奇数即可保证触达每个桶。均值 probe 更小，但跨 cache line 多，实测反而比 quadratic 慢。

**Robin Hood linear probing**（胜者）：插入时允许「抢占」——如果当前桶里的 key 离其理想位置比新 key 更近，就交换两者，继续插入被踢出的那一个。这样探测长度被非常**均匀地**摊薄。Slater 的 benchmark 里 90% 装载下最大 probe 只有 58，比朴素线性的 1604 强两个量级。**它解决了开放寻址最大的痛点。**

## Backward-shift 删除

传统开放寻址用 tombstone 标记已删槽，但 tombstone 累积会让 miss 查询越跑越慢。*Backward-shift* 删除是个少人讲但很优雅的算法：删掉某槽后，往后依次把「不在自己最佳位置」的 key 前移一格，直到遇到空槽或已在最佳位置的 key。

- 线性探测版本：要重新比较 `hash % N` 才知道能否前移。
- Robin Hood 版本更漂亮：**只要看到一个 key 已经在最佳位置就停**——因为它之前的 key 不可能越过它被推远。而且可以直接位移不用再 hash。

用了 backshift 就可以彻底丢掉 tombstone，miss 查询的平均 probe 长度瞬间降回近 1。

## Two-Way Chaining：确定性的极致

Cuckoo hashing 家族里最工程友好的一支。每个桶容纳一小把 key（比如 4-8 个），插入时同时 hash 出两个候选桶，放进空位较多的那个；两者都满就扩容。理论结果：添加第二个 hash 把期望最大桶大小从 $O(\log N / \log\log N)$ 压到 $O(\log\log N)$，于是**探测长度可以被小常数硬绑定**。Slater 测得 4-槽版本最大 probe = 6，几乎是常数时间查找，缺点是高内存放大（2× 起步）。

## CPU 级优化：unrolling / prefetch / SIMD

现代乱序 CPU 一次能在飞 ~10 个 pending load。裸循环其实已经能让硬件把多次 find 并行起来，所以手工 unrolling 没什么用。真正有效的是**软件预取**：先把批量 key 都 `prefetch` 到 cache line，再进入真正的 lookup 循环，开放寻址的 find 时间从 30ns 降到 20ns 左右。

**SIMD 探测**：用 AVX2 一次比较 4 或 8 个 key，对 two-way chaining 特别适合（一个桶刚好塞进一个 cache line）。对线性探测则鸡肋——平均 probe 只有 1.5 次，SIMD 的 setup 开销反而吃掉收益。

## 结论

- **默认选 Robin Hood 线性探测 + backward-shift 删除**，装载因子 75%。
- 如果查询延迟必须稳定（交互式、实时），换 **Two-Way Chaining**，配合 prefetch 和 SIMD。
- 表大小用 2 的幂是为了 `&` 取模；代价是 hash 高位会被丢弃，需要 hash 函数本身靠得住（文章用 `squirrel3`）。
- `std::unordered_map` 在所有维度上都被打败，但它的 API 仍然在标准库里，原因纯粹是兼容性债务。

## 相关

- [[cache-friendliness]] — flat 数据结构快的根本原因
- [[linear-allocator]] — 另一种「连续内存就是快」的例子
- [[gpu-latency-hiding]] — CPU 乱序执行和 GPU 藏延迟是一个思想
- [[max-slater]]

## Sources

- [[sources/slater-optimizing-open-addressing]]
