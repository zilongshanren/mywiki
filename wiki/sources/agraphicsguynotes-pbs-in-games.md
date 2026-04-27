---
tags: [source, 渲染, pbr, brdf, 微表面, 菲涅耳]
date: 2026-04-27
sources: 1
---

# Physically Based Shading in Games（A Graphics Guy's Note）

[[people/graphics-guy-notes|Jiayin Cao]] 发表于 2015 年 12 月的入门向文章，从旧式 Phong 模型出发，系统梳理 PBS 在游戏中的核心收益与关键属性。

## 摘要

文章先指出 Phong 模型的两个硬伤：镜面项不归一化（高光变窄时亮度不增强，违背能量守恒），以及 diffuse + specular 直接相加而非正确混合。随后介绍 [[microfacet-brdf|微表面 BRDF]] 如何用单一 roughness 参数同时控制高光形状与强度，使能量守恒自然成立。扩散-镜面混合部分说明 UE4 的 Metallic 参数如何通过 lerp 保证 `m_d + m_s ≤ 1`。菲涅耳效应一节用 Schlick 近似 `R = R₀ + (1−R₀)(1−cosθ)⁵` 解释为何掠射角反射必然趋向 1，以及为何边缘高光是物理正确的。文末汇总了 SIGGRAPH 2010–2015 的 PBS 课程链接。

## 关键要点

- Phong 的两大问题：高光不归一化、diffuse/specular 直接叠加；两者都会违反能量守恒。
- 微表面模型的 roughness 唯一参数让艺术家几乎不可能破坏能量守恒。
- UE4 即便 Metallic=0 也保留 8% 镜面反射；专门的 Specular 参数用于消除这 8%。
- Schlick 近似足够游戏实时使用，精度已充分。
- 离线与实时的理论基础相同，区别仅在采样策略与性能约束。

## 链接到的概念

- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[rendering/split-sum-approximation]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/physically_based_shading_in_games/
- 本地：`raw/articles/agraphicsguynotes.com/2015-12-05_physically-based-shading-in-games.md`
