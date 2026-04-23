---
tags: [source, graphics, 反走样, deferred-rendering, 综述]
date: 2026-04-19
sources: 1
---

# So Many AA Techniques, So Little Time（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 4 月的一篇抗锯齿综述，把当时能用的 AA 方案按「决定权在哪一层获得」分成五档——Universal / Hardware FSAA / 2D / Post-process / Deferred-only。写在 MLAA/FXAA 刚铺开、[[subpixel-reconstruction-antialiasing|SRAA]] 论文刚发、TAA 还没成主流的窗口期，反映了工程师选型时实际的决策轴。

## 摘要

Supnik 把 AA 走样的来源明确到两类「per-pixel 二元决策」：(1) 像素在不在三角形里、(2) alpha test 过不过。然后给出分类法：SSAA 最贵但最稳，MSAA 是硬件快路但不救 shader 内部走样、也不适合 deferred；CSAA 是 NV 的 MSAA 增强；2D 用 Texture AA 最干净但挡 Z buffer；MLAA/FXAA 放 post-process，代价是色图盲猜边缘（他承认分不清两者细节）；TAA 用历史帧当第二套样本；SRAA 和 edge-blur 是 deferred 专用、吃 G-Buffer。博文还记录 ATI 把 MLAA 做成驱动全局开关这件事——驱动厂商要把 deferred 时代的 GPU 销售点找回来。

## 关键要点

- AA 分类不是学术正交，而是工程「你得先问自己什么」的路径分叉
- MSAA 在延迟渲染下失灵：光照在 resolve 后做
- Texture AA（带 1px 透明边的 alpha-blend 纹理）在 2D UI 最划算，但不能和 Z buffer 共存
- 驱动层强制 MLAA 会误模糊 2D UI —— 应用层失控
- TAA 的「时间换样本」被归入 post-process，显示它当时还没被看成独立类别

## 链接到的概念

- [[aa-techniques-survey-2011]]
- [[aliasing]]
- [[msaa-ssaa]]
- [[subpixel-reconstruction-antialiasing]]
- [[analytical-antialiasing]]
- [[temporal-antialiasing]]
- [[deferred-rendering]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/04/so-many-aa-techniques-so-little-time.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-04-22_so-many-aa-techniques-so-little-time.md`
