---
tags: [rendering, shadows, csm]
date: 2026-04-19
sources: 1
---

# 级联阴影贴图（CSM）

级联阴影贴图（Cascaded Shadow Maps, CSM）把视锥沿深度切成若干段，给每段渲染一张独立分辨率的 shadow map，近处分辨率高、远处分辨率低，通过在采样阶段按深度挑选级联来缓解单张 shadow map 「近处锯齿、远处浪费」的固有矛盾。

Supnik 2011 年援引 NVIDIA 的 *GPU Programming Guide (G80)* 半开玩笑地指出：该指南对阴影技术的推荐是——「**除非你知道自己在做什么，否则就老老实实做 multi-tap cascaded shadow maps**」。他把这句话翻译为一句更直白的推论：如果你压根不知道自己在做什么，那就试 CSM，还能出什么乱子？——然后自嘲 X-Plane 10 恰好也走了 CSM 路线。

NVIDIA 指南顺口给出的经验值是「3 级对任何场景都够用」。Supnik 对此不买账：X-Plane 的 scene graph 是连续可视飞行距离（视野可达几十公里），3 级 CSM 根本吃不下这个深度范围，和典型的第三人称游戏场景不可同日而语。这条观察预示了他后来在 [[gpu-sliced-volumetric-shadows-limits]] 等文章里反复强调的主题：**通用 GPU 阴影经验不能无脑迁移到模拟飞行这类超大场景**。

与 CSM 配套需要关注的工程点：视锥分段方式（线性/对数/实用折中）、级联间边界过渡、samples 与 PCF 滤波、级联复用与缓存（见 [[cached-shadowmaps]]）、以及在大规模世界里的相机相对处理（见 [[camera-relative-sun-shadows]]）。

## Sources
- [[sources/supnik-csm-for-dummies]]
- [[sources/c0de517e-stable-csm-ideas]] —— Pesce 2011：stable CSM 实施要点（pancake / 最优级联 / 贴图打包）+ Crysis 2 阴影考古
