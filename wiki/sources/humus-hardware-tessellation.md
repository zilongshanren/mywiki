---
tags: [source, rendering, tessellation, dx11, hardware]
date: 2026-04-27
sources: 1
---

# Hardware Tessellation（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 发表于 2010 年 1 月的短文，梳理硬件曲面细分的三大优势及其局限。

## 摘要

Engel 归纳了 DirectX 11 硬件曲面细分的三个主要好处：**压缩**（仅存储粗网格，降低磁盘/显存占用及动画数据量）、**内存带宽**（GPU 仅通过 PCIe 读取粗网格顶点，提升顶点缓存命中率）、**可扩展性**（细分递归性使其天然适合自适应 LOD）。他同时指出 DX11 实现存在 hull/domain shader 的额外开销，可能抵消顶点着色器的节省。评论中的 Benualdo 补充了双抛物面阴影贴图与反射在曲面细分下质量大幅改善的案例，另有评论指出 DX11 并非真正递归细分——无法在子 patch 层面再次查询细分级别，限制了精细自适应 LOD 的实现。

## 关键要点

- 粗网格只经 PCIe 一次，细分在 GPU 内部完成，带宽压力转移
- Hull + Domain shader 总开销可能与顶点着色器减省相抵，真实收益需实测
- DX11 曲面细分不是真递归：TessFactor 需在 patch 粒度设定，子 patch 无法自主请求额外细分
- 双抛物面阴影贴图和反射因"几何无法弯曲"而引入错误，曲面细分可显著改善

## 链接到的概念

- [[rendering/tessellation-approaches-overview]]
- [[rendering/hull-domain-tessellation-urp]]
- [[rendering/deferred-rendering]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2010/01/hardware-tessellation.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2010-01-31_hardware-tessellation.md`
