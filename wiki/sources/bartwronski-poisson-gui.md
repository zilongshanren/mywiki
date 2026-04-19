---
tags: [source, 渲染, 采样, 工具]
date: 2026-04-19
sources: 1
---

# Updated Poisson-like generator with GUI and more（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 9 月的短篇更新笔记，交代他的 [PoissonSamplingGenerator](https://github.com/bartwronski/PoissonSamplingGenerator) 工具又加了哪些功能。

## 摘要

这篇是对一个既有工具的增量说明：作者给面向渲染的 [[poisson-disk-sampling|Poisson 盘 / 方形采样生成器]] 套了一层 PyQt 做的 GUI，支持「带旋转的 disk」模式（给 bokeh / PCF 阴影用——即使旋转整个采样集，样本之间的距离约束也仍然满足），补了更直观的可视化，并顺手调优了底层算法。作者同时预告要写一篇「把 Python 当作 Mathematica 的开源替代」的长文，梳理科学计算环境里他踩过的坑。对 wiki 来说，这篇主要的价值是补一个历史脉络：Wronski 持续把图形里的离线预计算（采样图案、核系数）从 Mathematica 迁到开源 Python，这是他后来一整条「Jax + Colab 做 data-driven filter design」路线的起点。

## 关键要点

- **旋转不变的 disk 采样**：除了普通 Poisson disk，新增「旋转后仍保持最小距离」的变体——直接服务 [[scatter-bokeh-dof|scatter bokeh DoF]] 和 PCF 软阴影在运行时对采样集随机旋转的做法。
- **GUI 不是目的**：Wronski 自嘲加 GUI 主要是为了学 PyQt，但之后能交互地调参、实时看可视化对生产力显著提升，这和 [[tools-first-iteration-loop|工具优先]] 的理念一致。
- **Python 作为 Mathematica 的开源替代**：作者提及长文预告（即后来的「Python as scientific toolbox」），主张 numpy + matplotlib + 一个脚本即可替代大多数 Mathematica 场景；wiki 里这条线一直延伸到他 2020 年用 [[iir-filter-deconvolution|Jax 做梯度下降滤波器设计]]。

## 链接到的概念

- [[poisson-disk-sampling]]
- [[scatter-bokeh-dof]]
- [[tools-first-iteration-loop]]

## 原文

- 链接：https://bartwronski.com/2014/09/05/updated-poisson-like-generator-with-gui-and-more/
- 本地：`raw/articles/bartwronski.com/2014-09-05_updated-poisson-like-generator-with-gui-and-more.md`
