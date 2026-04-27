---
tags: [source, 渲染, 光追, 混合渲染, 图像质量]
date: 2026-04-27
sources: 1
---

# Error Metrics for Smart Image Refinement（anteru.net）

[[matthaeus-chajdas]] 发表于 2025 年 2 月的研究页，介绍他早期关于**混合光栅 + 光追渲染**图像质量估计的工作。

## 摘要

扫线光栅化仍是实时渲染的主流；光线追踪虽然能生成更好的阴影、反射、折射和景深，但纯光追的性能成本在实时场景下不可接受。论文提出一个**GPU 混合系统**：先跑光栅渲染，然后对每个像素**估计**光追在此处能带来的质量提升指数（quality improvement index），对提升空间大的区域用光追重新着色。这是一种自适应的 "smart image refinement"——只在值得的地方花光追预算。

## 关键要点

- **核心思路**：光栅图是基准，光追只用于质量改善幅度显著的区域，由误差度量自动识别。
- **支持效果**：反射、景深（depth-of-field）、阴影——光栅器难以高质量表达的几类效果。
- **图像质量估计**：系统估计光栅与光追结果的差距，而非直接对比（因为此时光追结果还没算）；属于预测型度量。
- **GPU 实现**：整个流程在 GPU 上完成，符合实时渲染管线的集成需求。
- **历史背景**：论文发表于光追在消费级 GPU 上还很贵的年代，"混合"是当时的主要折中方向，与当今 [[hybrid-raytracing-pipeline|混合光追管线]] 的思路一脉相承。

## 链接到的概念

- [[hybrid-raytracing-pipeline]]
- [[hybrid-raytraced-shadows-reflections]]
- [[matthaeus-chajdas]]

## 原文

- 链接：https://anteru.net/research/error-metrics-for-smart-image-refinement
- 本地：`raw/articles/anteru.net/2025-02-16_error-metrics-for-smart-image-refinement.md`
