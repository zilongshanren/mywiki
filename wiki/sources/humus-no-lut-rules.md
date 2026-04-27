---
tags: [source, 图形, 软件设计, 查找表, 设计原则]
date: 2026-04-27
sources: 1
---

# No Look-up Tables: Rules for Designing Graphics Sub-systems Part II（Wolfgang Engel）

[[wolfgang-engel]] 发表于 2011 年 7 月的文章，"图形子系统设计规则"系列第二部分，阐述"避免查找表"设计原则。

## 摘要

文章指出，随着 GPU 算术吞吐的持续增长而内存带宽趋于停滞，传统的"打表换计算"策略已经不再有利。Engel 把"查找表"的概念扩展到 lightmap、shadow map、radiosity map、signed distance field、voxel 等所有预烘焙数据形式，认为应尽量以实时算术替代。他同时承认完全避免缓存是不现实的，提出"在 GPU 显存中缓存中间结果"作为折中——配合可见性驱动（只对可见且足够大的对象生成数据）、级联方案（CSM、Cascaded RSM）和屏幕空间技术（Screen-Space GI 使用已有 G-Buffer）来降低实时计算的总量。此文是系列第二篇，系列包括第一篇 Screen-Space 原则和本批次的第三篇均匀误差分布原则。

## 关键要点

- GPU 算术 > 带宽：算术越来越"便宜"，带宽越来越珍贵
- LUT 范围扩展：不只是 sin/cos 表，也包括 lightmap、shadowmap、SDF、voxel 等
- 预烘焙数据导致几何不可破坏（destructible geometry 不能用 lightmap）
- 折中策略：GPU 显存缓存 + 可见性剔除 + 级联方案 + 屏幕空间
- 该原则是 Engel"图形子系统设计规则"系列的核心之一

## 链接到的概念

- [[graphics-subsystem-no-lut]]
- [[graphics-subsystem-even-error-distribution]]
- [[cascaded-shadow-maps]]
- [[screenspace-reflections]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2011/07/no-look-up-tables-rules-for-designing.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2011-07-03_no-look-up-tables-rules-for-designing-graphics-sub-systems-p.md`
