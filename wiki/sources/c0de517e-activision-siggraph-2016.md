---
tags: [source, rendering, siggraph, activision, black-ops-3, ambient-occlusion, antialiasing, shadows]
date: 2026-04-27
sources: 1
---

# Activision @ SIGGRAPH 2016（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2016 年 8 月的文章，汇总了 Activision/Treyarch 在 SIGGRAPH 2016 上的多篇演讲内容，均基于 Call of Duty: Black Ops 3 的成果。

## 摘要

本文覆盖五个技术方向：

**1. 体积化烘焙辐照度（Volumetric Irradiance Volumes）**：用硬件过滤的体积纹理取代传统 lightmap，作为唯一的烘焙辐照度表示。解决了 lightmap 的多个历史痛点（baking 时间、动静物体光照不连续、kit-bash 几何渗漏）。结合视差校正反射探针与 Josiah Manson 的快速 GGX 预积分方案。

**2. 稀疏阴影树（Sparse Shadow Trees, SST）**：Kevin Myers 主导的新一代压缩阴影贴图技术，实现对整个关卡的预烘焙阴影，压缩比可达千倍以上。与 precomputed voxelized shadows 不同，SST 便于恢复深度值，易于与体积光等效果集成。

**3. Filmic SMAA（Jorge Jimenez）**：时域重投影 + SMAA 的组合，在相同性能预算下超越 MSAA 质量。Pesce 认为时域重投影在抗锯齿领域已基本"获胜"；MSAA 仍有价值但定位转向混合分辨率效果而非边缘抗锯齿。

**4. Ground Truth Ambient Occlusion（GTAO）**：Jorge Jimenez、Xian Wu、Adrian Jarabo 与 Pesce 合作。基于对 ray-traced ground truth 的建模推导出解析解，在 HemiAO 的同等性能预算（0.5ms）下达到比 HBAO+ 更高的质量，已在生产中替换了 HemiAO。

**5. Catmull-Clark 细分曲面**：Wade Brainerd 的工作，延续自 COD: Ghosts（第一个大规模在游戏中使用 CC 细分的标题），通过 hull shader 的 L2 读写传入可变控制点数量绕过硬件 tessellation 管线的限制。

## 关键要点

- Volumetric irradiance volumes 统一了动态/静态/粒子/皮肤等所有对象的光照，消除了 lightmap 与动态 probe 的不连续
- SST 是稀疏层级结构，最近亲是 Scandolo 等人的 Compact Multiresolution Hierarchies，但独立开发
- Filmic SMAA 宣告"抗锯齿战争"基本结束；temporal reprojection 成为事实标准
- GTAO 的 closed-form analytic solution + residual fitting 方法论可推广到其他 screen-space 近似问题
- 体积 irradiance 的关键实现：艺术家手动放置裁剪凸多面体避免光照渗漏，复用了 reflection probe 的标注工作流

## 链接到的概念

- [[ground-truth-ambient-occlusion]]
- [[temporal-antialiasing]]
- [[cached-shadowmaps]]
- [[physically-based-shading]]
- [[deferred-rendering]]
- [[parallax-corrected-cubemap]]

## 原文

- 链接：https://c0de517e.blogspot.com/2016/08/activision-siggraph-2016.html
- 本地：`raw/articles/c0de517e.blogspot.com/2016-08-13_activision-siggraph-2016.md`
