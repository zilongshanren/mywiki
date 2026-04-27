---
tags: [source, 渲染, 路径追踪, 蒙特卡洛, 全局光照]
date: 2026-04-27
sources: 1
---

# Basics about Path Tracing（Jiayin Cao / A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2015 年 7 月的文章，从渲染方程出发推导路径追踪算法的数学基础与工程实现要点。

## 摘要

文章从渲染方程的递归性入手：$L_o$ 依赖 $L_i$，而 $L_i$ 本质上是另一个方向的 $L_o$，形成无穷嵌套。作者展开到 $n$ 次弹射的贡献 $P(n)$，将全局解写成 $\sum_{n=1}^{\infty} P(n)$，清晰说明为什么 Whitted 光线追踪无法模拟颜色溢出（需至少 2 次弹射）。生成特定步数路径时，方向采样遵循余弦加权 pdf 效果最好；最后一个顶点应落在光源上以降低方差。俄罗斯轮盘赌（Russian roulette）以有限资源无偏地截断无穷弹射：以概率 $T$ 继续时将权重除以 $T$，以 $1-T$ 概率终止，期望保持不变。实现层面作者给出路径复用优化（一条路径的所有前缀均可贡献）与多线程 tile 调度的简要说明。

## 关键要点

- 路径追踪是无偏（unbiased）且一致（consistent）的算法，样本足够多时收敛到物理正确值。
- 重要性采样：pdf 越接近被积函数（brdf × cosine × radiance）方差越低；radiance 分布未知时退而按 cosine 或 brdf 采样。
- 小光源 + 漫反射面 → 优先采样光源；大面积光 + 高光面 → 优先采样 brdf；MIS 两者兼顾。
- Photon mapping 是一致但有偏的替代方案。

## 链接到的概念

- [[path-tracing-basics]]
- [[monte-carlo-integration]]
- [[importance-sampling-pdf-cancellation]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/basics_about_path_tracing/
- 本地：`raw/articles/agraphicsguynotes.com/2015-07-20_basics-about-path-tracing.md`
