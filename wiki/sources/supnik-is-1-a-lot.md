---
tags: [source, 性能优化, profiler, X-Plane]
date: 2026-04-19
sources: 1
---

# Is 1% A Lot?（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 11 月的随笔，回答一个业余开发者常问的问题：优化一段代码 1% 的改善值得花多少时间？

## 摘要

Supnik 的答案可以浓缩成一个乘法：**实际收益 = 局部改善 × 这段代码的杠杆率（它在总时间里的占比）**。一段占帧时间 5% 的代码，即使砍掉 20%，全局只省 1%；一段占 30% 的热点，1% 的改善也能立刻反映在 FPS 上。他用 X-Plane 9.62 的 Shark profile 做示范：`glDrawElements` 占 35.6%（高杠杆，值得追），quad-tree 遍历占 12.9%（同时出现在 L2 miss 榜上，方向是改数据布局），`glBegin` 只占 2%（低杠杆，虽然有很多代码可改，但不值得停下新功能去做）。中间还藏着一条副产品：profile 顺便是 bug 探测器——X-Plane 里有个「mesh 维护」例程跳到第三名（7.6%），Supnik 当场判断这是非预期的调用路径，是 bug 不是性能问题。最后加一个尾注：**低杠杆的 1% 如果能被复用到几十处，累积也能变高杠杆**——所以「一次能改 1%」+「改完可套用十次」是值得追的。

## 关键要点

- 杠杆率（leverage ratio）= 这段代码在总时间里的占比；优化收益必须乘上它。
- Adaptive sampling profiler（Shark / 类似工具）= 按杠杆率给你代码排序。
- Timed Profile 必须带 blocking（All Thread States），否则会漏掉 `glMapBufferARB` 等等待点。
- Time 与 L2 miss profile 同时看：两榜重叠时热点是内存访问受限。
- Profile 榜单上的意外项往往是 bug——比 1% 优化更值得挖。
- 低杠杆可以用「可复用的优化技巧」累积成高杠杆。

## 链接到的概念

- [[optimization-leverage-ratio]]
- [[amdahls-law]]
- [[bottleneck-analysis]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/11/is-1-lot.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-11-30_is-1-a-lot.md`
