---
tags: [source, 资源管理, 句柄, 热重载, 引擎架构, cache]
date: 2026-04-19
sources: 1
---

# Alternatives to Object Handles（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2011 年 3 月写给自己的一条「too tired to polish」笔记：除了经典的「Handle + Manager + RefCount」方案，资源热重载还可以怎么做？列出 4 条备选 + 1 条 hybrid，全部附上 pros / cons。

## 摘要

Pesce 先列基线的痛点：额外 indirection 的 cache miss；refcount 对循环引用无能为力、析构链式开销。然后提出四种替代：

1. **指针 patching**——manager 维护 `资源 → 所有持有点` 的 multimap，换资源时扫表修改所有 pointer。持有零开销；但赋值写入路径大幅变贵、线程安全难做、容易漏注册临时 copy。
2. **硬编码 GC**——每个类实现 `walk()` 给出它持有的资源；manager 持有全局对象表，换资源前跑可达性扫描。循环引用免费，但每次热重载都 ≈ 一次 GC 开销、并行化极难。
3. **全局位置列表**——方案 1 的简化版，用线性表替代 multimap。写便宜、换贵。
4. **置换数组 (perm table)**——句柄→perm→资源两层 indirection，perm 可自由重排以获得 cache 局部性。但「数据访问顺序和数据重排方向对齐」的场景很少，多数时候反而多一次 miss。

评论区补充：**如果数据有空间属性（2D 点等），先按四叉 / kd 树按空间 leaf 分组 → 每个 leaf 顺序存储**，方案 1 / 3 / 4 的问题都能被缓解；反之若访问是随机的，cache miss 无可奈何。

## 关键要点

- 所有方案的核心取舍：**cache locality / indirection cost** × **换资源的代价** × **线程安全与实现复杂度** × **接口对使用方的侵入度**。
- Pesce 举的那个「资源小到只是一个 GPU 指针」的例子，正是今天 [[bindless-rendering|bindless rendering]] 在 shader constant 上的形态。
- 十几年后主流答案：[[handle-based-resource-manager|index + magic number 的句柄]]——接受一次 indirection、用版本号验证 dangling、显式生命周期管理、不做 patch 也不做 GC。
- 文章的价值是**把「这件事还有别的做法」写出来**——即使最终工业没选它们，知道自己为什么没选也是工程素养。
- Hybrid 思路（按指针高位 bit 分桶 → 同桶换资源不需要更新 multimap）和现代 slab allocator / page-local 策略的精神一致。

## 链接到的概念

- [[hot-swap-pointer-patching]]
- [[handle-based-resource-manager]]
- [[id-based-lifetime-with-kill-flag]]
- [[bindless-rendering]]
- [[garbage-collector]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/03/alternatives-to-object-handles.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-03-02_alternatives-to-object-handles.md`
