---
tags: [source, hacksoflife, 并发, 引用计数, 锁, 资源管理, 双重检查]
date: 2026-04-27
sources: 1
---

# Second. Worst. Lock. Ever.（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2020 年 6 月的文章，是 2016 年[[sources/supnik-worst-lock-ever|"Worst Lock Ever"]]的后续。记录了对引用计数+全局表查找这一并发设计的第三次迭代——通过双重检查模式（先原子减、再条件锁）彻底解决了"正确但愚蠢"的第二版本问题。

## 摘要

第一版（先 dec 再锁）有竞态（race），第二版（先锁再 dec）正确但代价极大：表锁在创建时可能被持有数十毫秒（等待磁盘 IO），所有 smart handle 的拷贝构造和析构都要争抢这把锁，导致"仅仅移动所有权"这种本应极快的操作偶尔会导致渲染帧卡顿 100ms，破坏了 API 契约（client 不会预料到拷贝 handle 是"慢操作"）。

第三版（"取其精华"的双重检查）：

```cpp
void object::release() {
    if (m_count.decrement() == 0) {
        RAII_lock(m_table_lock());
        if (m_count.load() > 0) return;  // 有人抢先复活了它
        m_table.erase(this->name);
        delete this;
    }
}
```

先做原子减，只有在结果为 0 时才去争锁；拿到锁后再验一遍 count（防止极小窗口内有人复活）。胜率分析：count > 0 的普通 release 完全无锁；count → 0 说明调用方本来就准备好了释放资源，这类操作本就不在快速路径上。

## 关键要点

- 第二版"先锁再 dec"是正确但错误代价位置：把慢锁放在本应超快的 smart handle 操作上
- API 契约问题：client 不应预料"移动所有权"会慢，只有"真正释放资源"才应该慢
- 双重检查模式：原子 dec → 判零 → 加锁 → 再验 count → 删除，大幅降低热路径锁开销
- Vulkan 异步加载使资源有"构造中但已存在表里"的状态，这是另一层复杂性
- 评论中提到 move semantics 能避免一部分拷贝，但场景图 → 渲染收集路径**必须**拷贝引用，无法依赖 move

## 链接到的概念

- [[refcount-decrement-before-table-lock-race]]
- [[cas-refcount-lowbit-lock]]
- [[app-space-lock-free-simplification]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2020/06/second-worst-lock-ever.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2020-06-18_second-worst-lock-ever.md`
