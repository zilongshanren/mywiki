---
tags: [source, rendering, ocean, water, gerstner-wave, planet-engine, outerra]
date: 2026-04-27
sources: 1
---

# Ocean Rendering（Outerra）

[[people/outerra-team]] 发表于 2011 年 2 月的文章，介绍 Outerra 行星引擎的海洋渲染方案：开阔海域的 Gerstner 波叠加，以及海岸线附近的折射破碎浪。

## 摘要

系统将两类波形混合：**开阔海域波**以多个 Gerstner（trochoidal）波叠加写入一张 2D 贴图后无缝 tile；**海岸波**则依据岸线距离贴图动态定向并引入斜率参数模拟破浪（skewed trochoidal wave）。

开阔海域波的频率须满足整数峰数约束以保证可 tile；振幅限制在波长 1/20 以内；波速公式 $v = \sqrt{g\lambda/2\pi}$；方向通过各分量振幅权重偏向主风方向，逆向分量可完全抑制（适用于河流）。海岸波的核心是**岸线距离图**：对含有水陆边界的 tile，shader 寻找最近异类（水/陆）点并输出距离，再经 Sobel 滤波得到梯度向量用于波浪朝向；距离图作为波形函数的自变量，结合时间控制泡沫掩码使破浪不连续出现。水色由 RGB 分量的**吸收深度**（默认 7/30/70 m）决定；散射系数在纯水中可忽略，主要贡献来自溶解有机物。

## 关键要点

- 开阔海域：Gerstner 波整数峰约束 + 振幅 < 波长/20 + 风向振幅权重
- 海岸波：岸线距离图 + skewed trochoidal + Sobel 梯度 + 时变泡沫掩码
- 水色：RGB 吸收深度参数化，散射贡献主要来自有机物
- 地形 patch mesh 同时用于海面，顶点动画而非纯法线/贴图动画
- 文章末尾列出待做项：更好的破浪几何、adaptive 波频谱、气候化海洋参数等

## 链接到的概念

- [[gerstner-wave-ocean-rendering]]
- [[planet-terrain-dem-pipeline]]

## 原文

- 链接：https://outerra.blogspot.com/2011/02/ocean-rendering.html
- 本地：`raw/articles/outerra.blogspot.com/2011-02-18_ocean-rendering.md`
