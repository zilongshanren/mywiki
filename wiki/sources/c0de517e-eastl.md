---
tags: [source, c++, containers, stl, ea, 工业实践]
date: 2026-04-19
sources: 1
---

# EASTL（C0DE517E / Angelo Pesce 2010-10-20）

[[angelo-pesce]] 2010 年 10 月的一条短帖，只有三句话：EA 把自家的 STL（**EASTL**）开放了，贴了仓库与文档链接，其余不做展开。

## 摘要

这篇本身没有技术论述，但指向一件当时对 C++ 游戏引擎圈影响深远的事：2007 年 Paul Pedriana 的 EASTL 白皮书和 2010 年前后 EA 陆续开源的容器实现，把「游戏工作室为什么不能直接用标准 STL」这件事摆到了台面上——分配器设计不够显式、调试性差、不同编译器实现差异巨大、`std::vector::resize` 会默认构造而不是按游戏常见场景 reserve-without-init、`std::deque` 过度复杂等等。EASTL 的应对是：**保持和 STL 非常接近的接口，但在容器类型里显式带上分配器参数、提供 reset / reserve-without-init / fixed_* 容器、并同时维护可读性良好的调试实现**。这是「工作室自己写 STL」这一派工业实践的早期标杆，与更晚出现的 Orthodox C++、RDESTL、folly、absl 乃至 [[rpp-stl-replacement|Max Slater 的 rpp]] 一脉相承。

Pesce 本人当时忙于自己的游戏（后文揭晓是 *Fight Night Champion*），只留下了这条书签式的推荐。

## 关键要点

- EA 在 2010 年前后正式把 EASTL 实现放出来，不再只是一篇内部白皮书
- EASTL 的主要设计动机：**分配器显式**、**调试 build 可跑**、**对跨平台 ABI/实现差异更可控**
- 游戏业「自己写 STL」的传统可以回溯到这里，后续 [[rpp-stl-replacement|rpp]] 等项目的出发点几乎一致
- Pesce 选择把这条消息当新闻转发，而不是自己展开——但这个转发本身反映了圈内对 EASTL 的关注度

## 链接到的概念

- [[rpp-stl-replacement]] —— 2020s 个人项目版的「写自己的 STL」
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/10/eastl.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-10-20_eastl.md`
