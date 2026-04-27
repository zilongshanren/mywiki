---
tags: [source, rendering, 渲染哲学, 质量观]
date: 2026-04-27
sources: 1
---

# Next-gen: Quality vs Quantity（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2012 年 8 月的文章，讨论实时渲染中「数量驱动」与「质量驱动」之间的根本取舍，并指出行业在这一问题上普遍失焦。

## 摘要

Pesce 以 Pixar 的《Luxo Jr.》为引，点出电影离线渲染与游戏实时渲染之间的质量差距数十年来始终存在。他援引 Johan Andersson（DICE）在 SIGGRAPH 2012 的演讲——将「影院级质量」列为实时渲染第一优先——来支撑自己的核心论点：游戏行业系统性地选择「加功能」而非「做精一个功能」，根因不是技术局限，而是团队文化与生产流程的取向。

功能可以排进排期、放进 trailer 字幕、作为卖点宣传；质量却是无形的感受，难以量化、难以 demo。这导致团队默认走数量路线，而不是把现有功能做到真正高质量。Pesce 用 Crysis 2 的 LOD 溶解效果举例：玩家不需要那块岩石，但如果做了又能让人看见「渲染技法的痕迹」，反而更差。优秀的渲染技术应当「被感受到而非被看见」。

他进一步论述：如果从零开始用前向渲染 + 大量烘焙，只把 stable CSM、方向光等少数特性做到极致，反而能占据最高的画质门槛。行业既缺乏技术对照实验（A/B 测试、生物特征测量），也缺乏对「什么真正重要」的理解，导致大量资源投入在看不见的地方。

## 关键要点

- 「加功能」在流程上永远比「做精功能」更容易被衡量和认可，这是结构性偏见
- 「大量技巧堆叠」的失败案例：过曝 bloom + 不稳定 vignette + 过度 lens flare，都是掩盖而非提升
- 实时渲染离解决还很远，即便是理论层面——「已解决」是误判
- 如果一个视觉效果做不好，不做比做了更好（Toy Story / Pixar 有意回避无法高质量呈现的内容）
- 行业真正缺乏的是「视觉品味」和「理解什么重要」，而非纯粹的技术能力
- HDR 帧缓冲若没有正确 tonemapping 毫无意义（与 gamma/degamma 普及的历史类比）

## 链接到的概念

- [[realtime-quality-vs-quantity]]
- [[deferred-rendering]]
- [[stable-csm-implementation-tips]]
- [[experience-as-noise-filter]]

## 原文

- 链接：https://c0de517e.blogspot.com/2012/08/next-gen-quality-vs-quantity.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-08-18_next-gen-quality-vs-quantity.md`
