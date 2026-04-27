---
tags: [source, 渲染, 光照, pbr, 全局光照, 光照设计, 实时GI]
date: 2026-04-27
sources: 1
---

# Lighting a Game / Observational vs Physical Lighting（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel]] 于 2013 年 6 月发表的短文，讨论现代游戏光照实践中「大量光源 + 每光源可选反弹 GI」的工作流，并提出一个反直觉的优先级观点：光源数量带来的视觉提升远大于从观测型到物理型着色模型的切换。

## 摘要

Engel 描述了一种类 CG 电影的游戏场景光照工作流：艺术家放置大量实时光源（场景内百个量级），每个光源独立开关阴影和反弹 GI。光影部分在次世代主机上已有先例（XBOX 360/PS3 时代），新一代主机的增量是「每光源反弹光照」。他的核心论点是：对于画面质量的提升，大量光源的优先级高于 PBR 的引入。一个阴影遮蔽的场景无论物理着色多精准，不如多布几盏灯再配上非物理着色模型好看。这和 PBR 的通常叙事（先上物理正确）构成对立，但他认为「more than real」的视觉效果才是照明艺术家真正想要的工具。

## 关键要点

- 游戏光照工作流正向 CG 电影靠拢：百个量级的实时灯，每灯独立控制阴影和 GI
- 反弹光照（bounce lighting / realtime GI per light）是次世代增量，艺术家新增了 per-light GI 开关
- 核心命题：「数量 > 质量」——从少灯到多灯的收益大于从观测型到物理型着色的收益
- 物理着色的正确性在照明条件单薄时几乎不可见，多灯才能体现材质差异
- 这个判断依赖场景类型：高空飞行类游戏（Blackfoot Blade）只需少量灯，地面开放世界才能充分利用多灯优势

## 链接到的概念

- [[rendering/physically-based-shading]]
- [[rendering/realtime-gi-per-light]]
- [[rendering/deferred-rendering]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2013/06/lighting-game-lighting-artists.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2013-06-24_lighting-a-game-lighting-artists-physically-observational-li.md`
