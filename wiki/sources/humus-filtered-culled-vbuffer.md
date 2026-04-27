---
tags: [source, 渲染, visibility-buffer, 剔除, cluster]
date: 2026-04-27
sources: 1
---

# GDCE 2016 – The Filtered and Culled Visibility Buffer（Wolfgang Engel）

[[people/wolfgang-engel]] 在 2016 年 GDCE 上发表的演讲摘要，一句话主题：将三角形过滤与多视图剔除整合进 [[visibility-buffer|Visibility Buffer]] 管线，同时服务主视图、阴影视图、反射视图、GI 视图等多个渲染目标。

## 摘要

这篇博文是演讲 PPT 的下载导引页，核心论点浓缩为五条执行摘要：系统以 cluster 为粒度同时对多个视图剔除并过滤三角形，将优化后的几何数据写入一个或多个屏幕空间 Visibility Buffer；后续的光照、阴影、间接光均在这套优化几何上进行；管线允许将几何可见性判断与着色频率分离，也支持逐三角形光照或 object-space 光照。具体实现细节（cluster 剔除算法、多视图 VB 布局、Forward++ 接入方式）需参阅 PPT 本身。

## 关键要点

- Cluster 剔除可同时处理主视图、多个阴影视图、反射视图和 GI 视图，节省多遍提交开销
- 每个视图对应独立的 Visibility Buffer，shading 时在正确的 VB 上查询
- 几何可见性与着色频率可解耦——某些 pass 可以降采样 shading 但保持完整几何精度
- 支持逐三角形光照（per-triangle lighting）与 object-space 光照两种模式

## 链接到的概念

- [[visibility-buffer]]
- [[culling]]
- [[deferred-rendering]]
- [[async-compute]]
- [[the-forge-renderer]]
- [[triangle-filtering-pipeline]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2016/08/gdce-2016-filtered-and-culled.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2016-08-22_gdce-2016-the-filtered-and-culled-visibility-buffer.md`
