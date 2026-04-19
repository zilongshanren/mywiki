---
tags: [source, procedural-generation, sampling, infinite-world]
date: 2026-04-19
sources: 1
---

# Infinite Random Rectangles – the Poisson Rect Process（Boris The Brave）

[[boris-the-brave]] 发表于 2026 年 1 月的文章，接续他关于「无限平面上均匀采点」的系列，给出一个在无限平面上生成**互不重叠随机矩形**、且与分块方式无关的算法。

## 摘要

关键观察：朴素的「逐个生成、跳过重叠」策略在无限域不适用，因为没有全局遍历顺序。作者把问题拆两相：Phase 1 按泊松点过程独立生成候选矩形，并给每个矩形打一个随机 sort order；Phase 2 对每个矩形查询它的重叠邻居，只保留 sort order 高于**所有**重叠邻居者。重叠对中必有一败，所以结果无重叠；同时判定规则只依赖局部邻域，Phase 2 的每个 chunk 只依赖固定数量的 Phase 1 chunk（依赖半径由最大矩形尺寸决定），因此算法天然可按 chunk 延迟求值。文末扩展到任意有界形状，并留下一个开放问题：如何让尺寸分布满足给定比例（例如 20% 2×2 + 80% 1×1）。

## 关键要点

- 两相分离（生成 + 局部最大过滤）是把「全局无重叠」这种全局约束降维成局部规则的通用套路。
- 可分块执行要求依赖半径有限——最大矩形尺寸给出了这个半径。
- 扩展到任意形状只需「有最大尺寸上界 + 能判重叠」两个条件。
- 想要更高密度靠「跑多遍再跨组互斥」，不能靠单纯提高起始点密度。

## 链接到的概念

- [[poisson-rect-process]]
- [[infinite-chunked-procedural-generation]]
- [[poisson-disk-sampling]]
- [[probabilistic-algorithms]]

## 原文

- 链接：https://www.boristhebrave.com/2026/01/22/infinite-random-rectangles-the-poisson-rect-process/
- 本地：`raw/articles/boristhebrave.com/2026-01-22_infinite-random-rectangles-the-poisson-rect-process.md`
