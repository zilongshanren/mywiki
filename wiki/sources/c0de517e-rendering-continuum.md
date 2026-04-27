---
tags: [source, rendering, forward-rendering, deferred-rendering, visibility-buffer, pipeline-taxonomy]
date: 2026-04-27
sources: 1
---

# The Real-Time Rendering Continuum: A Taxonomy（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2016 年 8 月的文章，对实时渲染管线的各种变体（Forward、Forward+、Deferred Shading、Visibility Buffer、Texture-Space Shading）做了系统性的分类学梳理，并给出了技术选型的决策框架。

## 摘要

Pesce 将各种渲染管线统一为一个连续体框架：所有管线都在做同一件事（从几何到像素颜色），区别在于在哪里"切断"管线，以及用什么数据结构把前半段和后半段连接起来。

Forward 是完整的单 pass；各种 Deferred 变体是在不同位置切断并写入屏幕空间 G-buffer；Visibility Buffer 是在光栅化最前段切断，只写 primitive id，后续 compute 重建；Texture-Space Shading 则是把中间结果写入 UV 空间纹理而非屏幕空间。每种切断方式都有相同的权衡轴：专化（specialization）、线程间数据共享、计算再排布（wave efficiency）。

对于 PS4 这一代，Pesce 认为"vanilla deferred shading 目前可行"，但指出可见性缓冲区（Visibility Buffer）和纹理空间着色是值得关注的方向。同时提出混合渲染器（deferred + F+ 共享光源表示）和 GPU 驱动管线的趋势。

## 关键要点

- Forward 的光源分配问题（几何切割 vs. uber-shader 排列组合爆炸）是理解所有 pipeline 变体的基础
- Deferred 的本质是"为了更好的 specialization 或数据共享而付出 G-buffer 带宽代价"
- Visibility Buffer：thin gbuffer（primitive id），后续 compute 做 material shading，消除 overdraw，但失去固定功能硬件（导数计算困难、顶点 cache miss 更多）
- Texture-Space Shading：类似 Quake 的 surface cache 思想，解耦 shading rate 与帧率，支持时域缓存；tradeoff 是 cache invalidation 频率与内存占用
- 自动调优（autotuning）理论上可以帮助 pipeline 选型，但现实中因数据结构全局关联而难以落地
- 建议：deferred 与 F+ 共享同一套光源数据结构，混合管线理论上可行

## 链接到的概念

- [[rendering-pipeline-taxonomy]]
- [[deferred-rendering]]
- [[forward-plus-rendering]]
- [[visibility-buffer]]

## 原文

- 链接：https://c0de517e.blogspot.com/2016/08/the-real-time-rendering-continuum.html
- 本地：`raw/articles/c0de517e.blogspot.com/2016-08-06_the-real-time-rendering-continuum-a-taxonomy.md`
