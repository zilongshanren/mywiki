---
tags: [source, 渲染, 皮肤渲染, 次表面散射, 方法论]
date: 2026-04-27
sources: 1
---

# More Rules. On Skin Rendering（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2013 年 2 月的实践总结文章，是其 2011 年皮肤渲染"三大恐怖"系列的续篇，提炼出 5 条皮肤着色的方法论原则。原文因与 Jorge Jimenez 同期 GDC 2013 演讲内容存在独立交叉而被暂时下线，GDC 演讲结束后恢复发布。

## 摘要

文章不涉及具体技术细节（作者刻意回避以免泄露项目信息），而是从多年在多家工作室做角色渲染的经验出发，总结出 5 条跨技术方案的通用法则：关注细节并反复迭代、获取并使用高质量参考、必须做色调映射、理解不同光照现象的尺度范围、以及要同时处理所有光照分量和所有遮挡层次。文章将 Jorge Jimenez 的工作（Siggraph 2012 + GDC 2013）作为方法论典范反复推荐，视其为应用图形研发的范例。

## 关键要点

- **注意细节**：模型 → 调参（与美术合作）→ 对比参考，反复循环；推荐 Jimenez Siggraph 2012 作为该方法论的最佳示范
- **获取参考**：线性 HDR 照片为基础；解耦高光与漫反射以便单独调参；推荐 Debevec 的 light stage 数据、MERL/ETH 皮肤反射数据库
- **必须色调映射**：即便是 8-bit buffer 的老项目，皮肤高光若不做 tonemapping 会严重失真；White-balanced Reinhard 在资源紧张时勉强可用
- **理解尺度**：BRDF 的有效尺度、贴图纹素的尺度、几何的尺度各不相同，跨尺度套用同一模型会产生错误；skin specular 在近距离呈现出与 Cook-Torrance 假设不同的形态
- **完整光照与遮挡**：解析光、环境光、阴影、AO 都要同时考虑进 SSS 积分；用 `ambient * AO` 直接乘会丢失皮肤自散射的暖色调，需要在 AO 遮挡区域叠加额外红色反弹
- 推荐 Jimenez 的屏幕空间 SSS 方法优于 UV 空间方法，因其可以统一处理场景内所有光源

## 链接到的概念

- [[skin-rendering-practice]]
- [[preintegrated-skin-shading]]
- [[local-tonemapping]]
- [[microfacet-brdf]]

## 原文

- 链接：https://c0de517e.blogspot.com/2013/02/more-rules-on-skin-rendering.html
- 本地：`raw/articles/c0de517e.blogspot.com/2013-02-17_more-rules-on-skin-rendering.md`
