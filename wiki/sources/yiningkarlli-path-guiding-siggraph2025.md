---
tags: [source, 渲染, 路径追踪, path-guiding, openpgl, hyperion]
date: 2026-04-19
sources: 1
---

# SIGGRAPH 2025 Course — Path Guiding Surfaces and Volumes in Disney's Hyperion Renderer（Yining Karl Li / Code & Visuals）

[[yining-karl-li]] 2025 年 8 月发表的博客，配套 SIGGRAPH 2025 course *Path Guiding in Production and Recent Advancements*（由 Intel 的 Sebastian Herholz 组织）中 Disney Animation/DisneyResearch|Studios 的 36 页章节（全课共 80 页）。

## 摘要

Hyperion 是最早实装 Practical Path Guiding（Müller et al. 2017）的生产渲染器之一，一代系统从 *Frozen 2* 起有限部署；但多个原因（只支持表面、交互不透明、收益不稳定）使它一直没大规模上线。基于 Wayne Huang 的研究提案，Disney Research Studios、Disney Animation、Pixar、ILM 和 Intel 的 Sebastian Herholz 启动了二代项目：在 Intel 的 OpenPGL 之上做同时指导表面和体积的 guiding，专门应对 Moana 2 风暴、Zootopia 2 体积这类每个镜头都有体积的新常态。项目本身既产出了三篇论文（Dodik 2022 spatio-directional mixture、Xu 2024 volume scattering probability guiding、Rath 2025 神经 path guiding 嵌入 CPU 渲染器），也在 Hyperion 和 RenderMan XPU 里完成了艰难的工程化，并在 *Zootopia 2* 上迎来首次大规模部署。

## 关键要点

- 二代 path guiding 的两大产线技术难点：
  1. 在 [[wavefront-path-tracing]] 架构里保留足够路径历史来训练 guiding（Hyperion、RenderMan XPU 都是 wavefront）。
  2. 与大量「违反物理」的艺术指导开关（per-light AOV、可见性 override、lightpath 改写）共存。
- 团队为正确性验证与产线诊断专门写了可视化工具，这类工程细节在研究论文里一般不会涉及。
- 研究 × 产线共同推进的组织模式：Disney Research Studios 把 Hyperion 当作自己最主要的研究渲染器之一，研究员直接在同一个 codebase 上写代码；课程认为这种「双边协作」是大公司养 R&D 的真正价值点。
- 作者说课程里呈现的是「年初的快照」，项目仍在推进，2026 年还会有更多内容。

## 链接到的概念

- [[path-guiding-production]]
- [[wavefront-path-tracing]]
- [[hyperion-renderer]]

## 原文

- 链接：https://blog.yiningkarlli.com/2025/08/path-guiding-in-production.html
- 本地：`raw/articles/blog.yiningkarlli.com/2025-08-12_siggraph-2025-course-notes-path-guiding-surfaces-and-volumes.md`
