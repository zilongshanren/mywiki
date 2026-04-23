---
tags: [source, 渲染, 交互, 拾取, mouse-picking, 坐标空间]
date: 2026-04-19
sources: 1
---

# 3-d Mouse Testing（Ben Supnik）

[[ben-supnik|Ben Supnik]] 2013-10-03 修完 BrickSmith 一个长期 culling bug 后，把三种 3D 模型鼠标拾取坐标空间的选型拉到一张表上对比。

## 摘要

Supnik 把 BrickSmith 演进过程中用过的三种 hit-test 方案写清楚：(1) **Modelview space ray-triangle**：Möller-Trumbore，hit depth 副产出、不需求逆子变换，但没有剔除、扫全模型；(2) **Screen space**：把三角形正向投到 clip + 透视除法得到 2D 图元，AABB test 白菜价，层级 bounds 能剔一大片，**大模型 pick 比方案 A 快 10–50 倍**；(3) **Clip-space / eye-space** 未实现的备选。方案 B 踩到的坑是近裁剪面：**walk-through camera** 让用户进入模型内部后，跨 Z=0 的 AABB 在摄像机后半部被 W<0 镜像，整个 AABB 聚到屏幕同侧被误剔，表现为"模型随机消失"。修复"愚蠢但有效"——**透视除法前**先在 clip space 做近裁剪（AABB 12 条边 → 新点集 → 新 AABB；三角形 → 0/1/2 个新三角形）。X-Plane 走的是第三条：**eye-space + 平面侧性测试**，ray-triangle 直接在 model 自身坐标系解（sub-transform 都是简单旋转 / 平移，ray 求逆便宜）。

## 关键要点

- Modelview / Screen / Eye 三种空间各有一组特定坑，没有普适最佳。
- 屏幕空间 hit-test 便宜、层级 bounds cull 尤其有效，代价是**模型必须始终位于近裁剪面之后**这一隐含前提。
- 当"编辑器相机进入模型"这一需求出现，screen-space 方案需补 clip-space 裁剪或切换到 eye-space / 齐次坐标方案。
- Supnik 归结为"抽象的泄漏"：bug 不在数学，在坐标空间选型时的前提悄悄失效。

## 链接到的概念

- [[mouse-picking-coordinate-spaces]]
- [[coordinate-spaces]]
- [[culling]]
- [[occlusion-culling]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2013/10/3-d-mouse-testing.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-10-03_3-d-mouse-testing.md`
