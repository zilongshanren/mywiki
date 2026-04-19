---
tags: [source, 渲染, 路径追踪, hyperion, disney-animation, 嵌套介质]
date: 2026-04-19
sources: 1
---

# Zootopia 2（Yining Karl Li / Code & Visuals）

[[yining-karl-li]] 2025 年 12 月发表的《Zootopia 2》回顾文章。这是 Disney Animation 第 64 部长片；作者把它当作衡量团队能力在原作 Zootopia（2016）之后走了多远的标尺。

## 摘要

Zootopia 2 的技术主题和一代一样是「细节 + 规模」——现代城市视觉密度大，角色从小到鼩鼱大到长颈鹿都要自洽，几乎每个镜头都有 FX 和大量毛发角色。作者举了一个例子：艺术家把雪做成 zillions 个单独冰晶，这是 Disney Research 2016 年的理论研究想法，十年后被艺术家直接 brute-force 做了出来，无需任何专门优化。作者在片上亲自做了两类他最喜欢的项目：1）水管序列——把 Moana 2 的水渲染系统扩展成生产版嵌套介质，处理「角色 → 水 → 双面玻璃 → 城市/森林环境」的 4 层嵌套；2）与 Disney Research Studios 合作把基于 OpenPGL 的二代 path guiding 首次大规模铺到影片上（约 12% 镜头），此前仅在 Moana 2 做原型。另外 Chiang 毛发 shader 维持原样，但团队在 ray-curve 相交精度上做了大量艺术家迭代，避免多次散射下小误差被多 bounce 放大到续集维护不了原角色的毛发外观。

## 关键要点

- 嵌套介质（[[nested-dielectrics]]）算法本身是 Schmidt & Budge 2002 的老题目，玩具渲染器里几十行就行；作者 2019 年在个人 hobby renderer 里就写过。真正难的是让它与生产渲染器的一堆高级功能共存、在 wavefront 架构下稳定、在产线规模下鲁棒。
- 续集的「技术 tactics」新玩法：Harmony Li（作者之妻，Zootopia 2 Associate Technical Supervisor 之一）主导把渲染团队前移到 asset building 环节——每一个角色在模型/look dev 时就接受渲染性能审查，以应对「一屏数千角色」的人群规模。
- Zootopia 2 在工作流层面又换了一次 DCC：动画从 Maya 迁到 Presto，是 Disney Animation 长片首次；USD 管线足够灵活才允许这件事。
- 作者重申「in-house 渲染团队 + in-house 渲染器」的价值：重点不是 Hyperion 的某个独家 feature，而是渲染团队能贴近 artists 与 TD 做定制，从上到下自己掌控代码。

## 链接到的概念

- [[nested-dielectrics]]
- [[path-guiding-production]]
- [[hyperion-renderer]]
- [[wavefront-path-tracing]]

## 原文

- 链接：https://blog.yiningkarlli.com/2025/12/zootopia-2.html
- 本地：`raw/articles/blog.yiningkarlli.com/2025-12-17_zootopia-2.md`
