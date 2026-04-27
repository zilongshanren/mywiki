---
tags: [source, rendering, 遮挡剔除, 体素, 点云, roblox]
date: 2026-04-27
sources: 1
---

# Half Baked: Dynamic Occlusion Culling（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2023 年 3 月的"半成品"笔记，记录在 Roblox 全动态场景下探索无美术干预遮挡剔除方案的思路轨迹。

## 摘要

文章围绕两条主线展开。实时路径延伸自 CryEngine 3 的 coverage buffer：把上一帧深度降采样重投影，并尝试从多历史视点构建 world-space occluder 数据库，用法线检测切割 depth heightfield。体素路径把深度缓冲反投影到稀疏二进制体素网格，借助 bit-pack compute shader 快速累积，兼论其与点云的等价性。主要遗留问题是世界空间体素的近处屏幕误差无上界，作者提出 splatted quads、屏幕空间降采样孔洞重建和 surface net 光追三种候选解法，偏好"混合"路线：上帧深度做初始 reprojection，体素数据库仅负责填孔。

## 关键要点

- 全动态场景要求 occluder 生成也是增量/实时的，静态 PVS 不适用
- 多视点 depth heightfield 可共同支撑一个持久化 occluder 数据库，动态对象通过视锥相交批量失效
- 稀疏二进制体素 ≡ 整数坐标点云（压缩后等价），binary 比任何"聪明"混合表示都简单
- 最大挑战：世界空间表示的屏幕误差随距离反变——越近越大；唯有混合 screen-space 才能规避

## 链接到的概念

- [[dynamic-occlusion-culling-roblox]]
- [[occlusion-culling]]
- [[hierarchical-z-buffer]]
- [[gpu-based-occlusion-culling]]
- [[efficient-sparse-voxel-octrees]]

## 原文

- 链接：https://c0de517e.blogspot.com/2023/03/half-baked-dynamic-occlusion-culling.html
- 本地：`raw/articles/c0de517e.blogspot.com/2023-03-15_half-baked-dynamic-occlusion-culling.md`
