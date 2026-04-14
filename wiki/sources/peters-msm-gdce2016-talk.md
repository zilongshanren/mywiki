---
tags: [source, 渲染, 阴影, 矩, talk]
date: 2026-04-14
sources: 1
---

# Rendering Antialiased Shadows with Moment Shadow Mapping（Peters，GDCE 2016）

[[christoph-peters]] 在 Game Developers Conference Europe 2016 上的一小时讲座，针对游戏图形程序员介绍 [[moment-shadow-mapping|MSM]] 在实战中的适用边界、实现要点与应用。

## 摘要

shadow map 走样是游戏里常见的瑕疵。MSM 像 EVSM 一样可以**直接滤波**，但漏光更小、稳健性更好、代价相当——而且对高分辨率（4K、VR）扩展性极佳。讲座覆盖三个层次：何时该用 MSM；它是怎么工作的；如何把它落地。在此之上，还演示了如何用同一套数学机制做 contact-hardening soft shadows 与 god rays（crepuscular rays）。

讲座视频、PowerPoint、PDF（带演讲者 notes）以及 [[sources/peters-msm-jcgt2016-demo|带文档的 HLSL demo]] 都开放下载。

## 关键要点

- **目标听众**：游戏图形程序员，假设熟悉基础 [[shadow-mapping-basics|shadow mapping]]，但会在开头做一遍回顾。
- **MSM 优势的卖点**：和 EVSM 同一档 cost、更低漏光、更好稳健性、对 4K / VR 扩展性更佳。
- **应用面**：硬阴影 + soft shadows + 半透明遮挡物 + 体积阴影（参与介质）四类问题共享同一个 pipeline。
- **配套**：现场提到带文档的 demo，对应 2016-09 那篇 [[sources/peters-msm-jcgt2016-demo]] 博客发布的版本。
- **题材定位**：是一篇「学术成果落到引擎程序员手里」的桥梁性讲座，没有引入新方法，但是 MSM 故事中重要的传播节点。

## 链接到的概念

- [[moment-shadow-mapping]]
- [[shadow-mapping-basics]]
- [[christoph-peters]]

## 原文

- 链接：<http://momentsingraphics.de/GDCEurope2016.html>
- 视频：<https://gdcvault.com/play/1023864/Rendering-Antialiased-Shadows-with-Moment>
- 本地：`raw/articles/momentsingraphics.de/2016-01-01_rendering-antialiased-shadows-with-moment-shadow-mapping.md`
