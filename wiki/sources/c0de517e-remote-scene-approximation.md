---
tags: [source, rendering, LOD, impostor, 远景近似, 点云, 场景传输, roblox]
date: 2026-04-27
sources: 1
---

# Exploring the Design Space of "Remote Scene Approximation"（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2023 年 9 月的工作日志式 R&D 报告，记录 Roblox 场景远景 LOD/传输方案探索的思路轨迹与多轮原型实验。

## 摘要

问题定义：把远处（或来自远端服务器）的任意多边形汤替换为更小的传输包，客户端实时渲染，优先保证运行时性能与内存，其次是下载带宽。核心约束是不假设场景有任何可被利用的逻辑结构，且源几何可能频繁变更。

文章以"分支—实验—归纳"为骨架，映射出一张从 octahedral impostor、billboard cloud、remeshing LOD 到 NeRF、Gaussian Splatting、点云深度图的解空间。主要发现：(1) Octahedral impostor 非凸几何上成立，但贴图尺寸极其浪费（需同时存颜色/法线/粗糙度多视角），不适合任意多边形汤；(2) 体素化 + QEM 简化 + 多视点光栅烘焙的流程在数秒内可出 10k 面代理网格，质量已经"可接受"；(3) Screened Poisson 重建从点云直接出封闭网格效果好且快；(4) 直接生成低多边形拟合 mesh（2D 验证通过，3D 风险仍存）。

贯穿全文的关键观察：点云/深度图/heightfield/八叉树体素之间存在等价连续谱，外观与可见性的解耦是优化传输效率的核心轴。

## 关键要点

- 视图无关表示对服务器友好，octahedral impostor 是成熟起点但带宽效率低
- 解耦可见性（深度 per viewpoint）与外观（UV + 属性）可大幅压缩传输量
- Poisson 重建 + 多视点光栅烘焙是目前验证最充分的流程
- "允许客户端 transcode 缓存" 可解锁更紧凑格式（如传深度图、客户端合成 billboard）
- 这类问题连通 stereo reprojection、lightfield、photogrammetry、NeRF 等一整条技术谱系

## 链接到的概念

- [[remote-scene-approximation]]
- [[dynamic-occlusion-culling-roblox]]
- [[gaussian-splatting-web]]
- [[occlusion-culling]]
- [[efficient-sparse-voxel-octrees]]
- [[nanite-reyes-comparison]]

## 原文

- 链接：https://c0de517e.com/007_impostors.htm
- 本地（blogspot 存根）：`raw/articles/c0de517e.blogspot.com/2023-12-08_exploring-the-design-space-of-remote-scene-approximation.md`
- 本地（c0de517e.com 全文）：`raw/articles/c0de517e.com/2023-09-05_exploring-the-design-space-of-remote-scene-approximation-a-w.md`
