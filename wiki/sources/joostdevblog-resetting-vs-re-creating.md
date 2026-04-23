---
tags: [source, software-design, 对象生命周期, c++, 状态管理]
date: 2026-04-19
sources: 1
---

# Resetting versus re-creating（Joost van Dongen，2011-01-30）

[[joost-van-dongen]] 2011 年 1 月的工程随笔。作为 Ronimo 早期唯一程序员，他的代码风格无人 review；近期扩招之后新同事 Maarten 给他上了一课。

## 摘要

Ronimo 的「秘密新项目」（后来是 Awesomenauts）里角色死亡后要 respawn，Joost 最初的做法是**隐藏 + 重置**：死时把血条/阴影/本体/特效全部隐藏，重生时把连击数/冷却/中毒时长逐一清零。这套方案的致命问题是每加一条新状态就要同步改「隐藏」「重置」两张清单，漏了「没重置」的 bug 尤其难发现——很多效果会在重生前自然超时。Maarten 的反直觉解法：**死时直接 delete，重生时重新 new**；所有状态由构造函数统一定义，不存在两张清单不同步的问题。Joost 又把这个原则套回 Swords & Soldiers 的菜单系统（原来所有菜单启动时一次创建后 hide），觉得菜单也应该直接 delete 掉不用的。评论区围绕性能和适用范围展开：XNA / Windows Phone 7 的 compact .NET 没有 placement new 且 GC 会 mini-lag，必须用对象池；C++ 可以用 placement new；另一派认为**保留 reset 但强制「唯一初始化路径」**也能达到目的。Joost 拒绝「这就是 RAII」的说法——他的角色在任何时刻都是合法态，只是状态维度太多手维护不过来。

## 关键要点

- 隐藏 + 重置 = 两张必须手动同步的字段清单，**编译器不帮你查**。
- 销毁重建 = 只有一条初始化路径（构造函数），字段漏掉就是类型错误。
- 性能不是阻碍：placement new / 小分配器 / 对象池都能把「重建」开销打平。
- 粒子系统例外——**低频对象销毁重建，高频对象必须池化**。
- 这条原则是 Ronimo 编码纪律「用结构本身杜绝一类 bug」的具体案例。

## 链接到的概念

- [[destroy-recreate-vs-reset]]
- [[minimize-points-and-types-of-failure]]
- [[data-structure-invariants]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/01/resetting-versus-re-creating.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-01-30_resetting-versus-re-creating.md`
