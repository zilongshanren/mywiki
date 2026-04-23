---
tags: [source, lighting, brdf, normal-mapping, ldraw]
date: 2026-04-19
sources: 1
---

# Lego Lighting Effects（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2013-03-16 的一篇罕见的**前瞻性设计稿**：BrickSmith（[[bricksmith-instancing-pipeline]]）新渲染管线要做真实感光照时，观察了一盒 Maersk 列车对窗举着，把具体视觉线索和对应渲染技术整理成 wish list。

## 摘要

对比一张 POV-Ray 级 lego render 和一张朴素 forward-shaded 截图，差异来自五组物理效应：(1) lego 塑料的非标准 BRDF——材质种类少，可以为每种 surface 存 lookup table 型的 BRDF 曲线；(2) 方砖侧面不是平的，角上微凸中间微凹，用 tangent-space normal map 就能重建；(3) 斜坡砖的磨砂 grit 需要**LEAN mapping**（把法线的二阶矩存进贴图）以保证 mipmap 下 specular 响应正确；(4) LDraw 边缘是线段——给线段赋"折角均值法线"参与 specular，复现倒角高光与 crack 处的自阴影；(5) 装砖的角度松紧噪声——对每个砖的 instance transform 叠小随机偏移，即可制造真实位姿抖动。间接光方面，玩家多在室内漫射环境下看 lego，所以 AO + 环境贴图 > 硬投影阴影——延伸方案是 deferred shading + screen-space reflectance/AO。核心前提：LDraw 没有 normal map / roughness，所有材质 metadata 要人工补；但 lego 材质种类少，在游戏里"太贵"的技术在这里完全吃得下。

## 关键要点

- BRDF 用 lookup table 纹理——适合材质种类少的场景
- 砖侧面不平是制造工艺特征（Supnik 赌是 TLC 故意的）
- LEAN mapping 解决 normal map mipmap 后粗糙度丢失的问题
- LDraw 线段不仅画 wireframe，还可以参与折角高光
- Per-instance transform 的微小随机偏移 = 装砖松紧噪声
- 室内漫射场景：AO + env map > cast shadow
- 数据源表达力（LDraw 没有材质 metadata）决定算法能走多远

## 链接到的概念

- [[lego-realistic-lighting-brain-dump]]
- [[bricksmith-instancing-pipeline]]
- [[tangent-space-normal-mapping]]
- [[microfacet-brdf]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2013/03/lego-lighting-effects.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-03-16_lego-lighting-effects.md`
