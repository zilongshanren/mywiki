---
tags: [source, 渲染, 阴影, cube-shadow-map, 点光源, 椭球光源, esm]
date: 2026-04-27
sources: 1
---

# Shadows – Thoughts on Ellipsoid Light Shadow Rendering（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel]] 于 2011 年 2 月发表的技术文章，系统讨论开放世界游戏场景中椭球光源与点光源的阴影渲染方案，覆盖 cube shadow map 渲染、阴影缓存、bias、半影软化四大议题。

## 摘要

文章以一个模拟开放世界游戏需求（室内室外混合）的 demo 为出发点，分析四类阴影（云投影、角色自阴影、级联太阳阴影、点/聚光灯阴影），聚焦最后一类的工程挑战。Cube shadow map 相比双抛物面贴图提供更均匀的误差分布，利用几何着色器可以在一个 draw call 中渲染六个面；但几何着色器性能在某些 GPU 上不佳，需要将部分计算前移到顶点着色器。阴影缓存以「距离 + 屏幕像素大小 + 该光源范围内是否有移动物体」三参数驱动，可大幅降低每帧阴影 map 更新数量。Shadow bias 的传统方案对动态 cube shadow map 不可行，Salvi 的指数函数近似（ESM）是更稳健的替代。半影软化推荐概率滤波结合硬件滤波，作者自己实现了屏幕空间软化版本可同时管理 32 个软点光源阴影。

## 关键要点

- Cube shadow map 误差分布比双抛物面（dual-paraboloid）更均匀，是点/椭球光源阴影的首选存储
- 几何着色器一次 draw 渲染六面，但性能不稳定；将 viewProj 偏移前移到顶点着色器可提速
- 椭球光源（不同方向有独立衰减）同样可以存储于 cube map，无需特殊格式
- 阴影缓存策略：按距离、屏幕覆盖面积、区域内是否有运动物体共同决定是否更新
- ESM（指数阴影映射）用 `exp((pos.z - depth) * k)` 近似二值比较，规避 bias 参数的场景依赖性
- 屏幕空间 PCF 可以同时处理大量软点光源阴影（demo 展示了 16/32 个）
- 动态场景趋势：游戏开发者正在放弃预计算光照，走向完全实时的阴影与 GI

## 链接到的概念

- [[rendering/cube-shadow-map-rendering]]
- [[rendering/shadow-mapping-basics]]
- [[rendering/cached-shadowmaps]]
- [[rendering/moment-shadow-mapping]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2011/02/shadows-thoughts-on-ellipsoid-light.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2011-02-28_shadows-thoughts-on-ellipsoid-light-shadow-rendering.md`
