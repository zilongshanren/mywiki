---
tags: [source, 渲染, pbr, brdf, siggraph, disney-brdf]
date: 2026-04-19
sources: 1
---

# Physically Based Shading at SIGGRAPH 2012（Stephen Hill）

[[stephen-hill|Stephen Hill]] 和 Stephen McAuley 合办的 2012 年 SIGGRAPH 课程主页——这一届是 [[physically-based-shading|PBR]] 从「研究话题」跨入「游戏工业事实标准」的分水岭，很多后来被反复引用的基石论文首发于此。

## 摘要

2012 年的课表（上午 09:00 开始的半日课）：

- **Stephen Hill** — Introduction: The Importance of Physically Based Shading，开场强调为什么要把传统 ad hoc 模型换成物理模型。
- **Naty Hoffman** — Background: Physics and Math of Shading，之后每一届都保留的入门节目，从 Fresnel / microfacet / 能量守恒讲起，带 Mathematica notebook。
- **Stephen McAuley（Ubisoft）** — Calibrating Lighting and Materials in *Far Cry 3*，给出了游戏里如何用 chrome ball / gray ball 校准光照单位和材质 albedo 的完整流程，附带校准工具视频。
- **Yoshiharu Gotanda（tri-Ace）** — Beyond a Simple Physically Based Blinn-Phong Model in Real-Time，补全了能量守恒 Blinn-Phong 到 Oren-Nayar diffuse 的工业版修正。
- **Adam Martinez（Sony Pictures Imageworks）** — Physical Production Shaders with OSL，VFX 侧视角，讲 OSL 里的 physical shader 写法。
- **Brent Burley（Disney）** — **Physically Based Shading at Disney**。这是著名的 **Disney Principled BRDF** 论文，引入 roughness² 映射、基于艺术家直觉的单参数输入、`specular/specularTint/sheen/clearcoat` 等扩展——之后十余年游戏业界的 PBR 参数化事实上都在沿用这一套。
- **Brian Smits（Pixar）** — Reflection Model Design for *WALL-E* and *Up*，Pixar 自家离线反射模型的设计取舍。

## 关键要点

- **Disney Principled BRDF 首发**：Burley 把分散在多个模型里的参数统一成一组艺术家友好的输入，奠定了后续 UE4、Frostbite、Unity HDRP 的材质 UI 基础。
- **Far Cry 3 校准方法**：McAuley 公开了第一批「游戏实际怎么做 calibration」的可复用配方（chrome ball 标定、gray ball 曝光、HDR 探针），成了后续 Far Cry / Assassin's Creed 系列的内部标准。
- **2012 之后每年都有续集**：2013、2014、2015、2016、2017、2020、2025 都续开，成为 PBR 技术线最权威的年度论坛（见 [[stephen-hill]]）。
- 勘误记录里可以看到当时很多细节修正：Oren-Nayar 简化公式的修正（credit: James Canete）、Disney 课程 notes 里第 4 式的归一化因子修正（credit: Emmanuel Turquin）——说明这一届的数学严谨度已经被社区盯得很紧。

## 链接到的概念

- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[stephen-hill]]

## 原文

- 课程主页：https://blog.selfshadow.com/publications/s2012-shading-course/
- 本地：`raw/articles/blog.selfshadow.com/2026-01-01_siggraph-2012-course-practical-physically-based-shading-in-f.md`
