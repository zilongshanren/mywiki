---
tags: [source, 采样, poisson-disk, ssao, processing, 离线工具]
date: 2026-04-19
sources: 1
---

# Stupid sample generator - 3d version（C0DE517E / Angelo Pesce 2010-12-15）

[[angelo-pesce]] 2010 年 12 月贴出的一段 Processing 小程序，把 [[poisson-disk-sampling|Poisson-disk]] 家族的思路扩展到**带重要性权重的半球采样点生成**——每个点的排斥半径由一个 importance 函数决定，于是密度非均匀、但由作者显式控制。

## 摘要

32 个点随机撒进 `[-1,1]^3` 立方体，每帧做一轮松弛：先把越界点投影回单位半球、把 `z<radius` 的点顶到 z=radius 约束在上半球；再对每个点随机抽 50 个邻居，若间距小于 `importance × mindist` 就沿连线互相推开——是**stochastic Lloyd relaxation**。importance 函数 `1.3 - (z/scale + z/len)/2` 让靠顶（仰角大）的点半径小、密度大，契合 [[ground-truth-ambient-occlusion|AO 的 cosine-weighted]] 积分。鼠标右键加噪声跳出局部最优、中键收紧半径、左键 dump 点与权重，并打印"已生成点的球体积 / 理论半球体积"比率作为覆盖指标。这份 sketch 是 SSAO / PCF 预计算工作流的原始形态，比 [[bartosz-wronski|Bart Wronski]] 后来的 Poisson Sampling Generator 早八年左右；后者补上了渐进性、tile 排序、四种几何域等工业特性，但思路内核一致。

## 关键要点

- **importance 本地化在排斥半径里**，不需要后处理乘 weight
- 松弛式 Poisson-disk 是 Bridson / Mitchell best-candidate 的另一条路径，换"前缀性"为"Voronoi 更均匀"
- 体积比率（`unit_hemisphere_volume / sum(point_volumes)`）是作者选用的覆盖标量
- 硬编码的 shape constraint（半球 / 球）可以按需要改成 disk / square 等其它域
- 这是典型"离线生成 + 烘进代码"的图形工作流样本

## 链接到的概念

- [[iterative-sample-point-relaxation]]
- [[poisson-disk-sampling]]
- [[ground-truth-ambient-occlusion]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/12/stupid-sample-generator-3d-version.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-12-15_stupid-sample-generator-3d-version.md`
