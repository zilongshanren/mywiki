---
tags: [source, 游戏引擎, ecs, 粒子系统, c, cpp, cloudwu]
date: 2026-04-19
sources: 1
---

# ECS 粒子系统的 C/C++ 对比（云风的 BLOG）

[[cloudwu]] 发表于 2024 年 6 月的一篇短文，延续 2020 年的 [粒子系统的设计]，给出了用 C 写的 `psystem_manager.h` 实现，并反思用 C++ 重做同一套功能时的得失。

## 摘要

云风回顾了按属性聚合粒子数据的 [[ecs]] 做法：同一时间点通常只处理一种属性（递减生命期、施加重力、空间更新、渲染），因此按属性列连续存储比按对象聚合更友好——对 cache 友好、属性粒度不浪费对齐、支持自由属性装配、适合并行。粒子属性的自由组合需求让 OOP 多态或大量 if/else/switch 都很丑陋，ECS 天然避免了这种分支。但他用 C++ 重做了一遍同样的功能之后，陷入了自我怀疑：**强调类型安全无非是为了减少 bug 提高质量；但代码不那么浅显易懂却降低了质量**——这是对 [[type-safety-vs-simplicity|类型安全 vs 可读性]] 这条张力的直接命名。

## 关键要点

- 粒子系统按属性聚合 → cache 友好 + 天然适合并行
- 粒子属性自由组合是天然需求，ECS 消除了 OOP 多态 / switch case 的分支丛林
- [[aos-vs-soa|SoA]] 的实际好处在数据尺寸统一、即便单字节属性也不浪费
- C 实现朴素但所有细节摊开；C++ 实现在模板层加厚了认知负担
- 对粒子这种"逻辑朴素、改动频繁、性能敏感"的模块，他倾向 C 风格

## 链接到的概念

- [[ecs-particle-system-c]]
- [[type-safety-vs-simplicity]]
- [[ecs]]
- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[cpp-multi-paradigm-discipline]]

## 原文

- 链接：<https://blog.codingnow.com/cat2/ecs/> （2024-06-11）
- 本地：`raw/articles/blog.codingnow.com/2024-06-11_yun-feng-de-blog.md`
