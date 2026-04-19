---
tags: [source, 渲染, disney-animation, hyperion, fur, 毛发, 路径追踪]
date: 2026-04-19
sources: 1
---

# Zootopia（Yining Karl Li / Code & Visuals）

[[yining-karl-li]] 2016 年 2 月在《Zootopia》北美上映前三周发表的博客，记录他加入 [[hyperion-renderer]] 团队后经历的第一部长片，并用大量 SIGGRAPH 2016 论文引用勾勒出 *Zootopia* 技术上的复杂度挑战。

## 摘要

Yining 2015 年 7 月入职 Disney Animation，在 *Zootopia* 上的个人职责较小——主要做 Hyperion 针对 *Zootopia* 版本的支持和 bugfix，当时署名榜编完时他还没转正，因此并未被列入片尾 credits——精力重心已经在下一部《Moana》的 Hyperion 版本上。即便如此，他把 *Zootopia* 描述为「迄今为止技术上最先进的动画长片」，在 *Big Hero 6* 的基础上又推进了一个量级，核心难题可以压缩成一个字：**复杂度**。毛发、布料、布料叠毛发、生态环境、人群、肉体模拟，每一块都逼出新的系统或新的 BSDF。

## 关键要点

- **Fur / Cloth on Fur**：Burkard et al. 2016 *From Armadillo to Zebra* 记录了多样化动物角色的毛发方案；Palmer & Litaker 2016 讲毛发 LOD，让作者侧和渲染侧都承担得起。
- **Chiang 毛发 BSDF**：Chiang et al. 2016 *A Practical and Controllable Hair and Fur Model for Production Path Tracing*（CGF/Eurographics）——Hyperion 团队为 *Zootopia* 开发、兼顾艺术可控性、物理合理性与渲染效率的全新毛发着色模型，日后成为行业事实标准，*Zootopia 2* 仍基本沿用（[[hyperion-renderer]] 说明）。
- **Crowds**：El-Ali et al. 2016 的 Zootopia Crowd Pipeline，解决 authoring + rendering 双侧的 tractability。
- **植被**：Keim et al. 2016 Art-Directable Procedural Vegetation——丛林大量程序化植被。
- **肉体模拟**：Milne et al. 2016 *Flesh, Flab, and Fascia Simulation* 是 Disney Animation 首次在长片上部署的肌肉/脂肪/筋膜模拟系统，专门为毛皮下面的可信肌肉运动而做。
- **冰淇淋**：Byun et al. 2016 讲 non-simulation 的冰淇淋效果实现——细节尺度上的 CG 创新。
- 全片 100% 用 Hyperion 渲染；文章末尾的剧照全部来自 Disney Animation。
- 叙事基调：谦逊、产线视角——「伟大品质是艺术家用工具做出来的，工具开发者只提供了工具」。

## 链接到的概念

- [[hyperion-renderer]]
- [[yining-karl-li]]
- [[wavefront-path-tracing]]

## 原文

- 链接：<https://blog.yiningkarlli.com/2016/02/zootopia.html>
- 本地：`raw/articles/blog.yiningkarlli.com/2016-02-12_zootopia.md`
