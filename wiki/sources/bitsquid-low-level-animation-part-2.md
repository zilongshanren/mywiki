---
tags: [source, bitsquid, animation, cache-layout, data-oriented]
date: 2026-04-19
sources: 1
---

# Low Level Animation — Part 2（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 10 月的文章，是 2009 年动画压缩文的续集，专门讲曲线拟合后的动画数据如何排布才对 cache 友好。

## 摘要

每条 track（一个骨骼的位置或旋转）曲线拟合后得到若干 `(t_i, A_i)` 曲线点。评估 `t` 时刻需要前后两个点。如果按 track 再按时间排布，100 骨骼 × 2 通道在一帧里会踩出 200 次 cache miss。Frykholm 的解法是把"当前激活的曲线点"单独抽成一个 **active 数组**（hot data），并把所有曲线点按**它们被需要的时间**排成一条单流——播放器只维护一个指向流的指针，时间推进时把点 copy 到 active 数组再求值。结果：取数据只走一次顺序指针前进 + 一次 active 数组访问，总共两次 memory access；流是严格线性访问，可以再 gzip 压一半，也方便从磁盘 streaming。代价是**不能任意跳转**，需要跳转时加 jump frame 索引（保存某时刻 active 数组状态 + 流 offset），用空间换延迟。评论区补充：每个 key 要额外 10 bit 存 joint index + 1 bit 区分 pos/rot。

## 关键要点

- **hot / cold 分离**：active 数组装当前正在用的曲线点，其他都是 cold 流；
- **按需要时间排序流**：而不是按 track 分组，天然变成顺序访问；
- **两次内存访问**：指针前进 + active 数组，其他都在 cache 里；
- **单流 + 可压缩 + 可 streaming** 是顺序访问的副产品；
- **jump frame** 是向流式数据结构里加随机访问的通用招数——快照 + offset；
- 每 key 附加 11 bit tag 才知道放回 active 数组的哪一格，这是"全局流"必须付的协议税。

## 链接到的概念

- [[animation-stream-cache-layout]]
- [[cache-friendliness]]
- [[aos-vs-soa]]
- [[data-driven-architecture]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/10/low-level-animation-part-2.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-10-23_low-level-animation-part-2.md`
