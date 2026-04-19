---
tags: [source, 渲染, gpu-driven, 视频]
date: 2026-04-19
sources: 1
---

# GPU driven rendering in AnKi（Panagiotis Charitos / 视频 + slide）

[[people/panagiotis-charitos|Charitos]] 2024 年 11 月以视频形式做的一次 AnKi GPU-driven 管线综述。博客本体只是"去看视频 + Google Slides"的占位。

## 摘要

作者明确说"这次换成视频讲了，因为内容太多"，博客正文一句话带过，附一个 Google Slides 链接和嵌入视频。因此本地 markdown 并没有可供抽取的技术细节。作为索引项仍然保留此页，便于以后回看视频后回填要点。主题覆盖（根据标题和 AnKi 既有架构推断）：multidraw indirect / hi-z occlusion / bindless / mesh shader cluster culling / TLAS 驱动的动态 RT。这些话题 AnKi 博客 2023 年的 "GPU driven rendering in AnKi: a high-level overview" 有文字版，可作为补充阅读。

## 关键要点

- **本文是视频首发，博客只是门户**；要深入需看 Google Slides。
- 链接：Google Slides `1tsGjwZmP2mZBNyURNN4-XYsgJxfsG6omaC3w5ZQXzr4`。
- **数据缺口**：尚未观看视频，AnKi 2024 的 GPU-driven 细节（相对 2023 版的新变化）待补。
- 相关既有 wiki 概念：[[multidraw-indirect-occlusion-culling]], [[meshlets-and-mesh-shaders]], [[visibility-buffer]], [[bindless-rendering]]。

## 链接到的概念

- [[multidraw-indirect-occlusion-culling]]
- [[meshlets-and-mesh-shaders]]
- [[bindless-rendering]]
- [[visibility-buffer]]

## 原文

- 链接：https://anki3d.org/gpu-driven-rendering-in-anki/
- 本地：`raw/articles/anki3d.org/2024-11-21_gpu-driven-rendering-in-anki.md`
