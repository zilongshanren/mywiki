---
tags: [source, 渲染, 延迟渲染, deferred-lighting, g-buffer, 光照]
date: 2026-04-27
sources: 1
---

# Re-cap of Deferred Lighting（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel]] 于 2013 年 5 月在论坛回复中整理的延迟光照管线综述，后转载至博客。总结了他在 XBOX 360 / PS3 时代设计并落地于多款游戏的三阶段渲染器架构。

## 摘要

Engel 将他最喜欢的渲染器结构归纳为三个高层 stage：几何 → 光影数据 → 材质。从 Deferred Shading 向 Deferred Lighting 迁移的核心动机是在带宽受限的主机上削减 G-Buffer 体积——Deferred Lighting 只需要深度、法线和（可选的）高光信息来计算光照，不在光照 pass 中使用颜色缓冲。这使得同一个光影 buffer 可以被更多光源读写。材质阶段解耦的另一大优点是可以在屏幕空间以 PostFX 方式应用复杂材质（皮肤、头发、布料、车漆等），避免把材质计算压入光照 pass 造成重复开销。

## 关键要点

- Deferred Lighting（Light Prepass）= 三阶段：几何写 thin G-Buffer → 光照写 light/shadow buffer → 材质叠加
- G-Buffer 在 Deferred Lighting 中只需三个 RT：深度、颜色（仅几何阶段用）、法线 + 高光信息
- 光照/阴影 stage 只消费深度 + 法线这两个 RT，颜色 RT 此阶段不参与
- 带宽节省是从 PS3/XBOX 360 迁移的关键原因：读 G-Buffer for each light，体积小一个 RT 就能显著多塞几个光源
- 材质解耦允许在屏幕空间应用高代价材质模型，不和光照计算强耦合

## 链接到的概念

- [[rendering/deferred-lighting-vs-shading]]
- [[rendering/deferred-rendering]]
- [[rendering/tiled-light-prepass]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2013/05/re-cap-of-deferred-lighting.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2013-05-19_re-cap-of-deferred-lighting.md`
