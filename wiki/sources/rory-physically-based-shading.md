---
tags: [source, 渲染, pbr, brdf, 着色]
date: 2026-04-27
sources: 1
---

# Physically-Based Shading（Rory Driscoll / CodeItNow）

[[people/rory-driscoll]] 发表于 2013 年 11 月的思考文章，讨论「物理基础着色」一词的确切含义，并用 MERL BRDF 扫描数据对比 Lambert+Blinn-Phong 与 Disney Principled BRDF 的匹配质量。

## 摘要

文章从能量守恒切入：能量守恒的 Lambert+Blinn-Phong 是否算「物理基础」？Driscoll 认为业界通常指的是 BRDF 底层模型，例如 Torrance-Sparrow 微表面 BRDF。接下来他用 Disney 的 BRDF Explorer 加载 MERL 扫描材质（红色光泽塑料、哑光红色塑料、黄铜、钢铁），将 LBP 和 Disney BRDF 与扫描参考做对比。结论是：Disney BRDF 在 Fresnel 效果、掠射角高光形状、漫反射逆向反射等方面明显优于 LBP，但对黄铜的长尾高光仍不够好。文章最后指出：PBS 的最大价值不在于「更真实」，而在于**不同光照环境下材质表现一致、艺术家参数直观**——这是真正的工程收益。评论区对「physically-correct」vs「physically-based」的区分也很有价值。

## 关键要点

- 能量守恒的 LBP 不等于 PBS；PBS 的核心是底层 BRDF 模型的物理可信度
- MERL 数据提供真实材质扫描，用于客观评估 BRDF 拟合质量
- Disney BRDF 优于 LBP，但对金属长尾高光仍有差距
- PBS 的工程价值：跨光照一致性 + 直观的物理参数（albedo、roughness、F0）
- 「physically-correct」≠「physically-based」：正确性指渲染方程求解精度，基于性指 BRDF 的物理建模深度

## 链接到的概念

- [[rendering/physically-based-shading]]
- [[rendering/microfacet-brdf]]
- [[rendering/spectral-brdf]]

## 原文

- 链接：https://www.rorydriscoll.com/2013/11/22/physically-based-shading/
- 本地：`raw/articles/rorydriscoll.com/2013-11-22_physically-based-shading.md`
