---
tags: [source, 渲染, 全局光照, 虚拟点光源, 路径追踪, agraphicsguynotes]
date: 2026-04-27
sources: 1
---

# Instant Radiosity in my Renderer（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2016 年 2 月的文章，记录在 SORT 渲染器中实现 Instant Radiosity 算法的过程，分析算法的数学推导、工件处理（热点修复）以及与路径追踪的收敛速度对比，结论是算法实用性受限。

## 摘要

Instant Radiosity 与 Light Tracing 的区别在于顶点连接方式：LT 把光路顶点直接连到相机，IR 把光路顶点连到主光线（primary ray）的交点——相当于在场景中预先分布大量虚拟点光源（VPL），再对每个像素只做"直接光照"（对真实光源 + 所有 VPL）。VPL 是全局预计算的，不是每个样本独立生成，这是它与 BDPT 的最大区别。文章推导了两阶段的积分分解：预处理阶段沿光路累积 BSDF × G 项存于顶点；采样阶段只需追踪一段主光线并查询最近 VPL 的贡献。主要工件：镜面物体接近黑色（delta BSDF 无法处理）、Cornell Box 拐角出现亮斑（相邻顶点连接时 $1/r^2$ 爆炸）。亮斑修复采用 G 项截断 + 递归补偿方案（拆成 $G_0 + G_1$，$G_1$ 部分退化为路径追踪防止近距离连接），数学上保持无偏。实验表明即便用 1024 条光路，收敛速度仍比 MIS BDPT 慢近一倍，作者最终放弃此算法。

## 关键要点

- 与 BDPT 的关系：IR 是 BDPT 的子集——只考虑相机侧路径长度恰好为 2（一段主光线）的情形
- VPL 复用：光路顶点为所有像素样本共享，而非每样本独立生成，因此额外 VPL 的边际成本很低
- Delta BSDF 支持差：镜面材质必须特殊处理，作者的 SORT 渲染器中粗糙度为 0 的 microfacet 无法正确处理
- 近邻热点（hot spot）修复：将 G 项拆为截断部分 $G_0$（直接计算）和超限部分 $G_1$（退化为 PT 递归求解），无偏
- 实用结论：对一般场景 IR 收敛速度劣于 BDPT 和 PT，仅在特定间接光主导场景有优势

## 链接到的概念

- [[instant-radiosity-vpl]]
- [[path-tracing-basics]]
- [[gpu-unbiased-path-tracing]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/instant_radiosity_in_my_renderer/
- 本地：`raw/articles/agraphicsguynotes.com/2016-02-08_instant-radiosity-in-my-renderer.md`
