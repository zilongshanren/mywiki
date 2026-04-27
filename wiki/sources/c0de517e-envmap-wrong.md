---
tags: [source, rendering, ibl, physically-based-shading, cubemap, brdf]
date: 2026-04-27
sources: 1
---

# Oh envmap lighting, how do we get you wrong? Let me count the ways...（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2014 年 6 月的文章，系统罗列了基于 cubemap 的环境光照（IBL）实现中存在的各种近似误差，并为每个问题提供了对应的缓解方案。

## 摘要

文章以"标准 cubemap IBL 流程"（cosine-kernel 卷积漫反射、Phong mip 链镜面、运行时用反射向量取样）为基准，逐一列出其中的近似假设在什么情况下是错误的。核心错误来源可分为五类：

1. **反射向量 ≠ 半程向量**：cubemap 卷积核的对称轴是反射向量，但 Cook-Torrance BRDF 以半程向量为中心，二者在掠角差异显著；镜面波瓣在掠角被拉伸而非保持径向对称
2. **BRDF 不只是分布函数**：Fresnel 和阴影遮蔽项同样会"推移"波瓣中心，不仅仅是缩放；split-sum 方案（Brian Karis UE4）用 bias 修正了最大误差，但并非精确
3. **忽略遮挡**：任何简单缩放 envmap 来模拟遮挡的做法都是错的——遮挡应发生在预滤波之前；推荐方案：用反射向量方向的锥形 screen-space 或 voxel AO 来近似
4. **捕获位置误差**：cubemap 从单点捕获，但用于场景中其他位置时存在视差；parallax-corrected cubemap（盒体/球体 reproj）是常用缓解，但改变了预卷积的假设
5. **法线方差未处理**：强制 mip level 意味着没有对像素内法线分布做抗锯齿；正确做法是把法线方差推入 roughness（但该做法本身也有已知误差）

文章还提及 DX9/旧硬件的 cubemap 边缘连续性问题（block compression 跨 face 断裂）及其修复方法。

## 关键要点

- Split-sum（[[rendering/split-sum-approximation]]）用 bias 修正 FG 项偏移，实用但非精确
- 法线方差 → roughness 推移是必要做法，但 integral 形状与原 BRDF 在任何 roughness 下均不完全匹配
- 遮挡应在预滤波前处理；运行时的 renormalization（Black Ops 2 方案）是折衷
- Parallax-corrected cubemap（[[rendering/parallax-corrected-cubemap]]）与预卷积假设矛盾
- 验证手段：importance sampling 参考实现（慢但正确），与预过滤结果对比衡量误差
- 旧硬件 cubemap 边缘：DXT block 压缩导致跨 face 边缘不连续，需要同步 reference color

## 链接到的概念

- [[rendering/ibl-multiple-scattering]]
- [[rendering/split-sum-approximation]]
- [[rendering/parallax-corrected-cubemap]]
- [[rendering/microfacet-brdf]]
- [[rendering/physically-based-shading]]
- [[rendering/spherical-harmonics]]
- [[rendering/importance-sampling-pdf-cancellation]]
- [[rendering/specular-aliasing]]
- [[rendering/env-mapping-cubemap-shader]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/06/oh-envmap-lighting-how-do-we-get-you.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-06-25_oh-envmap-lighting-how-do-we-get-you-wrong-let-me-count-the.md`
