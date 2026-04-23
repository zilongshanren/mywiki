---
tags: [人物, 作者, 图形程序员]
date: 2026-04-14
sources: 5
---

# Angelo Pesce

**Angelo Pesce**（博客笔名 **C0DE517E**）是意大利籍图形程序员，长期在 3A 游戏工作室做实时渲染与 GPU 性能优化。职业轨迹包含 Milestone、EA Black Box、Relic、Capcom Vancouver、Activision 等，近年在 Roblox 负责渲染。博客 [c0de517e.blogspot.com](http://c0de517e.blogspot.com/) 自 2008 年起持续输出，内容偏「思考笔记」风格：半成品想法、对硬件与架构的怀疑、对工作室流程的吐槽，偶尔夹带一些怀旧技术考古。

他的写作风格典型特征：不怕公开提出自己都还没验证完的猜想，喜欢把当下工业实践与「如果换一种方式会怎样」对照着写，文风口语化、题图多用手机随手拍照加 Instagram 滤镜。

## 主要贡献 / 相关作品

- **Cached Cascaded Shadowmaps**：2011 年在博客随手抛出的一个「bad idea sketch」，提议把远距离的 cascaded shadowmap 分帧缓存，只重绘动态投射者。这个想法后被 Mike Day（Insomniac Games）在 SIGGRAPH 2012 的《Shadow Map Silhouette Revectorization / CSM Scrolling》工作中以更完整的形式实现并公开——Pesce 随后写了一篇 service update 指向 Mike Day 的 paper（见 [[cached-shadowmaps]]）。
- **Tiled 硬件的软件视角**：2017 年的 *Tiled hardware (speculations)* 讨论了 [[tbdr-vs-imr|TBDR 与 IMR]] 的功耗 / 面积 / 带宽权衡，并邀请 [[fabian-giesen]] 在评论区给出更权威的硬件侧修正，形成了一个经典的「软件工程师假设 + 硬件工程师打脸」对谈。
- 常年在博客上分享对 render graph、streaming、material system、debug 可视化的思考；不少早期内容是后来主流技术的前兆。

## 相关
- [[cached-shadowmaps]]
- [[tbdr-vs-imr]]
- [[fabian-giesen]]
- [[hsr-tbdr]]
- [[experience-as-noise-filter]]
- [[scene-graph-unnecessary-in-engine]]
- [[pesce-2010-engine-layer-sketch]]
- [[live-editing-taxonomy-2010]]
- [[linear-z-trick]]
- [[frame-pipeline-latency]]
- [[code-as-art-manifesto]]
- [[platform-specific-features-poll-2010]]
- [[stereo-reprojection-hole-fill]] —— 2010 立体渲染的单眼 reproject + 洞补实验
- [[iterative-sample-point-relaxation]] —— 带 importance 权重的半球 Poisson-like 采样点生成器
- [[code-tourism-practice]] —— 2011 把读代码类比为画家逛画廊

## Sources
- [[sources/c0de517e-cached-shadowmaps]]
- [[sources/c0de517e-tiled-hardware-speculations]]
- [[sources/c0de517e-pitfalls-of-experience]]
- [[sources/c0de517e-skin]]
- [[sources/c0de517e-collaborative-engine-design]]
- [[sources/c0de517e-homework-2-dependencies]]
- [[sources/c0de517e-pix-is-great-but]]
- [[sources/c0de517e-live-editing-poll-results]]
- [[sources/c0de517e-threads-buffers-and-latency]]
- [[sources/c0de517e-know-your-z]]
- [[sources/c0de517e-code-rights]]
- [[sources/c0de517e-platform-specific-features-poll-2010]]
- [[sources/c0de517e-eastl]]
- [[sources/c0de517e-stereoscopic-test]]
- [[sources/c0de517e-sample-generator-3d]]
- [[sources/c0de517e-next-next-gen-poll-2011]]
- [[sources/c0de517e-code-tourism]]
- [[sources/c0de517e-survive-cpp-guidelines-experiment]]
