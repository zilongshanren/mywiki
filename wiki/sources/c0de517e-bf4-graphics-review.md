---
tags: [source, graphics, rendering, frostbite, deferred-rendering, pbr, analysis]
date: 2026-04-27
sources: 1
---

# Battlefield 4 Review (graphics)（c0de517e / Angelo Pesce）

[[angelo-pesce]] 发表于 2013 年 11 月的文章，以渲染工程师视角对 BF4 的技术实现做非正式评析。

## 摘要

Pesce 在几小时的单人战役流程中观察 BF4（PC 超高画质）的渲染技术，分类记录了三个主要"缺陷"和若干亮点。三个缺陷是：镜头光晕滥用（效果本身工艺好但到处都是）；高光过强且有大量 specular aliasing；角色脸部着色缺少高光细节。亮点方面则肯定了纹理质量、几何密度、粒子/破坏系统、LOD 的自然过渡，以及 SSAO 参数调校的克制（避免了 Far Cry 3 的描边感）。在光照分析上，他反复强调 occlusion 是可信光照的根本，无 occlusion 的 specular/cubemap 会造成严重失真，并建议宁可不做某个效果也不要让没遮蔽的高光留在画面里。他还观察到 BF4 的 DOF 使用了 compute + append buffer 生成 sprite 列表，以及 thin-wire AA 的可能存在。

## 关键要点

- **occlusion 第一原则**：没有遮蔽项的光照或 specular 宁缺毋滥；planar reflection 不加 blur/occlusion 就不该出现
- Frostbite 使用 cubemap + proxy 几何体/reflection cards 增强反射，疑有 screenspace 反射补充
- SSAO 用大半径 + 不随机化取样（"stadium lights"效果），对角色脚边的 artifacts 控制得好
- 皮肤着色看似 screenspace SSS filter，pre-integrated SSS 也有可能；缺少 specular 使质感大打折扣
- DOF sprite 使用了 catadioptric 镜头光圈形状——Pesce 认为这对 sprite-based DOF 没有实际意义，纯粹是"风格声明"
- 破坏系统大量预计算，动态破坏分级（总是相同碎裂 / 渐进破坏 / 脚本事件）
- 非常规灯光（tube light 无 specular）、scattering 效果疑为大半径 bloom + 粒子 flare

## 链接到的概念

- [[deferred-rendering]]
- [[specular-aliasing]]
- [[ssao]]
- [[pbr-practice]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2013/11/battlefield-4-review-graphics.html
- 本地：`raw/articles/c0de517e.blogspot.com/2013-11-01_battlefield-4-review-graphics.md`
