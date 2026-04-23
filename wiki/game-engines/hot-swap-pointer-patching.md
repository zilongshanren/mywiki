---
tags: [资源管理, 热重载, 引擎架构, 句柄, 内存, 缓存友好]
date: 2026-04-19
sources: 1
---

# 热重载的四种实现：Handle vs 指针 patch vs GC vs 置换表

[[angelo-pesce|Pesce]] 2011 年的一篇「写给自己的笔记」：传统的**对象句柄 + 管理器 + 引用计数**方案并不是热重载（hot-swap）与资源生命周期管理的唯一解，甚至不一定是最好的解。文章列了四种候选，写得相当疲惫——但思路值得留档，因为后续十几年里这些取舍被逐个重新发现过。

## 基线：Handle + Manager + RefCount

这就是 [[handle-based-resource-manager|基于句柄的资源管理器]] 的经典形态：所有资源由 manager 统一分配（数组或指针数组 + slot），调用方持一个 32-bit 句柄（索引或共享指针封装），用 refcount 管生命周期。

痛点 Pesce 一口气列了两个：

- **额外一层间接寻址**——每次取资源都 miss 一次 cache。资源很小（比如一条 shader constant 的 GPU 指针，例如 NVIDIA bindless graphics API 里那种）时，这一层间接比资源本身还贵。
- **引用计数并不便宜也不安全**——循环引用会漏，debug allocator 能发现但修起来烦；析构时一串链式 RC decrement / destruct 会触发连锁 cache miss。

这两个痛点是所有替代方案的起点。

## 方案 A：指针 patching（manager 记录所有「持有点」）

资源不走句柄，直接让持有者存裸指针。但 manager 额外维护一张 **multimap**：`资源指针 → 所有「指向它」的内存位置列表`。资源要移动 / 换身份 / 热重载时，manager 扫一遍这张表，把每一份 pointer 改过去。

- **+** 无额外 indirection，持有者不多占空间。
- **+** 可以把 heap 上的资源**重排序**以获得 cache 友好的访问顺序（小资源特别受益）。
- **+** 可以用 shared_ptr-like 的包装把接口做成习惯形态，甚至是 Boost intrusive_ptr 的替代（后者性能好但资源必须实现特定接口）。
- **−** **任何 pointer 赋值都要去 manager 里增删表项**——写入侧代价剧增。
- **−** 数据结构本身（平衡 multimap）不好实现。
- **−** 「patch 别人内存」天然脆弱：一不留神漏注册一份临时 copy，热重载就 UAF；多线程下更难保证。
- **−** 创建 / 销毁也更慢。

## 方案 B：硬编码 GC（可达性遍历）

每个持有 GC 对象的类都自己实现一个 `walk()` 方法，标记它指向的资源。每个资源一个 mark flag。manager 持有全局对象表，从 root 出发扫遍。

- **+** **循环引用不再是问题**。
- **+** 如果你已经有反射 / 序列化系统，`walk()` 几乎是白送的。
- **+** 顺便知道「谁在持有我」，方便调试。
- **−** **每次换资源都跑一次 GC 扫描**——不适合频繁热重载。
- **−** 接口大改，不能渐进引入。
- **−** 每个类写 walk，漏了一个就静默出错；临时 copy 同样要小心。
- **−** **并行 / 增量 GC 非常难写**。

## 方案 C：全局位置列表（简化版 A）

不要 multimap，直接维护一张「所有指向资源的位置」列表。热重载时线性扫一遍找到需要 patch 的位置。

- **+** 持有者依然零开销。
- **−** 换资源仍然要过整张表——和方案 A 比只是写入更便宜、换资源更贵，权衡拖到另一端。
- **−** 如果还想能枚举资源本身，还得再开一张资源表。
- **−** 同样是 patch 别人内存，线程安全同样难。

## 方案 D：置换数组（perm table）

在句柄和资源之间再加一层：句柄指向 `perm[]`，`perm[i]` 指向真实资源。这样可以**自由移动资源** + 重排 `perm[]` 以获得 cache 局部性。

- **+** 资源可移动、可排序。
- **−** 大多数访问模式本身没有 coherence，重排 `perm[]` 也救不了。
- **−** 资源很小（如 GPU 指针）时，`perm[]` 本身也 miss，**省不下一次 cache miss，反而多一层跳转**。
- Pesce 自评：**这一条大多数时候并不是个好主意**。

## 混合方案

副笔记里 Pesce 提了一个 hybrid：**按资源指针的高位 bit 划桶**，方案 A 只在「资源换桶」时才更新 multimap，同桶内 patch 一次即可。评论区补充：如果资源有空间属性（2D 点、空间分布），先按四叉 / kd 树分段装进多个小数组，在 leaf 内线性存——索引方案 (B) 在**访问顺序和数据顺序能对齐**时最强。

## 这一切的今天

十几年后，主流答案收敛为 [[handle-based-resource-manager|索引 + 代号（generation / magic）的句柄]]：版本号验证 + pool slot 复用 + 显式生命周期，放弃自动 GC 与自动 patch。Pesce 写这篇时的直觉是对的——**多一层 indirection 不是白送的**——但他列举的 patch / GC 路线最终没有赢过「加一个小版本号」这种更保守的工程妥协。这个反思本身对思考资源系统仍然有价值。

## 相关

- [[handle-based-resource-manager]] —— 工业界收敛的那个答案
- [[id-based-lifetime-with-kill-flag]] —— skynet 2.0 变体：actor 场景下的 id + kill flag
- [[id-lookup-table-packed]] —— Bitsquid 的三种句柄实现
- [[bindless-rendering]] —— Pesce 举的那个「资源小到一个 GPU 指针」的例子的今天形态
- [[garbage-collector]]
- [[ring-buffer-virtual-stream]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-alternatives-to-object-handles]]
