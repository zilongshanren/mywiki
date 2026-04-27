---
tags: [source, 渲染, 路径追踪, 双向路径追踪, 蒙特卡洛, agraphicsguynotes]
date: 2026-04-27
sources: 1
---

# Naive Bidirectional Path Tracing（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2016 年 1 月的文章，记录在 SORT 渲染器中实现朴素双向路径追踪（BDPT）的过程，对比路径追踪（PT）、光线追踪（LT）和 BDPT 在特定场景下的收敛速度差异。

## 摘要

文章从渲染方程出发，推导路径对应的完整积分表达式，然后逐一分析三种路径策略的 PDF：路径追踪（从相机出发，按 BSDF 采样）、光线追踪（从光源出发，需显式连接相机）和双向路径追踪（两端同时生成路径并连接所有顶点对）。核心困难在于：BDPT 需要正确计算连接顶点间的几何项 $G(x_i \leftrightarrow x_{i+1})$（不能被 PDF 约掉），且任何细微错误（缺失 G 项、符号错误）都会导致渲染结果收敛到错误值，极难调试。作者采用"朴素平均"策略——对同等长度路径的所有拆分方案取均等权重（$1/n$），指出这比 MIS 加权差，留作后续工作。实验场景中顶部聚光灯朝右上射，导致大部分区域靠间接光照亮，此场景对 PT 非常不友好；LT 在该场景表现最好，BDPT 居中，PT 噪声最多。

## 关键要点

- BDPT 是 PT 和 LT 的超集：它同时生成相机路径和光源路径，连接所有组合——PT 和 LT 各自只是其中的特殊情形
- 调试难度极高：缺少一个 G 项、Fresnel 求值方向错误等微小 bug 都会产生偏差但仍收敛，肉眼和工具都难以定位
- 连接顶点的 G 项不可消除：$G(x_{eye} \leftrightarrow x_{light})$ 在两端路径连接时不会被 PDF 约分，必须显式计算
- 朴素加权（naive BDPT）用 $1/n$ 平均同等长度的所有拆分，噪声比 MIS 加权差，但实现简单
- 场景友好性：聚光灯 + 朴素 Cornell Box → LT 最优；含镜面物体 → PT 更稳；一般场景 BDPT 综合表现较好

## 链接到的概念

- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[gpu-unbiased-path-tracing]]
- [[instant-radiosity-vpl]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/naive_bidirectional_path_tracing/
- 本地：`raw/articles/agraphicsguynotes.com/2016-01-03_naive-bidirectional-path-tracing.md`
