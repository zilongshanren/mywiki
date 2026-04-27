---
tags: [source, 渲染, pbr, brdf, siggraph, atmosphere, hair-rendering, ao]
date: 2026-04-27
sources: 1
---

# SIGGRAPH 2016 Course: Physically Based Shading in Theory and Practice（Stephen Hill）

[[stephen-hill|Stephen Hill]] 与 Stephen McAuley 联合组织的年度 PBS 课程 2016 届，地点为 Anaheim Convention Center。相较往届，本届课程将重心从基础 BRDF 理论扩展到大气渲染、HDRI 工作流、毛发着色、实时间接遮蔽和路径追踪收敛方向。

## 摘要

六组演讲各有侧重：Naty Hoffman 继续承担 PBS 最新进展综述（slides 公开）；Roger Cordes & Dan Lobl（Lucasfilm/ILM）展示 Star Wars: The Force Awakens 的统一着色与资产工作流；Sébastien Hillaire（Frostbite）分享**基于物理的天空、大气与云渲染**，是游戏引擎中大气散射工程落地的重要参考；Sébastien Lagarde（Unity）深入讲解**全景 HDRI 工作流**（slides + course notes + supplemental 全部公开）；Brian Karis（Epic Games）介绍 Unreal Engine 4 中**基于物理的毛发着色**；Jorge Jiménez（Activision Blizzard）展示**实时精确间接遮蔽**的实践策略；Christophe Hery & Ryusuke Villemin（Pixar）探讨 *Finding Dory* 的双向路径追踪进展。

## 关键要点

- **大气渲染工程化**：Hillaire 的 Frostbite 大气演讲将 Bruneton/Neyret 的预计算框架简化为可在游戏引擎中实时运行的体积散射，是 2016 年后大量引擎实现体积大气的直接参考。
- **HDRI 工作流标准化**：Lagarde 的 Unity 演讲包含完整的全景 HDRI 采集、校正、引擎集成流程，有 supplemental 工具代码。
- **UE4 PBR 毛发**：Brian Karis 的 Marschner 改进方案将毛发着色纳入 Unreal 的 [[physically-based-shading|PBR]] 管线，课程 slides 公开。
- **实时精确 AO**：Jiménez 的间接遮蔽演讲延续其 GTAO / HBAO+ 系列，讨论如何在游戏实时约束下最大化遮蔽精度。
- **路径追踪收敛方向**：Pixar 的双向路径追踪讨论标志着 PBS 课程开始将离线渲染的理论前沿（BDPT、MIS）纳入讨论范围，与实时渲染的混合 RT 走向形成呼应。
- **所有 slides 公开**：blog.selfshadow.com/publications/s2016-shading-course 下可以找到大部分演讲的 pptx + pdf + course notes。

## 链接到的概念

- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[stephen-hill]]

## 原文

- 链接：https://blog.selfshadow.com/publications/s2016-shading-course/
- 本地：`raw/articles/blog.selfshadow.com/2016-01-01_siggraph-2016-course-physically-based-shading-in-theory-and.md`
