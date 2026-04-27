---
tags: [source, 渲染, derivative-map, 调试]
date: 2026-04-27
sources: 1
---

# Derivative Map Artifacts（Rory Driscoll / CodeItNow）

[[people/rory-driscoll]] 发表于 2012 年 1 月的简短勘误说明，澄清前一篇对比文章中出现的 artifact 来源。

## 摘要

前文（derivative maps vs normal maps）中报告的奇怪边缘 artifact 和竖向条纹，经过在 GPU Perf Studio 中深入调试，最终定位为**mipmap 生成代码 bug**——每个 mip 级别额外引入了一列垃圾数据。这个问题单独出现并不太显眼，但与 FXAA 和各向异性滤波叠加后被显著放大。文章结论：artifact 与 derivative map 技术本身无关，mipmap 生成正确后 derivative map 工作正常。建议 derivative map 使用常规三线性滤波而非各向异性滤波。

## 关键要点

- Artifact 根因：mipmap 生成 bug（每级多一列垃圾），与 DM 无关
- FXAA + 各向异性滤波会放大此类 mipmap 错误的视觉影响
- 建议：derivative map 使用三线性滤波

## 链接到的概念

- [[rendering/derivative-map]]
- [[rendering/mipmap-generation-sampling]]

## 原文

- 链接：https://www.rorydriscoll.com/2012/01/22/derivative-map-artifacts/
- 本地：`raw/articles/rorydriscoll.com/2012-01-22_derivative-map-artifacts.md`
