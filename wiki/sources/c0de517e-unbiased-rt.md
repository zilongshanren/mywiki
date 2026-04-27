---
tags: [source, rendering, 光线追踪, rtx, dxr, 实时渲染]
date: 2026-04-27
sources: 1
---

# An Unbiased Look at Real-Time Raytracing（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2019 年 3 月的文章，以「不带炒作、不带恐惧」的原则，给实时光追（DXR/RTX）的 R&D 方向提供务实建议。原稿写于 2018 年 GDC（DXR 公布后），拖了近一年才发布。

## 摘要

Pesce 用一组「DO / DO NOT」清单，梳理了当时实时光追研究中最容易走错的方向与最值得投入的方向。核心立场是：光追已经锁定在硬件里，不用争论要不要，只需判断如何研究才能真正落地并服务产品。

## 关键要点

- **DO NOT**：指望光追让渲染变简单——复杂度来自性能压力，光追只会增加混合管线的开发成本
- **DO NOT**：现在就优化性能/一致性——高端 GPU 足够暴力，但这不代表高效，长期不可持续
- **DO NOT**：把重点放在镜面反射——人眼对反射环境误差不敏感，cubemap 已经够用，而反射光追的 shading 开销极高
- **DO**：关注遮蔽（occlusion）——面积光正确阴影、间接光遮蔽，硬件友好，视觉收益大
- **DO NOT**：依赖 denoising 解决一切——低样本降噪会把高频噪声提升为低频 artifact，在动画下尤其糟糕
- **DO**：投资 caching 和 temporal accumulation——超出 screen-space 的长时间积累，比 denoising 更有根本价值
- **DO NOT**：用「RTX on vs RTX off」做对比——正确对比应包含「同等 GPU 预算给传统技术能做什么」
- **DO NOT**：假设场景复杂度已封顶——推更多资产往往比「更亮的着色效果」更有视觉冲击力
- **DO**：思考光追哪些情况能赢过光栅化——细粒度刷新（小区域 shadow map）、compute 单元全宽度使用
- **DO**：考虑工程成本和 fallback 方案——RTX 覆盖率低，fallback 不匹配会让内容制作更痛苦
- **DO**：寻找外部研究合作——RTX 不会直接卖游戏，内部资源不应全押

## 链接到的概念

- [[hybrid-raytracing-pipeline]]
- [[ray-tracing-api-debate]]
- [[raytracing-vs-rasterization]]
- [[temporal-antialiasing]]
- [[realtime-quality-vs-quantity]]

## 原文

- 链接：https://c0de517e.blogspot.com/2019/03/an-unbiased-look-at-real-time-raytracing.html
- 本地：`raw/articles/c0de517e.blogspot.com/2019-03-30_an-unbiased-look-at-real-time-raytracing.md`
