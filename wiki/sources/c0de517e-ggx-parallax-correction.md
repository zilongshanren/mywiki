---
tags: [source, rendering, ibl, cubemap, 视差修正, ggx, 粗糙度拟合]
date: 2026-04-27
sources: 1
---

# From the Archive: Notes on GGX Parallax Correction（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2023 年 4 月的存档笔记，整理了大约 2015 年为 [[parallax-corrected-cubemap]] 所做的 GGX 波瓣失真修正研究，此前从未公开。

## 摘要

[[parallax-corrected-cubemap]] 在高粗糙度下产生明显的 box proxy 平面跳变瑕疵，根本原因是预过滤时假设的 GGX 波瓣足迹与实际着色点处的足迹存在距离和角度双重差异。文章分两步处理这两个问题。第一步：对于"两个波瓣都垂直于同一平面、仅距离不同"的情况，可以把距离比率近似为粗糙度变化量，用数值拟合（alpha → alpha' + scale + offset）得到一个修正曲线，最后近似成从 cubemap mip 到调整后 mip 的解析函数。第二步：考虑非垂直交叉时各向异性尾部的影响——单次各向同性采样无论如何调整 mip 都难以匹配，作者的结论是：cubemap 应该按"垂直于 proxy 平面、固定距离"的核进行预过滤，然后在查询时仅做垂直情况下的距离—粗糙度修正，从而绕开各向异性问题。

## 关键要点

- 距离比越大，等效粗糙度越高；可用乘法 scale + 减法 offset 拟合，但 offset 不能真正用于 mip 选择（非零项集中在 alpha=1 边界）
- 交叉角度带来的各向异性尾部对视觉影响有限，真正的麻烦是烘焙时尾部"错位方向"留存在 cubemap mip 里形成瑕疵
- 根本修复思路：预过滤时就以垂直 proxy 平面为假设核，查询时仅做距离修正
- 精确公式已丢失，文章重点在推理方法而非具体数值

## 链接到的概念

- [[parallax-corrected-cubemap]]
- [[envmap-ibl-approximation-errors]]
- [[split-sum-approximation]]
- [[ggx-multiscattering-normalization]]

## 原文

- 链接：https://c0de517e.blogspot.com/2023/04/from-archive-notes-on-ggx-parallax.html
- 本地：`raw/articles/c0de517e.blogspot.com/2023-04-10_from-the-archive-notes-on-ggx-parallax-correction.md`
