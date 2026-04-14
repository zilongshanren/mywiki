---
tags: [source, 渲染, pbr, brdf, siggraph]
date: 2026-04-14
sources: 1
---

# Physically Based Shading at SIGGRAPH 2014（Stephen Hill）

[[stephen-hill|Stephen Hill]] 2014 年 8 月写的一篇课程预告 / 导读，介绍当年 SIGGRAPH *Physically Based Shading (in Theory and Practice)* 课程的阵容。本文本身是一个元数据贴，但 2014 年这一届课程包含了 [[physically-based-shading|PBR]] 演进史上若干标志性报告，值得单独存档。

## 摘要

2014 年的课表：

- **Naty Hoffman** — Physics and Math of Shading（每年保留的入门节目）
- **Eric Heitz** — Understanding the Masking-Shadowing Function，summarise 其 JCGT 上 *Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs* 一文，对 Smith 模型相对于暴力模拟的精度做了严谨分析，是此后业界普遍用 Smith G 的决定性依据。
- **Jonathan Dupuy** — Antialiasing Physically Based Shading with LEADR Mapping，把 NDF 预滤波和 LEAN / LEADR 的实际工程问题捋清楚。
- **Yoshiharu Gotanda（tri-Ace）** — Designing Reflectance Models for New Consoles。
- **Sébastien Lagarde & Charles de Rousiers（DICE）** — Moving Frostbite to PBR，Frostbite 3 引擎把所有渲染管线切到 PBR 的完整实战笔记，成为此后多家工作室的参考蓝本。
- **Anders Langlands（Solid Angle）** — Physically Based Shader Design in Arnold / alShaders，把 VFX 侧离线渲染器的 PBR 实现带进来对照。
- **Ian Megibben & Farhez Rayani（Pixar）** — Art Direction within Pixar's Physically Based Lighting System，用 Toy Story *OF TERROR!* 讲 PBR 给灯光艺术带来的变化。

另外一个亮点：**Brent Burley 更新了 2012 年 Disney Principled BRDF 的 course notes**，根据 Heitz 的新发现调整了「Smith G」的 roughness 重映射，并补充了 Disney BRDF Explorer 里的实现细节。

## 关键要点

- **2014 是 PBR 统一的关键节点**：Heitz 给 Smith 理论铺底、Lagarde 给游戏业界落地模板、Burley 更新 Disney Principled BRDF、Langlands 把 VFX 接入同一套话语。
- **课程笔记是公开的**：blog.selfshadow.com/publications 上按年份归档，至今仍是最高质量的 PBR 中文外入门资料集合。
- **Frostbite to PBR 笔记**极其详细，涵盖光单位、HDR 与 exposure、IBL split-sum、cloth、眼睛、水面——很多后续游戏引擎的 PBR 实现直接照抄其配方。

## 链接到的概念

- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[stephen-hill]]

## 原文

- 链接：https://blog.selfshadow.com/2014/08/12/physically-based-shading-at-siggraph-2014/
- 课程主页：https://blog.selfshadow.com/publications/s2014-shading-course
- 本地：`raw/articles/blog.selfshadow.com/2014-08-12_physically-based-shading-at-siggraph-2014.md`
