---
tags: [source, 渲染, 采样, 工具]
date: 2026-04-14
sources: 1
---

# Poisson disk/square sampling generator for rendering（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 8 月发布的小工具公告。一个 Python 脚本，离线生成 Poisson-like 分布的采样点序列，输出可以直接复制粘贴的 HLSL / C++ 数组。

## 摘要

文章是个简短的工具发布说明：[bartwronski/PoissonSamplingGenerator](https://github.com/bartwronski/PoissonSamplingGenerator)。和现有的 Poisson 采样生成器相比，这个脚本的特点是支持四种典型形状（disk、disk with central tap、square、repeating square），并且**生成的序列具有渐进性质——任意前 N 个点本身就是一个良好的 Poisson 分布**。这让自适应分支（例如 DoF 中根据 CoC 大小动态决定采样数）有了正确的方差行为。脚本还有一个可选的「按 tile 排序」选项，把序列按 n×n 桶重排以改善 cache locality。

## 关键要点

- **渐进序列**：前 N 个点也是良好的 Poisson 分布，支持自适应采样数。
- **四种形状**：disk / disk + central tap / square / repeating square——后者用于 screen-space tiling。
- **离线生成 + 烘进代码**：典型的图形小型常量数据工作流。
- **缓存优化（可选）**：tile 排序让相邻索引样本在空间上也相邻，对大内核 / 不连贯纹理访问降低 cache miss。
- **典型用途**：PCF / PCSS 阴影柔化、DoF bokeh、SSAO、importance sampling。

## 链接到的概念

- [[poisson-disk-sampling]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/08/08/poisson-disksquare-sampling-generator-for-rendering/
- 仓库：https://github.com/bartwronski/PoissonSamplingGenerator
- 本地：`raw/articles/bartwronski.com/2014-08-08_poisson-disk-square-sampling-generator-for-rendering.md`
