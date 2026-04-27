---
tags: [source, rendering, culling, visibility]
date: 2026-04-27
sources: 1
---

# Portals are misunderstood（Angelo Pesce / c0de517e）

[[angelo-pesce]] 发表于 2013 年 2 月的文章，论述 Portal/Cell 可见性系统的本质及其被误解的来源。

## 摘要

文章首先梳理了 Portal 技术从 Doom BSP 到 Quake PVS，再到 Doom 3 运行时裁剪的历史演进，然后提出核心重构：Portal 本质上是**谓词化渲染**——"若此传送门可见，则渲染关联内容"。这一解读将 Portal 从 CSG 关卡编辑工作流中解耦，支持动态 Portal（如车窗）、非严格开口（保守 Portal）和 GPU 驱动实现。文章还分析了 Antiportal（遮挡体）与 Portal 的对偶关系，指出两者可以在同一套光栅化遮挡系统中协同工作：先光栅化 Portal 测试可见性，若可见再递归处理关联 Cell。

## 关键要点

- Portal 不需要依附 CSG/BSP 关卡编辑器，可应用于任意网格场景
- Cell 的最小定义：一组"只要至少一个关联 Portal 可见就需要渲染"的对象集合
- Antiportal 与 Portal 是对偶的：一个描述"可进入"，一个描述"被遮挡"
- 光栅化遮挡系统中，Portal 测试几乎零额外开销

## 链接到的概念

- [[portals-cells-predicated-rendering]]
- [[occlusion-culling]]
- [[gpu-based-occlusion-culling]]
- [[culling]]

## 原文

- 链接：https://c0de517e.com/011_portals.htm
- 本地：`raw/articles/c0de517e.com/2013-02-17_portals-are-misunderstood-portals-cells-predicated-rendering.md`
