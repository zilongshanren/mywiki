---
tags: [source, cpp, stl, ranges, iterators]
date: 2026-04-19
sources: 1
---

# Sequences Vs. Iterators（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 9 月 1 日的 C++ 设计随笔。他在 X-Plane 里写了一个叫「sequence」的概念：自带终止判断的游标，用来替代 STL 的 iterator 配对。评论区很快指出这就是 Andrei Alexandrescu 《Iterators Must Go》里讲的 **range**（后来并入 C++20 `std::ranges`）。

## 摘要

STL forward iterator 需要 `begin / end` 两个游标，本质是 C 指针对的抄袭。对**适配器**尤其别扭：给 filter_iterator 传底层 `now` 和 `end`，外层还得再拿一个 end 做对照，而 filter 自己就知道什么时候结束。Supnik 的 sequence（= range）用三个算子：`operator()` 返回 bool 是否还有值，`operator++` 前进，`operator*` 取当前值——相当于 C `\0`-terminated 字符串的抽象。好处是**适配器链式组合**：串三层 filter、并联两个序列都只改一层模板。他用 range 重写 X-Plane 的 victor airway 和 nav DB 访问，说这是巨大的生产力提升。评论补充这种思路和 Python iterator 协议一致，但用 look-before-you-leap 取代 StopIteration 异常，更 C++ 风格。

## 关键要点

- sequence = range：自包含终止条件的游标抽象
- 三算子接口：`bool operator()`, `++`, `*`
- iterator 配对对适配器不友好，range 天然可组合
- 相当于 C 字符串 `\0` 终止的抽象
- Alexandrescu《Iterators Must Go》预告了 C++20 `std::ranges`
- X-Plane 生产环境用 range 重写导航数据访问

## 链接到的概念

- [[cpp-ranges-vs-iterators]]
- [[stl-not-abstraction-prescription]]
- [[rpp-stl-replacement]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/09/sequences-vs-iterators.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-09-01_sequences-vs-iterators.md`
