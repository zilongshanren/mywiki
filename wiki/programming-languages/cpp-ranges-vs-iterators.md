---
tags: [cpp, stl, ranges, iterators, abstraction]
date: 2026-04-19
sources: 1
---

# C++ Ranges vs. Iterators：自包含终止的「sequence」抽象

[[ben-supnik]] 2011 年 9 月在 X-Plane 里自己造了一个被他称作「sequence」的 C++ 抽象，后来被评论区指出：这就是 Andrei Alexandrescu 在《Iterators Must Go》里讲的 **range**——也是后来 C++20 `std::ranges` 的概念原型。

## 核心区别

STL 的 forward iterator 模型需要**两个游标**（begin、end）配对使用——完全抄自 C 指针对的写法。问题是**适配器**：想把一个迭代器包装成「跳过偶数」的新迭代器，你必须同时持有 `now` 和 `end` 两个位置；而组合三层 filter 后，end 只是一个占位符，因为上层 filter 自己知道什么时候终止。

range（Supnik 的 sequence）把终止条件内置：一个对象同时回答「当前值是什么」和「是否结束」。接口只有三条：

```cpp
while (my_seq()) {            // bool operator() —— 还有值吗？
    do_stuff_to(*my_seq);     // dereference 拿当前值
    ++my_seq;                 // 前进
}
```

这相当于 C 字符串「看到 `\0` 就停」的抽象——不需要外部的 end 指针。和 Python 的 iterator 协议（`__next__` + `StopIteration`）思路一致，但用 **look-before-you-leap** 而非异常来表达终止，更符合 C++ 的错误处理惯例。

## 为什么在 X-Plane 里是生产力工程

Supnik 用 range 重写了航路（victor airway）和导航数据库查询。亮点不是单一 range 比 iterator 快，而是**适配器链式组合**：

- 过滤一段航路中不匹配类型的航段
- 把相邻点变成中点序列
- 只保留锐角拐点
- 把多个 range 并联（concat）

这些组合在迭代器世界要写三到五个包装类 + 配对 end，在 range 世界就是几行 template。参见 [[rpp-stl-replacement]] 关于游戏工程里 STL 替代品的路线。

## 历史脉络

- 2011 Alexandrescu 《Iterators Must Go》 boostcon 演讲（Supnik 看的版本）
- 2014+ Eric Niebler 的 range-v3 实现
- C++20 正式并入 `std::ranges`

也因此 Supnik 这篇文章是一个有趣的时代切片——独立工程师凭第一性原理**重新发明了语言标准委员会要走十年才落地的东西**。对照 [[stl-not-abstraction-prescription]]、[[more-stl-abstraction-in-x-plane]] 看，可以理解他为何对 STL 的迭代器抽象始终保持怀疑。

## Sources

- [[sources/supnik-sequences-vs-iterators]]
